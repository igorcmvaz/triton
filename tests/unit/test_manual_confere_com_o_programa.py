"""Os números impressos no manual são os números que o programa produz.

Um manual de quatrocentas páginas envelhece em silêncio. A correção da energia de
bombeamento desta versão mudou o consumo da motobomba em 65%: num manual separado do
código, esse número ficaria errado por anos, e ninguém saberia.

A saída é fechar o laço. Cada valor impresso no manual tem asserção aqui. Quando o
programa muda, o teste falha e aponta **qual página** corrigir, em vez de o manual
passar a mentir.

Este arquivo cobre o capítulo 23, que é o caso resolvido dia a dia — o capítulo do
qual todos os outros dependem. Os demais capítulos entram aqui conforme forem
escritos.
"""

from __future__ import annotations

import os
import re

import numpy as np
import pytest

from netuno.core.simulation import run_single_simulation

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
CAP23 = os.path.join(MANUAL, "partes", "23_balanco_diario.md")
TABELA23 = os.path.join(MANUAL, "partes", "_tabelas", "cap23_dez_dias.md")

#: O caso do capítulo 23, exatamente como declarado em manual/gerar_tabelas.py.
CHUVA = [0.0, 12.4, 1.6, 0.0, 0.0, 28.0, 5.2, 0.0, 41.0, 0.0]
ENTRADA = dict(
    lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.85,
    discard_mm=2.0, discard_mode=1,
    total_demand_per_day=200.0, rainwater_share=0.40,
)


@pytest.fixture(scope="module")
def caso():
    return run_single_simulation(
        precip_data=np.array(CHUVA, dtype=float),
        store_daily_details=True, **ENTRADA
    )


def _numeros_da_tabela():
    """Lê os números da tabela publicada, sem depender de gerá-la de novo."""
    if not os.path.exists(TABELA23):
        pytest.skip("tabela do capítulo 23 ainda não gerada")
    texto = open(TABELA23, encoding="utf-8").read()
    linhas = [l for l in texto.split(chr(10)) if l.startswith("| ") and "|" in l]
    dias = []
    for l in linhas:
        celulas = [c.strip() for c in l.strip("|").split("|")]
        if not celulas or not celulas[0].isdigit():
            continue
        # O separador de milhar da tabela e espaco inquebravel, para o numero
        # nao quebrar de linha na impressao.
        dias.append([c.replace(chr(160), "").replace(" ", "").replace(",", ".")
                     for c in celulas])
    return dias, texto


# ────────────────────── o caso resolvido do capítulo 23 ───────────────────────

def test_o_potencial_do_caso_resolvido(caso):
    """Impresso no capítulo 23: «potencial obtido, 36,0%»."""
    assert caso.potential_potable_savings_pct == pytest.approx(36.0, abs=0.05)


def test_a_demanda_pluvial_diaria(caso):
    """Impresso: «200 × 0,40 = 80 L/dia»."""
    assert caso.daily_results[0].pluvial_demand_liters == pytest.approx(80.0)


def test_o_dia_1_e_de_atendimento_nulo(caso):
    """Impresso: reservatório vazio, dia nulo, 200 L da rede."""
    d = caso.daily_results[0]
    assert d.satisfaction_type == 0
    assert d.pluvial_consumed_liters == pytest.approx(0.0)
    assert d.potable_consumed_liters == pytest.approx(200.0)


def test_o_dia_3_se_perde_inteiro(caso):
    """Impresso: choveu 1,6 mm, a lâmina é 2,0 mm, capta-se zero.

    É a armadilha que o capítulo existe para ensinar: perde-se o dia inteiro, e
    não a diferença.
    """
    d = caso.daily_results[2]
    assert d.precip_mm == pytest.approx(1.6)
    assert d.eff_precip_mm == pytest.approx(0.0)
    assert d.harvested_liters == pytest.approx(0.0)


def test_o_dia_6_extravasa_antes_de_consumir(caso):
    """Impresso: 2.210 L captados, 774 L extravasados, 1.920 L no reservatório.

    Se a ordem fosse invertida — consumir antes de extravasar — o reservatório
    terminaria cheio, com 2.000 L, e o extravasamento seria 80 L menor.
    """
    d = caso.daily_results[5]
    assert d.harvested_liters == pytest.approx(2210.0, abs=1.0)
    assert d.spilled_liters == pytest.approx(774.0, abs=1.0)
    assert d.lower_tank_end_liters == pytest.approx(1920.0, abs=1.0)


def test_o_dia_9_extravasa_mais_que_o_reservatorio(caso):
    """Impresso: 3.315 L captados e 3.155 L extravasados."""
    d = caso.daily_results[8]
    assert d.harvested_liters == pytest.approx(3315.0, abs=1.0)
    assert d.spilled_liters == pytest.approx(3155.0, abs=1.0)
    assert d.spilled_liters > ENTRADA["lower_tank_vol"]


def test_as_somas_impressas(caso):
    """Impresso: 6.681 L captados, 4.121 L extravasados, 720 L consumidos."""
    captado = sum(d.harvested_liters for d in caso.daily_results)
    extravasado = sum(d.spilled_liters for d in caso.daily_results)
    consumido = sum(d.pluvial_consumed_liters for d in caso.daily_results)
    assert captado == pytest.approx(6681.0, abs=1.0)
    assert extravasado == pytest.approx(4121.0, abs=1.0)
    assert consumido == pytest.approx(720.0, abs=1.0)


def test_o_balanco_do_caso_fecha(caso):
    """Impresso: resíduo zero."""
    captado = sum(d.harvested_liters for d in caso.daily_results)
    extravasado = sum(d.spilled_liters for d in caso.daily_results)
    consumido = sum(d.pluvial_consumed_liters for d in caso.daily_results)
    final = caso.daily_results[-1].lower_tank_end_liters
    assert captado - extravasado - consumido - final == pytest.approx(0.0, abs=0.5)


def test_os_indicadores_impressos(caso):
    assert caso.avg_pluvial_consumed_l_day == pytest.approx(72.0, abs=0.05)
    assert caso.avg_potable_consumed_l_day == pytest.approx(128.0, abs=0.05)
    assert caso.pct_days_full_satisfaction == pytest.approx(90.0, abs=0.5)
    assert caso.pct_days_null_satisfaction == pytest.approx(10.0, abs=0.5)


# ─────────────── a tabela publicada bate com o que o programa faz ─────────────

def test_a_tabela_publicada_tem_os_dez_dias():
    dias, _ = _numeros_da_tabela()
    assert len(dias) == 10


def test_cada_linha_da_tabela_publicada_bate_com_a_simulacao(caso):
    """Se alguém editar a tabela à mão, este teste pega."""
    dias, _ = _numeros_da_tabela()
    for i, celulas in enumerate(dias):
        d = caso.daily_results[i]
        assert float(celulas[1]) == pytest.approx(d.precip_mm, abs=0.05), f"dia {i+1} chuva"
        assert float(celulas[3]) == pytest.approx(d.eff_precip_mm, abs=0.05), f"dia {i+1} efetiva"
        assert float(celulas[4]) == pytest.approx(d.harvested_liters, abs=1.0), f"dia {i+1} captado"
        assert float(celulas[6]) == pytest.approx(d.pluvial_consumed_liters, abs=1.0), f"dia {i+1} consumido"
        assert float(celulas[7]) == pytest.approx(d.spilled_liters, abs=1.0), f"dia {i+1} extravasado"


# ──────────────── o texto do capítulo não contradiz os números ───────────────

def test_o_capitulo_cita_os_numeros_que_o_programa_produz():
    """Os valores escritos no corpo do texto, e não só na tabela."""
    if not os.path.exists(CAP23):
        pytest.skip("capítulo 23 ainda não escrito")
    texto = open(CAP23, encoding="utf-8").read()
    for esperado in ("36,0%", "2.210 L", "774 L", "3.315 L", "3.155 L",
                     "6.681 L", "4.121 L", "720 L", "1.840 L", "80 L/dia"):
        assert esperado in texto, f"o capítulo 23 não cita {esperado}"


def test_o_capitulo_declara_a_divergencia_com_o_netuno_4():
    """Estudo de replicação que esconde a divergência não serve para nada."""
    if not os.path.exists(CAP23):
        pytest.skip("capítulo 23 ainda não escrito")
    texto = open(CAP23, encoding="utf-8").read()
    assert "Netuno 4" in texto
    assert "limiar" in texto
    assert re.search(r"2,3 a 2,7 pontos percentuais", texto)


def test_o_capitulo_declara_o_que_o_modelo_nao_representa():
    if not os.path.exists(CAP23):
        pytest.skip("capítulo 23 ainda não escrito")
    texto = open(CAP23, encoding="utf-8").read()
    assert "não representa" in texto or "não há sub-passo" in texto.lower()


# ══════════════════════════════════════════════════════════════════════════════
# O tutorial da Parte 2: residência unifamiliar em Florianópolis
# ══════════════════════════════════════════════════════════════════════════════
#
# Um projeto só, que atravessa dez capítulos. Cada número impresso tem asserção
# aqui, porque é assim que o manual não envelhece em silêncio.

SERIE_TUTORIAL = os.path.join(RAIZ, "data", "rainfall", "Florianopolis1.csv")
TUTORIAL = dict(
    area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
    total_demand_per_day=600.0, rainwater_share=0.40,
)


@pytest.fixture(scope="module")
def serie_tutorial():
    from netuno.core.parser import load_precipitation
    if not os.path.exists(SERIE_TUTORIAL):
        pytest.skip("série de Florianópolis não instalada")
    return load_precipitation(SERIE_TUTORIAL)[: 30 * 365]


def _tutorial(serie, volume):
    return run_single_simulation(
        precip_data=serie, lower_tank_vol=float(volume), **TUTORIAL)


def test_a_serie_do_tutorial_e_a_que_o_capitulo_4_descreve(serie_tutorial):
    """Impresso no capítulo 4: 30 anos, 1.795 mm/ano, chuva em 46% dos dias."""
    anos = len(serie_tutorial) / 365.25
    assert anos == pytest.approx(30.0, abs=0.1)
    assert serie_tutorial.sum() / anos == pytest.approx(1795.0, abs=5.0)
    assert (serie_tutorial > 0.1).mean() * 100 == pytest.approx(46.0, abs=1.0)


def test_o_descarte_atinge_sete_por_cento_dos_dias(serie_tutorial):
    """Impresso no capítulo 4: 7% dos dias têm chuva abaixo da lâmina."""
    abaixo = ((serie_tutorial > 0.1) & (serie_tutorial <= 2.0)).mean() * 100
    assert abaixo == pytest.approx(7.0, abs=1.0)


def test_a_agua_bruta_e_o_dobro_da_demanda(serie_tutorial):
    """Impresso no capítulo 5: 229 m³ de oferta bruta contra 88 m³ de demanda."""
    anos = len(serie_tutorial) / 365.25
    bruta = serie_tutorial.sum() / anos * TUTORIAL["area"] * TUTORIAL["runoff_coeff"] / 1000.0
    demanda = TUTORIAL["total_demand_per_day"] * TUTORIAL["rainwater_share"] * 365.25 / 1000.0
    assert bruta == pytest.approx(229.0, abs=2.0)
    assert demanda == pytest.approx(88.0, abs=1.0)
    assert bruta > 2 * demanda


def test_a_primeira_simulacao_do_capitulo_6(serie_tutorial):
    """Impresso: 34,92% com 3.000 L, 303 L/dia extravasados, 85,7% de dias plenos."""
    r = _tutorial(serie_tutorial, 3000)
    assert r.potential_potable_savings_pct == pytest.approx(34.92, abs=0.05)
    assert r.avg_spilled_l_day == pytest.approx(303.0, abs=1.0)
    assert r.pct_days_full_satisfaction == pytest.approx(85.7, abs=0.1)


def test_o_extravasamento_supera_o_consumo_pretendido(serie_tutorial):
    """Impresso no capítulo 6: extravasa mais do que os 240 L/dia pretendidos."""
    r = _tutorial(serie_tutorial, 3000)
    assert r.avg_spilled_l_day > 240.0


@pytest.mark.parametrize(("volume", "potencial"), [
    (1000, 25.32), (2000, 31.91), (3000, 34.92), (5000, 37.46),
    (8000, 38.85), (12000, 39.62), (20000, 39.98),
])
def test_a_curva_de_varredura_do_capitulo_7(serie_tutorial, volume, potencial):
    """Cada linha da tabela impressa no capítulo 7."""
    r = _tutorial(serie_tutorial, volume)
    assert r.potential_potable_savings_pct == pytest.approx(potencial, abs=0.05)


def test_o_potencial_nunca_passa_da_fracao_atendivel(serie_tutorial):
    """A lição central do capítulo 5: a fração é o teto, e nada a ultrapassa."""
    teto = TUTORIAL["rainwater_share"] * 100.0
    for v in (1000, 5000, 20000, 100000):
        assert _tutorial(serie_tutorial, v).potential_potable_savings_pct <= teto


@pytest.mark.parametrize(("limiar", "ideal"), [(3.0, 4000), (1.0, 5000), (0.5, 7000)])
def test_o_limiar_decide_o_volume_ideal(serie_tutorial, limiar, ideal):
    """Impresso no capítulo 7: o limiar é escolha do autor, e muda a resposta."""
    from netuno.core.simulation import run_sweep_simulation
    r = run_sweep_simulation(
        precip_data=serie_tutorial, lower_tank_max=20000.0, lower_tank_step=1000.0,
        delta_ideal_threshold=limiar, **TUTORIAL)
    assert r.optimal_lower_tank_vol == pytest.approx(ideal)


def test_o_volume_maior_custa_muito_mais_por_pouco_ganho(serie_tutorial):
    """Impresso no capítulo 7: 3,3× o preço e 3,6× o carbono por 2,53 pontos."""
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca

    r5 = _tutorial(serie_tutorial, 5000)
    r20 = _tutorial(serie_tutorial, 20000)
    assert r20.potential_potable_savings_pct - r5.potential_potable_savings_pct \
        == pytest.approx(2.53, abs=0.05)

    p5 = estimate_tank_price(5000.0, "CONCRETO")
    p20 = estimate_tank_price(20000.0, "CONCRETO")
    assert p20 / p5 == pytest.approx(3.3, abs=0.1)

    cfg = EnvironmentalConfig()
    cfg.lower_material_key = "CONCRETO"
    c5 = calculate_lca(5000.0, r5.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    c20 = calculate_lca(20000.0, r20.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    assert c20 / c5 == pytest.approx(3.6, abs=0.1)


def test_os_capitulos_do_tutorial_citam_os_numeros_do_programa():
    """Os valores escritos no corpo dos capítulos 4 a 7."""
    esperados = {
        "04_o_projeto_e_a_chuva.md": ("150 m²", "0,85", "2,0 mm", "229 m³"),
        "05_a_edificacao_e_a_demanda.md": ("600 L/dia", "240 L/dia", "40%", "88"),
        "06_a_primeira_simulacao.md": ("34,92%", "303 L/dia", "85,7%", "3.000"),
        "07_escolher_o_volume.md": ("5.000 L", "37,46%", "92,9%", "39,98%"),
    }
    for arquivo, termos in esperados.items():
        caminho = os.path.join(MANUAL, "partes", arquivo)
        if not os.path.exists(caminho):
            pytest.skip(f"{arquivo} ainda não escrito")
        texto = open(caminho, encoding="utf-8").read()
        for termo in termos:
            assert termo in texto, f"{arquivo} não cita {termo}"
