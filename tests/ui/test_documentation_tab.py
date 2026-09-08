"""
Teste automatizado para a Aba de Documentação do Netuno 5.
"""

import sys
import pytest
from PySide6.QtWidgets import QApplication

from netuno.ui.main_window import MainWindow
from netuno.ui.tab_documentation import TabDocumentation


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_documentation_tab_creation_and_content(qapp):
    doc_tab = TabDocumentation()
    assert doc_tab is not None
    assert doc_tab.doc_tabs.count() >= 10

    # Verifica se a citação do MIX Sustentável está presente na aba de Telhados (índice 2)
    roof_browser = doc_tab.doc_tabs.widget(2)
    html_roof = roof_browser.toHtml()
    assert "MIX Sustentável" in html_roof
    assert "10.29183/2447-3073.MIX2020.v6.n2.53-66" in html_roof
    assert "Telha Cerâmica" in html_roof

    # Verifica se a aba dos 9 índices pluviométricos está presente (índice 3)
    indices_browser = doc_tab.doc_tabs.widget(3)
    html_indices = indices_browser.toHtml()
    assert "PRCPTOT" in html_indices
    assert "R95p" in html_indices
    assert "RX1day" in html_indices
    assert "RX5day" in html_indices
    assert "SDII" in html_indices
    assert "R20mm" in html_indices
    assert "CDD" in html_indices
    assert "CWD" in html_indices
    assert "Walsh &amp; Lawler" in html_indices or "Walsh & Lawler" in html_indices

    # Verifica se a aba de Qualidade da Água & ETAP está presente (índice 7)
    etap_browser = doc_tab.doc_tabs.widget(7)
    html_etap = etap_browser.toHtml()
    assert "Maykot" in html_etap
    assert "Vaz" in html_etap
    assert "Yaziz" in html_etap
    assert "Martinson" in html_etap
    assert "NBR 15527" in html_etap
    assert "NBR 16783" in html_etap
    assert "ETAP" in html_etap


def test_main_window_has_documentation_tab(qapp):
    window = MainWindow()
    assert hasattr(window, 'tab_export')
    assert hasattr(window, 'tab_documentation')
    assert hasattr(window, 'tab_tariffs_manager')
    assert window.stack.count() == 12
    # Navega até a aba 9 (Exportação)
    window.sidebar.step_changed.emit(9)
    assert window.stack.currentIndex() == 9
    # Navega até a aba 10 (Documentação)
    window.sidebar.step_changed.emit(10)
    assert window.stack.currentIndex() == 10

