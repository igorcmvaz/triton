"""
Testes unitários robustos para o módulo de exportação CAD (DXF/SVG), planilhas Excel/CSV e TabExport.
Testa casos normais, valores faltantes, formatos especiais e resiliência contra erros de conversão.
"""

import os
import sys
import tempfile
import pytest
from pathlib import Path
from PySide6.QtWidgets import QApplication

from netuno.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram, _safe_float
from netuno.core.simulation_excel_exporter import export_simulation_to_excel, export_simulation_to_csv
from netuno.ui.tab_export import TabExport
from netuno.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_safe_float_robustness():
    """Garante que a função auxiliar _safe_float nunca lance exceções com entradas corrompidas ou strings."""
    assert _safe_float(None, 10.0) == 10.0
    assert _safe_float("", 5.0) == 5.0
    assert _safe_float("-", 2.0) == 2.0
    assert _safe_float("   -   ", 3.0) == 3.0
    assert _safe_float("invalid", 0.0) == 0.0
    assert _safe_float("12,5", 0.0) == 12.5
    assert _safe_float("12.5", 0.0) == 12.5
    assert _safe_float(42, 0.0) == 42.0


def test_cad_robustness_with_unsimulated_project():
    """
    Testa resiliência contra entradas não numéricas como '-' (cenário exato que causou o bug no diálogo do usuário).
    """
    unsimulated_data = {
        "project_name": "Projeto Novo Sem Simulação",
        "ref_code": "N5-EMPTY",
        "area": "-",
        "lower_vol": "-",
        "runoff": "-",
        "discard": "-",
        "upper_vol": "-",
        "potential_pct": "-",
        "audit_context": {"climate_location": "-"}
    }

    # Deve gerar o SVG sem lançar 'ValueError: could not convert string to float: -'
    svg = generate_project_svg_diagram(unsimulated_data)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "PROJETO NOVO SEM SIMULAÇÃO" in svg

    # Deve gerar o DXF sem lançar exceção
    with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as tf:
        temp_dxf = tf.name

    try:
        out_dxf = generate_project_dxf(unsimulated_data, temp_dxf)
        assert os.path.exists(out_dxf)
        assert os.path.getsize(out_dxf) > 500
    finally:
        if os.path.exists(temp_dxf):
            os.remove(temp_dxf)


def test_cad_dxf_generation():
    """Valida se o arquivo DXF é gerado com sintaxe ASCII válida, tabelas de layers e entidades."""
    sample_data = {
        "project_name": "Edifício Residencial Alpha",
        "ref_code": "N5-2026-TEST",
        "area": 250.0,
        "lower_vol": 7500.0,
        "runoff": 0.85,
        "discard": 2.0,
        "upper_vol": 1000.0,
        "potential_pct": 34.5,
        "audit_context": {"climate_location": "Florianópolis / SC"}
    }

    with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as tf:
        temp_dxf = tf.name

    try:
        out_path = generate_project_dxf(sample_data, temp_dxf)
        assert os.path.exists(out_path)
        assert os.path.getsize(out_path) > 500

        with open(out_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "SECTION" in content
        assert "TABLES" in content
        assert "LAYER" in content
        assert "01_ALVENARIA_COBERTURA" in content
        assert "03_TUB_RECALQUE" in content
        assert "04_TUB_DISTRIBUICAO" in content
        assert "06_EQUIPAMENTOS" in content
        assert "08_COTAS" in content
        assert "ENTITIES" in content
        assert "LINE" in content
        assert "TEXT" in content
        assert "EOF" in content
    finally:
        if os.path.exists(temp_dxf):
            os.remove(temp_dxf)


def test_excel_simulation_export_full_and_custom():
    """Valida a exportação completa e a personalização de abas e horizontes no Excel."""
    sample_proj = {
        "project_name": "Residencial Teste",
        "ref_code": "N5-TEST-EXCEL",
        "area": 120.0,
        "lower_vol": 6250.0,
        "potential_pct": 32.6,
        "vpl": 31213.52,
        "payback": 4.9,
    }

    sample_single = {
        "daily_series": [
            {"date": "01/01/2020", "rain": 12.5, "harvested": 1200.0, "discarded": 200.0, "demand": 240.0, "rain_used": 240.0, "overflow": 0.0, "volume": 760.0, "mains_used": 0.0},
        ]
    }

    # 1. Exportação Completa
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tf:
        temp_full = tf.name

    try:
        export_simulation_to_excel(sample_proj, temp_full, single_result=sample_single)
        import openpyxl
        wb = openpyxl.load_workbook(temp_full)
        assert len(wb.sheetnames) == 6
        assert "1_Resumo_Projeto" in wb.sheetnames
        assert "4_Fluxo_Caixa_Economico" in wb.sheetnames
    finally:
        if os.path.exists(temp_full):
            os.remove(temp_full)

    # 2. Exportação Personalizada: Somente Balanço e Fluxo com 30 anos
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tf:
        temp_custom = tf.name

    try:
        custom_sheets = {"resumo": False, "balanco": True, "varredura": False, "fluxo": True, "acv": False, "mcdm": False}
        export_simulation_to_excel(
            sample_proj,
            temp_custom,
            single_result=sample_single,
            selected_sheets=custom_sheets,
            horizon_years=30
        )
        wb2 = openpyxl.load_workbook(temp_custom)
        assert set(wb2.sheetnames) == {"2_Balanco_Hidrico_Diario", "4_Fluxo_Caixa_Economico"}
        ws_flow = wb2["4_Fluxo_Caixa_Economico"]
        # Verifica se o horizonte de 30 anos foi gerado (Ano 0 até Ano 30 = 31 linhas de dados + 1 cabeçalho)
        assert ws_flow.max_row == 32
    finally:
        if os.path.exists(temp_custom):
            os.remove(temp_custom)


def test_csv_simulation_export():
    """Valida a exportação em CSV com diferentes delimitadores (; e ,)."""
    sample_proj = {"project_name": "CSV Test"}
    sample_single = {
        "daily_series": [
            {"date": "01/01/2020", "rain": 10.0, "harvested": 1000.0, "discarded": 100.0, "demand": 200.0, "rain_used": 200.0, "overflow": 0.0, "volume": 700.0, "mains_used": 0.0}
        ]
    }

    # Teste com ponto e vírgula
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tf:
        temp_csv = tf.name

    try:
        export_simulation_to_csv(sample_proj, temp_csv, sample_single, delimiter=";")
        with open(temp_csv, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
        assert len(lines) >= 2
        assert ";" in lines[0]
        assert "Precipitacao_mm" in lines[0]

        # Teste com vírgula
        export_simulation_to_csv(sample_proj, temp_csv, sample_single, delimiter=",")
        with open(temp_csv, "r", encoding="utf-8-sig") as f:
            lines_comma = f.readlines()
        assert "," in lines_comma[0]
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_tab_export_ui_interactions(qapp):
    """Valida a interação de checkboxes, seleção de formatos e layout da TabExport."""
    tab = TabExport()
    assert tab is not None

    # Teste Marcar/Desmarcar todas as caixas
    tab._set_all_checkboxes(False)
    assert not tab.chk_resumo.isChecked()
    assert not tab.chk_balanco.isChecked()
    assert not tab.chk_mcdm.isChecked()

    tab._set_all_checkboxes(True)
    assert tab.chk_resumo.isChecked()
    assert tab.chk_balanco.isChecked()
    assert tab.chk_mcdm.isChecked()

    # Teste de alternância de formato
    idx_csv = tab.combo_format.findData("csv")
    tab.combo_format.setCurrentIndex(idx_csv)
    assert not tab.lbl_delim.isHidden()
    assert not tab.combo_delim.isHidden()

    idx_xlsx = tab.combo_format.findData("xlsx")
    tab.combo_format.setCurrentIndex(idx_xlsx)
    assert tab.lbl_delim.isHidden()
    assert tab.combo_delim.isHidden()
