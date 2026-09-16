# -*- coding: utf-8 -*-
"""Esquemas do manual: geometria, cadeias e camadas.

Cinco desenhos para pontos em que o texto pede do leitor uma construção mental
que o papel pode fazer por ele: a diferença entre a projeção horizontal e a área
inclinada, a sequência de estágios do tratamento, a cadeia de rendimentos que
separa a tomada da água entregue, a decomposição da altura manométrica e as
camadas da verificação do programa.

Saída: manual/figuras/fig00i*.png a fig00m*.png
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
from matplotlib.patches import (                                  # noqa: E402
    FancyArrowPatch, Polygon, Rectangle,
)

from gerar_desenhos import rotulo_de_painel                       # noqa: E402
from gerar_desenhos import (                                      # noqa: E402
    AZUL, CINZA, LARANJA, NL, Prancha, ROXO, TINTA, TINTA2, VERDE,
)

FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)
SUPERFICIE = "#fcfcfb"
AGUA = "#bcd6f5"
TELHA = "#d7d0c2"


def _tela(largura, altura, tamanho, titulo):
    fig, ax = plt.subplots(figsize=tamanho)
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.set_aspect("equal")
    ax.axis("off")
    rotulo_de_painel(ax, titulo)
    return fig, ax


def _gravar(fig, nome):
    fig.savefig(FIGURAS / nome, dpi=170, bbox_inches="tight",
                facecolor=SUPERFICIE)
    plt.close(fig)
    print("  figuras/" + nome)


# ══════════════════════════════════════════════════════════════════════════════
# A área de captação é a projeção horizontal
# ══════════════════════════════════════════════════════════════════════════════

def desenho_projecao():
    fig, ax = _tela(112, 50, (7.4, 3.4), "")

    def rot(x, y, t, cor=TINTA2, tam=7.6, ha="left", va="center", peso="normal"):
        ax.text(x, y, t, ha=ha, va=va, fontsize=tam, color=cor, zorder=8,
                linespacing=1.35, fontweight=peso)

    base_y = 14.0
    # o telhado inclinado
    ax.add_patch(Polygon([(14, base_y + 2), (62, base_y + 26),
                          (62, base_y + 22), (14, base_y - 2)], closed=True,
                         facecolor=TELHA, edgecolor=TINTA2, linewidth=1.3,
                         zorder=4))
    # O rótulo fica à esquerda do telhado, fora da chuva e da rampa: sobre a
    # rampa ele disputava espaço com as setas.
    rot(12.5, base_y, "telhado" + NL + "inclinado" + NL + "A_i", TINTA, 7.8,
        ha="right")

    # a chuva, sempre vertical
    for x in range(18, 63, 8):
        ax.add_patch(FancyArrowPatch((x, 48), (x, 40), arrowstyle="-|>",
                                     mutation_scale=9, linewidth=1.1,
                                     color=AZUL, zorder=3))
    rot(12.5, 44, "precipitação", AZUL, 7.8, ha="right")

    # a projeção horizontal
    ax.plot([14, 62], [8, 8], color=AZUL, linewidth=2.0, zorder=5)
    ax.annotate("", xy=(14, 5), xytext=(62, 5),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=1.2))
    rot(38, 2.6, "projeção horizontal A_h (NBR 10844)", AZUL, 7.6,
        ha="center", va="top")
    for x in (14, 62):
        ax.plot([x, x], [5, base_y + (2 if x == 14 else 22)], color=AZUL,
                linewidth=0.8, linestyle=":", zorder=3)

    # A comparação numérica, num quadro que cobre todas as linhas: a primeira
    # versão tinha o quadro mais estreito que o texto.
    ax.add_patch(Rectangle((70, 7), 41, 34, facecolor="#f4f3f0",
                           edgecolor=CINZA, linewidth=1.2, zorder=3))
    rot(72.5, 37, "Inclinação i = 30%", TINTA, 7.8, peso="bold")
    rot(72.5, 31.5, "θ = arctan i = 16,7°", TINTA2, 7.6)
    rot(72.5, 26.5, "A_h = 100,0 m²", TINTA2, 7.6)
    rot(72.5, 21.5, "A_i = A_h ÷ cos θ = 104,4 m²", TINTA2, 7.6)
    rot(72.5, 14.5, "Superestimativa com A_i:", TINTA2, 7.6)
    rot(72.5, 10.5, "+4,4% em todos os dias", LARANJA, 7.6, peso="bold")

    _gravar(fig, "fig00i_projecao.png")


# ══════════════════════════════════════════════════════════════════════════════
# A linha de tratamento, estágio a estágio
# ══════════════════════════════════════════════════════════════════════════════

def desenho_etap():
    p = Prancha(100, 36, tamanho=(7.4, 2.7))

    p.caixa("bruta", 1, 22, 17, 12, "Água bruta" + NL + "(cisterna)", cor=AZUL,
            peso="bold", tamanho=7.6)
    p.caixa("grade", 21, 22, 17, 12, "1. Gradeamento" + NL + "sólidos" + NL +
            "grosseiros", cor=VERDE, tamanho=7.2)
    p.caixa("sedim", 41, 22, 17, 12, "2. Sedimentação" + NL + "sólidos" + NL +
            "sedimentáveis", cor=VERDE, tamanho=7.2)
    p.caixa("filtro", 61, 22, 17, 12, "3. Filtração" + NL + "turbidez e" + NL +
            "cor aparente", cor=VERDE, tamanho=7.2)
    p.caixa("desinf", 81, 22, 18, 12, "4. Desinfecção" + NL + "cloração" + NL +
            "ou UV", cor=ROXO, tamanho=7.2)
    p.caixa("tratada", 61, 2, 17, 11, "Água tratada" + NL + "ao ponto de uso",
            cor=AZUL, peso="bold", tamanho=7.6)
    p.caixa("lodo", 31, 2, 24, 11, "Material retido" + NL +
            "(remoção na manutenção)", cor=LARANJA, fundo="#fdf0ea",
            tamanho=7.2)

    p.seta("bruta", "d", "grade", "e", cor=AZUL)
    p.seta("grade", "d", "sedim", "e", cor=AZUL)
    p.seta("sedim", "d", "filtro", "e", cor=AZUL)
    p.seta("filtro", "d", "desinf", "e", cor=AZUL)
    p.seta("desinf", "b", "tratada", "d", cor=AZUL, curva=0.25)
    p.seta("sedim", "b", "lodo", "c", cor=LARANJA)
    p.seta("grade", "b", "lodo", "ce", cor=LARANJA, curva=-0.2)
    p.salvar("fig00j_etap.png")


# ══════════════════════════════════════════════════════════════════════════════
# A cadeia de energia do bombeamento
# ══════════════════════════════════════════════════════════════════════════════

def desenho_energia():
    p = Prancha(100, 32, tamanho=(7.4, 2.4))

    p.caixa("tomada", 1, 17, 18, 13, "Potência elétrica" + NL + "P_el" + NL +
            "(medidor, kWh)", cor=LARANJA, peso="bold", tamanho=7.4)
    p.caixa("motor", 23, 17, 18, 13, "Motor elétrico" + NL + "η_m ≈ 60% a 70%",
            cor=ROXO, tamanho=7.4)
    p.caixa("eixo", 45, 17, 18, 13, "Potência no eixo" + NL + "P" + NL +
            "(dado de placa)", cor=ROXO, tamanho=7.4)
    p.caixa("bomba", 67, 17, 15, 13, "Bomba" + NL + "η_b ≈ 50%", cor=AZUL,
            tamanho=7.4)
    p.caixa("agua", 85, 17, 14, 13, "Potência" + NL + "hidráulica" + NL +
            "ρ·g·Q·H_man", cor=AZUL, peso="bold", tamanho=7.4)

    p.seta("tomada", "d", "motor", "e", cor=TINTA2)
    p.seta("motor", "d", "eixo", "e", cor=TINTA2)
    p.seta("eixo", "d", "bomba", "e", cor=TINTA2)
    p.seta("bomba", "d", "agua", "e", cor=TINTA2)

    p.caixa("perda1", 23, 1, 18, 10, "perdas Joule," + NL + "no ferro e atrito",
            cor=CINZA, fundo="#f4f3f0", tinta=TINTA2, tamanho=7.0)
    p.caixa("perda2", 64, 1, 21, 10, "perdas hidráulicas," + NL +
            "volumétricas e mecânicas", cor=CINZA, fundo="#f4f3f0",
            tinta=TINTA2, tamanho=7.0)
    p.seta("motor", "b", "perda1", "c", cor=CINZA, tracejada=True)
    p.seta("bomba", "b", "perda2", "c", cor=CINZA, tracejada=True)
    p.salvar("fig00k_energia.png")


# ══════════════════════════════════════════════════════════════════════════════
# A altura manométrica, decomposta
# ══════════════════════════════════════════════════════════════════════════════

def desenho_manometrica():
    from matplotlib.patches import Circle

    fig, (ax, bx) = plt.subplots(
        2, 1, figsize=(7.4, 7.0), gridspec_kw={"height_ratios": [78, 46]})
    fig.patch.set_facecolor(SUPERFICIE)
    for eixo, altura in ((ax, 78), (bx, 46)):
        eixo.set_facecolor(SUPERFICIE)
        eixo.set_xlim(0, 100)
        eixo.set_ylim(0, altura)
        eixo.set_aspect("equal")
        eixo.axis("off")
    rotulo_de_painel(ax, "(a)")
    rotulo_de_painel(bx, "(b)")

    def rot(eixo, x, y, t, cor=TINTA2, tam=7.6, ha="left", va="center",
            peso="normal"):
        eixo.text(x, y, t, ha=ha, va=va, fontsize=tam, color=cor, zorder=9,
                  linespacing=1.35, fontweight=peso)

    # (a) A instalação: cisterna embaixo, reservatório superior em cima.
    ax.add_patch(Rectangle((6, 4), 26, 13, facecolor="#ffffff",
                           edgecolor=AZUL, linewidth=1.5, zorder=4))
    ax.add_patch(Rectangle((6.3, 4.3), 25.4, 7.0, facecolor=AGUA,
                           edgecolor="none", zorder=5))
    rot(ax, 19, 14, "cisterna", TINTA, 8.0, ha="center", peso="bold")

    ax.add_patch(Rectangle((37, 52), 40, 13, facecolor="#ffffff",
                           edgecolor=ROXO, linewidth=1.5, zorder=4))
    ax.add_patch(Rectangle((37.3, 52.3), 39.4, 7.0, facecolor=AGUA,
                           edgecolor="none", zorder=5))
    rot(ax, 57, 62, "reservatório superior", TINTA, 8.0, ha="center",
        peso="bold")

    ax.plot([19, 19], [11.3, 30], color=ROXO, linewidth=2.0, zorder=3)
    ax.plot([19, 57], [30, 30], color=ROXO, linewidth=2.0, zorder=3)
    ax.plot([57, 57], [30, 52], color=ROXO, linewidth=2.0, zorder=3)
    ax.add_patch(FancyArrowPatch((57, 49), (57, 52.6), arrowstyle="-|>",
                                 mutation_scale=11, linewidth=2.0, color=ROXO,
                                 zorder=4))
    rot(ax, 38, 32, "tubulação de recalque (L, D)", ROXO, 7.4, ha="center",
        va="bottom")

    ax.annotate("", xy=(80, 11.3), xytext=(80, 59.3),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=1.3))
    ax.plot([32, 80], [11.3, 11.3], color=AZUL, linewidth=0.7, linestyle=":")
    ax.plot([77, 82], [59.3, 59.3], color=AZUL, linewidth=0.7, linestyle=":")
    rot(ax, 82, 35.3, "H_geo" + NL + "desnível" + NL + "geométrico", AZUL,
        7.6)

    # A expressão num quadro que a cobre inteira: a primeira versão tinha o
    # quadro mais estreito que o próprio texto.
    ax.add_patch(Rectangle((6, 68), 88, 8, facecolor="#fdf0ea",
                           edgecolor=LARANJA, linewidth=1.2, zorder=3))
    rot(ax, 50, 72, "H_man = H_geo + Σ h_f + Σ h_loc", LARANJA, 9.0,
        ha="center", peso="bold")

    ax.add_patch(Circle((19, 22), 3.4, facecolor="#f1ecf8", edgecolor=ROXO,
                        linewidth=1.5, zorder=6))
    ax.text(19, 22, "M", ha="center", va="center", fontsize=8.4, color=ROXO,
            fontweight="bold", zorder=7)
    rot(ax, 24, 22, "motobomba", ROXO, 7.4)

    # (b) O que é a perda de carga: a linha de energia ao longo de um trecho
    # de tubo com duas singularidades. Declina continuamente pelo atrito e cai
    # em degrau em cada conexão.
    y_tubo = 6.0
    bx.add_patch(Rectangle((6, y_tubo), 84, 4, facecolor="#eaf2fd",
                           edgecolor=AZUL, linewidth=1.3, zorder=3))
    for x, nome in ((36, "registro"), (64, "cotovelo 90°")):
        bx.add_patch(Rectangle((x - 1.6, y_tubo - 1.2), 3.2, 6.4,
                               facecolor="#ffffff", edgecolor=TINTA2,
                               linewidth=1.2, zorder=4))
        rot(bx, x, y_tubo - 2.4, nome, TINTA2, 7.2, ha="center", va="top")
    bx.add_patch(FancyArrowPatch((10, y_tubo + 2), (20, y_tubo + 2),
                                 arrowstyle="-|>", mutation_scale=9,
                                 linewidth=1.1, color=AZUL, zorder=5))
    rot(bx, 22, y_tubo + 2, "Q, v", AZUL, 7.4)

    inclinacao = 0.14
    salto = 6.0
    topo = 40.0
    xs = [6, 36, 36, 64, 64, 90]
    ys = [topo]
    ys.append(ys[-1] - inclinacao * 30)
    ys.append(ys[-1] - salto)
    ys.append(ys[-1] - inclinacao * 28)
    ys.append(ys[-1] - salto)
    ys.append(ys[-1] - inclinacao * 26)
    bx.plot(xs, ys, color=LARANJA, linewidth=2.0, zorder=5)
    bx.plot([6, 94], [topo, topo], color=TINTA2, linewidth=0.8,
            linestyle="--", zorder=2)
    rot(bx, 6, topo + 1.4, "carga total a montante", TINTA2, 7.2, va="bottom")
    rot(bx, 90, ys[-1] - 2.0, "linha de energia", LARANJA, 7.4, ha="right",
        va="top")

    rot(bx, 21, ys[1] - 3.0, "h_f = f · (L/D) · v²/2g", LARANJA, 7.6,
        ha="center", va="top")
    for x_salto, y_alto, y_baixo in ((36, ys[1], ys[2]), (64, ys[3], ys[4])):
        bx.annotate("", xy=(x_salto + 2.2, y_alto), xytext=(x_salto + 2.2,
                                                             y_baixo),
                    arrowprops=dict(arrowstyle="<->", color=ROXO,
                                    linewidth=1.0, shrinkA=0, shrinkB=0))
    rot(bx, 62, ys[3] - 2.2, "h_loc = K · v²/2g", ROXO, 7.6, ha="right",
        va="top")
    bx.annotate("", xy=(94, topo), xytext=(94, ys[-1]),
                arrowprops=dict(arrowstyle="<->", color=TINTA, linewidth=1.1))
    rot(bx, 92.5, (topo + ys[-1]) / 2.0, "Σ h", TINTA, 8.0, ha="right",
        peso="bold")

    _gravar(fig, "fig00l_manometrica.png")


# ══════════════════════════════════════════════════════════════════════════════
# As camadas da verificação
# ══════════════════════════════════════════════════════════════════════════════

def desenho_verificacao():
    fig, ax = _tela(120, 52, (7.4, 3.3), "")

    # Larguras que cabem o texto de cada camada: na primeira versão a base da
    # pirâmide tinha 30 unidades, e a descrição da conferência manual vazava.
    camadas = [
        (1, "Conferência manual", "balanço de dez dias recalculado em planilha",
         ROXO, "#f1ecf8"),
        (11, "Comparação com o Netuno 4", "divergência decomposta por causa",
         LARANJA, "#fdf0ea"),
        (21, "Casos de referência", "nove projetos com resultado publicado",
         AZUL, "#eaf2fd"),
        (31, "Testes de propriedade", "conservação de massa, limites, monotonicidade",
         VERDE, "#f2fbf2"),
        (41, "Testes de unidade", "cada função contra o valor esperado",
         VERDE, "#f2fbf2"),
    ]
    centro = 72.0
    for i, (y, titulo, detalhe, cor, fundo) in enumerate(camadas):
        largura = 54 + i * 8.5
        x = centro - largura / 2.0
        ax.add_patch(Rectangle((x, y), largura, 8.6, facecolor=fundo,
                               edgecolor=cor, linewidth=1.4, zorder=3))
        ax.text(centro, y + 5.6, titulo, ha="center", va="center", fontsize=8.2,
                color=TINTA, zorder=5, fontweight="bold")
        ax.text(centro, y + 2.5, detalhe, ha="center", va="center",
                fontsize=7.2, color=TINTA2, zorder=5)

    ax.annotate("", xy=(20, 3), xytext=(20, 48),
                arrowprops=dict(arrowstyle="<->", color=TINTA2, linewidth=1.2))
    ax.text(18.5, 47, "mais casos" + NL + "erro local", fontsize=7.4,
            color=TINTA2, va="top", ha="right", linespacing=1.35)
    ax.text(18.5, 4, "menos casos" + NL + "erro de modelo", fontsize=7.4,
            color=TINTA2, va="bottom", ha="right", linespacing=1.35)

    _gravar(fig, "fig00m_verificacao.png")


def main():
    print("esquemas:")
    desenho_projecao()
    desenho_etap()
    desenho_energia()
    desenho_manometrica()
    desenho_verificacao()


if __name__ == "__main__":
    main()
