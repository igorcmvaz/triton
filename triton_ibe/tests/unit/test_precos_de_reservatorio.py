"""O preço de reservatório sai do banco de custos, dentro e fora da tabela.

Decisão do professor: manter as duas funções órfãs, e fazer a interpolação usar
o banco como referência.

A tabela anterior misturava fabricantes, e isso aparecia como defeito de física
do preço:

    1.750 L → R$ 1.399,00
    2.000 L → R$ 1.299,00

Um reservatório **maior** custava **menos**. O par vinha de marcas diferentes, e
a interpolação entre eles devolvia preço decrescente com o volume numa faixa que
é justamente a residencial.

Dentro da tabela vale a interpolação ponto a ponto, porque cada ponto é um preço
observado. Fora dela não há ponto nenhum, e a extrapolação passa a usar a
regressão ajustada sobre o banco inteiro, que é o que
`get_tank_linear_regression` calcula e que até aqui não tinha chamador. O
critério anterior era a inclinação dos dois últimos pontos, o par mais sensível a
ruído de varejo de toda a série.
"""

from __future__ import annotations


from triton.core.cost_estimates import (
    LOWER_TANK_PRICE_TABLE,
    R2_MINIMO_PARA_EXTRAPOLAR,
    UPPER_TANK_PRICE_TABLE,
    estimate_tank_price,
    get_tank_linear_regression,
    interpolate_price,
    load_costs_database,
    regressao_linear_da_tabela,
)


# ─────────────────────────── a física do preço ─────────────────────────────────


# ────────────────────── dentro da tabela: o valor observado ────────────────────


# ─────────────────── fora da tabela: a regressão sobre o banco ─────────────────


# ────────────────────────────── procedência do dado ────────────────────────────

def test_o_banco_declara_de_onde_vieram_os_precos():
    """Preço de varejo sem data e sem fonte não é auditável.

    A tabela anterior não dizia de onde vinha, e foi por isso que a mistura de
    fabricantes passou despercebida.
    """
    proc = load_costs_database().get("_procedencia_precos_reservatorio")
    assert proc, "o banco de custos não declara a procedência dos preços"
    for campo in ("fabricante", "varejista", "coletado_em", "criterio", "alcance"):
        assert proc.get(campo), campo
    assert proc["coletado_em"].startswith("20")


# ─────────────── a tabela de recurso não pode divergir do banco ────────────────
