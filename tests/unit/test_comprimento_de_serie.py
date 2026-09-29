"""A análise que responde se a série de chuva basta para o projeto.

O método é o de Geraldi e Ghisi: subséries deslizantes, comparação com a série
inteira, e o menor comprimento que reproduz o resultado na maior parte das
janelas — e o mantém nos comprimentos maiores.
"""
import os
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from netuno.core.comprimento_de_serie import (  # noqa: E402
    DIAS_NO_ANO, analisar, volume_ideal,
)

PROJETO = dict(area=100.0, runoff_coeff=0.80, discard_mm=2.0, discard_mode=1,
               total_demand_per_day=600.0, rainwater_share=0.30)


def serie_regular(anos, mm_por_dia=5.0):
    """Chuva igual todo dia: toda janela tem de reproduzir a série inteira."""
    return np.full(anos * DIAS_NO_ANO, mm_por_dia, dtype=float)


def test_serie_constante_basta_com_um_ano():
    r = analisar(serie_regular(6), PROJETO, volume_maximo_l=6000.0, passo_l=1000.0)
    assert r.comprimento_representativo_anos == 1
    assert r.serie_e_representativa
    assert r.frequencia_por_comprimento[1] == 100.0
    assert "é representativa" in r.resumo()


def test_a_analise_recusa_serie_curta_demais():
    with pytest.raises(ValueError, match="dois anos"):
        analisar(serie_regular(1), PROJETO)


def test_o_volume_ideal_e_o_primeiro_abaixo_do_limiar():
    serie = serie_regular(4)
    volumes = [1000.0, 2000.0, 3000.0, 4000.0]
    escolhido, potenciais = volume_ideal(serie, volumes, 1.0, PROJETO)
    assert escolhido in volumes
    # O ganho no volume eleito já está abaixo do limiar declarado.
    anterior = volumes[volumes.index(escolhido) - 1]
    ganho = (potenciais[escolhido] - potenciais[anterior]) / ((escolhido - anterior) / 1000.0)
    assert ganho <= 1.0


def test_a_amostragem_e_reproduzivel_com_a_mesma_semente():
    serie = np.random.default_rng(3).gamma(0.6, 8.0, 12 * DIAS_NO_ANO)
    comum = dict(volume_maximo_l=8000.0, passo_l=2000.0, amostra_por_comprimento=3)
    a = analisar(serie, PROJETO, semente=7, **comum)
    b = analisar(serie, PROJETO, semente=7, **comum)
    assert a.frequencia_por_comprimento == b.frequencia_por_comprimento
    assert a.janelas_por_comprimento[1] == 3


def test_a_amostragem_nao_inventa_janela_alem_das_que_existem():
    serie = np.random.default_rng(5).gamma(0.6, 8.0, 5 * DIAS_NO_ANO)
    r = analisar(serie, PROJETO, volume_maximo_l=6000.0, passo_l=2000.0,
                 amostra_por_comprimento=50)
    # Com cinco anos, o comprimento de quatro anos só tem duas janelas possíveis.
    assert r.janelas_por_comprimento[4] == 2
    assert r.janelas_por_comprimento[1] == 5


def test_o_comprimento_tem_de_se_manter_nos_maiores():
    """Um acerto isolado num comprimento curto não vale recomendação."""
    serie = np.random.default_rng(11).gamma(0.5, 9.0, 10 * DIAS_NO_ANO)
    r = analisar(serie, PROJETO, volume_maximo_l=6000.0, passo_l=2000.0, confianca_pct=90.0)
    if r.comprimento_representativo_anos is not None:
        maiores = range(r.comprimento_representativo_anos, r.anos_da_serie)
        assert all(r.frequencia_por_comprimento[a] >= 90.0 for a in maiores)


def test_serie_que_nao_estabiliza_avisa_em_vez_de_afirmar():
    r = analisar(serie_regular(4), PROJETO, volume_maximo_l=6000.0, passo_l=1000.0,
                 confianca_pct=100.0, tolerancia_pp=0.0, tolerancia_passos=0)
    if r.comprimento_representativo_anos is None:
        assert not r.serie_e_representativa
        assert "provisório" in r.resumo()


def test_a_serie_do_tutorial_estabiliza_dentro_dos_trinta_anos():
    sys.path.insert(0, os.path.join(RAIZ, "manual"))
    from gerar_tabelas import _config_tutorial, _serie
    r = analisar(_serie(), dict(_config_tutorial()), volume_maximo_l=12000.0,
                 passo_l=1000.0, limiar_ganho_pct_m3=1.0, amostra_por_comprimento=5)
    assert r.volume_ideal_l == pytest.approx(4000.0)
    assert r.potencial_no_ideal_pct == pytest.approx(27.12, abs=0.01)
    assert r.comprimento_representativo_anos is not None
    assert 1 <= r.comprimento_representativo_anos <= 30
