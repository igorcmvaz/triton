"""Os números impressos no manual são os números que o programa produz.

Um manual de quatrocentas páginas envelhece em silêncio. A correção da energia de
bombeamento desta versão mudou o consumo da motobomba em 65%: num manual separado do
código, esse número ficaria errado por anos, e ninguém saberia.

A saída é fechar o laço. Cada valor impresso no manual tem asserção aqui. Quando o
programa muda, o teste falha e aponta **qual página** corrigir, em vez de o manual
passar a mentir.

Este arquivo cobre o capítulo 13, que é o caso resolvido dia a dia — o capítulo do
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
CAP13 = os.path.join(MANUAL, "partes", "13_balanco_diario.md")
TABELA13 = os.path.join(MANUAL, "partes", "_tabelas", "cap13_dez_dias.md")

#: O caso do capítulo 13, exatamente como declarado em manual/gerar_tabelas.py.
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
    if not os.path.exists(TABELA13):
        pytest.skip("tabela do capítulo 13 ainda não gerada")
    texto = open(TABELA13, encoding="utf-8").read()
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


# ────────────────────── o caso resolvido do capítulo 13 ───────────────────────

def test_o_potencial_do_caso_resolvido(caso):
    """Impresso no capítulo 13: «potencial obtido, 36,0%»."""
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
    if not os.path.exists(CAP13):
        pytest.skip("capítulo 13 ainda não escrito")
    texto = open(CAP13, encoding="utf-8").read()
    for esperado in ("36,0%", "2.210 L", "774 L", "3.315 L", "3.155 L",
                     "6.681 L", "4.121 L", "720 L", "1.840 L", "80 L/dia"):
        assert esperado in texto, f"o capítulo 13 não cita {esperado}"


def test_o_capitulo_declara_a_divergencia_com_o_netuno_4():
    """Estudo de replicação que esconde a divergência não serve para nada."""
    if not os.path.exists(CAP13):
        pytest.skip("capítulo 13 ainda não escrito")
    texto = open(CAP13, encoding="utf-8").read()
    assert "Netuno 4" in texto
    assert "limiar" in texto
    assert re.search(r"2,3 a 2,7 pontos percentuais", texto)


def test_o_capitulo_declara_o_que_o_modelo_nao_representa():
    if not os.path.exists(CAP13):
        pytest.skip("capítulo 13 ainda não escrito")
    texto = open(CAP13, encoding="utf-8").read()
    assert "não representa" in texto or "não há sub-passo" in texto.lower()
