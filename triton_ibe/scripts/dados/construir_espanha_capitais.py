# -*- coding: utf-8 -*-
"""Chuva e nível de qualidade das 52 capitais de província da Espanha (Triton IBE), a partir da E-OBS e do Iberia01.

Cada capital é um ponto (coordenadas do Wikidata, CC0, conferidas pelo código INE): a série vem da célula E-OBS mais próxima
(uma só, por isso a geometria é B, como nos concelhos pequenos) e o nível usa a MESMA fórmula do programa
(triton/core/qualidade_chuva.py), comparando com a célula do Iberia01 mais próxima em 1971-2000.
Saídas: qualidade_espanha_capitais.csv e as unidades ES-<INE> no ibe_prototipo.db. Ceuta, Melilla, Las Palmas e Santa Cruz de Tenerife
ficam sem série (fora da grelha do Iberia01). Não é uma média municipal: falta o limite municipal (CNIG).
Uso: python construir_espanha_capitais.py
"""
import json, os, sqlite3, sys
import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402
sys.path.insert(0, C.REPO)          # a fórmula do programa: triton/core/qualidade_chuva.py
AQUI = C.RESULTADOS
from triton.core.qualidade_chuva import nivel, REFERENCIA          # noqa: E402

EOBS = C.EOBS_NC
IBER = C.IBERIA01_NC


def main():
    cap = json.load(open(os.path.join(C.AUTOMATICOS, "capitais_provincia_es.json"), encoding="utf-8"))["capitais"]
    ib = xr.open_dataset(IBER)["pr"].load()
    ds = xr.open_dataset(EOBS)
    box = dict(latitude=slice(35.0, 44.0), longitude=slice(-10.0, 5.0))
    eo = np.concatenate([ds.rr.sel(time=str(a), **box).values for a in range(1950, 2026)], axis=0)
    la = ds.rr.sel(time="1950-01-01", **box).latitude.values; lo = ds.rr.sel(time="1950-01-01", **box).longitude.values
    tempo = pd.date_range("1950-01-01", "2025-12-31")
    i71 = (tempo >= "1971-01-01") & (tempo <= "2000-12-31"); ib71 = pd.DatetimeIndex(ib.time.values) <= "2000-12-31"
    ano71 = tempo[i71].year.values
    ok_e = np.isfinite(eo).mean(axis=0) >= 0.99
    linhas = []
    for c in cap:
        lat, lon = c["lat"], c["lon"]
        d2 = np.where(ok_e, (la[:, None] - lat) ** 2 + (lo[None, :] - lon) ** 2, np.inf)
        a, b = np.unravel_index(int(d2.argmin()), d2.shape)
        dist_e = float(np.sqrt(d2[a, b]) * 111)
        a2, b2 = int(np.abs(ib.lat.values - lat).argmin()), int(np.abs(ib.lon.values - lon).argmin())
        sem = not np.isfinite(ib.values[0, a2, b2]) or dist_e > 25
        if sem:
            linhas.append(dict(ine=c["ine"], capital=c["nome_ine"], lat=lat, lon=lon, nivel="sem série", motivo="fora da grelha do Iberia01 ou da E-OBS"))
            continue
        se = eo[i71, a, b]; si = ib.values[ib71, a2, b2]
        dtot = (se.sum() / si.sum() - 1) * 100
        rxe = np.mean([se[ano71 == y].max() for y in range(1971, 2001)]); rxi = np.mean([si[ano71 == y].max() for y in range(1971, 2001)])
        drx = (rxe / rxi - 1) * 100
        n = nivel(dtot, drx, 1, "dentro", False)
        linhas.append(dict(ine=c["ine"], capital=c["nome_ine"], lat=lat, lon=lon, celula_eobs_lat=round(float(la[a]), 2), celula_eobs_lon=round(float(lo[b]), 2),
                           dist_celula_km=round(dist_e, 1), mm_ano_iberia01=int(round(si.sum() / 30)), mm_ano_eobs=int(round(se.sum() / 30)),
                           dtot=round(float(dtot), 1), drx=round(float(drx), 1), nivel=n, motivo="uma só célula (geometria B)" if n == "B" else "diferença para o Iberia01 acima dos limites de B"))
    d = pd.DataFrame(linhas)
    d.to_csv(os.path.join(AQUI, "qualidade_espanha_capitais.csv"), index=False, encoding="utf-8-sig")
    print(d.nivel.value_counts().to_dict(), "| referência:", REFERENCIA)
    print(d[["capital", "mm_ano_iberia01", "dtot", "drx", "nivel"]].sort_values("dtot").head(8).to_string(index=False))
    # acrescentar ao protótipo do banco
    db = sqlite3.connect(os.path.join(C.PROTOTIPO, "ibe_prototipo.db"))
    db.execute("delete from qualidade where unidade_id like 'ES-%'"); db.execute("delete from unidade_ponto where unidade_id like 'ES-%'"); db.execute("delete from unidade where id like 'ES-%'")
    for r in d.itertuples():
        db.execute("insert into unidade values (?,?,?,?,?,?,?,?,?)", ("ES-" + r.ine, r.capital, "ES", "ponto da capital", None, None, r.lat, r.lon, None))
        if r.nivel != "sem série":
            pid = db.execute("select id from ponto where lat between ? and ? and lon between ? and ?", (r.celula_eobs_lat - .01, r.celula_eobs_lat + .01, r.celula_eobs_lon - .01, r.celula_eobs_lon + .01)).fetchone()
            if pid:
                db.execute("insert into unidade_ponto values (?,?,?,?)", ("ES-" + r.ine, pid[0], 1.0, "dentro"))
            db.execute("insert into qualidade (unidade_id,n_celulas,metodo,iberia01_dtot_pct,iberia01_drx1_pct,nivel,aviso) values (?,?,?,?,?,?,?)", ("ES-" + r.ine, 1, "ponto", r.dtot, r.drx, r.nivel, r.motivo))
    db.commit(); db.close()


if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(
        description="Chuva e nível de qualidade (A/B/C) das 52 capitais de província da Espanha, a partir da E-OBS e do "
                    "Iberia01. Sem argumentos: lê os ficheiros netCDF indicados em _caminhos.py (fora do Git) e escreve "
                    "resultados/qualidade_espanha_capitais.csv."
    ).parse_args()
    try:
        main()
    except (FileNotFoundError, OSError) as erro:
        sys.exit(f"Falta uma fonte de dados ou não foi possível lê-la: {erro}\nVer scripts/dados/LEIA.md e _caminhos.py.")
