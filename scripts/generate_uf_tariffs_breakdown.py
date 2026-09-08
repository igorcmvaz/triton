"""
=======================================================================================
NETUNO 5 -- AUDITORIA VISUAL DETALHADA DAS TARIFAS DE SANEAMENTO E ENERGIA (27 UFs)
=======================================================================================
Gera gráfico de alta resolução com 4 painéis detalhando por Unidade da Federação:
1. Estrutura da Tarifa de Água (R$/m³) - Faixa Inicial (Mínima) vs Faixa Típica (10-15 m³)
2. Alíquota Regulatória de Esgoto (% sobre a água: 100%, 85%, 80%, 70%, 50%)
3. Tarifa Combinada Água + Esgoto (R$/m³)
4. Tarifa Residencial de Eletricidade B1 ANEEL (R$/kWh)
=======================================================================================
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.recalc_full_study_with_real_tariffs import load_tariff_dictionary

STUDY_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz")
OUTPUT_FIG_DIR = os.path.join(STUDY_DIR, "figuras")
os.makedirs(OUTPUT_FIG_DIR, exist_ok=True)

# Estilo gráfico moderno
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 10,
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 10,
    'legend.fontsize': 9.5,
    'figure.titlesize': 13,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

def generate_uf_tariff_charts():
    print(" [*] Carregando dicionário tarifário de 652 municípios...")
    city_tariffs = load_tariff_dictionary()
    
    records = []
    for c, info in city_tariffs.items():
        tariffs = info['tariffs']
        vol_rates = [t[2] for t in tariffs if t[3] == 1 and t[2] > 0]
        # Tarifa inicial e tarifa intermediaria (10-15 m3 se houver)
        init_rate = vol_rates[0] if vol_rates else 5.50
        mid_rate = vol_rates[min(2, len(vol_rates)-1)] if len(vol_rates) > 1 else init_rate
        
        records.append({
            'city': c,
            'uf': info['uf'],
            'regiao': info['regiao'],
            'prestador': info['prestador'],
            'base_water_rate': info['base_water_rate'],
            'init_water_rate': init_rate,
            'mid_water_rate': mid_rate,
            'sewage_rate': info['sewage_rate'],
            'elec_tariff': info['elec_tariff'],
            'combined_tariff': info['base_water_rate'] * (1.0 + info['sewage_rate'] / 100.0)
        })
    df = pd.DataFrame(records)
    
    # Agregação por UF
    reg_order_map = {'Norte': 1, 'Nordeste': 2, 'Centro-Oeste': 3, 'Sudeste': 4, 'Sul': 5}
    df['reg_num'] = df['regiao'].map(reg_order_map)
    
    uf_agg = df.groupby(['regiao', 'reg_num', 'uf']).agg({
        'city': 'count',
        'base_water_rate': 'mean',
        'init_water_rate': 'mean',
        'mid_water_rate': 'mean',
        'sewage_rate': 'mean',
        'elec_tariff': 'mean',
        'combined_tariff': 'mean'
    }).reset_index().sort_values(['reg_num', 'uf']).reset_index(drop=True)
    
    # Cores por Macrorregião
    region_colors = {
        'Norte': '#1b9e77',
        'Nordeste': '#d95f02',
        'Centro-Oeste': '#7570b3',
        'Sudeste': '#e7298a',
        'Sul': '#377eb8'
    }
    bar_colors = [region_colors[r] for r in uf_agg['regiao']]
    
    fig, axes = plt.subplots(4, 1, figsize=(18, 20), sharex=True)
    
    x = np.arange(len(uf_agg))
    ufs = uf_agg['uf'].tolist()
    
    # =========================================================================
    # PAINEL 1: TARIFA BASE DE ÁGUA (R$/m³)
    # =========================================================================
    bars1 = axes[0].bar(x, uf_agg['base_water_rate'], color=bar_colors, edgecolor='black', linewidth=0.8, alpha=0.88)
    axes[0].set_title('A) Tarifa Média Efetiva de Água Pura (R$/m³) para Consumo Padrão Residencial de 18,26 m³/mês (4 hab × 150 L/dia)', fontweight='bold', fontsize=12.5)
    axes[0].set_ylabel('Tarifa Efetiva de Água (R$/m³)', fontweight='bold')
    axes[0].set_ylim(0, max(uf_agg['base_water_rate']) * 1.25)
    axes[0].grid(True, linestyle='--', alpha=0.5, axis='y')
    axes[0].axhline(uf_agg['base_water_rate'].mean(), color='red', linestyle='--', linewidth=1.5, label=f"Média Nacional: R$ {uf_agg['base_water_rate'].mean():.2f}/m³")
    
    for bar, val in zip(bars1, uf_agg['base_water_rate']):
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.25, f"R$ {val:.2f}".replace('.', ','), ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=45)
    axes[0].legend(loc='upper right')
    
    # =========================================================================
    # PAINEL 2: ALÍQUOTA DE ESGOTO (% SOBRE A ÁGUA)
    # =========================================================================
    bars2 = axes[1].bar(x, uf_agg['sewage_rate'], color=bar_colors, edgecolor='black', linewidth=0.8, alpha=0.88)
    axes[1].set_title('B) Alíquota Regulatória de Esgoto (% sobre o valor da Água)', fontweight='bold', fontsize=12.5)
    axes[1].set_ylabel('Alíquota de Esgoto (%)', fontweight='bold')
    axes[1].set_ylim(0, 118)
    axes[1].grid(True, linestyle='--', alpha=0.5, axis='y')
    axes[1].axhline(80.0, color='gray', linestyle=':', linewidth=1.2, label='Padrão Sanepar / Sabesp / Copasa (80%)')
    axes[1].axhline(100.0, color='darkred', linestyle=':', linewidth=1.2, label='Alíquota Integral (100%)')
    
    for bar, val in zip(bars2, uf_agg['sewage_rate']):
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{val:.0f}%" if val.is_integer() else f"{val:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    axes[1].legend(loc='upper right')
    
    # =========================================================================
    # PAINEL 3: TARIFA COMBINADA ÁGUA + ESGOTO (R$/m³)
    # =========================================================================
    bars3 = axes[2].bar(x, uf_agg['combined_tariff'], color=bar_colors, edgecolor='black', linewidth=0.8, alpha=0.88)
    axes[2].set_title('C) Tarifa Média Combinada Efetiva de Água + Esgoto (R$/m³) para Consumo de 18,26 m³/mês', fontweight='bold', fontsize=12.5)
    axes[2].set_ylabel('Combinada (R$/m³)', fontweight='bold')
    axes[2].set_ylim(0, max(uf_agg['combined_tariff']) * 1.25)
    axes[2].grid(True, linestyle='--', alpha=0.5, axis='y')
    axes[2].axhline(uf_agg['combined_tariff'].mean(), color='red', linestyle='--', linewidth=1.5, label=f"Média Nacional: R$ {uf_agg['combined_tariff'].mean():.2f}/m³")
    
    for bar, val in zip(bars3, uf_agg['combined_tariff']):
        h = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2, h + 0.35, f"R$ {val:.2f}".replace('.', ','), ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=45)
    axes[2].legend(loc='upper right')
    
    # =========================================================================
    # PAINEL 4: TARIFA RESIDENCIAL DE ENERGIA ELÉTRICA B1 ANEEL (R$/kWh)
    # =========================================================================
    bars4 = axes[3].bar(x, uf_agg['elec_tariff'], color=bar_colors, edgecolor='black', linewidth=0.8, alpha=0.88)
    axes[3].set_title('D) Tarifa Residencial de Eletricidade B1 ANEEL (R$/kWh)', fontweight='bold', fontsize=12.5)
    axes[3].set_ylabel('Tarifa B1 (R$/kWh)', fontweight='bold')
    axes[3].set_ylim(0, 1.25)
    axes[3].grid(True, linestyle='--', alpha=0.5, axis='y')
    axes[3].axhline(uf_agg['elec_tariff'].mean(), color='red', linestyle='--', linewidth=1.5, label=f"Média Nacional: R$ {uf_agg['elec_tariff'].mean():.2f}/kWh")
    
    for bar, val in zip(bars4, uf_agg['elec_tariff']):
        h = bar.get_height()
        axes[3].text(bar.get_x() + bar.get_width()/2, h + 0.02, f"R$ {val:.2f}".replace('.', ','), ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    axes[3].legend(loc='upper right')
    
    axes[3].set_xticks(x)
    axes[3].set_xticklabels([f"{uf}\n({reg})" for uf, reg in zip(ufs, uf_agg['regiao'])], fontweight='bold', fontsize=9)
    axes[3].set_xlabel('Unidade da Federação e Macrorregião Brasileira', fontweight='bold', fontsize=11)
    
    # Legenda de Regiões
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=col, edgecolor='black', label=reg) for reg, col in region_colors.items()]
    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.995), ncol=5, frameon=True, fontsize=10, title="Macrorregiões do Brasil", title_fontsize=11)
    
    plt.suptitle("Estrutura Tarifária Auditada das 27 Unidades da Federação (Consumo Benchmark: 18,26 m³/mês)", fontweight='bold', fontsize=15, y=1.015)
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_FIG_DIR, "figura_tarifas_detalhadas_por_estado_27_ufs.png")
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f" [OK] Gráfico comparativo de tarifas por estado salvo em: {out_path}")
    
    # Gerar também gráfico focado no Paraná (Sanepar por cidades)
    generate_parana_focus_chart(df, city_tariffs)

def generate_parana_focus_chart(df, city_tariffs):
    df_pr = df[df['uf'] == 'PR'].sort_values('city').reset_index(drop=True)
    if df_pr.empty:
        return
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    x = np.arange(len(df_pr))
    
    # A) Tarifa Água e Combinada
    w = 0.38
    b1 = axes[0].bar(x - w/2, df_pr['base_water_rate'], w, label='Tarifa Média Efetiva de Água Pura (R$/m³ para 18,26 m³)', color='#377eb8', edgecolor='black', alpha=0.88)
    b2 = axes[0].bar(x + w/2, df_pr['combined_tariff'], w, label='Tarifa Média Combinada Água + Esgoto (R$/m³ para 18,26 m³)', color='#e41a1c', edgecolor='black', alpha=0.85)
    axes[0].set_title('A) Paraná (SANEPAR) — Tarifas Efetivas Médias para Consumo Padrão de 18,26 m³/mês (34 Cidades)', fontweight='bold', fontsize=12)
    axes[0].set_ylabel('Tarifa Média (R$/m³)', fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(df_pr['city'], rotation=90, fontsize=8.5, fontweight='bold')
    axes[0].legend(loc='upper right')
    axes[0].grid(True, linestyle='--', alpha=0.5, axis='y')
    axes[0].set_ylim(0, 22)
    
    for bar in b1:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}", ha='center', va='bottom', fontsize=7, rotation=90)
    for bar in b2:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}", ha='center', va='bottom', fontsize=7, rotation=90)
        
    # B) Alíquota de Esgoto (%)
    bars_esg = axes[1].bar(x, df_pr['sewage_rate'], color='#4daf4a', edgecolor='black', alpha=0.88, width=0.55)
    axes[1].set_title('B) Alíquota Regulatória de Esgoto SANEPAR (% sobre água: Curitiba 85% vs Demais Cidades 80%)', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('Alíquota de Esgoto (%)', fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(df_pr['city'], rotation=90, fontsize=8.5, fontweight='bold')
    axes[1].set_ylim(0, 105)
    axes[1].grid(True, linestyle='--', alpha=0.5, axis='y')
    
    for bar, val in zip(bars_esg, df_pr['sewage_rate']):
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{val:.0f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
        
    plt.tight_layout()
    out_pr = os.path.join(OUTPUT_FIG_DIR, "figura_tarifas_detalhadas_parana_sanepar.png")
    plt.savefig(out_pr, bbox_inches='tight')
    plt.close()
    print(f" [OK] Gráfico focado no Paraná (Sanepar) salvo em: {out_pr}")

if __name__ == '__main__':
    generate_uf_tariff_charts()
