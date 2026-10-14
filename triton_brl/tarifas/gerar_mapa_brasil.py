# -*- coding: utf-8 -*-
"""O contorno dos 27 estados em SVG, simplificado, para a lista de coleta.

Lê `data/brazilSHP/BR_UF_2022` (malha estadual do IBGE, 2022) sem biblioteca de
geoprocessamento: o formato .shp de polígonos e o .dbf são lidos à mão. Os contornos
passam por Douglas-Peucker e por uma projeção equiretangular centrada em 15° S, e
ilhas pequenas demais para aparecer no mapa são descartadas.

Saída: `tarifas/mapa_brasil_uf.json`, com a caixa da projeção e um caminho SVG por UF.
`gerar_lista_de_coleta.py` usa a mesma projeção para pôr as cidades no mapa. Só é
preciso rodar de novo se a malha mudar.

Uso:
    python tarifas/gerar_mapa_brasil.py
"""

from __future__ import annotations

import json
import math
import os
import struct

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE = os.path.join(RAIZ, "data", "brazilSHP", "BR_UF_2022")
SAIDA = os.path.join(AQUI, "mapa_brasil_uf.json")

#: Tolerância da simplificação, em graus, e menor área de anel que fica no mapa.
TOLERANCIA = 0.04
AREA_MINIMA = 0.02
LARGURA = 1000.0
LAT0 = -15.0


def ler_dbf(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()
    n, cab, reg = struct.unpack("<IHH", dados[4:12])
    campos, pos = [], 32
    while dados[pos] != 0x0D:
        nome = dados[pos:pos + 11].split(b"\0")[0].decode("latin-1")
        campos.append((nome, dados[pos + 16]))
        pos += 32
    linhas = []
    for i in range(n):
        ini = cab + i * reg + 1
        linha = {}
        for nome, tam in campos:
            linha[nome] = dados[ini:ini + tam].decode("utf-8", "replace").strip()
            ini += tam
        linhas.append(linha)
    return linhas


def ler_shp(caminho):
    """Lista de polígonos; cada polígono é uma lista de anéis [(lon, lat), ...]."""
    with open(caminho, "rb") as f:
        dados = f.read()
    pos, poligonos = 100, []
    while pos < len(dados):
        _, tamanho = struct.unpack(">ii", dados[pos:pos + 8])
        pos += 8
        tipo = struct.unpack("<i", dados[pos:pos + 4])[0]
        if tipo == 0:
            poligonos.append([])
        else:
            npartes, npontos = struct.unpack("<ii", dados[pos + 36:pos + 44])
            partes = list(struct.unpack(f"<{npartes}i", dados[pos + 44:pos + 44 + 4 * npartes]))
            ini = pos + 44 + 4 * npartes
            pontos = struct.unpack(f"<{2 * npontos}d", dados[ini:ini + 16 * npontos])
            pts = list(zip(pontos[0::2], pontos[1::2]))
            partes.append(npontos)
            poligonos.append([pts[partes[k]:partes[k + 1]] for k in range(npartes)])
        pos += 2 * tamanho
    return poligonos


def area(anel):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(anel, anel[1:] + anel[:1]))) / 2


def douglas_peucker(pts, tol):
    if len(pts) < 3:
        return pts
    manter = [False] * len(pts)
    manter[0] = manter[-1] = True
    pilha = [(0, len(pts) - 1)]
    while pilha:
        a, b = pilha.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        norma = math.hypot(dx, dy) or 1e-12
        maior, idx = -1.0, -1
        for i in range(a + 1, b):
            x, y = pts[i]
            d = abs(dy * (x - x1) - dx * (y - y1)) / norma
            if d > maior:
                maior, idx = d, i
        if maior > tol:
            manter[idx] = True
            pilha += [(a, idx), (idx, b)]
    return [p for p, m in zip(pts, manter) if m]


def simplificar_anel(anel, tol):
    """O anel começa e termina no mesmo ponto: divide no ponto mais distante do início."""
    x0, y0 = anel[0]
    k = max(range(len(anel)), key=lambda i: (anel[i][0] - x0) ** 2 + (anel[i][1] - y0) ** 2)
    return douglas_peucker(anel[:k + 1], tol)[:-1] + douglas_peucker(anel[k:], tol)


def projetor(lon_min, lon_max, lat_min, lat_max):
    k = math.cos(math.radians(LAT0))
    escala = LARGURA / ((lon_max - lon_min) * k)
    altura = (lat_max - lat_min) * escala

    def p(lon, lat):
        return ((lon - lon_min) * k * escala, (lat_max - lat) * escala)
    return p, altura


def main() -> int:
    linhas = ler_dbf(BASE + ".dbf")
    poligonos = ler_shp(BASE + ".shp")
    todos = [pt for poli in poligonos for anel in poli for pt in anel]
    lon_min = min(p[0] for p in todos) - 0.3
    lon_max = max(p[0] for p in todos) + 0.3
    lat_min = min(p[1] for p in todos) - 0.3
    lat_max = max(p[1] for p in todos) + 0.3
    proj, altura = projetor(lon_min, lon_max, lat_min, lat_max)
    estados = {}
    for linha, poli in zip(linhas, poligonos):
        uf = linha.get("SIGLA_UF") or linha.get("SIGLA")
        partes = []
        for anel in poli:
            if area(anel) < AREA_MINIMA:
                continue
            simples = simplificar_anel(anel, TOLERANCIA)
            if len(simples) < 4:
                continue
            xy = [proj(*p) for p in simples]
            partes.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in xy) + "Z")
        cx, cy = proj(*_centro(poli))
        estados[uf] = {"nome": linha.get("NM_UF", uf), "d": "".join(partes),
                       "cx": round(cx, 1), "cy": round(cy, 1)}
    saida = {"fonte": "IBGE, malha estadual BR_UF_2022, simplificada",
             "caixa": [lon_min, lon_max, lat_min, lat_max], "lat0": LAT0,
             "largura": LARGURA, "altura": round(altura, 1), "estados": estados}
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        json.dump(saida, f, ensure_ascii=False, separators=(",", ":"))
    print(f"mapa: {len(estados)} UFs, {os.path.getsize(SAIDA) / 1024:.0f} kB -> "
          f"{os.path.relpath(SAIDA, RAIZ)}")
    return 0


def _centro(poli):
    """Centroide do maior anel, para o rótulo da UF."""
    anel = max(poli, key=area)
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(anel, anel[1:] + anel[:1]):
        f = x1 * y2 - x2 * y1
        a += f
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    a *= 0.5
    return (cx / (6 * a), cy / (6 * a))


if __name__ == "__main__":
    raise SystemExit(main())
