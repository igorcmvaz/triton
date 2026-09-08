"""
Testes unitários para a aba TabBuilding com modelo unificado de tipologias.
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication

from netuno.ui.tab_building import TabBuilding, BUILDING_TEMPLATES


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_building_templates_population(qapp):
    tab = TabBuilding()
    assert tab.combo_building_template.count() == len(BUILDING_TEMPLATES) + 1

    # 1. Selecionar o template Comercial (índice 4 no catálogo: comercial)
    comercial_idx = tab.combo_building_template.findData("comercial")
    assert comercial_idx >= 0
    tab.combo_building_template.setCurrentIndex(comercial_idx)

    # Chuveiro zerado para escritório
    assert tab.sp_shower_count.value() == 0.0
    assert tab.sp_shower_time.value() == 0.0
    # Consumo interno recalculado para ~50 L/pessoa/dia
    cfg = tab.get_building_config()
    assert cfg["template_id"] == "comercial"
    assert 40.0 <= cfg["demand"] <= 60.0
    assert 40.0 <= cfg["potable_indoor_share"] * 100.0 <= 60.0


def test_tab_building_fixture_tweak_marks_custom(qapp):
    tab = TabBuilding()
    # Começa no padrão médio
    medio_idx = tab.combo_building_template.findData("res_medio")
    tab.combo_building_template.setCurrentIndex(medio_idx)
    assert tab.combo_building_template.currentData() == "res_medio"

    # Usuário altera a vazão da ducha de 9.0 para 15.0 L/min
    tab.sp_shower_flow.setValue(15.0)

    # Verifica que o template foi alterado para 'custom'
    assert tab.combo_building_template.currentData() == "custom"
    cfg = tab.get_building_config()
    assert cfg["template_id"] == "custom"
    assert cfg["shower_flow"] == 15.0


def test_tab_building_contextual_typology_adaptations(qapp):
    tab = TabBuilding()

    # 1. Testar adaptação para Hospital / Clínica
    hosp_idx = tab.combo_building_template.findData("hospital")
    assert hosp_idx >= 0
    tab.combo_building_template.setCurrentIndex(hosp_idx)

    assert "Leitos" in tab.lbl_residents_title.text()
    assert "Esterilização" in tab.lbl_sp_sink_title.text() or "Higiene" in tab.lbl_cin_pot_title.text()
    assert "Lavanderia" in tab.lbl_sp_wash_cycles_title.text()
    cfg_hosp = tab.get_building_config()
    assert cfg_hosp["template_id"] == "hospital"
    assert 220.0 <= cfg_hosp["demand"] <= 280.0

    # 2. Testar adaptação para Escola / Educação
    escola_idx = tab.combo_building_template.findData("escola")
    assert escola_idx >= 0
    tab.combo_building_template.setCurrentIndex(escola_idx)

    assert "Alunos" in tab.lbl_residents_title.text()
    assert "Bebedouros" in tab.lbl_sp_sink_title.text()
    cfg_esc = tab.get_building_config()
    assert cfg_esc["template_id"] == "escola"
    assert 35.0 <= cfg_esc["demand"] <= 50.0

    # 3. Testar adaptação para Hotel / Hospedagem
    hotel_idx = tab.combo_building_template.findData("hotel")
    assert hotel_idx >= 0
    tab.combo_building_template.setCurrentIndex(hotel_idx)

    assert "Hóspedes" in tab.lbl_residents_title.text()
    assert "Enxoval" in tab.lbl_sp_wash_cycles_title.text() or "Rouparia" in tab.lbl_sp_wash_cycles_title.text()
    cfg_hotel = tab.get_building_config()
    assert cfg_hotel["template_id"] == "hotel"
    assert 220.0 <= cfg_hotel["demand"] <= 280.0

