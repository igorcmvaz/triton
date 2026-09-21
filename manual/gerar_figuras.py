# -*- coding: utf-8 -*-
"""Gera as figuras do manual, rodando o próprio programa.

Nenhuma figura é desenhada à mão: todas saem da simulação com os dados declarados
em `manual/gerar_tabelas.py`, de modo que uma correção no motor apareça no manual na
mesma alteração.

Executar a partir da raiz do programa:
    python manual/gerar_figuras.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np                # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_desenhos import rotulo_de_painel  # noqa: E402
from gerar_tabelas import (
    VOLUME, _config_projeto,
    CHUVA_23, CIDADES_GUIA14, NOMES_CIDADES, VOLUMES_VARREDURA,
    _config_tutorial, _serie,
)

from netuno.core.parser import load_precipitation      # noqa: E402
from netuno.core.simulation import run_single_simulation  # noqa: E402

# Paleta única do manual, a mesma de docs/gerar_figuras.py.
AZUL = "#2a78d6"
LARANJA = "#eb6834"
VERDE = "#0ca30c"
ROXO = "#7d5fb0"
TINTA = "#0b0b0b"
TINTA2 = "#52514e"
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"
SUPERFICIE = "#fcfcfb"

FIGURAS = Path(__file__).parent / "figuras"
FIGURAS.mkdir(exist_ok=True)


def teto_multiplo(valor, passo):
    """O menor múltiplo de «passo» que não fica abaixo de «valor».

    Os eixos começam em zero e terminam num número redondo da própria
    grandeza: 500 mm para chuva anual, 2,5 dias para sequências.
    """
    import math
    return passo * max(1, math.ceil(valor / passo - 1e-9))


def _teto_500(valor):
    return teto_multiplo(valor, 500.0)


def _eixos(ax, titulo, x, y):
    rotulo_de_painel(ax, titulo)
    ax.set_xlabel(x, color=TINTA2, fontsize=9)
    ax.set_ylabel(y, color=TINTA2, fontsize=9)
    ax.grid(True, color=GRADE, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(EIXO)
    ax.tick_params(colors=TINTA2, labelsize=8.5)


def _salvar(fig, nome):
    caminho = FIGURAS / nome
    fig.savefig(caminho, dpi=160, bbox_inches="tight", facecolor=SUPERFICIE)
    plt.close(fig)
    print(f"  {caminho.relative_to(Path(__file__).parent)}")


# ── figura 1: o balanço dos dez dias, capítulo 23 ────────────────────────────
def figura_dez_dias():
    r = run_single_simulation(
        precip_data=np.array(CHUVA_23, dtype=float), lower_tank_vol=2000.0,
        area=100.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
        total_demand_per_day=200.0, rainwater_share=0.40, store_daily_details=True)
    dias = np.arange(1, len(r.daily_results) + 1)
    captado = [d.harvested_liters for d in r.daily_results]
    extrav = [d.spilled_liters for d in r.daily_results]
    nivel = [d.lower_tank_end_liters for d in r.daily_results]

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.4), sharex=True,
                                 gridspec_kw={"height_ratios": [1, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    # Sem títulos soltos sobre os painéis: a identificação é (a) e (b), e o que
    # cada painel mostra fica na legenda da figura, como pede a ABNT.
    def _teto_500(valor):
        return 500.0 * int(np.ceil((float(valor) + 1e-9) / 500.0))

    a1.bar(dias, captado, color=AZUL, width=0.62, zorder=3, label="volume captado")
    a1.bar(dias, extrav, color=LARANJA, width=0.62, zorder=4, label="volume extravasado")
    _eixos(a1, "", "", "volume (L)")
    a1.set_ylim(0, _teto_500(max(captado)))
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")
    a1.set_title("(a)", color=TINTA, fontsize=10, fontweight="bold", loc="left", pad=6)

    a2.plot(dias, nivel, color=ROXO, linewidth=2.0, marker="o", markersize=4.5, zorder=3)
    a2.axhline(2000.0, color=EIXO, linestyle="--", linewidth=1.0, zorder=2)
    a2.text(10.1, 2000.0, "capacidade", color=TINTA2, fontsize=8, va="center")
    _eixos(a2, "", "dia", "volume armazenado (L)")
    a2.set_ylim(0, _teto_500(max(max(nivel), 2000.0) + 1.0))
    a2.set_title("(b)", color=TINTA, fontsize=10, fontweight="bold", loc="left", pad=6)
    a2.set_xticks(dias)

    fig.tight_layout()
    _salvar(fig, "fig01_dez_dias.png")


# ── figura 2: a curva de retorno decrescente, capítulo 7 ─────────────────────
def figura_curva():
    serie = _serie()
    cfg = _config_tutorial()
    vols, pots = [], []
    for v in VOLUMES_VARREDURA:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg)
        vols.append(v / 1000.0)
        pots.append(r.potential_potable_savings_pct)

    marg = [0.0] + [
        (pots[i] - pots[i - 1]) / (vols[i] - vols[i - 1]) for i in range(1, len(vols))
    ]

    # Empilhados, e não lado a lado: uma folha de 9 polegadas reduzida à
    # largura da página encolhe junto a fonte dos eixos.
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True)
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.plot(vols, pots, color=AZUL, linewidth=2.2, marker="o", markersize=4.5, zorder=3)
    a1.axhline(40.0, color=LARANJA, linestyle="--", linewidth=1.2, zorder=2)
    a1.text(0.4, 41.0, "fração atendível (teto)", color=LARANJA, fontsize=8.5,
            va="bottom")
    a1.axvline(5.0, color=VERDE, linestyle=":", linewidth=1.4, zorder=2)
    a1.text(5.3, 8.0, "volume ideal", color=VERDE, fontsize=8.5)
    _eixos(a1, "(a)", "", "potencial de economia (%)")
    a1.set_ylim(0, 46)

    a2.plot(vols[1:], marg[1:], color=LARANJA, linewidth=2.2, marker="o",
            markersize=4.5, zorder=3)
    a2.axhline(1.0, color=VERDE, linestyle="--", linewidth=1.2, zorder=2)
    a2.text(12.0, 1.9, "limiar de 1 %/m³", color=VERDE, fontsize=8.5)
    _eixos(a2, "(b)", "volume do reservatório (m³)", "ganho marginal (%/m³)")
    a2.set_yscale("log")

    fig.tight_layout()
    _salvar(fig, "fig02_curva_de_retorno.png")


# ── figura 3: regime de chuva contra potencial, guia 14 ──────────────────────
def figura_cidades():
    cfg = _config_tutorial()
    nomes, lamina, potencial = [], [], []
    for chave in CIDADES_GUIA14:
        caminho = RAIZ / "data" / "rainfall" / f"{chave}.csv"
        if not caminho.exists():
            continue
        serie = load_precipitation(str(caminho))[: 30 * 365]
        anos = len(serie) / 365.25
        r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME, **cfg)
        nomes.append(NOMES_CIDADES.get(chave, chave))
        lamina.append(serie.sum() / anos)
        potencial.append(r.potential_potable_savings_pct)

    # Dois painéis com uma escala cada, e não um eixo duplo: com duas escalas
    # no mesmo gráfico a altura relativa das barras não significa nada.
    x = np.arange(len(nomes))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True)
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.bar(x, lamina, width=0.5, color=AZUL, zorder=3)
    for i, v in enumerate(lamina):
        a1.text(i, v + 40, f"{v:,.0f}".replace(",", "."), ha="center",
                va="bottom", fontsize=8.2, color=TINTA2)
    _eixos(a1, "(a)", "", "precipitação anual (mm)")
    a1.set_ylim(0, _teto_500(max(lamina) * 1.08))
    a1.set_yticks(range(0, int(_teto_500(max(lamina) * 1.08)) + 1, 500))
    a1.set_yticklabels([f"{v:,}".replace(",", ".") for v in
                        range(0, int(_teto_500(max(lamina) * 1.08)) + 1, 500)])

    a2.bar(x, potencial, width=0.5, color=LARANJA, zorder=3)
    for i, v in enumerate(potencial):
        a2.text(i, v + 0.8, f"{v:.1f}".replace(".", ","), ha="center",
                va="bottom", fontsize=8.2, color=TINTA2)
    _eixos(a2, "(b)", "", "potencial de economia (%)")
    a2.set_ylim(0, 50)
    a2.set_yticks(range(0, 51, 10))
    a2.set_xticks(x)
    a2.set_xticklabels(nomes)

    fig.tight_layout()
    _salvar(fig, "fig03_cidades.png")


# ── figura 4: o material decide o sinal do carbono, capítulo 11 ──────────────
def figura_materiais():
    from netuno.core.environmental import (
        MATERIAL_PRESETS, EnvironmentalConfig, calculate_lca)

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3
    nomes = {"PEAD": "Polietileno", "CONCRETO": "Concreto",
             "FIBRA": "Fibra de vidro", "ACO_INOX": "Aço inox"}
    rot, saldo = [], []
    for k in MATERIAL_PRESETS:
        from gerar_tabelas import _config_ambiental
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        rot.append(nomes.get(k, k))
        saldo.append(calculate_lca(VOLUME, m3, cfg).lifetime_net_co2_saved_kg)

    cores = [VERDE if s > 0 else LARANJA for s in saldo]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.bar(rot, saldo, color=cores, width=0.55, zorder=3)
    ax.axhline(0.0, color=TINTA, linewidth=1.2, zorder=4)
    _eixos(ax, "", "", "saldo de carbono em 20 anos (kg CO₂e)")
    for i, s in enumerate(saldo):
        ax.text(i, s + (40 if s > 0 else -80), f"{s:+,.0f}".replace(",", "."),
                ha="center", color=TINTA2, fontsize=8.5)
    fig.tight_layout()
    _salvar(fig, "fig04_materiais.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figura: como a conta responde à economia, nos cinco regimes
# ══════════════════════════════════════════════════════════════════════════════

def figura_regimes():
    """A conta de água contra o consumo, em três regimes de mínimo.

    É o conceito que mais decide a viabilidade de um sistema pluvial no Brasil,
    e o mais difícil de transmitir em prosa: o que muda não é o preço, é o
    formato da curva.
    """
    from netuno.core.economic import calculate_water_bill

    # As três estruturas são reais: Florianópolis pratica disponibilidade e
    # Floriano pratica franquia no mínimo. A terceira é a mesma de Floriano sem
    # a franquia, para isolar o efeito dela.
    disponibilidade = [(0.0, 0.0, 46.34, -1), (0.0, 10.0, 3.08, 1),
                       (10.0, 25.0, 14.31, 1), (25.0, 50.0, 19.14, 1),
                       (50.0, 999999.0, 24.08, 1)]
    franquia = [(0.0, 0.0, 52.89, -1), (0.0, 10.0, 0.0, 1),
                (10.0, 15.0, 9.815, 1), (15.0, 20.0, 10.917, 1),
                (20.0, 999999.0, 12.8, 1)]
    sem_minimo = [(0.0, 10.0, 5.29, 1), (10.0, 15.0, 9.815, 1),
                  (15.0, 20.0, 10.917, 1), (20.0, 999999.0, 12.8, 1)]

    consumos = np.arange(0.0, 25.5, 0.5)
    curvas = [
        ("tarifa de disponibilidade", disponibilidade, AZUL),
        ("franquia no mínimo", franquia, LARANJA),
        ("sem valor mínimo", sem_minimo, VERDE),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    for rotulo, tarifa, cor in curvas:
        contas = [calculate_water_bill(c * 1000.0, tarifa, 1, 0.0, 0.0, 0.0)
                  for c in consumos]
        ax.plot(consumos, contas, color=cor, linewidth=2.2, zorder=3,
                label=rotulo)

    # A faixa em que a economia não desconta nada, no regime de franquia.
    ax.axvspan(0, 10, color=LARANJA, alpha=0.07, zorder=1)
    # O rótulo fica acima das três curvas no trecho da franquia, que é a faixa
    # de consumo entre zero e dez metros cúbicos.
    ax.text(5.0, 100.0, "franquia\n(0 a 10 m³)",
            ha="center", va="bottom", fontsize=8.0, color=LARANJA)

    # Só a parcela de água: o esgoto é percentual dela e multiplica a curva,
    # sem mudar o formato, que é o que a figura tem a mostrar.
    _eixos(ax, "", "consumo mensal (m³)",
           "parcela de água da fatura mensal (R$)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 300)
    ax.set_yticks(range(0, 301, 50))

    fig.tight_layout()
    _salvar(fig, "fig05_regimes.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figura: o retorno de carbono ao longo da vida útil
# ══════════════════════════════════════════════════════════════════════════════

def figura_carbono_no_tempo():
    """O saldo de carbono acumulado, ano a ano, por material da cisterna."""
    from netuno.core.environmental import (
        EnvironmentalConfig, calculate_lca)

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3

    materiais = [("PEAD", "Polietileno", VERDE),
                 ("CONCRETO", "Concreto", LARANJA)]
    anos = np.arange(0, 21)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    for chave, rotulo, cor in materiais:
        from gerar_tabelas import _config_ambiental
        cfg = _config_ambiental(r)
        cfg.lower_material_key = chave
        lca = calculate_lca(VOLUME, m3, cfg)
        saldo = [lca.net_annual_avoided_co2_kg * a - lca.total_embodied_co2_kg
                 for a in anos]
        ax.plot(anos, saldo, color=cor, linewidth=2.4, zorder=3, label=rotulo)
        # O ponto em que a curva cruza o zero é o retorno ambiental.
        if lca.net_annual_avoided_co2_kg > 0:
            cruzamento = lca.total_embodied_co2_kg / lca.net_annual_avoided_co2_kg
            if cruzamento <= 20:
                ax.plot([cruzamento], [0], "o", color=cor, markersize=7,
                        zorder=4)
                ax.annotate(f"{cruzamento:.1f} anos".replace(".", ","),
                            xy=(cruzamento, 0), xytext=(cruzamento + 0.6, 120),
                            fontsize=8.5, color=cor,
                            arrowprops=dict(arrowstyle="-", color=cor,
                                            linewidth=0.9))

    ax.axhline(0.0, color=TINTA, linewidth=1.2, zorder=2)
    _eixos(ax, "", "anos de operação", "saldo de carbono acumulado (kg CO₂e)")
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_xlim(0, 20)

    fig.tight_layout()
    _salvar(fig, "fig06_carbono_no_tempo.png")


def main():
    print("figuras do manual:")
    figura_dez_dias()
    figura_curva()
    figura_cidades()
    figura_materiais()
    figura_regimes()
    figura_carbono_no_tempo()


if __name__ == "__main__":
    main()
