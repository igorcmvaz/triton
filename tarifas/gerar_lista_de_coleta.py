# -*- coding: utf-8 -*-
"""A lista de sites a visitar para completar a base tarifária, numa página só.

Para cada prestador de saneamento do catálogo: os municípios que ele atende, a
agência reguladora, o endereço da fonte que a base usou, o que falta coletar
(categorias não residenciais e registros residenciais a confirmar) e se o
material da fonte (a página em HTML ou a tabela em PDF) já chegou, segundo
`tarifas/fontes/registro.json`.

A página separa os prestadores em dois grupos — sem material recebido e com material
recebido — e é regerada sempre que `registro_de_fontes.py` registra um arquivo.

Uso:
    python tarifas/gerar_lista_de_coleta.py

Saída: tarifas/lista_de_coleta.html, autocontida (abre direto do disco).
"""

from __future__ import annotations

import html
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date
from urllib.parse import quote_plus, urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _p in (AQUI, os.path.join(RAIZ, "manual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import registro_de_fontes as R  # noqa: E402
import tabela_de_faixas as T  # noqa: E402

SAIDA = os.path.join(AQUI, "lista_de_coleta.html")
MODELO = os.path.join(AQUI, "lista_de_coleta_modelo.html")

#: As categorias que faltam, na ordem em que a página as mostra.
CATEGORIAS = ["comercial", "publica", "industrial", "social"]


def _tipo(url: str) -> str:
    caminho = urlparse(url).path.lower()
    return "PDF" if caminho.endswith(".pdf") or "/download" in caminho else "página"


def _busca(agencia: str, prestador: str) -> str:
    termos = f"{agencia} resolução tarifária {prestador} {date.today().year}"
    return "https://www.google.com/search?q=" + quote_plus(termos)


def dados() -> dict:
    cidades = T.carregar()
    registro = R.carregar()
    recebidos = defaultdict(list)
    for item in registro["itens"]:
        recebidos[item["prestador"]].append({
            "arquivo": item["arquivo"], "data": item["recebido_em"],
            "situacao": R.SITUACOES.get(item["situacao"], item["situacao"]),
            "conteudo": item["conteudo"]})

    grupos = defaultdict(list)
    for d in cidades.values():
        grupos[d.get("prestador_saneamento") or "—"].append(d)

    prestadores = []
    for nome, lista in grupos.items():
        lista.sort(key=lambda d: (d["uf"], d["municipio"]))
        faltam = Counter()
        municipios = []
        for d in lista:
            extra = d.get("categorias") or {}
            ausentes = [c for c in CATEGORIAS if c not in extra]
            faltam.update(ausentes)
            municipios.append({"m": d["municipio"], "uf": d["uf"], "res": T.situacao(d),
                               "faltam": ausentes})
        urls = sorted({d.get("fonte_url") for d in lista if d.get("fonte_url")})
        agencias = sorted({d.get("agencia_reguladora") or "—" for d in lista})
        vigencias = Counter(d.get("vigencia_saneamento") or "" for d in lista)
        prestadores.append({
            "nome": nome,
            "pasta": "tarifas/entrada/" + R._pasta(nome) + "/",
            "ufs": sorted({d["uf"] for d in lista}),
            "agencias": agencias,
            "fontes": [{"url": u, "tipo": _tipo(u), "dominio": urlparse(u).netloc.removeprefix("www.")}
                       for u in urls],
            "busca": _busca(agencias[0], nome),
            "n": len(lista),
            "faltam": {c: faltam[c] for c in CATEGORIAS},
            "confirmar": sum(1 for m in municipios if m["res"] != "verde"),
            "vermelhos": sum(1 for m in municipios if m["res"] == "vermelho"),
            "vigencia": vigencias.most_common(1)[0][0],
            "municipios": municipios,
            "recebido": recebidos.get(nome, []),
        })
    prestadores.sort(key=lambda p: (-p["n"], p["nome"].lower()))
    return {"gerado_em": date.today().isoformat(), "prestadores": prestadores}


#: O que o arquivo local leva antes do conteúdo; o artefato publicado recebe isso do servidor.
CABECALHO = ('<!doctype html>\n<html lang="pt-BR">\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')


def pagina() -> tuple[str, dict]:
    """O conteúdo da página (sem o esqueleto do documento) e os dados que ele leva."""
    conteudo = dados()
    modelo = open(MODELO, encoding="utf-8").read()
    carga = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    texto = modelo.replace("/*DADOS*/null", carga).replace("{{GERADO_EM}}", html.escape(conteudo["gerado_em"]))
    return texto, conteudo


def gerar(saida: str = SAIDA, artefato: str = "") -> dict:
    texto, conteudo = pagina()
    with open(saida, "w", encoding="utf-8", newline="") as f:
        f.write(CABECALHO + texto)
    if artefato:
        with open(artefato, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
    return conteudo


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artefato", default="", help="grava também o conteúdo sem o esqueleto do documento")
    args = ap.parse_args()
    ps = gerar(artefato=args.artefato)["prestadores"]
    com = sum(1 for p in ps if p["recebido"])
    print(f"lista de coleta: {len(ps)} prestadores, {com} com material recebido -> "
          f"{os.path.relpath(SAIDA, RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
