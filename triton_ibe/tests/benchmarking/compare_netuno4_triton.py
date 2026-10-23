"""
Módulo de Comparação Estatística e Benchmarking (Netuno 4 vs Triton).
Calcula MAE, RMSE e aderência estatística entre os resultados oficiais exportados
pelo Netuno 4 e os resultados calculados pelo motor do Triton.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from functools import lru_cache

from triton.core.parser import load_precipitation
from triton.core.simulation import run_sweep_simulation


@lru_cache(maxsize=32)
def _serie_em_cache(caminho: str):
    """Série pluviométrica lida uma única vez por arquivo.

    As planilhas de referência têm milhares de linhas mas apenas seis séries distintas:
    sem cache, o mesmo CSV é relido centenas de vezes e a leitura domina o tempo de
    execução da comparação.
    """
    return load_precipitation(caminho)


def run_benchmark_comparison(planilha_path: str, limite_de_casos: int = 0) -> Dict[str, Any]:
    """
    Lê um arquivo de planilha CSV exportado do Netuno 4 e roda as mesmas configurações no Triton,
    retornando métricas estatísticas comparativas detalhadas.

    ``limite_de_casos`` maior que zero restringe a comparação às primeiras N linhas.
    A comparação completa percorre uma varredura de volumes por caso e leva cerca de
    40 s com os kernels acelerados — e mais de dez minutos sem eles. O limite existe
    para que a suíte padrão possa verificar o arranjo de comparação sem pagar esse
    custo; a amostra é determinística, e não aleatória, para que a execução seja
    reproduzível.
    """
    if not os.path.exists(planilha_path):
        return {"status": "error", "message": f"Arquivo não encontrado: {planilha_path}"}

    df_plan = pd.read_csv(planilha_path, sep=';', decimal=',', encoding='latin1', engine='python')
    if limite_de_casos > 0:
        df_plan = df_plan.head(limite_de_casos)
    precip_dir = os.path.join(BASE_DIR, "data", "rainfall")

    results_comparison = []
    errs_pot = []
    
    for idx, row in df_plan.iterrows():
        try:
            precip_fn = str(row.iloc[1]).strip()
            p_path = os.path.join(precip_dir, precip_fn)
            if not os.path.exists(p_path):
                continue

            p_data = _serie_em_cache(p_path)
            discard_mm = float(row.iloc[2])
            area = float(row.iloc[3])
            demand_capita = float(row.iloc[4])
            residents = int(row.iloc[5])
            share_pct = float(row.iloc[6])
            runoff = float(row.iloc[7])
            pot_official = float(row.iloc[10])

            tot_demand = demand_capita * residents
            rainwater_share = share_pct / 100.0

            sw_res = run_sweep_simulation(
                precip_data=p_data,
                lower_tank_max=10000.0,
                lower_tank_step=500.0,
                area=area,
                runoff_coeff=runoff,
                discard_mm=discard_mm,
                total_demand_per_day=tot_demand,
                rainwater_share=rainwater_share,
                upper_tank_vol=0.0,
                upper_tank_used=False,
                pumping_threshold=0.0,
                delta_ideal_threshold=2.0,
                store_daily_details=False
            )

            pot_py = sw_res.optimal_potential_pct if sw_res.optimal_potential_pct is not None else 0.0
            diff = abs(pot_official - pot_py)
            errs_pot.append(diff)

            results_comparison.append({
                "row_idx": idx + 1,
                "file": precip_fn,
                "area": area,
                "demand": tot_demand,
                "pot_netuno4": pot_official,
                "pot_triton": pot_py,
                "diff_abs": diff
            })
        except Exception as e:
            continue

    if not errs_pot:
        return {"status": "empty", "message": "Nenhum resultado válido para comparar."}

    mae = float(np.mean(errs_pot))
    rmse = float(np.sqrt(np.mean(np.square(errs_pot))))
    max_err = float(np.max(errs_pot))

    return {
        "status": "success",
        "total_compared": len(errs_pot),
        "mae_pct": mae,
        "rmse_pct": rmse,
        "max_error_pct": max_err,
        "details": results_comparison
    }


if __name__ == "__main__":
    sample_plan = os.path.join(BASE_DIR, "data", "simulation_outputs", "SimulacaoManausSaoPaulo", "Planilha.csv")
    res = run_benchmark_comparison(sample_plan)
    print("Resultado do Benchmarking Netuno 4 vs Triton:")
    print(f"   - Total de Casos: {res.get('total_compared')}")
    print(f"   - MAE (Erro Médio Absoluto): {res.get('mae_pct'):.4f}%")
    print(f"   - RMSE (Raiz do Erro Quadrático Médio): {res.get('rmse_pct'):.4f}%")
    print(f"   - Erro Máximo: {res.get('max_error_pct'):.4f}%")
