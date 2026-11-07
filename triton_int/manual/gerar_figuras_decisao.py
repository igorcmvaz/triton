# -*- coding: utf-8 -*-
"""Figuras da decisão: investimento, multicritério, sensibilidade e verificação.

Cinco figuras para a parte do manual que mais depende de números e menos se
deixa ler em tabela: de que é feito o investimento, como o TOPSIS mede distância
até o ideal, o que a análise estocástica diz sobre a estabilidade da escolha,
qual variável mais move o resultado econômico, e de que se compõe a divergência
entre o programa e uma regra de referência.

Executar a partir da raiz do programa:
    python manual/gerar_figuras_decisao.py
"""

from __future__ import annotations

import os
os.environ["TRITON_EDITION"] = "INT"

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
    CAMPOS_NOVA_YORK, CUSTOS_TUTORIAL, MANUTENCAO_TUTORIAL, TARIFA_TUTORIAL, TUTORIAL, VOLUME,
    _config_economica, _config_projeto, _config_tutorial, _serie,
)

from triton.core.simulation import run_single_simulation          # noqa: E402

VOLUMES = (1000, 2000, 3000, 4000, 5000, 8000, 12000)
MATERIAL = "PEAD"


def _candidatos():
    """Os seis volumes do capítulo multicritério, com os sete critérios."""
    from triton.core.economic import run_economic_analysis
    from triton.core.environmental import EnvironmentalConfig, calculate_lca
    from triton.core.topsis import TopsisCandidate

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

def rubricas_do_investimento(volume_l, material=MATERIAL):
    """As parcelas do investimento inicial, na definição do próprio programa.

    A soma fecha com ``capex_total`` da análise econômica: o CAPEX é a soma da
    cisterna, da caixa superior, da mão de obra, da tubulação, dos acessórios,
    das motobombas e do que a linha de tratamento acrescenta por cima da verba
    de filtração já embutida nos acessórios (triton/core/economic.py e
    triton/core/etap_integration.py). A versão anterior desta figura abria só
    cinco rubricas e não fechava com o investimento do tutorial.
    """
    from triton.core.etap_integration import capex_incremental_da_etap
    from triton.core.economic import run_economic_analysis

    from gerar_tabelas import _config_economica, _config_projeto

    cfg = _config_economica(volume_l, material)
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=float(volume_l),
                              **_config_projeto())
    etap = capex_incremental_da_etap(cfg, r.annual_pluvial_consumed_m3, r)
    valores = [
        cfg.cost_lower_tank, cfg.cost_upper_tank, cfg.cost_labor, cfg.cost_piping,
        cfg.cost_accessories, cfg.pump_unit_cost * cfg.pump_count, etap,
    ]
    return valores, run_economic_analysis(cfg, r).capex_total


def figura_investimento():
    """O CAPEX aberto por rubrica, em três volumes de reservatório (US$ ilustrativos)."""
    volumes = (2000, int(VOLUME), 12000)
    rubricas = [
        ("lower cistern", AZUL),
        ("header tank", "#4a90c4"),
        ("labour", LARANJA),
        ("piping", VERDE),
        ("accessories", ROXO),
        ("pump unit (duty & standby)", "#8a8880"),
        ("treatment train beyond base allowance", "#c2b59b"),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    rotulos, totais = [], []
    for i, v in enumerate(volumes):
        valores, _ = rubricas_do_investimento(v)
        base = 0.0
        for (nome, cor), valor in zip(rubricas, valores):
            ax.bar(i, valor, 0.5, bottom=base, color=cor, zorder=3,
                   edgecolor=SUPERFICIE, linewidth=2.0,
                   label=nome if i == 0 else None)
            if valor > 900:
                ax.text(i, base + valor / 2.0,
                        f"{valor:,.0f}",
                        ha="center", va="center", fontsize=8.0, color="#ffffff")
            base += valor
        total = base
        totais.append(total)
        rotulos.append(f"{v / 1000.0:.0f} m³" + "\n" +
                       f"US$ {total:,.0f}")

    _eixos(ax, "", "", "initial investment (US$, illustrative)")
    ax.set_xticks(range(len(volumes)))
    ax.set_xticklabels(rotulos, fontsize=9.0)
    ax.set_xlim(-0.6, len(volumes) - 0.4)
    teto = 2000.0 * np.ceil(max(totais) * 1.04 / 2000.0)
    ax.set_ylim(0, teto)
    ax.set_yticks(np.arange(0, teto + 1, 2000))
    ax.set_yticklabels([f"{v:,.0f}" for v in np.arange(0, teto + 1, 2000)])
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
    from triton.core.mcdm_methods import run_smaa_analysis

    cands = _candidatos()
    res = run_smaa_analysis(cands, num_samples=5000, random_seed=42)
    probs = np.asarray(res.first_rank_probs, dtype=float)
    rotulos = [f"{c.lower_tank_vol / 1000.0:.0f} m³" for c in cands]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    melhor = int(np.argmax(probs))
    cores = [ROXO if i == melhor else AZUL for i in range(len(probs))]
    ax.bar(rotulos, probs, color=cores, width=0.55, zorder=3)
    for i, p in enumerate(probs):
        if p >= 1.0:
            ax.text(i, p + 1.5, f"{p:.1f}%", ha="center",
                    fontsize=8.6, color=TINTA)

    _eixos(ax, "", "tank storage volume",
           "first-rank acceptability b¹ (%)")
    ax.set_ylim(0, 60)
    ax.set_yticks(range(0, 61, 10))

    fig.tight_layout()
    _salvar(fig, "fig23_smaa.png")


# ══════════════════════════════════════════════════════════════════════════════
# O tornado: que variável move o resultado
# ══════════════════════════════════════════════════════════════════════════════

def base_do_tornado():
    """O caso-base da análise de sensibilidade, numa definição só.

    A figura do manual e a figura interativa do site leem daqui, para não
    divergirem numa premissa. A tarifa é a de Nova York (água por m³ e esgoto a
    159% da água); os custos e os reajustes são os ilustrativos do tutorial.
    """
    from triton.core.economic import run_robust_economic_analysis
    from triton.core.etap_integration import (
        capex_incremental_da_etap, opex_anual_incremental_da_etap,
    )
    from triton.core.pump_energy import compute_annual_pump_energy

    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=VOLUME,
                              **_config_projeto())
    cfg = _config_economica(VOLUME, "CONCRETO")
    agua_m3 = float(TARIFA_TUTORIAL[1][2])                       # a faixa aberta de Nova York
    esgoto_m3 = agua_m3 * float(CAMPOS_NOVA_YORK["sewage_rate"]) / 100.0
    reajuste = CUSTOS_TUTORIAL["water_tariff_escalation"] / 100.0
    base = dict(
        # O investimento e o custeio incluem a linha de tratamento com o
        # descarte físico, como a análise econômica completa do tutorial.
        initial_investment=(cfg.cost_lower_tank + cfg.cost_upper_tank + cfg.cost_labor +
                            cfg.pump_unit_cost * cfg.pump_count +
                            cfg.cost_piping + cfg.cost_accessories +
                            capex_incremental_da_etap(cfg, None, r)),
        annual_water_saved_m3=r.annual_pluvial_consumed_m3,
        water_tariff_per_m3=agua_m3,
        sewage_tariff_per_m3=esgoto_m3,
        sewage_mode=1,
        water_tariff_escalation_rate=reajuste,
        sewage_tariff_escalation_rate=CUSTOS_TUTORIAL["sewage_tariff_escalation"] / 100.0,
        elec_tariff_escalation_rate=CUSTOS_TUTORIAL["elec_tariff_escalation"] / 100.0,
        # A interface do programa pede TMA e inflação ao mês; o modelo anual
        # pede as taxas equivalentes ao ano, e é a conversão que as iguala.
        inflation_rate=(1.0 + CUSTOS_TUTORIAL["inflation"] / 100.0) ** 12 - 1.0,
        discount_rate=(1.0 + CUSTOS_TUTORIAL["tma"] / 100.0) ** 12 - 1.0,
        annual_om_cost_base=(sum(m[2] for m in MANUTENCAO_TUTORIAL) +
                             opex_anual_incremental_da_etap(cfg, None, r)),
        # A energia do recalque, pela mesma função do econômico. Sem estes três
        # campos valiam os padrões da função, 0,75 kW por 150 h.
        pump_power_kw=compute_annual_pump_energy(cfg, r).annual_kwh,
        pump_hours_year=1.0,
        elec_tariff_kwh=cfg.elec_tariff,
        analysis_period_years=CUSTOS_TUTORIAL["analysis_period_years"],
    )
    return base


#: Os rótulos que o núcleo devolve, em inglês e sem moeda: o valor em dinheiro é sempre US$ ilustrativo.
ROTULOS_DO_TORNADO = {
    "Tarifa de Água (R$/m³)": "Water tariff",
    "Investimento Inicial (CAPEX)": "Initial investment (CAPEX)",
    "Volume de Água Pluvial Captada": "Harvested rainwater volume",
    "Reajuste Tarifário Água": "Water tariff escalation",
    "Custos de O&M": "O&M costs",
    "TMA (Taxa de Desconto)": "Discount rate (MARR)",
    "Taxa de Inflação": "Inflation rate",
    "Tarifa de Esgoto (R$/m³)": "Sewer tariff",
    "Reajuste Tarifário Energia": "Electricity tariff escalation",
    "Período de Análise (anos)": "Analysis period (years)",
}


def figura_tornado():
    from triton.core.economic import run_robust_economic_analysis, run_sensitivity_analysis

    base = base_do_tornado()
    vpl_base = run_robust_economic_analysis(**base).vpl
    curvas = run_sensitivity_analysis(base, variations_pct=[-30.0, 30.0])

    # A cor identifica a variação aplicada, e não o sinal do efeito: é o que
    # deixa ver que aumentar a TMA reduz o VPL, e não o contrário.
    itens = []
    for rotulo, curva in curvas.items():
        por_variacao = {round(p): v for p, v in curva}
        itens.append((ROTULOS_DO_TORNADO.get(rotulo, rotulo), por_variacao[-30] - vpl_base,
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
    _eixos(ax, "", "NPV variation relative to the base case (US$, illustrative)", "")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=VERDE, label="assumption +30%"),
                       Patch(facecolor=LARANJA, label="assumption −30%")],
              frameon=False, fontsize=8.4, loc="lower right")
    marcas = ax.get_xticks()
    ax.set_xticks(marcas)
    ax.set_xticklabels([f"{v:,.0f}".replace("-", "−")
                        for v in marcas])

    fig.tight_layout()
    _salvar(fig, "fig24_tornado.png")


# ══════════════════════════════════════════════════════════════════════════════
# A divergência entre o programa e uma regra de referência, decomposta
# ══════════════════════════════════════════════════════════════════════════════

#: A grade grossa de uma ferramenta de referência: o volume «ideal» sai do primeiro múltiplo de 5.000 L
#: cujo ganho marginal cai a 1 %/m³ ou menos (o mesmo limiar do tutorial, numa grade diferente).
PASSO_DA_REFERENCIA_L = 5000.0
LIMIAR_DO_TUTORIAL = 1.0


def _balanco_independente(serie, volume_l, descarte_mm, limiar):
    """Um balanço diário escrito à parte, sem o motor, para medir o resíduo.

    Ordem do dia como a do capítulo do balanço diário: capta, extravasa o que passa da capacidade,
    depois consome da demanda pluvial. ``limiar`` escolhe a regra do descarte: falso, a lâmina é
    subtraída da chuva do dia (a regra do programa); verdadeiro, abaixo da lâmina não se capta nada e
    acima dela capta-se a chuva inteira (a regra de limiar de outras ferramentas).
    """
    t = TUTORIAL
    demanda = t["moradores"] * t["per_capita"] * t["rainwater_share"]
    nivel, consumido = 0.0, 0.0
    for p in serie:
        p = float(p)
        if limiar:
            efetiva = p if p >= descarte_mm else 0.0
        else:
            efetiva = max(0.0, p - descarte_mm)
        nivel += efetiva * t["area"] * t["runoff_coeff"]
        nivel = min(nivel, volume_l)
        uso = min(nivel, demanda)
        nivel -= uso
        consumido += uso
    return 100.0 * consumido / (t["moradores"] * t["per_capita"] * len(serie))


def divergencia_decomposta():
    """Os quatro valores da figura: total, critério do volume, regra do descarte e resíduo (pontos).

    A «ferramenta de referência» é emulada: regra de limiar para a lâmina de descarte e volume ideal
    escolhido numa grade de 5.000 L; o balanço dela é o balanço diário independente. Cada passo
    retira da divergência média absoluta (três cidades) uma diferença de método declarada.
    """
    from gerar_tabelas import CIDADES_GUIA14

    cfg = _config_tutorial()
    d = TUTORIAL["discard_mm"]
    total, mesmo_volume, sem_descarte = [], [], []
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
        programa = lambda v, desc: run_single_simulation(          # noqa: E731
            precip_data=serie, lower_tank_vol=float(v),
            **{**cfg, "discard_mm": desc}).potential_potable_savings_pct
        # o volume do programa: o primeiro da grade de 1.000 L cujo ganho cai ao limiar
        pots = [programa(v, d) for v in range(0, 20001, 1000)]
        v_prog = next(1000.0 * i for i in range(1, len(pots)) if pots[i] - pots[i - 1] <= LIMIAR_DO_TUTORIAL)
        # o volume da referência: a mesma regra de limiar, numa grade de 5.000 L
        ref = [_balanco_independente(serie, v, d, True)
               for v in np.arange(0.0, 20001.0, PASSO_DA_REFERENCIA_L)]
        passo_m3 = PASSO_DA_REFERENCIA_L / 1000.0
        v_ref = next(PASSO_DA_REFERENCIA_L * i for i in range(1, len(ref))
                     if (ref[i] - ref[i - 1]) / passo_m3 <= LIMIAR_DO_TUTORIAL)
        p_prog = programa(v_prog, d)
        total.append(abs(p_prog - _balanco_independente(serie, v_ref, d, True)))
        mesmo_volume.append(abs(p_prog - _balanco_independente(serie, v_prog, d, True)))
        # sem descarte as duas regras coincidem: o que sobra é o balanço do motor contra o independente
        sem_descarte.append(abs(programa(v_prog, 0.0) - _balanco_independente(serie, v_prog, 0.0, False)))
    media = lambda x: float(np.mean(x))                             # noqa: E731
    return media(total), media(mesmo_volume), media(sem_descarte)


def figura_cascata():
    """De cada passo da divergência até o resíduo do balanço hídrico."""
    t, m, r = divergencia_decomposta()
    passos = [
        ("total\ndivergence", t, AZUL),
        ("volume\ncriterion", -(t - m), LARANJA),
        ("first-flush\nrule", -(m - r), LARANJA),
        ("water balance\nresidual", r, VERDE),
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
        ax.text(i, max(topo, base, base - valor if 0 < i < len(passos) - 1 else 0.0) + 0.03 * t,
                f"{abs(valor):.2f} pp", ha="center",
                fontsize=9.0, color=TINTA)

    ax.set_xticks(range(len(passos)))
    ax.set_xticklabels([p[0] for p in passos], fontsize=8.4)
    _eixos(ax, "", "", "mean absolute difference (percentage points)")
    teto = max(0.5, float(np.ceil(t * 1.25 * 2.0) / 2.0))
    ax.set_ylim(0, teto)
    ax.set_yticks(np.arange(0, teto + 0.01, 0.5))
    ax.set_yticklabels([f"{v:.1f}" for v in np.arange(0, teto + 0.01, 0.5)])
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
