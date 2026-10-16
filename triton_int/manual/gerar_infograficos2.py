# -*- coding: utf-8 -*-
"""Segunda leva de infográficos que substituem tabelas.

Mesma disciplina da primeira: cada figura entra no lugar de uma tabela, e não ao
lado dela. Aqui estão as tabelas de faixa — consumo per capita, variação
plausível das premissas, perdas por macrorregião — que se leem muito melhor como
barras de intervalo do que como pares de números separados por «a».

Executar a partir da raiz do programa:
    python manual/gerar_infograficos2.py
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import matplotlib                                                 # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
import numpy as np                                                # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle          # noqa: E402

from gerar_infograficos import (                                  # noqa: E402
    AZUL, CINZA, CLARO, GRADE, LARANJA, NL, ROXO, SUPERFICIE, TINTA, TINTA2,
    VERDE, _cartao, _confinar, _eixos, _gravar, _tela,
)


# ══════════════════════════════════════════════════════════════════════════════
# O consumo per capita de referência, por tipologia
# ══════════════════════════════════════════════════════════════════════════════

def info_per_capita():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    itens = [
        ("hospital", 250, 600, "L/bed·day", ROXO),
        ("hotel", 100, 300, "L/guest·day", LARANJA),
        ("single-family residential", 120, 200, "L/capita·day", AZUL),
        ("multi-family residential", 100, 180, "L/capita·day", AZUL),
        ("office", 50, 80, "L/person·day", VERDE),
        ("school", 10, 50, "L/student·day", VERDE),
        ("commercial / retail", 8, 20, "L/person·day", VERDE),
    ]
    y = np.arange(len(itens))[::-1]
    for i, (nome, a, b, unidade, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.52, color=cor, zorder=3)
        ax.text(b + 12, y[i], f"{a} to {b}  {unidade}", va="center",
                fontsize=8.0, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.6)
    _eixos(ax, "", "", "")
    ax.set_xlabel("benchmark per capita consumption (L per occupancy unit per day)", color=TINTA2, fontsize=9)
    ax.set_xlim(0, 800)
    ax.set_xticks(range(0, 601, 100))

    fig.tight_layout()
    _gravar(fig, "fig38_per_capita.png")


# ══════════════════════════════════════════════════════════════════════════════
# Tipologia, categoria tarifária e unidade de consumo
# ══════════════════════════════════════════════════════════════════════════════

def info_tipologias():
    # Mais alta que a primeira versão: as linhas de cada grupo tinham 6,6
    # unidades para dois rótulos e se encostavam no título do grupo.
    fig, ax = _tela(100, 46, (7.4, 3.6), "")
    grupos = [
        ("RESIDENTIAL", AZUL, [
            ("single-family", "L/capita·day"),
            ("multi-family", "L/capita·day"),
        ]),
        ("PUBLIC", VERDE, [
            ("school", "L/student·day"),
            ("hospital", "L/bed·day"),
        ]),
        ("COMMERCIAL", LARANJA, [
            ("office", "L/person·day"),
            ("hotel", "L/guest·day"),
            ("retail", "L/person·day"),
        ]),
        ("INDUSTRIAL", ROXO, [
            ("industry", "by process"),
        ]),
    ]
    x = 1
    for rotulo, cor, linhas in grupos:
        largura = 23.5
        ax.add_patch(FancyBboxPatch(
            (x, 1), largura, 44, boxstyle="round,pad=0.0,rounding_size=1.0",
            linewidth=1.4, edgecolor=cor, facecolor=CLARO[cor], zorder=3))
        _confinar(ax.text(x + largura / 2.0, 41.6, rotulo, ha="center",
                          va="center", fontsize=8.4, color=cor,
                          fontweight="bold", zorder=5),
                  (x, 39.4, x + largura, 44.2))
        ax.text(x + largura / 2.0, 37.6, "tariff category", ha="center",
                va="center", fontsize=6.8, color=TINTA2, zorder=5)
        for i, (nome, unidade) in enumerate(linhas):
            yy = 25.0 - i * 11.0
            ax.add_patch(FancyBboxPatch(
                (x + 1.5, yy), largura - 3, 9.0,
                boxstyle="round,pad=0.0,rounding_size=0.6", linewidth=1.0,
                edgecolor=cor, facecolor="#ffffff", zorder=4))
            _confinar(ax.text(x + largura / 2.0, yy + 6.0, nome,
                              ha="center", va="center", fontsize=7.4,
                              color=TINTA, zorder=5),
                      (x + 1.5, yy + 4.5, x + largura - 1.5, yy + 9.0))
            _confinar(ax.text(x + largura / 2.0, yy + 2.4, unidade,
                              ha="center", va="center", fontsize=7.0,
                              color=cor, zorder=5),
                      (x + 1.5, yy, x + largura - 1.5, yy + 4.5))
        x += largura + 1.5
    _gravar(fig, "fig39_tipologias.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os quatro modos de modulação
# ══════════════════════════════════════════════════════════════════════════════

def info_modos():
    fig, ax = _tela(100, 30, (7.4, 2.5),
                    "The four demand modulation modes")
    itens = [
        ("constant", "one value", "residential," + NL + "and default mode", CINZA),
        ("weekly", "seven values", "office, retail," + NL + "and school",
         VERDE),
        ("monthly", "twelve values", "hotel, seasonal" + NL + "variation",
         AZUL),
        ("daily", "entire series", "when actual daily" + NL + "metering exists",
         ROXO),
    ]
    for i, (nome, informa, quando, cor) in enumerate(itens):
        x = 1 + i * 25
        ax.add_patch(FancyBboxPatch(
            (x, 2), 23, 25, boxstyle="round,pad=0.0,rounding_size=1.0",
            linewidth=1.4, edgecolor=cor, facecolor=CLARO[cor], zorder=3))
        ax.add_patch(Rectangle((x, 26.1), 23, 0.9, facecolor=cor,
                               edgecolor="none", zorder=4))
        _confinar(ax.text(x + 11.5, 22.5, nome, ha="center", va="center",
                          fontsize=9.0, color=TINTA, fontweight="bold",
                          zorder=5), (x, 20, x + 23, 26))
        _confinar(ax.text(x + 11.5, 17.0, "you enter" + NL + informa,
                          ha="center", va="center", fontsize=7.2, color=cor,
                          zorder=5, linespacing=1.35), (x, 13, x + 23, 20))
        _confinar(ax.text(x + 11.5, 8.0, quando, ha="center", va="center",
                          fontsize=7.2, color=TINTA2, zorder=5,
                          linespacing=1.4), (x, 2, x + 23, 13))
    _gravar(fig, "fig40_modos.png")


# ══════════════════════════════════════════════════════════════════════════════
# A faixa de variação plausível de cada premissa
# ══════════════════════════════════════════════════════════════════════════════

def info_premissas():
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    itens = [
        ("investment (CAPEX)", 15, 30, "spread among quotes", LARANJA),
        ("baseline demand", 15, 25, "literature range", LARANJA),
        ("precipitation", 10, 20, "interannual variation", AZUL),
        ("metered demand", 5, 10, "measured seasonal variation", VERDE),
        ("tariff escalation (%/yr)", 3, 7, "utility track record",
         ROXO),
        ("catchment area", 2, 5, "survey tolerance", VERDE),
    ]
    y = np.arange(len(itens))[::-1]
    for i, (nome, a, b, porque, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.5, color=cor, zorder=3)
        # A faixa em percentual acompanha a barra; a razão fica numa coluna
        # fixa, longe dela. Acompanhando as duas a barra, a faixa mais larga
        # empurrava o seu percentual para cima da própria explicação.
        ax.text(b + 0.7, y[i], f"{a} to {b}%", va="center", fontsize=8.2,
                color=TINTA)
        ax.text(41, y[i], porque, va="center", fontsize=7.4, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.4)
    _eixos(ax, "", "", "")
    ax.set_xlabel("plausible variation around baseline value (%)",
                  color=TINTA2, fontsize=9)
    ax.set_xlim(0, 70)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_ylim(-0.6, len(itens) - 0.4)
    # A régua vai só até 30%: à direita dela fica a coluna da origem da
    # incerteza, e não uma escala.
    ax.spines["bottom"].set_bounds(0, 30)
    ax.grid(axis="x", visible=False)
    for v in (10, 20, 30):
        ax.plot([v, v], [-0.6, len(itens) - 0.4], color=GRADE, linewidth=0.7,
                zorder=0)

    fig.tight_layout()
    _gravar(fig, "fig41_premissas.png")


# fig42_uf (municípios do catálogo brasileiro, por unidade da federação) e
# fig43_perdas (perdas de distribuição por macrorregião do Brasil) não existem na
# edição INT: eram dados do Brasil, e nenhum capítulo em inglês as cita.

# ══════════════════════════════════════════════════════════════════════════════
# Os dois cenários de emissão da base
# ══════════════════════════════════════════════════════════════════════════════

def info_cenarios():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    anos = np.arange(2020, 2101)
    # Trajetórias esquemáticas, e não projeções: a figura mostra a forma de cada
    # cenário, que é o que distingue um do outro na hora de escolher.
    curvas = [

        ("SSP2-4.5", AZUL,
         40 + 8 * np.sin((anos - 2020) / 80.0 * np.pi) - 18 * (anos - 2020) / 80.0,
         "intermediate trajectory," + NL + "near current policies"),
        ("SSP5-8.5", LARANJA, 40 + 85 * ((anos - 2020) / 80.0) ** 1.4,
         "high emissions," + NL + "no effective mitigation"),
    ]
    for nome, cor, y, _ in curvas:
        ax.plot(anos, y, color=cor, linewidth=2.6, zorder=3, label=nome)
        ax.text(2101, y[-1], "  " + nome, color=cor, fontsize=8.6,
                va="center", fontweight="bold")

    ax.axhline(0.0, color=TINTA2, linewidth=1.0, zorder=2)
    ax.text(2021, 2.0, "net-zero emissions", fontsize=7.6, color=TINTA2)

    _eixos(ax, "", "", "global CO₂ emissions (schematic)")
    ax.set_xlim(2020, 2115)
    ax.set_xticks(range(2020, 2101, 20))
    ax.set_yticks([])

    fig.tight_layout()
    _gravar(fig, "fig44_cenarios.png")


# ══════════════════════════════════════════════════════════════════════════════
# As cinco famílias da suíte de verificação
# ══════════════════════════════════════════════════════════════════════════════

#: Coleta do pytest nesta versão (pytest --collect-only), por pasta de tests/.
#: Atualizar junto com a seção de verificação quando a suíte mudar.
SUITE = [
    ("unit tests", "unit", 104, 1269, VERDE),
    ("invariants", "invariants", 11, 175, AZUL),
    ("integration", "integration", 9, 65, AZUL),
    ("graphical UI", "ui", 10, 33, ROXO),
    ("benchmarks against reference results", "benchmarking", 1, 2, LARANJA),
]


def info_suite():
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    y = np.arange(len(SUITE))[::-1]
    for i, (nome, pasta, arquivos, testes, cor) in enumerate(SUITE):
        ax.barh(y[i], testes, height=0.55, color=cor, zorder=3)
        rotulo = (f"{testes:,} tests · "
                  + f"{arquivos} file" + ("s" if arquivos > 1 else ""))
        # A barra longa leva o rótulo por dentro; as curtas, por fora.
        if testes > 500:
            ax.text(testes - 12, y[i], rotulo, va="center", ha="right",
                    fontsize=8.2, color="#ffffff")
        else:
            ax.text(testes + 12, y[i], rotulo, va="center", fontsize=8.2,
                    color=TINTA)

    ax.set_yticks(y)
    ax.set_yticklabels([f"{nome}  (tests/{pasta})" for nome, pasta, *_ in SUITE],
                       fontsize=8.2)
    _eixos(ax, "", "", "")
    ax.set_xlabel("collected test cases", color=TINTA2, fontsize=9)
    ax.set_xlim(0, 1400)
    ax.set_xticks(range(0, 1201, 200))
    ax.set_xticklabels([f"{v:,}" for v in range(0, 1201, 200)])
    ax.grid(axis="y", visible=False)

    fig.tight_layout()
    _gravar(fig, "fig45_suite.png")


# ══════════════════════════════════════════════════════════════════════════════
# A fração atendível, conforme os usos previstos
# ══════════════════════════════════════════════════════════════════════════════

def info_atendivel():
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    itens = [
        ("commercial building:" + NL + "mostly toilets and cleaning", 70, 85,
         ROXO),
        ("all uses except shower," + NL + "kitchen & drinking", 45, 60, CINZA),
        ("with washing machine:" + NL + "expanded non-potable uses", 35, 45, AZUL),
        ("toilets & outdoor area:" + NL + "standard non-potable uses", 25, 35, VERDE),
        ("toilet flushing only", 20, 30, LARANJA),
    ]
    y = np.arange(len(itens))
    for i, (nome, a, b, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.5, color=cor, zorder=3)
        ax.text(b + 1.5, y[i], f"{a} to {b}%", va="center", fontsize=8.6,
                color=TINTA)

    # O valor do tutorial: bacia sanitária e usos externos, sem a máquina de lavar
    ax.axvline(28, color=TINTA2, lw=1.0, ls="--", zorder=4)
    ax.text(27, len(itens) - 0.45, "tutorial, 28%", ha="right", va="bottom",
            fontsize=8.0, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.0)
    ax.set_ylim(-0.6, len(itens) - 0.1)
    _eixos(ax, "", "", "")
    ax.set_xlabel("fraction of total demand meetable by rainwater (%)",
                  color=TINTA2, fontsize=9)
    ax.set_xlim(0, 100)
    ax.grid(axis="y", visible=False)

    fig.tight_layout()
    _gravar(fig, "fig46_atendivel.png")


def main():
    print("infográficos, segunda leva:")
    info_per_capita()
    info_tipologias()
    info_modos()
    info_premissas()
    info_cenarios()
    info_suite()
    info_atendivel()


if __name__ == "__main__":
    main()
