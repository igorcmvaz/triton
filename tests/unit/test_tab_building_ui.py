"""
Testes unitários rigorosos para a interface gráfica e callbacks da Etapa 2 (TabBuilding).
Garante que não existam erros de atributos, chamadas prematuras a widgets ou falhas de ciclo de vida.
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication
from netuno.ui.tab_building import TabBuilding


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_building_instantiation(qapp):
    tab = TabBuilding()
    assert tab is not None
    assert tab.txt_area.text() in ["100", ""]
    assert tab.txt_demand.text() in ["150", ""]
    assert tab.txt_residents.text() in ["4", ""]
    assert tab.lbl_tot_pluvial is not None


def test_tab_building_mode_switching(qapp):
    tab = TabBuilding()
    # Modo 0: Simplificado
    tab.tab_demand_mode.setCurrentIndex(0)
    cfg0 = tab.get_building_config()
    assert cfg0["demand_mode"] == "constant"

    # Modo 1: Detalhamento Avançado
    tab.tab_demand_mode.setCurrentIndex(1)
    cfg1 = tab.get_building_config()
    assert cfg1["demand_mode"] == "constant"

    # Modo 2: Semanal
    tab.tab_demand_mode.setCurrentIndex(2)
    tab._fill_weekly_from_constant()
    cfg2 = tab.get_building_config()
    assert cfg2["demand_mode"] == "weekly"
    assert len(cfg2["weekly_demands"]) == 7

    # Modo 3: Mensal
    tab.tab_demand_mode.setCurrentIndex(3)
    tab._fill_monthly_from_constant()
    cfg3 = tab.get_building_config()
    assert cfg3["demand_mode"] == "monthly"
    assert len(cfg3["monthly_demands"]) == 12

    # Modo 4: Diário
    tab.tab_demand_mode.setCurrentIndex(4)
    cfg4 = tab.get_building_config()
    assert cfg4["demand_mode"] == "daily"


def test_tab_building_cell_changes_no_exceptions(qapp):
    tab = TabBuilding()
    # Edição em tabela semanal
    tab.table_weekly.item(0, 1).setText("180")
    tab.table_weekly.item(0, 2).setText("5")
    tab.table_weekly.item(0, 3).setText("40")
    tab._on_weekly_cell_changed(0, 1)

    # Edição em tabela mensal
    tab.table_monthly.item(0, 1).setText("210")
    tab.table_monthly.item(0, 2).setText("3")
    tab.table_monthly.item(0, 3).setText("50")
    tab._on_monthly_cell_changed(0, 1)

    assert tab.lbl_tot_pluvial.text() != ""


def test_tab_building_precalc_and_presets(qapp):
    tab = TabBuilding()
    # Testar template popular
    pop_idx = tab.combo_building_template.findData("res_popular")
    assert pop_idx >= 0
    tab.combo_building_template.setCurrentIndex(pop_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0
    assert pot_sh + non_pot_sh == pytest.approx(100.0)

    # Testar template médio
    med_idx = tab.combo_building_template.findData("res_medio")
    assert med_idx >= 0
    tab.combo_building_template.setCurrentIndex(med_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0

    # Testar template comercial
    com_idx = tab.combo_building_template.findData("comercial")
    assert com_idx >= 0
    tab.combo_building_template.setCurrentIndex(com_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0
    assert 40.0 <= d_in <= 60.0
