# -*- coding: utf-8 -*-
"""Compara a E-OBS por concelho (portugal_eobs.db) com estações de precipitação diária.

Fontes das estações: ECA&D (nonblend, extraído só Portugal) e GHCN-Daily (NOAA).
Regras decididas pelo utilizador (painel, 22/10/2026): posto mais próximo do centroide do concelho, a até 15 km;
métricas: r diário, pbias, KGE mensal, frequência de dias >= 1 mm e >= 10 mm, P95 e máximo dos dias de chuva,
totais anuais e ciclo mensal. Período de comparação: 1991-2020 (só dias com dado válido nas duas séries).
Uma estação do ECA&D alimenta a E-OBS: o acordo ali não é independente (coluna `independente`).
Uso: python validar_eobs.py
"""
import csv, gzip, hashlib, os, re, sqlite3, sys, zipfile, zlib
import datetime as dt
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402

AQUI = C.RESULTADOS          # saídas
DB = C.BASE
CAOP = C.CAOP_CONTINENTE
ECAD_ZIP = os.path.join(C.BRUTOS, "ecad", "ECA_nonblend_rr.zip")
ECAD_PT = os.path.join(C.BRUTOS, "ecad", "pt")
GHCN = os.path.join(C.BRUTOS, "ghcnd")
LIMITE_KM = 15.0
MIN_DIAS = 1825            # pelo menos 5 anos de dias válidos nas duas séries em 1991-2020
D0, INI, FIM = dt.date(1950, 1, 1), dt.date(1991, 1, 1), dt.date(2020, 12, 31)


def dms(s):
    s = s.strip(); sinal = -1 if s[0] == "-" else 1
    g, m, sec = s[1:].split(":"); return sinal * (int(g) + int(m) / 60 + int(sec) / 3600)


def extrair_ecad():
    """Extrai só as fontes PT do zip (arquivos RR_SOUID*.txt); devolve {id: dict(nome, lat, lon, alt, arq)}."""
    os.makedirs(ECAD_PT, exist_ok=True)
    z = zipfile.ZipFile(ECAD_ZIP)
    nomes_zip = set(z.namelist())
    out = {}
    for l in z.read("sources.txt").decode("utf-8", "replace").splitlines():
        p = [x.strip() for x in l.split(",")]
        if len(p) >= 8 and p[0].isdigit() and p[2] == "PT" and p[6].startswith("RR"):
            sid = int(p[0]); nome = f"RR_SOUID{sid}.txt"
            if nome in nomes_zip:
                dest = os.path.join(ECAD_PT, nome)
                if not os.path.exists(dest):
                    open(dest, "wb").write(z.read(nome))
                out[f"ECAD{sid}"] = dict(nome=p[1], lat=dms(p[3]), lon=dms(p[4]), alt=float(p[5] or 0), arq=dest, fonte="ECA&D", indep=False)
    return out


def serie_ecad(arq):
    d = {}
    for l in open(arq, encoding="utf-8", errors="replace"):
        p = [x.strip() for x in l.split(",")]
        if len(p) >= 5 and p[2].isdigit() and len(p[2]) == 8 and p[4] == "0" and p[3] != "-9999":
            d[dt.date(int(p[2][:4]), int(p[2][4:6]), int(p[2][6:]))] = int(p[3]) / 10
    return d


def estacoes_ghcn():
    out = {}
    inv = {}
    for l in open(os.path.join(GHCN, "ghcnd-stations.txt"), encoding="utf-8"):
        if l.startswith("PO"):
            inv[l[:11]] = dict(nome=l[41:71].strip(), lat=float(l[12:20]), lon=float(l[21:30]), alt=float(l[31:37]))
    for f in os.listdir(GHCN):
        if f.endswith(".csv.gz"):
            i = f[:-7]
            if i in inv:
                out[i] = dict(inv[i], arq=os.path.join(GHCN, f), fonte="GHCN-D", indep=None)
    return out


def serie_ghcn(arq):
    d = {}
    for r in csv.reader(gzip.open(arq, "rt")):
        if r[2] == "PRCP" and r[5] == "":
            d[dt.date(int(r[1][:4]), int(r[1][4:6]), int(r[1][6:]))] = int(r[3]) / 10
    return d


def kge(obs, sim):
    r = np.corrcoef(obs, sim)[0, 1]; a = sim.std() / obs.std(); b = sim.mean() / obs.mean()
    return 1 - np.sqrt((r - 1) ** 2 + (a - 1) ** 2 + (b - 1) ** 2)


def main():
    ec = extrair_ecad(); gh = estacoes_ghcn()
    print("estações ECA&D PT:", len(ec), "| GHCN-D:", len(gh))
    est = dict(ec)
    # estação GHCN a menos de 10 km de uma do ECA&D é a mesma (as coordenadas diferem entre fontes): conta como ECA&D (alimenta a E-OBS)
    pts = gpd.GeoDataFrame({"id": list(ec)}, geometry=[Point(v["lon"], v["lat"]) for v in ec.values()], crs=4326).to_crs(3763)
    for i, v in gh.items():
        p = gpd.GeoSeries([Point(v["lon"], v["lat"])], crs=4326).to_crs(3763).iloc[0]
        dmin = pts.distance(p).min() / 1000 if len(pts) else 1e9
        # mesma estação se está a menos de 10 km de uma do ECA&D, ou a menos de 25 km com o mesmo primeiro nome (as coordenadas diferem entre fontes)
        pri = v["nome"].split("/")[0].split()[0].upper() if v["nome"] else ""
        mesmo_nome = any(e["nome"].upper().startswith(pri) and gpd.GeoSeries([Point(e["lon"], e["lat"])], crs=4326).to_crs(3763).iloc[0].distance(p) < 25000 for e in ec.values()) if pri else False
        v["indep"] = False if (dmin < 10 or mesmo_nome) else True
        v["dup_ecad_km"] = round(float(dmin), 2)
        est[i] = v
    gdf = gpd.GeoDataFrame({"id": list(est)}, geometry=[Point(v["lon"], v["lat"]) for v in est.values()], crs=4326).to_crs(3763)
    # só as que têm dados em 1991-2020 e estão no continente
    caop = gpd.read_file(CAOP, layer="cont_municipios").to_crs(3763)
    cent = caop.geometry.centroid
    series = {}
    for i, v in est.items():
        s = serie_ecad(v["arq"]) if v["fonte"] == "ECA&D" else serie_ghcn(v["arq"])
        n = sum(1 for d in s if INI <= d <= FIM)
        if n >= MIN_DIAS and v["lat"] > 36.5 and v["lon"] > -10 and 36.8 < v["lat"] < 42.3:
            series[i] = s
    print("estações do continente com >=5 anos em 1991-2020:", len(series), "| independentes:", sum(1 for i in series if est[i]["indep"]))
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    nomes = {r[0]: r[1] for r in db.execute("select dtmn,concelho from series")}
    linhas = []
    for k, row in caop.iterrows():
        if row["dtmn"] not in nomes:
            continue
        c = cent.iloc[k]
        cand = [(gdf.geometry.iloc[j].distance(c) / 1000, gdf.id.iloc[j]) for j in range(len(gdf)) if gdf.id.iloc[j] in series]
        if not cand:
            continue
        cand.sort()
        # a mais próxima dentro do limite; se a mais próxima não tiver dados suficientes em comum, tenta a seguinte
        blob = db.execute("select dados from series where dtmn=?", (row["dtmn"],)).fetchone()[0]
        e = np.frombuffer(zlib.decompress(blob), dtype=np.float32).astype(float)
        for dist, sid in cand:
            if dist > LIMITE_KM:
                break
            s = series[sid]
            dias = [d for d in s if INI <= d <= FIM]
            ix = np.array([(d - D0).days for d in dias]); x = np.array([s[d] for d in dias]); y = e[ix]
            ok = ~np.isnan(y); x, y, dias = x[ok], y[ok], [d for d, o in zip(dias, ok) if o]
            if len(x) < MIN_DIAS:
                continue
            anos = len(x) / 365.25
            mm = {}
            for d, a, b in zip(dias, x, y):
                m = mm.setdefault((d.year, d.month), [0.0, 0.0, 0]); m[0] += a; m[1] += b; m[2] += 1
            cheios = [v for v in mm.values() if v[2] >= 28]
            ko = np.array([v[0] for v in cheios]); ks = np.array([v[1] for v in cheios])
            clim_o = [np.mean([v[0] for (y_, m_), v in mm.items() if m_ == m and v[2] >= 28] or [np.nan]) for m in range(1, 13)]
            clim_s = [np.mean([v[1] for (y_, m_), v in mm.items() if m_ == m and v[2] >= 28] or [np.nan]) for m in range(1, 13)]
            wo, ws = x[x >= 1], y[y >= 1]
            st = est[sid]
            linhas.append(dict(
                dtmn=row["dtmn"], concelho=nomes[row["dtmn"]], estacao=st["nome"], id=sid, fonte=st["fonte"],
                independente="nao" if st["indep"] is False else "sim", dist_km=round(dist, 1), alt_estacao=st["alt"], dias=len(x), anos_equiv=round(anos, 1),
                mm_ano_estacao=round(x.sum() / anos), mm_ano_eobs=round(y.sum() / anos),
                pbias_pct=round((y.sum() - x.sum()) / x.sum() * 100, 1), r_diario=round(float(np.corrcoef(x, y)[0, 1]), 3),
                kge_mensal=round(float(kge(ko, ks)), 3) if len(ko) >= 24 else "",
                r_ciclo_mensal=round(float(np.corrcoef(clim_o, clim_s)[0, 1]), 3),
                dias_1mm_estacao_pct=round((x >= 1).mean() * 100, 1), dias_1mm_eobs_pct=round((y >= 1).mean() * 100, 1),
                dias_10mm_ano_estacao=round((x >= 10).sum() / anos, 1), dias_10mm_ano_eobs=round((y >= 10).sum() / anos, 1),
                p95_estacao=round(float(np.percentile(wo, 95)), 1), p95_eobs=round(float(np.percentile(ws, 95)), 1),
                max_estacao=round(float(x.max()), 1), max_eobs=round(float(y.max()), 1)))
            break
    saida = os.path.join(AQUI, "resultados_por_concelho.csv")
    with open(saida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    print("concelhos comparados:", len(linhas), "->", saida)


if __name__ == "__main__":
    main()
