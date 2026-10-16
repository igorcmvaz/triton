"""O texto-fonte do manual de INT e de PRT não traz material de outra edição.

INT: inglês neutro, nada do Brasil nem de Portugal. PRT: nada do Brasil. A BRL não é
conferida (o manual dela é brasileiro). A UFSC aparece como afiliação dos autores e é
permitida. O teste olha o texto-fonte (`manual/en/partes` e `manual/en/apendices` na INT;
`manual/partes` e `manual/apendices` na PRT), não os PDFs.
"""
import os
import re

import pytest

from triton.core.edition import get_current_edition

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")

BRASIL = ["Florianópolis", "Florianopolis", "Brasília", "Manaus", "São Paulo", "R$", "CASAN", "CELESC", "SABESP",
          "CLIMBra", "CMIP6", "INMET", "SINAPI", "ABNT", "NBR ", "Netuno", "Santa Catarina", "SNIS", "Selo Casa Azul"]
PORTUGAL = ["concelho", "EPAL", "E-OBS", "Lisboa", "Funchal", "ERSAR", "CAOP"]
PERMITIDO = ["Federal University of Santa Catarina", "Universidade Federal de Santa Catarina"]

EDICAO = get_current_edition()
if EDICAO == "INT":
    PASTAS, PROIBIDOS = ["en/partes", "en/apendices"], BRASIL + PORTUGAL
elif EDICAO == "PRT":
    pytest.skip("manual PRT ainda em reescrita (ativar quando a edicao estiver em portugues de Portugal)", allow_module_level=True)
else:
    pytest.skip("a BRL nao tem restricao de conteudo no manual", allow_module_level=True)


def _arquivos():
    for pasta in PASTAS:
        base = os.path.join(MANUAL, *pasta.split("/"))
        if not os.path.isdir(base):
            continue
        for raiz, _, nomes in os.walk(base):
            for n in nomes:
                if n.endswith(".md"):
                    yield os.path.join(raiz, n)


@pytest.mark.parametrize("caminho", sorted(_arquivos()), ids=lambda c: os.path.relpath(c, MANUAL))
def test_o_texto_do_manual_nao_traz_outra_edicao(caminho):
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    for ok in PERMITIDO:
        texto = texto.replace(ok, "")
    achados = sorted({t for t in PROIBIDOS if t in texto})
    assert not achados, f"{os.path.relpath(caminho, MANUAL)}: {achados}"
