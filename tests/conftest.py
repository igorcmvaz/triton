"""
Configuração global do Pytest para a suíte de testes do Netuno 5.
Garante execução em modo offscreen (headless) para Qt/PySide6 e Matplotlib (Agg).
"""

import os
import sys
import matplotlib

# Desativa renderização de janelas gráficas durante os testes automatizados
os.environ["QT_QPA_PLATFORM"] = "offscreen"
matplotlib.use("Agg")

import pytest
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session", autouse=True)
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
