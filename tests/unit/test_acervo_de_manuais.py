"""A aba de Documentação anuncia os manuais; o que ela anuncia tem de ser verdade.

A página «Manuais Oficiais & Acervo Técnico» traz, para cada volume, o número de
páginas e o arquivo que o botão abre. Os dois estão escritos à mão no código, e
o manual é regerado a cada mudança de texto: uma seção nova desloca as páginas de
todos os volumes seguintes, e a página passa a prometer um número que o PDF não
tem.

Este teste lê os PDFs de verdade e confere os dois.
"""
import ast
import os
import re

import pytest

pytest.importorskip("pypdf", reason="conta páginas dos PDFs do manual (pip install pypdf)")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABA = os.path.join(RAIZ, "netuno", "ui", "tab_documentation.py")


def _paginas_do_pdf(caminho_relativo):
    from pypdf import PdfReader
    caminho = os.path.join(RAIZ, caminho_relativo)
    if not os.path.isfile(caminho):
        return None
    return len(PdfReader(caminho).pages)


def _volumes_anunciados():
    """Os pares (páginas, arquivo) que a página dos manuais promete.

    Lidos do código, e não da tela: a página só é construída com o Qt de pé, e
    esta verificação precisa rodar em qualquer máquina.
    """
    fonte = open(ABA, encoding="utf-8").read()
    trecho = fonte[fonte.index("vols_data"):]
    trecho = trecho[:trecho.index("for vol_num")]
    anunciados = []
    for bloco in re.finditer(r"\((\d),\s*(\d+),(.*?)\"(manual/mini/[^\"]+\.pdf)\"\)",
                             trecho, flags=re.S):
        anunciados.append((int(bloco.group(1)), int(bloco.group(2)), bloco.group(4)))
    return anunciados


def test_a_pagina_anuncia_os_sete_volumes():
    assert [v for v, _, _ in _volumes_anunciados()] == [1, 2, 3, 4, 5, 6, 7]


@pytest.mark.parametrize("volume,paginas,arquivo", _volumes_anunciados())
def test_o_numero_de_paginas_anunciado_e_o_do_pdf(volume, paginas, arquivo):
    """Se falhar: o manual foi regerado e o número na aba ficou para trás."""
    reais = _paginas_do_pdf(arquivo)
    if reais is None:
        pytest.skip(f"{arquivo} não foi gerado nesta árvore")
    assert reais == paginas, (f"o volume {volume} anuncia {paginas} páginas e o PDF "
                              f"tem {reais}")


def test_o_volume_geral_tambem_confere():
    fonte = open(ABA, encoding="utf-8").read()
    anunciadas = {int(n) for n in re.findall(r"(\d+)\s*PÁGINAS", fonte)}
    reais = _paginas_do_pdf("manual/Manual-Netuno-5.pdf")
    if reais is None:
        pytest.skip("o manual completo não foi gerado nesta árvore")
    assert anunciadas == {reais}, (f"a aba anuncia {sorted(anunciadas)} páginas para o "
                                   f"volume geral, que tem {reais}")


def test_todo_pdf_prometido_existe():
    """Botão que promete um arquivo ausente é o defeito mais visível de todos."""
    faltam = [a for _, _, a in _volumes_anunciados()
              if not os.path.isfile(os.path.join(RAIZ, a))]
    assert not faltam, "a aba oferece PDFs que não existem: " + ", ".join(faltam)
