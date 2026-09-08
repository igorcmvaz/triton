"""
Teste de integração automatizado da interface gráfica do Netuno 5 (10 Etapas incluindo ACV e Relatório de Pesquisa).
"""

import os
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


def test_full_ui_flow(qapp):
    window = MainWindow()
    assert window is not None
    window.txt_workspace_project.setText("Residencial Horizonte")
    assert window.config.project_name == "Residencial Horizonte"

    # 1. Testar alternância entre as 11 abas via Sidebar
    for idx in range(11):
        window.sidebar.step_changed.emit(idx)
        assert window.stack.currentIndex() == idx


    # 2. Carregar série de chuva sintética (365 dias) para execução ultra-rápida do teste UI
    import numpy as np
    window.tab_project.precip_data = np.array([10.0] * 365, dtype=float)
    window.tab_project.txt_discard.setText("2.0")
    window.tab_project.txt_start_date.setText("01/01/1980")
    window.sync_project_state()
    assert window.tab_project.precip_data is not None
    assert len(window.tab_project.precip_data) == 365


    # 3. Testar alterações na Etapa 2 (Edificação)
    window.tab_building.txt_area.setText("800")
    window.tab_building.txt_demand.setText("180")
    window.tab_building.txt_residents.setText("10")
    window.tab_building.txt_share.setText("40")
    cfg = window.tab_building.get_building_config()
    assert cfg["area"] == 800.0
    assert cfg["residents"] == 10

    # 4. Sincronizar e Rodar Simulação na Etapa 4 (Reservatórios)
    window.tab_tanks_simulation.txt_sweep_max.setText("10000")
    window.tab_tanks_simulation.txt_sweep_step.setText("2500")

    window.tab_tanks_simulation.txt_delta_ideal.setText("5.0")
    window.tab_tanks_simulation.txt_pump_thresh_pct.setText("10.0")
    window.sync_project_state()
    window.tab_tanks_simulation.run_simulation(force=False)
    assert window.tab_tanks_simulation.last_single_result is not None
    assert window.tab_tanks_simulation.last_single_result.potential_potable_savings_pct > 0.0

    # Aumentar Vmax nao pode bloquear a execucao: o passo e dobrado em
    # multiplos de 250 L e o maximo exato permanece como ultimo candidato.
    window.tab_tanks_simulation.txt_sweep_max.setText("10001")
    window.tab_tanks_simulation.txt_sweep_step.setText("250")
    window.tab_tanks_simulation.run_simulation(force=False)
    adjusted_sweep = window.tab_tanks_simulation.last_sweep_result
    assert window.tab_tanks_simulation.txt_sweep_step.text() == "500"
    assert adjusted_sweep.effective_step_l == 500.0
    assert adjusted_sweep.results_by_volume[-1].lower_tank_vol == 10001.0
    assert len(adjusted_sweep.results_by_volume) - 1 <= 40

    # 5. Preencher parâmetros econômicos na Etapa 4 (agora ficam em tab_tanks_simulation)
    window.tab_tanks_simulation.txt_inflation.setText("0.20")
    window.tab_tanks_simulation.txt_readj_period.setText("12")
    window.tab_tanks_simulation.txt_period.setText("20")
    window.tab_tanks_simulation.txt_tma.setText("2.00")
    window.tab_tanks_simulation.txt_readj_water.setText("5.0")
    window.tab_tanks_simulation.txt_readj_elec.setText("5.0")
    # Forçar todos os 4 modais como verificados para liberar o cálculo econômico
    window.tab_tanks_simulation.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
    window.tab_economic.calculate_economics(force=True)
    window.sidebar.step_changed.emit(5)
    assert window.tab_economic.economic_optimum_volume is not None
    assert window.tab_economic.combo_active_volume.currentData() == window.tab_economic.economic_optimum_volume
    economic_headers = [
        window.tab_economic.table_mat_impact.horizontalHeaderItem(i).text()
        for i in range(window.tab_economic.table_mat_impact.columnCount())
    ]
    assert all("CO2" not in header for header in economic_headers)

    # 6. Rodar Otimização Multi-Critério (TOPSIS) na Etapa 7
    window.tab_global_optimizer.recalculate_all()
    assert window.tab_global_optimizer.table.rowCount() > 0
    assert window.tab_global_optimizer.tab_charts_topsis.count() == 2
    assert hasattr(window.tab_global_optimizer, "topsis_proximity_chart")


    # 7. Testar Otimizador Ambiental (ACV) na Etapa 8
    window.tab_environmental.combo_lower_mat.setCurrentIndex(1)  # Concreto Armado
    window.tab_environmental.recalculate_and_update()
    lca_res = window.tab_environmental._last_lca_result
    assert lca_res is not None
    assert lca_res.total_embodied_co2_kg > 0
    assert window.tab_environmental.combo_env_active_volume.currentData() == pytest.approx(
        window.tab_environmental._last_sweep_lca.best_lifetime_co2_vol_liters
    )

    # O resumo lateral substitui os indicadores do cenário ativo pelos quatro
    # volumes de referência da decisão.
    assert "--" not in window.sidebar.lbl_sum_opt_tech.text()
    assert "--" not in window.sidebar.lbl_sum_opt_econ.text()
    assert "--" not in window.sidebar.lbl_sum_opt_env.text()
    assert "--" not in window.sidebar.lbl_sum_opt_topsis.text()

    window.tab_reports.combo_report_type.setCurrentIndex(
        window.tab_reports.combo_report_type.findData("economic")
    )
    report_data = window.tab_reports._collect_project_data()
    assert report_data["report_charts"] == []

    window.tab_reports.combo_report_type.setCurrentIndex(
        window.tab_reports.combo_report_type.findData("research")
    )
    report_charts = window.tab_reports._collect_project_data()["report_charts"]
    assert len(report_charts) == 11
    assert {chart["chapter"] for chart in report_charts} == {
        "hydraulic", "decision", "economic", "environmental"
    }
    assert all(chart["data"].startswith("data:image/png;base64,") for chart in report_charts)

    # 8. Testar Alternância de Perfil de Relatório na Etapa 9 (Econômico vs Ambiental vs Pesquisa)
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData("economic"))
    window.tab_reports.update_report_preview()
    html_econ = window.tab_reports.generate_html_content()
    assert "laudo técnico executivo" in html_econ.lower() or "netuno" in html_econ.lower()

    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData("environmental"))
    window.tab_reports.update_report_preview()
    html_env = window.tab_reports.generate_html_content()
    assert "desempenho ambiental" in html_env.lower()
    assert "iso 14040" in html_env.lower() or "inventário" in html_env.lower()

    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData("research"))
    window.tab_reports.update_report_preview()
    html_research = window.tab_reports.generate_html_content()
    assert "relatório técnico-científico de pesquisa" in html_research.lower()
    assert "análise do ciclo de vida" in html_research.lower()
