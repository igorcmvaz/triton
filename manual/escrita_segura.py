# -*- coding: utf-8 -*-
"""Gravação que não desfaz revisão feita à mão.

Os geradores do manual escrevem arquivos que depois foram revisados diretamente:
legendas acrescentadas, tabelas trocadas por figuras, cabeçalhos preenchidos.
Rodar um gerador de novo sobrescrevia tudo em silêncio. A auditoria encontrou
dez arquivos nessa situação, com os números idênticos e a revisão perdida.

Esta função só grava quando o arquivo não existe ou quando o conteúdo é igual.
Se o conteúdo gerado difere do arquivo presente, ela não sobrescreve: grava a
versão nova ao lado, com a extensão `.gerado`, e avisa. Quem conduz a revisão
compara as duas, incorpora o que mudou e apaga o lateral. Para sobrescrever de
propósito, rode o gerador com a variável de ambiente NETUNO_REGERAR=1.

A proteção vale para o texto; os números continuam amarrados ao programa pelos
testes do manual, que falham se o texto revisado ficar para trás do motor.
"""

from __future__ import annotations

import os

IGUAL = "igual"
GRAVADO = "gravado"
DIVERGENTE = "divergente"


def gravar(caminho: str, texto: str) -> str:
    """Grava `texto` em `caminho` sem desfazer revisão manual. Devolve o que fez."""
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            atual = f.read()
        if atual == texto:
            lateral = caminho + ".gerado"
            if os.path.exists(lateral):
                os.remove(lateral)
            return IGUAL
        if os.environ.get("NETUNO_REGERAR") != "1":
            lateral = caminho + ".gerado"
            with open(lateral, "w", encoding="utf-8", newline="") as f:
                f.write(texto)
            print(f"  AVISO: {os.path.basename(caminho)} difere do que o gerador "
                  f"produz e não foi sobrescrito. A versão gerada está em "
                  f"{os.path.basename(lateral)}: compare, incorpore o que mudou e "
                  f"apague o lateral, ou rode com NETUNO_REGERAR=1.")
            return DIVERGENTE
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return GRAVADO
