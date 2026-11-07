# -*- coding: utf-8 -*-
"""``mkdocs.yml`` da raiz do monorepo: YAML válido, todo arquivo do ``nav`` existe e o site fica fora do instalador.

Não precisa do pacote ``mkdocs``: o YAML é lido com PyYAML (a marca ``!!python/name`` do superfences é ignorada) e os
arquivos são conferidos no disco. O arquivo fica na raiz do monorepo, fora das edições, por isso o teste é pulado se
a edição estiver isolada do restante.
"""
import importlib.util
import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

RAIZ_EDICAO = Path(__file__).resolve().parents[2]
RAIZ = RAIZ_EDICAO.parent
MKDOCS = RAIZ / "mkdocs.yml"
pytestmark = pytest.mark.skipif(not MKDOCS.is_file(), reason="mkdocs.yml fica na raiz do monorepo, fora da edição")


class _Leitor(yaml.SafeLoader):
    pass


_Leitor.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, sufixo, no: sufixo)


def _config():
    return yaml.load(MKDOCS.read_text(encoding="utf-8"), Loader=_Leitor)


def _arquivos_do_nav(no):
    if isinstance(no, str):
        yield no
    elif isinstance(no, list):
        for item in no:
            yield from _arquivos_do_nav(item)
    elif isinstance(no, dict):
        for valor in no.values():
            yield from _arquivos_do_nav(valor)


def _hooks():
    caminho = RAIZ / "scripts" / "mkdocs_hooks.py"
    spec = importlib.util.spec_from_file_location("mkdocs_hooks_do_triton", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_yaml_valido_com_mermaid_e_mathjax():
    cfg = _config()
    assert cfg["docs_dir"] == "docs" and cfg["theme"]["name"] == "material"
    texto = MKDOCS.read_text(encoding="utf-8")
    assert "name: mermaid" in texto and "pymdownx.arithmatex" in texto
    assert (RAIZ / "docs" / "javascripts" / "mathjax.js").is_file()
    assert "deploy" not in {k.lower() for k in cfg}          # sem deploy nem GitHub Pages
    assert not (RAIZ / ".github").exists() or not list((RAIZ / ".github").rglob("*mkdocs*"))


def test_todo_arquivo_do_nav_existe_em_docs_ou_e_um_original_declarado():
    cfg = _config()
    externos = _hooks().mapa_de_externos(RAIZ, cfg["extra"])
    docs = RAIZ / cfg["docs_dir"]
    arquivos = list(_arquivos_do_nav(cfg["nav"]))
    assert len(arquivos) >= 8 and len(set(arquivos)) == len(arquivos)
    assert "grafo_de_dependencias.md" in arquivos            # o grafo de dependências está na navegação
    faltam = [a for a in arquivos if not (docs / a).is_file() and not (a in externos and externos[a].is_file())]
    assert not faltam, f"arquivos do nav que não existem: {faltam}"


def test_originais_externos_ficam_dentro_do_monorepo_e_nao_colidem_com_docs():
    cfg = _config()
    externos = _hooks().mapa_de_externos(RAIZ, cfg["extra"])
    assert externos
    for destino, origem in externos.items():
        assert RAIZ.resolve() in origem.parents, destino
        assert not (RAIZ / cfg["docs_dir"] / destino).exists(), f"{destino} existe também em docs/"


def test_versao_do_material_fixada_e_fora_do_requirements():
    reqs = (RAIZ / "requirements-docs.txt").read_text(encoding="utf-8")
    assert re.search(r"^mkdocs-material==\d+\.\d+\.\d+", reqs, re.M) and re.search(r"^mkdocs<2", reqs, re.M)
    pyproject = (RAIZ_EDICAO / "pyproject.toml").read_text(encoding="utf-8")
    assert "mkdocs-material==" in pyproject
    for nome in ("requirements.txt",):
        assert "mkdocs" not in (RAIZ_EDICAO / nome).read_text(encoding="utf-8").lower()


def test_site_gerado_vai_para_o_gitignore_e_nada_do_mkdocs_no_empacotamento():
    assert re.search(r"^/site/\s*$", (RAIZ / ".gitignore").read_text(encoding="utf-8"), re.M)
    for nome in ("Triton.spec", "build_exe.py"):
        if not (RAIZ_EDICAO / nome).is_file():
            continue  # o empacotamento não vai ao Git (só o necessário para a linha de comando)
        assert "mkdocs" not in (RAIZ_EDICAO / nome).read_text(encoding="utf-8").lower(), nome


@pytest.mark.skipif(importlib.util.find_spec("mkdocs") is None, reason="extra «docs» (mkdocs) não instalado")
def test_mkdocs_build_gera_o_site(tmp_path):
    import subprocess
    import sys
    r = subprocess.run([sys.executable, "-m", "mkdocs", "build", "-q", "-d", str(tmp_path / "site")], cwd=str(RAIZ),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "site" / "index.html").is_file()
