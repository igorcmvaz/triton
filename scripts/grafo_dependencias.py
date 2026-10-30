# -*- coding: utf-8 -*-
"""Gera o grafo de dependências entre os módulos do Triton com o pydeps (ferramenta só de desenvolvimento).

Uso (da raiz do monorepo, com o extra ``grafo``: ``pip install "triton-int[grafo]"`` ou ``pip install pydeps``):

    python scripts/grafo_dependencias.py                          # as 3 edições, grafo de pacotes (.dot e, se houver Graphviz, .svg)
    python scripts/grafo_dependencias.py --edicao ibe             # só a Ibérica
    python scripts/grafo_dependencias.py --edicao int --modulo triton.core.estudo --modulo triton.cli
    python scripts/grafo_dependencias.py --edicao int --show-dot  # imprime o texto DOT, não grava nada

O núcleo ``triton/`` é idêntico nas 3 edições; as diferenças aparecem em ``main.py`` e nos módulos específicos
(por exemplo ``base_climatica_iberica``). A saída vai para ``docs/figuras/grafo_<edição>_<alvo>.dot|svg`` na raiz
do monorepo. O SVG exige o Graphviz (comando ``dot``); sem ele o script grava só o ``.dot`` e avisa, e o texto
DOT já serve para colar em qualquer visualizador. Nada disto entra no instalador. Só biblioteca padrão mais o pydeps.
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

RAIZ = Path(__file__).resolve().parents[1]
EDICOES = ("brl", "int", "ibe")


def _carregar_opcional(pasta: Path):
    """Carrega ``triton/core/_opcional.py`` da edição pelo caminho, sem importar o pacote ``triton`` inteiro."""
    caminho = pasta / "triton" / "core" / "_opcional.py"
    if not caminho.is_file():
        return None
    spec = importlib.util.spec_from_file_location("_opcional_do_triton", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def exigir_pydeps(pasta: Path) -> None:
    """Sai com a mensagem de instalação (do ``_opcional`` quando existe) se o pydeps não estiver instalado."""
    opc = _carregar_opcional(pasta)
    if opc is not None:
        if opc.disponivel("pydeps"):
            return
        sys.exit("erro: " + opc.mensagem_de_falta("pydeps", "grafo", "gerar o grafo de dependências"))
    if importlib.util.find_spec("pydeps") is None:
        sys.exit("erro: o pydeps não está instalado. Instale com: pip install pydeps")


def montar_comando(alvo: str, profundidade: int, somente: str, saida_svg: Optional[Path], mostrar_dot: bool) -> List[str]:
    """A linha de comando do pydeps. ``mostrar_dot`` pede o texto DOT em stdout, sem chamar o Graphviz."""
    cmd = [sys.executable, "-m", "pydeps", alvo, f"--max-module-depth={profundidade}", "--only", somente,
           "--noshow", "--no-config"]
    if mostrar_dot:
        cmd += ["--show-dot", "--no-output"]
    else:
        cmd += ["-T", "svg", "-o", str(saida_svg)]
    return cmd


def gerar_dot(pasta: Path, alvo: str, profundidade: int, somente: str) -> str:
    """O texto DOT do grafo de ``alvo`` (pacote ou módulo) visto a partir de ``pasta`` (a raiz da edição)."""
    cmd = montar_comando(alvo, profundidade, somente, None, True)
    r = subprocess.run(cmd, cwd=str(pasta), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or "digraph" not in r.stdout:
        raise RuntimeError(f"pydeps falhou para {alvo} em {pasta} (código {r.returncode}):\n{r.stderr.strip() or r.stdout.strip()}")
    return r.stdout[r.stdout.index("digraph"):]


def gerar_svg(pasta: Path, alvo: str, profundidade: int, somente: str, destino: Path) -> bool:
    """Grava o SVG com o Graphviz; devolve False (sem erro) se o comando ``dot`` não existe ou falha."""
    if shutil.which("dot") is None:
        return False
    r = subprocess.run(montar_comando(alvo, profundidade, somente, destino, False), cwd=str(pasta),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode == 0 and destino.is_file()


def nome_do_arquivo(edicao: str, alvo: str) -> str:
    return f"grafo_{edicao}_{'pacotes' if alvo == 'triton' else alvo.replace('.', '_')}"


def _argumentos(argv: Optional[List[str]]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="grafo_dependencias.py",
        description="Gera o grafo de dependências do Triton (pydeps, só desenvolvimento). Grava .dot sempre e .svg se o "
                    "Graphviz (comando 'dot') estiver instalado; --show-dot só imprime o texto DOT.")
    p.add_argument("--edicao", choices=EDICOES + ("todas",), default="todas", help="edição a analisar (padrão: todas)")
    p.add_argument("--pasta", type=Path, help="raiz de um pacote 'triton' qualquer (substitui --edicao; usado nos testes)")
    p.add_argument("--modulo", action="append", default=[], metavar="MODULO",
                   help="módulo-chave a desenhar, p. ex. triton.core.estudo (repetível); sem ele, o grafo de pacotes")
    p.add_argument("--profundidade", type=int, default=2, help="profundidade máxima dos módulos (padrão: 2; para --modulo use 1 a 3)")
    p.add_argument("--saida", type=Path, default=RAIZ / "docs" / "figuras", help="pasta de saída (padrão: docs/figuras)")
    p.add_argument("--show-dot", action="store_true", help="imprime o texto DOT em vez de gravar arquivos")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    a = _argumentos(argv)
    if a.pasta:
        pastas = [("pasta", a.pasta.resolve())]
    else:
        eds = EDICOES if a.edicao == "todas" else (a.edicao,)
        pastas = [(e, RAIZ / f"triton_{e}") for e in eds]
    alvos = a.modulo or ["triton"]
    for nome, pasta in pastas:
        if not (pasta / "triton").is_dir():
            sys.exit(f"erro: não encontrei o pacote 'triton' em {pasta}")
    exigir_pydeps(pastas[0][1])
    for nome, pasta in pastas:
        for alvo in alvos:
            prof = a.profundidade if alvo == "triton" else max(a.profundidade, 3)
            dot = gerar_dot(pasta, alvo, prof, "triton")
            if a.show_dot:
                print(dot)
                continue
            a.saida.mkdir(parents=True, exist_ok=True)
            base = a.saida / nome_do_arquivo(nome, alvo)
            base.with_suffix(".dot").write_text(dot, encoding="utf-8", newline="\n")
            print(f"gravado {base.with_suffix('.dot')}")
            if gerar_svg(pasta, alvo, prof, "triton", base.with_suffix(".svg")):
                print(f"gravado {base.with_suffix('.svg')}")
            else:
                print("aviso: o Graphviz ('dot') não está instalado ou falhou; gravei só o .dot "
                      "(use --show-dot para ver o texto, ou instale o Graphviz para o SVG)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
