# -*- coding: utf-8 -*-
"""E-OBS v33.0e contra Iberia01 (rede densa de estações, 0,1 grau, 1971-2015) em toda a Península Ibérica.

Compara célula a célula, dia a dia. A grade da E-OBS (centros em x,05) é interpolada linearmente para a do Iberia01 (centros em x,0).
Resultados: iberia_celulas.npz (um valor por célula), iberia_resumo.csv (por país e região), iberia_tendencias.csv (concelhos suspeitos e controlos).
Uso: python iberia_eobs_vs_iberia01.py
"""
import os
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from shapely import contains_xy

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402

AQUI = C.RESULTADOS          # saídas
EOBS = C.EOBS_NC
IBER = C.IBERIA01_NC
CAOP = C.CAOP_CONTINENTE


def main():
    ib = xr.open_dataset(IBER)["pr"].load()                       # (tempo, lat, lon), kg m-2 = mm
    lat, lon, tempo = ib.lat.values, ib.lon.values, ib.time.values
    eo = xr.open_dataset(EOBS)["rr"].sel(time=slice("1971-01-01", "2015-12-31"), latitude=slice(lat.min() - .3, lat.max() + .3),
                                         longitude=slice(lon.min() - .3, lon.max() + .3)).load()
    assert len(eo.time) == len(tempo)
    # interpolar a E-OBS para os centros do Iberia01, em blocos de anos para poupar memória
    e = np.empty(ib.shape, dtype=np.float32)
    n = 0
    for a in range(1971, 2016):
        blk = eo.sel(time=str(a)).interp(latitude=lat, longitude=lon, method="linear")
        e[n:n + blk.sizes["time"]] = blk.values; n += blk.sizes["time"]
    i = ib.values.astype(np.float32)
    ok = np.isfinite(i).all(axis=0) & np.isfinite(e).all(axis=0)   # células com dado completo nas duas
    print("células válidas nas duas:", int(ok.sum()), "de", int(np.isfinite(i).all(axis=0).sum()), flush=True)
    ii, ee = i[:, ok], e[:, ok]
    ci, cj = np.where(ok)
    anos = len(tempo) / 365.25
    # métricas por célula
    tot_i, tot_e = ii.sum(0) / anos, ee.sum(0) / anos
    zi, ze = (ii - ii.mean(0)) / (ii.std(0) + 1e-9), (ee - ee.mean(0)) / (ee.std(0) + 1e-9)
    r = (zi * ze).mean(0)
    w_i, w_e = (ii >= 1).mean(0) * 100, (ee >= 1).mean(0) * 100
    p95_i = np.array([np.percentile(c[c >= 1], 95) if (c >= 1).sum() > 20 else np.nan for c in ii.T])
    p95_e = np.array([np.percentile(c[c >= 1], 95) if (c >= 1).sum() > 20 else np.nan for c in ee.T])
    anos_idx = pd.DatetimeIndex(tempo).year.values
    rx_i = np.stack([ii[anos_idx == a].max(0) for a in range(1971, 2016)]).mean(0)
    rx_e = np.stack([ee[anos_idx == a].max(0) for a in range(1971, 2016)]).mean(0)
    # país: Portugal continental por polígono (CAOP)
    caop = gpd.read_file(CAOP, layer="cont_municipios").to_crs(4326)
    uni = caop.geometry.union_all()
    la, lo = lat[ci], lon[cj]
    pt = contains_xy(uni, lo, la)
    d = pd.DataFrame(dict(lat=la, lon=lo, pt=pt, tot_iberia=tot_i, tot_eobs=tot_e, dtot_pct=(tot_e / tot_i - 1) * 100, r=r,
                          dias1mm_iberia=w_i, dias1mm_eobs=w_e, p95_iberia=p95_i, p95_eobs=p95_e, dp95_pct=(p95_e / p95_i - 1) * 100,
                          rx1_iberia=rx_i, rx1_eobs=rx_e, drx1_pct=(rx_e / rx_i - 1) * 100))
    d["regiao"] = np.where(d.pt & (d.lat >= 39.5), "Portugal norte", np.where(d.pt, "Portugal sul", np.where(d.lon > -1.0, "Espanha mediterrânica",
                    np.where(d.lat > 41.8, "Espanha norte", "Espanha interior e oeste"))))
    d.to_csv(os.path.join(AQUI, "iberia_celulas.csv"), index=False, encoding="utf-8-sig")
    g = d.groupby("regiao")
    res = g.agg(celulas=("r", "size"), tot_iberia=("tot_iberia", "median"), dtot_mediana=("dtot_pct", "median"), dtot_p10=("dtot_pct", lambda x: np.percentile(x, 10)),
                dtot_p90=("dtot_pct", lambda x: np.percentile(x, 90)), r_mediana=("r", "median"), dias1mm_eobs_med=("dias1mm_eobs", "median"),
                dp95_mediana=("dp95_pct", "median"), drx1_mediana=("drx1_pct", "median")).round(2)
    res.loc["Portugal (todo)"] = [int(d.pt.sum()), d[d.pt].tot_iberia.median(), d[d.pt].dtot_pct.median(), np.percentile(d[d.pt].dtot_pct, 10), np.percentile(d[d.pt].dtot_pct, 90),
                                  d[d.pt].r.median(), d[d.pt].dias1mm_eobs.median(), d[d.pt].dp95_pct.median(), d[d.pt].drx1_pct.median()]
    res.loc["Península (toda)"] = [len(d), d.tot_iberia.median(), d.dtot_pct.median(), np.percentile(d.dtot_pct, 10), np.percentile(d.dtot_pct, 90), d.r.median(),
                                   d.dias1mm_eobs.median(), d.dp95_pct.median(), d.drx1_pct.median()]
    res.to_csv(os.path.join(AQUI, "iberia_resumo.csv"), encoding="utf-8-sig"); print(res.to_string(), flush=True)
    # tendências 1971-2015 nos concelhos suspeitos e de controlo
    conc = pd.read_csv(os.path.join(AQUI, "concelhos.csv"), dtype={"dtmn": str}).set_index("concelho")
    alvo = ["Vouzela", "Oliveira de Frades", "São Pedro do Sul", "Vale de Cambra", "Sever do Vouga", "Tondela", "Viseu", "Guarda", "Braga", "Aveiro", "Coimbra", "Lisboa", "Faro", "Évora", "Castelo Branco"]
    Y = np.arange(1971, 2016); linhas = []
    for c in alvo:
        y0, x0 = float(conc.loc[c, "lat"]), float(conc.loc[c, "lon"])
        dist2 = (lat[:, None] - y0) ** 2 + (lon[None, :] - x0) ** 2
        dist2 = np.where(ok, dist2, np.inf)                       # célula válida mais próxima do ponto do concelho
        a, b = np.unravel_index(int(dist2.argmin()), dist2.shape)
        si, se = i[:, a, b], e[:, a, b]
        ti = np.array([si[anos_idx == y].sum() for y in Y]); te = np.array([se[anos_idx == y].sum() for y in Y])
        linhas.append(dict(concelho=c, mm_iberia01=round(float(ti.mean())), mm_eobs=round(float(te.mean())), tend_iberia01=round(np.polyfit(Y, ti, 1)[0] * 10, 1),
                           tend_eobs=round(np.polyfit(Y, te, 1)[0] * 10, 1), r_anual=round(float(np.corrcoef(ti, te)[0, 1]), 2)))
    t = pd.DataFrame(linhas); t.to_csv(os.path.join(AQUI, "iberia_tendencias.csv"), index=False, encoding="utf-8-sig"); print(t.to_string(index=False))


if __name__ == "__main__":
    main()
