# -*- coding: utf-8 -*-
"""O desenho do sistema predial de aproveitamento de água pluvial.

Um corte esquemático da edificação, com os componentes na posição em que de
fato ficam: a cobertura no alto, a cisterna enterrada, a caixa elevada acima do
telhado e os pontos de consumo dentro da casa. O diagrama de caixas da seção 1.1
mostra o **encadeamento**; este mostra a **geometria**, que é o que responde às
perguntas de altura, desnível e posição.

Saída: manual/figuras/fig00d_corte.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
from matplotlib.patches import (                                  # noqa: E402
    Circle, FancyArrowPatch, Polygon, Rectangle,
)

AQUI = Path(__file__).resolve().parent
FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

AZUL = "#2a78d6"
AGUA = "#bcd6f5"
LARANJA = "#eb6834"
VERDE = "#0ca30c"
ROXO = "#7d5fb0"
TINTA = "#0b0b0b"
TINTA2 = "#52514e"
SUPERFICIE = "#fcfcfb"
CINZA = "#8a8880"
TERRA = "#e9e3d6"
PAREDE = "#f5f3ee"
TELHA = "#d7d0c2"
NL = chr(10)


def desenhar():
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.set_xlim(0, 120)
    ax.set_ylim(-2, 80)
    ax.set_aspect("equal")
    ax.axis("off")

    def rotulo(x, y, texto, cor=TINTA2, tamanho=7.4, ha="left", va="center",
               negrito=False):
        ax.text(x, y, texto, ha=ha, va=va, fontsize=tamanho, color=cor,
                zorder=20, linespacing=1.3,
                fontweight="bold" if negrito else "normal")

    # ── terreno ──────────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((0, -2), 120, 22, facecolor=TERRA, edgecolor="none",
                           zorder=1))
    ax.plot([0, 120], [20, 20], color=CINZA, linewidth=1.2, zorder=2)

    # ── chuva ────────────────────────────────────────────────────────────────
    # À direita, sobre o terreno livre: no meio do desenho os traços cruzariam a
    # cota da projeção horizontal e os rótulos da caixa elevada.
    for x in (96, 102, 108, 114):
        ax.plot([x, x - 2.2], [68, 60], color=AZUL, linewidth=1.1, zorder=2)
    rotulo(93, 66, "chuva", AZUL, 8.4, ha="right")

    # ── edificação ───────────────────────────────────────────────────────────
    ax.add_patch(Rectangle((12, 20), 46, 22, facecolor=PAREDE,
                           edgecolor=TINTA2, linewidth=1.3, zorder=3))
    ax.add_patch(Polygon([(8, 42), (35, 56), (62, 42)], closed=True,
                         facecolor=TELHA, edgecolor=TINTA2, linewidth=1.4,
                         zorder=4))
    rotulo(35, 47.5, "cobertura", TINTA, 8.6, ha="center", negrito=True)

    # a cota da projeção horizontal, sob o beiral
    ax.annotate("", xy=(8, 58.5), xytext=(62, 58.5),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=1.1),
                zorder=6)
    # Em duas linhas e afastado da seta: numa linha só, colado nela, o rótulo
    # parecia escrito em cima da cota.
    rotulo(8, 56.6, "captação:" + NL + "projeção horizontal",
           AZUL, 7.0, ha="left", va="top")

    # ── caixa elevada, sobre o telhado ───────────────────────────────────────
    ax.add_patch(Rectangle((26, 62), 17, 8, facecolor="#ffffff",
                           edgecolor=ROXO, linewidth=1.5, zorder=6))
    ax.add_patch(Rectangle((26.3, 62.3), 16.4, 4.6, facecolor=AGUA,
                           edgecolor="none", zorder=7))
    rotulo(34.5, 68.0, "caixa elevada", TINTA, 7.6, ha="center")
    # apoio da caixa
    ax.plot([31, 31], [55.0, 62], color=TINTA2, linewidth=1.0, zorder=5)
    ax.plot([38, 38], [57.5, 62], color=TINTA2, linewidth=1.0, zorder=5)

    # ── calha e condutor, à direita ──────────────────────────────────────────
    ax.add_patch(Rectangle((62, 41.2), 4.0, 2.0, facecolor=AGUA,
                           edgecolor=AZUL, linewidth=1.1, zorder=5))
    rotulo(67.5, 42.2, "calha", TINTA2, 7.4)
    ax.add_patch(Rectangle((63.0, 33), 1.8, 8.4, facecolor=AGUA,
                           edgecolor=AZUL, linewidth=1.1, zorder=5))
    rotulo(66.5, 36.5, "condutor", TINTA2, 7.4)

    # ── descarte de primeiras águas ──────────────────────────────────────────
    ax.add_patch(Rectangle((56.5, 24.0), 17.0, 8.5, facecolor="#fdf0ea",
                           edgecolor=LARANJA, linewidth=1.3, zorder=5))
    rotulo(65, 29.4, "descarte da", LARANJA, 7.0, ha="center")
    rotulo(65, 26.8, "primeira chuva", LARANJA, 7.0, ha="center")

    # ── cisterna enterrada ───────────────────────────────────────────────────
    ax.add_patch(Rectangle((78, 2), 30, 16, facecolor="#ffffff",
                           edgecolor=AZUL, linewidth=1.6, zorder=5))
    ax.add_patch(Rectangle((78.4, 2.4), 29.2, 9.6, facecolor=AGUA,
                           edgecolor="none", zorder=6))
    rotulo(93, 15.0, "cisterna", TINTA, 8.4, ha="center", negrito=True)
    rotulo(93, 6.8, "reservatório inferior", TINTA2, 7.2, ha="center")

    # do descarte para a cisterna
    ax.add_patch(FancyArrowPatch((73.5, 27.0), (84, 18.4), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.5, color=AZUL,
                                 zorder=8, connectionstyle="arc3,rad=-0.25"))
    rotulo(86, 27.0, "o resto da chuva", AZUL, 7.0, ha="left")

    # extravasor
    ax.add_patch(FancyArrowPatch((108, 16.0), (117, 16.0), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.5,
                                 color=LARANJA, zorder=6))
    rotulo(112.5, 18.0, "extravasa", LARANJA, 7.2, ha="center", va="bottom")

    # ── motobomba e recalque ─────────────────────────────────────────────────
    ax.add_patch(Circle((72, 8), 3.0, facecolor="#f1ecf8", edgecolor=ROXO,
                        linewidth=1.5, zorder=7))
    ax.text(72, 8, "M", ha="center", va="center", fontsize=8.4, color=ROXO,
            fontweight="bold", zorder=8)
    rotulo(68, 3.2, "motobomba", ROXO, 7.2, ha="center", va="top")
    # O recalque passa atrás de tudo: acima só do terreno, para continuar
    # visível no trecho enterrado, e abaixo da casa, das caixas e dos rótulos,
    # que ele antes atravessava.
    ATRAS = 1.5
    ax.plot([78, 75], [8, 8], color=ROXO, linewidth=1.7, zorder=ATRAS)

    ax.plot([72, 72], [11, 66], color=ROXO, linewidth=1.7, zorder=ATRAS)
    ax.plot([72, 45], [66, 66], color=ROXO, linewidth=1.7, zorder=ATRAS)
    ax.add_patch(FancyArrowPatch((46, 66), (43.2, 66), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.7, color=ROXO,
                                 zorder=ATRAS))
    rotulo(74, 44, "recalque", ROXO, 7.4)

    # ── pontos de consumo, dentro da casa ────────────────────────────────────
    ax.plot([34, 34], [62, 31], color=VERDE, linewidth=1.6, zorder=5)
    ax.plot([34, 28], [31, 31], color=VERDE, linewidth=1.6, zorder=5)
    ax.add_patch(FancyArrowPatch((29.5, 31), (27.2, 31), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.6, color=VERDE,
                                 zorder=6))
    ax.add_patch(Rectangle((14, 26.5), 13, 9, facecolor="#eefaee",
                           edgecolor=VERDE, linewidth=1.3, zorder=5))
    rotulo(20.5, 32.4, "usos não", VERDE, 7.2, ha="center")
    rotulo(20.5, 29.6, "potáveis", VERDE, 7.2, ha="center")
    rotulo(20.5, 25.4, "bacia, tanque," + NL + "lavagem, rega", TINTA2, 6.6,
           ha="center", va="top")
    rotulo(36, 37.5, "por gravidade", VERDE, 7.0)

    # ── rede pública ─────────────────────────────────────────────────────────
    ax.plot([0, 4], [12, 12], color=CINZA, linewidth=1.9, zorder=4)
    ax.plot([4, 4], [12, 74], color=CINZA, linewidth=1.9, zorder=4)
    ax.plot([4, 34], [74, 74], color=CINZA, linewidth=1.9, zorder=4)
    ax.plot([34, 34], [74, 71.5], color=CINZA, linewidth=1.9, zorder=4)
    ax.add_patch(FancyArrowPatch((34, 72.6), (34, 70.2), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=1.9, color=CINZA,
                                 zorder=5))
    rotulo(1, 9.5, "rede pública", TINTA2, 7.4)
    rotulo(36.5, 74.0, "completa o que a chuva não atendeu", TINTA2, 7.0)

    # ── nota ─────────────────────────────────────────────────────────────────
    ax.text(0, -4.5,
            "A caixa elevada e a motobomba são opcionais: em edificação térrea a "
            "bomba pode pressurizar os pontos de uso" + NL +
            "diretamente. A cisterna pode ser enterrada, apoiada ou elevada, "
            "conforme o terreno e o espaço disponível.",
            ha="left", va="top", fontsize=7.2, color=TINTA2, linespacing=1.5)

    ax.set_title("O sistema predial de aproveitamento de água pluvial, em corte",
                 color=TINTA, fontsize=10.5, loc="left", pad=12)

    caminho = FIGURAS / "fig00d_corte.png"
    fig.savefig(caminho, dpi=170, bbox_inches="tight", facecolor=SUPERFICIE)
    plt.close(fig)
    print("  figuras/fig00d_corte.png")


if __name__ == "__main__":
    print("desenho do sistema:")
    desenhar()
