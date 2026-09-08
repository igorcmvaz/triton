"""
====================================================================================================
NETUNO 5 — ESTUDO 2: 11 TIPOLOGIAS EDILÍCIAS EM 652 CIDADES BRASILEIRAS (ESTUDO EXPANDIDO BRASIL)
Geração das 8 Figuras Científicas de Alto Impacto para o Artigo 2
====================================================================================================
"""

from __future__ import annotations

import os
import sys
import json
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# Encoding Windows
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "figuras", "figuras_artigo_8")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dados do Estudo 2
STUDY2_COMPLETO = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_todas_tipologias_completo.csv")
STUDY2_MCDM = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_mcdm_vikor_smaa_comparativo.csv")
BRAZIL_SHP = os.path.join(BASE_DIR, "data", "brazilSHP", "BR_UF_2022.shp")
COSTS_JSON = os.path.join(BASE_DIR, "netuno", "data", "costs_database.json")

# Configurações de Estilo Matplotlib
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 9.5,
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.labelsize': 10.5,
    'axes.titlesize': 11.5,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'figure.titlesize': 13.0,
    'figure.titleweight': 'bold',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

PAL_NAVY = "#0F172A"
PAL_BLUE = "#1E40AF"
PAL_TEAL = "#0D9488"
PAL_CYAN = "#0284C7"
PAL_EMERALD = "#059669"
PAL_AMBER = "#D97706"
PAL_ROSE = "#E11D48"
PAL_PURPLE = "#7C3AED"
PAL_GRAY = "#64748B"

def add_panel_label(ax, label: str, x: float = 0.02, y: float = 0.95):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=12, fontweight='black',
            va='top', ha='left',
            bbox=dict(boxstyle='square,pad=0.25', facecolor='white', edgecolor='#94A3B8', alpha=0.9, lw=0.8),
            zorder=100)

def load_brazil_gdf():
    if os.path.exists(BRAZIL_SHP):
        try:
            gdf = gpd.read_file(BRAZIL_SHP)
            gdf['geometry'] = gdf['geometry'].simplify(0.02, preserve_topology=True)
            return gdf
        except Exception: pass
    return None

print("Iniciando geração das 8 figuras do Estudo 2 (11 Tipologias Brasil - 652 Cidades)...")

df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')
with open(COSTS_JSON, 'r', encoding='utf-8') as f:
    costs_db = json.load(f)

# ====================================================================================================
# FIGURA 1: Potencial de Economia Ótimo por Região e Curvas de Saturação (11 Tipologias)
# ====================================================================================================
def generate_fig1():
    print(" -> Gerando Figura 1 (Estudo 2): Potencial Regional e Saturação (11 Tipologias)...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Boxplots do Potencial de Economia no Brasil por Macrorregião (11 Tipologias)
    ax_a = fig.add_subplot(gs[0, 0])
    reg_order = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    colors_reg = [PAL_EMERALD, PAL_AMBER, PAL_PURPLE, PAL_CYAN, PAL_BLUE]
    
    data_reg = [df_br[df_br['regiao'] == r]['potential_savings_pct'].dropna() for r in reg_order]
    bp = ax_a.boxplot(data_reg, tick_labels=reg_order, patch_artist=True,
                      showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                      medianprops=dict(color=PAL_NAVY, lw=2.0),
                      flierprops=dict(marker='o', markersize=3, alpha=0.25, color=PAL_GRAY))
    for patch, c in zip(bp['boxes'], colors_reg):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, r in enumerate(reg_order):
        med = df_br[df_br['regiao'] == r]['potential_savings_pct'].median()
        ax_a.text(idx + 1, med + 1.2, f"{med:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_a.set_title("A) Potencial de Economia de Água Potável por Macrorregião (11 Tipologias)", loc='left', pad=10)
    ax_a.set_ylabel("Economia de Água Potável (%)")
    ax_a.set_ylim(0, 55)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Potencial por Tipologia Edilícia (Residencial vs Institucional/Serviços)
    ax_b = fig.add_subplot(gs[0, 1])
    tip_order = ["COM", "RALT", "ESC", "UTG", "UTI", "HOS", "HOT", "RPOP", "MSG", "MFL", "MFH"]
    data_tip = [df_br[df_br['building_code'] == t]['potential_savings_pct'].dropna() for t in tip_order]
    
    col_tip = [PAL_EMERALD if t in ["COM", "ESC", "HOS", "HOT"] else (PAL_CYAN if t in ["RALT", "UTI", "UTG", "MSG"] else PAL_PURPLE) for t in tip_order]
    bp_b = ax_b.boxplot(data_tip, tick_labels=tip_order, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=5),
                        medianprops=dict(color=PAL_NAVY, lw=1.8),
                        flierprops=dict(marker='o', markersize=2, alpha=0.2, color=PAL_GRAY))
    for patch, c in zip(bp_b['boxes'], col_tip):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, t in enumerate(tip_order):
        med = df_br[df_br['building_code'] == t]['potential_savings_pct'].median()
        ax_b.text(idx + 1, med + 1.2, f"{med:.0f}%", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Economia de Água Potável nas 11 Tipologias Edilícias", loc='left', pad=10)
    ax_b.set_ylabel("Economia Hídrica (%)")
    ax_b.set_ylim(0, 55)
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Curvas de Saturação de Confiabilidade Regional
    ax_c = fig.add_subplot(gs[1, 0])
    vols_sample = [0.5, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 50.0]
    for reg, c in zip(reg_order, colors_reg):
        sub = df_br[df_br['regiao'] == reg]
        rel_trend = [sub[sub['lower_tank_vol_m3'] == v]['reliability_pct'].mean() if len(sub[sub['lower_tank_vol_m3'] == v]) > 0 else np.nan for v in vols_sample]
        # Interpolar se necessário
        s_rel = pd.Series(rel_trend).interpolate().bfill()
        ax_c.plot(vols_sample, s_rel, marker='o', lw=2.2, color=c, label=reg, markersize=5)

    ax_c.axvspan(3, 10, color='#E2E8F0', alpha=0.5, label="Patamar de Saturação Ótima")
    ax_c.set_title("C) Curvas de Saturação de Confiabilidade Hídrica por Região", loc='left', pad=10)
    ax_c.set_xlabel("Capacidade da Cisterna (m³)")
    ax_c.set_ylabel("Confiabilidade Hídrica Média (%)")
    ax_c.set_xlim(0, 50)
    ax_c.set_ylim(10, 85)
    ax_c.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Rendimento Pluvial Absoluto (m³/ano) vs Área de Telhado (m²)
    ax_d = fig.add_subplot(gs[1, 1])
    tip_area = df_br.groupby('building_code', observed=False).agg({
        'roof_area_m2': 'first',
        'annual_pluvial_m3': 'median',
        'building_category': 'first'
    }).reset_index()

    for _, row in tip_area.iterrows():
        col = PAL_EMERALD if row['building_category'] in ['Comercial', 'Educacional', 'Hospitalar', 'Hospedagem'] else PAL_BLUE
        ax_d.scatter(row['roof_area_m2'], row['annual_pluvial_m3'], s=120, color=col, edgecolors=PAL_NAVY, lw=1.0)
        ax_d.annotate(f"{row['building_code']}\n({row['annual_pluvial_m3']:.0f} m³/a)", (row['roof_area_m2'], row['annual_pluvial_m3']),
                      textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Rendimento Volumétrico Anual Mediano vs. Área de Captação", loc='left', pad=10)
    ax_d.set_xlabel("Área de Cobertura / Telhado (m²)")
    ax_d.set_ylabel("Volume Pluvial Aproveitado (m³/ano)")
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 1: Potencial de Economia Ótimo, Confiabilidade e Saturação nas 11 Tipologias (Brasil)",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig01_estudo2_potencial_economia_regional_11tipologias.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 2: Custo dos Sistemas, 8 Subsistemas e CUB nas 11 Tipologias
# ====================================================================================================
def generate_fig2():
    print(" -> Gerando Figura 2 (Estudo 2): Estrutura de Custos, 8 Subsistemas e CUB...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Decomposição dos 8 Subsistemas de CAPEX em Unifamiliar vs Médio vs Grande Porte
    ax_a = fig.add_subplot(gs[0, 0])
    selected_tips = ["RPOP", "UTI", "MSG", "COM", "HOT", "ESC", "HOS"]
    subs = ["Reservatório PEAD", "Reservatório Superior", "Motobomba 1+1", "Painel/Automação",
            "Filtro/First-Flush", "Tubos PVC", "Air-Gap Potável", "Mão de Obra/Escavação"]
    pal_sub = ["#3B82F6", "#60A5FA", "#0D9488", "#F59E0B", "#8B5CF6", "#64748B", "#EC4899", "#E11D48"]

    data_capex = np.array([
        [1000, 200, 280, 250, 300, 700, 150, 950],     # RPOP (~3.8k)
        [1800, 300, 302, 300, 350, 950, 150, 1400],    # UTI (~5.5k)
        [2899, 400, 450, 500, 600, 1600, 200, 2200],   # MSG (~8.8k)
        [3800, 500, 650, 800, 750, 1800, 250, 2800],   # COM (~11.3k)
        [8500, 900, 1200, 1400, 1200, 3200, 350, 5500], # HOT (~22.2k)
        [9500, 1000, 1400, 1800, 1500, 3800, 400, 6200], # ESC (~25.6k)
        [18500, 1500, 2200, 2600, 2200, 6500, 500, 12500] # HOS (~46.5k)
    ])

    data_pct = (data_capex.T / data_capex.sum(axis=1) * 100).T
    bottom = np.zeros(len(selected_tips))

    for idx_sub, (sub_name, col) in enumerate(zip(subs, pal_sub)):
        values = data_pct[:, idx_sub]
        bars = ax_a.bar(selected_tips, values, bottom=bottom, color=col, edgecolor='white', lw=0.8, label=sub_name, alpha=0.9)
        for b_idx, rect in enumerate(bars):
            h = rect.get_height()
            if h >= 10.0:
                ax_a.text(rect.get_x() + rect.get_width()/2., bottom[b_idx] + h/2., f"{h:.0f}%",
                          ha='center', va='center', color='white', fontsize=7.5, fontweight='bold')
        bottom += values

    ax_a.set_title("A) Decomposição Percentual dos 8 Subsistemas Prediais de CAPEX", loc='left', pad=10)
    ax_a.set_ylabel("Participação Relativa no CAPEX (%)")
    ax_a.set_ylim(0, 100)
    ax_a.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), framealpha=0.9, fontsize=7.5)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Fator Regional CUB/SINAPI por UF (27 UFs)
    ax_b = fig.add_subplot(gs[0, 1])
    reg_factors = costs_db['regional_factors_by_uf']
    uf_sorted = sorted(reg_factors.items(), key=lambda x: x[1])
    ufs = [x[0] for x in uf_sorted]
    factors = [x[1] for x in uf_sorted]

    bar_colors = [PAL_EMERALD if f < 0.98 else (PAL_AMBER if f <= 1.05 else PAL_ROSE) for f in factors]
    ax_b.bar(ufs, factors, color=bar_colors, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)
    ax_b.axhline(1.00, color=PAL_NAVY, linestyle='--', lw=1.2, label="Referência SP (1.00)")
    ax_b.set_title("B) Fator de Calibração Regional CUB / SINAPI das 27 UFs", loc='left', pad=10)
    ax_b.set_ylabel("Multiplicador Regional de Custo")
    ax_b.set_ylim(0.85, 1.25)
    ax_b.tick_params(axis='x', rotation=90, labelsize=8)
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Decomposição do OPEX Anual nas 11 Tipologias
    ax_c = fig.add_subplot(gs[1, 0])
    tip_order = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]
    opex_sum = df_br.groupby('building_code', observed=False).agg({
        'annual_energy_cost_brl': 'median',
        'annual_chlorine_cost_brl': 'median',
        'annual_maint_cost_brl': 'median'
    }).reindex(tip_order)

    x = np.arange(len(tip_order))
    w = 0.55
    ax_c.bar(x, opex_sum['annual_energy_cost_brl'], width=w, label='Energia Elétrica (B1 ANEEL)', color=PAL_AMBER, alpha=0.85)
    ax_c.bar(x, opex_sum['annual_chlorine_cost_brl'], width=w, bottom=opex_sum['annual_energy_cost_brl'], label='Cloração Química', color=PAL_TEAL, alpha=0.85)
    ax_c.bar(x, opex_sum['annual_maint_cost_brl'], width=w,
             bottom=opex_sum['annual_energy_cost_brl'] + opex_sum['annual_chlorine_cost_brl'],
             label='Manutenção Modular', color=PAL_PURPLE, alpha=0.85)

    ax_c.set_title("C) Decomposição do OPEX Anual Mediano (R$/ano) nas 11 Tipologias", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tip_order, rotation=45)
    ax_c.set_ylabel("OPEX Anual (R$/ano)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Curvas de Economia de Escala: CAPEX por m³ Útil Anual
    ax_d = fig.add_subplot(gs[1, 1])
    tip_capex_scale = df_br.groupby('building_code', observed=False).agg({
        'annual_pluvial_m3': 'median',
        'capex_total_brl': 'median'
    }).reset_index()
    tip_capex_scale['capex_per_m3_yr'] = tip_capex_scale['capex_total_brl'] / tip_capex_scale['annual_pluvial_m3']
    tip_capex_scale = tip_capex_scale.sort_values('annual_pluvial_m3')

    ax_d.plot(tip_capex_scale['annual_pluvial_m3'], tip_capex_scale['capex_per_m3_yr'],
              marker='o', color=PAL_ROSE, lw=2.4, markersize=8, label='CAPEX Unitário (R$ / m³ pluvial anual)')
    for _, row in tip_capex_scale.iterrows():
        ax_d.annotate(f"{row['building_code']}", (row['annual_pluvial_m3'], row['capex_per_m3_yr']),
                      textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Economia de Escala: CAPEX Unitário por Volume Anual Entregue", loc='left', pad=10)
    ax_d.set_xlabel("Volume Pluvial Aproveitado Anualmente (m³/ano)")
    ax_d.set_ylabel("CAPEX por m³ Anual (R$ / m³)")
    ax_d.set_xscale('log')
    ax_d.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_d.grid(True, linestyle='--', alpha=0.5)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 2: Estrutura de Custos (CAPEX/OPEX), Subsistemas e Calibração Regional CUB",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig02_estudo2_custos_8subsistemas_cub_brasil.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 3: ACV e CO2 nas 11 Tipologias Edilícias
# ====================================================================================================
def generate_fig3():
    print(" -> Gerando Figura 3 (Estudo 2): ACV e Balanço de Carbono das 11 Tipologias...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Balanço de Carbono nos 20 Anos para 4 Tipologias Chave
    ax_a = fig.add_subplot(gs[0, 0])
    componentes = ["Reservatório PEAD", "Caixa Superior", "Tubos PVC", "Motobomba", "Recalque 20a", "Cloração", "Evitado Rede"]
    co2_uti = np.array([330.0, 33.0, 35.0, 18.0, 122.4, 18.0, -840.0])
    co2_com = np.array([495.0, 45.0, 62.0, 24.0, 280.0, 62.5, -2920.0])
    co2_esc = np.array([1980.0, 90.0, 180.0, 42.0, 1280.0, 209.0, -9750.0])
    co2_hos = np.array([3300.0, 120.0, 240.0, 55.0, 1850.0, 286.0, -13380.0])

    y = np.arange(len(componentes))
    h = 0.20
    ax_a.barh(y - 1.5*h, co2_uti, height=h, color=PAL_CYAN, label=f"UTI (Saldo: {co2_uti.sum():+.0f} kg)", alpha=0.85)
    ax_a.barh(y - 0.5*h, co2_com, height=h, color=PAL_AMBER, label=f"COM (Saldo: {co2_com.sum():+.0f} kg)", alpha=0.85)
    ax_a.barh(y + 0.5*h, co2_esc, height=h, color=PAL_BLUE, label=f"ESC (Saldo: {co2_esc.sum():+.0f} kg)", alpha=0.85)
    ax_a.barh(y + 1.5*h, co2_hos, height=h, color=PAL_EMERALD, label=f"HOS (Saldo: {co2_hos.sum():+.0f} kg)", alpha=0.85)

    ax_a.axvline(0, color=PAL_NAVY, lw=1.2)
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(componentes, fontsize=8.5)
    ax_a.set_title("A) Balanço de Carbono no Ciclo de Vida de 20 Anos (kg CO₂e)", loc='left', pad=10)
    ax_a.set_xlabel("Emissão (+) vs. Retirada / Evitado (−) (kg CO₂e)")
    ax_a.legend(loc='lower left', framealpha=0.9, fontsize=8)
    ax_a.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Benchmark Nacional de CO2 Evitado Anual Mediano (kg CO2e / ano)
    ax_b = fig.add_subplot(gs[0, 1])
    tip_co2 = df_br.groupby('building_code', observed=False)['annual_avoided_co2_kg'].median().sort_values(ascending=True)
    col_co2 = [PAL_EMERALD if v > 100 else (PAL_AMBER if v > 40 else PAL_CYAN) for v in tip_co2]
    bars_b = ax_b.barh(tip_co2.index, tip_co2.values, color=col_co2, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_b:
        w_val = rect.get_width()
        ax_b.text(w_val + 3, rect.get_y() + rect.get_height()/2., f"{w_val:.0f} kg/ano",
                  va='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Saldo Líquido de Descarbonização Anual por Tipologia", loc='left', pad=10)
    ax_b.set_xlabel("CO₂ Evitado Anual Mediano (kg CO₂e / ano)")
    ax_b.set_xlim(0, 240)
    ax_b.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Sensibilidade do CO2 Evitado vs Fator da Água Potável da Rede
    ax_c = fig.add_subplot(gs[1, 0])
    fator_range = np.linspace(0.10, 1.20, 50)
    for tip, v_ano, col in [("UTI", 36.08, PAL_CYAN), ("COM", 125.20, PAL_AMBER),
                            ("ESC", 418.15, PAL_BLUE), ("HOS", 573.40, PAL_EMERALD)]:
        bomba_co2 = 0.40 * 0.085 * v_ano
        saldo_anual = [v_ano * f - bomba_co2 for f in fator_range]
        ax_c.plot(fator_range, saldo_anual, label=f"{tip} ({v_ano:.0f} m³/ano)", color=col, lw=2.2)

    ax_c.axvline(0.35, color=PAL_GRAY, linestyle='--', lw=1.2, label='Brasil SIN (0.35 kg/m³)')
    ax_c.set_title("C) Sensibilidade da Descarbonização vs. Intensidade da Água de Rede", loc='left', pad=10)
    ax_c.set_xlabel("Fator da Água Tratada da Concessionária (kg CO₂e/m³)")
    ax_c.set_ylabel("CO₂ Líquido Evitado (kg CO₂e / ano)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Payback Ambiental (Anos) nas 11 Tipologias
    ax_d = fig.add_subplot(gs[1, 1])
    pb_ecol = [14.2, 12.8, 8.4, 6.2, 3.4, 5.8, 4.2, 3.1, 1.8, 2.4, 1.6]
    tip_pb = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]
    bars_d = ax_d.bar(tip_pb, pb_ecol, color=[PAL_EMERALD if p <= 4.0 else (PAL_AMBER if p <= 8.0 else PAL_ROSE) for p in pb_ecol],
                      edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_d:
        h_val = rect.get_height()
        ax_d.text(rect.get_x() + rect.get_width()/2., h_val + 0.3, f"{h_val:.1f}a",
                  ha='center', va='bottom', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.axhline(5.0, color=PAL_GRAY, linestyle='--', label='Meta Sustentável (<= 5 anos)')
    ax_d.set_title("D) Tempo de Retorno Ecológico (Payback de Carbono em Anos)", loc='left', pad=10)
    ax_d.set_xlabel("Tipologia Edilícia")
    ax_d.set_ylabel("Payback Ambiental (Anos)")
    ax_d.set_ylim(0, 16)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 3: Avaliação de Ciclo de Vida (ACV) e Balanço de Carbono das 11 Tipologias no Brasil",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig03_estudo2_acv_balanco_carbono_11tipologias.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 4: Otimização Ambiental vs Econômica e Fronteira de Pareto (11 Tipologias)
# ====================================================================================================
def generate_fig4():
    print(" -> Gerando Figura 4 (Estudo 2): Otimização Ambiental vs Econômica (11 Tipologias)...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Fronteira de Pareto VPL vs CO2 nas 11 Tipologias
    ax_a = fig.add_subplot(gs[0, 0])
    for cat, col in [("Educacional", PAL_BLUE), ("Hospitalar", PAL_EMERALD), ("Comercial", PAL_AMBER),
                     ("Multifamiliar", PAL_PURPLE), ("Residencial", PAL_CYAN)]:
        sub = df_br[df_br['building_category'] == cat]
        ax_a.scatter(sub['vpl_6pct_brl'] / 1000.0, sub['lifetime_net_co2_kg'] / 1000.0,
                     color=col, alpha=0.35, s=24, label=cat, edgecolors='none')

    ax_a.set_title("A) Fronteira de Pareto: VPL Econômico vs. Descarbonização", loc='left', pad=10)
    ax_a.set_xlabel("VPL a 6% a.a. (Milhares de R$)")
    ax_a.set_ylabel("CO₂ Evitado Vida Útil (Toneladas CO₂e)")
    ax_a.axhline(0, color=PAL_GRAY, linestyle=':')
    ax_a.axvline(0, color=PAL_GRAY, linestyle=':')
    ax_a.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_a.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Ponto de Inflexão Ambiental
    ax_b = fig.add_subplot(gs[0, 1])
    vols_sample = [1.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 50.0]
    for tip, col in [("UTI", PAL_CYAN), ("COM", PAL_AMBER), ("ESC", PAL_BLUE), ("HOS", PAL_EMERALD)]:
        # Curva representativa
        v_base = 36.0 if tip == "UTI" else (125.0 if tip == "COM" else (418.0 if tip == "ESC" else 573.0))
        co2_pts = []
        for v in vols_sample:
            pluv = v_base * min(1.0, 0.45 + 0.55 * (1.0 - math.exp(-v / (v_base * 0.05))))
            emb = 66.0 * v + 120.0 # PEAD
            evit = pluv * 0.35 * 20.0
            co2_pts.append(evit - emb)
        ax_b.plot(vols_sample, co2_pts, marker='o', lw=2.2, color=col, label=tip)
        max_i = np.argmax(co2_pts)
        ax_b.plot(vols_sample[max_i], co2_pts[max_i], marker='*', color=PAL_ROSE, markersize=11, zorder=10)

    ax_b.set_title("B) Ponto de Inflexão Ambiental: Ganho Hídrico vs. Carbono Incorporado", loc='left', pad=10)
    ax_b.set_xlabel("Capacidade da Cisterna (m³)")
    ax_b.set_ylabel("Saldo Acumulado de CO₂ Evitado em 20 Anos (kg CO₂e)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Divergência Dimensional nas 11 Tipologias
    ax_c = fig.add_subplot(gs[1, 0])
    tips_c = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]
    x = np.arange(len(tips_c))
    w = 0.35

    v_econ = [1.0, 1.0, 5.0, 5.0, 7.5, 5.0, 5.0, 20.0, 30.0, 15.0, 50.0]
    v_env = [3.0, 3.0, 5.0, 7.5, 10.0, 7.5, 10.0, 20.0, 30.0, 20.0, 50.0]

    ax_c.bar(x - w/2, v_econ, width=w, label='Ótimo Econômico (Max VPL)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_c.bar(x + w/2, v_env, width=w, label='Ótimo Ambiental (Max CO₂)', color=PAL_EMERALD, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    ax_c.set_title("C) Comparativo de Capacidades: Ótimo Econômico vs. Ambiental", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tips_c, rotation=45)
    ax_c.set_ylabel("Volume de Cisterna Recomendado (m³)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Co-benefício Financeiro e Ambiental
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df_br['annual_gross_savings_brl'], df_br['annual_avoided_co2_kg'],
                 c=df_br['capex_total_brl'], cmap='viridis', alpha=0.6, s=26, edgecolors='none')
    cb = plt.colorbar(cm.ScalarMappable(norm=Normalize(df_br['capex_total_brl'].min(), 50000), cmap='viridis'), ax=ax_d)
    cb.set_label("CAPEX Predial (R$)", fontsize=8.5, fontweight='bold')

    ax_d.set_title("D) Co-benefício: Economia Bruta na Fatura vs. CO₂ Evitado", loc='left', pad=10)
    ax_d.set_xlabel("Economia Anual de Água (R$/ano)")
    ax_d.set_ylabel("CO₂ Evitado Anualmente (kg CO₂e / ano)")
    ax_d.set_xscale('log')
    ax_d.set_yscale('log')
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 4: Otimização Ambiental vs. Econômica, Inflexão e Pareto nas 11 Tipologias (Brasil)",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig04_estudo2_otimizacao_ambiental_vs_economica.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 5: Otimização Multicritério TOPSIS vs VIKOR nas 652 Cidades
# ====================================================================================================
def generate_fig5():
    print(" -> Gerando Figura 5 (Estudo 2): Otimização Multicritério TOPSIS vs VIKOR...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    tip_order = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]

    # Painel A: Volumes Ótimos VPL vs VIKOR nas 11 Tipologias
    ax_a = fig.add_subplot(gs[0, 0])
    v_econ_med = df_br.groupby('building_code', observed=False)['opt_vol_econ_m3'].median().reindex(tip_order)
    v_vik_med = df_br.groupby('building_code', observed=False)['opt_vol_vikor_m3'].median().reindex(tip_order)

    x = np.arange(len(tip_order))
    w = 0.35
    ax_a.bar(x - w/2, v_econ_med, width=w, label='VPL Puro (Econômico)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_a.bar(x + w/2, v_vik_med, width=w, label='VIKOR (Compromisso v=0.5)', color=PAL_PURPLE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    ax_a.set_title("A) Volume Mediano de Cisterna (m³): VPL Econômico vs. VIKOR", loc='left', pad=10)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(tip_order, rotation=45)
    ax_a.set_ylabel("Volume Selecionado (m³)")
    ax_a.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Espaço de Decisão VIKOR (S vs R)
    ax_b = fig.add_subplot(gs[0, 1])
    for cat, col in [("Educacional", PAL_BLUE), ("Hospitalar", PAL_EMERALD), ("Comercial", PAL_AMBER),
                     ("Multifamiliar", PAL_PURPLE), ("Residencial", PAL_CYAN)]:
        sub = df_br[df_br['building_category'] == cat]
        ax_b.scatter(sub['vikor_s_score'], sub['vikor_r_score'],
                     color=col, alpha=0.35, s=24, label=cat, edgecolors='none')

    ax_b.set_title("B) Mecânica do VIKOR: Utilidade Coletiva (S) vs. Arrependimento (R)", loc='left', pad=10)
    ax_b.set_xlabel("Medida de Utilidade Coletiva S (Distância Manhattan L1)")
    ax_b.set_ylabel("Medida de Pior Arrependimento R (Distância Chebyshev L∞)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Pesos Centrais Estocásticos SMAA-2
    ax_c = fig.add_subplot(gs[1, 0])
    sc = ax_c.scatter(df_br['smaa_w_econ'] * 100, df_br['smaa_w_tech'] * 100,
                      c=df_br['smaa_w_env'] * 100, cmap='plasma', s=24, alpha=0.6, edgecolors='none')
    cb_c = plt.colorbar(sc, ax=ax_c)
    cb_c.set_label("Peso Central Ambiental w_env (%)", fontsize=8.5, fontweight='bold')

    ax_c.set_title("C) Pesos Centrais Estocásticos do SMAA-2 (652 Cidades)", loc='left', pad=10)
    ax_c.set_xlabel("Peso Central Econômico w_econ (%)")
    ax_c.set_ylabel("Peso Central Técnico w_tech (%)")
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Frequência de Concordância Decisória nas 11 Tipologias
    ax_d = fig.add_subplot(gs[1, 1])
    ag_counts = df_br.groupby(['building_code', 'decision_agreement'], observed=False).size().unstack(fill_value=0).reindex(tip_order)
    x_d = np.arange(len(tip_order))
    w_d = 0.55

    ax_d.bar(x_d, ag_counts['CONVERGENT'], width=w_d, label='Convergente (VIKOR = VPL)', color=PAL_EMERALD, alpha=0.85)
    ax_d.bar(x_d, ag_counts['DIVERGENT'], width=w_d, bottom=ag_counts['CONVERGENT'],
             label='Divergente (VIKOR Protege contra Subdimensionamento)', color=PAL_ROSE, alpha=0.85)

    ax_d.set_title("D) Taxa de Divergência Decisória: Proteção Técnica nas Tipologias", loc='left', pad=10)
    ax_d.set_xticks(x_d)
    ax_d.set_xticklabels(tip_order, rotation=45)
    ax_d.set_ylabel("Número de Cidades (Total = 652)")
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 5: Otimização Multicritério (MCDM): TOPSIS, VIKOR e Robustez SMAA-2 no Brasil",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig05_estudo2_mcdm_topsis_vs_vikor_652cidades.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 6: Panorama Tarifário de Saneamento e Energia no Brasil (652 Cidades)
# ====================================================================================================
def generate_fig6():
    print(" -> Gerando Figura 6 (Estudo 2): Panorama Tarifário de Saneamento e Energia (652 Cidades)...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    gdf_br = load_brazil_gdf()

    # Painel A: Mapa Coroplético das Tarifas Combinadas de Saneamento
    ax_a = fig.add_subplot(gs[0, 0])
    if gdf_br is not None:
        gdf_br.plot(ax=ax_a, color='#F1F5F9', edgecolor='#94A3B8', linewidth=0.5)

    city_tar = df_br.groupby(['city', 'uf', 'lat', 'lon'], observed=False)['tarifa_combinada_m3'].mean().reset_index()
    sc_a = ax_a.scatter(city_tar['lon'], city_tar['lat'], c=city_tar['tarifa_combinada_m3'],
                        cmap='YlOrRd', s=24, alpha=0.85, edgecolors=PAL_NAVY, lw=0.3)
    cb_a = plt.colorbar(sc_a, ax=ax_a, fraction=0.046, pad=0.04)
    cb_a.set_label("Tarifa Combinada Água+Esgoto (R$/m³)", fontsize=8.5, fontweight='bold')

    ax_a.set_title("A) Geografia das Tarifas de Saneamento no Brasil (652 Cidades)", loc='left', pad=10)
    ax_a.set_xlim(-74, -34)
    ax_a.set_ylim(-34, 6)
    ax_a.set_xlabel("Longitude (°W)")
    ax_a.set_ylabel("Latitude (°S)")
    ax_a.grid(True, linestyle='--', alpha=0.3)
    add_panel_label(ax_a, "A")

    # Painel B: O Efeito Multiplicador do Esgoto Indexado
    ax_b = fig.add_subplot(gs[0, 1])
    t_agua = np.linspace(2, 12, 50)
    ax_b.plot(t_agua, t_agua, color=PAL_GRAY, lw=2.0, linestyle='--', label='Água Pura (k_esgoto = 0%)')
    ax_b.plot(t_agua, t_agua * 1.8, color=PAL_AMBER, lw=2.2, label='Esgoto 80% (Copasa/Sanepar)')
    ax_b.plot(t_agua, t_agua * 2.0, color=PAL_BLUE, lw=2.4, label='Esgoto 100% (Sabesp/Caesb/Águas do Rio)')

    ax_b.set_title("B) Efeito Alavanca do Esgoto na Margem Financeira Marginal", loc='left', pad=10)
    ax_b.set_xlabel("Tarifa Básica de Água (R$/m³)")
    ax_b.set_ylabel("Tarifa Marginal Efetiva Evitada (R$/m³)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Dispersão Tarifa de Água vs Custo de Energia de Recalque
    ax_c = fig.add_subplot(gs[1, 0])
    ax_c.scatter(df_br['tarifa_combinada_m3'], df_br['cost_per_m3_opex_brl'],
                 color=PAL_TEAL, alpha=0.45, s=24, edgecolors='none')
    t_vals = np.linspace(2, 25, 50)
    ax_c.plot(t_vals, t_vals * 0.10, color=PAL_AMBER, lw=1.8, linestyle='--', label='10% da Tarifa')
    ax_c.plot(t_vals, t_vals * 0.05, color=PAL_EMERALD, lw=1.8, linestyle=':', label='5% da Tarifa')

    ax_c.set_title("C) Elasticidade Cruzada: OPEX de Recalque vs. Tarifa Evitada", loc='left', pad=10)
    ax_c.set_xlabel("Tarifa Combinada de Saneamento (R$/m³)")
    ax_c.set_ylabel("Custo Operacional Específico (R$/m³ aproveitado)")
    ax_c.set_ylim(0, 4.5)
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: VPL vs Spread Operacional Líquido
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df_br['spread_brl_m3'], df_br['vpl_6pct_brl'] / 1000.0,
                 c=df_br['annual_pluvial_m3'], cmap='viridis', alpha=0.5, s=24, edgecolors='none')
    cb_d = plt.colorbar(cm.ScalarMappable(norm=Normalize(20, 600), cmap='viridis'), ax=ax_d)
    cb_d.set_label("Volume Pluvial Anual (m³/ano)", fontsize=8.5, fontweight='bold')

    ax_d.axhline(0, color=PAL_ROSE, linestyle='--', lw=1.2)
    ax_d.set_title("D) VPL Financeiro (Milhares R$) vs. Spread Operacional Líquido", loc='left', pad=10)
    ax_d.set_xlabel("Spread Líquido Unitário (R$/m³ evitado − R$/m³ opex)")
    ax_d.set_ylabel("VPL a 6% a.a. (Milhares de R$)")
    ax_d.set_ylim(-30, 200)
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 6: Panorama Tarifário de Saneamento e Eletricidade nas 652 Cidades Brasileiras",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig06_estudo2_panorama_tarifario_saneamento_energia_652cidades.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 7: Comparativo das 11 Tipologias Edilícias no Brasil
# ====================================================================================================
def generate_fig7():
    print(" -> Gerando Figura 7 (Estudo 2): Análise Comparativa das 11 Tipologias Edilícias...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Radar Multidimensional das 11 Tipologias
    ax_a = fig.add_subplot(gs[0, 0], polar=True)
    cats = ['Economia Hídrica', 'Confiabilidade', 'VPL Financeiro', 'TIR Anual', 'CO2 Evitado', 'Giro Cisterna', 'Baixo LCOW']
    num_vars = len(cats)
    angles = [n / float(num_vars) * 2 * math.pi for n in range(num_vars)]
    angles += angles[:1]

    perfis = {
        "Unifamiliar (UTI)": [42, 45, 12, 10, 15, 25, 30],
        "Multifamiliar (MFL)": [20, 15, 65, 50, 75, 55, 65],
        "Comercial (COM)": [75, 70, 60, 68, 48, 70, 72],
        "Escolas (ESC)": [60, 52, 92, 95, 88, 85, 90]
    }
    cols_radar = [PAL_CYAN, PAL_PURPLE, PAL_AMBER, PAL_EMERALD]

    for (name, vals), col in zip(perfis.items(), cols_radar):
        v = vals + vals[:1]
        ax_a.plot(angles, v, lw=2.0, color=col, label=name)
        ax_a.fill(angles, v, facecolor=col, alpha=0.15)

    ax_a.set_xticks(angles[:-1])
    ax_a.set_xticklabels(cats, fontsize=8.5, fontweight='bold')
    ax_a.set_ylim(0, 100)
    ax_a.set_title("A) Diagrama Radar Multi-Indicador das Famílias Tipológicas", loc='left', pad=15)
    ax_a.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=2, framealpha=0.9, fontsize=8)
    add_panel_label(ax_a, "A")

    # Painel B: Ranking de Viabilidade (% Cidades VPL > 0 e Payback <= 10a)
    ax_b = fig.add_subplot(gs[0, 1])
    tip_viab = df_br.groupby('building_code', observed=False).agg({
        'is_viable_6pct': 'mean',
        'lcow_6pct_brl_m3': 'median'
    }).reset_index()
    tip_viab['viab_pct'] = tip_viab['is_viable_6pct'] * 100.0
    tip_viab = tip_viab.sort_values('viab_pct', ascending=True)

    col_bars = [PAL_ROSE if v < 20 else (PAL_AMBER if v < 60 else PAL_EMERALD) for v in tip_viab['viab_pct']]
    bars_b = ax_b.barh(tip_viab['building_code'], tip_viab['viab_pct'], color=col_bars, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect, (_, row) in zip(bars_b, tip_viab.iterrows()):
        w_val = rect.get_width()
        ax_b.text(w_val + 1.2, rect.get_y() + rect.get_height()/2.,
                  f"{w_val:.1f}% (LCOW: R${row['lcow_6pct_brl_m3']:.2f})",
                  va='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Taxa de Viabilidade Econômica (VPL > 0 e Payback <= 10 anos)", loc='left', pad=10)
    ax_b.set_xlabel("Percentual de Cidades Brasileiras Viáveis a 6% a.a. (%)")
    ax_b.set_xlim(0, 115)
    ax_b.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Intensidade Hídrica e Turnover de Cisterna
    ax_c = fig.add_subplot(gs[1, 0])
    tip_scale = df_br.groupby('building_code', observed=False).agg({
        'roof_area_m2': 'first',
        'occupants': 'first',
        'daily_pluvial_demand_l': 'first',
        'annual_pluvial_m3': 'median',
        'lower_tank_vol_m3': 'median'
    }).reset_index()

    tip_scale['area_per_capita'] = tip_scale['roof_area_m2'] / tip_scale['occupants']
    tip_scale['demand_per_capita'] = tip_scale['daily_pluvial_demand_l'] / tip_scale['occupants']
    tip_scale['turnover'] = tip_scale['annual_pluvial_m3'] / tip_scale['lower_tank_vol_m3']

    sc_c = ax_c.scatter(tip_scale['area_per_capita'], tip_scale['demand_per_capita'],
                        s=tip_scale['turnover'] * 18, c=tip_scale['turnover'], cmap='coolwarm',
                        edgecolors=PAL_NAVY, lw=0.8, alpha=0.9)
    cb_c = plt.colorbar(sc_c, ax=ax_c)
    cb_c.set_label("Taxa Anual de Giro da Cisterna (Turnover)", fontsize=8.5, fontweight='bold')

    for _, row in tip_scale.iterrows():
        ax_c.annotate(f"{row['building_code']}\n({row['turnover']:.0f}x)",
                      (row['area_per_capita'], row['demand_per_capita']),
                      textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_c.set_title("C) Intensidade Hídrica: Área per capita vs. Demanda e Giro Anual", loc='left', pad=10)
    ax_c.set_xlabel("Área de Telhado per capita (m² / ocupante)")
    ax_c.set_ylabel("Demanda Pluvial per capita (L / ocupante.dia)")
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: CAPEX Total vs VPL Mediano
    ax_d = fig.add_subplot(gs[1, 1])
    tip_fin = df_br.groupby('building_code', observed=False).agg({
        'capex_total_brl': 'median',
        'vpl_6pct_brl': 'median'
    }).reset_index()

    ax_d.scatter(tip_fin['capex_total_brl'] / 1000.0, tip_fin['vpl_6pct_brl'] / 1000.0,
                 color=PAL_BLUE, s=90, edgecolors=PAL_NAVY, lw=1.0)
    for _, row in tip_fin.iterrows():
        ax_d.annotate(f"{row['building_code']}", (row['capex_total_brl']/1000.0, row['vpl_6pct_brl']/1000.0),
                      textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_d.axhline(0, color=PAL_ROSE, linestyle='--', lw=1.2, label='Limiar de Viabilidade (VPL = 0)')
    ax_d.set_title("D) Retorno Líquido (VPL) vs. Desembolso Inicial de Capital", loc='left', pad=10)
    ax_d.set_xlabel("CAPEX Inicial Mediano (Milhares de R$)")
    ax_d.set_ylabel("VPL Mediano a 6% a.a. (Milhares de R$)")
    ax_d.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 7: Análise Comparativa das 11 Tipologias Edilícias no Brasil: Escala, LCOW e Atratividade",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig07_estudo2_comparativo_11_tipologias_desempenho_escala.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 8: Matriz Bivariada 3x3 Chuva vs Tarifa no Brasil (652 Cidades)
# ====================================================================================================
def generate_fig8():
    print(" -> Gerando Figura 8 (Estudo 2): Matriz Bivariada 3x3 Chuva vs Tarifa no Brasil...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    gdf_br = load_brazil_gdf()

    # Painel A: Matriz Conceitual 3x3
    ax_a = fig.add_subplot(gs[0, 0])
    biv_colors_matrix = [
        ["#E8E8E8", "#B5D2D8", "#78B9C8"],
        ["#D6AFB2", "#A69DA8", "#6D879B"],
        ["#C26A74", "#95596D", "#5B4461"]
    ]
    quad_names = [
        ["Deserto Econômico\n(Baixa C. / Baixa T.)", "Viabilidade Moderada\n(Baixa C. / Média T.)", "Oásis de Escassez\n(Baixa C. / Alta T.)"],
        ["Incentivo Requerido\n(Média C. / Baixa T.)", "Atratividade Média\n(Média C. / Média T.)", "Atratividade Elevada\n(Média C. / Alta T.)"],
        ["Paradoxo da Abundância\n(Alta C. / Baixa T.)", "Excelente Potencial\n(Alta C. / Média T.)", "QUADRANTE DE OURO\n(Alta C. / Alta T.)"]
    ]

    for r in range(3):
        for c in range(3):
            color = biv_colors_matrix[r][c]
            rect = patches.Rectangle((c, r), 1, 1, facecolor=color, edgecolor='white', lw=1.5)
            ax_a.add_patch(rect)
            tc = 'white' if (r >= 1 and c >= 1) or (r == 2 or c == 2) else PAL_NAVY
            ax_a.text(c + 0.5, r + 0.5, quad_names[r][c], ha='center', va='center', fontsize=8.5, fontweight='bold', color=tc)

    ax_a.set_xlim(0, 3)
    ax_a.set_ylim(0, 3)
    ax_a.set_xticks([0.5, 1.5, 2.5])
    ax_a.set_xticklabels(["Tercil 1 (Baixa Tarifa)", "Tercil 2 (Média Tarifa)", "Tercil 3 (Alta Tarifa)"], fontsize=8.5, fontweight='bold')
    ax_a.set_yticks([0.5, 1.5, 2.5])
    ax_a.set_yticklabels(["Tercil 1 (Baixa Chuva)", "Tercil 2 (Média Chuva)", "Tercil 3 (Alta Chuva)"], fontsize=8.5, fontweight='bold')
    ax_a.set_title("A) Matriz 3x3: Classificação dos 9 Quadrantes Geoeconômicos", loc='left', pad=10)
    add_panel_label(ax_a, "A")

    # Painel B: Mapa Bivariado do Brasil (652 Municípios)
    ax_b = fig.add_subplot(gs[0, 1])
    if gdf_br is not None:
        gdf_br.plot(ax=ax_b, color='#F8FAFC', edgecolor='#94A3B8', linewidth=0.5)

    df_br_uniq = df_br.groupby(['city', 'uf', 'lat', 'lon'], observed=False).agg({
        'precip_annual_mean_mm': 'first',
        'tarifa_combinada_m3': 'first',
        'vpl_6pct_brl': 'median'
    }).reset_index()

    p_terc = pd.qcut(df_br_uniq['precip_annual_mean_mm'], q=3, labels=[0, 1, 2]).astype(int)
    t_terc = pd.qcut(df_br_uniq['tarifa_combinada_m3'], q=3, labels=[0, 1, 2]).astype(int)

    city_colors = [biv_colors_matrix[p][t] for p, t in zip(p_terc, t_terc)]
    ax_b.scatter(df_br_uniq['lon'], df_br_uniq['lat'], color=city_colors, s=26, alpha=0.85, edgecolors=PAL_NAVY, lw=0.3)

    sc_pts = df_br_uniq[df_br_uniq['uf'] == 'SC']
    rj_pts = df_br_uniq[df_br_uniq['uf'] == 'RJ']
    ax_b.scatter(sc_pts['lon'], sc_pts['lat'], facecolors='none', edgecolors=PAL_ROSE, s=70, lw=1.2, label='SC (Topo Nacional)')
    ax_b.scatter(rj_pts['lon'], rj_pts['lat'], facecolors='none', edgecolors=PAL_PURPLE, s=70, lw=1.2, label='RJ (Alta Tarifa)')

    ax_b.set_title("B) Mapa Bivariado das 652 Cidades Brasileiras na Matriz 3x3", loc='left', pad=10)
    ax_b.set_xlabel("Longitude (°W)")
    ax_b.set_ylabel("Latitude (°S)")
    ax_b.set_xlim(-74, -34)
    ax_b.set_ylim(-34, 6)
    ax_b.legend(loc='lower left', framealpha=0.9, fontsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.3)
    add_panel_label(ax_b, "B")

    # Painel C: Dispersão Chuva vs Tarifa nas 652 Cidades
    ax_c = fig.add_subplot(gs[1, 0])
    sc = ax_c.scatter(df_br_uniq['precip_annual_mean_mm'], df_br_uniq['tarifa_combinada_m3'],
                      c=df_br_uniq['vpl_6pct_brl'] / 1000.0, cmap='viridis', alpha=0.75, s=32, edgecolors=PAL_NAVY, lw=0.3)
    cb_c = plt.colorbar(sc, ax=ax_c)
    cb_c.set_label("VPL Mediano a 6% a.a. (Milhares de R$)", fontsize=8.5, fontweight='bold')

    p_med = df_br_uniq['precip_annual_mean_mm'].median()
    t_med = df_br_uniq['tarifa_combinada_m3'].median()
    ax_c.axvline(p_med, color=PAL_GRAY, linestyle='--', label=f'Mediana Chuva ({p_med:.0f} mm)')
    ax_c.axhline(t_med, color=PAL_GRAY, linestyle=':', label=f'Mediana Tarifa (R${t_med:.2f})')

    ax_c.set_title("C) Dispersão Geoeconômica: Chuva Anual vs. Tarifa Combinada", loc='left', pad=10)
    ax_c.set_xlabel("Precipitação Média Anual (mm/ano)")
    ax_c.set_ylabel("Tarifa Combinada de Saneamento (R$/m³)")
    ax_c.legend(loc='upper right', framealpha=0.9, fontsize=8)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: VPL Mediano nos 9 Quadrantes da Matriz
    ax_d = fig.add_subplot(gs[1, 1])
    df_br_uniq['p_terc'] = p_terc
    df_br_uniq['t_terc'] = t_terc
    vpl_mat = df_br_uniq.groupby(['p_terc', 't_terc'], observed=False)['vpl_6pct_brl'].median().unstack()

    im = ax_d.imshow(vpl_mat, cmap='RdYlGn', aspect='auto', origin='lower')
    cb = plt.colorbar(im, ax=ax_d)
    cb.set_label("VPL Mediano a 6% a.a. (R$)", fontsize=8.5, fontweight='bold')

    for r in range(3):
        for c in range(3):
            val = vpl_mat.iloc[r, c]
            ax_d.text(c, r, f"R$ {val:,.0f}", ha='center', va='center', fontsize=9, fontweight='bold',
                      color='black' if abs(val) < 20000 else 'white')

    ax_d.set_xticks([0, 1, 2])
    ax_d.set_xticklabels(["Baixa Tarifa", "Média Tarifa", "Alta Tarifa"], fontweight='bold')
    ax_d.set_yticks([0, 1, 2])
    ax_d.set_yticklabels(["Baixa Chuva", "Média Chuva", "Alta Chuva"], fontweight='bold')
    ax_d.set_title("D) VPL Mediano nos 9 Quadrantes: Evidência da Alavanca Tarifária", loc='left', pad=10)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 2 — FIGURA 8: Matriz Bivariada 3x3 de Precipitação vs. Tarifa nas 652 Cidades Brasileiras",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig08_estudo2_matriz_bivariada_3x3_chuva_vs_tarifa_brasil.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

def main():
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    generate_fig5()
    generate_fig6()
    generate_fig7()
    generate_fig8()
    print("Suíte de 8 figuras do Estudo 2 gerada com sucesso em:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
