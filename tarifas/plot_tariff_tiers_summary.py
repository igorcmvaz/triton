#!/usr/bin/env python3
"""
Gera gráfico resumo científico e executivo da estrutura tarifária por faixas de consumo,
tarifas fixas e alíquotas de esgoto para o catálogo nacional do Netuno 5 (652 cidades).

Exporta:
  - outputs/grafico_resumo_tarifas_faixas.png (300 DPI)
  - outputs/grafico_resumo_tarifas_faixas.pdf (Vetorial)
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# Reconfigura stdout
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "tarifas" / "brazil_cities_tariffs.json"
OUT_DIR = ROOT / "outputs"


def calculate_bill(city_data: dict, volume_m3: float) -> tuple[float, float, float]:
    """Calcula (valor_agua, valor_esgoto, valor_total) para um dado volume mensal."""
    faixas = city_data.get("faixas", [])
    tarifa_fixa = float(city_data.get("tarifa_fixa_mensal", 0.0) or 0.0)
    esgoto_pct = float(city_data.get("esgoto_pct", 80.0) or 80.0)

    # 1. Parcela de água
    agua_val = 0.0
    tem_minima_fixa = False
    
    for inf, sup, rate, t_tipo in faixas:
        if t_tipo == -1 and volume_m3 <= sup:
            # Tarifa mínima fixa
            agua_val = max(agua_val, rate)
            tem_minima_fixa = True
        elif t_tipo == 1:
            if volume_m3 > inf:
                vol_na_faixa = min(volume_m3, sup) - inf
                agua_val += vol_na_faixa * rate

    if tem_minima_fixa and tarifa_fixa > 0 and agua_val < tarifa_fixa:
        agua_val = tarifa_fixa
    elif tarifa_fixa > 0 and not tem_minima_fixa:
        agua_val += tarifa_fixa

    esgoto_val = agua_val * (esgoto_pct / 100.0)
    return agua_val, esgoto_val, agua_val + esgoto_val


def get_marginal_rate(city_data: dict, vol: float) -> float:
    """Retorna a tarifa marginal (R$/m³) no ponto de consumo vol."""
    faixas = city_data.get("faixas", [])
    for inf, sup, rate, t_tipo in faixas:
        if t_tipo == 1 and inf <= vol < sup:
            return rate
        if t_tipo == -1 and vol <= sup:
            # Se for mínima fixa até sup (ex: 10 m3), taxa média unitária = rate/sup
            return rate / max(1.0, sup) if sup > 0 else 0.0
    if faixas:
        # Pega a última faixa marginal
        m_faixas = [f for f in faixas if f[3] == 1]
        if m_faixas:
            return m_faixas[-1][2]
    return float(city_data.get("tarifa_base_agua_r_m3", 5.0) or 5.0)


def main():
    if not DB_PATH.exists():
        print(f"Erro: Banco de tarifas não encontrado em {DB_PATH}")
        sys.exit(1)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    cities = db.get("cities", {})
    print(f"Carregadas {len(cities)} cidades de {DB_PATH}")

    # Configuração estética do Matplotlib
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.edgecolor"] = "#334155"
    plt.rcParams["axes.linewidth"] = 0.9
    plt.rcParams["grid.color"] = "#e2e8f0"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.7

    fig = plt.figure(figsize=(16, 11), dpi=300)
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.22, top=0.91, bottom=0.07, left=0.07, right=0.96)

    # -------------------------------------------------------------------------------------------------------------
    # PAINEL A: CURVAS DE DEGRAUS TARIFÁRIOS (TARIFA MARGINAL R$/m³ vs CONSUMO)
    # -------------------------------------------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    
    selected_capitals = [
        ("SP - São Paulo", "SABESP (SP)", "#1e3a8a", "-"),
        ("RJ - Rio de Janeiro", "Águas do Rio (RJ)", "#0284c7", "-"),
        ("MG - Belo Horizonte", "COPASA (MG)", "#059669", "-"),
        ("SC - Florianópolis", "CASAN (SC)", "#dc2626", "-"),
        ("PR - Curitiba", "SANEPAR (PR)", "#d97706", "-"),
        ("DF - Brasília", "CAESB (DF)", "#7c3aed", "-"),
        ("BA - Salvador", "EMBASA (BA)", "#db2777", "--"),
        ("PE - Recife", "COMPESA (PE)", "#ea580c", "--"),
        ("CE - Fortaleza", "CAGECE (CE)", "#4b5563", "--"),
        ("AM - Manaus", "Águas de Manaus (AM)", "#0d9488", ":"),
    ]

    vols = np.linspace(0.1, 50, 500)

    for key, label, color, lstyle in selected_capitals:
        c_data = cities.get(key)
        if not c_data:
            continue
        rates = [get_marginal_rate(c_data, v) for v in vols]
        ax1.plot(vols, rates, label=label, color=color, linestyle=lstyle, linewidth=2.0, alpha=0.9)

    ax1.set_title("A) Estrutura Progressiva por Faixas: Tarifa Marginal de Água (R$/m³)", fontsize=11, fontweight="bold", pad=10, color="#0f172a")
    ax1.set_xlabel("Volume Consumido Mensal (m³/mês)", fontsize=9.5, fontweight="bold", color="#334155")
    ax1.set_ylabel("Tarifa Marginal (R$ / m³)", fontsize=9.5, fontweight="bold", color="#334155")
    ax1.set_xlim(0, 50)
    ax1.set_ylim(0, 35)
    ax1.grid(True)
    ax1.legend(loc="upper left", fontsize=8.2, framealpha=0.95, edgecolor="#cbd5e1", ncol=2)

    # Anotação de faixas típicas de consumo
    ax1.axvspan(0, 10, color="#f1f5f9", alpha=0.5, zorder=0)
    ax1.axvspan(10, 20, color="#e2e8f0", alpha=0.3, zorder=0)
    ax1.axvspan(20, 50, color="#f8fafc", alpha=0.5, zorder=0)
    ax1.text(5, 33, "Faixa 1\n(0-10 m³)", ha="center", fontsize=7.5, color="#64748b", fontweight="bold")
    ax1.text(15, 33, "Faixa 2\n(10-20 m³)", ha="center", fontsize=7.5, color="#64748b", fontweight="bold")
    ax1.text(35, 33, "Faixas 3 e 4\n(20-50 m³)", ha="center", fontsize=7.5, color="#64748b", fontweight="bold")

    # -------------------------------------------------------------------------------------------------------------
    # PAINEL B: CURVAS DE FATURA TOTAL MENSAL (ÁGUA + ESGOTO + FIXO)
    # -------------------------------------------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])

    vols_bill = np.linspace(0, 40, 300)
    for key, label, color, lstyle in selected_capitals[:7]:  # 7 principais
        c_data = cities.get(key)
        if not c_data:
            continue
        bills = [calculate_bill(c_data, v)[2] for v in vols_bill]
        ax2.plot(vols_bill, bills, label=label, color=color, linestyle=lstyle, linewidth=2.2, alpha=0.95)

    ax2.set_title("B) Fatura Mensal Total Simulada (Água + Esgoto + Parcela Fixa)", fontsize=11, fontweight="bold", pad=10, color="#0f172a")
    ax2.set_xlabel("Volume Consumido Mensal (m³/mês)", fontsize=9.5, fontweight="bold", color="#334155")
    ax2.set_ylabel("Valor Total da Fatura (R$ / mês)", fontsize=9.5, fontweight="bold", color="#334155")
    ax2.set_xlim(0, 40)
    ax2.set_ylim(0, 600)
    ax2.grid(True)
    ax2.legend(loc="upper left", fontsize=8.5, framealpha=0.95, edgecolor="#cbd5e1")

    # Linha guia para consumo de família de 4 pessoas (15 m3/mês)
    ax2.axvline(15, color="#dc2626", linestyle=":", linewidth=1.5, alpha=0.8)
    ax2.text(15.5, 520, "Consumo Médio\nResidencial (15 m³/mês)", fontsize=8, color="#dc2626", fontweight="bold")

    # -------------------------------------------------------------------------------------------------------------
    # PAINEL C: DISTRIBUIÇÃO NACIONAL DAS TARIFAS MARGINAIS POR FAIXA (652 CIDADES)
    # -------------------------------------------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])

    tier_eval_pts = [5.0, 15.0, 25.0, 40.0, 60.0]
    tier_names = ["Faixa 1\n(0–10 m³)", "Faixa 2\n(11–20 m³)", "Faixa 3\n(21–30 m³)", "Faixa 4\n(31–50 m³)", "Faixa 5\n(> 50 m³)"]
    
    tier_data = []
    for pt in tier_eval_pts:
        rates_pt = [get_marginal_rate(c, pt) for c in cities.values()]
        # Filtra outliers absurdos para visualização clara
        rates_clean = [r for r in rates_pt if 0 < r < 50]
        tier_data.append(rates_clean)

    box = ax3.boxplot(
        tier_data,
        tick_labels=tier_names,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="o", markeredgecolor="#1e293b", markerfacecolor="#ffffff", markersize=6),
        medianprops=dict(color="#b91c1c", linewidth=2.0),
        whiskerprops=dict(color="#64748b", linewidth=1.2),
        capprops=dict(color="#64748b", linewidth=1.2),
        flierprops=dict(marker=".", markersize=4, alpha=0.3, markeredgecolor="#94a3b8")
    )

    colors_box = ["#dbeafe", "#bfdbfe", "#93c5fd", "#60a5fa", "#3b82f6"]
    for patch, c in zip(box["boxes"], colors_box):
        patch.set_facecolor(c)
        patch.set_edgecolor("#1e40af")
        patch.set_linewidth(1.2)

    # Anotações de medianas
    for i, data_pts in enumerate(tier_data):
        med = np.median(data_pts)
        ax3.text(i + 1, med + 0.8, f"R$ {med:.2f}", ha="center", fontsize=8.5, fontweight="bold", color="#1e293b")

    ax3.set_title("C) Distribuição Nacional da Tarifa Marginal de Água por Faixa (652 Municípios)", fontsize=11, fontweight="bold", pad=10, color="#0f172a")
    ax3.set_xlabel("Faixas Volumétricas de Consumo", fontsize=9.5, fontweight="bold", color="#334155")
    ax3.set_ylabel("Tarifa Marginal de Água (R$ / m³)", fontsize=9.5, fontweight="bold", color="#334155")
    ax3.set_ylim(0, 30)
    ax3.grid(True, axis="y")

    # -------------------------------------------------------------------------------------------------------------
    # PAINEL D: PARCELA FIXA E ALÍQUOTA DE ESGOTO POR MACRORREGIÃO
    # -------------------------------------------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])

    regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    reg_fixed = []
    reg_esgoto = []
    
    for r in regioes:
        c_reg = [c for c in cities.values() if c.get("regiao") == r]
        fixed_vals = [float(c.get("tarifa_fixa_mensal", 0.0) or 0.0) for c in c_reg]
        esg_vals = [float(c.get("esgoto_pct", 80.0) or 80.0) for c in c_reg]
        reg_fixed.append(np.mean(fixed_vals) if fixed_vals else 0)
        reg_esgoto.append(np.mean(esg_vals) if esg_vals else 80)

    x = np.arange(len(regioes))
    width = 0.35

    ax4_twin = ax4.twinx()
    
    bars1 = ax4.bar(x - width/2, reg_fixed, width, label="Parcela Fixa Média (R$/mês)", color="#0284c7", edgecolor="#0369a1", alpha=0.9)
    bars2 = ax4_twin.bar(x + width/2, reg_esgoto, width, label="Alíquota Esgoto Média (% água)", color="#f97316", edgecolor="#c2410c", alpha=0.9)

    ax4.set_title("D) Parcela Fixa Mensal e Alíquota de Esgoto por Região Geográfica", fontsize=11, fontweight="bold", pad=10, color="#0f172a")
    ax4.set_xlabel("Região do Brasil", fontsize=9.5, fontweight="bold", color="#334155")
    ax4.set_ylabel("Parcela Fixa Mensal de Água (R$ / mês)", fontsize=9.5, fontweight="bold", color="#0369a1")
    ax4_twin.set_ylabel("Alíquota Média de Esgoto (% sobre água)", fontsize=9.5, fontweight="bold", color="#c2410c")
    
    ax4.set_xticks(x)
    ax4.set_xticklabels(regioes, fontsize=9, fontweight="bold", color="#334155")
    ax4.set_ylim(0, 60)
    ax4_twin.set_ylim(0, 110)
    ax4.grid(True, axis="y")

    # Rótulos nas barras
    for b in bars1:
        h = b.get_height()
        ax4.text(b.get_x() + b.get_width()/2., h + 1.2, f"R$ {h:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#0369a1")
    for b in bars2:
        h = b.get_height()
        ax4_twin.text(b.get_x() + b.get_width()/2., h + 2.0, f"{h:.0f}%", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#c2410c")

    # Legenda combinada
    lines_labels = [bars1, bars2]
    labels = ["Parcela Fixa (R$/mês)", "Esgoto (% água)"]
    ax4.legend(lines_labels, labels, loc="upper left", fontsize=8.5, framealpha=0.95, edgecolor="#cbd5e1")

    # Título Principal Superior
    fig.suptitle("Panorama Nacional da Estrutura Tarifária de Água e Esgoto — Netuno 5 (652 Municípios)", fontsize=14, fontweight="bold", color="#0f172a")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / "grafico_resumo_tarifas_faixas.png"
    pdf_path = OUT_DIR / "grafico_resumo_tarifas_faixas.pdf"

    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    plt.close()

    print(f" [Gráfico] Imagem PNG (300 DPI) salva em: {png_path} ({png_path.stat().st_size:,} bytes)")
    print(f" [Gráfico] Arquivo PDF vetorial salvo em : {pdf_path} ({pdf_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
