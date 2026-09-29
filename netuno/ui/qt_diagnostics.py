"""Captura e localização de avisos do Qt.

O aviso ``QFont::setPointSize: Point size <= 0 (-1), must be greater than 0``
aparecia repetidamente no console durante o uso normal do programa. Ele não vem
do código do Netuno: uma varredura no pacote não encontrou **nenhuma** chamada a
``setPointSize``, e todas as construções de ``QFont`` usam tamanho literal
positivo. O aviso é emitido dentro do próprio Qt, a partir de alguma pilha que
não se reproduz na construção das telas — nem a janela principal, nem as 16
páginas da documentação, nem as 24 classes de gráfico o disparam num teste
headless.

Um aviso que não se reproduz não se corrige por adivinhação. O que este módulo
faz é transformá-lo de ruído em informação:

- na **primeira** ocorrência de cada aviso distinto, registra a pilha Python do
  momento em que o Qt o emitiu — que é exatamente o que faltava para localizar
  a origem;
- nas ocorrências seguintes do mesmo aviso, apenas conta, sem repetir no
  console. É o que elimina o incômodo sem esconder o fato.

O relatório fica em ``avisos_qt.log``, ao lado do executável, e um resumo é
impresso ao encerrar.
"""

from __future__ import annotations

import os
import sys
import traceback
from collections import Counter
from typing import Optional

from PySide6.QtCore import QtMsgType, qInstallMessageHandler

# Avisos que já tiveram a pilha registrada. Chave: o texto do aviso.
_JA_REGISTRADOS: set[str] = set()
_CONTAGEM: Counter[str] = Counter()
_CAMINHO_DO_LOG: Optional[str] = None

_ROTULOS = {
    QtMsgType.QtDebugMsg: "debug",
    QtMsgType.QtInfoMsg: "info",
    QtMsgType.QtWarningMsg: "aviso",
    QtMsgType.QtCriticalMsg: "crítico",
    QtMsgType.QtFatalMsg: "fatal",
}


def _diretorio_base() -> str:
    """Pasta onde gravar o log, tanto em execução normal quanto congelada."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _registrar_pilha(rotulo: str, mensagem: str) -> None:
    """Grava a pilha Python da primeira ocorrência de um aviso."""
    global _CAMINHO_DO_LOG
    if _CAMINHO_DO_LOG is None:
        _CAMINHO_DO_LOG = os.path.join(_diretorio_base(), "avisos_qt.log")

    # Descarta os quadros deste próprio módulo: eles não ajudam a localizar nada.
    pilha = traceback.format_stack()[:-2]

    try:
        with open(_CAMINHO_DO_LOG, "a", encoding="utf-8") as arquivo:
            barra = "=" * 78
            traco = "-" * 78
            arquivo.write(os.linesep)
            arquivo.write(f"{barra}{os.linesep}[{rotulo}] {mensagem}{os.linesep}{traco}{os.linesep}")
            arquivo.writelines(pilha)
    except OSError:
        # Um log que não pode ser escrito não é motivo para derrubar o programa.
        pass


def instalar_captura_de_avisos() -> None:
    """Instala o manipulador de mensagens do Qt.

    Chamado uma vez, logo após criar o ``QApplication``.
    """

    def manipulador(tipo, contexto, mensagem: str) -> None:
        rotulo = _ROTULOS.get(tipo, "qt")
        _CONTAGEM[mensagem] += 1

        if mensagem in _JA_REGISTRADOS:
            # Já se sabe de onde vem; repetir no console só atrapalha.
            return

        _JA_REGISTRADOS.add(mensagem)
        _registrar_pilha(rotulo, mensagem)
        print(f"[Qt {rotulo}] {mensagem}", file=sys.stderr)
        if _CAMINHO_DO_LOG:
            print(f"         pilha registrada em {_CAMINHO_DO_LOG}", file=sys.stderr)

    qInstallMessageHandler(manipulador)


def resumo_dos_avisos() -> str:
    """Uma linha por aviso distinto, com quantas vezes ocorreu."""
    if not _CONTAGEM:
        return ""
    linhas = ["Avisos do Qt nesta execução:"]
    for mensagem, quantas in _CONTAGEM.most_common():
        vezes = "vez" if quantas == 1 else "vezes"
        linhas.append(f"  {quantas} {vezes}: {mensagem}")
    if _CAMINHO_DO_LOG:
        linhas.append(f"  Pilhas em: {_CAMINHO_DO_LOG}")
    return os.linesep.join(linhas)


def contagem_de_avisos() -> Counter:
    """Exposto para teste."""
    return Counter(_CONTAGEM)
