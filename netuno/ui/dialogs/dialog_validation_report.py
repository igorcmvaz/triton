"""Diálogo do relatório de verificação interna e rastreabilidade do Netuno."""

from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QPushButton, QGroupBox
)
from PySide6.QtGui import QFont, QColor
from netuno.ui.translation import tr, get_current_lang, get_current_theme
from netuno import __version__


def caminho_do_relatorio(sufixo: str = ""):
    """O relatório de verificação que o diálogo mostra, ou None.

    O diálogo procurava `docs/relatorio_validacao.md`, nome que não existe no
    repositório, e abria sempre com o aviso de relatório ausente. O documento
    real é `docs/verificacao_e_validacao.md`; a versão traduzida, quando
    houver, leva o sufixo do idioma.
    """
    raiz = Path(__file__).resolve().parents[3]
    nomes = [f"verificacao_e_validacao{sufixo}.md", "verificacao_e_validacao.md"]
    for pasta in (raiz / "netuno" / "docs", raiz / "docs"):
        for nome in nomes:
            caminho = pasta / nome
            if caminho.exists():
                return caminho
    return None


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
        
        report_path = caminho_do_relatorio(suffix)

        if report_path is not None:
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
