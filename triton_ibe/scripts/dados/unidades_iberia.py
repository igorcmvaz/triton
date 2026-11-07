# -*- coding: utf-8 -*-
"""Unidades administrativas da Península Ibérica e ilhas (Edição Ibérica): fontes, tabelas e funções comuns.

Fontes dos limites (todas abertas; as brutas ficam fora do Git, ver ``_caminhos.py``):

- Portugal: CAOP 2025, Direção-Geral do Território (308 municípios; chave = código DTMN de 4 dígitos).
- Espanha, incluindo Baleares, Canárias, Ceuta e Melilla: Eurostat/GISCO, «Local Administrative Units» (LAU)
  2023, ``LAU_RG_01M_2023_4326`` (© EuroGeographics para os limites; a chave LAU_ID é o código INE de 5 dígitos).
  O pedido original apontava para o CNIG/IGN (BDLJE, CC BY 4.0), cujo centro de descargas não oferece ligação direta
  estável nem versão arquivável por script; o LAU do Eurostat deriva dos limites oficiais nacionais, é aberto e
  tem o mesmo código INE (ver auditoria/iberia/DECISOES_ASSUMIDAS.md). O script aceita ``--lau`` com outro ficheiro
  que tenha as colunas CNTR_CODE, LAU_ID, LAU_NAME, POP_2023 e a geometria.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

#: Província INE (2 primeiros dígitos do código) -> (nome, comunidade autónoma / cidade autónoma).
PROVINCIAS = {
    "01": ("Araba/Álava", "País Vasco"), "02": ("Albacete", "Castilla-La Mancha"), "03": ("Alicante/Alacant", "Comunitat Valenciana"),
    "04": ("Almería", "Andalucía"), "05": ("Ávila", "Castilla y León"), "06": ("Badajoz", "Extremadura"),
    "07": ("Illes Balears", "Illes Balears"), "08": ("Barcelona", "Cataluña"), "09": ("Burgos", "Castilla y León"),
    "10": ("Cáceres", "Extremadura"), "11": ("Cádiz", "Andalucía"), "12": ("Castellón/Castelló", "Comunitat Valenciana"),
    "13": ("Ciudad Real", "Castilla-La Mancha"), "14": ("Córdoba", "Andalucía"), "15": ("A Coruña", "Galicia"),
    "16": ("Cuenca", "Castilla-La Mancha"), "17": ("Girona", "Cataluña"), "18": ("Granada", "Andalucía"),
    "19": ("Guadalajara", "Castilla-La Mancha"), "20": ("Gipuzkoa", "País Vasco"), "21": ("Huelva", "Andalucía"),
    "22": ("Huesca", "Aragón"), "23": ("Jaén", "Andalucía"), "24": ("León", "Castilla y León"),
    "25": ("Lleida", "Cataluña"), "26": ("La Rioja", "La Rioja"), "27": ("Lugo", "Galicia"),
    "28": ("Madrid", "Comunidad de Madrid"), "29": ("Málaga", "Andalucía"), "30": ("Murcia", "Región de Murcia"),
    "31": ("Navarra", "Comunidad Foral de Navarra"), "32": ("Ourense", "Galicia"), "33": ("Asturias", "Principado de Asturias"),
    "34": ("Palencia", "Castilla y León"), "35": ("Las Palmas", "Canarias"), "36": ("Pontevedra", "Galicia"),
    "37": ("Salamanca", "Castilla y León"), "38": ("Santa Cruz de Tenerife", "Canarias"), "39": ("Cantabria", "Cantabria"),
    "40": ("Segovia", "Castilla y León"), "41": ("Sevilla", "Andalucía"), "42": ("Soria", "Castilla y León"),
    "43": ("Tarragona", "Cataluña"), "44": ("Teruel", "Aragón"), "45": ("Toledo", "Castilla-La Mancha"),
    "46": ("València/Valencia", "Comunitat Valenciana"), "47": ("Valladolid", "Castilla y León"), "48": ("Bizkaia", "País Vasco"),
    "49": ("Zamora", "Castilla y León"), "50": ("Zaragoza", "Aragón"), "51": ("Ceuta", "Ceuta"), "52": ("Melilla", "Melilla"),
}

#: Regiões sem cobertura do Iberia01 (ERA5, nível C) e as sem cobertura nenhuma.
REGIOES_ERA5 = {"Canarias", "Região Autónoma da Madeira", "Região Autónoma dos Açores"}
REGIOES_SEM_COBERTURA = {"Ceuta": "Ceuta fica fora do domínio do Iberia01 (latitude mínima 36,0° N)",
                         "Melilla": "Melilla fica fora do domínio do Iberia01 (latitude mínima 36,0° N)"}

CAMADAS_CAOP = (
    ("Continente_CAOP2025.gpkg", "cont_municipios", "Continente"),
    ("ArqMadeira_CAOP2025.gpkg", "ram_municipios", "Região Autónoma da Madeira"),
    ("ArqAcores_GCentral_GOriental_CAOP2025.gpkg", "raa_cen_ori_municipios", "Região Autónoma dos Açores"),
    ("ArqAcores_GOcidental_CAOP2025.gpkg", "raa_oci_municipios", "Região Autónoma dos Açores"),
)


def sha256(caminho) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def carregar_unidades(caop_dir: Path, lau: Path):
    """GeoDataFrame (WGS84) com todas as unidades: codigo, pais, regiao, provincia, nome, populacao, geometry."""
    import geopandas as gpd
    import pandas as pd
    linhas = []
    for arquivo, camada, regiao in CAMADAS_CAOP:
        g = gpd.read_file(Path(caop_dir) / arquivo, layer=camada)[["dtmn", "municipio", "distrito_ilha", "geometry"]].to_crs(4326)
        g["codigo"] = "PT-" + g["dtmn"].astype(str).str.zfill(4)
        g["pais"] = "PT"
        g["regiao"] = g["distrito_ilha"] if regiao == "Continente" else regiao
        g["provincia"] = g["distrito_ilha"] if regiao != "Continente" else ""
        g["nome"] = g["municipio"]
        g["populacao"] = None
        linhas.append(g[["codigo", "pais", "regiao", "provincia", "nome", "populacao", "geometry"]])
    e = gpd.read_file(lau)
    e = e[e["CNTR_CODE"] == "ES"].copy()
    e["codigo"] = "ES-" + e["LAU_ID"].astype(str).str.zfill(5)
    e["pais"] = "ES"
    e["provincia"] = e["LAU_ID"].astype(str).str.zfill(5).str[:2].map(lambda c: PROVINCIAS[c][0])
    e["regiao"] = e["LAU_ID"].astype(str).str.zfill(5).str[:2].map(lambda c: PROVINCIAS[c][1])
    e["nome"] = e["LAU_NAME"]
    e["populacao"] = e["POP_2023"]
    linhas.append(e[["codigo", "pais", "regiao", "provincia", "nome", "populacao", "geometry"]].to_crs(4326))
    u = gpd.GeoDataFrame(pd.concat(linhas, ignore_index=True), crs=4326)
    return u.sort_values("codigo").reset_index(drop=True)


ESQUEMA_UNIDADES = """
CREATE TABLE unidade (codigo TEXT PRIMARY KEY, pais TEXT, regiao TEXT, provincia TEXT, nome TEXT, populacao INTEGER,
                      fonte TEXT, cobertura TEXT, metodo TEXT, celulas_dentro INTEGER, dist_celula_km REAL,
                      nivel TEXT, motivo TEXT);
CREATE TABLE unidade_celula (codigo TEXT, celula INTEGER, peso REAL, PRIMARY KEY (codigo, celula));
CREATE TABLE celula (id INTEGER PRIMARY KEY, lat REAL, lon REAL, fonte TEXT, parte TEXT);
CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);
CREATE INDEX unidade_nome ON unidade (nome);
CREATE INDEX unidade_regiao ON unidade (pais, regiao);
"""

#: Nível de qualidade (representação geométrica): ver auditoria/iberia/DECISOES_ASSUMIDAS.md.
def nivel_por_geometria(celulas_dentro: int, dist_km: float, contido: bool = False) -> tuple:
    if celulas_dentro >= 3:
        return "A", f"{celulas_dentro} células do Iberia01 com centro dentro do limite"
    if celulas_dentro >= 1:
        return "B", f"{celulas_dentro} célula(s) do Iberia01 com centro dentro do limite (município pequeno para a grade de 0,1°)"
    if contido:
        return "B", f"município contido numa única célula de 0,1° do Iberia01 (centro a {dist_km:.0f} km do ponto representativo)"
    return "C", f"nenhuma célula com centro dentro do limite; usada a mais próxima ({dist_km:.0f} km do centroide)"


MOTIVO_ILHAS = ("reanálise ERA5 (0,25°) sem validação local; subestimou de 8% a 47% da chuva nas estações de "
                "ilha testadas pelo projeto: use a série da estação")
