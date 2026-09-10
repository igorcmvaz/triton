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
# Capítulo 13 — o balanço diário, dez dias resolvidos
# ──────────────────────────────────────────────────────────────────────────────
#
# O caso didático. Números escolhidos para que o leitor consiga refazer a conta na
# planilha: área redonda, coeficiente usual, demanda redonda, reservatório pequeno
# o bastante para extravasar dentro dos dez dias.

CASO_13 = {
    "area": 100.0,            # m²
    "runoff_coeff": 0.85,     # telha cerâmica
    "discard_mm": 2.0,        # NBR 15527, sem dado local
    "discard_mode": 1,        # todo evento de chuva
    "demanda_total": 200.0,   # L/dia
    "rainwater_share": 0.40,  # 40% da demanda é não potável
    "volume": 2000.0,         # L
}

CHUVA_13 = [0.0, 12.4, 1.6, 0.0, 0.0, 28.0, 5.2, 0.0, 41.0, 0.0]


def tabela_dez_dias():
    r = run_single_simulation(
        precip_data=np.array(CHUVA_13, dtype=float),
        lower_tank_vol=CASO_13["volume"],
        area=CASO_13["area"],
        runoff_coeff=CASO_13["runoff_coeff"],
        discard_mm=CASO_13["discard_mm"],
        discard_mode=CASO_13["discard_mode"],
        total_demand_per_day=CASO_13["demanda_total"],
        rainwater_share=CASO_13["rainwater_share"],
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
    c = CASO_13
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
        "| Chuva | " + " | ".join(br(p) for p in CHUVA_13) + " |",
    ])


def main():
    tabela, r = tabela_dez_dias()

    caminho = os.path.join(SAIDA, "cap13_entrada.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(entrada_dez_dias() + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    caminho = os.path.join(SAIDA, "cap13_dez_dias.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(tabela + NL)
    print(f"  {os.path.relpath(caminho, AQUI)}")

    print(f"  potencial dos dez dias: {r.potential_potable_savings_pct:.2f}%")
    return r


if __name__ == "__main__":
    print("tabelas do manual:")
    main()
