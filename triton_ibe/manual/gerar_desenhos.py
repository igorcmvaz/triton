# -*- coding: utf-8 -*-
"""Desenhos explicativos do manual.

As figuras de `gerar_figuras.py` mostram **resultados**; estas mostram o
**sistema**. Servem ao leitor que está chegando agora: antes de discutir
potencial de economia, é preciso saber o que é um sistema de aproveitamento de
água pluvial e por onde a água passa.

Cada seta é declarada como ligação entre duas caixas nomeadas, e um verificador
confere que as duas pontas encostam numa caixa existente. Foi assim que as setas
soltas do mapa de processos foram eliminadas, e a mesma disciplina vale aqui.

Saída: manual/figuras/fig00*.png
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch    # noqa: E402

AQUI = Path(__file__).resolve().parent
FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

# A mesma paleta das figuras de resultado.
AZUL = "#2a78d6"
LARANJA = "#eb6834"
VERDE = "#0ca30c"
ROXO = "#7d5fb0"
TINTA = "#0b0b0b"
TINTA2 = "#52514e"
SUPERFICIE = "#fcfcfb"
CINZA = "#8a8880"

NL = chr(10)


def rotulo_de_painel(ax, titulo):
    """Só o rótulo de painel, «(a)», «(b)», entra na figura.

    O título da figura é a legenda abaixo dela, à maneira da ABNT; uma frase
    escrita por cima do gráfico repete a legenda ou, pior, a contradiz.
    """
    if re.fullmatch(r"\([a-z]\)( [^.;:]{1,40})?", (titulo or "").strip()):
        ax.set_title(titulo.strip(), color=TINTA, fontsize=10,
                     fontweight="bold", loc="left", pad=6)


class Prancha:
    """Uma prancha de desenho com caixas nomeadas e setas entre elas."""

    def __init__(self, largura, altura, tamanho=(7.4, 4.4)):
        self.fig, self.ax = plt.subplots(figsize=tamanho)
        self.fig.patch.set_facecolor(SUPERFICIE)
        self.ax.set_facecolor(SUPERFICIE)
        self.ax.set_xlim(0, largura)
        self.ax.set_ylim(0, altura)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.caixas = {}
        self.ligacoes = []
        self.confinados = []
        self.notas = []

    def caixa(self, nome, x, y, w, h, rotulo, cor=AZUL, fundo="#ffffff",
              tinta=TINTA, tamanho=8.2, tracejada=False, peso="normal"):
        self.ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.0,rounding_size=1.2",
            linewidth=1.4, edgecolor=cor, facecolor=fundo, zorder=3,
            linestyle="--" if tracejada else "-"))
        artista = self.ax.text(
            x + w / 2.0, y + h / 2.0, rotulo, ha="center", va="center",
            fontsize=tamanho, color=tinta, zorder=4, linespacing=1.35,
            fontweight=peso)
        # O rótulo não pode sair da caixa. Medir depois de desenhado é a única
        # forma exata: estimar pela contagem de caracteres erra nos acentos e
        # nas palavras longas, que são justamente as que vazam.
        self.confinados.append((artista, (x, y, x + w, y + h)))
        self.caixas[nome] = (x, y, w, h)
        return nome

    def _ajustar_rotulos(self):
        """Encolhe o rótulo que não couber, e uniformiza o que sobrou.

        Encolher só a caixa que vaza deixaria letra menor ao lado de letra
        maior; por isso todos os rótulos que partiram do mesmo corpo terminam
        no menor corpo a que algum deles precisou descer.
        """
        if not self.confinados:
            return
        self.fig.canvas.draw()
        desenho = self.fig.canvas.get_renderer()
        originais = [a.get_fontsize() for a, _ in self.confinados]
        apertados = []
        for artista, (x0, y0, x1, y1) in self.confinados:
            while True:
                caixa = artista.get_window_extent(renderer=desenho)
                (ex0, ey0), (ex1, ey1) =                     self.ax.transData.inverted().transform(caixa)
                if (ex0 >= x0 + 0.8 and ex1 <= x1 - 0.8
                        and ey0 >= y0 + 0.3 and ey1 <= y1 - 0.3):
                    break
                corpo = artista.get_fontsize() * 0.94
                if corpo < 5.6:
                    apertados.append(
                        artista.get_text().replace(NL, " ")[:40])
                    break
                artista.set_fontsize(corpo)
                self.fig.canvas.draw()
                desenho = self.fig.canvas.get_renderer()
        if apertados:
            raise AssertionError(
                "rótulo que não cabe na caixa: " + "; ".join(apertados))
        menor = {}
        for (artista, _), original in zip(self.confinados, originais):
            chave = round(original, 2)
            menor[chave] = min(menor.get(chave, original),
                               artista.get_fontsize())
        for (artista, _), original in zip(self.confinados, originais):
            artista.set_fontsize(menor[round(original, 2)])

    def _ancora(self, nome, lado):
        x, y, w, h = self.caixas[nome]
        return {
            "d": (x + w, y + h / 2.0), "e": (x, y + h / 2.0),
            "c": (x + w / 2.0, y + h), "b": (x + w / 2.0, y),
            "cd": (x + w * 0.78, y + h), "bd": (x + w * 0.78, y),
            "ce": (x + w * 0.22, y + h), "be": (x + w * 0.22, y),
        }[lado]

    def seta(self, de, lado_de, para, lado_para, rotulo="", cor=AZUL,
             curva=0.0, rotulo_em=None, tracejada=False, tamanho=7.4):
        p1 = self._ancora(de, lado_de)
        p2 = self._ancora(para, lado_para)
        self.ax.add_patch(FancyArrowPatch(
            p1, p2, arrowstyle="-|>", mutation_scale=11, linewidth=1.3,
            color=cor, zorder=2, shrinkA=1.5, shrinkB=1.5,
            linestyle="--" if tracejada else "-",
            connectionstyle="arc3,rad=" + str(curva)))
        if rotulo:
            if rotulo_em is None:
                mx = (p1[0] + p2[0]) / 2.0
                my = (p1[1] + p2[1]) / 2.0
            else:
                mx, my = rotulo_em
            self.ax.text(mx, my, rotulo, ha="center", va="center",
                         fontsize=tamanho, color=cor, zorder=5,
                         bbox=dict(boxstyle="round,pad=0.2", fc=SUPERFICIE,
                                   ec="none"))
        self.ligacoes.append((de, para))

    def nota(self, x, y, texto, cor=TINTA2, tamanho=7.6):
        """Uma nota que não passa da largura da prancha.

        As quebras de linha escritas à mão envelhecem: basta trocar uma palavra
        para a linha passar da borda. A nota é remontada num parágrafo só e
        requebrada até caber, medida no renderizador.
        """
        artista = self.ax.text(x, y, texto, ha="left", va="top",
                               fontsize=tamanho, color=cor, linespacing=1.45,
                               zorder=4)
        self.notas.append((artista, x))
        return artista

    def _ajustar_notas(self):
        import textwrap

        if not self.notas:
            return
        _, limite = self.ax.get_xlim()
        self.fig.canvas.draw()
        desenho = self.fig.canvas.get_renderer()
        for artista, x in self.notas:
            paragrafo = " ".join(artista.get_text().split())
            largura = max(len(l) for l in artista.get_text().split(NL))
            while True:
                caixa = artista.get_window_extent(renderer=desenho)
                (_, _), (direita, _) =                     self.ax.transData.inverted().transform(caixa)
                if direita <= limite - 1.0 or largura <= 30:
                    break
                largura = int(largura * 0.93)
                artista.set_text(NL.join(textwrap.wrap(paragrafo, largura)))
                self.fig.canvas.draw()
                desenho = self.fig.canvas.get_renderer()

    def titulo(self, texto):
        # O título vai na legenda da figura; na prancha só o rótulo de painel.
        rotulo_de_painel(self.ax, texto)

    def conferir(self):
        """Toda seta precisa sair de uma caixa e chegar noutra caixa."""
        for de, para in self.ligacoes:
            for nome in (de, para):
                if nome not in self.caixas:
                    raise AssertionError("seta ligada a caixa inexistente: " + nome)

    def salvar(self, nome):
        self.conferir()
        self._ajustar_rotulos()
        self._ajustar_notas()
        self.fig.savefig(FIGURAS / nome, dpi=170, bbox_inches="tight",
                         facecolor=SUPERFICIE)
        plt.close(self.fig)
        print("  figuras/" + nome)


# ══════════════════════════════════════════════════════════════════════════════
# Desenho 1 — o sistema inteiro, da chuva ao uso
# ══════════════════════════════════════════════════════════════════════════════

def desenho_sistema():
    p = Prancha(100, 78, tamanho=(7.4, 5.8))

    # Fileira de cima: a captação.
    p.caixa("chuva", 1, 65, 26, 11, "Precipitação sobre" + NL + "a área de captação",
            cor=AZUL, peso="bold")
    p.caixa("calha", 38, 65, 22, 11, "Algerozes e" + NL + "tubos de queda", cor=AZUL)
    p.caixa("descarte", 71, 65, 28, 11,
            "Desvio do" + NL + "escoamento inicial", cor=LARANJA)
    p.caixa("perdido", 71, 50, 28, 9, "Rede pluvial pública", cor=CINZA, tinta=TINTA2,
            tracejada=True)

    # Meio: o armazenamento.
    p.caixa("cisterna", 16, 34, 34, 13,
            "Cisterna" + NL + "(reservatório inferior)", cor=AZUL, peso="bold")
    p.caixa("extravasor", 64, 35, 35, 11,
            "Descarregador de cheias" + NL + "para a rede pluvial", cor=LARANJA)

    # Fileira de baixo: a distribuição.
    p.caixa("bomba", 1, 14, 20, 10, "Grupo eletrobomba", cor=ROXO)
    p.caixa("superior", 32, 13, 24, 12, "Depósito /" + NL + "reservatório superior",
            cor=ROXO, tracejada=True)
    p.caixa("usos", 68, 13, 31, 12, "Usos não potáveis", cor=VERDE,
            peso="bold")
    p.caixa("rede", 68, 0, 31, 9, "Rede pública de abastecimento", cor=CINZA, tinta=TINTA2)

    p.seta("chuva", "d", "calha", "e", "escoamento")
    p.seta("calha", "d", "descarte", "e", "condução")
    p.seta("descarte", "b", "perdido", "c", "primeiros milímetros", cor=LARANJA,
           rotulo_em=(85, 62))
    p.seta("descarte", "be", "cisterna", "cd", "água aproveitável", curva=0.22,
           rotulo_em=(52, 53))
    p.seta("cisterna", "d", "extravasor", "e", "excedente", cor=LARANJA,
           rotulo_em=(57, 44))
    p.seta("cisterna", "be", "bomba", "c", "")
    p.seta("bomba", "d", "superior", "e", "bombagem", cor=ROXO,
           rotulo_em=(26, 22))
    p.seta("superior", "d", "usos", "e", "por gravidade", cor=VERDE,
           rotulo_em=(62, 22))
    p.seta("rede", "c", "usos", "b", "abastecimento complementar", cor=CINZA,
           rotulo_em=(83, 10.5), tamanho=7.0)

    p.salvar("fig00_sistema.png")


# ══════════════════════════════════════════════════════════════════════════════
# Desenho 2 — o destino da chuva de um dia
# ══════════════════════════════════════════════════════════════════════════════

def desenho_destino():
    p = Prancha(100, 64, tamanho=(7.4, 4.8))

    p.caixa("chuva", 1, 51, 24, 11, "Precipitação diária" + NL + "P (mm)",
            cor=AZUL, peso="bold")
    p.caixa("descartada", 36, 51, 26, 11,
            "Desvio do" + NL + "escoamento inicial", cor=LARANJA)
    p.caixa("efetiva", 72, 51, 27, 11, "Precipitação efetiva" + NL + "após o desvio",
            cor=AZUL, peso="bold")

    p.caixa("perdas", 1, 32, 24, 11, "Perdas na" + NL + "cobertura", cor=CINZA,
            tinta=TINTA2, tracejada=True)
    p.caixa("captado", 36, 32, 34, 11,
            "Volume captado" + NL + "chuva × área × coeficiente", cor=AZUL,
            peso="bold", tamanho=7.8)

    p.caixa("transborda", 1, 10, 27, 12,
            "Descarga / corte" + NL + "do excedente", cor=LARANJA)
    p.caixa("consumido", 36, 10, 30, 12,
            "Consumo diário" + NL + "limitado à procura", cor=VERDE,
            peso="bold", tamanho=7.8)
    p.caixa("guardado", 73, 10, 26, 12,
            "Volume armazenado" + NL + "para o dia seguinte", cor=ROXO)

    p.seta("chuva", "d", "descartada", "e", "1.º", cor=LARANJA)
    p.seta("descartada", "d", "efetiva", "e", "2.º")
    p.seta("efetiva", "b", "captado", "cd", "conversão em volume", curva=0.22,
           rotulo_em=(78, 45))
    p.seta("captado", "e", "perdas", "d", "parcela não escoada", cor=CINZA,
           rotulo_em=(30.5, 46.5))
    p.seta("captado", "be", "transborda", "c", "", cor=LARANJA, curva=0.12)
    p.seta("captado", "b", "consumido", "c", "")
    p.seta("captado", "bd", "guardado", "c", "", cor=ROXO, curva=-0.12)

    p.salvar("fig00b_destino.png")


# ══════════════════════════════════════════════════════════════════════════════
# Desenho 3 — que parte do consumo a chuva pode atender
# ══════════════════════════════════════════════════════════════════════════════

def desenho_fracao():
    fig, ax = plt.subplots(figsize=(7.4, 2.1))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    # Ordens de grandeza em Portugal
    usos = [
        ("Duche", 28, False), ("Cozinha e\nbebida", 18, False),
        ("Higiene", 14, False), ("Máquina de\nlavar roupa", 12, False),
        ("Autoclismo", 20, True), ("Limpeza e\nrega", 8, True),
    ]
    esquerda = 0.0
    for nome, pct, atendivel in usos:
        cor = VERDE if atendivel else CINZA
        ax.barh(0, pct, left=esquerda, height=0.5, color=cor,
                edgecolor=SUPERFICIE, linewidth=2.0, zorder=3)
        ax.text(esquerda + pct / 2.0, 0, str(pct) + "%", ha="center",
                va="center", fontsize=8.0, color="white", zorder=4,
                fontweight="bold")
        ax.text(esquerda + pct / 2.0, -0.36, nome, ha="center", va="top",
                fontsize=7.2, color=TINTA2, zorder=4, linespacing=1.3)
        esquerda += pct

    ax.annotate("", xy=(0.3, 0.46), xytext=(71.7, 0.46),
                arrowprops=dict(arrowstyle="<->", color=CINZA, linewidth=1.2))
    ax.text(36, 0.56, "água potável da rede pública: 72%", ha="center", va="bottom",
            fontsize=8.4, color=TINTA2)
    ax.annotate("", xy=(72.3, 0.46), xytext=(99.7, 0.46),
                arrowprops=dict(arrowstyle="<->", color=VERDE, linewidth=1.3))
    ax.text(86, 0.56, "água pluvial: 28%", ha="center", va="bottom",
            fontsize=8.4, color=VERDE, fontweight="bold")

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.axis("off")

    fig.savefig(FIGURAS / "fig00c_fracao.png", dpi=170, bbox_inches="tight",
                facecolor=SUPERFICIE)
    plt.close(fig)
    print("  figuras/fig00c_fracao.png")


def main():
    print("desenhos explicativos:")
    desenho_sistema()
    desenho_destino()
    desenho_fracao()


if __name__ == "__main__":
    main()
