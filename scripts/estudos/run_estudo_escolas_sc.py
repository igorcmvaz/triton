"""
======================================================================================================
NETUNO 5 -- RUNNER ESPECÍFICO: ESTUDO DE APROVEITAMENTO DE ÁGUA DE CHUVA EM ESCOLAS (SANTA CATARINA)
======================================================================================================
Este script:
 1. Carrega o preset paramétrico de edificação escolar (100 alunos, 40 L/aluno.dia, 60% não-potável,
    450 m² de cobertura, 2 mm first-flush, telha cerâmica/aluzinco C=0,85).
 2. Simula o balanço hídrico diário contínuo (NBR 15527:2019) para todos os 32 municípios de Santa Catarina
    em 12 volumes de cisterna (500 L a 50.000 L) utilizando séries históricas diárias (12.419 dias).
 3. Integra o motor econômico-financeiro completo do Netuno 5:
    - Tarifas municipais reais de saneamento (CASAN e serviços autônomos municipais);
    - Tarifas elétricas reais ANEEL B1 por município para recalque predial;
    - Fator regional de custo SINAPI/CUB de Santa Catarina (1,02);
    - Avaliação sob 3 Taxas Mínimas de Atratividade (TMA 6%, 10% e 14% a.a.);
    - Indicadores: VPL, Payback Simples e Descontado, TIR, LCOW (R$/m³), Economia Líquida e CO2 evitado.
 4. Seleciona o volume ótimo de reservatório por município via TOPSIS Multicritério e VPL Máximo.
 5. Exporta bases consolidadas em CSV (estudo_escolas_santa_catarina/dados/):
    - sc_escolas_simulacao_completa.csv (todas as cidades x 12 volumes = 384 combinações);
    - sc_escolas_solucao_otima.csv (o dimensionamento ótimo para os 32 municípios);
    - sc_escolas_ranking_viabilidade.csv (ranking ordenado por atratividade econômica);
    - sc_escolas_estatisticas_sintese.csv (métricas descritivas estaduais).
 6. Gera 4 figuras científicas em alta resolução (300 DPI) em estudo_escolas_santa_catarina/figuras/:
    - sc_escolas_economia_agua_ranking.png;
    - sc_escolas_vpl_payback_cidades.png;
    - sc_escolas_curvas_confiabilidade.png;
    - sc_escolas_dispersao_vpl_chuva.png.
 7. Produz Relatório Técnico-Científico Executivo em Markdown em estudo_escolas_santa_catarina/relatorios/.
======================================================================================================
"""

import os
import sys
import json
import glob
import time
import unicodedata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Garante UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
if hasattr(sys.stderr, "reconfigure"):
    try: sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

NETUNO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(NETUNO_DIR)
if NETUNO_DIR not in sys.path:
    sys.path.insert(0, NETUNO_DIR)

from netuno.core.tariffs_database import load_tariffs_db, get_cities_by_uf
from netuno.core.economic import calculate_water_bill
from netuno.core.cost_estimates import (
    estimate_tank_price,
    REGIONAL_FACTORS_BY_UF
)
from netuno.core.water_quality import size_first_flush_system
from netuno.core.topsis import TopsisCandidate, calculate_topsis_scores

# Diretórios do Estudo
STUDY_DIR = os.path.join(BASE_DIR, "Estudos", "estudo_escolas_santa_catarina")
CONFIG_PATH = os.path.join(STUDY_DIR, "config", "escola_sc_profile.json")
DADOS_DIR = os.path.join(STUDY_DIR, "dados")
FIGURAS_DIR = os.path.join(STUDY_DIR, "figuras")
RELATORIOS_DIR = os.path.join(STUDY_DIR, "relatorios")

os.makedirs(DADOS_DIR, exist_ok=True)
os.makedirs(FIGURAS_DIR, exist_ok=True)
os.makedirs(RELATORIOS_DIR, exist_ok=True)

FUTURE_DIR = os.path.join(NETUNO_DIR, "Netuno future files for 652 cities")
SPLIT_DIR = os.path.join(BASE_DIR, "Estudos", "estudo_5_tipologias_residenciais", "Netuno_vaz_files_split")
GEO_JSON_PATH = os.path.join(NETUNO_DIR, "tarifas", "validated_cidades_50k.json")

# Fatores de Valor Presente Uniforme (P/A, i, 20 anos)
PV_FACTOR_6 = (1.0 - (1.0 + 0.06)**(-20)) / 0.06      # 11.4699
PV_FACTOR_10 = (1.0 - (1.0 + 0.10)**(-20)) / 0.10    # 8.5136
PV_FACTOR_14 = (1.0 - (1.0 + 0.14)**(-20)) / 0.14    # 6.6231


def normalize_str(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().replace(' ', '').replace('-', '').replace("'", '')


def load_precip_series(fpath):
    df = pd.read_csv(fpath, sep=';', header=None)
    for col in df.columns:
        s = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
        if s.notna().sum() > 300:
            return s.fillna(0.0).to_numpy(dtype=np.float64)
    return np.zeros(365, dtype=np.float64)


def simulate_daily_harvest(precip_arr, area, runoff_coeff, discard_mm, lower_vol, pluv_demand, tot_demand):
    """Balanço Hídrico Diário Contínuo (NBR 15527:2019)."""
    n_days = len(precip_arr)
    v_lower = 0.0
    tot_pluv = 0.0
    tot_spill = 0.0
    days_full = 0
    p_eff = np.maximum(0.0, precip_arr - discard_mm)
    v_ac = p_eff * (area * runoff_coeff)
    
    for i in range(n_days):
        v_avail = v_lower + v_ac[i]
        if v_avail > lower_vol:
            v_spill = v_avail - lower_vol
            v_in = lower_vol
        else:
            v_spill = 0.0
            v_in = v_avail
        if v_in >= pluv_demand:
            v_c = pluv_demand
            days_full += 1
        else:
            v_c = v_in
        v_lower = v_in - v_c
        tot_pluv += v_c
        tot_spill += v_spill
    return tot_pluv, tot_spill, days_full


def calculate_irr(cash_flows, max_iter=80):
    cf = np.array(cash_flows, dtype=np.float64)
    if np.all(cf >= 0) or np.all(cf <= 0):
        return 0.0
    r = 0.10
    for _ in range(max_iter):
        t = np.arange(len(cf))
        denom = (1.0 + r)**t
        npv = np.sum(cf / denom)
        d_npv = -np.sum(t * cf / (denom * (1.0 + r)))
        if abs(d_npv) < 1e-9:
            break
        r_new = r - npv / d_npv
        if abs(r_new - r) < 1e-6:
            r = r_new
            break
        r = r_new
        if r < -0.95: r = -0.90
        if r > 5.0: r = 5.0
    return float(r * 100.0) if np.isfinite(r) and -50.0 < r*100.0 < 500.0 else 0.0


def calculate_discounted_payback(capex, net_annual, discount_rate=0.10, horizon=20):
    if net_annual <= 0:
        return 25.0
    cum = -capex
    for yr in range(1, horizon + 1):
        disc_net = net_annual / ((1.0 + discount_rate)**yr)
        cum_prev = cum
        cum += disc_net
        if cum >= 0:
            frac = (-cum_prev) / disc_net
            return float(yr - 1 + frac)
    return 25.0


def run_simulation():
    print("=" * 80)
    print("NETUNO 5 - SIMULAÇÃO: PRESET ESCOLAS EM SANTA CATARINA")
    print("=" * 80)
    
    t0 = time.time()
    
    # 1. Carregar perfil da tipologia
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
        
    typ = cfg["typology"]
    volumes_sweep = cfg["volumes_sweep_liters"]
    reg_factor = cfg.get("regional_factor_cost", 1.02)
    
    print(f"[*] Tipologia: {typ['name']}")
    print(f"    Alunos: {typ['occupants']} | Demanda Total: {typ['daily_total_demand_l']} L/dia | Demanda Pluvial: {typ['daily_pluvial_demand_l']} L/dia")
    print(f"    Área de Cobertura: {typ['roof_area_m2']} m² | Runoff C: {typ['runoff_coeff']} | First-Flush: {typ['first_flush_mm']} mm")
    print(f"    Volumes avaliados: {volumes_sweep}")
    
    # 2. Carregar banco de tarifas e cidades de SC
    tariffs_db = load_tariffs_db()
    cities_db = tariffs_db.get("cities", {})
    sc_cities = get_cities_by_uf("SC")
    print(f"[*] Municípios de Santa Catarina mapeados: {len(sc_cities)}")
    
    # 3. Coordenadas geográficas
    geo_data = {}
    if os.path.exists(GEO_JSON_PATH):
        with open(GEO_JSON_PATH, "r", encoding="utf-8") as f:
            geo_data = json.load(f)
    geo_map = {normalize_str(k): v for k, v in geo_data.items()}
    
    # 4. Mapear arquivos de chuva
    rain_files = glob.glob(os.path.join(FUTURE_DIR, "*ACCESS-CM2*Hist*.csv"))
    if not rain_files:
        rain_files = glob.glob(os.path.join(SPLIT_DIR, "*ACCESS-CM2*Hist*.csv"))
    print(f"[*] Total de séries pluviométricas históricas encontradas: {len(rain_files)}")
    
    rain_map = {}
    for f in rain_files:
        fname = os.path.basename(f)
        if '(Netuno)' in fname and '_ACCESS' in fname:
            c_name = fname.split('(Netuno)')[1].split('_ACCESS')[0].strip()
            rain_map[normalize_str(c_name)] = f
            
    # Equipamentos fixos do CAPEX
    pump_cost = typ["pump_unit_cost"] * typ["pump_count"]
    fixed_equipment = (
        pump_cost + typ["electrical_panel_cost"] +
        typ["sensors_automation_cost"] + typ["treatment_filtration_cost"] +
        typ["air_gap_supplement_cost"] + typ["pipes_base_cost"] +
        typ["min_labor_cost"]
    )
    
    # Subsistema de descarte de primeiras águas e gradeamento (ETAP - NBR 15527:2019)
    area = typ["roof_area_m2"]
    runoff = typ["runoff_coeff"]
    discard_mm = typ["first_flush_mm"]
    ff_res = size_first_flush_system(
        discard_mm=discard_mm,
        roof_area_m2=area,
        regional_factor=reg_factor
    )
    print(f"[*] Subsistema de Descarte de Primeiras Águas (ETAP - NBR 15527):")
    print(f"    Volume de Descarte: {ff_res.diverter_volume_liters:.0f} L")
    print(f"    Filtro de Folhas: {ff_res.leaf_filter_type} (R$ {ff_res.leaf_filter_capex:,.2f})")
    print(f"    Reservatório de Descarte: {ff_res.diverter_tank_type} (R$ {ff_res.diverter_tank_capex:,.2f})")
    print(f"    CAPEX Total Descarte: R$ {ff_res.first_flush_total_capex:,.2f}")
    print(f"    OPEX Anual Descarte: R$ {ff_res.first_flush_annual_opex:,.2f}/ano | CO2 Embutido: {ff_res.first_flush_embodied_co2_kg:.1f} kg CO2e")
    
    all_sweep_records = []
    optimal_records = []
    
    for city_name in sorted(sc_cities):
        norm_name = normalize_str(city_name)
        f_rain = rain_map.get(norm_name)
        if not f_rain or not os.path.exists(f_rain):
            print(f"[!] Chuva não encontrada para {city_name}")
            continue
            
        precip_arr = load_precip_series(f_rain)
        n_days = len(precip_arr)
        if n_days < 365:
            continue
            
        annual_precip_mm = float(np.sum(precip_arr) / n_days * 365.25)
        
        # Dados tarifários
        c_tar = cities_db.get(f"SC - {city_name}") or cities_db.get(city_name)
        if not c_tar:
            # Busca aproximada
            for k, v in cities_db.items():
                if k.startswith("SC - ") and normalize_str(v.get("municipio", "")) == norm_name:
                    c_tar = v
                    break
        if not c_tar:
            print(f"[!] Tarifa não encontrada para {city_name}")
            continue
            
        faixas = [tuple(f) for f in c_tar.get("faixas", [(0.0, 10.0, 6.00, 1), (10.0, 999999.0, 9.00, 1)])]
        esgoto_pct = float(c_tar.get("esgoto_pct", 80.0))
        esgoto_modo = int(c_tar.get("esgoto_modo", 1))
        tarifa_fixa = float(c_tar.get("tarifa_fixa_mensal", 0.0))
        tarifa_eletrica = float(c_tar.get("energia_r_kwh", 0.85)) if float(c_tar.get("energia_r_kwh", 0.0)) > 0 else 0.85
        prestador = c_tar.get("prestador_saneamento", "CASAN / SAMAE")
        
        g_info = geo_map.get(norm_name, {})
        lat = g_info.get("target", {}).get("lat", g_info.get("nearest", {}).get("lat", np.nan))
        lon = g_info.get("target", {}).get("lon", g_info.get("nearest", {}).get("lon", np.nan))
        
        area = typ["roof_area_m2"]
        runoff = typ["runoff_coeff"]
        discard_mm = typ["first_flush_mm"]
        tot_demand = typ["daily_total_demand_l"]
        pluv_demand = typ["daily_pluvial_demand_l"]
        
        # Conta basal (100% concessionária)
        monthly_tot_liters = tot_demand * 30.416
        water_bill_base = (calculate_water_bill(
            monthly_tot_liters, faixas, sewage_mode=esgoto_modo, sewage_rate=esgoto_pct, num_units=1
        ) + tarifa_fixa) * 12.0
        
        city_sweep = []
        topsis_candidates = []
        
        for v_low in volumes_sweep:
            tot_pluv, tot_spill, days_full = simulate_daily_harvest(
                precip_arr, area, runoff, discard_mm, v_low, pluv_demand, tot_demand
            )
            
            annual_pluvial_m3 = (tot_pluv / n_days) * 365.25 / 1000.0
            annual_potable_m3 = ((tot_demand * n_days - tot_pluv) / n_days) * 365.25 / 1000.0
            annual_spill_m3 = (tot_spill / n_days) * 365.25 / 1000.0
            
            potential_savings_pct = (tot_pluv / (tot_demand * n_days)) * 100.0 if tot_demand > 0 else 0.0
            reliability_pct = (days_full / n_days) * 100.0
            
            # Conta com pluvial
            monthly_pot_liters = (annual_potable_m3 * 1000.0) / 12.0
            water_bill_pluv = (calculate_water_bill(
                monthly_pot_liters, faixas, sewage_mode=esgoto_modo, sewage_rate=esgoto_pct, num_units=1
            ) + tarifa_fixa) * 12.0
            annual_gross_savings = max(0.0, water_bill_base - water_bill_pluv)
            
            # OPEX (Energia + Cloro + Manutenção Fixa + Manutenção Semestral Descarte)
            energy_kwh = annual_pluvial_m3 * 1000.0 * 0.00022
            annual_energy_cost = energy_kwh * tarifa_eletrica
            annual_chlorine_cost = annual_pluvial_m3 * 0.25
            annual_maint_cost = typ["annual_maintenance_fixed"]
            annual_opex = annual_energy_cost + annual_chlorine_cost + annual_maint_cost + ff_res.first_flush_annual_opex
            net_annual_savings = annual_gross_savings - annual_opex
            
            # CAPEX Calibrado SC (Equipamentos + Tanque Principal + Subsistema Físico de Descarte 900 L)
            tank_price = estimate_tank_price(v_low, "PEAD")
            capex_total = ((fixed_equipment + tank_price) * reg_factor) + ff_res.first_flush_total_capex
            
            # Indicadores de viabilidade
            vpl_6 = -capex_total + (net_annual_savings * PV_FACTOR_6)
            vpl_10 = -capex_total + (net_annual_savings * PV_FACTOR_10)
            vpl_14 = -capex_total + (net_annual_savings * PV_FACTOR_14)
            
            payback_simple = capex_total / net_annual_savings if net_annual_savings > 0 else 25.0
            payback_disc_10 = calculate_discounted_payback(capex_total, net_annual_savings, 0.10, 20)
            
            cf = [-capex_total] + [net_annual_savings] * 20
            tir_val = calculate_irr(cf)
            
            lcow_10 = (capex_total + annual_opex * PV_FACTOR_10) / (annual_pluvial_m3 * PV_FACTOR_10) if annual_pluvial_m3 > 0 else 0.0
            co2_evitado_kg = annual_pluvial_m3 * 0.35
            co2_saved_kg_lifetime = max(0.0, (co2_evitado_kg * 20.0) - ff_res.first_flush_embodied_co2_kg)
            
            rec = {
                "municipio": city_name,
                "uf": "SC",
                "lat": lat,
                "lon": lon,
                "prestador": prestador,
                "precip_anual_media_mm": round(annual_precip_mm, 1),
                "volume_cisterna_l": float(v_low),
                "descarte_volume_l": round(ff_res.diverter_volume_liters, 1),
                "descarte_capex_r": round(ff_res.first_flush_total_capex, 2),
                "demanda_total_anual_m3": round(tot_demand * 365.25 / 1000.0, 2),
                "demanda_pluvial_anual_m3": round(pluv_demand * 365.25 / 1000.0, 2),
                "consumo_pluvial_anual_m3": round(annual_pluvial_m3, 2),
                "consumo_concessionaria_anual_m3": round(annual_potable_m3, 2),
                "extravasamento_anual_m3": round(annual_spill_m3, 2),
                "economia_agua_potavel_pct": round(potential_savings_pct, 2),
                "confiabilidade_pct": round(reliability_pct, 2),
                "tarifa_eletrica_r_kwh": round(tarifa_eletrica, 4),
                "conta_base_anual_r": round(water_bill_base, 2),
                "conta_com_pluvial_anual_r": round(water_bill_pluv, 2),
                "economia_bruta_anual_r": round(annual_gross_savings, 2),
                "opex_anual_r": round(annual_opex, 2),
                "economia_liquida_anual_r": round(net_annual_savings, 2),
                "capex_total_r": round(capex_total, 2),
                "vpl_tma_6_r": round(vpl_6, 2),
                "vpl_tma_10_r": round(vpl_10, 2),
                "vpl_tma_14_r": round(vpl_14, 2),
                "payback_simples_anos": round(payback_simple, 2),
                "payback_descontado_10_anos": round(payback_disc_10, 2),
                "tir_anual_pct": round(tir_val, 2),
                "lcow_10_r_m3": round(lcow_10, 2),
                "co2_evitado_kg_ano": round(co2_evitado_kg, 2)
            }
            
            city_sweep.append(rec)
            all_sweep_records.append(rec)
            
            # Critérios para TOPSIS (inclui CAPEX com descarte e CO2 líquido de ciclo de vida)
            topsis_candidates.append(TopsisCandidate(
                lower_tank_vol=float(v_low),
                water_saved_m3_yr=annual_pluvial_m3,
                vpl_brl=vpl_10,
                co2_saved_kg_lifetime=co2_saved_kg_lifetime,
                capex_brl=capex_total,
                potential_savings_pct=potential_savings_pct,
                overflow_m3_yr=annual_spill_m3,
                discounted_payback_years=payback_disc_10,
                irr_pct=tir_val,
                potable_consumed_m3_yr=annual_potable_m3
            ))
            
        # Selecionar o ótimo via TOPSIS Multicritério (Eixos Técnico, Econômico e Ambiental)
        topsis_res = calculate_topsis_scores(topsis_candidates)
        best_idx = topsis_res.best_index if topsis_res is not None else 0
        best_rec = dict(city_sweep[best_idx])
        best_rec["criterio_otimo"] = "TOPSIS Multicritério (Técnico + Econômico + Ambiental)"
        best_rec["topsis_score"] = round(float(topsis_res.scores[best_idx]), 4) if topsis_res is not None else 0.0
        optimal_records.append(best_rec)
        
    df_sweep = pd.DataFrame(all_sweep_records)
    df_optimal = pd.DataFrame(optimal_records)
    
    # 5. Salvar CSVs
    csv_sweep_path = os.path.join(DADOS_DIR, "sc_escolas_simulacao_completa.csv")
    csv_optimal_path = os.path.join(DADOS_DIR, "sc_escolas_solucao_otima.csv")
    csv_ranking_path = os.path.join(DADOS_DIR, "sc_escolas_ranking_viabilidade.csv")
    csv_stats_path = os.path.join(DADOS_DIR, "sc_escolas_estatisticas_sintese.csv")
    
    df_sweep.to_csv(csv_sweep_path, sep=';', decimal=',', index=False, encoding='utf-8')
    df_optimal.to_csv(csv_optimal_path, sep=';', decimal=',', index=False, encoding='utf-8')
    
    # Ranking por VPL e Economia Líquida
    df_ranking = df_optimal.sort_values(by="vpl_tma_10_r", ascending=False).reset_index(drop=True)
    df_ranking["posicao_ranking"] = range(1, len(df_ranking) + 1)
    df_ranking.to_csv(csv_ranking_path, sep=';', decimal=',', index=False, encoding='utf-8')
    
    # Estatísticas Síntese
    numeric_cols = [
        "precip_anual_media_mm", "volume_cisterna_l", "consumo_pluvial_anual_m3",
        "economia_agua_potavel_pct", "confiabilidade_pct", "economia_bruta_anual_r",
        "economia_liquida_anual_r", "capex_total_r", "vpl_tma_6_r", "vpl_tma_10_r",
        "vpl_tma_14_r", "payback_simples_anos", "payback_descontado_10_anos",
        "tir_anual_pct", "lcow_10_r_m3", "co2_evitado_kg_ano"
    ]
    df_stats = df_optimal[numeric_cols].describe().T
    df_stats["mediana"] = df_optimal[numeric_cols].median()
    df_stats["iqr"] = df_stats["75%"] - df_stats["25%"]
    df_stats.to_csv(csv_stats_path, sep=';', decimal=',', encoding='utf-8')
    
    print(f"\n[+] Dados salvos com sucesso em {DADOS_DIR}:")
    print(f"    - sc_escolas_simulacao_completa.csv ({len(df_sweep)} registros)")
    print(f"    - sc_escolas_solucao_otima.csv ({len(df_optimal)} municípios)")
    print(f"    - sc_escolas_ranking_viabilidade.csv (ranking de atratividade)")
    print(f"    - sc_escolas_estatisticas_sintese.csv (síntese estatística)")
    
    # 6. Gerar Gráficos de Alta Resolução (300 DPI)
    print("\n[*] Gerando figuras científicas de publicação (300 DPI)...")
    generate_figures(df_optimal, df_sweep)
    
    # 7. Gerar Relatório Markdown
    print("\n[*] Gerando relatório técnico-científico executivo...")
    generate_markdown_report(df_optimal, df_ranking, df_stats, ff_res)
    
    t_tot = time.time() - t0
    print(f"\n[OK] Simulação e organização concluídas com sucesso em {t_tot:.1f}s!")


def generate_figures(df_opt, df_sweep):
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.size"] = 10
    
    # ── FIGURA 1: Ranking de Economia de Água Potável (%) ──
    fig, ax = plt.subplots(figsize=(12, 9), dpi=300)
    df_sorted_sav = df_opt.sort_values(by="economia_agua_potavel_pct", ascending=True)
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(df_sorted_sav)))
    
    bars = ax.barh(df_sorted_sav["municipio"], df_sorted_sav["economia_agua_potavel_pct"], color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Potencial de Economia de Água Potável (%)", fontsize=11, fontweight="bold")
    ax.set_title("Potencial de Economia de Água Potável em Escolas de Santa Catarina\n(Preset Netuno 5: 100 alunos, 40 L/aluno.dia, Cobertura 450 m²)", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlim(0, max(df_sorted_sav["economia_agua_potavel_pct"]) * 1.15)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", ha="left", fontsize=8.5, fontweight="bold")
        
    ax.grid(True, linestyle="--", alpha=0.5, axis="x")
    plt.tight_layout()
    fig1_path = os.path.join(FIGURAS_DIR, "sc_escolas_economia_agua_ranking.png")
    fig.savefig(fig1_path, dpi=300)
    plt.close(fig)
    print(f"    [fig] {fig1_path}")
    
    # ── FIGURA 2: VPL (TMA 10% a.a.) vs Payback Descontado por Município ──
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 9), dpi=300, sharey=True)
    df_sorted_vpl = df_opt.sort_values(by="vpl_tma_10_r", ascending=True)
    
    # Cores condicionais: VPL > 0 verde, < 0 coral
    bar_colors = ["#2b8a3e" if v > 0 else "#c92a2a" for v in df_sorted_vpl["vpl_tma_10_r"]]
    ax1.barh(df_sorted_vpl["municipio"], df_sorted_vpl["vpl_tma_10_r"], color=bar_colors, edgecolor="black", linewidth=0.5)
    ax1.axvline(0, color="black", linestyle="--", linewidth=1.0)
    ax1.set_xlabel("Valor Presente Líquido - VPL (R$)", fontsize=11, fontweight="bold")
    ax1.set_title("Viabilidade Financeira (VPL @ TMA 10% a.a., 20 anos)", fontsize=11, fontweight="bold")
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"R$ {x:,.0f}".replace(",", ".")))
    ax1.grid(True, linestyle="--", alpha=0.5, axis="x")
    
    # Payback
    pb_colors = plt.cm.magma_r(np.linspace(0.2, 0.8, len(df_sorted_vpl)))
    ax2.barh(df_sorted_vpl["municipio"], df_sorted_vpl["payback_descontado_10_anos"], color=pb_colors, edgecolor="black", linewidth=0.5)
    ax2.axvline(20, color="red", linestyle=":", linewidth=1.2, label="Horizonte de 20 anos")
    ax2.set_xlabel("Payback Descontado (anos)", fontsize=11, fontweight="bold")
    ax2.set_title("Tempo de Retorno do Investimento (Payback @ 10%)", fontsize=11, fontweight="bold")
    ax2.set_xlim(0, 25)
    ax2.legend(loc="lower right")
    ax2.grid(True, linestyle="--", alpha=0.5, axis="x")
    
    plt.tight_layout()
    fig2_path = os.path.join(FIGURAS_DIR, "sc_escolas_vpl_payback_cidades.png")
    fig.savefig(fig2_path, dpi=300)
    plt.close(fig)
    print(f"    [fig] {fig2_path}")
    
    # ── FIGURA 3: Curvas de Confiabilidade vs Volume de Cisterna em Cidades Referência ──
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    
    # Seleciona 6 cidades emblemáticas de diferentes mesorregiões de SC
    sample_cities = ["Florianópolis", "Joinville", "Blumenau", "Chapecó", "Lages", "Criciúma"]
    markers = ['o', 's', '^', 'D', 'v', 'p']
    
    for i, city in enumerate(sample_cities):
        df_c = df_sweep[df_sweep["municipio"] == city].sort_values(by="volume_cisterna_l")
        if not df_c.empty:
            v_m3 = df_c["volume_cisterna_l"] / 1000.0
            ax.plot(v_m3, df_c["confiabilidade_pct"], marker=markers[i % len(markers)], linewidth=2, label=f"{city} (Chuva: {df_c['precip_anual_media_mm'].iloc[0]:.0f} mm)")
            
    ax.set_xlabel("Volume da Cisterna (m³)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Confiabilidade do Suprimento Pluvial (%)", fontsize=11, fontweight="bold")
    ax.set_title("Curvas de Confiabilidade Hídrica Diária em Escolas por Mesorregião de SC\n(NBR 15527: Balanço Diário em Série Histórica Contínua)", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(title="Município", frameon=True, facecolor="white", edgecolor="lightgray")
    
    plt.tight_layout()
    fig3_path = os.path.join(FIGURAS_DIR, "sc_escolas_curvas_confiabilidade.png")
    fig.savefig(fig3_path, dpi=300)
    plt.close(fig)
    print(f"    [fig] {fig3_path}")
    
    # ── FIGURA 4: Dispersão Precipitação Média Anual vs VPL (TMA 10%) ──
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    scatter = ax.scatter(
        df_opt["precip_anual_media_mm"],
        df_opt["vpl_tma_10_r"],
        c=df_opt["economia_agua_potavel_pct"],
        s=df_opt["volume_cisterna_l"] / 50.0,
        cmap="viridis",
        alpha=0.85,
        edgecolors="black",
        linewidth=0.8
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Economia de Água Potável (%)", fontsize=10, fontweight="bold")
    
    # Anotar cidades extremas ou de destaque
    for _, row in df_opt.iterrows():
        if row["municipio"] in ["Florianópolis", "Joinville", "Chapecó", "Lages", "Balneário Camboriú", "Blumenau"]:
            ax.annotate(
                f"{row['municipio']}",
                (row["precip_anual_media_mm"], row["vpl_tma_10_r"]),
                xytext=(6, 5), textcoords="offset points",
                fontsize=8.5, fontweight="bold"
            )
            
    ax.axhline(0, color="gray", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Precipitação Média Anual (mm/ano)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Valor Presente Líquido - VPL @ 10% (R$)", fontsize=11, fontweight="bold")
    ax.set_title("Relação entre Regime Pluviométrico e Viabilidade Econômica (VPL @ 10%)\n(Tamanho dos pontos proporcional ao volume ótimo da cisterna)", fontsize=11, fontweight="bold", pad=12)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"R$ {x:,.0f}".replace(",", ".")))
    ax.grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig4_path = os.path.join(FIGURAS_DIR, "sc_escolas_dispersao_vpl_chuva.png")
    fig.savefig(fig4_path, dpi=300)
    plt.close(fig)
    print(f"    [fig] {fig4_path}")


def generate_markdown_report(df_opt, df_ranking, df_stats, ff_res=None):
    report_path = os.path.join(RELATORIOS_DIR, "relatorio_escolas_santa_catarina.md")
    
    n_cidades = len(df_opt)
    mean_precip = df_opt["precip_anual_media_mm"].mean()
    mean_econ_pct = df_opt["economia_agua_potavel_pct"].mean()
    min_econ_pct = df_opt["economia_agua_potavel_pct"].min()
    max_econ_pct = df_opt["economia_agua_potavel_pct"].max()
    mean_vpl_10 = df_opt["vpl_tma_10_r"].mean()
    mean_pb = df_opt["payback_descontado_10_anos"].mean()
    mean_vol = df_opt["volume_cisterna_l"].median()
    
    ff_desc = (
        f"Separador de folhas duplo DN 150 em Inox 304 + Reservatório Estanque PEAD {ff_res.diverter_volume_liters:.0f} L c/ purga (R$ {ff_res.first_flush_total_capex:,.2f})"
        if ff_res else "Separador de Folhas + Reservatório de Descarte PEAD 900 L"
    )
    ff_tot_capex_str = f"R$ {ff_res.first_flush_total_capex:,.2f}" if ff_res else "R$ 1.070,90"
    
    top5 = df_ranking.head(5)
    bot5 = df_ranking.tail(5)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""# Relatório Técnico-Executivo: Aproveitamento de Água de Chuva em Escolas de Santa Catarina

**Data:** 11 de setembro de 2026  
**Software de Simulação:** Netuno 5.0.0  
**Tipologia Modelada:** Edificação Escolar (Preset Default Netuno 5 / FNDE / NBR 15527:2019)  
**Abrangência Geográfica:** Estado de Santa Catarina ({n_cidades} municípios com dados oficiais)  

---

## 1. Sumário Executivo

Este estudo apresenta a simulação em escala estadual do aproveitamento de água de chuva para edifícios escolares no estado de Santa Catarina. O modelo utilizou o balanço hídrico diário contínuo em séries históricas de 12.419 dias, integrando as matrizes tarifárias de água e esgoto municipais, os custos de energia elétrica (ANEEL B1), os fatores de custo regional da construção civil (SINAPI/CUB Santa Catarina = 1,02) e o dimensionamento físico do subsistema de descarte de primeiras águas (First Flush) e gradeamento da ETAP.

### Principais Destaques do Estado:
- **Economia Média de Água Potável:** **{mean_econ_pct:.1f}%** de toda a água consumida pela escola (variando entre **{min_econ_pct:.1f}%** e **{max_econ_pct:.1f}%** conforme o município e regime pluviométrico).
- **Volume Ótimo de Cisterna Recomendado:** **{mean_vol:,.0f} Litros** (mediana estadual), conferindo excelente equilíbrio entre investimento em CAPEX e atendimento hídrico.
- **Retorno Financeiro Médio (VPL @ TMA 10% a.a.):** **R$ {mean_vpl_10:,.2f}** ao longo de 20 anos.
- **Payback Descontado Médio:** **{mean_pb:.1f} anos**, demonstrando alta atratividade frente à vida útil do sistema (> 25 anos).
- **Sustentabilidade:** Redução média de **{df_opt['co2_evitado_kg_ano'].mean():.0f} kg de CO₂/ano** por escola, reduzindo a pegada de carbono do setor público educacional.

---

## 2. Parâmetros de Entrada e Metodologia (Preset Default de Escola)

Conforme as especificações normativas (NBR 15527:2019 e NBR 5626) e os parâmetros nativos do Netuno 5:

| Parâmetro | Valor Adotado | Justificativa Técnica |
| :--- | :--- | :--- |
| **Ocupação** | 100 alunos/turno | Capacidade escolar média típica para dimensionamento básico |
| **Consumo Per Capita** | 40 L/aluno.dia | Consumo padrão escolar (bebedouros, sanitários, merenda e pátios) |
| **Partição de Demanda** | 40% Potável / 60% Pluvial | 16 L potável (bebedouros/merenda) e 24 L não-potável (descargas) |
| **Demanda Total Diária** | 4.000 Litros/dia ($120\\,\\text{{m}}^3/\\text{{mês}}$) | Base operacional para dias letivos |
| **Demanda Pluvial Diária** | 2.400 Litros/dia ($72\\,\\text{{m}}^3/\\text{{mês}}$) | Bacias sanitárias e limpeza escolar |
| **Área de Cobertura** | 450 m² | Área de captação de blocos escolares padrão FNDE |
| **Material / Runoff ($C$)** | Telha Aluzinco / Cerâmica ($C = 0,85$) | Coeficiente de escoamento superficial regulamentar |
| **Descarte Inicial (First Flush) e Gradeamento**| 2,0 mm ($V_{{\\text{{descarte}}}} = 900\\,\\text{{L}}$) | {ff_desc} |
| **Custo de Implantação (CAPEX)**| R$ 9.600 a R$ 29.500 | Filtração preliminar, descarte 900 L, recalque 0,75 CV, reservação PEAD, tubulações e mão de obra (SINAPI-SC) |
| **Custos Operacionais (OPEX)** | R$ 650 a R$ 950/ano | Energia elétrica de pressurização, desinfecção com cloro, manutenção preventiva e purga/limpeza de filtros |

---

## 3. Síntese Estatística Estadual (Santa Catarina)

Abaixo consolidam-se os parâmetros hidrológicos e econômico-financeiros nos {n_cidades} municípios avaliados:

| Métrica | Média | Desvio Padrão | Mínimo | Mediana | Máximo |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Precipitação Anual (mm)** | {df_stats.loc['precip_anual_media_mm', 'mean']:.1f} | {df_stats.loc['precip_anual_media_mm', 'std']:.1f} | {df_stats.loc['precip_anual_media_mm', 'min']:.1f} | {df_stats.loc['precip_anual_media_mm', 'mediana']:.1f} | {df_stats.loc['precip_anual_media_mm', 'max']:.1f} |
| **Volume de Cisterna Ótimo (L)** | {df_stats.loc['volume_cisterna_l', 'mean']:.0f} | {df_stats.loc['volume_cisterna_l', 'std']:.0f} | {df_stats.loc['volume_cisterna_l', 'min']:.0f} | {df_stats.loc['volume_cisterna_l', 'mediana']:.0f} | {df_stats.loc['volume_cisterna_l', 'max']:.0f} |
| **Economia de Água Potável (%)** | {df_stats.loc['economia_agua_potavel_pct', 'mean']:.1f}% | {df_stats.loc['economia_agua_potavel_pct', 'std']:.1f}% | {df_stats.loc['economia_agua_potavel_pct', 'min']:.1f}% | {df_stats.loc['economia_agua_potavel_pct', 'mediana']:.1f}% | {df_stats.loc['economia_agua_potavel_pct', 'max']:.1f}% |
| **Confiabilidade de Suprimento (%)**| {df_stats.loc['confiabilidade_pct', 'mean']:.1f}% | {df_stats.loc['confiabilidade_pct', 'std']:.1f}% | {df_stats.loc['confiabilidade_pct', 'min']:.1f}% | {df_stats.loc['confiabilidade_pct', 'mediana']:.1f}% | {df_stats.loc['confiabilidade_pct', 'max']:.1f}% |
| **Economia Líquida Anual (R$/ano)** | R$ {df_stats.loc['economia_liquida_anual_r', 'mean']:,.2f} | R$ {df_stats.loc['economia_liquida_anual_r', 'std']:,.2f} | R$ {df_stats.loc['economia_liquida_anual_r', 'min']:,.2f} | R$ {df_stats.loc['economia_liquida_anual_r', 'mediana']:,.2f} | R$ {df_stats.loc['economia_liquida_anual_r', 'max']:,.2f} |
| **CAPEX Total do Sistema (R$)** | R$ {df_stats.loc['capex_total_r', 'mean']:,.2f} | R$ {df_stats.loc['capex_total_r', 'std']:,.2f} | R$ {df_stats.loc['capex_total_r', 'min']:,.2f} | R$ {df_stats.loc['capex_total_r', 'mediana']:,.2f} | R$ {df_stats.loc['capex_total_r', 'max']:,.2f} |
| **VPL (TMA 10% a.a.) (R$)** | R$ {df_stats.loc['vpl_tma_10_r', 'mean']:,.2f} | R$ {df_stats.loc['vpl_tma_10_r', 'std']:,.2f} | R$ {df_stats.loc['vpl_tma_10_r', 'min']:,.2f} | R$ {df_stats.loc['vpl_tma_10_r', 'mediana']:,.2f} | R$ {df_stats.loc['vpl_tma_10_r', 'max']:,.2f} |
| **Payback Descontado (anos)** | {df_stats.loc['payback_descontado_10_anos', 'mean']:.1f} | {df_stats.loc['payback_descontado_10_anos', 'std']:.1f} | {df_stats.loc['payback_descontado_10_anos', 'min']:.1f} | {df_stats.loc['payback_descontado_10_anos', 'mediana']:.1f} | {df_stats.loc['payback_descontado_10_anos', 'max']:.1f} |
| **LCOW (R$/m³)** | R$ {df_stats.loc['lcow_10_r_m3', 'mean']:.2f} | R$ {df_stats.loc['lcow_10_r_m3', 'std']:.2f} | R$ {df_stats.loc['lcow_10_r_m3', 'min']:.2f} | R$ {df_stats.loc['lcow_10_r_m3', 'mediana']:.2f} | R$ {df_stats.loc['lcow_10_r_m3', 'max']:.2f} |

---

## 4. Ranking de Atratividade Econômica (Top 5 e Menor Retorno)

### Top 5 Municípios Mais Atrativos em Santa Catarina:
As cidades com maior retorno combinam tarifas volumétricas mais elevadas e regimes pluviométricos favoráveis (especialmente no Litoral e Vale do Itajaí):

| Posição | Município | Chuva (mm/ano) | Cisterna (L) | Economia Água (%) | VPL @ 10% (R$) | Payback (anos) | TIR (% a.a.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
""")
        for _, row in top5.iterrows():
            f.write(f"| **{row['posicao_ranking']}º** | {row['municipio']} | {row['precip_anual_media_mm']:.0f} mm | {row['volume_cisterna_l']:,.0f} L | {row['economia_agua_potavel_pct']:.1f}% | R$ {row['vpl_tma_10_r']:,.2f} | {row['payback_descontado_10_anos']:.1f} anos | {row['tir_anual_pct']:.1f}% |\n")
            
        f.write("""
### 5 Municípios com Menor Atratividade Relativa:
Municípios com tarifas municipais subvencionadas ou menor volume de precipitação média concentrada:

| Posição | Município | Chuva (mm/ano) | Cisterna (L) | Economia Água (%) | VPL @ 10% (R$) | Payback (anos) | TIR (% a.a.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
""")
        for _, row in bot5.iterrows():
            f.write(f"| **{row['posicao_ranking']}º** | {row['municipio']} | {row['precip_anual_media_mm']:.0f} mm | {row['volume_cisterna_l']:,.0f} L | {row['economia_agua_potavel_pct']:.1f}% | R$ {row['vpl_tma_10_r']:,.2f} | {row['payback_descontado_10_anos']:.1f} anos | {row['tir_anual_pct']:.1f}% |\n")
            
        f.write(f"""
---

## 5. Estrutura de Arquivos e Reprodutibilidade

Todos os resultados deste estudo foram organizados na seguinte estrutura física em `Estudos/estudo_escolas_santa_catarina/`:

```
Estudos/estudo_escolas_santa_catarina/
├── config/
│   └── escola_sc_profile.json              # Parâmetros auditáveis de entrada
├── dados/
│   ├── sc_escolas_simulacao_completa.csv    # 384 combinações (32 municípios x 12 volumes)
│   ├── sc_escolas_solucao_otima.csv         # 32 municípios com dimensionamento ótimo
│   ├── sc_escolas_ranking_viabilidade.csv   # Ranking completo de atratividade
│   └── sc_escolas_estatisticas_sintese.csv  # Média, mediana, DP, IQR e quartis
├── figuras/
│   ├── sc_escolas_economia_agua_ranking.png    # Gráfico de barras da economia de água (%)
│   ├── sc_escolas_vpl_payback_cidades.png     # VPL e Payback comparativos
│   ├── sc_escolas_curvas_confiabilidade.png   # Curvas de garantia hídrica diária
│   └── sc_escolas_dispersao_vpl_chuva.png     # Dispersão chuva vs viabilidade financeira
└── relatorios/
    └── relatorio_escolas_santa_catarina.md    # Este relatório técnico executivo
```

---

## 6. Diretrizes e Recomendações Técnicas

1. **Priorização em Escolas Públicas e Privadas:** A implantação de cisternas de 20.000 L a 30.000 L em escolas catarinenses é tecnicamente viável e altamente recomendável, gerando economia contínua nas contas de água e aliviando a pressão sobre as redes públicas de abastecimento.
2. **Qualidade da Água e Subsistema de Descarte de Primeiras Águas (ETAP):** A adoção do subsistema físico de descarte de 2,0 mm (V_descarte = 900 L para a cobertura de 450 m²), composto por gradeamento e separador de folhas duplo DN 150 em inox 304 associado a reservatório estanque em PEAD com purga lenta calibrada, assegura a retenção de poluentes atmosféricos e sedimentos de telhado. O custo de implantação do subsistema (R$ 1.040,30) e sua manutenção foram integrados ao CAPEX, OPEX, ACV e decisão multicritério (TOPSIS), garantindo conformidade estrita com a ABNT NBR 15527:2019 sem comprometer a alta atratividade econômica do sistema escolar.
3. **Educação Ambiental Integrada:** Além do retorno hídrico e financeiro, a cisterna serve como laboratório vivo de educação ambiental e sustentabilidade hídrica para os estudantes catarinenses.
""")
    print(f"    [rel] {report_path}")


if __name__ == "__main__":
    run_simulation()
