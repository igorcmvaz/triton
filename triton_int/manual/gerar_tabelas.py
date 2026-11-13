# -*- coding: utf-8 -*-
"""Gera as tabelas numéricas dos capítulos da Edição Internacional, rodando o próprio programa.

Nenhum número do manual sai da cabeça de quem escreve. As tabelas deste arquivo são produzidas
executando o Triton com os dados de entrada declarados, de modo que uma correção no motor apareça no
manual na mesma alteração.

Edição Internacional (INT): o tutorial é uma casa em **Nova York** (chuva ERA5 1991-2020 de
``data/rainfall/NewYork.csv`` e tarifa de água e esgoto do NYC Water Board, a mesma de
``examples/new_york.triton``); as cidades de comparação são **Londres** e **Cidade do Cabo**. Nada
do Brasil. Os **custos são ilustrativos**: a edição não traz preços de obra, e os números abaixo
(tanques, mão de obra, bomba, energia, cloro, taxas) servem para o leitor ver o método. Cada tabela
com dinheiro diz, na legenda e na linha, que o valor é «illustrative, not a market price».

Saída: as tabelas em inglês, em ``manual/en/partes/_tabelas/*.md`` (as que os capítulos incluem) e,
iguais, em ``manual/partes/_tabelas/*.md`` (o rastro em português da BRL, que na INT não é lido).
Como o texto da INT é inglês de origem, não há tradução depois: ``en/traduzir_tabelas.py`` não faz
mais parte do caminho.

Executar a partir da raiz do programa (``TRITON_REGERAR=1`` para sobrescrever tabelas revisadas):
    python manual/gerar_tabelas.py
"""

from __future__ import annotations

import os

os.environ["TRITON_EDITION"] = "INT"

import sys

import numpy as np

from escrita_segura import gravar  # não desfaz revisão feita à mão

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from triton.core.simulation import run_single_simulation  # noqa: E402

#: Onde as tabelas saem: a pasta que os capítulos em inglês incluem e o rastro da BRL.
SAIDA_EN = os.path.join(AQUI, "en", "partes", "_tabelas")
SAIDA = os.path.join(AQUI, "partes", "_tabelas")
os.makedirs(SAIDA_EN, exist_ok=True)
os.makedirs(SAIDA, exist_ok=True)

NL = chr(10)
MENOS = "−"

#: Nota que acompanha todo valor monetário do manual.
ILUSTRATIVO = "illustrative, not a market price"
MOEDA = "US$"


def n(v, casas=1):
    """Número no padrão inglês: 1,234.5 (sem «-0»)."""
    v = round(float(v), casas)
    if v == 0:
        v = 0.0
    return f"{v:,.{casas}f}".replace("-", MENOS)


def usd(v, casas=0):
    """Dinheiro do tutorial, em dólares americanos (ilustrativo)."""
    texto = n(abs(v) if round(float(v), casas) < 0 else v, casas)
    return (MENOS if round(float(v), casas) < 0 else "") + f"{MOEDA} {texto}"


def anos_ou_nunca(x):
    """Payback em anos, ou «no payback» quando o investimento não se recupera."""
    return n(x, 1) + " years" if x else "no payback"


# ──────────────────────────────────────────────────────────────────────────────
# Seção 2.1 — o balanço diário, dez dias resolvidos (chuva real de Nova York)
# ──────────────────────────────────────────────────────────────────────────────
#
# O caso didático: dez dias consecutivos da série de Nova York (21 a 30 de setembro de 2018, reanálise
# ERA5), escolhidos entre os 30 anos porque reúnem, em dez linhas, tudo o que o balanço ensina: o
# primeiro dia com o reservatório vazio, um dia de atendimento parcial, um dia com chuva abaixo da
# lâmina de descarte (perdido inteiro), um extravasamento maior que o próprio reservatório e um dia de
# extravasamento antes do consumo. Números redondos para a planilha do leitor.

CASO_23 = {
    "area": 100.0,            # m²
    "runoff_coeff": 0.85,     # telha cerâmica
    "discard_mm": 2.0,        # lâmina de descarte, todo evento
    "discard_mode": 1,
    "demanda_total": 200.0,   # L/dia
    "rainwater_share": 0.40,  # 40% da demanda é não potável
    "volume": 2000.0,         # L
    "inicio": "21/09/2018",   # data do primeiro dia, na série de Nova York
    "dia_na_serie": 10125,    # posição do primeiro dia em NewYork.csv (0 = 01/01/1991)
}

CHUVA_23 = [0.0, 2.4, 1.9, 0.0, 59.8, 9.2, 5.5, 32.9, 0.0, 0.0]


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

    cab = ("| Day | Rain | First flush | Effective rain | Collected | Rainwater demand "
           "| Consumed | Overflowed | In the tank | Supply |")
    sep = "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |"
    uni = "| | mm | mm | mm | L | L | L | L | L | |"
    linhas = [cab, sep, uni]

    nomes = {2: "full", 1: "partial", 0: "none"}
    for i, d in enumerate(r.daily_results, start=1):
        descartado = d.precip_mm - d.eff_precip_mm
        linhas.append(
            f"| {i} | {n(d.precip_mm)} | {n(descartado)} | {n(d.eff_precip_mm)} "
            f"| {n(d.harvested_liters, 0)} | {n(d.pluvial_demand_liters, 0)} "
            f"| {n(d.pluvial_consumed_liters, 0)} | {n(d.spilled_liters, 0)} "
            f"| {n(d.lower_tank_end_liters, 0)} | {nomes[d.satisfaction_type]} |"
        )

    tot_cap = sum(d.harvested_liters for d in r.daily_results)
    tot_con = sum(d.pluvial_consumed_liters for d in r.daily_results)
    tot_ext = sum(d.spilled_liters for d in r.daily_results)
    final = r.daily_results[-1].lower_tank_end_liters
    linhas.append(
        f"| **sum** | | | | **{n(tot_cap, 0)}** | | **{n(tot_con, 0)}** "
        f"| **{n(tot_ext, 0)}** | {n(final, 0)} | |"
    )

    resumo = NL.join([
        "",
        "| Closure check | Litres |",
        "| :--- | ---: |",
        f"| collected in the period | {n(tot_cap, 0)} |",
        f"| minus the overflow | {MENOS}{n(tot_ext, 0)} |",
        f"| minus the consumption | {MENOS}{n(tot_con, 0)} |",
        f"| minus what stayed in the tank | {MENOS}{n(final, 0)} |",
        f"| **residual** | **{n(tot_cap - tot_ext - tot_con - final, 0)}** |",
        "",
    ])

    indicadores = NL.join([
        "",
        "| Ten-day indicator | Value |",
        "| :--- | ---: |",
        f"| potable water saving potential | {n(r.potential_potable_savings_pct)}% |",
        f"| daily mean of rainwater consumed | {n(r.avg_pluvial_consumed_l_day)} L/day |",
        f"| daily mean of potable water consumed | {n(r.avg_potable_consumed_l_day)} L/day |",
        f"| daily mean overflow | {n(r.avg_spilled_l_day)} L/day |",
        f"| days of full supply | {n(r.pct_days_full_satisfaction, 0)}% |",
        f"| days of partial supply | {n(r.pct_days_partial_satisfaction, 0)}% |",
        f"| days of no supply | {n(r.pct_days_null_satisfaction, 0)}% |",
        "",
    ])

    return NL.join(linhas) + NL + resumo + indicadores, r


def entrada_dez_dias():
    c = CASO_23
    return NL.join([
        "| Input | Value |",
        "| :--- | ---: |",
        f"| catchment area | {n(c['area'], 0)} m² |",
        f"| runoff coefficient | {n(c['runoff_coeff'], 2)} |",
        f"| first-flush depth | {n(c['discard_mm'])} mm, at every event |",
        f"| total demand | {n(c['demanda_total'], 0)} L/day |",
        f"| fraction suppliable by rainwater | {n(c['rainwater_share'] * 100, 0)}% "
        f"= {n(c['demanda_total'] * c['rainwater_share'], 0)} L/day |",
        f"| lower tank volume | {n(c['volume'], 0)} L |",
        "| upper tank | none |",
        "| rainfall | New York, 21 to 30 September 2018 (ERA5 reanalysis) |",
        "",
        "The ten-day rainfall series, in millimetres:",
        "",
        "| Day | " + " | ".join(str(i) for i in range(1, 11)) + " |",
        "| ---: |" + " ---: |" * 10,
        "| Rain | " + " | ".join(n(p) for p in CHUVA_23) + " |",
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Parte 2 — o projeto do tutorial: residência unifamiliar em Nova York
# ──────────────────────────────────────────────────────────────────────────────
#
# Um projeto só, que cresce ao longo de dez capítulos. A série de Nova York é longa (30 anos), a tarifa do
# NYC Water Board é pública e auditável (``examples/LEIA.md``) e a cidade tem chuva bem distribuída
# no ano: o regime mais comum, contra o qual Londres (mais fina e frequente) e a Cidade do Cabo
# (concentrada no inverno) se comparam.

CHUVAS = os.path.join(RAIZ, "data", "rainfall")
SERIE_TUTORIAL = os.path.join(CHUVAS, "NewYork.csv")
ANOS_TUTORIAL = 30
INICIO_DA_SERIE = "01/01/1991"

TUTORIAL = {
    "area": 150.0,             # m² de cobertura, projeção horizontal
    "runoff_coeff": 0.85,      # telha cerâmica
    "discard_mm": 2.0,         # lâmina de descarte
    "discard_mode": 1,         # todo evento de chuva
    "moradores": 4,
    "per_capita": 150.0,       # L/hab·dia
    # Bacia sanitária e usos externos.
    "rainwater_share": 0.28,
    "volume_inicial": 3000.0,  # o primeiro palpite, do capítulo 6
    # A partir da seção do reservatório superior, o projeto adota recalque para
    # caixa elevada: é a comparação daquela seção, com o limiar de 100 L.
    "caixa_superior_l": 1000.0,
    "limiar_recalque_l": 100.0,
    # O volume que o tutorial escolhe: ideal pelo ganho marginal de 1 %/m³ em Nova York, Londres e
    # Cidade do Cabo. O multicritério de oito critérios da 0.2.0, com os quatro eixos iguais, indica
    # 2.000 L; o capítulo 12 mostra o que a escolha de 4.000 L cede e quando o menor é defensável.
    "volume": 4000.0,
}

VOLUME = TUTORIAL["volume"]


def vol_br(v=None):
    """Volume em litros com separador de milhar: 4,000 L (nome antigo, formato inglês)."""
    v = VOLUME if v is None else v
    return f"{int(round(v)):,} L"


vol_en = vol_br

VOLUMES_VARREDURA = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000,
                     10000, 12000, 16000, 20000]


def _serie(chave="NewYork"):
    from triton.core.parser import load_precipitation
    return load_precipitation(os.path.join(CHUVAS, chave + ".csv"))[: ANOS_TUTORIAL * 365 + 8]


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
    """Capítulo 4: o que a série de Nova York tem dentro."""
    serie = _serie()
    anos = len(serie) / 365.25
    chuvosos = serie[serie > 0.1]
    return NL.join([
        "| The New York series | Value |",
        "| :--- | ---: |",
        f"| days in the series | {n(len(serie), 0)} |",
        f"| years | {n(anos, 1)} |",
        f"| mean annual precipitation | {n(serie.sum() / anos, 0)} mm |",
        f"| days with rain | {n((serie > 0.1).mean() * 100, 0)}% |",
        f"| mean rain on rainy days | {n(chuvosos.mean(), 1)} mm |",
        f"| largest daily rainfall | {n(serie.max(), 1)} mm |",
        f"| days below the first-flush depth | {n(((serie > 0.1) & (serie <= 2.0)).mean() * 100, 0)}% |",
    ])


def tabela_primeira_simulacao():
    """Capítulo 6: o primeiro resultado, com o volume de palpite."""
    r = run_single_simulation(
        precip_data=_serie(), lower_tank_vol=TUTORIAL["volume_inicial"],
        **_config_tutorial())
    dem = TUTORIAL["moradores"] * TUTORIAL["per_capita"]
    return NL.join([
        "| Result with " + n(TUTORIAL["volume_inicial"], 0) + " L | Value |",
        "| :--- | ---: |",
        f"| potable water saving potential | **{n(r.potential_potable_savings_pct, 2)}%** |",
        f"| rainwater consumed | {n(r.avg_pluvial_consumed_l_day, 1)} L/day |",
        f"| mains water consumed | {n(r.avg_potable_consumed_l_day, 1)} L/day |",
        f"| water overflowed | {n(r.avg_spilled_l_day, 1)} L/day |",
        f"| days of full supply | {n(r.pct_days_full_satisfaction, 1)}% |",
        f"| days of partial supply | {n(r.pct_days_partial_satisfaction, 1)}% |",
        f"| days of no supply | {n(r.pct_days_null_satisfaction, 1)}% |",
        f"| intended rainwater demand | {n(dem * TUTORIAL['rainwater_share'], 0)} L/day |",
        f"| annual volume saved | {n(r.annual_pluvial_consumed_m3, 1)} m³/year |",
    ]), r


def tabela_varredura():
    """Capítulo 7: a curva de retorno decrescente."""
    serie = _serie()
    cfg = _config_tutorial()
    linhas = [
        "| Volume | Potential | Gain over the previous | Gain per cubic metre added "
        "| Overflow | Full-supply days |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        "| L | % | percentage points | %/m³ | L/day | % |",
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
            ganho, marginal = n(dp, 2), n(dp / dv, 2)
        linhas.append(
            f"| {n(v, 0)} | {n(r.potential_potable_savings_pct, 2)} | {ganho} "
            f"| {marginal} | {n(r.avg_spilled_l_day, 0)} | {n(r.pct_days_full_satisfaction, 1)} |"
        )
        dados.append((v, r.potential_potable_savings_pct))
        anterior = (v, r.potential_potable_savings_pct)
    return NL.join(linhas), dados


# ── os custos ilustrativos e a tarifa do tutorial, declarados uma vez ────────────────────────────
#
# A tarifa é a de Nova York (``examples/new_york.triton``, gerada por ``scripts/gerar_exemplos_int.py``).
# Os custos NÃO são preços de mercado: são números redondos, ilustrativos, para o leitor acompanhar o
# método. A edição não traz tabela de preços de obra; o usuário informa os dele (etapa 5).

def _tarifa_de_nova_york():
    from gerar_exemplos_int import _nova_york
    return _nova_york()["campos"]


CAMPOS_NOVA_YORK = _tarifa_de_nova_york()
#: Faixas de água de Nova York: (início, fim, tarifa, tipo). Nome antigo: ``TARIFA_CASAN``.
TARIFA_TUTORIAL = list(CAMPOS_NOVA_YORK["water_tariffs"])
TARIFA_CASAN = TARIFA_TUTORIAL

CUSTOS_TUTORIAL = dict(
    cost_labor=1500.0, cost_piping=600.0, cost_accessories=800.0,   # US$, ilustrativos
    pump_unit_cost=250.0,                                            # US$ por bomba, ilustrativo
    elec_tariff=0.20,                                                # US$/kWh, ilustrativo
    chlorine_cost_per_kg=8.0,                                        # US$/kg de produto, ilustrativo
    tma=0.4, inflation=0.2,                                          # % ao mês
    analysis_period_years=20, tariff_escalation=12,
    water_tariff_escalation=3.0, sewage_tariff_escalation=3.0,       # % ao ano, ilustrativos
    elec_tariff_escalation=3.0,
)

#: Manutenção anual do tutorial, US$ ilustrativos (nome, período em meses, custo fixo, custo por m³).
MANUTENCAO_TUTORIAL = [
    ("Gutter and pre-filter inspection and cleaning", 12, 20.0, 0.0),
    ("Cistern cleaning and inspection", 12, 40.0, 0.0),
    ("Preventive pump maintenance", 12, 30.0, 0.0),
]

#: Preço ilustrativo dos tanques: ``base + por_litro × volume``, em US$. Não é preço de mercado.
PRECO_DO_TANQUE = {
    "PEAD": (100.0, 0.55),
    "CONCRETO": (600.0, 0.40),
    "FIBRA": (120.0, 0.65),
    "ACO_INOX": (300.0, 2.00),
}

#: Fatores ambientais ilustrativos: a edição não traz fator de rede nem de água; o usuário informa o dele.
FATOR_DA_REDE_KG_KWH = 0.40       # kg CO₂e/kWh, ilustrativo
FATOR_DA_AGUA_KG_M3 = 0.50        # kg CO₂e/m³ de água de rede evitada, ilustrativo


def estimate_tank_price(volume_l, material="PEAD"):
    """Preço ilustrativo do tanque, em US$ (substitui o catálogo em reais do programa)."""
    base, por_litro = PRECO_DO_TANQUE[material]
    return base + por_litro * float(volume_l)


def _config_base(campos=None):
    """A configuração da edição com a tarifa e os custos ilustrativos do tutorial."""
    from triton.core.edition import configuracao_da_edicao
    cfg = configuracao_da_edicao()
    for k, v in (campos or CAMPOS_NOVA_YORK).items():
        setattr(cfg, k, v)
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    cfg.op_costs = list(MANUTENCAO_TUTORIAL)
    return cfg


def _config_economica(volume_l, material="CONCRETO"):
    cfg = _config_base()
    cfg.cost_lower_tank = estimate_tank_price(float(volume_l), material)
    # Recalque para caixa superior de 1.000 L em polietileno, com as duas
    # motobombas (principal e reserva).
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = True
    cfg.upper_tank_vol = TUTORIAL["caixa_superior_l"]
    cfg.pumping_threshold = TUTORIAL["limiar_recalque_l"]
    cfg.cost_upper_tank = estimate_tank_price(TUTORIAL["caixa_superior_l"], "PEAD")
    cfg.pump_count = 2
    cfg.residents_count = TUTORIAL["moradores"]
    cfg.area = TUTORIAL["area"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.first_flush_system_enabled = True
    return cfg


def _config_ambiental(sim=None):
    """A configuração ambiental do tutorial, coerente com a econômica.

    O descarte físico entra com o carbono incorporado do reservatório de
    descarte e do separador de folhas. Os fatores de rede e de água são
    ilustrativos (a edição não traz o do usuário). Com o resultado da simulação,
    a energia vem da mesma função que o econômico usa.
    """
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.pump_energy import compute_annual_pump_energy
    cfg = EnvironmentalConfig()
    cfg.grid_co2_factor_kg_kwh = FATOR_DA_REDE_KG_KWH
    cfg.potable_water_co2_kg_m3 = FATOR_DA_AGUA_KG_M3
    cfg.roof_area_m2 = TUTORIAL["area"]
    cfg.discard = TUTORIAL["discard_mm"]
    cfg.first_flush_system_enabled = True
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = True
    cfg.upper_tank_vol_liters = TUTORIAL["caixa_superior_l"]
    if sim is not None:
        cfg.annual_pump_kwh = compute_annual_pump_energy(_config_economica(VOLUME), sim).annual_kwh
    return cfg


def tabela_limiar_e_custo():
    """Capítulo 7: o limiar decide o volume, e o volume decide o custo."""
    from triton.core.environmental import calculate_lca
    from triton.core.simulation import run_sweep_simulation

    serie = _serie()
    cfg = _config_tutorial()
    linhas_limiar = [
        "| Declared threshold | Ideal volume | Potential |",
        "| ---: | ---: | ---: |",
    ]
    for limiar in (3.0, 1.0, 0.5):
        r = run_sweep_simulation(
            precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
            delta_ideal_threshold=limiar, **cfg)
        linhas_limiar.append(
            f"| {n(limiar, 1)} %/m³ | {n(r.optimal_lower_tank_vol, 0)} L "
            f"| {n(r.optimal_potential_pct, 2)}% |"
        )

    linhas_custo = [
        "",
        f"| | {vol_br()} | 20,000 L |",
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
        f"| saving potential | {n(a[0], 2)}% | {n(b[0], 2)}% |",
        f"| concrete cistern price ({ILUSTRATIVO}) | {usd(a[1])} | {usd(b[1])} |",
        f"| mass of concrete | {n(a[2], 0)} kg | {n(b[2], 0)} kg |",
        f"| embodied carbon of the system | {n(a[3], 0)} kg CO₂e | {n(b[3], 0)} kg CO₂e |",
        f"| **price ratio** | | **{n(b[1] / a[1], 1)}×** |",
        f"| **potential gain** | | **+{n(b[0] - a[0], 2)} points** |",
    ]
    return NL.join(linhas_limiar) + NL + NL.join(linhas_custo)


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
    tarifa = CUSTOS_TUTORIAL["elec_tariff"]

    L = [
        f"| Same storage of {vol_br(VOLUME + 1000)} | One tank only | {n(VOLUME, 0)} below + 1,000 above |",
        "| :--- | ---: | ---: |",
        f"| saving potential | {n(unico.potential_potable_savings_pct, 2)}% "
        f"| {n(duplo.potential_potable_savings_pct, 2)}% |",
        f"| days of full supply | {n(unico.pct_days_full_satisfaction, 1)}% "
        f"| {n(duplo.pct_days_full_satisfaction, 1)}% |",
        f"| volume pumped | — | {n(duplo.total_pumped_liters / anos / 1000, 1)} m³/year |",
        f"| pump starts | — | {n(duplo.total_pump_cycles / anos, 0)} per year |",
        f"| pump hours | — | {n(e.pump_hours_year, 1)} h/year |",
        f"| energy | — | {n(e.annual_kwh, 1)} kWh/year |",
        f"| energy cost ({ILUSTRATIVO}) | — | {usd(e.annual_kwh * tarifa, 2)}/year |",
        f"| **potential difference** | | **{n(duplo.potential_potable_savings_pct - unico.potential_potable_savings_pct, 2)} points** |",
    ]
    return NL.join(L)


def tabela_limiar_de_acionamento():
    """Capítulo 8: o limiar troca potencial por desgaste da bomba."""
    serie = _serie()
    cfg = _config_tutorial()
    L = ["| Trigger level | Potential | Starts per year |",
         "| ---: | ---: | ---: |"]
    for lim in (0, 100, 300, 500):
        r = run_single_simulation(
            precip_data=serie, lower_tank_vol=VOLUME, upper_tank_vol=1000.0,
            upper_tank_used=True, pumping_threshold=float(lim), **cfg)
        anos = r.total_days / 365.25
        L.append(f"| {n(lim, 0)} L | {n(r.potential_potable_savings_pct, 2)}% "
                 f"| {n(r.total_pump_cycles / anos, 0)} |")
    return NL.join(L)


def tabela_etap():
    """Capítulo 9: a classe recomenda, o projetista decide.

    A edição não traz preços de equipamento: a tabela mostra o que o programa dimensiona sem preço
    (as etapas de desinfecção, a energia e o carbono anual), e a recomendação de filtração fina por classe.
    """
    from triton.core.water_quality import WATER_QUALITY_CLASSES, size_etap

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3

    L = ["| Disinfection | Stages | Annual UV energy | Annual CO₂e |",
         "| :--- | :---: | ---: | ---: |"]
    nomes = {"cloro": "Tablet chlorination",
             "uv": "Chlorination + ultraviolet",
             "ozonio": "Chlorination + ozonation"}
    for des in ("cloro", "uv", "ozonio"):
        e = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=m3,
                      roof_area_m2=150.0, disinfection_choice=des,
                      discard_mm=2.0, include_first_flush=True,
                      grid_co2_factor_kg_kwh=FATOR_DA_REDE_KG_KWH)
        L.append(f"| {nomes[des]} | {len(e.disinfection_stages)} "
                 f"| {n(e.uv_annual_kwh, 1)} kWh "
                 f"| {n(e.total_etap_co2e_kg_yr, 1)} kg |")

    L += ["", "| Target class | Fine filtration recommended? |",
          "| :--- | :---: |"]
    for cid, c in WATER_QUALITY_CLASSES.items():
        L.append(f"| {cid.replace('_', ' ').replace('classe', 'class')} "
                 f"| {'yes' if c.exige_filtracao_fina else 'no'} |")
    return NL.join(L)


def _conta(litros_mes, cfg):
    """Fatura mensal de água e esgoto, pela tarifa do projeto."""
    from triton.core.economic import calculate_water_bill
    return calculate_water_bill(
        litros_mes, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
        cfg.water_tax_fixed, cfg.water_tax_var,
        sewage_tariffs=cfg.sewage_tariffs, sewage_volume_factor=cfg.sewage_volume_factor)


def tabela_economica():
    """Capítulo 10: a conta de Nova York, com e sem o sistema."""
    from triton.core.economic import run_economic_analysis

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    dias_mes = 30.4375
    tot_m3 = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * dias_mes / 1000.0
    pot_m3 = r.avg_potable_consumed_l_day * dias_mes / 1000.0

    cfg = _config_economica(VOLUME, "CONCRETO")
    sem = _conta(tot_m3 * 1000, cfg)
    com = _conta(pot_m3 * 1000, cfg)
    e = run_economic_analysis(cfg, r)

    L = [
        "| The New York water and sewer bill | Consumption | Amount |",
        "| :--- | ---: | ---: |",
        f"| without the system | {n(tot_m3, 2)} m³/month | {usd(sem, 2)} |",
        f"| with the system | {n(pot_m3, 2)} m³/month | {usd(com, 2)} |",
        f"| **saving** | {n(tot_m3 - pot_m3, 2)} m³/month | **{usd(sem - com, 2)}** |",
        "",
        f"| Twenty-year analysis (costs {ILUSTRATIVO}) | Value |",
        "| :--- | ---: |",
        f"| initial investment | {usd(e.capex_total, 2)} |",
        f"| annual water saving | {usd(e.annual_water_savings_brl, 2)} |",
        f"| annual running cost | {usd(e.annual_opex_brl, 2)} |",
        f"| net present value | {usd(e.vpl, 2)} |",
        f"| internal rate of return | {n(e.tir_annual_pct or 0.0, 2)}% per year |",
        f"| discounted payback | {anos_ou_nunca(e.payback_years)} |",
    ]
    return NL.join(L)


def tabela_materiais():
    """Capítulo 11: o material decide o sinal do resultado ambiental."""
    from triton.core.environmental import MATERIAL_PRESETS, calculate_lca

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3
    # Emissões líquidas, e não saldo: positivo emite, negativo retira. É a
    # convenção do gráfico de balanço da aba ambiental do programa.
    L = ["| Cistern material | Mass | Embodied carbon | Carbon payback "
         f"| Net emissions over 20 years | Price ({ILUSTRATIVO}) |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    nomes = {"PEAD": "Polyethylene (HDPE)", "CONCRETO": "Reinforced concrete",
             "FIBRA": "Glass fibre", "ACO_INOX": "Stainless steel"}
    for k in MATERIAL_PRESETS:
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        lca = calculate_lca(VOLUME, m3, cfg)
        preco = usd(estimate_tank_price(VOLUME, k)) if k in PRECO_DO_TANQUE else "—"
        L.append(f"| {nomes.get(k, k)} | {n(lca.lower_tank_mass_kg, 0)} kg "
                 f"| {n(lca.total_embodied_co2_kg, 0)} kg CO₂e "
                 f"| {n(lca.environmental_payback_years, 1)} years "
                 f"| {n(-lca.lifetime_net_co2_saved_kg, 0)} kg | {preco} |")

    L += ["", "| Concrete volume | Carbon payback | Net emissions over 20 years |",
          "| ---: | ---: | ---: |"]
    for v in (2000, 3000, VOLUME, 8000):
        rr = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                   **_config_projeto())
        cfg = _config_ambiental(rr)
        cfg.lower_material_key = "CONCRETO"
        lca = calculate_lca(float(v), rr.annual_pluvial_consumed_m3, cfg)
        L.append(f"| {n(v, 0)} L | {n(lca.environmental_payback_years, 1)} years "
                 f"| {n(-lca.lifetime_net_co2_saved_kg, 0)} kg CO₂e |")
    return NL.join(L)


#: Os volumes candidatos do capítulo 12 e da seção 32.
VOLUMES_MULTICRITERIO = (1000, 2000, 3000, 4000, 5000, 8000, 12000)


def candidatos_multicriterio(material="PEAD", volumes=VOLUMES_MULTICRITERIO):
    """As alternativas do multicritério, montadas como o programa as monta.

    ``candidato_dos_resultados`` é a mesma montagem da linha de comando e da interface: a
    simulação, a análise econômica e o CO₂e de ciclo de vida de cada volume, e a massa a seco da
    calculadora de peso com a configuração padrão. Devolve também as simulações e as análises
    econômicas, que as tabelas e as figuras citam.
    """
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import calculate_lca
    from triton.core.topsis import candidato_dos_resultados

    serie = _serie()
    cfg_sim = _config_projeto()
    cands, sims, econs = [], [], []
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg_sim)
        e = run_economic_analysis(_config_economica(v, material), r)
        amb = _config_ambiental(r)
        amb.lower_material_key = material
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        cands.append(candidato_dos_resultados(r, e, lca.lifetime_net_co2_saved_kg))
        sims.append(r)
        econs.append(e)
    return cands, sims, econs


def tabela_multicriterio():
    """Capítulo 12: oito critérios em quatro eixos, e o vencedor de cada eixo sozinho."""
    from triton.core.topsis import calculate_topsis_scores

    cands, _, _ = candidatos_multicriterio()
    res = calculate_topsis_scores(cands)
    m = res.decision_matrix
    linhas = [
        "| Volume | Volumetric reliability | Storage efficiency | Net saving (NPV) | LCOW "
        "| Discounted payback | Net life-cycle CO₂e | Dry mass | Overflow |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        "| L | % | % of the volume per day | US$ | US$/m³ | years | kg | kg | m³/year |",
    ]
    for i, c in enumerate(cands):
        pb = n(m[i, 4], 1) if c.discounted_payback_years else "no payback"
        linhas.append(
            f"| {n(c.lower_tank_vol, 0)} | {n(m[i, 0], 2)} | {n(m[i, 1], 2)} | {usd(m[i, 2])} "
            f"| {usd(m[i, 3], 2)} | {pb} | {n(m[i, 5], 0)} | {n(m[i, 6], 0)} | {n(m[i, 7], 1)} |")

    global _CANDIDATOS_MULTICRITERIO
    _CANDIDATOS_MULTICRITERIO = cands
    faixa = res.faixa_de_escolha()
    linhas += [
        "",
        "| Dimension taken alone, or the four together | Volume |",
        "| :--- | ---: |",
        f"| technical: highest volumetric reliability | {n(cands[res.technical_best_index].lower_tank_vol, 0)} L |",
        "| economic: shortest discounted payback, ties broken by the net saving "
        f"| {n(cands[res.financial_best_index].lower_tank_vol, 0)} L |",
        f"| environmental: lowest net life-cycle CO₂e | {n(cands[res.environmental_best_index].lower_tank_vol, 0)} L |",
        f"| **the four dimensions equal: TOPSIS choice band, within {n(100 * faixa['tolerance'], 0)}% "
        f"of the score range** | **{faixa_txt(faixa)}** |",
        f"| the four dimensions equal: highest TOPSIS score | {n(faixa['best_volume_l'], 0)} L |",
    ]
    return NL.join(linhas)


def faixa_txt(faixa):
    """A faixa de escolha em texto: «2,000–3,000 L», «1,000 L» ou, com lacuna, «2,000 and 4,000 L»."""
    vols = [n(v, 0) for v in faixa["volumes_l"]]
    if len(vols) == 1:
        return f"{vols[0]} L"
    if faixa["contiguous"]:
        return f"{vols[0]}–{vols[-1]} L"
    return ", ".join(vols[:-1]) + f" and {vols[-1]} L"


_CANDIDATOS_MULTICRITERIO = None

#: Pesos dos quatro eixos (técnico, econômico, ambiental, estrutural) da tabela de sensibilidade:
#: os quatro iguais, e 70% no eixo dominante com 10% em cada um dos outros três.
PESOS_SENSIBILIDADE = (
    ("equal weights, 25% on each dimension", (0.25, 0.25, 0.25, 0.25)),
    ("technical, 70%", (0.7, 0.1, 0.1, 0.1)),
    ("economic, 70%", (0.1, 0.7, 0.1, 0.1)),
    ("environmental, 70%", (0.1, 0.1, 0.7, 0.1)),
    ("structural, 70%", (0.1, 0.1, 0.1, 0.7)),
)

#: Partes no eixo com a eficiência de armazenamento fora da conta: o eixo técnico passa a medir só a
#: confiabilidade volumétrica. É o caso que o capítulo 12 discute para o volume do tutorial.
PARTES_SEM_EFICIENCIA = (1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
PESOS_SEM_EFICIENCIA = (
    ("equal weights, 25% on each dimension", (0.25, 0.25, 0.25, 0.25)),
    ("technical, 70%", (0.7, 0.1, 0.1, 0.1)),
)


def _ordem_e_margem(cands, res):
    """O volume de maior escore, o segundo e a margem entre os dois."""
    ordem = sorted(range(len(cands)), key=lambda i: (-res.scores[i], cands[i].lower_tank_vol))
    return ordem[0], ordem[1], res.scores[ordem[0]] - res.scores[ordem[1]]


def _linha_de_pesos(cands, rotulo, pesos, partes=None):
    from triton.core.topsis import calculate_topsis_scores
    res = calculate_topsis_scores(cands, weights=pesos, parts=partes)
    primeiro, segundo, margem = _ordem_e_margem(cands, res)
    return (f"| {rotulo} | {faixa_txt(res.faixa_de_escolha())} | {n(cands[primeiro].lower_tank_vol, 0)} L "
            f"| {n(cands[segundo].lower_tank_vol, 0)} L | {n(margem, 3)} |")


def _linha_de_eixos(cands, rotulo, pesos):
    """Os pesos somados por eixo, a faixa e o maior escore (pesos declarados ou «critic»)."""
    from triton.core.topsis import calculate_topsis_scores
    res = calculate_topsis_scores(cands, weights=pesos)
    w = np.asarray(res.criterion_weights, dtype=float)
    eixos = (w[0] + w[1], w[2] + w[3] + w[4], w[5], w[6] + w[7])
    primeiro, _, margem = _ordem_e_margem(cands, res)
    return (f"| {rotulo} | " + " | ".join(f"{n(100 * x, 1)}%" for x in eixos)
            + f" | {faixa_txt(res.faixa_de_escolha())} | {n(cands[primeiro].lower_tank_vol, 0)} L "
            f"| {n(margem, 3)} |")


def tabela_pesos():
    """Capítulo 12: a faixa do TOPSIS conforme o peso dominante, sem a eficiência e com o CRITIC."""
    from triton.core.topsis import PESOS_CRITIC
    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    L = ["| Dominant weight | Choice band | Highest score | Runner-up | Score margin |",
         "| :--- | ---: | ---: | ---: | ---: |"]
    for rotulo, pesos in PESOS_SENSIBILIDADE:
        L.append(_linha_de_pesos(cands, rotulo, pesos))
    L += ["", "| Weights, with the storage-efficiency share at zero | Choice band | Highest score | Runner-up "
          "| Score margin |",
          "| :--- | ---: | ---: | ---: | ---: |"]
    for rotulo, pesos in PESOS_SEM_EFICIENCIA:
        L.append(_linha_de_pesos(cands, rotulo, pesos, PARTES_SEM_EFICIENCIA))
    L += ["", "| Weights | Technical | Economic | Environmental | Structural | Choice band | Highest score "
          "| Score margin |",
          "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
          _linha_de_eixos(cands, "declared, equal", (0.25, 0.25, 0.25, 0.25)),
          _linha_de_eixos(cands, "objective, CRITIC", PESOS_CRITIC)]
    return NL.join(L)


#: Pressão de trabalho da comparação de pressurizadores, e a de uma casa mais alta.
PRESSOES_PRESSURIZADOR = (18.0, 24.0)


def _pressurizadores_ilustrativos():
    """Seis pressurizadores **genéricos**, de curvas ilustrativas: sem marca, sem catálogo.

    A edição não traz catálogo de fabricante. Os modelos A a F representam os três tipos de controle
    (pressostato, eletrônico, fluxostato) em duas ou três potências, com curvas simplificadas.
    """
    from triton.core.pressurizer_catalog import ELETRONICO, FLUXOSTATO, PRESSOSTATO, Pressurizador
    return (
        Pressurizador("a", "Model A, 0.25 hp", 0.25, PRESSOSTATO, ((0.0, 25.0), (36.0, 0.0)),
                      liga_m=12.0, desliga_m=22.0),
        Pressurizador("b", "Model B, 0.33 hp", 1.0 / 3.0, FLUXOSTATO, ((0.0, 20.0), (180.0, 0.0))),
        Pressurizador("c", "Model C, 0.5 hp", 0.5, PRESSOSTATO, ((0.0, 40.0), (50.0, 0.0)),
                      liga_m=18.0, desliga_m=28.0),
        Pressurizador("d", "Model D, 0.5 hp", 0.5, PRESSOSTATO,
                      ((0.0, 32.0), (12.0, 25.0), (30.0, 16.0), (45.0, 9.0), (52.0, 5.0)),
                      liga_m=15.0),
        Pressurizador("e", "Model E, 0.5 hp", 0.5, ELETRONICO,
                      ((0.0, 20.0), (7.0, 18.0), (17.0, 16.0), (27.0, 12.0), (39.0, 6.0), (41.0, 4.0)),
                      retardo_s=10.0),
        Pressurizador("f", "Model F, 0.5 hp", 0.5, ELETRONICO, ((0.0, 20.0), (83.0, 7.0))),
    )


def tabela_pressurizadores():
    """Seção 28: seis pressurizadores genéricos no projeto do tutorial."""
    from triton.core.pressurizer_catalog import (
        ELETRONICO, FLUXOSTATO, PRESSOSTATO, VAZAO_DO_PONTO_PADRAO_L_MIN, energia)
    from triton.core.supply_arrangement import DESCARGAS_POR_PESSOA_DIA

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_tutorial())
    v = r.annual_pluvial_consumed_m3
    partidas = TUTORIAL["moradores"] * DESCARGAS_POR_PESSOA_DIA * 365.25
    controle = {PRESSOSTATO: "pressure switch", ELETRONICO: "electronic", FLUXOSTATO: "flow switch"}
    h1, h2 = PRESSOES_PRESSURIZADOR
    L = [f"| Model | Control | Curve flow at {n(h1, 0)} m head | Hours per year "
         f"| kWh per year | kWh/m³ | kWh per year at {n(h2, 0)} m head |",
         "| :--- | :--- | ---: | ---: | ---: | ---: | ---: |"]
    linhas = []
    for p in _pressurizadores_ilustrativos():
        e1 = energia(p, v, h1, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        e2 = energia(p, v, h2, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        linhas.append((e1.kwh_ano, p, e1, e2))
    for _, p, e1, e2 in sorted(linhas, key=lambda x: x[0]):
        a24 = n(e2.kwh_ano, 1) if e2.atende else "not reached"
        L.append(f"| {p.rotulo} | {controle[p.controle]} | {n(e1.vazao_da_bomba_l_min, 1)} L/min "
                 f"| {n(e1.horas_ano, 0)} | {n(e1.kwh_ano, 1)} | {n(e1.kwh_por_m3, 2)} | {a24} |")
    return NL.join(L), v, partidas


#: Premissas perturbadas na tabela da seção 20: (rótulo, unidade, baixo, provável, alto).
PREMISSAS_SENSIBILIDADE = (
    ("tariff escalation, water and sewer", "% per year", 1.0, 3.0, 5.0),
    ("minimum attractive rate of return", "% per month", 0.2, 0.4, 0.6),
    ("per capita consumption", "L/person·day", 120.0, 150.0, 180.0),
    ("suppliable fraction", "%", 20.0, 28.0, 40.0),
    ("cistern price", "% of the budget", 70.0, 100.0, 130.0),
)


def _projeto_fechado(ajuste=None):
    """Potencial, VPL e retorno do projeto fechado do tutorial, com uma premissa mudada."""
    from triton.core.economic import run_economic_analysis
    cfg_sim = _config_projeto()
    cfg_eco = _config_economica(VOLUME, "PEAD")
    nome, valor = ajuste if ajuste else (None, None)
    if nome == "per capita consumption":
        cfg_sim["total_demand_per_day"] = TUTORIAL["moradores"] * valor
    elif nome == "suppliable fraction":
        cfg_sim["rainwater_share"] = valor / 100.0
    elif nome == "tariff escalation, water and sewer":
        cfg_eco.water_tariff_escalation = cfg_eco.sewage_tariff_escalation = valor
    elif nome == "minimum attractive rate of return":
        cfg_eco.tma = valor
    elif nome == "cistern price":
        cfg_eco.cost_lower_tank *= valor / 100.0
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **cfg_sim)
    e = run_economic_analysis(cfg_eco, r)
    return r.potential_potable_savings_pct, e.vpl, e.payback_years


def tabela_sensibilidade():
    """Seção 20: cada premissa variada sozinha, no projeto fechado do tutorial."""
    L = ["| Assumption | Low | Likely | High | Potential "
         f"| 20-year NPV ({ILUSTRATIVO}) | Discounted payback |",
         "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for rotulo, unidade, baixo, provavel, alto in PREMISSAS_SENSIBILIDADE:
        res = [_projeto_fechado((rotulo, v)) for v in (baixo, alto)]

        pb = anos_ou_nunca
        L.append(
            f"| {rotulo}, {unidade} | {n(baixo, 1)} | {n(provavel, 1)} | {n(alto, 1)} "
            f"| {n(res[0][0], 2)}% to {n(res[1][0], 2)}% "
            f"| {usd(res[0][1])} to {usd(res[1][1])} "
            f"| {pb(res[0][2])} to {pb(res[1][2])} |")
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
    ordem = sorted(range(len(cands)), key=lambda i: (-topsis.scores[i], cands[i].lower_tank_vol))
    posicao = {i: k + 1 for k, i in enumerate(ordem)}
    ordinal = {1: "st", 2: "nd", 3: "rd"}
    L = ["| Volume | TOPSIS score | TOPSIS rank | First place in SMAA-VIKOR, b¹ |",
         "| ---: | ---: | ---: | ---: |"]
    for i, c in enumerate(cands):
        p = posicao[i]
        L.append(f"| {n(c.lower_tank_vol, 0)} L | {n(topsis.scores[i], 3)} | {p}{ordinal.get(p, 'th')} "
                 f"| {n(float(smaa.first_rank_probs[i]), 1)}% |")

    # A faixa de escolha de cada método: os volumes a até 5% da amplitude do índice, contados do melhor.
    from triton.core.mcdm_methods import run_promethee, run_vikor
    vikor = run_vikor(cands, weights=None, v_param=0.5)
    promethee = run_promethee(cands, weights=None)
    L += ["", "| Method | Index | Choice band | Best index |", "| :--- | :--- | ---: | ---: |"]
    for metodo, indice, faixa in (
            ("TOPSIS", "closeness score, higher is better", topsis.faixa_de_escolha()),
            ("VIKOR, v = 0.5", "Q, lower is better", vikor.faixa_de_escolha()),
            ("PROMETHEE II, linear preference", "net flow Φ, higher is better", promethee.faixa_de_escolha()),
            ("SMAA-VIKOR, 5,000 weight draws", "first-rank acceptability b¹", smaa.faixa_de_escolha())):
        L.append(f"| {metodo} | {indice} | {faixa_txt(faixa)} | {n(faixa['best_volume_l'], 0)} L |")
    return NL.join(L)


# ── as cidades: o mesmo projeto em Nova York, Londres e Cidade do Cabo ──────────────────────────
CIDADES_GUIA14 = ("NewYork", "London", "CapeTown")
NOMES_CIDADES = {"NewYork": "New York", "London": "London", "CapeTown": "Cape Town"}


def mes_a_mes(serie):
    """Chuva média de cada mês (mm), a partir de 01/01/1991 com o calendário real."""
    from datetime import datetime, timedelta
    d0 = datetime(1991, 1, 1)
    meses = np.zeros(12)
    for i, v in enumerate(serie):
        meses[(d0 + timedelta(days=int(i))).month - 1] += float(v)
    return meses / (len(serie) / 365.25)


def tabela_cidades():
    """Seção 14: o regime de chuva manda mais que a lâmina anual."""
    from triton.core.simulation import run_sweep_simulation

    cfg = _config_tutorial()
    L = ["| City | Annual rain | Days with rain | Ratio between the wettest and the driest month "
         f"| Potential with {vol_br()} | Ideal volume |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **cfg)
        sw = run_sweep_simulation(
            precip_data=serie, lower_tank_max=20000.0, lower_tank_step=1000.0,
            delta_ideal_threshold=1.0, **cfg)
        meses = mes_a_mes(serie)
        razao = meses.max() / max(meses.min(), 0.1)
        L.append(
            f"| {NOMES_CIDADES.get(chave, chave)} | {n(serie.sum() / anos, 0)} mm "
            f"| {n((serie > 0.1).mean() * 100, 0)}% | {n(razao, 1)}× "
            f"| {n(r.potential_potable_savings_pct, 2)}% "
            f"| {n(sw.optimal_lower_tank_vol, 0)} L |")
    return NL.join(L)


#: A legenda de cada tabela gerada. Fica aqui, e não no capítulo, porque é aqui
#: que a tabela nasce; a montagem só lhe acrescenta o número.
LEGENDAS = {
    'cap30_inventario.md': [
        f'Carbon inventory of the final tutorial project, item by item, with the share of each component in the embodied carbon; negative annual values are credits (illustrative grid and water factors, not measured values)',
    ],
    'cap24_metodos.md': [
        'Volumes given by classical sizing rules for the tutorial project, rounded to 250 L, and the potential each one yields in the daily simulation',
        'Storage fraction of the sweep volumes and the simulation time step Fewkes and Butler (2000) recommend for each range',
    ],
    'cap23_entrada.md': [
        'Input data of the ten-day worked case',
        'Precipitation series of the ten days of the worked case (New York, September 2018)',
    ],
    'cap23_dez_dias.md': [
        'Daily water balance of the worked case, day by day, with collection, consumption, overflow and storage',
        'Check of the mass balance closure over the ten days',
        'Indicators of the ten-day worked case',
    ],
    'cap04_serie.md': [
        'Characteristics of the New York precipitation series used in the tutorial',
    ],
    'cap06_primeira_simulacao.md': [
        'Result of the first tutorial simulation, with a 3,000 L tank',
    ],
    'cap07_varredura.md': [
        'Volume sweep of the tutorial project, with the marginal gain of each added cubic metre',
    ],
    'cap07_limiar_e_custo.md': [
        'Ideal volume obtained with each marginal-gain threshold, for the same project',
        f'Cost and performance compared between the ideal volume and the largest volume swept (prices are illustrative, not market prices)',
    ],
    'cap08_reservatorio_superior.md': [
        'Single tank compared with two tanks, keeping the same total storage (energy cost is illustrative, not a market price)',
    ],
    'cap08_limiar.md': [
        'Effect of the pump trigger level on the saving potential and on the number of starts',
    ],
    'cap09_etap.md': [
        'Treatment line by disinfection technology adopted: stages, ultraviolet energy and annual carbon',
        'Fine-filtration recommendation by quality class',
    ],
    'cap10_economico.md': [
        'Make-up of the New York water and sewer bill before and after the rainwater system',
        'Economic indicators of the tutorial project over twenty years of analysis (all costs are illustrative, not market prices)',
    ],
    'cap11_materiais.md': [
        'Net carbon emissions of the tutorial project according to the tank material (prices are illustrative, not market prices)',
        'Effect of the concrete cistern volume on the net carbon emissions',
    ],
    'cap32_decisao.md': [
        'TOPSIS closeness score with the four dimensions weighted equally and first-rank acceptability in SMAA-VIKOR, with 5,000 vectors of eight criterion weights drawn with 25% expected on each dimension, for the tutorial volumes',
        'Choice band of each method for the tutorial volumes: the volumes whose index lies within 5% of the range of the index, counted from the best; TOPSIS, VIKOR and PROMETHEE II with the four dimensions weighted equally',
    ],
    'cap20_sensibilidade.md': [
        'Potential, net present value and payback of the final tutorial project with each assumption varied alone, from the low to the high value (costs are illustrative, not market prices)',
    ],
    'cap28_pressurizadores.md': [
        'Annual energy of six generic pressure pumps (illustrative curves, no brand) in the tutorial direct pressurisation, with the toilet flow limiting the pump flow',
    ],
    'cap12_pesos.md': [
        'TOPSIS choice band (the volumes within 5% of the score range, counted from the highest score) according to the dimension given the dominant weight (70% on it, 10% on each of the other three), with the highest score, the runner-up and the score margin between them',
        'The same with the share of storage efficiency set to zero, so that the technical dimension measures volumetric reliability alone',
        'Declared equal weights and the objective weights the CRITIC method computes from the seven volumes, summed per dimension, with the TOPSIS choice band each gives',
    ],
    'cap12_multicriterio.md': [
        'Multi-criteria decision matrix: the eight criteria of each candidate volume, as the program computes them (costs are illustrative, not market prices)',
        'Winning volume under each dimension taken alone, and the TOPSIS choice band with the four dimensions together',
    ],
    'cap14_cidades.md': [
        'The same tutorial project simulated in New York, London and Cape Town',
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
    """Seção do volume ideal: regras clássicas de dimensionamento contra a simulação diária."""
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
        ("German practical rule", "6% of the smaller of annual supply and demand",
         0.06 * min(oferta_anual_l, demanda_anual_l)),
        ("Rippl, monthly series", "largest accumulated deficit, months", rippl_mensal),
        ("Rippl, daily series", "largest accumulated deficit, days", rippl_diario),
        ("British practical rule", "0.05 × P × A", 0.05 * P * A),
    ]
    L = ["| Method | Rule | Volume | Simulated potential |",
         "| :--- | :--- | ---: | ---: |"]
    for nome, regra, volume in metodos:
        v = round(volume / 250.0) * 250.0
        r = run_single_simulation(precip_data=serie, lower_tank_vol=v, **_config_tutorial())
        L.append(f"| {nome} | {regra} | {n(v, 0)} L | {n(r.potential_potable_savings_pct, 2)}% |")
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **_config_tutorial())
    L.append(f"| **daily simulation, marginal gain of 1 %/m³** | sweep | **{n(VOLUME, 0)} L** "
             f"| **{n(r.potential_potable_savings_pct, 2)}%** |")

    F = ["", "| Volume | Storage fraction S/(A·R) | Time step recommended by Fewkes and Butler |",
         "| ---: | ---: | :--- |"]
    for v in (1, 2, 3, 4, 8, 12, 20):
        fr = v / (A * P / 1000.0)
        passo = "hourly" if fr <= 0.01 else ("daily" if fr <= 0.125 else "monthly")
        F.append(f"| {n(v * 1000, 0)} L | {n(fr, 4)} | {passo} |")
    return NL.join(L + F)


def tabela_inventario():
    """Seção de ciclo de vida: o inventário do projeto fechado, item a item."""
    from triton.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    cfg = _config_ambiental(r)
    cfg.lower_material_key = "PEAD"
    lca = calculate_lca(VOLUME, r.annual_pluvial_consumed_m3, cfg)
    nomes = {
        "Cisterna Inferior": f"{n(VOLUME, 0)} L cistern, polyethylene",
        "Caixa d'Água Superior": "1,000 L upper tank, polyethylene",
        "Motobomba": "two pumps of 0.5 hp",
        "Sistema de Descarte": "first flush: 300 L tank and leaf separator",
        "Consumo Elétrico": "pumping energy",
        "Linha de Tratamento": "tablet chlorination",
        "Água Potável Evitada": "mains water avoided",
    }

    def nome(categoria):
        for chave, rotulo in nomes.items():
            if categoria.startswith(chave):
                return rotulo
        if categoria.startswith("Tubulação"):
            return "PVC pipe, DN " + categoria.split("DN ")[1].split(" ")[0] + " mm"
        return categoria
    total = lca.total_embodied_co2_kg
    L = ["| Item | Embodied | Share of the embodied | Annual |",
         "| :--- | ---: | ---: | ---: |"]
    for it in lca.inventory_items:
        inc = f"{n(it.embodied_co2_kg, 1)} kg" if it.embodied_co2_kg else "—"
        parcela = f"{n(it.embodied_co2_kg / total * 100, 1)}%" if it.embodied_co2_kg else "—"
        anual = f"{n(it.annual_op_co2_kg, 2)} kg/year" if it.annual_op_co2_kg else "—"
        L.append(f"| {nome(it.category)} | {inc} | {parcela} | {anual} |")
    L.append(f"| **total** | **{n(total, 1)} kg** | **100%** "
             f"| **{n(-lca.net_annual_avoided_co2_kg, 2)} kg/year** |")
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


def escrever(nome, conteudo):
    """Grava a tabela nas duas pastas (a em inglês é a que os capítulos incluem)."""
    texto = com_legenda(nome, conteudo) + NL
    for pasta in (SAIDA_EN, SAIDA):
        gravar(os.path.join(pasta, nome), texto)
    print(f"  {os.path.relpath(os.path.join(SAIDA_EN, nome), AQUI)}")


def main():
    tabela, r = tabela_dez_dias()
    escrever("cap23_entrada.md", entrada_dez_dias())
    escrever("cap23_dez_dias.md", tabela)
    print(f"  ten-day potential: {r.potential_potable_savings_pct:.2f}%")

    escrever("cap04_serie.md", tabela_serie())

    tabela_p, r6 = tabela_primeira_simulacao()
    escrever("cap06_primeira_simulacao.md", tabela_p)
    print(f"    first simulation: {r6.potential_potable_savings_pct:.2f}%")

    tabela_v, dados = tabela_varredura()
    escrever("cap07_varredura.md", tabela_v)
    escrever("cap07_limiar_e_custo.md", tabela_limiar_e_custo())

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
        escrever(nome, fn())

    return r


if __name__ == "__main__":
    print("manual tables (International Edition):")
    main()
