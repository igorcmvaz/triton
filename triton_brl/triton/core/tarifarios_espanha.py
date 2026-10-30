# -*- coding: utf-8 -*-
"""Tarifas de água de Espanha, por camadas de confiança (``triton/data/espanha_tarifarios.json``, só na IBE).

Camada 1: tarifário do município, transcrito de documento oficial arquivado (URL, data de acesso, SHA-256); mesma
estrutura do ``portugal_tarifarios.json``. Camada 2: município sem documento próprio que herda o da sua entidade
(``herda_de``), sempre com aviso. Camada 3: média regional do INE (um preço total por m3, sem parte fixa), só
indicativa. Nenhum valor é inventado: município sem camada 1, 2 ou 3 devolve ``None`` e a interface diz «sem tarifa».
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Dict, Optional

from triton.core.fatura_portuguesa import Escalao, FaturaPortuguesa, Parcela

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "data", "espanha_tarifarios.json")
ROTULO_DA_CAMADA = {1: "tarifa do município (transcrita)", 2: "tarifa de outra entidade ou município (herdada)",
                    3: "média regional do INE (indicativa)"}


@lru_cache(maxsize=1)
def carregar() -> dict:
    if not os.path.isfile(_ARQUIVO):
        return {}
    with open(_ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def _escaloes(lista):
    return [Escalao(float(a), None if b is None else float(b), float(p)) for a, b, p in lista]


def _fatura_do_municipio(d: dict, codigo: str) -> FaturaPortuguesa:
    agua, san = d["agua"], d.get("saneamiento") or {}
    f = FaturaPortuguesa(
        entidade=d.get("entidades", ""), concelho=d.get("nome", codigo), fixa_agua=float(agua["fixa_mes"]),
        escaloes=_escaloes(agua["escaloes"]), iva_agua_pct=float(agua["iva_pct"]),
        parcelas=[Parcela(p["nome"], float(p.get("fixa", 0.0)), float(p.get("por_m3", 0.0)), float(p.get("iva_pct", 0.0)))
                  for p in d.get("parcelas", [])],
        fonte="; ".join(d.get("fontes", [])), vigencia=d.get("vigencia", ""))
    if san.get("escaloes"):
        f.saneamento_escaloes = _escaloes(san["escaloes"])
        f.saneamento_fixa = float(san.get("fixa_mes", 0.0))
        f.coef_recolha = float(san.get("coef_recolha", 1.0))
        f.iva_saneamento_pct = float(san.get("iva_pct", 0.0))
    f.validar()
    return f


def _resolver(codigo: str, profundidade: int = 0) -> Optional[tuple]:
    """(camada, registro) do município: 1 própria, 2 herdada, 3 média da comunidade; None se não houver nada."""
    dados = carregar()
    m = (dados.get("municipios") or {}).get(codigo)
    if m and m.get("camada") == 1 and m.get("agua"):
        return 1, m
    if m and m.get("camada") == 2 and m.get("herda_de") and profundidade < 3:
        base = _resolver(m["herda_de"], profundidade + 1)
        if base and base[0] == 1:
            return 2, {**base[1], "aviso": m.get("aviso") or "tarifa de outro município da mesma entidade gestora; confirme na sua fatura"}
    from triton.core import base_climatica_iberica as _ib
    u = _ib.unidade(codigo) if _ib.disponivel() else None
    c3 = (dados.get("camada3") or {})
    preco = (c3.get("eur_m3_total") or {}).get((u or {}).get("regiao", ""))
    if preco is not None:
        return 3, {"regiao": u["regiao"], "eur_m3_total": float(preco), "ano": c3.get("ano"), "aviso": c3.get("aviso", ""),
                   "fonte": c3.get("fonte", ""), "url": c3.get("url", ""), "sha256_documento": c3.get("sha256_documento", "")}
    return None


def camada(codigo: str) -> Optional[int]:
    r = _resolver(codigo)
    return r[0] if r else None


def fatura(codigo: str) -> Optional[FaturaPortuguesa]:
    r = _resolver(codigo)
    if r is None:
        return None
    cam, reg = r
    if cam in (1, 2):
        return _fatura_do_municipio(reg, codigo)
    f = FaturaPortuguesa(entidade=f"Média regional INE, {reg['regiao']} ({reg['ano']})", concelho=codigo, fixa_agua=0.0,
                         escaloes=[Escalao(0.0, None, reg["eur_m3_total"])], iva_agua_pct=0.0, parcelas=[],
                         fonte=f"{reg['fonte']} — {reg['url']}", vigencia=str(reg["ano"]))
    f.validar()
    return f


def aviso(codigo: str) -> str:
    """O aviso que acompanha a camada 2 e a 3 (vazio na 1 e sem tarifa)."""
    r = _resolver(codigo)
    return (r[1].get("aviso") or "") if r and r[0] in (2, 3) else ""


def procedencia(codigo: str) -> str:
    r = _resolver(codigo)
    if r is None:
        return "sem tarifa: nenhuma fonte verificada para este município"
    cam, reg = r
    txt = f"camada {cam}: {ROTULO_DA_CAMADA[cam]}"
    if cam == 3:
        txt += f"; {reg['eur_m3_total']:.2f}".replace(".", ",") + f" €/m³ total (água e saneamento), {reg['ano']}; {reg['aviso']}"
    elif cam == 2:
        txt += f"; {reg.get('aviso', '')}"
    return txt


def aplicar(codigo: str, cfg) -> bool:
    """Grava no projeto a tarifa do município de Espanha (camada 1, 2 ou 3); False se não houver (a tarifa fica vazia)."""
    from triton.core.fatura_portuguesa import aplicar_ao_projeto
    f = fatura(codigo)
    if f is None:
        return False
    aplicar_ao_projeto(f, cfg)
    cfg.tariff_city_name = codigo
    cfg.tariff_vigencia = f.vigencia
    cfg.tariff_category = "residencial"
    return True


def contagem_por_camada() -> Dict[int, int]:
    """Quantos municípios de Espanha têm cada camada (lida dos dados, nunca digitada)."""
    from triton.core import base_climatica_iberica as _ib
    c = {1: 0, 2: 0, 3: 0, 0: 0}
    for u in _ib.unidades():
        if u["pais"] != "ES":
            continue
        k = camada(u["codigo"])
        c[k or 0] += 1
    return c
