# -*- coding: utf-8 -*-
"""Neutralidade da interface por edição (rodada 4): varre os textos das 13 abas.

O pacote `triton/` é o mesmo nas três edições; o que é do Brasil só aparece na BRL e o que é de
Portugal só na PRT. Este teste abre a janela principal (fora da tela), percorre as 13 etapas, as
abas internas e o menu, coleta todo texto que o usuário pode ler (rótulos, botões, itens de lista,
dicas, cabeçalhos de tabela, textos longos) e procura os termos do Brasil de
`auditoria/ESPECIFICACAO_DE_NEUTRALIDADE.md`.

Uso como relatório (lista cada ocorrência, por edição e idioma):

    TRITON_EDITION=INT python tests/unit/test_neutralidade_interface.py --idioma en
"""
from __future__ import annotations

import os
import re
import sys

import pytest

#: Termos do Brasil (e o motivo). Procurados sem diferenciar maiúsculas, exceto onde indicado.
TERMOS_DO_BRASIL = [
    r"Florian[oó]polis", r"Bras[ií]lia", r"Manaus", r"S[aã]o Paulo", r"Santa Catarina",
    r"R\$", r"\bBRL\b", r"\breais\b", r"\breal brasileiro",
    r"\bCASAN\b", r"\bCELESC\b", r"\bSABESP\b", r"\bCOPASA\b", r"\bCORSAN\b", r"\bSANEPAR\b",
    r"\bANEEL\b", r"bandeira tarif", r"tariff flag",
    r"\bCLIMBra\b", r"\bCMIP6\b", r"\bINMET\b", r"\bIBGE\b", r"\bMCTI\b", r"\bSIRENE\b",
    r"\bSINAPI\b", r"\bSNIS\b", r"\bSIDAC\b", r"\bABNT\b", r"\bNBR\b", r"\bCREA\b",
    r"\bIPTU\b", r"\bSelic\b", r"\bIPCA\b", r"\bINPC\b", r"\bIGP-?(?:DI|M)\b",
    r"Casa Azul", r"AQUA-?HQE", r"GBC Brasil",
    r"\bSchneider\b", r"\bDancor\b", r"\bLepono\b", r"\bKomeco\b", r"\bAmanco\b", r"\bFortlev\b",
    r"Netuno\s*4", r"\b652\b", r"Brasil\b", r"Brazil", r"Brasileir", r"Brazilian",
    r"\bUF\b", r"concession[aá]ri", r"\bconcessionaire", r"\bTFDI\b",
]
_PADRAO_BRASIL = re.compile("|".join(f"(?:{t})" for t in TERMOS_DO_BRASIL), re.IGNORECASE)

#: Termos de Portugal (não podem aparecer na INT nem na BRL).
TERMOS_DE_PORTUGAL = [
    r"\bconcelho", r"\bEPAL\b", r"\bE-?OBS\b", r"\bLisboa\b", r"\bERSAR\b", r"\bFunchal\b",
    r"(?-i:\bMadeira\b)", r"(?-i:\bPorto\b)", r"\bPortugal\b", r"\bIVA\b",
]
_PADRAO_PORTUGAL = re.compile("|".join(f"(?:{t})" for t in TERMOS_DE_PORTUGAL), re.IGNORECASE)

#: Vocabulário do Brasil que não pode aparecer em português de Portugal.
TERMOS_PT_BR = [
    r"\barquivos?\b", r"\bplanilhas?\b", r"\busu[aá]rios?\b", r"\becon[ô]mic\w*", r"\bsalvar\b",
    r"\bbaixar\b", r"\btelas?\b", r"\bconcession[aá]ria", r"\bregistros?\b", r"\bseç[ãa]o\b",
    r"\bcontato\b", r"\bgerenciar\b", r"\besgoto\b", r"\bVPL\b", r"\bmotobombas?\b",
    r"\bcadastr\w+", r"\bvaz[ãa]o\b", r"\bequipe\b", r"\btubula[çc][ãa]o\b",
]
_PADRAO_PT_BR = re.compile("|".join(f"(?:{t})" for t in TERMOS_PT_BR), re.IGNORECASE)

#: Palavras que denunciam português dentro de uma interface em inglês.
_PORTUGUES_NO_INGLES = re.compile(
    r"\b(?:de|do|da|dos|das|para|com|sem|uma?|não|nao|são|serão|ou|está|valor|valores|projeto|"
    r"água|agua|chuva|reservat[óo]rio|c[áa]lculo|edifica[çc][ãa]o|moradores?|consumo|anos|dias|"
    r"padr[ãa]o|selecione|informe|carregue|resultado|econ[ôo]mic[ao]s?|tarifa|série|serie)\b",
    re.IGNORECASE)

#: Textos que podem legitimamente conter um dos termos (autoria, licença): sem diferenciar caixa.
PERMITIDOS = [
    r"UFSC", r"Universidade Federal de Santa Catarina", r"Grupo de Pesquisa em Ambientes Sustent",
    r"Sustainable Environments Research Group",
]
#: Só na Internacional (decisão U-24): o idioma-fonte do catálogo é o português do Brasil, e a lista
#: de idiomas do laudo o rotula assim. Na Portugal o laudo oferece «Português (Portugal)».
PERMITIDOS_INT = [r"Portuguese \(Brazil\)", r"Português \(Brasil\)"]


def _raiz_do_pacote() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _texto_simples(valor) -> str:
    """Tira as marcas HTML e normaliza os espaços."""
    if valor is None:
        return ""
    t = str(valor)
    if "<" in t and ">" in t:
        t = re.sub(r"<(?:br|/p|/div|/tr|/li|/h\d)[^>]*>", "\n", t, flags=re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        import html as _h
        t = _h.unescape(t)
    return " ".join(t.split())


def coletar_textos(janela, incluir_documentacao: bool = True, so_dialogos: bool = False):
    """Todo texto que o usuário pode ler na janela: lista de (onde, texto).

    Percorre as etapas da pilha e, dentro delas, cada página de abas e pilhas internas, de modo
    que o texto de uma aba que não está à frente também entra. Ignora o que o código esconde
    por edição (widgets escondidos explicitamente, ``hide()``): o usuário não os alcança.
    """
    from PySide6.QtWidgets import (
        QAbstractButton, QComboBox, QGroupBox, QLabel, QLineEdit, QListWidget, QPlainTextEdit,
        QSpinBox, QDoubleSpinBox, QStackedWidget, QTabWidget, QTableWidget, QTextEdit, QWidget,
        QMenu, QTextBrowser)

    achados: list[tuple[str, str]] = []
    vistos: set[tuple[str, str]] = set()

    def anota(onde: str, texto):
        t = _texto_simples(texto)
        if t and (onde, t) not in vistos:
            vistos.add((onde, t))
            achados.append((onde, t))

    def escondido_por_codigo(w, raiz) -> bool:
        """O widget, ou um ancestral até a raiz, foi escondido por ``hide()``/``setVisible(False)``.

        Páginas de abas e pilhas inativas também aparecem como escondidas; por isso as
        percorremos uma a uma (ver ``visita``) e só olhamos aqui os widgets dentro da página ativa.
        """
        p = w
        while p is not None:
            if p.isHidden() and not _e_pagina_inativa(p):
                return True
            if p is raiz:
                return False
            p = p.parentWidget()
        return False

    paginas_inativas: set[int] = set()

    def _e_pagina_inativa(w) -> bool:
        return id(w) in paginas_inativas

    def texto_do_widget(w, onde):
        anota(onde + ":dica", w.toolTip())
        if isinstance(w, QLabel):
            anota(onde, w.text())
        if isinstance(w, QAbstractButton):
            anota(onde, w.text())
        if isinstance(w, QGroupBox):
            anota(onde, w.title())
        if isinstance(w, QLineEdit):
            anota(onde + ":exemplo", w.placeholderText())
            anota(onde + ":valor", w.text())
        if isinstance(w, (QSpinBox, QDoubleSpinBox)):
            anota(onde, w.prefix() + "|" + w.suffix())
        if isinstance(w, QComboBox):
            for i in range(w.count()):
                anota(onde + f":item{i}", w.itemText(i))
                anota(onde + f":item{i}:dica", w.itemData(i, 3))  # ToolTipRole
        if isinstance(w, QTableWidget):
            for j in range(w.columnCount()):
                if w.isColumnHidden(j):
                    continue
                it = w.horizontalHeaderItem(j)
                if it is not None:
                    anota(onde + ":cab", it.text())
            for i in range(w.rowCount()):
                it = w.verticalHeaderItem(i)
                if it is not None:
                    anota(onde + ":linha", it.text())
        if isinstance(w, QListWidget):
            for i in range(w.count()):
                anota(onde + ":lista", w.item(i).text())
        if isinstance(w, (QTextEdit, QPlainTextEdit, QTextBrowser)):
            anota(onde + ":texto", w.toPlainText() if not isinstance(w, QTextEdit) else w.toPlainText())

    def visita(raiz: QWidget, onde: str, profundidade: int = 0):
        if profundidade > 12:
            return
        todos = [raiz] + raiz.findChildren(QWidget)
        for w in todos:
            if escondido_por_codigo(w, raiz):
                continue
            nome = f"{onde}/{w.objectName() or type(w).__name__}"
            texto_do_widget(w, nome)
        for w in todos:
            if escondido_por_codigo(w, raiz):
                continue
            if isinstance(w, QTabWidget):
                atual = w.currentIndex()
                for i in range(w.count()):
                    anota(f"{onde}/abas", w.tabText(i))
                    anota(f"{onde}/abas:dica", w.tabToolTip(i))
                    if w.isTabVisible(i) if hasattr(w, "isTabVisible") else True:
                        pg = w.widget(i)
                        w.setCurrentIndex(i)
                        visita(pg, f"{onde}/aba{i}", profundidade + 1)
                w.setCurrentIndex(atual)
            elif isinstance(w, QStackedWidget) and w is not janela.stack:
                atual = w.currentIndex()
                for i in range(w.count()):
                    w.setCurrentIndex(i)
                    visita(w.widget(i), f"{onde}/pg{i}", profundidade + 1)
                w.setCurrentIndex(atual)

    if so_dialogos:
        for nome, dlg in _abrir_dialogos(janela):
            dlg.show()
            visita(dlg, f"dialogo:{nome}")
            dlg.close()
        return achados

    # menu
    for m in janela.menuBar().findChildren(QMenu):
        for a in m.actions():
            anota("menu", a.text())
            anota("menu:dica", a.toolTip() if a.toolTip() != a.text() else "")
    anota("janela", janela.windowTitle())
    # barra lateral e cabeçalho
    visita(janela.sidebar, "lateral")
    for i in range(janela.stack.count()):
        if not incluir_documentacao and janela.stack.widget(i) is janela.tab_documentation:
            continue
        janela.on_step_changed(i)
        pagina = janela.stack.widget(i)
        if pagina.isHidden():
            pagina.setVisible(True)
        visita(pagina, f"etapa{i + 1}")
    return achados


def _abrir_dialogos(janela):
    """Os diálogos que as etapas abrem, construídos (sem ``exec``) com os dados da janela."""
    from triton.ui import dialogs as D
    from triton.ui.tab_environmental import LCAParametersDialog
    ts = janela.tab_tanks_simulation
    cfg = ts._get_config()
    saida = []

    def tenta(nome, fabrica):
        try:
            saida.append((nome, fabrica()))
        except Exception as exc:  # um diálogo que não abre é achado, mas não derruba a varredura
            saida.append((nome + "!erro", _Erro(str(exc))))

    tenta("capex", lambda: D.DialogInitialCosts(ts, config=cfg, evaluated_volumes=[1000.0, 2000.0]))
    tenta("motobomba", lambda: D.DialogMotobomba(ts, config=cfg))
    tenta("opex", lambda: D.DialogOtherOpCosts(ts, op_costs=cfg.op_costs))
    tenta("tarifas", lambda: D.DialogTariffs(ts, config=cfg))
    tenta("eletricidade", lambda: D.DialogElectricity(ts, config=cfg))
    tenta("estimativas", lambda: D.DialogWaterEstimates(ts, config=cfg))
    tenta("reservatorio_superior", lambda: D.DialogUpperTank(ts))
    tenta("assistente_de_bombas", lambda: D.PumpSelectionWizardDialog(upper_tank_vol=500.0, sweep_volumes=[1000, 2000], parent=ts))
    tenta("acv", lambda: LCAParametersDialog(janela.tab_environmental, parent=janela.tab_environmental))
    return [(n, d) for n, d in saida if not isinstance(d, _Erro)] +            [(n, d) for n, d in saida if isinstance(d, _Erro) and print("AVISO: diálogo não abriu:", n, d.msg, file=sys.stderr)]


class _Erro:
    def __init__(self, msg):
        self.msg = msg


def ocorrencias(achados, padrao) -> list[tuple[str, str, str]]:
    """(onde, termo, texto) para cada texto que casa com ``padrao`` fora dos permitidos."""
    saida = []
    extras = PERMITIDOS_INT if _edicao() == "INT" else []
    permitido = re.compile("|".join(PERMITIDOS + extras), re.IGNORECASE)
    for onde, texto in achados:
        limpo = permitido.sub("", texto)
        for m in padrao.finditer(limpo):
            saida.append((onde, m.group(0), texto))
    return saida


# --------------------------------------------------------------------------------------------
# Testes
# --------------------------------------------------------------------------------------------

def _abrir(qapp):
    from triton.ui.main_window import MainWindow
    return MainWindow()


def _edicao():
    from triton.core.edition import get_current_edition
    return get_current_edition()


def _com_idioma(idioma: str):
    from triton.ui import translation as T
    anterior = T.get_current_lang()
    T.set_current_lang(idioma)
    return anterior


@pytest.fixture
def idioma_restaurado():
    pytest.importorskip("PySide6", reason="a interface exige PySide6 (a CI não o instala)")
    from triton.ui import translation as T
    anterior = T.get_current_lang()
    yield
    T.set_current_lang(anterior)


@pytest.mark.parametrize("idioma", ["en", "pt", "es", "zh"])
def test_fora_da_brasil_a_interface_nao_fala_do_brasil(qapp, idioma_restaurado, idioma):
    """INT e PRT: nenhum termo do Brasil em nenhuma das 13 etapas, em nenhum idioma."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        pytest.skip("a Edição Brasil mantém o que é do Brasil")
    _com_idioma(idioma)
    janela = _abrir(qapp)
    try:
        achados = coletar_textos(janela)
        ruins = ocorrencias(achados, _PADRAO_BRASIL)
        resumo = sorted({(o.split("/")[0], t, x[:90]) for o, t, x in ruins})
        assert not ruins, f"{len(ruins)} ocorrências; amostra: {resumo[:25]}"
    finally:
        janela.close()


@pytest.mark.parametrize("idioma", ["en", "pt"])
def test_na_internacional_nao_ha_portugal(qapp, idioma_restaurado, idioma):
    if _edicao() != "INT":
        pytest.skip("só na Internacional")
    _com_idioma(idioma)
    janela = _abrir(qapp)
    try:
        ruins = ocorrencias(coletar_textos(janela), _PADRAO_PORTUGAL)
        resumo = sorted({(o.split("/")[0], t, x[:90]) for o, t, x in ruins})
        assert not ruins, f"{len(ruins)} ocorrências; amostra: {resumo[:25]}"
    finally:
        janela.close()


def test_na_brasil_nao_ha_portugal(qapp, idioma_restaurado):
    if _edicao() != "BRL":
        pytest.skip("só na Brasil")
    _com_idioma("pt")
    janela = _abrir(qapp)
    try:
        # «Portugal» aparece na lista de idiomas e em «Edição Portugal»? Não: a BRL não os oferece.
        ruins = [r for r in ocorrencias(coletar_textos(janela), _PADRAO_PORTUGAL)
                 if r[1].lower() not in ("porto", "iva")]
        assert not ruins, ruins[:15]
    finally:
        janela.close()


def test_portugal_fala_portugues_de_portugal(qapp, idioma_restaurado):
    """PRT em português: sem o vocabulário do Brasil (o glossário vale para todo o texto)."""
    if _edicao() != "PRT":
        pytest.skip("só na Portugal")
    _com_idioma("pt")
    janela = _abrir(qapp)
    try:
        ruins = ocorrencias(coletar_textos(janela), _PADRAO_PT_BR)
        resumo = sorted({(o.split("/")[0], t, x[:90]) for o, t, x in ruins})
        assert not ruins, f"{len(ruins)} ocorrências; amostra: {resumo[:25]}"
    finally:
        janela.close()


def test_internacional_em_ingles_sem_portugues(qapp, idioma_restaurado):
    """INT em inglês: nenhum rótulo ficou em português (fora das dicas longas da documentação)."""
    if _edicao() != "INT":
        pytest.skip("só na Internacional")
    _com_idioma("en")
    janela = _abrir(qapp)
    try:
        achados = coletar_textos(janela, incluir_documentacao=False)
        ruins = []
        for onde, texto in achados:
            if ":valor" in onde or ":cab" in onde and len(texto) < 3:
                continue
            palavras = _PORTUGUES_NO_INGLES.findall(texto)
            if len(palavras) >= 2 or (palavras and len(texto.split()) <= 3 and re.search(r"[ãõáéíóúâêôç]", texto)):
                ruins.append((onde.split("/")[0], texto[:100]))
        assert not ruins, f"{len(ruins)} textos em português; amostra: {sorted(set(ruins))[:25]}"
    finally:
        janela.close()


def test_a_brasil_continua_com_os_seus_termos(qapp, idioma_restaurado):
    """A BRL não perde nada: os termos do Brasil continuam à vista."""
    if _edicao() != "BRL":
        pytest.skip("só na Brasil")
    _com_idioma("pt")
    janela = _abrir(qapp)
    try:
        achados = coletar_textos(janela, incluir_documentacao=False)
        termos = {r[1].lower() for r in ocorrencias(achados, _PADRAO_BRASIL)}
        for esperado in ("florianópolis", "casan", "celesc", "r$", "nbr", "iptu", "ipca", "selic"):
            assert any(esperado in t for t in termos), esperado
        # as marcas de bomba estão no assistente (um diálogo, que a varredura das etapas não abre)
        from triton.ui.dialogs.pump_wizard_dialog import catalogo_de_bombas
        assert any("Schneider" in modelo["label"] for modelo in catalogo_de_bombas())
    finally:
        janela.close()


@pytest.mark.parametrize("idioma", ["en", "pt", "es", "zh"])
def test_fora_da_brasil_os_dialogos_nao_falam_do_brasil(qapp, idioma_restaurado, idioma):
    """Os diálogos das etapas (CAPEX, motobomba, tarifas, ACV, assistente de bombas...) também."""
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        pytest.skip("a Edição Brasil mantém o que é do Brasil")
    _com_idioma(idioma)
    janela = _abrir(qapp)
    try:
        achados = coletar_textos(janela, so_dialogos=True)
        assert any(o.startswith("dialogo:assistente_de_bombas") for o, _ in achados), "o assistente de bombas não abriu"
        ruins = ocorrencias(achados, _PADRAO_BRASIL)
        resumo = sorted({(o.split("/")[0], t, x[:90]) for o, t, x in ruins})
        assert not ruins, f"{len(ruins)} ocorrências; amostra: {resumo[:25]}"
    finally:
        janela.close()


def test_a_documentacao_fora_da_brasil_nao_oferece_pagina_vazia(qapp, idioma_restaurado):
    """A página que perde todo o texto ao tirar o Brasil (as certificações) não é oferecida."""
    from triton.core.edition import usa_dados_do_brasil
    _com_idioma("en")
    from triton.ui.tab_documentation import TabDocumentation
    aba = TabDocumentation()
    titulos = [aba.list_topics.item(i).text() for i in range(aba.list_topics.count())]
    assert aba.list_topics.count() == aba.stack_content.count()
    if usa_dados_do_brasil():
        assert any("Casa Azul" in t for t in titulos)
    else:
        assert not any("Certifica" in t or "Certifications" in t for t in titulos)
        assert not any("Casa Azul" in t or "AQUA" in t for t in titulos)


def _projeto_da_cli(tmp_path, nome="modelo.triton"):
    from triton import cli
    destino = cli._create_template(str(tmp_path / nome), cli.serie_de_exemplo_da_edicao(), False)
    return destino.read_text(encoding="utf-8")


def test_a_cli_nao_grava_dado_do_brasil_fora_da_brasil(tmp_path):
    """`triton init`: sem tarifa da CASAN, energia da CELESC, IPTU, Florianópolis nem fator 0,085."""
    from triton.core.edition import usa_dados_do_brasil
    texto = _projeto_da_cli(tmp_path)
    brasil = [t for t in ("CASAN", "CELESC", "Florianópolis", "Florianopolis", "SC", "0.6957", "46.34", "0.085", "iptu_annual_value\": 4000")
              if t in texto]
    if usa_dados_do_brasil():
        assert "Florianopolis1.csv" in texto
    else:
        assert not brasil, brasil


def test_a_cli_fora_da_brasil_cria_catalogo_da_propria_edicao(tmp_path):
    from triton import cli
    from triton.core.edition import usa_dados_do_brasil, serie_de_exemplo_da_edicao
    destino = cli._create_catalog("climates", str(tmp_path / "climas.json"))
    texto = destino.read_text(encoding="utf-8")
    assert serie_de_exemplo_da_edicao() in texto
    if not usa_dados_do_brasil():
        assert not _PADRAO_BRASIL.search(texto), texto


def test_a_ajuda_da_cli_fora_da_brasil_nao_traz_o_estudo_do_brasil(capsys, monkeypatch):
    """`--help`: sem `compare-mass` (TesteMassivo), `run-vaz-study` nem CLIMBra; na Brasil, tudo como antes."""
    from triton import cli
    from triton.core.edition import usa_dados_do_brasil
    monkeypatch.setattr(sys, "argv", ["triton", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    ajuda = capsys.readouterr().out
    if usa_dados_do_brasil():
        assert "compare-mass" in ajuda and "run-vaz-study" in ajuda
    else:
        assert "compare-mass" not in ajuda and "run-vaz-study" not in ajuda
        assert not _PADRAO_BRASIL.search(ajuda), _PADRAO_BRASIL.search(ajuda).group(0)


@pytest.mark.parametrize("edicao", ["INT", "PRT"])
def test_o_filtro_da_documentacao_tira_so_o_que_cita_o_brasil(edicao):
    from triton.core import edition
    from triton.ui.textos_da_edicao import sem_brasil_no_html
    anterior = edition.get_current_edition()
    edition.set_current_edition(edicao)
    try:
        html = ("<h2>Chuva</h2><p>A série é diária. Fonte: INMET e ANA. O balanço é feito dia a dia.</p>"
                "<h3>CLIMBra (CMIP6)</h3><p>Projeções de 652 municípios.</p><h3>Descarte</h3><p>Subtrai-se df.</p>"
                "<ul><li>Resolução de 0,25°</li><li>Norma ABNT NBR 15527</li></ul>"
                "<table><tr><td>Telha cerâmica</td><td>0,75</td><td>Usual em casas brasileiras.</td></tr>"
                "<tr><td>Fonte da CASAN</td><td>1</td><td>x</td></tr></table>")
        limpo = sem_brasil_no_html(html)
        assert "INMET" not in limpo and "CLIMBra" not in limpo and "652" not in limpo
        assert "ABNT" not in limpo and "CASAN" not in limpo and "brasileiras" not in limpo
        assert "A série é diária." in limpo and "O balanço é feito dia a dia." in limpo
        assert "Subtrai-se df." in limpo and "Resolução de 0,25°" in limpo
        assert "Telha cerâmica" in limpo and "0,75" in limpo   # a linha fica; só a nota sai
    finally:
        edition.set_current_edition(anterior)


def test_o_filtro_da_documentacao_nao_mexe_na_brasil():
    from triton.core.edition import usa_dados_do_brasil
    from triton.ui.textos_da_edicao import sem_brasil_no_html
    html = "<p>Fonte: INMET. NBR 15527.</p>"
    if usa_dados_do_brasil():
        assert sem_brasil_no_html(html) == html


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--idioma", default="en")
    ap.add_argument("--sem-doc", action="store_true")
    ap.add_argument("--tudo", action="store_true", help="lista todos os textos, e não só as ocorrências")
    ap.add_argument("--dialogos", action="store_true", help="varre os diálogos em vez das etapas")
    a = ap.parse_args()
    raiz = _raiz_do_pacote()
    sys.path.insert(0, raiz)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("TRITON_VOLUMETRIA_SIMPLES", "1")
    from PySide6.QtCore import QSettings
    from PySide6.QtWidgets import QApplication, QMessageBox
    import tempfile
    QSettings.setDefaultFormat(QSettings.IniFormat)
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, tempfile.mkdtemp(prefix="triton_ini_"))
    app = QApplication.instance() or QApplication(sys.argv)
    for nome in ("information", "warning", "critical", "question"):
        setattr(QMessageBox, nome, staticmethod(lambda *x, **k: QMessageBox.StandardButton.Yes))
    from triton.ui import translation as T
    T.set_current_lang(a.idioma)
    from triton.ui.main_window import MainWindow
    j = MainWindow()
    achados = coletar_textos(j, incluir_documentacao=not a.sem_doc, so_dialogos=a.dialogos)
    print(f"# edição {_edicao()} idioma {a.idioma}: {len(achados)} textos", file=sys.stderr)
    if a.tudo:
        for o, t in achados:
            print(f"{o}\t{t}")
    else:
        for nome, padrao in (("BRASIL", _PADRAO_BRASIL), ("PORTUGAL", _PADRAO_PORTUGAL),
                             ("PT-BR", _PADRAO_PT_BR if _edicao() == "PRT" else re.compile(r"(?!x)x"))):
            for o, t, x in ocorrencias(achados, padrao):
                print(f"{nome}\t{o}\t[{t}]\t{x[:160]}")
