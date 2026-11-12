"""Central do nome do programa: ponto único para trocar a marca.

Nada aqui altera o pacote Python (continua ``triton``). Quando o nome do programa for
fechado, mude as constantes abaixo; interface, manuais, relatórios e instaladores leem daqui.

Os textos-fonte (catálogos de tradução, ajuda da linha de comando, laudos) continuam escritos
com o nome antigo, porque são chaves de dicionário. O nome que o usuário vê sai de ``aplicar``,
chamada nos pontos de passagem: ``tr`` (interface), ``cli_textos.t`` (linha de comando),
``report_generator._localize_report_markup`` (laudos) e a montagem das páginas da aba de
Documentação. Texto que não passa por eles usa ``NOME`` ou ``aplicar`` onde é montado; o teste
``tests/unit/test_marca_varredura.py`` aponta o literal novo que escapar.
"""
from __future__ import annotations

import re
from functools import lru_cache

#: Nome mostrado ao usuário (títulos, manuais, relatórios, instaladores).
NOME = "Triton"
#: Nome completo para citação (CITATION.cff e metadados do Zenodo devem coincidir).
NOME_CITACAO = "Triton"
#: Identificador DOI do registro vigente do Zenodo (muda quando o nome mudar e houver novo registro).
DOI = "10.5281/zenodo.23402916"

#: Extensão com que os projetos são gravados.
EXTENSAO_PROJETO = ".triton"
#: Todas as extensões de projeto que o programa abre (a antiga continua aceita).
EXTENSOES_PROJETO = (".triton", ".netuno")
#: Extensões aceitas como entrada de projeto, incluindo o JSON estruturado.
EXTENSOES_ENTRADA = EXTENSOES_PROJETO + (".json",)

#: Manual completo em português (BRL e IBE), relativo à raiz do programa. Mudar aqui não renomeia o PDF.
MANUAL_COMPLETO_PT = "manual/Manual-Triton.pdf"
#: Manual completo em inglês (INT), relativo à raiz do programa. Mudar aqui não renomeia o PDF.
MANUAL_COMPLETO_EN = "manual/en/Triton-User-Manual.pdf"
#: Os oito volumes temáticos, na ordem em que a aba de Documentação os mostra (volume 1 primeiro).
MANUAIS_TEMATICOS = (
    "manual/mini/Manual-Triton-1-comece-aqui.pdf",
    "manual/mini/Manual-Triton-2-metodo.pdf",
    "manual/mini/Manual-Triton-3-guias.pdf",
    "manual/mini/Manual-Triton-4-tutorial.pdf",
    "manual/mini/Manual-Triton-5-confiabilidade.pdf",
    "manual/mini/Manual-Triton-6-versoes.pdf",
    "manual/mini/Manual-Triton-7-modulacao.pdf",
    "manual/mini/Manual-Triton-8-apendices.pdf",
)


def eh_projeto(caminho: str) -> bool:
    """True se o caminho termina numa extensão de projeto (.triton ou .netuno)."""
    return str(caminho).lower().endswith(EXTENSOES_PROJETO)


def eh_entrada(caminho: str) -> bool:
    """True se o caminho termina numa extensão aceita como entrada (.triton, .netuno, .json)."""
    return str(caminho).lower().endswith(EXTENSOES_ENTRADA)


def filtro_qt(inclui_csv: bool = True) -> str:
    """Padrões para o diálogo de abrir arquivo, por exemplo ``*.triton *.netuno *.json *.csv``."""
    pads = ["*" + e for e in EXTENSOES_ENTRADA] + (["*.csv"] if inclui_csv else [])
    return " ".join(pads)


def extensao_para_salvar(caminho_aberto: str = "") -> str:
    """Extensão do diálogo de salvar: a do projeto aberto, se for de projeto; senão ``EXTENSAO_PROJETO``."""
    for ext in EXTENSOES_PROJETO:
        if str(caminho_aberto or "").lower().endswith(ext):
            return ext
    return EXTENSAO_PROJETO


def filtro_para_salvar(filtro: str, extensao: str = EXTENSAO_PROJETO) -> str:
    """O filtro do diálogo de salvar com as duas extensões de projeto, ``extensao`` primeiro.

    ``filtro`` é a saída de ``tr`` para a chave com ``(*.triton)``: a chave do catálogo não muda,
    só o padrão que o diálogo recebe (``(*.triton *.netuno)`` ou ``(*.netuno *.triton)``).
    """
    exts = [extensao] + [e for e in EXTENSOES_PROJETO if e != extensao]
    return filtro.replace("(*.triton)", "(" + " ".join("*" + e for e in exts) + ")", 1)


def _nome_no_codigo() -> str:
    """O nome com que os textos-fonte estão escritos no código; não é a marca.

    Montado em partes de propósito: não é constante da marca, e a ferramenta que troca o nome
    em ``marca.py`` não deve reescrevê-lo (os catálogos continuam com o nome antigo).
    """
    return "".join(("Tri", "ton"))


@lru_cache(maxsize=1)
def _padrao() -> "re.Pattern[str]":
    """A palavra inteira (``Triton`` ou ``TRITON``), fora de caminhos, nomes de arquivo e identificadores.

    Não casa em ``.triton``, ``triton.``, ``TritonConfig``, ``TRITON_EDITION``, ``Manual-Triton.pdf``,
    ``Triton-INT``, ``Triton2.png``, ``Triton.exe``, ``/Triton/`` nem em ``subject=Triton%20``.
    """
    nome = _nome_no_codigo()
    return re.compile(r"(?<![A-Za-z0-9_./\\=-])(" + nome + "|" + nome.upper()
                      + r")(?![A-Za-z0-9_%-]|\.[A-Za-z0-9]|[/\\])")


def aplicar(texto):
    """O texto com o nome do programa trocado por ``NOME`` (em maiúsculas onde estava em maiúsculas).

    Com ``NOME`` igual ao nome no código, devolve o próprio objeto, sem nenhuma mudança. O que não
    é ``str`` volta como veio.
    """
    if not isinstance(texto, str) or NOME == _nome_no_codigo():
        return texto
    return _padrao().sub(lambda m: NOME.upper() if m.group(1).isupper() else NOME, texto)
