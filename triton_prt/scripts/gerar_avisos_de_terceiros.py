"""
Gera ``infos_licenses/AVISOS_DE_TERCEIROS.txt``: as licenças do que vai dentro do programa.

O executável empacota o Python, o Qt (PySide6) e as bibliotecas de
``requirements.txt`` com as dependências delas. Licenças como MIT, BSD e Apache pedem
que o aviso de copyright acompanhe as cópias, e a LGPL do Qt pede o texto da licença e o
caminho do código-fonte. Este script reúne tudo num arquivo só, a partir dos metadados
dos pacotes **instalados no ambiente que compila** — por isso o ``build_exe.py`` o roda
antes de empacotar, e o arquivo sempre corresponde às versões que vão no pacote.

Uso
---
    python scripts/gerar_avisos_de_terceiros.py            # grava
    python scripts/gerar_avisos_de_terceiros.py --conferir # só confere a cobertura
"""

from __future__ import annotations

import argparse
import importlib.metadata as md
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "infos_licenses" / "AVISOS_DE_TERCEIROS.txt"
TEXTOS = RAIZ / "infos_licenses" / "textos"

#: Pacotes do Qt: as rodas não trazem o texto da licença, que fica em textos/.
_QT = {"pyside6", "pyside6-essentials", "pyside6-addons", "shiboken6"}
_ARQUIVO_DE_LICENCA = re.compile(r"(LICEN[CS]E|COPYING|NOTICE)", re.IGNORECASE)
_LINHA = "=" * 78


def _normalizar(nome: str) -> str:
    return re.sub(r"[-_.]+", "-", nome).lower()


def pacotes_de_producao() -> List[str]:
    nomes = []
    for linha in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines():
        linha = linha.split("#", 1)[0].strip()
        if linha:
            nomes.append(re.split(r"[ ;<>=!~\[(]", linha)[0])
    return nomes


def distribuicoes() -> Dict[str, md.Distribution]:
    """Os pacotes de produção e as dependências deles, sem extras, como instalados."""
    vistos: Dict[str, md.Distribution] = {}
    pilha = pacotes_de_producao()
    while pilha:
        nome = pilha.pop()
        try:
            dist = md.distribution(nome)
        except md.PackageNotFoundError:
            continue  # dependência condicional de outra plataforma (tzdata, tomli)
        chave = _normalizar(dist.metadata["Name"])
        if chave in vistos:
            continue
        vistos[chave] = dist
        for requisito in dist.requires or []:
            if "extra ==" not in requisito:
                pilha.append(re.split(r"[ ;<>=!~\[(]", requisito)[0])
    return dict(sorted(vistos.items()))


def _licenca(dist: md.Distribution) -> str:
    texto = dist.metadata.get("License-Expression") or ""
    if not texto:
        classificadores = [c.split("::")[-1].strip() for c in dist.metadata.get_all("Classifier") or []
                           if c.startswith("License ::")]
        texto = "; ".join(classificadores)
    if not texto:
        linhas = (dist.metadata.get("License") or "").strip().splitlines()
        texto = linhas[0] if linhas else ""
    return (texto or "ver o texto abaixo").strip()[:120]


def _textos_da_distribuicao(dist: md.Distribution) -> List[Tuple[str, str]]:
    textos = []
    for arquivo in dist.files or []:
        if _ARQUIVO_DE_LICENCA.search(str(arquivo).split("/")[-1]):
            try:
                textos.append((str(arquivo), Path(dist.locate_file(arquivo)).read_text(encoding="utf-8",
                                                                                      errors="replace")))
            except OSError:
                continue
    return textos


def montar() -> str:
    dists = distribuicoes()
    partes = [
        "TRITON 5 — AVISOS DE TERCEIROS",
        "",
        "O Triton é distribuído sob a GNU GPL v3 ou posterior (LICENSE.txt, na pasta do",
        "programa). O executável inclui os componentes abaixo, cada um sob a sua própria",
        "licença, reproduzida neste arquivo. Arquivo gerado por",
        "scripts/gerar_avisos_de_terceiros.py a partir dos pacotes empacotados.",
        "",
        "RESUMO",
        "",
        f"  {'Componente':32} {'Versão':14} Licença",
        f"  {'Python (interpretador embutido)':32} {sys.version.split()[0]:14} PSF-2.0",
    ]
    for chave, dist in dists.items():
        partes.append(f"  {dist.metadata['Name']:32} {dist.version:14} {_licenca(dist)}")
    partes += [
        f"  {'three.js':32} {'0.186.1':14} MIT",
        f"  {'Céu «Quarry» (Poly Haven)':32} {'1k HDR':14} CC0-1.0",
        f"  {'Base climática CLIMBra':32} {'2023':14} CC0-1.0",
        "",
    ]

    # Qt: LGPL v3, com o caminho do código-fonte e a possibilidade de substituição.
    partes += [
        _LINHA,
        "Qt for Python (PySide6, Shiboken6) e Qt — LGPL-3.0-only",
        _LINHA,
        "",
        "O Qt e o Qt for Python são usados sob a GNU Lesser General Public License v3.",
        "As bibliotecas do Qt vão como arquivos separados na pasta _internal do programa",
        "e podem ser substituídas por outra versão compatível. O código-fonte está em",
        "https://code.qt.io (qt/qtbase e demais módulos; pyside/pyside-setup) e em",
        "https://download.qt.io/official_releases/. A LGPL v3 complementa a GPL v3, cujo",
        "texto está em LICENSE.txt.",
        "",
        (TEXTOS / "LGPL-3.0.txt").read_text(encoding="utf-8"),
        _LINHA,
        "Python — Python Software Foundation License",
        _LINHA,
        "",
        (TEXTOS / "PSF-Python.txt").read_text(encoding="utf-8"),
    ]
    for chave, dist in dists.items():
        if chave in _QT:
            continue
        partes += [_LINHA, f"{dist.metadata['Name']} {dist.version} — {_licenca(dist)}", _LINHA, ""]
        textos = _textos_da_distribuicao(dist)
        if not textos:
            partes.append(f"(o pacote não traz arquivo de licença; licença declarada: {_licenca(dist)})\n")
        for nome, texto in textos:
            partes += [f"--- {nome} ---", texto.rstrip(), ""]
    partes += [
        _LINHA,
        "Visualizador 3D: three.js (MIT) e céu «Quarry» do Poly Haven (CC0-1.0)",
        _LINHA,
        "",
        (RAIZ / "triton" / "data" / "volumetria" / "LICENCAS.md").read_text(encoding="utf-8"),
        _LINHA,
        "Base climática CLIMBra — CC0 1.0 Universal (domínio público)",
        _LINHA,
        "",
        "Ballarin, A. S. et al. (2023). CLIMBra — Climate Change Dataset for Brazil.",
        "Scientific Data 10, 47. doi:10.1038/s41597-023-01956-z. Dados no Science Data",
        "Bank, doi:10.57760/sciencedb.02316, sob CC0 1.0 Universal. O Triton os compila em",
        "data/climbra.db sem alterar os valores além da compactação.",
        "",
    ]
    return "\n".join(partes)


def faltando() -> List[str]:
    """Pacotes de produção que não aparecem no arquivo gravado."""
    texto = SAIDA.read_text(encoding="utf-8") if SAIDA.is_file() else ""
    return [p for p in pacotes_de_producao() if p.lower() not in texto.lower()]


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("--conferir", action="store_true")
    args = analisador.parse_args()
    if args.conferir:
        ausentes = faltando()
        print("faltam: " + ", ".join(ausentes) if ausentes else "todos os pacotes de produção constam")
        return 1 if ausentes else 0
    SAIDA.write_text(montar(), encoding="utf-8")
    print(f"gravado: {SAIDA.relative_to(RAIZ).as_posix()} ({len(distribuicoes())} pacotes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
