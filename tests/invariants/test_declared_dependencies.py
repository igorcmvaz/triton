"""
Invariante de empacotamento: tudo que o pacote importa deve estar declarado.

Motivação
---------
A versão 5.0.0 foi auditada e três dependências de terceiros eram importadas sem
constar de `pyproject.toml`: `requests` e `beautifulsoup4` (atualizador tarifário) e
`pyarrow` (exportação parquet da CLI em lote). Uma instalação limpa via
`pip install -e .` funcionava até o usuário tocar nesses caminhos, e então falhava
com `ModuleNotFoundError`.

O caso do `numba` é da mesma família, com agravante: por não estar declarado, ele
trocava silenciosamente o kernel de cálculo conforme estivesse ou não presente na
máquina (ver `test_numba_python_parity.py`).

Este teste fecha a classe inteira: qualquer importação de terceiros introduzida no
pacote sem a declaração correspondente reprova a suíte.
"""

import ast
import sys
import tomllib
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
PACOTE = RAIZ / "netuno"
PYPROJECT = RAIZ / "pyproject.toml"

# O nome importado nem sempre é o nome da distribuição no PyPI.
NOME_DA_DISTRIBUICAO = {
    "bs4": "beautifulsoup4",
    "PIL": "pillow",
    "yaml": "pyyaml",
    "dateutil": "python-dateutil",
    "fitz": "pymupdf",
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
}

# Módulos internos ao próprio projeto.
INTERNOS = {"netuno", "main"}


def _modulos_de_terceiros_importados() -> dict[str, set[str]]:
    """Mapeia cada módulo de terceiros aos arquivos do pacote que o importam."""
    encontrados: dict[str, set[str]] = {}
    for arquivo in sorted(PACOTE.rglob("*.py")):
        try:
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):  # pragma: no cover - arquivo inválido
            continue

        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                nomes = [alias.name for alias in no.names]
            elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
                nomes = [no.module]
            else:
                continue

            for nome in nomes:
                raiz = nome.split(".")[0]
                if raiz in sys.stdlib_module_names or raiz in INTERNOS:
                    continue
                caminho = arquivo.relative_to(RAIZ).as_posix()
                encontrados.setdefault(raiz, set()).add(caminho)
    return encontrados


def _distribuicoes_declaradas() -> set[str]:
    """Todas as distribuições declaradas, obrigatórias e opcionais."""
    dados = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    projeto = dados["project"]

    especificacoes = list(projeto.get("dependencies", []))
    for grupo in projeto.get("optional-dependencies", {}).values():
        especificacoes.extend(grupo)

    declaradas = set()
    for especificacao in especificacoes:
        # "pacote[extra]>=1.2" -> "pacote"
        nome = especificacao.split(";")[0]
        for separador in (">", "<", "=", "!", "~", "["):
            nome = nome.split(separador)[0]
        declaradas.add(nome.strip().lower())
    return declaradas


def test_todo_import_de_terceiros_esta_declarado():
    """Nenhum módulo de terceiros pode ser importado sem constar de pyproject.toml."""
    declaradas = _distribuicoes_declaradas()
    nao_declaradas = []

    for modulo, arquivos in sorted(_modulos_de_terceiros_importados().items()):
        distribuicao = NOME_DA_DISTRIBUICAO.get(modulo, modulo).lower()
        if distribuicao not in declaradas and modulo.lower() not in declaradas:
            nao_declaradas.append(f"{distribuicao} (importado como '{modulo}') "
                                  f"em {', '.join(sorted(arquivos)[:3])}")

    assert not nao_declaradas, (
        "dependências de terceiros importadas mas não declaradas em pyproject.toml:\n  "
        + "\n  ".join(nao_declaradas)
    )


def test_requirements_acompanha_as_dependencias_obrigatorias():
    """requirements.txt não pode divergir das dependências obrigatórias do pyproject.

    Os dois arquivos são mantidos à mão; sem esta verificação, um instalado por
    `pip install -r requirements.txt` pode receber um conjunto diferente do de quem
    instala por `pip install -e .`.
    """
    dados = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))

    def normalizar(especificacoes):
        nomes = set()
        for especificacao in especificacoes:
            nome = especificacao.split(";")[0]
            for separador in (">", "<", "=", "!", "~", "["):
                nome = nome.split(separador)[0]
            nomes.add(nome.strip().lower())
        return nomes

    do_pyproject = normalizar(dados["project"]["dependencies"])

    linhas = [
        linha.strip()
        for linha in (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if linha.strip() and not linha.strip().startswith("#")
    ]
    do_requirements = normalizar(linhas)

    assert do_pyproject == do_requirements, (
        "pyproject.toml e requirements.txt divergem.\n"
        f"  só em pyproject.toml : {sorted(do_pyproject - do_requirements) or '—'}\n"
        f"  só em requirements.txt: {sorted(do_requirements - do_pyproject) or '—'}"
    )


@pytest.mark.parametrize("modulo_obrigatorio", ["numpy", "pandas"])
def test_dependencias_essenciais_estao_presentes(modulo_obrigatorio):
    """Guarda de sanidade do próprio ambiente de teste."""
    pytest.importorskip(modulo_obrigatorio)
