"""O consumo sorteado dia a dia, e o que ele desloca no resultado.

O módulo existe para responder a Silva e Ghisi (2016) com o motor do Netuno 5.
Estes testes travam três coisas: o sorteio devolve a média e a dispersão pedidas,
o resultado é reproduzível com a semente, e — o achado que o módulo documenta —
o ruído do dia para o dia quase não move o resultado, ao passo que a incerteza do
nível do consumo move.
"""
import os
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from netuno.core.demanda_estocastica import (  # noqa: E402
    DISTRIBUICOES, PerfilDeConsumo, simular, sortear_demanda, sortear_media,
    volume_ideal_por_realizacao,
)

PROJETO = dict(area=100.0, runoff_coeff=0.80, discard_mm=2.0, discard_mode=1,
               rainwater_share=0.30)


def chuva(anos=8, semente=1):
    return np.random.default_rng(semente).gamma(0.6, 9.0, anos * 365)


@pytest.mark.parametrize("distribuicao", DISTRIBUICOES)
def test_o_sorteio_devolve_a_media_e_o_cv_pedidos(distribuicao):
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=25.0, distribuicao=distribuicao)
    valores = sortear_demanda(perfil, 40000, np.random.default_rng(2))
    assert float(np.mean(valores)) == pytest.approx(600.0, rel=0.02)
    cv = float(np.std(valores)) / float(np.mean(valores)) * 100.0
    assert cv == pytest.approx(25.0, rel=0.06)


def test_a_probabilidade_de_ausencia_zera_a_fracao_pedida_dos_dias():
    perfil = PerfilDeConsumo(media_l_dia=500.0, cv_pct=10.0,
                             probabilidade_de_ausencia_pct=12.0)
    valores = sortear_demanda(perfil, 50000, np.random.default_rng(3))
    assert float(np.mean(valores == 0.0)) == pytest.approx(0.12, abs=0.01)


def test_o_piso_e_o_teto_limitam_o_sorteio():
    perfil = PerfilDeConsumo(media_l_dia=400.0, cv_pct=60.0, distribuicao="normal",
                             minimo_l_dia=200.0, maximo_l_dia=600.0)
    valores = sortear_demanda(perfil, 5000, np.random.default_rng(4))
    assert valores.min() >= 200.0 and valores.max() <= 600.0


@pytest.mark.parametrize("perfil,mensagem", [
    (PerfilDeConsumo(media_l_dia=0.0), "positiva"),
    (PerfilDeConsumo(media_l_dia=100.0, cv_pct=-1.0), "negativo"),
    (PerfilDeConsumo(media_l_dia=100.0, probabilidade_de_ausencia_pct=120.0), "0 a 100"),
    (PerfilDeConsumo(media_l_dia=100.0, distribuicao="weibull"), "Distribuição desconhecida"),
    (PerfilDeConsumo(media_l_dia=100.0, minimo_l_dia=50.0, maximo_l_dia=10.0), "menor que o piso"),
    (PerfilDeConsumo(media_l_dia=100.0, incerteza_da_media_pct=-5.0), "não pode ser negativa"),
])
def test_perfil_implausivel_e_recusado(perfil, mensagem):
    with pytest.raises(ValueError, match=mensagem):
        perfil.validar()


def test_sem_variacao_o_sorteio_devolve_o_deterministico():
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0)
    r = simular(chuva(), 4000.0, perfil, PROJETO, realizacoes=3)
    assert r["potencial_pct"]["media"] == pytest.approx(r["deterministico"]["potencial_pct"], abs=0.01)
    assert r["potencial_pct"]["amplitude"] == pytest.approx(0.0, abs=0.001)


def test_a_mesma_semente_devolve_o_mesmo_resultado():
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=20.0, incerteza_da_media_pct=10.0)
    a = simular(chuva(), 4000.0, perfil, PROJETO, realizacoes=8, semente=9)
    b = simular(chuva(), 4000.0, perfil, PROJETO, realizacoes=8, semente=9)
    assert a["potencial_pct"] == b["potencial_pct"]


def test_o_ruido_diario_se_cancela_e_a_incerteza_do_nivel_nao():
    """O achado que o módulo documenta, e a razão de os dois parâmetros existirem.

    A comparação precisa de um sistema limitado pela oferta, que é onde o nível
    da demanda pesa. Num sistema com chuva sobrando o potencial é quase
    insensível à demanda, porque ela aparece no numerador e no denominador do
    indicador ao mesmo tempo — e é por isso que a série aqui é seca.
    """
    seca = np.random.default_rng(21).gamma(0.4, 3.0, 12 * 365)
    diario = simular(seca, 4000.0, PerfilDeConsumo(media_l_dia=600.0, cv_pct=25.0),
                     PROJETO, realizacoes=12)
    nivel = simular(seca, 4000.0,
                    PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0, incerteza_da_media_pct=15.0),
                    PROJETO, realizacoes=12)
    assert diario["potencial_pct"]["amplitude"] < 0.5
    assert nivel["potencial_pct"]["amplitude"] > 2 * diario["potencial_pct"]["amplitude"]


def test_com_chuva_sobrando_o_nivel_da_demanda_quase_nao_muda_o_potencial():
    """A outra metade do achado: o regime decide se a incerteza importa."""
    farta = np.random.default_rng(22).gamma(0.9, 12.0, 12 * 365)
    nivel = simular(farta, 12000.0,
                    PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0, incerteza_da_media_pct=15.0),
                    PROJETO, realizacoes=10)
    assert nivel["potencial_pct"]["amplitude"] < 1.0


def test_a_media_sorteada_respeita_a_incerteza_declarada():
    perfil = PerfilDeConsumo(media_l_dia=600.0, incerteza_da_media_pct=20.0)
    gerador = np.random.default_rng(6)
    medias = [sortear_media(perfil, gerador) for _ in range(4000)]
    assert float(np.mean(medias)) == pytest.approx(600.0, rel=0.03)
    assert float(np.std(medias)) == pytest.approx(120.0, rel=0.08)
    assert sortear_media(PerfilDeConsumo(media_l_dia=600.0), gerador) == 600.0


def test_o_volume_ideal_sai_da_grade_e_varia_com_a_incerteza():
    volumes = [1000.0 * i for i in range(1, 9)]
    r = volume_ideal_por_realizacao(
        chuva(anos=10), PerfilDeConsumo(media_l_dia=600.0, cv_pct=15.0,
                                        incerteza_da_media_pct=20.0),
        PROJETO, volumes_l=volumes, realizacoes=6)
    assert set(r["volumes_distintos"]) <= set(volumes)
    assert r["volume_ideal_l"]["p5"] <= r["volume_ideal_l"]["p95"]
