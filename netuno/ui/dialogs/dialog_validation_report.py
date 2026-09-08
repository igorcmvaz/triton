"""Diálogo do relatório de verificação interna e rastreabilidade do Netuno."""

from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QPushButton, QGroupBox
)
from PySide6.QtGui import QFont, QColor
from netuno.ui.translation import tr, get_current_lang, get_current_theme
from netuno import __version__


class DialogValidationReport(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr(f"Relatório de Verificação Técnica e Computacional — Netuno {__version__}"))
        self.resize(820, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Header Info Box
        gb_header = QGroupBox(tr("Evidências de Verificação e Rastreabilidade"))
        h_lay = QHBoxLayout()
        
        is_dark = get_current_theme() == "dark"
        green_color = "#4ade80" if is_dark else "#16a34a"
        
        lbl_status = QLabel(
            f"{tr('Status:')} <b style='color: {green_color};'>{tr('VERIFICAÇÃO AUTOMATIZADA')}</b><br>"
            f"{tr('A suíte cobre balanço hídrico, tarifas, bombeamento, economia, ACV, TOPSIS, persistência e interface.')}"
        )
        lbl_status.setWordWrap(True)
        font_st = QFont("Segoe UI", 10)
        lbl_status.setFont(font_st)
        h_lay.addWidget(lbl_status)
        gb_header.setLayout(h_lay)
        layout.addWidget(gb_header)

        # Text Browser com o conteúdo formatado do relatório
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        lang = get_current_lang()
        suffix = "_en" if lang != "pt" else ""
        
        base_dir = Path(__file__).resolve().parent.parent
        report_path = base_dir / "docs" / f"relatorio_validacao{suffix}.md"
        if not report_path.exists():
            report_path = base_dir.parent / "docs" / f"relatorio_validacao{suffix}.md"

        if report_path.exists():
            with open(report_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            self.browser.setMarkdown(md_text)
        else:
            self.browser.setText(tr("Relatório de validação não encontrado. Execute `python -m pytest tests -v` para gerar evidências atuais."))

        layout.addWidget(self.browser)

        # Action Buttons
        row_btns = QHBoxLayout()
        btn_close = QPushButton(tr("Fechar"))
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.accept)
        row_btns.addStretch()
        row_btns.addWidget(btn_close)

        layout.addLayout(row_btns)
        self.setLayout(layout)
