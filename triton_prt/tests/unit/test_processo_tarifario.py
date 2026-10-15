# -*- coding: utf-8 -*-
"""Os elos do processo tarifário: registro, arquivos, transcrições, banco e histórico.

Cada documento recebido passa por `processar_entrada.py` (registro e arquivo em
`tarifas/fontes/`), vira transcrição (`tarifas/transcricoes/*.json`) e entra no banco
por `aplicar_transcricoes.py --aplicar`, que grava o histórico. Um elo quebrado faz o
autor buscar de novo o que já mandou, ou deixa no banco um número sem documento.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = json.load(open(os.path.join(RAIZ, "tarifas", "fontes", "registro.json"), encoding="utf-8"))["itens"]
REGID = {i["id"]: i for i in REG}
BASE = json.load(open(os.path.join(RAIZ, "triton", "data", "brazil_cities_tariffs.json"), encoding="utf-8"))["cities"]
TRANS = {}
for _c in glob.glob(os.path.join(RAIZ, "tarifas", "transcricoes", "*.json")):
    if os.path.basename(_c) not in ("historico.json", "cobertura.json", "imagens_conferidas.json"):
        TRANS["tarifas/transcricoes/" + os.path.basename(_c)] = json.load(open(_c, encoding="utf-8"))


def _municipios(t):
    return {f"{tab['uf']} - {m}" for tab in t["tabelas"] for m in tab["municipios"]}


def _tem_documentos():
    """Os PDFs e páginas dos prestadores são de terceiros e não vão ao Git: só o registro vai."""
    return any(os.path.isfile(os.path.join(RAIZ, i["guardado_em"])) for i in REG if i.get("guardado_em"))


SEM_DOCUMENTOS = not _tem_documentos()
PULAR = pytest.mark.skipif(SEM_DOCUMENTOS, reason="documentos de terceiros ausentes neste clone (tarifas/fontes/procedencia.tsv traz hash e URL; o banco tarifas/tarifas_fontes.db os reúne)")


@PULAR
def test_todo_item_registrado_tem_o_arquivo_com_a_mesma_impressao_digital():
    ruins = []
    for i in REG:
        g = i.get("guardado_em")
        if not g:
            continue
        caminho = os.path.join(RAIZ, g)
        if not os.path.isfile(caminho):
            ruins.append((i["id"], g, "falta"))
        elif hashlib.sha256(open(caminho, "rb").read()).hexdigest() != i["sha256"]:
            ruins.append((i["id"], g, "mudou"))
    assert not ruins


def test_nada_fica_recebido_sem_destino():
    """Todo documento recebido é transcrito, consultado (com o motivo) ou descartado."""
    assert not [(i["id"], i["arquivo"]) for i in REG if i["situacao"] == "recebido"]
    assert not [(i["id"], i.get("uso")) for i in REG
                if i["situacao"] in ("consultado", "descartado")
                and not str(i.get("uso", "")).startswith(("consultado:", "descartado:"))]


def test_transcricao_e_registro_concordam():
    usados = set()
    for nome, t in TRANS.items():
        for r in t["registro"]:
            assert r in REGID, f"{nome} cita o item {r}, que não existe"
            usados.add(r)
        assert t["registro"][0] in REGID and REGID[t["registro"][0]]["situacao"] == "transcrito", (
            f"{nome}: o documento principal (item {t['registro'][0]}) não está marcado como transcrito")
        for m in _municipios(t):
            assert m in BASE, f"{nome}: «{m}» não está na base"
    soltos = [i["id"] for i in REG if i["situacao"] == "transcrito" and i["id"] not in usados]
    assert not soltos, f"itens marcados transcrito sem transcrição: {soltos}"


def test_banco_aponta_para_transcricao_que_cobre_o_municipio():
    for chave, d in BASE.items():
        ft = d.get("fonte_transcricao")
        if not ft:
            continue
        assert ft in TRANS, f"{chave}: aponta {ft}, que não existe"
        assert chave in _municipios(TRANS[ft]), f"{chave}: {ft} não cobre o município"
        for r in d.get("fonte_registro") or []:
            assert r in REGID, f"{chave}: item {r} não existe"


def test_historico_so_tem_transcricoes_vigentes():
    hist = json.load(open(os.path.join(RAIZ, "tarifas", "transcricoes", "historico.json"), encoding="utf-8"))
    for h in hist:
        assert h["transcricao"] in TRANS, f"histórico de transcrição removida: {h['transcricao']}"
        assert h["municipio"] in _municipios(TRANS[h["transcricao"]]), (
            f"histórico de {h['municipio']} numa transcrição que já não o cobre ({h['transcricao']})")


@pytest.mark.parametrize("pasta", sorted(p.replace("\\", "/") for p in glob.glob(os.path.join(RAIZ, "tarifas", "fontes", "*", ""))))
def test_toda_pasta_de_fontes_tem_item_registrado(pasta):
    rel = os.path.relpath(pasta.rstrip("/"), RAIZ).replace("\\", "/")
    assert any(os.path.dirname(i.get("guardado_em") or "") == rel for i in REG), f"{rel} sem item no registro"


@PULAR
def test_toda_imagem_de_pagina_foi_lida():
    """Tabela em imagem salva com a página (`*_files/`) não pode passar despercebida.

    A tabela de 2026 do SAMAE Gaspar e a Tabela 1 da DAE Americana (com o esgoto) estavam
    em imagens que nenhuma transcrição citava. Cada imagem grande é citada por uma
    transcrição ou registrada, com o que mostra, em `transcricoes/imagens_conferidas.json`.
    """
    import sys
    sys.path.insert(0, os.path.join(RAIZ, "tarifas"))
    import auditar_cobertura as A
    assert A.imagens_nao_conferidas() == []
