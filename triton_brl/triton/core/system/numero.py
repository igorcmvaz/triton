# -*- coding: utf-8 -*-
"""Convenção numérica da interface: ponto único para mostrar e ler números.

Duas convenções:

* **pt/es (vírgula decimal)**: «1.234,56». É a da BRL em qualquer idioma, e a de qualquer edição em
  português ou espanhol.
* **en/zh (ponto decimal)**: «1,234.56». Vale fora da BRL quando a interface está em inglês ou chinês
  (a Internacional abre em inglês; a BRL em inglês segue o formato brasileiro, como o laudo dela).

Os valores dos cálculos não passam por aqui: só o texto que se mostra e o texto que o usuário digita.
O que a tela mostra, a tela lê de volta: ``«4,000»`` na convenção en é 4000, e nunca 4,0.

Em português (a BRL e a IBE) todas as funções devolvem exatamente o que o código antigo devolvia
(``.replace(',', '.')`` e companhia), de modo que nada muda ali.
"""

from __future__ import annotations

import re

_MILHAR_EN = re.compile(r"^[+-]?\d{1,3}(,\d{3})+(\.\d*)?$")


_provedor_do_idioma = []


def registrar_idioma(funcao) -> None:
    """A interface diz aqui como saber o idioma atual (``triton.ui.translation`` se registra ao ser importada).
    O núcleo não importa a interface: sem ela registrada (CLI mínima, CI sem Qt), o idioma é o português."""
    _provedor_do_idioma[:] = [funcao]


def _idioma() -> str:
    if not _provedor_do_idioma:
        # CLI sem interface: a Internacional é em inglês (convenção «1,234.56»); as demais, em português.
        from triton.core.edition import is_int_edition
        return "en" if is_int_edition() else "pt"
    try:
        return _provedor_do_idioma[0]()
    except Exception:
        return "pt"


def usa_ponto_decimal() -> bool:
    """True quando a interface mostra «1,234.56» (fora da BRL, em inglês ou chinês)."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        return False
    return _idioma() in ("en", "zh")


# ── Mostrar ──────────────────────────────────────────────────────────────────────────────────

def formatar(valor, casas: int = 2, milhar: bool = True) -> str:
    """O número no formato da interface: «1.234,56» (pt/es) ou «1,234.56» (en/zh)."""
    if valor is None:
        return "-"
    try:
        v = float(valor)
        if usa_ponto_decimal():
            return f"{v:,.{casas}f}" if milhar else f"{v:.{casas}f}"
        if milhar:
            return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{v:.{casas}f}".replace(".", ",")
    except Exception:
        return str(valor)


def milhar(texto: str) -> str:
    """Um texto montado com ``f"{x:,.0f}"`` (milhar em vírgula): em pt/es troca por ponto, em en/zh deixa."""
    return texto if usa_ponto_decimal() else texto.replace(",", ".")


def ptbr(texto: str) -> str:
    """Um texto montado com ``f"{x:,.2f}"`` (formato en do Python): em pt/es vira «1.234,56»; em en/zh fica."""
    if usa_ponto_decimal():
        return texto
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


# ── Ler ──────────────────────────────────────────────────────────────────────────────────────

def _normaliza(texto: str, estrito_pt: bool) -> str:
    s = str(texto).strip()
    if usa_ponto_decimal():
        if _MILHAR_EN.match(s):
            return s.replace(",", "")          # «4,000» é 4000; «1,234.5» é 1234,5
        if "," in s and "." not in s:
            return s.replace(",", ".")         # «2,5» digitado com vírgula decimal: aceito
        if "," in s and "." in s and s.rfind(",") > s.rfind("."):
            return s.replace(".", "").replace(",", ".")   # «1.234,5»: quem digita à brasileira
        return s.replace(",", "")
    if estrito_pt:
        return s.replace(".", "").replace(",", ".")
    return s.replace(",", ".")


def para_float(texto) -> float:
    """``float(texto.replace(',', '.'))`` em pt/es; em en/zh lê «4,000» como 4000. Levanta ValueError como ``float``."""
    return float(_normaliza(texto, estrito_pt=False))


def para_float_milhar(texto) -> float:
    """``float(texto.replace('.', '').replace(',', '.'))`` em pt/es (ponto é milhar); em en/zh, convenção en."""
    return float(_normaliza(texto, estrito_pt=True))


def normalizar(texto) -> str:
    """O texto numérico na forma que ``float`` lê: em pt/es, o que ``.replace(',', '.')`` dava; em en/zh, sem o milhar."""
    return _normaliza(texto, estrito_pt=False)


def normalizar_milhar(texto) -> str:
    """Como ``normalizar``, mas em pt/es o ponto é milhar (o que ``.replace('.', '').replace(',', '.')`` dava)."""
    return _normaliza(texto, estrito_pt=True)


def decimal(texto: str) -> str:
    """Um texto montado com ``f"{x:.2f}"`` (ponto decimal do Python): em pt/es troca por vírgula; em en/zh deixa."""
    return texto if usa_ponto_decimal() else texto.replace(".", ",")


_LOCALE_DO_SISTEMA = []


def aplicar_locale() -> None:
    """Põe o ``QLocale`` padrão do Qt na convenção da interface: spin boxes e validadores mostram o separador
    que o resto da tela mostra. Em inglês/chinês fora da BRL, inglês do Reino Unido (ponto decimal, vírgula de
    milhar), mesmo num Windows em português; nos demais casos, o locale que o sistema tinha (nada muda)."""
    try:
        from PySide6.QtCore import QLocale
    except Exception:
        return
    if not _LOCALE_DO_SISTEMA:
        _LOCALE_DO_SISTEMA.append(QLocale())
    if usa_ponto_decimal():
        if _idioma() == "zh":
            QLocale.setDefault(QLocale(QLocale.Chinese, QLocale.China))
        else:
            QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedKingdom))
    else:
        QLocale.setDefault(_LOCALE_DO_SISTEMA[0])


def locale_da_interface():
    """O ``QLocale`` dos campos que antes eram fixos em português do Brasil: pt-BR em pt/es e na BRL (como
    sempre); o locale padrão (en-GB) em inglês/chinês fora da BRL."""
    from PySide6.QtCore import QLocale
    if usa_ponto_decimal():
        return QLocale()
    return QLocale(QLocale.Portuguese, QLocale.Brazil)
