# -*- coding: utf-8 -*-
"""Infográficos que substituem tabelas do manual.

Há tabelas que existem só porque a informação precisava caber em algum lugar, e
não porque a linha e a coluna digam algo sobre ela. Uma lista de tecnologias, uma
escala de coeficientes, cinco referenciais com limiares diferentes: tudo isso se
lê mais rápido desenhado do que tabulado, e o manual ficava cansativo por
acumular tabelas onde bastava uma figura.

Cada figura aqui **substitui** uma tabela do texto, e não se acrescenta a ela.

Executar a partir da raiz do programa:
    python manual/gerar_infograficos.py
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

from gerar_desenhos import rotulo_de_painel                       # noqa: E402

FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

AZUL = "#2a78d6"
LARANJA = "#eb6834"
VERDE = "#0ca30c"
ROXO = "#7d5fb0"
TINTA = "#0b0b0b"
TINTA2 = "#52514e"
CINZA = "#8a8880"
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"
SUPERFICIE = "#fcfcfb"
NL = chr(10)

CLARO = {AZUL: "#eaf2fd", LARANJA: "#fdf0ea", VERDE: "#eefaee",
         ROXO: "#f1ecf8", CINZA: "#f4f3f0"}


def _tela(largura, altura, tamanho, titulo):
    fig, ax = plt.subplots(figsize=tamanho)
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.set_xlim(0, largura)
    ax.set_ylim(0, altura)
    ax.axis("off")
    rotulo_de_painel(ax, titulo)
    _CONFINADOS.clear()
    return fig, ax


# ── texto que cabe na caixa em que foi posto ─────────────────────────────────
#
# Estimar a largura de um texto pelo número de caracteres erra, e errava para
# mais nos rótulos com acentos e palavras longas: «o método, com procedência»
# saía pelos dois lados do cartão. A medida agora é feita no próprio
# renderizador, depois de desenhado, e a fonte encolhe até caber.

#: Os textos que precisam caber numa caixa: (artista, (x0, y0, x1, y1)).
_CONFINADOS = []

#: Abaixo disto o texto fica ilegível na página, e é melhor o desenho falhar.
FONTE_MINIMA = 5.6


def _confinar(artista, caixa):
    """Registra um texto e a caixa da qual ele não pode sair."""
    _CONFINADOS.append((artista, caixa))
    return artista


def _cabe(artista, caixa, ax, renderizador, folga_x=0.7, folga_y=0.25):
    """A folga horizontal é maior: é na largura que o texto costuma vazar.

    Na vertical o rótulo é posto centrado numa faixa medida para ele, e exigir
    ali a mesma folga da largura reprovaria caixas que estão corretas.
    """
    x0, y0, x1, y1 = caixa
    extensao = artista.get_window_extent(renderer=renderizador)
    (ex0, ey0), (ex1, ey1) = ax.transData.inverted().transform(extensao)
    return (ex0 >= x0 + folga_x and ex1 <= x1 - folga_x
            and ey0 >= y0 + folga_y and ey1 <= y1 - folga_y)


def _ajustar_textos(fig, ax):
    """Encolhe cada texto confinado até caber, e uniformiza o resultado.

    Encolher só o rótulo que vaza deixa um cartão com letra menor que os
    vizinhos, e a diferença salta aos olhos numa fileira de cartões iguais. Por
    isso, depois de acertar cada um, todos os rótulos que partiram do mesmo
    tamanho terminam no menor tamanho a que algum deles precisou descer.
    """
    fig.canvas.draw()
    renderizador = fig.canvas.get_renderer()
    originais = [a.get_fontsize() for a, _ in _CONFINADOS]
    apertados = []
    for artista, caixa in _CONFINADOS:
        while not _cabe(artista, caixa, ax, renderizador):
            tamanho = artista.get_fontsize() * 0.94
            if tamanho < FONTE_MINIMA:
                apertados.append(artista.get_text().replace(NL, " ")[:40])
                break
            artista.set_fontsize(tamanho)
            fig.canvas.draw()
            renderizador = fig.canvas.get_renderer()
    if apertados:
        raise AssertionError(
            "texto que não cabe na caixa nem na fonte mínima: "
            + "; ".join(apertados))

    menor = {}
    for (artista, _), original in zip(_CONFINADOS, originais):
        chave = round(original, 2)
        menor[chave] = min(menor.get(chave, original), artista.get_fontsize())
    for (artista, _), original in zip(_CONFINADOS, originais):
        artista.set_fontsize(menor[round(original, 2)])
    _CONFINADOS.clear()


def _cartao(ax, x, y, w, h, cor, titulo, corpo, tam_titulo=8.6, tam_corpo=7.4,
            numero=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.0,rounding_size=1.0",
        linewidth=1.4, edgecolor=cor, facecolor=CLARO.get(cor, "#ffffff"),
        zorder=3))
    ax.add_patch(Rectangle((x, y + h - 0.9), w, 0.9, facecolor=cor,
                           edgecolor="none", zorder=4))
    cx = x + w / 2.0
    caixa = (x, y, x + w, y + h)
    if numero is not None:
        # O número numa linha própria: posto ao lado do título, ele empurrava
        # os títulos longos para fora do cartão.
        ax.text(cx, y + h - 3.2, str(numero), ha="center", va="center",
                fontsize=11.5, color=cor, fontweight="bold", zorder=5)
        _confinar(ax.text(cx, y + h - 7.0, titulo, ha="center", va="center",
                          fontsize=tam_titulo, color=TINTA, fontweight="bold",
                          zorder=5, linespacing=1.25), caixa)
        _confinar(ax.text(cx, y + (h - 10.0) / 2.0, corpo, ha="center",
                          va="center", fontsize=tam_corpo, color=TINTA2,
                          zorder=5, linespacing=1.4), caixa)
        return
    _confinar(ax.text(cx, y + h - 3.4, titulo, ha="center", va="center",
                      fontsize=tam_titulo, color=TINTA, fontweight="bold",
                      zorder=5), caixa)
    _confinar(ax.text(cx, y + (h - 5.0) / 2.0, corpo, ha="center", va="center",
                      fontsize=tam_corpo, color=TINTA2, zorder=5,
                      linespacing=1.4), caixa)


def _gravar(fig, nome):
    if _CONFINADOS:
        _ajustar_textos(fig, fig.axes[0])
    fig.savefig(FIGURAS / nome, dpi=170, bbox_inches="tight",
                facecolor=SUPERFICIE)
    plt.close(fig)
    print("  figuras/" + nome)


def _eixos(ax, titulo, x, y):
    rotulo_de_painel(ax, titulo)
    ax.set_xlabel(x, color=TINTA2, fontsize=9)
    ax.set_ylabel(y, color=TINTA2, fontsize=9)
    ax.grid(True, color=GRADE, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(EIXO)
    ax.tick_params(colors=TINTA2, labelsize=8.5)


# ══════════════════════════════════════════════════════════════════════════════
# As seis dimensões de análise
# ══════════════════════════════════════════════════════════════════════════════

def info_dimensoes():
    fig, ax = _tela(100, 46, (7.4, 3.5),
                    "As seis dimensões de análise e a questão avaliada em cada uma")
    itens = [
        ("técnica", "volume fornecido" + NL + "pelo sistema e" + NL +
         "confiabilidade", AZUL),
        ("qualidade", "tratamento exigido" + NL + "pelo uso previsto" + NL +
         "e seu custo", VERDE),
        ("econômica", "viabilidade: prazo" + NL + "de retorno, VPL" + NL +
         "e TIR", LARANJA),
        ("ambiental", "emissões evitadas" + NL + "e prazo de retorno" + NL +
         "de carbono", VERDE),
        ("certificação", "enquadramento em" + NL + "cinco referenciais" + NL +
         "de certificação", ROXO),
        ("decisão", "seleção do volume" + NL + "entre critérios" + NL +
         "concorrentes", ROXO),
    ]
    for i, (titulo, corpo, cor) in enumerate(itens):
        x = 1 + (i % 3) * 33
        y = 24 if i < 3 else 1
        _cartao(ax, x, y, 31, 20, cor, titulo, corpo)
    _gravar(fig, "fig26_dimensoes.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os quatro perfis de leitor
# ══════════════════════════════════════════════════════════════════════════════

def info_leitores():
    fig, ax = _tela(100, 26, (7.4, 2.2),
                    "Percursos de leitura do manual")
    itens = [
        ("estudante", "tutorial: um estudo" + NL + "completo, em sequência", AZUL),
        ("projetista", "guias práticos e" + NL + "roteiro por objetivo", VERDE),
        ("pesquisador", "método, com a" + NL + "procedência dos dados",
         LARANJA),
        ("revisor", "verificação e" + NL + "limitações declaradas", ROXO),
    ]
    for i, (titulo, corpo, cor) in enumerate(itens):
        _cartao(ax, 1 + i * 25, 1, 23, 23, cor, titulo, corpo,
                tam_titulo=8.8, tam_corpo=7.4)
    _gravar(fig, "fig27_leitores.png")


# ══════════════════════════════════════════════════════════════════════════════
# As doze etapas do programa
# ══════════════════════════════════════════════════════════════════════════════

def info_etapas():
    fig, ax = _tela(100, 66, (7.4, 4.9),
                    "As doze etapas do programa, na ordem de trabalho")
    grupos = [
        (AZUL, "ENTRADA", [
            (1, "Projeto e Chuva", "série de precipitação" + NL + "e captação"),
            (2, "Edificação" + NL + "e Consumo", "ocupação, consumo," + NL +
             "fração atendível"),
            (3, "Qualidade e ETAP", "classe de água" + NL + "e tratamento"),
            (4, "Reservatório" + NL + "e Custos", "volume ou varredura," + NL +
             "e orçamento"),
        ]),
        (VERDE, "RESULTADOS", [
            (5, "Resultados Técnicos", "quanta água" + NL + "o sistema entrega"),
            (6, "Resultados" + NL + "Econômicos", "em quanto tempo" + NL +
             "se paga"),
            (7, "Ambientais e ESG", "carbono e" + NL + "certificações"),
            (8, "Decisão" + NL + "Multicritério", "qual volume" + NL +
             "escolher"),
        ]),
        (ROXO, "SAÍDA E APOIO", [
            (9, "Relatórios PDF", "o documento" + NL + "do estudo"),
            (10, "Exportação", "planilhas, desenho" + NL + "e dados"),
            (11, "Documentação", "o método dentro" + NL + "do programa"),
            (12, "Gestor de Tarifas", "a tarifa do" + NL + "seu município"),
        ]),
    ]
    for g, (cor, rotulo, etapas) in enumerate(grupos):
        y = 45 - g * 21
        ax.text(0.5, y + 9.0, rotulo, fontsize=7.6, color=cor, va="center",
                rotation=90, ha="center", fontweight="bold")
        for i, (n, titulo, corpo) in enumerate(etapas):
            _cartao(ax, 3 + i * 24.5, y, 23, 18, cor, titulo, corpo,
                    tam_titulo=7.2, tam_corpo=6.8, numero=n)
    _gravar(fig, "fig28_etapas.png")


# ══════════════════════════════════════════════════════════════════════════════
# As três classes de atendimento diário
# ══════════════════════════════════════════════════════════════════════════════

def info_atendimento():
    fig, ax = _tela(100, 33, (7.4, 2.45), "")
    casos = [
        ("pleno", VERDE, 1.0, "V_con,t = D_pl,t"),
        ("parcial", LARANJA, 0.45, "0 < V_con,t < D_pl,t"),
        ("nulo", CINZA, 0.0, "V_con,t = 0"),
    ]
    # O rótulo vai abaixo da barra, e não ao lado: ao lado ele dispunha de
    # meia coluna e saía por cima do caso seguinte.
    for i, (nome, cor, fracao, criterio) in enumerate(casos):
        x = 2 + i * 32
        cx = x + 15.5
        ax.add_patch(Rectangle((cx - 6, 12), 12, 16, facecolor="#ffffff",
                               edgecolor=CINZA, linewidth=1.3, zorder=3))
        if fracao > 0:
            ax.add_patch(Rectangle((cx - 5.7, 12.3), 11.4, 15.4 * fracao,
                                   facecolor=cor, edgecolor="none", zorder=4))
        ax.text(cx, 29.4, nome, ha="center", va="bottom", fontsize=9.4,
                color=cor, fontweight="bold")
        ax.text(cx + 6.8, 26.5, "D_pl,t", ha="left", va="center",
                fontsize=7.2, color=TINTA2)
        _confinar(ax.text(cx, 6.0, criterio, ha="center", va="center",
                          fontsize=8.0, color=TINTA, linespacing=1.4),
                  (x, 1.0, x + 31, 10.5))
    _gravar(fig, "fig29_atendimento.png")


# ══════════════════════════════════════════════════════════════════════════════
# As três tecnologias de desinfecção
# ══════════════════════════════════════════════════════════════════════════════

def info_desinfeccao():
    fig, ax = _tela(100, 30, (7.4, 2.3), "")
    itens = [
        ("cloração" + NL + "(hipoclorito em pastilhas)", VERDE, "sim",
         "reposição de pastilhas" + NL + "(kg/ano)"),
        ("radiação ultravioleta", AZUL, "não", "energia elétrica e" + NL +
         "troca de lâmpada"),
        ("ozonização", ROXO, "não", "energia elétrica e" + NL +
         "manutenção do gerador"),
    ]
    for i, (nome, cor, residual, custeio) in enumerate(itens):
        x = 2 + i * 32.5
        ax.add_patch(FancyBboxPatch(
            (x, 1), 30, 28, boxstyle="round,pad=0.0,rounding_size=1.0",
            linewidth=1.4, edgecolor=cor, facecolor=CLARO[cor], zorder=3))
        _confinar(ax.text(x + 15, 24, nome, ha="center", va="center",
                          fontsize=8.8, color=TINTA, fontweight="bold",
                          zorder=5, linespacing=1.3), (x, 19, x + 30, 29))
        marca = "●" if residual == "sim" else "○"
        cor_marca = VERDE if residual == "sim" else CINZA
        _confinar(ax.text(x + 15, 16.5, marca + "  efeito residual: " + residual,
                          ha="center", va="center", fontsize=8.4,
                          color=cor_marca, zorder=5, fontweight="bold"),
                  (x, 13, x + 30, 20))
        _confinar(ax.text(x + 15, 8.0, "OPEX: " + custeio,
                          ha="center", va="center", fontsize=7.4, color=TINTA2,
                          zorder=5, linespacing=1.4), (x, 1, x + 30, 14))
    _gravar(fig, "fig30_desinfeccao.png")


# ══════════════════════════════════════════════════════════════════════════════
# O rendimento dos motores de indução
# ══════════════════════════════════════════════════════════════════════════════

def info_motores():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    potencias = ["1/4 CV" + NL + "0,18 kW", "1/3 CV" + NL + "0,25 kW",
                 "1/2 CV" + NL + "0,37 kW", "3/4 CV" + NL + "0,55 kW",
                 "1 CV" + NL + "0,75 kW", "1,5 CV" + NL + "1,10 kW",
                 "2 CV" + NL + "1,50 kW"]
    ir1 = [50.0, 55.5, 60.5, 64.0, 69.3, 71.5, 72.4]
    ir2 = [64.0, 68.0, 72.0, 74.0, 75.5, 82.5, 84.0]

    x = np.arange(len(potencias))
    ax.bar(x - 0.19, ir1, 0.36, color=AZUL, zorder=3, label="IR1 (padrão)")
    ax.bar(x + 0.19, ir2, 0.36, color=VERDE, zorder=3,
           label="IR2 (alto rendimento)")
    for i, (a, b) in enumerate(zip(ir1, ir2)):
        ax.text(i - 0.19, a + 1.2, f"{a:.1f}".replace(".", ","), ha="center",
                fontsize=7.4, color=TINTA2)
        ax.text(i + 0.19, b + 1.2, f"{b:.1f}".replace(".", ","), ha="center",
                fontsize=7.4, color=TINTA2)

    ax.annotate("o motor mais comum em\ninstalação predial",
                xy=(2 - 0.19, 60.5), xytext=(2.3, 34.0), fontsize=8.0,
                color=AZUL,
                arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=1.0))

    _eixos(ax, "O rendimento do motor cresce com a potência, e muda com a classe",
           "", "rendimento (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(potencias, fontsize=7.4)
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2)

    fig.tight_layout()
    _gravar(fig, "fig31_motores.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os seis códigos de faixa tarifária
# ══════════════════════════════════════════════════════════════════════════════

def info_codigos():
    fig, ax = _tela(100, 75, (7.4, 5.8), "")
    itens = [
        ("1  ou  0", "faixa de consumo", AZUL,
         "preço por m³ do volume alocado" + NL +
         "em cada faixa de consumo"),
        ("−1", "tarifa de disponibilidade", LARANJA,
         "valor fixo somado à parcela" + NL + "do consumo medido"),
        ("−2", "franquia retroativa", ROXO,
         "valor fixo até a franquia;" + NL +
         "acima dela, faturamento desde 0 m³"),
        ("−3", "piso de pagamento", VERDE,
         "valor mínimo da fatura:" + NL + "limite inferior, sem soma"),
        ("2", "preço-base exponencial", AZUL,
         "PB da fórmula PB × Cⁿ," + NL + "válida até o teto da linha"),
        ("3", "expoente da tabela", AZUL,
         "n aplicado ao consumo do mês" + NL + "inteiro que cai nesta linha"),
    ]
    for i, (codigo, nome, cor, efeito) in enumerate(itens):
        y = 63 - i * 12.4
        ax.add_patch(FancyBboxPatch(
            (1, y), 97, 11, boxstyle="round,pad=0.0,rounding_size=0.8",
            linewidth=1.3, edgecolor=cor, facecolor=CLARO[cor], zorder=3))
        ax.add_patch(Rectangle((1, y), 13, 11, facecolor=cor,
                               edgecolor="none", zorder=4))
        ax.text(7.5, y + 5.5, codigo, ha="center", va="center", fontsize=10.5,
                color="#ffffff", fontweight="bold", zorder=5)
        ax.text(16, y + 7.6, nome, ha="left", va="center", fontsize=8.8,
                color=TINTA, fontweight="bold", zorder=5)
        ax.text(16, y + 3.4, efeito, ha="left", va="center", fontsize=7.6,
                color=TINTA2, zorder=5, linespacing=1.4)
    _gravar(fig, "fig32_codigos.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os seis regimes de mínimo no catálogo
# ══════════════════════════════════════════════════════════════════════════════

def info_regimes_base():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    regimes = ["franquia no mínimo", "sem valor mínimo", "tarifa de disponibilidade",
               "fórmula exponencial", "franquia retroativa", "piso de pagamento"]
    quantos = [329, 165, 122, 34, 2, 0]
    cores = [LARANJA, VERDE, AZUL, AZUL, ROXO, CINZA]

    y = np.arange(len(regimes))[::-1]
    ax.barh(y, quantos, height=0.58, color=cores, zorder=3)
    total = sum(quantos)
    for i, (n, cor) in enumerate(zip(quantos, cores)):
        ax.text(n + 6, y[i], f"{n}  ({n / total * 100:.0f}%)", va="center",
                fontsize=8.6, color=TINTA)

    ax.set_yticks(y)
    ax.set_yticklabels(regimes, fontsize=8.6)
    _eixos(ax, "", "número de municípios", "")
    ax.set_xlim(0, 400)
    ax.set_xticks(range(0, 401, 50))

    fig.tight_layout()
    _gravar(fig, "fig33_regimes_base.png")


# ══════════════════════════════════════════════════════════════════════════════
# As sete etapas do inventário
# ══════════════════════════════════════════════════════════════════════════════

def info_inventario():
    fig, ax = _tela(100, 39, (7.4, 2.6), "")
    ax.set_ylim(5, 39)
    grupos = [
        # O subtítulo de cada grupo vai em duas linhas: numa só ele passava da
        # largura da coluna e saía por cima da coluna vizinha.
        ("INCORPORADO", LARANJA, "emissão única" + NL + "(fabricação)",
         ["1. cisterna inferior", "2. reservatório superior",
          "3. tubulação", "4. motobomba"]),
        ("OPERACIONAL", AZUL, "emissão anual" + NL + "(operação)",
         ["5. bombeamento", "6. tratamento"]),
        ("CRÉDITO", VERDE, "emissão evitada" + NL + "(sinal negativo)",
         ["7. água potável evitada"]),
    ]
    # As colunas dividem a prancha proporcionalmente ao que cada uma guarda, e
    # nenhuma delas fica estreita demais para o próprio rótulo.
    pesos = [4, 2, 2]
    vao = 3.0
    disponivel = 98.0 - vao * (len(grupos) - 1)
    x = 1
    for (rotulo, cor, explica, etapas), peso in zip(grupos, pesos):
        largura = disponivel * peso / float(sum(pesos))
        ax.add_patch(FancyBboxPatch(
            (x, 6), largura, 32, boxstyle="round,pad=0.0,rounding_size=1.0",
            linewidth=1.4, edgecolor=cor, facecolor=CLARO[cor], zorder=3))
        _confinar(ax.text(x + largura / 2.0, 35.2, rotulo, ha="center",
                          va="center", fontsize=8.6, color=cor,
                          fontweight="bold", zorder=5),
                  (x, 33.2, x + largura, 37.6)),
        _confinar(ax.text(x + largura / 2.0, 31.2, explica, ha="center",
                          va="center", fontsize=6.8, color=TINTA2, zorder=5,
                          linespacing=1.35),
                  (x, 28.2, x + largura, 33.6))
        for i, etapa in enumerate(etapas):
            ax.add_patch(FancyBboxPatch(
                (x + 2, 22.4 - i * 5.2), largura - 4, 4.4,
                boxstyle="round,pad=0.0,rounding_size=0.6", linewidth=1.0,
                edgecolor=cor, facecolor="#ffffff", zorder=4))
            _confinar(ax.text(x + largura / 2.0, 24.6 - i * 5.2, etapa,
                              ha="center", va="center", fontsize=7.6,
                              color=TINTA, zorder=5),
                      (x + 2, 22.4 - i * 5.2, x + largura - 2,
                       26.8 - i * 5.2))
        x += largura + vao
    _gravar(fig, "fig34_inventario.png")


# ══════════════════════════════════════════════════════════════════════════════
# O coeficiente de escoamento
# ══════════════════════════════════════════════════════════════════════════════

def info_escoamento():
    # A figura lê a mesma tabela que a interface aplica. A primeira versão
    # desenhava faixas sem fonte, e a telha cerâmica aparecia entre 0,80 e 0,90
    # enquanto a lista de materiais do programa usava 0,75.
    raiz = str(AQUI.parent)
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from netuno.core.hydrology_defaults import (
        COEFICIENTE_DE_ESCOAMENTO_PADRAO, COEFICIENTES_POR_MATERIAL)

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    itens = sorted(COEFICIENTES_POR_MATERIAL, key=lambda item: item[1])
    y = np.arange(len(itens))
    cores = [LARANJA if valor < 0.5 else AZUL for _, valor in itens]
    ax.barh(y, [valor for _, valor in itens], height=0.55, color=cores, zorder=3)
    for i, (_, valor) in enumerate(itens):
        ax.text(valor + 0.012, y[i], f"{valor:.2f}".replace(".", ","),
                va="center", fontsize=8.4, color=TINTA)

    # A linha marca o fator da NBR 15527 que o tutorial digita, e não o padrão
    # do programa, que é o da telha cerâmica e já aparece como barra.
    padrao = 0.85
    ax.axvline(padrao, color=VERDE, linestyle="--", linewidth=1.3, zorder=4)
    ax.text(padrao, len(itens) - 0.3,
            f"{padrao:.2f}".replace(".", ",") + ": η da NBR 15527," + NL +
            "digitado no tutorial",
            ha="center", va="bottom", fontsize=7.8, color=VERDE)

    ax.set_yticks(y)
    ax.set_yticklabels([nome for nome, _ in itens], fontsize=8.6)
    _eixos(ax, "O coeficiente que o programa aplica a cada cobertura", "", "")
    ax.set_ylim(-0.6, len(itens) + 0.7)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 1.12)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticklabels(["0", "0,2", "0,4", "0,6", "0,8", "1,0"])
    ax.set_xlabel("fração da chuva que chega ao reservatório", color=TINTA2,
                  fontsize=9)

    fig.tight_layout()
    _gravar(fig, "fig35_escoamento.png")


# ══════════════════════════════════════════════════════════════════════════════
# As quatro classes de qualidade
# ══════════════════════════════════════════════════════════════════════════════

def info_classes():
    fig, ax = _tela(100, 30, (7.4, 2.3), "")
    itens = [
        ("1", VERDE, "ABNT NBR 15527:2019", "Tabela 1 da norma" + NL +
         "(usos não potáveis)"),
        ("2", LARANJA, "adaptação do programa", "irrigação, lavagem de" + NL +
         "pisos e de veículos"),
        ("3", LARANJA, "adaptação do programa", "torres de resfriamento" + NL +
         "e caldeiras"),
        ("4", LARANJA, "adaptação do programa", "lavagem de roupas e" + NL +
         "demais usos não potáveis"),
    ]
    for i, (classe, cor, situacao, uso) in enumerate(itens):
        x = 1 + i * 24.7
        ax.add_patch(FancyBboxPatch(
            (x, 1), 23, 28, boxstyle="round,pad=0.0,rounding_size=1.0",
            linewidth=1.6 if cor == VERDE else 1.2, edgecolor=cor,
            facecolor=CLARO[cor], zorder=3))
        _confinar(ax.text(x + 11.5, 24.5, "classe " + classe, ha="center",
                          va="center", fontsize=9.4, color=TINTA,
                          fontweight="bold", zorder=5), (x, 22, x + 23, 28))
        _confinar(ax.text(x + 11.5, 19.0, situacao, ha="center",
                          va="center", fontsize=7.6, color=cor,
                          fontweight="bold", zorder=5), (x, 16, x + 23, 22))
        _confinar(ax.text(x + 11.5, 9.5, uso, ha="center", va="center",
                          fontsize=7.4, color=TINTA2, zorder=5,
                          linespacing=1.4), (x, 1, x + 23, 16))
    _gravar(fig, "fig36_classes.png")


# ══════════════════════════════════════════════════════════════════════════════
# Os cinco referenciais de certificação, na mesma régua
# ══════════════════════════════════════════════════════════════════════════════

def info_certificacoes():
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    # Cada referencial declara os seus limiares em percentual de economia; postos
    # na mesma régua, vê-se de imediato qual exige mais e onde um projeto cai.
    trilhas = [
        ("LEED v4  ·  WEc1" + NL + "uso externo", AZUL,
         [(50, "1 pt"), (100, "2 pt")]),
        ("LEED v4  ·  WEc2" + NL + "uso interno", AZUL,
         [(25, "1 pt"), (30, "2 pt"), (35, "3 pt"), (40, "4 pt"),
          (45, "5 pt"), (50, "6 pt")]),
        # Referencial AQUA-HQE Residencial v00 (22/11/2024). O Selo Casa Azul
        # saiu da régua: o critério 3.6 pontua a existência do sistema e a
        # abrangência do uso, e não um percentual de economia.
        ("LEED v5  ·  WEc2" + NL + "opção 2: louças e metais", AZUL,
         [(30, "1 pt"), (35, "2 pt"), (40, "3 pt")]),
        ("LEED v5  ·  WEc2" + NL + "opção 1: projeto inteiro", AZUL,
         [(30, "1"), (35, "2"), (40, "3"), (45, "4"), (50, "5"), (55, "6"), (60, "7"), (65, "8 pt")]),
        ("AQUA-HQE Resid." + NL + "consumo de água", ROXO,
         [(20, "EAU.1.2" + NL + "HQE"), (40, "EAU.1.3" + NL + "HQE 3")]),
        ("EDGE  ·  água," + NL + "energia e materiais", LARANJA,
         [(20, "EDGE" + NL + "Certified")]),
    ]

    for i, (nome, cor, marcos) in enumerate(trilhas):
        y = len(trilhas) - 1 - i
        ax.plot([0, 100], [y, y], color=GRADE, linewidth=6.0,
                solid_capstyle="round", zorder=2)
        for valor, rotulo in marcos:
            ax.plot([valor], [y], "o", color=cor, markersize=9, zorder=4)
            ax.text(valor, y + 0.19, rotulo, ha="center", va="bottom",
                    fontsize=6.8, color=cor, linespacing=1.25)
            ax.text(valor, y - 0.20, f"{valor}%", ha="center", va="top",
                    fontsize=7.4, color=TINTA2)

    ax.set_yticks(range(len(trilhas)))
    ax.set_yticklabels([t[0] for t in trilhas][::-1], fontsize=8.2)
    _eixos(ax, "", "", "")
    ax.set_xlabel("redução do consumo de água potável exigida (%)",
                  color=TINTA2, fontsize=9)
    ax.set_xlim(-3, 106)
    ax.set_xticks(range(0, 101, 10))
    ax.set_ylim(-0.6, len(trilhas) - 0.25)
    ax.grid(axis="y", visible=False)

    fig.tight_layout()
    _gravar(fig, "fig37_certificacoes.png")


# ══════════════════════════════════════════════════════════════════════════════
# A fração atendível: percentual onde se digita, e o marcador de valor suspeito
# ══════════════════════════════════════════════════════════════════════════════

def info_percentual():
    # Os textos do aviso vêm da mesma função que a interface usa, para que a
    # figura não possa descrever um marcador diferente do que o programa mostra.
    raiz = str(AQUI.parent)
    if raiz not in sys.path:
        sys.path.insert(0, raiz)
    from netuno.core.fracao_atendivel import aviso_percentual_pequeno

    fig, ax = _tela(100, 46, (7.4, 3.3), "")
    estados = [
        ("40", AZUL, "#ffffff", "aceito", "40% da demanda"),
        ("0,4", LARANJA, CLARO[LARANJA], "aceito, e assinalado",
         "digitou a fração?" + NL + "se quis 40%, digite 40"),
        ("", "#eab308", "#fef08a", "pendente", "campo vazio:" + NL + "falta preencher"),
    ]
    for i, (valor, cor, fundo, estado, leitura) in enumerate(estados):
        x = 1 + i * 33
        _confinar(ax.text(x + 15.5, 40.5, "Substituição por água" + NL + "de chuva (%)",
                          ha="center", va="center", fontsize=7.6, color=TINTA2,
                          linespacing=1.25), (x, 37, x + 31, 45))
        ax.add_patch(FancyBboxPatch(
            (x + 4, 27), 23, 7, boxstyle="round,pad=0.0,rounding_size=0.8",
            linewidth=1.8, edgecolor=cor, facecolor=fundo, zorder=3))
        ax.text(x + 6, 30.5, valor or "—", ha="left", va="center", fontsize=10,
                color=TINTA if valor else CINZA, zorder=5)
        _confinar(ax.text(x + 15.5, 21.5, estado, ha="center", va="center",
                          fontsize=8.4, color=cor, fontweight="bold", zorder=5),
                  (x, 18, x + 31, 25))
        _confinar(ax.text(x + 15.5, 12.5, leitura, ha="center", va="center",
                          fontsize=7.6, color=TINTA2, linespacing=1.35, zorder=5),
                  (x, 7, x + 31, 18))
    aviso = aviso_percentual_pequeno(0.4)
    assert aviso and "digite 40" in aviso, aviso
    _gravar(fig, "fig46b_percentual.png")


def main():
    print("infográficos que substituem tabelas:")
    info_dimensoes()
    info_leitores()
    info_etapas()
    info_atendimento()
    info_desinfeccao()
    info_motores()
    info_codigos()
    info_regimes_base()
    info_inventario()
    info_escoamento()
    info_classes()
    info_certificacoes()
    info_percentual()


if __name__ == "__main__":
    main()
