"""Varredura: literal com o nome do programa que não passa pelo ponto de passagem da marca.

O nome que o usuário vê sai de ``triton/marca.py``: ``tr`` (interface), ``cli_textos.t`` (``_t`` e
``_m``, linha de comando), ``marca.aplicar`` ou ``marca.NOME``. Este teste percorre o pacote com
``ast`` e lista os literais de texto com a palavra «Triton»/«TRITON» que não estão dentro de uma
chamada a ``tr``/``_t``/``_m``/``aplicar`` nem nos catálogos de tradução. Cada um tem de estar em
``test_marca_varredura_excecoes.txt``, com o motivo (chave de tradução, identificador, texto que
passa por ``aplicar`` mais adiante...). Docstrings e comentários não contam.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EXCECOES = Path(__file__).with_name("test_marca_varredura_excecoes.txt")

#: A palavra, como ``marca.aplicar`` a procura (só a palavra inteira; ``triton`` minúsculo é do pacote).
_NOME = re.compile(r"\bTriton\b|\bTRITON\b")
#: Chamadas que já entregam o texto com ``marca.NOME``.
_PASSAGEM = {"tr", "_t", "_m", "aplicar"}
#: Catálogos: os literais dos dicionários deles saem por ``tr``/``t``; ``marca.py`` é a fonte.
_CATALOGOS = {
    "triton/ui/translation.py", "triton/ui/translation_complement.py",
    "triton/ui/translation_neutralidade.py", "triton/cli_textos.py", "triton/marca.py",
}


def _nome_da_chamada(func) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def trecho(texto: str) -> str:
    """A identificação de um literal: o texto em volta da primeira ocorrência, sem quebras."""
    m = _NOME.search(texto)
    return " ".join(texto[max(0, m.start() - 30):m.end() + 30].split())


def literais_fora_da_passagem():
    """Pares (caminho, trecho) de cada literal com o nome que não passa pelo ponto de passagem."""
    achados = set()
    for arquivo in sorted((RAIZ / "triton").rglob("*.py")) + [RAIZ / "main.py"]:
        rel = arquivo.relative_to(RAIZ).as_posix()
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        pais = {filho: no for no in ast.walk(arvore) for filho in ast.iter_child_nodes(no)}
        docstrings = {
            no.body[0].value for no in ast.walk(arvore)
            if isinstance(no, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            and no.body and isinstance(no.body[0], ast.Expr) and isinstance(no.body[0].value, ast.Constant)
        }
        for no in ast.walk(arvore):
            if not (isinstance(no, ast.Constant) and isinstance(no.value, str)) or no in docstrings:
                continue
            if not _NOME.search(no.value):
                continue
            acima, coberto = no, False
            while acima in pais and not coberto:
                acima = pais[acima]
                coberto = ((isinstance(acima, ast.Call) and _nome_da_chamada(acima.func) in _PASSAGEM)
                           or (rel in _CATALOGOS and isinstance(acima, (ast.Dict, ast.Assign))))
            if not coberto:
                achados.add((rel, trecho(no.value)))
    return achados


def excecoes():
    """As exceções justificadas: linhas ``caminho :: trecho`` (comentários com ``#`` dão o motivo)."""
    pares = set()
    for linha in EXCECOES.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            caminho, _, texto = linha.partition(" :: ")
            pares.add((caminho.strip(), texto.strip()))
    return pares


def test_todo_literal_com_o_nome_passa_pela_marca_ou_esta_nas_excecoes():
    novos = sorted(literais_fora_da_passagem() - excecoes())
    assert not novos, (
        "Literal com o nome do programa fora do ponto de passagem da marca:\n"
        + "\n".join(f"  {c} :: {t}" for c, t in novos)
        + "\n\nSe o usuário vê esse texto, monte-o com marca.NOME (f-string) ou envolva-o em "
          "marca.aplicar(...) (ou tr(...) se for rótulo da interface). Se não vê (identificador, "
          "nome de arquivo, chave de tradução que sai por tr/aplicar adiante), copie a linha acima "
          f"para {EXCECOES.name}, na seção do motivo.")


def test_o_arquivo_de_excecoes_tem_motivo_e_formato():
    secoes = 0
    for linha in EXCECOES.read_text(encoding="utf-8").splitlines():
        if linha.startswith("# ==") and len(linha.strip("#= ")) > 10:
            secoes += 1
        elif linha.strip() and not linha.startswith("#"):
            assert " :: " in linha, f"linha sem «caminho :: trecho»: {linha!r}"
            assert secoes, f"exceção antes de qualquer seção com motivo: {linha!r}"
