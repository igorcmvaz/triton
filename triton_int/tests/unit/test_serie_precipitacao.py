# -*- coding: utf-8 -*-
"""Validação da série diária de chuva: vazia, NaN, negativa (já havia) e, agora, chuva impossível e anos inteiros.

Série válida continua válida: os avisos de comprimento e de escala não recusam nada, para não mudar resultados.
"""
import numpy as np
import pytest

from triton.core.simulation import (
    LIMITE_DE_CHUVA_DIARIA_MM, avisos_da_serie_precipitacao, validar_serie_precipitacao)


def _serie(dias, total_anual=1200.0):
    return np.full(dias, total_anual / 365.25)


@pytest.mark.parametrize("dias", [365, 366, 730, 1461, 3652, 3653, 10957])
def test_anos_inteiros_nao_geram_aviso(dias):
    avisos = []
    validar_serie_precipitacao(_serie(dias), avisos)
    assert avisos == []


@pytest.mark.parametrize("dias", [400, 1000, 8000, 8780])
def test_comprimento_fora_de_anos_inteiros_avisa_sem_recusar(dias):
    avisos = []
    validar_serie_precipitacao(_serie(dias), avisos)           # não levanta
    assert len(avisos) == 1 and "anos inteiros" in avisos[0] and str(dias) in avisos[0]


def test_chuva_diaria_impossivel_levanta_com_o_dia():
    s = _serie(730)
    s[41] = 2500.0
    with pytest.raises(ValueError, match=r"acima de 2000 mm.*dia 42"):
        validar_serie_precipitacao(s)
    s[41] = LIMITE_DE_CHUVA_DIARIA_MM                          # no limite ainda passa
    validar_serie_precipitacao(s)


@pytest.mark.parametrize("total", [5.0, 20000.0])
def test_total_anual_implausivel_avisa(total):
    avisos = []
    validar_serie_precipitacao(_serie(1461, total), avisos)
    assert len(avisos) == 1 and "total anual medio" in avisos[0]


def test_sem_lista_de_avisos_o_comportamento_antigo_nao_muda():
    validar_serie_precipitacao(_serie(1000))
    validar_serie_precipitacao([0.0, 1.0, 2.5])
    for ruim, trecho in (([], "vazia"), ([1.0, float("nan")], "sem valor numerico"), ([1.0, -999.0], "negativo")):
        with pytest.raises(ValueError, match=trecho):
            validar_serie_precipitacao(ruim)


def test_avisos_nao_alteram_a_serie():
    s = _serie(1000)
    antes = s.copy()
    validar_serie_precipitacao(s, [])
    assert np.array_equal(s, antes)
