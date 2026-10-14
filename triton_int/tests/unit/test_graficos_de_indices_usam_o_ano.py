# -*- coding: utf-8 -*-
"""Os gráficos anuais de índices precisam mostrar o ano, e não a posição.

`IndicesCalculator.compute_climate_indices()` devolve o ano numa **coluna**, e
deixa o índice do DataFrame posicional. Os três gráficos anuais liam o índice e
rotulavam o eixo «Ano» com 0, 1, 2 e assim por diante, o que aparecia tanto na
tela quanto nas figuras do manual geradas a partir dela.

O defeito é da mesma família dos demais deste repositório: um valor correto
calculado num lugar e descartado antes de chegar a quem o consome.
"""

import os
from datetime import datetime, timedelta

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6")
pd = pytest.importorskip("pandas")

from triton.core.calculator import IndicesCalculator          # noqa: E402

PRIMEIRO_ANO = 1980
ANOS = 5


@pytest.fixture(scope="module")
def indices():
    inicio = datetime(PRIMEIRO_ANO, 1, 1)
    dias = (ANOS + 1) * 366
    datas = [inicio + timedelta(days=i) for i in range(dias)]
    # Chuva sintética: o valor não importa, a data importa.
    chuva = [float((i % 17) * 1.3) for i in range(dias)]
    calc = IndicesCalculator(list(zip(datas, chuva)))
    return calc.compute_climate_indices()


@pytest.fixture(scope="module")
def aplicacao():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


def _anos_no_eixo(widget):
    eixo = widget.figure.axes[0]
    valores = []
    for colecao in eixo.containers:
        for barra in colecao:
            valores.append(barra.get_x() + barra.get_width() / 2.0)
    for linha in eixo.lines:
        dados = list(linha.get_xdata())
        # A linha da média é traçada em coordenadas de eixo, de 0 a 1, e não
        # representa ano nenhum.
        if len(dados) == 2 and dados == [0, 1]:
            continue
        valores.extend(dados)
    return [v for v in valores if v is not None]


def test_o_calculador_devolve_o_ano_numa_coluna(indices):
    """Se isto mudar, os gráficos precisam mudar junto."""
    assert "year" in indices.columns
    assert int(indices["year"].iloc[0]) == PRIMEIRO_ANO
    assert len(indices) >= ANOS


@pytest.mark.parametrize("classe", [
    "PrcptotAnnualChart", "SdiiVsR95pChart", "CddCwdAnnualChart",
])
def test_o_eixo_anual_traz_o_ano_e_nao_a_posicao(aplicacao, indices, classe):
    """Um eixo rotulado «Ano» que vai de 0 a 4 não é um eixo de anos."""
    import triton.ui.charts as charts

    grafico = getattr(charts, classe)()
    grafico.plot_data(indices)
    valores = _anos_no_eixo(grafico)
    assert valores, classe
    assert min(valores) >= PRIMEIRO_ANO - 1, (classe, min(valores))
    assert max(valores) <= PRIMEIRO_ANO + ANOS + 2, (classe, max(valores))
