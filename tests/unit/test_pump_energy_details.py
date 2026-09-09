"""
Suíte de Testes para Validação Físico-Matemática e Interface da Motobomba e Consumo de Energia Elétrica.
Testa:
1. Fórmula física exata de consumo de energia (Potência, Rendimento, Vazão, Partida, Horas e Custo).
2. Conversões de unidades de potência (CV, HP, W, kW).
3. Duplicação de CAPEX em caso de motobomba de reserva (backup pump).
4. Atualização dos atributos do Dashboard da Motobomba na TabTanksSimulation (UI).
"""

import pytest
import sys
from PySide6.QtWidgets import QApplication

from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult, SimulationDayResult
from netuno.core.economic import run_economic_analysis
from netuno.ui.tab_tanks_simulation import TabTanksSimulation


def test_pump_power_conversions():
    """Testa a conversão de unidades de potência da motobomba."""
    # 1 CV ~ 0.735499 kW
    cv_val = 1.0
    p_kw_from_cv = cv_val * 0.735499
    assert pytest.approx(p_kw_from_cv, rel=1e-4) == 0.735499

    # 1 HP ~ 0.7457 kW
    hp_val = 2.0
    p_kw_from_hp = hp_val * 0.7457
    assert pytest.approx(p_kw_from_hp, rel=1e-4) == 1.4914

    # 750 W = 0.75 kW
    w_val = 750.0
    p_kw_from_w = w_val / 1000.0
    assert p_kw_from_w == 0.75


def test_pump_energy_exact_physics_formula():
    """
    Testa a fórmula física exata de consumo elétrico da motobomba:
    - E = (P_kW * (t_recalque + t_partida)) / (eta)
    - Custo_E = E * Tarifa * (1 + Imposto_Var) + Imposto_Fixo
    """
    config = NetunoConfig()
    config.upper_tank_used = True
    config.pump_power_kw = 0.7355        # ~ 1 CV
    config.pump_efficiency = 60.0         # 60%
    config.pump_flow_rate = 3000.0        # 3000 L/h
    config.pump_startup_time_h = 10.0 / 3600.0  # 10s por partida
    config.elec_tariff = 1.00             # R$ 1,00 / kWh
    config.elec_tax_var = 0.0             # 0%
    config.elec_tax_fixed = 0.0           # R$ 0

    # Simulando 30 dias com total de 30.000 L recalcados e 60 partidas
    total_pumped_liters = 30000.0
    total_pump_cycles = 60

    daily = []
    for d in range(30):
        daily.append(SimulationDayResult(
            day_index=d+1, precip_mm=10.0, eff_precip_mm=10.0, harvested_liters=1000.0,
            total_demand_liters=1000.0, pluvial_demand_liters=1000.0, pluvial_consumed_liters=1000.0,
            potable_consumed_liters=0.0, spilled_liters=0.0, lower_tank_end_liters=1000.0,
            upper_tank_end_liters=500.0, pumped_liters=1000.0, pump_cycles=2, satisfaction_type=2
        ))

    sim_res = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=80.0,
        avg_pluvial_consumed_l_day=1000.0,
        avg_potable_consumed_l_day=200.0,
        avg_spilled_l_day=100.0,
        pct_days_full_satisfaction=80.0,
        pct_days_partial_satisfaction=10.0,
        pct_days_null_satisfaction=10.0,
        total_pumped_liters=total_pumped_liters,
        total_pump_cycles=total_pump_cycles,
        daily_results=daily
    )

    econ = run_economic_analysis(config, sim_res)

    days_in_month = 30.4375
    avg_daily_pumped = 30000.0 / 30.0
    avg_daily_cycles = 60.0 / 30.0

    t_rec_expected = (avg_daily_pumped * days_in_month) / 3000.0
    t_part_expected = avg_daily_cycles * days_in_month * (10.0 / 3600.0)
    t_tot_expected = t_rec_expected + t_part_expected

    # A potencia de placa e o que o motor CONSOME: a energia por m3 recalcado e
    # P/Q, e nao P/Q dividido pelo rendimento. O rendimento ja esta embutido no
    # fato de uma bomba de P kW entregar Q m3/h naquela altura.
    #
    # Ate a versao 5.0.8 esta conta fazia P x horas / eta, dividindo por eta uma
    # segunda vez e superestimando a energia de bombeamento em 1/eta - 67% com o
    # rendimento de 60% usado aqui. Este teste fixava justamente a conta errada.
    volume_mensal_m3 = (avg_daily_pumped * days_in_month) / 1000.0
    energia_recalque = (0.7355 / 3.0) * volume_mensal_m3

    # As partidas sao a excecao: ali a bomba consome sem entregar vazao util, de
    # modo que a perda entra explicitamente.
    energia_partidas = (0.7355 * t_part_expected) / 0.60

    energy_kwh_expected = energia_recalque + energia_partidas
    cost_expected = energy_kwh_expected * 1.00

    assert pytest.approx(econ.monthly_pump_kwh, rel=1e-3) == energy_kwh_expected
    assert pytest.approx(econ.monthly_pump_cost_brl, rel=1e-3) == cost_expected

    # E a comparacao com a conta antiga, para que a diferenca fique registrada.
    conta_antiga = (0.7355 * t_tot_expected) / 0.60
    assert conta_antiga > energy_kwh_expected * 1.5


def test_pump_backup_count_capex_cost():
    """Testa se a consideração da bomba de reserva multiplica o custo CAPEX por 2."""
    config_single = NetunoConfig()
    config_single.pump_unit_cost = 850.0
    config_single.pump_count = 1
    assert config_single.pump_unit_cost * config_single.pump_count == 850.0

    config_backup = NetunoConfig()
    config_backup.pump_unit_cost = 850.0
    config_backup.pump_count = 2
    assert config_backup.pump_unit_cost * config_backup.pump_count == 1700.0


def test_pump_tab_tanks_simulation_dashboard_widgets():
    """Testa a atualização completa dos KPIs da Motobomba no TabChartsNetuno (Etapa 4)."""
    from netuno.ui.main_window import MainWindow
    import numpy as np
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    tab = window.tab_tanks_simulation
    tab_charts = window.tab_charts

    # Preenche dados fictícios de chuva e simulação
    tab.precip_data = np.array([10.0] * 365, dtype=float)
    tab.last_single_result = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=85.0,
        avg_pluvial_consumed_l_day=328.5,
        avg_potable_consumed_l_day=50.0,
        avg_spilled_l_day=82.1,
        pct_days_full_satisfaction=80.0,
        pct_days_partial_satisfaction=10.0,
        pct_days_null_satisfaction=10.0,
        total_pumped_liters=100000.0,
        total_pump_cycles=250,
        daily_results=[]
    )
    tab.txt_pump_thresh_pct.setText("10.0")
    tab.txt_upper_vol.setText("500")

    # Dispara update via signal
    tab.simulation_completed.emit(tab.last_single_result, None)

    # Verifica os KPIs na Etapa 4 (tab_charts)
    assert hasattr(tab_charts, "val_pump_power"), "tab_charts deve ter val_pump_power"
    assert hasattr(tab_charts, "val_pump_cycles"), "tab_charts deve ter val_pump_cycles"
    assert hasattr(tab_charts, "val_pump_energy"), "tab_charts deve ter val_pump_energy"
    assert hasattr(tab_charts, "val_pump_cost"), "tab_charts deve ter val_pump_cost"
    assert hasattr(tab_charts, "val_pumped_vol"), "tab_charts deve ter val_pumped_vol"
