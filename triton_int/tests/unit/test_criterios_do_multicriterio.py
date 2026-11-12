"""Os oito critérios do multicritério (0.2.0): definição de cada um e regra dos pesos."""
import numpy as np
import pytest

from triton.core.simulation import run_single_simulation
from triton.core.topsis import (
    CRITERION_IS_BENEFIT, CRITERION_KEYS, PESOS_PADRAO, _criterion_weights, _decision_matrix,
    calculate_topsis_scores, candidato_dos_resultados, pesos_dos_criterios,
)


@pytest.fixture(scope="module")
def chuva():
    return np.random.default_rng(11).gamma(0.4, 12.0, 3650)


def _sim(chuva, volume, **kw):
    return run_single_simulation(precip_data=chuva, lower_tank_vol=float(volume), area=150.0,
                                 total_demand_per_day=600.0, rainwater_share=0.4, **kw)


def test_oito_criterios_em_quatro_eixos():
    assert len(CRITERION_KEYS) == 8
    assert list(CRITERION_IS_BENEFIT) == [True, True, True, False, False, False, False, False]
    assert PESOS_PADRAO == (0.25, 0.25, 0.25, 0.25)


def test_confiabilidade_volumetrica_e_a_demanda_pluvial_atendida(chuva):
    r = _sim(chuva, 3000)
    demanda = 600.0 * 0.4
    assert r.avg_pluvial_demand_l_day == pytest.approx(demanda)
    assert r.volumetric_reliability_pct == pytest.approx(100.0 * r.avg_pluvial_consumed_l_day / demanda)
    # Difere do potencial de economia, que divide pela demanda total
    assert r.volumetric_reliability_pct == pytest.approx(r.potential_potable_savings_pct / 0.4, rel=1e-9)


def test_eficiencia_de_armazenamento_e_a_renovacao_diaria_do_volume(chuva):
    r = _sim(chuva, 4000)
    assert r.storage_efficiency_pct == pytest.approx(100.0 * r.avg_pluvial_consumed_l_day / 4000.0)
    # Freia o superdimensionamento: cai com o volume
    efs = [_sim(chuva, v).storage_efficiency_pct for v in (1000, 3000, 8000, 20000)]
    assert efs == sorted(efs, reverse=True)
    assert _sim(chuva, 0).storage_efficiency_pct == 0.0


@pytest.mark.parametrize("superior", [False, True])
def test_numba_e_python_dao_os_mesmos_criterios(chuva, superior):
    kw = dict(upper_tank_used=True, upper_tank_vol=500.0) if superior else {}
    a = _sim(chuva, 2500, **kw)
    b = _sim(chuva, 2500, store_daily_details=True, **kw)
    assert a.volumetric_reliability_pct == pytest.approx(b.volumetric_reliability_pct, rel=1e-12)
    assert a.storage_efficiency_pct == pytest.approx(b.storage_efficiency_pct, rel=1e-12)
    assert a.mean_storage_pct == pytest.approx(b.mean_storage_pct, rel=1e-12)


def test_lcow_do_fluxo_anual_confere_com_a_conta_a_mao():
    from triton.core.economic import run_robust_economic_analysis
    e = run_robust_economic_analysis(
        initial_investment=10000.0, annual_water_saved_m3=50.0, water_tariff_per_m3=8.0,
        sewage_tariff_per_m3=0.0, sewage_mode=0, water_tariff_escalation_rate=0.0,
        sewage_tariff_escalation_rate=0.0, elec_tariff_escalation_rate=0.0, inflation_rate=0.0,
        discount_rate=0.05, annual_om_cost_base=100.0, pump_power_kw=0.0, pump_hours_year=0.0,
        elec_tariff_kwh=0.0, analysis_period_years=20)
    fatores = [1.0 / 1.05 ** ano for ano in range(1, 21)]
    esperado = (10000.0 + 100.0 * sum(fatores)) / (50.0 * sum(fatores))
    assert e.lcow_per_m3 == pytest.approx(esperado, rel=1e-9)


def test_pesos_padrao_tres_legados_e_sete_recusados():
    w = pesos_dos_criterios()
    assert w.sum() == pytest.approx(1.0)
    # Cada eixo com 25%, repartido em partes iguais dentro do eixo
    assert w[0] + w[1] == pytest.approx(0.25) and w[5] == pytest.approx(0.25)
    assert _criterion_weights((1, 1, 1)) == pytest.approx(_criterion_weights((1, 1, 1, 1)))
    assert _criterion_weights((2, 1, 0)) == pytest.approx(_criterion_weights((2, 1, 0, 1)))
    with pytest.raises(ValueError, match="oito critérios"):
        _criterion_weights((1, 0, 1, 1, 0, 1, 0))
    with pytest.raises(ValueError, match="oito critérios"):
        pesos_dos_criterios((1, 1, 1, 1), (1, 0, 1, 1, 0, 1, 0))


def test_candidato_dos_resultados_leva_os_criterios_do_programa(chuva):
    from triton.core.economic import run_robust_economic_analysis
    r = _sim(chuva, 3000)
    e = run_robust_economic_analysis(
        initial_investment=6000.0, annual_water_saved_m3=r.annual_pluvial_consumed_m3, water_tariff_per_m3=10.0,
        sewage_tariff_per_m3=0.0, sewage_mode=0, water_tariff_escalation_rate=0.0,
        sewage_tariff_escalation_rate=0.0, elec_tariff_escalation_rate=0.0, inflation_rate=0.0,
        discount_rate=0.06, annual_om_cost_base=80.0, pump_power_kw=0.0, pump_hours_year=0.0,
        elec_tariff_kwh=0.0, analysis_period_years=20)
    c = candidato_dos_resultados(r, e, 500.0, massa_seca_kg=120.0)
    linha = _decision_matrix([c])[0]
    valores = dict(zip(CRITERION_KEYS, linha))
    assert valores["volumetric_reliability_pct"] == pytest.approx(r.volumetric_reliability_pct)
    assert valores["storage_efficiency_pct"] == pytest.approx(r.storage_efficiency_pct)
    assert valores["net_financial_savings_brl"] == pytest.approx(e.vpl)
    assert valores["lcow_brl_m3"] == pytest.approx(e.lcow_per_m3)
    assert valores["lifecycle_co2_kg"] == pytest.approx(-500.0)
    assert valores["material_mass_kg"] == pytest.approx(120.0)
    assert valores["overflow_m3_yr"] == pytest.approx(r.annual_spill_m3)


def test_alternativa_sem_cisterna_recebe_a_pior_lcow_e_o_pior_payback(chuva):
    from triton.core.topsis import TopsisCandidate
    cands = [
        TopsisCandidate(lower_tank_vol=0.0, water_saved_m3_yr=0.0, vpl_brl=0.0, co2_saved_kg_lifetime=0.0),
        TopsisCandidate(lower_tank_vol=2000.0, water_saved_m3_yr=40.0, vpl_brl=900.0, co2_saved_kg_lifetime=100.0,
                        lcow_brl_m3=12.0, discounted_payback_years=9.0),
        TopsisCandidate(lower_tank_vol=4000.0, water_saved_m3_yr=45.0, vpl_brl=700.0, co2_saved_kg_lifetime=80.0,
                        lcow_brl_m3=14.0, discounted_payback_years=11.0),
    ]
    m = _decision_matrix(cands)
    col = {k: i for i, k in enumerate(CRITERION_KEYS)}
    assert m[0, col["lcow_brl_m3"]] > m[2, col["lcow_brl_m3"]]
    assert m[0, col["payback_years"]] > m[2, col["payback_years"]]
    assert calculate_topsis_scores(cands).best_candidate.lower_tank_vol > 0
