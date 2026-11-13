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


# ── SMAA e PROMETHEE (0.2.0) ─────────────────────────────────────────────────────────────────

def _quatro_candidatos():
    from triton.core.topsis import TopsisCandidate
    dados = [(1000, 40, 900, 100, 12, 9, 70, 11, 60, 30), (2000, 50, 1200, 130, 11, 8, 85, 7, 80, 22),
             (4000, 55, 800, 90, 13, 11, 95, 4, 120, 15), (8000, 57, -500, -50, 18, 0, 99, 2, 200, 11)]
    return [TopsisCandidate(lower_tank_vol=v, water_saved_m3_yr=w, vpl_brl=n, co2_saved_kg_lifetime=c, lcow_brl_m3=l,
                            discounted_payback_years=pb, volumetric_reliability_pct=r, storage_efficiency_pct=e,
                            material_mass_kg=ms, overflow_m3_yr=o) for v, w, n, c, l, pb, r, e, ms, o in dados]


def test_promethee_usual_nao_zera_os_fluxos():
    from triton.core.mcda.mcdm_methods import run_promethee
    fluxos = run_promethee(_quatro_candidatos(), preference_function="usual").net_flows
    assert np.any(np.abs(fluxos) > 1e-9)
    assert float(np.sum(fluxos)) == pytest.approx(0.0, abs=1e-12)


def test_smaa_sorteia_25_por_cento_por_eixo_em_media():
    from triton.core.mcda.mcdm_methods import _smaa_dirichlet_alpha
    a = _smaa_dirichlet_alpha(8)
    assert [a[0:2].sum(), a[2:5].sum(), a[5], a[6:8].sum()] == pytest.approx([2.0, 2.0, 2.0, 2.0])
    # O peso esperado de cada critério é o padrão do TOPSIS
    assert a / a.sum() == pytest.approx(pesos_dos_criterios())
    assert np.array_equal(_smaa_dirichlet_alpha(5), np.ones(5))


def test_smaa_topsis_usa_a_conta_do_topsis_do_programa():
    from triton.core.mcda.mcdm_methods import _topsis_scores_kernel, run_smaa_analysis
    cands = _quatro_candidatos()
    m = _decision_matrix(cands)
    desloc = m - m.min(axis=0)
    norma = np.sqrt((desloc ** 2).sum(axis=0))
    norma[norma == 0] = 1.0
    w = np.array([0.2, 0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.1])
    esperado = calculate_topsis_scores(cands, weights=tuple(w)).scores
    obtido = _topsis_scores_kernel(np.ascontiguousarray(desloc / norma), np.ascontiguousarray(CRITERION_IS_BENEFIT), w)
    assert obtido == pytest.approx(esperado, abs=1e-12)
    s = run_smaa_analysis(cands, num_samples=2000, engine="topsis", random_seed=7)
    assert s.first_rank_probs.sum() == pytest.approx(100.0)
    assert len(s.confidence_factors) == len(cands)
    assert sum(s.get_central_dimension_weights(s.best_index)) == pytest.approx(1.0)


# ── Pesos objetivos pelo CRITIC (Diakoulaki, Mavrotas e Papayannakis, 1995) ─────────────────────

def test_critic_confere_com_a_formula():
    from triton.core.topsis import pesos_critic
    cands = _quatro_candidatos()
    M = _decision_matrix(cands)
    B = CRITERION_IS_BENEFIT
    R = np.where(B, (M - M.min(0)) / (M.max(0) - M.min(0)), (M.max(0) - M) / (M.max(0) - M.min(0)))
    C = R.std(0) * (1.0 - np.corrcoef(R, rowvar=False)).sum(1)
    w = pesos_critic(M, [c.lower_tank_vol for c in cands])
    assert w == pytest.approx(C / C.sum())
    assert w.sum() == pytest.approx(1.0) and np.all(w >= 0)


def test_critic_criterio_constante_pesa_zero_e_sem_contraste_os_pesos_ficam_iguais():
    from triton.core.topsis import pesos_critic
    M = np.array([[1.0, 5.0, 3.0, 2.0, 7.0, 1.0, 4.0, 9.0],
                  [2.0, 5.0, 1.0, 4.0, 6.0, 3.0, 4.0, 7.0],
                  [3.0, 5.0, 2.0, 1.0, 9.0, 2.0, 4.0, 8.0]])
    w = pesos_critic(M)
    assert w[1] == 0.0 and w[6] == 0.0
    assert pesos_critic(np.ones((3, 8))) == pytest.approx(np.full(8, 1 / 8))


def test_critic_vale_no_topsis_no_vikor_e_no_promethee_e_ignora_o_volume_zero():
    from triton.core.mcda.mcdm_methods import run_promethee, run_vikor
    from triton.core.topsis import TopsisCandidate, pesos_critic
    cands = [TopsisCandidate(lower_tank_vol=0.0, water_saved_m3_yr=0.0, vpl_brl=0.0, co2_saved_kg_lifetime=0.0)] + _quatro_candidatos()
    res = calculate_topsis_scores(cands, weights="critic")
    sem_zero = pesos_critic(_decision_matrix(cands)[1:])
    assert res.criterion_weights == pytest.approx(sem_zero)
    assert run_vikor(cands, weights="CRITIC").best_candidate.lower_tank_vol > 0
    assert run_promethee(cands, weights="critic").best_candidate.lower_tank_vol > 0
    with pytest.raises(ValueError):
        calculate_topsis_scores(cands, weights="entropia")


def test_critic_na_linha_de_comando_e_no_estudo():
    from triton import cli
    assert cli._parse_weights("critic") == "critic"
    assert cli._validate_analysis_config({"topsis_weights": "critic"}) == []
    assert cli._pesos_lidos("Critic") == "critic" and cli._pesos_lidos([1, 1, 1, 1]) == (1, 1, 1, 1)
    assert cli._analysis_from_ui_state({"topsis": {"preset_key": "critic"}})["topsis_weights"] == "critic"


# ── Faixa de escolha: volumes de resultado semelhante, em vez de «o melhor volume» ─────────────────

def test_faixa_de_escolha_reune_os_volumes_proximos_do_maior_escore():
    from triton.core.topsis import faixa_de_escolha
    v = [0, 1000, 2000, 3000, 4000, 5000, 8000, 12000]
    s = [0.9, 0.653, 0.773, 0.754, 0.717, 0.668, 0.484, 0.31]   # o volume zero fica de fora
    f = faixa_de_escolha(v, s)
    assert (f["min_volume_l"], f["max_volume_l"], f["best_volume_l"]) == (2000.0, 3000.0, 2000.0)
    assert f["contiguous"] and f["tolerance"] == 0.05
    assert faixa_de_escolha(v, s, tolerancia=0.15)["max_volume_l"] == 4000.0
    assert faixa_de_escolha(v, s, tolerancia=0.0)["volumes_l"] == [2000.0]
    # Faixa com lacuna: 2.000 L fica fora entre dois volumes de dentro
    lacuna = faixa_de_escolha([1000, 2000, 3000], [0.5, 0.2, 0.49])
    assert lacuna["volumes_l"] == [1000.0, 3000.0] and not lacuna["contiguous"]
    # Menor é melhor (índice Q do VIKOR)
    assert faixa_de_escolha([1000, 2000, 3000], [0.0, 0.03, 1.0], maior_melhor=False)["volumes_l"] == [1000.0, 2000.0]
    with pytest.raises(ValueError):
        faixa_de_escolha(v, s, tolerancia=1.5)


def test_faixa_de_escolha_sai_na_analise_e_nas_metricas_do_estudo():
    from triton import cli
    from triton.core.estudo import METRICAS
    cfg = cli.configuracao_da_edicao()
    cfg.area = 150.0
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 6000.0
    cfg.lower_tank_step = 1000.0
    rel = cli.run_analysis(cfg, np.random.default_rng(2).gamma(0.4, 12.0, 730), "all", smaa=False, score_band=0.10)
    t = rel["topsis"]
    assert t["choice_band"]["tolerance"] == 0.10
    assert t["choice_band_min_volume_l"] <= t["best_volume_l"] <= t["choice_band_max_volume_l"]
    assert METRICAS["faixa_topsis_min_l"]["chave"] == "choice_band_min_volume_l"
    assert cli._validate_analysis_config({"topsis_score_band": 2}) != []


# ── Faixa de escolha nas saídas da linha de comando (0.2.0) ──────────────────────────────────

def _faixa(volumes, contigua=True, melhor=None):
    return {"tolerance": 0.05, "volumes_l": [float(v) for v in volumes], "min_volume_l": float(min(volumes)),
            "max_volume_l": float(max(volumes)), "best_volume_l": float(melhor or volumes[0]), "contiguous": contigua}


def test_texto_dos_volumes_da_faixa():
    from triton.core.topsis import volumes_da_faixa, faixa_de_um_volume
    assert volumes_da_faixa(_faixa([2000, 2500, 3000])) == "2000–3000"
    assert volumes_da_faixa(_faixa([2000])) == "2000"
    assert volumes_da_faixa(_faixa([1000, 3000], contigua=False)) == "1000, 3000"
    assert volumes_da_faixa(None) == ""
    assert faixa_de_um_volume(_faixa([2000])) and not faixa_de_um_volume(_faixa([2000, 2500]))


def test_linha_do_topsis_nao_diz_de_1000_a_1000():
    from triton import cli
    base = {"best_volume_l": 1000.0, "best_score": 0.674}
    so_um = cli._linha_do_topsis({**base, "choice_band": _faixa([1000])})
    assert "1000 a 1000" not in so_um and "1000–1000" not in so_um
    assert "1000 L" in so_um and "0.674" in so_um
    com_lacuna = cli._linha_do_topsis({**base, "choice_band": _faixa([1000, 3000], contigua=False)})
    assert "1000, 3000 L" in com_lacuna and " a 3000" not in com_lacuna
    continua = cli._linha_do_topsis({**base, "choice_band": _faixa([1000, 1500, 2000])})
    assert "1000" in continua and "2000" in continua and ("semelhantes" in continua or "similar" in continua)


def test_linha_do_smaa_traz_a_faixa_quando_ha_mais_de_um_volume():
    from triton import cli
    sv = {"best_volume_l": 2000.0, "best_acceptability_pct": 27.7, "samples": 20000}
    faixa = cli._linha_do_smaa({**sv, "choice_band": _faixa([1500, 2000, 2500], melhor=2000)})
    assert "1500–2500 L" in faixa and "27.7" in faixa
    so_um = cli._linha_do_smaa({**sv, "choice_band": _faixa([2000])})
    assert so_um.startswith("SMAA-VIKOR: 2000 L |") and "–" not in so_um


def test_html_da_faixa_com_um_volume_e_com_lacuna():
    from triton import cli
    um = cli._html_da_faixa({"topsis": {"choice_band": _faixa([1000])}})
    assert "1000 a 1000" not in um and "1000 L" in um
    lacuna = cli._html_da_faixa({"topsis": {"choice_band": _faixa([1000, 3000], contigua=False)}})
    assert "1000, 3000 L" in lacuna


def test_pesos_somados_por_eixo():
    from triton.core.topsis import pesos_somados_por_eixo
    eixos = pesos_somados_por_eixo([0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.15, 0.15])
    assert eixos == pytest.approx((0.2, 0.3, 0.2, 0.3))
    with pytest.raises(ValueError):
        pesos_somados_por_eixo([0.25] * 4)


# ── Linhas econômica e ambiental do relatório de texto ────────────────────────────────────────

def _alt_econ(vol, npv, capex, payback):
    return {"lower_tank_volume_l": float(vol), "npv_brl": npv, "capex_brl": capex, "discounted_payback_months": payback}


def test_linha_economica_diz_o_criterio_e_avisa_capex_zero():
    from triton import cli
    sem_custo = {"economic": {"alternatives": [_alt_econ(0, 0, 0, 0), _alt_econ(1000, 600, 0, 0), _alt_econ(5000, 850, 0, 0)]}}
    linhas = cli._linhas_economicas(sem_custo)
    assert "5000 L" in linhas[0]
    from triton.cli_textos import t as _t  # «maior VAL» na Ibérica, «highest NPV» na Internacional
    assert "Payback" not in linhas[0] and _t("Melhor alternativa econômica (maior VPL):") in linhas[0], linhas
    assert len(linhas) == 2 and "CAPEX" in linhas[1]
    com_custo = {"economic": {"alternatives": [_alt_econ(1000, 300, 900, 60), _alt_econ(2000, 500, 1500, 48)]}}
    linhas = cli._linhas_economicas(com_custo)
    assert len(linhas) == 1 and "2000 L" in linhas[0] and "Payback: 4.0" in linhas[0]
    assert "4.0a" not in linhas[0]


def test_linha_ambiental_explica_o_negativo():
    from triton import cli
    alts = [{"lower_tank_volume_l": 1000.0, "lifetime_net_co2_saved_kg": -162.9},
            {"lower_tank_volume_l": 2000.0, "lifetime_net_co2_saved_kg": -240.0}]
    linha = cli._linha_ambiental({"environmental": {"alternatives": alts}})
    assert "1000 L" in linha and "-162.90 kg" in linha and "CO2e" in linha
    assert "negativo" in linha or "negative" in linha
    positivo = cli._linha_ambiental({"environmental": {"alternatives": [{"lower_tank_volume_l": 3000.0, "lifetime_net_co2_saved_kg": 342.7}]}})
    assert "342.70 kg" in positivo and "negativo" not in positivo and "negative" not in positivo
