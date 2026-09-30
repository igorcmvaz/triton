"""A emissão evitada por m³ é escolhida pela tecnologia de tratamento do local.

Decisão do professor: o valor deve ser modificável conforme a tecnologia, com
0,35 kg CO₂e/m³ como base do programa, e a rota do SNIS não serve como padrão
porque parte de um indicador de energia, e uma ACV é mais do que energia.

Dois conceitos que estes testes protegem, porque errá-los produz números que
parecem certos:

**Fronteira.** O sistema pluvial substitui água ENTREGUE na edificação, não água
produzida na estação. Entre uma e outra estão as perdas de distribuição: no
Brasil, de 33,9% no sudeste a 46,9% no norte. Um valor de porta de estação
subestima o benefício em 50 a 88%.

**Matriz elétrica.** Rotas dominadas por eletricidade — a dessalinização por
osmose reversa à frente — têm de ser recalculadas com o fator da rede local. Um
número fixo esconderia que a mesma planta emite muito mais numa matriz carvoeira.
"""

from __future__ import annotations

import pytest

from netuno.core import water_supply_routes as rotas


# ─────────────────────────── a base é 0,35 e é declarada ───────────────────────

def test_a_base_do_programa_e_035_e_e_a_rota_padrao():
    assert rotas.BASE_DO_PROGRAMA_KG_M3 == pytest.approx(0.35)
    assert rotas.ROTA_PADRAO == "convencional_br"
    assert rotas.co2_evitado_por_m3(rotas.ROTA_PADRAO) == pytest.approx(0.35)


def test_a_base_e_conservadora_perante_as_duas_faixas_publicadas():
    """Fica logo abaixo da faixa europeia e da brasileira.

    Subestimar o benefício do sistema pluvial é o erro conservador: uma
    conclusão de viabilidade obtida com este valor continua valendo se o número
    verdadeiro for maior.
    """
    base = rotas.BASE_DO_PROGRAMA_KG_M3
    europeia = rotas.co2_evitado_por_m3("convencional_garfi")          # 0,44
    brasileira = rotas.co2_evitado_por_m3("vaz_2025_brasil")           # 0,394
    assert base < brasileira < europeia


def test_o_padrao_declara_as_duas_corroboracoes():
    fonte = rotas.procedencia_da_rota(rotas.ROTA_PADRAO)["fonte"]
    assert "Garfi" in fonte
    assert "Vaz" in fonte


# ─────────────────────── toda rota declara o que a torna usável ────────────────

def test_toda_rota_declara_fonte_tecnologia_matriz_e_fronteira():
    """Sem tecnologia e fronteira a escolha não é informada.

    Dois valores muito diferentes podem descrever a mesma coisa medida de dois
    jeitos, e sem os dois campos o usuário não tem como perceber.
    """
    for chave in rotas.chaves_das_rotas():
        proc = rotas.procedencia_da_rota(chave)
        assert proc.get("fonte"), chave
        assert proc.get("tecnologia"), chave
        assert proc.get("fronteira"), chave

        # A matriz assumida só faz sentido para quem publica um total: as rotas
        # recalculadas usam a matriz do usuário, e declarar uma seria falso.
        # Em troca, elas têm de declarar a intensidade energética.
        registro = rotas.rota(chave)
        if registro.get("tipo") == "total_publicado":
            assert proc.get("matriz_da_fonte"), chave
        else:
            assert registro.get("kwh_por_m3", 0) > 0, chave
            assert "matriz_da_fonte" not in proc, chave


def test_todo_doi_citado_tem_forma_de_doi():
    for chave in rotas.chaves_das_rotas():
        doi = rotas.procedencia_da_rota(chave).get("doi_da_fonte")
        if doi:
            assert doi.startswith("10."), (chave, doi)
            assert "/" in doi, (chave, doi)


def test_o_catalogo_cobre_tecnologias_distintas():
    tecnologias = {
        rotas.procedencia_da_rota(c).get("tecnologia", "").lower()
        for c in rotas.chaves_das_rotas()
    }
    assert len(tecnologias) >= 5
    junto = " ".join(tecnologias)
    for termo in ("convencional", "osmose", "termica"):
        assert termo in junto, termo


# ─────────────────────────────── fronteira do sistema ──────────────────────────

def test_as_rotas_de_fronteira_parcial_sao_marcadas():
    """São limite inferior, não estimativa central, e o programa tem de dizê-lo."""
    incompletas = [c for c in rotas.chaves_das_rotas() if rotas.fronteira_e_incompleta(c)]
    assert "rede_publica_brasil_snis" in incompletas
    assert "vaz_2025_porta_da_eta" in incompletas
    assert rotas.ROTA_PADRAO not in incompletas


def test_a_rota_padrao_esta_entre_as_de_fronteira_completa():
    completas = rotas.chaves_com_fronteira_completa()
    assert rotas.ROTA_PADRAO in completas
    assert len(completas) < len(rotas.chaves_das_rotas())
    assert all(not rotas.fronteira_e_incompleta(c) for c in completas)


def test_a_rota_do_snis_nao_pode_voltar_a_ser_padrao():
    """Parte de um indicador de ENERGIA, e uma ACV é mais do que energia.

    Adotá-la como padrão inverteria conclusões de estudos publicados, e o faria
    com um valor que omite produtos químicos, infraestrutura e lodo.
    """
    assert rotas.ROTA_PADRAO != "rede_publica_brasil_snis"
    assert rotas.fronteira_e_incompleta("rede_publica_brasil_snis")
    proc = rotas.procedencia_da_rota("rede_publica_brasil_snis")
    assert "LIMITE INFERIOR" in proc["observacao"]


def test_a_porta_da_eta_e_menor_que_o_valor_entregue():
    """As perdas de distribuição separam os dois, e são grandes no Brasil.

    Produzir 1 m³ não é entregar 1 m³: para entregar um, produz-se de 1,51 a
    1,88, conforme a macrorregião.
    """
    porta = rotas.co2_evitado_por_m3("vaz_2025_porta_da_eta")
    for regiao in ("norte", "nordeste", "centro_oeste", "sudeste", "sul"):
        entregue = rotas.co2_evitado_por_m3(f"vaz_2025_{regiao}")
        assert entregue > porta, regiao
        # O quociente é 1/(1-perda), e as perdas brasileiras vão de 33,9 a 46,9%.
        assert 1.4 < entregue / porta < 2.0, regiao


# ──────────────────────── as rotas do artigo do professor ──────────────────────

def test_as_cinco_macrorregioes_estao_no_catalogo():
    for regiao in ("norte", "nordeste", "centro_oeste", "sudeste", "sul"):
        chave = f"vaz_2025_{regiao}"
        assert chave in rotas.chaves_das_rotas()
        assert rotas.procedencia_da_rota(chave)["doi_da_fonte"] == "10.1016/j.buildenv.2025.113085"


def test_o_nordeste_emite_mais_por_m3_apesar_de_consumir_menos():
    """É o resultado contraintuitivo do artigo, e vem das perdas.

    O nordeste tem o menor consumo por domicílio e as maiores perdas de
    distribuição, 46,7%, e por isso a maior emissão por metro cúbico entregue.
    """
    por_regiao = {
        r: rotas.co2_evitado_por_m3(f"vaz_2025_{r}")
        for r in ("norte", "nordeste", "centro_oeste", "sudeste", "sul")
    }
    assert max(por_regiao, key=por_regiao.get) == "nordeste"
    assert min(por_regiao, key=por_regiao.get) == "sudeste"


def test_a_media_brasileira_fica_dentro_da_faixa_das_regioes():
    valores = [rotas.co2_evitado_por_m3(f"vaz_2025_{r}")
               for r in ("norte", "nordeste", "centro_oeste", "sudeste", "sul")]
    media = rotas.co2_evitado_por_m3("vaz_2025_brasil")
    assert min(valores) < media < max(valores)
    assert media == pytest.approx(sum(valores) / len(valores), abs=0.01)


# ────────────────────── a matriz elétrica move o que deve mover ────────────────

def test_a_dessalinizacao_por_osmose_acompanha_a_matriz():
    """É dominada por eletricidade: fixar o número esconderia isso."""
    limpa = rotas.co2_evitado_por_m3("dessalinizacao_osmose_reversa", 0.085)
    suja = rotas.co2_evitado_por_m3("dessalinizacao_osmose_reversa", 0.700)
    assert suja > 5 * limpa


def test_as_rotas_de_total_publicado_nao_se_movem_com_a_matriz():
    """O total já embute a matriz que a fonte assumiu; recalcular seria contar duas vezes."""
    for chave in ("convencional_br", "vaz_2025_sul", "dessalinizacao_termica"):
        assert rotas.co2_evitado_por_m3(chave, 0.085) == pytest.approx(
            rotas.co2_evitado_por_m3(chave, 0.700)
        ), chave


def test_a_dessalinizacao_termica_e_ordens_de_grandeza_acima_do_convencional():
    """Onde há dessalinização térmica, o sistema pluvial se paga muito rápido."""
    termica = rotas.co2_evitado_por_m3("dessalinizacao_termica")
    assert termica > 20 * rotas.BASE_DO_PROGRAMA_KG_M3
    proc = rotas.procedencia_da_rota("dessalinizacao_termica")
    # Energia térmica, não elétrica: por isso não se recalcula com o fator da rede.
    assert "TERMICA" in proc["observacao"] or "térmica" in proc["observacao"].lower()


def test_a_comparacao_ordena_da_menor_para_a_maior():
    linhas = rotas.comparar_rotas(0.085)
    valores = [linha["co2_evitado_kg_m3"] for linha in linhas]
    assert valores == sorted(valores)
    assert linhas[-1]["co2_evitado_kg_m3"] > 50   # água mineral engarrafada
