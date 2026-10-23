"""A fórmula exponencial da CORSAN: Água = PB × Cⁿ + serviço básico.

A CORSAN não cobra por faixas. O expoente ``n`` sai da Tabela de Exponenciais pelo
consumo do mês inteiro e se aplica a todo o volume: 1,00 até 20 m³, subindo até
1,13 entre 101 e 150 m³. Só a categoria industrial tem teto (1.000 m³); a tabela
sintética abaixo usa um teto para exercitar o excedente. O esgoto é cobrado por m³
consumido, sem serviço básico nem expoente. Antes da 0.1.0 esses municípios estavam
gravados como uma reta, ``PB × C + SB``, com esgoto de 70% sobre a conta inteira.
"""

import json
from pathlib import Path

import pytest

from triton.core.economic import calculate_water_bill
from triton.core.tariff_regimes import EXPONENCIAL, ler_estrutura, resumo_do_regime, validar_estrutura
from triton.core.tariffs_database import get_city_data, get_city_tariffs_by_category

RAIZ = Path(__file__).resolve().parents[2]

#: Uma tabela com três linhas, para que o expoente mude com o consumo.


def test_os_34_municipios_da_corsan_estao_na_formula_exponencial():
    base = json.loads((RAIZ / "triton" / "data" / "brazil_cities_tariffs.json").read_text(encoding="utf-8"))
    corsan = {k: v for k, v in base["cities"].items() if "CORSAN" in v["prestador_saneamento"].upper()}
    assert len(corsan) == 34
    for chave, dados in corsan.items():
        assert dados["regime_tarifario"] == EXPONENCIAL, chave
        assert ler_estrutura(dados["faixas"]).regime == EXPONENCIAL, chave
        erros = [a for a in validar_estrutura(dados) if a.gravidade == "erro"]
        assert erros == [], (chave, erros)


def _tabela_oficial():
    return json.loads((RAIZ / "tarifas" / "tabela_exponencial_corsan.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("consumo, basica", [
    (1, 1.0), (20, 1.0), (21, 1.01), (25, 1.05), (29, 1.08), (30, 1.09), (31, 1.09),
    (36, 1.10), (46, 1.11), (101, 1.13), (151, 1.1287), (501, 1.12), (1001, 1.11), (9001, 1.0858),
])
def test_a_tabela_transcrita_confere_com_a_da_corsan(consumo, basica):
    """Linhas lidas da Tabela de Exponenciais, coluna Básica (Residencial B)."""
    tabela = _tabela_oficial()
    coluna = tabela["colunas"].index("BASICA")
    linha = next(l for l in tabela["linhas"] if l[0] == consumo)
    assert linha[coluna] == basica
    assert tabela["verificada"] is True


def test_a_conta_de_alegrete_reproduz_a_tabela_tarifaria():
    """10 m³ é a «tarifa mínima sem HD» do ANEXO-5: R$ 134,89 = 43,39 + 9,15 × 10."""
    faixas = [tuple(f) for f in get_city_data("RS", "Alegrete")["faixas"]]

    def agua(m3):
        return calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=1, sewage_rate=0.0)

    assert agua(10) == pytest.approx(134.89)
    assert agua(21) == pytest.approx(43.39 + 9.15 * 21 ** 1.01)
    assert agua(150) == pytest.approx(43.39 + 9.15 * 150 ** 1.13)
    # Sem teto no residencial: a 2.000 m³ ainda vale a fórmula, com n = 1,11.
    assert agua(2000) == pytest.approx(43.39 + 9.15 * 2000 ** 1.11)


@pytest.mark.parametrize("uf, cidade, minima", [
    ("RS", "Alegrete", 134.89), ("RS", "Erechim", 102.45), ("RS", "Santa Cruz do Sul", 116.60),
    ("RS", "Canoas", 128.00), ("RS", "Esteio", 128.00),  # ANEXO-3, Residencial B
])
def test_a_tarifa_minima_sem_hidrometro_bate_com_cada_tabela(uf, cidade, minima):
    faixas = [tuple(f) for f in get_city_data(uf, cidade)["faixas"]]
    assert calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=0.0) == pytest.approx(minima)


def test_o_manual_compoe_o_expoente_sobrescrito():
    """Com espaço em volta do ^, o mathtext punha o expoente na linha de base."""
    import sys

    if not (RAIZ / "manual" / "gerar_equacoes.py").is_file():
        pytest.skip("gerador do manual ausente neste clone (fica no disco do mantenedor)")
    sys.path.insert(0, str(RAIZ / "manual"))
    import gerar_equacoes

    assert gerar_equacoes.para_tex("T_agua = PB × C^n + SB").count("C^{n}") == 1
    assert "( 1 + i )^{m - 1}" in gerar_equacoes.para_tex("f_inf = ( 1 + i )^( m − 1 )")
    assert "^{2}" in gerar_equacoes.para_tex("A = x²")
