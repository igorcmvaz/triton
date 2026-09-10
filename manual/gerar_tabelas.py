# -*- coding: utf-8 -*-
"""Gera as tabelas numéricas dos capítulos, rodando o próprio programa.

Nenhum número do manual sai da cabeça de quem escreve. As tabelas deste arquivo
são produzidas executando o Netuno com os dados de entrada declarados, de modo que
uma correção no motor apareça no manual na mesma alteração.

Saída: manual/partes/_tabelas/*.md, incluídos pelos capítulos.
"""

from __future__ import annotations

import os
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
}

VOLUMES_VARREDURA = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000,
                     10000, 12000, 16000, 20000]


def _serie():
    from netuno.core.parser import load_precipitation
    p = load_precipitation(SERIE_TUTORIAL)
    return p[: ANOS_TUTORIAL * 365]


def _config_tutorial():
    t = TUTORIAL
    return dict(
        area=t["area"], runoff_coeff=t["runoff_coeff"],
        discard_mm=t["discard_mm"], discard_mode=t["discard_mode"],
        total_demand_per_day=t["moradores"] * t["per_capita"],
        rainwater_share=t["rainwater_share"],
    )


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
        amb = EnvironmentalConfig()
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


def main():
    tabela, r = tabela_dez_dias()

    caminho = os.path.join(SAIDA, "cap23_entrada.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(entrada_dez_dias() + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    caminho = os.path.join(SAIDA, "cap23_dez_dias.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(tabela + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    print(f"  potencial dos dez dias: {r.potential_potable_savings_pct:.2f}%")

    # ── tabelas do tutorial ──
    for nome, conteudo in (
        ("cap04_serie.md", tabela_serie()),
    ):
        caminho = os.path.join(SAIDA, nome)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo + NL)
        print(f"  {os.path.relpath(caminho, AQUI)}")

    tabela_p, r6 = tabela_primeira_simulacao()
    caminho = os.path.join(SAIDA, "cap06_primeira_simulacao.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(tabela_p + NL)
    print(f"  {os.path.relpath(caminho, AQUI)} — {r6.potential_potable_savings_pct:.2f}%")

    tabela_v, dados = tabela_varredura()
    caminho = os.path.join(SAIDA, "cap07_varredura.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(tabela_v + NL)
    print(f"  {os.path.relpath(caminho, AQUI)} — {len(dados)} volumes")

    caminho = os.path.join(SAIDA, "cap07_limiar_e_custo.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(tabela_limiar_e_custo() + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    return r


if __name__ == "__main__":
    print("tabelas do manual:")
    main()
