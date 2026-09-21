"""
Testes unitários para TabProject garantindo o modelo padrão INM-CM4,
recorte temporal inicial até 31/12/2013 e o descarte inicial por declarar.
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication
from netuno.core.hydrology_defaults import LAMINA_DE_DESCARTE_PADRAO_MM
from netuno.ui.tab_project import TabProject


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_tab_project_defaults(qapp):
    tab = TabProject()
    assert tab is not None

    # Modelo GCM padrão deve ser INM-CM4
    assert tab.combo_climate_model.currentText() == "INM-CM4"

    # Período temporal inicial completo de 1980 a 2013 (inclusive)
    assert tab.txt_start_date.text() == "01/01/1980"
    assert tab.txt_end_date.text() == "31/12/2013"

    # O campo abre vazio, e em amarelo, para pedir a lâmina medida na cobertura.
    assert tab.txt_discard.text() in ["-", ""]
    # O exemplo da dica é a lâmina da norma, que é o que vale se nada for dito.
    assert "2,0" in tab.txt_discard.placeholderText()

    # Dados de chuva carregados (1980 a 2013 = 34 anos cheios = 12419 dias)
    assert tab.precip_data is not None
    assert len(tab.precip_data) == 12419


def test_tab_project_discard_fill(qapp):
    tab = TabProject()
    # Ao preencher o descarte com valor válido, o estado do projeto é atualizado
    tab.txt_discard.setText("2.5")
    assert tab.txt_discard.text() == "2.5"
    assert tab.get_project_state()["discard"] == "2.5"


def test_descarte_vazio_fica_amarelo_pedindo_a_lamina(qapp):
    """Campo por declarar é campo destacado; é assim que o usuário sabe que falta."""
    tab = TabProject()
    assert tab.txt_discard.text().strip() == ""
    assert tab.check_field_highlight(tab.txt_discard, is_date=False) is False
    assert "eab308" in tab.txt_discard.styleSheet()      # a borda amarela


def test_com_o_campo_vazio_a_previa_usa_a_lamina_da_norma(qapp):
    """Vazio não é lâmina zero.

    Antes, esta prévia mostrava a chuva sem descarte nenhum enquanto a simulação
    já descontava a lâmina da ABNT NBR 15527:2019: duas contas diferentes na
    mesma janela, e a da tela era a errada.
    """
    tab = TabProject()
    tab.update_preview_table()
    COL_CHUVA, COL_DESCARTE = 2, 3
    for linha in range(tab.table_preview.rowCount()):
        bruto = tab.table_preview.item(linha, COL_CHUVA)
        desconto = tab.table_preview.item(linha, COL_DESCARTE)
        if not bruto or not desconto:
            continue
        chuva = float(bruto.text().replace(" mm", "").replace(",", "."))
        if chuva >= LAMINA_DE_DESCARTE_PADRAO_MM:
            esperado = f"-{LAMINA_DE_DESCARTE_PADRAO_MM:.1f}".replace(".", ",") + " mm"
            assert desconto.text() == esperado, (linha, chuva, desconto.text())
            return
    raise AssertionError("nenhum dia da prévia chove o bastante para descartar")
