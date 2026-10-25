# -*- coding: utf-8 -*-
"""Acrescenta a tabela `qualidade` e as chaves de `metadados` ao banco de chuva da edição IBE/PRT.

Entrada: `qualidade_prototipo.csv` (colunas uid, n, metodo, dtot, drx, ...; E-OBS menos Iberia01,
1971-2000), produzido por `scripts/dados/construir_banco_ibe.py`. A série repetida
(um concelho com a série de outro) é derivada das próprias séries do banco, por SHA-256 da série
descomprimida; com `--prototipo ibe_prototipo.db` confere-se que o conjunto de células
(`unidade_ponto`) dá os mesmos concelhos.

O nível e o motivo vêm de `triton.core.qualidade_chuva` (fórmula única); este script não repete limiar.
Corra a partir de `triton_ibe/`:

    python scripts/acrescentar_qualidade_ao_banco.py --csv tests/dados_ibe/qualidade_prototipo.csv

É idempotente: refaz a tabela e as chaves. As séries (`series`) não são tocadas, e o `sha256_pacote`
(SHA-256 do conteúdo da tabela `series`) por isso não muda.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import os
import sqlite3
import sys
import zlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from triton.core import qualidade_chuva as Q  # noqa: E402

VERSAO_EOBS = "v33.0e"


def sha256_do_pacote(con) -> str:
    """SHA-256 do conteúdo da tabela `series` (dtmn, inicio, dias, dados), em ordem de dtmn."""
    h = hashlib.sha256()
    for dtmn, inicio, dias, dados in con.execute("SELECT dtmn, inicio, dias, dados FROM series ORDER BY dtmn"):
        h.update(f"{dtmn}|{inicio}|{dias}|".encode("utf-8"))
        h.update(dados)
    return h.hexdigest()


def repetidas_por_sha(con) -> set:
    hs = {d: hashlib.sha256(zlib.decompress(b)).hexdigest() for d, b in con.execute("SELECT dtmn, dados FROM series")}
    cont = collections.Counter(hs.values())
    return {d for d, h in hs.items() if cont[h] > 1}


def repetidas_por_celulas(caminho_prototipo: str) -> set:
    con = sqlite3.connect(caminho_prototipo)
    conj = collections.defaultdict(set)
    for u, p in con.execute("SELECT unidade_id, ponto_id FROM unidade_ponto"):
        conj[u].add(p)
    cont = collections.Counter(frozenset(v) for v in conj.values())
    return {u.split("-", 1)[1] for u, v in conj.items() if cont[frozenset(v)] > 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--db", default=os.path.join(RAIZ, "data", "portugal_eobs.db"))
    ap.add_argument("--prototipo", default="", help="ibe_prototipo.db, para conferir a repetição pelas células")
    a = ap.parse_args()

    con = sqlite3.connect(a.db)
    series = {d: c for d, c in con.execute("SELECT dtmn, concelho FROM series")}
    rep = repetidas_por_sha(con)
    if a.prototipo:
        por_celulas = repetidas_por_celulas(a.prototipo)
        assert por_celulas == rep, (sorted(por_celulas ^ rep))
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    dtmns = {r["uid"].split("-", 1)[1] for r in linhas}
    assert dtmns == set(series), (sorted(dtmns ^ set(series))[:10])

    con.execute("DROP TABLE IF EXISTS qualidade")
    con.execute("""CREATE TABLE qualidade (
        dtmn TEXT PRIMARY KEY, concelho TEXT NOT NULL, n_eff INTEGER NOT NULL, metodo TEXT NOT NULL,
        repetida INTEGER NOT NULL CHECK (repetida IN (0, 1)), dtot REAL NOT NULL, drx REAL NOT NULL,
        nivel TEXT NOT NULL CHECK (nivel IN ('A', 'B', 'C')), motivo TEXT NOT NULL)""")
    cont = collections.Counter()
    for r in linhas:
        dtmn = r["uid"].split("-", 1)[1]
        n, metodo = int(r["n"]), r["metodo"]
        dtot, drx = float(r["dtot"]), float(r["drx"])
        repetida = dtmn in rep
        niv = Q.nivel(dtot, drx, n, metodo, repetida)
        cont[niv] += 1
        con.execute("INSERT INTO qualidade VALUES (?,?,?,?,?,?,?,?,?)",
                    (dtmn, series[dtmn], n, metodo, int(repetida), dtot, drx, niv,
                     Q.motivo(dtot, drx, n, metodo, repetida)))
    sha = sha256_do_pacote(con)
    meta = {
        "pacote_id": f"PT-EOBS-{VERSAO_EOBS}-{sha[:8]}",
        "versao_eobs": VERSAO_EOBS,
        "sha256_pacote": sha,
        "qualidade_versao": Q.VERSAO_DA_QUALIDADE,
        "qualidade_referencia": Q.REFERENCIA + "; diferença = E-OBS menos Iberia01",
        "limiares": Q.limiares_em_texto(),
        "espanha_locais": "0",
    }
    for k, v in meta.items():
        con.execute("INSERT OR REPLACE INTO metadados (chave, valor) VALUES (?, ?)", (k, v))
    con.commit()
    con.execute("VACUUM")
    con.close()
    print("níveis:", dict(sorted(cont.items())), "| repetidas:", len(rep), "| pacote_id:", meta["pacote_id"])


if __name__ == "__main__":
    main()
