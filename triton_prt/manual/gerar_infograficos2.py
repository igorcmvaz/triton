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
        ("hospital", 250, 600, "L/cama·dia", ROXO),
        ("hotel", 100, 300, "L/hóspede·dia", LARANJA),
        ("residencial unifamiliar", 120, 200, "L/hab·dia", AZUL),
        ("residencial multifamiliar", 100, 180, "L/hab·dia", AZUL),
        ("escritório", 50, 80, "L/pessoa·dia", VERDE),
        ("escola", 10, 50, "L/aluno·dia", VERDE),
        ("comércio", 8, 20, "L/pessoa·dia", VERDE),
    ]
    y = np.arange(len(itens))[::-1]
    for i, (nome, a, b, unidade, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.52, color=cor, zorder=3)
        ax.text(b + 12, y[i], f"{a} a {b}  {unidade}", va="center",
                fontsize=8.0, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.6)
    _eixos(ax, "", "", "")
    ax.set_xlabel("consumo per capita de referência (L por unidade de "
                  "ocupação por dia)", color=TINTA2, fontsize=9)
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
        ("RESIDENCIAL", AZUL, [
            ("unifamiliar", "L/hab·dia"),
            ("multifamiliar", "L/hab·dia"),
        ]),
        ("PÚBLICA", VERDE, [
            ("escola", "L/aluno·dia"),
            ("hospital", "L/cama·dia"),
        ]),
        ("COMERCIAL", LARANJA, [
            ("escritório", "L/pessoa·dia"),
            ("hotel", "L/hóspede·dia"),
            ("comércio", "L/pessoa·dia"),
        ]),
        ("INDUSTRIAL", ROXO, [
            ("indústria", "conforme processo"),
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
        ax.text(x + largura / 2.0, 37.6, "categoria tarifária", ha="center",
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
                    "Os quatro modos de modulação da procura")
    itens = [
        ("constante", "um valor", "habitação," + NL + "e padrão da app", CINZA),
        ("semanal", "sete valores", "escritório, comércio," + NL + "escola",
         VERDE),
        ("mensal", "doze valores", "hotel, sazonalidade" + NL + "climática",
         AZUL),
        ("diário", "a série inteira", "quando há medição" + NL + "real, dia a dia",
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
        _confinar(ax.text(x + 11.5, 17.0, "você introduz" + NL + informa,
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
        ("investimento (CAPEX)", 15, 30, "dispersão entre orçamentos", LARANJA),
        ("procura de referência", 15, 25, "dispersão na literatura", LARANJA),
        ("precipitação", 10, 20, "variabilidade interanual", AZUL),
        ("consumo medido", 5, 10, "variação sazonal medida", VERDE),
        ("atualização tarifária (% a.a.)", 3, 7, "histórico da entidade gestora",
         ROXO),
        ("área de captação", 2, 5, "tolerância de levantamento", VERDE),
    ]
    y = np.arange(len(itens))[::-1]
    for i, (nome, a, b, porque, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.5, color=cor, zorder=3)
        # A faixa em percentual acompanha a barra; a razão fica numa coluna
        # fixa, longe dela. Acompanhando as duas a barra, a faixa mais larga
        # empurrava o seu percentual para cima da própria explicação.
        ax.text(b + 0.7, y[i], f"{a} a {b}%", va="center", fontsize=8.2,
                color=TINTA)
        ax.text(41, y[i], porque, va="center", fontsize=7.4, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.4)
    _eixos(ax, "", "", "")
    ax.set_xlabel("variação plausível em torno do valor adotado (%)",
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


# ══════════════════════════════════════════════════════════════════════════════
# Os municípios do catálogo, por unidade da federação
# ══════════════════════════════════════════════════════════════════════════════

def _municipios_por_uf():
    """A contagem por UF lida da própria base tarifária, e não digitada.

    A primeira versão trazia a lista escrita à mão; o apêndice D lê a base, e as
    duas podiam divergir sem aviso quando um município entrasse no catálogo.
    """
    import json
    from collections import Counter

    caminho = AQUI.parent / "triton" / "data" / "brazil_cities_tariffs.json"
    if not caminho.exists():
        caminho = AQUI.parent.parent / "triton_brl" / "triton" / "data" / "brazil_cities_tariffs.json"
    cidades = json.load(open(caminho, encoding="utf-8"))["cities"]
    contagem = Counter(c.get("uf") for c in cidades.values() if c.get("uf"))
    return sorted(contagem.items(), key=lambda item: (-item[1], item[0]))

REGIAO = {
    "Sudeste": ("SP", "MG", "RJ", "ES"),
    "Sul": ("RS", "PR", "SC"),
    "Nordeste": ("BA", "CE", "PE", "MA", "AL", "PB", "RN", "SE", "PI"),
    "Norte": ("PA", "AM", "RO", "AC", "AP", "TO", "RR"),
    "Centro-Oeste": ("GO", "MT", "MS", "DF"),
}
COR_REGIAO = {"Sudeste": AZUL, "Sul": VERDE, "Nordeste": LARANJA,
              "Norte": ROXO, "Centro-Oeste": CINZA}


def info_uf():
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    def regiao_de(uf):
        for nome, ufs in REGIAO.items():
            if uf in ufs:
                return nome
        return "Norte"

    ufs = _municipios_por_uf()
    nomes = [u for u, _ in ufs]
    quantos = [n for _, n in ufs]
    cores = [COR_REGIAO[regiao_de(u)] for u in nomes]

    x = np.arange(len(nomes))
    ax.bar(x, quantos, 0.66, color=cores, zorder=3)
    for i, n in enumerate(quantos):
        ax.text(i, n + 2.5, str(n), ha="center", fontsize=7.0, color=TINTA2)

    ax.set_xticks(x)
    ax.set_xticklabels(nomes, fontsize=7.6)
    _eixos(ax, "", "", "número de municípios")
    ax.set_ylim(0, 160)
    ax.set_yticks(range(0, 161, 20))

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=COR_REGIAO[r], label=r)
                       for r in REGIAO],
              frameon=False, fontsize=8.0, loc="upper right", ncol=1)

    fig.tight_layout()
    _gravar(fig, "fig42_uf.png")


# ══════════════════════════════════════════════════════════════════════════════
# As perdas de distribuição, por macrorregião
# ══════════════════════════════════════════════════════════════════════════════

def info_perdas():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    itens = [("Sudeste", 33.9, False), ("Sul", 35.0, True),
             ("Centro-Oeste", 40.0, True), ("Nordeste", 45.0, True),
             ("Norte", 46.9, False)]
    y = np.arange(len(itens))[::-1]
    for i, (nome, perda, aprox) in enumerate(itens):
        ax.barh(y[i], perda, height=0.55, color=LARANJA, zorder=3)
        ax.barh(y[i], 100 - perda, left=perda, height=0.55, color=AZUL,
                zorder=3)
        marca = "~" if aprox else ""
        ax.text(perda / 2.0, y[i], f"{marca}{perda:.1f}%".replace(".", ","),
                ha="center", va="center", fontsize=8.0, color="#ffffff")
        ax.text(perda + (100 - perda) / 2.0, y[i],
                f"entrega {marca}{(100 - perda) / 100:.2f} m³".replace(".", ","),
                ha="center", va="center", fontsize=8.0, color="#ffffff")

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.8)
    _eixos(ax, "", "", "")
    ax.set_xlabel("% do volume produzido", color=TINTA2, fontsize=9)
    ax.set_xlim(0, 100)
    ax.grid(axis="y", visible=False)

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=LARANJA, label="perdas na distribuição"),
                       Patch(facecolor=AZUL, label="entregue no edifício")],
              frameon=False, fontsize=8.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.22), ncol=2)

    fig.tight_layout()
    _gravar(fig, "fig43_perdas.png")


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
         "trajetória intermédia," + NL + "próxima das políticas atuais"),
        ("SSP5-8.5", LARANJA, 40 + 85 * ((anos - 2020) / 80.0) ** 1.4,
         "emissões elevadas," + NL + "sem mitigação efetiva"),
    ]
    for nome, cor, y, _ in curvas:
        ax.plot(anos, y, color=cor, linewidth=2.6, zorder=3, label=nome)
        ax.text(2101, y[-1], "  " + nome, color=cor, fontsize=8.6,
                va="center", fontweight="bold")

    ax.axhline(0.0, color=TINTA2, linewidth=1.0, zorder=2)
    ax.text(2021, 2.0, "emissões líquidas nulas", fontsize=7.6, color=TINTA2)

    _eixos(ax, "", "", "emissões globais de CO₂ (esquemático)")
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
    ("unitários", "unit", 104, 1269, VERDE),
    ("invariantes", "invariants", 11, 175, AZUL),
    ("integração", "integration", 9, 65, AZUL),
    ("interface gráfica", "ui", 10, 33, ROXO),
    ("replicação do Netuno 4", "benchmarking", 1, 2, LARANJA),
]


def info_suite():
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    y = np.arange(len(SUITE))[::-1]
    for i, (nome, pasta, arquivos, testes, cor) in enumerate(SUITE):
        ax.barh(y[i], testes, height=0.55, color=cor, zorder=3)
        rotulo = (f"{testes:,}".replace(",", ".") + " testes · "
                  + f"{arquivos} ficheiro" + ("s" if arquivos > 1 else ""))
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
    ax.set_xlabel("casos de teste recolhidos", color=TINTA2, fontsize=9)
    ax.set_xlim(0, 1400)
    ax.set_xticks(range(0, 1201, 200))
    ax.set_xticklabels([f"{v:,}".replace(",", ".") for v in range(0, 1201, 200)])
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
        ("edifício comercial:" + NL + "quase só autoclismos e limpeza", 70, 85,
         ROXO),
        ("tudo exceto duche," + NL + "cozinha e água para beber", 45, 60, CINZA),
        ("com máquina de lavar:" + NL + "usos não potáveis alargados", 35, 45, AZUL),
        ("autoclismos e rega:" + NL + "usos de referência", 25, 35, VERDE),
        ("apenas autoclismos", 20, 30, LARANJA),
    ]
    y = np.arange(len(itens))
    for i, (nome, a, b, cor) in enumerate(itens):
        ax.barh(y[i], b - a, left=a, height=0.5, color=cor, zorder=3)
        ax.text(b + 1.5, y[i], f"{a} a {b}%", va="center", fontsize=8.6,
                color=TINTA)

    # O valor do tutorial: bacia sanitária e usos externos, sem a máquina de lavar
    ax.axvline(28, color=TINTA2, lw=1.0, ls="--", zorder=4)
    ax.text(27, len(itens) - 0.45, "tutorial, 28%", ha="right", va="bottom",
            fontsize=8.0, color=TINTA2)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.0)
    ax.set_ylim(-0.6, len(itens) - 0.1)
    _eixos(ax, "", "", "")
    ax.set_xlabel("fração da procura total atendível por água pluvial (%)",
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
    info_uf()
    info_perdas()
    info_cenarios()
    info_suite()
    info_atendivel()


if __name__ == "__main__":
    main()
