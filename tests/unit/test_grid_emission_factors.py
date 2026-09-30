"""Verificação da série de fatores de emissão da rede elétrica (MCTI/SIRENE).

O que estes testes protegem não é a aritmética — não há aritmética a proteger —,
e sim a **procedência**: que a série continue vindo do arquivo oficial
arquivado, que o ano do fator seja sempre declarado, e que ninguém volte a
enfiar um número solto no código.
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest

from netuno.core import grid_emission_factors as fatores
from netuno.core.environmental import EnvironmentalConfig


def test_serie_cobre_o_periodo_publicado():
    anos = fatores.anos_disponiveis()
    assert anos[0] == 2006
    assert anos == sorted(anos)
    # Sem buracos: a série do MCTI é contínua.
    assert anos == list(range(anos[0], anos[-1] + 1))


def test_ano_padrao_existe_na_serie():
    assert fatores.ANO_PADRAO in fatores.anos_disponiveis()


def test_fatores_em_faixa_fisicamente_plausivel():
    """A matriz brasileira é predominantemente hídrica.

    Um fator acima de 0,5 kg CO₂/kWh indicaria matriz majoritariamente térmica
    — não é o caso do SIN em ano nenhum da série, e um valor assim denunciaria
    erro de unidade (g em vez de kg, ou MWh em vez de kWh).
    """
    for ano in fatores.anos_disponiveis():
        valor = fatores.fator_anual(ano)
        assert 0.0 < valor < 0.5, f"{ano}: {valor}"


def test_ano_fora_da_serie_falha_alto():
    """Pedir um ano sem publicação deve falhar, nunca devolver um valor vizinho."""
    with pytest.raises(KeyError):
        fatores.fator_anual(1999)
    with pytest.raises(KeyError):
        fatores.fator_anual(fatores.anos_disponiveis()[-1] + 5)


def test_mes_invalido_falha():
    with pytest.raises(ValueError):
        fatores.fator_mensal(2025, 0)
    with pytest.raises(ValueError):
        fatores.fator_mensal(2025, 13)


def test_config_ambiental_usa_uma_base_declarada_de_co2eq():
    """O padrão da ACV tem de ser CO₂-equivalente, com a base declarada.

    Uma versão intermediária deste módulo fez a ACV ler a série anual do MCTI,
    que é de **CO₂ apenas** e cobre só a geração. Era erro de grandeza, e
    subestimava o bombeamento. O teste fixa a correção.
    """
    config = EnvironmentalConfig()
    assert config.grid_co2_factor_basis in fatores.bases_disponiveis()
    assert config.grid_co2_factor_kg_kwh == fatores.fator_co2eq(config.grid_co2_factor_basis)


def test_o_fator_da_acv_nao_e_o_do_mcti():
    """Guarda contra a reintrodução do erro CO₂ × CO₂e.

    O fator de CO₂e usado pela ACV tem de ser maior que o fator de CO₂ da
    geração: ele cobre mais gases e uma fronteira mais ampla. Se algum dia
    passar a coincidir com a série do MCTI, alguém terá trocado as grandezas.
    """
    config = EnvironmentalConfig()
    co2_apenas = fatores.fator_anual(fatores.ANO_PADRAO)
    assert config.grid_co2_factor_kg_kwh > co2_apenas, (
        "o fator de CO₂e da ACV não pode ser menor ou igual ao de CO₂ da geração"
    )


def test_toda_base_declara_gas_fronteira_e_fonte():
    for nome, base in fatores.bases_disponiveis().items():
        for campo in ("valor", "gas", "fronteira", "fonte"):
            assert base.get(campo), f"base {nome} sem {campo}"
        assert 0.0 < float(base["valor"]) < 1.0, nome


def test_base_desconhecida_falha_alto():
    with pytest.raises(KeyError):
        fatores.fator_co2eq("base_que_nao_existe")


def test_nenhum_fator_de_rede_transcrito_no_codigo():
    """Impede o retorno do 0,085 solto — e de qualquer sucessor dele.

    O valor da rede elétrica reapareceu copiado em oito lugares (CLI, interface,
    gráficos) e num deles ocupava o campo errado, o da energia específica da
    bomba. A cura é estrutural: o número existe num arquivo só, e o código o
    pede à função.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pacote = os.path.join(raiz, "netuno")

    ofensores = []
    for pasta, _, arquivos in os.walk(pacote):
        for nome in arquivos:
            if not nome.endswith(".py"):
                continue
            caminho = os.path.join(pasta, nome)
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for numero, linha in enumerate(arquivo, start=1):
                    if "0.085" in linha and not linha.lstrip().startswith("#"):
                        ofensores.append(f"{os.path.relpath(caminho, raiz)}:{numero}")

    assert not ofensores, (
        "Fator da rede elétrica transcrito no código em vez de lido da série "
        f"oficial: {ofensores}"
    )


def test_procedencia_declara_o_essencial():
    """Sem estes campos o número não é rastreável, e é isso que se está comprando."""
    fonte = fatores.procedencia()
    for campo in ("orgao", "serie", "arquivo_arquivado", "sha256", "url", "unidade", "gas", "fronteira"):
        assert fonte.get(campo), f"campo de procedência ausente ou vazio: {campo}"
    # A distinção CO2 × CO2e é o engano mais provável de quem reutilizar isto.
    assert "CO2e" in fonte["gas"] or "equivalente" in fonte["gas"].lower()


def test_arquivo_fonte_arquivado_confere_com_o_hash_registrado():
    """A série tem de continuar sendo a que se leu da planilha oficial.

    Se alguém reeditar o JSON à mão, o hash do XLSX ainda bate — por isso o
    teste também reconfere um valor contra a planilha.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fonte = fatores.procedencia()
    caminho = os.path.join(raiz, fonte["arquivo_arquivado"])

    if not os.path.isfile(caminho):
        pytest.skip("planilha original do MCTI não distribuída nesta cópia")

    with open(caminho, "rb") as arquivo:
        digest = hashlib.sha256(arquivo.read()).hexdigest()
    assert digest == fonte["sha256"], (
        "A planilha arquivada do MCTI mudou. Se a atualização é intencional, "
        "regenere netuno/data/fatores_emissao_rede_mcti.json a partir dela."
    )
