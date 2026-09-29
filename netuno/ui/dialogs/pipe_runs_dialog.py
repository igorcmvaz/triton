"""Organização dos trechos de tubulação para a planta 3D.

O projetista posiciona os componentes e lista os trechos na ordem de montagem.
Cada trecho parte de um componente, do fim de um trecho anterior ou, com a origem
em branco, do fim do trecho imediatamente acima. A validação e a prévia
o esquema 3D usam o mesmo núcleo que gera o DXF, para que o que se vê aqui seja o
que será exportado. A organização é salva mesmo com erros, porque é trabalho em
andamento; quem recusa uma organização inválida é a exportação.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog, QHBoxLayout, QHeaderView,
    QLabel, QMessageBox, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem,
    QTabWidget, QVBoxLayout, QWidget,
)

from netuno.core.bim_exporter import COMPONENT_TYPES, build_bim_manifest, validate_bim_manifest
from netuno.core.pipe_network import PIPE_SYSTEMS, format_route, parse_route
from netuno.core.schematic_3d import generate_schematic_3d_svg
from netuno.core.volumetry import build_volumetry
from netuno.core.volumetry_export import write_glb, write_html_viewer
from netuno.ui.translation import tr
from netuno.ui.volumetry_view import VolumetryPanel


COMPONENT_COLUMNS = ["ID", "Tipo", "X (mm)", "Y (mm)", "Z (mm)", "Rotação (°)", "Nível"]
RUN_COLUMNS = ["ID", "Sistema", "DN (mm)", "Material", "Origem", "Percurso", "Destino"]
_NUMBER_TRIPLE = re.compile(r"^\s*(-?\d+(?:[.,]\d+)?)[\s;]+(-?\d+(?:[.,]\d+)?)[\s;]+(-?\d+(?:[.,]\d+)?)\s*$")


def parse_origin(text: str) -> Optional[Any]:
    """``""`` → continua o anterior; ``"x y z"`` → coordenadas; senão, referência."""
    text = (text or "").strip()
    if not text:
        return None
    match = _NUMBER_TRIPLE.match(text)
    if match:
        x, y, z = (float(value.replace(",", ".")) for value in match.groups())
        return {"x": x, "y": y, "z": z}
    return text


def format_origin(value: Any) -> str:
    if isinstance(value, dict) and {"x", "y", "z"} <= set(value):
        return " ".join(f"{float(value[k]):g}" for k in ("x", "y", "z"))
    if isinstance(value, dict):
        return str(value.get("instance_id") or value.get("run_id") or "")
    return "" if value is None else str(value)


class PipeRunsDialog(QDialog):
    """Editor de componentes posicionados e trechos em sequência."""

    def __init__(self, parent=None, layout: Optional[Dict[str, Any]] = None, project_data: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.setWindowTitle(tr("Organizar trechos de tubulação — planta 3D"))
        self.resize(1280, 900)
        self._project_data = dict(project_data or {})
        # Parâmetros das famílias (capacidade, potência...) não aparecem na
        # tabela, mas são preservados por linha para não se perderem ao salvar.
        self._extra_component_parameters: Dict[int, Dict[str, Any]] = {}
        layout = layout or {}

        root = QVBoxLayout(self)
        intro = QLabel(tr(
            "Coordenadas locais em mm, z para cima. Os trechos são montados de cima para baixo: "
            "origem em branco continua do fim do trecho anterior. Percurso: '+x 3000; desce 1200; "
            "d 2000 0 -20' (d = deslocamento livre, para declividade). O destino é conferido, não completado. "
            "Pontos de conexão: RS-01:topo, RS-01:fundo, RS-01:sup+x, RS-01:inf-y… — ligue recalque e "
            "distribuição em pontos distintos; tubos que ocupam o mesmo espaço são recusados."
        ))
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #475569; font-size: 11.5px;")
        root.addWidget(intro)

        splitter = QSplitter(Qt.Vertical)
        self._valid_data: Optional[Dict[str, Any]] = None
        splitter.addWidget(self._build_components_box(layout.get("bim_components") or [], layout.get("building_volume") or {}))
        splitter.addWidget(self._build_runs_box(layout.get("pipe_runs") or []))
        splitter.addWidget(self._build_preview_box())
        splitter.setSizes([200, 200, 480])
        root.addWidget(splitter, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr("Salvar organização"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancelar"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)
        self.refresh_preview()

    # ── Componentes ──

    def _build_components_box(self, components: List[Dict[str, Any]], building: Dict[str, Any]) -> QWidget:
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        head = QHBoxLayout()
        title = QLabel(tr("<b>1. Componentes posicionados</b>"))
        head.addWidget(title)
        head.addStretch()
        for label, slot in ((tr("+ Componente"), self.add_component), (tr("− Remover"), self._remove_component)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            head.addWidget(btn)
        lay.addLayout(head)
        self.table_components = QTableWidget(0, len(COMPONENT_COLUMNS))
        self.table_components.setHorizontalHeaderLabels([tr(c) for c in COMPONENT_COLUMNS])
        self.table_components.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lay.addWidget(self.table_components)
        for item in components:
            self.add_component(item)
        lay.addLayout(self._build_building_row(building))
        return box

    def _build_building_row(self, building: Dict[str, Any]) -> QHBoxLayout:
        """Edificação para a volumetria: prisma retangular a partir da origem (canto)."""
        row = QHBoxLayout()
        row.addWidget(QLabel(tr("<b>Edificação</b> (volumetria, opcional; 0 = sem edificação):")))
        origin = building.get("origin_mm") or {}
        self.building_fields: Dict[str, QDoubleSpinBox] = {}
        for key, label, value, low in (
            ("x", tr("canto x"), origin.get("x", 0), -1e6), ("y", tr("canto y"), origin.get("y", 0), -1e6),
            ("z", tr("cota"), origin.get("z", 0), -1e5), ("width_mm", tr("largura x"), building.get("width_mm", 0), 0),
            ("depth_mm", tr("profund. y"), building.get("depth_mm", 0), 0), ("height_mm", tr("altura"), building.get("height_mm", 0), 0),
        ):
            spin = QDoubleSpinBox()
            spin.setRange(low, 1e6)
            spin.setDecimals(0)
            spin.setSingleStep(100)
            spin.setSuffix(" mm")
            spin.setValue(float(value or 0))
            spin.setToolTip(label)
            row.addWidget(QLabel(label))
            row.addWidget(spin)
            spin.editingFinished.connect(self.refresh_preview)
            self.building_fields[key] = spin
        self.spin_floors = QSpinBox()
        self.spin_floors.setRange(1, 60)
        self.spin_floors.setValue(int(building.get("floors") or 1))
        self.spin_floors.editingFinished.connect(self.refresh_preview)
        row.addWidget(QLabel(tr("pavimentos")))
        row.addWidget(self.spin_floors)
        row.addStretch()
        return row

    def _building_from_fields(self) -> Dict[str, Any]:
        f = self.building_fields
        if not all(f[k].value() > 0 for k in ("width_mm", "depth_mm", "height_mm")):
            return {}
        return {
            "origin_mm": {k: f[k].value() for k in ("x", "y", "z")},
            "width_mm": f["width_mm"].value(), "depth_mm": f["depth_mm"].value(),
            "height_mm": f["height_mm"].value(), "floors": self.spin_floors.value(),
        }

    def add_component(self, item: Optional[Dict[str, Any]] = None) -> None:
        item = item if isinstance(item, dict) else {}
        table = self.table_components
        row = table.rowCount()
        table.insertRow(row)
        combo = QComboBox()
        for spec in COMPONENT_TYPES:
            combo.addItem(spec["type_id"], spec["type_id"])
        index = combo.findData(item.get("type_id", COMPONENT_TYPES[0]["type_id"]))
        combo.setCurrentIndex(max(index, 0))
        pos = item.get("position_mm") or {}
        table.setItem(row, 0, QTableWidgetItem(str(item.get("instance_id") or f"C-{row + 1:02d}")))
        table.setCellWidget(row, 1, combo)
        for col, key in ((2, "x"), (3, "y"), (4, "z")):
            table.setItem(row, col, QTableWidgetItem(f"{float(pos.get(key, 0) or 0):g}"))
        table.setItem(row, 5, QTableWidgetItem(f"{float(item.get('rotation_deg', 0) or 0):g}"))
        table.setItem(row, 6, QTableWidgetItem(str(item.get("level") or "Nível 0")))
        self._extra_component_parameters[row] = dict(item.get("parameters") or {})

    def _remove_component(self) -> None:
        row = self.table_components.currentRow()
        if row >= 0:
            self.table_components.removeRow(row)
            params = self._extra_component_parameters
            self._extra_component_parameters = {
                (r if r < row else r - 1): p for r, p in params.items() if r != row
            }

    # ── Trechos ──

    def _build_runs_box(self, runs: List[Dict[str, Any]]) -> QWidget:
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        head = QHBoxLayout()
        head.addWidget(QLabel(tr("<b>2. Trechos na ordem de montagem</b>")))
        head.addStretch()
        for label, slot in (
            (tr("+ Trecho"), self.add_run), (tr("− Remover"), self._remove_run),
            (tr("▲ Subir"), lambda: self.move_run(-1)), (tr("▼ Descer"), lambda: self.move_run(1)),
            (tr("↻ Validar e pré-visualizar"), self.refresh_preview),
        ):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            head.addWidget(btn)
        lay.addLayout(head)
        self.table_runs = QTableWidget(0, len(RUN_COLUMNS))
        self.table_runs.setHorizontalHeaderLabels([tr(c) for c in RUN_COLUMNS])
        port_help = tr("Componente com ponto de conexão opcional: CI-01, RS-01:topo, RS-01:fundo, "
                       "RS-01:sup+x (lateral a 85 % da altura), RS-01:inf-y (lateral a 12 %).")
        for col, text in ((4, port_help + " " + tr("Em branco: continua do fim do trecho anterior. Também aceita um trecho (T-01) ou 'x y z'.")),
                          (6, port_help + " " + tr("O Netuno confere se o percurso chega exatamente ali."))):
            self.table_runs.horizontalHeaderItem(col).setToolTip(text)
        header = self.table_runs.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        for col, width in ((0, 90), (1, 210), (2, 80), (3, 110), (4, 120), (6, 120)):
            self.table_runs.setColumnWidth(col, width)
        lay.addWidget(self.table_runs)
        for run in runs:
            self.add_run(run)
        return box

    def add_run(self, run: Optional[Dict[str, Any]] = None) -> None:
        run = run if isinstance(run, dict) else {}
        table = self.table_runs
        row = table.rowCount()
        table.insertRow(row)
        self._fill_run_row(row, run if run else {"run_id": f"T-{row + 1:02d}", "system": "captacao", "dn_mm": 100})

    def _fill_run_row(self, row: int, run: Dict[str, Any]) -> None:
        table = self.table_runs
        combo = QComboBox()
        for spec in PIPE_SYSTEMS:
            combo.addItem(tr(spec["label"]), spec["system_id"])
        combo.setCurrentIndex(max(combo.findData(run.get("system", "captacao")), 0))
        route = run.get("route") or ""
        if not isinstance(route, str):
            route = format_route(parse_route(route))
        dn = run.get("dn_mm")
        table.setItem(row, 0, QTableWidgetItem(str(run.get("run_id") or "")))
        table.setCellWidget(row, 1, combo)
        table.setItem(row, 2, QTableWidgetItem("" if dn is None else f"{float(dn):g}"))
        table.setItem(row, 3, QTableWidgetItem(str(run.get("material") or "PVC")))
        table.setItem(row, 4, QTableWidgetItem(format_origin(run.get("start"))))
        table.setItem(row, 5, QTableWidgetItem(route))
        table.setItem(row, 6, QTableWidgetItem(format_origin(run.get("end"))))

    def _remove_run(self) -> None:
        row = self.table_runs.currentRow()
        if row >= 0:
            self.table_runs.removeRow(row)

    def move_run(self, step: int) -> None:
        row = self.table_runs.currentRow()
        target = row + step
        if row < 0 or not 0 <= target < self.table_runs.rowCount():
            return
        runs = self._runs_from_table()
        runs[row], runs[target] = runs[target], runs[row]
        for index, run in enumerate(runs):
            self._fill_run_row(index, run)
        self.table_runs.setCurrentCell(target, 0)

    # ── Leitura ──

    @staticmethod
    def _text(table: QTableWidget, row: int, col: int) -> str:
        item = table.item(row, col)
        return item.text().strip() if item else ""

    def _components_from_table(self) -> List[Dict[str, Any]]:
        table = self.table_components
        params = self._extra_component_parameters
        items = []
        for row in range(table.rowCount()):
            items.append({
                "instance_id": self._text(table, row, 0),
                "type_id": table.cellWidget(row, 1).currentData(),
                "position_mm": {k: self._text(table, row, c).replace(",", ".") or "0" for c, k in ((2, "x"), (3, "y"), (4, "z"))},
                "rotation_deg": self._text(table, row, 5).replace(",", ".") or "0",
                "level": self._text(table, row, 6) or "Nível 0",
                "parameters": dict(params.get(row, {})),
            })
        return items

    def _runs_from_table(self) -> List[Dict[str, Any]]:
        table = self.table_runs
        runs = []
        for row in range(table.rowCount()):
            runs.append({
                "run_id": self._text(table, row, 0),
                "system": table.cellWidget(row, 1).currentData(),
                "dn_mm": self._text(table, row, 2).replace(",", ".") or None,
                "material": self._text(table, row, 3) or "PVC",
                "start": parse_origin(self._text(table, row, 4)),
                "route": self._text(table, row, 5),
                "end": parse_origin(self._text(table, row, 6)),
            })
        return runs

    def get_layout(self) -> Dict[str, Any]:
        return {
            "bim_components": self._components_from_table(),
            "pipe_runs": self._runs_from_table(),
            "building_volume": self._building_from_fields(),
        }

    # ── Prévia ──

    def _build_preview_box(self) -> QWidget:
        # O esquema já traz a sequência, o quantitativo e os avisos; ao lado dele
        # fica só o estado da validação, com os erros que impedem a exportação.
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        head = QHBoxLayout()
        self.lbl_report = QLabel()
        self.lbl_report.setWordWrap(True)
        self.lbl_report.setTextInteractionFlags(Qt.TextSelectableByMouse)
        head.addWidget(self.lbl_report, 1)
        self.btn_html = QPushButton(tr("🌐 Volumetria interativa (.html)"))
        self.btn_html.setToolTip(tr("Página autocontida, girável no navegador, para compartilhar"))
        self.btn_html.clicked.connect(lambda: self.export_volumetry("html"))
        self.btn_glb = QPushButton(tr("🧊 Modelo 3D (.glb)"))
        self.btn_glb.setToolTip(tr("glTF 2.0: Visualizador 3D do Windows, Blender, SketchUp e visualizadores web"))
        self.btn_glb.clicked.connect(lambda: self.export_volumetry("glb"))
        head.addWidget(self.btn_html)
        head.addWidget(self.btn_glb)
        lay.addLayout(head)
        self.tabs = QTabWidget()
        self.volumetry = VolumetryPanel()
        self.preview = SchematicView()
        self.tabs.addTab(self.volumetry, tr("🧊 Volumetria 3D (girável)"))
        self.tabs.addTab(self.preview, tr("🧭 Esquema 3D (medidas e sequência)"))
        lay.addWidget(self.tabs, 1)
        return box

    def export_volumetry(self, fmt: str) -> Optional[str]:
        if self._valid_data is None:
            QMessageBox.warning(self, tr("Volumetria"), tr("Resolva as pendências da organização antes de exportar."))
            return None
        name = str(self._valid_data.get("project_name") or "Projeto").replace(" ", "_")
        filters = {"html": "Página HTML (*.html)", "glb": "glTF binário (*.glb)"}
        path, _ = QFileDialog.getSaveFileName(self, tr("Exportar volumetria"), f"{name}_Volumetria_Netuno.{fmt}", filters[fmt])
        if not path:
            return None
        scene = build_volumetry(self._valid_data)
        (write_html_viewer if fmt == "html" else write_glb)(scene, path)
        self.lbl_report.setText(self.lbl_report.text() + f" · {tr('exportado')}: {escape(Path(path).name)}")
        return path

    def refresh_preview(self) -> List[str]:
        """Valida com o núcleo e atualiza o estado e o esquema 3D; devolve os erros."""
        data = dict(self._project_data)
        try:
            data.update(self.get_layout())
            manifest = build_bim_manifest(data)
            errors = validate_bim_manifest(manifest)
        except ValueError as exc:
            manifest, errors = None, [str(exc)]
        if errors:
            self.lbl_report.setText(
                f"<b style='color:#b91c1c'>{tr('Pendências — a planta 3D não será exportada:')}</b><br>"
                + "<br>".join(f"• {escape(e)}" for e in errors)
            )
        else:
            warnings = len(manifest["validation"]["warnings"])
            note = f" · {warnings} {tr('aviso(s) numerado(s) no esquema')}" if warnings else ""
            self.lbl_report.setText(
                f"<b style='color:#047857'>{tr('Organização válida')}</b> · "
                f"{len(manifest['pipe_runs'])} {tr('trecho(s)')}{note}"
            )
        has_content = bool(data.get("pipe_runs") or data.get("bim_components"))
        valid = not errors and has_content
        self._valid_data = data if valid else None
        self.preview.set_svg(generate_schematic_3d_svg(data) if valid else None)
        self.volumetry.set_scene(build_volumetry(data) if valid else None)
        self.btn_html.setEnabled(valid)
        self.btn_glb.setEnabled(valid)
        return errors


class SchematicView(QWidget):
    """Desenha o SVG vetorialmente no espaço disponível, sem distorcer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._renderer: Optional[QSvgRenderer] = None
        self.setMinimumHeight(260)

    def set_svg(self, svg: Optional[str]) -> None:
        self._renderer = QSvgRenderer(QByteArray(svg.encode("utf-8"))) if svg else None
        self.update()

    def has_drawing(self) -> bool:
        return self._renderer is not None and self._renderer.isValid()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        painter.setPen(QColor("#cbd5e1"))
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
        if not self.has_drawing():
            painter.setPen(QColor("#64748b"))
            painter.drawText(self.rect(), Qt.AlignCenter, tr("O esquema 3D aparece quando a organização estiver válida."))
            return
        size = self._renderer.defaultSize()
        scale = min(self.width() / size.width(), self.height() / size.height())
        width, height = size.width() * scale, size.height() * scale
        target = QRectF((self.width() - width) / 2, (self.height() - height) / 2, width, height)
        self._renderer.render(painter, target)
