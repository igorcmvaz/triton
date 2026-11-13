# -*- coding: utf-8 -*-
"""Gera as tabelas numéricas dos capítulos da Edição Ibérica, a correr o próprio programa.

Nenhum número do manual sai da cabeça de quem escreve. As tabelas deste ficheiro são produzidas
a executar o Triton com os dados de entrada declarados, de modo que uma correção no motor apareça no
manual na mesma alteração.

Edição Ibérica (IBE): o tutorial é uma moradia em **Lisboa** (chuva do **Iberia01**, ODbL, normal 1986-2015,
município PT-1106, e o tarifário de água e saneamento transcrito em ``triton/data/portugal_tarifarios.json``,
o mesmo de ``examples/portugal/lisboa.triton``); as cidades de comparação são o **Porto** (Iberia01, PT-1312)
e o **Funchal** (reanálise ERA5 de 0,25° das ilhas, ``data/chuva_ilhas_era5.db``, PT-3103, nível C).
Nada do Brasil. Os **custos são ilustrativos**: a edição não traz preços de obra, e os números abaixo
(reservatórios, mão de obra, bomba, energia, cloro, taxas) servem para o leitor ver o método. Cada
tabela com dinheiro diz, na legenda e na linha, que o valor é «ilustrativo, não é preço de mercado».

Saída: as tabelas em português de Portugal, em ``manual/partes/_tabelas/*.md`` (as que os capítulos
incluem). Texto de origem em português de Portugal: não há tradução depois.

Executar a partir da raiz do programa (``TRITON_REGERAR=1`` para sobrescrever tabelas revistas):
    python manual/gerar_tabelas.py
"""

from __future__ import annotations

import os

os.environ["TRITON_EDITION"] = "IBE"

import sys
from functools import lru_cache

import numpy as np

from escrita_segura import gravar  # não desfaz revisão feita à mão

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from triton.core.simulation import run_single_simulation  # noqa: E402

#: Onde as tabelas saem: a pasta que os capítulos incluem.
SAIDA = os.path.join(AQUI, "partes", "_tabelas")
os.makedirs(SAIDA, exist_ok=True)

NL = chr(10)
NBSP = chr(160)
MENOS = "−"

#: Nota que acompanha todo o valor monetário do manual.
ILUSTRATIVO = "ilustrativo, não é preço de mercado"
ILUSTRATIVOS = "ilustrativos, não são preços de mercado"   # para o plural («custos»)


def n(v, casas=1):
    """Número no padrão português: 1 234,5 (espaço inseparável no milhar, sem «-0»)."""
    v = round(float(v), casas)
    if v == 0:
        v = 0.0
    texto = f"{abs(v):,.{casas}f}".replace(",", NBSP).replace(".", ",")
    return (MENOS if v < 0 else "") + texto


br = n  # nome antigo (padrão da edição Brasil), mantido para os geradores de figuras


def eur(v, casas=0):
    """Dinheiro do tutorial, em euros (ilustrativo): 6 250 €, −2 919,90 €."""
    return f"{n(v, casas)}{NBSP}€"


def anos_ou_nunca(x):
    """Período de recuperação em anos, ou «sem recuperação» quando o investimento não se recupera."""
    return n(x, 1) + " anos" if x else "sem recuperação"


# ──────────────────────────────────────────────────────────────────────────────
# Secção 2.1 — o balanço diário, dez dias resolvidos (chuva real de Lisboa)
# ──────────────────────────────────────────────────────────────────────────────
#
# O caso didático: dez dias consecutivos da série de Lisboa (15 a 24 de dezembro de 2013, Iberia01,
# município PT-1106), escolhidos entre os 30 anos porque reúnem, em dez linhas, tudo o que o balanço ensina: o
# primeiro dia com o reservatório vazio, um dia de abastecimento parcial, um dia com chuva abaixo da
# lâmina de descarte (perdido por inteiro), um extravasamento maior do que o próprio reservatório e um
# dia de extravasamento com o reservatório já cheio. Busca determinística: a janela mais recente que
# reúne tudo. Números redondos para a folha de cálculo do leitor (chuva ao décimo de milímetro).

CASO_23 = {
    "area": 100.0,            # m²
    "runoff_coeff": 0.85,     # telha cerâmica
    "discard_mm": 2.0,        # lâmina de descarte, todo o evento
    "discard_mode": 1,
    "demanda_total": 200.0,   # L/dia
    "rainwater_share": 0.40,  # 40% da procura é não potável
    "volume": 2000.0,         # L
    "inicio": "15/12/2013",   # data do primeiro dia, na série de Lisboa
    "dia_na_serie": 10210,    # posição do primeiro dia na série (0 = 01/01/1986)
}

CHUVA_23 = [0.0, 0.6, 2.6, 7.2, 33.9, 3.7, 0.9, 0.1, 4.9, 50.9]


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

    cab = ("| Dia | Chuva | Descarte | Chuva efetiva | Captado | Procura pluvial "
           "| Consumido | Extravasado | No reservatório | Abastecimento |")
    sep = "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |"
    uni = "| | mm | mm | mm | L | L | L | L | L | |"
    linhas = [cab, sep, uni]

    nomes = {2: "pleno", 1: "parcial", 0: "nulo"}
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
        f"| **soma** | | | | **{n(tot_cap, 0)}** | | **{n(tot_con, 0)}** "
        f"| **{n(tot_ext, 0)}** | {n(final, 0)} | |"
    )

    resumo = NL.join([
        "",
        "| Verificação do fecho | Litros |",
        "| :--- | ---: |",
        f"| captado no período | {n(tot_cap, 0)} |",
        f"| menos o extravasado | {MENOS}{n(tot_ext, 0)} |",
        f"| menos o consumido | {MENOS}{n(tot_con, 0)} |",
        f"| menos o que ficou no reservatório | {MENOS}{n(final, 0)} |",
        f"| **resíduo** | **{n(tot_cap - tot_ext - tot_con - final, 0)}** |",
        "",
    ])

    indicadores = NL.join([
        "",
        "| Indicador dos dez dias | Valor |",
        "| :--- | ---: |",
        f"| potencial de poupança de água potável | {n(r.potential_potable_savings_pct)}% |",
        f"| média diária de água pluvial consumida | {n(r.avg_pluvial_consumed_l_day)} L/dia |",
        f"| média diária de água da rede consumida | {n(r.avg_potable_consumed_l_day)} L/dia |",
        f"| média diária extravasada | {n(r.avg_spilled_l_day)} L/dia |",
        f"| dias de abastecimento pleno | {n(r.pct_days_full_satisfaction, 0)}% |",
        f"| dias de abastecimento parcial | {n(r.pct_days_partial_satisfaction, 0)}% |",
        f"| dias de abastecimento nulo | {n(r.pct_days_null_satisfaction, 0)}% |",
        "",
    ])

    return NL.join(linhas) + NL + resumo + indicadores, r


def entrada_dez_dias():
    c = CASO_23
    return NL.join([
        "| Dado de entrada | Valor |",
        "| :--- | ---: |",
        f"| área de captação | {n(c['area'], 0)} m² |",
        f"| coeficiente de escoamento | {n(c['runoff_coeff'], 2)} |",
        f"| lâmina de descarte | {n(c['discard_mm'])} mm, em todo o evento |",
        f"| procura total | {n(c['demanda_total'], 0)} L/dia |",
        f"| fração suprível por água da chuva | {n(c['rainwater_share'] * 100, 0)}% "
        f"= {n(c['demanda_total'] * c['rainwater_share'], 0)} L/dia |",
        f"| volume do reservatório inferior | {n(c['volume'], 0)} L |",
        "| reservatório superior | nenhum |",
        "| chuva | Lisboa, 15 a 24 de dezembro de 2013 (Iberia01, município PT-1106) |",
        "",
        "A série de chuva dos dez dias, em milímetros:",
        "",
        "| Dia | " + " | ".join(str(i) for i in range(1, 11)) + " |",
        "| ---: |" + " ---: |" * 10,
        "| Chuva | " + " | ".join(n(p) for p in CHUVA_23) + " |",
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Parte 2 — o projeto do tutorial: moradia unifamiliar em Lisboa
# ──────────────────────────────────────────────────────────────────────────────
#
# Um projeto só, que cresce ao longo de dez capítulos. A série de Lisboa é longa (30 anos, Iberia01,
# normal 1986-2015), o tarifário da EPAL e da Câmara é público e verificável
# (``examples/LEIA.md``) e a cidade tem um regime mediterrânico (chuva de outono e inverno, verão seco):
# o Porto (atlântico, mais chuvoso) e o Funchal (ilha, com pouca chuva na costa sul) comparam-se com ele.

CHUVAS = os.path.join(RAIZ, "data", "rainfall")
SERIE_TUTORIAL = None            # a série do tutorial vem do Iberia01 (data/chuva_iberia01_p*.db)
ANOS_TUTORIAL = 30
INICIO_DA_SERIE = "01/01/1986"
FIM_DA_SERIE = "31/12/2015"
#: O município de cada cidade do manual na base ibérica (Porto repete-se em Espanha: vale o código).
CODIGO_DA_CIDADE = {"Lisboa": "PT-1106", "Porto": "PT-1312", "Funchal": "PT-3103"}

TUTORIAL = {
    "area": 150.0,             # m² de cobertura, projeção horizontal
    "runoff_coeff": 0.85,      # telha cerâmica
    "discard_mm": 2.0,         # lâmina de descarte
    "discard_mode": 1,         # todo o evento de chuva
    "moradores": 4,
    "per_capita": 150.0,       # L/hab·dia
    # Autoclismos e usos exteriores.
    "rainwater_share": 0.28,
    "volume_inicial": 3000.0,  # o primeiro palpite, do capítulo 6
    # A partir da secção do reservatório superior, o projeto adota elevação para
    # reservatório elevado: é a comparação daquela secção, com o limiar de 100 L.
    "caixa_superior_l": 1000.0,
    "limiar_recalque_l": 100.0,
    # O volume que o tutorial escolhe: ideal pelo ganho marginal de 1 %/m³ (secção 7). Desde a 0.2.0, o
    # multicritério de oito critérios com pesos iguais indica um volume menor; a secção 12 diz o que esta
    # escolha cede.
    "volume": 5000.0,
}

VOLUME = TUTORIAL["volume"]


def vol_br(v=None):
    """Volume em litros com espaço no milhar: 4 000 L."""
    v = VOLUME if v is None else v
    return f"{n(v, 0)} L"


vol_en = vol_br

VOLUMES_VARREDURA = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000,
                     10000, 12000, 16000, 20000]


@lru_cache(maxsize=None)
def _serie_cache(chave):
    from triton.core import base_climatica_iberica as ib
    return ib.carregar_serie(CODIGO_DA_CIDADE[chave], INICIO_DA_SERIE, FIM_DA_SERIE)[0]


def _serie(chave="Lisboa"):
    """A série diária (mm) de 1986-2015 da cidade: Iberia01 (Lisboa, Porto) ou ERA5 de ilha (Funchal)."""
    return _serie_cache(chave)


def _config_tutorial(caixa=False):
    """Parâmetros de simulação do tutorial.

    ``caixa=True`` acrescenta o arranjo adotado na secção do reservatório
    superior; as secções anteriores estudam a cisterna sozinha.
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
    """O projeto do tutorial depois da decisão pelo reservatório superior elevado."""
    return _config_tutorial(caixa=True)


# ── os custos ilustrativos e o tarifário do tutorial, declarados uma vez ─────────────────────────
#
# O tarifário é o de Lisboa (EPAL, água; Câmara Municipal de Lisboa, saneamento e resíduos), transcrito em
# ``triton/data/portugal_tarifarios.json`` (o mesmo de ``examples/portugal/lisboa.triton``). Os custos NÃO
# são preços de mercado: são números redondos, ilustrativos, para o leitor acompanhar o método. A
# edição não traz tabela de preços de obra; o utilizador introduz os dele (etapa 5).

def _tarifa_de_lisboa():
    from triton.core import tarifarios_portugal as tarifas
    from triton.core.edition import configuracao_da_edicao
    cfg = configuracao_da_edicao()
    assert tarifas.aplicar("Lisboa", cfg), "tarifário de Lisboa ausente"
    return cfg


_CFG_LISBOA = _tarifa_de_lisboa()
#: Escalões de água de Lisboa: (início, fim, tarifa, tipo). Nome antigo: ``TARIFA_CASAN``.
TARIFA_TUTORIAL = list(_CFG_LISBOA.water_tariffs)
TARIFA_CASAN = TARIFA_TUTORIAL

CUSTOS_TUTORIAL = dict(
    cost_labor=1500.0, cost_piping=600.0, cost_accessories=800.0,   # €, ilustrativos
    pump_unit_cost=250.0,                                            # € por bomba, ilustrativo
    elec_tariff=0.20,                                                # €/kWh, ilustrativo
    chlorine_cost_per_kg=8.0,                                        # €/kg de produto, ilustrativo
    tma=0.4, inflation=0.2,                                          # % ao mês
    analysis_period_years=20, tariff_escalation=12,
    water_tariff_escalation=3.0, sewage_tariff_escalation=3.0,       # % ao ano, ilustrativos
    elec_tariff_escalation=3.0,
)

#: Manutenção anual do tutorial, € ilustrativos (nome, período em meses, custo fixo, custo por m³).
MANUTENCAO_TUTORIAL = [
    ("Inspeção e limpeza das caleiras e do pré-filtro", 12, 20.0, 0.0),
    ("Limpeza e inspeção da cisterna", 12, 40.0, 0.0),
    ("Manutenção preventiva da bomba", 12, 30.0, 0.0),
]

#: Preço ilustrativo dos reservatórios: ``base + por_litro × volume``, em €. Não é preço de mercado.
PRECO_DO_TANQUE = {
    "PEAD": (100.0, 0.55),
    "CONCRETO": (600.0, 0.40),
    "FIBRA": (120.0, 0.65),
    "ACO_INOX": (300.0, 2.00),
}

#: Fatores ambientais ilustrativos: a edição não traz fator da rede nem da água; o utilizador informa o dele.
FATOR_DA_REDE_KG_KWH = 0.40       # kg CO₂e/kWh, ilustrativo
FATOR_DA_AGUA_KG_M3 = 0.50        # kg CO₂e/m³ de água da rede evitada, ilustrativo


def estimate_tank_price(volume_l, material="PEAD"):
    """Preço ilustrativo do reservatório, em € (substitui o catálogo do programa)."""
    base, por_litro = PRECO_DO_TANQUE[material]
    return base + por_litro * float(volume_l)


def _config_base():
    """A configuração da edição com o tarifário de Lisboa e os custos ilustrativos do tutorial."""
    from triton.core import tarifarios_portugal as tarifas
    from triton.core.edition import configuracao_da_edicao
    cfg = configuracao_da_edicao()
    assert tarifas.aplicar("Lisboa", cfg)
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    cfg.op_costs = list(MANUTENCAO_TUTORIAL)
    # A data do estudo entra no reajuste das tarifas (vigência 01/01/2026): sem fixá-la, os números do manual
    # mudariam a cada dia e o teste que os confere com o programa quebraria na manhã seguinte à geração.
    cfg.data_base_estudo = "31/10/2026"
    return cfg


def _config_economica(volume_l, material="CONCRETO"):
    cfg = _config_base()
    cfg.cost_lower_tank = estimate_tank_price(float(volume_l), material)
    # Elevação para um reservatório superior de 1.000 L em polietileno, com as duas
    # eletrobombas (principal e reserva).
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
    """A configuração ambiental do tutorial, coerente com a económica.

    O descarte físico entra com o carbono incorporado do reservatório de
    descarte e do separador de folhas. Os fatores da rede e da água são
    ilustrativos (a edição não traz o do utilizador). Com o resultado da simulação,
    a energia vem da mesma função que a económica usa.
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


def tabela_serie():
    """Capítulo 4: o que a série de Lisboa tem dentro."""
    serie = _serie()
    anos = len(serie) / 365.25
    chuvosos = serie[serie > 0.1]
    return NL.join([
        "| A série de Lisboa | Valor |",
        "| :--- | ---: |",
        f"| dias na série | {n(len(serie), 0)} |",
        f"| anos | {n(anos, 1)} |",
        f"| precipitação média anual | {n(serie.sum() / anos, 0)} mm |",
        f"| dias com chuva | {n((serie > 0.1).mean() * 100, 0)}% |",
        f"| chuva média nos dias chuvosos | {n(chuvosos.mean(), 1)} mm |",
        f"| maior chuva diária | {n(serie.max(), 1)} mm |",
        f"| dias abaixo da lâmina de descarte | {n(((serie > 0.1) & (serie <= 2.0)).mean() * 100, 0)}% |",
    ])


def tabela_primeira_simulacao():
    """Capítulo 6: o primeiro resultado, com o volume de palpite."""
    r = run_single_simulation(
        precip_data=_serie(), lower_tank_vol=TUTORIAL["volume_inicial"],
        **_config_tutorial())
    dem = TUTORIAL["moradores"] * TUTORIAL["per_capita"]
    return NL.join([
        "| Resultado com " + n(TUTORIAL["volume_inicial"], 0) + " L | Valor |",
        "| :--- | ---: |",
        f"| potencial de poupança de água potável | **{n(r.potential_potable_savings_pct, 2)}%** |",
        f"| água da chuva consumida | {n(r.avg_pluvial_consumed_l_day, 1)} L/dia |",
        f"| água da rede consumida | {n(r.avg_potable_consumed_l_day, 1)} L/dia |",
        f"| água extravasada | {n(r.avg_spilled_l_day, 1)} L/dia |",
        f"| dias de abastecimento pleno | {n(r.pct_days_full_satisfaction, 1)}% |",
        f"| dias de abastecimento parcial | {n(r.pct_days_partial_satisfaction, 1)}% |",
        f"| dias de abastecimento nulo | {n(r.pct_days_null_satisfaction, 1)}% |",
        f"| procura pluvial pretendida | {n(dem * TUTORIAL['rainwater_share'], 0)} L/dia |",
        f"| volume anual poupado | {n(r.annual_pluvial_consumed_m3, 1)} m³/ano |",
    ]), r


def tabela_varredura():
    """Capítulo 7: a curva de retorno decrescente."""
    serie = _serie()
    cfg = _config_tutorial()
    linhas = [
        "| Volume | Potencial | Ganho sobre o anterior | Ganho por metro cúbico acrescentado "
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
            ganho, marginal = n(dp, 2), n(dp / dv, 2)
        linhas.append(
            f"| {n(v, 0)} | {n(r.potential_potable_savings_pct, 2)} | {ganho} "
            f"| {marginal} | {n(r.avg_spilled_l_day, 0)} | {n(r.pct_days_full_satisfaction, 1)} |"
        )
        dados.append((v, r.potential_potable_savings_pct))
        anterior = (v, r.potential_potable_savings_pct)
    return NL.join(linhas), dados


def tabela_limiar_e_custo():
    """Capítulo 7: o limiar decide o volume, e o volume decide o custo."""
    from triton.core.environmental import calculate_lca
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
            f"| {n(limiar, 1)} %/m³ | {n(r.optimal_lower_tank_vol, 0)} L "
            f"| {n(r.optimal_potential_pct, 2)}% |"
        )

    linhas_custo = [
        "",
        f"| | {vol_br()} | {n(20000, 0)} L |",
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
        f"| potencial de poupança | {n(a[0], 2)}% | {n(b[0], 2)}% |",
        f"| preço da cisterna de betão ({ILUSTRATIVO}) | {eur(a[1])} | {eur(b[1])} |",
        f"| massa de betão | {n(a[2], 0)} kg | {n(b[2], 0)} kg |",
        f"| carbono incorporado do sistema | {n(a[3], 0)} kg CO₂e | {n(b[3], 0)} kg CO₂e |",
        f"| **razão de preços** | | **{n(b[1] / a[1], 1)}×** |",
        f"| **ganho de potencial** | | **+{n(b[0] - a[0], 2)} pontos** |",
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
        f"| Mesmo armazenamento de {vol_br(VOLUME + 1000)} | Um só reservatório | {n(VOLUME, 0)} em baixo + 1 000 em cima |",
        "| :--- | ---: | ---: |",
        f"| potencial de poupança | {n(unico.potential_potable_savings_pct, 2)}% "
        f"| {n(duplo.potential_potable_savings_pct, 2)}% |",
        f"| dias de abastecimento pleno | {n(unico.pct_days_full_satisfaction, 1)}% "
        f"| {n(duplo.pct_days_full_satisfaction, 1)}% |",
        f"| volume elevado | — | {n(duplo.total_pumped_liters / anos / 1000, 1)} m³/ano |",
        f"| arranques da bomba | — | {n(duplo.total_pump_cycles / anos, 0)} por ano |",
        f"| horas de bomba | — | {n(e.pump_hours_year, 1)} h/ano |",
        f"| energia | — | {n(e.annual_kwh, 1)} kWh/ano |",
        f"| custo da energia ({ILUSTRATIVO}) | — | {eur(e.annual_kwh * tarifa, 2)}/ano |",
        f"| **diferença de potencial** | | **{n(duplo.potential_potable_savings_pct - unico.potential_potable_savings_pct, 2)} pontos** |",
    ]
    return NL.join(L)


def tabela_limiar_de_acionamento():
    """Capítulo 8: o limiar troca potencial por desgaste da bomba."""
    serie = _serie()
    cfg = _config_tutorial()
    L = ["| Limiar de arranque | Potencial | Arranques por ano |",
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
    (as etapas de desinfeção, a energia e o carbono anual), e a recomendação de filtração fina por classe.
    """
    from triton.core.water_quality import WATER_QUALITY_CLASSES, size_etap

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3

    L = ["| Desinfeção | Etapas | Energia UV anual | CO₂e anual |",
         "| :--- | :---: | ---: | ---: |"]
    nomes = {"cloro": "Cloragem por pastilhas",
             "uv": "Cloragem + ultravioleta",
             "ozonio": "Cloragem + ozonização"}
    for des in ("cloro", "uv", "ozonio"):
        e = size_etap(target_class_id="classe_1", annual_pluvial_consumed_m3=m3,
                      roof_area_m2=150.0, disinfection_choice=des,
                      discard_mm=2.0, include_first_flush=True,
                      grid_co2_factor_kg_kwh=FATOR_DA_REDE_KG_KWH)
        L.append(f"| {nomes[des]} | {len(e.disinfection_stages)} "
                 f"| {n(e.uv_annual_kwh, 1)} kWh "
                 f"| {n(e.total_etap_co2e_kg_yr, 1)} kg |")

    L += ["", "| Classe de destino | Recomenda-se filtração fina? |",
          "| :--- | :---: |"]
    for cid, c in WATER_QUALITY_CLASSES.items():
        L.append(f"| {cid.replace('_', ' ')} "
                 f"| {'sim' if c.exige_filtracao_fina else 'não'} |")
    return NL.join(L)


def _conta(litros_mes, cfg):
    """Fatura mensal de água e saneamento, pelo tarifário do projeto."""
    from triton.core.economic import calculate_water_bill, esgoto_do_projeto
    return calculate_water_bill(
        litros_mes, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
        cfg.water_tax_fixed, cfg.water_tax_var, **esgoto_do_projeto(cfg))


def tabela_economica():
    """Capítulo 10: a fatura de Lisboa, com e sem o sistema."""
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
        "| A fatura de água, saneamento e resíduos de Lisboa | Consumo | Valor |",
        "| :--- | ---: | ---: |",
        f"| sem o sistema | {n(tot_m3, 2)} m³/mês | {eur(sem, 2)} |",
        f"| com o sistema | {n(pot_m3, 2)} m³/mês | {eur(com, 2)} |",
        f"| **poupança** | {n(tot_m3 - pot_m3, 2)} m³/mês | **{eur(sem - com, 2)}** |",
        "",
        f"| Análise a vinte anos (custos {ILUSTRATIVOS}) | Valor |",
        "| :--- | ---: |",
        f"| investimento inicial | {eur(e.capex_total, 2)} |",
        f"| poupança anual na água | {eur(e.annual_water_savings_brl, 2)} |",
        f"| custo anual de exploração | {eur(e.annual_opex_brl, 2)} |",
        f"| valor atual líquido | {eur(e.vpl, 2)} |",
        f"| taxa interna de rentabilidade | {n(e.tir_annual_pct or 0.0, 2)}% ao ano |",
        f"| período de recuperação descontado | {anos_ou_nunca(e.payback_years)} |",
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
    # convenção do gráfico de balanço do separador ambiental do programa.
    L = ["| Material da cisterna | Massa | Carbono incorporado | Retorno do carbono "
         f"| Emissões líquidas em 20 anos | Preço ({ILUSTRATIVO}) |",
         "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    nomes = {"PEAD": "Polietileno (PEAD)", "CONCRETO": "Betão armado",
             "FIBRA": "Fibra de vidro", "ACO_INOX": "Aço inoxidável"}
    for k in MATERIAL_PRESETS:
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        lca = calculate_lca(VOLUME, m3, cfg)
        preco = eur(estimate_tank_price(VOLUME, k)) if k in PRECO_DO_TANQUE else "—"
        L.append(f"| {nomes.get(k, k)} | {n(lca.lower_tank_mass_kg, 0)} kg "
                 f"| {n(lca.total_embodied_co2_kg, 0)} kg CO₂e "
                 f"| {n(lca.environmental_payback_years, 1)} anos "
                 f"| {n(-lca.lifetime_net_co2_saved_kg, 0)} kg | {preco} |")

    L += ["", "| Volume em betão | Retorno do carbono | Emissões líquidas em 20 anos |",
          "| ---: | ---: | ---: |"]
    for v in (2000, 3000, VOLUME, 8000):
        rr = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                   **_config_projeto())
        cfg = _config_ambiental(rr)
        cfg.lower_material_key = "CONCRETO"
        lca = calculate_lca(float(v), rr.annual_pluvial_consumed_m3, cfg)
        L.append(f"| {n(v, 0)} L | {n(lca.environmental_payback_years, 1)} anos "
                 f"| {n(-lca.lifetime_net_co2_saved_kg, 0)} kg CO₂e |")
    return NL.join(L)


#: Os volumes candidatos do multicritério do tutorial (secções 12 e 32), todos em polietileno.
VOLUMES_MULTICRITERIO = (1000, 2000, 3000, 4000, 5000, 8000, 12000)


def candidato_do_tutorial(r, material="PEAD"):
    """A alternativa do multicritério para uma simulação do projeto do tutorial.

    Montada por ``candidato_dos_resultados``, a mesma função que a linha de comandos e a interface
    usam: os oito critérios saem do resultado da simulação, da análise económica e do ciclo de vida.
    A massa a seco vem da calculadora de peso do programa (cisterna do material indicado e o
    reservatório superior de 1 000 L do tutorial).
    """
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import calculate_lca
    from triton.core.system_weight import calculate_system_weight
    from triton.core.topsis import candidato_dos_resultados

    v = float(r.lower_tank_vol)
    e = run_economic_analysis(_config_economica(v, material), r)
    amb = _config_ambiental(r)
    amb.lower_material_key = material
    lca = calculate_lca(v, r.annual_pluvial_consumed_m3, amb)
    massa = calculate_system_weight(v, lower_material_key=material,
                                    upper_tank_vol_l=TUTORIAL["caixa_superior_l"]).total_dry_mass_kg
    return candidato_dos_resultados(r, e, lca.lifetime_net_co2_saved_kg, massa_seca_kg=massa,
                                    upper_tank_vol=TUTORIAL["caixa_superior_l"])


def candidatos_multicriterio(volumes=VOLUMES_MULTICRITERIO, material="PEAD"):
    """As alternativas do multicritério do tutorial, uma por volume."""
    serie = _serie()
    cfg_sim = _config_projeto()
    return [candidato_do_tutorial(run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg_sim),
                                  material)
            for v in volumes]


def tabela_multicriterio():
    """Capítulo 12: os oito critérios de cada volume e o vencedor de cada critério isolado."""
    from triton.core.topsis import calculate_topsis_scores

    cands = candidatos_multicriterio()
    res = calculate_topsis_scores(cands)
    matriz = res.decision_matrix
    linhas = [
        "| Volume | Fiabilidade volumétrica | Eficiência de armazenamento | VAL | LCOW "
        "| Período de recuperação | Emissões líquidas em 20 anos | Massa a seco | Extravasamento |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for c, x in zip(cands, matriz):
        recuperacao = anos_ou_nunca(c.discounted_payback_years)
        linhas.append(
            f"| {n(c.lower_tank_vol, 0)} L | {n(x[0], 1)}% | {n(x[1], 2)}% ao dia | {eur(x[2])} "
            f"| {n(x[3], 2)}{NBSP}€/m³ | {recuperacao} | {n(x[5], 0)} kg CO₂e | {n(x[6], 0)} kg "
            f"| {n(x[7], 1)} m³/ano |")

    global _CANDIDATOS_MULTICRITERIO
    _CANDIDATOS_MULTICRITERIO = cands
    faixa = res.faixa_de_escolha()
    linhas += [
        "",
        "| Critério | Volume |",
        "| :--- | ---: |",
        f"| maior fiabilidade volumétrica | {n(cands[res.technical_best_index].lower_tank_vol, 0)} L |",
        f"| menor período de recuperação descontado, desempate pelo VAL | {n(cands[res.financial_best_index].lower_tank_vol, 0)} L |",
        f"| menores emissões líquidas de carbono | {n(cands[res.environmental_best_index].lower_tank_vol, 0)} L |",
        f"| **compromisso TOPSIS, 25% em cada eixo: faixa de escolha ({_pct_da_tolerancia(faixa)})** "
        f"| **{texto_da_faixa(faixa)}** |",
        f"| maior pontuação TOPSIS, 25% em cada eixo | {n(faixa['best_volume_l'], 0)} L |",
    ]
    return NL.join(linhas)


_CANDIDATOS_MULTICRITERIO = None


def texto_da_faixa(faixa):
    """A faixa de escolha como o manual a escreve: «2 000 a 3 000 L», ou um volume só.

    A faixa vem de ``faixa_de_escolha`` do programa: os volumes cuja pontuação, normalizada entre a pior
    (0) e a melhor (1), fica a até a tolerância da melhor. Quando algum volume avaliado no meio fica fora,
    a faixa não é contígua, e o texto lista os volumes em vez de escrever um intervalo.
    """
    vols = faixa["volumes_l"]
    if len(vols) == 1:
        return f"{n(vols[0], 0)} L"
    if not faixa["contiguous"]:
        return ", ".join(n(v, 0) for v in vols[:-1]) + f" e {n(vols[-1], 0)} L"
    return f"{n(faixa['min_volume_l'], 0)} a {n(faixa['max_volume_l'], 0)} L"


def _pct_da_tolerancia(faixa):
    """«até 5% da amplitude»: a tolerância com que a faixa foi calculada."""
    return f"até {n(100 * faixa['tolerance'], 0)}% da amplitude"


def _pesos_por_eixo(pesos_dos_criterios):
    """Os oito pesos de critério somados nos quatro eixos, pela ordem técnico, económico, ambiental, estrutural."""
    from triton.core.topsis import CRITERION_GROUPS
    eixos = ("technical", "economic", "environmental", "structural")
    return [float(sum(w for w, g in zip(pesos_dos_criterios, CRITERION_GROUPS) if g == e)) for e in eixos]

#: Pesos de eixo (técnico, económico, ambiental, estrutural) da tabela de sensibilidade: os quatro iguais, e
#: 70% no eixo dominante com 10% em cada um dos outros três (os perfis «Priorizar …» da interface).
PESOS_SENSIBILIDADE = (
    ("pesos iguais, 25% em cada eixo", (0.25, 0.25, 0.25, 0.25)),
    ("técnico, 70%", (0.7, 0.1, 0.1, 0.1)),
    ("económico, 70%", (0.1, 0.7, 0.1, 0.1)),
    ("ambiental, 70%", (0.1, 0.1, 0.7, 0.1)),
    ("estrutural, 70%", (0.1, 0.1, 0.1, 0.7)),
)


def tabela_pesos():
    """Capítulo 12: a faixa de escolha do TOPSIS conforme a ponderação.

    As ponderações declaradas (os quatro eixos iguais e o eixo dominante) e, por último, os pesos objetivos
    do CRITIC, calculados dos próprios resultados; o rótulo da linha do CRITIC traz os pesos por eixo que ele
    deu. A faixa usa a tolerância por omissão do programa (5% da amplitude das pontuações).
    """
    from triton.core.topsis import PESOS_CRITIC, calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    critic = calculate_topsis_scores(cands, weights=PESOS_CRITIC)
    t, e, a, s = _pesos_por_eixo(critic.criterion_weights)
    rotulo_critic = (f"pesos objetivos (CRITIC): técnico {n(100 * t, 1)}%, económico {n(100 * e, 1)}%, "
                     f"ambiental {n(100 * a, 1)}%, estrutural {n(100 * s, 1)}%")
    faixa0 = critic.faixa_de_escolha()
    L = [f"| Ponderação | Faixa de escolha ({_pct_da_tolerancia(faixa0)}) | Maior pontuação "
         "| Segundo classificado | Diferença de pontuação |",
         "| :--- | ---: | ---: | ---: | ---: |"]
    for rotulo, pesos in tuple(PESOS_SENSIBILIDADE) + ((rotulo_critic, PESOS_CRITIC),):
        res = critic if pesos == PESOS_CRITIC else calculate_topsis_scores(cands, weights=pesos)
        ordem = sorted(range(len(cands)), key=lambda i: -res.scores[i])
        L.append(f"| {rotulo} | {texto_da_faixa(res.faixa_de_escolha())} "
                 f"| {n(cands[ordem[0]].lower_tank_vol, 0)} L "
                 f"| {n(cands[ordem[1]].lower_tank_vol, 0)} L "
                 f"| {n(res.scores[ordem[0]] - res.scores[ordem[1]], 4)} |")
    return NL.join(L)


#: Pressão de trabalho da comparação de sobrepressores, e a de uma casa mais alta.
PRESSOES_PRESSURIZADOR = (18.0, 24.0)


def _pressurizadores_ilustrativos():
    """Seis sobrepressores **genéricos**, de curvas ilustrativas: sem marca, sem catálogo.

    A edição não traz catálogo de fabricante. Os modelos A a F representam os três tipos de comando
    (pressostato, eletrónico, fluxostato) em duas ou três potências, com curvas simplificadas.
    """
    from triton.core.pressurizer_catalog import ELETRONICO, FLUXOSTATO, PRESSOSTATO, Pressurizador
    return (
        Pressurizador("a", "Modelo A, 0,25 cv", 0.25, PRESSOSTATO, ((0.0, 25.0), (36.0, 0.0)),
                      liga_m=12.0, desliga_m=22.0),
        Pressurizador("b", "Modelo B, 0,33 cv", 1.0 / 3.0, FLUXOSTATO, ((0.0, 20.0), (180.0, 0.0))),
        Pressurizador("c", "Modelo C, 0,5 cv", 0.5, PRESSOSTATO, ((0.0, 40.0), (50.0, 0.0)),
                      liga_m=18.0, desliga_m=28.0),
        Pressurizador("d", "Modelo D, 0,5 cv", 0.5, PRESSOSTATO,
                      ((0.0, 32.0), (12.0, 25.0), (30.0, 16.0), (45.0, 9.0), (52.0, 5.0)),
                      liga_m=15.0),
        Pressurizador("e", "Modelo E, 0,5 cv", 0.5, ELETRONICO,
                      ((0.0, 20.0), (7.0, 18.0), (17.0, 16.0), (27.0, 12.0), (39.0, 6.0), (41.0, 4.0)),
                      retardo_s=10.0),
        Pressurizador("f", "Modelo F, 0,5 cv", 0.5, ELETRONICO, ((0.0, 20.0), (83.0, 7.0))),
    )


def tabela_pressurizadores():
    """Secção 28: seis sobrepressores genéricos no projeto do tutorial."""
    from triton.core.pressurizer_catalog import (
        ELETRONICO, FLUXOSTATO, PRESSOSTATO, VAZAO_DO_PONTO_PADRAO_L_MIN, energia)
    from triton.core.supply_arrangement import DESCARGAS_POR_PESSOA_DIA

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_tutorial())
    v = r.annual_pluvial_consumed_m3
    partidas = TUTORIAL["moradores"] * DESCARGAS_POR_PESSOA_DIA * 365.25
    controle = {PRESSOSTATO: "pressostato", ELETRONICO: "eletrónico", FLUXOSTATO: "fluxostato"}
    h1, h2 = PRESSOES_PRESSURIZADOR
    L = [f"| Modelo | Comando | Caudal da curva a {n(h1, 0)} m de altura manométrica | Horas por ano "
         f"| kWh por ano | kWh/m³ | kWh por ano a {n(h2, 0)} m |",
         "| :--- | :--- | ---: | ---: | ---: | ---: | ---: |"]
    linhas = []
    for p in _pressurizadores_ilustrativos():
        e1 = energia(p, v, h1, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        e2 = energia(p, v, h2, partidas, VAZAO_DO_PONTO_PADRAO_L_MIN)
        linhas.append((e1.kwh_ano, p, e1, e2))
    for _, p, e1, e2 in sorted(linhas, key=lambda x: x[0]):
        a24 = n(e2.kwh_ano, 1) if e2.atende else "não atinge"
        L.append(f"| {p.rotulo} | {controle[p.controle]} | {n(e1.vazao_da_bomba_l_min, 1)} L/min "
                 f"| {n(e1.horas_ano, 0)} | {n(e1.kwh_ano, 1)} | {n(e1.kwh_por_m3, 2)} | {a24} |")
    return NL.join(L), v, partidas


#: Premissas perturbadas na tabela da secção 20: (rótulo, unidade, baixo, provável, alto).
PREMISSAS_SENSIBILIDADE = (
    ("atualização das tarifas de água e saneamento", "% ao ano", 1.0, 3.0, 5.0),
    ("taxa de atualização mínima", "% ao mês", 0.2, 0.4, 0.6),
    ("consumo per capita", "L/hab·dia", 120.0, 150.0, 180.0),
    ("fração suprível", "%", 20.0, 28.0, 40.0),
    ("preço da cisterna", "% do orçamento", 70.0, 100.0, 130.0),
)


def _projeto_fechado(ajuste=None):
    """Potencial, VAL e recuperação do projeto fechado do tutorial, com uma premissa mudada."""
    from triton.core.economic import run_economic_analysis
    cfg_sim = _config_projeto()
    cfg_eco = _config_economica(VOLUME, "PEAD")
    nome, valor = ajuste if ajuste else (None, None)
    if nome == "consumo per capita":
        cfg_sim["total_demand_per_day"] = TUTORIAL["moradores"] * valor
    elif nome == "fração suprível":
        cfg_sim["rainwater_share"] = valor / 100.0
    elif nome == "atualização das tarifas de água e saneamento":
        cfg_eco.water_tariff_escalation = cfg_eco.sewage_tariff_escalation = valor
    elif nome == "taxa de atualização mínima":
        cfg_eco.tma = valor
    elif nome == "preço da cisterna":
        cfg_eco.cost_lower_tank *= valor / 100.0
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **cfg_sim)
    e = run_economic_analysis(cfg_eco, r)
    return r.potential_potable_savings_pct, e.vpl, e.payback_years


def tabela_sensibilidade():
    """Secção 20: cada premissa variada sozinha, no projeto fechado do tutorial."""
    L = ["| Premissa | Baixo | Provável | Alto | Potencial "
         f"| VAL a 20 anos ({ILUSTRATIVO}) | Período de recuperação descontado |",
         "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for rotulo, unidade, baixo, provavel, alto in PREMISSAS_SENSIBILIDADE:
        res = [_projeto_fechado((rotulo, v)) for v in (baixo, alto)]

        pb = anos_ou_nunca
        L.append(
            f"| {rotulo}, {unidade} | {n(baixo, 1)} | {n(provavel, 1)} | {n(alto, 1)} "
            f"| {n(res[0][0], 2)}% a {n(res[1][0], 2)}% "
            f"| {eur(res[0][1])} a {eur(res[1][1])} "
            f"| {pb(res[0][2])} a {pb(res[1][2])} |")
    return NL.join(L)


def tabela_decisao():
    """Secção 32: pontuação TOPSIS e aceitabilidade SMAA de cada volume do tutorial."""
    from triton.core.mcdm_methods import run_smaa_analysis
    from triton.core.topsis import calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    topsis = calculate_topsis_scores(cands)
    smaa = run_smaa_analysis(cands, num_samples=5000, random_seed=42)
    ordem = sorted(range(len(cands)), key=lambda i: -topsis.scores[i])
    posicao = {i: k + 1 for k, i in enumerate(ordem)}
    L = ["| Volume | Pontuação TOPSIS | Posição no TOPSIS | Primeiro lugar no SMAA-VIKOR, b¹ |",
         "| ---: | ---: | ---: | ---: |"]
    for i, c in enumerate(cands):
        p = posicao[i]
        L.append(f"| {n(c.lower_tank_vol, 0)} L | {n(topsis.scores[i], 4)} | {p}.º "
                 f"| {n(float(smaa.first_rank_probs[i]), 1)}% |")
    return NL.join(L)


#: As tolerâncias da tabela que mostra como a faixa de escolha depende da tolerância declarada.
TOLERANCIAS_DA_FAIXA = (0.0, 0.02, 0.05, 0.10, 0.20)


def tabela_faixas():
    """Secção 32: a faixa de escolha de cada método no tutorial, e a do TOPSIS conforme a tolerância.

    Os quatro métodos com os quatro eixos a 25% e partes iguais (o SMAA sorteia os pesos), pela regra do
    programa (``faixa_de_escolha``): a medida de cada método normalizada entre o pior (0) e o melhor (1)
    volume, e os volumes a até 5% do melhor.
    """
    from triton.core.mcdm_methods import run_promethee, run_smaa_analysis, run_vikor
    from triton.core.topsis import calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    topsis = calculate_topsis_scores(cands)
    metodos = (
        ("TOPSIS", "pontuação de proximidade (maior é melhor)", topsis.faixa_de_escolha()),
        ("VIKOR, v = 0,5", "índice Q (menor é melhor)", run_vikor(cands).faixa_de_escolha()),
        ("PROMETHEE II", "fluxo líquido (maior é melhor)", run_promethee(cands).faixa_de_escolha()),
        ("SMAA-VIKOR", "aceitabilidade de primeiro lugar (maior é melhor)",
         run_smaa_analysis(cands, num_samples=5000, random_seed=42).faixa_de_escolha()),
    )
    L = [f"| Método | Medida | Faixa de escolha ({_pct_da_tolerancia(metodos[0][2])}) | Melhor medida |",
         "| :--- | :--- | ---: | ---: |"]
    for nome, medida, faixa in metodos:
        L.append(f"| {nome} | {medida} | {texto_da_faixa(faixa)} | {n(faixa['best_volume_l'], 0)} L |")
    L += ["", "| Tolerância | Faixa do TOPSIS, 25% em cada eixo |", "| ---: | ---: |"]
    for tol in TOLERANCIAS_DA_FAIXA:
        L.append(f"| {n(100 * tol, 0)}% da amplitude | {texto_da_faixa(topsis.faixa_de_escolha(tol))} |")
    return NL.join(L)


def tabela_critic():
    """Secção 32: os pesos objetivos do CRITIC no tutorial, por critério e por eixo, ao lado dos de omissão."""
    from triton.core.topsis import PESOS_CRITIC, calculate_topsis_scores

    if _CANDIDATOS_MULTICRITERIO is None:
        tabela_multicriterio()
    cands = _CANDIDATOS_MULTICRITERIO
    w_critic = calculate_topsis_scores(cands, weights=PESOS_CRITIC).criterion_weights
    w_omissao = calculate_topsis_scores(cands).criterion_weights
    criterios = (("técnico", "fiabilidade volumétrica"), ("técnico", "eficiência de armazenamento"),
                 ("económico", "economia financeira líquida (VAL)"), ("económico", "custo nivelado da água (LCOW)"),
                 ("económico", "período de recuperação descontado"), ("ambiental", "CO₂e de ciclo de vida"),
                 ("estrutural", "massa a seco dos materiais"), ("estrutural", "extravasamento anual"))
    L = ["| Eixo | Critério | Peso pelo CRITIC | Peso por omissão |", "| :--- | :--- | ---: | ---: |"]
    for (eixo, nome), wc, wo in zip(criterios, w_critic, w_omissao):
        L.append(f"| {eixo} | {nome} | {n(100 * wc, 1)}% | {n(100 * wo, 1)}% |")
    L += ["", "| Eixo | Peso pelo CRITIC | Peso por omissão |", "| :--- | ---: | ---: |"]
    for eixo, wc, wo in zip(("técnico", "económico", "ambiental", "estrutural"),
                            _pesos_por_eixo(w_critic), _pesos_por_eixo(w_omissao)):
        L.append(f"| {eixo} | {n(100 * wc, 1)}% | {n(100 * wo, 1)}% |")
    return NL.join(L)


# ── as cidades: o mesmo projeto em Lisboa, no Porto e no Funchal ─────────────────────────────────
CIDADES_GUIA14 = ("Lisboa", "Porto", "Funchal")
NOMES_CIDADES = {"Lisboa": "Lisboa", "Porto": "Porto", "Funchal": "Funchal"}


def mes_a_mes(serie):
    """Chuva média de cada mês (mm), a partir de 01/01/1986 com o calendário real."""
    from datetime import datetime, timedelta
    d0 = datetime(1986, 1, 1)
    meses = np.zeros(12)
    for i, v in enumerate(serie):
        meses[(d0 + timedelta(days=int(i))).month - 1] += float(v)
    return meses / (len(serie) / 365.25)


def tabela_cidades():
    """Secção 14: o regime de chuva manda mais do que a lâmina anual."""
    from triton.core.simulation import run_sweep_simulation

    cfg = _config_tutorial()
    L = ["| Cidade | Chuva anual | Dias com chuva | Razão entre o mês mais e o menos chuvoso "
         f"| Potencial com {vol_br()} | Volume ideal |",
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
    'cap10_custos_estado.md': [
        'O que um projeto novo da Edição Ibérica traz preenchido e o que fica por definir pelo utilizador',
    ],
    'cap10_custos_ilustrativos.md': [
        'Parâmetros ilustrativos do tutorial, que não são preços de mercado, e onde o utilizador os troca pelos seus',
    ],
    'cap10_custos_peso.md': [
        'Efeito das três rotinas de manutenção ilustrativas sobre o custo do resumo e sobre o resultado do tutorial (custos ilustrativos, não são preços de mercado)',
    ],
    'cap10_custos_series_publicas.md': [
        'Séries públicas recolhidas fora do programa, ainda não ligadas a ele, com a data de acesso e o início da soma de verificação',
    ],
    'cap30_inventario.md': [
        'Inventário de carbono do projeto final do tutorial, item a item, com a parcela de cada componente no carbono incorporado; os valores anuais negativos são créditos (fatores da rede e da água ilustrativos, não são valores medidos)',
    ],
    'cap24_metodos.md': [
        'Volumes dados por regras clássicas de dimensionamento para o projeto do tutorial, arredondados a 250 L, e o potencial que cada um produz na simulação diária',
        'Fração de armazenamento dos volumes da varredura e o passo de simulação que Fewkes e Butler (2000) recomendam para cada gama',
    ],
    'cap23_entrada.md': [
        'Dados de entrada do caso resolvido de dez dias',
        'Série de precipitação dos dez dias do caso resolvido (Lisboa, dezembro de 2013)',
    ],
    'cap23_dez_dias.md': [
        'Balanço hídrico diário do caso resolvido, dia a dia, com captação, consumo, extravasamento e armazenamento',
        'Verificação do fecho do balanço de massa nos dez dias',
        'Indicadores do caso resolvido de dez dias',
    ],
    'cap04_serie.md': [
        'Caracterização da série de precipitação de Lisboa adotada no tutorial',
    ],
    'cap06_primeira_simulacao.md': [
        'Resultado da primeira simulação do tutorial, com um reservatório de 3 000 L',
    ],
    'cap07_varredura.md': [
        'Varredura de volumes do projeto do tutorial, com o ganho marginal de cada metro cúbico acrescentado',
    ],
    'cap07_limiar_e_custo.md': [
        'Volume ideal obtido com cada limiar de ganho marginal, para o mesmo projeto',
        'Custo e desempenho comparados entre o volume ideal e o maior volume varrido (os preços são ilustrativos, não são preços de mercado)',
    ],
    'cap08_reservatorio_superior.md': [
        'Reservatório único comparado com dois reservatórios, mantido o mesmo armazenamento total (o custo da energia é ilustrativo, não é preço de mercado)',
    ],
    'cap08_limiar.md': [
        'Efeito do limiar de arranque da bomba no potencial de poupança e no número de arranques',
    ],
    'cap09_etap.md': [
        'Linha de tratamento conforme a tecnologia de desinfeção adotada: etapas, energia ultravioleta e carbono anual',
        'Recomendação de filtração fina por classe de qualidade',
    ],
    'cap10_economico.md': [
        'Composição da fatura de água, saneamento e resíduos de Lisboa antes e depois do sistema pluvial',
        'Indicadores económicos do projeto do tutorial em vinte anos de análise (todos os custos são ilustrativos, não são preços de mercado)',
    ],
    'cap11_materiais.md': [
        'Emissões líquidas de carbono do projeto do tutorial conforme o material do reservatório (os preços são ilustrativos, não são preços de mercado)',
        'Efeito do volume da cisterna de betão nas emissões líquidas de carbono',
    ],
    'cap32_decisao.md': [
        'Pontuação de proximidade TOPSIS com 25% em cada eixo e partes iguais no eixo, e aceitabilidade do primeiro lugar no SMAA-VIKOR, com 5 000 vetores de oito pesos sorteados com 25% esperado em cada eixo, para os volumes do tutorial',
    ],
    'cap32_faixas.md': [
        'Faixa de escolha de cada método no tutorial, com os quatro eixos a 25% e partes iguais no eixo: os volumes cuja medida fica a até 5% da amplitude da melhor, e o volume de melhor medida',
        'Faixa de escolha do TOPSIS no tutorial conforme a tolerância declarada',
    ],
    'cap32_critic.md': [
        'Pesos objetivos do CRITIC calculados dos sete volumes do tutorial, por critério, ao lado dos pesos por omissão (25% em cada eixo, partes iguais no eixo)',
        'Os mesmos pesos somados por eixo',
    ],
    'cap20_sensibilidade.md': [
        'Potencial, valor atual líquido e período de recuperação do projeto final do tutorial com cada premissa variada isoladamente, do valor baixo ao alto (os custos são ilustrativos, não são preços de mercado)',
    ],
    'cap28_pressurizadores.md': [
        'Energia anual de seis sobrepressores genéricos (curvas ilustrativas, sem marca) na pressurização direta do tutorial, com o caudal do autoclismo a limitar o caudal da bomba',
    ],
    'cap12_pesos.md': [
        'Faixa de escolha do TOPSIS conforme a ponderação — os quatro eixos iguais, 70% num eixo e 10% em cada um dos outros três, e os pesos objetivos do CRITIC —, com o volume de maior pontuação, o segundo classificado e a diferença de pontuação entre os dois',
    ],
    'cap12_multicriterio.md': [
        'Matriz de decisão multicritério: os oito critérios de cada volume candidato, em polietileno, com o reservatório superior de 1 000 L (os custos são ilustrativos, não são preços de mercado)',
        'Volume vencedor segundo cada critério isolado, e a faixa de escolha do compromisso TOPSIS (os volumes com pontuação a até 5% da amplitude da maior)',
    ],
    'cap14_cidades.md': [
        'O mesmo projeto do tutorial simulado em Lisboa, no Porto e no Funchal',
    ],
}


def _rippl(deficits):
    """Maior défice acumulado: o volume que o método de Rippl exige."""
    acumulado, maximo = 0.0, 0.0
    for d in deficits:
        acumulado = max(0.0, acumulado + d)
        maximo = max(maximo, acumulado)
    return maximo


def tabela_metodos_empiricos():
    """Secção do volume ideal: regras clássicas de dimensionamento contra a simulação diária."""
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
        ("regra prática alemã", "6% do menor entre a oferta e a procura anuais",
         0.06 * min(oferta_anual_l, demanda_anual_l)),
        ("Rippl, série mensal", "maior défice acumulado, meses", rippl_mensal),
        ("Rippl, série diária", "maior défice acumulado, dias", rippl_diario),
        ("regra prática britânica", "0,05 × P × A", 0.05 * P * A),
    ]
    L = ["| Método | Regra | Volume | Potencial simulado |",
         "| :--- | :--- | ---: | ---: |"]
    for nome, regra, volume in metodos:
        v = round(volume / 250.0) * 250.0
        r = run_single_simulation(precip_data=serie, lower_tank_vol=v, **_config_tutorial())
        L.append(f"| {nome} | {regra} | {n(v, 0)} L | {n(r.potential_potable_savings_pct, 2)}% |")
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **_config_tutorial())
    L.append(f"| **simulação diária, ganho marginal de 1 %/m³** | varredura | **{n(VOLUME, 0)} L** "
             f"| **{n(r.potential_potable_savings_pct, 2)}%** |")

    F = ["", "| Volume | Fração de armazenamento S/(A·R) | Passo de tempo recomendado por Fewkes e Butler |",
         "| ---: | ---: | :--- |"]
    for v in (1, 2, 3, 4, 8, 12, 20):
        fr = v / (A * P / 1000.0)
        passo = "horário" if fr <= 0.01 else ("diário" if fr <= 0.125 else "mensal")
        F.append(f"| {n(v * 1000, 0)} L | {n(fr, 4)} | {passo} |")
    return NL.join(L + F)


def tabela_inventario():
    """Secção de ciclo de vida: o inventário do projeto fechado, item a item."""
    from triton.core.environmental import calculate_lca
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    cfg = _config_ambiental(r)
    cfg.lower_material_key = "PEAD"
    lca = calculate_lca(VOLUME, r.annual_pluvial_consumed_m3, cfg)
    nomes = {
        "Cisterna Inferior": f"cisterna de {n(VOLUME, 0)} L, polietileno",
        "Caixa d'Água Superior": f"reservatório superior de {n(1000, 0)} L, polietileno",
        "Motobomba": "duas eletrobombas de 0,5 cv",
        "Sistema de Descarte": "descarte das primeiras águas: reservatório de 300 L e separador de folhas",
        "Consumo Elétrico": "energia de elevação",
        "Linha de Tratamento": "cloragem por pastilhas",
        "Água Potável Evitada": "água da rede evitada",
    }

    def nome(categoria):
        for chave, rotulo in nomes.items():
            if categoria.startswith(chave):
                return rotulo
        if categoria.startswith("Tubulação"):
            return "tubagem de PVC, DN " + categoria.split("DN ")[1].split(" ")[0] + " mm"
        return categoria
    total = lca.total_embodied_co2_kg
    L = ["| Item | Incorporado | Parcela do incorporado | Anual |",
         "| :--- | ---: | ---: | ---: |"]
    for it in lca.inventory_items:
        inc = f"{n(it.embodied_co2_kg, 1)} kg" if it.embodied_co2_kg else "—"
        parcela = f"{n(it.embodied_co2_kg / total * 100, 1)}%" if it.embodied_co2_kg else "—"
        anual = f"{n(it.annual_op_co2_kg, 2)} kg/ano" if it.annual_op_co2_kg else "—"
        L.append(f"| {nome(it.category)} | {inc} | {parcela} | {anual} |")
    L.append(f"| **total** | **{n(total, 1)} kg** | **100%** "
             f"| **{n(-lca.net_annual_avoided_co2_kg, 2)} kg/ano** |")
    return NL.join(L)


# ──────────────────────────────────────────────────────────────────────────────
# Secção 10 — o que o programa traz de custos na Edição Ibérica (quase nada, de propósito)
# ──────────────────────────────────────────────────────────────────────────────
#
# Nada aqui é digitado: o estado de um projeto novo sai de ``projeto_novo_da_edicao()``, os parâmetros
# ilustrativos do tutorial saem das constantes deste ficheiro e as séries públicas saem dos ficheiros JSON
# que ``coletar_series_publicas.py`` escreve. Para gerar só estas tabelas (sem tocar nas outras, que têm
# legendas revistas à mão):
#     python manual/gerar_tabelas.py custos

NOMES_MATERIAL = {'PEAD': 'polietileno', 'CONCRETO': 'betão', 'FIBRA': 'fibra de vidro', 'ACO_INOX': 'aço inoxidável'}


def _eur2(v):
    return eur(v, 2)


def _descricao_da_base_de_custos(base):
    """O que a base de custos interna traz: só a estrutura (edição neutra) ou preços de origem brasileira."""
    moeda = (base.get("_metadata") or {}).get("currency") or ""
    if not moeda:
        return "só a estrutura, sem preços nem moeda; não é usada nesta edição"
    return f"valores em {'reais' if moeda == 'BRL' else moeda}, de origem brasileira; não são usados nesta edição"


def tabela_custos_estado():
    """O que um projeto novo da edição traz preenchido, e o que fica a zero."""
    import json

    from triton.core.edition import projeto_novo_da_edicao

    cfg = projeto_novo_da_edicao()
    with open(os.path.join(RAIZ, "triton", "data", "costs_database.json"), encoding="utf-8") as f:
        base = json.load(f)
    rotinas = len(cfg.op_costs)
    periodos = sorted({m for _, m, _, _ in cfg.op_costs})
    soma_rotinas = sum(c for _, _, c, _ in cfg.op_costs)
    sim_nao = lambda b: "ligado" if b else "desligado"
    L = ["| Campo do projeto novo | Valor | O que significa |",
         "| :--- | ---: | :--- |",
         f"| cisterna e reservatório superior | {_eur2(cfg.cost_lower_tank + cfg.cost_upper_tank)} | por definir pelo utilizador |",
         f"| tubagem, acessórios e mão de obra | {_eur2(cfg.cost_piping + cfg.cost_accessories + cfg.cost_labor)} | por definir pelo utilizador |",
         f"| preço de cada eletrobomba | {_eur2(cfg.pump_unit_cost)} | por definir; o projeto parte de {cfg.pump_count} eletrobombas, serviço e reserva |",
         f"| tarifa de eletricidade | {n(cfg.elec_tariff, 4)}{NBSP}€/kWh | por definir; sem ela a energia da bomba custa zero |",
         f"| preço do cloro | {n(cfg.chlorine_cost_per_kg, 2)}{NBSP}€/kg | por definir; sem ele o cloro custa zero |",
         f"| rotinas de manutenção | {rotinas} rotinas, periodicidade de {' e '.join(str(m) for m in periodos)} meses, {_eur2(soma_rotinas)} no total | os nomes ficam como roteiro; os custos são do utilizador |",
         f"| orçamento automático do arranjo 3D | {sim_nao(cfg.capex_do_arranjo)} | os preços das peças são em reais, de origem brasileira |",
         f"| mão de obra automática | {sim_nao(cfg.mao_de_obra_automatica)} | idem |",
         f"| preços de catálogo (reservatórios, tratamento) | {sim_nao(cfg.precos_de_catalogo)} | a linha de tratamento é dimensionada, mas não custa nada |",
         f"| base de custos interna (`costs_database.json`) | {len(base['regional_factors_by_uf'])} fatores regionais | {_descricao_da_base_de_custos(base)} |",
         f"| dose de cloro e pureza da pastilha | {n(cfg.chlorine_dose_mg_l, 1)} mg/L e {n(cfg.chlorine_product_purity * 100, 0)}% | parâmetros técnicos, não são preços |",
         f"| tarifário de água, saneamento e resíduos | {cfg.tariff_city_name}, desde {cfg.tariff_vigencia} | **inserido automaticamente**; transcrito dos documentos de 2026 |",
         f"| taxa de atualização | {n(cfg.tma, 1)}% ao mês | valor genérico do núcleo, não é dado de Portugal |",
         f"| inflação dos custos | {n(cfg.inflation, 1)}% ao mês | idem |",
         f"| atualização das tarifas de água, saneamento e eletricidade | {n(cfg.water_tariff_escalation, 1)}%, {n(cfg.sewage_tariff_escalation, 1)}% e {n(cfg.elec_tariff_escalation, 1)}% ao ano | idem |",
         ]
    return NL.join(L)


def tabela_custos_ilustrativos():
    """Os parâmetros ilustrativos do tutorial, com o aviso de que não são preços de mercado."""
    c = CUSTOS_TUTORIAL
    L = ["| Parâmetro do tutorial | Valor ilustrativo | Onde o utilizador o troca |",
         "| :--- | ---: | :--- |",
         f"| mão de obra e escavação | {_eur2(c['cost_labor'])} | CAPEX, mão de obra |",
         f"| tubagem | {_eur2(c['cost_piping'])} | CAPEX, tubagens |",
         f"| acessórios | {_eur2(c['cost_accessories'])} | CAPEX, acessórios |",
         f"| eletrobomba, por unidade | {_eur2(c['pump_unit_cost'])} | eletrobomba e custo de energia |",
         f"| tarifa de eletricidade | {n(c['elec_tariff'], 2)}{NBSP}€/kWh | eletrobomba e custo de energia |",
         f"| cloro, por quilograma de produto | {_eur2(c['chlorine_cost_per_kg'])} | só no ficheiro do projeto |",
         f"| taxa de atualização | {n(c['tma'], 1)}% ao mês | etapa 4 |",
         f"| inflação dos custos | {n(c['inflation'], 1)}% ao mês | etapa 4 |",
         f"| atualização das tarifas | {n(c['water_tariff_escalation'], 1)}% ao ano | etapa 4 |"]
    for nome, meses, fixo, _ in MANUTENCAO_TUTORIAL:
        L.append(f"| rotina: {nome[0].lower() + nome[1:]} | {_eur2(fixo)} a cada {meses} meses | outros custos operacionais |")
    for mat, (base, litro) in PRECO_DO_TANQUE.items():
        L.append(f"| reservatório de {NOMES_MATERIAL[mat]} | {_eur2(base)} mais {n(litro, 2)}{NBSP}€ por litro | só neste manual; o programa não tem esta regra |")
    return NL.join(L)


def _ultimo(serie):
    chave = sorted(serie)[-1]
    return chave, serie[chave]


def tabela_custos_series_publicas():
    """As séries públicas já recolhidas fora do programa, com data de acesso e prova."""
    import json

    pasta = os.environ.get("TRITON_IBE_AUTOMATICOS") or os.path.join(RAIZ, "scripts", "dados", "dados_automaticos")
    necessarios = ("eurostat_eletricidade_domestica", "eurostat_preco_eletricidade_sem_impostos",
                   "eurostat_inflacao_anual", "bce_taxa_refinanciamento")
    if not os.path.isdir(pasta) or not all(os.path.isfile(os.path.join(pasta, x + ".json")) for x in necessarios):
        return None          # as séries recolhidas ficam fora do Git: sem elas a tabela fica como está
    L = ["| Série pública | Portugal | Espanha | Acesso | SHA-256 (início) |",
         "| :--- | ---: | ---: | :--- | :--- |"]
    unidade = {"eurostat_eletricidade_domestica": "€/kWh", "eurostat_preco_eletricidade_sem_impostos": "€/kWh",
               "eurostat_inflacao_anual": "% ao ano"}
    rotulo = {"eurostat_eletricidade_domestica": "eletricidade doméstica, com impostos",
              "eurostat_preco_eletricidade_sem_impostos": "eletricidade doméstica, sem impostos",
              "eurostat_inflacao_anual": "inflação anual (IPCH)"}
    for nome in ("eurostat_eletricidade_domestica", "eurostat_preco_eletricidade_sem_impostos", "eurostat_inflacao_anual"):
        with open(os.path.join(pasta, nome + ".json"), encoding="utf-8") as f:
            d = json.load(f)
        pt, es = _ultimo(d["resumo"]["PT"]), _ultimo(d["resumo"]["ES"])
        casas = 4 if "€" in unidade[nome] else 1
        L.append(f"| {rotulo[nome]} ({pt[0]}) | {n(pt[1], casas)}{NBSP}{unidade[nome]} | {n(es[1], casas)}{NBSP}{unidade[nome]} "
                 f"| {d['acesso'][:10]} | `{d['sha256'][:12]}` |")
    with open(os.path.join(pasta, "bce_taxa_refinanciamento.json"), encoding="utf-8") as f:
        d = json.load(f)
    data, valor = _ultimo(d["resumo"]["U2"])
    L.append(f"| taxa de refinanciamento do BCE ({data}) | {n(valor, 2)}{NBSP}% | zona euro: o mesmo valor | {d['acesso'][:10]} | `{d['sha256'][:12]}` |")
    return NL.join(L)


def tabela_custos_peso():
    """O peso das rotinas de manutenção ilustrativas no resultado do tutorial."""
    from triton.core.economic import run_economic_analysis

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME, **_config_projeto())
    com = _config_economica(VOLUME, "CONCRETO")
    sem = _config_economica(VOLUME, "CONCRETO")
    sem.op_costs = []
    ec, es = run_economic_analysis(com, r), run_economic_analysis(sem, r)
    por_ano = sum(fixo * 12.0 / meses for _, meses, fixo, _ in com.op_costs)
    return NL.join([
        f"| Projeto do tutorial (custos {ILUSTRATIVOS}) | Com as rotinas | Sem rotinas |",
        "| :--- | ---: | ---: |",
        f"| rotinas de manutenção por ano | {_eur2(por_ano)} | {_eur2(0.0)} |",
        f"| custo anual do resumo: energia, cloro e tratamento | {_eur2(ec.annual_opex_brl)} | {_eur2(es.annual_opex_brl)} |",
        f"| valor atual líquido | {_eur2(ec.vpl)} | {_eur2(es.vpl)} |",
    ])


TABELAS_DE_CUSTOS = (
    ("cap10_custos_estado.md", tabela_custos_estado),
    ("cap10_custos_ilustrativos.md", tabela_custos_ilustrativos),
    ("cap10_custos_peso.md", tabela_custos_peso),
    ("cap10_custos_series_publicas.md", tabela_custos_series_publicas),
)


def main_custos():
    """Gera só as tabelas de custos da secção 10 (`python manual/gerar_tabelas.py custos`)."""
    for nome, fn in TABELAS_DE_CUSTOS:
        conteudo = fn()
        if conteudo is None:
            print(f"  {nome}: fonte ausente nesta máquina; tabela mantida como está")
            continue
        escrever(nome, conteudo)


def com_legenda(nome, conteudo):
    """Põe a legenda declarada acima de cada tabela do ficheiro, na ordem."""
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
    """Grava a tabela na pasta que os capítulos incluem."""
    texto = com_legenda(nome, conteudo) + NL
    gravar(os.path.join(SAIDA, nome), texto)
    print(f"  {os.path.relpath(os.path.join(SAIDA, nome), AQUI)}")


def main():
    tabela, r = tabela_dez_dias()
    escrever("cap23_entrada.md", entrada_dez_dias())
    escrever("cap23_dez_dias.md", tabela)
    print(f"  potencial dos dez dias: {r.potential_potable_savings_pct:.2f}%")

    escrever("cap04_serie.md", tabela_serie())

    tabela_p, r6 = tabela_primeira_simulacao()
    escrever("cap06_primeira_simulacao.md", tabela_p)
    print(f"    primeira simulação: {r6.potential_potable_savings_pct:.2f}%")

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
        ("cap32_faixas.md", tabela_faixas),
        ("cap32_critic.md", tabela_critic),
        ("cap14_cidades.md", tabela_cidades),
        ("cap24_metodos.md", tabela_metodos_empiricos),
        ("cap30_inventario.md", tabela_inventario),
    ):
        escrever(nome, fn())

    main_custos()

    return r


if __name__ == "__main__":
    if "custos" in sys.argv[1:]:
        print("tabelas de custos do manual (Edição Ibérica):")
        main_custos()
    else:
        print("tabelas do manual (Edição Ibérica):")
        main()
