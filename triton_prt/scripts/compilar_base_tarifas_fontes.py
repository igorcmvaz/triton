# -*- coding: utf-8 -*-
"""Compila os documentos de terceiros das tarifas num único banco SQLite, para guardar e consultar.

Os PDFs e as páginas salvas dos prestadores de saneamento são material de terceiros: não vão para o
Git. Este script os reúne num arquivo só (`tarifas_portugal/tarifas_portugal_fontes.db`), que fica no disco do
mantenedor, como o `data/climbra.db`. O banco guarda:

* `arquivos`: um registro por arquivo, com o conteúdo comprimido (`zlib`), a impressão digital
  SHA-256 e, para PDF e HTML, o texto extraído (busca por texto com FTS5, se o SQLite a oferecer);
* `metadados`: a data de geração, as contagens e o aviso de que o conteúdo é de terceiros.

A pasta de origem continua como está. O que vai ao Git é só o registro de procedência
(`tarifas_portugal/fontes/FONTES.tsv`): URL e hash de cada documento.

Uso (da raiz da edição):

    python scripts/compilar_base_tarifas_fontes.py                       # compila
    python scripts/compilar_base_tarifas_fontes.py --conferir            # confere o banco contra a pasta
    python scripts/compilar_base_tarifas_fontes.py --restaurar DESTINO   # recria a árvore de arquivos
    python scripts/compilar_base_tarifas_fontes.py --buscar "tarifa social"
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import sqlite3
import sys
import zlib
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PASTA_PADRAO = RAIZ / "tarifas_portugal" / "fontes"
SAIDA_PADRAO = RAIZ / "tarifas_portugal" / "tarifas_portugal_fontes.db"
#: Arquivos que ficam no Git e não entram no banco.
FICAM_NO_GIT = {"registro.json", "REGISTRO.md", "LEIAME.md", "LEIA.md", "procedencia.tsv", "FONTES.tsv"}
AVISO = ("Material de terceiros (documentos de prestadores e agências). Guardado para consulta e conferência do mantenedor; "
         "não redistribuir. A procedência (hash e URL) está em tarifas_portugal/fontes/FONTES.tsv.")


def _tipo(p: Path) -> str:
    return p.suffix.lower().lstrip(".") or "sem_extensao"


def _texto_pdf(dados: bytes) -> str:
    try:
        import io

        from pypdf import PdfReader
        r = PdfReader(io.BytesIO(dados))
        return "\n".join((pg.extract_text() or "") for pg in r.pages)
    except Exception:
        return ""


def _texto_html(dados: bytes) -> str:
    for cod in ("utf-8", "latin-1"):
        try:
            t = dados.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def compilar(pasta: Path, saida: Path) -> None:
    arquivos = sorted(p for p in pasta.rglob("*") if p.is_file() and p.name not in FICAM_NO_GIT)
    if not arquivos:
        sys.exit(f"nada a compilar em {pasta}")
    tmp = saida.with_suffix(".db.novo")
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    con.executescript(
        "CREATE TABLE arquivos (id INTEGER PRIMARY KEY, caminho TEXT UNIQUE NOT NULL, pasta TEXT, nome TEXT, tipo TEXT,"
        " bytes INTEGER, sha256 TEXT, conteudo BLOB, texto TEXT);"
        "CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);")
    total = comprimido = 0
    for n, p in enumerate(arquivos, 1):
        dados = p.read_bytes()
        rel = p.relative_to(pasta).as_posix()
        tipo = _tipo(p)
        texto = _texto_pdf(dados) if tipo == "pdf" else (_texto_html(dados) if tipo in ("htm", "html") else "")
        blob = zlib.compress(dados, 6)
        total += len(dados)
        comprimido += len(blob)
        con.execute("INSERT INTO arquivos (caminho, pasta, nome, tipo, bytes, sha256, conteudo, texto) VALUES (?,?,?,?,?,?,?,?)",
                    (rel, str(Path(rel).parent.as_posix()), p.name, tipo, len(dados), hashlib.sha256(dados).hexdigest(), blob, texto or None))
        if n % 200 == 0:
            print(f"  {n}/{len(arquivos)}", flush=True)
    try:
        con.executescript("CREATE VIRTUAL TABLE busca USING fts5(caminho, texto, content='arquivos', content_rowid='id');"
                          "INSERT INTO busca(rowid, caminho, texto) SELECT id, caminho, coalesce(texto,'') FROM arquivos;")
        fts = "sim"
    except sqlite3.OperationalError:
        fts = "não"
    meta = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "pasta_de_origem": str(pasta.relative_to(RAIZ).as_posix()),
            "arquivos": str(len(arquivos)), "bytes_originais": str(total), "bytes_comprimidos": str(comprimido),
            "busca_de_texto_fts5": fts, "aviso": AVISO}
    con.executemany("INSERT INTO metadados VALUES (?,?)", list(meta.items()))
    con.commit()
    con.execute("VACUUM")
    con.close()
    tmp.replace(saida)
    print(f"{saida.relative_to(RAIZ)}: {len(arquivos)} arquivos, {total / 1e6:.0f} MB -> {saida.stat().st_size / 1e6:.0f} MB (FTS5: {fts})")


def conferir(pasta: Path, saida: Path) -> int:
    con = sqlite3.connect(saida)
    ruins = 0
    banco = {c: (s, b) for c, s, b in con.execute("SELECT caminho, sha256, bytes FROM arquivos")}
    for rel, (sha, tam) in banco.items():
        f = pasta / rel
        if not f.is_file():
            print("falta na pasta:", rel)
            ruins += 1
        elif hashlib.sha256(f.read_bytes()).hexdigest() != sha:
            print("mudou:", rel)
            ruins += 1
    for p in pasta.rglob("*"):
        if p.is_file() and p.name not in FICAM_NO_GIT and p.relative_to(pasta).as_posix() not in banco:
            print("fora do banco:", p.relative_to(pasta).as_posix())
            ruins += 1
    print(f"{len(banco)} arquivos no banco; {ruins} divergência(s)")
    return 1 if ruins else 0


def restaurar(saida: Path, destino: Path) -> None:
    con = sqlite3.connect(saida)
    n = 0
    for rel, sha, blob in con.execute("SELECT caminho, sha256, conteudo FROM arquivos"):
        dados = zlib.decompress(blob)
        if hashlib.sha256(dados).hexdigest() != sha:
            sys.exit(f"impressão digital diferente: {rel}")
        alvo = destino / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(dados)
        n += 1
    print(f"{n} arquivos restaurados em {destino}")


def buscar(saida: Path, termo: str) -> None:
    con = sqlite3.connect(saida)
    for caminho, trecho in con.execute(
            "SELECT caminho, snippet(busca, 1, '[', ']', ' … ', 12) FROM busca WHERE busca MATCH ? LIMIT 25", (termo,)):
        print(f"{caminho}\n    {trecho}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", type=Path, default=PASTA_PADRAO)
    ap.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    ap.add_argument("--conferir", action="store_true")
    ap.add_argument("--restaurar", type=Path, metavar="DESTINO")
    ap.add_argument("--buscar", metavar="TERMO")
    a = ap.parse_args()
    if a.conferir:
        sys.exit(conferir(a.pasta, a.saida))
    if a.restaurar:
        return restaurar(a.saida, a.restaurar)
    if a.buscar:
        return buscar(a.saida, a.buscar)
    compilar(a.pasta, a.saida)


if __name__ == "__main__":
    main()
