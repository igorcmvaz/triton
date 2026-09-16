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
    nomes = ["tarifa de disponibilidade (valor fixo)",
             "faixa de consumo 0 a 10 m³", "faixa de consumo 10 a 25 m³",
             "esgoto (100% do valor da água)"]
    vistos = set()
    legendas_x = []
    alturas_totais = []

    for i, (rotulo, consumo) in enumerate(casos):
        disp, faixas, agua = _parcelas_da_conta(consumo)
        parcelas = [(nomes[0], disp)]
        for j, (inicio, fim, valor) in enumerate(faixas):
            parcelas.append((nomes[1 + j] if 1 + j < 3 else
                             f"faixa de consumo {inicio:.0f} a {fim:.0f} m³",
                             valor))
        parcelas.append((nomes[3], agua))

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

    _eixos(ax, "", "", "fatura mensal de água e esgoto (R$)")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(legendas_x, fontsize=9.0)
    ax.set_xlim(-0.6, 2.3)
    teto = 50.0 * np.ceil(max(alturas_totais) * 1.05 / 50.0)
    ax.set_ylim(0, teto)
    ax.set_yticks(np.arange(0, teto + 1, 50))
    ax.legend(frameon=False, fontsize=8.2, loc="upper right")

    fig.tight_layout()
    _salvar(fig, "fig07_fatura.png")


# ══════════════════════════════════════════════════════════════════════════════
# Quando o investimento se paga
# ══════════════════════════════════════════════════════════════════════════════

def figura_fluxo_de_caixa():
    """Custos e economias de cada ano, em colunas, e o saldo acumulado.

    A primeira versão mostrava só a curva do saldo descontado, mês a mês, e o
    leitor não via de que ela era feita. Em colunas anuais aparecem as duas
    parcelas que a formam, o investimento no ano zero, e a linha acumulada
    cruza o zero no tempo de retorno.
    """
    from netuno.core.economic import run_economic_analysis

    r, _, _ = _consumos_do_tutorial()
    cfg = _config_economica(VOLUME_TUTORIAL, "CONCRETO")
    e = run_economic_analysis(cfg, r)

    fluxos = e.monthly_cash_flows
    n_anos = int(np.ceil(len(fluxos) / 12.0))
    anos = np.arange(0, n_anos + 1)
    economias = np.zeros(n_anos + 1)
    custos = np.zeros(n_anos + 1)
    custos[0] = e.capex_total
    acumulado = np.zeros(n_anos + 1)
    acumulado[0] = -e.capex_total
    for f in fluxos:
        ano = (f.month - 1) // 12 + 1
        economias[ano] += f.water_savings + f.iptu_savings
        custos[ano] += f.pump_cost + f.om_cost + f.chlorine_cost
        acumulado[ano] = f.cumulative_discounted

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)

    largura = 0.38
    ax.bar(anos - largura / 2.0, economias, largura, color=VERDE, zorder=3,
           label="economia na fatura de água e esgoto")
    ax.bar(anos + largura / 2.0, -custos, largura, color=LARANJA, zorder=3,
           label="investimento (ano 0) e custeio anual")
    ax.plot(anos, acumulado, color=ROXO, linewidth=2.2, marker="o",
            markersize=4.0, zorder=5, label="saldo acumulado descontado")
    ax.axhline(0.0, color=TINTA, linewidth=1.0, zorder=4)

    if e.payback_years:
        ax.axvline(e.payback_years, color=ROXO, linewidth=1.0, linestyle=":",
                   zorder=2)
        ax.text(e.payback_years + 0.25, acumulado.max() * 0.92,
                "tempo de retorno: " +
                f"{e.payback_years:.1f}".replace(".", ",") + " anos",
                fontsize=8.4, color=ROXO, va="top")

    _eixos(ax, "", "ano de operação", "valor (R$)")
    ax.set_xlim(-0.7, n_anos + 0.7)
    ax.set_xticks(range(0, n_anos + 1, 2))
    passo = 2500.0
    baixo = -passo * np.ceil(max(custos.max(), -acumulado.min()) / passo)
    alto = passo * np.ceil(max(acumulado.max(), economias.max()) * 1.05 / passo)
    ax.set_ylim(baixo, alto)
    marcas = np.arange(baixo, alto + 1, passo)
    ax.set_yticks(marcas)
    ax.set_yticklabels([f"{v:,.0f}".replace(",", ".").replace("-", "−")
                        for v in marcas])
    ax.legend(frameon=False, fontsize=8.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.14), ncol=2)

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

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True,
                                 gridspec_kw={"height_ratios": [1.15, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    a1.plot(vols, pots, color=AZUL, linewidth=2.4, zorder=3)
    a2.plot(vols, vpls, color=TINTA2, linewidth=2.0, zorder=3)
    # Os critérios que coincidem no mesmo volume ficam distinguíveis pelo traço,
    # e a identificação vai na legenda, e não em frases sobre o gráfico.
    marcas = [
        (i_ideal, ROXO, (0, (5, 3)), "critério 1: ganho marginal ≤ 1 %/m³"),
        (i_vpl, VERDE, (0, (1, 2)), "critério 2: VPL máximo"),
        (i_max, LARANJA, (0, (5, 3)), "critério 3: potencial máximo"),
    ]
    from matplotlib.lines import Line2D
    alcas = []
    for i, cor, traco, texto in marcas:
        for ax, serie_y in ((a1, pots), (a2, vpls)):
            ax.axvline(vols[i], color=cor, linewidth=1.6, linestyle=traco,
                       zorder=2)
            ax.plot([vols[i]], [serie_y[i]], "o", color=cor, markersize=7.0,
                    zorder=4)
        alcas.append(Line2D([0], [0], color=cor, linewidth=1.6, linestyle=traco,
                            marker="o", markersize=6.0,
                            label=texto + f" ({vols[i]:.0f} m³)"))

    passo_x = 2
    teto_x = passo_x * np.ceil(vols.max() / passo_x)
    _eixos(a1, "(a)", "", "potencial de economia (%)")
    a1.set_ylim(0, 50)
    a1.set_yticks(range(0, 51, 10))
    _eixos(a2, "(b)", "volume do reservatório (m³)",
           "valor presente líquido (R$)")
    passo_vpl = 2500.0
    teto_vpl = passo_vpl * np.ceil(vpls.max() * 1.02 / passo_vpl)
    piso_vpl = min(0.0, passo_vpl * np.floor(vpls.min() / passo_vpl))
    a2.set_ylim(piso_vpl, teto_vpl)
    marcas_vpl = np.arange(piso_vpl, teto_vpl + 1, passo_vpl)
    a2.set_yticks(marcas_vpl)
    a2.set_yticklabels([f"{v:,.0f}".replace(",", ".") for v in marcas_vpl])
    for ax in (a1, a2):
        ax.set_xlim(0, teto_x)
        ax.set_xticks(np.arange(0, teto_x + 1, passo_x))
    a2.set_xticklabels([f"{v:.0f}" for v in np.arange(0, teto_x + 1, passo_x)])
    a2.legend(handles=alcas, frameon=False, fontsize=8.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.22), ncol=1)

    fig.tight_layout()
    _salvar(fig, "fig09_criterios.png")


# ══════════════════════════════════════════════════════════════════════════════
# A permanência do nível: quanto tempo o reservatório passa vazio ou cheio
# ══════════════════════════════════════════════════════════════════════════════

#: Os volumes da curva de permanência, em litros.
VOLUMES_PERMANENCIA = (2000, 5000, 10000, 20000)
#: Os volumes das barras de estado, em litros.
VOLUMES_ESTADOS = (1000, 2000, 3000, 5000, 8000, 12000, 20000)
#: Abaixo desta fração da capacidade o reservatório conta como vazio; acima
#: da complementar, como cheio.
FOLGA_DE_NIVEL = 0.05


def _niveis_relativos(volume_l):
    """O nível ao fim de cada dia, como fração da capacidade."""
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=float(volume_l),
                              store_daily_details=True, **_config_tutorial())
    return np.asarray([d.lower_tank_end_liters for d in r.daily_results],
                      dtype=float) / float(volume_l)


def figura_permanencia():
    """A curva de permanência do nível e a fração de dias vazio e cheio.

    Substitui o gráfico do volume médio armazenado, cuja leitura era óbvia. A
    permanência mostra o que a média esconde: um reservatório grande não fica
    «meio cheio»; passa longos períodos vazio na estiagem e raramente enche.
    """
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 6.4),
                                 gridspec_kw={"height_ratios": [1.15, 1]})
    fig.patch.set_facecolor(SUPERFICIE)
    for ax in (a1, a2):
        ax.set_facecolor(SUPERFICIE)

    cores = [VERDE, AZUL, ROXO, LARANJA]
    for volume, cor in zip(VOLUMES_PERMANENCIA, cores):
        nivel = np.sort(_niveis_relativos(volume))[::-1] * 100.0
        permanencia = np.arange(1, len(nivel) + 1) / len(nivel) * 100.0
        a1.plot(permanencia, nivel, color=cor, linewidth=2.0, zorder=3,
                label=f"{volume / 1000.0:.0f} m³")
    _eixos(a1, "(a)", "permanência: tempo em que o nível é igualado ou "
           "superado (%)", "nível do reservatório (% da capacidade)")
    a1.set_xlim(0, 100)
    a1.set_ylim(0, 100)
    a1.set_xticks(range(0, 101, 10))
    a1.set_yticks(range(0, 101, 20))
    a1.legend(frameon=False, fontsize=8.4, loc="upper right",
              title="capacidade", title_fontsize=8.4)

    vazio, meio, cheio = [], [], []
    for volume in VOLUMES_ESTADOS:
        n = _niveis_relativos(volume)
        v = float(np.mean(n <= FOLGA_DE_NIVEL)) * 100.0
        c = float(np.mean(n >= 1.0 - FOLGA_DE_NIVEL)) * 100.0
        vazio.append(v)
        cheio.append(c)
        meio.append(100.0 - v - c)
    x = np.arange(len(VOLUMES_ESTADOS))
    a2.bar(x, vazio, 0.6, color=LARANJA, zorder=3, edgecolor=SUPERFICIE,
           linewidth=1.5, label=f"vazio (≤ {FOLGA_DE_NIVEL * 100:.0f}%)")
    a2.bar(x, meio, 0.6, bottom=vazio, color="#bcd6f5", zorder=3,
           edgecolor=SUPERFICIE, linewidth=1.5, label="nível intermediário")
    a2.bar(x, cheio, 0.6, bottom=np.add(vazio, meio), color=AZUL, zorder=3,
           edgecolor=SUPERFICIE, linewidth=1.5,
           label=f"cheio (≥ {100 - FOLGA_DE_NIVEL * 100:.0f}%)")
    for i in range(len(x)):
        if vazio[i] >= 6:
            a2.text(i, vazio[i] / 2.0, f"{vazio[i]:.0f}%", ha="center",
                    va="center", fontsize=7.8, color="#ffffff")
        if cheio[i] >= 6:
            a2.text(i, 100.0 - cheio[i] / 2.0, f"{cheio[i]:.0f}%",
                    ha="center", va="center", fontsize=7.8, color="#ffffff")
    _eixos(a2, "(b)", "capacidade do reservatório (m³)", "dias da série (%)")
    a2.set_xticks(x)
    a2.set_xticklabels([f"{v / 1000.0:.0f}" for v in VOLUMES_ESTADOS])
    a2.set_ylim(0, 100)
    a2.set_yticks(range(0, 101, 20))
    a2.grid(axis="x", visible=False)
    a2.legend(frameon=False, fontsize=8.2, loc="upper center",
              bbox_to_anchor=(0.5, -0.22), ncol=3)

    fig.tight_layout()
    _salvar(fig, "fig47_permanencia.png")


def main():
    print("figuras de resultado (extra):")
    figura_fatura()
    figura_fluxo_de_caixa()
    figura_criterios()
    figura_permanencia()


if __name__ == "__main__":
    main()
