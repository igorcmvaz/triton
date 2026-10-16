# -*- coding: utf-8 -*-
"""As figuras que o próprio programa desenha, tal como aparecem na tela.

As demais figuras do manual foram desenhadas para o manual. Estas não: são os
gráficos das abas de resultados do Triton, produzidos pelo mesmo código que o
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
os.environ["TRITON_EDITION"] = "INT"

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

VOLUME_TUTORIAL = 4000.0  # gerar_tabelas.TUTORIAL["volume"]
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
    from triton.core.simulation import run_single_simulation, run_sweep_simulation

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


ROTULOS_DOS_CRITERIOS = (
    "Maximum potential", "Minimum overflow", "Highest NPV", "Shortest discounted payback",
    "Highest IRR", "Lowest end-of-life CO₂", "Lowest potable water use",
)


def _formato_en(valor, decimals=2, thousands=True):
    """O número no formato do manual em inglês: vírgula de milhar, ponto decimal.

    Os gráficos da interface chamam ``format_ptbr`` do núcleo, que sempre imprime no formato
    brasileiro («26,8%», «4.000 L»). Aqui ele é trocado só durante o desenho das figuras.
    """
    if valor is None:
        return "-"
    return f"{float(valor):,.{decimals}f}" if thousands else f"{float(valor):.{decimals}f}"


def _gravar(widget, nome, proporcao=9.0 / 16.0, nota=None):
    """Grava a figura do widget na largura em que ela será impressa."""
    fig = widget.figure
    fig.set_size_inches(LARGURA_PAGINA, LARGURA_PAGINA * proporcao)
    try:
        fig.tight_layout(pad=0.9)
    except Exception:
        pass
    if nota:
        fig.text(0.995, 0.005, nota, ha="right", va="bottom", fontsize=6.5, color="#64748b")
    fig.savefig(FIGURAS / nome, dpi=220, facecolor="#ffffff",
                bbox_inches="tight")
    print("  figuras/" + nome)


def _candidatos(serie, material=MATERIAL,
                volumes=(1000, 2000, 3000, 4000, 5000, 8000, 12000)):
    from gerar_tabelas import _config_economica, _config_projeto
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.simulation import run_single_simulation
    from triton.core.topsis import TopsisCandidate

    cfg_sim = _config_projeto()
    cands, economico = [], []
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  **cfg_sim)
        e = run_economic_analysis(_config_economica(v, material), r)
        from gerar_tabelas import _config_ambiental
        amb = _config_ambiental(r)
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
    from triton.core.edition import set_current_edition, EDITION_INT
    set_current_edition(EDITION_INT)
    from triton.ui.translation import set_current_lang
    set_current_lang('en')

    import triton.ui.charts as _graficos
    _graficos.format_ptbr = _formato_en
    from triton.ui.charts import (
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
    # No projeto de Nova York o consumo pluvial passa o extravasado perto do volume escolhido: os dois
    # rótulos do gráfico (extravasado acima, consumo abaixo) caem um sobre o outro. Troca-se o lado.
    if unica.annual_spill_m3 < unica.annual_pluvial_consumed_m3:
        from matplotlib.text import Annotation
        for a in g.figure.axes[0].texts:
            if isinstance(a, Annotation):
                a.xyann = (0, -12) if a.get_color() == "#dc2626" else (0, 6)
    _gravar(g, "fig12_programa_extravasamento.png")

    g = DaysSatisfactionVsVolumeChart()
    g.update_chart(sweep_results=resultados, single_result=unica)
    _gravar(g, "fig13_programa_dias.png")

    # O gráfico do volume médio armazenado saiu do manual a pedido do
    # professor: a leitura dele era óbvia. Em seu lugar entrou a curva de
    # permanência do nível, desenhada em `gerar_figuras_extra.py`.

    # ── a série diária, na aba da simulação única ────────────────────────────
    from gerar_tabelas import _config_tutorial
    from triton.core.simulation import run_single_simulation
    curta = run_single_simulation(
        precip_data=serie[:365], lower_tank_vol=VOLUME_TUTORIAL,
        store_daily_details=True, **_config_tutorial())
    g = DailyBalanceTimeSeriesChart()
    g.update_chart(single_result=curta)
    # A legenda do gráfico cobre o topo da curva: abre-se espaço acima dos 3.800 L do nível máximo.
    g.figure.axes[0].set_ylim(top=5000)
    _gravar(g, "fig48_programa_serie_diaria.png")

    # ── a aba econômica ──────────────────────────────────────────────────────
    # As abas econômica e ambiental ilustram as seções do custo e do carbono,
    # em que o tutorial ainda usa cisterna de concreto; o polietileno só entra
    # na seção da decisão, que é a dos gráficos multicritério.
    cands, _ = _candidatos(serie)
    _, economico = _candidatos(serie, material="CONCRETO")
    g = VplVsVolumeChart()
    g.update_chart(sweep_data=economico, metric="vpl",
                   optimal_tech_vol=varredura.optimal_lower_tank_vol,
                   currency_symbol="US$")
    from matplotlib.ticker import FuncFormatter
    for eixo in g.figure.axes:
        eixo.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{int(x):,}"))
    _gravar(g, "fig49_programa_vpl.png", nota="illustrative costs, not market prices")

    # ── a aba ambiental ──────────────────────────────────────────────────────
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from gerar_tabelas import _config_ambiental
    from gerar_tabelas import _config_projeto
    projeto = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME_TUTORIAL,
                                    **_config_projeto())
    amb = _config_ambiental(projeto)
    amb.lower_material_key = "CONCRETO"
    lca = calculate_lca(VOLUME_TUTORIAL, projeto.annual_pluvial_consumed_m3, amb)
    g = EnvironmentalBalanceSummaryChart()
    g.update_chart(lca_result=lca, lifespan_years=VIDA_UTIL)
    _gravar(g, "fig50_programa_balanco_ambiental.png", nota="illustrative emission factors")

    # ── a aba multicritério ──────────────────────────────────────────────────
    from triton.core.topsis import calculate_topsis_scores
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

    # Os rótulos dos sete critérios vêm do núcleo em português e a tradução da interface não os cobre;
    # no manual em inglês a figura leva a versão inglesa deles.
    topsis.criterion_labels = ROTULOS_DOS_CRITERIOS
    g = TOPSISProximityChart()
    g.update_chart(topsis_result=topsis,
                   selected_best_index=topsis.best_index)
    _gravar(g, "fig52_programa_proximidade.png")

    # ── a aba dos índices pluviométricos ─────────────────────────────────────
    from triton.core.calculator import IndicesCalculator
    inicio = datetime(1991, 1, 1)   # a série ERA5 de data/rainfall começa em 1/1/1991
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
