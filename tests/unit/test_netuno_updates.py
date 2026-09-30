"""
Testes de verificação para as atualizações do Netuno 5.0.0:
1. Versão 5.0.0
2. Paybacks simples e descontados calculados com precisão mensal
3. Cloração uniforme do reservatório superior nas varreduras
4. Sincronização e integridade do módulo ambiental
"""

import pytest
import numpy as np
from netuno import __version__
from netuno.core.economic import run_robust_economic_analysis, calculate_economic_indicators
from netuno.core.environmental import (
    EnvironmentalConfig, calculate_lca, run_environmental_sweep
)


def test_version_is_5_0_0():
    assert __version__ == "5.0.0"


def test_monthly_precision_payback_simple():
    """Valida se o payback simples é fracionário com precisão mensal."""
    # Investimento: 12.000, Economia líquida: 1.000/mês -> 12.000/ano
    # Payback deve ser exatamente 1.0 ano (12 meses).
    # Com economia de 1.500/mês -> 18.000/ano -> 8 meses -> 0.67 anos
    res = run_robust_economic_analysis(
        initial_investment=12000.0,
        annual_water_saved_m3=1800.0,
        water_tariff_per_m3=10.0,
        sewage_tariff_per_m3=0.0,
        sewage_mode=0,
        water_tariff_escalation_rate=0.0,
        sewage_tariff_escalation_rate=0.0,
        elec_tariff_escalation_rate=0.0,
        inflation_rate=0.0,
        discount_rate=0.0,
        annual_om_cost_base=0.0,
        pump_power_kw=0.0,
        pump_hours_year=0.0,
        elec_tariff_kwh=0.0,
        analysis_period_years=5,
        annual_chlorine_cost=0.0,
    )
    # 18.000/ano = 1.500/mês -> Mês 8 = 12.000
    assert res.payback_simple_years == pytest.approx(8.0 / 12.0, rel=1e-3)
    assert res.payback_discounted_years == pytest.approx(8.0 / 12.0, rel=1e-3)


def test_monthly_precision_payback_discounted():
    """Valida se o payback descontado é calculado mês a mês com taxa de desconto."""
    res = run_robust_economic_analysis(
        initial_investment=10000.0,
        annual_water_saved_m3=1000.0,
        water_tariff_per_m3=5.0,  # 5.000/ano bruto
        sewage_tariff_per_m3=0.0,
        sewage_mode=0,
        water_tariff_escalation_rate=0.0,
        discount_rate=0.10,  # 10% a.a., como fração (10.0 é recusado)
        annual_om_cost_base=0.0,
        pump_power_kw=0.0,
        analysis_period_years=10,
    )
    assert res.payback_simple_years == pytest.approx(2.0, rel=1e-2)
    # Payback descontado deve ser maior que o simples devido ao valor do dinheiro no tempo
    assert res.payback_discounted_years is not None
    assert res.payback_discounted_years > res.payback_simple_years
    # Deve ser um valor fracionário não inteiro
    assert res.payback_discounted_years > 2.0


def test_upper_tank_chlorination_uniform_in_environmental_sweep():
    """Valida se a cloração da caixa d'água superior é uniforme entre volumes na varredura ambiental."""
    cfg = EnvironmentalConfig(
        upper_tank_used=True,
        upper_tank_vol_liters=500.0,
        annual_water_saved_m3=120.0,
        chlorine_dose_mg_l=2.0,
        chlorine_co2_kg_per_kg=25.0
    )

    volume_map = [
        (0.0, 0.0),
        (1000.0, 50.0),
        (3000.0, 80.0),
        (5000.0, 100.0),
        (10000.0, 120.0),
    ]

    sw_res = run_environmental_sweep(volume_map, cfg)
    assert len(sw_res.sweep_details) == 5

    # Para V=0 (sem sistema), emissão e massa de cloro são 0
    assert sw_res.sweep_details[0]["lca_result"].annual_chlorine_kg == 0.0
    assert sw_res.sweep_details[0]["lca_result"].annual_treatment_co2_kg == 0.0

    # Para todos os volumes V > 0, massa e emissão de cloro devem ser iguais e uniformes
    cl_masses = [d["lca_result"].annual_chlorine_kg for d in sw_res.sweep_details[1:]]
    cl_co2s = [d["lca_result"].annual_treatment_co2_kg for d in sw_res.sweep_details[1:]]

    # Todos os valores devem ser iguais entre si
    assert len(set(round(m, 4) for m in cl_masses)) == 1
    assert len(set(round(c, 4) for c in cl_co2s)) == 1
    assert cl_masses[0] > 0.0


def test_a_cloracao_acompanha_o_tratamento_e_nao_a_caixa_superior():
    """Sem caixa superior, a água pluvial continua sendo clorada.

    Regra da 5.0.0: antes, desmarcar a caixa tirava o cloro do carbono e o
    deixava no custo. Sem cloro só quando o tratamento está desligado.
    """
    com_caixa = calculate_lca(5000.0, 100.0, EnvironmentalConfig(
        upper_tank_used=True, chlorine_dose_mg_l=2.0, chlorine_co2_kg_per_kg=25.0))
    sem_caixa = calculate_lca(5000.0, 100.0, EnvironmentalConfig(
        upper_tank_used=False, chlorine_dose_mg_l=2.0, chlorine_co2_kg_per_kg=25.0))
    assert sem_caixa.annual_chlorine_kg > 0.0
    assert sem_caixa.annual_chlorine_kg == pytest.approx(com_caixa.annual_chlorine_kg)

    cfg = EnvironmentalConfig(upper_tank_used=False, etap_enabled=False,
                              chlorine_dose_mg_l=2.0, chlorine_co2_kg_per_kg=25.0)
    cfg.chlorine_treatment_enabled = False   # lido por getattr; não é campo declarado
    sem_tratamento = calculate_lca(5000.0, 100.0, cfg)
    assert sem_tratamento.annual_chlorine_kg == 0.0
    assert sem_tratamento.annual_treatment_co2_kg == 0.0
