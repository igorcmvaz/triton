"""Suíte essencial do Triton: o que não pode quebrar, sem depender da interface gráfica.

Invariantes de negócio (conservação de massa, sentido do VPL, «economizar nunca aumenta a conta»),
limites críticos (zero, vazio, extremos, entradas impossíveis) e modos de falha reais (série com
falha, base ausente, download interrompido, registro corrompido). Roda na integração contínua,
que não instala o PySide6. Os testes de dado com procedência, de manual e de distribuição
continuam nos seus arquivos.
"""
import pathlib as _pathlib
import numpy as np
import pytest
from triton.core.simulation import run_single_simulation
from triton.core import simulation
from triton.core.parser import parse_float, parse_int, TritonConfig
from triton.core.simulation import build_sweep_volume_grid, build_daily_demand_vectors, build_detailed_daily_demand_vectors, run_single_simulation, run_sweep_simulation
from triton.core.economic import run_robust_economic_analysis, calculate_effective_tariff
from triton.core.environmental import calculate_lca, EnvironmentalConfig
import math
import os
import tempfile
from triton.core.parser import load_precipitation
from triton.core.simulation import run_single_simulation, run_sweep_simulation, validar_serie_precipitacao
from triton.core.simulation import run_single_simulation, validar_parametros_fisicos
import json
from pathlib import Path
from triton.core.fracao_atendivel import conciliar_fracoes, fracao_interna_da_total, fracao_total
from triton.core.parser import TritonConfig, load_triton_project
from triton.core.simulation import build_detailed_daily_demand_vectors
from triton.core import simulation as S
from triton.core.simulation import build_sweep_volume_grid, run_single_simulation, run_sweep_simulation
from triton.core.parser import TritonConfig, export_netuno_csv, parse_netuno_csv
from triton.core.simulation import build_daily_demand_vectors, build_detailed_daily_demand_vectors, run_single_simulation, run_sweep_simulation
from triton.core.water_quality import calculate_first_flush_washoff, size_etap, WATER_QUALITY_CLASSES, EtapSizingResult, FirstFlushAnalysis
import sys
from triton.core.comprimento_de_serie import DIAS_NO_ANO, analisar, volume_ideal
from triton.core.demanda_estocastica import DISTRIBUICOES, PerfilDeConsumo, simular, sortear_demanda, sortear_media, volume_ideal_por_realizacao
from datetime import datetime, timedelta
import pandas as pd
from triton.core.calculator import IndicesCalculator, find_max_consecutive_run_length, compute_seasonality_index
from triton.core.test_framework import InputRainfall, InputData, Output, WaterBalanceTestCase
from triton.core.economic import calculate_economic_indicators, run_robust_economic_analysis
from triton.core.economic import run_economic_analysis, TritonConfig, SingleTankSimulationResult
from triton.core.economic import run_robust_economic_analysis, run_sensitivity_analysis, calculate_water_bill, run_economic_analysis
from triton.core.economic import calculate_water_bill
from triton.core.tariff_regimes import CONSUMO_MINIMO_USUAL_M3, DISPONIBILIDADE, FRANQUIA_NO_MINIMO, FRANQUIA_RETROATIVA, PISO_DE_PAGAMENTO, REGIMES as REGIMES_TARIFARIOS_REGIMES, SEM_MINIMO, auditar_base, ler_estrutura, resumo_do_regime, validar_estrutura
from triton.core.tariffs_database import load_tariffs_db
from triton.core.tariff_regimes import EXPONENCIAL, ler_estrutura, resumo_do_regime, validar_estrutura
from triton.core.tariffs_database import get_city_data, get_city_tariffs_by_category
from triton.core.tariffs_structure import EXPOENTE_DE_CONSUMO, PRECO_BASE_EXPONENCIAL, diagnosticar, expoente_do_consumo, parcela_exponencial
from types import SimpleNamespace
from triton.core.economic import calculate_effective_tariff, run_economic_analysis
from triton.core.parser import TritonConfig, export_triton_json, load_triton_project
from triton.core.simulation import SingleTankSimulationResult
from triton.core.vigencia_tarifaria import data_da_vigencia, fatores_desde_a_vigencia, meses_desde_a_vigencia, reajustes_desde_a_vigencia
from triton.core.cost_estimates import LOWER_TANK_PRICE_TABLE, R2_MINIMO_PARA_EXTRAPOLAR, UPPER_TANK_PRICE_TABLE, estimate_tank_price, get_tank_linear_regression, interpolate_price, load_costs_database, regressao_linear_da_tabela
from triton.core.cost_estimates import REGIONAL_FACTORS_BY_UF, TYPOLOGY_COST_CONFIGS, estimate_calibrated_capex_opex, estimate_preliminary_capex
from triton.cli import _get_precipitation, _load_bundle, _preco_da_cisterna, run_analysis
from triton.core.cost_estimates import estimate_preliminary_capex
from triton.core.chlorination import Cloracao
from triton.core.cost_estimates import verba_generica_de_tratamento_brl
from triton.core.economic import run_economic_analysis
from triton.core.environmental import EnvironmentalConfig, calculate_lca
from triton.core.etap_integration import VOLUME_PLUVIAL_DE_RECURSO_M3, dimensionar_etap_do_projeto, volume_pluvial_anual_m3
from triton.core.parser import TritonConfig
from triton.core.etap_integration import capex_incremental_da_etap, opex_anual_incremental_da_etap
from triton.core.water_quality import WATER_QUALITY_CLASSES, size_etap
from triton.core.economic import run_robust_economic_analysis, calculate_economic_indicators
from triton.core.environmental import EnvironmentalConfig, PipeInput, calculate_lca, run_environmental_sweep
import re
from triton.core.chlorination import DOSE_PADRAO_MG_POR_LITRO, FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO, PUREZA_PADRAO, Cloracao, cloracao_padrao
from triton.core.pump_energy import CV_TO_KW, consumo_especifico_padrao_kwh_por_m3
from triton.core.pump_hydraulics import ALTURA_MANOMETRICA_PADRAO_M, energia_especifica_a_partir_da_vazao, energia_especifica_kwh_por_m3, ponto_de_operacao, rendimento_tipico, vazao_l_por_h
from triton.core.pump_energy import compute_annual_pump_energy, consumo_especifico_padrao_kwh_por_m3
from triton.core.pump_hydraulics import ALTURA_MANOMETRICA_PADRAO_M, energia_especifica_kwh_por_m3, rendimento_do_motor, rendimento_tipico
from triton.core.pump_energy import compute_annual_pump_energy
from triton.core import grid_emission_factors as fatores
from triton.core.environmental import EnvironmentalConfig
from triton.core.supply_arrangement import ACIONAMENTOS_POR_PESSOA_DIA, GRAVIDADE, NAO_INFORMADO, PRESSURIZACAO, RECALQUE, arranjo_de
from triton.core.bim_exporter import COMPONENT_TYPES
from triton.core.environmental import calculate_lca
from triton.core.etap_integration import capex_incremental_da_etap
from triton.core.quantitativo_do_arranjo import CATALOGO_DE_PECAS, DESTINO_PROPRIO, conferir_cobertura, itens_para_acv, levantar, quantitativo_do_projeto
from triton.core.study_layout import generate_study_layout
from triton.core.simulation import SingleTankSimulationResult, SimulationDayResult
from triton.core.pump_energy import compute_annual_pump_energy, nearest_pump_cv
from triton.core.environmental_sync import infer_tank_material, estimate_pipe_lengths_m, build_sync_snapshot, material_preset_values
from triton.core.environmental import EnvironmentalConfig, calculate_lca, MATERIAL_PRESETS
from triton.core.topsis import TopsisCandidate
from triton.core.mcdm_methods import run_vikor, run_smaa_analysis, run_smaa_vikor, VikorResult, SmaaResult
from triton.core.edge_certification import LIMIAR_DE_AGUA_PCT, LIMIAR_DE_ENERGIA_AVANCADO_PCT, MEDIDAS_DE_AGUA, avaliar_agua_edge, consumo_base_anual_m3
from triton.core.esg_certifications import calculate_esg_certifications
from triton import cli
from datetime import datetime
from triton.core.parser import parse_float, parse_int, load_precipitation, parse_netuno_csv
from argparse import Namespace
from triton.cli import _json_default, _run_project_matrix, _validate_config, run_analysis
from triton.core.parser import TritonConfig, export_triton_json
from triton.core.parser import FormatoDeProjetoDesconhecido, TritonConfig, export_triton_json, load_triton_project
import subprocess
from triton.core.parser import TritonConfig, export_triton_json, impressao_da_serie, load_triton_project, serie_da_climbra
import io
from triton.core.excel_scenarios import export_scenarios_to_excel_bytes, generate_factorial_grid, generate_sample_scenario_excel, parse_excel_scenarios, run_parsed_scenarios
from triton.core.scenarios import export_matrix_planilha_csv, run_multi_scenario_matrix
import dataclasses
import openpyxl
from triton.core.exportar_tudo import exportar_tudo
from triton.core.tariffs_database import esgoto_do_municipio, get_city_data
from triton import __version__
from triton.cli import _get_precipitation, _load_bundle
from triton.core import modulacao_estocastica as M
from triton.core.fracao_atendivel import fracao_total
from triton.core.tariff_regimes import validar_estrutura
import ezdxf
from triton.core.bim_exporter import build_bim_manifest, validate_bim_manifest
from triton.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram
from triton.core.pipe_network import format_route, lengths_by_dn, parse_route
from triton.core.schematic_3d import generate_schematic_3d_svg
from triton.core.volumetry import build_volumetry
import base64
import struct
from triton.core.volumetry import build_volumetry, face_normal, prism, regular_polygon, tank_dimensions_mm, tube
from triton.core.volumetry_export import feature_edges, scene_payload, write_glb, write_html_viewer

_TESTES = _pathlib.Path(__file__).resolve().parent


# ==================================================================================================
# Motor hidrológico: soluções fechadas, conservação, limites físicos e entradas extremas
# ==================================================================================================

# ---- origem: tests/invariants/test_casos_analiticos.py

def test_regime_limitado_pela_oferta_tem_solucao_fechada():
    """Quando a captação diária é menor que a demanda pluvial, tudo que entra é
    consumido no mesmo dia: a cisterna nunca acumula e nunca extravasa.

    Parâmetros: P = 2 mm/dia constante, A = 50 m², C = 1,0, descarte 0,
    demanda total 1.000 L/dia, fração pluvial 0,5 → demanda pluvial 500 L/dia.

    Derivação:
        captação diária  = 2 × 50 × 1,0            = 100 L
        100 < 500, logo consome-se 100 L todo dia e o estoque volta a zero
        consumo pluvial  = 100 L/dia
        consumo potável  = 1.000 − 100             = 900 L/dia
        extravasamento   = 0
        economia         = 100 ÷ 1.000 × 100       = 10,0 %
        atendimento      = parcial em todos os dias (0 < 100 < 500) → 100 %
    """
    dias = 365
    resultado = run_single_simulation(precip_data=np.full(dias, 2.0), lower_tank_vol=10000.0, area=50.0, runoff_coeff=1.0, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.5)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(100.0, rel=1e-12)
    assert resultado.avg_potable_consumed_l_day == pytest.approx(900.0, rel=1e-12)
    assert resultado.avg_spilled_l_day == pytest.approx(0.0, abs=1e-09)
    assert resultado.potential_potable_savings_pct == pytest.approx(10.0, rel=1e-12)
    assert resultado.pct_days_partial_satisfaction == pytest.approx(100.0, rel=1e-12)


def test_enchimento_e_extravasamento_tem_solucao_fechada():
    """Com captação maior que a demanda, a cisterna enche num dia determinado e a partir
    dali extravasa exatamente o excedente diário.

    Parâmetros: P = 10 mm/dia constante, A = 100 m², C = 1,0, descarte 0,
    demanda total 1.000 L/dia, fração pluvial 0,5, cisterna 5.000 L.

    Derivação:
        captação diária H = 10 × 100 × 1,0 = 1.000 L
        demanda pluvial D = 500 L; excedente diário H − D = 500 L

        O extravasamento antecede o consumo. Seja S o estoque no início do dia:
            após captar: S + H;  se S + H > 5.000, extravasa S + H − 5.000
        Partindo de S = 0, o estoque ao fim do dia k é 500·k enquanto não houver
        extravasamento. No dia 9 tem-se S = 4.000 e S + H = 5.000, que não excede a
        capacidade — logo ainda não há extravasamento e o dia fecha em 4.500 L.
        No dia 10, S + H = 5.500 > 5.000: extravasa 500 L, e assim permanece.

        dias com extravasamento = 365 − 9 = 356
        extravasamento total    = 356 × 500                 = 178.000 L
        consumo pluvial total   = 365 × 500                 = 182.500 L
        conferência do balanço  = 365.000 captados
                                = 182.500 + 178.000 + 4.500 de estoque final ✓
        economia                = 182.500 ÷ 365.000 × 100   = 50,0 %
        atendimento pleno       = todos os dias             = 100 %
    """
    dias = 365
    resultado = run_single_simulation(precip_data=np.full(dias, 10.0), lower_tank_vol=5000.0, area=100.0, runoff_coeff=1.0, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.5)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(500.0, rel=1e-12)
    assert resultado.avg_spilled_l_day == pytest.approx(178000.0 / dias, rel=1e-09)
    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-12)
    assert resultado.pct_days_full_satisfaction == pytest.approx(100.0, rel=1e-12)


def test_descarte_subtrai_lamina_em_proporcao_exata():
    """O descarte reduz a captação na proporção exata da lâmina subtraída.

    Parâmetros: P = 10 mm/dia constante, descarte 3 mm, modo 1 (todo evento).

    Derivação:
        sem descarte: P_ef = 10 mm
        com descarte: P_ef = 10 − 3 = 7 mm
        razão entre as captações = 7 ÷ 10 = 0,7 exatamente

        No regime limitado pela oferta (captação abaixo da demanda pluvial), todo o
        captado é consumido, e a razão dos consumos é a mesma razão das captações.

        A = 50 m², C = 1,0 → captação 500 L/dia sem descarte, 350 L/dia com descarte.
        Demanda pluvial = 1.000 L/dia, acima de ambas, garantindo o regime.

    Sob a regra do Netuno 4 (limiar), 10 mm ≥ 3 mm implicaria captar os 10 mm
    integrais, e a razão seria 1,0. Este teste distingue as duas semânticas.
    """
    comum = dict(precip_data=np.full(365, 10.0), lower_tank_vol=50000.0, area=50.0, runoff_coeff=1.0, discard_mode=1, total_demand_per_day=2000.0, rainwater_share=0.5)
    sem_descarte = run_single_simulation(discard_mm=0.0, **comum)
    com_descarte = run_single_simulation(discard_mm=3.0, **comum)
    assert sem_descarte.avg_pluvial_consumed_l_day == pytest.approx(500.0, rel=1e-12)
    assert com_descarte.avg_pluvial_consumed_l_day == pytest.approx(350.0, rel=1e-12)
    assert com_descarte.avg_pluvial_consumed_l_day / sem_descarte.avg_pluvial_consumed_l_day == pytest.approx(0.7, rel=1e-12)


def test_descarte_periodico_atinge_apenas_os_dias_previstos():
    """No modo 3 o descarte se repete a cada intervalo configurado, e não todo dia.

    Parâmetros: P = 10 mm/dia constante (chove todos os dias), descarte 4 mm,
    modo 3 com intervalo de 5 dias, A = 50 m², C = 1,0, 100 dias.

    Derivação:
        O motor descarta quando ``i − último_descarte ≥ 5``, partindo de um último
        descarte muito antigo. Logo descarta nos dias 0, 5, 10, … 95 — um a cada
        cinco — totalizando 20 dias em 100.

        captação nos 20 dias com descarte  = (10 − 4) × 50 = 300 L
        captação nos 80 dias sem descarte  =  10      × 50 = 500 L
        captação total = 20 × 300 + 80 × 500 = 6.000 + 40.000 = 46.000 L
        média diária   = 460 L

        Com demanda pluvial de 1.000 L/dia, o regime é limitado pela oferta e todo o
        captado é consumido: consumo médio = 460 L/dia.
    """
    resultado = run_single_simulation(precip_data=np.full(100, 10.0), lower_tank_vol=50000.0, area=50.0, runoff_coeff=1.0, discard_mm=4.0, discard_mode=3, discard_days_interval=5, total_demand_per_day=2000.0, rainwater_share=0.5)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(460.0, rel=1e-09)


def test_descarte_apos_estiagem_atinge_apenas_o_primeiro_evento():
    """No modo 2 o descarte incide só no primeiro dia de chuva após um dia seco.

    Parâmetros: padrão de 4 dias — 10 mm, 10 mm, 0 mm, 0 mm — repetido 25 vezes
    (100 dias), descarte 4 mm, A = 50 m², C = 1,0.

    Derivação:
        O motor aplica o descarte quando chove e a véspera teve menos de 1 mm.
        No padrão, o primeiro dia de cada ciclo sucede um dia seco: recebe descarte.
        O segundo dia sucede um dia de 10 mm: não recebe.
        Exceção: o dia 0 não tem véspera, e o motor a trata como 0 mm — logo também
        recebe descarte, o que é consistente com o padrão.

        por ciclo: 1 dia com descarte (P_ef = 6 mm) + 1 dia sem (P_ef = 10 mm)
        captação por ciclo = (6 + 10) × 50 = 800 L, em 4 dias
        captação total     = 25 ciclos × 800 = 20.000 L
        média diária       = 200 L

        Demanda pluvial de 1.000 L/dia mantém o regime limitado pela oferta, mas a
        cisterna precisa acumular entre chuvas; com 50.000 L de capacidade e consumo
        diário limitado pela demanda, todo o captado é consumido ao longo do período.
    """
    padrao = np.array([10.0, 10.0, 0.0, 0.0])
    resultado = run_single_simulation(precip_data=np.tile(padrao, 25), lower_tank_vol=50000.0, area=50.0, runoff_coeff=1.0, discard_mm=4.0, discard_mode=2, total_demand_per_day=2000.0, rainwater_share=0.5)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(200.0, rel=1e-06)


def test_modulacao_semanal_reproduz_o_total_do_padrao():
    """Em um número inteiro de semanas, cada dia da semana ocorre o mesmo número de
    vezes, e a demanda total é o padrão semanal multiplicado por esse número.

    Parâmetros: padrão de segunda a domingo, em L/dia,
    [100, 200, 300, 400, 500, 600, 700]; 364 dias = 52 semanas exatas.

    Derivação:
        soma do padrão = 100+200+300+400+500+600+700 = 2.800 L por semana
        demanda total  = 52 × 2.800 = 145.600 L, qualquer que seja o dia inicial,
        porque em 52 semanas exatas cada dia da semana aparece 52 vezes.

        Com fração pluvial 0,5 e oferta abundante (P = 100 mm/dia sobre 100 m²,
        ou seja 10.000 L/dia, muito acima de qualquer demanda diária do padrão),
        toda a demanda pluvial é atendida:
            consumo pluvial total = 0,5 × 145.600 = 72.800 L
            economia = 72.800 ÷ 145.600 × 100 = 50,0 %
    """
    padrao = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]
    dias = 364
    resultado = run_single_simulation(precip_data=np.full(dias, 100.0), lower_tank_vol=100000.0, area=100.0, runoff_coeff=1.0, discard_mm=0.0, total_demand_per_day=400.0, rainwater_share=0.5, demand_mode='weekly', weekly_demands=padrao, start_date_str='01/01/1980')
    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-09)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(72800.0 / dias, rel=1e-09)


def test_modulacao_mensal_respeita_a_duracao_de_cada_mes():
    """A demanda mensal é ponderada pelo número de dias de cada mês, inclusive em
    fevereiro de ano bissexto.

    Parâmetros: demanda de 100 L/dia em janeiro, 200 em fevereiro, e assim por diante
    até 1.200 em dezembro; ano de 1980, que é bissexto, começando em 01/01.

    Derivação (dias de cada mês em 1980):
        jan 31 ×  100 =  3.100      jul 31 ×  700 = 21.700
        fev 29 ×  200 =  5.800      ago 31 ×  800 = 24.800
        mar 31 ×  300 =  9.300      set 30 ×  900 = 27.000
        abr 30 ×  400 = 12.000      out 31 × 1000 = 31.000
        mai 31 ×  500 = 15.500      nov 30 × 1100 = 33.000
        jun 30 ×  600 = 18.000      dez 31 × 1200 = 37.200

        soma das doze parcelas = 238.400 L, distribuídos em 31+29+31+30+31+30+31+31
        +30+31+30+31 = 366 dias.

        Com oferta abundante e fração pluvial 0,5, a economia é 50,0 % e o consumo
        pluvial total é 119.200 L.

    Um motor que tratasse todos os meses como tendo 30 dias, ou que ignorasse o ano
    bissexto, produziria outro total — daí a escolha de 1980.

    Nota de proveniência: na primeira redação deste caso a soma das doze parcelas foi
    anotada como 237.400 L, por erro de adição manual. O teste reprovou, e a conferência
    mostrou que o valor correto é 238.400 L — ou seja, o defeito estava na derivação e
    não no motor. Fica o registro porque ilustra o que o método faz: obriga a explicitar
    a conta a ponto de o erro, de qualquer um dos dois lados, aparecer.
    """
    mensais = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0]
    dias = 366
    resultado = run_single_simulation(precip_data=np.full(dias, 100.0), lower_tank_vol=200000.0, area=100.0, runoff_coeff=1.0, discard_mm=0.0, total_demand_per_day=650.0, rainwater_share=0.5, demand_mode='monthly', monthly_demands=mensais, start_date_str='01/01/1980')
    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-09)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(119200.0 / dias, rel=1e-09)


def test_irrigacao_e_suprimida_exatamente_nos_dias_de_chuva():
    """A irrigação é suprimida nos dias em que a chuva atinge o limiar configurado.

    Parâmetros: padrão alternado de 5 mm e 0 mm ao longo de 100 dias, limiar de
    supressão 2 mm, irrigação de 150 L/dia.

    Derivação:
        dias com chuva ≥ 2 mm = 50 (os pares do padrão alternado)
        logo a irrigação é suprimida em 50 dias e ativa nos outros 50.

        volume de irrigação suprimido = 50 × 150 = 7.500 L no período
    """
    padrao = np.tile(np.array([5.0, 0.0]), 50)
    configuracao = dict(demand=200.0, residents=4, share=0.5, demand_mode='constant', irrigation_liters_per_day=150.0, irrigation_rain_threshold_mm=2.0, non_potable_indoor_share=0.35, irrigation_potable_backup=True)
    resultado = run_single_simulation(precip_data=padrao, lower_tank_vol=50000.0, area=100.0, runoff_coeff=1.0, discard_mm=0.0, building_config=configuracao)
    assert resultado.total_irrigation_days_suppressed == 50, f'esperados 50 dias de supressão, obtidos {resultado.total_irrigation_days_suppressed}'


def test_reservatorio_superior_amplo_nao_altera_o_consumo():
    """Um reservatório superior que nunca restringe o recalque não muda o balanço.

    O recalque é transferência entre reservatórios, não entrada nem saída do sistema.
    Se o reservatório superior for grande o bastante para nunca limitar o bombeamento,
    o consumo pluvial total deve ser idêntico ao do arranjo com reservatório único.

    Parâmetros: P = 3 mm/dia constante, A = 100 m², C = 1,0 → 300 L/dia captados;
    demanda pluvial 500 L/dia, mantendo o regime limitado pela oferta.

    Derivação: consumo = captação = 300 L/dia nos dois arranjos.
    """
    comum = dict(precip_data=np.full(365, 3.0), lower_tank_vol=20000.0, area=100.0, runoff_coeff=1.0, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.5)
    unico = run_single_simulation(**comum)
    duplo = run_single_simulation(upper_tank_used=True, upper_tank_vol=10000.0, pumping_threshold=0.0, **comum)
    assert unico.avg_pluvial_consumed_l_day == pytest.approx(300.0, rel=1e-09)
    assert duplo.avg_pluvial_consumed_l_day == pytest.approx(unico.avg_pluvial_consumed_l_day, rel=1e-09), 'o reservatório superior alterou o consumo, o que contraria a conservação'


# ---- origem: tests/invariants/test_scientific_properties.py

def _scientific_properties_serie_chuva(escala: float, n_dias: int, semente: int) -> np.ndarray:
    """Série pluviométrica sintética exponencial com dias secos."""
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=escala, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


REGIME_DEMANDA = dict(precip_data=_scientific_properties_serie_chuva(12.0, 1825, 2026), area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.5)


REGIME_OFERTA = dict(precip_data=_scientific_properties_serie_chuva(4.0, 1825, 7), area=30.0, runoff_coeff=0.8, discard_mm=2.0, discard_mode=1, total_demand_per_day=1500.0, rainwater_share=0.6)


SCIENTIFIC_PROPERTIES_REGIMES = [pytest.param(REGIME_DEMANDA, id='limitado-pela-demanda'), pytest.param(REGIME_OFERTA, id='limitado-pela-oferta')]


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_economia_monotona_nao_decrescente_no_volume(regime):
    """P1 — Ampliar a cisterna nunca pode reduzir a economia de água potável.

    Uma violação indicaria que o balanço descarta água já armazenada ao aumentar a
    capacidade, o que é fisicamente impossível num modelo YAS.
    """
    volumes = [0.0, 250.0, 500.0, 1000.0, 2000.0, 5000.0, 10000.0, 25000.0, 60000.0]
    economias = [run_single_simulation(lower_tank_vol=v, **regime).potential_potable_savings_pct for v in volumes]
    for anterior, seguinte, v_ant, v_seg in zip(economias, economias[1:], volumes, volumes[1:]):
        assert seguinte >= anterior - 1e-09, f'economia caiu de {anterior:.6f}% (V={v_ant} L) para {seguinte:.6f}% (V={v_seg} L)'


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_economia_dentro_dos_limites_fisicos(regime):
    """P2 — A economia é uma fração: pertence a [0, 100] e nunca excede a fração não potável."""
    teto_nao_potavel = regime['rainwater_share'] * 100.0
    for v in [0.0, 1000.0, 10000.0, 100000.0]:
        economia = run_single_simulation(lower_tank_vol=v, **regime).potential_potable_savings_pct
        assert 0.0 <= economia <= 100.0, f'economia fora de [0,100]: {economia}'
        assert economia <= teto_nao_potavel + 1e-09, f'economia {economia:.4f}% excede a fração não potável {teto_nao_potavel:.4f}%'


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_volume_zero_nao_aproveita_agua(regime):
    """P2b — Sem reservatório não há armazenamento, logo não há economia."""
    res = run_single_simulation(lower_tank_vol=0.0, **regime)
    assert res.potential_potable_savings_pct == pytest.approx(0.0, abs=1e-09)
    assert res.avg_pluvial_consumed_l_day == pytest.approx(0.0, abs=1e-09)


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_saturacao_em_teto_finito(regime):
    """P3 — A economia converge: dobrar um reservatório já enorme não muda o resultado."""
    grande = run_single_simulation(lower_tank_vol=1000000.0, **regime)
    enorme = run_single_simulation(lower_tank_vol=5000000.0, **regime)
    assert enorme.potential_potable_savings_pct == pytest.approx(grande.potential_potable_savings_pct, abs=0.5), 'a economia não convergiu para um teto estável'


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_reprodutibilidade_exata(regime):
    """P4 — O motor é determinístico: mesma entrada produz saída bit a bit idêntica."""
    a = run_single_simulation(lower_tank_vol=5000.0, **regime)
    b = run_single_simulation(lower_tank_vol=5000.0, **regime)
    assert a.potential_potable_savings_pct == b.potential_potable_savings_pct
    assert a.total_overflow_liters == b.total_overflow_liters


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_economia_nao_decrescente_na_area_de_captacao(regime):
    """P5 — Ampliar a área de captação nunca reduz a economia."""
    economias = []
    for area in [25.0, 50.0, 100.0, 200.0, 400.0]:
        parametros = {**regime, 'area': area}
        economias.append(run_single_simulation(lower_tank_vol=5000.0, **parametros).potential_potable_savings_pct)
    for anterior, seguinte in zip(economias, economias[1:]):
        assert seguinte >= anterior - 1e-09, f'economia caiu ao ampliar a área: {economias}'


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_descarte_de_primeira_chuva_nao_aumenta_economia(regime):
    """P6 — Descartar mais água de first flush nunca pode aumentar o aproveitamento."""
    economias = []
    for descarte in [0.0, 1.0, 2.0, 5.0, 10.0]:
        parametros = {**regime, 'discard_mm': descarte}
        economias.append(run_single_simulation(lower_tank_vol=5000.0, **parametros).potential_potable_savings_pct)
    for anterior, seguinte in zip(economias, economias[1:]):
        assert seguinte <= anterior + 1e-09, f'economia subiu ao descartar mais: {economias}'


@pytest.mark.parametrize('regime', SCIENTIFIC_PROPERTIES_REGIMES)
def test_extravasamento_nao_crescente_no_volume(regime):
    """P7 — Ampliar a cisterna nunca pode aumentar o extravasamento."""
    extravasamentos = [run_single_simulation(lower_tank_vol=v, **regime).total_overflow_liters for v in [250.0, 1000.0, 4000.0, 16000.0, 64000.0]]
    for anterior, seguinte in zip(extravasamentos, extravasamentos[1:]):
        assert seguinte <= anterior + 1e-06, f'extravasamento subiu com V maior: {extravasamentos}'


@pytest.mark.parametrize('volume', [1000.0, 5000.0, 20000.0])
@pytest.mark.parametrize('area', [80.0, 300.0])
@pytest.mark.parametrize('descarte', [0.0, 3.0])
def test_balanco_de_massa_fecha_em_grade_de_parametros(volume, area, descarte):
    """P8 — Conservação de massa em grade paramétrica.

    Complementa `test_mass_conservation.py`, que verifica uma única parametrização:
    aqui o fechamento é exigido em 12 combinações de volume, área e descarte.
    """
    parametros = {**REGIME_DEMANDA, 'area': area, 'discard_mm': descarte}
    res = run_single_simulation(lower_tank_vol=volume, store_daily_details=True, **parametros)
    estoque_anterior = 0.0
    for dia in res.daily_results:
        entradas = estoque_anterior + dia.harvested_liters
        saidas = dia.lower_tank_end_liters + dia.pluvial_consumed_liters + dia.spilled_liters
        assert entradas == pytest.approx(saidas, abs=1e-06), f'balanço não fecha (V={volume}, A={area}, descarte={descarte}): entradas={entradas!r} saídas={saidas!r}'
        estoque_anterior = dia.lower_tank_end_liters


def test_serie_sem_chuva_nao_produz_aproveitamento():
    """P9 — Sem precipitação não há captação, economia nem extravasamento."""
    parametros = {**REGIME_DEMANDA, 'precip_data': np.zeros(365)}
    res = run_single_simulation(lower_tank_vol=5000.0, **parametros)
    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.total_overflow_liters == 0.0


def test_descarte_subtrai_a_lamina_e_nao_atua_como_limiar():
    """P10 — Com chuva uniforme acima do limiar, o descarte reduz proporcionalmente.

    Sob o tratamento por limiar do Netuno 4, uma série em que toda chuva excede `df`
    seria aproveitada integralmente e o descarte não teria efeito algum. Sob a
    subtração, cada evento perde exatamente `df` mm.
    """
    chuva = np.full(730, 10.0)
    parametros = dict(precip_data=chuva, area=100.0, runoff_coeff=1.0, discard_mode=1, total_demand_per_day=2000.0, rainwater_share=1.0)
    sem_descarte = run_single_simulation(lower_tank_vol=1000000000.0, discard_mm=0.0, **parametros)
    com_descarte = run_single_simulation(lower_tank_vol=1000000000.0, discard_mm=2.0, **parametros)
    assert com_descarte.avg_pluvial_consumed_l_day < sem_descarte.avg_pluvial_consumed_l_day, 'o descarte não reduziu o aproveitamento: o motor está tratando `df` como limiar (comportamento do Netuno 4) em vez de subtrair a lâmina'
    perda_observada = sem_descarte.avg_pluvial_consumed_l_day - com_descarte.avg_pluvial_consumed_l_day
    assert perda_observada == pytest.approx(200.0, rel=0.001), f'perda de {perda_observada:.2f} L/dia; esperada 200 L/dia (2 mm × 100 m² × 1,0)'


def test_chuva_abaixo_do_descarte_nao_e_captada():
    """P10b — Evento menor que a lâmina de descarte não rende captação alguma."""
    chuva = np.full(365, 1.5)
    resultado = run_single_simulation(precip_data=chuva, lower_tank_vol=10000.0, area=100.0, runoff_coeff=1.0, discard_mm=3.0, discard_mode=1, total_demand_per_day=500.0, rainwater_share=1.0)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(0.0, abs=1e-09)


@pytest.mark.parametrize('modo,descricao', [(1, 'todos os eventos'), (2, 'primeiro evento após estiagem'), (3, 'periodicidade de manutenção')])
def test_modos_de_descarte_diferem_apenas_na_frequencia(modo, descricao):
    """P10c — Os modos mudam em quais dias o descarte age, não a fórmula.

    Numa série com dias secos intercalados, o modo 1 descarta em todo evento e os
    modos 2 e 3 em subconjuntos dele. Logo o modo 1 nunca aproveita mais água que os
    demais sob a mesma lâmina.
    """
    rng = np.random.default_rng(11)
    chuva = rng.exponential(scale=8.0, size=1095)
    chuva[rng.random(1095) < 0.45] = 0.0
    parametros = dict(precip_data=chuva, lower_tank_vol=8000.0, area=120.0, runoff_coeff=0.9, discard_mm=4.0, discard_days_interval=7, total_demand_per_day=700.0, rainwater_share=0.5)
    todos_os_eventos = run_single_simulation(discard_mode=1, **parametros)
    avaliado = run_single_simulation(discard_mode=modo, **parametros)
    assert avaliado.avg_pluvial_consumed_l_day >= todos_os_eventos.avg_pluvial_consumed_l_day - 1e-09, f'o modo {modo} ({descricao}) aproveitou menos água que o modo 1, que descarta em todos os eventos — a frequência de descarte está invertida'


# ---- origem: tests/invariants/test_mass_conservation.py

def test_water_mass_balance_conservation_invariant():
    """
    Invariante Fundamental:
    Chuva_Total_Capitada = (Estoque_Final - Estoque_Inicial) + Consumo_Pluvial_Total + Extravasamento_Total + Descarte_Total
    """
    np.random.seed(123)
    precip_data = np.random.exponential(scale=15.0, size=100)
    precip_data[precip_data < 2.0] = 0.0
    area = 150.0
    runoff = 0.85
    discard_mm = 2.0
    lower_vol = 5000.0
    tot_demand = 400.0
    share = 0.5
    res = run_single_simulation(precip_data=precip_data, lower_tank_vol=lower_vol, area=area, runoff_coeff=runoff, discard_mm=discard_mm, discard_mode=1, total_demand_per_day=tot_demand, rainwater_share=share, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=200.0, store_daily_details=True)
    previous_lower = 0.0
    previous_upper = 0.0
    for day_res in res.daily_results:
        assert day_res.lower_tank_end_liters >= 0.0
        assert day_res.upper_tank_end_liters >= 0.0
        assert day_res.pluvial_consumed_liters >= 0.0
        assert day_res.spilled_liters >= 0.0
        assert day_res.lower_tank_end_liters <= lower_vol + 1e-05
        assert day_res.upper_tank_end_liters <= 1000.0 + 1e-05
        inputs = previous_lower + previous_upper + day_res.harvested_liters
        outputs = day_res.lower_tank_end_liters + day_res.upper_tank_end_liters + day_res.pluvial_consumed_liters + day_res.spilled_liters
        assert inputs == pytest.approx(outputs, abs=1e-07)
        previous_lower = day_res.lower_tank_end_liters
        previous_upper = day_res.upper_tank_end_liters


# ---- origem: tests/invariants/test_numba_python_parity.py

numba_necessario = pytest.mark.skipif(not simulation.HAS_NUMBA, reason='numba não instalado: o kernel JIT não existe neste ambiente')


TOLERANCIA_RELATIVA = 1e-09


def _numba_python_parity_serie_chuva(semente: int, n_dias: int=1825, escala: float=10.0) -> np.ndarray:
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=escala, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


CENARIOS = [pytest.param(dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.5, upper_tank_used=False, upper_tank_vol=0.0, pumping_threshold=0.0), id='reservatorio-unico'), pytest.param(dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.5, upper_tank_used=True, upper_tank_vol=1000.0, pumping_threshold=300.0), id='reservatorio-duplo-com-recalque'), pytest.param(dict(area=30.0, runoff_coeff=0.8, discard_mm=5.0, discard_mode=2, discard_days_interval=7, total_demand_per_day=1500.0, rainwater_share=0.6, upper_tank_used=False, upper_tank_vol=0.0, pumping_threshold=0.0), id='limitado-pela-oferta-descarte-pos-estiagem')]


def _executar_nos_dois_kernels(monkeypatch, volume, parametros):
    """Roda a mesma parametrização no kernel JIT e no kernel Python de referência."""
    chuva = _numba_python_parity_serie_chuva(2026)
    resultado_jit = run_single_simulation(precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, **parametros)
    monkeypatch.setattr(simulation, 'HAS_NUMBA', False)
    resultado_python = run_single_simulation(precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, **parametros)
    return (resultado_jit, resultado_python)


@numba_necessario
@pytest.mark.parametrize('parametros', CENARIOS)
@pytest.mark.parametrize('volume', [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_na_economia_de_agua(monkeypatch, volume, parametros):
    """O indicador principal do software não pode depender de haver numba instalado."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, volume, parametros)
    assert jit.potential_potable_savings_pct == pytest.approx(puro.potential_potable_savings_pct, rel=TOLERANCIA_RELATIVA), f'economia de água potável diverge entre os kernels: JIT={jit.potential_potable_savings_pct!r} vs Python={puro.potential_potable_savings_pct!r}'


@numba_necessario
@pytest.mark.parametrize('parametros', CENARIOS)
@pytest.mark.parametrize('volume', [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_nos_fluxos_agregados(monkeypatch, volume, parametros):
    """Consumo pluvial, consumo potável e extravasamento devem coincidir."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, volume, parametros)
    for atributo in ('avg_pluvial_consumed_l_day', 'avg_potable_consumed_l_day', 'avg_spilled_l_day', 'total_overflow_liters'):
        assert getattr(jit, atributo) == pytest.approx(getattr(puro, atributo), rel=TOLERANCIA_RELATIVA), f"'{atributo}' diverge entre os kernels"


@numba_necessario
@pytest.mark.parametrize('parametros', CENARIOS)
def test_kernels_concordam_na_estatistica_de_atendimento(monkeypatch, parametros):
    """Os percentuais de dias com atendimento pleno, parcial e nulo devem coincidir."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, 5000.0, parametros)
    for atributo in ('pct_days_full_satisfaction', 'pct_days_partial_satisfaction', 'pct_days_null_satisfaction'):
        assert getattr(jit, atributo) == pytest.approx(getattr(puro, atributo), rel=TOLERANCIA_RELATIVA), f"'{atributo}' diverge entre os kernels"


@numba_necessario
def test_kernel_jit_preserva_a_conservacao_de_massa(monkeypatch):
    """O agregado do kernel JIT deve fechar o balanço tanto quanto o kernel Python.

    Como o caminho JIT não emite detalhamento diário, o fechamento é verificado no
    agregado: captado = consumido + extravasado + estoque final.
    """
    chuva = _numba_python_parity_serie_chuva(99)
    parametros = dict(area=120.0, runoff_coeff=0.85, discard_mm=1.0, discard_mode=1, total_demand_per_day=500.0, rainwater_share=0.5)
    jit = run_single_simulation(precip_data=chuva, lower_tank_vol=8000.0, store_daily_details=False, **parametros)
    monkeypatch.setattr(simulation, 'HAS_NUMBA', False)
    puro = run_single_simulation(precip_data=chuva, lower_tank_vol=8000.0, store_daily_details=False, **parametros)
    captado_jit = jit.annual_pluvial_consumed_m3 + jit.annual_spill_m3
    captado_puro = puro.annual_pluvial_consumed_m3 + puro.annual_spill_m3
    assert captado_jit == pytest.approx(captado_puro, rel=1e-09), 'o volume total captado (consumido + extravasado) diverge entre os kernels'


@numba_necessario
@pytest.mark.parametrize('volume', [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_na_divisao_interno_irrigacao(monkeypatch, volume):
    """Regressão do defeito de repartição interno/irrigação no kernel JIT.

    Histórico. Até a correção, o kernel JIT estimava a repartição aplicando `min()`
    sobre os TOTAIS anuais, enquanto o kernel Python acumulava `min()` DIA A DIA.
    Como Σ min(aᵢ,bᵢ) ≤ min(Σaᵢ, Σbᵢ), o JIT superestimava sistematicamente o consumo
    interno e subestimava a irrigação — divergência medida de 1,8% no interno e 26,3%
    na irrigação, com os totais agregados permanecendo corretos.

    A correção passou a acumular a repartição dentro dos próprios kernels. Este teste
    impede o retorno do viés.

    A repartição importa para além do relatório: LEED v4 pontua uso externo (WEc1) e
    uso interno (WEc2) em créditos separados, de modo que um erro na repartição pode
    alterar o enquadramento em certificação ainda que o total esteja certo.
    """
    configuracao_predial = dict(demand=200.0, residents=4, share=0.5, demand_mode='constant', irrigation_liters_per_day=150.0, irrigation_rain_threshold_mm=2.0, non_potable_indoor_share=0.35, irrigation_potable_backup=True)
    chuva = _numba_python_parity_serie_chuva(2026)
    jit = run_single_simulation(precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, building_config=configuracao_predial)
    monkeypatch.setattr(simulation, 'HAS_NUMBA', False)
    puro = run_single_simulation(precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, building_config=configuracao_predial)
    assert jit.avg_pluvial_consumed_l_day == pytest.approx(puro.avg_pluvial_consumed_l_day, rel=TOLERANCIA_RELATIVA), 'o total de água pluvial consumida divergiu (defeito mais grave que o conhecido)'
    assert jit.annual_pluvial_indoor_consumed_m3 == pytest.approx(puro.annual_pluvial_indoor_consumed_m3, rel=1e-06), 'consumo pluvial interno diverge entre os kernels'
    assert jit.annual_pluvial_irrigation_consumed_m3 == pytest.approx(puro.annual_pluvial_irrigation_consumed_m3, rel=1e-06), 'consumo pluvial de irrigação diverge entre os kernels'


# ---- origem: tests/invariants/test_user_input_robustness.py

def test_parser_chaotic_strings():
    """Valida se o parser tolera formatos pt-BR, en-US, lixo textual e vazios sem quebrar."""
    assert parse_float('1.234,56') == 1234.56
    assert parse_float('1,234.56') == 1234.56
    assert parse_float('1234,56') == 1234.56
    assert parse_float('1234.56') == 1234.56
    assert parse_float('  150,00  ') == 150.0
    assert parse_float('NaN', 42.0) == 42.0
    assert parse_float('inf', 42.0) == 42.0
    assert parse_float('texto_invalido', 10.0) == 10.0
    assert parse_float('-', 5.0) == 5.0
    assert parse_float('', 99.0) == 99.0
    assert parse_float(None, 7.0) == 7.0
    assert parse_int(' 1000 ') == 1000
    assert parse_int(' 1.000,00 ') == 1000
    assert parse_int('10,0') == 10
    assert parse_int('abc', 4) == 4
    assert parse_int('-', 2) == 2
    assert parse_int(None, 1) == 1


def test_sweep_step_larger_than_max():
    """Valida se passo maior que o volume máximo não quebra a grade nem trava em loop infinito."""
    grid = build_sweep_volume_grid(lower_tank_max=500.0, requested_step_l=5000.0)
    assert grid.volumes_l == [0.0, 500.0]
    assert grid.positive_volume_count == 1


def test_sweep_with_zero_maximum():
    """Valida se varredura com volume máximo zero gera a referência de 0 L com segurança."""
    grid = build_sweep_volume_grid(lower_tank_max=0.0, requested_step_l=250.0)
    assert grid.volumes_l == [0.0]
    assert grid.positive_volume_count == 0


def test_sweep_with_fractional_non_multiple_max():
    """Valida se volume máximo quebrado é preservado como último ponto auditável."""
    grid = build_sweep_volume_grid(lower_tank_max=1350.0, requested_step_l=500.0)
    assert grid.volumes_l == [0.0, 500.0, 1000.0, 1350.0]
    assert grid.volumes_l[-1] == 1350.0


def test_simulation_with_zero_demand_and_residents():
    """Valida que demanda zero ou moradores zero não causam divisão por zero na simulação."""
    precip = np.array([10.0, 0.0, 5.0, 0.0], dtype=np.float64)
    b_cfg = {'demand': 0.0, 'residents': 0, 'share': 0.4, 'potable_indoor_share': 0.65, 'non_potable_indoor_share': 0.35, 'irrigation_liters_per_day': 0.0}
    res = run_single_simulation(precip_data=precip, lower_tank_vol=5000.0, area=100.0, runoff_coeff=0.8, discard_mm=1.0, building_config=b_cfg)
    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.annual_pluvial_consumed_m3 == 0.0


def test_simulation_with_zero_area_or_runoff():
    """Valida captação nula com área zero ou coeficiente de escoamento zero."""
    precip = np.array([50.0, 20.0, 10.0], dtype=np.float64)
    b_cfg = {'demand': 150.0, 'residents': 4, 'share': 0.4}
    res = run_single_simulation(precip_data=precip, lower_tank_vol=5000.0, area=0.0, runoff_coeff=0.0, discard_mm=0.0, building_config=b_cfg)
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.potential_potable_savings_pct == 0.0


def test_inverted_potable_and_non_potable_shares():
    """Valida se 100% não-potável ou 100% potável funcionam estavelmente."""
    precip = np.array([10.0, 0.0, 0.0], dtype=np.float64)
    b_cfg_100np = {'demand': 100.0, 'residents': 2, 'potable_indoor_share': 0.0, 'non_potable_indoor_share': 1.0, 'irrigation_liters_per_day': 0.0}
    res_100np = run_single_simulation(precip_data=precip, lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True, building_config=b_cfg_100np)
    assert res_100np.daily_results[0].potable_indoor_consumed_liters == 0.0
    assert res_100np.daily_results[0].pluvial_indoor_consumed_liters == 200.0
    b_cfg_100p = {'demand': 100.0, 'residents': 2, 'potable_indoor_share': 1.0, 'non_potable_indoor_share': 0.0, 'irrigation_liters_per_day': 0.0}
    res_100p = run_single_simulation(precip_data=precip, lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True, building_config=b_cfg_100p)
    assert res_100p.daily_results[0].pluvial_indoor_consumed_liters == 0.0
    assert res_100p.daily_results[0].potable_indoor_consumed_liters == 200.0


def test_huge_demand_and_huge_area_resilience():
    """Valida se demandas industriais/enormes não causam overflow numérico."""
    precip = np.array([25.0, 10.0, 0.0, 50.0], dtype=np.float64)
    b_cfg = {'demand': 50000.0, 'residents': 100, 'potable_indoor_share': 0.5, 'non_potable_indoor_share': 0.5, 'irrigation_liters_per_day': 200000.0}
    res = run_single_simulation(precip_data=precip, lower_tank_vol=1000000.0, area=50000.0, runoff_coeff=0.9, discard_mm=2.0, building_config=b_cfg)
    assert np.isfinite(res.avg_pluvial_consumed_l_day)
    assert np.isfinite(res.potential_potable_savings_pct)
    assert res.avg_pluvial_consumed_l_day > 0


def test_economic_hyper_discount_rate_and_zero_inflation():
    """Valida TMA de 40% a.a. ou inflação zero sem overflow ou erro de convergência."""
    res = run_robust_economic_analysis(initial_investment=50000.0, annual_water_saved_m3=100.0, water_tariff_per_m3=5.0, sewage_tariff_per_m3=5.0, discount_rate=0.4, inflation_rate=0.0, analysis_period_years=20)
    assert np.isfinite(res.vpl)
    assert res.vpl < 0


def test_economic_zero_investment_and_zero_savings():
    """Valida caso sem investimento e sem economia (referência 0 L)."""
    res = run_robust_economic_analysis(initial_investment=0.0, annual_water_saved_m3=0.0, water_tariff_per_m3=5.0, sewage_tariff_per_m3=5.0, discount_rate=0.1, inflation_rate=0.04, analysis_period_years=20)
    assert res.vpl == 0.0
    assert res.total_investment == 0.0
    assert res.payback_simple_years == 0.0
    assert res.payback_discounted_years == 0.0


def test_environmental_zero_volume_and_zero_chlorine():
    """Valida se ACV com 0 L não quebra nem gera impactos de fabricação."""
    cfg = EnvironmentalConfig(upper_tank_used=False, chlorine_dose_mg_l=0.0, pipes=[])
    res = calculate_lca(tank_vol_liters=0.0, annual_pluvial_m3=0.0, config=cfg)
    assert res.total_embodied_co2_kg == 0.0
    assert res.annual_avoided_co2_kg == 0.0
    assert res.annual_treatment_co2_kg == 0.0
    assert res.environmental_payback_years == 0.0


# ---- origem: tests/unit/test_auditoria_do_motor.py

AUDITORIA_DO_MOTOR_BASE = dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.4)


def _serie_sintetica(dias=3650, semente=7):
    """Chuva diária com cerca de metade dos dias secos e cauda longa."""
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=12.0, size=dias)
    chuva[rng.random(dias) < 0.55] = 0.0
    return chuva


def _auditoria_do_motor_arquivo(conteudo):
    f = tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, encoding='utf-8')
    f.write(conteudo)
    f.close()
    return f.name


@pytest.mark.parametrize('volume', [0.0, 1000.0, 5000.0, 50000.0])
def test_massa_fecha_dia_a_dia_e_no_periodo(volume):
    """V(t-1) + captado = extravasado + consumido + V(t), em todo dia."""
    chuva = _serie_sintetica()
    r = run_single_simulation(precip_data=chuva, lower_tank_vol=volume, store_daily_details=True, **AUDITORIA_DO_MOTOR_BASE)
    anterior = 0.0
    entrou = saiu = 0.0
    for d in r.daily_results:
        residuo = anterior + d.harvested_liters - (d.spilled_liters + d.pluvial_consumed_liters + d.lower_tank_end_liters)
        assert abs(residuo) <= 1e-06, (d.day_index, residuo)
        assert -1e-09 <= d.lower_tank_end_liters <= volume + 1e-09
        entrou += d.harvested_liters
        saiu += d.spilled_liters + d.pluvial_consumed_liters
        anterior = d.lower_tank_end_liters
    assert math.isclose(entrou, saiu + anterior, rel_tol=1e-12, abs_tol=1e-06)


def test_evento_extremo_unico_extravasa_so_o_excedente():
    """500 mm num dia sobre 150 m² e C=0,85: capta 63.495 L; cabem 2.000 L."""
    chuva = np.zeros(10)
    chuva[0] = 500.0
    r = run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0, store_daily_details=True, **AUDITORIA_DO_MOTOR_BASE)
    d0 = r.daily_results[0]
    captado = (500.0 - 2.0) * 150.0 * 0.85
    assert d0.harvested_liters == pytest.approx(captado)
    assert d0.spilled_liters == pytest.approx(captado - 2000.0)
    assert d0.pluvial_consumed_liters == pytest.approx(240.0)
    assert d0.lower_tank_end_liters == pytest.approx(1760.0)


def test_descarte_consome_o_dia_inteiro_quando_a_chuva_nao_passa_da_lamina():
    """Modo 1: P <= d_f não produz captação nenhuma naquele dia."""
    r = run_single_simulation(precip_data=np.array([1.0, 2.0, 2.5]), lower_tank_vol=5000.0, store_daily_details=True, **AUDITORIA_DO_MOTOR_BASE)
    assert [d.eff_precip_mm for d in r.daily_results] == pytest.approx([0.0, 0.0, 0.5])


def test_leitor_pula_cabecalho_em_vez_de_devolver_serie_vazia():
    nome = _auditoria_do_motor_arquivo('Data;Precipitacao\n1,2\n3,4\n')
    try:
        assert load_precipitation(nome).tolist() == pytest.approx([1.2, 3.4])
    finally:
        os.unlink(nome)


def test_leitor_preserva_falha_como_nan_e_nao_como_dia_seco():
    nome = _auditoria_do_motor_arquivo('0\n5\n\nfalha\n4\n\n\n')
    try:
        serie = load_precipitation(nome)
    finally:
        os.unlink(nome)
    assert len(serie) == 5, 'linhas vazias no fim do arquivo não são dias'
    assert np.isnan(serie[2]) and np.isnan(serie[3])
    assert serie[4] == 4.0


def test_leitor_para_no_bloco_de_configuracao_do_netuno4():
    nome = _auditoria_do_motor_arquivo('1\n2\nDescarte;2\nÁrea;100\n')
    try:
        assert load_precipitation(nome).tolist() == [1.0, 2.0]
    finally:
        os.unlink(nome)


@pytest.mark.parametrize('detalhe', [False, True])
def test_motor_recusa_falha_de_registro(detalhe):
    chuva = np.array([0.0, 20.0, float('nan'), 5.0])
    with pytest.raises(ValueError, match='dia 3'):
        run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0, store_daily_details=detalhe, **AUDITORIA_DO_MOTOR_BASE)


@pytest.mark.parametrize('detalhe', [False, True])
def test_motor_recusa_sentinela_negativo(detalhe):
    chuva = np.array([0.0, 20.0, -999.0, 0.0])
    with pytest.raises(ValueError, match='-999'):
        run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0, store_daily_details=detalhe, **AUDITORIA_DO_MOTOR_BASE)


def test_motor_recusa_serie_vazia_com_mensagem_e_nao_divisao_por_zero():
    with pytest.raises(ValueError, match='vazia'):
        run_single_simulation(precip_data=np.array([]), lower_tank_vol=2000.0, **AUDITORIA_DO_MOTOR_BASE)


def test_varredura_tambem_valida_a_serie():
    with pytest.raises(ValueError):
        run_sweep_simulation(precip_data=np.array([1.0, float('inf')]), lower_tank_max=1000.0, lower_tank_step=500.0, **AUDITORIA_DO_MOTOR_BASE)


@pytest.mark.parametrize('campo,valor', [('area', float('nan')), ('area', float('inf')), ('runoff_coeff', float('nan')), ('discard_mm', float('nan')), ('total_demand_per_day', float('nan')), ('rainwater_share', float('nan'))])
def test_parametro_nao_finito_e_recusado(campo, valor):
    args = dict(AUDITORIA_DO_MOTOR_BASE)
    args[campo] = valor
    with pytest.raises(ValueError):
        run_single_simulation(precip_data=_serie_sintetica(365), lower_tank_vol=2000.0, **args)


def test_volume_nao_finito_e_recusado():
    with pytest.raises(ValueError):
        run_single_simulation(precip_data=_serie_sintetica(365), lower_tank_vol=float('nan'), **AUDITORIA_DO_MOTOR_BASE)


def test_modo_de_descarte_desconhecido_e_recusado():
    args = dict(AUDITORIA_DO_MOTOR_BASE)
    args['discard_mode'] = 7
    with pytest.raises(ValueError, match='Modo de descarte'):
        run_single_simulation(precip_data=_serie_sintetica(365), lower_tank_vol=2000.0, **args)


def test_modo_3_exige_intervalo_positivo():
    args = dict(AUDITORIA_DO_MOTOR_BASE)
    args['discard_mode'] = 3
    with pytest.raises(ValueError, match='Intervalo'):
        run_single_simulation(precip_data=_serie_sintetica(365), lower_tank_vol=2000.0, discard_days_interval=0, **args)


@pytest.mark.parametrize('reserva', [True, False])
def test_varredura_preserva_irrigacao_e_suprimento_de_reserva(reserva):
    """O volume da varredura e a simulação única do mesmo volume coincidem.

    Com a reserva desligada a varredura comprava da rede a irrigação que a
    simulação única deixava sem atender: 467 contra 445 L/dia de água potável
    no caso da auditoria, com a demanda não atendida zerada e os dias de
    irrigação suprimida também.
    """
    edificacao = dict(demand_mode='constant', demand=150.0, residents=4, share=0.4, non_potable_indoor_share=0.35, irrigation_liters_per_day=80.0, irrigation_rain_threshold_mm=2.0, irrigation_potable_backup=reserva)
    kw = dict(AUDITORIA_DO_MOTOR_BASE, building_config=edificacao)
    chuva = _serie_sintetica()
    unica = run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0, **kw)
    varredura = run_sweep_simulation(precip_data=chuva, lower_tank_max=2000.0, lower_tank_step=1000.0, **kw)
    mesmo = [x for x in varredura.results_by_volume if x.lower_tank_vol == 2000.0][0]
    for campo in ('potential_potable_savings_pct', 'avg_potable_consumed_l_day', 'avg_unmet_demand_l_day', 'avg_pluvial_irrigation_consumed_l_day', 'avg_pluvial_indoor_consumed_l_day', 'total_irrigation_days_suppressed'):
        assert getattr(mesmo, campo) == pytest.approx(getattr(unica, campo)), campo


# ---- origem: tests/unit/test_validacao_fisica.py

_VALIDO = dict(area=120.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4, upper_tank_vol=500.0)


@pytest.fixture(scope='module')
def validacao_fisica_chuva():
    rng = np.random.default_rng(42)
    return np.clip(rng.gamma(0.6, 9.0, 730), 0, None)


def _validacao_fisica_simular(validacao_fisica_chuva, volume=5000.0, **trocas):
    kw = dict(_VALIDO)
    kw.update(trocas)
    return run_single_simulation(precip_data=validacao_fisica_chuva, lower_tank_vol=volume, pumping_threshold=50.0, **kw)


@pytest.mark.parametrize(('campo', 'valor', 'termo'), [('area', -100.0, 'Area'), ('runoff_coeff', -0.5, 'escoamento'), ('runoff_coeff', 1.8, 'escoamento'), ('discard_mm', -5.0, 'descarte'), ('total_demand_per_day', -80.0, 'Demanda'), ('rainwater_share', 2.5, 'Fracao'), ('rainwater_share', -0.3, 'Fracao'), ('upper_tank_vol', -200.0, 'superior')])
def test_parametro_impossivel_e_rejeitado(validacao_fisica_chuva, campo, valor, termo):
    with pytest.raises(ValueError, match=termo):
        _validacao_fisica_simular(validacao_fisica_chuva, **{campo: valor})


def test_volume_negativo_e_rejeitado(validacao_fisica_chuva):
    """Devolvia −166,67% de economia, e o número seguia para o relatório."""
    with pytest.raises(ValueError, match='negativo'):
        _validacao_fisica_simular(validacao_fisica_chuva, volume=-1000.0)


def test_a_mensagem_diz_o_campo_e_o_valor(validacao_fisica_chuva):
    """Erro que não nomeia o campo obriga o usuário a caçar o problema."""
    with pytest.raises(ValueError) as erro:
        _validacao_fisica_simular(validacao_fisica_chuva, runoff_coeff=1.8)
    texto = str(erro.value)
    assert '1.8' in texto
    assert '0,80' in texto and '0,95' in texto


def test_volume_zero_continua_valido(validacao_fisica_chuva):
    """É a referência «sem sistema» da varredura, e não pode ser rejeitada."""
    r = _validacao_fisica_simular(validacao_fisica_chuva, volume=0.0)
    assert r.potential_potable_savings_pct == pytest.approx(0.0)


@pytest.mark.parametrize('coef', [0.0, 0.5, 0.8, 0.95, 1.0])
def test_a_faixa_valida_do_coeficiente_passa_inteira(validacao_fisica_chuva, coef):
    """Os extremos 0 e 1 são legítimos: telhado impermeável ideal e captação nula."""
    assert _validacao_fisica_simular(validacao_fisica_chuva, runoff_coeff=coef).potential_potable_savings_pct >= 0.0


def test_sem_reservatorio_superior_continua_valido(validacao_fisica_chuva):
    assert _validacao_fisica_simular(validacao_fisica_chuva, upper_tank_vol=0.0) is not None


def test_demanda_zero_continua_valida(validacao_fisica_chuva):
    """Edificação sem consumo é caso-limite legítimo, e dá economia nula."""
    assert _validacao_fisica_simular(validacao_fisica_chuva, total_demand_per_day=0.0).potential_potable_savings_pct == pytest.approx(0.0)


def test_o_potencial_fica_sempre_entre_zero_e_cem(validacao_fisica_chuva):
    """A invariante que a validação existe para garantir.

    Antes, três entradas diferentes produziam percentual fora de [0, 100], e
    nenhuma delas era detectada.
    """
    for volume in (0.0, 500.0, 2000.0, 5000.0, 20000.0):
        for coef in (0.0, 0.5, 0.85, 1.0):
            for area in (0.0, 50.0, 400.0):
                r = _validacao_fisica_simular(validacao_fisica_chuva, volume=volume, runoff_coeff=coef, area=area)
                assert 0.0 <= r.potential_potable_savings_pct <= 100.0, (volume, coef, area)


def test_o_validador_e_chamavel_isoladamente():
    """Serve à interface, que pode conferir antes de rodar a simulação inteira."""
    validar_parametros_fisicos(lower_tank_vol=5000.0, area=120.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4)
    with pytest.raises(ValueError):
        validar_parametros_fisicos(lower_tank_vol=5000.0, area=-1.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4)


# ---- origem: tests/unit/test_tres_fracoes.py
_ARQUIVO_TRES_FRACOES = str(_TESTES / 'unit/test_tres_fracoes.py')

TRES_FRACOES_RAIZ = Path(_ARQUIVO_TRES_FRACOES).resolve().parents[2]


_c_sweep = TRES_FRACOES_RAIZ / 'manual' / 'casos' / '04_tutorial_sweep.triton'
_c_varr = TRES_FRACOES_RAIZ / 'manual' / 'casos' / '04_tutorial_varredura.triton'
_c_antigo = TRES_FRACOES_RAIZ / 'manual' / 'casos' / '02_tutorial_varredura.triton'
TRES_FRACOES_CASO = _c_sweep if _c_sweep.exists() else (_c_varr if _c_varr.exists() else _c_antigo)


def test_total_derivada_da_interna_e_da_externa():
    assert fracao_total(600.0, 0.3, 150.0) == pytest.approx(0.44)
    assert fracao_total(600.0, 0.3, 0.0) == pytest.approx(0.3)
    assert fracao_interna_da_total(600.0, 0.44, 150.0) == pytest.approx(0.3)


def test_total_impossivel_e_recusada():
    with pytest.raises(ValueError, match='impossível'):
        fracao_interna_da_total(600.0, 0.1, 150.0)


def _tres_fracoes_arquivo(tmp_path, interna, externa, jardim=0.0):
    d = json.loads(TRES_FRACOES_CASO.read_text(encoding='utf-8'))
    i = d['inputs']
    i['incentives_and_shares']['non_potable_indoor_share'] = interna
    i['incentives_and_shares']['potable_indoor_share'] = 1 - interna
    i['irrigation']['liters_per_day'] = externa
    i['irrigation']['garden_area_m2'] = jardim
    p = tmp_path / 'caso.triton'
    p.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    return p


def test_arquivo_antigo_com_padroes_vazados_vale_a_total(tmp_path):
    """Antes da 0.1.0 a interna e a externa eram gravadas com os padrões."""
    r = load_triton_project(str(_tres_fracoes_arquivo(tmp_path, 0.35, 50.0)))
    c = r['config']
    assert (c.rainwater_share, c.non_potable_indoor_share, c.irrigation_liters_per_day) == (0.28, 0.28, 0.0)
    assert r['aviso_fracoes'] and 'vale a total' in r['aviso_fracoes']


def test_arquivo_coerente_com_demanda_externa_e_preservado(tmp_path):
    d = json.loads(TRES_FRACOES_CASO.read_text(encoding='utf-8'))
    total = (0.2 * 600 + 100) / 700
    d['inputs']['building_and_demand']['rainwater_share'] = total
    p = _tres_fracoes_arquivo(tmp_path, 0.2, 100.0, jardim=30.0)
    d2 = json.loads(p.read_text(encoding='utf-8'))
    d2['inputs']['building_and_demand']['rainwater_share'] = total
    p.write_text(json.dumps(d2), encoding='utf-8')
    r = load_triton_project(str(p))
    c = r['config']
    assert c.non_potable_indoor_share == pytest.approx(0.2)
    assert c.irrigation_liters_per_day == pytest.approx(100.0)
    assert r['aviso_fracoes'] is None


def test_alterar_a_total_recalcula_a_interna():
    c = load_triton_project(str(TRES_FRACOES_CASO))['config']
    c.rainwater_share = 0.4
    conciliar_fracoes(c)
    assert c.non_potable_indoor_share == pytest.approx(0.4)


def test_alterar_a_interna_recalcula_a_total():
    c = load_triton_project(str(TRES_FRACOES_CASO))['config']
    c.non_potable_indoor_share = 0.2
    c.irrigation_liters_per_day = 150.0
    conciliar_fracoes(c)
    assert c.rainwater_share == pytest.approx((0.2 * 600 + 150) / 750)


def test_alterar_as_duas_em_desacordo_e_erro():
    c = load_triton_project(str(TRES_FRACOES_CASO))['config']
    c.rainwater_share, c.non_potable_indoor_share = (0.5, 0.2)
    with pytest.raises(ValueError, match='Altere só uma'):
        conciliar_fracoes(c)


def test_config_montada_no_codigo_vale_a_total():
    c = TritonConfig(rainwater_share=0.55)
    conciliar_fracoes(c)
    assert c.non_potable_indoor_share == pytest.approx(0.55)
    assert c.potable_indoor_share == pytest.approx(0.45)


@pytest.mark.parametrize('modo', ['constant', 'weekly', 'monthly'])
def test_motor_aplica_a_interna_a_demanda_interna_em_todos_os_modos(modo):
    """A total inclui a externa; aplicada ao consumo interno, contaria a externa duas vezes."""
    n = 60
    b = {'demand': 150.0, 'residents': 4, 'share': 0.44, 'non_potable_indoor_share': 0.3, 'irrigation_liters_per_day': 150.0, 'irrigation_rain_threshold_mm': 2.0, 'demand_mode': modo}
    if modo == 'weekly':
        b.update(weekly_demands=[150.0] * 7, weekly_residents=[4] * 7, weekly_shares=None)
    if modo == 'monthly':
        b.update(monthly_demands=[150.0] * 12, monthly_residents=[4] * 12, monthly_shares=None)
    tot, pluv, pot_in, non_pot_in, irr, _ = build_detailed_daily_demand_vectors(n_days=n, building_config=b, precip_data=np.zeros(n))
    assert np.allclose(non_pot_in, 600.0 * 0.3)
    assert np.allclose(irr, 150.0)
    assert np.allclose(pluv / tot, 0.44)


def test_projetos_distribuidos_sao_coerentes():
    """Nenhum projeto que acompanha o programa precisa de conciliação ao abrir."""
    arquivos = sorted((TRES_FRACOES_RAIZ / 'manual' / 'casos').glob('*.triton')) + sorted((TRES_FRACOES_RAIZ / 'examples').glob('estudo_caso_*.triton'))
    assert arquivos
    for arq in arquivos:
        assert load_triton_project(str(arq))['aviso_fracoes'] is None, arq.name


# ---- origem: tests/unit/test_fechamento_do_balanco.py

_CFG = {'demand': 150.0, 'residents': 4, 'share': 0.4, 'non_potable_indoor_share': 0.35, 'irrigation_liters_per_day': 120.0, 'irrigation_rain_threshold_mm': 2.0}


@pytest.fixture(scope='module')
def fechamento_do_balanco_chuva():
    rng = np.random.default_rng(19)
    return np.clip(rng.gamma(0.55, 8.0, 1826), 0, None)


def _rodar(fechamento_do_balanco_chuva, backup=True, detalhe=False, duplo=False):
    kw = dict(precip_data=fechamento_do_balanco_chuva, lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4, building_config=dict(_CFG, irrigation_potable_backup=backup), store_daily_details=detalhe)
    if duplo:
        kw.update(upper_tank_vol=800.0, upper_tank_used=True, pumping_threshold=80.0)
    return run_single_simulation(**kw)


def test_desligar_a_reserva_reduz_o_potavel(fechamento_do_balanco_chuva):
    """Era o defeito: a escolha não mexia um litro no resumo."""
    com = _rodar(fechamento_do_balanco_chuva, backup=True)
    sem = _rodar(fechamento_do_balanco_chuva, backup=False)
    assert sem.avg_potable_consumed_l_day < com.avg_potable_consumed_l_day


def test_o_resumo_concorda_com_a_serie_diaria(fechamento_do_balanco_chuva):
    """Dois números do mesmo objeto não podem se contradizer."""
    for backup in (True, False):
        r = _rodar(fechamento_do_balanco_chuva, backup=backup, detalhe=True)
        serie = sum((d.potable_consumed_liters for d in r.daily_results)) / len(r.daily_results)
        assert r.avg_potable_consumed_l_day == pytest.approx(serie, rel=1e-09)


def test_com_a_reserva_ligada_nada_muda(fechamento_do_balanco_chuva):
    """O padrão do programa: as duas fórmulas coincidem exatamente."""
    r = _rodar(fechamento_do_balanco_chuva, backup=True, detalhe=True)
    por_diferenca = sum((d.total_demand_liters - d.pluvial_consumed_liters for d in r.daily_results)) / len(r.daily_results)
    assert r.avg_potable_consumed_l_day == pytest.approx(por_diferenca, rel=1e-09)
    assert r.avg_unmet_demand_l_day == pytest.approx(0.0)


@pytest.mark.parametrize('backup', [True, False])
@pytest.mark.parametrize('duplo', [False, True])
def test_a_demanda_e_a_soma_de_tres_parcelas(fechamento_do_balanco_chuva, backup, duplo):
    """demanda total = pluvial + potável + não atendida."""
    r = _rodar(fechamento_do_balanco_chuva, backup=backup, detalhe=True, duplo=duplo)
    demanda = sum((d.total_demand_liters for d in r.daily_results)) / len(r.daily_results)
    soma = r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day + r.avg_unmet_demand_l_day
    assert soma == pytest.approx(demanda, rel=1e-09)


def test_a_nao_atendida_so_aparece_sem_reserva(fechamento_do_balanco_chuva):
    assert _rodar(fechamento_do_balanco_chuva, backup=True).avg_unmet_demand_l_day == pytest.approx(0.0)
    assert _rodar(fechamento_do_balanco_chuva, backup=False).avg_unmet_demand_l_day > 0.0


def test_sem_irrigacao_nao_ha_demanda_nao_atendida(fechamento_do_balanco_chuva):
    """Sem jardim cadastrado, a bandeira não tem sobre o que agir."""
    r = run_single_simulation(precip_data=fechamento_do_balanco_chuva, lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4, building_config={'demand': 150.0, 'residents': 4, 'share': 0.4, 'irrigation_potable_backup': False})
    assert r.avg_unmet_demand_l_day == pytest.approx(0.0)


@pytest.mark.skipif(not S.HAS_NUMBA, reason='núcleo compilado não instalado')
@pytest.mark.parametrize('backup', [True, False])
@pytest.mark.parametrize('duplo', [False, True])
def test_o_nucleo_compilado_concorda_com_o_python(fechamento_do_balanco_chuva, backup, duplo):
    """O kernel não recebia a bandeira: com ele ativo, a escolha era ignorada."""
    kernel = _rodar(fechamento_do_balanco_chuva, backup=backup, detalhe=False, duplo=duplo)
    puro = _rodar(fechamento_do_balanco_chuva, backup=backup, detalhe=True, duplo=duplo)
    assert kernel.avg_potable_consumed_l_day == pytest.approx(puro.avg_potable_consumed_l_day, rel=1e-09)
    assert kernel.avg_unmet_demand_l_day == pytest.approx(puro.avg_unmet_demand_l_day, rel=1e-09)
    assert kernel.avg_pluvial_consumed_l_day == pytest.approx(puro.avg_pluvial_consumed_l_day, rel=1e-09)


# ---- origem: tests/unit/test_simulation.py
_ARQUIVO_SIMULATION = str(_TESTES / 'unit/test_simulation.py')

SIMULATION_WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_SIMULATION)))


@pytest.fixture
def fpolis_precip():
    # Série da Edição Brasil: os testes que a usam estão em tests/so_da_brl.txt.
    return load_precipitation(os.path.join(SIMULATION_WORKSPACE_DIR, 'data', 'rainfall', 'Florianopolis1.csv'))

def test_extreme_rain_simulation():
    """Verify that constant high rain fills tank, maximizes potential savings, and generates spillover."""
    heavy_precip = np.full(365, 100.0, dtype=np.float64)
    res = run_single_simulation(precip_data=heavy_precip, lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.9, discard_mm=1.0, total_demand_per_day=300.0, rainwater_share=0.4)
    assert abs(res.avg_pluvial_consumed_l_day - 120.0) < 0.1
    assert abs(res.potential_potable_savings_pct - 40.0) < 0.1
    assert res.pct_days_full_satisfaction == 100.0
    assert res.avg_spilled_l_day > 8000.0


def test_dual_tank_pumping(fpolis_precip):
    """Verify dual tank pumping threshold logic."""
    res = run_single_simulation(precip_data=fpolis_precip, lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.9, discard_mm=1.0, total_demand_per_day=300.0, rainwater_share=0.4, upper_tank_vol=500.0, upper_tank_used=True, pumping_threshold=375.0)
    assert res.total_pumped_liters > 0.0
    assert res.total_pump_cycles > 0
    assert res.potential_potable_savings_pct > 30.0


def test_higher_pump_threshold_increases_starts_and_reduces_batch_size():
    """Higher triggers start earlier; they do not prescribe total annual transfer."""
    regular_rain = np.full(30, 10.0, dtype=np.float64)
    common = dict(precip_data=regular_rain, lower_tank_vol=5000.0, area=100.0, runoff_coeff=0.8, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.4, upper_tank_vol=500.0, upper_tank_used=True)
    responsive = run_single_simulation(**common, pumping_threshold=50.0)
    conservative = run_single_simulation(**common, pumping_threshold=250.0)
    assert conservative.total_pump_cycles > responsive.total_pump_cycles
    assert conservative.average_pumped_liters_per_cycle < responsive.average_pumped_liters_per_cycle
    assert abs(conservative.total_pumped_liters - responsive.total_pumped_liters) <= 500.0


def _chuva_sintetica_umida(anos=10):
    """Série diária determinística (sem arquivo): um aguaceiro de 25 mm a cada 8 dias, outro de 6 mm a meio."""
    ciclo = np.array([0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, 25.0], dtype=np.float64)
    return np.tile(ciclo, int(anos * 365.25 / 8))


def test_dual_tank_pumping_com_chuva_sintetica():
    """O mesmo teste do reservatório duplo, com uma série que não é de nenhum local (roda em todas as edições)."""
    res = run_single_simulation(precip_data=_chuva_sintetica_umida(), lower_tank_vol=2000.0, area=100.0, runoff_coeff=0.9, discard_mm=1.0, total_demand_per_day=300.0, rainwater_share=0.4, upper_tank_vol=500.0, upper_tank_used=True, pumping_threshold=375.0)
    assert res.total_pumped_liters > 0.0
    assert res.total_pump_cycles > 0
    assert 0.0 < res.potential_potable_savings_pct <= 40.0 + 1e-9  # nunca passa da fração atendida pela chuva


def test_varredura_de_volumes_com_chuva_sintetica():
    """Varredura do reservatório inferior: grade, passo e ótimo coerentes, sem depender de série real."""
    sweep = run_sweep_simulation(precip_data=_chuva_sintetica_umida(), lower_tank_max=10000.0, lower_tank_step=250.0, area=100.0, runoff_coeff=0.9, discard_mm=1.0, total_demand_per_day=300.0, rainwater_share=0.4, delta_ideal_threshold=1.0)
    assert sweep.optimal_lower_tank_vol is not None and 0.0 < sweep.optimal_lower_tank_vol <= 10000.0
    assert sweep.optimal_lower_tank_vol % 250.0 == 0.0
    assert len(sweep.results_by_volume) == 41
    assert sweep.effective_step_l == 250.0 and sweep.step_adjusted is False
    pct = [r.potential_potable_savings_pct for r in sweep.results_by_volume]
    assert all(b >= a - 1e-9 for a, b in zip(pct, pct[1:])), 'mais reservatório nunca economiza menos água potável'


@pytest.mark.parametrize('threshold', [0.0, 50.0, 250.0, 500.0, 900.0])
def test_pump_threshold_is_bounded_and_internal_transfer_is_mass_conservative(threshold):
    result = run_single_simulation(precip_data=np.full(30, 10.0, dtype=np.float64), lower_tank_vol=5000.0, area=100.0, runoff_coeff=0.8, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.4, upper_tank_vol=500.0, upper_tank_used=True, pumping_threshold=threshold, store_daily_details=True)
    final_upper = result.daily_results[-1].upper_tank_end_liters
    total_consumed_from_upper = sum((day.pluvial_consumed_liters for day in result.daily_results))
    assert 0.0 <= final_upper <= 500.0
    assert result.total_pumped_liters == pytest.approx(total_consumed_from_upper + final_upper)
    assert result.max_pump_batch_liters <= 500.0
    assert all((day.pumped_liters <= day.pump_cycles * 500.0 for day in result.daily_results))


@pytest.mark.parametrize('upper_volume', [320.0, 500.0, 1000.0])
def test_pump_batch_is_limited_by_each_configured_upper_tank_volume(upper_volume):
    result = run_single_simulation(precip_data=np.full(30, 10.0, dtype=np.float64), lower_tank_vol=5000.0, area=100.0, runoff_coeff=0.8, discard_mm=0.0, total_demand_per_day=1000.0, rainwater_share=0.4, upper_tank_vol=upper_volume, upper_tank_used=True, pumping_threshold=upper_volume * 0.5, store_daily_details=True)
    assert result.total_pump_cycles > 0
    assert result.max_pump_batch_liters <= upper_volume
    assert all((day.upper_tank_end_liters <= upper_volume for day in result.daily_results))
    assert all((day.pumped_liters <= day.pump_cycles * upper_volume for day in result.daily_results))


def test_sweep_optimal_volume_determination(fpolis_precip):
    """Verify lower tank range sweep and optimal volume determination algorithm."""
    sweep = run_sweep_simulation(precip_data=fpolis_precip, lower_tank_max=10000.0, lower_tank_step=250.0, area=100.0, runoff_coeff=0.9, discard_mm=1.0, total_demand_per_day=300.0, rainwater_share=0.4, delta_ideal_threshold=1.0)
    assert sweep.optimal_lower_tank_vol is not None
    assert sweep.optimal_lower_tank_vol in [2250.0, 2500.0, 2750.0, 3000.0, 3250.0, 3500.0, 3750.0, 4000.0, 4500.0]
    assert sweep.optimal_potential_pct > 35.0
    assert len(sweep.results_by_volume) == 41
    assert sweep.effective_step_l == 250.0
    assert sweep.step_adjusted is False


def test_sweep_grid_allows_40_positive_volumes_plus_zero_reference():
    grid = build_sweep_volume_grid(10000.0, 250.0)
    assert grid.positive_volume_count == 40
    assert len(grid.volumes_l) == 41
    assert grid.volumes_l[0] == 0.0
    assert grid.volumes_l[-1] == 10000.0
    assert grid.effective_step_l == 250.0
    assert grid.step_adjusted is False


def test_sweep_grid_doubles_step_above_40_and_keeps_exact_maximum():
    grid = build_sweep_volume_grid(10001.0, 250.0)
    assert grid.effective_step_l == 500.0
    assert grid.step_adjusted is True
    assert grid.positive_volume_count == 21
    assert grid.volumes_l[-2] == 10000.0
    assert grid.volumes_l[-1] == 10001.0
    assert grid.volumes_l[-1] - grid.volumes_l[-2] == 1.0


def test_sweep_grid_rounds_step_up_to_250_l_multiple_before_doubling():
    grid = build_sweep_volume_grid(25000.0, 300.0)
    assert grid.effective_step_l == 1000.0
    assert grid.effective_step_l % 250.0 == 0.0
    assert grid.positive_volume_count == 25
    assert grid.volumes_l[-1] == 25000.0


def test_monthly_potable_use_tracks_each_days_variable_demand():
    result = run_single_simulation(precip_data=np.zeros(32, dtype=np.float64), lower_tank_vol=1000.0, total_demand_per_day=999.0, rainwater_share=0.4, monthly_demands=[100.0, 200.0] + [100.0] * 10, monthly_residents=[1] * 12, start_date_str='01/01/2024', store_daily_details=True)
    assert result.daily_results[0].potable_consumed_liters == pytest.approx(100.0)
    assert result.daily_results[30].potable_consumed_liters == pytest.approx(100.0)
    assert result.daily_results[31].potable_consumed_liters == pytest.approx(200.0)


# ---- origem: tests/unit/test_discretized_demand_irrigation.py

def test_discretized_indoor_and_irrigation_vectors():
    """Valida se a construção de vetores separa corretamente potável interno, não-potável interno e irrigação."""
    n_days = 5
    precip = np.array([0.0, 1.0, 2.5, 10.0, 0.0], dtype=np.float64)
    b_cfg = {'demand': 150.0, 'residents': 4.0, 'potable_indoor_share': 0.65, 'non_potable_indoor_share': 0.35, 'irrigation_liters_per_day': 50.0, 'irrigation_rain_threshold_mm': 2.0, 'irrigation_potable_backup': True}
    tot_arr, pluv_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_supp_mask = build_detailed_daily_demand_vectors(n_days=n_days, building_config=b_cfg, precip_data=precip)
    assert np.allclose(pot_in_arr, 390.0)
    assert np.allclose(non_pot_in_arr, 210.0)
    assert irr_arr[0] == 50.0
    assert irr_arr[1] == 50.0
    assert irr_arr[2] == 0.0
    assert irr_arr[3] == 0.0
    assert irr_arr[4] == 50.0
    assert not irr_supp_mask[0]
    assert not irr_supp_mask[1]
    assert irr_supp_mask[2]
    assert irr_supp_mask[3]
    assert not irr_supp_mask[4]
    assert pluv_arr[0] == 260.0
    assert pluv_arr[1] == 260.0
    assert pluv_arr[2] == 210.0
    assert pluv_arr[3] == 210.0
    assert pluv_arr[4] == 260.0
    assert tot_arr[0] == 650.0
    assert tot_arr[1] == 650.0
    assert tot_arr[2] == 600.0
    assert tot_arr[3] == 600.0
    assert tot_arr[4] == 650.0


def test_hydraulic_priority_and_potable_backup():
    """
    Valida se a cisterna atende primeiro o não-potável interno (bacias/máquinas)
    e somente o saldo excedente vai para a irrigação externa.
    """
    precip = np.array([10.0, 0.0, 0.0], dtype=np.float64)
    b_cfg = {'demand': 100.0, 'residents': 2.0, 'potable_indoor_share': 0.5, 'non_potable_indoor_share': 0.5, 'irrigation_liters_per_day': 80.0, 'irrigation_rain_threshold_mm': 2.0, 'irrigation_potable_backup': True}
    res = run_single_simulation(precip_data=precip, lower_tank_vol=5000.0, area=100.0, runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True, building_config=b_cfg)
    d0 = res.daily_results[0]
    assert d0.irrigation_suppressed is True
    assert d0.irrigation_demand_liters == 0.0
    assert d0.pluvial_indoor_consumed_liters == 100.0
    assert d0.pluvial_irrigation_consumed_liters == 0.0
    d1 = res.daily_results[1]
    assert d1.irrigation_suppressed is False
    assert d1.irrigation_demand_liters == 80.0
    assert d1.pluvial_indoor_consumed_liters == 100.0
    assert d1.pluvial_irrigation_consumed_liters == 80.0
    assert res.total_irrigation_days_suppressed == 1
    assert res.total_irrigation_days_active == 2


def test_irrigation_without_potable_backup():
    """Valida se, sem backup potável para irrigação, a concessionária não é cobrada pela irrigação se a cisterna secar."""
    precip = np.array([0.0, 0.0], dtype=np.float64)
    b_cfg = {'demand': 100.0, 'residents': 2.0, 'potable_indoor_share': 0.5, 'non_potable_indoor_share': 0.5, 'irrigation_liters_per_day': 50.0, 'irrigation_rain_threshold_mm': 2.0, 'irrigation_potable_backup': False}
    res = run_single_simulation(precip_data=precip, lower_tank_vol=1000.0, area=100.0, runoff_coeff=0.9, discard_mm=0.0, store_daily_details=True, building_config=b_cfg)
    d0 = res.daily_results[0]
    assert d0.pluvial_consumed_liters == 0.0
    assert d0.potable_consumed_liters == 200.0


def test_parser_discretized_roundtrip():
    """Valida salvamento e carregamento de configurações com discretização de usos."""
    cfg = TritonConfig(potable_indoor_share=0.7, non_potable_indoor_share=0.3, irrigation_liters_per_day=75.0, irrigation_rain_threshold_mm=3.0, irrigation_potable_backup=False)
    assert cfg.potable_indoor_share == 0.7
    assert cfg.non_potable_indoor_share == 0.3
    assert cfg.irrigation_liters_per_day == 75.0
    assert cfg.irrigation_rain_threshold_mm == 3.0
    assert cfg.irrigation_potable_backup is False


def test_discretized_weekly_modulation_with_irrigation():
    """Valida se a modulação semanal separa corretamente frações internas e adiciona irrigação."""
    n_days = 7
    precip = np.array([0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float64)
    b_cfg = {'demand_mode': 'weekly', 'weekly_demands': [100.0, 100.0, 100.0, 100.0, 100.0, 200.0, 200.0], 'weekly_residents': [4.0] * 7, 'weekly_shares': [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5], 'irrigation_liters_per_day': 60.0, 'irrigation_rain_threshold_mm': 2.0, 'irrigation_potable_backup': True}
    tot_arr, pluv_arr, pot_in_arr, non_pot_in_arr, irr_arr, irr_supp_mask = build_detailed_daily_demand_vectors(n_days=n_days, building_config=b_cfg, precip_data=precip, start_date_str='07/01/2002')
    assert pot_in_arr[0] == 280.0
    assert non_pot_in_arr[0] == 120.0
    assert irr_arr[0] == 60.0
    assert pluv_arr[0] == 180.0
    assert tot_arr[0] == 460.0
    assert bool(irr_supp_mask[2]) is True
    assert irr_arr[2] == 0.0
    assert pluv_arr[2] == 120.0
    assert pot_in_arr[5] == 400.0
    assert non_pot_in_arr[5] == 400.0
    assert irr_arr[5] == 60.0
    assert pluv_arr[5] == 460.0


# ---- origem: tests/unit/test_water_quality.py

def test_first_flush_washoff_defaults():
    res = calculate_first_flush_washoff(discard_mm=2.0, roof_area_m2=200.0, annual_precipitation_mm=1400.0, roof_runoff_coeff=0.85)
    assert isinstance(res, FirstFlushAnalysis)
    assert res.discard_mm == 2.0
    assert res.annual_discard_volume_m3 > 0
    assert 0 < res.removal_coarse_solids_pct <= 100.0
    assert res.estimated_raw_turbidity_ntu > res.estimated_post_discard_turbidity_ntu


def test_first_flush_zero_discard():
    res = calculate_first_flush_washoff(discard_mm=0.0, roof_area_m2=150.0, annual_precipitation_mm=1200.0)
    assert res.annual_discard_volume_m3 == 0.0
    assert res.removal_coarse_solids_pct == 0.0


def test_water_quality_classes_nbr15527():
    assert 'classe_1' in WATER_QUALITY_CLASSES
    assert 'classe_2' in WATER_QUALITY_CLASSES
    assert 'classe_3' in WATER_QUALITY_CLASSES
    assert 'classe_4' in WATER_QUALITY_CLASSES
    c1 = WATER_QUALITY_CLASSES['classe_1']
    assert c1.turbidez_max_ntu <= 5.0
    assert c1.exige_desinfeccao is True


def test_size_etap():
    res = size_etap(target_class_id='classe_1', annual_pluvial_consumed_m3=300.0, roof_area_m2=250.0, disinfection_choice='cloro', include_polishing_filter=True)
    assert isinstance(res, EtapSizingResult)
    assert res.total_etap_capex > 0
    assert res.total_etap_annual_opex > 0
    assert res.total_etap_co2e_kg_yr >= 0
    assert res.annual_chlorine_kg > 0


def test_size_first_flush_system_small_diverter():
    from triton.core.water_quality import size_first_flush_system, FirstFlushSizingResult
    res = size_first_flush_system(discard_mm=1.0, roof_area_m2=100.0)
    assert isinstance(res, FirstFlushSizingResult)
    assert res.diverter_volume_liters == 100.0
    assert 'PVC' in res.diverter_tank_type
    assert res.leaf_filter_capex > 0
    assert res.diverter_tank_capex > 0
    assert res.first_flush_total_capex == res.leaf_filter_capex + res.diverter_tank_capex
    assert res.first_flush_embodied_co2_kg > 0
    assert res.first_flush_annual_opex > 0


def test_size_first_flush_system_large_diverter():
    from triton.core.water_quality import size_first_flush_system
    res = size_first_flush_system(discard_mm=2.0, roof_area_m2=500.0)
    assert res.diverter_volume_liters == 1000.0
    assert 'PEAD' in res.diverter_tank_type
    assert res.first_flush_total_capex > 0
    assert res.first_flush_embodied_co2_kg > 0


def test_size_first_flush_system_zero():
    from triton.core.water_quality import size_first_flush_system
    res = size_first_flush_system(discard_mm=0.0, roof_area_m2=100.0)
    assert res.diverter_volume_liters == 0.0
    assert res.first_flush_total_capex == 0.0
    assert res.first_flush_embodied_co2_kg == 0.0


def test_size_etap_with_first_flush_integration():
    from triton.core.water_quality import size_etap
    res_sem = size_etap(target_class_id='classe_1', annual_pluvial_consumed_m3=120.0, roof_area_m2=100.0, discard_mm=1.0, include_first_flush=False)
    res_com = size_etap(target_class_id='classe_1', annual_pluvial_consumed_m3=120.0, roof_area_m2=100.0, discard_mm=1.0, include_first_flush=True)
    assert res_com.first_flush is not None
    assert res_com.first_flush_diverter_vol_l == 100.0
    assert res_com.first_flush_capex > 0
    assert res_com.total_etap_capex == pytest.approx(res_sem.total_etap_capex + res_com.first_flush_capex)


# ---- origem: tests/unit/test_comprimento_de_serie.py
_ARQUIVO_COMPRIMENTO_DE_SERIE = str(_TESTES / 'unit/test_comprimento_de_serie.py')

COMPRIMENTO_DE_SERIE_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_COMPRIMENTO_DE_SERIE))))


if COMPRIMENTO_DE_SERIE_RAIZ not in sys.path:
    sys.path.insert(0, COMPRIMENTO_DE_SERIE_RAIZ)


COMPRIMENTO_DE_SERIE_PROJETO = dict(area=100.0, runoff_coeff=0.8, discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.3)


def serie_regular(anos, mm_por_dia=5.0):
    """Chuva igual todo dia: toda janela tem de reproduzir a série inteira."""
    return np.full(anos * DIAS_NO_ANO, mm_por_dia, dtype=float)


def test_serie_constante_basta_com_um_ano():
    r = analisar(serie_regular(6), COMPRIMENTO_DE_SERIE_PROJETO, volume_maximo_l=6000.0, passo_l=1000.0)
    assert r.comprimento_representativo_anos == 1
    assert r.serie_e_representativa
    assert r.frequencia_por_comprimento[1] == 100.0
    assert 'é representativa' in r.resumo()


def test_a_analise_recusa_serie_curta_demais():
    with pytest.raises(ValueError, match='dois anos'):
        analisar(serie_regular(1), COMPRIMENTO_DE_SERIE_PROJETO)


def test_o_volume_ideal_e_o_primeiro_abaixo_do_limiar():
    serie = serie_regular(4)
    volumes = [1000.0, 2000.0, 3000.0, 4000.0]
    escolhido, potenciais = volume_ideal(serie, volumes, 1.0, COMPRIMENTO_DE_SERIE_PROJETO)
    assert escolhido in volumes
    anterior = volumes[volumes.index(escolhido) - 1]
    ganho = (potenciais[escolhido] - potenciais[anterior]) / ((escolhido - anterior) / 1000.0)
    assert ganho <= 1.0


def test_a_amostragem_e_reproduzivel_com_a_mesma_semente():
    serie = np.random.default_rng(3).gamma(0.6, 8.0, 12 * DIAS_NO_ANO)
    comum = dict(volume_maximo_l=8000.0, passo_l=2000.0, amostra_por_comprimento=3)
    a = analisar(serie, COMPRIMENTO_DE_SERIE_PROJETO, semente=7, **comum)
    b = analisar(serie, COMPRIMENTO_DE_SERIE_PROJETO, semente=7, **comum)
    assert a.frequencia_por_comprimento == b.frequencia_por_comprimento
    assert a.janelas_por_comprimento[1] == 3


def test_a_amostragem_nao_inventa_janela_alem_das_que_existem():
    serie = np.random.default_rng(5).gamma(0.6, 8.0, 5 * DIAS_NO_ANO)
    r = analisar(serie, COMPRIMENTO_DE_SERIE_PROJETO, volume_maximo_l=6000.0, passo_l=2000.0, amostra_por_comprimento=50)
    assert r.janelas_por_comprimento[4] == 2
    assert r.janelas_por_comprimento[1] == 5


def test_o_comprimento_tem_de_se_manter_nos_maiores():
    """Um acerto isolado num comprimento curto não vale recomendação."""
    serie = np.random.default_rng(11).gamma(0.5, 9.0, 10 * DIAS_NO_ANO)
    r = analisar(serie, COMPRIMENTO_DE_SERIE_PROJETO, volume_maximo_l=6000.0, passo_l=2000.0, confianca_pct=90.0)
    if r.comprimento_representativo_anos is not None:
        maiores = range(r.comprimento_representativo_anos, r.anos_da_serie)
        assert all((r.frequencia_por_comprimento[a] >= 90.0 for a in maiores))


def test_serie_que_nao_estabiliza_avisa_em_vez_de_afirmar():
    r = analisar(serie_regular(4), COMPRIMENTO_DE_SERIE_PROJETO, volume_maximo_l=6000.0, passo_l=1000.0, confianca_pct=100.0, tolerancia_pp=0.0, tolerancia_passos=0)
    if r.comprimento_representativo_anos is None:
        assert not r.serie_e_representativa
        assert 'provisório' in r.resumo()


def test_a_serie_do_tutorial_estabiliza_dentro_dos_trinta_anos():
    sys.path.insert(0, os.path.join(COMPRIMENTO_DE_SERIE_RAIZ, 'manual'))
    from gerar_tabelas import _config_tutorial, _serie
    r = analisar(_serie(), dict(_config_tutorial()), volume_maximo_l=12000.0, passo_l=1000.0, limiar_ganho_pct_m3=1.0, amostra_por_comprimento=5)
    assert r.volume_ideal_l == pytest.approx(4000.0)
    assert r.potencial_no_ideal_pct == pytest.approx(27.12, abs=0.01)
    assert r.comprimento_representativo_anos is not None
    assert 1 <= r.comprimento_representativo_anos <= 30


# ---- origem: tests/unit/test_demanda_estocastica.py
_ARQUIVO_DEMANDA_ESTOCASTICA = str(_TESTES / 'unit/test_demanda_estocastica.py')

DEMANDA_ESTOCASTICA_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_DEMANDA_ESTOCASTICA))))


if DEMANDA_ESTOCASTICA_RAIZ not in sys.path:
    sys.path.insert(0, DEMANDA_ESTOCASTICA_RAIZ)


DEMANDA_ESTOCASTICA_PROJETO = dict(area=100.0, runoff_coeff=0.8, discard_mm=2.0, discard_mode=1, rainwater_share=0.3)


def demanda_estocastica_chuva(anos=8, semente=1):
    return np.random.default_rng(semente).gamma(0.6, 9.0, anos * 365)


@pytest.mark.parametrize('distribuicao', DISTRIBUICOES)
def test_o_sorteio_devolve_a_media_e_o_cv_pedidos(distribuicao):
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=25.0, distribuicao=distribuicao)
    valores = sortear_demanda(perfil, 40000, np.random.default_rng(2))
    assert float(np.mean(valores)) == pytest.approx(600.0, rel=0.02)
    cv = float(np.std(valores)) / float(np.mean(valores)) * 100.0
    assert cv == pytest.approx(25.0, rel=0.06)


def test_a_probabilidade_de_ausencia_zera_a_fracao_pedida_dos_dias():
    perfil = PerfilDeConsumo(media_l_dia=500.0, cv_pct=10.0, probabilidade_de_ausencia_pct=12.0)
    valores = sortear_demanda(perfil, 50000, np.random.default_rng(3))
    assert float(np.mean(valores == 0.0)) == pytest.approx(0.12, abs=0.01)


def test_o_piso_e_o_teto_limitam_o_sorteio():
    perfil = PerfilDeConsumo(media_l_dia=400.0, cv_pct=60.0, distribuicao='normal', minimo_l_dia=200.0, maximo_l_dia=600.0)
    valores = sortear_demanda(perfil, 5000, np.random.default_rng(4))
    assert valores.min() >= 200.0 and valores.max() <= 600.0


@pytest.mark.parametrize('perfil,mensagem', [(PerfilDeConsumo(media_l_dia=0.0), 'positiva'), (PerfilDeConsumo(media_l_dia=100.0, cv_pct=-1.0), 'negativo'), (PerfilDeConsumo(media_l_dia=100.0, probabilidade_de_ausencia_pct=120.0), '0 a 100'), (PerfilDeConsumo(media_l_dia=100.0, distribuicao='weibull'), 'Distribuição desconhecida'), (PerfilDeConsumo(media_l_dia=100.0, minimo_l_dia=50.0, maximo_l_dia=10.0), 'menor que o piso'), (PerfilDeConsumo(media_l_dia=100.0, incerteza_da_media_pct=-5.0), 'não pode ser negativa')])
def test_perfil_implausivel_e_recusado(perfil, mensagem):
    with pytest.raises(ValueError, match=mensagem):
        perfil.validar()


def test_sem_variacao_o_sorteio_devolve_o_deterministico():
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0)
    r = simular(demanda_estocastica_chuva(), 4000.0, perfil, DEMANDA_ESTOCASTICA_PROJETO, realizacoes=3)
    assert r['potencial_pct']['media'] == pytest.approx(r['deterministico']['potencial_pct'], abs=0.01)
    assert r['potencial_pct']['amplitude'] == pytest.approx(0.0, abs=0.001)


def test_a_mesma_semente_devolve_o_mesmo_resultado():
    perfil = PerfilDeConsumo(media_l_dia=600.0, cv_pct=20.0, incerteza_da_media_pct=10.0)
    a = simular(demanda_estocastica_chuva(), 4000.0, perfil, DEMANDA_ESTOCASTICA_PROJETO, realizacoes=8, semente=9)
    b = simular(demanda_estocastica_chuva(), 4000.0, perfil, DEMANDA_ESTOCASTICA_PROJETO, realizacoes=8, semente=9)
    assert a['potencial_pct'] == b['potencial_pct']


def test_o_ruido_diario_se_cancela_e_a_incerteza_do_nivel_nao():
    """O achado que o módulo documenta, e a razão de os dois parâmetros existirem.

    A comparação precisa de um sistema limitado pela oferta, que é onde o nível
    da demanda pesa. Num sistema com chuva sobrando o potencial é quase
    insensível à demanda, porque ela aparece no numerador e no denominador do
    indicador ao mesmo tempo — e é por isso que a série aqui é seca.
    """
    seca = np.random.default_rng(21).gamma(0.4, 3.0, 12 * 365)
    diario = simular(seca, 4000.0, PerfilDeConsumo(media_l_dia=600.0, cv_pct=25.0), DEMANDA_ESTOCASTICA_PROJETO, realizacoes=12)
    nivel = simular(seca, 4000.0, PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0, incerteza_da_media_pct=15.0), DEMANDA_ESTOCASTICA_PROJETO, realizacoes=12)
    assert diario['potencial_pct']['amplitude'] < 0.5
    assert nivel['potencial_pct']['amplitude'] > 2 * diario['potencial_pct']['amplitude']


def test_com_chuva_sobrando_o_nivel_da_demanda_quase_nao_muda_o_potencial():
    """A outra metade do achado: o regime decide se a incerteza importa."""
    farta = np.random.default_rng(22).gamma(0.9, 12.0, 12 * 365)
    nivel = simular(farta, 12000.0, PerfilDeConsumo(media_l_dia=600.0, cv_pct=0.0, incerteza_da_media_pct=15.0), DEMANDA_ESTOCASTICA_PROJETO, realizacoes=10)
    assert nivel['potencial_pct']['amplitude'] < 1.0


def test_a_media_sorteada_respeita_a_incerteza_declarada():
    perfil = PerfilDeConsumo(media_l_dia=600.0, incerteza_da_media_pct=20.0)
    gerador = np.random.default_rng(6)
    medias = [sortear_media(perfil, gerador) for _ in range(4000)]
    assert float(np.mean(medias)) == pytest.approx(600.0, rel=0.03)
    assert float(np.std(medias)) == pytest.approx(120.0, rel=0.08)
    assert sortear_media(PerfilDeConsumo(media_l_dia=600.0), gerador) == 600.0


def test_o_volume_ideal_sai_da_grade_e_varia_com_a_incerteza():
    volumes = [1000.0 * i for i in range(1, 9)]
    r = volume_ideal_por_realizacao(demanda_estocastica_chuva(anos=10), PerfilDeConsumo(media_l_dia=600.0, cv_pct=15.0, incerteza_da_media_pct=20.0), DEMANDA_ESTOCASTICA_PROJETO, volumes_l=volumes, realizacoes=6)
    assert set(r['volumes_distintos']) <= set(volumes)
    assert r['volume_ideal_l']['p5'] <= r['volume_ideal_l']['p95']


# ---- origem: tests/unit/test_calculator.py

def test_find_max_consecutive_run_length():
    assert find_max_consecutive_run_length(pd.Series([1, 1, 0, 0, 1, 1, 1, 1, 0])) == 4
    assert find_max_consecutive_run_length(pd.Series([0, 0, 0])) == 0
    assert find_max_consecutive_run_length(pd.Series([True, True, False, True])) == 2


def test_indices_use_wet_day_percentile_and_keep_windows_inside_year():
    """Protege R95p contra dias secos e RX5day contra vazamento entre anos."""
    start_dt = datetime(2020, 12, 29)
    rain = [10.0, 10.0, 10.0, 10.0, 10.0]
    calc = IndicesCalculator([(start_dt + timedelta(days=i), value) for i, value in enumerate(rain)], exclude_incomplete=False)
    indices = calc.compute_climate_indices().set_index('year')
    assert indices.loc[2020, 'RX5day'] == 30.0
    assert indices.loc[2021, 'RX5day'] == 20.0
    start_dt = datetime(2022, 1, 1)
    wet_day_reference = [0.0] * 80 + [float(value) for value in range(1, 21)]
    calc = IndicesCalculator([(start_dt + timedelta(days=i), value) for i, value in enumerate(wet_day_reference)], variable_name='rain_mm', exclude_incomplete=False)
    row = calc.compute_climate_indices().iloc[0]
    assert row['R95p'] == 20.0


def test_exclude_incomplete_years():
    start_dt = datetime(2021, 1, 1)
    rain = [5.0] * 365 + [2.0] * 10
    data_series = [(start_dt + timedelta(days=i), float(val)) for i, val in enumerate(rain)]
    calc_exclude = IndicesCalculator(data_series)
    df_exclude = calc_exclude.compute_climate_indices()
    assert list(df_exclude['year']) == [2021]
    calc_include = IndicesCalculator(data_series, exclude_incomplete=False)
    df_include = calc_include.compute_climate_indices()
    assert list(df_include['year']) == [2021, 2022]


# ---- origem: tests/unit/test_daily_water_balance.py

def test_simple_3day_water_balance():
    """
    Exemplo Didático de Balanço Hídrico de 3 dias:
    - Área: 100 m², Coeficiente C: 1.0, Descarte: 0.0 mm
    - Moradores: 4, Demanda per capita: 100 L/hab/dia -> Demanda Total = 400 L/dia
    - Substituição pluvial: 50% -> Demanda Pluvial = 200 L/dia
    - Reservatório inferior: 500 L (inicia vazio = 0 L)
    
    Chuva:
    - Dia 1: 5.0 mm -> Captação = 5 * 100 * 1.0 = 500 L
      - Reservatório recebe 500 L. Consumo pluvial = 200 L. Reservatório final = 300 L.
      - Atendimento: TOTAL (200 L).
    - Dia 2: 0.0 mm -> Captação = 0 L
      - Reservatório inicial = 300 L. Consumo pluvial = 200 L. Reservatório final = 100 L.
      - Atendimento: TOTAL (200 L).
    - Dia 3: 0.0 mm -> Captação = 0 L
      - Reservatório inicial = 100 L. Consumo pluvial = 100 L (limite do reservatório). Reservatório final = 0 L.
      - Atendimento: PARCIAL (100 L).
    """
    test_case = WaterBalanceTestCase(test_id='TEST_3DAY_SIMPLE', name='Teste Didático 3 Dias', input_rainfall=InputRainfall(rainfall_mm=[5.0, 0.0, 0.0]), input_data=InputData(area=100.0, runoff_coeff=1.0, discard_mm=0.0, residents=4, demand_per_capita=100.0, rainwater_share=0.5, lower_tank_vol=500.0))
    out = test_case.run()
    d1 = out.daily_details[0]
    assert d1.precip_mm == 5.0
    assert d1.harvested_liters == 500.0
    assert d1.pluvial_consumed_liters == 200.0
    assert d1.potable_consumed_liters == 200.0
    assert d1.lower_tank_end_liters == 300.0
    assert d1.satisfaction_type == 'TOTAL'
    d2 = out.daily_details[1]
    assert d2.precip_mm == 0.0
    assert d2.harvested_liters == 0.0
    assert d2.pluvial_consumed_liters == 200.0
    assert d2.potable_consumed_liters == 200.0
    assert d2.lower_tank_end_liters == 100.0
    assert d2.satisfaction_type == 'TOTAL'
    d3 = out.daily_details[2]
    assert d3.precip_mm == 0.0
    assert d3.harvested_liters == 0.0
    assert d3.pluvial_consumed_liters == 100.0
    assert d3.potable_consumed_liters == 300.0
    assert d3.lower_tank_end_liters == 0.0
    assert d3.satisfaction_type == 'PARCIAL'
    assert abs(out.potential_savings_pct - 41.6667) < 0.01
    assert abs(out.avg_pluvial_consumed_l_day - 166.6667) < 0.01
    assert abs(out.pct_days_full_satisfaction - 66.6667) < 0.01
    assert abs(out.pct_days_partial_satisfaction - 33.3333) < 0.01


# ==================================================================================================
# Economia e tarifas: sentido do VPL, regimes de cobrança, preços e investimento
# ==================================================================================================

# ---- origem: tests/invariants/test_economic_properties.py

ECONOMIC_PROPERTIES_BASE = dict(initial_investment=15000.0, annual_water_saved_m3=180.0, water_tariff_per_m3=12.0, sewage_tariff_per_m3=6.0, sewage_mode=1, water_tariff_escalation_rate=0.04, sewage_tariff_escalation_rate=0.04, elec_tariff_escalation_rate=0.04, inflation_rate=0.04, discount_rate=0.08, annual_om_cost_base=150.0, pump_power_kw=0.5, pump_hours_year=200.0, elec_tariff_kwh=0.9, analysis_period_years=20)


def _vpl(**alteracoes):
    return run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, **alteracoes}).vpl


def test_vpl_cresce_com_a_tarifa_de_agua():
    """E1 — Água mais cara torna o aproveitamento mais valioso."""
    valores = [_vpl(water_tariff_per_m3=t) for t in (4.0, 8.0, 12.0, 20.0, 30.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-06, f'VPL caiu com tarifa maior: {valores}'


def test_vpl_decresce_com_o_investimento_inicial():
    """E2 — O mesmo benefício por um custo maior nunca vale mais."""
    valores = [_vpl(initial_investment=i) for i in (5000.0, 15000.0, 30000.0, 60000.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-06, f'VPL subiu com investimento maior: {valores}'


def test_vpl_decresce_com_a_taxa_de_desconto():
    """E3 — Descontar mais o futuro reduz o valor presente de benefícios futuros."""
    valores = [_vpl(discount_rate=d) for d in (0.02, 0.05, 0.08, 0.12, 0.2)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-06, f'VPL subiu com TMA maior: {valores}'


def test_vpl_cresce_com_o_volume_de_agua_economizada():
    """E4 — Economizar mais água nunca reduz o retorno."""
    valores = [_vpl(annual_water_saved_m3=v) for v in (0.0, 60.0, 120.0, 240.0, 480.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-06, f'VPL caiu com mais água economizada: {valores}'


def test_vpl_decresce_com_o_custo_de_operacao():
    """E5 — OPEX maior reduz o retorno."""
    valores = [_vpl(annual_om_cost_base=c) for c in (0.0, 150.0, 500.0, 1500.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-06, f'VPL subiu com OPEX maior: {valores}'


def test_payback_descontado_nunca_precede_o_simples():
    """E6 — Descontar o fluxo só pode atrasar a recuperação do investimento."""
    for tarifa in (8.0, 12.0, 20.0, 35.0):
        resultado = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'water_tariff_per_m3': tarifa})
        if resultado.payback_simple_years is None or resultado.payback_discounted_years is None:
            continue
        assert resultado.payback_discounted_years >= resultado.payback_simple_years - 1e-09, f'payback descontado ({resultado.payback_discounted_years:.4f}) precede o simples ({resultado.payback_simple_years:.4f}) com tarifa {tarifa}'


def test_paybacks_nunca_sao_negativos():
    """E7 — Tempo de retorno é uma duração; não existe retorno antes do desembolso."""
    for investimento in (1000.0, 15000.0, 100000.0):
        resultado = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'initial_investment': investimento})
        for rotulo, valor in (('simples', resultado.payback_simple_years), ('descontado', resultado.payback_discounted_years)):
            if valor is not None:
                assert valor >= 0.0, f'payback {rotulo} negativo: {valor}'


def test_sem_economia_de_agua_o_projeto_nao_se_paga():
    """E8 — Sem benefício não há retorno: o VPL não pode ser positivo."""
    resultado = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'annual_water_saved_m3': 0.0, 'annual_iptu_savings': 0.0})
    assert resultado.vpl <= 0.0, f'VPL positivo ({resultado.vpl:.2f}) sem nenhuma água economizada'


def test_vpl_e_linear_no_escalonamento_do_projeto():
    """E9 — O VPL é linear no fluxo de caixa.

    Dobrar simultaneamente investimento, água economizada e custos operacionais
    equivale a dois projetos idênticos, e deve dobrar o valor presente líquido.
    """
    simples = run_robust_economic_analysis(**ECONOMIC_PROPERTIES_BASE)
    dobrado = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'initial_investment': ECONOMIC_PROPERTIES_BASE['initial_investment'] * 2, 'annual_water_saved_m3': ECONOMIC_PROPERTIES_BASE['annual_water_saved_m3'] * 2, 'annual_om_cost_base': ECONOMIC_PROPERTIES_BASE['annual_om_cost_base'] * 2, 'pump_hours_year': ECONOMIC_PROPERTIES_BASE['pump_hours_year'] * 2})
    assert dobrado.vpl == pytest.approx(simples.vpl * 2, rel=1e-06), f'VPL não escalou linearmente: {simples.vpl:.4f} -> {dobrado.vpl:.4f}'


def test_horizonte_maior_nao_reduz_o_vpl_de_projeto_rentavel():
    """E10 — Se o fluxo anual é positivo, estender o horizonte só acrescenta valor."""
    valores = [run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'water_tariff_per_m3': 25.0, 'analysis_period_years': anos}).vpl for anos in (5, 10, 20, 30)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-06, f'VPL caiu ao estender o horizonte num projeto rentável: {valores}'


def test_tir_e_coerente_com_o_sinal_do_vpl():
    """E11 — TIR e VPL concordam: VPL > 0 à TMA implica TIR acima da TMA."""
    for tarifa in (6.0, 12.0, 25.0, 40.0):
        resultado = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'water_tariff_per_m3': tarifa})
        if resultado.tir_pct is None:
            continue
        tma_pct = ECONOMIC_PROPERTIES_BASE['discount_rate'] * 100.0
        if resultado.vpl > 1.0:
            assert resultado.tir_pct >= tma_pct - 1e-06, f'VPL positivo ({resultado.vpl:.2f}) com TIR ({resultado.tir_pct:.4f}%) abaixo da TMA ({tma_pct:.2f}%), tarifa {tarifa}'


@pytest.mark.parametrize('campo', ['initial_investment', 'annual_water_saved_m3', 'water_tariff_per_m3', 'annual_om_cost_base', 'pump_power_kw'])
def test_entradas_negativas_sao_rejeitadas(campo):
    """E13 — Grandezas físicas e monetárias negativas não são aceitas silenciosamente."""
    with pytest.raises(ValueError):
        run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, campo: -1.0})


def test_horizonte_invalido_e_rejeitado():
    """E14 — O horizonte de análise deve ser um número inteiro positivo de anos."""
    for invalido in (0, -5):
        with pytest.raises(ValueError):
            run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'analysis_period_years': invalido})


def test_indicadores_simples_acompanham_o_investimento():
    """E15 — O payback do cálculo simplificado cresce com o investimento."""
    paybacks = []
    for investimento in (5000.0, 10000.0, 20000.0, 40000.0):
        resultado = calculate_economic_indicators(initial_investment=investimento, annual_water_saved_m3=200.0, water_tariff_per_m3=14.0, analysis_period_years=20, discount_rate=0.08)
        if resultado.payback_simple_years is not None:
            paybacks.append(resultado.payback_simple_years)
    assert len(paybacks) >= 2, 'nenhum payback pôde ser comparado'
    for anterior, seguinte in zip(paybacks, paybacks[1:]):
        assert seguinte >= anterior - 1e-09, f'payback caiu com investimento maior: {paybacks}'


def test_indicadores_simples_e_robusto_concordam_no_sinal_do_vpl():
    """E16 — Os dois caminhos de cálculo econômico não podem discordar sobre viabilidade.

    `calculate_economic_indicators` e `run_robust_economic_analysis` são
    implementações distintas do mesmo fluxo de caixa, com granularidades diferentes.
    Não se exige igualdade numérica — os modelos de OPEX diferem —, mas discordar
    sobre o *sinal* do VPL significaria dizer ao usuário que o mesmo projeto é
    viável ou inviável conforme a tela consultada.
    """
    for tarifa, investimento in ((25.0, 8000.0), (5.0, 60000.0)):
        simples = calculate_economic_indicators(initial_investment=investimento, annual_water_saved_m3=200.0, water_tariff_per_m3=tarifa, annual_om_cost=150.0, discount_rate=0.08, analysis_period_years=20)
        robusto = run_robust_economic_analysis(**{**ECONOMIC_PROPERTIES_BASE, 'initial_investment': investimento, 'annual_water_saved_m3': 200.0, 'water_tariff_per_m3': tarifa, 'sewage_tariff_per_m3': 0.0, 'sewage_mode': 0, 'annual_om_cost_base': 150.0, 'pump_power_kw': 0.0, 'pump_hours_year': 0.0})
        if abs(simples.npv) < 500.0 or abs(robusto.vpl) < 500.0:
            continue
        assert (simples.npv > 0) == (robusto.vpl > 0), f'os dois cálculos discordam sobre a viabilidade com tarifa {tarifa} e investimento {investimento}: simplificado={simples.npv:.2f}, robusto={robusto.vpl:.2f}'


# ---- origem: tests/invariants/test_financial_invariants.py

def test_financial_invariants_zero_investment():
    """Invariante: Se o CAPEX for zero e houver economias, o Payback deve ser no 1º mês e VPL > 0."""
    config = TritonConfig()
    config.cost_lower_tank = 0.0
    config.cost_upper_tank = 0.0
    config.cost_labor = 0.0
    config.cost_piping = 0.0
    config.cost_accessories = 0.0
    config.pump_unit_cost = 0.0
    config.etap_enabled = False
    config.water_tariffs = [(0, 9999, 10.0, 0)]
    config.sewage_rate = 0.0
    sim_res = SingleTankSimulationResult(lower_tank_vol=1000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=500.0, avg_potable_consumed_l_day=500.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=100.0, pct_days_partial_satisfaction=0.0, pct_days_null_satisfaction=0.0)
    econ = run_economic_analysis(config, sim_res)
    assert econ.capex_total == 0.0
    assert econ.payback_months == 1
    assert econ.vpl > 0.0


def test_reference_zero_volume_has_zero_capex_and_zero_opex():
    """Invariante: No cenário de 0 L (sem sistema), CAPEX e OPEX (anual e acumulado) devem ser estritamente R$ 0,00."""
    from triton.core.economic import run_robust_economic_analysis
    res = run_robust_economic_analysis(initial_investment=0.0, annual_water_saved_m3=0.0, water_tariff_per_m3=10.0, sewage_tariff_per_m3=8.0, annual_om_cost_base=120.0, pump_power_kw=0.75, pump_hours_year=150.0, elec_tariff_kwh=1.0, analysis_period_years=20, annual_chlorine_cost=50.0)
    assert res.total_investment == 0.0
    assert res.total_opex_brl == 0.0
    assert res.total_gross_savings_brl == 0.0
    assert res.vpl == 0.0
    assert res.payback_simple_years == 0.0
    assert res.payback_discounted_years == 0.0
    for cf in res.annual_cash_flows:
        assert cf.initial_investment == 0.0
        assert cf.pump_energy_cost_brl == 0.0
        assert cf.om_cost_brl == 0.0
        assert cf.chlorine_cost_brl == 0.0
        assert cf.total_gross_savings_brl == 0.0
        assert cf.net_cash_flow_nominal_brl == 0.0


def test_opex_scales_coherently_with_water_harvested_and_pumping():
    """Invariante: Quanto maior a água captada/bombeada/tratada, maior o OPEX de energia e cloração."""
    from triton.core.economic import run_robust_economic_analysis
    from triton.core.cost_estimates import estimate_annual_chlorination_cost
    _, cl_cost_1 = estimate_annual_chlorination_cost(50.0, 2.0, 25.0)
    res_1 = run_robust_economic_analysis(initial_investment=3000.0, annual_water_saved_m3=50.0, water_tariff_per_m3=8.0, annual_om_cost_base=150.0, pump_power_kw=0.37, pump_hours_year=50.0, elec_tariff_kwh=0.85, analysis_period_years=20, annual_chlorine_cost=cl_cost_1)
    _, cl_cost_2 = estimate_annual_chlorination_cost(200.0, 2.0, 25.0)
    res_2 = run_robust_economic_analysis(initial_investment=8000.0, annual_water_saved_m3=200.0, water_tariff_per_m3=8.0, annual_om_cost_base=150.0, pump_power_kw=0.37, pump_hours_year=200.0, elec_tariff_kwh=0.85, analysis_period_years=20, annual_chlorine_cost=cl_cost_2)
    cf1_yr1 = res_1.annual_cash_flows[1]
    cf2_yr1 = res_2.annual_cash_flows[1]
    opex_yr1_1 = cf1_yr1.pump_energy_cost_brl + cf1_yr1.om_cost_brl + cf1_yr1.chlorine_cost_brl
    opex_yr1_2 = cf2_yr1.pump_energy_cost_brl + cf2_yr1.om_cost_brl + cf2_yr1.chlorine_cost_brl
    assert opex_yr1_2 > opex_yr1_1
    assert res_2.total_opex_brl > res_1.total_opex_brl


# ---- origem: tests/integration/test_financial_robustness.py

def test_robust_irr_matches_known_conventional_cash_flow():
    result = run_robust_economic_analysis(initial_investment=1000.0, annual_water_saved_m3=600.0, water_tariff_per_m3=1.0, annual_om_cost_base=0.0, pump_power_kw=0.0, pump_hours_year=0.0, elec_tariff_kwh=0.0, analysis_period_years=2, discount_rate=0.0, water_tariff_escalation_rate=0.0, sewage_tariff_escalation_rate=0.0, elec_tariff_escalation_rate=0.0, inflation_rate=0.0)
    assert result.tir_pct == pytest.approx(13.066, abs=0.01)


@pytest.mark.parametrize('field,value', [('initial_investment', -1.0), ('annual_water_saved_m3', float('nan')), ('analysis_period_years', 0)])
def test_robust_economic_rejects_invalid_inputs(field, value):
    params = dict(initial_investment=1000.0, annual_water_saved_m3=100.0, water_tariff_per_m3=5.0, analysis_period_years=20)
    params[field] = value
    with pytest.raises(ValueError):
        run_robust_economic_analysis(**params)


def test_invariant_monotonicity_volume_and_tariff():
    """Garante que aumentar o volume economizado ou a tarifa DEVE aumentar ou manter o VPL (ceteris paribus)."""
    base_params = {'initial_investment': 10000.0, 'annual_water_saved_m3': 100.0, 'water_tariff_per_m3': 8.0, 'sewage_tariff_per_m3': 6.4, 'sewage_mode': 1, 'water_tariff_escalation_rate': 0.05, 'sewage_tariff_escalation_rate': 0.05, 'elec_tariff_escalation_rate': 0.05, 'inflation_rate': 0.04, 'discount_rate': 0.08, 'annual_om_cost_base': 150.0, 'analysis_period_years': 20}
    res_base = run_robust_economic_analysis(**base_params)
    params_more_vol = base_params.copy()
    params_more_vol['annual_water_saved_m3'] = 150.0
    res_more_vol = run_robust_economic_analysis(**params_more_vol)
    assert res_more_vol.vpl > res_base.vpl, 'VPL deveria aumentar com maior volume economizado'
    params_higher_tariff = base_params.copy()
    params_higher_tariff['water_tariff_per_m3'] = 12.0
    res_higher_tariff = run_robust_economic_analysis(**params_higher_tariff)
    assert res_higher_tariff.vpl > res_base.vpl, 'VPL deveria aumentar com tarifa de água maior'
    params_higher_capex = base_params.copy()
    params_higher_capex['initial_investment'] = 15000.0
    res_higher_capex = run_robust_economic_analysis(**params_higher_capex)
    assert res_higher_capex.vpl < res_base.vpl, 'VPL deveria diminuir com CAPEX maior'


def test_invariant_cash_flow_equation_balance():
    """Garante que Fluxo Líquido = Receita Bruta - Custos OPEX (em todos os anos)."""
    res = run_robust_economic_analysis(initial_investment=12000.0, annual_water_saved_m3=120.0, water_tariff_per_m3=9.0, sewage_tariff_per_m3=7.2, water_tariff_escalation_rate=0.06, inflation_rate=0.04, discount_rate=0.09, annual_om_cost_base=200.0, analysis_period_years=20)
    for item in res.annual_cash_flows:
        if item.year == 0:
            assert item.net_cash_flow_nominal_brl == -12000.0
        else:
            expected_net = item.total_gross_savings_brl - item.pump_energy_cost_brl - item.om_cost_brl
            assert math.isclose(item.net_cash_flow_nominal_brl, expected_net, abs_tol=0.0001)


# ---- origem: tests/unit/test_regimes_tarifarios.py
# Fora da Edição Brasil o banco vem vazio, e os testes que percorrem os municípios estão em tests/so_da_brl.txt.

CIDADES = load_tariffs_db()['cities']


def conta(faixas, m3: float) -> float:
    """Conta só de água, sem esgoto nem tributos."""
    return calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=1, sewage_rate=0.0)


FRANQUIA = [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]]


DISPON = [[0.0, 0.0, 40.0, -1], [0.0, 999999.0, 5.0, 1]]


PISO = [[0.0, 0.0, 40.0, -3], [0.0, 999999.0, 5.0, 1]]


LIVRE = [[0.0, 999999.0, 5.0, 1]]


def test_franquia_no_minimo_nao_da_economia_abaixo_do_minimo():
    """É o caso que o professor teme, e o mais comum no Brasil.

    Pagam-se R$ 40 que já dão direito a 10 m³. Consumir 3 ou 10 custa o mesmo,
    de modo que economizar dentro da franquia não reduz a conta em nada.
    """
    assert conta(FRANQUIA, 0) == pytest.approx(40.0)
    assert conta(FRANQUIA, 3) == pytest.approx(40.0)
    assert conta(FRANQUIA, 10) == pytest.approx(40.0)
    assert conta(FRANQUIA, 9) - conta(FRANQUIA, 3) == pytest.approx(0.0)
    assert conta(FRANQUIA, 20) - conta(FRANQUIA, 14) == pytest.approx(30.0)


def test_disponibilidade_converte_toda_economia_em_desconto():
    """Instituto distinto do consumo mínimo: a taxa soma POR CIMA do medido."""
    assert conta(DISPON, 0) == pytest.approx(40.0)
    assert conta(DISPON, 3) == pytest.approx(55.0)
    assert conta(DISPON, 9) - conta(DISPON, 3) == pytest.approx(30.0)


def test_a_diferenca_entre_franquia_e_disponibilidade_e_a_economia_do_primeiro_bloco():
    """As duas têm a MESMA forma e diferem só pela tarifa da primeira faixa.

    Um erro de digitação numa casa decimal troca um regime pelo outro em
    silêncio, e a diferença é a economia inteira do primeiro bloco.
    """
    economia_franquia = conta(FRANQUIA, 10) - conta(FRANQUIA, 0)
    economia_dispon = conta(DISPON, 10) - conta(DISPON, 0)
    assert economia_franquia == pytest.approx(0.0)
    assert economia_dispon == pytest.approx(50.0)


def test_piso_de_pagamento_limita_por_baixo_sem_somar_por_cima():
    """Era o regime que faltava ao motor.

    O custo fixo SOMA; o piso LIMITA. Com piso de R$ 40, consumir 8 m³ custa
    R$ 40 e não R$ 80.
    """
    assert conta(PISO, 0) == pytest.approx(40.0)
    assert conta(PISO, 8) == pytest.approx(40.0)
    assert conta(PISO, 10) == pytest.approx(50.0)
    assert conta(PISO, 20) == pytest.approx(100.0)
    assert conta(PISO, 20) < conta(DISPON, 20)


def test_o_piso_zera_a_economia_ate_alcanca_lo():
    assert conta(PISO, 8) - conta(PISO, 4) == pytest.approx(0.0)
    assert conta(PISO, 20) - conta(PISO, 14) == pytest.approx(30.0)


def test_sem_minimo_toda_economia_vira_desconto():
    assert conta(LIVRE, 0) == pytest.approx(0.0)
    assert conta(LIVRE, 9) - conta(LIVRE, 3) == pytest.approx(30.0)


@pytest.mark.parametrize(('faixas', 'esperado'), [(FRANQUIA, FRANQUIA_NO_MINIMO), (DISPON, DISPONIBILIDADE), (PISO, PISO_DE_PAGAMENTO), (LIVRE, SEM_MINIMO), ([[0.0, 6.0, 14.3, -2], [6.0, 999999.0, 3.49, 1]], FRANQUIA_RETROATIVA)])
def test_o_regime_e_lido_da_forma_da_tabela(faixas, esperado):
    assert ler_estrutura(faixas).regime == esperado


def test_a_franquia_lida_e_o_volume_de_tarifa_nula():
    est = ler_estrutura(FRANQUIA)
    assert est.consumo_minimo_m3 == pytest.approx(10.0)
    assert est.custo_fixo_mensal == pytest.approx(40.0)


def test_o_resumo_diz_ao_projetista_o_que_ele_precisa_saber():
    """Não o nome do regime: se economizar reduz a conta, e a partir de quanto."""
    franquia = resumo_do_regime({'faixas': FRANQUIA})
    assert '10 m³' in franquia and 'não cai' in franquia
    assert 'vira desconto' in resumo_do_regime({'faixas': DISPON})
    assert 'piso' in resumo_do_regime({'faixas': PISO}).lower()


def test_a_tabela_truncada_e_erro():
    """Acima do teto a conta não cresce, e o programa não vê economia nenhuma."""
    truncada = [[0.0, 0.0, 30.0, -1], [0.0, 6.0, 0.0, 1]]
    codigos = {a.codigo for a in validar_estrutura({'faixas': truncada})}
    assert 'tabela_truncada' in codigos
    assert conta(truncada, 30) == conta(truncada, 6)


def test_o_minimo_diluido_em_tarifa_e_erro():
    """R$ 52,89 gravado como 5,289 R$/m³ até 10 m³ faz a franquia virar faixa cobrada."""
    diluido = {'tarifa_fixa_mensal': 52.89, 'faixas': [[0.0, 10.0, 5.289, 1], [10.0, 999999.0, 9.8, 1]]}
    codigos = {a.codigo for a in validar_estrutura(diluido)}
    assert 'minimo_diluido_em_tarifa' in codigos


def test_o_minimo_declarado_e_nao_cobrado_e_erro():
    reg = {'tarifa_fixa_mensal': 50.0, 'faixas': [[0.0, 999999.0, 5.0, 1]]}
    codigos = {a.codigo for a in validar_estrutura(reg)}
    assert 'minimo_declarado_e_nao_cobrado' in codigos


def test_a_lacuna_entre_faixas_e_erro():
    reg = {'faixas': [[0.0, 10.0, 3.0, 1], [15.0, 999999.0, 5.0, 1]]}
    assert 'lacuna_entre_faixas' in {a.codigo for a in validar_estrutura(reg)}


def test_a_tarifa_nao_progressiva_e_aviso_e_nao_erro():
    """Existe em tarifa social, então merece conferência e não rejeição."""
    reg = {'faixas': [[0.0, 5.0, 8.0, 1], [5.0, 999999.0, 3.0, 1]]}
    achados = [a for a in validar_estrutura(reg) if a.codigo == 'nao_progressiva']
    assert achados and achados[0].gravidade == 'aviso'


def test_uma_estrutura_correta_nao_gera_erro():
    assert validar_estrutura({'tarifa_fixa_mensal': 40.0, 'faixas': FRANQUIA}) == []


def test_toda_conta_cresce_com_o_consumo():
    """Conta que não cresce é cadastro quebrado, e o efeito é grave.

    Se a conta não sobe com o consumo, economizar água não a reduz, e o
    aproveitamento pluvial aparece sem retorno nenhum por defeito de dado.
    """
    quebrados = []
    for c in CIDADES.values():
        if c.get('estrutura_incompleta'):
            continue
        faixas = c.get('faixas') or []
        if not faixas:
            continue
        anterior = -1.0
        for m3 in (0, 5, 10, 15, 20, 30, 50, 80):
            atual = conta(faixas, m3)
            if atual < anterior - 1e-06:
                quebrados.append(f'{c.get('uf')}/{c.get('municipio')} caiu em {m3} m³')
                break
            anterior = atual
    assert not quebrados, quebrados[:5]


def test_economizar_nunca_aumenta_a_conta():
    """Invariante mais forte: a economia creditada nunca é negativa."""
    negativas = []
    for c in CIDADES.values():
        faixas = c.get('faixas') or []
        if not faixas:
            continue
        for base in (12, 20, 30):
            economia = conta(faixas, base) - conta(faixas, base - 6)
            if economia < -1e-06:
                negativas.append(f'{c.get('uf')}/{c.get('municipio')} em {base} m³: {economia:.2f}')
    assert not negativas, negativas[:5]


def test_o_minimo_usual_brasileiro_e_referencia_e_nao_regra():
    """A conta mínima é o produto da tarifa mínima pelo consumo mínimo.

    O regulamento fala em no mínimo 10 m³ mensais por economia residencial, mas
    a base tem municípios com 6 e com 15: é referência de conferência, não valor
    a impor.
    """
    minimos = {float(c.get('consumo_minimo_faturado_m3', 0.0)) for c in CIDADES.values() if c.get('regime_tarifario') == FRANQUIA_NO_MINIMO}
    assert CONSUMO_MINIMO_USUAL_M3 in minimos
    assert len(minimos) > 1, 'todos os mínimos iguais indicaria valor imposto, não coletado'


# ---- origem: tests/unit/test_tarifa_exponencial.py

TABELA = [(0.0, 0.0, 43.39, -1), (0.0, 1000.0, 9.15, PRECO_BASE_EXPONENCIAL), (0.0, 10.0, 1.0, EXPOENTE_DE_CONSUMO), (10.0, 20.0, 1.05, EXPOENTE_DE_CONSUMO), (20.0, 1000.0, 1.1, EXPOENTE_DE_CONSUMO), (1000.0, 999999.0, 9.15, 1)]


def _agua(m3, tabela=TABELA):
    return calculate_water_bill(m3 * 1000.0, tabela, sewage_mode=1, sewage_rate=0.0)


def test_o_expoente_e_lido_pelo_consumo_do_mes_inteiro():
    assert expoente_do_consumo(TABELA, 0.0) == 1.0
    assert expoente_do_consumo(TABELA, 10.0) == 1.0
    assert expoente_do_consumo(TABELA, 10.5) == 1.05
    assert expoente_do_consumo(TABELA, 25.0) == 1.1
    assert expoente_do_consumo([], 25.0) == 1.0


@pytest.mark.parametrize('consumo, n', [(5.0, 1.0), (15.0, 1.05), (30.0, 1.1)])
def test_a_conta_e_pb_vezes_c_elevado_a_n_mais_o_servico_basico(consumo, n):
    assert _agua(consumo) == pytest.approx(9.15 * consumo ** n + 43.39)


def test_o_expoente_vale_para_o_volume_todo_e_nao_so_para_o_ultimo_m3():
    """Passar de 10 para 11 m³ muda a conta inteira, não só o 11º metro cúbico."""
    salto = _agua(11.0) - _agua(10.0)
    assert salto == pytest.approx(9.15 * 11 ** 1.05 - 9.15 * 10.0)
    assert salto > 9.15 * 1.5


def test_acima_do_teto_o_excedente_e_cobrado_pelo_preco_do_m3():
    no_teto = 9.15 * 1000.0 ** 1.1 + 43.39
    assert _agua(1000.0) == pytest.approx(no_teto)
    assert _agua(1200.0) == pytest.approx(no_teto + 200.0 * 9.15)


def test_o_esgoto_e_percentual_da_agua_inteira():
    total = calculate_water_bill(15000.0, TABELA, sewage_mode=1, sewage_rate=70.0)
    assert total == pytest.approx(_agua(15.0) * 1.7)


def test_a_economia_e_a_diferenca_entre_as_duas_potencias():
    """O m³ poupado vale mais que o preço-base quando n > 1."""
    economia = _agua(30.0) - _agua(20.0)
    assert economia == pytest.approx(9.15 * (30 ** 1.1 - 20 ** 1.05))
    assert economia / 10.0 > 9.15


def test_micromedicao_aplica_a_formula_por_economia():
    """Vinte apartamentos de 15 m³ não são um consumidor de 300 m³."""
    predio = calculate_water_bill(300000.0, TABELA, sewage_mode=1, sewage_rate=0.0, num_units=20)
    assert predio == pytest.approx(20 * _agua(15.0))


def test_a_estrutura_e_lida_e_validada_como_exponencial():
    est = ler_estrutura(TABELA)
    assert est.regime == EXPONENCIAL
    assert est.preco_base == 9.15 and est.teto_exponencial_m3 == 1000.0
    assert [n for *_, n in est.expoentes] == [1.0, 1.05, 1.1]
    assert validar_estrutura({'faixas': TABELA, 'tarifa_fixa_mensal': 43.39}) == []
    assert diagnosticar(TABELA).responde_ao_consumo
    assert 'PB × Cⁿ' in resumo_do_regime({'faixas': TABELA})


@pytest.mark.parametrize('defeito, codigo', [([f for f in TABELA if f[3] != EXPOENTE_DE_CONSUMO], 'sem_tabela_exponencial'), ([f for f in TABELA if f[:2] != (10.0, 20.0)], 'lacuna_na_tabela_exponencial'), ([f if f[:2] != (20.0, 1000.0) else (20.0, 500.0, 1.1, 3) for f in TABELA], 'tabela_exponencial_truncada'), ([f if f[:2] != (20.0, 1000.0) else (20.0, 1000.0, 3.0, 3) for f in TABELA], 'expoente_implausivel')])
def test_a_validacao_aponta_a_tabela_exponencial_defeituosa(defeito, codigo):
    achados = {a.codigo: a.gravidade for a in validar_estrutura({'faixas': defeito})}
    assert achados.get(codigo) == 'erro'


@pytest.mark.parametrize('consumo, n', [(10, 1.0), (20, 1.0), (21, 1.01), (28, 1.08), (29, 1.08), (30, 1.09), (35, 1.09), (40, 1.1), (100, 1.11), (150, 1.13), (200, 1.1287), (1500, 1.11), (10000, 1.0858)])
def test_cada_consumo_le_o_expoente_da_sua_linha(consumo, n):
    """A linha «31» vale de 31 a 35 m³: o consumo 35 ainda usa o expoente de 31."""
    assert expoente_do_consumo(get_city_data('RS', 'Alegrete')['faixas'], consumo) == n


@pytest.mark.parametrize('uf, cidade, esgoto', [('RS', 'Alegrete', 6.4), ('RS', 'Erechim', 4.86), ('RS', 'Santa Cruz do Sul', 5.53), ('RS', 'Canoas', 6.07)])
def test_o_esgoto_e_cobrado_por_m3_consumido(uf, cidade, esgoto):
    """Sem serviço básico e sem expoente: 70% do PB, truncado no centavo."""
    from triton.core.tariffs_database import esgoto_do_municipio
    from triton.core.tariffs_structure import ESGOTO_POR_M3
    dados = get_city_data(uf, cidade)
    assert esgoto_do_municipio(dados) == (ESGOTO_POR_M3, esgoto)
    faixas = [tuple(f) for f in dados['faixas']]
    agua = calculate_water_bill(25000.0, faixas, sewage_mode=1, sewage_rate=0.0)
    total = calculate_water_bill(25000.0, faixas, sewage_mode=ESGOTO_POR_M3, sewage_rate=esgoto)
    assert total - agua == pytest.approx(25 * esgoto)


def test_categoria_sem_tabela_da_corsan_nao_e_derivada_da_residencial():
    """A comercial da CORSAN tem preço-base e tabela de expoentes próprios: não se deriva."""
    assert get_city_tariffs_by_category('RS', 'Alegrete', 'residencial')
    if 'comercial' not in (get_city_data('RS', 'Alegrete').get('categorias') or {}):
        assert get_city_tariffs_by_category('RS', 'Alegrete', 'comercial') is None


def test_parcela_exponencial_sem_preco_base_e_zero():
    assert parcela_exponencial([(0.0, 999999.0, 5.0, 1)], 10.0) == 0.0
    assert parcela_exponencial(TABELA, 0.0) == 0.0


def test_entre_dois_inteiros_a_conta_e_a_reta_que_os_une():
    """O hidrômetro fatura m³ inteiros; o consumo médio fracionário fica entre as duas contas.

    Antes, 20,01 m³ já levava n = 1,01 ao volume todo, e a tarifa evitada de 1 m³ oscilava
    com a casa decimal do consumo médio (R$ 25,42 a 30 m³, R$ 13,55 a 30,5 m³, em Alegrete).
    """
    assert _agua(10.5) == pytest.approx((_agua(10.0) + _agua(11.0)) / 2)
    assert _agua(10.01) == pytest.approx(_agua(10.0) + 0.01 * (_agua(11.0) - _agua(10.0)))
    alegrete = [tuple(f) for f in get_city_tariffs_by_category('RS', 'Alegrete', 'residencial')['faixas']]
    conta = lambda m3: calculate_water_bill(m3 * 1000.0, alegrete, sewage_mode=1, sewage_rate=0.0)
    evitada = [conta(d) - conta(d - 1.0) for d in (29.5, 30.0, 30.5, 31.0)]
    assert evitada[1] > evitada[0] > evitada[3] and evitada[1] > evitada[2] > evitada[3]


# ---- origem: tests/unit/test_vigencia_tarifaria.py

@pytest.mark.parametrize('texto,esperado', [('01/12/2024', '2024-12-01'), ('12/2025', '2025-12-01'), ('Vigente desde fevereiro de 2026', '2026-02-01'), ('2025', '2025-07-01'), ('', None), ('Regulação Oficial', None)])
def test_le_a_vigencia_do_catalogo(texto, esperado):
    d = data_da_vigencia(texto)
    assert (d.isoformat() if d else None) == esperado


def _cfg(vig, base, intervalo=12, w=5.0, s=4.0):
    return SimpleNamespace(tariff_vigencia=vig, data_base_estudo=base, tariff_escalation=intervalo, water_tariff_escalation=w, sewage_tariff_escalation=s)


def test_conta_os_reajustes_completos_entre_as_datas():
    c = _cfg('01/12/2024', '05/10/2026')
    assert meses_desde_a_vigencia(c) == 22
    assert reajustes_desde_a_vigencia(c) == 1
    assert fatores_desde_a_vigencia(c) == pytest.approx((1.05, 1.04))
    c = _cfg('01/12/2024', '01/12/2026')
    assert reajustes_desde_a_vigencia(c) == 2


@pytest.mark.parametrize('vig,base', [('', '05/10/2026'), ('01/12/2024', ''), ('01/12/2026', '05/10/2026')])
def test_sem_as_duas_datas_ou_vigencia_futura_nada_muda(vig, base):
    assert fatores_desde_a_vigencia(_cfg(vig, base)) == (1.0, 1.0)


def _vigencia_tarifaria_config(vig='', base=''):
    cfg = TritonConfig()
    cfg.water_tariffs = [(0.0, 10.0, 5.0, 1), (10.0, 999999.0, 10.0, 1)]
    cfg.sewage_mode, cfg.sewage_rate = (1, 80.0)
    cfg.tariff_escalation = 12
    cfg.water_tariff_escalation = 5.0
    cfg.sewage_tariff_escalation = 5.0
    cfg.tariff_vigencia, cfg.data_base_estudo = (vig, base)
    cfg.analysis_period_years = 5
    return cfg


def _vigencia_tarifaria_sim():
    return SingleTankSimulationResult(lower_tank_vol=2000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=300.0, avg_potable_consumed_l_day=300.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=50.0, pct_days_partial_satisfaction=0.0, pct_days_null_satisfaction=50.0)


def test_conta_mensal_aplica_o_reajuste_passado_e_os_aniversarios_da_vigencia():
    sem = run_economic_analysis(_vigencia_tarifaria_config(), _vigencia_tarifaria_sim()).monthly_cash_flows
    com = run_economic_analysis(_vigencia_tarifaria_config('01/12/2024', '05/10/2026'), _vigencia_tarifaria_sim()).monthly_cash_flows
    assert com[0].water_savings == pytest.approx(sem[0].water_savings * 1.05, rel=1e-09)
    assert com[1].water_savings == pytest.approx(com[0].water_savings, rel=1e-09)
    assert com[2].water_savings == pytest.approx(com[0].water_savings * 1.05, rel=1e-09)
    assert sem[12].water_savings == pytest.approx(sem[0].water_savings * 1.05, rel=1e-09)


def test_conta_anual_usa_a_tarifa_atualizada():
    sem = calculate_effective_tariff(_vigencia_tarifaria_config(), 50.0, annual_total_demand_m3=200.0)
    com = calculate_effective_tariff(_vigencia_tarifaria_config('01/12/2024', '05/10/2026'), 50.0, annual_total_demand_m3=200.0)
    assert com[0] == pytest.approx(sem[0] * 1.05)
    assert com[1] == pytest.approx(sem[1] * 1.05)


def test_o_projeto_guarda_as_datas_e_o_antigo_fica_como_era(tmp_path):
    cfg = _vigencia_tarifaria_config('01/12/2024', '05/10/2026')
    arq = tmp_path / 'p.triton'
    export_triton_json(cfg, str(arq))
    lido = load_triton_project(str(arq))['config']
    assert (lido.tariff_vigencia, lido.data_base_estudo) == ('01/12/2024', '05/10/2026')
    dados = json.loads(arq.read_text(encoding='utf-8'))
    fe = dados['inputs']['financial_and_economic']
    del fe['tariff_vigencia'], fe['data_base_estudo']
    arq.write_text(json.dumps(dados), encoding='utf-8')
    antigo = load_triton_project(str(arq))['config']
    assert fatores_desde_a_vigencia(antigo) == (1.0, 1.0)


# ---- origem: tests/unit/test_precos_de_reservatorio.py

def test_o_preco_nunca_cai_quando_o_volume_sobe():
    """Era o defeito: 1.750 L custava R$ 1.399 e 2.000 L custava R$ 1.299."""
    for tabela, nome in ((LOWER_TANK_PRICE_TABLE, 'inferior'), (UPPER_TANK_PRICE_TABLE, 'superior')):
        pares = sorted(((float(v), float(p)) for v, p in tabela))
        precos = [p for _, p in pares]
        assert precos == sorted(precos), f'tabela {nome} não é monotônica: {pares}'


def test_a_curva_interpolada_e_monotonica_em_toda_a_faixa_de_uso():
    """A monotonicidade da tabela não basta: a curva entre os pontos também precisa dela."""
    anterior = -1.0
    for litros in range(100, 60001, 100):
        preco = interpolate_price(LOWER_TANK_PRICE_TABLE, litros)
        assert preco >= anterior, f'preço caiu em {litros} L'
        anterior = preco


def test_volume_nulo_nao_custa_nada():
    assert interpolate_price(LOWER_TANK_PRICE_TABLE, 0.0) == 0.0
    assert estimate_tank_price(0.0, 'PEAD') == 0.0


def test_nos_pontos_tabelados_a_estimativa_devolve_o_preco_tabelado():
    """É o vínculo com o banco: se a interpolação se soltar dele, este teste cai."""
    for volume, preco in LOWER_TANK_PRICE_TABLE:
        assert estimate_tank_price(volume, 'PEAD') == pytest.approx(preco), volume


def test_entre_dois_pontos_a_estimativa_fica_entre_os_dois_precos():
    pares = sorted(((float(v), float(p)) for v, p in LOWER_TANK_PRICE_TABLE))
    for (v1, p1), (v2, p2) in zip(pares, pares[1:]):
        meio = (v1 + v2) / 2.0
        assert p1 <= interpolate_price(LOWER_TANK_PRICE_TABLE, meio) <= p2, (v1, v2)


def test_o_material_multiplica_o_preco_de_referencia():
    pead = estimate_tank_price(5000.0, 'PEAD')
    for material in ('CONCRETO', 'PRFV', 'ACO_INOX'):
        assert estimate_tank_price(5000.0, material) > pead, material


def test_a_regressao_descreve_bem_a_tabela():
    """Se o R² não for alto, a reta não serve para extrapolar, e o código sabe disso."""
    reg = get_tank_linear_regression('PEAD')
    assert reg['r_squared'] >= R2_MINIMO_PARA_EXTRAPOLAR
    assert reg['slope_r_per_l'] > 0.0
    assert reg['n_pontos'] == len(LOWER_TANK_PRICE_TABLE)
    assert reg['volume_maximo_tabelado_l'] == max((float(v) for v, _ in LOWER_TANK_PRICE_TABLE))


def test_a_extrapolacao_segue_a_regressao_e_nao_os_dois_ultimos_pontos():
    """É a ligação pedida: a referência é o banco inteiro, não o par final.

    Uma promoção no maior volume tabelado girava a reta inteira quando só os dois
    últimos pontos a definiam.
    """
    reg = get_tank_linear_regression('PEAD')
    maximo = reg['volume_maximo_tabelado_l']
    for volume in (maximo * 1.5, maximo * 2.0, maximo * 3.0):
        esperado = reg['slope_r_per_l'] * volume + reg['intercept_r']
        assert interpolate_price(LOWER_TANK_PRICE_TABLE, volume) == pytest.approx(esperado, rel=1e-09)


def test_a_extrapolacao_nunca_fica_abaixo_do_ultimo_preco_tabelado():
    """Reservatório maior não custa menos, mesmo que a reta ajustada diga que sim."""
    tabela_ruim = [(1000.0, 500.0), (2000.0, 900.0), (3000.0, 905.0)]
    ultimo = 905.0
    for volume in (3100.0, 5000.0, 20000.0):
        assert interpolate_price(tabela_ruim, volume) >= ultimo


def test_ajuste_ruim_cai_no_metodo_local():
    """Uma reta que não descreve a tabela é pior que a inclinação local.

    O degrau abaixo derruba o R², e nesse caso a extrapolação volta a usar os
    dois últimos pontos, que ao menos descrevem o trecho final.
    """
    degrau = [(100.0, 100.0), (200.0, 105.0), (300.0, 110.0), (400.0, 9000.0)]
    assert regressao_linear_da_tabela(degrau)['r_squared'] < R2_MINIMO_PARA_EXTRAPOLAR
    inclinacao_local = (9000.0 - 110.0) / 100.0
    assert interpolate_price(degrau, 500.0) == pytest.approx(9000.0 + inclinacao_local * 100.0)


def test_a_regressao_de_tabela_curta_nao_estoura():
    assert regressao_linear_da_tabela([])['r_squared'] == 0.0
    assert regressao_linear_da_tabela([(1000.0, 500.0)])['slope_r_per_l'] == 0.0


def test_a_regressao_acompanha_o_material():
    pead = get_tank_linear_regression('PEAD')['slope_r_per_l']
    inox = get_tank_linear_regression('ACO_INOX')['slope_r_per_l']
    assert inox > pead


def test_a_regressao_da_caixa_superior_usa_a_tabela_da_caixa_superior():
    sup = get_tank_linear_regression('PEAD', is_upper=True)
    assert sup['is_upper'] is True
    assert sup['n_pontos'] == len(UPPER_TANK_PRICE_TABLE)
    assert sup['volume_maximo_tabelado_l'] <= get_tank_linear_regression('PEAD')['volume_maximo_tabelado_l']


def test_a_tabela_de_recurso_espelha_o_banco():
    """Corrigir o JSON não bastava.

    `load_costs_database` cai numa tabela embutida quando o arquivo não está
    legível, e essa tabela guardava a versão antiga, com 1.750 L a R$ 1.399 e
    2.000 L a R$ 1.299. Bastava o arquivo faltar — instalação nova, permissão
    negada, JSON corrompido — para o programa voltar a cobrar menos por um
    reservatório maior, sem aviso nenhum.
    """
    from triton.core.cost_estimates import _DEFAULT_LOWER_TANK_PRICES, _DEFAULT_UPPER_TANK_PRICES
    db = load_costs_database()
    for recurso, chave in ((_DEFAULT_LOWER_TANK_PRICES, 'lower_tank_pead_prices'), (_DEFAULT_UPPER_TANK_PRICES, 'upper_tank_pead_prices')):
        do_banco = [(float(v), float(p)) for v, p in db[chave]]
        do_recurso = [(float(v), float(p)) for v, p in recurso]
        assert do_recurso == do_banco, chave


def test_a_tabela_de_recurso_tambem_e_monotonica():
    """A verificação da monotonicidade tem de alcançar o caminho de recurso."""
    from triton.core.cost_estimates import _DEFAULT_LOWER_TANK_PRICES, _DEFAULT_UPPER_TANK_PRICES
    for tabela in (_DEFAULT_LOWER_TANK_PRICES, _DEFAULT_UPPER_TANK_PRICES):
        precos = [float(p) for _, p in sorted(tabela)]
        assert precos == sorted(precos), tabela


# ---- origem: tests/unit/test_capex_calibrado.py

TIPOLOGIAS = ('UTI', 'UTG', 'MSG', 'MFH', 'MFL')


def _orcar(tipologia: str='UTI', volume_l: float=5000.0, uf: str='SP'):
    return estimate_calibrated_capex_opex(typology=tipologia, volume_l=volume_l, uf=uf)


def test_o_orcamento_traz_todas_as_parcelas_declaradas():
    """Um total sem as parcelas não é auditável: não dá para conferir de onde veio."""
    r = _orcar()
    for campo in ('c_inf', 'c_sup', 'c_pump', 'c_pipes', 'c_panel', 'c_sensors', 'c_treatment', 'c_air_gap', 'labor_cost', 'capex_base_brl', 'capex_total_brl', 'f_regional', 'opex_fixed_annual_brl', 'opex_variable_per_m3_brl'):
        assert campo in r, campo
        assert isinstance(r[campo], (int, float)), campo


def test_as_parcelas_somam_o_capex_base():
    """Se as partes não somam o todo, alguma entrou ou saiu sem aparecer."""
    r = _orcar()
    partes = r['c_inf'] + r['c_sup'] + r['c_pump'] + r['c_pipes'] + r['c_accessories_total'] + r['labor_cost']
    assert partes == pytest.approx(r['capex_base_brl'], rel=1e-06)


def test_os_acessorios_somam_os_quatro_subsistemas():
    r = _orcar()
    assert r['c_accessories_total'] == pytest.approx(r['c_panel'] + r['c_sensors'] + r['c_treatment'] + r['c_air_gap'])


def test_o_fator_regional_multiplica_a_base():
    for uf in ('SP', 'RR', 'RS', 'AM'):
        r = _orcar(uf=uf)
        assert r['capex_total_brl'] == pytest.approx(r['capex_base_brl'] * r['f_regional'])


def test_o_capex_cresce_com_o_porte_da_tipologia():
    """Da casa térrea ao bloco multifamiliar não há inversão.

    O bloco tem prumadas duplas, bomba principal e reserva, painel elétrico e
    shafts: custa mais, e o modelo tem de refletir isso monotonicamente.
    """
    valores = [_orcar(t)['capex_total_brl'] for t in TIPOLOGIAS]
    assert valores == sorted(valores), dict(zip(TIPOLOGIAS, valores))
    assert valores[-1] > 3 * valores[0]


def test_o_opex_fixo_cresce_com_o_porte():
    valores = [_orcar(t)['opex_fixed_annual_brl'] for t in TIPOLOGIAS]
    assert valores == sorted(valores)
    assert all((v > 0 for v in valores))


def test_toda_tipologia_do_banco_e_orcavel():
    """Acrescentar tipologia ao banco e esquecer o modelo derruba este teste."""
    for chave in TYPOLOGY_COST_CONFIGS:
        r = _orcar(chave)
        assert r['capex_total_brl'] > 0, chave
        assert r['typology_name'], chave


def test_o_capex_cresce_com_o_volume():
    valores = [_orcar('MFL', volume_l=v)['capex_total_brl'] for v in (1000, 5000, 20000)]
    assert valores == sorted(valores)


def test_os_fatores_regionais_cobrem_as_27_unidades_da_federacao():
    assert len(REGIONAL_FACTORS_BY_UF) >= 27
    for uf, fator in REGIONAL_FACTORS_BY_UF.items():
        assert 0.7 <= float(fator) <= 1.6, (uf, fator)


def test_roraima_custa_mais_que_sao_paulo():
    """É o sentido do fator regional: logística encarece o Norte."""
    assert _orcar('MFL', 20000, 'RR')['capex_total_brl'] > _orcar('MFL', 20000, 'SP')['capex_total_brl']


def test_uf_desconhecida_cai_no_fator_neutro():
    assert _orcar(uf='XX')['f_regional'] == pytest.approx(1.0)


def test_a_api_legada_continua_respondendo():
    """Projetos e chamadas antigas usam a assinatura posicional."""
    legado = estimate_preliminary_capex(5000, 500, True, 0.37, 1)
    assert legado['total'] > 0
    for campo in ('lower', 'upper', 'pump', 'piping', 'accessories', 'labor'):
        assert campo in legado, campo


def test_a_api_legada_aceita_tipologia_e_uf():
    barato = estimate_preliminary_capex(5000, 500, True, typology='UTI', uf='SP')
    caro = estimate_preliminary_capex(5000, 500, True, typology='MFL', uf='RJ')
    assert caro['total'] > barato['total']


def test_volume_nulo_nao_produz_capex_negativo():
    r = _orcar(volume_l=0.0)
    assert r['capex_total_brl'] >= 0.0


# ---- origem: tests/unit/test_capex_por_volume_na_cli.py
_ARQUIVO_CAPEX_POR_VOLUME_NA_CLI = str(_TESTES / 'unit/test_capex_por_volume_na_cli.py')

CAPEX_POR_VOLUME_NA_CLI_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_CAPEX_POR_VOLUME_NA_CLI))))


_c_sw = os.path.join(CAPEX_POR_VOLUME_NA_CLI_RAIZ, 'manual', 'casos', '04_tutorial_sweep.triton')
_c_va = os.path.join(CAPEX_POR_VOLUME_NA_CLI_RAIZ, 'manual', 'casos', '04_tutorial_varredura.triton')
_c_an = os.path.join(CAPEX_POR_VOLUME_NA_CLI_RAIZ, 'manual', 'casos', '02_tutorial_varredura.triton')
CAPEX_POR_VOLUME_NA_CLI_CASO = _c_sw if os.path.exists(_c_sw) else (_c_va if os.path.exists(_c_va) else _c_an)


def load_project_file(caminho):
    bundle = _load_bundle(caminho)
    return (bundle['config'], _get_precipitation(bundle))


@pytest.fixture(scope='module')
def relatorio():
    cfg, precip = load_project_file(CAPEX_POR_VOLUME_NA_CLI_CASO)
    # Estes testes verificam o catálogo de preços do motor (cisterna por volume). Fora da
    # Brasil o projeto lido sem o campo nasce com o catálogo desligado (premissa de
    # neutralidade, edition.configuracao_da_edicao); aqui ele é ligado de propósito.
    cfg.precos_de_catalogo = True
    return (run_analysis(cfg, precip, 'economic'), cfg)


def test_o_preco_da_cisterna_e_o_mesmo_da_interface(relatorio):
    _, cfg = relatorio
    for volume in (1000.0, 4000.0, 12000.0):
        interface = estimate_preliminary_capex(volume, cfg.upper_tank_vol, bool(cfg.upper_tank_used), cfg.pump_power_kw, cfg.pump_count, lower_material=cfg.lower_tank_material, upper_material=cfg.upper_tank_material)['lower']
        assert _preco_da_cisterna(cfg, volume) == pytest.approx(interface)


def test_o_capex_cresce_com_o_volume_na_varredura(relatorio):
    rel, _ = relatorio
    linhas = [l for l in rel['economic']['alternatives'] if l['lower_tank_volume_l'] > 0]
    capex = [l['capex_brl'] for l in sorted(linhas, key=lambda l: l['lower_tank_volume_l'])]
    assert all((b > a for a, b in zip(capex, capex[1:]))), capex


def test_o_vpl_tem_maximo_interior(relatorio):
    rel, _ = relatorio
    linhas = sorted((l for l in rel['economic']['alternatives'] if l['lower_tank_volume_l'] > 0), key=lambda l: l['lower_tank_volume_l'])
    vpl = [l['npv_brl'] for l in linhas]
    melhor = vpl.index(max(vpl))
    assert 0 < melhor < len(vpl) - 1, 'o VPL máximo caiu na borda da varredura'
    assert vpl[-1] < max(vpl)


def test_volume_unico_mantem_o_preco_declarado():
    cfg, precip = load_project_file(CAPEX_POR_VOLUME_NA_CLI_CASO)
    rel = run_analysis(cfg, precip, 'economic', volume=4000.0)
    declarado = cfg.cost_lower_tank
    assert rel['economic']['alternatives'][0]['capex_brl'] >= declarado


# ---- origem: tests/unit/test_etap_integration.py

VOLUME_M3 = 120.0


#: Fatores da rede e da água potável dados de propósito: fora da Edição Brasil o padrão do motor é zero (o usuário informa os dele).
FATOR_DA_REDE_DE_TESTE = 0.085
FATOR_DA_AGUA_DE_TESTE = 0.35


def _config_ambiental(**kwargs) -> EnvironmentalConfig:
    base = dict(annual_water_saved_m3=VOLUME_M3, grid_co2_factor_kg_kwh=FATOR_DA_REDE_DE_TESTE, potable_water_co2_kg_m3=FATOR_DA_AGUA_DE_TESTE)
    base.update(kwargs)
    return EnvironmentalConfig(**base)


def _acv(metodo: str='cloro', **kwargs):
    return calculate_lca(5000.0, VOLUME_M3, _config_ambiental(water_quality_disinfection=metodo, **kwargs))


def test_o_volume_pluvial_vem_da_simulacao_e_nao_de_um_valor_fixo():
    """A aba pedia `annual_pluvial_consumed_m3` à configuração, e o campo não existe.

    É propriedade do RESULTADO da simulação, não de `TritonConfig`. O `getattr`
    devolvia sempre o valor de recurso, e a ETAP era dimensionada para 120 m³/ano
    qualquer que fosse o projeto.
    """
    assert not hasattr(TritonConfig(), 'annual_pluvial_consumed_m3')
    sim = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=1000.0, avg_potable_consumed_l_day=500.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    assert sim.annual_pluvial_consumed_m3 == pytest.approx(365.25)
    assert volume_pluvial_anual_m3(TritonConfig(), sim) == pytest.approx(365.25)


def test_sem_simulacao_o_volume_cai_no_valor_de_recurso():
    assert volume_pluvial_anual_m3(TritonConfig(), None) == VOLUME_PLUVIAL_DE_RECURSO_M3


def test_a_etap_acompanha_o_volume_do_projeto():
    """Dobrar o consumo dobra o consumo de hipoclorito, não o investimento."""
    pequeno = dimensionar_etap_do_projeto(TritonConfig(), annual_pluvial_m3=100.0)
    grande = dimensionar_etap_do_projeto(TritonConfig(), annual_pluvial_m3=200.0)
    assert grande.custo_anual_do_cloro == pytest.approx(2 * pequeno.custo_anual_do_cloro)
    assert grande.capex == pytest.approx(pequeno.capex)


def test_escolher_ultravioleta_muda_a_emissao_da_acv():
    """Era a desconexão principal: a escolha ficava guardada e era ignorada."""
    cloro = _acv('cloro')
    uv = _acv('uv')
    ozonio = _acv('ozonio')
    assert uv.annual_treatment_co2_kg > 10 * cloro.annual_treatment_co2_kg
    assert ozonio.annual_treatment_co2_kg > uv.annual_treatment_co2_kg
    assert uv.net_annual_avoided_co2_kg < cloro.net_annual_avoided_co2_kg
    assert ozonio.environmental_payback_years > cloro.environmental_payback_years


def test_o_polimento_tambem_chega_a_acv():
    sem = _acv('cloro', water_quality_polishing=False)
    com = _acv('cloro', water_quality_polishing=True)
    assert com.annual_treatment_co2_kg > sem.annual_treatment_co2_kg


def test_o_cloro_e_contado_uma_vez_na_acv():
    """Somar o total da ETAP ao termo de cloração contaria o hipoclorito duas vezes.

    Com apenas cloração, a ETAP e o termo antigo têm de coincidir: é essa
    identidade que prova que houve substituição, e não soma.
    """
    cfg = _config_ambiental(water_quality_disinfection='cloro')
    cloracao = Cloracao(dose_mg_por_litro=cfg.chlorine_dose_mg_l, pureza=cfg.chlorine_product_purity, fator_kg_co2e_por_kg_produto=cfg.chlorine_co2_kg_per_kg)
    esperado = cloracao.co2e_anual_kg(VOLUME_M3)
    obtido = calculate_lca(5000.0, VOLUME_M3, cfg).annual_treatment_co2_kg
    assert obtido == pytest.approx(esperado, rel=1e-09)


def test_a_parcela_extra_isola_o_que_nao_e_cloro():
    assert _acv('cloro').etap_extra_co2_kg_yr == pytest.approx(0.0)
    uv = _acv('uv')
    assert uv.etap_extra_co2_kg_yr == pytest.approx(uv.annual_treatment_co2_kg - _acv('cloro').annual_treatment_co2_kg, rel=1e-09)


def test_desligar_a_etap_devolve_o_resultado_anterior():
    """Estudos já rodados usaram só a cloração, e têm de continuar reproduzíveis."""
    antigo = calculate_lca(5000.0, VOLUME_M3, _config_ambiental(etap_enabled=False, water_quality_disinfection='uv'))
    assert antigo.etap_extra_co2_kg_yr == pytest.approx(0.0)
    assert antigo.annual_treatment_co2_kg == pytest.approx(_acv('cloro').annual_treatment_co2_kg)


def test_o_campo_legado_de_intensidade_continua_mandando():
    """Projetos antigos informavam kg CO2e/m³ diretamente; trocar por baixo mudaria resultados publicados."""
    cfg = _config_ambiental(chemical_treatment_co2_m3=0.5, water_quality_disinfection='ozonio')
    r = calculate_lca(5000.0, VOLUME_M3, cfg)
    assert r.annual_treatment_co2_kg == pytest.approx(0.5 * VOLUME_M3)


def test_o_inventario_nomeia_os_estagios_de_desinfeccao():
    uv = _acv('uv')
    item = next((i for i in uv.inventory_items if 'Tratamento' in i.category))
    assert 'ultravioleta' in item.source_reference.lower()
    assert any(('ultravioleta' in e.lower() for e in uv.etap_disinfection_stages))


def _etap_integration_sim() -> SingleTankSimulationResult:
    return SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)


def _econ(metodo: str='cloro', **kwargs):
    cfg = TritonConfig()
    cfg.water_quality_disinfection = metodo
    for k, v in kwargs.items():
        setattr(cfg, k, v)
    return run_economic_analysis(cfg, _etap_integration_sim())


def test_a_etap_entra_no_investimento():
    econ = _econ('cloro')
    assert econ.etap_capex_brl > 0.0
    assert econ.etap_disinfection_method == 'cloro'


def test_escolher_ultravioleta_encarece_o_investimento_e_o_custeio():
    cloro, uv = (_econ('cloro'), _econ('uv'))
    assert uv.etap_capex_brl > cloro.etap_capex_brl
    assert uv.capex_total > cloro.capex_total
    assert uv.annual_etap_opex_brl > cloro.annual_etap_opex_brl
    assert uv.vpl < cloro.vpl


def test_o_cloro_e_pago_uma_vez_no_economico():
    """Só a cloração: a parcela extra da ETAP tem de ser nula.

    O custeio do hipoclorito já vinha da linha de cloração. Somar o custeio
    total da ETAP o cobraria duas vezes.
    """
    econ = _econ('cloro')
    assert econ.annual_etap_opex_brl == pytest.approx(0.0)
    assert econ.annual_chlorine_cost_brl > 0.0


def test_o_capex_da_etap_desloca_a_verba_generica_de_acessorios():
    """«Acessórios» já embute uma verba de filtração e tratamento.

    Somar o CAPEX inteiro da ETAP sobre ela contaria o filtro duas vezes.
    """
    verba = verba_generica_de_tratamento_brl('UTI')
    assert verba > 0.0
    sem_acessorios = _econ('cloro', cost_accessories=0.0)
    com_acessorios = _econ('cloro', cost_accessories=800.0)
    assert com_acessorios.etap_capex_brl == pytest.approx(sem_acessorios.etap_capex_brl - verba)


def test_desligar_a_etap_zera_as_duas_parcelas_no_economico():
    econ = _econ('uv', etap_enabled=False)
    assert econ.etap_capex_brl == 0.0
    assert econ.annual_etap_opex_brl == 0.0


def test_a_dose_e_a_pureza_do_projeto_chegam_ao_dimensionamento():
    """A ETAP assumia a pureza padrão mesmo com outra configurada.

    A mesma cloração aparecia com massa e custo diferentes em duas telas.
    """
    cfg = TritonConfig()
    cfg.chlorine_product_purity = 0.65
    padrao = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    cfg.chlorine_product_purity = 0.325
    diluida = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    assert diluida.resultado.annual_chlorine_kg == pytest.approx(2 * padrao.resultado.annual_chlorine_kg, rel=1e-09)


def test_o_preco_do_cloro_e_o_mesmo_nos_dois_modulos():
    """Estavam em R$ 38,00/kg na aba de qualidade e R$ 25,00/kg no econômico."""
    cfg = TritonConfig()
    etap = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    esperado = etap.resultado.annual_chlorine_kg * cfg.chlorine_cost_per_kg
    assert etap.resultado.annual_chlorine_cost_brl == pytest.approx(esperado, rel=1e-09)


def test_a_dose_relatada_vale_para_qualquer_metodo():
    """Valia zero quando o método não era «cloro», embora a cloração seja sempre aplicada."""
    for metodo in ('cloro', 'uv', 'ozonio'):
        cfg = TritonConfig()
        cfg.water_quality_disinfection = metodo
        etap = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
        assert etap.resultado.chlorine_dose_mg_l > 0.0, metodo
        assert etap.resultado.annual_chlorine_kg > 0.0, metodo


def test_descarte_primeiras_aguas_soma_no_capex_da_etap_e_economico():
    cfg = TritonConfig()
    cfg.discard = 2.0
    cfg.area = 100.0
    cfg.first_flush_system_enabled = False
    etap_sem = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    cfg.first_flush_system_enabled = True
    etap_com = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    assert etap_com.first_flush_volume_l == 200.0
    assert etap_com.first_flush_capex > 0.0
    assert etap_com.capex == pytest.approx(etap_sem.capex + etap_com.first_flush_capex)


def test_descarte_primeiras_aguas_soma_no_inventario_da_acv():
    cfg_env_sem = EnvironmentalConfig(annual_water_saved_m3=VOLUME_M3, discard=2.0, roof_area_m2=100.0, first_flush_system_enabled=False)
    lca_sem = calculate_lca(5000.0, VOLUME_M3, cfg_env_sem)
    cfg_env_com = EnvironmentalConfig(annual_water_saved_m3=VOLUME_M3, discard=2.0, roof_area_m2=100.0, first_flush_system_enabled=True)
    lca_com = calculate_lca(5000.0, VOLUME_M3, cfg_env_com)
    assert lca_com.total_embodied_co2_kg > lca_sem.total_embodied_co2_kg
    categorias = [item.category for item in lca_com.inventory_items]
    assert any(('Descarte' in cat for cat in categorias))


# ---- origem: tests/unit/test_filtro_de_polimento.py

CLASSES_QUE_RECOMENDAM = tuple((c for c, v in WATER_QUALITY_CLASSES.items() if v.exige_filtracao_fina))


def test_a_classe_padrao_nem_sequer_recomenda_polimento():
    """A classe 1 é a dos parâmetros mínimos da NBR 15527:2019."""
    padrao = TritonConfig().water_quality_target_class
    assert WATER_QUALITY_CLASSES[padrao].exige_filtracao_fina is False


def test_sem_polimento_o_dimensionamento_nao_cobra_filtro():
    r = size_etap(include_polishing_filter=False)
    assert r.polishing_capex == 0.0
    assert r.polishing_annual_opex == 0.0


def test_desmarcar_surte_efeito_em_todas_as_classes():
    """Era o defeito principal: nas classes 2 a 4 desmarcar não fazia nada."""
    assert CLASSES_QUE_RECOMENDAM, 'nenhuma classe recomenda filtração fina'
    for classe in CLASSES_QUE_RECOMENDAM:
        sem = size_etap(target_class_id=classe, include_polishing_filter=False)
        com = size_etap(target_class_id=classe, include_polishing_filter=True)
        assert sem.polishing_capex == 0.0, classe
        assert sem.polishing_annual_opex == 0.0, classe
        assert com.polishing_capex > 0.0, classe
        assert com.total_etap_capex > sem.total_etap_capex, classe
        assert com.total_etap_annual_opex > sem.total_etap_annual_opex, classe
        assert com.total_etap_co2e_kg_yr > sem.total_etap_co2e_kg_yr, classe


def test_a_recusa_da_recomendacao_fica_registrada():
    """Não é erro, e não é silêncio: o relatório precisa poder declarar a escolha."""
    for classe in CLASSES_QUE_RECOMENDAM:
        recusado = size_etap(target_class_id=classe, include_polishing_filter=False)
        aceito = size_etap(target_class_id=classe, include_polishing_filter=True)
        assert recusado.polishing_recommended_but_declined is True, classe
        assert aceito.polishing_recommended_but_declined is False, classe
        assert 'dispensada' in recusado.polishing_filter_type


def test_a_classe_1_nunca_marca_recusa():
    """Ela não recomenda, então não há o que recusar."""
    for incluir in (False, True):
        r = size_etap(target_class_id='classe_1', include_polishing_filter=incluir)
        assert r.polishing_recommended_but_declined is False


def test_a_classe_4_leva_carvao_ativado_e_as_demais_areia():
    """O tipo de filtro muda com a classe, e o custo com ele."""
    carvao = size_etap(target_class_id='classe_4', include_polishing_filter=True)
    areia = size_etap(target_class_id='classe_2', include_polishing_filter=True)
    assert 'Carvão' in carvao.polishing_filter_type
    assert carvao.polishing_capex > areia.polishing_capex


def _filtro_de_polimento_config(polimento: bool, classe: str='classe_4') -> TritonConfig:
    cfg = TritonConfig()
    cfg.water_quality_target_class = classe
    cfg.water_quality_polishing = polimento
    return cfg


def test_o_polimento_move_o_investimento_incremental():
    sem = capex_incremental_da_etap(_filtro_de_polimento_config(False))
    com = capex_incremental_da_etap(_filtro_de_polimento_config(True))
    assert com > sem
    esperado = size_etap(target_class_id='classe_4', include_polishing_filter=True).polishing_capex
    assert com - sem == pytest.approx(esperado)


def test_o_polimento_move_o_custeio_incremental():
    sem = opex_anual_incremental_da_etap(_filtro_de_polimento_config(False))
    com = opex_anual_incremental_da_etap(_filtro_de_polimento_config(True))
    esperado = size_etap(target_class_id='classe_4', include_polishing_filter=True).polishing_annual_opex
    assert com - sem == pytest.approx(esperado)


def test_a_regra_incremental_tem_uma_definicao_so():
    """Havia dois motores econômicos, e só um recebia a linha de tratamento.

    O núcleo tem de devolver exatamente o que o auxiliar compartilhado calcula:
    se divergirem, a aba econômica e o relatório mostram números diferentes para
    o mesmo projeto, que foi como o cloro chegou a ter cinco convenções.
    """
    from triton.core.economic import run_economic_analysis
    from triton.core.simulation import SingleTankSimulationResult
    sim = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    for polimento in (False, True):
        cfg = _filtro_de_polimento_config(polimento)
        econ = run_economic_analysis(cfg, sim)
        anual = sim.annual_pluvial_consumed_m3
        assert econ.etap_capex_brl == pytest.approx(capex_incremental_da_etap(cfg, anual, sim))
        assert econ.annual_etap_opex_brl == pytest.approx(opex_anual_incremental_da_etap(cfg, anual, sim))


def test_desligar_a_etap_zera_o_incremental():
    cfg = _filtro_de_polimento_config(True)
    cfg.etap_enabled = False
    assert capex_incremental_da_etap(cfg) == 0.0
    assert opex_anual_incremental_da_etap(cfg) == 0.0


def test_a_verba_ja_prevista_em_acessorios_e_descontada_uma_vez_so():
    """O desconto vale para a linha inteira, e não por estágio.

    Descontá-lo duas vezes faria o filtro de polimento parecer mais barato do que
    é quando há acessórios orçados.
    """
    from triton.core.cost_estimates import verba_generica_de_tratamento_brl
    verba = verba_generica_de_tratamento_brl('UTI')
    sem_acessorios, com_acessorios = (_filtro_de_polimento_config(True), _filtro_de_polimento_config(True))
    com_acessorios.cost_accessories = 800.0
    assert capex_incremental_da_etap(sem_acessorios) - capex_incremental_da_etap(com_acessorios) == pytest.approx(verba)


@pytest.fixture
def janela(qapp):
    pytest.importorskip('PySide6')
    from triton.core.simulation import SingleTankSimulationResult
    from triton.ui.main_window import MainWindow
    win = MainWindow()
    sim = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    sim.n_days_simulated = 365
    sim.total_pumped_liters = 330.0 * 365
    sim.total_pump_cycles = 365
    win.tab_tanks_simulation.last_single_result = sim
    win.tab_tanks_simulation._is_technical_only = False
    return win


def _reais(texto: str) -> float:
    return float(texto.replace('R$', '').replace('.', '').replace(',', '.').strip() or 0.0)


def test_a_caixa_comeca_desmarcada(janela):
    """O professor pediu que o padrão fosse não utilizar."""
    aba = janela.tab_water_quality
    assert aba.chk_polishing.isChecked() is False
    assert janela.config.water_quality_polishing is False


def test_trocar_de_classe_recomenda_mas_nao_marca_a_caixa(janela):
    """Marcar sozinho fazia o polimento parecer obrigatório."""
    aba = janela.tab_water_quality
    for classe in CLASSES_QUE_RECOMENDAM:
        aba.combo_class.setCurrentIndex(aba.combo_class.findData(classe))
        aba.on_class_changed()
        assert aba.chk_polishing.isChecked() is False, classe
        assert aba.lbl_polishing_reco.text(), f'{classe} não mostrou a recomendação'
    aba.combo_class.setCurrentIndex(aba.combo_class.findData('classe_1'))
    aba.on_class_changed()
    assert aba.lbl_polishing_reco.text() == ''


def test_o_investimento_e_a_manutencao_exibidos_acompanham_a_caixa(janela):
    """Era o sintoma relatado: marcar ou desmarcar não mexia nos dois valores.

    A aba econômica integrada soma o investimento à mão e monta o próprio fluxo
    de caixa, e não recebia a linha de tratamento. Ligar só o motor do núcleo
    deixava o número certo fora da tela.
    """
    aba, tab = (janela.tab_water_quality, janela.tab_economic)
    aba.combo_class.setCurrentIndex(aba.combo_class.findData('classe_4'))
    aba.on_class_changed()
    medidas = {}
    for estado in (False, True):
        aba.chk_polishing.setChecked(estado)
        aba.on_polishing_changed()
        tab.calculate_economics(force=True)
        tabela = tab.table_cashflow
        medidas[estado] = (_reais(tabela.item(0, 1).text()), _reais(tabela.item(1, 9).text()))
    esperado = size_etap(target_class_id='classe_4', include_polishing_filter=True)
    assert medidas[True][0] - medidas[False][0] == pytest.approx(esperado.polishing_capex)
    assert medidas[True][1] - medidas[False][1] == pytest.approx(esperado.polishing_annual_opex)


def test_o_payback_exibido_piora_com_o_filtro(janela):
    """Se o investimento sobe e a economia não, o retorno tem de demorar mais."""
    aba, tab = (janela.tab_water_quality, janela.tab_economic)
    aba.combo_class.setCurrentIndex(aba.combo_class.findData('classe_4'))
    aba.on_class_changed()
    textos = {}
    for estado in (False, True):
        aba.chk_polishing.setChecked(estado)
        aba.on_polishing_changed()
        tab.calculate_economics(force=True)
        textos[estado] = tab.lbl_val_payback.text()
    assert textos[True] != textos[False]


# ---- origem: tests/unit/test_triton_updates.py

def test_monthly_precision_payback_simple():
    """Valida se o payback simples é fracionário com precisão mensal."""
    res = run_robust_economic_analysis(initial_investment=12000.0, annual_water_saved_m3=1800.0, water_tariff_per_m3=10.0, sewage_tariff_per_m3=0.0, sewage_mode=0, water_tariff_escalation_rate=0.0, sewage_tariff_escalation_rate=0.0, elec_tariff_escalation_rate=0.0, inflation_rate=0.0, discount_rate=0.0, annual_om_cost_base=0.0, pump_power_kw=0.0, pump_hours_year=0.0, elec_tariff_kwh=0.0, analysis_period_years=5, annual_chlorine_cost=0.0)
    assert res.payback_simple_years == pytest.approx(8.0 / 12.0, rel=0.001)
    assert res.payback_discounted_years == pytest.approx(8.0 / 12.0, rel=0.001)


def test_monthly_precision_payback_discounted():
    """Valida se o payback descontado é calculado mês a mês com taxa de desconto."""
    res = run_robust_economic_analysis(initial_investment=10000.0, annual_water_saved_m3=1000.0, water_tariff_per_m3=5.0, sewage_tariff_per_m3=0.0, sewage_mode=0, water_tariff_escalation_rate=0.0, discount_rate=0.1, annual_om_cost_base=0.0, pump_power_kw=0.0, analysis_period_years=10)
    assert res.payback_simple_years == pytest.approx(2.0, rel=0.01)
    assert res.payback_discounted_years is not None
    assert res.payback_discounted_years > res.payback_simple_years
    assert res.payback_discounted_years > 2.0


# ==================================================================================================
# Ambiente e energia: emissões, cloro, bombeamento e arranjo
# ==================================================================================================

# ---- origem: tests/invariants/test_environmental_properties.py

def _environmental_properties_config(**alteracoes) -> EnvironmentalConfig:
    padrao = dict(lower_tank_vol=5000.0, annual_water_saved_m3=120.0, annual_pump_kwh=180.0, upper_tank_used=True, upper_tank_vol_liters=500.0, chlorine_dose_mg_l=2.0, chlorine_co2_kg_per_kg=25.0)
    padrao.update(alteracoes)
    return EnvironmentalConfig(**padrao)


@pytest.mark.parametrize('volume', [0.0, 1000.0, 5000.0, 20000.0, 100000.0])
def test_emissoes_nunca_sao_negativas(volume):
    """A1 — Massa e emissão são grandezas físicas não-negativas."""
    resultado = calculate_lca(volume, 120.0, _environmental_properties_config(lower_tank_vol=volume))
    for campo in ('lower_tank_mass_kg', 'upper_tank_mass_kg', 'total_pipes_co2_kg', 'pump_embodied_co2_kg', 'total_embodied_co2_kg', 'annual_pumping_co2_kg', 'annual_treatment_co2_kg', 'annual_chlorine_kg', 'annual_avoided_co2_kg'):
        valor = getattr(resultado, campo)
        assert valor >= 0.0, f"'{campo}' negativo ({valor}) para V = {volume} L"


def test_co2_incorporado_cresce_com_o_volume_da_cisterna():
    """A2 — Cisterna maior exige mais material, logo mais carbono incorporado."""
    valores = []
    for volume in (0.0, 1000.0, 3000.0, 8000.0, 20000.0, 50000.0):
        valores.append(calculate_lca(volume, 120.0, _environmental_properties_config(lower_tank_vol=volume)).total_embodied_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-09, f'CO2 incorporado caiu com cisterna maior: {valores}'


def test_co2_evitado_cresce_com_a_agua_aproveitada():
    """A3 — Substituir mais água de rede evita mais emissão de tratamento."""
    valores = []
    for agua in (0.0, 30.0, 90.0, 200.0, 500.0):
        valores.append(calculate_lca(5000.0, agua, _environmental_properties_config(annual_water_saved_m3=agua)).annual_avoided_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-09, f'CO2 evitado caiu com mais água: {valores}'


def test_emissao_de_bombeamento_cresce_com_o_consumo_eletrico():
    """A4 — Mais energia de recalque, mais emissão operacional."""
    valores = []
    for kwh in (0.0, 50.0, 200.0, 800.0):
        valores.append(calculate_lca(5000.0, 120.0, _environmental_properties_config(annual_pump_kwh=kwh)).annual_pumping_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-09, f'emissão de bombeamento não cresceu: {valores}'


def test_comprimento_de_tubulacao_nao_reduz_o_carbono_incorporado():
    """A5 — Mais metros de tubo nunca reduzem o material empregado."""
    valores = []
    for comprimento in (0.0, 10.0, 40.0, 120.0):
        config = _environmental_properties_config(pipes=[PipeInput(diameter_mm=100, length_m=comprimento)])
        valores.append(calculate_lca(5000.0, 120.0, config).total_pipes_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-09, f'CO2 das tubulações caiu com mais tubo: {valores}'


def test_saldo_liquido_e_a_diferenca_entre_evitado_e_operacional():
    """A6 — O saldo líquido fecha com as suas parcelas.

    saldo = evitado − (bombeamento + tratamento)
    """
    for volume, agua in ((2000.0, 60.0), (8000.0, 200.0), (25000.0, 400.0)):
        resultado = calculate_lca(volume, agua, _environmental_properties_config(lower_tank_vol=volume, annual_water_saved_m3=agua))
        esperado = resultado.annual_avoided_co2_kg - resultado.annual_pumping_co2_kg - resultado.annual_treatment_co2_kg
        assert resultado.net_annual_avoided_co2_kg == pytest.approx(esperado, rel=1e-09, abs=1e-09), f'saldo líquido não fecha para V={volume}, água={agua}: {resultado.net_annual_avoided_co2_kg} != {esperado}'


def test_inventario_detalhado_soma_o_carbono_incorporado():
    """A7 — O detalhamento por item reconstitui o total incorporado.

    Um inventário que não soma o próprio total inviabiliza auditoria da ACV.
    """
    resultado = calculate_lca(8000.0, 200.0, _environmental_properties_config(lower_tank_vol=8000.0))
    if not resultado.inventory_items:
        pytest.skip('inventário detalhado não disponível nesta configuração')
    soma = sum((item.embodied_co2_kg for item in resultado.inventory_items))
    assert soma == pytest.approx(resultado.total_embodied_co2_kg, rel=1e-06), f'itens do inventário somam {soma:.4f} kg, total declarado {resultado.total_embodied_co2_kg:.4f} kg'


def test_inventario_detalhado_reconstitui_o_saldo_operacional():
    """A7b — As parcelas operacionais do inventário reconstituem o saldo anual.

    No inventário, emissões evitadas entram com sinal negativo em `annual_op_co2_kg`,
    de modo que o saldo líquido anual é o simétrico da soma das parcelas operacionais.
    Verificar esse lado é mais exigente que o incorporado: envolve bombeamento,
    dosagem química e água evitada, com convenções de sinal distintas.
    """
    resultado = calculate_lca(8000.0, 200.0, _environmental_properties_config(lower_tank_vol=8000.0))
    if not resultado.inventory_items:
        pytest.skip('inventário detalhado não disponível nesta configuração')
    soma_operacional = sum((item.annual_op_co2_kg for item in resultado.inventory_items))
    assert -soma_operacional == pytest.approx(resultado.net_annual_avoided_co2_kg, rel=1e-06, abs=1e-09), f'parcelas operacionais somam {soma_operacional:.4f} kg/ano; saldo líquido declarado é {resultado.net_annual_avoided_co2_kg:.4f} kg/ano'


def test_a_cloracao_nao_depende_do_reservatorio_superior():
    """A8 — A cloração acompanha o tratamento, e não a caixa superior.

    Até setembro de 2026 esta propriedade dizia o contrário, e a ACV perdia o
    cloro ao desmarcar a caixa enquanto o econômico continuava a pagá-lo.
    """
    com = calculate_lca(5000.0, 150.0, _environmental_properties_config(upper_tank_used=True))
    sem = calculate_lca(5000.0, 150.0, _environmental_properties_config(upper_tank_used=False))
    assert sem.annual_chlorine_kg > 0.0
    assert sem.annual_chlorine_kg == com.annual_chlorine_kg


def test_payback_ambiental_nao_e_negativo():
    """A9 — Tempo de retorno ambiental é uma duração."""
    for volume in (1000.0, 5000.0, 20000.0):
        resultado = calculate_lca(volume, 150.0, _environmental_properties_config(lower_tank_vol=volume))
        assert resultado.environmental_payback_years >= 0.0, f'payback ambiental negativo ({resultado.environmental_payback_years}) para V = {volume} L'


def test_viabilidade_ambiental_concorda_com_o_saldo_acumulado():
    """A10 — O selo de viabilidade não pode contradizer o balanço de carbono."""
    for volume, agua in ((500.0, 10.0), (5000.0, 150.0), (50000.0, 400.0)):
        resultado = calculate_lca(volume, agua, _environmental_properties_config(lower_tank_vol=volume, annual_water_saved_m3=agua))
        if abs(resultado.lifetime_net_co2_saved_kg) < 1e-06:
            continue
        assert resultado.is_environmentally_viable == (resultado.lifetime_net_co2_saved_kg > 0), f'selo de viabilidade ({resultado.is_environmentally_viable}) contradiz o saldo acumulado ({resultado.lifetime_net_co2_saved_kg:.4f} kg) para V = {volume} L'


def test_varredura_preserva_a_monotonicidade_do_carbono_incorporado():
    """A12 — A varredura ambiental herda a monotonicidade do cálculo individual."""
    mapa_de_volumes = [(0.0, 0.0), (1000.0, 40.0), (3000.0, 80.0), (8000.0, 110.0), (20000.0, 130.0)]
    resultado = run_environmental_sweep(mapa_de_volumes, _environmental_properties_config())
    assert len(resultado.sweep_details) == len(mapa_de_volumes)
    incorporado = [d['lca_result'].total_embodied_co2_kg for d in resultado.sweep_details]
    for anterior, seguinte in zip(incorporado, incorporado[1:]):
        assert seguinte >= anterior - 1e-09, f'CO2 incorporado caiu ao longo da varredura: {incorporado}'


def test_varredura_concorda_com_o_calculo_individual():
    """A13 — Varrer volumes equivale a calcular cada volume isoladamente.

    Se divergirem, a varredura estaria propagando estado entre alternativas — o mesmo
    tipo de erro que produziu a divergência de repartição nos kernels acelerados.
    """
    mapa_de_volumes = [(2000.0, 60.0), (9000.0, 140.0)]
    config = _environmental_properties_config()
    varredura = run_environmental_sweep(mapa_de_volumes, config)
    for (volume, agua), detalhe in zip(mapa_de_volumes, varredura.sweep_details):
        isolado = calculate_lca(volume, agua, config)
        assert detalhe['lca_result'].total_embodied_co2_kg == pytest.approx(isolado.total_embodied_co2_kg, rel=1e-09), f'varredura diverge do cálculo isolado em V = {volume} L'


# ---- origem: tests/unit/test_chlorination.py
_ARQUIVO_CHLORINATION = str(_TESTES / 'unit/test_chlorination.py')

def test_a_pureza_converte_cloro_ativo_em_produto():
    """É a conversão que faltava, e metade da divergência de 11,7 vezes."""
    c = Cloracao(dose_mg_por_litro=1.5, pureza=0.65)
    assert c.cloro_ativo_kg_por_m3 == pytest.approx(0.0015)
    assert c.produto_kg_por_m3 == pytest.approx(0.0015 / 0.65)
    assert c.produto_kg_por_m3 > c.cloro_ativo_kg_por_m3


def test_emissao_e_massa_de_produto_vezes_fator():
    c = cloracao_padrao()
    assert c.co2e_kg_por_m3 == pytest.approx(c.produto_kg_por_m3 * FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO)


def test_valores_anuais_escalam_com_o_volume():
    c = cloracao_padrao()
    assert c.co2e_anual_kg(100.0) == pytest.approx(100.0 * c.co2e_kg_por_m3)
    assert c.massa_anual_de_produto_kg(100.0) == pytest.approx(100.0 * c.produto_kg_por_m3)
    assert c.co2e_anual_kg(-5.0) == 0.0, 'volume negativo não pode gerar emissão negativa'


def test_pureza_fora_da_faixa_falha_com_mensagem_util():
    """O engano provável é escrever 65 em vez de 0,65."""
    with pytest.raises(ValueError, match='0,65'):
        Cloracao(pureza=65.0)
    with pytest.raises(ValueError):
        Cloracao(pureza=0.0)


def test_dose_negativa_falha():
    with pytest.raises(ValueError):
        Cloracao(dose_mg_por_litro=-1.0)


def test_dose_padrao_dentro_da_faixa_normativa():
    """A NBR 15527:2019, item 4.6.5, trabalha entre 0,5 e 2,0 mg/L."""
    assert 0.5 <= DOSE_PADRAO_MG_POR_LITRO <= 2.0


def test_fator_plausivel_para_hipoclorito():
    """Cloro de rota cloro-álcali fica entre 1 e 2 kg CO₂e/kg."""
    assert 0.5 < FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO < 5.0


def test_o_fator_do_cloro_nunca_volta_a_ser_o_preco():
    """Guarda estrutural contra o retorno do 25,0.

    O valor circulava por seis arquivos — motor, interface, CLI, parser — e em
    todos era o preço em reais ocupando um campo de emissão. Basta que reapareça
    num deles para o resultado ambiental voltar a ser dez vezes maior do que
    deveria.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_CHLORINATION))))
    pacote = os.path.join(raiz, 'triton')
    padrao = re.compile('chlorine_co2\\w*\\s*[=:]\\s*2[45]\\.?\\d*')
    ofensores = []
    for pasta, _, arquivos in os.walk(pacote):
        for nome in arquivos:
            if not nome.endswith('.py'):
                continue
            caminho = os.path.join(pasta, nome)
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                for numero, linha in enumerate(arquivo, start=1):
                    if padrao.search(linha):
                        ofensores.append(f'{os.path.relpath(caminho, raiz)}:{numero}')
    assert not ofensores, f'Fator de emissão do cloro com valor de custo (25 R$/kg): {ofensores}'


def test_os_tres_modulos_partem_da_mesma_cadeia():
    from triton.core.environmental import EnvironmentalConfig
    from triton.core.parser import TritonConfig
    ambiental = EnvironmentalConfig()
    projeto = TritonConfig()
    assert ambiental.chlorine_dose_mg_l == DOSE_PADRAO_MG_POR_LITRO
    assert ambiental.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    assert ambiental.chlorine_product_purity == PUREZA_PADRAO
    assert projeto.chlorine_dose_mg_l == DOSE_PADRAO_MG_POR_LITRO
    assert projeto.chlorine_co2_kg_per_kg == FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO


def test_cloracao_e_sempre_aplicada_na_linha_de_tratamento():
    """É a única barreira que deixa residual livre.

    O programa tratava cloro, ultravioleta e ozônio como escolhas exclusivas, e
    admitia «sem desinfecção». Ultravioleta e ozônio desinfetam na passagem e não
    deixam residual, de modo que somam-se à cloração em vez de substituí-la.
    """
    from triton.core.water_quality import size_etap
    for escolha in ('cloro', 'uv', 'ozonio', 'nenhum'):
        resultado = size_etap(disinfection_choice=escolha, annual_pluvial_consumed_m3=120.0)
        assert resultado.annual_chlorine_kg > 0, f'sem cloro em {escolha!r}'
        assert any(('lora' in etapa for etapa in resultado.disinfection_stages))


def test_barreiras_adicionais_somam_custo_e_emissao():
    from triton.core.water_quality import size_etap
    so_cloro = size_etap(disinfection_choice='cloro', annual_pluvial_consumed_m3=120.0)
    com_uv = size_etap(disinfection_choice='uv', annual_pluvial_consumed_m3=120.0)
    assert com_uv.total_etap_capex > so_cloro.total_etap_capex
    assert com_uv.total_etap_annual_opex > so_cloro.total_etap_annual_opex
    assert com_uv.total_etap_co2e_kg_yr > so_cloro.total_etap_co2e_kg_yr
    assert com_uv.uv_annual_kwh > 0


# ---- origem: tests/unit/test_pump_hydraulics.py

def test_energia_especifica_e_rho_g_h_sobre_eta():
    """Confere contra a conta feita à mão, em unidades do SI."""
    esperado = 1000.0 * 9.81 * 12.0 / (0.55 * 3600000.0)
    assert energia_especifica_kwh_por_m3(12.0, 0.55) == pytest.approx(esperado)


def test_energia_especifica_nao_depende_da_potencia():
    """É o ponto central: elevar 1 m³ a uma altura custa o mesmo, com bomba grande ou pequena.

    O que muda com a potência é o tempo de operação, não o consumo por metro
    cúbico. Uma bomba superdimensionada custa mais no investimento, não na conta
    de luz por m³ elevado.
    """
    a = ponto_de_operacao(0.25 * CV_TO_KW, 12.0, rendimento=0.55)
    b = ponto_de_operacao(2.0 * CV_TO_KW, 12.0, rendimento=0.55)
    assert a.energia_especifica_kwh_m3 == pytest.approx(b.energia_especifica_kwh_m3)
    assert b.vazao_l_h > 7 * a.vazao_l_h


def test_a_vazao_acompanha_a_potencia():
    """Era o defeito principal: 2.280 L/h valia de 1/4 a 2 CV."""
    vazoes = [vazao_l_por_h(cv * CV_TO_KW, 12.0, 0.55) for cv in (0.25, 0.5, 1.0, 2.0)]
    assert vazoes == sorted(vazoes)
    assert vazoes[3] == pytest.approx(8 * vazoes[0], rel=1e-06)


def test_a_vazao_cai_quando_a_altura_sobe():
    alta = vazao_l_por_h(0.5 * CV_TO_KW, 8.0, 0.55)
    baixa = vazao_l_por_h(0.5 * CV_TO_KW, 30.0, 0.55)
    assert alta > 3 * baixa


def test_rendimento_cresce_com_o_porte():
    """Tratar toda bomba com 55% penalizava a grande, que é a mais eficiente."""
    valores = [rendimento_tipico(cv * CV_TO_KW) for cv in (0.25, 0.5, 1.0, 1.5, 2.0)]
    assert valores == sorted(valores)
    assert all((0.3 < v <= 0.8 for v in valores))


def test_rendimento_fora_da_faixa_falha_com_mensagem_util():
    """O engano provável é escrever 55 em vez de 0,55."""
    with pytest.raises(ValueError, match='0,55'):
        energia_especifica_kwh_por_m3(12.0, 55.0)


def test_energia_pela_vazao_nao_divide_por_eta_de_novo():
    """A potência de placa é o que o motor consome: e = P/Q, e nada mais.

    A conta anterior fazia P x horas / η, dividindo pela perda uma segunda vez.
    Com η de 60%, superestimava em 67%.
    """
    potencia_kw, vazao_l_h = (0.7355, 3000.0)
    correta = energia_especifica_a_partir_da_vazao(potencia_kw, vazao_l_h)
    assert correta == pytest.approx(0.7355 / 3.0)
    antiga = potencia_kw * (1000.0 / vazao_l_h) / 0.6
    assert antiga == pytest.approx(correta / 0.6)


def test_as_duas_formas_coincidem_no_ponto_de_operacao():
    """ρ·g·H/η e P/Q dão o mesmo quando Q é a vazão que a bomba entrega em H.

    Se divergirem, alguma das duas está errada — e é essa coerência que permite
    usar uma quando a vazão é declarada e a outra quando não é.
    """
    potencia_kw, altura, eta = (0.5 * CV_TO_KW, 12.0, 0.55)
    vazao = vazao_l_por_h(potencia_kw, altura, eta)
    assert energia_especifica_a_partir_da_vazao(potencia_kw, vazao) == pytest.approx(energia_especifica_kwh_por_m3(altura, eta), rel=1e-09)


def test_altura_padrao_e_de_casa_e_nao_de_predio():
    """O par de valores fixos anterior implicava 67 m, cinco vezes o desnível real."""
    assert 8.0 <= ALTURA_MANOMETRICA_PADRAO_M <= 15.0
    implicada_pelo_valor_antigo = 0.3334 * 0.55 / (1000.0 * 9.81 / 3600000.0)
    assert implicada_pelo_valor_antigo > 4 * ALTURA_MANOMETRICA_PADRAO_M


def test_consumo_de_recurso_e_plausivel_para_recalque_residencial():
    """Entre 0,05 e 0,20 kWh/m³ para um desnível de casa.

    Fora dessa faixa o número denuncia altura ou rendimento errados. O valor
    antigo, de 0,40, ficava muito acima.
    """
    valor = consumo_especifico_padrao_kwh_por_m3()
    assert 0.05 < valor < 0.2, valor


def test_o_exportador_cad_usa_a_mesma_vazao():
    """Havia uma segunda tabela ali, com 2,4 m³/h para meio CV."""
    from triton.core.cad_exporter import calculate_forchheimer_pumping_diameters
    resultado = calculate_forchheimer_pumping_diameters(pump_hp='1/2', daily_pumped_volume_l=1000.0)
    esperado_m3_h = vazao_l_por_h(0.5 * CV_TO_KW) / 1000.0
    obtido = resultado.get('flow_m3_h', resultado.get('q_m3_h'))
    assert obtido == pytest.approx(esperado_m3_h, rel=1e-06)


# ---- origem: tests/unit/test_energia_de_partida.py

@pytest.fixture(scope='module')
def sim():
    rng = np.random.default_rng(11)
    chuva = np.clip(rng.gamma(0.55, 8.0, 1826), 0, None)
    return run_single_simulation(precip_data=chuva, lower_tank_vol=5000.0, area=150.0, runoff_coeff=0.85, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4, upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0)


def _energia_de_partida_config():
    cfg = TritonConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw = 0.37
    cfg.pump_efficiency = 0.0
    cfg.pump_flow_rate = 0.0
    cfg.pump_manometric_head_m = ALTURA_MANOMETRICA_PADRAO_M
    cfg.pump_startup_time_h = 0.03
    return cfg


def test_a_energia_e_recalque_mais_partidas_pelo_rendimento_do_motor(sim):
    """Recalque por ρgH/(η_bomba·η_motor); partidas por placa/η_motor."""
    cfg = _energia_de_partida_config()
    r = compute_annual_pump_energy(cfg, sim)
    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    t_part = sim.total_pump_cycles / (sim.total_days / 365.25) * cfg.pump_startup_time_h
    esperado = especifica * r.annual_pumped_m3 + cfg.pump_power_kw * t_part / eta_motor
    assert r.annual_kwh == pytest.approx(esperado, rel=1e-09)


def test_o_rendimento_do_motor_sai_da_tabela_da_norma():
    """Tabela 13 da ABNT NBR 17094-2:2016, motores de 2 polos, linha IR1."""
    assert rendimento_do_motor(0.37) == pytest.approx(0.605)
    assert rendimento_do_motor(0.75) == pytest.approx(0.693)
    assert rendimento_do_motor(0.18) == pytest.approx(0.5)


def test_o_rendimento_do_motor_informado_prevalece(sim):
    """Quem lê a placa informa o valor dela, e o programa obedece."""
    cfg = _energia_de_partida_config()
    padrao = compute_annual_pump_energy(cfg, sim).annual_kwh
    cfg.pump_motor_efficiency = 72.0
    melhor = compute_annual_pump_energy(cfg, sim).annual_kwh
    assert melhor < padrao
    assert melhor / padrao == pytest.approx(rendimento_do_motor(0.37) / 0.72, rel=1e-09)


def test_as_partidas_nao_dividem_pelo_rendimento_da_bomba(sim):
    """Na partida não há vazão, logo não há perda hidráulica a descontar."""
    cfg = _energia_de_partida_config()
    r = compute_annual_pump_energy(cfg, sim)
    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    t_part = r.annual_cycles * cfg.pump_startup_time_h
    com_bomba = especifica * r.annual_pumped_m3 + cfg.pump_power_kw * t_part / (eta * eta_motor)
    assert com_bomba > r.annual_kwh


def test_sem_partidas_a_energia_e_so_o_recalque(sim):
    cfg = _energia_de_partida_config()
    cfg.pump_startup_time_h = 0.0
    r = compute_annual_pump_energy(cfg, sim)
    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    assert r.annual_kwh == pytest.approx(especifica * r.annual_pumped_m3, rel=1e-09)


def test_o_consumo_especifico_de_recurso_segue_a_mesma_convencao():
    """O valor de recurso usado quando não há simulação vem da mesma conta."""
    assert 0.0 < consumo_especifico_padrao_kwh_por_m3() < 0.3


def test_o_economico_e_a_acv_calculam_a_mesma_energia(sim):
    """Duas cópias da fórmula divergiriam, e foi assim que ela se espalhou."""
    from triton.core.economic import run_economic_analysis
    cfg = _energia_de_partida_config()
    cfg.water_tariffs = [(0.0, 10.0, 3.08, 1), (10.0, 999999.0, 6.81, 1)]
    econ = run_economic_analysis(cfg, sim)
    bomba = compute_annual_pump_energy(cfg, sim)
    assert econ.annual_pump_kwh == pytest.approx(bomba.annual_kwh, rel=0.02)


# ---- origem: tests/unit/test_energia_de_bombeamento_unica.py
_ARQUIVO_ENERGIA_DE_BOMBEAMENTO_UNICA = str(_TESTES / 'unit/test_energia_de_bombeamento_unica.py')

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_ENERGIA_DE_BOMBEAMENTO_UNICA))))


_PACOTE = os.path.join(_RAIZ, 'triton')


def _energia_de_bombeamento_unica_config(rendimento: float=55.0) -> TritonConfig:
    cfg = TritonConfig()
    cfg.pump_power_kw = 0.37
    cfg.pump_flow_rate = 2280.0
    cfg.pump_efficiency = rendimento
    cfg.pump_startup_time_h = 0.0167
    return cfg


def _energia_de_bombeamento_unica_sim(litros_por_dia: float=330.0) -> SingleTankSimulationResult:
    r = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=50.0, avg_pluvial_consumed_l_day=litros_por_dia, avg_potable_consumed_l_day=330.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0, pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0)
    r.n_days_simulated = 365
    r.total_pumped_liters = litros_por_dia * 365.0
    r.total_pump_cycles = 365
    return r


def test_a_energia_nao_divide_pelo_rendimento_uma_segunda_vez():
    """A potência de placa é o que o motor consome da tomada.

    Com vazão informada, a energia por m³ é P/Q e nada mais. A fórmula antiga
    fazia P × horas / η, o que embutia a perda duas vezes.
    """
    cfg, sim = (_energia_de_bombeamento_unica_config(), _energia_de_bombeamento_unica_sim())
    correta = compute_annual_pump_energy(cfg, sim, upper_tank_used=True).annual_kwh
    anos = sim.total_days / 365.25
    horas_recalque = sim.total_pumped_liters / anos / cfg.pump_flow_rate
    horas_partida = sim.total_pump_cycles / anos * cfg.pump_startup_time_h
    antiga = cfg.pump_power_kw * (horas_recalque + horas_partida) / (cfg.pump_efficiency / 100.0)
    from triton.core.pump_hydraulics import rendimento_do_motor
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    assert correta == pytest.approx(cfg.pump_power_kw * (horas_recalque + horas_partida) / eta_motor, rel=1e-09)
    assert antiga / correta == pytest.approx(eta_motor / (cfg.pump_efficiency / 100.0), rel=1e-09)


def test_o_excesso_da_formula_antiga_e_exatamente_um_sobre_eta():
    """Com rendimento pior, o erro cresce — é a assinatura do defeito."""
    for rendimento in (40.0, 55.0, 70.0):
        cfg, sim = (_energia_de_bombeamento_unica_config(rendimento), _energia_de_bombeamento_unica_sim())
        correta = compute_annual_pump_energy(cfg, sim, upper_tank_used=True)
        recalque_correto = cfg.pump_power_kw / (cfg.pump_flow_rate / 1000.0) * correta.annual_pumped_m3
        recalque_antigo = recalque_correto / (rendimento / 100.0)
        assert recalque_antigo / recalque_correto == pytest.approx(100.0 / rendimento)


def test_sem_reservatorio_superior_nao_ha_recalque():
    assert compute_annual_pump_energy(_energia_de_bombeamento_unica_config(), _energia_de_bombeamento_unica_sim(), upper_tank_used=False).annual_kwh == 0.0


def test_a_energia_acompanha_o_volume_recalcado():
    pouco = compute_annual_pump_energy(_energia_de_bombeamento_unica_config(), _energia_de_bombeamento_unica_sim(150.0), upper_tank_used=True)
    muito = compute_annual_pump_energy(_energia_de_bombeamento_unica_config(), _energia_de_bombeamento_unica_sim(600.0), upper_tank_used=True)
    assert muito.annual_kwh > pouco.annual_kwh
    assert muito.specific_kwh_per_m3 == pytest.approx(pouco.specific_kwh_per_m3, rel=0.25)


def _fontes():
    for dp, _dn, fn in os.walk(_PACOTE):
        if '__pycache__' in dp:
            continue
        for f in fn:
            if f.endswith('.py'):
                caminho = os.path.join(dp, f)
                yield (os.path.relpath(caminho, _RAIZ).replace('\\', '/'), open(caminho, encoding='utf-8', errors='replace').read())


def test_nenhuma_tela_divide_horas_de_bomba_pelo_rendimento():
    """Varredura pela assinatura textual da fórmula antiga.

    Quatro cópias sobreviveram à correção porque cada uma parecia local e
    inofensiva. A verificação por física não as pega — elas não passam por
    `compute_annual_pump_energy`. Só a varredura pega.
    """
    padrao = re.compile('(?:t_rec|t_part|run_h|start_h|p_hrs|pump_hours)[^\\n]*?/\\s*max\\(\\s*0\\.01\\s*,\\s*[a-z_.]*pump_efficiency\\s*/\\s*100', re.IGNORECASE)
    achados = []
    for rel, texto in _fontes():
        for m in padrao.finditer(texto):
            linha = texto[:m.start()].count('\n') + 1
            achados.append(f'{rel}:{linha}')
    assert not achados, 'cópia da fórmula antiga de energia de bombeamento: ' + str(achados)


def test_so_o_nucleo_converte_rendimento_percentual_em_fracao():
    """`pump_efficiency / 100` fora do núcleo é sinal de conta própria.

    O rendimento entra na energia específica, que vive em `pump_energy.py` e
    `economic.py`. Qualquer outro módulo que o converta está refazendo a conta.
    """
    permitidos = {'triton/core/pump_energy.py', 'triton/core/economic.py'}
    fora = [rel for rel, texto in _fontes() if rel not in permitidos and re.search('pump_efficiency\\s*/\\s*100', texto)]
    assert not fora, fora


# ---- origem: tests/unit/test_grid_emission_factors.py

def test_ano_fora_da_serie_falha_alto():
    """Pedir um ano sem publicação deve falhar, nunca devolver um valor vizinho."""
    with pytest.raises(KeyError):
        fatores.fator_anual(1999)
    with pytest.raises(KeyError):
        fatores.fator_anual(fatores.anos_disponiveis()[-1] + 5)


def test_mes_invalido_falha():
    with pytest.raises(ValueError):
        fatores.fator_mensal(2025, 0)
    with pytest.raises(ValueError):
        fatores.fator_mensal(2025, 13)


def test_config_ambiental_usa_uma_base_declarada_de_co2eq():
    """O padrão da ACV tem de ser CO₂-equivalente, com a base declarada.

    Uma versão intermediária deste módulo fez a ACV ler a série anual do MCTI,
    que é de **CO₂ apenas** e cobre só a geração. Era erro de grandeza, e
    subestimava o bombeamento. O teste fixa a correção.
    """
    config = EnvironmentalConfig()
    assert config.grid_co2_factor_basis in fatores.bases_disponiveis()
    assert config.grid_co2_factor_kg_kwh == fatores.fator_co2eq(config.grid_co2_factor_basis)


def test_o_fator_da_acv_nao_e_o_do_mcti():
    """Guarda contra a reintrodução do erro CO₂ × CO₂e.

    O fator de CO₂e usado pela ACV tem de ser maior que o fator de CO₂ da
    geração: ele cobre mais gases e uma fronteira mais ampla. Se algum dia
    passar a coincidir com a série do MCTI, alguém terá trocado as grandezas.
    """
    config = EnvironmentalConfig()
    co2_apenas = fatores.fator_anual(fatores.ANO_PADRAO)
    assert config.grid_co2_factor_kg_kwh > co2_apenas, 'o fator de CO₂e da ACV não pode ser menor ou igual ao de CO₂ da geração'


def test_base_desconhecida_falha_alto():
    with pytest.raises(KeyError):
        fatores.fator_co2eq('base_que_nao_existe')


# ---- origem: tests/unit/test_arranjo_de_abastecimento.py

def _arranjo_de_abastecimento_chuva(anos=3):
    rng = np.random.default_rng(7)
    dias = int(365 * anos)
    return np.where(rng.random(dias) < 0.4, rng.gamma(0.8, 12.0, dias), 0.0)


def _projeto(arranjo):
    cfg = TritonConfig()
    cfg.supply_arrangement = arranjo
    cfg.upper_tank_used = 1 if arranjo == RECALQUE else 0
    cfg.residents_count = 4
    cfg.cost_lower_tank = 3000.0
    return cfg


def _arranjo_de_abastecimento_simular(cfg):
    recalque = arranjo_de(cfg) == RECALQUE
    return run_single_simulation(precip_data=_arranjo_de_abastecimento_chuva(), lower_tank_vol=5000.0, area=150.0, discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4, upper_tank_vol=500.0 if recalque else 0.0, upper_tank_used=recalque, pumping_threshold=150.0 if recalque else 0.0)


@pytest.mark.parametrize('arranjo', [GRAVIDADE, NAO_INFORMADO])
def test_sem_bomba_nao_ha_energia_em_modulo_algum(arranjo):
    cfg = _projeto(arranjo)
    sim = _arranjo_de_abastecimento_simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    assert energia.annual_kwh == 0.0
    assert run_economic_analysis(cfg, sim).annual_pump_kwh == 0.0
    acv = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3, EnvironmentalConfig(supply_arrangement=cfg.supply_arrangement, upper_tank_used=False))
    assert acv.annual_pumping_co2_kg == 0.0


@pytest.mark.parametrize('arranjo', [RECALQUE, PRESSURIZACAO])
def test_economico_e_acv_usam_a_mesma_energia(arranjo):
    cfg = _projeto(arranjo)
    sim = _arranjo_de_abastecimento_simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    econ = run_economic_analysis(cfg, sim)
    assert energia.annual_kwh > 0
    assert econ.annual_pump_kwh == pytest.approx(energia.annual_kwh, rel=1e-09)


def test_pressurizacao_bombeia_todo_o_volume_pluvial():
    cfg = _projeto(PRESSURIZACAO)
    sim = _arranjo_de_abastecimento_simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    assert energia.annual_pumped_m3 == pytest.approx(sim.annual_pluvial_consumed_m3)
    assert energia.annual_cycles == round(4 * ACIONAMENTOS_POR_PESSOA_DIA * 365.25)


def test_a_pressao_so_pesa_quando_a_curva_limita_a_vazao():
    """Enquanto o modelo entrega mais que o ponto de uso, quem dita o tempo ligado
    é o ponto; acima disso, a curva estrangula a vazão e a bomba fica mais tempo ligada."""
    cfgs = {h: _projeto(PRESSURIZACAO) for h in (12.0, 18.0, 24.0)}
    for h, cfg in cfgs.items():
        cfg.pressurizer_pressure_m = h
    sim = _arranjo_de_abastecimento_simular(cfgs[12.0])
    e = {h: compute_annual_pump_energy(cfg, sim).annual_kwh for h, cfg in cfgs.items()}
    assert e[12.0] == pytest.approx(e[18.0], rel=1e-09)
    assert e[24.0] == pytest.approx(e[12.0] * 9.0 / (40.0 * 3.0 / 27.0), rel=1e-06)


def test_o_modelo_maior_gasta_mais_quando_o_ponto_limita_a_vazao():
    """ABNT NBR 5626:2020, 6.5.11.12: a escolha da bomba é que minimiza a energia."""
    pequeno, grande = (_projeto(PRESSURIZACAO), _projeto(PRESSURIZACAO))
    grande.pressurizer_model = 'komeco_tp825t'
    sim = _arranjo_de_abastecimento_simular(pequeno)
    e_p = compute_annual_pump_energy(pequeno, sim)
    e_g = compute_annual_pump_energy(grande, sim)
    assert e_g.pump_hours_year == pytest.approx(e_p.pump_hours_year)
    assert e_g.annual_kwh > e_p.annual_kwh


def test_o_retardo_eletronico_soma_tempo_a_cada_partida():
    from triton.core.pressurizer_catalog import POR_CHAVE, energia
    syllent = POR_CHAVE['syllent_impulse']
    sem = energia(syllent, 60.0, 12.0, 0.0)
    com = energia(syllent, 60.0, 12.0, 7373.0)
    assert com.horas_ano - sem.horas_ano == pytest.approx(7373.0 * 10.0 / 3600.0)


def test_personalizado_usa_os_dados_digitados():
    cfg = _projeto(PRESSURIZACAO)
    cfg.pressurizer_model = 'personalizado'
    cfg.pressurizer_power_kw, cfg.pressurizer_flow_l_min = (0.37, 20.0)
    cfg.pressurizer_point_flow_l_min, cfg.pressurizer_post_run_s = (10.0, 0.0)
    sim = _arranjo_de_abastecimento_simular(cfg)
    e = compute_annual_pump_energy(cfg, sim)
    horas = sim.annual_pluvial_consumed_m3 * 1000.0 / 10.0 / 60.0
    assert e.pump_hours_year == pytest.approx(horas)
    assert e.annual_kwh == pytest.approx(0.37 / 0.605 * horas)


def test_o_menor_modelo_que_atende():
    from triton.core.pressurizer_catalog import menor_que_atende
    assert menor_que_atende(18.0).chave == 'komeco_tp820t'
    assert menor_que_atende(24.0).chave == 'komeco_tp825t'
    assert menor_que_atende(50.0) is None


def test_gravidade_nao_compra_nem_fabrica_motobomba():
    com_bomba, sem_bomba = (_projeto(PRESSURIZACAO), _projeto(GRAVIDADE))
    sim = _arranjo_de_abastecimento_simular(sem_bomba)
    assert run_economic_analysis(com_bomba, sim).capex_total - run_economic_analysis(sem_bomba, sim).capex_total == pytest.approx(com_bomba.pump_unit_cost * com_bomba.pump_count)
    acv = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3, EnvironmentalConfig(supply_arrangement=GRAVIDADE, upper_tank_used=False))
    assert acv.pump_embodied_co2_kg == 0.0
    assert acv.upper_tank_mass_kg == 0.0


@pytest.mark.parametrize('arranjo', [RECALQUE, PRESSURIZACAO, GRAVIDADE])
def test_cloracao_entra_na_acv_em_qualquer_arranjo(arranjo):
    acv = calculate_lca(5000.0, 80.0, EnvironmentalConfig(supply_arrangement=arranjo, upper_tank_used=arranjo == RECALQUE))
    assert acv.annual_treatment_co2_kg > 0


def test_so_o_recalque_tem_caixa_superior_no_carbono():
    for arranjo, esperado in ((RECALQUE, True), (PRESSURIZACAO, False)):
        acv = calculate_lca(5000.0, 80.0, EnvironmentalConfig(supply_arrangement=arranjo))
        assert (acv.upper_tank_mass_kg > 0) is esperado


def test_arquivo_antigo_sem_caixa_abre_como_nao_informado():
    cfg = TritonConfig()
    cfg.upper_tank_used = 0
    assert arranjo_de(cfg) == NAO_INFORMADO
    cfg.upper_tank_used = 1
    assert arranjo_de(cfg) == RECALQUE


def test_arranjo_sobrevive_a_gravar_e_reabrir():
    cfg = _projeto(PRESSURIZACAO)
    cfg.pressurizer_pressure_m = 21.0
    cfg.pressurizer_starts_per_person_day = 6.0
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, 'p.triton')
        export_triton_json(cfg, caminho, precip_data=_arranjo_de_abastecimento_chuva(1))
        with open(caminho, encoding='utf-8') as f:
            assert json.load(f)['inputs']['reservoirs_and_pumping']['supply_arrangement'] == PRESSURIZACAO
        lido = load_triton_project(caminho)['config']
    assert arranjo_de(lido) == PRESSURIZACAO
    assert lido.pressurizer_pressure_m == 21.0
    assert lido.pressurizer_starts_per_person_day == 6.0


# ---- origem: tests/unit/test_quantitativo_do_arranjo.py

def _simulacao():
    rng = np.random.default_rng(3)
    chuva = np.where(rng.random(730) < 0.35, rng.exponential(12, 730), 0.0)
    return run_single_simulation(chuva, 5000.0, area=150, total_demand_per_day=400, rainwater_share=0.4)


def test_todo_tipo_de_peca_tem_onde_ser_contado():
    tipos = {t['type_id'] for t in COMPONENT_TYPES}
    sem_destino = tipos - set(CATALOGO_DE_PECAS) - set(DESTINO_PROPRIO)
    assert not sem_destino, sem_destino


@pytest.mark.parametrize('volume, area, pavimentos, caixa', [(1500, 60, 1, 500), (5000, 150, 2, 1000), (10000, 180, 3, 1000), (30000, 400, 6, 3000)])
@pytest.mark.parametrize('descarte, etap', [(False, True), (True, True), (True, False), (False, False)])
@pytest.mark.parametrize('abastecimento, bombas', [('recalque', 1), ('recalque', 2), ('pressurizacao', 2), ('gravidade', 1)])
def test_nada_do_arranjo_fica_sem_custo_ou_sem_carbono(volume, area, pavimentos, caixa, descarte, etap, abastecimento, bombas):
    layout = generate_study_layout({'lower_vol': volume, 'area': area, 'floors': pavimentos, 'upper_vol': caixa, 'supply_arrangement': abastecimento, 'pump_count': bombas})
    q = levantar(layout, subsistema_de_descarte=descarte, etap=etap)
    assert conferir_cobertura(q) == []
    assert len({i.item for i in q.itens if i.unidade == 'un' and i.tipo not in ('conexao',)}) == len(layout['bim_components'])


def test_a_conferencia_aponta_a_peca_esquecida():
    """Uma peça sem catálogo nem linha própria aparece na lista, e não some."""
    layout = generate_study_layout({'lower_vol': 5000, 'area': 150})
    layout['bim_components'].append({'instance_id': 'XX-01', 'type_id': 'peca_nova', 'level': 'Térreo', 'position_mm': {'x': 0, 'y': 0, 'z': 0}, 'rotation_deg': 0, 'parameters': {}})
    from triton.core import bim_exporter
    bim_exporter.COMPONENT_TYPES.append({'type_id': 'peca_nova', 'cad_block': 'TRITON_REGISTRO', 'revit_category': 'OST_PipeAccessory', 'parameters': []})
    try:
        q = levantar(layout)
    except Exception:
        pytest.skip('o manifesto recusa tipo desconhecido antes do quantitativo')
    finally:
        bim_exporter.COMPONENT_TYPES.pop()
    assert any(('XX-01' in f for f in conferir_cobertura(q)))


def _projeto_novo():
    cfg = TritonConfig()
    cfg.capex_do_arranjo = True
    return cfg


def test_o_capex_le_a_tubulacao_e_os_acessorios_do_arranjo():
    cfg = _projeto_novo()
    q = quantitativo_do_projeto(cfg)
    run_economic_analysis(cfg, _simulacao())
    assert cfg.cost_piping == pytest.approx(q.custo_de_tubulacao)
    assert cfg.cost_accessories == pytest.approx(q.custo_de_acessorios)
    assert cfg.pipes_list == q.pipes_list()


def test_a_acv_le_a_tubulacao_e_soma_as_pecas_do_arranjo():
    import triton.cli as cli
    cfg = _projeto_novo()
    sim = _simulacao()
    q = quantitativo_do_projeto(cfg)
    env_cfg = cli._environmental_config(cfg, sim, 150.0, None)
    assert sum((p.length_m for p in env_cfg.pipes)) == pytest.approx(sum(q.tubos_m_por_dn.values()), abs=0.01)
    lca = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3, env_cfg)
    arranjo = sum((i.embodied_co2_kg for i in lca.inventory_items if i.category.startswith('Arranjo 3D')))
    assert arranjo == pytest.approx(q.co2e_de_acessorios + q.co2e_de_conexoes)
    assert arranjo > 0
    categorias = {i.category for i in lca.inventory_items}
    for nome, *_ in itens_para_acv(q):
        assert f'Arranjo 3D: {nome}' in categorias


def test_o_valor_digitado_pelo_projetista_prevalece():
    cfg = TritonConfig()
    cfg.capex_do_arranjo = False
    cfg.cost_piping, cfg.cost_accessories = (999.0, 111.0)
    antes = list(cfg.pipes_list)
    run_economic_analysis(cfg, _simulacao())
    assert (cfg.cost_piping, cfg.cost_accessories, cfg.pipes_list) == (999.0, 111.0, antes)


def test_a_etap_nao_desconta_verba_que_o_arranjo_nao_tem():
    """A verba genérica de tratamento só existe nos acessórios estimados por percentual."""
    cfg = TritonConfig()
    cfg.cost_accessories = 3000.0
    cfg.capex_do_arranjo = False
    com_verba = capex_incremental_da_etap(cfg)
    cfg.capex_do_arranjo = True
    assert capex_incremental_da_etap(cfg) > com_verba


def test_o_arranjo_organizado_viaja_com_o_projeto(tmp_path):
    from triton.core.parser import export_triton_json, load_triton_project
    cfg = _projeto_novo()
    layout = generate_study_layout({'lower_vol': 8000, 'area': 200})
    layout['pipe_runs'] = layout['pipe_runs'][:5]
    cfg.bim_layout = layout
    caminho = tmp_path / 'p.triton'
    export_triton_json(cfg, str(caminho))
    relido = load_triton_project(str(caminho))['config']
    assert len(relido.bim_layout['pipe_runs']) == 5
    assert relido.capex_do_arranjo is True
    assert quantitativo_do_projeto(relido).tubos_m_por_dn == quantitativo_do_projeto(cfg).tubos_m_por_dn


def test_o_arquivo_antigo_mantem_os_custos_que_declara(tmp_path):
    """Sem a chave no arquivo, os custos gravados são os do estudo publicado."""
    import json
    from triton.core.parser import export_triton_json, load_triton_project
    cfg = TritonConfig()
    cfg.cost_piping, cfg.cost_accessories = (1200.0, 1800.0)
    caminho = tmp_path / 'antigo.triton'
    export_triton_json(cfg, str(caminho))
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    dados['inputs']['capex_and_opex'].pop('capex_do_arranjo')
    caminho.write_text(json.dumps(dados), encoding='utf-8')
    relido = load_triton_project(str(caminho))['config']
    assert relido.capex_do_arranjo is False
    run_economic_analysis(relido, _simulacao())
    assert (relido.cost_piping, relido.cost_accessories) == (1200.0, 1800.0)


def test_o_arranjo_usual_acompanha_o_volume_do_projeto():
    """Era 5.000 L para todo projeto: a configuração não tem ``lower_tank_vol``."""
    from triton.core.quantitativo_do_arranjo import arranjo_do_projeto
    pequeno, grande = (_projeto_novo(), _projeto_novo())
    pequeno.econ_lower_tank_vol, grande.econ_lower_tank_vol = (1500.0, 30000.0)
    cisterna = lambda cfg: next((c for c in arranjo_do_projeto(cfg)['bim_components'] if c['type_id'] == 'cisterna_inferior'))
    assert cisterna(pequeno)['parameters'] != cisterna(grande)['parameters']
    assert quantitativo_do_projeto(pequeno).tubos_m_por_dn != quantitativo_do_projeto(grande).tubos_m_por_dn
    fixo = _projeto_novo()
    fixo.lower_tank_mode, fixo.lower_tank_fixed, fixo.econ_lower_tank_vol = (0, 30000.0, 1500.0)
    assert cisterna(fixo)['parameters'] == cisterna(grande)['parameters']


def test_o_capex_e_o_desenho_levantam_o_mesmo_arranjo():
    """Com os dados que a prancha recebe, ou só com o projeto, o arranjo usual é um só."""
    from triton.core.quantitativo_do_arranjo import arranjo_do_projeto, dados_do_estudo
    cfg = _projeto_novo()
    cfg.econ_lower_tank_vol, cfg.area, cfg.upper_tank_vol = (8000.0, 220.0, 1000.0)
    relatorio = {'lower_vol': 8000.0, 'area': '-', 'discard': '-', 'upper_vol': 1000.0, 'pluv_day': 0.0}
    desenho = generate_study_layout(dados_do_estudo(cfg, relatorio))
    assert desenho == arranjo_do_projeto(cfg)
    assert quantitativo_do_projeto(cfg, None).tubos_m_por_dn == levantar(desenho).tubos_m_por_dn


def _tipos(layout):
    return [c['type_id'] for c in layout['bim_components']]


def _validado(dados):
    from triton.core.bim_exporter import build_bim_manifest, validate_bim_manifest
    layout = generate_study_layout(dados)
    manifesto = build_bim_manifest(dict(dados, project_name='t', **layout))
    assert validate_bim_manifest(manifesto) == []
    return (layout, {c['instance_id']: c for c in layout['bim_components']})


def test_a_reserva_e_desenhada_em_paralelo_com_as_suas_pecas():
    layout, por_id = _validado({'lower_vol': 5000, 'pump_count': 2})
    assert _tipos(layout).count('motobomba') == 2
    for peca in ('RG-06', 'VR-03', 'RG-07'):
        assert peca in por_id
    q = levantar(layout)
    assert {i.item for i in q.itens} >= {'Tês DN 25', 'Tês DN 32'}
    um = levantar(generate_study_layout({'lower_vol': 5000, 'pump_count': 1}))
    assert q.custo_de_acessorios > um.custo_de_acessorios
    assert q.custo_de_tubulacao > um.custo_de_tubulacao


def test_sem_caixa_o_backup_potavel_desce_na_propria_cisterna():
    for abastecimento in ('pressurizacao', 'gravidade'):
        layout, por_id = _validado({'lower_vol': 5000, 'supply_arrangement': abastecimento, 'pump_count': 2})
        assert 'reservatorio_superior' not in _tipos(layout)
        assert not {'SN-02', 'RP-02', 'RG-04'} & set(por_id)
        cisterna = por_id['CI-01']
        topo = cisterna['position_mm']['z'] + cisterna['parameters']['ALTURA_MM']
        assert por_id['AG-01']['position_mm']['z'] == pytest.approx(topo)
        assert 'SN-03' in por_id
        trecho = next((r for r in layout['pipe_runs'] if r['run_id'] == 'T-19'))
        assert trecho['end'] == 'AG-01:topo'


def test_pressurizacao_leva_o_recalque_direto_ao_ponto():
    layout, por_id = _validado({'lower_vol': 5000, 'supply_arrangement': 'pressurizacao', 'pump_count': 1})
    assert _tipos(layout).count('motobomba') == 1
    saida = next((r for r in layout['pipe_runs'] if r['start'] == 'RG-01'))
    assert saida['end'] == 'PNP-01:topo'


def test_gravidade_nao_tem_bomba_e_a_cisterna_fica_acima_do_ponto():
    layout, por_id = _validado({'lower_vol': 5000, 'supply_arrangement': 'gravidade', 'pump_count': 2})
    assert not {'motobomba', 'succao_flutuante', 'valvula_pe_crivo'} & set(_tipos(layout))
    assert por_id['CI-01']['position_mm']['z'] > por_id['PNP-01']['position_mm']['z']


def test_o_arranjo_usual_segue_o_abastecimento_e_as_bombas_do_projeto():
    from triton.core.quantitativo_do_arranjo import divergencias_com_o_projeto
    for abastecimento, caixa in (('recalque', 1), ('pressurizacao', 0), ('gravidade', 0)):
        cfg = _projeto_novo()
        cfg.supply_arrangement, cfg.upper_tank_used, cfg.pump_count = (abastecimento, caixa, 2)
        q = quantitativo_do_projeto(cfg)
        assert divergencias_com_o_projeto(cfg, q) == []
    cfg = _projeto_novo()
    cfg.pump_count = 2
    cfg.bim_layout = generate_study_layout({'lower_vol': 5000, 'pump_count': 1})
    assert divergencias_com_o_projeto(cfg, quantitativo_do_projeto(cfg))


def test_a_mao_de_obra_automatica_acompanha_os_materiais():
    from triton.core.cost_estimates import LABOR_PCT
    from triton.core.quantitativo_do_arranjo import capex_do_volume, materiais_do_projeto, sincronizar_com_o_arranjo
    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    cfg.cost_lower_tank, cfg.cost_upper_tank, cfg.pump_unit_cost = (6000.0, 500.0, 600.0)
    sincronizar_com_o_arranjo(cfg)
    assert cfg.cost_labor == pytest.approx(max(1400.0, LABOR_PCT * materiais_do_projeto(cfg)), abs=0.01)
    assert materiais_do_projeto(cfg) == pytest.approx(6000 + 500 + 600 * cfg.pump_count + cfg.cost_piping + cfg.cost_accessories)
    _, _, mao_pequena = capex_do_volume(cfg, 2000.0, 1500.0)
    _, _, mao_grande = capex_do_volume(cfg, 30000.0, 15000.0)
    assert mao_grande > mao_pequena


def test_a_mao_de_obra_digitada_prevalece():
    from triton.core.quantitativo_do_arranjo import capex_do_volume, sincronizar_com_o_arranjo
    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica, cfg.cost_labor = (False, 2222.0)
    sincronizar_com_o_arranjo(cfg)
    assert cfg.cost_labor == 2222.0
    assert capex_do_volume(cfg, 30000.0, 15000.0)[2] == 2222.0


def test_o_capex_do_motor_usa_a_mao_de_obra_automatica():
    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    cfg.cost_labor = 1.0
    res = run_economic_analysis(cfg, _simulacao())
    assert cfg.cost_labor >= 1400.0
    assert res is not None


def test_a_escolha_da_mao_de_obra_viaja_com_o_projeto(tmp_path):
    import json
    from triton.core.parser import export_triton_json, load_triton_project
    cfg = _projeto_novo()
    cfg.mao_de_obra_automatica = True
    caminho = tmp_path / 'p.triton'
    export_triton_json(cfg, str(caminho))
    assert load_triton_project(str(caminho))['config'].mao_de_obra_automatica is True
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    dados['inputs']['capex_and_opex'].pop('mao_de_obra_automatica')
    caminho.write_text(json.dumps(dados), encoding='utf-8')
    assert load_triton_project(str(caminho))['config'].mao_de_obra_automatica is False


# ---- origem: tests/unit/test_environmental_sync.py

def test_infer_tank_material_from_cost():
    assert infer_tank_material(5000, 2500) == 'PEAD'
    assert infer_tank_material(5000, 9000) == 'CONCRETO'
    assert infer_tank_material(3000, 7000) == 'ACO_INOX'


def test_material_preset_values_match_catalog():
    density, co2 = material_preset_values('PEAD')
    assert density == MATERIAL_PRESETS['PEAD'].material_density_kg_per_m3_tank
    assert co2 == MATERIAL_PRESETS['PEAD'].co2_factor_kg_per_kg


def test_compute_annual_pump_energy_from_simulation():
    config = TritonConfig()
    config.pump_power_kw = 0.7355
    config.pump_efficiency = 60.0
    config.pump_flow_rate = 3000.0
    config.pump_startup_time_h = 10.0 / 3600.0
    config.upper_tank_used = 1
    daily = [SimulationDayResult(day_index=d + 1, precip_mm=10.0, eff_precip_mm=10.0, harvested_liters=1000.0, total_demand_liters=1000.0, pluvial_demand_liters=1000.0, pluvial_consumed_liters=1000.0, potable_consumed_liters=0.0, spilled_liters=0.0, lower_tank_end_liters=1000.0, upper_tank_end_liters=500.0, pumped_liters=1000.0, pump_cycles=2, satisfaction_type=2) for d in range(365)]
    sim = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=80.0, avg_pluvial_consumed_l_day=1000.0, avg_potable_consumed_l_day=0.0, avg_spilled_l_day=0.0, pct_days_full_satisfaction=100.0, pct_days_partial_satisfaction=0.0, pct_days_null_satisfaction=0.0, total_pumped_liters=365000.0, total_pump_cycles=730, daily_results=daily)
    result = compute_annual_pump_energy(config, sim)
    assert result.annual_kwh > 0
    assert result.specific_kwh_per_m3 > 0
    assert result.annual_pumped_m3 == pytest.approx(365.0, rel=0.01)


def test_build_sync_snapshot_uses_simulation_pump_data():
    config = TritonConfig()
    config.pump_power_kw = 0.7355
    config.pump_efficiency = 60.0
    config.pump_flow_rate = 3000.0
    config.cost_lower_tank = 2800.0
    config.analysis_period_years = 25
    config.lower_tank_material = 'PEAD'
    config.upper_tank_material = 'FIBRA'
    sim = SingleTankSimulationResult(lower_tank_vol=5000.0, potential_potable_savings_pct=80.0, avg_pluvial_consumed_l_day=500.0, avg_potable_consumed_l_day=100.0, avg_spilled_l_day=50.0, pct_days_full_satisfaction=80.0, pct_days_partial_satisfaction=10.0, pct_days_null_satisfaction=10.0, total_pumped_liters=120000.0, total_pump_cycles=300, n_days_simulated=365)
    snap = build_sync_snapshot(config, sim, upper_used=True, upper_vol_l=500.0, lower_vol_l=5000.0, capture_area_m2=120.0)
    assert snap['lower_material_key'] == 'PEAD'
    assert snap['upper_material_key'] == 'FIBRA'
    assert snap['lifespan_years'] == 25
    assert snap['annual_pump_kwh'] > 0
    assert snap['specific_kwh_per_m3'] > 0
    assert snap['pipes_m'][100] > 0


def test_sync_never_changes_explicit_material_because_of_cost():
    config = TritonConfig()
    config.lower_tank_material = 'PEAD'
    config.upper_tank_material = 'FIBRA'
    config.cost_lower_tank = 25000.0
    config.cost_upper_tank = 5000.0
    snap = build_sync_snapshot(config, None, upper_used=True, upper_vol_l=500.0, lower_vol_l=5000.0, capture_area_m2=100.0)
    assert snap['lower_material_key'] == 'PEAD'
    assert snap['upper_material_key'] == 'FIBRA'


def test_lca_uses_annual_pump_kwh_when_provided():
    config = EnvironmentalConfig(lower_material_key='PEAD', upper_tank_used=False, annual_pump_kwh=150.0, pump_count=1, system_lifespan_years=20.0)
    res = calculate_lca(5000.0, 100.0, config)
    assert res.annual_pumping_co2_kg == pytest.approx(150.0 * config.grid_co2_factor_kg_kwh, rel=0.001)


def test_nearest_pump_cv_lookup():
    assert nearest_pump_cv(0.48) == 0.5
    assert nearest_pump_cv(1.2) == 1.0


def test_config_pipe_lengths_and_sync():
    cfg = TritonConfig()
    assert cfg.total_pipe_length() == 45.0
    cfg.set_pipe_length(50, 20.0)
    cfg.set_pipe_length(75, 10.0)
    cfg.set_pipe_length(100, 30.0)
    cfg.set_pipe_length(150, 5.0)
    assert cfg.get_pipe_length(50) == 20.0
    assert cfg.get_pipe_length(75) == 10.0
    assert cfg.get_pipe_length(100) == 30.0
    assert cfg.get_pipe_length(150) == 5.0
    assert cfg.total_pipe_length() == 90.0
    snap = build_sync_snapshot(cfg, None, upper_used=True, upper_vol_l=500.0, lower_vol_l=5000.0, capture_area_m2=100.0)
    assert snap['pipes_m'][50] == 20.0
    assert snap['pipes_m'][75] == 10.0
    assert snap['pipes_m'][100] == 30.0
    assert snap['pipes_m'][150] == 5.0


# ==================================================================================================
# Decisão: TOPSIS, SMAA e certificações
# ==================================================================================================

# ---- origem: tests/unit/test_mcdm_methods.py

@pytest.fixture
def sample_candidates():
    return [TopsisCandidate(lower_tank_vol=1000.0, water_saved_m3_yr=80.0, vpl_brl=3500.0, co2_saved_kg_lifetime=1200.0, capex_brl=4000.0, upper_tank_vol=500.0, technical_threshold_met=True, potential_savings_pct=40.0, overflow_m3_yr=120.0, discounted_payback_years=4.5, irr_pct=18.5, potable_consumed_m3_yr=120.0), TopsisCandidate(lower_tank_vol=3000.0, water_saved_m3_yr=140.0, vpl_brl=6200.0, co2_saved_kg_lifetime=2100.0, capex_brl=6500.0, upper_tank_vol=500.0, technical_threshold_met=True, potential_savings_pct=70.0, overflow_m3_yr=60.0, discounted_payback_years=5.2, irr_pct=16.0, potable_consumed_m3_yr=60.0), TopsisCandidate(lower_tank_vol=5000.0, water_saved_m3_yr=165.0, vpl_brl=5800.0, co2_saved_kg_lifetime=2500.0, capex_brl=8500.0, upper_tank_vol=500.0, technical_threshold_met=True, potential_savings_pct=82.5, overflow_m3_yr=35.0, discounted_payback_years=6.8, irr_pct=13.2, potable_consumed_m3_yr=35.0)]


def test_run_vikor(sample_candidates):
    res = run_vikor(sample_candidates, weights=(0.333, 0.333, 0.334), v_param=0.5)
    assert isinstance(res, VikorResult)
    assert len(res.q_scores) == len(sample_candidates)
    assert len(res.ranks) == len(sample_candidates)
    assert 0 <= res.best_index < len(sample_candidates)
    assert 1 in res.ranks


def test_run_smaa_vikor(sample_candidates):
    res = run_smaa_vikor(sample_candidates, v_param=0.75, num_samples=1000)
    assert isinstance(res, SmaaResult)
    assert res.engine == 'vikor'
    assert res.v_weight == 0.75
    assert len(res.first_rank_acceptabilities) == len(sample_candidates)
    assert np.isclose(np.sum(res.first_rank_acceptabilities), 1.0, atol=0.05)
    assert 0 <= res.best_index < len(sample_candidates)
    assert res.acceptability_matrix.shape == (3, 3)
    assert len(res.confidence_factors) == len(sample_candidates)
    assert res.num_samples == 1000
    assert res.num_simulations == 1000
    w_t, w_f, w_e = res.get_central_dimension_weights(res.best_index)
    assert np.isclose(w_t + w_f + w_e, 1.0, atol=0.01)
    assert 0.0 <= w_t <= 1.0
    assert 0.0 <= w_f <= 1.0
    assert 0.0 <= w_e <= 1.0


def test_run_smaa_analysis(sample_candidates):
    res = run_smaa_analysis(sample_candidates, num_samples=1000, engine='vikor')
    assert isinstance(res, SmaaResult)
    assert res.engine == 'vikor'
    assert len(res.first_rank_acceptabilities) == len(sample_candidates)
    assert np.isclose(np.sum(res.first_rank_acceptabilities), 1.0, atol=0.05)
    assert 0 <= res.best_index < len(sample_candidates)
    assert res.acceptability_matrix.shape == (3, 3)
    res_topsis = run_smaa_analysis(sample_candidates, num_samples=1000, engine='topsis')
    assert res_topsis.engine == 'topsis'
    assert len(res_topsis.first_rank_acceptabilities) == len(sample_candidates)


@pytest.mark.parametrize('num_samples', [0, -1, 1.5])
def test_smaa_rejects_invalid_number_of_simulations(sample_candidates, num_samples):
    with pytest.raises(ValueError, match='inteiro positivo'):
        run_smaa_vikor(sample_candidates, num_samples=num_samples)


# ---- origem: tests/unit/test_certificacao_edge.py

def _avaliar(pluvial, demanda=250.0, area=180.0, base=None):
    return avaliar_agua_edge(volume_pluvial_anual_m3=pluvial, demanda_total_anual_m3=demanda, area_de_captacao_m2=area, consumo_base_anual_m3_declarado=base)


def test_o_limiar_das_tres_barras_e_vinte_por_cento():
    assert LIMIAR_DE_AGUA_PCT == 20.0


def test_o_nivel_avancado_pede_quarenta_por_cento_de_energia():
    """EDGE Advanced acrescenta energia, e não água: a barra de água segue em 20%."""
    assert LIMIAR_DE_ENERGIA_AVANCADO_PCT == 40.0
    assert LIMIAR_DE_ENERGIA_AVANCADO_PCT > LIMIAR_DE_AGUA_PCT


@pytest.mark.parametrize(('pct', 'atende'), [(19.9, False), (20.0, True), (20.1, True)])
def test_a_fronteira_dos_vinte_por_cento_e_inclusiva(pct, atende):
    r = _avaliar(pluvial=250.0 * pct / 100.0, demanda=250.0)
    assert r.atende_o_padrao_de_agua is atende


def test_a_margem_diz_quanto_sobra_ou_falta():
    assert _avaliar(75.0).margem_pct == pytest.approx(10.0)
    assert _avaliar(25.0).margem_pct == pytest.approx(-10.0)


def test_sem_caso_base_declarado_usa_a_demanda_do_projeto_e_avisa():
    r = _avaliar(pluvial=100.0, demanda=400.0)
    assert r.consumo_base_anual_m3 == pytest.approx(400.0)
    assert r.base_declarada_pelo_usuario is False
    assert 'piso' in r.ressalva


def test_caso_base_declarado_maior_reduz_o_percentual():
    """Com louças e metais eficientes, o caso-base do EDGE é maior que a demanda.

    O mesmo volume de chuva vale um percentual menor da barra, embora a barra
    total do projeto seja maior. É por isso que o número sem caso-base é piso.
    """
    sem = _avaliar(pluvial=100.0, demanda=400.0)
    com = _avaliar(pluvial=100.0, demanda=400.0, base=600.0)
    assert com.economia_de_agua_pct < sem.economia_de_agua_pct
    assert com.base_declarada_pelo_usuario is True


def test_o_caso_base_converte_de_litros_por_pessoa_dia():
    assert consumo_base_anual_m3(150.0, 4) == pytest.approx(219.0)


def test_caso_base_zero_ou_negativo_nao_e_aceito_como_declarado():
    r = _avaliar(pluvial=50.0, demanda=250.0, base=0.0)
    assert r.base_declarada_pelo_usuario is False
    assert r.consumo_base_anual_m3 == pytest.approx(250.0)


def test_demanda_nula_nao_divide_por_zero():
    r = _avaliar(pluvial=50.0, demanda=0.0)
    assert r.economia_de_agua_pct == 0.0
    assert r.atende_o_padrao_de_agua is False


def test_o_percentual_nunca_passa_de_cem():
    assert _avaliar(pluvial=900.0, demanda=250.0).economia_de_agua_pct == 100.0


def test_a_wem14_e_a_medida_que_este_programa_dimensiona():
    wem14 = [m for m in MEDIDAS_DE_AGUA if m.codigo == 'WEM14']
    assert len(wem14) == 1
    assert wem14[0].modelada_pelo_triton is True
    assert 'pluvial' in wem14[0].nome.lower()


def test_as_medidas_fora_do_escopo_estao_declaradas_como_tal():
    """Honestidade sobre o que não se modela vale mais que cobertura aparente."""
    fora = [m for m in MEDIDAS_DE_AGUA if not m.modelada_pelo_triton]
    assert {m.codigo for m in fora} == {'WEM13', 'WEM15'}
    for m in fora:
        assert m.observacao


def _esg(area=180.0, pluvial=95.0, potavel=155.0):
    return calculate_esg_certifications(potable_savings_pct=pluvial / (pluvial + potavel) * 100.0, annual_pluvial_consumed_m3=pluvial, annual_potable_consumed_m3=potavel, net_co2e_saved_kg_lifetime=1200.0, catchment_area_m2=area)


def test_a_area_de_captacao_atravessa_ate_a_matriz():
    """Era o percurso em risco: sem ela, o campo da WEM14 sairia zerado."""
    linha = [c for c in _esg(area=240.0).credit_details if c.credit_code == 'WEM14']
    assert len(linha) == 1
    assert '240' in linha[0].notes


def test_mais_chuva_aproveitada_move_a_barra_de_agua():
    """Se a barra não se mexesse com a simulação, seria enfeite."""
    pouco = _esg(pluvial=30.0, potavel=220.0).edge.economia_de_agua_pct
    muito = _esg(pluvial=120.0, potavel=130.0).edge.economia_de_agua_pct
    assert muito > pouco


def test_o_edge_e_independente_da_pontuacao_leed():
    """São réguas diferentes: uma mede percentual, a outra soma pontos."""
    r = _esg(pluvial=60.0, potavel=190.0)
    assert r.edge.atende_o_padrao_de_agua is True
    assert r.leed.total_leed_we_points >= 0


def test_o_caso_base_e_um_campo_do_projeto_e_volta_ao_reabrir(tmp_path):
    """Parâmetro sem onde ser informado é o defeito que esta rodada corrigiu."""
    from triton.core.parser import TritonConfig, export_triton_json, load_triton_project
    cfg = TritonConfig()
    assert hasattr(cfg, 'edge_base_case_l_person_day')
    cfg.edge_base_case_l_person_day = 165.0
    caminho = str(tmp_path / 'projeto.triton')
    export_triton_json(cfg, caminho)
    pacote = load_triton_project(caminho)
    lido = pacote['config'] if isinstance(pacote, dict) else pacote
    assert lido.edge_base_case_l_person_day == pytest.approx(165.0)


def test_o_campo_da_tela_chega_ao_calculo(qapp):
    """Percurso tela → cálculo: o campo converte L/pessoa·dia em m³/ano."""
    pytest.importorskip('PySide6')
    from triton.core.parser import TritonConfig
    from triton.ui.tab_environmental import TabEnvironmental
    aba = TabEnvironmental()
    assert aba._edge_base_case_annual_m3() is None
    aba.txt_edge_base.setText('150')
    janela = aba.window()
    janela.config = TritonConfig()
    janela.config.residents_count = 4
    janela.config.num_economias = 1
    assert aba._edge_base_case_annual_m3() == pytest.approx(219.0)


def test_valor_ilegivel_no_campo_nao_derruba_a_tela(qapp):
    pytest.importorskip('PySide6')
    from triton.ui.tab_environmental import TabEnvironmental
    aba = TabEnvironmental()
    for texto in ('abc', '-5', '0'):
        aba.txt_edge_base.setText(texto)
        assert aba._edge_base_case_annual_m3() is None


def test_o_caso_base_percorre_os_dois_sentidos(qapp):
    """Tela → projeto → arquivo → projeto → tela.

    O extrator de ligações desta rodada pegou o campo recém-criado como
    «gravado e nunca lido»: a tela lia a própria caixa de texto e nunca tocava
    a configuração. Gravado no arquivo, o valor não voltava para a tela.
    """
    pytest.importorskip('PySide6')
    from triton.core.parser import TritonConfig
    from triton.ui.tab_environmental import TabEnvironmental
    aba = TabEnvironmental()
    janela = aba.window()
    janela.config = TritonConfig()
    janela.config.residents_count = 4
    aba.txt_edge_base.setText('172')
    aba._edge_base_case_annual_m3()
    assert janela.config.edge_base_case_l_person_day == pytest.approx(172.0)
    outra = TabEnvironmental()
    outra.window().config = janela.config
    outra.sync_from_project(force=True)
    assert outra.txt_edge_base.text().strip() != ''


# ---- origem: tests/integration/test_exemplo_quatro_criterios.py
_ARQUIVO_EXEMPLO_QUATRO_CRITERIOS = str(_TESTES / 'integration/test_exemplo_quatro_criterios.py')

EXEMPLO = Path(_ARQUIVO_EXEMPLO_QUATRO_CRITERIOS).resolve().parents[2] / 'examples' / 'exemplo_quatro_criterios.triton'


@pytest.fixture(scope='module')
def saida():
    b = cli._load_bundle(str(EXEMPLO))
    an = b.get('analysis') or {}
    return cli.run_analysis(b['config'], cli._get_precipitation(b), 'all', environmental=an.get('environmental'))


def test_fracoes_do_exemplo():
    c = cli._load_bundle(str(EXEMPLO))['config']
    assert c.non_potable_indoor_share == pytest.approx(0.35)
    assert c.irrigation_liters_per_day == pytest.approx(90.0)
    assert c.rainwater_share == pytest.approx(200.0 / 460.0, abs=1e-06)


def test_quatro_otimos_distintos(saida):
    t = saida['topsis']
    otimos = (t['technical_best_volume_l'], t['economic_best_volume_l'], t['environmental_best_volume_l'], t['best_volume_l'])
    assert otimos == (6000.0, 5000.0, 3000.0, 7000.0)
    assert len(set(otimos)) == 4


# ==================================================================================================
# Arquivo, linha de comando e paridade com a interface
# ==================================================================================================

# ---- origem: tests/unit/test_parser.py
_ARQUIVO_PARSER = str(_TESTES / 'unit/test_parser.py')

PARSER_WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_PARSER))))


def test_project_filename_contains_name_date_and_stable_hash():
    from triton import get_project_filename
    stamp = datetime(2026, 9, 1, 18, 30, 45)
    filename = get_project_filename('Edifício Águas do Sul', 'N5-20260901-ABCDEF12', now=stamp)
    assert filename.startswith('triton-projeto-edificio-aguas-do-sul-2026-09-01-183045-')
    assert filename.endswith('.triton')
    assert filename == get_project_filename('Edifício Águas do Sul', 'N5-20260901-ABCDEF12', now=stamp)


def test_parse_float_and_int():
    assert parse_float('12,34') == 12.34
    assert parse_float(' 100.5 ') == 100.5
    assert parse_float('', 1.0) == 1.0
    assert parse_float(None, 0.5) == 0.5
    assert parse_float(0, 5.0) == 0.0
    assert parse_int(' 10 ') == 10
    assert parse_int('12,34') == 12
    assert parse_int('', 3) == 3
    assert parse_int(0, 5) == 0


def test_load_precipitation_file():
    path = os.path.join(PARSER_WORKSPACE_DIR, 'data', 'rainfall', 'Florianopolis2.csv')
    arr = load_precipitation(path)
    assert isinstance(arr, np.ndarray)
    assert len(arr) == 31411


def test_parse_triton_project_csv():
    """A configuracao de uma exportacao do Netuno 4 vem do NOME do arquivo.

    O Netuno 4 grava so a tabela de varredura: volume contra resultado, sem
    parametro nenhum no corpo. Toda a configuracao fica no nome, por convencao.

    Este parser ja ignorou o nome e devolvia a configuracao
    padrao inteira. O retorno parecia leitura bem-sucedida, e este teste fixava
    exatamente esses padroes - area 100 e residentes 4 batiam por coincidencia,
    e os outros cinco estavam simplesmente errados. Quem montasse uma comparacao
    com o Netuno 4 a partir dele rodava com descarte de 1 mm onde o arquivo diz
    2 mm, e com 40% de fracao pluvial onde o arquivo diz 90%.
    """
    nome = 'Florianopolis2_Descarte2_Area100_Consumo100_Pessoas4_Percentual90_Coefs08_Recalque20_5000_500_2.csv'
    path = os.path.join(PARSER_WORKSPACE_DIR, 'data', 'simulation_outputs', nome)
    cfg = parse_netuno_csv(path)
    assert cfg.discard == 2.0
    assert cfg.area == 100.0
    assert cfg.demand_value == 100.0
    assert cfg.residents_count == 4
    assert cfg.rainwater_share == 0.9
    assert cfg.runoff_coeff == 0.8
    assert cfg.pumping_threshold == 20.0


def test_parametros_do_nome_devolvem_so_o_que_encontram():
    """Distingue «nao estava no nome» de «era igual ao padrao».

    E essa distincao que faltava: uma configuracao devolvida por inteiro nao
    permitia saber o que fora lido e o que fora presumido.
    """
    from triton.core.parser import parametros_do_nome_do_arquivo
    completo = parametros_do_nome_do_arquivo('Manaus1_Descarte2_Area200_Consumo150_Pessoas5_Percentual40_Coefs09_Recalque0.csv')
    assert completo['discard'] == 2.0
    assert completo['area'] == 200.0
    assert completo['runoff_coeff'] == 0.9
    assert completo['rainwater_share'] == 0.4
    vazio = parametros_do_nome_do_arquivo('arquivo_qualquer.csv')
    assert vazio == {}


def test_coeficiente_do_nome_nunca_passa_de_um():
    """«Coefs08» e 0,80 e «Coefs095» e 0,95, nunca 8 nem 95.

    Um coeficiente de escoamento acima de 1 significaria captar mais agua do que
    a que cai no telhado.
    """
    from triton.core.parser import parametros_do_nome_do_arquivo
    for sufixo, esperado in (('Coefs08', 0.8), ('Coefs09', 0.9), ('Coefs095', 0.95)):
        lido = parametros_do_nome_do_arquivo(f'Serie_{sufixo}_Area100.csv')
        assert lido['runoff_coeff'] == pytest.approx(esperado)
        assert 0.0 < lido['runoff_coeff'] <= 1.0


def test_export_netuno4_csv_roundtrip(tmp_path):
    from triton.core.parser import TritonConfig, export_netuno_csv, parse_netuno_csv
    from triton.core.simulation import SingleTankSimulationResult
    cfg = TritonConfig(area=120.0, demand_value=150.0, residents_count=4, rainwater_share=0.5, runoff_coeff=0.85, discard=2.0, lower_tank_fixed=3000.0, lower_tank_mode=0)
    results = [SingleTankSimulationResult(lower_tank_vol=3000.0, potential_potable_savings_pct=42.5, avg_pluvial_consumed_l_day=120.0, avg_potable_consumed_l_day=480.0, avg_spilled_l_day=50.0, pct_days_full_satisfaction=80.0, pct_days_partial_satisfaction=10.0, pct_days_null_satisfaction=10.0)]
    out_file = str(tmp_path / 'test_out_netuno4.csv')
    export_netuno_csv(cfg, results, out_file)
    assert os.path.exists(out_file)
    reparsed_cfg = parse_netuno_csv(out_file)
    assert reparsed_cfg.area == 120.0
    assert reparsed_cfg.demand_value == 150.0
    assert reparsed_cfg.residents_count == 4
    assert reparsed_cfg.rainwater_share == 0.5
    assert reparsed_cfg.runoff_coeff == 0.85
    assert reparsed_cfg.discard == 2.0


def test_export_and_load_triton_json_project(tmp_path):
    from triton.core.parser import TritonConfig, export_triton_json, load_triton_project
    cfg = TritonConfig(project_name='Residencial Horizonte', area=150.0, demand_value=120.0, residents_count=5, rainwater_share=0.45, runoff_coeff=0.88, discard=1.5)
    precip_data = np.array([0.0, 10.5, 25.0, 0.0, 5.2], dtype=np.float64)
    building_data = {'area': 150.0, 'demand': 120.0, 'residents': 5, 'share': 0.45, 'runoff': 0.88, 'discard': 1.5}
    scenarios = [{'name': 'Option 1', 'lower_vol': 2000.0, 'upper_vol': 500.0}, {'name': 'Option 2', 'lower_vol': 3500.0, 'upper_vol': 500.0}]
    out_file = str(tmp_path / 'meu_projeto.triton')
    export_triton_json(cfg, out_file, precip_data=precip_data, building_data=building_data, global_scenarios=scenarios)
    assert os.path.exists(out_file)
    proj = load_triton_project(out_file)
    assert proj['is_json'] is True
    assert proj['config'].project_name == 'Residencial Horizonte'
    assert proj['precip_data'] is not None
    assert len(proj['precip_data']) == 5
    assert proj['building_data']['area'] == 150.0
    assert proj['building_data']['demand'] == 120.0
    assert proj['building_data']['residents'] == 5
    assert len(proj['global_scenarios']) == 2
    assert proj['global_scenarios'][1]['name'] == 'Option 2'


# ---- origem: tests/unit/test_cli.py

def test_cli_full_analysis_supports_seasonality_and_json_output():
    cfg = TritonConfig(area=100.0, demand_value=100.0, residents_count=3, demand_monthly=[100.0] * 12, residents_monthly=[3] * 12, rainwater_share=0.4, runoff_coeff=0.9, lower_tank_mode=1, lower_tank_max=1000.0, lower_tank_step=500.0, analysis_period_years=20)
    rainfall = np.array([8.0] * 60, dtype=float)
    assert _validate_config(cfg, rainfall) == []
    report = run_analysis(cfg, rainfall, 'all', source='test', weight_sensitivity=8, seed=7)
    assert len(report['technical']['alternatives']) == 3
    assert 'economic' in report and 'environmental' in report and ('topsis' in report)
    assert report['topsis']['best_volume_l'] in {0.0, 500.0, 1000.0}
    assert len(report['topsis']['criteria']) == 7
    assert set(report['topsis']['ranking'][0]['criterion_values']) == {'technical_potential_pct', 'technical_overflow_m3_yr', 'economic_npv_brl', 'economic_discounted_payback_years', 'economic_irr_pct', 'environmental_lifecycle_co2_kg', 'environmental_potable_water_m3_yr'}
    assert report['topsis']['weight_sensitivity']['samples'] == 8
    json.dumps(report, default=_json_default)


def test_cli_validation_rejects_incomplete_monthly_seasonality():
    cfg = TritonConfig(demand_monthly=[100.0] * 11, residents_monthly=[3] * 12)
    errors = _validate_config(cfg, np.array([1.0], dtype=float))
    assert any(('demand_monthly' in error for error in errors))


def test_cli_reports_requested_and_effective_sweep_grid():
    cfg = TritonConfig(area=100.0, demand_value=100.0, residents_count=3, rainwater_share=0.4, runoff_coeff=0.9, lower_tank_mode=1, lower_tank_max=10001.0, lower_tank_step=250.0)
    report = run_analysis(cfg, np.array([0.0, 8.0], dtype=float), 'technical', source='test-grid')
    grid = report['technical']['summary']['sweep_grid']
    assert grid['requested_step_l'] == 250.0
    assert grid['effective_step_l'] == 500.0
    assert grid['step_adjusted'] is True
    assert grid['positive_volume_count'] == 21
    assert report['technical']['alternatives'][-1]['lower_tank_volume_l'] == 10001.0


def _project_matrix_args(project, output_dir, rainfall_dir=None, ignore_project_factors=False):
    return Namespace(projects=[str(project)], rainfall_dir=str(rainfall_dir) if rainfall_dir else None, recursive=False, ignore_project_factors=ignore_project_factors, analysis='technical', weights=None, weight_sensitivity=0, seed=42, output_dir=str(output_dir), quiet=True)


def test_cli_project_matrix_expands_factorial_block_and_rainfall_folder(tmp_path):
    cfg = TritonConfig(area=100.0, demand_value=100.0, residents_count=3, rainwater_share=0.4, runoff_coeff=0.9, lower_tank_mode=1, lower_tank_max=1000.0, lower_tank_step=1000.0)
    project = tmp_path / 'modelo.triton'
    export_triton_json(cfg, str(project), precip_data=np.array([8.0] * 30, dtype=float), analysis={})
    raw = json.loads(project.read_text(encoding='utf-8'))
    raw['cli_factorial'] = {'factors': {'area': [80.0, 120.0], 'residents_count': [2, 4]}, 'rainfall_files': []}
    project.write_text(json.dumps(raw, ensure_ascii=False), encoding='utf-8')
    factorial_output = tmp_path / 'factorial'
    _run_project_matrix(_project_matrix_args(project, factorial_output))
    with (factorial_output / 'triton-matriz-detalhado.json').open(encoding='utf-8') as stream:
        factorial = json.load(stream)
    assert len(factorial['reports']) == 4
    rainfall_dir = tmp_path / 'climas'
    rainfall_dir.mkdir()
    (rainfall_dir / 'cidade_a.csv').write_text('5\n0\n12\n', encoding='utf-8')
    (rainfall_dir / 'cidade_b.csv').write_text('0\n8\n2\n', encoding='utf-8')
    folder_output = tmp_path / 'folder'
    _run_project_matrix(_project_matrix_args(project, folder_output, rainfall_dir, ignore_project_factors=True))
    with (folder_output / 'triton-matriz-detalhado.json').open(encoding='utf-8') as stream:
        folder = json.load(stream)
    assert len(folder['reports']) == 2
    assert {item['rainfall_name'] for item in folder['reports']} == {'cidade_a', 'cidade_b'}


# ---- origem: tests/unit/test_persistencia_do_projeto.py

NAO_PERSISTIDOS = {'created_at', 'precip_file'}


BANDEIRAS_NUMERICAS = {'upper_tank_used'}


def _marcar(valor):
    """Devolve um valor distinto do padrão, do mesmo tipo."""
    if isinstance(valor, bool):
        return not valor
    if isinstance(valor, int):
        return int(valor) + 7
    if isinstance(valor, float):
        return round(float(valor) * 1.37 + 3.1, 4)
    if isinstance(valor, str) and valor:
        return valor + '_X'
    return None


@pytest.fixture(scope='module')
def ciclo():
    """Marca todos os campos, grava, relê e devolve (marcas, configuração lida)."""
    cfg = TritonConfig()
    marcas = {}
    for nome in sorted(vars(cfg)):
        if nome in NAO_PERSISTIDOS:
            continue
        novo = _marcar(getattr(cfg, nome))
        if novo is None:
            continue
        marcas[nome] = novo
        setattr(cfg, nome, novo)
    from triton.core.fracao_atendivel import fracao_total
    coerentes = {'non_potable_indoor_share': 0.3, 'potable_indoor_share': 0.7, 'irrigation_liters_per_day': 150.0}
    coerentes['rainwater_share'] = fracao_total(cfg.demand_value * cfg.residents_count, 0.3, 150.0)
    for nome, valor in coerentes.items():
        marcas[nome] = valor
        setattr(cfg, nome, valor)
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, 'projeto.triton')
        export_triton_json(cfg, caminho)
        pacote = load_triton_project(caminho)
    lido = pacote['config'] if isinstance(pacote, dict) else pacote
    return (marcas, lido)


def test_o_ciclo_cobre_praticamente_toda_a_configuracao():
    """Se o teste cobrir poucos campos, ele não prova nada."""
    cfg = TritonConfig()
    total = sum((1 for n in vars(cfg) if _marcar(getattr(cfg, n)) is not None))
    assert total >= 80, total


def test_todo_parametro_sobrevive_a_salvar_e_reabrir(ciclo):
    """A verificação central. Trinta campos falhavam aqui.

    Acrescentar um campo a `TritonConfig` e esquecer de gravá-lo derruba este
    teste, que é exatamente o que se quer: o esquecimento é silencioso, a falha
    não pode ser.
    """
    marcas, lido = ciclo
    perdidos = []
    for nome, esperado in sorted(marcas.items()):
        if nome in BANDEIRAS_NUMERICAS:
            continue
        obtido = getattr(lido, nome, '<AUSENTE>')
        if isinstance(esperado, float) and isinstance(obtido, (int, float)):
            if abs(esperado - float(obtido)) < 1e-06:
                continue
        elif obtido == esperado:
            continue
        perdidos.append(f'{nome}: gravou {esperado!r}, voltou {obtido!r}')
    assert not perdidos, perdidos


@pytest.mark.parametrize('campo', ['water_quality_target_class', 'water_quality_disinfection', 'water_quality_polishing', 'etap_enabled', 'chlorine_treatment_enabled', 'chlorine_dose_mg_l', 'chlorine_product_purity', 'chlorine_cost_per_kg', 'chlorine_co2_kg_per_kg'])
def test_a_linha_de_tratamento_sobrevive(ciclo, campo):
    """Escolher ozônio e reabrir com cloração invalida o estudo inteiro."""
    marcas, lido = ciclo
    assert getattr(lido, campo) == marcas[campo]


@pytest.mark.parametrize('campo', ['building_template_id', 'lower_tank_material', 'upper_tank_material'])
def test_a_tipologia_e_os_materiais_sobrevivem(ciclo, campo):
    """Os materiais regem o carbono incorporado; a tipologia rege a demanda."""
    marcas, lido = ciclo
    assert getattr(lido, campo) == marcas[campo]


def test_a_altura_manometrica_do_assistente_sobrevive(ciclo):
    """É o resultado do assistente de motobomba, e governa a energia de recalque.

    Perdê-la ao reabrir devolvia o projeto ao valor de recurso, e a emissão de
    bombeamento voltava a ignorar o desnível informado.
    """
    marcas, lido = ciclo
    assert lido.pump_manometric_head_m == pytest.approx(marcas['pump_manometric_head_m'])


@pytest.mark.parametrize('campo', ['irrigation_garden_area_m2', 'irrigation_rate_l_m2_day', 'irrigation_liters_per_day', 'irrigation_rain_threshold_mm', 'irrigation_potable_backup'])
def test_a_irrigacao_sobrevive(ciclo, campo):
    marcas, lido = ciclo
    esperado, obtido = (marcas[campo], getattr(lido, campo))
    if isinstance(esperado, float):
        assert obtido == pytest.approx(esperado)
    else:
        assert obtido == esperado


@pytest.mark.parametrize('campo', ['iptu_green_enabled', 'iptu_annual_value', 'iptu_discount_pct', 'tariff_flag', 'num_economias', 'potable_indoor_share', 'non_potable_indoor_share'])
def test_os_tributos_e_as_fracoes_sobrevivem(ciclo, campo):
    marcas, lido = ciclo
    esperado, obtido = (marcas[campo], getattr(lido, campo))
    if isinstance(esperado, float):
        assert obtido == pytest.approx(esperado)
    else:
        assert obtido == esperado


def test_um_arquivo_sem_as_secoes_novas_continua_legivel():
    """Projetos gravados antes desta revisão não têm as quatro seções acrescentadas.

    Eles têm de continuar abrindo, com os campos ausentes caindo no padrão —
    que é o comportamento que já tinham.
    """
    import json
    cfg = TritonConfig()
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, 'antigo.triton')
        export_triton_json(cfg, caminho)
        dados = json.loads(open(caminho, encoding='utf-8').read())
        for secao in ('water_quality_and_etap', 'materials_and_typology', 'irrigation', 'incentives_and_shares'):
            dados['inputs'].pop(secao, None)
        open(caminho, 'w', encoding='utf-8').write(json.dumps(dados, ensure_ascii=False))
        pacote = load_triton_project(caminho)
    lido = pacote['config'] if isinstance(pacote, dict) else pacote
    assert lido.water_quality_disinfection == 'cloro'
    assert lido.lower_tank_material == 'PEAD'
    assert lido.iptu_green_enabled is False


def test_o_estudo_reaberto_produz_o_mesmo_resultado():
    """A prova final: mesmos parâmetros, mesmos números.

    Preservar os campos só vale se o resultado voltar igual. Um campo lido no
    lugar errado passaria no teste de igualdade e falharia aqui.

    Usa valores plausíveis, e não os marcadores sintéticos: a pureza do cloro
    tem guarda de faixa em (0, 1], e o marcador a estouraria — o que está certo,
    e é verificado em `test_chlorination.py`.
    """
    from triton.core.etap_integration import capex_incremental_da_etap
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    antes = TritonConfig()
    antes.water_quality_target_class = 'classe_4'
    antes.water_quality_disinfection = 'ozonio'
    antes.water_quality_polishing = True
    antes.chlorine_dose_mg_l = 2.5
    antes.chlorine_product_purity = 0.325
    antes.chlorine_cost_per_kg = 38.0
    antes.lower_tank_material = 'CONCRETO'
    antes.pump_manometric_head_m = 30.0
    antes.area = 250.0
    antes.cost_accessories = 800.0
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, 'estudo.triton')
        export_triton_json(antes, caminho)
        pacote = load_triton_project(caminho)
    depois = pacote['config'] if isinstance(pacote, dict) else pacote
    assert capex_incremental_da_etap(antes) == pytest.approx(capex_incremental_da_etap(depois))
    assert capex_incremental_da_etap(depois) > 0.0

    def _acv(cfg):
        return calculate_lca(5000.0, 120.0, EnvironmentalConfig(annual_water_saved_m3=120.0, lower_material_key=cfg.lower_tank_material, water_quality_target_class=cfg.water_quality_target_class, water_quality_disinfection=cfg.water_quality_disinfection, water_quality_polishing=cfg.water_quality_polishing, chlorine_dose_mg_l=cfg.chlorine_dose_mg_l, chlorine_product_purity=cfg.chlorine_product_purity))
    a, b = (_acv(antes), _acv(depois))
    assert a.total_embodied_co2_kg == pytest.approx(b.total_embodied_co2_kg)
    assert a.annual_treatment_co2_kg == pytest.approx(b.annual_treatment_co2_kg)


# ---- origem: tests/unit/test_projeto_sobrevive_ao_arquivo.py
_ARQUIVO_PROJETO_SOBREVIVE_AO_ARQUIVO = str(_TESTES / 'unit/test_projeto_sobrevive_ao_arquivo.py')

PROJETO_SOBREVIVE_AO_ARQUIVO_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_PROJETO_SOBREVIVE_AO_ARQUIVO))))


CASOS = os.path.join(PROJETO_SOBREVIVE_AO_ARQUIVO_RAIZ, 'manual', 'casos')


@pytest.fixture()
def pasta():
    with tempfile.TemporaryDirectory() as d:
        yield d


def _projeto_sobrevive_ao_arquivo_chuva():
    return np.full(140, 10.0, dtype=float)


def test_a_modulacao_semanal_sobrevive_ao_arquivo(pasta):
    cfg = TritonConfig()
    cfg.demand_mode = 'weekly'
    cfg.weekly_demands = [40.0] * 5 + [20.0, 5.0]
    cfg.weekly_residents = [300] * 5 + [150, 20]
    cfg.weekly_shares = [0.7] * 5 + [0.85, 1.0]
    caminho = os.path.join(pasta, 'p.triton')
    export_triton_json(cfg, caminho, precip_data=_projeto_sobrevive_ao_arquivo_chuva())
    lido = load_triton_project(caminho)['config']
    assert lido.demand_mode == 'weekly'
    assert lido.weekly_demands == cfg.weekly_demands
    assert lido.weekly_residents == cfg.weekly_residents
    assert lido.weekly_shares == cfg.weekly_shares


def test_a_modulacao_mensal_e_a_diaria_sobrevivem(pasta):
    cfg = TritonConfig()
    cfg.demand_mode = 'monthly'
    cfg.demand_monthly = [200.0] * 12
    cfg.residents_monthly = list(range(1, 13))
    cfg.monthly_shares = [0.45] * 12
    cfg.daily_demands = [100.0, 120.0, 90.0]
    cfg.daily_residents = [2, 3, 2]
    cfg.daily_shares = [0.4, 0.5, 0.4]
    caminho = os.path.join(pasta, 'p.triton')
    export_triton_json(cfg, caminho, precip_data=_projeto_sobrevive_ao_arquivo_chuva())
    lido = load_triton_project(caminho)['config']
    assert lido.monthly_shares == cfg.monthly_shares
    assert lido.residents_monthly == cfg.residents_monthly
    assert lido.daily_demands == cfg.daily_demands
    assert lido.daily_shares == cfg.daily_shares


def test_a_modulacao_muda_o_resultado_depois_de_reabrir(pasta):
    """O teste que importa: não basta o campo voltar, o cálculo tem de usá-lo.

    Sem isto, as listas poderiam voltar do arquivo e continuar inertes — que é
    exatamente o que acontecia com as duas listas mensais, gravadas desde sempre
    e ignoradas na releitura porque o modo lido dizia «constant».
    """
    chuva = _projeto_sobrevive_ao_arquivo_chuva()
    cfg = TritonConfig()
    cfg.area = 1000.0
    cfg.residents_count = 100
    cfg.demand_value = 40.0
    cfg.rainwater_share = 0.7
    cfg.demand_mode = 'weekly'
    cfg.weekly_demands = [40.0] * 5 + [2.0, 2.0]
    cfg.weekly_residents = [100] * 5 + [5, 5]
    cfg.weekly_shares = [0.7] * 7
    caminho = os.path.join(pasta, 'p.triton')
    export_triton_json(cfg, caminho, precip_data=chuva)
    lido = load_triton_project(caminho)['config']
    comum = dict(precip_data=chuva, lower_tank_vol=5000.0, area=lido.area, runoff_coeff=lido.runoff_coeff, discard_mm=lido.discard, rainwater_share=lido.rainwater_share)
    constante = run_single_simulation(total_demand_per_day=4000.0, **comum)
    modulado = run_single_simulation(total_demand_per_day=4000.0, demand_mode=lido.demand_mode, weekly_demands=lido.weekly_demands, weekly_residents=lido.weekly_residents, weekly_shares=lido.weekly_shares, **comum)
    assert modulado.avg_pluvial_consumed_l_day != pytest.approx(constante.avg_pluvial_consumed_l_day, rel=0.01), 'a modulação voltou do arquivo e não mudou nada: está inerte'


def test_json_sem_as_secoes_do_projeto_e_recusado(pasta):
    caminho = os.path.join(pasta, 'outro.triton')
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump({'format_version': '5.0', 'area': 180.0, 'residents': 4}, f)
    with pytest.raises(FormatoDeProjetoDesconhecido) as erro:
        load_triton_project(caminho)
    assert 'outro.triton' in str(erro.value)


def test_projeto_do_esquema_corrente_continua_abrindo(pasta):
    cfg = TritonConfig()
    cfg.area = 180.0
    caminho = os.path.join(pasta, 'bom.triton')
    export_triton_json(cfg, caminho, precip_data=_projeto_sobrevive_ao_arquivo_chuva())
    assert load_triton_project(caminho)['config'].area == 180.0


def test_o_caso_da_escola_guarda_mesmo_a_modulacao():
    """O caso que só existe porque o defeito da modulação foi corrigido."""
    caminho = os.path.join(CASOS, '08_escola_semanal.triton')
    if not os.path.exists(caminho):
        pytest.skip('casos do manual ainda não gerados')
    cfg = load_triton_project(caminho)['config']
    assert cfg.demand_mode == 'weekly'
    assert len(cfg.weekly_demands) == 7
    assert cfg.weekly_demands[-1] < cfg.weekly_demands[0], 'domingo fechado'


def test_os_estudos_de_exemplo_estao_no_esquema_corrente():
    """Os três de `examples/` eram lidos como projeto padrão, em silêncio."""
    pasta = os.path.join(PROJETO_SOBREVIVE_AO_ARQUIVO_RAIZ, 'examples')
    if not os.path.isdir(pasta):
        pytest.skip('pasta de exemplos ausente')
    achados = 0
    for arquivo in sorted(os.listdir(pasta)):
        if not arquivo.startswith('estudo_caso_'):
            continue
        achados += 1
        proj = load_triton_project(os.path.join(pasta, arquivo))
        assert proj['precip_data'] is not None, arquivo
        assert proj['config'].area > 100.0, arquivo
    assert achados == 3


# ---- origem: tests/unit/test_projeto_climbra.py
_ARQUIVO_PROJETO_CLIMBRA = str(_TESTES / 'unit/test_projeto_climbra.py')

PROJETO_CLIMBRA_RAIZ = Path(_ARQUIVO_PROJETO_CLIMBRA).resolve().parents[2]


@pytest.fixture(scope='module')
def cfg_climbra():
    cfg = TritonConfig()
    cfg.climate_source_mode = 'national_db'
    cfg.climate_city_uf, cfg.climate_city_name = ('SC', 'Florianópolis')
    cfg.climate_model, cfg.climate_scenario = ('MIROC6', 'HIST')
    cfg.climate_start_date, cfg.climate_end_date = ('01/01/1990', '31/12/1999')
    cfg.start_date = '01/01/1990'
    try:
        serie = serie_da_climbra(cfg)
    except (FileNotFoundError, ValueError):
        pytest.skip('base CLIMBra ausente')
    return (cfg, serie)


def test_arquivo_guarda_a_referencia_e_nao_a_serie(cfg_climbra, tmp_path):
    cfg, serie = cfg_climbra
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)
    chuva = json.loads(destino.read_text(encoding='utf-8'))['rainfall']
    assert chuva['precipitation_mm'] == []
    ref = chuva['climbra_series']
    assert (ref['origem'], ref['modelo'], ref['cenario']) == ('CLIMBra', 'MIROC6', 'HIST')
    assert (ref['inicio'], ref['fim']) == ('01/01/1990', '31/12/1999')
    assert ref['dias'] == len(serie) == chuva['total_days']
    assert ref['sha256'] == impressao_da_serie(serie)['sha256']


def test_leitura_recompoe_a_serie_igual(cfg_climbra, tmp_path):
    cfg, serie = cfg_climbra
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)
    proj = load_triton_project(str(destino))
    assert proj.get('chuva_da_climbra') and (not proj.get('aviso_chuva'))
    assert np.array_equal(proj['precip_data'], serie)
    assert proj['config'].climate_model == 'MIROC6'


def test_serie_alterada_continua_incorporada(cfg_climbra, tmp_path):
    cfg, serie = cfg_climbra
    alterada = serie.copy()
    alterada[10] += 5.0
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=alterada)
    chuva = json.loads(destino.read_text(encoding='utf-8'))['rainfall']
    assert chuva['climbra_series'] is None and len(chuva['precipitation_mm']) == len(serie)
    assert np.array_equal(load_triton_project(str(destino))['precip_data'], alterada)


def test_arquivo_proprio_continua_incorporado(cfg_climbra, tmp_path):
    cfg, serie = cfg_climbra
    proprio = TritonConfig()
    proprio.climate_source_mode = 'custom_file'
    destino = tmp_path / 'p.triton'
    export_triton_json(proprio, str(destino), precip_data=serie)
    assert len(json.loads(destino.read_text(encoding='utf-8'))['rainfall']['precipitation_mm']) == len(serie)


def test_impressao_diferente_avisa(cfg_climbra, tmp_path):
    cfg, serie = cfg_climbra
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)
    dados = json.loads(destino.read_text(encoding='utf-8'))
    dados['rainfall']['climbra_series']['sha256'] = '0' * 64
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')
    proj = load_triton_project(str(destino))
    assert 'difere' in proj['aviso_chuva']
    assert proj['precip_data'] is not None


def test_base_climbra_ausente_ao_abrir_avisa_e_nao_inventa_serie(cfg_climbra, tmp_path, monkeypatch):
    """Modo de falha: o projeto guarda a referência da série, e a base não existe ali.

    É o caso do arquivo gravado na Edição Brasil e aberto na International, que não traz a
    CLIMBra. O leitor não pode cair numa série qualquer nem estourar: avisa e devolve sem chuva.
    """
    from triton.core import parser as _parser
    cfg, serie = cfg_climbra
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)

    def sem_base(_cfg):
        raise FileNotFoundError('base CLIMBra não instalada')
    monkeypatch.setattr(_parser, 'serie_da_climbra', sem_base)
    proj = load_triton_project(str(destino))
    assert proj['precip_data'] is None
    assert not proj.get('chuva_da_climbra')
    assert 'CLIMBra' in proj['aviso_chuva'] and 'MIROC6' in proj['aviso_chuva']
    assert proj['config'].climate_source_mode == 'national_db'  # a referência continua no projeto


def test_linha_de_comando_le_o_projeto_pela_referencia(cfg_climbra, tmp_path):
    """Paridade: a linha de comando recompõe a mesma série e dá o mesmo resultado."""
    from triton.cli import run_analysis
    cfg, serie = cfg_climbra
    destino = tmp_path / 'p.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)
    saida = tmp_path / 'r.json'
    subprocess.run([sys.executable, '-m', 'triton.cli', 'run', str(destino), '--format', 'json', '--output', str(saida)], check=True, cwd=PROJETO_CLIMBRA_RAIZ, capture_output=True)
    cli = json.loads(saida.read_text(encoding='utf-8'))
    assert cli['provenance']['rainfall_days'] == len(serie)
    direto = run_analysis(load_triton_project(str(destino))['config'], serie, 'technical')
    assert [a['potable_savings_pct'] for a in cli['technical']['alternatives']] == pytest.approx([a['potable_savings_pct'] for a in direto['technical']['alternatives']])


# ---- origem: tests/unit/test_excel_scenarios.py
_ARQUIVO_EXCEL_SCENARIOS = str(_TESTES / 'unit/test_excel_scenarios.py')

SERIES = Path(_ARQUIVO_EXCEL_SCENARIOS).resolve().parents[2] / 'data' / 'rainfall'


def test_modelo_gerado_pelo_programa_e_legivel_pelo_programa(tmp_path):
    """O modelo de planilha distribuído ao usuário precisa ser lido de volta.

    Se gerador e leitor divergirem nos nomes de coluna, o usuário recebe um modelo
    que o próprio programa não entende.
    """
    destino = tmp_path / 'modelo.xlsx'
    caminho = generate_sample_scenario_excel(str(destino))
    assert Path(caminho).exists(), 'o modelo de cenários não foi gravado'
    cenarios = parse_excel_scenarios(str(destino))
    assert cenarios, 'o modelo gerado pelo programa não produziu nenhum cenário ao ser lido'
    for cenario in cenarios:
        assert cenario.get('scenario_name'), 'cenário sem nome após a leitura'
        assert float(cenario.get('area', 0)) > 0, f'área inválida em {cenario}'


def test_modelo_gerado_pelo_programa_roda_com_as_series_distribuidas(tmp_path):
    """Cada série citada no modelo existe em data/rainfall, e o modelo roda.

    O modelo já apontou para uma série que não era distribuída: o exemplo
    entregue ao usuário falhava na primeira execução.
    """
    destino = tmp_path / 'modelo.xlsx'
    cenarios = parse_excel_scenarios(generate_sample_scenario_excel(str(destino)))
    for cenario in cenarios:
        assert (SERIES / Path(cenario['precip_file']).name).exists(), cenario['precip_file']
    resultados = run_parsed_scenarios(cenarios[:1])
    assert len(resultados) == 1


def test_serie_ausente_e_erro_claro_e_nunca_troca_silenciosa(tmp_path):
    """Sem a série do cenário, o erro diz qual cenário e qual arquivo.

    Trocar em silêncio pela chuva de outra cidade daria um resultado plausível
    e errado.
    """
    destino = tmp_path / 'modelo.xlsx'
    cenarios = parse_excel_scenarios(generate_sample_scenario_excel(str(destino)))[:1]
    cenarios[0]['precip_file'] = 'Cidade_Inexistente.csv'
    with pytest.raises(FileNotFoundError, match="Cenário '.+': série de chuva 'Cidade_Inexistente.csv' não encontrada"):
        run_parsed_scenarios(cenarios)


def test_leitura_aceita_planilha_em_memoria(tmp_path):
    """A leitura funciona a partir de bytes, e não apenas de caminho em disco."""
    destino = tmp_path / 'modelo.xlsx'
    generate_sample_scenario_excel(str(destino))
    do_disco = parse_excel_scenarios(str(destino))
    da_memoria = parse_excel_scenarios(destino.read_bytes())
    assert len(da_memoria) == len(do_disco)
    assert [c['scenario_name'] for c in da_memoria] == [c['scenario_name'] for c in do_disco]


def test_leitura_de_csv_com_separador_detectado(tmp_path):
    """Planilhas exportadas como CSV também são aceitas."""
    csv = tmp_path / 'cenarios.csv'
    csv.write_text('cenario;area;moradores;demanda;percentual;reservatorio\nResidencial A;120;4;150;40;5000\nResidencial B;250;6;150;50;8000\n', encoding='utf-8')
    cenarios = parse_excel_scenarios(str(csv))
    assert len(cenarios) == 2
    assert cenarios[0]['scenario_name'] == 'Residencial A'
    assert float(cenarios[0]['area']) == pytest.approx(120.0)


def test_leitura_usa_nome_padrao_quando_a_coluna_falta(tmp_path):
    """Sem coluna de nome, os cenários recebem identificação sequencial.

    Evita que linhas anônimas se confundam num relatório de lote.
    """
    csv = tmp_path / 'sem_nome.csv'
    csv.write_text('area;moradores;demanda\n100;4;150\n200;4;150\n', encoding='utf-8')
    cenarios = parse_excel_scenarios(str(csv))
    assert len(cenarios) == 2
    nomes = [c['scenario_name'] for c in cenarios]
    assert len(set(nomes)) == 2, f'cenários sem nome não foram distinguidos: {nomes}'


def test_grade_fatorial_tem_o_produto_cartesiano_completo():
    """A contagem de combinações é o produto das dimensões — sem faltar nem repetir."""
    grade = generate_factorial_grid(precip_files=[('Floripa', 'Florianopolis1.csv'), ('Manaus', 'Manaus1.csv')], areas=[100.0, 200.0, 300.0], residents_list=[2, 4], demands_per_capita=[150.0], rainwater_shares=[0.4, 0.5], lower_tanks=[5000.0])
    esperado = 2 * 3 * 2 * 1 * 2
    assert len(grade) == esperado, f'grade fatorial com {len(grade)} combinações, esperado {esperado}'


def test_grade_fatorial_gera_nomes_unicos():
    """Nomes repetidos sobrescreveriam resultados na consolidação do lote."""
    grade = generate_factorial_grid(precip_files=[('Floripa', 'Florianopolis1.csv')], areas=[100.0, 200.0], residents_list=[2, 4], demands_per_capita=[150.0, 200.0], rainwater_shares=[0.4], lower_tanks=[5000.0])
    nomes = [c['scenario_name'] for c in grade]
    assert len(set(nomes)) == len(nomes), 'a grade fatorial gerou nomes duplicados'


def test_grade_fatorial_preserva_os_valores_de_entrada():
    """Cada combinação carrega exatamente os parâmetros que a originaram."""
    areas = [80.0, 160.0]
    grade = generate_factorial_grid(precip_files=[('Floripa', 'Florianopolis1.csv')], areas=areas, residents_list=[3], demands_per_capita=[180.0], rainwater_shares=[0.45], lower_tanks=[6000.0])
    assert sorted({float(c['area']) for c in grade}) == sorted(areas)
    for cenario in grade:
        assert cenario['city_label'] == 'Floripa'
        assert cenario['precip_file'] == 'Florianopolis1.csv'


def test_grade_fatorial_vazia_quando_uma_dimensao_e_vazia():
    """Produto cartesiano com fator vazio é vazio — não deve gerar combinação órfã."""
    grade = generate_factorial_grid(precip_files=[], areas=[100.0], residents_list=[4], demands_per_capita=[150.0], rainwater_shares=[0.4], lower_tanks=[5000.0])
    assert grade == []


def test_exportacao_produz_planilha_legivel():
    """O que é exportado precisa ser reabrível como planilha."""
    resultados = [{'scenario_name': 'Cenario A', 'city_label': 'Floripa', 'area': 120.0, 'potential_savings_pct': 42.5, 'optimal_volume_l': 5000.0}, {'scenario_name': 'Cenario B', 'city_label': 'Manaus', 'area': 250.0, 'potential_savings_pct': 61.2, 'optimal_volume_l': 8000.0}]
    conteudo = export_scenarios_to_excel_bytes(resultados)
    assert isinstance(conteudo, (bytes, bytearray)) and len(conteudo) > 0
    import openpyxl
    planilha = openpyxl.load_workbook(io.BytesIO(conteudo))
    aba = planilha[planilha.sheetnames[0]]
    assert aba.max_row >= len(resultados), 'a planilha exportada perdeu linhas'
    texto = ' '.join((str(celula.value) for linha in aba.iter_rows() for celula in linha if celula.value is not None))
    assert 'Cenario A' in texto and 'Cenario B' in texto, 'os nomes dos cenários não sobreviveram à exportação'


def test_exportacao_de_lista_vazia_nao_quebra():
    """Um lote sem resultados exporta planilha vazia em vez de estourar exceção."""
    conteudo = export_scenarios_to_excel_bytes([])
    assert isinstance(conteudo, (bytes, bytearray))


# ---- origem: tests/unit/test_scenarios_matrix.py
_ARQUIVO_SCENARIOS_MATRIX = str(_TESTES / 'unit/test_scenarios_matrix.py')

SCENARIOS_MATRIX_RAIZ = Path(_ARQUIVO_SCENARIOS_MATRIX).resolve().parents[2]


CHUVA = SCENARIOS_MATRIX_RAIZ / 'data' / 'rainfall'


REFERENCIA_NETUNO4 = SCENARIOS_MATRIX_RAIZ / 'data' / 'simulation_outputs' / 'SimulacaoManausSaoPaulo' / 'Planilha.csv'


from triton.core.edition import serie_de_exemplo_da_edicao  # a série de chuva distribuída com a edição


def _series(*nomes):
    disponiveis = [(nome.split('.')[0], str(CHUVA / nome)) for nome in nomes if (CHUVA / nome).exists()]
    if not disponiveis:
        pytest.skip('séries pluviométricas ausentes em data/rainfall/')
    return disponiveis


@pytest.fixture(scope='module')
def matriz_pequena():
    """Matriz fatorial mínima, executada em modo sequencial."""
    return run_multi_scenario_matrix(precip_files=_series(serie_de_exemplo_da_edicao()), areas=[100.0, 200.0], residents_list=[4], demands_per_capita=[150.0], rainwater_shares=[0.4], lower_tanks=[5000.0], run_as_sweeps=False, parallel=False)


def test_matriz_executa_o_produto_cartesiano(matriz_pequena):
    """Cada combinação de parâmetros vira exatamente um cenário executado."""
    assert matriz_pequena.total_scenarios_run == 2, f'esperadas 2 combinações, obtidas {matriz_pequena.total_scenarios_run}'
    assert len(matriz_pequena.outputs) == 2


def test_cada_cenario_produz_resultado(matriz_pequena):
    """Nenhum cenário pode voltar vazio: um lote silenciosamente incompleto é pior
    que um lote que falha, porque entra no estudo sem ser notado."""
    for saida in matriz_pequena.outputs:
        assert saida.result is not None or saida.sweep_result is not None, f'cenário {saida.scenario.scenario_id} não produziu resultado'


def test_parametros_do_cenario_sao_preservados(matriz_pequena):
    """Os parâmetros que definiram a combinação chegam íntegros ao resultado."""
    areas = sorted((saida.scenario.area for saida in matriz_pequena.outputs))
    assert areas == [100.0, 200.0]
    for saida in matriz_pequena.outputs:
        assert saida.scenario.residents == 4
        assert saida.scenario.demand_per_capita == pytest.approx(150.0)
        assert saida.scenario.total_demand_l_day == pytest.approx(600.0), 'demanda total deveria ser demanda per capita × moradores'


def test_area_maior_nao_reduz_a_economia(matriz_pequena):
    """A matriz herda a monotonicidade do motor: mais captação, não menos economia."""
    por_area = {}
    for saida in matriz_pequena.outputs:
        resultado = saida.result or saida.sweep_result
        economia = getattr(resultado, 'potential_potable_savings_pct', None)
        if economia is None:
            economia = getattr(resultado, 'optimal_potential_pct', None)
        if economia is not None:
            por_area[saida.scenario.area] = economia
    if len(por_area) == 2:
        assert por_area[200.0] >= por_area[100.0] - 1e-09, f'economia caiu com área maior: {por_area}'


def test_callback_de_progresso_e_chamado_uma_vez_por_cenario():
    """A interface depende do callback para a barra de progresso do lote."""
    chamadas = []
    run_multi_scenario_matrix(precip_files=_series(serie_de_exemplo_da_edicao()), areas=[100.0, 150.0, 200.0], residents_list=[4], demands_per_capita=[150.0], rainwater_shares=[0.4], lower_tanks=[5000.0], run_as_sweeps=False, parallel=False, progress_callback=lambda atual, total, saida, resumo: chamadas.append((atual, total)))
    assert len(chamadas) == 3, f'callback chamado {len(chamadas)} vezes para 3 cenários'
    assert all((total == 3 for _, total in chamadas)), 'o total informado ao callback oscilou'
    assert [atual for atual, _ in chamadas] == [1, 2, 3], f'a contagem de progresso não foi sequencial: {chamadas}'


def test_exportacao_gera_arquivo_com_uma_linha_por_cenario(matriz_pequena, tmp_path):
    """O arquivo exportado tem cabeçalho mais uma linha por cenário."""
    destino = tmp_path / 'Planilha.csv'
    export_matrix_planilha_csv(matriz_pequena, str(destino))
    assert destino.exists()
    linhas = [l for l in destino.read_text(encoding='latin-1').splitlines() if l.strip()]
    assert len(linhas) == 1 + len(matriz_pequena.outputs), f'{len(linhas)} linhas para {len(matriz_pequena.outputs)} cenários mais cabeçalho'


def test_cabecalho_exportado_coincide_com_a_planilha_real_do_netuno4(matriz_pequena, tmp_path):
    """Confronta a afirmação do código com os dados de referência.

    `export_matrix_planilha_csv` declara produzir o formato exato do Netuno 4. Como o
    repositório versiona planilhas realmente exportadas pelo Netuno 4, a afirmação é
    verificável: os cabeçalhos devem coincidir coluna a coluna.
    """
    if not REFERENCIA_NETUNO4.exists():
        pytest.skip('planilha de referência do Netuno 4 ausente')
    destino = tmp_path / 'Planilha.csv'
    export_matrix_planilha_csv(matriz_pequena, str(destino))
    cabecalho_exportado = destino.read_text(encoding='latin-1').splitlines()[0]
    cabecalho_referencia = REFERENCIA_NETUNO4.read_text(encoding='latin-1').splitlines()[0]
    colunas_exportadas = [c.strip() for c in cabecalho_exportado.split(';') if c.strip()]
    colunas_referencia = [c.strip() for c in cabecalho_referencia.split(';') if c.strip()]
    assert colunas_exportadas == colunas_referencia, f'o cabeçalho exportado difere do produzido pelo Netuno 4.\n  exportado : {colunas_exportadas}\n  referência: {colunas_referencia}'


def test_exportacao_usa_virgula_decimal(matriz_pequena, tmp_path):
    """O formato do Netuno 4 usa vírgula decimal; ponto quebraria a releitura."""
    destino = tmp_path / 'Planilha.csv'
    export_matrix_planilha_csv(matriz_pequena, str(destino))
    primeira_linha_de_dados = destino.read_text(encoding='latin-1').splitlines()[1]
    campos = primeira_linha_de_dados.split(';')
    numericos = [c for c in campos if c and any((d.isdigit() for d in c))]
    assert numericos, 'a linha exportada não contém campos numéricos'
    assert not any(('.' in campo and ',' not in campo and campo.replace('.', '').isdigit() for campo in numericos)), f'campo numérico com ponto decimal na exportação: {numericos}'


def test_planilha_exportada_e_relida_pelo_comparador_de_replicacao(matriz_pequena, tmp_path):
    """Fecha o ciclo: o que o Triton exporta é lido pelo comparador de replicação.

    Garante que a exportação não é apenas parecida com o formato do Netuno 4, mas
    efetivamente consumível pelo mesmo leitor usado na comparação oficial.
    """
    import pandas as pd
    destino = tmp_path / 'Planilha.csv'
    export_matrix_planilha_csv(matriz_pequena, str(destino))
    df = pd.read_csv(destino, sep=';', decimal=',', encoding='latin1', engine='python')
    assert len(df) == len(matriz_pequena.outputs)
    assert str(df.iloc[0, 1]).endswith('.csv'), f'a segunda coluna deveria nomear a série pluviométrica, obtido {df.iloc[0, 1]!r}'


# ---- origem: tests/unit/test_exportar_tudo.py

@pytest.fixture(scope='module')
def planilha(tmp_path_factory):
    rng = np.random.default_rng(7)
    chuva = np.where(rng.random(730) < 0.35, rng.exponential(12, 730), 0.0)
    cfg = TritonConfig()
    alegrete = get_city_data('RS', 'Alegrete')  # None fora da Edição Brasil (banco vazio)
    if alegrete is not None:
        cfg.water_tariffs = [tuple(f) for f in alegrete['faixas']]
        cfg.sewage_mode, cfg.sewage_rate = esgoto_do_municipio(alegrete)
    else:
        # Escalões de água sintéticos, só para o teste (não são de nenhuma entidade).
        cfg.water_tariffs = [(0.0, 0.0, 12.0, -1), (0.0, 10.0, 4.0, 1), (10.0, 20.0, 6.0, 1), (20.0, 999999.0, 8.0, 1)]
        cfg.sewage_mode, cfg.sewage_rate = 1, 80.0

    sim = run_single_simulation(chuva, 5000.0, area=150, total_demand_per_day=400, rainwater_share=0.4, store_daily_details=True)
    economia = run_economic_analysis(cfg, sim)
    m3 = sim.avg_pluvial_consumed_l_day * 0.365
    ambiental = calculate_lca(5000.0, m3, EnvironmentalConfig(annual_water_saved_m3=m3))
    dados = {'project_name': 'Auditoria', 'lower_vol': 5000, 'upper_vol': 1000, 'area': 150}
    dados.update(generate_study_layout(dados))
    caminho = tmp_path_factory.mktemp('tudo') / 'auditoria.xlsx'
    exportar_tudo(str(caminho), config=cfg, project_data=dados, single_result=sim, economic_result=economia, environmental_result=ambiental)
    return (cfg, openpyxl.load_workbook(caminho))


def _coluna(ws, indice=0):
    return [linha[indice] for linha in ws.iter_rows(min_row=2, values_only=True)]


def test_todo_campo_da_configuracao_esta_nas_premissas(planilha):
    cfg, wb = planilha
    campos = set(_coluna(wb['Auditoria_Premissas']))
    faltam = {f.name for f in dataclasses.fields(TritonConfig)} - campos
    assert not faltam, faltam


def test_a_tarifa_sai_com_o_significado_de_cada_codigo_e_o_esgoto(planilha):
    _, wb = planilha
    ws = wb['Auditoria_Tarifa']
    textos = ' '.join((str(c) for linha in ws.iter_rows(values_only=True) for c in linha if c is not None))
    assert 'preço-base da fórmula exponencial' in textos and 'exponencial' in textos
    assert 'preço por m³ consumido' in textos


def test_a_etapa_de_qualidade_entra_no_carbono_e_na_planilha(planilha):
    """A ACV soma a ETAP dimensionada na etapa de qualidade; as duas aparecem."""
    _, wb = planilha
    assert 'Auditoria_ETAP' in wb.sheetnames
    itens = next((n for n in wb.sheetnames if n.startswith('Auditoria_Ambi·')))
    categorias = ' '.join((str(c) for c in _coluna(wb[itens], 1)))
    assert 'ETAP' in categorias or 'Desinfecção' in categorias


# ---- origem: tests/unit/test_verificacoes_da_revisao.py
_ARQUIVO_VERIFICACOES_DA_REVISAO = str(_TESTES / 'unit/test_verificacoes_da_revisao.py')

def test_versao_declarada_e_coerente():
    """A versao e declarada num lugar so e segue versionamento semantico.

    Fixar o numero exato aqui faria o teste reprovar a cada release, sem
    detectar defeito nenhum. O que se verifica e a forma e a coerencia entre
    triton/__init__.py e pyproject.toml, que e onde o engano acontece.
    """
    import os
    import re
    assert re.fullmatch('\\d+\\.\\d+\\.\\d+', __version__), __version__
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(_ARQUIVO_VERIFICACOES_DA_REVISAO))))
    caminho = os.path.join(raiz, 'pyproject.toml')
    if not os.path.isfile(caminho):
        pytest.skip('pyproject.toml nao distribuido nesta copia')
    with open(caminho, encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    declarada = re.search('^version\\s*=\\s*"([^"]+)"', conteudo, re.M)
    assert declarada, 'pyproject.toml sem declaracao de versao'
    assert declarada.group(1) == __version__, f'pyproject.toml diz {declarada.group(1)}, triton/__init__.py diz {__version__}'


# ==================================================================================================
# Modulação Probabilística
# ==================================================================================================

# ---- origem: tests/unit/test_modulacao_estocastica.py
_ARQUIVO_MODULACAO_ESTOCASTICA = str(_TESTES / 'unit/test_modulacao_estocastica.py')

MODULACAO_ESTOCASTICA_RAIZ = Path(_ARQUIVO_MODULACAO_ESTOCASTICA).resolve().parents[2]


_c_sw = MODULACAO_ESTOCASTICA_RAIZ / 'manual' / 'casos' / '04_tutorial_sweep.triton'
_caso_04 = MODULACAO_ESTOCASTICA_RAIZ / 'manual' / 'casos' / '04_tutorial_varredura.triton'
_caso_02 = MODULACAO_ESTOCASTICA_RAIZ / 'manual' / 'casos' / '02_tutorial_varredura.triton'
MODULACAO_ESTOCASTICA_CASO = _c_sw if _c_sw.exists() else (_caso_04 if _caso_04.exists() else _caso_02)


@pytest.fixture(scope='module')
def estudo():
    b = _load_bundle(str(MODULACAO_ESTOCASTICA_CASO))
    return (b['config'], _get_precipitation(b))


@pytest.mark.parametrize('dist, media, desvio', [(M.Distribuicao('normal', media=150, desvio=20), 150, 20), (M.Distribuicao('lognormal', media=150, desvio=30), 150, 30), (M.Distribuicao('uniforme', minimo=100, maximo=200), 150, 100 / np.sqrt(12)), (M.Distribuicao('triangular', minimo=100, moda=150, maximo=200), 150, np.sqrt((100 ** 2 + 150 ** 2 + 200 ** 2 - 100 * 150 - 100 * 200 - 150 * 200) / 18))])
def test_cada_distribuicao_devolve_a_media_e_o_desvio_pedidos(dist, media, desvio):
    v = dist.sortear(np.random.default_rng(1), 40000)
    assert v.mean() == pytest.approx(media, rel=0.01)
    assert v.std() == pytest.approx(desvio, rel=0.03)


def test_truncagem_respeita_os_limites():
    d = M.Distribuicao('normal', media=1.5, desvio=2.0, limite_inferior=1.0, limite_superior=4.0)
    v = d.sortear(np.random.default_rng(2), 5000)
    assert v.min() >= 1.0 and v.max() <= 4.0


def test_distribuicao_invalida_e_recusada():
    with pytest.raises(ValueError):
        M.Distribuicao('triangular', minimo=10, moda=5, maximo=20).validar()
    with pytest.raises(ValueError):
        M.Distribuicao('lognormal', media=0, desvio=1).validar()
    with pytest.raises(ValueError):
        M.Distribuicao('gama').validar()


def test_pessoas_sempre_inteiro_e_ao_menos_um(estudo):
    cfg, _ = estudo
    par = M.padroes_do_projeto(cfg)
    par.variaveis['pessoas'] = M.Distribuicao('normal', media=1.2, desvio=3.0, limite_inferior=0.0)
    amostras = M.sortear_amostras(cfg, par, 500, 3)
    pessoas = [a['pessoas'] for a in amostras]
    assert all((p >= 1 and float(p).is_integer() for p in pessoas))


def test_mesma_semente_mesmas_amostras(estudo):
    cfg, _ = estudo
    par = M.padroes_do_projeto(cfg)
    assert M.sortear_amostras(cfg, par, 20, 7) == M.sortear_amostras(cfg, par, 20, 7)
    assert M.sortear_amostras(cfg, par, 20, 7) != M.sortear_amostras(cfg, par, 20, 8)


def test_amostra_aplicada_recalcula_a_fracao_total(estudo):
    cfg, _ = estudo
    novo = M.aplicar_amostra(cfg, {'per_capita_l_dia': 120.0, 'pessoas': 3.0, 'fracao_nao_potavel_pct': 45.0})
    assert novo.demand_value == 120.0 and novo.residents_count == 3
    assert novo.non_potable_indoor_share == pytest.approx(0.45)
    assert novo.potable_indoor_share == pytest.approx(0.55)
    assert novo.rainwater_share == pytest.approx(fracao_total(360.0, 0.45, cfg.irrigation_liters_per_day or 0.0))
    assert cfg.demand_value != 120.0 or cfg.residents_count != 3


def test_series_recebem_o_fator_e_mantem_o_perfil(estudo):
    cfg, _ = estudo
    import copy
    c = copy.deepcopy(cfg)
    c.weekly_demands = [100.0, 200.0]
    c.weekly_shares = [30.0, 60.0]
    novo = M.aplicar_amostra(c, {'per_capita_l_dia': 2 * c.demand_value, 'pessoas': float(c.residents_count), 'fracao_nao_potavel_pct': 100.0 * c.non_potable_indoor_share * 2})
    assert novo.weekly_demands == pytest.approx([200.0, 400.0])
    assert novo.weekly_shares[0] == pytest.approx(60.0) and novo.weekly_shares[1] <= 100.0


def test_sem_variar_nada_o_p50_e_o_estudo(estudo):
    cfg, precip = estudo
    par = M.padroes_do_projeto(cfg)
    for dist in par.variaveis.values():
        dist.variar = False
    r = M.simular(cfg, precip, par, amostras=3, semente=1)
    for v in r['por_volume']:
        assert v['potencial_pct']['p50'] == pytest.approx(v['base']['potencial_pct'])
        assert v['vpl_brl']['p50'] == pytest.approx(v['base']['vpl_brl'])


@pytest.fixture(scope='module')
def resultado(estudo):
    cfg, precip = estudo
    return M.simular(cfg, precip, M.padroes_do_projeto(cfg), amostras=12, semente=5)


def test_painel_tem_faixas_ordenadas_e_frequencias_que_somam_100(resultado):
    assert resultado['realizacoes_feitas'] == 12 and (not resultado['cancelado'])
    for v in resultado['por_volume']:
        p = v['potencial_pct']
        assert p['p5'] <= p['p50'] <= p['p95']
    for chave in ('ideal_tecnico', 'otimo_economico', 'vencedor_topsis'):
        assert sum(resultado['frequencia_pct'][chave].values()) == pytest.approx(100.0)
    assert len(resultado['amostras']) == 12
    assert set(resultado['sensibilidade_spearman']) == set(M.PARAMETROS)
    json.dumps(resultado)


def test_otimo_economico_e_o_menor_payback_e_nao_o_maior_vpl():
    economicas = [{'npv_brl': 0.0, 'discounted_payback_months': None}, {'npv_brl': 1000.0, 'discounted_payback_months': 40.0}, {'npv_brl': 5000.0, 'discounted_payback_months': 60.0}]
    assert M._otimo_economico(economicas, [0.0, 1000.0, 2000.0]) == 1000.0


def test_cancelar_devolve_o_que_ja_foi_feito(estudo):
    cfg, precip = estudo
    feitas = []
    r = M.simular(cfg, precip, M.padroes_do_projeto(cfg), amostras=10, semente=1, ao_progredir=lambda a, b: feitas.append(a), cancelar=lambda: len(feitas) >= 2)
    assert r['realizacoes_feitas'] == 2 and r['cancelado']


def test_spearman():
    assert M.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert M.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)
    assert M.spearman([1, 1, 1], [1, 2, 3]) is None


def test_linha_de_comando_da_o_mesmo_resultado_que_o_nucleo(estudo, tmp_path):
    """Paridade: `triton probabilistic-study` e o núcleo (que a interface usa), mesma semente."""
    cfg, precip = estudo
    saida = tmp_path / 'r.json'
    subprocess.run([sys.executable, '-m', 'triton.cli', 'probabilistic-study', str(MODULACAO_ESTOCASTICA_CASO), '--samples', '4', '--seed', '11', '--format', 'json', '--output', str(saida), '--quiet'], check=True, cwd=MODULACAO_ESTOCASTICA_RAIZ, capture_output=True)
    cli = json.loads(saida.read_text(encoding='utf-8'))
    b = _load_bundle(str(MODULACAO_ESTOCASTICA_CASO))
    analise = b.get('analysis') or {}
    nucleo = M.simular(b['config'], _get_precipitation(b), M.padroes_do_projeto(b['config']), amostras=4, semente=11, pesos=analise.get('topsis_weights'), ambiental=analise.get('environmental'))
    assert cli['frequencia_pct'] == nucleo['frequencia_pct']
    for a, c in zip(cli['por_volume'], nucleo['por_volume']):
        assert a['potencial_pct'] == pytest.approx(c['potencial_pct'])
        assert a['vpl_brl'] == pytest.approx(c['vpl_brl'])


def test_linha_de_comando_aceita_distribuicao_por_opcao(tmp_path):
    saida = tmp_path / 'r.json'
    subprocess.run([sys.executable, '-m', 'triton.cli', 'probabilistic-study', str(MODULACAO_ESTOCASTICA_CASO), '--samples', '3', '--per-capita', 'triangular:100:150:200', '--people', 'fixo', '--non-potable', 'uniforme:20:40', '--format', 'json', '--output', str(saida), '--quiet'], check=True, cwd=MODULACAO_ESTOCASTICA_RAIZ, capture_output=True)
    r = json.loads(saida.read_text(encoding='utf-8'))
    assert r['parametros']['variaveis']['per_capita_l_dia']['tipo'] == 'triangular'
    assert r['parametros']['variaveis']['pessoas']['variar'] is False
    assert all((20 <= a['fracao_nao_potavel_pct'] <= 40 for a in r['amostras']))
    assert all((100 <= a['per_capita_l_dia'] <= 200 for a in r['amostras']))


def test_catalogo_padrao_liga_so_as_tres_de_consumo(estudo):
    cfg, _ = estudo
    par = M.padroes_do_projeto(cfg)
    assert set(par.variaveis) == set(M.CATALOGO)
    assert par.ativas() == list(M.PARAMETROS)
    for chave in M.CATALOGO:
        d = par.variaveis[chave]
        d.validar()
        assert d.valor_central() == pytest.approx(M.valor_do_projeto(cfg, chave), abs=1e-09)


def test_formato_da_primeira_versao_ainda_abre():
    antigo = {'per_capita_l_dia': {'tipo': 'normal', 'media': 150, 'desvio': 20}, 'pessoas': {'tipo': 'normal', 'media': 4, 'desvio': 1}, 'cv_diario_pct': 5}
    par = M.ParametrosIncertos.de_dict(antigo)
    assert set(par.variaveis) == {'per_capita_l_dia', 'pessoas'} and par.cv_diario_pct == 5
    assert M.ParametrosIncertos.de_dict(par.para_dict()).para_dict() == par.para_dict()


@pytest.mark.parametrize('chave, valor, grandeza, sentido', [('fator_investimento', 1.5, 'vpl', -1), ('fator_tarifa', 1.2, 'vpl', +1), ('area_m2', 1.3, 'economia', +1), ('descarte_mm', +2.0, 'economia', -1), ('demanda_externa_l_dia', 200.0, 'economia', +1)])
def test_cada_variavel_move_o_resultado_no_sentido_esperado(estudo, chave, valor, grandeza, sentido):
    from triton.cli import run_analysis
    cfg, precip = estudo
    base = M.valor_do_projeto(cfg, chave)
    novo = {'area_m2': base * valor, 'descarte_mm': base + valor}.get(chave, valor)

    def no_volume(c):
        r = run_analysis(c, precip, 'all')
        t = next((x for x in r['technical']['alternatives'] if x['lower_tank_volume_l'] == 4000))
        e = next((x for x in r['economic']['alternatives'] if x['lower_tank_volume_l'] == 4000))
        return {'economia': t['potable_savings_pct'], 'vpl': e['npv_brl'], 'chuva': t['annual_rainwater_m3']}[grandeza]
    from triton.core.edition import usa_dados_do_brasil
    if chave == 'demanda_externa_l_dia' and not usa_dados_do_brasil():
        # A economia em % é relativa à demanda total: num clima seco (Lisboa) o reservatório de 4 m³
        # já está curto, a demanda extra é mal atendida e o percentual cai, embora a chuva
        # aproveitada suba. O sentido físico que vale em qualquer clima é o do volume aproveitado.
        grandeza = 'chuva'
    antes, depois = (no_volume(M.aplicar_amostra(cfg, {})), no_volume(M.aplicar_amostra(cfg, {chave: novo})))
    assert (depois - antes) * sentido > 0


def test_fator_da_chuva_multiplica_a_serie(estudo):
    cfg, precip = estudo
    par = M.ParametrosIncertos(variaveis={'fator_chuva': M.Distribuicao('uniforme', minimo=0.5, maximo=0.5)})
    r = M.simular(cfg, precip, par, amostras=2, semente=1)
    seco = r['referencia']['potencial_pct']['media']
    assert seco < r['referencia']['base']['potencial_pct']


def test_wilson():
    w = M.intervalo_de_wilson(0, 20)
    assert w['pct'] == 0 and w['ic95_inf'] == 0 and (0 < w['ic95_sup'] < 20)
    w = M.intervalo_de_wilson(10, 20)
    assert w['ic95_inf'] < 50 < w['ic95_sup']


def test_variavel_desconhecida_e_recusada():
    with pytest.raises(ValueError):
        M.ParametrosIncertos(variaveis={'chuva_de_granizo': M.Distribuicao()}).validar()


def _no_volume(cfg, precip, grandeza, volume=4000, ambiental=None):
    from triton.cli import run_analysis
    r = run_analysis(cfg, precip, 'all', environmental=ambiental, smaa=False)
    e = next((x for x in r['economic']['alternatives'] if x['lower_tank_volume_l'] == volume))
    a = next((x for x in r['environmental']['alternatives'] if x['lower_tank_volume_l'] == volume))
    return {'vpl': e['npv_brl'], 'capex': e['capex_brl'], 'co2': a['lifetime_net_co2_saved_kg']}[grandeza]


@pytest.mark.parametrize('chave, operacao, valor, sentido', [('fator_cisterna', 'vezes', 1.5, -1), ('fator_om', 'vezes', 2.0, -1), ('inflacao_om_pct_mes', 'mais', 0.5, -1), ('fator_esgoto', 'vezes', 1.5, +1), ('reajuste_tarifa_pct', 'mais', 3.0, +1), ('periodo_analise_anos', 'mais', 10.0, +1)])
def test_variaveis_de_custo_movem_o_vpl_no_sentido_esperado(estudo, chave, operacao, valor, sentido):
    cfg, precip = estudo
    base = M.valor_do_projeto(cfg, chave)
    novo = base * valor if operacao == 'vezes' else base + valor
    antes = _no_volume(M.aplicar_amostra(cfg, {}), precip, 'vpl')
    depois = _no_volume(M.aplicar_amostra(cfg, {chave: novo}), precip, 'vpl')
    assert (depois - antes) * sentido > 0


def test_fator_da_cisterna_pesa_menos_que_o_do_investimento_inteiro(estudo):
    """A cisterna é uma parte do investimento: dobrá-la custa menos que dobrar tudo."""
    cfg, precip = estudo
    base = _no_volume(M.aplicar_amostra(cfg, {}), precip, 'capex')
    cisterna = _no_volume(M.aplicar_amostra(cfg, {'fator_cisterna': 2.0}), precip, 'capex')
    tudo = _no_volume(M.aplicar_amostra(cfg, {'fator_investimento': 2.0}), precip, 'capex')
    assert base < cisterna < tudo
    assert tudo == pytest.approx(2.0 * base)


def test_periodo_de_analise_e_inteiro_e_ao_menos_um(estudo):
    cfg, _ = estudo
    par = M.ParametrosIncertos(variaveis={'periodo_analise_anos': M.Distribuicao('normal', media=3, desvio=5)})
    anos = [a['periodo_analise_anos'] for a in M.sortear_amostras(cfg, par, 300, 4)]
    assert all((x >= 1 and float(x).is_integer() for x in anos))
    assert M.aplicar_amostra(cfg, {'periodo_analise_anos': 17.0}).analysis_period_years == 17


@pytest.mark.parametrize('modo', [0, 1, 2])
def test_fator_do_esgoto_vale_em_todos_os_modos(estudo, modo):
    cfg, _ = estudo
    c = M.aplicar_amostra(cfg, {})
    c.sewage_mode, c.sewage_rate = (modo, 80.0)
    assert M.aplicar_amostra(c, {'fator_esgoto': 1.25}).sewage_rate == pytest.approx(100.0)
    esperado = 80.0 * 1.1 if modo in (0, 2) else 80.0
    assert M.aplicar_amostra(c, {'fator_tarifa': 1.1}).sewage_rate == pytest.approx(esperado)


@pytest.mark.parametrize('chave, sentido', [('fator_emissao_agua', +1), ('fator_emissao_rede', -1)])
def test_fatores_de_emissao_movem_o_saldo_de_carbono(estudo, chave, sentido):
    cfg, precip = estudo
    par = M.ParametrosIncertos(variaveis={chave: M.Distribuicao('uniforme', minimo=3.0, maximo=3.0)})
    # Fatores da rede e da água dados de propósito: fora da Brasil o padrão do motor é zero, e um
    # multiplicador de zero não move o saldo de carbono.
    r = M.simular(cfg, precip, par, amostras=1, semente=1, ambiental={'grid_co2_factor_kg_kwh': FATOR_DA_REDE_DE_TESTE, 'potable_water_co2_kg_m3': 0.35})
    ref = r['referencia']
    assert (ref['co2_kg']['media'] - ref['base']['co2_kg']) * sentido > 0


def test_sorteio_de_modelos_nao_muda_os_demais_sorteios(estudo):
    cfg, _ = estudo
    sem = M.padroes_do_projeto(cfg)
    com = M.padroes_do_projeto(cfg)
    com.modelos_climaticos = ['INM-CM4', 'MIROC6', 'KACE']
    a, b = (M.sortear_amostras(cfg, sem, 50, 8), M.sortear_amostras(cfg, com, 50, 8))
    for x, y in zip(a, b):
        assert {k: v for k, v in y.items() if k != 'modelo_climatico'} == x
    sorteados = [y['modelo_climatico'] for y in b]
    assert set(sorteados) == set(com.modelos_climaticos)
    assert sorteados == [y['modelo_climatico'] for y in M.sortear_amostras(cfg, com, 50, 8)]


def test_modelo_desconhecido_ou_repetido_e_recusado():
    with pytest.raises(ValueError):
        M.ParametrosIncertos(modelos_climaticos=['MODELO-X']).validar()
    with pytest.raises(ValueError):
        M.ParametrosIncertos(modelos_climaticos=['MIROC6', 'MIROC6']).validar()


def test_modelos_pedem_a_base_climbra(estudo):
    cfg, precip = estudo
    assert not M.pode_sortear_modelos(cfg)
    with pytest.raises(ValueError, match='CLIMBra'):
        M.simular(cfg, precip, M.ParametrosIncertos(modelos_climaticos=['MIROC6']), amostras=1)


def test_cada_realizacao_usa_a_serie_do_modelo_sorteado(estudo):
    """Só o modelo varia: um modelo seco dá economia menor, e o η² da economia é 1."""
    cfg, precip = estudo
    serie = np.asarray(precip, dtype=float)
    par = M.ParametrosIncertos(modelos_climaticos=['INM-CM4', 'MIROC6'])
    r = M.simular(cfg, serie, par, amostras=8, semente=3, series_dos_modelos={'INM-CM4': serie, 'MIROC6': serie * 0.3})
    por = {m['modelo']: m for m in r['por_modelo']}
    assert por['INM-CM4']['realizacoes'] + por['MIROC6']['realizacoes'] == 8
    assert por['MIROC6']['potencial_pct']['media'] < por['INM-CM4']['potencial_pct']['media']
    assert por['INM-CM4']['potencial_pct']['media'] == pytest.approx(r['referencia']['base']['potencial_pct'])
    assert r['sensibilidade_modelo_eta2']['potencial_pct'] == pytest.approx(1.0)
    assert all(('modelo_climatico' in a for a in r['amostras']))
    json.dumps(r)


def test_razao_de_correlacao():
    assert M.razao_de_correlacao(['a', 'a', 'b', 'b'], [1, 1, 5, 5]) == pytest.approx(1.0)
    assert M.razao_de_correlacao(['a', 'b', 'a', 'b'], [1, 1, 5, 5]) == pytest.approx(0.0)
    assert M.razao_de_correlacao(['a', 'a', 'a'], [1, 2, 3]) is None


def _projeto_climbra(tmp_path):
    dados = json.loads(MODULACAO_ESTOCASTICA_CASO.read_text(encoding='utf-8'))
    dados['rainfall']['source_mode'] = 'national_db'
    destino = tmp_path / 'climbra.triton'
    destino.write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')
    return destino


def test_linha_de_comando_sorteia_os_modelos_como_o_nucleo(tmp_path):
    """Paridade com modelos climáticos: `--climate-models` e o núcleo, mesma semente."""
    projeto = _projeto_climbra(tmp_path)
    b = _load_bundle(str(projeto))
    try:
        M.series_dos_modelos_climaticos(b['config'], ['INM-CM4'])
    except (FileNotFoundError, ValueError):
        pytest.skip('base CLIMBra ausente')
    saida = tmp_path / 'r.json'
    subprocess.run([sys.executable, '-m', 'triton.cli', 'probabilistic-study', str(projeto), '--samples', '4', '--seed', '11', '--climate-models', 'INM-CM4,MIROC6', '--format', 'json', '--output', str(saida), '--quiet'], check=True, cwd=MODULACAO_ESTOCASTICA_RAIZ, capture_output=True)
    cli = json.loads(saida.read_text(encoding='utf-8'))
    analise = b.get('analysis') or {}
    par = M.padroes_do_projeto(b['config'])
    par.modelos_climaticos = ['INM-CM4', 'MIROC6']
    nucleo = M.simular(b['config'], _get_precipitation(b), par, amostras=4, semente=11, pesos=analise.get('topsis_weights'), ambiental=analise.get('environmental'))
    assert [a['modelo_climatico'] for a in cli['amostras']] == [a['modelo_climatico'] for a in nucleo['amostras']]
    for a, c in zip(cli['por_volume'], nucleo['por_volume']):
        assert a['potencial_pct'] == pytest.approx(c['potencial_pct'])


def test_linha_de_comando_recusa_modelos_com_arquivo_proprio():
    r = subprocess.run([sys.executable, '-m', 'triton.cli', 'probabilistic-study', str(MODULACAO_ESTOCASTICA_CASO), '--samples', '2', '--climate-models', 'MIROC6', '--quiet'], cwd=MODULACAO_ESTOCASTICA_RAIZ, capture_output=True)
    assert r.returncode != 0
    assert 'CLIMBra' in r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')


# ==================================================================================================
# Porta de validação da estrutura tarifária
# ==================================================================================================

# ---- origem: tests/unit/test_porta_de_validacao_tarifaria.py

TRUNCADA = {'municipio': 'Teste', 'tarifa_fixa_mensal': 30.0, 'faixas': [[0.0, 0.0, 30.0, -1], [0.0, 6.0, 0.0, 1]]}


MINIMO_DILUIDO = {'municipio': 'Teste', 'tarifa_fixa_mensal': 52.89, 'faixas': [[0.0, 10.0, 5.289, 1], [10.0, 999999.0, 9.8, 1]]}


COM_LACUNA = {'municipio': 'Teste', 'faixas': [[0.0, 10.0, 3.0, 1], [15.0, 999999.0, 5.0, 1]]}


BOA = {'municipio': 'Teste', 'tarifa_fixa_mensal': 40.0, 'faixas': [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]]}


@pytest.mark.parametrize(('registro', 'codigo'), [(TRUNCADA, 'tabela_truncada'), (MINIMO_DILUIDO, 'minimo_diluido_em_tarifa'), (COM_LACUNA, 'lacuna_entre_faixas')])
def test_a_porta_reconhece_cada_defeito_da_auditoria(registro, codigo):
    erros = [a for a in validar_estrutura(registro) if a.gravidade == 'erro']
    assert codigo in {a.codigo for a in erros}


def test_a_porta_deixa_passar_estrutura_correta():
    assert [a for a in validar_estrutura(BOA) if a.gravidade == 'erro'] == []


def test_um_aviso_nao_barra_a_atualizacao():
    """Tarifa não progressiva existe em tarifa social, e não é motivo de rejeição."""
    social = {'municipio': 'Teste', 'faixas': [[0.0, 5.0, 8.0, 1], [5.0, 999999.0, 3.0, 1]]}
    achados = validar_estrutura(social)
    assert achados
    assert [a for a in achados if a.gravidade == 'erro'] == []


# ==================================================================================================
# Geometria do arranjo, desenho e volumetria
# ==================================================================================================

# ---- origem: tests/unit/test_pipe_network.py

PIPE_NETWORK_COMPONENTS = [{'instance_id': 'CI-01', 'type_id': 'cisterna_inferior', 'position_mm': {'x': 0, 'y': 0, 'z': -1500}}, {'instance_id': 'B-01', 'type_id': 'motobomba', 'position_mm': {'x': 1500, 'y': 0, 'z': 0}}, {'instance_id': 'RS-01', 'type_id': 'reservatorio_superior', 'position_mm': {'x': 4500, 'y': 2000, 'z': 6500}, 'parameters': {'DIAMETRO_MM': 1200, 'ALTURA_MM': 700}}]


PIPE_NETWORK_RUNS = [{'run_id': 'T-01', 'system': 'succao', 'dn_mm': 32, 'start': 'CI-01', 'route': 'sobe 1500; +x 1500', 'end': 'B-01'}, {'run_id': 'T-02', 'system': 'recalque', 'dn_mm': 25, 'route': '+x 2100; +y 2000; sobe 7500; +x 900; desce 300', 'end': 'RS-01:topo'}, {'run_id': 'T-03', 'system': 'distribuicao', 'dn_mm': 25, 'start': 'RS-01:fundo', 'route': 'desce 3000; -y 4000'}]


def _pipe_network_project(runs=PIPE_NETWORK_RUNS, components=PIPE_NETWORK_COMPONENTS):
    return {'project_name': 'Casa 3D', 'ref_code': 'N5-3D', 'bim_components': components, 'pipe_runs': runs}


def test_parse_route_accepts_axes_aliases_and_free_deltas():
    assert parse_route('+x 3000; desce 1200; norte 500; d 2000 0 -20') == [(3000.0, 0.0, 0.0), (0.0, 0.0, -1200.0), (0.0, 500.0, 0.0), (2000.0, 0.0, -20.0)]
    assert parse_route([{'direction': '-y', 'length_mm': '1,5'}, {'dx': 1, 'dy': 2, 'dz': 3}]) == [(0.0, -1.5, 0.0), (1.0, 2.0, 3.0)]
    assert format_route(parse_route('+x 3000; desce 1200; d 2000 0 -20')) == '+x 3000; -z 1200; d 2000 0 -20'
    for bad in ('+w 100', '+x -5', 'd 1 2', 'sobe'):
        with pytest.raises(ValueError):
            parse_route(bad)


def test_runs_are_resolved_in_sequence_from_the_previous_end():
    manifest = build_bim_manifest(_pipe_network_project())
    assert validate_bim_manifest(manifest) == []
    runs = {run['run_id']: run for run in manifest['pipe_runs']}
    assert [run['sequence'] for run in manifest['pipe_runs']] == [1, 2, 3]
    assert runs['T-02']['start_ref'] == 'T-01'
    assert runs['T-02']['vertices_mm'][0] == {'x': 1500, 'y': 0, 'z': 0}
    assert runs['T-02']['vertices_mm'][-1] == {'x': 4500, 'y': 2000, 'z': 7200}
    assert runs['T-02']['length_mm'] == 12800
    assert lengths_by_dn(manifest['pipe_runs']) == {25.0: 19.8, 32.0: 3.0}


def test_reordering_changes_the_plant_and_is_reported():
    manifest = build_bim_manifest(_pipe_network_project(runs=[PIPE_NETWORK_RUNS[1], PIPE_NETWORK_RUNS[0], PIPE_NETWORK_RUNS[2]]))
    errors = validate_bim_manifest(manifest)
    assert any(('T-02' in e and 'primeiro trecho precisa de origem' in e for e in errors))


def test_declared_destination_is_checked_not_completed():
    runs = [dict(PIPE_NETWORK_RUNS[0], route='sobe 1500; +x 1400')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=runs)))
    assert errors == ["Trecho T-01: termina a 100 mm de B-01; falta 'd 100 0 0'."]


def test_dependent_run_is_not_resolved_when_its_origin_failed():
    runs = [dict(PIPE_NETWORK_RUNS[0], dn_mm=0), PIPE_NETWORK_RUNS[1]]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=runs)))
    assert any(('T-02: continua o trecho T-01' in e for e in errors))


def test_gravity_systems_warn_about_rising_or_flat_segments():
    runs = [{'run_id': 'C-01', 'system': 'captacao', 'dn_mm': 100, 'start': {'x': 0, 'y': 0, 'z': 3000}, 'route': '+x 2000; d 2000 0 -20; sobe 100'}]
    manifest = build_bim_manifest(_pipe_network_project(runs=runs, components=[]))
    assert validate_bim_manifest(manifest) == []
    warnings = manifest['validation']['warnings']
    assert len(warnings) == 2
    assert 'segmento 1: declividade 0,00 % abaixo de 0,5 %' in warnings[0]
    assert 'segmento 3: sobe 100 mm' in warnings[1]


def test_plant_3d_dxf_has_axes_tubes_components_and_manifest(tmp_path):
    output = tmp_path / 'planta.dxf'
    generate_project_dxf(_pipe_network_project(), str(output), mode='plant_3d')
    doc = ezdxf.readfile(output)
    assert not doc.audit().errors
    msp = doc.modelspace()
    axes = msp.query('POLYLINE')
    assert len(axes) == 3 and all((axis.is_3d_polyline for axis in axes))
    assert [axis.get_xdata('TRITON')[0].value for axis in axes] == ['T-01', 'T-02', 'T-03']
    assert len(msp.query('MESH')) == 2 + 5 + 2
    assert all((name in doc.layers for name in ('NETUNO_3D_SUCCAO', 'NETUNO_3D_RECALQUE_TUBO')))
    assert len(msp.query('INSERT')) == 3
    manifest = json.loads((tmp_path / 'planta_triton-bim.json').read_text(encoding='utf-8'))
    assert manifest['schema_version'] == '1.1'
    assert [run['run_id'] for run in manifest['pipe_runs']] == ['T-01', 'T-02', 'T-03']


def test_plant_3d_refuses_invalid_or_empty_organisation(tmp_path):
    with pytest.raises(ValueError, match='nenhum componente'):
        generate_project_dxf(_pipe_network_project(runs=[], components=[]), str(tmp_path / 'vazio.dxf'), mode='plant_3d')
    with pytest.raises(ValueError, match='falta'):
        generate_project_dxf(_pipe_network_project(runs=[dict(PIPE_NETWORK_RUNS[0], route='sobe 1500')]), str(tmp_path / 'x.dxf'), mode='plant_3d')
    assert not (tmp_path / 'x.dxf').exists()


def test_schematic_3d_lists_sequence_and_writes_real_measures():
    svg = generate_project_svg_diagram(_pipe_network_project(), mode='plant_3d')
    assert svg.startswith('<svg') and 'Esquema 3D da tubulação' in svg
    assert 'Sequência de montagem' in svg and 'Quantitativo por DN' in svg
    assert '↑ 7,50 m' in svg and '3,00 m' in svg and ('Cota +6,50 m' in svg) and ('Cota −1,50 m' in svg)
    assert 'CI-01 → B-01' in svg and 'T-01 → RS-01:topo' in svg
    assert 'paint-order' not in svg and 'context-stroke' not in svg


def test_schematic_axis_keeps_order_and_connections_but_compresses_long_runs():
    from triton.core.schematic_3d import _AxisScale
    scale = _AxisScale([0, 300, 12000, 12000, 12030])
    assert scale(0) < scale(300) < scale(12000) == scale(12030)
    assert scale(300) - scale(0) > 0.15


def test_schematic_marks_gravity_slope_and_numbers_warnings():
    runs = [{'run_id': 'C-01', 'system': 'captacao', 'dn_mm': 100, 'start': {'x': 0, 'y': 0, 'z': 3000}, 'route': 'd 6000 0 -12; desce 3000'}]
    svg = generate_project_svg_diagram(_pipe_network_project(runs=runs, components=[]), mode='plant_3d')
    assert 'i=0,2%' in svg and 'Avisos' in svg and ('C-01, segmento 1' in svg)


def test_bim_layout_round_trips_through_triton_file(tmp_path):
    path = tmp_path / 'projeto.triton'
    building = {'origin_mm': {'x': 0, 'y': 0, 'z': 0}, 'width_mm': 8000, 'depth_mm': 7000, 'height_mm': 6000, 'floors': 2}
    layout = {'bim_components': PIPE_NETWORK_COMPONENTS, 'pipe_runs': PIPE_NETWORK_RUNS, 'building_volume': building}
    export_triton_json(TritonConfig(), str(path), bim_layout=layout)
    assert load_triton_project(str(path))['bim_layout'] == layout
    export_triton_json(TritonConfig(), str(path))
    assert load_triton_project(str(path))['bim_layout'] == {'bim_components': [], 'pipe_runs': [], 'building_volume': {}}


def test_overlapping_pipes_under_the_tank_are_a_clash():
    runs = [PIPE_NETWORK_RUNS[0], dict(PIPE_NETWORK_RUNS[1], route='+x 3000; +y 2000; sobe 6500', end='RS-01'), dict(PIPE_NETWORK_RUNS[2], start='RS-01')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=runs)))
    assert len(errors) == 1
    assert errors[0].startswith('Trechos T-02 (recalque) e T-03 (distribuição não potável) se sobrepõem em 3,00 m')
    assert 'RS-01:topo e RS-01:fundo' in errors[0]


def test_crossing_and_parallel_close_pipes_are_clashes_but_touching_is_not():
    base = {'system': 'distribuicao', 'dn_mm': 50}
    crossing = [dict(base, run_id='A', start={'x': 0, 'y': 0, 'z': 0}, route='+x 2000'), dict(base, run_id='B', start={'x': 1000, 'y': -1000, 'z': 30}, route='+y 2000')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=crossing, components=[])))
    assert len(errors) == 1 and 'se cruzam' in errors[0]
    touching = [crossing[0], dict(base, run_id='C', start={'x': 0, 'y': 50, 'z': 0}, route='+x 2000')]
    assert validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=touching, components=[]))) == []
    close = [crossing[0], dict(base, run_id='C', start={'x': 0, 'y': 30, 'z': 0}, route='+x 2000')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=close, components=[])))
    assert len(errors) == 1 and 'se sobrepõem em 2,0' in errors[0] and ('afaste os percursos' in errors[0])


def test_joints_tees_and_continuations_are_not_clashes():
    base = {'system': 'distribuicao', 'dn_mm': 50}
    runs = [dict(base, run_id='A', start={'x': 0, 'y': 0, 'z': 0}, route='+x 2000; +y 1000; sobe 500'), dict(base, run_id='B', route='+x 1000'), dict(base, run_id='C', start={'x': 1000, 'y': 0, 'z': 0}, route='-y 800')]
    assert validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=runs, components=[]))) == []
    folded = [dict(base, run_id='D', start={'x': 0, 'y': 0, 'z': 0}, route='+x 2000; -x 1000')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=folded, components=[])))
    assert errors == ['Trecho D volta sobre si mesmo em 1,00 m perto de x 1,48 · y 0,00 · cota 0,00 m (segmentos 1 e 2); afaste os percursos.']


def test_connection_ports_follow_the_component_envelope():
    from triton.core.component_geometry import port_position
    rs = PIPE_NETWORK_COMPONENTS[2]
    assert port_position(rs, None) == (4500, 2000, 6500)
    assert port_position(rs, 'topo') == (4500, 2000, 7200)
    assert port_position(rs, 'sup+x') == pytest.approx((5100, 2000, 6500 + 0.85 * 700))
    rotated = dict(PIPE_NETWORK_COMPONENTS[1], rotation_deg=90)
    assert port_position(rotated, 'inf+x') == pytest.approx((1500, 300, 0.12 * 320))
    with pytest.raises(ValueError):
        port_position(rs, 'lado')
    runs = [dict(PIPE_NETWORK_RUNS[0], end='B-01:meio')]
    errors = validate_bim_manifest(build_bim_manifest(_pipe_network_project(runs=runs)))
    assert errors and "ponto de conexão 'meio' desconhecido" in errors[0]


def test_schematic_keeps_close_parallel_pipes_apart_and_breaks_the_back_one():
    from triton.core.schematic_3d import _AxisScale
    plan = _AxisScale([0, 30, 5000], 1.0)
    assert plan(0) < plan(30) < plan(5000)
    svg = generate_project_svg_diagram(_pipe_network_project(), mode='plant_3d')
    assert svg.count('stroke="#ffffff" stroke-width="') >= 5


# ---- origem: tests/unit/test_study_layout.py

ARRANJO = ['FP-01', 'FF-01', 'CI-01', 'B-01', 'RS-01', 'FR-01', 'SF-01', 'VP-01', 'SN-01', 'RP-01', 'LS-01', 'RG-03', 'VR-01', 'RG-01', 'QC-01', 'SN-02', 'SN-03', 'RP-02', 'AG-01', 'HD-01', 'RG-02', 'VS-01', 'RG-05', 'RG-04', 'VR-02', 'PNP-01']


def test_generate_study_layout_creates_valid_bim_manifest():
    project_data = {'project_name': 'Edifício Residencial Teste', 'lower_vol': 8000.0, 'upper_vol': 2000.0, 'area': 250.0, 'discard': 2.0, 'floors': 3}
    layout = generate_study_layout(project_data)
    comp_ids = [c['instance_id'] for c in layout['bim_components']]
    assert comp_ids == ARRANJO
    assert len(layout['pipe_runs']) == 19
    assert layout['building_volume']['floors'] == 3
    ff_comp = next((c for c in layout['bim_components'] if c['instance_id'] == 'FF-01'))
    assert ff_comp['parameters']['VOLUME_L'] == 500.0
    assert ff_comp['parameters']['DESCARTE_MM'] == 2.0
    fp_comp = next((c for c in layout['bim_components'] if c['instance_id'] == 'FP-01'))
    assert fp_comp['parameters']['DN_MM'] == 150.0
    assert fp_comp['parameters']['MALHA_MM'] == 0.35
    pump_comp = next((c for c in layout['bim_components'] if c['instance_id'] == 'B-01'))
    assert pump_comp['parameters']['POTENCIA_KW'] > 0
    assert pump_comp['parameters']['VAZAO_L_MIN'] > 0
    full_project = dict(project_data, **layout)
    manifest = build_bim_manifest(full_project)
    errors = validate_bim_manifest(manifest)
    assert errors == []
    assert manifest['validation']['warnings'] == []
    scene = build_volumetry(full_project)
    assert len(scene.solids) > 12
    pump_solid = next((s for s in scene.solids if s.key == 'B-01'))
    assert any(('Potência nominal' in line for line in pump_solid.info))
    assert any(('Vazão de operação' in line for line in pump_solid.info))
    assert any(('Forchheimer' in line for line in pump_solid.info))
    ff_solid = next((s for s in scene.solids if s.key == 'FF-01'))
    assert any(('Volume de descarte calculado' in line for line in ff_solid.info))
    fp_solid = next((s for s in scene.solids if s.key == 'FP-01'))
    assert any(('Malha filtrante' in line for line in fp_solid.info))
    svg = generate_schematic_3d_svg(full_project)
    assert 'Esquema 3D da tubulação' in svg
    assert 'CI-01' in svg and 'RS-01' in svg and ('FP-01' in svg) and ('FF-01' in svg)


@pytest.mark.parametrize('volume, area, pavimentos, caixa', [(1500, 60, 1, 500), (5000, 150, 2, 1000), (10000, 180, 3, 1000), (30000, 400, 6, 3000), (2000, 400, 1, 3000)])
def test_o_arranjo_normativo_fecha_sem_erros_nem_avisos(volume, area, pavimentos, caixa):
    """Da cisterna pequena ao prédio: todo trecho chega onde declara, sem colisão."""
    layout = generate_study_layout({'lower_vol': volume, 'area': area, 'floors': pavimentos, 'upper_vol': caixa})
    manifest = build_bim_manifest({'project_name': 'Grade', **layout})
    assert validate_bim_manifest(manifest) == []
    assert manifest['validation']['warnings'] == []


def test_o_arranjo_tem_o_que_a_instalacao_pede():
    """Freio d'água, sucção flutuante, extravasor, retenção e o backup potável."""
    layout = generate_study_layout({'lower_vol': 10000, 'area': 180, 'floors': 2})
    tipos = {c['instance_id']: c['type_id'] for c in layout['bim_components']}
    trechos = {r['run_id']: r for r in layout['pipe_runs']}
    assert tipos['FR-01'] == 'freio_dagua' and trechos['T-03']['end'] == 'FR-01:topo'
    assert tipos['SF-01'] == 'succao_flutuante' and tipos['VP-01'] == 'valvula_pe_crivo'
    assert trechos['T-04']['start'] == 'VP-01:topo'
    assert [trechos[t]['start'] for t in ('T-05', 'T-06', 'T-07', 'T-08')] == ['RG-03', 'B-01', 'VR-01', 'RG-01']
    assert tipos['RG-03'] == tipos['RG-01'] == 'registro_gaveta' and tipos['VR-01'] == 'valvula_retencao'
    assert trechos['T-11']['end'] == 'LS-01:sup+y' and trechos['T-12']['end'] == 'VR-02'
    assert trechos['T-09']['start'] == 'RS-01:inf-y' and trechos['T-09']['end'] == 'RG-05'
    assert trechos['T-10']['end'] == 'PNP-01:topo'
    assert trechos['T-14']['start'] == 'RS-01:sup+y' and trechos['T-14']['system'] == 'extravasor'
    assert trechos['T-15']['start'] == 'RS-01:inf+x' and trechos['T-15']['end'] == 'RG-04'
    assert tipos['RP-01'] == tipos['RP-02'] == 'respiro' and tipos['QC-01'] == 'quadro_comando'
    potavel = [r for r in layout['pipe_runs'] if r['system'] == 'alimentacao_potavel']
    assert [r['start'] for r in potavel] == ['HD-01', 'RG-02', 'VS-01']
    assert potavel[-1]['end'] == 'AG-01:topo' and tipos['VS-01'] == 'valvula_solenoide'
    assert tipos['SN-01'] == tipos['SN-02'] == tipos['SN-03'] == 'sensor_nivel'
    cota = {c['instance_id']: c['position_mm']['z'] for c in layout['bim_components']}
    assert cota['SN-03'] < cota['SN-02']


@pytest.mark.parametrize('rotulo, cv, kw', [('1/2', 0.5, 0.37), ('3/4', 0.75, 0.55), ('1', 1.0, 0.75), ('1 1/2', 1.5, 1.1), ('1.1/2', 1.5, 1.1), ('1/3', 1 / 3, 0.25), ('2 CV', 2.0, 1.5), ('', 0.5, 0.37)])
def test_o_rotulo_da_bomba_vira_a_potencia_certa(rotulo, cv, kw):
    """«1 1/2» era lido como ½ CV, e «1/3» como 1 CV (teste por substring)."""
    from triton.core.study_layout import potencia_da_motobomba
    assert potencia_da_motobomba(rotulo) == (pytest.approx(cv), pytest.approx(kw))


def test_o_kw_informado_prevalece_sobre_o_rotulo():
    from triton.core.study_layout import potencia_da_motobomba
    assert potencia_da_motobomba('1/2', 0.55)[1] == pytest.approx(0.55)


def test_a_captacao_nasce_no_telhado_e_desce_no_filtro():
    """O trecho do telhado começava no ar, além do filtro, apontando para fora."""
    layout = generate_study_layout({'lower_vol': 10000, 'area': 180, 'floors': 3})
    predio = layout['building_volume']
    t01 = next((r for r in layout['pipe_runs'] if r['run_id'] == 'T-01'))
    inicio = t01['start']
    assert inicio['z'] == pytest.approx(predio['height_mm'])
    assert 0 < inicio['x'] < predio['width_mm'] and 0 < inicio['y'] < predio['depth_mm']
    filtro = next((c for c in layout['bim_components'] if c['instance_id'] == 'FP-01'))['position_mm']
    assert filtro['x'] < 0 < inicio['x']
    cena = build_volumetry({'project_name': 'Telhado', **layout})
    assert any((s.key.startswith('T-01#') for s in cena.solids))


# ---- origem: tests/unit/test_volumetry.py

VOLUMETRY_COMPONENTS = [{'instance_id': 'CI-01', 'type_id': 'cisterna_inferior', 'position_mm': {'x': 0, 'y': 0, 'z': -1500}}, {'instance_id': 'B-01', 'type_id': 'motobomba', 'position_mm': {'x': 1500, 'y': 0, 'z': 0}, 'rotation_deg': 30}, {'instance_id': 'RS-01', 'type_id': 'reservatorio_superior', 'position_mm': {'x': 4500, 'y': 2000, 'z': 6500}, 'parameters': {'CAPACIDADE_L': 1000, 'DIAMETRO_MM': 1400, 'ALTURA_MM': 800}}]


VOLUMETRY_RUNS = [{'run_id': 'T-01', 'system': 'succao', 'dn_mm': 32, 'start': 'CI-01', 'route': 'sobe 1500; +x 1500', 'end': 'B-01'}, {'run_id': 'T-02', 'system': 'recalque', 'dn_mm': 25, 'route': '+x 3000; +y 2000; sobe 6500', 'end': 'RS-01'}]


BUILDING = {'origin_mm': {'x': -1000, 'y': -3000, 'z': 0}, 'width_mm': 8000, 'depth_mm': 7000, 'height_mm': 6000, 'floors': 2}


def _volumetry_project(**extra):
    data = {'project_name': 'Casa 3D', 'lower_vol': 5000, 'upper_vol': 500, 'bim_components': VOLUMETRY_COMPONENTS, 'pipe_runs': VOLUMETRY_RUNS, 'building_volume': BUILDING}
    data.update(extra)
    return data


def _outward(faces):
    pts = [p for f in faces for p in f]
    center = [sum(c) / len(pts) for c in zip(*pts)]
    for face in faces:
        n = face_normal(face)
        fc = [sum(c) / len(face) for c in zip(*face)]
        if sum((a * (b - c) for a, b, c in zip(n, fc, center))) <= 0:
            return False
    return True


def test_primitives_are_closed_with_outward_normals():
    assert _outward(prism(regular_polygon(900, 32), (0, 0, 0), 1800))
    assert _outward(prism([(300, 0), (0, 200), (-300, 0), (0, -200)], (10, 20, 30), 320, rotation_deg=45))
    for a, b in (((0, 0, 0), (3000, 0, 0)), ((0, 0, 0), (0, 0, -2000)), ((0, 0, 0), (1000, 2000, -30))):
        faces = tube(a, b, 50)
        assert len(faces) == 10 and _outward(faces)


def test_tank_dimensions_reproduce_the_capacity_or_keep_given_measures():
    d, h, capacity, estimated = tank_dimensions_mm('cisterna_inferior', {}, 5000)
    assert estimated and capacity == 5000 and (h == pytest.approx(d))
    assert math.pi * d ** 2 / 4 * h == pytest.approx(5000000000.0)
    d, h, _, estimated = tank_dimensions_mm('reservatorio_superior', {'CAPACIDADE_L': '500'}, 9999)
    assert estimated and h == pytest.approx(0.55 * d) and (math.pi * d ** 2 / 4 * h == pytest.approx(500000000.0))
    assert tank_dimensions_mm('reservatorio_superior', {'DIAMETRO_MM': 1400, 'ALTURA_MM': 800}, 1)[:2] == (1400, 800)
    d, h, _, _ = tank_dimensions_mm('cisterna_inferior', {'DIAMETRO_MM': 2000}, 10000)
    assert d == 2000 and math.pi * d ** 2 / 4 * h == pytest.approx(10000000000.0)


def test_scene_uses_the_expected_volumes_and_declares_estimates():
    scene = build_volumetry(_volumetry_project())
    by_key = {s.key: s for s in scene.solids}
    assert by_key['CI-01'].kind == 'tank' and len(by_key['CI-01'].faces) == 34
    assert any(('estimado' in line for line in by_key['CI-01'].info))
    assert not any(('estimado' in line for line in by_key['RS-01'].info))
    zs = [p[2] for f in by_key['RS-01'].faces for p in f]
    assert (min(zs), max(zs)) == (6500, 7300)
    pump_xy = {(round(p[0]), round(p[1])) for f in by_key['B-01'].faces for p in f}
    assert len(pump_xy) == 4
    assert by_key['EDIFICACAO'].opacity < 0.5 and 'LAJE-1' in by_key
    assert [s.key for s in scene.solids if s.kind == 'pipe' and s.pickable] == ['T-01#1', 'T-01#2', 'T-02#1', 'T-02#2', 'T-02#3']
    assert scene.solids[0].kind == 'ground'
    assert any(('ampliada' in n for n in scene.notes))


def test_scene_without_building_or_with_invalid_layout():
    scene = build_volumetry(_volumetry_project(building_volume={'width_mm': 0}))
    assert not any((s.kind == 'building' for s in scene.solids))
    with pytest.raises(ValueError, match='falta'):
        build_volumetry(_volumetry_project(pipe_runs=[dict(VOLUMETRY_RUNS[0], route='sobe 1500')]))


def test_glb_is_structurally_valid_gltf(tmp_path):
    path = write_glb(build_volumetry(_volumetry_project()), str(tmp_path / 'v.glb'))
    data = open(path, 'rb').read()
    magic, version, total = struct.unpack_from('<4sII', data)
    assert (magic, version, total) == (b'glTF', 2, len(data))
    json_len, json_type = struct.unpack_from('<I4s', data, 12)
    assert json_type == b'JSON' and json_len % 4 == 0
    doc = json.loads(data[20:20 + json_len])
    bin_len, bin_type = struct.unpack_from('<I4s', data, 20 + json_len)
    assert bin_type == b'BIN\x00' and bin_len == doc['buffers'][0]['byteLength'] and (bin_len % 4 == 0)
    for acc in doc['accessors']:
        view = doc['bufferViews'][acc['bufferView']]
        assert view['byteLength'] == acc['count'] * 12 and view['byteOffset'] % 4 == 0
        assert view['byteOffset'] + view['byteLength'] <= bin_len
    names = [n['name'] for n in doc['nodes']]
    assert 'CI-01' in names and 'T-02#3' in names
    assert doc['nodes'][names.index('RS-01')]['extras']['titulo'].startswith('RS-01')
    blend = [m for m in doc['materials'] if m.get('alphaMode') == 'BLEND']
    assert blend and all((m['pbrMetallicRoughness']['baseColorFactor'][3] < 1 for m in blend))


def test_html_viewer_is_self_contained_and_carries_the_scene(tmp_path):
    scene = build_volumetry(_volumetry_project(project_name='Casa </script> 3D'))
    html = open(write_html_viewer(scene, str(tmp_path / 'v.html')), encoding='utf-8').read()
    assert not re.search('(src|href)\\s*=\\s*["\']?https?:|@import|url\\(\\s*["\']?https?:|fetch\\(\\s*["\']https?:|from\\s*["\']https?:', html)
    assert html.count('</script>') == 1
    payload = re.search('const SCENE = (\\{.*?\\});\\n', html, re.S).group(1)
    data = json.loads(payload.replace('<\\/', '</'))
    assert data['title'] == 'Casa </script> 3D'
    assert {s['key'] for s in data['solids']} >= {'CI-01', 'B-01', 'RS-01', 'EDIFICACAO', 'TERRENO'}
    tank = next((s for s in data['solids'] if s['key'] == 'CI-01'))
    assert len(tank['tris']) == len(tank['norms']) and len(tank['tris']) % 9 == 0
    assert scene_payload(scene)['bounds'][0][2] == pytest.approx(-1.5)
    assert 'TritonVolumetria.mount(' in html
    sky = re.search('const SKY = "([A-Za-z0-9+/=]*)";', html).group(1)
    assert base64.b64decode(sky)[:10] == b'#?RADIANCE'


# ---- origem: tests/unit/test_cad_exporter.py

PROJECT = {'project_name': 'Edifício Residencial Teste', 'ref_code': 'N5-2026-CAD-TEST', 'organization': 'Escritório Exemplo', 'technical_responsible': 'Responsável a validar — CREA 000000', 'area': 250.0, 'runoff': 0.85, 'discard': 2.0, 'lower_vol': 10000.0, 'upper_vol': 1000.0, 'tot_demand': 2500.0, 'share': 0.45, 'potential_pct': 48.0, 'audit_context': {'climate_location': 'Florianópolis / SC'}}


def _read_clean(path):
    doc = ezdxf.readfile(path)
    auditor = doc.audit()
    assert not auditor.errors
    return doc


def test_generate_technical_a3_dxf(tmp_path):
    output = tmp_path / 'technical.dxf'
    generate_project_dxf(PROJECT, str(output), mode='technical_a3')
    doc = _read_clean(output)
    assert doc.dxfversion == 'AC1032'
    assert doc.header['$INSUNITS'] == 4
    assert {'00_folha_e_margem', '00_selo', '06_equipamentos', '08_cotas'} <= set(doc.layers.entries)
    text = ' '.join((entity.dxf.text for entity in doc.modelspace().query('TEXT')))
    assert 'ESCRITÓRIO EXEMPLO' in text
    assert 'Responsável a validar' in text
    assert '250,0 m²' in text
    assert '10.000 Litros' in text
    assert 'UNIVERSIDADE FEDERAL' not in text
    assert 'i = ___%' in text
    assert 'i = 30%' not in text
    assert 'Cisterna: 10.000 L' in text
    assert 'Economia Estimada:' not in text
    texts_list = [e.dxf.text for e in doc.modelspace().query('TEXT')]
    assert 'Sucção' in texts_list
    assert any((t.startswith('DN ') for t in texts_list))
    assert 'Recalque' in texts_list
    assert 'DISTRIBUIÇÃO NÃO POTÁVEL' in texts_list
    assert not any(('DISTRIBUIÇÃO DN' in t for t in texts_list))
    assert 'BACKUP POTÁVEL (AIR-GAP >= 50 mm)' in text
    inserts = [e.dxf.name for e in doc.modelspace().query('INSERT')]
    assert 'SIMBOLO_NORTE' not in inserts


def test_generate_simple_dxf_and_svg(tmp_path):
    output = tmp_path / 'simple.dxf'
    generate_project_dxf(PROJECT, str(output), mode='simple')
    doc = _read_clean(output)
    assert doc.header['$INSUNITS'] == 4
    text = ' '.join((entity.dxf.text for entity in doc.modelspace().query('TEXT')))
    assert 'ESQUEMA UNIFILAR' in text
    assert 'Escritório Exemplo' in text
    svg = generate_project_svg_diagram(PROJECT, mode='simple')
    assert '<svg' in svg and 'Escritório Exemplo' in svg
    assert 'Igor Catão' not in svg


def test_share_is_a_fraction_and_percent_is_refused():
    data = dict(PROJECT)
    with pytest.raises(ValueError, match='percentual'):
        generate_project_svg_diagram({**data, 'share': 45.0}, mode='technical_a3')
    data['share'] = 0.45
    data['audit_context'] = None
    svg = generate_project_svg_diagram(data, mode='technical_a3')
    assert '1.125 L/dia (45%)' in svg
    assert 'NÃO INFORMADA' in svg


def test_block_library_is_reusable_and_auditable(tmp_path):
    output = tmp_path / 'biblioteca.dxf'
    generate_project_dxf(PROJECT, str(output), mode='block_library')
    doc = _read_clean(output)
    names = set(doc.blocks.block_names())
    expected = {'triton_cisterna_planta', 'triton_res_sup_planta', 'triton_filtro_pluvial', 'triton_first_flush', 'triton_motobomba', 'triton_reg_gaveta', 'triton_reg_esfera', 'triton_valv_retencao', 'triton_air_gap', 'triton_ladrao_sifonado', 'triton_ponto_nao_potavel', 'triton_freio_dagua', 'triton_succao_flutuante', 'triton_sensor_nivel', 'triton_valv_solenoide', 'triton_hidrometro', 'triton_valv_pe_crivo', 'triton_respiro', 'triton_quadro_comando'}
    assert expected <= names
    assert len(doc.modelspace().query('INSERT')) == len(expected)
    for name in expected:
        entities = list(doc.blocks.get(name))
        assert any((entity.dxftype() == 'ATTDEF' for entity in entities))
        assert all((entity.dxf.layer == '0' for entity in entities))
    for insert in doc.modelspace().query('INSERT'):
        assert insert.has_xdata('TRITON')
    manifest_path = output.with_name('biblioteca_triton-bim.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert manifest['schema_version'] == '1.1'
    assert manifest['pipe_runs'] == []
    assert len(manifest['component_types']) == 19
    assert manifest['instances'] == []
    assert validate_bim_manifest(manifest) == []


def test_bim_manifest_preserves_explicit_placements():
    data = dict(PROJECT)
    data['bim_components'] = [{'instance_id': 'CI-01', 'type_id': 'cisterna_inferior', 'level': 'Térreo', 'position_mm': {'x': 12500, 'y': 8200, 'z': 0}, 'rotation_deg': 90, 'parameters': {'CAPACIDADE_L': 10000}}]
    manifest = build_bim_manifest(data)
    assert manifest['instances'][0]['position_mm']['x'] == 12500.0
    assert manifest['instances'][0]['parameters']['CAPACIDADE_L'] == 10000
    assert validate_bim_manifest(manifest) == []


def test_invalid_cad_mode_is_rejected(tmp_path):
    try:
        generate_project_dxf(PROJECT, str(tmp_path / 'bad.dxf'), mode='unknown')
    except ValueError as error:
        assert 'Modo CAD inválido' in str(error)
    else:
        raise AssertionError('Modo desconhecido deveria ser rejeitado')


def test_forchheimer_calculation_and_materials_list(tmp_path):
    from triton.core.cad_exporter import calculate_forchheimer_pumping_diameters
    calc = calculate_forchheimer_pumping_diameters(pump_flow_rate_m3_h=3.6, daily_pumped_volume_l=2500.0, pump_hp='3/4')
    assert calc['dn_rec'] in (25, 32, 40)
    assert calc['dn_suc'] > calc['dn_rec']
    assert calc['v_rec'] < 2.5
    assert calc['v_suc'] < 1.5
    output = tmp_path / 'prancha_forchheimer.dxf'
    generate_project_dxf(PROJECT, str(output), mode='technical_a3')
    doc = _read_clean(output)
    text = ' '.join((entity.dxf.text for entity in doc.modelspace().query('TEXT')))
    assert 'Conf. Projeto' in text
    assert 'ECONÔMICO' in text or 'Econômico' in text
    assert 'Recalque' in text
    assert 'Sucção' in text or 'SUCÇÃO' in text
    svg = generate_project_svg_diagram(PROJECT, mode='technical_a3')
    assert 'Conf. Projeto' in svg
    assert 'ECONÔMICO' in svg or 'Econômico' in svg
    assert 'Recalque' in svg
    assert 'Sucção' in svg or 'SUCÇÃO' in svg


# ==================================================================================================
# Edições: português de Portugal (Edição IBE)
# ==================================================================================================

@pytest.mark.parametrize('brasil, portugal', [
    ('Valor Presente Líquido (VPL)', 'Valor Atual Líquido (VAL)'),
    ('Salvar arquivo', 'Guardar ficheiro'),
    ('ANÁLISE ECONÔMICA', 'ANÁLISE ECONÓMICA'),
    ('Na tela de resultados, o prestador cobra a tarifa de esgoto', 'No ecrã de resultados, a entidade gestora cobra a tarifa de saneamento'),
    ('A caixa superior recebe a água', 'O reservatório superior recebe a água'),
    ('Faixas tarifárias da concessionária', 'Escalões tarifários da entidade gestora'),
])
def test_glossario_de_portugal_troca_o_vocabulario_com_concordancia(brasil, portugal):
    from triton.ui.portugues_de_portugal import para_portugal
    assert para_portugal(brasil) == portugal


@pytest.mark.parametrize('texto', [
    'Payback descontado e TIR',           # termos técnicos não mudam
    'Esgotamento das reservas',           # «esgot» dentro de outra palavra não é «esgoto»
    'Telas e telhados',                   # fronteira de palavra: «telhados» fica
    '',
])
def test_glossario_de_portugal_respeita_a_fronteira_de_palavra(texto):
    from triton.ui.portugues_de_portugal import para_portugal
    esperado = {'Telas e telhados': 'Ecrãs e telhados'}.get(texto, texto)
    assert para_portugal(texto) == esperado


def test_edicao_portugal_pede_dados_de_portugal_e_nao_do_brasil(monkeypatch):
    from triton.core import edition as E
    monkeypatch.setenv('TRITON_EDITION', 'IBE')
    assert E.is_ibe_edition() and E.usa_dados_de_portugal() and not E.usa_dados_do_brasil()
    assert E.rotulo_da_edicao() == 'Edição Ibérica (IBE)' and E.rotulo_da_edicao(curto=True) == 'IBE'
    assert E.get_edition_currency_symbol() == '€'
    assert E.manual_do_usuario('pt') == E.MANUAL_PT
    monkeypatch.setenv('TRITON_EDITION', 'XYZ')
    assert E.get_current_edition() == 'BRL'  # edição desconhecida cai na Brasil, como antes
    with pytest.raises(ValueError):
        E.set_current_edition('ESP')


# ---------------------------------------------------------------------------
# Edição Ibérica: base E-OBS por concelho (data/portugal_eobs.db)
# ---------------------------------------------------------------------------

def _base_portugal():
    from triton.core import base_climatica_portugal as pt
    if not pt.disponivel():
        pytest.skip("data/portugal_eobs.db ausente")
    return pt


def test_base_portugal_lisboa_normal_completa_e_plausivel():
    pt = _base_portugal()
    p, ini, fim, total, n, ident = pt.carregar_serie("Lisboa", pt.INICIO_PADRAO, pt.FIM_PADRAO)
    assert (ini, fim) == ("01/01/1991", "31/12/2020") and n == len(p) == 10958
    assert ident.startswith("E-OBS v33.0e/") and not np.isnan(p).any() and (p >= 0).all()
    assert 500 < p.sum() / 30 < 1000  # mm/ano


def test_base_portugal_so_serve_concelho_sem_falha():
    """Ilhas sem cobertura (Açores fora do domínio, Madeira com falhas) não ganham série."""
    pt = _base_portugal()
    fora = {c["concelho"]: c["motivo"] for c in pt.nao_cobertos()}
    assert "Funchal" in fora and "Ponta Delgada" in fora and "Funchal" not in pt.concelhos()
    assert len(pt.concelhos()) == 278 and "Lisboa" in pt.concelhos("Lisboa")
    meta = pt.metadados()
    assert "10.1029/2017JD028200" in meta["citacao"] and "completude" in meta


def test_projeto_com_chuva_da_e_obs_guarda_referencia_e_relê_igual_na_cli(tmp_path):
    """Interface e CLI recompõem a mesma série E-OBS a partir da referência gravada."""
    pt = _base_portugal()
    from triton import cli
    cfg = TritonConfig()
    cfg.climate_source_mode = 'national_db'
    cfg.climate_city_uf, cfg.climate_city_name = ('Faro', 'Faro')
    cfg.climate_model, cfg.climate_scenario = (pt.MODELO_EOBS, pt.CENARIO_EOBS)
    cfg.climate_start_date, cfg.climate_end_date = ('01/01/2001', '31/12/2010')
    cfg.start_date = '01/01/2001'
    serie = serie_da_climbra(cfg)
    destino = tmp_path / 'faro.triton'
    export_triton_json(cfg, str(destino), precip_data=serie)
    chuva = json.loads(destino.read_text(encoding='utf-8'))['rainfall']
    # Chuva E-OBS: a referência e o pacote são gravados e, por padrão, a série vai junto (reprodutibilidade).
    assert chuva['climbra_series']['origem'] == 'E-OBS (Portugal)' and len(chuva['precipitation_mm']) == len(serie)
    assert chuva['pacote_chuva']['pacote_id'] == pt.metadados()['pacote_id']
    proj = load_triton_project(str(destino))
    assert proj.get('chuva_da_climbra') and not proj.get('aviso_chuva')
    assert np.array_equal(proj['precip_data'], serie) and len(serie) == 3652
    assert np.array_equal(cli._load_bundle(str(destino))['precip_data'], serie)


# ---------------------------------------------------------------------------
# Edição Ibérica: a fatura (água, saneamento, resíduos, TRH, IVA) nos campos do motor
# ---------------------------------------------------------------------------

def _fatura_sintetica():
    """Valores sintéticos, só para o teste de equivalência (não são de nenhuma entidade)."""
    from triton.core.fatura_portuguesa import Escalao, FaturaPortuguesa, Parcela
    return FaturaPortuguesa(
        entidade='teste', concelho='teste', fixa_agua=4.0, iva_agua_pct=6.0,
        escaloes=[Escalao(0, 5, 0.6), Escalao(5, 15, 1.2), Escalao(15, 25, 2.5), Escalao(25, None, 4.0)],
        parcelas=[Parcela('saneamento', fixa=3.0, por_m3=0.9, iva_pct=6.0),
                  Parcela('resíduos', fixa=2.5, por_m3=0.7, iva_pct=6.0),
                  Parcela('TRH', por_m3=0.05)])


def _fatura_sintetica_com_saneamento_por_escaloes():
    """Saneamento por escalões sobre 90% do volume, com TRH e IVA próprio (sintético)."""
    from triton.core.fatura_portuguesa import Escalao
    f = _fatura_sintetica()
    f.parcelas = [p for p in f.parcelas if p.nome != 'saneamento']
    f.saneamento_escaloes = [Escalao(0, 5, 0.2), Escalao(5, 15, 0.6), Escalao(15, 25, 1.4), Escalao(25, None, 1.7)]
    f.saneamento_fixa, f.saneamento_trh_m3, f.coef_recolha, f.iva_saneamento_pct = 3.0, 0.03, 0.9, 6.0
    return f


@pytest.mark.parametrize('m3', [0.0, 3.0, 5.0, 5.5, 12.5, 16.7, 25.0, 27.8, 40.0])
def test_motor_reproduz_a_fatura_portuguesa(m3):
    from triton.core.economic import calculate_water_bill
    from triton.core.fatura_portuguesa import campos_do_motor, conta_mensal
    for f in (_fatura_sintetica(), _fatura_sintetica_com_saneamento_por_escaloes()):
        c = campos_do_motor(f)
        conta = calculate_water_bill(m3 * 1000.0, c['tariffs'], c['sewage_mode'], c['sewage_rate'],
                                     c['water_tax_fixed'], c['water_tax_var'],
                                     sewage_tariffs=c['sewage_tariffs'], sewage_volume_factor=c['sewage_volume_factor'])
        assert conta == pytest.approx(conta_mensal(f, m3), abs=1e-9)


def test_economia_da_fatura_portuguesa_nao_conta_as_tarifas_fixas():
    from triton.core.economic import calculate_effective_tariff
    from triton.core.fatura_portuguesa import aplicar_ao_projeto, conta_mensal
    f = _fatura_sintetica()
    cfg = TritonConfig()
    aplicar_ao_projeto(f, cfg)
    cfg.tariff_start_date = ''
    agua, outras = calculate_effective_tariff(cfg, annual_m3_saved=60.0, annual_total_demand_m3=240.0)
    # 20 → 15 m³/mês: tudo no 3.º escalão (15–25 m³); as fixas se anulam.
    assert agua == pytest.approx(2.5 * 1.06)
    assert outras == pytest.approx(0.9 * 1.06 + 0.7 * 1.06 + 0.05)
    assert (agua + outras) * 5 == pytest.approx(conta_mensal(f, 20) - conta_mensal(f, 15))


def test_fatura_portuguesa_recusa_escaloes_com_buraco():
    from triton.core.fatura_portuguesa import Escalao, campos_do_motor
    f = _fatura_sintetica()
    f.escaloes = [Escalao(0, 5, 0.6), Escalao(6, None, 1.0)]
    with pytest.raises(ValueError, match='salto'):
        campos_do_motor(f)
    f.escaloes = [Escalao(0, 5, 0.6)]
    with pytest.raises(ValueError, match='sem limite'):
        campos_do_motor(f)


@pytest.mark.parametrize('concelho', __import__('triton.core.tarifarios_portugal', fromlist=['x']).concelhos())
def test_tarifario_portugues_reproduz_as_contas_impressas(concelho):
    """Fatura e motor reproduzem cada conta de conferência feita com os números do documento."""
    from triton.core import tarifarios_portugal as T
    from triton.core.economic import calculate_water_bill, esgoto_do_projeto
    from triton.core.fatura_portuguesa import conta_mensal
    f = T.fatura(concelho)
    cfg = TritonConfig()
    assert T.aplicar(concelho, cfg) and cfg.tariff_vigencia
    for c in T.carregar()[concelho]['conferencia']:
        assert conta_mensal(f, c['m3']) == pytest.approx(c['conta'], abs=5e-4)
        motor = calculate_water_bill(c['m3'] * 1000.0, cfg.water_tariffs, cfg.sewage_mode, cfg.sewage_rate,
                                     cfg.water_tax_fixed, cfg.water_tax_var, **esgoto_do_projeto(cfg))
        assert motor == pytest.approx(c['conta'], abs=5e-4)


def test_esgoto_por_escaloes_sobrevive_ao_arquivo_e_entra_na_economia(tmp_path):
    from triton.core import tarifarios_portugal as T
    from triton.core.economic import calculate_effective_tariff
    cfg = TritonConfig()
    assert T.aplicar('Lisboa', cfg)
    destino = tmp_path / 'l.triton'
    export_triton_json(cfg, str(destino), precip_data=np.zeros(365))
    lido = load_triton_project(str(destino))['config']
    assert lido.sewage_mode == 3 and lido.sewage_volume_factor == 0.9
    assert [tuple(f) for f in lido.sewage_tariffs] == [tuple(f) for f in cfg.sewage_tariffs]
    agua, esgoto = calculate_effective_tariff(lido, annual_m3_saved=36.0, annual_total_demand_m3=180.0)
    assert agua > 0 and esgoto > 0  # 15 → 12 m³/mês: o saneamento também deixa de ser cobrado



def test_cli_importa_sem_console():
    """No executável de janela, sys.stdout é None; importar a CLI não pode derrubar a interface."""
    import subprocess
    import sys as _sys
    pasta_edicao = str(Path(__file__).resolve().parent.parent)
    codigo = "import sys; sys.stdout = None; import triton.cli; sys.stderr.write('ok')"
    r = subprocess.run([_sys.executable, "-c", codigo], cwd=pasta_edicao, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0 and r.stderr.endswith('ok'), r.stderr[-800:]


def test_planilha_de_dados_le_os_resultados_calculados(planilha):
    """As abas 1–6 leem os objetos de resultado; nada de tabela fixa nem estimativa."""
    _, wb = planilha
    resumo = {l[0]: l[1] for l in wb['1_Resumo_Projeto'].iter_rows(min_row=3, values_only=True) if l[0]}
    vpl = float(next(v for k, v in resumo.items() if k.startswith('VPL')))
    aud = {l[0]: l[1] for l in wb['Auditoria_Economia'].iter_rows(values_only=True) if l and l[0]}
    assert vpl == pytest.approx(float(aud['vpl']), abs=0.01)
    assert wb['2_Balanco_Hidrico_Diario'].max_row == 730 + 1  # um dia por linha
    fluxo = list(wb['4_Fluxo_Caixa_Economico'].iter_rows(min_row=2, values_only=True))
    assert len(fluxo) > 12 and fluxo[-1][-1] is not None  # fluxo mensal real, não o de TMA fixa
    acv = [l[0] for l in wb['5_Inventario_ACV_ESG'].iter_rows(min_row=2, values_only=True)]
    assert 'Cisterna Inferior (Polietileno)' not in acv or len(acv) != 7  # não é a tabela fixa antiga
    assert len(acv) == len([n for n in wb.sheetnames if n.startswith('Auditoria_Ambi·')] and
                           list(wb[next(n for n in wb.sheetnames if n.startswith('Auditoria_Ambi·'))].iter_rows(min_row=2)))
    # sem varredura nem multicritério calculados: as abas dizem isso, sem números inventados
    assert 'volume fixo' in str(wb['3_Curva_Varredura_Volumes']['A2'].value)
    assert 'Não calculado' in str(wb['6_Decisao_Multicriterio']['A2'].value)


# ---- Saídas (relatório PDF/HTML, JSON, CAD, CSV legado, CLI): o que aparece vem do cálculo

def _linha_hidrica(vol, pot):
    from types import SimpleNamespace as _NS
    return _NS(lower_tank_vol=vol, potential_potable_savings_pct=pot, avg_pluvial_consumed_l_day=pot * 2,
               avg_potable_consumed_l_day=100.0, avg_spilled_l_day=5.0, pct_days_full_satisfaction=60.0,
               pct_days_null_satisfaction=10.0, pct_days_partial_satisfaction=30.0, delta_potential_per_m3=1.0,
               annual_pluvial_consumed_m3=pot * 2 * 0.365, annual_spill_m3=1.8, annual_potable_consumed_m3=36.5)


def test_relatorio_le_a_economia_calculada_do_volume_e_nao_interpola():
    """O laudo lia «tab_economic.last_econ_res», que não existe: VPL, CAPEX e TIR saíam zero.

    E interpolava potencial e VPL para volumes não simulados. Agora: a varredura econômica,
    o último resultado (se for do volume), o otimizador; fora disso, None («Não calculado»).
    """
    from types import SimpleNamespace as _NS
    from triton.core.dados_do_relatorio import (CHAVES_ECONOMICAS, CHAVES_HIDRICAS, indicadores_economicos,
                                                indicadores_hidricos, volume_do_relatorio)
    sweep = _NS(results_by_volume=[_linha_hidrica(1000.0, 20.0), _linha_hidrica(2000.0, 30.0)],
                optimal_lower_tank_vol=1000.0)
    # volume: o ótimo econômico vence o técnico; o escolhido vence os dois; sem nada, None
    assert volume_do_relatorio(otimo_economico=2000.0, sweep=sweep) == 2000.0
    assert volume_do_relatorio(selecionado=1500.0, otimo_economico=2000.0, sweep=sweep) == 1500.0
    assert volume_do_relatorio(sweep=sweep) == 1000.0
    assert volume_do_relatorio() is None
    assert indicadores_hidricos(2000.0, sweep=sweep)["potential_pct"] == 30.0
    assert all(v is None for v in indicadores_hidricos(1500.0, sweep=sweep).values())  # nada de interpolar
    assert set(indicadores_hidricos(None)) == set(CHAVES_HIDRICAS)

    ultimo = run_robust_economic_analysis(initial_investment=6000.0, annual_water_saved_m3=40.0,
                                          water_tariff_per_m3=8.0, discount_rate=0.06, analysis_period_years=20)
    varredura = {2000.0: {"volume_l": 2000.0, "capex": 5000.0, "gross_monthly": 25.0, "vpl": 1234.5, "tir": 9.0,
                          "payback_simple": 8.0, "payback_discounted": 11.0}}
    e = indicadores_economicos(2000.0, varredura_economica=varredura)
    assert (e["capex"], e["annual_gross"], e["vpl"], e["payback_s"], e["payback_d"]) == (5000.0, 300.0, 1234.5, 8.0, 11.0)
    e = indicadores_economicos(3000.0, varredura_economica=varredura, ultimo=ultimo, volume_do_ultimo=3000.0)
    assert e["vpl"] == pytest.approx(ultimo.vpl) and e["capex"] == pytest.approx(6000.0)
    assert e["annual_gross"] == pytest.approx(ultimo.annual_cash_flows[1].total_gross_savings_brl)
    # mesmo volume na varredura e no último resultado: vale o que a Etapa 5 mostra (o último)
    varredura[3000.0] = dict(varredura[2000.0], volume_l=3000.0, vpl=-1.0)
    e = indicadores_economicos(3000.0, varredura_economica=varredura, ultimo=ultimo, volume_do_ultimo=3000.0)
    assert e["vpl"] == pytest.approx(ultimo.vpl)
    # o último resultado é de outro volume: não serve para este
    nada = indicadores_economicos(3000.0, ultimo=ultimo, volume_do_ultimo=4000.0)
    assert set(nada) == set(CHAVES_ECONOMICAS) and all(v is None for v in nada.values())
    # otimizador: sem payback simples (o dele é o descontado)
    cand = _NS(lower_tank_vol=2500.0, capex_brl=5500.0, vpl_brl=900.0, irr_pct=7.0, discounted_payback_years=12.0)
    e = indicadores_economicos(2500.0, topsis=_NS(candidates=[cand]))
    assert e["vpl"] == 900.0 and e["payback_s"] is None and e["payback_d"] == 12.0
    e = indicadores_economicos(2500.0, cenarios=[{"vol": 2500.0, "capex": 1.0, "gross_m": 10.0, "vpl": 2.0,
                                                  "tir": 3.0, "payback": 4.0, "payback_discounted": 5.0}])
    assert e["annual_gross"] == 120.0 and e["payback_s"] is None and e["payback_d"] == 5.0


def test_relatorio_pdf_sem_calculo_diz_nao_calculado_e_usa_a_moeda_do_projeto():
    """Os laudos traziam CAPEX 8.950, VPL 24.150 e TIR 34,2% inventados, «R$» e «20 anos» fixos."""
    pytest.importorskip('PySide6')
    import re as _re
    from triton.core.report_service import generate_report_html
    vazio = generate_report_html("economic", {}, lang="pt")
    texto = _re.sub(r"<[^>]+>", " ", vazio)
    assert "Não calculado" in texto
    for inventado in ("8.950", "24.150", "34,2", "3.240", "2.000 L"):
        assert inventado not in texto, inventado
    assert "comprovam a" not in texto  # parecer não afirma atratividade sem cálculo
    dados = {"moeda": "€", "lower_vol": 3000.0, "potential_pct": 40.0, "pluv_day": 100.0, "potable_day": 150.0,
             "spill_day": 20.0, "sat_full": 50.0, "sat_null": 10.0, "capex": 5000.0, "vpl": -200.0, "tir": 3.0,
             "annual_gross": 400.0, "payback_s": None, "payback_d": None,
             "audit_context": {"analysis_period_years": 25},
             "topsis_candidates": [{"volume": 3000.0, "saving": 40.0, "water_m3": 36.5, "capex": 5000.0,
                                    "vpl": -200.0, "co2": 10.0, "score": 1.0, "rank": 1, "is_best": True}]}
    for tipo in ("economic", "research"):
        html = _re.sub(r"<[^>]+>", " ", generate_report_html(tipo, dict(dados), lang="pt"))
        assert "€" in html and "R$" not in html, tipo
        assert "25 anos" in html or "25 Anos" in html, tipo
    executivo = _re.sub(r"<[^>]+>", " ", generate_report_html("economic", dict(dados), lang="pt"))
    assert "não se paga" in executivo and "Sem retorno" in executivo
    # o laudo ambiental não supõe 100 m³/ano sem consumo pluvial simulado
    amb = generate_report_html("environmental", {"lower_vol": 3000.0}, lang="pt")
    assert "Não calculado" in amb


def test_prancha_cad_nao_inventa_demanda_area_nem_potencial(tmp_path):
    """A prancha escrevia 1.000 L/dia (chave «tot_demand» que ninguém enviava), 150 m², 5.000 L
    e 42,5%, e dimensionava o recalque com a demanda inventada."""
    import ezdxf as _ezdxf
    from triton.core.cad_exporter import NAO_CALCULADO, NAO_INFORMADO, demanda_total_do_desenho, textos_do_quadro
    tx = textos_do_quadro({})
    assert tx["demanda"] == tx["area"] == tx["volume"] == NAO_INFORMADO and tx["potencial"] == NAO_CALCULADO
    assert demanda_total_do_desenho({"residents": 4, "demand": 150.0}) == 600.0
    assert demanda_total_do_desenho({}) is None
    for modo in ("technical_a3", "simple"):
        destino = tmp_path / f"{modo}.dxf"
        generate_project_dxf({}, str(destino), mode=modo)
        texto = " ".join(e.dxf.text for e in _ezdxf.readfile(str(destino)).modelspace().query("TEXT"))
        assert "1.000 L/dia" not in texto and "42,5" not in texto and "150,0 m²" not in texto, modo
        assert NAO_INFORMADO in texto or NAO_CALCULADO in texto, modo
    svg = tmp_path / "t.svg"
    generate_project_svg_diagram({"residents": 4, "demand": 150.0, "share": 0.5, "area": 120.0}, str(svg),
                                 mode="technical_a3")
    conteudo = svg.read_text(encoding="utf-8")
    assert "600 L/dia" in conteudo and "300 L/dia (50%)" in conteudo and "120,0 m²" in conteudo


def test_painel_da_motobomba_nao_supoe_800_litros_por_dia():
    from triton.core.volumetry import _component_solid_body
    item = {"type_id": "motobomba", "parameters": {}, "position_mm": {"x": 0.0, "y": 0.0, "z": 0.0},
            "instance_id": "MB-01"}
    info = " | ".join(_component_solid_body(item, {}).info)
    assert "800 L/dia" not in info and "Demanda diária bombeada: Não calculado" in info
    info = " | ".join(_component_solid_body(item, {"pluv_day": 450.0}).info)
    assert "450 L/dia" in info


def test_csv_legado_leva_a_simulacao_unica(tmp_path):
    """O botão do CSV legado chamava «export_legacy_csv», que a janela não tem; e o CSV só
    levava a varredura, nunca a simulação de um volume."""
    from types import SimpleNamespace as _NS
    from triton.core.dados_do_relatorio import resultados_para_csv_legado
    unica = _linha_hidrica(2500.0, 33.0)
    assert resultados_para_csv_legado(None, unica) == [unica]
    sweep = _linha_hidrica(1000.0, 20.0)
    assert resultados_para_csv_legado(_NS(results_by_volume=[sweep]), unica) == [sweep]
    destino = tmp_path / "legado.csv"
    export_netuno_csv(TritonConfig(), resultados_para_csv_legado(None, unica), str(destino))
    linhas = destino.read_text(encoding="latin1").splitlines()
    assert linhas[-1].startswith("2500;33")


def test_cli_declara_a_moeda_do_projeto_nas_saidas():
    """A CLI não dizia a moeda: em projeto em euro, «npv_brl» sem moeda e «R$» no texto da modulação."""
    from triton.core.dados_do_relatorio import moeda_do_projeto
    from triton.cli import _flat_rows, _render_html, _simbolo
    assert moeda_do_projeto({"stage3": {"currency_code": "EUR"}}) == {"code": "EUR", "symbol": "€"}
    assert moeda_do_projeto({"stage3": {"currency": 0}})["symbol"] == "R$"  # projeto antigo, só o índice
    assert moeda_do_projeto({}) is None
    rel = {"generated_at_utc": "agora",
           "provenance": {"currency": {"code": "EUR", "symbol": "€"}},
           "technical": {"alternatives": [{"lower_tank_volume_l": 1000.0, "potable_savings_pct": 20.0}]},
           "economic": {"alternatives": [{"lower_tank_volume_l": 1000.0, "npv_brl": 10.0}]}}
    assert _flat_rows(rel)[0]["currency"] == "EUR"
    assert "Valores monetários em: €" in _render_html(rel)
    assert _simbolo({"provenance": {}}) == "(moeda do projeto)"


def test_laudo_ambiental_so_mostra_selos_brasileiros_na_brasil(monkeypatch):
    """AQUA-HQE e Casa Azul são certificações brasileiras; a aba ambiental já os escondia
    fora da Brasil, e o laudo os mostrava nas três edições."""
    pytest.importorskip('PySide6')
    from triton.core.report_service import generate_report_html
    monkeypatch.setenv('TRITON_EDITION', 'BRL')
    assert 'AQUA-HQE Residencial' in generate_report_html("environmental", {}, lang="pt")
    for edicao in ('INT', 'IBE'):
        monkeypatch.setenv('TRITON_EDITION', edicao)
        html = generate_report_html("environmental", {}, lang="pt")
        assert 'AQUA-HQE Residencial' not in html and 'Casa Azul + CAIXA' not in html, edicao


def test_cli_sem_catalogo_nao_preenche_manutencoes_em_reais():
    """Paridade com a interface: fora do catálogo, as rotinas ficam a custo zero."""
    from triton.cli import _prefill_preliminary_capex
    cfg = TritonConfig()
    cfg.op_costs = []
    cfg.precos_de_catalogo = False
    _prefill_preliminary_capex(cfg)
    assert cfg.op_costs and all(fixo == 0 and variavel == 0 for _, _, fixo, variavel in cfg.op_costs)
    cfg = TritonConfig()
    cfg.op_costs = []
    _prefill_preliminary_capex(cfg)
    assert any(fixo > 0 for _, _, fixo, _ in cfg.op_costs)  # na Brasil, os de referência


def test_preco_da_cisterna_sem_catalogo_e_o_informado_no_projeto():
    """Sem o catálogo (fora da Brasil) a cisterna entrava a custo zero mesmo com o preço
    digitado na etapa 5; interface e CLI usam agora a mesma regra."""
    from triton.cli import _preco_da_cisterna
    from triton.core.cost_estimates import preco_da_cisterna_do_volume
    cfg = TritonConfig()
    assert preco_da_cisterna_do_volume(cfg, 3000.0) > 0  # catálogo, na Brasil
    assert preco_da_cisterna_do_volume(cfg, 3000.0) < preco_da_cisterna_do_volume(cfg, 10000.0)
    cfg.precos_de_catalogo, cfg.cost_lower_tank = False, 1500.0
    assert preco_da_cisterna_do_volume(cfg, 3000.0) == 1500.0 == _preco_da_cisterna(cfg, 3000.0)
    assert preco_da_cisterna_do_volume(cfg, 0.0) == 0.0
