"""
Testes unitários e de integração para a geração de relatórios (Executive vs Research) e PDF.
"""

import os
import tempfile
import pytest

from triton.core.report_generator import (
    generate_executive_html_report,
    generate_research_html_report,
    save_pdf_report
)
from triton.core.environmental import calculate_lca, EnvironmentalConfig
import sys
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_generate_executive_html_report():

    project_data = {
        "ref_code": "NET-TEST-001",
        "rain_file": "ClimaFpolis.csv",
        "area": 250.0,
        "runoff": 0.85,
        "discard": 2.0,
        "residents": 5,
        "demand": 150.0,
        "share": 0.40,
        "lower_vol": 5000.0,
        "potential_pct": 35.5,
        "pluv_day": 120.0,
        "potable_day": 180.0,
        "spill_day": 40.0,
        "sat_full": 80.0,
        "sat_null": 10.0,
        "capex": 9500.0,
        "annual_gross": 3200.0,
        "vpl": 28500.0,
        "tir": 26.5,
        "payback_s": "4,1",
        "payback_d": "5,5"
    }

    html = generate_executive_html_report(project_data)
    assert isinstance(html, str)
    assert "Laudo Técnico Executivo" in html
    assert "NET-TEST-001" in html
    assert "5.000 L" in html or "5000" in html
    assert "35,5%" in html


def test_generate_research_html_report():
    project_data = {
        "ref_code": "NET-RESEARCH-99",
        "rain_file": "ClimaManaus.csv",
        "area": 500.0,
        "runoff": 0.80,
        "discard": 2.5,
        "residents": 12,
        "demand": 200.0,
        "share": 0.50,
        "lower_vol": 10000.0,
        "potential_pct": 48.2,
        "pluv_day": 450.0,
        "potable_day": 550.0,
        "spill_day": 120.0,
        "sat_full": 85.0,
        "sat_null": 5.0,
        "capex": 18000.0,
        "annual_gross": 6500.0,
        "vpl": 55000.0,
        "tir": 31.2,
        "payback_s": "3,8",
        "payback_d": "4,9",
        "system_design": {
            "upper_used": True,
            "upper_volume_l": 500.0,
            "pump_power_cv": "1/2",
            "pump_power_kw": 0.37,
            "pump_flow_l_h": 3000.0,
            "pump_count": 1,
            "pump_threshold_pct": "50",
        },
        "optima": {
            "technical": {"volume": 8000.0, "water_saved": 150.0, "vpl": 42000.0, "co2": 310.0, "capex": 16000.0},
            "economic": {"volume": 6000.0, "water_saved": 142.0, "vpl": 55000.0, "co2": 280.0, "capex": 13000.0},
            "environmental": {"volume": 5000.0, "water_saved": 136.0, "vpl": 48000.0, "co2": 340.0, "capex": 11800.0},
            "balanced": {"volume": 6500.0, "water_saved": 145.0, "vpl": 53500.0, "co2": 325.0, "capex": 14000.0},
        },
        "topsis_criterion_labels": ["Potencial máximo", "Maior VPL", "Menor CO2"],
        "topsis_criterion_weights": [0.34, 0.33, 0.33],
        "topsis_candidates": [
            {"volume": 5000.0, "saving": 44.0, "water_m3": 136.0, "potable_m3": 140.0, "overflow_m3": 52.0, "capex": 11800.0, "vpl": 48000.0, "co2": 340.0, "score": 0.78, "rank": 3, "discounted_payback": 5.2, "irr": 28.0},
            {"volume": 6000.0, "saving": 46.0, "water_m3": 142.0, "potable_m3": 134.0, "overflow_m3": 46.0, "capex": 13000.0, "vpl": 55000.0, "co2": 280.0, "score": 0.84, "rank": 2, "discounted_payback": 4.9, "irr": 31.2},
            {"volume": 6500.0, "saving": 47.0, "water_m3": 145.0, "potable_m3": 131.0, "overflow_m3": 43.0, "capex": 14000.0, "vpl": 53500.0, "co2": 325.0, "score": 0.91, "rank": 1, "discounted_payback": 5.0, "irr": 30.5},
            {"volume": 8000.0, "saving": 48.2, "water_m3": 150.0, "potable_m3": 126.0, "overflow_m3": 38.0, "capex": 16000.0, "vpl": 42000.0, "co2": 310.0, "score": 0.73, "rank": 4, "discounted_payback": 6.2, "irr": 25.0},
        ],
        "sweep_points": [
            {"volume": 5000.0, "saving": 44.0, "pluvial_m3": 136.0, "potable_m3": 140.0, "spill_m3": 52.0, "sat_full": 78.0},
            {"volume": 6000.0, "saving": 46.0, "pluvial_m3": 142.0, "potable_m3": 134.0, "spill_m3": 46.0, "sat_full": 81.0},
            {"volume": 6500.0, "saving": 47.0, "pluvial_m3": 145.0, "potable_m3": 131.0, "spill_m3": 43.0, "sat_full": 83.0},
            {"volume": 8000.0, "saving": 48.2, "pluvial_m3": 150.0, "potable_m3": 126.0, "spill_m3": 38.0, "sat_full": 85.0},
        ],
        "report_charts": [
            {"chapter": "hydraulic", "title": "Desempenho hídrico: potencial de economia", "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="},
            {"chapter": "economic", "title": "Avaliação econômica: VPL por volume", "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="},
            {"chapter": "decision", "title": "Decisão multicritério: desempenho TOPSIS", "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="},
            {"chapter": "environmental", "title": "ACV: comparação ambiental", "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="},
        ],
    }

    lca_res = calculate_lca(10000.0, 160.0, EnvironmentalConfig(material_key="PEAD"))

    html = generate_research_html_report(project_data, lca_result=lca_res)
    assert isinstance(html, str)
    assert "Relatório Técnico-Científico de Pesquisa" in html
    assert "NET-RESEARCH-99" in html
    assert "Análise do Ciclo de Vida" in html
    assert "Responsabilidade de Verificação das Equações" in html
    assert "Sistemas Representativos e Diferenças Principais" in html
    assert "Sensibilidade, Incertezas e Limitações" in html
    assert "Conclusões e Protocolo de Escolha" in html
    assert "Compromisso TOPSIS" in html
    assert "Referência técnica" in html
    assert ("Dif. para maior VPL" in html) or ("Dif. para maior VAL" in html)
    assert "Figura 1 — Economia de água potável por capacidade" in html or "Figura 1" in html
    assert "Figura 2 — VPL por capacidade" in html or "Figura 2" in html
    assert "Figura 3 — Desempenho TOPSIS por capacidade" in html or "Figura 3" in html
    assert "Figura 4 — Comparação ambiental da ACV" in html or "Figura 4" in html
    assert "Fonte: resultados calculados pelo Triton" in html
    assert "Leitura:" in html
    assert "elevada atratividade" not in html
    assert "excelente regularidade" not in html
    assert "<table" in html

    project_data["mcdm_method"] = "smaa_vikor"
    project_data["mcdm_num_simulations"] = 5000
    project_data["topsis_candidates"][2]["score"] = 63.4
    html_smaa = generate_research_html_report(project_data, lca_result=lca_res)
    assert "Compromisso robusto SMAA-VIKOR" in html_smaa
    assert "5.000 simulações Monte Carlo" in html_smaa
    assert "um vetor de pesos no simplex" in html_smaa
    assert "Aceitabilidade SMAA-VIKOR" in html_smaa
    assert "63,40%" in html_smaa
    assert "não existe um perfil único de pesos" in html_smaa
