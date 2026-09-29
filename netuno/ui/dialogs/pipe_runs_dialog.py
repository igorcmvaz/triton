"""Organização dos trechos de tubulação para a planta 3D.

O projetista posiciona os componentes e lista os trechos na ordem de montagem.
Cada trecho parte de um componente, do fim de um trecho anterior ou, com a origem
em branco, do fim do trecho imediatamente acima. A validação e a prévia
isométrica usam o mesmo núcleo que gera o DXF, para que o que se vê aqui seja o
que será exportado. A organização é salva mesmo com erros, porque é trabalho em
andamento; quem recusa uma organização inválida é a exportação.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from netuno.core.bim_exporter import COMPONENT_TYPES, build_bim_manifest, validate_bim_manifest
from netuno.core.pipe_network import PIPE_SYSTEMS, format_route, lengths_by_dn, parse_route
from netuno.core.plant_3d import generate_plant_3d_svg
from netuno.ui.translation import tr


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
        self.resize(1250, 820)
        self._project_data = dict(project_data or {})
        # Parâmetros das famílias (capacidade, potência...) não aparecem na
        # tabela, mas são preservados por linha para não se perderem ao salvar.
        self._extra_component_parameters: Dict[int, Dict[str, Any]] = {}
        layout = layout or {}

        root = QVBoxLayout(self)
        intro = QLabel(tr(
            "Coordenadas locais em mm, z para cima. Os trechos são montados de cima para baixo: "
            "origem em branco continua do fim do trecho anterior. Percurso: '+x 3000; desce 1200; "
            "d 2000 0 -20' (d = deslocamento livre, para declividade). O destino é conferido, não completado."
        ))
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #475569; font-size: 11.5px;")
        root.addWidget(intro)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self._build_components_box(layout.get("bim_components") or []))
        splitter.addWidget(self._build_runs_box(layout.get("pipe_runs") or []))
        splitter.addWidget(self._build_preview_box())
        splitter.setSizes([200, 280, 340])
        root.addWidget(splitter, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr("Salvar organização"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr("Cancelar"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)
        self.refresh_preview()

    # ── Componentes ──

    def _build_components_box(self, components: List[Dict[str, Any]]) -> QWidget:
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
        return box

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
        return {"bim_components": self._components_from_table(), "pipe_runs": self._runs_from_table()}

    # ── Prévia ──

    def _build_preview_box(self) -> QWidget:
        box = QWidget()
        lay = QHBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        self.lbl_report = QLabel()
        self.lbl_report.setWordWrap(True)
        self.lbl_report.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_report.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_report.setMinimumWidth(360)
        self.lbl_preview = QLabel()
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("background: #ffffff; border: 1px solid #cbd5e1;")
        lay.addWidget(self.lbl_report, 1)
        lay.addWidget(self.lbl_preview, 2)
        return box

    def refresh_preview(self) -> List[str]:
        """Valida com o núcleo e atualiza o relatório e a isométrica; devolve os erros."""
        data = dict(self._project_data)
        try:
            data.update(self.get_layout())
            manifest = build_bim_manifest(data)
            errors = validate_bim_manifest(manifest)
        except ValueError as exc:
            manifest, errors = None, [str(exc)]
        lines: List[str] = []
        if errors:
            lines.append(f"<b style='color:#b91c1c'>{tr('Erros')}</b>")
            lines += [f"• {e}" for e in errors]
        if manifest:
            if manifest["validation"]["warnings"]:
                lines.append(f"<b style='color:#b45309'>{tr('Avisos')}</b>")
                lines += [f"• {w}" for w in manifest["validation"]["warnings"]]
            totals = lengths_by_dn(manifest["pipe_runs"])
            if totals:
                lines.append(f"<b>{tr('Comprimento por DN')}</b>")
                lines += [f"• DN {dn:g}: {m:.2f} m".replace(".", ",") for dn, m in totals.items()]
        if not errors:
            lines.insert(0, f"<b style='color:#047857'>{tr('Organização válida')}</b>")
        self.lbl_report.setText("<br>".join(lines))
        self._render_preview(data if not errors else None)
        return errors

    def _render_preview(self, data: Optional[Dict[str, Any]]) -> None:
        if data is None or not (data.get("pipe_runs") or data.get("bim_components")):
            self.lbl_preview.setPixmap(QPixmap())
            self.lbl_preview.setText(tr("Prévia disponível quando a organização estiver válida."))
            return
        renderer = QSvgRenderer(QByteArray(generate_plant_3d_svg(data).encode("utf-8")))
        image = QImage(1000, 700, QImage.Format_ARGB32)
        image.fill(QColor("white"))
        painter = QPainter(image)
        renderer.render(painter)
        painter.end()
        self.lbl_preview.setText("")
        self.lbl_preview.setPixmap(QPixmap.fromImage(image).scaled(760, 532, Qt.KeepAspectRatio, Qt.SmoothTransformation))
