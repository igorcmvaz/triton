"""
Teste de integração de ponta a ponta: Base de dados CLIMBra,
sincronização de tarifas, simulação de balanço hídrico e análise econômica.
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication

from netuno.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_national_climate_and_tariff_integration_flow(qapp):
    """Valida o fluxo integrado de seleção de cidade, carregamento de chuva e tarifas."""
    win = MainWindow()
    assert win is not None

    tab_p = win.tab_project

    # 1. Selecionar Estado DF e Município Brasília
    idx_uf = tab_p.combo_climate_uf.findData("DF")
    if idx_uf >= 0:
        tab_p.combo_climate_uf.setCurrentIndex(idx_uf)
    idx_city = tab_p.combo_climate_city.findText("Brasília")
    if idx_city >= 0:
        tab_p.combo_climate_city.setCurrentIndex(idx_city)

    assert tab_p.precip_data is not None
    assert len(tab_p.precip_data) > 0
    assert "Brasília" in tab_p.lbl_t_prestador.text() or "CAESB" in tab_p.lbl_t_prestador.text()

    # 2. Verificar sincronização no NetunoConfig
    cfg = win.config
    assert cfg.tariff_city_uf == "DF"
    assert "Brasília" in cfg.tariff_city_name

    # 3. Aplicar recorte temporal para 5 anos (1995 a 1999)
    tab_p.txt_start_date.setText("01/01/1995")
    tab_p.txt_end_date.setText("31/12/1999")
    tab_p.on_apply_date_filter()

    assert len(tab_p.precip_data) == 1826  # 5 anos (com bissexto 1996)
    assert tab_p.txt_start_date.text() == "01/01/1995"
    assert tab_p.txt_end_date.text() == "31/12/1999"

    # 4. Executar simulação técnica com os dados nacionais
    win.tab_tanks_simulation.txt_sweep_max.setText("8000")
    win.tab_tanks_simulation.txt_sweep_step.setText("2000")
    win.tab_tanks_simulation.txt_delta_ideal.setText("2.5")
    win.tab_tanks_simulation.txt_pump_thresh_pct.setText("30")
    win.sync_project_state()
    win.tab_tanks_simulation.run_simulation(force=False)

    assert win.tab_tanks_simulation.last_sweep_result is not None
    assert len(win.tab_tanks_simulation.last_sweep_result.results_by_volume) > 1

    # 5. Executar análise econômica
    win.tab_tanks_simulation.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
    win.tab_economic.calculate_economics(force=True)

    assert win.tab_economic.economic_optimum_volume is not None

    # 6. Testar restauração de tarifas
    tab_p._tariff_is_customized = True
    tab_p.on_restore_official_tariffs(show_dialog=False)
    assert tab_p._tariff_is_customized is False
