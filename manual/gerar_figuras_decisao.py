# -*- coding: utf-8 -*-
"""Figuras da decisão: investimento, multicritério, sensibilidade e verificação.

Cinco figuras para a parte do manual que mais depende de números e menos se
deixa ler em tabela: de que é feito o investimento, como o TOPSIS mede distância
até o ideal, o que a análise estocástica diz sobre a estabilidade da escolha,
qual variável mais move o resultado econômico, e de que se compõe a divergência
em relação ao Netuno 4.

Executar a partir da raiz do programa:
    python manual/gerar_figuras_decisao.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import matplotlib                                                 # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                   # noqa: E402
import numpy as np                                                # noqa: E402

from gerar_figuras import (                                       # noqa: E402
    AZUL, EIXO, LARANJA, ROXO, SUPERFICIE, TINTA, TINTA2, VERDE,
    _eixos, _salvar,
)
from gerar_tabelas import (                                       # noqa: E402
    CUSTOS_TUTORIAL, TARIFA_CASAN, VOLUME, _config_economica, _config_projeto, _config_tutorial,
    _serie,
)

from netuno.core.simulation import run_single_simulation          # noqa: E402

VOLUMES = (1000, 2000, 3000, 4000, 5000, 8000, 12000)
MATERIAL = "PEAD"


def _candidatos():
    """Os seis volumes do capítulo multicritério, com os sete critérios."""
    from netuno.core.economic import run_economic_analysis
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.topsis import TopsisCandidate

    serie = _serie()
    cfg_sim = _config_projeto()
    cands = []
    for v in VOLUMES:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  **cfg_sim)
        e = run_economic_analysis(_config_economica(v, MATERIAL), r)
        from gerar_tabelas import _config_ambiental
        amb = _config_ambiental(r)
        amb.lower_material_key = MATERIAL
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
    return cands


# ══════════════════════════════════════════════════════════════════════════════
# De que é feito o investimento
# ══════════════════════════════════════════════════════════════════════════════

def figura_investimento():
    """O CAPEX aberto por rubrica, em três volumes de reservatório."""
    from netuno.core.cost_estimates import estimate_tank_price
    from netuno.core.water_quality import size_first_flush_system

    from gerar_tabelas import TUTORIAL

    # O descarte inicial não depende do volume da cisterna, e sim da lâmina de
    # descarte e da área de captação: V = d × A. Entra como rubrica própria
    # porque o programa o orça à parte, na linha de tratamento.
    descarte = size_first_flush_system(discard_mm=TUTORIAL["discard_mm"],
                                       roof_area_m2=TUTORIAL["area"])

    volumes = (2000, int(VOLUME), 12000)
    rubricas = [
        ("reservatório inferior", AZUL),
        ("mão de obra", LARANJA),
        ("tubulação", VERDE),
        ("acessórios", ROXO),
        (f"descarte inicial ({descarte.diverter_volume_liters:.0f} L "
         "e separador de folhas)", "#8a8880"),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    rotulos, totais = [], []
    for i, v in enumerate(volumes):
        valores = [
            estimate_tank_price(float(v), MATERIAL),
            CUSTOS_TUTORIAL["cost_labor"],
            CUSTOS_TUTORIAL["cost_piping"],
            CUSTOS_TUTORIAL["cost_accessories"],
            descarte.first_flush_total_capex,
        ]
        base = 0.0
        for (nome, cor), valor in zip(rubricas, valores):
            ax.bar(i, valor, 0.5, bottom=base, color=cor, zorder=3,
                   edgecolor=SUPERFICIE, linewidth=2.0,
                   label=nome if i == 0 else None)
            if valor > 900:
                ax.text(i, base + valor / 2.0,
                        ("R$ " + f"{valor:,.0f}").replace(",", "."),
                        ha="center", va="center", fontsize=8.0, color="#ffffff")
            base += valor
        total = base
        totais.append(total)
        rotulos.append(f"{v / 1000.0:.0f} m³".replace(".", ",") + "\n" +
                       ("R$ " + f"{total:,.0f}").replace(",", "."))

    _eixos(ax, "", "", "investimento inicial (R$)")
    ax.set_xticks(range(len(volumes)))
    ax.set_xticklabels(rotulos, fontsize=9.0)
    ax.set_xlim(-0.6, len(volumes) - 0.4)
    teto = 2000.0 * np.ceil(max(totais) * 1.04 / 2000.0)
    ax.set_ylim(0, teto)
    ax.set_yticks(np.arange(0, teto + 1, 2000))
    ax.set_yticklabels([f"{v:,.0f}".replace(",", ".")
                        for v in np.arange(0, teto + 1, 2000)])
    ax.legend(frameon=False, fontsize=8.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.2), ncol=2)

    fig.tight_layout()
    _salvar(fig, "fig21_investimento.png")


# O esquema do TOPSIS no plano de dois critérios saiu a pedido do professor: a
# seção do método mostra o gráfico que o próprio programa desenha, gerado em
# `gerar_figuras_do_programa.py` com o mesmo nome de arquivo.


# ══════════════════════════════════════════════════════════════════════════════
# A aceitabilidade estocástica, volume a volume
# ══════════════════════════════════════════════════════════════════════════════

def figura_smaa():
    """Com que frequência cada volume vence, sorteando os pesos."""
    from netuno.core.mcdm_methods import run_smaa_analysis

    cands = _candidatos()
    res = run_smaa_analysis(cands, num_samples=5000, random_seed=42)
    probs = np.asarray(res.first_rank_probs, dtype=float)
    rotulos = [f"{c.lower_tank_vol / 1000.0:.0f}".replace(".", ",") + " m³"
               for c in cands]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    melhor = int(np.argmax(probs))
    cores = [ROXO if i == melhor else AZUL for i in range(len(probs))]
    ax.bar(rotulos, probs, color=cores, width=0.55, zorder=3)
    for i, p in enumerate(probs):
        if p > 0.4:
            ax.text(i, p + max(probs) * 0.03, f"{p:.0f}%", ha="center",
                    fontsize=8.6, color=TINTA)

    _eixos(ax, "", "volume do reservatório",
           "aceitabilidade de primeiro lugar b¹ (%)")
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))

    fig.tight_layout()
    _salvar(fig, "fig23_smaa.png")


# ══════════════════════════════════════════════════════════════════════════════
# O tornado: que variável move o resultado
# ══════════════════════════════════════════════════════════════════════════════

def figura_tornado():
    from netuno.core.economic import (
        run_robust_economic_analysis, run_sensitivity_analysis,
    )
    from netuno.core.etap_integration import (
        capex_incremental_da_etap, opex_anual_incremental_da_etap,
    )
    from netuno.core.pump_energy import compute_annual_pump_energy

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME,
                              **_config_projeto())
    cfg = _config_economica(VOLUME, "CONCRETO")
    base = dict(
        # O investimento e o custeio incluem a linha de tratamento com o
        # descarte físico, como a análise econômica completa do tutorial.
        initial_investment=(cfg.cost_lower_tank + cfg.cost_upper_tank + cfg.cost_labor +
                            cfg.pump_unit_cost * cfg.pump_count +
                            cfg.cost_piping + cfg.cost_accessories +
                            capex_incremental_da_etap(cfg, None, r)),
        annual_water_saved_m3=r.annual_pluvial_consumed_m3,
        water_tariff_per_m3=float(TARIFA_CASAN[2][2]),
        sewage_tariff_per_m3=float(TARIFA_CASAN[2][2]),
        sewage_mode=1,
        water_tariff_escalation_rate=0.05,
        sewage_tariff_escalation_rate=0.05,
        elec_tariff_escalation_rate=0.05,
        # A interface do programa pede TMA e inflação ao mês; o modelo anual
        # pede as taxas equivalentes ao ano, e é a conversão que as iguala.
        inflation_rate=(1.0 + CUSTOS_TUTORIAL["inflation"] / 100.0) ** 12 - 1.0,
        discount_rate=(1.0 + CUSTOS_TUTORIAL["tma"] / 100.0) ** 12 - 1.0,
        annual_om_cost_base=120.0 + opex_anual_incremental_da_etap(cfg, None, r),
        # A energia do recalque, pela mesma função do econômico. Sem estes três
        # campos valiam os padrões da função, 0,75 kW por 150 h a R$ 1/kWh.
        pump_power_kw=compute_annual_pump_energy(cfg, r).annual_kwh,
        pump_hours_year=1.0,
        elec_tariff_kwh=cfg.elec_tariff,
        analysis_period_years=20,
    )
    vpl_base = run_robust_economic_analysis(**base).vpl
    curvas = run_sensitivity_analysis(base, variations_pct=[-30.0, 30.0])

    # A cor identifica a variação aplicada, e não o sinal do efeito: é o que
    # deixa ver que aumentar a TMA reduz o VPL, e não o contrário.
    itens = []
    for rotulo, curva in curvas.items():
        por_variacao = {round(p): v for p, v in curva}
        itens.append((rotulo, por_variacao[-30] - vpl_base,
                      por_variacao[30] - vpl_base))
    itens.sort(key=lambda t: max(abs(t[1]), abs(t[2])))

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    y = np.arange(len(itens))
    for i, (_, menos, mais) in enumerate(itens):
        ax.barh(i, mais, height=0.6, color=VERDE, zorder=3)
        ax.barh(i, menos, height=0.6, color=LARANJA, zorder=3)
    ax.axvline(0.0, color=TINTA, linewidth=1.2, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels([t[0] for t in itens], fontsize=8.0)
    _eixos(ax, "", "variação do VPL em relação ao caso-base (R$)", "")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=VERDE, label="premissa +30%"),
                       Patch(facecolor=LARANJA, label="premissa −30%")],
              frameon=False, fontsize=8.4, loc="lower right")
    marcas = ax.get_xticks()
    ax.set_xticks(marcas)
    ax.set_xticklabels([f"{v:,.0f}".replace(",", ".").replace("-", "−")
                        for v in marcas])

    fig.tight_layout()
    _salvar(fig, "fig24_tornado.png")


# ══════════════════════════════════════════════════════════════════════════════
# A divergência em relação ao Netuno 4, decomposta
# ══════════════════════════════════════════════════════════════════════════════

def figura_cascata():
    """De 2,81 pp a 0,25 pp: o que cada explicação retira da divergência."""
    passos = [
        ("divergência\ntotal", 2.81, AZUL),
        ("critério de\nvolume ótimo", -1.11, LARANJA),
        ("tratamento do\ndescarte", -1.36, LARANJA),
        ("resíduo do\nbalanço hídrico", 0.25, VERDE),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    base = 0.0
    for i, (rotulo, valor, cor) in enumerate(passos):
        if i == 0:
            ax.bar(i, valor, 0.55, color=cor, zorder=3)
            topo, base = valor, valor
        elif i == len(passos) - 1:
            ax.bar(i, valor, 0.55, color=cor, zorder=3)
            topo = valor
        else:
            ax.bar(i, valor, 0.55, bottom=base, color=cor, zorder=3)
            ax.plot([i - 0.75, i + 0.28], [base, base], color=TINTA2,
                    linewidth=0.8, linestyle=":", zorder=2)
            base += valor
            topo = base
        ax.text(i, max(topo, base) + 0.10,
                f"{abs(valor):.2f} pp".replace(".", ","), ha="center",
                fontsize=9.0, color=TINTA)

    ax.set_xticks(range(len(passos)))
    ax.set_xticklabels([p[0] for p in passos], fontsize=8.4)
    _eixos(ax, "", "", "erro médio absoluto (pontos percentuais)")
    ax.set_ylim(0, 3.5)
    ax.set_yticks(np.arange(0, 3.51, 0.5))
    ax.set_yticklabels([f"{v:.1f}".replace(".", ",")
                        for v in np.arange(0, 3.51, 0.5)])
    # A leitura dos passos fica na legenda da figura: dentro do desenho,
    # qualquer bloco de texto encobre uma das barras.
    fig.tight_layout()
    _salvar(fig, "fig25_cascata.png")


def main():
    print("figuras da decisão:")
    figura_investimento()
    figura_smaa()
    figura_tornado()
    figura_cascata()


if __name__ == "__main__":
    main()
