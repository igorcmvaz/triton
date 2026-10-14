# -*- coding: utf-8 -*-
"""Grava as categorias Comercial, Industrial, Pública e Social da CASAN a partir da fonte oficial.

Todas as categorias saem da página oficial da CASAN com vigência a partir de 01/04/2026,
guardada em tarifas/fontes/casan/CASAN - Companhia Catarinense de Águas e Saneamento.html
e transcrita em tarifas/categorias/casan_2026.json.

Uso:
    python scripts/aplicar_categorias_casan.py --conferir
    python scripts/aplicar_categorias_casan.py --aplicar
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "triton" / "data" / "brazil_cities_tariffs.json"
TRANSCRICAO = RAIZ / "tarifas" / "categorias" / "casan_2026.json"

for _p in (RAIZ, RAIZ / "scripts", RAIZ / "tarifas"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from triton.core.tariff_regimes import validar_estrutura  # noqa: E402
import registro_de_fontes as R  # noqa: E402
import gerar_lista_de_coleta  # noqa: E402


def carregar_banco() -> dict:
    with open(BANCO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_banco(dados: dict) -> None:
    with open(BANCO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        f.write("\n")


def carregar_transcricao() -> dict:
    with open(TRANSCRICAO, "r", encoding="utf-8") as f:
        return json.load(f)


def aplicar(banco: dict, transcricao: dict) -> dict:
    cidades = banco["cities"]
    categorias_def = transcricao["categorias"]
    doc = transcricao["documento"]
    vigencia = transcricao["vigencia"]
    fonte_url = transcricao["fonte_url"]

    contagem: dict = {}
    afetados = 0
    for chave, dados in cidades.items():
        if dados.get("prestador_saneamento") != "CASAN":
            continue
        afetados += 1
        novas_cats = {}
        for cat_id, cat_info in categorias_def.items():
            registro = {
                "faixas": cat_info["faixas"],
                "faixas_desc": cat_info["faixas_desc"],
                "tarifa_fixa_mensal": float(cat_info["tarifa_fixa_mensal"]),
                "regime_tarifario": cat_info["regime_tarifario"],
                "consumo_minimo_faturado_m3": float(cat_info.get("consumo_minimo_faturado_m3", 0.0)),
                "esgoto_modo": int(cat_info["esgoto_modo"]),
                "esgoto_pct": float(cat_info["esgoto_pct"]),
                "fonte_url": fonte_url,
                "fonte_documento": doc,
                "vigencia_saneamento": vigencia,
            }
            erros = [a for a in validar_estrutura(dict(dados, **registro)) if a.gravidade == "erro"]
            if erros:
                raise ValueError(f"{chave} {cat_id}: {erros}")
            novas_cats[cat_id] = registro
            contagem[cat_id] = contagem.get(cat_id, 0) + 1

        dados["categorias"] = novas_cats
        # Marca como auditado com fonte primária
        dados["fonte_documento"] = doc

    return {"afetados": afetados, "categorias": contagem}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aplicar", action="store_true", help="grava as categorias no banco")
    ap.add_argument("--conferir", action="store_true", help="apenas valida sem salvar")
    args = ap.parse_args()

    banco = carregar_banco()
    trans = carregar_transcricao()
    res = aplicar(banco, trans)
    print(f"CASAN: {res['afetados']} municípios processados.")
    for cat, n in res["categorias"].items():
        print(f"  - {cat}: {n} municípios")

    if args.aplicar:
        salvar_banco(banco)
        print("Salvo em:", os.path.relpath(BANCO, RAIZ))

        # Atualiza situação no registro de fontes
        reg = R.carregar()
        for item in reg["itens"]:
            if item["prestador"] == "CASAN":
                item["situacao"] = "transcrito"
                item["uso"] = "tarifas/categorias/casan_2026.json; todas as categorias nos 22 municípios"
        R.gravar(reg)
        print("Registro de fontes atualizado.")
    else:
        print("Modo conferência: nenhuma alteração gravada. Use --aplicar para salvar.")


if __name__ == "__main__":
    main()
