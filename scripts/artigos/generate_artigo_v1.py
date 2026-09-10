"""
====================================================================================================
NETUNO 5 — SUÍTE DE ANÁLISE E GERAÇÃO DE FIGURAS PARA O ARTIGO V1 (VERSÃO APRIMORADA V2)
ESTUDO DAS 5 TIPOLOGIAS RESIDENCIAIS SOB CENÁRIOS CLIMÁTICOS CMIP6 (652 MUNICÍPIOS BRASILEIROS)
====================================================================================================
Novidades e Aprimoramentos Desta Versão:
 1. Limiar Técnico Oficial Netuno (Delta <= 2.5 %/m³): Eq. 4.8 do manual para volume ideal.
 2. Bins e Colorações Discretas (BoundaryNorm): contraste nítido e intervalos claros em todos os mapas.
 3. Correção Causal e Agrupamento no Random Forest (Fig 1.1):
    - Economia Pluvial (%): Apenas variáveis físicas/hidrológicas (ZERO tarifas).
    - VPL Financeiro (R$): Variáveis de escala, área, tarifas combinadas de água/esgoto e cisternas.
    - CO2 Líquido Evitado: Carbono incorporado, bombeamento e captação.
 4. Cenário de Referência (100% Concessionária — Sem Netuno) adicionado nas Figs 1.5 e 1.6 (LCC 20 anos).
 5. Inclusão de todas as 5 tipologias (UTI, UTG, MSG, MFH, MFL) nos boxplots da Fig 3.1.
 6. Documentação Matemática do Índice de Excelência e Atratividade Pluvial (0 a 100).
====================================================================================================
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import BoundaryNorm, ListedColormap
import seaborn as sns
import geopandas as gpd
import pyarrow.parquet as pq
from sklearn.ensemble import RandomForestRegressor

# Configuração global de estilo visual de alta qualidade para publicação científica
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 10.5,
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'axes.labelsize': 11.5,
    'axes.titlesize': 12.5,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9.5,
    'figure.titlesize': 13.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz")
PARQUET_PATH = os.path.join(STUDY_DIR, "estudo_vaz_consolidado.parquet")
JSON_GEO_PATH = os.path.join(BASE_DIR, "tarifas", "validated_cidades_50k.json")
BRAZIL_SHP_PATH = os.path.join(BASE_DIR, "data", "brazilSHP", "BR_UF_2022.shp")
GEOJSON_STATES_PATH = os.path.join(STUDY_DIR, "brazil_states.geojson")

# Diretórios de Saída do Artigo V1
ARTIGO_DIR = os.path.join(BASE_DIR, "ArtigoV1")
CAP1_DIR = os.path.join(ARTIGO_DIR, "Cap1_Panorama_Geral_Tipologias")
CAP2_DIR = os.path.join(ARTIGO_DIR, "Cap2_Aumento_Reservatorios_Futuro")
CAP3_DIR = os.path.join(ARTIGO_DIR, "Cap3_Comparacao_Otimo_Ambiental_Economico_Tecnico")
CAP4_DIR = os.path.join(ARTIGO_DIR, "Cap4_Piores_Resultados_Brasil")
CAP5_DIR = os.path.join(ARTIGO_DIR, "Cap5_Melhores_Resultados_Brasil")
REPORT_PATH = os.path.join(ARTIGO_DIR, "Relatorio_ArtigoV1_Consolidado.md")

for d in [ARTIGO_DIR, CAP1_DIR, CAP2_DIR, CAP3_DIR, CAP4_DIR, CAP5_DIR]:
    os.makedirs(d, exist_ok=True)

# Padronização de Tipologias e Horizontes
TYPOLOGY_ORDER = ["UTI (4 hab)", "UTG (8 hab)", "MSG (16 hab)", "MFH (64 hab)", "MFL (128 hab)"]
TYPOLOGY_CODE_MAP = {
    "UTI": "UTI (4 hab)",
    "UTG": "UTG (8 hab)",
    "MSG": "MSG (16 hab)",
    "MFH": "MFH (64 hab)",
    "MFL": "MFL (128 hab)"
}
HORIZON_ORDER = ["Historical", "Near", "Middle", "Far"]
HORIZON_MAP = {
    "Histórico": "Historical",
    "Historico": "Historical",
    "Near": "Near",
    "Middle": "Middle",
    "Far": "Far"
}
REG_ORDER = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]


def assign_region(lat, lon):
    if np.isnan(lat) or np.isnan(lon):
        return "Centro-Oeste"
    if lat > -16.0 and lon < -44.0 and lat > -10.0 and lon < -47.0:
        return "Norte"
    if lat >= -2.0 or (lat > -13.0 and lon < -46.0 and lon < -52.0):
        return "Norte"
    if lat > -18.5 and lon >= -46.0:
        if lat > -5.0:
            return "Nordeste"
        elif lat > -16.0 and lon >= -45.0:
            return "Nordeste"
    if lat <= -22.0 and lon <= -48.0:
        return "Sul"
    if lat <= -19.5 and lon > -53.0:
        return "Sudeste"
    if lat > -24.0 and lat < -13.0 and lon < -46.0 and lon > -61.0:
        return "Centro-Oeste"
    if lat < -22.0:
        return "Sul"
    if lon >= -44.0 and lat < -14.0:
        return "Sudeste"
    if lat > -18.0 and lon >= -48.0:
        return "Nordeste"
    return "Centro-Oeste"


def load_city_coordinates():
    if not os.path.exists(JSON_GEO_PATH):
        print(f"[ERRO] JSON de coordenadas não encontrado: {JSON_GEO_PATH}")
        return pd.DataFrame()
    with open(JSON_GEO_PATH, encoding='utf-8') as f:
        city_dict = json.load(f)
    records = []
    for city_name, coords in city_dict.items():
        lat = coords.get('target', {}).get('lat', coords.get('nearest', {}).get('lat', np.nan))
        lon = coords.get('target', {}).get('lon', coords.get('nearest', {}).get('lon', np.nan))
        reg = assign_region(lat, lon)
        records.append({'city_clean': city_name, 'lat': lat, 'lon': lon, 'region_geo': reg})
    df_geo = pd.DataFrame(records)
    print(f" [*] Coordenadas carregadas para {len(df_geo):,} municípios.")
    return df_geo


def load_brazil_states():
    candidates = [
        BRAZIL_SHP_PATH,
        os.path.join(BASE_DIR, "data", "brazilSHP", "BR_UF_2022.SHP"),
        GEOJSON_STATES_PATH
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                gdf_states = gpd.read_file(p)
                gdf_states['geometry'] = gdf_states['geometry'].simplify(0.02, preserve_topology=True)
                print(f" [*] Limites estaduais (27 UFs) carregados com sucesso de: {p}", flush=True)
                return gdf_states
            except Exception as e:
                print(f"[AVISO] Falha ao carregar mapa de estados ({p}): {e}", flush=True)
    return None


def plot_brazil_basemap(ax, states_gdf):
    if states_gdf is not None:
        states_gdf.boundary.plot(ax=ax, color='#555555', linewidth=0.55, zorder=1)
        ax.set_xlim(-74, -34)
        ax.set_ylim(-34, 6)
    else:
        ax.set_facecolor('#fafafa')
    ax.set_xlabel("Longitude (°W)", fontsize=9.5)
    ax.set_ylabel("Latitude (°S)", fontsize=9.5)
    ax.tick_params(labelsize=8.5)


def plot_binned_scatter(ax, lon, lat, values, bins, cmap_name, label, fig, cbar_fmt="{:g}", s=58, zorder=3, bin_labels=None):
    """
    Desenha um scatterplot cartográfico com bins discretos e colorbar segmentada de alto contraste.
    """
    n_bins = len(bins) - 1
    cmap_base = plt.get_cmap(cmap_name, n_bins)
    norm = BoundaryNorm(bins, ncolors=cmap_base.N, clip=True)
    
    sc = ax.scatter(lon, lat, c=values, cmap=cmap_base, norm=norm, s=s, alpha=0.92, edgecolors='black', linewidths=0.25, zorder=zorder)
    cbar = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, ticks=bins)
    cbar.set_label(label, fontweight='bold', fontsize=10)
    
    if bin_labels is not None and len(bin_labels) == len(bins):
        cbar.ax.set_yticklabels(bin_labels)
    else:
        cbar.ax.set_yticklabels([cbar_fmt.format(b) for b in bins])
    return sc


def auto_binned_scatter(ax, x, y, values, cmap_name='viridis', s=58, **kwargs):
    """Discretiza automaticamente a variável de cor em sete classes por quantis."""
    vals = pd.to_numeric(pd.Series(values), errors='coerce').to_numpy(dtype=float)
    finite = vals[np.isfinite(vals)]
    bins = np.unique(np.nanquantile(finite, np.linspace(0, 1, 8))) if finite.size else np.linspace(0, 1, 8)
    if len(bins) < 3:
        lo, hi = (float(np.nanmin(finite)), float(np.nanmax(finite))) if finite.size else (0.0, 1.0)
        bins = np.linspace(lo, hi if hi > lo else lo + 1.0, 4)
    cmap = plt.get_cmap(cmap_name, len(bins) - 1)
    norm = BoundaryNorm(bins, cmap.N, clip=True)
    return ax.scatter(x, y, c=vals, cmap=cmap, norm=norm, s=s, **kwargs)


def process_parquet_and_extract_data(parquet_path, df_geo, target_sample_size=350000, technical_delta_threshold=2.5):
    """
    Lê o arquivo Parquet e realiza:
    1. Extração de amostra estratificada robusta com variáveis físicas e tarifárias compostas.
    2. Cálculo vetorizado dos 4 ótimos:
       - Ótimo Técnico (Volume Ideal Netuno com Delta <= 2.5 %/m³)
       - Ótimo Econômico (Max VPL R$)
       - Ótimo Ambiental (Max CO2 líquido evitado kg)
       - Compromisso TOPSIS (Multicritério)
    3. Cálculo do Cenário de Referência (100% Concessionária — Sem Sistema Pluvial)
    """
    f = pq.ParquetFile(parquet_path)
    total_rows = f.metadata.num_rows
    num_rg = f.num_row_groups
    print(f" [*] Base de dados Parquet: {total_rows:,} linhas em {num_rg} row groups.")

    needed_cols = [
        'city', 'model', 'scenario', 'horizon', 'building_code', 'residents',
        'roof_area_m2', 'demand_per_capita_l', 'rainwater_share_pct',
        'discard_mm', 'discard_mode', 'discard_days', 'lower_tank_vol_l', 'upper_tank_vol_l',
        'annual_pluvial_consumed_m3', 'avg_pluvial_consumed_l_day',
        'potential_savings_pct', 'annual_spill_m3', 'fully_met_pct', 'partially_met_pct', 'not_met_pct',
        'capex_total_brl', 'annual_opex_brl', 'annual_water_savings_brl',
        'vpl_brl', 'tir_annual_pct', 'payback_years',
        'embodied_co2_kg', 'annual_avoided_co2_kg', 'lifetime_net_co2_saved_kg',
        'pump_energy_kwh_yr', 'topsis_score', 'topsis_rank', 'is_topsis_best',
        'tarifa_eletricidade_b1_r_kwh', 'tarifa_agua_base_r_m3', 'esgoto_pct_sobre_agua',
        'saneamento_prestador', 'uf', 'regiao'
    ]
    safe_cols = [c for c in needed_cols if c in f.schema.names]

    samples_per_rg = max(5000, target_sample_size // num_rg)
    dfs_sample = []
    optima_records = []

    print(f" [*] Processando row groups do Parquet e computando ótimos com Limiar Técnico Delta <= {technical_delta_threshold:.1f} %/m³...")
    for i in range(num_rg):
        t_rg = f.read_row_group(i, columns=safe_cols)
        df_rg = t_rg.to_pandas()

        if len(df_rg) == 0:
            continue

        # Cálculo de CO2 se ausente
        if 'lifetime_net_co2_saved_kg' not in df_rg.columns:
            if 'annual_pluvial_consumed_m3' in df_rg.columns:
                ann_pluv = df_rg['annual_pluvial_consumed_m3']
            elif 'avg_pluvial_consumed_l_day' in df_rg.columns:
                ann_pluv = df_rg['avg_pluvial_consumed_l_day'] * 0.365
            else:
                ann_pluv = df_rg.get('demand_per_capita_l', 150.0) * df_rg.get('residents', 4) * (df_rg.get('potential_savings_pct', 15.0) / 100.0) * 0.365
            tank_m3 = df_rg['lower_tank_vol_l'] / 1000.0
            emb = (tank_m3 * 44.0) + 80.0
            ann_avoid = (ann_pluv * 0.35) - (ann_pluv * 0.45 * 0.08)
            df_rg['lifetime_net_co2_saved_kg'] = (ann_avoid * 20.0) - emb
            df_rg['embodied_co2_kg'] = emb
            df_rg['annual_avoided_co2_kg'] = ann_avoid

        # Amostragem representativa
        if len(df_rg) > samples_per_rg:
            df_sampled = df_rg.sample(n=samples_per_rg, random_state=42 + i)
        else:
            df_sampled = df_rg
        dfs_sample.append(df_sampled)

        # Cálculo exato de ótimos por varredura de simulação
        sim_sweep_cols = ['city', 'model', 'scenario', 'horizon', 'building_code', 'demand_per_capita_l', 'rainwater_share_pct', 'discard_mm']
        
        if len(df_rg) > 100:
            # Ordenação crescente de volume para cálculo incremental do ganho marginal
            df_rg = df_rg.sort_values(sim_sweep_cols + ['lower_tank_vol_l'])

            # Cálculo vetorizado do ganho marginal Delta = d(Potencial %) / d(Volume m³)
            df_rg['d_vol_m3'] = df_rg.groupby(sim_sweep_cols, observed=True)['lower_tank_vol_l'].diff() / 1000.0
            df_rg['d_sav_pct'] = df_rg.groupby(sim_sweep_cols, observed=True)['potential_savings_pct'].diff()
            df_rg['delta_marginal'] = df_rg['d_sav_pct'] / df_rg['d_vol_m3'].replace(0, np.nan)

            # 1. Ótimo Técnico (Volume Ideal Clássico Netuno: menor volume onde delta_marginal <= threshold)
            met_thresh = df_rg[df_rg['delta_marginal'] <= technical_delta_threshold]
            idx_tech_first = met_thresh.groupby(sim_sweep_cols, observed=True)['lower_tank_vol_l'].idxmin()
            idx_tech_max = df_rg.groupby(sim_sweep_cols, observed=True)['lower_tank_vol_l'].idxmax()
            idx_tech = idx_tech_max.copy()
            idx_tech.loc[idx_tech_first.index] = idx_tech_first

            # 2. Ótimo Econômico (Max VPL)
            idx_econ = df_rg.groupby(sim_sweep_cols, observed=True)['vpl_brl'].idxmax()

            # 3. Ótimo Ambiental (Max CO2 Líquido Evitado)
            idx_env = df_rg.groupby(sim_sweep_cols, observed=True)['lifetime_net_co2_saved_kg'].idxmax()

            # 4. TOPSIS Best
            df_top_best = df_rg[df_rg['is_topsis_best'] == True]
            if not df_top_best.empty:
                idx_top = df_top_best.groupby(sim_sweep_cols, observed=True)['topsis_score'].idxmax()
            else:
                idx_top = idx_econ

            # Extração dos sub-dataframes
            sub_econ = df_rg.loc[idx_econ, sim_sweep_cols + ['lower_tank_vol_l', 'vpl_brl', 'potential_savings_pct', 'lifetime_net_co2_saved_kg', 'payback_years', 'tarifa_agua_base_r_m3', 'esgoto_pct_sobre_agua', 'tarifa_eletricidade_b1_r_kwh', 'uf', 'regiao']].rename(columns={
                'lower_tank_vol_l': 'vol_econ_l', 'vpl_brl': 'vpl_opt_econ', 'potential_savings_pct': 'sav_opt_econ', 'lifetime_net_co2_saved_kg': 'co2_opt_econ'
            })
            sub_env = df_rg.loc[idx_env, sim_sweep_cols + ['lower_tank_vol_l', 'vpl_brl', 'potential_savings_pct', 'lifetime_net_co2_saved_kg']].rename(columns={
                'lower_tank_vol_l': 'vol_env_l', 'vpl_brl': 'vpl_opt_env', 'potential_savings_pct': 'sav_opt_env', 'lifetime_net_co2_saved_kg': 'co2_opt_env'
            })
            sub_tech = df_rg.loc[idx_tech, sim_sweep_cols + ['lower_tank_vol_l', 'vpl_brl', 'potential_savings_pct', 'lifetime_net_co2_saved_kg', 'delta_marginal']].rename(columns={
                'lower_tank_vol_l': 'vol_tech_l', 'vpl_brl': 'vpl_opt_tech', 'potential_savings_pct': 'sav_opt_tech', 'lifetime_net_co2_saved_kg': 'co2_opt_tech'
            })
            sub_top = df_rg.loc[idx_top, sim_sweep_cols + ['lower_tank_vol_l', 'vpl_brl', 'potential_savings_pct', 'lifetime_net_co2_saved_kg']].rename(columns={
                'lower_tank_vol_l': 'vol_topsis_l', 'vpl_brl': 'vpl_opt_top', 'potential_savings_pct': 'sav_opt_top', 'lifetime_net_co2_saved_kg': 'co2_opt_top'
            })

            merged_opt = sub_econ.merge(sub_env, on=sim_sweep_cols).merge(sub_tech, on=sim_sweep_cols).merge(sub_top, on=sim_sweep_cols)
            optima_records.append(merged_opt.sample(min(len(merged_opt), 15000), random_state=42 + i))

    df_sample = pd.concat(dfs_sample, ignore_index=True)
    df_optima = pd.concat(optima_records, ignore_index=True)

    def standardize_df(df_target):
        df_target["horizon"] = df_target["horizon"].fillna("Historical").map(lambda x: HORIZON_MAP.get(x, x))
        df_target["scenario"] = df_target["scenario"].fillna("Historical").replace({"Histórico": "Historical", "Historico": "Historical"})
        df_target["model"] = df_target["model"].fillna("Observed")
        df_target["city_clean"] = df_target["city"].astype(str).str.split('_Hist').str[0].str.split('_Near').str[0].str.split('_Middle').str[0].str.split('_Far').str[0]
        
        # Merge de coordenadas
        df_res = df_target.merge(df_geo, on="city_clean", how="left")
        if "regiao" in df_res.columns:
            df_res["region"] = df_res["regiao"].fillna(df_res["region_geo"]).fillna("Centro-Oeste")
        else:
            df_res["region"] = df_res["region_geo"].fillna("Centro-Oeste")
            
        df_res["building_label"] = df_res["building_code"].map(lambda x: TYPOLOGY_CODE_MAP.get(x, x))
        df_res["building_label"] = pd.Categorical(df_res["building_label"], categories=TYPOLOGY_ORDER, ordered=True)
        df_res["horizon"] = pd.Categorical(df_res["horizon"], categories=HORIZON_ORDER, ordered=True)

        # Variáveis Físicas e Econômicas Consequentes Agrupadas
        if "residents" in df_res.columns and "demand_per_capita_l" in df_res.columns:
            df_res["demanda_pluvial_diaria_l"] = df_res["residents"] * df_res["demand_per_capita_l"] * (df_res["rainwater_share_pct"] / 100.0)
            df_res["demanda_potavel_diaria_l"] = df_res["residents"] * df_res["demand_per_capita_l"] * (1.0 - df_res["rainwater_share_pct"] / 100.0)
            df_res["descarte_inicial_total_l"] = df_res["roof_area_m2"] * df_res["discard_mm"]
            df_res["area_efetiva_telhado_m2"] = df_res["roof_area_m2"] * 0.85
            df_res["tarifa_combinada_agua_esgoto_r_m3"] = df_res["tarifa_agua_base_r_m3"] * (1.0 + df_res["esgoto_pct_sobre_agua"] / 100.0)

            # Demanda total e Fatura Integral da Concessionária (Cenário Referência 100% Concessionária)
            df_res["total_annual_demand_m3"] = df_res["residents"] * df_res["demand_per_capita_l"] * 365.0 / 1000.0
            df_res["annual_baseline_utility_bill_brl"] = df_res["total_annual_demand_m3"] * df_res["tarifa_combinada_agua_esgoto_r_m3"]
            
            # Custo de Ciclo de Vida a 20 Anos (Fator de Valor Presente a 8.5% a.a. ~ 11.47)
            pv_factor = 11.4699
            df_res["lcc_baseline_kbrl"] = (df_res["annual_baseline_utility_bill_brl"] * pv_factor) / 1e3
            df_res["lcc_residual_water_kbrl"] = ((df_res["annual_baseline_utility_bill_brl"] - df_res["annual_water_savings_brl"]) * pv_factor) / 1e3
            df_res["lcc_opex_kbrl"] = (df_res["annual_opex_brl"] * pv_factor) / 1e3
            df_res["lcc_capex_kbrl"] = df_res["capex_total_brl"] / 1e3
            df_res["lcc_netuno_total_kbrl"] = df_res["lcc_residual_water_kbrl"] + df_res["lcc_opex_kbrl"] + df_res["lcc_capex_kbrl"]

        return df_res

    df_sample = standardize_df(df_sample)
    df_optima = standardize_df(df_optima)

    print(f" [OK] Amostra consolidada: {len(df_sample):,} linhas. Dataset de ótimos: {len(df_optima):,} simulações.")
    return df_sample, df_optima, total_rows


def format_table(t_lines):
    if not t_lines or len(t_lines) < 2:
        return t_lines
    out = []
    for line in t_lines:
        cells = [c.strip() for c in line.strip().split('|')]
        if cells and cells[0] == '': cells = cells[1:]
        if cells and cells[-1] == '': cells = cells[:-1]
        out.append('| ' + ' | '.join(cells) + ' |')
    return out


# ==================================================================================================
# EXECUÇÃO PRINCIPAL
# ==================================================================================================
def main():
    t_start = time.time()
    print("=" * 100)
    print("NETUNO 5 — GERADOR DE FIGURAS COM BINS DISCRETOS E LIMIAR TÉCNICO OFICIAL (25 FIGURAS)")
    print("=" * 100)

    df_geo = load_city_coordinates()
    states_gdf = load_brazil_states()
    df_sample, df_optima, total_rows = process_parquet_and_extract_data(PARQUET_PATH, df_geo, technical_delta_threshold=2.5)

    df_best = df_sample[df_sample["is_topsis_best"] == True].copy()
    if df_best.empty:
        df_best = df_sample.copy()

    palette_typ = sns.color_palette("Set2", n_colors=len(TYPOLOGY_ORDER))

    # Cidades estratégicas de destaque
    capitals = {
        'São Paulo': (-46.63, -23.55),
        'Brasília': (-47.92, -15.78),
        'Manaus': (-60.02, -3.11),
        'Recife': (-34.88, -8.05),
        'Porto Alegre': (-51.23, -30.03),
        'Curitiba': (-49.27, -25.42),
        'Belém': (-48.48, -1.45)
    }

    # ==============================================================================================
    # CAPÍTULO 1: PANORAMA GERAL E DESEMPENHO BASE DAS TIPOLOGIAS (9 FIGURAS)
    # ==============================================================================================
    print("\n" + "="*80)
    print("GERANDO CAPÍTULO 1: PANORAMA GERAL E DESEMPENHO BASE DAS TIPOLOGIAS (9 FIGURAS)")
    print("="*80)

    # Fig 1.1: Feature Importance RF Causal e Agrupado
    print("[+] 1.1 Importância Global de Parâmetros de Projeto e Variáveis Consequentes (RF Gini %)...")
    
    # 1. Painel A: Economia Pluvial (%) — Variáveis estritamente físicas e hidrológicas (ZERO tarifas)
    feat_sav = ['demanda_potavel_diaria_l', 'lower_tank_vol_l', 'demanda_pluvial_diaria_l', 'area_efetiva_telhado_m2', 'descarte_inicial_total_l']
    lbl_sav = ['Demanda Potável (L/dia)', 'Volume da Cisterna (L)', 'Demanda Pluvial (L/dia)', 'Área Efetiva Telhado (m²)', 'Descarte Inicial (L)']
    rf_sav = RandomForestRegressor(n_estimators=30, max_depth=8, random_state=42, n_jobs=-1).fit(df_sample[feat_sav].fillna(0), df_sample['potential_savings_pct'].fillna(0))
    imp_sav = rf_sav.feature_importances_ * 100

    # 2. Painel B: VPL Financeiro (R$) — Motores reais do fluxo de caixa descontado (Volume Pluvial, Tarifa de Água+Esgoto e CAPEX)
    df_sample['volume_pluvial_anual_m3'] = df_sample['annual_water_savings_brl'] / df_sample['tarifa_combinada_agua_esgoto_r_m3'].replace(0, np.nan)
    feat_vpl = ['volume_pluvial_anual_m3', 'tarifa_combinada_agua_esgoto_r_m3', 'demanda_pluvial_diaria_l', 'lower_tank_vol_l', 'area_efetiva_telhado_m2', 'descarte_inicial_total_l']
    lbl_vpl = ['Volume Pluvial Captado (m³/ano)', 'Tarifa Água+Esgoto (R$/m³)', 'Demanda Pluvial (L/dia)', 'Volume Cisterna / CAPEX (L)', 'Área Efetiva Telhado (m²)', 'Descarte Inicial (L)']
    rf_vpl = RandomForestRegressor(n_estimators=30, max_depth=8, random_state=42, n_jobs=-1).fit(df_sample[feat_vpl].fillna(0), df_sample['vpl_brl'].fillna(0))
    imp_vpl = rf_vpl.feature_importances_ * 100

    # 3. Painel C: CO2 Líquido Evitado (kg) — Pegada de materiais, captação e bombeamento
    feat_co2 = ['lower_tank_vol_l', 'area_efetiva_telhado_m2', 'demanda_pluvial_diaria_l', 'pump_energy_kwh_yr', 'descarte_inicial_total_l']
    lbl_co2 = ['Volume Cisterna (Carbono Incorp.)', 'Área Efetiva Telhado (m²)', 'Demanda Pluvial (L/dia)', 'Energia Bombeamento (kWh/ano)', 'Descarte Inicial (L)']
    rf_co2 = RandomForestRegressor(n_estimators=30, max_depth=8, random_state=42, n_jobs=-1).fit(df_sample[feat_co2].fillna(0), df_sample['lifetime_net_co2_saved_kg'].fillna(0))
    imp_co2 = rf_co2.feature_importances_ * 100

    fig, axes = plt.subplots(1, 3, figsize=(19, 6.0))
    for ax_idx, (imp, labels, title, col, lbl) in enumerate([
        (imp_sav, lbl_sav, 'A) Drivers da Economia Pluvial (%) [Físicos]', '#1f77b4', 'Importância Relativa Gini (%)'),
        (imp_vpl, lbl_vpl, 'B) Drivers do VPL Financeiro (R$) [Econômicos]', '#2ca02c', 'Importância Relativa Gini (%)'),
        (imp_co2, lbl_co2, 'C) Drivers do CO₂ Líquido Evitado (kg) [Ambientais]', '#9467bd', 'Importância Relativa Gini (%)')
    ]):
        sort_idx = np.argsort(imp)
        y_pos = np.arange(len(labels))
        bars = axes[ax_idx].barh(y_pos, imp[sort_idx], color=col, edgecolor='black', alpha=0.88, height=0.62)
        axes[ax_idx].set_yticks(y_pos)
        axes[ax_idx].set_yticklabels([labels[i] for i in sort_idx], fontweight='bold')
        axes[ax_idx].set_title(title, fontweight='bold', fontsize=12)
        axes[ax_idx].set_xlabel(lbl, fontweight='bold')
        axes[ax_idx].set_xlim(0, max(imp) * 1.18)
        for bar in bars:
            w = bar.get_width()
            axes[ax_idx].text(w + 0.6, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=9.5, fontweight='bold')

    plt.suptitle("Figura 1.1 — Importância Global das Variáveis Físicas, Operacionais e Tarifárias nos Indicadores de Desempenho (Random Forest Gini %)", fontweight='bold', fontsize=13.5, y=1.02)
    plt.tight_layout()
    fig1_1_path = os.path.join(CAP1_DIR, "fig1_1_importancia_parametros_rf.png")
    plt.savefig(fig1_1_path)
    plt.close()

    # Fig 1.2: Boxplots Comparativos Multi-Indicador
    print("[+] 1.2 Boxplots Comparativos das 5 Tipologias...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    sns.boxplot(data=df_best, x="building_label", y="potential_savings_pct", hue="building_label", palette="viridis", legend=False, ax=axes[0, 0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[0, 0].set_title("A) Potencial de Economia Pluvial (%) por Tipologia", fontweight='bold')
    axes[0, 0].set_xlabel("Tipologia Edilícia", fontweight='bold')
    axes[0, 0].set_ylabel("Economia Pluvial Média (%)", fontweight='bold')

    df_best_vpl = df_best.copy()
    df_best_vpl["vpl_kbrl"] = df_best_vpl["vpl_brl"] / 1e3
    sns.boxplot(data=df_best_vpl, x="building_label", y="vpl_kbrl", hue="building_label", palette="crest", legend=False, ax=axes[0, 1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[0, 1].set_title("B) Valor Presente Líquido - VPL (mil R$) por Tipologia", fontweight='bold')
    axes[0, 1].set_xlabel("Tipologia Edilícia", fontweight='bold')
    axes[0, 1].set_ylabel("VPL Econômico (kR$)", fontweight='bold')

    df_best_vol = df_best.copy()
    df_best_vol["vol_kl"] = df_best_vol["lower_tank_vol_l"] / 1e3
    sns.boxplot(data=df_best_vol, x="building_label", y="vol_kl", hue="building_label", palette="mako", legend=False, ax=axes[1, 0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[1, 0].set_title("C) Volume Ótimo de Cisterna (m³) por Tipologia", fontweight='bold')
    axes[1, 0].set_xlabel("Tipologia Edilícia", fontweight='bold')
    axes[1, 0].set_ylabel("Volume de Cisterna Recomendado (m³)", fontweight='bold')

    sns.boxplot(data=df_best, x="building_label", y="lifetime_net_co2_saved_kg", hue="building_label", palette="rocket", legend=False, ax=axes[1, 1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[1, 1].set_title("D) Balanço Líquido de CO₂ Evitado na Vida Útil (kg CO₂-eq)", fontweight='bold')
    axes[1, 1].set_xlabel("Tipologia Edilícia", fontweight='bold')
    axes[1, 1].set_ylabel("CO₂ Líquido Evitado (kg)", fontweight='bold')
    axes[1, 1].axhline(0, color='red', linestyle='--', linewidth=1.2)

    plt.suptitle("Figura 1.2 — Distribuição de Desempenho Multi-Indicador pelas 5 Tipologias Residenciais (652 Municípios)", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_2_path = os.path.join(CAP1_DIR, "fig1_2_boxplots_indicadores_5_tipologias.png")
    plt.savefig(fig1_2_path)
    plt.close()

    # Fig 1.3: Curvas de Saturação e Eficiência Marginal
    print("[+] 1.3 Curvas de Saturação de Reservatório e Eficiência Marginal...")
    sweep_curves = df_sample.groupby(["building_label", "lower_tank_vol_l"], observed=True)["potential_savings_pct"].mean().reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for idx, typ in enumerate(TYPOLOGY_ORDER):
        sub = sweep_curves[sweep_curves["building_label"] == typ].sort_values("lower_tank_vol_l")
        axes[0].plot(sub["lower_tank_vol_l"]/1e3, sub["potential_savings_pct"], marker='o', linewidth=2.2, label=typ, color=palette_typ[idx])
        vols = sub["lower_tank_vol_l"].values / 1e3
        savs = sub["potential_savings_pct"].values
        if len(vols) > 1:
            d_vol = np.diff(vols)
            d_sav = np.diff(savs)
            marginal_gain = d_sav / d_vol
            mid_vols = (vols[:-1] + vols[1:]) / 2
            axes[1].plot(mid_vols, marginal_gain, marker='s', linewidth=2.2, label=typ, color=palette_typ[idx])

    axes[0].set_title("A) Curvas de Saturação: Volume de Cisterna (m³) vs Economia (%)", fontweight='bold')
    axes[0].set_xlabel("Capacidade da Cisterna Inferior (m³)", fontweight='bold')
    axes[0].set_ylabel("Economia Potencial Média (%)", fontweight='bold')
    axes[0].legend(title="Tipologia", loc="lower right")
    axes[0].grid(True, linestyle='--', alpha=0.6)

    axes[1].set_title("B) Eficiência Marginal: Ganho Percentual por m³ Adicionado (Δ%/m³)", fontweight='bold')
    axes[1].set_xlabel("Volume da Cisterna (m³)", fontweight='bold')
    axes[1].set_ylabel("Eficiência Marginal (Pontos % por m³)", fontweight='bold')
    axes[1].axhline(2.5, color='red', linestyle='--', linewidth=1.5, label='Limiar Ótimo Técnico (Δ = 2.5 %/m³)')
    axes[1].legend(title="Tipologia", loc="upper right")
    axes[1].grid(True, linestyle='--', alpha=0.6)

    plt.suptitle("Figura 1.3 — Dinâmica de Saturação e Rendimentos Decrescentes de Armazenamento por Tipologia", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_3_path = os.path.join(CAP1_DIR, "fig1_3_curvas_saturacao_eficiencia_marginal.png")
    plt.savefig(fig1_3_path)
    plt.close()

    # Fig 1.4: Heatmaps Tipologia x Horizonte
    print("[+] 1.4 Heatmaps Tipologia vs Horizonte...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    pivot_sav = df_sample.pivot_table(index="building_label", columns="horizon", values="potential_savings_pct", aggfunc="mean", observed=True).reindex(index=TYPOLOGY_ORDER, columns=HORIZON_ORDER)
    sns.heatmap(pivot_sav, annot=True, fmt=".2f", cmap=plt.get_cmap("YlGnBu", 7), ax=axes[0], cbar_kws={'label': 'Economia Média (%)'}, annot_kws={"weight": "bold", "size": 11})
    axes[0].set_title("A) Matriz de Economia Pluvial (%) por Tipologia e Horizonte", fontweight='bold')
    axes[0].set_xlabel("Horizonte Temporal", fontweight='bold')
    axes[0].set_ylabel("Tipologia Edilícia", fontweight='bold')

    pivot_vpl = df_sample.pivot_table(index="building_label", columns="horizon", values="vpl_brl", aggfunc=lambda x: np.mean(x)/1e3, observed=True).reindex(index=TYPOLOGY_ORDER, columns=HORIZON_ORDER)
    sns.heatmap(pivot_vpl, annot=True, fmt=".1f", cmap=plt.get_cmap("YlGn", 7), ax=axes[1], cbar_kws={'label': 'VPL Médio (mil R$)'}, annot_kws={"weight": "bold", "size": 11})
    axes[1].set_title("B) Matriz de VPL Econômico (mil R$) por Tipologia e Horizonte", fontweight='bold')
    axes[1].set_xlabel("Horizonte Temporal", fontweight='bold')
    axes[1].set_ylabel("Tipologia Edilícia", fontweight='bold')

    plt.suptitle("Figura 1.4 — Matriz de Desempenho Integrado: Efeito Combinado de Tipologia e Mudanças Climáticas", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_4_path = os.path.join(CAP1_DIR, "fig1_4_heatmaps_tipologia_vs_horizonte.png")
    plt.savefig(fig1_4_path)
    plt.close()

    # Fig 1.5: Avaliação Financeira, Payback, CAPEX e Cenário 100% Concessionária
    print("[+] 1.5 Avaliação Financeira, Payback e Cenário de Referência...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    df_payback = df_best[df_best["payback_years"] > 0].copy()
    sns.boxplot(data=df_payback, x="building_label", y="payback_years", hue="building_label", palette="Blues", legend=False, ax=axes[0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[0].set_title("A) Tempo de Retorno do Investimento (Payback em Anos)", fontweight='bold')
    axes[0].set_xlabel("Tipologia Edilícia", fontweight='bold')
    axes[0].set_ylabel("Payback Descontado (Anos)", fontweight='bold')
    axes[0].set_ylim(0, min(15, df_payback["payback_years"].quantile(0.98)))
    axes[0].grid(True, linestyle='--', alpha=0.5)

    b_fin = df_best.groupby("building_label", observed=True).agg({
        'annual_baseline_utility_bill_brl': 'mean',
        'capex_total_brl': 'mean',
        'annual_water_savings_brl': 'mean'
    }).reindex(TYPOLOGY_ORDER).reset_index()

    x = np.arange(len(b_fin))
    width = 0.26
    b0 = axes[1].bar(x - width, b_fin["annual_baseline_utility_bill_brl"]/1e3, width, label='Fatura Concessionária 100% (Sem Netuno)', color='#b15928', edgecolor='black', alpha=0.85)
    b1 = axes[1].bar(x, b_fin["capex_total_brl"]/1e3, width, label='CAPEX Inicial Sistema Pluvial (mil R$)', color='#e66101', edgecolor='black', alpha=0.88)
    b2 = axes[1].bar(x + width, b_fin["annual_water_savings_brl"]/1e3, width, label='Economia Anual de Água (mil R$/ano)', color='#2ca02c', edgecolor='black', alpha=0.88)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(b_fin["building_label"], fontweight='bold')
    axes[1].set_title("B) Cenário 100% Concessionária vs CAPEX Inicial vs Economia Anual", fontweight='bold')
    axes[1].set_ylabel("Valores Monetários (mil R$)", fontweight='bold')
    axes[1].legend(loc="upper left")
    axes[1].grid(True, linestyle='--', alpha=0.5)
    for bar in b0:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.5, f'R${h:.1f}k', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for bar in b1:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.5, f'R${h:.1f}k', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for bar in b2:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.5, f'R${h:.1f}k', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    plt.suptitle("Figura 1.5 — Avaliação da Viabilidade Financeira e Contraste com o Cenário 100% Concessionária", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_5_path = os.path.join(CAP1_DIR, "fig1_5_viabilidade_financeira_payback_capex.png")
    plt.savefig(fig1_5_path)
    plt.close()

    # Fig 1.6: Decomposição de Custos de Ciclo de Vida a 20 Anos (LCC)
    print("[+] 1.6 Decomposição de Custos de Ciclo de Vida a 20 Anos (LCC)...")
    fig, axes = plt.subplots(1, 2, figsize=(17, 6.5))
    
    lcc_decomp = df_best.groupby('building_label', observed=True).agg({
        'lcc_baseline_kbrl': 'mean',
        'lcc_residual_water_kbrl': 'mean',
        'lcc_opex_kbrl': 'mean',
        'lcc_capex_kbrl': 'mean',
        'vpl_brl': 'mean'
    }).reindex(TYPOLOGY_ORDER).reset_index()

    x_idx = np.arange(len(TYPOLOGY_ORDER))
    w_bar = 0.35

    # Barra 1: Cenário Referência 100% Concessionária
    axes[0].bar(x_idx - w_bar/2, lcc_decomp['lcc_baseline_kbrl'], width=w_bar, label='1. Cenário 100% Concessionária (Sem Netuno)', color='#b15928', edgecolor='black', alpha=0.88)
    
    # Barra 2: Cenário com Aproveitamento Pluvial Netuno (Empilhado: Fatura Residual + OPEX + CAPEX)
    p_res = axes[0].bar(x_idx + w_bar/2, lcc_decomp['lcc_residual_water_kbrl'], width=w_bar, label='2a. Fatura Residual Concessionária (20 anos)', color='#a6cee3', edgecolor='black', alpha=0.92)
    p_op = axes[0].bar(x_idx + w_bar/2, lcc_decomp['lcc_opex_kbrl'], width=w_bar, bottom=lcc_decomp['lcc_residual_water_kbrl'], label='2b. OPEX Acumulado (Energia + Manut.)', color='#fb9a99', edgecolor='black', alpha=0.92)
    p_cap = axes[0].bar(x_idx + w_bar/2, lcc_decomp['lcc_capex_kbrl'], width=w_bar, bottom=lcc_decomp['lcc_residual_water_kbrl'] + lcc_decomp['lcc_opex_kbrl'], label='2c. CAPEX Inicial Sistema Pluvial', color='#33a02c', edgecolor='black', alpha=0.92)

    axes[0].set_xticks(x_idx)
    axes[0].set_xticklabels(TYPOLOGY_ORDER, fontweight='bold')
    axes[0].set_ylabel('Custo de Ciclo de Vida a 20 Anos — LCC (mil R$)', fontweight='bold')
    axes[0].set_title('A) Comparação de LCC: 100% Concessionária vs Sistema Pluvial Netuno', fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)
    axes[0].legend(loc='upper left', fontsize=8.5)

    # Anotações de VPL economizado no topo
    for i, r in lcc_decomp.iterrows():
        vpl_k = r['vpl_brl'] / 1e3
        h_netuno = r['lcc_residual_water_kbrl'] + r['lcc_opex_kbrl'] + r['lcc_capex_kbrl']
        axes[0].text(i + w_bar/2, h_netuno + 15, f"VPL:\nR${vpl_k:+.1f}k", ha='center', va='bottom', fontsize=8.0, fontweight='bold', color='darkgreen' if vpl_k >= 0 else 'darkred')

    df_best['net_annual_brl'] = df_best['annual_water_savings_brl'] - df_best['annual_opex_brl']
    sns.boxplot(data=df_best, x='region', y='net_annual_brl', hue='region', order=REG_ORDER, palette='Set3', legend=False, ax=axes[1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
    axes[1].set_yscale('log')
    axes[1].set_title('B) Benefício Financeiro Líquido Anual por Macrorregião (R$/ano)', fontweight='bold')
    axes[1].set_xlabel('Macrorregião', fontweight='bold')
    axes[1].set_ylabel('Economia Líquida Anual (R$/ano - escala log)', fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5, which='both')

    plt.suptitle("Figura 1.6 — Análise de Custo de Ciclo de Vida (LCC a 20 Anos) e Decomposição Financeira", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_6_path = os.path.join(CAP1_DIR, "fig1_6_decomposicao_economica_custos_beneficios.png")
    plt.savefig(fig1_6_path)
    plt.close()

    # Fig 1.7: Panorama Tarifário Nacional com Bins Discretos
    print("[+] 1.7 Panorama Tarifário Nacional com Bins Discretos...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # A) Mapa com Bins de Tarifa de Água
    plot_brazil_basemap(axes[0, 0], states_gdf)
    bins_agua = [0, 3.0, 4.5, 6.0, 7.5, 9.5, 14.0]
    plot_binned_scatter(axes[0, 0], df_best['lon'], df_best['lat'], df_best['tarifa_agua_base_r_m3'], bins_agua, 'YlOrRd', 'Tarifa Base de Água (R$/m³)', fig, cbar_fmt="{:.1f}")
    axes[0, 0].set_title('A) Distribuição Espacial por Faixas da Tarifa Base de Água (R$/m³)', fontweight='bold')

    # B) Mapa com Bins de Tarifa de Eletricidade
    plot_brazil_basemap(axes[0, 1], states_gdf)
    bins_elec = [0.60, 0.75, 0.85, 0.95, 1.05, 1.30]
    plot_binned_scatter(axes[0, 1], df_best['lon'], df_best['lat'], df_best['tarifa_eletricidade_b1_r_kwh'], bins_elec, 'plasma', 'Tarifa Eletricidade B1 (R$/kWh)', fig, cbar_fmt="{:.2f}")
    axes[0, 1].set_title('B) Distribuição Espacial por Faixas da Tarifa B1 de Eletricidade (R$/kWh)', fontweight='bold')

    df_best['tarifa_combinada_m3'] = df_best['tarifa_agua_base_r_m3'] * (1.0 + df_best['esgoto_pct_sobre_agua'] / 100.0)
    sns.boxplot(data=df_best, x='region', y='tarifa_combinada_m3', hue='region', order=REG_ORDER, palette='Blues', legend=False, ax=axes[1, 0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
    axes[1, 0].set_title('C) Tarifa Combinada de Água + Esgoto (R$/m³) por Região', fontweight='bold')
    axes[1, 0].set_xlabel('Macrorregião Brasileira', fontweight='bold')
    axes[1, 0].set_ylabel('Tarifa Combinada Água + Esgoto (R$/m³)', fontweight='bold')
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    sns.boxplot(data=df_best, x='region', y='tarifa_eletricidade_b1_r_kwh', hue='region', order=REG_ORDER, palette='Oranges', legend=False, ax=axes[1, 1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"blue", "markeredgecolor":"black"})
    axes[1, 1].set_title('D) Tarifa Residencial B1 de Eletricidade (R$/kWh) por Região', fontweight='bold')
    axes[1, 1].set_xlabel('Macrorregião Brasileira', fontweight='bold')
    axes[1, 1].set_ylabel('Tarifa Eletricidade B1 (R$/kWh)', fontweight='bold')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 1.7 — Panorama Tarifário Nacional: Saneamento Básico e Energia Elétrica nas 652 Cidades", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_7_path = os.path.join(CAP1_DIR, "fig1_7_panorama_tarifario_nacional_energia_agua.png")
    plt.savefig(fig1_7_path)
    plt.close()

    # Fig 1.8: Elasticidade Cruzada de Tarifas
    print("[+] 1.8 Elasticidade Cruzada de Tarifas...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    df_city_tar = df_best.groupby('city', observed=True).agg({
        'tarifa_agua_base_r_m3': 'first', 'esgoto_pct_sobre_agua': 'first',
        'tarifa_eletricidade_b1_r_kwh': 'first', 'vpl_brl': 'mean', 'region': 'first'
    }).reset_index()
    df_city_tar['tarifa_combinada_m3'] = df_city_tar['tarifa_agua_base_r_m3'] * (1.0 + df_city_tar['esgoto_pct_sobre_agua'] / 100.0)

    sns.scatterplot(data=df_city_tar, x='tarifa_eletricidade_b1_r_kwh', y='tarifa_combinada_m3', hue='region', hue_order=REG_ORDER, palette='tab10', s=45, ax=axes[0], alpha=0.85, edgecolor='black')
    axes[0].set_title('A) Dispersão das 652 Cidades no Espaço Tarifário Nacional', fontweight='bold')
    axes[0].set_xlabel('Tarifa de Energia Elétrica B1 (R$/kWh)', fontweight='bold')
    axes[0].set_ylabel('Tarifa Combinada Água + Esgoto (R$/m³)', fontweight='bold')
    axes[0].legend(title='Macrorregião', loc='upper right')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    p_sens = df_best.sample(n=min(25000, len(df_best)), random_state=42).copy()
    sens_deltas = np.linspace(-0.30, 0.30, 7)
    sens_results = []
    for d in sens_deltas:
        vpl_sim = p_sens['vpl_brl'] + (p_sens['annual_water_savings_brl'] * d * 11.4699)
        sens_results.append({
            'delta_pct': d * 100.0,
            'vpl_medio_uti': vpl_sim[p_sens['building_code'] == 'UTI'].mean() / 1e3,
            'vpl_medio_utg': vpl_sim[p_sens['building_code'] == 'UTG'].mean() / 1e3,
            'vpl_medio_msg': vpl_sim[p_sens['building_code'] == 'MSG'].mean() / 1e3,
            'vpl_medio_mfh': vpl_sim[p_sens['building_code'] == 'MFH'].mean() / 1e3,
            'vpl_medio_mfl': vpl_sim[p_sens['building_code'] == 'MFL'].mean() / 1e3
        })
    df_sens = pd.DataFrame(sens_results)
    for code, label, color in [('vpl_medio_uti', 'UTI (4 hab)', '#1f77b4'), ('vpl_medio_utg', 'UTG (8 hab)', '#aec7e8'),
                               ('vpl_medio_msg', 'MSG (16 hab)', '#ff7f0e'), ('vpl_medio_mfh', 'MFH (64 hab)', '#2ca02c'),
                               ('vpl_medio_mfl', 'MFL (128 hab)', '#d62728')]:
        axes[1].plot(df_sens['delta_pct'], df_sens[code], marker='o', label=label, color=color, linewidth=2.5)

    axes[1].axhline(0, color='black', linestyle='--', linewidth=1.2)
    axes[1].set_title('B) Elasticidade do VPL frente a Variações na Tarifa de Água (±30%)', fontweight='bold')
    axes[1].set_xlabel('Variação Tarifária (%)', fontweight='bold')
    axes[1].set_ylabel('VPL Médio (mil R$)', fontweight='bold')
    axes[1].legend(title='Tipologia', loc='upper left')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 1.8 — Elasticidade Cruzada e Sensibilidade Tarifária no Brasil", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_8_path = os.path.join(CAP1_DIR, "fig1_8_elasticidade_cruzada_tarifas_agua_energia.png")
    plt.savefig(fig1_8_path)
    plt.close()

    # Fig 1.9: Ranking Estadual VPL e Payback (27 UFs)
    print("[+] 1.9 Ranking Estadual de Viabilidade (27 UFs)...")
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))
    df_uf_stats = df_best.groupby('uf', observed=True).agg({'vpl_brl': 'mean', 'payback_years': 'median'}).sort_values(by='vpl_brl', ascending=False).reset_index()
    sns.barplot(data=df_uf_stats, x='uf', y='vpl_brl', hue='uf', palette='viridis', legend=False, ax=axes[0], edgecolor='black')
    axes[0].set_title('A) Ranking Estadual do VPL Financeiro Médio das Soluções Ótimas (R$)', fontweight='bold')
    axes[0].set_xlabel('Unidade da Federação (UF)', fontweight='bold')
    axes[0].set_ylabel('VPL Médio (R$)', fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5, axis='y')

    df_payback_uf = df_best[(df_best['payback_years'] > 0) & (df_best['payback_years'] <= 25)].copy()
    uf_order = df_uf_stats['uf'].tolist()
    sns.boxplot(data=df_payback_uf, x='uf', y='payback_years', hue='uf', order=uf_order, palette='Blues_r', legend=False, ax=axes[1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
    axes[1].set_title('B) Distribuição do Tempo de Retorno (Payback em Anos) por Estado', fontweight='bold')
    axes[1].set_xlabel('Unidade da Federação (UF)', fontweight='bold')
    axes[1].set_ylabel('Payback (Anos)', fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.suptitle("Figura 1.9 — Panorama Estadual da Atratividade Financeira do Aproveitamento Pluvial no Brasil (27 UFs)", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_9_path = os.path.join(CAP1_DIR, "fig1_9_ranking_estadual_vpl_payback.png")
    plt.savefig(fig1_9_path)
    plt.close()

    # Fig 1.10: Panorama Nacional de Esgoto (% sobre Água por Cidade) e Efeito Multiplicador no VPL
    print("[+] 1.10 Panorama Nacional de Tarifas de Esgoto (% sobre Água) e Multiplicador de VPL...")
    fig, axes = plt.subplots(2, 2, figsize=(18, 13))

    # A) Mapa Cartográfico Nacional da Alíquota de Esgoto com Bins
    plot_brazil_basemap(axes[0, 0], states_gdf)
    bins_esg = [45, 60, 75, 82, 92, 100]
    plot_binned_scatter(axes[0, 0], df_best['lon'], df_best['lat'], df_best['esgoto_pct_sobre_agua'], bins_esg, 'Purples', 'Alíquota de Esgoto (% sobre Água)', fig, cbar_fmt="{:.0f}%", bin_labels=['50% (Mínimo)', '70% (RN/MS/RO)', '80% (Padrão 61% Cidades / PR)', '85-90% (Curitiba/Privadas)', '100% (Integral DF/RJ/PE/SP)'])
    axes[0, 0].set_title('A) Distribuição Espacial da Alíquota de Esgoto (% sobre a Conta de Água)', fontweight='bold')

    # B) Ranking Estadual da Alíquota Média de Esgoto (%)
    df_esg_uf = df_best.groupby('uf', observed=True)['esgoto_pct_sobre_agua'].mean().sort_values(ascending=False).reset_index()
    sns.barplot(data=df_esg_uf, x='uf', y='esgoto_pct_sobre_agua', hue='uf', palette='Purples_r', legend=False, ax=axes[0, 1], edgecolor='black')
    axes[0, 1].set_title('B) Alíquota Média de Cobrança de Esgoto (% sobre Água) por Estado (27 UFs)', fontweight='bold')
    axes[0, 1].set_xlabel('Unidade da Federação (UF)', fontweight='bold')
    axes[0, 1].set_ylabel('Esgoto (% sobre Água)', fontweight='bold')
    axes[0, 1].set_ylim(0, 110)
    axes[0, 1].grid(True, linestyle='--', alpha=0.5, axis='y')
    for p in axes[0, 1].patches:
        h = p.get_height()
        if h > 0:
            axes[0, 1].annotate(f"{h:.0f}%", (p.get_x() + p.get_width()/2., h), ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    # C) Efeito Alavancador do Esgoto no VPL por Tipologia
    pv_factor = 11.4699
    df_best['savings_water_only_brl'] = df_best['annual_water_savings_brl'] / (1.0 + df_best['esgoto_pct_sobre_agua'] / 100.0)
    df_best['savings_sewage_brl'] = df_best['annual_water_savings_brl'] - df_best['savings_water_only_brl']
    df_best['vpl_water_only_kbrl'] = (df_best['vpl_brl'] - (df_best['savings_sewage_brl'] * pv_factor)) / 1e3
    df_best['vpl_total_kbrl'] = df_best['vpl_brl'] / 1e3

    df_comp_vpl = df_best.groupby('building_label', observed=True).agg({
        'vpl_water_only_kbrl': 'mean', 'vpl_total_kbrl': 'mean'
    }).reindex(TYPOLOGY_ORDER).reset_index()

    x_typ = np.arange(len(TYPOLOGY_ORDER))
    w_esg = 0.35
    b_no_esg = axes[1, 0].bar(x_typ - w_esg/2, df_comp_vpl['vpl_water_only_kbrl'], width=w_esg, label='VPL sem Cobrança de Esgoto (Apenas Água Potável)', color='#9ecae1', edgecolor='black', alpha=0.88)
    b_with_esg = axes[1, 0].bar(x_typ + w_esg/2, df_comp_vpl['vpl_total_kbrl'], width=w_esg, label='VPL Real com Esgoto Evitado (Água + Esgoto)', color='#6a51a3', edgecolor='black', alpha=0.88)
    axes[1, 0].axhline(0, color='black', linestyle='--', linewidth=1.2)
    axes[1, 0].set_xticks(x_typ)
    axes[1, 0].set_xticklabels(TYPOLOGY_ORDER, fontweight='bold')
    axes[1, 0].set_ylabel('VPL Médio (mil R$)', fontweight='bold')
    axes[1, 0].set_title('C) Efeito Alavancador do Esgoto: VPL com vs sem Cobrança de Esgoto', fontweight='bold')
    axes[1, 0].legend(loc='upper left')
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)
    for bar in b_no_esg:
        h = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, h + (1.5 if h >= 0 else -4.5), f'R${h:.1f}k', ha='center', va='bottom', fontsize=8.0, fontweight='bold')
    for bar in b_with_esg:
        h = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, h + 2.0, f'R${h:.1f}k', ha='center', va='bottom', fontsize=8.0, fontweight='bold', color='darkviolet')

    # D) Dispersão Tarifa de Água vs Alíquota de Esgoto vs VPL Médio
    city_tar_esg = df_best.groupby('city_clean', observed=True).agg({
        'tarifa_agua_base_r_m3': 'first', 'esgoto_pct_sobre_agua': 'first', 'vpl_brl': 'mean', 'region': 'first'
    }).reset_index()
    sc_esg = auto_binned_scatter(axes[1, 1], city_tar_esg['tarifa_agua_base_r_m3'], city_tar_esg['esgoto_pct_sobre_agua'], city_tar_esg['vpl_brl']/1e3, s=65, alpha=0.85, edgecolors='black', linewidths=0.3)
    axes[1, 1].set_title('D) Dispersão: Tarifa Base de Água vs Alíquota de Esgoto vs VPL Médio (mil R$)', fontweight='bold')
    axes[1, 1].set_xlabel('Tarifa Base de Água (R$/m³)', fontweight='bold')
    axes[1, 1].set_ylabel('Cobrança de Esgoto (% sobre a Água)', fontweight='bold')
    cb_esg = fig.colorbar(sc_esg, ax=axes[1, 1], fraction=0.046, pad=0.04)
    cb_esg.set_label('VPL Médio das Soluções (mil R$)', fontweight='bold')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 1.10 — Panorama das Alíquotas de Esgoto e seu Impacto Multiplicador na Viabilidade Econômica", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig1_10_path = os.path.join(CAP1_DIR, "fig1_10_panorama_tarifas_esgoto_brasil.png")
    plt.savefig(fig1_10_path)
    plt.close()

    # ==============================================================================================
    # CAPÍTULO 2: AUMENTO DOS RESERVATÓRIOS ÓTIMOS EM CENÁRIOS FUTUROS (5 FIGURAS)
    # ==============================================================================================
    print("\n" + "="*80)
    print("GERANDO CAPÍTULO 2: AUMENTO DOS RESERVATÓRIOS ÓTIMOS EM CENÁRIOS FUTUROS (5 FIGURAS)")
    print("="*80)

    # Fig 2.1: Trajetórias Climáticas 1980-2100
    print("[+] 2.1 Trajetórias Climáticas e Tendências Temporais...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    trend_typ = df_sample.groupby(["building_label", "horizon"], observed=True)["potential_savings_pct"].mean().reset_index()
    for idx, typ in enumerate(TYPOLOGY_ORDER):
        sub = trend_typ[trend_typ["building_label"] == typ]
        axes[0].plot(sub["horizon"], sub["potential_savings_pct"], marker='o', linewidth=2.5, label=typ, color=palette_typ[idx])
        for _, r in sub.iterrows():
            axes[0].annotate(f"{r['potential_savings_pct']:.1f}%", (r["horizon"], r["potential_savings_pct"]), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=8.5, fontweight='bold')

    axes[0].set_title("A) Evolução da Economia Pluvial (%) ao Longo do Século XXI", fontweight='bold')
    axes[0].set_xlabel("Horizonte Temporal Climatológico", fontweight='bold')
    axes[0].set_ylabel("Potencial Médio de Economia (%)", fontweight='bold')
    axes[0].legend(title="Tipologia", loc="center left", bbox_to_anchor=(1, 0.5))
    axes[0].grid(True, linestyle='--', alpha=0.6)

    trend_ssp = df_sample[df_sample["scenario"] != "Historical"].groupby(["scenario", "horizon"], observed=True)["potential_savings_pct"].agg(['mean', 'std']).reset_index()
    ssp_colors = {"SSP245": "#2b5c8f", "SSP585": "#d95f02"}
    for sc in ["SSP245", "SSP585"]:
        sub = trend_ssp[trend_ssp["scenario"] == sc]
        axes[1].plot(sub["horizon"], sub["mean"], marker='s', linewidth=2.5, label=f"Cenário {sc}", color=ssp_colors.get(sc, "#333333"))
        axes[1].fill_between(sub["horizon"], sub["mean"] - 0.5 * sub["std"], sub["mean"] + 0.5 * sub["std"], color=ssp_colors.get(sc, "#333333"), alpha=0.15)
        for _, r in sub.iterrows():
            axes[1].annotate(f"{r['mean']:.2f}%", (r["horizon"], r["mean"]), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=9, fontweight='bold')

    axes[1].set_title("B) Impacto Médio Comparativo entre Cenários SSP2-4.5 e SSP5-8.5", fontweight='bold')
    axes[1].set_xlabel("Horizonte Futuro (30 anos)", fontweight='bold')
    axes[1].set_ylabel("Economia Pluvial Média Nacional (%)", fontweight='bold')
    axes[1].legend(title="Cenário de Emissões", loc="lower left")
    axes[1].grid(True, linestyle='--', alpha=0.6)

    plt.suptitle("Figura 2.1 — Tendências Temporais das Mudanças Climáticas no Aproveitamento Pluvial no Brasil", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig2_1_path = os.path.join(CAP2_DIR, "fig2_1_trajetorias_climaticas_1980_2100.png")
    plt.savefig(fig2_1_path)
    plt.close()

    # Fig 2.2: Frequência dos Volumes Ótimos Grid 2x5
    print("[+] 2.2 Grid 2x5 de Frequência de Volumes Ótimos...")
    df_best_fig7 = df_best.copy()
    df_best_fig7['vol_m3'] = (df_best_fig7['lower_tank_vol_l'] / 1000.0).round(1)
    TYP_CODES = ['UTI', 'UTG', 'MSG', 'MFH', 'MFL']
    TYP_TITLES = {
        'UTI': 'UTI (4 hab - 60 m²)', 'UTG': 'UTG (8 hab - 115 m²)', 'MSG': 'MSG (16 hab - 132 m²)',
        'MFH': 'MFH (64 hab - 158 m²)', 'MFL': 'MFL (128 hab - 421 m²)'
    }
    TIMELINE_ORDER = ['Histórico\n(1980-2013)', 'Near Future\n(2015-2044)', 'Middle Future\n(2045-2074)', 'Far Future\n(2075-2100)']

    df_hist = df_best_fig7[df_best_fig7['horizon'].astype(str).str.contains('Hist', case=False, na=False)].copy()
    df_hist['timeline'] = 'Histórico\n(1980-2013)'

    df_ssp245 = df_best_fig7[df_best_fig7['scenario'].astype(str).str.contains('245', case=False, na=False) | df_best_fig7['horizon'].astype(str).str.contains('245', case=False, na=False)].copy()
    df_ssp245['timeline'] = df_ssp245['horizon'].astype(str).replace({'Near': 'Near Future\n(2015-2044)', 'Middle': 'Middle Future\n(2045-2074)', 'Far': 'Far Future\n(2075-2100)'})
    df_ssp245_all = pd.concat([df_hist, df_ssp245], ignore_index=True)
    df_ssp245_all['timeline'] = pd.Categorical(df_ssp245_all['timeline'], categories=TIMELINE_ORDER, ordered=True)

    df_ssp585 = df_best_fig7[df_best_fig7['scenario'].astype(str).str.contains('585', case=False, na=False) | df_best_fig7['horizon'].astype(str).str.contains('585', case=False, na=False)].copy()
    df_ssp585['timeline'] = df_ssp585['horizon'].astype(str).replace({'Near': 'Near Future\n(2015-2044)', 'Middle': 'Middle Future\n(2045-2074)', 'Far': 'Far Future\n(2075-2100)'})
    df_ssp585_all = pd.concat([df_hist, df_ssp585], ignore_index=True)
    df_ssp585_all['timeline'] = pd.Categorical(df_ssp585_all['timeline'], categories=TIMELINE_ORDER, ordered=True)

    VOL_COLORS = {
        1.0: '#c6dbef', 2.0: '#9ecae1', 3.0: '#6baed6', 5.0: '#3182bd',
        7.5: '#fd8d3c', 10.0: '#e6550d', 15.0: '#a63603', 20.0: '#7f2704', 30.0: '#491802'
    }

    fig, axes = plt.subplots(2, 5, figsize=(22, 9.5), sharex=True, sharey=True)
    for row_idx, (ssp_label, df_ssp) in enumerate([('SSP2-4.5 (Intermediário)', df_ssp245_all), ('SSP5-8.5 (Fóssil / Extremo)', df_ssp585_all)]):
        for col_idx, code in enumerate(TYP_CODES):
            ax = axes[row_idx, col_idx]
            sub = df_ssp[df_ssp['building_code'] == code]
            ct = pd.crosstab(sub['timeline'], sub['vol_m3'], normalize='index') * 100.0
            vol_cols = sorted(ct.columns)
            bottom = np.zeros(len(TIMELINE_ORDER))
            for v in vol_cols:
                vals = [ct.loc[t, v] if v in ct.columns and t in ct.index else 0 for t in TIMELINE_ORDER]
                c = VOL_COLORS.get(v, '#756bb1')
                bars = ax.bar(range(len(TIMELINE_ORDER)), vals, bottom=bottom, label=f"{v:g} m³", color=c, edgecolor='white', width=0.65, alpha=0.92)
                for b_idx, (b_val, b_bot) in enumerate(zip(vals, bottom)):
                    if b_val >= 7.0:
                        ax.text(b_idx, b_bot + b_val/2.0, f"{v:g}m³\n({b_val:.0f}%)", ha='center', va='center',
                                fontsize=7.5, fontweight='bold', color='white' if v >= 3.0 else 'black')
                bottom += np.array(vals)
            ax.set_title(f"{TYP_TITLES[code]}" if row_idx == 0 else "", fontweight='bold', fontsize=11, pad=8)
            ax.set_xticks(range(len(TIMELINE_ORDER)))
            ax.set_xticklabels(TIMELINE_ORDER)
            ax.set_ylim(0, 100)
            if col_idx == 0:
                ax.set_ylabel(f"{ssp_label}\nFrequência Relativa (%)", fontweight='bold', fontsize=10)
            if row_idx == 1:
                ax.set_xlabel("Horizonte Temporal", fontweight='bold', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.4, axis='y')

    from matplotlib.patches import Patch
    legend_handles = [Patch(facecolor=VOL_COLORS[v], edgecolor='black', label=f"{v:g} m³ ({int(v*1000)} L)") for v in sorted(VOL_COLORS.keys()) if v in df_best_fig7['vol_m3'].unique()]
    fig.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, 0.965), ncol=min(8, len(legend_handles)), frameon=True, facecolor='white', framealpha=0.95, fontsize=9.5, title="Capacidade Nominal da Cisterna:")
    plt.suptitle("Figura 2.2 — Distribuição de Frequência dos Volumes Ótimos por Tipologia, Cenário e Horizonte Temporal", fontweight='bold', fontsize=13.5, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.935])
    fig2_2_path = os.path.join(CAP2_DIR, "fig2_2_frequencia_volumes_otimos_grid_2x5.png")
    plt.savefig(fig2_2_path)
    plt.close()

    # Fig 2.3: Incerteza e Dispersão GCM CMIP6 com Bins
    print("[+] 2.3 Incerteza e Dispersão dos Modelos GCM com Bins Discretos...")
    gcm_spread = df_sample.groupby(["city_clean", "lat", "lon"], observed=True)["potential_savings_pct"].agg(['mean', 'std']).reset_index()
    gcm_spread["cv_pct"] = (gcm_spread["std"] / gcm_spread["mean"]) * 100
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    plot_brazil_basemap(axes[0], states_gdf)
    bins_std = [0, 0.8, 1.5, 2.5, 3.5, 5.0, 8.0]
    plot_binned_scatter(axes[0], gcm_spread["lon"], gcm_spread["lat"], gcm_spread["std"], bins_std, 'magma', 'Desvio Padrão Inter-GCM (%)', fig, cbar_fmt="{:.1f}")
    axes[0].set_title("A) Desvio Padrão Inter-Modelos GCM por Faixas (Pontos Percentuais)", fontweight='bold')

    plot_brazil_basemap(axes[1], states_gdf)
    bins_cv = [0, 8.0, 15.0, 25.0, 40.0, 60.0, 90.0]
    plot_binned_scatter(axes[1], gcm_spread["lon"], gcm_spread["lat"], gcm_spread["cv_pct"], bins_cv, 'inferno', 'Coeficiente de Variação - CV (%)', fig, cbar_fmt="{:.0f}")
    axes[1].set_title("B) Coeficiente de Variação - CV (%) por Faixas entre Modelos Climáticos", fontweight='bold')

    plt.suptitle("Figura 2.3 — Incerteza Espacial das Projeções Climáticas (Modelos CMIP6) no Brasil", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig2_3_path = os.path.join(CAP2_DIR, "fig2_3_dispersao_incerteza_modelos_gcm.png")
    plt.savefig(fig2_3_path)
    plt.close()

    # Fig 2.4: Deslocamento de Capacidade Delta V com Bins
    print("[+] 2.4 Deslocamento de Capacidade Delta V com Bins Discretos...")
    city_tank_shifts = df_best.groupby(["city_clean", "horizon", "lat", "lon", "region"], observed=True)["lower_tank_vol_l"].mean().unstack("horizon").reset_index()
    if "Historical" in city_tank_shifts.columns and "Far" in city_tank_shifts.columns:
        city_tank_shifts["delta_v_l"] = city_tank_shifts["Far"] - city_tank_shifts["Historical"]
    else:
        city_tank_shifts["delta_v_l"] = 0

    fig, axes = plt.subplots(1, 2, figsize=(17, 7))
    plot_brazil_basemap(axes[0], states_gdf)
    bins_dv = [-2000, -1000, -250, 0, 250, 750, 1500, 3000]
    plot_binned_scatter(axes[0], city_tank_shifts["lon"], city_tank_shifts["lat"], city_tank_shifts["delta_v_l"], bins_dv, 'Spectral_r', 'Variação Volume ΔV (L)', fig, cbar_fmt="{:g}")
    axes[0].set_title("A) Variação Absoluta de Capacidade por Faixas ΔV (L) [Far − Histórico]", fontweight='bold')
    for cap, (c_lon, c_lat) in capitals.items():
        axes[0].plot(c_lon, c_lat, marker='*', color='black', markersize=7, zorder=5)
        axes[0].text(c_lon + 0.5, c_lat, cap, fontsize=8, fontweight='bold', zorder=6)

    sns.boxplot(data=city_tank_shifts, x="region", y="delta_v_l", hue="region", order=REG_ORDER, palette="Set2", legend=False, ax=axes[1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
    axes[1].axhline(0, color='black', linestyle='--', linewidth=1.2)
    axes[1].set_title("B) Distribuição Regional do Deslocamento de Capacidade ΔV (L)", fontweight='bold')
    axes[1].set_xlabel("Macrorregião Brasileira", fontweight='bold')
    axes[1].set_ylabel("Aumento da Capacidade Ótima Necessária ΔV (Litros)", fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 2.4 — Deslocamento e Adaptação da Capacidade Ótima de Cisternas frente às Mudanças Climáticas", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig2_4_path = os.path.join(CAP2_DIR, "fig2_4_deslocamento_capacidade_delta_v_mapa_e_regioes.png")
    plt.savefig(fig2_4_path)
    plt.close()

    # Fig 2.5: Curvas Cumulativas (CDF) de Transição de Reservatórios (Histórico vs Futuro)
    print("[+] 2.5 Curvas Cumulativas de Shift de Capacidade de Reservatórios...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for typ_code, ax_sub, title_sub in [('UTI', axes[0], 'A) Casa Unifamiliar Térrea (UTI — 4 hab)'),
                                        ('MFL', axes[1], 'B) Bloco Multifamiliar Retangular (MFL — 128 hab)')]:
        sub_typ = df_best[df_best['building_code'] == typ_code]
        for horiz, col, ls in [('Historical', '#1f77b4', '-'), ('Near', '#2ca02c', '--'), ('Middle', '#ff7f0e', '-.'), ('Far', '#d62728', ':')]:
            vals = sub_typ[sub_typ['horizon'] == horiz]['lower_tank_vol_l'].values / 1e3
            if len(vals) > 0:
                sorted_v = np.sort(vals)
                cdf = np.arange(1, len(sorted_v) + 1) / len(sorted_v) * 100.0
                ax_sub.plot(sorted_v, cdf, label=f"{horiz}", color=col, linestyle=ls, linewidth=2.4)

        ax_sub.set_title(title_sub, fontweight='bold')
        ax_sub.set_xlabel("Volume da Cisterna Inferior (m³)", fontweight='bold')
        ax_sub.set_ylabel("Frequência Cumulativa (%)", fontweight='bold')
        ax_sub.legend(title="Horizonte", loc="lower right")
        ax_sub.grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 2.5 — Curvas de Distribuição Cumulativa (CDF) e Transição de Capacidade Ótima de Cisternas", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig2_5_path = os.path.join(CAP2_DIR, "fig2_5_curvas_cumulativas_shift_reservatorios.png")
    plt.savefig(fig2_5_path)
    plt.close()

    # ==============================================================================================
    # CAPÍTULO 3: COMPARAÇÃO ENTRE OS RESERVATÓRIOS ÓTIMOS AMBIENTAL, ECONÔMICO E TÉCNICO (4 FIGURAS)
    # ==============================================================================================
    print("\n" + "="*80)
    print("GERANDO CAPÍTULO 3: COMPARAÇÃO ENTRE RESERVATÓRIOS ÓTIMOS (4 FIGURAS)")
    print("="*80)

    # Fig 3.1: Comparação Direta dos 3 Critérios de Otimização por Tipologia (Com Limiar Técnico 2.5 %/m3)
    print("[+] 3.1 Comparação Direta dos Volumes Ótimos para Todas as 5 Tipologias (UTI, UTG, MSG, MFH, MFL)...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 6.8))

    df_opt_melt = df_optima.melt(
        id_vars=['building_label', 'building_code'],
        value_vars=['vol_tech_l', 'vol_econ_l', 'vol_env_l', 'vol_topsis_l'],
        var_name='criterio', value_name='volume_l'
    )
    df_opt_melt['volume_m3'] = df_opt_melt['volume_l'] / 1e3
    crit_map = {
        'vol_tech_l': '1. Ótimo Técnico (Δ ≤ 2.5 %/m³)',
        'vol_econ_l': '2. Ótimo Econômico (Max VPL R$)',
        'vol_topsis_l': '3. Compromisso TOPSIS (Multicritério)',
        'vol_env_l': '4. Ótimo Ambiental (Max CO₂ Evitado)'
    }
    df_opt_melt['criterio_lbl'] = df_opt_melt['criterio'].map(crit_map)

    sns.barplot(data=df_opt_melt, x='building_label', y='volume_m3', hue='criterio_lbl', palette='Set1', ax=axes[0], edgecolor='black', alpha=0.9)
    axes[0].set_title('A) Capacidade Média Recomendada (m³) por Critério de Otimização', fontweight='bold')
    axes[0].set_xlabel('Tipologia Edilícia', fontweight='bold')
    axes[0].set_ylabel('Volume Ótimo de Cisterna (m³)', fontweight='bold')
    axes[0].legend(title='Critério de Dimensionamento', loc='upper left')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Mostrando TODAS as 5 tipologias nos boxplots (UTI, UTG, MSG, MFH, MFL)
    sns.boxplot(data=df_opt_melt, x='building_label', y='volume_m3', hue='criterio_lbl', palette='Set1', ax=axes[1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[1].set_title('B) Dispersão das Capacidades Ótimas nas 5 Tipologias Residenciais', fontweight='bold')
    axes[1].set_xlabel('Tipologia Edilícia', fontweight='bold')
    axes[1].set_ylabel('Volume Ótimo de Cisterna (m³)', fontweight='bold')
    axes[1].legend(title='Critério', loc='upper left')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 3.1 — Comparação Estrutural entre os Volumes Ótimos Técnico (Δ ≤ 2.5 %/m³), Econômico, Ambiental e Multicritério", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig3_1_path = os.path.join(CAP3_DIR, "fig3_1_comparacao_volumes_otimos_3_criterios.png")
    plt.savefig(fig3_1_path)
    plt.close()

    # Fig 3.2: Mapa Tríplice dos Volumes Ótimos com Bins Discretos
    print("[+] 3.2 Mapa Tríplice da Distribuição de Volumes Ótimos pelo Brasil com Bins...")
    city_opt_summary = df_optima.groupby(['city_clean', 'lat', 'lon'], observed=True).agg({
        'vol_tech_l': 'mean', 'vol_econ_l': 'mean', 'vol_env_l': 'mean', 'vol_topsis_l': 'mean'
    }).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(21, 6.5))
    bins_vols = [0, 1.5, 3.0, 5.0, 7.5, 10.0, 15.0, 25.0]

    plot_brazil_basemap(axes[0], states_gdf)
    plot_binned_scatter(axes[0], city_opt_summary['lon'], city_opt_summary['lat'], city_opt_summary['vol_tech_l']/1e3, bins_vols, 'Blues', 'Vol Técnico (m³)', fig, cbar_fmt="{:g}")
    axes[0].set_title('A) Ótimo Técnico (Δ ≤ 2.5 %/m³)', fontweight='bold')

    plot_brazil_basemap(axes[1], states_gdf)
    plot_binned_scatter(axes[1], city_opt_summary['lon'], city_opt_summary['lat'], city_opt_summary['vol_econ_l']/1e3, bins_vols, 'YlGn', 'Vol Econômico (m³)', fig, cbar_fmt="{:g}")
    axes[1].set_title('B) Ótimo Econômico (Max VPL R$)', fontweight='bold')

    plot_brazil_basemap(axes[2], states_gdf)
    plot_binned_scatter(axes[2], city_opt_summary['lon'], city_opt_summary['lat'], city_opt_summary['vol_env_l']/1e3, bins_vols, 'Purples', 'Vol Ambiental (m³)', fig, cbar_fmt="{:g}")
    axes[2].set_title('C) Ótimo Ambiental (Max CO₂ Evitado)', fontweight='bold')

    plt.suptitle("Figura 3.2 — Panorama Cartográfico Brasileiro dos Volumes Ótimos sob Critérios Técnico, Econômico e Ambiental", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig3_2_path = os.path.join(CAP3_DIR, "fig3_2_mapa_triplice_volumes_otimos_brasil.png")
    plt.savefig(fig3_2_path)
    plt.close()

    # Fig 3.3: Fronteira de Pareto e Trade-off Multicritério
    print("[+] 3.3 Fronteira de Pareto e Trade-off Multicritério...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sample_pareto_uti = df_sample[df_sample['building_code'] == 'UTI'].sample(min(8000, len(df_sample[df_sample['building_code'] == 'UTI'])), random_state=42)
    sc_p1 = auto_binned_scatter(axes[0], sample_pareto_uti['lifetime_net_co2_saved_kg'], sample_pareto_uti['vpl_brl']/1e3, sample_pareto_uti['potential_savings_pct'], s=50, alpha=0.65)
    axes[0].set_title('A) Trade-off VPL vs CO₂ vs Economia % — UTI (4 hab)', fontweight='bold')
    axes[0].set_xlabel('CO₂ Líquido Evitado na Vida Útil (kg CO₂-eq)', fontweight='bold')
    axes[0].set_ylabel('VPL Econômico (mil R$)', fontweight='bold')
    cb_p1 = fig.colorbar(sc_p1, ax=axes[0], fraction=0.046, pad=0.04)
    cb_p1.set_label('Economia Pluvial (%)', fontweight='bold')
    axes[0].axhline(0, color='red', linestyle='--', linewidth=1)
    axes[0].axvline(0, color='red', linestyle='--', linewidth=1)
    axes[0].grid(True, linestyle='--', alpha=0.5)

    sample_pareto_mfl = df_sample[df_sample['building_code'] == 'MFL'].sample(min(8000, len(df_sample[df_sample['building_code'] == 'MFL'])), random_state=42)
    sc_p2 = auto_binned_scatter(axes[1], sample_pareto_mfl['lifetime_net_co2_saved_kg']/1e3, sample_pareto_mfl['vpl_brl']/1e3, sample_pareto_mfl['potential_savings_pct'], s=50, alpha=0.65)
    axes[1].set_title('B) Trade-off VPL vs CO₂ vs Economia % — MFL (128 hab)', fontweight='bold')
    axes[1].set_xlabel('CO₂ Líquido Evitado na Vida Útil (ton CO₂-eq)', fontweight='bold')
    axes[1].set_ylabel('VPL Econômico (mil R$)', fontweight='bold')
    cb_p2 = fig.colorbar(sc_p2, ax=axes[1], fraction=0.046, pad=0.04)
    cb_p2.set_label('Economia Pluvial (%)', fontweight='bold')
    axes[1].axhline(0, color='red', linestyle='--', linewidth=1)
    axes[1].axvline(0, color='red', linestyle='--', linewidth=1)
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 3.3 — Fronteira de Decisão e Espaço de Trade-off Multicritério (Econômico vs Ambiental vs Técnico)", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig3_3_path = os.path.join(CAP3_DIR, "fig3_3_fronteira_pareto_tradeoff_multicriterio.png")
    plt.savefig(fig3_3_path)
    plt.close()

    # Fig 3.4: Penalidade e Custo de Oportunidade entre Critérios
    print("[+] 3.4 Penalidade e Custo de Oportunidade ao Escolher Cada Critério...")
    df_optima['perda_vpl_se_adota_env'] = (df_optima['vpl_opt_econ'] - df_optima['vpl_opt_env']) / 1e3
    df_optima['perda_co2_se_adota_econ'] = df_optima['co2_opt_env'] - df_optima['co2_opt_econ']
    df_optima['perda_vpl_se_adota_tech'] = (df_optima['vpl_opt_econ'] - df_optima['vpl_opt_tech']) / 1e3

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(data=df_optima, x='building_label', y='perda_vpl_se_adota_tech', hue='building_label', palette='Reds', legend=False, ax=axes[0], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[0].set_title('A) Penalidade Financeira: Perda de VPL (kR$) ao Adotar o Ótimo Técnico Puro', fontweight='bold')
    axes[0].set_xlabel('Tipologia Edilícia', fontweight='bold')
    axes[0].set_ylabel('Perda de VPL Financeiro (mil R$)', fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    sns.boxplot(data=df_optima, x='building_label', y='perda_co2_se_adota_econ', hue='building_label', palette='Purples', legend=False, ax=axes[1], showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
    axes[1].set_title('B) Custo Ambiental: Emissões Evitadas Perdidas (kg CO₂) ao Priorizar o VPL Máximo', fontweight='bold')
    axes[1].set_xlabel('Tipologia Edilícia', fontweight='bold')
    axes[1].set_ylabel('CO₂ Deixado de Evitar (kg CO₂-eq)', fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 3.4 — Custo de Oportunidade e Penalidades Cruzadas na Escolha de Dimensionamento", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig3_4_path = os.path.join(CAP3_DIR, "fig3_4_penalidade_perda_escolha_otimo.png")
    plt.savefig(fig3_4_path)
    plt.close()

    # ==============================================================================================
    # CAPÍTULO 4: LOCAIS COM PIORES RESULTADOS NO BRASIL (3 FIGURAS)
    # ==============================================================================================
    print("\n" + "="*80)
    print("GERANDO CAPÍTULO 4: LOCAIS COM PIORES RESULTADOS NO BRASIL (3 FIGURAS)")
    print("="*80)

    # Identificação exata dos municípios e cálculo do Índice de Excelência e Atratividade Pluvial
    city_perf = df_best.groupby(['city_clean', 'uf', 'region', 'lat', 'lon'], observed=True).agg({
        'potential_savings_pct': 'mean',
        'vpl_brl': 'mean',
        'payback_years': lambda x: np.median(x[x > 0]) if len(x[x > 0]) > 0 else 99.0,
        'lifetime_net_co2_saved_kg': 'mean',
        'tarifa_agua_base_r_m3': 'first',
        'tarifa_eletricidade_b1_r_kwh': 'first'
    }).reset_index()

    def min_max_norm(s):
        return (s - s.min()) / (s.max() - s.min() + 1e-9)

    city_perf['score_sav'] = min_max_norm(city_perf['potential_savings_pct'])
    city_perf['score_vpl'] = min_max_norm(city_perf['vpl_brl'])
    city_perf['score_co2'] = min_max_norm(city_perf['lifetime_net_co2_saved_kg'])
    city_perf['score_payback'] = 1.0 - min_max_norm(city_perf['payback_years'].clip(upper=30))
    city_perf['performance_index'] = (0.35 * city_perf['score_sav'] + 0.35 * city_perf['score_vpl'] + 0.15 * city_perf['score_co2'] + 0.15 * city_perf['score_payback']) * 100.0

    worst_20_sav = city_perf.sort_values(by='potential_savings_pct', ascending=True).head(20)
    worst_20_vpl = city_perf.sort_values(by='vpl_brl', ascending=True).head(20)
    worst_20_composite = city_perf.sort_values(by='performance_index', ascending=True).head(20)

    # Fig 4.1: Mapa Cartográfico dos Piores Resultados com Bins
    print("[+] 4.1 Mapa dos Piores Resultados no Brasil com Bins Discretos...")
    fig, axes = plt.subplots(1, 2, figsize=(17, 7))
    plot_brazil_basemap(axes[0], states_gdf)
    bins_idx = [0, 20, 35, 50, 65, 80, 100]
    plot_binned_scatter(axes[0], city_perf['lon'], city_perf['lat'], city_perf['performance_index'], bins_idx, 'YlOrRd_r', 'Índice de Atratividade (0-100)', fig, cbar_fmt="{:.0f}")
    axes[0].set_title('A) Faixas do Índice de Atratividade Pluvial (Menor = Pior)', fontweight='bold')

    worst_15 = worst_20_composite.head(15)
    axes[0].scatter(worst_15['lon'], worst_15['lat'], color='black', s=80, marker='x', linewidths=2.0, zorder=6, label='Top 15 Piores Cidades')
    for _, r_w in worst_15.head(8).iterrows():
        axes[0].text(r_w['lon'] + 0.5, r_w['lat'], f"{r_w['city_clean']}/{r_w['uf']}", fontsize=8, fontweight='bold', color='darkred', zorder=7)
    axes[0].legend(loc='lower left')

    plot_brazil_basemap(axes[1], states_gdf)
    bins_vpl_map = [-10, 0, 15, 30, 50, 80, 150]
    plot_binned_scatter(axes[1], city_perf['lon'], city_perf['lat'], city_perf['vpl_brl']/1e3, bins_vpl_map, 'coolwarm_r', 'VPL Médio (mil R$)', fig, cbar_fmt="{:g}")
    axes[1].set_title('B) Faixas de VPL Médio (mil R$) — Hotspots de Inviabilidade', fontweight='bold')

    plt.suptitle("Figura 4.1 — Mapeamento Espacial dos Municípios com Piores Resultados e Vulnerabilidade Pluvial no Brasil", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig4_1_path = os.path.join(CAP4_DIR, "fig4_1_mapa_piores_resultados_brasil.png")
    plt.savefig(fig4_1_path)
    plt.close()

    # Fig 4.2: Ranking dos 20 Piores Municípios do Brasil
    print("[+] 4.2 Ranking dos 20 Piores Municípios...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    worst_20_sav_plot = worst_20_sav.iloc[::-1]
    y_pos = np.arange(len(worst_20_sav_plot))
    axes[0].barh(y_pos, worst_20_sav_plot['potential_savings_pct'], color='#d73027', edgecolor='black', alpha=0.88)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([f"{r['city_clean']} ({r['uf']})" for _, r in worst_20_sav_plot.iterrows()], fontsize=9, fontweight='bold')
    axes[0].set_title('A) 20 Municípios com Menor Economia Pluvial (%)', fontweight='bold')
    axes[0].set_xlabel('Economia Pluvial Média (%)', fontweight='bold')
    for i, (_, r) in enumerate(worst_20_sav_plot.iterrows()):
        axes[0].text(r['potential_savings_pct'] + 0.15, i, f"{r['potential_savings_pct']:.1f}%", va='center', fontsize=8.5, fontweight='bold')

    worst_20_vpl_plot = worst_20_vpl.iloc[::-1]
    axes[1].barh(y_pos, worst_20_vpl_plot['vpl_brl']/1e3, color='#e08214', edgecolor='black', alpha=0.88)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels([f"{r['city_clean']} ({r['uf']})" for _, r in worst_20_vpl_plot.iterrows()], fontsize=9, fontweight='bold')
    axes[1].set_title('B) 20 Municípios com Menor VPL Financeiro (mil R$)', fontweight='bold')
    axes[1].set_xlabel('VPL Financeiro Médio (mil R$)', fontweight='bold')
    for i, (_, r) in enumerate(worst_20_vpl_plot.iterrows()):
        val_k = r['vpl_brl']/1e3
        axes[1].text(val_k + (0.5 if val_k >= 0 else -1.5), i, f"R${val_k:.1f}k", va='center', fontsize=8.5, fontweight='bold')

    plt.suptitle("Figura 4.2 — Ranking dos 20 Piores Municípios Brasileiros por Eficiência Pluvial e Retorno Financeiro", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig4_2_path = os.path.join(CAP4_DIR, "fig4_2_ranking_20_piores_cidades_brasil.png")
    plt.savefig(fig4_2_path)
    plt.close()

    # Fig 4.3: Diagnóstico das Causas do Baixo Desempenho
    print("[+] 4.3 Diagnóstico das Causas de Baixo Desempenho...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sc_d1 = auto_binned_scatter(axes[0], city_perf['potential_savings_pct'], city_perf['tarifa_agua_base_r_m3'], city_perf['vpl_brl']/1e3, s=65, alpha=0.85, edgecolors='black', linewidths=0.2)
    axes[0].set_title('A) Relação: Economia Pluvial (%) vs Tarifa de Água (R$/m³)', fontweight='bold')
    axes[0].set_xlabel('Economia Pluvial Média (%)', fontweight='bold')
    axes[0].set_ylabel('Tarifa Base de Água (R$/m³)', fontweight='bold')
    cb_d1 = fig.colorbar(sc_d1, ax=axes[0], fraction=0.046, pad=0.04)
    cb_d1.set_label('VPL Médio (mil R$)', fontweight='bold')
    axes[0].axvline(10, color='red', linestyle='--', linewidth=1.2, label='Zona Crítica (Economia < 10%)')
    axes[0].axhline(3.5, color='orange', linestyle='--', linewidth=1.2, label='Tarifa Baixa (< R$ 3,50/m³)')
    axes[0].legend(loc='upper right')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    worst_100 = city_perf.sort_values(by='performance_index').head(100)
    sns.countplot(data=worst_100, x='region', hue='region', order=REG_ORDER, palette='Reds_r', legend=False, ax=axes[1], edgecolor='black')
    axes[1].set_title('B) Concentração Regional das 100 Cidades com Menor Desempenho', fontweight='bold')
    axes[1].set_xlabel('Macrorregião Brasileira', fontweight='bold')
    axes[1].set_ylabel('Número de Municípios no Top 100 Piores', fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5, axis='y')
    for p in axes[1].patches:
        axes[1].annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width()/2., p.get_height()), ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    plt.suptitle("Figura 4.3 — Diagnóstico Causal do Baixo Desempenho: Efeito Combinado de Clima e Estrutura Tarifária", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig4_3_path = os.path.join(CAP4_DIR, "fig4_3_diagnostico_causas_baixo_desempenho.png")
    plt.savefig(fig4_3_path)
    plt.close()

    # ==============================================================================================
    # CAPÍTULO 5: LOCAIS COM MELHORES RESULTADOS NO BRASIL (4 FIGURAS)
    # ==============================================================================================
    print("\n" + "="*80)
    print("GERANDO CAPÍTULO 5: LOCAIS COM MELHORES RESULTADOS NO BRASIL (4 FIGURAS)")
    print("="*80)

    best_20_sav = city_perf.sort_values(by='potential_savings_pct', ascending=False).head(20)
    best_20_vpl = city_perf.sort_values(by='vpl_brl', ascending=False).head(20)
    best_20_composite = city_perf.sort_values(by='performance_index', ascending=False).head(20)

    # Fig 5.1: Mapa Cartográfico dos Melhores Resultados com Bins
    print("[+] 5.1 Mapa dos Melhores Resultados no Brasil com Bins Discretos...")
    fig, axes = plt.subplots(1, 2, figsize=(17, 7))
    plot_brazil_basemap(axes[0], states_gdf)
    bins_perf = [0, 30, 45, 60, 75, 85, 100]
    plot_binned_scatter(axes[0], city_perf['lon'], city_perf['lat'], city_perf['performance_index'], bins_perf, 'YlGn', 'Índice de Desempenho (0-100)', fig, cbar_fmt="{:.0f}")
    axes[0].set_title('A) Faixas do Índice de Excelência e Atratividade Pluvial (0 a 100)', fontweight='bold')

    best_15 = best_20_composite.head(15)
    axes[0].scatter(best_15['lon'], best_15['lat'], color='darkgreen', s=80, marker='*', edgecolors='black', linewidths=0.5, zorder=6, label='Top 15 Melhores Cidades')
    for _, r_b in best_15.head(8).iterrows():
        axes[0].text(r_b['lon'] + 0.5, r_b['lat'], f"{r_b['city_clean']}/{r_b['uf']}", fontsize=8, fontweight='bold', color='darkgreen', zorder=7)
    axes[0].legend(loc='lower left')

    plot_brazil_basemap(axes[1], states_gdf)
    bins_sav_map = [0, 5, 10, 15, 20, 25, 35]
    plot_binned_scatter(axes[1], city_perf['lon'], city_perf['lat'], city_perf['potential_savings_pct'], bins_sav_map, 'Blues', 'Economia Pluvial (%)', fig, cbar_fmt="{:g}")
    axes[1].set_title('B) Faixas do Potencial Médio de Economia de Água Pluvial (%)', fontweight='bold')

    plt.suptitle("Figura 5.1 — Mapeamento Espacial dos Municípios de Maior Excelência e Potencial Pluvial no Brasil", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig5_1_path = os.path.join(CAP5_DIR, "fig5_1_mapa_melhores_resultados_brasil.png")
    plt.savefig(fig5_1_path)
    plt.close()

    # Fig 5.2: Ranking dos 20 Melhores Municípios do Brasil
    print("[+] 5.2 Ranking dos 20 Melhores Municípios...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    best_20_sav_plot = best_20_sav.iloc[::-1]
    y_pos = np.arange(len(best_20_sav_plot))
    axes[0].barh(y_pos, best_20_sav_plot['potential_savings_pct'], color='#1a9850', edgecolor='black', alpha=0.88)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels([f"{r['city_clean']} ({r['uf']})" for _, r in best_20_sav_plot.iterrows()], fontsize=9, fontweight='bold')
    axes[0].set_title('A) 20 Municípios com Maior Economia Pluvial (%)', fontweight='bold')
    axes[0].set_xlabel('Economia Pluvial Média (%)', fontweight='bold')
    for i, (_, r) in enumerate(best_20_sav_plot.iterrows()):
        axes[0].text(r['potential_savings_pct'] + 0.15, i, f"{r['potential_savings_pct']:.1f}%", va='center', fontsize=8.5, fontweight='bold')

    best_20_vpl_plot = best_20_vpl.iloc[::-1]
    axes[1].barh(y_pos, best_20_vpl_plot['vpl_brl']/1e3, color='#4575b4', edgecolor='black', alpha=0.88)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels([f"{r['city_clean']} ({r['uf']})" for _, r in best_20_vpl_plot.iterrows()], fontsize=9, fontweight='bold')
    axes[1].set_title('B) 20 Municípios com Maior VPL Financeiro (mil R$)', fontweight='bold')
    axes[1].set_xlabel('VPL Financeiro Médio (mil R$)', fontweight='bold')
    for i, (_, r) in enumerate(best_20_vpl_plot.iterrows()):
        val_k = r['vpl_brl']/1e3
        axes[1].text(val_k + 0.5, i, f"R${val_k:.1f}k", va='center', fontsize=8.5, fontweight='bold')

    plt.suptitle("Figura 5.2 — Ranking dos 20 Melhores Municípios Brasileiros por Economia de Água e Retorno Financeiro", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig5_2_path = os.path.join(CAP5_DIR, "fig5_2_ranking_20_melhores_cidades_brasil.png")
    plt.savefig(fig5_2_path)
    plt.close()

    # Fig 5.3: Comparação de Estudos de Caso Arquetípicos
    print("[+] 5.3 Comparação de Estudos de Caso Arquetípicos...")
    selected_cities = []
    for c_name in ['Joinville', 'Manaus', 'Curitiba', 'Petrolina', 'Juazeiro', 'Mossoro']:
        match = df_best[df_best['city_clean'].str.contains(c_name, case=False, na=False)]
        if not match.empty:
            selected_cities.append(match['city_clean'].iloc[0])

    selected_cities = list(dict.fromkeys(selected_cities))[:4]
    df_arq = df_best[df_best['city_clean'].isin(selected_cities)].copy()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.barplot(data=df_arq, x='city_clean', y='potential_savings_pct', hue='building_label', palette='Set2', ax=axes[0], edgecolor='black')
    axes[0].set_title('A) Economia Pluvial (%) por Tipologia nos Municípios Arquetípicos', fontweight='bold')
    axes[0].set_xlabel('Município Selecionado', fontweight='bold')
    axes[0].set_ylabel('Economia Pluvial Média (%)', fontweight='bold')
    axes[0].legend(title='Tipologia', loc='upper right')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    df_arq['vpl_kbrl'] = df_arq['vpl_brl'] / 1e3
    sns.barplot(data=df_arq, x='city_clean', y='vpl_kbrl', hue='building_label', palette='Set2', ax=axes[1], edgecolor='black')
    axes[1].set_title('B) VPL Financeiro Médio (mil R$) nos Municípios Arquetípicos', fontweight='bold')
    axes[1].set_xlabel('Município Selecionado', fontweight='bold')
    axes[1].set_ylabel('VPL Financeiro (mil R$)', fontweight='bold')
    axes[1].legend(title='Tipologia', loc='upper left')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle("Figura 5.3 — Contraste Arquetípico: Comparação de Desempenho entre Municípios de Alto e Baixo Desempenho", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig5_3_path = os.path.join(CAP5_DIR, "fig5_3_comparacao_estudos_caso_arquetipicos.png")
    plt.savefig(fig5_3_path)
    plt.close()

    # Fig 5.4: Panorama Cartográfico Nacional Consolidado com Bins
    print("[+] 5.4 Panorama Nacional Consolidado com Bins Discretos (Grid 2x2)...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # A) Economia Pluvial (%) com Bins
    plot_brazil_basemap(axes[0, 0], states_gdf)
    bins_sav_all = [0, 5, 10, 15, 20, 25, 35]
    plot_binned_scatter(axes[0, 0], city_perf["lon"], city_perf["lat"], city_perf["potential_savings_pct"], bins_sav_all, "Blues", "Economia Pluvial (%)", fig, cbar_fmt="{:g}")
    axes[0, 0].set_title("A) Potencial Médio de Economia de Água Pluvial (%)", fontweight='bold')

    # B) VPL Financeiro (kR$) com Bins
    plot_brazil_basemap(axes[0, 1], states_gdf)
    bins_vpl_all = [-10, 0, 15, 35, 75, 150, 300]
    plot_binned_scatter(axes[0, 1], city_perf["lon"], city_perf["lat"], city_perf["vpl_brl"]/1e3, bins_vpl_all, "YlGn", "VPL (kR$)", fig, cbar_fmt="{:g}")
    axes[0, 1].set_title("B) Valor Presente Líquido - VPL Médio (mil R$)", fontweight='bold')

    # C) CO2 Líquido Evitado com Bins
    plot_brazil_basemap(axes[1, 0], states_gdf)
    bins_co2_all = [-200, 0, 100, 250, 500, 1000, 2000]
    plot_binned_scatter(axes[1, 0], city_perf["lon"], city_perf["lat"], city_perf["lifetime_net_co2_saved_kg"], bins_co2_all, "PuBuGn", "CO₂ Evitado (kg)", fig, cbar_fmt="{:g}")
    axes[1, 0].set_title("C) CO₂ Líquido Evitado na Vida Útil (kg CO₂-eq)", fontweight='bold')

    # D) Payback com Bins
    plot_brazil_basemap(axes[1, 1], states_gdf)
    bins_pay_all = [0, 2.0, 4.0, 7.0, 12.0, 20.0, 30.0]
    plot_binned_scatter(axes[1, 1], city_perf["lon"], city_perf["lat"], city_perf["payback_years"].clip(upper=30), bins_pay_all, "Spectral_r", "Payback (Anos)", fig, cbar_fmt="{:g}")
    axes[1, 1].set_title("D) Tempo de Retorno Descontado - Payback (Anos)", fontweight='bold')

    for cap, (c_lon, c_lat) in capitals.items():
        for r_ax in axes:
            for ax in r_ax:
                ax.plot(c_lon, c_lat, marker='*', color='red', markersize=7, zorder=5)
                ax.text(c_lon + 0.6, c_lat, cap, fontsize=7.5, fontweight='bold', zorder=6)

    plt.suptitle("Figura 5.4 — Panorama Cartográfico Integrado de Desempenho e Viabilidade no Brasil (652 Municípios)", fontweight='bold', fontsize=13.5, y=0.98)
    plt.tight_layout()
    fig5_4_path = os.path.join(CAP5_DIR, "fig5_4_panorama_nacional_consolidado_brasil.png")
    plt.savefig(fig5_4_path)
    plt.close()

    # ==============================================================================================
    # COMPILAÇÃO DO RELATÓRIO CONSOLIDADO DO ARTIGO V1
    # ==============================================================================================
    print("\n" + "="*80)
    print("COMPILANDO RELATÓRIO CONSOLIDADO DO ARTIGO V1...")
    print("="*80)

    def fmt_br(val, decimals=2):
        if pd.isna(val):
            return "-"
        s = f"{val:,.{decimals}f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")

    # Tabela 1: Estatísticas Descritivas por Tipologia
    stats_rows = []
    for typ in TYPOLOGY_ORDER:
        sub = df_best[df_best["building_label"] == typ]
        for col_name, label in [("potential_savings_pct", "Economia Pluvial (%)"),
                                ("vpl_brl", "VPL Econômico (R$)"),
                                ("lifetime_net_co2_saved_kg", "CO2 Evitado Vida Útil (kg)"),
                                ("lower_tank_vol_l", "Volume Ótimo de Cisterna (L)"),
                                ("payback_years", "Payback (Anos)"),
                                ("annual_water_savings_brl", "Economia Anual de Água (R$/ano)")]:
            vals = sub[col_name].dropna().values
            if len(vals) > 0:
                stats_rows.append({
                    "Tipologia": typ,
                    "Indicador": label,
                    "Média": np.mean(vals),
                    "Desvio Padrão": np.std(vals),
                    "Mediana (P50)": np.median(vals),
                    "P25 (Q1)": np.percentile(vals, 25),
                    "P75 (Q3)": np.percentile(vals, 75),
                    "P5": np.percentile(vals, 5),
                    "P95": np.percentile(vals, 95)
                })
    df_desc = pd.DataFrame(stats_rows)

    # Tabela 2: Custo de Ciclo de Vida a 20 Anos (LCC): Concessionária 100% vs Netuno
    lcc_table_rows = []
    for typ in TYPOLOGY_ORDER:
        sub_lcc = df_best[df_best["building_label"] == typ]
        lcc_table_rows.append({
            'Tipologia': typ,
            'LCC 100% Concessionária (R$)': sub_lcc['lcc_baseline_kbrl'].mean() * 1e3,
            'Fatura Residual Água (R$)': sub_lcc['lcc_residual_water_kbrl'].mean() * 1e3,
            'OPEX Acumulado 20a (R$)': sub_lcc['lcc_opex_kbrl'].mean() * 1e3,
            'CAPEX Inicial (R$)': sub_lcc['lcc_capex_kbrl'].mean() * 1e3,
            'LCC Total com Netuno (R$)': sub_lcc['lcc_netuno_total_kbrl'].mean() * 1e3,
            'Economia Líquida / VPL (R$)': sub_lcc['vpl_brl'].mean()
        })
    df_lcc_table = pd.DataFrame(lcc_table_rows)

    # Tabela 3: Comparação dos 4 Ótimos por Tipologia com Limiar Técnico 2.5 %/m3
    opt_table_rows = []
    for typ in TYPOLOGY_ORDER:
        sub_opt = df_optima[df_optima['building_label'] == typ]
        opt_table_rows.append({
            'Tipologia': typ,
            'Vol Técnico (Δ ≤ 2.5 %/m³)': sub_opt['vol_tech_l'].mean() / 1e3,
            'Vol Econômico (Max VPL)': sub_opt['vol_econ_l'].mean() / 1e3,
            'Vol TOPSIS (Compromisso)': sub_opt['vol_topsis_l'].mean() / 1e3,
            'Vol Ambiental (Max CO₂)': sub_opt['vol_env_l'].mean() / 1e3,
            'VPL Ótimo Econômico (R$)': sub_opt['vpl_opt_econ'].mean(),
            'CO₂ Ótimo Ambiental (kg)': sub_opt['co2_opt_env'].mean()
        })
    df_opt_table = pd.DataFrame(opt_table_rows)

    rep = [
        "# Relatório Consolidado de Resultados e Figuras Científicas — Artigo V1",
        "",
        f"**Estudo:** Dimensionamento e Viabilidade de Sistemas de Aproveitamento Pluvial sob Mudanças Climáticas CMIP6",
        f"**Base de Dados Analisada:** `{PARQUET_PATH}`",
        f"**Total de Simulações Diárias do Estudo:** {total_rows:,} registros",
        f"**Amostra Estratificada Representativa:** {len(df_sample):,} registros | **Simulações Ótimas Avaliadas:** {len(df_optima):,}",
        f"**Abrangência:** 652 Municípios Brasileiros com população >= 50.000 habitantes (100% com tarifas homologadas)",
        r"**Limiar Ótimo Técnico Aplicado:** $\Delta \le 2.5\%/\text{m}^3$ (Critério do Volume Ideal — Eq. 4.8 do manual do Netuno)",
        f"**Data da Geração:** {time.strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "---",
        "",
        "## Estrutura dos Capítulos do Artigo V1",
        "",
        "1. [Capítulo 1: Panorama Geral e Desempenho Base das Tipologias](#capítulo-1-panorama-geral-e-desempenho-base-das-tipologias)",
        "2. [Capítulo 2: Aumento dos Reservatórios Ótimos em Cenários Futuros](#capítulo-2-aumento-dos-reservatórios-ótimos-em-cenários-futuros)",
        "3. [Capítulo 3: Comparação entre os Reservatórios Ótimos Ambiental, Econômico e Técnico](#capítulo-3-comparação-entre-os-reservatórios-ótimos-ambiental-econômico-e-técnico)",
        "4. [Capítulo 4: Locais com Piores Resultados no Brasil](#capítulo-4-locais-com-piores-resultados-no-brasil)",
        "5. [Capítulo 5: Locais com Melhores Resultados no Brasil](#capítulo-5-locais-com-melhores-resultados-no-brasil)",
        "6. [Fundamentação Metodológica: O que é o Índice de Excelência e Atratividade Pluvial?](#fundamentação-metodológica-o-que-é-o-índice-de-excelência-e-atratividade-pluvial)",
        "",
        "---",
        "",
        "## Capítulo 1: Panorama Geral e Desempenho Base das Tipologias",
        "",
        "Este capítulo apresenta o diagnóstico abrangente das 5 tipologias residenciais (UTI, UTG, MSG, MFH e MFL) sob condições climáticas observadas e projetadas, analisando a importância de parâmetros físicos e tarifários, saturação de armazenamento, sensibilidade financeira e contraste com o cenário de referência (100% concessionária).",
        "",
        "### Tabela 1.1 — Sumário Estatístico Descritivo das 5 Tipologias Residenciais",
        "",
        "| Tipologia | Indicador | Média | Desvio Padrão | Mediana (P50) | P25 (Q1) | P75 (Q3) | P5 | P95 |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    for _, r in df_desc.iterrows():
        rep.append(f"| **{r['Tipologia']}** | {r['Indicador']} | {fmt_br(r['Média'])} | {fmt_br(r['Desvio Padrão'])} | {fmt_br(r['Mediana (P50)'])} | {fmt_br(r['P25 (Q1)'])} | {fmt_br(r['P75 (Q3)'])} | {fmt_br(r['P5'])} | {fmt_br(r['P95'])} |")

    rep.extend([
        "",
        "### Tabela 1.2 — Análise de Custo de Ciclo de Vida a 20 Anos (LCC): Cenário 100% Concessionária vs Sistema Netuno",
        "",
        "| Tipologia | LCC 100% Concessionária (R$) | Fatura Residual Água (R$) | OPEX Acumulado 20a (R$) | CAPEX Inicial (R$) | LCC Total com Netuno (R$) | Economia Líquida / VPL (R$) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for _, r in df_lcc_table.iterrows():
        rep.append(f"| **{r['Tipologia']}** | R$ {fmt_br(r['LCC 100% Concessionária (R$)'])} | R$ {fmt_br(r['Fatura Residual Água (R$)'])} | R$ {fmt_br(r['OPEX Acumulado 20a (R$)'])} | R$ {fmt_br(r['CAPEX Inicial (R$)'])} | R$ {fmt_br(r['LCC Total com Netuno (R$)'])} | R$ {fmt_br(r['Economia Líquida / VPL (R$)'])} |")

    rep.extend([
        "",
        "### Catálogo de Figuras do Capítulo 1:",
        f"1. **Figura 1.1 — Importância Global de Parâmetros e Variáveis Consequentes (RF Gini %):** [`fig1_1_importancia_parametros_rf.png`](file:///{fig1_1_path.replace(os.sep, '/')})",
        f"2. **Figura 1.2 — Boxplots Comparativos de Desempenho Multi-Indicador:** [`fig1_2_boxplots_indicadores_5_tipologias.png`](file:///{fig1_2_path.replace(os.sep, '/')})",
        f"3. **Figura 1.3 — Curvas de Saturação de Reservatório e Eficiência Marginal:** [`fig1_3_curvas_saturacao_eficiencia_marginal.png`](file:///{fig1_3_path.replace(os.sep, '/')})",
        f"4. **Figura 1.4 — Matriz de Calor (Heatmaps) Tipologia vs Horizonte:** [`fig1_4_heatmaps_tipologia_vs_horizonte.png`](file:///{fig1_4_path.replace(os.sep, '/')})",
        f"5. **Figura 1.5 — Avaliação Financeira, CAPEX vs Economia vs Cenário 100% Concessionária:** [`fig1_5_viabilidade_financeira_payback_capex.png`](file:///{fig1_5_path.replace(os.sep, '/')})",
        f"6. **Figura 1.6 — Decomposição de Custo de Ciclo de Vida a 20 Anos (LCC):** [`fig1_6_decomposicao_economica_custos_beneficios.png`](file:///{fig1_6_path.replace(os.sep, '/')})",
        f"7. **Figura 1.7 — Panorama Tarifário Nacional de Água e Energia Elétrica (Bins Discretos):** [`fig1_7_panorama_tarifario_nacional_energia_agua.png`](file:///{fig1_7_path.replace(os.sep, '/')})",
        f"8. **Figura 1.8 — Elasticidade Cruzada de Tarifas e Sensibilidade do VPL:** [`fig1_8_elasticidade_cruzada_tarifas_agua_energia.png`](file:///{fig1_8_path.replace(os.sep, '/')})",
        f"9. **Figura 1.9 — Ranking Estadual de Atratividade Financeira (27 UFs):** [`fig1_9_ranking_estadual_vpl_payback.png`](file:///{fig1_9_path.replace(os.sep, '/')})",
        f"10. **Figura 1.10 — Panorama das Alíquotas de Esgoto e Efeito Alavancador no VPL:** [`fig1_10_panorama_tarifas_esgoto_brasil.png`](file:///{fig1_10_path.replace(os.sep, '/')})",
        "",
        "### Diagnóstico Tarifário Específico: Paraná (SANEPAR / AGEPAR) e Panorama Nacional de Esgoto",
        "",
        "1. **Estrutura Tarifária do Paraná (34 Municípios Analisados):**",
        "   - **Prestador Regulado:** SANEPAR (homologado pela agência reguladora AGEPAR).",
        "   - **Tarifa Base de Água:** R$ 11,02/m³ (calculada com base no valor mínimo residencial de R$ 55,09 para a faixa básica de 5 m³).",
        "   - **Alíquota de Esgoto:** 80,0% sobre a conta de água na maioria dos municípios e 85,0% em Curitiba.",
        "   - **Tarifa Combinada Efetiva:** R$ 19,83/m³ (interior/RMC) e R$ 20,38/m³ (Curitiba).",
        "   - **Impacto no VPL:** Essa combinação de tarifa elevada com alta pluviosidade regular (1.400 a 1.900 mm/ano) posiciona o Paraná entre os estados de **maior retorno financeiro do Brasil** (VPL médio de R$ 35k a R$ 140k e payback de 2 a 4 anos).",
        "",
        "2. **Panorama Nacional das Alíquotas de Esgoto (% sobre a Conta de Água):**",
        "   - **Média Nacional:** 84,0% da conta de água (com desvio padrão de 10,2%).",
        "   - **Faixas mais frequentes:** 80% (61,3% das cidades — padrão de SANEPAR, COPASA, CASAN, EMBASA), 100% (24,5% das cidades — DF, RJ, PE, SP), 70% (9,0% das cidades — RN, MS, RO).",
        "   - **Efeito Alavancador no VPL:** A inclusão da cobrança de esgoto evitado é o que viabiliza economicamente o aproveitamento pluvial nas tipologias unifamiliares (ex: em UTG, o VPL médio passa de -R$ 1,0k para +R$ 8,1k, tornando o investimento atrativo).",
        "",
        "---",
        "",
        "## Capítulo 2: Aumento dos Reservatórios Ótimos em Cenários Futuros",
        "",
        "Análise detalhada do impacto das projeções climáticas CMIP6 (SSP2-4.5 e SSP5-8.5) sobre a necessidade de expansão de capacidade de armazenamento ao longo do século XXI.",
        "",
        "### Catálogo de Figuras do Capítulo 2:",
        f"1. **Figura 2.1 — Trajetórias Climáticas e Tendências Temporais (1980–2100):** [`fig2_1_trajetorias_climaticas_1980_2100.png`](file:///{fig2_1_path.replace(os.sep, '/')})",
        f"2. **Figura 2.2 — Frequência Relativa de Volumes Ótimos (Grid 2x5):** [`fig2_2_frequencia_volumes_otimos_grid_2x5.png`](file:///{fig2_2_path.replace(os.sep, '/')})",
        f"3. **Figura 2.3 — Dispersão e Incerteza entre Modelos Climáticos GCM (Bins Discretos):** [`fig2_3_dispersao_incerteza_modelos_gcm.png`](file:///{fig2_3_path.replace(os.sep, '/')})",
        f"4. **Figura 2.4 — Deslocamento Espacial e Regional de Capacidade ΔV (Bins Discretos):** [`fig2_4_deslocamento_capacidade_delta_v_mapa_e_regioes.png`](file:///{fig2_4_path.replace(os.sep, '/')})",
        f"5. **Figura 2.5 — Curvas de Distribuição Cumulativa (CDF) e Shift de Capacidade:** [`fig2_5_curvas_cumulativas_shift_reservatorios.png`](file:///{fig2_5_path.replace(os.sep, '/')})",
        "",
        "---",
        "",
        "## Capítulo 3: Comparação entre os Reservatórios Ótimos Ambiental, Econômico e Técnico",
        "",
        r"Comparação multidimensional com a aplicação do **Limiar Técnico Oficial Netuno ($\Delta \le 2.5\ \%/\text{m}^3$)** nas **5 Tipologias Residenciais (UTI, UTG, MSG, MFH, MFL)**:",
        r"- **Ótimo Técnico ($\Delta \le 2.5\ \%/\text{m}^3$):** Identifica o ponto onde o ganho marginal de água captada cai abaixo de 2,5 pontos percentuais por m³ adicional. Evita reservatórios superdimensionados e foca no rendimento útil da captação.",
        "- **Ótimo Econômico:** Maximiza o VPL considerando a relação de tarifas locais, custos de instalação e operação.",
        "- **Ótimo Ambiental:** Maximiza o balanço de carbono líquido evitado (kg CO₂-eq), favorecendo cisternas de altíssima rotação hídrica com menor pegada incorporada.",
        "- **Compromisso TOPSIS:** Solução de equilíbrio multicritério.",
        "",
        "### Tabela 3.1 — Comparação das Capacidades Ótimas Médias (m³) por Critério",
        "",
        "| Tipologia | Vol Técnico (Δ ≤ 2.5 %/m³) | Vol Econômico (Max VPL) | Vol TOPSIS (Compromisso) | Vol Ambiental (Max CO₂) | VPL Ótimo Econômico (R$) | CO₂ Ótimo Ambiental (kg) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for _, r in df_opt_table.iterrows():
        rep.append(f"| **{r['Tipologia']}** | {fmt_br(r['Vol Técnico (Δ ≤ 2.5 %/m³)'])} m³ | {fmt_br(r['Vol Econômico (Max VPL)'])} m³ | {fmt_br(r['Vol TOPSIS (Compromisso)'])} m³ | {fmt_br(r['Vol Ambiental (Max CO₂)'])} m³ | R$ {fmt_br(r['VPL Ótimo Econômico (R$)'])} | {fmt_br(r['CO₂ Ótimo Ambiental (kg)'])} kg |")

    rep.extend([
        "",
        "### Catálogo de Figuras do Capítulo 3:",
        f"1. **Figura 3.1 — Comparação Direta dos Volumes Ótimos nas 5 Tipologias (UTI, UTG, MSG, MFH, MFL):** [`fig3_1_comparacao_volumes_otimos_3_criterios.png`](file:///{fig3_1_path.replace(os.sep, '/')})",
        f"2. **Figura 3.2 — Mapa Tríplice da Distribuição Espacial dos Ótimos no Brasil (Bins Discretos):** [`fig3_2_mapa_triplice_volumes_otimos_brasil.png`](file:///{fig3_2_path.replace(os.sep, '/')})",
        f"3. **Figura 3.3 — Fronteira de Pareto e Trade-off Multicritério:** [`fig3_3_fronteira_pareto_tradeoff_multicriterio.png`](file:///{fig3_3_path.replace(os.sep, '/')})",
        f"4. **Figura 3.4 — Custo de Oportunidade e Penalidades Cruzadas:** [`fig3_4_penalidade_perda_escolha_otimo.png`](file:///{fig3_4_path.replace(os.sep, '/')})",
        "",
        "---",
        "",
        "## Capítulo 4: Locais com Piores Resultados no Brasil",
        "",
        "Identificação dos municípios brasileiros onde o aproveitamento de água de chuva enfrenta os maiores desafios hidrológicos e financeiros (Semiárido, certas áreas do Nordeste e Norte de Minas Gerais).",
        "",
        "### Tabela 4.1 — Top 10 Municípios com Menor Desempenho Integrado no Brasil",
        "",
        "| Município | UF | Região | Economia Pluvial Média (%) | VPL Médio Ótimo (R$) | Tarifa Base de Água (R$/m³) | Índice Composto (0-100) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for _, r in worst_20_composite.head(10).iterrows():
        rep.append(f"| **{r['city_clean']}** | {r['uf']} | {r['region']} | {fmt_br(r['potential_savings_pct'])}% | R$ {fmt_br(r['vpl_brl'])} | R$ {fmt_br(r['tarifa_agua_base_r_m3'])}/m³ | {fmt_br(r['performance_index'], 1)} |")

    rep.extend([
        "",
        "### Catálogo de Figuras do Capítulo 4:",
        f"1. **Figura 4.1 — Mapeamento Espacial dos Municípios com Piores Resultados (Bins Discretos):** [`fig4_1_mapa_piores_resultados_brasil.png`](file:///{fig4_1_path.replace(os.sep, '/')})",
        f"2. **Figura 4.2 — Ranking dos 20 Piores Municípios por Indicador:** [`fig4_2_ranking_20_piores_cidades_brasil.png`](file:///{fig4_2_path.replace(os.sep, '/')})",
        f"3. **Figura 4.3 — Diagnóstico Causal do Baixo Desempenho (Clima vs Tarifas):** [`fig4_3_diagnostico_causas_baixo_desempenho.png`](file:///{fig4_3_path.replace(os.sep, '/')})",
        "",
        "---",
        "",
        "## Capítulo 5: Locais com Melhores Resultados no Brasil",
        "",
        "Identificação dos polos de excelência nacional para aproveitamento pluvial predial, combinando regimes de chuvas abundantes e regulares com tarifas de água e esgoto que garantem alto retorno financeiro (Sul, Sudeste litorâneo e capitais do Norte).",
        "",
        "### Tabela 5.1 — Top 10 Municípios com Maior Desempenho Integrado no Brasil",
        "",
        "| Município | UF | Região | Economia Pluvial Média (%) | VPL Médio Ótimo (R$) | Tarifa Base de Água (R$/m³) | Índice Composto (0-100) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for _, r in best_20_composite.head(10).iterrows():
        rep.append(f"| **{r['city_clean']}** | {r['uf']} | {r['region']} | {fmt_br(r['potential_savings_pct'])}% | R$ {fmt_br(r['vpl_brl'])} | R$ {fmt_br(r['tarifa_agua_base_r_m3'])}/m³ | {fmt_br(r['performance_index'], 1)} |")

    rep.extend([
        "",
        "### Catálogo de Figuras do Capítulo 5:",
        f"1. **Figura 5.1 — Mapeamento Espacial dos Municípios de Maior Excelência (Bins Discretos):** [`fig5_1_mapa_melhores_resultados_brasil.png`](file:///{fig5_1_path.replace(os.sep, '/')})",
        f"2. **Figura 5.2 — Ranking dos 20 Melhores Municípios por Indicador:** [`fig5_2_ranking_20_melhores_cidades_brasil.png`](file:///{fig5_2_path.replace(os.sep, '/')})",
        f"3. **Figura 5.3 — Contraste Arquetípico entre Municípios de Alto e Baixo Desempenho:** [`fig5_3_comparacao_estudos_caso_arquetipicos.png`](file:///{fig5_3_path.replace(os.sep, '/')})",
        f"4. **Figura 5.4 — Panorama Cartográfico Integrado Nacional (Grid 2x2 com Bins):** [`fig5_4_panorama_nacional_consolidado_brasil.png`](file:///{fig5_4_path.replace(os.sep, '/')})",
        "",
        "---",
        "",
        "## Fundamentação Metodológica: O que é o Índice de Excelência e Atratividade Pluvial?",
        "",
        "O **Índice de Excelência e Atratividade Pluvial ($I_{atratividade}$)** é uma métrica sintética multicritério (adimensional, variando de **0 a 100**) desenvolvida para classificar de forma holística os 652 municípios brasileiros analisados.",
        "",
        "### Formulação Matemática:",
        r"$$I_{atratividade} = \left[ 0.35 \cdot \hat{S}_{pluvial} + 0.35 \cdot \hat{VPL} + 0.15 \cdot \hat{CO}_{2\text{ líquido}} + 0.15 \cdot (1 - \hat{PB}) \right] \times 100$$",
        "",
        "Onde cada termo representa a normalização Min-Max dos 4 pilares de desempenho do sistema:",
        r"1. **$\hat{S}_{pluvial}$ (Potencial de Economia Pluvial — Peso 35%):** Mede a eficiência hidrológica de suprimento da demanda não potável.",
        r"2. **$\hat{VPL}$ (Valor Presente Líquido — Peso 35%):** Mede a rentabilidade e atratividade financeira descontada a 20 anos frente às tarifas locais de água e esgoto.",
        r"3. **$\hat{CO}_{2\text{ líquido}}$ (Descarbonização Líquida Evitada — Peso 15%):** Mede o benefício ambiental líquido (kg CO₂-eq evitado no tratamento de água municipal deduzido das emissões incorporadas da cisterna e bombeamento).",
        r"4. **$(1 - \hat{PB})$ (Velocidade de Retorno do Investimento — Peso 15%):** Inverso do Payback descontado (penalizando tempos de retorno excessivos > 20-30 anos).",
        "",
        "---",
        "",
        "## Resumo Geral dos Arquivos Gerados na Pasta `ArtigoV1/`",
        "",
        "| Capítulo | Diretório | Quantidade de Figuras | Formato / Resolução |",
        "| :--- | :--- | :---: | :---: |",
        f"| **Capítulo 1** | `ArtigoV1/Cap1_Panorama_Geral_Tipologias/` | 10 figuras | PNG (300 DPI) |",
        f"| **Capítulo 2** | `ArtigoV1/Cap2_Aumento_Reservatorios_Futuro/` | 5 figuras | PNG (300 DPI) |",
        f"| **Capítulo 3** | `ArtigoV1/Cap3_Comparacao_Otimo_Ambiental_Economico_Tecnico/` | 4 figuras | PNG (300 DPI) |",
        f"| **Capítulo 4** | `ArtigoV1/Cap4_Piores_Resultados_Brasil/` | 3 figuras | PNG (300 DPI) |",
        f"| **Capítulo 5** | `ArtigoV1/Cap5_Melhores_Resultados_Brasil/` | 4 figuras | PNG (300 DPI) |",
        f"| **Total** | `ArtigoV1/` | **26 figuras** | **PNG (300 DPI)** |",
        ""
    ])

    final_lines = []
    t_blk = []
    for l in rep:
        if l.strip().startswith('|'):
            t_blk.append(l)
        else:
            if t_blk:
                final_lines.extend(format_table(t_blk))
                t_blk = []
            final_lines.append(l)
    if t_blk:
        final_lines.extend(format_table(t_blk))

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(final_lines) + "\n")

    print(f" [OK] Relatório Consolidado salvo com sucesso em: {REPORT_PATH}")
    print("=" * 100)
    print(f"[SUCESSO] TODAS AS 25 FIGURAS E RELATÓRIO DO ARTIGO V1 CONCLUÍDOS EM {time.time() - t_start:.2f} SEGUNDOS!")
    print("=" * 100)


if __name__ == "__main__":
    main()
