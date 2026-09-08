"""
Testes de robustez contra entradas caóticas, inversões de parâmetros
e comportamentos inesperados de usuários leigos.
"""

import numpy as np
import pytest

from netuno.core.parser import parse_float, parse_int, NetunoConfig
from netuno.core.simulation import (
    build_sweep_volume_grid,
    build_daily_demand_vectors,
    build_detailed_daily_demand_vectors,
    run_single_simulation,
    run_sweep_simulation,
)
from netuno.core.economic import (
    run_robust_economic_analysis,
    calculate_effective_tariff,
)
from netuno.core.cost_estimates import (
    estimate_preliminary_capex,
)
from netuno.core.environmental import (
    calculate_lca,
    EnvironmentalConfig,
)


# ── 1. Robustez do Parser com Strings Caóticas e Inversões de Formatação ───────

def test_parser_chaotic_strings():
    """Valida se o parser tolera formatos pt-BR, en-US, lixo textual e vazios sem quebrar."""
    assert parse_float("1.234,56") == 1234.56
    assert parse_float("1,234.56") == 1234.56
    assert parse_float("1234,56") == 1234.56
    assert parse_float("1234.56") == 1234.56
    assert parse_float("  150,00  ") == 150.0
    assert parse_float("NaN", 42.0) == 42.0
    assert parse_float("inf", 42.0) == 42.0
    assert parse_float("texto_invalido", 10.0) == 10.0
    assert parse_float("-", 5.0) == 5.0
    assert parse_float("", 99.0) == 99.0
    assert parse_float(None, 7.0) == 7.0

    assert parse_int(" 1000 ") == 1000
    assert parse_int(" 1.000,00 ") == 1000
    assert parse_int("10,0") == 10
    assert parse_int("abc", 4) == 4
    assert parse_int("-", 2) == 2
    assert parse_int(None, 1) == 1


# ── 2. Inversão de Parâmetros de Varredura de Reservatórios ────────────────────

def test_sweep_step_larger_than_max():
    """Valida se passo maior que o volume máximo não quebra a grade nem trava em loop infinito."""
    grid = build_sweep_volume_grid(lower_tank_max=500.0, requested_step_l=5000.0)
    assert grid.volumes_l == [0.0, 500.0]
    assert grid.positive_volume_count == 1


def test_sweep_with_zero_maximum():
    """Valida se varredura com volume máximo zero gera a referência de 0 L com segurança."""
    grid = build_sweep_volume_grid(lower_tank_max=0.0, requested_step_l=250.0)
    assert grid.volumes_l == [0.0]
    assert grid.positive_volume_count == 0


def test_sweep_with_fractional_non_multiple_max():
    """Valida se volume máximo quebrado é preservado como último ponto auditável."""
    grid = build_sweep_volume_grid(lower_tank_max=1350.0, requested_step_l=500.0)
    assert grid.volumes_l == [0.0, 500.0, 1000.0, 1350.0]
    assert grid.volumes_l[-1] == 1350.0


# ── 3. Robustez Hidráulica: Entradas Limítrofes e Inversões de Demanda ──────────

def test_simulation_with_zero_demand_and_residents():
    """Valida que demanda zero ou moradores zero não causam divisão por zero na simulação."""
    precip = np.array([10.0, 0.0, 5.0, 0.0], dtype=np.float64)
    b_cfg = {
        "demand": 0.0,
        "residents": 0,
        "share": 0.4,
        "potable_indoor_share": 0.65,
        "non_potable_indoor_share": 0.35,
        "irrigation_liters_per_day": 0.0,
    }
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.8,
        discard_mm=1.0,
        building_config=b_cfg,
    )
    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.annual_pluvial_consumed_m3 == 0.0


def test_simulation_with_zero_area_or_runoff():
    """Valida captação nula com área zero ou coeficiente de escoamento zero."""
    precip = np.array([50.0, 20.0, 10.0], dtype=np.float64)
    b_cfg = {"demand": 150.0, "residents": 4, "share": 0.4}
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=5000.0,
        area=0.0,
        runoff_coeff=0.0,
        discard_mm=0.0,
        building_config=b_cfg,
    )
    # Sem captação, cisterna permanece vazia e não supre pluvial
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.potential_potable_savings_pct == 0.0


def test_inverted_potable_and_non_potable_shares():
    """Valida se 100% não-potável ou 100% potável funcionam estavelmente."""
    precip = np.array([10.0, 0.0, 0.0], dtype=np.float64)
    
    # Caso 100% não-potável interno
    b_cfg_100np = {
        "demand": 100.0, "residents": 2,
        "potable_indoor_share": 0.0, "non_potable_indoor_share": 1.0,
        "irrigation_liters_per_day": 0.0
    }
    res_100np = run_single_simulation(
        precip_data=precip, lower_tank_vol=2000.0, area=100.0,
        runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True,
        building_config=b_cfg_100np
    )
    assert res_100np.daily_results[0].potable_indoor_consumed_liters == 0.0
    assert res_100np.daily_results[0].pluvial_indoor_consumed_liters == 200.0

    # Caso 100% potável interno
    b_cfg_100p = {
        "demand": 100.0, "residents": 2,
        "potable_indoor_share": 1.0, "non_potable_indoor_share": 0.0,
        "irrigation_liters_per_day": 0.0
    }
    res_100p = run_single_simulation(
        precip_data=precip, lower_tank_vol=2000.0, area=100.0,
        runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True,
        building_config=b_cfg_100p
    )
    assert res_100p.daily_results[0].pluvial_indoor_consumed_liters == 0.0
    assert res_100p.daily_results[0].potable_indoor_consumed_liters == 200.0


def test_huge_demand_and_huge_area_resilience():
    """Valida se demandas industriais/enormes não causam overflow numérico."""
    precip = np.array([25.0, 10.0, 0.0, 50.0], dtype=np.float64)
    b_cfg = {
        "demand": 50000.0,  # 50.000 L/hab/dia
        "residents": 100,    # 5.000.000 L/dia
        "potable_indoor_share": 0.50,
        "non_potable_indoor_share": 0.50,
        "irrigation_liters_per_day": 200000.0,
    }
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=1000000.0,  # 1.000 m³
        area=50000.0,              # 50.000 m²
        runoff_coeff=0.9,
        discard_mm=2.0,
        building_config=b_cfg,
    )
    assert np.isfinite(res.avg_pluvial_consumed_l_day)
    assert np.isfinite(res.potential_potable_savings_pct)
    assert res.avg_pluvial_consumed_l_day > 0


# ── 4. Robustez Econômica: Taxas Extremas e Inversões Financeiras ──────────────

def test_economic_hyper_discount_rate_and_zero_inflation():
    """Valida TMA de 40% a.a. ou inflação zero sem overflow ou erro de convergência."""
    res = run_robust_economic_analysis(
        initial_investment=50000.0,
        annual_water_saved_m3=100.0,
        water_tariff_per_m3=5.0,
        sewage_tariff_per_m3=5.0,
        discount_rate=0.40,  # 40% a.a.
        inflation_rate=0.0,
        analysis_period_years=20,
    )
    assert np.isfinite(res.vpl)
    assert res.vpl < 0


def test_economic_zero_investment_and_zero_savings():
    """Valida caso sem investimento e sem economia (referência 0 L)."""
    res = run_robust_economic_analysis(
        initial_investment=0.0,
        annual_water_saved_m3=0.0,
        water_tariff_per_m3=5.0,
        sewage_tariff_per_m3=5.0,
        discount_rate=0.10,
        inflation_rate=0.04,
        analysis_period_years=20,
    )
    assert res.vpl == 0.0
    assert res.total_investment == 0.0
    assert res.payback_simple_years == 0.0
    assert res.payback_discounted_years == 0.0


# ── 5. Robustez Ambiental (ACV) com Entradas Limítrofes ────────────────────────

def test_environmental_zero_volume_and_zero_chlorine():
    """Valida se ACV com 0 L não quebra nem gera impactos de fabricação."""
    cfg = EnvironmentalConfig(
        upper_tank_used=False,
        chlorine_dose_mg_l=0.0,
        pipes=[],
    )
    res = calculate_lca(tank_vol_liters=0.0, annual_pluvial_m3=0.0, config=cfg)
    assert res.total_embodied_co2_kg == 0.0
    assert res.annual_avoided_co2_kg == 0.0
    assert res.annual_treatment_co2_kg == 0.0
    assert res.environmental_payback_years == 0.0
