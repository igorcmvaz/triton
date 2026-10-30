# -*- coding: utf-8 -*-
"""Saída de progresso de ``triton estudo run`` e ``triton estudo lote`` (``--progresso {auto,rich,simples}``).

O progresso vai SEMPRE para a saída de erro: os arquivos de resultado (CSV, JSON, Markdown, LaTeX, XLSX) e a saída padrão
não mudam um byte com o modo escolhido.

* ``simples``: uma linha por caso, ``[i/N] id: ok (t s)``, como sempre foi (o ``log`` de :func:`triton.core.estudo.rodar_estudo`);
* ``rich``: barra de progresso colorida do pacote opcional ``rich`` (extra ``cli``, via :mod:`triton.core._opcional`); sem o
  pacote, ou sem terminal de erro (executável de janela), cai em ``simples`` com um aviso, uma vez;
* ``auto``: ``rich`` se o pacote existe e a saída de erro é um terminal; senão ``simples``.

``--quiet`` desliga tudo, e nesse caso o modo nem é avaliado.
"""

from __future__ import annotations

import sys
from typing import Any, Callable, Optional, Tuple

from triton.cli_textos import t as _t
from triton.core import _opcional

MODOS = ("auto", "rich", "simples")

Log = Optional[Callable[[str], None]]
Progresso = Optional[Callable[..., None]]


def _erro_e_terminal() -> bool:
    erro = sys.stderr
    return erro is not None and bool(getattr(erro, "isatty", lambda: False)())


def _escrever_erro(msg: str) -> None:
    print(msg, file=sys.stderr)


def escolher_modo(modo: str, rich_disponivel: Optional[bool] = None, terminal: Optional[bool] = None) -> Tuple[str, Optional[str]]:
    """O modo efetivo (``rich`` ou ``simples``) e o aviso a mostrar (ou ``None``).

    Só o ``rich`` pedido de forma explícita e indisponível gera aviso; ``auto`` cai em ``simples`` sem barulho.
    """
    if modo not in MODOS:
        raise ValueError(_t("progresso desconhecido: {0}. Use {1}.").format(modo, ", ".join(MODOS)))
    if modo == "simples":
        return "simples", None
    ha_rich = _opcional.disponivel("rich") if rich_disponivel is None else rich_disponivel
    e_terminal = _erro_e_terminal() if terminal is None else terminal
    if modo == "auto":
        return ("rich", None) if (ha_rich and e_terminal) else ("simples", None)
    if not ha_rich:
        aviso = _opcional.mensagem_de_falta("rich", "cli", _t("o progresso colorido")) + " " + _t("Usando o progresso simples.")
        return "simples", aviso
    if sys.stderr is None:                       # executável de janela: nada onde desenhar a barra
        return "simples", None
    return "rich", None


class _Rich:
    """Uma barra por estudo, na saída de erro; os casos com erro aparecem como linhas acima da barra."""

    def __init__(self, rich_progress: Any, rich_console: Any) -> None:
        P = rich_progress
        self._console = rich_console.Console(stderr=True)
        self._barra = P.Progress(P.TextColumn("{task.description}"), P.BarColumn(), P.MofNCompleteColumn(),
                                 P.TimeElapsedColumn(), P.TimeRemainingColumn(), console=self._console)
        self._tarefa: Any = None
        self._total = 1
        self._iniciada = False

    def __call__(self, evento: str, feitos: int, total: int, rotulo: str, erro: Optional[str] = None) -> None:
        if not self._iniciada:
            self._barra.start()
            self._iniciada = True
        if evento == "inicio":
            if self._tarefa is not None:
                self._barra.update(self._tarefa, completed=self._total)
            self._total = max(1, total)
            self._tarefa = self._barra.add_task(rotulo, total=self._total, completed=feitos)
            return
        if erro is not None:
            self._console.print(f"{rotulo}: {erro}", markup=False, highlight=False)
        if self._tarefa is not None:
            self._barra.update(self._tarefa, completed=feitos)

    def fechar(self) -> None:
        if self._iniciada:
            self._barra.stop()


def criar(modo: str, quiet: bool) -> Tuple[Log, Progresso, Callable[[], None]]:
    """``(log, progresso, fechar)`` para passar a ``rodar_estudo``/``rodar_lote``; ``fechar`` sempre deve ser chamado no fim."""
    nada = (lambda: None)
    if quiet:
        return None, None, nada
    efetivo, aviso = escolher_modo(modo)
    if aviso:
        _escrever_erro(f"{_t('Aviso:')} {aviso}")
    if efetivo == "simples":
        return _escrever_erro, None, nada
    progress = _opcional.importar("rich.progress", "cli", _t("o progresso colorido"))
    console = _opcional.importar("rich.console", "cli", _t("o progresso colorido"))
    barra = _Rich(progress, console)
    return None, barra, barra.fechar
