#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figuras para publicação dos seis estudos de Santa Catarina (edição BRL).

Lê apenas os ``resultados.csv`` produzidos por ``triton estudo run`` (nenhuma simulação é
refeita e nenhum número é digitado aqui) e gera, em ``estudos/santa-catarina/_saida``:

* ``figuras_artigos/<idioma>/<coluna>/fig_resumo.*``  : uma figura comparando as seis
  tipologias (volume ótimo, viabilidade econômica, indicador ambiental);
* ``figuras_artigos/<idioma>/<coluna>/fig_<tipologia>.*`` : uma figura por tipologia;
* ``figuras_artigos/<idioma>/legenda_*.md``           : legenda sugerida de cada figura, com
  todo número calculado dos resultados;
* ``dashboard_artigos.html``                          : painel interativo, sem dependência de
  rede, em modo claro/escuro e em pt-BR/en-GB.

Idiomas: ``pt-BR`` e ``en-GB``. Larguras: ``dupla`` (7,2 pol = 183 mm) e ``simples``
(3,46 pol = 88 mm), com fontes de 6,5 a 8,5 pt no tamanho final. Formatos: PNG a 300 dpi,
SVG e PDF (vetoriais, texto em curvas no SVG e fonte TrueType incorporada no PDF).
Determinístico: sem datas nos metadados, sem sorteios.

Paleta categórica única (validada com ``validate_palette`` do skill dataviz, adjacente, claro e
escuro: separação CVD >= 8,4 e diferença em visão normal >= 19): cada tipologia mantém a mesma
cor, o mesmo marcador e o mesmo rótulo em todas as figuras. A cor nunca é o único canal:
rótulo direto, marcador, hachura e contorno escuro.

Uso (na pasta ``triton_brl``)::

    python scripts/gerar_graficos_artigos.py
    python scripts/gerar_graficos_artigos.py --idioma en-GB --coluna simples --formatos png,pdf
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA_PADRAO = RAIZ / "estudos" / "santa-catarina" / "_saida"
ESTUDOS = RAIZ / "estudos" / "santa-catarina"

IDIOMAS = ("pt-BR", "en-GB")
COLUNAS = {"dupla": 7.2, "simples": 3.46}
FORMATOS = ("png", "svg", "pdf")
DPI = 300
HIST = "hist-1981-2010"
RECORTES = [  # (id, posição em x, cenário)
    (HIST, 0, "HIST"),
    ("ssp245-2021-2050", 1, "SSP245"), ("ssp245-2041-2070", 2, "SSP245"),
    ("ssp245-2071-2100", 3, "SSP245"),
    ("ssp585-2021-2050", 1, "SSP585"), ("ssp585-2041-2070", 2, "SSP585"),
    ("ssp585-2071-2100", 3, "SSP585"),
]
METRICAS = [
    "volume_otimo_tecnico_l", "volume_otimo_economico_l", "volume_otimo_ambiental_l",
    "volume_topsis_l", "volume_smaa_vikor_l", "economia_agua_potavel_pct", "vpl",
    "co2_liquido_vida_kg", "payback_ambiental_anos",
]
CRITERIOS = [  # (chave, métrica, marcador)
    ("tec", "volume_otimo_tecnico_l", "^"), ("eco", "volume_otimo_economico_l", "s"),
    ("amb", "volume_otimo_ambiental_l", "D"), ("top", "volume_topsis_l", "P"),
    ("smaa", "volume_smaa_vikor_l", "o"),
]

# Paleta categórica (slots 1 a 6 do dataviz/palette.md), claro e escuro; ordem fixa.
CORES_CLARO = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
CORES_ESCURO = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRADE = "#e1e0d9"
CINZA = "#c3c2b7"

TIPOLOGIAS = [  # ordem fixa = ordem do artigo e do slot de cor
    {"chave": "escolar", "estudo": "sc-escolar", "pasta": "escolar", "slot": 0, "marcador": "o",
     "nome": {"pt-BR": "Escolar", "en-GB": "School"}},
    {"chave": "comercial", "estudo": "sc-comercial", "pasta": "comercial", "slot": 1,
     "marcador": "s",
     "nome": {"pt-BR": "Comercial", "en-GB": "Commercial"}},
    {"chave": "unifamiliar", "estudo": "sc-residencial-unifamiliar",
     "pasta": "residencial-unifamiliar", "slot": 2, "marcador": "^",
     "nome": {"pt-BR": "Residencial\nunifamiliar", "en-GB": "Single-family\nhousing"}},
    {"chave": "multifamiliar", "estudo": "sc-residencial-multifamiliar",
     "pasta": "residencial-multifamiliar", "slot": 3, "marcador": "D",
     "nome": {"pt-BR": "Residencial\nmultifamiliar", "en-GB": "Multi-family\nhousing"}},
    {"chave": "hospitalar", "estudo": "sc-hospitalar", "pasta": "hospitalar", "slot": 4,
     "marcador": "v",
     "nome": {"pt-BR": "Hospitalar", "en-GB": "Hospital"}},
    {"chave": "aeroportuario", "estudo": "sc-aeroportuario", "pasta": "aeroportos", "slot": 5,
     "marcador": "P",
     "nome": {"pt-BR": "Aeroportuária", "en-GB": "Airport"}},
]

TXT = {
    "pt-BR": {
        "crit": {"tec": "Técnico", "eco": "Econômico", "amb": "Ambiental", "top": "TOPSIS",
                 "smaa": "SMAA-VIKOR"},
        "rec": ["histórico", "próximo", "médio", "distante"],
        "rec_x": "Recorte climático (CLIMBra, 19 modelos)",
        "vol_x": "Volume do reservatório (m³)",
        "casos_pos_x": "Casos do recorte histórico (%)",
        "payback_x": "Payback ambiental (anos)",
        "a_volume": "Volume ótimo por critério",
        "res_volume": "Volume ótimo",
        "res_viab": "Viabilidade econômica",
        "res_amb": "Indicador ambiental",
        "agua": "Economia de água potável",
        "agua_y": "Economia de água potável (%)",
        "vpl": "Valor presente líquido",
        "vpl_y": "VPL em 20 anos ({u})",
        "co2": "Saldo líquido de carbono",
        "co2_y": "Saldo líquido de CO₂e em 20 anos ({u})",
        "moeda": {1: "R$", 1e3: "R$ mil", 1e6: "R$ milhões"},
        "massa": {1: "kg", 1e3: "t"},
        "l_ssp245": "SSP2-4.5", "l_ssp585": "SSP5-8.5",
        "l_ic": "Símbolo: mediana; barra: percentis 10 a 90",
        "l_pos": "VPL > 0", "l_zero": "VPL = 0 (sem reservatório)", "l_neg": "VPL < 0",
        "milhar": ".", "dec": ",",
    },
    "en-GB": {
        "crit": {"tec": "Technical", "eco": "Economic", "amb": "Environmental", "top": "TOPSIS",
                 "smaa": "SMAA-VIKOR"},
        "rec": ["historical", "near", "mid", "far"],
        "rec_x": "Climate window (CLIMBra, 19 models)",
        "vol_x": "Reservoir volume (m³)",
        "casos_pos_x": "Historical-window cases (%)",
        "payback_x": "Environmental payback (years)",
        "a_volume": "Optimal volume by criterion",
        "res_volume": "Optimal volume",
        "res_viab": "Economic viability",
        "res_amb": "Environmental indicator",
        "agua": "Potable-water saving",
        "agua_y": "Potable-water saving (%)",
        "vpl": "Net present value",
        "vpl_y": "20-year NPV ({u})",
        "co2": "Net carbon balance",
        "co2_y": "20-year net CO₂e balance ({u})",
        "moeda": {1: "R$", 1e3: "R$ thousand", 1e6: "R$ million"},
        "massa": {1: "kg", 1e3: "t"},
        "l_ssp245": "SSP2-4.5", "l_ssp585": "SSP5-8.5",
        "l_ic": "Symbol: median; bar: 10th to 90th percentile",
        "l_pos": "NPV > 0", "l_zero": "NPV = 0 (no reservoir)", "l_neg": "NPV < 0",
        "milhar": ",", "dec": ".",
    },
}


# ───────────────────────── utilidades numéricas ─────────────────────────
def num(x: float, d: int, lang: str) -> str:
    """Formata ``x`` com ``d`` decimais no padrão do idioma (pt-BR: 1.234,5; en-GB: 1,234.5)."""
    s = f"{x:,.{d}f}"
    if lang == "pt-BR":
        s = s.replace(",", "\0").replace(".", ",").replace("\0", ".")
    return s.replace("-", "−")


def num_auto(x: float, lang: str) -> str:
    """Número de rótulo de eixo: inteiro sem decimais; senão 1 ou 2 decimais."""
    if abs(x - round(x)) < 1e-9:
        return num(round(x), 0, lang)
    return num(x, 1 if abs(round(x, 1) - x) < 1e-9 else 2, lang)


def quantis(v):
    """(mediana, P10, P90) de um vetor; NaN descartados."""
    import numpy as np
    a = np.asarray(v, dtype=float)
    a = a[~np.isnan(a)]
    if a.size == 0:
        return (float("nan"),) * 3
    return (float(np.percentile(a, 50)), float(np.percentile(a, 10)), float(np.percentile(a, 90)))


def escolher_escala(valores, tipo: str, lang: str):
    """Divisor e rótulo de unidade pelo maior valor absoluto plotado (moeda ou massa)."""
    m = max((abs(v) for v in valores if v == v), default=0.0)
    if tipo == "moeda":
        div = 1e6 if m >= 1e6 else (1e3 if m >= 1e4 else 1)
        return div, TXT[lang]["moeda"][div]
    div = 1e3 if m >= 1e4 else 1
    return div, TXT[lang]["massa"][div]


# ───────────────────────── dados ─────────────────────────
def carregar(tip: dict, saida: Path):
    """DataFrame largo (uma linha por caso) com as métricas usadas, ordenado por caso."""
    import pandas as pd
    arq = saida / tip["estudo"] / "resultados.csv"
    df = pd.read_csv(arq, usecols=["caso_id", "recorte", "cenario", "metrica", "valor"])
    df = df[df["metrica"].isin(METRICAS)]
    meta = df.drop_duplicates("caso_id").set_index("caso_id")[["recorte", "cenario"]]
    largo = df.pivot(index="caso_id", columns="metrica", values="valor")
    largo = meta.join(largo).sort_index()
    largo["local"] = [c.split("__")[0] for c in largo.index]
    return largo


def arquetipo(tip: dict) -> dict:
    """Parâmetros do arquétipo, lidos do estudo.json (não digitados)."""
    d = json.loads((ESTUDOS / tip["pasta"] / "estudo.json").read_text(encoding="utf-8"))
    return d["padroes"]["substituicoes"]


def estatisticas(tip: dict, largo) -> dict:
    """Todos os números de figuras, legendas e painel, calculados dos resultados."""
    hist = largo[largo["recorte"] == HIST]
    est = {"n_casos": int(len(largo)), "n_hist": int(len(hist)),
           "n_locais": int(largo["local"].nunique()),
           "n_modelos": int(len(hist) // max(1, hist["local"].nunique()))}
    est["vol"] = {k: tuple(v / 1000.0 for v in quantis(hist[m])) for k, m, _ in CRITERIOS}
    v = hist["vpl"]
    est["share"] = {"pos": float((v > 0).mean() * 100), "zero": float((v == 0).mean() * 100),
                    "neg": float((v < 0).mean() * 100)}
    com_res = hist[hist["volume_smaa_vikor_l"] > 0]
    est["pay"] = quantis(com_res["payback_ambiental_anos"]) + (int(com_res["payback_ambiental_anos"].notna().sum()),)
    est["rec"] = {}
    est["pos_vpl"] = {}
    est["pos_co2"] = {}
    for r, _, _ in RECORTES:
        sub = largo[largo["recorte"] == r]
        est["rec"][r] = {m: quantis(sub[m]) for m in
                         ("economia_agua_potavel_pct", "vpl", "co2_liquido_vida_kg")}
        est["pos_vpl"][r] = float((sub["vpl"] > 0).mean() * 100)
        est["pos_co2"][r] = float((sub["co2_liquido_vida_kg"] > 0).mean() * 100)
    return est


# ───────────────────────── matplotlib ─────────────────────────
def configurar_mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7.5, "axes.labelsize": 7.5,
        "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "axes.linewidth": 0.6, "axes.edgecolor": TINTA_2, "axes.labelcolor": TINTA,
        "xtick.color": TINTA_2, "ytick.color": TINTA_2, "text.color": TINTA,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5,
        "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.5, "axes.axisbelow": True,
        "legend.frameon": False, "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "hatch.linewidth": 0.6, "axes.unicode_minus": True,
        "svg.fonttype": "path", "svg.hashsalt": "triton-sc", "pdf.fonttype": 42,
        "figure.dpi": 100, "savefig.dpi": DPI,
    })
    return plt


def cor(tip: dict) -> str:
    return CORES_CLARO[tip["slot"]]


def salvar(fig, base: Path, formatos):
    base.parent.mkdir(parents=True, exist_ok=True)
    for f in formatos:
        meta = {"png": {"Software": "Triton gerar_graficos_artigos.py"},
                "svg": {"Date": None, "Creator": "Triton gerar_graficos_artigos.py"},
                "pdf": {"Creator": "Triton gerar_graficos_artigos.py", "CreationDate": None,
                        "ModDate": None, "Producer": "matplotlib"}}[f]
        fig.savefig(base.with_suffix("." + f), dpi=DPI, metadata=meta)


def letra(ax, txt, lang_sub=None):
    ax.set_title(txt, loc="left", fontweight="bold", fontsize=8, pad=4, color=TINTA)


def ponto_ic(ax, x, y, ic, cor_, marcador, horizontal=True, ms=5.0, fill=True, lw=1.4, z=3):
    """Marcador na mediana e barra P10 a P90 (horizontal ou vertical)."""
    med, lo, hi = ic
    mfc = cor_ if fill else "white"
    if horizontal:
        ax.hlines(y, lo, hi, color=cor_, lw=lw, zorder=z - 1, capstyle="round")
        ax.plot([med], [y], marcador, ms=ms, mfc=mfc, mec=TINTA, mew=0.6, zorder=z, clip_on=False)
    else:
        ax.vlines(x, lo, hi, color=cor_, lw=lw, zorder=z - 1, capstyle="round")
        ax.plot([x], [med], marcador, ms=ms, mfc=mfc, mec=TINTA, mew=0.6, zorder=z, clip_on=False)


def painel_volumes(ax, tip, est, lang):
    """Painel (a) da figura por tipologia: cinco critérios, mediana e P10 a P90."""
    t = TXT[lang]
    c = cor(tip)
    for i, (k, _, mk) in enumerate(CRITERIOS):
        smaa = k == "smaa"
        ponto_ic(ax, 0, i, est["vol"][k], c, mk, True, ms=6.5 if smaa else 5.0,
                 lw=2.0 if smaa else 1.2)
    ax.set_yticks(range(len(CRITERIOS)))
    ax.set_yticklabels([t["crit"][k] for k, _, _ in CRITERIOS])
    ax.invert_yaxis()
    ax.set_ylim(len(CRITERIOS) - 0.4, -0.6)
    ax.grid(axis="y", visible=False)
    topo = max(h for k, *_ in [(k,) for k, _, _ in CRITERIOS] for h in [est["vol"][k][2]])
    ax.set_xlim(-0.03 * topo, topo * 1.05 if topo > 0 else 1)
    ax.set_xlabel(t["vol_x"])
    ax.xaxis.set_major_formatter(_fmt(lang))
    letra(ax, "(a) " + t["a_volume"])


def _fmt(lang, div=1.0):
    from matplotlib.ticker import FuncFormatter
    return FuncFormatter(lambda x, _p: num_auto(x / div, lang))


def painel_recortes(ax, tip, est, lang, metrica, tipo_unidade, ylabel_chave, titulo_chave, letra_):
    """Painel de série por recorte climático: histórico + 3 janelas futuras em dois cenários."""
    t = TXT[lang]
    c = cor(tip)
    todos = [v for r in est["rec"].values() for v in r[metrica]]
    if tipo_unidade:
        div, unid = escolher_escala(todos, tipo_unidade, lang)
        ylab = t[ylabel_chave].format(u=unid)
    else:
        div, ylab = 1.0, t[ylabel_chave]
    esc = lambda ic: tuple(v / div for v in ic)  # noqa: E731
    h = esc(est["rec"][HIST][metrica])
    dod = {"SSP245": -0.09, "SSP585": 0.09}
    for cen, ls, mk, fill in (("SSP245", "-", "o", True), ("SSP585", (0, (4, 2)), "s", False)):
        ids = [r for r, _, cc in RECORTES if cc == cen]
        xs = [0] + [x + dod[cen] for r, x, cc in RECORTES if cc == cen]
        ys = [h[0]] + [esc(est["rec"][r][metrica])[0] for r in ids]
        ax.plot(xs, ys, ls=ls, color=c, lw=1.2, zorder=2)
        for r, x, cc in RECORTES:
            if cc == cen:
                ponto_ic(ax, x + dod[cen], 0, esc(est["rec"][r][metrica]), c, mk, False,
                         ms=4.6, fill=fill, lw=1.1)
    ponto_ic(ax, 0, 0, h, c, "o", False, ms=4.6, lw=1.1)
    ax.set_xlim(-0.45, 3.45)
    ax.set_xticks(range(4))
    ax.set_xticklabels([f"{j}\n{n}" for j, n in zip(
        ["1981–2010", "2021–2050", "2041–2070", "2071–2100"], t["rec"])], fontsize=6.5)
    ax.set_xlabel(t["rec_x"])
    ax.set_ylabel(ylab)
    ax.grid(axis="x", visible=False)
    ax.yaxis.set_major_formatter(_fmt(lang))
    if tipo_unidade and any(v < 0 for v in todos) and any(v > 0 for v in todos):
        ax.axhline(0, color=TINTA_2, lw=0.8, zorder=1)
    elif metrica != "economia_agua_potavel_pct":
        ax.axhline(0, color=TINTA_2, lw=0.8, zorder=1)
    letra(ax, f"({letra_}) " + t[titulo_chave])


def legenda_recortes(fig, tip, lang, ncol):
    from matplotlib.lines import Line2D
    t = TXT[lang]
    c = cor(tip)
    hs = [
        Line2D([], [], color=c, ls="-", marker="o", mfc=c, mec=TINTA, mew=0.6, ms=4.6, lw=1.2,
               label=t["l_ssp245"]),
        Line2D([], [], color=c, ls=(0, (4, 2)), marker="s", mfc="white", mec=TINTA, mew=0.6,
               ms=4.6, lw=1.2, label=t["l_ssp585"]),
        Line2D([], [], color=c, ls="none", marker="|", ms=7, mew=1.4, label=t["l_ic"]),
    ]
    fig.legend(handles=hs, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, 0.005),
               handletextpad=0.5, columnspacing=1.4)


def fig_tipologia(plt, tip, est, lang, coluna):
    larg = COLUNAS[coluna]
    if coluna == "dupla":
        fig, axs = plt.subplots(2, 2, figsize=(larg, 5.3))
        fig.subplots_adjust(left=0.11, right=0.985, top=0.955, bottom=0.14, hspace=0.52,
                            wspace=0.34)
        axs = list(axs.ravel())
        ncol = 3
    else:
        fig, axs = plt.subplots(4, 1, figsize=(larg, 9.0))
        fig.subplots_adjust(left=0.27, right=0.96, top=0.975, bottom=0.135, hspace=0.62)
        axs = list(axs)
        ncol = 1
    painel_volumes(axs[0], tip, est, lang)
    painel_recortes(axs[1], tip, est, lang, "economia_agua_potavel_pct", None, "agua_y", "agua", "b")
    painel_recortes(axs[2], tip, est, lang, "vpl", "moeda", "vpl_y", "vpl", "c")
    painel_recortes(axs[3], tip, est, lang, "co2_liquido_vida_kg", "massa", "co2_y", "co2", "d")
    legenda_recortes(fig, tip, lang, ncol)
    return fig


def _rotulos_tipologias(ax, lang, tips):
    ax.set_yticks(range(len(tips)))
    ax.set_yticklabels([x["nome"][lang] for x in tips])
    ax.set_ylim(len(tips) - 0.4, -0.6)
    ax.grid(axis="y", visible=False)


def fig_resumo(plt, dados, lang, coluna):
    """Resumo: seis tipologias em três painéis com linhas alinhadas (volume, viabilidade, ambiente)."""
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    t = TXT[lang]
    tips = [x for x, _ in dados]
    larg = COLUNAS[coluna]
    if coluna == "dupla":
        fig, axs = plt.subplots(1, 3, figsize=(larg, 3.5), sharey=True,
                                gridspec_kw={"width_ratios": [1.15, 1, 1]})
        fig.subplots_adjust(left=0.135, right=0.975, top=0.925, bottom=0.30, wspace=0.24)
    else:
        fig, axs = plt.subplots(3, 1, figsize=(larg, 8.2))
        fig.subplots_adjust(left=0.30, right=0.87, top=0.975, bottom=0.14, hspace=0.62)
    ax_v, ax_b, ax_p = axs
    simples = coluna == "simples"
    # (a) volumes em escala simétrica-log (zero preservado)
    ax_v.set_xscale("symlog", linthresh=1, linscale=0.5)
    for i, (tip, est) in enumerate(dados):
        c = cor(tip)
        ic = est["vol"]["smaa"]
        ax_v.hlines(i, ic[1], ic[2], color=c, lw=2.2, zorder=2, capstyle="round")
        for k, _, mk in CRITERIOS:
            if k in ("tec", "eco", "amb"):
                ax_v.plot([est["vol"][k][0]], [i], mk, ms=4.2, mfc=c, mec=TINTA, mew=0.5,
                          zorder=3, clip_on=False)
        ax_v.plot([ic[0]], [i], "o", ms=6.8, mfc=c, mec=TINTA, mew=0.7, zorder=4, clip_on=False)
    topo = max(est["vol"]["smaa"][2] for _, est in dados)
    ax_v.set_xlim(-0.15, topo * 1.3)
    ticks = [0] + [10 ** e for e in range(0, 4) if 10 ** e <= topo * 1.3]
    ax_v.set_xticks(ticks)
    ax_v.set_xticklabels([num_auto(v, lang) for v in ticks])
    ax_v.minorticks_off()
    ax_v.set_xlabel(t["vol_x"] + (" – symlog" if lang == "en-GB" else " – simétrica-log"))
    _rotulos_tipologias(ax_v, lang, tips)
    letra(ax_v, "(a) " + t["res_volume"])
    # (b) viabilidade: composição do VPL no recorte histórico
    for i, (tip, est) in enumerate(dados):
        c = cor(tip)
        s = est["share"]
        ax_b.barh(i, s["pos"], height=0.62, color=c, edgecolor=TINTA, linewidth=0.5, zorder=3)
        ax_b.barh(i, s["zero"], left=s["pos"], height=0.62, color="#e8e7e1", edgecolor=TINTA_2,
                  linewidth=0.5, hatch="....", zorder=3)
        ax_b.barh(i, s["neg"], left=s["pos"] + s["zero"], height=0.62, color="white",
                  edgecolor=TINTA, linewidth=0.5, hatch="////", zorder=3)
        ax_b.text(102, i, num(s["pos"], 0, lang) + " %", va="center", ha="left", fontsize=7,
                  fontweight="bold", color=TINTA, clip_on=False)
    ax_b.set_xlim(0, 100)
    ax_b.set_xticks([0, 25, 50, 75, 100])
    ax_b.set_xticklabels([num_auto(v, lang) for v in (0, 25, 50, 75, 100)])
    ax_b.set_xlabel(t["casos_pos_x"])
    ax_b.grid(axis="y", visible=False)
    letra(ax_b, "(b) " + t["res_viab"])
    # (c) payback ambiental (casos com reservatório)
    for i, (tip, est) in enumerate(dados):
        ponto_ic(ax_p, 0, i, est["pay"][:3], cor(tip), tip["marcador"], True, ms=5.8, lw=2.0)
    ax_p.set_xlim(left=0)
    ax_p.set_xlabel(t["payback_x"])
    ax_p.xaxis.set_major_formatter(_fmt(lang))
    ax_p.grid(axis="y", visible=False)
    letra(ax_p, "(c) " + t["res_amb"])
    if simples:
        for a in (ax_b, ax_p):
            _rotulos_tipologias(a, lang, tips)
    else:
        for a in (ax_b, ax_p):
            a.tick_params(axis="y", length=0)
    # legendas (neutras): critérios, composição e intervalo
    ink = dict(mfc="#9a9992", mec=TINTA, mew=0.6, ls="none")
    h_crit = [Line2D([], [], marker="^", ms=4.2, label=t["crit"]["tec"], **ink),
              Line2D([], [], marker="s", ms=4.2, label=t["crit"]["eco"], **ink),
              Line2D([], [], marker="D", ms=4.2, label=t["crit"]["amb"], **ink),
              Line2D([], [], marker="o", ms=6.5, label=t["crit"]["smaa"] + " (P10–P90)", **ink)]
    h_bar = [Patch(facecolor="#9a9992", edgecolor=TINTA, lw=0.5, label=t["l_pos"]),
             Patch(facecolor="#e8e7e1", edgecolor=TINTA_2, lw=0.5, hatch="....", label=t["l_zero"]),
             Patch(facecolor="white", edgecolor=TINTA, lw=0.5, hatch="////", label=t["l_neg"])]
    h_pay = [Line2D([], [], marker="o", ms=5, label=t["l_ic"].replace("; ", ";\n"), **ink)]
    if simples:
        fig.legend(handles=h_crit + h_bar, loc="lower center", ncol=2,
                   bbox_to_anchor=(0.5, 0.0), columnspacing=1.2, handletextpad=0.5)
    else:
        kw = dict(loc="upper left", handletextpad=0.5, columnspacing=1.0, borderaxespad=0)
        ax_v.legend(handles=h_crit, ncol=2, bbox_to_anchor=(-0.02, -0.25), **kw)
        ax_b.legend(handles=h_bar, ncol=1, bbox_to_anchor=(0.0, -0.25), **kw)
        ax_p.legend(handles=h_pay, ncol=1, bbox_to_anchor=(0.0, -0.25), **kw)
    return fig


# ───────────────────────── legendas ─────────────────────────
def _ic_txt(ic, d, lang, un=""):
    return (f"{num(ic[0], d, lang)}{un} (P10–P90: {num(ic[1], d, lang)}–{num(ic[2], d, lang)}{un})")


def legenda_tipologia(tip, est, arq, lang, n_fig) -> str:
    nome = tip["nome"][lang].replace("\n", " ")
    h = est["rec"][HIST]
    ult = "ssp585-2071-2100"
    zero = est["share"]["zero"]
    S = est["vol"]["smaa"]
    div_m, un_m = escolher_escala([v for r in est["rec"].values() for v in r["vpl"]], "moeda", lang)
    if lang == "pt-BR":
        t = (f"**Figura {n_fig}.** Reservatório de água de chuva, tipologia {nome.lower()}, em Santa "
             f"Catarina. Estudo `{tip['estudo']}`: {est['n_locais']} locais × 19 modelos "
             f"climáticos da CLIMBra × 7 recortes = {num(est['n_casos'], 0, lang)} casos; arquétipo com "
             f"{num(arq['area_captacao_m2'], 0, lang)} m² de captação e "
             f"{num(arq['usuarios'], 0, lang)} usuários. Em todos os painéis, o símbolo indica a "
             f"mediana e a barra, os percentis 10 e 90 entre locais e modelos. "
             f"(a) Volume ótimo por critério no recorte histórico (1981–2010; "
             f"n = {est['n_hist']}); o volume SMAA-VIKOR tem mediana de "
             f"{_ic_txt(S, 1, lang, ' m³')}. "
             f"(b) Economia de água potável: mediana de {num(h['economia_agua_potavel_pct'][0], 1, lang)} % "
             f"no histórico e de {num(est['rec'][ult]['economia_agua_potavel_pct'][0], 1, lang)} % em "
             f"2071–2100 (SSP5-8.5). (c) Valor presente líquido em 20 anos ({un_m}): "
             f"VPL > 0 em {num(est['pos_vpl'][HIST], 0, lang)} % dos casos no histórico e em "
             f"{num(est['pos_vpl'][ult], 0, lang)} % em 2071–2100 (SSP5-8.5). "
             f"(d) Saldo líquido de CO₂e em 20 anos: positivo em "
             f"{num(est['pos_co2'][HIST], 0, lang)} % dos casos no histórico e em "
             f"{num(est['pos_co2'][ult], 0, lang)} % em 2071–2100 (SSP5-8.5). ")
        if zero > 0:
            t += (f"Em {num(zero, 0, lang)} % dos casos históricos o SMAA-VIKOR indica volume "
                  f"nulo (VPL = 0, sem reservatório). ")
        t += ("Todos os valores vêm de `resultados.csv`; os parâmetros do arquétipo são "
              "estimativas, a refinar pelo autor.\n")
    else:
        t = (f"**Figure {n_fig}.** Rainwater-harvesting reservoir, {nome.lower()} typology, in Santa "
             f"Catarina. Study `{tip['estudo']}`: {est['n_locais']} sites × 19 CLIMBra climate "
             f"models × 7 windows = {num(est['n_casos'], 0, lang)} cases; archetype with "
             f"{num(arq['area_captacao_m2'], 0, lang)} m² of catchment and "
             f"{num(arq['usuarios'], 0, lang)} users. In every panel the symbol is the median and "
             f"the bar the 10th–90th percentile across sites and models. "
             f"(a) Optimal volume by criterion in the historical window (1981–2010; "
             f"n = {est['n_hist']}); the SMAA-VIKOR volume has a median of "
             f"{_ic_txt(S, 1, lang, ' m³')}. "
             f"(b) Potable-water saving: median of {num(h['economia_agua_potavel_pct'][0], 1, lang)}% "
             f"in the historical window and {num(est['rec'][ult]['economia_agua_potavel_pct'][0], 1, lang)}% in "
             f"2071–2100 (SSP5-8.5). (c) 20-year net present value ({un_m}): "
             f"NPV > 0 in {num(est['pos_vpl'][HIST], 0, lang)}% of cases in the historical window and in "
             f"{num(est['pos_vpl'][ult], 0, lang)}% in 2071–2100 (SSP5-8.5). "
             f"(d) 20-year net CO₂e balance: positive in "
             f"{num(est['pos_co2'][HIST], 0, lang)}% of cases in the historical window and in "
             f"{num(est['pos_co2'][ult], 0, lang)}% in 2071–2100 (SSP5-8.5). ")
        if zero > 0:
            t += (f"In {num(zero, 0, lang)}% of the historical cases SMAA-VIKOR selects no "
                  f"reservoir (NPV = 0). ")
        t += ("All values are taken from `resultados.csv`; archetype parameters are estimates "
              "to be refined by the author.\n")
    return t


def legenda_resumo(dados, lang, n_fig) -> str:
    def extremos(f, d, un=""):
        v = sorted(((f(e), x["nome"][lang].replace("\n", " ")) for x, e in dados))
        return (f"{v[0][1]} ({num(v[0][0], d, lang)}{un}) – {v[-1][1]} ({num(v[-1][0], d, lang)}{un})")
    vol = extremos(lambda e: e["vol"]["smaa"][0], 1, " m³")
    pos = extremos(lambda e: e["share"]["pos"], 0, " %")
    pay = extremos(lambda e: e["pay"][0], 1, " a" if lang == "pt-BR" else " yr")
    n_hist = sorted({e["n_hist"] for _, e in dados})
    n_txt = " / ".join(str(n) for n in n_hist)
    if lang == "pt-BR":
        return (f"**Figura {n_fig}.** Comparação das seis tipologias de edificação em Santa Catarina "
                f"no recorte histórico (1981–2010; 19 modelos da CLIMBra; n = {n_txt} casos por "
                f"tipologia, conforme o número de locais). Cada tipologia mantém cor e marcador em "
                f"todas as figuras. (a) Volume ótimo de reservatório em escala simétrica-log "
                f"(o zero é preservado): círculo grande = mediana do SMAA-VIKOR com barra de "
                f"percentis 10 a 90; triângulo, quadrado e losango = medianas dos ótimos técnico, "
                f"econômico e ambiental. Mediana do SMAA-VIKOR, menor a maior: {vol}. "
                f"(b) Composição dos casos por sinal do VPL em 20 anos; o número à direita é a "
                f"parcela com VPL > 0. Menor a maior: {pos}. (c) Payback ambiental (anos) nos casos "
                f"com reservatório, mediana e percentis 10 a 90. Menor a maior: {pay}. "
                f"Todos os valores vêm de `resultados.csv` de cada estudo.\n")
    return (f"**Figure {n_fig}.** Comparison of the six building typologies in Santa Catarina in the "
            f"historical window (1981–2010; 19 CLIMBra models; n = {n_txt} cases per typology, "
            f"depending on the number of sites). Each typology keeps its colour and marker in every "
            f"figure. (a) Optimal reservoir volume on a symmetric-log scale (zero is preserved): "
            f"large circle = SMAA-VIKOR median with a 10th–90th percentile bar; triangle, square "
            f"and diamond = medians of the technical, economic and environmental optima. SMAA-VIKOR "
            f"median, lowest to highest: {vol}. (b) Composition of cases by sign of the 20-year NPV; "
            f"the number on the right is the share with NPV > 0. Lowest to highest: {pos}. "
            f"(c) Environmental payback (years) for cases with a reservoir, median and 10th–90th "
            f"percentiles. Lowest to highest: {pay}. All values are taken from each study's "
            f"`resultados.csv`.\n")


# ───────────────────────── painel HTML ─────────────────────────
def dados_painel(dados, formatos) -> dict:
    out = []
    for tip, est in dados:
        rec = {r: {m: [round(v, 6) for v in ic] for m, ic in mm.items()} for r, mm in est["rec"].items()}
        out.append({
            "chave": tip["chave"], "slot": tip["slot"], "marcador": tip["marcador"],
            "nome": {l: tip["nome"][l].replace("\n", " ") for l in IDIOMAS},
            "n_casos": est["n_casos"], "n_hist": est["n_hist"], "n_locais": est["n_locais"],
            "vol": {k: [round(v, 6) for v in ic] for k, ic in est["vol"].items()},
            "share": {k: round(v, 6) for k, v in est["share"].items()},
            "pay": [round(v, 6) if isinstance(v, float) else v for v in est["pay"]],
            "rec": rec,
            "pos_vpl": {k: round(v, 6) for k, v in est["pos_vpl"].items()},
            "pos_co2": {k: round(v, 6) for k, v in est["pos_co2"].items()},
        })
    return {"tipologias": out, "cores_claro": CORES_CLARO, "cores_escuro": CORES_ESCURO,
            "formatos": list(formatos)}


def escrever_painel(dados, formatos, destino: Path):
    modelo = ESTUDOS / "painel_artigos_modelo.html"
    html = modelo.read_text(encoding="utf-8")
    js = json.dumps(dados_painel(dados, formatos), ensure_ascii=False, sort_keys=True,
                    separators=(",", ":"))
    destino.write_text(html.replace("/*__DADOS__*/null", js), encoding="utf-8", newline="\n")


# ───────────────────────── principal ─────────────────────────
def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gerar_graficos_artigos.py",
        description="Gera as figuras de publicação (PNG 300 dpi, SVG, PDF), as legendas sugeridas "
                    "(.md) e o painel dashboard_artigos.html dos seis estudos de Santa Catarina, "
                    "a partir dos resultados.csv já produzidos por 'triton estudo run'.")
    p.add_argument("--saida", type=Path, default=SAIDA_PADRAO,
                   help="pasta _saida dos estudos (padrão: estudos/santa-catarina/_saida)")
    p.add_argument("--idioma", choices=("pt-BR", "en-GB", "ambos"), default="ambos")
    p.add_argument("--coluna", choices=("dupla", "simples", "ambas"), default="ambas",
                   help="largura: dupla = 7,2 pol; simples = 3,46 pol")
    p.add_argument("--formatos", default="png,svg,pdf",
                   help="lista separada por vírgulas entre png, svg, pdf")
    p.add_argument("--sem-painel", action="store_true", help="não gerar dashboard_artigos.html")
    return p


def principal(argv=None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")
    args = construir_parser().parse_args(argv)
    formatos = [f.strip().lower() for f in args.formatos.split(",") if f.strip()]
    if not formatos or any(f not in FORMATOS for f in formatos):
        print(f"formatos inválidos: {args.formatos} (use {', '.join(FORMATOS)})", file=sys.stderr)
        return 2
    idiomas = IDIOMAS if args.idioma == "ambos" else (args.idioma,)
    colunas = tuple(COLUNAS) if args.coluna == "ambas" else (args.coluna,)
    saida: Path = args.saida
    plt = configurar_mpl()
    dados = []
    for tip in TIPOLOGIAS:
        if not (saida / tip["estudo"] / "resultados.csv").exists():
            print(f"falta {saida / tip['estudo'] / 'resultados.csv'}", file=sys.stderr)
            return 1
        dados.append((tip, estatisticas(tip, carregar(tip, saida))))
    arqs = {tip["chave"]: arquetipo(tip) for tip, _ in dados}
    raiz_fig = saida / "figuras_artigos"
    for lang in idiomas:
        for col in colunas:
            d = raiz_fig / lang / col
            fig = fig_resumo(plt, dados, lang, col)
            salvar(fig, d / "fig_resumo", formatos)
            plt.close(fig)
            for tip, est in dados:
                fig = fig_tipologia(plt, tip, est, lang, col)
                salvar(fig, d / f"fig_{tip['chave']}", formatos)
                plt.close(fig)
        (raiz_fig / lang).mkdir(parents=True, exist_ok=True)
        (raiz_fig / lang / "legenda_resumo.md").write_text(
            legenda_resumo(dados, lang, 1), encoding="utf-8", newline="\n")
        for i, (tip, est) in enumerate(dados, start=2):
            (raiz_fig / lang / f"legenda_{tip['chave']}.md").write_text(
                legenda_tipologia(tip, est, arqs[tip["chave"]], lang, i),
                encoding="utf-8", newline="\n")
        print(f"[{lang}] figuras e legendas em {raiz_fig / lang}")
    if not args.sem_painel:
        escrever_painel(dados, formatos, saida / "dashboard_artigos.html")
        print(f"painel em {saida / 'dashboard_artigos.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
