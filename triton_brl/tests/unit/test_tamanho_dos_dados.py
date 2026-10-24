# -*- coding: utf-8 -*-
"""Tamanho dos dados versionados e documento de dados da edição.

O projeto não deixa nenhum arquivo rastreado passar de 50 MiB (o GitHub avisa em 50 e recusa em 100).
O mesmo teste vale nas três edições: confere os arquivos rastreados da pasta da edição, o limite
declarado no manifesto das partes da base climática (só a edição que o traz) e a existência do
`docs/DADOS.md`, ligado no README. O conjunto do repositório é conferido por `scripts/verificar_tamanhos.py`
(raiz), que a CI roda.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
LIMITE = 50 * 1024 * 1024


def _rastreados() -> list[Path]:
    try:
        saida = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, check=True, capture_output=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("pasta fora de um repositório Git (ou Git ausente)")
    arquivos = [RAIZ / b.decode("utf-8", "surrogateescape") for b in saida.split(b"\0") if b]
    if not arquivos:
        pytest.skip("nenhum arquivo rastreado nesta pasta")
    return arquivos


def test_nenhum_arquivo_rastreado_passa_de_50_mib():
    grandes = [(p.relative_to(RAIZ).as_posix(), p.stat().st_size) for p in _rastreados()
               if p.is_file() and p.stat().st_size > LIMITE]
    assert not grandes, f"arquivos rastreados acima de 50 MiB: {grandes}"


def test_manifesto_das_partes_declara_o_limite_do_projeto():
    manifesto = RAIZ / "data" / "climbra_partes.json"
    if not manifesto.is_file():
        pytest.skip("esta edição não traz a base climática em partes")
    dados = json.loads(manifesto.read_text(encoding="utf-8"))
    assert dados["limite_github_mb"] == 50
    for parte in dados["partes"]:
        arquivo = manifesto.parent / parte["arquivo"]
        if arquivo.is_file():
            assert arquivo.stat().st_size <= LIMITE, f"{arquivo.name} passa de 50 MiB"


def test_documento_de_dados_existe_e_o_readme_o_cita():
    doc = RAIZ / "docs" / "DADOS.md"
    assert doc.is_file() and doc.stat().st_size > 2000, "docs/DADOS.md ausente ou vazio"
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    assert "docs/DADOS.md" in readme, "o README não liga docs/DADOS.md"
