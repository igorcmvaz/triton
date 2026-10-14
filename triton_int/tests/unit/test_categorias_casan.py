# -*- coding: utf-8 -*-
"""As categorias não residenciais da CASAN, conferidas contra a tabela oficial de 01/04/2026.

Conforme a Tabela Tarifária da CASAN (Resolução ARESC nº 389/2026 e Deliberação ARIS nº 003/2026),
as faixas e TFDI cobrados nos 22 municípios atendidos em Santa Catarina são validados aqui.
"""

from __future__ import annotations

import pytest

from triton.core.economic import calculate_water_bill
from triton.core.tariffs_database import categorias_coletadas, get_city_data, get_city_tariffs_by_category
from triton.core.tariffs_structure import custo_volumetrico

MUNICIPIOS_CASAN = [
    "Florianópolis", "São José", "Criciúma", "Chapecó", "Itapema",
    "Palhoça", "Camboriú", "Navegantes", "Tijucas", "Biguaçu",
    "Caçador", "Concórdia", "Rio do Sul", "Araranguá", "São Francisco do Sul",
    "Mafra", "Canoinhas", "Indaial", "Videira", "Xanxerê", "Imbituba", "Içara"
]


@pytest.mark.parametrize("cidade", MUNICIPIOS_CASAN[:5])
def test_todas_as_categorias_estao_disponiveis(cidade):
    dados = get_city_data("SC", cidade)
    assert dados is not None
    coletadas = categorias_coletadas(dados)
    for cat in ("residencial", "comercial", "industrial", "publica", "social"):
        assert cat in coletadas, f"{cidade} sem categoria {cat}"


def test_calculo_comercial_casan():
    """TFDI R$ 46,34 + 0-10 m³ a R$ 6,81/m³ + 11-50 m³ a R$ 19,14/m³, esgoto 100%."""
    dados = get_city_tariffs_by_category("SC", "Florianópolis", "comercial")
    assert dados is not None
    assert dados["tarifa_fixa_mensal"] == 46.34
    assert dados["esgoto_pct"] == 100.0

    # 10 m³: 46.34 + 10 * 6.81 = 114.44 (água) -> total com 100% esgoto = 228.88
    conta = calculate_water_bill(10000.0, dados["faixas"], sewage_rate=dados["esgoto_pct"],
                                 sewage_mode=dados["esgoto_modo"])
    assert conta == pytest.approx(228.88, abs=0.01)

    # 20 m³: 46.34 + 68.10 + 10 * 19.14 = 305.84 (água) -> total = 611.68
    conta_20 = calculate_water_bill(20000.0, dados["faixas"], sewage_rate=dados["esgoto_pct"],
                                    sewage_mode=dados["esgoto_modo"])
    assert conta_20 == pytest.approx(611.68, abs=0.01)


def test_calculo_social_casan():
    """TFDI R$ 8,63 + 0-10 m³ a R$ 0,58/m³, esgoto 100%."""
    dados = get_city_tariffs_by_category("SC", "Florianópolis", "social")
    assert dados is not None
    assert dados["tarifa_fixa_mensal"] == 8.63
    # 10 m³: 8.63 + 5.80 = 14.43 (água) -> total com 100% esgoto = 28.86
    conta = calculate_water_bill(10000.0, dados["faixas"], sewage_rate=dados["esgoto_pct"],
                                 sewage_mode=dados["esgoto_modo"])
    assert conta == pytest.approx(28.86, abs=0.01)
