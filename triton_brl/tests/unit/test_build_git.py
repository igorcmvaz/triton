"""O build compila o código atual e não deixa a pasta suja para o próximo git pull."""

import shutil
import subprocess
from pathlib import Path

import pytest

import build_exe

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git ausente")


def _git(pasta: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=pasta, check=True, capture_output=True, text=True).stdout


def _repositorio(pasta: Path) -> Path:
    pasta.mkdir()
    _git(pasta, "init", "-q", "-b", "main")
    _git(pasta, "config", "user.email", "t@t")
    _git(pasta, "config", "user.name", "t")
    (pasta / "manual.md").write_text("v1\n", encoding="utf-8")
    (pasta / "codigo.py").write_text("x = 1\n", encoding="utf-8")
    _git(pasta, "add", ".")
    _git(pasta, "commit", "-q", "-m", "c1")
    return pasta


def test_a_pasta_atras_do_origin_main_e_recusada(tmp_path):
    origem = _repositorio(tmp_path / "origem")
    _git(tmp_path, "clone", "-q", str(origem), "copia")
    copia = tmp_path / "copia"
    assert build_exe.conferir_a_pasta(copia) is True
    (origem / "codigo.py").write_text("x = 2\n", encoding="utf-8")
    _git(origem, "commit", "-qam", "c2")
    assert build_exe.conferir_a_pasta(copia) is False      # o pull não aconteceu
    assert build_exe.conferir_a_pasta(copia, ignorar=True) is True


def test_so_o_que_o_build_alterou_e_restaurado(tmp_path):
    pasta = _repositorio(tmp_path / "repo")
    (pasta / "codigo.py").write_text("x = 99\n", encoding="utf-8")   # alteração do usuário
    limpos = build_exe.arquivos_versionados_limpos(pasta)
    assert "manual.md" in limpos and "codigo.py" not in limpos
    (pasta / "manual.md").write_text("regerado\n", encoding="utf-8")  # o build regera o manual
    build_exe.restaurar_gerados(pasta, limpos)
    assert (pasta / "manual.md").read_text(encoding="utf-8") == "v1\n"
    assert (pasta / "codigo.py").read_text(encoding="utf-8") == "x = 99\n"


def test_o_spec_gerado_nao_sobrescreve_o_da_raiz():
    texto = Path(build_exe.__file__).read_text(encoding="utf-8")
    assert "--specpath=" in texto
