"""A tabela de faixas do apêndice D cobre os 652 municípios nas cinco categorias.

Cada combinação de município e categoria tem de aparecer em algum lugar: numa linha
com preço (auditada, a confirmar ou incompleta) ou na lista das não coletadas.
"""

from __future__ import annotations

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "manual"))

import tabela_de_faixas as t  # noqa: E402


def test_cada_categoria_soma_todos_os_municipios():
    cidades = t.carregar()
    for cat, n in t.cobertura(cidades).items():
        assert sum(n.values()) == len(cidades), cat


def test_toda_combinacao_aparece_uma_vez():
    cidades = t.carregar()
    vistas = {}
    for _p, cat, municipios, _d in t.linhas(cidades):
        for m in municipios:
            vistas[(m, cat)] = vistas.get((m, cat), 0) + 1
    for _p, cat, municipios in t.nao_coletadas(cidades):
        for m in municipios:
            vistas[(m, cat)] = vistas.get((m, cat), 0) + 1
    # a CORSAN não entra em linhas(): a fórmula exponencial tem tabela própria
    for d in cidades.values():
        if d.get("regime_tarifario") == "exponencial":
            m = f"{d['municipio']} ({d['uf']})"
            for cat in ["residencial"] + list(d.get("categorias") or {}):
                vistas[(m, cat)] = vistas.get((m, cat), 0) + 1
    # cobrança direta e parcela fixa por faixa também têm tabela própria
    for chave, d, cat in t._estruturas(cidades):
        if t._convertida(d) and d.get("regime_tarifario") != "exponencial":
            m = f"{d['municipio']} ({d['uf']})"
            vistas[(m, cat)] = vistas.get((m, cat), 0) + 1
    assert len(vistas) == len(cidades) * len(t.CATEGORIAS)
    assert set(vistas.values()) == {1}
