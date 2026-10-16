# -*- coding: utf-8 -*-
"""Figuras da chuva e da demanda, todas rodadas do próprio programa.

Sete figuras para o que o manual vinha explicando só em prosa: por que o passo
da varredura importa, o que são trinta anos de série, onde estão os índices
pluviométricos dentro de um ano, como a sazonalidade separa as capitais, e o que
acontece quando a demanda deixa de ser constante.

Executar a partir da raiz do programa:
    python manual/gerar_figuras_chuva.py
"""

from __future__ import annotations

import os
os.environ["TRITON_EDITION"] = "INT"

import sys
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import matplotlib                                                 # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
import numpy as np                                                # noqa: E402

from gerar_figuras import (                                       # noqa: E402
    AZUL, EIXO, LARANJA, ROXO, SUPERFICIE, TINTA, TINTA2, VERDE,
    _eixos, _salvar, teto_multiplo,
)
from gerar_tabelas import (                                       # noqa: E402
    ANOS_TUTORIAL, CIDADES_GUIA14, NOMES_CIDADES, SERIE_TUTORIAL,
    VOLUME, _config_tutorial, _serie,
)

from triton.core.parser import load_precipitation                 # noqa: E402
from triton.core.simulation import (                              # noqa: E402
    run_single_simulation, run_sweep_simulation,
)

# A série de data/rainfall (ERA5) começa em 1 de janeiro de 1991 e tem 10.958 dias, até 2020.
INICIO = datetime(1991, 1, 1)
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _datas(n):
    return [INICIO + timedelta(days=int(i)) for i in range(n)]


def _serie_da_cidade(chave):
    caminho = RAIZ / "data" / "rainfall" / (chave + ".csv")
    if not caminho.exists():
        caminho = RAIZ.parent / "triton_brl" / "data" / "rainfall" / (chave + ".csv")
    return load_precipitation(str(caminho))[: ANOS_TUTORIAL * 365 + 8]


def _media_mensal(serie):
    """Lâmina média de cada mês, em milímetros por mês."""
    meses = np.zeros(12)
    anos = np.zeros(12)
    for i, v in enumerate(serie):
        d = INICIO + timedelta(days=int(i))
        meses[d.month - 1] += float(v)
    anos[:] = len(serie) / 365.25
    return meses / anos


# ══════════════════════════════════════════════════════════════════════════════
# A grade discreta: o passo da varredura decide o que se enxerga
# ══════════════════════════════════════════════════════════════════════════════

def figura_grade():
    serie = _serie()
    cfg = _config_tutorial()

    fina = run_sweep_simulation(precip_data=serie, lower_tank_max=20000.0,
                                lower_tank_step=250.0, **cfg)
    grossa = run_sweep_simulation(precip_data=serie, lower_tank_max=20000.0,
                                  lower_tank_step=5000.0, **cfg)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    vf = [r.lower_tank_vol / 1000.0 for r in fina.results_by_volume]
    pf = [r.potential_potable_savings_pct for r in fina.results_by_volume]
    vg = [r.lower_tank_vol / 1000.0 for r in grossa.results_by_volume]
    pg = [r.potential_potable_savings_pct for r in grossa.results_by_volume]

    ax.plot(vf, pf, color=AZUL, linewidth=2.2, zorder=3,
            label="250 L step")
    ax.plot(vg, pg, color=LARANJA, linewidth=1.8, marker="o", markersize=7,
            zorder=4, label="5,000 L step")
    for x, y in zip(vg, pg):
        ax.plot([x, x], [0, y], color=LARANJA, linewidth=0.7, linestyle=":",
                zorder=2)

    _eixos(ax, "", "tank volume (m³)", "savings potential (%)")
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_xlim(0, 20)
    ax.set_xticks(range(0, 21, 2))
    ax.set_ylim(0, 35)
    ax.set_yticks(range(0, 36, 5))

    fig.tight_layout()
    _salvar(fig, "fig14_grade.png")


# ══════════════════════════════════════════════════════════════════════════════
# Trinta anos de série, e a distribuição diária que os produz
# ══════════════════════════════════════════════════════════════════════════════

def figura_serie():
    serie = _serie()
    datas = _datas(len(serie))
    anos = sorted({d.year for d in datas})
    totais = []
    for ano in anos:
        totais.append(sum(float(v) for v, d in zip(serie, datas)
                          if d.year == ano))

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.8),
                                 gridspec_kw={"height_ratios": [1.25, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    media = float(np.mean(totais))
    cores = [AZUL if t >= media else LARANJA for t in totais]
    a1.bar(anos, totais, color=cores, width=0.72, zorder=3)
    a1.axhline(media, color=TINTA, linewidth=1.2, zorder=4)
    a1.text(0.015, 0.95, f"mean of the series: {media:,.0f} mm/year",
            transform=a1.transAxes, va="top", fontsize=8.2, color=TINTA)
    _eixos(a1, "(a)", "", "annual precipitation (mm)")
    a1.set_xlim(anos[0] - 1, anos[-1] + 1)
    teto = teto_multiplo(max(totais) * 1.04, 500.0)
    a1.set_ylim(0, teto)
    a1.set_yticks(np.arange(0, teto + 1, 500))
    a1.set_yticklabels([f"{v:,.0f}" for v in np.arange(0, teto + 1, 500)])

    diarios = np.asarray([float(v) for v in serie])
    umidos = diarios[diarios >= 1.0]
    a2.hist(umidos, bins=np.arange(0, 120, 4), color=AZUL, zorder=3)
    a2.set_yscale("log")
    _eixos(a2, "(b)", "daily precipitation on wet days (mm)",
           "number of days (log scale)")
    a2.set_xlim(0, 120)
    a2.set_xticks(range(0, 121, 20))
    a2.text(0.96, 0.92,
            f"{len(umidos) / len(diarios) * 100:.0f}% of days with 1 mm or more\n"
            f"maximum: {diarios.max():.0f} mm",
            transform=a2.transAxes, ha="right", va="top", fontsize=8.2,
            color=TINTA2)

    fig.tight_layout()
    _salvar(fig, "fig15_serie.png")


# ══════════════════════════════════════════════════════════════════════════════
# Onde estão os índices dentro de um ano de série
# ══════════════════════════════════════════════════════════════════════════════

def figura_indices():
    serie = _serie()
    datas = _datas(len(serie))
    # O ano do registro cujo total fica mais perto da média de trinta anos: um ano típico.
    totais = {}
    for d, v in zip(datas, serie):
        totais[d.year] = totais.get(d.year, 0.0) + float(v)
    media = sum(totais.values()) / len(totais)
    ano = min(totais, key=lambda a: abs(totais[a] - media))
    dias = [(d, float(v)) for d, v in zip(datas, serie) if d.year == ano]
    x = np.arange(len(dias))
    y = np.asarray([v for _, v in dias])

    fig, ax = plt.subplots(figsize=(7.3, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    ax.bar(x, y, color=AZUL, width=1.0, zorder=3)

    # RX1day — o maior dia do ano
    i_max = int(np.argmax(y))
    ax.annotate(f"RX1day = {y[i_max]:.0f} mm",
                xy=(i_max, y[i_max]), xytext=(i_max - 14, y[i_max] * 0.96), ha="right",
                va="center",
                fontsize=8.4, color=ROXO,
                arrowprops=dict(arrowstyle="->", color=ROXO, linewidth=1.0))

    # R20mm — os dias acima de 20 mm
    acima = x[y >= 20.0]
    ax.plot(acima, np.full(len(acima), -2.5), "o", color=LARANJA,
            markersize=3.2, zorder=4)
    ax.text(0.015, 0.82, f"R20mm = {len(acima)} days",
            transform=ax.transAxes, fontsize=8.4, color=LARANJA, va="top")

    # CDD — a maior sequência seca
    melhor, atual, fim = 0, 0, 0
    for i, v in enumerate(y):
        atual = atual + 1 if v < 1.0 else 0
        if atual > melhor:
            melhor, fim = atual, i
    ax.axvspan(fim - melhor + 1, fim, color=LARANJA, alpha=0.16, zorder=1)
    ax.text((fim - melhor / 2.0), y.max() * 0.55,
            f"CDD = {melhor} days", ha="center", fontsize=8.4,
            color=LARANJA)

    # PRCPTOT — a soma dos dias úmidos
    ax.text(0.015, 0.93,
            f"PRCPTOT = {y[y >= 1.0].sum():,.0f} mm" +
            f"   ·   SDII = {y[y >= 1.0].mean():.1f} mm/day",
            transform=ax.transAxes, fontsize=8.6, color=TINTA, va="top")

    _eixos(ax, "", f"day of the year ({ano})", "daily precipitation (mm)")
    ax.set_xlim(0, len(x))
    teto = teto_multiplo(y.max() * 1.12, 20.0)
    ax.set_ylim(-teto * 0.08, teto)
    ax.set_yticks(np.arange(0, teto + 1, 20))
    ax.set_xticks([0, 60, 120, 180, 240, 300, 365])

    fig.tight_layout()
    _salvar(fig, "fig16_indices.png")


# ══════════════════════════════════════════════════════════════════════════════
# A sazonalidade separa as cidades mais do que a lâmina anual
# ══════════════════════════════════════════════════════════════════════════════

def figura_sazonalidade():
    dados = []
    for chave in CIDADES_GUIA14:
        serie = _serie_da_cidade(chave)
        mensal = _media_mensal(serie)
        total = mensal.sum()
        si = float(np.sum(np.abs(mensal - total / 12.0)) / total)
        dados.append((NOMES_CIDADES[chave], total, si))
    n = len(dados)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    # As classes de Walsh e Lawler (1981). Os rótulos ficam à direita das
    # barras, numa margem própria: à esquerda, a primeira barra os cobria.
    faixas = [
        (0.00, 0.20, "very equable", "#eef6ee"),
        (0.20, 0.40, "equable with a wet season", "#e7f1fb"),
        (0.40, 0.60, "seasonal, short dry season", "#fdf6e8"),
        (0.60, 0.80, "seasonal", "#fdf1e8"),
        (0.80, 1.00, "markedly seasonal", "#fbe7e0"),
        (1.00, 1.20, "rain in ≤ 3 months", "#f8ddd4"),
    ]
    maximo = max(d[2] for d in dados)
    teto = teto_multiplo(maximo * 1.12, 0.2)
    # O fundo cobre a largura das barras e a margem dos rótulos, e só.
    for ini, fim, nome, cor in faixas:
        if ini >= teto:
            continue
        ax.axhspan(ini, min(fim, teto), color=cor, zorder=1)
        ax.text(n - 0.55, (ini + min(fim, teto)) / 2.0, nome, fontsize=7.4,
                color=TINTA2, va="center", ha="left")

    nomes = [d[0] for d in dados]
    ax.bar(range(len(nomes)), [d[2] for d in dados], color=AZUL, width=0.5,
           zorder=3)
    for i, (nome, total, si) in enumerate(dados):
        ax.text(i, si + 0.015, f"{si:.2f}", ha="center",
                fontsize=8.6, color=TINTA)

    _eixos(ax, "", "", "seasonality index SI (dimensionless)")
    ax.set_xticks(range(len(nomes)))
    ax.set_xticklabels([f"{d[0]}\n{d[1]:,.0f} mm/yr"
                        for d in dados], fontsize=8.2)
    ax.set_xlim(-0.5, n + 1.25)
    ax.spines["bottom"].set_bounds(-0.5, n - 0.5)
    ax.set_ylim(0, teto)
    marcas = np.arange(0, teto + 1e-9, 0.2)
    ax.set_yticks(marcas)
    ax.set_yticklabels([f"{v:.1f}" for v in marcas])
    ax.grid(axis="x", visible=False)

    fig.tight_layout()
    _salvar(fig, "fig17_sazonalidade.png")


# ══════════════════════════════════════════════════════════════════════════════
# O regime mensal das três cidades
# ══════════════════════════════════════════════════════════════════════════════

def figura_capitais():
    """O regime mensal de Nova York, Londres e Cidade do Cabo, na mesma escala."""
    fig, eixos = plt.subplots(1, len(CIDADES_GUIA14), figsize=(7.6, 3.3), sharey=True)
    fig.patch.set_facecolor(SUPERFICIE)

    maximo = 0.0
    series = []
    for chave in CIDADES_GUIA14:
        mensal = _media_mensal(_serie_da_cidade(chave))
        series.append((NOMES_CIDADES[chave], mensal))
        maximo = max(maximo, mensal.max())

    iniciais = [m[0] for m in MESES]
    for k, (ax, (nome, mensal)) in enumerate(zip(eixos, series)):
        ax.set_facecolor(SUPERFICIE)
        ax.bar(range(12), mensal, color=AZUL, width=0.68, zorder=3)
        ax.axhline(mensal.mean(), color=TINTA2, linewidth=1.0, linestyle="--",
                   zorder=4)
        _eixos(ax, "(" + "abc"[k] + ") " + nome, "", "")
        ax.set_xticks(range(12))
        ax.set_xticklabels(iniciais)
        ax.tick_params(labelsize=7.6)
        teto = teto_multiplo(maximo * 1.05, 25.0)
        ax.set_ylim(0, teto)
        ax.set_yticks(np.arange(0, teto + 1, 25))

    eixos[0].set_ylabel("mean precipitation (mm/month)", color=TINTA2,
                        fontsize=8.6)

    fig.tight_layout()
    _salvar(fig, "fig18_capitais.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os perfis de demanda, e o que cada um faz com o mesmo reservatório
# ══════════════════════════════════════════════════════════════════════════════

CASOS_DO_MANUAL = AQUI / "casos"
DIAS_DO_MES = np.array([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
DIAS_DA_SEMANA = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _casos_de_demanda():
    """O hotel da Cidade do Cabo e a escola de Londres, lidos dos arquivos de caso do manual.

    Devolve, para cada um, o perfil de demanda total (L/dia), a chuva mensal da cidade do caso e o
    potencial do perfil e da mesma demanda anual espalhada, os dois de ``casos/resultados.json``.
    """
    import json

    from triton.core.parser import load_triton_project

    resultados = json.loads((CASOS_DO_MANUAL / "resultados.json").read_text(encoding="utf-8"))
    hotel = load_triton_project(str(CASOS_DO_MANUAL / "08_hotel_monthly.triton"))
    escola = load_triton_project(str(CASOS_DO_MANUAL / "07_school_weekly.triton"))

    cfg_h, cfg_e = hotel["config"], escola["config"]
    mensal_hotel = np.array(cfg_h.demand_monthly) * np.array(cfg_h.residents_monthly)
    media_hotel = float((mensal_hotel * DIAS_DO_MES).sum() / DIAS_DO_MES.sum())
    semanal_escola = np.array(cfg_e.weekly_demands) * np.array(cfg_e.weekly_residents)
    media_escola = float(semanal_escola.mean())
    return {
        "hotel": dict(nome="Cape Town hotel", cidade="Cape Town", perfil=mensal_hotel, media=media_hotel,
                      chuva=_media_mensal(np.asarray(hotel["precip_data"], dtype=float)),
                      potencial=resultados["08_hotel_monthly.triton"]["potencial_pct"],
                      constante=resultados["08_hotel_monthly.triton"]["potencial_demanda_constante_pct"]),
        "escola": dict(nome="London school", cidade="London", perfil=semanal_escola, media=media_escola,
                       chuva=_media_mensal(np.asarray(escola["precip_data"], dtype=float)),
                       potencial=resultados["07_school_weekly.triton"]["potencial_pct"],
                       constante=resultados["07_school_weekly.triton"]["potencial_demanda_constante_pct"]),
    }


def figura_modulacao():
    """Os perfis de demanda do capítulo 17, cada um dividido pela demanda média (mesmo consumo anual)."""
    casos = _casos_de_demanda()
    hotel, escola = casos["hotel"], casos["escola"]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.6), gridspec_kw={"width_ratios": [12, 7]},
                                 sharey=True)
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.plot(range(12), np.ones(12), color=TINTA2, linewidth=2.0, linestyle="--", zorder=3,
            label="constant")
    a1.plot(range(12), hotel["perfil"] / hotel["media"], color=LARANJA, linewidth=2.2, marker="o",
            markersize=4.5, zorder=4, label="hotel, monthly")
    _eixos(a1, "(a) Cape Town hotel, by month", "", "demand ÷ mean demand")
    a1.set_xticks(range(12))
    a1.set_xticklabels(MESES, fontsize=7.6)
    a1.legend(frameon=False, fontsize=8.2, loc="upper right")

    a2.plot(range(7), np.ones(7), color=TINTA2, linewidth=2.0, linestyle="--", zorder=3,
            label="constant")
    a2.plot(range(7), escola["perfil"] / escola["media"], color=VERDE, linewidth=2.2, marker="o",
            markersize=4.5, zorder=4, label="school, weekly")
    _eixos(a2, "(b) London school, by weekday", "", "")
    a2.set_xticks(range(7))
    a2.set_xticklabels(DIAS_DA_SEMANA, fontsize=7.6)
    a2.legend(frameon=False, fontsize=8.2, loc="upper right")

    a1.set_ylim(0, 2.4)
    a1.set_yticks(np.arange(0, 2.41, 0.5))
    a1.set_yticklabels([f"{v:.1f}" for v in np.arange(0, 2.41, 0.5)])

    fig.tight_layout()
    _salvar(fig, "fig19_modulacao.png")


def figura_tipologias():
    """O perfil contra a chuva da cidade de cada caso, e o que cada perfil rende."""
    casos = _casos_de_demanda()
    hotel, escola = casos["hotel"], casos["escola"]

    fig = plt.figure(figsize=(7.4, 6.0))
    fig.patch.set_facecolor(SUPERFICIE)
    grade = fig.add_gridspec(2, 2, height_ratios=[1.45, 1])
    topo = [fig.add_subplot(grade[0, 0]), fig.add_subplot(grade[0, 1])]
    base = fig.add_subplot(grade[1, :])
    for ax in topo + [base]:
        ax.set_facecolor(SUPERFICIE)

    for ax, caso, cor, titulo, mensal in (
            (topo[0], escola, VERDE, "(a) London school", None),
            (topo[1], hotel, LARANJA, "", hotel["perfil"])):
        ax.bar(range(12), caso["chuva"], color="#d6e6fa", width=0.72, zorder=2,
               label="mean precipitation")
        demanda = np.full(12, caso["media"]) if mensal is None else mensal
        eixo_d = ax.twinx()
        eixo_d.set_facecolor("none")
        eixo_d.plot(range(12), demanda, color=cor, linewidth=2.2, marker="o", markersize=4.0,
                    zorder=4, label=f"demand, {caso['nome']}")
        teto_d = teto_multiplo(max(demanda) * 1.5, 2000.0)
        eixo_d.set_ylim(0, teto_d)
        eixo_d.set_yticks(np.arange(0, teto_d + 1, 2000))
        eixo_d.set_yticklabels([f"{v:,.0f}" for v in np.arange(0, teto_d + 1, 2000)])
        eixo_d.set_ylabel("demand (L/day)", color=TINTA2, fontsize=8.6)
        eixo_d.tick_params(colors=TINTA2, labelsize=8.0)
        for lado in ("top", "left"):
            eixo_d.spines[lado].set_visible(False)
        eixo_d.spines["right"].set_color(EIXO)
        _eixos(ax, titulo, "", "mean precipitation (mm/month)" if ax is topo[0] else "")
        teto_p = teto_multiplo(max(caso["chuva"]) * 1.5, 25.0)
        ax.set_ylim(0, teto_p)
        ax.set_yticks(np.arange(0, teto_p + 1, 25))
        ax.set_xticks(range(12))
        ax.set_xticklabels([m[0] for m in MESES], fontsize=7.6)
        ax.set_zorder(eixo_d.get_zorder() + 1)
        ax.patch.set_visible(False)
        linhas, rotulos = eixo_d.get_legend_handles_labels()
        barras, nomes_barras = ax.get_legend_handles_labels()
        ax.legend(barras + linhas, nomes_barras + rotulos, frameon=False, fontsize=7.6,
                  loc="upper center")

    # (b) o potencial de cada perfil contra a mesma demanda anual espalhada por igual.
    x = np.arange(2)
    largura = 0.26
    base.bar(x - largura / 2.0, [escola["constante"], hotel["constante"]], largura, color=TINTA2,
             zorder=3, label="same annual demand, constant")
    base.bar(x + largura / 2.0, [escola["potencial"], hotel["potencial"]], largura,
             color=[VERDE, LARANJA], zorder=3, label="profile of the case")
    for i, caso in enumerate((escola, hotel)):
        base.text(i - largura / 2.0, caso["constante"] + 0.4, f"{caso['constante']:.2f}", ha="center",
                  fontsize=8.6, color=TINTA)
        base.text(i + largura / 2.0, caso["potencial"] + 0.4, f"{caso['potencial']:.2f}", ha="center",
                  fontsize=8.6, color=TINTA)
    _eixos(base, "(b)", "", "savings potential (%)")
    base.set_xticks(x)
    base.set_xticklabels(["London school (weekly profile)", "Cape Town hotel (monthly profile)"],
                         fontsize=8.6)
    base.set_ylim(0, 16)
    base.set_yticks(range(0, 17, 4))
    base.legend(frameon=False, fontsize=8.2, loc="upper right")
    base.grid(axis="x", visible=False)

    fig.tight_layout()
    _salvar(fig, "fig20_tipologias.png")


def main():
    print("figuras da chuva e da demanda:")
    figura_grade()
    figura_serie()
    figura_indices()
    figura_sazonalidade()
    figura_capitais()
    figura_modulacao()
    figura_tipologias()


if __name__ == "__main__":
    main()
