"""Replica, com o Triton, o desenho do artigo climático de 2026, numa amostra.

Artigo: Projected Climate Change Impacts on Rainwater Harvesting in Brazilian
Single-Family Houses (Water, 2026). Arquétipo: 60 m² de cobertura, quatro
moradores, 150 L/pessoa·dia, 30% de uso não potável, coeficiente 0,80, descarte de
2 mm; cisterna de 500 L com caixa de 250 L (cenário S2). Séries: base CLIMBra,
19 modelos do CMIP6, histórico (1980–2013), SSP2-4.5 e SSP5-8.5 (2015–2100,
partidos em futuro próximo até 2059 e futuro distante a partir de 2060).
"""
import json
import os
import re
import statistics
import sys

from pathlib import Path

RAIZ = str(Path(__file__).resolve().parents[2])
BASE = os.path.join(RAIZ, "climbra_data")
if not os.path.isdir(BASE):
    BASE = os.path.join(RAIZ, "Triton future files for 652 cities")
sys.path.insert(0, RAIZ)

from triton.core.parser import load_precipitation          # noqa: E402
from triton.core.simulation import run_single_simulation   # noqa: E402

CIDADES = ["Florianópolis", "Manaus", "Fortaleza", "Brasília"]
CONFIG = dict(area=60.0, runoff_coeff=0.80, discard_mm=2.0, discard_mode=1,
              total_demand_per_day=600.0, rainwater_share=0.30,
              upper_tank_vol=250.0, upper_tank_used=True, pumping_threshold=100.0)
CISTERNA = 500.0            # cenário S2 do artigo
DIAS_ANO = 365.25
CORTE_FUTURO = int(45 * DIAS_ANO)   # 2015–2059 é o futuro próximo


def arquivos_da_cidade(cidade):
    alvo = cidade.lower()
    achados = {}
    with os.scandir(BASE) as it:
        for e in it:
            if not e.name.lower().endswith(".csv"):
                continue
            m = re.match(r"\(Triton\)(.+?)_(.+?)_(Hist[óo]rico|SSP245|SSP585)\.csv$", e.name)
            if not m or m.group(1).lower() != alvo:
                continue
            achados.setdefault(m.group(2), {})[m.group(3).replace("ó", "o")] = e.path
    return achados


def simular(serie):
    r = run_single_simulation(precip_data=serie, lower_tank_vol=CISTERNA, **CONFIG)
    anos = len(serie) / DIAS_ANO
    return (r.potential_potable_savings_pct, r.avg_spilled_l_day * DIAS_ANO / 1000.0,
            float(serie.sum()) / anos)


def main():
    saida = {}
    for cidade in CIDADES:
        modelos = arquivos_da_cidade(cidade)
        if not modelos:
            print(f"{cidade}: sem arquivos na base")
            continue
        linhas = {"historico": [], "245_proximo": [], "245_distante": [],
                  "585_proximo": [], "585_distante": []}
        for modelo, arquivos in sorted(modelos.items()):
            if "Historico" in arquivos:
                linhas["historico"].append(simular(load_precipitation(arquivos["Historico"])))
            for ssp, rotulo in (("SSP245", "245"), ("SSP585", "585")):
                if ssp not in arquivos:
                    continue
                serie = load_precipitation(arquivos[ssp])
                linhas[f"{rotulo}_proximo"].append(simular(serie[:CORTE_FUTURO]))
                linhas[f"{rotulo}_distante"].append(simular(serie[CORTE_FUTURO:]))
        resumo = {}
        for chave, valores in linhas.items():
            if not valores:
                continue
            resumo[chave] = {
                "modelos": len(valores),
                "potencial_medio": round(statistics.fmean(v[0] for v in valores), 2),
                "potencial_min": round(min(v[0] for v in valores), 2),
                "potencial_max": round(max(v[0] for v in valores), 2),
                "extravasado_m3_ano": round(statistics.fmean(v[1] for v in valores), 1),
                "chuva_anual_mm": round(statistics.fmean(v[2] for v in valores), 0),
            }
        base = resumo.get("historico", {}).get("potencial_medio")
        for chave, r in resumo.items():
            if base:
                r["variacao_vs_historico_pp"] = round(r["potencial_medio"] - base, 2)
        saida[cidade] = resumo
        print(f"\n{cidade} ({len(modelos)} modelos)")
        for chave, r in resumo.items():
            print(f"  {chave:<15} potencial {r['potencial_medio']:5.2f}% "
                  f"[{r['potencial_min']:.2f}–{r['potencial_max']:.2f}] "
                  f"chuva {r['chuva_anual_mm']:.0f} mm  extravasa {r['extravasado_m3_ano']:.1f} m³/ano "
                  f"{'' if chave == 'historico' else f'({r[chr(118)+chr(97)+chr(114)+chr(105)+chr(97)+chr(99)+chr(97)+chr(111)+chr(95)+chr(118)+chr(115)+chr(95)+chr(104)+chr(105)+chr(115)+chr(116)+chr(111)+chr(114)+chr(105)+chr(99)+chr(111)+chr(95)+chr(112)+chr(112)]:+.2f} p.p.)'}")
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "replicacao_clima.json")
    json.dump(saida, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\ngravado em", destino)


if __name__ == "__main__":
    main()
