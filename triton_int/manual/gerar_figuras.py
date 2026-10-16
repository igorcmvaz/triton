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
os.environ["TRITON_EDITION"] = "INT"

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
    CHUVA_23, CIDADES_GUIA14, NOMES_CIDADES, TUTORIAL, VOLUMES_VARREDURA,
    _config_tutorial, _serie,
)

from triton.core.parser import load_precipitation      # noqa: E402
from triton.core.simulation import run_single_simulation  # noqa: E402

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

    a1.bar(dias, captado, color=AZUL, width=0.62, zorder=3, label="harvested volume")
    a1.bar(dias, extrav, color=LARANJA, width=0.62, zorder=4, label="spilled volume")
    _eixos(a1, "", "", "volume (L)")
    a1.set_ylim(0, _teto_500(max(captado)))
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")
    a1.set_title("(a)", color=TINTA, fontsize=10, fontweight="bold", loc="left", pad=6)

    a2.plot(dias, nivel, color=ROXO, linewidth=2.0, marker="o", markersize=4.5, zorder=3)
    a2.axhline(2000.0, color=EIXO, linestyle="--", linewidth=1.0, zorder=2)
    a2.text(10.1, 2000.0, "capacity", color=TINTA2, fontsize=8, va="center")
    _eixos(a2, "", "day", "stored volume (L)")
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

    teto_pct = TUTORIAL["rainwater_share"] * 100.0           # fração atendível: o teto do potencial
    # O volume ideal pelo limiar de 1 %/m³: o primeiro volume da varredura cujo ganho cai a esse valor.
    ideal = next((vols[i] for i in range(1, len(vols)) if marg[i] <= 1.0), vols[-1])
    a1.plot(vols, pots, color=AZUL, linewidth=2.2, marker="o", markersize=4.5, zorder=3)
    a1.axhline(teto_pct, color=LARANJA, linestyle="--", linewidth=1.2, zorder=2)
    a1.text(0.4, teto_pct + 0.8, f"suppliable fraction ({teto_pct:.0f}%, ceiling)",
            color=LARANJA, fontsize=8.5, va="bottom")
    a1.axvline(ideal, color=VERDE, linestyle=":", linewidth=1.4, zorder=2)
    a1.text(ideal + 0.3, 6.0, f"optimal volume\n({ideal:.0f} m³)", color=VERDE, fontsize=8.5)
    _eixos(a1, "(a)", "", "savings potential (%)")
    a1.set_ylim(0, 34)

    a2.plot(vols[1:], marg[1:], color=LARANJA, linewidth=2.2, marker="o",
            markersize=4.5, zorder=3)
    a2.axhline(1.0, color=VERDE, linestyle="--", linewidth=1.2, zorder=2)
    a2.text(12.0, 1.35, "1 %/m³ threshold", color=VERDE, fontsize=8.5)
    _eixos(a2, "(b)", "tank volume (m³)", "marginal gain (%/m³)")
    a2.set_yscale("log")
    a2.set_xticks(range(0, 21, 2))
    a2.set_xlim(0, 21)

    fig.tight_layout()
    _salvar(fig, "fig02_curva_de_retorno.png")


# ── figura 3: regime de chuva contra potencial, guia 14 ──────────────────────
def figura_cidades():
    cfg = _config_tutorial()
    nomes, lamina, potencial = [], [], []
    for chave in CIDADES_GUIA14:
        serie = _serie(chave)
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
        a1.text(i, v + 25, f"{v:,.0f}", ha="center",
                va="bottom", fontsize=8.2, color=TINTA2)
    _eixos(a1, "(a)", "", "annual precipitation (mm)")
    teto = _teto_500(max(lamina) * 1.08)
    a1.set_ylim(0, teto)
    a1.set_yticks(range(0, int(teto) + 1, 500))
    a1.set_yticklabels([f"{v:,}" for v in range(0, int(teto) + 1, 500)])

    a2.bar(x, potencial, width=0.5, color=LARANJA, zorder=3)
    for i, v in enumerate(potencial):
        a2.text(i, v + 0.8, f"{v:.1f}", ha="center",
                va="bottom", fontsize=8.2, color=TINTA2)
    _eixos(a2, "(b)", "", "savings potential (%)")
    a2.set_ylim(0, 40)
    a2.set_yticks(range(0, 41, 10))
    a2.set_xticks(x)
    a2.set_xticklabels(nomes)

    fig.tight_layout()
    _salvar(fig, "fig03_cidades.png")


# ── figura 4: o material decide o sinal do carbono, capítulo 11 ──────────────
def figura_materiais():
    from triton.core.environmental import (
        MATERIAL_PRESETS, EnvironmentalConfig, calculate_lca)

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3
    nomes = {"PEAD": "Polyethylene", "CONCRETO": "Concrete",
             "FIBRA": "Fiberglass", "ACO_INOX": "Stainless Steel"}
    rot, saldo = [], []
    for k in MATERIAL_PRESETS:
        from gerar_tabelas import _config_ambiental
        cfg = _config_ambiental(r)
        cfg.lower_material_key = k
        rot.append(nomes.get(k, k))
        # Emissoes liquidas: o negativo do saldo, pela convencao de que
        # positivo emite.
        saldo.append(-calculate_lca(VOLUME, m3, cfg).lifetime_net_co2_saved_kg)

    cores = [VERDE if s < 0 else LARANJA for s in saldo]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.bar(rot, saldo, color=cores, width=0.55, zorder=3)
    ax.axhline(0.0, color=TINTA, linewidth=1.2, zorder=4)
    _eixos(ax, "", "", "20-year net emissions (kg CO₂e)")
    span = max(saldo) - min(min(saldo), 0.0)
    span = max(saldo) - min(min(saldo), 0.0)
    for i, s in enumerate(saldo):
        ax.text(i, s + (0.03 if s > 0 else -0.03) * span, f"{s:+,.0f}".replace("-", "−"),
                ha="center", va="bottom" if s > 0 else "top", color=TINTA2, fontsize=8.5)
    ax.set_ylim(min(saldo) - 0.16 * span, max(saldo) + 0.14 * span)
    fig.tight_layout()
    _salvar(fig, "fig04_materiais.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figura: como a conta responde à economia, nos cinco regimes
# ══════════════════════════════════════════════════════════════════════════════

#: As três estruturas hipotéticas do capítulo «Adjusting to the tariff», em unidades monetárias
#: (cu): números redondos, uma ilustração e não uma tarifa. A: franquia no valor mínimo (50 cu pelos
#: primeiros 10 m³, depois 5 cu/m³); B: tarifa de disponibilidade (40 cu mais 5 cu/m³); C: sem mínimo
#: (5 cu/m³). Cada uma na forma que o motor lê: (início, fim, valor ou preço, código).
REGIMES_HIPOTETICOS = (
    ("allowance in the minimum", [(0.0, 0.0, 50.0, -1), (0.0, 10.0, 0.0, 1),
                                  (10.0, 999999.0, 5.0, 1)]),
    ("availability charge", [(0.0, 0.0, 40.0, -1), (0.0, 999999.0, 5.0, 1)]),
    ("no minimum", [(0.0, 999999.0, 5.0, 1)]),
)


def figura_regimes():
    """A conta de água contra o consumo, em três regimes de mínimo.

    É o conceito que mais decide a viabilidade de um sistema pluvial, e o mais
    difícil de transmitir em prosa: o que muda não é o preço, é o formato da
    curva. As estruturas são hipotéticas, em unidades monetárias.
    """
    from triton.core.economic import calculate_water_bill

    consumos = np.arange(0.0, 25.5, 0.5)
    cores = (LARANJA, AZUL, VERDE)
    estilos = ("-", "-", (0, (5, 3)))

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    for (rotulo, tarifa), cor, estilo in zip(REGIMES_HIPOTETICOS, cores, estilos):
        contas = [calculate_water_bill(c * 1000.0, tarifa, 1, 0.0, 0.0, 0.0)
                  for c in consumos]
        ax.plot(consumos, contas, color=cor, linewidth=2.2, zorder=3,
                linestyle=estilo, label=rotulo)

    # A faixa em que a economia não desconta nada, no regime de franquia.
    ax.axvspan(0, 10, color=LARANJA, alpha=0.07, zorder=1)
    ax.text(5.0, 4.0, "allowance, 0 to 10 m³",
            ha="center", va="bottom", fontsize=8.0, color=LARANJA)

    # Só a parcela de água: o esgoto é percentual dela e multiplica a curva,
    # sem mudar o formato, que é o que a figura tem a mostrar.
    _eixos(ax, "", "monthly consumption (m³)",
           "water bill component (currency units, hypothetical)")
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 200)
    ax.set_yticks(range(0, 201, 50))

    fig.tight_layout()
    _salvar(fig, "fig05_regimes.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figura: o retorno de carbono ao longo da vida útil
# ══════════════════════════════════════════════════════════════════════════════

def figura_carbono_no_tempo():
    """O saldo de carbono acumulado, ano a ano, por material da cisterna."""
    from triton.core.environmental import (
        EnvironmentalConfig, calculate_lca)

    serie = _serie()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=VOLUME,
                              **_config_projeto())
    m3 = r.annual_pluvial_consumed_m3

    materiais = [("PEAD", "Polyethylene", VERDE),
                 ("CONCRETO", "Concrete", LARANJA)]
    anos = np.arange(0, 21)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    for chave, rotulo, cor in materiais:
        from gerar_tabelas import _config_ambiental
        cfg = _config_ambiental(r)
        cfg.lower_material_key = chave
        lca = calculate_lca(VOLUME, m3, cfg)
        # Emissoes liquidas acumuladas: positivo emite, negativo retira. E a
        # mesma convencao do grafico de balanco da aba ambiental do programa,
        # e a oposta da que esta figura usava ate a versao 1.0.0.
        emissoes = [lca.total_embodied_co2_kg - lca.net_annual_avoided_co2_kg * a
                    for a in anos]
        ax.plot(anos, emissoes, color=cor, linewidth=2.4, zorder=3, label=rotulo)
        # O ponto em que a curva cruza o zero é o retorno ambiental.
        if lca.net_annual_avoided_co2_kg > 0:
            cruzamento = lca.total_embodied_co2_kg / lca.net_annual_avoided_co2_kg
            if cruzamento <= 20:
                ax.plot([cruzamento], [0], "o", color=cor, markersize=7,
                        zorder=4)
                ax.annotate(f"{cruzamento:.1f} years",
                            xy=(cruzamento, 0), xytext=(cruzamento + 0.6, -120),
                            fontsize=8.5, color=cor,
                            arrowprops=dict(arrowstyle="-", color=cor,
                                            linewidth=0.9))

    ax.axhline(0.0, color=TINTA, linewidth=1.2, zorder=2)
    _eixos(ax, "", "years of operation",
           "cumulative net emissions (kg CO₂e)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax.set_xlim(0, 20)

    fig.tight_layout()
    _salvar(fig, "fig06_carbono_no_tempo.png")


# ══════════════════════════════════════════════════════════════════════════════
# Figura: a curva de otimizacao ambiental
# ══════════════════════════════════════════════════════════════════════════════

def figura_otimizacao_ambiental():
    """As emissoes liquidas em vinte anos contra o volume da cisterna.

    A figura existe para mostrar o que a intuicao corrente nega: o carbono nao
    melhora indefinidamente com mais reservacao. O carbono incorporado cresce de
    forma quase afim com o volume, enquanto a agua evitada cresce com o
    atendimento, que satura. A soma tem minimo interior.

    Dois paineis porque as escalas diferem por uma ordem de grandeza: num unico
    eixo, a curva do concreto achata justamente a inflexao do polietileno, que e
    o que a figura precisa mostrar.
    """
    from triton.core.environmental import calculate_lca
    from gerar_tabelas import _config_ambiental

    serie = _serie()
    volumes = list(range(500, 12001, 500))
    # O atendimento nao depende do material: simula uma vez por volume.
    consumo = {}
    resultados = {}
    for vol in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(vol),
                                  **_config_projeto())
        consumo[vol] = r.annual_pluvial_consumed_m3
        resultados[vol] = r

    fig, eixos = plt.subplots(1, 2, figsize=(7.2, 3.4))
    fig.patch.set_facecolor(SUPERFICIE)

    paineis = [("PEAD", "(a) polyethylene", VERDE), ("CONCRETO", "(b) concrete", LARANJA)]
    for ax, (chave, rotulo, cor) in zip(eixos, paineis):
        ax.set_facecolor(SUPERFICIE)
        emissoes = []
        for vol in volumes:
            cfg = _config_ambiental(resultados[vol])
            cfg.lower_material_key = chave
            lca = calculate_lca(float(vol), consumo[vol], cfg)
            emissoes.append(-lca.lifetime_net_co2_saved_kg)
        ax.plot([v / 1000 for v in volumes], emissoes, color=cor, linewidth=2.4,
                zorder=3)
        ax.axhline(0.0, color=TINTA, linewidth=1.0, zorder=2)

        # So marca o minimo quando ele e interior: minimo na borda nao e otimo,
        # e marca-lo sugeriria uma inflexao que nao existe.
        k = min(range(len(emissoes)), key=lambda n: emissoes[n])
        if 0 < k < len(emissoes) - 1:
            ax.plot([volumes[k] / 1000], [emissoes[k]], "o", color=cor,
                    markersize=7, zorder=5)
            faixa = max(emissoes) - min(emissoes)
            ax.annotate(f"minimum at {volumes[k] / 1000:.1f} m³",
                        xy=(volumes[k] / 1000, emissoes[k]),
                        xytext=(volumes[k] / 1000 + 1.4,
                                emissoes[k] - faixa * 0.16),
                        fontsize=8.5, color=cor,
                        arrowprops=dict(arrowstyle="-", color=cor, linewidth=0.9))

        _eixos(ax, "", "cistern volume (m³)", "")
        ax.set_ylim(min(emissoes) - 0.26 * (max(emissoes) - min(emissoes)),
                    max(emissoes) + 0.04 * (max(emissoes) - min(emissoes)))
        ax.set_xlim(0, 12)
        ax.set_title(rotulo, fontsize=9, color=TINTA2, loc="left", pad=8)

    eixos[0].set_ylabel("20-year net emissions (kg CO₂e)",
                        fontsize=8.5, color=TINTA2)

    fig.tight_layout()
    _salvar(fig, "fig06b_otimizacao_ambiental.png")


def main():
    print("figuras do manual:")
    figura_dez_dias()
    figura_curva()
    figura_cidades()
    figura_materiais()
    figura_regimes()
    figura_carbono_no_tempo()
    figura_otimizacao_ambiental()


if __name__ == "__main__":
    main()
