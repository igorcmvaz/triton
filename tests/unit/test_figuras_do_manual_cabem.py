# -*- coding: utf-8 -*-
"""Nenhum texto de figura sai da prancha, e nenhum cobre outro texto.

O professor encontrou, lendo o PDF, rótulos que saíam da caixa em que estavam e
rótulos que caíam uns por cima dos outros. Os dois defeitos são invisíveis no
código — só aparecem quando a figura é desenhada — e voltam sozinhos assim que um
dado muda de tamanho, porque a posição do rótulo foi escolhida para o dado de
ontem.

Este teste redesenha todas as figuras e mede cada texto no renderizador. Leva
cerca de meio minuto, e é o preço de não descobrir o problema no PDF impresso.
"""

import os
import sys

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("matplotlib")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")


@pytest.fixture(scope="module")
def conferencia():
    if not os.path.exists(os.path.join(MANUAL, "conferir_figuras.py")):
        pytest.skip("conferidor de figuras ausente")
    for caminho in (RAIZ, MANUAL):
        if caminho not in sys.path:
            sys.path.insert(0, caminho)
    import conferir_figuras
    return conferir_figuras.conferir()


def test_nenhum_texto_sai_da_prancha(conferencia):
    """Rótulo que passa da borda aparece cortado, ou alarga a figura."""
    problemas, _, _ = conferencia
    assert not problemas, [(n, a[0]) for n, a in problemas[:5]]


def test_nenhum_texto_cobre_outro(conferencia):
    """Dois rótulos sobrepostos são tão ilegíveis quanto um rótulo cortado."""
    _, encobertos, _ = conferencia
    assert not encobertos, encobertos[:5]


def test_nenhuma_frase_ou_titulo_dentro_da_figura(conferencia):
    """O título é a legenda, e a explicação é o texto.

    O professor pediu, lendo o PDF, que as frases e os títulos saíssem de dentro
    das figuras: num manual de engenharia a figura mostra, a legenda identifica,
    e o parágrafo que a chama explica. Por cima do gráfico só o rótulo de painel.
    """
    _, _, frases = conferencia
    assert not frases, frases[:8]
