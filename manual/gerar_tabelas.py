# -*- coding: utf-8 -*-
"""Gera as tabelas numéricas dos capítulos, rodando o próprio programa.

Nenhum número do manual sai da cabeça de quem escreve. As tabelas deste arquivo
são produzidas executando o Netuno com os dados de entrada declarados, de modo que
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

from netuno.core.simulation import run_single_simulation  # noqa: E402

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
    "rainwater_share": 0.40,   # bacias, máquina de lavar e área externa
    "volume_inicial": 3000.0,  # o primeiro palpite, do capítulo 6
    # A partir da seção do reservatório superior, o projeto adota recalque para
    # caixa elevada: é a comparação daquela seção, com o limiar de 100 L.
    "caixa_superior_l": 1000.0,
    "limiar_recalque_l": 100.0,
}

VOLUMES_VARREDURA = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000,
                     10000, 12000, 16000, 20000]


def _serie():
    from netuno.core.parser import load_precipitation
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
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.simulation import run_sweep_simulation

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
        "| | 5.000 L | 20.000 L |",
        "| :--- | ---: | ---: |",
    ]
    vals = {}
    for v in (5000, 20000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg)
        preco = estimate_tank_price(float(v), "CONCRETO")
        amb = _config_ambiental()
        amb.lower_material_key = "CONCRETO"
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        vals[v] = (r.potential_potable_savings_pct, preco,
                   lca.lower_tank_mass_kg, lca.total_embodied_co2_kg)
    a, b = vals[5000], vals[20000]
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
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.parser import NetunoConfig
    cfg = NetunoConfig()
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
    from netuno.core.environmental import EnvironmentalConfig
    from netuno.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.roof_area_m2 = TUTORIAL["area"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.first_flush_system_enabled = True
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = True
    cfg.upper_tank_vol_liters = TUTORIAL["caixa_superior_l"]
    if sim is not None:
        cfg.annual_pump_kwh = compute_annual_pump_energy(_config_economica(5000.0), sim).annual_kwh
    return cfg


def tabela_reservatorio_superior():
    """Capítulo 8: a comparação justa, com o mesmo armazenamento total."""
    from netuno.core.parser import NetunoConfig
    from netuno.core.pump_energy import compute_annual_pump_energy

    serie = _serie()
    cfg = _config_tutorial()
    unico = run_single_simulation(precip_data=serie, lower_tank_vol=6000.0, **cfg)
    duplo = run_single_simulation(
        precip_data=serie, lower_tank_vol=5000.0, upper_tank_vol=1000.0,
        upper_tank_used=True, pumping_threshold=100.0, **cfg)

    bomba = NetunoConfig()
    bomba.upper_tank_used = True
    bomba.pump_power_kw, bomba.pump_efficiency, bomba.pump_flow_rate = 0.37, 0.0, 0.0
    bomba.pump_manometric_head_m, bomba.pump_startup_time_h = 12.0, 0.03
    e = compute_annual_pump_energy(bomba, duplo)
    anos = duplo.total_days / 365.25

    L = [
        "| Mesmo armazenamento de 6.000 L | Um tanque só | 5.000 embaixo + 1.000 em cima |",
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
            precip_data=serie, lower_tank_vol=5000.0, upper_tank_vol=1000.0,
            upper_tank_used=True, pumping_threshold=float(lim), **cfg)
        anos = r.total_days / 365.25
        L.append(f"| {br(lim, 0)} L | {br(r.potential_potable_savings_pct, 2)}% "
                 f"| {br(r.total_pump_cycles / anos, 0)} |")
    return NL.join(L)


def tabela_etap():
    """Capítulo 9: a classe recomenda, o projetista decide."""
    from netuno.core.water_quality import WATER_QUALITY_CLASSES, size_etap

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0,
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
    from netuno.core.economic import calculate_water_bill, run_economic_analysis

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0,
                              **_config_projeto())
    dias_mes = 30.4375
    tot_m3 = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * dias_mes / 1000.0
    pot_m3 = r.avg_potable_consumed_l_day * dias_mes / 1000.0
    sem = calculate_water_bill(tot_m3 * 1000, TARIFA_CASAN, 1, 100.0, 0.0, 0.0)
    com = calculate_water_bill(pot_m3 * 1000, TARIFA_CASAN, 1, 100.0, 0.0, 0.0)

    cfg = _config_economica(5000.0, "CONCRETO")
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
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.environmental import MATERIAL_PRESETS, EnvironmentalConfig, calculate_lca

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3
    L = ["| Material da cisterna | Massa | Carbono incorporado | Payback de carbono "
         "| Saldo em 20 anos | Preço |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    nomes = {"PEAD": "Polietileno (PEAD)", "CONCRETO": "Concreto armado",
             "FIBRA": "Fibra de vidro", "ACO_INOX": "Aço inoxidável"}
    for k in MATERIAL_PRESETS:
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        l = calculate_lca(5000.0, m3, cfg)
        try:
            preco = f"R$ {br(estimate_tank_price(5000.0, k), 0)}"
        except Exception:
            preco = "—"
        L.append(f"| {nomes.get(k, k)} | {br(l.lower_tank_mass_kg, 0)} kg "
                 f"| {br(l.total_embodied_co2_kg, 0)} kg CO₂e "
                 f"| {br(l.environmental_payback_years, 1)} anos "
                 f"| {br(l.lifetime_net_co2_saved_kg, 0)} kg | {preco} |")

    L += ["", "| Volume em concreto | Payback de carbono | Saldo em 20 anos |",
          "| ---: | ---: | ---: |"]
    for v in (2000, 3000, 5000, 8000):
        rr = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                   **_config_projeto())
        cfg = _config_ambiental(rr)
        cfg.lower_material_key = "CONCRETO"
        l = calculate_lca(float(v), rr.annual_pluvial_consumed_m3, cfg)
        L.append(f"| {br(v, 0)} L | {br(l.environmental_payback_years, 1)} anos "
                 f"| {br(l.lifetime_net_co2_saved_kg, 0)} kg CO₂e |")
    return NL.join(L)


def tabela_multicriterio():
    """Capítulo 12: três critérios, três respostas."""
    from netuno.core.economic import run_economic_analysis
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.topsis import TopsisCandidate, calculate_topsis_scores

    serie = _serie()
    cfg_sim = _config_projeto()
    cands, linhas = [], [
        "| Volume | Potencial | VPL | Payback | Saldo de carbono em 20 anos | Investimento |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for v in (1000, 2000, 3000, 5000, 8000, 12000):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg_sim)
        e = run_economic_analysis(_config_economica(v, "PEAD"), r)
        amb = _config_ambiental(r)
        amb.lower_material_key = "PEAD"
        l = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        linhas.append(
            f"| {br(v, 0)} L | {br(r.potential_potable_savings_pct, 2)}% "
            f"| R$ {br(e.vpl, 0)} | {br(e.payback_years or 0.0, 1)} anos "
            f"| {br(l.lifetime_net_co2_saved_kg, 0)} kg | R$ {br(e.capex_total, 0)} |")
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v), water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=l.lifetime_net_co2_saved_kg,
            capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct,
            overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years,
            irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))

    res = calculate_topsis_scores(cands)
    linhas += [
        "",
        "| Critério isolado | Volume que vence |",
        "| :--- | ---: |",
        f"| maior potencial de economia | {br(cands[res.technical_best_index].lower_tank_vol, 0)} L |",
        f"| menor payback descontado, desempate pelo VPL | {br(cands[res.financial_best_index].lower_tank_vol, 0)} L |",
        f"| maior saldo de carbono | {br(cands[res.environmental_best_index].lower_tank_vol, 0)} L |",
        f"| **compromisso, pesos iguais** | **{br(cands[res.best_index].lower_tank_vol, 0)} L** |",
    ]
    return NL.join(linhas)


CIDADES_GUIA14 = ("Florianopolis1", "SaoPaulo1", "Brasilia1", "Manaus1")
NOMES_CIDADES = {
    "Florianopolis1": "Florianópolis", "SaoPaulo1": "São Paulo",
    "Brasilia1": "Brasília", "Manaus1": "Manaus",
}


def tabela_cidades():
    """Guia 14: o regime de chuva manda mais que a lâmina anual."""
    from datetime import datetime, timedelta

    import numpy as np

    from netuno.core.parser import load_precipitation
    from netuno.core.simulation import run_sweep_simulation

    cfg = _config_tutorial()
    L = ["| Cidade | Chuva anual | Dias com chuva | Razão entre o mês mais e o menos "
         "chuvoso | Potencial com 5.000 L | Volume ideal |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for chave in CIDADES_GUIA14:
        caminho = os.path.join(os.path.dirname(AQUI), "data", "rainfall", chave + ".csv")
        if not os.path.exists(caminho):
            continue
        serie = load_precipitation(caminho)[: ANOS_TUTORIAL * 365]
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0, **cfg)
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
        'Saldo de carbono do projeto do tutorial conforme o material do reservatório',
        'Efeito do volume da cisterna de concreto sobre o saldo de carbono',
    ],
    'cap12_multicriterio.md': [
        'Matriz de decisão multicritério: cada volume da varredura avaliado nas três dimensões de análise',
        'Volume vencedor segundo cada critério isolado',
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
    r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0, **_config_tutorial())
    L.append(f"| **simulação diária, ganho marginal de 1 %/m³** | varredura | **5 000 L** "
             f"| **{br(r.potential_potable_savings_pct, 2)}%** |")

    F = ["", "| Volume | Fração de armazenamento S/(A·R) | Passo recomendado por Fewkes e Butler |",
         "| ---: | ---: | :--- |"]
    for v in (1, 2, 3, 5, 8, 12, 20):
        fr = v / (A * P / 1000.0)
        passo = "horário" if fr <= 0.01 else ("diário" if fr <= 0.125 else "mensal")
        F.append(f"| {br(v * 1000, 0)} L | {br(fr, 4)} | {passo} |")
    return NL.join(L + F)


def tabela_inventario():
    """Seção de ciclo de vida: o inventário do projeto fechado, item a item."""
    from netuno.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=5000.0, **_config_projeto())
    cfg = _config_ambiental(r)
    cfg.lower_material_key = "PEAD"
    lca = calculate_lca(5000.0, r.annual_pluvial_consumed_m3, cfg)
    nomes = {
        "Cisterna Inferior": "cisterna de 5.000 L, polietileno",
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
        ("cap14_cidades.md", tabela_cidades),
        ("cap24_metodos.md", tabela_metodos_empiricos),
        ("cap30_inventario.md", tabela_inventario),
    ):
        caminho = os.path.join(SAIDA, nome)
        gravar(caminho, com_legenda(os.path.basename(caminho), fn()) + NL)
        print(f"  {os.path.relpath(caminho, AQUI)}")

    return r


if __name__ == "__main__":
    print("tabelas do manual:")
    main()
