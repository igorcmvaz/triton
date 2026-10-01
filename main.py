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


def diagnosticar(argumentos_qt) -> int:
    """``--diagnostico``: o que este pacote traz. Grava, mostra e devolve 1 se faltar o essencial."""
    import tempfile
    from netuno.core.diagnostico import faltam_obrigatorios, relatorio, verificacoes

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([sys.argv[0]] + list(argumentos_qt))
    itens = verificacoes()
    texto = relatorio(itens)
    arquivo = os.path.join(tempfile.gettempdir(), "netuno_diagnostico.txt")
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(texto)
    except OSError:
        arquivo = ""
    try:
        print(texto)
    except Exception:
        pass  # executável sem console
    if app.platformName() not in ("offscreen", "minimal"):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(None, "Netuno — diagnóstico",
                                texto + (f"\nGravado em {arquivo}" if arquivo else ""))
    return 1 if faltam_obrigatorios(itens) else 0


def main():
    # Edição (--edition brl|int); main_brl.py e main_int.py a fixam pela variável
    # de ambiente NETUNO_EDITION. Os demais argumentos seguem para o Qt.
    import argparse
    from netuno.core.edition import get_edition_title, is_int_edition, set_current_edition

    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument("--edition", "-e", choices=["brl", "int", "BRL", "INT"], default=None)
    arg_parser.add_argument("--diagnostico", action="store_true")
    parsed_args, remaining = arg_parser.parse_known_args()
    if parsed_args.edition:
        set_current_edition(parsed_args.edition)
    if parsed_args.diagnostico:
        sys.exit(diagnosticar(remaining))

    # Garante contexto OpenGL compartilhado exigido pelo Chromium/QtWebEngine no Windows
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication([sys.argv[0]] + remaining)

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
    app.setApplicationName("Netuno 5 (INT)" if is_int_edition() else "Netuno 5 (BRL)")
    app.setOrganizationName("Grupo de Pesquisa em Ambientes Sustentáveis")

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



