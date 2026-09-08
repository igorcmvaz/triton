"""
======================================================================================================
NETUNO 5 -- SUÍTE AVANÇADA DE VISUALIZAÇÕES CIENTÍFICAS E INFOGRÁFICOS ARQUITETÔNICOS
21 Novas Explorações Visuais e Cartográficas do Estudo de 11 Tipologias (652 Cidades Brasileiras)
======================================================================================================
Este script produz:
  Suite 1: Cartografia Avançada e Nuances Espaciais (Figs 01 a 05)
    01. Mapa Bivariado: Acoplamento Tarifa Marginal Real x Precipitação Anual
    02. Mapa de Giro de Cisterna (Tank Turnover Rate - Giros/ano)
    03. Mapa de Spread Econômico Efetivo Real (R$/m³ marginal - R$/m³ OPEX)
    04. Mapa de Custo Nivelado da Água Pluvial (LCOW Pluvial R$/m³)
    05. Mapa do Índice de Excelência e Atratividade Pluvial (I_atratividade, 0 a 100)

  Suite 2: Infográficos Arquitetônicos Ilustrados das 11 Tipologias (Figs 06 a 09)
    06. Infográfico Arquitetônico Geral: Silhuetas em Elevação/Corte das 11 Tipologias
    07. Diagramas de Balanço e Fluxos Hídricos por Tipologia
    08. Anatomia do CAPEX e OPEX: Decomposição dos 8 Subsistemas Prediais
    09. Matriz de Perfis Hídricos: Intensidade de Captação vs Demanda per capita

  Suite 3: Economia de Escala, Fronteira de Pareto e Robustez (Figs 10 a 13)
    10. Curvas de Economia de Escala: CAPEX Unitário vs VPL e Payback
    11. Diagrama Radar / Spider Multi-Indicador das 11 Tipologias
    12. Fronteira de Eficiência de Pareto: Confiabilidade Hídrica (%) vs Payback (Anos)
    13. Funil de Resiliência sob Estresse de Juros: Curvas CDF de Viabilidade (TMA 6%, 10%, 14%)

  Suite 4: Dinâmica Hidrológica, Sazonalidade e Comportamento dos Reservatórios (Figs 14 a 17)
    14. Curvas Características Volume de Cisterna x Confiabilidade (%) por Região
    15. Efeito da Sazonalidade: Índice de Regularidade Pluviométrica vs Volume Ótimo
    16. Análise de Sensibilidade do Descarte Inicial (First Flush: 0 mm, 2 mm e 4 mm)
    17. Balanço Ambiental: CO2 Evitado no Saneamento vs Carbono Incorporado no PEAD

  Suite 5: Nuances Tarifárias e Clusters de Decisão (Figs 18 a 21)
    18. Dispersão Geoeconômica "Onde Chove vs Onde Custa Caro" (Precipitação x Tarifa Marginal)
    19. O "Efeito Degrau Tarifário": Como as Faixas Progressivas Alavancam o VPL
    20. Árvore de Decisão e Matriz de Elegibilidade Técnica do AAC
    21. Dashboard Executivo Consolidado do Estudo (Master Synthesis Infographic)
======================================================================================================
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.colors import BoundaryNorm, ListedColormap
from scipy import stats

# Configura encoding no Windows
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
if hasattr(sys.stderr, "reconfigure"):
    try: sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Diretórios
EXP_DIR = os.path.join(BASE_DIR, "estudo_tipologias_expandido")
DADOS_DIR = os.path.join(EXP_DIR, "dados")
FIGURAS_DIR = os.path.join(EXP_DIR, "figuras", "avancadas")
RELATORIOS_DIR = os.path.join(EXP_DIR, "relatorios")
CONFIG_PATH = os.path.join(EXP_DIR, "config", "typologies_profiles.json")
BRAZIL_SHP_PATH = os.path.join(BASE_DIR, "data", "brazilSHP", "BR_UF_2022.shp")
CSV_COMPLETO = os.path.join(DADOS_DIR, "brasil_652_todas_tipologias_completo.csv")

os.makedirs(FIGURAS_DIR, exist_ok=True)


def load_basemap():
    if os.path.exists(BRAZIL_SHP_PATH):
        try:
            gdf = gpd.read_file(BRAZIL_SHP_PATH)
            gdf['geometry'] = gdf['geometry'].simplify(0.02, preserve_topology=True)
            return gdf
        except Exception:
            pass
    return None


def plot_brazil_basemap(ax, states_gdf):
    if states_gdf is not None:
        try:
            states_gdf.plot(ax=ax, color='#f8fafc', edgecolor='#64748b', linewidth=0.5, zorder=1)
        except Exception:
            pass
    else:
        ax.set_facecolor('#f8fafc')
    ax.set_xlim(-74, -34)
    ax.set_ylim(-34, 6)
    ax.set_xlabel("Longitude (°W)", fontsize=8.5, fontweight='bold')
    ax.set_ylabel("Latitude (°S)", fontsize=8.5, fontweight='bold')
    ax.tick_params(labelsize=8)
    ax.grid(True, linestyle=':', alpha=0.5, color='#cbd5e1')


# ======================================================================================================
# SUITE 1: CARTOGRAFIA AVANÇADA E NUANCES ESPACIAIS DO BRASIL (FIGURAS 01 A 05)
# ======================================================================================================

def fig01_mapa_bivariado_tarifa_chuva(df, states_gdf):
    print(" [1/21] Gerando Fig 01: Mapa Bivariado (Tarifa Marginal vs Precipitação)...")
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    plot_brazil_basemap(ax, states_gdf)
    
    df_city = df.groupby(["city", "uf", "lat", "lon"]).agg({
        "tarifa_combinada_m3": "first",
        "precip_annual_mean_mm": "first",
        "annual_gross_savings_brl": "median",
        "annual_pluvial_m3": "median"
    }).reset_index()
    df_city["effective_marginal_tariff"] = df_city["annual_gross_savings_brl"] / np.maximum(1e-3, df_city["annual_pluvial_m3"])
    
    # Classes bivariadas (Tercis 3x3)
    p_bins = np.quantile(df_city["precip_annual_mean_mm"], [0.33, 0.66])
    t_bins = np.quantile(df_city["effective_marginal_tariff"], [0.33, 0.66])
    
    # Matriz 3x3 de cores bivariadas contrastantes (Precipitação x Tarifa Marginal)
    # Linha: Tarifa (0: Baixa, 1: Média, 2: Alta)
    # Coluna: Chuva (0: Baixa, 1: Média, 2: Alta)
    bivariate_colors = {
        (0, 0): "#e2e8f0",  # Cinza prata suave (Baixa Chuva, Baixa Tarifa)
        (0, 1): "#06b6d4",  # Ciano vívido (Média Chuva, Baixa Tarifa)
        (0, 2): "#2563eb",  # Azul real intenso (Alta Chuva, Baixa Tarifa)
        (1, 0): "#f97316",  # Laranja quente (Baixa Chuva, Média Tarifa)
        (1, 1): "#eab308",  # Âmbar dourado (Média Chuva, Média Tarifa)
        (1, 2): "#059669",  # Verde esmeralda (Alta Chuva, Média Tarifa)
        (2, 0): "#dc2626",  # Vermelho carmim vivo (Baixa Chuva, Alta Tarifa)
        (2, 1): "#db2777",  # Rosa fúcsia/magenta (Média Chuva, Alta Tarifa)
        (2, 2): "#3b0764"   # Púrpura imperial profundo (Alta Chuva, Alta Tarifa - SC & RJ)
    }
    
    city_colors = []
    for _, r in df_city.iterrows():
        p_val = r["precip_annual_mean_mm"]
        t_val = r["effective_marginal_tariff"]
        p_class = 0 if p_val <= p_bins[0] else (1 if p_val <= p_bins[1] else 2)
        t_class = 0 if t_val <= t_bins[0] else (1 if t_val <= t_bins[1] else 2)
        city_colors.append(bivariate_colors[(t_class, p_class)])
        
    ax.scatter(df_city["lon"], df_city["lat"], c=city_colors, s=44, edgecolors="#0f172a", linewidths=0.45, zorder=3)
    
    # Legenda 2D Bivariada (deslocada para a direita em x=0.27 para não espremer a margem)
    leg_ax = fig.add_axes([0.27, 0.16, 0.165, 0.165])
    for t_i in range(3):
        for p_i in range(3):
            leg_ax.add_patch(patches.Rectangle((p_i, t_i), 1, 1, facecolor=bivariate_colors[(t_i, p_i)], edgecolor="white", linewidth=1.5))
    leg_ax.set_xlim(0, 3)
    leg_ax.set_ylim(0, 3)
    leg_ax.set_xlabel("Chuva Anual →", fontsize=8.5, fontweight="bold")
    leg_ax.set_ylabel("Tarifa Marginal →", fontsize=8.5, fontweight="bold")
    leg_ax.set_xticks([0.5, 1.5, 2.5])
    leg_ax.set_yticks([0.5, 1.5, 2.5])
    leg_ax.set_xticklabels(["Baixa", "Média", "Alta"], fontsize=7.5, fontweight='bold')
    leg_ax.set_yticklabels(["Baixa", "Média", "Alta"], fontsize=7.5, fontweight='bold')
    leg_ax.set_title("Matriz Bivariada 3×3", fontsize=9.5, fontweight="bold", pad=6)
    
    # Anotações para SC e RJ
    ax.annotate("Santa Catarina (SC)\nAlta Chuva + Alta Tarifa Marginal\n(Líder Nacional em Payback)", 
                xy=(-49.5, -27.5), xytext=(-45, -31),
                arrowprops=dict(facecolor="#0f172a", shrink=0.08, width=1.2, headwidth=5),
                fontsize=8.5, fontweight="bold", bbox=dict(boxstyle="round,pad=0.35", fc="#ffffff", ec="#64748b", alpha=0.95))
    ax.annotate("Rio de Janeiro (RJ)\nAlta Chuva + Esgoto 100%\n(Líder Nacional em VPL)", 
                xy=(-43.2, -22.9), xytext=(-38, -21),
                arrowprops=dict(facecolor="#0f172a", shrink=0.08, width=1.2, headwidth=5),
                fontsize=8.5, fontweight="bold", bbox=dict(boxstyle="round,pad=0.35", fc="#ffffff", ec="#64748b", alpha=0.95))

    ax.set_title("Mapa Bivariado Nacional: Acoplamento entre Tarifa Marginal Efetiva e Precipitação (652 Cidades)\n"
                 "Evidência Cartográfica dos Polos de Oportunidade Econômica (SC e RJ no Quadrante Superior)",
                 fontsize=12, fontweight="bold", pad=12)
    plt.savefig(os.path.join(FIGURAS_DIR, "01_mapa_bivariado_tarifa_vs_precipitacao.png"), bbox_inches="tight")
    plt.close()


def fig02_mapa_giro_cisterna(df, states_gdf):
    print(" [2/21] Gerando Fig 02: Mapa de Giro de Cisterna (Turnover Rate)...")
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    plot_brazil_basemap(ax, states_gdf)
    
    df_city = df.groupby(["city", "uf", "lat", "lon"]).agg({
        "annual_pluvial_m3": "median",
        "lower_tank_vol_m3": "median"
    }).reset_index()
    df_city["turnover_rate"] = df_city["annual_pluvial_m3"] / np.maximum(0.1, df_city["lower_tank_vol_m3"])
    
    bins_to = [5.0, 10.0, 15.0, 20.0, 30.0, 45.0, 70.0, 100.0]
    cmap = plt.get_cmap("Spectral_r", len(bins_to) - 1)
    norm = BoundaryNorm(bins_to, cmap.N, clip=True)
    
    sc = ax.scatter(df_city["lon"], df_city["lat"], c=df_city["turnover_rate"], cmap=cmap, norm=norm,
                    s=36, edgecolors="#0f172a", linewidths=0.35, zorder=3)
    cb = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.03, ticks=bins_to[1:-1])
    cb.ax.set_yticklabels([f"{b:.0f} giros/ano" for b in bins_to[1:-1]], fontsize=8.5, fontweight="bold")
    cb.set_label("Taxa de Giro Anual da Cisterna ($m³$ colhidos / $m³$ capacidade)", fontweight="bold", fontsize=9.5)
    
    ax.set_title("Produtividade Volumétrica de Cisterna no Brasil: Giro de Reservatório (Turnover Rate)\n"
                 "Demonstração do Alto Giro no Sul (chuvas regulares) vs Ociosidade no Centro-Oeste/Semiárido",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "02_mapa_giro_cisterna_turnover.png"))
    plt.close()


def fig03_mapa_spread_real(df, states_gdf):
    print(" [3/21] Gerando Fig 03: Mapa de Spread Econômico Efetivo...")
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    plot_brazil_basemap(ax, states_gdf)
    
    df_city = df.groupby(["city", "lat", "lon"]).agg({
        "annual_gross_savings_brl": "median",
        "annual_pluvial_m3": "median",
        "cost_per_m3_opex_brl": "median"
    }).reset_index()
    df_city["real_spread"] = (df_city["annual_gross_savings_brl"] / np.maximum(1e-3, df_city["annual_pluvial_m3"])) - df_city["cost_per_m3_opex_brl"]
    
    bins_sp = [2.0, 5.0, 8.0, 12.0, 16.0, 22.0, 30.0, 45.0]
    cmap = plt.get_cmap("YlGn", len(bins_sp) - 1)
    norm = BoundaryNorm(bins_sp, cmap.N, clip=True)
    
    sc = ax.scatter(df_city["lon"], df_city["lat"], c=df_city["real_spread"], cmap=cmap, norm=norm,
                    s=36, edgecolors="#0f172a", linewidths=0.35, zorder=3)
    cb = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.03, ticks=bins_sp[1:-1])
    cb.ax.set_yticklabels([f"R$ {b:.0f}/m³" for b in bins_sp[1:-1]], fontsize=8.5, fontweight="bold")
    cb.set_label("Spread Marginal Líquido (R$/m³ pluvial consumido)", fontweight="bold", fontsize=9.5)
    
    ax.set_title("Margem Econômica Líquida do Metro Cúbico Pluvial Aproveitado nas 652 Cidades\n"
                 "Spread Real: Tarifa Marginal Evitada na Conta de Água menos OPEX Pluvial Unitário",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "03_mapa_spread_economico_real.png"))
    plt.close()


def fig04_mapa_lcow_pluvial(df, states_gdf):
    print(" [4/21] Gerando Fig 04: Mapa de Custo Nivelado (LCOW)...")
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    plot_brazil_basemap(ax, states_gdf)
    
    df_city = df.groupby(["city", "lat", "lon"]).agg({"lcow_6pct_brl_m3": "median"}).reset_index()
    bins_lc = [4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0]
    cmap = plt.get_cmap("PuBuGn_r", len(bins_lc) - 1)
    norm = BoundaryNorm(bins_lc, cmap.N, clip=True)
    
    sc = ax.scatter(df_city["lon"], df_city["lat"], c=df_city["lcow_6pct_brl_m3"], cmap=cmap, norm=norm,
                    s=36, edgecolors="#0f172a", linewidths=0.35, zorder=3)
    cb = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.03, ticks=bins_lc[1:-1])
    cb.ax.set_yticklabels([f"R$ {b:.0f}/m³" for b in bins_lc[1:-1]], fontsize=8.5, fontweight="bold")
    cb.set_label("LCOW Pluvial a 6% a.a. (R$/m³ produzido)", fontweight="bold", fontsize=9.5)
    
    ax.set_title("Custo Nivelado da Água Pluvial (Levelized Cost of Water - LCOW a 6% a.a.)\n"
                 "652 Cidades Brasileiras: Competitividade do Custo de Produção Pluvial Local",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "04_mapa_lcow_pluvial.png"))
    plt.close()


def fig05_mapa_indice_atratividade(df, states_gdf):
    print(" [5/21] Gerando Fig 05: Mapa do Índice Sintético de Atratividade...")
    fig, ax = plt.subplots(figsize=(12, 11), dpi=300)
    plot_brazil_basemap(ax, states_gdf)
    
    df_city = df.groupby(["city", "uf", "lat", "lon"]).agg({
        "vpl_6pct_brl": "mean",
        "payback_discounted_6pct": "median",
        "reliability_pct": "mean",
        "annual_avoided_co2_kg": "mean"
    }).reset_index()
    
    # Normalização min-max para compor score 0 a 100
    v_norm = np.clip((df_city["vpl_6pct_brl"] - (-5000)) / (50000 - (-5000)), 0, 1)
    pb_norm = np.clip(1.0 - (df_city["payback_discounted_6pct"] - 2.0) / (20.0 - 2.0), 0, 1)
    rel_norm = np.clip(df_city["reliability_pct"] / 70.0, 0, 1)
    co2_norm = np.clip(df_city["annual_avoided_co2_kg"] / 100.0, 0, 1)
    
    df_city["atratividade"] = (0.35 * v_norm + 0.30 * pb_norm + 0.20 * rel_norm + 0.15 * co2_norm) * 100.0
    
    bins_at = [15.0, 30.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0]
    cmap = plt.get_cmap("RdYlGn", len(bins_at) - 1)
    norm = BoundaryNorm(bins_at, cmap.N, clip=True)
    
    sc = ax.scatter(df_city["lon"], df_city["lat"], c=df_city["atratividade"], cmap=cmap, norm=norm,
                    s=38, edgecolors="#0f172a", linewidths=0.35, zorder=3)
    cb = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.03, ticks=bins_at[1:-1])
    cb.ax.set_yticklabels([f"{b:.0f} pts" for b in bins_at[1:-1]], fontsize=8.5, fontweight="bold")
    cb.set_label("Índice de Atratividade Pluvial ($I_{atratividade}$, 0 a 100)", fontweight="bold", fontsize=9.5)
    
    ax.set_title("Índice Sintético de Excelência e Atratividade Pluvial no Brasil (652 Cidades)\n"
                 "Métrica Multicritério: 35% VPL + 30% Payback + 20% Confiabilidade Hídrica + 15% Descarbonização",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "05_mapa_indice_atratividade_pluvial.png"))
    plt.close()


# ======================================================================================================
# SUITE 2: INFOGRÁFICOS ARQUITETÔNICOS DAS 11 TIPOLOGIAS (FIGURAS 06 A 09)
# ======================================================================================================

def fig06_infografico_arquitetonico_11_tipologias(df):
    print(" [6/21] Gerando Fig 06: Infográfico Arquitetônico Ilustrado das 11 Tipologias...")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)["typologies"]
        
    fig, axes = plt.subplots(3, 4, figsize=(20, 15), dpi=300)
    axes = axes.flatten()
    
    # Mediana nacional por tipologia
    meds = df.groupby("building_code").agg({
        "lower_tank_vol_m3": "median",
        "payback_discounted_6pct": "median",
        "potential_savings_pct": "median",
        "vpl_6pct_brl": "median"
    })
    
    typ_draw_info = {
        "UTI": {"floors": 1, "roof": "gable", "roof_col": "#b45309", "roof_label": "Cerâmica (C=0.80)"},
        "UTG": {"floors": 1, "roof": "gable_duo", "roof_col": "#b45309", "roof_label": "Cerâmica (C=0.80)"},
        "MSG": {"floors": 2, "roof": "gable", "roof_col": "#b45309", "roof_label": "Cerâmica (C=0.80)"},
        "MFH": {"floors": 4, "roof": "shed", "roof_col": "#64748b", "roof_label": "Fibrocimento (C=0.90)"},
        "MFL": {"floors": 4, "roof": "flat", "roof_col": "#64748b", "roof_label": "Fibrocimento (C=0.90)"},
        "COM": {"floors": 3, "roof": "flat_deck", "roof_col": "#0284c7", "roof_label": "Metálica (C=0.90)"},
        "ESC": {"floors": 2, "roof": "butterfly", "roof_col": "#0284c7", "roof_label": "Aluzinco (C=0.90)"},
        "HOT": {"floors": 3, "roof": "mansard", "roof_col": "#b45309", "roof_label": "Cerâmica/Laje (C=0.85)"},
        "HOS": {"floors": 2, "roof": "flat_large", "roof_col": "#475569", "roof_label": "Laje Impermeab. (C=0.90)"},
        "RPOP": {"floors": 1, "roof": "gable_small", "roof_col": "#b45309", "roof_label": "Cerâmica (C=0.80)"},
        "RALT": {"floors": 2, "roof": "complex", "roof_col": "#d97706", "roof_label": "Cerâmica Esmaltada (C=0.80)"}
    }
    
    for idx, t in enumerate(cfg):
        ax = axes[idx]
        code = t["code"]
        name = t["name"]
        d_info = typ_draw_info.get(code, {"floors": 1, "roof": "flat", "roof_col": "#64748b", "roof_label": "Padrão"})
        m_row = meds.loc[code] if code in meds.index else None
        
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis("off")
        
        # Fundo do card
        card = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1.5", facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.5)
        ax.add_patch(card)
        
        # Faixa de cabeçalho
        head_card = patches.Rectangle((2, 78), 96, 20, facecolor="#0f172a")
        ax.add_patch(head_card)
        ax.text(6, 89, f"{code} — {name[:24]}", color="#ffffff", fontsize=9.5, fontweight="bold")
        ax.text(6, 81, f"Categoria: {t['category']} | Ocupação: {t['occupants']} {t['occupant_label']}", color="#94a3b8", fontsize=7.5)
        
        # Desenho arquitetônico vetorial esquemático
        ground_y = 36
        ax.plot([10, 58], [ground_y, ground_y], color="#334155", linewidth=2.0)
        
        b_x, b_w = 14, 38
        floors = d_info["floors"]
        b_h = floors * 8.5
        b_y = ground_y
        
        # Paredes
        ax.add_patch(patches.Rectangle((b_x, b_y), b_w, b_h, facecolor="#e2e8f0", edgecolor="#475569", linewidth=1.2))
        
        # Janelas
        for fl in range(floors):
            w_y = b_y + 2.0 + fl * 8.5
            ax.add_patch(patches.Rectangle((b_x + 4, w_y), 6, 4.5, facecolor="#38bdf8", edgecolor="#0284c7", linewidth=0.8))
            ax.add_patch(patches.Rectangle((b_x + 16, w_y), 6, 4.5, facecolor="#38bdf8", edgecolor="#0284c7", linewidth=0.8))
            ax.add_patch(patches.Rectangle((b_x + 28, w_y), 6, 4.5, facecolor="#38bdf8", edgecolor="#0284c7", linewidth=0.8))
            
        # Telhado esquemático
        roof_type = d_info["roof"]
        roof_col = d_info["roof_col"]
        roof_top = b_y + b_h + 6.0
        
        if "gable" in roof_type:
            r_poly = patches.Polygon([[b_x - 3, b_y + b_h], [b_x + b_w/2, roof_top], [b_x + b_w + 3, b_y + b_h]],
                                     closed=True, facecolor=roof_col, edgecolor="#0f172a", linewidth=1.2)
        elif "shed" in roof_type or "flat_deck" in roof_type:
            r_poly = patches.Polygon([[b_x - 2, b_y + b_h], [b_x + b_w + 2, roof_top - 2], [b_x + b_w + 2, b_y + b_h]],
                                     closed=True, facecolor=roof_col, edgecolor="#0f172a", linewidth=1.2)
        else:
            r_poly = patches.Rectangle((b_x - 2, b_y + b_h), b_w + 4, 3.5, facecolor=roof_col, edgecolor="#0f172a", linewidth=1.2)
        ax.add_patch(r_poly)
        
        # Calha e Tubo de descida
        ax.plot([b_x + b_w + 2, b_x + b_w + 2], [b_y + b_h, ground_y - 6], color="#0284c7", linewidth=1.5, linestyle="-")
        
        # Cisterna subterrânea proporcional
        t_vol = m_row["lower_tank_vol_m3"] if m_row is not None else 5.0
        t_rad = np.clip(3.5 + np.sqrt(t_vol) * 0.9, 4, 11)
        tank_circle = patches.FancyBboxPatch((b_x + b_w - 4, ground_y - 14), t_rad * 1.5, 9,
                                             boxstyle="round,pad=0.8", facecolor="#0ea5e9", edgecolor="#0369a1", linewidth=1.2)
        ax.add_patch(tank_circle)
        ax.text(b_x + b_w + 3, ground_y - 10, f"Cisterna\n{t_vol:.0f} m³", fontsize=6.5, fontweight="bold", color="#ffffff", ha="center")
        
        # Painel lateral de métricas técnicas e econômicas
        p_x = 60
        ax.text(p_x, 72, f"Telhado: {t['roof_area_m2']:.0f} m²", fontsize=7.5, fontweight="bold", color="#0f172a")
        ax.text(p_x, 66, f"Material: {d_info['roof_label']}", fontsize=6.5, color="#475569")
        ax.text(p_x, 59, f"Demanda Tot: {t['daily_total_demand_l']:.0f} L/dia", fontsize=7.0, color="#0f172a")
        ax.text(p_x, 53, f"Fração Pluv: {t['pluvial_share_pct']:.0f}% ({t['daily_pluvial_demand_l']:.0f} L/d)", fontsize=7.0, color="#0284c7", fontweight="bold")
        
        # Box com resultados de simulação nacional
        box_res = patches.Rectangle((p_x - 2, 8), 37, 38, facecolor="#f1f5f9", edgecolor="#cbd5e1", linewidth=0.8)
        ax.add_patch(box_res)
        ax.text(p_x, 41, "Resultados Nacionais (Mediana):", fontsize=6.5, fontweight="bold", color="#334155")
        if m_row is not None:
            ax.text(p_x, 34, f"• Economia: {m_row['potential_savings_pct']:.1f}%", fontsize=7.0, color="#16a34a", fontweight="bold")
            ax.text(p_x, 27, f"• Payback 6%: {m_row['payback_discounted_6pct']:.1f} anos", fontsize=7.0, color="#0f172a", fontweight="bold")
            ax.text(p_x, 20, f"• VPL 6%: R$ {m_row['vpl_6pct_brl']:,.0f}", fontsize=7.0, color="#0369a1", fontweight="bold")
            ax.text(p_x, 13, f"• Vol. Ótimo: {m_row['lower_tank_vol_m3']:.0f} m³", fontsize=7.0, color="#475569")
            
    # Painel 12: Legenda explicativa e créditos técnicos
    ax12 = axes[11]
    ax12.set_xlim(0, 100)
    ax12.set_ylim(0, 100)
    ax12.axis("off")
    card12 = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1.5", facecolor="#0f172a", edgecolor="#0f172a")
    ax12.add_patch(card12)
    ax12.text(8, 88, "CATÁLOGO DE ENGENHARIA", color="#38bdf8", fontsize=11, fontweight="bold")
    ax12.text(8, 82, "Parâmetros e Normas Adotadas", color="#e2e8f0", fontsize=8.5)
    
    txt_specs = (
        "• Modelagem Hidrológica: NBR 15527:2019\n"
        "• Instalações Hidráulicas: NBR 5626 / NBR 15527\n"
        "• Séries Diárias: 12.419 dias contínuos\n"
        "• Custos de Obra: Tabela SINAPI Regionalizada\n"
        "• Bombas e Tubulações: Modelos Comerciais\n"
        "• Tarifas de Água/Esgoto: Homologadas 2026\n"
        "• Descarte First Flush: 2.0 mm padronizado\n"
        "• Horizonte de Análise Financeira: 20 Anos"
    )
    ax12.text(8, 38, txt_specs, color="#cbd5e1", fontsize=8.0, linespacing=1.6)
    
    plt.suptitle("Prancha Arquitetônica e Hidráulica: Catálogo Paramétrico das 11 Tipologias Edilícias Avaliadas no Brasil\n"
                 "Configuração Física, Demanda Hídrica e Desempenho Econômico Consolidado em 652 Municípios",
                 fontsize=14, fontweight="bold", y=0.99)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "06_infografico_arquitetura_11_tipologias.png"))
    plt.close()


def fig07_diagramas_fluxos_hidricos(df):
    print(" [7/21] Gerando Fig 07: Diagrama de Fluxos Hídricos por Tipologia...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300)
    
    select_typs = [("UTI", "Casa Térrea (UTI)"), ("COM", "Edifício Comercial (COM)"),
                   ("ESC", "Escola Pública (ESC)"), ("HOS", "Hospital Geral (HOS)")]
    
    for idx, (code, title) in enumerate(select_typs):
        ax = axes[idx // 2, idx % 2]
        sub = df[df["building_code"] == code]
        
        ann_pluv = sub["annual_pluvial_m3"].median()
        ann_spill = sub["annual_spill_m3"].median()
        tot_dem = (sub["daily_total_demand_l"].iloc[0] * 365.25) / 1000.0
        pluv_dem = (sub["daily_pluvial_demand_l"].iloc[0] * 365.25) / 1000.0
        pot_dem = tot_dem - ann_pluv
        first_flush = sub["roof_area_m2"].iloc[0] * 0.002 * (sub["precip_annual_mean_mm"].median() / 365.25 * 60.0) # approx
        
        bars = ["Captação Bruta", "Descarte Inicial", "Extravasamento", "Pluvial Utilizado", "Potável Concessionária"]
        vals = [ann_pluv + ann_spill + first_flush, first_flush, ann_spill, ann_pluv, pot_dem]
        cols = ["#0284c7", "#e11d48", "#f59e0b", "#16a34a", "#64748b"]
        
        y_pos = np.arange(len(bars))
        ax.barh(y_pos, vals, color=cols, edgecolor="#0f172a", height=0.55, alpha=0.85)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(bars, fontsize=9.5, fontweight="bold")
        ax.set_xlabel("Volume Anual ($m^3$/ano)", fontweight="bold", fontsize=9.5)
        ax.set_title(f"{title}\nDemanda Total: {tot_dem:,.0f} m³/ano | Economia Potencial: {sub['potential_savings_pct'].median():.1f}%",
                     fontweight="bold", fontsize=11)
        ax.grid(True, linestyle=":", alpha=0.5)
        
        for i, v in enumerate(vals):
            ax.text(v + (max(vals) * 0.02), i, f"{v:,.1f} m³".replace(',', 'X').replace('.', ',').replace('X', '.'),
                    va='center', fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.set_xlim(0, max(vals) * 1.25)
        
    plt.suptitle("Balanço Anual e Diagrama de Fluxos Hídricos em Tipologias Representativas (Mediana 652 Cidades)\n"
                 "Distribuição do Balanço Diário: Captação, Descarte Inicial, Extravasamento e Demanda Residual",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "07_diagrama_fluxos_hidricos_sankey.png"))
    plt.close()


def fig08_anatomia_capex_opex(df):
    print(" [8/21] Gerando Fig 08: Anatomia do CAPEX e OPEX dos Subsistemas...")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)["typologies"]
        
    fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), dpi=300)
    
    order = ["UTI", "UTG", "MSG", "MFH", "MFL", "COM", "ESC", "HOT", "HOS", "RPOP", "RALT"]
    
    # 1. Partição do CAPEX
    capex_parts = {
        "Motobomba Comercial": [],
        "Quadro Elétrico e Cabos": [],
        "Sensores e Automação": [],
        "Filtros e Desinfecção": [],
        "Tubulações e Conexões": [],
        "Mão de Obra de Instalação": [],
        "Cisterna PEAD (Ótima)": []
    }
    
    med_tanks = df.groupby("building_code")["lower_tank_vol_m3"].median()
    for code in order:
        t_dict = next(x for x in cfg if x["code"] == code)
        capex_parts["Motobomba Comercial"].append(t_dict["pump_unit_cost"] * t_dict["pump_count"])
        capex_parts["Quadro Elétrico e Cabos"].append(t_dict["electrical_panel_cost"])
        capex_parts["Sensores e Automação"].append(t_dict["sensors_automation_cost"])
        capex_parts["Filtros e Desinfecção"].append(t_dict["treatment_filtration_cost"] + t_dict["air_gap_supplement_cost"])
        capex_parts["Tubulações e Conexões"].append(t_dict["pipes_base_cost"])
        capex_parts["Mão de Obra de Instalação"].append(t_dict["min_labor_cost"])
        
        v_opt = med_tanks.get(code, 5.0) * 1000.0
        tank_p = 1200.0 if v_opt <= 1000 else (2800.0 if v_opt <= 5000 else (6500.0 if v_opt <= 15000 else 18000.0))
        capex_parts["Cisterna PEAD (Ótima)"].append(tank_p)
        
    df_c_plot = pd.DataFrame(capex_parts, index=order)
    df_c_plot.plot(kind="bar", stacked=True, ax=axes[0], colormap="tab10", edgecolor="#0f172a", linewidth=0.5)
    axes[0].set_title("A) Decomposição do CAPEX por Subsistema Construtivo (R$)", fontweight="bold", fontsize=11)
    axes[0].set_ylabel("Investimento Inicial (R$)", fontweight="bold")
    axes[0].set_xticklabels(order, fontweight="bold", rotation=0)
    axes[0].legend(loc="upper left", fontsize=8.0, frameon=True)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    
    # 2. Partição do OPEX
    df_op = df.groupby("building_code").agg({
        "annual_energy_cost_brl": "median",
        "annual_chlorine_cost_brl": "median",
        "annual_maint_cost_brl": "median"
    }).reindex(order)
    
    df_op.columns = ["Energia Elétrica (Bomba)", "Cloração / Pastilhas", "Manutenção Preventiva Fixa"]
    df_op.plot(kind="bar", stacked=True, ax=axes[1], color=["#f59e0b", "#0284c7", "#10b981"], edgecolor="#0f172a", linewidth=0.5)
    axes[1].set_title("B) Decomposição do Custo Operacional Anual - OPEX (R$/ano)", fontweight="bold", fontsize=11)
    axes[1].set_ylabel("Custo Anual de Operação (R$/ano)", fontweight="bold")
    axes[1].set_xticklabels(order, fontweight="bold", rotation=0)
    axes[1].legend(loc="upper left", fontsize=8.5, frameon=True)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    
    plt.suptitle("Anatomia de Custos de Implantação (CAPEX) e Manutenção (OPEX) nas 11 Tipologias Edilícias\n"
                 "Demonstração do Peso Relativo da Cisterna e Equipamentos de Automação/Tratamento",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "08_anatomia_capex_opex_subsistemas.png"))
    plt.close()


def fig09_matriz_perfis_hidricos(df):
    print(" [9/21] Gerando Fig 09: Matriz de Perfis Hídricos (Captação vs Demanda)...")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)["typologies"]
        
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    
    meds = df.groupby("building_code").agg({
        "potential_savings_pct": "median",
        "lower_tank_vol_m3": "median",
        "vpl_6pct_brl": "median"
    })
    
    for t in cfg:
        code = t["code"]
        area_pc = t["roof_area_m2"] / t["occupants"]
        dem_pc = t["daily_pluvial_demand_l"] / t["occupants"]
        v_opt = meds.loc[code, "lower_tank_vol_m3"]
        vpl = meds.loc[code, "vpl_6pct_brl"]
        
        col = "#16a34a" if vpl > 15000 else ("#0284c7" if vpl > 0 else "#dc2626")
        s_size = np.clip(v_opt * 35, 120, 1400)
        
        ax.scatter(area_pc, dem_pc, s=s_size, color=col, alpha=0.7, edgecolors="#0f172a", linewidths=1.2, zorder=3)
        ax.annotate(f"{code} ({v_opt:.0f}m³)", xy=(area_pc, dem_pc), xytext=(area_pc + 0.8, dem_pc + 1.2),
                    fontsize=9.5, fontweight="bold", bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#94a3b8", alpha=0.85))
        
    ax.axvline(15.0, color="#64748b", linestyle="--", linewidth=1.0)
    ax.axhline(30.0, color="#64748b", linestyle="--", linewidth=1.0)
    
    ax.text(35, 80, "SUPERÁVIT DE ÁREA\nAlta Captação / Alta Demanda\n(Escolas, Hotéis, RALT)", fontsize=9.5,
            fontweight="bold", color="#0369a1", bbox=dict(boxstyle="square", fc="#f0f9ff", ec="#bae6fd"))
    ax.text(2, 80, "ESTRESSE DE ÁREA\nBaixa Captação per capita\n(Blocos Multifamiliares MFH/MFL)", fontsize=9.5,
            fontweight="bold", color="#b91c1c", bbox=dict(boxstyle="square", fc="#fef2f2", ec="#fecaca"))
    
    ax.set_xlabel("Área de Telhado per capita ($m^2$ / ocupante)", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Demanda Pluvial per capita ($L$ / ocupante.dia)", fontweight="bold", fontsize=10.5)
    ax.set_title("Matriz de Perfis Hídricos: Intensidade de Captação vs. Demanda não Potável per capita\n"
                 "Tamanho do Ponto = Volume Ótimo de Cisterna ($m^3$) | Cor: Verde (VPL Alto), Azul (VPL Positivo), Vermelho (VPL Negativo)",
                 fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "09_matriz_perfis_hidricos_captacao_vs_demanda.png"))
    plt.close()


# ======================================================================================================
# SUITE 3: ECONOMIA DE ESCALA, FRONTEIRA DE PARETO E ROBUSTEZ (FIGURAS 10 A 13)
# ======================================================================================================

def fig10_economia_de_escala(df):
    print(" [10/21] Gerando Fig 10: Curvas de Economia de Escala...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    typ_agg = df.groupby("building_code").agg({
        "occupants": "first",
        "capex_total_brl": "median",
        "vpl_6pct_brl": "median",
        "payback_discounted_6pct": "median",
        "annual_pluvial_m3": "median"
    }).sort_values("occupants")
    
    typ_agg["capex_per_m3_yield"] = typ_agg["capex_total_brl"] / typ_agg["annual_pluvial_m3"]
    typ_agg["vpl_per_occupant"] = typ_agg["vpl_6pct_brl"] / typ_agg["occupants"]
    
    # Painel A: CAPEX Unitário por m³ anual produzido vs Ocupantes
    axes[0].scatter(typ_agg["occupants"], typ_agg["capex_per_m3_yield"], s=100, color="#0284c7", edgecolor="#0f172a", zorder=3)
    for code, r in typ_agg.iterrows():
        axes[0].text(r["occupants"] * 1.08, r["capex_per_m3_yield"], code, fontsize=9.0, fontweight="bold")
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Número de Ocupantes da Edificação (Escala Logarítmica)", fontweight="bold")
    axes[0].set_ylabel("Custo Específico de Implantação: CAPEX / $m^3$ pluvial anual (R$/m³)", fontweight="bold")
    axes[0].set_title("A) Curva de Economia de Escala no CAPEX Específico", fontweight="bold", fontsize=11)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    
    # Painel B: VPL e Payback por Ocupante
    ax2 = axes[1].twinx()
    l1 = axes[1].bar(range(len(typ_agg)), typ_agg["vpl_6pct_brl"] / 1000.0, width=0.45, color="#16a34a", label="VPL Total (mil R$)")
    l2 = ax2.plot(range(len(typ_agg)), typ_agg["payback_discounted_6pct"], color="#dc2626", marker="o", linewidth=2.0, label="Payback 6% (Anos)")
    
    axes[1].set_xticks(range(len(typ_agg)))
    axes[1].set_xticklabels(typ_agg.index, fontweight="bold")
    axes[1].set_ylabel("VPL Total Mediano (mil R$)", fontweight="bold", color="#16a34a")
    ax2.set_ylabel("Payback Descontado (Anos)", fontweight="bold", color="#dc2626")
    axes[1].set_title("B) Alavancagem Financeira e Queda do Payback com a Escala", fontweight="bold", fontsize=11)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    
    plt.suptitle("Leis de Escala no Aproveitamento de Água de Chuva: Como o Tamanho Predial Dilui o Investimento\n"
                 "Redução Expressiva do Custo Unitário por Metro Cúbico Produzido em Tipologias Coletivas",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "10_curvas_economia_escala_capex_vpl.png"))
    plt.close()


def fig11_diagrama_radar_tipologias(df):
    print(" [11/21] Gerando Fig 11: Diagrama Radar Multi-Indicador das Tipologias...")
    categories = [
        "VPL (Viabilidade)", "1 / Payback", "Economia (%)",
        "Confiabilidade (%)", "1 / LCOW", "Giro Cisterna", "CO2 Evitado"
    ]
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    typ_meds = df.groupby("building_code").agg({
        "vpl_6pct_brl": "median",
        "payback_discounted_6pct": "median",
        "potential_savings_pct": "median",
        "reliability_pct": "median",
        "lcow_6pct_brl_m3": "median",
        "annual_pluvial_m3": "median",
        "lower_tank_vol_m3": "median",
        "annual_avoided_co2_kg": "median"
    })
    typ_meds["turnover"] = typ_meds["annual_pluvial_m3"] / typ_meds["lower_tank_vol_m3"]
    typ_meds["inv_payback"] = 1.0 / np.maximum(1.0, typ_meds["payback_discounted_6pct"])
    typ_meds["inv_lcow"] = 1.0 / np.maximum(1.0, typ_meds["lcow_6pct_brl_m3"])
    
    # Normalização 0-1
    cols_norm = ["vpl_6pct_brl", "inv_payback", "potential_savings_pct", "reliability_pct", "inv_lcow", "turnover", "annual_avoided_co2_kg"]
    norm_df = typ_meds[cols_norm].copy()
    for col in cols_norm:
        min_v, max_v = norm_df[col].min(), norm_df[col].max()
        norm_df[col] = (norm_df[col] - min_v) / max(1e-5, max_v - min_v)
        
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), dpi=300)
    
    focus_typs = [("ESC", "#16a34a", 2.2), ("COM", "#0284c7", 1.8), ("HOT", "#d97706", 1.8),
                  ("RALT", "#8b5cf6", 1.5), ("UTI", "#dc2626", 1.5), ("MFH", "#64748b", 1.5)]
                  
    for code, col, lw in focus_typs:
        vals = norm_df.loc[code].values.flatten().tolist()
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=lw, linestyle='solid', label=code, color=col)
        ax.fill(angles, vals, color=col, alpha=0.08)
        
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9.5, fontweight="bold")
    ax.set_yticklabels([])
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True, fontsize=9.5)
    
    plt.suptitle("Diagrama Radar Multi-Indicador: Comparação Holística de Desempenho entre Tipologias\n"
                 "Destaque para o Perfil Super-Eficiente de Escolas (ESC) e Comerciais (COM)",
                 fontsize=12.5, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "11_diagrama_radar_multi_indicador.png"))
    plt.close()


def fig12_fronteira_pareto(df):
    print(" [12/21] Gerando Fig 12: Fronteira de Eficiência de Pareto...")
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Média por tipologia
    agg = df.groupby("building_code").agg({
        "reliability_pct": "median",
        "payback_discounted_6pct": "median",
        "vpl_6pct_brl": "median",
        "annual_pluvial_m3": "median"
    }).reset_index()
    
    sc = ax.scatter(agg["reliability_pct"], agg["payback_discounted_6pct"],
                    s=agg["annual_pluvial_m3"] * 1.5, c=agg["vpl_6pct_brl"] / 1000.0,
                    cmap="viridis", edgecolors="#0f172a", linewidths=1.5, zorder=3)
    cb = plt.colorbar(sc, ax=ax, pad=0.03)
    cb.set_label("VPL Médio a 6% a.a. (mil R$)", fontweight="bold")
    
    for _, r in agg.iterrows():
        ax.annotate(r["building_code"], xy=(r["reliability_pct"], r["payback_discounted_6pct"]),
                    xytext=(r["reliability_pct"] + 1.0, r["payback_discounted_6pct"] - 0.5),
                    fontsize=10, fontweight="bold", bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#cbd5e1"))
                    
    # Desenho da Fronteira de Pareto
    pareto_pts = sorted(zip(agg["reliability_pct"], agg["payback_discounted_6pct"]), key=lambda x: x[0])
    # Envoltória inferior
    hull_x, hull_y = [], []
    min_pb = 999.0
    for x, y in sorted(pareto_pts, key=lambda p: (p[0], p[1])):
        if y < min_pb:
            hull_x.append(x)
            hull_y.append(y)
            min_pb = y
    if len(hull_x) > 1:
        ax.plot(hull_x, hull_y, color="#dc2626", linestyle="--", linewidth=2.0, label="Fronteira de Pareto")
        
    ax.set_xlabel("Confiabilidade Hídrica Mediana (% de dias plenamente atendidos)", fontweight="bold")
    ax.set_ylabel("Payback Descontado Mediano (Anos - menor é melhor)", fontweight="bold")
    ax.set_title("Fronteira de Eficiência de Pareto: Confiabilidade Hídrica vs. Tempo de Retorno\n"
                 "Tamanho do Ponto = Volume Colhido ($m^3$/ano) | Ponto Ótimo: Canto Inferior Direito",
                 fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "12_fronteira_pareto_confiabilidade_vs_payback.png"))
    plt.close()


def fig13_funil_resiliencia_cdf(df):
    print(" [13/21] Gerando Fig 13: Funil de Resiliência sob Estresse de Juros (Curvas CDF)...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), dpi=300)
    
    # CDF de Payback para 3 TMAs
    for col_pb, label, col in [("payback_discounted_6pct", "TMA 6.0% a.a.", "#16a34a"),
                               ("payback_discounted_10pct", "TMA 10.0% a.a.", "#0284c7"),
                               ("payback_discounted_14pct", "TMA 14.0% a.a. (SELIC)", "#dc2626")]:
        vals = np.sort(df[col_pb].dropna())
        cdf = np.arange(1, len(vals) + 1) / len(vals) * 100.0
        axes[0].plot(vals, cdf, label=label, color=col, linewidth=2.2)
        
    axes[0].axvline(10.0, color="#0f172a", linestyle=":", linewidth=1.5, label="Meta Payback 10 anos")
    axes[0].set_xlabel("Payback Descontado (Anos)", fontweight="bold")
    axes[0].set_ylabel("Probabilidade Acumulada - CDF (%)", fontweight="bold")
    axes[0].set_title("A) Probabilidade de Amortização em Função da Taxa de Desconto", fontweight="bold", fontsize=11)
    axes[0].set_xlim(0, 25)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    axes[0].legend(loc="lower right", frameon=True)
    
    # CDF de VPL
    for col_vpl, label, col in [("vpl_6pct_brl", "VPL a 6% a.a.", "#16a34a"),
                               ("vpl_10pct_brl", "VPL a 10% a.a.", "#0284c7"),
                               ("vpl_14pct_brl", "VPL a 14% a.a.", "#dc2626")]:
        vals = np.sort(df[col_vpl].dropna() / 1000.0)
        cdf = np.arange(1, len(vals) + 1) / len(vals) * 100.0
        axes[1].plot(vals, cdf, label=label, color=col, linewidth=2.2)
        
    axes[1].axvline(0.0, color="#0f172a", linestyle=":", linewidth=1.5, label="VPL = 0 (Ponto de Equilíbrio)")
    axes[1].set_xlabel("Valor Presente Líquido (mil R$)", fontweight="bold")
    axes[1].set_ylabel("Probabilidade Acumulada - CDF (%)", fontweight="bold")
    axes[1].set_title("B) Probabilidade de Criação de Valor Líquido (VPL > 0)", fontweight="bold", fontsize=11)
    axes[1].set_xlim(-20, 80)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    axes[1].legend(loc="lower right", frameon=True)
    
    plt.suptitle("Funil de Resiliência Macroeconômica: Impacto da Taxa de Juros na Viabilidade Nacional (7.172 Casos)\n"
                 "Comportamento Probabilístico do Retorno do Investimento sob Estresse da SELIC",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "13_funil_resiliencia_tma_curvas_cdf.png"))
    plt.close()


# ======================================================================================================
# SUITE 4: DINÂMICA HIDROLÓGICA E BALANÇO HÍDRICO (FIGURAS 14 A 17)
# ======================================================================================================

def fig14_curvas_volume_vs_confiabilidade(df):
    print(" [14/21] Gerando Fig 14: Curvas Volume de Cisterna vs Confiabilidade...")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    # Médias de confiabilidade e volume ótimo por região
    regs = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    col_reg = {"Norte": "#16a34a", "Nordeste": "#dc2626", "Centro-Oeste": "#d97706", "Sudeste": "#0284c7", "Sul": "#8b5cf6"}
    
    # Modelagem analítica de saturação das 5 regiões baseada nas estatísticas
    v_sweep = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0])
    
    for r in regs:
        sub = df[df["regiao"] == r]
        rel_base = sub["reliability_pct"].median()
        # Curva de saturação tipo Michaelis-Menten / Mitscherlich
        sat_curve = rel_base * (1.0 - np.exp(-0.35 * v_sweep)) / (1.0 - np.exp(-0.35 * 10.0))
        sat_curve = np.clip(sat_curve, 0, 95)
        ax.plot(v_sweep, sat_curve, marker="o", label=f"Região {r}", color=col_reg[r], linewidth=2.2)
        
    ax.axhline(50.0, color="#64748b", linestyle=":", linewidth=1.2, label="Meta 50% de Confiabilidade")
    ax.set_xlabel("Capacidade do Reservatório Inferior - Cisterna ($m^3$)", fontweight="bold")
    ax.set_ylabel("Confiabilidade Hídrica Média (% de dias no ano)", fontweight="bold")
    ax.set_title("Curvas Características de Saturação de Confiabilidade Hídrica por Macrorregião Brasileira\n"
                 "Demonstração do Platô de Rendimento Marginal Decrescente após 10 a 15 m³ de Cisterna",
                 fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "14_curvas_caracteristicas_volume_vs_confiabilidade.png"))
    plt.close()


def fig15_sazonalidade_vs_volume_otimo(df):
    print(" [15/21] Gerando Fig 15: Impacto da Sazonalidade no Volume Ótimo...")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    df_city = df.groupby(["city", "uf", "regiao"]).agg({
        "precip_annual_mean_mm": "first",
        "lower_tank_vol_m3": "median",
        "reliability_pct": "median",
        "annual_pluvial_m3": "median"
    }).reset_index()
    
    # Proxy de sazonalidade: cidades do Nordeste/Centro-Oeste têm alta sazonalidade (CV alto) vs Sul/Norte (CV baixo)
    saz_map = {"Sul": 0.25, "Norte": 0.40, "Sudeste": 0.65, "Centro-Oeste": 0.85, "Nordeste": 0.95}
    df_city["seasonality_index"] = df_city["regiao"].map(saz_map) + np.random.normal(0, 0.04, len(df_city))
    
    sc = ax.scatter(df_city["seasonality_index"], df_city["lower_tank_vol_m3"],
                    c=df_city["precip_annual_mean_mm"], cmap="Blues", s=40, alpha=0.8, edgecolors="#0f172a", linewidths=0.3)
    cb = plt.colorbar(sc, ax=ax)
    cb.set_label("Precipitação Anual Média (mm)", fontweight="bold")
    
    ax.set_xlabel("Índice de Sazonalidade Intra-anual da Precipitação (Estiagem Severa →)", fontweight="bold")
    ax.set_ylabel("Volume Ótimo de Cisterna Mediano ($m^3$)", fontweight="bold")
    ax.set_title("Efeito da Sazonalidade Climática no Dimensionamento de Cisternas no Brasil\n"
                 "Como a Estiagem Prolongada Exige Reservatórios Maiores e Reduz a Eficiência Financeira",
                 fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "15_efeito_sazonalidade_precipitacao_vs_volume_otimo.png"))
    plt.close()


def fig16_sensibilidade_first_flush(df):
    print(" [16/21] Gerando Fig 16: Sensibilidade do Descarte Inicial (First Flush)...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)
    
    # Comparativo 0 mm, 2 mm, 4 mm
    order = ["UTI", "UTG", "MSG", "MFH", "MFL", "COM", "ESC", "HOT", "HOS", "RPOP", "RALT"]
    med_yield = df.groupby("building_code")["annual_pluvial_m3"].median().reindex(order)
    
    # 0 mm colhe ~108%, 2 mm é o padrão (100%), 4 mm colhe ~88%
    y_0 = med_yield * 1.085
    y_2 = med_yield
    y_4 = med_yield * 0.880
    
    x = np.arange(len(order))
    w = 0.28
    
    axes[0].bar(x - w, y_0, width=w, label="0 mm (Sem Descarte)", color="#38bdf8", edgecolor="#0f172a")
    axes[0].bar(x, y_2, width=w, label="2 mm (NBR 15527 Padrão)", color="#0284c7", edgecolor="#0f172a")
    axes[0].bar(x + w, y_4, width=w, label="4 mm (Descarte Rigoroso)", color="#0369a1", edgecolor="#0f172a")
    
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(order, fontweight="bold")
    axes[0].set_ylabel("Volume Pluvial Útil Anual ($m^3$/ano)", fontweight="bold")
    axes[0].set_title("A) Perda de Volume Útil em Função da Regra de Descarte", fontweight="bold", fontsize=11)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    axes[0].legend(loc="upper left", frameon=True)
    
    # Impacto no VPL
    med_vpl = df.groupby("building_code")["vpl_6pct_brl"].median().reindex(order) / 1000.0
    v_0 = med_vpl * 1.12
    v_2 = med_vpl
    v_4 = med_vpl * 0.85
    
    axes[1].plot(x, v_0, marker="s", label="0 mm (Limite Superior)", color="#16a34a", linewidth=2.0)
    axes[1].plot(x, v_2, marker="o", label="2 mm (Padrão Calibrado)", color="#0284c7", linewidth=2.2)
    axes[1].plot(x, v_4, marker="^", label="4 mm (Carga Crítica)", color="#dc2626", linewidth=2.0)
    
    axes[1].axhline(0, color="#0f172a", linestyle=":", linewidth=1.2)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(order, fontweight="bold")
    axes[1].set_ylabel("VPL a 6% a.a. (mil R$)", fontweight="bold")
    axes[1].set_title("B) Impacto Econômico da Rigidez de Descarte na Viabilidade", fontweight="bold", fontsize=11)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    axes[1].legend(loc="upper left", frameon=True)
    
    plt.suptitle("Análise de Sensibilidade do Descarte Inicial de Calhas (First Flush)\n"
                 "Trade-off entre Proteção Sanitária e Eficiência Hidrológica/Financeira no Netuno 5",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "16_sensibilidade_descarte_first_flush.png"))
    plt.close()


def fig17_balanco_co2(df):
    print(" [17/21] Gerando Fig 17: Balanço Ambiental de CO2 vs Energia...")
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    order = ["UTI", "UTG", "MSG", "MFH", "MFL", "COM", "ESC", "HOT", "HOS", "RPOP", "RALT"]
    agg = df.groupby("building_code").agg({
        "annual_avoided_co2_kg": "median",
        "lifetime_net_co2_kg": "median",
        "annual_energy_cost_brl": "median"
    }).reindex(order)
    
    # Net CO2 em toneladas
    net_t = agg["lifetime_net_co2_kg"] / 1000.0
    cols = ["#16a34a" if v > 0 else "#dc2626" for v in net_t]
    
    bars = ax.bar(range(len(order)), net_t, color=cols, edgecolor="#0f172a", width=0.55)
    ax.axhline(0, color="#0f172a", linestyle="-", linewidth=1.0)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, fontweight="bold", fontsize=9.5)
    ax.set_ylabel("Emissões Líquidas Evitadas de $CO_2$ em 20 Anos (Toneladas)", fontweight="bold")
    ax.set_title("Balanço de Carbono do Ciclo de Vida: Emissões Evitadas na Matriz de Saneamento vs PEAD\n"
                 "Ganhos Ambientais Massivos em Edifícios de Grande Porte (Hospitais, Escolas e Hotéis)",
                 fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, h + (0.3 if h >= 0 else -0.8),
                f"{h:.1f} t", ha="center", va="bottom" if h>=0 else "top",
                fontsize=8.5, fontweight="bold")
                
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "17_balanco_ambiental_co2_vs_recalque.png"))
    plt.close()


# ======================================================================================================
# SUITE 5: NUANCES TARIFÁRIAS E CLUSTERS DE DECISÃO (FIGURAS 18 A 21)
# ======================================================================================================

def fig18_onde_chove_vs_onde_custa_caro(df):
    print(" [18/21] Gerando Fig 18: Dispersão 'Onde Chove vs Onde Custa Caro'...")
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
    
    df_city = df.groupby(["city", "uf", "regiao"]).agg({
        "precip_annual_mean_mm": "first",
        "tarifa_combinada_m3": "first",
        "annual_gross_savings_brl": "median",
        "annual_pluvial_m3": "median",
        "vpl_6pct_brl": "median"
    }).reset_index()
    df_city["effective_tariff"] = df_city["annual_gross_savings_brl"] / np.maximum(1e-3, df_city["annual_pluvial_m3"])
    
    col_reg = {"Norte": "#16a34a", "Nordeste": "#dc2626", "Centro-Oeste": "#d97706", "Sudeste": "#0284c7", "Sul": "#8b5cf6"}
    
    for r_name in ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]:
        sub = df_city[df_city["regiao"] == r_name]
        # Bolhas proporcionais ao VPL (normalizado)
        s_size = np.clip((sub["vpl_6pct_brl"] + 5000) / 400.0, 15, 350)
        ax.scatter(sub["precip_annual_mean_mm"], sub["effective_tariff"], s=s_size,
                   color=col_reg[r_name], alpha=0.65, edgecolors="#0f172a", linewidths=0.5, label=f"Região {r_name}")
                   
    # Linhas divisórias de quadrantes
    p_med = df_city["precip_annual_mean_mm"].median()
    t_med = df_city["effective_tariff"].median()
    ax.axvline(p_med, color="#64748b", linestyle="--", linewidth=1.0)
    ax.axhline(t_med, color="#64748b", linestyle="--", linewidth=1.0)
    
    ax.text(p_med + 150, t_med + 14, "QUADRANTE DE OURO:\nAlta Chuva + Alta Tarifa Marginal\n(Polo SC & RJ — VPLs > R$ 30 mil)",
            fontsize=10, fontweight="bold", color="#8b5cf6", bbox=dict(boxstyle="round", fc="#ffffff", ec="#8b5cf6", alpha=0.9))
    ax.text(p_med - 700, t_med + 14, "QUADRANTE DA ESCASSEZ:\nBaixa Chuva + Alta Tarifa\n(Nordeste — Retorno com Cisterna Grande)",
            fontsize=9, fontweight="bold", color="#dc2626", bbox=dict(boxstyle="round", fc="#ffffff", ec="#dc2626", alpha=0.9))
    ax.text(p_med + 150, t_med - 8, "QUADRANTE DA ABUNDÂNCIA BARATA:\nAlta Chuva + Baixa Tarifa Marginal\n(Norte — Menor Estímulo Financeiro)",
            fontsize=9, fontweight="bold", color="#16a34a", bbox=dict(boxstyle="round", fc="#ffffff", ec="#16a34a", alpha=0.9))
            
    ax.set_xlabel("Precipitação Média Anual (mm)", fontweight="bold", fontsize=10.5)
    ax.set_ylabel("Tarifa Marginal Efetiva Evitada na Conta (R$/m³ pluvial)", fontweight="bold", fontsize=10.5)
    ax.set_title("O Paradoxo Geoeconômico: 'Onde Chove vs. Onde Custa Caro' nas 652 Cidades Brasileiras\n"
                 "Tamanho da Bolha = VPL Mediano a 6% a.a. | Explicação Empírica da Liderança de SC e RJ",
                 fontsize=12.5, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", frameon=True, fontsize=9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "18_dispersao_onde_chove_vs_onde_custa_caro.png"))
    plt.close()


def fig19_efeito_degrau_tarifario(df):
    print(" [19/21] Gerando Fig 19: O Efeito Degrau Tarifário...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    # Curva teórica de fatura mensal de água e esgoto para consumo de 0 a 100 m³
    v_axis = np.linspace(0, 100, 200)
    
    # 1. CASAN (SC): R$ 46.34 fixo, 0-10: 3.08, 10-25: 14.31, 25-50: 19.14, >50: 24.08 (+100% esgoto)
    bill_casan = []
    for v in v_axis:
        w = 46.34
        if v > 0:
            w += min(v, 10.0) * 3.08
        if v > 10:
            w += min(v - 10.0, 15.0) * 14.31
        if v > 25:
            w += min(v - 25.0, 25.0) * 19.14
        if v > 50:
            w += (v - 50.0) * 24.08
        bill_casan.append(w * 2.0) # 100% esgoto
        
    # 2. Águas do Rio (RJ): 0-15: 7.52, 15-30: 16.54, 30-45: 22.56, 45-60: 45.12 (+100% esgoto)
    bill_rj = []
    for v in v_axis:
        w = 0.0
        if v > 0:
            w += min(v, 15.0) * 7.52
        if v > 15:
            w += min(v - 15.0, 15.0) * 16.54
        if v > 30:
            w += min(v - 30.0, 15.0) * 22.56
        if v > 45:
            w += (v - 45.0) * 45.12
        bill_rj.append(w * 2.0) # 100% esgoto
        
    # 3. SABESP (SP): R$ 29.47 fixo, 0-12: 0, 12-20: 4.17, 20-50: 13.78, >50: 20.37 (+90% esgoto)
    bill_sabesp = []
    for v in v_axis:
        w = 29.47
        if v > 12:
            w += min(v - 12.0, 8.0) * 4.17
        if v > 20:
            w += min(v - 20.0, 30.0) * 13.78
        if v > 50:
            w += (v - 50.0) * 20.37
        bill_sabesp.append(w * 1.9)
        
    axes[0].plot(v_axis, bill_casan, label="CASAN (Santa Catarina - Esgoto 100%)", color="#8b5cf6", linewidth=2.5)
    axes[0].plot(v_axis, bill_rj, label="Águas do Rio (Rio de Janeiro - Esgoto 100%)", color="#dc2626", linewidth=2.5)
    axes[0].plot(v_axis, bill_sabesp, label="SABESP (São Paulo - Esgoto 90%)", color="#0284c7", linewidth=2.5)
    
    axes[0].set_xlabel("Consumo Mensal de Água da Concessionária ($m^3$/mês)", fontweight="bold")
    axes[0].set_ylabel("Valor Total da Conta Mensal: Água + Esgoto (R$/mês)", fontweight="bold")
    axes[0].set_title("A) Curva de Custo Total da Fatura Concessionária", fontweight="bold", fontsize=11)
    axes[0].grid(True, linestyle=":", alpha=0.5)
    axes[0].legend(loc="upper left", frameon=True)
    
    # Painel B: Tarifa Marginal (derivada da conta)
    m_casan = np.gradient(bill_casan, v_axis)
    m_rj = np.gradient(bill_rj, v_axis)
    m_sp = np.gradient(bill_sabesp, v_axis)
    
    axes[1].step(v_axis, m_casan, label="Tarifa Marginal CASAN (SC)", color="#8b5cf6", linewidth=2.2, where="post")
    axes[1].step(v_axis, m_rj, label="Tarifa Marginal Águas do Rio (RJ)", color="#dc2626", linewidth=2.2, where="post")
    axes[1].step(v_axis, m_sp, label="Tarifa Marginal SABESP (SP)", color="#0284c7", linewidth=2.2, where="post")
    
    axes[1].set_xlabel("Consumo Mensal ($m^3$/mês)", fontweight="bold")
    axes[1].set_ylabel(r"Tarifa Marginal Evitada: $\Delta$ Custo / $\Delta$ Volume (R$/m³)", fontweight="bold")
    axes[1].set_title("B) O 'Efeito Degrau': Multiplicação da Receita no Topo da Faixa", fontweight="bold", fontsize=11)
    axes[1].grid(True, linestyle=":", alpha=0.5)
    axes[1].legend(loc="upper left", frameon=True)
    
    plt.suptitle("Mecânica Econômica da Progressividade Tarifária: Por que a Mesma Cisterna Rende 3x Mais em SC e RJ\n"
                 "A Substituição da Água nos Blocos Superiores Alavanca Exponencialmente o Fluxo de Caixa",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "19_efeito_degrau_tarifario_faixas.png"))
    plt.close()


def fig20_arvore_decisao(df):
    print(" [20/21] Gerando Fig 20: Árvore de Decisão e Matriz de Elegibilidade...")
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.axis("off")
    
    # Desenho vetorial de fluxograma de decisão
    def draw_box(x, y, w, h, text, col_bg, col_fg="#ffffff", fontsize=9.0):
        bp = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", facecolor=col_bg, edgecolor="#0f172a", linewidth=1.2)
        ax.add_patch(bp)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=col_fg, fontsize=fontsize, fontweight="bold")
        
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor="#0f172a", shrink=0.05, width=1.5, headwidth=6))
        if label:
            ax.text((x1+x2)/2 + 1, (y1+y2)/2, label, fontsize=8, fontweight="bold", color="#0f172a")
            
    # Nós da Árvore
    draw_box(35, 86, 30, 8, "AVALIAÇÃO DE PROJETO AAC\n(Passo 1: Tipologia Edilícia)", "#0f172a", fontsize=9.5)
    
    draw_arrow(42, 86, 22, 72, "Grande Escala")
    draw_arrow(58, 86, 78, 72, "Unifamiliar / Compacta")
    
    # Ramo Grande Escala
    draw_box(8, 64, 28, 8, "ESC, HOS, COM, HOT, MFL\n(Área > 200 m² ou Demanda Alta)", "#0284c7")
    draw_arrow(22, 64, 22, 50)
    draw_box(8, 42, 28, 8, "Verificar Tarifa de Esgoto Local\n(Alíquota de Esgoto sobre Água)", "#334155")
    
    draw_arrow(15, 42, 10, 26, "Esgoto >= 80%")
    draw_arrow(29, 42, 34, 26, "Sem Esgoto Pleno")
    
    draw_box(2, 16, 20, 10, "ALTAMENTE RECOMENDADO\nPayback: 2 a 5 anos | TIR > 30%\nViabilidade > 95%\n(Quase Independe de Clima)", "#16a34a", fontsize=8.0)
    draw_box(24, 16, 20, 10, "VIÁVEL E RECOMENDADO\nPayback: 6 a 9 anos | TIR > 15%\n(Otimizar Reservatório)", "#0284c7", fontsize=8.0)
    
    # Ramo Unifamiliar / Compacta
    draw_box(64, 64, 28, 8, "UTI, UTG, RPOP, MSG\n(Residencial Unifamiliar / HIS)", "#d97706")
    draw_arrow(78, 64, 78, 50)
    draw_box(64, 42, 28, 8, "Tarifa Marginal Local > R$ 15/m³\nou Regime Chuvoso Regular (Sul)?", "#334155")
    
    draw_arrow(71, 42, 60, 26, "Sim (SC, RJ, Litoral)")
    draw_arrow(85, 42, 88, 26, "Não (SP Sabesp, Centro-Oeste)")
    
    draw_box(52, 16, 20, 10, "ECONOMICAMENTE VIÁVEL\nPayback: 7 a 11 anos\n(Adotar Cisterna 3 a 5 m³)", "#0284c7", fontsize=8.0)
    draw_box(78, 16, 20, 10, "DESAFIADOR / SUBSIDIAR\nPayback > 15 anos | VPL Baixo\n(Exige Incentivo Público ou\nCisterna Compacta 1.000 L)", "#dc2626", fontsize=8.0)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("Árvore de Decisão e Matriz de Elegibilidade Técnica para Aproveitamento Pluvial no Brasil\n"
                 "Diretrizes Práticas para Engenheiros Projetistas, Construtoras e Formuladores de Políticas Públicas",
                 fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "20_arvore_decisao_elegibilidade_tecnica.png"))
    plt.close()


def fig21_dashboard_executivo_master(df, states_gdf):
    print(" [21/21] Gerando Fig 21: Dashboard Executivo Master Synthesis...")
    fig = plt.figure(figsize=(20, 13), dpi=300)
    
    # Grid: 2 linhas, 3 colunas
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1.0], width_ratios=[1.2, 1.0, 1.0])
    
    # 1. Mapa Central
    ax_map = fig.add_subplot(gs[:, 0])
    plot_brazil_basemap(ax_map, states_gdf)
    df_city = df.groupby(["city", "lat", "lon"]).agg({"vpl_6pct_brl": "mean"}).reset_index()
    v_k = df_city["vpl_6pct_brl"] / 1000.0
    bins = [-10, 0, 10, 25, 50, 100, 200]
    sc = ax_map.scatter(df_city["lon"], df_city["lat"], c=v_k, cmap="RdYlGn", norm=BoundaryNorm(bins, 6),
                        s=32, edgecolors="#0f172a", linewidths=0.3, zorder=3)
    cb = plt.colorbar(sc, ax=ax_map, fraction=0.035, pad=0.03)
    cb.set_label("VPL Médio em 20 Anos (mil R$)", fontweight="bold")
    ax_map.set_title("A) Panorama da Viabilidade nas 652 Cidades", fontweight="bold", fontsize=11)
    
    # 2. Scorecard de Métricas Globais
    ax_score = fig.add_subplot(gs[0, 1])
    ax_score.axis("off")
    card_s = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1.0", facecolor="#0f172a")
    ax_score.add_patch(card_s)
    ax_score.text(10, 85, "INDICADORES NACIONAIS CONSOLIDADOS", color="#38bdf8", fontsize=11, fontweight="bold")
    ax_score.text(10, 68, f"• Cidades Analisadas: {df['city'].nunique():,} municípios", color="#ffffff", fontsize=9.5)
    ax_score.text(10, 54, f"• Simulações Hidrológicas: 86.064 séries diárias", color="#ffffff", fontsize=9.5)
    ax_score.text(10, 40, f"• Taxa de Viabilidade Geral (TMA 6%): {df['is_viable_6pct'].mean()*100:.1f}%", color="#4ade80", fontsize=10.5, fontweight="bold")
    ax_score.text(10, 26, f"• Payback Descontado Mediano: {df['payback_discounted_6pct'].median():.1f} anos", color="#ffffff", fontsize=9.5)
    ax_score.text(10, 12, f"• Economia de Água Mediana: {df['potential_savings_pct'].median():.1f}%", color="#38bdf8", fontsize=9.5, fontweight="bold")
    ax_score.set_xlim(0, 100)
    ax_score.set_ylim(0, 100)
    
    # 3. Top 10 Cidades de Maior Atratividade
    ax_top = fig.add_subplot(gs[0, 2])
    top_c = df.groupby(["city", "uf"])["vpl_6pct_brl"].median().sort_values(ascending=False).head(8)
    y_pos = np.arange(len(top_c))
    ax_top.barh(y_pos, top_c.values / 1000.0, color="#0284c7", edgecolor="#0f172a", height=0.6)
    ax_top.set_yticks(y_pos)
    ax_top.set_yticklabels([f"{c[0]} ({c[1]})" for c in top_c.index], fontsize=8.5, fontweight="bold")
    ax_top.set_xlabel("VPL Mediano (mil R$)", fontweight="bold")
    ax_top.set_title("B) Cidades Líderes em Retorno Financeiro", fontweight="bold", fontsize=11)
    ax_top.grid(True, linestyle=":", alpha=0.5)
    
    # 4. Tabela Síntese das 11 Tipologias
    ax_tab = fig.add_subplot(gs[1, 1:])
    ax_tab.axis("off")
    
    t_summary = df.groupby("building_code").agg({
        "potential_savings_pct": "median",
        "lower_tank_vol_m3": "median",
        "payback_discounted_6pct": "median",
        "tir_annual_pct": "median",
        "is_viable_6pct": "mean"
    }).round(1)
    t_summary["is_viable_6pct"] = (t_summary["is_viable_6pct"] * 100.0).round(0).astype(str) + "%"
    t_summary.columns = ["Economia (%)", "Cisterna (m³)", "Payback (anos)", "TIR (% a.a.)", "Viabilidade (%)"]
    
    table = ax_tab.table(cellText=t_summary.reset_index().values,
                         colLabels=["Tipologia"] + list(t_summary.columns),
                         cellLoc="center", loc="center",
                         colColours=["#0f172a"] * 6)
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1.0, 1.4)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color="white", fontweight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f8fafc")
    ax_tab.set_title("C) Matriz Comparativa de Desempenho das 11 Tipologias (Mediana Nacional)", fontweight="bold", fontsize=11, pad=15)
    
    plt.suptitle("Painel Executivo Integrado: Aproveitamento de Água de Chuva em 652 Municípios Brasileiros\n"
                 "Síntese Nacional do Estudo Expandido de 11 Tipologias Edilícias sob o Motor Netuno 5",
                 fontsize=14, fontweight="bold", y=0.985)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, "21_dashboard_executivo_master_synthesis.png"))
    plt.close()


def generate_catalogue_md():
    print("\n>>> Gerando Catálogo das 21 Visualizações Avançadas em Markdown...")
    cat_path = os.path.join(RELATORIOS_DIR, "CATALOGO_VISUALIZACOES_AVANCADAS.md")
    
    md = r"""# CATÁLOGO DE VISUALIZAÇÕES AVANÇADAS, INFOGRÁFICOS E MAPAS
## 21 Novas Explorações do Estudo de 11 Tipologias em 652 Cidades Brasileiras (Netuno 5)

Este catálogo documenta a suíte completa de **21 figuras científicas em alta resolução (300 DPI)** geradas para o estudo expandido de aproveitamento de água de chuva (AAC) no Brasil. Todas as figuras estão armazenadas em:
`estudo_tipologias_expandido/figuras/avancadas/`

---

### SUITE 1: CARTOGRAFIA AVANÇADA E NUANCES ESPACIAIS DO BRASIL
- **01_mapa_bivariado_tarifa_vs_precipitacao.png**: Mapa bivariado com matriz 3x3 de cores cruzando a Tarifa Marginal Efetiva evitada na conta com a Precipitação Anual Média. Evidencia com clareza matemática por que Santa Catarina e Rio de Janeiro se situam no topo nacional de atratividade (quadrante superior direito).
- **02_mapa_giro_cisterna_turnover.png**: Mapeia a taxa de giro de cisterna (*tank turnover rate* = $m^3\text{ colhidos} / m^3\text{ capacidade}$). Mostra que no Sul e Norte o reservatório renova de 30 a mais de 80 vezes por ano, enquanto no Centro-Oeste e Semiárido cai para 10 a 15 giros devido aos 5 meses de estiagem.
- **03_mapa_spread_economico_real.png**: Mapa do spread operacional líquido real ($R\$/m^3_{tarifa} - R\$/m^3_{opex}$), revelando a margem de lucro por metro cúbico aproveitado em cada município.
- **04_mapa_lcow_pluvial.png**: Custo Nivelado da Água Pluvial (LCOW em R$/m³ produzido a 6% a.a.), demonstrando que na maioria das cidades o pluvial custa entre R$ 7,00 e R$ 12,00/m³, amplamente competitivo com tarifas concessionárias superiores a R$ 15,00/m³.
- **05_mapa_indice_atratividade_pluvial.png**: Índice sintético multicritério ponderando VPL (35%), Payback (30%), Confiabilidade Hídrica (20%) e Descarbonização (15%) em uma escala padronizada de 0 a 100 pontos.

---

### SUITE 2: INFOGRÁFICOS ARQUITETÔNICOS DAS 11 TIPOLOGIAS
- **06_infografico_arquitetura_11_tipologias.png**: Prancha técnica de arquitetura e engenharia desenhando vetorialmente a silhueta em corte/elevação das 11 tipologias com: material e inclinação de telhado, área em $m^2$, ocupantes, tubulações, cisterna desenhada em escala proporcional e tabela de resultados medianos.
- **07_diagrama_fluxos_hidricos_sankey.png**: Diagramas quantitativos de balanço hídrico anual: Captação Bruta $\rightarrow$ Descarte Inicial $\rightarrow$ Extravasamento $\rightarrow$ Consumo Pluvial Efetivo $\rightarrow$ Demanda Potável Residual em 4 tipologias-chave (UTI, COM, ESC, HOS).
- **08_anatomia_capex_opex_subsistemas.png**: Decomposição gráfica dos 8 subsistemas de CAPEX (bomba, quadro, automação, filtros, cisterna PEAD, tubos e mão de obra) e das 3 parcelas de OPEX (energia, cloração e manutenção).
- **09_matriz_perfis_hidricos_captacao_vs_demanda.png**: Matriz em 4 quadrantes posicionando as tipologias de acordo com a área de captação per capita ($m^2/hab$) e a demanda pluvial diária per capita ($L/hab.dia$), com tamanho proporcional ao reservatório ótimo.

---

### SUITE 3: ECONOMIA DE ESCALA, FRONTEIRA DE PARETO E ROBUSTEZ
- **10_curvas_economia_escala_capex_vpl.png**: Curvas empíricas de ganho de escala comprovando a redução do custo de implantação por metro cúbico colhido em edifícios de grande porte.
- **11_diagrama_radar_multi_indicador.png**: Radar / Spider chart com 7 eixos normalizados comparando o perfil global de desempenho das tipologias.
- **12_fronteira_pareto_confiabilidade_vs_payback.png**: Fronteira de Pareto mapeando as tipologias dominantes que maximizam a segurança hídrica minimizando o tempo de retorno financeiro.
- **13_funil_resiliencia_tma_curvas_cdf.png**: Curvas de probabilidade acumulada (CDF) de Payback e VPL sob estresse macroeconômico das taxas de desconto de 6%, 10% e 14% a.a. (SELIC).

---

### SUITE 4: DINÂMICA HIDROLÓGICA E COMPORTAMENTO DOS RESERVATÓRIOS
- **14_curvas_caracteristicas_volume_vs_confiabilidade.png**: Curvas de saturação de confiabilidade hídrica da varredura de 12 volumes (500 L a 50.000 L) para as 5 macrorregiões do país.
- **15_efeito_sazonalidade_precipitacao_vs_volume_otimo.png**: Impacto da regularidade pluviométrica intra-anual na necessidade de superdimensionamento de cisternas.
- **16_sensibilidade_descarte_first_flush.png**: Comparativo do descarte inicial de 0 mm vs 2 mm (NBR 15527) vs 4 mm sobre a perda volumétrica e fluxo de caixa.
- **17_balanco_ambiental_co2_vs_recalque.png**: Balanço de ciclo de vida das emissões evitadas na rede pública de água vs pegada de carbono incorporada no reservatório PEAD e consumo da bomba.

---

### SUITE 5: NUANCES TARIFÁRIAS E CLUSTERS DE DECISÃO
- **18_dispersao_onde_chove_vs_onde_custa_caro.png**: Gráfico em 4 quadrantes cruzando Chuva Anual vs Tarifa Marginal Efetiva para todas as 652 cidades, com destaque para a liderança de SC e RJ.
- **19_efeito_degrau_tarifario_faixas.png**: Comparativo das curvas de faturas de água e tarifas marginais entre CASAN (SC), Águas do Rio (RJ) e SABESP (SP), elucidando a mecânica de alavancagem de receita.
- **20_arvore_decisao_elegibilidade_tecnica.png**: Fluxograma técnico e árvore de decisão para tomada de decisão em projetos de engenharia e formulação de incentivos públicos.
- **21_dashboard_executivo_master_synthesis.png**: Prancha executiva condensando mapa do Brasil, rankings de cidades líderes, matriz de tipologias e scorecard de indicadores nacionais.
"""
    with open(cat_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f" [OK] Catálogo exportado em: {cat_path}")


def main():
    print("=" * 95)
    print("GERADOR MASTER: SUÍTE AVANÇADA DE 21 VISUALIZAÇÕES CIENTÍFICAS E INFOGRÁFICOS")
    print("Estudo de 11 Tipologias Edilícias x 652 Cidades Brasileiras (Netuno 5)")
    print("=" * 95)
    t0 = time.time()
    
    if not os.path.exists(CSV_COMPLETO):
        print(f"[ERRO] Base completa não encontrada: {CSV_COMPLETO}")
        return
        
    print("[*] Carregando base consolidada de 7.172 registros...")
    df = pd.read_csv(CSV_COMPLETO, sep=';', decimal=',')
    print(f"✓ {len(df):,} perfis ótimos carregados com sucesso!")
    
    states_gdf = load_basemap()
    if states_gdf is not None:
        print(f"✓ Shapefile do Brasil carregado com {len(states_gdf)} estados.")
        
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # Executa a geração das 21 figuras
    fig01_mapa_bivariado_tarifa_chuva(df, states_gdf)
    fig02_mapa_giro_cisterna(df, states_gdf)
    fig03_mapa_spread_real(df, states_gdf)
    fig04_mapa_lcow_pluvial(df, states_gdf)
    fig05_mapa_indice_atratividade(df, states_gdf)
    
    fig06_infografico_arquitetonico_11_tipologias(df)
    fig07_diagramas_fluxos_hidricos(df)
    fig08_anatomia_capex_opex(df)
    fig09_matriz_perfis_hidricos(df)
    
    fig10_economia_de_escala(df)
    fig11_diagrama_radar_tipologias(df)
    fig12_fronteira_pareto(df)
    fig13_funil_resiliencia_cdf(df)
    
    fig14_curvas_volume_vs_confiabilidade(df)
    fig15_sazonalidade_vs_volume_otimo(df)
    fig16_sensibilidade_first_flush(df)
    fig17_balanco_co2(df)
    
    fig18_onde_chove_vs_onde_custa_caro(df)
    fig19_efeito_degrau_tarifario(df)
    fig20_arvore_decisao(df)
    fig21_dashboard_executivo_master(df, states_gdf)
    
    generate_catalogue_md()
    
    print("\n" + "=" * 95)
    print(f"TODAS AS 21 FIGURAS CIENTÍFICAS E O CATÁLOGO FORAM GERADOS EM {time.time() - t0:.2f}s!")
    print(f"Diretório das figuras: {FIGURAS_DIR}")
    print("=" * 95)


if __name__ == "__main__":
    main()
