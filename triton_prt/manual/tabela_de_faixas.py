# -*- coding: utf-8 -*-
"""A tabela de escalões por concelho, para o apêndice de regimes tarifários da Edição Portugal.

As colunas são os intervalos de consumo mensal na maior discretização que os tarifários
transcritos pedem: a união dos limites de escalão de todos os concelhos. Se nenhum concelho
separa 0 a 5 m³, a coluna é «0–5»; se algum muda o preço aos 50 m³, nasce a coluna «25–50».
A grelha refaz-se sozinha a cada montagem, de modo que um tarifário novo transcrito em
``triton/data/portugal_tarifarios.json`` entra no apêndice sem que ninguém mexa aqui.

Os valores são os impressos nos documentos das entidades gestoras, antes do IVA: o IVA de cada
parcela vem à parte, na tabela de cada concelho. O saneamento é mostrado por m³ de volume
recolhido (em Lisboa, 90% do volume de água).
"""

from __future__ import annotations

import json
import os
from typing import Callable, Dict, List, Optional, Tuple

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANCO = os.path.join(BASE, "triton", "data", "portugal_tarifarios.json")
NL = chr(10)


def carregar() -> Dict[str, dict]:
    with open(BANCO, encoding="utf-8") as f:
        dados = json.load(f)
    return {k: v for k, v in dados.items() if not k.startswith("_")}


def grelha(tarifarios: Dict[str, dict]) -> List[Tuple[float, Optional[float]]]:
    """Os intervalos de consumo: a união dos limites de todos os escalões."""
    limites = {0.0}
    for d in tarifarios.values():
        for servico in ("agua", "saneamento"):
            for a, b, _p in (d.get(servico) or {}).get("escaloes", []):
                limites.add(float(a))
                if b is not None:
                    limites.add(float(b))
    pontos = sorted(limites)
    return [(a, b) for a, b in zip(pontos, pontos[1:])] + [(pontos[-1], None)]


def _preco(escaloes, a: float, b: Optional[float]) -> Optional[float]:
    meio = a + 0.5 if b is None else (a + b) / 2.0
    for x, y, p in escaloes:
        if float(x) < meio and (y is None or meio <= float(y)):
            return float(p)
    return None


def _rotulo(a: float, b: Optional[float], num: Callable) -> str:
    return f"mais de {num(a)}" if b is None else f"{num(a)}–{num(b)}"


def secao(tarifarios: Dict[str, dict], num: Callable[[float], str], preco: Callable[[float], str]) -> List[str]:
    """As linhas Markdown da tabela de escalões. ``num`` e ``preco`` formatam em português de Portugal."""
    cols = grelha(tarifarios)
    cab = ["Concelho", "Serviço"] + [_rotulo(a, b, num) for a, b in cols]
    L = ["<!-- tabela: Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço -->",
         "| " + " | ".join(cab) + " |",
         "| :--- | :--- " + "| ---: " * len(cols) + "|"]
    for nome in sorted(tarifarios):
        d = tarifarios[nome]
        for rot, chave in (("água", "agua"), ("saneamento", "saneamento")):
            esc = (d.get(chave) or {}).get("escaloes")
            if not esc:
                continue
            celulas = []
            for a, b in cols:
                p = _preco(esc, a, b)
                celulas.append("—" if p is None else preco(p))
            L.append(f"| {nome} | {rot} | " + " | ".join(celulas) + " |")
    return L
