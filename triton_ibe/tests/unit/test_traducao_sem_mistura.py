"""Nenhum rótulo pode sair metade em chinês e metade em português.

A tradução do chinês e do espanhol tem um recurso de composição: quando a frase
inteira não está no catálogo, o programa substitui os pedaços que reconhece. Para
um rótulo longo, montado de partes conhecidas, isso funciona. Para um rótulo
curto, produz «Análise 经济-Financeira» — que não é chinês nem português, e que
ninguém percebe sem abrir o programa em chinês.

Eram oitenta e quatro rótulos assim. Este teste percorre tudo o que o programa
passa por `tr()` e recusa saída em chinês que ainda carregue palavra latina.

A verificação usa `tr(texto, lang="zh")`, e não `set_current_lang`: este último
grava o idioma nas preferências do usuário, e um teste não tem o direito de
deixar o programa em outra língua depois de rodar.
"""
import ast
import os
import re

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACOTE = os.path.join(RAIZ, "triton")

CJK = re.compile(r"[一-鿿]")
PALAVRA_LATINA = re.compile(r"\b[A-Za-zÀ-ÿ]{4,}\b")

#: Siglas, nomes próprios e unidades que ficam em alfabeto latino também em
#: chinês, como é praxe em texto técnico.
ESTRANGEIRISMOS = re.compile(
    r"(Triton|PDF|CSV|CAD|BIM|TOPSIS|VIKOR|SMAA|ESG|LEED|EDGE|GRI|AQUA|HQE|ETAP|"
    r"YAS|CAPEX|OPEX|CMIP|INMET|ABNT|NBR|ANEEL|CLIMBra|Excel|JSON|HTML|SVG|DXF|"
    r"ACV|LCA|SSP|GCM|QDM|TIR|VPL|PRCPTOT|SDII|CDD|CWD|ETCCDI|INM|IPCA|INPC|"
    r"Selic|SINAPI|CUB|CREA|UFSC|CASAN|Joinville|AISI|HDPE|PEAD|PRFV|TFDI|"
    r"Casa|Azul|CAIXA|Schneider|Cryspin|Walsh|Lawler|Mayer|DeOreo|Ghisi|Vaz|IPTU|"
    r"First|Flush|kWh|CO2|json|xlsx|triton|Delta|"
    r"three\.js|MIT|Poly|Haven|Quarry|CC0|WebGL)")

#: Rótulos longos e trechos de HTML não são texto de botão: a composição neles é
#: o recurso funcionando, e não o defeito.
LIMITE_DE_ROTULO = 70


def _frases_passadas_por_tr():
    """Toda constante literal que o programa entrega a `tr()`."""
    frases = set()
    for pasta, _, arquivos in os.walk(PACOTE):
        if "__pycache__" in pasta:
            continue
        for arquivo in arquivos:
            if not arquivo.endswith(".py"):
                continue
            caminho = os.path.join(pasta, arquivo)
            try:
                arvore = ast.parse(open(caminho, encoding="utf-8").read(), filename=caminho)
            except SyntaxError:
                continue
            for no in ast.walk(arvore):
                if (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                        and no.func.id == "tr" and no.args
                        and isinstance(no.args[0], ast.Constant)
                        and isinstance(no.args[0].value, str)):
                    frases.add(no.args[0].value)
    return frases


def _sai_misturado(traduzido):
    if not CJK.search(traduzido):
        return False                      # não foi traduzido: outro assunto
    resto = ESTRANGEIRISMOS.sub("", traduzido)
    resto = re.sub(r"\{[a-z_]+\}", "", resto)        # marcas de formatação
    return bool(PALAVRA_LATINA.search(resto))


def test_nenhum_rotulo_curto_sai_metade_em_cada_lingua():
    """Se falhar: ponha a frase inteira em `_CHINESE_DICTIONARY`.

    Traduzir o pedaço não resolve — é justamente o pedaço reconhecido que
    produz a mistura.
    """
    from triton.ui.translation import tr

    misturados = []
    for frase in sorted(_frases_passadas_por_tr()):
        if "<" in frase or len(frase) > LIMITE_DE_ROTULO:
            continue
        traduzido = tr(frase, lang="zh")
        if _sai_misturado(traduzido):
            misturados.append(f"{frase!r} -> {traduzido!r}")
    assert not misturados, ("rótulo em duas línguas:\n  " + "\n  ".join(misturados[:20]))


def test_conferir_a_traducao_nao_muda_o_idioma_do_usuario():
    """O teste acima não pode deixar o programa em chinês depois de rodar."""
    from triton.ui.translation import get_current_lang, tr

    antes = get_current_lang()
    tr("Carregar arquivo", lang="zh")
    assert get_current_lang() == antes


@pytest.mark.parametrize("frase,esperado", [
    ("Análise Econômico-Financeira", "经济财务分析"),
    ("Referências Bibliográficas", "参考文献"),
    ("Precipitação & Hidrologia", "降水与水文"),
])
def test_alguns_rotulos_conferidos_um_a_um(frase, esperado):
    """Amostra fixa: a varredura acima prova ausência de mistura, não acerto."""
    from triton.ui.translation import tr
    assert tr(frase, lang="zh") == esperado
