# -*- coding: utf-8 -*-
"""O histórico de versões, escrito uma vez e distribuído em três lugares.

O que há de novo em cada versão é escrito só em
`manual/partes/38_historico_de_versoes.md`, no modelo:

    ## Versão 0.1.0 — 15 de outubro de 2026

    > **Em uma frase.** o resumo que aparece no panorama e no site

    ### Novidades
    ### Correções que alteram resultados
    ### Correções que não alteram resultados
    ### Documentação

Deste arquivo saem três coisas, e por isso elas não podem divergir:

1. `CHANGELOG.md`, na raiz, para quem acompanha o programa pelo código;
2. `manual/partes/_tabelas/cap38_versoes.md`, o panorama que o próprio capítulo
   inclui — número, data, resumo e quantas correções de cada tipo;
3. os dados da página de versões do site, por `entradas_estruturadas()`.

Uso:
    python manual/gerar_changelog.py
"""

from __future__ import annotations

import os
import re
import sys
from typing import Dict, List, Optional

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for caminho in (RAIZ, AQUI):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

from triton import __version__ as VERSAO  # noqa: E402

CAPITULO = os.path.join(AQUI, "partes", "38_historico_de_versoes.md")
SAIDA = os.path.join(RAIZ, "CHANGELOG.md")
TABELA = os.path.join(AQUI, "partes", "_tabelas", "cap38_versoes.md")
NL = chr(10)

#: As seções que uma entrada de versão pode ter, na ordem em que aparecem.
SECOES = ("Novidades", "Correções que alteram resultados",
          "Correções que não alteram resultados", "Documentação")

CABECALHO = f"""# O que há de novo em cada versão do Triton

Este arquivo é **gerado** do capítulo de histórico do manual do usuário
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz as mesmas seções: o resumo em uma frase, as novidades, **as
correções que alteram resultados de estudos já feitos**, as que não alteram e o
que mudou na documentação. A distinção entre os dois tipos de correção é a que
mais importa para quem publica com o programa: uma correção de cálculo obriga a
declarar a versão usada num trabalho; uma correção de interface, não.

A versão atual é a {VERSAO}. O manual completo está em `manual/Manual-Triton.pdf`
e o site de documentação, em `manual/site/index.html`.
"""


def entradas(texto: str) -> List[str]:
    """Os blocos «## Versão X.Y.Z — data» do capítulo, na ordem em que aparecem."""
    partes = re.split(r"^## (?=Versão \d)", texto, flags=re.M)[1:]
    blocos = []
    for parte in partes:
        # A entrada termina onde começa a próxima seção que não é de versão.
        corte = re.search(r"^## (?!Versão \d)", parte, flags=re.M)
        blocos.append(("## " + (parte[: corte.start()] if corte else parte)).rstrip())
    return blocos


def _texto_limpo(bloco: str) -> str:
    """Tira do texto o que só faz sentido dentro do manual montado."""
    import gerar as g
    linhas = [l for l in bloco.split(NL) if not re.match(r"^<!--\s*tabela:", l.strip())]
    texto = g.resolver_marcas(NL.join(linhas))
    texto = texto.replace("==", "")                    # o destaque é convenção do manual
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def _quantas_linhas(corpo: str) -> int:
    """Quantas linhas de tabela a seção traz — o tamanho da lista, sem contar cabeçalho."""
    linhas = [l for l in corpo.split(NL) if l.strip().startswith("|")]
    uteis = [l for l in linhas if not re.match(r"^\|[\s:\-|]+\|$", l.strip())]
    return max(0, len(uteis) - 1)


def entradas_estruturadas(texto: Optional[str] = None) -> List[Dict[str, object]]:
    """Cada versão como dado: número, data, resumo e as seções que ela traz.

    É o que a página de versões do site consome, e o que o panorama do manual
    conta. Nenhum destes números é digitado à mão.
    """
    texto = texto if texto is not None else open(CAPITULO, encoding="utf-8").read()
    estruturadas = []
    for bloco in entradas(texto):
        limpo = _texto_limpo(bloco)
        cabecalho = limpo.splitlines()[0]
        m = re.match(r"## Versão (\S+)( \(beta\))? — (.+)$", cabecalho)
        if not m:
            raise SystemExit(f"entrada fora do modelo «## Versão X.Y.Z — data»: {cabecalho}")
        corpo = limpo[len(cabecalho):].strip()
        resumo = ""
        r = re.search(r"^> \*\*Em uma frase\.\*\*\s*(.+?)(?=\n\s*\n|\Z)", corpo, flags=re.M | re.S)
        if r:
            resumo = re.sub(r"\s*\n>\s*", " ", r.group(1)).strip()
        secoes = {}
        for nome in SECOES:
            achada = re.search(rf"^### {re.escape(nome)}\s*\n(.*?)(?=^### |\Z)",
                               corpo, flags=re.M | re.S)
            if achada and achada.group(1).strip():
                secoes[nome] = achada.group(1).strip()
        estruturadas.append({
            "versao": m.group(1),
            "beta": bool(m.group(2)),
            "data": m.group(3).strip(),
            "resumo": resumo,
            "secoes": secoes,
            "altera_resultados": _quantas_linhas(secoes.get("Correções que alteram resultados", "")),
            "nao_altera_resultados": _quantas_linhas(secoes.get("Correções que não alteram resultados", "")),
            "texto": limpo,
        })
    return estruturadas


def montar() -> str:
    """O conteúdo do CHANGELOG.md."""
    itens = entradas_estruturadas()
    if not itens:
        raise SystemExit("nenhuma entrada «## Versão X.Y.Z» encontrada no capítulo")
    if itens[0]["versao"] != VERSAO:
        raise SystemExit(f"a entrada mais recente é a {itens[0]['versao']}, "
                         f"e a versão do programa é {VERSAO}")
    corpo = (NL * 2 + "---" + NL * 2).join(str(i["texto"]) for i in itens)
    return CABECALHO + NL + "---" + NL * 2 + corpo + NL


def montar_panorama() -> str:
    """O panorama que o capítulo inclui: uma linha por versão."""
    itens = entradas_estruturadas()
    linhas = ["<!-- tabela: **Tabela 99** — Panorama das versões publicadas -->",
              "| Versão | Data | O que trouxe | Correções que alteram resultados |",
              "| :--- | :--- | :--- | ---: |"]
    for i in itens:
        resumo = str(i["resumo"]).replace("|", "/") or "—"
        beta = " (beta)" if i.get("beta") else ""  # fora do negrito: o teste procura **X.Y.Z**
        linhas.append(f"| **{i['versao']}**{beta} | {i['data']} | {resumo} | {i['altera_resultados']} |")
    return NL.join(linhas) + NL


def _gravar(caminho: str, conteudo: str) -> bool:
    anterior = open(caminho, encoding="utf-8").read() if os.path.exists(caminho) else ""
    if conteudo == anterior:
        return False
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, "w", encoding="utf-8", newline="\n").write(conteudo)
    return True


def main() -> None:
    itens = entradas_estruturadas()
    _gravar(SAIDA, montar())
    _gravar(TABELA, montar_panorama())
    print(f"CHANGELOG.md e panorama: {len(itens)} versão(ões), a mais recente é a {VERSAO}")


if __name__ == "__main__":
    main()
