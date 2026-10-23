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

from PySide6.QtCore import QByteArray, QRectF, Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog, QHBoxLayout, QHeaderView,
    QLabel, QMessageBox, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem,
    QTabWidget, QVBoxLayout, QWidget,
)

from triton.core.bim_exporter import COMPONENT_TYPES, build_bim_manifest, validate_bim_manifest
from triton.core.pipe_network import PIPE_SYSTEMS, format_route, parse_route
from triton.core.schematic_3d import generate_schematic_3d_svg
from triton.core.volumetry import build_volumetry
from triton.core.volumetry_export import write_glb, write_html_viewer
from triton.ui.translation import tr
from triton.ui.volumetry_web import criar_painel_de_volumetria, textos_da_volumetria


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
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.resize(1280, 900)
        self._editor_before_fullscreen = True
        self.imersivo = False  # tela cheia de visualização (editor recolhido)
        self.setWindowState(Qt.WindowMaximized)
        self._project_data = dict(project_data or {})
        # Parâmetros das famílias (capacidade, potência...) não aparecem na
        # tabela, mas são preservados por linha para não se perderem ao salvar.
        self._extra_component_parameters: Dict[int, Dict[str, Any]] = {}
        layout = layout or {}
        if not (layout.get("bim_components") or layout.get("pipe_runs")):
            from triton.core.study_layout import generate_study_layout
            layout = generate_study_layout(self._project_data)

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

        # As tabelas ficam num painel recolhível: com a organização válida, a
        # janela abre na volumetria, e o editor aparece quando se quer mudar algo.
        self._valid_data: Optional[Dict[str, Any]] = None
        self.editor = QWidget()
        editor_lay = QVBoxLayout(self.editor)
        editor_lay.setContentsMargins(0, 0, 0, 0)
        editor_lay.addWidget(intro)
        editor_split = QSplitter(Qt.Vertical)
        editor_split.addWidget(self._build_components_box(layout.get("bim_components") or [], layout.get("building_volume") or {}))
        editor_split.addWidget(self._build_runs_box(layout.get("pipe_runs") or []))
        editor_lay.addWidget(editor_split, 1)

        self.btn_editor = QPushButton()
        self.btn_editor.setCheckable(True)
        self.btn_editor.toggled.connect(self.set_editor_visible)
        top = QHBoxLayout()
        top.addWidget(self.btn_editor)
        top.addStretch()
        root.addLayout(top)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self._build_preview_box())
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([420, 560])
        root.addWidget(self.splitter, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr("Salvar organização"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancelar"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)
        self._buttons = buttons
        errors = self.refresh_preview()
        # Organização válida abre direto na volumetria; com pendências, no editor.
        self.btn_editor.setChecked(bool(errors) or self._valid_data is None)
        self.set_editor_visible(self.btn_editor.isChecked())

    # ── Componentes ──

    def apply_study_layout(self) -> None:
        """Substitui a organização atual pelo traçado normativo pré-preenchido do estudo."""
        from triton.core.study_layout import generate_study_layout

        layout = generate_study_layout(self._project_data)
        self.table_components.setRowCount(0)
        self._extra_component_parameters.clear()
        for item in layout.get("bim_components") or []:
            self.add_component(item)

        self.table_runs.setRowCount(0)
        for run in layout.get("pipe_runs") or []:
            self.add_run(run)

        bldg = layout.get("building_volume") or {}
        orig = bldg.get("origin_mm") or {}
        for k in ("x", "y", "z"):
            if k in self.building_fields:
                self.building_fields[k].setValue(float(orig.get(k, 0.0)))
        for k in ("width_mm", "depth_mm", "height_mm"):
            if k in self.building_fields:
                self.building_fields[k].setValue(float(bldg.get(k, 0.0)))
        if hasattr(self, "spin_floors"):
            self.spin_floors.setValue(int(bldg.get("floors", 1)))

        self.refresh_preview()

    def _build_components_box(self, components: List[Dict[str, Any]], building: Dict[str, Any]) -> QWidget:
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        head = QHBoxLayout()
        title = QLabel(tr("<b>1. Componentes posicionados</b>"))
        head.addWidget(title)
        head.addStretch()
        for label, slot in (
            (tr("+ Componente"), self.add_component),
            (tr("− Remover"), self._remove_component),
            (tr("⚡ Pré-preencher do Estudo"), self.apply_study_layout),
        ):
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
                          (6, port_help + " " + tr("O Triton confere se o percurso chega exatamente ali."))):
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
        self.btn_fullscreen = QPushButton(tr("⛶ Tela cheia"))
        self.btn_fullscreen.setToolTip(tr("Alternar modo tela cheia (F11)"))
        self.btn_fullscreen.clicked.connect(self.toggle_fullscreen)
        self.btn_html = QPushButton(tr("🌐 Volumetria interativa (.html)"))
        self.btn_html.setToolTip(tr("Página autocontida, girável no navegador, para compartilhar"))
        self.btn_html.clicked.connect(lambda: self.export_volumetry("html"))
        self.btn_glb = QPushButton(tr("🧊 Modelo 3D (.glb)"))
        self.btn_glb.setToolTip(tr("glTF 2.0: Visualizador 3D do Windows, Blender, SketchUp e visualizadores web"))
        self.btn_glb.clicked.connect(lambda: self.export_volumetry("glb"))
        head.addWidget(self.btn_fullscreen)
        head.addWidget(self.btn_html)
        head.addWidget(self.btn_glb)
        lay.addLayout(head)
        self.tabs = QTabWidget()
        self.volumetry = criar_painel_de_volumetria()
        if hasattr(self.volumetry, "tela_cheia_pedida"):
            self.volumetry.tela_cheia_pedida.connect(self._on_viewer_fullscreen)
        self.preview = SchematicView()
        self.tabs.addTab(self.volumetry, tr("🧊 Volumetria 3D (girável)"))
        self.tabs.addTab(self.preview, tr("🧭 Esquema 3D (medidas e sequência)"))
        lay.addWidget(self.tabs, 1)
        return box

    def set_editor_visible(self, visible: bool) -> None:
        """Mostra ou recolhe as tabelas de componentes e trechos."""
        self.editor.setVisible(visible)
        if self.btn_editor.isChecked() != visible:
            self.btn_editor.blockSignals(True)
            self.btn_editor.setChecked(visible)
            self.btn_editor.blockSignals(False)
        self.btn_editor.setText(tr("▾ Recolher o editor de componentes e trechos") if visible
                                else tr("✏️ Editar componentes e trechos"))

    def toggle_fullscreen(self) -> None:
        """Tela cheia de visualização: a janela ocupa a tela e o editor recolhe."""
        if self.imersivo:
            self.imersivo = False
            if hasattr(self.volumetry, "sair_da_tela_cheia"):
                self.volumetry.sair_da_tela_cheia()
            self.showMaximized()
            self.set_editor_visible(self._editor_before_fullscreen)
            self._buttons.setVisible(True)
            self.btn_fullscreen.setText(tr("⛶ Tela cheia"))
            self.btn_fullscreen.setToolTip(tr("Alternar modo tela cheia (F11)"))
        else:
            self.imersivo = True
            self._editor_before_fullscreen = not self.editor.isHidden()
            self.set_editor_visible(False)
            self._buttons.setVisible(False)
            self.showFullScreen()
            self.btn_fullscreen.setText(tr("🗗 Minimizar tela cheia"))
            self.btn_fullscreen.setToolTip(tr("Restaurar tamanho da janela (F11 ou Esc)"))

    def _on_viewer_fullscreen(self, on: bool) -> None:
        """O botão «Tela cheia» de dentro do visualizador pede o mesmo modo."""
        if on != self.imersivo:
            self.toggle_fullscreen()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
            event.accept()
            return
        if event.key() == Qt.Key_Escape and self.imersivo:
            self.toggle_fullscreen()
            event.accept()
            return
        super().keyPressEvent(event)

    def export_volumetry(self, fmt: str, open_browser: bool = False) -> Optional[str]:
        if self._valid_data is None:
            QMessageBox.warning(self, tr("Volumetria"), tr("Resolva as pendências da organização antes de exportar."))
            return None
        name = str(self._valid_data.get("project_name") or "Projeto").replace(" ", "_")
        filters = {"html": "Página HTML (*.html)", "glb": "glTF binário (*.glb)"}
        path, _ = QFileDialog.getSaveFileName(self, tr("Exportar volumetria"), f"{name}_Volumetria_Triton.{fmt}", filters[fmt])
        if not path:
            return None
        scene = build_volumetry(self._valid_data)
        if fmt == "html":
            write_html_viewer(scene, path, textos_da_volumetria())
        else:
            write_glb(scene, path)
        self.lbl_report.setText(self.lbl_report.text() + f" · {tr('exportado')}: {escape(Path(path).name)}")
        if open_browser and fmt == "html":
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
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
