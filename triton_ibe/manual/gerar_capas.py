# -*- coding: utf-8 -*-
"""Os painéis das capas: um desenho por volume, feito com os dados do manual.

Cada capa tem o mesmo esqueleto — painel azul-marinho no alto, título e créditos
embaixo — e um desenho próprio no painel, na cor do volume. Os desenhos não são
decoração inventada: saem da série de Lisboa (Iberia01, 1986-2015) e das simulações do tutorial,
as mesmas que alimentam as tabelas e as figuras do texto.

Saída: manual/figuras/capas/capa_<volume>.png, que o gerar_pdf.py põe na página.
"""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.dirname(AQUI))

from gerar_tabelas import _config_tutorial, _serie  # noqa: E402
from triton.core.simulation import run_single_simulation  # noqa: E402

SAIDA = os.path.join(AQUI, "figuras", "capas")

#: O fundo comum e a cor de cada volume.
MARINHO = "#0b2545"
CORES = {
    "completo": "#8ecae6",
    "1-comece-aqui": "#2ec4b6",
    "2-metodo": "#4ea8de",
    "3-guias": "#74c69d",
    "4-tutorial": "#f4a261",
    "5-confiabilidade": "#e76f51",
    "6-versoes": "#b8a9f5",
    "7-modulacao": "#f2c14e",
    "8-apendices": "#a9b4c2",
}

#: O painel ocupa a largura da folha A4 e 62% da altura.
LARGURA_POL = 210 / 25.4
ALTURA_POL = 297 * 0.62 / 25.4


def _tela():
    fig = plt.figure(figsize=(LARGURA_POL, ALTURA_POL), dpi=300)
    fig.patch.set_facecolor(MARINHO)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(MARINHO)
    ax.set_axis_off()
    return fig, ax


def _gravar(fig, nome):
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, f"capa_{nome}.png")
    fig.savefig(caminho, dpi=300, facecolor=MARINHO)
    plt.close(fig)
    print(f"  {os.path.relpath(caminho, AQUI)}")


def _chuva():
    return np.asarray(_serie(), dtype=float)


# ── um desenho por volume ─────────────────────────────────────────────────────

def completo(cor):
    """Trinta anos de chuva diária, dia a dia, como um sismograma."""
    p = _chuva()
    fig, ax = _tela()
    x = np.arange(len(p))
    # Espelhada e comprimida, a série ocupa a faixa central do painel sem que os
    # poucos dias extremos achatem o resto.
    a = p ** 0.6
    ax.vlines(x, -a, a, color=cor, linewidth=0.22, alpha=0.9)
    ax.set_xlim(-len(p) * 0.07, len(p) * 1.07)
    ax.set_ylim(-a.max() * 2.1, a.max() * 1.9)
    _gravar(fig, "completo")


def comece_aqui(cor):
    """Os quarenta maiores eventos de um ano, como anéis na superfície da água."""
    p = _chuva()[:365]
    fig, ax = _tela()
    rng = np.random.default_rng(5)
    dias = np.argsort(p)[-40:]
    for d in dias:
        x, y = rng.uniform(0.08, 0.92), rng.uniform(0.34, 0.64)
        r0 = 0.010 + p[d] / p.max() * 0.075
        for k in range(1, 6):
            circulo = plt.Circle((x, y), r0 * k * 0.55, fill=False, color=cor,
                                 linewidth=0.9, alpha=0.75 / k)
            ax.add_patch(circulo)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1 * ALTURA_POL / LARGURA_POL * 1.0 / (ALTURA_POL / LARGURA_POL))
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, ALTURA_POL / LARGURA_POL)
    _gravar(fig, "1-comece-aqui")


def metodo(cor):
    """A curva de retorno para frações atendíveis de 10% a 60%, em leque."""
    serie = _chuva()
    cfg = dict(_config_tutorial())
    volumes = np.array([0, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6500, 8000,
                        10000, 13000, 16000, 20000], dtype=float)
    fig, ax = _tela()
    fracoes = np.linspace(0.10, 0.60, 11)
    for i, f in enumerate(fracoes):
        cfg["rainwater_share"] = f
        pot = [run_single_simulation(precip_data=serie, lower_tank_vol=v, **cfg)
               .potential_potable_savings_pct for v in volumes]
        ax.plot(volumes, pot, color=cor, linewidth=1.3, alpha=0.35 + 0.6 * i / len(fracoes),
                solid_capstyle="round")
        ax.scatter(volumes, pot, s=5, color=cor, alpha=0.8, zorder=3)
    ax.set_xlim(-2500, 22500)
    ax.set_ylim(-40, 88)
    _gravar(fig, "2-metodo")


def guias(cor):
    """O regime mensal de Lisboa, Porto e Funchal, lado a lado, na mesma escala."""
    fig, ax = _tela()
    cidades = ("Lisboa", "Porto", "Funchal")
    largura = 0.9
    for c, nome in enumerate(cidades):
        s = np.asarray(_serie(nome), dtype=float)[: 30 * 365]
        anos = len(s) // 365
        mensal = s[: anos * 365].reshape(anos, 365)
        limites = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        medias = [mensal[:, limites[m]:limites[m + 1]].sum(axis=1).mean() for m in range(12)]
        x0 = c * 13.5
        for m, v in enumerate(medias):
            ax.bar(x0 + m, v, width=largura, color=cor, alpha=min(1.0, 0.35 + 0.55 * (v / 150.0)))
    ax.set_xlim(-6, 3 * 13.5 + 4)
    ax.set_ylim(-160, 260)
    _gravar(fig, "3-guias")


def tutorial(cor):
    """O nível da cisterna de 4.000 L em dois anos, com a chuva caindo do alto."""
    serie = _chuva()
    r = run_single_simulation(precip_data=serie, lower_tank_vol=4000.0,
                              store_daily_details=True, **_config_tutorial())
    dias = 730
    nivel = np.array([d.lower_tank_end_liters for d in r.daily_results[:dias]])
    chuva = serie[:dias]
    fig, ax = _tela()
    x = np.arange(dias)
    ax.fill_between(x, 0, nivel, color=cor, alpha=0.55, linewidth=0)
    ax.plot(x, nivel, color=cor, linewidth=0.8)
    topo = 8600
    ax.vlines(x, topo - chuva * 18, topo, color=cor, linewidth=0.6, alpha=0.8)
    ax.set_xlim(-60, dias + 60)
    ax.set_ylim(-3600, topo + 2400)
    _gravar(fig, "4-tutorial")


def confiabilidade(cor):
    """Curvas de permanência da autonomia armazenada, de 1 a 20 m³."""
    serie = _chuva()
    cfg = _config_tutorial()
    fig, ax = _tela()
    vols = (1000, 2000, 3000, 4000, 6000, 8000, 12000, 20000)
    for i, v in enumerate(vols):
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  store_daily_details=True, **cfg)
        dem = r.daily_results[0].pluvial_demand_liters
        aut = np.sort([d.lower_tank_end_liters / dem for d in r.daily_results])[::-1]
        perm = np.linspace(0, 100, len(aut))
        ax.plot(perm, aut, color=cor, linewidth=1.4, alpha=0.3 + 0.7 * i / len(vols))
    ax.set_xlim(-10, 110)
    ax.set_ylim(-110, 190)
    _gravar(fig, "5-confiabilidade")


def versoes(cor):
    """Trinta faixas, uma por ano, com a intensidade da chuva anual."""
    p = _chuva()
    anos = len(p) // 365
    totais = p[: anos * 365].reshape(anos, 365).sum(axis=1)
    norm = (totais - totais.min()) / (totais.max() - totais.min())
    fig, ax = _tela()
    for i, t in enumerate(norm):
        ax.add_patch(plt.Rectangle((i, 0), 1.0, 1.0, color=cor, alpha=0.12 + 0.85 * t,
                                   linewidth=0))
    ax.set_xlim(-2, anos + 2)
    ax.set_ylim(-0.75, 1.25)
    _gravar(fig, "6-versoes")


def apendices(cor):
    """A chuva de cada mês de cada ano, em grade: 30 anos por 12 meses."""
    p = _chuva()
    anos = len(p) // 365
    limites = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    grade = np.array([[p[a * 365 + limites[m]: a * 365 + limites[m + 1]].sum()
                       for a in range(anos)] for m in range(12)])
    norm = grade / grade.max()
    fig, ax = _tela()
    for m in range(12):
        for a in range(anos):
            r = 0.12 + 0.36 * np.sqrt(norm[m, a])
            ax.add_patch(plt.Circle((a, 11 - m), r, color=cor, alpha=0.3 + 0.65 * norm[m, a],
                                    linewidth=0))
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, anos + 0.5)
    ax.set_ylim(-8.5, 14.0)
    _gravar(fig, "8-apendices")


def modulacao(cor):
    """Duzentas curvas de economia por volume, uma por realização: o leque da modulação."""
    rng = np.random.default_rng(42)
    v = np.linspace(0, 20, 60)
    fig, ax = _tela()
    for _ in range(200):
        teto = rng.normal(28, 4)
        k = rng.lognormal(np.log(0.6), 0.25)
        ax.plot(v, teto * (1 - np.exp(-k * v)), color=cor, linewidth=0.8, alpha=0.18)
    ax.set_xlim(-0.5, 20.5)
    ax.set_ylim(-4, 45)
    _gravar(fig, "7-modulacao")


DESENHOS = {
    "completo": completo, "1-comece-aqui": comece_aqui, "2-metodo": metodo,
    "3-guias": guias, "4-tutorial": tutorial, "5-confiabilidade": confiabilidade,
    "6-versoes": versoes, "7-modulacao": modulacao, "8-apendices": apendices,
}


def main(so=None):
    print("capas:")
    for nome, desenho in DESENHOS.items():
        if so and nome not in so:
            continue
        desenho(CORES[nome])


if __name__ == "__main__":
    main(sys.argv[1:] or None)
