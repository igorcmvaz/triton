"""
Compara uma exportação de varredura do Netuno 4 com o motor do Netuno 5.

Por que esta comparação é mais forte que a da `Planilha.csv`
------------------------------------------------------------
A `Planilha.csv` da matriz de cenários traz **um** número por caso: o potencial de
economia no volume ótimo. A exportação de varredura do Netuno 4 traz **seis saídas por
volume simulado**:

    Volume | Potencial de economia | Consumo pluvial | Consumo potável
           | Extravasamento | % dias atendidos plenamente / parcialmente / não atendidos

Cada uma corresponde a um campo de `SingleTankSimulationResult`. Verificar as seis, em
toda a grade de volumes, exercita o balanço diário muito além do indicador agregado — em
particular o **extravasamento** e a **estatística de atendimento**, que a comparação
anterior não alcançava.

Semântica do descarte
---------------------
O manual do Netuno 4 (junho/2014, seção 3.1) define o descarte como limiar:

    «Caso a precipitação em um dado dia esteja abaixo desse valor, o Netuno considerará
    que não houve precipitação.»

O Netuno 5 subtrai a lâmina. São regras distintas e deliberadas (ver
`docs/metodologia.md` §1). Por isso a comparação oferece `--descarte-como-limiar`, que
emula a regra do Netuno 4 transformando a série de entrada, sem alterar o motor. Use-a
para isolar o balanço hídrico; omita-a para medir a diferença total entre os programas.

Uso
---
    python scripts/comparar_exportacao_netuno4.py EXPORTACAO.csv \\
        --serie Florianopolis2.csv --area 100 --demanda 100 --moradores 4 \\
        --percentual 90 --coeficiente 0.8 --descarte 2 --descarte-como-limiar
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from netuno.core.parser import load_precipitation  # noqa: E402
from netuno.core.simulation import run_single_simulation  # noqa: E402

SERIES = RAIZ / "data" / "rainfall"

#: Colunas da exportação do Netuno 4, na ordem, e o campo equivalente no Netuno 5.
#: A correspondência é posicional porque os cabeçalhos do Netuno 4 contêm quebras de
#: linha e espaçamento irregular, que variam entre versões.
CORRESPONDENCIA = [
    (1, "potential_potable_savings_pct", "potencial de economia (%)", "pp"),
    (2, "avg_pluvial_consumed_l_day", "consumo pluvial (L/dia)", "L/dia"),
    (3, "avg_potable_consumed_l_day", "consumo potável (L/dia)", "L/dia"),
    (4, "avg_spilled_l_day", "extravasamento (L/dia)", "L/dia"),
    (5, "pct_days_full_satisfaction", "dias com atendimento pleno (%)", "pp"),
    (6, "pct_days_partial_satisfaction", "dias com atendimento parcial (%)", "pp"),
    (7, "pct_days_null_satisfaction", "dias sem atendimento (%)", "pp"),
]


def como_limiar(precipitacao, descarte_mm: float) -> np.ndarray:
    """Emula a regra de descarte do Netuno 4 sem alterar o motor do Netuno 5.

    O Netuno 5 calcula ``max(0, Pt − df)``. Com ``P' = Pt + df`` nos eventos aceitos e
    ``0`` nos descartados, ``max(0, P' − df)`` devolve exatamente ``Pt`` ou ``0``, que é
    a regra de limiar do Netuno 4.
    """
    serie = np.asarray(precipitacao, dtype=float)
    return np.where(serie >= descarte_mm, serie + descarte_mm, 0.0)


def comparar(exportacao: Path, serie: str, area: float, demanda_per_capita: float,
             moradores: int, percentual: float, coeficiente: float, descarte: float,
             usar_limiar: bool, reservatorio_superior: float, limiar_recalque: float):
    tabela = pd.read_csv(exportacao, sep=";", decimal=",", encoding="latin1",
                         engine="python")
    caminho_da_serie = SERIES / serie
    if not caminho_da_serie.exists():
        raise SystemExit(f"série pluviométrica não encontrada: {caminho_da_serie}")

    chuva = load_precipitation(str(caminho_da_serie))
    if usar_limiar:
        chuva = como_limiar(chuva, descarte)

    parametros = dict(
        precip_data=chuva, area=area, runoff_coeff=coeficiente, discard_mm=descarte,
        total_demand_per_day=demanda_per_capita * moradores,
        rainwater_share=percentual / 100.0,
        upper_tank_used=reservatorio_superior > 0,
        upper_tank_vol=reservatorio_superior,
        pumping_threshold=limiar_recalque,
    )

    erros = {campo: [] for _, campo, _, _ in CORRESPONDENCIA}
    volumes = []

    for _, linha in tabela.iterrows():
        try:
            volume = float(linha.iloc[0])
        except (TypeError, ValueError):
            continue
        resultado = run_single_simulation(lower_tank_vol=volume, **parametros)
        volumes.append(volume)
        for indice, campo, _, _ in CORRESPONDENCIA:
            referencia = float(linha.iloc[indice])
            erros[campo].append(getattr(resultado, campo) - referencia)

    if not volumes:
        raise SystemExit("nenhuma linha de volume pôde ser lida da exportação")

    regra = "limiar (como o Netuno 4)" if usar_limiar else "subtração (Netuno 5)"
    print(f"\n{exportacao.name}")
    print(f"  série {serie} | área {area:g} m² | demanda {demanda_per_capita:g} L/hab·dia "
          f"× {moradores} | {percentual:g}% pluvial | C={coeficiente:g} | "
          f"descarte {descarte:g} mm ({regra})")
    if reservatorio_superior > 0:
        print(f"  reservatório superior {reservatorio_superior:g} L, "
              f"limiar de recalque {limiar_recalque:g} L")
    print(f"  {len(volumes)} volumes, de {min(volumes):g} a {max(volumes):g} L\n")

    print(f"  {'saída':<34}{'EMA':>10}{'máximo':>11}{'viés':>11}")
    print("  " + "-" * 66)
    houve_divergencia = False
    for _, campo, rotulo, unidade in CORRESPONDENCIA:
        vetor = np.asarray(erros[campo])
        ema, maximo, vies = np.abs(vetor).mean(), np.abs(vetor).max(), vetor.mean()
        marca = "" if maximo < 0.5 else "   <-- divergente"
        if maximo >= 0.5:
            houve_divergencia = True
        print(f"  {rotulo:<34}{ema:>10.4f}{maximo:>11.4f}{vies:>+11.4f}{marca}")
    print(f"\n  unidades: pp para percentuais, L/dia para volumes")

    if houve_divergencia:
        print("\n  Divergência acima de 0,5 na maior diferença de alguma saída.")
        if not usar_limiar:
            print("  Repita com --descarte-como-limiar: sem isso, a diferença inclui a")
            print("  mudança deliberada no tratamento do descarte de primeira chuva.")
    else:
        print("\n  Todas as saídas concordam dentro de 0,5 na maior diferença.")
    return 0


def main() -> int:
    analisador = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
    analisador.add_argument("exportacao", type=Path, help="CSV exportado do Netuno 4")
    analisador.add_argument("--serie", required=True,
                            help="arquivo em data/rainfall/ usado na simulação")
    analisador.add_argument("--area", type=float, required=True, help="área de captação (m2)")
    analisador.add_argument("--demanda", type=float, required=True,
                            help="demanda total por morador (L/dia)")
    analisador.add_argument("--moradores", type=int, required=True)
    analisador.add_argument("--percentual", type=float, required=True,
                            help="percentual da demanda suprido por água pluvial")
    analisador.add_argument("--coeficiente", type=float, required=True,
                            help="coeficiente de escoamento superficial")
    analisador.add_argument("--descarte", type=float, required=True,
                            help="descarte da precipitação inicial (mm)")
    analisador.add_argument("--descarte-como-limiar", action="store_true",
                            help="emula a regra do Netuno 4, isolando o balanço hídrico")
    analisador.add_argument("--reservatorio-superior", type=float, default=0.0,
                            help="volume do reservatório superior (L); 0 desativa")
    analisador.add_argument("--limiar-recalque", type=float, default=0.0,
                            help="volume de acionamento da motobomba (L)")
    a = analisador.parse_args()

    if not a.exportacao.exists():
        raise SystemExit(f"exportação não encontrada: {a.exportacao}")

    return comparar(a.exportacao, a.serie, a.area, a.demanda, a.moradores,
                    a.percentual, a.coeficiente, a.descarte, a.descarte_como_limiar,
                    a.reservatorio_superior, a.limiar_recalque)


if __name__ == "__main__":
    raise SystemExit(main())
