"""
Coerência interna da documentação.

A documentação afirma coisas verificáveis: aponta para arquivos de código, cita figuras,
numera seções e faz referências cruzadas entre documentos. Nada disso é verificado por
um leitor humano de forma confiável, e tudo apodrece silenciosamente quando o código se
move — como já ocorreu neste projeto, em que 19 links relativos apontavam para caminhos
válidos apenas a partir da raiz.

Este módulo verifica o que é mecanicamente verificável:

- todo link relativo resolve para um arquivo existente;
- toda figura citada existe;
- todo caminho de código mencionado em `docs/` existe;
- a numeração de seções do relatório de V&V é sequencial, sem lacuna nem repetição.

Não verifica o conteúdo das afirmações — isso continua sendo trabalho de revisão.
"""

import re
import urllib.parse
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
DOCS = RAIZ / "docs"

#: Documentos cuja coerência é verificada. Inclui os README de cada área, porque são
#: os pontos de entrada que o leitor efetivamente segue.
DOCUMENTOS = [
    RAIZ / "README.md",
    DOCS / "README.md",
    DOCS / "metodologia.md",
    DOCS / "verificacao_e_validacao.md",
    RAIZ / "tarifas" / "README.md",
    RAIZ / "tests" / "README.md",
    RAIZ / "infos_licenses" / "README.md",
]

PADRAO_DE_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PADRAO_DE_IMAGEM = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def _documentos_existentes():
    return [d for d in DOCUMENTOS if d.exists()]


def _links_relativos(documento: Path):
    texto = documento.read_text(encoding="utf-8")
    for alvo in PADRAO_DE_LINK.findall(texto):
        if alvo.startswith(("http://", "https://", "mailto:", "#")):
            continue
        yield alvo


@pytest.mark.parametrize(
    "documento", _documentos_existentes(), ids=lambda d: d.relative_to(RAIZ).as_posix()
)
def test_links_relativos_resolvem(documento):
    """Nenhum link relativo aponta para arquivo inexistente."""
    quebrados = []
    for alvo in _links_relativos(documento):
        caminho = urllib.parse.unquote(alvo.split("#")[0])
        if not caminho:
            continue
        if not (documento.parent / caminho).exists():
            quebrados.append(alvo)

    assert not quebrados, (
        f"{documento.relative_to(RAIZ).as_posix()} tem links que não resolvem:\n  "
        + "\n  ".join(quebrados)
    )


@pytest.mark.parametrize(
    "documento", _documentos_existentes(), ids=lambda d: d.relative_to(RAIZ).as_posix()
)
def test_figuras_citadas_existem(documento):
    """Toda imagem referenciada está no repositório.

    Uma figura ausente degrada o documento em silêncio: o texto continua descrevendo
    um gráfico que o leitor não vê.
    """
    texto = documento.read_text(encoding="utf-8")
    ausentes = [
        alvo for alvo in PADRAO_DE_IMAGEM.findall(texto)
        if not alvo.startswith(("http://", "https://"))
        and not (documento.parent / urllib.parse.unquote(alvo)).exists()
    ]

    assert not ausentes, (
        f"{documento.relative_to(RAIZ).as_posix()} cita figuras inexistentes: {ausentes}"
    )


def test_secoes_do_relatorio_sao_sequenciais():
    """A numeração de seções do relatório de V&V não tem lacuna nem repetição.

    O relatório é lido por referência cruzada («ver §5.4»); numeração furada torna
    essas referências ambíguas.
    """
    relatorio = DOCS / "verificacao_e_validacao.md"
    if not relatorio.exists():
        pytest.skip("relatório de V&V ausente")

    numeros = [
        int(correspondencia.group(1))
        for linha in relatorio.read_text(encoding="utf-8").splitlines()
        if (correspondencia := re.match(r"^## (\d+)\.", linha))
    ]

    assert numeros, "o relatório não tem seções numeradas"
    esperado = list(range(1, len(numeros) + 1))
    assert numeros == esperado, (
        f"numeração de seções fora de ordem: {numeros}, esperado {esperado}"
    )


def test_caminhos_de_codigo_citados_existem():
    """Todo arquivo de código mencionado em `docs/` existe.

    A documentação cita módulos e testes por caminho (`triton/core/simulation.py`,
    `tests/invariants/...`). Quando um arquivo é renomeado, a citação passa a apontar
    para o nada sem que nada acuse.
    """
    # `scripts/` fica de fora: são ferramentas de desenvolvimento, no disco do mantenedor e fora do Git.
    padrao = re.compile(r"`((?:triton|tests|docs)/[\w/.-]+\.(?:py|md|json|csv))`")
    ausentes = {}

    for documento in DOCS.glob("*.md"):
        for caminho_citado in set(padrao.findall(documento.read_text(encoding="utf-8"))):
            if not (RAIZ / caminho_citado).exists():
                ausentes.setdefault(documento.name, []).append(caminho_citado)

    assert not ausentes, (
        "a documentação cita arquivos que não existem:\n  "
        + "\n  ".join(f"{doc}: {caminhos}" for doc, caminhos in ausentes.items())
    )


def test_indice_da_documentacao_cobre_os_documentos_principais():
    """O índice em `docs/README.md` não pode omitir os documentos centrais.

    O índice existe porque a documentação estava espalhada por sete diretórios sem
    ponto de entrada; ele só cumpre esse papel enquanto estiver completo.
    """
    indice = DOCS / "README.md"
    if not indice.exists():
        pytest.skip("índice ausente")

    texto = indice.read_text(encoding="utf-8")
    obrigatorios = ["metodologia.md", "verificacao_e_validacao.md",
                    "fluxogramas_metodologicos.md", "CLI_USAGE.md"]
    faltando = [nome for nome in obrigatorios if nome not in texto]

    assert not faltando, f"o índice não menciona: {faltando}"
