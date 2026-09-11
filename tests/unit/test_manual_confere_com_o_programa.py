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
        texto = _capitulo(arquivo)
        for termo in termos:
            assert termo in texto, f"{arquivo} não cita {termo}"

# ── tutorial, capítulos 8 a 13 ────────────────────────────────────────────────

def _economico(serie, volume, material):
    """Monta a análise econômica do tutorial, como os capítulos 10 e 12 fazem."""
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.economic import run_economic_analysis
    from netuno.core.parser import NetunoConfig

    r = run_single_simulation(precip_data=serie, lower_tank_vol=float(volume), **TUTORIAL)
    cfg = NetunoConfig()
    cfg.water_tariffs = [(0.0, 0.0, 46.34, -1), (0.0, 10.0, 3.08, 1),
                         (10.0, 25.0, 14.31, 1), (25.0, 50.0, 19.14, 1),
                         (50.0, 999999.0, 24.08, 1)]
    cfg.sewage_mode, cfg.sewage_rate = 1, 100.0
    cfg.cost_lower_tank = estimate_tank_price(float(volume), material)
    cfg.cost_upper_tank, cfg.pump_unit_cost, cfg.pump_count = 0.0, 0.0, 0
    cfg.cost_labor, cfg.cost_piping, cfg.cost_accessories = 3500.0, 1200.0, 1800.0
    cfg.upper_tank_used = False
    cfg.elec_tariff, cfg.tma, cfg.inflation = 0.69568, 0.5, 0.35
    cfg.analysis_period_years, cfg.tariff_escalation = 20, 12
    return r, run_economic_analysis(cfg, r)


def test_a_caixa_superior_nao_aumenta_a_economia(serie_tutorial):
    """Impresso no capítulo 8: com o mesmo armazenamento, o arranjo duplo perde."""
    unico = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=6000.0, **TUTORIAL)
    duplo = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=5000.0, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **TUTORIAL)
    assert duplo.potential_potable_savings_pct < unico.potential_potable_savings_pct
    assert unico.potential_potable_savings_pct - duplo.potential_potable_savings_pct \
        == pytest.approx(0.33, abs=0.05)


def test_a_energia_do_recalque_do_capitulo_8(serie_tutorial):
    """Impresso: 10,7 kWh/ano e 96 acionamentos."""
    from netuno.core.parser import NetunoConfig
    from netuno.core.pump_energy import compute_annual_pump_energy

    duplo = run_single_simulation(
        precip_data=serie_tutorial, lower_tank_vol=5000.0, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **TUTORIAL)
    cfg = NetunoConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw, cfg.pump_efficiency, cfg.pump_flow_rate = 0.37, 0.0, 0.0
    cfg.pump_manometric_head_m, cfg.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(cfg, duplo)
    assert e.annual_kwh == pytest.approx(10.7, abs=0.3)
    assert e.annual_cycles == pytest.approx(96, abs=3)


def test_o_limiar_de_acionamento_troca_potencial_por_desgaste(serie_tutorial):
    """Impresso no capítulo 8: limiar maior, mais potencial e mais acionamentos."""
    anterior = None
    for limiar in (0, 100, 300, 500):
        r = run_single_simulation(
            precip_data=serie_tutorial, lower_tank_vol=5000.0, upper_tank_vol=1000.0,
            upper_tank_used=True, pumping_threshold=float(limiar), **TUTORIAL)
        ciclos = r.total_pump_cycles / (r.total_days / 365.25)
        if anterior is not None:
            assert ciclos >= anterior
        anterior = ciclos


def test_a_classe_alvo_sozinha_nao_muda_o_custo_da_etap():
    """Impresso no capítulo 9: sem polimento, as quatro classes custam o mesmo."""
    from netuno.core.water_quality import WATER_QUALITY_CLASSES, size_etap
    custos = {
        cid: size_etap(target_class_id=cid, annual_pluvial_consumed_m3=82.1,
                       roof_area_m2=150.0, include_polishing_filter=False
                       ).total_etap_capex
        for cid in WATER_QUALITY_CLASSES
    }
    assert len(set(round(c, 2) for c in custos.values())) == 1


def test_a_recusa_do_polimento_fica_registrada():
    """Impresso: quem recusa o que a classe recomenda tem a recusa documentada."""
    from netuno.core.water_quality import size_etap
    r2 = size_etap(target_class_id="classe_2", annual_pluvial_consumed_m3=82.1,
                   roof_area_m2=150.0, include_polishing_filter=False)
    r1 = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=82.1,
                   roof_area_m2=150.0, include_polishing_filter=False)
    assert r2.polishing_recommended_but_declined is True
    assert r1.polishing_recommended_but_declined is False


def test_uv_e_ozonio_somam_a_cloracao_em_vez_de_substitui_la():
    """Impresso no capítulo 9: são barreiras adicionais, sem residual próprio."""
    from netuno.core.water_quality import size_etap
    cloro = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=82.1,
                      roof_area_m2=150.0, disinfection_choice="cloro")
    uv = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=82.1,
                   roof_area_m2=150.0, disinfection_choice="uv")
    assert uv.total_etap_capex > cloro.total_etap_capex
    assert len(uv.disinfection_stages) == 2


def test_o_resultado_economico_do_capitulo_10(serie_tutorial):
    """Impresso: R$ 2.349/ano, VPL R$ 15.295, payback 8,7 anos, em concreto."""
    _, e = _economico(serie_tutorial, 5000, "CONCRETO")
    assert e.capex_total == pytest.approx(13379.79, abs=1.0)
    assert e.annual_water_savings_brl == pytest.approx(2349.21, abs=5.0)
    assert e.vpl == pytest.approx(15295.0, abs=50.0)
    assert e.payback_years == pytest.approx(8.7, abs=0.2)


def test_a_troca_para_polietileno_melhora_as_tres_dimensoes(serie_tutorial):
    """Impresso no capítulo 11: mais barato, melhor VPL e carbono positivo."""
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca

    r_c, e_c = _economico(serie_tutorial, 5000, "CONCRETO")
    r_p, e_p = _economico(serie_tutorial, 5000, "PEAD")
    assert e_p.capex_total < e_c.capex_total
    assert e_p.vpl > e_c.vpl
    assert e_p.payback_years < e_c.payback_years

    saldos = {}
    for k, r in (("CONCRETO", r_c), ("PEAD", r_p)):
        cfg = EnvironmentalConfig()
        cfg.lower_material_key = k
        saldos[k] = calculate_lca(5000.0, r.annual_pluvial_consumed_m3, cfg)
    assert saldos["PEAD"].lifetime_net_co2_saved_kg > 0
    assert saldos["CONCRETO"].lifetime_net_co2_saved_kg < 0
    assert saldos["CONCRETO"].environmental_payback_years > 20.0
    assert saldos["PEAD"].environmental_payback_years == pytest.approx(10.9, abs=0.3)


def test_em_concreto_o_carbono_piora_com_o_volume(serie_tutorial):
    """Impresso: cada metro cúbico de concreto acrescenta mais dívida que crédito."""
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    anterior = None
    for v in (2000, 3000, 5000, 8000):
        r = run_single_simulation(
            precip_data=serie_tutorial, lower_tank_vol=float(v), **TUTORIAL)
        cfg = EnvironmentalConfig()
        cfg.lower_material_key = "CONCRETO"
        saldo = calculate_lca(float(v), r.annual_pluvial_consumed_m3,
                              cfg).lifetime_net_co2_saved_kg
        if anterior is not None:
            assert saldo < anterior, f"{v} L não piorou"
        anterior = saldo


def test_os_tres_criterios_do_capitulo_12_discordam(serie_tutorial):
    """Impresso: técnico diz 12.000, financeiro 5.000, ambiental 3.000."""
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.topsis import TopsisCandidate, calculate_topsis_scores

    cands = []
    for v in (1000, 2000, 3000, 5000, 8000, 12000):
        r, e = _economico(serie_tutorial, v, "PEAD")
        amb = EnvironmentalConfig()
        amb.lower_material_key = "PEAD"
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
    assert cands[res.financial_best_index].lower_tank_vol == 5000.0
    assert cands[res.environmental_best_index].lower_tank_vol == 3000.0
    assert cands[res.best_index].lower_tank_vol == 5000.0


def test_os_capitulos_8_a_13_citam_os_numeros_do_programa():
    esperados = {
        "08_reservatorio_superior.md": ("10,7 kWh", "0,33 ponto", "6.000 L"),
        "09_qualidade_que_o_uso_exige.md": ("R$ 930", "R$ 2.130", "R$ 4.430", "R$ 580"),
        "10_quanto_custa.md": ("R$ 195,77", "R$ 15.295", "8,7 anos", "R$ 28,62"),
        "11_quanto_carbono_evita.md": ("962 kg", "35,1 anos", "10,9 anos", "248 kg"),
        "12_qual_volume_escolher.md": ("5.000 L", "12.000 L", "3.000 L", "37,46%"),
        "13_o_relatorio_e_o_artigo.md": ("5.0.0", "2,3 a 2,7", "1 %/m"),
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
    for exigido in ("Versão do Netuno", "fronteira", "regime", "pesos",
                    "limiar", "rótulo de triagem"):
        assert exigido in texto, f"a lista de declaração não cobre {exigido}"

# ══════════════════════════════════════════════════════════════════════════════
# Integridade do manual montado
# ══════════════════════════════════════════════════════════════════════════════

#: A estrutura da ABNT: sete capítulos, e as seções de cada um. A contagem sai
#: da própria declaração do montador, para que reordenar o manual não exija
#: reescrever este teste — foi assim que a numeração parou de divergir.
SECOES_EM_PARTES = 39
APENDICES = 10


def _manual_montado():
    caminho = os.path.join(MANUAL, "Manual-Netuno-5.md")
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
    from gerar import ESTRUTURA, TITULOS

    texto = _manual_montado()
    cabeca = texto.split("# 1. ")[0]
    for i, (titulo_cap, _, secoes) in enumerate(ESTRUTURA, start=1):
        assert f"{i} {titulo_cap}" in cabeca, f"falta o capítulo {i}"
        for j, chave in enumerate(secoes, start=1):
            linha = f"{i}.{j} {TITULOS[chave]}"
            assert linha in cabeca, f"o sumário não lista «{linha}»"


def test_a_numeracao_das_secoes_segue_a_ordem_da_estrutura():
    """Cada título numerado do corpo confere com a posição declarada."""
    import sys
    sys.path.insert(0, MANUAL)
    from gerar import ESTRUTURA, TITULOS

    texto = _manual_montado()
    for i, (_, _, secoes) in enumerate(ESTRUTURA, start=1):
        for j, chave in enumerate(secoes, start=1):
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
    """Impresso: 329 de franquia, 165 sem mínimo, 156 de disponibilidade."""
    import json
    from collections import Counter

    caminho = os.path.join(RAIZ, "netuno", "data", "brazil_cities_tariffs.json")
    base = json.load(open(caminho, encoding="utf-8"))
    regimes = Counter(c.get("regime_tarifario") for c in base["cities"].values())
    assert len(base["cities"]) == 652
    assert regimes["franquia_no_minimo"] == 329
    assert regimes["sem_minimo"] == 165
    assert regimes["disponibilidade"] == 156


def test_a_franquia_para_de_descontar_como_o_guia_16_mostra():
    """Impresso: em Floriano, poupar 4 ou poupar 7 economiza o mesmo."""
    from netuno.core.economic import calculate_water_bill

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
    from netuno.core.parser import load_precipitation

    resultados = {}
    for chave in ("Florianopolis1", "Manaus1", "Brasilia1"):
        caminho = os.path.join(RAIZ, "data", "rainfall", f"{chave}.csv")
        if not os.path.exists(caminho):
            pytest.skip(f"série {chave} não instalada")
        serie = load_precipitation(caminho)[: 30 * 365]
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0, **TUTORIAL)
        resultados[chave] = (serie.sum() / anos, r.potential_potable_savings_pct)

    chuva_flo, pot_flo = resultados["Florianopolis1"]
    chuva_man, pot_man = resultados["Manaus1"]
    chuva_bsb, pot_bsb = resultados["Brasilia1"]

    assert chuva_man > chuva_flo and pot_man < pot_flo
    assert chuva_bsb < chuva_flo and pot_bsb < pot_flo / 1.5
    assert pot_man == pytest.approx(27.92, abs=0.05)
    assert pot_bsb == pytest.approx(20.80, abs=0.05)


def test_o_rendimento_do_motor_do_capitulo_28():
    """Impresso: a Tabela 13 da ABNT NBR 17094-2, dois polos, linha IR1."""
    from netuno.core.pump_hydraulics import rendimento_do_motor
    esperado = {0.18: 0.500, 0.25: 0.555, 0.37: 0.605,
                0.55: 0.640, 0.75: 0.693, 1.10: 0.715, 1.50: 0.724}
    for kw, eta in esperado.items():
        assert rendimento_do_motor(kw) == pytest.approx(eta), f"{kw} kW"


def test_as_densidades_do_apendice_C():
    """Impresso: massa por m³ útil de cada material."""
    from netuno.core.environmental import MATERIAL_PRESETS
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
        "01_o_que_o_netuno_faz.md": ("dimensiona a instalação hidráulica", "triagem", "0,25"),
        "03_por_onde_comecar.md": ("fração atendível", "varredura"),
        "24_volume_ideal.md": ("250", "limitado a 40", "%/m"),
        "25_indicadores.md": ("365,25", "demanda pluvial", "demanda total"),
        "26_indices_pluviometricos.md": ("R10mm", "1961", "Walsh"),
        "27_etap.md": ("incremental", "65%", "substitui"),
        "28_energia_de_bombeamento.md": ("17094", "60,5%", "eixo"),
        "29_analise_economica.md": ("329", "diferença entre duas contas"),
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
    "PySide6", "Numba", "netuno.cli", "argparse",
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

FIGURAS_ESPERADAS = 9


def test_as_figuras_estao_numeradas_na_ordem_da_leitura():
    """A legenda «Figura 1» já apareceu no capítulo 23, depois da «Figura 2».

    A numeração passou a ser feita na montagem, e este teste é o que impede o
    problema de voltar quando alguém inserir uma figura no meio.
    """
    texto = _manual_montado()
    numeros = [int(n) for n in re.findall(r"\*Figura (\d+) —", texto)]
    assert numeros == list(range(1, len(numeros) + 1)), numeros
    assert len(numeros) == FIGURAS_ESPERADAS


def test_os_desenhos_explicativos_existem():
    """Os três desenhos que explicam o sistema a quem chega agora."""
    pasta = os.path.join(MANUAL, "figuras")
    for nome in ("fig00_sistema.png", "fig00b_destino.png", "fig00c_fracao.png"):
        caminho = os.path.join(pasta, nome)
        assert os.path.exists(caminho), nome
        assert os.path.getsize(caminho) > 20_000, nome


def test_o_capitulo_1_apresenta_o_sistema_antes_de_falar_do_programa():
    """Quem abre o manual pode não saber o que é a instalação que vai simular."""
    texto = _capitulo("01_o_que_o_netuno_faz.md")
    assert "O que é um sistema de aproveitamento de água pluvial" in texto
    for termo in ("calhas", "cisterna", "primeira chuva", "projeção horizontal",
                  "fig00_sistema.png", "fig00b_destino.png"):
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
    "1. Projeto e Chuva", "2. Edificação Consumo", "3. Qualidade & ETAP",
    "4. Reservatório & Custos", "5. Resultados Técnicos",
    "6. Resultados Econômicos", "7. Resultados Ambientais & ESG",
    "8. Decisão Multicritério", "9. Relatórios PDF", "10. Exportação",
    "11. Documentação", "12. Gestor de Tarifas",
)


def test_as_etapas_citadas_pelo_manual_sao_as_da_barra_lateral():
    """O nome que o manual manda procurar precisa existir na tela."""
    fonte = os.path.join(RAIZ, "netuno", "ui", "sidebar.py")
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

    from collections import Counter
    contagem = Counter(re.findall(r"\b([A-Z]{2,}(?:-[A-Z0-9]+)?)\b", texto))
    faltando = [
        s for s, n in contagem.items()
        if n >= 3 and s.lower() not in verbetes
        and s not in SIGLAS_DISPENSADAS and not s.startswith("PROC-")
    ]
    assert not faltando, sorted(faltando)
