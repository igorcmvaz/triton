"""
===================================================================================================================
NETUNO 5 -- MASTER RUNNER UNIFICADO E EXPANDIDO: ESTUDO MULTIDIMENSIONAL DE 5 TIPOLOGIAS (652 CIDADES / CMIP6)
===================================================================================================================
Estrutura Multidimensional do Estudo:
  • 5 Tipologias Habitacionais com Telhados Reais:
      - UTI: Casa Térrea (4 hab, 60.19 m², Telha Cerâmica, Coeficiente C = 0.80)
      - UTG: Casa Geminada (8 hab, 115.43 m², Telha Cerâmica, Coeficiente C = 0.80)
      - MSG: Sobrado Geminado 2 pav (16 hab, 132.53 m², Telha Cerâmica, Coeficiente C = 0.80)
      - MFH: Bloco Multifamiliar H (64 hab, 158.70 m², Telhado Fibrocimento, Coeficiente C = 0.90)
      - MFL: Bloco Multifamiliar Retangular L (128 hab, 421.52 m², Telhado Fibrocimento, Coeficiente C = 0.90)

  • 3 Regras de First Flush (Descarte Inicial):
      - 0 mm: Sem Descarte (Captação Bruta / Limite Superior Teórico)
      - 2 mm: Padrão NBR 15527 (Lavagem Clássica de Telhado)
      - 4 mm: Descarte Rigoroso (Alta Carga Poluidora / Zonas Urbanas e Industriais)

  • 3 Níveis de Demanda per capita: Baixa (120 L/hab.dia), Base (150 L/hab.dia), Alta (180 L/hab.dia)
  • 3 Frações de Substituição Pluvial: Baixa (30%), Base (40%), Alta (50%)
  • 12 Volumes de Cisterna: [500, 1.000, 2.000, 3.000, 5.000, 7.500, 10.000, 15.000, 20.000, 30.000, 40.000, 50.000] L

  • Matriz de Análise Econômico-Financeira com 3 Taxas de Desconto (TMA):
      - TMA 6.0% a.a. (Cenário de Longo Prazo / Infraestrutura Social Sustentável)
      - TMA 10.0% a.a. (Cenário Intermediário de Custo de Capital Privado)
      - TMA 14.0% a.a. (Cenário de Juros Altos / Referência Taxa SELIC Brasil)
      - LCOW (Levelized Cost of Water - Custo Nivelado do Metro Cúbico em R$/m³)
      - CAPEX Calibrado para 8 Subsistemas Prediais com Fatores Regionais SINAPI/CUB por UF
      - Tarifas Municipais de Água, Esgoto (70% a 100%) e Energia B1 ANEEL das 652 Cidades

  • Ranqueamento Multicritério TOPSIS Vectorized (12 volumes por perfil)

Uso no CMD:
  python scripts/run_estudo_5_tipologias.py --simulate    # Simulação diária completa (86.716 séries x 1.620 perfis)
  python scripts/run_estudo_5_tipologias.py --recalc      # Recálculo rápido de parâmetros econômicos na base Parquet
  python scripts/run_estudo_5_tipologias.py --capitais    # Gráficos, curvas de VPL e Dashboard das 27 capitais
  python scripts/run_estudo_5_tipologias.py --all         # Pipeline completo end-to-end
===================================================================================================================
"""

import os
import sys
import time
import glob
import json
import re
import math
import shutil
import argparse
import subprocess
import gc
import concurrent.futures
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from concurrent.futures import ProcessPoolExecutor, as_completed
from numba import njit

# Reconfigura saída para UTF-8 seguro em consoles Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Garante inclusão da raiz do projeto no PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from netuno.core.parser import load_precipitation
from netuno.core.simulation import _numba_sim_single, HAS_NUMBA
from netuno.core.economic import calculate_water_bill
from netuno.core.cost_estimates import (
    estimate_calibrated_capex_opex,
    REGIONAL_FACTORS_BY_UF,
    TYPOLOGY_COST_CONFIGS
)

# Diretórios padrão
STUDY_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais")
INPUT_SPLIT_DIR = os.path.join(STUDY_DIR, "Netuno_vaz_files_split")
OUTPUT_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz")
CHUNKS_DIR = os.path.join(OUTPUT_DIR, "chunks")
FINAL_PARQUET_PATH = os.path.join(OUTPUT_DIR, "estudo_vaz_consolidado.parquet")
TEMP_PARQUET_PATH = os.path.join(OUTPUT_DIR, "estudo_vaz_consolidado_updated.parquet")
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "checkpoint_progress.json")
CSV_TARIFAS_PATH = os.path.join(BASE_DIR, "tarifas", "tarifas_detalhadas_auditadas.csv")

os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 12 Volumes discretos de cisterna avaliados na varredura (Litros)
VOLUMES_SWEEP = [
    500.0, 1000.0, 2000.0, 3000.0, 5000.0, 7500.0,
    10000.0, 15000.0, 20000.0, 30000.0, 40000.0, 50000.0
]

# Definição das 5 Tipologias Edilícias com Materiais Reais de Cobertura
TYPOLOGIES = [
    {
        "code": "UTI",
        "name": "Casa Unifamiliar Térrea",
        "residents": 4,
        "units": 1,
        "roof_area_m2": 60.19,
        "roof_material": "Telha Cerâmica",
        "runoff_coeff": 0.80,
        "base_demand": 150.0,
        "base_share": 0.40
    },
    {
        "code": "UTG",
        "name": "Casa Unifamiliar Geminada",
        "residents": 8,
        "units": 2,
        "roof_area_m2": 115.43,
        "roof_material": "Telha Cerâmica",
        "runoff_coeff": 0.80,
        "base_demand": 150.0,
        "base_share": 0.40
    },
    {
        "code": "MSG",
        "name": "Sobrado Multifamiliar Geminado",
        "residents": 16,
        "units": 4,
        "roof_area_m2": 132.53,
        "roof_material": "Telha Cerâmica",
        "runoff_coeff": 0.80,
        "base_demand": 150.0,
        "base_share": 0.40
    },
    {
        "code": "MFH",
        "name": "Bloco Multifamiliar H",
        "residents": 64,
        "units": 16,
        "roof_area_m2": 158.70,
        "roof_material": "Fibrocimento",
        "runoff_coeff": 0.90,
        "base_demand": 150.0,
        "base_share": 0.40
    },
    {
        "code": "MFL",
        "name": "Bloco Multifamiliar Retangular",
        "residents": 128,
        "units": 32,
        "roof_area_m2": 421.52,
        "roof_material": "Fibrocimento",
        "runoff_coeff": 0.90,
        "base_demand": 150.0,
        "base_share": 0.40
    },
]

TYPOLOGY_UNITS = {t["code"]: t.get("units", 1) for t in TYPOLOGIES}

# ===================================================================================================================
# REGRAS DE FIRST FLUSH (DESCARTE DE ESCOAMENTO INICIAL) -- 3 MODOS DO NETUNO
# Modo 1: Todos os eventos de chuva (P_i > 0)
# Modo 2: Apenas após dias secos antecedentes (< 1 mm de chuva no dia anterior)
# Modo 3: Apenas se o intervalo desde o último descarte for >= N dias (padrão: 7 dias)
# ===================================================================================================================
def get_discard_variations(modes_list=(1, 2, 3), discard_days=7):
    """
    Constrói a matriz de regras de First Flush para o estudo:
    - 0 mm: Sem descarte (independente do modo)
    - 2 mm e 4 mm: instanciados para cada modo selecionado (1, 2 e 3)
    """
    variations = [
        {"code": "Disc0mm", "val": 0.0, "mode": 1, "days": 1, "name": "Sem Descarte (0 mm)"}
    ]
    for val in [2.0, 4.0]:
        val_int = int(val)
        if 1 in modes_list:
            variations.append({
                "code": f"Disc{val_int}mm_M1",
                "val": val,
                "mode": 1,
                "days": 1,
                "name": f"{val_int} mm - Todos os eventos (Modo 1)"
            })
        if 2 in modes_list:
            variations.append({
                "code": f"Disc{val_int}mm_M2",
                "val": val,
                "mode": 2,
                "days": 1,
                "name": f"{val_int} mm - Após dia seco < 1mm (Modo 2)"
            })
        if 3 in modes_list:
            variations.append({
                "code": f"Disc{val_int}mm_M3",
                "val": val,
                "mode": 3,
                "days": int(discard_days),
                "name": f"{val_int} mm - Intervalo >= {int(discard_days)}d (Modo 3)"
            })
    return variations

DISCARD_VARIATIONS = get_discard_variations(modes_list=[1, 2, 3], discard_days=7)

# 3 Variações de Demanda per capita
DEMAND_VARIATIONS = [
    {"suffix": "DemLow", "multiplier": 0.80, "val": 120.0},
    {"suffix": "DemBase", "multiplier": 1.00, "val": 150.0},
    {"suffix": "DemHigh", "multiplier": 1.20, "val": 180.0},
]

# 3 Variações de Substituição Pluvial
SHARE_VARIATIONS = [
    {"suffix": "ShareLow", "val": 0.30, "pct": 30.0},
    {"suffix": "ShareBase", "val": 0.40, "pct": 40.0},
    {"suffix": "ShareHigh", "val": 0.50, "pct": 50.0},
]

# Fatores de Valor Presente (PV Factors) para 20 anos
PV_FACTOR_6 = (1.0 - (1.0 + 0.06)**(-20)) / 0.06    # 11.4699
PV_FACTOR_10 = (1.0 - (1.0 + 0.10)**(-20)) / 0.10  # 8.5136
PV_FACTOR_14 = (1.0 - (1.0 + 0.14)**(-20)) / 0.14  # 6.6231 (SELIC)


# ===================================================================================================================
# 1. BANCO TARIFÁRIO UNIFICADO E PRÉ-COMPUTAÇÃO DE CAPEX CALIBRADO
# ===================================================================================================================

def load_tariff_dictionary():
    """Carrega o banco de dados oficial e otimizado de tarifas do Netuno 5 (652 cidades / 27 UFs)."""
    from netuno.core.tariffs_database import load_tariffs_db
    db = load_tariffs_db()
    city_tariffs = {}
    for key, c_data in db.get('cities', {}).items():
        m_clean = c_data.get('municipio', '').strip()
        tariff_tuples = [tuple(f) for f in c_data.get('faixas', [])]
        if not tariff_tuples:
            tariff_tuples = [(0.0, 10.0, 5.50, 1), (10.0, 999999.0, 8.50, 1)]
            
        vol_rates = [t[2] for t in tariff_tuples if t[3] == 1 and t[2] > 0]
        base_water_rate = vol_rates[0] if vol_rates else tariff_tuples[0][2]
        
        info = {
            'tariffs': tariff_tuples,
            'sewage_rate': float(c_data.get('esgoto_pct', 80.0)),
            'elec_tariff': float(c_data.get('energia_r_kwh', 0.85)),
            'prestador': str(c_data.get('prestador_saneamento', '')),
            'uf': str(c_data.get('uf', '')).strip().upper(),
            'regiao': str(c_data.get('regiao', '')).strip(),
            'base_water_rate': float(base_water_rate)
        }
        city_tariffs[m_clean] = info
        city_tariffs[key] = info
    return city_tariffs


def build_calibrated_capex_lookup():
    lookup = {}
    volumes = VOLUMES_SWEEP
    typologies = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    ufs = list(REGIONAL_FACTORS_BY_UF.keys())
    
    for uf in ufs:
        for typ in typologies:
            for vol in volumes:
                res = estimate_calibrated_capex_opex(typology=typ, volume_l=vol, uf=uf, detailed_breakdown=False)
                lookup[(typ, float(vol), uf)] = (float(res["capex_total_brl"]), float(res["opex_fixed_annual_brl"]))
    return lookup


CITY_TARIFFS_PRELOADED = load_tariff_dictionary()
CAPEX_LOOKUP = build_calibrated_capex_lookup()
DEFAULT_CITY_TARIFF = list(CITY_TARIFFS_PRELOADED.values())[0] if CITY_TARIFFS_PRELOADED else {
    'tariffs': [(0.0, 10.0, 5.50, 1), (10.0, 999999.0, 8.50, 1)],
    'sewage_rate': 80.0,
    'elec_tariff': 0.75,
    'prestador': 'Referência Regional',
    'uf': 'SP',
    'regiao': 'Sudeste',
    'base_water_rate': 5.50
}


def calc_bill_single(vol_l, tariffs, sewage_rate):
    vol_m3 = vol_l / 1000.0
    c_agua = 0.0
    for min_v, max_v, rate, is_fix in tariffs:
        if is_fix == -1:
            c_agua += rate
        elif vol_m3 > min_v:
            v_in_tier = min(vol_m3, max_v) - min_v
            if v_in_tier > 0:
                c_agua += v_in_tier * rate
    return c_agua * (1.0 + (sewage_rate / 100.0))


def recompute_topsis_vectorized(v_sav, v_vpl, v_co2, v_full, v_cpx, n_vols=12):
    """TOPSIS multicritério vetorizado rápido para N volumes discretos por perfil."""
    n_rows = len(v_sav)
    n_profiles = n_rows // n_vols
    
    m_sav = v_sav.reshape(n_profiles, n_vols)
    m_vpl = v_vpl.reshape(n_profiles, n_vols)
    m_co2 = v_co2.reshape(n_profiles, n_vols)
    m_full = v_full.reshape(n_profiles, n_vols)
    m_cpx = v_cpx.reshape(n_profiles, n_vols)
    
    def norm_matrix(mat):
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms < 1e-9] = 1.0
        return mat / norms
        
    n_sav = norm_matrix(m_sav) * 0.25
    n_vpl = norm_matrix(m_vpl) * 0.25
    n_co2 = norm_matrix(m_co2) * 0.20
    n_full = norm_matrix(m_full) * 0.15
    n_cpx = norm_matrix(m_cpx) * 0.15
    
    id_sav, aid_sav = np.max(n_sav, axis=1, keepdims=True), np.min(n_sav, axis=1, keepdims=True)
    id_vpl, aid_vpl = np.max(n_vpl, axis=1, keepdims=True), np.min(n_vpl, axis=1, keepdims=True)
    id_co2, aid_co2 = np.max(n_co2, axis=1, keepdims=True), np.min(n_co2, axis=1, keepdims=True)
    id_full, aid_full = np.max(n_full, axis=1, keepdims=True), np.min(n_full, axis=1, keepdims=True)
    id_cpx, aid_cpx = np.min(n_cpx, axis=1, keepdims=True), np.max(n_cpx, axis=1, keepdims=True)
    
    d_plus = np.sqrt(
        (n_sav - id_sav)**2 + (n_vpl - id_vpl)**2 + (n_co2 - id_co2)**2 + (n_full - id_full)**2 + (n_cpx - id_cpx)**2
    )
    d_minus = np.sqrt(
        (n_sav - aid_sav)**2 + (n_vpl - aid_vpl)**2 + (n_co2 - aid_co2)**2 + (n_full - aid_full)**2 + (n_cpx - aid_cpx)**2
    )
    
    sum_d = d_plus + d_minus
    scores = np.where(sum_d > 1e-9, d_minus / sum_d, 0.5)
    
    ranks = np.zeros_like(scores, dtype=np.int16)
    is_best = np.zeros_like(scores, dtype=bool)
    
    for p in range(n_profiles):
        s_p = scores[p]
        order = np.argsort(-s_p)
        for r, idx in enumerate(order):
            ranks[p, idx] = r + 1
        is_best[p, order[0]] = True
        
    return scores.flatten(), ranks.flatten(), is_best.flatten()


# ===================================================================================================================
# 2. SIMULAÇÃO HIDROLÓGICA COMPLETA DE BALANÇO DIÁRIO
# ===================================================================================================================

def parse_climate_filename(fname: str):
    clean_name = fname.replace("(Netuno)", "").replace(".csv", "").replace(".txt", "")
    parts = clean_name.split("_")
    city = parts[0].strip() if len(parts) > 0 else "Desconhecido"
    model = parts[1].strip() if len(parts) > 1 else "Observed"
    
    if len(parts) == 3:
        p2 = parts[2].strip()
        scenario = "Histórico" if "Hist" in p2 else p2
        horizon = "Histórico"
    elif len(parts) >= 4:
        scenario = parts[2].strip()
        horizon = parts[3].strip()
    else:
        scenario = "Desconhecido"
        horizon = "Desconhecido"
    return city, model, scenario, horizon


@njit(fastmath=True, nogil=True)
def run_worker_batch_numba(
    precip_matrix,      # (N_files, N_days)
    params_matrix,      # (N_profiles, 8)
    results_matrix      # (N_files, N_profiles, 6)
):
    n_files = precip_matrix.shape[0]
    n_profiles = params_matrix.shape[0]
    n_days = precip_matrix.shape[1]
    
    for f_idx in range(n_files):
        for p_idx in range(n_profiles):
            lower_vol = params_matrix[p_idx, 0]
            area = params_matrix[p_idx, 1]
            runoff_coeff = params_matrix[p_idx, 2]
            discard_mm = params_matrix[p_idx, 3]
            discard_mode = int(params_matrix[p_idx, 4])
            discard_days = int(params_matrix[p_idx, 5])
            tot_demand = params_matrix[p_idx, 6]
            pluv_demand = params_matrix[p_idx, 7]
            
            v_lower = 0.0
            tot_pluv = 0.0
            tot_pot = 0.0
            tot_spill = 0.0
            days_full = 0
            days_partial = 0
            days_null = 0
            last_discard = -999999
            
            for i in range(n_days):
                p_i = precip_matrix[f_idx, i]
                apply_discard = False
                if p_i > 0.0:
                    if discard_mode == 1:
                        apply_discard = True
                    elif discard_mode == 2:
                        prev_p = precip_matrix[f_idx, i-1] if i > 0 else 0.0
                        if prev_p < 1.0:
                            apply_discard = True
                    elif discard_mode == 3:
                        if (i - last_discard) >= discard_days:
                            apply_discard = True
                            
                if apply_discard:
                    p_eff = p_i - discard_mm if p_i > discard_mm else 0.0
                    last_discard = i
                else:
                    p_eff = p_i
                    
                v_ac = p_eff * area * runoff_coeff
                v_avail = v_lower + v_ac
                if v_avail > lower_vol:
                    tot_spill += (v_avail - lower_vol)
                    v_in = lower_vol
                else:
                    v_in = v_avail
                    
                v_c = pluv_demand if v_in >= pluv_demand else v_in
                v_lower = v_in - v_c
                tot_pot += (tot_demand - v_c)
                tot_pluv += v_c
                
                if v_c >= (pluv_demand - 1e-4):
                    days_full += 1
                elif v_c > 1e-4:
                    days_partial += 1
                else:
                    days_null += 1
                    
            results_matrix[f_idx, p_idx, 0] = tot_pluv
            results_matrix[f_idx, p_idx, 1] = tot_pot
            results_matrix[f_idx, p_idx, 2] = tot_spill
            results_matrix[f_idx, p_idx, 3] = days_full
            results_matrix[f_idx, p_idx, 4] = days_partial
            results_matrix[f_idx, p_idx, 5] = days_null


def init_worker_process():
    precip_mat = np.zeros((1, 100), dtype=np.float64)
    params_mat = np.ones((10, 8), dtype=np.float64)
    res_mat = np.zeros((1, 10, 6), dtype=np.float64)
    run_worker_batch_numba(precip_mat, params_mat, res_mat)


def build_simulation_profiles(discard_variations):
    profiles = []
    for typ in TYPOLOGIES:
        b_code = typ["code"]
        b_name = typ["name"]
        residents = typ["residents"]
        units = typ.get("units", 1)
        roof_area = typ["roof_area_m2"]
        runoff_coeff = typ["runoff_coeff"]
        
        for disc in discard_variations:
            discard_mm = disc["val"]
            discard_mode = disc["mode"]
            discard_days = disc["days"]
            discard_name = disc["name"]
            discard_code = disc["code"]
            
            for dem_var in DEMAND_VARIATIONS:
                dem_val = dem_var["val"]
                tot_demand_day = dem_val * residents
                
                for sh_var in SHARE_VARIATIONS:
                    sh_val = sh_var["val"]
                    sh_pct = sh_var["pct"]
                    pluv_demand_day = tot_demand_day * sh_val
                    
                    for vol in VOLUMES_SWEEP:
                        profiles.append({
                            "b_code": b_code,
                            "b_name": b_name,
                            "residents": residents,
                            "units": units,
                            "roof_area": roof_area,
                            "runoff_coeff": runoff_coeff,
                            "discard_mm": discard_mm,
                            "discard_mode": discard_mode,
                            "discard_days": discard_days,
                            "discard_name": discard_name,
                            "discard_code": discard_code,
                            "demand_per_capita": dem_val,
                            "share_pct": sh_pct,
                            "vol": vol,
                            "tot_demand_day": tot_demand_day,
                            "pluv_demand_day": pluv_demand_day
                        })
    return profiles


def process_chunk_batch_worker(args):
    chunk_idx, file_paths, params_mat, profiles_meta = args
    n_files = len(file_paths)
    n_profiles = len(profiles_meta)
    
    precips = [load_precipitation(f) for f in file_paths]
    n_days = max(len(p) for p in precips)
    precip_mat = np.zeros((n_files, n_days), dtype=np.float64)
    for i, p in enumerate(precips):
        precip_mat[i, :len(p)] = p
        
    results_mat = np.zeros((n_files, n_profiles, 6), dtype=np.float64)
    run_worker_batch_numba(precip_mat, params_mat, results_mat)
    
    n_tot = n_files * n_profiles
    meta_list = [parse_climate_filename(os.path.basename(f)) for f in file_paths]
    cities_col = np.repeat([m[0] for m in meta_list], n_profiles)
    models_col = np.repeat([m[1] for m in meta_list], n_profiles)
    scenarios_col = np.repeat([m[2] for m in meta_list], n_profiles)
    horizons_col = np.repeat([m[3] for m in meta_list], n_profiles)
    clean_cities_col = np.repeat([m[0].strip() for m in meta_list], n_profiles)

    b_codes_col = np.tile([p["b_code"] for p in profiles_meta], n_files)
    b_names_col = np.tile([p["b_name"] for p in profiles_meta], n_files)
    residents_col = np.tile([p["residents"] for p in profiles_meta], n_files)
    units_col = np.tile([p["units"] for p in profiles_meta], n_files)
    roof_areas_col = np.tile([p["roof_area"] for p in profiles_meta], n_files)
    runoff_coeffs_col = np.tile([p["runoff_coeff"] for p in profiles_meta], n_files)
    disc_codes_col = np.tile([p["discard_code"] for p in profiles_meta], n_files)
    disc_names_col = np.tile([p["discard_name"] for p in profiles_meta], n_files)
    disc_modes_col = np.tile([p["discard_mode"] for p in profiles_meta], n_files)
    disc_days_col = np.tile([p["discard_days"] for p in profiles_meta], n_files)
    disc_mms_col = np.tile([p["discard_mm"] for p in profiles_meta], n_files)
    demands_col = np.tile([p["demand_per_capita"] for p in profiles_meta], n_files)
    shares_col = np.tile([p["share_pct"] for p in profiles_meta], n_files)
    vols_col = np.tile([p["vol"] for p in profiles_meta], n_files)
    tot_demands_col = np.tile([p["tot_demand_day"] for p in profiles_meta], n_files)

    flat_res = results_mat.reshape(n_tot, 6)
    avg_pluv = flat_res[:, 0] / n_days
    avg_pot = flat_res[:, 1] / n_days
    avg_spill = flat_res[:, 2] / n_days
    days_full = flat_res[:, 3]
    days_partial = flat_res[:, 4]
    days_null = flat_res[:, 5]

    ann_tot_dem = (tot_demands_col * 365.25) / 1000.0
    ann_pluv = (avg_pluv * 365.25) / 1000.0
    ann_pot = (avg_pot * 365.25) / 1000.0
    ann_spill = (avg_spill * 365.25) / 1000.0
    pot_savings = np.where(tot_demands_col > 0, (avg_pluv / tot_demands_col) * 100.0, 0.0)
    rel_full = (days_full / n_days) * 100.0
    rel_part = (days_partial / n_days) * 100.0
    rel_null = (days_null / n_days) * 100.0

    # Computação Financeira e Calibração Tarifária Direta no Worker
    city_tariffs = CITY_TARIFFS_PRELOADED
    capex_lookup = CAPEX_LOOKUP
    fallback_city_key = list(city_tariffs.keys())[0]

    annual_water_savings = np.zeros(n_tot, dtype=np.float32)
    annual_opex = np.zeros(n_tot, dtype=np.float32)
    capex_calibrated = np.zeros(n_tot, dtype=np.float32)
    tarifa_elec_arr = np.zeros(n_tot, dtype=np.float32)
    tarifa_agua_base_arr = np.zeros(n_tot, dtype=np.float32)
    esgoto_pct_arr = np.zeros(n_tot, dtype=np.float32)
    prestador_arr = np.empty(n_tot, dtype=object)
    uf_arr = np.empty(n_tot, dtype=object)
    regiao_arr = np.empty(n_tot, dtype=object)

    monthly_tot_l = tot_demands_col * 30.4375
    monthly_pot_l = avg_pot * 30.4375

    for f_idx in range(n_files):
        c_raw = meta_list[f_idx][0]
        c_clean = c_raw.strip()
        info = city_tariffs.get(c_clean, city_tariffs[fallback_city_key])

        tariffs = info['tariffs']
        sew_rate = info['sewage_rate']
        elec_rate = info['elec_tariff']
        base_w_rate = info['base_water_rate']
        uf_city = info['uf']
        regiao_city = info['regiao']
        prestador_city = info['prestador']

        slice_f = slice(f_idx * n_profiles, (f_idx + 1) * n_profiles)
        
        sub_b_codes = b_codes_col[slice_f]
        sub_units = units_col[slice_f].astype(np.float64)
        sub_tot_l = monthly_tot_l[slice_f]
        sub_pot_l = monthly_pot_l[slice_f]
        sub_pluv_m3 = ann_pluv[slice_f]
        sub_vols = vols_col[slice_f]

        sub_tot_l_unit = sub_tot_l / sub_units
        sub_pot_l_unit = sub_pot_l / sub_units

        unique_vols = np.unique(np.concatenate([sub_tot_l_unit, sub_pot_l_unit]))
        bill_dict = {v: calc_bill_single(v, tariffs, sew_rate) for v in unique_vols}

        sub_bill_without = np.array([bill_dict[v] for v in sub_tot_l_unit]) * sub_units
        sub_bill_with = np.array([bill_dict[v] for v in sub_pot_l_unit]) * sub_units
        sub_water_savings = np.maximum(0.0, sub_bill_without - sub_bill_with) * 12.0

        annual_water_savings[slice_f] = sub_water_savings.astype(np.float32)

        sub_cpx = np.empty(n_profiles, dtype=np.float32)
        sub_maint_fixed = np.empty(n_profiles, dtype=np.float32)

        for i in range(n_profiles):
            cpx_val, maint_val = capex_lookup.get(
                (sub_b_codes[i], sub_vols[i], uf_city),
                (6500.0, 420.0)
            )
            sub_cpx[i] = cpx_val
            sub_maint_fixed[i] = maint_val

        capex_calibrated[slice_f] = sub_cpx

        sub_pump_kwh = sub_pluv_m3 * 0.45
        sub_pump_cost = sub_pump_kwh * elec_rate
        sub_chlorine_cost = sub_pluv_m3 * 0.05

        annual_opex[slice_f] = (sub_pump_cost + sub_chlorine_cost + sub_maint_fixed).astype(np.float32)
        tarifa_elec_arr[slice_f] = elec_rate
        tarifa_agua_base_arr[slice_f] = base_w_rate
        esgoto_pct_arr[slice_f] = sew_rate
        prestador_arr[slice_f] = prestador_city
        uf_arr[slice_f] = uf_city
        regiao_arr[slice_f] = regiao_city

    net_annual = annual_water_savings - annual_opex
    vpl_6 = -capex_calibrated + (net_annual * PV_FACTOR_6)
    vpl_10 = -capex_calibrated + (net_annual * PV_FACTOR_10)
    vpl_14 = -capex_calibrated + (net_annual * PV_FACTOR_14)

    payback = np.where(net_annual > 0, capex_calibrated / net_annual, 99.0).astype(np.float32)
    tir = np.where(capex_calibrated > 0, (net_annual / capex_calibrated) * 100.0, 0.0).astype(np.float32)
    denom_lcow = np.maximum(0.001, ann_pluv * PV_FACTOR_6)
    lcow = ((capex_calibrated + (annual_opex * PV_FACTOR_6)) / denom_lcow).astype(np.float32)

    co2_val = ann_pluv * 0.35 * 20.0

    t_score, t_rank, t_is_best = recompute_topsis_vectorized(
        pot_savings,
        vpl_6,
        co2_val,
        rel_full,
        capex_calibrated,
        n_vols=12
    )

    table = pa.Table.from_arrays([
        pa.array(cities_col, pa.string()),
        pa.array(models_col, pa.string()),
        pa.array(scenarios_col, pa.string()),
        pa.array(horizons_col, pa.string()),
        pa.array(clean_cities_col, pa.string()),
        pa.array(b_codes_col, pa.string()),
        pa.array(b_names_col, pa.string()),
        pa.array(residents_col, pa.int32()),
        pa.array(roof_areas_col, pa.float32()),
        pa.array(runoff_coeffs_col, pa.float32()),
        pa.array(disc_codes_col, pa.string()),
        pa.array(disc_names_col, pa.string()),
        pa.array(disc_modes_col, pa.int32()),
        pa.array(disc_days_col, pa.int32()),
        pa.array(disc_mms_col, pa.float32()),
        pa.array(demands_col, pa.float32()),
        pa.array(shares_col, pa.float32()),
        pa.array(vols_col, pa.float32()),
        pa.array(tot_demands_col, pa.float32()),
        pa.array(ann_tot_dem, pa.float32()),
        pa.array(avg_pluv, pa.float32()),
        pa.array(ann_pluv, pa.float32()),
        pa.array(pot_savings, pa.float32()),
        pa.array(avg_pot, pa.float32()),
        pa.array(ann_pot, pa.float32()),
        pa.array(avg_spill, pa.float32()),
        pa.array(ann_spill, pa.float32()),
        pa.array(rel_full, pa.float32()),
        pa.array(rel_part, pa.float32()),
        pa.array(rel_null, pa.float32()),
        pa.array(capex_calibrated, pa.float32()),
        pa.array(annual_opex, pa.float32()),
        pa.array(annual_water_savings, pa.float32()),
        pa.array(vpl_6, pa.float32()),
        pa.array(vpl_10, pa.float32()),
        pa.array(vpl_14, pa.float32()),
        pa.array(payback, pa.float32()),
        pa.array(tir, pa.float32()),
        pa.array(lcow, pa.float32()),
        pa.array(t_score, pa.float32()),
        pa.array(vpl_6, pa.float32()),
        pa.array(lcow, pa.float32()),
        pa.array(tir, pa.float32()),
        pa.array(t_rank, pa.int32()),
        pa.array(t_is_best, pa.bool_()),
        pa.array(tarifa_elec_arr, pa.float32()),
        pa.array(tarifa_agua_base_arr, pa.float32()),
        pa.array(esgoto_pct_arr, pa.float32()),
        pa.array(prestador_arr, pa.string()),
        pa.array(uf_arr, pa.string()),
        pa.array(regiao_arr, pa.string()),
    ], names=[
        'city', 'model', 'scenario', 'horizon', 'clean_city', 'building_code',
        'building_name', 'residents', 'roof_area_m2', 'runoff_coeff',
        'discard_code', 'discard_name', 'discard_mode', 'discard_days',
        'discard_mm', 'demand_per_capita_l_day', 'share_pct', 'lower_tank_vol_l',
        'total_demand_l_day', 'annual_total_demand_m3', 'avg_pluvial_consumed_l_day',
        'annual_pluvial_consumed_m3', 'potential_water_savings_pct',
        'avg_potable_consumed_l_day', 'annual_potable_consumed_m3',
        'avg_overflow_spill_l_day', 'annual_overflow_spill_m3',
        'reliability_fully_met_pct', 'reliability_partially_met_pct',
        'reliability_not_met_pct', 'capex_total_brl', 'annual_opex_brl',
        'annual_water_savings_brl', 'vpl_6pct_brl', 'vpl_10pct_brl',
        'vpl_14pct_brl', 'payback_years', 'tir_pct_yr', 'lcow_brl_m3',
        'topsis_score', 'vpl_brl', 'lcow_r_per_m3', 'tir_annual_pct',
        'topsis_rank', 'is_topsis_best', 'tarifa_eletricidade_b1_r_kwh',
        'tarifa_agua_base_r_m3', 'esgoto_pct_sobre_agua', 'saneamento_prestador',
        'uf', 'regiao'
    ])
    
    chunk_path = os.path.join(CHUNKS_DIR, f"part_{chunk_idx:05d}.parquet")
    pq.write_table(table, chunk_path, compression='snappy')
    
    fnames = [os.path.basename(f) for f in file_paths]
    return n_files, n_tot, fnames


def process_single_climate_file(file_path: str) -> list:
    """Processa 1 arquivo de chuva executando os 135 perfis edilícios x 12 volumes com Numba JIT."""
    fname = os.path.basename(file_path)
    city, model, scenario, horizon = parse_climate_filename(fname)

    precip_data = load_precipitation(file_path)
    n_days = len(precip_data)
    if n_days == 0:
        return []

    precip_arr = np.array(precip_data, dtype=np.float64)
    all_file_rows = []

    # Recupera tarifação real do município
    city_tar = CITY_TARIFFS_PRELOADED.get(city.strip(), DEFAULT_CITY_TARIFF)
    c_tariffs = city_tar['tariffs']
    c_sewage_rate = city_tar['sewage_rate']
    c_elec_rate = city_tar['elec_tariff']
    c_uf = str(city_tar.get('uf', 'SP')).strip().upper()
    c_regiao = str(city_tar.get('regiao', 'Sudeste')).strip()

    # 5 Tipologias
    for typ in TYPOLOGIES:
        b_code = typ["code"]
        b_name = typ["name"]
        residents = typ["residents"]
        roof_area = typ["roof_area_m2"]
        roof_material = typ["roof_material"]
        runoff_coeff = typ["runoff_coeff"]

        # Regras de First Flush (Lâminas 0, 2 e 4 mm x Modos 1, 2 e 3 com intervalo de 7 dias)
        for disc in DISCARD_VARIATIONS:
            discard_mm = disc["val"]
            discard_mode = disc["mode"]
            discard_days = disc["days"]
            discard_name = disc["name"]
            discard_code = disc["code"]

            # 3 Variações de Demanda x 3 Variações de Substituição (9 Combinações)
            for dem_var in DEMAND_VARIATIONS:
                dem_val = dem_var["val"]
                tot_demand_day = dem_val * residents
                tot_demands_arr = np.full(n_days, tot_demand_day, dtype=np.float64)

                for sh_var in SHARE_VARIATIONS:
                    sh_val = sh_var["val"]
                    sh_pct = sh_var["pct"]
                    pluv_demand_day = tot_demand_day * sh_val
                    pluvial_demands_arr = np.full(n_days, pluv_demand_day, dtype=np.float64)

                    profile_candidates = []

                    # 12 Volumes de Cisterna
                    for vol in VOLUMES_SWEEP:
                        (
                            tot_pluv, tot_pot, tot_spill,
                            _, _, _,
                            days_full, days_partial, days_null
                        ) = _numba_sim_single(
                            precip_arr, vol, roof_area, runoff_coeff,
                            discard_mm, int(discard_mode), int(discard_days),
                            tot_demands_arr, pluvial_demands_arr
                        )

                        avg_pluv = tot_pluv / n_days
                        avg_pot = tot_pot / n_days
                        avg_spill = tot_spill / n_days

                        potential_savings_pct = (avg_pluv / tot_demand_day) * 100.0 if tot_demand_day > 0 else 0.0
                        fully_met_pct = (days_full / n_days) * 100.0
                        partially_met_pct = (days_partial / n_days) * 100.0
                        not_met_pct = (days_null / n_days) * 100.0

                        annual_pluv_m3 = (avg_pluv * 365.25) / 1000.0
                        annual_pot_m3 = (avg_pot * 365.25) / 1000.0
                        annual_spill_m3 = (avg_spill * 365.25) / 1000.0

                        # CAPEX e Manutenção Fixa por tipologia e UF
                        capex_total, maint_cost_yr = CAPEX_LOOKUP.get((b_code, float(vol), c_uf), (6500.0, 420.0))

                        # Economia Financeira na Conta de Água com Micromedição por Apartamento/Unidade
                        b_units = typ.get("units", 1)
                        monthly_tot_l = tot_demand_day * 30.4375
                        monthly_pot_l = avg_pot * 30.4375

                        bill_without = calculate_water_bill(monthly_tot_l, tariffs=c_tariffs, sewage_mode=1, sewage_rate=c_sewage_rate, num_units=b_units)
                        bill_with = calculate_water_bill(monthly_pot_l, tariffs=c_tariffs, sewage_mode=1, sewage_rate=c_sewage_rate, num_units=b_units)
                        monthly_water_savings = max(0.0, bill_without - bill_with)
                        annual_water_savings = monthly_water_savings * 12.0

                        # OPEX Anual (Energia B1 + Cloro + Manutenção Calibrada)
                        pump_kwh_yr = annual_pluv_m3 * 0.45
                        pump_cost_yr = pump_kwh_yr * c_elec_rate
                        chlorine_cost_yr = annual_pluv_m3 * 0.05
                        annual_opex = pump_cost_yr + chlorine_cost_yr + maint_cost_yr

                        net_annual = annual_water_savings - annual_opex

                        # VPL e Payback para as 3 Taxas de Desconto (6%, 10% e 14% SELIC)
                        vpl_6 = -capex_total + (net_annual * PV_FACTOR_6)
                        vpl_10 = -capex_total + (net_annual * PV_FACTOR_10)
                        vpl_14 = -capex_total + (net_annual * PV_FACTOR_14)

                        payback_years = (capex_total / net_annual) if net_annual > 0 else 99.0
                        tir_annual = ((net_annual / capex_total) * 100.0) if capex_total > 0 else 0.0

                        # LCOW (Levelized Cost of Water em R$/m³)
                        denom_lcow = max(0.001, annual_pluv_m3 * PV_FACTOR_6)
                        lcow_r_m3 = (capex_total + (annual_opex * PV_FACTOR_6)) / denom_lcow

                        # Pegada de Carbono ACV
                        pead_kg = vol * 0.045
                        embodied_co2 = (pead_kg * 1.9) + 45.0 + 35.0
                        annual_avoided_co2 = (annual_pluv_m3 * 0.35) - (pump_kwh_yr * 0.08)
                        lifetime_net_co2 = (annual_avoided_co2 * 20.0) - embodied_co2
                        upper_tank_vol = max(200.0, vol * 0.10)

                        row_dict = {
                            "city": city,
                            "model": model,
                            "scenario": scenario,
                            "horizon": horizon,
                            "building_code": b_code,
                            "building_name": b_name,
                            "roof_material": roof_material,
                            "runoff_coeff": float(runoff_coeff),
                            "discard_mm": float(discard_mm),
                            "discard_mode": int(discard_mode),
                            "discard_days_interval": int(discard_days),
                            "discard_code": discard_code,
                            "discard_name": discard_name,
                            "residents": int(residents),
                            "roof_area_m2": float(roof_area),
                            "demand_per_capita_l": float(dem_val),
                            "total_demand_l_day": float(tot_demand_day),
                            "rainwater_share_pct": float(sh_pct),
                            "lower_tank_vol_l": float(vol),
                            "upper_tank_vol_l": float(upper_tank_vol),
                            "potential_savings_pct": float(potential_savings_pct),
                            "avg_pluvial_consumed_l_day": float(avg_pluv),
                            "annual_pluvial_consumed_m3": float(annual_pluv_m3),
                            "avg_potable_consumed_l_day": float(avg_pot),
                            "annual_potable_consumed_m3": float(annual_pot_m3),
                            "avg_spilled_l_day": float(avg_spill),
                            "annual_spill_m3": float(annual_spill_m3),
                            "fully_met_pct": float(fully_met_pct),
                            "partially_met_pct": float(partially_met_pct),
                            "not_met_pct": float(not_met_pct),
                            "capex_total_brl": float(capex_total),
                            "annual_opex_brl": float(annual_opex),
                            "annual_water_savings_brl": float(annual_water_savings),
                            "vpl_brl": float(vpl_6),
                            "vpl_6pct_brl": float(vpl_6),
                            "vpl_10pct_brl": float(vpl_10),
                            "vpl_14pct_brl": float(vpl_14),
                            "lcow_r_per_m3": float(lcow_r_m3),
                            "tir_annual_pct": float(tir_annual),
                            "payback_years": float(payback_years),
                            "embodied_co2_kg": float(embodied_co2),
                            "annual_avoided_co2_kg": float(annual_avoided_co2),
                            "lifetime_net_co2_saved_kg": float(lifetime_net_co2),
                            "pump_energy_kwh_yr": float(pump_kwh_yr),
                            "tarifa_eletricidade_b1_r_kwh": float(c_elec_rate),
                            "tarifa_agua_base_r_m3": float(city_tar['base_water_rate']),
                            "esgoto_pct_sobre_agua": float(c_sewage_rate),
                            "saneamento_prestador": str(city_tar['prestador']),
                            "uf": str(c_uf),
                            "regiao": str(c_regiao),
                        }
                        profile_candidates.append(row_dict)

                    # TOPSIS no perfil de 12 volumes
                    v_sav = np.array([c["potential_savings_pct"] for c in profile_candidates])
                    v_vpl = np.array([c["vpl_brl"] for c in profile_candidates])
                    v_co2 = np.array([c["lifetime_net_co2_saved_kg"] for c in profile_candidates])
                    v_full = np.array([c["fully_met_pct"] for c in profile_candidates])
                    v_cpx = np.array([c["capex_total_brl"] for c in profile_candidates])

                    scores, ranks, is_best = recompute_topsis_vectorized(v_sav, v_vpl, v_co2, v_full, v_cpx, n_vols=12)
                    for idx in range(12):
                        profile_candidates[idx]["topsis_score"] = float(scores[idx])
                        profile_candidates[idx]["topsis_rank"] = int(ranks[idx])
                        profile_candidates[idx]["is_topsis_best"] = bool(is_best[idx])

                    all_file_rows.extend(profile_candidates)

    return all_file_rows


def format_time_hms(seconds: float) -> str:
    if seconds < 0 or math.isinf(seconds) or math.isnan(seconds):
        return "--:--:--"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}h {m:02d}m {s:02d}s" if h > 0 else f"{m:02d}m {s:02d}s"


def render_progress_bar(pct: float, width: int = 22) -> str:
    filled = int(width * (pct / 100.0))
    filled = max(0, min(width, filled))
    return "=" * filled + "-" * (width - filled)


def merge_chunks_to_final_parquet(delete_chunks: bool = True):
    chunk_files = sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.parquet")))
    if not chunk_files:
        if os.path.exists(FINAL_PARQUET_PATH):
            return True
        return False
    print("\n" + "=" * 105)
    print("CONSOLIDAÇÃO FINAL DE ARQUIVOS PARQUET (STREAMING OTIMIZADO)")
    print("=" * 105)
    print(f" [+] Lendo {len(chunk_files):,} blocos intermediários de chunks...")
    start_merge = time.time()
    
    temp_merge_path = FINAL_PARQUET_PATH + ".tmp"
    if os.path.exists(temp_merge_path):
        try:
            os.remove(temp_merge_path)
        except Exception:
            pass

    # Extrai o schema canônico a partir do primeiro chunk
    first_table = pq.read_table(chunk_files[0])
    canonical_schema = first_table.schema.remove_metadata()
    writer = pq.ParquetWriter(temp_merge_path, canonical_schema, compression="snappy")

    total_rows = 0

    for i, c_path in enumerate(chunk_files, start=1):
        table = pq.read_table(c_path)
        total_rows += table.num_rows

        # Alinha tipos com o schema canônico se houver qualquer divergência de tipo ou metadata
        if table.schema != canonical_schema:
            try:
                cols = []
                for field in canonical_schema:
                    if field.name in table.column_names:
                        col = table[field.name].cast(field.type)
                    else:
                        col = pa.nulls(table.num_rows, type=field.type)
                    cols.append(col)
                table = pa.Table.from_arrays(cols, schema=canonical_schema)
            except Exception:
                table = table.replace_schema_metadata(None)

        writer.write_table(table)
        del table
        if i % 25 == 0 or i == len(chunk_files):
            gc.collect()
            print(f"  --> Integrado bloco {i:,}/{len(chunk_files):,} | Total acumulado: {total_rows:,} registros", flush=True)

    writer.close()
    del writer
    gc.collect()

    print(" [*] Atualizando arquivo consolidado principal em disco...")
    replaced = False
    for attempt in range(10):
        try:
            if os.path.exists(FINAL_PARQUET_PATH):
                os.replace(temp_merge_path, FINAL_PARQUET_PATH)
            else:
                shutil.move(temp_merge_path, FINAL_PARQUET_PATH)
            replaced = True
            break
        except Exception:
            gc.collect()
            time.sleep(1.0)

    if not replaced:
        shutil.copy2(temp_merge_path, FINAL_PARQUET_PATH)
        try:
            os.remove(temp_merge_path)
        except Exception:
            pass

    if delete_chunks:
        shutil.rmtree(CHUNKS_DIR, ignore_errors=True)
        os.makedirs(CHUNKS_DIR, exist_ok=True)

    file_size_gb = os.path.getsize(FINAL_PARQUET_PATH) / (1024 * 1024 * 1024)
    print(f"[OK] CONSOLIDAÇÃO CONCLUÍDA EM {time.time() - start_merge:.2f}s! ({total_rows:,} registros, Tamanho: {file_size_gb:.2f} GB)")
    print("=" * 105)
    return True


def run_night_simulation(max_files=None, batch_chunk_size=50, workers=None, clean=False, discard_modes="1,2,3", discard_days=7):
    """Executa a simulação massiva diária multithread paralela em lotes de alto desempenho."""
    global DISCARD_VARIATIONS
    if isinstance(discard_modes, str):
        if discard_modes.lower() in ["all", "todos", "1,2,3"]:
            modes_list = [1, 2, 3]
        else:
            modes_list = [int(m.strip()) for m in discard_modes.split(",") if m.strip().isdigit()]
    elif isinstance(discard_modes, (list, tuple)):
        modes_list = list(discard_modes)
    else:
        modes_list = [1, 2, 3]

    DISCARD_VARIATIONS = get_discard_variations(modes_list=modes_list, discard_days=discard_days)
    n_discard_rules = len(DISCARD_VARIATIONS)
    sims_per_file = 5 * n_discard_rules * 3 * 3 * 12

    print("=" * 105)
    print("  NETUNO 5 -- SIMULAÇÃO HIDROLÓGICA MASSIVA PARALELA (5 TIPOLOGIAS x CLIMA CMIP6)")
    print(f"  (Configuração: First Flush Modos {modes_list} [Intervalo Modo 3: {discard_days} dias] | 12 Volumes de Cisterna)")
    print("=" * 105)

    pattern_csv = os.path.join(INPUT_SPLIT_DIR, "*.csv")
    pattern_txt = os.path.join(INPUT_SPLIT_DIR, "*.txt")
    all_files = sorted(glob.glob(pattern_csv) + glob.glob(pattern_txt))

    total_available = len(all_files)
    if total_available == 0:
        print(f"[ERRO] Nenhum arquivo de chuva encontrado em: {INPUT_SPLIT_DIR}")
        return

    if max_files is not None and max_files > 0:
        all_files = all_files[:max_files]
        print(f" [*] Modo de teste limitado a: {len(all_files):,} arquivos.")

    if clean:
        print(" [*] Flag --clean ativa: limpando checkpoints anteriores e chunks temporários...")
        if os.path.exists(CHECKPOINT_FILE):
            try:
                os.remove(CHECKPOINT_FILE)
            except Exception:
                pass
        shutil.rmtree(CHUNKS_DIR, ignore_errors=True)
        os.makedirs(CHUNKS_DIR, exist_ok=True)

    completed_files = set()
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                chk = json.load(f)
                completed_files = set(chk.get("completed_files", []))
        except Exception:
            pass

    pending_files = [f for f in all_files if os.path.basename(f) not in completed_files]
    total_target = len(all_files)
    already_done = len(completed_files)
    n_workers = workers if workers else max(1, os.cpu_count() - 1)

    print(f" [+] Séries Climáticas: {total_target:,} (Pendentes: {len(pending_files):,} | Concluídas: {already_done:,})")
    print(f" [+] Regras de First Flush Ativas: {n_discard_rules} regras (Modos {modes_list} | Modo 3 com {discard_days} dias)")
    print(f" [+] Simulações Diárias por Série: {sims_per_file:,} execuções")
    print(f" [+] Total de Simulações do Estudo: {total_target * sims_per_file:,} execuções")
    print(f" [+] Paralelismo Ativo: {n_workers} workers paralelos de alto rendimento")
    print(f" [+] Tamanho do Bloco (Chunk): {batch_chunk_size} arquivos ({batch_chunk_size * sims_per_file:,} registros/chunk)")
    print("=" * 105)

    if not pending_files:
        print(" [OK] Todas as séries já foram processadas!")
        merge_chunks_to_final_parquet()
        return

    start_total = time.time()
    total_processed = already_done
    last_print_time = 0.0

    profiles_meta = build_simulation_profiles(DISCARD_VARIATIONS)
    n_profiles = len(profiles_meta)
    params_mat = np.zeros((n_profiles, 8), dtype=np.float64)
    for p_idx, p in enumerate(profiles_meta):
        params_mat[p_idx, 0] = p["vol"]
        params_mat[p_idx, 1] = p["roof_area"]
        params_mat[p_idx, 2] = p["runoff_coeff"]
        params_mat[p_idx, 3] = p["discard_mm"]
        params_mat[p_idx, 4] = p["discard_mode"]
        params_mat[p_idx, 5] = p["discard_days"]
        params_mat[p_idx, 6] = p["tot_demand_day"]
        params_mat[p_idx, 7] = p["pluv_demand_day"]

    chunk_idx = len(glob.glob(os.path.join(CHUNKS_DIR, "*.parquet"))) + 1
    batches = []
    for i in range(0, len(pending_files), batch_chunk_size):
        chunk_files = pending_files[i:i+batch_chunk_size]
        batches.append((chunk_idx, chunk_files, params_mat, profiles_meta))
        chunk_idx += 1

    with ProcessPoolExecutor(max_workers=n_workers, initializer=init_worker_process) as executor:
        for n_f, n_sims, fnames in executor.map(process_chunk_batch_worker, batches):
            completed_files.update(fnames)
            total_processed += n_f

            with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "completed_files": list(completed_files),
                    "last_update": time.strftime('%Y-%m-%d %H:%M:%S')
                }, f)

            now = time.time()
            if now - last_print_time >= 0.25 or total_processed == total_target:
                elapsed = now - start_total
                pct = (total_processed / total_target) * 100.0 if total_target > 0 else 100.0
                files_done = total_processed - already_done
                rate_files = files_done / max(0.001, elapsed)
                rate_sims = rate_files * sims_per_file
                eta_str = format_time_hms((total_target - total_processed) / max(0.001, rate_files))
                elapsed_str = format_time_hms(elapsed)
                bar = render_progress_bar(pct, width=22)

                sys.stdout.write(
                    f"\r [{bar}] {pct:5.1f}% | {total_processed:,}/{total_target:,} séries ({total_processed * sims_per_file:,} sim) | "
                    f"{rate_files:4.1f} arq/s ({rate_sims:,.0f} sim/s) | Decorrido: {elapsed_str} | ETA: {eta_str} "
                )
                sys.stdout.flush()
                last_print_time = now

    print(f"\n\n[OK] TODAS AS {total_target:,} SÉRIES PROCESSADAS EM {format_time_hms(time.time() - start_total)}!\n")
    merge_chunks_to_final_parquet()


def run_recalculation():
    """Recalcula métricas financeiras (VPL a 6%, 10%, 14%, LCOW, OPEX e TOPSIS) no Parquet consolidado."""
    print("=" * 105)
    print("  NETUNO 5 -- RECÁLCULO RÁPIDO MULTI-CENÁRIO NO PARQUET CONSOLIDADO")
    print("  (VPL 6%, 10%, 14% SELIC + LCOW + CAPEX Calibrado por Tipologia/UF + Tarifas Auditadas)")
    print("=" * 105)

    if not os.path.exists(FINAL_PARQUET_PATH):
        print(f"[AVISO] Arquivo final não encontrado em: {FINAL_PARQUET_PATH}")
        print("Iniciando simulação completa a partir dos arquivos de chuva...")
        run_night_simulation()
        if not os.path.exists(FINAL_PARQUET_PATH):
            print(f"[ERRO] Arquivo consolidado não pôde ser gerado em: {FINAL_PARQUET_PATH}")
            return

    t_start_total = time.time()
    city_tariffs = CITY_TARIFFS_PRELOADED
    capex_lookup = CAPEX_LOOKUP
    fallback_city_key = list(city_tariffs.keys())[0]

    with pq.ParquetFile(FINAL_PARQUET_PATH) as pf:
        total_rows = pf.metadata.num_rows
        num_row_groups = pf.num_row_groups
        print(f" [*] Base de Dados: {FINAL_PARQUET_PATH}")
        print(f" [*] Total de registros a recalcular: {total_rows:,} distribuídos em {num_row_groups} row groups.")

        writer = None
        processed_count = 0
        leftover_df = None

        for rg_idx in range(num_row_groups):
            t_rg_start = time.time()
            df_raw = pf.read_row_group(rg_idx).to_pandas()

            if leftover_df is not None and len(leftover_df) > 0:
                df = pd.concat([leftover_df, df_raw], ignore_index=True)
            else:
                df = df_raw

            rem = len(df) % 10
            if rem > 0 and (rg_idx < num_row_groups - 1):
                leftover_df = df.iloc[-rem:].copy()
                df = df.iloc[:-rem].copy()
            else:
                leftover_df = None

            n_df = len(df)

            monthly_tot_l = df['total_demand_l_day'].values * 30.4375
            monthly_pot_l = df['avg_potable_consumed_l_day'].values * 30.4375
            annual_pluv_m3 = df['annual_pluvial_consumed_m3'].values
            building_codes = df['building_code'].values
            tank_vols = df['lower_tank_vol_l'].values.astype(np.float64)

            annual_water_savings = np.zeros(n_df, dtype=np.float64)
            annual_opex = np.zeros(n_df, dtype=np.float64)
            capex_calibrated = np.zeros(n_df, dtype=np.float64)
            tarifa_elec_arr = np.zeros(n_df, dtype=np.float64)
            tarifa_agua_base_arr = np.zeros(n_df, dtype=np.float64)
            esgoto_pct_arr = np.zeros(n_df, dtype=np.float64)
            prestador_arr = np.empty(n_df, dtype=object)
            uf_arr = np.empty(n_df, dtype=object)
            regiao_arr = np.empty(n_df, dtype=object)

            cities = df['city'].unique()
            for city_name in cities:
                c_clean = str(city_name).strip()
                mask = (df['city'] == city_name).values
                info = city_tariffs.get(c_clean, city_tariffs[fallback_city_key])

                tariffs = info['tariffs']
                sew_rate = info['sewage_rate']
                elec_rate = info['elec_tariff']
                base_w_rate = info['base_water_rate']
                uf_city = info['uf']
                regiao_city = info['regiao']

                sub_b_codes = building_codes[mask]
                sub_units = np.array([TYPOLOGY_UNITS.get(b, 1) for b in sub_b_codes], dtype=np.float64)

                sub_tot_l = monthly_tot_l[mask]
                sub_pot_l = monthly_pot_l[mask]

                sub_tot_l_unit = sub_tot_l / sub_units
                sub_pot_l_unit = sub_pot_l / sub_units

                unique_vols = np.unique(np.concatenate([sub_tot_l_unit, sub_pot_l_unit]))
                bill_dict = {v: calc_bill_single(v, tariffs, sew_rate) for v in unique_vols}

                sub_bill_without = np.array([bill_dict[v] for v in sub_tot_l_unit]) * sub_units
                sub_bill_with = np.array([bill_dict[v] for v in sub_pot_l_unit]) * sub_units
                sub_water_savings = np.maximum(0.0, sub_bill_without - sub_bill_with) * 12.0

                annual_water_savings[mask] = sub_water_savings

                sub_vols = tank_vols[mask]
                sub_pluv_m3 = annual_pluv_m3[mask]

                sub_cpx = np.empty(len(sub_b_codes), dtype=np.float64)
                sub_maint_fixed = np.empty(len(sub_b_codes), dtype=np.float64)

                for i in range(len(sub_b_codes)):
                    cpx_val, maint_val = capex_lookup.get(
                        (sub_b_codes[i], sub_vols[i], uf_city),
                        (6500.0, 420.0)
                    )
                    sub_cpx[i] = cpx_val
                    sub_maint_fixed[i] = maint_val

                capex_calibrated[mask] = sub_cpx

                sub_pump_kwh = sub_pluv_m3 * 0.45
                sub_pump_cost = sub_pump_kwh * elec_rate
                sub_chlorine_cost = sub_pluv_m3 * 0.05

                annual_opex[mask] = sub_pump_cost + sub_chlorine_cost + sub_maint_fixed
                tarifa_elec_arr[mask] = elec_rate
                tarifa_agua_base_arr[mask] = base_w_rate
                esgoto_pct_arr[mask] = sew_rate
                prestador_arr[mask] = info['prestador']
                uf_arr[mask] = uf_city
                regiao_arr[mask] = regiao_city

            net_annual = annual_water_savings - annual_opex
            vpl_6 = -capex_calibrated + (net_annual * PV_FACTOR_6)
            vpl_10 = -capex_calibrated + (net_annual * PV_FACTOR_10)
            vpl_14 = -capex_calibrated + (net_annual * PV_FACTOR_14)

            payback = np.where(net_annual > 0, capex_calibrated / net_annual, 99.0)
            tir = np.where(capex_calibrated > 0, (net_annual / capex_calibrated) * 100.0, 0.0)
            denom_lcow = np.maximum(0.001, annual_pluv_m3 * PV_FACTOR_6)
            lcow = (capex_calibrated + (annual_opex * PV_FACTOR_6)) / denom_lcow

            sav_pct = df['potential_water_savings_pct'].values if 'potential_water_savings_pct' in df else (df['potential_savings_pct'].values if 'potential_savings_pct' in df else np.zeros(n_df, dtype=np.float64))
            full_pct = df['reliability_fully_met_pct'].values if 'reliability_fully_met_pct' in df else (df['fully_met_pct'].values if 'fully_met_pct' in df else np.zeros(n_df, dtype=np.float64))
            co2_val = df['lifetime_net_co2_saved_kg'].values if 'lifetime_net_co2_saved_kg' in df else (annual_pluv_m3 * 0.35 * 20.0)

            t_score, t_rank, t_is_best = recompute_topsis_vectorized(
                sav_pct,
                vpl_6,
                co2_val,
                full_pct,
                capex_calibrated,
                n_vols=12 if (len(df) % 12 == 0) else (10 if (len(df) % 10 == 0) else 12)
            )

            df['capex_total_brl'] = capex_calibrated
            df['annual_water_savings_brl'] = annual_water_savings
            df['annual_opex_brl'] = annual_opex
            df['vpl_brl'] = vpl_6
            df['vpl_6pct_brl'] = vpl_6
            df['vpl_10pct_brl'] = vpl_10
            df['vpl_14pct_brl'] = vpl_14
            df['lcow_r_per_m3'] = lcow
            df['tir_annual_pct'] = tir
            df['payback_years'] = payback
            df['topsis_score'] = t_score
            df['topsis_rank'] = t_rank
            df['is_topsis_best'] = t_is_best

            df['tarifa_eletricidade_b1_r_kwh'] = tarifa_elec_arr
            df['tarifa_agua_base_r_m3'] = tarifa_agua_base_arr
            df['esgoto_pct_sobre_agua'] = esgoto_pct_arr
            df['saneamento_prestador'] = prestador_arr
            df['uf'] = uf_arr
            df['regiao'] = regiao_arr

            table_chunk = pa.Table.from_pandas(df, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(TEMP_PARQUET_PATH, table_chunk.schema, compression='snappy')

            writer.write_table(table_chunk)
            processed_count += n_df

            elapsed_rg = time.time() - t_rg_start
            pct_done = (processed_count / total_rows) * 100.0
            sys.stdout.write(f"\r  [>] Row Group {rg_idx+1}/{num_row_groups} ({n_df:,} linhas) em {elapsed_rg:.2f}s | Progresso: {processed_count:,}/{total_rows:,} ({pct_done:.1f}%)")
            sys.stdout.flush()

        if writer is not None:
            writer.close()

    del writer
    gc.collect()
    time.sleep(0.5)

    print("\n [*] Atualizando arquivo Parquet principal em disco...")
    replaced = False
    for attempt in range(10):
        try:
            if os.path.exists(FINAL_PARQUET_PATH):
                os.replace(TEMP_PARQUET_PATH, FINAL_PARQUET_PATH)
            else:
                shutil.move(TEMP_PARQUET_PATH, FINAL_PARQUET_PATH)
            replaced = True
            break
        except Exception:
            gc.collect()
            time.sleep(1.0)

    if not replaced:
        shutil.copy2(TEMP_PARQUET_PATH, FINAL_PARQUET_PATH)
        try:
            os.remove(TEMP_PARQUET_PATH)
        except Exception:
            pass

    total_sec = time.time() - t_start_total
    print("=" * 105)
    print(f" [[ok] SUCESSO] RECÁLCULO INTEGRAL CONCLUÍDO EM {total_sec/60.0:.2f} MINUTOS ({total_sec:.1f}s)!")
    print(f" [*] Registros consolidados: {processed_count:,}")
    print(f" [*] Tamanho final do banco: {os.path.getsize(FINAL_PARQUET_PATH)/(1024*1024*1024):.2f} GB")
    print("=" * 105)


def run_capitais_analysis():
    script_capitais = os.path.join(BASE_DIR, "scripts", "generate_capitais_global_vpl.py")
    if os.path.exists(script_capitais):
        print("\n" + "=" * 105)
        print("  GERANDO ANÁLISE, CURVAS CANÔNICAS DE VPL E DASHBOARD DAS 27 CAPITAIS")
        print("=" * 105)
        subprocess.run([sys.executable, script_capitais], check=True)
    else:
        print(f"[ERRO] Script de capitais não encontrado: {script_capitais}")


def run_publication_figures_analysis():
    script_figures = os.path.join(BASE_DIR, "scripts", "analyze_vaz_parquet.py")
    if os.path.exists(script_figures):
        print("\n" + "=" * 105)
        print("  GERANDO AS 10 FIGURAS TEMÁTICAS DE PUBLICAÇÃO CIENTÍFICA E RELATÓRIO ESTATÍSTICO")
        print("=" * 105)
        subprocess.run([sys.executable, script_figures], check=True)
    else:
        print(f"[ERRO] Script de figuras não encontrado: {script_figures}")


def main():
    parser = argparse.ArgumentParser(
        description="Master Runner Netuno 5 - Estudo Multidimensional das 5 Tipologias Residenciais (652 Cidades)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de Uso:
  python scripts/run_estudo_5_tipologias.py --simulate    # Roda simulação diária completa (86.716 séries x 1.620 perfis)
  python scripts/run_estudo_5_tipologias.py --recalc      # Recalcula a base de 39M registros com VPL 6%, 10%, 14% e LCOW
  python scripts/run_estudo_5_tipologias.py --capitais    # Gera gráficos e dashboard das 27 capitais
  python scripts/run_estudo_5_tipologias.py --figures     # Gera as 10 figuras temáticas de publicação (mapas, clima, etc.)
  python scripts/run_estudo_5_tipologias.py --all         # Executa Pipeline Completo (Simulação/Consolidação + Capitais + 10 Figuras)
        """
    )
    parser.add_argument("--simulate", "-s", action="store_true", help="Executa a simulação diária hidrológica completa do zero (1.620 perfis)")
    parser.add_argument("--recalc", "-r", action="store_true", help="Executa o recálculo rápido da base com VPL (6%%, 10%%, 14%%), LCOW e CAPEX")
    parser.add_argument("--capitais", "-c", action="store_true", help="Gera as curvas canônicas de VPL e dashboards das 27 capitais")
    parser.add_argument("--figures", "-f", action="store_true", help="Gera as 10 figuras temáticas de publicação e relatório estatístico")
    parser.add_argument("--all", "-a", action="store_true", help="Executa o pipeline completo (Simulação + Capitais + 10 Figuras)")
    parser.add_argument("--clean", action="store_true", help="Limpa checkpoint e chunks temporários antes de simular")
    parser.add_argument("--discard-modes", "-dm", type=str, default="1,2,3", help="Modos de First Flush a simular (1: Todos os eventos, 2: Após dia seco <1mm, 3: Intervalo 7d, all: Todos) [Padrão: 1,2,3]")
    parser.add_argument("--discard-days", "-dd", type=int, default=7, help="Intervalo mínimo de dias secos sem descarte para o Modo 3 (Padrão: 7 dias)")
    parser.add_argument("--chunk-size", type=int, default=100, help="Tamanho do lote/chunk em arquivos de chuva (padrão: 100 arquivos)")
    parser.add_argument("--max-files", "-n", type=int, default=None, help="Limite de arquivos para teste (usado com --simulate)")
    parser.add_argument("--workers", "-w", type=int, default=None, help="Número de workers paralelos (usado com --simulate)")

    args = parser.parse_args()

    if args.all:
        print("\n>>> INICIANDO PIPELINE COMPLETO END-TO-END...")
        pattern_csv = os.path.join(INPUT_SPLIT_DIR, "*.csv")
        pattern_txt = os.path.join(INPUT_SPLIT_DIR, "*.txt")
        all_files = sorted(glob.glob(pattern_csv) + glob.glob(pattern_txt))
        completed_files = set()
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                    chk = json.load(f)
                    completed_files = set(chk.get("completed_files", []))
            except Exception:
                pass
        pending = [f for f in all_files if os.path.basename(f) not in completed_files]
        if pending or not os.path.exists(FINAL_PARQUET_PATH):
            print(f" [*] Séries pendentes detectadas ({len(pending):,} de {len(all_files):,}). Executando simulação de chuva...")
            run_night_simulation(
                max_files=args.max_files,
                batch_chunk_size=args.chunk_size,
                workers=args.workers,
                clean=args.clean,
                discard_modes=args.discard_modes,
                discard_days=args.discard_days
            )

        run_capitais_analysis()
        run_publication_figures_analysis()
    elif args.figures:
        run_publication_figures_analysis()
    elif args.capitais:
        run_capitais_analysis()
    elif args.simulate:
        run_night_simulation(
            max_files=args.max_files,
            batch_chunk_size=args.chunk_size,
            workers=args.workers,
            clean=args.clean,
            discard_modes=args.discard_modes,
            discard_days=args.discard_days
        )
    elif args.recalc:
        run_recalculation()
    else:
        pattern_csv = os.path.join(INPUT_SPLIT_DIR, "*.csv")
        pattern_txt = os.path.join(INPUT_SPLIT_DIR, "*.txt")
        all_files = sorted(glob.glob(pattern_csv) + glob.glob(pattern_txt))
        completed_files = set()
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                    chk = json.load(f)
                    completed_files = set(chk.get("completed_files", []))
            except Exception:
                pass
        pending = [f for f in all_files if os.path.basename(f) not in completed_files]
        if pending or not os.path.exists(FINAL_PARQUET_PATH):
            print(f" [*] Séries pendentes detectadas ({len(pending):,} de {len(all_files):,}). Executando simulação hidrológica massiva completa...")
            run_night_simulation(
                max_files=args.max_files,
                batch_chunk_size=args.chunk_size,
                workers=args.workers,
                clean=args.clean,
                discard_modes=args.discard_modes,
                discard_days=args.discard_days
            )
        else:
            print(" [*] Todas as séries já simuladas e consolidadas. Executando análises das capitais e figuras...")
            run_capitais_analysis()
            run_publication_figures_analysis()


if __name__ == "__main__":
    main()
