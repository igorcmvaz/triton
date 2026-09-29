"""O modelo calibrado de CAPEX e OPEX por tipologia de edificação.

Substitui `tests/test_cost_calibrated.py`, que **não era um teste**: tinha zero
funções `test_`, zero asserções, e terminava imprimindo «[SUCESSO] Todos os
testes passaram com perfeita conformidade técnica e matemática» qualquer que
fosse o resultado. Um arquivo assim é pior que a ausência de teste, porque ocupa
o lugar de um e passa a impressão de cobertura: se o modelo devolvesse absurdo,
ele imprimiria SUCESSO do mesmo jeito.

O que ele exercitava de fato — o modelo calibrado, com as cinco tipologias e os
fatores regionais SINAPI/CUB — não tinha nenhuma verificação real. Passa a ter.
"""

from __future__ import annotations

import pytest

from netuno.core.cost_estimates import (
    REGIONAL_FACTORS_BY_UF,
    TYPOLOGY_COST_CONFIGS,
    estimate_calibrated_capex_opex,
    estimate_preliminary_capex,
)

#: As cinco tipologias do modelo calibrado, da casa térrea ao bloco multifamiliar.
TIPOLOGIAS = ("UTI", "UTG", "MSG", "MFH", "MFL")


def _orcar(tipologia: str = "UTI", volume_l: float = 5000.0, uf: str = "SP"):
    return estimate_calibrated_capex_opex(typology=tipologia, volume_l=volume_l, uf=uf)


# ───────────────────────────── o contrato do retorno ───────────────────────────

def test_o_orcamento_traz_todas_as_parcelas_declaradas():
    """Um total sem as parcelas não é auditável: não dá para conferir de onde veio."""
    r = _orcar()
    for campo in (
        "c_inf", "c_sup", "c_pump", "c_pipes", "c_panel", "c_sensors",
        "c_treatment", "c_air_gap", "labor_cost",
        "capex_base_brl", "capex_total_brl", "f_regional",
        "opex_fixed_annual_brl", "opex_variable_per_m3_brl",
    ):
        assert campo in r, campo
        assert isinstance(r[campo], (int, float)), campo


def test_as_parcelas_somam_o_capex_base():
    """Se as partes não somam o todo, alguma entrou ou saiu sem aparecer."""
    r = _orcar()
    partes = (
        r["c_inf"] + r["c_sup"] + r["c_pump"] + r["c_pipes"]
        + r["c_accessories_total"] + r["labor_cost"]
    )
    assert partes == pytest.approx(r["capex_base_brl"], rel=1e-6)


def test_os_acessorios_somam_os_quatro_subsistemas():
    r = _orcar()
    assert r["c_accessories_total"] == pytest.approx(
        r["c_panel"] + r["c_sensors"] + r["c_treatment"] + r["c_air_gap"]
    )


def test_o_fator_regional_multiplica_a_base():
    for uf in ("SP", "RR", "RS", "AM"):
        r = _orcar(uf=uf)
        assert r["capex_total_brl"] == pytest.approx(r["capex_base_brl"] * r["f_regional"])


# ─────────────────────────── a escala das tipologias ───────────────────────────

def test_o_capex_cresce_com_o_porte_da_tipologia():
    """Da casa térrea ao bloco multifamiliar não há inversão.

    O bloco tem prumadas duplas, bomba principal e reserva, painel elétrico e
    shafts: custa mais, e o modelo tem de refletir isso monotonicamente.
    """
    valores = [_orcar(t)["capex_total_brl"] for t in TIPOLOGIAS]
    assert valores == sorted(valores), dict(zip(TIPOLOGIAS, valores))
    assert valores[-1] > 3 * valores[0]


def test_o_opex_fixo_cresce_com_o_porte():
    valores = [_orcar(t)["opex_fixed_annual_brl"] for t in TIPOLOGIAS]
    assert valores == sorted(valores)
    assert all(v > 0 for v in valores)


def test_toda_tipologia_do_banco_e_orcavel():
    """Acrescentar tipologia ao banco e esquecer o modelo derruba este teste."""
    for chave in TYPOLOGY_COST_CONFIGS:
        r = _orcar(chave)
        assert r["capex_total_brl"] > 0, chave
        assert r["typology_name"], chave


def test_o_capex_cresce_com_o_volume():
    valores = [_orcar("MFL", volume_l=v)["capex_total_brl"] for v in (1000, 5000, 20000)]
    assert valores == sorted(valores)


# ─────────────────────────────── fatores regionais ─────────────────────────────

def test_os_fatores_regionais_cobrem_as_27_unidades_da_federacao():
    assert len(REGIONAL_FACTORS_BY_UF) >= 27
    for uf, fator in REGIONAL_FACTORS_BY_UF.items():
        assert 0.7 <= float(fator) <= 1.6, (uf, fator)


def test_roraima_custa_mais_que_sao_paulo():
    """É o sentido do fator regional: logística encarece o Norte."""
    assert _orcar("MFL", 20000, "RR")["capex_total_brl"] > _orcar("MFL", 20000, "SP")["capex_total_brl"]


def test_uf_desconhecida_cai_no_fator_neutro():
    assert _orcar(uf="XX")["f_regional"] == pytest.approx(1.0)


# ────────────────────────── compatibilidade com a API antiga ───────────────────

def test_a_api_legada_continua_respondendo():
    """Projetos e chamadas antigas usam a assinatura posicional."""
    legado = estimate_preliminary_capex(5000, 500, True, 0.37, 1)
    assert legado["total"] > 0
    for campo in ("lower", "upper", "pump", "piping", "accessories", "labor"):
        assert campo in legado, campo


def test_a_api_legada_aceita_tipologia_e_uf():
    barato = estimate_preliminary_capex(5000, 500, True, typology="UTI", uf="SP")
    caro = estimate_preliminary_capex(5000, 500, True, typology="MFL", uf="RJ")
    assert caro["total"] > barato["total"]


def test_volume_nulo_nao_produz_capex_negativo():
    r = _orcar(volume_l=0.0)
    assert r["capex_total_brl"] >= 0.0
