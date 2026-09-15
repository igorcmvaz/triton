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
    p = Prancha(100, 70, tamanho=(7.4, 5.0))
    p.titulo("A ordem das operações de um dia, e a memória que sobra para o seguinte")

    p.caixa("chuva", 2, 47, 21, 11, "Chuva do dia" + NL + "P (mm)", cor=AZUL,
            peso="bold")
    p.caixa("descarte", 28, 47, 21, 11, "1. Desconta-se" + NL + "o descarte",
            cor=LARANJA)
    p.caixa("volume", 54, 47, 21, 11, "2. Converte-se" + NL + "em litros",
            cor=AZUL)
    p.caixa("soma", 78, 47, 20, 11, "3. Soma-se ao" + NL + "que havia", cor=AZUL)

    p.caixa("extravasa", 78, 28, 20, 10, "Extravasa" + NL + "o que não coube",
            cor=LARANJA, fundo="#fdf0ea")
    p.caixa("consumo", 45, 28, 26, 10, "4. Retira-se o" + NL + "consumo do dia",
            cor=VERDE)
    p.caixa("resto", 45, 8, 26, 11, "5. O que sobra é o" + NL +
            "volume de amanhã", cor=ROXO, peso="bold")
    p.caixa("rede", 8, 28, 28, 10, "A rede completa" + NL + "o que faltou",
            cor=CINZA, fundo="#f4f3f0")

    p.seta("chuva", "d", "descarte", "e", cor=AZUL)
    p.seta("descarte", "d", "volume", "e", cor=AZUL)
    p.seta("volume", "d", "soma", "e", cor=AZUL)
    p.seta("soma", "b", "extravasa", "c", cor=LARANJA)
    p.seta("extravasa", "e", "consumo", "d", cor=AZUL,
           rotulo="o que coube", rotulo_em=(74, 36))
    p.seta("consumo", "e", "rede", "d", cor=CINZA, tracejada=True,
           rotulo="se faltou", rotulo_em=(40, 36))
    p.seta("consumo", "b", "resto", "c", cor=ROXO)
    # A memória entre um dia e o seguinte, contornando o desenho por fora: é a
    # única ligação que não pertence ao dia corrente, e por isso não cruza nada.
    from matplotlib.patches import FancyArrowPatch
    volta = [(45, 13.5), (0.8, 13.5), (0.8, 64), (88, 64)]
    for (x1, y1), (x2, y2) in zip(volta, volta[1:]):
        p.ax.plot([x1, x2], [y1, y2], color=ROXO, linewidth=1.3, zorder=2)
    p.ax.add_patch(FancyArrowPatch((88, 64), (88, 58.6), arrowstyle="-|>",
                                   mutation_scale=11, linewidth=1.3, color=ROXO,
                                   zorder=2))
    p.ax.text(46, 65.4, "o volume que sobra é o volume inicial do dia seguinte",
              ha="left", va="bottom", fontsize=7.4, color=ROXO, zorder=5)

    p.nota(2, 5,
           "A seta roxa que volta é a razão de a simulação ser diária: o dia de "
           "hoje começa onde o de ontem parou." + NL +
           "Nenhuma média anual carrega essa memória, e é por isso que ela "
           "superestima o aproveitamento.")
    p.salvar("fig00e_balanco_do_dia.png")


# ══════════════════════════════════════════════════════════════════════════════
# YAS contra a ordem invertida
# ══════════════════════════════════════════════════════════════════════════════

def desenho_yas():
    p = Prancha(100, 58, tamanho=(7.4, 4.3))
    p.titulo("A mesma chuva, duas ordens: por que o Netuno extravasa antes de consumir")

    p.nota(2, 48, "YAS — o que o programa faz", AZUL, 8.6)
    p.caixa("a1", 2, 36, 21, 9, "Soma a chuva" + NL + "ao reservatório", cor=AZUL)
    p.caixa("a2", 27, 36, 21, 9, "Extravasa" + NL + "o excedente", cor=AZUL)
    p.caixa("a3", 52, 36, 21, 9, "Só então" + NL + "retira o consumo", cor=AZUL)
    p.caixa("a4", 77, 36, 21, 9, "Rende menos" + NL + "no dia de cheia",
            cor=AZUL, fundo="#eaf2fd", peso="bold")
    p.seta("a1", "d", "a2", "e", cor=AZUL)
    p.seta("a2", "d", "a3", "e", cor=AZUL)
    p.seta("a3", "d", "a4", "e", cor=AZUL)

    p.nota(2, 22, "YBS — a ordem invertida", LARANJA, 8.6)
    p.caixa("b1", 2, 10, 21, 9, "Soma a chuva" + NL + "ao reservatório",
            cor=LARANJA)
    p.caixa("b2", 27, 10, 21, 9, "Retira o consumo" + NL + "primeiro",
            cor=LARANJA)
    p.caixa("b3", 52, 10, 21, 9, "Extravasa" + NL + "o que ainda sobrou",
            cor=LARANJA)
    p.caixa("b4", 77, 10, 21, 9, "Rende mais," + NL + "e engana", cor=LARANJA,
            fundo="#fdf0ea", peso="bold")
    p.seta("b1", "d", "b2", "e", cor=LARANJA)
    p.seta("b2", "d", "b3", "e", cor=LARANJA)
    p.seta("b3", "d", "b4", "e", cor=LARANJA)

    p.nota(2, 6,
           "A diferença só aparece no dia em que o reservatório enche. O YAS "
           "supõe que o consumo ocorre antes da chuva do dia," + NL +
           "e é a hipótese conservadora consagrada na literatura; o YBS supõe o "
           "contrário e superestima o aproveitamento.")
    p.salvar("fig00f_yas.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os três indicadores e o que cada um divide
# ══════════════════════════════════════════════════════════════════════════════

def desenho_indicadores():
    # A primeira versão ligava os três indicadores ao mesmo numerador, o que é
    # verdade para os dois volumétricos e falso para o temporal: este não divide
    # litros, conta dias. A seção 2.3 define assim, e o desenho passa a dizer o
    # mesmo que ela.
    p = Prancha(100, 62, tamanho=(7.4, 4.6))
    p.titulo("Três indicadores: dois contam litros, um conta dias")

    p.caixa("agua", 2, 48, 60, 9, "Água de chuva consumida, em litros",
            cor=AZUL, fundo="#eaf2fd", peso="bold")
    p.caixa("pot", 2, 25, 28, 14,
            "Potencial de economia" + NL + "÷ demanda TOTAL", cor=AZUL)
    p.caixa("conf", 34, 25, 28, 14,
            "Confiabilidade" + NL + "volumétrica" + NL + "÷ demanda PLUVIAL",
            cor=VERDE)
    p.seta("agua", "be", "pot", "c", cor=AZUL)
    p.seta("agua", "bd", "conf", "c", cor=VERDE)

    p.caixa("dias", 68, 48, 30, 9, "Cada dia da série",
            cor=ROXO, fundo="#f1ecf8", peso="bold")
    p.caixa("temp", 68, 25, 30, 14,
            "Confiabilidade temporal" + NL + "% de dias plenos," + NL +
            "parciais e nulos", cor=ROXO)
    p.seta("dias", "b", "temp", "c", cor=ROXO)

    p.caixa("aviso", 2, 5, 96, 13,
            "Os dois volumétricos têm o mesmo numerador e se ligam por uma "
            "identidade exata: Epot = Rv × f," + NL +
            "em que f é a fração atendível. A confiabilidade temporal fica fora "
            "dessa conta: não mede volume," + NL +
            "e responde com que frequência se pode contar com o sistema.",
            cor=CINZA, fundo="#f4f3f0", tinta=TINTA2, tamanho=7.2)

    p.salvar("fig00g_indicadores.png")


# ══════════════════════════════════════════════════════════════════════════════
# A fronteira da avaliação ambiental
# ══════════════════════════════════════════════════════════════════════════════

def desenho_fronteira():
    p = Prancha(100, 66, tamanho=(7.4, 4.8))
    p.titulo("Até onde vai a avaliação ambiental do programa, e onde ela para")

    p.caixa("dentro", 1, 22, 66, 40, "", cor=VERDE, fundo="#f2fbf2",
            tracejada=True)
    p.nota(3, 61, "DENTRO da fronteira — o que o programa contabiliza", VERDE, 8.2)

    # O que entra e o que fica de fora segue, item por item, as sete etapas e a
    # lista «O que a avaliação não cobre» da seção 2.8. A primeira versão tinha
    # «transporte», que o texto não menciona, e omitia os impactos além do
    # carbono, que o texto chama de a exclusão mais importante.
    p.caixa("mat", 5, 45, 27, 10, "Reservatórios" + NL +
            "e tubulação", cor=VERDE, tamanho=7.6)
    p.caixa("bomba", 36, 45, 27, 10, "Fabricação" + NL + "da motobomba",
            cor=VERDE, tamanho=7.6)
    p.caixa("energia", 5, 27, 27, 10, "Bombeamento e" + NL +
            "insumos de tratamento", cor=VERDE, tamanho=7.6)
    p.caixa("evitada", 36, 27, 27, 10, "Água potável evitada" + NL +
            "(o crédito)", cor=VERDE, tamanho=7.6)

    p.caixa("fora", 71, 22, 28, 40, "", cor=LARANJA, fundo="#fdf3ee",
            tracejada=True)
    p.nota(73, 61, "FORA — e declarado", LARANJA, 8.2)
    p.caixa("obra", 74, 51.5, 22, 7.4, "Obra civil" + NL + "e escavação",
            cor=LARANJA, tamanho=7.2)
    p.caixa("manut", 74, 42.5, 22, 7.4, "Manutenção e" + NL + "reposição",
            cor=LARANJA, tamanho=7.2)
    p.caixa("fim", 74, 33.5, 22, 7.4, "Fim de vida" + NL + "(reciclagem, descarte)",
            cor=LARANJA, tamanho=7.2)
    p.caixa("impactos", 74, 24.5, 22, 7.4, "Impactos além" + NL + "do carbono",
            cor=LARANJA, tamanho=7.2)

    p.nota(1, 18,
           "A avaliação é de TRIAGEM: compara alternativas entre si e não "
           "substitui um inventário completo conforme a ISO 14040. Os itens de "
           "fora são recorte declarado, e não esquecimento. O mais limitante é o "
           "último: um sistema com bom desempenho de carbono pode ter desempenho "
           "ruim em outra categoria de impacto, e esta avaliação não o veria.")
    p.salvar("fig00h_fronteira.png")


def main():
    print("desenhos do método:")
    desenho_balanco_do_dia()
    desenho_yas()
    desenho_indicadores()
    desenho_fronteira()


if __name__ == "__main__":
    main()
