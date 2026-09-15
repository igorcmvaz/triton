# -*- coding: utf-8 -*-
"""Figuras de resultado que faltavam ao manual, todas do projeto do tutorial.

As três respondem a perguntas que o texto vinha respondendo só com tabelas: de
que a conta de água é feita, quando o investimento se paga, e por que três
critérios legítimos apontam três volumes diferentes para o mesmo projeto.

Como as demais, saem de uma rodada do próprio programa, e não de números
transcritos: corrigir o motor corrige a figura.

Executar a partir da raiz do programa:
    python manual/gerar_figuras_extra.py
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
    AZUL, EIXO, GRADE, LARANJA, ROXO, SUPERFICIE, TINTA, TINTA2, VERDE,
    _eixos, _salvar,
)
from gerar_tabelas import (                                       # noqa: E402
    TARIFA_CASAN, VOLUMES_VARREDURA, _config_economica,
    _config_tutorial, _serie,
)

from netuno.core.simulation import run_single_simulation          # noqa: E402

DIAS_MES = 30.4375
VOLUME_TUTORIAL = 5000.0


def _consumos_do_tutorial():
    """Os dois consumos mensais do projeto do tutorial, em m³."""
    r = run_single_simulation(precip_data=_serie(),
                              lower_tank_vol=VOLUME_TUTORIAL,
                              **_config_tutorial())
    total = ((r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day)
             * DIAS_MES / 1000.0)
    potavel = r.avg_potable_consumed_l_day * DIAS_MES / 1000.0
    return r, total, potavel


# ══════════════════════════════════════════════════════════════════════════════
# De que a conta de água é feita
# ══════════════════════════════════════════════════════════════════════════════

def _parcelas_da_conta(consumo_m3):
    """A conta aberta em disponibilidade, faixas de consumo e esgoto."""
    disponibilidade = sum(t[2] for t in TARIFA_CASAN if t[3] == -1)
    faixas = []
    for inicio, fim, preco, codigo in TARIFA_CASAN:
        if codigo != 1:
            continue
        volume = max(0.0, min(consumo_m3, fim) - inicio)
        if volume > 0:
            faixas.append((inicio, fim, volume * preco))
    agua = disponibilidade + sum(v for _, _, v in faixas)
    return disponibilidade, faixas, agua


def figura_fatura():
    """A fatura da CASAN aberta, antes e depois do sistema.

    O leitor que só vê o total não entende por que a economia de água não vira
    economia proporcional de dinheiro. Aberta em parcelas, a razão fica visível:
    a disponibilidade não se mexe, e a faixa cara é a única que encolhe.
    """
    _, total_m3, potavel_m3 = _consumos_do_tutorial()

    casos = [("sem o sistema", total_m3), ("com o sistema", potavel_m3)]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    largura = 0.5
    cores = [LARANJA, AZUL, "#7fb0ea", VERDE]
    nomes = ["disponibilidade (fixa)", "faixa 0 a 10 m³",
             "faixa 10 a 25 m³", "esgoto (100% da água)"]
    vistos = set()
    legendas_x = []
    alturas_totais = []

    for i, (rotulo, consumo) in enumerate(casos):
        disp, faixas, agua = _parcelas_da_conta(consumo)
        parcelas = [("disponibilidade (fixa)", disp)]
        for j, (inicio, fim, valor) in enumerate(faixas):
            parcelas.append((nomes[1 + j] if 1 + j < 3 else
                             f"faixa {inicio:.0f} a {fim:.0f} m³", valor))
        parcelas.append(("esgoto (100% da água)", agua))

        base = 0.0
        for nome, valor in parcelas:
            cor = cores[nomes.index(nome)] if nome in nomes else TINTA2
            ax.bar(i, valor, largura, bottom=base, color=cor, zorder=3,
                   edgecolor=SUPERFICIE, linewidth=2.0,
                   label=nome if nome not in vistos else None)
            vistos.add(nome)
            if valor > 12.0:
                ax.text(i, base + valor / 2.0,
                        ("R$ " + f"{valor:,.0f}").replace(",", "."),
                        ha="center", va="center", fontsize=8.2, color="#ffffff")
            base += valor
        legendas_x.append(
            rotulo + "\n" + f"{consumo:.1f} m³".replace(".", ",") + " · " +
            ("R$ " + f"{base:,.0f}").replace(",", "."))
        alturas_totais.append(base)

    _eixos(ax, "A economia sai da faixa mais cara; a parcela fixa não se mexe", "",
           "conta mensal (R$)")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(legendas_x, fontsize=9.0)
    ax.set_xlim(-0.6, 1.9)
    ax.set_ylim(0, max(alturas_totais) * 1.14)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")

    fig.tight_layout()
    _salvar(fig, "fig07_fatura.png")


# ══════════════════════════════════════════════════════════════════════════════
# Quando o investimento se paga
# ══════════════════════════════════════════════════════════════════════════════

def figura_fluxo_de_caixa():
    """O saldo descontado acumulado, mês a mês, ao longo de vinte anos."""
    from netuno.core.economic import run_economic_analysis

    r, _, _ = _consumos_do_tutorial()
    cfg = _config_economica(VOLUME_TUTORIAL, "CONCRETO")
    e = run_economic_analysis(cfg, r)

    fluxos = e.monthly_cash_flows
    anos = np.array([f.month / 12.0 for f in fluxos])
    saldo = np.array([f.cumulative_discounted for f in fluxos])

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    ax.fill_between(anos, saldo, 0.0, where=(saldo < 0), color=LARANJA,
                    alpha=0.13, zorder=2)
    ax.fill_between(anos, saldo, 0.0, where=(saldo >= 0), color=VERDE,
                    alpha=0.13, zorder=2)
    ax.plot(anos, saldo, color=ROXO, linewidth=2.4, zorder=4)
    ax.axhline(0.0, color=TINTA, linewidth=1.1, zorder=3)

    if e.payback_years:
        ax.plot([e.payback_years], [0.0], "o", color=ROXO, markersize=8,
                zorder=5)
        ax.annotate("retorno em " + f"{e.payback_years:.1f}".replace(".", ",") +
                    " anos",
                    xy=(e.payback_years, 0.0),
                    xytext=(e.payback_years + 1.2, saldo.max() * 0.42),
                    fontsize=9.0, color=ROXO,
                    arrowprops=dict(arrowstyle="-", color=ROXO, linewidth=0.9))

    ax.text(max(anos) * 0.60, -abs(e.capex_total) * 0.62,
            "investimento inicial\n" + ("R$ " + f"{e.capex_total:,.0f}").replace(",", "."),
            fontsize=8.4, color=TINTA2, va="center")

    _eixos(ax, "O saldo descontado atravessa o zero uma única vez",
           "anos de operação", "saldo acumulado e descontado (R$)")
    ax.set_xlim(0, max(anos))

    fig.tight_layout()
    _salvar(fig, "fig08_fluxo_de_caixa.png")


# ══════════════════════════════════════════════════════════════════════════════
# Três critérios, três volumes
# ══════════════════════════════════════════════════════════════════════════════

def figura_criterios():
    """A mesma curva de varredura lida por três critérios legítimos.

    É a figura que o capítulo dos enganos pede: nenhum dos três está errado, e
    quem não declara qual usou não comunicou o resultado.
    """
    from netuno.core.economic import run_economic_analysis

    serie = _serie()
    cfg_sim = _config_tutorial()
    vols, pots, vpls = [], [], []
    for v in VOLUMES_VARREDURA:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  **cfg_sim)
        vols.append(v / 1000.0)
        pots.append(r.potential_potable_savings_pct)
        if v == 0:
            vpls.append(0.0)
            continue
        e = run_economic_analysis(_config_economica(float(v), "CONCRETO"), r)
        vpls.append(e.vpl)

    vols = np.array(vols)
    pots = np.array(pots)
    vpls = np.array(vpls)

    # Critério 1 — o limiar de ganho marginal, que é o do programa.
    marginal = np.zeros_like(pots)
    marginal[1:] = np.diff(pots) / np.diff(vols)
    limiar = 1.0  # o limiar do tutorial, seção do volume ideal
    ideais = np.where((vols > 0) & (marginal <= limiar))[0]
    i_ideal = int(ideais[0]) if len(ideais) else len(vols) - 1
    # Critério 2 — o maior valor presente líquido.
    i_vpl = int(np.argmax(vpls))
    # Critério 3 — o maior potencial de economia da varredura.
    i_max = int(np.argmax(pots))

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True,
                                 gridspec_kw={"height_ratios": [1.15, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.plot(vols, pots, color=AZUL, linewidth=2.4, zorder=3)
    a2.plot(vols, vpls, color=TINTA2, linewidth=2.0, zorder=3)
    marcas = [
        (i_ideal, ROXO, "1. ganho marginal\nabaixo de 1 %/m³\n(o do tutorial)"),
        (i_vpl, VERDE, "2. maior valor\npresente líquido"),
        (i_max, LARANJA, "3. maior potencial\nda varredura"),
    ]
    alturas = (0.42, 0.24, 0.06)
    for (i, cor, texto), altura in zip(marcas, alturas):
        for ax, serie_y in ((a1, pots), (a2, vpls)):
            ax.axvline(vols[i], color=cor, linewidth=1.3, linestyle="--",
                       zorder=2)
            ax.plot([vols[i]], [serie_y[i]], "o", color=cor, markersize=7.5,
                    zorder=4)
        # O rótulo fica do lado em que há espaço: à direita da linha, e à
        # esquerda quando a linha está na metade direita do gráfico.
        direita = vols[i] > vols.max() * 0.55
        a1.text(vols[i] + (-0.5 if direita else 0.4),
                pots.max() * altura + pots.max() * 0.18, texto,
                fontsize=8.0, color=cor, va="center", linespacing=1.35,
                ha="right" if direita else "left")

    rotulados = set()
    for i, cor, _texto in marcas:
        # Dois critérios que elegem o mesmo volume ganham um rótulo só: com
        # dois, o número saía escrito duas vezes no mesmo lugar.
        if i in rotulados:
            continue
        rotulados.add(i)
        direita = vols[i] > vols.max() * 0.55
        a2.annotate(f"{vols[i]:.0f} m³", xy=(vols[i], 0.0),
                    xytext=(vols[i] + (-0.45 if direita else 0.35),
                            vpls.max() * 0.08),
                    fontsize=8.5, color=cor,
                    ha="right" if direita else "left")

    _eixos(a1, "Três critérios, dois volumes: o técnico e o econômico coincidem",
           "", "potencial de economia (%)")
    _eixos(a2, "", "volume do reservatório (m³)", "valor presente líquido (R$)")
    a2.axhline(0.0, color=EIXO, linewidth=1.0, zorder=2)

    fig.tight_layout()
    _salvar(fig, "fig09_criterios.png")


def main():
    print("figuras de resultado (extra):")
    figura_fatura()
    figura_fluxo_de_caixa()
    figura_criterios()


if __name__ == "__main__":
    main()
