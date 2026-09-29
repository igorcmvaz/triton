import pytest
from netuno.core.report_generator import (
    generate_executive_html_report,
    generate_environmental_html_report,
    generate_research_html_report,
)
from netuno.core.environmental import calculate_lca, EnvironmentalConfig
from netuno.core.esg_certifications import calculate_esg_certifications
from netuno.ui.translation import set_current_lang, get_current_lang


@pytest.fixture
def sample_project_data():
    return {
        "ref_code": "NET-TEST-2026",
        "rain_file": "Florianopolis_Historico.csv",
        "area": 250.0,
        "runoff": 0.85,
        "discard": 2.0,
        "residents": 6,
        "demand": 180.0,
        "share": 0.40,
        "lower_vol": 6000.0,
        "potential_pct": 38.5,
        "pluv_day": 415.8,
        "potable_day": 664.2,
        "spill_day": 120.5,
        "sat_full": 88.2,
        "sat_null": 4.1,
        "capex": 12500.0,
        "annual_gross": 3890.0,
        "vpl": 28400.0,
        "tir": 29.4,
        "payback_s": "3.2",
        "payback_d": "4.1",
    }


def test_generate_environmental_html_report_pt(sample_project_data):
    set_current_lang("pt")
    lca_res = calculate_lca(
        tank_vol_liters=sample_project_data["lower_vol"],
        annual_pluvial_m3=(sample_project_data["pluv_day"] * 365.0) / 1000.0,
        config=EnvironmentalConfig(),
    )
    esg_res = calculate_esg_certifications(
        potable_savings_pct=sample_project_data["potential_pct"],
        annual_pluvial_consumed_m3=(sample_project_data["pluv_day"] * 365.0) / 1000.0,
        annual_potable_consumed_m3=(sample_project_data["potable_day"] * 365.0) / 1000.0,
        net_co2e_saved_kg_lifetime=lca_res.lifetime_net_co2_saved_kg,
        project_lifetime_years=20,
    )

    html = generate_environmental_html_report(
        project_data=sample_project_data,
        lca_result=lca_res,
        esg_result=esg_res,
    )

    assert html is not None
    assert "<!DOCTYPE html>" in html
    assert "Relatório de Desempenho Ambiental" in html
    assert "NET-TEST-2026" in html
    assert "Carbono Incorporado" in html
    assert "Inventário do Ciclo de Vida" in html
    assert "LEED" in html
    assert "AQUA-HQE" in html
    assert "Casa Azul" in html
    assert "GRI 303" in html
    assert "Responsável Técnico(a) / Especialista Ambiental" in html


def test_generate_environmental_html_report_en(sample_project_data):
    set_current_lang("en")
    lca_res = calculate_lca(
        tank_vol_liters=sample_project_data["lower_vol"],
        annual_pluvial_m3=(sample_project_data["pluv_day"] * 365.0) / 1000.0,
        config=EnvironmentalConfig(),
    )
    esg_res = calculate_esg_certifications(
        potable_savings_pct=sample_project_data["potential_pct"],
        annual_pluvial_consumed_m3=(sample_project_data["pluv_day"] * 365.0) / 1000.0,
        annual_potable_consumed_m3=(sample_project_data["potable_day"] * 365.0) / 1000.0,
        net_co2e_saved_kg_lifetime=lca_res.lifetime_net_co2_saved_kg,
        project_lifetime_years=20,
    )

    html = generate_environmental_html_report(
        project_data=sample_project_data,
        lca_result=lca_res,
        esg_result=esg_res,
    )

    assert html is not None
    assert "<!DOCTYPE html>" in html
    assert "Environmental Performance" in html
    assert "Embodied Carbon" in html
    assert "ISO 14040" in html
    set_current_lang("pt")


def test_tab_reports_pdf_integration(qapp, sample_project_data):
    from netuno.ui.tab_reports_pdf import TabReportsPdf

    tab = TabReportsPdf()
    tab._collect_project_data = lambda: sample_project_data
    tab._project_data = sample_project_data

    # Test Economic Report
    tab.combo_report_type.setCurrentIndex(tab.combo_report_type.findData("economic"))
    tab.update_report_preview()
    html_econ = tab.generate_html_content()
    assert "Laudo Técnico Executivo" in html_econ

    # Test Environmental Report
    tab.combo_report_type.setCurrentIndex(tab.combo_report_type.findData("environmental"))
    tab.update_report_preview()
    assert "Relatório de Desempenho Ambiental" in tab.txt_preview.toPlainText()
    html_env = tab.generate_html_content()
    assert "Relatório de Desempenho Ambiental" in html_env

    # Test Research Report
    tab.combo_report_type.setCurrentIndex(tab.combo_report_type.findData("research"))
    tab.update_report_preview()
    assert "Relatório Técnico-Científico de Pesquisa" in tab.txt_preview.toPlainText()
    html_res = tab.generate_html_content()
    assert "Relatório Técnico-Científico de Pesquisa" in html_res
