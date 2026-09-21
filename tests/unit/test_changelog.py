"""O CHANGELOG.md distribuído é o capítulo de histórico do manual, e não outra lista.

Duas listas escritas à mão divergem no segundo lançamento. Aqui existe uma só: o
capítulo do manual. O arquivo da raiz é gerado dele, e estes testes recusam a
divergência e o esquecimento — lançar sem registrar o que mudou.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
for caminho in (RAIZ, MANUAL):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

import gerar_changelog as gc  # noqa: E402
from netuno import __version__  # noqa: E402


def test_o_changelog_da_raiz_esta_em_dia_com_o_manual():
    """Se falhar: rode python manual/gerar_changelog.py e comite o resultado."""
    assert os.path.exists(gc.SAIDA), "CHANGELOG.md não existe na raiz"
    assert open(gc.SAIDA, encoding="utf-8").read() == gc.montar()


def test_a_versao_atual_tem_entrada_propria():
    """Lançar sem dizer o que mudou é o defeito que este teste impede."""
    blocos = gc.entradas(open(gc.CAPITULO, encoding="utf-8").read())
    assert blocos, "o capítulo não tem nenhuma entrada «## Versão X.Y.Z»"
    titulo = blocos[0].split("\n")[0]
    assert __version__ in titulo, (f"a entrada mais recente é «{titulo}», "
                                   f"e a versão do programa é {__version__}")
    assert re.search(r"— \d{1,2} de \w+ de \d{4}", titulo), f"falta a data em «{titulo}»"


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


def test_a_data_do_lancamento_e_a_mesma_no_manual_e_na_citacao():
    """O CITATION.cff diz quando a versão saiu; o manual tem de dizer o mesmo dia."""
    citacao = open(os.path.join(RAIZ, "CITATION.cff"), encoding="utf-8").read()
    m = re.search(r'date-released:\s*"(\d{4})-(\d{2})-(\d{2})"', citacao)
    assert m, "CITATION.cff sem date-released"
    ano, mes, dia = int(m.group(1)), int(m.group(2)), int(m.group(3))
    titulo = gc.entradas(open(gc.CAPITULO, encoding="utf-8").read())[0].splitlines()[0]
    assert f"{dia} de {MESES[mes - 1]} de {ano}" in titulo, (titulo, m.group(0))


def test_cada_entrada_separa_o_que_muda_resultado_do_que_nao_muda():
    for bloco in gc.entradas(open(gc.CAPITULO, encoding="utf-8").read()):
        titulo = bloco.split("\n")[0]
        assert "### Correções que alteram resultados" in bloco, titulo
        assert "### Correções que não alteram resultados" in bloco, titulo


def test_as_versoes_vem_da_mais_nova_para_a_mais_antiga():
    def numero(bloco):
        m = re.search(r"Versão (\d+)\.(\d+)\.(\d+)", bloco)
        return tuple(int(x) for x in m.groups())
    numeros = [numero(b) for b in gc.entradas(open(gc.CAPITULO, encoding="utf-8").read())]
    assert numeros == sorted(numeros, reverse=True), numeros


def test_o_changelog_nao_leva_as_convencoes_do_manual():
    texto = open(gc.SAIDA, encoding="utf-8").read()
    assert "{{" not in texto, "marca de remissão não resolvida"
    assert "==" not in texto, "destaque do manual vazou para o changelog"
    assert "<!-- tabela:" not in texto, "comentário de legenda de tabela vazou"
