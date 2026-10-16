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
ABA = os.path.join(RAIZ, "triton", "ui", "tab_documentation.py")


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


def test_a_pagina_anuncia_os_oito_volumes():
    assert [v for v, _, _ in _volumes_anunciados()] == [1, 2, 3, 4, 5, 6, 7, 8]


@pytest.mark.parametrize("volume,paginas,arquivo", _volumes_anunciados())
def test_o_numero_de_paginas_anunciado_e_o_do_pdf(volume, paginas, arquivo):
    """A aba mostra as páginas do PDF que acompanha o programa, lidas na hora.

    O número escrito no código só vale se o PDF faltar; antes era o único, e a cada
    regeração do manual ficava para trás.
    """
    reais = _paginas_do_pdf(arquivo)
    if reais is None:
        pytest.skip(f"{arquivo} não foi gerado nesta árvore")
    # A aba é de interface: sem Qt (integração contínua), o teste é pulado, e não falha.
    pytest.importorskip("PySide6.QtWidgets", reason="a aba de documentação exige a interface gráfica")
    from triton.ui.tab_documentation import paginas_do_pdf
    assert paginas_do_pdf(arquivo, -1) == reais, f"o volume {volume} não mostra as {reais} páginas do PDF"


def _manuais_completos_anunciados():
    """O dicionário PAGINAS_DO_MANUAL_COMPLETO da aba, lido do código pelo mesmo motivo."""
    fonte = open(ABA, encoding="utf-8").read()
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.Assign) and any(
                getattr(alvo, "id", None) == "PAGINAS_DO_MANUAL_COMPLETO" for alvo in no.targets):
            return sorted(ast.literal_eval(no.value).items())
    raise AssertionError("a aba não declara PAGINAS_DO_MANUAL_COMPLETO")


def test_a_aba_anuncia_o_manual_completo_nas_duas_linguas():
    assert [a for a, _ in _manuais_completos_anunciados()] == [
        "manual/Manual-Triton.pdf", "manual/en/Triton-User-Manual.pdf"]


@pytest.mark.parametrize("arquivo,paginas", _manuais_completos_anunciados())
def test_o_volume_geral_tambem_confere(arquivo, paginas):
    from triton.core.edition import get_current_edition
    if get_current_edition() == "INT" and arquivo == "manual/Manual-Triton.pdf":
        # A edição internacional publica só o manual em inglês; o PDF em português que sobrou
        # na pasta é rastro da edição brasileira e não é o que a aba abre.
        pytest.skip("a edição INT não publica o manual em português")
    reais = _paginas_do_pdf(arquivo)
    if reais is None:
        pytest.skip(f"{arquivo} não foi gerado nesta árvore")
    assert reais == paginas, (f"a aba anuncia {paginas} páginas para {arquivo}, "
                              f"que tem {reais}")


def test_nenhum_numero_de_paginas_escrito_a_mao_no_volume_geral():
    """O cartão do volume geral lê o número do dicionário; um «312 PÁGINAS» solto envelhece."""
    fonte = open(ABA, encoding="utf-8").read()
    assert not re.findall(r"\b\d+\s*PÁGINAS", fonte)


def test_todo_pdf_prometido_existe():
    """Botão que promete um arquivo ausente é o defeito mais visível de todos."""
    from triton.core.edition import get_current_edition
    if get_current_edition() == "INT":
        pytest.skip("a edição INT publica apenas o manual completo em inglês")
    faltam = [a for _, _, a in _volumes_anunciados()
              if not os.path.isfile(os.path.join(RAIZ, a))]
    assert not faltam, "a aba oferece PDFs que não existem: " + ", ".join(faltam)

