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

import pytest

from netuno.core.cost_estimates import (
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

def test_o_preco_nunca_cai_quando_o_volume_sobe():
    """Era o defeito: 1.750 L custava R$ 1.399 e 2.000 L custava R$ 1.299."""
    for tabela, nome in ((LOWER_TANK_PRICE_TABLE, "inferior"), (UPPER_TANK_PRICE_TABLE, "superior")):
        pares = sorted((float(v), float(p)) for v, p in tabela)
        precos = [p for _, p in pares]
        assert precos == sorted(precos), f"tabela {nome} não é monotônica: {pares}"


def test_a_curva_interpolada_e_monotonica_em_toda_a_faixa_de_uso():
    """A monotonicidade da tabela não basta: a curva entre os pontos também precisa dela."""
    anterior = -1.0
    for litros in range(100, 60_001, 100):
        preco = interpolate_price(LOWER_TANK_PRICE_TABLE, litros)
        assert preco >= anterior, f"preço caiu em {litros} L"
        anterior = preco


def test_volume_nulo_nao_custa_nada():
    assert interpolate_price(LOWER_TANK_PRICE_TABLE, 0.0) == 0.0
    assert estimate_tank_price(0.0, "PEAD") == 0.0


# ────────────────────── dentro da tabela: o valor observado ────────────────────

def test_nos_pontos_tabelados_a_estimativa_devolve_o_preco_tabelado():
    """É o vínculo com o banco: se a interpolação se soltar dele, este teste cai."""
    for volume, preco in LOWER_TANK_PRICE_TABLE:
        assert estimate_tank_price(volume, "PEAD") == pytest.approx(preco), volume


def test_entre_dois_pontos_a_estimativa_fica_entre_os_dois_precos():
    pares = sorted((float(v), float(p)) for v, p in LOWER_TANK_PRICE_TABLE)
    for (v1, p1), (v2, p2) in zip(pares, pares[1:]):
        meio = (v1 + v2) / 2.0
        assert p1 <= interpolate_price(LOWER_TANK_PRICE_TABLE, meio) <= p2, (v1, v2)


def test_o_material_multiplica_o_preco_de_referencia():
    pead = estimate_tank_price(5000.0, "PEAD")
    for material in ("CONCRETO", "PRFV", "ACO_INOX"):
        assert estimate_tank_price(5000.0, material) > pead, material


# ─────────────────── fora da tabela: a regressão sobre o banco ─────────────────

def test_a_regressao_descreve_bem_a_tabela():
    """Se o R² não for alto, a reta não serve para extrapolar, e o código sabe disso."""
    reg = get_tank_linear_regression("PEAD")
    assert reg["r_squared"] >= R2_MINIMO_PARA_EXTRAPOLAR
    assert reg["slope_r_per_l"] > 0.0
    assert reg["n_pontos"] == len(LOWER_TANK_PRICE_TABLE)
    assert reg["volume_maximo_tabelado_l"] == max(float(v) for v, _ in LOWER_TANK_PRICE_TABLE)


def test_a_extrapolacao_segue_a_regressao_e_nao_os_dois_ultimos_pontos():
    """É a ligação pedida: a referência é o banco inteiro, não o par final.

    Uma promoção no maior volume tabelado girava a reta inteira quando só os dois
    últimos pontos a definiam.
    """
    reg = get_tank_linear_regression("PEAD")
    maximo = reg["volume_maximo_tabelado_l"]
    for volume in (maximo * 1.5, maximo * 2.0, maximo * 3.0):
        esperado = reg["slope_r_per_l"] * volume + reg["intercept_r"]
        assert interpolate_price(LOWER_TANK_PRICE_TABLE, volume) == pytest.approx(esperado, rel=1e-9)


def test_a_extrapolacao_nunca_fica_abaixo_do_ultimo_preco_tabelado():
    """Reservatório maior não custa menos, mesmo que a reta ajustada diga que sim."""
    tabela_ruim = [(1000.0, 500.0), (2000.0, 900.0), (3000.0, 905.0)]
    ultimo = 905.0
    for volume in (3100.0, 5000.0, 20000.0):
        assert interpolate_price(tabela_ruim, volume) >= ultimo


def test_ajuste_ruim_cai_no_metodo_local():
    """Uma reta que não descreve a tabela é pior que a inclinação local.

    O degrau abaixo derruba o R², e nesse caso a extrapolação volta a usar os
    dois últimos pontos, que ao menos descrevem o trecho final.
    """
    degrau = [(100.0, 100.0), (200.0, 105.0), (300.0, 110.0), (400.0, 9000.0)]
    assert regressao_linear_da_tabela(degrau)["r_squared"] < R2_MINIMO_PARA_EXTRAPOLAR
    inclinacao_local = (9000.0 - 110.0) / 100.0
    assert interpolate_price(degrau, 500.0) == pytest.approx(9000.0 + inclinacao_local * 100.0)


def test_a_regressao_de_tabela_curta_nao_estoura():
    assert regressao_linear_da_tabela([])["r_squared"] == 0.0
    assert regressao_linear_da_tabela([(1000.0, 500.0)])["slope_r_per_l"] == 0.0


def test_a_regressao_acompanha_o_material():
    pead = get_tank_linear_regression("PEAD")["slope_r_per_l"]
    inox = get_tank_linear_regression("ACO_INOX")["slope_r_per_l"]
    assert inox > pead


def test_a_regressao_da_caixa_superior_usa_a_tabela_da_caixa_superior():
    sup = get_tank_linear_regression("PEAD", is_upper=True)
    assert sup["is_upper"] is True
    assert sup["n_pontos"] == len(UPPER_TANK_PRICE_TABLE)
    assert sup["volume_maximo_tabelado_l"] <= get_tank_linear_regression("PEAD")["volume_maximo_tabelado_l"]


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

def test_a_tabela_de_recurso_espelha_o_banco():
    """Corrigir o JSON não bastava.

    `load_costs_database` cai numa tabela embutida quando o arquivo não está
    legível, e essa tabela guardava a versão antiga, com 1.750 L a R$ 1.399 e
    2.000 L a R$ 1.299. Bastava o arquivo faltar — instalação nova, permissão
    negada, JSON corrompido — para o programa voltar a cobrar menos por um
    reservatório maior, sem aviso nenhum.
    """
    from netuno.core.cost_estimates import (
        _DEFAULT_LOWER_TANK_PRICES,
        _DEFAULT_UPPER_TANK_PRICES,
    )

    db = load_costs_database()
    for recurso, chave in (
        (_DEFAULT_LOWER_TANK_PRICES, "lower_tank_pead_prices"),
        (_DEFAULT_UPPER_TANK_PRICES, "upper_tank_pead_prices"),
    ):
        do_banco = [(float(v), float(p)) for v, p in db[chave]]
        do_recurso = [(float(v), float(p)) for v, p in recurso]
        assert do_recurso == do_banco, chave


def test_a_tabela_de_recurso_tambem_e_monotonica():
    """A verificação da monotonicidade tem de alcançar o caminho de recurso."""
    from netuno.core.cost_estimates import (
        _DEFAULT_LOWER_TANK_PRICES,
        _DEFAULT_UPPER_TANK_PRICES,
    )

    for tabela in (_DEFAULT_LOWER_TANK_PRICES, _DEFAULT_UPPER_TANK_PRICES):
        precos = [float(p) for _, p in sorted(tabela)]
        assert precos == sorted(precos), tabela
