"""
Testes unitários para TabProject garantindo o modelo padrão INM-CM4,
recorte temporal inicial até 31/12/2013 e descarte inicial sem valor (-).
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication
from netuno.ui.tab_project import TabProject


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_project_defaults(qapp):
    tab = TabProject()
    assert tab is not None

    # Modelo GCM padrão deve ser INM-CM4
    assert tab.combo_climate_model.currentText() == "INM-CM4"

    # Período temporal inicial completo de 1980 a 2013 (inclusive)
    assert tab.txt_start_date.text() == "01/01/1980"
    assert tab.txt_end_date.text() == "31/12/2013"

    # Descarte inicial deve vir sem valor para forçar o preenchimento pelo usuário
    assert tab.txt_discard.text() in ["-", ""]
    assert tab.txt_discard.placeholderText() != ""

    # Dados de chuva carregados (1980 a 2013 = 34 anos cheios = 12419 dias)
    assert tab.precip_data is not None
    assert len(tab.precip_data) == 12419


def test_tab_project_discard_fill(qapp):
    tab = TabProject()
    # Ao preencher o descarte com valor válido, o estado do projeto é atualizado
    tab.txt_discard.setText("2.5")
    assert tab.txt_discard.text() == "2.5"
    assert tab.get_project_state()["discard"] == "2.5"
