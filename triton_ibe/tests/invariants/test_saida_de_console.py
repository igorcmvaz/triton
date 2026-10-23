"""
Compatibilidade da saída de console com a codificação padrão do Windows.

O console do Windows em português usa cp1252 por padrão. Um `print()` que contenha
caractere fora dessa codificação levanta `UnicodeEncodeError` e **derruba o script no
meio da execução** — não é um problema estético.

O defeito ocorreu três vezes neste projeto antes de ser tratado como classe:

- `scripts/qa_runner.py` abortava ao imprimir ``>=`` como sinal matemático;
- `tests/benchmarking/compare_netuno4_triton.py` rodava a comparação inteira dos
  2.592 casos e falhava na última linha, ao imprimir um emoji;
- `tests/benchmarking/decomposicao_divergencia.py` repetiu o padrão com ``<=``.

Este teste varre, por análise sintática, as strings que efetivamente chegam a `print()`
nos módulos executáveis do projeto. Docstrings, comentários e strings de exceção não são
verificados: só o que vai para a saída padrão.

Escrever ``>=`` em vez de ``≥`` na saída de console é uma restrição pequena; a
documentação em Markdown segue livre para usar a tipografia correta.
"""

import ast
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]

#: Diretórios cujos módulos são executados diretamente pelo usuário no terminal.
DIRETORIOS_DE_CONSOLE = ["scripts", "tests/benchmarking"]

#: Arquivos na raiz que também são pontos de entrada de linha de comando.
ARQUIVOS_DE_CONSOLE_NA_RAIZ = ["build_exe.py", "main.py"]


def _modulos_de_console():
    for diretorio in DIRETORIOS_DE_CONSOLE:
        caminho = RAIZ / diretorio
        if caminho.is_dir():
            yield from sorted(caminho.rglob("*.py"))
    for nome in ARQUIVOS_DE_CONSOLE_NA_RAIZ:
        if (RAIZ / nome).is_file():
            yield RAIZ / nome


def _textos_impressos(arvore: ast.AST):
    """Devolve (linha, texto) de cada literal que chega a um `print()`.

    Cobre tanto strings simples quanto as partes literais de f-strings, que são onde
    os símbolos costumam ser escritos.
    """
    for no in ast.walk(arvore):
        if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                and no.func.id == "print"):
            continue

        for argumento in no.args:
            for parte in ast.walk(argumento):
                if isinstance(parte, ast.Constant) and isinstance(parte.value, str):
                    yield getattr(parte, "lineno", no.lineno), parte.value


def _fora_do_cp1252(texto: str):
    incompativeis = []
    for caractere in texto:
        try:
            caractere.encode("cp1252")
        except UnicodeEncodeError:
            incompativeis.append(f"U+{ord(caractere):04X}")
    return incompativeis


@pytest.mark.parametrize(
    "modulo", list(_modulos_de_console()), ids=lambda p: p.relative_to(RAIZ).as_posix()
)
def test_saida_de_console_sobrevive_ao_cp1252(modulo):
    """Nenhuma string impressa pode conter caractere fora do cp1252."""
    try:
        arvore = ast.parse(modulo.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError) as erro:  # pragma: no cover
        pytest.skip(f"não foi possível analisar {modulo.name}: {erro}")

    problemas = [
        f"linha {linha}: {codepoints} em {texto.strip()[:60]!r}"
        for linha, texto in _textos_impressos(arvore)
        if (codepoints := _fora_do_cp1252(texto))
    ]

    assert not problemas, (
        f"{modulo.relative_to(RAIZ).as_posix()} imprime caracteres que o console padrão "
        "do Windows (cp1252) não codifica, o que aborta a execução:\n  "
        + "\n  ".join(problemas)
        + "\nUse equivalentes ASCII na saída de console (>=, <=, -, ->)."
    )
