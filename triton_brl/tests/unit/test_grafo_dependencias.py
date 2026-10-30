# -*- coding: utf-8 -*-
"""``scripts/grafo_dependencias.py`` (raiz do monorepo): --help sempre; o grafo de um pacote mínimo só com o pydeps."""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "grafo_dependencias.py"
pytestmark = pytest.mark.skipif(not SCRIPT.is_file(), reason="o script fica na raiz do monorepo, fora da edição")


def _rodar(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=cwd)


def test_help_lista_as_opcoes():
    r = _rodar("--help")
    assert r.returncode == 0
    for opcao in ("--edicao", "--modulo", "--profundidade", "--saida", "--show-dot", "--pasta"):
        assert opcao in r.stdout


@pytest.mark.skipif(importlib.util.find_spec("pydeps") is None, reason="extra «grafo» (pydeps) não instalado")
def test_show_dot_de_um_pacote_minimo_tem_nos_e_arestas(tmp_path):
    pacote = tmp_path / "triton"
    (pacote / "core").mkdir(parents=True)
    (pacote / "ui").mkdir()
    for p in (pacote, pacote / "core", pacote / "ui"):
        (p / "__init__.py").write_text("", encoding="utf-8")
    (pacote / "core" / "motor.py").write_text("X = 1\n", encoding="utf-8")
    (pacote / "ui" / "tela.py").write_text("from triton.core import motor\n", encoding="utf-8")
    r = _rodar("--pasta", str(tmp_path), "--show-dot")
    assert r.returncode == 0, r.stderr
    assert "digraph" in r.stdout and "triton_ui" in r.stdout and "triton_core" in r.stdout
    assert "triton_core -> triton_ui" in r.stdout and "triton_ui -> triton_core" not in r.stdout   # seta: do importado para quem importa
    assert not list(tmp_path.glob("**/*.dot")) and not list(tmp_path.glob("**/*.svg"))   # --show-dot não grava


def test_sem_o_pacote_triton_diz_onde_procurou(tmp_path):
    r = _rodar("--pasta", str(tmp_path), "--show-dot")
    assert r.returncode != 0 and "triton" in r.stderr
