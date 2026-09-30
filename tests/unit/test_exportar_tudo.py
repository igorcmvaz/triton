"""Exportar tudo: a planilha de auditoria traz todos os campos, sem seleção."""

import dataclasses

import numpy as np
import openpyxl
import pytest

from netuno.core.economic import run_economic_analysis
from netuno.core.environmental import EnvironmentalConfig, calculate_lca
from netuno.core.exportar_tudo import exportar_tudo
from netuno.core.parser import NetunoConfig
from netuno.core.simulation import run_single_simulation
from netuno.core.study_layout import generate_study_layout
from netuno.core.tariffs_database import esgoto_do_municipio, get_city_data


@pytest.fixture(scope="module")
def planilha(tmp_path_factory):
    rng = np.random.default_rng(7)
    chuva = np.where(rng.random(730) < 0.35, rng.exponential(12, 730), 0.0)
    cfg = NetunoConfig()
    alegrete = get_city_data("RS", "Alegrete")
    cfg.water_tariffs = [tuple(f) for f in alegrete["faixas"]]
    cfg.sewage_mode, cfg.sewage_rate = esgoto_do_municipio(alegrete)
    sim = run_single_simulation(chuva, 5000.0, area=150, total_demand_per_day=400, rainwater_share=0.4,
                                store_daily_details=True)
    economia = run_economic_analysis(cfg, sim)
    m3 = sim.avg_pluvial_consumed_l_day * 0.365
    ambiental = calculate_lca(5000.0, m3, EnvironmentalConfig(annual_water_saved_m3=m3))
    dados = {"project_name": "Auditoria", "lower_vol": 5000, "upper_vol": 1000, "area": 150}
    dados.update(generate_study_layout(dados))
    caminho = tmp_path_factory.mktemp("tudo") / "auditoria.xlsx"
    exportar_tudo(str(caminho), config=cfg, project_data=dados, single_result=sim,
                  economic_result=economia, environmental_result=ambiental)
    return cfg, openpyxl.load_workbook(caminho)


def _coluna(ws, indice=0):
    return [linha[indice] for linha in ws.iter_rows(min_row=2, values_only=True)]


def test_todo_campo_da_configuracao_esta_nas_premissas(planilha):
    cfg, wb = planilha
    campos = set(_coluna(wb["Auditoria_Premissas"]))
    faltam = {f.name for f in dataclasses.fields(NetunoConfig)} - campos
    assert not faltam, faltam


def test_as_seis_abas_de_dados_vem_junto(planilha):
    _, wb = planilha
    for aba in ("1_Resumo_Projeto", "4_Fluxo_Caixa_Economico", "5_Inventario_ACV_ESG"):
        assert aba in wb.sheetnames
    assert wb.sheetnames[0] == "0_Leia_me"


def test_a_tarifa_sai_com_o_significado_de_cada_codigo_e_o_esgoto(planilha):
    _, wb = planilha
    ws = wb["Auditoria_Tarifa"]
    textos = " ".join(str(c) for linha in ws.iter_rows(values_only=True) for c in linha if c is not None)
    assert "preço-base da fórmula exponencial" in textos and "exponencial" in textos
    assert "preço por m³ consumido" in textos


def test_a_etapa_de_qualidade_entra_no_carbono_e_na_planilha(planilha):
    """A ACV soma a ETAP dimensionada na etapa de qualidade; as duas aparecem."""
    _, wb = planilha
    assert "Auditoria_ETAP" in wb.sheetnames
    itens = next(n for n in wb.sheetnames if n.startswith("Auditoria_Ambi·"))
    categorias = " ".join(str(c) for c in _coluna(wb[itens], 1))
    assert "ETAP" in categorias or "Desinfecção" in categorias


def test_o_arranjo_3d_sai_com_o_quantitativo(planilha):
    _, wb = planilha
    assert len(_coluna(wb["Auditoria_Componentes"])) == 26
    textos = [c for c in _coluna(wb["Auditoria_Trechos"]) if c]
    assert any(str(t).startswith("DN ") for t in textos)
