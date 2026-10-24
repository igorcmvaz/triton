# -*- coding: utf-8 -*-
"""CPC Global Unified Gauge-Based Analysis (NOAA PSL, 0,5 graus) contra estações do GHCN-Daily em Portugal, 1991-2020.
Acesso por OPeNDAP (psl.noaa.gov/thredds): extrai uma caixa que cobre o continente, uma vez por ano, e guarda em dados_brutos/cpc/.
Uso: python testar_cpc.py
"""
import os, time
import datetime as dt
import numpy as np
import xarray as xr
import comparar_fontes as cf

AQUI = cf.AQUI
DEST = os.path.join(cf.C.BRUTOS, "cpc")
LAT0, LAT1, LON0, LON1 = 36.5, 42.5, 350.0, 354.5          # 10 O a 5,5 O


def caixa():
    os.makedirs(DEST, exist_ok=True)
    for ano in range(1991, 2021):
        arq = os.path.join(DEST, f"cpc_pt_{ano}.nc")
        if os.path.exists(arq):
            continue
        for t in range(5):
            try:
                ds = xr.open_dataset(f"https://psl.noaa.gov/thredds/dodsC/Datasets/cpc_global_precip/precip.{ano}.nc", engine="netcdf4")
                x = ds.precip.sel(lat=slice(LAT1, LAT0), lon=slice(LON0, LON1)).load()
                x.to_netcdf(arq); ds.close(); print(ano, "ok", flush=True); break
            except Exception as e:
                print(ano, "tentativa", t, e, flush=True); time.sleep(20)


def serie(lat, lon):
    out = {}
    for ano in range(1991, 2021):
        x = xr.open_dataarray(os.path.join(DEST, f"cpc_pt_{ano}.nc")).sel(lat=lat, lon=lon % 360, method="nearest")
        for t, v in zip(x.time.values, x.values):
            if v == v and v > -900:
                out[dt.date.fromisoformat(str(t)[:10])] = float(v)
    return out


def main():
    caixa()
    import csv
    linhas = []
    for sid, conc, indep, lat, lon in cf.PONTOS:
        g = {d: v for d, v in cf.ghcn(sid).items() if cf.INI <= d <= cf.FIM}
        s = serie(lat, lon)
        dias = sorted(d for d in g if d in s)
        if len(dias) < 1500:
            continue
        x = np.array([g[d] for d in dias]); y = np.array([s[d] for d in dias]); anos = len(x) / 365.25
        mm = {}
        for d, a, b in zip(dias, x, y):
            v = mm.setdefault((d.year, d.month), [0.0, 0.0, 0]); v[0] += a; v[1] += b; v[2] += 1
        ch = [v for v in mm.values() if v[2] >= 28]
        linhas.append(dict(estacao=conc, independente={True: "sim", False: "nao", None: "?"}[indep], fonte="CPC", dias=len(x),
                           pbias=round((y.sum() - x.sum()) / x.sum() * 100, 1), r=round(float(np.corrcoef(x, y)[0, 1]), 2),
                           kge_mensal=round(float(cf.kge(np.array([v[0] for v in ch]), np.array([v[1] for v in ch]))), 2) if len(ch) >= 24 else "",
                           dias1mm_est=round((x >= 1).mean() * 100, 1), dias1mm_fonte=round((y >= 1).mean() * 100, 1),
                           p95_est=round(float(np.percentile(x[x >= 1], 95)), 1), p95_fonte=round(float(np.percentile(y[y >= 1], 95)), 1)))
    out = os.path.join(AQUI, "comparacao_cpc.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    for l in linhas:
        print("%-15s %-3s CPC dias=%5d pbias=%6.1f r=%.2f kge=%s d1mm %.1f/%.1f p95 %.1f/%.1f" % (l["estacao"], l["independente"], l["dias"], l["pbias"], l["r"], l["kge_mensal"], l["dias1mm_est"], l["dias1mm_fonte"], l["p95_est"], l["p95_fonte"]))


if __name__ == "__main__":
    main()
