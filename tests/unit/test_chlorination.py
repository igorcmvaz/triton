"""Verificação da cadeia única de cloração.

Havia três convenções incompatíveis no mesmo programa, e nenhuma podia concordar
com as outras porque as bases eram diferentes:

| Módulo | Dose | Base do fator | Resultado |
| :--- | :--- | :--- | ---: |
| Ambiental | 2,0 mg/L | por kg de Cl₂ puro, fator 25,0 | 0,0500 kg CO₂e/m³ |
| Qualidade | 1,5 mg/L | por kg de pastilha a 65%, fator 1,85 | 0,0043 kg CO₂e/m³ |
| Econômico | 2,0 mg/L | cobrava o preço sobre cloro ativo | custo 35% baixo |

Estes testes protegem a unificação e, sobretudo, impedem o retorno do fator de
25,0 — que não tinha fonte, é implausível por uma ordem de grandeza para cloro
de rota cloro-álcali, e era **idêntico** ao preço de 25,00 R$/kg no
`costs_database.json`.
"""

from __future__ import annotations

import os
import re

import pytest

from netuno.core.chlorination import (
    DOSE_PADRAO_MG_POR_LITRO,
    FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
    PUREZA_PADRAO,
    Cloracao,
    cloracao_padrao,
)


def test_a_pureza_converte_cloro_ativo_em_produto():
    """É a conversão que faltava, e metade da divergência de 11,7 vezes."""
    c = Cloracao(dose_mg_por_litro=1.5, pureza=0.65)
    assert c.cloro_ativo_kg_por_m3 == pytest.approx(0.0015)
    assert c.produto_kg_por_m3 == pytest.approx(0.0015 / 0.65)
    assert c.produto_kg_por_m3 > c.cloro_ativo_kg_por_m3


def test_emissao_e_massa_de_produto_vezes_fator():
    c = cloracao_padrao()
    assert c.co2e_kg_por_m3 == pytest.approx(
        c.produto_kg_por_m3 * FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    )


def test_valores_anuais_escalam_com_o_volume():
    c = cloracao_padrao()
    assert c.co2e_anual_kg(100.0) == pytest.approx(100.0 * c.co2e_kg_por_m3)
    assert c.massa_anual_de_produto_kg(100.0) == pytest.approx(100.0 * c.produto_kg_por_m3)
    assert c.co2e_anual_kg(-5.0) == 0.0, "volume negativo não pode gerar emissão negativa"


def test_pureza_fora_da_faixa_falha_com_mensagem_util():
    """O engano provável é escrever 65 em vez de 0,65."""
    with pytest.raises(ValueError, match="0,65"):
        Cloracao(pureza=65.0)
    with pytest.raises(ValueError):
        Cloracao(pureza=0.0)


def test_dose_negativa_falha():
    with pytest.raises(ValueError):
        Cloracao(dose_mg_por_litro=-1.0)


def test_dose_padrao_dentro_da_faixa_normativa():
    """A NBR 15527:2019, item 4.6.5, trabalha entre 0,5 e 2,0 mg/L."""
    assert 0.5 <= DOSE_PADRAO_MG_POR_LITRO <= 2.0


def test_fator_plausivel_para_hipoclorito():
    """Cloro de rota cloro-álcali fica entre 1 e 2 kg CO₂e/kg."""
    assert 0.5 < FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO < 5.0


def test_o_fator_do_cloro_nunca_volta_a_ser_o_preco():
    """Guarda estrutural contra o retorno do 25,0.

    O valor circulava por seis arquivos — motor, interface, CLI, parser — e em
    todos era o preço em reais ocupando um campo de emissão. Basta que reapareça
    num deles para o resultado ambiental voltar a ser dez vezes maior do que
    deveria.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pacote = os.path.join(raiz, "netuno")

    padrao = re.compile(r"chlorine_co2\w*\s*[=:]\s*2[45]\.?\d*")
    ofensores = []
    for pasta, _, arquivos in os.walk(pacote):
        for nome in arquivos:
            if not nome.endswith(".py"):
                continue
            caminho = os.path.join(pasta, nome)
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for numero, linha in enumerate(arquivo, start=1):
                    if padrao.search(linha):
                        ofensores.append(f"{os.path.relpath(caminho, raiz)}:{numero}")

    assert not ofensores, (
        "Fator de emissão do cloro com valor de custo (25 R$/kg): " f"{ofensores}"
    )


def test_os_tres_modulos_partem_da_mesma_cadeia():
    from netuno.core.environmental import EnvironmentalConfig
    from netuno.core.parser import NetunoConfig

    ambiental = EnvironmentalConfig()
    projeto = NetunoConfig()

    assert ambiental.chlorine_dose_mg_l == DOSE_PADRAO_MG_POR_LITRO
    assert ambiental.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    assert ambiental.chlorine_product_purity == PUREZA_PADRAO

    assert projeto.chlorine_dose_mg_l == DOSE_PADRAO_MG_POR_LITRO
    assert projeto.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO


def test_cloracao_e_sempre_aplicada_na_linha_de_tratamento():
    """É a única barreira que deixa residual livre.

    O programa tratava cloro, ultravioleta e ozônio como escolhas exclusivas, e
    admitia «sem desinfecção». Ultravioleta e ozônio desinfetam na passagem e não
    deixam residual, de modo que somam-se à cloração em vez de substituí-la.
    """
    from netuno.core.water_quality import size_etap

    for escolha in ("cloro", "uv", "ozonio", "nenhum"):
        resultado = size_etap(disinfection_choice=escolha, annual_pluvial_consumed_m3=120.0)
        assert resultado.annual_chlorine_kg > 0, f"sem cloro em {escolha!r}"
        assert any("lora" in etapa for etapa in resultado.disinfection_stages)


def test_barreiras_adicionais_somam_custo_e_emissao():
    from netuno.core.water_quality import size_etap

    so_cloro = size_etap(disinfection_choice="cloro", annual_pluvial_consumed_m3=120.0)
    com_uv = size_etap(disinfection_choice="uv", annual_pluvial_consumed_m3=120.0)

    assert com_uv.total_etap_capex > so_cloro.total_etap_capex
    assert com_uv.total_etap_annual_opex > so_cloro.total_etap_annual_opex
    # A energia do reator entrava em lugar nenhum: nem no custo, nem na emissão.
    assert com_uv.total_etap_co2e_kg_yr > so_cloro.total_etap_co2e_kg_yr
    assert com_uv.uv_annual_kwh > 0
