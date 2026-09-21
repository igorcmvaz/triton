"""Um padrão hidrológico vale em todo caminho de entrada, ou não é padrão.

O coeficiente de escoamento já teve quatro valores de recurso diferentes
espalhados pelo programa, e o mesmo projeto rendia captações diferentes conforme
fosse aberto por arquivo, por planilha ou pela tela. A lâmina de descarte tinha o
mesmo defeito: 1,0 mm no arquivo de projeto, na leitura de planilha e no motor,
contra 2,0 mm no exportador CAD, na linha de comando e na dica do próprio campo.

`netuno/core/hydrology_defaults.py` é o único lugar onde esses números moram.
Este teste recusa que alguém volte a escrever um deles à mão.
"""
import ast
import os

from netuno.core.hydrology_defaults import (
    COEFICIENTE_DE_ESCOAMENTO_PADRAO,
    FONTE_DA_LAMINA_DE_DESCARTE,
    LAMINA_DE_DESCARTE_PADRAO_MM,
)
from netuno.core.parser import NetunoConfig

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, "netuno")

#: O módulo dos padrões é onde os números podem aparecer escritos.
DONO = os.path.join(PACOTE, "core", "hydrology_defaults.py")

#: Argumentos cujo valor de recurso é a lâmina de descarte.
NOMES_DA_LAMINA = ("discard", "discard_mm", "discard_depth")


def test_a_lamina_padrao_e_a_da_norma():
    """A NBR 15527:2019 recomenda 2 mm na ausência de dado local."""
    assert LAMINA_DE_DESCARTE_PADRAO_MM == 2.0
    assert "15527" in FONTE_DA_LAMINA_DE_DESCARTE


def test_o_projeto_novo_ja_nasce_com_a_lamina_da_norma():
    """Quem não toca no campo recebe o número da norma, e não um sem procedência."""
    assert NetunoConfig().discard == LAMINA_DE_DESCARTE_PADRAO_MM


def _defaults_de_lamina_escritos_a_mao():
    """Assinaturas `def f(..., discard_mm=<número>)` fora do módulo dos padrões."""
    achados = []
    for pasta, _, arquivos in os.walk(PACOTE):
        if "__pycache__" in pasta:
            continue
        for arquivo in arquivos:
            if not arquivo.endswith(".py"):
                continue
            caminho = os.path.join(pasta, arquivo)
            if os.path.abspath(caminho) == os.path.abspath(DONO):
                continue
            arvore = ast.parse(open(caminho, encoding="utf-8").read(), filename=caminho)
            for no in ast.walk(arvore):
                if not isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                args = no.args.args + no.args.kwonlyargs
                padroes = ([None] * (len(no.args.args) - len(no.args.defaults))
                           + list(no.args.defaults) + list(no.args.kw_defaults))
                for arg, padrao in zip(args, padroes):
                    # Zero não é um valor de recurso: quer dizer «sem
                    # descartador», que é uma configuração, não uma omissão.
                    if arg.arg in NOMES_DA_LAMINA and isinstance(padrao, ast.Constant) \
                            and isinstance(padrao.value, (int, float)) and padrao.value:
                        achados.append(f"{os.path.relpath(caminho, RAIZ)}:{no.lineno} "
                                       f"{no.name}({arg.arg}={padrao.value})")
    return achados


def test_nenhuma_funcao_escreve_a_lamina_a_mao():
    """Se falhar: importe LAMINA_DE_DESCARTE_PADRAO_MM em vez de digitar o número."""
    achados = _defaults_de_lamina_escritos_a_mao()
    assert not achados, ("lâmina de descarte escrita à mão em: " + "; ".join(achados))


def test_o_coeficiente_de_escoamento_continua_num_lugar_so():
    """O defeito que o módulo dos padrões resolveu primeiro não pode voltar."""
    assert COEFICIENTE_DE_ESCOAMENTO_PADRAO == 0.75


def test_o_exemplo_da_tela_e_a_lamina_que_vale_se_nada_for_dito():
    """A dica do campo não pode sugerir um número e o motor assumir outro.

    O texto é traduzido por frase inteira, e por isso o número está escrito nele.
    Este teste é o que mantém os dois em acordo.
    """
    fonte = open(os.path.join(PACOTE, "ui", "tab_project.py"), encoding="utf-8").read()
    esperado = f"{LAMINA_DE_DESCARTE_PADRAO_MM:.1f}".replace(".", ",")
    assert f'setPlaceholderText(tr("Ex: {esperado}"))' in fonte
