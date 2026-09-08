"""
Decomposição da divergência entre o Netuno 5 e o Netuno 4.

Comparar o resultado ótimo de um programa com o do outro mistura três coisas: a
diferença do balanço hídrico, a diferença do critério que escolhe o volume ótimo e a
diferença do tratamento do descarte de primeira chuva. Uma métrica agregada sobre essa
mistura não permite dizer se o motor replica o Netuno 4.

Este módulo separa as três parcelas, comparando em três configurações sucessivamente
mais controladas:

1. **Ótimo contra ótimo.** Cada programa escolhe o próprio volume. É a comparação
   ingênua, e a única disponível antes desta apuração.
2. **No volume do Netuno 4.** O Netuno 5 é avaliado exatamente no volume que o Netuno 4
   declarou ótimo na planilha de referência. Remove a diferença de critério e de grade.
3. **No volume do Netuno 4, com descarte por limiar.** Além do volume, adota-se o
   tratamento de descarte do Netuno 4. Sobra apenas o balanço hídrico.

O que restar na terceira configuração é a diferença do modelo propriamente dito.

Emulação do descarte por limiar
-------------------------------
O Netuno 5 calcula ``Pef = max(0, Pt − df)``; o Netuno 4 usava ``Pef = Pt se Pt ≥ df``.
Para medir a segunda semântica sem alterar o motor, transforma-se a série de entrada:

    P' = Pt + df   quando Pt ≥ df
    P' = 0         caso contrário

Assim ``max(0, P' − df)`` devolve exatamente ``Pt`` nos eventos aceitos e ``0`` nos
descartados — a regra do Netuno 4, obtida sem tocar no código do balanço.
"""

from __future__ import annotations

import os
import re
import sys
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from netuno.core.parser import load_precipitation  # noqa: E402
from netuno.core.simulation import run_single_simulation  # noqa: E402


@lru_cache(maxsize=32)
def _serie_em_cache(caminho: str):
    """Série pluviométrica lida uma única vez por arquivo.

    As planilhas de referência têm milhares de linhas mas apenas seis séries distintas:
    sem cache, o mesmo CSV é relido centenas de vezes e a leitura domina o tempo de
    execução da comparação.
    """
    return load_precipitation(caminho)

SERIES_DE_CHUVA = RAIZ / "data" / "rainfall"
PLANILHA_PADRAO = (RAIZ / "data" / "simulation_outputs" /
                   "SimulacaoManausSaoPaulo" / "Planilha.csv")


@dataclass
class Metricas:
    casos: int
    mae_pp: float
    rmse_pp: float
    vies_pp: float
    fracao_ate_5pp: float

    def __str__(self) -> str:
        return (f"{self.casos} casos | MAE {self.mae_pp:.3f} pp | "
                f"RMSE {self.rmse_pp:.3f} pp | vies {self.vies_pp:+.3f} pp | "
                f"ate 5 pp em {self.fracao_ate_5pp:.1%}")


def _metricas(erros: List[float]) -> Metricas:
    vetor = np.asarray(erros, dtype=float)
    return Metricas(
        casos=len(vetor),
        mae_pp=float(np.abs(vetor).mean()),
        rmse_pp=float(np.sqrt((vetor ** 2).mean())),
        vies_pp=float(vetor.mean()),
        fracao_ate_5pp=float((np.abs(vetor) <= 5.0).mean()),
    )


def _como_limiar(precipitacao, descarte_mm: float) -> np.ndarray:
    """Transforma a série para que o motor reproduza o descarte por limiar."""
    serie = np.asarray(precipitacao, dtype=float)
    return np.where(serie >= descarte_mm, serie + descarte_mm, 0.0)


def _volume_otimo_declarado(celula) -> float | None:
    """Extrai o volume que o Netuno 4 declarou ótimo (ex.: ``Vol ideal: 1500``)."""
    correspondencia = re.search(r"(\d+)", str(celula))
    return float(correspondencia.group(1)) if correspondencia else None


def decompor(caminho_da_planilha: Path = PLANILHA_PADRAO,
             limite_de_casos: int = 0) -> Dict[str, Metricas]:
    """Mede a divergência nas três configurações. Devolve as métricas por configuração."""
    if not caminho_da_planilha.exists():
        raise FileNotFoundError(f"planilha de referência ausente: {caminho_da_planilha}")

    planilha = pd.read_csv(caminho_da_planilha, sep=";", decimal=",",
                           encoding="latin1", engine="python")
    if limite_de_casos > 0:
        planilha = planilha.head(limite_de_casos)

    erros: Dict[str, List[float]] = {"volume_do_netuno4": [], "volume_e_descarte_do_netuno4": []}

    for _, linha in planilha.iterrows():
        try:
            arquivo = str(linha.iloc[1]).strip()
            caminho_da_serie = SERIES_DE_CHUVA / arquivo
            if not caminho_da_serie.exists():
                continue

            potencial_oficial = float(linha.iloc[10])
            volume = _volume_otimo_declarado(linha.iloc[9])
            if volume is None or potencial_oficial == 0.0:
                continue

            chuva = _serie_em_cache(str(caminho_da_serie))
            descarte = float(linha.iloc[2])
            parametros = dict(
                lower_tank_vol=volume,
                area=float(linha.iloc[3]),
                runoff_coeff=float(linha.iloc[7]),
                discard_mm=descarte,
                total_demand_per_day=float(linha.iloc[4]) * int(linha.iloc[5]),
                rainwater_share=float(linha.iloc[6]) / 100.0,
            )

            com_subtracao = run_single_simulation(precip_data=chuva, **parametros)
            erros["volume_do_netuno4"].append(
                com_subtracao.potential_potable_savings_pct - potencial_oficial
            )

            com_limiar = run_single_simulation(
                precip_data=_como_limiar(chuva, descarte), **parametros
            )
            erros["volume_e_descarte_do_netuno4"].append(
                com_limiar.potential_potable_savings_pct - potencial_oficial
            )
        except Exception:
            # Linhas malformadas da planilha de referência são ignoradas, como no
            # comparador original; a contagem de casos revela se forem muitas.
            continue

    return {nome: _metricas(valores) for nome, valores in erros.items() if valores}


def main() -> int:
    from tests.benchmarking.compare_netuno4_netuno5 import run_benchmark_comparison

    print("DECOMPOSIÇÃO DA DIVERGÊNCIA NETUNO 5 vs NETUNO 4")
    print("=" * 74)

    ingenua = run_benchmark_comparison(str(PLANILHA_PADRAO))
    print(f"\n1. Ótimo do N5 contra ótimo do N4 (comparação ingênua)")
    print(f"   MAE {ingenua['mae_pct']:.3f} pp | RMSE {ingenua['rmse_pct']:.3f} pp "
          f"| {ingenua['total_compared']} casos")

    resultados = decompor()
    print(f"\n2. Avaliado no volume ótimo declarado pelo Netuno 4")
    print(f"   {resultados['volume_do_netuno4']}")
    print(f"\n3. Idem, com o descarte por limiar do Netuno 4")
    print(f"   {resultados['volume_e_descarte_do_netuno4']}")

    print("\n" + "=" * 74)
    print("O que resta na configuração 3 é a diferença do balanço hídrico em si.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
