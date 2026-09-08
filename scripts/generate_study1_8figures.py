"""
====================================================================================================
NETUNO 5 — ESTUDO 1: 5 TIPOLOGIAS RESIDENCIAIS SOB CENÁRIOS CLIMÁTICOS CMIP6 (BRASIL)
Geração das 8 Figuras Científicas de Alto Impacto para o Artigo 1
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
OUTPUT_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "figuras_artigo_8")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Bases de dados do Estudo 1
STUDY1_VARREDURA = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "capitais_varredura_completa.csv")
STUDY1_MCDM = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "capitais_mcdm_vikor_smaa_resumo.csv")
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

print("Iniciando geração das 8 figuras do Estudo 1 (5 Tipologias Residenciais CMIP6)...")

df_sw = pd.read_csv(STUDY1_VARREDURA, sep=';')
df_mcdm = pd.read_csv(STUDY1_MCDM, sep=';')
with open(COSTS_JSON, 'r', encoding='utf-8') as f:
    costs_db = json.load(f)

# ====================================================================================================
# FIGURA 1: Potencial de Economia Ótimo por Região e Degradação Climática
# ====================================================================================================
def generate_fig1():
    print(" -> Gerando Figura 1 (Estudo 1): Potencial Regional e Degradação Climática...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Potencial por Macrorregião Brasileira nas 5 Residenciais
    ax_a = fig.add_subplot(gs[0, 0])
    reg_order = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    colors_reg = [PAL_EMERALD, PAL_AMBER, PAL_PURPLE, PAL_CYAN, PAL_BLUE]
    
    data_reg = [df_mcdm[df_mcdm['regiao'] == r]['savings_econ_pct'].dropna() for r in reg_order]
    bp = ax_a.boxplot(data_reg, tick_labels=reg_order, patch_artist=True,
                      showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                      medianprops=dict(color=PAL_NAVY, lw=2.0))
    for patch, c in zip(bp['boxes'], colors_reg):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, r in enumerate(reg_order):
        med = df_mcdm[df_mcdm['regiao'] == r]['savings_econ_pct'].median()
        ax_a.text(idx + 1, med + 0.8, f"{med:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_a.set_title("A) Potencial Ótimo de Economia de Água Potável por Macrorregião", loc='left', pad=10)
    ax_a.set_ylabel("Economia de Água Potável (%)")
    ax_a.set_ylim(0, 32)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Degradação Climática do Potencial: Histórico (1980-2013) vs Far Future (2075-2100) SSP5-8.5
    ax_b = fig.add_subplot(gs[0, 1])
    # Dados empíricos agregados do modelo CMIP6 (Vaz / Netuno 5)
    hist_pot = [17.60, 9.79, 12.69, 12.81, 14.66]
    far_pot  = [12.03, 7.18, 9.31, 10.14, 12.31]
    perda_rel = [(h - f) / h * 100 for h, f in zip(hist_pot, far_pot)]

    x = np.arange(len(reg_order))
    w = 0.35
    ax_b.bar(x - w/2, hist_pot, width=w, label='Histórico (1980–2013)', color=PAL_CYAN, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_b.bar(x + w/2, far_pot, width=w, label='Far Future (SSP5-8.5 / 2075–2100)', color=PAL_ROSE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    for i in x:
        ax_b.text(i, max(hist_pot[i], far_pot[i]) + 0.8, f"−{perda_rel[i]:.1f}%", ha='center', va='bottom',
                  fontsize=8, fontweight='bold', color=PAL_ROSE)

    ax_b.set_title("B) Degradação do Potencial sob Mudanças Climáticas (CMIP6 / SSP5-8.5)", loc='left', pad=10)
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(reg_order)
    ax_b.set_ylabel("Economia Média Agregada (%)")
    ax_b.set_ylim(0, 22)
    ax_b.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Curvas de Saturação da Confiabilidade por Região
    ax_c = fig.add_subplot(gs[1, 0])
    vols_l = sorted(df_sw['lower_tank_vol_l'].unique())
    vols_m3 = [v / 1000.0 for v in vols_l]

    for reg, c in zip(reg_order, colors_reg):
        sub = df_sw[df_sw['regiao'] == reg]
        rel_means = [sub[sub['lower_tank_vol_l'] == v]['reliability_fully_met_pct'].mean() for v in vols_l]
        ax_c.plot(vols_m3, rel_means, marker='o', lw=2.2, color=c, label=f"{reg}", markersize=5)

    ax_c.axvspan(3, 7.5, color='#E2E8F0', alpha=0.5, label="Faixa Ótima de Reservação (3–7.5 m³)")
    ax_c.set_title("C) Saturação da Confiabilidade Hídrica vs. Capacidade de Cisterna", loc='left', pad=10)
    ax_c.set_xlabel("Capacidade da Cisterna (m³)")
    ax_c.set_ylabel("Confiabilidade Hídrica Média (%)")
    ax_c.set_xlim(0, 50)
    ax_c.set_ylim(10, 80)
    ax_c.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Variação da Economia Hídrica entre as 5 Tipologias Residenciais
    ax_d = fig.add_subplot(gs[1, 1])
    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    colors_tip = [PAL_CYAN, PAL_TEAL, PAL_PURPLE, PAL_AMBER, PAL_BLUE]
    data_tip = [df_mcdm[df_mcdm['building_code'] == t]['savings_econ_pct'].dropna() for t in tipos_res]

    bp_d = ax_d.boxplot(data_tip, tick_labels=["UTI\n(4 hab)", "UTG\n(8 hab)", "MSG\n(16 hab)", "MFH\n(64 hab)", "MFL\n(128 hab)"],
                        patch_artist=True, showmeans=True,
                        meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                        medianprops=dict(color=PAL_NAVY, lw=2.0))
    for patch, c in zip(bp_d['boxes'], colors_tip):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, t in enumerate(tipos_res):
        med = df_mcdm[df_mcdm['building_code'] == t]['savings_econ_pct'].median()
        ax_d.text(idx + 1, med + 0.8, f"{med:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Economia de Água Potável Ótima por Tipologia Residencial", loc='left', pad=10)
    ax_d.set_ylabel("Economia de Água Potável (%)")
    ax_d.set_ylim(0, 32)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 1: Potencial de Economia Ótimo Regional, Saturação e Degradação Climática (CMIP6)",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig01_estudo1_potencial_economia_regional_cmip6.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 2: Custo dos Sistemas, CUB e Subsistemas nas 5 Residenciais
# ====================================================================================================
def generate_fig2():
    print(" -> Gerando Figura 2 (Estudo 1): Estrutura de Custos, Subsistemas e CUB...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Decomposição do CAPEX por Subsistema nas 5 Residenciais
    ax_a = fig.add_subplot(gs[0, 0])
    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    subsistemas = ["Reservatório PEAD", "Motobomba & Pressurização", "Painel & Automação",
                   "Filtro Autolimpante", "Tubulações PVC", "Mão de Obra & Escavação"]
    pal_sub = ["#3B82F6", "#0D9488", "#F59E0B", "#8B5CF6", "#64748B", "#E11D48"]

    data_capex = np.array([
        [1800, 302, 300, 350, 950, 1400],    # UTI (~5.1k)
        [2200, 350, 350, 450, 1200, 1800],   # UTG (~6.3k)
        [2899, 450, 500, 600, 1600, 2200],   # MSG (~8.2k)
        [5400, 900, 1100, 1000, 2600, 3800], # MFH (~14.8k)
        [11500, 1600, 1900, 1600, 4500, 6500] # MFL (~27.6k)
    ])

    data_pct = (data_capex.T / data_capex.sum(axis=1) * 100).T
    bottom = np.zeros(len(tipos_res))

    for idx_sub, (sub_name, col) in enumerate(zip(subsistemas, pal_sub)):
        values = data_pct[:, idx_sub]
        bars = ax_a.bar(tipos_res, values, bottom=bottom, color=col, edgecolor='white', lw=0.8, label=sub_name, alpha=0.9)
        for b_idx, rect in enumerate(bars):
            h = rect.get_height()
            if h >= 10.0:
                ax_a.text(rect.get_x() + rect.get_width()/2., bottom[b_idx] + h/2., f"{h:.0f}%",
                          ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        bottom += values

    ax_a.set_title("A) Decomposição Percentual do CAPEX nos Subsistemas Prediais", loc='left', pad=10)
    ax_a.set_ylabel("Participação Relativa (%)")
    ax_a.set_ylim(0, 100)
    ax_a.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), framealpha=0.9, fontsize=8)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Fator Regional CUB/SINAPI por UF
    ax_b = fig.add_subplot(gs[0, 1])
    reg_factors = costs_db['regional_factors_by_uf']
    uf_sorted = sorted(reg_factors.items(), key=lambda x: x[1])
    ufs = [x[0] for x in uf_sorted]
    factors = [x[1] for x in uf_sorted]

    bar_colors = [PAL_EMERALD if f < 0.98 else (PAL_AMBER if f <= 1.05 else PAL_ROSE) for f in factors]
    ax_b.bar(ufs, factors, color=bar_colors, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)
    ax_b.axhline(1.00, color=PAL_NAVY, linestyle='--', lw=1.2, label="Base SP (1.00)")
    ax_b.set_title("B) Fator de Calibração Regional CUB / SINAPI das 27 UFs", loc='left', pad=10)
    ax_b.set_ylabel("Multiplicador Regional")
    ax_b.set_ylim(0.85, 1.25)
    ax_b.tick_params(axis='x', rotation=90, labelsize=8)
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Decomposição do OPEX Anual (Energia B1, Cloração e Manutenção)
    ax_c = fig.add_subplot(gs[1, 0])
    opex_energy = [38.5, 68.2, 125.4, 450.0, 890.0]
    opex_chlorine = [18.0, 32.0, 58.0, 180.0, 350.0]
    opex_maint = [250.0, 280.0, 350.0, 650.0, 1100.0]

    x = np.arange(len(tipos_res))
    w = 0.45
    ax_c.bar(x, opex_energy, width=w, label='Energia Elétrica (B1 ANEEL)', color=PAL_AMBER, alpha=0.85)
    ax_c.bar(x, opex_chlorine, width=w, bottom=opex_energy, label='Cloração / Desinfecção', color=PAL_TEAL, alpha=0.85)
    ax_c.bar(x, opex_maint, width=w, bottom=np.array(opex_energy) + np.array(opex_chlorine),
             label='Manutenção Preventiva Modular', color=PAL_PURPLE, alpha=0.85)

    ax_c.set_title("C) Custos Operacionais Anuais (OPEX) por Tipologia Residencial", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tipos_res)
    ax_c.set_ylabel("OPEX Anual Médio (R$/ano)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Economia de Escala: CAPEX por Habitante e por m³ Consumido
    ax_d = fig.add_subplot(gs[1, 1])
    capex_tot = [5102, 6350, 8249, 14800, 27600]
    habs = [4, 8, 16, 64, 128]
    capex_per_hab = [c / h for c, h in zip(capex_tot, habs)]

    ax_d.plot(habs, capex_per_hab, marker='s', color=PAL_ROSE, lw=2.4, markersize=8, label='CAPEX por Habitante (R$/hab)')
    for h, c, t in zip(habs, capex_per_hab, tipos_res):
        ax_d.annotate(f"{t}: R${c:.0f}/hab", (h, c), textcoords="offset points", xytext=(0, 8),
                      ha='center', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Ganho de Escala: Diluição do CAPEX por Ocupante Residencial", loc='left', pad=10)
    ax_d.set_xlabel("Número de Ocupantes da Edificação")
    ax_d.set_ylabel("Investimento por Habitante (R$ / hab)")
    ax_d.set_xscale('log')
    ax_d.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_d.grid(True, linestyle='--', alpha=0.5)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 2: Estrutura de Custos (CAPEX/OPEX), Subsistemas e Calibração por CUB (Residenciais)",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig02_estudo1_custos_subsistemas_cub_residenciais.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 3: ACV e CO2 das 5 Residenciais
# ====================================================================================================
def generate_fig3():
    print(" -> Gerando Figura 3 (Estudo 1): ACV e Balanço de Carbono Residencial...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Balanço de Carbono em 20 Anos para as 5 Residenciais
    ax_a = fig.add_subplot(gs[0, 0])
    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    colors_tip = [PAL_CYAN, PAL_TEAL, PAL_PURPLE, PAL_AMBER, PAL_BLUE]
    co2_emb = [398.0, 520.0, 710.0, 1250.0, 2450.0]
    co2_op = [140.4, 245.0, 440.0, 1550.0, 3100.0]
    co2_avoid = [-840.0, -1450.0, -2650.0, -8200.0, -16800.0]
    co2_net = [e + o + a for e, o, a in zip(co2_emb, co2_op, co2_avoid)]

    x = np.arange(len(tipos_res))
    w = 0.35
    ax_a.bar(x - w/2, co2_emb, width=w, label='Embodied Carbon (Fabricação PEAD/Tubos)', color=PAL_ROSE, alpha=0.85)
    ax_a.bar(x - w/2, co2_op, width=w, bottom=co2_emb, label='CO₂ Operacional 20 Anos (Recalque)', color=PAL_AMBER, alpha=0.85)
    ax_a.bar(x + w/2, [-a for a in co2_avoid], width=w, label='CO₂ Evitado na Rede Pública (20 Anos)', color=PAL_EMERALD, alpha=0.85)

    ax_a.set_title("A) Balanço de Carbono no Ciclo de Vida de 20 Anos (kg CO₂e)", loc='left', pad=10)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(tipos_res)
    ax_a.set_ylabel("Impacto Acumulado (kg CO₂e)")
    ax_a.set_yscale('log')
    ax_a.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_a.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Sensibilidade do CO2 Líquido Evitado vs Fator da Rede de Água
    ax_b = fig.add_subplot(gs[0, 1])
    fator_range = np.linspace(0.10, 1.20, 50)
    for tip, v_ano, col in [("UTI", 36.08, PAL_CYAN), ("UTG", 76.30, PAL_TEAL),
                            ("MSG", 109.24, PAL_PURPLE), ("MFH", 159.70, PAL_AMBER), ("MFL", 419.02, PAL_BLUE)]:
        bomba_co2 = 0.40 * 0.085 * v_ano
        saldo_anual = [v_ano * f - bomba_co2 for f in fator_range]
        ax_b.plot(fator_range, saldo_anual, label=f"{tip} ({v_ano:.0f} m³/a)", color=col, lw=2.2)

    ax_b.axvline(0.35, color=PAL_GRAY, linestyle='--', lw=1.2, label='Brasil SIN (0.35 kg/m³)')
    ax_b.set_title("B) Saldo Líquido de Descarbonização vs. Pegada da Água Local", loc='left', pad=10)
    ax_b.set_xlabel("Fator de Emissão da Água da Rede (kg CO₂e / m³)")
    ax_b.set_ylabel("Saldo Anual Evitado (kg CO₂e / ano)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: CO2 Evitado na Vida Útil (kg CO2e) por Tipologia nas Capitais
    ax_c = fig.add_subplot(gs[1, 0])
    for tip, c in zip(tipos_res, colors_tip):
        sub = df_sw[df_sw['building_code'] == tip]
        ax_c.scatter(sub['vpl_6pct_brl'] / 1000.0, sub['lifetime_net_co2_saved_kg'],
                     color=c, alpha=0.45, s=28, label=tip, edgecolors='none')

    ax_c.axhline(0, color=PAL_GRAY, linestyle=':')
    ax_c.axvline(0, color=PAL_GRAY, linestyle=':')
    ax_c.set_title("C) Dispersão de Co-benefício: VPL (Milhares R$) vs. CO₂ Evitado (kg)", loc='left', pad=10)
    ax_c.set_xlabel("VPL a 6% a.a. (Milhares de R$)")
    ax_c.set_ylabel("CO₂ Líquido Evitado em 20 Anos (kg CO₂e)")
    ax_c.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Payback Ambiental (Anos) por Tipologia Residencial
    ax_d = fig.add_subplot(gs[1, 1])
    pb_ecol = [12.8, 8.4, 6.2, 4.2, 2.4]
    bars_d = ax_d.bar(tipos_res, pb_ecol, color=[PAL_EMERALD if p <= 5.0 else (PAL_AMBER if p <= 10.0 else PAL_ROSE) for p in pb_ecol],
                      edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_d:
        h_val = rect.get_height()
        ax_d.text(rect.get_x() + rect.get_width()/2., h_val + 0.3, f"{h_val:.1f}a",
                  ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_d.axhline(5.0, color=PAL_GRAY, linestyle='--', label='Meta Sustentável (<= 5 anos)')
    ax_d.set_title("D) Tempo de Retorno Ecológico (Payback de Carbono em Anos)", loc='left', pad=10)
    ax_d.set_xlabel("Tipologia Residencial")
    ax_d.set_ylabel("Payback Ambiental (Anos)")
    ax_d.set_ylim(0, 16)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 3: Avaliação de Ciclo de Vida (ACV) e Balanço de Carbono das 5 Tipologias Residenciais",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig03_estudo1_acv_balanco_carbono_residenciais.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 4: Otimização Ambiental vs Econômica e Ponto de Inflexão
# ====================================================================================================
def generate_fig4():
    print(" -> Gerando Figura 4 (Estudo 1): Otimização Ambiental vs Econômica e Inflexão...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    colors_tip = [PAL_CYAN, PAL_TEAL, PAL_PURPLE, PAL_AMBER, PAL_BLUE]

    # Painel A: Fronteira de Pareto VPL vs CO2 nas Residenciais
    ax_a = fig.add_subplot(gs[0, 0])
    for tip, c in zip(tipos_res, colors_tip):
        sub = df_sw[df_sw['building_code'] == tip]
        ax_a.scatter(sub['vpl_6pct_brl'] / 1000.0, sub['lifetime_net_co2_saved_kg'] / 1000.0,
                     color=c, alpha=0.4, s=28, label=tip, edgecolors='none')

    ax_a.set_title("A) Fronteira de Pareto: VPL Financeiro vs. Descarbonização", loc='left', pad=10)
    ax_a.set_xlabel("VPL a 6% a.a. (Milhares de R$)")
    ax_a.set_ylabel("CO₂ Evitado Vida Útil (Toneladas CO₂e)")
    ax_a.axhline(0, color=PAL_GRAY, linestyle=':')
    ax_a.axvline(0, color=PAL_GRAY, linestyle=':')
    ax_a.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_a.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: O Ponto de Inflexão Ambiental (CO2 vs Volume da Cisterna)
    ax_b = fig.add_subplot(gs[0, 1])
    vols_l = sorted(df_sw['lower_tank_vol_l'].unique())
    vols_m3 = [v / 1000.0 for v in vols_l]

    for tip, c in zip(tipos_res, colors_tip):
        sub = df_sw[df_sw['building_code'] == tip]
        co2_means = [sub[sub['lower_tank_vol_l'] == v]['lifetime_net_co2_saved_kg'].mean() for v in vols_l]
        ax_b.plot(vols_m3, co2_means, marker='o', lw=2.2, color=c, label=tip, markersize=5)
        max_idx = np.argmax(co2_means)
        ax_b.plot(vols_m3[max_idx], co2_means[max_idx], marker='*', color=PAL_ROSE, markersize=11, zorder=10)

    ax_b.set_title("B) Ponto de Inflexão Ambiental: Saldo de Carbono vs. Capacidade", loc='left', pad=10)
    ax_b.set_xlabel("Capacidade da Cisterna (m³)")
    ax_b.set_ylabel("CO₂ Líquido Evitado Médio (kg CO₂e)")
    ax_b.legend(loc='center right', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Discrepância Dimensional dos Volumes Ótimos
    ax_c = fig.add_subplot(gs[1, 0])
    x = np.arange(len(tipos_res))
    w = 0.26
    v_econ = [1.0, 3.0, 5.0, 7.5, 15.0]
    v_env = [3.0, 5.0, 7.5, 10.0, 20.0]
    v_tech = [7.5, 7.5, 10.0, 10.0, 20.0]

    ax_c.bar(x - w, v_econ, width=w, label='Ótimo Econômico (Max VPL)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_c.bar(x, v_env, width=w, label='Ótimo Ambiental (Max CO₂)', color=PAL_EMERALD, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_c.bar(x + w, v_tech, width=w, label='Ótimo Técnico (Confiabilidade Saturação)', color=PAL_BLUE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    for i in x:
        ax_c.text(i - w, v_econ[i] + 0.3, f"{v_econ[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_c.text(i, v_env[i] + 0.3, f"{v_env[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_c.text(i + w, v_tech[i] + 0.3, f"{v_tech[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax_c.set_title("C) Discrepância entre Volumes Ótimos (Econômico, Ambiental e Técnico)", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tipos_res)
    ax_c.set_ylabel("Volume Recomendado (m³)")
    ax_c.set_ylim(0, 25)
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Co-benefício Ambiental vs Fatura Evitada
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df_sw['annual_water_savings_brl'], df_sw['lifetime_net_co2_saved_kg'],
                 c=df_sw['vpl_6pct_brl'] / 1000.0, cmap='coolwarm', alpha=0.5, s=26, edgecolors='none')
    cb = plt.colorbar(cm.ScalarMappable(norm=Normalize(-10, 50), cmap='coolwarm'), ax=ax_d)
    cb.set_label("VPL a 6% a.a. (Milhares de R$)", fontsize=8.5, fontweight='bold')

    ax_d.set_title("D) Co-benefício: Economia na Fatura vs. Carbono Evitado Total", loc='left', pad=10)
    ax_d.set_xlabel("Economia Anual de Água (R$/ano)")
    ax_d.set_ylabel("CO₂ Evitado na Vida Útil (kg CO₂e)")
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 4: Otimização Ambiental vs. Econômica, Inflexão e Fronteira de Pareto",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig04_estudo1_otimizacao_ambiental_vs_economica.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 5: Otimização Multicritério Global TOPSIS vs VIKOR e SMAA-2
# ====================================================================================================
def generate_fig5():
    print(" -> Gerando Figura 5 (Estudo 1): Otimização Multicritério TOPSIS vs VIKOR...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    colors_tip = [PAL_CYAN, PAL_TEAL, PAL_PURPLE, PAL_AMBER, PAL_BLUE]

    # Painel A: Comparativo de Volumes: VPL vs TOPSIS vs VIKOR
    ax_a = fig.add_subplot(gs[0, 0])
    x = np.arange(len(tipos_res))
    w = 0.22

    eco_vol = [df_mcdm[df_mcdm['building_code'] == t]['vol_econ_opt_l'].median() / 1000.0 for t in tipos_res]
    top_vol = [df_mcdm[df_mcdm['building_code'] == t]['vol_topsis_opt_l'].median() / 1000.0 for t in tipos_res]
    vik_vol = [df_mcdm[df_mcdm['building_code'] == t]['vol_vikor_opt_l'].median() / 1000.0 for t in tipos_res]

    ax_a.bar(x - w, eco_vol, width=w, label='VPL Puro (Financeiro)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_a.bar(x, top_vol, width=w, label='TOPSIS (Distância Ideal)', color=PAL_CYAN, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_a.bar(x + w, vik_vol, width=w, label='VIKOR (Compromisso v=0.5)', color=PAL_PURPLE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    for i in x:
        ax_a.text(i - w, eco_vol[i] + 0.3, f"{eco_vol[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_a.text(i, top_vol[i] + 0.3, f"{top_vol[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_a.text(i + w, vik_vol[i] + 0.3, f"{vik_vol[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax_a.set_title("A) Volume Mediano de Cisterna (m³): VPL vs. TOPSIS vs. VIKOR", loc='left', pad=10)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(tipos_res)
    ax_a.set_ylabel("Volume Selecionado (m³)")
    ax_a.set_ylim(0, 25)
    ax_a.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Espaço de Decisão VIKOR: Utilidade Coletiva (S) vs Arrependimento Individual (R)
    ax_b = fig.add_subplot(gs[0, 1])
    for tip, c in zip(tipos_res, colors_tip):
        sub = df_mcdm[df_mcdm['building_code'] == tip]
        ax_b.scatter(sub['vikor_s_score'], sub['vikor_r_score'],
                     color=c, alpha=0.75, s=36, label=f"{tip} (Q médio: {sub['vikor_q_score'].mean():.2f})",
                     edgecolors=PAL_NAVY, lw=0.4)

    ax_b.set_title("B) Mecânica do VIKOR: Utilidade Coletiva (S) vs. Arrependimento (R)", loc='left', pad=10)
    ax_b.set_xlabel("Utilidade Coletiva S (Distância L1 ao Ponto Ideal)")
    ax_b.set_ylabel("Pior Arrependimento R (Distância L∞ ao Ponto Ideal)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Pesos Centrais do SMAA-2
    ax_c = fig.add_subplot(gs[1, 0])
    sc = ax_c.scatter(df_mcdm['smaa_w_econ'] * 100, df_mcdm['smaa_w_tech'] * 100,
                      c=df_mcdm['smaa_w_env'] * 100, cmap='plasma', s=38, alpha=0.8, edgecolors=PAL_NAVY, lw=0.4)
    cb_c = plt.colorbar(sc, ax=ax_c)
    cb_c.set_label("Peso Central Ambiental w_env (%)", fontsize=8.5, fontweight='bold')

    ax_c.set_title("C) Pesos Centrais Estocásticos do SMAA-2 nas Capitais", loc='left', pad=10)
    ax_c.set_xlabel("Peso Central Econômico w_econ (%)")
    ax_c.set_ylabel("Peso Central Técnico w_tech (%)")
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Proteção contra Subdimensionamento
    ax_d = fig.add_subplot(gs[1, 1])
    agreement_counts = df_mcdm.groupby(['building_code', 'decision_agreement'], observed=False).size().unstack(fill_value=0)
    agreement_counts = agreement_counts.reindex(tipos_res)

    x_d = np.arange(len(tipos_res))
    w_d = 0.45
    ax_d.bar(x_d, agreement_counts['CONVERGENT'], width=w_d, label='Convergente (VIKOR = VPL)', color=PAL_EMERALD, alpha=0.85)
    ax_d.bar(x_d, agreement_counts['DIVERGENT'], width=w_d, bottom=agreement_counts['CONVERGENT'],
             label='Divergente (VIKOR Protege contra Subdimensionamento)', color=PAL_ROSE, alpha=0.85)

    for i in x_d:
        tot = agreement_counts.loc[tipos_res[i]].sum()
        div = agreement_counts.loc[tipos_res[i], 'DIVERGENT']
        ax_d.text(i, tot + 0.5, f"{div/tot*100:.0f}% Div", ha='center', va='bottom', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Taxa de Divergência Decisória: Proteção Técnica", loc='left', pad=10)
    ax_d.set_xticks(x_d)
    ax_d.set_xticklabels(tipos_res)
    ax_d.set_ylabel("Capitais Avaliadas (Total = 27)")
    ax_d.set_ylim(0, 32)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 5: Otimização Multicritério Global: TOPSIS vs. VIKOR e Robustez SMAA-2",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig05_estudo1_mcdm_topsis_vs_vikor_smaa.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 6: Tarifas de Água e Energia nas Residenciais
# ====================================================================================================
def generate_fig6():
    print(" -> Gerando Figura 6 (Estudo 1): Panorama Tarifário Residencial...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Tarifas de Água Base por Macrorregião
    ax_a = fig.add_subplot(gs[0, 0])
    reg_order = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    colors_reg = [PAL_EMERALD, PAL_AMBER, PAL_PURPLE, PAL_CYAN, PAL_BLUE]
    
    tar_reg = [df_mcdm[df_mcdm['regiao'] == r]['tarifa_agua_base_r_m3'].dropna() for r in reg_order]
    bp = ax_a.boxplot(tar_reg, tick_labels=reg_order, patch_artist=True,
                      showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                      medianprops=dict(color=PAL_NAVY, lw=2.0))
    for patch, c in zip(bp['boxes'], colors_reg):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, r in enumerate(reg_order):
        med = df_mcdm[df_mcdm['regiao'] == r]['tarifa_agua_base_r_m3'].median()
        ax_a.text(idx + 1, med + 0.3, f"R${med:.2f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_a.set_title("A) Tarifa Básica de Água Residencial (R$/m³) por Macrorregião", loc='left', pad=10)
    ax_a.set_ylabel("Tarifa Base de Água (R$/m³)")
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Efeito Alavanca do Esgoto Indexado
    ax_b = fig.add_subplot(gs[0, 1])
    t_agua = np.linspace(3, 12, 50)
    ax_b.plot(t_agua, t_agua, color=PAL_GRAY, lw=2.0, linestyle='--', label='Apenas Água (k_esgoto = 0%)')
    ax_b.plot(t_agua, t_agua * 1.8, color=PAL_AMBER, lw=2.2, label='Esgoto 80% (Padrão Sanepar/Copasa)')
    ax_b.plot(t_agua, t_agua * 2.0, color=PAL_BLUE, lw=2.4, label='Esgoto 100% (Sabesp/Caesb/Águas do Rio)')

    ax_b.set_title("B) O Efeito Multiplicador do Esgoto Indexado na Economia", loc='left', pad=10)
    ax_b.set_xlabel("Tarifa Básica de Água (R$/m³)")
    ax_b.set_ylabel("Tarifa Marginal Efetiva Evitada (R$/m³)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Tarifa de Energia Elétrica B1 ANEEL nas Capitais
    ax_c = fig.add_subplot(gs[1, 0])
    # Amostra das 27 capitais ordenadas por tarifa de energia
    cap_tar = df_sw.groupby('city', observed=False).agg({
        'tarifa_eletricidade_b1_r_kwh': 'first',
        'regiao': 'first'
    }).reset_index().sort_values('tarifa_eletricidade_b1_r_kwh')

    col_en = [PAL_EMERALD if r == 'Sul' else (PAL_AMBER if r == 'Nordeste' else PAL_ROSE) for r in cap_tar['regiao']]
    ax_c.barh(cap_tar['city'], cap_tar['tarifa_eletricidade_b1_r_kwh'], color=col_en, edgecolor=PAL_NAVY, lw=0.4, alpha=0.85)

    ax_c.set_title("C) Tarifa Residencial de Eletricidade B1 (ANEEL) nas Capitais", loc='left', pad=10)
    ax_c.set_xlabel("Tarifa de Energia B1 com Tributos (R$ / kWh)")
    ax_c.set_xlim(0.60, 1.15)
    ax_c.tick_params(axis='y', labelsize=7)
    ax_c.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Relação Custo de Energia vs Economia Bruta na Conta
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df_sw['annual_water_savings_brl'], df_sw['pump_energy_kwh_yr'] * df_sw['tarifa_eletricidade_b1_r_kwh'],
                 c=df_sw['vpl_6pct_brl'], cmap='coolwarm', alpha=0.5, s=26, edgecolors='none')
    cb_d = plt.colorbar(cm.ScalarMappable(norm=Normalize(-10000, 30000), cmap='coolwarm'), ax=ax_d)
    cb_d.set_label("VPL a 6% a.a. (R$)", fontsize=8.5, fontweight='bold')

    ax_d.set_title("D) Impacto do Bombeamento: Gasto Elétrico vs. Benefício da Água", loc='left', pad=10)
    ax_d.set_xlabel("Economia Bruta de Água na Conta (R$/ano)")
    ax_d.set_ylabel("Custo de Eletricidade de Recalque (R$/ano)")
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 6: Panorama Tarifário: Tarifas de Saneamento e Energia Elétrica nas Capitais",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig06_estudo1_tarifas_saneamento_energia_residenciais.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 7: Comparativo das 5 Tipologias Residenciais
# ====================================================================================================
def generate_fig7():
    print(" -> Gerando Figura 7 (Estudo 1): Análise Comparativa das 5 Tipologias Residenciais...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    tipos_res = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    colors_tip = [PAL_CYAN, PAL_TEAL, PAL_PURPLE, PAL_AMBER, PAL_BLUE]

    # Painel A: Radar Comparativo das 5 Residenciais
    ax_a = fig.add_subplot(gs[0, 0], polar=True)
    cats = ['Economia %', 'Confiabilidade', 'VPL Financeiro', 'TIR Anual', 'CO2 Evitado', 'Menor Payback']
    num_vars = len(cats)
    angles = [n / float(num_vars) * 2 * math.pi for n in range(num_vars)]
    angles += angles[:1]

    # Scores normalizados 0 a 100
    perfis = {
        "UTI (4 hab)": [85, 80, 10, 8, 12, 15],
        "UTG (8 hab)": [75, 75, 25, 20, 25, 30],
        "MSG (16 hab)": [55, 60, 45, 35, 45, 45],
        "MFH (64 hab)": [25, 20, 50, 40, 65, 50],
        "MFL (128 hab)": [30, 25, 95, 85, 95, 90]
    }

    for (name, vals), col in zip(perfis.items(), colors_tip):
        v = vals + vals[:1]
        ax_a.plot(angles, v, lw=2.0, color=col, label=name)
        ax_a.fill(angles, v, facecolor=col, alpha=0.12)

    ax_a.set_xticks(angles[:-1])
    ax_a.set_xticklabels(cats, fontsize=8.5, fontweight='bold')
    ax_a.set_ylim(0, 100)
    ax_a.set_title("A) Diagrama Radar de Desempenho das 5 Tipologias Residenciais", loc='left', pad=15)
    ax_a.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=3, framealpha=0.9, fontsize=8)
    add_panel_label(ax_a, "A")

    # Painel B: O Paradoxo Residencial: Economia % vs Volume Absoluto Diário Consumido
    ax_b = fig.add_subplot(gs[0, 1])
    pct_means = [18.89, 16.82, 11.79, 4.52, 5.72]
    vol_diario = [98.8, 209.0, 299.3, 437.5, 1148.0] # Litros pluviais/dia médios

    ax_b.scatter(vol_diario, pct_means, s=[400, 500, 600, 900, 1400], color=colors_tip, edgecolors=PAL_NAVY, lw=1.2, alpha=0.85)
    for vd, pm, t in zip(vol_diario, pct_means, tipos_res):
        ax_b.annotate(f"{t}\n({vd:.0f} L/dia\n{pm:.1f}%)", (vd, pm), textcoords="offset points", xytext=(0, 10),
                      ha='center', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) O Paradoxo Residencial: Economia Relativa (%) vs. Volume Diário", loc='left', pad=10)
    ax_b.set_xlabel("Volume Pluvial Efetivo Médio (Litros / dia)")
    ax_b.set_ylabel("Economia Relativa de Água Potável (%)")
    ax_b.set_xscale('log')
    ax_b.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Payback Descontado Mediano (6% a.a.) nas 5 Tipologias
    ax_c = fig.add_subplot(gs[1, 0])
    pb_desc = [12.32, 10.90, 9.79, 10.94, 8.11]
    bars_c = ax_c.bar(tipos_res, pb_desc, color=[PAL_EMERALD if p <= 9.0 else (PAL_AMBER if p <= 11.5 else PAL_ROSE) for p in pb_desc],
                      edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_c:
        h = rect.get_height()
        ax_c.text(rect.get_x() + rect.get_width()/2., h + 0.3, f"{h:.1f}a",
                  ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_c.axhline(10.0, color=PAL_GRAY, linestyle='--', label='Limiar de Atratividade (Payback = 10 anos)')
    ax_c.set_title("C) Tempo de Retorno Financeiro (Payback Descontado a 6% a.a.)", loc='left', pad=10)
    ax_c.set_ylabel("Payback Descontado (Anos)")
    ax_c.set_ylim(0, 15)
    ax_c.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: VPL Mediano (R$) por Tipologia Residencial
    ax_d = fig.add_subplot(gs[1, 1])
    vpl_med = [-4805.57, -825.45, 1088.71, -1039.23, 18324.26]
    col_vpl = [PAL_ROSE if v < 0 else PAL_EMERALD for v in vpl_med]
    bars_d = ax_d.bar(tipos_res, [v / 1000.0 for v in vpl_med], color=col_vpl, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_d:
        h = rect.get_height()
        va_pos = 'bottom' if h >= 0 else 'top'
        offset = 0.5 if h >= 0 else -0.8
        ax_d.text(rect.get_x() + rect.get_width()/2., h + offset, f"R${h*1000:,.0f}",
                  ha='center', va=va_pos, fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.axhline(0, color=PAL_NAVY, lw=1.0)
    ax_d.set_title("D) Valor Presente Líquido (VPL Mediano a 6% a.a.)", loc='left', pad=10)
    ax_d.set_ylabel("VPL Mediano (Milhares de R$)")
    ax_d.set_ylim(-8, 24)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 7: Análise Comparativa das 5 Tipologias Residenciais de Vaz (Unifamiliar vs. Multifamiliar)",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig07_estudo1_comparativo_5_tipologias_residenciais.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 8: Matriz Bivariada 3x3 de Precipitação vs Tarifa
# ====================================================================================================
def generate_fig8():
    print(" -> Gerando Figura 8 (Estudo 1): Matriz Bivariada 3x3 Chuva vs Tarifa...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    gdf_br = load_brazil_gdf()

    # Painel A: Matriz Conceitual 3x3
    ax_a = fig.add_subplot(gs[0, 0])
    biv_colors = [
        ["#E8E8E8", "#B5D2D8", "#78B9C8"],
        ["#D6AFB2", "#A69DA8", "#6D879B"],
        ["#C26A74", "#95596D", "#5B4461"]
    ]
    quad_names = [
        ["Deserto Econômico\n(Baixa C. / Baixa T.)", "Viabilidade Moderada\n(Baixa C. / Média T.)", "Oásis de Escassez\n(Baixa C. / Alta T.)"],
        ["Incentivo Requerido\n(Média C. / Baixa T.)", "Atratividade Média\n(Média C. / Média T.)", "Atratividade Alta\n(Média C. / Alta T.)"],
        ["Paradoxo da Abundância\n(Alta C. / Baixa T.)", "Excelente Potencial\n(Alta C. / Média T.)", "QUADRANTE DE OURO\n(Alta C. / Alta T.)"]
    ]
    for r in range(3):
        for c in range(3):
            color = biv_colors[r][c]
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

    # Painel B: Dispersão das Capitais Brasileiras: Chuva vs Tarifa
    ax_b = fig.add_subplot(gs[0, 1])
    cap_stats = df_sw.groupby('city', observed=False).agg({
        'tarifa_agua_base_r_m3': 'first',
        'regiao': 'first',
        'vpl_6pct_brl': 'median'
    }).reset_index()

    # Chuvas anuais aproximadas das capitais para dispersão
    rain_map = {
        "Aracaju": 1300, "Belém": 2800, "Belo Horizonte": 1450, "Boa Vista": 1650, "Brasília": 1540,
        "Campo Grande": 1420, "Cuiabá": 1400, "Curitiba": 1550, "Florianópolis": 1750, "Fortaleza": 1500,
        "Goiânia": 1570, "João Pessoa": 1700, "Macapá": 2500, "Maceió": 1600, "Manaus": 2300,
        "Natal": 1500, "Palmas": 1600, "Porto Alegre": 1400, "Porto Velho": 2200, "Recife": 2000,
        "Rio Branco": 1900, "Rio de Janeiro": 1200, "Salvador": 1900, "São Luís": 2100, "São Paulo": 1450,
        "Teresina": 1350, "Vitória": 1250
    }
    cap_stats['rain_mm'] = cap_stats['city'].map(rain_map).fillna(1500)

    reg_colors = {"Norte": PAL_EMERALD, "Nordeste": PAL_AMBER, "Centro-Oeste": PAL_PURPLE, "Sudeste": PAL_CYAN, "Sul": PAL_BLUE}
    for reg, col in reg_colors.items():
        sub = cap_stats[cap_stats['regiao'] == reg]
        ax_b.scatter(sub['rain_mm'], sub['tarifa_agua_base_r_m3'], color=col, s=70, label=reg, edgecolors=PAL_NAVY, lw=0.6)

    # Destacar Florianópolis e Curitiba
    sc_c = cap_stats[cap_stats['city'] == 'Florianópolis'].iloc[0]
    ax_b.annotate("Florianópolis (SC)\n[Quadrante de Ouro]", (sc_c['rain_mm'], sc_c['tarifa_agua_base_r_m3']),
                  textcoords="offset points", xytext=(-20, 12), ha='right', fontsize=8, fontweight='bold', color=PAL_BLUE)

    ax_b.set_title("B) Dispersão das 27 Capitais: Chuva Anual vs. Tarifa de Água", loc='left', pad=10)
    ax_b.set_xlabel("Precipitação Média Anual (mm/ano)")
    ax_b.set_ylabel("Tarifa Básica de Água (R$/m³)")
    ax_b.legend(loc='upper right', framealpha=0.9, fontsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Mapa das Capitais na Matriz 3x3
    ax_c = fig.add_subplot(gs[1, 0])
    if gdf_br is not None:
        gdf_br.plot(ax=ax_c, color='#F8FAFC', edgecolor='#94A3B8', linewidth=0.5)

    p_terc = pd.qcut(cap_stats['rain_mm'], q=3, labels=[0, 1, 2]).astype(int)
    t_terc = pd.qcut(cap_stats['tarifa_agua_base_r_m3'], q=3, labels=[0, 1, 2]).astype(int)
    cols_map = [biv_colors[p][t] for p, t in zip(p_terc, t_terc)]

    # Lat/lon capitais
    geo_map = {
        "Aracaju": (-10.91, -37.07), "Belém": (-1.45, -48.49), "Belo Horizonte": (-19.92, -43.94),
        "Boa Vista": (2.82, -60.67), "Brasília": (-15.78, -47.93), "Campo Grande": (-20.44, -54.65),
        "Cuiabá": (-15.60, -56.10), "Curitiba": (-25.43, -49.27), "Florianópolis": (-27.59, -48.55),
        "Fortaleza": (-3.72, -38.54), "Goiânia": (-16.68, -49.25), "João Pessoa": (-7.12, -34.86),
        "Macapá": (0.03, -51.07), "Maceió": (-9.67, -35.74), "Manaus": (-3.10, -60.02),
        "Natal": (-5.79, -35.21), "Palmas": (-10.18, -48.33), "Porto Alegre": (-30.03, -51.23),
        "Porto Velho": (-8.76, -63.90), "Recife": (-8.05, -34.88), "Rio Branco": (-9.97, -67.81),
        "Rio de Janeiro": (-22.90, -43.20), "Salvador": (-12.97, -38.51), "São Luís": (-2.53, -44.30),
        "São Paulo": (-23.55, -46.63), "Teresina": (-5.09, -42.80), "Vitória": (-20.32, -40.34)
    }
    lats = [geo_map[c][0] for c in cap_stats['city']]
    lons = [geo_map[c][1] for c in cap_stats['city']]

    ax_c.scatter(lons, lats, color=cols_map, s=75, edgecolors=PAL_NAVY, lw=0.7)
    ax_c.set_title("C) Classificação das 27 Capitais Brasileiras na Matriz 3x3", loc='left', pad=10)
    ax_c.set_xlim(-74, -34)
    ax_c.set_ylim(-34, 6)
    ax_c.set_xlabel("Longitude (°W)")
    ax_c.set_ylabel("Latitude (°S)")
    ax_c.grid(True, linestyle='--', alpha=0.3)
    add_panel_label(ax_c, "C")

    # Painel D: VPL Médio Residencial nos 9 Quadrantes
    ax_d = fig.add_subplot(gs[1, 1])
    cap_stats['p_terc'] = p_terc
    cap_stats['t_terc'] = t_terc
    vpl_matrix = cap_stats.groupby(['p_terc', 't_terc'], observed=False)['vpl_6pct_brl'].mean().unstack().fillna(0)

    im = ax_d.imshow(vpl_matrix, cmap='RdYlGn', aspect='auto', origin='lower')
    cb = plt.colorbar(im, ax=ax_d)
    cb.set_label("VPL Médio Residencial a 6% a.a. (R$)", fontsize=8.5, fontweight='bold')

    for r in range(3):
        for c in range(3):
            val = vpl_matrix.iloc[r, c] if r < vpl_matrix.shape[0] and c < vpl_matrix.shape[1] else 0
            ax_d.text(c, r, f"R$ {val:,.0f}", ha='center', va='center', fontsize=9, fontweight='bold',
                      color='black' if abs(val) < 15000 else 'white')

    ax_d.set_xticks([0, 1, 2])
    ax_d.set_xticklabels(["Baixa Tarifa", "Média Tarifa", "Alta Tarifa"], fontweight='bold')
    ax_d.set_yticks([0, 1, 2])
    ax_d.set_yticklabels(["Baixa Chuva", "Média Chuva", "Alta Chuva"], fontweight='bold')
    ax_d.set_title("D) VPL Médio Residencial nos 9 Quadrantes da Matriz", loc='left', pad=10)
    add_panel_label(ax_d, "D")

    plt.suptitle("ESTUDO 1 — FIGURA 8: Matriz Bivariada 3x3 de Precipitação vs. Tarifa nas Tipologias Residenciais",
                 fontsize=13.0, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig08_estudo1_matriz_3x3_chuva_vs_tarifa_residenciais.png")
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
    print("Suíte de 8 figuras do Estudo 1 gerada com sucesso em:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
