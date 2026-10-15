"""Replica, com o Triton, o método de Geraldi e Ghisi sobre comprimento de série.

Artigo: «Assessment of the length of rainfall time series for rainwater harvesting
in buildings» (Resour. Conserv. Recycl., 2018). Parâmetros do artigo: cobertura de
100 m², descarte de 2 mm, quatro moradores, 150 L/pessoa·dia, coeficiente 0,80,
caixa superior de 600 L; volumes de 1.000 a 70.000 L; demanda pluvial de 20% a 50%.

Aqui a varredura vai até 20.000 L em passos de 1.000 L, que é onde as curvas das
quatro cidades já achataram, e a série de referência é a de 30 anos que acompanha
o programa.
"""
import json
import os
import sys

import numpy as np

RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[2])
sys.path.insert(0, RAIZ)

from triton.core.parser import load_precipitation          # noqa: E402
from triton.core.simulation import run_single_simulation   # noqa: E402

CIDADES = {"Florianópolis": "Florianopolis1", "São Paulo": "SaoPaulo1",
           "Brasília": "Brasilia1", "Manaus": "Manaus1"}
ANOS = 30
VOLUMES = list(range(1000, 20001, 1000))
FRACOES = [0.20, 0.30, 0.40, 0.50]
LIMIAR = 1.0          # %/m³, o critério de volume ideal do tutorial
TOL_POTENCIAL = 2.0   # pontos percentuais
CONFIG = dict(area=100.0, runoff_coeff=0.80, discard_mm=2.0, discard_mode=1,
              total_demand_per_day=600.0, upper_tank_vol=600.0,
              upper_tank_used=True, pumping_threshold=100.0)


def potenciais(serie, fracao):
    return [run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  rainwater_share=fracao, **CONFIG
                                  ).potential_potable_savings_pct for v in VOLUMES]


def ideal(pots):
    """Menor volume cujo ganho marginal já caiu abaixo do limiar."""
    for i in range(1, len(pots)):
        ganho = (pots[i] - pots[i - 1]) / ((VOLUMES[i] - VOLUMES[i - 1]) / 1000.0)
        if ganho <= LIMIAR:
            return VOLUMES[i]
    return VOLUMES[-1]


def main():
    saida = {}
    for nome, chave in CIDADES.items():
        serie = load_precipitation(f"{RAIZ}/data/rainfall/{chave}.csv")[: ANOS * 365]
        cidade = {}
        for fracao in FRACOES:
            referencia = potenciais(serie, fracao)
            ref_ideal = ideal(referencia)
            ref_pot = referencia[VOLUMES.index(ref_ideal)]
            por_comprimento = {}
            for anos in range(1, ANOS + 1):
                iguais = 0
                total = 0
                for inicio in range(0, ANOS - anos + 1):
                    trecho = serie[inicio * 365: (inicio + anos) * 365]
                    pots = potenciais(trecho, fracao)
                    v = ideal(pots)
                    total += 1
                    # «Semelhante» é o critério do artigo: mesmo volume ideal e
                    # potencial dentro da tolerância, no volume ideal da referência.
                    if v == ref_ideal and abs(pots[VOLUMES.index(ref_ideal)] - ref_pot) <= TOL_POTENCIAL:
                        iguais += 1
                por_comprimento[anos] = round(100.0 * iguais / total, 1)
            representativo = next((a for a in range(1, ANOS + 1)
                                   if all(por_comprimento[b] >= 90.0 for b in range(a, ANOS + 1))), None)
            cidade[f"{int(fracao * 100)}%"] = {
                "volume_ideal_30_anos": ref_ideal,
                "potencial_30_anos": round(ref_pot, 2),
                "comprimento_representativo": representativo,
                "frequencia_por_comprimento": por_comprimento,
            }
            print(f"{nome} · fração {int(fracao*100)}%: ideal {ref_ideal} L, "
                  f"potencial {ref_pot:.2f}%, série representativa "
                  f"{representativo if representativo else '>30'} anos")
        saida[nome] = cidade
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replicacao_serie.json")
    json.dump(saida, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("gravado em", destino)


if __name__ == "__main__":
    main()
