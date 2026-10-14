"""A caixa de entrada reconhece o prestador mesmo quando o arquivo não o nomeia.

Os casos são arquivos reais recebidos em 04/10/2026: resoluções da ARISB-MG com o
município no nome e uma página salva com o nome genérico «TARIFAS VIGENTES.html».
"""

from __future__ import annotations

import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _p in (os.path.join(RAIZ, "tarifas"), os.path.join(RAIZ, "manual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import processar_entrada as P  # noqa: E402


@pytest.mark.parametrize("arquivo,prestador", [
    ("RES_367_2025_ARISB_MG_Revisao_Pirapora_corrigida.pdf", "SAAE Pirapora"),
    ("RES_373_2025_ARISB_MG_Revisão_Lagoa da Prata - assinada.pdf", "SAAE Lagoa da Prata"),
    ("RESOLUÇÃO DE FISCALIZAÇÃO E REGULAÇÃO 361 FORMIGA.pdf", "SAAE Formiga"),
    ("Tarifas_2026-Parcela1_Tarifas.pdf", "COMUSA Novo Hamburgo"),
])
def test_reconhece_pelo_nome_do_arquivo(arquivo, prestador):
    assert P._identificar_prestador(arquivo)[0] == prestador


def test_nome_generico_nao_identifica_pelo_nome():
    assert P._identificar_prestador("TARIFAS VIGENTES.html")[0] == ""


def test_reconhece_pelo_conteudo_e_avisa():
    caminho = os.path.join(RAIZ, "tarifas", "fontes", "saae_nova_mutum", "TARIFAS VIGENTES.html")
    if not os.path.exists(caminho):
        pytest.skip("página de Nova Mutum não guardada nesta cópia")
    prestador, conteudo, _ = P._identificar_pelo_conteudo(caminho)
    assert prestador == "SAAE Nova Mutum"
    assert "conferir" in conteudo


def _pelo_texto(tmp_path, monkeypatch, texto):
    arq = tmp_path / "doc.pdf"
    arq.write_bytes(b"%PDF")
    monkeypatch.setattr(P, "_texto", lambda caminho: texto)
    return P._identificar_pelo_conteudo(str(arq))[0]


def test_conteudo_reconhece_municipio_de_prestador_estadual(tmp_path, monkeypatch):
    """Resolução da agência de Natal: Natal é da CAERN, que atende muitos municípios."""
    texto = "AGÊNCIA REGULADORA DO MUNICÍPIO DE NATAL ... no âmbito do Município do Natal ... Natal"
    assert _pelo_texto(tmp_path, monkeypatch, texto) == "CAERN"


def test_palavra_comum_nao_e_municipio(tmp_path, monkeypatch):
    """«registro do cavalete» não é Registro/SP (caso real: tarifas de Castilho/SP)."""
    texto = "Substituição registro de cavalete; Reparo registro do ramal; Instalação de registro"
    assert _pelo_texto(tmp_path, monkeypatch, texto) == ""


def test_nome_mais_longo_vence(tmp_path, monkeypatch):
    """«Barra do Garças» não conta como Barra/BA."""
    texto = "Águas de Barra do Garças, concessionária em Barra do Garças, Mato Grosso"
    assert _pelo_texto(tmp_path, monkeypatch, texto) == "Águas de Barra do Garças (Aegea)"


def test_avisa_municipio_fora_da_base():
    texto = "Avenida Presidente Getúlio Vargas, 20, CEP: 16920-000, Castilho/SP"
    assert P.municipios_fora_da_base(texto, P.T.carregar()) == ["Castilho/SP"]


@pytest.mark.parametrize("arquivo", ["aguas_de_sorriso_legislacao_e_tarifas.html",
                                     "aguas_de_teresina_legislacao_e_tarifas.html"])
def test_nome_de_pagina_generico_nao_vira_aguas_do_rio(arquivo):
    """«legislacao_e_tarifas» é o nome da página de todas as concessionárias da Aegea."""
    assert P._identificar_prestador(arquivo)[0] != "Águas do Rio"


@pytest.mark.parametrize("arquivo,prestador", [
    ("Tabela Tarifária - 2025_2026 - SAMAE SBS.html", "SAMAE São Bento do Sul"),
    ("9. Estrutura Tarifaria Bloco C - Ano 04 2025-2026 Rampa - Vigente a partir de 08.03.2026.pdf", "Verde Alagoas"),
])
def test_siglas_e_blocos_recebidos_em_05_10(arquivo, prestador):
    assert P._identificar_prestador(arquivo)[0] == prestador
