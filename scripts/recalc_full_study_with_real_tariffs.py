"""
=======================================================================================================
NETUNO 5 -- RECÁLCULO INTEGRAL DO ESTUDO DE 5 TIPOLOGIAS COM MODELO CALIBRADO E REGIONALIZADO (652 CIDADES)
=======================================================================================================
Processa em lote os 39.022.200 registros de simulação do CMIP6, casando cada cidade com:
- Estrutura tarifária oficial de água (faixas e tarifas mínimas)
- Alíquota regulatória de esgoto (% sobre água)
- Tarifa de energia elétrica B1 residencial ANEEL (R$/kWh)
- CAPEX Calibrado para os 8 Subsistemas Prediais (Bombas 1+1, Painel, Sensores, Air Gap NBR 5626, Prumadas)
- Fator Regional de CAPEX SINAPI/CUB por UF (27 UFs)
- OPEX Modular (Manutenção Predial por Tipologia/UF + Energia B1 ANEEL + Desinfecção Cloro)

Recalcula:
- Economia anual na conta de água/esgoto (R$)
- CAPEX Total Calibrado (R$)
- Custo de OPEX Real (R$/ano)
- VPL em 20 anos, TIR anual (%) e Payback (anos)
- Ranqueamento Multicritério TOPSIS (Scores, Ranks e Seleção de Ótimo)
- Colunas de metadados tarifários, de engenharia e geográficos
=======================================================================================================
"""

import os
import sys
import time
import math
import re
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from netuno.core.cost_estimates import (
    estimate_calibrated_capex_opex,
    REGIONAL_FACTORS_BY_UF,
    TYPOLOGY_COST_CONFIGS
)

STUDY_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais")
CSV_TARIFAS = os.path.join(BASE_DIR, "tarifas", "tarifas_detalhadas_auditadas.csv")
PARQUET_IN = os.path.join(STUDY_DIR, "estudo_vaz", "estudo_vaz_consolidado.parquet")
PARQUET_OUT_TEMP = os.path.join(STUDY_DIR, "estudo_vaz", "estudo_vaz_consolidado_updated.parquet")
PARQUET_FINAL = os.path.join(STUDY_DIR, "estudo_vaz", "estudo_vaz_consolidado.parquet")


TYPOLOGY_UNITS = {
    "UTI": 1,
    "UTG": 2,
    "MSG": 4,
    "MFH": 16,
    "MFL": 32
}


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


def build_capex_opex_lookup():
    """Pré-computa dicionário (tipologia, volume, UF) -> (capex, opex_fixo)."""
    print(" [*] Pré-computando matriz de CAPEX e Manutenção Calibrada por Tipologia e UF...")
    lookup = {}
    volumes = [500.0, 1000.0, 2000.0, 3000.0, 5000.0, 7500.0, 10000.0, 15000.0, 20000.0, 30000.0, 40000.0, 50000.0]
    typologies = ["UTI", "UTG", "MSG", "MFH", "MFL"]
    ufs = list(REGIONAL_FACTORS_BY_UF.keys())
    
    for uf in ufs:
        for typ in typologies:
            for vol in volumes:
                res = estimate_calibrated_capex_opex(typology=typ, volume_l=vol, uf=uf, detailed_breakdown=False)
                lookup[(typ, float(vol), uf)] = (float(res["capex_total_brl"]), float(res["opex_fixed_annual_brl"]))
    print(f" [OK] Matriz com {len(lookup)} combinações de CAPEX/OPEX gerada com sucesso.")
    return lookup


def recompute_topsis(v_sav, v_vpl, v_co2, v_full, v_cpx, n_vols=12):
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
    
    order = np.argsort(-scores, axis=1)
    ranks = np.empty_like(scores, dtype=np.int16)
    np.put_along_axis(ranks, order, np.arange(1, n_vols + 1, dtype=np.int16)[None, :], axis=1)
    is_best = np.zeros_like(scores, dtype=bool)
    best_idx = np.argmax(scores, axis=1)
    np.put_along_axis(is_best, best_idx[:, None], True, axis=1)
        
    return scores.flatten(), ranks.flatten(), is_best.flatten()


def run_full_recalc():
    import gc
    import psutil
    import shutil
    proc = psutil.Process()

    print("=" * 95)
    print("NETUNO 5 -- INICIANDO RECÁLCULO INTEGRAL DAS 39 MILHÕES DE SIMULAÇÕES")
    print("           (CAPEX CALIBRADO POR SUBSISTEMAS + SINAPI/CUB POR UF + TARIFAS AUDITADAS)")
    print("=" * 95)
    
    t_start_total = time.time()
    city_tariffs = load_tariff_dictionary()
    capex_lookup = build_capex_opex_lookup()
    fallback_city_key = list(city_tariffs.keys())[0]
    default_info = city_tariffs[fallback_city_key]

    # Estruturas de mapeamento rápido e matrizes pré-computadas
    RESIDENTS_TO_TYP_IDX = np.zeros(129, dtype=np.int32)
    RESIDENTS_TO_UNITS = np.zeros(129, dtype=np.float64)
    for r, idx, u in [(4, 0, 1.0), (8, 1, 2.0), (16, 2, 4.0), (64, 3, 16.0), (128, 4, 32.0)]:
        RESIDENTS_TO_TYP_IDX[r] = idx
        RESIDENTS_TO_UNITS[r] = u

    VOL_LIST = np.array([500.0, 1000.0, 2000.0, 3000.0, 5000.0, 7500.0, 10000.0, 15000.0, 20000.0, 30000.0, 40000.0, 50000.0])
    UF_LIST = list(sorted(set(info['uf'] for info in city_tariffs.values())))
    UF_TO_IDX = {uf: i for i, uf in enumerate(UF_LIST)}
    typ_names = ['UTI', 'UTG', 'MSG', 'MFH', 'MFL']

    capex_matrices = np.zeros((len(UF_LIST), 5, 12), dtype=np.float64)
    maint_matrices = np.zeros((len(UF_LIST), 5, 12), dtype=np.float64)
    for uf_i, uf in enumerate(UF_LIST):
        for typ_i, typ in enumerate(typ_names):
            for vol_i, vol in enumerate(VOL_LIST):
                cpx, mnt = capex_lookup.get((typ, float(vol), uf), (6500.0, 420.0))
                capex_matrices[uf_i, typ_i, vol_i] = cpx
                maint_matrices[uf_i, typ_i, vol_i] = mnt
    
    if os.path.exists(PARQUET_OUT_TEMP):
        try:
            os.remove(PARQUET_OUT_TEMP)
            print(f" [*] Arquivo temporário anterior removido: {PARQUET_OUT_TEMP}")
        except Exception as e:
            print(f" [!] Aviso ao limpar temporário: {e}")
            
    pf = pq.ParquetFile(PARQUET_IN)
    schema = pf.schema_arrow
    total_rows = pf.metadata.num_rows
    num_row_groups = pf.num_row_groups
    print(f" [*] Arquivo Parquet de Entrada: {PARQUET_IN}")
    print(f" [*] Total de registros: {total_rows:,} distribuídos em {num_row_groups} row groups.")
    
    writer = pq.ParquetWriter(PARQUET_OUT_TEMP, schema, compression='snappy')
    processed_count = 0
    
    pv_factor_6 = (1.0 - (1.0 + 0.06)**(-20)) / 0.06
    pv_factor_10 = (1.0 - (1.0 + 0.10)**(-20)) / 0.10
    pv_factor_14 = (1.0 - (1.0 + 0.14)**(-20)) / 0.14
    
    for rg_idx in range(num_row_groups):
        t_rg_start = time.time()
        rg = pf.read_row_group(rg_idx)
        n_df = rg.num_rows

        residents = rg.column('residents').to_numpy()
        tot_dem = rg.column('total_demand_l_day').to_numpy()
        avg_pot = rg.column('avg_potable_consumed_l_day').to_numpy()
        ann_pluv = rg.column('annual_pluvial_consumed_m3').to_numpy()
        tank_vol = rg.column('lower_tank_vol_l').to_numpy()
        sav_pct = rg.column('potential_water_savings_pct').to_numpy() if 'potential_water_savings_pct' in rg.column_names else (
            rg.column('potential_savings_pct').to_numpy() if 'potential_savings_pct' in rg.column_names else np.zeros(n_df, dtype=np.float64)
        )
        full_pct = rg.column('reliability_fully_met_pct').to_numpy() if 'reliability_fully_met_pct' in rg.column_names else (
            rg.column('fully_met_pct').to_numpy() if 'fully_met_pct' in rg.column_names else np.zeros(n_df, dtype=np.float64)
        )
        co2_val = rg.column('lifetime_net_co2_saved_kg').to_numpy() if 'lifetime_net_co2_saved_kg' in rg.column_names else (ann_pluv * 7.0)

        typ_idx = RESIDENTS_TO_TYP_IDX[residents]
        sub_units = RESIDENTS_TO_UNITS[residents]
        vol_idx = np.searchsorted(VOL_LIST, tank_vol)

        unique_cities = rg.column('city').unique().to_pylist()
        if len(unique_cities) == 1:
            c_clean = str(unique_cities[0]).strip()
            info = city_tariffs.get(c_clean, default_info)
            uf_idx = UF_TO_IDX[info['uf']]
            elec_rate = info['elec_tariff']
            base_w_rate = info['base_water_rate']
            sew_rate = info['sewage_rate']
            tariffs = info['tariffs']
            
            capex_calibrated = capex_matrices[uf_idx, typ_idx, vol_idx]
            maint_fixed = maint_matrices[uf_idx, typ_idx, vol_idx]
            
            monthly_tot_m3 = (tot_dem * 30.4375) / (sub_units * 1000.0)
            monthly_pot_m3 = (avg_pot * 30.4375) / (sub_units * 1000.0)
            sew_mult = 1.0 + (sew_rate / 100.0)
            
            c_without = np.zeros(n_df, dtype=np.float64)
            c_with = np.zeros(n_df, dtype=np.float64)
            for min_v, max_v, rate, is_fix in tariffs:
                if is_fix == -1:
                    c_without += rate
                    c_with += rate
                else:
                    c_without += np.maximum(0.0, np.minimum(monthly_tot_m3, max_v) - min_v) * rate
                    c_with += np.maximum(0.0, np.minimum(monthly_pot_m3, max_v) - min_v) * rate
            c_without *= (sew_mult * sub_units)
            c_with *= (sew_mult * sub_units)
            annual_water_savings = np.maximum(0.0, c_without - c_with) * 12.0
            
            sub_pump_kwh = ann_pluv * 0.45
            annual_opex = (sub_pump_kwh * elec_rate) + (ann_pluv * 0.05) + maint_fixed
            
            pa_elec = pa.repeat(pa.scalar(elec_rate, type=pa.float64()), n_df)
            pa_base_w = pa.repeat(pa.scalar(base_w_rate, type=pa.float64()), n_df)
            pa_esgoto = pa.repeat(pa.scalar(sew_rate, type=pa.float64()), n_df)
            pa_prestador = pa.repeat(pa.scalar(info['prestador'], type=pa.string()), n_df)
            pa_uf = pa.repeat(pa.scalar(info['uf'], type=pa.string()), n_df)
            pa_regiao = pa.repeat(pa.scalar(info['regiao'], type=pa.string()), n_df)
        else:
            annual_water_savings = np.zeros(n_df, dtype=np.float64)
            annual_opex = np.zeros(n_df, dtype=np.float64)
            capex_calibrated = np.zeros(n_df, dtype=np.float64)
            elec_arr = np.zeros(n_df, dtype=np.float64)
            base_w_arr = np.zeros(n_df, dtype=np.float64)
            esgoto_arr = np.zeros(n_df, dtype=np.float64)
            prestador_list = [None] * n_df
            uf_list = [None] * n_df
            regiao_list = [None] * n_df
            
            city_col_pylist = rg.column('city').to_pylist()
            city_series = np.array(city_col_pylist)
            
            for c_raw in unique_cities:
                c_clean = str(c_raw).strip()
                info = city_tariffs.get(c_clean, default_info)
                uf_idx = UF_TO_IDX[info['uf']]
                elec_rate = info['elec_tariff']
                base_w_rate = info['base_water_rate']
                sew_rate = info['sewage_rate']
                tariffs = info['tariffs']
                prest = info['prestador']
                uf_str = info['uf']
                reg_str = info['regiao']
                
                mask = (city_series == c_raw)
                idx_where = np.where(mask)[0]
                n_mask = len(idx_where)
                if n_mask == 0:
                    continue
                    
                m_typ_idx = typ_idx[mask]
                m_vol_idx = vol_idx[mask]
                m_sub_units = sub_units[mask]
                m_tot_dem = tot_dem[mask]
                m_avg_pot = avg_pot[mask]
                m_ann_pluv = ann_pluv[mask]
                
                m_cpx = capex_matrices[uf_idx, m_typ_idx, m_vol_idx]
                m_maint = maint_matrices[uf_idx, m_typ_idx, m_vol_idx]
                capex_calibrated[mask] = m_cpx
                
                m_tot_m3 = (m_tot_dem * 30.4375) / (m_sub_units * 1000.0)
                m_pot_m3 = (m_avg_pot * 30.4375) / (m_sub_units * 1000.0)
                m_sew_mult = 1.0 + (sew_rate / 100.0)
                
                m_c_without = np.zeros(n_mask, dtype=np.float64)
                m_c_with = np.zeros(n_mask, dtype=np.float64)
                for min_v, max_v, rate, is_fix in tariffs:
                    if is_fix == -1:
                        m_c_without += rate
                        m_c_with += rate
                    else:
                        m_c_without += np.maximum(0.0, np.minimum(m_tot_m3, max_v) - min_v) * rate
                        m_c_with += np.maximum(0.0, np.minimum(m_pot_m3, max_v) - min_v) * rate
                m_c_without *= (m_sew_mult * m_sub_units)
                m_c_with *= (m_sew_mult * m_sub_units)
                annual_water_savings[mask] = np.maximum(0.0, m_c_without - m_c_with) * 12.0
                
                m_pump_kwh = m_ann_pluv * 0.45
                annual_opex[mask] = (m_pump_kwh * elec_rate) + (m_ann_pluv * 0.05) + m_maint
                
                elec_arr[mask] = elec_rate
                base_w_arr[mask] = base_w_rate
                esgoto_arr[mask] = sew_rate
                for i_pos in idx_where:
                    prestador_list[i_pos] = prest
                    uf_list[i_pos] = uf_str
                    regiao_list[i_pos] = reg_str
                    
            pa_elec = pa.array(elec_arr, type=pa.float64())
            pa_base_w = pa.array(base_w_arr, type=pa.float64())
            pa_esgoto = pa.array(esgoto_arr, type=pa.float64())
            pa_prestador = pa.array(prestador_list, type=pa.string())
            pa_uf = pa.array(uf_list, type=pa.string())
            pa_regiao = pa.array(regiao_list, type=pa.string())

        # VPL, TIR, Payback e LCOW
        net_annual = annual_water_savings - annual_opex
        vpl_6 = -capex_calibrated + (net_annual * pv_factor_6)
        vpl_10 = -capex_calibrated + (net_annual * pv_factor_10)
        vpl_14 = -capex_calibrated + (net_annual * pv_factor_14)
        
        payback = np.where(net_annual > 0, capex_calibrated / net_annual, 99.0)
        tir = np.where(capex_calibrated > 0, (net_annual / capex_calibrated) * 100.0, 0.0)
        denom_lcow = np.maximum(0.001, ann_pluv * pv_factor_6)
        lcow = (capex_calibrated + (annual_opex * pv_factor_6)) / denom_lcow
        
        # TOPSIS
        n_vols = 12 if (n_df % 12 == 0) else (10 if (n_df % 10 == 0) else 12)
        t_score, t_rank, t_is_best = recompute_topsis(
            sav_pct,
            vpl_6,
            co2_val,
            full_pct,
            capex_calibrated,
            n_vols=n_vols
        )
        
        # Mapeamento de colunas atualizadas
        col_replacements = {
            'capex_total_brl': pa.array(capex_calibrated, type=pa.float64()),
            'annual_water_savings_brl': pa.array(annual_water_savings, type=pa.float64()),
            'annual_opex_brl': pa.array(annual_opex, type=pa.float64()),
            'vpl_6pct_brl': pa.array(vpl_6, type=pa.float64()),
            'vpl_10pct_brl': pa.array(vpl_10, type=pa.float64()),
            'vpl_14pct_brl': pa.array(vpl_14, type=pa.float64()),
            'vpl_brl': pa.array(vpl_6, type=pa.float64()),
            'lcow_brl_m3': pa.array(lcow, type=pa.float64()),
            'lcow_r_per_m3': pa.array(lcow, type=pa.float64()),
            'payback_years': pa.array(payback, type=pa.float64()),
            'tir_pct_yr': pa.array(tir, type=pa.float64()),
            'tir_annual_pct': pa.array(tir, type=pa.float64()),
            'topsis_score': pa.array(t_score, type=pa.float64()),
            'topsis_rank': pa.array(t_rank, type=pa.int16()),
            'is_topsis_best': pa.array(t_is_best, type=pa.bool_()),
            'tarifa_eletricidade_b1_r_kwh': pa_elec,
            'tarifa_agua_base_r_m3': pa_base_w,
            'esgoto_pct_sobre_agua': pa_esgoto,
            'saneamento_prestador': pa_prestador,
            'uf': pa_uf,
            'regiao': pa_regiao,
        }
        
        new_cols = [col_replacements.get(name, rg.column(i)) for i, name in enumerate(rg.column_names)]
        out_table = pa.Table.from_arrays(new_cols, schema=schema)
        writer.write_table(out_table)
        processed_count += n_df
        
        del rg, out_table, new_cols, col_replacements
        del residents, tot_dem, avg_pot, ann_pluv, tank_vol, sav_pct, full_pct, co2_val
        del capex_calibrated, annual_water_savings, annual_opex, net_annual, vpl_6, vpl_10, vpl_14, payback, tir, lcow, t_score, t_rank, t_is_best
        del pa_elec, pa_base_w, pa_esgoto, pa_prestador, pa_uf, pa_regiao
        
        if (rg_idx + 1) % 25 == 0 or rg_idx == num_row_groups - 1:
            gc.collect()
            pa.default_memory_pool().release_unused()
            
        elapsed_rg = time.time() - t_rg_start
        pct_done = (processed_count / total_rows) * 100.0
        rss_mb = proc.memory_info().rss / 1024 / 1024
        if (rg_idx + 1) % 10 == 0 or rg_idx == num_row_groups - 1 or rg_idx < 5:
            print(f"  [>] Row Group {rg_idx+1}/{num_row_groups} ({n_df:,} linhas) concluído em {elapsed_rg:.2f}s | Progresso: {processed_count:,}/{total_rows:,} ({pct_done:.1f}%) | RAM: {rss_mb:.1f} MB", flush=True)
        
    writer.close()
    del writer
    del pf
    gc.collect()
    pa.default_memory_pool().release_unused()
    time.sleep(1.0)
    
    print(" [*] Substituindo arquivo Parquet antigo pelo Parquet atualizado...")
    if os.path.exists(PARQUET_FINAL):
        try:
            os.remove(PARQUET_FINAL)
        except Exception:
            time.sleep(1.5)
            gc.collect()
            try:
                os.remove(PARQUET_FINAL)
            except Exception as e:
                print(f" [!] Erro ao remover Parquet antigo: {e}")
                
    shutil.move(PARQUET_OUT_TEMP, PARQUET_FINAL)
    
    total_sec = time.time() - t_start_total
    print("=" * 95)
    print(f"[OK] RECÁLCULO TOTAL CONCLUÍDO COM SUCESSO EM {total_sec/60.0:.2f} MINUTOS ({total_sec:.1f}s)!")
    print(f"[*] Registros gravados no Parquet final: {processed_count:,}")
    print(f"[*] Tamanho do Parquet final: {os.path.getsize(PARQUET_FINAL)/(1024*1024*1024):.2f} GB")
    print("=" * 95)


if __name__ == '__main__':
    run_full_recalc()

