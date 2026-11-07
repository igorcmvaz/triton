"""
Divide a base CLIMBra compilada (um único `climbra.db`) em um banco por modelo CMIP6.

Cada parte é `data/climbra_<modelo>.db`, com o mesmo esquema do banco único (tabelas
`climbra_meta`, `climbra_cities`, `climbra_series` e o índice de cidades) e os mesmos blobs,
byte a byte: a série lida de uma parte é idêntica à lida do banco único. Cada parte tem 40 a
44 MB, abaixo do aviso do GitHub (50 MB) e do limite (100 MB) por arquivo.

Uso:

    python scripts/dividir_base_climbra.py                       # data/climbra.db -> data/climbra_<modelo>.db
    python scripts/dividir_base_climbra.py --origem X.db --destino pasta/
    python scripts/dividir_base_climbra.py --verificar           # só confere as partes de data/
    python scripts/dividir_base_climbra.py --verificar --origem data/climbra.db   # e compara com o banco único

Se algum modelo passar do limite (`--limite-mb`, padrão 50), o script o divide por cenário:
`climbra_<modelo>__HIST.db`, `climbra_<modelo>__SSP245.db`, `climbra_<modelo>__SSP585.db`.
`--por-cenario` força esse formato. O leitor (`triton/core/climate_database.py`) entende os dois.

Além das partes, grava `climbra_partes.json` (arquivo, modelo, tamanho, SHA-256 do arquivo e
do conteúdo) para conferir a integridade depois de baixar ou copiar a base.

A tabela `climbra_meta` de cada parte traz: title, source_article, article_doi, repository_doi,
license, dtype, compression (como no banco único) e ainda model, scenarios, cities, total_series,
total_cities, periods (JSON: início, dias e fim por cenário), schema_version ("2"), layout,
content_sha256 (SHA-256 sobre cidade, cenário, contagem e bytes de cada série, em ordem), created_at
e, ao dividir, split_from_compiled_at.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
import zlib
from datetime import datetime, timedelta
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "2"
LAYOUT_POR_MODELO = "per-model"
LAYOUT_POR_CENARIO = "per-model-scenario"
CENARIOS = ("HIST", "SSP245", "SSP585")
INICIO_DO_CENARIO = {"HIST": (1980, 1, 1), "SSP245": (2015, 1, 1), "SSP585": (2015, 1, 1)}
LIMITE_PADRAO_MB = 50.0   # limite do projeto (MiB): o GitHub avisa em 50 e recusa em 100
AVISO_GITHUB_MB = 50.0    # o GitHub avisa a partir de 50 MB
NOME_DO_MANIFESTO = "climbra_partes.json"
NOME_DO_BANCO_UNICO = "climbra.db"

ESQUEMA = (
    """CREATE TABLE climbra_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );""",
    """CREATE TABLE climbra_cities (
        city TEXT PRIMARY KEY,
        city_norm TEXT NOT NULL
    );""",
    "CREATE INDEX idx_climbra_cities_norm ON climbra_cities(city_norm);",
    """CREATE TABLE climbra_series (
        city TEXT NOT NULL,
        model TEXT NOT NULL,
        scenario TEXT NOT NULL,
        count INTEGER NOT NULL,
        data BLOB NOT NULL,
        PRIMARY KEY (city, model, scenario)
    );""",
)

#: Chaves do banco único repassadas às partes (o título é reescrito).
META_HERDADA = ("source_article", "article_doi", "repository_doi", "license", "dtype", "compression")
TITULO = "CLIMBra - Climate Change Dataset for Brazil (CMIP6 / Triton)"


def nome_da_parte(modelo: str, cenario: Optional[str] = None) -> str:
    return f"climbra_{modelo}.db" if cenario is None else f"climbra_{modelo}__{cenario}.db"


def _ro(caminho: str) -> sqlite3.Connection:
    from pathlib import Path
    return sqlite3.connect(Path(caminho).resolve().as_uri() + "?mode=ro", uri=True)


def sha256_do_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


class HashDoConteudo:
    """SHA-256 sobre as séries de uma parte, em ordem (cidade, cenário): independe do layout do arquivo."""

    def __init__(self) -> None:
        self._h = hashlib.sha256()

    def somar(self, cidade: str, cenario: str, contagem: int, blob: bytes) -> None:
        self._h.update(cidade.encode("utf-8") + b"\0" + cenario.encode("utf-8") + b"\0"
                       + str(int(contagem)).encode("ascii") + b"\0" + bytes(blob))

    def hexdigest(self) -> str:
        return self._h.hexdigest()


def hash_do_conteudo_do_banco(caminho: str, modelo: Optional[str] = None) -> Tuple[str, int]:
    """(hash, número de séries) lendo o banco; `modelo` filtra, se o banco tiver vários."""
    h = HashDoConteudo()
    n = 0
    conn = _ro(caminho)
    try:
        consulta = "SELECT city, scenario, count, data FROM climbra_series"
        args: tuple = ()
        if modelo is not None:
            consulta += " WHERE model = ?"
            args = (modelo,)
        for cidade, cenario, contagem, blob in conn.execute(consulta + " ORDER BY city, scenario;", args):
            h.somar(cidade, cenario, contagem, blob)
            n += 1
    finally:
        conn.close()
    return h.hexdigest(), n


def periodos(contagens: Dict[str, Tuple[int, int]]) -> str:
    """JSON {cenário: {start, days_min, days_max, end}} a partir de (mín, máx) de dias por cenário."""
    saida = {}
    for cenario, (dmin, dmax) in sorted(contagens.items()):
        a, m, d = INICIO_DO_CENARIO.get(cenario, (1980, 1, 1))
        inicio = datetime(a, m, d)
        fim = inicio + timedelta(days=dmax - 1)
        saida[cenario] = {"start": inicio.strftime("%Y-%m-%d"), "days_min": dmin, "days_max": dmax,
                          "end": fim.strftime("%Y-%m-%d")}
    return json.dumps(saida, sort_keys=True)


def gravar_parte(destino: str, modelo: str, cidades: Sequence[Tuple[str, str]],
                 series: Iterable[Tuple[str, str, int, bytes]], meta_base: Dict[str, str],
                 cenario: Optional[str] = None, origem_compilada_em: Optional[str] = None) -> Dict[str, object]:
    """Cria um banco de parte e devolve o seu registro para o manifesto.

    `series` entrega (cidade, cenário, contagem, blob) já em ordem (cidade, cenário). Os blobs são
    gravados como vieram: zlib sobre float16 (ou float32), como no banco único.
    """
    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    temporario = destino + ".tmp"
    for lixo in (temporario, temporario + "-journal"):
        if os.path.exists(lixo):
            os.remove(lixo)
    conn = sqlite3.connect(temporario)
    try:
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA journal_mode = MEMORY;")
        for comando in ESQUEMA:
            conn.execute(comando)
        conn.executemany("INSERT INTO climbra_cities (city, city_norm) VALUES (?, ?);", list(cidades))

        h = HashDoConteudo()
        n = 0
        dias: Dict[str, List[int]] = {}
        lote: List[tuple] = []
        for cidade, cen, contagem, blob in series:
            h.somar(cidade, cen, contagem, blob)
            lote.append((cidade, modelo, cen, contagem, blob))
            faixa = dias.setdefault(cen, [contagem, contagem])
            faixa[0], faixa[1] = min(faixa[0], contagem), max(faixa[1], contagem)
            n += 1
            if len(lote) >= 500:
                conn.executemany("INSERT INTO climbra_series (city, model, scenario, count, data) VALUES (?, ?, ?, ?, ?);", lote)
                lote.clear()
        if lote:
            conn.executemany("INSERT INTO climbra_series (city, model, scenario, count, data) VALUES (?, ?, ?, ?, ?);", lote)

        cenarios = sorted(dias)
        meta = {"title": TITULO}
        meta.update({k: meta_base[k] for k in META_HERDADA if k in meta_base})
        # o climbra.db antigo citava «art. 48»; o artigo é Scientific Data 10, art. 47 (Crossref, 24/10/2026)
        if "source_article" in meta:
            meta["source_article"] = meta["source_article"].replace("Nature Scientific Data, 10, art. 48", "Scientific Data, 10, art. 47")
        meta.update({
            "model": modelo,
            "scenarios": ",".join(cenarios),
            "total_series": str(n),
            "total_cities": str(len(cidades)),
            "periods": periodos({c: tuple(v) for c, v in dias.items()}),
            "schema_version": SCHEMA_VERSION,
            "layout": LAYOUT_POR_MODELO if cenario is None else LAYOUT_POR_CENARIO,
            "content_sha256": h.hexdigest(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        })
        if origem_compilada_em:
            meta["split_from_compiled_at"] = origem_compilada_em
        conn.executemany("INSERT INTO climbra_meta (key, value) VALUES (?, ?);", sorted(meta.items()))
        conn.commit()
        conn.execute("ANALYZE;")
        conn.commit()
        conn.execute("VACUUM;")
    finally:
        conn.close()
    os.replace(temporario, destino)
    tamanho = os.path.getsize(destino)
    return {"arquivo": os.path.basename(destino), "modelo": modelo, "cenario": cenario, "bytes": tamanho,
            "mb": round(tamanho / (1024 * 1024), 2), "series": n, "content_sha256": h.hexdigest(),
            "sha256": sha256_do_arquivo(destino), "cenarios": cenarios}


def _meta_do_banco(conn: sqlite3.Connection) -> Dict[str, str]:
    return dict(conn.execute("SELECT key, value FROM climbra_meta;").fetchall())


def _series_do_modelo(conn: sqlite3.Connection, modelo: str,
                      cenario: Optional[str] = None) -> Iterator[Tuple[str, str, int, bytes]]:
    consulta = "SELECT city, scenario, count, data FROM climbra_series WHERE model = ?"
    args: tuple = (modelo,)
    if cenario is not None:
        consulta += " AND scenario = ?"
        args = (modelo, cenario)
    yield from conn.execute(consulta + " ORDER BY city, scenario;", args)


def escrever_manifesto(destino_dir: str, registros: List[Dict[str, object]], origem: Optional[Dict[str, object]] = None) -> str:
    caminho = os.path.join(destino_dir, NOME_DO_MANIFESTO)
    manifesto = {
        "schema_version": SCHEMA_VERSION,
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "limite_github_mb": int(LIMITE_PADRAO_MB),
        "origem": origem,
        "partes": sorted(registros, key=lambda r: (str(r["modelo"]), str(r["cenario"] or ""))),
    }
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return caminho


def dividir(origem: str, destino_dir: str, modelos: Optional[Sequence[str]] = None,
            limite_mb: float = LIMITE_PADRAO_MB, por_cenario: bool = False,
            sobrescrever: bool = False, verbose: bool = True) -> List[Dict[str, object]]:
    """Divide o banco único `origem` em partes dentro de `destino_dir`. Devolve os registros do manifesto."""
    if not os.path.isfile(origem):
        raise FileNotFoundError(f"Banco de origem não encontrado: {origem}")
    os.makedirs(destino_dir, exist_ok=True)
    conn = _ro(origem)
    registros: List[Dict[str, object]] = []
    try:
        meta = _meta_do_banco(conn)
        cidades = conn.execute("SELECT city, city_norm FROM climbra_cities ORDER BY city;").fetchall()
        existentes = [m for (m,) in conn.execute("SELECT DISTINCT model FROM climbra_series ORDER BY model;")]
        escolhidos = list(modelos) if modelos else existentes
        ausentes = [m for m in escolhidos if m not in existentes]
        if ausentes:
            raise ValueError(f"Modelos ausentes no banco de origem: {', '.join(ausentes)}")
        t0 = time.time()
        for i, modelo in enumerate(escolhidos, 1):
            def gravar(cen: Optional[str]) -> Dict[str, object]:
                alvo = os.path.join(destino_dir, nome_da_parte(modelo, cen))
                if os.path.exists(alvo) and not sobrescrever:
                    raise FileExistsError(f"{alvo} já existe (use --sobrescrever)")
                return gravar_parte(alvo, modelo, cidades, _series_do_modelo(conn, modelo, cen), meta,
                                    cenario=cen, origem_compilada_em=meta.get("compiled_at"))

            if por_cenario:
                novos = [gravar(c) for c in CENARIOS]
            else:
                inteiro = gravar(None)
                novos = [inteiro]
                if inteiro["mb"] > limite_mb:
                    if verbose:
                        print(f"  {modelo}: {inteiro['mb']} MB > {limite_mb} MB; dividindo por cenário")
                    os.remove(os.path.join(destino_dir, str(inteiro["arquivo"])))
                    novos = [gravar(c) for c in CENARIOS]
            registros.extend(novos)
            if verbose:
                print(f"  [{i:2d}/{len(escolhidos)}] {modelo}: "
                      + ", ".join(f"{r['arquivo']} {r['mb']} MB" for r in novos)
                      + f"  ({time.time() - t0:.0f} s)")
        info_origem = {"arquivo": os.path.basename(origem), "bytes": os.path.getsize(origem),
                       "compiled_at": meta.get("compiled_at"), "total_series": meta.get("total_series")}
    finally:
        conn.close()
    escrever_manifesto(destino_dir, registros, info_origem)
    return registros


def verificar(destino_dir: str, origem: Optional[str] = None, verbose: bool = True) -> List[str]:
    """Confere as partes de `destino_dir`; devolve a lista de problemas (vazia se tudo certo).

    Sem `origem`: hash do arquivo contra o manifesto, hash do conteúdo contra o `climbra_meta`,
    contagens e tamanho contra o limite do GitHub. Com `origem` (banco único): cada série de
    cada parte deve ter contagem e bytes idênticos aos da origem, e a origem não pode ter série
    sem parte.
    """
    problemas: List[str] = []
    caminho_manifesto = os.path.join(destino_dir, NOME_DO_MANIFESTO)
    manifesto = None
    if os.path.isfile(caminho_manifesto):
        with open(caminho_manifesto, encoding="utf-8") as f:
            manifesto = json.load(f)
    else:
        problemas.append(f"manifesto {NOME_DO_MANIFESTO} ausente")
    por_arquivo = {p["arquivo"]: p for p in (manifesto or {}).get("partes", [])}

    arquivos = sorted(f for f in os.listdir(destino_dir)
                      if f.startswith("climbra_") and f.endswith(".db") and f != NOME_DO_BANCO_UNICO)
    for f in sorted(set(por_arquivo) - set(arquivos)):
        problemas.append(f"{f}: no manifesto, mas ausente da pasta")
    if not arquivos:
        problemas.append("nenhuma parte climbra_<modelo>.db encontrada")

    total_origem = 0
    origem_conn = _ro(origem) if origem else None
    try:
        vistos = 0
        for f in arquivos:
            caminho = os.path.join(destino_dir, f)
            mb = os.path.getsize(caminho) / (1024 * 1024)
            if mb >= LIMITE_PADRAO_MB:
                problemas.append(f"{f}: {mb:.1f} MB, acima do limite do projeto ({LIMITE_PADRAO_MB:g} MiB)")
            registro = por_arquivo.get(f)
            if registro is None:
                problemas.append(f"{f}: fora do manifesto")
            elif sha256_do_arquivo(caminho) != registro["sha256"]:
                problemas.append(f"{f}: SHA-256 do arquivo difere do manifesto")
            conn = _ro(caminho)
            try:
                if conn.execute("PRAGMA quick_check;").fetchone()[0] != "ok":
                    problemas.append(f"{f}: PRAGMA quick_check falhou")
                meta = _meta_do_banco(conn)
                modelo = meta.get("model")
                if not modelo:
                    problemas.append(f"{f}: climbra_meta sem 'model'")
                    continue
                modelos_no_banco = [m for (m,) in conn.execute("SELECT DISTINCT model FROM climbra_series;")]
                if modelos_no_banco != [modelo]:
                    problemas.append(f"{f}: contém modelos {modelos_no_banco}, esperado [{modelo}]")
                esperado = nome_da_parte(modelo, None if meta.get("layout") == LAYOUT_POR_MODELO
                                         else (meta.get("scenarios") or "").split(",")[0])
                if esperado != f:
                    problemas.append(f"{f}: o nome não corresponde ao conteúdo (esperado {esperado})")
                h = HashDoConteudo()
                n = 0
                for cidade, cen, contagem, blob in conn.execute(
                        "SELECT city, scenario, count, data FROM climbra_series ORDER BY city, scenario;"):
                    h.somar(cidade, cen, contagem, blob)
                    n += 1
                    if origem_conn is not None:
                        linha = origem_conn.execute(
                            "SELECT count, data FROM climbra_series WHERE city = ? AND model = ? AND scenario = ?;",
                            (cidade, modelo, cen)).fetchone()
                        if linha is None or linha[0] != contagem or bytes(linha[1]) != bytes(blob):
                            problemas.append(f"{f}: série {cidade}/{modelo}/{cen} difere da origem")
                if h.hexdigest() != meta.get("content_sha256"):
                    problemas.append(f"{f}: hash do conteúdo difere do climbra_meta")
                if str(n) != meta.get("total_series"):
                    problemas.append(f"{f}: total_series={meta.get('total_series')}, lidas {n}")
                n_cidades = conn.execute("SELECT count(*) FROM climbra_cities;").fetchone()[0]
                if str(n_cidades) != meta.get("total_cities"):
                    problemas.append(f"{f}: total_cities={meta.get('total_cities')}, tabela com {n_cidades}")
                vistos += n
                if verbose:
                    print(f"  {f}: {n} séries, {mb:.1f} MB")
            finally:
                conn.close()
        if origem_conn is not None:
            total_origem = origem_conn.execute("SELECT count(*) FROM climbra_series;").fetchone()[0]
            if vistos != total_origem:
                problemas.append(f"origem tem {total_origem} séries; as partes somam {vistos}")
            cidades_o = origem_conn.execute("SELECT city, city_norm FROM climbra_cities ORDER BY city;").fetchall()
            for f in arquivos:
                conn = _ro(os.path.join(destino_dir, f))
                try:
                    if conn.execute("SELECT city, city_norm FROM climbra_cities ORDER BY city;").fetchall() != cidades_o:
                        problemas.append(f"{f}: tabela de cidades difere da origem")
                finally:
                    conn.close()
    finally:
        if origem_conn is not None:
            origem_conn.close()
    return problemas


def main(argv: Optional[Sequence[str]] = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    pasta_data = os.path.normpath(os.path.join(raiz, "data"))
    ap = argparse.ArgumentParser(description="Divide o climbra.db em um banco por modelo CMIP6")
    ap.add_argument("--origem", default=os.path.join(pasta_data, NOME_DO_BANCO_UNICO), help="banco único de origem")
    ap.add_argument("--destino", default=pasta_data, help="pasta das partes (padrão: data/)")
    ap.add_argument("--modelo", action="append", help="só este modelo (repetível)")
    ap.add_argument("--limite-mb", type=float, default=LIMITE_PADRAO_MB,
                    help="acima disto, o modelo é dividido por cenário (padrão: %(default)s)")
    ap.add_argument("--por-cenario", action="store_true", help="força a divisão de cada modelo por cenário")
    ap.add_argument("--sobrescrever", action="store_true", help="substitui partes existentes")
    ap.add_argument("--verificar", action="store_true",
                    help="não divide: confere as partes de --destino (e as compara com --origem, se ela existir)")
    ap.add_argument("--sem-comparar", action="store_true", help="com --verificar, não compara com a origem")
    args = ap.parse_args(argv)

    if args.verificar:
        origem = args.origem if (os.path.isfile(args.origem) and not args.sem_comparar) else None
        print(f"[*] Verificando as partes em '{args.destino}'" + (f" contra '{origem}'" if origem else ""))
        problemas = verificar(args.destino, origem)
    else:
        print(f"[*] Dividindo '{args.origem}' em '{args.destino}'")
        try:
            registros = dividir(args.origem, args.destino, args.modelo, args.limite_mb, args.por_cenario, args.sobrescrever)
        except (FileNotFoundError, FileExistsError, ValueError) as erro:
            print(f"[ERRO] {erro}")
            return 2
        maior = max(r["mb"] for r in registros)
        print(f"[*] {len(registros)} parte(s), {sum(r['mb'] for r in registros):.1f} MB no total, a maior com {maior} MB")
        if maior >= AVISO_GITHUB_MB:
            print(f"[AVISO] Há parte com mais de {AVISO_GITHUB_MB:.0f} MB: o GitHub avisa ao enviar.")
        print("[*] Verificando as partes contra a origem...")
        problemas = verificar(args.destino, args.origem if not args.modelo else None, verbose=False)
    if problemas:
        for p in problemas:
            print(f"[ERRO] {p}")
        return 1
    print("[OK] Partes íntegras" + ("" if args.verificar else " e idênticas ao banco único") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
