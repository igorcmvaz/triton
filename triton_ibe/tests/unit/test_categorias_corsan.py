"""As categorias não residenciais da CORSAN, conferidas contra as tabelas oficiais.

Cada tabela tarifária traz, por categoria, a «tarifa mínima sem hidrômetro»: a conta de
água de um consumo presumido (20 m³ na Comercial e na Pública, 30 m³ na Industrial),
calculada pela fórmula PB × Cⁿ + serviço básico. São números impressos pela CORSAN, e a
estrutura gravada no banco tem de reproduzi-los ao centavo.
"""

from __future__ import annotations

import pytest

from triton.core.economic import calculate_water_bill
from triton.core.tariffs_database import categorias_coletadas, get_city_data, get_city_tariffs_by_category
from triton.core.tariffs_structure import custo_volumetrico

# (município, categoria, consumo presumido em m³, tarifa mínima sem HD da Tabela I)
TARIFA_MINIMA_SEM_HD = [
    ("Alegrete", "comercial", 20, 285.61),     # ANEXO-5
    ("Alegrete", "publica", 20, 362.84),
    ("Alegrete", "industrial", 30, 547.66),
    ("Canoas", "comercial", 20, 271.08),       # ANEXO-3
    ("Canoas", "publica", 20, 344.39),
    ("Erechim", "comercial", 20, 216.79),
    ("Erechim", "publica", 20, 275.40),
    ("Santa Cruz do Sul", "comercial", 20, 246.52),
    ("Santa Cruz do Sul", "publica", 20, 313.24),
]


@pytest.mark.parametrize("cidade,categoria,consumo,esperado", TARIFA_MINIMA_SEM_HD)
def test_a_estrutura_reproduz_a_tabela_oficial(cidade, categoria, consumo, esperado):
    dados = get_city_tariffs_by_category("RS", cidade, categoria)
    assert dados is not None, f"{cidade}: {categoria} não coletada"
    agua = custo_volumetrico(dados["faixas"], consumo) + dados["tarifa_fixa_mensal"]
    assert agua == pytest.approx(esperado, abs=0.01)


def test_industrial_acima_de_mil_m3_segue_a_tabela_ix():
    """Acima de 1.000 m³ o excedente é cobrado pelos preços da Tabela IX, sem expoente."""
    faixas = get_city_tariffs_by_category("RS", "Alegrete", "industrial")["faixas"]
    mil = custo_volumetrico(faixas, 1000)
    assert custo_volumetrico(faixas, 1500) - mil == pytest.approx(500 * 9.87)
    assert custo_volumetrico(faixas, 3000) - mil == pytest.approx(1000 * 9.87 + 1000 * 8.60)


def test_sem_tabela_ix_a_industrial_nao_e_oferecida():
    for cidade in ("Canoas", "Erechim", "Santa Cruz do Sul"):
        assert "industrial" not in categorias_coletadas(get_city_data("RS", cidade))
        assert get_city_tariffs_by_category("RS", cidade, "industrial") is None


def test_a_social_da_corsan_fica_de_fora():
    """O PB da Social troca no excedente, e a estrutura de quádruplas não representa isso."""
    assert get_city_tariffs_by_category("RS", "Alegrete", "social") is None


def test_esgoto_por_m3_consumido_da_categoria():
    dados = get_city_tariffs_by_category("RS", "Alegrete", "comercial")
    assert dados["esgoto_r_m3"] == 7.28
    assert dados["fonte_documento"].startswith("ANEXO-5")
    conta = calculate_water_bill(20000.0, dados["faixas"], sewage_rate=dados["esgoto_r_m3"],
                                 sewage_mode=dados["esgoto_modo"])
    assert conta == pytest.approx(285.61 + 20 * 7.28, abs=0.01)
