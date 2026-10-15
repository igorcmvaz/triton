# -*- coding: utf-8 -*-
"""O mapa das edições (docs/edicoes.md e docs/en/editions.md) acompanha o código.

Todo arquivo que pergunta pela edição antes de oferecer um dado brasileiro tem de
constar da tabela «Onde está no código», nas duas línguas; um arquivo que deixa de
perguntar sai dela.
"""

import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERGUNTA = re.compile(r"\b(usa_dados_do_brasil|usa_dados_de_portugal|is_int_edition|is_brl_edition|is_prt_edition)\(\)")
MAPAS = (os.path.join(RAIZ, "docs", "edicoes.md"), os.path.join(RAIZ, "docs", "en", "editions.md"))


def _arquivos_que_perguntam():
    achados = set()
    for raiz, _, nomes in os.walk(os.path.join(RAIZ, "triton")):
        for nome in nomes:
            if not nome.endswith(".py"):
                continue
            caminho = os.path.join(raiz, nome)
            if PERGUNTA.search(open(caminho, encoding="utf-8").read()):
                achados.add(os.path.relpath(caminho, RAIZ).replace(os.sep, "/"))
    return achados


def _arquivos_do_mapa(caminho):
    texto = open(caminho, encoding="utf-8").read()
    return set(re.findall(r"^\| `(triton/[^`]+\.py)` \|", texto, flags=re.M))


def test_todo_arquivo_que_pergunta_pela_edicao_esta_no_mapa():
    no_codigo = _arquivos_que_perguntam()
    assert no_codigo, "nenhum arquivo pergunta pela edição?"
    for mapa in MAPAS:
        no_mapa = _arquivos_do_mapa(mapa)
        assert not no_codigo - no_mapa, f"{os.path.basename(mapa)}: faltam {sorted(no_codigo - no_mapa)}"
        assert not no_mapa - no_codigo, f"{os.path.basename(mapa)}: sobram {sorted(no_mapa - no_codigo)}"
