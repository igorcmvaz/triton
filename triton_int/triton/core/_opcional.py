# -*- coding: utf-8 -*-
"""Importação preguiçosa de pacotes opcionais (extras do ``pyproject.toml``) com mensagem clara quando faltam.

Os extras ``docs``, ``analise``, ``cli``, ``otimizacao`` e ``grafo`` não fazem parte do ``requirements.txt`` nem do
instalador. Quem usa um recurso que depende deles chama :func:`importar` (ou :func:`disponivel`, quando há alternativa
sem o pacote); sem o pacote, o erro diz qual pacote, qual extra e como instalar, em vez de um ``ModuleNotFoundError``
solto. Este módulo usa só a biblioteca padrão e deve ser importado no TOPO do módulo que o usa: assim o empacotador o
alcança sem entrada em ``hiddenimports`` (``tests/unit/test_empacotamento.py``). Os pacotes opcionais em si nunca são
importados no topo de ``core``.
"""
from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType
from typing import Dict, Optional

#: Pacote opcional -> extra do ``pyproject.toml`` que o instala.
EXTRA_DO_PACOTE: Dict[str, str] = {
    "mkdocs": "docs",
    "duckdb": "analise",
    "rich": "cli",
    "optuna": "otimizacao",
    "pydeps": "grafo",
}


class PacoteOpcionalAusente(ImportError):
    """O recurso pedido precisa de um pacote opcional que não está instalado."""


def _distribuicao() -> str:
    """Nome da distribuição da edição ativa (``triton-brl``, ``triton-int`` ou ``triton-ibe``)."""
    try:
        from triton.core.edition import get_current_edition
        return "triton-" + str(get_current_edition()).lower()
    except Exception:
        return "triton-int"


def mensagem_de_falta(nome: str, extra: Optional[str] = None, para: str = "") -> str:
    """O texto do erro: o pacote, o recurso que o pede e o comando de instalação do extra."""
    extra = extra or EXTRA_DO_PACOTE.get(nome.split(".")[0], "")
    recurso = f" para {para}" if para else ""
    comando = f'pip install "{_distribuicao()}[{extra}]"' if extra else f"pip install {nome.split('.')[0]}"
    return (f"O pacote opcional «{nome}» é necessário{recurso}, mas não está instalado. "
            f"Instale-o com: {comando}. Ele não vem no instalador do programa.")


def disponivel(nome: str) -> bool:
    """Verdadeiro se o pacote pode ser importado (sem importá-lo)."""
    try:
        return importlib.util.find_spec(nome) is not None
    except (ImportError, ValueError):
        return False


def importar(nome: str, extra: Optional[str] = None, para: str = "") -> ModuleType:
    """Importa ``nome``; se faltar, levanta :class:`PacoteOpcionalAusente` com a mensagem de instalação."""
    try:
        return importlib.import_module(nome)
    except ImportError as erro:
        raise PacoteOpcionalAusente(mensagem_de_falta(nome, extra, para)) from erro
