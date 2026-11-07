# -*- coding: utf-8 -*-
"""Duas verificações com a Open-Meteo (CC BY 4.0; uso não comercial em instituição pública):

A) Ilhas: ERA5 e CERRA contra as estações do GHCN-Daily da Madeira e dos Açores, 1991-2020.
B) Tendências: totais anuais 1950-2025 da E-OBS contra o ERA5 nos concelhos de tendência mais suspeita e em controlos.
Respostas guardadas em dados_brutos/openmeteo/. Resultados: comparacao_ilhas.csv e comparacao_tendencias.csv.
"""
import csv, json, os, sqlite3, time, urllib.error, urllib.request, zlib
import datetime as dt
import numpy as np
import pandas as pd
import comparar_fontes as cf

AQUI = cf.AQUI
ILHAS = [("PO000008522", "Funchal", 32.6300, -16.8997), ("POM00008521", "Funchal/S.Catarina", 32.683, -16.767),
         ("POM00008524", "Porto Santo", 33.073, -16.350), ("PO000008506", "Horta", 38.520, -28.630),
         ("POM00008501", "Flores", 39.455, -31.131), ("POM00008512", "Ponta Delgada", 37.741, -25.698),
         ("POM00008515", "Santa Maria", 36.971, -25.171), ("POW00013201", "Lajes (Terceira)", 38.730, -27.322)]


def om_longo(modelo, lat, lon, ini, fim, tag):
    arq = os.path.join(cf.OM, f"{modelo}_{lat:.3f}_{lon:.3f}_{tag}.json")
    if not os.path.exists(arq):
        url = ("https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s&start_date=%s&end_date=%s"
               "&daily=precipitation_sum&timezone=UTC&models=%s" % (lat, lon, ini, fim, modelo))
        for t in range(10):
            try:
                dados = urllib.request.urlopen(url, timeout=180).read()
                json.loads(dados); break
            except (urllib.error.HTTPError, json.JSONDecodeError) as e:
                if (isinstance(e, urllib.error.HTTPError) and e.code != 429) or t == 9:
                    raise
                time.sleep(75)
        time.sleep(3)
        j = json.loads(dados); j["_acesso"] = dt.datetime.now(dt.timezone.utc).isoformat(); j["_url"] = url
        open(arq, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False))
    j = json.load(open(arq, encoding="utf-8"))
    return {dt.date.fromisoformat(t): v for t, v in zip(j["daily"]["time"], j["daily"]["precipitation_sum"]) if v is not None}


def ilhas():
    linhas = []
    for sid, nome, lat, lon in ILHAS:
        g = {d: v for d, v in cf.ghcn(sid).items() if cf.INI <= d <= cf.FIM}
        for m in ("era5", "cerra"):
            try:
                s = om_longo(m, lat, lon, "1991-01-01", "2020-12-31", "1991-2020")
            except Exception as e:
                print("falhou", nome, m, e); continue
            dias = sorted(d for d in g if d in s)
            if len(dias) < 1500:
                print(nome, m, "sem dados em comum:", len(dias)); continue
            x = np.array([g[d] for d in dias]); y = np.array([s[d] for d in dias]); anos = len(x) / 365.25
            mm = {}
            for d, a, b in zip(dias, x, y):
                v = mm.setdefault((d.year, d.month), [0.0, 0.0, 0]); v[0] += a; v[1] += b; v[2] += 1
            ch = [v for v in mm.values() if v[2] >= 28]
            linhas.append(dict(estacao=nome, fonte=m, dias=len(x), mm_ano_est=round(x.sum() / anos), mm_ano_fonte=round(y.sum() / anos),
                               pbias=round((y.sum() - x.sum()) / x.sum() * 100, 1), r=round(float(np.corrcoef(x, y)[0, 1]), 2),
                               kge_mensal=round(float(cf.kge(np.array([v[0] for v in ch]), np.array([v[1] for v in ch]))), 2) if len(ch) >= 24 else "",
                               p95_est=round(float(np.percentile(x[x >= 1], 95)), 1), p95_fonte=round(float(np.percentile(y[y >= 1], 95)), 1)))
    pd.DataFrame(linhas).to_csv(os.path.join(AQUI, "comparacao_ilhas.csv"), index=False, encoding="utf-8-sig")
    print(pd.DataFrame(linhas).to_string(index=False))


def tendencias():
    conc = pd.read_csv(os.path.join(AQUI, "concelhos.csv"), dtype={"dtmn": str}).set_index("concelho")
    alvo = ["Vouzela", "Oliveira de Frades", "São Pedro do Sul", "Vale de Cambra", "Sever do Vouga", "Tondela",   # tendência mais negativa
            "Viseu", "Guarda", "Braga", "Aveiro", "Coimbra", "Lisboa"]                                          # controlos
    db = sqlite3.connect(f"file:{cf.DB}?mode=ro", uri=True)
    Y = np.arange(1950, 2026); linhas = []
    for c in alvo:
        lat, lon = float(conc.loc[c, "lat"]), float(conc.loc[c, "lon"])
        b = db.execute("select dados from series where concelho=?", (c,)).fetchone()[0]
        e = np.frombuffer(zlib.decompress(b), dtype=np.float32).astype(float)
        yr = np.array([(cf.D0 + dt.timedelta(days=i)).year for i in range(len(e))])
        ae = np.array([e[yr == y].sum() for y in Y])
        s = om_longo("era5", lat, lon, "1950-01-01", "2025-12-31", "1950-2025")
        ar = np.array([sum(v for d, v in s.items() if d.year == y) for y in Y])
        te, tr = np.polyfit(Y, ae, 1)[0] * 10, np.polyfit(Y, ar, 1)[0] * 10
        linhas.append(dict(concelho=c, tipo="tendência suspeita" if c in alvo[:6] else "controlo", mm_ano_eobs=round(ae.mean()), mm_ano_era5=round(ar.mean()),
                           tend_eobs_mm_dec=round(te, 1), tend_era5_mm_dec=round(tr, 1), r_anual=round(float(np.corrcoef(ae, ar)[0, 1]), 2),
                           eobs_1950_70=round(ae[:21].mean()), eobs_2005_25=round(ae[55:].mean()), era5_1950_70=round(ar[:21].mean()), era5_2005_25=round(ar[55:].mean())))
    pd.DataFrame(linhas).to_csv(os.path.join(AQUI, "comparacao_tendencias.csv"), index=False, encoding="utf-8-sig")
    print(pd.DataFrame(linhas).to_string(index=False))


if __name__ == "__main__":
    if not os.path.exists(os.path.join(AQUI, 'comparacao_ilhas.csv')):
        ilhas()
    tendencias()
