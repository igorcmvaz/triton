# -*- coding: utf-8 -*-
"""Gera o CHANGELOG.md da raiz a partir do capítulo de histórico do manual.

O que há de novo em cada versão é escrito uma vez só, em
`manual/partes/38_historico_de_versoes.md`, na forma de uma entrada por versão:

    ## Versão 5.0.0 — 21 de setembro de 2026
    ### Correções que alteram resultados
    ### Correções que não alteram resultados

Daqui sai o arquivo que o repositório distribui, para quem acompanha o programa
pelo código e não pelo manual. Como é gerado, os dois não podem divergir, e um
teste recusa a divergência (tests/unit/test_changelog.py).

Uso:
    python manual/gerar_changelog.py
"""

from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from netuno import __version__ as VERSAO  # noqa: E402

CAPITULO = os.path.join(AQUI, "partes", "38_historico_de_versoes.md")
SAIDA = os.path.join(RAIZ, "CHANGELOG.md")
NL = chr(10)

CABECALHO = f"""# O que há de novo em cada versão do Netuno

Este arquivo é **gerado** do capítulo de histórico do manual do usuário
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz duas listas, e a distinção é a que mais importa para quem
publica com o programa: **o que altera resultados de estudos já feitos** e o que
não altera. Uma correção de cálculo obriga a declarar a versão usada num
trabalho; uma correção de interface, não.

A versão atual é a {VERSAO}. O manual completo está em `manual/Manual-Netuno-5.pdf`
e o site de documentação, em `manual/site/index.html`.
"""


def entradas(texto):
    """Os blocos «## Versão X.Y.Z — data» do capítulo, na ordem em que aparecem."""
    partes = re.split(r"^## (?=Versão \d)", texto, flags=re.M)[1:]
    blocos = []
    for parte in partes:
        # A entrada termina onde começa a próxima seção que não é de versão.
        corte = re.search(r"^## (?!Versão \d)", parte, flags=re.M)
        blocos.append(("## " + (parte[: corte.start()] if corte else parte)).rstrip())
    return blocos


def limpar(bloco):
    """Tira do texto o que só faz sentido dentro do manual montado."""
    import gerar as g
    linhas = []
    for linha in bloco.split(NL):
        if re.match(r"^<!--\s*tabela:", linha.strip()):
            continue
        linhas.append(linha)
    texto = NL.join(linhas)
    # As marcas de remissão viram o número da seção desta montagem.
    texto = g.resolver_marcas(texto)
    texto = texto.replace("==", "")                    # o destaque é convenção do manual
    texto = re.sub(r"^> \*\*(Aprofundamento[^*]*)\*\*\s*", r"> **\1** ", texto, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def montar():
    texto = open(CAPITULO, encoding="utf-8").read()
    blocos = entradas(texto)
    if not blocos:
        raise SystemExit("nenhuma entrada «## Versão X.Y.Z» encontrada no capítulo")
    if VERSAO not in blocos[0]:
        raise SystemExit(f"a entrada mais recente não é a da versão {VERSAO}: {blocos[0][:60]}")
    corpo = (NL * 2 + "---" + NL * 2).join(limpar(b) for b in blocos)
    return CABECALHO + NL + "---" + NL * 2 + corpo + NL


def main():
    conteudo = montar()
    anterior = open(SAIDA, encoding="utf-8").read() if os.path.exists(SAIDA) else ""
    if conteudo != anterior:
        open(SAIDA, "w", encoding="utf-8", newline="\n").write(conteudo)
    versoes = len(entradas(open(CAPITULO, encoding="utf-8").read()))
    print(f"CHANGELOG.md  {versoes} versão(ões), a mais recente é a {VERSAO}")


if __name__ == "__main__":
    main()
