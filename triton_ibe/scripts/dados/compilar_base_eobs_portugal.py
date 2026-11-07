# -*- coding: utf-8 -*-
"""Compila a base de precipitação diária por concelho da Edição Ibérica (dados de Portugal) (IBE).

Fontes (por defeito em data/portugal/fontes, fora do Git; ver scripts/dados/LEIA.md e _caminhos.py):

- E-OBS v33.0e, precipitação diária (RR), média do conjunto, grade regular de 0,1°,
  1950-01-01 a 2025-12-31 (Copernicus Climate Change Service / KNMI). Citação exigida:
  Cornes et al. (2018), JGR Atmospheres 123, doi:10.1029/2017JD028200, e o reconhecimento
  ao projeto UERRA, ao C3S e aos fornecedores de dados do ECA&D.
- CAOP2025 (Direção-Geral do Território), limites oficiais dos 308 municípios.

Método. A série de cada concelho é a média diária das células da grade cujo centro cai
dentro do limite do município; concelho pequeno, sem centro de célula dentro, recebe a
célula mais próxima do seu centroide (registrado em ``metodo``). Dia em que todas as
células do concelho estão sem dado fica sem dado (NaN), e o programa o trata como falha,
não como dia seco. Concelho fora do domínio da E-OBS (Açores, a oeste de 25° W) fica
registrado como não coberto, e nunca recebe a série de um vizinho. Também fica não coberto
o concelho com mais de 1% de dias sem dado na normal 1991–2020: é o caso de toda a Madeira,
onde a E-OBS só tem a célula das estações que funcionavam em cada ano (o Funchal falta em
22% dos dias de 1991–2020), e a simulação recusa série com falha.

Saída: data/portugal_eobs.db (SQLite), uma linha por concelho com a série float32
comprimida (zlib), e a tabela ``metadados`` com versão, período, método e as impressões
SHA-256 das fontes.

    python scripts/dados/compilar_base_eobs_portugal.py [--saida banco.db]
    python scripts/dados/compilar_base_eobs_portugal.py --so-completude [--saida banco.db]   # só o critério, na base pronta
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import zlib
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _caminhos as C  # noqa: E402

FONTES = Path(C.FONTES)
EOBS = Path(C.EOBS_NC)
CAOP = Path(C.CAOP_DIR)
#: Saída: por defeito o banco do repositório; ``--saida <ficheiro>`` escreve noutro lado (para reproduzir sem o substituir).
SAIDA = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else Path(C.BASE)

#: Camadas de municípios da CAOP2025, com o nome da região para a tela.
CAMADAS = (
    ("Continente_CAOP2025.gpkg", "cont_municipios", "Continente"),
    ("ArqMadeira_CAOP2025.gpkg", "ram_municipios", "Região Autónoma da Madeira"),
    ("ArqAcores_GCentral_GOriental_CAOP2025.gpkg", "raa_cen_ori_municipios", "Região Autónoma dos Açores"),
    ("ArqAcores_GOcidental_CAOP2025.gpkg", "raa_oci_municipios", "Região Autónoma dos Açores"),
)
VERSAO_EOBS = "33.0e"
#: Critério de completude: fração máxima de dias sem dado na normal de referência.
NORMAL_DE_REFERENCIA = ("1991-01-01", "2020-12-31")
FALHAS_MAXIMAS = 0.01


def impressao(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def municipios():
    """Os 308 municípios em WGS84, com código, nome, distrito/ilha e região."""
    import geopandas as gpd
    import pandas as pd
    partes = []
    for arquivo, camada, regiao in CAMADAS:
        g = gpd.read_file(CAOP / arquivo, layer=camada)[["dtmn", "municipio", "distrito_ilha", "geometry"]]
        g = g.to_crs(4326)
        g["regiao"] = regiao
        partes.append(g)
    return gpd.GeoDataFrame(pd.concat(partes, ignore_index=True), crs=4326)


def main():
    import xarray as xr
    from shapely import contains_xy

    if not EOBS.exists():
        sys.exit(f"Falta {EOBS}: baixe a E-OBS (ver o docstring e scripts/dados/LEIA.md).")
    mun = municipios()
    print(f"{len(mun)} municípios na CAOP2025")

    ds = xr.open_dataset(EOBS)
    rr = ds["rr"]
    lat, lon = ds["latitude"].values, ds["longitude"].values
    tempos = ds["time"].values
    inicio = str(np.datetime_as_string(tempos[0], unit="D"))
    fim = str(np.datetime_as_string(tempos[-1], unit="D"))
    print(f"E-OBS: {len(tempos)} dias, {inicio} a {fim}; lat {lat.min()}..{lat.max()}, lon {lon.min()}..{lon.max()}")

    # Recorte das duas áreas cobertas (Continente e Madeira), para não ler a Europa inteira.
    caixas = {"Continente": (36.8, 42.3, -9.7, -6.1), "Região Autónoma da Madeira": (32.3, 33.2, -17.4, -16.2)}
    registros = []
    for regiao, (la0, la1, lo0, lo1) in caixas.items():
        sub = rr.sel(latitude=slice(la0, la1), longitude=slice(lo0, lo1)).load().values  # (tempo, lat, lon)
        sla = lat[(lat >= la0) & (lat <= la1)]
        slo = lon[(lon >= lo0) & (lon <= lo1)]
        LO, LA = np.meshgrid(slo, sla)
        com_dado = np.isfinite(sub).any(axis=0)
        print(f"{regiao}: grade {sub.shape}, {int(com_dado.sum())} células com dado")
        for _, m in mun[mun["regiao"] == regiao].iterrows():
            dentro = contains_xy(m.geometry, LO, LA) & com_dado
            if dentro.any():
                serie = np.nanmean(sub[:, dentro], axis=1)
                metodo = f"média de {int(dentro.sum())} células com centro dentro do limite"
            else:
                c = m.geometry.representative_point()
                d = (LA - c.y) ** 2 + (LO - c.x) ** 2
                d[~com_dado] = np.inf
                i, j = np.unravel_index(np.argmin(d), d.shape)
                serie = sub[:, i, j]
                metodo = f"célula mais próxima do centroide ({sla[i]:.2f}, {slo[j]:.2f})"
            # Todas as células sem dado no dia: falha, e não dia seco.
            registros.append((m.dtmn, m.municipio, m.distrito_ilha, regiao, metodo, serie.astype(np.float32)))

    cobertos = {r[0] for r in registros}
    nao_cobertos = mun[~mun["dtmn"].isin(cobertos)]
    SAIDA.unlink(missing_ok=True)
    con = sqlite3.connect(SAIDA)
    con.execute("CREATE TABLE series (dtmn TEXT PRIMARY KEY, concelho TEXT, distrito TEXT, regiao TEXT, "
                "metodo TEXT, inicio TEXT, dias INTEGER, falhas INTEGER, media_anual_mm REAL, dados BLOB)")
    con.execute("CREATE TABLE nao_cobertos (dtmn TEXT PRIMARY KEY, concelho TEXT, distrito TEXT, regiao TEXT, motivo TEXT)")
    con.execute("CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT)")
    anos = (date.fromisoformat(fim) - date.fromisoformat(inicio)).days / 365.25
    for dtmn, nome, distrito, regiao, metodo, serie in registros:
        falhas = int(np.isnan(serie).sum())
        con.execute("INSERT INTO series VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (dtmn, nome, distrito, regiao, metodo, inicio, len(serie), falhas,
                     float(np.nansum(serie) / anos), zlib.compress(serie.tobytes(), 9)))
    for _, m in nao_cobertos.iterrows():
        con.execute("INSERT INTO nao_cobertos VALUES (?,?,?,?,?)",
                    (m.dtmn, m.municipio, m.distrito_ilha, m.regiao,
                     "fora do domínio da E-OBS (a oeste de 25° W)"))
    meta = {
        "fonte": f"E-OBS v{VERSAO_EOBS}, precipitação diária (RR), média do conjunto, grade de 0,1°",
        "periodo": f"{inicio} a {fim}",
        # Conferido no Crossref em 07/10/2026.
        "citacao": "Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D. (2018). An Ensemble "
                   "Version of the E-OBS Temperature and Precipitation Data Sets. Journal of Geophysical Research: "
                   "Atmospheres, 123(17), 9391-9409. doi:10.1029/2017JD028200",
        "reconhecimento": "We acknowledge the E-OBS dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and "
                          "the Copernicus Climate Change Service, and the data providers in the ECA&D project "
                          "(https://www.ecad.eu)",
        "limites": "CAOP2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR 2.ª série n.º 34, 18/02/2026)",
        "metodo": "média diária das células com centro dentro do limite do concelho; sem centro dentro, a célula "
                  "mais próxima do centroide; dia sem dado em todas as células = falha (NaN)",
        "sha256_eobs": impressao(EOBS),
        "sha256_caop": json.dumps({a: impressao(CAOP / a) for a, _, _ in CAMADAS}),
        "concelhos_cobertos": str(len(registros)),
        "concelhos_nao_cobertos": str(len(nao_cobertos)),
    }
    con.executemany("INSERT INTO metadados VALUES (?,?)", meta.items())
    con.commit()
    con.close()
    print(f"{SAIDA}: {len(registros)} concelhos com série, {len(nao_cobertos)} fora do domínio; "
          f"{SAIDA.stat().st_size / 1e6:.1f} MB")


def aplicar_completude(caminho: Path = None) -> list:
    """Passa para ``nao_cobertos`` o concelho com falhas demais na normal de referência."""
    from datetime import datetime
    caminho = caminho or SAIDA
    a, b = (datetime.fromisoformat(x) for x in NORMAL_DE_REFERENCIA)
    con = sqlite3.connect(caminho)
    retirados = []
    for dtmn, nome, distrito, regiao, ini, blob in con.execute(
            "SELECT dtmn, concelho, distrito, regiao, inicio, dados FROM series WHERE falhas > 0").fetchall():
        serie = np.frombuffer(zlib.decompress(blob), dtype=np.float32)
        i0 = (a - datetime.fromisoformat(ini)).days
        i1 = (b - datetime.fromisoformat(ini)).days + 1
        fracao = float(np.isnan(serie[i0:i1]).mean())
        if fracao > FALHAS_MAXIMAS:
            motivo = (f"cobertura insuficiente da E-OBS: {100 * fracao:.0f}% dos dias sem dado em "
                      f"{a.year}–{b.year} (limite {100 * FALHAS_MAXIMAS:.0f}%)")
            con.execute("DELETE FROM series WHERE dtmn = ?", (dtmn,))
            con.execute("INSERT OR REPLACE INTO nao_cobertos VALUES (?,?,?,?,?)", (dtmn, nome, distrito, regiao, motivo))
            retirados.append((nome, motivo))
    n_series = con.execute("SELECT count(*) FROM series").fetchone()[0]
    n_fora = con.execute("SELECT count(*) FROM nao_cobertos").fetchone()[0]
    con.executemany("INSERT OR REPLACE INTO metadados VALUES (?,?)", [
        ("concelhos_cobertos", str(n_series)), ("concelhos_nao_cobertos", str(n_fora)),
        ("completude", f"concelho com mais de {100 * FALHAS_MAXIMAS:.0f}% de dias sem dado em "
                       f"{a.year}–{b.year} fica não coberto")])
    con.commit()
    con.execute("VACUUM")
    con.close()
    return retirados


if __name__ == "__main__":
    import argparse
    _ap = argparse.ArgumentParser(
        description="Compila data/portugal_eobs.db (precipitação diária por concelho, E-OBS v33.0e e CAOP2025). "
                    "Os ficheiros de origem (cerca de 3 GB) ficam fora do Git; ver scripts/dados/LEIA.md e _caminhos.py.")
    _ap.add_argument("--saida", metavar="BANCO.db", help="escreve noutro ficheiro, sem substituir o banco do repositório")
    _ap.add_argument("--so-completude", action="store_true",
                     help="só aplica o critério de completude (1 %% de dias sem dado em 1991-2020) na base pronta")
    _ap.parse_args()
    if "--so-completude" not in sys.argv:
        main()
    for nome, motivo in aplicar_completude():
        print(f"não coberto: {nome} — {motivo}")
