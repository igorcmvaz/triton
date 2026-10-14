"""Exercício de regressão em lote do motor Triton.

Executa matrizes fatoriais derivadas de planilhas de trabalho, quando elas
estão disponíveis. Conclusão sem exceções verifica execução/cobertura, mas não
compara automaticamente cada saída com o Netuno 4 e não é validação externa.
"""

import os
import sys
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from triton.core.scenarios import run_multi_scenario_matrix


def run_full_validation():
    print("=" * 95)
    print("TRITON 5 - EXERCÍCIO DE REGRESSÃO DE CENÁRIOS EM LOTE")
    print("=" * 95)

    precip_dir = os.path.join(BASE_DIR, "data", "rainfall")
    
    # 1. Validação Lote 1 (Florianópolis & Brasília - 1.458 cenários)
    planilha1 = os.path.join(BASE_DIR, "data", "simulation_outputs", "SimulacaoFloripaBrasilia", "Planilha.csv")
    if not os.path.exists(planilha1):
        planilha1 = os.path.join(BASE_DIR, "data", "simulation_outputs", "Planilha.csv")

    if os.path.exists(planilha1):
        df1 = pd.read_csv(planilha1, sep=';', decimal=',', encoding='latin1', engine='python')
        u_files1 = [(fn, os.path.join(precip_dir, fn)) for fn in df1.iloc[:, 1].unique() if os.path.exists(os.path.join(precip_dir, fn))]
        
        m_res1 = run_multi_scenario_matrix(
            precip_files=u_files1,
            areas=sorted(list(df1.iloc[:, 3].unique())),
            residents_list=sorted(list(df1.iloc[:, 5].unique())),
            demands_per_capita=sorted(list(df1.iloc[:, 4].unique())),
            # A planilha do Netuno 4 traz a substituição em percentual.
            rainwater_shares=[float(s) / 100.0 for s in sorted(df1.iloc[:, 6].unique())],
            lower_tanks=[5000.0],
            runoff_coeffs=sorted(list(df1.iloc[:, 7].unique())),
            upper_tank_vol=0.0,
            upper_tank_used=False,
            pumping_threshold=0.0,
            discard_mm=2.0,
            delta_ideal=2.0,
            run_as_sweeps=True,
            sweep_step=500.0,
            parallel=True
        )
        print(f"[LOTE 1 - Floripa & Brasília]: {m_res1.total_scenarios_run} simulações concluídas no core.")

    # 2. Validação Lote 2 (Manaus & São Paulo - 2.592 cenários)
    planilha2 = os.path.join(BASE_DIR, "data", "simulation_outputs", "SimulacaoManausSaoPaulo", "Planilha.csv")
    if os.path.exists(planilha2):
        df2 = pd.read_csv(planilha2, sep=';', decimal=',', encoding='latin1', engine='python')
        u_files2 = [(fn, os.path.join(precip_dir, fn)) for fn in df2.iloc[:, 1].unique() if os.path.exists(os.path.join(precip_dir, fn))]
        
        m_res2 = run_multi_scenario_matrix(
            precip_files=u_files2,
            areas=sorted(list(df2.iloc[:, 3].unique())),
            residents_list=sorted(list(df2.iloc[:, 5].unique())),
            demands_per_capita=sorted(list(df2.iloc[:, 4].unique())),
            rainwater_shares=[float(s) / 100.0 for s in sorted(df2.iloc[:, 6].unique())],
            lower_tanks=[10000.0],
            runoff_coeffs=sorted(list(df2.iloc[:, 7].unique())),
            upper_tank_vol=0.0,
            upper_tank_used=False,
            pumping_threshold=0.0,
            discard_mm=1.0,
            delta_ideal=2.0,
            run_as_sweeps=True,
            sweep_step=500.0,
            parallel=True
        )
        print(f"[LOTE 2 - Manaus & São Paulo]: {m_res2.total_scenarios_run} simulações concluídas no core.")

    print("=" * 95)
    print("MATRIZES DISPONÍVEIS EXECUTADAS SEM ERROS; NENHUMA VALIDAÇÃO EXTERNA É INFERIDA.")
    print("=" * 95)

if __name__ == "__main__":
    run_full_validation()
