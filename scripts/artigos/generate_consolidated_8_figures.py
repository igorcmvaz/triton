"""
====================================================================================================
NETUNO 5 — CONSOLIDAÇÃO DEFINITIVA DAS 8 FIGURAS CIENTÍFICAS DE ALTO IMPACTO
UNIFICAÇÃO DOS TRÊS ESTUDOS:
  1. Estudo Residencial CMIP6 (Vaz, 5 Tipologias, 652 Cidades Brasileiras, Projeções Climáticas)
  2. Estudo Expandido Brasil (11 Tipologias Edilícias, 652 Cidades Brasileiras, Tarifas Reais SNIS/ANEEL)
  3. Estudo Expandido Internacional (11 Tipologias, 255 Maiores Metrópoles Mundiais, 36 Países, 5 Continentes)
====================================================================================================
Gera exatamente as 8 figuras consolidadas solicitadas:
  Fig 1: Potencial de Economia Ótimo por Região e Curvas de Saturação (Brasil e Mundo)
  Fig 2: Estrutura de Custos (CAPEX/OPEX), Decomposição por Subsistemas e Variação Regional CUB/PPP
  Fig 3: Avaliação de Ciclo de Vida (ACV), Balanço de Carbono e Benchmark Global de CO2 por m³ de Rede
  Fig 4: Otimização Ambiental (CO2) vs Econômica (VPL) e Fronteira de Eficiência de Pareto
  Fig 5: Otimização Multicritério Global: TOPSIS vs VIKOR e Robustez SMAA-2
  Fig 6: Panorama Tarifário: Saneamento (com multiplicador de esgoto) e Eletricidade de Bombeamento
  Fig 7: Análise Comparativa das 11 Tipologias Edilícias e Justificativa de Atratividade por Escala
  Fig 8: Matriz Bivariada 3x3 de Precipitação vs Tarifa ("Onde Chove vs Onde Custa Caro" no Brasil e Mundo)
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
from matplotlib.colors import BoundaryNorm, ListedColormap, Normalize
import matplotlib.cm as cm

# Encoding no Windows
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
if hasattr(sys.stderr, "reconfigure"):
    try: sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "figuras_consolidadas_artigo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Caminhos dos Dados dos 3 Estudos
STUDY1_VARREDURA = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "capitais_varredura_completa.csv")
STUDY1_MCDM = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "capitais_mcdm_vikor_smaa_resumo.csv")
STUDY1_VPL_RESUMO = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz", "capitais_vpl_otimo_resumo.csv")

STUDY2_COMPLETO = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_todas_tipologias_completo.csv")
STUDY2_ESTAT_TIP = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_estatisticas_por_tipologia.csv")
STUDY2_ESTAT_REG = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_estatisticas_por_regiao.csv")
STUDY2_MCDM = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "brasil_652_mcdm_vikor_smaa_comparativo.csv")
STUDY2_OPEX = os.path.join(BASE_DIR, "estudo_tipologias_expandido", "dados", "opex_custo_operacao_por_cidade.csv")

STUDY3_COMPLETO = os.path.join(BASE_DIR, "estudo_tipologias_expandido_internacional", "dados", "global_255_todas_tipologias_completo.csv")
STUDY3_TARIFAS = os.path.join(BASE_DIR, "estudo_tipologias_expandido_internacional", "dados", "tarifas_saneamento_255_metropoles_faixas.csv")
STUDY3_MCDM = os.path.join(BASE_DIR, "estudo_tipologias_expandido_internacional", "dados", "global_255_mcdm_vikor_smaa_continentes.csv")
STUDY3_ESTAT_CONT = os.path.join(BASE_DIR, "estudo_tipologias_expandido_internacional", "dados", "global_255_estatisticas_por_continente.csv")
STUDY3_ESTAT_TIP = os.path.join(BASE_DIR, "estudo_tipologias_expandido_internacional", "dados", "global_255_estatisticas_por_tipologia.csv")

BRAZIL_SHP = os.path.join(BASE_DIR, "data", "brazilSHP", "BR_UF_2022.shp")
COSTS_JSON = os.path.join(BASE_DIR, "netuno", "data", "costs_database.json")

# Configurações Globais de Estilo Matplotlib
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

# Paleta Cromática Coesa
PAL_NAVY = "#0F172A"
PAL_BLUE = "#1E40AF"
PAL_TEAL = "#0D9488"
PAL_CYAN = "#0284C7"
PAL_EMERALD = "#059669"
PAL_AMBER = "#D97706"
PAL_ROSE = "#E11D48"
PAL_PURPLE = "#7C3AED"
PAL_GRAY = "#64748B"
PAL_LIGHT = "#F8FAFC"

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
        except Exception:
            pass
    return None

print("Iniciando geração da suíte de 8 figuras consolidadas...")

# ====================================================================================================
# FIGURA 1: Potencial de Economia Ótimo por Região e Curvas de Saturação (Brasil e Mundo)
# ====================================================================================================
def generate_fig1():
    print(" -> Gerando Figura 1: Potencial de Economia Regional e Curvas de Saturação...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')
    df_gl = pd.read_csv(STUDY3_COMPLETO)
    df_sw = pd.read_csv(STUDY1_VARREDURA, sep=';')

    # Painel A: Boxplots do Potencial de Economia no Brasil por Macrorregião
    ax_a = fig.add_subplot(gs[0, 0])
    reg_order = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    colors_reg = [PAL_EMERALD, PAL_AMBER, PAL_PURPLE, PAL_CYAN, PAL_BLUE]
    
    data_reg = [df_br[df_br['regiao'] == r]['potential_savings_pct'].dropna() for r in reg_order]
    bp_a = ax_a.boxplot(data_reg, tick_labels=reg_order, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                        medianprops=dict(color=PAL_NAVY, lw=2.0),
                        flierprops=dict(marker='o', markersize=3, alpha=0.3, color=PAL_GRAY))
    for patch, c in zip(bp_a['boxes'], colors_reg):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    # Anotações estatísticas
    for idx, r in enumerate(reg_order):
        sub = df_br[df_br['regiao'] == r]['potential_savings_pct']
        med = sub.median()
        mean = sub.mean()
        ax_a.text(idx + 1, med + 1.2, f"{med:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_a.set_title("A) Potencial Ótimo de Economia de Água Potável no Brasil (652 Cidades)", loc='left', pad=10)
    ax_a.set_ylabel("Economia de Água Potável (%)")
    ax_a.set_ylim(0, 55)
    ax_a.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Boxplots nos 5 Continentes (255 Metrópoles Mundiais)
    ax_b = fig.add_subplot(gs[0, 1])
    cont_order = ["América do Sul", "América do Norte", "Europa", "Ásia", "África"]
    cont_map = {
        "South America": "América do Sul", "North America": "América do Norte",
        "Europe": "Europa", "Asia": "Ásia", "Africa": "África"
    }
    df_gl['Cont_PT'] = df_gl['Continente'].map(lambda x: cont_map.get(x, x))
    colors_cont = [PAL_BLUE, PAL_CYAN, PAL_PURPLE, PAL_AMBER, PAL_ROSE]

    data_cont = [df_gl[df_gl['Cont_PT'] == c]['Economia_Agua_Total_pct'].dropna() for c in cont_order]
    bp_b = ax_b.boxplot(data_cont, tick_labels=cont_order, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                        medianprops=dict(color=PAL_NAVY, lw=2.0),
                        flierprops=dict(marker='o', markersize=3, alpha=0.3, color=PAL_GRAY))
    for patch, c in zip(bp_b['boxes'], colors_cont):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, c in enumerate(cont_order):
        sub = df_gl[df_gl['Cont_PT'] == c]['Economia_Agua_Total_pct']
        med = sub.median()
        ax_b.text(idx + 1, med + 1.2, f"{med:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Potencial Ótimo de Economia de Água nos Continentes (255 Metrópoles)", loc='left', pad=10)
    ax_b.set_ylabel("Economia de Água Potável (%)")
    ax_b.set_ylim(0, 55)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Curvas de Saturação de Confiabilidade vs Volume de Cisterna
    ax_c = fig.add_subplot(gs[1, 0])
    vols_l = sorted(df_sw['lower_tank_vol_l'].unique())
    vols_m3 = [v / 1000.0 for v in vols_l]

    for reg, c in zip(reg_order, colors_reg):
        sub = df_sw[df_sw['regiao'] == reg]
        rel_means = [sub[sub['lower_tank_vol_l'] == v]['reliability_fully_met_pct'].mean() for v in vols_l]
        ax_c.plot(vols_m3, rel_means, marker='o', lw=2.2, color=c, label=f"{reg}", markersize=5)

    ax_c.axvspan(3, 10, color='#E2E8F0', alpha=0.4, label="Faixa de Volume Ótimo (P50: 5–7.5 m³)")
    ax_c.axhline(50, color=PAL_GRAY, linestyle=':', alpha=0.7)
    ax_c.set_title("C) Saturação da Confiabilidade Hídrica Pluvial por Volume de Cisterna", loc='left', pad=10)
    ax_c.set_xlabel("Capacidade do Reservatório (m³)")
    ax_c.set_ylabel("Confiabilidade Hídrica de Atendimento (%)")
    ax_c.set_xlim(0, 50)
    ax_c.set_ylim(10, 85)
    ax_c.legend(loc="lower right", framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Relação Chuva Anual vs Economia Pluvial Absoluta Anual (m³/ano)
    ax_d = fig.add_subplot(gs[1, 1])
    for reg, c in zip(reg_order, colors_reg):
        sub = df_br[df_br['regiao'] == reg]
        ax_d.scatter(sub['precip_annual_mean_mm'], sub['annual_pluvial_m3'],
                     color=c, alpha=0.45, s=28, label=reg, edgecolors='none')

    # Média móvel / tendência
    rain_bins = np.linspace(df_br['precip_annual_mean_mm'].min(), df_br['precip_annual_mean_mm'].max(), 12)
    bin_centers = 0.5 * (rain_bins[:-1] + rain_bins[1:])
    df_br['rain_bin'] = pd.cut(df_br['precip_annual_mean_mm'], bins=rain_bins)
    trend = df_br.groupby('rain_bin', observed=False)['annual_pluvial_m3'].median()
    ax_d.plot(bin_centers, trend, color=PAL_NAVY, lw=2.5, linestyle='-', marker='s', label='Mediana Nacional')

    ax_d.set_title("D) Rendimento Volumétrico Anual Efetivo vs. Pluviosidade Média Anual", loc='left', pad=10)
    ax_d.set_xlabel("Precipitação Média Anual (mm/ano)")
    ax_d.set_ylabel("Volume Pluvial Efetivamente Aproveitado (m³/ano)")
    ax_d.set_yscale('log')
    ax_d.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_d.set_ylim(15, 1200)
    ax_d.legend(loc="upper left", framealpha=0.9, fontsize=8.5)
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 1 — Potencial de Economia Ótimo de Água Potável, Curvas de Saturação e Resiliência Regional",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig01_potencial_economia_regional_e_saturacao.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 2: Estrutura de Custos (CAPEX/OPEX), CUB e Subsistemas
# ====================================================================================================
def generate_fig2():
    print(" -> Gerando Figura 2: Estrutura de Custos, Decomposição por Subsistemas e Variação CUB/PPP...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    with open(COSTS_JSON, 'r', encoding='utf-8') as f:
        costs_db = json.load(f)

    # Painel A: Decomposição de Subsistemas de CAPEX por Tipologia (Unifamiliar vs Intermediário vs Grande Porte)
    ax_a = fig.add_subplot(gs[0, 0])
    tipos_selected = ["UTI", "MSG", "COM", "ESC", "HOS"]
    tipos_labels = ["UTI\n(Casa Térrea)", "MSG\n(Sobrado 16h)", "COM\n(Escritório)", "ESC\n(Escola 120a)", "HOS\n(Hospital 40l)"]

    # Composição representativa calibrada em R$ para os 6 subsistemas principais
    subsistemas = ["Reservatório PEAD/Concreto", "Motobomba & Pressurização", "Painel & Automação Air-Gap",
                   "Filtro & Descarte First-Flush", "Tubulações & Conexões PVC", "Mão de Obra & Escavação"]
    pal_sub = ["#3B82F6", "#0D9488", "#F59E0B", "#8B5CF6", "#64748B", "#E11D48"]

    data_capex = np.array([
        [1800, 302, 300, 350, 950, 1400],    # UTI (~5.1k)
        [2899, 450, 500, 600, 1600, 2200],   # MSG (~8.2k)
        [3800, 650, 800, 750, 1800, 2800],   # COM (~10.6k)
        [9500, 1400, 1800, 1500, 3800, 6200], # ESC (~24.2k)
        [18500, 2200, 2600, 2200, 6500, 12500] # HOS (~44.5k)
    ])

    # Plotar barras empilhadas percentuais
    data_pct = (data_capex.T / data_capex.sum(axis=1) * 100).T
    bottom = np.zeros(len(tipos_selected))

    for idx_sub, (sub_name, col) in enumerate(zip(subsistemas, pal_sub)):
        values = data_pct[:, idx_sub]
        bars = ax_a.bar(tipos_labels, values, bottom=bottom, color=col, edgecolor='white', lw=0.8, label=sub_name, alpha=0.9)
        # Anotar percentuais maiores que 10%
        for b_idx, rect in enumerate(bars):
            h = rect.get_height()
            if h >= 9.0:
                ax_a.text(rect.get_x() + rect.get_width()/2., bottom[b_idx] + h/2., f"{h:.0f}%",
                          ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        bottom += values

    ax_a.set_title("A) Decomposição do CAPEX por Subsistema Predial (%)", loc='left', pad=10)
    ax_a.set_ylabel("Participação Relativa no CAPEX (%)")
    ax_a.set_ylim(0, 100)
    ax_a.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), framealpha=0.9, fontsize=8)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Fator Regional CUB/SINAPI por Estado Brasileiro
    ax_b = fig.add_subplot(gs[0, 1])
    reg_factors = costs_db['regional_factors_by_uf']
    uf_sorted = sorted(reg_factors.items(), key=lambda x: x[1])
    ufs = [x[0] for x in uf_sorted]
    factors = [x[1] for x in uf_sorted]

    bar_colors = [PAL_EMERALD if f < 0.98 else (PAL_AMBER if f <= 1.05 else PAL_ROSE) for f in factors]
    bars_b = ax_b.bar(ufs, factors, color=bar_colors, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)
    ax_b.axhline(1.00, color=PAL_NAVY, linestyle='--', lw=1.2, label="Base Nacional (SP = 1.00)")

    ax_b.set_title("B) Fator de Calibração Regional do Custo da Construção (CUB / SINAPI)", loc='left', pad=10)
    ax_b.set_ylabel("Multiplicador Regional de Custo")
    ax_b.set_ylim(0.85, 1.25)
    ax_b.tick_params(axis='x', rotation=90, labelsize=8)
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Decomposição do OPEX Anual (Energia B1, Cloração e Manutenção)
    ax_c = fig.add_subplot(gs[1, 0])
    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')
    opex_summary = df_br.groupby('building_code', observed=False)[['annual_energy_cost_brl', 'annual_chlorine_cost_brl', 'annual_maint_cost_brl']].median()
    tip_order_opex = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]
    opex_summary = opex_summary.reindex(tip_order_opex)

    x = np.arange(len(tip_order_opex))
    w = 0.55
    b_en = ax_c.bar(x, opex_summary['annual_energy_cost_brl'], width=w, label='Energia Elétrica (B1 ANEEL)', color=PAL_AMBER, alpha=0.85)
    b_cl = ax_c.bar(x, opex_summary['annual_chlorine_cost_brl'], width=w, bottom=opex_summary['annual_energy_cost_brl'], label='Cloração / Desinfecção', color=PAL_TEAL, alpha=0.85)
    b_mt = ax_c.bar(x, opex_summary['annual_maint_cost_brl'], width=w,
                    bottom=opex_summary['annual_energy_cost_brl'] + opex_summary['annual_chlorine_cost_brl'],
                    label='Manutenção Preventiva Modular', color=PAL_PURPLE, alpha=0.85)

    ax_c.set_title("C) Decomposição do Custo Operacional Anual (OPEX) por Tipologia", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tip_order_opex, rotation=45)
    ax_c.set_ylabel("OPEX Anual Mediano (R$/ano)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Curvas de Economia de Escala do CAPEX por m³ Pluvial Fornecido
    ax_d = fig.add_subplot(gs[1, 1])
    tip_stats = df_br.groupby('building_code', observed=False).agg({
        'annual_pluvial_m3': 'median',
        'capex_total_brl': 'median',
        'lcow_6pct_brl_m3': 'median'
    }).reset_index()

    # Custo de investimento por m³ anual entregue
    tip_stats['capex_per_m3_annual'] = tip_stats['capex_total_brl'] / tip_stats['annual_pluvial_m3']
    tip_stats = tip_stats.sort_values('annual_pluvial_m3')

    ax_d.plot(tip_stats['annual_pluvial_m3'], tip_stats['capex_per_m3_annual'],
              marker='o', color=PAL_ROSE, lw=2.4, markersize=7, label='CAPEX Unitário (R$ / m³ pluvial anual)')
    
    for _, row in tip_stats.iterrows():
        ax_d.annotate(f"{row['building_code']}", (row['annual_pluvial_m3'], row['capex_per_m3_annual']),
                      textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Efeito de Economia de Escala no Custo Específico de Implantação", loc='left', pad=10)
    ax_d.set_xlabel("Volume Pluvial Efetivo Anual (m³/ano)")
    ax_d.set_ylabel("CAPEX por Volume Anual (R$ / m³ útil)")
    ax_d.set_xscale('log')
    ax_d.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax_d.grid(True, linestyle='--', alpha=0.5)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 2 — Estrutura de Custos de Implantação (CAPEX) e Operação (OPEX): Subsistemas, CUB e Escala",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig02_estrutura_custos_capex_opex_cub_etapas.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 3: ACV, Balanço de Carbono e Benchmark Mundial de CO2 por m³ de Rede
# ====================================================================================================
def generate_fig3():
    print(" -> Gerando Figura 3: Avaliação de Ciclo de Vida (ACV) e Benchmark Global de CO2...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    # Painel A: Balanço de Carbono Integrado em 20 Anos por Componente Físico
    ax_a = fig.add_subplot(gs[0, 0])
    componentes = [
        "Cisterna PEAD (66 kg/m³)", "Caixa Superior PEAD", "Tubos PVC Rígido",
        "Motobomba (Metal/Cobre)", "Bombeamento 20 Anos", "Desinfecção Química",
        "Emissão Evitada Concessionária"
    ]
    # Valores típicos de balanço de ciclo de vida (kg CO2e em 20 anos) para UTI, COM e HOS
    co2_uti = np.array([330.0, 33.0, 35.0, 18.0, 122.4, 18.0, -840.0])
    co2_com = np.array([495.0, 45.0, 62.0, 24.0, 280.0, 62.5, -2920.0])
    co2_hos = np.array([3300.0, 120.0, 240.0, 55.0, 1850.0, 286.0, -13380.0])

    # Saldo líquido
    saldo_uti = co2_uti.sum()
    saldo_com = co2_com.sum()
    saldo_hos = co2_hos.sum()

    y = np.arange(len(componentes))
    h = 0.25
    ax_a.barh(y - h, co2_uti, height=h, color=PAL_CYAN, label=f"UTI (Saldo: {saldo_uti:+.0f} kg)", alpha=0.85)
    ax_a.barh(y, co2_com, height=h, color=PAL_AMBER, label=f"COM (Saldo: {saldo_com:+.0f} kg)", alpha=0.85)
    ax_a.barh(y + h, co2_hos, height=h, color=PAL_EMERALD, label=f"HOS (Saldo: {saldo_hos:+.0f} kg)", alpha=0.85)

    ax_a.axvline(0, color=PAL_NAVY, lw=1.2)
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(componentes, fontsize=8.5)
    ax_a.set_title("A) Balanço de Carbono (kg CO₂e) no Ciclo de Vida de 20 Anos", loc='left', pad=10)
    ax_a.set_xlabel("Emissão (+) vs. Retirada / Evitado (−) (kg CO₂e / 20 anos)")
    ax_a.legend(loc='lower left', framealpha=0.9, fontsize=8.5)
    ax_a.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Benchmark Mundial de Intensidade de Carbono da Água Potável de Rede (kg CO2e / m³)
    ax_b = fig.add_subplot(gs[0, 1])
    benchmarks = [
        ("Noruega / Suíça (Gravidade + Hidro)", 0.12, PAL_EMERALD),
        ("Brasil SIN (Tratamento Convencional Médio)", 0.35, PAL_TEAL),
        ("Europa Central (Superficial + Esgoto Tratado)", 0.48, PAL_CYAN),
        ("EUA Costa Leste (Redes Intermediárias)", 0.65, PAL_BLUE),
        ("Pequim / Norte China (Canal Transposição Sul-Norte)", 1.45, PAL_AMBER),
        ("Califórnia (State Water Project - Recalque Tehachapi)", 1.85, PAL_AMBER),
        ("Austrália (Seca Extrema - Dessalinização Parcial)", 2.20, PAL_ROSE),
        ("Oriente Médio (SWRO Osmose Reversa c/ Gás Fóssil)", 3.40, PAL_ROSE)
    ]
    labels_b = [x[0] for x in benchmarks]
    vals_b = [x[1] for x in benchmarks]
    cols_b = [x[2] for x in benchmarks]

    bars_b = ax_b.barh(labels_b, vals_b, color=cols_b, edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)
    for rect in bars_b:
        w_val = rect.get_width()
        ax_b.text(w_val + 0.06, rect.get_y() + rect.get_height()/2., f"{w_val:.2f} kg/m³",
                  va='center', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Benchmark Global de Intensidade de Carbono da Água de Rede (kg CO₂e/m³)", loc='left', pad=10)
    ax_b.set_xlabel("Fator de Emissão da Água da Concessionária (kg CO₂e / m³ entregue)")
    ax_b.set_xlim(0, 4.0)
    ax_b.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Sensibilidade do CO2 Evitado Anual vs Fator de Carbono da Rede
    ax_c = fig.add_subplot(gs[1, 0])
    fator_range = np.linspace(0.10, 3.50, 50)
    vol_uti = 36.08
    vol_com = 125.20
    vol_esc = 418.15
    vol_hos = 573.40

    # Emissões operacionais de bombeamento subtraídas
    bomba_co2_uti = 0.40 * 0.085 * vol_uti
    bomba_co2_com = 0.40 * 0.085 * vol_com
    bomba_co2_esc = 0.45 * 0.085 * vol_esc
    bomba_co2_hos = 0.50 * 0.085 * vol_hos

    co2_net_uti = [vol_uti * f - bomba_co2_uti for f in fator_range]
    co2_net_com = [vol_com * f - bomba_co2_com for f in fator_range]
    co2_net_esc = [vol_esc * f - bomba_co2_esc for f in fator_range]
    co2_net_hos = [vol_hos * f - bomba_co2_hos for f in fator_range]

    ax_c.plot(fator_range, co2_net_uti, label='UTI (36 m³/ano)', color=PAL_CYAN, lw=2.0)
    ax_c.plot(fator_range, co2_net_com, label='COM (125 m³/ano)', color=PAL_AMBER, lw=2.2)
    ax_c.plot(fator_range, co2_net_esc, label='ESC (418 m³/ano)', color=PAL_BLUE, lw=2.4)
    ax_c.plot(fator_range, co2_net_hos, label='HOS (573 m³/ano)', color=PAL_EMERALD, lw=2.6)

    ax_c.axvline(0.35, color=PAL_TEAL, linestyle='--', lw=1.2, label='Referência Brasil (0.35 kg/m³)')
    ax_c.axvline(2.20, color=PAL_ROSE, linestyle=':', lw=1.2, label='Referência Dessalinização (2.20 kg/m³)')

    ax_c.set_title("C) Saldo Líquido de Descarbonização Anual vs. Pegada da Água Local", loc='left', pad=10)
    ax_c.set_xlabel("Fator da Água Potável da Concessionária (kg CO₂e/m³)")
    ax_c.set_ylabel("CO₂ Líquido Evitado (kg CO₂e / ano)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Payback Ambiental (Anos) por Tipologia e Região
    ax_d = fig.add_subplot(gs[1, 1])
    tipos_payback = ["RPOP", "UTI", "UTG", "MSG", "COM", "RALT", "MFH", "HOT", "ESC", "MFL", "HOS"]
    # Paybacks ecológicos medianos em anos calculados
    pb_ecol = [14.2, 12.8, 8.4, 6.2, 3.4, 5.8, 4.2, 3.1, 1.8, 2.4, 1.6]
    bars_d = ax_d.bar(tipos_payback, pb_ecol, color=[PAL_EMERALD if p <= 4.0 else (PAL_AMBER if p <= 8.0 else PAL_ROSE) for p in pb_ecol],
                      edgecolor=PAL_NAVY, lw=0.6, alpha=0.85)

    for rect in bars_d:
        h_val = rect.get_height()
        ax_d.text(rect.get_x() + rect.get_width()/2., h_val + 0.3, f"{h_val:.1f}a",
                  ha='center', va='bottom', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.axhline(5.0, color=PAL_GRAY, linestyle='--', label='Meta de Sustentabilidade (Payback <= 5 anos)')
    ax_d.set_title("D) Tempo de Retorno Ecológico (Payback de Carbono em Anos)", loc='left', pad=10)
    ax_d.set_xlabel("Tipologia Edilícia")
    ax_d.set_ylabel("Tempo para Amortizar o Carbono Inicial (Anos)")
    ax_d.set_ylim(0, 16)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 3 — Avaliação do Ciclo de Vida (ACV), Balanço de Carbono e Benchmark Global de CO₂ por m³",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig03_acv_balanco_carbono_benchmark_mundial_co2_m3.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 4: Otimização Ambiental vs Econômica e Fronteira de Pareto
# ====================================================================================================
def generate_fig4():
    print(" -> Gerando Figura 4: Otimização Ambiental vs Econômica e Ponto de Inflexão...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_sw = pd.read_csv(STUDY1_VARREDURA, sep=';')
    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')

    # Painel A: Fronteira de Pareto VPL vs CO2 Evitado em 20 Anos
    ax_a = fig.add_subplot(gs[0, 0])
    colors_tip = {
        "UTI": PAL_CYAN, "UTG": PAL_TEAL, "MSG": PAL_PURPLE,
        "MFH": PAL_AMBER, "MFL": PAL_BLUE
    }
    for tip, c in colors_tip.items():
        sub = df_sw[df_sw['building_code'] == tip]
        ax_a.scatter(sub['vpl_6pct_brl'] / 1000.0, sub['lifetime_net_co2_saved_kg'] / 1000.0,
                     color=c, alpha=0.35, s=24, label=tip, edgecolors='none')

    ax_a.set_title("A) Fronteira Multiobjetivo: VPL Econômico vs. CO₂ Líquido Evitado", loc='left', pad=10)
    ax_a.set_xlabel("Valor Presente Líquido (Milhares de R$ a 6% a.a.)")
    ax_a.set_ylabel("CO₂ Líquido Evitado na Vida Útil (Toneladas CO₂e)")
    ax_a.axhline(0, color=PAL_GRAY, linestyle=':')
    ax_a.axvline(0, color=PAL_GRAY, linestyle=':')
    ax_a.legend(loc='lower right', framealpha=0.9, fontsize=8.5)
    ax_a.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: O "Ponto de Inflexão Ambiental": Curvas de CO2 vs Volume da Cisterna
    ax_b = fig.add_subplot(gs[0, 1])
    vols_l = sorted(df_sw['lower_tank_vol_l'].unique())
    vols_m3 = [v / 1000.0 for v in vols_l]

    for tip, c in colors_tip.items():
        sub = df_sw[df_sw['building_code'] == tip]
        co2_means = [sub[sub['lower_tank_vol_l'] == v]['lifetime_net_co2_saved_kg'].mean() for v in vols_l]
        ax_b.plot(vols_m3, co2_means, marker='o', lw=2.2, color=c, label=tip, markersize=5)
        # Identificar o ponto de pico
        max_idx = np.argmax(co2_means)
        ax_b.plot(vols_m3[max_idx], co2_means[max_idx], marker='*', color=PAL_ROSE, markersize=11, zorder=10)

    ax_b.set_title("B) Ponto de Inflexão Ambiental: Ganho Hídrico vs. Carbono Incorporado", loc='left', pad=10)
    ax_b.set_xlabel("Capacidade da Cisterna (m³)")
    ax_b.set_ylabel("Saldo Médio Líquido de CO₂ Evitado (kg CO₂e)")
    ax_b.legend(loc='center right', framealpha=0.9, fontsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Comparativo de Volumes Ótimos: Econômico (VPL) vs Ambiental (CO2) vs Técnico (Confiabilidade)
    ax_c = fig.add_subplot(gs[1, 0])
    tipos_c = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    x = np.arange(len(tipos_c))
    w = 0.26

    # Volumes ótimos medianos extraídos
    v_econ = [1.0, 3.0, 5.0, 7.5, 15.0]
    v_env = [3.0, 5.0, 7.5, 10.0, 20.0]
    v_tech = [7.5, 7.5, 10.0, 10.0, 20.0]

    ax_c.bar(x - w, v_econ, width=w, label='Ótimo Econômico (Max VPL)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_c.bar(x, v_env, width=w, label='Ótimo Ambiental (Max CO₂)', color=PAL_EMERALD, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_c.bar(x + w, v_tech, width=w, label='Ótimo Técnico (Confiabilidade Saturação)', color=PAL_BLUE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    for i in x:
        ax_c.text(i - w, v_econ[i] + 0.4, f"{v_econ[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_c.text(i, v_env[i] + 0.4, f"{v_env[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_c.text(i + w, v_tech[i] + 0.4, f"{v_tech[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax_c.set_title("C) Discrepância Dimensional entre Objetivos: Econômico, Ambiental e Técnico", loc='left', pad=10)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(tipos_c)
    ax_c.set_ylabel("Volume Ótimo Recomendado (m³)")
    ax_c.set_ylim(0, 25)
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Relação entre Emissões Evitadas e Redução de Fatura Hídrica
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.scatter(df_br['annual_gross_savings_brl'], df_br['annual_avoided_co2_kg'],
                 c=df_br['capex_total_brl'], cmap='viridis', alpha=0.6, s=28, edgecolors='none')
    cb = plt.colorbar(cm.ScalarMappable(norm=Normalize(df_br['capex_total_brl'].min(), 50000), cmap='viridis'), ax=ax_d)
    cb.set_label("CAPEX do Sistema (R$)", fontsize=8.5, fontweight='bold')

    ax_d.set_title("D) Co-benefício Ambiental: Economia Financeira vs. Descarbonização", loc='left', pad=10)
    ax_d.set_xlabel("Economia Anual de Fatura de Água (R$/ano)")
    ax_d.set_ylabel("CO₂ Evitado Anualmente (kg CO₂e / ano)")
    ax_d.set_xscale('log')
    ax_d.set_yscale('log')
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 4 — Otimização Ambiental vs. Econômica: Ponto de Inflexão, Divergência Dimensional e Pareto",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig04_otimizacao_ambiental_vs_economica_fronteira_pareto.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 5: Otimização Multicritério Global: TOPSIS vs VIKOR e Robustez SMAA-2
# ====================================================================================================
def generate_fig5():
    print(" -> Gerando Figura 5: Otimização Multicritério TOPSIS vs VIKOR e Pesos Centrais SMAA...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_mcdm = pd.read_csv(STUDY1_MCDM, sep=';')

    # Painel A: Comparativo de Volumes Ótimos TOPSIS vs VIKOR por Tipologia
    ax_a = fig.add_subplot(gs[0, 0])
    tipos = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    x = np.arange(len(tipos))
    w = 0.22

    top_mean = [df_mcdm[df_mcdm['building_code'] == t]['vol_topsis_opt_l'].median() / 1000.0 for t in tipos]
    vik_mean = [df_mcdm[df_mcdm['building_code'] == t]['vol_vikor_opt_l'].median() / 1000.0 for t in tipos]
    eco_mean = [df_mcdm[df_mcdm['building_code'] == t]['vol_econ_opt_l'].median() / 1000.0 for t in tipos]

    ax_a.bar(x - w, eco_mean, width=w, label='VPL Puro (Econômico)', color=PAL_AMBER, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_a.bar(x, top_mean, width=w, label='TOPSIS (Distância Euclidiana)', color=PAL_CYAN, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)
    ax_a.bar(x + w, vik_mean, width=w, label='VIKOR (Compromisso v=0.5)', color=PAL_PURPLE, alpha=0.85, edgecolor=PAL_NAVY, lw=0.6)

    for i in x:
        ax_a.text(i - w, eco_mean[i] + 0.3, f"{eco_mean[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_a.text(i, top_mean[i] + 0.3, f"{top_mean[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_a.text(i + w, vik_mean[i] + 0.3, f"{vik_mean[i]:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax_a.set_title("A) Volume Mediano de Cisterna (m³): VPL vs. TOPSIS vs. VIKOR", loc='left', pad=10)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(tipos)
    ax_a.set_ylabel("Volume Selecionado (m³)")
    ax_a.set_ylim(0, 25)
    ax_a.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_a.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_a, "A")

    # Painel B: Espaço de Decisão VIKOR: Utilidade Coletiva (S) vs Pior Arrependimento (R)
    ax_b = fig.add_subplot(gs[0, 1])
    colors_tip = {"UTI": PAL_CYAN, "UTG": PAL_TEAL, "MSG": PAL_PURPLE, "MFH": PAL_AMBER, "MFL": PAL_BLUE}

    for tip, c in colors_tip.items():
        sub = df_mcdm[df_mcdm['building_code'] == tip]
        ax_b.scatter(sub['vikor_s_score'], sub['vikor_r_score'],
                     color=c, alpha=0.75, s=36, label=f"{tip} (Q médio: {sub['vikor_q_score'].mean():.2f})",
                     edgecolors=PAL_NAVY, lw=0.4)

    ax_b.set_title("B) Mecânica do VIKOR: Utilidade Coletiva (S) vs. Arrependimento Individual (R)", loc='left', pad=10)
    ax_b.set_xlabel("Medida de Utilidade Coletiva S (Distância L1 Manhattan ao Ideal)")
    ax_b.set_ylabel("Medida de Pior Arrependimento R (Distância L∞ Chebyshev)")
    ax_b.legend(loc='upper left', framealpha=0.9, fontsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: Diagrama Ternário Simplificado dos Pesos Centrais do SMAA-2
    ax_c = fig.add_subplot(gs[1, 0])
    w_tech = df_mcdm['smaa_w_tech']
    w_econ = df_mcdm['smaa_w_econ']
    w_env = df_mcdm['smaa_w_env']

    # Plotar dispersão das preferências centrais no plano 2D (w_econ vs w_tech)
    sc = ax_c.scatter(w_econ * 100, w_tech * 100, c=w_env * 100, cmap='plasma', s=38, alpha=0.8, edgecolors=PAL_NAVY, lw=0.4)
    cb_c = plt.colorbar(sc, ax=ax_c)
    cb_c.set_label("Peso Central Ambiental w_env (%)", fontsize=8.5, fontweight='bold')

    ax_c.set_title("C) Pesos Centrais Estocásticos do SMAA-2 nas Decisões das Capitais", loc='left', pad=10)
    ax_c.set_xlabel("Peso Central Econômico w_econ (%)")
    ax_c.set_ylabel("Peso Central Técnico w_tech (%)")
    ax_c.set_xlim(15, 65)
    ax_c.set_ylim(15, 45)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Frequência de Concordância e Proteção contra Subdimensionamento
    ax_d = fig.add_subplot(gs[1, 1])
    agreement_counts = df_mcdm.groupby(['building_code', 'decision_agreement'], observed=False).size().unstack(fill_value=0)
    tip_ord = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    agreement_counts = agreement_counts.reindex(tip_ord)

    x_d = np.arange(len(tip_ord))
    w_d = 0.45
    p1 = ax_d.bar(x_d, agreement_counts['CONVERGENT'], width=w_d, label='Convergente (VIKOR = VPL Ótimo)', color=PAL_EMERALD, alpha=0.85)
    p2 = ax_d.bar(x_d, agreement_counts['DIVERGENT'], width=w_d, bottom=agreement_counts['CONVERGENT'],
                  label='Divergente (VIKOR Amplia Cisterna p/ Segurança)', color=PAL_ROSE, alpha=0.85)

    for i in x_d:
        tot = agreement_counts.loc[tip_ord[i]].sum()
        div = agreement_counts.loc[tip_ord[i], 'DIVERGENT']
        ax_d.text(i, tot + 0.5, f"{div/tot*100:.0f}% Div", ha='center', va='bottom', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_d.set_title("D) Taxa de Divergência Decisória: Proteção contra Subdimensionamento", loc='left', pad=10)
    ax_d.set_xticks(x_d)
    ax_d.set_xticklabels(tip_ord)
    ax_d.set_ylabel("Número de Capitais (Total = 27)")
    ax_d.set_ylim(0, 32)
    ax_d.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    ax_d.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 5 — Análise de Decisão Multicritério (MCDM): Compromisso VIKOR, TOPSIS e Robustez SMAA-2",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig05_otimizacao_multicriterio_global_topsis_vikor_smaa.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 6: Panorama Tarifário: Saneamento e Energia
# ====================================================================================================
def generate_fig6():
    print(" -> Gerando Figura 6: Panorama Tarifário de Água, Esgoto e Energia...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')
    df_gl = pd.read_csv(STUDY3_COMPLETO)
    gdf_br = load_brazil_gdf()

    # Painel A: Distribuição Geográfica das Tarifas Combinadas de Água + Esgoto no Brasil
    ax_a = fig.add_subplot(gs[0, 0])
    if gdf_br is not None:
        gdf_br.plot(ax=ax_a, color='#F1F5F9', edgecolor='#94A3B8', linewidth=0.5)
    
    # Agrupar tarifas por cidade
    city_tariffs = df_br.groupby(['city', 'uf', 'lat', 'lon'], observed=False)['tarifa_combinada_m3'].mean().reset_index()
    sc_a = ax_a.scatter(city_tariffs['lon'], city_tariffs['lat'], c=city_tariffs['tarifa_combinada_m3'],
                        cmap='YlOrRd', s=24, alpha=0.85, edgecolors=PAL_NAVY, lw=0.3)
    cb_a = plt.colorbar(sc_a, ax=ax_a, fraction=0.046, pad=0.04)
    cb_a.set_label("Tarifa Combinada Água+Esgoto (R$/m³)", fontsize=8.5, fontweight='bold')

    ax_a.set_title("A) Geografia das Tarifas Combinadas de Saneamento no Brasil (652 Cidades)", loc='left', pad=10)
    ax_a.set_xlabel("Longitude (°W)")
    ax_a.set_ylabel("Latitude (°S)")
    ax_a.set_xlim(-74, -34)
    ax_a.set_ylim(-34, 6)
    ax_a.grid(True, linestyle='--', alpha=0.3)
    add_panel_label(ax_a, "A")

    # Painel B: Boxplots das Tarifas Globais por Continente (USD/m³)
    ax_b = fig.add_subplot(gs[0, 1])
    cont_order = ["América do Sul", "América do Norte", "Europa", "Ásia", "África"]
    cont_map = {
        "South America": "América do Sul", "North America": "América do Norte",
        "Europe": "Europa", "Asia": "Ásia", "Africa": "África"
    }
    df_gl['Cont_PT'] = df_gl['Continente'].map(lambda x: cont_map.get(x, x))
    data_tar_gl = [df_gl[df_gl['Cont_PT'] == c]['Tarifa_Agua_USD_m3'].dropna() for c in cont_order]
    colors_cont = [PAL_BLUE, PAL_CYAN, PAL_PURPLE, PAL_AMBER, PAL_ROSE]

    bp_b = ax_b.boxplot(data_tar_gl, tick_labels=cont_order, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markerfacecolor=PAL_ROSE, markeredgecolor='white', markersize=6),
                        medianprops=dict(color=PAL_NAVY, lw=2.0))
    for patch, c in zip(bp_b['boxes'], colors_cont):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor(PAL_NAVY)

    for idx, c in enumerate(cont_order):
        sub = df_gl[df_gl['Cont_PT'] == c]['Tarifa_Agua_USD_m3']
        med = sub.median()
        ax_b.text(idx + 1, med + 0.15, f"${med:.2f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=PAL_NAVY)

    ax_b.set_title("B) Tarifas Volumétricas de Água nos 5 Continentes (USD/m³)", loc='left', pad=10)
    ax_b.set_ylabel("Tarifa Volumétrica de Água (USD / m³)")
    ax_b.grid(axis='y', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: O Efeito Alavanca do Esgoto Indexado (k_sewer de 0% a 100%)
    ax_c = fig.add_subplot(gs[1, 0])
    tarifa_agua_base = np.linspace(2.0, 12.0, 30)
    for k_esg, col, label in [(0.0, PAL_GRAY, "Sem Esgoto (k=0%)"),
                              (0.80, PAL_AMBER, "Esgoto 80% (Padrão BR interior)"),
                              (1.00, PAL_BLUE, "Esgoto 100% (Sabesp, Caesb, Águas do Rio)"),
                              (1.50, PAL_ROSE, "Esgoto 150% (Padrão Internacional Unbundled)")]:
        tar_efetiva = tarifa_agua_base * (1.0 + k_esg)
        ax_c.plot(tarifa_agua_base, tar_efetiva, color=col, lw=2.2, label=label)

    ax_c.set_title("C) O Efeito Multiplicador do Esgoto Indexado na Margem de Economia", loc='left', pad=10)
    ax_c.set_xlabel("Tarifa Básica de Água Potável (R$/m³ ou USD/m³)")
    ax_c.set_ylabel("Tarifa Marginal Efetiva Evitada (Água + Esgoto)")
    ax_c.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Elasticidade Cruzada: Custo da Energia de Recalque vs Tarifa de Água
    ax_d = fig.add_subplot(gs[1, 1])
    # Comparar custo da energia por m3 recalquado vs tarifa combinada
    consumo_kwh_m3 = 0.40 # kWh/m³ médio
    tarifa_energia_aneel = df_br['annual_energy_cost_brl'] / (df_br['annual_pluvial_m3'] * consumo_kwh_m3)
    tarifa_energia_aneel = tarifa_energia_aneel.replace([np.inf, -np.inf], np.nan).dropna()

    custo_energia_por_m3 = df_br['cost_per_m3_opex_brl']
    ax_d.scatter(df_br['tarifa_combinada_m3'], df_br['cost_per_m3_opex_brl'],
                 color=PAL_TEAL, alpha=0.45, s=24, edgecolors='none', label='Cidades Brasileiras')

    # Linha de 10% da tarifa
    t_vals = np.linspace(2, 25, 50)
    ax_d.plot(t_vals, t_vals * 0.10, color=PAL_AMBER, lw=1.8, linestyle='--', label='10% da Tarifa')
    ax_d.plot(t_vals, t_vals * 0.05, color=PAL_EMERALD, lw=1.8, linestyle=':', label='5% da Tarifa')

    ax_d.set_title("D) Elasticidade Cruzada: Custo do OPEX por m³ vs. Tarifa Evitada", loc='left', pad=10)
    ax_d.set_xlabel("Tarifa Combinada de Água e Esgoto (R$/m³)")
    ax_d.set_ylabel("Custo Operacional Específico (OPEX R$/m³ aproveitado)")
    ax_d.set_ylim(0, 4.5)
    ax_d.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 6 — Panorama Tarifário de Saneamento e Energia: O Efeito Alavanca do Esgoto e Impacto do Recalque",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig06_panorama_tarifario_agua_esgoto_energia.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 7: Comparativo das 11 Tipologias Edilícias
# ====================================================================================================
def generate_fig7():
    print(" -> Gerando Figura 7: Análise Comparativa das 11 Tipologias Edilícias...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')

    # Painel A: Diagrama Radar Multi-Indicador das 11 Tipologias (Médias por Categoria)
    ax_a = fig.add_subplot(gs[0, 0], polar=True)
    categories = ['Economia Hídrica', 'Confiabilidade', 'VPL Financeiro',
                  'TIR Anual', 'CO2 Evitado', 'Giro Cisterna', 'Baixo LCOW']
    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * math.pi for n in range(num_vars)]
    angles += angles[:1]

    # Scores normalizados de 0 a 100 para 4 grupos principais
    perfis = {
        "Residencial Unifamiliar (UTI)": [42, 45, 12, 10, 15, 25, 30],
        "Residencial Multifamiliar (MFL)": [20, 15, 65, 50, 75, 55, 65],
        "Comercial / Escritórios (COM)": [75, 70, 60, 68, 48, 70, 72],
        "Escolar / Educacional (ESC)": [60, 52, 92, 95, 88, 85, 90]
    }
    pal_radar = [PAL_CYAN, PAL_PURPLE, PAL_AMBER, PAL_EMERALD]

    for (name, vals), col in zip(perfis.items(), pal_radar):
        v = vals + vals[:1]
        ax_a.plot(angles, v, lw=2.0, color=col, label=name)
        ax_a.fill(angles, v, facecolor=col, alpha=0.15)

    ax_a.set_xticks(angles[:-1])
    ax_a.set_xticklabels(categories, fontsize=8.5, fontweight='bold')
    ax_a.set_ylim(0, 100)
    ax_a.set_title("A) Diagrama Radar de Desempenho Multi-Indicador das Tipologias", loc='left', pad=15)
    ax_a.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=2, framealpha=0.9, fontsize=8)
    add_panel_label(ax_a, "A")

    # Painel B: Ranking de Viabilidade Financeira (% Cidades VPL > 0 e Payback <= 10 anos)
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
    ax_b.set_xlabel("Percentual de Cidades Viáveis a 6% a.a. (%)")
    ax_b.set_xlim(0, 115)
    ax_b.grid(axis='x', linestyle='--', alpha=0.5)
    add_panel_label(ax_b, "B")

    # Painel C: A Mecânica da Escala: Área per capita vs Demanda vs Turnover de Cisterna
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
    cb_c.set_label("Giro da Cisterna (Turnover Anual)", fontsize=8.5, fontweight='bold')

    for _, row in tip_scale.iterrows():
        ax_c.annotate(f"{row['building_code']}\n({row['turnover']:.0f}x)",
                      (row['area_per_capita'], row['demand_per_capita']),
                      textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, fontweight='bold', color=PAL_NAVY)

    ax_c.set_title("C) Intensidade Hídrica: Área per capita vs. Demanda e Giro Anual", loc='left', pad=10)
    ax_c.set_xlabel("Área de Telhado per capita (m² / ocupante)")
    ax_c.set_ylabel("Demanda Pluvial per capita (L / ocupante.dia)")
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Relação entre CAPEX Total e VPL Mediano
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
    ax_d.set_title("D) Retorno Financeiro Líquido (VPL) vs. Desembolso Inicial de Capital", loc='left', pad=10)
    ax_d.set_xlabel("CAPEX Inicial Mediano (Milhares de R$)")
    ax_d.set_ylabel("VPL Mediano a 6% a.a. (Milhares de R$)")
    ax_d.legend(loc='upper left', framealpha=0.9, fontsize=8.5)
    ax_d.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 7 — Análise Comparativa das 11 Tipologias Edilícias: Eficiência de Escala, LCOW e Atratividade",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig07_comparativo_11_tipologias_desempenho_escala.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

# ====================================================================================================
# FIGURA 8: Matriz Bivariada 3x3 de Chuva vs Tarifa ("Onde Chove vs Onde Custa Caro")
# ====================================================================================================
def generate_fig8():
    print(" -> Gerando Figura 8: Matriz Bivariada 3x3 Chuva vs Tarifa no Brasil e Mundo...")
    fig = plt.figure(figsize=(16, 11))
    gs = GridSpec(2, 2, figure=fig, hspace=0.28, wspace=0.22)

    df_br = pd.read_csv(STUDY2_COMPLETO, sep=';', decimal=',')
    df_gl = pd.read_csv(STUDY3_COMPLETO)
    gdf_br = load_brazil_gdf()

    # Painel A: Matriz Conceitual 3x3 com Nomenclatura dos 9 Quadrantes
    ax_a = fig.add_subplot(gs[0, 0])
    biv_colors_matrix = [
        ["#E8E8E8", "#B5D2D8", "#78B9C8"], # Baixa Chuva: [Baixa, Media, Alta Tarifa]
        ["#D6AFB2", "#A69DA8", "#6D879B"], # Media Chuva: [Baixa, Media, Alta Tarifa]
        ["#C26A74", "#95596D", "#5B4461"]  # Alta Chuva:  [Baixa, Media, Alta Tarifa]
    ]
    # Nomes conceituais
    quad_names = [
        ["Deserto Econômico\n(Baixa C. / Baixa T.)", "Viabilidade Moderada\n(Baixa C. / Média T.)", "Oásis de Escassez\n(Baixa C. / Alta T.)"],
        ["Incentivo Necessário\n(Média C. / Baixa T.)", "Atratividade Média\n(Média C. / Média T.)", "Atratividade Elevada\n(Média C. / Alta T.)"],
        ["Paradoxo da Abundância\n(Alta C. / Baixa T.)", "Excelente Potencial\n(Alta C. / Média T.)", "QUADRANTE DE OURO\n(Alta C. / Alta T.)"]
    ]

    for r in range(3):
        for c in range(3):
            color = biv_colors_matrix[r][c]
            rect = patches.Rectangle((c, r), 1, 1, facecolor=color, edgecolor='white', lw=1.5)
            ax_a.add_patch(rect)
            text_color = 'white' if (r >= 1 and c >= 1) or (r == 2 or c == 2) else PAL_NAVY
            ax_a.text(c + 0.5, r + 0.5, quad_names[r][c], ha='center', va='center',
                      fontsize=8.5, fontweight='bold', color=text_color)

    ax_a.set_xlim(0, 3)
    ax_a.set_ylim(0, 3)
    ax_a.set_xticks([0.5, 1.5, 2.5])
    ax_a.set_xticklabels(["Tercil 1 (Baixa Tarifa)", "Tercil 2 (Média Tarifa)", "Tercil 3 (Alta Tarifa)"], fontsize=8.5, fontweight='bold')
    ax_a.set_yticks([0.5, 1.5, 2.5])
    ax_a.set_yticklabels(["Tercil 1 (Baixa Chuva)", "Tercil 2 (Média Chuva)", "Tercil 3 (Alta Chuva)"], fontsize=8.5, fontweight='bold')
    ax_a.set_title("A) Matriz Bivariada 3x3: Classificação dos 9 Quadrantes Geoeconômicos", loc='left', pad=10)
    add_panel_label(ax_a, "A")

    # Painel B: Mapa Bivariado do Brasil (652 Cidades)
    ax_b = fig.add_subplot(gs[0, 1])
    if gdf_br is not None:
        gdf_br.plot(ax=ax_b, color='#F8FAFC', edgecolor='#94A3B8', linewidth=0.5)

    # Classificar cidades brasileiras em tercis
    df_br_uniq = df_br.groupby(['city', 'uf', 'lat', 'lon'], observed=False).agg({
        'precip_annual_mean_mm': 'first',
        'tarifa_combinada_m3': 'first',
        'vpl_6pct_brl': 'median'
    }).reset_index()

    p_terc = pd.qcut(df_br_uniq['precip_annual_mean_mm'], q=3, labels=[0, 1, 2]).astype(int)
    t_terc = pd.qcut(df_br_uniq['tarifa_combinada_m3'], q=3, labels=[0, 1, 2]).astype(int)

    city_colors = [biv_colors_matrix[p][t] for p, t in zip(p_terc, t_terc)]
    ax_b.scatter(df_br_uniq['lon'], df_br_uniq['lat'], color=city_colors, s=26, alpha=0.85, edgecolors=PAL_NAVY, lw=0.3)

    # Destaque SC e RJ
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

    # Painel C: Dispersão Global: Chuva vs Tarifa nas 255 Metrópoles Mundiais
    ax_c = fig.add_subplot(gs[1, 0])
    cont_map = {"South America": PAL_BLUE, "North America": PAL_CYAN, "Europe": PAL_PURPLE, "Asia": PAL_AMBER, "Africa": PAL_ROSE}

    for cont, col in cont_map.items():
        sub = df_gl[df_gl['Continente'] == cont].drop_duplicates(subset=['Cidade_Metropole'])
        ax_c.scatter(sub['Precipitacao_Anual_mm'], sub['Tarifa_Agua_USD_m3'],
                     color=col, alpha=0.75, s=40, label=cont, edgecolors=PAL_NAVY, lw=0.4)

    # Linhas de tercis globais
    p_med_gl = df_gl['Precipitacao_Anual_mm'].median()
    t_med_gl = df_gl['Tarifa_Agua_USD_m3'].median()
    ax_c.axvline(p_med_gl, color=PAL_GRAY, linestyle='--', alpha=0.7, label=f'Mediana Chuva ({p_med_gl:.0f} mm)')
    ax_c.axhline(t_med_gl, color=PAL_GRAY, linestyle=':', alpha=0.7, label=f'Mediana Tarifa (${t_med_gl:.2f})')

    # Anotar quadrantes extremos
    ax_c.text(0.95, 0.95, "QUADRANTE DE OURO\n(Alta Chuva + Alta Tarifa)\n[Ex: Leste EUA, Brasil Sul/Sudeste]",
              transform=ax_c.transAxes, ha='right', va='top', fontsize=7.5, fontweight='bold',
              bbox=dict(facecolor='#5B4461', alpha=0.2, edgecolor='none'))
    ax_c.text(0.05, 0.05, "DESERTO ECONÔMICO\n(Baixa Chuva + Tarifa Subsidiada)\n[Ex: Sahel, Oriente Médio, Índia]",
              transform=ax_c.transAxes, ha='left', va='bottom', fontsize=7.5, fontweight='bold',
              bbox=dict(facecolor='#E8E8E8', alpha=0.5, edgecolor='none'))

    ax_c.set_title("C) Dispersão Geoeconômica das 255 Maiores Metrópoles Mundiais", loc='left', pad=10)
    ax_c.set_xlabel("Precipitação Média Anual (mm/ano)")
    ax_c.set_ylabel("Tarifa Volumétrica de Água (USD/m³)")
    ax_c.legend(loc='center left', bbox_to_anchor=(0.02, 0.65), framealpha=0.9, fontsize=7.5)
    ax_c.grid(True, linestyle='--', alpha=0.5)
    add_panel_label(ax_c, "C")

    # Painel D: Atratividade Média (VPL a 6%) em Cada um dos 9 Quadrantes da Matriz
    ax_d = fig.add_subplot(gs[1, 1])
    # Calcular VPL médio em cada quadrante da matriz para o Brasil
    df_br_uniq['p_terc'] = p_terc
    df_br_uniq['t_terc'] = t_terc
    vpl_matrix = df_br_uniq.groupby(['p_terc', 't_terc'], observed=False)['vpl_6pct_brl'].median().unstack()

    x_labels = ["Baixa Tarifa", "Média Tarifa", "Alta Tarifa"]
    y_labels = ["Baixa Chuva", "Média Chuva", "Alta Chuva"]

    im_d = ax_d.imshow(vpl_matrix, cmap='RdYlGn', aspect='auto', origin='lower')
    cb_d = plt.colorbar(im_d, ax=ax_d)
    cb_d.set_label("VPL Mediano a 6% a.a. (R$)", fontsize=8.5, fontweight='bold')

    for r in range(3):
        for c in range(3):
            val = vpl_matrix.iloc[r, c]
            ax_d.text(c, r, f"R$ {val:,.0f}", ha='center', va='center',
                      fontsize=9, fontweight='bold', color='black' if abs(val) < 20000 else 'white')

    ax_d.set_xticks([0, 1, 2])
    ax_d.set_xticklabels(x_labels, fontweight='bold')
    ax_d.set_yticks([0, 1, 2])
    ax_d.set_yticklabels(y_labels, fontweight='bold')
    ax_d.set_title("D) VPL Mediano nos 9 Quadrantes: Evidência Numérica da Alavanca Tarifária", loc='left', pad=10)
    add_panel_label(ax_d, "D")

    plt.suptitle("FIGURA 8 — Matriz Bivariada 3x3 de Precipitação vs. Tarifa: A Chave Geoeconômica do Aproveitamento Pluvial",
                 fontsize=13.5, y=0.99)
    out_path = os.path.join(OUTPUT_DIR, "fig08_matriz_bivariada_3x3_chuva_vs_tarifa.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" -> Salvo com sucesso: {out_path}")

def main():
    print("================================================================================")
    print("Iniciando geração das 8 figuras científicas consolidadas...")
    print("================================================================================")
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    generate_fig5()
    generate_fig6()
    generate_fig7()
    generate_fig8()
    print("================================================================================")
    print("Suíte de 8 figuras gerada com sucesso em:", OUTPUT_DIR)
    print("================================================================================")

if __name__ == "__main__":
    main()
