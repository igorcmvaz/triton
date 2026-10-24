# -*- coding: utf-8 -*-
"""Convenção numérica da interface (UI-22): «20.08 %» e «4,000 L» na Internacional em inglês.

Regra (``triton.core.numero``): fora da BRL, em inglês ou chinês, ponto decimal e vírgula de milhar;
em português e espanhol, e na BRL em qualquer idioma, vírgula decimal e ponto de milhar. O que a tela
mostra, a tela lê de volta: «4,000» na convenção en é 4000, nunca 4,0. O arquivo é o mesmo nas três
edições; o que depende da edição confere ``get_current_edition()``.
"""

from __future__ import annotations

import re

import pytest

from triton.core import numero as N
from triton.core.edition import get_current_edition, usa_dados_do_brasil
from triton.core.parser import format_ptbr, parse_float

try:
    from triton.ui import translation as T
except Exception:  # sem PySide6
    T = None

pytestmark = pytest.mark.skipif(T is None, reason="precisa de PySide6 (idioma da interface)")


class _idioma:
    def __init__(self, lang):
        self.lang = lang

    def __enter__(self):
        self.anterior = T._runtime_language
        T._runtime_language = self.lang

    def __exit__(self, *exc):
        T._runtime_language = self.anterior


def _formato_antigo(val, decimals=2, thousands=True):
    """O ``format_ptbr`` de antes (sempre brasileiro): a referência para a BRL e para o português."""
    if val is None:
        return "-"
    v = float(val)
    if thousands:
        return f"{v:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{v:.{decimals}f}".replace(".", ",")


VALORES = [0, 0.5, 4, 4000, 1234.5, 20.08, -1234.56, 999.999, 1000000.0, 12.3456, 0.0001, 123456.789]


# ── Quem usa qual convenção ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("idioma", ["pt", "es", "en", "zh"])
def test_convencao_por_edicao_e_idioma(idioma):
    with _idioma(idioma):
        esperado = (not usa_dados_do_brasil()) and idioma in ("en", "zh")
        assert N.usa_ponto_decimal() is esperado


# ── A BRL e o português não mudam ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("idioma", ["pt", "es"])
@pytest.mark.parametrize("casas", [0, 1, 2, 4])
@pytest.mark.parametrize("milhar", [True, False])
def test_portugues_e_espanhol_formatam_como_antes(idioma, casas, milhar):
    with _idioma(idioma):
        for v in VALORES:
            assert format_ptbr(v, casas, milhar) == _formato_antigo(v, casas, milhar)


def test_brl_em_ingles_segue_o_formato_brasileiro():
    if not usa_dados_do_brasil():
        pytest.skip("só a BRL")
    with _idioma("en"):
        assert format_ptbr(4000, 0) == "4.000"
        assert format_ptbr(1234.5, 2) == "1.234,50"


def test_funcoes_de_exibicao_em_portugues_sao_as_antigas():
    with _idioma("pt"):
        assert N.milhar("4,000 L; 1,234.5") == "4.000 L; 1.234.5"           # o replace global de antes
        assert N.ptbr("1,234.50") == "1.234,50"
        assert N.decimal("2.50") == "2,50"
        assert N.normalizar("2,5") == "2.5" and N.para_float("2,5") == 2.5
        assert N.para_float_milhar("1.234,5") == 1234.5
        assert N.normalizar_milhar("1.234,5") == "1234.5"


# ── Inglês fora da BRL: ponto decimal, vírgula de milhar ────────────────────────────────────

def _em_ingles():
    if usa_dados_do_brasil():
        pytest.skip("a BRL em inglês segue o formato brasileiro")
    return _idioma("en")


def test_ingles_formata_com_ponto_decimal():
    with _em_ingles():
        assert format_ptbr(20.08, 2) == "20.08"
        assert format_ptbr(4000, 0) == "4,000"
        assert format_ptbr(1234.5, 2) == "1,234.50"
        assert format_ptbr(4000.5, 1, thousands=False) == "4000.5"
        assert N.milhar("4,000 L") == "4,000 L"
        assert N.decimal("2.50") == "2.50"
        assert N.ptbr("1,234.50") == "1,234.50"


@pytest.mark.parametrize("idioma", ["en", "zh"])
def test_nunca_le_quatro_mil_como_quatro(idioma):
    if usa_dados_do_brasil():
        pytest.skip("a BRL em inglês segue o formato brasileiro")
    with _idioma(idioma):
        assert parse_float("4,000") == 4000.0
        assert N.para_float("4,000") == 4000.0
        assert N.para_float_milhar("4,000") == 4000.0
        assert float(N.normalizar("4,000")) == 4000.0
        assert parse_float("1,234,567.5") == 1234567.5
        assert parse_float("4.000") == 4.0                    # em inglês, ponto é decimal
        assert N.para_float("2,5") == 2.5                     # vírgula decimal digitada à brasileira: aceita
        assert N.para_float("1.234,5") == 1234.5              # idem, com milhar


def test_em_portugues_quatro_virgula_zero_zero_zero_continua_4():
    with _idioma("pt"):
        assert parse_float("4,000") == 4.0
        assert N.para_float("4,000") == 4.0


# ── Ida e volta: formatar → ler ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("idioma", ["pt", "es", "en", "zh"])
@pytest.mark.parametrize("milhar", [True, False])
def test_ida_e_volta_com_o_leitor_geral(idioma, milhar):
    with _idioma(idioma):
        for v in VALORES:
            for casas in (2, 4):
                texto = format_ptbr(v, casas, milhar)
                esperado = round(v, casas)
                assert parse_float(texto) == pytest.approx(esperado, abs=10 ** -casas), (idioma, texto, v)


@pytest.mark.parametrize("idioma", ["pt", "es", "en", "zh"])
def test_ida_e_volta_com_os_leitores_de_campo(idioma):
    """Os campos da interface lêem com ``para_float`` (ponto ou vírgula decimal) e as tabelas de custos com
    ``para_float_milhar`` (milhar escrito); ambos devolvem o número que a tela mostra."""
    with _idioma(idioma):
        for v in VALORES:
            sem_milhar = format_ptbr(v, 2, False)
            com_milhar = format_ptbr(v, 2, True)
            assert N.para_float(sem_milhar) == pytest.approx(round(v, 2), abs=0.005), (idioma, sem_milhar)
            assert N.para_float_milhar(com_milhar) == pytest.approx(round(v, 2), abs=0.005), (idioma, com_milhar)
            assert float(N.normalizar(sem_milhar)) == pytest.approx(round(v, 2), abs=0.005)
            assert float(N.normalizar_milhar(com_milhar)) == pytest.approx(round(v, 2), abs=0.005)


@pytest.mark.parametrize("idioma", ["pt", "en"])
def test_campo_preenchido_com_decimal_volta_igual(idioma):
    """O que os diálogos gravam nos campos (``decimal(f"{x:.2f}")``) é lido de volta sem perder o valor."""
    with _idioma(idioma):
        for v in (0.5, 12.34, 1234.56, 0.6957):
            assert N.para_float(N.decimal(f"{v:.4f}")) == pytest.approx(v)


# ── O seletor de volume dos laudos lê o que o rótulo mostra ─────────────────────────────────

@pytest.mark.parametrize("idioma", ["pt", "en"])
def test_seletor_de_volume_le_o_rotulo(idioma):
    from triton.ui.tab_reports_pdf import TabReportsPdf
    parse = TabReportsPdf._parse_volume_string
    with _idioma(idioma):
        for v in (500.0, 1000.0, 4000.0, 12000.0, 20000.0):
            rotulo = N.milhar(f"{v:,.0f} L (ótimo)")
            assert parse(None, rotulo) == v, (idioma, rotulo)


# ── Janela real ─────────────────────────────────────────────────────────────────────────────

def test_janela_mostra_a_convencao_do_idioma():
    from PySide6.QtWidgets import QApplication, QLabel, QMessageBox
    from pathlib import Path

    exemplos = {
        "BRL": "examples/estudo_caso_1_florianopolis1.triton",
        "INT": "examples/new_york.triton",
        "IBE": "examples/portugal/lisboa.triton",
    }
    caminho = Path(__file__).resolve().parents[2] / exemplos[get_current_edition()]
    if not caminho.is_file():
        pytest.skip("sem exemplo")
    app = QApplication.instance() or QApplication([])
    mp = pytest.MonkeyPatch()
    for nome in ("information", "warning", "critical"):
        mp.setattr(QMessageBox, nome, staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok))
    try:
        from triton.ui.main_window import MainWindow
        resultados = {}
        for idioma in ("pt", "en"):
            with _idioma(idioma):
                janela = MainWindow()
                janela.on_load_simulation(str(caminho))
                janela.on_step_changed(4)
                textos = " ".join(w.text() for w in janela.tab_charts.findChildren(QLabel))
                resultados[idioma] = textos
        ponto = bool(re.search(r"\b\d+\.\d{2} ?%", resultados["en"]))
        virgula = bool(re.search(r"\b\d+,\d{2} ?%", resultados["en"]))
        if usa_dados_do_brasil():
            assert virgula and not ponto, "a BRL em inglês segue o formato brasileiro"
        else:
            assert ponto and not virgula, resultados["en"][:300]
        assert re.search(r"\b\d+,\d{2} ?%", resultados["pt"]), "em português a vírgula decimal continua"
    finally:
        mp.undo()
