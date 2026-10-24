# -*- coding: utf-8 -*-
"""Etapa 0 do plano da edição internacional: validar o ERA5 (Open-Meteo, CC BY 4.0) contra estações do GHCN-Daily (NOAA) pelo mundo.

1. Escolhe até uma estação por célula de 15 x 15 graus (espalhamento espacial), com PRCP em 1991-2020 segundo o inventário.
2. Baixa a série da estação (by_station) e a do ERA5 no mesmo ponto.
3. Calcula viés do total, correlação diária, KGE mensal, frequência de dias >= 1 mm e percentil 95; grava em validacao_global_era5.csv.
Tudo é guardado (dados_brutos/ghcnd_global e dados_brutos/openmeteo_global) e o script retoma de onde parou.
Uso: python global_era5_vs_ghcn.py [N_MAX]
"""
import csv, gzip, json, os, random, sys, time, urllib.error, urllib.request
import datetime as dt
import numpy as np

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402

AQUI = C.RESULTADOS          # saídas
GH = os.path.join(C.BRUTOS, "ghcnd")
GHG = os.path.join(C.BRUTOS, "ghcnd_global")
OMG = os.path.join(C.BRUTOS, "openmeteo_global")
INI, FIM = dt.date(1991, 1, 1), dt.date(2020, 12, 31)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
random.seed(42)


def estacoes():
    est = {}
    for l in open(os.path.join(GH, "ghcnd-stations.txt"), encoding="utf-8"):
        est[l[:11]] = (float(l[12:20]), float(l[21:30]), float(l[31:37]), l[41:71].strip())
    cand = {}
    for l in open(os.path.join(GH, "ghcnd-inventory.txt")):
        if l[31:35] == "PRCP":
            a, b = int(l[36:40]), int(l[41:45])
            if a <= 1992 and b >= 2019:                       # cobre quase todo 1991-2020
                i = l[:11]
                if i in est and abs(est[i][0]) <= 60:
                    cand[i] = est[i]
    # uma estação por célula de 15 x 15 graus, a aleatória com seed fixa
    cel = {}
    for i, (lat, lon, alt, nome) in sorted(cand.items()):
        cel.setdefault((int((lat + 90) // 15), int((lon + 180) // 15)), []).append(i)
    esc = [random.choice(v) for k, v in sorted(cel.items())]
    random.shuffle(esc)
    return [(i, *cand[i]) for i in esc[:NMAX]], len(cand), len(cel)


def baixar(url, dest, tentativas=6):
    for t in range(tentativas):
        try:
            return urllib.request.urlopen(url, timeout=180).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or t == tentativas - 1:
                raise
            time.sleep(75)
        except Exception:
            time.sleep(20)
    raise RuntimeError(url)


def serie_ghcn(i):
    arq = os.path.join(GHG, i + ".csv.gz")
    if not os.path.exists(arq):
        open(arq, "wb").write(baixar(f"https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/{i}.csv.gz", arq))
    d = {}
    for r in csv.reader(gzip.open(arq, "rt")):
        if r[2] == "PRCP" and r[5] == "":
            data = dt.date(int(r[1][:4]), int(r[1][4:6]), int(r[1][6:]))
            if INI <= data <= FIM:
                d[data] = int(r[3]) / 10
    return d


def serie_era5(i, lat, lon):
    arq = os.path.join(OMG, f"{i}.json")
    if not os.path.exists(arq):
        url = ("https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s&start_date=1991-01-01&end_date=2020-12-31"
               "&daily=precipitation_sum&timezone=UTC&models=era5" % (lat, lon))
        for t in range(10):
            try:
                dados = urllib.request.urlopen(url, timeout=180).read(); j = json.loads(dados); break
            except (urllib.error.HTTPError, json.JSONDecodeError) as e:
                if isinstance(e, urllib.error.HTTPError) and e.code != 429:
                    raise
                time.sleep(75)
        else:
            raise RuntimeError("limite da API")
        j["_acesso"] = dt.datetime.now(dt.timezone.utc).isoformat(); j["_url"] = url
        open(arq, "w", encoding="utf-8").write(json.dumps(j))
        time.sleep(2)
    j = json.load(open(arq, encoding="utf-8"))
    return {dt.date.fromisoformat(t): v for t, v in zip(j["daily"]["time"], j["daily"]["precipitation_sum"]) if v is not None}


def kge(o, s):
    r = np.corrcoef(o, s)[0, 1]; return 1 - np.sqrt((r - 1) ** 2 + (s.std() / o.std() - 1) ** 2 + (s.mean() / o.mean() - 1) ** 2)


def main():
    os.makedirs(GHG, exist_ok=True); os.makedirs(OMG, exist_ok=True)
    esc, ncand, ncel = estacoes()
    print(f"candidatas {ncand} em {ncel} células; escolhidas {len(esc)}", flush=True)
    saida = os.path.join(AQUI, "validacao_global_era5.csv"); linhas = []
    for n, (i, lat, lon, alt, nome) in enumerate(esc, 1):
        try:
            g = serie_ghcn(i)
            if len(g) < 1825:
                print(n, i, "poucos dias", len(g), flush=True); continue
            s = serie_era5(i, lat, lon)
        except Exception as e:
            print(n, i, "falhou:", e, flush=True); continue
        dias = sorted(d for d in g if d in s)
        if len(dias) < 1825:
            print(n, i, "poucos dias em comum", len(dias), flush=True); continue
        x = np.array([g[d] for d in dias]); y = np.array([s[d] for d in dias]); anos = len(x) / 365.25
        mm = {}
        for d, a, b in zip(dias, x, y):
            v = mm.setdefault((d.year, d.month), [0.0, 0.0, 0]); v[0] += a; v[1] += b; v[2] += 1
        ch = [v for v in mm.values() if v[2] >= 28]
        if x.sum() == 0 or x.std() == 0 or y.std() == 0:
            continue
        linhas.append(dict(id=i, nome=nome, pais=i[:2], lat=lat, lon=lon, alt=alt, dias=len(x), anos=round(anos, 1), mm_ano_est=round(x.sum() / anos),
                           mm_ano_era5=round(y.sum() / anos), pbias=round((y.sum() - x.sum()) / x.sum() * 100, 1), r=round(float(np.corrcoef(x, y)[0, 1]), 2),
                           kge_mensal=round(float(kge(np.array([v[0] for v in ch]), np.array([v[1] for v in ch]))), 2) if len(ch) >= 24 else "",
                           d1mm_est=round((x >= 1).mean() * 100, 1), d1mm_era5=round((y >= 1).mean() * 100, 1),
                           p95_est=round(float(np.percentile(x[x >= 1], 95)), 1) if (x >= 1).sum() > 20 else "", p95_era5=round(float(np.percentile(y[y >= 1], 95)), 1) if (y >= 1).sum() > 20 else ""))
        if n % 10 == 0:
            with open(saida, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
            print(n, "estações processadas;", len(linhas), "com resultado", flush=True)
    with open(saida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
    print("fim:", len(linhas), "estações ->", saida, flush=True)


if __name__ == "__main__":
    main()
