# -*- coding: utf-8 -*-
"""Gera os logos das edições a partir do logo do Triton: o planeta (a gota) ganha uma marca "tatuada".

    BRL  mapa do Brasil, com as divisas dos estados
    INT  globo terrestre, com meridianos e paralelos
    PRT  mapa de Portugal continental

Parte de `icons/Triton2.png` (logo com anéis) e grava, na pasta de saída:
    Triton2.png      logo 600 x 486, fundo transparente
    triton.png/.ico e icon.png/.ico      ícone do aplicativo (azulejo 256 x 256)

Uso (da raiz do repositório principal):
    python scripts/gerar_logos_edicoes.py --saida icons/edicoes        # as três, para conferir
    python scripts/gerar_logos_edicoes.py --aplicar ../triton_brl ../triton_int ../triton_prt
O segundo comando substitui os ícones nas cópias de cada edição. O repositório principal não muda.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[1]
SS = 4                                  # supersampling para suavizar as bordas
CLARO = (196, 218, 242, 255)            # preenchimento da marca
LINHA = (255, 255, 255, 255)
AZUL = (31, 73, 125, 255)


def mascara_do_planeta(img: Image.Image) -> np.ndarray:
    """A gota: o azul sólido que sobra depois de apagar as linhas finas dos anéis."""
    a = np.array(img.convert("RGBA"))
    azul = ((a[..., 0] < 90) & (a[..., 1] < 120) & (a[..., 2] > 80) & (a[..., 3] > 128)).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    solido = cv2.morphologyEx(azul, cv2.MORPH_OPEN, k)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(solido, 8)
    if n <= 1:
        raise SystemExit("não achei a gota no logo")
    maior = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return lab == maior


def _projetar(geom, bbox, caixa):
    """Longitude e latitude -> pixels, preservando a proporção (cos da latitude média)."""
    minx, miny, maxx, maxy = bbox
    lat0 = math.radians((miny + maxy) / 2)
    sx = math.cos(lat0)
    w, h = (maxx - minx) * sx, (maxy - miny)
    x0, y0, x1, y1 = caixa
    esc = min((x1 - x0) / w, (y1 - y0) / h)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    def f(x, y):
        return (cx + ((x - (minx + maxx) / 2) * sx) * esc, cy - (y - (miny + maxy) / 2) * esc)
    return f


def _poligonos(geom):
    if geom.geom_type == "Polygon":
        yield geom
    else:
        for g in geom.geoms:
            yield from _poligonos(g)


def _contorno(pais, tam, caixa, largura):
    """Só o contorno externo, em linha branca, sem preenchimento (marca minimalista)."""
    f = _projetar(pais, pais.bounds, caixa)
    cam = Image.new("RGBA", tam, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    for p in _poligonos(pais):
        pts = [f(x, y) for x, y in p.exterior.coords]
        d.line(pts + [pts[0]], fill=LINHA, width=largura, joint="curve")
    return cam


def marca_brasil(tam, caixa):
    import geopandas as gpd
    g = gpd.read_file(RAIZ / "data" / "brazilSHP" / "BR_UF_2022.shp")
    pais = g.geometry.union_all().simplify(0.03)
    return _contorno(pais, tam, caixa, max(6, tam[0] // 200))


def marca_portugal(tam, caixa):
    import geopandas as gpd
    g = gpd.read_file(RAIZ / "data" / "portugal" / "fontes" / "caop" / "Continente_CAOP2025.gpkg", layer="cont_areas_administrativas")
    pais = g.to_crs(4326).geometry.union_all().simplify(0.01)
    return _contorno(pais, tam, caixa, max(6, tam[0] // 200))


def marca_globo(tam, caixa):
    x0, y0, x1, y1 = caixa
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) / 2
    cam = Image.new("RGBA", tam, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
    lw = max(3, tam[0] // 260)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LINHA, width=lw + 1)
    tilt = math.radians(20)                                         # eixo levemente inclinado
    def orto(lon, lat):
        lon, lat = math.radians(lon), math.radians(lat)
        x = math.cos(lat) * math.sin(lon); y = math.sin(lat); z = math.cos(lat) * math.cos(lon)
        yy = y * math.cos(tilt) - z * math.sin(tilt); zz = y * math.sin(tilt) + z * math.cos(tilt)
        return cx + r * x, cy - r * yy, zz
    for lat in range(-60, 61, 30):                                   # paralelos
        pts = [orto(lon, lat) for lon in range(-90, 91, 3)]
        seg = []
        for x, y, z in pts:
            if z >= 0: seg.append((x, y))
            elif len(seg) > 1: d.line(seg, fill=LINHA, width=lw); seg = []
            else: seg = []
        if len(seg) > 1: d.line(seg, fill=LINHA, width=lw)
    for lon in range(-90, 91, 30):                                   # meridianos
        seg = []
        for lat in range(-90, 91, 3):
            x, y, z = orto(lon, lat)
            if z >= 0: seg.append((x, y))
            elif len(seg) > 1: d.line(seg, fill=LINHA, width=lw); seg = []
            else: seg = []
        if len(seg) > 1: d.line(seg, fill=LINHA, width=lw)
    return cam


MARCAS = {"brl": marca_brasil, "int": marca_globo, "prt": marca_portugal}


def logo(edicao: str) -> Image.Image:
    base = Image.open(RAIZ / "icons" / "Triton2.png").convert("RGBA")
    m = mascara_do_planeta(base)
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    larg, alt = x1 - x0, y1 - y0
    # caixa da marca: a parte larga da gota, um pouco recuada
    # caixa da marca, em fração da gota: o globo fica menor; os contornos de país usam mais da gota
    fx, fy0, fy1 = {"int": (0.14, 0.30, 0.10), "brl": (0.15, 0.31, 0.09), "prt": (0.08, 0.20, 0.12)}[edicao]
    caixa = ((x0 + fx * larg) * SS, (y0 + fy0 * alt) * SS, (x1 - fx * larg) * SS, (y1 - fy1 * alt) * SS)
    cam = MARCAS[edicao]((base.width * SS, base.height * SS), caixa).resize(base.size, Image.LANCZOS)
    ca = np.array(cam); out = np.array(base)
    pinta = m & (ca[..., 3] > 0)
    a = ca[..., 3:4].astype(float) / 255
    out[pinta, :3] = (ca[..., :3][pinta] * a[pinta] + out[..., :3][pinta] * (1 - a[pinta])).astype(np.uint8)
    return Image.fromarray(out)


def azulejo(img: Image.Image, lado: int = 256) -> Image.Image:
    """Ícone do aplicativo: quadrado arredondado claro com o logo no meio."""
    t = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle((18, 18, lado - 18, lado - 18), radius=int(lado * 0.22), fill=(246, 244, 240, 255))
    cx = img.crop(img.getbbox())
    esc = (lado * 0.72) / max(cx.size)
    cx = cx.resize((int(cx.width * esc), int(cx.height * esc)), Image.LANCZOS)
    t.alpha_composite(cx, ((lado - cx.width) // 2, (lado - cx.height) // 2))
    return t


def gravar(edicao: str, pasta: Path, nome_logo: str = "Triton2.png", nomes_icone=("triton", "icon")) -> None:
    pasta.mkdir(parents=True, exist_ok=True)
    L = logo(edicao); L.save(pasta / nome_logo)
    A = azulejo(L)
    for nome in nomes_icone:
        A.save(pasta / f"{nome}.png")
        A.save(pasta / f"{nome}.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", help="grava as três edições em <saida>/<brl|int|prt> para conferir")
    ap.add_argument("--aplicar", nargs=3, metavar=("BRL", "INT", "PRT"), help="pastas das cópias: substitui <pasta>/icons")
    a = ap.parse_args()
    if a.saida:
        for ed in MARCAS:
            gravar(ed, Path(a.saida) / ed); print("gerado:", Path(a.saida) / ed)
    if a.aplicar:
        for ed, pasta in zip(("brl", "int", "prt"), a.aplicar):
            gravar(ed, Path(pasta) / "icons"); print("aplicado em", Path(pasta) / "icons")


if __name__ == "__main__":
    main()
