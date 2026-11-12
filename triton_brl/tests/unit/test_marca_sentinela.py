"""Sentinela: com ``marca.NOME`` trocado, o que o usuário vê mostra o nome novo, e nunca «Triton».

Ensaia o dia da troca do nome sem mexer em arquivo nenhum: ``monkeypatch`` põe um nome que não
existe em lugar nenhum («Zyx 9») e as superfícies visíveis são conferidas: o catálogo da interface
(``tr``), a ajuda da linha de comando, o título da janela e o nome da aplicação, as páginas da aba
de Documentação e um laudo. O que ficar com «Triton» (fora de caminhos e identificadores, que
``marca.aplicar`` não toca) escapou do ponto de passagem.
"""
from __future__ import annotations

import sys

import pytest

pytest.importorskip("PySide6.QtWidgets", reason="tr e a interface exigem PySide6")

from triton import marca  # noqa: E402

SENTINELA = "Zyx 9"


@pytest.fixture
def nome_novo(monkeypatch):
    monkeypatch.setattr(marca, "NOME", SENTINELA)
    return SENTINELA


@pytest.fixture(scope="module")
def qapp():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


def _sobra(texto: str) -> str | None:
    """O trecho com o nome antigo fora de caminho/identificador, ou None."""
    m = marca._padrao().search(texto or "")
    return None if m is None else texto[max(0, m.start() - 40):m.end() + 40]


def test_tr_de_todas_as_entradas_dos_catalogos(nome_novo):
    from triton.ui import translation as T
    chaves = set(T._DICTIONARY) | set(T._SPANISH_DICTIONARY) | set(T._CHINESE_DICTIONARY)
    sobras, sem_sentinela = [], []
    for chave in sorted(chaves):
        for lang in ("pt", "en", "es", "zh"):
            saida = T.tr(chave, lang)
            if _sobra(saida):
                sobras.append((lang, chave[:60], _sobra(saida)))
            if _sobra(T._traduz_do_catalogo(chave, lang)) and SENTINELA not in saida.replace(SENTINELA.upper(), SENTINELA):
                sem_sentinela.append((lang, chave[:60]))
    assert not sobras, sobras[:10]
    assert not sem_sentinela, sem_sentinela[:10]


def _ajuda(monkeypatch, capsys, *argv) -> str:
    from triton import cli
    monkeypatch.setattr(sys, "argv", ["cli.py", *argv])
    with pytest.raises(SystemExit):
        cli.main()
    return capsys.readouterr().out


def test_ajuda_da_linha_de_comando(nome_novo, monkeypatch, capsys):
    principal = _ajuda(monkeypatch, capsys, "--help")
    assert SENTINELA in principal and not _sobra(principal), principal[:400]
    sub = _ajuda(monkeypatch, capsys, "init", "--help")
    assert "usage:" in sub and not _sobra(sub), sub[:400]


def test_titulo_da_janela_e_nome_da_aplicacao(nome_novo, qapp):
    from triton.core.edition import get_edition_title, nome_da_aplicacao
    from triton.ui.main_window import MainWindow
    janela = MainWindow()
    try:
        assert SENTINELA in janela.windowTitle() and not _sobra(janela.windowTitle())
        assert get_edition_title().startswith(SENTINELA) and not _sobra(get_edition_title())
        assert nome_da_aplicacao().startswith(SENTINELA + " (")
        from PySide6.QtGui import QAction
        menus = [a.text() for a in janela.findChildren(QAction)]
        assert any(SENTINELA in t for t in menus)          # «Sobre o …», «Como Citar o …»
        assert not [t for t in menus if _sobra(t)]
    finally:
        janela.close()
        janela.deleteLater()


def test_paginas_da_aba_de_documentacao(nome_novo, qapp):
    from PySide6.QtWidgets import QLabel, QTextBrowser
    from triton.ui.tab_documentation import TabDocumentation
    aba = TabDocumentation()
    paginas = [b.toPlainText() for b in aba.findChildren(QTextBrowser)]
    rotulos = [r.text() for r in aba.findChildren(QLabel)]
    topicos = [aba.list_topics.item(i).text() for i in range(aba.list_topics.count())]
    assert any(SENTINELA in p for p in paginas)
    assert not [p for p in paginas + rotulos + topicos if _sobra(p)], \
        [_sobra(p) for p in paginas + rotulos + topicos if _sobra(p)][:5]


def test_laudo_executivo(nome_novo):
    from triton.core.report_generator import generate_executive_html_report
    html = generate_executive_html_report({
        "ref_code": "REF-TESTE-1", "rain_file": "chuva.csv", "area": 250.0, "runoff": 0.85,
        "discard": 2.0, "residents": 5, "demand": 150.0, "share": 0.40, "lower_vol": 5000.0,
        "potential_pct": 35.5, "pluv_day": 120.0, "potable_day": 180.0, "spill_day": 40.0,
        "sat_full": 80.0, "sat_null": 10.0, "capex": 9500.0, "annual_gross": 3200.0,
        "vpl": 28500.0, "tir": 26.5, "payback_s": "4,1", "payback_d": "5,5",
    })
    assert SENTINELA in html and not _sobra(html), _sobra(html)
