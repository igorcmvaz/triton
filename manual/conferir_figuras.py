# -*- coding: utf-8 -*-
"""Confere que nenhum texto das figuras sai da prancha nem cobre outro texto.

Há três maneiras de um rótulo estragar uma figura: sair da caixa em que foi
posto, sair da própria prancha, e cair em cima de outro rótulo. A primeira os
geradores já resolvem sozinhos, medindo cada rótulo contra a sua caixa na hora
de gravar. As outras duas são o que esta conferência procura, redesenhando todas
as figuras e medindo cada texto no renderizador.

Todas as três apareceram de verdade neste manual, e nenhuma delas se enxerga
lendo o código: só medindo o desenho pronto.

Executar a partir da raiz do programa:
    python manual/conferir_figuras.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

RAIZ = Path(__file__).resolve().parent.parent
AQUI = Path(__file__).resolve().parent
for caminho in (str(RAIZ), str(AQUI)):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

import matplotlib                                                 # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402

#: Os geradores que desenham figuras do manual.
MODULOS = [
    "gerar_desenhos", "gerar_desenhos_metodo", "gerar_desenhos_esquemas",
    "gerar_infograficos", "gerar_infograficos2",
    "gerar_figuras", "gerar_figuras_extra", "gerar_figuras_chuva",
    "gerar_figuras_decisao",
]

#: Quanto um texto pode passar dos limites do eixo, em fração da dimensão. As
#: notas de rodapé das pranchas ficam abaixo do desenho de propósito.
TOLERANCIA_ABAIXO = 0.32
TOLERANCIA_LATERAL = 0.06
TOLERANCIA_ACIMA = 0.10

#: Abaixo destas frações, dois textos apenas se encostam.
CORTE_HORIZONTAL = 0.06
CORTE_VERTICAL = 0.30


def _medidas(fig):
    fig.canvas.draw()
    return fig.canvas.get_renderer()


def _fora(fig):
    """Os textos que passam dos limites toleráveis do eixo."""
    desenho = _medidas(fig)
    achados = []
    for ax in fig.axes:
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        larg, alt = abs(x1 - x0), abs(y1 - y0)
        for artista in ax.texts:
            if not artista.get_text().strip():
                continue
            caixa = artista.get_window_extent(renderer=desenho)
            (ex0, ey0), (ex1, ey1) = ax.transData.inverted().transform(caixa)
            if (ex0 < x0 - larg * TOLERANCIA_LATERAL
                    or ex1 > x1 + larg * TOLERANCIA_LATERAL
                    or ey1 > y1 + alt * TOLERANCIA_ACIMA
                    or ey0 < y0 - alt * TOLERANCIA_ABAIXO):
                achados.append((artista.get_text().replace(chr(10), " ")[:44],
                                round(ex0, 1), round(ex1, 1),
                                round(ey0, 1), round(ey1, 1),
                                round(x0, 1), round(x1, 1),
                                round(y0, 1), round(y1, 1)))
    return achados


def _sobrepostos(fig):
    """Os pares de texto que se cobrem, no mesmo eixo."""
    desenho = _medidas(fig)
    achados = []
    for ax in fig.axes:
        caixas = [(a, a.get_window_extent(renderer=desenho))
                  for a in ax.texts if a.get_text().strip()]
        for i in range(len(caixas)):
            for j in range(i + 1, len(caixas)):
                a, ca = caixas[i]
                b, cb = caixas[j]
                largura = min(ca.x1 - ca.x0, cb.x1 - cb.x0)
                altura = min(ca.y1 - ca.y0, cb.y1 - cb.y0)
                if largura <= 0 or altura <= 0:
                    continue
                corte_x = min(ca.x1, cb.x1) - max(ca.x0, cb.x0)
                corte_y = min(ca.y1, cb.y1) - max(ca.y0, cb.y0)
                if (corte_x > largura * CORTE_HORIZONTAL
                        and corte_y > altura * CORTE_VERTICAL):
                    achados.append((a.get_text().replace(chr(10), " ")[:30],
                                    b.get_text().replace(chr(10), " ")[:30]))
    return achados


def conferir():
    """Roda cada gerador com a gravação interceptada, e mede antes de salvar."""
    problemas, encobertos = [], []

    def examinar(fig, nome):
        for achado in _fora(fig):
            problemas.append((nome, achado))
        for a, b in _sobrepostos(fig):
            encobertos.append((nome, a, b))
        plt.close(fig)
        print(f"  {nome}")

    for nome_modulo in MODULOS:
        modulo = __import__(nome_modulo)

        if hasattr(modulo, "_gravar"):
            def gravar(fig, nome, _mod=modulo):
                if getattr(_mod, "_CONFINADOS", None):
                    _mod._ajustar_textos(fig, fig.axes[0])
                examinar(fig, nome)

            modulo._gravar = gravar

        if hasattr(modulo, "_salvar"):
            modulo._salvar = examinar

        if hasattr(modulo, "Prancha"):
            def salvar(self, nome):
                self.conferir()
                self._ajustar_rotulos()
                self._ajustar_notas()
                examinar(self.fig, nome)

            modulo.Prancha.salvar = salvar

        print(nome_modulo + ":")
        modulo.main()

    return problemas, encobertos


def main():
    problemas, encobertos = conferir()
    print()
    if problemas:
        print(f"{len(problemas)} texto(s) fora da prancha:")
        for nome, (texto, ex0, ex1, ey0, ey1, x0, x1, y0, y1) in problemas:
            print(f"  {nome}: «{texto}»")
            print(f"      texto [{ex0}, {ex1}] x [{ey0}, {ey1}]  "
                  f"prancha [{x0}, {x1}] x [{y0}, {y1}]")
    if encobertos:
        print(f"{len(encobertos)} par(es) de texto sobrepostos:")
        for nome, a, b in encobertos:
            print(f"  {nome}: «{a}»  sobre  «{b}»")
    if not problemas and not encobertos:
        print("nenhum texto fora da prancha, nenhum texto sobreposto.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
