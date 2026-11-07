# -*- coding: utf-8 -*-
"""Protótipo do banco de chuva da Península Ibérica (Triton IBE): ver ESTRUTURA_DE_DADOS_IBE.md.

Gera, nesta pasta:
  ibe_prototipo.db  células E-OBS (toda a Península), unidades (concelhos de Portugal), pesos, qualidade, procedência
  ibe_correcao.db   correção de escala opcional derivada do Iberia01 (ODbL), em ficheiro separado
  relatorio_prototipo.md  verificações (reconstrução contra o portugal_eobs.db atual, tamanhos, níveis de qualidade)
Nenhum código do programa é alterado. Uso: python construir_banco_ibe.py
"""
import datetime as dt
import json
import os
import re
import sqlite3
import zlib

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from shapely import contains_xy

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _caminhos as C  # noqa: E402

AQUI = C.PROTOTIPO           # saídas: ibe_prototipo.db e ibe_correcao.db (fora do Git)
FONTES = C.FONTES
EOBS = C.EOBS_NC
CAOP = C.CAOP_CONTINENTE
IBERIA01 = C.IBERIA01_NC
BASE_ATUAL = C.BASE
BOX = dict(latitude=slice(36.0, 43.9), longitude=slice(-9.6, 4.4))
SEM_DADO = 65535

ESQUEMA = """
CREATE TABLE fonte (id TEXT PRIMARY KEY, tipo TEXT, nome TEXT, versao TEXT, resolucao_graus REAL, inicio TEXT, fim TEXT, convencao_dia TEXT,
  licenca TEXT, citacao TEXT, url TEXT, obtido_em TEXT, sha256 TEXT, redistribuivel TEXT);
CREATE TABLE ponto (id INTEGER PRIMARY KEY, fonte_id TEXT REFERENCES fonte(id), tipo TEXT, lat REAL, lon REAL, altitude_m REAL, codigo_externo TEXT, nome TEXT, pais TEXT);
CREATE TABLE serie_bloco (ponto_id INTEGER REFERENCES ponto(id), ano_ini INTEGER, dias INTEGER, dados BLOB, marcas BLOB, PRIMARY KEY (ponto_id, ano_ini));
CREATE TABLE unidade (id TEXT PRIMARY KEY, nome TEXT, pais TEXT, nivel TEXT, distrito_ou_provincia TEXT, regiao TEXT, lat_ref REAL, lon_ref REAL, area_km2 REAL);
CREATE TABLE unidade_ponto (unidade_id TEXT REFERENCES unidade(id), ponto_id INTEGER REFERENCES ponto(id), peso REAL, metodo TEXT);
CREATE TABLE qualidade (unidade_id TEXT PRIMARY KEY REFERENCES unidade(id), n_celulas INTEGER, metodo TEXT, serie_repetida_com TEXT,
  estacao_nome TEXT, dist_estacao_km REAL, estacao_independente TEXT, pbias_estacao_pct REAL, r_estacao REAL,
  iberia01_dtot_pct REAL, iberia01_r_diario REAL, iberia01_ddias1mm_pp REAL, iberia01_dp95_pct REAL, iberia01_drx1_pct REAL, nivel TEXT, aviso TEXT);
CREATE TABLE nao_coberto (unidade_id TEXT, nome TEXT, motivo TEXT);
CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);
"""


def codificar(v):
    """uint16 em 0,1 mm, 65535 = sem dado; planos de byte + zlib."""
    q = np.where(np.isfinite(v), np.clip(np.round(v * 10), 0, 65534), SEM_DADO).astype(np.uint16)
    return zlib.compress(q.view(np.uint8).reshape(-1, 2).T.tobytes(), 9)


def decodificar(b, dias):
    p = np.frombuffer(zlib.decompress(b), dtype=np.uint8).reshape(2, dias)
    q = np.ascontiguousarray(p.T).view(np.uint16).reshape(-1)
    return np.where(q == SEM_DADO, np.nan, q / 10.0)


def main():
    t0 = dt.datetime.now()
    ds = xr.open_dataset(EOBS)
    x = np.concatenate([ds.rr.sel(time=str(a), **BOX).values for a in range(1950, 2026)], axis=0)       # (dias, lat, lon)
    lat = ds.rr.sel(time="1950-01-01", **BOX).latitude.values
    lon = ds.rr.sel(time="1950-01-01", **BOX).longitude.values
    tempo = pd.date_range("1950-01-01", "2025-12-31")
    assert len(tempo) == x.shape[0], (len(tempo), x.shape)
    valida = np.isfinite(x).mean(axis=0) >= 0.99
    print("células E-OBS com dado:", int(valida.sum()), flush=True)

    db_arq = os.path.join(AQUI, "ibe_prototipo.db")
    if os.path.exists(db_arq):
        os.remove(db_arq)
    db = sqlite3.connect(db_arq); db.executescript(ESQUEMA)
    meta = {}
    for l in open(os.path.join(FONTES, "LEIA.txt"), encoding="utf-8", errors="replace") if os.path.exists(os.path.join(FONTES, "LEIA.txt")) else []:
        pass
    db_atual = sqlite3.connect(f"file:{BASE_ATUAL}?mode=ro", uri=True)
    m_atual = dict(db_atual.execute("select chave, valor from metadados"))
    db.execute("insert into fonte values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ("eobs_v33", "grade", "E-OBS ensemble mean (rr)", "v33.0e", 0.1, "1950-01-01", "2025-12-31",
               "06-06 UTC", "Uso estritamente não comercial em pesquisa e educação (E-OBS product licence, rev. 1); citar Cornes et al. (2018)",
               m_atual.get("citacao", "Cornes et al. (2018) doi:10.1029/2017JD028200"), "https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php",
               "2026-10-07", m_atual.get("sha256_eobs", ""), "a confirmar (a licença não trata a redistribuição)"))
    ids = {}
    k = 0
    pontos = []
    for a in range(len(lat)):
        for b in range(len(lon)):
            if valida[a, b]:
                ids[(a, b)] = k; pontos.append((k, "eobs_v33", "celula", float(lat[a]), float(lon[b]), None, f"{lat[a]:.2f}_{lon[b]:.2f}", None, None)); k += 1
    db.executemany("insert into ponto values (?,?,?,?,?,?,?,?,?)", pontos)
    # séries em blocos de 10 anos
    blocos = [(1950 + 10 * i, 1950 + 10 * i + 9 if i < 7 else 2025) for i in range(8)]
    anos = tempo.year.values
    linhas = []
    for (a, b), pid in ids.items():
        for ini, fim in blocos:
            sel = (anos >= ini) & (anos <= fim)
            linhas.append((pid, ini, int(sel.sum()), codificar(x[sel, a, b]), None))
        if len(linhas) > 5000:
            db.executemany("insert into serie_bloco values (?,?,?,?,?)", linhas); linhas = []
    db.executemany("insert into serie_bloco values (?,?,?,?,?)", linhas); db.commit()
    print("séries gravadas;", (dt.datetime.now() - t0).seconds, "s", flush=True)

    # unidades de Portugal: células com o centro dentro do concelho; senão a mais próxima do centroide
    caop = gpd.read_file(CAOP, layer="cont_municipios").to_crs(4326)
    proj = caop.to_crs(3763)
    LA, LO = np.meshgrid(lat, lon, indexing="ij")
    atual = {r[0]: r for r in db_atual.execute("select dtmn, concelho, distrito, metodo from series")}
    unidades, pesos, qual = [], [], []
    for i, r in caop.iterrows():
        pol = r.geometry
        dentro = contains_xy(pol, LO, LA) & valida
        cel = [(int(a), int(b)) for a, b in np.argwhere(dentro)]
        metodo = "dentro"
        if not cel:
            # mesma célula que a base atual registou (a E-OBS tem centros em x,x5: lat e lon do texto do método)
            m_ = re.search(r"\(([-\d.]+), ([-\d.]+)\)", atual[r["dtmn"]][3])
            la0, lo0 = float(m_.group(1)), float(m_.group(2))
            d2 = np.where(valida, (LA - la0) ** 2 + (LO - lo0) ** 2, np.inf)
            a, b = np.unravel_index(int(d2.argmin()), d2.shape); cel = [(int(a), int(b))]; metodo = "centroide"
        uid = "PT-" + r["dtmn"]
        rp = pol.representative_point()
        unidades.append((uid, r["municipio"], "PT", "concelho", r["distrito_ilha"], r["nuts2"], float(rp.y), float(rp.x), float(r["area_ha"]) / 100))
        for c in cel:
            pesos.append((uid, ids[c], 1.0 / len(cel), metodo))
        qual.append(dict(uid=uid, n=len(cel), metodo=metodo, cel=cel, dtmn=r["dtmn"]))
    db.executemany("insert into unidade values (?,?,?,?,?,?,?,?,?)", unidades)
    db.executemany("insert into unidade_ponto values (?,?,?,?)", pesos)
    # séries repetidas (mesmo conjunto de células)
    chave = {}
    for q in qual:
        chave.setdefault(tuple(sorted(q["cel"])), []).append(q["uid"])
    rep = {u: [o for o in v if o != u] for v in chave.values() if len(v) > 1 for u in v}
    db.commit()

    # reconstrução contra a base atual
    dif_max, dif_med = [], []
    for q in qual:
        w = [r for r in pesos if r[0] == q["uid"]]
        serie = np.zeros(len(tempo))
        for _, pid, peso, _m in w:
            parts = [decodificar(b, d) for d, b in db.execute("select dias, dados from serie_bloco where ponto_id=? order by ano_ini", (pid,))]
            serie += peso * np.concatenate(parts)
        ref = np.frombuffer(zlib.decompress(db_atual.execute("select dados from series where dtmn=?", (q["dtmn"],)).fetchone()[0]), dtype=np.float32).astype(float)
        d = np.abs(serie - ref); dif_max.append(float(np.nanmax(d))); dif_med.append(float(np.nanmean(d)))
        q["serie"] = serie
    print("reconstrução: diferença máxima %.3f mm, média %.5f mm" % (max(dif_max), np.mean(dif_med)), flush=True)

    # Iberia01 por unidade (células com o centro dentro do concelho; senão a mais próxima)
    ib = xr.open_dataset(IBERIA01)["pr"].load()
    ilat, ilon = ib.lat.values, ib.lon.values
    iLA, iLO = np.meshgrid(ilat, ilon, indexing="ij")
    itemp = pd.DatetimeIndex(ib.time.values)
    i71 = (tempo >= "1971-01-01") & (tempo <= "2000-12-31")      # 1971-2000: período de referência recomendado pelos autores do Iberia01
    i71_ib = itemp <= "2000-12-31"
    mes71 = tempo[i71].month.values
    ano71 = tempo[i71].year.values
    est = pd.read_csv(os.path.join(C.RESULTADOS, "resultados_por_concelho.csv"))
    est = est.set_index("concelho")
    nomes = {u[0]: u[1] for u in unidades}
    corr_linhas = []
    for q in qual:
        i = int(np.where(caop.dtmn == q["dtmn"])[0][0]); pol = caop.geometry.iloc[i]
        dentro = contains_xy(pol, iLO, iLA) & np.isfinite(ib.values[0])
        if not dentro.any():
            rp = pol.representative_point()
            d2 = np.where(np.isfinite(ib.values[0]), (iLA - rp.y) ** 2 + (iLO - rp.x) ** 2, np.inf); dentro = d2 == d2.min()
        si = np.nanmean(ib.values[i71_ib][:, dentro], axis=1); se = q["serie"][i71]
        anos = len(si) / 365.25
        dtot = (se.sum() / si.sum() - 1) * 100
        r = float(np.corrcoef(si, se)[0, 1])
        dd = ((se >= 1).mean() - (si >= 1).mean()) * 100
        p95i = np.percentile(si[si >= 1], 95); p95e = np.percentile(se[se >= 1], 95)
        rxi = np.mean([si[ano71 == a].max() for a in range(1971, 2001)]); rxe = np.mean([se[ano71 == a].max() for a in range(1971, 2001)])
        q.update(dtot=dtot, r=r, dd=dd, dp95=(p95e / p95i - 1) * 100, drx=(rxe / rxi - 1) * 100)
        # nível de qualidade (critérios propostos; ver relatório)
        rep_c = rep.get(q["uid"], [])
        if q["metodo"] == "centroide" or q["n"] == 1 or rep_c:
            nivel = "C"
        elif abs(dtot) <= 10 and q["dp95"] >= -15 and q["n"] >= 3:
            nivel = "A"
        elif abs(dtot) <= 20 and q["dp95"] >= -25:
            nivel = "B"
        else:
            nivel = "C"
        motivos = []
        if q["metodo"] == "centroide": motivos.append("nenhuma célula da grade tem o centro dentro do concelho; usada a mais próxima do centroide")
        elif q["n"] == 1: motivos.append("série de uma única célula de cerca de 10 km")
        if rep_c: motivos.append("a série é igual à de " + ", ".join(nomes[x] for x in rep_c))
        if dtot < -10: motivos.append("a E-OBS dá %.0f %% menos chuva que o Iberia01 (rede densa)" % abs(dtot))
        if q["dp95"] < -15: motivos.append("extremos diários %.0f %% abaixo do Iberia01" % abs(q["dp95"]))
        nome = nomes[q["uid"]]
        e = est.loc[nome] if nome in est.index else None
        if e is not None and hasattr(e, "estacao") and not isinstance(e, pd.DataFrame):
            en, ed, ei, ep, er = e.estacao, float(e.dist_km), e.independente, float(e.pbias_pct), float(e.r_diario)
        else:
            en = ed = ei = ep = er = None
        q.update(nivel=nivel, aviso="; ".join(motivos) if motivos else "")
        db.execute("insert into qualidade values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (q["uid"], q["n"], q["metodo"], ", ".join(nomes[x] for x in rep_c) or None, en, ed, ei, ep, er,
                   float(dtot), r, float(dd), float(q["dp95"]), float(q["drx"]), nivel, q["aviso"]))
        # correção de escala opcional: razão mensal Iberia01 / E-OBS em 1971-2015 (ficheiro à parte, ODbL)
        for m in range(1, 13):
            a, b = si[mes71 == m].sum(), se[mes71 == m].sum()
            corr_linhas.append((q["uid"], m, float(a / b) if b > 0 else 1.0, float(rxi / rxe), float(np.percentile(se[se >= 1], 90)), "Iberia01 v1.0", "1971-2000", None, float(abs(dtot))))
    # não cobertos (Madeira e Açores), como na base atual
    for r in db_atual.execute("select dtmn, concelho, motivo from nao_cobertos"):
        db.execute("insert into nao_coberto values (?,?,?)", r)
    for k_, v in (("schema_versao", "0.1 (protótipo)"), ("criado_em", dt.datetime.now(dt.timezone.utc).isoformat()), ("celulas", str(len(ids))), ("periodo", "1950-01-01 a 2025-12-31"),
                  ("codificacao", "uint16 em 0,1 mm; 65535 sem dado; planos de byte + zlib; blocos de 10 anos"), ("regiao", "Península Ibérica (36,0–43,9 N; 9,6 O–4,4 E)"),
                  ("niveis", "A: >=3 células, |Δtotal|<=10 %, ΔP95>=-15 % (contra o Iberia01, 1971-2000); B: |Δtotal|<=20 %, ΔP95>=-25 %; C: o resto, 1 célula, centroide ou série repetida")):
        db.execute("insert into metadados values (?,?)", (k_, v))
    db.commit()
    # ficheiro de correção separado
    cor_arq = os.path.join(AQUI, "ibe_correcao.db")
    if os.path.exists(cor_arq):
        os.remove(cor_arq)
    c = sqlite3.connect(cor_arq)
    c.executescript("CREATE TABLE correcao (unidade_id TEXT, mes INTEGER, fator_total REAL, fator_extremos REAL, limiar_mm REAL, referencia TEXT, periodo_calibracao TEXT, n_estacoes INTEGER, incerteza REAL);"
                    "CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);")
    c.executemany("insert into correcao values (?,?,?,?,?,?,?,?,?)", corr_linhas)
    c.executemany("insert into metadados values (?,?)", [("licenca", "Open Database License (ODbL) 1.0, derivada do Iberia01 v1.0 (Herrera et al., 2019; doi:10.20350/digitalCSIC/8641); atribuição obrigatória"),
                  ("aviso", "Parâmetros experimentais, desligados por defeito. Não alteram a série da E-OBS; quem os liga aplica a razão mensal e o fator de extremos."),
                  ("atribuicao", "Contains information from Iberia01, made available under the Open Database License.")])
    c.commit(); c.close(); db.close()
    # relatório
    q = pd.DataFrame([{k: v for k, v in z.items() if k not in ("cel", "serie")} for z in qual])
    tam = os.path.getsize(db_arq) / 1e6
    rel = f"""# Protótipo do banco IBE: relatório
- Gerado em {dt.datetime.now().isoformat(timespec='seconds')}
- Células E-OBS com dado na Península: {len(ids)}; tamanho de `ibe_prototipo.db`: {tam:.0f} MB; `ibe_correcao.db`: {os.path.getsize(cor_arq) / 1e6:.2f} MB
- Reconstrução das {len(qual)} séries dos concelhos contra o `portugal_eobs.db` atual: diferença máxima {max(dif_max):.3f} mm, média {np.mean(dif_med):.5f} mm (arredondamento a 0,1 mm)
- Níveis de qualidade: {q.nivel.value_counts().to_dict()}
- Concelhos de uma célula: {int((q.n == 1).sum())}; pelo centroide: {int((q.metodo == 'centroide').sum())}; séries repetidas: {len(rep)}
"""
    open(os.path.join(C.RESULTADOS, "relatorio_prototipo.md"), "w", encoding="utf-8").write(rel); print(rel)
    q.drop(columns=["dtmn"]).to_csv(os.path.join(C.RESULTADOS, "qualidade_prototipo.csv"), index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
