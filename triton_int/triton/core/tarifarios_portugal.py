# -*- coding: utf-8 -*-
"""Tarifários transcritos da Edição Portugal (``triton/data/portugal_tarifarios.json``).

Cada concelho traz a água (tarifa fixa e escalões), o saneamento (por escalões sobre o volume
recolhido, ou como parcela por m³), as demais parcelas da fatura e o IVA de cada uma, com as
fontes e as contas de conferência. ``fatura`` devolve a ``FaturaPortuguesa`` pronta para
``fatura_portuguesa.aplicar_ao_projeto``.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Dict, List, Optional

from triton.core.fatura_portuguesa import Escalao, FaturaPortuguesa, Parcela

_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "data", "portugal_tarifarios.json")


@lru_cache(maxsize=1)
def carregar() -> Dict[str, dict]:
    with open(_ARQUIVO, encoding="utf-8") as f:
        dados = json.load(f)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def concelhos() -> List[str]:
    """Concelhos com tarifário transcrito."""
    return sorted(carregar())


def _escaloes(lista) -> List[Escalao]:
    return [Escalao(float(a), None if b is None else float(b), float(p)) for a, b, p in lista]


def fatura(concelho: str) -> Optional[FaturaPortuguesa]:
    """A fatura doméstica do concelho, ou None se ele ainda não foi transcrito."""
    d = carregar().get(concelho)
    if d is None:
        return None
    agua, san = d["agua"], d.get("saneamento") or {}
    f = FaturaPortuguesa(
        entidade=d["entidades"], concelho=concelho,
        fixa_agua=float(agua["fixa_mes"]), escaloes=_escaloes(agua["escaloes"]),
        iva_agua_pct=float(agua["iva_pct"]),
        parcelas=[Parcela(p["nome"], float(p.get("fixa", 0.0)), float(p.get("por_m3", 0.0)),
                          float(p.get("iva_pct", 0.0))) for p in d.get("parcelas", [])],
        fonte="; ".join(d.get("fontes", [])), vigencia=d.get("vigencia", ""))
    if san.get("escaloes"):
        f.saneamento_escaloes = _escaloes(san["escaloes"])
        f.saneamento_fixa = float(san.get("fixa_mes", 0.0))
        f.saneamento_trh_m3 = float(san.get("trh_m3", 0.0))
        f.coef_recolha = float(san.get("coef_recolha", 1.0))
        f.iva_saneamento_pct = float(san.get("iva_pct", 0.0))
    f.validar()
    return f


def aplicar(concelho: str, cfg) -> bool:
    """Grava no projeto o tarifário do concelho e a vigência; False se não houver."""
    from triton.core.fatura_portuguesa import aplicar_ao_projeto
    f = fatura(concelho)
    if f is None:
        return False
    aplicar_ao_projeto(f, cfg)
    cfg.tariff_city_name = concelho
    cfg.tariff_city_uf = carregar()[concelho].get("distrito", "")
    cfg.tariff_vigencia = f.vigencia
    cfg.tariff_category = "residencial"
    return True
