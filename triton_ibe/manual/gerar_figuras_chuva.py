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
os.environ["TRITON_EDITION"] = "IBE"

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

INICIO = datetime(1980, 1, 1)
MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]


def _datas(n):
    return [INICIO + timedelta(days=int(i)) for i in range(n)]


def _serie_da_cidade(chave):
    caminho = RAIZ / "data" / "rainfall" / (chave + ".csv")
    if not caminho.exists():
        caminho = RAIZ.parent / "triton_brl" / "data" / "rainfall" / (chave + ".csv")
    return load_precipitation(str(caminho))[: ANOS_TUTORIAL * 365]


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
            label="passo de 250 L")
    ax.plot(vg, pg, color=LARANJA, linewidth=1.8, marker="o", markersize=7,
            zorder=4, label="passo de 5.000 L")
    for x, y in zip(vg, pg):
        ax.plot([x, x], [0, y], color=LARANJA, linewidth=0.7, linestyle=":",
                zorder=2)

    _eixos(ax, "", "volume do reservatório (m³)", "potencial de poupança (%)")
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_xlim(0, 20)
    ax.set_xticks(range(0, 21, 2))
    ax.set_ylim(0, 50)
    ax.set_yticks(range(0, 51, 10))

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
    a1.text(anos[0], media + 40, f"média: {media:,.0f} mm".replace(",", "."),
            fontsize=8.2, color=TINTA)
    _eixos(a1, "(a)", "", "precipitação anual (mm)")
    a1.set_xlim(anos[0] - 1, anos[-1] + 1)
    teto = teto_multiplo(max(totais) * 1.04, 500.0)
    a1.set_ylim(0, teto)
    a1.set_yticks(np.arange(0, teto + 1, 500))
    a1.set_yticklabels([f"{v:,.0f}".replace(",", ".")
                        for v in np.arange(0, teto + 1, 500)])

    diarios = np.asarray([float(v) for v in serie])
    umidos = diarios[diarios >= 1.0]
    a2.hist(umidos, bins=np.arange(0, 120, 4), color=AZUL, zorder=3)
    a2.set_yscale("log")
    _eixos(a2, "(b)", "precipitação diária em dias húmidos (mm)",
           "número de dias (escala log)")
    a2.set_xlim(0, 120)
    a2.set_xticks(range(0, 121, 20))
    a2.text(0.96, 0.92,
            f"{len(umidos) / len(diarios) * 100:.0f}% dos dias com chuva\n"
            f"máximo: {diarios.max():.0f} mm",
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
    ano = 1995
    dias = [(d, float(v)) for d, v in zip(datas, serie) if d.year == ano]
    x = np.arange(len(dias))
    y = np.asarray([v for _, v in dias])

    fig, ax = plt.subplots(figsize=(7.3, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    ax.bar(x, y, color=AZUL, width=1.0, zorder=3)

    # RX1day — o maior dia do ano
    i_max = int(np.argmax(y))
    ax.annotate(f"RX1day = {y[i_max]:.0f} mm".replace(".", ","),
                xy=(i_max, y[i_max]), xytext=(i_max - 14, y[i_max] * 0.96), ha="right",
                va="center",
                fontsize=8.4, color=ROXO,
                arrowprops=dict(arrowstyle="->", color=ROXO, linewidth=1.0))

    # R20mm — os dias acima de 20 mm
    acima = x[y >= 20.0]
    ax.plot(acima, np.full(len(acima), -2.5), "o", color=LARANJA,
            markersize=3.2, zorder=4)
    ax.text(0.015, 0.82, f"R20mm = {len(acima)} dias",
            transform=ax.transAxes, fontsize=8.4, color=LARANJA, va="top")

    # CDD — a maior sequência seca
    melhor, atual, fim = 0, 0, 0
    for i, v in enumerate(y):
        atual = atual + 1 if v < 1.0 else 0
        if atual > melhor:
            melhor, fim = atual, i
    ax.axvspan(fim - melhor + 1, fim, color=LARANJA, alpha=0.16, zorder=1)
    ax.text((fim - melhor / 2.0), y.max() * 0.55,
            f"CDD = {melhor} dias", ha="center", fontsize=8.4,
            color=LARANJA)

    # PRCPTOT — a soma dos dias úmidos
    ax.text(0.015, 0.93,
            f"PRCPTOT = {y[y >= 1.0].sum():,.0f} mm".replace(",", ".") +
            f"   ·   SDII = {y[y >= 1.0].mean():.1f} mm/dia".replace(".", ","),
            transform=ax.transAxes, fontsize=8.6, color=TINTA, va="top")

    _eixos(ax, "", "dia do ano", "precipitação diária (mm)")
    ax.set_xlim(0, len(x))
    teto = teto_multiplo(y.max() * 1.12, 20.0)
    ax.set_ylim(-teto * 0.08, teto)
    ax.set_yticks(np.arange(0, teto + 1, 20))
    ax.set_xticks([0, 60, 120, 180, 240, 300, 365])

    fig.tight_layout()
    _salvar(fig, "fig16_indices.png")


# ══════════════════════════════════════════════════════════════════════════════
# A sazonalidade separa as capitais mais do que a lâmina anual
# ══════════════════════════════════════════════════════════════════════════════

def figura_sazonalidade():
    dados = []
    for chave in CIDADES_GUIA14:
        serie = _serie_da_cidade(chave)
        mensal = _media_mensal(serie)
        total = mensal.sum()
        si = float(np.sum(np.abs(mensal - total / 12.0)) / total)
        dados.append((NOMES_CIDADES[chave], total, si))

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    # As classes de Walsh e Lawler (1981). Os rótulos ficam à direita das
    # barras, numa margem própria: à esquerda, a primeira barra os cobria.
    faixas = [
        (0.00, 0.20, "muito uniforme", "#eef6ee"),
        (0.20, 0.40, "uniforme, com estação húmida", "#e7f1fb"),
        (0.40, 0.60, "sazonal, estação seca curta", "#fdf6e8"),
        (0.60, 0.80, "sazonal", "#fdf1e8"),
        (0.80, 1.00, "marcadamente sazonal", "#fbe7e0"),
        (1.00, 1.20, "chuva em até 3 meses", "#f8ddd4"),
    ]
    maximo = max(d[2] for d in dados)
    teto = teto_multiplo(maximo * 1.12, 0.2)
    for ini, fim, nome, cor in faixas:
        if ini >= teto:
            continue
        ax.axhspan(ini, min(fim, teto), color=cor, zorder=1)
        ax.text(3.45, (ini + min(fim, teto)) / 2.0, nome, fontsize=7.4,
                color=TINTA2, va="center", ha="left")

    nomes = [d[0] for d in dados]
    ax.bar(range(len(nomes)), [d[2] for d in dados], color=AZUL, width=0.5,
           zorder=3)
    for i, (nome, total, si) in enumerate(dados):
        ax.text(i, si + 0.015, f"{si:.2f}".replace(".", ","), ha="center",
                fontsize=8.6, color=TINTA)

    _eixos(ax, "", "", "índice de sazonalidade SI (adimensional)")
    ax.set_xticks(range(len(nomes)))
    ax.set_xticklabels([f"{d[0]}\n{d[1]:,.0f} mm/ano".replace(",", ".")
                        for d in dados], fontsize=8.2)
    ax.set_xlim(-0.5, 5.3)
    ax.spines["bottom"].set_bounds(-0.5, 3.5)
    ax.set_ylim(0, teto)
    marcas = np.arange(0, teto + 1e-9, 0.2)
    ax.set_yticks(marcas)
    ax.set_yticklabels([f"{v:.1f}".replace(".", ",") for v in marcas])
    ax.grid(axis="x", visible=False)

    fig.tight_layout()
    _salvar(fig, "fig17_sazonalidade.png")


# ══════════════════════════════════════════════════════════════════════════════
# O regime mensal das quatro capitais
# ══════════════════════════════════════════════════════════════════════════════

def figura_capitais():
    fig, eixos = plt.subplots(2, 2, figsize=(7.6, 4.8), sharex=True,
                              sharey=True)
    fig.patch.set_facecolor(SUPERFICIE)

    maximo = 0.0
    series = []
    for chave in CIDADES_GUIA14:
        mensal = _media_mensal(_serie_da_cidade(chave))
        series.append((NOMES_CIDADES[chave], mensal))
        maximo = max(maximo, mensal.max())

    for k, (ax, (nome, mensal)) in enumerate(zip(eixos.ravel(), series)):
        ax.set_facecolor(SUPERFICIE)
        cor = AZUL
        ax.bar(MESES, mensal, color=cor, width=0.68, zorder=3)
        ax.axhline(mensal.mean(), color=TINTA2, linewidth=1.0, linestyle="--",
                   zorder=4)
        _eixos(ax, "(" + "abcd"[k] + ") " + nome, "", "")
        ax.tick_params(labelsize=7.0)
        teto = teto_multiplo(maximo * 1.05, 50.0)
        ax.set_ylim(0, teto)
        ax.set_yticks(np.arange(0, teto + 1, 50))

    eixos[0][0].set_ylabel("precipitação média (mm/mês)", color=TINTA2,
                           fontsize=8.6)
    eixos[1][0].set_ylabel("precipitação média (mm/mês)", color=TINTA2,
                           fontsize=8.6)

    fig.tight_layout()
    _salvar(fig, "fig18_capitais.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os perfis de demanda, e o que cada um faz com o mesmo reservatório
# ══════════════════════════════════════════════════════════════════════════════

PERFIS = {
    "constante": [1.0] * 12,
    "escola": [0.15, 1.15, 1.15, 1.15, 1.15, 1.15,
               0.15, 1.15, 1.15, 1.15, 1.15, 1.15],
    "hotel de praia": [3.0, 3.0, 1.2, 0.6, 0.5, 0.5,
                       0.8, 0.5, 0.5, 0.6, 0.8, 1.0],
}


def _simular_perfil(multiplicadores):
    serie = _serie()
    cfg = dict(_config_tutorial())
    base = cfg.pop("total_demand_per_day")
    m = np.asarray(multiplicadores, dtype=float)
    m = m / m.mean()
    return run_single_simulation(
        precip_data=serie, lower_tank_vol=VOLUME, total_demand_per_day=base,
        monthly_demands=[base * v for v in m], demand_mode="monthly",
        start_date_str="01/01/1980", **cfg), base * m


def figura_modulacao():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    cores = {"constante": TINTA2, "escola": VERDE, "hotel de praia": LARANJA}
    for nome, mult in PERFIS.items():
        m = np.asarray(mult, dtype=float)
        m = m / m.mean()
        ax.plot(MESES, m, color=cores[nome], linewidth=2.2, marker="o",
                markersize=4.5, zorder=3, label=nome)

    ax.axhline(1.0, color=EIXO, linewidth=1.0, zorder=2)
    _eixos(ax, "", "", "procura do mês ÷ procura média anual")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_ylim(0, 3.5)
    ax.set_yticks(np.arange(0, 3.51, 0.5))
    ax.set_yticklabels([f"{v:.1f}".replace(".", ",")
                        for v in np.arange(0, 3.51, 0.5)])

    fig.tight_layout()
    _salvar(fig, "fig19_modulacao.png")


def figura_tipologias():
    mensal_chuva = _media_mensal(_serie())
    resultados = {}
    perfis_l = {}
    for nome, mult in PERFIS.items():
        r, litros = _simular_perfil(mult)
        resultados[nome] = r
        perfis_l[nome] = litros

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.4),
                                 gridspec_kw={"height_ratios": [2.0, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.bar(MESES, mensal_chuva, color="#d6e6fa", width=0.72, zorder=2,
           label="precipitação média")
    eixo_d = a1.twinx()
    eixo_d.set_facecolor("none")
    for nome, cor in (("escola", VERDE), ("hotel de praia", LARANJA)):
        eixo_d.plot(MESES, perfis_l[nome], color=cor, linewidth=2.2,
                    marker="o", markersize=4.5, zorder=4, label=nome)
    eixo_d.set_ylabel("procura do mês (L/dia)", color=TINTA2, fontsize=9)
    eixo_d.tick_params(colors=TINTA2, labelsize=8.5)
    # As duas escalas com o mesmo número de divisões, para que a grade de uma
    # sirva à outra.
    eixo_d.set_ylim(0, 2500)
    eixo_d.set_yticks(range(0, 2501, 500))
    eixo_d.set_yticklabels([f"{v:,}".replace(",", ".") for v in range(0, 2501, 500)])
    for lado in ("top", "left"):
        eixo_d.spines[lado].set_visible(False)
    eixo_d.spines["right"].set_color(EIXO)

    _eixos(a1, "(a)", "", "precipitação média (mm/mês)")
    a1.set_ylim(0, 250)
    a1.set_yticks(range(0, 251, 50))
    linhas, rotulos = eixo_d.get_legend_handles_labels()
    barras, nomes_barras = a1.get_legend_handles_labels()
    linhas, rotulos = barras + linhas, nomes_barras + rotulos
    a1.legend(linhas, rotulos, frameon=False, fontsize=8.5, loc="lower center",
              bbox_to_anchor=(0.5, 1.0), ncol=3)

    nomes = list(PERFIS)
    pots = [resultados[n].potential_potable_savings_pct for n in nomes]
    cores = [TINTA2, VERDE, LARANJA]
    a2.bar(nomes, pots, color=cores, width=0.55, zorder=3)
    for i, p in enumerate(pots):
        a2.text(i, p + 1.5, f"{p:.1f}%".replace(".", ","), ha="center",
                fontsize=9.0, color=TINTA)
    _eixos(a2, "(b)", "", "potencial de poupança (%)")
    a2.set_ylim(0, 50)
    a2.set_yticks(range(0, 51, 10))
    a2.tick_params(axis="x", labelsize=8.0)

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
