"""Edições do Netuno 5: Brasil (BRL) e Internacional (INT).

As duas edições partem do mesmo código e hoje se distinguem pelo ponto de
entrada (main_brl.py, main_int.py), pelo executável e pelo título da janela.
Idioma, moeda e fonte de chuva são escolhidos na própria interface em qualquer
edição; get_edition_default_language e get_edition_currency_symbol registram os
padrões pretendidos para cada uma, mas ainda não são aplicados à interface.
"""

from __future__ import annotations

import os

EDITION_BRL = "BRL"
EDITION_INT = "INT"

ENV_VAR_EDITION = "NETUNO_EDITION"


def get_current_edition() -> str:
    """Retorna o código da edição ativa ('BRL' ou 'INT'). Padrão: 'BRL'."""
    val = os.environ.get(ENV_VAR_EDITION, EDITION_BRL).strip().upper()
    if val in (EDITION_BRL, EDITION_INT):
        return val
    return EDITION_BRL


def set_current_edition(edition: str) -> None:
    """Define a edição ativa ('BRL' ou 'INT')."""
    ed = str(edition).strip().upper()
    if ed not in (EDITION_BRL, EDITION_INT):
        raise ValueError(f"Edição inválida: {edition}. Escolha 'BRL' ou 'INT'.")
    os.environ[ENV_VAR_EDITION] = ed


def is_brl_edition() -> bool:
    """Verifica se a edição Brasil está ativa."""
    return get_current_edition() == EDITION_BRL


def is_int_edition() -> bool:
    """Verifica se a edição Internacional está ativa."""
    return get_current_edition() == EDITION_INT


def get_edition_title() -> str:
    """Título da janela principal: o título do programa e a edição ativa."""
    from netuno import APP_TITLE

    if is_int_edition():
        return f"{APP_TITLE} — International Edition (INT)"
    return f"{APP_TITLE} — Edição Brasil (BRL)"


def get_edition_default_language() -> str:
    """Retorna o idioma padrão da edição."""
    if is_int_edition():
        return "en_US"
    return "pt_BR"


def get_edition_currency_symbol() -> str:
    """Retorna o símbolo monetário padrão da edição."""
    if is_int_edition():
        return "$"
    return "R$"
