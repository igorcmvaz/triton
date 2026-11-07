# -*- coding: utf-8 -*-
"""Compila a chuva das ilhas fora do Iberia01 (Canárias, Madeira, Açores) a partir da reanálise ERA5, nível C fixo.

Fonte: ERA5 (Copernicus Climate Change Service / ECMWF; Hersbach et al. 2020, doi:10.1002/qj.3803), grade de 0,25°,
precipitação diária (soma de 00 a 24 UTC), obtida da API de arquivo da Open-Meteo (dados CC BY 4.0; a API é gratuita
para uso não comercial, e este script é executado pelo mantenedor, não pelo programa instalado). O pedido original
previa a ERA5-Land (0,1°); a Open-Meteo devolve precipitação nula para a ERA5-Land (testado em 30/10/2026) e o
Climate Data Store exige conta e chave, por isso usa-se a ERA5 de 0,25°, também CC BY. Nada é inventado: o nó da
grade mais próximo do ponto representativo do município é a série do município, sempre com nível C.

Período igual ao do Iberia01 (1971-01-01 a 2015-12-31) para que as duas fontes tenham os mesmos recortes.

Saídas: ``data/chuva_ilhas_era5.db`` (mesmo esquema das partes do Iberia01), linhas ``unidade_celula`` e ``celula`` em
``data/ibe_unidades.db`` (o script ``compilar_base_iberia01.py`` deve ter corrido antes) e as respostas brutas em
``<dados_brutos>/open_meteo_era5/`` (fora do Git).

    python scripts/dados/compilar_ilhas_era5.py [--caop-dir D] [--lau F] [--saida-dir D]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _caminhos as C  # noqa: E402
import unidades_iberia as U  # noqa: E402
from compilar_base_iberia01 import AVISO_ODBL, codificar  # noqa: E402

INICIO, FIM = "1971-01-01", "2015-12-31"
DIAS = 16436
GRADE = 0.25
LOTE = 4
URL = ("https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=" + INICIO +
       "&end_date=" + FIM + "&daily=precipitation_sum&timezone=UTC&models=era5")
CITACAO_ERA5 = ("Hersbach, H. et al. (2020). The ERA5 global reanalysis. Q. J. R. Meteorol. Soc., 146, 1999-2049. "
                "doi:10.1002/qj.3803. Contains modified Copernicus Climate Change Service information; dados via "
                "Open-Meteo.com (CC BY 4.0).")


def id_do_no(lat: float, lon: float) -> int:
    return 1_000_000_000 + (round(lat * 100) + 9000) * 100_000 + (round(lon * 100) + 18000)


def obter(nos, cache: Path):
    """Séries diárias (mm) de cada nó (lat, lon); respostas guardadas em cache, para reproduzir sem a rede."""
    cache.mkdir(parents=True, exist_ok=True)
    faltam = [n for n in nos if not (cache / f"{id_do_no(*n)}.json").exists()]
    for i in range(0, len(faltam), LOTE):
        lote = faltam[i:i + LOTE]
        url = URL.format(lat=",".join(f"{a:.2f}" for a, _ in lote), lon=",".join(f"{o:.2f}" for _, o in lote))
        for tentativa in range(8):
            try:
                with urllib.request.urlopen(url, timeout=180) as r:
                    dados = json.load(r)
                break
            except Exception as erro:  # 429 e falhas de rede: espera e repete
                print("  nova tentativa:", erro)
                time.sleep(30 * (tentativa + 1))
        else:
            sys.exit("Open-Meteo indisponível; reexecute (o cache aproveita o que já veio).")
        if isinstance(dados, dict):
            dados = [dados]
        for no, resp in zip(lote, dados):
            v = resp["daily"]["precipitation_sum"]
            if len(v) != DIAS or any(x is None for x in v):
                sys.exit(f"nó {no}: série incompleta ({len(v)} dias, {sum(x is None for x in v)} nulos)")
            (cache / f"{id_do_no(*no)}.json").write_text(json.dumps({"lat": no[0], "lon": no[1], "pr": v}), encoding="utf-8")
        print(f"  {min(i + LOTE, len(faltam))}/{len(faltam)} nós")
        time.sleep(2)
    return {n: np.array(json.loads((cache / f"{id_do_no(*n)}.json").read_text(encoding="utf-8"))["pr"], dtype=np.float32)
            for n in nos}


def main(a):
    un = U.carregar_unidades(Path(a.caop_dir), Path(a.lau))
    un = un[un.regiao.isin(U.REGIOES_ERA5)]
    nos_de = {}
    for _, u in un.iterrows():
        c = u.geometry.representative_point()
        nos_de[u.codigo] = (round(round(c.y / GRADE) * GRADE, 2), round(round(c.x / GRADE) * GRADE, 2))
    nos = sorted(set(nos_de.values()))
    print(f"{len(un)} unidades de ilha, {len(nos)} nós ERA5 de {GRADE}°")
    series = obter(nos, Path(C.BRUTOS) / "open_meteo_era5")
    saida = Path(a.saida_dir)
    arq = saida / "chuva_ilhas_era5.db"
    arq.unlink(missing_ok=True)
    con = sqlite3.connect(arq)
    con.execute("CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, inicio TEXT, dias INTEGER, "
                "passo_mm REAL, dados BLOB)")
    con.execute("CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT)")
    for n in nos:
        con.execute("INSERT INTO celula VALUES (?,?,?,?,?,?,?)",
                    (id_do_no(*n), n[0], n[1], INICIO, DIAS, 0.1, codificar(series[n])))
    con.executemany("INSERT INTO metadados VALUES (?,?)", [
        ("fonte", "ERA5 (0,25°) via Open-Meteo archive API"), ("licenca", "CC BY 4.0 (Copernicus / Open-Meteo)"),
        ("citacao", CITACAO_ERA5), ("periodo", f"{INICIO} a {FIM}"), ("nivel", "C")])
    con.commit()
    con.execute("VACUUM")
    con.close()
    u_db = sqlite3.connect(saida / "ibe_unidades.db")
    u_db.execute("DELETE FROM celula WHERE fonte = 'era5'")
    u_db.execute("DELETE FROM unidade_celula WHERE celula >= 1000000000")
    for n in nos:
        u_db.execute("INSERT INTO celula VALUES (?,?,?,?,?)", (id_do_no(*n), n[0], n[1], "era5", "ilhas_era5"))
    for cod, n in nos_de.items():
        u_db.execute("INSERT INTO unidade_celula VALUES (?,?,?)", (cod, id_do_no(*n), 1.0))
        u_db.execute("UPDATE unidade SET metodo = ?, nivel = 'C', motivo = ?, dist_celula_km = NULL WHERE codigo = ?",
                     (f"nó ERA5 de 0,25° mais próximo do ponto representativo ({n[0]:.2f}, {n[1]:.2f})",
                      U.MOTIVO_ILHAS, cod))
    u_db.executemany("INSERT OR REPLACE INTO metadados VALUES (?,?)", [
        ("ilhas_fonte", "ERA5 0,25° via Open-Meteo archive API, CC BY 4.0"), ("ilhas_citacao", CITACAO_ERA5),
        ("ilhas_sha256", U.sha256(arq)), ("ilhas_nos", str(len(nos))),
        ("unidades_era5", str(len(nos_de)))])
    u_db.commit()
    u_db.execute("VACUUM")
    u_db.close()
    print(f"{arq.name}: {arq.stat().st_size / 2 ** 20:.2f} MiB, {len(nos)} nós")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--caop-dir", default=C.CAOP_DIR)
    ap.add_argument("--lau", default=str(Path(C.FONTES) / "gisco" / "LAU_RG_01M_2023_4326.geojson"))
    ap.add_argument("--saida-dir", default=str(Path(C.REPO) / "data"))
    main(ap.parse_args())
