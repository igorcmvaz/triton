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
    ax.set_title(titulo, color=TINTA, fontsize=10.5, loc="left", pad=10)
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
    fig, ax = _tela(100, 52, (7.4, 4.0),
                    "A chuva cai na vertical: a área que capta é a sombra do telhado")

    def rot(x, y, t, cor=TINTA2, tam=7.6, ha="left", va="center", peso="normal"):
        ax.text(x, y, t, ha=ha, va=va, fontsize=tam, color=cor, zorder=8,
                linespacing=1.35, fontweight=peso)

    # Água-furtada única, inclinada, com a projeção marcada embaixo.
    base_y = 14.0
    ax.add_patch(Polygon([(14, base_y), (62, base_y), (62, base_y + 1.6),
                          (14, base_y + 1.6)], closed=True, facecolor="none",
                         edgecolor="none"))
    # o telhado inclinado
    ax.add_patch(Polygon([(14, base_y + 2), (62, base_y + 26),
                          (62, base_y + 22), (14, base_y - 2)], closed=True,
                         facecolor=TELHA, edgecolor=TINTA2, linewidth=1.3,
                         zorder=4))
    rot(36, base_y + 15, "telhado inclinado", TINTA, 8.0, ha="center")

    # a chuva, sempre vertical
    for x in range(18, 63, 8):
        ax.add_patch(FancyArrowPatch((x, 48), (x, 40), arrowstyle="-|>",
                                     mutation_scale=9, linewidth=1.1,
                                     color=AZUL, zorder=3))
    rot(8, 44, "chuva", AZUL, 8.4)

    # a projeção horizontal
    ax.plot([14, 62], [8, 8], color=AZUL, linewidth=2.0, zorder=5)
    ax.annotate("", xy=(14, 5), xytext=(62, 5),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=1.2))
    rot(38, 2.6, "projeção horizontal — é esta a área de captação", AZUL, 7.6,
        ha="center", va="top")
    for x in (14, 62):
        ax.plot([x, x], [5, base_y + (2 if x == 14 else 22)], color=AZUL,
                linewidth=0.8, linestyle=":", zorder=3)

    # a comparação numérica, à direita
    ax.add_patch(Rectangle((68, 6), 31, 36, facecolor="#f4f3f0",
                           edgecolor=CINZA, linewidth=1.2, zorder=3))
    rot(70, 38, "Telhado de 30% de inclinação", TINTA, 7.8, peso="bold")
    rot(70, 33.5, "projeção horizontal .... 100 m²", TINTA2, 7.6)
    rot(70, 29.5, "área inclinada ......... 104 m²", TINTA2, 7.6)
    rot(70, 25.5, "diferença ............... 4%", LARANJA, 7.6)
    rot(70, 19.5, "Usar a área inclinada" + NL +
        "superestima a captação" + NL + "na mesma proporção, todo" + NL +
        "dia da série.", TINTA2, 7.4, va="top")

    _gravar(fig, "fig00i_projecao.png")


# ══════════════════════════════════════════════════════════════════════════════
# A linha de tratamento, estágio a estágio
# ══════════════════════════════════════════════════════════════════════════════

def desenho_etap():
    p = Prancha(100, 56, tamanho=(7.4, 4.2))
    p.titulo("A linha de tratamento: cada estágio remove o que o seguinte não removeria")

    p.caixa("bruta", 1, 34, 17, 11, "Água bruta" + NL + "da cisterna", cor=AZUL,
            peso="bold", tamanho=7.6)
    p.caixa("grade", 21, 34, 17, 11, "1. Gradeamento" + NL + "folhas e detritos",
            cor=VERDE, tamanho=7.2)
    p.caixa("sedim", 41, 34, 17, 11, "2. Sedimentação" + NL + "areia e partículas",
            cor=VERDE, tamanho=7.2)
    p.caixa("filtro", 61, 34, 17, 11, "3. Filtração" + NL + "turbidez e cor",
            cor=VERDE, tamanho=7.2)
    p.caixa("desinf", 81, 34, 18, 11, "4. Desinfecção" + NL + "cloro ou UV",
            cor=ROXO, tamanho=7.2)
    p.caixa("tratada", 61, 14, 17, 11, "Água tratada" + NL + "ao ponto de uso",
            cor=AZUL, peso="bold", tamanho=7.6)
    p.caixa("lodo", 31, 14, 24, 11, "Resíduo retido" + NL +
            "sai na limpeza periódica", cor=LARANJA, fundo="#fdf0ea",
            tamanho=7.2)

    p.seta("bruta", "d", "grade", "e", cor=AZUL)
    p.seta("grade", "d", "sedim", "e", cor=AZUL)
    p.seta("sedim", "d", "filtro", "e", cor=AZUL)
    p.seta("filtro", "d", "desinf", "e", cor=AZUL)
    p.seta("desinf", "b", "tratada", "d", cor=AZUL, curva=0.25)
    p.seta("sedim", "b", "lodo", "c", cor=LARANJA)
    p.seta("grade", "b", "lodo", "ce", cor=LARANJA, curva=-0.2)

    p.nota(1, 10,
           "A ordem não é negociável: desinfetar antes de filtrar gasta "
           "reagente na matéria orgânica em suspensão e deixa" + NL +
           "o patógeno protegido dentro dela. A turbidez é, por isso, a "
           "condição de validade da desinfecção, e não" + NL +
           "apenas um parâmetro estético — é o que a classe de qualidade "
           "exigida pelo uso vai cobrar.")
    p.salvar("fig00j_etap.png")


# ══════════════════════════════════════════════════════════════════════════════
# A cadeia de energia do bombeamento
# ══════════════════════════════════════════════════════════════════════════════

def desenho_energia():
    p = Prancha(100, 52, tamanho=(7.4, 3.9))
    p.titulo("Da tomada à água entregue: onde a energia se perde no caminho")

    p.caixa("tomada", 1, 30, 18, 12, "Energia na" + NL + "tomada" + NL +
            "(kWh medidos)", cor=LARANJA, peso="bold", tamanho=7.4)
    p.caixa("motor", 23, 30, 18, 12, "Motor elétrico" + NL + "η ≈ 60% a 70%",
            cor=ROXO, tamanho=7.4)
    p.caixa("eixo", 45, 30, 18, 12, "Potência no eixo" + NL +
            "(é esta a da placa)", cor=ROXO, tamanho=7.4)
    p.caixa("bomba", 67, 30, 15, 12, "Bomba" + NL + "η ≈ 50%", cor=AZUL,
            tamanho=7.4)
    p.caixa("agua", 85, 30, 14, 12, "Água" + NL + "elevada", cor=AZUL,
            peso="bold", tamanho=7.4)

    p.seta("tomada", "d", "motor", "e", cor=TINTA2)
    p.seta("motor", "d", "eixo", "e", cor=TINTA2)
    p.seta("eixo", "d", "bomba", "e", cor=TINTA2)
    p.seta("bomba", "d", "agua", "e", cor=TINTA2)

    p.caixa("perda1", 23, 15, 18, 9, "calor" + NL + "no enrolamento",
            cor=CINZA, fundo="#f4f3f0", tinta=TINTA2, tamanho=7.0)
    p.caixa("perda2", 67, 15, 15, 9, "atrito e" + NL + "recirculação",
            cor=CINZA, fundo="#f4f3f0", tinta=TINTA2, tamanho=7.0)
    p.seta("motor", "b", "perda1", "c", cor=CINZA, tracejada=True)
    p.seta("bomba", "b", "perda2", "c", cor=CINZA, tracejada=True)

    p.nota(1, 11,
           "==A potência de placa de uma motobomba é a potência no eixo, e não "
           "a que o medidor registra.== Uma bomba de" + NL +
           "meio CV com motor de 60,5% de rendimento puxa da rede cerca de "
           "0,61 kW, e não 0,37 kW. Ignorar essa" + NL +
           "diferença subestima o custeio de energia em dois terços — e o "
           "custeio de energia é o que consome a economia.")
    p.salvar("fig00k_energia.png")


# ══════════════════════════════════════════════════════════════════════════════
# A altura manométrica, decomposta
# ══════════════════════════════════════════════════════════════════════════════

def desenho_manometrica():
    fig, ax = _tela(100, 84, (7.4, 5.6),
                    "A altura manométrica: o desnível é só uma parte da conta")

    def rot(x, y, t, cor=TINTA2, tam=7.6, ha="left", va="center", peso="normal"):
        ax.text(x, y, t, ha=ha, va=va, fontsize=tam, color=cor, zorder=9,
                linespacing=1.35, fontweight=peso)

    # cisterna embaixo, caixa elevada em cima
    ax.add_patch(Rectangle((6, 4), 26, 13, facecolor="#ffffff",
                           edgecolor=AZUL, linewidth=1.5, zorder=4))
    ax.add_patch(Rectangle((6.3, 4.3), 25.4, 7.0, facecolor=AGUA,
                           edgecolor="none", zorder=5))
    rot(19, 14, "cisterna", TINTA, 8.0, ha="center", peso="bold")

    ax.add_patch(Rectangle((44, 52), 26, 13, facecolor="#ffffff",
                           edgecolor=ROXO, linewidth=1.5, zorder=4))
    ax.add_patch(Rectangle((44.3, 52.3), 25.4, 7.0, facecolor=AGUA,
                           edgecolor="none", zorder=5))
    rot(57, 62, "caixa elevada", TINTA, 8.0, ha="center", peso="bold")

    # o recalque
    ax.plot([19, 19], [11.3, 30], color=ROXO, linewidth=2.0, zorder=3)
    ax.plot([19, 57], [30, 30], color=ROXO, linewidth=2.0, zorder=3)
    ax.plot([57, 57], [30, 52], color=ROXO, linewidth=2.0, zorder=3)
    ax.add_patch(FancyArrowPatch((57, 49), (57, 52.6), arrowstyle="-|>",
                                 mutation_scale=11, linewidth=2.0, color=ROXO,
                                 zorder=4))
    rot(38, 32, "tubulação de recalque", ROXO, 7.4, ha="center", va="bottom")

    # a cota geométrica
    ax.annotate("", xy=(80, 11.3), xytext=(80, 59.3),
                arrowprops=dict(arrowstyle="<->", color=AZUL, linewidth=1.3))
    ax.plot([32, 80], [11.3, 11.3], color=AZUL, linewidth=0.7, linestyle=":")
    ax.plot([70, 82], [59.3, 59.3], color=AZUL, linewidth=0.7, linestyle=":")
    rot(82, 36, "H_geo" + NL + "desnível entre" + NL + "as duas lâminas",
        AZUL, 7.6, va="center")

    # a parcela de perda
    ax.add_patch(Rectangle((6, 73), 62, 8, facecolor="#fdf0ea",
                           edgecolor=LARANJA, linewidth=1.2, zorder=3))
    rot(8, 77, "H_man = H_geo + perdas de carga (atrito no tubo + conexões)",
        LARANJA, 8.0)

    # a motobomba, no pé do recalque
    from matplotlib.patches import Circle
    ax.add_patch(Circle((19, 22), 3.4, facecolor="#f1ecf8", edgecolor=ROXO,
                        linewidth=1.5, zorder=6))
    ax.text(19, 22, "M", ha="center", va="center", fontsize=8.4, color=ROXO,
            fontweight="bold", zorder=7)
    rot(24, 22, "motobomba", ROXO, 7.4)

    rot(6, 1.5,
        "As perdas dependem do comprimento, do diâmetro e das conexões, e num "
        "recalque predial" + NL +
        "típico somam de 10% a 30% do desnível. A altura manométrica é o que "
        "a bomba precisa" + NL +
        "vencer; o desnível é só o piso dessa conta.",
        TINTA2, 7.2, va="top")

    _gravar(fig, "fig00l_manometrica.png")


# ══════════════════════════════════════════════════════════════════════════════
# As camadas da verificação
# ══════════════════════════════════════════════════════════════════════════════

def desenho_verificacao():
    fig, ax = _tela(100, 62, (7.4, 4.4),
                    "As camadas da verificação: cada uma responde por um tipo de erro")

    camadas = [
        (8, "Conferência manual", "o balanço de dez dias, refeito na planilha",
         ROXO, "#f1ecf8"),
        (18, "Comparação com o Netuno 4", "a divergência decomposta e explicada",
         LARANJA, "#fdf0ea"),
        (28, "Casos de referência", "nove projetos que reproduzem números publicados",
         AZUL, "#eaf2fd"),
        (38, "Testes de propriedade", "invariantes que valem para qualquer entrada",
         VERDE, "#f2fbf2"),
        (48, "Testes de unidade", "cada função contra o valor que dela se espera",
         VERDE, "#f2fbf2"),
    ]
    for y, titulo, detalhe, cor, fundo in camadas:
        largura = 30 + (y - 8) * 1.35
        x = (100 - largura) / 2.0
        ax.add_patch(Rectangle((x, y), largura, 8.4, facecolor=fundo,
                               edgecolor=cor, linewidth=1.4, zorder=3))
        ax.text(50, y + 5.4, titulo, ha="center", va="center", fontsize=8.2,
                color=TINTA, zorder=5, fontweight="bold")
        ax.text(50, y + 2.4, detalhe, ha="center", va="center", fontsize=7.0,
                color=TINTA2, zorder=5)

    ax.annotate("", xy=(4, 8), xytext=(4, 56),
                arrowprops=dict(arrowstyle="-|>", color=TINTA2, linewidth=1.2))
    ax.text(1.2, 32, "de muitos casos e erro pequeno, a poucos casos e erro grave",
            fontsize=7.2, color=TINTA2, va="center", ha="center", rotation=270)

    ax.text(0, 3,
            "Nenhuma camada substitui a de baixo. O teste de unidade não vê um "
            "erro de modelo, e a conferência manual não" + chr(10) +
            "cobre mil combinações de entrada; é a superposição das cinco que "
            "sustenta o número publicado.",
            ha="left", va="top", fontsize=7.2, color=TINTA2, linespacing=1.45)

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
