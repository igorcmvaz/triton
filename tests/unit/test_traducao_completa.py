"""Todo texto que a interface passa por tr() tem tradução nos três idiomas.

Em 18/09/2026 a varredura achou 1.117 textos sem inglês, espanhol ou chinês, e
outros 75 que nem passavam por tr(). Este teste lê as chamadas tr("...") de todo
o pacote e falha se uma delas voltar ao idioma-fonte.
"""
import ast
import os
import re

import pytest

from netuno.ui import translation as T

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _chaves():
    chaves = {}
    for raiz, _, arquivos in os.walk(os.path.join(RAIZ, "netuno")):
        if "__pycache__" in raiz:
            continue
        for nome in arquivos:
            if not nome.endswith(".py") or nome.startswith("translation"):
                continue
            caminho = os.path.join(raiz, nome)
            arvore = ast.parse(open(caminho, encoding="utf-8").read())
            for no in ast.walk(arvore):
                if (isinstance(no, ast.Call)
                        and getattr(no.func, "id", getattr(no.func, "attr", None)) == "tr"
                        and no.args and isinstance(no.args[0], ast.Constant)
                        and isinstance(no.args[0].value, str)
                        and any(c.isalpha() for c in no.args[0].value)):
                    chaves.setdefault(no.args[0].value, os.path.relpath(caminho, RAIZ))
    return chaves


CHAVES = _chaves()


def test_a_varredura_acha_as_chamadas():
    assert len(CHAVES) > 1000


@pytest.mark.parametrize("lang", ["en", "es", "zh"])
def test_nenhum_texto_fica_sem_traducao(lang):
    faltam = []
    for chave, arquivo in CHAVES.items():
        if lang == "en":
            ok = chave in T._DICTIONARY
        else:
            catalogo = T._SPANISH_DICTIONARY if lang == "es" else T._CHINESE_DICTIONARY
            ok = chave in catalogo or T.tr(chave, lang) != T._DICTIONARY.get(chave, chave)
        if not ok:
            faltam.append((arquivo, chave[:60]))
    assert not faltam, faltam[:10]


def test_as_traducoes_preservam_os_marcadores():
    """Um {0} ou {mass} perdido na tradução quebra o .format() da tela."""
    marcador = re.compile(r"\{[^{}]*\}")
    ruins = []
    for chave in CHAVES:
        esperado = sorted(marcador.findall(chave))
        if not esperado:
            continue
        for lang in ("en", "es", "zh"):
            if sorted(marcador.findall(T.tr(chave, lang))) != esperado:
                ruins.append((lang, chave[:60]))
    assert not ruins, ruins[:10]
