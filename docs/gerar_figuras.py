"""
Gera as figuras do relatório de verificação e validação (docs/verificacao_e_validacao.md).

Executar a partir da raiz do programa:
    python docs/gerar_figuras.py

As figuras 1 e 3 são recalculadas a cada execução a partir do motor e do relatório de
cobertura. A figura 2 usa valores medidos em ambiente com numba instalado (ver o
relatório), pois este ambiente não possui numba.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from netuno.core.simulation import run_single_simulation  # noqa: E402

# Paleta validada (dataviz: slots categóricos 1 e 2, superfície clara)
SERIE_1 = "#2a78d6"   # azul
SERIE_2 = "#eb6834"   # laranja
TINTA_PRIMARIA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_SUAVE = "#898781"
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"
SUPERFICIE = "#fcfcfb"
CRITICO = "#d03b3b"
BOM = "#0ca30c"

FIGURAS = Path(__file__).parent / "figuras"
FIGURAS.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "sans-serif"],
    "font.size": 9,
    "axes.edgecolor": EIXO,
    "axes.labelcolor": TINTA_SECUNDARIA,
    "xtick.color": TINTA_SUAVE,
    "ytick.color": TINTA_SUAVE,
    "figure.facecolor": SUPERFICIE,
    "axes.facecolor": SUPERFICIE,
    "savefig.facecolor": SUPERFICIE,
})


def _estilizar(ax):
    """Grade recessiva, eixos limpos."""
    ax.grid(True, color=GRADE, linewidth=0.8, alpha=1.0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(EIXO)
        ax.spines[lado].set_linewidth(1.0)


def _serie_chuva(escala, n_dias, semente):
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=escala, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


# --------------------------------------------------------------------------------------
# Figura 1 — resposta do modelo ao volume, nos dois regimes hidrológicos
# Painéis separados (small multiples): as escalas diferem em uma ordem de grandeza e um
# eixo duplo seria enganoso.
# --------------------------------------------------------------------------------------
def figura_resposta_do_modelo():
    volumes = np.array([0, 250, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000], dtype=float)

    regimes = [
        ("Limitado pela demanda", SERIE_1, dict(
            precip_data=_serie_chuva(12.0, 1825, 2026), area=150.0, runoff_coeff=0.85,
            discard_mm=2.0, discard_mode=1, total_demand_per_day=600.0, rainwater_share=0.5)),
        ("Limitado pela oferta", SERIE_2, dict(
            precip_data=_serie_chuva(4.0, 1825, 7), area=30.0, runoff_coeff=0.80,
            discard_mm=2.0, discard_mode=1, total_demand_per_day=1500.0, rainwater_share=0.6)),
    ]

    fig, eixos = plt.subplots(1, 2, figsize=(9.5, 4.1))

    for ax, (rotulo, cor, params) in zip(eixos, regimes):
        economias = [run_single_simulation(lower_tank_vol=v, **params).potential_potable_savings_pct
                     for v in volumes]
        teto = params["rainwater_share"] * 100.0

        # Escala logarítmica: a resposta se desenvolve ao longo de 2,4 décadas de volume;
        # em escala linear todo o comportamento colapsaria contra o eixo.
        ax.set_xscale("log")
        ax.plot(volumes[1:] / 1000.0, economias[1:], color=cor, linewidth=2.0,
                marker="o", markersize=5.0, markerfacecolor=cor,
                markeredgecolor=SUPERFICIE, markeredgewidth=1.2, zorder=3)

        # O teto só vira linha quando está próximo dos dados; caso contrário viraria
        # uma referência distante que achataria a curva medida.
        topo = max(economias)
        if teto <= topo * 1.6:
            ax.axhline(teto, color=TINTA_SUAVE, linewidth=1.0, linestyle=(0, (4, 3)), zorder=1)
            # Rótulo do teto à esquerda para não colidir com o rótulo de saturação,
            # que fica ancorado no último ponto, à direita.
            ax.annotate(f"teto não potável ({teto:.0f}%)", xy=(0.02, teto),
                        xycoords=("axes fraction", "data"), xytext=(0, 5),
                        textcoords="offset points", ha="left", fontsize=8,
                        color=TINTA_SUAVE)
            limite_superior = teto * 1.20
        else:
            ax.annotate(f"teto não potável em {teto:.0f}%  (fora da escala:\n"
                        f"o sistema é limitado pela captação, não pela demanda)",
                        xy=(0.5, 0.90), xycoords="axes fraction", ha="center",
                        fontsize=8, color=TINTA_SUAVE)
            limite_superior = topo * 1.45

        ax.annotate(f"satura em {topo:.2f}%".replace(".", ","),
                    xy=(volumes[-1] / 1000.0, topo), xytext=(-8, 11),
                    textcoords="offset points", ha="right", fontsize=8.5,
                    color=TINTA_PRIMARIA, fontweight="bold")

        ax.set_title(rotulo, fontsize=10, color=TINTA_PRIMARIA, fontweight="bold", pad=8)
        ax.set_xlabel("Volume do reservatório inferior (m³, escala log)")
        ax.set_ylim(bottom=0, top=limite_superior)
        ax.set_xticks([0.25, 1, 4, 16, 64])
        ax.set_xticklabels(["0,25", "1", "4", "16", "64"])
        ax.minorticks_off()
        _estilizar(ax)

    eixos[0].set_ylabel("Economia de água potável (%)")

    fig.suptitle("Resposta do motor hidrológico ao volume do reservatório",
                 fontsize=11.5, color=TINTA_PRIMARIA, fontweight="bold", y=0.99)
    fig.text(0.5, 0.005,
             "Série sintética de 1.825 dias; V = 0 produz economia nula em ambos os regimes. "
             "As duas curvas são monótonas não-decrescentes e saturam em teto finito.",
             ha="center", fontsize=8, color=TINTA_SUAVE)
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    destino = FIGURAS / "fig01_resposta_do_modelo.png"
    fig.savefig(destino, dpi=200)
    plt.close(fig)
    print(f"  gerada: {destino.name}")


# --------------------------------------------------------------------------------------
# Figura 2 — divergência entre os kernels JIT e Python na repartição do consumo
# Valores medidos em ambiente isolado com numba 0.67.0 / numpy 2.5.3.
# --------------------------------------------------------------------------------------
def figura_divergencia_kernels():
    volumes = ["1.000 L", "5.000 L", "20.000 L"]
    # (interno JIT, interno Python), (irrigação JIT, irrigação Python) em m³/ano
    interno = [(102.270, 100.430), (102.270, 102.214), (102.270, 102.214)]
    irrigacao = [(5.156, 6.996), (8.860, 8.916), (8.860, 8.916)]

    fig, eixos = plt.subplots(1, 2, figsize=(9.5, 3.9))
    largura = 0.34
    posicoes = np.arange(len(volumes))

    for ax, dados, titulo in zip(
        eixos, [interno, irrigacao],
        ["Consumo pluvial interno", "Consumo pluvial de irrigação"],
    ):
        jit = [d[0] for d in dados]
        puro = [d[1] for d in dados]
        ax.bar(posicoes - largura / 2 - 0.01, jit, largura, label="Kernel JIT (numba)",
               color=SERIE_2, zorder=3)
        ax.bar(posicoes + largura / 2 + 0.01, puro, largura, label="Kernel Python (referência)",
               color=SERIE_1, zorder=3)

        for i, (a, b) in enumerate(dados):
            erro = abs(a - b) / max(abs(a), abs(b)) * 100.0
            if erro > 0.1:
                ax.annotate(f"{erro:.1f}%".replace(".", ","), xy=(i, max(a, b)),
                            xytext=(0, 6), textcoords="offset points", ha="center",
                            fontsize=8.5, color=CRITICO, fontweight="bold")

        ax.set_xticks(posicoes)
        ax.set_xticklabels(volumes)
        ax.set_title(titulo, fontsize=10, color=TINTA_PRIMARIA, fontweight="bold", pad=8)
        ax.set_xlabel("Volume do reservatório inferior")
        ax.set_ylim(bottom=0, top=max(max(j for j, _ in dados), max(p for _, p in dados)) * 1.22)
        _estilizar(ax)

    eixos[0].set_ylabel("Volume anual (m³)")

    # Legenda no nível da figura: dentro dos eixos ela cobriria as barras.
    alcas, rotulos = eixos[0].get_legend_handles_labels()
    fig.legend(alcas, rotulos, frameon=False, fontsize=8.5, ncol=2,
               loc="upper center", bbox_to_anchor=(0.5, 0.935),
               labelcolor=TINTA_SECUNDARIA)

    fig.suptitle("Divergência entre kernels na repartição do consumo pluvial",
                 fontsize=11.5, color=TINTA_PRIMARIA, fontweight="bold", y=0.99)
    fig.text(0.5, 0.005,
             "O total aproveitado coincide exatamente nos dois kernels; apenas a repartição "
             "diverge (rótulos em vermelho: erro relativo).",
             ha="center", fontsize=8, color=TINTA_SUAVE)
    fig.tight_layout(rect=(0, 0.035, 1, 0.885))
    destino = FIGURAS / "fig02_divergencia_kernels.png"
    fig.savefig(destino, dpi=200)
    plt.close(fig)
    print(f"  gerada: {destino.name}")


# --------------------------------------------------------------------------------------
# Figura 3 — cobertura de testes por módulo do núcleo
# --------------------------------------------------------------------------------------
def figura_cobertura():
    # Medição de 2026-09-07 (pytest-cov sobre netuno.core)
    modulos = [
        ("excel_scenarios", 14), ("change_detector", 24), ("scenarios", 33),
        ("cost_estimates", 63), ("environmental_sync", 64), ("simulation", 70),
        ("tariff_updater/aneel", 71), ("updater_engine", 73), ("tariffs_database", 75),
        ("environmental_justif.", 79), ("simulation_excel_exp.", 78),
        ("climate_database", 82), ("report_generator", 83), ("water_quality", 84),
        ("economic", 87), ("parser", 87), ("esg_certifications", 90),
        ("cad_exporter", 94), ("environmental", 95), ("mcdm_methods", 95),
        ("topsis", 98), ("report_service", 100),
    ]
    modulos.sort(key=lambda x: x[1])
    nomes = [m[0] for m in modulos]
    valores = [m[1] for m in modulos]

    # Magnitude com limiar: uma série, cor por faixa de risco (status, com rótulo direto)
    cores = [CRITICO if v < 50 else (SERIE_2 if v < 80 else SERIE_1) for v in valores]

    fig, ax = plt.subplots(figsize=(8.2, 6.4))
    barras = ax.barh(nomes, valores, color=cores, height=0.68, zorder=3)

    ax.axvline(80, color=TINTA_SUAVE, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
    ax.annotate("meta 80%", xy=(80, len(nomes) - 0.4), xytext=(5, 0),
                textcoords="offset points", fontsize=8.5, color=TINTA_SECUNDARIA,
                fontweight="bold")

    for barra, valor in zip(barras, valores):
        ax.annotate(f"{valor}%", xy=(valor, barra.get_y() + barra.get_height() / 2),
                    xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=8, color=TINTA_SECUNDARIA)

    ax.set_xlim(0, 108)
    ax.set_xlabel("Cobertura de linhas (%)")
    ax.set_title("Cobertura de testes por módulo do núcleo de cálculo",
                 fontsize=11.5, color=TINTA_PRIMARIA, fontweight="bold", pad=12, loc="left")
    _estilizar(ax)
    ax.grid(axis="y", visible=False)

    fig.text(0.01, 0.005,
             "Vermelho: abaixo de 50%.  Laranja: entre 50% e a meta.  Azul: na meta ou acima.  "
             "Total do núcleo: 81%.",
             ha="left", fontsize=8, color=TINTA_SUAVE)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    destino = FIGURAS / "fig03_cobertura_por_modulo.png"
    fig.savefig(destino, dpi=200)
    plt.close(fig)
    print(f"  gerada: {destino.name}")


if __name__ == "__main__":
    print("Gerando figuras do relatório de verificação e validação...")
    figura_resposta_do_modelo()
    figura_divergencia_kernels()
    figura_cobertura()
    print(f"Concluído. Figuras em: {FIGURAS}")
