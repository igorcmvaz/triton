"""
Módulo Gerador de Projetos em Lote para Benchmarking Netuno 4 vs Triton.
Gera combinações variadas de séries climatológicas, geometrias de telhado,
ocupação e demandas para alimentar simulações de referência no Netuno 4.
"""

import os
import sys
import argparse
import random
import pandas as pd
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAINFALL_DIR = os.path.join(BASE_DIR, "data", "rainfall")


def generate_benchmark_scenarios(count: int = 20, seed: int = 42) -> List[Dict[str, Any]]:
    """
    Gera uma lista de cenários combinatórios aleatórios, porém reprodutíveis.
    """
    random.seed(seed)
    
    rain_files = [f for f in os.listdir(RAINFALL_DIR) if f.endswith(".csv")]
    if not rain_files:
        rain_files = ["Florianopolis1.csv", "Brasilia1.csv", "Manaus1.csv", "SaoPaulo1.csv"]

    areas = [30.0, 50.0, 80.0, 100.0, 150.0, 200.0, 300.0, 500.0]
    demands = [80.0, 100.0, 120.0, 150.0, 180.0, 200.0, 250.0]
    residents = [1, 2, 3, 4, 5, 6, 8, 10]
    shares = [30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    runoffs = [0.70, 0.73, 0.75, 0.85, 0.88, 0.90, 0.92, 0.94]
    discards = [0.0, 1.0, 2.0, 3.0, 5.0]
    discard_modes = [1, 2, 3]
    discard_days_list = [7, 14, 30]

    scenarios = []
    for i in range(1, count + 1):
        scen = {
            "id": f"BENCH_{i:03d}",
            "rain_file": random.choice(rain_files),
            "area_m2": random.choice(areas),
            "demand_l_hab_day": random.choice(demands),
            "residents": random.choice(residents),
            "rainwater_share_pct": random.choice(shares),
            "runoff_coeff": random.choice(runoffs),
            "discard_mm": random.choice(discards),
            "discard_mode": random.choice(discard_modes),
            "discard_days": random.choice(discard_days_list),
            "lower_tank_max_l": 10000.0,
            "lower_tank_step_l": 500.0,
            "upper_tank_vol_l": 1000.0 if random.random() > 0.5 else 0.0,
            "upper_tank_used": random.choice([True, False]),
            "pumping_threshold_pct": 20.0,
            "delta_ideal_threshold": 2.0
        }
        scenarios.append(scen)
        
    return scenarios


def export_scenarios_to_csv(scenarios: List[Dict[str, Any]], output_file: str):
    """
    Salva os cenários em formato CSV legível.
    """
    df = pd.DataFrame(scenarios)
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False, sep=";", decimal=",", encoding="utf-8-sig")
    print(f"[ok] {len(scenarios)} cenários de teste exportados para: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Projetos para Benchmarking Netuno 4 vs 5")
    parser.add_argument("--count", type=int, default=30, help="Número de cenários a gerar")
    parser.add_argument("--output", type=str, default=os.path.join(BASE_DIR, "data", "benchmark_scenarios.csv"), help="Caminho do CSV de saída")
    args = parser.parse_args()

    scens = generate_benchmark_scenarios(count=args.count)
    export_scenarios_to_csv(scens, args.output)
