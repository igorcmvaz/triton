# -*- coding: utf-8 -*-
"""A lista de sites a visitar para completar a base tarifária, numa página só.

Para cada prestador de saneamento do catálogo: os municípios que ele atende, a
agência reguladora, o endereço da fonte que a base usou, o que falta coletar
(categorias não residenciais e registros residenciais a confirmar) e se o
material da fonte (a página em HTML ou a tabela em PDF) já chegou, segundo
`tarifas/fontes/registro.json`.

Cada município traz a classe de procedência e o documento-base (arquivo, tabela,
vigência, data de recebimento), de `procedencia.py`; o mapa mostra isso por padrão.

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
MAPA = os.path.join(AQUI, "mapa_brasil_uf.json")
COORDENADAS = os.path.join(AQUI, "validated_cidades_50k.json")

#: As categorias que faltam, na ordem em que a página as mostra.
CATEGORIAS = ["comercial", "publica", "industrial", "social"]


def _tipo(url: str) -> str:
    caminho = urlparse(url).path.lower()
    return "PDF" if caminho.endswith(".pdf") or "/download" in caminho else "página"


def _busca(agencia: str, prestador: str) -> str:
    termos = f"{agencia} resolução tarifária {prestador} {date.today().year}"
    return "https://www.google.com/search?q=" + quote_plus(termos)


def _recebidos_do_prestador(nome: str, recebidos: dict, agencias: list[str] | None = None) -> list:
    if not nome or nome == "—":
        return []
    itens = list(recebidos.get(nome, []))
    for pr, lista in recebidos.items():
        if pr != nome:
            p_norm = pr.lower().replace("–", "-").strip()
            n_norm = nome.lower().replace("–", "-").strip()
            if p_norm and (p_norm in n_norm or n_norm in p_norm):
                for it in lista:
                    if it not in itens:
                        itens.append(it)
    if agencias:
        for ag in agencias:
            if ag and ag in recebidos:
                for it in recebidos[ag]:
                    if it not in itens:
                        itens.append(it)
    return itens


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
            "recebido": _recebidos_do_prestador(nome, recebidos, agencias),
        })
    # Em dia: todos os municípios com a residencial documentada e vigente (procedencia.py).
    import procedencia as Pr
    classe = {(d["uf"], d["municipio"]): Pr.classe(d) for d in cidades.values()}
    for p in prestadores:
        cls = [classe[(m["uf"], m["m"])] for m in p["municipios"]]
        p["em_dia"] = sum(1 for c in cls if c in ("completa", "documentada"))
        p["todo_em_dia"] = p["em_dia"] == p["n"]
        p["url"] = p["fontes"][0]["url"] if p["fontes"] else p["busca"]
    # A mesma página serve a vários prestadores (as listas da ARES-PCJ e da ARISB, por
    # exemplo): a página é visitada uma vez, e o cartão diz quem mais está nela.
    por_url = defaultdict(list)
    for p in prestadores:
        por_url[p["url"]].append(p["nome"])
    for p in prestadores:
        p["compartilha"] = sorted(n for n in por_url[p["url"]] if n != p["nome"])
    prestadores.sort(key=lambda p: (-(p["n"] - p["em_dia"]), -p["n"], p["nome"].lower()))
    return {"gerado_em": date.today().isoformat(), "prestadores": prestadores,
            "cidades": _cidades(cidades, recebidos), "mapa": _mapa()}


def _mapa() -> dict:
    """Os contornos dos estados, de `mapa_brasil_uf.json` (gerado por gerar_mapa_brasil.py)."""
    with open(MAPA, encoding="utf-8") as f:
        m = json.load(f)
    return {"largura": m["largura"], "altura": m["altura"], "estados": m["estados"]}


def _cidades(cidades: dict, recebidos: dict) -> list:
    """Uma linha por município, com a posição no mapa e a situação de cada categoria."""
    import gerar_mapa_brasil as G
    with open(MAPA, encoding="utf-8") as f:
        caixa = json.load(f)["caixa"]
    projetar, _ = G.projetor(*caixa)
    import procedencia as P
    itens = {i["id"]: i for i in R.carregar()["itens"]}
    with open(COORDENADAS, encoding="utf-8") as f:
        coordenadas = json.load(f)
    linhas = []
    for d in sorted(cidades.values(), key=lambda d: (d["uf"], d["municipio"])):
        alvo = (coordenadas.get(d["municipio"]) or {}).get("target") or {}
        x, y = projetar(alvo["lon"], alvo["lat"]) if alvo else (None, None)
        extra = d.get("categorias") or {}
        ag = d.get("agencia_reguladora") or ""
        linhas.append({
            "m": d["municipio"], "uf": d["uf"], "p": d.get("prestador_saneamento") or "—",
            "x": None if x is None else round(x, 1), "y": None if y is None else round(y, 1),
            "res": T.situacao(d),
            "cats": [c for c in CATEGORIAS if c in extra],
            "html": bool(_recebidos_do_prestador(d.get("prestador_saneamento"), recebidos, [ag] if ag else None)),
            "cl": P.classe(d),
            "o": P.origem(d, itens),
        })
    return linhas


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
    # A página do que buscar sai dos mesmos dados e se atualiza junto.
    # Primeiro a cobertura (cada documento lido por inteiro), depois a página de busca, que
    # mostra o que já veio e não pede de novo o que já foi mandado.
    import auditar_cobertura
    auditar_cobertura.gerar()
    import gerar_o_que_buscar
    gerar_o_que_buscar.gerar()
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
