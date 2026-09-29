"""Nenhuma figura pode desenhar texto fora da própria moldura.

Um rótulo de eixo comprido, ou um valor escrito na ponta da barra mais longa,
atravessa a borda da figura e aparece cortado na tela — ou, pior, por cima do
rótulo da categoria ao lado. Aconteceu com as duas figuras de carbono, cujo
rótulo dizia «Carbono no Ciclo de Vida: [- Retirada / + Emissão] (kg CO2e /
20 anos)» numa faixa que não comportava metade disso.

Olhar figura por figura não escala: são dezoito. Este teste desenha cada uma com
dados do próprio motor, mede o retângulo de cada texto e recusa o que escapa.

A medida só vale para o que o matplotlib realmente desenha: marcas de eixo fora
do intervalo ficam guardadas no eixo sem serem pintadas, e entrariam aqui como
alarme falso.
"""
import os
import sys

import numpy as np
import pandas as pd
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

#: O painel mais estreito em que uma figura aparece: ao lado da tabela
#: comparativa, na aba econômica.
LARGURA, ALTURA = 620, 420


@pytest.fixture(scope="module")
def motor():
    """Uma varredura e uma simulação de verdade, para alimentar as figuras."""
    from netuno.core.parser import load_precipitation
    from netuno.core.simulation import run_sweep_simulation, run_single_simulation
    chuva = load_precipitation(os.path.join(RAIZ, "data", "rainfall", "Florianopolis1.csv"))
    varredura = run_sweep_simulation(chuva, lower_tank_max=8000.0, lower_tank_step=1000.0,
                                     area=150.0, total_demand_per_day=400.0,
                                     rainwater_share=0.45)
    unico = run_single_simulation(chuva, lower_tank_vol=6000.0, area=150.0,
                                  total_demand_per_day=400.0, rainwater_share=0.45,
                                  store_daily_details=True)
    return varredura.results_by_volume, unico


def _lca():
    import types
    return types.SimpleNamespace(
        annual_avoided_co2_kg=29.35, total_embodied_co2_kg=295.0,
        annual_pumping_co2_kg=1.0, annual_treatment_co2_kg=0.25,
        annual_water_saved_m3=92.0, annual_pluvial_m3=92.0,
        tank_embodied_co2_kg=180.0, upper_tank_embodied_co2_kg=60.0,
        piping_embodied_co2_kg=35.0, pump_embodied_co2_kg=20.0,
        environmental_payback_years=16.3, net_balance_co2_kg=-267.0)


def _topsis():
    n = 6
    return {"scores": list(np.linspace(0.2, 0.9, n)), "ranking": list(range(n)),
            "alternatives": [f"{500 * (i + 1)} L" for i in range(n)], "best_index": n - 1,
            "distances_best": list(np.linspace(0.8, 0.1, n)),
            "distances_worst": list(np.linspace(0.1, 0.8, n))}


def _indices():
    anos = list(range(1990, 2015))
    gerador = np.random.default_rng(3)
    return pd.DataFrame({
        "year": anos,
        "PRCPTOT": gerador.uniform(900, 2200, len(anos)),
        "R95p": gerador.uniform(150, 600, len(anos)),
        "SDII": gerador.uniform(6, 18, len(anos)),
        "CDD": gerador.integers(10, 80, len(anos)),
        "CWD": gerador.integers(3, 20, len(anos)),
    })


def _economico(pontos):
    """A varredura chega às figuras econômicas como lista de dicionários."""
    return [{"volume_l": r.lower_tank_vol, "vpl": -9000 + 1100 * i - 22 * i * i,
             "capex": 3200 + 520 * i, "annual_opex": 210 + 6 * i,
             "total_opex": (210 + 6 * i) * 20, "tir": 3.5 + 0.45 * i,
             "payback_simple": max(1.0, 27 - 0.8 * i),
             "payback_discounted": max(1.5, 31 - 0.9 * i)}
            for i, r in enumerate(pontos)]


def _casos(motor):
    pontos, unico = motor
    eco = _economico(pontos)
    varredura = dict(sweep_results=pontos, single_result=unico)
    return [
        ("PotentialVsVolumeChart", "update_chart", dict(**varredura, optimal_vol=6000)),
        ("DeltaVsVolumeChart", "update_chart", dict(**varredura)),
        ("SpillAndConsumptionVsVolumeChart", "update_chart", dict(**varredura)),
        ("StoredVolumeVsTankVolumeChart", "update_chart", dict(**varredura)),
        ("DaysSatisfactionVsVolumeChart", "update_chart", dict(**varredura)),
        ("DailyBalanceTimeSeriesChart", "update_chart", dict(single_result=unico)),
        ("TOPSISComparisonChart", "update_chart", dict(topsis_result=_topsis())),
        ("TOPSISProximityChart", "update_chart", dict(topsis_result=_topsis())),
        ("VplVsVolumeChart", "update_chart", dict(sweep_data=eco, metric="vpl",
                                                  optimal_tech_vol=6000, tma_rate=8.0)),
        ("VplVsVolumeChart", "update_chart", dict(sweep_data=eco, metric="costs")),
        ("VplVsVolumeChart", "update_chart", dict(sweep_data=eco, metric="tir", tma_rate=8.0)),
        ("VplVsVolumeChart", "update_chart", dict(sweep_data=eco, metric="payback_discounted")),
        ("EnvironmentalBalanceSummaryChart", "update_chart", dict(lca_result=_lca())),
        ("CO2ComparisonChart", "update_chart", dict(lca_result=_lca())),
        ("LCAComponentBreakdownChart", "update_chart", dict(lca_result=_lca())),
        ("PrcptotAnnualChart", "plot_data", dict(df_indices=_indices())),
        ("SdiiVsR95pChart", "plot_data", dict(df_indices=_indices())),
        ("CddCwdAnnualChart", "plot_data", dict(df_indices=_indices())),
    ]


def _textos_fora_da_moldura(figura):
    figura.canvas.draw()
    moldura = figura.bbox
    desenhador = figura.canvas.get_renderer()
    fora = []
    for eixo in figura.axes:
        alvos = [(eixo.xaxis.label, "rótulo do eixo X"),
                 (eixo.yaxis.label, "rótulo do eixo Y"),
                 (eixo.title, "título")]
        # Só as marcas dentro do intervalo: as de fora não chegam a ser pintadas.
        x0, x1 = sorted(eixo.get_xlim())
        y0, y1 = sorted(eixo.get_ylim())
        alvos += [(t, "marca do eixo X")
                  for t, v in zip(eixo.get_xticklabels(), eixo.get_xticks())
                  if x0 - 1e-9 <= v <= x1 + 1e-9]
        alvos += [(t, "marca do eixo Y")
                  for t, v in zip(eixo.get_yticklabels(), eixo.get_yticks())
                  if y0 - 1e-9 <= v <= y1 + 1e-9]
        alvos += [(t, "texto no gráfico") for t in eixo.texts]
        for artista, papel in alvos:
            texto = artista.get_text()
            if not texto.strip():
                continue
            try:
                caixa = artista.get_window_extent(desenhador)
            except Exception:
                continue
            escapa = max(moldura.x0 - caixa.x0, caixa.x1 - moldura.x1,
                         moldura.y0 - caixa.y0, caixa.y1 - moldura.y1)
            if escapa > 0.5:
                fora.append(f"{papel} «{texto[:50]}» escapa {escapa:.1f} px")
    return fora


def test_nenhuma_figura_desenha_texto_fora_da_moldura(qapp, motor):
    """Se falhar: encurte o rótulo, quebre-o em duas linhas ou traga o valor
    para dentro da barra. Aumentar a figura não resolve — ela encolhe de novo na
    tela do usuário."""
    import netuno.ui.charts as charts

    problemas = []
    for classe, metodo, argumentos in _casos(motor):
        figura_widget = getattr(charts, classe)()
        figura_widget.resize(LARGURA, ALTURA)
        figura_widget.show()
        qapp.processEvents()
        getattr(figura_widget, metodo)(**argumentos)
        qapp.processEvents()
        rotulo = classe + (f"/{argumentos['metric']}" if argumentos.get("metric") else "")
        for achado in _textos_fora_da_moldura(figura_widget.figure):
            problemas.append(f"{rotulo}: {achado}")
        figura_widget.close()

    assert not problemas, "texto cortado em:\n  " + "\n  ".join(problemas)
