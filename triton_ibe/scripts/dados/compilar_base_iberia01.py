# -*- coding: utf-8 -*-
"""Compila a base de chuva da Edição Ibérica a partir do Iberia01 v1.0 (Península, Baleares): células + mapa município->células.

Fonte da chuva: Iberia01 v1.0, «Iberia010reg: daily gridded precipitation and temperature datasets for the Iberian
Peninsula» (Santander Meteorology Group, UC-CSIC), grade de 0,1°, 1971-01-01 a 2015-12-31, ODbL. Citação:
Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019). Iberia01: a new
gridded dataset of daily precipitation and temperatures over Iberia. Earth Syst. Sci. Data 11, 1947-1956,
doi:10.5194/essd-11-1947-2019. «Contains information from Iberia01, made available under the Open Database License».

Saídas (por defeito em ``<triton_ibe>/data``), todas sob ODbL, fora do programa:

- ``chuva_iberia01_p1.db`` ... ``p4.db``  uma linha por célula (série diária em inteiros de 0,1 mm, planos de bytes + zlib),
  cada parte com menos de 43 MiB (limite do GitHub: 50 MiB por ficheiro);
- ``iberia01_partes.json``  manifesto das partes (tamanho, SHA-256, células), como o ``climbra_partes.json``;
- ``ibe_unidades.db``  municípios (INE e DTMN), células, pesos, nível de qualidade A/B/C e metadados.

Método. A série de um município é a média, ponderada, das células com centro dentro do limite; sem nenhum centro dentro,
a célula válida mais próxima do ponto representativo do município (até 0,25°), registada em ``metodo``. Quantização:
0,1 mm (viés medido de -0,06% no total anual). Ceuta e Melilla ficam fora da grade; Canárias, Madeira e Açores são tratados
por ``compilar_ilhas_era5.py``.

    python scripts/dados/compilar_base_iberia01.py [--iberia01 F.nc] [--caop-dir D] [--lau F.geojson] [--saida-dir D]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import zlib
from datetime import datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _caminhos as C  # noqa: E402
import unidades_iberia as U  # noqa: E402

N_PARTES = 4
LIMITE_PARTE_MIB = 43
PASSO = 10  # 0,1 mm
DIST_MAX_GRAUS = 0.25
CITACAO = ("Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019). "
           "Iberia01: a new gridded dataset of daily precipitation and temperatures over Iberia. Earth System Science "
           "Data, 11, 1947-1956. doi:10.5194/essd-11-1947-2019")
AVISO_ODBL = "Contains information from Iberia01, made available under the Open Database License (ODbL 1.0)."


def codificar(serie: np.ndarray) -> bytes:
    q = np.round(np.nan_to_num(serie, nan=6553.5) * PASSO).astype(np.uint16)
    return zlib.compress(q.view(np.uint8).reshape(-1, 2).T.tobytes(), 9)


def main(args):
    import geopandas as gpd
    import netCDF4
    from shapely.geometry import Point

    nc = Path(args.iberia01)
    saida = Path(args.saida_dir)
    saida.mkdir(parents=True, exist_ok=True)
    d = netCDF4.Dataset(nc)
    lat, lon = np.asarray(d["lat"][:]), np.asarray(d["lon"][:])
    t = d["time"]
    inicio = netCDF4.num2date(t[0], t.units).strftime("%Y-%m-%d")
    fim = netCDF4.num2date(t[-1], t.units).strftime("%Y-%m-%d")
    dias = len(t)
    pr = np.ma.filled(d["pr"][:, :, :].astype(np.float32), np.nan)
    validas = np.argwhere(np.isfinite(pr[0]))
    print(f"Iberia01: {dias} dias ({inicio} a {fim}), {len(validas)} células válidas")

    # Células, ordenadas por longitude e depois latitude; partes balanceadas por contagem.
    ordem = sorted(range(len(validas)), key=lambda k: (validas[k][1], validas[k][0]))
    bloco = -(-len(ordem) // N_PARTES)
    parte_de = {}
    for k, idx in enumerate(ordem):
        parte_de[idx] = f"p{k // bloco + 1}"
    celulas = []
    for idx, (i, j) in enumerate(validas):
        celulas.append((int(i) * 1000 + int(j), round(float(lat[i]), 4), round(float(lon[j]), 4), parte_de[idx], i, j))
    celulas.sort()

    # Partes de chuva.
    manifesto = {"fonte": "Iberia01 v1.0", "licenca": "ODbL 1.0", "citacao": CITACAO, "aviso": AVISO_ODBL,
                 "limite_github_mb": 50, "limite_parte_mib": LIMITE_PARTE_MIB, "passo_mm": 1 / PASSO,
                 "inicio": inicio, "fim": fim, "dias": dias, "partes": []}
    h_pacote = hashlib.sha256()
    for p in sorted({c[3] for c in celulas}):
        arq = saida / f"chuva_iberia01_{p}.db"
        arq.unlink(missing_ok=True)
        con = sqlite3.connect(arq)
        con.execute("CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, inicio TEXT, dias INTEGER, "
                    "passo_mm REAL, dados BLOB)")
        con.execute("CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT)")
        mem = [c for c in celulas if c[3] == p]
        for cid, la, lo, _, i, j in mem:
            blob = codificar(pr[:, i, j])
            h_pacote.update(cid.to_bytes(8, "little") + hashlib.sha256(blob).digest())
            con.execute("INSERT INTO celula VALUES (?,?,?,?,?,?,?)", (cid, la, lo, inicio, dias, 1 / PASSO, blob))
        con.executemany("INSERT INTO metadados VALUES (?,?)", [
            ("fonte", "Iberia01 v1.0"), ("licenca", "ODbL 1.0"), ("citacao", CITACAO), ("aviso", AVISO_ODBL),
            ("parte", p), ("periodo", f"{inicio} a {fim}")])
        con.commit()
        con.execute("VACUUM")
        con.close()
        mib = arq.stat().st_size / 2 ** 20
        if mib >= LIMITE_PARTE_MIB:
            sys.exit(f"{arq.name}: {mib:.1f} MiB passa de {LIMITE_PARTE_MIB} MiB")
        manifesto["partes"].append({"arquivo": arq.name, "tamanho_bytes": arq.stat().st_size, "sha256": U.sha256(arq),
                                    "celulas": len(mem),
                                    "lon_min": min(c[2] for c in mem), "lon_max": max(c[2] for c in mem)})
        print(f"{arq.name}: {len(mem)} células, {mib:.1f} MiB")
    sha_pacote = h_pacote.hexdigest()
    manifesto["sha256_pacote"] = sha_pacote
    manifesto["pacote_id"] = f"iberia01-v1.0-{sha_pacote[:12]}"
    (saida / "iberia01_partes.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Unidades e mapa unidade -> células.
    un = U.carregar_unidades(Path(args.caop_dir), Path(args.lau))
    print(f"{len(un)} unidades ({(un.pais == 'PT').sum()} PT, {(un.pais == 'ES').sum()} ES)")
    pts = gpd.GeoDataFrame({"celula": [c[0] for c in celulas]},
                           geometry=[Point(c[2], c[1]) for c in celulas], crs=4326)
    sj = gpd.sjoin(pts, un[["codigo", "geometry"]], how="inner", predicate="within")
    dentro = {}
    for cod, cel in zip(sj["codigo"], sj["celula"]):
        dentro.setdefault(cod, []).append(int(cel))
    cel_xy = np.array([[c[2], c[1]] for c in celulas])
    cel_id = np.array([c[0] for c in celulas])
    arq_u = saida / "ibe_unidades.db"
    arq_u.unlink(missing_ok=True)
    con = sqlite3.connect(arq_u)
    con.executescript(U.ESQUEMA_UNIDADES)
    con.executemany("INSERT INTO celula VALUES (?,?,?,?,?)",
                    [(c[0], c[1], c[2], "iberia01", c[3]) for c in celulas])
    cont = {"iberia01": 0, "era5": 0, "nenhuma": 0}
    for _, u in un.iterrows():
        fonte_lim = "CAOP 2025 (DGT)" if u.pais == "PT" else "Eurostat/GISCO LAU 2023"
        pop = None if u.populacao is None or u.populacao != u.populacao else int(u.populacao)
        if u.regiao in U.REGIOES_SEM_COBERTURA:
            con.execute("INSERT INTO unidade VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (u.codigo, u.pais, u.regiao, u.provincia, u.nome, pop, fonte_lim, "nenhuma", "", 0, None,
                         "", U.REGIOES_SEM_COBERTURA[u.regiao]))
            cont["nenhuma"] += 1
            continue
        if u.regiao in U.REGIOES_ERA5:
            con.execute("INSERT INTO unidade VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (u.codigo, u.pais, u.regiao, u.provincia, u.nome, pop, fonte_lim, "era5", "", 0, None,
                         "C", U.MOTIVO_ILHAS))
            cont["era5"] += 1
            continue
        c = u.geometry.representative_point()
        contido = False
        if u.codigo in dentro:
            ids = sorted(dentro[u.codigo])
            metodo = f"média de {len(ids)} célula(s) com centro dentro do limite"
            dist = 0.0
            n_in = len(ids)
        else:
            dd = np.hypot((cel_xy[:, 0] - c.x) * np.cos(np.radians(c.y)), cel_xy[:, 1] - c.y)
            k = int(np.argmin(dd))
            if dd[k] > DIST_MAX_GRAUS:
                con.execute("INSERT INTO unidade VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (u.codigo, u.pais, u.regiao, u.provincia, u.nome, pop, fonte_lim, "nenhuma", "", 0, None, "",
                             "sem célula do Iberia01 a menos de 0,25° do município"))
                cont["nenhuma"] += 1
                continue
            ids = [int(cel_id[k])]
            contido = abs(cel_xy[k, 0] - c.x) <= 0.05 + 1e-9 and abs(cel_xy[k, 1] - c.y) <= 0.05 + 1e-9
            dist = float(dd[k] * 111.0)
            n_in = 0
            metodo = f"célula válida mais próxima do ponto representativo ({dist:.0f} km)"
        nivel, motivo = U.nivel_por_geometria(n_in, dist, contido)
        con.execute("INSERT INTO unidade VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (u.codigo, u.pais, u.regiao, u.provincia, u.nome, pop, fonte_lim, "iberia01", metodo, n_in,
                     round(dist, 1), nivel, motivo))
        con.executemany("INSERT INTO unidade_celula VALUES (?,?,?)", [(u.codigo, i, 1.0 / len(ids)) for i in ids])
        cont["iberia01"] += 1
    meta = {
        "fonte": "Iberia01 v1.0", "licenca": "ODbL 1.0", "citacao": CITACAO, "aviso": AVISO_ODBL,
        "periodo": f"{inicio} a {fim}", "dias": str(dias), "pacote_id": manifesto["pacote_id"],
        "sha256_pacote": sha_pacote, "sha256_iberia01": U.sha256(nc),
        "sha256_lau": U.sha256(args.lau),
        "limites_pt": "CAOP 2025, Direção-Geral do Território (Aviso n.º 3502/2026/2)",
        "limites_es": "Eurostat/GISCO, Local Administrative Units 2023 (LAU_RG_01M_2023_4326), códigos INE",
        "metodo": "média das células com centro dentro do limite; sem nenhuma, a mais próxima até 0,25°",
        "quantizacao_mm": str(1 / PASSO),
        "unidades_iberia01": str(cont["iberia01"]), "unidades_era5": str(cont["era5"]),
        "unidades_sem_cobertura": str(cont["nenhuma"]),
        "espanha_locais": str(int((un.pais == "ES").sum())),
        "construido_com": "scripts/dados/compilar_base_iberia01.py",
    }
    con.executemany("INSERT INTO metadados VALUES (?,?)", meta.items())
    con.commit()
    con.execute("VACUUM")
    con.close()
    print(cont, f"{arq_u.name}: {arq_u.stat().st_size / 2 ** 20:.2f} MiB")
    print("pacote_id", manifesto["pacote_id"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--iberia01", default=C.IBERIA01_NC)
    ap.add_argument("--caop-dir", default=C.CAOP_DIR)
    ap.add_argument("--lau", default=str(Path(C.FONTES) / "gisco" / "LAU_RG_01M_2023_4326.geojson"))
    ap.add_argument("--saida-dir", default=str(Path(C.REPO) / "data"))
    main(ap.parse_args())
