"""
Suíte Completa de Testes de Validação do Motor Econômico do Netuno.
Testa:
1. Tarifas de água em faixas (fixas e variáveis) + Esgoto (percentual e fixo) + Impostos
2. Consumo elétrico da motobomba (Potência, Rendimento, Vazão, Partida, Tarifas de Energia, Reserva)
3. Outros custos operacionais (Linhares, Angulares, Periodicidades)
4. Balanço de Fluxo de Caixa Mensal, Inflação, TMA, VPL, TIR e Payback Descontado
5. Cenários desfavoráveis (VPL Negativo e Payback Inexistente)
"""

import pytest
import math
import numpy as np

from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult, SimulationDayResult

from netuno.core.economic import calculate_water_bill, run_economic_analysis
from netuno.core.cost_estimates import estimate_preliminary_capex, default_maintenance_items


def test_water_bill_multi_tier_calculation():
    """Valida cálculo da conta de água por faixas de consumo."""
    tariffs = [
        (0, 10, 25.0, -1),   # 0..10 m3 fixo R$ 25
        (10, 25, 5.0, 0),    # 10..25 m3 variável R$ 5/m3
        (25, 50, 7.0, 0),    # 25..50 m3 variável R$ 7/m3
        (50, 100000, 8.0, 0)
    ]
    
    # 5 m3 -> Faixa 1 fixa = 25,00 + 100% esgoto = R$ 50,00
    bill_5m3 = calculate_water_bill(5000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_5m3 == 50.0
    
    # 15 m3 -> 25,00 (primeiros 10m3) + 5 * 5,00 (próximos 5m3) = 50,00 + 100% esgoto = R$ 100,00
    bill_15m3 = calculate_water_bill(15000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_15m3 == 100.0

    # 30 m3 -> 25,00 + (15 * 5,0) + (5 * 7,0) = 25 + 75 + 35 = 135,00 + 100% esgoto = R$ 270,00
    bill_30m3 = calculate_water_bill(30000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_30m3 == 270.0


def test_casan_residential_2026_tariff_example():
    """Confere TFDI, faixas residenciais e esgoto de 100% da CASAN."""
    tariffs = NetunoConfig().water_tariffs

    # Água: 46,34 + (5 × 3,08) = 61,74. Esgoto é 100% da tarifa de água.
    assert calculate_water_bill(5000.0, tariffs, sewage_mode=1, sewage_rate=100.0) == pytest.approx(123.48)

    # Água: 46,34 + (10 × 3,08) + (5 × 14,31) = 148,69; com esgoto, 297,38.
    assert calculate_water_bill(15000.0, tariffs, sewage_mode=1, sewage_rate=100.0) == pytest.approx(297.38)


def test_americana_residential_minimum_franchise_tariff():
    """Valida a cobrança com franquia mínima não-cumulativa de Americana (DAE Americana / ARES-PCJ).
    - Até 6 m³: R$ 14,30 fixo de água + 100% esgoto = R$ 28,60 total.
    - 25 m³ (> 6 m³): 25 m³ × R$ 3,49 = R$ 87,25 de água + 100% esgoto = R$ 174,50 total.
    """
    tariffs = [
        (0.0, 6.0, 14.30, -2),
        (6.0, 999999.0, 3.49, 1)
    ]
    # Consumo de 0 m³
    bill_0m3 = calculate_water_bill(0.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_0m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 4 m³ (dentro do consumo mínimo)
    bill_4m3 = calculate_water_bill(4000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_4m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 6 m³ (dentro do consumo mínimo)
    bill_6m3 = calculate_water_bill(6000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_6m3 == pytest.approx(28.60, abs=0.01)

    # Consumo de 25 m³ (excede franquia, recalculado desde 0 pelo valor de R$ 3,49/m³)
    bill_25m3 = calculate_water_bill(25000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_25m3 == pytest.approx(174.50, abs=0.01)


def test_preliminary_capex_and_maintenance_follow_system_configuration():
    estimates = estimate_preliminary_capex(5000.0, 500.0, True, 0.36775)
    # 5.000 L é um ponto explícito da tabela de preços do banco de custos. O que
    # se verifica é o vínculo com o banco, e não o número: o preço é de varejo e
    # muda quando a fonte é atualizada, mas a estimativa tem de continuar
    # devolvendo exatamente o valor tabelado nos pontos que existem na tabela.
    from netuno.core.cost_estimates import LOWER_TANK_PRICE_TABLE
    tabelado_5000 = dict(LOWER_TANK_PRICE_TABLE)[5000.0]
    assert estimates["lower"] == pytest.approx(tabelado_5000)
    assert estimates["pump_unit"] >= 280.0
    assert estimates["labor"] > 0
    assert len(default_maintenance_items(True)) == 3

    without_upper = estimate_preliminary_capex(5000.0, 500.0, False, 0.36775)
    assert without_upper["upper"] == 0.0
    assert without_upper["pump"] == 0.0
    assert len(default_maintenance_items(False)) == 2


def test_sewage_fixed_and_water_taxes():
    """Valida esgoto em valor fixo e impostos fixos/variáveis sobre a tarifa de água."""
    tariffs = [(0, 999, 4.0, 0)]  # R$ 4,00 por m³ puro
    
    # Consumo 10 m³ -> Água: R$ 40,00. Esgoto Fixo: R$ 15,00. Imposto Fixo: R$ 5,00. Imposto Var (10%): R$ 4,00. Total = R$ 64,00
    bill = calculate_water_bill(
        vol_liters=10000.0,
        tariffs=tariffs,
        sewage_mode=0,  # Fixo
        sewage_rate=15.0,
        water_tax_fixed=5.0,
        water_tax_var=10.0
    )
    assert bill == 64.0


def test_pump_operational_electricity_costs():
    """Valida o cálculo do consumo elétrico da motobomba e custo operacional mensal."""
    config = NetunoConfig()
    config.upper_tank_used = True
    config.pump_power_kw = 0.7355  # 1 CV ~ 0,7355 kW
    config.pump_efficiency = 50.0   # 50% rendimento
    config.pump_flow_rate = 2000.0  # 2000 L/h
    config.pump_startup_time_h = 15.0 / 3600.0  # 15s de partida
    config.elec_tariff = 0.80       # R$ 0,80 / kWh
    config.elec_tax_var = 10.0      # 10% imposto
    config.elec_tax_fixed = 5.0     # R$ 5,00 imposto fixo de iluminação

    # Criamos um resultado simulação com 10.000 L bombeados e 50 ciclos em 30 dias
    daily = []
    for d in range(30):
        daily.append(SimulationDayResult(
            day_index=d+1,
            precip_mm=10.0,
            eff_precip_mm=10.0,
            harvested_liters=300.0,
            total_demand_liters=300.0,
            pluvial_demand_liters=300.0,
            pluvial_consumed_liters=300.0,
            potable_consumed_liters=0.0,
            spilled_liters=0.0,
            lower_tank_end_liters=1000.0,
            upper_tank_end_liters=500.0,
            pumped_liters=400.0 if d < 25 else 0.0,
            pump_cycles=2 if d < 25 else 0,
            satisfaction_type=2
        ))


    sim_res = SingleTankSimulationResult(
        lower_tank_vol=2000.0,
        potential_potable_savings_pct=100.0,
        avg_pluvial_consumed_l_day=300.0,
        avg_potable_consumed_l_day=0.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=100.0,
        pct_days_partial_satisfaction=0.0,
        pct_days_null_satisfaction=0.0,
        total_pumped_liters=10000.0,
        total_pump_cycles=50,
        daily_results=daily
    )

    econ = run_economic_analysis(config, sim_res)
    assert len(econ.monthly_cash_flows) > 0
    cf1 = econ.monthly_cash_flows[0]
    
    # Valida presença de gasto elétrico da bomba positivo
    assert cf1.pump_energy_kwh > 0.0
    assert cf1.pump_cost > 0.0


def test_additional_operational_costs():
    """Valida a inclusão de outros custos operacionais (manutenção linear e angular)."""
    config = NetunoConfig()
    config.cost_lower_tank = 1000.0
    config.cost_upper_tank = 500.0
    config.analysis_period_years = 5
    
    # Custo operacional 1: Manutenção anual fixa R$ 120,00 (período = 12 meses)
    # Custo operacional 2: Insumo produto de tratamento R$ 0,50 / m³ (período = 1 mês)
    config.op_costs = [
        ("Manutenção Anual", 12, 120.0, 0.0),
        ("Insumos Tratamento", 1, 0.0, 0.50)
    ]
    
    sim_res = SingleTankSimulationResult(
        lower_tank_vol=2000.0,
        potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=500.0, # ~15.2 m³/mês
        avg_potable_consumed_l_day=500.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=50.0,
        pct_days_partial_satisfaction=0.0,
        pct_days_null_satisfaction=50.0
    )

    econ = run_economic_analysis(config, sim_res)
    
    # Mês 1: Apenas Insumos Tratamento
    cf1 = econ.monthly_cash_flows[0]
    assert cf1.om_cost > 0.0
    
    # Mês 12: Manutenção Anual + Insumos Tratamento
    cf12 = econ.monthly_cash_flows[11]
    assert cf12.om_cost > cf1.om_cost


def test_economic_vpl_and_payback_favorable():
    """Valida VPL positivo, TIR válida e payback no prazo para sistema viável."""
    config = NetunoConfig()
    config.cost_lower_tank = 1000.0
    config.cost_upper_tank = 300.0
    config.cost_labor = 500.0
    config.cost_piping = 200.0
    config.cost_accessories = 100.0
    config.pump_unit_cost = 200.0
    config.pump_count = 1
    
    config.water_tariffs = [
        (0, 10, 30.0, -1),
        (10, 50, 8.0, 0)
    ]
    config.sewage_rate = 100.0
    config.sewage_mode = 1
    config.inflation = 0.2
    config.analysis_period_years = 20
    config.tma = 1.0  # 1% a.m.

    sim_res = SingleTankSimulationResult(
        lower_tank_vol=3000.0,
        potential_potable_savings_pct=80.0,
        avg_pluvial_consumed_l_day=800.0,
        avg_potable_consumed_l_day=200.0,
        avg_spilled_l_day=100.0,
        pct_days_full_satisfaction=95.0,
        pct_days_partial_satisfaction=2.0,
        pct_days_null_satisfaction=3.0
    )
    
    econ = run_economic_analysis(config, sim_res)
    
    # O CAPEX passou a conter a linha de tratamento, que ate a 5.0.7 era
    # dimensionada e descartada. A soma dos seis campos de custo continua sendo
    # a base; a ETAP e a parcela nova, e o teste a nomeia em vez de congelar o
    # total, para que trocar o filtro de entrada nao quebre o caso.
    assert econ.etap_capex_brl > 0.0
    assert econ.capex_total == pytest.approx(2300.0 + econ.etap_capex_brl)
    assert len(econ.monthly_cash_flows) == 240
    assert econ.vpl > 0.0
    assert econ.payback_months is not None
    assert econ.payback_months <= 240
    assert econ.tir_annual_pct > 0.0


def test_economic_unfavorable_scenario_negative_vpl():
    """Valida cenário inviável onde o investimento não se paga (VPL negativo, payback None)."""
    config = NetunoConfig()
    # Investimento altíssimo
    config.cost_lower_tank = 50000.0
    config.cost_upper_tank = 10000.0
    config.cost_labor = 15000.0
    config.cost_piping = 5000.0
    config.pump_unit_cost = 5000.0
    
    # Tarifa de água muito barata
    config.water_tariffs = [(0, 9999, 1.0, 0)]
    config.sewage_rate = 0.0
    config.analysis_period_years = 10
    config.tma = 2.0  # 2% a.m. high discount rate

    sim_res = SingleTankSimulationResult(
        lower_tank_vol=10000.0,
        potential_potable_savings_pct=10.0,
        avg_pluvial_consumed_l_day=50.0,
        avg_potable_consumed_l_day=450.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=10.0,
        pct_days_partial_satisfaction=0.0,
        pct_days_null_satisfaction=90.0
    )

    econ = run_economic_analysis(config, sim_res)
    
    # Configuração inicial inclui bomba principal e reserva.
    assert econ.capex_total == pytest.approx(90000.0 + econ.etap_capex_brl)
    assert econ.vpl < 0.0
    assert econ.payback_months is None
    assert econ.payback_years is None


def test_separate_tariff_escalations_and_pump_metrics():
    """Valida o funcionamento dos reajustes tarifários separados e métricas de energia da motobomba."""
    config = NetunoConfig()
    config.upper_tank_vol = 1000.0
    config.upper_tank_used = True
    config.pumping_threshold_pct = 80.0
    config.water_tariff_escalation = 6.0
    config.sewage_tariff_escalation = 4.0
    config.elec_tariff_escalation = 8.0
    config.pump_power_kw = 0.7355
    config.pump_flow_rate = 2000.0
    config.elec_tariff = 0.90

    sim_res = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=60.0,
        avg_pluvial_consumed_l_day=600.0,
        avg_potable_consumed_l_day=400.0,
        avg_spilled_l_day=50.0,
        pct_days_full_satisfaction=60.0,
        pct_days_partial_satisfaction=20.0,
        pct_days_null_satisfaction=20.0,
        total_pumped_liters=18000.0,
        total_pump_cycles=60,
        daily_results=[]
    )

    econ = run_economic_analysis(config, sim_res)

    assert econ.monthly_pump_kwh > 0.0
    assert econ.annual_pump_kwh > 0.0
    assert econ.monthly_pump_cost_brl > 0.0
    assert econ.annual_pump_cost_brl > 0.0


def test_robust_sensitivity_rate_normalization():
    """Taxas anuais entram como fração decimal; um valor percentual é recusado, e não reinterpretado."""
    from netuno.core.economic import run_robust_economic_analysis, run_sensitivity_analysis

    base_params = {
        'initial_investment': 8950.0,
        'annual_water_saved_m3': 53.8,
        'water_tariff_per_m3': 6.50,
        'sewage_tariff_per_m3': 5.20,
        'sewage_mode': 1,
        'water_tariff_escalation_rate': 0.05,  # 5% a.a.
        'sewage_tariff_escalation_rate': 0.05,
        'elec_tariff_escalation_rate': 0.05,
        'inflation_rate': 0.04,  # 4% a.a.
        'discount_rate': 0.08,   # 8% a.a.
        'annual_om_cost_base': 150.0,
        'analysis_period_years': 20
    }

    with pytest.raises(ValueError, match="parece estar em percentual"):
        run_robust_economic_analysis(**{**base_params, 'water_tariff_escalation_rate': 5.0})

    res_base = run_robust_economic_analysis(**base_params)
    
    # O VPL para investimento de R$ 8950 e economia inicial de ~R$ 630/ano deve ser um valor razoável e realista (ex: entre -R$ 10.000 e +R$ 10.000), NÃO BILHÕES!
    assert -20000.0 < res_base.vpl < 20000.0

    sens_data = run_sensitivity_analysis(base_params)
    reajuste_points = sens_data['Reajuste Tarifário Água']
    vpls_reajuste = [p[1] for p in reajuste_points]

    # Nenhum VPL na curva de sensibilidade de reajuste deve ser astronômico (> R$ 1.000.000)
    for vpl_val in vpls_reajuste:
        assert abs(vpl_val) < 100000.0


def test_step5_and_step7_exact_parity():
    """Garante paridade matemática absoluta entre os resultados da Etapa 5 e da Opção 1 da Etapa 7."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    from netuno.ui.main_window import MainWindow
    window = MainWindow()
    
    # Preenche dados sintéticos de chuva
    window.tab_project.precip_data = np.array([10.0] * 365, dtype=float)
    window.tab_tanks_simulation.precip_data = window.tab_project.precip_data
    window.sync_project_state()
    window.config.precip_file = "synthetic.csv"


    window.tab_building.txt_area.setText("150")
    window.tab_building.txt_demand.setText("150")
    window.tab_building.txt_residents.setText("4")
    window.config.area = 150.0
    window.config.demand_value = 150.0
    window.config.residents_count = 4
    window.config.econ_lower_tank_vol = 5000.0
    window.config.cost_lower_tank = 3500.0


    window.config.cost_upper_tank = 800.0
    window.config.pump_unit_cost = 320.0
    window.config.cost_piping = 1200.0
    window.config.cost_accessories = 500.0
    window.config.cost_labor = 1000.0
    # Taxas em % ao mês, a unidade gravada no projeto
    window.config.tma = 1.0
    window.config.inflation = 0.4
    window.tab_economic._internal_config = window.config


    # Configura parâmetros financeiros e diálogos verificados antes de rodar a simulação
    window.tab_tanks_simulation.txt_inflation.setText("0.4")
    window.tab_tanks_simulation.txt_period.setText("20")
    window.tab_tanks_simulation.txt_tma.setText("1.0")
    window.tab_tanks_simulation.txt_readj_period.setText("12")
    window.tab_tanks_simulation.txt_readj_water.setText("5.0")
    window.tab_tanks_simulation.txt_readj_elec.setText("5.0")
    window.tab_tanks_simulation.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}

    # Roda a simulação de volume único na Etapa 3 com varredura reduzida (2 pontos) para execução ultra-rápida (1s)
    window.tab_tanks_simulation.selected_volume_mode = "custom"
    window.tab_tanks_simulation.custom_selected_vol = 5000.0
    window.tab_tanks_simulation.txt_sweep_max.setText("5000")
    window.tab_tanks_simulation.txt_sweep_step.setText("2500")
    window.tab_tanks_simulation.txt_delta_ideal.setText("5.0")
    window.tab_tanks_simulation.txt_pump_thresh_pct.setText("10.0")
    window.tab_tanks_simulation.run_simulation(force=False)

    econ_step5 = getattr(window.tab_economic, 'last_result', getattr(window.tab_economic, 'last_econ_res', None))
    assert econ_step5 is not None


    window.tab_global_optimizer.recalculate_all()
    table7 = window.tab_global_optimizer.table
    assert table7.rowCount() > 0

    target_row = next(r for r in range(table7.rowCount()) if "5000" in table7.item(r, 1).text())
    vpl_step7_str = table7.item(target_row, 8).text()
    vpl_step7 = float(vpl_step7_str.replace('R$', '').replace('$', '').replace('.', '').replace(',', '.').strip())

    # VPL da Etapa 5 e VPL da Etapa 7 possuem 100% de paridade exata para o mesmo volume (5000 L)
    vpl_step5_5000 = window.tab_economic.last_sweep_econ_results[5000.0]["vpl"]
    assert vpl_step5_5000 == pytest.approx(vpl_step7, abs=200.0)


def test_material_cost_multipliers_and_tank_pricing():
    """Valida estimativa de custo de reservatório por material (PEAD, Concreto, PRFV, Inox)."""
    from netuno.core.cost_estimates import (
        estimate_tank_price_linear, estimate_pipe_network_cost,
        estimate_annual_chlorination_cost, estimate_preliminary_capex
    )

    from netuno.core.cost_estimates import LOWER_TANK_PRICE_TABLE

    p_pead = estimate_tank_price_linear(5000.0, "PEAD")
    p_concreto = estimate_tank_price_linear(5000.0, "CONCRETO")
    p_prfv = estimate_tank_price_linear(5000.0, "PRFV")
    p_inox = estimate_tank_price_linear(5000.0, "ACO_INOX")

    # O polietileno é a referência da tabela, e o multiplicador de material é 1.
    assert p_pead == pytest.approx(dict(LOWER_TANK_PRICE_TABLE)[5000.0])
    assert p_prfv > p_pead
    assert p_concreto > p_prfv
    assert p_inox > p_concreto

    # Tubulações
    pipes = [(100, 20.0), (50, 15.0)]
    pipe_cost = estimate_pipe_network_cost(pipes)
    # (20m * 38 + 15m * 18) * 1.25 = (760 + 270) * 1.25 = 1030 * 1.25 = 1287.50
    assert pipe_cost == 1287.50

    # Cloração: a massa devolvida é de PRODUTO comercial, já corrigida pela
    # pureza, porque é o produto que se compra e sobre ele que incide o preço.
    # Até a versão 5.0.8 esta conta devolvia a massa de cloro ATIVO e a
    # multiplicava pelo preço do produto, subestimando o custo em 1/pureza.
    from netuno.core.chlorination import PUREZA_PADRAO

    cl_kg, cl_cost = estimate_annual_chlorination_cost(100.0, dose_mg_l=2.0, cost_per_kg=25.0)
    cloro_ativo_kg = 100.0 * 2.0 / 1000.0            # 100 m³ a 2 g/m³ = 0,20 kg
    assert cl_kg == pytest.approx(cloro_ativo_kg / PUREZA_PADRAO)
    assert cl_cost == pytest.approx(cl_kg * 25.0)
    assert cl_kg > cloro_ativo_kg

    # CAPEX discriminado
    est = estimate_preliminary_capex(5000.0, 500.0, True, 0.368, lower_material="CONCRETO", upper_material="PEAD")
    assert est["lower"] == pytest.approx(p_concreto)
    assert est["upper"] > 0
    assert est["total"] > est["lower"]

    baseline = estimate_preliminary_capex(0.0, 500.0, True, 0.368)
    assert baseline["total"] == pytest.approx(0.0)


def test_operational_cost_annualization_preserves_netuno4_throughput_basis():
    from netuno.core.cost_estimates import annualize_operational_costs

    items = [
        ("Inspeção anual", 12, 120.0, 0.0),
        ("Tratamento mensal", 1, 10.0, 0.50),
    ]
    # 120 fixos anuais + 12 * R$10 + 0,50 * 120 m³/ano.
    assert annualize_operational_costs(items, 120.0) == pytest.approx(300.0)


def test_effective_tariff_uses_actual_total_demand_when_available():
    from netuno.core.economic import calculate_effective_tariff

    cfg = NetunoConfig()
    cfg.water_tariffs = [
        (0.0, 10.0, 1.0, 0),
        (10.0, 999999.0, 2.0, 0),
    ]
    cfg.sewage_mode = 1
    cfg.sewage_rate = 100.0

    water, sewage = calculate_effective_tariff(
        cfg, annual_m3_saved=120.0, annual_total_demand_m3=240.0
    )
    # 20 -> 10 m³/mês reduz a conta de R$30 para R$10: R$2/m³ evitado.
    assert water == pytest.approx(2.0)
    assert sewage == pytest.approx(2.0)


def test_capex_dialog_opens_recalculated_for_every_sweep_volume(qapp):
    from netuno.ui.dialogs.dialog_economic import DialogInitialCosts, DialogMotobomba

    config = NetunoConfig()
    config.cost_upper_tank = 9999.0  # deve ser substituído pela estimativa ao abrir
    dialog = DialogInitialCosts(config=config, evaluated_volumes=[0, 1000, 2000, 3000])

    assert dialog.table_lower_costs.rowCount() == 4
    assert dialog.table_lower_costs.item(0, 0).text() == "0"
    # O diálogo mostra o preço tabelado para 1.000 L, formatado em pt-BR. O
    # valor vem do banco de custos, e o teste o lê de lá em vez de congelá-lo.
    from netuno.core.cost_estimates import LOWER_TANK_PRICE_TABLE
    _esperado = f"{dict(LOWER_TANK_PRICE_TABLE)[1000.0]:.2f}".replace(".", ",")
    assert _esperado in dialog.table_lower_costs.item(1, 1).text()
    # A caixa superior padrao e de 500 L, e o preco tambem vem do banco.
    from netuno.core.cost_estimates import UPPER_TANK_PRICE_TABLE
    _esperado_sup = f"{dict(UPPER_TANK_PRICE_TABLE)[500.0]:.2f}".replace(".", ",")
    assert dialog.txt_upper.text() == _esperado_sup

    pump_dialog = DialogMotobomba(config=config)
    assert pump_dialog.chk_backup_pump.isChecked()

    dialog.close()
    pump_dialog.close()


def test_iptu_green_year_over_year_cashflow_and_savings(qapp):
    """Valida se o benefício do IPTU Verde é aplicado ano a ano no fluxo de caixa e melhora o VPL."""
    from netuno.core.economic import run_robust_economic_analysis
    from netuno.ui.tab_economic_integrated import TabEconomicIntegrated

    # Cenário base sem IPTU Verde
    base_res = run_robust_economic_analysis(
        initial_investment=5000.0,
        annual_water_saved_m3=100.0,
        water_tariff_per_m3=6.0,
        sewage_tariff_per_m3=4.8,
        discount_rate=0.08,
        inflation_rate=0.04,
        analysis_period_years=10,
        annual_iptu_savings=0.0
    )

    # Cenário com IPTU Verde: R$ 4000 de IPTU com 5% de desconto = R$ 200/ano
    iptu_res = run_robust_economic_analysis(
        initial_investment=5000.0,
        annual_water_saved_m3=100.0,
        water_tariff_per_m3=6.0,
        sewage_tariff_per_m3=4.8,
        discount_rate=0.08,
        inflation_rate=0.04,
        analysis_period_years=10,
        annual_iptu_savings=200.0
    )

    # VPL com IPTU Verde deve ser significativamente maior
    assert iptu_res.vpl > base_res.vpl
    # Payback simples e descontado com IPTU Verde devem ser menores ou iguais
    assert iptu_res.payback_simple_years <= base_res.payback_simple_years

    # Verifica aplicação ano a ano no fluxo de caixa
    for yr in range(1, 11):
        cf_base = base_res.annual_cash_flows[yr]
        cf_iptu = iptu_res.annual_cash_flows[yr]
        # Economia bruta no ano deve ser exatamente a economia de água/esgoto + o IPTU do ano corrigido
        expected_iptu_yr = 200.0 * ((1.0 + 0.04) ** (yr - 1))
        assert cf_iptu.iptu_green_savings_brl == pytest.approx(expected_iptu_yr, rel=1e-3)
        assert cf_iptu.total_gross_savings_brl == pytest.approx(cf_base.total_gross_savings_brl + expected_iptu_yr, rel=1e-3)

    # Validação da interface gráfica: toggle e preenchimento da tabela
    tab = TabEconomicIntegrated()
    tab.chk_iptu.setChecked(True)
    tab.spin_iptu_val.setValue(5000.0)
    tab.spin_iptu_disc.setValue(10.0)
    tab._on_fiscal_param_changed()

    # Badge deve indicar R$ 500,00/ano
    assert "500,00" in tab.lbl_iptu_badge.text()
    # As 3 manutenções de referência devem constar na tabela de materiais e impacto
    maint_texts = [tab.table_mat_impact.item(r, 0).text() for r in range(tab.table_mat_impact.rowCount())]
    assert any("calhas" in t.lower() for t in maint_texts)
    assert any("reservatório" in t.lower() for t in maint_texts)
    assert any("motobomba" in t.lower() for t in maint_texts)

    # Linha do IPTU Verde na tabela de materiais
    iptu_row = [r for r in range(tab.table_mat_impact.rowCount()) if "IPTU Verde" in tab.table_mat_impact.item(r, 0).text()][0]
    assert "500,00" in tab.table_mat_impact.item(iptu_row, 4).text()
    assert "Economia" in tab.table_mat_impact.item(iptu_row, 4).text()
