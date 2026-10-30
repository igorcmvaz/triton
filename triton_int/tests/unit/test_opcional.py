# -*- coding: utf-8 -*-
"""``triton.core._opcional``: importação preguiçosa com mensagem clara e extras declarados no pyproject."""
import re
import sys
from pathlib import Path

import pytest

from triton.core import _opcional

RAIZ = Path(__file__).resolve().parents[2]


def test_importar_pacote_presente_devolve_o_modulo():
    assert _opcional.importar("json").dumps({}) == "{}"
    assert _opcional.disponivel("json") and not _opcional.disponivel("pacote_que_nao_existe_xyz")


def test_pacote_ausente_diz_pacote_extra_e_comando():
    with pytest.raises(_opcional.PacoteOpcionalAusente) as e:
        _opcional.importar("pacote_que_nao_existe_xyz", "analise", "consolidar estudos")
    texto = str(e.value)
    assert "pacote_que_nao_existe_xyz" in texto and "consolidar estudos" in texto
    assert re.search(r'pip install "triton-(brl|int|ibe)\[analise\]"', texto)
    assert isinstance(e.value, ImportError) and isinstance(e.value.__cause__, ImportError)


def test_extra_sai_do_nome_conhecido(monkeypatch):
    monkeypatch.setitem(sys.modules, "duckdb", None)          # simula o pacote ausente, instalado ou não
    with pytest.raises(_opcional.PacoteOpcionalAusente, match=r"\[analise\]"):
        _opcional.importar("duckdb")


def test_nao_importa_nada_ao_ser_carregado():
    import ast
    topo = [n for n in ast.parse((RAIZ / "triton" / "core" / "_opcional.py").read_text(encoding="utf-8")).body
            if isinstance(n, (ast.Import, ast.ImportFrom))]
    nomes = {a.name.split(".")[0] for n in topo for a in n.names} | {n.module.split(".")[0] for n in topo
                                                                     if isinstance(n, ast.ImportFrom)}
    assert not nomes & set(_opcional.EXTRA_DO_PACOTE)


def test_os_extras_do_pyproject_existem_e_o_requirements_nao_os_leva():
    texto = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    bloco = texto[texto.index("[project.optional-dependencies]"):texto.index("[project.scripts]")]
    for extra, pacote in (("docs", "mkdocs-material"), ("analise", "duckdb"), ("cli", "rich"),
                          ("otimizacao", "optuna"), ("grafo", "pydeps")):
        m = re.search(rf"^{extra}\s*=\s*\[(.*?)\]", bloco, re.S | re.M)
        assert m and pacote in m.group(1), extra
    assert set(_opcional.EXTRA_DO_PACOTE.values()) == {"docs", "analise", "cli", "otimizacao", "grafo"}
    req = (RAIZ / "requirements.txt").read_text(encoding="utf-8").lower()
    assert not any(p in req for p in ("mkdocs", "duckdb", "rich", "optuna", "pydeps"))
