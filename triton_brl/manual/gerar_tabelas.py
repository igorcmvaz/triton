# -*- coding: utf-8 -*-
"""Gera as tabelas numéricas dos capítulos, rodando o próprio programa.

Nenhum número do manual sai da cabeça de quem escreve. As tabelas deste arquivo
são produzidas executando o Triton com os dados de entrada declarados, de modo que
uma correção no motor apareça no manual na mesma alteração.

Saída: manual/partes/_tabelas/*.md, incluídos pelos capítulos.
"""

from __future__ import annotations

import os

from escrita_segura import gravar  # não desfaz revisão feita à mão
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

from triton.core.simulation import run_single_simulation  # noqa: E402

SAIDA = os.path.join(AQUI, "partes", "_tabelas")
os.makedirs(SAIDA, exist_ok=True)

NL = chr(10)


def br(v, casas=1):
    """Número no padrão brasileiro."""
    return f"{v:,.{casas}f}".replace(",", " ").replace(".", ",")


# ──────────────────────────────────────────────────────────────────────────────
# Capítulo 23 — o balanço diário, dez dias resolvidos
# ──────────────────────────────────────────────────────────────────────────────
#
# O caso didático. Números escolhidos para que o leitor consiga refazer a conta na
# planilha: área redonda, coeficiente usual, demanda redonda, reservatório pequeno
# o bastante para extravasar dentro dos dez dias.

CASO_23 = {
    "area": 100.0,            # m²
    "runoff_coeff": 0.85,     # telha cerâmica
    "discard_mm": 2.0,        # NBR 15527, sem dado local
    "discard_mode": 1,        # todo evento de chuva
    "demanda_total": 200.0,   # L/dia
    "rainwater_share": 0.40,  # 40% da demanda é não potável
    "volume": 2000.0,         # L
}

CHUVA_23 = [0.0, 12.4, 1.6, 0.0, 0.0, 28.0, 5.2, 0.0, 41.0, 0.0]


def tabela_dez_dias():
    r = run_single_simulation(
        precip_data=np.array(CHUVA_23, dtype=float),
        lower_tank_vol=CASO_23["volume"],
        area=CASO_23["area"],
        runoff_coeff=CASO_23["runoff_coeff"],
        discard_mm=CASO_23["discard_mm"],
        discard_mode=CASO_23["discard_mode"],
        total_demand_per_day=CASO_23["demanda_total"],
        rainwater_share=CASO_23["rainwater_share"],
        store_daily_details=True,
    )

    cab = ("| Dia | Chuva | Descarte | Chuva efetiva | Captado | Demanda pluvial "
           "| Consumido | Extravasado | No reservatório | Atendimento |")
    sep = ("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |")
    uni = ("| | mm | mm | mm | L | L | L | L | L | |")
    linhas = [cab, sep, uni]

    nomes = {2: "pleno", 1: "parcial", 0: "nulo"}
    for i, d in enumerate(r.daily_results, start=1):
        descartado = d.precip_mm - d.eff_precip_mm
        linhas.append(
            f"| {i} | {br(d.precip_mm)} | {br(descartado)} | {br(d.eff_precip_mm)} "
            f"| {br(d.harvested_liters, 0)} | {br(d.pluvial_demand_liters, 0)} "
            f"| {br(d.pluvial_consumed_liters, 0)} | {br(d.spilled_liters, 0)} "
            f"| {br(d.lower_tank_end_liters, 0)} | {nomes[d.satisfaction_type]} |"
        )

    tot_cap = sum(d.harvested_liters for d in r.daily_results)
    tot_con = sum(d.pluvial_consumed_liters for d in r.daily_results)
    tot_ext = sum(d.spilled_liters for d in r.daily_results)
    final = r.daily_results[-1].lower_tank_end_liters
    linhas.append(
        f"| **soma** | | | | **{br(tot_cap, 0)}** | | **{br(tot_con, 0)}** "
        f"| **{br(tot_ext, 0)}** | {br(final, 0)} | |"
    )

    resumo = NL.join([
        "",
        "| Verificação do fechamento | Litros |",
        "| :--- | ---: |",
        f"| captado no período | {br(tot_cap, 0)} |",
        f"| menos o extravasado | −{br(tot_ext, 0)} |",
        f"| menos o consumido | −{br(tot_con, 0)} |",
        f"| menos o que ficou no reservatório | −{br(final, 0)} |",
        f"| **resíduo** | **{br(tot_cap - tot_ext - tot_con - final, 0)}** |",
        "",
    ])

    indicadores = NL.join([
        "",
        "| Indicador dos dez dias | Valor |",
        "| :--- | ---: |",
        f"| potencial de economia de água potável | {br(r.potential_potable_savings_pct)}% |",
        f"| média diária de pluvial consumida | {br(r.avg_pluvial_consumed_l_day)} L/dia |",
        f"| média diária de potável consumida | {br(r.avg_potable_consumed_l_day)} L/dia |",
        f"| média diária extravasada | {br(r.avg_spilled_l_day)} L/dia |",
        f"| dias de atendimento pleno | {br(r.pct_days_full_satisfaction, 0)}% |",
        f"| dias de atendimento parcial | {br(r.pct_days_partial_satisfaction, 0)}% |",
        f"| dias de atendimento nulo | {br(r.pct_days_null_satisfaction, 0)}% |",
        "",
    ])

    return NL.join(linhas) + NL + resumo + indicadores, r


def entrada_dez_dias():
    c = CASO_23
    return NL.join([
        "| Dado de entrada | Valor |",
        "| :--- | ---: |",
        f"| área de captação | {br(c['area'], 0)} m² |",
        f"| coeficiente de escoamento | {br(c['runoff_coeff'], 2)} |",
        f"| lâmina de descarte | {br(c['discard_mm'])} mm, em todo evento |",
        f"| demanda total | {br(c['demanda_total'], 0)} L/dia |",
        f"| fração atendível por água pluvial | {br(c['rainwater_share'] * 100, 0)}% "
        f"= {br(c['demanda_total'] * c['rainwater_share'], 0)} L/dia |",
        f"| volume do reservatório inferior | {br(c['volume'], 0)} L |",
        "| reservatório superior | não há |",
        "",
        "A série de chuva dos dez dias, em milímetros:",
        "",
        "| Dia | " + " | ".join(str(i) for i in range(1, 11)) + " |",
        "| ---: |" + " ---: |" * 10,
        "| Chuva | " + " | ".join(br(p) for p in CHUVA_23) + " |",
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Parte 2 — o projeto do tutorial: residência unifamiliar em Florianópolis
# ──────────────────────────────────────────────────────────────────────────────
#
# Um projeto só, que cresce ao longo de dez capítulos. Escolhido porque a série de
# Florianópolis é longa, a tarifa da CASAN é auditável e o caso é o mais comum do
# Brasil.

SERIE_TUTORIAL = os.path.join(
    os.path.dirname(AQUI), "data", "rainfall", "Florianopolis1.csv")
ANOS_TUTORIAL = 30

TUTORIAL = {
    "area": 150.0,             # m² de cobertura, projeção horizontal
    "runoff_coeff": 0.85,      # telha cerâmica
    "discard_mm": 2.0,         # NBR 15527, sem dado local
    "discard_mode": 1,         # todo evento de chuva
    "moradores": 4,
    "per_capita": 150.0,       # L/hab·dia
    # Bacia sanitária e usos externos. A máquina de lavar roupa saiu em
    # 2026-09-18: está fora dos usos do item 4.1.7 da ABNT NBR 15527:2019.
    "rainwater_share": 0.28,
    "volume_inicial": 3000.0,  # o primeiro palpite, do capítulo 6
    # A partir da seção do reservatório superior, o projeto adota recalque para
    # caixa elevada: é a comparação daquela seção, com o limiar de 100 L.
    "caixa_superior_l": 1000.0,
    "limiar_recalque_l": 100.0,
    # O volume que o tutorial escolhe: ideal pelo ganho marginal de 1 %/m³. Desde a
    # 0.2.0, o multicritério de oito critérios com pesos iguais indica um volume menor
    # (2.000 L); o capítulo 12 mostra o que os 4.000 L cedem.
    "volume": 4000.0,
}

VOLUME = TUTORIAL["volume"]


def vol_br(v=None):
    """Volume em litros com separador de milhar: 4.000 L."""
    v = VOLUME if v is None else v
    return f"{int(round(v)):,}".replace(",", ".") + " L"

VOLUMES_VARREDURA = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000,
                     10000, 12000, 16000, 20000]


def faixa_br(faixa):
    """A faixa de escolha no padrão das tabelas: «2 000 a 3 000 L», «1 000 L» ou, com lacuna, a lista."""
    if not faixa:
        return "—"
    if faixa["min_volume_l"] == faixa["max_volume_l"]:
        return f"{br(faixa['min_volume_l'], 0)} L"
    if not faixa.get("contiguous", True):
        return ", ".join(br(v, 0) for v in faixa["volumes_l"]) + " L"
    return f"{br(faixa['min_volume_l'], 0)} a {br(faixa['max_volume_l'], 0)} L"


def _serie():
    from triton.core.parser import load_precipitation
    p = load_precipitation(SERIE_TUTORIAL)
    return p[: ANOS_TUTORIAL * 365]


def _config_tutorial(caixa=False):
    """Parâmetros de simulação do tutorial.

    ``caixa=True`` acrescenta o arranjo adotado na seção do reservatório
    superior; as seções anteriores estudam a cisterna sozinha.
    """
    t = TUTORIAL
    cfg = dict(
        area=t["area"], runoff_coeff=t["runoff_coeff"],
        discard_mm=t["discard_mm"], discard_mode=t["discard_mode"],
        total_demand_per_day=t["moradores"] * t["per_capita"],
        rainwater_share=t["rainwater_share"],
    )
    if caixa:
        cfg.update(upper_tank_vol=t["caixa_superior_l"], upper_tank_used=True,
                   pumping_threshold=t["limiar_recalque_l"])
    return cfg


def _config_projeto():
    """O projeto do tutorial depois da decisão pelo recalque para caixa superior."""
    return _config_tutorial(caixa=True)


def tabela_serie():
    """Capítulo 4: o que a série de Florianópolis tem dentro."""
    serie = _serie()
    anos = len(serie) / 365.25
    chuvosos = serie[serie > 0.1]
    return NL.join([
        "| A série de Florianópolis | Valor |",
        "| :--- | ---: |",
        f"| dias na série | {br(len(serie), 0)} |",
        f"| anos | {br(anos, 1)} |",
        f"| precipitação média anual | {br(serie.sum() / anos, 0)} mm |",
        f"| dias com chuva | {br((serie > 0.1).mean() * 100, 0)}% |",
        f"| chuva média nos dias chuvosos | {br(chuvosos.mean(), 1)} mm |",
        f"| maior chuva diária | {br(serie.max(), 1)} mm |",
        f"| dias abaixo da lâmina de descarte | {br(((serie > 0.1) & (serie <= 2.0)).mean() * 100, 0)}% |",
    ])


def tabela_primeira_simulacao():
    """Capítulo 6: o primeiro resultado, com o volume de palpite."""
    r = run_single_simulation(
        precip_data=_serie(), lower_tank_vol=TUTORIAL["volume_inicial"],
        **_config_tutorial())
    dem = TUTORIAL["moradores"] * TUTORIAL["per_capita"]
    return NL.join([
        "| Resultado com "
        + br(TUTORIAL["volume_inicial"], 0) + " L | Valor |",
        "| :--- | ---: |",
        f"| potencial de economia de água potável | **{br(r.potential_potable_savings_pct, 2)}%** |",
        f"| água pluvial consumida | {br(r.avg_pluvial_consumed_l_day, 1)} L/dia |",
        f"| água da rede consumida | {br(r.avg_potable_consumed_l_day, 1)} L/dia |",
        f"| água extravasada | {br(r.avg_spilled_l_day, 1)} L/dia |",
        f"| dias de atendimento pleno | {br(r.pct_days_full_satisfaction, 1)}% |",
        f"| dias de atendimento parcial | {br(r.pct_days_partial_satisfaction, 1)}% |",
        f"| dias de atendimento nulo | {br(r.pct_days_null_satisfaction, 1)}% |",
        f"| demanda pluvial pretendida | {br(dem * TUTORIAL['rainwater_share'], 0)} L/dia |",
        f"| volume anual poupado | {br(r.annual_pluvial_consumed_m3, 1)} m³/ano |",
    ]), r


def tabela_varredura():
    """Capítulo 7: a curva de retorno decrescente."""
    serie = _serie()
    cfg = _config_tutorial()
    linhas = [
        "| Volume | Potencial | Ganho sobre o anterior | Ganho por m³ acrescentado "
        "| Extravasado | Dias plenos |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        "| L | % | pontos percentuais | %/m³ | L/dia | % |",
    ]
    anterior = None
    dados = []
    for v in VOLUMES_VARREDURA:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg)
        if anterior is None:
            ganho, marginal = "—", "—"
        else:
            dp = r.potential_potable_savings_pct - anterior[1]
            dv = (v - anterior[0]) / 1000.0
            ganho, marginal = br(dp, 2), br(dp / dv, 2)
        linhas.append(
            f"| {br(v, 0)} | {br(r.potential_potable_savings_pct, 2)} | {ganho} "
            f"| {marginal} | {br(r.avg_spilled_l_day, 0)} | {br(r.pct_days_full_satisfaction, 1)} |"
        )
        dados.append((v, r.potential_potable_savings_pct))
        anterior = (v, r.potential_potable_savings_pct)
    return NL.join(linhas), dados


def tabela_limiar_e_custo():
    """Capítulo 7: o limiar decide o volume, e o volume decide o custo."""
    from triton.core.cost_estimates import estimate_tank_price
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.simulation import run_sweep_simulation

    serie = _serie()
    cfg = _config_tutorial()
    linhas_limiar = [
        "| Limiar declarado | Volume ideal | Potencial |",
        "| ---: | ---: | ---: |",
    ]
    for limiar in (3.0, 1.0, 0.5):
        r = run_sweep_simulation(
            precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
            delta_ideal_threshold=limiar, **cfg)
        linhas_limiar.append(
            f"| {br(limiar, 1)} %/m³ | {br(r.optimal_lower_tank_vol, 0)} L "
            f"| {br(r.optimal_potential_pct, 2)}% |"
        )

    linhas_custo = [
        "",
        f"| | {vol_br()} | 20.000 L |",
        "| :--- | ---: | ---: |",
    ]
    vals = {}
    for v in (VOLUME, 20000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg)
        preco = estimate_tank_price(float(v), "CONCRETO")
        amb = _config_ambiental()
        amb.lower_material_key = "CONCRETO"
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        vals[v] = (r.potential_potable_savings_pct, preco,
                   lca.lower_tank_mass_kg, lca.total_embodied_co2_kg)
    a, b = vals[VOLUME], vals[20000]
    linhas_custo += [
        f"| potencial de economia | {br(a[0], 2)}% | {br(b[0], 2)}% |",
        f"| preço da cisterna de concreto | R$ {br(a[1], 0)} | R$ {br(b[1], 0)} |",
        f"| massa de concreto | {br(a[2], 0)} kg | {br(b[2], 0)} kg |",
        f"| carbono incorporado do sistema | {br(a[3], 0)} kg CO₂e | {br(b[3], 0)} kg CO₂e |",
        f"| **razão de preço** | | **{br(b[1] / a[1], 1)}×** |",
        f"| **ganho de potencial** | | **+{br(b[0] - a[0], 2)} pontos** |",
    ]
    return NL.join(linhas_limiar) + NL + NL.join(linhas_custo)


# ── a tarifa e os custos do tutorial, declarados uma vez ─────────────────────
TARIFA_CASAN = [
    (0.0, 0.0, 46.34, -1),        # disponibilidade, soma por cima
    (0.0, 10.0, 3.08, 1),
    (10.0, 25.0, 14.31, 1),
    (25.0, 50.0, 19.14, 1),
    (50.0, 999999.0, 24.08, 1),
]
CUSTOS_TUTORIAL = dict(
    cost_labor=3500.0, cost_piping=1200.0, cost_accessories=1800.0,
    elec_tariff=0.69568, tma=0.5, inflation=0.35,
    analysis_period_years=20, tariff_escalation=12,
)


def _config_economica(volume_l, material="CONCRETO"):
    from triton.core.cost_estimates import estimate_tank_price
    from triton.core.parser import TritonConfig
    cfg = TritonConfig()
    cfg.water_tariffs = list(TARIFA_CASAN)
    cfg.sewage_mode, cfg.sewage_rate = 1, 100.0
    cfg.cost_lower_tank = estimate_tank_price(float(volume_l), material)
    # Recalque para caixa superior de 1.000 L em polietileno, com as duas
    # motobombas (principal e reserva) e o preço padrão do programa.
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = True
    cfg.upper_tank_vol = TUTORIAL["caixa_superior_l"]
    cfg.pumping_threshold = TUTORIAL["limiar_recalque_l"]
    cfg.cost_upper_tank = estimate_tank_price(TUTORIAL["caixa_superior_l"], "PEAD")
    cfg.residents_count = TUTORIAL["moradores"]
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    # A área, a lâmina de descarte e o descarte físico são os do tutorial e os
    # da interface. Antes a configuração econômica herdava a área de 100 m² e
    # a lâmina de 1 mm do padrão, e deixava o reservatório de descarte fora do
    # investimento, que a etapa 3 inclui por padrão.
    cfg.area = TUTORIAL["area"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.first_flush_system_enabled = True
    return cfg


def _config_ambiental(sim=None):
    """A configuração ambiental do tutorial, coerente com a econômica.

    O descarte físico entra com o carbono incorporado do reservatório de
    descarte e do separador de folhas, como na etapa 7 da interface. Com o
    resultado da simulação, a energia vem da mesma função que o econômico usa.
    """
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.roof_area_m2 = TUTORIAL["area"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.first_flush_system_enabled = True
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = True
    cfg.upper_tank_vol_liters = TUTORIAL["caixa_superior_l"]
    if sim is not None:
        cfg.annual_pump_kwh = compute_annual_pump_energy(_config_economica(VOLUME), sim).annual_kwh
    return cfg


def tabela_reservatorio_superior():
    """Capítulo 8: a comparação justa, com o mesmo armazenamento total."""
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy

    serie = _serie()
    cfg = _config_tutorial()
    unico = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME + 1000.0, **cfg)
    duplo = run_single_simulation(
        precip_data=serie, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **cfg)

    bomba = TritonConfig()
    bomba.upper_tank_used = True
    bomba.pump_power_kw, bomba.pump_efficiency, bomba.pump_flow_rate = 0.37, 0.0, 0.0
    bomba.pump_manometric_head_m, bomba.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(bomba, duplo)
    anos = duplo.total_days / 365.25

    L = [
        f"| Mesmo armazenamento de {vol_br(VOLUME + 1000)} | Um tanque só | {vol_br()[:-2]} embaixo + 1.000 em cima |",
        "| :--- | ---: | ---: |",
        f"| potencial de economia | {br(unico.potential_potable_savings_pct, 2)}% "
        f"| {br(duplo.potential_potable_savings_pct, 2)}% |",
        f"| dias de atendimento pleno | {br(unico.pct_days_full_satisfaction, 1)}% "
        f"| {br(duplo.pct_days_full_satisfaction, 1)}% |",
        f"| volume recalcado | — | {br(duplo.total_pumped_liters / anos / 1000, 1)} m³/ano |",
        f"| acionamentos da bomba | — | {br(duplo.total_pump_cycles / anos, 0)} por ano |",
        f"| horas de bomba | — | {br(e.pump_hours_year, 1)} h/ano |",
        f"| energia | — | {br(e.annual_kwh, 1)} kWh/ano |",
        f"| custo da energia | — | R$ {br(e.annual_kwh * 0.69568, 2)}/ano |",
        f"| **diferença de potencial** | | **{br(duplo.potential_potable_savings_pct - unico.potential_potable_savings_pct, 2)} pontos** |",
    ]
    return NL.join(L)


def tabela_limiar_de_acionamento():
    """Capítulo 8: o limiar troca potencial por desgaste da bomba."""
    serie = _serie()
    cfg = _config_tutorial()
    L = ["| Limiar de acionamento | Potencial | Acionamentos por ano |",
         "| ---: | ---: | ---: |"]
    for lim in (0, 100, 300, 500):
        r = run_single_simulation(
            precip_data=serie, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
            upper_tank_used=True, pumping_threshold=float(lim), **cfg)
        anos = r.total_days / 365.25
        L.append(f"| {br(lim, 0)} L | {br(r.potential_potable_savings_pct, 2)}% "
                 f"| {br(r.total_pump_cycles / anos, 0)} |")
    return NL.join(L)


def tabela_etap():
    """Capítulo 9: a classe recomenda, o projetista decide."""
    from triton.core.water_quality import WATER_QUALITY_CLASSES, size_etap

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3

    L = ["| Desinfecção | CAPEX | Custeio anual | CO₂e anual |",
         "| :--- | ---: | ---: | ---: |"]
    nomes = {"cloro": "Cloração por pastilhas",
             "uv": "Cloração + ultravioleta",
             "ozonio": "Cloração + ozonização"}
    for des in ("cloro", "uv", "ozonio"):
        e = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=m3,
                      roof_area_m2=150.0, disinfection_choice=des,
                      discard_mm=2.0, include_first_flush=True)
        L.append(f"| {nomes[des]} | R$ {br(e.total_etap_capex, 0)} "
                 f"| R$ {br(e.total_etap_annual_opex, 0)} "
                 f"| {br(e.total_etap_co2e_kg_yr, 1)} kg |")

    L += ["", "| Classe alvo | Recomenda filtração fina? | CAPEX sem | CAPEX com |",
          "| :--- | :---: | ---: | ---: |"]
    for cid, c in WATER_QUALITY_CLASSES.items():
        sem = size_etap(target_class_id=cid, annual_pluvial_consumed_m3=m3,
                        roof_area_m2=150.0, include_polishing_filter=False,
                        discard_mm=2.0, include_first_flush=True)
        com = size_etap(target_class_id=cid, annual_pluvial_consumed_m3=m3,
                        roof_area_m2=150.0, include_polishing_filter=True,
                        discard_mm=2.0, include_first_flush=True)
        L.append(f"| {cid.replace('_', ' ')} | {'sim' if c.exige_filtracao_fina else 'não'} "
                 f"| R$ {br(sem.total_etap_capex, 0)} | R$ {br(com.total_etap_capex, 0)} |")
    return NL.join(L)


def tabela_economica():
    """Capítulo 10: a conta da CASAN, com e sem o sistema."""
    from triton.core.economic import calculate_water_bill, run_economic_analysis

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    dias_mes = 30.4375
    tot_m3 = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * dias_mes / 1000.0
    pot_m3 = r.avg_potable_consumed_l_day * dias_mes / 1000.0
    sem = calculate_water_bill(tot_m3 * 1000, TARIFA_CASAN, 1, 100.0, 0.0, 0.0)
    com = calculate_water_bill(pot_m3 * 1000, TARIFA_CASAN, 1, 100.0, 0.0, 0.0)

    cfg = _config_economica(VOLUME, "CONCRETO")
    e = run_economic_analysis(cfg, r)

    L = [
        "| A fatura da CASAN | Consumo | Valor |",
        "| :--- | ---: | ---: |",
        f"| sem o sistema | {br(tot_m3, 2)} m³/mês | R$ {br(sem, 2)} |",
        f"| com o sistema | {br(pot_m3, 2)} m³/mês | R$ {br(com, 2)} |",
        f"| **economia** | {br(tot_m3 - pot_m3, 2)} m³/mês | **R$ {br(sem - com, 2)}** |",
        "",
        "| Análise de 20 anos | Valor |",
        "| :--- | ---: |",
        f"| investimento inicial | R$ {br(e.capex_total, 2)} |",
        f"| economia anual com água | R$ {br(e.annual_water_savings_brl, 2)} |",
        f"| custeio anual | R$ {br(e.annual_opex_brl, 2)} |",
        f"| valor presente líquido | R$ {br(e.vpl, 2)} |",
        f"| taxa interna de retorno | {br(e.tir_annual_pct or 0.0, 2)}% ao ano |",
        f"| payback descontado | {br(e.payback_years or 0.0, 1)} anos |",
    ]
    return NL.join(L)


def tabela_materiais():
    """Capítulo 11: o material decide o sinal do resultado ambiental."""
    from triton.core.cost_estimates import estimate_tank_price
    from triton.core.environmental import MATERIAL_PRESETS, EnvironmentalConfig, calculate_lca

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3
    # Emissoes liquidas, e nao saldo: positivo emite, negativo retira. E a
    # convencao do grafico de balanco da aba ambiental do programa, e a mesma
    # das figuras deste capitulo desde a inversao de sinal.
    L = ["| Material da cisterna | Massa | Carbono incorporado | Payback de carbono "
         "| Emissões líquidas em 20 anos | Preço |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    nomes = {"PEAD": "Polietileno (PEAD)", "CONCRETO": "Concreto armado",
             "FIBRA": "Fibra de vidro", "ACO_INOX": "Aço inoxidável"}
    for k in MATERIAL_PRESETS:
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        l = calculate_lca(VOLUME, m3, cfg)
        try:
            preco = f"R$ {br(estimate_tank_price(VOLUME, k), 0)}"
        except Exception:
            preco = "—"
        L.append(f"| {nomes.get(k, k)} | {br(l.lower_tank_mass_kg, 0)} kg "
                 f"| {br(l.total_embodied_co2_kg, 0)} kg CO₂e "
                 f"| {br(l.environmental_payback_years, 1)} anos "
                 f"| {br(-l.lifetime_net_co2_saved_kg, 0)} kg | {preco} |")

    L += ["", "| Volume em concreto | Payback de carbono | Emissões líquidas em 20 anos |",
          "| ---: | ---: | ---: |"]
    for v in (2000, 3000, VOLUME, 8000):
        rr = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                   **_config_projeto())
        cfg = _config_ambiental(rr)
        cfg.lower_material_key = "CONCRETO"
        l = calculate_lca(float(v), rr.annual_pluvial_consumed_m3, cfg)
        L.append(f"| {br(v, 0)} L | {br(l.environmental_payback_years, 1)} anos "
                 f"| {br(-l.lifetime_net_co2_saved_kg, 0)} kg CO₂e |")
    return NL.join(L)


def tabela_multicriterio():
    """Capítulo 12: oito critérios em quatro eixos, e o volume que cada um prefere."""
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import calculate_lca
    from triton.core.topsis import _decision_matrix, calculate_topsis_scores, candidato_dos_resultados

    serie = _serie()
    cfg_sim = _config_projeto()
    cands = []
    for v in (1000, 2000, 3000, 4000, 5000, 8000, 12000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg_sim)
        e = run_economic_analysis(_config_economica(v, "PEAD"), r)
        amb = _config_ambiental(r)
        amb.lower_material_key = "PEAD"
        l = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        # A mesma montagem da linha de comando e da interface: os oito critérios do programa.
        cands.append(candidato_dos_resultados(r, e, l.lifetime_net_co2_saved_kg))

    m = _decision_matrix(cands)
    linhas = [
        "| Volume | Confiabilidade | Eficiência | VPL | LCOW | Payback | CO₂e líquido | Massa | Extravasamento |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        "| L | % | % ao dia | R$ | R$/m³ | anos | kg em 20 anos | kg a seco | m³/ano |",
    ]
    for c, x in zip(cands, m):
        linhas.append(
            f"| {br(c.lower_tank_vol, 0)} | {br(x[0], 1)} | {br(x[1], 2)} | {br(x[2], 0)} "
            f"| {br(x[3], 2)} | {br(x[4], 1)} | {br(x[5], 0).replace('-', '−')} | {br(x[6], 0)} "
            f"| {br(x[7], 1)} |")

    res = calculate_topsis_scores(cands)
    global _CANDIDATOS_MULTICRITERIO
    _CANDIDATOS_MULTICRITERIO = cands
    menor_lcow = min(range(len(cands)), key=lambda i: (m[i, 3], cands[i].lower_tank_vol))
    linhas += [
        "",
        "| Critério | Volume |",
        "| :--- | ---: |",
        f"| maior confiabilidade volumétrica | {br(cands[res.technical_best_index].lower_tank_vol, 0)} L |",
        f"| menor payback descontado, desempate pelo VPL | {br(cands[res.financial_best_index].lower_tank_vol, 0)} L |",
        f"| menor custo nivelado da água (LCOW) | {br(cands[menor_lcow].lower_tank_vol, 0)} L |",
        f"| menor CO₂e de ciclo de vida | {br(cands[res.environmental_best_index].lower_tank_vol, 0)} L |",
        # O multicritério não elege um volume: devolve a faixa de escolha (escores a até 5% da amplitude
        # do maior). O maior escore fica como informação.
        f"| **faixa de escolha do TOPSIS, 25% em cada eixo** | **{faixa_br(res.faixa_de_escolha())}** |",
        f"| maior escore do TOPSIS, 25% em cada eixo | {br(cands[res.best_index].lower_tank_vol, 0)} L |",
    ]
    return NL.join(linhas)


_CANDIDATOS_MULTICRITERIO = None

#: Pesos dos quatro eixos (técnico, econômico, ambiental, estrutural) da tabela de sensibilidade:
#: iguais, 70% no eixo dominante com 10% em cada um dos outros três, como os perfis da interface,
#: e os pesos objetivos do CRITIC.
PESOS_SENSIBILIDADE = (
    ("pesos iguais, 25% em cada eixo", (0.25, 0.25, 0.25, 0.25)),
    ("técnico, 70%", (0.7, 0.1, 0.1, 0.1)),
    ("econômico, 70%", (0.1, 0.7, 0.1, 0.1)),
    ("ambiental, 70%", (0.1, 0.1, 0.7, 0.1)),
    ("estrutural, 70%", (0.1, 0.1, 0.1, 0.7)),
    # Pesos objetivos, calculados dos próprios resultados (seção 32); a linha mostra a soma por eixo.
    ("pesos objetivos, CRITIC", "critic"),
)


def tabela_pesos():
    """Capítulo 12: o volume escolhido pelo TOPSIS conforme o peso dominante."""
    from triton.core.topsis import calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    i_tutorial = [c.lower_tank_vol for c in cands].index(VOLUME)
    L = [f"| Ponderação | Faixa de escolha | Maior escore | Posição de {vol_br()} |",
         "| :--- | ---: | ---: | ---: |"]
    for rotulo, pesos in PESOS_SENSIBILIDADE:
        res = calculate_topsis_scores(cands, weights=pesos)
        if pesos == "critic":
            # Os pesos que o CRITIC deu aos oito critérios, somados por eixo.
            w = res.criterion_weights
            eixos = (("técnico", w[0] + w[1]), ("econômico", w[2] + w[3] + w[4]),
                     ("ambiental", w[5]), ("estrutural", w[6] + w[7]))
            rotulo += ": " + ", ".join(f"{nome} {br(100 * x, 1)}%" for nome, x in eixos)
        L.append(f"| {rotulo} | {faixa_br(res.faixa_de_escolha())} "
                 f"| {br(res.best_candidate.lower_tank_vol, 0)} L | {int(res.rankings[i_tutorial])}º |")
    return NL.join(L)


#: Pressão de trabalho da comparação de pressurizadores, e a de uma casa mais alta.
PRESSOES_PRESSURIZADOR = (18.0, 24.0)


def tabela_pressurizadores():
    """Seção 28: seis pressurizadores de catálogo no projeto do tutorial."""
    from triton.core.pressurizer_catalog import (
        CATALOGO, ELETRONICO, FLUXOSTATO, PRESSOSTATO, VAZAO_DO_PONTO_PADRAO_L_MIN, energia)
    from triton.core.supply_arrangement import DESCARGAS_POR_PESSOA_DIA

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_tutorial())
    v = r.annual_pluvial_consumed_m3
    partidas = TUTORIAL["moradores"] * DESCARGAS_POR_PESSOA_DIA * 365.25
    controle = {PRESSOSTATO: "pressostato", ELETRONICO: "eletrônico", FLUXOSTATO: "fluxostato"}
    h1, h2 = PRESSOES_PRESSURIZADOR
    L = [f"| Modelo | Controle | Vazão da curva a {br(h1, 0)} m.c.a. | Horas por ano "
         f"| kWh por ano | kWh/m³ | kWh por ano a {br(h2, 0)} m.c.a. |",
         "| :--- | :--- | ---: | ---: | ---: | ---: | ---: |"]
    linhas = []
    for p in CATALOGO:
        e1 = energia(p, v, h1, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        e2 = energia(p, v, h2, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        linhas.append((e1.kwh_ano, p, e1, e2))
    for _, p, e1, e2 in sorted(linhas, key=lambda x: x[0]):
        a24 = br(e2.kwh_ano, 1) if e2.atende else "não alcança"
        L.append(f"| {p.rotulo} | {controle[p.controle]} | {br(e1.vazao_da_bomba_l_min, 1)} L/min "
                 f"| {br(e1.horas_ano, 0)} | {br(e1.kwh_ano, 1)} | {br(e1.kwh_por_m3, 2)} | {a24} |")
    return NL.join(L), v, partidas


#: Premissas perturbadas na tabela da seção 20: (rótulo, unidade, baixo, provável, alto).
PREMISSAS_SENSIBILIDADE = (
    ("reajuste das tarifas de água e esgoto", "% ao ano", 3.0, 5.0, 7.0),
    ("taxa mínima de atratividade", "% ao mês", 0.3, 0.5, 0.7),
    ("consumo per capita", "L/hab·dia", 120.0, 150.0, 180.0),
    ("fração atendível", "%", 20.0, 28.0, 40.0),
    ("preço da cisterna", "% do orçamento", 70.0, 100.0, 130.0),
)


def _projeto_fechado(ajuste=None):
    """Potencial, VPL e retorno do projeto fechado do tutorial, com uma premissa mudada."""
    from triton.core.economic import run_economic_analysis
    cfg_sim = _config_projeto()
    cfg_eco = _config_economica(VOLUME, "PEAD")
    nome, valor = ajuste if ajuste else (None, None)
    if nome == "consumo per capita":
        cfg_sim["total_demand_per_day"] = TUTORIAL["moradores"] * valor
    elif nome == "fração atendível":
        cfg_sim["rainwater_share"] = valor / 100.0
    elif nome == "reajuste das tarifas de água e esgoto":
        cfg_eco.water_tariff_escalation = cfg_eco.sewage_tariff_escalation = valor
    elif nome == "taxa mínima de atratividade":
        cfg_eco.tma = valor
    elif nome == "preço da cisterna":
        cfg_eco.cost_lower_tank *= valor / 100.0
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **cfg_sim)
    e = run_economic_analysis(cfg_eco, r)
    return r.potential_potable_savings_pct, e.vpl, e.payback_years


def tabela_sensibilidade():
    """Seção 20: cada premissa variada sozinha, no projeto fechado do tutorial."""
    L = ["| Premissa | Baixa | Provável | Alta | Potencial | VPL em 20 anos | Payback descontado |",
         "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for rotulo, unidade, baixo, provavel, alto in PREMISSAS_SENSIBILIDADE:
        res = [_projeto_fechado((rotulo, v)) for v in (baixo, alto)]
        def pb(x):
            return br(x, 1) + " anos" if x else "não retorna"
        L.append(
            f"| {rotulo}, {unidade} | {br(baixo, 1)} | {br(provavel, 1)} | {br(alto, 1)} "
            f"| {br(res[0][0], 2)}% a {br(res[1][0], 2)}% "
            f"| R$ {br(res[0][1], 0)} a R$ {br(res[1][1], 0)} "
            f"| {pb(res[0][2])} a {pb(res[1][2])} |")
    return NL.join(L)


def tabela_decisao():
    """Seção 32: escore TOPSIS e aceitabilidade SMAA de cada volume do tutorial."""
    from triton.core.mcdm_methods import run_smaa_analysis
    from triton.core.topsis import calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    topsis = calculate_topsis_scores(cands)
    smaa = run_smaa_analysis(cands, num_samples=5000, random_seed=42)
    ordem = sorted(range(len(cands)), key=lambda i: -topsis.scores[i])
    posicao = {i: k + 1 for k, i in enumerate(ordem)}
    L = ["| Volume | Escore TOPSIS | Posição TOPSIS | Primeiro lugar no SMAA-VIKOR, b¹ |",
         "| ---: | ---: | ---: | ---: |"]
    for i, c in enumerate(cands):
        L.append(f"| {br(c.lower_tank_vol, 0)} L | {br(topsis.scores[i], 3)} | {posicao[i]}º "
                 f"| {br(float(smaa.first_rank_probs[i]), 1)}% |")
    return NL.join(L)


CIDADES_GUIA14 = ("Florianopolis1", "SaoPaulo1", "Brasilia1", "Manaus1")
NOMES_CIDADES = {
    "Florianopolis1": "Florianópolis", "SaoPaulo1": "São Paulo",
    "Brasilia1": "Brasília", "Manaus1": "Manaus",
}


def tabela_cidades():
    """Guia 14: o regime de chuva manda mais que a lâmina anual."""
    from datetime import datetime, timedelta

    import numpy as np

    from triton.core.parser import load_precipitation
    from triton.core.simulation import run_sweep_simulation

    cfg = _config_tutorial()
    L = ["| Cidade | Chuva anual | Dias com chuva | Razão entre o mês mais e o menos "
         f"chuvoso | Potencial com {vol_br()} | Volume ideal |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for chave in CIDADES_GUIA14:
        caminho = os.path.join(os.path.dirname(AQUI), "data", "rainfall", chave + ".csv")
        if not os.path.exists(caminho):
            continue
        serie = load_precipitation(caminho)[: ANOS_TUTORIAL * 365]
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **cfg)
        sw = run_sweep_simulation(
            precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
            delta_ideal_threshold=1.0, **cfg)
        d0 = datetime(1980, 1, 1)
        meses = np.zeros(12)
        for i, v in enumerate(serie):
            meses[(d0 + timedelta(days=int(i))).month - 1] += float(v)
        meses /= ANOS_TUTORIAL
        razao = meses.max() / max(meses.min(), 0.1)
        L.append(
            f"| {NOMES_CIDADES.get(chave, chave)} | {br(serie.sum() / anos, 0)} mm "
            f"| {br((serie > 0.1).mean() * 100, 0)}% | {br(razao, 1)}× "
            f"| {br(r.potential_potable_savings_pct, 2)}% "
            f"| {br(sw.optimal_lower_tank_vol, 0)} L |")
    return NL.join(L)


#: A legenda de cada tabela gerada. Fica aqui, e não no capítulo, porque é aqui
#: que a tabela nasce; a montagem só lhe acrescenta o número.
LEGENDAS = {
    'cap10_capex_cadeia.md': [
        'Rubricas do investimento que o programa calcula sozinho, a regra de cada uma, o parâmetro que a governa e o valor padrão',
    ],
    'cap10_capex_reservatorios.md': [
        'Preço de reservatório por volume e por material, obtido pela interpolação da tabela do polietileno e pelo fator de cada material',
    ],
    'cap10_capex_tubos.md': [
        'Preço por metro dos tubos de PVC por diâmetro nominal, sem e com o acréscimo de 25% de conexões',
    ],
    'cap10_capex_pecas.md': [
        'Peças do arranjo 3D que o programa orça sozinho, com o preço de referência e o destino no investimento',
    ],
    'cap10_capex_bombas.md': [
        'Motobombas do assistente de dimensionamento, com o preço do catálogo e o preço que a fórmula do estimador daria para a mesma potência',
    ],
    'cap10_capex_etap.md': [
        'Preço da linha de tratamento e do descarte inicial, conforme o componente e a condição que o escolhe',
    ],
    'cap10_capex_tipologias.md': [
        'Subsistemas calibrados das cinco tipologias residenciais da base de custos',
        'Orçamento calibrado de cada tipologia para uma cisterna de 5.000 L em polietileno, pela função de estimativa calibrada (fora do caminho da interface)',
    ],
    'cap10_capex_regional.md': [
        'Fator regional de custo por unidade da federação',
    ],
    'cap10_capex_procedencia.md': [
        'O que a base de custos registra sobre a origem e a data dos próprios números',
    ],
    'cap10_capex_constantes.md': [
        'Constantes que o código usa para orçar e que a base de custos não acompanha com fonte e data',
    ],
    'cap10_capex_exemplo.md': [
        'Investimento do projeto do tutorial com os valores digitados e com os valores que o programa calcularia sozinho',
    ],
    'cap10_opex_itens.md': [
        'Itens que entram sozinhos no custeio anual de um projeto novo, com valor padrão, periodicidade, origem e modo de alterar',
    ],
    'cap10_opex_energia.md': [
        'Tarifa de energia da base de municípios',
        'Acréscimo de cada bandeira tarifária sobre a tarifa de energia',
    ],
    'cap10_opex_peso.md': [
        'Efeito das três rotinas de manutenção de partida sobre o custeio do resumo e sobre o resultado do projeto do tutorial',
    ],
    'cap10_opex_premissas.md': [
        'Premissas da projeção no projeto novo e no tutorial',
        'Perfis de referência que a etapa 4 oferece',
    ],
    'cap30_inventario.md': [
        'Inventário de carbono do projeto fechado do tutorial, item a item, com a parcela de cada componente no carbono incorporado; valores anuais negativos são crédito',
    ],
    'cap24_metodos.md': [
        'Volumes dados pelos métodos do Anexo A da ABNT NBR 15527:2007 para o projeto do tutorial, arredondados a 250 L, e o potencial que cada um produz na simulação diária',
        'Fração de armazenamento dos volumes da varredura e o passo de simulação que Fewkes e Butler (2000) recomendam para cada faixa',
    ],
    # Uma legenda por tabela, na ordem em que aparecem no arquivo. Antes só a
    # primeira tabela recebia legenda, e regenerar apagava as demais.
    'cap23_entrada.md': [
        'Dados de entrada do caso resolvido de dez dias',
        'Série de precipitação dos dez dias do caso resolvido',
    ],
    'cap23_dez_dias.md': [
        'Balanço hídrico diário do caso resolvido, dia a dia, com as parcelas de captação, consumo, extravasamento e armazenamento',
        'Verificação do fechamento do balanço de massa nos dez dias',
        'Indicadores resultantes do caso resolvido de dez dias',
    ],
    'cap04_serie.md': [
        'Caracterização da série de precipitação de Florianópolis adotada no tutorial',
    ],
    'cap06_primeira_simulacao.md': [
        'Resultado da primeira simulação do tutorial, com reservatório de 3.000 L',
    ],
    'cap07_varredura.md': [
        'Varredura de volumes do projeto do tutorial, com o ganho marginal de cada metro cúbico acrescentado',
    ],
    'cap07_limiar_e_custo.md': [
        'Volume ideal obtido com cada limiar de ganho marginal, para o mesmo projeto',
        'Custo e desempenho comparados entre o volume ideal e o volume máximo varrido',
    ],
    'cap08_reservatorio_superior.md': [
        'Comparação entre reservatório único e reservatório duplo, mantido o mesmo armazenamento total',
    ],
    'cap08_limiar.md': [
        'Efeito do limiar de acionamento da motobomba sobre o potencial de economia e sobre o número de acionamentos',
    ],
    'cap09_etap.md': [
        'Custo da linha de tratamento conforme a tecnologia de desinfecção adotada',
        'Recomendação de filtração fina e custo da linha por classe de qualidade',
    ],
    'cap10_economico.md': [
        'Composição da fatura de água e esgoto antes e depois do sistema pluvial',
        'Indicadores econômicos do projeto do tutorial em vinte anos de análise',
    ],
    'cap11_materiais.md': [
        'Emissões líquidas de carbono do projeto do tutorial conforme o material do reservatório',
        'Efeito do volume da cisterna de concreto sobre as emissões líquidas de carbono',
    ],
    'cap32_decisao.md': [
        'Escore de proximidade TOPSIS com 25% de peso em cada um dos quatro eixos e aceitabilidade de primeiro lugar no SMAA-VIKOR, com 5.000 vetores de oito pesos sorteados com 25% esperado em cada eixo, para os volumes do tutorial',
    ],
    'cap20_sensibilidade.md': [
        'Potencial, valor presente líquido e retorno do projeto fechado do tutorial com cada premissa variada sozinha, do valor baixo ao alto',
    ],
    'cap28_pressurizadores.md': [
        'Energia anual de seis pressurizadores de catálogo na pressurização direta do tutorial, com a vazão da bacia sanitária limitando a da bomba',
    ],
    'cap12_pesos.md': [
        'Faixa de escolha do TOPSIS (volumes com escore a até 5% da amplitude do maior), volume de maior escore e posição do volume do tutorial, com pesos iguais, com 70% num eixo e 10% em cada um dos outros três, e com os pesos objetivos do CRITIC',
    ],
    'cap12_multicriterio.md': [
        'Matriz de decisão multicritério com os oito critérios dos quatro eixos para cada volume candidato em polietileno',
        'Volume vencedor segundo cada critério isolado, e a faixa de escolha e o maior escore do TOPSIS com 25% em cada eixo',
    ],
    'cap14_cidades.md': [
        'O mesmo projeto do tutorial simulado em quatro capitais brasileiras',
    ],
}


def _rippl(deficits):
    """Maior deficit acumulado: o volume que o método de Rippl exige."""
    acumulado, maximo = 0.0, 0.0
    for d in deficits:
        acumulado = max(0.0, acumulado + d)
        maximo = max(maximo, acumulado)
    return maximo


def tabela_metodos_empiricos():
    """Seção do volume ideal: os métodos do Anexo A da NBR 15527:2007 contra a simulação."""
    import numpy as np
    t = TUTORIAL
    serie = _serie()
    anos = len(serie) / 365.25
    P = serie.sum() / anos
    A, C = t["area"], t["runoff_coeff"]
    demanda = t["moradores"] * t["per_capita"] * t["rainwater_share"]
    oferta_anual_l = P * A * C
    demanda_anual_l = demanda * 365.25

    rippl_diario = _rippl(demanda - serie * A * C)
    mensal = []
    for a in range(len(serie) // 365):
        ano = serie[a * 365:(a + 1) * 365]
        limites = np.linspace(0, 365, 13).astype(int)
        for k in range(12):
            trecho = ano[limites[k]:limites[k + 1]]
            mensal.append(demanda * len(trecho) - trecho.sum() * A * C)
    rippl_mensal = _rippl(mensal)

    metodos = [
        ("prático alemão", "6% do menor entre oferta e demanda anuais",
         0.06 * min(oferta_anual_l, demanda_anual_l)),
        ("Rippl, série mensal", "maior déficit acumulado, meses", rippl_mensal),
        ("Azevedo Neto, T = 1 mês", "0,042 × P × A × T", 0.042 * P * A * 1),
        ("Rippl, série diária", "maior déficit acumulado, dias", rippl_diario),
        ("prático inglês", "0,05 × P × A", 0.05 * P * A),
    ]
    L = ["| Método | Regra | Volume | Potencial simulado |",
         "| :--- | :--- | ---: | ---: |"]
    for nome, regra, volume in metodos:
        v = round(volume / 250.0) * 250.0
        r = run_single_simulation(precip_data=serie, lower_tank_vol=v, **_config_tutorial())
        L.append(f"| {nome} | {regra} | {br(v, 0)} L | {br(r.potential_potable_savings_pct, 2)}% |")
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **_config_tutorial())
    L.append(f"| **simulação diária, ganho marginal de 1 %/m³** | varredura | **{br(VOLUME, 0)} L** "
             f"| **{br(r.potential_potable_savings_pct, 2)}%** |")

    F = ["", "| Volume | Fração de armazenamento S/(A·R) | Passo recomendado por Fewkes e Butler |",
         "| ---: | ---: | :--- |"]
    for v in (1, 2, 3, 4, 8, 12, 20):
        fr = v / (A * P / 1000.0)
        passo = "horário" if fr <= 0.01 else ("diário" if fr <= 0.125 else "mensal")
        F.append(f"| {br(v * 1000, 0)} L | {br(fr, 4)} | {passo} |")
    return NL.join(L + F)


def tabela_inventario():
    """Seção de ciclo de vida: o inventário do projeto fechado, item a item."""
    from triton.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    cfg = _config_ambiental(r)
    cfg.lower_material_key = "PEAD"
    lca = calculate_lca(VOLUME, r.annual_pluvial_consumed_m3, cfg)
    nomes = {
        "Cisterna Inferior": f"cisterna de {vol_br()}, polietileno",
        "Caixa d'Água Superior": "caixa superior de 1.000 L, polietileno",
        "Motobomba": "duas motobombas de meio CV",
        "Sistema de Descarte": "descarte inicial: reservatório de 300 L e separador de folhas",
        "Consumo Elétrico": "energia do recalque",
        "Linha de Tratamento": "cloração por pastilhas",
        "Água Potável Evitada": "água potável evitada",
    }
    def nome(categoria):
        for chave, rotulo in nomes.items():
            if categoria.startswith(chave):
                return rotulo
        if categoria.startswith("Tubulação"):
            return "tubulação de PVC, DN " + categoria.split("DN ")[1].split(" ")[0] + " mm"
        return categoria
    total = lca.total_embodied_co2_kg
    L = ["| Item | Incorporado | Parcela do incorporado | Anual |",
         "| :--- | ---: | ---: | ---: |"]
    for it in lca.inventory_items:
        inc = f"{br(it.embodied_co2_kg, 1)} kg" if it.embodied_co2_kg else "—"
        parcela = f"{br(it.embodied_co2_kg / total * 100, 1)}%" if it.embodied_co2_kg else "—"
        anual = f"{br(it.annual_op_co2_kg, 2)} kg/ano" if it.annual_op_co2_kg else "—"
        L.append(f"| {nome(it.category)} | {inc} | {parcela} | {anual} |")
    L.append(f"| **total** | **{br(total, 1)} kg** | **100%** "
             f"| **{br(-lca.net_annual_avoided_co2_kg, 2)} kg/ano** |")
    return NL.join(L)


# ──────────────────────────────────────────────────────────────────────────────
# Seção 10 — como o CAPEX é calculado sozinho e o que entra sozinho no custeio
# ──────────────────────────────────────────────────────────────────────────────
#
# Nada aqui é digitado: cada número sai de triton/data/costs_database.json, das constantes de
# triton/core (cost_estimates, quantitativo_do_arranjo, water_quality, chlorination, parser) ou de
# uma chamada às próprias funções de cálculo. Quem muda um preço no programa muda a tabela, e o
# teste tests/unit/test_manual_capex_opex.py confere os dois lados.
#
# Como rodar só estas tabelas (sem regerar as demais, que têm legendas revisadas à mão):
#     python manual/gerar_tabelas.py custos

def _rs(v, casas=2):
    return f"R$ {br(v, casas)}"


def _data_iso(texto):
    """«2026-09-09» → «09/09/2026»; «2026-08» → «08/2026»."""
    partes = str(texto).split("-")
    return "/".join(reversed(partes))


def _pct(v, casas=0):
    return f"{br(v * 100.0, casas)}%"


def tabela_capex_cadeia():
    """A cadeia do CAPEX automático: rubrica, regra, parâmetro e valor padrão."""
    from triton.core import cost_estimates as ce
    from triton.core.parser import TritonConfig
    from triton.core.quantitativo_do_arranjo import CATALOGO_DE_PECAS

    cfg = TritonConfig()
    inf, sup = ce.LOWER_TANK_PRICE_TABLE, ce.UPPER_TANK_PRICE_TABLE
    pisos = ce.estimate_preliminary_capex(100.0, 0.0, False)   # reservatório mínimo: só os pisos aparecem
    fatores = list(ce.REGIONAL_FACTORS_BY_UF.values())
    return NL.join([
        "| Rubrica | Como o programa a calcula | Parâmetro | Valor padrão |",
        "| :--- | :--- | :--- | :--- |",
        "| cisterna | interpola linearmente a tabela de preços do polietileno pelo volume e multiplica pelo fator do material "
        "| `lower_tank_pead_prices`, `material_multipliers` "
        f"| {len(inf)} preços, de {vol_br(inf[0][0])} a {vol_br(inf[-1][0])} |",
        "| caixa superior | a mesma interpolação, na tabela própria da caixa, com o volume da caixa "
        "| `upper_tank_pead_prices`, `upper_tank_vol` "
        f"| {len(sup)} preços, de {vol_br(sup[0][0])} a {vol_br(sup[-1][0])}; caixa de {vol_br(cfg.upper_tank_vol)} |",
        "| motobombas | custo unitário vezes o número de motobombas; zero no abastecimento por gravidade "
        "| `pump_unit_cost`, `pump_count` do projeto "
        f"| {_rs(cfg.pump_unit_cost)} por unidade, {cfg.pump_count} unidades |",
        "| tubulação | soma, no arranjo 3D, dos metros de tubo de cada diâmetro vezes o preço por metro, mais curvas, conexões de extremidade e tês "
        "| `pipes_cost_per_meter` e as peças de linha do arranjo "
        f"| {len(ce.PIPE_COST_PER_METER)} diâmetros, de DN {min(ce.PIPE_COST_PER_METER)} a DN {max(ce.PIPE_COST_PER_METER)} |",
        "| acessórios | soma, no arranjo 3D, do preço de cada peça (registros, válvulas, quadro, sensores, air gap, hidrômetro) e dos cabos de comando "
        "| `CATALOGO_DE_PECAS`, que `pecas_do_arranjo` pode sobrescrever "
        f"| {len(CATALOGO_DE_PECAS)} tipos de peça |",
        "| mão de obra | percentual da soma de cisterna, caixa, motobombas, tubulação e acessórios, com um piso "
        "| `labor_percentage`, `MAO_DE_OBRA_MINIMA` "
        f"| {_pct(ce.LABOR_PCT)} dos materiais, no mínimo {_rs(ce.MAO_DE_OBRA_MINIMA)} |",
        "| linha de tratamento e descarte | dimensiona a linha pela classe de qualidade, pelo método de desinfecção e pela área do telhado; "
        "soma ao CAPEX só o que excede a verba genérica de filtragem dos acessórios digitados "
        "| `size_etap`, `capex_incremental_da_etap` "
        f"| verba genérica de {_rs(ce.verba_generica_de_tratamento_brl())} |",
        "| tubulação e acessórios sem arranjo | estimativa por percentual do preço dos reservatórios, com piso, quando o arranjo não é a fonte "
        "| `piping_percentage_fallback`, `accessories_percentage` "
        f"| tubulação: {_pct(ce.PIPING_PCT)}, piso de {_rs(pisos['piping'])}; acessórios: {_pct(ce.ACCESSORIES_PCT)}, piso de {_rs(pisos['accessories'])} |",
        "| fator regional | multiplica o total do estimador preliminar; **não entra** no investimento do projeto, porque a interface e a linha de comando usam as parcelas, e não o total "
        "| `regional_factors_by_uf` "
        f"| {len(fatores)} UFs, de {br(min(fatores), 2)} a {br(max(fatores), 2)} |",
    ])


def tabela_capex_reservatorios():
    """Preço de reservatório por volume e por material, lido da tabela e do multiplicador."""
    from triton.core import cost_estimates as ce

    materiais = (("PEAD", "polietileno (tabela)"), ("FIBRA", "fibra de vidro"),
                 ("CONCRETO", "concreto armado"), ("ACO_INOX", "aço inoxidável"))
    volumes = sorted({v for v, _ in ce.LOWER_TANK_PRICE_TABLE} | {VOLUME})
    limite_caixa = max(v for v, _ in ce.UPPER_TANK_PRICE_TABLE)
    tabelados = {v for v, _ in ce.LOWER_TANK_PRICE_TABLE}
    L = ["| Volume | " + " | ".join(r for _, r in materiais) + " | Também na tabela da caixa |",
         "| ---: | " + " | ".join("---:" for _ in materiais) + " | :---: |",
         "| fator do material | " + " | ".join(br(ce.MATERIAL_COST_MULTIPLIERS[m], 2) for m, _ in materiais) + " | |"]
    for v in volumes:
        nota = "" if v in tabelados else " (interpolado)"
        celulas = [_rs(ce.estimate_tank_price(v, m, ce.LOWER_TANK_PRICE_TABLE)) for m, _ in materiais]
        L.append(f"| {vol_br(v)}{nota} | " + " | ".join(celulas) + f" | {'sim' if v <= limite_caixa else '—'} |")
    return NL.join(L)


def tabela_capex_tubos():
    """Preço por metro de cada diâmetro, sem e com os 25% de conexões do orçamento por comprimento."""
    from triton.core import cost_estimates as ce

    L = ["| Diâmetro | Polegadas | Tipo | Preço por metro | Com 25% de conexões |",
         "| :--- | :--- | :--- | ---: | ---: |"]
    for p in ce.COMMERCIAL_PIPES_CAPEX:
        dn = p["dn"]
        L.append(f"| DN {dn} | {p['pol']} | {p['category'].replace('soldavel', 'soldável')} | {_rs(ce.PIPE_COST_PER_METER[dn])} "
                 f"| {_rs(ce.compute_pipe_item_cost(dn, 1.0, include_fittings=True))} |")
    return NL.join(L)


def tabela_capex_pecas():
    """As peças do arranjo 3D que o programa orça sozinho, com preço e regra de escala."""
    from triton.core.quantitativo_do_arranjo import CABO, CATALOGO_DE_PECAS, CONEXAO, CURVA, TE, _DN_REFERENCIA

    L = ["| Peça | Preço de referência | Muda com o diâmetro | Onde entra no CAPEX |",
         "| :--- | ---: | :---: | :--- |"]
    for tipo, p in CATALOGO_DE_PECAS.items():
        destino = ("linha de tratamento, quando a ETAP está ligada; senão, acessórios"
                   if tipo in ("filtro_pluvial", "first_flush") else "acessórios")
        L.append(f"| {p.nome} | {_rs(p.preco_brl)} | {'sim' if p.escala_pelo_dn else 'não'} | {destino} |")
    for p, un in ((CURVA, ""), (CONEXAO, ""), (TE, ""), (CABO, " por metro")):
        L.append(f"| {p.nome} | {_rs(p.preco_brl)}{un} | {'sim' if p.escala_pelo_dn else 'não'} "
                 f"| {'tubulação' if p is not CABO else 'acessórios'} |")
    L += ["", f"Os preços das peças que mudam com o diâmetro valem para o DN {br(_DN_REFERENCIA, 0)}."]
    return NL.join(L)


def tabela_capex_bombas():
    """Motobombas: preço do assistente de dimensionamento e preço da fórmula do estimador."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from triton.core import cost_estimates as ce
    from triton.ui.dialogs.pump_wizard_dialog import PUMP_CATALOG

    L = ["| Modelo do assistente | Potência | Vazão nominal | Altura máxima | Preço do assistente | Preço pela fórmula |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for m in PUMP_CATALOG:
        formula = ce.estimate_preliminary_capex(5000.0, 500.0, True, m["kw"], 1)["pump_unit"]
        L.append(f"| {m['brand']}, {br(m['cv'], 2)} CV | {br(m['kw'], 3)} kW | {br(m['flow_lh'], 0)} L/h "
                 f"| {br(m['max_h'], 0)} m.c.a. | {_rs(m['cost'])} | {_rs(formula)} |")
    p = ce.PUMP_PARAMS
    L += ["", f"A fórmula é o maior entre {_rs(p['min_cost'])} e "
              f"{_rs(p['base_cost'])} × (P ÷ {br(p['base_power_kw'], 5)} kW)^{br(p['power_exponent'], 2)}."]
    return NL.join(L)


def tabela_capex_etap():
    """Preços da linha de tratamento e do descarte, obtidos pelo dimensionamento."""
    from triton.core.water_quality import ENERGY_PRICE_BRL_PER_KWH, size_etap, size_first_flush_system

    cloro = size_etap(roof_area_m2=150.0, annual_pluvial_consumed_m3=120.0)
    L = ["| Componente | Condição | Investimento | Custeio anual |",
         "| :--- | :--- | ---: | ---: |"]
    for area in (150.0, 300.0, 600.0):
        r = size_etap(roof_area_m2=area, annual_pluvial_consumed_m3=120.0)
        L.append(f"| filtro de entrada | {r.pre_filter_type}; telhado de {br(area, 0)} m² | {_rs(r.pre_filter_capex)} | — |")
    L.append(f"| dosador de cloração | sempre que a ETAP está ligada | {_rs(cloro.disinfection_capex)} | o do cloro, à parte |")
    for m3 in (120.0, 300.0):
        r = size_etap(roof_area_m2=150.0, annual_pluvial_consumed_m3=m3, disinfection_choice="uv")
        L.append(f"| reator ultravioleta, {br(r.uv_power_watts, 0)} W | estágio adicional; {br(m3, 0)} m³/ano de água de chuva "
                 f"| {_rs(r.disinfection_capex - cloro.disinfection_capex)} "
                 f"| {_rs(r.disinfection_opex_yr - r.annual_chlorine_cost_brl)} |")
    r = size_etap(roof_area_m2=150.0, annual_pluvial_consumed_m3=120.0, disinfection_choice="ozonio")
    L.append(f"| ozonizador | estágio adicional | {_rs(r.disinfection_capex - cloro.disinfection_capex)} "
             f"| {_rs(r.disinfection_opex_yr - r.annual_chlorine_cost_brl)} |")
    for classe, rotulo in (("classe_1", "classes 1 a 3: areia multicamada ou cartucho"), ("classe_4", "classe 4: carvão ativado")):
        r = size_etap(target_class_id=classe, roof_area_m2=150.0, annual_pluvial_consumed_m3=120.0, include_polishing_filter=True)
        L.append(f"| filtro de polimento | {rotulo} | {_rs(r.polishing_capex)} | {_rs(r.polishing_annual_opex)} |")
    for area, mm in ((100.0, 2.0), (150.0, 2.0)):
        d = size_first_flush_system(discard_mm=mm, roof_area_m2=area)
        L.append(f"| descarte inicial | {br(mm, 0)} mm sobre {br(area, 0)} m²: reservatório de {br(d.diverter_volume_liters, 0)} L e separador de folhas "
                 f"| {_rs(d.first_flush_total_capex)} | {_rs(d.first_flush_annual_opex)} |")
    L += ["", f"A energia do reator ultravioleta é paga a {_rs(ENERGY_PRICE_BRL_PER_KWH)} por kWh, valor fixo do módulo de qualidade."]
    return NL.join(L)


def tabela_capex_tipologias():
    """As cinco tipologias: subsistemas calibrados e o orçamento calibrado de referência."""
    from triton.core import cost_estimates as ce

    L = ["| Tipologia | Motobombas | Painel elétrico | Sensores e automação | Filtragem | Air gap | Tubulação base | Manutenção anual | Mão de obra mínima |",
         "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for cod, c in ce.TYPOLOGY_COST_CONFIGS.items():
        L.append(f"| {cod}: {c['name']} | {c['pump_count']} × {_rs(c['pump_unit_cost'])} | {_rs(c['electrical_panel_cost'], 0)} "
                 f"| {_rs(c['sensors_automation_cost'], 0)} | {_rs(c['treatment_filtration_cost'], 0)} | {_rs(c['air_gap_supplement_cost'], 0)} "
                 f"| {_rs(c['pipes_base_cost'], 0)} | {_rs(c['maint_base_annual'], 0)} | {_rs(c['min_labor_cost'], 0)} |")
    L += ["", f"| Orçamento calibrado, cisterna de {vol_br(5000)} em polietileno, SP | Cisterna | Caixa | Motobombas | Tubulação | Acessórios | Mão de obra | Total |",
          "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for cod in ce.TYPOLOGY_COST_CONFIGS:
        r = ce.estimate_calibrated_capex_opex(typology=cod, volume_l=5000.0, uf="SP")
        L.append(f"| {cod} | {_rs(r['c_inf'], 0)} | {_rs(r['c_sup'], 0)} | {_rs(r['c_pump'], 0)} | {_rs(r['c_pipes'], 0)} "
                 f"| {_rs(r['c_accessories_total'], 0)} | {_rs(r['labor_cost'], 0)} | {_rs(r['capex_total_brl'], 0)} |")
    return NL.join(L)


def tabela_capex_regional():
    """Os 27 fatores regionais, em três colunas de pares."""
    from triton.core import cost_estimates as ce

    itens = sorted(ce.REGIONAL_FACTORS_BY_UF.items())
    linhas = ["| UF | Fator | UF | Fator | UF | Fator |", "| :--- | ---: | :--- | ---: | :--- | ---: |"]
    por_linha = 3
    n_linhas = -(-len(itens) // por_linha)
    for i in range(n_linhas):
        celulas = []
        for j in range(por_linha):
            k = i + j * n_linhas
            celulas += [itens[k][0], br(itens[k][1], 2)] if k < len(itens) else ["", ""]
        linhas.append("| " + " | ".join(celulas) + " |")
    return NL.join(linhas)


def tabela_capex_procedencia():
    """O que a base registra sobre a origem e a data dos próprios números."""
    from triton.core import cost_estimates as ce

    db = ce.load_costs_database()
    meta, proc = db["_metadata"], db["_procedencia_precos_reservatorio"]
    return NL.join([
        "| Registro na base de custos | Conteúdo |",
        "| :--- | :--- |",
        f"| atualização da base (`updated_at`) | {_data_iso(meta['updated_at'])} |",
        f"| fontes declaradas (`source_references`) | {meta['source_references']} |",
        f"| moeda | {meta['currency']} |",
        f"| preços de reservatório: fabricante | {proc['fabricante']} |",
        f"| preços de reservatório: varejista | {proc['varejista']} |",
        f"| preços de reservatório: coletados em | {_data_iso(proc['coletado_em'])} |",
        "| preços de reservatório: critério | menor preço anunciado por capacidade, uma única marca e um único varejista, no mesmo dia |",
        f"| preços de reservatório: alcance | {vol_br(ce.LOWER_TANK_PRICE_TABLE[0][0])} a {vol_br(ce.LOWER_TANK_PRICE_TABLE[-1][0])} |",
    ])


def tabela_opex_itens():
    """O que entra sozinho no custeio de um projeto novo: valor, periodicidade, origem e como mudar."""
    from triton.core.chlorination import Cloracao
    from triton.core.edition import projeto_novo_da_edicao
    from triton.core.water_quality import size_first_flush_system

    cfg = projeto_novo_da_edicao()
    cl = Cloracao(dose_mg_por_litro=cfg.chlorine_dose_mg_l, pureza=cfg.chlorine_product_purity)
    descarte = size_first_flush_system(discard_mm=2.0, roof_area_m2=150.0)
    L = ["| Item | Valor padrão | Periodicidade | Origem | Como alterar ou desligar |",
         "| :--- | :--- | :--- | :--- | :--- |"]
    for nome, meses, fixo, var in cfg.op_costs:
        L.append(f"| {nome} | {_rs(fixo)} por evento | a cada {meses} meses | padrão do projeto novo; os mesmos três valores estão em `default_maintenance_items` | "
                 "botão «3. Outros Custos Operacionais»: editar, excluir ou acrescentar |")
    L.append(f"| cloração | {br(cfg.chlorine_dose_mg_l, 1)} mg/L de cloro ativo, pastilha a {_pct(cfg.chlorine_product_purity)}, "
             f"{_rs(cfg.chlorine_cost_per_kg)} por kg de produto: {br(cl.produto_kg_por_m3, 5)} kg e "
             f"{_rs(cl.produto_kg_por_m3 * cfg.chlorine_cost_per_kg, 4)} por m³ | contínua, proporcional ao volume pluvial aproveitado "
             "| `Cloracao` (`chlorination.py`) e `chlorine_cost_per_kg` | dose e desinfetante na etapa «3. Qualidade & ETAP»; o preço do quilograma só pelo arquivo do projeto |")
    L.append(f"| descarte inicial | {_rs(descarte.first_flush_annual_opex)} por ano (reservatório de descarte e separador de folhas) "
             "| anual | `size_first_flush_system` | caixa do descarte físico na etapa «3. Qualidade & ETAP» |")
    L.append(f"| energia da motobomba | {_rs(cfg.elec_tariff, 4)} por kWh, bandeira verde, impostos de {br(cfg.elec_tax_var, 0)}% "
             "| contínua, proporcional à energia anual da motobomba "
             "| tarifa B1 residencial do município na base ANEEL, ou o padrão do projeto | botão «2. Motobomba e Custo de Energia»: cidade, tarifa, impostos; bandeira na etapa econômica |")
    L.append(f"| IPTU Verde | {'ligado' if cfg.iptu_green_enabled else 'desligado'} | anual | opção do município na base de tarifas | caixa na etapa econômica |")
    return NL.join(L)


def tabela_opex_energia():
    """A tarifa de energia: a base de 652 municípios e as bandeiras, lidas dos dados e do motor."""
    import json
    import statistics

    from triton.core.economic import run_economic_analysis
    from triton.core.parser import TritonConfig
    from triton.core.pump_energy import compute_annual_pump_energy

    caminho = os.path.join(os.path.dirname(AQUI), "triton", "data", "brazil_cities_tariffs.json")
    with open(caminho, encoding="utf-8") as f:
        base = json.load(f)
    cidades = base["cities"].values()
    valores = [c["energia_r_kwh"] for c in cidades if c.get("energia_r_kwh", 0) > 0]
    expirados = sum(1 for c in cidades if c.get("status_energia") == "EXPIRED_ANEEL_REF")
    distribuidoras = {c.get("distribuidora_energia") for c in cidades}
    padrao = TritonConfig().elec_tariff

    # Os acréscimos das bandeiras não são constantes importáveis: saem do motor, pela diferença do custeio.
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    acrescimo = {}
    for bandeira in ("verde", "amarela", "vermelha_1", "vermelha_2", "branca"):
        cfg = _config_economica(VOLUME, "CONCRETO")
        cfg.tariff_flag = bandeira
        acrescimo[bandeira] = (run_economic_analysis(cfg, r).annual_opex_brl,
                               compute_annual_pump_energy(cfg, r).annual_kwh)
    base_opex, kwh = acrescimo["verde"]
    ad = {b: (v[0] - base_opex) / v[1] for b, v in acrescimo.items()}

    return NL.join([
        "| A tarifa de energia da base | Valor |",
        "| :--- | ---: |",
        f"| municípios com tarifa de energia | {len(valores)} |",
        f"| distribuidoras | {len(distribuidoras)} |",
        f"| menor tarifa | {_rs(min(valores), 4)}/kWh |",
        f"| mediana | {_rs(statistics.median(valores), 4)}/kWh |",
        f"| maior tarifa | {_rs(max(valores), 4)}/kWh |",
        f"| municípios cuja tarifa vem de um ato já expirado | {expirados} |",
        f"| valor padrão do projeto novo | {_rs(padrao, 4)}/kWh |",
        "",
        "| Bandeira tarifária | Acréscimo sobre a tarifa |",
        "| :--- | ---: |",
        f"| verde | {_rs(ad['verde'], 5)}/kWh |",
        f"| amarela | {_rs(ad['amarela'], 5)}/kWh |",
        f"| vermelha, patamar 1 | {_rs(ad['vermelha_1'], 5)}/kWh |",
        f"| vermelha, patamar 2 | {_rs(ad['vermelha_2'], 5)}/kWh |",
        f"| branca | desconto de {_pct(-ad['branca'] / padrao_tarifa_tutorial(), 0)} da tarifa, fora de ponta |",
    ])


def padrao_tarifa_tutorial():
    """Tarifa de energia da configuração econômica do tutorial (a mesma usada na tabela das bandeiras)."""
    return _config_economica(VOLUME, "CONCRETO").elec_tariff


def tabela_opex_premissas():
    """As premissas de projeção: padrão do projeto novo, valor do tutorial e perfis de referência."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from triton.core.edition import projeto_novo_da_edicao
    from triton.ui.tab_tanks_simulation import TabTanksSimulation as Tab

    novo = projeto_novo_da_edicao()
    tut = _config_economica(VOLUME, "CONCRETO")

    def anual(mensal_pct):
        return ((1 + mensal_pct / 100.0) ** 12 - 1) * 100.0

    L = ["| Premissa | Padrão do projeto novo | Valor do tutorial |",
         "| :--- | ---: | ---: |",
         f"| taxa mínima de atratividade | {br(novo.tma, 2)}% ao mês ({br(anual(novo.tma), 1)}% ao ano) | {br(tut.tma, 2)}% ao mês |",
         f"| inflação dos custos | {br(novo.inflation, 2)}% ao mês ({br(anual(novo.inflation), 1)}% ao ano) | {br(tut.inflation, 2)}% ao mês |",
         f"| reajuste da tarifa de água | {br(novo.water_tariff_escalation, 1)}% ao ano | {br(tut.water_tariff_escalation, 1)}% ao ano |",
         f"| reajuste da tarifa de esgoto | {br(novo.sewage_tariff_escalation, 1)}% ao ano | {br(tut.sewage_tariff_escalation, 1)}% ao ano |",
         f"| reajuste da tarifa de energia | {br(novo.elec_tariff_escalation, 1)}% ao ano | {br(tut.elec_tariff_escalation, 1)}% ao ano |",
         f"| intervalo de reajuste | {br(novo.tariff_escalation, 0)} meses | {br(tut.tariff_escalation, 0)} meses |",
         f"| período de análise | {novo.analysis_period_years} anos | {tut.analysis_period_years} anos |",
         "",
         "| Perfis de referência da etapa 4 | Taxa |",
         "| :--- | ---: |"]
    for rotulo, dado in Tab._perfis_de_inflacao(None):
        if dado.get("annual_rate") is not None:
            L.append(f"| inflação: {rotulo.split(' — ')[0].replace('Referência ', '')} | {br(dado['annual_rate'], 1)}% ao ano |")
    for rotulo, taxa in Tab._perfis_de_tma(None):
        if taxa is not None:
            curto = rotulo.split(' — ')[0].replace('Referência ', '')
            L.append(f"| taxa mínima de atratividade: {curto[0].lower() + curto[1:]} | {br(taxa, 1)}% ao ano |")
    for rotulo, valores in Tab._perfis_de_reajuste(None):
        if valores is not None:
            _, agua, energia = valores
            L.append(f"| reajuste: {rotulo.split(' — ')[0].replace('projecao', 'projeção')} | água e esgoto {br(agua, 1)}%; energia {br(energia, 1)}% ao ano |")
    return NL.join(L)


def tabela_opex_peso():
    """O peso das rotinas de manutenção de partida no resultado do tutorial."""
    from triton.core.economic import run_economic_analysis

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    com = _config_economica(VOLUME, "CONCRETO")
    sem = _config_economica(VOLUME, "CONCRETO")
    sem.op_costs = []
    ec, es = run_economic_analysis(com, r), run_economic_analysis(sem, r)
    por_ano = sum(fixo * 12.0 / meses for _, meses, fixo, _ in com.op_costs)
    return NL.join([
        "| Projeto do tutorial | Com as rotinas de partida | Sem rotinas |",
        "| :--- | ---: | ---: |",
        f"| rotinas de manutenção por ano | {_rs(por_ano)} | {_rs(0.0)} |",
        f"| custeio anual do resumo: energia, cloro e linha de tratamento | {_rs(ec.annual_opex_brl)} | {_rs(es.annual_opex_brl)} |",
        f"| valor presente líquido | {_rs(ec.vpl)} | {_rs(es.vpl)} |",
        f"| payback descontado | {br(ec.payback_years, 1)} anos | {br(es.payback_years, 1)} anos |",
    ])


def tabela_capex_constantes():
    """Constantes do código que não têm registro de fonte na base: o valor e onde estão."""
    from triton.core import cost_estimates as ce
    from triton.core.water_quality import ENERGY_PRICE_BRL_PER_KWH

    cal = ce.estimate_calibrated_capex_opex(typology="UTI", volume_l=5000.0, uf="SP", energy_tariff_kwh=1.0)
    fator_conexoes = ce.compute_pipe_item_cost(32, 1.0, include_fittings=True) / ce.compute_pipe_item_cost(32, 1.0, include_fittings=False)
    pisos = ce.estimate_preliminary_capex(100.0, 0.0, False)
    L = ["| Constante | Valor | Onde está | Fonte registrada |",
         "| :--- | ---: | :--- | :---: |",
         f"| consumo específico de recalque do orçamento calibrado | {br(cal['opex_energy_per_m3_brl'], 2)} kWh/m³ | `estimate_calibrated_capex_opex` | não |",
         f"| custo de cloração do orçamento calibrado | {_rs(cal['opex_chlorine_per_m3_brl'], 2)}/m³ | `estimate_calibrated_capex_opex` | não |",
         f"| mão de obra | {_pct(ce.LABOR_PCT)} dos materiais | `labor_percentage` | não |",
         f"| acessórios sem arranjo | {_pct(ce.ACCESSORIES_PCT)} dos reservatórios | `accessories_percentage` | não |",
         f"| tubulação sem arranjo | {_pct(ce.PIPING_PCT)} da cisterna | `piping_percentage_fallback` | não |",
         f"| conexões sobre o tubo, no orçamento por comprimento | {_pct(fator_conexoes - 1.0)} | `compute_pipe_item_cost` | não |",
         f"| volume da caixa no orçamento calibrado | {_pct(cal['volume_sup_l'] / cal['volume_l'])} da cisterna | `estimate_calibrated_capex_opex` | não |",
         f"| pisos da tubulação, dos acessórios e da mão de obra | {_rs(pisos['piping'], 0)}, {_rs(pisos['accessories'], 0)} e {_rs(pisos['labor'], 0)} | `estimate_preliminary_capex` | não |",
         f"| preço da energia do reator ultravioleta | {_rs(ENERGY_PRICE_BRL_PER_KWH)}/kWh | `water_quality.py` | não |",
         "| preços da linha de tratamento e do descarte | tabela anterior | `water_quality.py` | não |",
         "| multiplicadores de material | " + ", ".join(br(ce.MATERIAL_COST_MULTIPLIERS[m], 2) for m in ("FIBRA", "CONCRETO", "ACO_INOX"))
         + " | `material_multipliers` | não |"]
    return NL.join(L)


def tabela_capex_exemplo():
    """O projeto do tutorial, com o CAPEX digitado e com o CAPEX que o programa calcularia sozinho."""
    from triton.core.economic import run_economic_analysis
    from triton.core.etap_integration import capex_incremental_da_etap
    from triton.core.quantitativo_do_arranjo import sincronizar_com_o_arranjo

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    digitado = _config_economica(VOLUME, "CONCRETO")
    auto = _config_economica(VOLUME, "CONCRETO")
    auto.capex_do_arranjo = True
    auto.mao_de_obra_automatica = True
    auto.cost_piping = auto.cost_accessories = auto.cost_labor = 0.0
    auto.econ_lower_tank_vol = VOLUME
    sincronizar_com_o_arranjo(auto)

    def linhas(cfg):
        bombas = cfg.pump_unit_cost * cfg.pump_count
        etap = capex_incremental_da_etap(cfg, sim_result=r)
        return [cfg.cost_lower_tank, cfg.cost_upper_tank, bombas, cfg.cost_labor, cfg.cost_piping,
                cfg.cost_accessories, etap]

    a, b = linhas(digitado), linhas(auto)
    rotulos = ("cisterna de concreto de 4.000 L", "caixa superior de 1.000 L em polietileno", "duas motobombas",
               "mão de obra", "tubulação", "acessórios", "linha de tratamento e descarte (incremento)")
    L = ["| Rubrica | Digitado no tutorial | Calculado sozinho |", "| :--- | ---: | ---: |"]
    for rot, x, y in zip(rotulos, a, b):
        L.append(f"| {rot} | {_rs(x)} | {_rs(y)} |")
    L.append(f"| **investimento total** | **{_rs(run_economic_analysis(digitado, r).capex_total)}** "
             f"| **{_rs(run_economic_analysis(auto, r).capex_total)}** |")
    return NL.join(L)


def com_legenda(nome, conteudo):
    """Põe a legenda declarada acima de cada tabela do arquivo, na ordem."""
    fila = list(LEGENDAS.get(nome) or [])
    if not fila:
        return conteudo
    saida, anterior = [], ""
    for linha in conteudo.split(NL):
        if (linha.startswith("|") and not anterior.startswith("|")
                and not anterior.startswith("<!-- tabela:") and fila):
            saida.append("<!-- tabela: " + fila.pop(0) + " -->")
        saida.append(linha)
        anterior = linha
    return NL.join(saida)


#: As tabelas da seção 10 sobre o CAPEX calculado sozinho e o custeio inserido sozinho.
TABELAS_DE_CUSTOS = (
    ("cap10_capex_cadeia.md", tabela_capex_cadeia),
    ("cap10_capex_reservatorios.md", tabela_capex_reservatorios),
    ("cap10_capex_tubos.md", tabela_capex_tubos),
    ("cap10_capex_pecas.md", tabela_capex_pecas),
    ("cap10_capex_bombas.md", tabela_capex_bombas),
    ("cap10_capex_etap.md", tabela_capex_etap),
    ("cap10_capex_tipologias.md", tabela_capex_tipologias),
    ("cap10_capex_regional.md", tabela_capex_regional),
    ("cap10_capex_procedencia.md", tabela_capex_procedencia),
    ("cap10_capex_constantes.md", tabela_capex_constantes),
    ("cap10_capex_exemplo.md", tabela_capex_exemplo),
    ("cap10_opex_itens.md", tabela_opex_itens),
    ("cap10_opex_energia.md", tabela_opex_energia),
    ("cap10_opex_premissas.md", tabela_opex_premissas),
    ("cap10_opex_peso.md", tabela_opex_peso),
)


def main_custos():
    """Gera só as tabelas de custos da seção 10 (`python manual/gerar_tabelas.py custos`)."""
    os.environ["TRITON_EDITION"] = "BRL"
    for nome, fn in TABELAS_DE_CUSTOS:
        caminho = os.path.join(SAIDA, nome)
        gravar(caminho, com_legenda(os.path.basename(caminho), fn()) + NL)
        print(f"  {os.path.relpath(caminho, AQUI)}")


def main():
    tabela, r = tabela_dez_dias()

    caminho = os.path.join(SAIDA, "cap23_entrada.md")
    gravar(caminho, com_legenda(os.path.basename(caminho), entrada_dez_dias()) + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    caminho = os.path.join(SAIDA, "cap23_dez_dias.md")
    gravar(caminho, com_legenda(os.path.basename(caminho), tabela) + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    print(f"  potencial dos dez dias: {r.potential_potable_savings_pct:.2f}%")

    # ── tabelas do tutorial ──
    for nome, conteudo in (
        ("cap04_serie.md", tabela_serie()),
    ):
        caminho = os.path.join(SAIDA, nome)
        gravar(caminho, com_legenda(os.path.basename(caminho), conteudo) + NL)
        print(f"  {os.path.relpath(caminho, AQUI)}")

    tabela_p, r6 = tabela_primeira_simulacao()
    caminho = os.path.join(SAIDA, "cap06_primeira_simulacao.md")
    gravar(caminho, com_legenda(os.path.basename(caminho), tabela_p) + NL)
    print(f"  {os.path.relpath(caminho, AQUI)} — {r6.potential_potable_savings_pct:.2f}%")

    tabela_v, dados = tabela_varredura()
    caminho = os.path.join(SAIDA, "cap07_varredura.md")
    gravar(caminho, com_legenda(os.path.basename(caminho), tabela_v) + NL)
    print(f"  {os.path.relpath(caminho, AQUI)} — {len(dados)} volumes")

    caminho = os.path.join(SAIDA, "cap07_limiar_e_custo.md")
    gravar(caminho, com_legenda(os.path.basename(caminho), tabela_limiar_e_custo()) + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    for nome, fn in (
        ("cap08_reservatorio_superior.md", tabela_reservatorio_superior),
        ("cap08_limiar.md", tabela_limiar_de_acionamento),
        ("cap09_etap.md", tabela_etap),
        ("cap10_economico.md", tabela_economica),
        ("cap11_materiais.md", tabela_materiais),
        ("cap12_multicriterio.md", tabela_multicriterio),
        ("cap12_pesos.md", tabela_pesos),
        ("cap28_pressurizadores.md", lambda: tabela_pressurizadores()[0]),
        ("cap20_sensibilidade.md", tabela_sensibilidade),
        ("cap32_decisao.md", tabela_decisao),
        ("cap14_cidades.md", tabela_cidades),
        ("cap24_metodos.md", tabela_metodos_empiricos),
        ("cap30_inventario.md", tabela_inventario),
    ):
        caminho = os.path.join(SAIDA, nome)
        gravar(caminho, com_legenda(os.path.basename(caminho), fn()) + NL)
        print(f"  {os.path.relpath(caminho, AQUI)}")

    main_custos()

    return r


if __name__ == "__main__":
    if "custos" in sys.argv[1:]:
        print("tabelas de custos do manual:")
        main_custos()
    else:
        print("tabelas do manual:")
        main()
