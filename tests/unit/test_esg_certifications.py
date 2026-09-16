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
    # Sem a economia externa calculada, WEc1 não é estimado: só WEc2 pontua.
    assert res.leed.outdoor_water_points == 0
    assert res.leed.total_leed_we_points == res.leed.indoor_water_points
    assert isinstance(res.aqua, AquaHqeRating)
    assert res.aqua.performance_level == "HQE (EAU.1.2)"   # 38%: acima de 20, abaixo de 40
    assert isinstance(res.casa_azul, CasaAzulRating)
    assert res.casa_azul.criterion_met
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
    # O modo simplificado deixou de inventar a partição 85/15 e os 35%.
    assert res.indoor_savings_pct == pytest.approx(40.0)
    assert res.outdoor_savings_pct == 0.0
    assert res.leed.indoor_water_points >= 2
    assert res.leed.outdoor_water_points == 0
    assert res.credit_details[0].status.startswith("Não avaliado")
    # Conta pelo conteúdo, não pelo tamanho: a matriz cresce quando entra uma
    # certificação nova, e contar linhas quebra o teste sem indicar defeito.
    codigos = {d.credit_code for d in res.credit_details}
    assert {"WEc1", "WEc2", "EAU.1.2 / EAU.1.3 / EAU.1.5", "Critério 3.6", "WEM14"} <= codigos
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


def test_certificacoes_usam_so_a_economia_total():
    """AQUA-HQE não sobe de nível por atalho do uso interno."""
    res = calculate_esg_certifications(
        potable_savings_pct=12.0,
        annual_pluvial_consumed_m3=60.0,
        annual_potable_consumed_m3=440.0,
        net_co2e_saved_kg_lifetime=500.0,
        indoor_savings_pct=36.0,
        outdoor_savings_pct=60.0,
    )
    assert res.aqua.performance_level == "Abaixo de EAU.1.2"
    assert any(i.startswith("EAU.1.5") for i in res.aqua.itens_atendidos)


@pytest.mark.parametrize("economia, nivel", [(19.9, "Abaixo de EAU.1.2"), (20.0, "HQE (EAU.1.2)"),
                                             (39.9, "HQE (EAU.1.2)"), (40.0, "HQE 3 (EAU.1.3)")])
def test_aqua_segue_os_itens_do_referencial_de_2024(economia, nivel):
    """Referencial AQUA-HQE Residencial v00 (22/11/2024): EAU.1.2 a 20%, EAU.1.3 a 40%.

    Os perfis «Base, Boas Práticas, Excelente» a 10, 25 e 40% não existem no referencial.
    """
    res = calculate_esg_certifications(
        potable_savings_pct=economia, annual_pluvial_consumed_m3=100.0,
        annual_potable_consumed_m3=300.0, net_co2e_saved_kg_lifetime=500.0)
    assert res.aqua.performance_level == nivel


@pytest.mark.parametrize("abrangencia, pontos", [(None, 0), ("areas_comuns", 2), ("loteamento", 2),
                                                 ("unidades", 4), ("unidades_e_areas_comuns", 5)])
def test_casa_azul_pontua_pela_abrangencia_e_nao_pelo_percentual(abrangencia, pontos):
    """Guia Casa Azul + CAIXA V023 (29/04/2026), critério 3.6: o indicador é a existência."""
    for economia in (5.0, 35.0):
        res = calculate_esg_certifications(
            potable_savings_pct=economia, annual_pluvial_consumed_m3=50.0,
            annual_potable_consumed_m3=400.0, net_co2e_saved_kg_lifetime=100.0,
            casa_azul_abrangencia=abrangencia)
        assert res.casa_azul.criterion_met
        assert res.casa_azul.points_awarded == pontos
    sem_sistema = calculate_esg_certifications(
        potable_savings_pct=0.0, annual_pluvial_consumed_m3=0.0,
        annual_potable_consumed_m3=400.0, net_co2e_saved_kg_lifetime=0.0,
        casa_azul_abrangencia=abrangencia)
    assert not sem_sistema.casa_azul.criterion_met and sem_sistema.casa_azul.points_awarded == 0


@pytest.mark.parametrize("externa, pontos", [(49.9, 0), (50.0, 1), (96.0, 1), (100.0, 2)])
def test_wec1_segue_os_limiares_do_leed(externa, pontos):
    res = calculate_esg_certifications(
        potable_savings_pct=30.0,
        annual_pluvial_consumed_m3=100.0,
        annual_potable_consumed_m3=233.0,
        net_co2e_saved_kg_lifetime=500.0,
        has_irrigation_demand=True,
        outdoor_demand_m3=20.0,
        indoor_savings_pct=30.0,
        outdoor_savings_pct=externa,
    )
    assert res.leed.outdoor_water_points == pontos


def test_irrigacao_atendida_sai_do_resultado_do_balanco():
    from types import SimpleNamespace
    from netuno.core.esg_certifications import irrigacao_atendida_m3
    assert irrigacao_atendida_m3(None) is None
    r = SimpleNamespace(avg_pluvial_irrigation_consumed_l_day=100.0)
    assert irrigacao_atendida_m3(r) == pytest.approx(36.525)
