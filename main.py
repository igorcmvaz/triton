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
    # Garante contexto OpenGL compartilhado exigido pelo Chromium/QtWebEngine no Windows
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)
    app.setStyle(NoMnemonicUnderlineStyle(app.style()))
    app.setApplicationName("Netuno 5")
    app.setOrganizationName("Grupo de Pesquisa Gestão do Espaço Sustentável")

    # Verifica se é a primeira execução do aplicativo para selecionar o idioma
    check_first_run_language()

    window = MainWindow()
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



