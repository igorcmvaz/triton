# -*- coding: utf-8 -*-
"""Vigia os documentos de ``fontes/FONTES.tsv``: mudou algum tarifário desde a recolha?

Ferramenta de desenvolvimento (fica fora do Git, como ``tarifas_portugal/*.py``). Para cada URL
de FONTES.tsv faz UM pedido GET, com User-Agent que se identifica, pausa entre pedidos e sem
insistir: um 403 ou 429 fica registado como «não respondeu» e o anfitrião não volta a ser
contactado nesta rodada (o ``Retry-After`` vai para o relatório). Nada é guardado em disco: o
corpo da resposta só serve para calcular o SHA-256 e o tamanho, que se comparam com os registados.

* SHA-256 registado: a 3.ª coluna de FONTES.tsv;
* tamanho registado: o do ficheiro arquivado em ``fontes/`` (FONTES.tsv não o traz), se existir.

Escreve ``tarifas_portugal/FILA.md`` com as secções «mudou», «não respondeu», «sem alteração» e as
linhas sem URL (entregues pelo autor, não vigiáveis). Um tarifário que mudou é candidato a nova
recolha: abrir o documento, arquivá-lo em ``fontes/``, registá-lo em FONTES.tsv e transcrevê-lo.
Páginas HTML (Águas de Santarém) podem mudar de hash por razões triviais (scripts, datas): conferir
à vista antes de concluir que o tarifário mudou. Não altera FONTES.tsv.

Uso (na pasta ``triton_prt``):
    python tarifas_portugal/monitorar_tarifas.py [--pausa 3] [--so-listar]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from urllib.parse import urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes", "FONTES.tsv")
PASTA = os.path.join(AQUI, "fontes")
FILA = os.path.join(AQUI, "FILA.md")
NL = chr(10)
AGENTE = ("TritonIBE-monitor/1.0 (Universidade Federal de Santa Catarina; verificação anual de tarifários "
          "de águas; um pedido por documento; contacto: ver o README do repositório)")
LIMITE = 60 * 1024 * 1024


def url_de(origem: str) -> str:
    m = re.search(r"https?://\S+", origem)
    return m.group(0) if m else ""


def ler_fontes() -> list:
    out = []
    with open(FONTES, encoding="utf-8") as f:
        for linha in f:
            linha = linha.rstrip(NL).rstrip(chr(13))
            if not linha.strip():
                continue
            c = linha.split("\t")
            caminho = os.path.join(PASTA, *c[0].split("/"))
            out.append({"caminho": c[0], "origem": c[1], "sha256": c[2], "data": c[3] if len(c) > 3 else "",
                        "url": url_de(c[1]),
                        "bytes": os.path.getsize(caminho) if os.path.isfile(caminho) else None})
    return out


def buscar(url: str) -> dict:
    """Um GET. Devolve {estado, http, sha256, bytes, nota}; estado: ok | recusou | erro."""
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            h = hashlib.sha256()
            n = 0
            primeiro = b""
            while True:
                bloco = r.read(1 << 20)
                if not bloco:
                    break
                if not primeiro:
                    primeiro = bloco[:8]
                n += len(bloco)
                if n > LIMITE:
                    return {"estado": "erro", "http": r.status, "nota": "resposta maior que 60 MB: não lida"}
                h.update(bloco)
            nota = ""
            if url.lower().split("?")[0].endswith(".pdf") and not primeiro.startswith(b"%PDF"):
                nota = "o endereço de um PDF devolveu outra coisa (página de erro?)"
            return {"estado": "ok", "http": r.status, "sha256": h.hexdigest(), "bytes": n, "nota": nota}
    except urllib.error.HTTPError as e:
        estado = "recusou" if e.code in (403, 429) else "erro"
        nota = f"Retry-After: {e.headers.get('Retry-After')}" if e.headers.get("Retry-After") else ""
        return {"estado": estado, "http": e.code, "nota": nota}
    except Exception as e:  # sem rede, certificado, tempo esgotado...
        return {"estado": "erro", "http": 0, "nota": f"{type(e).__name__}: {str(e)[:100]}"}


def vigiar(pausa: float, so_listar: bool) -> list:
    itens = ler_fontes()
    bloqueados = set()
    ultimo = 0.0
    for it in itens:
        if not it["url"]:
            it["resultado"] = {"estado": "sem_url"}
            continue
        if so_listar:
            it["resultado"] = {"estado": "nao_pedido"}
            continue
        host = urlparse(it["url"]).netloc
        if host in bloqueados:
            it["resultado"] = {"estado": "recusou", "http": 0, "nota": "anfitrião recusou antes (403/429): não insistido"}
            continue
        espera = pausa - (time.time() - ultimo)
        if espera > 0:
            time.sleep(espera)
        it["resultado"] = buscar(it["url"])
        ultimo = time.time()
        if it["resultado"]["estado"] == "recusou":
            bloqueados.add(host)
        print(f"{it['resultado']['estado']:8s} {it['resultado'].get('http', '')} {it['caminho']}", flush=True)
    return itens


def classificar(it: dict) -> str:
    r = it["resultado"]
    if r["estado"] == "sem_url":
        return "sem_url"
    if r["estado"] != "ok":
        return "nao_respondeu"
    if r.get("nota"):
        return "nao_respondeu"
    if r["sha256"] != it["sha256"]:
        return "mudou"
    if it["bytes"] is not None and r["bytes"] != it["bytes"]:
        return "mudou"
    return "sem_alteracao"


def escrever_fila(itens: list, quando: str) -> str:
    grupos = {k: [] for k in ("mudou", "nao_respondeu", "sem_alteracao", "sem_url")}
    for it in itens:
        grupos[classificar(it)].append(it)
    L = ["# Fila dos tarifários de Portugal", "",
         f"Gerado em {quando} por `tarifas_portugal/monitorar_tarifas.py`. Não edite à mão.", "",
         "Um pedido GET por URL de `fontes/FONTES.tsv`, com User-Agent identificado e pausa entre pedidos; "
         "403 e 429 não são repetidos. Compara o SHA-256 (e o tamanho do ficheiro arquivado, quando existe) com o "
         "registado. Nada é descarregado para o disco.", "",
         f"Resumo: **{len(grupos['mudou'])} mudou**, **{len(grupos['nao_respondeu'])} não respondeu**, "
         f"**{len(grupos['sem_alteracao'])} sem alteração**, {len(grupos['sem_url'])} sem URL (não vigiáveis).", ""]
    L += ["## Mudou", "",
          "Candidatos a nova recolha (as páginas HTML podem mudar por razões triviais: conferir à vista).", ""]
    if grupos["mudou"]:
        L += ["| Ficheiro | URL | SHA-256 registado | SHA-256 agora | Tamanho registado | Tamanho agora |",
              "| :--- | :--- | :--- | :--- | ---: | ---: |"]
        for it in grupos["mudou"]:
            r = it["resultado"]
            L.append(f"| {it['caminho']} | {it['url']} | `{it['sha256'][:12]}…` | `{r['sha256'][:12]}…` | "
                     f"{it['bytes'] if it['bytes'] is not None else '—'} | {r['bytes']} |")
    else:
        L.append("Nenhum.")
    L += ["", "## Não respondeu", ""]
    if grupos["nao_respondeu"]:
        L += ["| Ficheiro | URL | Resposta | Nota |", "| :--- | :--- | :--- | :--- |"]
        for it in grupos["nao_respondeu"]:
            r = it["resultado"]
            L.append(f"| {it['caminho']} | {it['url']} | {r.get('http') or 'sem resposta'} | {r.get('nota', '')} |")
    else:
        L.append("Nenhum.")
    L += ["", "## Sem alteração", ""]
    if grupos["sem_alteracao"]:
        L += ["| Ficheiro | URL | SHA-256 |", "| :--- | :--- | :--- |"]
        for it in grupos["sem_alteracao"]:
            L.append(f"| {it['caminho']} | {it['url']} | `{it['sha256'][:12]}…` |")
    else:
        L.append("Nenhum.")
    L += ["", "## Sem URL", "",
          "Documentos entregues pelo autor, sem endereço de origem em FONTES.tsv: não há o que vigiar. Quando possível, "
          "procurar o endereço no sítio da entidade e registá-lo.", ""]
    if grupos["sem_url"]:
        L += ["| Ficheiro | Origem registada |", "| :--- | :--- |"]
        for it in grupos["sem_url"]:
            L.append(f"| {it['caminho']} | {it['origem']} |")
    else:
        L.append("Nenhum.")
    L.append("")
    texto = NL.join(L)
    with open(FILA, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return texto


def atualizar_confirmacao(itens: list, hoje: str) -> int:
    """Grava ``confirmado_em`` = hoje (coluna 9 de FONTES.tsv) nos documentos sem alteração. Só a pedido
    do mantenedor (``--atualizar-confirmacao``): a confirmação é um ato dele, e só vale para documentos
    cujo hash não mudou e que ele conferiu estarem ainda em vigor."""
    certos = {it["caminho"] for it in itens if classificar(it) == "sem_alteracao" and not it["caminho"].startswith("_")}
    linhas, n = [], 0
    with open(FONTES, encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip(NL).rstrip(chr(13)).split("	")
            if c and c[0] in certos and len(c) >= 9:
                c[8] = hoje
                n += 1
            linhas.append("	".join(c))
    with open(FONTES, "w", encoding="utf-8", newline="") as f:
        f.write(NL.join(linhas) + NL)
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pausa", type=float, default=3.0, help="segundos entre pedidos (por defeito 3)")
    ap.add_argument("--atualizar-confirmacao", action="store_true",
                    help="grava confirmado_em = hoje nos documentos sem alteração (ato do mantenedor)")
    ap.add_argument("--so-listar", action="store_true", help="não pede nada; só lista o que seria vigiado")
    a = ap.parse_args()
    itens = vigiar(a.pausa, a.so_listar)
    escrever_fila(itens, datetime.now().strftime("%Y-%m-%d %H:%M"))
    if a.atualizar_confirmacao and not a.so_listar:
        print(f"confirmado_em atualizado em {atualizar_confirmacao(itens, datetime.now().strftime('%Y-%m-%d'))} linhas")
    print("escrito: " + os.path.relpath(FILA, os.path.dirname(AQUI)))
