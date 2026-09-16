# -*- coding: utf-8 -*-
"""As figuras que o próprio programa desenha, tal como aparecem na tela.

As demais figuras do manual foram desenhadas para o manual. Estas não: são os
gráficos das abas de resultados do Netuno 5, produzidos pelo mesmo código que o
usuário aciona, com os dados do projeto do tutorial. O leitor que chegar a essas
telas reconhece o que está vendo, e o manual passa a mostrar a interface em vez
de descrevê-la.

**Sobre o tamanho.** Os gráficos da interface declaram tamanhos de fonte em
pontos e são desenhados numa tela larga. Gravá-los na largura da tela e depois
reduzi-los à largura da página encolheria a fonte na mesma proporção, e foi o que
tornou ilegível a primeira versão destas figuras. Aqui cada figura é gravada já
na largura em que será impressa, de modo que oito pontos na tela continuem oito
pontos no papel.

A janela nunca é aberta: o Qt roda em plataforma «offscreen» e só a figura do
matplotlib é gravada.

Executar a partir da raiz do programa:
    python manual/gerar_figuras_do_programa.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

FIGURAS = AQUI / "figuras"
FIGURAS.mkdir(exist_ok=True)

VOLUME_TUTORIAL = 5000.0
PASSO = 1000.0
VOLUME_MAXIMO = 20000.0
VIDA_UTIL = 20.0
MATERIAL = "PEAD"
# O limiar de ganho marginal do tutorial. A varredura sem ele usava o padrão
# do programa, 5 %/m3, e marcava 3.000 L como ótimo técnico num gráfico
# posto ao lado de um texto que escolhe 5.000 L.
LIMIAR_TUTORIAL = 1.0

# A largura útil da página do manual, em polegadas: 16,7 cm. Gravar nesta
# largura é o que preserva o tamanho da fonte depois da composição.
LARGURA_PAGINA = 6.57


def _dados():
    """Uma varredura e uma simulação única, as duas entradas dos gráficos."""
    from gerar_tabelas import _config_tutorial, _serie
    from netuno.core.simulation import run_single_simulation, run_sweep_simulation

    serie = _serie()
    cfg = _config_tutorial()
    varredura = run_sweep_simulation(precip_data=serie,
                                     lower_tank_max=VOLUME_MAXIMO,
                                     lower_tank_step=PASSO,
                                     delta_ideal_threshold=LIMIAR_TUTORIAL,
                                     **cfg)
    unica = run_single_simulation(precip_data=serie,
                                  lower_tank_vol=VOLUME_TUTORIAL, **cfg)
    return serie, varredura, unica


def _gravar(widget, nome, proporcao=9.0 / 16.0):
    """Grava a figura do widget na largura em que ela será impressa."""
    fig = widget.figure
    fig.set_size_inches(LARGURA_PAGINA, LARGURA_PAGINA * proporcao)
    try:
        fig.tight_layout(pad=0.9)
    except Exception:
        pass
    fig.savefig(FIGURAS / nome, dpi=220, facecolor="#ffffff",
                bbox_inches="tight")
    print("  figuras/" + nome)


def _candidatos(serie, material=MATERIAL,
                volumes=(1000, 2000, 3000, 5000, 8000, 12000)):
    from gerar_tabelas import _config_economica, _config_tutorial
    from netuno.core.economic import run_economic_analysis
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.simulation import run_single_simulation
    from netuno.core.topsis import TopsisCandidate

    cfg_sim = _config_tutorial()
    cands, economico = [], []
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  **cfg_sim)
        e = run_economic_analysis(_config_economica(v, material), r)
        amb = EnvironmentalConfig()
        amb.lower_material_key = material
        lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, amb)
        cands.append(TopsisCandidate(
            lower_tank_vol=float(v),
            water_saved_m3_yr=r.annual_pluvial_consumed_m3,
            vpl_brl=e.vpl, co2_saved_kg_lifetime=lca.lifetime_net_co2_saved_kg,
            capex_brl=e.capex_total,
            potential_savings_pct=r.potential_potable_savings_pct,
            overflow_m3_yr=r.annual_spill_m3,
            discounted_payback_years=e.payback_years,
            irr_pct=e.tir_annual_pct,
            potable_consumed_m3_yr=r.annual_potable_consumed_m3))
        economico.append({
            "volume_l": float(v), "vpl": e.vpl,
            "tir": e.tir_annual_pct or 0.0,
            "payback": e.payback_years or 0.0,
            "capex": e.capex_total,
        })
    return cands, economico


def main():
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])

    from netuno.ui.charts import (
        CddCwdAnnualChart, DailyBalanceTimeSeriesChart,
        DaysSatisfactionVsVolumeChart, DeltaVsVolumeChart,
        EnvironmentalBalanceSummaryChart, PotentialVsVolumeChart,
        PrcptotAnnualChart, SeasonalPrecipChart,
        SpillAndConsumptionVsVolumeChart,
        TOPSISComparisonChart, TOPSISProximityChart, VplVsVolumeChart,
    )

    serie, varredura, unica = _dados()
    resultados = varredura.results_by_volume

    print("figuras geradas pelo próprio programa:")

    # ── a varredura, os quatro gráficos da aba técnica ───────────────────────
    g = PotentialVsVolumeChart()
    g.update_chart(sweep_results=resultados, single_result=unica,
                   optimal_vol=varredura.optimal_lower_tank_vol)
    _gravar(g, "fig10_programa_potencial.png")

    g = DeltaVsVolumeChart()
    g.update_chart(sweep_results=resultados, single_result=unica,
                   delta_threshold=LIMIAR_TUTORIAL)
    _gravar(g, "fig11_programa_delta.png")

    g = SpillAndConsumptionVsVolumeChart()
    g.update_chart(sweep_results=resultados, single_result=unica)
    _gravar(g, "fig12_programa_extravasamento.png")

    g = DaysSatisfactionVsVolumeChart()
    g.update_chart(sweep_results=resultados, single_result=unica)
    _gravar(g, "fig13_programa_dias.png")

    # O gráfico do volume médio armazenado saiu do manual a pedido do
    # professor: a leitura dele era óbvia. Em seu lugar entrou a curva de
    # permanência do nível, desenhada em `gerar_figuras_extra.py`.

    # ── a série diária, na aba da simulação única ────────────────────────────
    from gerar_tabelas import _config_tutorial
    from netuno.core.simulation import run_single_simulation
    curta = run_single_simulation(
        precip_data=serie[:365], lower_tank_vol=VOLUME_TUTORIAL,
        store_daily_details=True, **_config_tutorial())
    g = DailyBalanceTimeSeriesChart()
    g.update_chart(single_result=curta)
    _gravar(g, "fig48_programa_serie_diaria.png")

    # ── a aba econômica ──────────────────────────────────────────────────────
    # As abas econômica e ambiental ilustram as seções do custo e do carbono,
    # em que o tutorial ainda usa cisterna de concreto; o polietileno só entra
    # na seção da decisão, que é a dos gráficos multicritério.
    cands, _ = _candidatos(serie)
    _, economico = _candidatos(serie, material="CONCRETO")
    g = VplVsVolumeChart()
    g.update_chart(sweep_data=economico, metric="vpl",
                   optimal_tech_vol=varredura.optimal_lower_tank_vol)
    _gravar(g, "fig49_programa_vpl.png")

    # ── a aba ambiental ──────────────────────────────────────────────────────
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    amb = EnvironmentalConfig()
    amb.lower_material_key = "CONCRETO"
    lca = calculate_lca(VOLUME_TUTORIAL, unica.annual_pluvial_consumed_m3, amb)
    g = EnvironmentalBalanceSummaryChart()
    g.update_chart(lca_result=lca, lifespan_years=VIDA_UTIL)
    _gravar(g, "fig50_programa_balanco_ambiental.png")

    # ── a aba multicritério ──────────────────────────────────────────────────
    from netuno.core.topsis import calculate_topsis_scores
    topsis = calculate_topsis_scores(cands)
    g = TOPSISComparisonChart()
    g.update_chart(topsis_result=topsis, method="topsis")
    _gravar(g, "fig51_programa_topsis.png")

    # A seção do método mostra o mesmo gráfico sobre a varredura inteira, de
    # 1 a 20 m³, em que o programa troca as barras pela curva do escore.
    cands_varredura, _ = _candidatos(
        serie, volumes=tuple(range(1000, 20001, 1000)))
    g = TOPSISComparisonChart()
    g.update_chart(topsis_result=calculate_topsis_scores(cands_varredura),
                   method="topsis")
    _gravar(g, "fig22_topsis.png")

    g = TOPSISProximityChart()
    g.update_chart(topsis_result=topsis,
                   selected_best_index=topsis.best_index)
    _gravar(g, "fig52_programa_proximidade.png")

    # ── a aba dos índices pluviométricos ─────────────────────────────────────
    from netuno.core.calculator import IndicesCalculator
    inicio = datetime(1980, 1, 1)
    import pandas as pd
    datas = pd.date_range(inicio, periods=len(serie), freq="D")
    calc = IndicesCalculator(list(zip(datas, [float(v) for v in serie])))
    indices = calc.compute_climate_indices()

    g = PrcptotAnnualChart()
    g.plot_data(indices)
    _gravar(g, "fig53_programa_prcptot.png", proporcao=9.0 / 24.0)

    g = CddCwdAnnualChart()
    g.plot_data(indices)
    _gravar(g, "fig54_programa_cdd_cwd.png", proporcao=9.0 / 24.0)

    g = SeasonalPrecipChart()
    g.plot_data(serie, start_date=inicio)
    _gravar(g, "fig55_programa_sazonal.png", proporcao=9.0 / 24.0)

    del app


if __name__ == "__main__":
    main()
