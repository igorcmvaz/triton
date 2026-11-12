# -*- coding: utf-8 -*-
"""Testes de unidade e invariantes para o método PROMETHEE II em triton.core.mcdm_methods."""

import pytest
import numpy as np

from triton.core.topsis import TopsisCandidate
from triton.core.mcdm_methods import run_promethee, PrometheeResult


def _criar_candidatos_teste():
    """Cria conjunto de candidatos para validação de ordenação multicritério."""
    c1 = TopsisCandidate(
        lower_tank_vol=1000.0,
        water_saved_m3_yr=80.0,
        vpl_brl=12000.0,
        co2_saved_kg_lifetime=-250.0,
        potential_savings_pct=25.0,
        overflow_m3_yr=80.0,
        discounted_payback_years=5.0,
        irr_pct=15.0,
        potable_consumed_m3_yr=150.0,
    )
    c2 = TopsisCandidate(
        lower_tank_vol=3000.0,
        water_saved_m3_yr=140.0,
        vpl_brl=25000.0,
        co2_saved_kg_lifetime=-400.0,
        potential_savings_pct=50.0,
        overflow_m3_yr=40.0,
        discounted_payback_years=4.0,
        irr_pct=22.0,
        potable_consumed_m3_yr=100.0,
    )
    c3 = TopsisCandidate(
        lower_tank_vol=5000.0,
        water_saved_m3_yr=180.0,
        vpl_brl=30000.0,
        co2_saved_kg_lifetime=-600.0,
        potential_savings_pct=65.0,
        overflow_m3_yr=20.0,
        discounted_payback_years=4.5,
        irr_pct=20.0,
        potable_consumed_m3_yr=70.0,
    )
    return [c1, c2, c3]


def test_promethee_resultado_basico():
    cands = _criar_candidatos_teste()
    res = run_promethee(cands)
    assert isinstance(res, PrometheeResult)
    assert len(res.leaving_flows) == 3
    assert len(res.entering_flows) == 3
    assert len(res.net_flows) == 3
    assert res.best_candidate in cands
    assert 0 <= res.best_index < 3
    # Postos (ranks): menor número = melhor alternativa
    assert len(res.ranks) == 3
    assert np.min(res.ranks) == 1
    assert np.max(res.ranks) == 3


def test_promethee_invariante_soma_zero_fluxos_liquidos():
    """Propriedade fundamental do PROMETHEE II: sum(Phi) == 0."""
    cands = _criar_candidatos_teste()
    for pref in ("linear", "usual", "gaussian"):
        res = run_promethee(cands, preference_function=pref)
        soma = float(np.sum(res.net_flows))
        assert abs(soma) < 1e-12, f"Soma dos fluxos liquidos deve ser zero no modo {pref}: {soma}"


def test_promethee_invariante_fluxos_positivos_e_negativos_limitados():
    """Fluxos positivos e negativos ficam em [0, 1]; fluxo líquido fica em [-1, 1]."""
    cands = _criar_candidatos_teste()
    res = run_promethee(cands)
    assert np.all(res.leaving_flows >= 0.0)
    assert np.all(res.leaving_flows <= 1.0)
    assert np.all(res.entering_flows >= 0.0)
    assert np.all(res.entering_flows <= 1.0)
    assert np.all(res.net_flows >= -1.0)
    assert np.all(res.net_flows <= 1.0)


def test_promethee_dominancia_estrita():
    """Alternativa que domina outra em todos os critérios deve ter fluxo líquido estritamente maior."""
    fraca = TopsisCandidate(
        lower_tank_vol=1000.0,
        water_saved_m3_yr=20.0,
        vpl_brl=1000.0,
        co2_saved_kg_lifetime=-1000.0,
        potential_savings_pct=10.0,
        overflow_m3_yr=100.0,
        discounted_payback_years=15.0,
        irr_pct=5.0,
        potable_consumed_m3_yr=200.0,
    )
    forte = TopsisCandidate(
        lower_tank_vol=2000.0,
        water_saved_m3_yr=180.0,
        vpl_brl=50000.0,
        co2_saved_kg_lifetime=-100.0,
        potential_savings_pct=90.0,
        overflow_m3_yr=5.0,
        discounted_payback_years=2.0,
        irr_pct=40.0,
        potable_consumed_m3_yr=20.0,
    )
    res = run_promethee([fraca, forte])
    assert res.best_index == 1
    assert res.net_flows[1] > res.net_flows[0]
    assert res.ranks[1] == 1
    assert res.ranks[0] == 2


def test_promethee_casos_de_borda():
    """Testa casos de 0 alternativas, 1 alternativa e alternativas idênticas."""
    with pytest.raises(ValueError, match="vazia"):
        run_promethee([])

    cand = _criar_candidatos_teste()[0]
    res_1 = run_promethee([cand])
    assert res_1.best_index == 0
    assert float(res_1.net_flows[0]) == 0.0
    assert res_1.ranks[0] == 1

    # Alternativas idênticas
    res_ident = run_promethee([cand, cand])
    assert np.allclose(res_ident.net_flows, 0.0)


def test_promethee_pesos_de_eixo_de_criterio_e_legados():
    """Aceita 4 pesos de eixo, 8 de critério e os 3 de eixo de antes da 0.2.0; recusa os 7 do modelo antigo."""
    cands = _criar_candidatos_teste()
    res_4 = run_promethee(cands, weights=[0.4, 0.3, 0.2, 0.1])
    assert isinstance(res_4, PrometheeResult)

    res_8 = run_promethee(cands, weights=[0.2, 0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.1])
    assert isinstance(res_8, PrometheeResult)
    assert abs(float(np.sum(res_8.net_flows))) < 1e-12

    # Três eixos (projetos até a 0.1.0): o estrutural recebe a média, como no TOPSIS.
    res_3 = run_promethee(cands, weights=[0.5, 0.3, 0.2])
    res_3_em_4 = run_promethee(cands, weights=[0.5, 0.3, 0.2, (0.5 + 0.3 + 0.2) / 3.0])
    assert np.allclose(res_3.net_flows, res_3_em_4.net_flows)

    with pytest.raises(ValueError, match="oito critérios"):
        run_promethee(cands, weights=[0.2, 0.1, 0.25, 0.15, 0.1, 0.1, 0.1])
