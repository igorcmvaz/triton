# -*- coding: utf-8 -*-
"""Desenhos do método: o que o programa faz por dentro.

Os desenhos de `gerar_desenhos.py` apresentam a instalação a quem chega agora.
Estes apresentam o **cálculo**: a ordem das operações do balanço diário, a
diferença entre tirar o extravasamento antes ou depois do consumo, o que cada
indicador divide por quê, e até onde vai a fronteira da avaliação ambiental.

São justamente os quatro pontos em que a prosa precisa de mais parágrafos e
consegue menos: todos se resolvem pela ordem ou pelo recorte, e ordem e recorte
se veem num desenho antes de se entenderem num texto.

Saída: manual/figuras/fig00e*.png a fig00h*.png
"""

from __future__ import annotations

import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

from gerar_desenhos import (                                      # noqa: E402
    AZUL, CINZA, LARANJA, NL, Prancha, ROXO, TINTA2, VERDE,
)


# ══════════════════════════════════════════════════════════════════════════════
# A ordem das operações de um dia, e a memória que liga um dia ao seguinte
# ══════════════════════════════════════════════════════════════════════════════

def desenho_balanco_do_dia():
    p = Prancha(100, 68, tamanho=(7.4, 4.9))

    p.caixa("chuva", 2, 47, 21, 11, "Precipitação" + NL + "P_t (mm)", cor=AZUL,
            peso="bold")
    p.caixa("descarte", 28, 47, 21, 11, "1. Desvio" + NL + "P_ef,t = P_t − d",
            cor=LARANJA)
    p.caixa("volume", 54, 47, 21, 11, "2. Captação" + NL + "P_ef,t × A × C",
            cor=AZUL)
    p.caixa("soma", 78, 47, 20, 11, "3. Disponível" + NL + "D_t", cor=AZUL)

    p.caixa("extravasa", 78, 28, 20, 10, "Extravasamento" + NL + "V_ext,t",
            cor=LARANJA, fundo="#fdf0ea")
    p.caixa("consumo", 45, 28, 26, 10, "4. Consumo pluvial" + NL + "V_con,t",
            cor=VERDE)
    p.caixa("resto", 45, 8, 26, 11, "5. Volume remanescente" + NL + "V_res,t",
            cor=ROXO, peso="bold")
    p.caixa("rede", 8, 28, 28, 10, "Abastecimento pela" + NL + "rede pública",
            cor=CINZA, fundo="#f4f3f0")

    p.seta("chuva", "d", "descarte", "e", cor=AZUL)
    p.seta("descarte", "d", "volume", "e", cor=AZUL)
    p.seta("volume", "d", "soma", "e", cor=AZUL)
    p.seta("soma", "b", "extravasa", "c", cor=LARANJA)
    p.seta("extravasa", "e", "consumo", "d", cor=AZUL,
           rotulo="V_arm,t", rotulo_em=(74.5, 40.2))
    p.seta("consumo", "e", "rede", "d", cor=CINZA, tracejada=True,
           rotulo="défice", rotulo_em=(40, 36))
    p.seta("consumo", "b", "resto", "c", cor=ROXO)

    from matplotlib.patches import FancyArrowPatch
    volta = [(45, 13.5), (0.8, 13.5), (0.8, 64), (88, 64)]
    for (x1, y1), (x2, y2) in zip(volta, volta[1:]):
        p.ax.plot([x1, x2], [y1, y2], color=ROXO, linewidth=1.3, zorder=2)
    p.ax.add_patch(FancyArrowPatch((88, 64), (88, 58.6), arrowstyle="-|>",
                                   mutation_scale=11, linewidth=1.3, color=ROXO,
                                   zorder=2))
    p.ax.text(46, 65.4, "V_res,t transferido para o dia t + 1",
              ha="left", va="bottom", fontsize=7.6, color=ROXO, zorder=5)
    p.salvar("fig00e_balanco_do_dia.png")


# ══════════════════════════════════════════════════════════════════════════════
# YAS contra a ordem invertida
# ══════════════════════════════════════════════════════════════════════════════

def desenho_yas():
    p = Prancha(107, 38, tamanho=(7.4, 2.75))
    ramos = [
        (AZUL, "#eaf2fd", 21.5, 37.6, "(a) YAS — extravasamento antes do consumo", [
            ("Disponível", "D_t =", "V_res,t−1 + V_cap,t"),
            ("Extravasamento", "V_ext,t =", "max(0 ; D_t − V_max)"),
            ("Consumo", "V_con,t =", "min(D_pl,t ; V_arm,t)"),
            ("Remanescente", "V_res,t =", "V_arm,t − V_con,t"),
        ]),
        (LARANJA, "#fdf0ea", 1.0, 17.1, "(b) YBS — consumo antes do extravasamento", [
            ("Disponível", "D_t =", "V_res,t−1 + V_cap,t"),
            ("Consumo", "V_con,t =", "min(D_pl,t ; D_t)"),
            ("Extravasamento", "V_ext,t =", "max(0 ; D_t − V_con,t − V_max)"),
            ("Remanescente", "V_res,t =", "min(D_t − V_con,t ; V_max)"),
        ]),
    ]
    larguras = [22, 25, 28, 24]
    for cor, fundo, y, y_rotulo, rotulo, passos in ramos:
        p.nota(1, y_rotulo, rotulo, cor, 8.4)
        x = 0.5
        nomes = []
        for k, ((nome, lado, expressao), w) in enumerate(zip(passos, larguras)):
            chave = rotulo[1] + str(k)
            p.caixa(chave, x, y, w, 12.5, nome + NL + lado + NL + expressao,
                    cor=cor, fundo=fundo if k == 3 else "#ffffff", tamanho=7.2)
            nomes.append(chave)
            x += w + 2.2
        for de, para in zip(nomes, nomes[1:]):
            p.seta(de, "d", para, "e", cor=cor)
    p.salvar("fig00f_yas.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os três indicadores e o que cada um divide
# ══════════════════════════════════════════════════════════════════════════════

def desenho_indicadores():
    p = Prancha(100, 36, tamanho=(7.4, 2.7))

    p.caixa("agua", 2, 26, 60, 9, "Água pluvial consumida  Σ V_con,t",
            cor=AZUL, fundo="#eaf2fd", peso="bold")
    p.caixa("pot", 2, 2, 28, 15,
            "Potencial de poupança" + NL + "Epot = Σ V_con,t ÷ Σ D_t",
            cor=AZUL)
    p.caixa("conf", 34, 2, 28, 15,
            "Fiabilidade volumétrica" + NL + "Rv = Σ V_con,t ÷ Σ D_pl,t",
            cor=VERDE)
    p.seta("agua", "be", "pot", "c", cor=AZUL)
    p.seta("agua", "bd", "conf", "c", cor=VERDE)

    p.caixa("dias", 68, 26, 30, 9, "Dias da série  N",
            cor=ROXO, fundo="#f1ecf8", peso="bold")
    p.caixa("temp", 68, 2, 30, 15,
            "Fiabilidade temporal" + NL + "dias plenos, parciais" + NL +
            "e nulos ÷ N", cor=ROXO)
    p.seta("dias", "b", "temp", "c", cor=ROXO)

    p.salvar("fig00g_indicadores.png")


# ══════════════════════════════════════════════════════════════════════════════
# A fronteira da avaliação ambiental
# ══════════════════════════════════════════════════════════════════════════════

def desenho_fronteira():
    p = Prancha(100, 50, tamanho=(7.4, 3.7))

    p.caixa("dentro", 1, 2, 66, 40, "", cor=VERDE, fundo="#f2fbf2",
            tracejada=True)
    p.nota(1, 49, "(a) Incluído na fronteira do sistema", VERDE, 8.4)

    p.caixa("mat", 5, 24, 27, 13, "Carbono incorporado" + NL +
            "reservatórios e" + NL + "tubagens", cor=VERDE, tamanho=7.6)
    p.caixa("bomba", 36, 24, 27, 13, "Carbono incorporado" + NL +
            "eletrobomba", cor=VERDE, tamanho=7.6)
    p.caixa("energia", 5, 6, 27, 13, "Emissão operacional" + NL +
            "energia de bombagem" + NL + "e reagentes da ETAP", cor=VERDE,
            tamanho=7.6)
    p.caixa("evitada", 36, 6, 27, 13, "Crédito ambiental" + NL +
            "água de rede evitada", cor=VERDE, tamanho=7.6)

    p.caixa("fora", 71, 2, 28, 40, "", cor=LARANJA, fundo="#fdf3ee",
            tracejada=True)
    p.nota(71, 49, "(b) Excluído", LARANJA, 8.4)
    p.caixa("obra", 74, 32, 22, 7.4, "Construção civil" + NL + "e escavação",
            cor=LARANJA, tamanho=7.2)
    p.caixa("manut", 74, 23, 22, 7.4, "Manutenção e" + NL + "substituição",
            cor=LARANJA, tamanho=7.2)
    p.caixa("fim", 74, 14, 22, 7.4, "Fim de vida" + NL + "(módulos C e D)",
            cor=LARANJA, tamanho=7.2)
    p.caixa("impactos", 74, 5, 22, 7.4, "Categorias além do" + NL + "aquecimento global",
            cor=LARANJA, tamanho=7.2)
    p.salvar("fig00h_fronteira.png")


def main():
    print("desenhos do método:")
    desenho_balanco_do_dia()
    desenho_yas()
    desenho_indicadores()
    desenho_fronteira()


if __name__ == "__main__":
    main()
