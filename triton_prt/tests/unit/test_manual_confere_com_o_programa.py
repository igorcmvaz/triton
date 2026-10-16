"""Os números impressos no manual são os números que o programa produz.

Um manual separado do código envelhece em silêncio. A correção da energia de
bombeamento desta versão mudou o consumo da motobomba em 65%: num manual separado do
código, esse número ficaria errado por anos, e ninguém saberia.

A saída é fechar o laço. Cada valor impresso no manual tem asserção aqui. Quando o
programa muda, o teste falha e aponta **qual página** corrigir, em vez de o manual
passar a mentir.

Este arquivo cobre o capítulo 23, que é o caso resolvido dia a dia — o capítulo do
qual todos os outros dependem. Os demais capítulos entram aqui conforme forem
escritos.

O arquivo é IDÊNTICO nas três edições (`auditoria/ferramentas/sync_nucleo.py`) e vale
sempre: o conjunto de testes sai da edição ativa (`TRITON_EDITION`).

- **BRL**: o conjunto original (tutorial de Florianópolis, texto em português), sem mudança.
- **INT**: o conjunto `test_int_*`, no fim do arquivo (tutorial de Nova York, Londres e Cidade
  do Cabo, custos ilustrativos, texto em inglês); o resto é saltado, exceto os `NEUTROS`.
- **PRT**: o conjunto `test_prt_*`, no fim do arquivo (tutorial de Lisboa, Porto e Funchal, custos
  ilustrativos em euros, texto em português de Portugal); o resto é saltado, exceto os `NEUTROS`.
"""

from __future__ import annotations

import os
import re

import numpy as np
import pytest

from triton.core.edition import get_current_edition
from triton.core.simulation import run_single_simulation

EDICAO = get_current_edition()

#: Testes do motor, sem dado de nenhuma edição: rodam nas três edições.
NEUTROS = {
    "test_a_classe_alvo_sozinha_nao_muda_o_custo_da_etap",
    "test_a_recusa_do_polimento_fica_registrada",
    "test_uv_e_ozonio_somam_a_cloracao_em_vez_de_substitui_la",
    "test_o_rendimento_do_motor_do_capitulo_28",
    "test_as_densidades_do_apendice_C",
    "test_a_franquia_para_de_descontar_como_o_guia_16_mostra",
}


@pytest.fixture(autouse=True)
def _conjunto_da_edicao(request):
    """Escolhe o conjunto de testes pela edição: BRL o original, INT os `test_int_*`, PRT os `test_prt_*`."""
    nome = request.node.name.split("[")[0]
    if EDICAO == "BRL":
        if nome.startswith(("test_int_", "test_prt_")):
            pytest.skip("conjunto de outra edição")
    elif EDICAO == "INT":
        if not nome.startswith("test_int_") and nome not in NEUTROS:
            pytest.skip("conjunto da Edição Brasil; a INT usa os test_int_* (fim do arquivo)")
    else:
        if not nome.startswith("test_prt_") and nome not in NEUTROS:
            pytest.skip("conjunto da Edição Brasil; a PRT usa os test_prt_* (fim do arquivo)")


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


def _capitulo(arquivo):
    """Texto do capítulo com as tabelas geradas já incluídas.

    O capítulo pede a tabela por `<!-- inclui: ... -->`, e é o manual montado que o
    leitor vê. Testar só o fonte do capítulo deixaria passar número errado na tabela.
    """
    caminho = os.path.join(MANUAL, "partes", arquivo)
    if not os.path.exists(caminho):
        pytest.skip(f"{arquivo} ainda não escrito")
    saida = []
    for linha in open(caminho, encoding="utf-8").read().split(chr(10)):
        m = re.match(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$", linha)
        if m:
            alvo = os.path.join(MANUAL, "partes", m.group(1))
            if os.path.exists(alvo):
                saida.append(open(alvo, encoding="utf-8").read())
                continue
        saida.append(linha)
    return chr(10).join(saida)


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
    # Bacia sanitária e usos externos: desde 2026-09-18 a máquina de lavar roupa
    # fica fora, como no item 4.1.7 da ABNT NBR 15527:2019.
    total_demand_per_day=600.0, rainwater_share=0.28,
)
VOLUME = 4000.0


@pytest.fixture(scope="module")
def serie_tutorial():
    from triton.core.parser import load_precipitation
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


def test_a_agua_bruta_e_o_triplo_da_demanda(serie_tutorial):
    """Impresso no capítulo 5: 229 m³ de oferta bruta contra 61 m³ de demanda."""
    anos = len(serie_tutorial) / 365.25
    bruta = serie_tutorial.sum() / anos * TUTORIAL["area"] * TUTORIAL["runoff_coeff"] / 1000.0
    demanda = TUTORIAL["total_demand_per_day"] * TUTORIAL["rainwater_share"] * 365.25 / 1000.0
    assert bruta == pytest.approx(229.0, abs=2.0)
    assert demanda == pytest.approx(61.0, abs=1.0)
    assert bruta > 3 * demanda


def test_a_primeira_simulacao_do_capitulo_6(serie_tutorial):
    """Impresso: 26,48% com 3.000 L, 354 L/dia extravasados, 93,9% de dias plenos."""
    r = _tutorial(serie_tutorial, 3000)
    assert r.potential_potable_savings_pct == pytest.approx(26.48, abs=0.05)
    assert r.avg_spilled_l_day == pytest.approx(354.0, abs=1.0)
    assert r.pct_days_full_satisfaction == pytest.approx(93.9, abs=0.1)
    assert r.annual_pluvial_consumed_m3 == pytest.approx(58.0, abs=0.1)


def test_o_extravasamento_supera_o_consumo_pretendido(serie_tutorial):
    """Impresso no capítulo 6: extravasa mais que o dobro dos 168 L/dia pretendidos."""
    r = _tutorial(serie_tutorial, 3000)
    assert r.avg_spilled_l_day > 2 * 168.0


@pytest.mark.parametrize(("volume", "potencial"), [
    (1000, 21.03), (2000, 25.03), (3000, 26.48), (4000, 27.12), (5000, 27.47),
    (8000, 27.92), (12000, 28.00), (20000, 28.00),
])
def test_a_curva_de_varredura_do_capitulo_7(serie_tutorial, volume, potencial):
    """Cada linha da tabela impressa no capítulo 7."""
    r = _tutorial(serie_tutorial, volume)
    assert r.potential_potable_savings_pct == pytest.approx(potencial, abs=0.05)


def test_o_potencial_nunca_passa_da_fracao_atendivel(serie_tutorial):
    """A lição central do capítulo 5: a fração é o teto, e nada a ultrapassa."""
    teto = TUTORIAL["rainwater_share"] * 100.0
    for v in (1000, 4000, 20000, 100000):
        assert _tutorial(serie_tutorial, v).potential_potable_savings_pct <= teto + 1e-9


@pytest.mark.parametrize(("limiar", "ideal"), [(3.0, 3000), (1.0, 4000), (0.5, 5000)])
def test_o_limiar_decide_o_volume_ideal(serie_tutorial, limiar, ideal):
    """Impresso no capítulo 7: o limiar é escolha do autor, e muda a resposta."""
    from triton.core.simulation import run_sweep_simulation
    r = run_sweep_simulation(
        precip_data=serie_tutorial, lower_tank_max=20000.0, lower_tank_step=1000.0,
        delta_ideal_threshold=limiar, **TUTORIAL)
    assert r.optimal_lower_tank_vol == pytest.approx(ideal)


def test_o_volume_maior_custa_muito_mais_por_pouco_ganho(serie_tutorial):
    """Impresso no capítulo 7: 3,9× o preço e 4,1× o carbono por 0,88 ponto."""
    from triton.core.cost_estimates import estimate_tank_price
    from triton.core.environmental import EnvironmentalConfig, calculate_lca

    r4 = _tutorial(serie_tutorial, VOLUME)
    r20 = _tutorial(serie_tutorial, 20000)
    assert r20.potential_potable_savings_pct - r4.potential_potable_savings_pct \
        == pytest.approx(0.88, abs=0.05)

    p4 = estimate_tank_price(VOLUME, "CONCRETO")
    p20 = estimate_tank_price(20000.0, "CONCRETO")
    assert p20 / p4 == pytest.approx(3.9, abs=0.1)

    cfg = _ambiental("CONCRETO")
    c4 = calculate_lca(VOLUME, r4.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    c20 = calculate_lca(20000.0, r20.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    assert c20 / c4 == pytest.approx(4.1, abs=0.1)


def test_os_capitulos_do_tutorial_citam_os_numeros_do_programa():
    """Os valores escritos no corpo dos capítulos 4 a 7."""
    esperados = {
        "04_o_projeto_e_a_chuva.md": ("150 m²", "0,85", "2,0 mm", "229 m³"),
        "05_a_edificacao_e_a_demanda.md": ("600 L/dia", "168 L/dia", "28%", "61"),
        "06_a_primeira_simulacao.md": ("26,48%", "354 L/dia", "93,9%", "3.000"),
        "07_escolher_o_volume.md": ("4.000 L", "27,12%", "96,6%", "28,00%"),
    }
    for arquivo, termos in esperados.items():
        texto = _capitulo(arquivo)
        for termo in termos:
            assert termo in texto, f"{arquivo} não cita {termo}"

# ── tutorial, capítulos 8 a 13 ────────────────────────────────────────────────

def _economico(serie, volume, material):
    """Monta a análise econômica do tutorial, como os capítulos 10 e 12 fazem."""
    from triton.core.cost_estimates import estimate_tank_price
    from triton.core.economic import run_economic_analysis
    from triton.core.parser import TritonConfig

    # Da seção do reservatório superior em diante, o tutorial adota recalque para
    # caixa de 1.000 L com limiar de 100 L, e as duas motobombas padrão.
    r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                              upper_tank_vol=1000.0, upper_tank_used=True,
                              pumping_threshold=100.0, **TUTORIAL)
    cfg = TritonConfig()
    cfg.water_tariffs = [(0.0, 0.0, 46.34, -1), (0.0, 10.0, 3.08, 1),
                         (10.0, 25.0, 14.31, 1), (25.0, 50.0, 19.14, 1),
                         (50.0, 999999.0, 24.08, 1)]
    cfg.sewage_mode, cfg.sewage_rate = 1, 100.0
    cfg.cost_lower_tank = estimate_tank_price(float(volume), material)
    cfg.cost_upper_tank = estimate_tank_price(1000.0, "PEAD")
    cfg.cost_labor, cfg.cost_piping, cfg.cost_accessories = 3500.0, 1200.0, 1800.0
    cfg.supply_arrangement, cfg.upper_tank_used = "recalque", True
    cfg.upper_tank_vol, cfg.pumping_threshold = 1000.0, 100.0
    cfg.elec_tariff, cfg.tma, cfg.inflation = 0.69568, 0.5, 0.35
    cfg.analysis_period_years, cfg.tariff_escalation = 20, 12
    # O descarte físico entra como na interface: 2 mm sobre 150 m².
    cfg.area, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    return r, run_economic_analysis(cfg, r)


def _ambiental(material, resultado=None):
    """A configuração ambiental do tutorial, com o descarte físico e o recalque.

    Com o resultado da simulação, a energia vem da mesma função do econômico.
    """
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.lower_material_key = material
    cfg.roof_area_m2, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    cfg.supply_arrangement, cfg.upper_tank_vol_liters = "recalque", 1000.0
    if resultado is not None:
        bomba = TritonConfig()
        bomba.supply_arrangement = "recalque"
        cfg.annual_pump_kwh = compute_annual_pump_energy(bomba, resultado).annual_kwh
    return cfg


def test_a_caixa_superior_nao_aumenta_a_economia(serie_tutorial):
    """Impresso no capítulo 8: com o mesmo armazenamento, o arranjo duplo perde."""
    unico = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=VOLUME + 1000.0, **TUTORIAL)
    duplo = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **TUTORIAL)
    assert duplo.potential_potable_savings_pct < unico.potential_potable_savings_pct
    assert unico.potential_potable_savings_pct - duplo.potential_potable_savings_pct \
        == pytest.approx(0.17, abs=0.05)


def test_a_energia_do_recalque_do_capitulo_8(serie_tutorial):
    """Impresso: 7,7 kWh/ano e 68 acionamentos."""
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy

    duplo = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **TUTORIAL)
    cfg = TritonConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw, cfg.pump_efficiency, cfg.pump_flow_rate = 0.37, 0.0, 0.0
    cfg.pump_manometric_head_m, cfg.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(cfg, duplo)
    assert e.annual_kwh == pytest.approx(7.7, abs=0.3)
    assert e.annual_cycles == pytest.approx(68, abs=3)


def test_o_limiar_de_acionamento_troca_potencial_por_desgaste(serie_tutorial):
    """Impresso no capítulo 8: limiar maior, mais potencial e mais acionamentos."""
    anterior = None
    for limiar in (0, 100, 300, 500):
        r = run_single_simulation(
            precip_data=serie_tutorial, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
            upper_tank_used=True, pumping_threshold=float(limiar), **TUTORIAL)
        ciclos = r.total_pump_cycles / (r.total_days / 365.25)
        if anterior is not None:
            assert ciclos >= anterior
        anterior = ciclos


def test_a_classe_alvo_sozinha_nao_muda_o_custo_da_etap():
    """Impresso no capítulo 9: sem polimento, as quatro classes custam o mesmo."""
    from triton.core.water_quality import WATER_QUALITY_CLASSES, size_etap
    custos = {
        cid: size_etap(target_class_id=cid, annual_pluvial_consumed_m3=59.8,
                       roof_area_m2=150.0, include_polishing_filter=False
                       ).total_etap_capex
        for cid in WATER_QUALITY_CLASSES
    }
    assert len(set(round(c, 2) for c in custos.values())) == 1


def test_a_recusa_do_polimento_fica_registrada():
    """Impresso: quem recusa o que a classe recomenda tem a recusa documentada."""
    from triton.core.water_quality import size_etap
    r2 = size_etap(target_class_id="classe_2", annual_pluvial_consumed_m3=59.8,
                   roof_area_m2=150.0, include_polishing_filter=False)
    r1 = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=59.8,
                   roof_area_m2=150.0, include_polishing_filter=False)
    assert r2.polishing_recommended_but_declined is True
    assert r1.polishing_recommended_but_declined is False


def test_uv_e_ozonio_somam_a_cloracao_em_vez_de_substitui_la():
    """Impresso no capítulo 9: são barreiras adicionais, sem residual próprio."""
    from triton.core.water_quality import size_etap
    cloro = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=59.8,
                      roof_area_m2=150.0, disinfection_choice="cloro")
    uv = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=59.8,
                   roof_area_m2=150.0, disinfection_choice="uv")
    assert uv.total_etap_capex > cloro.total_etap_capex
    assert len(uv.disinfection_stages) == 2


def test_o_resultado_economico_do_capitulo_10(serie_tutorial):
    """Impresso: R$ 1.712/ano, VPL R$ 2.745, payback 16,3 anos, em concreto.

    Com o descarte físico da etapa 3 e o recalque para a caixa superior: sem o
    descarte o investimento seria R$ 13.444,29 e o VPL R$ 4.032, valores que o
    capítulo cita como comparação.
    """
    _, e = _economico(serie_tutorial, VOLUME, "CONCRETO")
    assert e.capex_total == pytest.approx(14061.19, abs=1.0)
    assert e.annual_water_savings_brl == pytest.approx(1712.26, abs=5.0)
    assert e.vpl == pytest.approx(2745.0, abs=50.0)
    assert e.payback_years == pytest.approx(16.3, abs=0.2)
    assert e.annual_pump_cost_brl == pytest.approx(5.36, abs=0.05)
    assert e.annual_opex_brl == pytest.approx(48.82, abs=0.05)


def test_a_troca_para_polietileno_melhora_as_tres_dimensoes(serie_tutorial):
    """Impresso no capítulo 11: mais barato, melhor VPL e carbono positivo."""
    from triton.core.environmental import EnvironmentalConfig, calculate_lca

    r_c, e_c = _economico(serie_tutorial, VOLUME, "CONCRETO")
    r_p, e_p = _economico(serie_tutorial, VOLUME, "PEAD")
    assert e_p.capex_total < e_c.capex_total
    assert e_p.vpl > e_c.vpl
    assert e_p.payback_years < e_c.payback_years

    saldos = {}
    for k, r in (("CONCRETO", r_c), ("PEAD", r_p)):
        cfg = _ambiental(k, r)
        saldos[k] = calculate_lca(VOLUME, r.annual_pluvial_consumed_m3, cfg)
    assert saldos["PEAD"].lifetime_net_co2_saved_kg > 0
    assert saldos["CONCRETO"].lifetime_net_co2_saved_kg < 0
    assert saldos["CONCRETO"].environmental_payback_years > 20.0
    # 11,8 anos desde 2026-09-15: a emissão de fabricação da motobomba passou a vir de
    # massa de catálogo x intensidade de EPD (30,5 kg CO2e a 1/2 CV, antes 18,0).
    # 12,6 anos com o descarte físico (reservatório de 300 L e separador de folhas).
    # 13,1 anos com a caixa superior de 1.000 L e a energia do recalque.
    # 16,3 anos com 28% de fração atendível e 4.000 L, desde 2026-09-18.
    assert saldos["PEAD"].environmental_payback_years == pytest.approx(16.3, abs=0.3)
    assert saldos["CONCRETO"].environmental_payback_years == pytest.approx(42.8, abs=0.5)


def test_em_concreto_o_carbono_piora_com_o_volume(serie_tutorial):
    """Impresso: cada metro cúbico de concreto acrescenta mais dívida que crédito."""
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    anterior = None
    for v in (2000, 3000, 4000, 8000):
        r = run_single_simulation(
            precip_data=serie_tutorial, lower_tank_vol=float(v), **TUTORIAL)
        cfg = _ambiental("CONCRETO")
        saldo = calculate_lca(float(v), r.annual_pluvial_consumed_m3,
                              cfg).lifetime_net_co2_saved_kg
        if anterior is not None:
            assert saldo < anterior, f"{v} L não piorou"
        anterior = saldo


def test_os_tres_criterios_do_capitulo_12_discordam(serie_tutorial):
    """Impresso: técnico diz 12.000, financeiro 2.000, ambiental 2.000, compromisso 4.000."""
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.topsis import TopsisCandidate, calculate_topsis_scores

    cands = []
    for v in (1000, 2000, 3000, 4000, 5000, 8000, 12000):
        r, e = _economico(serie_tutorial, v, "PEAD")
        amb = _ambiental("PEAD", r)
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v), water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg,
            capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct,
            overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years, irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))

    res = calculate_topsis_scores(cands)
    assert cands[res.technical_best_index].lower_tank_vol == 12000.0
    assert cands[res.financial_best_index].lower_tank_vol == 2000.0
    assert cands[res.environmental_best_index].lower_tank_vol == 2000.0
    assert cands[res.best_index].lower_tank_vol == VOLUME


def test_os_capitulos_8_a_13_citam_os_numeros_do_programa():
    esperados = {
        "08_reservatorio_superior.md": ("7,7 kWh", "um sexto de ponto", "5.000 L"),
        "09_qualidade_que_o_uso_exige.md": ("R$ 1.547", "R$ 2.747", "R$ 5.047", "R$ 1.197"),
        "10_quanto_custa.md": ("R$ 142,69", "R$ 2.745", "16,3 anos", "R$ 28,60", "R$ 5,36"),
        "11_quanto_carbono_evita.md": ("858 kg", "42,8 anos", "16,3 anos", "74 kg"),
        "12_qual_volume_escolher.md": ("4.000 L", "12.000 L", "2.000 L", "27,30%"),
        "13_o_relatorio_e_o_artigo.md": ("0.1.0", "2,3 a 2,7", "1 %/m"),
    }
    for arquivo, termos in esperados.items():
        texto = _capitulo(arquivo)
        for termo in termos:
            assert termo in texto, f"{arquivo} não cita {termo}"


def test_o_capitulo_13_traz_a_lista_de_declaracao():
    """O capítulo que não existe em manual nenhum, e é o que torna um estudo
    reproduzível."""
    caminho = os.path.join(MANUAL, "partes", "13_o_relatorio_e_o_artigo.md")
    if not os.path.exists(caminho):
        pytest.skip("capítulo 13 ainda não escrito")
    texto = open(caminho, encoding="utf-8").read()
    for exigido in ("Versão do Triton", "fronteira", "regime", "pesos",
                    "limiar", "rótulo de triagem"):
        assert exigido in texto, f"a lista de declaração não cobre {exigido}"

# ══════════════════════════════════════════════════════════════════════════════
# Integridade do manual montado
# ══════════════════════════════════════════════════════════════════════════════

#: A estrutura da ABNT: sete capítulos, e as seções de cada um. A contagem sai
#: da própria declaração do montador, para que reordenar o manual não exija
#: reescrever este teste — foi assim que a numeração parou de divergir.
# 44 desde que o capítulo «Modulação probabilística» (seções 40 a 44) entrou.
SECOES_EM_PARTES = 45
APENDICES = 10


def _manual_montado():
    caminho = os.path.join(MANUAL, "Manual-Triton.md")
    if not os.path.exists(caminho):
        pytest.skip("manual ainda não montado; rode manual/gerar.py")
    return open(caminho, encoding="utf-8").read()


def test_todos_os_capitulos_e_apendices_estao_escritos():
    """Nenhuma seção pode sair como esqueleto no manual montado."""
    texto = _manual_montado()
    assert "Capítulo por escrever" not in texto
    assert "Apêndice por escrever" not in texto


def test_o_manual_tem_todos_os_arquivos_de_secao():
    partes = os.path.join(MANUAL, "partes")
    escritos = [f for f in os.listdir(partes) if f.endswith(".md")]
    assert len(escritos) == SECOES_EM_PARTES, sorted(escritos)


def test_o_manual_tem_todos_os_apendices():
    apend = os.path.join(MANUAL, "apendices")
    escritos = [f for f in os.listdir(apend) if f.endswith(".md")]
    assert len(escritos) == APENDICES, sorted(escritos)


def test_nenhuma_inclusao_de_tabela_ficou_por_resolver():
    """Se uma tabela gerada faltar, o número some do manual sem aviso."""
    texto = _manual_montado()
    assert "<!-- inclui:" not in texto


def test_as_figuras_referidas_existem():
    partes = os.path.join(MANUAL, "partes")
    faltando = []
    for arquivo in sorted(os.listdir(partes)):
        if not arquivo.endswith(".md"):
            continue
        texto = open(os.path.join(partes, arquivo), encoding="utf-8").read()
        for ref in re.findall(r"!\[[^\]]*\]\((\.\./figuras/[^)]+)\)", texto):
            alvo = os.path.normpath(os.path.join(partes, ref))
            if not os.path.exists(alvo):
                faltando.append(f"{arquivo}: {ref}")
    assert not faltando, faltando


def test_o_sumario_lista_todas_as_secoes():
    """O sumário sai da estrutura declarada, e precisa cobri-la inteira."""
    import sys
    sys.path.insert(0, MANUAL)
    from gerar import ESTRUTURA, entrada_do_sumario, sumario_do_capitulo

    texto = _manual_montado()
    cabeca = texto.split("# 1. ")[0]
    for i, (titulo_cap, pasta, secoes) in enumerate(ESTRUTURA, start=1):
        assert sumario_do_capitulo(i, titulo_cap, pasta) in cabeca, f"falta o capítulo {i}"
        for chave in secoes:
            linha = entrada_do_sumario(chave, pasta)
            assert linha in cabeca, f"o sumário não lista «{linha}»"


def test_a_numeracao_das_secoes_segue_a_ordem_da_estrutura():
    """Cada título numerado do corpo confere com a posição declarada."""
    import sys
    sys.path.insert(0, MANUAL)
    from gerar import ESTRUTURA, TITULOS

    texto = _manual_montado()
    for i, (_, pasta, secoes) in enumerate(ESTRUTURA, start=1):
        for j, chave in enumerate(secoes, start=1):
            if pasta == "apendices":
                # Apêndices por letra, como pede a ABNT NBR 14724.
                letra = chave.split("_")[0]
                assert f"## Apêndice {letra} — {TITULOS[chave]}" in texto, chave
            else:
                assert f"## {i}.{j}. {TITULOS[chave]}" in texto, f"{i}.{j} {chave}"


def test_nenhuma_marca_de_referencia_sobrou_por_resolver():
    """Marca não resolvida é referência cruzada apontando para lugar nenhum."""
    texto = _manual_montado()
    assert "{{" not in texto, texto[texto.index("{{"):texto.index("{{") + 60]
    assert "??" not in texto


def test_as_equacoes_estao_numeradas_em_sequencia():
    """A ABNT numera as equações em sequência, e cada citação tem destino."""
    texto = _manual_montado()
    numeros = [int(n) for n in re.findall(r"^```equacao:[^:]+:(\d+)$", texto,
                                          flags=re.M)]
    assert numeros == list(range(1, len(numeros) + 1)), numeros
    assert len(numeros) >= 8


def test_toda_equacao_declara_as_variaveis_e_as_unidades():
    """Equação sem a tabela de variáveis é equação que o leitor não consegue usar.

    A tabela pode vir depois de uma sequência de equações encadeadas; o que o
    teste exige é que nenhuma equação fique órfã de declaração até o próximo
    título.
    """
    texto = _manual_montado()
    for m in re.finditer(r"^```equacao:([^:]+):\d+$", texto, flags=re.M):
        # Do início da equação até o próximo título: é a janela em que a
        # declaração das variáveis precisa aparecer. Equações encadeadas podem
        # dividir uma tabela só, e por isso a janela não para na equação
        # seguinte.
        resto = texto[m.end():]
        fim = re.search(r"^#{2,4} ", resto, flags=re.M)
        janela = resto[: fim.start()] if fim else resto
        assert "| Símbolo | Significado | Unidade |" in janela, (
            "equação sem tabela de variáveis: " + m.group(1))


def test_o_manual_declara_que_os_numeros_sao_calculados():
    """A promessa que dá autoridade ao documento inteiro."""
    texto = _manual_montado()
    assert "Todo número impresso neste manual é calculado pelo programa" in texto


# ══════════════════════════════════════════════════════════════════════════════
# Os guias e o método
# ══════════════════════════════════════════════════════════════════════════════

def test_os_regimes_tarifarios_do_guia_16_e_do_apendice_D():
    """Impresso: 371 de franquia, 100 sem mínimo, 122 de disponibilidade, 36 exponenciais, 23 retroativas."""
    import json
    from collections import Counter

    caminho = os.path.join(RAIZ, "triton", "data", "brazil_cities_tariffs.json")
    base = json.load(open(caminho, encoding="utf-8"))
    regimes = Counter(c.get("regime_tarifario") for c in base["cities"].values())
    assert len(base["cities"]) == 652
    assert regimes["franquia_no_minimo"] == 371
    assert regimes["sem_minimo"] == 100
    assert regimes["franquia_retroativa"] == 23
    assert regimes["disponibilidade"] == 122
    assert regimes["exponencial"] == 36

    # As tabelas de regimes dos capítulos 10 e 16 (PT e EN) citam as mesmas contagens.
    import re
    rotulos = {"sem mínimo": "sem_minimo", "no minimum": "sem_minimo", "disponibilidade": "disponibilidade",
               "availability charge": "disponibilidade", "franquia no mínimo": "franquia_no_minimo",
               "allowance in the minimum": "franquia_no_minimo", "franquia retroativa": "franquia_retroativa",
               "retroactive allowance": "franquia_retroativa", "fórmula exponencial": "exponencial",
               "exponential formula": "exponencial"}
    for rel in ("manual/partes/10_quanto_custa.md", "manual/en/partes/10_quanto_custa.md",
                "manual/partes/16_ajustar_a_tarifa.md", "manual/en/partes/16_ajustar_a_tarifa.md"):
        caminho_completo = os.path.join(RAIZ, rel)
        if not os.path.exists(caminho_completo):
            continue
        texto = open(caminho_completo, encoding="utf-8").read()
        for rotulo, regime in rotulos.items():
            for m in re.finditer(r"^\| \**" + re.escape(rotulo) + r"\** \|.*\| (\d+) \|$", texto, flags=re.M):
                assert int(m.group(1)) == regimes[regime], f"{rel}: «{rotulo}» diz {m.group(1)}, a base tem {regimes[regime]}"


def test_a_franquia_para_de_descontar_como_o_guia_16_mostra():
    """Impresso: em Floriano, poupar 4 ou poupar 7 economiza o mesmo."""
    from triton.core.economic import calculate_water_bill

    FLORIANO = [(0.0, 0.0, 52.89, -1), (0.0, 10.0, 0.0, 1),
                (10.0, 15.0, 9.815, 1), (15.0, 20.0, 10.917, 1),
                (20.0, 999999.0, 12.8, 1)]
    conta = lambda m3: calculate_water_bill(m3 * 1000, FLORIANO, 1, 0.0, 0.0, 0.0)
    assert conta(12.0) == pytest.approx(72.52, abs=0.05)
    assert conta(8.0) == pytest.approx(52.89, abs=0.05)
    assert conta(5.0) == pytest.approx(52.89, abs=0.05)
    assert conta(12.0) - conta(8.0) == pytest.approx(conta(12.0) - conta(5.0), abs=0.01)


def test_as_cidades_do_guia_14(serie_tutorial):
    """Impresso: Manaus chove mais que Florianópolis e rende menos."""
    from triton.core.parser import load_precipitation

    resultados = {}
    for chave in ("Florianopolis1", "Manaus1", "Brasilia1"):
        caminho = os.path.join(RAIZ, "data", "rainfall", f"{chave}.csv")
        if not os.path.exists(caminho):
            pytest.skip(f"série {chave} não instalada")
        serie = load_precipitation(caminho)[: 30 * 365]
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **TUTORIAL)
        resultados[chave] = (serie.sum() / anos, r.potential_potable_savings_pct)

    chuva_flo, pot_flo = resultados["Florianopolis1"]
    chuva_man, pot_man = resultados["Manaus1"]
    chuva_bsb, pot_bsb = resultados["Brasilia1"]

    assert chuva_man > chuva_flo and pot_man < pot_flo
    assert chuva_bsb < chuva_flo and pot_bsb < pot_flo / 1.5
    assert pot_man == pytest.approx(20.96, abs=0.05)
    assert pot_bsb == pytest.approx(15.45, abs=0.05)


def test_o_rendimento_do_motor_do_capitulo_28():
    """Impresso: a Tabela 13 da ABNT NBR 17094-2, dois polos, linha IR1."""
    from triton.core.pump_hydraulics import rendimento_do_motor
    esperado = {0.18: 0.500, 0.25: 0.555, 0.37: 0.605,
                0.55: 0.640, 0.75: 0.693, 1.10: 0.715, 1.50: 0.724}
    for kw, eta in esperado.items():
        assert rendimento_do_motor(kw) == pytest.approx(eta), f"{kw} kW"


def test_as_densidades_do_apendice_C():
    """Impresso: massa por m³ útil de cada material."""
    from triton.core.environmental import MATERIAL_PRESETS
    esperado = {"PEAD": 22.0, "CONCRETO": 1200.0, "FIBRA": 15.0, "ACO_INOX": 38.0}
    for k, densidade in esperado.items():
        assert MATERIAL_PRESETS[k].material_density_kg_per_m3_tank \
            == pytest.approx(densidade)


def test_a_decomposicao_da_divergencia_e_coerente_entre_documentos():
    """`metodologia.md` e `verificacao_e_validacao.md` diziam 46% e 50%.

    A decomposição é 1,36 pp de 2,71 pp, ou seja 50%. O documento de metodologia
    trazia 46%, e os dois passaram anos discordando sobre o mesmo número.
    """
    met = os.path.join(RAIZ, "docs", "metodologia.md")
    ver = os.path.join(RAIZ, "docs", "verificacao_e_validacao.md")
    for caminho in (met, ver):
        if not os.path.exists(caminho):
            pytest.skip("documentação de referência ausente")
    texto_met = open(met, encoding="utf-8").read()
    texto_ver = open(ver, encoding="utf-8").read()
    assert "1,36 pp (50%)" in texto_ver
    assert "46%" not in texto_met
    assert "50%" in texto_met
    assert 1.36 / 2.71 == pytest.approx(0.50, abs=0.01)


def test_os_capitulos_finais_citam_o_que_precisam_citar():
    esperados = {
        "01_o_que_o_triton_faz.md": ("dimensiona a instalação hidráulica", "triagem", "0,25"),
        "03_por_onde_comecar.md": ("fração atendível", "varredura"),
        "24_volume_ideal.md": ("250", "limitado a 40", "%/m"),
        "25_indicadores.md": ("365,25", "demanda pluvial", "demanda total"),
        "26_indices_pluviometricos.md": ("R10mm", "1961", "Walsh"),
        "27_etap.md": ("incremental", "65%", "substitui"),
        "28_energia_de_bombeamento.md": ("17094", "60,5%", "eixo"),
        "29_analise_economica.md": ("371", "diferença entre duas faturas"),
        "30_acv.md": ("entregue", "33,9%", "triagem"),
        "31_certificacoes.md": ("WEM14", "barra de água", "não pontua"),
        "32_multicriterio.md": ("Opricovic", "variante", "SMAA"),
        "33_dez_enganos.md": ("projeção horizontal", "milímetros", "franquia"),
        "35_comparacao_netuno4.md": ("0,25 pp", "4.050", "1,36 pp"),
        "36_limitacoes.md": ("residencial", "triagem", "108 s"),
        "37_mensagens_de_erro.md": ("negativ", "0,4 para 40%"),
    }
    for arquivo, termos in esperados.items():
        texto = _capitulo(arquivo)
        for termo in termos:
            assert termo in texto, f"{arquivo} não cita {termo}"

# ══════════════════════════════════════════════════════════════════════════════
# O manual descreve o programa instalado, e não o ambiente de desenvolvimento
# ══════════════════════════════════════════════════════════════════════════════
#
# O leitor recebe um executável. Comando de terminal, nome de módulo e caminho de
# arquivo-fonte descrevem uma máquina que ele não tem, e mandá-lo procurá-los é
# pior que omissão: é instrução que não funciona.

TERMOS_DE_DESENVOLVIMENTO = (
    "python -m", "python manual", "pip install", "pytest", "requirements.txt",
    "PySide6", "Numba", "triton.cli", "argparse",
)


def _todo_o_texto_do_manual():
    partes = []
    for pasta in ("partes", "apendices"):
        caminho = os.path.join(MANUAL, pasta)
        for arquivo in sorted(os.listdir(caminho)):
            if arquivo.endswith(".md"):
                partes.append((
                    os.path.join(pasta, arquivo),
                    open(os.path.join(caminho, arquivo), encoding="utf-8").read()))
    return partes


def test_o_manual_nao_manda_o_leitor_rodar_nada_no_terminal():
    achados = []
    for nome, texto in _todo_o_texto_do_manual():
        for termo in TERMOS_DE_DESENVOLVIMENTO:
            if termo.lower() in texto.lower():
                achados.append(f"{nome}: {termo}")
    assert not achados, achados


def test_o_manual_nao_cita_arquivos_de_codigo():
    """`.py` no texto é sinal de que a frase fala do repositório, não do programa."""
    achados = []
    for nome, texto in _todo_o_texto_do_manual():
        for linha in texto.split(chr(10)):
            if re.search(r"[\w/\\]+\.py\b", linha):
                achados.append(f"{nome}: {linha.strip()[:70]}")
    assert not achados, achados


# ══════════════════════════════════════════════════════════════════════════════
# Figuras
# ══════════════════════════════════════════════════════════════════════════════

# 70 desde que a curva de otimizacao ambiental (fig06b) entrou no capitulo 12.
# 74 desde que as quatro figuras da modulação probabilística (fig52 a fig55) entraram.
FIGURAS_ESPERADAS = 74


def test_as_figuras_estao_numeradas_na_ordem_da_leitura():
    """A legenda «Figura 1» já apareceu no capítulo 23, depois da «Figura 2».

    A numeração passou a ser feita na montagem, e este teste é o que impede o
    problema de voltar quando alguém inserir uma figura no meio.
    """
    texto = _manual_montado()
    numeros = [int(n) for n in re.findall(r"\*Figura (\d+) —", texto)]
    assert numeros == list(range(1, len(numeros) + 1)), numeros
    assert len(numeros) == FIGURAS_ESPERADAS


def test_toda_figura_e_chamada_no_texto_antes_da_legenda():
    """O professor pediu, lendo o PDF: toda figura tem de ser chamada.

    A chamada é escrita nas partes como «{{fig:nome_do_arquivo}}» e vira
    «Figura N» na montagem. O teste lê o manual montado e exige, para cada
    legenda, que o número apareça antes dela no corpo do texto, fora de outra
    legenda: figura que aparece sem ser evocada é figura solta.
    """
    texto = _manual_montado()
    assert "{{fig:" not in texto
    sem_chamada = []
    for m in re.finditer(r"^\*Figura (\d+) —", texto, re.M):
        n = m.group(1)
        anterior = texto[:m.start()]
        corpo = re.sub(r"^\*Figura \d+ —.*$", "", anterior, flags=re.M)
        if not re.search(r"Figura " + n + r"(?!\d)", corpo):
            sem_chamada.append(int(n))
    assert not sem_chamada, sem_chamada


def test_os_desenhos_explicativos_existem():
    """Os três desenhos que explicam o sistema a quem chega agora."""
    pasta = os.path.join(MANUAL, "figuras")
    for nome in ("fig00_sistema.png", "fig00b_destino.png", "fig00c_fracao.png",
                 "fig00d_corte.png", "fig00e_balanco_do_dia.png",
                 "fig00f_yas.png", "fig00g_indicadores.png",
                 "fig00h_fronteira.png"):
        caminho = os.path.join(pasta, nome)
        assert os.path.exists(caminho), nome
        assert os.path.getsize(caminho) > 20_000, nome


def test_o_capitulo_1_apresenta_o_sistema_antes_de_falar_do_programa():
    """Quem abre o manual pode não saber o que é a instalação que vai simular."""
    texto = _capitulo("01_o_que_o_triton_faz.md")
    assert "O que é um sistema de aproveitamento de água pluvial" in texto
    for termo in ("calhas", "cisterna", "primeira chuva", "projeção horizontal",
                  "fig00_sistema.png", "fig00d_corte.png", "fig00b_destino.png"):
        assert termo in texto, termo
    # A ordem importa: o desenho do sistema vem antes do desenho do dia.
    assert texto.index("fig00_sistema.png") < texto.index("fig00b_destino.png")


def test_o_manual_explica_as_duas_caixas():
    texto = _manual_montado()
    assert "Aprofundamento" in texto
    cabeca = texto.split("## Sumário")[0]
    assert "régua **laranja**" in cabeca


# ══════════════════════════════════════════════════════════════════════════════
# As telas citadas são as telas que existem
# ══════════════════════════════════════════════════════════════════════════════

ETAPAS = (
    "1. Projeto e Chuva", "2. Edificação e Consumo", "3. Qualidade & ETAP",
    "4. Reservatório & Custos", "5. Resultados Técnicos",
    "6. Resultados Econômicos", "7. Resultados Ambientais & ESG",
    "8. Decisão Multicritério", "9. Relatórios PDF", "10. Exportação",
    "11. Documentação", "12. Gestor de Tarifas",
)


def test_as_etapas_citadas_pelo_manual_sao_as_da_barra_lateral():
    """O nome que o manual manda procurar precisa existir na tela."""
    fonte = os.path.join(RAIZ, "triton", "ui", "sidebar.py")
    texto_fonte = open(fonte, encoding="utf-8").read()
    for etapa in ETAPAS:
        assert etapa in texto_fonte, f"a barra lateral não tem «{etapa}»"

    citadas = set()
    for _, texto in _todo_o_texto_do_manual():
        for m in re.finditer(r"etapa \*\*([^*]+)\*\*", texto):
            citadas.add(m.group(1).strip())
    desconhecidas = [c for c in citadas
                     if not any(c.startswith(e) or e.endswith(c) for e in ETAPAS)]
    assert not desconhecidas, desconhecidas

# ══════════════════════════════════════════════════════════════════════════════
# Legenda de tabela e vocabulário
# ══════════════════════════════════════════════════════════════════════════════

def test_toda_tabela_tem_legenda():
    """Tabela sem legenda não se cita no texto nem se acha na lista inicial."""
    # Os elementos pré-textuais — a folha de rosto e o «como usar» — ficam de
    # fora: a ABNT não os numera, e uma tabela numerada antes da lista de
    # tabelas apontaria para trás dela.
    texto = _manual_montado().split("# 1. ", 1)[-1]
    linhas = texto.split(chr(10))
    sem_legenda = []
    for i, linha in enumerate(linhas[:-1]):
        if not linha.startswith("|"):
            continue
        if not re.match(r"^\|[\s:\-|]+\|$", linhas[i + 1].rstrip()):
            continue
        anterior = linhas[i - 1].strip() if i else ""
        if not anterior.startswith("<!-- tabela:"):
            sem_legenda.append(linha[:60])
    assert not sem_legenda, sem_legenda[:5]


def test_nenhuma_legenda_repete_os_cabecalhos():
    """A legenda descreve a tabela; repetir o cabeçalho não descreve nada.

    A montagem sabe compor uma legenda a partir do título da subseção e dos
    cabeçalhos, e essa composição é o último recurso. Este teste exige que ela
    não seja usada: toda tabela do manual tem legenda escrita à mão, ou é uma
    tabela de variáveis de equação.
    """
    texto = _manual_montado()
    mecanicas = []
    for numero, legenda in re.findall(
            r"<!-- tabela: \*\*Tabela (\d+)\*\* — (.+?) -->", texto):
        if legenda.startswith("Variáveis da Equação"):
            continue
        if re.search(r": .+, .+", legenda):
            mecanicas.append(f"Tabela {numero}: {legenda}")
    assert not mecanicas, mecanicas[:5]


def test_as_listas_iniciais_cobrem_tudo():
    """Lista de figuras, de tabelas e de equações, com todos os itens."""
    texto = _manual_montado()
    cabeca = texto.split("# 1. ")[0]
    for titulo in ("Lista de figuras", "Lista de tabelas", "Lista de equações"):
        assert titulo in cabeca, titulo

    figuras = len(re.findall(r"^\*Figura \d+ — ", texto, flags=re.M))
    tabelas = len(re.findall(r"<!-- tabela: \*\*Tabela \d+\*\*", texto))
    equacoes = len(re.findall(r"^```equacao:", texto, flags=re.M))
    assert cabeca.count("Figura ") >= figuras
    assert cabeca.count("Tabela ") >= tabelas
    assert cabeca.count("Equação ") >= equacoes


SIGLAS_DISPENSADAS = {
    # Siglas de uso corrente fora da engenharia, ou identificadores internos do
    # próprio manual, que não precisam de verbete.
    "PDF", "HTML", "GB", "SC", "PI", "AM", "DF", "SP", "UF", "CAIXA", "CNPJ",
    "GPL", "UFSC", "IBGE", "YAS", "SMAA-VIKOR",
    "TP",  # modelo de pressurizador citado (Komeco TP 820), não sigla
    "GHISI",  # sobrenome em caixa alta nas referências, não sigla
    "MIX",  # nome do periódico MIX Sustentável, não sigla a definir
    "LL",  # sufixo de nome de modelo climático (HadGEM3-GC31-LL, UKESM1-0-LL), não sigla
}


def test_toda_sigla_recorrente_esta_no_glossario():
    """Sigla usada três vezes ou mais é vocabulário, e precisa de verbete."""
    texto = _manual_montado()
    caminho = os.path.join(MANUAL, "apendices", "G_glossario.md")
    if not os.path.exists(caminho):
        pytest.skip("glossário ausente")
    # «IPTU verde» e «ISO 14040» são verbetes; a sigla nua também conta como
    # coberta, porque o leitor que procura «ISO» acha «ISO 14040».
    nomes = re.findall(r"^\*\*(.+?)\*\*",
                       open(caminho, encoding="utf-8").read(), flags=re.M)
    verbetes = {v.lower() for v in nomes}
    verbetes |= {v.split()[0].lower() for v in nomes if " " in v}
    # «BD+C» cobre a sigla nua «BD», pelo mesmo motivo.
    verbetes |= {v.split("+")[0].lower() for v in nomes if "+" in v}

    # As tabelas de faixas por município do apêndice de regimes tarifários são dado: os
    # nomes de prestadores e as siglas de UF ali são células, e não vocabulário do texto.
    texto = re.sub(r"(?ms)^#+ [^\n]*As faixas por município e categoria.*?(?=^#{2,3} )", "", texto)
    from collections import Counter
    contagem = Counter(re.findall(r"\b([A-Z]{2,}(?:-[A-Z0-9]+)?)\b", texto))
    faltando = [
        s for s, n in contagem.items()
        if n >= 3 and s.lower() not in verbetes
        and s not in SIGLAS_DISPENSADAS and not s.startswith("PROC-")
    ]
    assert not faltando, sorted(faltando)

# ══════════════════════════════════════════════════════════════════════════════
# Referências cruzadas e imagens
# ══════════════════════════════════════════════════════════════════════════════

def _titulos_numerados(texto):
    """Todo número de título do manual montado, seções e apêndices."""
    numeros = set(re.findall(r"^#{1,4} +([0-9]+(?:\.[0-9]+)*)\.? ", texto,
                             flags=re.M))
    numeros |= set(re.findall(r"^#{1,4} +Ap[êe]ndice +([A-J])", texto, flags=re.M))
    return numeros


def test_toda_referencia_a_secao_aponta_para_uma_secao_que_existe():
    """«A seção 35» é uma referência morta se a última seção é a 6.4.

    A renumeração para capítulos e seções da ABNT invalidou os números escritos à
    mão. As marcas {{n:...}} acompanham a renumeração; os números literais, não.
    """
    texto = _manual_montado()
    titulos = _titulos_numerados(texto)
    padrao = re.compile(
        r"(?:[Ss]eç(?:ão|ões)|[Cc]apítulos?|[Aa]pêndices?)\s+"
        r"((?:[0-9]+)(?:\.[0-9]+)*|[A-J])\b")
    mortas = []
    for m in padrao.finditer(texto):
        if m.group(1) not in titulos:
            inicio = max(0, m.start() - 60)
            mortas.append(texto[inicio:m.end()].replace(chr(10), " "))
    assert not mortas, mortas[:5]


def test_nenhum_numero_de_secao_antigo_sobrou_no_texto():
    """As antigas partes iam até 39; o manual agora tem seis capítulos.

    Um «33.4» solto numa célula de tabela é o resto de uma numeração que não
    existe mais, e não há como o leitor saber para onde ele aponta.
    """
    texto = _manual_montado()
    titulos = _titulos_numerados(texto)
    suspeitos = []
    for m in re.finditer(r"(?<![0-9,.])([1-9][0-9])\.([0-9]{1,2})(?![0-9,%])",
                         texto):
        if m.group(0) in titulos:
            continue
        contexto = texto[max(0, m.start() - 40):m.end() + 10]
        if "NBR" in contexto or "ISO" in contexto or "R$" in contexto:
            continue
        suspeitos.append(contexto.replace(chr(10), " "))
    assert not suspeitos, suspeitos[:5]


def test_toda_imagem_citada_existe_no_disco():
    """Uma figura ausente vira um retângulo vazio no PDF, sem aviso."""
    texto = _manual_montado()
    faltando = []
    # As capas dos volumes moram em `figuras/capas/`: procurar só na raiz de
    # `figuras/` dava por ausente a figura que está uma pasta abaixo.
    no_disco = set()
    for pasta, _, arquivos in os.walk(os.path.join(MANUAL, "figuras")):
        no_disco.update(arquivos)
    for caminho in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", texto):
        if os.path.basename(caminho) not in no_disco:
            faltando.append(os.path.basename(caminho))
    assert not faltando, sorted(set(faltando))


def test_toda_figura_do_disco_esta_no_manual():
    """Figura gerada e não citada é trabalho perdido, e some na próxima limpeza."""
    texto = _manual_montado()
    pasta = os.path.join(MANUAL, "figuras")
    orfas = [n for n in sorted(os.listdir(pasta))
             if n.endswith(".png") and n not in texto]
    assert not orfas, orfas


def test_o_historico_cita_a_conferencia_atual_da_base():
    """A linha da seção 38 sobre a conferência da base usa os números de ALTERACOES.md."""
    import re
    alt = open(os.path.join(RAIZ, "tarifas", "transcricoes", "ALTERACOES.md"), encoding="utf-8").read()
    m = re.search(r"Conferências: (\d+) · corrigidas: (\d+)", alt)
    conferidos, corrigidos = m.group(1), m.group(2)
    for rel in ("manual/partes/38_historico_de_versoes.md", "manual/en/partes/38_historico_de_versoes.md"):
        caminho_completo = os.path.join(RAIZ, rel)
        if not os.path.exists(caminho_completo):
            continue
        texto = open(caminho_completo, encoding="utf-8").read()
        assert f" {conferidos} " in texto and f" {corrigidos} " in texto, f"{rel}: conferência desatualizada"


# ══════════════════════════════════════════════════════════════════════════════
# Edição Internacional (INT): Nova York, Londres e Cidade do Cabo
# ══════════════════════════════════════════════════════════════════════════════
#
# O tutorial da INT é a mesma casa (150 m², 4 moradores, 150 L/hab·dia, 28% não potável) em Nova York,
# com a chuva ERA5 1991-2020 de `data/rainfall` e a tarifa de `examples/new_york.triton`; Londres e
# Cidade do Cabo são as cidades de comparação. Os custos são ILUSTRATIVOS (US$, números redondos
# declarados em `manual/gerar_tabelas.py`), nunca preços de mercado. Os valores abaixo são os que
# `manual/gerar_tabelas.py` e `manual/gerar_casos.py` produzem; o texto em inglês cita os mesmos.

INT_CHUVAS = os.path.join(RAIZ, "data", "rainfall")
INT_CASOS = os.path.join(MANUAL, "casos")
INT_TABELAS = os.path.join(MANUAL, "en", "partes", "_tabelas")
INT_PARTES = os.path.join(MANUAL, "en", "partes")
INT_VOLUME = 4000.0
INT_TUTORIAL = dict(
    area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
    total_demand_per_day=600.0, rainwater_share=0.28,
)
#: O caso dos dez dias: 21 a 30 de setembro de 2018 da série de Nova York (dia 10125 de NewYork.csv).
INT_DEZ_DIAS_CHUVA = [0.0, 2.4, 1.9, 0.0, 59.8, 9.2, 5.5, 32.9, 0.0, 0.0]
INT_DEZ_DIAS = dict(
    lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
    total_demand_per_day=200.0, rainwater_share=0.40,
)
#: Custos ilustrativos do tutorial (US$): não são preços de mercado.
INT_CUSTOS = dict(cost_labor=1500.0, cost_piping=600.0, cost_accessories=800.0, pump_unit_cost=250.0,
                  elec_tariff=0.20, chlorine_cost_per_kg=8.0, tma=0.4, inflation=0.2,
                  analysis_period_years=20, tariff_escalation=12, water_tariff_escalation=3.0,
                  sewage_tariff_escalation=3.0, elec_tariff_escalation=3.0)
INT_PRECO_DO_TANQUE = {"PEAD": (100.0, 0.55), "CONCRETO": (600.0, 0.40)}   # base + por litro, ilustrativo
INT_FATOR_REDE, INT_FATOR_AGUA = 0.40, 0.50                                # kg CO2e, ilustrativos
#: Termos do Brasil e de Portugal que não podem aparecer nos arquivos de caso e nas tabelas da INT.
INT_TERMOS_PROIBIDOS = ("Florianópolis", "Florianopolis", "Manaus", "Brasília", "São Paulo", "CLIMBra",
                        "CMIP6", "CASAN", "R$", "NBR", "Netuno", "Santa Catarina", "Lisboa", "Funchal")


def _int_serie(nome):
    from triton.core.parser import load_precipitation
    caminho = os.path.join(INT_CHUVAS, nome + ".csv")
    if not os.path.exists(caminho):
        pytest.skip(f"série {nome} não instalada")
    return load_precipitation(caminho)


@pytest.fixture(scope="module")
def int_serie():
    return _int_serie("NewYork")


def _int_sim(serie, volume, **extra):
    return run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                 **{**INT_TUTORIAL, **extra})


def _int_preco(volume, material):
    base, por_litro = INT_PRECO_DO_TANQUE[material]
    return base + por_litro * float(volume)


def _int_exemplo_de_nova_york():
    from triton.core.parser import load_triton_project
    exemplo = os.path.join(RAIZ, "examples", "new_york.triton")
    if not os.path.exists(exemplo):
        pytest.skip("examples/new_york.triton ausente")
    return load_triton_project(exemplo)["config"]


def _int_economico(serie, volume, material):
    """A análise econômica do tutorial de Nova York, com a tarifa do exemplo e os custos ilustrativos."""
    from triton.core.economic import run_economic_analysis
    from triton.core.edition import configuracao_da_edicao
    ny = _int_exemplo_de_nova_york()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **INT_TUTORIAL)
    cfg = configuracao_da_edicao()
    for campo in ("water_tariffs", "sewage_mode", "sewage_rate", "sewage_tariffs",
                  "sewage_volume_factor", "water_tax_fixed", "water_tax_var"):
        setattr(cfg, campo, getattr(ny, campo))
    for k, v in INT_CUSTOS.items():
        setattr(cfg, k, v)
    cfg.op_costs = [("Gutter and pre-filter inspection and cleaning", 12, 20.0, 0.0),
                    ("Cistern cleaning and inspection", 12, 40.0, 0.0),
                    ("Preventive pump maintenance", 12, 30.0, 0.0)]
    cfg.cost_lower_tank = _int_preco(volume, material)
    cfg.cost_upper_tank = _int_preco(1000.0, "PEAD")
    cfg.supply_arrangement, cfg.upper_tank_used = "recalque", True
    cfg.upper_tank_vol, cfg.pumping_threshold, cfg.pump_count = 1000.0, 100.0, 2
    cfg.residents_count = 4
    cfg.area, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    return r, run_economic_analysis(cfg, r)


def _int_ambiental(material, resultado=None):
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.lower_material_key = material
    cfg.grid_co2_factor_kg_kwh = INT_FATOR_REDE
    cfg.potable_water_co2_kg_m3 = INT_FATOR_AGUA
    cfg.roof_area_m2, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    cfg.supply_arrangement, cfg.upper_tank_vol_liters = "recalque", 1000.0
    if resultado is not None:
        bomba = TritonConfig()
        bomba.supply_arrangement = "recalque"
        cfg.annual_pump_kwh = compute_annual_pump_energy(bomba, resultado).annual_kwh
    return cfg


def _int_lido(caminho):
    if not os.path.exists(caminho):
        pytest.skip(f"{os.path.relpath(caminho, RAIZ)} ainda não gerado")
    return open(caminho, encoding="utf-8").read()


def _int_capitulo(arquivo):
    """Capítulo em inglês com as tabelas incluídas; salta se o texto ainda não foi reapoiado nas cidades da INT.

    O texto da INT é escrito à parte (`manual/en/partes`). Enquanto o capítulo ainda cita algo do Brasil
    (`INT_TERMOS_PROIBIDOS`: cidades, CLIMBra, R$, NBR...), as asserções sobre o que ele cita ficam saltadas;
    assim que o capítulo deixa de citá-lo e passa a falar de Nova York, elas valem.
    """
    caminho = os.path.join(INT_PARTES, arquivo)
    if not os.path.exists(caminho):
        pytest.skip(f"{arquivo} ainda não escrito")
    saida = []
    for linha in open(caminho, encoding="utf-8").read().split(chr(10)):
        m = re.match(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$", linha)
        alvo = os.path.join(INT_PARTES, m.group(1)) if m else None
        saida.append(open(alvo, encoding="utf-8").read() if alvo and os.path.exists(alvo) else linha)
    texto = chr(10).join(saida)
    ainda = [x for x in INT_TERMOS_PROIBIDOS if x in texto]
    if ainda:
        pytest.skip(f"{arquivo} ainda não foi reapoiado nas cidades da INT (cita {', '.join(ainda[:3])})")
    return texto


# ── seção 2.1: o caso dos dez dias, com a chuva real de Nova York ───────────────────────────────

@pytest.fixture(scope="module")
def int_dez_dias():
    return run_single_simulation(precip_data=np.array(INT_DEZ_DIAS_CHUVA), store_daily_details=True,
                                 **INT_DEZ_DIAS)


def test_int_os_dez_dias_sao_os_de_nova_york(int_serie):
    """A janela está na série distribuída: 21/09/2018 é o dia 10125 de NewYork.csv (01/01/1991 = dia 0)."""
    import datetime as dt
    assert (dt.date(2018, 9, 21) - dt.date(1991, 1, 1)).days == 10125
    assert list(int_serie[10125:10135]) == pytest.approx(INT_DEZ_DIAS_CHUVA)


def test_int_o_potencial_e_os_indicadores_dos_dez_dias(int_dez_dias):
    """Impresso na seção 2.1: potencial 25,7%, 51,4 L/dia pluviais, 620,9 L/dia extravasados, dias 60/10/30%."""
    r = int_dez_dias
    assert r.potential_potable_savings_pct == pytest.approx(25.7, abs=0.05)
    assert r.avg_pluvial_consumed_l_day == pytest.approx(51.4, abs=0.05)
    assert r.avg_potable_consumed_l_day == pytest.approx(148.6, abs=0.05)
    assert r.avg_spilled_l_day == pytest.approx(620.9, abs=0.05)
    assert r.pct_days_full_satisfaction == pytest.approx(60.0, abs=0.5)
    assert r.pct_days_partial_satisfaction == pytest.approx(10.0, abs=0.5)
    assert r.pct_days_null_satisfaction == pytest.approx(30.0, abs=0.5)


def test_int_o_dia_2_e_parcial_e_o_dia_3_se_perde_inteiro(int_dez_dias):
    """Dia 2: 2,4 mm, 0,4 mm efetivos, 34 L e atendimento parcial. Dia 3: 1,9 mm < 2,0 mm, capta-se zero."""
    d2, d3 = int_dez_dias.daily_results[1], int_dez_dias.daily_results[2]
    assert d2.satisfaction_type == 1
    assert d2.harvested_liters == pytest.approx(34.0, abs=1.0)
    assert d2.pluvial_consumed_liters == pytest.approx(34.0, abs=1.0)
    assert d3.precip_mm == pytest.approx(1.9)
    assert d3.eff_precip_mm == pytest.approx(0.0)
    assert d3.harvested_liters == pytest.approx(0.0)
    assert d3.satisfaction_type == 0


def test_int_o_dia_5_extravasa_mais_que_o_reservatorio(int_dez_dias):
    """Dia 5 (59,8 mm): 4.913 L captados, 2.913 L extravasados, 1.920 L no reservatório."""
    d = int_dez_dias.daily_results[4]
    assert d.harvested_liters == pytest.approx(4913.0, abs=1.0)
    assert d.spilled_liters == pytest.approx(2913.0, abs=1.0)
    assert d.lower_tank_end_liters == pytest.approx(1920.0, abs=1.0)
    assert d.spilled_liters > INT_DEZ_DIAS["lower_tank_vol"]


def test_int_o_dia_8_extravasa_antes_de_consumir(int_dez_dias):
    """Dia 8 (32,9 mm): 2.626 L captados e 2.546 L extravasados; o reservatório já estava cheio no dia 7."""
    d7, d8 = int_dez_dias.daily_results[6], int_dez_dias.daily_results[7]
    assert d7.spilled_liters == pytest.approx(218.0, abs=1.0)
    assert d8.harvested_liters == pytest.approx(2626.0, abs=1.0)
    assert d8.spilled_liters == pytest.approx(2546.0, abs=1.0)


def test_int_as_somas_dos_dez_dias_fecham(int_dez_dias):
    """Impresso: 8.483 L captados, 6.209 L extravasados, 514 L consumidos, 1.760 L ao fim; resíduo zero."""
    d = int_dez_dias.daily_results
    captado = sum(x.harvested_liters for x in d)
    extravasado = sum(x.spilled_liters for x in d)
    consumido = sum(x.pluvial_consumed_liters for x in d)
    final = d[-1].lower_tank_end_liters
    assert captado == pytest.approx(8483.0, abs=1.0)
    assert extravasado == pytest.approx(6209.0, abs=1.0)
    assert consumido == pytest.approx(514.0, abs=1.0)
    assert final == pytest.approx(1760.0, abs=1.0)
    assert captado - extravasado - consumido - final == pytest.approx(0.0, abs=0.5)


def test_int_a_tabela_publicada_dos_dez_dias_bate_com_a_simulacao(int_dez_dias):
    """Se alguém editar a tabela à mão, este teste pega."""
    texto = _int_lido(os.path.join(INT_TABELAS, "cap23_dez_dias.md"))
    dias = []
    for linha in texto.split(chr(10)):
        celulas = [c.strip() for c in linha.strip("|").split("|")] if linha.startswith("| ") else []
        if celulas and celulas[0].isdigit():
            dias.append([c.replace(",", "") for c in celulas])
    assert len(dias) == 10
    for i, c in enumerate(dias):
        d = int_dez_dias.daily_results[i]
        assert float(c[1]) == pytest.approx(d.precip_mm, abs=0.05), f"dia {i+1} chuva"
        assert float(c[3]) == pytest.approx(d.eff_precip_mm, abs=0.05), f"dia {i+1} efetiva"
        assert float(c[4]) == pytest.approx(d.harvested_liters, abs=1.0), f"dia {i+1} captado"
        assert float(c[6]) == pytest.approx(d.pluvial_consumed_liters, abs=1.0), f"dia {i+1} consumido"
        assert float(c[7]) == pytest.approx(d.spilled_liters, abs=1.0), f"dia {i+1} extravasado"


# ── o tutorial de Nova York: capítulos 4 a 7 ────────────────────────────────────────────────────

def test_int_a_serie_do_tutorial_e_a_que_o_capitulo_4_descreve(int_serie):
    """Impresso: 30 anos, 1.125 mm/ano, chuva em 44% dos dias, maior chuva diária 128,2 mm."""
    anos = len(int_serie) / 365.25
    assert anos == pytest.approx(30.0, abs=0.1)
    assert int_serie.sum() / anos == pytest.approx(1125.0, abs=3.0)
    assert (int_serie > 0.1).mean() * 100 == pytest.approx(44.0, abs=1.0)
    assert int_serie.max() == pytest.approx(128.2, abs=0.05)


def test_int_o_descarte_atinge_dezessete_por_cento_dos_dias(int_serie):
    """Impresso: 17% dos dias têm chuva (acima de 0,1 mm) mas abaixo da lâmina de descarte de 2 mm."""
    abaixo = ((int_serie > 0.1) & (int_serie <= 2.0)).mean() * 100
    assert abaixo == pytest.approx(17.0, abs=1.0)


def test_int_a_oferta_bruta_e_mais_que_o_dobro_da_demanda(int_serie):
    """Impresso no capítulo 5: 143 m³/ano de oferta bruta contra 61 m³/ano de demanda pluvial."""
    anos = len(int_serie) / 365.25
    bruta = int_serie.sum() / anos * INT_TUTORIAL["area"] * INT_TUTORIAL["runoff_coeff"] / 1000.0
    demanda = INT_TUTORIAL["total_demand_per_day"] * INT_TUTORIAL["rainwater_share"] * 365.25 / 1000.0
    assert bruta == pytest.approx(143.0, abs=1.0)
    assert demanda == pytest.approx(61.0, abs=1.0)
    assert bruta > 2 * demanda


def test_int_a_primeira_simulacao_do_capitulo_6(int_serie):
    """Impresso: 25,99% com 3.000 L, 150,8 L/dia extravasados, 91,9% de dias plenos, 57,0 m³/ano."""
    r = _int_sim(int_serie, 3000)
    assert r.potential_potable_savings_pct == pytest.approx(25.99, abs=0.05)
    assert r.avg_spilled_l_day == pytest.approx(150.8, abs=0.1)
    assert r.pct_days_full_satisfaction == pytest.approx(91.9, abs=0.1)
    assert r.annual_pluvial_consumed_m3 == pytest.approx(57.0, abs=0.1)
    assert r.avg_pluvial_consumed_l_day == pytest.approx(155.9, abs=0.1)


@pytest.mark.parametrize(("volume", "potencial"), [
    (1000, 19.14), (2000, 24.24), (3000, 25.99), (4000, 26.83), (5000, 27.24),
    (8000, 27.74), (12000, 27.94), (20000, 27.98),
])
def test_int_a_curva_de_varredura_do_capitulo_7(int_serie, volume, potencial):
    """Cada linha da tabela impressa no capítulo 7."""
    assert _int_sim(int_serie, volume).potential_potable_savings_pct == pytest.approx(potencial, abs=0.05)


def test_int_o_potencial_nunca_passa_da_fracao_atendivel(int_serie):
    teto = INT_TUTORIAL["rainwater_share"] * 100.0
    for v in (1000, 4000, 20000, 100000):
        assert _int_sim(int_serie, v).potential_potable_savings_pct <= teto + 1e-9


@pytest.mark.parametrize(("limiar", "ideal"), [(3.0, 3000), (1.0, 4000), (0.5, 5000)])
def test_int_o_limiar_decide_o_volume_ideal(int_serie, limiar, ideal):
    from triton.core.simulation import run_sweep_simulation
    r = run_sweep_simulation(precip_data=int_serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
                             delta_ideal_threshold=limiar, **INT_TUTORIAL)
    assert r.optimal_lower_tank_vol == pytest.approx(ideal)


def test_int_o_volume_maior_custa_muito_mais_por_pouco_ganho(int_serie):
    """Impresso: 3,9× o preço (ilustrativo) e 4,1× o carbono por 1,15 ponto."""
    from triton.core.environmental import calculate_lca
    r4, r20 = _int_sim(int_serie, INT_VOLUME), _int_sim(int_serie, 20000)
    assert r20.potential_potable_savings_pct - r4.potential_potable_savings_pct == pytest.approx(1.15, abs=0.05)
    assert _int_preco(20000, "CONCRETO") / _int_preco(INT_VOLUME, "CONCRETO") == pytest.approx(3.9, abs=0.1)
    cfg = _int_ambiental("CONCRETO")
    c4 = calculate_lca(INT_VOLUME, r4.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    c20 = calculate_lca(20000.0, r20.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    assert c20 / c4 == pytest.approx(4.1, abs=0.1)


# ── capítulos 8 a 12: a caixa superior, o custo (ilustrativo), o carbono, a decisão ──────────────

def test_int_a_caixa_superior_nao_aumenta_a_economia(int_serie):
    """Impresso no capítulo 8: com o mesmo armazenamento (5.000 L), o arranjo duplo perde 0,15 ponto."""
    unico = _int_sim(int_serie, INT_VOLUME + 1000.0)
    duplo = _int_sim(int_serie, INT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0)
    assert unico.potential_potable_savings_pct == pytest.approx(27.24, abs=0.05)
    assert duplo.potential_potable_savings_pct == pytest.approx(27.09, abs=0.05)
    assert unico.potential_potable_savings_pct - duplo.potential_potable_savings_pct == pytest.approx(0.15, abs=0.03)


def test_int_a_energia_do_recalque_do_capitulo_8(int_serie):
    """Impresso: 7,7 kWh/ano e 69 acionamentos por ano."""
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    duplo = _int_sim(int_serie, INT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0)
    cfg = TritonConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw, cfg.pump_efficiency, cfg.pump_flow_rate = 0.37, 0.0, 0.0
    cfg.pump_manometric_head_m, cfg.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(cfg, duplo)
    assert e.annual_kwh == pytest.approx(7.7, abs=0.3)
    assert e.annual_cycles == pytest.approx(69, abs=3)


def test_int_o_limiar_de_acionamento_troca_potencial_por_desgaste(int_serie):
    anterior, potencial = None, None
    for limiar in (0, 100, 300, 500):
        r = _int_sim(int_serie, INT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True,
                     pumping_threshold=float(limiar))
        ciclos = r.total_pump_cycles / (r.total_days / 365.25)
        if anterior is not None:
            assert ciclos >= anterior
            assert r.potential_potable_savings_pct >= potencial - 1e-9
        anterior, potencial = ciclos, r.potential_potable_savings_pct


def test_int_o_resultado_economico_do_capitulo_10(int_serie):
    """Impresso (custos ILUSTRATIVOS, US$): investimento 6.250; economia anual 290,53; VPL -2.919,90; sem payback.

    A tarifa de Nova York é a publicada (`examples/new_york.triton`); a análise não se paga com estes
    custos, e o capítulo diz isso em vez de ajustar os custos até o payback aparecer.
    """
    _, e = _int_economico(int_serie, INT_VOLUME, "CONCRETO")
    assert e.capex_total == pytest.approx(6250.0, abs=1.0)
    assert e.annual_water_savings_brl == pytest.approx(290.53, abs=3.0)
    assert e.vpl == pytest.approx(-2919.9, abs=50.0)
    assert not e.payback_years


def test_int_a_conta_de_nova_york_com_e_sem_o_sistema(int_serie):
    """Impresso: US$ 89,37 sem o sistema, US$ 65,15 com ele, economia de US$ 24,21 por mês."""
    from triton.core.economic import calculate_water_bill
    ny = _int_exemplo_de_nova_york()
    r = run_single_simulation(precip_data=int_serie, lower_tank_vol=INT_VOLUME, upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **INT_TUTORIAL)
    dias = 30.4375

    def conta(l_dia):
        return calculate_water_bill(l_dia * dias, ny.water_tariffs, ny.sewage_mode, ny.sewage_rate,
                                    ny.water_tax_fixed, ny.water_tax_var,
                                    sewage_tariffs=ny.sewage_tariffs, sewage_volume_factor=ny.sewage_volume_factor)
    sem = conta(r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day)
    com = conta(r.avg_potable_consumed_l_day)
    assert sem == pytest.approx(89.37, abs=0.05)
    assert com == pytest.approx(65.15, abs=0.05)
    assert sem - com == pytest.approx(24.21, abs=0.05)


def test_int_a_troca_para_polietileno_inverte_o_sinal_do_carbono(int_serie):
    """Impresso no capítulo 11: em polietileno o carbono se paga em 12,4 anos; em concreto, em 32,5 (> 20)."""
    from triton.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=int_serie, lower_tank_vol=INT_VOLUME, upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **INT_TUTORIAL)
    lca = {k: calculate_lca(INT_VOLUME, r.annual_pluvial_consumed_m3, _int_ambiental(k, r))
           for k in ("PEAD", "CONCRETO")}
    assert lca["PEAD"].lifetime_net_co2_saved_kg > 0
    assert lca["CONCRETO"].lifetime_net_co2_saved_kg < 0
    assert lca["PEAD"].environmental_payback_years == pytest.approx(12.4, abs=0.3)
    assert lca["CONCRETO"].environmental_payback_years == pytest.approx(32.5, abs=0.5)
    assert lca["PEAD"].total_embodied_co2_kg == pytest.approx(327.0, abs=2.0)
    assert lca["CONCRETO"].total_embodied_co2_kg == pytest.approx(858.0, abs=2.0)


def test_int_os_tres_criterios_do_capitulo_12_discordam(int_serie):
    """Impresso: técnico 12.000 L, econômico 2.000 L, ambiental 2.000 L, compromisso 4.000 L."""
    from triton.core.environmental import calculate_lca
    from triton.core.topsis import TopsisCandidate, calculate_topsis_scores
    cands = []
    for v in (1000, 2000, 3000, 4000, 5000, 8000, 12000):
        r, e = _int_economico(int_serie, v, "PEAD")
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, _int_ambiental("PEAD", r))
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v), water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg, capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct, overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years, irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))
    res = calculate_topsis_scores(cands)
    assert cands[res.technical_best_index].lower_tank_vol == 12000.0
    assert cands[res.financial_best_index].lower_tank_vol == 2000.0
    assert cands[res.environmental_best_index].lower_tank_vol == 2000.0
    assert cands[res.best_index].lower_tank_vol == INT_VOLUME


# ── seção 3.1: as cidades de comparação ─────────────────────────────────────────────────────────

def test_int_as_cidades_da_secao_3_1():
    """Impresso: o mesmo projeto rende 26,83% em Nova York, 20,08% em Londres e 14,52% na Cidade do Cabo.

    A Cidade do Cabo chove menos que Londres e rende menos porque a chuva é de inverno: a razão entre o
    mês mais e o menos chuvoso é 8,3×, contra 1,4× e 1,5×. O volume ideal é 4.000 L nas três.
    """
    from datetime import datetime, timedelta

    from triton.core.simulation import run_sweep_simulation
    res = {}
    for chave in ("NewYork", "London", "CapeTown"):
        serie = _int_serie(chave)
        anos = len(serie) / 365.25
        r = _int_sim(serie, INT_VOLUME)
        sw = run_sweep_simulation(precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
                                  delta_ideal_threshold=1.0, **INT_TUTORIAL)
        d0, meses = datetime(1991, 1, 1), np.zeros(12)
        for i, v in enumerate(serie):
            meses[(d0 + timedelta(days=i)).month - 1] += float(v)
        meses /= anos
        res[chave] = (serie.sum() / anos, r.potential_potable_savings_pct, meses.max() / max(meses.min(), 0.1),
                      sw.optimal_lower_tank_vol)
    ny, lo, ct = res["NewYork"], res["London"], res["CapeTown"]
    assert ny[0] > lo[0] > ct[0]
    assert ny[1] == pytest.approx(26.83, abs=0.05)
    assert lo[1] == pytest.approx(20.08, abs=0.05)
    assert ct[1] == pytest.approx(14.52, abs=0.05)
    assert ny[0] == pytest.approx(1125.0, abs=3.0) and lo[0] == pytest.approx(649.0, abs=3.0) \
        and ct[0] == pytest.approx(495.0, abs=3.0)
    assert ct[2] > 5 * max(ny[2], lo[2])
    assert ny[2] == pytest.approx(1.4, abs=0.1) and lo[2] == pytest.approx(1.5, abs=0.1) \
        and ct[2] == pytest.approx(8.3, abs=0.2)
    assert ny[3] == lo[3] == ct[3] == 4000.0


# ── os arquivos de caso e as tabelas ────────────────────────────────────────────────────────────

INT_CASOS_ESPERADOS = {
    "01_tutorial_new_york.triton": ("volume fixo", 27.09),
    "02_london.triton": ("volume fixo", 20.08),
    "03_cape_town.triton": ("volume fixo", 14.52),
    "04_tutorial_sweep.triton": ("varredura", 26.83),
    "05_ten_days.triton": ("volume fixo", 25.70),
    "06_upper_tank.triton": ("volume fixo", 27.09),
    "07_school_weekly.triton": ("volume fixo", 12.58),
    "08_hotel_monthly.triton": ("volume fixo", 9.83),
    "09_modulation_tutorial.triton": ("varredura", 26.83),
    "10_modulation_catchment.triton": ("varredura", 26.83),
}


def _int_resultados():
    import json
    return json.loads(_int_lido(os.path.join(INT_CASOS, "resultados.json")))


def test_int_os_casos_publicados_sao_os_da_edicao():
    pub = _int_resultados()
    assert sorted(pub) == sorted(INT_CASOS_ESPERADOS)
    for arquivo, (modo, potencial) in INT_CASOS_ESPERADOS.items():
        assert pub[arquivo]["modo"] == modo, arquivo
        assert pub[arquivo]["potencial_pct"] == pytest.approx(potencial, abs=0.01), arquivo
        assert os.path.exists(os.path.join(INT_CASOS, arquivo)), arquivo


def test_int_os_casos_batem_com_as_tabelas_e_os_capitulos():
    """O caso de Nova York com volume fixo é o da tabela de varredura; o de dez dias, o da tabela dos dez dias."""
    pub = _int_resultados()
    assert pub["04_tutorial_sweep.triton"]["volume_ideal_l"] == 4000.0
    assert pub["04_tutorial_sweep.triton"]["volumes_simulados"] == 21
    d = pub["05_ten_days.triton"]
    assert (d["volume_l"], d["dias_de_chuva"]) == (2000.0, 10)
    assert d["pluvial_l_dia"] == pytest.approx(51.4) and d["extravasado_l_dia"] == pytest.approx(620.9)
    assert d["atendimento_pleno_pct"] == pytest.approx(60.0)
    # A caixa superior de 1.000 L perde 0,15 ponto contra um tanque só de 5.000 L.
    u = pub["06_upper_tank.triton"]
    assert u["potencial_tanque_unico_pct"] - u["potencial_pct"] == pytest.approx(0.15, abs=0.01)
    # O mesmo projeto em três chuvas.
    assert pub["01_tutorial_new_york.triton"]["atendimento_pleno_pct"] == pytest.approx(96.4)
    assert pub["02_london.triton"]["atendimento_pleno_pct"] == pytest.approx(69.1)
    assert pub["03_cape_town.triton"]["atendimento_pleno_pct"] == pytest.approx(49.9)


def test_int_o_calendario_concentrado_rende_menos_que_a_demanda_constante():
    """Seção 3.4: o hotel (cheio de dezembro a fevereiro, estação seca da Cidade do Cabo) perde 1,14 ponto
    contra a mesma demanda anual espalhada; a escola semanal de Londres, que só fecha no fim de semana, quase não muda."""
    pub = _int_resultados()
    hotel, escola = pub["08_hotel_monthly.triton"], pub["07_school_weekly.triton"]
    assert hotel["potencial_demanda_constante_pct"] - hotel["potencial_pct"] == pytest.approx(1.14, abs=0.02)
    assert hotel["demanda_media_l_dia"] == pytest.approx(5779.9, abs=0.1)
    assert abs(escola["potencial_demanda_constante_pct"] - escola["potencial_pct"]) < 0.2
    assert escola["demanda_media_l_dia"] == pytest.approx(9014.3, abs=0.1)


def test_int_todo_caso_do_manual_reproduz_o_numero_publicado():
    """O arquivo gravado, relido e simulado dá o número publicado (o campo que se perca aparece aqui)."""
    import sys
    sys.path.insert(0, MANUAL)
    try:
        from gerar_casos import simular_do_arquivo
    except ImportError:
        pytest.skip("gerador de casos ausente")
    for arquivo, publicado in sorted(_int_resultados().items()):
        obtido = simular_do_arquivo(os.path.join(INT_CASOS, arquivo))
        assert obtido["potencial_pct"] == pytest.approx(publicado["potencial_pct"], abs=0.05), arquivo
        assert obtido["modo"] == publicado["modo"], arquivo


def test_int_os_casos_de_modulacao_abrem_com_a_modulacao_montada():
    import json
    for arquivo, chaves in (("09_modulation_tutorial.triton", {"per_capita_l_dia", "pessoas", "fator_chuva"}),
                            ("10_modulation_catchment.triton", {"area_m2", "coef_escoamento", "fator_chuva"})):
        d = json.loads(_int_lido(os.path.join(INT_CASOS, arquivo)))
        mod = d["ui_state"]["modulacao_estocastica"]
        marcadas = {k for k, v in mod["parametros"]["variaveis"].items() if v.get("variar")}
        assert chaves <= marcadas, arquivo
        assert (mod["amostras"], mod["semente"]) == (1000, 42), arquivo
        assert not mod["parametros"].get("modelos_climaticos"), arquivo


def test_int_os_casos_e_as_tabelas_nao_trazem_nada_do_brasil_nem_de_portugal():
    """Nenhum arquivo de caso, README, resultado ou tabela da INT cita cidade, norma ou moeda da BRL/PRT."""
    achados = []
    arquivos = [os.path.join(INT_CASOS, f) for f in sorted(os.listdir(INT_CASOS))
                if f.endswith((".triton", ".json", ".md", ".csv"))]
    if os.path.isdir(INT_TABELAS):
        arquivos += [os.path.join(INT_TABELAS, f) for f in sorted(os.listdir(INT_TABELAS))
                     if f.endswith(".md") and not f.startswith(("cap38", "cap40", "cap43"))]
    if not arquivos:
        pytest.skip("casos ainda não gerados")
    for caminho in arquivos:
        texto = open(caminho, encoding="utf-8").read()
        for termo in INT_TERMOS_PROIBIDOS:
            if termo in texto:
                achados.append(f"{os.path.relpath(caminho, MANUAL)}: {termo}")
    assert not achados, achados


def test_int_todo_valor_em_dinheiro_das_tabelas_e_ilustrativo_e_rotulado():
    """Regra 6: custo de obra, energia e preço de tanque levam «illustrative, not a market price» na legenda ou na linha."""
    if not os.path.isdir(INT_TABELAS):
        pytest.skip("tabelas ainda não geradas")
    faltando = []
    for nome in ("cap07_limiar_e_custo.md", "cap08_reservatorio_superior.md", "cap10_economico.md",
                 "cap11_materiais.md", "cap12_multicriterio.md", "cap20_sensibilidade.md"):
        texto = _int_lido(os.path.join(INT_TABELAS, nome))
        for bloco in texto.split("<!-- tabela: ")[1:]:
            legenda, _, corpo = bloco.partition(" -->")
            cabeca = corpo.split(chr(10))[1]
            if "New York water and sewer bill" in legenda:
                continue          # a tarifa publicada, e não um custo
            if "US$" in corpo and "illustrative" not in (legenda + cabeca):
                faltando.append(f"{nome}: {legenda[:50]}")
    assert not faltando, faltando


# ── o que o texto em inglês cita ────────────────────────────────────────────────────────────────

#: Para cada capítulo, o que ele tem de citar do programa. Cada capítulo vale a partir do momento em que
#: deixa de citar o Brasil (`_int_capitulo`); antes disso, é saltado, sem esconder os demais.
INT_CITACOES = {
    "23_balanco_diario.md": ("25.7%", "8,483 L", "6,209 L", "514 L", "4,913 L", "2,913 L", "2,546 L",
                             "34 L", "1,760 L"),
    "04_o_projeto_e_a_chuva.md": ("150 m²", "0.85", "2.0 mm", "1,125 mm", "New York"),
    "05_a_edificacao_e_a_demanda.md": ("600 L/day", "168 L/day", "28%", "61"),
    "06_a_primeira_simulacao.md": ("25.99%", "150.8 L/day", "91.9%", "3,000"),
    "07_escolher_o_volume.md": ("4,000 L", "26.83%", "95.3%", "27.98%"),
    "08_reservatorio_superior.md": ("7.7 kWh", "5,000 L"),
    "10_quanto_custa.md": ("US$ 24.21", "illustrative"),
    "11_quanto_carbono_evita.md": ("858 kg", "32.5 years", "12.4 years"),
    "12_qual_volume_escolher.md": ("4,000 L", "12,000 L", "2,000 L", "27.09%"),
    "14_comparar_cidades.md": ("London", "Cape Town", "26.83%", "20.08%", "14.52%", "8.3"),
}


@pytest.mark.parametrize("arquivo", sorted(INT_CITACOES))
def test_int_o_capitulo_cita_os_numeros_do_programa(arquivo):
    texto = _int_capitulo(arquivo)
    for termo in INT_CITACOES[arquivo]:
        assert termo in texto, f"{arquivo} não cita {termo}"


# ══════════════════════════════════════════════════════════════════════════════
# Edição Portugal (PRT): Lisboa, Porto e Funchal
# ══════════════════════════════════════════════════════════════════════════════
#
# O tutorial da PRT é a mesma casa (150 m², 4 residentes, 150 L/hab·dia, 28% não potável) em Lisboa,
# com a chuva E-OBS por concelho (normal 1991-2020, `data/portugal_eobs.db`) e o tarifário transcrito
# em `triton/data/portugal_tarifarios.json`; o Porto (E-OBS) e o Funchal (ERA5, `data/rainfall/Funchal.csv`)
# são as cidades de comparação. Os custos são ILUSTRATIVOS (euros, números redondos declarados em
# `manual/gerar_tabelas.py`), nunca preços de mercado. Os valores abaixo são os que `manual/gerar_tabelas.py`
# e `manual/gerar_casos.py` produzem; o texto em português de Portugal cita os mesmos.
#
# Os números de texto levam o espaço inseparável do milhar (U+00A0): as tabelas e os capítulos são lidos
# com ele trocado por espaço comum, de modo que o teste não dependa de qual espaço o redator usou.

PRT_CHUVAS = os.path.join(RAIZ, "data", "rainfall")
PRT_CASOS = os.path.join(MANUAL, "casos")
PRT_TABELAS = os.path.join(MANUAL, "partes", "_tabelas")
PRT_PARTES = os.path.join(MANUAL, "partes")
PRT_VOLUME = 5000.0
PRT_TUTORIAL = dict(
    area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
    total_demand_per_day=600.0, rainwater_share=0.28,
)
#: O caso dos dez dias: 11 a 20 de dezembro de 2019 da série de Lisboa (dia 10571; 01/01/1991 = dia 0).
PRT_DEZ_DIAS_CHUVA = [0.0, 2.1, 0.0, 1.2, 6.0, 13.5, 0.7, 8.1, 35.7, 25.8]
PRT_DEZ_DIAS = dict(
    lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
    total_demand_per_day=200.0, rainwater_share=0.40,
)
#: Custos ilustrativos do tutorial (euros): não são preços de mercado.
PRT_CUSTOS = dict(cost_labor=1500.0, cost_piping=600.0, cost_accessories=800.0, pump_unit_cost=250.0,
                  elec_tariff=0.20, chlorine_cost_per_kg=8.0, tma=0.4, inflation=0.2,
                  analysis_period_years=20, tariff_escalation=12, water_tariff_escalation=3.0,
                  sewage_tariff_escalation=3.0, elec_tariff_escalation=3.0)
PRT_PRECO_DO_TANQUE = {"PEAD": (100.0, 0.55), "CONCRETO": (600.0, 0.40)}   # base + por litro, ilustrativo
PRT_FATOR_REDE, PRT_FATOR_AGUA = 0.40, 0.50                                # kg CO2e, ilustrativos
#: Termos do Brasil que não podem aparecer nos ficheiros de caso e nas tabelas da PRT.
PRT_TERMOS_PROIBIDOS = ("Florianópolis", "Florianopolis", "Manaus", "Brasília", "São Paulo", "CLIMBra",
                        "CMIP6", "CASAN", "R$", "NBR", "Netuno", "Santa Catarina", "IPTU", "SABESP")


def _prt_serie(nome):
    """A série diária de 1991-2020 da cidade: E-OBS por concelho (Lisboa, Porto) ou ERA5 (Funchal)."""
    if nome == "Funchal":
        from triton.core.parser import load_precipitation
        caminho = os.path.join(PRT_CHUVAS, "Funchal.csv")
        if not os.path.exists(caminho):
            pytest.skip("série do Funchal não instalada")
        return load_precipitation(caminho)
    from triton.core import base_climatica_portugal as pt
    if not pt.disponivel():
        pytest.skip("base E-OBS de Portugal (data/portugal_eobs.db) não instalada")
    return pt.carregar_serie(nome, "01/01/1991", "31/12/2020")[0]


@pytest.fixture(scope="module")
def prt_serie():
    return _prt_serie("Lisboa")


def _prt_sim(serie, volume, **extra):
    return run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                 **{**PRT_TUTORIAL, **extra})


def _prt_preco(volume, material):
    base, por_litro = PRT_PRECO_DO_TANQUE[material]
    return base + por_litro * float(volume)


def _prt_config_de_lisboa():
    """A configuração da edição com o tarifário de Lisboa transcrito."""
    from triton.core import tarifarios_portugal as tarifas
    from triton.core.edition import configuracao_da_edicao
    cfg = configuracao_da_edicao()
    assert tarifas.aplicar("Lisboa", cfg), "tarifário de Lisboa ausente"
    return cfg


def _prt_economico(serie, volume, material):
    """A análise económica do tutorial de Lisboa, com o tarifário transcrito e os custos ilustrativos."""
    from triton.core.economic import run_economic_analysis
    r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **PRT_TUTORIAL)
    cfg = _prt_config_de_lisboa()
    for k, v in PRT_CUSTOS.items():
        setattr(cfg, k, v)
    cfg.op_costs = [("Inspeção e limpeza das caleiras e do pré-filtro", 12, 20.0, 0.0),
                    ("Limpeza e inspeção da cisterna", 12, 40.0, 0.0),
                    ("Manutenção preventiva da bomba", 12, 30.0, 0.0)]
    cfg.cost_lower_tank = _prt_preco(volume, material)
    cfg.cost_upper_tank = _prt_preco(1000.0, "PEAD")
    cfg.supply_arrangement, cfg.upper_tank_used = "recalque", True
    cfg.upper_tank_vol, cfg.pumping_threshold, cfg.pump_count = 1000.0, 100.0, 2
    cfg.residents_count = 4
    cfg.area, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    return r, run_economic_analysis(cfg, r)


def _prt_ambiental(material, resultado=None):
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.lower_material_key = material
    cfg.grid_co2_factor_kg_kwh = PRT_FATOR_REDE
    cfg.potable_water_co2_kg_m3 = PRT_FATOR_AGUA
    cfg.roof_area_m2, cfg.discard, cfg.first_flush_system_enabled = 150.0, 2.0, True
    cfg.supply_arrangement, cfg.upper_tank_vol_liters = "recalque", 1000.0
    if resultado is not None:
        bomba = TritonConfig()
        bomba.supply_arrangement = "recalque"
        cfg.annual_pump_kwh = compute_annual_pump_energy(bomba, resultado).annual_kwh
    return cfg


def _prt_normalizado(texto):
    """O texto com os espaços inseparáveis (milhar, antes de «€») trocados por espaço comum."""
    return texto.replace(chr(160), " ").replace(chr(0x202F), " ")


def _prt_lido(caminho):
    if not os.path.exists(caminho):
        pytest.skip(f"{os.path.relpath(caminho, RAIZ)} ainda não gerado")
    return _prt_normalizado(open(caminho, encoding="utf-8").read())


def _prt_capitulo(arquivo):
    """Capítulo em português de Portugal com as tabelas incluídas; salta se o texto ainda cita o Brasil.

    O texto da PRT é escrito à parte (`manual/partes`). Enquanto o capítulo ainda cita algo do Brasil
    (`PRT_TERMOS_PROIBIDOS`: cidades, CLIMBra, R$, NBR...), as asserções sobre o que ele cita ficam
    saltadas; assim que o capítulo deixa de o citar e passa a falar de Lisboa, elas valem.
    """
    caminho = os.path.join(PRT_PARTES, arquivo)
    if not os.path.exists(caminho):
        pytest.skip(f"{arquivo} ainda não escrito")
    saida = []
    for linha in open(caminho, encoding="utf-8").read().split(chr(10)):
        m = re.match(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$", linha)
        alvo = os.path.join(PRT_PARTES, m.group(1)) if m else None
        saida.append(open(alvo, encoding="utf-8").read() if alvo and os.path.exists(alvo) else linha)
    texto = _prt_normalizado(chr(10).join(saida))
    ainda = [x for x in PRT_TERMOS_PROIBIDOS if x in texto]
    if ainda:
        pytest.skip(f"{arquivo} ainda não foi reapoiado nas cidades da PRT (cita {', '.join(ainda[:3])})")
    return texto


# ── secção 2.1: o caso dos dez dias, com a chuva real de Lisboa ─────────────────────────────────

@pytest.fixture(scope="module")
def prt_dez_dias():
    return run_single_simulation(precip_data=np.array(PRT_DEZ_DIAS_CHUVA), store_daily_details=True,
                                 **PRT_DEZ_DIAS)


def test_prt_os_dez_dias_sao_os_de_lisboa(prt_serie):
    """A janela está na série da base E-OBS: 11/12/2019 é o dia 10571 (01/01/1991 = dia 0), ao décimo de mm."""
    import datetime as dt
    assert (dt.date(2019, 12, 11) - dt.date(1991, 1, 1)).days == 10571
    assert [round(float(x), 1) for x in prt_serie[10571:10581]] == pytest.approx(PRT_DEZ_DIAS_CHUVA)


def test_prt_o_potencial_e_os_indicadores_dos_dez_dias(prt_dez_dias):
    """Impresso na secção 2.1: potencial 24,4%, 48,9 L/dia pluviais, 432,4 L/dia extravasados, dias 60/10/30%."""
    r = prt_dez_dias
    assert r.potential_potable_savings_pct == pytest.approx(24.4, abs=0.05)
    assert r.avg_pluvial_consumed_l_day == pytest.approx(48.9, abs=0.05)
    assert r.avg_potable_consumed_l_day == pytest.approx(151.1, abs=0.15)
    assert r.avg_spilled_l_day == pytest.approx(432.4, abs=0.05)
    assert r.pct_days_full_satisfaction == pytest.approx(60.0, abs=0.5)
    assert r.pct_days_partial_satisfaction == pytest.approx(10.0, abs=0.5)
    assert r.pct_days_null_satisfaction == pytest.approx(30.0, abs=0.5)


def test_prt_o_dia_2_e_parcial_e_o_dia_4_se_perde_inteiro(prt_dez_dias):
    """Dia 2: 2,1 mm, 0,1 mm efetivo, 9 L e abastecimento parcial. Dia 4: 1,2 mm < 2,0 mm, capta-se zero."""
    d2, d4 = prt_dez_dias.daily_results[1], prt_dez_dias.daily_results[3]
    assert d2.satisfaction_type == 1
    assert d2.eff_precip_mm == pytest.approx(0.1, abs=0.01)
    assert d2.harvested_liters == pytest.approx(9.0, abs=1.0)
    assert d2.pluvial_consumed_liters == pytest.approx(9.0, abs=1.0)
    assert d4.precip_mm == pytest.approx(1.2)
    assert d4.eff_precip_mm == pytest.approx(0.0)
    assert d4.harvested_liters == pytest.approx(0.0)
    assert d4.satisfaction_type == 0


def test_prt_o_dia_9_extravasa_mais_que_o_reservatorio(prt_dez_dias):
    """Dia 9 (35,7 mm): 2.865 L captados, 2.380 L extravasados, 1.920 L no reservatório."""
    d = prt_dez_dias.daily_results[8]
    assert d.harvested_liters == pytest.approx(2865.0, abs=1.0)
    assert d.spilled_liters == pytest.approx(2380.0, abs=1.0)
    assert d.lower_tank_end_liters == pytest.approx(1920.0, abs=1.0)
    assert d.spilled_liters > PRT_DEZ_DIAS["lower_tank_vol"]


def test_prt_o_dia_10_extravasa_com_o_reservatorio_ja_cheio(prt_dez_dias):
    """Dia 10 (25,8 mm): 2.023 L captados e 1.943 L extravasados; o reservatório acabara o dia 9 com 1.920 L."""
    d9, d10 = prt_dez_dias.daily_results[8], prt_dez_dias.daily_results[9]
    assert d9.lower_tank_end_liters == pytest.approx(1920.0, abs=1.0)
    assert d10.harvested_liters == pytest.approx(2023.0, abs=1.0)
    assert d10.spilled_liters == pytest.approx(1943.0, abs=1.0)


def test_prt_as_somas_dos_dez_dias_fecham(prt_dez_dias):
    """Impresso: 6.732 L captados, 4.324 L extravasados, 488 L consumidos, 1.920 L ao fim; resíduo zero."""
    d = prt_dez_dias.daily_results
    captado = sum(x.harvested_liters for x in d)
    extravasado = sum(x.spilled_liters for x in d)
    consumido = sum(x.pluvial_consumed_liters for x in d)
    final = d[-1].lower_tank_end_liters
    assert captado == pytest.approx(6732.0, abs=1.0)
    assert extravasado == pytest.approx(4324.0, abs=1.0)
    assert consumido == pytest.approx(488.0, abs=1.0)
    assert final == pytest.approx(1920.0, abs=1.0)
    assert captado - extravasado - consumido - final == pytest.approx(0.0, abs=0.5)


def test_prt_a_tabela_publicada_dos_dez_dias_bate_com_a_simulacao(prt_dez_dias):
    """Se alguém editar a tabela à mão, este teste apanha-o."""
    texto = _prt_lido(os.path.join(PRT_TABELAS, "cap23_dez_dias.md"))
    dias = []
    for linha in texto.split(chr(10)):
        celulas = [c.strip() for c in linha.strip("|").split("|")] if linha.startswith("| ") else []
        if celulas and celulas[0].isdigit():
            dias.append([c.replace(" ", "").replace(",", ".") for c in celulas])
    assert len(dias) == 10
    for i, c in enumerate(dias):
        d = prt_dez_dias.daily_results[i]
        assert float(c[1]) == pytest.approx(d.precip_mm, abs=0.05), f"dia {i+1} chuva"
        assert float(c[3]) == pytest.approx(d.eff_precip_mm, abs=0.05), f"dia {i+1} efetiva"
        assert float(c[4]) == pytest.approx(d.harvested_liters, abs=1.0), f"dia {i+1} captado"
        assert float(c[6]) == pytest.approx(d.pluvial_consumed_liters, abs=1.0), f"dia {i+1} consumido"
        assert float(c[7]) == pytest.approx(d.spilled_liters, abs=1.0), f"dia {i+1} extravasado"


# ── o tutorial de Lisboa: capítulos 4 a 7 ───────────────────────────────────────────────────────

def test_prt_a_serie_do_tutorial_e_a_que_o_capitulo_4_descreve(prt_serie):
    """Impresso: 30 anos, 719 mm/ano, chuva em 22% dos dias, 9,0 mm nos dias chuvosos, máximo 91,2 mm."""
    anos = len(prt_serie) / 365.25
    assert len(prt_serie) == 10958
    assert anos == pytest.approx(30.0, abs=0.1)
    assert prt_serie.sum() / anos == pytest.approx(719.0, abs=3.0)
    assert (prt_serie > 0.1).mean() * 100 == pytest.approx(22.0, abs=1.0)
    assert prt_serie[prt_serie > 0.1].mean() == pytest.approx(9.0, abs=0.1)
    assert prt_serie.max() == pytest.approx(91.2, abs=0.05)


def test_prt_o_descarte_atinge_quatro_por_cento_dos_dias(prt_serie):
    """Impresso: 4% dos dias têm chuva (acima de 0,1 mm) mas abaixo da lâmina de descarte de 2 mm."""
    abaixo = ((prt_serie > 0.1) & (prt_serie <= 2.0)).mean() * 100
    assert abaixo == pytest.approx(4.0, abs=1.0)


def test_prt_a_oferta_bruta_e_uma_vez_e_meia_a_procura(prt_serie):
    """Impresso no capítulo 5: 92 m³/ano de oferta bruta contra 61 m³/ano de procura pluvial (1,5×)."""
    anos = len(prt_serie) / 365.25
    bruta = prt_serie.sum() / anos * PRT_TUTORIAL["area"] * PRT_TUTORIAL["runoff_coeff"] / 1000.0
    procura = PRT_TUTORIAL["total_demand_per_day"] * PRT_TUTORIAL["rainwater_share"] * 365.25 / 1000.0
    assert bruta == pytest.approx(92.0, abs=1.0)
    assert procura == pytest.approx(61.0, abs=1.0)
    assert bruta / procura == pytest.approx(1.5, abs=0.05)


def test_prt_a_primeira_simulacao_do_capitulo_6(prt_serie):
    """Impresso: 15,39% com 3.000 L, 106,4 L/dia extravasados, 53,3% de dias plenos, 33,7 m³/ano."""
    r = _prt_sim(prt_serie, 3000)
    assert r.potential_potable_savings_pct == pytest.approx(15.39, abs=0.05)
    assert r.avg_spilled_l_day == pytest.approx(106.4, abs=0.1)
    assert r.pct_days_full_satisfaction == pytest.approx(53.3, abs=0.1)
    assert r.pct_days_partial_satisfaction == pytest.approx(2.9, abs=0.1)
    assert r.pct_days_null_satisfaction == pytest.approx(43.8, abs=0.1)
    assert r.annual_pluvial_consumed_m3 == pytest.approx(33.7, abs=0.1)
    assert r.avg_pluvial_consumed_l_day == pytest.approx(92.3, abs=0.1)


@pytest.mark.parametrize(("volume", "potencial"), [
    (1000, 10.39), (2000, 13.55), (3000, 15.39), (4000, 16.60), (5000, 17.49),
    (8000, 19.39), (12000, 21.23), (20000, 24.01),
])
def test_prt_a_curva_de_varredura_do_capitulo_7(prt_serie, volume, potencial):
    """Cada linha da tabela impressa no capítulo 7."""
    assert _prt_sim(prt_serie, volume).potential_potable_savings_pct == pytest.approx(potencial, abs=0.05)


def test_prt_o_potencial_nunca_passa_da_fracao_suprivel(prt_serie):
    teto = PRT_TUTORIAL["rainwater_share"] * 100.0
    for v in (1000, 5000, 20000, 100000):
        assert _prt_sim(prt_serie, v).potential_potable_savings_pct <= teto + 1e-9


@pytest.mark.parametrize(("limiar", "ideal"), [(3.0, 3000), (1.0, 5000), (0.5, 10000)])
def test_prt_o_limiar_decide_o_volume_ideal(prt_serie, limiar, ideal):
    from triton.core.simulation import run_sweep_simulation
    r = run_sweep_simulation(precip_data=prt_serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
                             delta_ideal_threshold=limiar, **PRT_TUTORIAL)
    assert r.optimal_lower_tank_vol == pytest.approx(ideal)


def test_prt_o_volume_maior_custa_muito_mais_por_pouco_ganho(prt_serie):
    """Impresso: 3,3× o preço (ilustrativo) e 3,5× o carbono por 6,52 pontos (de 5.000 a 20.000 L)."""
    from triton.core.environmental import calculate_lca
    r5, r20 = _prt_sim(prt_serie, PRT_VOLUME), _prt_sim(prt_serie, 20000)
    assert r20.potential_potable_savings_pct - r5.potential_potable_savings_pct == pytest.approx(6.52, abs=0.05)
    assert _prt_preco(20000, "CONCRETO") / _prt_preco(PRT_VOLUME, "CONCRETO") == pytest.approx(3.3, abs=0.1)
    cfg = _prt_ambiental("CONCRETO")
    c5 = calculate_lca(PRT_VOLUME, r5.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    c20 = calculate_lca(20000.0, r20.annual_pluvial_consumed_m3, cfg).total_embodied_co2_kg
    assert c5 == pytest.approx(1026.0, abs=2.0)
    assert c20 / c5 == pytest.approx(3.5, abs=0.1)


# ── capítulos 8 a 12: o reservatório superior, o custo (ilustrativo), o carbono, a decisão ───────

def test_prt_o_reservatorio_superior_nao_aumenta_a_poupanca(prt_serie):
    """Impresso no capítulo 8: com o mesmo armazenamento (6.000 L), o arranjo duplo perde 0,31 ponto."""
    unico = _prt_sim(prt_serie, PRT_VOLUME + 1000.0)
    duplo = _prt_sim(prt_serie, PRT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0)
    assert unico.potential_potable_savings_pct == pytest.approx(18.19, abs=0.05)
    assert duplo.potential_potable_savings_pct == pytest.approx(17.88, abs=0.05)
    assert unico.potential_potable_savings_pct - duplo.potential_potable_savings_pct == pytest.approx(0.31, abs=0.03)
    assert unico.pct_days_full_satisfaction == pytest.approx(64.0, abs=0.1)
    assert duplo.pct_days_full_satisfaction == pytest.approx(62.8, abs=0.1)


def test_prt_a_energia_da_elevacao_do_capitulo_8(prt_serie):
    """Impresso: 5,1 kWh/ano e 49 arranques por ano."""
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    duplo = _prt_sim(prt_serie, PRT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0)
    cfg = TritonConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw, cfg.pump_efficiency, cfg.pump_flow_rate = 0.37, 0.0, 0.0
    cfg.pump_manometric_head_m, cfg.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(cfg, duplo)
    assert e.annual_kwh == pytest.approx(5.1, abs=0.3)
    assert e.annual_cycles == pytest.approx(49, abs=3)


@pytest.mark.parametrize(("limiar", "potencial", "arranques"), [
    (0, 17.78, 45), (100, 17.88, 49), (300, 17.95, 61), (500, 18.01, 80),
])
def test_prt_o_limiar_de_arranque_troca_potencial_por_desgaste(prt_serie, limiar, potencial, arranques):
    r = _prt_sim(prt_serie, PRT_VOLUME, upper_tank_vol=1000.0, upper_tank_used=True,
                 pumping_threshold=float(limiar))
    assert r.potential_potable_savings_pct == pytest.approx(potencial, abs=0.05)
    assert r.total_pump_cycles / (r.total_days / 365.25) == pytest.approx(arranques, abs=1.5)


def test_prt_o_resultado_economico_do_capitulo_10(prt_serie):
    """Impresso (custos ILUSTRATIVOS, euros): investimento 6.650; poupança anual 134,28; VAL -5.828,77; sem recuperação.

    O tarifário de Lisboa é o transcrito (EPAL e Câmara); o sistema não se paga com estes custos, e o
    capítulo diz isso em vez de ajustar os custos até a recuperação aparecer.
    """
    _, e = _prt_economico(prt_serie, PRT_VOLUME, "CONCRETO")
    assert e.capex_total == pytest.approx(6650.0, abs=1.0)
    assert e.annual_water_savings_brl == pytest.approx(134.28, abs=3.0)
    assert e.vpl == pytest.approx(-5828.8, abs=60.0)
    assert not e.payback_years


def test_prt_a_fatura_de_lisboa_com_e_sem_o_sistema(prt_serie):
    """Impresso: 46,25 € sem o sistema, 35,06 € com ele, poupança de 11,19 € por mês."""
    from triton.core.economic import calculate_water_bill, esgoto_do_projeto
    cfg = _prt_config_de_lisboa()
    r = run_single_simulation(precip_data=prt_serie, lower_tank_vol=PRT_VOLUME, upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **PRT_TUTORIAL)
    dias = 30.4375

    def conta(l_dia):
        return calculate_water_bill(l_dia * dias, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
                                    cfg.water_tax_fixed, cfg.water_tax_var, **esgoto_do_projeto(cfg))
    sem = conta(r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day)
    com = conta(r.avg_potable_consumed_l_day)
    assert sem == pytest.approx(46.25, abs=0.05)
    assert com == pytest.approx(35.06, abs=0.05)
    assert sem - com == pytest.approx(11.19, abs=0.05)


def test_prt_o_tarifario_de_lisboa_e_o_impresso_na_base():
    """A conta de 10 m³ por mês (25,8683 €) é a do exemplo conferido à mão em `examples/LEIA.md`."""
    from triton.core.economic import calculate_water_bill, esgoto_do_projeto
    cfg = _prt_config_de_lisboa()
    conta = calculate_water_bill(10000.0, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
                                 cfg.water_tax_fixed, cfg.water_tax_var, **esgoto_do_projeto(cfg))
    assert conta == pytest.approx(25.8683, abs=0.0005)


def test_prt_a_troca_para_polietileno_muda_o_retorno_do_carbono(prt_serie):
    """Impresso no capítulo 11: o carbono retorna em 20,9 anos em polietileno e em 59,0 em betão.

    Com a chuva de Lisboa e os fatores ilustrativos, nenhum dos dois cumpre 20 anos com folga: o polietileno
    fica na fronteira (emite 15 kg em 20 anos), o betão emite 678 kg.
    """
    from triton.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=prt_serie, lower_tank_vol=PRT_VOLUME, upper_tank_vol=1000.0,
                              upper_tank_used=True, pumping_threshold=100.0, **PRT_TUTORIAL)
    lca = {k: calculate_lca(PRT_VOLUME, r.annual_pluvial_consumed_m3, _prt_ambiental(k, r))
           for k in ("PEAD", "CONCRETO")}
    assert lca["PEAD"].environmental_payback_years == pytest.approx(20.9, abs=0.3)
    assert lca["CONCRETO"].environmental_payback_years == pytest.approx(59.0, abs=0.5)
    assert lca["PEAD"].total_embodied_co2_kg == pytest.approx(363.0, abs=2.0)
    assert lca["CONCRETO"].total_embodied_co2_kg == pytest.approx(1026.0, abs=2.0)
    assert -lca["PEAD"].lifetime_net_co2_saved_kg == pytest.approx(15.0, abs=3.0)
    assert -lca["CONCRETO"].lifetime_net_co2_saved_kg == pytest.approx(678.0, abs=5.0)


def test_prt_os_tres_criterios_do_capitulo_12_discordam(prt_serie):
    """Impresso: técnico 12.000 L, financeiro 1.000 L, ambiental 2.000 L, compromisso 5.000 L."""
    from triton.core.environmental import calculate_lca
    from triton.core.topsis import TopsisCandidate, calculate_topsis_scores
    cands = []
    for v in (1000, 2000, 3000, 4000, 5000, 8000, 12000):
        r, e = _prt_economico(prt_serie, v, "PEAD")
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, _prt_ambiental("PEAD", r))
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v), water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg, capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct, overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years, irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))
    res = calculate_topsis_scores(cands)
    assert cands[res.technical_best_index].lower_tank_vol == 12000.0
    assert cands[res.financial_best_index].lower_tank_vol == 1000.0
    assert cands[res.environmental_best_index].lower_tank_vol == 2000.0
    assert cands[res.best_index].lower_tank_vol == PRT_VOLUME


# ── secção 3.1: as cidades de comparação ────────────────────────────────────────────────────────

def test_prt_as_cidades_da_secao_3_1():
    """Impresso: o mesmo projeto rende 17,49% em Lisboa, 22,04% no Porto e 12,98% no Funchal (com 5.000 L).

    O Porto chove 1,7 vez o que chove Lisboa e rende 4,6 pontos mais; o Funchal, com menos chuva, rende menos.
    O volume ideal é 5.000 L em Lisboa e no Porto e 4.000 L no Funchal. A razão entre o mês mais e o menos
    chuvoso é 47,3× em Lisboa (verão seco), 9,8× no Porto e 14,8× no Funchal.
    """
    from datetime import datetime, timedelta

    from triton.core.simulation import run_sweep_simulation
    res = {}
    for chave in ("Lisboa", "Porto", "Funchal"):
        serie = _prt_serie(chave)
        anos = len(serie) / 365.25
        r = _prt_sim(serie, PRT_VOLUME)
        sw = run_sweep_simulation(precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
                                  delta_ideal_threshold=1.0, **PRT_TUTORIAL)
        d0, meses = datetime(1991, 1, 1), np.zeros(12)
        for i, v in enumerate(serie):
            meses[(d0 + timedelta(days=i)).month - 1] += float(v)
        meses /= anos
        res[chave] = (serie.sum() / anos, r.potential_potable_savings_pct, meses.max() / max(meses.min(), 0.1),
                      sw.optimal_lower_tank_vol, (serie > 0.1).mean() * 100)
    li, po, fu = res["Lisboa"], res["Porto"], res["Funchal"]
    assert po[0] > li[0] > fu[0]
    assert li[1] == pytest.approx(17.49, abs=0.05)
    assert po[1] == pytest.approx(22.04, abs=0.05)
    assert fu[1] == pytest.approx(12.98, abs=0.05)
    assert li[0] == pytest.approx(719.0, abs=3.0) and po[0] == pytest.approx(1199.0, abs=3.0) \
        and fu[0] == pytest.approx(538.0, abs=3.0)
    assert li[2] == pytest.approx(47.3, abs=0.5) and po[2] == pytest.approx(9.8, abs=0.2) \
        and fu[2] == pytest.approx(14.8, abs=0.3)
    assert (li[4], po[4], fu[4]) == pytest.approx((22.0, 31.0, 42.0), abs=1.0)
    assert (li[3], po[3], fu[3]) == (5000.0, 5000.0, 4000.0)


# ── os ficheiros de caso e as tabelas ───────────────────────────────────────────────────────────

PRT_CASOS_ESPERADOS = {
    "01_tutorial_lisboa.triton": ("volume fixo", 17.88),
    "02_porto.triton": ("volume fixo", 22.04),
    "03_funchal.triton": ("volume fixo", 12.98),
    "04_tutorial_varredura.triton": ("varredura", 17.49),
    "05_dez_dias.triton": ("volume fixo", 24.43),
    "06_reservatorio_superior.triton": ("volume fixo", 17.88),
    "07_escola_semanal.triton": ("volume fixo", 23.03),
    "08_hotel_mensal.triton": ("volume fixo", 10.36),
    "09_modulacao_tutorial.triton": ("varredura", 17.49),
    "10_modulacao_captacao.triton": ("varredura", 17.49),
}


def _prt_resultados():
    import json
    return json.loads(_prt_lido(os.path.join(PRT_CASOS, "resultados.json")))


def test_prt_os_casos_publicados_sao_os_da_edicao():
    pub = _prt_resultados()
    assert sorted(pub) == sorted(PRT_CASOS_ESPERADOS)
    for arquivo, (modo, potencial) in PRT_CASOS_ESPERADOS.items():
        assert pub[arquivo]["modo"] == modo, arquivo
        assert pub[arquivo]["potencial_pct"] == pytest.approx(potencial, abs=0.01), arquivo
        assert os.path.exists(os.path.join(PRT_CASOS, arquivo)), arquivo


def test_prt_os_casos_batem_com_as_tabelas_e_os_capitulos():
    """O caso de Lisboa com volume fixo é o da tabela de varredura; o de dez dias, o da tabela dos dez dias."""
    pub = _prt_resultados()
    assert pub["04_tutorial_varredura.triton"]["volume_ideal_l"] == 5000.0
    assert pub["04_tutorial_varredura.triton"]["volumes_simulados"] == 21
    d = pub["05_dez_dias.triton"]
    assert (d["volume_l"], d["dias_de_chuva"]) == (2000.0, 10)
    assert d["pluvial_l_dia"] == pytest.approx(48.9) and d["extravasado_l_dia"] == pytest.approx(432.4)
    assert d["atendimento_pleno_pct"] == pytest.approx(60.0)
    # O reservatório superior de 1.000 L perde 0,31 ponto contra um reservatório só de 6.000 L.
    u = pub["06_reservatorio_superior.triton"]
    assert u["volume_tanque_unico_l"] == 6000.0
    assert u["potencial_tanque_unico_pct"] - u["potencial_pct"] == pytest.approx(0.31, abs=0.01)
    # O mesmo projeto em três chuvas.
    assert pub["01_tutorial_lisboa.triton"]["atendimento_pleno_pct"] == pytest.approx(62.8)
    assert pub["02_porto.triton"]["atendimento_pleno_pct"] == pytest.approx(77.9)
    assert pub["03_funchal.triton"]["atendimento_pleno_pct"] == pytest.approx(44.5)


def test_prt_o_calendario_concentrado_rende_menos_que_a_procura_constante():
    """Secção 3.4: o hotel de Lisboa (cheio de junho a setembro, o verão seco) perde 0,71 ponto contra a mesma
    procura anual espalhada; a escola semanal do Porto, que só fecha ao fim de semana, quase não muda."""
    pub = _prt_resultados()
    hotel, escola = pub["08_hotel_mensal.triton"], pub["07_escola_semanal.triton"]
    assert hotel["potencial_demanda_constante_pct"] - hotel["potencial_pct"] == pytest.approx(0.71, abs=0.02)
    assert hotel["demanda_media_l_dia"] == pytest.approx(8365.1, abs=0.1)
    assert abs(escola["potencial_demanda_constante_pct"] - escola["potencial_pct"]) < 0.2
    assert escola["demanda_media_l_dia"] == pytest.approx(9014.3, abs=0.1)


def test_prt_todo_o_caso_do_manual_reproduz_o_numero_publicado():
    """O ficheiro gravado, relido e simulado dá o número publicado (o campo que se perca aparece aqui)."""
    import sys
    sys.path.insert(0, MANUAL)
    try:
        from gerar_casos import simular_do_arquivo
    except ImportError:
        pytest.skip("gerador de casos ausente")
    for arquivo, publicado in sorted(_prt_resultados().items()):
        obtido = simular_do_arquivo(os.path.join(PRT_CASOS, arquivo))
        assert obtido["potencial_pct"] == pytest.approx(publicado["potencial_pct"], abs=0.05), arquivo
        assert obtido["modo"] == publicado["modo"], arquivo


def test_prt_os_casos_de_modulacao_abrem_com_a_modulacao_montada():
    import json
    for arquivo, chaves in (("09_modulacao_tutorial.triton", {"per_capita_l_dia", "pessoas", "fator_chuva"}),
                            ("10_modulacao_captacao.triton", {"area_m2", "coef_escoamento", "fator_chuva"})):
        d = json.loads(_prt_lido(os.path.join(PRT_CASOS, arquivo)))
        mod = d["ui_state"]["modulacao_estocastica"]
        marcadas = {k for k, v in mod["parametros"]["variaveis"].items() if v.get("variar")}
        assert chaves <= marcadas, arquivo
        assert (mod["amostras"], mod["semente"]) == (1000, 42), arquivo
        assert not mod["parametros"].get("modelos_climaticos"), arquivo


def test_prt_os_casos_e_as_tabelas_nao_trazem_nada_do_brasil():
    """Nenhum ficheiro de caso, README, resultado ou tabela da PRT cita cidade, norma ou moeda da BRL."""
    achados = []
    arquivos = [os.path.join(PRT_CASOS, f) for f in sorted(os.listdir(PRT_CASOS))
                if f.endswith((".triton", ".json", ".md", ".csv"))]
    if os.path.isdir(PRT_TABELAS):
        arquivos += [os.path.join(PRT_TABELAS, f) for f in sorted(os.listdir(PRT_TABELAS))
                     if f.endswith(".md")]
    if not arquivos:
        pytest.skip("casos ainda não gerados")
    for caminho in arquivos:
        texto = open(caminho, encoding="utf-8").read()
        for termo in PRT_TERMOS_PROIBIDOS:
            if termo in texto:
                achados.append(f"{os.path.relpath(caminho, MANUAL)}: {termo}")
    assert not achados, achados


def test_prt_todo_o_valor_em_dinheiro_das_tabelas_e_ilustrativo_e_rotulado():
    """Regra 6: custo de obra, energia e preço de reservatório levam «ilustrativo, não é preço de mercado» na
    legenda ou no cabeçalho (a fatura de Lisboa é o tarifário transcrito, e não um custo)."""
    if not os.path.isdir(PRT_TABELAS):
        pytest.skip("tabelas ainda não geradas")
    faltando = []
    for nome in ("cap07_limiar_e_custo.md", "cap08_reservatorio_superior.md", "cap10_economico.md",
                 "cap11_materiais.md", "cap12_multicriterio.md", "cap20_sensibilidade.md"):
        texto = _prt_lido(os.path.join(PRT_TABELAS, nome))
        for bloco in texto.split("<!-- tabela: ")[1:]:
            legenda, _, corpo = bloco.partition(" -->")
            cabeca = corpo.split(chr(10))[1]
            if "fatura de água, saneamento e resíduos de Lisboa" in legenda:
                continue          # o tarifário publicado, e não um custo
            if "€" in corpo and "ilustrativ" not in (legenda + cabeca):
                faltando.append(f"{nome}: {legenda[:50]}")
    assert not faltando, faltando


def test_prt_as_tabelas_estao_em_portugues_de_portugal():
    """O glossário da edição não troca nada nas tabelas geradas (já saem em português de Portugal)."""
    from triton.ui.portugues_de_portugal import para_portugal
    if not os.path.isdir(PRT_TABELAS):
        pytest.skip("tabelas ainda não geradas")
    trocadas = []
    for f in sorted(os.listdir(PRT_TABELAS)):
        if not f.endswith(".md"):
            continue
        texto = open(os.path.join(PRT_TABELAS, f), encoding="utf-8").read()
        if para_portugal(texto) != texto:
            trocadas.append(f)
    assert not trocadas, trocadas


# ── o que o texto em português de Portugal cita ─────────────────────────────────────────────────

#: Para cada capítulo, o que ele tem de citar do programa. Cada capítulo vale a partir do momento em que
#: deixa de citar o Brasil (`_prt_capitulo`); antes disso, é saltado, sem esconder os demais.
PRT_CITACOES = {
    "23_balanco_diario.md": ("24,4%", "6 732 L", "4 324 L", "488 L", "2 865 L", "2 380 L", "1 943 L",
                             "9 L", "1 920 L"),
    "04_o_projeto_e_a_chuva.md": ("150 m²", "0,85", "2,0 mm", "719 mm", "Lisboa"),
    "05_a_edificacao_e_a_demanda.md": ("600 L/dia", "168 L/dia", "28%", "61"),
    "06_a_primeira_simulacao.md": ("15,39%", "106,4 L/dia", "53,3%", "3 000"),
    "07_escolher_o_volume.md": ("5 000 L", "17,49%", "61,3%", "24,01%"),
    "08_reservatorio_superior.md": ("5,1 kWh", "6 000 L"),
    "10_quanto_custa.md": ("11,19 €", "ilustrativo"),
    "11_quanto_carbono_evita.md": ("1 026 kg", "59,0 anos", "20,9 anos"),
    "12_qual_volume_escolher.md": ("5 000 L", "12 000 L", "1 000 L", "2 000 L", "17,88%"),
    "14_comparar_cidades.md": ("Porto", "Funchal", "17,49%", "22,04%", "12,98%", "47,3"),
}


@pytest.mark.parametrize("arquivo", sorted(PRT_CITACOES))
def test_prt_o_capitulo_cita_os_numeros_do_programa(arquivo):
    texto = _prt_capitulo(arquivo)
    for termo in PRT_CITACOES[arquivo]:
        assert termo in texto, f"{arquivo} não cita {termo}"
