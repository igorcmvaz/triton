"""Entrada fisicamente impossível é rejeitada, e não simulada.

A simulação aceitava área negativa, coeficiente de escoamento negativo e volume
negativo, e devolvia **potencial de economia negativo**:

| Entrada | Potencial devolvido |
| :--- | ---: |
| volume de −1.000 L | −166,67% |
| área de −100 m² | −49,91% |
| coeficiente de −0,5 | −35,23% |

Um percentual de economia negativo não significa nada, e o programa não parava
ali: o número entrava no módulo econômico como economia de água, na avaliação de
ciclo de vida como emissão evitada, e no relatório como resultado.

Não se corrige calando o valor. Área negativa é erro de digitação, e quem digitou
precisa ver — por isso a validação levanta erro nomeando o campo e dizendo por
quê, em vez de corrigir por baixo dos panos.
"""

from __future__ import annotations

import numpy as np
import pytest

from netuno.core.simulation import run_single_simulation, validar_parametros_fisicos

_VALIDO = dict(
    area=120.0,
    runoff_coeff=0.85,
    discard_mm=2.0,
    total_demand_per_day=600.0,
    rainwater_share=0.4,
    upper_tank_vol=500.0,
)


@pytest.fixture(scope="module")
def chuva():
    rng = np.random.default_rng(42)
    return np.clip(rng.gamma(0.6, 9.0, 730), 0, None)


def _simular(chuva, volume=5000.0, **trocas):
    kw = dict(_VALIDO)
    kw.update(trocas)
    return run_single_simulation(
        precip_data=chuva, lower_tank_vol=volume, pumping_threshold=50.0, **kw
    )


# ────────────────────────── o que tem de ser rejeitado ─────────────────────────

@pytest.mark.parametrize(
    ("campo", "valor", "termo"),
    [
        ("area", -100.0, "Area"),
        ("runoff_coeff", -0.5, "escoamento"),
        ("runoff_coeff", 1.8, "escoamento"),
        ("discard_mm", -5.0, "descarte"),
        ("total_demand_per_day", -80.0, "Demanda"),
        ("rainwater_share", 2.5, "Fracao"),
        ("rainwater_share", -0.3, "Fracao"),
        ("upper_tank_vol", -200.0, "superior"),
    ],
)
def test_parametro_impossivel_e_rejeitado(chuva, campo, valor, termo):
    with pytest.raises(ValueError, match=termo):
        _simular(chuva, **{campo: valor})


def test_volume_negativo_e_rejeitado(chuva):
    """Devolvia −166,67% de economia, e o número seguia para o relatório."""
    with pytest.raises(ValueError, match="negativo"):
        _simular(chuva, volume=-1000.0)


def test_a_mensagem_diz_o_campo_e_o_valor(chuva):
    """Erro que não nomeia o campo obriga o usuário a caçar o problema."""
    with pytest.raises(ValueError) as erro:
        _simular(chuva, runoff_coeff=1.8)
    texto = str(erro.value)
    assert "1.8" in texto
    assert "0,80" in texto and "0,95" in texto     # a faixa usual, como orientação


# ─────────────────────────── o que continua válido ─────────────────────────────

def test_volume_zero_continua_valido(chuva):
    """É a referência «sem sistema» da varredura, e não pode ser rejeitada."""
    r = _simular(chuva, volume=0.0)
    assert r.potential_potable_savings_pct == pytest.approx(0.0)


@pytest.mark.parametrize("coef", [0.0, 0.5, 0.8, 0.95, 1.0])
def test_a_faixa_valida_do_coeficiente_passa_inteira(chuva, coef):
    """Os extremos 0 e 1 são legítimos: telhado impermeável ideal e captação nula."""
    assert _simular(chuva, runoff_coeff=coef).potential_potable_savings_pct >= 0.0


def test_sem_reservatorio_superior_continua_valido(chuva):
    assert _simular(chuva, upper_tank_vol=0.0) is not None


def test_demanda_zero_continua_valida(chuva):
    """Edificação sem consumo é caso-limite legítimo, e dá economia nula."""
    assert _simular(chuva, total_demand_per_day=0.0).potential_potable_savings_pct == pytest.approx(0.0)


# ────────────────── o resultado sempre faz sentido dimensional ─────────────────

def test_o_potencial_fica_sempre_entre_zero_e_cem(chuva):
    """A invariante que a validação existe para garantir.

    Antes, três entradas diferentes produziam percentual fora de [0, 100], e
    nenhuma delas era detectada.
    """
    for volume in (0.0, 500.0, 2000.0, 5000.0, 20000.0):
        for coef in (0.0, 0.5, 0.85, 1.0):
            for area in (0.0, 50.0, 400.0):
                r = _simular(chuva, volume=volume, runoff_coeff=coef, area=area)
                assert 0.0 <= r.potential_potable_savings_pct <= 100.0, (volume, coef, area)


def test_o_validador_e_chamavel_isoladamente():
    """Serve à interface, que pode conferir antes de rodar a simulação inteira."""
    validar_parametros_fisicos(
        lower_tank_vol=5000.0, area=120.0, runoff_coeff=0.85,
        discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4,
    )
    with pytest.raises(ValueError):
        validar_parametros_fisicos(
            lower_tank_vol=5000.0, area=-1.0, runoff_coeff=0.85,
            discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4,
        )
