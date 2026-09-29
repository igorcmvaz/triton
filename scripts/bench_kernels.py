"""
Mede o custo real de remover o caminho acelerado (numba) do Netuno 5.

Compara o kernel JIT e o kernel Python no MESMO processo e no mesmo hardware,
alternando simulation.HAS_NUMBA. Reporta separadamente o custo de compilacao
JIT, que o usuario paga uma vez por sessao.
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from netuno.core import simulation  # noqa: E402
from netuno.core.simulation import run_single_simulation, run_sweep_simulation  # noqa: E402

if not simulation.HAS_NUMBA:
    sys.exit("numba ausente: rode este script com o venv isolado")


def cronometrar(funcao, repeticoes: int) -> float:
    """Menor tempo observado, em segundos (o menor sofre menos ruido do SO)."""
    melhor = float("inf")
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao()
        melhor = min(melhor, time.perf_counter() - inicio)
    return melhor


def serie(n_dias: int, semente: int = 42) -> np.ndarray:
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=10.0, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


PARAMS = dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
              total_demand_per_day=600.0, rainwater_share=0.5)

print("=" * 78)
print("  CUSTO DE COMPILACAO JIT (pago uma vez por sessao)")
print("=" * 78)
simulation.HAS_NUMBA = True
chuva_curta = serie(365)
inicio = time.perf_counter()
run_single_simulation(precip_data=chuva_curta, lower_tank_vol=5000.0, **PARAMS)
compilacao_simples = time.perf_counter() - inicio
inicio = time.perf_counter()
run_single_simulation(precip_data=chuva_curta, lower_tank_vol=5000.0,
                      upper_tank_used=True, upper_tank_vol=1000.0,
                      pumping_threshold=300.0, **PARAMS)
compilacao_dupla = time.perf_counter() - inicio
print(f"  kernel de reservatorio unico : {compilacao_simples:6.2f} s")
print(f"  kernel de reservatorio duplo : {compilacao_dupla:6.2f} s")
print(f"  TOTAL na primeira simulacao  : {compilacao_simples + compilacao_dupla:6.2f} s")

print()
print("=" * 78)
print("  SIMULACAO UNICA (ja compilado)")
print("=" * 78)
print(f"  {'serie':>12}  {'JIT':>11}  {'Python':>11}  {'ganho':>9}")
print("  " + "-" * 50)
for n_dias, repeticoes in [(365, 30), (3650, 15), (10950, 8), (36500, 4)]:
    chuva = serie(n_dias)
    alvo = lambda: run_single_simulation(precip_data=chuva, lower_tank_vol=5000.0, **PARAMS)

    simulation.HAS_NUMBA = True
    alvo()  # aquecimento para este tamanho
    t_jit = cronometrar(alvo, repeticoes)

    simulation.HAS_NUMBA = False
    t_py = cronometrar(alvo, repeticoes)
    simulation.HAS_NUMBA = True

    anos = n_dias / 365
    print(f"  {anos:>8.0f} anos  {t_jit*1000:>8.1f} ms  {t_py*1000:>8.1f} ms  {t_py/t_jit:>7.1f}x")

print()
print("=" * 78)
print("  VARREDURA DE VOLUMES (uso real da interface)")
print("=" * 78)
print(f"  {'cenario':>28}  {'JIT':>11}  {'Python':>11}  {'ganho':>9}")
print("  " + "-" * 66)
for n_dias, vol_max, passo in [(3650, 10000.0, 250.0), (3650, 50000.0, 250.0), (10950, 20000.0, 100.0)]:
    chuva = serie(n_dias)
    n_pontos = int(vol_max / passo) + 1
    alvo = lambda: run_sweep_simulation(precip_data=chuva, lower_tank_max=vol_max,
                                        lower_tank_step=passo, **PARAMS)

    simulation.HAS_NUMBA = True
    alvo()
    t_jit = cronometrar(alvo, 3)

    simulation.HAS_NUMBA = False
    t_py = cronometrar(alvo, 3)
    simulation.HAS_NUMBA = True

    rotulo = f"{n_dias//365}a, {n_pontos} volumes"
    print(f"  {rotulo:>28}  {t_jit:>8.2f} s  {t_py:>8.2f} s  {t_py/t_jit:>7.1f}x")

print()
print("=" * 78)
print("  LEITURA: o ganho do JIT so compensa se o tempo do kernel Python")
print("  exceder o limiar de percepcao do usuario na varredura tipica.")
print("=" * 78)
