"""Central do nome (triton/marca.py) e aceitação das extensões .triton e .netuno."""
from __future__ import annotations

import shutil
from pathlib import Path

from triton import marca
from triton.cli import _discover_project_files


def test_marca_tem_nome_e_extensoes():
    assert marca.NOME and marca.DOI.startswith("10.5281/zenodo.")
    assert ".triton" in marca.EXTENSOES_PROJETO and ".netuno" in marca.EXTENSOES_PROJETO
    assert marca.EXTENSAO_PROJETO in marca.EXTENSOES_PROJETO


def test_eh_projeto_ignora_maiusculas_e_nao_confunde_json():
    assert marca.eh_projeto("a/b.NETUNO") and marca.eh_projeto("x.triton")
    assert not marca.eh_projeto("x.json") and marca.eh_entrada("x.json")
    assert "*.netuno" in marca.filtro_qt()


def test_pasta_com_triton_e_netuno_lista_os_dois(tmp_path: Path):
    (tmp_path / "a.triton").write_text("{}", encoding="utf-8")
    (tmp_path / "b.netuno").write_text("{}", encoding="utf-8")
    (tmp_path / "c.txt").write_text("x", encoding="utf-8")
    nomes = sorted(p.name for p in _discover_project_files([str(tmp_path)], False))
    assert nomes == ["a.triton", "b.netuno"]


def test_projeto_netuno_abre_como_o_triton(tmp_path: Path):
    from triton.core.system.parser import load_triton_project

    exemplo = next(Path(__file__).resolve().parents[2].glob("examples/*.triton"))
    copia = tmp_path / "projeto.netuno"
    shutil.copyfile(exemplo, copia)
    original = load_triton_project(str(exemplo))
    novo = load_triton_project(str(copia))
    assert novo["is_json"] is True
    assert novo["config"].__dict__.keys() == original["config"].__dict__.keys()
