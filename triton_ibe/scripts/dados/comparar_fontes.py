# -*- coding: utf-8 -*-
"""Compara E-OBS, ERA5, ERA5-Land e CERRA (Open-Meteo, CC BY 4.0) com estações GHCN-Daily, 1991-2020, dia a dia.

Cada resposta da Open-Meteo é guardada em dados_brutos/openmeteo/ (JSON), com a data de acesso.
Uso: python comparar_fontes.py
"""
import csv, gzip, json, os, sqlite3, time, urllib.error, urllib.request, zlib
import datetime as dt
import numpy as np

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402

AQUI = C.RESULTADOS          # saídas
DB = C.BASE
OM = os.path.join(C.BRUTOS, "openmeteo")
GH = os.path.join(C.BRUTOS, "ghcnd")
MODELOS = ["era5", "era5_land", "cerra"]
# estação GHCN, concelho da E-OBS, independente da E-OBS?, latitude, longitude
PONTOS = [("POM00008554", "Faro", True, 37.014, -7.966), ("POM00008558", "Évora", True, 38.533, -7.900),
          ("POM00008570", "Castelo Branco", True, 39.833, -7.483), ("POM00008548", "Coimbra", None, 40.150, -8.467),
          ("PO000008535", "Lisboa", False, 38.7167, -9.15), ("PO000008546", "Porto", False, 41.1331, -8.60),
          ("PO000008562", "Beja", False, 38.0167, -7.8667), ("PO000008575", "Bragança", False, 41.80, -6.7331)]
D0, INI, FIM = dt.date(1950, 1, 1), dt.date(1991, 1, 1), dt.date(2020, 12, 31)


def om(modelo, lat, lon):
    arq = os.path.join(OM, f"{modelo}_{lat:.3f}_{lon:.3f}_1991-2020.json")
    if not os.path.exists(arq):
        url = ("https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s&start_date=1991-01-01&end_date=2020-12-31"
               "&daily=precipitation_sum&timezone=UTC&models=%s" % (lat, lon, modelo))
        for tentativa in range(10):
            try:
                dados = urllib.request.urlopen(url, timeout=120).read(); break
            except urllib.error.HTTPError as e:
                if e.code != 429 or tentativa == 9:
                    raise
                time.sleep(75)           # limite da API gratuita (por minuto/hora): espera e repete
        time.sleep(3)
        j = json.loads(dados); j["_acesso"] = dt.datetime.now(dt.timezone.utc).isoformat(); j["_url"] = url
        open(arq, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False))
    j = json.load(open(arq, encoding="utf-8"))
    return {dt.date.fromisoformat(t): v for t, v in zip(j["daily"]["time"], j["daily"]["precipitation_sum"]) if v is not None}


def ghcn(i):
    d = {}
    for r in csv.reader(gzip.open(os.path.join(GH, i + ".csv.gz"), "rt")):
        if r[2] == "PRCP" and r[5] == "":
            d[dt.date(int(r[1][:4]), int(r[1][4:6]), int(r[1][6:]))] = int(r[3]) / 10
    return d


def eobs(db, c):
    b = db.execute("select dados from series where concelho=?", (c,)).fetchone()[0]
    e = np.frombuffer(zlib.decompress(b), dtype=np.float32).astype(float)
    return {D0 + dt.timedelta(days=i): float(v) for i, v in enumerate(e) if INI <= D0 + dt.timedelta(days=i) <= FIM and v == v}


def kge(o, s):
    r = np.corrcoef(o, s)[0, 1]; return 1 - np.sqrt((r - 1) ** 2 + (s.std() / o.std() - 1) ** 2 + (s.mean() / o.mean() - 1) ** 2)


def main():
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    linhas = []
    for sid, conc, indep, lat, lon in PONTOS:
        g = {d: v for d, v in ghcn(sid).items() if INI <= d <= FIM}
        fontes = {"E-OBS": eobs(db, conc)}
        for m in MODELOS:
            fontes[m] = om(m, lat, lon)
        for nome, s in fontes.items():
            dias = sorted(d for d in g if d in s)
            if len(dias) < 1500:
                continue
            x = np.array([g[d] for d in dias]); y = np.array([s[d] for d in dias]); anos = len(x) / 365.25
            mm = {}
            for d, a, b in zip(dias, x, y):
                v = mm.setdefault((d.year, d.month), [0.0, 0.0, 0]); v[0] += a; v[1] += b; v[2] += 1
            ch = [v for v in mm.values() if v[2] >= 28]
            wo, ws = x[x >= 1], y[y >= 1]
            linhas.append(dict(estacao=conc, independente={True: "sim", False: "nao", None: "?"}[indep], fonte=nome, dias=len(x),
                               pbias=round((y.sum() - x.sum()) / x.sum() * 100, 1), r=round(float(np.corrcoef(x, y)[0, 1]), 2),
                               kge_mensal=round(float(kge(np.array([v[0] for v in ch]), np.array([v[1] for v in ch]))), 2) if len(ch) >= 24 else "",
                               dias1mm_est=round((x >= 1).mean() * 100, 1), dias1mm_fonte=round((y >= 1).mean() * 100, 1),
                               p95_est=round(float(np.percentile(wo, 95)), 1), p95_fonte=round(float(np.percentile(ws, 95)), 1)))
    out = os.path.join(AQUI, "comparacao_fontes.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    print(out)
    for l in linhas:
        print("%-15s %-3s %-9s dias=%5d pbias=%6.1f r=%.2f kge=%s d1mm %.1f/%.1f p95 %.1f/%.1f" % (l["estacao"], l["independente"], l["fonte"], l["dias"], l["pbias"], l["r"], l["kge_mensal"], l["dias1mm_est"], l["dias1mm_fonte"], l["p95_est"], l["p95_fonte"]))


if __name__ == "__main__":
    main()
