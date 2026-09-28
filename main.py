"""
Ponto de Entrada Principal da Aplicação Netuno 5 (PySide6).
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# No Windows, define o AppId para que a Barra de Tarefas exiba o ícone correto do Netuno
if sys.platform.startswith("win"):
    import ctypes
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ufsc.ges.netuno.5.0")
    except Exception:
        pass

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QProxyStyle, QStyle, QAbstractSpinBox
from netuno.ui.translation import check_first_run_language, get_resource_path
from netuno.ui.main_window import MainWindow
from netuno.ui.qt_diagnostics import instalar_captura_de_avisos


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

    # Define o ícone oficial em nível de aplicativo (barra de tarefas, janelas, caixas de diálogo)
    for icone_rel in (
        os.path.join("icons", "netuno5.ico"),
        os.path.join("icons", "icon.ico"),
        os.path.join("icons", "netuno5.png"),
        os.path.join("icons", "icon.png"),
        os.path.join("icons", "Netuno2.png"),
    ):
        icone_path = get_resource_path(icone_rel)
        if os.path.isfile(icone_path):
            app.setWindowIcon(QIcon(icone_path))
            break

    # Captura os avisos do Qt: cada aviso distinto aparece uma vez no console,
    # com a pilha Python gravada em avisos_qt.log. Era assim que o
    # "QFont::setPointSize: Point size <= 0 (-1)" enchia o console sem que se
    # soubesse de onde vinha — ele nao vem do codigo do Netuno, e nao se
    # reproduz na construcao das telas.
    instalar_captura_de_avisos()

    app.setStyle(NoMnemonicUnderlineStyle(app.style()))
    app.setApplicationName("Netuno 5")
    app.setOrganizationName("Grupo de Pesquisa em Ambientes Sustentáveis")

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

    # Aberto por um arquivo de projeto (duplo clique num .netuno, associação
    # criada pelo instalador): carrega-o assim que a janela estiver pronta.
    projeto = next((a for a in sys.argv[1:]
                    if a.lower().endswith((".netuno", ".json")) and os.path.isfile(a)), None)
    if projeto:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, lambda: window.on_load_simulation(projeto))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()



