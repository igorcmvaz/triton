"""Esquema 3D da tubulação organizada pelo projetista.

Não é uma vista em escala: é um diagrama para ler o sistema. Uma perspectiva em
escala confunde justamente onde importa — um trecho de 12 m esmaga as conexões
de 30 cm junto à bomba, e um desnível de 3 cm de declividade some. Por isso:

* **Posições ordenadas, não medidas.** Em cada eixo, as coordenadas distintas
  são ordenadas e espaçadas por uma função côncava da distância real: o que está
  à frente continua à frente, o que está acima continua acima, pontos coincidentes
  continuam ligados, mas trechos curtos ganham espaço e os longos não dominam.
* **Medidas reais escritas.** Todo segmento legível traz o comprimento real;
  subidas e descidas trazem seta vertical; trechos por gravidade trazem a
  declividade. Desníveis pequenos (menores que ``_SNAP_MM``) são desenhados
  planos e informados em texto, em vez de virarem um degrau exagerado.
* **Níveis como referência.** Cada cota em que há componente vira um plano
  tracejado com a cota real, para que a leitura vertical não dependa da escala.
* **Projeção cavaleira.** Largura na horizontal, altura na vertical e
  profundidade em diagonal: verticais continuam verticais e horizontais em x
  continuam horizontais, o que se lê mais depressa que uma isométrica.
* **Sequência e sentido.** O número de cada trecho fica na sua origem e se
  repete na tabela ao lado; setas no meio dos segmentos dão o sentido de
  montagem, que é o sentido do escoamento quando o trecho é organizado assim.
"""

from __future__ import annotations

import math
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .pipe_network import SYSTEMS_BY_ID, lengths_by_dn
from .plant_3d import _checked_manifest


# Coordenadas a menos disto (a partir do início do grupo) ocupam a mesma posição.
_SNAP_MM = 50.0
# Espaço mínimo entre posições distintas, como fração do maior intervalo.
_MIN_GAP_WEIGHT = 0.3
# Direção da profundidade (eixo y) na projeção cavaleira.
_DEPTH_ANGLE = math.radians(35.0)

_WIDTH, _HEIGHT = 1280.0, 820.0
_PANEL_W = 400.0
_MARGIN = 48.0
_LABEL_ROOM = 170.0

_TYPE_LABELS = {
    "cisterna_inferior": "Cisterna",
    "reservatorio_superior": "Reservatório superior",
    "filtro_pluvial": "Filtro",
    "first_flush": "Descarte (first flush)",
    "motobomba": "Motobomba",
    "registro_gaveta": "Registro de gaveta",
    "registro_esfera": "Registro de esfera",
    "valvula_retencao": "Válvula de retenção",
    "air_gap": "Air gap",
    "ladrao_sifonado": "Ladrão sifonado",
    "ponto_nao_potavel": "Ponto não potável",
}
_TANKS = {"cisterna_inferior", "reservatorio_superior"}


def _br(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}".replace(".", ",")


def _cota(z_mm: float) -> str:
    meters = z_mm / 1000.0 + 0.0
    return ("+" if meters >= 0 else "−") + _br(abs(meters))


class _AxisScale:
    """Mapeia coordenadas reais em posições ordenadas de 0 a 1."""

    def __init__(self, values: Iterable[float]):
        anchors: List[float] = []
        for value in sorted(set(values)):
            if not anchors or value - anchors[-1] > _SNAP_MM:
                anchors.append(value)
        self._anchors = anchors
        gaps = [b - a for a, b in zip(anchors, anchors[1:])]
        largest = max(gaps, default=0.0)
        positions = [0.0]
        for gap in gaps:
            positions.append(positions[-1] + _MIN_GAP_WEIGHT + math.sqrt(gap / largest))
        total = positions[-1]
        self._positions = [p / total if total else 0.0 for p in positions]
        self.span = total

    def __call__(self, value: float) -> float:
        # Grupo cujo início é o maior valor não superior a ``value``.
        index = 0
        for i, anchor in enumerate(self._anchors):
            if anchor <= value + 1e-9:
                index = i
        return self._positions[index]


class _Projection:
    def __init__(self, points: List[Tuple[float, float, float]]):
        xs, ys, zs = zip(*points)
        self.sx, self.sy, self.sz = _AxisScale(xs), _AxisScale(ys), _AxisScale(zs)
        # 140 px à esquerda para as cotas; _LABEL_ROOM à direita para rótulos.
        area_w = _WIDTH - _PANEL_W - 2 * _MARGIN - 140.0 - _LABEL_ROOM
        area_h = _HEIGHT - 2 * _MARGIN - 90.0
        has_depth = self.sy.span > 0
        depth = 0.32 if has_depth else 0.0
        # Largura, profundidade e altura dividem a área disponível.
        self.w = area_w * (1 - depth * math.cos(_DEPTH_ANGLE)) if self.sx.span else 0.0
        self.d = area_w * depth
        self.h = (area_h - self.d * math.sin(_DEPTH_ANGLE)) if self.sz.span else 0.0
        self.origin = (
            _MARGIN + 140.0 + (0 if self.sx.span else area_w / 2 - self.d * math.cos(_DEPTH_ANGLE) / 2),
            _HEIGHT - _MARGIN - 50.0 - (0 if self.sz.span else area_h / 2),
        )

    def __call__(self, x: float, y: float, z: float) -> Tuple[float, float]:
        ox, oy = self.origin
        dx, dy = self.sy(y) * self.d * math.cos(_DEPTH_ANGLE), self.sy(y) * self.d * math.sin(_DEPTH_ANGLE)
        return ox + self.sx(x) * self.w + dx, oy - self.sz(z) * self.h - dy


def _points(manifest: Dict[str, Any]) -> List[Tuple[float, float, float]]:
    points = [(v["x"], v["y"], v["z"]) for run in manifest["pipe_runs"] for v in run["vertices_mm"]]
    points += [(i["position_mm"]["x"], i["position_mm"]["y"], i["position_mm"]["z"]) for i in manifest["instances"]]
    return points


def _warning_locations(manifest: Dict[str, Any]) -> List[Tuple[int, str, Optional[Tuple[str, int]]]]:
    """Numera os avisos e, quando citam um segmento, devolve onde marcá-los."""
    located = []
    for number, text in enumerate(manifest["validation"]["warnings"], start=1):
        match = re.match(r"Trecho (\S+), segmento (\d+):", text)
        located.append((number, text, (match.group(1), int(match.group(2))) if match else None))
    return located


class _Placer:
    """Posiciona rótulos na primeira posição candidata que não colide.

    Os rótulos cruzam linhas com um contorno branco, mas nunca se sobrepõem a
    outro rótulo nem a um símbolo. Sem posição livre, fica a que menos colide:
    uma medida deslocada ainda informa; uma medida omitida, não.
    """

    def __init__(self, right: float):
        self.right = right
        self.boxes: List[Tuple[float, float, float, float]] = []

    def block(self, x0: float, y0: float, x1: float, y1: float) -> None:
        self.boxes.append((x0, y0, x1, y1))

    @staticmethod
    def _box(lines, x: float, y: float, anchor: str) -> Tuple[float, float, float, float]:
        width = max(len(text) * size * (0.6 if weight == "700" else 0.55) for text, size, weight, _ in lines)
        height = sum(size + 3 for _, size, _, _ in lines)
        left = {"start": x, "end": x - width, "middle": x - width / 2}[anchor]
        return (left - 2, y - lines[0][1], left + width + 2, y - lines[0][1] + height)

    def _cost(self, box) -> float:
        x0, y0, x1, y1 = box
        overlap = sum(max(0.0, min(x1, b[2]) - max(x0, b[0])) * max(0.0, min(y1, b[3]) - max(y0, b[1])) for b in self.boxes)
        outside = max(0.0, x1 - self.right) * (y1 - y0) + max(0.0, _MARGIN / 2 - x0) * (y1 - y0) + max(0.0, 64 - y0) * (x1 - x0)
        return overlap + 4 * outside

    def place(self, lines, candidates) -> List[str]:
        options = [(self._cost(self._box(lines, x, y, a)), i, (x, y, a)) for i, (x, y, a) in enumerate(candidates)]
        _, _, (x, y, anchor) = min(options)
        self.block(*self._box(lines, x, y, anchor))
        out: List[str] = []
        offset = 0.0
        for text, size, weight, fill in lines:
            out.extend(_halo(f'<text x="{x:.1f}" y="{y + offset:.1f}" font-size="{size:g}" font-weight="{weight}" '
                             f'text-anchor="{anchor}" fill="{fill}">{escape(text)}</text>'))
            offset += size + 3
        return out


def _segment_candidates(ax: float, ay: float, bx: float, by: float):
    """Posições ao lado do segmento: meio, depois quartos, dos dois lados."""
    positions = [0.5, 0.3, 0.7]
    if abs(bx - ax) < 1.0:  # vertical
        return [(ax + side * 12, ay + (by - ay) * t + 4, "start" if side > 0 else "end") for t in positions for side in (1, -1)]
    return [(ax + (bx - ax) * t, ay + (by - ay) * t + dy, "middle") for t in positions for dy in (-9, 17)]


def _halo(text_element: str) -> List[str]:
    """Contorno branco sob o texto; ``paint-order`` não existe no SVG Tiny do Qt."""
    halo = text_element.replace("<text ", '<text stroke="#ffffff" stroke-width="4" stroke-linejoin="round" ', 1)
    return [halo, text_element]


def _arrow(x: float, y: float, ux: float, uy: float, color: str) -> str:
    """Seta de sentido centrada em (x, y), na cor do sistema."""
    px, py = -uy, ux
    tip = (x + ux * 7, y + uy * 7)
    left = (x - ux * 5 + px * 5, y - uy * 5 + py * 5)
    right = (x - ux * 5 - px * 5, y - uy * 5 - py * 5)
    points = " ".join(f"{a:.1f},{b:.1f}" for a, b in (tip, left, right))
    return f'<polygon points="{points}" fill="{color}" stroke="#ffffff" stroke-width="1"/>'


def _wrap(text: str, width: int) -> List[str]:
    lines: List[str] = []
    for word in text.split():
        if lines and len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += " " + word
        else:
            lines.append(word)
    return lines


def _segment_note(seg: Dict[str, Any], gravity: bool) -> str:
    a, b = seg["start_mm"], seg["end_mm"]
    dz = b["z"] - a["z"]
    horizontal = math.hypot(b["x"] - a["x"], b["y"] - a["y"])
    if horizontal <= 1.0:
        return f"{'↑' if dz > 0 else '↓'} {_br(abs(dz) / 1000.0)} m"
    text = f"{_br(seg['length_mm'] / 1000.0)} m"
    if gravity and abs(dz) > 0.5:
        text += f" · i={_br(-dz / horizontal * 100, 1)}%"
    elif abs(dz) > 0.5:
        text += f" · Δz {'+' if dz > 0 else '−'}{_br(abs(dz) / 1000.0)} m"
    return text


def generate_schematic_3d_svg(project_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """Esquema 3D fora de escala, com medidas reais, níveis e sequência dos trechos."""
    manifest = _checked_manifest(project_data)
    project = _Projection(_points(manifest))
    runs, instances = manifest["pipe_runs"], manifest["instances"]
    warnings = _warning_locations(manifest)
    warn_at = {loc: number for number, _, loc in warnings if loc}

    out: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_WIDTH:.0f}" height="{_HEIGHT:.0f}" '
        f'viewBox="0 0 {_WIDTH:.0f} {_HEIGHT:.0f}" font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{_WIDTH:.0f}" height="{_HEIGHT:.0f}" fill="#ffffff"/>',
        f'<text x="{_MARGIN}" y="34" font-size="19" font-weight="700" fill="#0f172a">'
        f'Esquema 3D da tubulação — {escape(manifest["project"]["name"])}</text>',
        f'<text x="{_MARGIN}" y="54" font-size="11.5" fill="#64748b">Fora de escala: posições ordenadas, '
        f'medidas e cotas reais indicadas. Números = ordem de montagem.</text>',
    ]

    # 1. Níveis: um plano por cota em que há componente (e o zero de referência).
    xs, ys, _ = zip(*_points(manifest))
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    levels: Dict[float, List[str]] = {}
    for item in instances:
        z = item["position_mm"]["z"]
        key = next((k for k in levels if abs(k - z) <= _SNAP_MM), z)
        levels.setdefault(key, []).append(item["instance_id"])
    for z in sorted(levels):
        corners = [project(x0, y0, z), project(x1, y0, z), project(x1, y1, z), project(x0, y1, z)]
        (ax, ay), (bx, by) = corners[0], corners[1]
        pad = 26.0
        c2, c3 = corners[2], corners[3]
        poly = f"{ax - pad:.1f},{ay:.1f} {bx + pad:.1f},{by:.1f} {c2[0] + pad:.1f},{c2[1]:.1f} {c3[0] - pad:.1f},{c3[1]:.1f}"
        out.append(f'<polygon points="{poly}" fill="#f1f5f9" fill-opacity="0.45" stroke="#cbd5e1" stroke-dasharray="5 4" stroke-width="1"/>')
        out.append(f'<text x="{ax - pad - 8:.1f}" y="{ay + 4:.1f}" font-size="12" font-weight="700" text-anchor="end" fill="#334155">'
                   f'Cota {_cota(z)} m</text>')

    # 2. Trechos: linha por sistema e seta de sentido. Os rótulos são reunidos
    # e posicionados no fim, depois de todos os obstáculos serem conhecidos.
    placer = _Placer(right=_WIDTH - _PANEL_W - _MARGIN / 2)
    marks: List[str] = []
    segment_labels = []
    for run in runs:
        system = SYSTEMS_BY_ID[run["system"]]
        color = system["svg"]
        width = 2.5 if run["dn_mm"] < 40 else 4.0 if run["dn_mm"] < 75 else 5.5
        pts = [project(v["x"], v["y"], v["z"]) for v in run["vertices_mm"]]
        out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{color}" '
                   f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')
        longest = max(range(len(run["segments"])), key=lambda i: math.dist(pts[i], pts[i + 1]))
        for index, seg in enumerate(run["segments"]):
            (ax, ay), (bx, by) = pts[index], pts[index + 1]
            size = math.dist((ax, ay), (bx, by))
            mx, my = (ax + bx) / 2, (ay + by) / 2
            if size >= 30:
                out.append(_arrow(mx, my, (bx - ax) / size, (by - ay) / size, color))
                placer.block(mx - 8, my - 8, mx + 8, my + 8)
            number = warn_at.get((run["run_id"], index + 1))
            if number:
                wx, wy = mx + 14, my + 14
                marks.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="8" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>'
                             f'<text x="{wx:.1f}" y="{wy + 4:.1f}" font-size="10" font-weight="700" text-anchor="middle" fill="#ffffff">{number}</text>')
                placer.block(wx - 9, wy - 9, wx + 9, wy + 9)
            if size >= 44:
                note = _segment_note(seg, system["gravity"])
                if index == longest:
                    note = f"DN {run['dn_mm']:g} · {note}"
                segment_labels.append((note, _segment_candidates(ax, ay, bx, by)))
        # O número fica logo depois da origem, para não cobrir o componente.
        (ax, ay), (bx, by) = pts[0], pts[1]
        size = max(math.dist(pts[0], pts[1]), 1e-9)
        step = min(22.0, size / 2)
        sx, sy = ax + (bx - ax) / size * step, ay + (by - ay) / size * step
        marks.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="10" fill="{color}" stroke="#ffffff" stroke-width="2"/>'
                     f'<text x="{sx:.1f}" y="{sy + 4:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="#ffffff">{run["sequence"]}</text>')
        placer.block(sx - 11, sy - 11, sx + 11, sy + 11)

    # 3. Componentes por cima das linhas: símbolo simples, identificação e dado principal.
    component_labels = []
    for item in instances:
        pos = item["position_mm"]
        x, y = project(pos["x"], pos["y"], pos["z"])
        type_id = item["type_id"]
        if type_id in _TANKS:
            out.append(f'<rect x="{x - 22:.1f}" y="{y - 16:.1f}" width="44" height="32" rx="4" fill="#e0f2fe" stroke="#0369a1" stroke-width="1.5"/>')
            placer.block(x - 23, y - 17, x + 23, y + 17)
        elif type_id == "motobomba":
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#fee2e2" stroke="#b91c1c" stroke-width="1.5"/>'
                       f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="#b91c1c">B</text>')
            placer.block(x - 14, y - 14, x + 14, y + 14)
        else:
            out.append(f'<rect x="{x - 8:.1f}" y="{y - 8:.1f}" width="16" height="16" transform="rotate(45 {x:.1f} {y:.1f})" '
                       f'fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
            placer.block(x - 12, y - 12, x + 12, y + 12)
        detail = _TYPE_LABELS.get(type_id, type_id)
        capacity = item["parameters"].get("CAPACIDADE_L")
        if capacity not in (None, ""):
            detail += f" {int(float(capacity)):,} L".replace(",", ".")
        lines = [(item["instance_id"], 12.0, "700", "#0f172a"), (f"{detail} · {_cota(pos['z'])} m", 11.0, "400", "#475569")]
        candidates = [(x + 28, y - 18, "start"), (x - 28, y - 18, "end"), (x + 28, y + 12, "start"),
                      (x - 28, y + 12, "end"), (x, y - 40, "middle"), (x, y + 36, "middle")]
        component_labels.append((lines, candidates))
    out.extend(marks)

    # Componentes primeiro: o nome do equipamento é o que orienta a leitura.
    for lines, candidates in component_labels:
        out.extend(placer.place(lines, candidates))
    for note, candidates in segment_labels:
        out.extend(placer.place([(note, 10.5, "400", "#1e293b")], candidates))

    # 4. Painel: legenda dos sistemas usados, tabela da sequência, totais e avisos.
    px = _WIDTH - _PANEL_W + 8
    out.append(f'<rect x="{px - 16}" y="70" width="{_PANEL_W - 8}" height="{_HEIGHT - 100}" rx="8" fill="#f8fafc" stroke="#e2e8f0"/>')
    y = 98.0
    out.append(f'<text x="{px}" y="{y}" font-size="13" font-weight="700" fill="#0f172a">Sequência de montagem</text>')
    y += 20
    for header, hx in (("Nº", 0), ("Sistema", 26), ("DN", 190), ("Compr.", 228), ("De → Para", 290)):
        out.append(f'<text x="{px + hx}" y="{y}" font-size="10" font-weight="700" fill="#64748b">{header}</text>')
    for run in runs:
        y += 19
        system = SYSTEMS_BY_ID[run["system"]]
        route = f'{run["start_ref"] or "coord."} → {run["end_ref"] or "—"}'
        out.append(f'<circle cx="{px + 7}" cy="{y - 4}" r="8" fill="{system["svg"]}"/>'
                   f'<text x="{px + 7}" y="{y}" font-size="9.5" font-weight="700" text-anchor="middle" fill="#ffffff">{run["sequence"]}</text>')
        cells = ((26, f'{system["label"][:24]}'), (190, f'{run["dn_mm"]:g}'), (228, f'{_br(run["length_mm"] / 1000)} m'), (290, route[:18]))
        for cx, text in cells:
            out.append(f'<text x="{px + cx}" y="{y}" font-size="10.5" fill="#1e293b">{escape(text)}</text>')
    totals = lengths_by_dn(runs)
    if totals:
        y += 30
        out.append(f'<text x="{px}" y="{y}" font-size="13" font-weight="700" fill="#0f172a">Quantitativo por DN</text>')
        for dn, meters in totals.items():
            y += 18
            out.append(f'<text x="{px}" y="{y}" font-size="11" fill="#1e293b">DN {dn:g}: {_br(meters)} m</text>')
    if warnings:
        y += 30
        out.append(f'<text x="{px}" y="{y}" font-size="13" font-weight="700" fill="#b45309">Avisos</text>')
        for number, text, _ in warnings:
            if y > _HEIGHT - 80:
                out.append(f'<text x="{px}" y="{y + 18}" font-size="10" fill="#78350f">… demais avisos no manifesto BIM.</text>')
                break
            y += 18
            out.append(f'<circle cx="{px + 7}" cy="{y - 4}" r="7" fill="#f59e0b"/>'
                       f'<text x="{px + 7}" y="{y}" font-size="9" font-weight="700" text-anchor="middle" fill="#ffffff">{number}</text>')
            for offset, line in enumerate(_wrap(re.sub(r"^Trecho ", "", text), 60)):
                out.append(f'<text x="{px + 20}" y="{y + offset * 13}" font-size="10" fill="#78350f">{escape(line)}</text>')
            y += 13 * (len(_wrap(re.sub(r"^Trecho ", "", text), 60)) - 1)
    used = [s for s in SYSTEMS_BY_ID.values() if any(r["system"] == s["system_id"] for r in runs)]
    lx = _MARGIN
    for system in used:
        out.append(f'<line x1="{lx}" y1="{_HEIGHT - 20}" x2="{lx + 22}" y2="{_HEIGHT - 20}" stroke="{system["svg"]}" stroke-width="4"/>'
                   f'<text x="{lx + 28}" y="{_HEIGHT - 16}" font-size="11" fill="#334155">{escape(system["label"])}</text>')
        lx += 36 + 6.2 * len(system["label"])
    out.append("</svg>")
    svg = "\n".join(out)
    if output_path:
        Path(output_path).write_text(svg, encoding="utf-8")
    return svg
