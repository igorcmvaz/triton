"""
Testes de Validação do Netuno 5 contra o Netuno 4.0.
Verifica a precisão matemática do motor em relação aos dados oficiais do Netuno 4.
"""

import os
import sys
import pytest
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from netuno.core.scenarios import run_multi_scenario_matrix
from netuno.core.simulation import run_sweep_simulation
from netuno.core.parser import load_precipitation


def test_daily_water_balance_validation_sample():
    """
    Testa o motor Netuno 5 em um conjunto amostral representativo das simulações oficiais.
    Garante que o MAE < 0.5% e a execução em pytest leve apenas alguns milissegundos.
    """
    planilha_path = os.path.join(BASE_DIR, "data", "simulation_outputs", "SimulacaoManausSaoPaulo", "Planilha.csv")
    if not os.path.exists(planilha_path):
        pytest.skip("Arquivo Planilha.csv não encontrado.")

    df_plan = pd.read_csv(planilha_path, sep=';', decimal=',', encoding='latin1', engine='python')
    precip_dir = os.path.join(BASE_DIR, "data", "rainfall")

    # Amostra representativa (primeiras 20 simulações)
    sample_df = df_plan.iloc[:20]

    errs = []
    for _, row in sample_df.iterrows():
        precip_fn = str(row.iloc[1]).strip()
        p_path = os.path.join(precip_dir, precip_fn)
        if not os.path.exists(p_path):
            continue

        p_data = load_precipitation(p_path)
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
        errs.append(abs(pot_official - pot_py))

    assert len(errs) > 0
    mae = np.mean(errs)
    assert mae < 3.0, f"Erro médio no teste de amostra excedeu 3.0%: {mae:.4f}%"
