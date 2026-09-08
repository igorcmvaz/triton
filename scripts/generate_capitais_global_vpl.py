"""
======================================================================================================
NETUNO 5 -- OBSERVATÓRIO E OTIMIZADOR GLOBAL DAS 27 CAPITAIS BRASILEIRAS (MODO GLOBAL)
======================================================================================================
Este script:
 1. Extrai do banco de dados consolidado do Netuno 5 (86.716 séries x 652 cidades) todas as 27 capitais brasileiras.
 2. Executa a análise de otimização global (Técnica, Econômico-Financeira VPL, Ambiental e TOPSIS Multi-Critério).
 3. Processa cenários climáticos CMIP6 (Histórico, Near, Middle, Far sob SSP2-4.5 e SSP5-8.5).
 4. Integra tarifas reais de saneamento e energia elétrica (SABESP, COPASA, CASAN, CEDAE, etc.).
 5. Gera 11 gráficos científicos de alta fidelidade visual (PNG 300 DPI) no padrão Netuno 5 GUI.
 6. Gera um Dashboard HTML interativo de última geração com Mapa Leaflet do Brasil, Chart.js,
    comparador lado a lado de capitais, matriz multi-tipologia, drawer de detalhes e exportador de dados.
======================================================================================================
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pyarrow.dataset as ds

# Reconfigura saída para UTF-8 seguro no Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from netuno.core.topsis import TopsisCandidate
from netuno.core.mcdm_methods import run_vikor, run_smaa_vikor

OUTPUT_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz")
PARQUET_PATH = os.path.join(OUTPUT_DIR, "estudo_vaz_consolidado.parquet")
os.makedirs(OUTPUT_DIR, exist_ok=True)
FIGURAS_DIR = os.path.join(OUTPUT_DIR, "figuras")
os.makedirs(FIGURAS_DIR, exist_ok=True)

# 27 Capitais Brasileiras
CAPITAIS_BR = [
    "Aracaju", "Belém", "Belo Horizonte", "Boa Vista", "Brasília",
    "Campo Grande", "Cuiabá", "Curitiba", "Florianópolis", "Fortaleza",
    "Goiânia", "João Pessoa", "Macapá", "Maceió", "Manaus",
    "Natal", "Palmas", "Porto Alegre", "Porto Velho", "Recife",
    "Rio Branco", "Rio de Janeiro", "Salvador", "São Luís", "São Paulo",
    "Teresina", "Vitória"
]

REGION_COLORS = {
    "Norte": "#0284c7",         # Azul Oceano
    "Nordeste": "#d97706",      # Âmbar / Laranja
    "Centro-Oeste": "#059669",  # Esmeralda / Verde
    "Sudeste": "#7c3aed",       # Roxo Real
    "Sul": "#2563eb"            # Azul Cobalto
}

REGION_ORDER = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

CAPITAIS_POR_REGIAO = {
    "Norte": ["Belém", "Boa Vista", "Macapá", "Manaus", "Palmas", "Porto Velho", "Rio Branco"],
    "Nordeste": ["Aracaju", "Fortaleza", "João Pessoa", "Maceió", "Natal", "Recife", "Salvador", "São Luís", "Teresina"],
    "Centro-Oeste": ["Brasília", "Campo Grande", "Cuiabá", "Goiânia"],
    "Sudeste": ["Belo Horizonte", "Rio de Janeiro", "São Paulo", "Vitória"],
    "Sul": ["Curitiba", "Florianópolis", "Porto Alegre"]
}

CAPITAIS_UF = {
    "Aracaju": "SE", "Belém": "PA", "Belo Horizonte": "MG", "Boa Vista": "RR", "Brasília": "DF",
    "Campo Grande": "MS", "Cuiabá": "MT", "Curitiba": "PR", "Florianópolis": "SC", "Fortaleza": "CE",
    "Goiânia": "GO", "João Pessoa": "PB", "Macapá": "AP", "Maceió": "AL", "Manaus": "AM",
    "Natal": "RN", "Palmas": "TO", "Porto Alegre": "RS", "Porto Velho": "RO", "Recife": "PE",
    "Rio Branco": "AC", "Rio de Janeiro": "RJ", "Salvador": "BA", "São Luís": "MA", "São Paulo": "SP",
    "Teresina": "PI", "Vitória": "ES"
}

CITY_STYLE_MAP = {
    # Norte (7 capitais)
    "Belém": {"color": "#0284c7", "marker": "o", "ls": "-"},
    "Boa Vista": {"color": "#06b6d4", "marker": "s", "ls": "--"},
    "Macapá": {"color": "#0d9488", "marker": "^", "ls": "-."},
    "Manaus": {"color": "#1e40af", "marker": "D", "ls": "-"},
    "Palmas": {"color": "#38bdf8", "marker": "v", "ls": "--"},
    "Porto Velho": {"color": "#0891b2", "marker": "p", "ls": "-."},
    "Rio Branco": {"color": "#2563eb", "marker": "h", "ls": "-"},
    # Nordeste (9 capitais)
    "Aracaju": {"color": "#d97706", "marker": "o", "ls": "-"},
    "Fortaleza": {"color": "#ea580c", "marker": "s", "ls": "--"},
    "João Pessoa": {"color": "#f59e0b", "marker": "^", "ls": "-."},
    "Maceió": {"color": "#c2410c", "marker": "D", "ls": "-"},
    "Natal": {"color": "#eab308", "marker": "v", "ls": "--"},
    "Recife": {"color": "#b45309", "marker": "p", "ls": "-."},
    "Salvador": {"color": "#e11d48", "marker": "h", "ls": "-"},
    "São Luís": {"color": "#f97316", "marker": "<", "ls": "--"},
    "Teresina": {"color": "#9a3412", "marker": ">", "ls": "-."},
    # Centro-Oeste (4 capitais)
    "Brasília": {"color": "#059669", "marker": "o", "ls": "-"},
    "Campo Grande": {"color": "#10b981", "marker": "s", "ls": "--"},
    "Cuiabá": {"color": "#047857", "marker": "^", "ls": "-."},
    "Goiânia": {"color": "#34d399", "marker": "D", "ls": "-"},
    # Sudeste (4 capitais)
    "Belo Horizonte": {"color": "#7c3aed", "marker": "o", "ls": "-"},
    "Rio de Janeiro": {"color": "#9333ea", "marker": "s", "ls": "--"},
    "São Paulo": {"color": "#475569", "marker": "^", "ls": "-."},
    "Vitória": {"color": "#c026d3", "marker": "D", "ls": "-"},
    # Sul (3 capitais)
    "Curitiba": {"color": "#2563eb", "marker": "o", "ls": "-"},
    "Florianópolis": {"color": "#059669", "marker": "s", "ls": "--"},
    "Porto Alegre": {"color": "#1d4ed8", "marker": "^", "ls": "-."}
}

TYPOLOGY_NAMES = {
    "UTI": "Casa Unifamiliar Térrea (4 hab, 60.19 m²)",
    "UTG": "Casa Unifamiliar Geminada (8 hab, 115.43 m²)",
    "MSG": "Sobrado Multifamiliar Geminado (16 hab, 132.53 m²)",
    "MFH": "Bloco Multifamiliar H (64 hab, 158.70 m²)",
    "MFL": "Bloco Multifamiliar Retangular (128 hab, 421.52 m²)"
}

TYPOLOGY_SHORT = {
    "UTI": "UTI (4 hab)",
    "UTG": "UTG (8 hab)",
    "MSG": "MSG (16 hab)",
    "MFH": "MFH (64 hab)",
    "MFL": "MFL (128 hab)"
}

TYPOLOGY_SPECS = {
    "UTI": {"residents": 4, "roof": 60.19, "type": "Unifamiliar Térrea", "name": "Unifamiliar Térrea"},
    "UTG": {"residents": 8, "roof": 115.43, "type": "Unifamiliar Geminada", "name": "Unifamiliar Geminada"},
    "MSG": {"residents": 16, "roof": 132.53, "type": "Multifamiliar Geminado", "name": "Multifamiliar Geminado"},
    "MFH": {"residents": 64, "roof": 158.70, "type": "Multifamiliar Bloco H", "name": "Multifamiliar Bloco H"},
    "MFL": {"residents": 128, "roof": 421.52, "type": "Multifamiliar Bloco L", "name": "Multifamiliar Bloco L"}
}

HORIZON_MAP = {
    "Histórico": "Historical",
    "Historico": "Historical",
    "Historical": "Historical",
    "Near": "Near",
    "Middle": "Middle",
    "Far": "Far"
}


def setup_matplotlib_netuno_style(dark_mode=False):
    """Aplica o estilo visual refinado para gráficos científicos do Netuno 5."""
    plt.style.use('default')
    bg_color = '#18181b' if dark_mode else '#ffffff'
    text_color = '#f4f4f5' if dark_mode else '#0f172a'
    grid_color = '#3f3f46' if dark_mode else '#e2e8f0'
    
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
        'font.size': 9.5,
        'figure.facecolor': bg_color,
        'axes.facecolor': bg_color,
        'axes.edgecolor': grid_color,
        'axes.labelcolor': text_color,
        'axes.labelsize': 10,
        'axes.labelweight': 'bold',
        'axes.titlesize': 11.5,
        'axes.titleweight': 'bold',
        'axes.titlecolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'grid.color': grid_color,
        'grid.linestyle': ':',
        'grid.alpha': 0.7,
        'legend.facecolor': bg_color,
        'legend.edgecolor': grid_color,
        'legend.labelcolor': text_color,
        'legend.fontsize': 8.8,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight'
    })


def load_geo_and_catalogue():
    """Carrega dados geográficos e catálogo tarifário completo das capitais."""
    geo_dict = {}
    p_geo = os.path.join(BASE_DIR, "tarifas", "validated_cidades_50k.json")
    if os.path.exists(p_geo):
        with open(p_geo, encoding="utf-8") as f:
            raw_geo = json.load(f)
            for k, v in raw_geo.items():
                lat = v.get("target", {}).get("lat", v.get("nearest", {}).get("lat", np.nan))
                lon = v.get("target", {}).get("lon", v.get("nearest", {}).get("lon", np.nan))
                geo_dict[k] = {"lat": lat, "lon": lon}

    cat_dict = {}
    p_cat = os.path.join(BASE_DIR, "tarifas", "catalogo_tarifas_auditado_652.csv")
    if os.path.exists(p_cat):
        raw_cat = pd.read_csv(p_cat, encoding="utf-8-sig").to_dict("records")
        for item in raw_cat:
            muni = item.get("municipio", "")
            cat_dict[muni] = item

    return geo_dict, cat_dict


def load_and_process_capitals_data():
    """Extrai do Parquet e consolida todas as métricas das 27 capitais."""
    print("⏳ Carregando dados completos das 27 capitais do banco Parquet consolidado...")
    t0 = time.time()
    dataset = ds.dataset(PARQUET_PATH, format="parquet")
    filter_expr = ds.field("city").isin(CAPITAIS_BR)

    cols = [
        'city', 'uf', 'regiao', 'building_code', 'building_name', 'residents', 'roof_area_m2',
        'horizon', 'scenario', 'model', 'lower_tank_vol_l',
        'annual_pluvial_consumed_m3', 'potential_water_savings_pct',
        'annual_overflow_spill_m3', 'reliability_fully_met_pct',
        'capex_total_brl', 'annual_opex_brl', 'annual_water_savings_brl',
        'vpl_6pct_brl', 'vpl_10pct_brl', 'vpl_14pct_brl', 'vpl_brl',
        'payback_years', 'tir_pct_yr', 'lcow_brl_m3',
        'topsis_score', 'tarifa_eletricidade_b1_r_kwh', 'tarifa_agua_base_r_m3',
        'esgoto_pct_sobre_agua', 'saneamento_prestador'
    ]

    schema_cols = set(dataset.schema.names)
    safe_cols = [c for c in cols if c in schema_cols]
    table = dataset.scanner(filter=filter_expr, columns=safe_cols).to_table()
    df = table.to_pandas()
    print(f"✓ Carregados {len(df):,} registros em {time.time()-t0:.2f}s.")

    # Padronização de colunas
    if "vpl_6pct_brl" not in df.columns and "vpl_brl" in df.columns:
        df["vpl_6pct_brl"] = df["vpl_brl"]
    if "vpl_brl" not in df.columns and "vpl_6pct_brl" in df.columns:
        df["vpl_brl"] = df["vpl_6pct_brl"]
    if "potential_savings_pct" not in df.columns and "potential_water_savings_pct" in df.columns:
        df["potential_savings_pct"] = df["potential_water_savings_pct"]
    if "tir_annual_pct" not in df.columns and "tir_pct_yr" in df.columns:
        df["tir_annual_pct"] = df["tir_pct_yr"]

    df["horizon_std"] = df["horizon"].map(lambda x: HORIZON_MAP.get(str(x), str(x)))
    df["scenario_std"] = df["scenario"].fillna("Historical").replace({"Histórico": "Historical", "Historico": "Historical"})

    return df


def aggregate_capitals_data(df, geo_dict, cat_dict):
    """Calcula estatísticas agregadas, curvas de volume, ótimos e impactos climáticos."""
    print("⏳ Processando agregações multi-dimensionais e cálculos de otimização...")
    
    # 1. Agregação Histórica por (city, building_code, lower_tank_vol_l)
    df_hist = df[df["horizon_std"] == "Historical"].copy()
    if len(df_hist) == 0:
        df_hist = df.copy()

    agg_dict = {
        "potential_water_savings_pct": "mean",
        "annual_pluvial_consumed_m3": "mean",
        "annual_overflow_spill_m3": "mean",
        "reliability_fully_met_pct": "mean",
        "capex_total_brl": "mean",
        "annual_opex_brl": "mean",
        "annual_water_savings_brl": "mean",
        "vpl_6pct_brl": "mean",
        "vpl_10pct_brl": "mean",
        "vpl_14pct_brl": "mean",
        "payback_years": "mean",
        "tir_pct_yr": "mean",
        "lcow_brl_m3": "mean",
        "topsis_score": "mean",
        "tarifa_eletricidade_b1_r_kwh": "mean",
        "tarifa_agua_base_r_m3": "mean",
        "esgoto_pct_sobre_agua": "mean"
    }

    grouped_hist = df_hist.groupby(
        ["city", "uf", "regiao", "building_code", "lower_tank_vol_l"]
    ).agg(agg_dict).reset_index()

    # Cálculos financeiros avançados de payback simples e descontado
    r_disc = 0.06
    net_ann = grouped_hist["annual_water_savings_brl"] - grouped_hist["annual_opex_brl"]
    cpx = grouped_hist["capex_total_brl"]
    grouped_hist["payback_simple_years"] = np.where(net_ann > 0, cpx / np.maximum(0.001, net_ann), 99.0)

    ratio = cpx / np.maximum(0.001, net_ann)
    valid_pb_6 = (net_ann > 0) & (1.0 - 0.06 * ratio > 0) & (grouped_hist["vpl_6pct_brl"] >= 0)
    grouped_hist["payback_discounted_6pct"] = np.where(
        valid_pb_6,
        -np.log(np.maximum(1e-6, 1.0 - 0.06 * ratio)) / np.log(1.0 + 0.06),
        99.0
    )

    valid_pb_10 = (net_ann > 0) & (1.0 - 0.10 * ratio > 0) & (grouped_hist["vpl_10pct_brl"] >= 0)
    grouped_hist["payback_discounted_10pct"] = np.where(
        valid_pb_10,
        -np.log(np.maximum(1e-6, 1.0 - 0.10 * ratio)) / np.log(1.0 + 0.10),
        99.0
    )

    # Pegada de Carbono e Descarbonização
    grouped_hist["avoided_co2_annual_kg"] = grouped_hist["annual_pluvial_consumed_m3"] * 0.35
    grouped_hist["pump_energy_kwh_yr"] = grouped_hist["annual_pluvial_consumed_m3"] * 0.45
    grouped_hist["pump_co2_annual_kg"] = grouped_hist["pump_energy_kwh_yr"] * 0.08
    grouped_hist["embodied_co2_kg"] = 50.0 + (grouped_hist["lower_tank_vol_l"] / 1000.0) * 22.0
    grouped_hist["lifetime_net_co2_saved_kg"] = (
        (grouped_hist["avoided_co2_annual_kg"] - grouped_hist["pump_co2_annual_kg"]) * 20.0 - grouped_hist["embodied_co2_kg"]
    )

    # 2. Agregação de Impactos Climáticos (CMIP6)
    df_clim = df.groupby(
        ["city", "building_code", "horizon_std", "scenario_std"]
    ).agg({
        "potential_water_savings_pct": "mean",
        "annual_pluvial_consumed_m3": "mean",
        "annual_overflow_spill_m3": "mean",
        "reliability_fully_met_pct": "mean",
        "vpl_6pct_brl": "mean",
        "lower_tank_vol_l": "mean"
    }).reset_index()

    # 3. Construção dos Ótimos por Capital e Tipologia
    capitals_data = []
    
    for city in CAPITAIS_BR:
        c_hist = grouped_hist[grouped_hist["city"] == city]
        if c_hist.empty:
            continue

        uf = c_hist["uf"].iloc[0]
        regiao = c_hist["regiao"].iloc[0]
        coords = geo_dict.get(city, {"lat": -15.78, "lon": -47.92})
        cat_info = cat_dict.get(city, {})

        cap_obj = {
            "city": city,
            "uf": uf,
            "regiao": regiao,
            "lat": coords["lat"],
            "lon": coords["lon"],
            "prestador": cat_info.get("prestador", "Concessionária Estadual"),
            "agencia": cat_info.get("agencia", "Agência Reguladora"),
            "distribuidora": cat_info.get("distribuidora", "Distribuidora de Energia"),
            "energia_b1_r_kwh": cat_info.get("energia_b1_r_kwh", 0.85),
            "tarifa_agua_base_r_m3": cat_info.get("agua_1o_escalao_r_m3", 5.50),
            "tarifa_combinada_r_m3": cat_info.get("tarifa_combinada_1o_esc_r_m3", 10.00),
            "esgoto_pct": cat_info.get("esgoto_pct", 80.0),
            "tbo_fixa_r": cat_info.get("tbo_fixa_r", 15.00),
            "faixas_completas": cat_info.get("faixas_completas", "Consulte a estrutura tarifária vigente."),
            "typologies": {}
        }

        for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
            sub_b = c_hist[c_hist["building_code"] == bcode].sort_values("lower_tank_vol_l")
            if sub_b.empty:
                continue

            # Ótimo Econômico (Max VPL 6%)
            idx_opt_econ = sub_b["vpl_6pct_brl"].idxmax()
            opt_econ_row = sub_b.loc[idx_opt_econ]

            # Ótimo TOPSIS
            idx_opt_topsis = sub_b["topsis_score"].idxmax()
            opt_topsis_row = sub_b.loc[idx_opt_topsis]

            # Ótimo Hidráulico (Max Savings %)
            idx_opt_hyd = sub_b["potential_water_savings_pct"].idxmax()
            opt_hyd_row = sub_b.loc[idx_opt_hyd]

            # Construção dos candidatos MCDM para avaliação VIKOR e SMAA-2
            mcdm_candidates = []
            for _, r in sub_b.iterrows():
                pot_pct = float(r["potential_water_savings_pct"])
                pluv_cons = float(r["annual_pluvial_consumed_m3"])
                if pot_pct > 0:
                    tot_demand = pluv_cons / (pot_pct / 100.0)
                else:
                    tot_demand = pluv_cons
                potable_consumed = max(0.0, tot_demand - pluv_cons)

                cand = TopsisCandidate(
                    lower_tank_vol=float(r["lower_tank_vol_l"]),
                    water_saved_m3_yr=pluv_cons,
                    vpl_brl=float(r["vpl_6pct_brl"]),
                    co2_saved_kg_lifetime=float(r["lifetime_net_co2_saved_kg"]),
                    capex_brl=float(r["capex_total_brl"]),
                    potential_savings_pct=pot_pct,
                    overflow_m3_yr=float(r["annual_overflow_spill_m3"]),
                    discounted_payback_years=float(r["payback_discounted_6pct"]),
                    irr_pct=float(r["tir_pct_yr"]),
                    potable_consumed_m3_yr=potable_consumed
                )
                mcdm_candidates.append(cand)

            # Executa VIKOR (consenso v=0.5)
            vikor_res = run_vikor(mcdm_candidates, v_param=0.5)
            best_vikor_idx = vikor_res.best_index
            opt_vikor_row = sub_b.iloc[best_vikor_idx]

            # Executa SMAA-VIKOR (1.000 amostras Monte Carlo)
            smaa_res = run_smaa_vikor(mcdm_candidates, num_samples=1000, random_seed=42)
            best_smaa_idx = smaa_res.most_acceptable_index
            opt_smaa_row = sub_b.iloc[best_smaa_idx]
            w_tech, w_econ, w_env = smaa_res.get_central_dimension_weights(best_smaa_idx)
            smaa_conf = float(smaa_res.confidence_factors[best_smaa_idx]) if len(smaa_res.confidence_factors) > best_smaa_idx else 0.0

            # Varredura de volumes
            vol_sweep = []
            for i, (_, r) in enumerate(sub_b.iterrows()):
                vol_sweep.append({
                    "vol_l": float(r["lower_tank_vol_l"]),
                    "vpl_6": float(r["vpl_6pct_brl"]),
                    "vpl_10": float(r["vpl_10pct_brl"]),
                    "vpl_14": float(r["vpl_14pct_brl"]),
                    "savings_pct": float(r["potential_water_savings_pct"]),
                    "consumed_m3": float(r["annual_pluvial_consumed_m3"]),
                    "spill_m3": float(r["annual_overflow_spill_m3"]),
                    "reliability": float(r["reliability_fully_met_pct"]),
                    "capex": float(r["capex_total_brl"]),
                    "opex": float(r["annual_opex_brl"]),
                    "water_savings_brl": float(r["annual_water_savings_brl"]),
                    "pb_simple": float(r["payback_simple_years"]),
                    "pb_desc_6": float(r["payback_discounted_6pct"]),
                    "tir_pct": float(r["tir_pct_yr"]),
                    "lcow": float(r["lcow_brl_m3"]),
                    "topsis": float(r["topsis_score"]),
                    "net_co2_kg": float(r["lifetime_net_co2_saved_kg"]),
                    "vikor_q": float(vikor_res.q_scores[i]),
                    "vikor_s": float(vikor_res.s_scores[i]),
                    "vikor_r": float(vikor_res.r_scores[i]),
                    "vikor_rank": int(vikor_res.ranks[i]),
                    "smaa_first_prob": float(smaa_res.first_rank_probs[i]),
                    "smaa_rank": int(smaa_res.ranks[i])
                })

            # Projeções climáticas para a capital e tipologia
            c_clim_sub = df_clim[(df_clim["city"] == city) & (df_clim["building_code"] == bcode)]
            clim_proj = {}
            for _, cr in c_clim_sub.iterrows():
                key = f"{cr['horizon_std']}_{cr['scenario_std']}" if cr['scenario_std'] != "Historical" else "Historical"
                clim_proj[key] = {
                    "horizon": cr['horizon_std'],
                    "scenario": cr['scenario_std'],
                    "savings_pct": float(cr["potential_water_savings_pct"]),
                    "consumed_m3": float(cr["annual_pluvial_consumed_m3"]),
                    "spill_m3": float(cr["annual_overflow_spill_m3"]),
                    "reliability": float(cr["reliability_fully_met_pct"]),
                    "vpl_6": float(cr["vpl_6pct_brl"])
                }

            cap_obj["typologies"][bcode] = {
                "specs": TYPOLOGY_SPECS[bcode],
                "opt_econ": {
                    "vol_l": float(opt_econ_row["lower_tank_vol_l"]),
                    "vpl_6": float(opt_econ_row["vpl_6pct_brl"]),
                    "vpl_10": float(opt_econ_row["vpl_10pct_brl"]),
                    "vpl_14": float(opt_econ_row["vpl_14pct_brl"]),
                    "savings_pct": float(opt_econ_row["potential_water_savings_pct"]),
                    "consumed_m3": float(opt_econ_row["annual_pluvial_consumed_m3"]),
                    "spill_m3": float(opt_econ_row["annual_overflow_spill_m3"]),
                    "reliability": float(opt_econ_row["reliability_fully_met_pct"]),
                    "capex": float(opt_econ_row["capex_total_brl"]),
                    "opex": float(opt_econ_row["annual_opex_brl"]),
                    "water_savings_brl": float(opt_econ_row["annual_water_savings_brl"]),
                    "pb_simple": float(opt_econ_row["payback_simple_years"]),
                    "pb_desc_6": float(opt_econ_row["payback_discounted_6pct"]),
                    "pb_desc_10": float(opt_econ_row["payback_discounted_10pct"]),
                    "tir_pct": float(opt_econ_row["tir_pct_yr"]),
                    "lcow": float(opt_econ_row["lcow_brl_m3"]),
                    "topsis": float(opt_econ_row["topsis_score"]),
                    "embodied_co2_kg": float(opt_econ_row["embodied_co2_kg"]),
                    "avoided_co2_annual_kg": float(opt_econ_row["avoided_co2_annual_kg"]),
                    "net_co2_kg": float(opt_econ_row["lifetime_net_co2_saved_kg"])
                },
                "opt_topsis": {
                    "vol_l": float(opt_topsis_row["lower_tank_vol_l"]),
                    "score": float(opt_topsis_row["topsis_score"]),
                    "vpl_6": float(opt_topsis_row["vpl_6pct_brl"]),
                    "savings_pct": float(opt_topsis_row["potential_water_savings_pct"])
                },
                "opt_hydraulic": {
                    "vol_l": float(opt_hyd_row["lower_tank_vol_l"]),
                    "savings_pct": float(opt_hyd_row["potential_water_savings_pct"]),
                    "consumed_m3": float(opt_hyd_row["annual_pluvial_consumed_m3"])
                },
                "opt_vikor": {
                    "vol_l": float(opt_vikor_row["lower_tank_vol_l"]),
                    "q_score": float(vikor_res.q_scores[best_vikor_idx]),
                    "s_score": float(vikor_res.s_scores[best_vikor_idx]),
                    "r_score": float(vikor_res.r_scores[best_vikor_idx]),
                    "vpl_6": float(opt_vikor_row["vpl_6pct_brl"]),
                    "savings_pct": float(opt_vikor_row["potential_water_savings_pct"]),
                    "capex": float(opt_vikor_row["capex_total_brl"]),
                    "pb_desc_6": float(opt_vikor_row["payback_discounted_6pct"]),
                    "tir_pct": float(opt_vikor_row["tir_pct_yr"]),
                    "net_co2_kg": float(opt_vikor_row["lifetime_net_co2_saved_kg"])
                },
                "opt_smaa": {
                    "vol_l": float(opt_smaa_row["lower_tank_vol_l"]),
                    "first_rank_prob": float(smaa_res.first_rank_probs[best_smaa_idx]),
                    "w_tech": float(w_tech),
                    "w_econ": float(w_econ),
                    "w_env": float(w_env),
                    "confidence": float(smaa_conf),
                    "vpl_6": float(opt_smaa_row["vpl_6pct_brl"]),
                    "savings_pct": float(opt_smaa_row["potential_water_savings_pct"]),
                    "capex": float(opt_smaa_row["capex_total_brl"]),
                    "pb_desc_6": float(opt_smaa_row["payback_discounted_6pct"]),
                    "tir_pct": float(opt_smaa_row["tir_pct_yr"]),
                    "net_co2_kg": float(opt_smaa_row["lifetime_net_co2_saved_kg"])
                },
                "volume_sweep": vol_sweep,
                "climate_projections": clim_proj
            }

        capitals_data.append(cap_obj)

    print(f"✓ Agregação concluída para {len(capitals_data)} capitais brasileiras.")
    return grouped_hist, capitals_data


# ====================================================================================================
# GERAÇÃO DE FIGURAS CIENTÍFICAS DE ALTA RESOLUÇÃO (MATPLOTLIB 300 DPI)
# ====================================================================================================

def generate_scientific_figures(grouped_hist, capitals_data):
    """Gera o conjunto completo de figuras científicas para o observatório cobrindo todas as 27 capitais com subplots por região."""
    print("\n🎨 Gerando conjunto de figuras científicas em alta resolução (300 DPI) para todas as 27 capitais...")
    setup_matplotlib_netuno_style(dark_mode=False)

    # 1. Curvas Canônicas de VPL vs Volume com Subplots por Macrorregião (Grid 2x3 para cada tipologia)
    for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        fig, axes = plt.subplots(2, 3, figsize=(18, 11))
        sub_b = grouped_hist[grouped_hist["building_code"] == bcode].copy()

        region_pos = [
            ("Norte", 0, 0),
            ("Nordeste", 0, 1),
            ("Centro-Oeste", 0, 2),
            ("Sudeste", 1, 0),
            ("Sul", 1, 1)
        ]

        for reg_name, r_idx, c_idx in region_pos:
            ax = axes[r_idx, c_idx]
            reg_cities = CAPITAIS_POR_REGIAO[reg_name]
            sub_reg = sub_b[sub_b["city"].isin(reg_cities)].copy()

            ax.axhline(0, color="#94a3b8", linestyle="--", linewidth=1.2, zorder=2, label="VPL = 0 (Breakeven)")

            for city in reg_cities:
                c_data = sub_reg[sub_reg["city"] == city].sort_values("lower_tank_vol_l")
                if not c_data.empty:
                    vols = c_data["lower_tank_vol_l"].values
                    vpls = c_data["vpl_6pct_brl"].values
                    style = CITY_STYLE_MAP.get(city, {"color": REGION_COLORS[reg_name], "marker": "o", "ls": "-"})
                    uf_str = CAPITAIS_UF.get(city, "")
                    lbl = f"{city} ({uf_str})"

                    ax.plot(vols, vpls, color=style["color"], linestyle=style["ls"], linewidth=2.0,
                            marker=style["marker"], markersize=5.0, alpha=0.9, label=lbl, zorder=3)

                    best_idx = np.argmax(vpls)
                    ax.plot(vols[best_idx], vpls[best_idx], marker="*", markersize=12,
                            color=style["color"], markeredgecolor="#0f172a", markeredgewidth=1.0, zorder=5)

            if not sub_reg.empty:
                reg_mean = sub_reg.groupby("lower_tank_vol_l")["vpl_6pct_brl"].mean().reset_index()
                ax.plot(reg_mean["lower_tank_vol_l"], reg_mean["vpl_6pct_brl"], color="#0f172a",
                        linewidth=2.4, linestyle=":", marker="X", markersize=5.5, label="Média Regional", zorder=4)

            ax.set_title(f"Região {reg_name} ({len(reg_cities)} Capitais)", fontsize=11, fontweight="bold", pad=8, color=REGION_COLORS[reg_name])
            ax.set_xlabel("Volume da Cisterna (Litros)", fontsize=9)
            ax.set_ylabel("VPL Líquido (R$)", fontsize=9)
            ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")
            ax.legend(loc="best", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=7.8, ncol=2 if len(reg_cities) > 4 else 1)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}".replace(",", ".")))
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"R$ {y:,.0f}".replace(",", ".")))

        # Subplot (1, 2): Síntese Macrorregional & Média Brasil
        ax_syn = axes[1, 2]
        ax_syn.axhline(0, color="#94a3b8", linestyle="--", linewidth=1.2, zorder=2, label="VPL = 0 (Breakeven)")

        for reg_name in REGION_ORDER:
            sub_reg = sub_b[sub_b["regiao"] == reg_name]
            if not sub_reg.empty:
                reg_mean = sub_reg.groupby("lower_tank_vol_l")["vpl_6pct_brl"].mean().reset_index()
                ax_syn.plot(reg_mean["lower_tank_vol_l"], reg_mean["vpl_6pct_brl"], color=REGION_COLORS[reg_name],
                            linewidth=2.2, marker="o", markersize=4.8, label=f"Média {reg_name}", zorder=3)

        nat_mean = sub_b.groupby("lower_tank_vol_l")["vpl_6pct_brl"].mean().reset_index()
        ax_syn.plot(nat_mean["lower_tank_vol_l"], nat_mean["vpl_6pct_brl"], color="#0f172a",
                    linewidth=2.8, linestyle="-.", marker="X", markersize=6.5, label="Média Brasil (27 Capitais)", zorder=4)

        ax_syn.set_title("Síntese Macrorregional & Média Brasil", fontsize=11, fontweight="bold", pad=8, color="#0f172a")
        ax_syn.set_xlabel("Volume da Cisterna (Litros)", fontsize=9)
        ax_syn.set_ylabel("VPL Líquido (R$)", fontsize=9)
        ax_syn.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1")
        ax_syn.legend(loc="best", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)
        ax_syn.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}".replace(",", ".")))
        ax_syn.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"R$ {y:,.0f}".replace(",", ".")))

        t_name = TYPOLOGY_NAMES.get(bcode, bcode)
        fig.suptitle(f"Curvas Canônicas de VPL Líquido vs. Volume nas 27 Capitais Brasileiras por Macrorregião — {t_name}",
                     fontsize=13, fontweight="bold", y=0.995)
        plt.tight_layout()
        out_png = os.path.join(FIGURAS_DIR, f"grafico_vpl_vs_volume_capitais_{bcode}.png")
        plt.savefig(out_png)
        plt.close()

    print(" ✓ Curvas Canônicas VPL vs Volume geradas com subplots regionais para as 5 tipologias.")

    # 2. Rankings Nacionais de VPL Ótimo (Todas as 5 Tipologias)
    for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        fig, ax = plt.subplots(figsize=(12.5, 9.5))
        ranks = []
        for c in capitals_data:
            if bcode in c["typologies"]:
                ranks.append({
                    "city": c["city"],
                    "uf": c["uf"],
                    "regiao": c["regiao"],
                    "vpl_6": c["typologies"][bcode]["opt_econ"]["vpl_6"],
                    "vol_l": c["typologies"][bcode]["opt_econ"]["vol_l"],
                    "pot_pct": c["typologies"][bcode]["opt_econ"]["savings_pct"]
                })
        df_rank = pd.DataFrame(ranks).sort_values("vpl_6", ascending=True)

        y_pos = np.arange(len(df_rank))
        colors = [REGION_COLORS.get(r, "#64748b") for r in df_rank["regiao"]]
        bars = ax.barh(y_pos, df_rank["vpl_6"], color=colors, height=0.68, edgecolor="#334155", linewidth=0.6, zorder=3)

        ax.axvline(0, color="#dc2626", linestyle="--", linewidth=1.2, zorder=4, label="VPL = 0 (Limiar de Viabilidade)")
        mean_vpl = df_rank["vpl_6"].mean()
        ax.axvline(mean_vpl, color="#0f172a", linestyle="-.", linewidth=1.3, zorder=4, label=f"Média Nacional: R$ {mean_vpl:,.2f}".replace(",", "."))

        ax.set_yticks(y_pos)
        labels = [f"{row['city']} ({row['uf']}) — {row['vol_l']:,.0f} L ({row['pot_pct']:.1f}%)".replace(",", ".") for _, row in df_rank.iterrows()]
        ax.set_yticklabels(labels, fontsize=8.8)

        min_v = df_rank["vpl_6"].min()
        max_v = df_rank["vpl_6"].max()
        span = max(1.0, max_v - min_v)
        ax.set_xlim(min_v - span * 0.16, max_v + span * 0.16)

        for bar, (_, row) in zip(bars, df_rank.iterrows()):
            val = row["vpl_6"]
            offset = span * 0.012 if val >= 0 else -span * 0.012
            ha = "left" if val >= 0 else "right"
            color_txt = "#047857" if val >= 0 else "#b91c1c"
            ax.text(
                val + offset, bar.get_y() + bar.get_height() / 2,
                f"R$ {val:,.2f}".replace(",", "."),
                ha=ha, va="center", fontsize=8.2, fontweight="bold", color=color_txt, zorder=5
            )

        t_name = TYPOLOGY_NAMES.get(bcode, bcode)
        ax.set_title(f"Ranking Nacional do VPL Ótimo nas 27 Capitais Brasileiras — ({t_name})", pad=15, fontsize=12)
        ax.set_xlabel("VPL Líquido Ótimo (R$)")
        ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1", axis="x")

        legend_elements = [plt.Rectangle((0, 0), 1, 1, color=REGION_COLORS[r], label=f"Região {r}") for r in REGION_ORDER]
        legend_elements.append(plt.Line2D([0], [0], color="#dc2626", linestyle="--", label="VPL = 0"))
        legend_elements.append(plt.Line2D([0], [0], color="#0f172a", linestyle="-.", label="Média Nacional"))
        ax.legend(handles=legend_elements, loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"R$ {x:,.0f}".replace(",", ".")))

        plt.tight_layout()
        out_png = os.path.join(FIGURAS_DIR, f"ranking_nacional_vpl_otimo_{bcode}.png")
        plt.savefig(out_png)
        plt.close()

    print(" ✓ Rankings Nacionais de VPL gerados para as 5 tipologias.")

    # 3. Matriz Multi-Tipologia (Grid 5x1)
    fig, axes = plt.subplots(1, 5, figsize=(20, 9.5), sharey=True)
    typologies = ["UTI", "UTG", "MSG", "MFH", "MFL"]

    cap_means = {}
    for c in capitals_data:
        vpls = [c["typologies"][t]["opt_econ"]["vpl_6"] for t in typologies if t in c["typologies"]]
        cap_means[c["city"]] = np.mean(vpls) if vpls else 0
    cap_order = sorted(cap_means.keys(), key=lambda k: cap_means[k])

    for idx, (ax, bcode) in enumerate(zip(axes, typologies)):
        rows = []
        for city in cap_order:
            cap_obj = next((c for c in capitals_data if c["city"] == city), None)
            if cap_obj and bcode in cap_obj["typologies"]:
                rows.append({
                    "city": city,
                    "uf": cap_obj["uf"],
                    "regiao": cap_obj["regiao"],
                    "vpl_6": cap_obj["typologies"][bcode]["opt_econ"]["vpl_6"]
                })
        sub_df = pd.DataFrame(rows)
        y_pos = np.arange(len(sub_df))
        colors = [REGION_COLORS.get(r, "#64748b") for r in sub_df["regiao"]]

        ax.barh(y_pos, sub_df["vpl_6"], color=colors, height=0.65, edgecolor="#334155", linewidth=0.5, zorder=3)
        ax.axvline(0, color="#dc2626", linestyle="--", linewidth=1.0, zorder=4)

        mean_v = sub_df["vpl_6"].mean()
        ax.axvline(mean_v, color="#0f172a", linestyle="-.", linewidth=1.1, zorder=4)

        ax.set_title(f"{TYPOLOGY_SHORT[bcode]}\nMédia: R$ {mean_v:,.0f}".replace(",", "."), fontsize=9.5, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1", axis="x")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"R$ {x/1e3:.0f}k" if abs(x) >= 1000 else f"R$ {x:.0f}"))

        if idx == 0:
            labels = [f"{row['city']} ({row['uf']})" for _, row in sub_df.iterrows()]
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=8.5)
        else:
            ax.tick_params(left=False)

    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=REGION_COLORS[r], label=f"Região {r}") for r in REGION_ORDER]
    legend_elements.append(plt.Line2D([0], [0], color="#dc2626", linestyle="--", label="VPL = 0"))
    legend_elements.append(plt.Line2D([0], [0], color="#0f172a", linestyle="-.", label="Média Nacional"))
    fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 0.99), ncol=7, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

    fig.suptitle("Comparativo Nacional do VPL Ótimo nas 5 Tipologias Residenciais — 27 Capitais Brasileiras", fontsize=12.5, fontweight="bold", y=1.03)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "matriz_multitipologia_vpl_otimo_27_capitais.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Matriz Multi-Tipologia VPL gerada.")

    # 3.1 Matriz Multi-Tipologia CO2 Líquido Evitado (Grid 5x1)
    fig, axes = plt.subplots(1, 5, figsize=(20, 9.5), sharey=True)
    typologies = ["UTI", "UTG", "MSG", "MFH", "MFL"]

    cap_co2_means = {}
    for c in capitals_data:
        co2_vals = [c["typologies"][t]["opt_econ"]["net_co2_kg"] for t in typologies if t in c["typologies"]]
        cap_co2_means[c["city"]] = np.mean(co2_vals) if co2_vals else 0
    cap_co2_order = sorted(cap_co2_means.keys(), key=lambda k: cap_co2_means[k])

    for idx, (ax, bcode) in enumerate(zip(axes, typologies)):
        rows = []
        for city in cap_co2_order:
            cap_obj = next((c for c in capitals_data if c["city"] == city), None)
            if cap_obj and bcode in cap_obj["typologies"]:
                rows.append({
                    "city": city,
                    "uf": cap_obj["uf"],
                    "regiao": cap_obj["regiao"],
                    "co2": cap_obj["typologies"][bcode]["opt_econ"]["net_co2_kg"]
                })
        sub_df = pd.DataFrame(rows)
        y_pos = np.arange(len(sub_df))
        colors = [REGION_COLORS.get(r, "#64748b") for r in sub_df["regiao"]]

        ax.barh(y_pos, sub_df["co2"], color=colors, height=0.65, edgecolor="#334155", linewidth=0.5, zorder=3)
        ax.axvline(0, color="#dc2626", linestyle="--", linewidth=1.0, zorder=4)

        mean_v = sub_df["co2"].mean()
        ax.axvline(mean_v, color="#0f172a", linestyle="-.", linewidth=1.1, zorder=4)

        ax.set_title(f"{TYPOLOGY_SHORT[bcode]}\nMédia: {mean_v:,.0f} kg CO₂".replace(",", "."), fontsize=9.5, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1", axis="x")
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x/1e3:.1f}k kg" if abs(x) >= 1000 else f"{x:.0f} kg"))

        if idx == 0:
            labels = [f"{row['city']} ({row['uf']})" for _, row in sub_df.iterrows()]
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=8.5)
        else:
            ax.tick_params(left=False)

    legend_elements = [plt.Rectangle((0, 0), 1, 1, color=REGION_COLORS[r], label=f"Região {r}") for r in REGION_ORDER]
    legend_elements.append(plt.Line2D([0], [0], color="#dc2626", linestyle="--", label="CO₂ = 0 kg"))
    legend_elements.append(plt.Line2D([0], [0], color="#0f172a", linestyle="-.", label="Média Nacional"))
    fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 0.99), ncol=7, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)

    fig.suptitle("Balanço Ambiental: CO₂ Líquido Evitado na Vida Útil (20 Anos) nas 5 Tipologias — 27 Capitais Brasileiras", fontsize=12.5, fontweight="bold", y=1.03)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "matriz_multitipologia_co2_otimo_27_capitais.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Matriz Multi-Tipologia CO₂ gerada.")

    # 3.2 Rankings Nacionais de CO2 (Todas as 5 Tipologias)
    for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        rows = []
        for c in capitals_data:
            if bcode in c["typologies"]:
                opt = c["typologies"][bcode]["opt_econ"]
                rows.append({
                    "city": c["city"],
                    "uf": c["uf"],
                    "regiao": c["regiao"],
                    "co2": opt["net_co2_kg"],
                    "vol_l": opt["vol_l"],
                    "savings_pct": opt["savings_pct"]
                })
        df_rank = pd.DataFrame(rows).sort_values("co2", ascending=True)

        fig, ax = plt.subplots(figsize=(12.5, 9.5))
        y_pos = np.arange(len(df_rank))
        colors = [REGION_COLORS.get(r, "#64748b") for r in df_rank["regiao"]]

        bars = ax.barh(y_pos, df_rank["co2"], color=colors, height=0.68, edgecolor="#1e293b", linewidth=0.6, zorder=3)
        ax.axvline(0, color="#dc2626", linestyle="--", linewidth=1.2, label="CO₂ = 0", zorder=4)

        mean_co2 = df_rank["co2"].mean()
        ax.axvline(mean_co2, color="#0f172a", linestyle="-.", linewidth=1.3, label="Média Nacional", zorder=4)

        for bar, (_, row) in zip(bars, df_rank.iterrows()):
            v = row["co2"]
            x_pos = v + (15 if v >= 0 else -15)
            ha = "left" if v >= 0 else "right"
            val_str = f"{v:,.0f} kg CO₂".replace(",", ".")
            ax.text(x_pos, bar.get_y() + bar.get_height()/2, val_str,
                    va="center", ha=ha, fontsize=8.5, fontweight="bold",
                    color="#065f46" if v >= 0 else "#991b1b")

        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"{r['city']} ({r['uf']}) — {r['vol_l']:,.0f} L ({r['savings_pct']:.1f}%)".replace(",", ".") for _, r in df_rank.iterrows()], fontsize=8.8)
        t_name = TYPOLOGY_NAMES.get(bcode, bcode)
        ax.set_title(f"Ranking Nacional de Descarbonização (CO₂ Líquido Evitado) — ({t_name})", pad=15, fontsize=12)
        ax.set_xlabel("CO₂ Líquido Evitado no Ciclo de Vida de 20 Anos (kg CO₂)")
        ax.grid(True, linestyle=":", alpha=0.6, color="#cbd5e1", axis="x")

        legend_elements = [plt.Rectangle((0, 0), 1, 1, color=REGION_COLORS[r], label=f"Região {r}") for r in REGION_ORDER]
        legend_elements.append(plt.Line2D([0], [0], color="#dc2626", linestyle="--", label="CO₂ = 0"))
        legend_elements.append(plt.Line2D([0], [0], color="#0f172a", linestyle="-.", label="Média Nacional"))
        ax.legend(handles=legend_elements, loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.5)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f} kg".replace(",", ".")))

        plt.tight_layout()
        out_png = os.path.join(FIGURAS_DIR, f"ranking_nacional_co2_otimo_{bcode}.png")
        plt.savefig(out_png)
        plt.close()
    print(" ✓ Rankings Nacionais de CO₂ gerados para as 5 tipologias.")

    # 4. Gráfico Radar Multi-Critério TOPSIS com Subplots por Macrorregião (Grid 2x3 Polar)
    fig, axes = plt.subplots(2, 3, figsize=(19, 12.5), subplot_kw=dict(polar=True))
    categories = ['Economia Hídrica (%)', 'VPL Financeiro (R$)', 'Retorno / Payback', 'CO₂ Evitado Líquido (kg)', 'Confiabilidade Pluvial (%)', 'Tarifa Água (R$/m³)']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    bcode = "UTI"
    all_pot = [c["typologies"][bcode]["opt_econ"]["savings_pct"] for c in capitals_data if bcode in c["typologies"]]
    all_vpl = [c["typologies"][bcode]["opt_econ"]["vpl_6"] for c in capitals_data if bcode in c["typologies"]]
    all_pb = [c["typologies"][bcode]["opt_econ"]["pb_desc_6"] for c in capitals_data if bcode in c["typologies"]]
    all_co2 = [c["typologies"][bcode]["opt_econ"]["net_co2_kg"] for c in capitals_data if bcode in c["typologies"]]
    all_rel = [c["typologies"][bcode]["opt_econ"]["reliability"] for c in capitals_data if bcode in c["typologies"]]
    all_tar = [c["tarifa_agua_base_r_m3"] for c in capitals_data if bcode in c["typologies"]]

    def norm_val(v, min_v, max_v):
        if max_v == min_v: return 50.0
        return max(5.0, min(100.0, ((v - min_v) / (max_v - min_v)) * 95.0 + 5.0))

    region_pos = [
        ("Norte", 0, 0),
        ("Nordeste", 0, 1),
        ("Centro-Oeste", 0, 2),
        ("Sudeste", 1, 0),
        ("Sul", 1, 1)
    ]

    for reg_name, r_idx, c_idx in region_pos:
        ax = axes[r_idx, c_idx]
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]

        for city in reg_cities:
            c_obj = next((c for c in capitals_data if c["city"] == city), None)
            if c_obj and bcode in c_obj["typologies"]:
                opt = c_obj["typologies"][bcode]["opt_econ"]
                v_pot = norm_val(opt["savings_pct"], min(all_pot), max(all_pot))
                v_vpl = norm_val(opt["vpl_6"], min(all_vpl), max(all_vpl))
                v_pb = norm_val(-min(opt["pb_desc_6"], 25.0), -max(all_pb), -min(all_pb))
                v_co2 = norm_val(opt["net_co2_kg"], min(all_co2), max(all_co2))
                v_rel = norm_val(opt["reliability"], min(all_rel), max(all_rel))
                v_tar = norm_val(c_obj["tarifa_agua_base_r_m3"], min(all_tar), max(all_tar))

                vals = [v_pot, v_vpl, v_pb, v_co2, v_rel, v_tar]
                vals += vals[:1]

                style = CITY_STYLE_MAP.get(city, {"color": REGION_COLORS[reg_name], "marker": "o", "ls": "-"})
                uf_str = CAPITAIS_UF.get(city, "")
                ax.plot(angles, vals, linewidth=2.0, linestyle=style["ls"], marker=style["marker"], markersize=4.5,
                        label=f"{city} ({uf_str})", color=style["color"])
                ax.fill(angles, vals, color=style["color"], alpha=0.10)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=7.8, fontweight="bold")
        ax.set_rlabel_position(0)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(["25%", "50%", "75%", "100%"], color="#64748b", size=7.0)
        ax.set_ylim(0, 100)
        ax.set_title(f"Região {reg_name} ({len(reg_cities)} Capitais)", size=11, fontweight="bold", y=1.12, color=REGION_COLORS[reg_name])
        ax.legend(loc='upper right', bbox_to_anchor=(1.28, 1.15), fontsize=7.5, ncol=1)

    # Subplot (1, 2): Panorama Comparativo Macrorregional
    ax_syn = axes[1, 2]
    for reg_name in REGION_ORDER:
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]
        reg_objs = [c for c in capitals_data if c["city"] in reg_cities and bcode in c["typologies"]]
        if reg_objs:
            m_pot = np.mean([c["typologies"][bcode]["opt_econ"]["savings_pct"] for c in reg_objs])
            m_vpl = np.mean([c["typologies"][bcode]["opt_econ"]["vpl_6"] for c in reg_objs])
            m_pb = np.mean([min(c["typologies"][bcode]["opt_econ"]["pb_desc_6"], 25.0) for c in reg_objs])
            m_co2 = np.mean([c["typologies"][bcode]["opt_econ"]["net_co2_kg"] for c in reg_objs])
            m_rel = np.mean([c["typologies"][bcode]["opt_econ"]["reliability"] for c in reg_objs])
            m_tar = np.mean([c["tarifa_agua_base_r_m3"] for c in reg_objs])

            v_pot = norm_val(m_pot, min(all_pot), max(all_pot))
            v_vpl = norm_val(m_vpl, min(all_vpl), max(all_vpl))
            v_pb = norm_val(-m_pb, -max(all_pb), -min(all_pb))
            v_co2 = norm_val(m_co2, min(all_co2), max(all_co2))
            v_rel = norm_val(m_rel, min(all_rel), max(all_rel))
            v_tar = norm_val(m_tar, min(all_tar), max(all_tar))

            vals = [v_pot, v_vpl, v_pb, v_co2, v_rel, v_tar]
            vals += vals[:1]
            ax_syn.plot(angles, vals, linewidth=2.2, linestyle='solid', marker='o', markersize=4.5,
                        label=f"Média {reg_name}", color=REGION_COLORS[reg_name])
            ax_syn.fill(angles, vals, color=REGION_COLORS[reg_name], alpha=0.10)

    # Média Brasil
    m_pot_br = np.mean(all_pot)
    m_vpl_br = np.mean(all_vpl)
    m_pb_br = np.mean([min(x, 25.0) for x in all_pb])
    m_co2_br = np.mean(all_co2)
    m_rel_br = np.mean(all_rel)
    m_tar_br = np.mean(all_tar)
    vals_br = [
        norm_val(m_pot_br, min(all_pot), max(all_pot)),
        norm_val(m_vpl_br, min(all_vpl), max(all_vpl)),
        norm_val(-m_pb_br, -max(all_pb), -min(all_pb)),
        norm_val(m_co2_br, min(all_co2), max(all_co2)),
        norm_val(m_rel_br, min(all_rel), max(all_rel)),
        norm_val(m_tar_br, min(all_tar), max(all_tar))
    ]
    vals_br += vals_br[:1]
    ax_syn.plot(angles, vals_br, linewidth=2.8, linestyle='-.', marker='X', markersize=6.0,
                label="Média Brasil (27 Capitais)", color="#0f172a")

    ax_syn.set_theta_offset(np.pi / 2)
    ax_syn.set_theta_direction(-1)
    ax_syn.set_xticks(angles[:-1])
    ax_syn.set_xticklabels(categories, fontsize=7.8, fontweight="bold")
    ax_syn.set_rlabel_position(0)
    ax_syn.set_yticks([25, 50, 75, 100])
    ax_syn.set_yticklabels(["25%", "50%", "75%", "100%"], color="#64748b", size=7.0)
    ax_syn.set_ylim(0, 100)
    ax_syn.set_title("Síntese Macrorregional & Média Brasil", size=11, fontweight="bold", y=1.12, color="#0f172a")
    ax_syn.legend(loc='upper right', bbox_to_anchor=(1.28, 1.15), fontsize=8.0)

    fig.suptitle("Avaliação Multi-Critério TOPSIS Normalizada — 27 Capitais Brasileiras por Macrorregião (Tipologia UTI)",
                 size=14, fontweight="bold", y=0.995)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "figura_radar_multicriterio_capitais.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Radar Multi-Critério por Região gerado.")

    # 4.1 Curvas de CO2 vs Volume de Cisterna com Subplots por Macrorregião (Grid 2x3)
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    bcode = "UTI"

    region_pos = [
        ("Norte", 0, 0),
        ("Nordeste", 0, 1),
        ("Centro-Oeste", 0, 2),
        ("Sudeste", 1, 0),
        ("Sul", 1, 1)
    ]

    for reg_name, r_idx, c_idx in region_pos:
        ax = axes[r_idx, c_idx]
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]
        ax.axhline(0, color="#dc2626", linestyle="--", linewidth=1.1, label="CO₂ = 0")

        for city in reg_cities:
            c_obj = next((c for c in capitals_data if c["city"] == city), None)
            if c_obj and bcode in c_obj["typologies"]:
                vols_curve = c_obj["typologies"][bcode]["volume_sweep"]
                vx = [pt["vol_l"] for pt in vols_curve]
                vy_co2 = [pt["net_co2_kg"] for pt in vols_curve]
                style = CITY_STYLE_MAP.get(city, {"color": REGION_COLORS[reg_name], "marker": "o", "ls": "-"})
                uf_str = CAPITAIS_UF.get(city, "")

                ax.plot(vx, vy_co2, marker=style["marker"], linestyle=style["ls"], linewidth=1.9,
                        label=f"{city} ({uf_str})", color=style["color"], markersize=4.8)

                best_co2_idx = int(np.argmax(vy_co2))
                ax.plot(vx[best_co2_idx], vy_co2[best_co2_idx], marker="*", markersize=11,
                        color=style["color"], markeredgecolor="#0f172a", markeredgewidth=0.8, zorder=5)

        ax.set_title(f"Região {reg_name} ({len(reg_cities)} Capitais)", fontweight="bold", fontsize=11, color=REGION_COLORS[reg_name])
        ax.set_xlabel("Capacidade da Cisterna (L)", fontsize=9)
        ax.set_ylabel("CO₂ Líquido Evitado (kg CO₂)", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="best", fontsize=7.8, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", ncol=2 if len(reg_cities) > 4 else 1)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x/1e3:.0f}k L" if x >= 1000 else f"{x:.0f} L"))

    # Subplot (1, 2): Síntese Regional & Brasil
    ax_syn = axes[1, 2]
    ax_syn.axhline(0, color="#dc2626", linestyle="--", linewidth=1.1, label="CO₂ = 0")

    for reg_name in REGION_ORDER:
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]
        reg_curves = []
        for city in reg_cities:
            c_obj = next((c for c in capitals_data if c["city"] == city), None)
            if c_obj and bcode in c_obj["typologies"]:
                vols_curve = c_obj["typologies"][bcode]["volume_sweep"]
                reg_curves.append([pt["net_co2_kg"] for pt in vols_curve])
        if reg_curves:
            mean_curve = np.mean(reg_curves, axis=0)
            sample_vx = [pt["vol_l"] for pt in capitals_data[0]["typologies"][bcode]["volume_sweep"]]
            ax_syn.plot(sample_vx, mean_curve, color=REGION_COLORS[reg_name], linewidth=2.2, marker="o", markersize=4.8, label=f"Média {reg_name}")

    all_co2_curves = []
    for c in capitals_data:
        if bcode in c["typologies"]:
            all_co2_curves.append([pt["net_co2_kg"] for pt in c["typologies"][bcode]["volume_sweep"]])
    if all_co2_curves:
        br_mean_co2 = np.mean(all_co2_curves, axis=0)
        sample_vx = [pt["vol_l"] for pt in capitals_data[0]["typologies"][bcode]["volume_sweep"]]
        ax_syn.plot(sample_vx, br_mean_co2, color="#0f172a", linewidth=2.8, linestyle="-.", marker="X", markersize=6.0, label="Média Brasil")

    ax_syn.set_title("Síntese Macrorregional & Média Brasil", fontweight="bold", fontsize=11, color="#0f172a")
    ax_syn.set_xlabel("Capacidade da Cisterna (L)", fontsize=9)
    ax_syn.set_ylabel("CO₂ Líquido Evitado (kg CO₂)", fontsize=9)
    ax_syn.grid(True, linestyle=":", alpha=0.6)
    ax_syn.legend(loc="best", fontsize=8.0, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax_syn.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x/1e3:.0f}k L" if x >= 1000 else f"{x:.0f} L"))

    fig.suptitle("Dinâmica de Carbono: Saldo Líquido de CO₂ Evitado vs. Volume da Cisterna — 27 Capitais por Macrorregião (UTI)",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "figura_curvas_co2_vs_volume_5_tipologias.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Curvas de CO₂ vs Volume por Região geradas.")

    # 5. Trajetórias Climáticas CMIP6 com Subplots por Macrorregião (Grid 2x5)
    fig, axes = plt.subplots(2, 5, figsize=(23, 9.5), sharey=True)
    horizons = ["Histórico", "Near (2030)", "Middle (2060)", "Far (2085)"]
    x_pos = np.arange(len(horizons))
    bcode = "UTI"

    for col_idx, reg_name in enumerate(REGION_ORDER):
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]

        ax_ssp2 = axes[0, col_idx]
        ax_ssp5 = axes[1, col_idx]

        ssp2_all = []
        ssp5_all = []

        for city in reg_cities:
            c_obj = next((c for c in capitals_data if c["city"] == city), None)
            if c_obj and bcode in c_obj["typologies"]:
                clim = c_obj["typologies"][bcode]["climate_projections"]
                style = CITY_STYLE_MAP.get(city, {"color": REGION_COLORS[reg_name], "marker": "o", "ls": "-"})
                uf_str = CAPITAIS_UF.get(city, "")

                v_ssp2 = [
                    clim.get("Historical", {}).get("savings_pct", 15),
                    clim.get("Near_SSP245", {}).get("savings_pct", 15),
                    clim.get("Middle_SSP245", {}).get("savings_pct", 15),
                    clim.get("Far_SSP245", {}).get("savings_pct", 15)
                ]
                ssp2_all.append(v_ssp2)
                ax_ssp2.plot(x_pos, v_ssp2, marker=style["marker"], linestyle=style["ls"], linewidth=1.9,
                             label=f"{city} ({uf_str})", color=style["color"], markersize=4.8)

                v_ssp5 = [
                    clim.get("Historical", {}).get("savings_pct", 15),
                    clim.get("Near_SSP585", {}).get("savings_pct", 15),
                    clim.get("Middle_SSP585", {}).get("savings_pct", 15),
                    clim.get("Far_SSP585", {}).get("savings_pct", 15)
                ]
                ssp5_all.append(v_ssp5)
                ax_ssp5.plot(x_pos, v_ssp5, marker=style["marker"], linestyle=style["ls"], linewidth=1.9,
                             label=f"{city} ({uf_str})", color=style["color"], markersize=4.8)

        if ssp2_all:
            ax_ssp2.plot(x_pos, np.mean(ssp2_all, axis=0), color="#0f172a", linewidth=2.4, linestyle=":", marker="X", label="Média Regional")
        if ssp5_all:
            ax_ssp5.plot(x_pos, np.mean(ssp5_all, axis=0), color="#0f172a", linewidth=2.4, linestyle=":", marker="X", label="Média Regional")

        ax_ssp2.set_title(f"SSP2-4.5 — {reg_name} ({len(reg_cities)} cap.)", fontsize=10.5, fontweight="bold", color=REGION_COLORS[reg_name])
        ax_ssp2.set_xticks(x_pos)
        ax_ssp2.set_xticklabels(horizons, fontsize=8, rotation=20)
        ax_ssp2.grid(True, linestyle=":", alpha=0.6)
        ax_ssp2.legend(loc="best", fontsize=7.2, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", ncol=2 if len(reg_cities) > 4 else 1)
        if col_idx == 0:
            ax_ssp2.set_ylabel("Economia Pluvial (%) [SSP2-4.5]", fontsize=9, fontweight="bold")

        ax_ssp5.set_title(f"SSP5-8.5 — {reg_name} ({len(reg_cities)} cap.)", fontsize=10.5, fontweight="bold", color=REGION_COLORS[reg_name])
        ax_ssp5.set_xticks(x_pos)
        ax_ssp5.set_xticklabels(horizons, fontsize=8, rotation=20)
        ax_ssp5.grid(True, linestyle=":", alpha=0.6)
        ax_ssp5.legend(loc="best", fontsize=7.2, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", ncol=2 if len(reg_cities) > 4 else 1)
        if col_idx == 0:
            ax_ssp5.set_ylabel("Economia Pluvial (%) [SSP5-8.5]", fontsize=9, fontweight="bold")

    fig.suptitle("Projeções de Desempenho Pluvial das 27 Capitais Brasileiras sob Cenários Climáticos CMIP6 (SSP2-4.5 vs. SSP5-8.5)",
                 fontsize=13.5, fontweight="bold", y=0.995)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "figura_trajetorias_climaticas_capitais_cmip6.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Trajetórias Climáticas CMIP6 por Região geradas.")

    # 6. Análise de Sensibilidade TMA com Subplots por Macrorregião (Grid 2x3)
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    bcode = "UTI"

    region_pos = [
        ("Norte", 0, 0),
        ("Nordeste", 0, 1),
        ("Centro-Oeste", 0, 2),
        ("Sudeste", 1, 0),
        ("Sul", 1, 1)
    ]

    for reg_name, r_idx, c_idx in region_pos:
        ax = axes[r_idx, c_idx]
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]

        rows = []
        for city in reg_cities:
            c_obj = next((c for c in capitals_data if c["city"] == city), None)
            if c_obj and bcode in c_obj["typologies"]:
                opt = c_obj["typologies"][bcode]["opt_econ"]
                rows.append({
                    "city": f"{city} ({c_obj['uf']})",
                    "TMA_6": opt["vpl_6"],
                    "TMA_10": opt["vpl_10"],
                    "TMA_14": opt["vpl_14"]
                })
        df_sens_reg = pd.DataFrame(rows).sort_values("TMA_6", ascending=False)

        x = np.arange(len(df_sens_reg))
        width = 0.26
        ax.bar(x - width, df_sens_reg["TMA_6"], width, label="TMA 6% a.a. (Base)", color="#059669", edgecolor="#334155", linewidth=0.5)
        ax.bar(x, df_sens_reg["TMA_10"], width, label="TMA 10% a.a. (Interm.)", color="#d97706", edgecolor="#334155", linewidth=0.5)
        ax.bar(x + width, df_sens_reg["TMA_14"], width, label="TMA 14% a.a. (Severo)", color="#dc2626", edgecolor="#334155", linewidth=0.5)

        ax.axhline(0, color="#0f172a", linestyle="--", linewidth=1.1)
        ax.set_xticks(x)
        ax.set_xticklabels(df_sens_reg["city"], rotation=35, ha="right", fontsize=8.2, fontweight="bold")
        ax.set_title(f"Região {reg_name} ({len(reg_cities)} Capitais)", fontsize=11, fontweight="bold", color=REGION_COLORS[reg_name])
        ax.set_ylabel("VPL Ótimo (R$)", fontsize=9)
        ax.grid(True, linestyle=":", alpha=0.6, axis="y")
        ax.legend(loc="upper right", fontsize=7.8)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"R$ {y:,.0f}".replace(",", ".")))

    # Subplot (1, 2): Síntese Regional & Brasil
    ax_syn = axes[1, 2]
    syn_rows = []
    for reg_name in REGION_ORDER:
        reg_cities = CAPITAIS_POR_REGIAO[reg_name]
        reg_objs = [c for c in capitals_data if c["city"] in reg_cities and bcode in c["typologies"]]
        if reg_objs:
            syn_rows.append({
                "label": f"Média {reg_name}",
                "TMA_6": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_6"] for c in reg_objs]),
                "TMA_10": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_10"] for c in reg_objs]),
                "TMA_14": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_14"] for c in reg_objs])
            })
    all_uti_objs = [c for c in capitals_data if bcode in c["typologies"]]
    syn_rows.append({
        "label": "Média Brasil",
        "TMA_6": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_6"] for c in all_uti_objs]),
        "TMA_10": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_10"] for c in all_uti_objs]),
        "TMA_14": np.mean([c["typologies"][bcode]["opt_econ"]["vpl_14"] for c in all_uti_objs])
    })
    df_syn = pd.DataFrame(syn_rows)

    x_syn = np.arange(len(df_syn))
    width = 0.26
    ax_syn.bar(x_syn - width, df_syn["TMA_6"], width, label="TMA 6% a.a. (Base)", color="#059669", edgecolor="#334155", linewidth=0.5)
    ax_syn.bar(x_syn, df_syn["TMA_10"], width, label="TMA 10% a.a. (Interm.)", color="#d97706", edgecolor="#334155", linewidth=0.5)
    ax_syn.bar(x_syn + width, df_syn["TMA_14"], width, label="TMA 14% a.a. (Severo)", color="#dc2626", edgecolor="#334155", linewidth=0.5)

    ax_syn.axhline(0, color="#0f172a", linestyle="--", linewidth=1.1)
    ax_syn.set_xticks(x_syn)
    ax_syn.set_xticklabels(df_syn["label"], rotation=35, ha="right", fontsize=8.5, fontweight="bold")
    ax_syn.set_title("Síntese Macrorregional & Média Brasil", fontsize=11, fontweight="bold", color="#0f172a")
    ax_syn.set_ylabel("VPL Ótimo (R$)", fontsize=9)
    ax_syn.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax_syn.legend(loc="upper right", fontsize=8.0)
    ax_syn.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f"R$ {y:,.0f}".replace(",", ".")))

    fig.suptitle("Sensibilidade do VPL Ótimo à Taxa TMA (6%, 10% e 14% a.a.) — 27 Capitais por Macrorregião (UTI)",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    out_png = os.path.join(FIGURAS_DIR, "figura_sensibilidade_tma_capitais.png")
    plt.savefig(out_png)
    plt.close()
    print(" ✓ Gráfico de Sensibilidade TMA por Região gerado.")

    # 10. Figura MCDM VIKOR: Fronteira de Compromisso (Utilidade S vs Arrependimento R)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    ax_a = axes[0]
    typ_markers = {"UTI": "o", "UTG": "s", "MSG": "^", "MFH": "D", "MFL": "v"}
    typ_colors = {"UTI": "#2563eb", "UTG": "#059669", "MSG": "#d97706", "MFH": "#7c3aed", "MFL": "#dc2626"}
    
    for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        s_vals, r_vals, q_vals = [], [], []
        for c in capitals_data:
            if bcode in c["typologies"] and "opt_vikor" in c["typologies"][bcode]:
                v = c["typologies"][bcode]["opt_vikor"]
                s_vals.append(v["s_score"])
                r_vals.append(v["r_score"])
                q_vals.append(v["q_score"])
        if s_vals:
            sizes = 40 + (1.0 - np.array(q_vals)) * 120
            ax_a.scatter(s_vals, r_vals, s=sizes, color=typ_colors.get(bcode, "#2563eb"),
                         marker=typ_markers.get(bcode, "o"), alpha=0.75, edgecolor="#0f172a",
                         label=f"{bcode} ({TYPOLOGY_SPECS[bcode]['name']})", zorder=3)
    
    ax_a.set_title("(A) Espaço de Compromisso VIKOR: Utilidade Coletiva ($S$) vs. Arrependimento Individual ($R$)", fontsize=11, fontweight="bold")
    ax_a.set_xlabel("Medida de Utilidade Coletiva ($S$ — Distância Manhattan Ponderada)", fontsize=10)
    ax_a.set_ylabel("Medida de Arrependimento Individual ($R$ — Máx. Distância Chebyshev)", fontsize=10)
    ax_a.grid(True, linestyle=":", alpha=0.6)
    ax_a.legend(loc="upper left", fontsize=8.5)
    
    # Subplot B: Comparativo de Volumes Ótimos VPL vs VIKOR vs SMAA por Tipologia
    ax_b = axes[1]
    vol_comp_rows = []
    for bcode in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        for c in capitals_data:
            if bcode in c["typologies"]:
                t = c["typologies"][bcode]
                vol_comp_rows.append({
                    "bcode": bcode,
                    "vol_econ": t["opt_econ"]["vol_l"],
                    "vol_vikor": t["opt_vikor"]["vol_l"],
                    "vol_smaa": t["opt_smaa"]["vol_l"]
                })
    df_vol_comp = pd.DataFrame(vol_comp_rows)
    bcodes = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    x = np.arange(len(bcodes))
    w = 0.25
    med_econ = [df_vol_comp[df_vol_comp["bcode"] == b]["vol_econ"].median() for b in bcodes]
    med_vikor = [df_vol_comp[df_vol_comp["bcode"] == b]["vol_vikor"].median() for b in bcodes]
    med_smaa = [df_vol_comp[df_vol_comp["bcode"] == b]["vol_smaa"].median() for b in bcodes]
    
    ax_b.bar(x - w, med_econ, w, label="Ótimo Econômico (VPL)", color="#3b82f6", edgecolor="#1e293b")
    ax_b.bar(x, med_vikor, w, label="Compromisso VIKOR ($Q_{min}$)", color="#10b981", edgecolor="#1e293b")
    ax_b.bar(x + w, med_smaa, w, label="Robustez SMAA ($b_i^1$ máx)", color="#8b5cf6", edgecolor="#1e293b")
    
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(bcodes, fontsize=10, fontweight="bold")
    ax_b.set_title("(B) Volume Mediano de Cisterna (L): Econômico vs. VIKOR vs. SMAA", fontsize=11, fontweight="bold")
    ax_b.set_ylabel("Volume de Armazenamento (Litros)", fontsize=10)
    ax_b.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax_b.legend(loc="upper left", fontsize=8.5)
    
    fig.suptitle("Análise Multicritério MCDM — Fronteira de Compromisso VIKOR e Comparação Volumétrica (27 Capitais)", fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    out_png_vikor = os.path.join(FIGURAS_DIR, "fig_mcdm_vikor_compromise_capitais.png")
    plt.savefig(out_png_vikor)
    plt.close()
    print(" ✓ Figura MCDM VIKOR (Fronteira de Compromisso) gerada.")
    
    # 11. Figura MCDM SMAA: Distribuição de Aceitabilidade de Primeiro Lugar (b_i^1)
    fig, ax_smaa = plt.subplots(figsize=(13, 7))
    vol_cand_list = [500, 1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000, 30000, 40000, 50000]
    smaa_prob_by_vol = {b: {v: [] for v in vol_cand_list} for b in bcodes}
    
    for c in capitals_data:
        for b in bcodes:
            if b in c["typologies"]:
                sweep = c["typologies"][b].get("volume_sweep", [])
                for item in sweep:
                    v = int(item["vol_l"])
                    if v in smaa_prob_by_vol[b]:
                        smaa_prob_by_vol[b][v].append(item.get("smaa_first_prob", 0.0))
                        
    x_vols = np.arange(len(vol_cand_list))
    width_sub = 0.16
    for idx_b, b in enumerate(bcodes):
        mean_probs = [np.mean(smaa_prob_by_vol[b][v]) if smaa_prob_by_vol[b][v] else 0.0 for v in vol_cand_list]
        ax_smaa.bar(x_vols + (idx_b - 2) * width_sub, mean_probs, width_sub,
                    label=f"{b} ({TYPOLOGY_SPECS[b]['name']})", color=typ_colors.get(b, "#2563eb"),
                    edgecolor="#1e293b", linewidth=0.5)
                    
    ax_smaa.set_xticks(x_vols)
    ax_smaa.set_xticklabels([f"{v:,.0f} L" if v < 1000 else f"{v/1000:,.1f} m³".replace(".0", "") for v in vol_cand_list], rotation=35, ha="right", fontsize=9)
    ax_smaa.set_title("Análise Estocástica de Aceitabilidade SMAA-2: Probabilidade Média de 1º Lugar ($b_i^1$) por Volume", fontsize=12, fontweight="bold")
    ax_smaa.set_xlabel("Volume do Reservatório Inferior", fontsize=10)
    ax_smaa.set_ylabel("Probabilidade de Aceitabilidade de Primeiro Posto $b_i^1$ (%)", fontsize=10)
    ax_smaa.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax_smaa.legend(loc="upper right", fontsize=8.5)
    plt.tight_layout()
    out_png_smaa = os.path.join(FIGURAS_DIR, "fig_mcdm_smaa_acceptability_capitais.png")
    plt.savefig(out_png_smaa)
    plt.close()
    print(" ✓ Figura MCDM SMAA (Aceitabilidade de Postos) gerada.")

    # 12. Figura MCDM Pesos Centrais: Decomposição das 3 Dimensões
    fig, ax_cw = plt.subplots(figsize=(11, 6.5))
    cw_rows = []
    for b in bcodes:
        tech_list, econ_list, env_list = [], [], []
        for c in capitals_data:
            if b in c["typologies"] and "opt_smaa" in c["typologies"][b]:
                tech_list.append(c["typologies"][b]["opt_smaa"]["w_tech"])
                econ_list.append(c["typologies"][b]["opt_smaa"]["w_econ"])
                env_list.append(c["typologies"][b]["opt_smaa"]["w_env"])
        cw_rows.append({
            "bcode": b,
            "w_tech": np.mean(tech_list) * 100 if tech_list else 33.3,
            "w_econ": np.mean(econ_list) * 100 if econ_list else 33.3,
            "w_env": np.mean(env_list) * 100 if env_list else 33.4
        })
    df_cw = pd.DataFrame(cw_rows)
    x_cw = np.arange(len(bcodes))
    ax_cw.bar(x_cw, df_cw["w_econ"], 0.5, label="Dimensão Financeira (VPL, Payback, TIR)", color="#059669", edgecolor="#1e293b")
    ax_cw.bar(x_cw, df_cw["w_tech"], 0.5, bottom=df_cw["w_econ"], label="Dimensão Técnica (Economia Hídrica, Extravasamento)", color="#2563eb", edgecolor="#1e293b")
    ax_cw.bar(x_cw, df_cw["w_env"], 0.5, bottom=df_cw["w_econ"] + df_cw["w_tech"], label="Dimensão Ambiental (CO₂ Evitado, Demanda de Rede)", color="#10b981", edgecolor="#1e293b")
    
    ax_cw.set_xticks(x_cw)
    ax_cw.set_xticklabels(bcodes, fontsize=10, fontweight="bold")
    ax_cw.set_ylabel("Composição Ponderal dos Pesos Centrais SMAA (%)", fontsize=10)
    ax_cw.set_title("Vetor de Pesos Centrais Médios ($w_i^c$) que Elege a Solução Mais Aceitável por Tipologia", fontsize=12, fontweight="bold")
    ax_cw.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax_cw.legend(loc="lower right", fontsize=9)
    plt.tight_layout()
    out_png_cw = os.path.join(FIGURAS_DIR, "fig_mcdm_central_weights_ternary_capitais.png")
    plt.savefig(out_png_cw)
    plt.close()
    print(" ✓ Figura MCDM Pesos Centrais SMAA gerada.")


# ====================================================================================================
# GERADOR DO DASHBOARD HTML INTERATIVO AVANÇADO (LEAFLET + CHART.JS + COMPARADOR + TABELA MESTRE)
# ====================================================================================================

def generate_advanced_html_dashboard(capitals_data):
    """Gera a interface completa do Dashboard das 27 Capitais Brasileiras."""
    print("\n🌐 Construindo Dashboard HTML Interativo de Alta Fidelidade...")

    json_capitals = json.dumps(capitals_data, ensure_ascii=False)

    html_code = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netuno 5 — Observatório das 27 Capitais Brasileiras</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --bg-body: #090d16;
            --bg-sidebar: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --bg-card-hover: rgba(51, 65, 85, 0.8);
            --bg-input: #1e293b;
            --border-card: rgba(51, 65, 85, 0.6);
            --border-highlight: rgba(56, 189, 248, 0.4);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --accent-blue: #38bdf8;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-purple: #a855f7;
            --accent-indigo: #6366f1;
            --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
        }}

        html.light {{
            --bg-body: #f1f5f9;
            --bg-sidebar: #ffffff;
            --bg-card: rgba(255, 255, 255, 0.95);
            --bg-card-hover: #f8fafc;
            --bg-input: #ffffff;
            --border-card: #cbd5e1;
            --border-highlight: rgba(2, 132, 199, 0.5);
            --text-main: #0f172a;
            --text-muted: #475569;
            --text-dim: #94a3b8;
            --shadow-card: 0 4px 15px -2px rgba(0, 0, 0, 0.08);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; transition: background-color 0.2s ease, border-color 0.2s ease; }}
        body {{ background-color: var(--bg-body); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }}

        /* Top Header */
        .app-header {{
            background: var(--bg-sidebar);
            border-bottom: 1px solid var(--border-card);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(12px);
        }}
        .brand-box {{ display: flex; align-items: center; gap: 14px; }}
        .brand-icon {{
            width: 40px; height: 40px; border-radius: 10px;
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        }}
        .brand-title h1 {{ font-size: 19px; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .brand-title p {{ font-size: 11.5px; color: var(--text-muted); font-weight: 500; }}

        .header-actions {{ display: flex; align-items: center; gap: 12px; }}
        .search-box {{
            position: relative; width: 260px;
        }}
        .search-box input {{
            width: 100%; background: var(--bg-input); border: 1px solid var(--border-card);
            padding: 8px 12px 8px 34px; border-radius: 8px; font-size: 12.5px; color: var(--text-main);
            outline: none;
        }}
        .search-box input:focus {{ border-color: var(--accent-blue); box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2); }}
        .search-icon {{ position: absolute; left: 10px; top: 50%; transform: translateY(-50%); font-size: 13px; color: var(--text-dim); }}

        .btn-action {{
            background: var(--bg-input); border: 1px solid var(--border-card); color: var(--text-main);
            padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;
            display: flex; align-items: center; gap: 6px;
        }}
        .btn-action:hover {{ background: var(--bg-card-hover); border-color: var(--accent-blue); }}
        .btn-primary {{ background: linear-gradient(135deg, #0284c7, #2563eb); border: none; color: #fff; }}
        .btn-primary:hover {{ opacity: 0.95; }}

        /* Main Container */
        .main-wrapper {{ padding: 22px 28px; max-width: 1700px; margin: 0 auto; width: 100%; flex: 1; }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 22px;
        }}
        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 18px;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-card);
            backdrop-filter: blur(10px);
        }}
        .kpi-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
            background: var(--accent-blue);
        }}
        .kpi-card.emerald::before {{ background: var(--accent-emerald); }}
        .kpi-card.amber::before {{ background: var(--accent-amber); }}
        .kpi-card.purple::before {{ background: var(--accent-purple); }}
        .kpi-card.rose::before {{ background: var(--accent-rose); }}

        .kpi-header {{ display: flex; justify-content: space-between; align-items: center; }}
        .kpi-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px; }}
        .kpi-icon {{ font-size: 18px; opacity: 0.8; }}
        .kpi-value {{ font-size: 24px; font-weight: 800; color: var(--text-main); margin: 8px 0 4px; letter-spacing: -0.5px; }}
        .kpi-sub {{ font-size: 11.5px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }}

        /* Controls Filter Bar */
        .controls-card {{
            background: var(--bg-sidebar);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
            box-shadow: var(--shadow-card);
        }}
        .filter-group {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
        .filter-label {{ font-size: 11.5px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); }}
        .pill-selector {{
            display: flex; background: var(--bg-input); border: 1px solid var(--border-card); border-radius: 8px; padding: 3px; gap: 3px;
        }}
        .pill-btn {{
            background: transparent; border: none; padding: 6px 12px; border-radius: 6px;
            color: var(--text-muted); font-size: 12px; font-weight: 600; cursor: pointer;
        }}
        .pill-btn.active {{
            background: var(--accent-blue); color: #ffffff; box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
        }}

        /* Tabs Navigation */
        .tab-nav {{
            display: flex;
            gap: 8px;
            border-bottom: 1px solid var(--border-card);
            margin-bottom: 22px;
            overflow-x: auto;
            padding-bottom: 2px;
        }}
        .tab-btn {{
            background: transparent; border: none; padding: 12px 18px; color: var(--text-muted);
            font-size: 13.5px; font-weight: 600; cursor: pointer; border-bottom: 3px solid transparent;
            display: flex; align-items: center; gap: 8px; white-space: nowrap;
        }}
        .tab-btn:hover {{ color: var(--text-main); }}
        .tab-btn.active {{
            color: var(--accent-blue); border-bottom-color: var(--accent-blue);
        }}

        /* Tab Panes */
        .tab-pane {{ display: none; }}
        .tab-pane.active {{ display: block; }}

        /* Map Section */
        .map-grid {{
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 18px;
            margin-bottom: 22px;
        }}
        @media (max-width: 1100px) {{
            .map-grid {{ grid-template-columns: 1fr; }}
        }}
        .map-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 16px;
            box-shadow: var(--shadow-card);
            position: relative;
        }}
        #brazilMap {{ height: 560px; width: 100%; border-radius: 8px; z-index: 1; }}

        .map-side-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .panel-title {{ font-size: 14px; font-weight: 700; color: var(--text-main); display: flex; align-items: center; justify-content: space-between; }}
        .map-layer-select {{
            background: var(--bg-input); border: 1px solid var(--border-card); color: var(--text-main);
            padding: 8px 12px; border-radius: 8px; font-size: 12.5px; width: 100%; outline: none;
        }}
        .mini-rank-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; }}
        .mini-rank-item {{
            display: flex; justify-content: space-between; align-items: center;
            background: var(--bg-input); padding: 9px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;
        }}
        .mini-rank-item:hover {{ border-left: 3px solid var(--accent-blue); }}
        .val-badge {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 11.5px; }}

        /* Charts Grid */
        .charts-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 18px;
            margin-bottom: 22px;
        }}
        @media (max-width: 768px) {{
            .charts-row {{ grid-template-columns: 1fr; }}
        }}
        .chart-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--shadow-card);
        }}
        .chart-box-header {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;
        }}
        .chart-box-title {{ font-size: 14.5px; font-weight: 700; color: var(--text-main); }}

        /* Table Card */
        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--shadow-card);
            overflow-x: auto;
        }}
        table.data-table {{
            width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left;
        }}
        table.data-table th {{
            background: var(--bg-sidebar); color: var(--text-muted); font-weight: 700;
            padding: 12px 14px; border-bottom: 2px solid var(--border-card); text-transform: uppercase; font-size: 10.5px;
            cursor: pointer; user-select: none;
        }}
        table.data-table th:hover {{ color: var(--accent-blue); }}
        table.data-table td {{
            padding: 12px 14px; border-bottom: 1px solid var(--border-card); color: var(--text-main);
        }}
        table.data-table tr:hover {{ background: var(--bg-card-hover); cursor: pointer; }}
        .badge-regiao {{ padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 10px; color: white; }}
        .pos-num {{ color: var(--accent-emerald); font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
        .neg-num {{ color: var(--accent-rose); font-weight: 700; font-family: 'JetBrains Mono', monospace; }}

        /* Comparator Tool */
        .comparator-grid {{
            display: grid;
            grid-template-columns: 1fr 80px 1fr;
            gap: 16px;
            margin-bottom: 22px;
            align-items: center;
        }}
        @media (max-width: 900px) {{
            .comparator-grid {{ grid-template-columns: 1fr; }}
            .vs-circle {{ margin: 0 auto; }}
        }}
        .comp-card {{
            background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; padding: 22px;
        }}
        .vs-circle {{
            width: 50px; height: 50px; border-radius: 50%; background: var(--accent-purple); color: white;
            display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
        }}

        /* Figures Gallery */
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 20px;
        }}
        .gallery-item {{
            background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;
            box-shadow: var(--shadow-card); transition: transform 0.2s ease;
        }}
        .gallery-item:hover {{ transform: translateY(-4px); border-color: var(--accent-blue); }}
        .gallery-img-wrap {{
            height: 240px; background: #000; overflow: hidden; display: flex; align-items: center; justify-content: center;
        }}
        .gallery-img-wrap img {{ width: 100%; height: 100%; object-fit: cover; cursor: pointer; }}
        .gallery-info {{ padding: 16px; }}
        .gallery-title {{ font-size: 13.5px; font-weight: 700; margin-bottom: 6px; }}
        .gallery-desc {{ font-size: 11.5px; color: var(--text-muted); line-height: 1.5; margin-bottom: 12px; }}

        /* Detail Modal / Drawer */
        .modal-overlay {{
            position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(6px); z-index: 2000; display: none; align-items: center; justify-content: center;
            padding: 20px;
        }}
        .modal-overlay.active {{ display: flex; }}
        .modal-container {{
            background: var(--bg-sidebar); border: 1px solid var(--border-card); border-radius: 16px;
            width: 100%; max-width: 1000px; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);
            padding: 28px; position: relative;
        }}
        .modal-close {{
            position: absolute; top: 20px; right: 20px; background: var(--bg-input); border: 1px solid var(--border-card);
            width: 34px; height: 34px; border-radius: 8px; color: var(--text-main); font-size: 18px; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
        }}
        .modal-close:hover {{ background: var(--accent-rose); color: white; }}

        /* Image Lightbox */
        #imgLightbox {{
            position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.92);
            z-index: 3000; display: none; align-items: center; justify-content: center; padding: 20px; cursor: zoom-out;
        }}
        #imgLightbox.active {{ display: flex; }}
        #imgLightbox img {{ max-width: 95vw; max-height: 95vh; border-radius: 8px; box-shadow: 0 0 30px rgba(0,0,0,0.8); }}

        /* Footer */
        .app-footer {{
            background: var(--bg-sidebar); border-top: 1px solid var(--border-card); padding: 18px 28px;
            text-align: center; font-size: 12px; color: var(--text-muted); margin-top: auto;
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header class="app-header">
        <div class="brand-box">
            <div class="brand-icon">💧</div>
            <div class="brand-title">
                <h1>Netuno 5 — Observatório das 27 Capitais Brasileiras</h1>
                <p>Otimização Técnico-Econômica, Pegada Hídrica e Resiliência Climática CMIP6</p>
            </div>
        </div>
        <div class="header-actions">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="globalSearch" placeholder="Buscar capital, UF ou prestador..." oninput="handleSearch(this.value)">
            </div>
            <button class="btn-action" onclick="toggleTheme()" id="themeToggleBtn">🌙 Tema</button>
            <button class="btn-action btn-primary" onclick="exportDataCSV()">📥 Exportar CSV</button>
        </div>
    </header>

    <div class="main-wrapper">

        <!-- Top KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card emerald">
                <div class="kpi-header">
                    <span class="kpi-title">Maior VPL Ótimo Nacional</span>
                    <span class="kpi-icon">🏆</span>
                </div>
                <div class="kpi-value" id="kpi-max-vpl">R$ 9.563,05</div>
                <div class="kpi-sub" id="kpi-max-vpl-sub">Florianópolis (SC) — Cisterna 5.000 L</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Média Nacional de VPL</span>
                    <span class="kpi-icon">📊</span>
                </div>
                <div class="kpi-value" id="kpi-avg-vpl">R$ -1.729,42</div>
                <div class="kpi-sub" id="kpi-avg-vpl-sub">27 Capitais Brasileiras</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-header">
                    <span class="kpi-title">Economia Pluvial Média</span>
                    <span class="kpi-icon">💧</span>
                </div>
                <div class="kpi-value" id="kpi-avg-sav">17,4%</div>
                <div class="kpi-sub" id="kpi-avg-sav-sub">Atendimento de Demanda Não-Potável</div>
            </div>
            <div class="kpi-card purple">
                <div class="kpi-header">
                    <span class="kpi-title">Capitais com VPL Positivo</span>
                    <span class="kpi-icon">📈</span>
                </div>
                <div class="kpi-value" id="kpi-pos-rate">3 / 27 (11,1%)</div>
                <div class="kpi-sub" id="kpi-pos-sub">Tipologia Unifamiliar Térrea (UTI)</div>
            </div>
            <div class="kpi-card rose">
                <div class="kpi-header">
                    <span class="kpi-title">Descarbonização Consolidada</span>
                    <span class="kpi-icon">🌿</span>
                </div>
                <div class="kpi-value" id="kpi-total-co2">28,4 t CO₂</div>
                <div class="kpi-sub">Saldo Líquido Evitado na Vida Útil</div>
            </div>
        </div>

        <!-- Global Filter Controls -->
        <div class="controls-card">
            <div class="filter-group">
                <span class="filter-label">Tipologia Edilícia:</span>
                <div class="pill-selector" id="typologySelector">
                    <button class="pill-btn active" data-val="UTI" onclick="setTypology('UTI')">UTI (4 hab)</button>
                    <button class="pill-btn" data-val="UTG" onclick="setTypology('UTG')">UTG (8 hab)</button>
                    <button class="pill-btn" data-val="MSG" onclick="setTypology('MSG')">MSG (16 hab)</button>
                    <button class="pill-btn" data-val="MFH" onclick="setTypology('MFH')">MFH (64 hab)</button>
                    <button class="pill-btn" data-val="MFL" onclick="setTypology('MFL')">MFL (128 hab)</button>
                </div>
            </div>

            <div class="filter-group">
                <span class="filter-label">Região:</span>
                <div class="pill-selector" id="regionSelector">
                    <button class="pill-btn active" data-val="ALL" onclick="setRegion('ALL')">Todas</button>
                    <button class="pill-btn" data-val="Norte" onclick="setRegion('Norte')">Norte</button>
                    <button class="pill-btn" data-val="Nordeste" onclick="setRegion('Nordeste')">Nordeste</button>
                    <button class="pill-btn" data-val="Centro-Oeste" onclick="setRegion('Centro-Oeste')">C.-Oeste</button>
                    <button class="pill-btn" data-val="Sudeste" onclick="setRegion('Sudeste')">Sudeste</button>
                    <button class="pill-btn" data-val="Sul" onclick="setRegion('Sul')">Sul</button>
                </div>
            </div>

            <div class="filter-group">
                <span class="filter-label">Taxa TMA:</span>
                <div class="pill-selector" id="tmaSelector">
                    <button class="pill-btn active" data-val="6" onclick="setTMA(6)">6% a.a.</button>
                    <button class="pill-btn" data-val="10" onclick="setTMA(10)">10% a.a.</button>
                    <button class="pill-btn" data-val="14" onclick="setTMA(14)">14% a.a.</button>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <nav class="tab-nav">
            <button class="tab-btn active" onclick="switchTab('tab-mapa')">🗺️ Mapa Interativo do Brasil</button>
            <button class="tab-btn" onclick="switchTab('tab-rankings')">📊 Rankings & Curvas Canônicas</button>
            <button class="tab-btn" onclick="switchTab('tab-matriz')">🏢 Matriz 5 Tipologias</button>
            <button class="tab-btn" onclick="switchTab('tab-clima')">🌦️ Mudanças Climáticas (CMIP6)</button>
            <button class="tab-btn" onclick="switchTab('tab-comparador')">⚖️ Comparador Lado a Lado</button>
            <button class="tab-btn" onclick="switchTab('tab-tabela')">📋 Tabela Mestre Avançada</button>
            <button class="tab-btn" onclick="switchTab('tab-galeria')">🖼️ Galeria de Figuras Científicas</button>
        </nav>

        <!-- TAB 1: MAPA DO BRASIL -->
        <div id="tab-mapa" class="tab-pane active">
            <div class="map-grid">
                <div class="map-card">
                    <div id="brazilMap"></div>
                </div>
                <div class="map-side-panel">
                    <div class="panel-title">
                        <span>Configuração da Camada</span>
                        <span style="font-size: 18px;">🎯</span>
                    </div>
                    <div>
                        <label style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Métrica no Mapa:</label>
                        <select class="map-layer-select" id="mapMetricSelect" onchange="updateMapMarkers()" style="margin-top: 6px;">
                            <option value="vpl">Valor Presente Líquido - VPL Ótimo (R$)</option>
                            <option value="savings">Economia Pluvial Potencial (%)</option>
                            <option value="vol">Capacidade Ótima da Cisterna (L)</option>
                            <option value="pb">Payback Descontado (anos)</option>
                            <option value="tarifa">Tarifa Base de Água Concessionária (R$/m³)</option>
                            <option value="co2">Saldo de CO₂ Evitado na Vida Útil (kg)</option>
                        </select>
                    </div>

                    <div style="border-top: 1px solid var(--border-card); padding-top: 12px;">
                        <div class="panel-title" style="margin-bottom: 8px;">
                            <span>Top 5 Capitais — <span id="sideRankTitle">VPL</span></span>
                        </div>
                        <ul class="mini-rank-list" id="topRankList"></ul>
                    </div>

                    <div style="border-top: 1px solid var(--border-card); padding-top: 12px;">
                        <div class="panel-title" style="margin-bottom: 8px; color: var(--accent-rose);">
                            <span>5 Menores Desempenhos</span>
                        </div>
                        <ul class="mini-rank-list" id="bottomRankList"></ul>
                    </div>
                </div>
            </div>
        </div>
        <!-- TAB 2: RANKINGS & CURVAS -->
        <div id="tab-rankings" class="tab-pane">
            <div class="charts-row">
                <div class="chart-box" style="grid-column: span 2;">
                    <div class="chart-box-header">
                        <span class="chart-box-title" id="barChartTitle">📊 Ranking Nacional das 27 Capitais por VPL Ótimo (R$)</span>
                        <div style="display: flex; gap: 8px;">
                            <select class="map-layer-select" id="barMetricSelect" onchange="updateRankingChart()" style="width: 220px;">
                                <option value="vpl">VPL Ótimo (R$)</option>
                                <option value="savings">Economia Pluvial (%)</option>
                                <option value="vol">Volume Ótimo (L)</option>
                                <option value="capex">CAPEX Total (R$)</option>
                                <option value="consumed">Volume Consumido (m³/ano)</option>
                                <option value="co2">CO₂ Líquido Evitado (kg)</option>
                                <option value="topsis">TOPSIS Score (%)</option>
                            </select>
                        </div>
                    </div>
                    <div style="height: 580px;">
                        <canvas id="rankingChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="charts-row">
                <div class="chart-box">
                    <div class="chart-box-header">
                        <span class="chart-box-title">📈 Curva Canônica VPL vs. Volume (Estilo Netuno 5 GUI)</span>
                        <select class="map-layer-select" id="curveCitySelect" onchange="updateCurveChart()" style="width: 200px;"></select>
                    </div>
                    <div style="height: 380px;">
                        <canvas id="canonicalCurveChart"></canvas>
                    </div>
                </div>

                <div class="chart-box">
                    <div class="chart-box-header">
                        <span class="chart-box-title">🕸️ Radar Multi-Critério TOPSIS Normalizado</span>
                        <select class="map-layer-select" id="radarCitySelect" onchange="updateRadarChart()" style="width: 200px;"></select>
                    </div>
                    <div style="height: 380px;">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: MATRIZ 5 TIPOLOGIAS -->
        <div id="tab-matriz" class="tab-pane">
            <div class="chart-box" style="margin-bottom: 22px;">
                <div class="chart-box-header">
                    <span class="chart-box-title">🏢 Comparativo de Ganhos de Escala: Unifamiliar vs. Multifamiliar (UTI a MFL)</span>
                    <select class="map-layer-select" id="matrixCitySelect" onchange="updateMatrixChart()" style="width: 220px;"></select>
                </div>
                <div style="height: 420px;">
                    <canvas id="typologyCompChart"></canvas>
                </div>
            </div>

            <div class="chart-box">
                <div class="chart-box-header">
                    <span class="chart-box-title">📊 Distribuição Regional de VPL por Tipologia (Boxplots Médios)</span>
                </div>
                <div style="height: 400px;">
                    <canvas id="regionBoxChart"></canvas>
                </div>
            </div>
        </div>

        <!-- TAB 4: MUDANÇAS CLIMÁTICAS CMIP6 -->
        <div id="tab-clima" class="tab-pane">
            <div class="charts-row">
                <div class="chart-box">
                    <div class="chart-box-header">
                        <span class="chart-box-title">🌦️ Trajetória Temporal de Economia Pluvial (%): SSP2-4.5 vs. SSP5-8.5</span>
                        <select class="map-layer-select" id="climateCitySelect" onchange="updateClimateChart()" style="width: 200px;"></select>
                    </div>
                    <div style="height: 400px;">
                        <canvas id="climateTrajectoryChart"></canvas>
                    </div>
                </div>

                <div class="chart-box">
                    <div class="chart-box-header">
                        <span class="chart-box-title">📉 Variação Temporal de Potencial Pluvial: Δ% (Far 2085 − Histórico)</span>
                    </div>
                    <div style="height: 400px;">
                        <canvas id="deltaVChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: COMPARADOR LADO A LADO -->
        <div id="tab-comparador" class="tab-pane">
            <div class="controls-card" style="margin-bottom: 18px; display: flex; align-items: center; justify-content: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 700; font-size: 13px;">Capital A:</span>
                    <select class="map-layer-select" id="compCityA" onchange="updateComparator()" style="width: 200px;"></select>
                </div>
                <div style="background: linear-gradient(135deg, #0284c7, #a855f7); color: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px;">VS</div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 700; font-size: 13px;">Capital B:</span>
                    <select class="map-layer-select" id="compCityB" onchange="updateComparator()" style="width: 200px;"></select>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 20px;">
                <div class="kpi-card" id="compCardA"></div>
                <div class="kpi-card" id="compCardB"></div>
            </div>

            <div class="chart-box">
                <div class="chart-box-header">
                    <span class="chart-box-title">📊 Comparativo Direto Multi-Critério (Capital A vs. Capital B)</span>
                </div>
                <div style="height: 380px;">
                    <canvas id="compBarChart"></canvas>
                </div>
            </div>
        </div>

        <!-- TAB 6: TABELA MESTRE -->
        <div id="tab-tabela" class="tab-pane">
            <div class="table-card">
                <div class="table-toolbar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div style="position: relative; width: 320px;">
                        <input type="text" id="tableSearchInput" placeholder="🔍 Filtrar capital, UF ou região..." oninput="renderMasterTable()" style="width: 100%; background: var(--bg-input); border: 1px solid var(--border-card); padding: 8px 12px; border-radius: 8px; font-size: 12.5px; color: var(--text-main); outline: none;">
                    </div>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <span id="tableCountInfo" style="font-size: 12px; color: var(--text-muted);">Exibindo 27 de 27 capitais</span>
                        <button class="btn-action btn-primary" onclick="exportTableToCSV()">📥 Baixar CSV Completo</button>
                    </div>
                </div>
                <div style="overflow-x: auto; max-height: 650px;">
                    <table class="master-table" style="width: 100%; border-collapse: collapse; font-size: 12px;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-card); text-align: left;">
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(0)">Capital ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(1)">UF ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(2)">Região ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(3)">Concessionária ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(4)">Tarifa (R$/m³) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(5)">Vol. Ótimo ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(6)">VPL Ótimo ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(7)">Economia (%) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(8)">Consumo (m³/ano) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(9)">CAPEX (R$) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(10)">Payback Desc. ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(11)">TIR (% a.a.) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(12)">CO₂ Evitado (kg) ↕</th>
                                <th style="padding: 10px; cursor: pointer;" onclick="sortTable(13)">TOPSIS ↕</th>
                                <th style="padding: 10px;">Ações</th>
                            </tr>
                        </thead>
                        <tbody id="masterTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 7: GALERIA DE FIGURAS CIENTÍFICAS -->
        <div id="tab-galeria" class="tab-pane">
            <div style="margin-bottom: 16px;">
                <h2 style="font-size: 18px; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">Galeria de Figuras Científicas do Estudo (300 DPI)</h2>
                <p style="font-size: 13px; color: var(--text-muted);">Figuras analíticas de alta resolução geradas com Matplotlib prontas para inserção no artigo científico e relatórios técnicos.</p>
            </div>
            <div class="gallery-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px;">
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/ranking_nacional_vpl_otimo_UTI.png" alt="Ranking UTI VPL" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Ranking Nacional de VPL — Casa Unifamiliar (UTI)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Distribuição do VPL ótimo e capacidade ideal de cisterna para 4 habitantes nas 27 capitais.</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/ranking_nacional_vpl_otimo_MFH.png" alt="Ranking MFH VPL" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Ranking Nacional de VPL — Bloco Multifamiliar H (MFH)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Desempenho econômico em condomínios residenciais coletivos (64 habitantes).</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/matriz_multitipologia_vpl_otimo_27_capitais.png" alt="Matriz Multi-Tipologia VPL" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Matriz Multi-Tipologia do VPL Ótimo (5 Tipologias)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Comparativo sistemático de ganhos de escala da UTI (4 hab) ao MFL (128 hab) nas 27 capitais.</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/matriz_multitipologia_co2_otimo_27_capitais.png" alt="Matriz Multi-Tipologia CO2" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #10b981; margin-bottom: 4px;">Balanço Ambiental: CO₂ Líquido Evitado (5 Tipologias)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Balanço líquido de carbono na vida útil de 20 anos em todas as capitais brasileiras.</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/ranking_nacional_co2_otimo_MFL.png" alt="Ranking MFL CO2" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #10b981; margin-bottom: 4px;">Ranking Nacional de Descarbonização — MFL (128 hab)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Toneladas de CO₂ evitadas por edifício residencial de alta densidade no Brasil.</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/figura_curvas_co2_vs_volume_5_tipologias.png" alt="Curvas CO2 vs Volume" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #10b981; margin-bottom: 4px;">Curvas de CO₂ Líquido Evitado vs. Volume de Cisterna</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Trade-off entre carbono incorporado nos reservatórios e emissões evitadas de água tratada.</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/figura_radar_multicriterio_capitais.png" alt="Radar TOPSIS" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Radar Multi-Critério TOPSIS Normalizado (UTI vs. MFL)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Avaliação pareada das 6 dimensões de projeto (água, VPL, payback, CO₂, confiabilidade, tarifa).</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/figura_trajetorias_climaticas_capitais_cmip6.png" alt="Trajetórias Climáticas CMIP6" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Projeções Climáticas CMIP6 ao Longo do Século XXI</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Evolução temporal do potencial pluvial sob cenários SSP2-4.5 e SSP5-8.5 (1980–2100).</p>
                    </div>
                </div>
                <div class="gallery-card" style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; overflow: hidden;">
                    <img src="figuras/figura_sensibilidade_tma_capitais.png" alt="Sensibilidade TMA" style="width: 100%; height: auto; cursor: pointer;" onclick="openLightbox(this.src)">
                    <div style="padding: 14px;">
                        <h4 style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">Sensibilidade do VPL à Taxa de Atratividade (TMA)</h4>
                        <p style="font-size: 11.5px; color: var(--text-muted);">Impacto de taxas reais de 6%, 10% e 14% a.a. na viabilidade financeira das capitais.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Capital Detail Modal -->
    <div class="modal-overlay" id="detailModal" onclick="closeModal(event)" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 2000; align-items: center; justify-content: center; backdrop-filter: blur(8px);">
        <div class="modal-container" style="background: var(--bg-sidebar); border: 1px solid var(--border-card); border-radius: 16px; width: 90%; max-width: 850px; max-height: 90vh; overflow-y: auto; padding: 24px; position: relative;">
            <button class="modal-close" onclick="closeModal(null, true)" style="position: absolute; right: 18px; top: 18px; background: var(--bg-input); border: 1px solid var(--border-card); color: var(--text-main); width: 32px; height: 32px; border-radius: 8px; cursor: pointer; font-size: 16px;">✕</button>
            <div id="modalContent"></div>
        </div>
    </div>

    <!-- Image Lightbox -->
    <div id="imgLightbox" onclick="closeLightbox()" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 3000; align-items: center; justify-content: center; padding: 20px;">
        <img id="lightboxImg" src="" alt="Figura Ampliada" style="max-width: 95%; max-height: 95%; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
    </div>

    <footer class="app-footer" style="padding: 20px; text-align: center; border-top: 1px solid var(--border-card); margin-top: 40px; font-size: 12px; color: var(--text-muted);">
        <p><strong>Netuno 5</strong> — Plataforma Avançada de Modelagem Hidrológica e Análise de Investimento em Recursos Hídricos Pluviais</p>
        <p style="margin-top: 4px; font-size: 11px;">Estudo de 5 Tipologias Residenciais sob Projeções CMIP6 • Dados de 652 Municípios Brasileiros • 27 Capitais</p>
    </footer>

    <script>
        // Carrega dados completos serializados
        const capitalsData = {json_capitals};

        let currentTypology = "UTI";
        let currentRegion = "ALL";
        let currentTMA = 6;
        let map = null;
        let mapMarkers = [];

        // Inicialização do Leaflet Map
        function initMap() {{
            map = L.map('brazilMap', {{
                center: [-14.2350, -51.9253],
                zoom: 4,
                zoomControl: true
            }});

            const isDark = document.documentElement.classList.contains('dark');
            const tileUrl = isDark
                ? 'https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png'
                : 'https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png';

            L.tileLayer(tileUrl, {{
                attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
                maxZoom: 18
            }}).addTo(map);

            updateMapMarkers();
        }}

        function getFilteredCapitals() {{
            return capitalsData.filter(c => {{
                if (currentRegion !== "ALL" && c.regiao !== currentRegion) return false;
                return true;
            }});
        }}

        function updateMapMarkers() {{
            if (!map) return;
            mapMarkers.forEach(m => map.removeLayer(m));
            mapMarkers = [];

            const metric = document.getElementById('mapMetricSelect').value;
            const filtered = getFilteredCapitals();

            // Determinar min e max da métrica
            const vals = filtered.map(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                if (!opt) return 0;
                if (metric === "vpl") return currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                if (metric === "savings") return opt.savings_pct;
                if (metric === "vol") return opt.vol_l;
                if (metric === "pb") return opt.pb_desc_6 <= 20 ? opt.pb_desc_6 : 25;
                if (metric === "tarifa") return c.tarifa_agua_base_r_m3;
                if (metric === "co2") return opt.net_co2_kg;
                return 0;
            }});

            const minVal = Math.min(...vals);
            const maxVal = Math.max(...vals);

            filtered.forEach(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                if (!opt) return;

                let val = 0;
                if (metric === "vpl") val = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                else if (metric === "savings") val = opt.savings_pct;
                else if (metric === "vol") val = opt.vol_l;
                else if (metric === "pb") val = opt.pb_desc_6 <= 20 ? opt.pb_desc_6 : 25;
                else if (metric === "tarifa") val = c.tarifa_agua_base_r_m3;
                else if (metric === "co2") val = opt.net_co2_kg;

                // Normalização de cor
                const ratio = maxVal > minVal ? (val - minVal) / (maxVal - minVal) : 0.5;
                let color = "#38bdf8";
                if (metric === "vpl") {{
                    color = val >= 0 ? "#10b981" : "#f43f5e";
                }} else if (metric === "pb") {{
                    color = val <= 20 ? "#10b981" : "#f43f5e";
                }} else {{
                    color = ratio > 0.6 ? "#10b981" : (ratio > 0.3 ? "#38bdf8" : "#f59e0b");
                }}

                const radius = 8 + ratio * 8;

                const marker = L.circleMarker([c.lat, c.lon], {{
                    radius: radius,
                    fillColor: color,
                    color: "#ffffff",
                    weight: 1.5,
                    opacity: 0.9,
                    fillOpacity: 0.85
                }}).addTo(map);

                marker.bindPopup(`
                    <div style="font-family: 'Inter', sans-serif; min-width: 200px;">
                        <h4 style="margin: 0 0 6px; font-weight: 800; color: #0284c7;">${{c.city}} (${{c.uf}})</h4>
                        <div style="font-size: 11.5px; color: #475569; line-height: 1.5;">
                            <strong>Região:</strong> ${{c.regiao}}<br>
                            <strong>Prestador:</strong> ${{c.prestador}}<br>
                            <strong>Tarifa Água:</strong> R$ ${{c.tarifa_agua_base_r_m3.toFixed(2)}}/m³<br>
                            <strong>Vol. Ótimo:</strong> ${{opt.vol_l.toLocaleString('pt-BR')}} L<br>
                            <strong>VPL Ótimo (TMA ${{currentTMA}}%):</strong> <span style="font-weight: bold; color: ${{val >= 0 ? '#10b981' : '#ef4444'}};">R$ ${{opt.vpl_6.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</span><br>
                            <strong>Economia Pluvial:</strong> ${{opt.savings_pct.toFixed(1)}}%<br>
                            <strong>Payback Desc.:</strong> ${{opt.pb_desc_6 <= 20 ? opt.pb_desc_6.toFixed(1) + ' anos' : 'Sem Retorno'}}
                        </div>
                        <button onclick="openDetailModal('${{c.city}}')" style="margin-top: 10px; width: 100%; background: #0284c7; color: white; border: none; padding: 6px; border-radius: 6px; font-weight: 700; cursor: pointer;">Ver Dossiê Completo</button>
                    </div>
                `);

                mapMarkers.push(marker);
            }});

            updateSideRankings(filtered, metric);
        }}

        function updateSideRankings(filtered, metric) {{
            const listData = filtered.map(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                let val = 0;
                let text = "";
                if (metric === "vpl") {{
                    val = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                    text = `R$ ${{val.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}`;
                }} else if (metric === "savings") {{
                    val = opt.savings_pct;
                    text = `${{val.toFixed(1)}}%`;
                }} else if (metric === "vol") {{
                    val = opt.vol_l;
                    text = `${{val.toLocaleString('pt-BR')}} L`;
                }} else if (metric === "pb") {{
                    val = opt.pb_desc_6 <= 20 ? opt.pb_desc_6 : 99;
                    text = val <= 20 ? `${{val.toFixed(1)}}a` : `>20a`;
                }} else if (metric === "tarifa") {{
                    val = c.tarifa_agua_base_r_m3;
                    text = `R$ ${{val.toFixed(2)}}/m³`;
                }} else if (metric === "co2") {{
                    val = opt.net_co2_kg;
                    text = `${{val.toFixed(0)}} kg`;
                }}
                return {{ city: c.city, uf: c.uf, val: val, text: text }};
            }});

            listData.sort((a, b) => b.val - a.val);

            const topEl = document.getElementById('topRankList');
            const botEl = document.getElementById('bottomRankList');
            topEl.innerHTML = "";
            botEl.innerHTML = "";

            listData.slice(0, 5).forEach((item, i) => {{
                topEl.innerHTML += `
                    <li class="mini-rank-item" onclick="openDetailModal('${{item.city}}')">
                        <span><strong>#${{i+1}}</strong> ${{item.city}} (${{item.uf}})</span>
                        <span class="val-badge pos-num">${{item.text}}</span>
                    </li>
                `;
            }});

            listData.slice(-5).reverse().forEach((item, i) => {{
                botEl.innerHTML += `
                    <li class="mini-rank-item" onclick="openDetailModal('${{item.city}}')">
                        <span><strong>#${{listData.length - i}}</strong> ${{item.city}} (${{item.uf}})</span>
                        <span class="val-badge neg-num">${{item.text}}</span>
                    </li>
                `;
            }});
        }}

        // Gestão de Filtros Globais
        function setTypology(typ) {{
            currentTypology = typ;
            document.querySelectorAll('#typologySelector .pill-btn').forEach(b => {{
                b.classList.toggle('active', b.dataset.val === typ);
            }});
            refreshAll();
        }}

        function setRegion(reg) {{
            currentRegion = reg;
            document.querySelectorAll('#regionSelector .pill-btn').forEach(b => {{
                b.classList.toggle('active', b.dataset.val === reg);
            }});
            refreshAll();
        }}

        function setTMA(tma) {{
            currentTMA = tma;
            document.querySelectorAll('#tmaSelector .pill-btn').forEach(b => {{
                b.classList.toggle('active', parseInt(b.dataset.val) === tma);
            }});
            refreshAll();
        }}

        function refreshAll() {{
            updateKPIs();
            updateMapMarkers();
            updateRankingChart();
            updateCurveChart();
            updateRadarChart();
            updateMatrixChart();
            updateClimateChart();
            updateComparator();
            renderMasterTable();
        }}

        function updateKPIs() {{
            const filtered = getFilteredCapitals();
            if (filtered.length === 0) return;

            let maxVpl = -Infinity;
            let maxCity = "";
            let maxVol = 0;
            let totalVpl = 0;
            let totalSav = 0;
            let posCount = 0;
            let totalCO2 = 0;

            filtered.forEach(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                if (!opt) return;
                const vpl = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                if (vpl > maxVpl) {{
                    maxVpl = vpl;
                    maxCity = `${{c.city}} (${{c.uf}})`;
                    maxVol = opt.vol_l;
                }}
                totalVpl += vpl;
                totalSav += opt.savings_pct;
                if (vpl > 0) posCount++;
                totalCO2 += opt.net_co2_kg;
            }});

            const avgVpl = totalVpl / filtered.length;
            const avgSav = totalSav / filtered.length;

            document.getElementById('kpi-max-vpl').textContent = `R$ ${{maxVpl.toLocaleString('pt-BR', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;
            document.getElementById('kpi-max-vpl-sub').textContent = `${{maxCity}} — Cisterna ${{maxVol.toLocaleString('pt-BR')}} L`;

            document.getElementById('kpi-avg-vpl').textContent = `R$ ${{avgVpl.toLocaleString('pt-BR', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;
            document.getElementById('kpi-avg-vpl').className = `kpi-value ${{avgVpl >= 0 ? 'pos-num' : 'neg-num'}}`;

            document.getElementById('kpi-avg-sav').textContent = `${{avgSav.toFixed(1)}}%`;
            document.getElementById('kpi-pos-rate').textContent = `${{posCount}} / ${{filtered.length}} (${{((posCount/filtered.length)*100).toFixed(1)}}%)`;
            document.getElementById('kpi-pos-sub').textContent = `Tipologia ${{currentTypology}} • TMA ${{currentTMA}}% a.a.`;
            document.getElementById('kpi-total-co2').textContent = `${{(totalCO2/1000).toFixed(1)}} t CO₂`;
        }}

        // Gráficos Chart.js
        let rankingChartInstance = null;
        let curveChartInstance = null;
        let radarChartInstance = null;
        let matrixChartInstance = null;
        let regionBoxChartInstance = null;
        let climateChartInstance = null;
        let deltaVChartInstance = null;
        let compBarChartInstance = null;

        const regionColorMap = {{
            "Norte": "#0284c7",
            "Nordeste": "#d97706",
            "Centro-Oeste": "#059669",
            "Sudeste": "#7c3aed",
            "Sul": "#2563eb"
        }};

        function updateRankingChart() {{
            const ctx = document.getElementById('rankingChart').getContext('2d');
            if (rankingChartInstance) rankingChartInstance.destroy();

            const metric = document.getElementById('barMetricSelect').value;
            const filtered = getFilteredCapitals();

            const dataPoints = filtered.map(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                let val = 0;
                if (metric === "vpl") val = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                else if (metric === "savings") val = opt.savings_pct;
                else if (metric === "vol") val = opt.vol_l;
                else if (metric === "capex") val = opt.capex;
                else if (metric === "consumed") val = opt.consumed_m3;
                else if (metric === "topsis") val = opt.topsis * 100;
                return {{
                    city: c.city,
                    uf: c.uf,
                    regiao: c.regiao,
                    val: val,
                    vol: opt.vol_l
                }};
            }}).sort((a, b) => a.val - b.val);

            rankingChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: dataPoints.map(d => `${{d.city}} (${{d.uf}}) — ${{d.vol.toLocaleString('pt-BR')}} L`),
                    datasets: [{{
                        data: dataPoints.map(d => d.val),
                        backgroundColor: dataPoints.map(d => regionColorMap[d.regiao] || '#64748b'),
                        borderColor: '#0f172a',
                        borderWidth: 1,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: ctx => `Valor: ${{ctx.parsed.x.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}`
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            ticks: {{ color: '#94a3b8' }}
                        }},
                        y: {{
                            grid: {{ display: false }},
                            ticks: {{ color: '#f8fafc', font: {{ size: 11, weight: '600' }} }}
                        }}
                    }}
                }}
            }});
        }}

        function updateCurveChart() {{
            const ctx = document.getElementById('canonicalCurveChart').getContext('2d');
            if (curveChartInstance) curveChartInstance.destroy();

            const city = document.getElementById('curveCitySelect').value || "Florianópolis";
            const capObj = capitalsData.find(c => c.city === city);
            if (!capObj || !capObj.typologies[currentTypology]) return;

            const sweep = capObj.typologies[currentTypology].volume_sweep;

            curveChartInstance = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: sweep.map(s => `${{s.vol_l.toLocaleString('pt-BR')}} L`),
                    datasets: [
                        {{
                            label: `${{city}} (VPL TMA 6%)`,
                            data: sweep.map(s => s.vpl_6),
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.15)',
                            fill: true,
                            tension: 0.2,
                            borderWidth: 3,
                            pointRadius: 5
                        }},
                        {{
                            label: 'VPL TMA 10%',
                            data: sweep.map(s => s.vpl_10),
                            borderColor: '#f59e0b',
                            borderDash: [4, 4],
                            borderWidth: 2,
                            fill: false,
                            tension: 0.2
                        }},
                        {{
                            label: 'VPL TMA 14%',
                            data: sweep.map(s => s.vpl_14),
                            borderColor: '#f43f5e',
                            borderDash: [2, 2],
                            borderWidth: 2,
                            fill: false,
                            tension: 0.2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: '#f8fafc', font: {{ size: 11, weight: 'bold' }} }} }}
                    }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(51, 65, 85, 0.4)' }}, ticks: {{ color: '#94a3b8' }} }},
                        y: {{ grid: {{ color: 'rgba(51, 65, 85, 0.4)' }}, ticks: {{ color: '#94a3b8', callback: v => 'R$ ' + v.toLocaleString('pt-BR') }} }}
                    }}
                }}
            }});
        }}

        function updateRadarChart() {{
            const ctx = document.getElementById('radarChart').getContext('2d');
            if (radarChartInstance) radarChartInstance.destroy();

            const city = document.getElementById('radarCitySelect').value || "Florianópolis";
            const capObj = capitalsData.find(c => c.city === city);
            if (!capObj || !capObj.typologies[currentTypology]) return;

            const opt = capObj.typologies[currentTypology].opt_econ;

            const v_pot = Math.min(100, opt.savings_pct * 2.5);
            const v_vpl = Math.max(0, Math.min(100, (opt.vpl_6 + 5000) / 150));
            const v_pb = Math.max(0, Math.min(100, (20 - opt.pb_desc_6) * 5));
            const v_co2 = Math.max(0, Math.min(100, opt.net_co2_kg / 30));
            const v_rel = Math.min(100, opt.reliability);
            const v_tar = Math.min(100, capObj.tarifa_agua_base_r_m3 * 10);

            radarChartInstance = new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: ['Economia Pluvial (%)', 'VPL Financeiro', 'Retorno / Payback', 'CO₂ Evitado', 'Confiabilidade', 'Tarifa Concessionária'],
                    datasets: [{{
                        label: `${{city}} (${{capObj.uf}})`,
                        data: [v_pot, v_vpl, v_pb, v_co2, v_rel, v_tar],
                        backgroundColor: 'rgba(56, 189, 248, 0.25)',
                        borderColor: '#38bdf8',
                        borderWidth: 2.5,
                        pointBackgroundColor: '#38bdf8'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            angleLines: {{ color: 'rgba(51, 65, 85, 0.6)' }},
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            pointLabels: {{ color: '#f8fafc', font: {{ size: 10.5, weight: 'bold' }} }},
                            ticks: {{ display: false, max: 100 }}
                        }}
                    }}
                }}
            }});
        }}

        function updateMatrixChart() {{
            const ctx = document.getElementById('typologyCompChart').getContext('2d');
            if (matrixChartInstance) matrixChartInstance.destroy();

            const city = document.getElementById('matrixCitySelect').value || "Florianópolis";
            const capObj = capitalsData.find(c => c.city === city);
            if (!capObj) return;

            const typKeys = ["UTI", "UTG", "MSG", "MFH", "MFL"];
            const vplVals = typKeys.map(t => capObj.typologies[t]?.opt_econ.vpl_6 || 0);
            const savVals = typKeys.map(t => capObj.typologies[t]?.opt_econ.savings_pct || 0);

            matrixChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: typKeys.map(t => `${{t}} (${{capObj.typologies[t]?.specs.residents}} hab)`),
                    datasets: [
                        {{
                            label: 'VPL Ótimo (R$)',
                            data: vplVals,
                            backgroundColor: '#10b981',
                            yAxisID: 'y'
                        }},
                        {{
                            label: 'Economia Pluvial (%)',
                            data: savVals,
                            type: 'line',
                            borderColor: '#38bdf8',
                            borderWidth: 3,
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            type: 'linear', position: 'left',
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            ticks: {{ color: '#94a3b8', callback: v => 'R$ ' + v.toLocaleString('pt-BR') }}
                        }},
                        y1: {{
                            type: 'linear', position: 'right',
                            grid: {{ display: false }},
                            ticks: {{ color: '#38bdf8', callback: v => v + '%' }}
                        }}
                    }}
                }}
            }});

            updateRegionBoxChart();
        }}

        function updateRegionBoxChart() {{
            const ctx = document.getElementById('regionBoxChart').getContext('2d');
            if (regionBoxChartInstance) regionBoxChartInstance.destroy();

            const regKeys = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"];
            const regAverages = regKeys.map(reg => {{
                const items = capitalsData.filter(c => c.regiao === reg);
                const avg = items.reduce((s, c) => s + (c.typologies[currentTypology]?.opt_econ.vpl_6 || 0), 0) / items.length;
                return avg;
            }});

            regionBoxChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: regKeys,
                    datasets: [{{
                        label: `VPL Médio Regional (Tipologia ${{currentTypology}})`,
                        data: regAverages,
                        backgroundColor: regKeys.map(r => regionColorMap[r]),
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            ticks: {{ color: '#94a3b8', callback: v => 'R$ ' + v.toLocaleString('pt-BR') }}
                        }}
                    }}
                }}
            }});
        }}

        function updateClimateChart() {{
            const ctx = document.getElementById('climateTrajectoryChart').getContext('2d');
            if (climateChartInstance) climateChartInstance.destroy();

            const city = document.getElementById('climateCitySelect').value || "Florianópolis";
            const capObj = capitalsData.find(c => c.city === city);
            if (!capObj || !capObj.typologies[currentTypology]) return;

            const clim = capObj.typologies[currentTypology].climate_projections;
            const labels = ["Histórico (1980-2013)", "Near (2015-2044)", "Middle (2045-2074)", "Far (2075-2100)"];

            const ssp245 = [
                clim["Historical"]?.savings_pct || 15,
                clim["Near_SSP245"]?.savings_pct || 15,
                clim["Middle_SSP245"]?.savings_pct || 15,
                clim["Far_SSP245"]?.savings_pct || 15
            ];

            const ssp585 = [
                clim["Historical"]?.savings_pct || 15,
                clim["Near_SSP585"]?.savings_pct || 15,
                clim["Middle_SSP585"]?.savings_pct || 15,
                clim["Far_SSP585"]?.savings_pct || 15
            ];

            climateChartInstance = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [
                        {{
                            label: 'Cenário SSP2-4.5 (Intermediário)',
                            data: ssp245,
                            borderColor: '#0284c7',
                            backgroundColor: 'rgba(2, 132, 199, 0.1)',
                            fill: true,
                            tension: 0.25,
                            borderWidth: 3,
                            pointRadius: 6
                        }},
                        {{
                            label: 'Cenário SSP5-8.5 (Altas Emissões)',
                            data: ssp585,
                            borderColor: '#f59e0b',
                            backgroundColor: 'rgba(245, 158, 11, 0.1)',
                            fill: true,
                            tension: 0.25,
                            borderWidth: 3,
                            pointRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            ticks: {{ color: '#94a3b8', callback: v => v.toFixed(1) + '%' }}
                        }}
                    }}
                }}
            }});

            updateDeltaVChart();
        }}

        function updateDeltaVChart() {{
            const ctx = document.getElementById('deltaVChart').getContext('2d');
            if (deltaVChartInstance) deltaVChartInstance.destroy();

            const filtered = getFilteredCapitals();
            const deltaData = filtered.map(c => {{
                const clim = c.typologies[currentTypology]?.climate_projections;
                const histSav = clim?.["Historical"]?.savings_pct || 0;
                const farSav = clim?.["Far_SSP585"]?.savings_pct || histSav;
                return {{
                    city: c.city,
                    uf: c.uf,
                    delta: farSav - histSav,
                    regiao: c.regiao
                }};
            }}).sort((a, b) => b.delta - a.delta);

            deltaVChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: deltaData.map(d => `${{d.city}} (${{d.uf}})`),
                    datasets: [{{
                        label: 'Variação de Economia Δ (Far − Histórico) em p.p.',
                        data: deltaData.map(d => d.delta),
                        backgroundColor: deltaData.map(d => d.delta >= 0 ? '#10b981' : '#f43f5e'),
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }} }},
                        y: {{
                            grid: {{ color: 'rgba(51, 65, 85, 0.4)' }},
                            ticks: {{ color: '#94a3b8', callback: v => v.toFixed(1) + ' pp' }}
                        }}
                    }}
                }}
            }});
        }}

        function updateComparator() {{
            const cityA = document.getElementById('compCityA').value || "Florianópolis";
            const cityB = document.getElementById('compCityB').value || "São Paulo";

            const capA = capitalsData.find(c => c.city === cityA);
            const capB = capitalsData.find(c => c.city === cityB);
            if (!capA || !capB) return;

            const optA = capA.typologies[currentTypology]?.opt_econ;
            const optB = capB.typologies[currentTypology]?.opt_econ;

            document.getElementById('compCardA').innerHTML = renderCompCardHTML(capA, optA);
            document.getElementById('compCardB').innerHTML = renderCompCardHTML(capB, optB);

            // Gráfico comparativo
            const ctx = document.getElementById('compBarChart').getContext('2d');
            if (compBarChartInstance) compBarChartInstance.destroy();

            compBarChartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Economia Pluvial (%)', 'Confiabilidade (%)', 'Tarifa Água (R$/m³)', 'TIR (% a.a.)', 'TOPSIS Score (%)'],
                    datasets: [
                        {{
                            label: `${{cityA}} (${{capA.uf}})`,
                            data: [optA.savings_pct, optA.reliability, capA.tarifa_agua_base_r_m3, optA.tir_pct, optA.topsis * 100],
                            backgroundColor: '#38bdf8'
                        }},
                        {{
                            label: `${{cityB}} (${{capB.uf}})`,
                            data: [optB.savings_pct, optB.reliability, capB.tarifa_agua_base_r_m3, optB.tir_pct, optB.topsis * 100],
                            backgroundColor: '#a855f7'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: 'rgba(51, 65, 85, 0.4)' }}, ticks: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});
        }}

        function renderCompCardHTML(cap, opt) {{
            const vpl = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
            const vplClass = vpl >= 0 ? "pos-num" : "neg-num";
            return `
                <h3 style="font-size: 18px; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">${{cap.city}} (${{cap.uf}})</h3>
                <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 16px;">Região ${{cap.regiao}} • Prestador: ${{cap.prestador}}</p>
                <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-card); padding-bottom: 6px;">
                        <span>VPL Ótimo (TMA ${{currentTMA}}%):</span>
                        <span class="${{vplClass}}">R$ ${{vpl.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-card); padding-bottom: 6px;">
                        <span>Volume Ótimo:</span>
                        <span style="font-weight: 700;">${{opt.vol_l.toLocaleString('pt-BR')}} L</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-card); padding-bottom: 6px;">
                        <span>Economia Pluvial:</span>
                        <span style="font-weight: 700; color: #38bdf8;">${{opt.savings_pct.toFixed(1)}}%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-card); padding-bottom: 6px;">
                        <span>Tarifa Concessionária:</span>
                        <span style="font-weight: 700;">R$ ${{cap.tarifa_agua_base_r_m3.toFixed(2)}}/m³</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-card); padding-bottom: 6px;">
                        <span>Payback Descontado:</span>
                        <span>${{opt.pb_desc_6 <= 20 ? opt.pb_desc_6.toFixed(1) + ' anos' : 'Sem Retorno'}}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>CO₂ Evitado na Vida Útil:</span>
                        <span style="font-weight: 700; color: #10b981;">${{opt.net_co2_kg.toFixed(0)}} kg CO₂</span>
                    </div>
                </div>
            `;
        }}

        // Render da Tabela Mestre
        function renderMasterTable() {{
            const tbody = document.getElementById('masterTableBody');
            tbody.innerHTML = "";
            const filtered = getFilteredCapitals();

            document.getElementById('tableCountInfo').textContent = `Exibindo ${{filtered.length}} de 27 capitais`;

            filtered.forEach(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                if (!opt) return;

                const vpl = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);
                const vplClass = vpl >= 0 ? "pos-num" : "neg-num";
                const pbText = opt.pb_desc_6 <= 20 ? `${{opt.pb_desc_6.toFixed(1)}} anos` : `<span style="color: #ef4444;">Sem Retorno</span>`;

                const tr = document.createElement('tr');
                tr.onclick = () => openDetailModal(c.city);
                tr.innerHTML = `
                    <td style="font-weight: 700; color: #38bdf8;">${{c.city}}</td>
                    <td style="font-weight: 600;">${{c.uf}}</td>
                    <td><span class="badge-regiao" style="background: ${{regionColorMap[c.regiao]}};">${{c.regiao}}</span></td>
                    <td style="font-size: 11.5px;">${{c.prestador}}</td>
                    <td>R$ ${{c.tarifa_agua_base_r_m3.toFixed(2)}}</td>
                    <td style="font-weight: 700;">${{opt.vol_l.toLocaleString('pt-BR')}} L</td>
                    <td class="${{vplClass}}">R$ ${{vpl.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</td>
                    <td style="font-weight: 600; color: #38bdf8;">${{opt.savings_pct.toFixed(1)}}%</td>
                    <td>${{opt.consumed_m3.toFixed(1)}} m³</td>
                    <td>R$ ${{opt.capex.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</td>
                    <td>${{pbText}}</td>
                    <td>${{opt.tir_pct ? opt.tir_pct.toFixed(1) + '%' : '--'}}</td>
                    <td style="font-weight: 700; color: #c084fc;">${{(opt.topsis * 100).toFixed(1)}}%</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Dossiê Completo da Capital (Modal)
        function openDetailModal(cityName) {{
            const cap = capitalsData.find(c => c.city === cityName);
            if (!cap) return;

            const opt = cap.typologies[currentTypology]?.opt_econ;
            const vpl = currentTMA === 6 ? opt.vpl_6 : (currentTMA === 10 ? opt.vpl_10 : opt.vpl_14);

            const modal = document.getElementById('detailModal');
            const content = document.getElementById('modalContent');

            content.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                    <div>
                        <h2 style="font-size: 22px; font-weight: 900; color: #38bdf8; display: flex; align-items: center; gap: 8px;">
                            ${{cap.city}} (${{cap.uf}})
                            <span class="badge-regiao" style="background: ${{regionColorMap[cap.regiao]}}; font-size: 11px;">${{cap.regiao}}</span>
                        </h2>
                        <p style="color: var(--text-muted); font-size: 12.5px; margin-top: 4px;">Dossiê Técnico-Econômico e Tarifário Consolidado • Netuno 5</p>
                    </div>
                </div>

                <div style="background: var(--bg-input); border: 1px solid var(--border-card); border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
                    <h4 style="font-size: 12px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px;">Estrutura Tarifária & Saneamento</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; font-size: 12.5px;">
                        <div><strong>Prestador:</strong> ${{cap.prestador}}</div>
                        <div><strong>Agência:</strong> ${{cap.agencia}}</div>
                        <div><strong>Distribuidora:</strong> ${{cap.distribuidora}}</div>
                        <div><strong>Tarifa B1 Energia:</strong> R$ ${{cap.energia_b1_r_kwh.toFixed(4)}}/kWh</div>
                        <div><strong>Tarifa Água Base:</strong> R$ ${{cap.tarifa_agua_base_r_m3.toFixed(2)}}/m³</div>
                        <div><strong>Esgoto:</strong> ${{cap.esgoto_pct}}% sobre água</div>
                    </div>
                    <div style="margin-top: 8px; font-size: 11.5px; color: var(--text-muted); border-top: 1px solid var(--border-card); padding-top: 6px;">
                        <strong>Faixas de Consumo:</strong> ${{cap.faixas_completas}}
                    </div>
                </div>

                <div class="kpi-grid" style="margin-bottom: 20px;">
                    <div class="kpi-card emerald" style="padding: 14px;">
                        <div class="kpi-title">VPL Ótimo Líquido</div>
                        <div class="kpi-value" style="font-size: 20px;">R$ ${{vpl.toLocaleString('pt-BR', {{minimumFractionDigits: 2}})}}</div>
                        <div class="kpi-sub">TMA ${{currentTMA}}% a.a.</div>
                    </div>
                    <div class="kpi-card" style="padding: 14px;">
                        <div class="kpi-title">Volume Ótimo Cisterna</div>
                        <div class="kpi-value" style="font-size: 20px;">${{opt.vol_l.toLocaleString('pt-BR')}} L</div>
                        <div class="kpi-sub">Capacidade Recomendada</div>
                    </div>
                    <div class="kpi-card amber" style="padding: 14px;">
                        <div class="kpi-title">Economia Pluvial</div>
                        <div class="kpi-value" style="font-size: 20px;">${{opt.savings_pct.toFixed(1)}}%</div>
                        <div class="kpi-sub">${{opt.consumed_m3.toFixed(1)}} m³/ano consumidos</div>
                    </div>
                    <div class="kpi-card purple" style="padding: 14px;">
                        <div class="kpi-title">Retorno (Payback Desc.)</div>
                        <div class="kpi-value" style="font-size: 20px;">${{opt.pb_desc_6 <= 20 ? opt.pb_desc_6.toFixed(1) + ' anos' : 'Sem Retorno'}}</div>
                        <div class="kpi-sub">Simples: ${{opt.pb_simple.toFixed(1)}} anos</div>
                    </div>
                </div>

                <div style="background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; padding: 18px;">
                    <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 12px;">Curva Canônica de Otimização — ${{cityName}}</h4>
                    <div style="height: 300px;">
                        <canvas id="modalCurveChart"></canvas>
                    </div>
                </div>
            `;

            modal.classList.add('active');

            setTimeout(() => {{
                const mCtx = document.getElementById('modalCurveChart').getContext('2d');
                const sweep = cap.typologies[currentTypology].volume_sweep;
                new Chart(mCtx, {{
                    type: 'line',
                    data: {{
                        labels: sweep.map(s => `${{s.vol_l.toLocaleString('pt-BR')}} L`),
                        datasets: [{{
                            label: 'VPL (R$)',
                            data: sweep.map(s => s.vpl_6),
                            borderColor: '#0284c7',
                            backgroundColor: 'rgba(2, 132, 199, 0.15)',
                            fill: true,
                            borderWidth: 2.5
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{ ticks: {{ color: '#94a3b8', callback: v => 'R$ ' + v.toLocaleString('pt-BR') }} }}
                        }}
                    }}
                }});
            }}, 50);
        }}

        function closeModal() {{
            document.getElementById('detailModal').classList.remove('active');
        }}

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

            document.getElementById(tabId).classList.add('active');
            const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
            if (btn) btn.classList.add('active');

            if (tabId === 'tab-mapa' && map) {{
                setTimeout(() => map.invalidateSize(), 150);
            }}
        }}

        function toggleTheme() {{
            const isDark = document.documentElement.classList.toggle('dark');
            document.documentElement.classList.toggle('light', !isDark);
            document.getElementById('themeToggleBtn').textContent = isDark ? '🌙 Tema' : '☀️ Tema';
            if (map) {{
                map.remove();
                initMap();
            }}
        }}

        function handleSearch(query) {{
            const q = query.toLowerCase().trim();
            const rows = document.querySelectorAll('#masterTableBody tr');
            rows.forEach(r => {{
                const text = r.textContent.toLowerCase();
                r.style.display = text.includes(q) ? '' : 'none';
            }});
        }}

        function exportDataCSV() {{
            const filtered = getFilteredCapitals();
            let csv = "Capital;UF;Regiao;Prestador;Tarifa_Agua_R_m3;Esgoto_Pct;Vol_Otimo_L;VPL_6pct_BRL;VPL_10pct_BRL;VPL_14pct_BRL;Economia_Pluvial_Pct;Consumo_Pluvial_m3_ano;CAPEX_Total_BRL;Payback_Simples_anos;Payback_Desc_6pct;TIR_Pct_aa;TOPSIS_Score;Net_CO2_kg\\n";
            filtered.forEach(c => {{
                const opt = c.typologies[currentTypology]?.opt_econ;
                if (!opt) return;
                csv += `${{c.city}};${{c.uf}};${{c.regiao}};${{c.prestador}};${{c.tarifa_agua_base_r_m3}};${{c.esgoto_pct}};${{opt.vol_l}};${{opt.vpl_6.toFixed(2)}};${{opt.vpl_10.toFixed(2)}};${{opt.vpl_14.toFixed(2)}};${{opt.savings_pct.toFixed(2)}};${{opt.consumed_m3.toFixed(2)}};${{opt.capex.toFixed(2)}};${{opt.pb_simple.toFixed(2)}};${{opt.pb_desc_6.toFixed(2)}};${{opt.tir_pct.toFixed(2)}};${{opt.topsis.toFixed(4)}};${{opt.net_co2_kg.toFixed(1)}}\\n`;
            }});
            const blob = new Blob(["\\uFEFF" + csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `Netuno5_Capitais_Brasil_${{currentTypology}}.csv`;
            link.click();
        }}

        function openLightbox(src) {{
            document.getElementById('lightboxImg').src = src;
            document.getElementById('imgLightbox').classList.add('active');
        }}

        function closeLightbox() {{
            document.getElementById('imgLightbox').classList.remove('active');
        }}

        function populateCitySelectors() {{
            const cities = capitalsData.map(c => c.city).sort();
            const selectors = ['curveCitySelect', 'radarCitySelect', 'matrixCitySelect', 'climateCitySelect', 'compCityA', 'compCityB'];
            
            selectors.forEach(sId => {{
                const el = document.getElementById(sId);
                if (!el) return;
                el.innerHTML = "";
                cities.forEach(city => {{
                    const opt = document.createElement('option');
                    opt.value = city;
                    opt.textContent = city;
                    if (sId === 'compCityB' && city === 'São Paulo') opt.selected = true;
                    else if (city === 'Florianópolis') opt.selected = true;
                    el.appendChild(opt);
                }});
            }});
        }}

        function populateGallery() {{
            const figures = [
                {{
                    title: "Curvas Canônicas de VPL vs. Volume (UTI - 27 Capitais por Região)",
                    desc: "Grid 2x3 com subplots pelas 5 macrorregiões brasileiras (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) e síntese nacional, exibindo todas as 27 capitais e seus ótimos econômicos.",
                    file: "figuras/grafico_vpl_vs_volume_capitais_UTI.png"
                }},
                {{
                    title: "Ranking Nacional do VPL Ótimo (UTI)",
                    desc: "Comparativo das 27 capitais para casas unifamiliares térreas, com código de cores regional.",
                    file: "figuras/ranking_nacional_vpl_otimo_UTI.png"
                }},
                {{
                    title: "Ranking Nacional do VPL Ótimo (MFH)",
                    desc: "Viabilidade acentuada em edifícios multifamiliares de 64 moradores (escala vertical) em todas as capitais.",
                    file: "figuras/ranking_nacional_vpl_otimo_MFH.png"
                }},
                {{
                    title: "Matriz Multi-Tipologia das 27 Capitais (VPL)",
                    desc: "Grid 5x1 correlacionando o ganho de escala de UTI até MFL (128 habitantes) em todas as 27 capitais.",
                    file: "figuras/matriz_multitipologia_vpl_otimo_27_capitais.png"
                }},
                {{
                    title: "Balanço Ambiental: Matriz Multi-Tipologia CO₂",
                    desc: "Grid 5x1 com o saldo líquido de carbono evitado na vida útil de 20 anos em todas as 27 capitais.",
                    file: "figuras/matriz_multitipologia_co2_otimo_27_capitais.png"
                }},
                {{
                    title: "Curvas de CO₂ vs. Volume da Cisterna (Subplots Regionais)",
                    desc: "Grid 2x3 por macrorregiões detalhando o trade-off entre carbono incorporado e emissões evitadas para todas as 27 capitais.",
                    file: "figuras/figura_curvas_co2_vs_volume_5_tipologias.png"
                }},
                {{
                    title: "Radar Multi-Critério TOPSIS por Macrorregião",
                    desc: "Grid polar 2x3 com avaliação pareada das 6 dimensões de projeto (água, VPL, payback, CO₂, confiabilidade, tarifa) para todas as 27 capitais.",
                    file: "figuras/figura_radar_multicriterio_capitais.png"
                }},
                {{
                    title: "Trajetórias Climáticas CMIP6 (SSP2-4.5 vs. SSP5-8.5)",
                    desc: "Grid 2x5 abrangendo a evolução temporal do potencial pluvial nas 27 capitais de 1980 a 2100 por macrorregião.",
                    file: "figuras/figura_trajetorias_climaticas_capitais_cmip6.png"
                }},
                {{
                    title: "Sensibilidade à Taxa TMA por Macrorregião",
                    desc: "Grid 2x3 com barras agrupadas para TMA de 6%, 10% e 14% a.a. em todas as capitais brasileiras.",
                    file: "figuras/figura_sensibilidade_tma_capitais.png"
                }}
            ];

            const galleryEl = document.getElementById('figuresGallery');
            galleryEl.innerHTML = "";

            figures.forEach(f => {{
                galleryEl.innerHTML += `
                    <div class="gallery-item">
                        <div class="gallery-img-wrap" onclick="openLightbox('${{f.file}}')">
                            <img src="${{f.file}}" alt="${{f.title}}" onerror="this.src='data:image/svg+xml,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'300\\' height=\\'200\\'><rect width=\\'100%\\' height=\\'100%\\' fill=\\'%231e293b\\'/><text x=\\'50%\\' y=\\'50%\\' fill=\\'%2394a3b8\\' text-anchor=\\'middle\\'>Figura Científica</text></svg>'">
                        </div>
                        <div class="gallery-info">
                            <h4 class="gallery-title">${{f.title}}</h4>
                            <p class="gallery-desc">${{f.desc}}</p>
                            <button class="btn-action" onclick="openLightbox('${{f.file}}')" style="width: 100%; justify-content: center;">🔍 Expandir Figura (Alta Resolução)</button>
                        </div>
                    </div>
                `;
            }});
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            populateCitySelectors();
            populateGallery();
            initMap();
            refreshAll();
        }});
    </script>
</body>
</html>
"""
    out_html = os.path.join(OUTPUT_DIR, "dashboard_capitais_modo_global.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"✓ Dashboard HTML Interativo salvo em: {out_html}")
    return out_html


def export_csv_and_summary_reports(capitals_data, grouped_hist):
    """Exporta CSVs consolidados de resumo, MCDM comparativo e varredura completa."""
    rows_summary = []
    rows_mcdm = []

    for c in capitals_data:
        for bcode, tdata in c["typologies"].items():
            opt = tdata["opt_econ"]
            top = tdata.get("opt_topsis", {})
            vik = tdata.get("opt_vikor", {})
            sma = tdata.get("opt_smaa", {})

            vol_econ = opt["vol_l"]
            vol_vikor = vik.get("vol_l", vol_econ)
            vol_smaa = sma.get("vol_l", vol_econ)

            agreement = "CONVERGENT" if (vol_vikor == vol_econ == vol_smaa) else "DIVERGENT"

            # Resumo Completo Enriquecido
            rows_summary.append({
                "city": c["city"],
                "uf": c["uf"],
                "regiao": c["regiao"],
                "building_code": bcode,
                "residents": tdata["specs"]["residents"],
                "roof_area_m2": tdata["specs"]["roof"],
                "prestador": c["prestador"],
                "tarifa_agua_base_r_m3": c["tarifa_agua_base_r_m3"],
                "esgoto_pct": c["esgoto_pct"],
                "opt_vol_econ_l": vol_econ,
                "opt_vpl_6pct_brl": opt["vpl_6"],
                "opt_vpl_10pct_brl": opt["vpl_10"],
                "opt_vpl_14pct_brl": opt["vpl_14"],
                "potential_savings_pct": opt["savings_pct"],
                "annual_pluvial_consumed_m3": opt["consumed_m3"],
                "annual_water_savings_brl": opt["water_savings_brl"],
                "capex_total_brl": opt["capex"],
                "annual_opex_brl": opt["opex"],
                "payback_simple_years": opt["pb_simple"],
                "payback_discounted_6pct": opt["pb_desc_6"],
                "tir_annual_pct": opt["tir_pct"],
                "lcow_brl_m3": opt["lcow"],
                "topsis_score": opt["topsis"],
                "lifetime_net_co2_saved_kg": opt["net_co2_kg"],
                "opt_vol_topsis_l": top.get("vol_l", vol_econ),
                "opt_vol_vikor_l": vol_vikor,
                "vikor_q_score": vik.get("q_score", 0.0),
                "vikor_s_score": vik.get("s_score", 0.0),
                "vikor_r_score": vik.get("r_score", 0.0),
                "opt_vol_smaa_l": vol_smaa,
                "smaa_first_rank_prob_pct": sma.get("first_rank_prob", 0.0),
                "smaa_w_tech": sma.get("w_tech", 0.333),
                "smaa_w_econ": sma.get("w_econ", 0.333),
                "smaa_w_env": sma.get("w_env", 0.334),
                "smaa_confidence": sma.get("confidence", 0.0),
                "mcdm_agreement": agreement
            })

            # Tabela Comparativa de Decisão MCDM
            rows_mcdm.append({
                "city": c["city"],
                "uf": c["uf"],
                "regiao": c["regiao"],
                "building_code": bcode,
                "residents": tdata["specs"]["residents"],
                "roof_area_m2": tdata["specs"]["roof"],
                "tarifa_agua_base_r_m3": c["tarifa_agua_base_r_m3"],
                "esgoto_pct": c["esgoto_pct"],
                "vol_econ_opt_l": vol_econ,
                "vpl_econ_brl": opt["vpl_6"],
                "pb_desc_econ_yr": opt["pb_desc_6"],
                "savings_econ_pct": opt["savings_pct"],
                "vol_topsis_opt_l": top.get("vol_l", vol_econ),
                "topsis_score": top.get("score", opt["topsis"]),
                "vol_vikor_opt_l": vol_vikor,
                "vikor_vpl_brl": vik.get("vpl_6", opt["vpl_6"]),
                "vikor_pb_desc_yr": vik.get("pb_desc_6", opt["pb_desc_6"]),
                "vikor_savings_pct": vik.get("savings_pct", opt["savings_pct"]),
                "vikor_q_score": vik.get("q_score", 0.0),
                "vikor_s_score": vik.get("s_score", 0.0),
                "vikor_r_score": vik.get("r_score", 0.0),
                "vol_smaa_opt_l": vol_smaa,
                "smaa_vpl_brl": sma.get("vpl_6", opt["vpl_6"]),
                "smaa_pb_desc_yr": sma.get("pb_desc_6", opt["pb_desc_6"]),
                "smaa_savings_pct": sma.get("savings_pct", opt["savings_pct"]),
                "smaa_first_rank_prob_pct": sma.get("first_rank_prob", 0.0),
                "smaa_w_tech": sma.get("w_tech", 0.333),
                "smaa_w_econ": sma.get("w_econ", 0.333),
                "smaa_w_env": sma.get("w_env", 0.334),
                "smaa_confidence": sma.get("confidence", 0.0),
                "delta_vol_vikor_vs_econ_l": vol_vikor - vol_econ,
                "delta_vol_smaa_vs_econ_l": vol_smaa - vol_econ,
                "decision_agreement": agreement
            })

    df_summary = pd.DataFrame(rows_summary)
    out_csv_summary = os.path.join(OUTPUT_DIR, "capitais_vpl_otimo_resumo.csv")
    df_summary.to_csv(out_csv_summary, index=False, sep=";", encoding="utf-8-sig")

    df_mcdm = pd.DataFrame(rows_mcdm)
    out_csv_mcdm = os.path.join(OUTPUT_DIR, "capitais_mcdm_vikor_smaa_resumo.csv")
    df_mcdm.to_csv(out_csv_mcdm, index=False, sep=";", encoding="utf-8-sig")

    out_csv_all = os.path.join(OUTPUT_DIR, "capitais_varredura_completa.csv")
    grouped_hist.to_csv(out_csv_all, index=False, sep=";", encoding="utf-8-sig")

    print(f"✓ CSV de Resumo salvo: {out_csv_summary}")
    print(f"✓ CSV MCDM (VIKOR & SMAA) salvo: {out_csv_mcdm}")
    print(f"✓ CSV de Varredura Completa salvo: {out_csv_all}")


def main():
    print("=" * 90)
    print("NETUNO 5 -- OBSERVATÓRIO E GERADOR DO DASHBOARD DAS 27 CAPITAIS BRASILEIRAS")
    print("=" * 90)

    # 1. Carrega dados de geolocalização e catálogo tarifário
    geo_dict, cat_dict = load_geo_and_catalogue()

    # 2. Carrega dados das 27 capitais do banco Parquet
    df_capitais = load_and_process_capitals_data()

    # 3. Executa agregações multi-dimensionais
    grouped_hist, capitals_data = aggregate_capitals_data(df_capitais, geo_dict, cat_dict)

    # 4. Gera figuras científicas em alta resolução
    generate_scientific_figures(grouped_hist, capitals_data)

    # 5. Constrói Dashboard HTML Interativo Completo
    generate_advanced_html_dashboard(capitals_data)

    # 6. Exporta arquivos CSV
    export_csv_and_summary_reports(capitals_data, grouped_hist)

    print("\n" + "=" * 90)
    print("🎉 DASHBOARD E FIGURAS DAS CAPITAIS GERADOS COM SUCESSO TOTAL!")
    print(f"📁 Dashboard: {os.path.join(OUTPUT_DIR, 'dashboard_capitais_modo_global.html')}")
    print(f"📁 Figuras: {FIGURAS_DIR}")
    print("=" * 90)


if __name__ == "__main__":
    main()
