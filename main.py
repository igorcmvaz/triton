"""
Ponto de Entrada Principal da Aplicação Netuno 5 (PySide6).
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication, QProxyStyle, QStyle, QAbstractSpinBox
from netuno.ui.translation import check_first_run_language
from netuno.ui.main_window import MainWindow


class NoMnemonicUnderlineStyle(QProxyStyle):
    """Mantém possíveis atalhos Qt, mas não desenha sublinhados nos rótulos e remove setas de incremento dos SpinBoxes."""
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_UnderlineShortcut:
            return 0
        return super().styleHint(hint, option, widget, returnData)

    def polish(self, widget):
        super().polish(widget)
        if isinstance(widget, QAbstractSpinBox):
            widget.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


def main():
    # Suporte a argumento de linha de comando --edition BRL|INT
    import argparse
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument("--edition", "-e", choices=["brl", "int", "BRL", "INT"], default=None)
    parsed_args, remaining = arg_parser.parse_known_args()
    if parsed_args.edition:
        from netuno.core.edition import set_current_edition
        set_current_edition(parsed_args.edition)

    from netuno.core.edition import get_edition_title, is_int_edition

    # Garante contexto OpenGL compartilhado exigido pelo Chromium/QtWebEngine no Windows
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    qt_args = [sys.argv[0]] + remaining
    app = QApplication(qt_args)
    app.setStyle(NoMnemonicUnderlineStyle(app.style()))
    app_name = "Netuno 5 (INT)" if is_int_edition() else "Netuno 5 (BRL)"
    app.setApplicationName(app_name)
    app.setOrganizationName("Grupo de Pesquisa Gestão do Espaço Sustentável")

    # Verifica se é a primeira execução do aplicativo para selecionar o idioma
    check_first_run_language()

    window = MainWindow()
    window.setWindowTitle(get_edition_title())
    primary_screen = app.primaryScreen()
    if primary_screen is not None:
        # Posiciona a janela nativa no monitor principal antes de maximizá-la;
        # isso evita que o Qt reutilize o monitor da sessão anterior.
        window.setGeometry(primary_screen.geometry())
        window.winId()
        if window.windowHandle() is not None:
            window.windowHandle().setScreen(primary_screen)
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()



