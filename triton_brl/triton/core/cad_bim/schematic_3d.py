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

from triton.core.component_geometry import component_envelope, fallback_volumes
from triton.core.pipe_network import SYSTEMS_BY_ID, lengths_by_dn
from triton.core.plant_3d import _checked_manifest
from triton.core.dados_do_relatorio import svg_de_exportacao
from triton import marca as _marca


# Coordenadas a menos disto (a partir do início do grupo) ocupam a mesma posição.
_SNAP_MM = 50.0
# Espaço mínimo entre posições distintas, como fração do maior intervalo.
_MIN_GAP_WEIGHT = 0.3
# Direção da profundidade (eixo y) na projeção cavaleira.
_DEPTH_ANGLE = math.radians(35.0)

# Proporção de uma folha A3 deitada: o arranjo completo tem 26 peças e 19
# trechos, e numa folha estreita elas ficavam umas sobre as outras.
_WIDTH, _HEIGHT = 1680.0, 1188.0
_PANEL_W = 480.0
_MARGIN = 48.0
_LABEL_ROOM = 190.0

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
    "freio_dagua": "Freio d'água",
    "succao_flutuante": "Sucção flutuante",
    "sensor_nivel": "Chave de nível",
    "valvula_solenoide": "Válvula solenoide",
    "hidrometro": "Hidrômetro",
    "valvula_pe_crivo": "Válvula de pé com crivo",
    "respiro": "Respiro",
    "quadro_comando": "Quadro de comando",
}
_TANKS = {"cisterna_inferior", "reservatorio_superior"}
#: Peças que definem um nível da instalação e ganham plano de cota e rótulo
#: completo. As demais — registros, válvulas, chaves de nível, respiros — levam
#: só o código no desenho; tipo e cota vão para a tabela de peças do painel.
_PRINCIPAIS = _TANKS | {"motobomba", "filtro_pluvial", "first_flush"}
#: Níveis mais próximos que isto viram um só plano.
_NIVEL_MINIMO_MM = 300.0
#: Distância mínima, em px, entre dois rótulos de cota na margem.
_COTA_MINIMA_PX = 18.0




def _edicao() -> str:
    from triton.core.edition import rotulo_da_edicao

    return rotulo_da_edicao()

def _br(value: float, decimals: int = 2) -> str:
    return f"{value:.{decimals}f}".replace(".", ",")


def _cota(z_mm: float) -> str:
    meters = z_mm / 1000.0 + 0.0
    return ("+" if meters >= 0 else "−") + _br(abs(meters))


class _AxisScale:
    """Mapeia coordenadas reais em posições ordenadas de 0 a 1."""

    def __init__(self, values: Iterable[float], snap: float = _SNAP_MM):
        anchors: List[float] = []
        for value in sorted(set(values)):
            if not anchors or value - anchors[-1] > snap:
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
        # Só a cota é aproximada (declividades); em planta, tubos paralelos
        # próximos precisam continuar separados no desenho.
        self.sx, self.sy, self.sz = _AxisScale(xs, 1.0), _AxisScale(ys, 1.0), _AxisScale(zs)
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


def _points(manifest: Dict[str, Any], envelopes: Optional[Dict[str, Any]] = None) -> List[Tuple[float, float, float]]:
    points = [(v["x"], v["y"], v["z"]) for run in manifest["pipe_runs"] for v in run["vertices_mm"]]
    for item in manifest["instances"]:
        x, y, z = item["position_mm"]["x"], item["position_mm"]["y"], item["position_mm"]["z"]
        points.append((x, y, z))
        env = (envelopes or {}).get(item["instance_id"])
        if env is not None:
            # A envoltória entra na escala: topo e laterais são pontos de conexão.
            points += [(x - env.half_x, y, z), (x + env.half_x, y, z), (x, y - env.half_y, z),
                       (x, y + env.half_y, z), (x, y, z + env.height)]
    return points


def _xyz(p: Dict[str, float]) -> Tuple[float, float, float]:
    return p["x"], p["y"], p["z"]


def _dist_2d(p, a, b) -> float:
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    denom = dx * dx + dy * dy
    t = 0.0 if denom == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / denom))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def _segment_hits_box(a, b, box) -> bool:
    """Liang–Barsky: o segmento a→b atravessa o retângulo?"""
    x0, y0, x1, y1 = box
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


def _stroke_width(run: Dict[str, Any]) -> float:
    return 2.5 if run["dn_mm"] < 40 else 4.0 if run["dn_mm"] < 75 else 5.5


def _pipe_strokes(runs, project) -> List[str]:
    """Segmentos do fundo para a frente, cada um com um vão branco por baixo.

    Convenção de desenho técnico: onde dois tubos se cruzam só na projeção, o
    de trás aparece interrompido e o da frente, contínuo. O vão não chega às
    pontas, para não entalhar as curvas do próprio trecho.
    """
    items = []
    for run in runs:
        color, width = SYSTEMS_BY_ID[run["system"]]["svg"], _stroke_width(run)
        for seg in run["segments"]:
            a, b = seg["start_mm"], seg["end_mm"]
            depth = (a["y"] + b["y"]) / 2 - 1e-6 * (a["z"] + b["z"])  # mais ao fundo = y maior
            items.append((depth, project(a["x"], a["y"], a["z"]), project(b["x"], b["y"], b["z"]), color, width))
    items.sort(key=lambda item: -item[0])
    out = []
    for _, (ax, ay), (bx, by), color, width in items:
        size = math.dist((ax, ay), (bx, by))
        if size > 16:
            ux, uy = (bx - ax) / size, (by - ay) / size
            out.append(f'<line x1="{ax + ux * 8:.1f}" y1="{ay + uy * 8:.1f}" x2="{bx - ux * 8:.1f}" y2="{by - uy * 8:.1f}" '
                       f'stroke="#ffffff" stroke-width="{width + 6}" stroke-linecap="butt"/>')
        out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" '
                   f'stroke-width="{width}" stroke-linecap="round"/>')
    return out


def _component_body(item, env, project, placer, labels) -> List[str]:
    """Corpo do componente como retângulo da base ao topo, na frente (y da base)."""
    pos = item["position_mm"]
    x, y, z = pos["x"], pos["y"], pos["z"]
    left, bottom = project(x - env.half_x, y, z)
    right, top = project(x + env.half_x, y, z + env.height)
    cx = (left + right) / 2
    type_id = item["type_id"]
    min_w, min_h = (40, 26) if type_id in _TANKS else (30, 24) if type_id == "first_flush" else (26, 22) if type_id in {"motobomba", "filtro_pluvial"} else (16, 16)
    if right - left < min_w:
        left, right = cx - min_w / 2, cx + min_w / 2
    if bottom - top < min_h:
        top = bottom - min_h
    fill, stroke = {
        "motobomba": ("#fee2e2", "#b91c1c"),
        "filtro_pluvial": ("#f1f5f9", "#475569"),
        "first_flush": ("#fef3c7", "#b45309"),
    }.get(type_id, ("#e0f2fe", "#0369a1") if type_id in _TANKS else ("#ffffff", "#0f172a"))
    out = [f'<rect x="{left:.1f}" y="{top:.1f}" width="{right - left:.1f}" height="{bottom - top:.1f}" rx="3" '
           f'fill="{fill}" fill-opacity="0.9" stroke="{stroke}" stroke-width="1.5"/>']
    if type_id == "motobomba":
        out.append(f'<text x="{cx:.1f}" y="{(top + bottom) / 2 + 4:.1f}" font-size="11" font-weight="700" '
                   f'text-anchor="middle" fill="#b91c1c">B</text>')
    elif type_id == "filtro_pluvial":
        out.append(f'<text x="{cx:.1f}" y="{(top + bottom) / 2 + 4:.1f}" font-size="10" font-weight="700" '
                   f'text-anchor="middle" fill="#475569">F</text>')
    elif type_id == "first_flush":
        out.append(f'<text x="{cx:.1f}" y="{(top + bottom) / 2 + 4:.1f}" font-size="10" font-weight="700" '
                   f'text-anchor="middle" fill="#b45309">D</text>')
    placer.block(left - 1, top - 1, right + 1, bottom + 1)
    detail = _TYPE_LABELS.get(type_id, type_id)
    params = item.get("parameters") or {}
    capacity = params.get("CAPACIDADE_L") or params.get("VOLUME_L")
    if capacity not in (None, ""):
        detail += f" {int(float(capacity)):,} L".replace(",", ".")
    elif type_id == "filtro_pluvial" and params.get("DN_MM"):
        detail += f" DN {int(float(params['DN_MM']))}"
    elif type_id == "motobomba":
        hp = params.get("POTENCIA_HP_LABEL")
        if hp:
            detail += f" {hp} HP"
    mid = (top + bottom) / 2
    if type_id in _PRINCIPAIS:
        lines = [(item["instance_id"], 12.0, "700", "#0f172a"), (f"{detail} · {_cota(z)} m", 11.0, "400", "#475569")]
        labels.append((lines, [(right + 10, mid - 2, "start"), (left - 10, mid - 2, "end"), (cx, top - 22, "middle"),
                               (cx, bottom + 16, "middle"), (right + 10, top - 6, "start"), (left - 10, top - 6, "end")]))
    else:
        lines = [(item["instance_id"], 10.5, "700", "#334155")]
        near = [(right + 6, mid + 4, "start"), (left - 6, mid + 4, "end"), (cx, top - 6, "middle"),
                (cx, bottom + 14, "middle")]
        far = [(x + dx, y + dy, a) for x, y, a in near for dx, dy in ((0, -16), (0, 16), (14, 0), (-14, 0))]
        labels.append((lines, near + far))
    return out


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
        # Linhas dos tubos: rótulo por cima de outro tubo cria um falso vão.
        self.lines: List[Tuple[Any, Tuple[float, float], Tuple[float, float]]] = []
        self._own: Any = None

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
        crossings = sum(1 for key, a, b in self.lines if key != self._own and _segment_hits_box(a, b, box))
        return overlap + 4 * outside + 400 * crossings

    def place(self, lines, candidates, own: Any = None) -> List[str]:
        self._own = own
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
    positions = [0.5, 0.3, 0.7, 0.2, 0.8, 0.12, 0.88]
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
    fallbacks = fallback_volumes(project_data)
    envelopes = {item["instance_id"]: component_envelope(item, fallbacks) for item in manifest["instances"]}
    project = _Projection(_points(manifest, envelopes))
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
        f'medidas e cotas reais indicadas. Números = ordem de montagem. '
        f'{_marca.NOME} · {escape(_edicao())}.</text>',
    ]

    # 1. Níveis: um plano por cota em que há componente (e o zero de referência).
    xs, ys, _ = zip(*_points(manifest, envelopes))
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    levels: Dict[float, List[str]] = {}
    principais = [i for i in instances if i["type_id"] in _PRINCIPAIS] or instances
    for item in sorted(principais, key=lambda i: i["position_mm"]["z"]):
        z = item["position_mm"]["z"]
        key = next((k for k in levels if abs(k - z) <= _NIVEL_MINIMO_MM), z)
        levels.setdefault(key, []).append(item["instance_id"])
    last_label_y = None
    for z in sorted(levels):
        corners = [project(x0, y0, z), project(x1, y0, z), project(x1, y1, z), project(x0, y1, z)]
        (ax, ay), (bx, by) = corners[0], corners[1]
        pad = 26.0
        c2, c3 = corners[2], corners[3]
        poly = f"{ax - pad:.1f},{ay:.1f} {bx + pad:.1f},{by:.1f} {c2[0] + pad:.1f},{c2[1]:.1f} {c3[0] - pad:.1f},{c3[1]:.1f}"
        out.append(f'<polygon points="{poly}" fill="#f1f5f9" fill-opacity="0.45" stroke="#cbd5e1" stroke-dasharray="5 4" stroke-width="1"/>')
        if last_label_y is not None and abs(last_label_y - ay) < _COTA_MINIMA_PX:
            continue
        last_label_y = ay
        out.append(f'<text x="{ax - pad - 8:.1f}" y="{ay + 4:.1f}" font-size="12" font-weight="700" text-anchor="end" fill="#334155">'
                   f'Cota {_cota(z)} m</text>')

    # 2. Componentes sob as linhas, na altura e largura que ocupam (na escala do
    # esquema): um tubo ligado ao topo ou à lateral encosta no contorno.
    placer = _Placer(right=_WIDTH - _PANEL_W - _MARGIN / 2)
    component_labels = []
    for item in instances:
        out.extend(_component_body(item, envelopes[item["instance_id"]], project, placer, component_labels))

    # 3. Trechos: linha por sistema e seta de sentido. Os rótulos são reunidos
    # e posicionados no fim, depois de todos os obstáculos serem conhecidos.
    marks: List[str] = []
    segment_labels = []
    out.extend(_pipe_strokes(runs, project))
    screen_segments = [(run["run_id"], project(*_xyz(seg["start_mm"])), project(*_xyz(seg["end_mm"])))
                       for run in runs for seg in run["segments"]]
    placer.lines = [((run["run_id"], i), project(*_xyz(seg["start_mm"])), project(*_xyz(seg["end_mm"])))
                    for run in runs for i, seg in enumerate(run["segments"])]
    for run in runs:
        system = SYSTEMS_BY_ID[run["system"]]
        color = system["svg"]
        pts = [project(v["x"], v["y"], v["z"]) for v in run["vertices_mm"]]
        others = [(a, b) for rid, a, b in screen_segments if rid != run["run_id"]]
        longest = max(range(len(run["segments"])), key=lambda i: math.dist(pts[i], pts[i + 1]))
        for index, seg in enumerate(run["segments"]):
            (ax, ay), (bx, by) = pts[index], pts[index + 1]
            size = math.dist((ax, ay), (bx, by))
            mx, my = (ax + bx) / 2, (ay + by) / 2
            if size >= 30:
                # Seta longe de cruzamentos aparentes, para não esconder o vão.
                t = next((t for t in (0.5, 0.35, 0.65, 0.25, 0.75)
                          if all(_dist_2d((ax + (bx - ax) * t, ay + (by - ay) * t), a, b) > 14 for a, b in others)), 0.5)
                px_, py_ = ax + (bx - ax) * t, ay + (by - ay) * t
                out.append(_arrow(px_, py_, (bx - ax) / size, (by - ay) / size, color))
                placer.block(px_ - 8, py_ - 8, px_ + 8, py_ + 8)
            number = warn_at.get((run["run_id"], index + 1))
            if number:
                wx, wy = mx + 14, my + 14
                marks.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="8" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>'
                             f'<text x="{wx:.1f}" y="{wy + 4:.1f}" font-size="10" font-weight="700" text-anchor="middle" fill="#ffffff">{number}</text>')
                placer.block(wx - 9, wy - 9, wx + 9, wy + 9)
            if size >= 56:
                note = _segment_note(seg, system["gravity"])
                if index == longest:
                    note = f"DN {run['dn_mm']:g} · {note}"
                segment_labels.append((note, _segment_candidates(ax, ay, bx, by), (run["run_id"], index), color))
        # O número fica logo depois da origem, para não cobrir o componente.
        (ax, ay), (bx, by) = pts[0], pts[1]
        size = max(math.dist(pts[0], pts[1]), 1e-9)
        step = min(22.0, size / 2)
        sx, sy = ax + (bx - ax) / size * step, ay + (by - ay) / size * step
        marks.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="10" fill="{color}" stroke="#ffffff" stroke-width="2"/>'
                     f'<text x="{sx:.1f}" y="{sy + 4:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="#ffffff">{run["sequence"]}</text>')
        placer.block(sx - 11, sy - 11, sx + 11, sy + 11)

    out.extend(marks)

    # Componentes primeiro: o nome do equipamento é o que orienta a leitura.
    for lines, candidates in component_labels:
        out.extend(placer.place(lines, candidates))
    # Medida na cor do sistema: não há dúvida de a qual tubo ela pertence.
    for note, candidates, own, color in segment_labels:
        out.extend(placer.place([(note, 10.5, "600", color)], candidates, own))

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
    pecas = [i for i in instances if i["type_id"] not in _PRINCIPAIS]
    if pecas and len(pecas) < len(instances):
        y += 30
        out.append(f'<text x="{px}" y="{y}" font-size="13" font-weight="700" fill="#0f172a">Peças e acessórios</text>')
        coluna = (len(pecas) + 1) // 2
        topo = y
        for n, item in enumerate(pecas):
            cx = px + (0 if n < coluna else (_PANEL_W - 40) / 2)
            cy = topo + 17 * (n % coluna + 1)
            tipo = _TYPE_LABELS.get(item["type_id"], item["type_id"])
            out.append(f'<text x="{cx}" y="{cy}" font-size="10" font-weight="700" fill="#334155">{escape(item["instance_id"])}</text>'
                       f'<text x="{cx + 50}" y="{cy}" font-size="10" fill="#1e293b">{escape(tipo[:20])} · {_cota(item["position_mm"]["z"])}</text>')
        y = topo + 17 * coluna
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
    svg = svg_de_exportacao("\n".join(out))
    if output_path:
        Path(output_path).write_text(svg, encoding="utf-8")
    return svg
