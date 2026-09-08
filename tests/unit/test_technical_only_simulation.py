import pytest
import numpy as np
from PySide6.QtWidgets import QApplication, QMessageBox
from netuno.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_technical_only_simulation_clears_and_hides_economic_environmental_topsis(qapp, monkeypatch):
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
    main_win = MainWindow()
    
    # Simula dados sintéticos de chuva (364 dias)
    dummy_precip = np.array([0.0, 15.0, 30.0, 0.0, 5.0, 25.0, 0.0] * 52)
    main_win.tab_project.precip_data = dummy_precip
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.txt_sweep_max.setText("5000")
    main_win.tab_tanks_simulation.txt_sweep_step.setText("2500")
    main_win.tab_tanks_simulation.txt_delta_ideal.setText("5.0")
    main_win.tab_tanks_simulation.txt_pump_thresh_pct.setText("10.0")
    main_win.sync_project_state()
    
    # 1. Executa a varredura técnica SOMENTE FÍSICA
    main_win.tab_tanks_simulation.run_technical_simulation()
    
    assert main_win.tab_tanks_simulation._is_technical_only is True
    
    # Verifica Etapa 4 (Resultados Técnicos)
    assert main_win.tab_charts.val_pot.text() != "--"
    assert main_win.tab_charts.val_fin_annual.text() == "--"
    
    # Verifica Etapa 5 (Econômico)
    assert main_win.tab_economic.lbl_val_vpl.text() == "--"
    assert main_win.tab_economic.lbl_val_invest.text() == "--"
    assert main_win.tab_economic.last_result is None
    assert main_win.tab_economic.economic_optimum_volume is None
    
    # Verifica Etapa 6 (Ambiental)
    assert main_win.tab_environmental._last_lca_result is None
    assert main_win.tab_environmental._last_sweep_lca is None
    
    # Verifica Etapa 7 (TOPSIS)
    assert main_win.tab_global_optimizer.last_topsis_result is None
    assert main_win.tab_global_optimizer.table.rowCount() == 0
    
    # Verifica Sidebar: Apenas ótimo técnico deve estar presente
    tech, econ, env, topsis = main_win._optimal_volumes()
    assert tech is not None and tech > 0
    assert econ is None
    assert env is None
    assert topsis is None
    
    # 2. Executa a varredura COMPLETA
    main_win.tab_tanks_simulation.run_simulation(force=True, is_technical_only=False)
    
    assert main_win.tab_tanks_simulation._is_technical_only is False
    
    # Verifica Etapa 4 (Resultados Técnicos com economia financeira exibida)
    assert main_win.tab_charts.val_fin_annual.text() != "--"
    
    # Verifica Etapa 5 (Econômico calculado)
    assert main_win.tab_economic.lbl_val_vpl.text() != "--"
    assert main_win.tab_economic.last_result is not None
    assert main_win.tab_economic.economic_optimum_volume is not None
    
    # Verifica Etapa 6 (Ambiental calculado)
    assert main_win.tab_environmental._last_lca_result is not None
    
    # Verifica Etapa 7 (TOPSIS calculado)
    assert main_win.tab_global_optimizer.last_topsis_result is not None
    assert main_win.tab_global_optimizer.table.rowCount() > 0
    
    # Verifica Sidebar com todos os ótimos
    tech2, econ2, env2, topsis2 = main_win._optimal_volumes()
    assert tech2 is not None
    assert econ2 is not None
    assert env2 is not None
    assert topsis2 is not None


def test_sweep_buttons_trigger_confirmation_dialogs(qapp, monkeypatch):
    dialogs = []

    def fake_info(parent, title, text):
        dialogs.append((title, text))

    monkeypatch.setattr(QMessageBox, "information", fake_info)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)

    main_win = MainWindow()
    dummy_precip = np.array([0.0, 15.0, 30.0, 0.0, 5.0, 25.0, 0.0] * 52)
    main_win.tab_project.precip_data = dummy_precip
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.txt_sweep_max.setText("5000")
    main_win.tab_tanks_simulation.txt_sweep_step.setText("2500")
    main_win.tab_tanks_simulation.txt_delta_ideal.setText("5.0")
    main_win.tab_tanks_simulation.txt_pump_thresh_pct.setText("10.0")
    main_win.sync_project_state()

    # 1. Clique no botão de varredura técnica
    main_win.tab_tanks_simulation.btn_run_tech_sim.click()
    assert len(dialogs) == 1
    assert "Varredura Técnica Concluída" in dialogs[0][0]

    # 2. Clique no botão de varredura completa
    dialogs.clear()
    main_win.tab_tanks_simulation.btn_run_sim.click()
    assert len(dialogs) == 1
    assert "Varredura Completa Concluída" in dialogs[0][0]

