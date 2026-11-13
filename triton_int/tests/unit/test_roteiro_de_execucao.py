# -*- coding: utf-8 -*-
"""Defeitos achados no roteiro de execução da interface (24/10/2026), um teste para cada.

O roteiro abriu cada exemplo da edição na janela real (offscreen), percorreu as etapas e conferiu os
textos nos quatro idiomas. Achou texto em português na interface inglesa (unidades, rótulos
montados na tela, a frase da decisão multicritério), a norma brasileira na tabela de custos da INT
e da IBE, nome de projeto cortado no cabeçalho e português do Brasil num laudo da IBE.

O arquivo é o mesmo nas três edições. Cada teste abre o exemplo da própria edição (BRL: estudo de caso 1;
INT: Nova York; IBE: Lisboa); o que só vale fora da BRL (a norma NBR) confere ``usa_dados_do_brasil()``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QMessageBox, QTableWidget  # noqa: E402

from triton.core.edition import get_current_edition, usa_dados_do_brasil  # noqa: E402
from triton.ui import translation as T  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]

_EXEMPLO_POR_EDICAO = {
    "BRL": RAIZ / "examples" / "estudo_caso_1_florianopolis1.triton",
    "INT": RAIZ / "examples" / "new_york.triton",
    "IBE": RAIZ / "examples" / "portugal" / "lisboa.triton",
}
EXEMPLO = _EXEMPLO_POR_EDICAO.get(get_current_edition())

sem_exemplo = pytest.mark.skipif(EXEMPLO is None or not EXEMPLO.is_file(), reason="sem exemplo nesta edição")


# ── Auxiliares (únicos para o arquivo) ───────────────────────────────────────────────────────

def _textos_das_tabelas(widget) -> str:
    """Tudo o que as tabelas sob o widget mostram, em uma só cadeia."""
    partes = []
    for tabela in widget.findChildren(QTableWidget):
        for c in range(tabela.columnCount()):
            it = tabela.horizontalHeaderItem(c)
            partes.append(it.text() if it else "")
        for r in range(tabela.rowCount()):
            for c in range(tabela.columnCount()):
                it = tabela.item(r, c)
                partes.append(it.text() if it else "")
    return "\n".join(partes)


@pytest.fixture(scope="module")
def _app():
    return QApplication.instance() or QApplication([])


@pytest.fixture(scope="module")
def _sem_dialogos():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ("information", "warning", "critical"):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, "question", staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    yield
    mp.undo()


def _abre_exemplo(idioma: str):
    """A janela com o exemplo da edição aberto, no idioma pedido; economia e decisão já calculadas.

    O idioma vai direto no estado do módulo (sem ``set_current_lang``): o teste não grava nas
    preferências do usuário.
    """
    from triton.ui.main_window import MainWindow

    anterior = T._runtime_language
    T._runtime_language = idioma
    try:
        janela = MainWindow()
        janela.on_load_simulation(str(EXEMPLO))
        for etapa in (5, 7, 4):  # economia, decisão multicritério, resultados técnicos
            janela.on_step_changed(etapa)
        return janela
    finally:
        T._runtime_language = anterior


@pytest.fixture(scope="module")
def janela_en(_app, _sem_dialogos):
    return _abre_exemplo("en")


@pytest.fixture(scope="module")
def janela_pt(_app, _sem_dialogos):
    return _abre_exemplo("pt")


class _idioma:
    """``with _idioma("en"):`` — o idioma da interface só durante o bloco (sem gravar preferências)."""

    def __init__(self, lang):
        self.lang = lang

    def __enter__(self):
        self.anterior = T._runtime_language
        T._runtime_language = self.lang

    def __exit__(self, *exc):
        T._runtime_language = self.anterior


# ── Catálogo e unidades (independem da edição) ──────────────────────────────────────────────

def test_unidades_por_ano_dia_mes_seguem_o_idioma():
    anterior = T._runtime_language
    try:
        texto = "18,0 m³/ano; 168 L/dia; R$ 3/mês; 1/diário"
        T._runtime_language = "pt"
        assert T.un(texto) == texto
        T._runtime_language = "en"
        assert T.un(texto) == "18,0 m³/year; 168 L/day; R$ 3/month; 1/diário"
        T._runtime_language = "es"
        assert T.un(texto) == "18,0 m³/año; 168 L/día; R$ 3/mes; 1/diário"
        T._runtime_language = "zh"
        assert T.un(texto) == "18,0 m³/年; 168 L/日; R$ 3/月; 1/diário"
    finally:
        T._runtime_language = anterior


FRASES_DO_ROTEIRO = (
    "Cisterna de {0} L", "Cloro Ativo", "kg/ano", "m³/ano", "Triton (regra do programa)",
    "Inspeção e limpeza de calhas/pré-filtro", "Limpeza e inspeção do reservatório",
    "Limpeza e higienização do reservatório", "Manutenção preventiva da motobomba",
    "pesos ponderados: {0}% Técnico, {1}% Econômico, {2}% Ambiental",
    "Economia Financeira Estimada", "Sem Atendimento (Dias Secos)", "Economia Bruta (1º Ano)",
    "Classe 1: parâmetros mínimos da NBR 15527:2019",
    "Classe 2 (adaptada, não normativa): Irrigação de Jardins e Lavagem de Pisos/Veículos",
    "Classe 3 (adaptada, não normativa): Torres de Resfriamento e Caldeiras Industriais",
    "Classe 4 (adaptada, não normativa): Lavagem de Roupas e Usos Nobres Não Potáveis",
)


@pytest.mark.parametrize("idioma", ["en", "es", "zh"])
def test_frases_do_roteiro_tem_traducao(idioma):
    for chave in FRASES_DO_ROTEIRO:
        traduzida = T.tr(chave, lang=idioma)
        assert traduzida != chave, f"{chave!r} sem tradução em {idioma}"
        assert not re.search(r"[ãõç]|\b(ano|dia)s?\b", traduzida), f"{chave!r} em {idioma} ainda tem português: {traduzida!r}"


def test_frase_da_decisao_tem_os_treze_campos_em_todos_os_idiomas():
    """A frase da faixa de escolha (0.2.0) leva treze campos; faltando um, a tradução quebra o format."""
    from triton.ui.translation_complement import COMPLEMENTO
    chave = next(k for k in COMPLEMENTO if k.startswith("No TOPSIS ({0}), as cisternas de {1}"))
    for idioma in ("pt", "en", "es", "zh"):
        texto = T.tr(chave, lang=idioma)
        for i in range(13):
            assert "{%d}" % i in texto, f"{idioma}: falta {{{i}}}"
        assert texto.format(*["x"] * 13)


def test_glossario_de_portugal_regista_e_equipa():
    from triton.ui.portugues_de_portugal import para_portugal
    saida = para_portugal("O relatório registra as equações. A equipe do estudo registrar dados; as equipes registram.")
    assert "regista as equações" in saida and "A equipa do estudo" in saida
    assert "registar dados" in saida and "as equipas registam" in saida
    assert "equipe" not in saida and "registra " not in saida


# ── Janela real: o exemplo da edição, em inglês e em português ──────────────────────────────

@sem_exemplo
def test_decisao_multicriterio_em_ingles_sem_portugues(janela_en):
    otimizador = janela_en.tab_global_optimizer
    frase = otimizador.lbl_tradeoff_desc.text()
    # 0.2.0: a frase dá a faixa de escolha, e não um volume «recomendado».
    assert "have similar scores" in frase and "cistern" in frase, frase
    assert not re.search(r"recomenda|semelhante|simulações|cisterna", frase), frase
    rotulo = otimizador.table.item(0, 0).text()
    assert rotulo.startswith("Option 1 ("), rotulo


@sem_exemplo
def test_decisao_multicriterio_em_portugues_nao_troca_virgula_por_ponto(janela_pt):
    frase = janela_pt.tab_global_optimizer.lbl_tradeoff_desc.text()
    # 0.2.0: a frase dá a faixa de escolha, e não um volume «recomendado».
    assert "as cisternas de" in frase and "têm escores semelhantes" in frase, frase
    # escore e aceitabilidade com vírgula decimal; antes saía «0.94» no meio do português
    assert re.search(r"maior escore em \d+ L, \d,\d\d\)", frase), frase
    # antes: VPL «2.428.94», porque um replace global trocava toda vírgula
    assert not re.search(r"\d\.\d{3}\.\d{2}\b", frase), frase
    rotulo = janela_pt.tab_global_optimizer.table.item(0, 0).text()
    assert rotulo.startswith("Opção 1 ("), rotulo


@sem_exemplo
def test_tabela_de_custos_em_ingles_sem_portugues_nem_norma_estrangeira(janela_en):
    economica = janela_en.tab_economic
    titulo = economica.gb_res.title()
    assert "Cisterna" not in titulo and "Cistern" in titulo, titulo
    texto = _textos_das_tabelas(economica)
    for termo in ("Cloro Ativo", "kg/ano", "Inspeção", "Limpeza", "Manutenção", "Descarte", "parâmetros mínimos"):
        assert termo not in texto, f"{termo!r} na tabela de custos em inglês"
    assert "Active chlorine" in texto
    if not usa_dados_do_brasil():
        assert "NBR" not in texto, "norma brasileira na tabela de custos fora da Brasil"


@sem_exemplo
def test_tabela_de_custos_em_portugues_fora_da_brasil_nao_cita_a_nbr(janela_pt):
    texto = _textos_das_tabelas(janela_pt.tab_economic)
    assert "Cloro Ativo" in texto or "Cloro ativo" in texto   # o português segue igual
    if not usa_dados_do_brasil():
        assert "NBR" not in texto
    else:
        assert "NBR 15527" in texto  # na BRL a norma continua citada


@sem_exemplo
def test_regra_operacional_traduzida_na_etapa_5(janela_en, janela_pt):
    assert janela_en.tab_charts.val_phi_rule.text() == "Triton (program rule)"
    assert janela_pt.tab_charts.val_phi_rule.text() == "Triton (regra do programa)"


@sem_exemplo
def test_cartoes_de_qualidade_da_etap_em_ingles_com_unidades_em_ingles(janela_en):
    qualidade = janela_en.tab_water_quality
    with _idioma("en"):
        qualidade.recalculate_all()
    from PySide6.QtWidgets import QLabel
    textos = " ".join(w.text() for w in qualidade.findChildren(QLabel))
    assert "/ano" not in textos and "/dia" not in textos, "unidade em português nos cartões da ETAP em inglês"
    assert "m³/year" in textos


@sem_exemplo
def test_nome_do_projeto_aberto_mostra_o_comeco_do_nome(janela_pt):
    campo = janela_pt.txt_workspace_project
    assert len(campo.text()) > 3
    assert campo.cursorPosition() == 0, "o campo mostra só o fim do nome do projeto"


# ── Linha de comando ─────────────────────────────────────────────────────────────────────────

@sem_exemplo
def test_cli_diz_onde_gravou_na_lingua_da_edicao(tmp_path, monkeypatch, capsys):
    """«Resultado salvo em:» saía em português do Brasil também na INT (inglês) e na IBE (Portugal)."""
    import sys

    from triton import cli

    saida = tmp_path / "resultado.json"
    monkeypatch.setattr(sys, "argv", ["triton", "run", str(EXEMPLO), "--format", "json", "--output", str(saida)])
    cli.main()
    texto = capsys.readouterr().out
    esperado = {"BRL": "Resultado salvo em:", "INT": "Result saved to:", "IBE": "Resultado guardado em:"}[get_current_edition()]
    assert esperado in texto, texto
    assert saida.is_file()


# ── Segunda rodada: rotinas de manutenção, cabeçalhos cortados, textos residuais ────────────

@sem_exemplo
def test_apagar_as_rotinas_nao_traz_de_volta_custo_de_outra_regiao(janela_pt):
    """Sem rotinas, a Etapa 6 repovoava a lista com os custos de referência em reais, também na INT e na IBE."""
    economica = janela_pt.tab_economic
    cfg = economica._internal_config
    cfg.op_costs = []
    novo = economica.get_triton_config()
    assert novo.op_costs, "as rotinas voltam (nome e periodicidade)"
    custos = [(fixo, variavel) for _n, _m, fixo, variavel in novo.op_costs]
    if usa_dados_do_brasil():
        assert any(f > 0 for f, _v in custos), "na BRL os custos de referência continuam"
    else:
        assert all(f == 0 and v == 0 for f, v in custos), custos


@sem_exemplo
def test_titulo_e_cabecalhos_nao_sao_cortados_em_1500_px(_app, _sem_dialogos):
    from PySide6.QtWidgets import QLabel
    anterior = T._runtime_language
    T._runtime_language = "pt"
    try:
        from triton.ui.main_window import MainWindow
        w = MainWindow()
        w.resize(1500, 950)
        w.show()
        w.on_load_simulation(str(EXEMPLO))
        for etapa, titulo in ((5, "Economia e viabilidade financeira"), (6, "Desempenho ambiental e ESG")):
            w.on_step_changed(etapa)
            _app.processEvents()
            alvo = T.tr(titulo)
            rotulo = next(l for l in w.stack.widget(etapa).findChildren(QLabel) if l.text() == alvo)
            assert rotulo.width() >= rotulo.sizeHint().width(), f"título cortado na etapa {etapa + 1}"
        tabela = w.tab_environmental.table_icv
        cab = tabela.horizontalHeader()
        assert all(cab.sectionSize(i) >= 120 for i in range(tabela.columnCount())), [cab.sectionSize(i) for i in range(5)]
    finally:
        T._runtime_language = anterior


@pytest.mark.parametrize("idioma", ["es", "zh"])
def test_descricao_do_descarte_nao_fica_em_duas_linguas(idioma):
    texto = "Reservatório Estanque de Descarte em PEAD Rotomoldado (300 L) com Extravasor Superior, Boia Flutuante de Vedação e Purga Lenta Calibrada"
    saida = T.tr(texto, lang=idioma)
    assert "Reservatório" not in saida and "Extravasor" not in saida and "Boia" not in saida, saida
    assert "300 L" in saida


@sem_exemplo
def test_procedencia_do_tarifario_ibe_em_ingles():
    if get_current_edition() != "IBE":
        pytest.skip("só a IBE tem o tarifário por concelho")
    from triton.core import tarifarios_portugal as tp
    from triton.ui.textos_da_edicao import traduz_descritivo
    with _idioma("en"):
        saida = traduz_descritivo(tp.procedencia("Lisboa"))
    assert "documentos oficiais" not in saida and "entidades gestoras" not in saida, saida
    assert "official documents" in saida
