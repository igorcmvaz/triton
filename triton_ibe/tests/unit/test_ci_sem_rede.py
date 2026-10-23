"""Os testes de rede (ANEEL) rodam só quando pedidos, nunca no CI de push e PR.

O ``addopts`` do pyproject.toml já deseleciona ``rede``, mas um ``-m`` explícito na
linha de comando **substitui** o do addopts. O workflow chamava
``pytest -m "not replicacao"`` e, com isso, baixava ~90 MB da ANEEL a cada push —
e uma conexão cortada no meio derrubou o CI do main.

O workflow fica na raiz do repositório (uma pasta acima da edição). Num clone que
traga só a pasta da edição ele não existe, e os testes que o leem são pulados.
"""

import re
from pathlib import Path

import pytest

EDICAO = Path(__file__).resolve().parents[2]
WORKFLOW = EDICAO.parent / ".github" / "workflows" / "verificacao.yml"

pytestmark = pytest.mark.skipif(not WORKFLOW.is_file(), reason="workflow do GitHub ausente neste clone")


def _chamadas_do_pytest():
    return re.findall(r"python -m pytest[^\n]*", WORKFLOW.read_text(encoding="utf-8"))


def test_toda_selecao_explicita_do_ci_exclui_a_rede():
    for chamada in _chamadas_do_pytest():
        argumentos = chamada.split("pytest", 1)[1]
        selecao = re.search(r'-m\s+"([^"]+)"|-m\s+(\S+)', argumentos)
        if selecao is None:
            continue  # sem -m, vale o addopts, que já exclui a rede
        expressao = selecao.group(1) or selecao.group(2)
        if expressao == "rede":
            continue  # o job sob demanda
        assert "not rede" in expressao or expressao == "replicacao", chamada


def test_o_job_de_rede_so_roda_quando_disparado_a_mao():
    texto = WORKFLOW.read_text(encoding="utf-8")
    if "\n  rede:" not in texto:
        pytest.skip("o workflow não tem job de rede")
    job = texto[texto.index("\n  rede:"):]
    assert "if: github.event_name == 'workflow_dispatch'" in job
    assert "pytest -m rede" in job


def test_o_addopts_exclui_a_rede():
    pyproject = (EDICAO / "pyproject.toml").read_text(encoding="utf-8")
    assert "not rede" in re.search(r'addopts\s*=\s*"([^"]+)"', pyproject).group(1)
