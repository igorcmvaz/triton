# -*- coding: utf-8 -*-
"""Falha se algum arquivo rastreado pelo Git passar do limite de tamanho do projeto (50 MB).

O GitHub avisa a partir de 50 MiB e recusa acima de 100 MiB por arquivo; o projeto adota o limite
mais rígido, 50 MiB (52.428.800 bytes), para que nenhuma parte de dados precise de Git LFS. Em
50 MiB = 50 * 1024 * 1024 bytes, a mesma unidade do aviso do GitHub e do teste das partes da CLIMBra
(`tests/unit/test_climbra_particionada.py`). Acima de 45 MiB o arquivo passa, mas é listado como
«perto do limite».

Uso (da raiz do repositório):

    python scripts/verificar_tamanhos.py                  # arquivos rastreados, no disco (git ls-files)
    python scripts/verificar_tamanhos.py --arvore HEAD    # tamanhos dos objetos de um commit (git ls-tree -l)
    python scripts/verificar_tamanhos.py --limite-mib 50 --aviso-mib 45 --top 15

Saída: resumo por pasta (edição / primeira subpasta) e os maiores arquivos. Código de saída 0 se
tudo estiver dentro do limite, 1 se algum arquivo passar, 2 se o Git não puder ser consultado.
Só biblioteca padrão. O arquivo vale também em Linux (CI) e em Windows.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

MIB = 1024 * 1024


def _git(raiz: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(raiz), *args], check=True, capture_output=True).stdout


def arquivos_do_disco(raiz: Path) -> list[tuple[str, int]]:
    """(caminho, bytes) de cada arquivo rastreado que existe no disco."""
    saida = _git(raiz, "ls-files", "-z")
    achados: list[tuple[str, int]] = []
    for bruto in saida.split(b"\0"):
        if not bruto:
            continue
        rel = bruto.decode("utf-8", "surrogateescape")
        caminho = raiz / rel
        if caminho.is_file() and not caminho.is_symlink():
            achados.append((rel, caminho.stat().st_size))
    return achados


def arquivos_da_arvore(raiz: Path, ref: str) -> list[tuple[str, int]]:
    """(caminho, bytes) de cada blob de um commit, sem precisar do arquivo no disco."""
    saida = _git(raiz, "ls-tree", "-r", "-l", "-z", ref)
    achados: list[tuple[str, int]] = []
    for bruto in saida.split(b"\0"):
        if not bruto:
            continue
        meta, _, caminho = bruto.partition(b"\t")
        partes = meta.split()
        if len(partes) >= 4 and partes[1] == b"blob":
            achados.append((caminho.decode("utf-8", "surrogateescape"), int(partes[3])))
    return achados


def pasta_do_resumo(rel: str) -> str:
    partes = rel.split("/")
    if len(partes) >= 3 and partes[0].startswith("triton_"):
        return f"{partes[0]}/{partes[1]}"
    if len(partes) >= 2:
        return partes[0]
    return "(raiz)"


def formatar(n: int) -> str:
    return f"{n / MIB:9.2f} MiB"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parents[1],
                    help="raiz do repositório (padrão: a pasta acima de scripts/)")
    ap.add_argument("--arvore", metavar="REF", help="usa os objetos do commit REF em vez do disco")
    ap.add_argument("--limite-mib", type=float, default=50.0, help="limite por arquivo (padrão 50)")
    ap.add_argument("--aviso-mib", type=float, default=45.0, help="a partir daqui, avisa (padrão 45)")
    ap.add_argument("--top", type=int, default=10, help="quantos arquivos maiores listar")
    a = ap.parse_args(argv)

    try:
        arquivos = arquivos_da_arvore(a.raiz, a.arvore) if a.arvore else arquivos_do_disco(a.raiz)
    except (OSError, subprocess.CalledProcessError) as erro:
        print(f"Não foi possível consultar o Git em {a.raiz}: {erro}", file=sys.stderr)
        return 2

    limite = int(a.limite_mib * MIB)
    aviso = int(a.aviso_mib * MIB)
    por_pasta: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for rel, tamanho in arquivos:
        acumulado = por_pasta[pasta_do_resumo(rel)]
        acumulado[0] += 1
        acumulado[1] += tamanho

    total = sum(t for _, t in arquivos)
    print(f"{len(arquivos)} arquivos rastreados, {formatar(total).strip()} no total "
          f"({'commit ' + a.arvore if a.arvore else 'disco'}); limite por arquivo {a.limite_mib:g} MiB.\n")
    print("Resumo por pasta (arquivos, tamanho):")
    for pasta, (n, tam) in sorted(por_pasta.items(), key=lambda kv: -kv[1][1]):
        print(f"  {pasta:<40s} {n:6d}  {formatar(tam)}")

    maiores = sorted(arquivos, key=lambda x: -x[1])[: a.top]
    print(f"\nOs {len(maiores)} maiores arquivos:")
    for rel, tamanho in maiores:
        marca = "ACIMA DO LIMITE" if tamanho > limite else ("perto do limite" if tamanho > aviso else "")
        print(f"  {formatar(tamanho)}  {rel}  {marca}".rstrip())

    acima = [(rel, t) for rel, t in arquivos if t > limite]
    perto = [(rel, t) for rel, t in arquivos if aviso < t <= limite]
    if perto:
        print(f"\nAviso: {len(perto)} arquivo(s) entre {a.aviso_mib:g} e {a.limite_mib:g} MiB.")
    if acima:
        print(f"\nFALHA: {len(acima)} arquivo(s) rastreado(s) passam de {a.limite_mib:g} MiB:", file=sys.stderr)
        for rel, tamanho in sorted(acima, key=lambda x: -x[1]):
            print(f"  {formatar(tamanho)}  {rel}", file=sys.stderr)
        print("Particione o arquivo (veja docs/DADOS.md da edição) ou tire-o do Git.", file=sys.stderr)
        return 1
    print(f"\nOK: nenhum arquivo rastreado passa de {a.limite_mib:g} MiB.")
    return 0


if __name__ == "__main__":
    if os.name == "nt":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
    sys.exit(main())
