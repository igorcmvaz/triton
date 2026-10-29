"""Suíte essencial do Triton que exige a interface gráfica: telas que levam dado ao cálculo,
paridade tela × linha de comando, edições e a Modulação Probabilística na tela.

Fica fora da integração contínua sem Qt, como a pasta tests/ui (ver tests/conftest.py).
"""
import pathlib as _pathlib
import pytest
import numpy as np
from triton.core.parser import TritonConfig
from triton.core.simulation import SingleTankSimulationResult, SimulationDayResult
from triton.core.economic import calculate_water_bill, run_economic_analysis
from triton.core.economic import calculate_water_bill
from triton.ui.dialogs.dialog_economic import DialogElectricity, DialogTariffs
from triton.core.environmental import EnvironmentalConfig, PipeInput, PumpInput, calculate_lca, run_environmental_sweep, MATERIAL_PRESETS, PIPE_EMISSION_FACTORS_PER_METER, PUMP_EMBEDDED_CO2
from triton.core.chlorination import Cloracao
from triton.ui.dialogs.pump_wizard_dialog import calculate_forchheimer_diameter, find_commercial_recalque, get_suction_pipe, COMMERCIAL_PIPES, PUMP_CATALOG
from triton.core.pump_hydraulics import energia_especifica_kwh_por_m3
from triton.ui.dialogs.pump_wizard_dialog import PUMP_CATALOG, PumpSelectionWizardDialog
from triton.core.chlorination import PUREZA_PADRAO
from triton.core.environmental import EnvironmentalConfig, calculate_lca, pump_embodied_co2_is_extrapolated
from triton.core.grid_emission_factors import BASE_PADRAO, bases_disponiveis, fator_co2eq, procedencia_da_base
from triton.core.topsis import TopsisCandidate, calculate_topsis_scores
from triton.core.esg_certifications import calculate_esg_certifications, EsgConsolidatedReport, LeedWaterCredits, AquaHqeRating, CasaAzulRating
import json
import re
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from triton import cli
from triton.core.economic import run_economic_analysis
from triton.core.environmental import EnvironmentalConfig, calculate_lca
from triton.core.simulation import SingleTankSimulationResult
from PySide6.QtWidgets import QApplication
from triton.ui.main_window import MainWindow
from triton.core.report_generator import generate_environmental_html_report, generate_executive_html_report
import os
import tempfile
from triton.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram, _safe_float
from triton.core.report_generator import generate_executive_html_report, generate_research_html_report, save_pdf_report
from triton.core.report_service import normalize_report_type
from triton.core import modulacao_estocastica as M
from triton.core.parser import load_triton_project
import unittest
from triton.core.tariffs_database import get_city_data, get_city_tariffs_by_category, CATEGORIAS_TARIFARIAS, categorias_coletadas
from triton.core.edition import neutralizar_para_a_internacional, rotulo_da_edicao
from triton.core.tariffs_structure import EXPOENTE_DE_CONSUMO, PRECO_BASE_EXPONENCIAL
from triton.ui.dialogs.pipe_runs_dialog import PipeRunsDialog, format_origin, parse_origin
from triton.ui.tab_building import TabBuilding, BUILDING_TEMPLATES
from PySide6.QtCore import QPointF
from triton.core.volumetry import build_volumetry
from triton.ui.volumetry_view import VolumetryPanel
from tests.test_essencial import _volumetry_project as _project  # mesmo projeto de exemplo da volumetria
from triton.ui.tab_economic_global_optimizer import TabEconomicGlobalOptimizer
from triton.ui.tab_building import TabBuilding
from triton.core.hydrology_defaults import LAMINA_DE_DESCARTE_PADRAO_MM
from triton.ui.tab_project import TabProject
from PySide6.QtWidgets import QApplication, QTableWidget
from triton.ui.tab_tanks_simulation import TabTanksSimulation
from PySide6.QtWidgets import QApplication, QMessageBox
from triton.core.study_layout import generate_study_layout

_TESTES = _pathlib.Path(__file__).resolve().parent


# ==================================================================================================
# Economia e tarifas: sentido do VPL, regimes de cobrança, preços e investimento
# ==================================================================================================

# ---- origem: tests/unit/test_economic.py

def test_water_bill_multi_tier_calculation():
    """Valida cálculo da conta de água por faixas de consumo."""
    tariffs = [(0, 10, 25.0, -1), (10, 25, 5.0, 0), (25, 50, 7.0, 0), (50, 100000, 8.0, 0)]
    bill_5m3 = calculate_water_bill(5000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_5m3 == 50.0
    bill_15m3 = calculate_water_bill(15000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_15m3 == 100.0
    bill_30m3 = calculate_water_bill(30000.0, tariffs, sewage_mode=1, sewage_rate=100.0)
    assert bill_30m3 == 270.0


def test_sewage_fixed_and_water_taxes():
    """Valida esgoto em valor fixo e impostos fixos/variáveis sobre a tarifa de água."""
    tariffs = [(0, 999, 4.0, 0)]
    bill = calculate_water_bill(vol_liters=10000.0, tariffs=tariffs, sewage_mode=0, sewage_rate=15.0, water_tax_fixed=5.0, water_tax_var=10.0)
    assert bill == 64.0


def test_additional_operational_costs():
    """Valida a inclusão de outros custos operacionais (manutenção linear e angular)."""
    config = TritonConfig()
    config.cost_lower_tank = 1000.0
    config.cost_upper_tank = 500.0
    config.analysis_period_years = 5
    config.op_costs = [('Manutenção Anual', 12, 120.0, 0.0), ('Insumos Tratamento', 1, 0.0, 0.5)]
    sim_res = SingleTankSimulationResult(lower_tank_vol=2000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=500.0, avg_potable_consumed_l_day=500.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=50.0, pct_days_partial_satisfaction=0.0, pct_days_null_satisfaction=50.0)
    econ = run_economic_analysis(config, sim_res)
    cf1 = econ.monthly_cash_flows[0]
    assert cf1.om_cost > 0.0
    cf12 = econ.monthly_cash_flows[11]
    assert cf12.om_cost > cf1.om_cost


def test_separate_tariff_escalations_and_pump_metrics():
    """Valida o funcionamento dos reajustes tarifários separados e métricas de energia da motobomba."""
    config = TritonConfig()
    config.upper_tank_vol = 1000.0
    config.upper_tank_used = True
    config.pumping_threshold_pct = 80.0
    config.water_tariff_escalation = 6.0
    config.sewage_tariff_escalation = 4.0
    config.elec_tariff_escalation = 8.0
    config.pump_power_kw = 0.7355
    config.pump_flow_rate = 2000.0
    config.elec_tariff = 0.9
    sim_res = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=60.0, avg_pluvial_consumed_l_day=600.0, avg_potable_consumed_l_day=400.0, avg_spilled_l_day=50.0, pct_days_full_satisfaction=60.0, pct_days_partial_satisfaction=20.0, pct_days_null_satisfaction=20.0, total_pumped_liters=18000.0, total_pump_cycles=60, daily_results=[])
    econ = run_economic_analysis(config, sim_res)
    assert econ.monthly_pump_kwh > 0.0
    assert econ.annual_pump_kwh > 0.0
    assert econ.monthly_pump_cost_brl > 0.0
    assert econ.annual_pump_cost_brl > 0.0


def test_robust_sensitivity_rate_normalization():
    """Taxas anuais entram como fração decimal; um valor percentual é recusado, e não reinterpretado."""
    from triton.core.economic import run_robust_economic_analysis, run_sensitivity_analysis
    base_params = {'initial_investment': 8950.0, 'annual_water_saved_m3': 53.8, 'water_tariff_per_m3': 6.5, 'sewage_tariff_per_m3': 5.2, 'sewage_mode': 1, 'water_tariff_escalation_rate': 0.05, 'sewage_tariff_escalation_rate': 0.05, 'elec_tariff_escalation_rate': 0.05, 'inflation_rate': 0.04, 'discount_rate': 0.08, 'annual_om_cost_base': 150.0, 'analysis_period_years': 20}
    with pytest.raises(ValueError, match='parece estar em percentual'):
        run_robust_economic_analysis(**{**base_params, 'water_tariff_escalation_rate': 5.0})
    res_base = run_robust_economic_analysis(**base_params)
    assert -20000.0 < res_base.vpl < 20000.0
    sens_data = run_sensitivity_analysis(base_params)
    reajuste_points = sens_data['Reajuste Tarifário Água']
    vpls_reajuste = [p[1] for p in reajuste_points]
    for vpl_val in vpls_reajuste:
        assert abs(vpl_val) < 100000.0


def test_step5_and_step7_exact_parity():
    """Garante paridade matemática absoluta entre os resultados da Etapa 5 e da Opção 1 da Etapa 7."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    from triton.ui.main_window import MainWindow
    window = MainWindow()
    window.tab_project.precip_data = np.array([10.0] * 365, dtype=float)
    window.tab_tanks_simulation.precip_data = window.tab_project.precip_data
    window.sync_project_state()
    window.config.precip_file = 'synthetic.csv'
    window.tab_building.txt_area.setText('150')
    window.tab_building.txt_demand.setText('150')
    window.tab_building.txt_residents.setText('4')
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
    window.config.tma = 1.0
    window.config.inflation = 0.4
    window.tab_economic._internal_config = window.config
    window.tab_tanks_simulation.txt_inflation.setText('0.4')
    window.tab_tanks_simulation.txt_period.setText('20')
    window.tab_tanks_simulation.txt_tma.setText('1.0')
    window.tab_tanks_simulation.txt_readj_period.setText('12')
    window.tab_tanks_simulation.txt_readj_water.setText('5.0')
    window.tab_tanks_simulation.txt_readj_elec.setText('5.0')
    window.tab_tanks_simulation.verified_dialogs = {'capex', 'motobomba', 'opex', 'tariffs'}
    window.tab_tanks_simulation.selected_volume_mode = 'custom'
    window.tab_tanks_simulation.custom_selected_vol = 5000.0
    window.tab_tanks_simulation.txt_sweep_max.setText('5000')
    window.tab_tanks_simulation.txt_sweep_step.setText('2500')
    window.tab_tanks_simulation.txt_delta_ideal.setText('5.0')
    window.tab_tanks_simulation.txt_pump_thresh_pct.setText('10.0')
    window.tab_tanks_simulation.run_simulation(force=False)
    econ_step5 = getattr(window.tab_economic, 'last_result', getattr(window.tab_economic, 'last_econ_res', None))
    assert econ_step5 is not None
    window.tab_global_optimizer.recalculate_all()
    table7 = window.tab_global_optimizer.table
    assert table7.rowCount() > 0
    target_row = next((r for r in range(table7.rowCount()) if '5000' in table7.item(r, 1).text()))
    vpl_step7_str = table7.item(target_row, 8).text()
    # Qualquer símbolo de moeda (R$, €, $...): fica só o número no formato da interface.
    vpl_step7 = float(re.sub(r'[^0-9,.\-]', '', vpl_step7_str).replace('.', '').replace(',', '.'))
    vpl_step5_5000 = window.tab_economic.last_sweep_econ_results[5000.0]['vpl']
    assert vpl_step5_5000 == pytest.approx(vpl_step7, abs=200.0)


def test_operational_cost_annualization_preserves_netuno4_throughput_basis():
    from triton.core.cost_estimates import annualize_operational_costs
    items = [('Inspeção anual', 12, 120.0, 0.0), ('Tratamento mensal', 1, 10.0, 0.5)]
    assert annualize_operational_costs(items, 120.0) == pytest.approx(300.0)


def test_effective_tariff_uses_actual_total_demand_when_available():
    from triton.core.economic import calculate_effective_tariff
    cfg = TritonConfig()
    cfg.water_tariffs = [(0.0, 10.0, 1.0, 0), (10.0, 999999.0, 2.0, 0)]
    cfg.sewage_mode = 1
    cfg.sewage_rate = 100.0
    water, sewage = calculate_effective_tariff(cfg, annual_m3_saved=120.0, annual_total_demand_m3=240.0)
    assert water == pytest.approx(2.0)
    assert sewage == pytest.approx(2.0)


def test_capex_dialog_opens_recalculated_for_every_sweep_volume(qapp):
    from triton.ui.dialogs.dialog_economic import DialogInitialCosts, DialogMotobomba
    config = TritonConfig()
    config.cost_upper_tank = 9999.0
    dialog = DialogInitialCosts(config=config, evaluated_volumes=[0, 1000, 2000, 3000])
    assert dialog.table_lower_costs.rowCount() == 4
    assert dialog.table_lower_costs.item(0, 0).text() == '0'
    from triton.core.cost_estimates import LOWER_TANK_PRICE_TABLE
    _esperado = f'{dict(LOWER_TANK_PRICE_TABLE)[1000.0]:.2f}'.replace('.', ',')
    assert _esperado in dialog.table_lower_costs.item(1, 1).text()
    from triton.core.cost_estimates import UPPER_TANK_PRICE_TABLE
    _esperado_sup = f'{dict(UPPER_TANK_PRICE_TABLE)[500.0]:.2f}'.replace('.', ',')
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        assert dialog.txt_upper.text() == _esperado_sup
    else:   # sem catálogo de preços, o campo é o que o projeto informa; sem estimativa
        assert dialog.txt_upper.text() != _esperado_sup
    pump_dialog = DialogMotobomba(config=config)
    assert pump_dialog.chk_backup_pump.isChecked()
    dialog.close()
    pump_dialog.close()


def test_iptu_green_year_over_year_cashflow_and_savings(qapp):
    """Valida se o benefício do IPTU Verde é aplicado ano a ano no fluxo de caixa e melhora o VPL."""
    from triton.core.economic import run_robust_economic_analysis
    from triton.ui.tab_economic_integrated import TabEconomicIntegrated
    base_res = run_robust_economic_analysis(initial_investment=5000.0, annual_water_saved_m3=100.0, water_tariff_per_m3=6.0, sewage_tariff_per_m3=4.8, discount_rate=0.08, inflation_rate=0.04, analysis_period_years=10, annual_iptu_savings=0.0)
    iptu_res = run_robust_economic_analysis(initial_investment=5000.0, annual_water_saved_m3=100.0, water_tariff_per_m3=6.0, sewage_tariff_per_m3=4.8, discount_rate=0.08, inflation_rate=0.04, analysis_period_years=10, annual_iptu_savings=200.0)
    assert iptu_res.vpl > base_res.vpl
    assert iptu_res.payback_simple_years <= base_res.payback_simple_years
    for yr in range(1, 11):
        cf_base = base_res.annual_cash_flows[yr]
        cf_iptu = iptu_res.annual_cash_flows[yr]
        expected_iptu_yr = 200.0 * (1.0 + 0.04) ** (yr - 1)
        assert cf_iptu.iptu_green_savings_brl == pytest.approx(expected_iptu_yr, rel=0.001)
        assert cf_iptu.total_gross_savings_brl == pytest.approx(cf_base.total_gross_savings_brl + expected_iptu_yr, rel=0.001)
    tab = TabEconomicIntegrated()
    tab.chk_iptu.setChecked(True)
    tab.spin_iptu_val.setValue(5000.0)
    tab.spin_iptu_disc.setValue(10.0)
    tab._on_fiscal_param_changed()
    assert '500,00' in tab.lbl_iptu_badge.text()
    maint_texts = [tab.table_mat_impact.item(r, 0).text() for r in range(tab.table_mat_impact.rowCount())]
    assert any(('calhas' in t.lower() for t in maint_texts))
    assert any(('reservatório' in t.lower() for t in maint_texts))
    assert any(('motobomba' in t.lower() for t in maint_texts))
    iptu_row = [r for r in range(tab.table_mat_impact.rowCount()) if 'IPTU Verde' in tab.table_mat_impact.item(r, 0).text()][0]
    assert '500,00' in tab.table_mat_impact.item(iptu_row, 4).text()
    assert 'Economia' in tab.table_mat_impact.item(iptu_row, 4).text()


# ---- origem: tests/unit/test_impostos_e_bomba_reserva.py

TARIFA_SIMPLES = [(0.0, 10.0, 3.08, 1), (10.0, 999999.0, 6.81, 1)]


def _config(**trocas):
    cfg = TritonConfig()
    cfg.water_tariffs = list(TARIFA_SIMPLES)
    cfg.sewage_mode, cfg.sewage_rate = (1, 100.0)
    for k, v in trocas.items():
        setattr(cfg, k, v)
    return cfg


def test_o_imposto_da_agua_nao_e_zerado_ao_fechar(qapp):
    """Antes, `on_accept` atribuía 0.0 aos dois, apagando o que viesse do arquivo."""
    cfg = _config(water_tax_fixed=4.75, water_tax_var=12.5)
    d = DialogTariffs(config=cfg)
    d.on_accept()
    assert cfg.water_tax_fixed == pytest.approx(4.75)
    assert cfg.water_tax_var == pytest.approx(12.5)


def test_o_imposto_da_energia_nao_e_zerado_ao_fechar(qapp):
    cfg = _config(elec_tax_fixed=9.2, elec_tax_var=29.5)
    d = DialogElectricity(config=cfg)
    d.on_accept()
    assert cfg.elec_tax_fixed == pytest.approx(9.2)
    assert cfg.elec_tax_var == pytest.approx(29.5)


def test_o_que_o_usuario_digita_e_o_que_chega_ao_config(qapp):
    """Vírgula decimal, como o resto do programa aceita."""
    cfg = _config()
    d = DialogTariffs(config=cfg)
    d.txt_tax_fix.setText('3,40')
    d.txt_tax_var.setText('7,25')
    d.on_accept()
    assert cfg.water_tax_fixed == pytest.approx(3.4)
    assert cfg.water_tax_var == pytest.approx(7.25)


def test_campo_vazio_ou_ilegivel_nao_derruba_a_tela(qapp):
    cfg = _config(water_tax_fixed=1.0)
    d = DialogTariffs(config=cfg)
    d.txt_tax_fix.setText('')
    d.txt_tax_var.setText('abc')
    d.on_accept()
    assert cfg.water_tax_fixed == 0.0
    assert cfg.water_tax_var == 0.0


def test_o_imposto_da_agua_move_a_conta():
    """Percurso fechado: se o campo não mudasse a conta, o campo seria decorativo."""
    sem = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 0.0)
    com = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 5.0, 10.0)
    assert com > sem
    assert com - sem > 5.0


def test_o_imposto_fixo_e_o_variavel_agem_por_caminhos_diferentes():
    base = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 0.0)
    so_fixo = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 7.0, 0.0)
    so_var = calculate_water_bill(20.0, TARIFA_SIMPLES, 1, 100.0, 0.0, 20.0)
    assert so_fixo - base == pytest.approx(7.0)
    assert so_var > base


@pytest.mark.parametrize('quantas', [1, 2])
def test_a_contagem_de_bombas_volta_como_foi_escolhida(qapp, quantas):
    """A caixa era marcada por um ternário que devolvia True nos dois ramos."""
    cfg = _config(pump_count=quantas, pump_power_kw=0.37, pump_efficiency=60.0, pump_flow_rate=3000.0)
    d = DialogElectricity(config=cfg)
    assert d.chk_backup_pump.isChecked() is (quantas >= 2)
    d.on_accept()
    assert cfg.pump_count == quantas


def test_desmarcar_a_reserva_deixa_uma_bomba(qapp):
    cfg = _config(pump_count=2, pump_power_kw=0.37, pump_efficiency=60.0, pump_flow_rate=3000.0)
    d = DialogElectricity(config=cfg)
    d.chk_backup_pump.setChecked(False)
    d.on_accept()
    assert cfg.pump_count == 1


# ==================================================================================================
# Ambiente e energia: emissões, cloro, bombeamento e arranjo
# ==================================================================================================

# ---- origem: tests/unit/test_environmental.py

def test_prfv_alias_uses_fiberglass_preset_and_zero_is_no_system_baseline():
    alias = calculate_lca(5000.0, 100.0, EnvironmentalConfig(lower_material_key='PRFV'))
    canonical = calculate_lca(5000.0, 100.0, EnvironmentalConfig(lower_material_key='FIBRA'))
    assert alias.lower_tank_mass_kg == pytest.approx(canonical.lower_tank_mass_kg)
    assert alias.total_embodied_co2_kg == pytest.approx(canonical.total_embodied_co2_kg)
    baseline = calculate_lca(0.0, 0.0, EnvironmentalConfig())
    assert baseline.total_embodied_co2_kg == pytest.approx(0.0)
    assert baseline.lifetime_net_co2_saved_kg == pytest.approx(0.0)


def test_chlorine_mass_and_emissions_are_calculated_from_dose():
    """A massa reportada e de PRODUTO comercial, nao de cloro ativo.

    A distincao nao e cosmetica. A dose e prescrita em mg de cloro ativo por
    litro, mas o que se compra, se transporta e se fabrica e a pastilha, que tem
    65% de cloro ativo. Somar uma dose de cloro ativo a um fator de emissao por
    kg de pastilha subestima em 35%, e era metade da divergencia de 11,7x que
    existia entre o modulo ambiental e o de qualidade.
    """
    config = EnvironmentalConfig(upper_tank_used=True, pipes=[], chlorine_dose_mg_l=2.0)
    result = calculate_lca(5000.0, 100.0, config)
    cloracao = Cloracao(dose_mg_por_litro=2.0, pureza=config.chlorine_product_purity, fator_kg_co2e_por_kg_produto=config.chlorine_co2_kg_per_kg)
    assert cloracao.cloro_ativo_kg_por_m3 * 100 == pytest.approx(0.2)
    assert result.annual_chlorine_kg == pytest.approx(0.2 / config.chlorine_product_purity)
    assert result.treatment_co2_kg_per_m3 == pytest.approx(cloracao.co2e_kg_por_m3)
    assert result.annual_treatment_co2_kg == pytest.approx(cloracao.co2e_anual_kg(100.0))


def test_os_modulos_ambiental_e_de_qualidade_concordam_no_cloro():
    """Os dois usavam bases diferentes e divergiam por 11,7x."""
    from triton.core.chlorination import FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO, PUREZA_PADRAO
    config = EnvironmentalConfig()
    assert config.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    assert config.chlorine_product_purity == PUREZA_PADRAO


def test_environmental_sweep_uses_pump_energy_of_each_volume():
    config = EnvironmentalConfig(lower_material_key='PEAD', grid_co2_factor_kg_kwh=1.0, chlorine_dose_mg_l=0.0)
    result = run_environmental_sweep([(1000.0, 100.0, 10.0), (2000.0, 100.0, 30.0)], config)
    assert result.sweep_details[0]['lca_result'].annual_pumping_co2_kg == pytest.approx(10.0)
    assert result.sweep_details[1]['lca_result'].annual_pumping_co2_kg == pytest.approx(30.0)


def test_a_contagem_de_bombas_e_a_mesma_no_projeto_e_na_acv():
    """Os dois padrões divergiam, e ninguém via.

    `TritonConfig.pump_count` sempre foi 2 — principal mais reserva, a
    configuração inicial recomendada — e o módulo econômico cobra as duas
    (`pump_unit_cost × pump_count`). `EnvironmentalConfig.pump_count` era 1, de
    modo que a avaliação de ciclo de vida contava o carbono de uma bomba só,
    18 kg CO₂e a menos, para o mesmo sistema que o econômico orçava com duas.

    A divergência só aparecia quando a configuração ambiental era construída sem
    o projeto — geração de relatório e alguns caminhos de otimização.
    """
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.parser import TritonConfig
    assert EnvironmentalConfig().pump_count == TritonConfig().pump_count


def test_o_carbono_da_bomba_dobra_com_a_bomba_reserva():
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    uma = calculate_lca(5000.0, 100.0, EnvironmentalConfig(annual_water_saved_m3=100.0, pump_count=1))
    duas = calculate_lca(5000.0, 100.0, EnvironmentalConfig(annual_water_saved_m3=100.0, pump_count=2))
    assert duas.pump_embodied_co2_kg == pytest.approx(2 * uma.pump_embodied_co2_kg)
    assert duas.total_embodied_co2_kg > uma.total_embodied_co2_kg


# ---- origem: tests/unit/test_pump_energy_details.py

def test_pump_backup_count_capex_cost():
    """Testa se a consideração da bomba de reserva multiplica o custo CAPEX por 2."""
    config_single = TritonConfig()
    config_single.pump_unit_cost = 850.0
    config_single.pump_count = 1
    assert config_single.pump_unit_cost * config_single.pump_count == 850.0
    config_backup = TritonConfig()
    config_backup.pump_unit_cost = 850.0
    config_backup.pump_count = 2
    assert config_backup.pump_unit_cost * config_backup.pump_count == 1700.0


# ---- origem: tests/unit/test_pump_wizard.py

def test_forchheimer_calculation():
    q_m3s = 3.6 / 3600.0
    t_h = 2.0
    d_m = calculate_forchheimer_diameter(q_m3s, t_h)
    d_mm = d_m * 1000.0
    assert 15.0 <= d_mm <= 35.0
    rec_pipe = find_commercial_recalque(d_m)
    assert rec_pipe['dn'] in [25, 32, 40]
    assert rec_pipe['di_mm'] >= d_mm * 0.9


def test_suction_pipe_one_size_above():
    for i in range(len(COMMERCIAL_PIPES) - 1):
        rec_pipe = COMMERCIAL_PIPES[i]
        suc_pipe = get_suction_pipe(rec_pipe)
        expected_suc = COMMERCIAL_PIPES[i + 1]
        assert suc_pipe['dn'] == expected_suc['dn'], f'Para recalque {rec_pipe['dn']}, sucção esperada {expected_suc['dn']}'
        assert suc_pipe['dn'] > rec_pipe['dn'], f'Sucção {suc_pipe['dn']} deve ser maior que recalque {rec_pipe['dn']}'


def test_commercial_pump_catalog_consistency():
    assert len(PUMP_CATALOG) >= 6
    for pump in PUMP_CATALOG:
        assert pump['cv'] > 0
        assert pump['kw'] > 0
        assert pump['flow_lh'] > 0
        assert pump['max_h'] > 0
        assert pump['cost'] > 0
        assert 'bocal_suc' in pump and pump['bocal_suc']
        assert 'bocal_rec' in pump and pump['bocal_rec']
        assert pump['rec_pipe_dn'] in [25, 32, 40, 50, 60, 75]
        assert pump['suc_pipe_dn'] in [25, 32, 40, 50, 60, 75]
        assert pump['rec_pipe_dn'] >= 25
        assert pump['suc_pipe_dn'] >= 32
        assert pump['suc_pipe_dn'] > pump['rec_pipe_dn'], f'Bomba {pump['brand']}: sucção ({pump['suc_pipe_dn']}) deve ser estritamente maior que recalque ({pump['rec_pipe_dn']})'


def test_motobomba_model_governs_pipes_over_forchheimer(qapp):
    from triton.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    dlg = PumpSelectionWizardDialog(upper_tank_vol=350.0)
    data = dlg.selected_pump_data
    assert data is not None
    assert data['recalque_dn'] >= 25
    assert data['suction_dn'] >= 32
    assert data['suction_dn'] > data['recalque_dn']
    idx_1cv = -1
    for i in range(dlg.combo_pump.count()):
        p = dlg.combo_pump.itemData(i)
        if p and p.get('cv') == 1.0:
            idx_1cv = i
            break
    assert idx_1cv >= 0
    dlg.combo_pump.setCurrentIndex(idx_1cv)
    data_1cv = dlg.selected_pump_data
    assert data_1cv['recalque_dn'] == 40
    assert data_1cv['suction_dn'] == 50


def test_wizard_no_forchheimer_text_and_commercial_pipes():
    from triton.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    from triton.core.cost_estimates import COMMERCIAL_PIPES_CAPEX, _DEFAULT_PIPE_COST_PER_METER
    from triton.core.parser import TritonConfig
    for p in COMMERCIAL_PIPES:
        assert any((cp['dn'] == p['dn'] for cp in COMMERCIAL_PIPES_CAPEX)), f'DN {p['dn']} ausente no CAPEX'
        assert p['dn'] in _DEFAULT_PIPE_COST_PER_METER, f'Preço de DN {p['dn']} ausente na tabela de custos'
    assert any((cp['dn'] == 100 for cp in COMMERCIAL_PIPES_CAPEX))
    assert any((cp['dn'] == 150 for cp in COMMERCIAL_PIPES_CAPEX))
    cfg = TritonConfig()
    cfg.set_pipe_length(20, 12.5)
    assert cfg.get_pipe_length(20) == 12.5
    d = cfg.get_pipe_lengths_dict()
    assert 20 in d and d[20] == 12.5


def test_dialog_other_op_costs_height_and_items(qapp):
    from triton.ui.dialogs.dialog_economic import DialogOtherOpCosts
    dlg = DialogOtherOpCosts()
    assert dlg.minimumHeight() >= 600 or dlg.height() >= 600
    assert dlg.table.minimumHeight() >= 150
    assert dlg.table.rowCount() == 3
    assert len(dlg.op_costs) == 3


def test_dialog_initial_costs_all_commercial_pipes(qapp):
    from triton.ui.dialogs.dialog_economic import DialogInitialCosts
    from triton.core.cost_estimates import COMMERCIAL_PIPES_CAPEX
    from triton.core.parser import TritonConfig
    cfg = TritonConfig()
    cfg.set_pipe_length(25, 10.0)
    cfg.set_pipe_length(32, 12.0)
    cfg.set_pipe_length(110, 8.0)
    dlg = DialogInitialCosts(config=cfg)
    assert hasattr(dlg, 'txt_pipes')
    assert len(dlg.txt_pipes) == len(COMMERCIAL_PIPES_CAPEX)
    for p in COMMERCIAL_PIPES_CAPEX:
        dn = p['dn']
        assert dn in dlg.txt_pipes
        assert dn in dlg.lbl_pipe_costs
        assert hasattr(dlg, f'txt_pipe_{dn}')
    assert float(dlg.txt_pipes[25].text().replace(',', '.')) == 10.0
    assert float(dlg.txt_pipes[32].text().replace(',', '.')) == 12.0
    assert float(dlg.txt_pipes[110].text().replace(',', '.')) == 8.0
    dlg.txt_pipes[40].setText('15,0')
    dlg.on_accept()
    assert cfg.get_pipe_length(40) == 15.0


# ---- origem: tests/unit/test_pump_wizard_chain.py

@pytest.fixture
def assistente(qapp):
    return PumpSelectionWizardDialog(upper_tank_vol=500.0)


def test_o_catalogo_tem_bombas_reais_e_coerentes():
    assert len(PUMP_CATALOG) >= 5
    for bomba in PUMP_CATALOG:
        for campo in ('brand', 'cv', 'kw', 'flow_lh', 'max_h', 'cost'):
            assert bomba.get(campo), f'{bomba.get('label')} sem {campo}'
        assert bomba['kw'] == pytest.approx(bomba['cv'] * 0.7355, rel=0.12), bomba['label']
    potencias = [b['kw'] for b in PUMP_CATALOG]
    assert potencias == sorted(potencias)


def test_a_altura_manometrica_sai_do_assistente(assistente):
    """Era calculada e descartada."""
    assistente.spin_h_geom.setValue(10.0)
    assistente.recalculate()
    dados = assistente.selected_pump_data
    assert dados['manometric_head_m'] > 0
    assert dados['geometric_head_m'] == pytest.approx(10.0)
    assert dados['head_loss_m'] >= 0
    assert dados['manometric_head_m'] == pytest.approx(dados['geometric_head_m'] + dados['head_loss_m'], rel=1e-06)


def test_desnivel_maior_leva_a_bomba_maior(assistente):
    """É o propósito do assistente, e precisa continuar valendo."""
    potencias = []
    for altura in (4.0, 15.0, 40.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        potencias.append(assistente.selected_pump_data['kw'])
    assert potencias == sorted(potencias)
    assert potencias[-1] > potencias[0]


def test_a_bomba_escolhida_vence_a_altura_pedida(assistente):
    """Selecionar bomba que não alcança o desnível seria erro de projeto."""
    for altura in (4.0, 10.0, 20.0, 35.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data
        modelo = next((b for b in PUMP_CATALOG if b['kw'] == dados['kw']))
        assert modelo['max_h'] >= dados['manometric_head_m'], f'{modelo['label']} não alcança {dados['manometric_head_m']:.1f} mca'


def test_a_energia_por_m3_acompanha_o_desnivel(assistente):
    """O que se ganhou ao fechar o elo.

    Antes a energia saía da vazão nominal do catálogo, que não muda com a
    altura: casa térrea e sobrado davam o mesmo consumo por metro cúbico.
    """
    consumos = []
    for altura in (4.0, 15.0, 40.0):
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data
        consumos.append(energia_especifica_kwh_por_m3(dados['manometric_head_m'], dados['efficiency'] / 100.0))
    assert consumos == sorted(consumos)
    assert consumos[-1] > 3 * consumos[0]


def test_o_rendimento_do_assistente_chega_ao_retorno(assistente):
    """Era o segundo parâmetro calculado e descartado."""
    assistente.spin_efficiency.setValue(62.0)
    assistente.recalculate()
    assert assistente.selected_pump_data['efficiency'] == pytest.approx(62.0)


def test_dialog_electricity_open_pump_wizard(qapp, monkeypatch):
    """Garante que DialogElectricity._open_pump_wizard não falha com AttributeError."""
    from triton.core.parser import TritonConfig
    from triton.ui.dialogs.dialog_economic import DialogElectricity
    config = TritonConfig()
    dialog = DialogElectricity(config=config)

    class MockPumpWizard:

        def __init__(self, *args, **kwargs):
            self.selected_pump_data = {'cv': 0.5, 'kw': 0.37, 'flow_lh': 2500, 'efficiency': 50.0, 'cost': 450.0, 'suction_dn': 32, 'recalque_dn': 25, 'suction_len': 5.0, 'recalque_len': 20.0}

        def exec(self):
            return True
    monkeypatch.setattr('triton.ui.dialogs.pump_wizard_dialog.PumpSelectionWizardDialog', MockPumpWizard)
    dialog._open_pump_wizard()
    assert dialog.txt_power.text() == '0,50'
    assert dialog.combo_power_unit.currentText() == 'CV'
    assert dialog.txt_flow.text() == '2500'
    assert dialog.txt_eff.text() == '50,0'
    assert dialog.txt_unit_cost.text() == '450,00'


# ---- origem: tests/unit/test_environmental_params_ui.py

def test_escolher_a_base_muda_o_resultado_da_acv():
    valores = {c: fator_co2eq(c) for c in bases_disponiveis()}
    assert len(set(valores.values())) > 1, 'bases idênticas não seriam escolha'
    menor = min(valores, key=valores.get)
    maior = max(valores, key=valores.get)
    base = dict(annual_water_saved_m3=120.0, annual_pump_kwh=200.0)
    r_menor = calculate_lca(5000.0, 120.0, EnvironmentalConfig(grid_co2_factor_kg_kwh=valores[menor], grid_co2_factor_basis=menor, **base))
    r_maior = calculate_lca(5000.0, 120.0, EnvironmentalConfig(grid_co2_factor_kg_kwh=valores[maior], grid_co2_factor_basis=maior, **base))
    assert r_maior.annual_pumping_co2_kg > r_menor.annual_pumping_co2_kg


def test_a_pureza_muda_a_massa_de_produto_na_acv():
    """O efeito é de 1/pureza, e a pureza não era editável.

    Quem clora com água sanitária (cerca de 10% de cloro ativo) precisa de seis
    vezes mais produto que quem usa pastilha, e via o mesmo número.
    """

    def massa(pureza: float) -> float:
        cfg = EnvironmentalConfig(annual_water_saved_m3=120.0, chlorine_product_purity=pureza, etap_enabled=False)
        return calculate_lca(5000.0, 120.0, cfg).annual_chlorine_kg
    assert massa(0.325) == pytest.approx(2 * massa(0.65), rel=1e-09)
    assert massa(PUREZA_PADRAO) == pytest.approx(massa(0.65), rel=1e-09)


@pytest.fixture
def aba(qapp):
    from triton.ui.tab_environmental import TabEnvironmental
    return TabEnvironmental()


def test_a_aba_entrega_a_pureza_e_a_base_escolhidas(aba):
    """O diálogo grava as duas no estado da aba, e `get_config` as lê.

    Se `get_config` não as lesse, o controle seria decorativo — que é o defeito
    que ele existe para corrigir.
    """
    aba._pureza_do_cloro = 0.1
    aba._base_do_fator_da_rede = 'sidac'
    cfg = aba.get_config()
    assert cfg.chlorine_product_purity == pytest.approx(0.1)
    assert cfg.grid_co2_factor_basis == 'sidac'


def test_a_aba_entrega_a_escolha_de_desinfeccao_do_projeto(aba, monkeypatch):
    """A escolha feita na Etapa 2 tem de atravessar até a ACV."""
    from triton.core.parser import TritonConfig
    proj = TritonConfig()
    proj.water_quality_disinfection = 'uv'
    proj.water_quality_polishing = True
    proj.area = 320.0

    class _Janela:
        config = proj
    monkeypatch.setattr(type(aba), 'window', lambda self: _Janela(), raising=False)
    cfg = aba.get_config()
    assert cfg.water_quality_disinfection == 'uv'
    assert cfg.water_quality_polishing is True
    assert cfg.roof_area_m2 == pytest.approx(320.0)


def test_a_pureza_fora_da_faixa_e_contida(aba):
    """Zero ou negativo dividiria por zero na conversão de massa."""
    aba._pureza_do_cloro = 0.0
    assert aba.get_config().chlorine_product_purity > 0.0
    aba._pureza_do_cloro = 5.0
    assert aba.get_config().chlorine_product_purity <= 1.0


@pytest.fixture
def dialogo(aba, qapp):
    from triton.ui.tab_environmental import LCAParametersDialog
    return LCAParametersDialog(aba)


def test_o_dialogo_constroi_com_os_controles_novos(dialogo):
    """Um campo que só aparece na tela é o que este teste protege.

    Os testes de núcleo não constroem o diálogo, de modo que um erro de
    montagem passaria despercebido até o usuário abrir a janela.
    """
    assert dialogo.txt_chlorine_purity is not None
    assert dialogo.cmb_base_rede.count() >= 3


def test_escolher_a_base_reescreve_o_fator_e_mostra_a_procedencia(dialogo):
    """Era o ponto: as bases não eram selecionáveis, só o número era editável."""
    valores = {}
    for i in range(dialogo.cmb_base_rede.count()):
        dialogo.cmb_base_rede.setCurrentIndex(i)
        chave = dialogo.cmb_base_rede.currentData()
        valores[chave] = float(dialogo.txt_grid_co2.text().replace(',', '.'))
        assert dialogo.lbl_base_rede_fonte.text().strip(), chave
    for chave, valor in valores.items():
        assert valor == pytest.approx(fator_co2eq(chave), abs=5e-05), chave
    assert len(set(valores.values())) > 1


def test_salvar_devolve_a_pureza_e_a_base_para_a_aba(dialogo, aba):
    """Sem isto o valor escolhido morreria ao fechar a janela."""
    dialogo.txt_chlorine_purity.setText('0,10')
    idx = dialogo.cmb_base_rede.findData('sidac')
    if idx >= 0:
        dialogo.cmb_base_rede.setCurrentIndex(idx)
    dialogo.save_and_accept()
    assert aba._pureza_do_cloro == pytest.approx(0.1)
    assert aba.get_config().chlorine_product_purity == pytest.approx(0.1)
    if idx >= 0:
        assert aba.get_config().grid_co2_factor_basis == 'sidac'


# ==================================================================================================
# Decisão: TOPSIS, SMAA e certificações
# ==================================================================================================

# ---- origem: tests/unit/test_topsis.py

def candidate(volume, potential, overflow, vpl, payback, irr, lifecycle_co2, potable):
    return TopsisCandidate(lower_tank_vol=volume, water_saved_m3_yr=100.0 - potable, vpl_brl=vpl, co2_saved_kg_lifetime=-lifecycle_co2, potential_savings_pct=potential, overflow_m3_yr=overflow, discounted_payback_years=payback, irr_pct=irr, potable_consumed_m3_yr=potable)


def test_topsis_uses_all_seven_requested_criteria():
    candidates = [candidate(2000, 45, 22, 1000, 9, 8, 800, 55), candidate(5000, 70, 12, 4000, 5, 15, 500, 30), candidate(10000, 82, 5, 3500, 7, 12, 650, 18)]
    result = calculate_topsis_scores(candidates)
    assert result.decision_matrix.shape == (3, 7)
    assert result.criterion_gap_to_best.shape == (3, 7)
    assert result.criterion_weights.sum() == pytest.approx(1.0)
    assert len(result.criterion_keys) == 7
    assert result.rankings[result.best_index] == 1
    assert np.all((result.scores >= 0) & (result.scores <= 1))


def test_topsis_cost_and_benefit_directions_are_correct():
    candidates = [candidate(1000, 90, 30, 10, 9, 3, 900, 70), candidate(2000, 70, 5, 20, 3, 8, 400, 20), candidate(3000, 80, 15, 30, 6, 12, 700, 40)]
    result = calculate_topsis_scores(candidates)
    expected_best_rows = [0, 1, 2, 1, 2, 1, 1]
    for column, row in enumerate(expected_best_rows):
        assert result.criterion_gap_to_best[row, column] == pytest.approx(0.0)
        assert result.criterion_proximity_to_best[row, column] == pytest.approx(1.0)


def test_three_axis_weights_are_distributed_without_changing_axis_totals():
    result = calculate_topsis_scores([candidate(1000, 50, 10, 10, 5, 8, 300, 50)], weights=(0.2, 0.5, 0.3))
    assert result.criterion_weights[:2].sum() == pytest.approx(0.2)
    assert result.criterion_weights[2:5].sum() == pytest.approx(0.5)
    assert result.criterion_weights[5:].sum() == pytest.approx(0.3)


def test_seven_explicit_weights_are_supported():
    weights = (1, 2, 3, 4, 5, 6, 7)
    result = calculate_topsis_scores([candidate(1000, 50, 10, 10, 5, 8, 300, 50)], weights=weights)
    assert result.criterion_weights == pytest.approx(np.asarray(weights) / sum(weights))


def test_no_discounted_payback_is_worse_than_any_observed_return():
    candidates = [candidate(1000, 50, 10, 10, None, 8, 300, 50), candidate(2000, 50, 10, 10, 20, 8, 300, 50)]
    result = calculate_topsis_scores(candidates, weights=(0, 0, 0, 1, 0, 0, 0))
    assert result.best_index == 1
    assert result.decision_matrix[0, 3] > result.decision_matrix[1, 3]


def test_topsis_single_candidate_and_identical_candidates_are_stable():
    one = candidate(5000, 70, 10, 1000, 5, 10, 500, 30)
    result = calculate_topsis_scores([one])
    assert result.best_index == 0
    assert result.scores[0] == 1.0
    tied = calculate_topsis_scores([one, candidate(2000, 70, 10, 1000, 5, 10, 500, 30)])
    assert tied.scores == pytest.approx([0.5, 0.5])
    assert tied.best_candidate.lower_tank_vol == 2000


def test_topsis_empty_and_invalid_inputs():
    assert calculate_topsis_scores([]) is None
    valid = candidate(1000, 50, 10, 10, 5, 8, 300, 50)
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(-1.0, 1.0, 1.0))
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(0.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        calculate_topsis_scores([valid], weights=(1.0, 2.0))
    invalid = candidate(1000, np.nan, 10, 10, 5, 8, 300, 50)
    with pytest.raises(ValueError, match='technical_potential_pct'):
        calculate_topsis_scores([invalid])


def test_topsis_translation_is_invariant_to_column_origin():
    base = [candidate(1000, 10, 30, -100, 9, -3, 30, 70), candidate(2000, 15, 20, -50, 6, -2, 20, 50), candidate(3000, 20, 10, 10, 3, -1, 10, 30)]
    shifted = [candidate(c.lower_tank_vol, c.potential_savings_pct + 100, c.overflow_m3_yr + 100, c.vpl_brl + 5000, c.discounted_payback_years + 10, c.irr_pct + 30, c.lifecycle_co2_kg + 300, c.potable_consumed_m3_yr + 1000) for c in base]
    assert calculate_topsis_scores(base).scores == pytest.approx(calculate_topsis_scores(shifted).scores)


def test_optima_indices_follow_potential_vpl_and_minimum_lifecycle_co2():
    candidates = [candidate(1000, 90, 30, 10, 9, 3, 900, 70), candidate(2000, 70, 5, 30, 3, 8, 400, 20), candidate(3000, 80, 15, 20, 6, 12, 700, 40)]
    result = calculate_topsis_scores(candidates)
    assert result.technical_best_index == 0
    assert result.financial_best_index == 1
    assert result.environmental_best_index == 1


def test_financial_best_prefers_shorter_payback_over_higher_vpl():
    c_high_vpl_long_pb = candidate(5000, 85, 10, 50000, 6.0, 10, 500, 30)
    c_low_vpl_short_pb = candidate(2000, 65, 5, 30000, 2.0, 18, 200, 15)
    candidates = [c_high_vpl_long_pb, c_low_vpl_short_pb]
    res = calculate_topsis_scores(candidates)
    assert res.financial_best_index == 1


def test_zero_liter_is_never_financial_or_technical_optimum():
    c_zero = candidate(0, 0, 0, 0, 0.0, 0, 0, 100)
    c_2500 = candidate(2500, 60, 5, 20000, 3.2, 15, 200, 40)
    c_2500.is_technical_optimum = True
    c_5000 = candidate(5000, 80, 15, 25000, 4.5, 12, 400, 20)
    candidates = [c_zero, c_2500, c_5000]
    res = calculate_topsis_scores(candidates)
    assert res.financial_best_index == 1
    assert candidates[res.financial_best_index].lower_tank_vol == 2500.0
    assert res.technical_best_index == 1
    assert candidates[res.technical_best_index].lower_tank_vol == 2500.0


# ---- origem: tests/unit/test_esg_certifications.py

def test_esg_explicit_indoor_outdoor():
    res = calculate_esg_certifications(potable_savings_pct=35.0, annual_pluvial_consumed_m3=180.0, annual_potable_consumed_m3=320.0, net_co2e_saved_kg_lifetime=1800.0, indoor_savings_pct=32.0, outdoor_savings_pct=75.0, is_simplified_mode=False)
    assert res.indoor_savings_pct == 32.0
    assert res.outdoor_savings_pct == 75.0
    assert res.leed.indoor_water_points == 2
    assert res.leed.outdoor_water_points == 1
    assert res.leed.total_leed_we_points == 3


def test_esg_zero_outdoor_demand():
    """Valida que consumo externo zero resulta em 0 pontos no crédito LEED WEc1 e texto adequado."""
    res = calculate_esg_certifications(potable_savings_pct=42.0, annual_pluvial_consumed_m3=200.0, annual_potable_consumed_m3=276.0, net_co2e_saved_kg_lifetime=2500.0, project_lifetime_years=20, has_irrigation_demand=False, outdoor_demand_m3=0.0, outdoor_savings_pct=0.0, is_simplified_mode=False)
    assert res.leed.outdoor_water_points == 0
    assert res.outdoor_savings_pct == 0.0
    assert res.leed.indoor_water_points == 4
    assert res.leed.total_leed_we_points == 4
    wec1 = res.credit_details[0]
    assert wec1.credit_code == 'WEc1'
    assert wec1.achieved_performance == 'Sem consumo externo (0 m³/ano)'
    assert wec1.status == 'Não aplicável (sem rega/área externa)'
    assert wec1.points_or_level == '0 / 2 pts'


def test_esg_zero_outdoor_demand_simplified_mode():
    """Valida que no modo simplificado com demanda externa zero não se inventa partição de 15% nem economia fictícia."""
    res = calculate_esg_certifications(potable_savings_pct=42.0, annual_pluvial_consumed_m3=200.0, annual_potable_consumed_m3=276.0, net_co2e_saved_kg_lifetime=2500.0, project_lifetime_years=20, has_irrigation_demand=False, outdoor_demand_m3=0.0, is_simplified_mode=True)
    assert res.outdoor_savings_pct == 0.0
    assert res.leed.outdoor_water_points == 0
    wec1 = res.credit_details[0]
    assert wec1.achieved_performance == 'Sem consumo externo (0 m³/ano)'
    assert wec1.status == 'Não aplicável (sem rega/área externa)'
    assert wec1.points_or_level == '0 / 2 pts'
    assert res.indoor_savings_pct == pytest.approx(200.0 / 476.0 * 100.0, rel=0.01)


def test_certificacoes_usam_so_a_economia_total():
    """AQUA-HQE não sobe de nível por atalho do uso interno."""
    res = calculate_esg_certifications(potable_savings_pct=12.0, annual_pluvial_consumed_m3=60.0, annual_potable_consumed_m3=440.0, net_co2e_saved_kg_lifetime=500.0, indoor_savings_pct=36.0, outdoor_savings_pct=60.0)
    assert res.aqua.performance_level == 'Abaixo de EAU.1.2'
    assert any((i.startswith('EAU.1.5') for i in res.aqua.itens_atendidos))


@pytest.mark.parametrize('economia, nivel', [(19.9, 'Abaixo de EAU.1.2'), (20.0, 'HQE (EAU.1.2)'), (39.9, 'HQE (EAU.1.2)'), (40.0, 'HQE 3 (EAU.1.3)')])
def test_aqua_segue_os_itens_do_referencial_de_2024(economia, nivel):
    """Referencial AQUA-HQE Residencial v00 (22/11/2024): EAU.1.2 a 20%, EAU.1.3 a 40%.

    Os perfis «Base, Boas Práticas, Excelente» a 10, 25 e 40% não existem no referencial.
    """
    res = calculate_esg_certifications(potable_savings_pct=economia, annual_pluvial_consumed_m3=100.0, annual_potable_consumed_m3=300.0, net_co2e_saved_kg_lifetime=500.0)
    assert res.aqua.performance_level == nivel


@pytest.mark.parametrize('abrangencia, pontos', [(None, 0), ('areas_comuns', 2), ('loteamento', 2), ('unidades', 4), ('unidades_e_areas_comuns', 5)])
def test_casa_azul_pontua_pela_abrangencia_e_nao_pelo_percentual(abrangencia, pontos):
    """Guia Casa Azul + CAIXA V023 (29/04/2026), critério 3.6: o indicador é a existência."""
    for economia in (5.0, 35.0):
        res = calculate_esg_certifications(potable_savings_pct=economia, annual_pluvial_consumed_m3=50.0, annual_potable_consumed_m3=400.0, net_co2e_saved_kg_lifetime=100.0, casa_azul_abrangencia=abrangencia)
        assert res.casa_azul.criterion_met
        assert res.casa_azul.points_awarded == pontos
    sem_sistema = calculate_esg_certifications(potable_savings_pct=0.0, annual_pluvial_consumed_m3=0.0, annual_potable_consumed_m3=400.0, net_co2e_saved_kg_lifetime=0.0, casa_azul_abrangencia=abrangencia)
    assert not sem_sistema.casa_azul.criterion_met and sem_sistema.casa_azul.points_awarded == 0


@pytest.mark.parametrize('externa, pontos', [(49.9, 0), (50.0, 1), (96.0, 1), (100.0, 2)])
def test_wec1_segue_os_limiares_do_leed(externa, pontos):
    res = calculate_esg_certifications(potable_savings_pct=30.0, annual_pluvial_consumed_m3=100.0, annual_potable_consumed_m3=233.0, net_co2e_saved_kg_lifetime=500.0, has_irrigation_demand=True, outdoor_demand_m3=20.0, indoor_savings_pct=30.0, outdoor_savings_pct=externa)
    assert res.leed.outdoor_water_points == pontos


def test_irrigacao_atendida_sai_do_resultado_do_balanco():
    from types import SimpleNamespace
    from triton.core.esg_certifications import irrigacao_atendida_m3
    assert irrigacao_atendida_m3(None) is None
    r = SimpleNamespace(avg_pluvial_irrigation_consumed_l_day=100.0)
    assert irrigacao_atendida_m3(r) == pytest.approx(36.525)


def _v5(**kw):
    base = dict(potable_savings_pct=37.5, annual_pluvial_consumed_m3=82.0, annual_potable_consumed_m3=137.0, net_co2e_saved_kg_lifetime=200.0, has_irrigation_demand=False, indoor_savings_pct=37.5)
    base.update(kw)
    return calculate_esg_certifications(**base).leed_v5


def test_leed_v5_soma_as_opcoes_2_a_6():
    """37,5% interno dá 2 pontos na Opção 2, e o sistema pluvial 2 na Opção 6."""
    r = _v5()
    assert r.opcao2_pts == 2
    assert r.opcao6_pts == 2
    assert r.opcao4_pts == 0
    assert r.total_pts == 4
    assert r.caminho == 'Opções 2 a 6'


@pytest.mark.parametrize('pct, pontos', [(29.9, 0), (30.0, 1), (35.0, 2), (40.0, 3), (60.0, 3)])
def test_leed_v5_opcao_2_faixas(pct, pontos):
    assert _v5(indoor_savings_pct=pct, potable_savings_pct=pct).opcao2_pts == pontos


@pytest.mark.parametrize('pct, pontos', [(30.0, 2), (45.0, 5), (65.0, 8), (80.0, 8)])
def test_leed_v5_opcao_1_com_fonte_alternativa(pct, pontos):
    """Tabela 1 do WEc2: 30% vale 1 ponto, e a fonte alternativa acrescenta 1, até 8."""
    assert _v5(potable_savings_pct=pct, indoor_savings_pct=pct).opcao1_pts == pontos


def test_leed_v5_sem_sistema_nao_pontua_a_opcao_6():
    r = _v5(annual_pluvial_consumed_m3=0.0, potable_savings_pct=0.0, indoor_savings_pct=0.0)
    assert r.opcao6_pts == 0
    assert r.total_pts == 0


# ==================================================================================================
# Arquivo, linha de comando e paridade com a interface
# ==================================================================================================

# ---- origem: tests/integration/test_paridade_interface_cli.py
_ARQUIVO_PARIDADE_INTERFACE_CLI = str(_TESTES / 'integration/test_paridade_interface_cli.py')

PARIDADE_INTERFACE_CLI_RAIZ = Path(_ARQUIVO_PARIDADE_INTERFACE_CLI).resolve().parents[2]


def _caso_do_manual(raiz, *nomes):
    """O primeiro caso do manual que existe nesta edição (cada edição tem os seus casos e nomes)."""
    pasta = Path(raiz) / 'manual' / 'casos'
    for nome in nomes:
        if (pasta / nome).exists():
            return pasta / nome
    return pasta / nomes[0]


_VARREDURA = ('02_tutorial_varredura.triton', '04_tutorial_sweep.triton', '04_tutorial_varredura.triton')
_ESCOLA = ('08_escola_semanal.triton', '07_school_weekly.triton', '07_escola_semanal.triton')

PROJETOS = sorted((PARIDADE_INTERFACE_CLI_RAIZ / 'manual' / 'casos').glob('*.triton')) + sorted((PARIDADE_INTERFACE_CLI_RAIZ / 'examples').glob('estudo_caso_*.triton')) + [PARIDADE_INTERFACE_CLI_RAIZ / 'examples' / 'exemplo_quatro_criterios.triton']


@pytest.fixture(scope='module', autouse=True)
def _sem_dialogos():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ('information', 'warning', 'critical'):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, 'question', staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    QApplication.instance() or QApplication(sys.argv)
    yield mp
    mp.undo()


def _abrir(caminho):
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(caminho))
    return w


def _rodar_janela(w):
    sim = w.tab_tanks_simulation
    sim.verified_dialogs = {'capex', 'motobomba', 'opex', 'tariffs'}
    sim.run_simulation(force=True)
    w.tab_economic.calculate_economics(force=True)
    w.tab_environmental.recalculate_and_update()
    g = w.tab_global_optimizer
    g.recalculate_all()
    t, smaa = (g.last_topsis_result, g.last_smaa_vikor_result)
    linhas = {round(x['vol']): x for x in g.last_scenario_results}
    varredura = sim.last_sweep_result.results_by_volume
    pares = varredura.items() if isinstance(varredura, dict) else [(r.lower_tank_vol, r) for r in varredura]
    return {'unico': sim.last_single_result.potential_potable_savings_pct, 'potencial': {round(v): r.potential_potable_savings_pct for v, r in pares}, 'vpl': {v: x['vpl'] for v, x in linhas.items()}, 'carbono': {v: x['lifecycle_co2'] for v, x in linhas.items()}, 'otimos': (t.candidates[t.technical_best_index].lower_tank_vol, t.candidates[t.financial_best_index].lower_tank_vol, t.candidates[t.environmental_best_index].lower_tank_vol, t.best_candidate.lower_tank_vol, smaa.best_candidate.lower_tank_vol), 'topsis': float(t.scores[t.best_index])}


def _rodar_cli(caminho, varredura=True):
    """Com ``varredura``, um projeto de volume fixo é varrido como a interface faz
    ao lado do volume fixo; sem ela, só o volume declarado é avaliado."""
    b = cli._load_bundle(str(caminho))
    if varredura:
        b['config'].lower_tank_mode = 1
    an = b.get('analysis') or {}
    o = cli.run_analysis(b['config'], cli._get_precipitation(b), 'all', environmental=an.get('environmental'))
    t = o['topsis']
    return {'potencial': {round(a['lower_tank_volume_l']): a['potable_savings_pct'] for a in o['technical']['alternatives']}, 'vpl': {round(a['lower_tank_volume_l']): a['npv_brl'] for a in o['economic']['alternatives']}, 'carbono': {round(a['lower_tank_volume_l']): -a['lifetime_net_co2_saved_kg'] for a in o['environmental']['alternatives']}, 'otimos': (t['technical_best_volume_l'], t['economic_best_volume_l'], t['environmental_best_volume_l'], t['best_volume_l'], o['smaa_vikor']['best_volume_l']), 'topsis': t['best_score']}


def _comparar(j, c, nome):
    comuns = sorted(set(j['potencial']) & set(c['potencial']))
    assert len(comuns) >= 3, f'{nome}: varreduras sem volumes em comum'
    for v in comuns:
        assert j['potencial'][v] == pytest.approx(c['potencial'][v], abs=0.01), f'{nome} {v} L: potencial'
        if v > 0 and v in j['vpl'] and (v in c['vpl']):
            assert j['vpl'][v] == pytest.approx(c['vpl'][v], rel=0.001, abs=1.0), f'{nome} {v} L: VPL'
            assert j['carbono'][v] == pytest.approx(c['carbono'][v], rel=0.001, abs=0.5), f'{nome} {v} L: carbono'
    rotulos = ('técnico', 'econômico', 'ambiental', 'TOPSIS', 'SMAA-VIKOR')
    for r, a, b in zip(rotulos, j['otimos'], c['otimos']):
        assert a == b, f'{nome}: ótimo {r} {a} L na interface e {b} L na linha de comando'
    assert j['topsis'] == pytest.approx(c['topsis'], abs=0.001), f'{nome}: escore TOPSIS'


@pytest.mark.parametrize('caminho', PROJETOS, ids=lambda p: p.stem)
def test_projeto_distribuido(caminho):
    w = _abrir(caminho)
    try:
        janela = _rodar_janela(w)
    finally:
        w.close()
    _comparar(janela, _rodar_cli(caminho), caminho.stem)
    if w.config.lower_tank_mode == 0:
        so_ele = _rodar_cli(caminho, varredura=False)['potencial']
        assert len(so_ele) == 1
        assert janela['unico'] == pytest.approx(next(iter(so_ele.values())), abs=0.01), f'{caminho.stem}: potencial do volume fixo'


def test_alteracao_feita_na_tela_e_gravada(tmp_path, _sem_dialogos):
    """Fração interna e demanda externa digitadas na tela chegam iguais à linha de comando."""
    w = _abrir(_caso_do_manual(PARIDADE_INTERFACE_CLI_RAIZ, *_VARREDURA))
    try:
        tb = w.tab_building
        tb.txt_non_potable_indoor_share_simple.setText('30')
        tb.txt_external_demand_l_day.setText('120')
        destino = tmp_path / 'alterado.triton'
        _sem_dialogos.setattr(QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: (str(destino), '')))
        w.on_save_simulation()
        janela = _rodar_janela(w)
    finally:
        w.close()
    _comparar(janela, _rodar_cli(destino), 'alterado na tela')


def test_modo_diario(tmp_path):
    """Demanda diária: a série do arquivo manda nos dois caminhos."""
    d = json.loads((_caso_do_manual(PARIDADE_INTERFACE_CLI_RAIZ, *_VARREDURA)).read_text(encoding='utf-8'))
    n = len(d['rainfall']['precipitation_mm']) if 'precipitation_mm' in d.get('rainfall', {}) else 3650
    mod = d['inputs'].setdefault('demand_modulation', {})
    mod.update(demand_mode='daily', daily_demands=[150.0 if i % 7 < 5 else 190.0 for i in range(n)], daily_residents=[4] * n, daily_shares=[0.28] * n)
    d['inputs']['incentives_and_shares']['demand_mode'] = 'daily'
    p = tmp_path / 'diario.triton'
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    w = _abrir(p)
    try:
        _comparar(_rodar_janela(w), _rodar_cli(p), 'modo diário')
    finally:
        w.close()


# ---- origem: tests/integration/test_propagacao_de_entradas.py

def _simulacao(pluvial_l_dia: float=330.0, potavel_l_dia: float=330.0):
    """Resultado de simulação com recalque real.

    `total_pumped_liters` em zero não é neutro: sem volume recalcado a altura
    manométrica não tem o que encarecer, e a energia dá zero em qualquer
    desnível.
    """
    r = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=pluvial_l_dia, avg_potable_consumed_l_day=potavel_l_dia, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    r.n_days_simulated = 365
    r.total_pumped_liters = pluvial_l_dia * 365.0
    r.total_pump_cycles = 365
    return r


@pytest.fixture
def propagacao_de_entradas_janela(qapp):
    from triton.ui.main_window import MainWindow
    win = MainWindow()
    # Estes testes verificam que a escolha da tela move o investimento pelo catálogo de preços do
    # motor. Fora da Brasil o projeto novo parte com o catálogo desligado (neutralidade); aqui
    # ele é ligado de propósito.
    win.config.precos_de_catalogo = True
    win.tab_tanks_simulation.last_single_result = _simulacao()
    win.tab_tanks_simulation._is_technical_only = False
    return win


def _econ(cfg, sim=None):
    return run_economic_analysis(cfg, sim or _simulacao())


def _propagacao_de_entradas_acv(**kwargs):
    base = dict(annual_water_saved_m3=120.0, annual_pump_kwh=150.0)
    base.update(kwargs)
    return calculate_lca(5000.0, base['annual_water_saved_m3'], EnvironmentalConfig(**base))


def test_a_serie_de_chuva_chega_a_aba_de_qualidade(propagacao_de_entradas_janela):
    """A precipitação estava fixa em 1.500 mm no cálculo de wash-off."""
    aba = propagacao_de_entradas_janela.tab_water_quality
    propagacao_de_entradas_janela.tab_tanks_simulation.precip_data = [2.0] * 365
    seca = aba._precipitacao_anual_mm()
    propagacao_de_entradas_janela.tab_tanks_simulation.precip_data = [8.0] * 365
    umida = aba._precipitacao_anual_mm()
    assert umida > 3 * seca


def test_a_area_de_captacao_dimensiona_o_filtro_de_entrada(propagacao_de_entradas_janela):
    """Telhado maior pede filtro maior, e o preço acompanha."""
    from triton.core.etap_integration import capex_incremental_da_etap
    propagacao_de_entradas_janela.config.area = 100.0
    pequeno = capex_incremental_da_etap(propagacao_de_entradas_janela.config)
    propagacao_de_entradas_janela.config.area = 400.0
    grande = capex_incremental_da_etap(propagacao_de_entradas_janela.config)
    assert grande > pequeno


def test_a_tipologia_chega_a_configuracao_e_ao_aviso(propagacao_de_entradas_janela):
    """Ficava presa num dicionário local da aba de edificação."""
    from triton.core.edition import usa_dados_do_brasil
    from triton.core.tariff_category import incompatibilidade_de_categoria
    aba = propagacao_de_entradas_janela.tab_building
    for tid, avisa in (('res_medio', False), ('hospital', True), ('comercial', True)):
        aba.combo_building_template.setCurrentIndex(aba.combo_building_template.findData(tid))
        aba.get_building_config()
        assert propagacao_de_entradas_janela.config.building_template_id == tid
        # O aviso fala do catálogo tarifário do Brasil: fora dele não existe catálogo, e não há aviso.
        assert bool(incompatibilidade_de_categoria(propagacao_de_entradas_janela.config)) is (avisa and usa_dados_do_brasil()), tid


def test_o_volume_pluvial_simulado_rege_o_dimensionamento_da_etap(propagacao_de_entradas_janela):
    """A aba pedia o volume a um atributo que não existe em TritonConfig."""
    from triton.core.etap_integration import volume_pluvial_anual_m3
    propagacao_de_entradas_janela.tab_tanks_simulation.last_single_result = _simulacao(1000.0)
    volume = volume_pluvial_anual_m3(propagacao_de_entradas_janela.config, propagacao_de_entradas_janela.tab_water_quality._simulacao_corrente())
    assert volume == pytest.approx(365.25, rel=1e-06)
    assert volume != 120.0


@pytest.mark.parametrize('metodo', ['uv', 'ozonio'])
def test_a_desinfeccao_escolhida_encarece_e_emite(propagacao_de_entradas_janela, metodo):
    aba = propagacao_de_entradas_janela.tab_water_quality
    aba.combo_disinf.setCurrentIndex(aba.combo_disinf.findData('cloro'))
    aba.on_disinfection_changed()
    base_econ = _econ(propagacao_de_entradas_janela.config)
    base_acv = _propagacao_de_entradas_acv(water_quality_disinfection='cloro')
    aba.combo_disinf.setCurrentIndex(aba.combo_disinf.findData(metodo))
    aba.on_disinfection_changed()
    assert _econ(propagacao_de_entradas_janela.config).capex_total > base_econ.capex_total
    assert _propagacao_de_entradas_acv(water_quality_disinfection=metodo).annual_treatment_co2_kg > base_acv.annual_treatment_co2_kg


def test_o_filtro_de_polimento_move_investimento_e_manutencao(propagacao_de_entradas_janela):
    aba = propagacao_de_entradas_janela.tab_water_quality
    aba.combo_class.setCurrentIndex(aba.combo_class.findData('classe_4'))
    aba.on_class_changed()
    aba.chk_polishing.setChecked(False)
    aba.on_polishing_changed()
    sem = _econ(propagacao_de_entradas_janela.config)
    aba.chk_polishing.setChecked(True)
    aba.on_polishing_changed()
    com = _econ(propagacao_de_entradas_janela.config)
    assert com.capex_total > sem.capex_total
    assert com.annual_etap_opex_brl > sem.annual_etap_opex_brl


def test_a_dose_de_cloro_digitada_rege_a_massa_anual(propagacao_de_entradas_janela):
    aba = propagacao_de_entradas_janela.tab_water_quality
    aba.txt_cl_dose.setText('3,0')
    aba.recalculate_all()
    dobro = _econ(propagacao_de_entradas_janela.config).annual_chlorine_kg
    aba.txt_cl_dose.setText('1,5')
    aba.recalculate_all()
    metade = _econ(propagacao_de_entradas_janela.config).annual_chlorine_kg
    assert dobro == pytest.approx(2 * metade, rel=1e-06)


def test_a_altura_manometrica_do_assistente_rege_a_emissao_de_bombeamento(propagacao_de_entradas_janela):
    """O assistente calculava a altura e a descartava no retorno."""
    from triton.core.pump_energy import compute_annual_pump_energy
    from triton.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    consumos = []
    for altura in (4.0, 30.0):
        assistente = PumpSelectionWizardDialog(upper_tank_vol=500.0)
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data
        cfg = propagacao_de_entradas_janela.config
        cfg.pump_power_kw = dados['kw']
        cfg.pump_flow_rate = dados['flow_lh']
        cfg.pump_efficiency = float(dados['efficiency'])
        cfg.pump_manometric_head_m = float(dados['manometric_head_m'])
        consumos.append(compute_annual_pump_energy(cfg, _simulacao(), upper_tank_used=True).annual_kwh)
    assert consumos[1] > 3 * consumos[0], consumos


def test_o_investimento_informado_muda_o_retorno(propagacao_de_entradas_janela):
    cfg = propagacao_de_entradas_janela.config
    cfg.cost_lower_tank = 2000.0
    barato = _econ(cfg)
    cfg.cost_lower_tank = 12000.0
    caro = _econ(cfg)
    assert caro.capex_total > barato.capex_total
    assert caro.vpl < barato.vpl


def test_a_estrutura_tarifaria_rege_a_economia_de_agua(propagacao_de_entradas_janela):
    """Franquia e disponibilidade diferem só pela tarifa da primeira faixa."""
    cfg = propagacao_de_entradas_janela.config
    cfg.water_tariffs = [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]]
    com_franquia = _econ(cfg).annual_water_savings_brl
    cfg.water_tariffs = [[0.0, 0.0, 40.0, -1], [0.0, 999999.0, 5.0, 1]]
    com_disponibilidade = _econ(cfg).annual_water_savings_brl
    assert com_disponibilidade > com_franquia


def test_o_percentual_de_esgoto_rege_a_economia_total(propagacao_de_entradas_janela):
    cfg = propagacao_de_entradas_janela.config
    cfg.water_tariffs = [[0.0, 999999.0, 5.0, 1]]
    cfg.sewage_mode = 1
    cfg.sewage_rate = 0.0
    sem = _econ(cfg).annual_water_savings_brl
    cfg.sewage_rate = 100.0
    com = _econ(cfg).annual_water_savings_brl
    # O esgoto a 100 % dobra a poupança da água; um imposto variável sobre a água (o IVA dos
    # tarifários de Portugal) incide só na parcela da água e entra na razão: (2 + t) / (1 + t).
    t = float(getattr(cfg, 'water_tax_var', 0.0) or 0.0) / 100.0
    assert com == pytest.approx((2 + t) / (1 + t) * sem, rel=1e-06)


def test_a_rota_de_agua_rege_a_emissao_evitada():
    from triton.core import water_supply_routes as rotas
    from triton.core.edition import usa_dados_do_brasil
    # A rota de rede mais limpa do catálogo: a macrorregião Sudeste (SNIS) é do Brasil; fora dele,
    # a rede convencional do catálogo geral.
    rota_limpa = 'vaz_2025_sudeste' if usa_dados_do_brasil() else 'convencional_br'
    baixa = _propagacao_de_entradas_acv(potable_water_co2_kg_m3=rotas.co2_evitado_por_m3(rota_limpa))
    alta = _propagacao_de_entradas_acv(potable_water_co2_kg_m3=rotas.co2_evitado_por_m3('dessalinizacao_termica'))
    assert alta.annual_avoided_co2_kg > 20 * baixa.annual_avoided_co2_kg
    assert alta.environmental_payback_years < baixa.environmental_payback_years


def test_o_fator_da_rede_rege_a_emissao_de_bombeamento():
    limpa = _propagacao_de_entradas_acv(grid_co2_factor_kg_kwh=0.085)
    suja = _propagacao_de_entradas_acv(grid_co2_factor_kg_kwh=0.7)
    assert suja.annual_pumping_co2_kg > 7 * limpa.annual_pumping_co2_kg


def test_o_material_do_reservatorio_rege_o_carbono_incorporado():
    pead = _propagacao_de_entradas_acv(lower_material_key='PEAD')
    concreto = _propagacao_de_entradas_acv(lower_material_key='CONCRETO')
    assert concreto.total_embodied_co2_kg != pead.total_embodied_co2_kg


def test_dobrar_o_aproveitamento_move_todos_os_modulos(propagacao_de_entradas_janela):
    """A verificação de fecho: um sistema que aproveita o dobro tem de aparecer
    diferente em todos os módulos de saída, e nos sentidos certos."""
    from triton.core.edition import usa_dados_do_brasil
    brasil = usa_dados_do_brasil()
    if not brasil:
        # Fora da Brasil o projeto novo parte sem tarifa nem fator de emissão da água (o usuário os
        # informa); aqui entram valores de ensaio, para o dobro do aproveitamento aparecer nos módulos.
        propagacao_de_entradas_janela.config.water_tariffs = [[0.0, 999999.0, 5.0, 1]]
    pouco, muito = (_simulacao(200.0), _simulacao(600.0))
    e_pouco, e_muito = (_econ(propagacao_de_entradas_janela.config, pouco), _econ(propagacao_de_entradas_janela.config, muito))
    assert e_muito.annual_water_savings_brl > e_pouco.annual_water_savings_brl
    assert e_muito.vpl > e_pouco.vpl
    fator_da_agua = {} if brasil else {'potable_water_co2_kg_m3': 0.35}
    a_pouco = _propagacao_de_entradas_acv(annual_water_saved_m3=pouco.annual_pluvial_consumed_m3, **fator_da_agua)
    a_muito = _propagacao_de_entradas_acv(annual_water_saved_m3=muito.annual_pluvial_consumed_m3, **fator_da_agua)
    assert a_muito.annual_avoided_co2_kg > a_pouco.annual_avoided_co2_kg
    assert a_muito.environmental_payback_years < a_pouco.environmental_payback_years


def test_nenhum_modulo_devolve_valor_nao_finito(propagacao_de_entradas_janela):
    """Um NaN atravessa o programa inteiro sem erro e contamina o relatório."""
    import math
    econ = _econ(propagacao_de_entradas_janela.config)
    for campo in ('vpl', 'capex_total', 'annual_water_savings_brl', 'annual_opex_brl', 'etap_capex_brl', 'annual_etap_opex_brl'):
        valor = getattr(econ, campo)
        assert math.isfinite(valor), campo
    acv = _propagacao_de_entradas_acv()
    for campo in ('total_embodied_co2_kg', 'annual_pumping_co2_kg', 'annual_treatment_co2_kg', 'annual_avoided_co2_kg', 'lifetime_net_co2_saved_kg', 'environmental_payback_years', 'specific_co2_avoided_g_per_liter'):
        valor = getattr(acv, campo)
        assert math.isfinite(valor), campo


def _sim_cli():
    from triton.core.simulation import SingleTankSimulationResult
    r = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    r.n_days_simulated = 365
    r.total_pumped_liters = 330.0 * 365
    r.total_pump_cycles = 365
    return r


def test_a_linha_de_comando_honra_a_escolha_de_desinfeccao():
    """O econômico honrava e a ACV não, na MESMA rodada.

    `run_economic_analysis` recebe o `TritonConfig` inteiro, de modo que a linha
    de comando já cobrava o ozonizador no fluxo de caixa. A ACV montava a própria
    configuração sem os campos de qualidade da água e caía nos padrões, emitindo
    como se fosse só cloração. O relatório saía internamente contraditório.
    """
    from triton.cli import _environmental_config
    from triton.core.parser import TritonConfig
    sim = _sim_cli()
    emissoes = {}
    for metodo in ('cloro', 'uv', 'ozonio'):
        cfg = TritonConfig()
        cfg.water_quality_disinfection = metodo
        ambiental = _environmental_config(cfg, sim, 150.0, {})
        assert ambiental.water_quality_disinfection == metodo
        emissoes[metodo] = calculate_lca(ambiental).annual_treatment_co2_kg
    assert emissoes['uv'] > 5 * emissoes['cloro']
    assert emissoes['ozonio'] > emissoes['uv']


def test_a_linha_de_comando_usa_o_consumo_especifico_corrigido():
    """Estava congelado em 0,40 kWh/m³, o valor anterior à correção da hidráulica.

    Aquele número dividia pelo rendimento duas vezes e implicava 67 m de altura
    manométrica. A mesma configuração dava emissão de bombeamento diferente na
    tela e no terminal, com fator de 3,7.

    Agora o valor sai da mesma função que a aba ambiental da interface usa,
    ``compute_annual_pump_energy``, calculada sobre a simulação do volume.
    """
    from triton.cli import _environmental_config
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg, sim = (TritonConfig(), _sim_cli())
    ambiental = _environmental_config(cfg, sim, 150.0, {})
    esperado = compute_annual_pump_energy(cfg, sim, upper_tank_used=bool(cfg.upper_tank_used))
    assert ambiental.pump.specific_kwh_per_m3 == pytest.approx(esperado.specific_kwh_per_m3)
    assert ambiental.pump.specific_kwh_per_m3 < 0.2


def test_a_sobreposicao_legada_vale_so_para_quem_a_declara():
    """Ela tem precedência sobre a linha de tratamento, e portanto a desliga.

    Aplicá-la a todo projeto que não declarasse cloro — a maioria — fazia a
    escolha de desinfecção não surtir efeito ambiental nenhum na linha de comando.
    Projetos que a declaram continuam reproduzindo o resultado histórico.
    """
    from triton.cli import _environmental_config
    from triton.core.parser import TritonConfig
    sim = _sim_cli()
    sem_declaracao = _environmental_config(TritonConfig(), sim, 150.0, {})
    assert sem_declaracao.chemical_treatment_co2_m3 is None
    legado = _environmental_config(TritonConfig(), sim, 150.0, {'chemical_treatment_co2_m3': 0.02})
    assert legado.chemical_treatment_co2_m3 == pytest.approx(0.02)
    cfg = TritonConfig()
    cfg.water_quality_disinfection = 'ozonio'
    com_ozonio = _environmental_config(cfg, sim, 150.0, {'chemical_treatment_co2_m3': 0.02})
    assert calculate_lca(com_ozonio).annual_treatment_co2_kg == pytest.approx(calculate_lca(legado).annual_treatment_co2_kg)


# ---- origem: tests/integration/test_fluidez_de_informacoes.py

@pytest.fixture(scope='module')
def fluidez_de_informacoes_app():
    inst = QApplication.instance()
    if inst is None:
        inst = QApplication(sys.argv)
    yield inst


@pytest.fixture
def fluidez_de_informacoes_janela(fluidez_de_informacoes_app):
    return MainWindow()


def test_recalcular_a_qualidade_nao_apaga_a_escolha_do_usuario(fluidez_de_informacoes_janela):
    """Recalcular reescreve campos, e um `recalculate` distraído já apagou escolha
    antes. O teste guarda a idempotência."""
    aba = fluidez_de_informacoes_janela.tab_water_quality
    idx = aba.combo_disinf.findData('ozonio')
    aba.combo_disinf.setCurrentIndex(idx)
    aba.on_disinfection_changed()
    aba.chk_polishing.setChecked(True)
    aba.on_polishing_changed()
    aba.txt_cl_dose.setText('2,5')
    for _ in range(3):
        aba.recalculate_all()
    assert fluidez_de_informacoes_janela.config.water_quality_disinfection == 'ozonio'
    assert fluidez_de_informacoes_janela.config.water_quality_polishing is True
    assert fluidez_de_informacoes_janela.config.chlorine_dose_mg_l == pytest.approx(2.5)


# ---- origem: tests/integration/test_report_omitted_values.py

PROJETO = {'ref_code': 'NET-OMIT-001', 'rain_file': 'ClimaFpolis.csv', 'area': 250.0, 'runoff': 0.85, 'discard': 2.0, 'residents': 5, 'demand': 150.0, 'share': 0.4, 'lower_vol': 5000.0, 'potential_pct': 35.5, 'pluv_day': 120.0, 'potable_day': 180.0, 'spill_day': 40.0, 'sat_full': 62.0, 'sat_null': 13.7, 'capex': 9500.0, 'annual_gross': 3200.0, 'vpl': 28500.0, 'tir': 26.5, 'payback_s': '4,1', 'payback_d': '5,5', 'annual_pluvial_m3': 120.0}


def test_o_laudo_executivo_traz_a_confiabilidade(qapp):
    """Dizer que 62% dos dias tiveram atendimento integral não diz o resto.

    O percentual de dias em que a demanda pluvial não foi atendida é o indicador
    de confiabilidade que o leitor procura, e era calculado e descartado.
    """
    html = generate_executive_html_report(PROJETO)
    assert '13,7' in html
    assert 'Atendimento Nulo' in html


def _report_omitted_values_acv(metodo: str):
    cfg = EnvironmentalConfig(annual_water_saved_m3=120.0, water_quality_disinfection=metodo)
    return calculate_lca(5000.0, 120.0, cfg)


def test_o_laudo_ambiental_traz_a_dose_de_cloro(qapp):
    """A tabela mostrava a massa anual sem a dose que a origina.

    Sem a dose não há como conferir a conta, que é a razão de a tabela existir.
    """
    lca = _report_omitted_values_acv('cloro')
    html = generate_environmental_html_report(PROJETO, lca_result=lca)
    assert 'mg Cl2/L' in html
    assert 'produto/ano' in html


def test_o_laudo_ambiental_nomeia_os_estagios_de_desinfeccao(qapp):
    uv = generate_environmental_html_report(PROJETO, lca_result=_report_omitted_values_acv('uv'))
    assert 'ultravioleta' in uv.lower()
    cloro = generate_environmental_html_report(PROJETO, lca_result=_report_omitted_values_acv('cloro'))
    assert 'ultravioleta' not in cloro.lower()


def test_a_emissao_por_litro_continua_no_cartao(qapp):
    """Estava listada como omitida e não estava: aparece sob o payback ambiental.

    O teste a fixa para que a correção das outras duas não a derrube.
    """
    html = generate_environmental_html_report(PROJETO, lca_result=_report_omitted_values_acv('cloro'))
    assert 'g CO2e/L' in html


# ---- origem: tests/unit/test_export_tab_and_exporters.py

def test_safe_float_robustness():
    """Garante que a função auxiliar _safe_float nunca lance exceções com entradas corrompidas ou strings."""
    assert _safe_float(None, 10.0) == 10.0
    assert _safe_float('', 5.0) == 5.0
    assert _safe_float('-', 2.0) == 2.0
    assert _safe_float('   -   ', 3.0) == 3.0
    assert _safe_float('invalid', 0.0) == 0.0
    assert _safe_float('12,5', 0.0) == 12.5
    assert _safe_float('12.5', 0.0) == 12.5
    assert _safe_float(42, 0.0) == 42.0


def test_cad_robustness_with_unsimulated_project():
    """
    Testa resiliência contra entradas não numéricas como '-' (cenário exato que causou o bug no diálogo do usuário).
    """
    unsimulated_data = {'project_name': 'Projeto Novo Sem Simulação', 'ref_code': 'N5-EMPTY', 'area': '-', 'lower_vol': '-', 'runoff': '-', 'discard': '-', 'upper_vol': '-', 'potential_pct': '-', 'audit_context': {'climate_location': '-'}}
    svg = generate_project_svg_diagram(unsimulated_data)
    assert '<svg' in svg
    assert '</svg>' in svg
    assert 'PROJETO NOVO SEM SIMULAÇÃO' in svg
    with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tf:
        temp_dxf = tf.name
    try:
        out_dxf = generate_project_dxf(unsimulated_data, temp_dxf)
        assert os.path.exists(out_dxf)
        assert os.path.getsize(out_dxf) > 500
    finally:
        if os.path.exists(temp_dxf):
            os.remove(temp_dxf)


def test_cad_dxf_generation():
    """Valida se o arquivo DXF é gerado com sintaxe ASCII válida, tabelas de layers e entidades."""
    sample_data = {'project_name': 'Edifício Residencial Alpha', 'ref_code': 'N5-2026-TEST', 'area': 250.0, 'lower_vol': 7500.0, 'runoff': 0.85, 'discard': 2.0, 'upper_vol': 1000.0, 'potential_pct': 34.5, 'audit_context': {'climate_location': 'Florianópolis / SC'}}
    with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tf:
        temp_dxf = tf.name
    try:
        out_path = generate_project_dxf(sample_data, temp_dxf)
        assert os.path.exists(out_path)
        assert os.path.getsize(out_path) > 500
        with open(out_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'SECTION' in content
        assert 'TABLES' in content
        assert 'LAYER' in content
        assert '01_ALVENARIA_COBERTURA' in content
        assert '03_TUB_RECALQUE' in content
        assert '04_TUB_DISTRIBUICAO' in content
        assert '06_EQUIPAMENTOS' in content
        assert '08_COTAS' in content
        assert 'ENTITIES' in content
        assert 'LINE' in content
        assert 'TEXT' in content
        assert 'EOF' in content
    finally:
        if os.path.exists(temp_dxf):
            os.remove(temp_dxf)


# ---- origem: tests/integration/test_report_generator.py

def test_generate_research_html_report_without_optimizer_data():
    html = generate_research_html_report({'ref_code': 'NET-RESEARCH-FALLBACK', 'rain_file': 'serie.csv', 'area': 100.0, 'lower_vol': 2000.0, 'potential_pct': 25.0})
    assert 'NET-RESEARCH-FALLBACK' in html
    assert 'Execute a análise multicritério para preencher a comparação' in html
    assert 'Pesos detalhados não estavam disponíveis' in html
    assert 'Conclusões e Protocolo de Escolha' in html


# ---- origem: tests/unit/test_report_service.py

def test_invalid_report_type_is_rejected():
    with pytest.raises(ValueError):
        normalize_report_type('inventado')


# ==================================================================================================
# Modulação Probabilística
# ==================================================================================================

# ---- origem: tests/ui/test_modulacao_estocastica_ui.py
_ARQUIVO_MODULACAO_ESTOCASTICA_UI = str(_TESTES / 'ui/test_modulacao_estocastica_ui.py')

MODULACAO_ESTOCASTICA_UI_RAIZ = Path(_ARQUIVO_MODULACAO_ESTOCASTICA_UI).resolve().parents[2]


MODULACAO_ESTOCASTICA_UI_CASO = _caso_do_manual(MODULACAO_ESTOCASTICA_UI_RAIZ, *_VARREDURA)


@pytest.fixture(scope='module')
def modulacao_estocastica_ui_monkeypatch_module():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ('information', 'warning', 'critical'):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, 'question', staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    yield mp
    mp.undo()


@pytest.fixture(scope='module')
def modulacao_estocastica_ui_janela(modulacao_estocastica_ui_monkeypatch_module):
    app = QApplication.instance() or QApplication(sys.argv)
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(MODULACAO_ESTOCASTICA_UI_CASO))
    yield w
    w.close()
    app.processEvents()


def test_valores_de_triagem_centrados_no_projeto(modulacao_estocastica_ui_janela):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    cfg = modulacao_estocastica_ui_janela.config_do_estudo()
    assert t.cartoes['per_capita_l_dia'].distribuicao().media == pytest.approx(cfg.demand_value)
    assert t.cartoes['pessoas'].distribuicao().media == pytest.approx(cfg.residents_count)


def test_roda_e_da_o_mesmo_que_o_nucleo_com_o_estudo_da_tela(modulacao_estocastica_ui_janela):
    """Paridade: a tela usa o estudo que grava (config_do_estudo) e o mesmo núcleo da linha de comando."""
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    t.spin_n.setValue(3)
    t.spin_semente.setValue(9)
    t.simular(bloquear=True)
    assert t.resultado and t.resultado['realizacoes_feitas'] == 3
    estudo, falta = t._estudo()
    assert falta is None
    cfg, precip, pesos, ambiental = estudo
    nucleo = M.simular(cfg, precip, t.parametros(), amostras=3, semente=9, pesos=pesos, ambiental=ambiental)
    assert t.resultado['frequencia_pct'] == nucleo['frequencia_pct']
    assert t.tabela.rowCount() == len(nucleo['por_volume'])


def test_projeto_gravado_e_reaberto_mantem_as_distribuicoes(modulacao_estocastica_ui_janela, tmp_path, modulacao_estocastica_ui_monkeypatch_module):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.cartoes['per_capita_l_dia'].combo_tipo.setCurrentIndex(t.cartoes['per_capita_l_dia'].combo_tipo.findData('triangular'))
    t.spin_n.setValue(77)
    destino = tmp_path / 'salvo.triton'
    modulacao_estocastica_ui_monkeypatch_module.setattr(QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: (str(destino), '')))
    modulacao_estocastica_ui_janela.on_save_simulation()
    estado = load_triton_project(str(destino))['ui_state']['modulacao_estocastica']
    assert estado['amostras'] == 77
    assert estado['parametros']['variaveis']['per_capita_l_dia']['tipo'] == 'triangular'
    t.spin_n.setValue(5)
    t.apply_project_state(estado)
    assert t.spin_n.value() == 77
    assert t.cartoes['per_capita_l_dia'].distribuicao().tipo == 'triangular'


def test_marcar_variavel_mostra_o_cartao_e_entra_no_sorteio(modulacao_estocastica_ui_janela):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    assert not t.cartoes['fator_chuva'].isVisibleTo(t)
    t.checks['fator_chuva'].setChecked(True)
    assert t.cartoes['fator_chuva'].isVisibleTo(t)
    assert 'fator_chuva' in t.parametros().ativas()
    t.checks['fator_chuva'].setChecked(False)
    assert 'fator_chuva' not in t.parametros().ativas()


def test_modelos_climaticos_ficam_inativos_com_arquivo_proprio(modulacao_estocastica_ui_janela):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    assert len(t.checks_modelos) == 19
    assert not any((c.isEnabled() for c in t.checks_modelos.values()))
    assert t.parametros().modelos_climaticos == []
    from triton.core.edition import usa_dados_de_portugal
    # Na IBE a chuva do projeto é a E-OBS (uma só série por concelho), e não um arquivo próprio.
    assert ('E-OBS' if usa_dados_de_portugal() else 'arquivo próprio') in t.lbl_modelos.text()


def test_modelos_marcados_entram_no_sorteio_e_na_tabela_4(modulacao_estocastica_ui_janela, monkeypatch):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    monkeypatch.setattr(M, 'pode_sortear_modelos', lambda cfg: True)
    cfg = modulacao_estocastica_ui_janela.config_do_estudo()
    try:
        M.series_dos_modelos_climaticos(cfg, ['MIROC6'])
    except (FileNotFoundError, ValueError):
        pytest.skip('base CLIMBra ausente')
    t.restaurar_padroes()
    t.checks_modelos['INM-CM4'].setChecked(True)
    t.checks_modelos['MIROC6'].setChecked(True)
    assert t.parametros().modelos_climaticos == ['INM-CM4', 'MIROC6']
    assert t.get_project_state()['parametros']['modelos_climaticos'] == ['INM-CM4', 'MIROC6']
    t.spin_n.setValue(4)
    t.simular(bloquear=True)
    assert [m['modelo'] for m in t.resultado['por_modelo']] == ['INM-CM4', 'MIROC6']
    assert t.tabela_modelos.isVisibleTo(t) and t.tabela_modelos.rowCount() == 2
    t._marcar_modelos(False)
    assert t.parametros().modelos_climaticos == []


def test_poucas_realizacoes_avisam_do_vies_do_eta2(modulacao_estocastica_ui_janela):
    """Limite: com N pequeno, o η² por decis passa de 1 na soma; a legenda tem de dizer por quê."""
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    t.spin_n.setValue(12)
    t.simular(bloquear=True)
    legenda = t.leg_variancia.text()
    assert 'superestimado' in legenda and '12 realizações' in legenda
    assert legenda.startswith('Tabela ')  # a renumeração continua achando o número da tabela


def test_trocar_para_a_climbra_na_etapa_1_libera_os_modelos(modulacao_estocastica_ui_janela):
    """O estudo segue a fonte de chuva da tela, e não a da última gravação do projeto."""
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    tp = modulacao_estocastica_ui_janela.tab_project
    assert modulacao_estocastica_ui_janela.config_do_estudo().climate_source_mode == 'custom_file'
    try:
        tp.rb_source_national.setChecked(True)
        QApplication.processEvents()
        cfg = modulacao_estocastica_ui_janela.config_do_estudo()
        assert cfg.climate_source_mode == 'national_db'
        assert cfg.climate_model == tp.combo_climate_model.currentText().strip()
        assert cfg.climate_scenario == (tp.combo_climate_scenario.currentData() or 'HIST')
        t._descrever_modelos()
        assert all((c.isEnabled() for c in t.checks_modelos.values()))
        t.checks_modelos['MIROC6'].setChecked(True)
        assert t.parametros().modelos_climaticos == ['MIROC6']
    finally:
        t._marcar_modelos(False)
        tp.rb_source_custom.setChecked(True)
        QApplication.processEvents()
    assert modulacao_estocastica_ui_janela.config_do_estudo().climate_source_mode == 'custom_file'
    t._descrever_modelos()
    assert not any((c.isEnabled() for c in t.checks_modelos.values()))


def test_abrir_projeto_sem_modulacao_gravada_recentra_os_cartoes(modulacao_estocastica_ui_janela):
    """Os cartões partiam da tela vazia do início: a lognormal do per capita ficava com média 0."""
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    outro = _caso_do_manual(MODULACAO_ESTOCASTICA_UI_RAIZ, *_ESCOLA)
    modulacao_estocastica_ui_janela.on_load_simulation(str(outro))
    cfg = modulacao_estocastica_ui_janela.config_do_estudo()
    for chave in ('per_capita_l_dia', 'pessoas', 'fracao_nao_potavel_pct'):
        assert t.cartoes[chave].distribuicao().valor_central() == pytest.approx(M.valor_do_projeto(cfg, chave), rel=0.01)
    t.spin_n.setValue(3)
    t.simular(bloquear=True)
    assert t.resultado and t.resultado['realizacoes_feitas'] == 3
    assert t.lbl_um_volume.isVisibleTo(t)
    modulacao_estocastica_ui_janela.on_load_simulation(str(MODULACAO_ESTOCASTICA_UI_CASO))
    t.restaurar_padroes()


def test_cartao_nao_editado_acompanha_a_etapa_2_e_o_editado_fica(modulacao_estocastica_ui_janela, monkeypatch):
    t = modulacao_estocastica_ui_janela.tab_modulacao_estocastica
    t.restaurar_padroes()
    t.cartoes['pessoas'].campos['media'].setValue(7)
    original = modulacao_estocastica_ui_janela.config_do_estudo
    novo_per_capita = original().demand_value + 50.0

    def com_outro_per_capita(*a, **k):
        cfg = original(*a, **k)
        cfg.demand_value = novo_per_capita
        return cfg
    monkeypatch.setattr(modulacao_estocastica_ui_janela, 'config_do_estudo', com_outro_per_capita)
    t.recentrar()
    assert t.cartoes['per_capita_l_dia'].distribuicao().media == pytest.approx(novo_per_capita)
    assert t.cartoes['pessoas'].distribuicao().media == pytest.approx(7)
    monkeypatch.undo()
    t.restaurar_padroes()


# ==================================================================================================
# Fontes externas que falham: atualizador, detector de mudança e porta de validação
# ==================================================================================================

# ---- origem: tests/unit/test_tariffs_manager_tab.py

class TestTariffsMultiCategoryAndTab(unittest.TestCase):

    def test_categoria_sem_tabela_coletada_nao_e_estimada(self):
        """Antes da 0.1.0 a comercial era a residencial vezes 1,85, sem fonte.

        Uma categoria sem tabela oficial no registro do município não devolve nada:
        o programa não inventa a tarifa de uma categoria a partir de outra.
        """
        res = get_city_tariffs_by_category('SC', 'Florianópolis', category='residencial')
        self.assertIsNotNone(res)
        self.assertEqual(res['faixas'], get_city_data('SC', 'Florianópolis')['faixas'])
        for cat in ('comercial', 'industrial', 'publica', 'social'):
            if cat not in (get_city_data('SC', 'Florianópolis').get('categorias') or {}):
                self.assertIsNone(get_city_tariffs_by_category('SC', 'Florianópolis', category=cat))

    def test_categoria_coletada_usa_a_tabela_dela(self):
        from unittest import mock
        import triton.core.tariffs_database as tdb
        base = dict(get_city_data('SC', 'Florianópolis'))
        base['categorias'] = {'comercial': {'faixas': [[0.0, 999999.0, 6.81, 1]], 'tarifa_fixa_mensal': 46.34, 'fonte_url': 'resolução'}}
        with mock.patch.object(tdb, 'get_city_data', return_value=base):
            com = tdb.get_city_tariffs_by_category('SC', 'Florianópolis', 'comercial')
            self.assertEqual(com['faixas'], [[0.0, 999999.0, 6.81, 1]])
            self.assertEqual(com['categoria_tarifaria'], 'comercial')
            self.assertNotIn('categorias', com)
            self.assertEqual(tdb.categorias_coletadas(base), ['residencial', 'comercial'])


# ==================================================================================================
# Interface: edições, frações, telas que levam dado ao cálculo
# ==================================================================================================

# ---- origem: tests/ui/test_edicoes.py
_ARQUIVO_EDICOES = str(_TESTES / 'ui/test_edicoes.py')

@pytest.fixture
def internacional(monkeypatch):
    monkeypatch.setenv('TRITON_EDITION', 'INT')


@pytest.fixture
def brasil(monkeypatch):
    monkeypatch.setenv('TRITON_EDITION', 'BRL')


@pytest.fixture
def portugal(monkeypatch):
    monkeypatch.setenv('TRITON_EDITION', 'IBE')


def test_janela_da_portugal(qapp, portugal):
    """A Portugal parte do núcleo neutro, em português de Portugal e só em euros."""
    from triton.ui.main_window import MainWindow
    from triton.ui.translation import get_available_languages, tr
    janela = MainWindow()
    try:
        assert janela.sidebar.lbl_edicao.text() == 'Edição Ibérica (IBE)'
        assert not any('Tarif' in b.text() for b in janela.sidebar.btn_group.buttons())
        ts = janela.tab_tanks_simulation
        assert ts.get_currency_symbol() == '€'
        assert ts.combo_currency.count() == 1 and not ts.combo_currency.isEnabled()
        # Projeto novo: concelho padrão (Lisboa) com o tarifário transcrito; sem custos brasileiros.
        from triton.core import tarifarios_portugal as tp_
        lisboa = TritonConfig()
        tp_.aplicar('Lisboa', lisboa)
        assert janela.config.water_tariffs == lisboa.water_tariffs and janela.config.capex_do_arranjo is False
        from triton.core import base_climatica_portugal as pt
        # Sem a CLIMBra, que é brasileira; com a base E-OBS por concelho, quando instalada.
        assert janela.tab_project.rb_source_national.isVisibleTo(janela) == pt.disponivel()
        assert 'CLIMBra' not in janela.tab_project.rb_source_national.text() or not pt.disponivel()
        assert get_available_languages()['pt'] == 'Português (Portugal)'
        assert tr('VPL (R$)', 'pt') == 'VAL (R$)' and tr('Salvar arquivo', 'pt') == 'Guardar ficheiro'
    finally:
        janela.close()


def test_etapa_1_da_portugal_carrega_a_serie_do_concelho(qapp, portugal):
    """Distrito e concelho no lugar de UF e município; Lisboa, normal 1991–2020, por padrão."""
    from triton.core import base_climatica_portugal as pt
    if not pt.disponivel():
        pytest.skip('data/portugal_eobs.db ausente')
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        tp = janela.tab_project
        tp.rb_source_national.setChecked(True)
        assert 'Distrito' in tp.lbl_climate_uf.text() and 'Concelho' in tp.lbl_climate_city.text()
        assert tp.combo_climate_uf.findData('Faro') >= 0 and tp.combo_climate_uf.findData('Ilha da Madeira') < 0
        assert not tp.combo_climate_model.isEnabled() and tp.combo_climate_scenario.currentData() == 'EOBS'
        assert (tp.combo_climate_uf.currentData(), tp.combo_climate_city.currentText()) == ('Lisboa', 'Lisboa')
        tp.load_active_national_series()
        assert len(tp.precip_data) == 10958 and tp.precip_file_path.startswith('E-OBS v33.0e/')
        assert (tp.txt_start_date.text(), tp.txt_end_date.text()) == ('01/01/1991', '31/12/2020')
        tp.combo_climate_uf.setCurrentIndex(tp.combo_climate_uf.findData('Porto'))
        assert tp.combo_climate_city.findText('Lisboa') < 0 and tp.combo_climate_city.findText('Porto') >= 0
        estado = tp.get_project_state()
        assert estado['source_mode'] == 'national_db' and estado['climate_scenario'] == 'EOBS'
        # Lisboa tem tarifário transcrito: a etapa 1 o aplica e o quadro diz de onde veio.
        tp.combo_climate_uf.setCurrentIndex(tp.combo_climate_uf.findData('Lisboa'))
        tp.combo_climate_city.setCurrentIndex(tp.combo_climate_city.findText('Lisboa'))
        tp.load_active_national_series()
        cfg = janela.config
        assert cfg.sewage_mode == 3 and cfg.sewage_volume_factor == 0.9 and cfg.water_tax_var == 6.0
        assert tp.gb_tariffs.isVisibleTo(janela) and 'EPAL' in tp.lbl_t_prestador.text()
        assert not tp.lbl_t_elec.isVisibleTo(janela)  # sem a energia ANEEL da Brasil
        tp.combo_climate_city.setCurrentIndex(tp.combo_climate_city.findText('Sintra'))
        tp.load_active_national_series()
        assert 'sem tarifário' in tp.lbl_tariff_status.text()
    finally:
        janela.close()


def test_a_brasil_continua_em_portugues_do_brasil(qapp, brasil):
    from triton.ui.translation import get_available_languages, tr
    assert tr('VPL (R$)', 'pt') == 'VPL (R$)' and tr('Salvar arquivo', 'pt') == 'Salvar arquivo'
    assert get_available_languages()['pt'] == 'Português (Brasil)'


def test_o_rotulo_identifica_a_edicao(brasil, monkeypatch):
    assert rotulo_da_edicao() == 'Edição Brasil (BRL)'
    monkeypatch.setenv('TRITON_EDITION', 'INT')
    assert rotulo_da_edicao() == 'International Edition (INT)'
    assert rotulo_da_edicao(curto=True) == 'INT'


def test_projeto_novo_da_internacional_nao_traz_precos_brasileiros():
    cfg = TritonConfig()
    neutralizar_para_a_internacional(cfg)
    assert cfg.water_tariffs == [] and cfg.elec_tariff == 0 and (cfg.pump_unit_cost == 0)
    assert cfg.chlorine_cost_per_kg == 0 and cfg.iptu_green_enabled is False
    assert cfg.capex_do_arranjo is False and cfg.mao_de_obra_automatica is False
    assert cfg.op_costs and all((fixo == 0 and variavel == 0 for _, _, fixo, variavel in cfg.op_costs))


def test_janela_da_internacional(qapp, internacional):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        assert janela.sidebar.lbl_edicao.text() == 'International Edition (INT)'
        assert not any(('Tarif' in b.text() for b in janela.sidebar.btn_group.buttons()))
        ts = janela.tab_tanks_simulation
        assert ts.get_currency_symbol() == '¤'
        assert ts.combo_currency.isEnabled()
        assert [ts.combo_currency.itemData(i) for i in range(ts.combo_currency.count())] == ['XXX', 'USD', 'EUR', 'GBP', 'CNY', 'ZAR', 'INR', 'AUD', 'CAD', 'CHF']
        assert janela.config.water_tariffs == [] and janela.config.capex_do_arranjo is False
        ambiental = janela.tab_environmental
        assert ambiental.faltam_fatores_do_pais()
        assert ambiental.get_config().grid_co2_factor_kg_kwh == 0.0
        assert not ambiental.card_aqua.isVisibleTo(janela) and (not ambiental.card_casa_azul.isVisibleTo(janela))
        assert 'Casa Azul' not in ambiental._get_esg_methodology_html(False)
        assert 'AQUA' not in ambiental._get_esg_methodology_html(False)
        assert not janela.tab_project.rb_source_national.isVisibleTo(janela)
        ambiental.txt_grid_co2.setText('0.4')
        ambiental.txt_potable_co2.setText('0.3')
        assert not ambiental.faltam_fatores_do_pais()
    finally:
        janela.close()


def test_janela_da_brasil_continua_como_era(qapp, brasil):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        assert janela.sidebar.lbl_edicao.text() == 'Edição Brasil (BRL)'
        assert any(('Tarif' in b.text() for b in janela.sidebar.btn_group.buttons()))
        assert janela.tab_tanks_simulation.get_currency_symbol() == 'R$'
        assert janela.config.water_tariffs and janela.config.capex_do_arranjo is True
        ambiental = janela.tab_environmental
        assert not ambiental.faltam_fatores_do_pais()
        assert ambiental.get_config().grid_co2_factor_kg_kwh > 0
        assert 'Casa Azul' in ambiental._get_esg_methodology_html(False)
    finally:
        janela.close()


def test_relatorios_e_prancha_trazem_a_edicao(internacional):
    from triton.core.schematic_3d import generate_schematic_3d_svg
    from triton.core.study_layout import generate_study_layout
    dados = dict(generate_study_layout({}), project_name='t')
    assert 'International Edition (INT)' in generate_schematic_3d_svg(dados)


def test_instalador_por_edicao():
    from pathlib import Path
    iss = (Path(_ARQUIVO_EDICOES).resolve().parents[2] / 'setup_script.iss').read_text(encoding='utf-8')
    assert '#if Edition == "INT"' in iss and '#elif Edition == "IBE"' in iss
    assert iss.count('#define AppGuid') == 3  # BRL, INT e POR instalam-se lado a lado
    guids = [l.split('"')[1] for l in iss.splitlines() if l.strip().startswith('#define AppGuid')]
    assert len(set(guids)) == 3
    assert 'Source: "{#DistDir}\\*"' in iss


def test_moeda_gravada_pelo_codigo_e_lida_tambem_pelo_indice_antigo(qapp, internacional):
    """O projeto grava o código da moeda; o índice dos arquivos antigos continua lido."""
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        ts = janela.tab_tanks_simulation
        ts.apply_project_state({'currency': 1})
        assert ts.get_currency_symbol() == '$'
        ts.apply_project_state({'currency_code': 'GBP'})
        assert ts.get_currency_symbol() == '£'
        estado = ts.get_project_state()
        assert estado['currency_code'] == 'GBP' and estado['currency'] == 3
    finally:
        janela.close()


def test_brasil_mostra_so_o_real(qapp, brasil):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        ts = janela.tab_tanks_simulation
        assert ts.combo_currency.count() == 1 and (not ts.combo_currency.isEnabled())
        ts.apply_project_state({'currency_code': 'USD'})
        assert ts.get_currency_symbol() == 'R$'
    finally:
        janela.close()


def test_modulacao_da_internacional_fala_em_euro(qapp, internacional):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        t = janela.tab_modulacao_estocastica
        t.atualizar_moeda()
        # Sem escolha prévia, inicia com o sinal genérico de moeda (¤)
        assert '¤/kWh' in t.checks['tarifa_energia'].text()
        assert 'R$' not in t.cartoes['tarifa_energia'].title()
        cabecalhos = [t.tabela.horizontalHeaderItem(j).text() for j in range(t.tabela.columnCount())]
        assert any(('(¤)' in c for c in cabecalhos)) and (not any(('R$' in c for c in cabecalhos)))
        assert not t.caixa_modelos.isVisibleTo(janela)
        # Ao selecionar o Euro na simulação, passa a falar em euro
        ts = janela.tab_tanks_simulation
        ts.combo_currency.setCurrentIndex(ts.combo_currency.findData('EUR'))
        t.atualizar_moeda()
        assert '€/kWh' in t.checks['tarifa_energia'].text()
        cabecalhos_eur = [t.tabela.horizontalHeaderItem(j).text() for j in range(t.tabela.columnCount())]
        assert any(('(€)' in c for c in cabecalhos_eur))
    finally:
        janela.close()


# ---- origem: tests/ui/test_fracoes_na_interface.py
_ARQUIVO_FRACOES_NA_INTERFACE = str(_TESTES / 'ui/test_fracoes_na_interface.py')

FRACOES_NA_INTERFACE_RAIZ = Path(_ARQUIVO_FRACOES_NA_INTERFACE).resolve().parents[2]


FRACOES_NA_INTERFACE_CASO = _caso_do_manual(FRACOES_NA_INTERFACE_RAIZ, *_VARREDURA)


@pytest.fixture(scope='module')
def fracoes_na_interface_janela(fracoes_na_interface_monkeypatch_module):
    app = QApplication.instance() or QApplication(sys.argv)
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(FRACOES_NA_INTERFACE_CASO))
    yield w
    w.close()
    app.processEvents()


@pytest.fixture(scope='module')
def fracoes_na_interface_monkeypatch_module():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ('information', 'warning', 'critical'):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, 'question', staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    yield mp
    mp.undo()


def test_tela_mostra_as_fracoes_do_arquivo(fracoes_na_interface_janela):
    tb = fracoes_na_interface_janela.tab_building
    assert tb.txt_non_potable_indoor_share_simple.text() == '28'
    assert tb.txt_external_demand_l_day.text() == '0'
    assert tb.txt_share.text() == '28'
    assert tb.txt_share.isReadOnly()


def test_interface_e_linha_de_comando_dao_o_mesmo_potencial(fracoes_na_interface_janela):
    sim = fracoes_na_interface_janela.tab_tanks_simulation
    sim.verified_dialogs = {'capex', 'motobomba', 'opex', 'tariffs'}
    sim.run_simulation(force=True)
    r = sim.last_sweep_result.results_by_volume
    pares = r.items() if isinstance(r, dict) else [(x.lower_tank_vol, x) for x in r]
    por_volume = {int(v): x.potential_potable_savings_pct for v, x in pares}
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        assert por_volume[4000] == pytest.approx(27.12, abs=0.005)
    else:
        # O 27,12 % é do tutorial do Brasil; o de cada edição é o que a linha de comando dá ao mesmo projeto.
        assert por_volume[4000] == pytest.approx(_rodar_cli(FRACOES_NA_INTERFACE_CASO)['potencial'][4000], abs=0.01)


def test_gravar_e_reabrir_preserva_as_fracoes(fracoes_na_interface_janela, tmp_path, fracoes_na_interface_monkeypatch_module):
    tb = fracoes_na_interface_janela.tab_building
    tb.txt_non_potable_indoor_share_simple.setText('30')
    tb.txt_external_demand_l_day.setText('150')
    destino = tmp_path / 'salvo.triton'
    fracoes_na_interface_monkeypatch_module.setattr(QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: (str(destino), '')))
    fracoes_na_interface_janela.on_save_simulation()
    c = load_triton_project(str(destino))
    cfg = c['config']
    assert c['aviso_fracoes'] is None
    assert cfg.non_potable_indoor_share == pytest.approx(0.3)
    assert cfg.irrigation_liters_per_day == pytest.approx(150.0)
    assert cfg.rainwater_share == pytest.approx((0.3 * 600 + 150) / 750, abs=0.0001)


# ---- origem: tests/ui/test_projeto_climbra_ui.py
_ARQUIVO_PROJETO_CLIMBRA_UI = str(_TESTES / 'ui/test_projeto_climbra_ui.py')

PROJETO_CLIMBRA_UI_RAIZ = Path(_ARQUIVO_PROJETO_CLIMBRA_UI).resolve().parents[2]


PROJETO_CLIMBRA_UI_CASO = _caso_do_manual(PROJETO_CLIMBRA_UI_RAIZ, *_VARREDURA)


@pytest.fixture
def projeto_climbra_ui_janela(monkeypatch):
    for nome in ('information', 'warning', 'critical'):
        monkeypatch.setattr(QMessageBox, nome, staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok))
    monkeypatch.setattr(QMessageBox, 'question', staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    app = QApplication.instance() or QApplication(sys.argv)
    from triton.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(PROJETO_CLIMBRA_UI_CASO))
    yield w
    w.close()
    app.processEvents()


def test_gravar_e_reabrir_com_a_climbra(projeto_climbra_ui_janela, tmp_path, monkeypatch):
    tp = projeto_climbra_ui_janela.tab_project
    tp.rb_source_national.setChecked(True)
    QApplication.processEvents()
    if tp.precip_data is None or len(tp.precip_data) == 0:
        pytest.skip('base CLIMBra ausente')
    serie = np.asarray(tp.precip_data, dtype=float).copy()
    destino = tmp_path / 'climbra.triton'
    monkeypatch.setattr(QFileDialog, 'getSaveFileName', staticmethod(lambda *a, **k: (str(destino), '')))
    projeto_climbra_ui_janela.on_save_simulation()
    chuva = json.loads(destino.read_text(encoding='utf-8'))['rainfall']
    assert chuva['source_mode'] == 'national_db'
    assert chuva['precipitation_mm'] == []
    assert chuva['climbra_series']['dias'] == len(serie)
    assert destino.stat().st_size < PROJETO_CLIMBRA_UI_CASO.stat().st_size / 3
    projeto_climbra_ui_janela.on_load_simulation(str(destino))
    QApplication.processEvents()
    assert projeto_climbra_ui_janela.tab_project.rb_source_national.isChecked()
    assert np.array_equal(np.asarray(projeto_climbra_ui_janela.tab_project.precip_data, dtype=float), serie)


# ---- origem: tests/ui/test_tarifa_exponencial_ui.py

TABELA = [(0.0, 0.0, 43.39, -1), (0.0, 1000.0, 9.15, PRECO_BASE_EXPONENCIAL), (0.0, 10.0, 1.0, EXPOENTE_DE_CONSUMO), (10.0, 20.0, 1.05, EXPOENTE_DE_CONSUMO), (20.0, 1000.0, 1.1, EXPOENTE_DE_CONSUMO), (1000.0, 999999.0, 9.15, 1)]


def test_o_gestor_mostra_a_formula_e_simula_com_o_motor(qapp):
    from triton.ui.tab_tariffs_manager import TabTariffsManager
    tab = TabTariffsManager()
    tab.load_city_tariffs('RS', 'Alegrete', 'residencial')
    assert 'Fórmula exponencial' in tab.lbl_disp_callout.text()
    tipos = [tab.table_tiers.item(r, 3).text() for r in range(tab.table_tiers.rowCount())]
    assert 'Preço-base (PB × Cⁿ)' in tipos and 'Expoente n' in tipos
    linha = tipos.index('Expoente n')
    tab.table_tiers.item(linha, 2).setText('1.1000')
    tab.spin_sim_vol.setValue(15.0)
    tab.update_bill_simulation()
    esperado = 43.39 + 9.15 * 15 ** 1.1 + 6.4 * 15
    assert f'Total: R$ {esperado:.2f}/mês' in tab.lbl_sim_result.text()
    assert 'PB × Cⁿ' in tab.lbl_sim_result.text()
    assert tab._faixas_da_tabela()[linha] == [0.0, 20.0, 1.1, EXPOENTE_DE_CONSUMO]
    assert tab.lbl_sewage.text() == 'Esgoto (R$/m³ consumido):'


def test_a_etapa_economica_preserva_a_tabela_exponencial(qapp):
    from triton.core.parser import TritonConfig
    from triton.ui.dialogs.dialog_economic import DialogTariffs
    cfg = TritonConfig()
    cfg.water_tariffs = list(TABELA)
    dialogo = DialogTariffs(config=cfg)
    dialogo.populate_table_from_tariffs(TABELA)
    dialogo.on_accept()
    assert cfg.water_tariffs == TABELA


def test_a_etapa_economica_traz_o_esgoto_por_m3_da_corsan(qapp):
    from triton.core.parser import TritonConfig
    from triton.core.tariffs_structure import ESGOTO_POR_M3
    from triton.ui.dialogs.dialog_economic import DialogTariffs
    cfg = TritonConfig()
    cfg.tariff_city_uf, cfg.tariff_city_name = ('RS', 'Alegrete')
    dialogo = DialogTariffs(config=cfg)
    assert dialogo.radio_esg_m3.isChecked()
    dialogo.on_accept()
    assert (cfg.sewage_mode, cfg.sewage_rate) == (ESGOTO_POR_M3, 6.4)


def test_municipio_com_tarifa_por_bairro_oferece_as_alternativas(qapp):
    """Rio de Janeiro: representativa, mais Zona Sul, Tarifa B e «sem a Tarifa 1»; a vigência vai junto."""
    from triton.core.parser import TritonConfig
    from triton.ui.dialogs.dialog_economic import DialogTariffs
    cfg = TritonConfig()
    cfg.tariff_city_uf, cfg.tariff_city_name = ('RJ', 'Rio de Janeiro')
    dialogo = DialogTariffs(config=cfg)
    dialogo.combo_uf.setCurrentIndex(dialogo.combo_uf.findData('RJ'))
    dialogo.combo_city.setCurrentIndex(dialogo.combo_city.findText('Rio de Janeiro'))
    dialogo.apply_city_tariffs()
    assert dialogo.combo_variante.count() == 4
    assert not dialogo.combo_variante.isHidden()
    assert dialogo.txt_vigencia.text() == '01/12/2025'
    dialogo.combo_variante.setCurrentIndex(1)
    dialogo.on_accept()
    assert cfg.water_tariffs[0] == (0.0, 15.0, 97.37, -2)
    assert cfg.tariff_vigencia == '01/12/2025'


# ---- origem: tests/ui/test_pipe_runs_dialog.py

LAYOUT = {'bim_components': [{'instance_id': 'CI-01', 'type_id': 'cisterna_inferior', 'position_mm': {'x': 0, 'y': 0, 'z': -1500}, 'parameters': {'CAPACIDADE_L': 5000}}, {'instance_id': 'B-01', 'type_id': 'motobomba', 'position_mm': {'x': 1500, 'y': 0, 'z': 0}}], 'pipe_runs': [{'run_id': 'T-01', 'system': 'succao', 'dn_mm': 32, 'start': 'CI-01', 'route': 'sobe 1500; +x 1500', 'end': 'B-01'}, {'run_id': 'T-02', 'system': 'recalque', 'dn_mm': 25, 'route': [{'direction': '+x', 'length_mm': 3000}]}]}


def test_dialog_keeps_parameters_and_revalidates_after_reordering(qapp):
    dialog = PipeRunsDialog(None, layout=LAYOUT, project_data={'project_name': 'Teste'})
    assert dialog.refresh_preview() == []
    assert dialog.preview.has_drawing()
    assert dialog.get_layout()['bim_components'][0]['parameters'] == {'CAPACIDADE_L': 5000}
    dialog.table_runs.setCurrentCell(1, 0)
    dialog.move_run(-1)
    runs = dialog.get_layout()['pipe_runs']
    assert [run['run_id'] for run in runs] == ['T-02', 'T-01']
    assert runs[0]['route'] == '+x 3000'
    errors = dialog.refresh_preview()
    assert errors == ['Trecho T-02: o primeiro trecho precisa de origem (componente ou coordenadas).']
    assert not dialog.preview.has_drawing()
    assert 'não será exportada' in dialog.lbl_report.text()


def test_dialog_builds_volumetry_with_building_and_exports(qapp, tmp_path, monkeypatch):
    layout = dict(LAYOUT, building_volume={'origin_mm': {'x': -1000, 'y': -3000, 'z': 0}, 'width_mm': 8000, 'depth_mm': 7000, 'height_mm': 6000, 'floors': 2})
    dialog = PipeRunsDialog(None, layout=layout, project_data={'project_name': 'Teste', 'lower_vol': 5000})
    assert dialog.get_layout()['building_volume']['floors'] == 2
    keys = {s.key for s in dialog.volumetry.view.scene.solids}
    assert {'EDIFICACAO', 'LAJE-1', 'CI-01', 'B-01', 'T-01#1'} <= keys
    assert dialog.btn_glb.isEnabled() and dialog.btn_html.isEnabled()
    from PySide6.QtWidgets import QFileDialog
    for fmt in ('glb', 'html'):
        target = tmp_path / f'vol.{fmt}'
        monkeypatch.setattr(QFileDialog, 'getSaveFileName', staticmethod(lambda *a, t=target: (str(t), '')))
        assert dialog.export_volumetry(fmt) == str(target) and target.stat().st_size > 1000
    dialog.building_fields['width_mm'].setValue(0)
    assert dialog.get_layout()['building_volume'] == {}
    dialog.table_runs.setCurrentCell(1, 0)
    dialog.move_run(-1)
    dialog.refresh_preview()
    assert dialog.volumetry.view.scene is None and (not dialog.btn_glb.isEnabled())


def test_dialog_prefills_from_study_when_layout_is_empty(qapp):
    project_data = {'project_name': 'Casa Modelo Estudo', 'lower_vol': 6000, 'upper_vol': 1500, 'floors': 2}
    dialog = PipeRunsDialog(None, layout=None, project_data=project_data)
    assert dialog.refresh_preview() == []
    assert dialog.preview.has_drawing()
    assert dialog.volumetry.view.scene is not None
    assert len(dialog.get_layout()['bim_components']) == 26
    assert len(dialog.get_layout()['pipe_runs']) == 19
    dialog.table_runs.setRowCount(0)
    assert dialog.table_runs.rowCount() == 0
    dialog.apply_study_layout()
    assert dialog.table_runs.rowCount() == 19
    assert dialog.refresh_preview() == []


# ---- origem: tests/ui/test_tab_building_templates.py

@pytest.fixture(scope='session')
def tab_building_templates_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_building_fixture_tweak_marks_custom(tab_building_templates_qapp):
    tab = TabBuilding()
    medio_idx = tab.combo_building_template.findData('res_medio')
    tab.combo_building_template.setCurrentIndex(medio_idx)
    assert tab.combo_building_template.currentData() == 'res_medio'
    tab.sp_shower_flow.setValue(15.0)
    assert tab.combo_building_template.currentData() == 'custom'
    cfg = tab.get_building_config()
    assert cfg['template_id'] == 'custom'
    assert cfg['shower_flow'] == 15.0


def test_tab_building_contextual_typology_adaptations(tab_building_templates_qapp):
    tab = TabBuilding()
    hosp_idx = tab.combo_building_template.findData('hospital')
    assert hosp_idx >= 0
    tab.combo_building_template.setCurrentIndex(hosp_idx)
    assert 'Leitos' in tab.lbl_residents_title.text()
    assert 'Esterilização' in tab.lbl_sp_sink_title.text() or 'Higiene' in tab.lbl_cin_pot_title.text()
    assert 'Lavanderia' in tab.lbl_sp_wash_cycles_title.text()
    cfg_hosp = tab.get_building_config()
    assert cfg_hosp['template_id'] == 'hospital'
    assert 220.0 <= cfg_hosp['demand'] <= 280.0
    escola_idx = tab.combo_building_template.findData('escola')
    assert escola_idx >= 0
    tab.combo_building_template.setCurrentIndex(escola_idx)
    assert 'Alunos' in tab.lbl_residents_title.text()
    assert 'Bebedouros' in tab.lbl_sp_sink_title.text()
    cfg_esc = tab.get_building_config()
    assert cfg_esc['template_id'] == 'escola'
    assert 35.0 <= cfg_esc['demand'] <= 50.0
    hotel_idx = tab.combo_building_template.findData('hotel')
    assert hotel_idx >= 0
    tab.combo_building_template.setCurrentIndex(hotel_idx)
    assert 'Hóspedes' in tab.lbl_residents_title.text()
    assert 'Enxoval' in tab.lbl_sp_wash_cycles_title.text() or 'Rouparia' in tab.lbl_sp_wash_cycles_title.text()
    cfg_hotel = tab.get_building_config()
    assert cfg_hotel['template_id'] == 'hotel'
    assert 220.0 <= cfg_hotel['demand'] <= 280.0


# ---- origem: tests/ui/test_volumetry_view.py

def _panel(qapp):
    panel = VolumetryPanel()
    panel.resize(1000, 600)
    panel.set_scene(build_volumetry(_project()))
    panel.show()
    qapp.processEvents()
    return panel


def test_click_selects_component_and_whole_run(qapp):
    panel = _panel(qapp)
    view = panel.view
    view.set_view('top')
    view.grab()
    project, *_ = view._projector()
    rs = next((s for s in view.scene.solids if s.key == 'RS-01'))
    centre = np.mean([p for f in rs.faces for p in f], axis=0)
    sx, sy, _ = project(np.array([centre]))
    assert view.select_at(QPointF(float(sx[0]), float(sy[0]))).key == 'RS-01'
    assert 'Capacidade: 1.000 L' in panel.lbl_info.text()
    pipe = next((s for s in view.scene.solids if s.key == 'T-02#1'))
    a, b, _ = pipe.axis
    sx, sy, _ = project(np.array([[(a[i] + b[i]) / 2 for i in range(3)]]))
    view.grab()
    hit = view.select_at(QPointF(float(sx[0]), float(sy[0])))
    assert hit is not None and hit.group == 'T-02'
    assert view._is_selected(next((s for s in view.scene.solids if s.key == 'T-02#3')))
    assert view.select_at(QPointF(2, 2)) is None


# ---- origem: tests/ui/test_ui_flow.py

@pytest.fixture(scope='session')
def ui_flow_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def _informa_os_fatores_do_pais(janela):
    """Fora da Brasil a ACV só roda com o fator da rede e o da água potável informados pelo usuário
    (``faltam_fatores_do_pais``); na Brasil eles já vêm preenchidos e nada muda."""
    from triton.core.edition import usa_dados_do_brasil
    if not usa_dados_do_brasil():
        janela.tab_environmental.txt_grid_co2.setText('0.2')
        janela.tab_environmental.txt_potable_co2.setText('0.35')


def test_full_ui_flow(ui_flow_qapp):
    window = MainWindow()
    _informa_os_fatores_do_pais(window)
    assert window is not None
    window.txt_workspace_project.setText('Residencial Horizonte')
    assert window.config.project_name == 'Residencial Horizonte'
    for idx in range(11):
        window.sidebar.step_changed.emit(idx)
        assert window.stack.currentIndex() == idx
    import numpy as np
    window.tab_project.precip_data = np.array([10.0] * 365, dtype=float)
    window.tab_project.txt_discard.setText('2.0')
    window.tab_project.txt_start_date.setText('01/01/1980')
    window.sync_project_state()
    assert window.tab_project.precip_data is not None
    assert len(window.tab_project.precip_data) == 365
    window.tab_building.txt_area.setText('800')
    window.tab_building.txt_demand.setText('180')
    window.tab_building.txt_residents.setText('10')
    window.tab_building.txt_share.setText('40')
    cfg = window.tab_building.get_building_config()
    assert cfg['area'] == 800.0
    assert cfg['residents'] == 10
    window.tab_tanks_simulation.txt_sweep_max.setText('10000')
    window.tab_tanks_simulation.txt_sweep_step.setText('2500')
    window.tab_tanks_simulation.txt_delta_ideal.setText('5.0')
    window.tab_tanks_simulation.txt_pump_thresh_pct.setText('10.0')
    window.sync_project_state()
    window.tab_tanks_simulation.run_simulation(force=False)
    assert window.tab_tanks_simulation.last_single_result is not None
    assert window.tab_tanks_simulation.last_single_result.potential_potable_savings_pct > 0.0
    window.tab_tanks_simulation.txt_sweep_max.setText('10001')
    window.tab_tanks_simulation.txt_sweep_step.setText('250')
    window.tab_tanks_simulation.run_simulation(force=False)
    adjusted_sweep = window.tab_tanks_simulation.last_sweep_result
    assert window.tab_tanks_simulation.txt_sweep_step.text() == '500'
    assert adjusted_sweep.effective_step_l == 500.0
    assert adjusted_sweep.results_by_volume[-1].lower_tank_vol == 10001.0
    assert len(adjusted_sweep.results_by_volume) - 1 <= 40
    window.tab_tanks_simulation.txt_inflation.setText('0.20')
    window.tab_tanks_simulation.txt_readj_period.setText('12')
    window.tab_tanks_simulation.txt_period.setText('20')
    window.tab_tanks_simulation.txt_tma.setText('2.00')
    window.tab_tanks_simulation.txt_readj_water.setText('5.0')
    window.tab_tanks_simulation.txt_readj_elec.setText('5.0')
    window.tab_tanks_simulation.verified_dialogs = {'capex', 'motobomba', 'opex', 'tariffs'}
    window.tab_economic.calculate_economics(force=True)
    window.sidebar.step_changed.emit(5)
    assert window.tab_economic.economic_optimum_volume is not None
    assert window.tab_economic.combo_active_volume.currentData() == window.tab_economic.economic_optimum_volume
    economic_headers = [window.tab_economic.table_mat_impact.horizontalHeaderItem(i).text() for i in range(window.tab_economic.table_mat_impact.columnCount())]
    assert all(('CO2' not in header for header in economic_headers))
    window.tab_global_optimizer.recalculate_all()
    assert window.tab_global_optimizer.table.rowCount() > 0
    assert window.tab_global_optimizer.tab_charts_topsis.count() == 2
    assert hasattr(window.tab_global_optimizer, 'topsis_proximity_chart')
    window.tab_environmental.combo_lower_mat.setCurrentIndex(1)
    window.tab_environmental.recalculate_and_update()
    lca_res = window.tab_environmental._last_lca_result
    assert lca_res is not None
    assert lca_res.total_embodied_co2_kg > 0
    assert window.tab_environmental.combo_env_active_volume.currentData() == pytest.approx(window.tab_environmental._last_sweep_lca.best_lifetime_co2_vol_liters)
    assert '--' not in window.sidebar.lbl_sum_opt_tech.text()
    assert '--' not in window.sidebar.lbl_sum_opt_econ.text()
    assert '--' not in window.sidebar.lbl_sum_opt_env.text()
    assert '--' not in window.sidebar.lbl_sum_opt_topsis.text()
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData('economic'))
    report_data = window.tab_reports._collect_project_data()
    assert report_data['report_charts'] == []
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData('research'))
    report_charts = window.tab_reports._collect_project_data()['report_charts']
    assert len(report_charts) == 11
    assert {chart['chapter'] for chart in report_charts} == {'hydraulic', 'decision', 'economic', 'environmental'}
    assert all((chart['data'].startswith('data:image/png;base64,') for chart in report_charts))
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData('economic'))
    window.tab_reports.update_report_preview()
    html_econ = window.tab_reports.generate_html_content()
    assert 'laudo técnico executivo' in html_econ.lower() or 'triton' in html_econ.lower()
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData('environmental'))
    window.tab_reports.update_report_preview()
    html_env = window.tab_reports.generate_html_content()
    assert 'desempenho ambiental' in html_env.lower()
    assert 'iso 14040' in html_env.lower() or 'inventário' in html_env.lower()
    window.tab_reports.combo_report_type.setCurrentIndex(window.tab_reports.combo_report_type.findData('research'))
    window.tab_reports.update_report_preview()
    html_research = window.tab_reports.generate_html_content()
    assert 'relatório técnico-científico de pesquisa' in html_research.lower()
    assert 'análise do ciclo de vida' in html_research.lower()


# ---- origem: tests/ui/test_mcdm_method_selector.py

def test_selector_exposes_smaa_vikor_as_one_method_with_simulation_profiles(qapp):
    tab = TabEconomicGlobalOptimizer()
    methods = [tab.combo_mcdm_method.itemData(i) for i in range(tab.combo_mcdm_method.count())]
    assert methods == ['topsis', 'smaa_vikor']
    tab.combo_mcdm_method.setCurrentIndex(1)
    assert tab.combo_smaa_profile.isVisibleTo(tab)
    assert not tab.combo_preset.isVisibleTo(tab)
    assert tab.lbl_profile.text() == 'Perfil de simulações:'
    assert tab.combo_smaa_profile.currentData() == 20000
    assert '20.000 simulações' in tab.lbl_weight_validation.text()
    assert 'VIKOR v=0.50' in tab.lbl_weight_validation.text()
    assert not tab.spin_w_tech.isVisibleTo(tab)
    assert tab.spin_v_param.isVisibleTo(tab)
    profiles = [tab.combo_smaa_profile.itemData(i) for i in range(tab.combo_smaa_profile.count())]
    assert profiles == [1000, 5000, 10000, 20000, 50000, 'custom']
    tab.combo_smaa_profile.setCurrentIndex(tab.combo_smaa_profile.findData('custom'))
    assert tab.spin_smaa_custom_samples.isVisibleTo(tab)
    tab.spin_smaa_custom_samples.setValue(12500)
    assert tab.get_smaa_num_simulations() == 12500
    assert '12.500 simulações' in tab.lbl_weight_validation.text()
    tab.spin_v_param.setValue(0.75)
    assert tab.get_vikor_v_param() == 0.75
    assert 'VIKOR v=0.75' in tab.lbl_weight_validation.text()
    tab.combo_mcdm_method.setCurrentIndex(0)
    assert not tab.combo_smaa_profile.isVisibleTo(tab)
    assert tab.combo_preset.isVisibleTo(tab)
    assert tab.lbl_profile.text() == 'Perfil de decisão:'
    assert tab.spin_w_tech.isVisibleTo(tab)
    assert not tab.spin_v_param.isVisibleTo(tab)
    tab.close()


# ---- origem: tests/unit/test_tab_building_ui.py

@pytest.fixture(scope='session')
def tab_building_ui_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_building_precalc_and_presets(tab_building_ui_qapp):
    tab = TabBuilding()
    pop_idx = tab.combo_building_template.findData('res_popular')
    assert pop_idx >= 0
    tab.combo_building_template.setCurrentIndex(pop_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0
    assert pot_sh + non_pot_sh == pytest.approx(100.0)
    med_idx = tab.combo_building_template.findData('res_medio')
    assert med_idx >= 0
    tab.combo_building_template.setCurrentIndex(med_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0
    com_idx = tab.combo_building_template.findData('comercial')
    assert com_idx >= 0
    tab.combo_building_template.setCurrentIndex(com_idx)
    v_pot, v_non_pot, d_in, pot_sh, non_pot_sh, irr_l = tab._calculate_fixture_values()
    assert d_in > 0
    assert 40.0 <= d_in <= 60.0


# ---- origem: tests/unit/test_tab_project_ui.py

@pytest.fixture(scope='session')
def tab_project_ui_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_com_o_campo_vazio_a_previa_usa_a_lamina_da_norma(tab_project_ui_qapp):
    """Vazio não é lâmina zero.

    Antes, esta prévia mostrava a chuva sem descarte nenhum enquanto a simulação
    já descontava a lâmina da ABNT NBR 15527:2019: duas contas diferentes na
    mesma janela, e a da tela era a errada.
    """
    tab = TabProject()
    tab.update_preview_table()
    COL_CHUVA, COL_DESCARTE = (2, 3)
    for linha in range(tab.table_preview.rowCount()):
        bruto = tab.table_preview.item(linha, COL_CHUVA)
        desconto = tab.table_preview.item(linha, COL_DESCARTE)
        if not bruto or not desconto:
            continue
        chuva = float(bruto.text().replace(' mm', '').replace(',', '.'))
        if chuva >= LAMINA_DE_DESCARTE_PADRAO_MM:
            esperado = f'-{LAMINA_DE_DESCARTE_PADRAO_MM:.1f}'.replace('.', ',') + ' mm'
            assert desconto.text() == esperado, (linha, chuva, desconto.text())
            return
    raise AssertionError('nenhum dia da prévia chove o bastante para descartar')


# ---- origem: tests/unit/test_comprimento_de_serie_ui.py
_ARQUIVO_COMPRIMENTO_DE_SERIE_UI = str(_TESTES / 'unit/test_comprimento_de_serie_ui.py')

COMPRIMENTO_DE_SERIE_UI_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_COMPRIMENTO_DE_SERIE_UI))))


if COMPRIMENTO_DE_SERIE_UI_RAIZ not in sys.path:
    sys.path.insert(0, COMPRIMENTO_DE_SERIE_UI_RAIZ)


@pytest.fixture(scope='session')
def comprimento_de_serie_ui_app():
    return QApplication.instance() or QApplication(sys.argv)


def test_a_aba_avisa_quando_a_serie_e_curta_demais(comprimento_de_serie_ui_app, monkeypatch):
    aba = TabTanksSimulation()
    aba.precip_data = np.full(200, 5.0)
    avisos = []
    monkeypatch.setattr('triton.ui.tab_tanks_simulation.QMessageBox.warning', lambda *args, **kwargs: avisos.append(args[1:3]))
    aba.on_analisar_comprimento_da_serie()
    assert avisos, 'a aba tinha de avisar que a série não dá para analisar'
    aba.deleteLater()


# ---- origem: tests/unit/test_technical_only_simulation.py

@pytest.fixture(scope='session')
def technical_only_simulation_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_technical_only_simulation_clears_and_hides_economic_environmental_topsis(technical_only_simulation_qapp, monkeypatch):
    monkeypatch.setattr(QMessageBox, 'information', lambda *args, **kwargs: None)
    monkeypatch.setattr(QMessageBox, 'warning', lambda *args, **kwargs: None)
    main_win = MainWindow()
    _informa_os_fatores_do_pais(main_win)
    dummy_precip = np.array([0.0, 15.0, 30.0, 0.0, 5.0, 25.0, 0.0] * 52)
    main_win.tab_project.precip_data = dummy_precip
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.txt_sweep_max.setText('5000')
    main_win.tab_tanks_simulation.txt_sweep_step.setText('2500')
    main_win.tab_tanks_simulation.txt_delta_ideal.setText('5.0')
    main_win.tab_tanks_simulation.txt_pump_thresh_pct.setText('10.0')
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.run_technical_simulation()
    assert main_win.tab_tanks_simulation._is_technical_only is True
    assert main_win.tab_charts.val_pot.text() != '--'
    assert main_win.tab_charts.val_fin_annual.text() == '--'
    assert main_win.tab_economic.lbl_val_vpl.text() == '--'
    assert main_win.tab_economic.lbl_val_invest.text() == '--'
    assert main_win.tab_economic.last_result is None
    assert main_win.tab_economic.economic_optimum_volume is None
    assert main_win.tab_environmental._last_lca_result is None
    assert main_win.tab_environmental._last_sweep_lca is None
    assert main_win.tab_global_optimizer.last_topsis_result is None
    assert main_win.tab_global_optimizer.table.rowCount() == 0
    tech, econ, env, topsis = main_win._optimal_volumes()
    assert tech is not None and tech > 0
    assert econ is None
    assert env is None
    assert topsis is None
    main_win.tab_tanks_simulation.run_simulation(force=True, is_technical_only=False)
    assert main_win.tab_tanks_simulation._is_technical_only is False
    assert main_win.tab_charts.val_fin_annual.text() != '--'
    assert main_win.tab_economic.lbl_val_vpl.text() != '--'
    assert main_win.tab_economic.last_result is not None
    assert main_win.tab_economic.economic_optimum_volume is not None
    assert main_win.tab_environmental._last_lca_result is not None
    assert main_win.tab_global_optimizer.last_topsis_result is not None
    assert main_win.tab_global_optimizer.table.rowCount() > 0
    tech2, econ2, env2, topsis2 = main_win._optimal_volumes()
    assert tech2 is not None
    assert econ2 is not None
    assert env2 is not None
    assert topsis2 is not None


def test_sweep_buttons_trigger_confirmation_dialogs(technical_only_simulation_qapp, monkeypatch):
    dialogs = []

    def fake_info(parent, title, text):
        dialogs.append((title, text))
    monkeypatch.setattr(QMessageBox, 'information', fake_info)
    monkeypatch.setattr(QMessageBox, 'warning', lambda *args, **kwargs: None)
    main_win = MainWindow()
    dummy_precip = np.array([0.0, 15.0, 30.0, 0.0, 5.0, 25.0, 0.0] * 52)
    main_win.tab_project.precip_data = dummy_precip
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.txt_sweep_max.setText('5000')
    main_win.tab_tanks_simulation.txt_sweep_step.setText('2500')
    main_win.tab_tanks_simulation.txt_delta_ideal.setText('5.0')
    main_win.tab_tanks_simulation.txt_pump_thresh_pct.setText('10.0')
    main_win.sync_project_state()
    main_win.tab_tanks_simulation.btn_run_tech_sim.click()
    assert len(dialogs) == 1
    assert 'Varredura Técnica Concluída' in dialogs[0][0]
    dialogs.clear()
    main_win.tab_tanks_simulation.btn_run_sim.click()
    assert len(dialogs) == 1
    assert 'Varredura Completa Concluída' in dialogs[0][0]


# ---- origem: tests/integration/test_national_climate_flow.py

@pytest.fixture(scope='session')
def national_climate_flow_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_national_climate_and_tariff_integration_flow(national_climate_flow_qapp):
    """Valida o fluxo integrado de seleção de cidade, carregamento de chuva e tarifas."""
    win = MainWindow()
    assert win is not None
    tab_p = win.tab_project
    idx_uf = tab_p.combo_climate_uf.findData('DF')
    if idx_uf >= 0:
        tab_p.combo_climate_uf.setCurrentIndex(idx_uf)
    idx_city = tab_p.combo_climate_city.findText('Brasília')
    if idx_city >= 0:
        tab_p.combo_climate_city.setCurrentIndex(idx_city)
    assert tab_p.precip_data is not None
    assert len(tab_p.precip_data) > 0
    assert 'Brasília' in tab_p.lbl_t_prestador.text() or 'CAESB' in tab_p.lbl_t_prestador.text()
    cfg = win.config
    assert cfg.tariff_city_uf == 'DF'
    assert 'Brasília' in cfg.tariff_city_name
    tab_p.txt_start_date.setText('01/01/1995')
    tab_p.txt_end_date.setText('31/12/1999')
    tab_p.on_apply_date_filter()
    assert len(tab_p.precip_data) == 1826
    assert tab_p.txt_start_date.text() == '01/01/1995'
    assert tab_p.txt_end_date.text() == '31/12/1999'
    win.tab_tanks_simulation.txt_sweep_max.setText('8000')
    win.tab_tanks_simulation.txt_sweep_step.setText('2000')
    win.tab_tanks_simulation.txt_delta_ideal.setText('2.5')
    win.tab_tanks_simulation.txt_pump_thresh_pct.setText('30')
    win.sync_project_state()
    win.tab_tanks_simulation.run_simulation(force=False)
    assert win.tab_tanks_simulation.last_sweep_result is not None
    assert len(win.tab_tanks_simulation.last_sweep_result.results_by_volume) > 1
    win.tab_tanks_simulation.verified_dialogs = {'capex', 'motobomba', 'opex', 'tariffs'}
    win.tab_economic.calculate_economics(force=True)
    assert win.tab_economic.economic_optimum_volume is not None
    tab_p._tariff_is_customized = True
    tab_p.on_restore_official_tariffs(show_dialog=False)
    assert tab_p._tariff_is_customized is False


# ---- origem: tests/ui/test_quantitativo_na_interface.py

def test_a_janela_nova_parte_do_arranjo(qapp):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    from triton.core.edition import usa_dados_do_brasil
    # CAPEX e mão de obra do arranjo (catálogos em reais) só no projeto novo da Brasil.
    assert janela.config.capex_do_arranjo is usa_dados_do_brasil()
    assert janela.config.mao_de_obra_automatica is usa_dados_do_brasil()
    janela.bim_layout = generate_study_layout({'lower_vol': 6000, 'area': 120})
    assert janela.config.bim_layout is janela.bim_layout or janela.config.bim_layout == janela.bim_layout
    janela.close()


def test_exportacoes_leem_os_resultados_que_as_abas_guardam(qapp, portugal):
    """A exportação procurava last_economic_result e last_env_result, que nenhuma aba define,
    e saía sem economia nem ACV. Lê agora os atributos reais e mostra a moeda do projeto."""
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        eco, amb, mcdm = object(), object(), object()
        janela.tab_economic.last_result = eco
        janela.tab_environmental._last_lca_result = amb
        janela.tab_global_optimizer.last_mcdm_result = mcdm
        r = janela.tab_export._resultados_do_estudo()
        assert r['economic_result'] is eco and r['environmental_result'] is amb and r['mcdm_result'] is mcdm
        assert janela.tab_export._collect_project_data()['moeda'] == '€'
    finally:
        janela.close()


# ---- coerência das edições na interface (auditoria de 08/10/2026)

def _textos_visiveis(raiz, janela, excluir=()):
    """Rótulos, botões, títulos, dicas, itens de lista e cabeçalhos que o usuário vê."""
    from PySide6.QtWidgets import QWidget, QLabel, QAbstractButton, QGroupBox, QComboBox, QTableWidget, QLineEdit
    textos = []
    for w in [raiz] + raiz.findChildren(QWidget):
        if not w.isVisibleTo(janela) or any(w is e or e.isAncestorOf(w) for e in excluir):
            continue
        textos.append(w.toolTip())
        if isinstance(w, (QLabel, QAbstractButton)):
            textos.append(w.text())
        elif isinstance(w, QGroupBox):
            textos.append(w.title())
        elif isinstance(w, QLineEdit):
            textos.append(w.placeholderText())
        elif isinstance(w, QComboBox):
            textos += [w.itemText(i) for i in range(w.count())]
        elif isinstance(w, QTableWidget):
            textos += [w.horizontalHeaderItem(j).text() for j in range(w.columnCount()) if w.horizontalHeaderItem(j)]
    return [t for t in textos if t]


def test_internacional_nao_mostra_reais_nem_a_climbra_nas_etapas(qapp, internacional):
    """Cabeçalhos, cartões e dicas em reais ao lado de valores em euros; a etapa 1 abria com a
    série de Florianópolis da CLIMBra (oculta) quando a base estava na pasta."""
    from PySide6.QtWidgets import QMenu
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        janela.show()
        tp = janela.tab_project
        assert tp.rb_source_custom.isChecked() and not tp.panel_national.isVisibleTo(janela)
        assert 'INM-CM4' not in tp.precip_file_path and tp.get_tariff_location() == ('CUSTOM', 'CUSTOM')
        acoes = [a.text() for m in janela.menuBar().findChildren(QMenu) for a in m.actions()]
        assert not any('652' in t for t in acoes)  # o Gestor de Tarifas, nem pelo menu
        moeda = janela.tab_tanks_simulation.combo_currency
        for etapa in (0, 1, 2, 3, 4, 5, 6, 7, 12):
            janela.on_step_changed(etapa)
            qapp.processEvents()
            textos = _textos_visiveis(janela.stack.widget(etapa), janela, excluir=(moeda,))
            ruins = [t for t in textos if any(m in t for m in ('R$', 'CLIMBra', 'CELESC', 'CASAN'))]
            assert not ruins, (etapa, ruins[:5])
    finally:
        janela.close()


def test_a_moeda_troca_de_novo_nos_cabecalhos(qapp, internacional):
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        ts, eco = janela.tab_tanks_simulation, janela.tab_economic
        def cab():
            t = eco.table_mat_impact
            return [t.horizontalHeaderItem(j).text() for j in range(t.columnCount())]
        assert any('(¤)' in c for c in cab())
        ts.combo_currency.setCurrentIndex(ts.combo_currency.findData('USD'))
        assert any('($)' in c for c in cab()) and not any('¤' in c for c in cab())
        ts.combo_currency.setCurrentIndex(ts.combo_currency.findData('EUR'))
        assert any('(€)' in c for c in cab()) and not any('$' in c for c in cab())
    finally:
        janela.close()


def test_portugal_mostra_a_etap_sem_precos_em_reais(qapp, portugal):
    from PySide6.QtWidgets import QLabel
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        aq = janela.tab_water_quality
        janela.config.chlorine_cost_per_kg = 0.0
        aq.recalculate_all()
        valor = lambda card: card.findChild(QLabel, 'val_label').text()
        assert valor(aq.card_etap_capex) == '—' and valor(aq.card_ff_capex) == '—'
        assert valor(aq.card_etap_opex) == '€ 0,00/ano'  # o cloro a preço zero não vira 25 €/kg
        assert 'R$' not in aq.lbl_cl_calc_cost.text() and '€ 0,00/kg' in aq.lbl_cl_calc_cost.text()
    finally:
        janela.close()


def test_brasil_continua_com_a_etap_e_os_cabecalhos_em_reais(qapp, brasil):
    from PySide6.QtWidgets import QLabel
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        aq = janela.tab_water_quality
        aq.recalculate_all()
        assert aq.card_etap_capex.findChild(QLabel, 'val_label').text().startswith('R$ ')
        assert 'R$ 25,00/kg' in aq.lbl_cl_calc_cost.text()
        assert 'R$' in janela.tab_economic.table_mat_impact.horizontalHeaderItem(3).text()
        janela.tab_modulacao_estocastica.atualizar_moeda()
        assert 'reais' in janela.tab_modulacao_estocastica.checks['fator_tarifa'].toolTip()
    finally:
        janela.close()


def test_preco_e_fator_zero_da_etap_nao_viram_os_da_brasil(monkeypatch):
    """`or 25.0` transformava o cloro a preço zero em R$ 25,00/kg; fator da rede zero virava o do MCTI."""
    from types import SimpleNamespace
    from triton.core.etap_integration import dimensionar_etap_do_projeto
    base = dict(water_quality_disinfection='uv', chlorine_dose_mg_l=1.5, area=100.0)
    zero = dimensionar_etap_do_projeto(SimpleNamespace(chlorine_cost_per_kg=0.0, grid_co2_factor_kg_kwh=0.0, **base),
                                       annual_pluvial_m3=100.0)
    assert zero.custo_anual_do_cloro == 0.0
    from triton.core.edition import usa_dados_do_brasil
    if not usa_dados_do_brasil():
        # Fora da Brasil a base padrão da rede vale zero (o usuário informa a dele): sem um padrão
        # diferente de zero, «ausente» e «zero informado» não se distinguem. Ensaia-se com um padrão.
        monkeypatch.setattr('triton.core.water_quality.fator_co2eq', lambda base='': 0.2)
    mcti = dimensionar_etap_do_projeto(SimpleNamespace(chlorine_cost_per_kg=0.0, **base), annual_pluvial_m3=100.0)
    assert zero.co2e_anual < mcti.co2e_anual


def test_dialogos_da_internacional_na_moeda_e_sem_precos_em_reais(qapp, internacional):
    from PySide6.QtWidgets import QLabel
    from triton.ui.main_window import MainWindow
    from triton.ui.dialogs import DialogTariffs, DialogOtherOpCosts, DialogInitialCosts
    from triton.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
    janela = MainWindow()
    try:
        ts = janela.tab_tanks_simulation
        for d in (DialogTariffs(ts, config=ts._get_config()),
                  DialogInitialCosts(ts, config=ts._get_config(), evaluated_volumes=[1000, 2000])):
            d.show()
            qapp.processEvents()
            ruins = [l.text() for l in d.findChildren(QLabel) if 'R$' in l.text() or 'Florianópolis' in l.text()]
            d.close()
            assert not ruins, ruins
        opex = DialogOtherOpCosts(ts, op_costs=[])
        assert opex.op_costs and all(fixo == 0 and var == 0 for _, _, fixo, var in opex.op_costs)
        assistente = PumpSelectionWizardDialog(upper_tank_vol=500, sweep_volumes=[1000], parent=ts)
        assert assistente.lbl_pump_cost.text() == '—' and assistente.table_sweep.item(0, 4).text() == '—'
        janela.tab_modulacao_estocastica.atualizar_moeda()
        assert 'reais' not in janela.tab_modulacao_estocastica.checks['fator_tarifa'].toolTip()
        # Trocar de moeda zera as manutenções sem apagá-las: a lista vazia voltava em reais.
        ts.combo_currency.setCurrentIndex(ts.combo_currency.findData('USD'))
        assert janela.config.op_costs and all(f == 0 and v == 0 for _, _, f, v in janela.config.op_costs)
    finally:
        janela.close()


def test_portugal_documentacao_em_portugues_de_portugal(qapp, portugal, monkeypatch):
    from PySide6.QtWidgets import QPushButton
    from triton.ui import translation as T
    from triton.ui.portugues_de_portugal import para_portugal
    monkeypatch.setattr(T, '_runtime_language', 'pt')
    from triton.ui.tab_documentation import TabDocumentation
    doc = TabDocumentation()
    botoes = [b.text() for b in doc.findChildren(QPushButton) if b.text()]
    assert botoes and not [t for t in botoes if para_portugal(t) != t]
    assert not any('Baixar' in t for t in botoes)
    assert T.em_portugues_da_edicao('VPL') == 'VAL'
    monkeypatch.setenv('TRITON_EDITION', 'BRL')
    assert T.em_portugues_da_edicao('VPL') == 'VPL'
