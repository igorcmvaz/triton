# -*- coding: utf-8 -*-
"""O que cada documento guardado cobre, lido por inteiro, contra o que já foi transcrito.

Um documento recebido pode valer para mais municípios do que a transcrição usou (uma
resolução estadual com a lista de municípios no fim, uma página com abas de vários
anos). Se isso não é visto, o município continua «sem documento» e volta para a lista de
busca, e o autor procura de novo o que já mandou.

Este script lê o texto inteiro de cada arquivo em `tarifas/fontes/` (PDF e HTML; imagem
fica marcada para leitura visual), acha os municípios da base citados como nome próprio
(o mesmo critério de `processar_entrada.py`) e cruza com as transcrições:

- por documento: municípios citados, municípios transcritos, citados e não transcritos;
- por município pendente (sem documento, dado ruim, a confirmar): os documentos já
  recebidos que o citam. Esses saem da lista de busca e entram na fila de transcrição.

Saídas: `tarifas/transcricoes/COBERTURA.md` e `tarifas/transcricoes/cobertura.json`
(lido por `gerar_o_que_buscar.py`).

    python tarifas/auditar_cobertura.py
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _p in (AQUI, os.path.join(RAIZ, "manual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import procedencia as P  # noqa: E402
import processar_entrada as E  # noqa: E402
import registro_de_fontes as R  # noqa: E402
import tabela_de_faixas as T  # noqa: E402

SAIDA_MD = os.path.join(AQUI, "transcricoes", "COBERTURA.md")
SAIDA_JSON = os.path.join(AQUI, "transcricoes", "cobertura.json")
IMAGEM = (".png", ".jpg", ".jpeg", ".gif", ".webp")
PENDENTES = ("sem_documento", "ruim", "a_confirmar")
#: Imagens salvas com as páginas (`*_files/`) já olhadas e sem tabela tarifária a transcrever,
#: com o que mostram. Imagem grande que nenhuma transcrição cita e que não está aqui é tabela
#: possivelmente não lida (a tabela de 2026 do SAMAE Gaspar e a de Americana estavam assim).
IMAGENS_CONFERIDAS = os.path.join(AQUI, "transcricoes", "imagens_conferidas.json")
IMAGEM_MINIMA = 15_000  # bytes: abaixo disso, ícones e logotipos


def municipios_citados(texto: str, cidades: dict) -> dict:
    """{«UF - Município»: citações}, nome próprio, do nome mais longo para o mais curto."""
    texto = E._sem_acento(texto)
    achados = {}
    for chave, d in sorted(cidades.items(), key=lambda kv: -len(kv[1]["municipio"])):
        nome = E._sem_acento(d["municipio"])
        if len(nome) < 5:
            continue
        n = E._citacoes(nome, texto)
        if n:
            achados[chave] = n
            for f in (nome, nome.upper()):
                texto = re.sub(r"(?<![\w])" + re.escape(f) + r"(?![\w])", " ", texto)
    return achados


def _transcritos() -> dict:
    """{id do registro: {municípios transcritos}}."""
    por_item = defaultdict(set)
    for c in glob.glob(os.path.join(AQUI, "transcricoes", "*.json")):
        if os.path.basename(c) in ("historico.json", "cobertura.json", "imagens_conferidas.json"):
            continue
        t = json.load(open(c, encoding="utf-8"))
        for tab in t.get("tabelas", []):
            for m in tab.get("municipios", []):
                for i in t.get("registro", []):
                    por_item[i].add(f"{tab['uf']} - {m}")
    return por_item


CACHE = os.path.join(AQUI, "transcricoes", ".cobertura_cache.json")


def _cache() -> dict:
    """{sha256: {"citados": [...], "leitura": ...}}: um documento só é lido de novo se mudar."""
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def auditar() -> dict:
    cidades = T.carregar()
    reg = R.carregar()
    transcritos = _transcritos()
    cache = _cache()
    assinatura_base = str(len(cidades))  # se a base ganhar municípios, tudo é relido
    docs, por_municipio = [], defaultdict(list)
    for item in reg["itens"]:
        caminho = os.path.join(RAIZ, item.get("guardado_em") or "")
        if not item.get("guardado_em") or not os.path.isfile(caminho):
            continue
        chave = f"{item['sha256']}:{assinatura_base}"
        if chave in cache:
            citados, leitura = dict.fromkeys(cache[chave]["citados"], 1), cache[chave]["leitura"]
        elif caminho.lower().endswith(IMAGEM):
            citados, leitura = {}, "imagem: lida visualmente"
        else:
            texto = E._texto(caminho)
            citados = municipios_citados(texto, cidades) if texto.strip() else {}
            leitura = "texto" if texto.strip() else "sem texto extraível (digitalizado?)"
        cache[chave] = {"citados": sorted(citados), "leitura": leitura}
        usados = transcritos.get(item["id"], set())
        doc = {"id": item["id"], "arquivo": item["arquivo"], "prestador": item["prestador"],
               "situacao": item["situacao"], "leitura": leitura,
               "citados": sorted(citados), "transcritos": sorted(usados),
               "citados_nao_transcritos": sorted(set(citados) - usados)}
        docs.append(doc)
        for m in citados:
            por_municipio[m].append(item["id"])
    with open(CACHE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(cache, f, ensure_ascii=False)
    pendentes = {}
    for chave, d in cidades.items():
        classe = P.classe(d)
        if classe in PENDENTES and por_municipio.get(chave):
            pendentes[chave] = {"classe": classe, "prestador": d.get("prestador_saneamento", ""),
                                "documentos": sorted(set(por_municipio[chave]))}
    return {"gerado_em": date.today().isoformat(), "documentos": docs, "pendentes_com_documento": pendentes,
            "imagens_nao_conferidas": imagens_nao_conferidas()}


def imagens_nao_conferidas() -> list:
    """Imagens de página (`*_files/`) acima do tamanho mínimo que ninguém leu.

    Lida = citada pelo nome em alguma transcrição ou no `uso` do registro, ou listada em
    `transcricoes/imagens_conferidas.json` com o que mostra.
    """
    citado = " ".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(AQUI, "transcricoes", "*.json")))
    citado += " ".join(i.get("uso", "") for i in R.carregar()["itens"])
    conferidas = {}
    if os.path.isfile(IMAGENS_CONFERIDAS):
        with open(IMAGENS_CONFERIDAS, encoding="utf-8") as f:
            conferidas = json.load(f)
    faltam = []
    for pasta in sorted(glob.glob(os.path.join(AQUI, "fontes", "*", "*_files"))):
        for nome in sorted(os.listdir(pasta)):
            caminho = os.path.join(pasta, nome)
            if not nome.lower().endswith(IMAGEM) or os.path.getsize(caminho) < IMAGEM_MINIMA:
                continue
            rel = os.path.relpath(caminho, AQUI).replace(os.sep, "/")
            if nome not in citado and rel not in conferidas:
                faltam.append(rel)
    return faltam


def relatorio(a: dict) -> str:
    reg = {i["id"]: i for i in R.carregar()["itens"]}
    L = ["# Cobertura dos documentos recebidos", "",
         f"Gerado em {a['gerado_em']} por `tarifas/auditar_cobertura.py`. Não edite à mão.", "",
         "Cada documento guardado foi lido por inteiro e cruzado com as transcrições. Município "
         "pendente que um documento já recebido cita **não volta para a lista de busca**: entra aqui, "
         "para ser transcrito ou para se registrar por que o documento não o atende.", ""]
    pend = a["pendentes_com_documento"]
    L += [f"## Pendentes que já têm documento recebido ({len(pend)})", "",
          "| Município | Situação | Prestador na base | Documentos que o citam |", "| :--- | :--- | :--- | :--- |"]
    for chave, p in sorted(pend.items()):
        docs = "; ".join(f"{i} «{reg[i]['arquivo']}» ({reg[i]['situacao']})" for i in p["documentos"])
        L.append(f"| {chave} | {p['classe']} | {p['prestador']} | {docs} |")
    L += ["", "## Documentos que citam municípios não transcritos", "",
          "| Item | Arquivo | Prestador | Situação | Citados não transcritos |", "| :--- | :--- | :--- | :--- | :--- |"]
    for d in a["documentos"]:
        if d["citados_nao_transcritos"]:
            resto = d["citados_nao_transcritos"]
            txt = ", ".join(resto[:12]) + (f" e mais {len(resto) - 12}" if len(resto) > 12 else "")
            L.append(f"| {d['id']} | {d['arquivo']} | {d['prestador']} | {d['situacao']} | {txt} |")
    if a.get("imagens_nao_conferidas"):
        L += ["", f"## Imagens de página não conferidas ({len(a['imagens_nao_conferidas'])})", "",
              "Abra cada uma: se tiver tabela, transcreva; se não, registre o que mostra em "
              "`transcricoes/imagens_conferidas.json`.", ""]
        L += [f"- `{c}`" for c in a["imagens_nao_conferidas"]]
    sem = [d for d in a["documentos"] if d["leitura"] != "texto"]
    if sem:
        L += ["", "## Lidos sem texto (imagem ou digitalizado)", ""]
        L += [f"- {d['id']} «{d['arquivo']}» ({d['prestador']}): {d['leitura']}" for d in sem]
    return "\n".join(L) + "\n"


def gerar() -> dict:
    a = auditar()
    with open(SAIDA_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    with open(SAIDA_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write(relatorio(a))
    return a


if __name__ == "__main__":
    a = gerar()
    print(f"{len(a['documentos'])} documentos lidos; {len(a['pendentes_com_documento'])} municípios pendentes "
          f"já citados por documento recebido -> {os.path.relpath(SAIDA_MD, RAIZ)}")
