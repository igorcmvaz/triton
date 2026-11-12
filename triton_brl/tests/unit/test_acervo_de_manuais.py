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
    esta verificação precisa rodar em qualquer máquina. O arquivo de cada volume vem de
    ``marca.MANUAIS_TEMATICOS`` (os nomes dos PDFs ficam em ``triton/marca.py``).
    """
    from triton import marca
    fonte = open(ABA, encoding="utf-8").read()
    trecho = fonte[fonte.index("vols_data"):]
    trecho = trecho[:trecho.index("for vol_num")]
    anunciados = []
    for bloco in re.finditer(r"\((\d),\s*(\d+),(.*?)_marca\.MANUAIS_TEMATICOS\[(\d)\]\)",
                             trecho, flags=re.S):
        anunciados.append((int(bloco.group(1)), int(bloco.group(2)),
                           marca.MANUAIS_TEMATICOS[int(bloco.group(4))]))
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
    """O dicionário PAGINAS_POR_EDICAO da aba, lido do código pelo mesmo motivo, na edição ativa."""
    from triton.core.edition import get_current_edition
    fonte = open(ABA, encoding="utf-8").read()
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.Assign) and any(
                getattr(alvo, "id", None) == "PAGINAS_POR_EDICAO" for alvo in no.targets):
            # As chaves são as constantes de triton/marca.py; só elas entram na avaliação.
            from triton import marca
            dicionario = eval(compile(ast.Expression(no.value), ABA, "eval"), {"__builtins__": {}, "_marca": marca})
            return sorted(dicionario.get(get_current_edition(), {}).items())
    raise AssertionError("a aba não declara PAGINAS_POR_EDICAO")


def test_a_aba_anuncia_o_manual_completo_da_edicao():
    """Cada edição publica um manual: o inglês na INT, o português na BRL e na IBE."""
    from triton.core.edition import get_current_edition
    from triton import marca
    esperado = marca.MANUAL_COMPLETO_EN if get_current_edition() == "INT" else marca.MANUAL_COMPLETO_PT
    assert [a for a, _ in _manuais_completos_anunciados()] == [esperado]


@pytest.mark.parametrize("arquivo,paginas", _manuais_completos_anunciados())
def test_o_volume_geral_tambem_confere(arquivo, paginas):
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

