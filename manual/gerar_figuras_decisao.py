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
    CUSTOS_TUTORIAL, TARIFA_CASAN, _config_economica, _config_tutorial,
    _serie,
)

from netuno.core.simulation import run_single_simulation          # noqa: E402

VOLUMES = (1000, 2000, 3000, 5000, 8000, 12000)
MATERIAL = "PEAD"


def _candidatos():
    """Os seis volumes do capítulo multicritério, com os sete critérios."""
    from netuno.core.economic import run_economic_analysis
    from netuno.core.environmental import EnvironmentalConfig, calculate_lca
    from netuno.core.topsis import TopsisCandidate

    serie = _serie()
    cfg_sim = _config_tutorial()
    cands = []
    for v in VOLUMES:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  **cfg_sim)
        e = run_economic_analysis(_config_economica(v, MATERIAL), r)
        amb = EnvironmentalConfig()
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

    volumes = (2000, 5000, 12000)
    rubricas = [
        ("reservatório", AZUL),
        ("mão de obra", LARANJA),
        ("tubulação", VERDE),
        ("acessórios", ROXO),
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

    _eixos(ax, "O reservatório só domina o investimento nos volumes grandes", "",
           "investimento inicial (R$)")
    ax.set_xticks(range(len(volumes)))
    ax.set_xticklabels(rotulos, fontsize=9.0)
    ax.set_xlim(-0.6, len(volumes) - 0.2)
    ax.set_ylim(0, max(totais) * 1.15)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")

    fig.tight_layout()
    _salvar(fig, "fig21_investimento.png")


# ══════════════════════════════════════════════════════════════════════════════
# O TOPSIS, no plano de dois critérios
# ══════════════════════════════════════════════════════════════════════════════

def figura_topsis():
    """As alternativas no plano, com o ideal e o anti-ideal marcados.

    O método trabalha em sete dimensões; duas bastam para mostrar o que ele faz,
    que é medir distância até dois pontos de referência que não existem.
    """
    from netuno.core.topsis import calculate_topsis_scores

    cands = _candidatos()
    res = calculate_topsis_scores(cands)

    pot = np.asarray([c.potential_savings_pct for c in cands])
    vpl = np.asarray([c.vpl_brl for c in cands])

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    ideal = (pot.max(), vpl.max())
    anti = (pot.min(), vpl.min())

    ax.plot(*ideal, "*", color=VERDE, markersize=17, zorder=5)
    ax.text(ideal[0], ideal[1] * 1.03, "solução ideal\n(não existe)",
            ha="right", va="bottom", fontsize=8.2, color=VERDE)
    ax.plot(*anti, "X", color=LARANJA, markersize=11, zorder=5)
    ax.text(anti[0], anti[1] * 1.03, "anti-ideal", ha="left", va="bottom",
            fontsize=8.2, color=LARANJA)

    escolhido = int(res.best_index)
    for i, c in enumerate(cands):
        cor = ROXO if i == escolhido else AZUL
        ax.plot(pot[i], vpl[i], "o", color=cor,
                markersize=11 if i == escolhido else 7.5, zorder=4)
        ax.annotate(f"{c.lower_tank_vol / 1000.0:.0f} m³".replace(".", ","),
                    xy=(pot[i], vpl[i]), xytext=(0, -14),
                    textcoords="offset points", ha="center", fontsize=8.0,
                    color=cor)
        if i == escolhido:
            # As duas distâncias que decidem o método, só para a alternativa
            # vencedora: traçá-las para todas encobriria a figura.
            ax.plot([pot[i], ideal[0]], [vpl[i], ideal[1]], color=VERDE,
                    linewidth=1.4, linestyle="--", zorder=2)
            ax.plot([pot[i], anti[0]], [vpl[i], anti[1]], color=LARANJA,
                    linewidth=1.4, linestyle="--", zorder=2)

    # A explicação sai da nuvem e vai para baixo do eixo: dentro do gráfico
    # não há vazio que a comporte sem cobrir o rótulo de algum volume.
    ax.text(0.0, -0.19,
            "O compromisso, em roxo, é o ponto mais próximo do ideal e mais "
            "longe do anti-ideal.",
            transform=ax.transAxes, fontsize=8.4, color=ROXO, va="top")

    _eixos(ax, "O que o TOPSIS mede: distância até dois pontos de referência",
           "potencial de economia (%)", "valor presente líquido (R$)")

    fig.tight_layout()
    _salvar(fig, "fig22_topsis.png")


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

    _eixos(ax, "Sorteando cinco mil conjuntos de pesos, quantas vezes cada volume vence",
           "volume do reservatório", "aceitabilidade de primeiro lugar (%)")
    ax.set_ylim(0, max(100.0, float(probs.max()) * 1.18))
    ax.text(0.02, 0.96,
            "Um volume que vence em quase todos os sorteios é uma escolha "
            "robusta;\ndois volumes empatados significam que a decisão depende "
            "do peso,\ne o peso é do projetista, não do programa.",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.0,
            color=TINTA2, linespacing=1.4)

    fig.tight_layout()
    _salvar(fig, "fig23_smaa.png")


# ══════════════════════════════════════════════════════════════════════════════
# O tornado: que variável move o resultado
# ══════════════════════════════════════════════════════════════════════════════

def figura_tornado():
    from netuno.core.economic import (
        run_robust_economic_analysis, run_sensitivity_analysis,
    )

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=5000.0,
                              **_config_tutorial())
    cfg = _config_economica(5000.0, "CONCRETO")
    base = dict(
        initial_investment=(cfg.cost_lower_tank + cfg.cost_labor +
                            cfg.cost_piping + cfg.cost_accessories),
        annual_water_saved_m3=r.annual_pluvial_consumed_m3,
        water_tariff_per_m3=float(TARIFA_CASAN[2][2]),
        sewage_tariff_per_m3=float(TARIFA_CASAN[2][2]),
        sewage_mode=1,
        water_tariff_escalation_rate=0.12,
        sewage_tariff_escalation_rate=0.12,
        elec_tariff_escalation_rate=0.12,
        # A interface do programa pede TMA e inflação ao mês; o modelo anual
        # pede as taxas equivalentes ao ano, e é a conversão que as iguala.
        inflation_rate=(1.0 + CUSTOS_TUTORIAL["inflation"] / 100.0) ** 12 - 1.0,
        discount_rate=(1.0 + CUSTOS_TUTORIAL["tma"] / 100.0) ** 12 - 1.0,
        annual_om_cost_base=120.0,
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
    _eixos(ax, "O que move o valor presente líquido, a 30% para mais e para menos",
           "variação do VPL em relação ao caso-base (R$)", "")
    ax.text(0.02, 0.04,
            "verde: a variável 30% maior   ·   laranja: 30% menor",
            transform=ax.transAxes, ha="left", fontsize=8.4, color=TINTA2)

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
    _eixos(ax, "A divergência com o Netuno 4, explicada até o resíduo", "",
           "erro médio absoluto (pontos percentuais)")
    ax.set_ylim(0, 3.3)
    # A leitura dos passos fica na legenda da figura: dentro do desenho,
    # qualquer bloco de texto encobre uma das barras.
    fig.tight_layout()
    _salvar(fig, "fig25_cascata.png")


def main():
    print("figuras da decisão:")
    figura_investimento()
    figura_topsis()
    figura_smaa()
    figura_tornado()
    figura_cascata()


if __name__ == "__main__":
    main()
