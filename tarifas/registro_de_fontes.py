# -*- coding: utf-8 -*-
"""Registro do material recebido para a base tarifária: o que chegou, quando, e o que virou.

Todo PDF, planilha ou página que o usuário manda entra aqui antes de ser usado. O
registro guarda a impressão digital SHA-256 do arquivo, a data de recebimento, o
prestador, o conteúdo, onde o arquivo foi guardado e o que foi feito com ele. Um
arquivo já recebido é reconhecido pela impressão digital, ainda que venha com outro
nome: é o que evita reenviar e retranscrever o mesmo material.

O registro mora em `tarifas/fontes/registro.json`, e `tarifas/fontes/REGISTRO.md` é
gerado dele, com a lista do que ainda falta coletar, por prestador, em ordem de
municípios atendidos.

Uso
---
    python tarifas/registro_de_fontes.py conferir ARQUIVO
    python tarifas/registro_de_fontes.py registrar ARQUIVO --prestador CORSAN \\
        --conteudo "Tabela I, todas as categorias" --vigencia 01/07/2026 \\
        --situacao transcrito --uso "tarifas/categorias/corsan_2026.json"
    python tarifas/registro_de_fontes.py registrar ARQUIVO ... --nao-guardar --motivo "licenciada"
    python tarifas/registro_de_fontes.py situacao ID --situacao transcrito --uso "..."
    python tarifas/registro_de_fontes.py gerar
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from collections import Counter
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FONTES = os.path.join(AQUI, "fontes")
REGISTRO = os.path.join(FONTES, "registro.json")
RELATORIO = os.path.join(FONTES, "REGISTRO.md")
NL = chr(10)

#: O que pode ter acontecido com o material.
SITUACOES = {
    "recebido": "recebido, ainda não usado",
    "transcrito": "transcrito para a base",
    "consultado": "consultado, sem dado para a base",
    "descartado": "descartado (duplicado, ilegível ou fora de escopo)",
}


def impressao(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def carregar() -> dict:
    if not os.path.exists(REGISTRO):
        return {"itens": []}
    with open(REGISTRO, encoding="utf-8") as f:
        return json.load(f)


def gravar(reg: dict) -> None:
    with open(REGISTRO, "w", encoding="utf-8", newline="") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write(NL)
    gerar(reg)


def _pasta(prestador: str) -> str:
    nome = re.sub(r"[^a-z0-9]+", "_", prestador.lower()).strip("_")
    return nome or "outros"


def ja_recebido(reg: dict, sha: str):
    return next((i for i in reg["itens"] if i["sha256"] == sha), None)


def registrar(caminho: str, prestador: str, conteudo: str, vigencia: str = "",
              situacao: str = "recebido", uso: str = "", guardar: bool = True,
              motivo: str = "", recebido_em: str = "", nome: str = "") -> dict:
    reg = carregar()
    sha = impressao(caminho)
    anterior = ja_recebido(reg, sha)
    if anterior:
        raise SystemExit(f"já recebido em {anterior['recebido_em']} como «{anterior['arquivo']}» "
                         f"(item {anterior['id']}, {SITUACOES[anterior['situacao']]})")
    arquivo = nome or re.sub(r"^[0-9a-f]{8}-", "", os.path.basename(caminho))
    destino = ""
    if guardar:
        pasta = os.path.join(FONTES, _pasta(prestador))
        os.makedirs(pasta, exist_ok=True)
        destino = os.path.join(pasta, arquivo)
        if not os.path.exists(destino) or impressao(destino) != sha:
            shutil.copy2(caminho, destino)
        destino = os.path.relpath(destino, RAIZ).replace(os.sep, "/")
    item = {
        "id": max((i["id"] for i in reg["itens"]), default=0) + 1,
        "recebido_em": recebido_em or date.today().isoformat(),
        "arquivo": arquivo,
        "sha256": sha,
        "bytes": os.path.getsize(caminho),
        "prestador": prestador,
        "conteudo": conteudo,
        "vigencia": vigencia,
        "guardado_em": destino,
        "nao_guardado_motivo": "" if guardar else (motivo or "não guardado"),
        "situacao": situacao,
        "uso": uso,
    }
    reg["itens"].append(item)
    gravar(reg)
    return item


def mudar_situacao(id_: int, situacao: str, uso: str = "") -> dict:
    reg = carregar()
    item = next(i for i in reg["itens"] if i["id"] == id_)
    item["situacao"] = situacao
    if uso:
        item["uso"] = uso
    gravar(reg)
    return item


def _lacunas():
    """[(prestador, municípios, categorias faltando, residencial a confirmar)] da base."""
    sys.path.insert(0, os.path.join(RAIZ, "manual"))
    import tabela_de_faixas as t
    cidades = t.carregar()
    por_prestador = {}
    for d in cidades.values():
        p = d.get("prestador_saneamento") or "—"
        reg = por_prestador.setdefault(p, {"municipios": 0, "faltam": Counter(), "confirmar": 0})
        reg["municipios"] += 1
        extra = d.get("categorias") or {}
        for cat in t.CATEGORIAS[1:]:
            if cat not in extra:
                reg["faltam"][cat] += 1
        if t.situacao(d) != "verde":
            reg["confirmar"] += 1
    return sorted(por_prestador.items(), key=lambda kv: (-kv[1]["municipios"], kv[0].lower()))


def gerar(reg: dict | None = None) -> None:
    reg = reg or carregar()
    L = ["# Registro do material recebido para a base tarifária", "",
         "Gerado por `tarifas/registro_de_fontes.py` a partir de `registro.json`. Não edite à mão.", "",
         "Antes de mandar um arquivo, confira aqui se ele já veio: o registro reconhece o "
         "arquivo pela impressão digital SHA-256, ainda que o nome mude.", "",
         "## O que já chegou", "",
         "| # | Recebido | Arquivo | Prestador | Conteúdo | Vigência | Situação | Onde está / uso |",
         "| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
    for i in reg["itens"]:
        onde = i["guardado_em"] or f"não guardado: {i['nao_guardado_motivo']}"
        if i.get("uso"):
            onde += f"; uso: {i['uso']}"
        L.append(f"| {i['id']} | {i['recebido_em']} | {i['arquivo']} | {i['prestador']} | "
                 f"{i['conteudo']} | {i.get('vigencia') or '—'} | {SITUACOES[i['situacao']]} | {onde} |")
    L += ["", "## O que falta coletar", "",
          "Por prestador, em ordem de municípios atendidos. «Categorias faltando» conta "
          "municípios sem a tabela oficial da categoria; «residencial a confirmar» conta os "
          "registros residenciais que não estão auditados (amarelos ou vermelhos no apêndice D "
          "do manual). O material que mais rende é a resolução tarifária vigente do prestador, "
          "com todas as categorias.", "",
          "| Prestador | Municípios | Comercial | Pública | Industrial | Social | Residencial a confirmar |",
          "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for prestador, d in _lacunas():
        f = d["faltam"]
        if not (sum(f.values()) or d["confirmar"]):
            continue
        L.append(f"| {prestador} | {d['municipios']} | {f['comercial']} | {f['publica']} | "
                 f"{f['industrial']} | {f['social']} | {d['confirmar']} |")
    with open(RELATORIO, "w", encoding="utf-8", newline="") as fh:
        fh.write(NL.join(L) + NL)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("conferir")
    c.add_argument("arquivo")
    r = sub.add_parser("registrar")
    r.add_argument("arquivo")
    r.add_argument("--prestador", required=True)
    r.add_argument("--conteudo", required=True)
    r.add_argument("--vigencia", default="")
    r.add_argument("--situacao", choices=list(SITUACOES), default="recebido")
    r.add_argument("--uso", default="")
    r.add_argument("--nao-guardar", action="store_true")
    r.add_argument("--motivo", default="")
    r.add_argument("--recebido-em", default="")
    r.add_argument("--nome", default="")
    s = sub.add_parser("situacao")
    s.add_argument("id", type=int)
    s.add_argument("--situacao", choices=list(SITUACOES), required=True)
    s.add_argument("--uso", default="")
    sub.add_parser("gerar")
    a = ap.parse_args()
    if a.cmd == "conferir":
        item = ja_recebido(carregar(), impressao(a.arquivo))
        print(f"já recebido: item {item['id']}, {item['recebido_em']}, «{item['arquivo']}», "
              f"{SITUACOES[item['situacao']]}" if item else "novo: ainda não está no registro")
    elif a.cmd == "registrar":
        item = registrar(a.arquivo, a.prestador, a.conteudo, a.vigencia, a.situacao, a.uso,
                         not a.nao_guardar, a.motivo, a.recebido_em, a.nome)
        print(f"registrado: item {item['id']} — {item['arquivo']}")
    elif a.cmd == "situacao":
        mudar_situacao(a.id, a.situacao, a.uso)
        print("atualizado")
    else:
        gerar()
        print(f"gerado: {os.path.relpath(RELATORIO, RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
