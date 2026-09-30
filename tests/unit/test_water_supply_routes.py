"""Verificação do catálogo de rotas de produção de água.

A emissão evitada por metro cúbico era um número só, tratado como se fosse
propriedade do sistema pluvial. É propriedade da **água substituída**: o mesmo
reservatório muda de mérito por uma ordem de grandeza conforme desloque água de
manancial tratada por gravidade ou água engarrafada.

Estes testes protegem duas coisas: que toda rota diga de onde veio, e que as
rotas dominadas por eletricidade sejam recalculadas com a matriz escolhida em
vez de carregarem o impacto da matriz de outro país.
"""

from __future__ import annotations

import pytest

from netuno.core import water_supply_routes as rotas
from netuno.core.environmental import EnvironmentalConfig, calculate_lca, PipeInput, PumpInput


def test_rota_padrao_existe():
    assert rotas.ROTA_PADRAO in rotas.chaves_das_rotas()


def test_toda_rota_declara_fonte():
    """Uma rota sem fonte é um número solto com nome bonito."""
    for chave, registro in rotas.rotas_disponiveis().items():
        assert registro.get("fonte"), f"rota {chave} sem fonte"
        assert registro.get("nome_pt") and registro.get("nome_en"), f"rota {chave} sem nome bilíngue"
        assert registro.get("tipo") in {"total_publicado", "energia_mais_outros"}, chave


def test_toda_rota_devolve_valor_positivo_e_plausivel():
    for chave in rotas.chaves_das_rotas():
        valor = rotas.co2_evitado_por_m3(chave)
        assert 0.0 < valor < 200.0, f"{chave}: {valor}"


def test_rota_desconhecida_falha_alto():
    with pytest.raises(KeyError):
        rotas.co2_evitado_por_m3("rota_que_nao_existe")


def test_rotas_dominadas_por_energia_seguem_a_matriz():
    """A dessalinização tem de mudar quando a matriz muda — é o ponto do tipo.

    Uma planta de osmose reversa consome a mesma energia no Brasil e na
    Alemanha, e emite coisas muito diferentes. Uma rota que devolvesse o mesmo
    número nos dois casos estaria escondendo exatamente o que interessa.
    """
    limpa = rotas.co2_evitado_por_m3("dessalinizacao_osmose_reversa", fator_da_rede_kg_kwh=0.085)
    suja = rotas.co2_evitado_por_m3("dessalinizacao_osmose_reversa", fator_da_rede_kg_kwh=0.400)
    assert suja > limpa * 3, "a dessalinização deve responder fortemente à matriz"


def test_rotas_de_total_publicado_nao_mudam_com_a_matriz():
    """O que não se sabe decompor não se rescala."""
    a = rotas.co2_evitado_por_m3("agua_mineral_pet", fator_da_rede_kg_kwh=0.085)
    b = rotas.co2_evitado_por_m3("agua_mineral_pet", fator_da_rede_kg_kwh=0.400)
    assert a == b


def test_ordem_de_grandeza_entre_rotas():
    """Água engarrafada tem de estar duas ordens de grandeza acima da rede."""
    rede = rotas.co2_evitado_por_m3("convencional_br")
    pet = rotas.co2_evitado_por_m3("agua_mineral_pet")
    assert pet > 100 * rede


def test_agua_engarrafada_em_pet_supera_a_de_vidro_no_clima():
    """Resultado contraintuitivo da fonte, e que por isso convém fixar.

    Garfí et al. registram que o vidro tem impacto maior em quase todos os
    indicadores, **exceto** aquecimento global e oxidação fotoquímica, por causa
    das emissões da produção do PET.
    """
    assert rotas.co2_evitado_por_m3("agua_mineral_pet") > rotas.co2_evitado_por_m3("agua_mineral_vidro")


def test_comparacao_vem_ordenada():
    linhas = rotas.comparar_rotas()
    valores = [linha["co2_evitado_kg_m3"] for linha in linhas]
    assert valores == sorted(valores)
    assert len(linhas) == len(rotas.chaves_das_rotas())


def test_config_ambiental_parte_da_rota_padrao():
    config = EnvironmentalConfig()
    assert config.water_supply_route == rotas.ROTA_PADRAO
    assert config.potable_water_co2_kg_m3 == rotas.co2_evitado_por_m3(rotas.ROTA_PADRAO)


def test_a_rota_muda_o_resultado_da_acv():
    """É o efeito que justifica a funcionalidade existir."""

    def rodar(rota_escolhida):
        config = EnvironmentalConfig(
            lower_material_key="PEAD",
            upper_tank_used=False,
            pipes=[PipeInput(diameter_mm=100, length_m=20.0)],
            pump=PumpInput(power_cv=0.5),
            system_lifespan_years=20.0,
            water_supply_route=rota_escolhida,
            potable_water_co2_kg_m3=rotas.co2_evitado_por_m3(rota_escolhida),
        )
        return calculate_lca(5000.0, 100.0, config)

    convencional = rodar("convencional_br")
    osmose = rodar("osmose_reversa_na_eta")

    assert osmose.annual_avoided_co2_kg > convencional.annual_avoided_co2_kg
    assert osmose.environmental_payback_years < convencional.environmental_payback_years


def test_nao_existe_rota_definida_so_por_energia():
    """Representar a agua da rede so pela eletricidade e contabilidade parcial.

    Uma rota assim ignora produtos quimicos, infraestrutura, perdas e lodo, e
    devolveria cerca de um oitavo do valor completo. Como opcao selecionavel,
    convidaria o usuario a destruir a propria analise sem perceber. A
    intensidade energetica continua util para comparar com o SINISA, mas isso e
    outra pergunta, e nao pertence a esta lista.
    """
    assert "abastecimento_publico_energia" not in rotas.chaves_das_rotas()
    for chave in rotas.chaves_das_rotas():
        assert rotas.co2_evitado_por_m3(chave) > 0.1, (
            f"rota {chave} devolve valor baixo demais para representar agua tratada"
        )


def test_procedencia_traz_doi_quando_ha_fonte_publicada():
    com_doi = [c for c in rotas.chaves_das_rotas() if "doi_da_fonte" in rotas.procedencia_da_rota(c)]
    assert len(com_doi) >= 5, "a maioria das rotas deve apontar para um artigo recuperável"
