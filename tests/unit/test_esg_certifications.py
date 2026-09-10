import pytest
from netuno.core.esg_certifications import (
    calculate_esg_certifications,
    EsgConsolidatedReport,
    LeedWaterCredits,
    AquaHqeRating,
    CasaAzulRating
)


def test_calculate_esg_certifications():
    res = calculate_esg_certifications(
        potable_savings_pct=38.0,
        annual_pluvial_consumed_m3=250.0,
        annual_potable_consumed_m3=400.0,
        net_co2e_saved_kg_lifetime=3500.0,
        project_lifetime_years=20,
        has_irrigation_demand=True
    )
    assert isinstance(res, EsgConsolidatedReport)
    assert isinstance(res.leed, LeedWaterCredits)
    assert res.leed.indoor_water_points >= 3
    assert res.leed.total_leed_we_points >= 5
    assert isinstance(res.aqua, AquaHqeRating)
    assert res.aqua.stars >= 2
    assert isinstance(res.casa_azul, CasaAzulRating)
    assert res.casa_azul.category in ["Diamante", "Ouro", "Prata"]
    assert res.water_positive_ratio > 0
    assert len(res.esg_summary_text) > 20


def test_esg_simplified_mode():
    res = calculate_esg_certifications(
        potable_savings_pct=40.0,
        annual_pluvial_consumed_m3=200.0,
        annual_potable_consumed_m3=300.0,
        net_co2e_saved_kg_lifetime=2000.0,
        project_lifetime_years=20,
        is_simplified_mode=True
    )
    assert res.indoor_savings_pct > 0.0
    assert res.outdoor_savings_pct > 0.0
    assert res.leed.indoor_water_points >= 2
    assert res.leed.outdoor_water_points >= 1
    # Conta pelo conteúdo, não pelo tamanho: a matriz cresce quando entra uma
    # certificação nova, e contar linhas quebra o teste sem indicar defeito.
    codigos = {d.credit_code for d in res.credit_details}
    assert {"WEc1", "WEc2", "Categoria 4", "Critério 2.1", "WEM14"} <= codigos
    # Focus field should be populated
    assert any(d.focus for d in res.credit_details)


def test_esg_explicit_indoor_outdoor():
    res = calculate_esg_certifications(
        potable_savings_pct=35.0,
        annual_pluvial_consumed_m3=180.0,
        annual_potable_consumed_m3=320.0,
        net_co2e_saved_kg_lifetime=1800.0,
        indoor_savings_pct=32.0,
        outdoor_savings_pct=75.0,
        is_simplified_mode=False
    )
    assert res.indoor_savings_pct == 32.0
    assert res.outdoor_savings_pct == 75.0
    assert res.leed.indoor_water_points == 2
    assert res.leed.outdoor_water_points == 1
    assert res.leed.total_leed_we_points == 3


def test_esg_zero_outdoor_demand():
    """Valida que consumo externo zero resulta em 0 pontos no crédito LEED WEc1 e texto adequado."""
    res = calculate_esg_certifications(
        potable_savings_pct=42.0,
        annual_pluvial_consumed_m3=200.0,
        annual_potable_consumed_m3=276.0,
        net_co2e_saved_kg_lifetime=2500.0,
        project_lifetime_years=20,
        has_irrigation_demand=False,
        outdoor_demand_m3=0.0,
        outdoor_savings_pct=0.0,
        is_simplified_mode=False
    )
    assert res.leed.outdoor_water_points == 0
    assert res.outdoor_savings_pct == 0.0
    assert res.leed.indoor_water_points == 4  # 42% -> 4 pts (>= 40% e < 45%)
    assert res.leed.total_leed_we_points == 4
    wec1 = res.credit_details[0]
    assert wec1.credit_code == "WEc1"
    assert wec1.achieved_performance == "Sem consumo externo (0 m³/ano)"
    assert wec1.status == "Não aplicável (sem rega/área externa)"
    assert wec1.points_or_level == "0 / 2 pts"


def test_esg_zero_outdoor_demand_simplified_mode():
    """Valida que no modo simplificado com demanda externa zero não se inventa partição de 15% nem economia fictícia."""
    res = calculate_esg_certifications(
        potable_savings_pct=42.0,
        annual_pluvial_consumed_m3=200.0,
        annual_potable_consumed_m3=276.0,
        net_co2e_saved_kg_lifetime=2500.0,
        project_lifetime_years=20,
        has_irrigation_demand=False,
        outdoor_demand_m3=0.0,
        is_simplified_mode=True
    )
    assert res.outdoor_savings_pct == 0.0
    assert res.leed.outdoor_water_points == 0
    wec1 = res.credit_details[0]
    assert wec1.achieved_performance == "Sem consumo externo (0 m³/ano)"
    assert wec1.status == "Não aplicável (sem rega/área externa)"
    assert wec1.points_or_level == "0 / 2 pts"
    # A água pluvial vai 100% para o consumo interno
    assert res.indoor_savings_pct == pytest.approx(200.0 / 476.0 * 100.0, rel=1e-2)


def test_environmental_tab_opens_with_environmental_optimum(qapp):
    from netuno.ui.main_window import MainWindow
    from netuno.core.simulation import SweepSimulationResult, SingleTankSimulationResult

    win = MainWindow()
    results = [
        SingleTankSimulationResult(
            lower_tank_vol=float(v),
            potential_potable_savings_pct=40.0 + i * 5,
            avg_pluvial_consumed_l_day=(100.0 + i * 40) * 1000.0 / 365.25,
            avg_potable_consumed_l_day=(200.0 - i * 20) * 1000.0 / 365.25,
            avg_spilled_l_day=10.0,
            pct_days_full_satisfaction=60.0 + i * 5,
            pct_days_partial_satisfaction=20.0,
            pct_days_null_satisfaction=20.0 - i * 5,
        )
        for i, v in enumerate([2000, 3000, 5000, 7500, 10000])
    ]
    sweep_res = SweepSimulationResult(
        optimal_lower_tank_vol=5000.0,
        optimal_potential_pct=50.0,
        results_by_volume=results,
    )
    win.tab_tanks_simulation.last_sweep_result = sweep_res
    win.tab_tanks_simulation._is_technical_only = False
    win.config.econ_lower_tank_vol = 2000.0  # Volume econômico propositalmente discrepante

    win.tab_environmental.recalculate_and_update()

    opt_env = win.tab_environmental.environmental_optimum_volume
    assert opt_env is not None
    assert opt_env >= 5000.0
    cur_selected = win.tab_environmental.combo_env_active_volume.currentData()
    # Deve abrir rigorosamente com o reservatório ótimo ambiental selecionado
    assert cur_selected == pytest.approx(opt_env)
    assert cur_selected != 2000.0


