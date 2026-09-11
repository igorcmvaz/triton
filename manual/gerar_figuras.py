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
from gerar_tabelas import (       # noqa: E402
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


def _eixos(ax, titulo, x, y):
    ax.set_title(titulo, color=TINTA, fontsize=11, loc="left", pad=12)
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

    a1.bar(dias, captado, color=AZUL, width=0.62, zorder=3, label="captado")
    a1.bar(dias, extrav, color=LARANJA, width=0.62, zorder=4, label="extravasado")
    _eixos(a1, "Captação e extravasamento, dia a dia", "", "litros")
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")

    a2.plot(dias, nivel, color=ROXO, linewidth=2.0, marker="o", markersize=4.5, zorder=3)
    a2.axhline(2000.0, color=EIXO, linestyle="--", linewidth=1.0, zorder=2)
    a2.text(10.1, 2000.0, "capacidade", color=TINTA2, fontsize=8, va="center")
    _eixos(a2, "Volume armazenado ao fim de cada dia", "dia", "litros")
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

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.plot(vols, pots, color=AZUL, linewidth=2.2, marker="o", markersize=4.5, zorder=3)
    a1.axhline(40.0, color=LARANJA, linestyle="--", linewidth=1.2, zorder=2)
    a1.text(0.4, 41.0, "teto: a fração atendível", color=LARANJA, fontsize=8.5,
            va="bottom")
    a1.axvline(5.0, color=VERDE, linestyle=":", linewidth=1.4, zorder=2)
    a1.text(5.3, 8.0, "volume ideal", color=VERDE, fontsize=8.5)
    _eixos(a1, "Potencial de economia", "volume do reservatório (m³)", "%")
    a1.set_ylim(0, 46)

    a2.plot(vols[1:], marg[1:], color=LARANJA, linewidth=2.2, marker="o",
            markersize=4.5, zorder=3)
    a2.axhline(1.0, color=VERDE, linestyle="--", linewidth=1.2, zorder=2)
    a2.text(12.0, 1.9, "limiar de 1 %/m³", color=VERDE, fontsize=8.5)
    _eixos(a2, "Ganho por m³ acrescentado", "volume do reservatório (m³)", "%/m³")
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
        r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0, **cfg)
        nomes.append(NOMES_CIDADES.get(chave, chave))
        lamina.append(serie.sum() / anos)
        potencial.append(r.potential_potable_savings_pct)

    x = np.arange(len(nomes))
    fig, a1 = plt.subplots(figsize=(7.2, 3.8))
    fig.patch.set_facecolor(SUPERFICIE)
    a1.set_facecolor(SUPERFICIE)

    a1.bar(x - 0.19, lamina, width=0.36, color=AZUL, zorder=3, label="chuva anual (mm)")
    _eixos(a1, "Chove mais não significa render mais", "", "mm por ano")
    a1.set_xticks(x)
    a1.set_xticklabels(nomes)

    a2 = a1.twinx()
    a2.bar(x + 0.19, potencial, width=0.36, color=LARANJA, zorder=3,
           label="potencial de economia (%)")
    a2.set_ylabel("potencial de economia (%)", color=TINTA2, fontsize=9)
    a2.tick_params(colors=TINTA2, labelsize=8.5)
    for lado in ("top", "left"):
        a2.spines[lado].set_visible(False)
    a2.spines["right"].set_color(EIXO)
    a2.set_ylim(0, 46)

    linhas = a1.get_legend_handles_labels()[0] + a2.get_legend_handles_labels()[0]
    rotulos = a1.get_legend_handles_labels()[1] + a2.get_legend_handles_labels()[1]
    a1.legend(linhas, rotulos, frameon=False, fontsize=8.5, loc="upper center",
              bbox_to_anchor=(0.5, -0.08), ncol=2)

    fig.tight_layout()
    _salvar(fig, "fig03_cidades.png")


# ── figura 4: o material decide o sinal do carbono, capítulo 11 ──────────────
def figura_materiais():
    from netuno.core.environmental import (
        MATERIAL_PRESETS, EnvironmentalConfig, calculate_lca)

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=5000.0,
                              **_config_tutorial())
    m3 = r.annual_pluvial_consumed_m3
    nomes = {"PEAD": "Polietileno", "CONCRETO": "Concreto",
             "FIBRA": "Fibra de vidro", "ACO_INOX": "Aço inox"}
    rot, saldo = [], []
    for k in MATERIAL_PRESETS:
        cfg = EnvironmentalConfig()
        cfg.lower_material_key = k
        rot.append(nomes.get(k, k))
        saldo.append(calculate_lca(5000.0, m3, cfg).lifetime_net_co2_saved_kg)

    cores = [VERDE if s > 0 else LARANJA for s in saldo]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.bar(rot, saldo, color=cores, width=0.55, zorder=3)
    ax.axhline(0.0, color=TINTA, linewidth=1.2, zorder=4)
    _eixos(ax, "Saldo de carbono em 20 anos, cisterna de 5.000 L", "", "kg CO₂e")
    for i, s in enumerate(saldo):
        ax.text(i, s + (40 if s > 0 else -80), f"{s:+,.0f}".replace(",", "."),
                ha="center", color=TINTA2, fontsize=8.5)
    fig.tight_layout()
    _salvar(fig, "fig04_materiais.png")


def main():
    print("figuras do manual:")
    figura_dez_dias()
    figura_curva()
    figura_cidades()
    figura_materiais()


if __name__ == "__main__":
    main()
