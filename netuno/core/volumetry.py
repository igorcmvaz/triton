"""Volumetria 3D do sistema: sólidos simples, em escala, para girar e conferir.

A volumetria não substitui o modelo do Revit; é a maquete de estudo. Cada
elemento vira um sólido reconhecível à distância:

* reservatórios → prismas circulares, dimensionados pela capacidade;
* edificação → prisma retangular translúcido, com as lajes dos pavimentos;
* motobombas → prismas de base losango;
* filtro e descarte → cilindros verticais; válvulas e registros → cubos;
* tubulação → prismas octogonais ao longo de cada segmento, no DN.

Convenções: milímetros, ``z`` para cima, ``position_mm`` dos componentes é o
centro da base. As dimensões que o projetista não informou são estimadas por
regras explícitas (ver :func:`tank_dimensions_mm`) e marcadas como estimadas na
ficha do sólido, nunca apresentadas como medida de projeto.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .pipe_network import SYSTEMS_BY_ID
from .plant_3d import _checked_manifest

Point = Tuple[float, float, float]
Color = Tuple[int, int, int]

# Proporção altura/diâmetro quando o projetista não informa as dimensões:
# cisterna enterrada tende ao cubo; caixa d'água superior é baixa e larga.
_TANK_HEIGHT_RATIO = {"cisterna_inferior": 1.0, "reservatorio_superior": 0.55}
_TUBE_SIDES = 8
_TANK_SIDES = 32
# Tubos finos somem numa maquete de dezenas de metros: abaixo desta fração da
# diagonal da cena, o raio é ampliado para visualização (e isso é declarado).
_MIN_TUBE_RADIUS_FRACTION = 0.0035

_COLORS: Dict[str, Color] = {
    "cisterna_inferior": (56, 142, 196),
    "reservatorio_superior": (79, 172, 222),
    "motobomba": (214, 69, 65),
    "filtro_pluvial": (100, 116, 139),
    "first_flush": (180, 115, 45),
    "registro_gaveta": (51, 65, 85),
    "registro_esfera": (51, 65, 85),
    "valvula_retencao": (51, 65, 85),
    "air_gap": (22, 163, 74),
    "ladrao_sifonado": (100, 116, 139),
    "ponto_nao_potavel": (147, 51, 234),
    "building": (203, 213, 225),
    "ground": (163, 190, 140),
}
_TYPE_NAMES = {
    "cisterna_inferior": "Cisterna",
    "reservatorio_superior": "Reservatório superior",
    "filtro_pluvial": "Filtro pluvial",
    "first_flush": "Descarte (first flush)",
    "motobomba": "Motobomba",
    "registro_gaveta": "Registro de gaveta",
    "registro_esfera": "Registro de esfera",
    "valvula_retencao": "Válvula de retenção",
    "air_gap": "Air gap",
    "ladrao_sifonado": "Ladrão sifonado",
    "ponto_nao_potavel": "Ponto não potável",
}


@dataclass
class Solid:
    """Poliedro de faces planas e convexas, com o que o visualizador precisa."""

    key: str
    kind: str  # pipe, tank, pump, accessory, building, slab, ground
    title: str
    info: List[str]
    color: Color
    faces: List[List[Point]]
    opacity: float = 1.0
    outline: bool = False
    pickable: bool = True
    label_at: Optional[Point] = None
    group: str = ""
    # Tubos: eixo e raio, para o visualizador trocar o prisma por uma linha
    # quando ele ficar mais fino que poucos pixels (nível de detalhe).
    axis: Optional[Tuple[Point, Point, float]] = None


@dataclass
class Scene:
    title: str
    solids: List[Solid]
    bounds: Tuple[Point, Point]
    notes: List[str] = field(default_factory=list)

    @property
    def center(self) -> Point:
        (x0, y0, z0), (x1, y1, z1) = self.bounds
        return ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)

    @property
    def diagonal(self) -> float:
        low, high = self.bounds
        return max(math.dist(low, high), 1.0)


# ── Primitivas ───────────────────────────────────────────────────────────────

def _number(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) and number > 0 else default


def _rotate(points: Sequence[Tuple[float, float]], degrees: float) -> List[Tuple[float, float]]:
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return [(x * c - y * s, x * s + y * c) for x, y in points]


def prism(outline_xy: Sequence[Tuple[float, float]], base: Point, height: float, rotation_deg: float = 0.0) -> List[List[Point]]:
    """Extrusão vertical de um polígono convexo em sentido anti-horário."""
    bx, by, bz = base
    ring = [(bx + x, by + y) for x, y in _rotate(outline_xy, rotation_deg)]
    bottom = [(x, y, bz) for x, y in reversed(ring)]
    top = [(x, y, bz + height) for x, y in ring]
    sides = []
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        sides.append([(x0, y0, bz), (x1, y1, bz), (x1, y1, bz + height), (x0, y0, bz + height)])
    return [bottom, top, *sides]


def regular_polygon(radius: float, sides: int, phase: float = 0.0) -> List[Tuple[float, float]]:
    return [(radius * math.cos(phase + 2 * math.pi * i / sides), radius * math.sin(phase + 2 * math.pi * i / sides)) for i in range(sides)]


def tube(a: Point, b: Point, radius: float, sides: int = _TUBE_SIDES) -> List[List[Point]]:
    """Prisma regular ao longo de ``a → b``, com as duas tampas."""
    axis = tuple(q - p for p, q in zip(a, b))
    length = math.sqrt(sum(c * c for c in axis))
    if length <= 0:
        return []
    w = tuple(c / length for c in axis)
    helper = (0.0, 0.0, 1.0) if abs(w[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = _normalize(_cross(w, helper))
    v = _cross(w, u)
    ring_a, ring_b = [], []
    for i in range(sides):
        ang = 2 * math.pi * i / sides + math.pi / sides
        off = tuple(radius * (math.cos(ang) * uu + math.sin(ang) * vv) for uu, vv in zip(u, v))
        ring_a.append(tuple(p + o for p, o in zip(a, off)))
        ring_b.append(tuple(p + o for p, o in zip(b, off)))
    faces = [list(reversed(ring_a)), list(ring_b)]
    for i in range(sides):
        j = (i + 1) % sides
        faces.append([ring_a[i], ring_a[j], ring_b[j], ring_b[i]])
    return faces  # type: ignore[return-value]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _normalize(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


def face_normal(face: Sequence[Point]) -> Point:
    """Normal de Newell: estável para polígonos planos com vértices colineares."""
    nx = ny = nz = 0.0
    for (x0, y0, z0), (x1, y1, z1) in zip(face, list(face[1:]) + [face[0]]):
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return _normalize((nx, ny, nz))  # type: ignore[return-value]


# ── Dimensionamento dos sólidos ──────────────────────────────────────────────

def tank_dimensions_mm(type_id: str, parameters: Dict[str, Any], fallback_volume_l: float) -> Tuple[float, float, float, bool]:
    """Diâmetro, altura, capacidade e se as dimensões foram estimadas.

    Com ``DIAMETRO_MM`` e ``ALTURA_MM`` informados, valem eles. Sem eles, o
    cilindro com a capacidade (do componente ou, na falta, a calculada pelo
    Netuno) e a proporção típica do tipo: V = π·D²/4·H, H = k·D.
    """
    capacity = _number(parameters.get("CAPACIDADE_L"), None) or fallback_volume_l
    diameter = _number(parameters.get("DIAMETRO_MM"), None)
    height = _number(parameters.get("ALTURA_MM"), None)
    if diameter and height:
        return diameter, height, capacity, False
    ratio = _TANK_HEIGHT_RATIO.get(type_id, 1.0)
    volume_mm3 = max(capacity, 1.0) * 1e6
    if diameter:
        return diameter, volume_mm3 / (math.pi * diameter ** 2 / 4), capacity, True
    if height:
        return math.sqrt(4 * volume_mm3 / (math.pi * height)), height, capacity, True
    diameter = (4 * volume_mm3 / (math.pi * ratio)) ** (1 / 3)
    return diameter, ratio * diameter, capacity, True


def _fmt(value: float, decimals: int = 2) -> str:
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _component_solid(item: Dict[str, Any], project_data: Dict[str, Any]) -> Solid:
    type_id = item["type_id"]
    params = item.get("parameters") or {}
    pos = item["position_mm"]
    base = (pos["x"], pos["y"], pos["z"])
    rotation = item.get("rotation_deg", 0.0)
    name = _TYPE_NAMES.get(type_id, type_id)
    info = [f"Tipo: {name}", f"Base: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível: {item.get('level', '')}"]
    color = _COLORS.get(type_id, (100, 116, 139))

    if type_id in _TANK_HEIGHT_RATIO:
        fallback = _number(project_data.get("lower_vol" if type_id == "cisterna_inferior" else "upper_vol"), 1000.0)
        diameter, height, capacity, estimated = tank_dimensions_mm(type_id, params, fallback)
        faces = prism(regular_polygon(diameter / 2, _TANK_SIDES), base, height)
        info += [f"Capacidade: {_fmt(capacity, 0)} L",
                 f"Ø {_fmt(diameter / 1000)} m × H {_fmt(height / 1000)} m" + (" (estimado pela capacidade)" if estimated else "")]
        return Solid(item["instance_id"], "tank", f"{item['instance_id']} · {name}", info, color, faces,
                     opacity=0.55, outline=True, label_at=(base[0], base[1], base[2] + height))

    if type_id == "motobomba":
        power = _number(params.get("POTENCIA_KW"), None)
        scale = 1.0 if power is None else min(1.8, max(0.8, (power / 0.37) ** (1 / 3)))
        half_long, half_short, height = 300 * scale, 200 * scale, 320 * scale
        faces = prism([(half_long, 0), (0, half_short), (-half_long, 0), (0, -half_short)], base, height, rotation)
        info.append(f"Potência: {_fmt(power)} kW" if power else "Potência: não informada (volume ilustrativo)")
        return Solid(item["instance_id"], "pump", f"{item['instance_id']} · {name}", info, color, faces,
                     outline=True, label_at=(base[0], base[1], base[2] + height))

    dn = _number(params.get("DN_MM"), None)
    if type_id in {"filtro_pluvial", "first_flush"}:
        radius, height = (220.0, 600.0) if type_id == "filtro_pluvial" else (90.0, 900.0)
        faces = prism(regular_polygon(radius, 16), base, height)
    elif type_id == "ponto_nao_potavel":
        radius, height = 110.0, 220.0
        faces = prism(regular_polygon(radius, 4, math.pi / 4), base, height, rotation)
    else:
        side = max(140.0, (dn or 25.0) * 3)
        radius, height = side / 2, side
        faces = prism(regular_polygon(side / math.sqrt(2), 4, math.pi / 4), base, height, rotation)
    if dn:
        info.append(f"DN {dn:g}")
    return Solid(item["instance_id"], "accessory", f"{item['instance_id']} · {name}", info, color, faces,
                 outline=True, label_at=(base[0], base[1], base[2] + height))


def _building_solids(building: Dict[str, Any]) -> List[Solid]:
    width, depth, height = (_number(building.get(k), None) for k in ("width_mm", "depth_mm", "height_mm"))
    if not (width and depth and height):
        return []
    origin = building.get("origin_mm") or {}
    # Origem pode ser negativa ou zero: _number só aceita positivos.
    x0, y0, z0 = (_signed(origin.get(k)) for k in ("x", "y", "z"))
    floors = int(_number(building.get("floors"), 1) or 1)
    rect = [(0, 0), (width, 0), (width, depth), (0, depth)]
    info = [f"{_fmt(width / 1000)} × {_fmt(depth / 1000)} m em planta", f"Altura {_fmt(height / 1000)} m · {floors} pavimento(s)",
            f"Origem: x {_fmt(x0 / 1000)} · y {_fmt(y0 / 1000)} · cota {_fmt(z0 / 1000)} m"]
    solids = [Solid("EDIFICACAO", "building", "Edificação (volumetria)", info, _COLORS["building"],
                    prism(rect, (x0, y0, z0), height), opacity=0.16, outline=True)]
    for floor in range(1, floors):
        z = z0 + height * floor / floors
        slab = [[(x0 + x, y0 + y, z) for x, y in rect]]
        solids.append(Solid(f"LAJE-{floor}", "slab", f"Laje do {floor + 1}º pavimento", [f"Cota {_fmt(z / 1000)} m"],
                            _COLORS["building"], slab, opacity=0.10, outline=True, pickable=False))
    return solids


def _signed(value: Any) -> float:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def _bounds_of(solids: Iterable[Solid]) -> Tuple[Point, Point]:
    pts = [p for s in solids for f in s.faces for p in f]
    if not pts:
        return (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
    xs, ys, zs = zip(*pts)
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def build_volumetry(project_data: Dict[str, Any]) -> Scene:
    """Monta a cena a partir do mesmo manifesto validado que gera DXF e JSON."""
    manifest = _checked_manifest(project_data)
    solids: List[Solid] = []
    solids += _building_solids(project_data.get("building_volume") or {})
    solids += [_component_solid(item, project_data) for item in manifest["instances"]]

    geometry_bounds = _bounds_of(solids) if solids else None
    raw_points = [(v["x"], v["y"], v["z"]) for run in manifest["pipe_runs"] for v in run["vertices_mm"]]
    if geometry_bounds:
        raw_points += list(geometry_bounds)
    xs, ys, zs = zip(*raw_points) if raw_points else ((0.0,), (0.0,), (0.0,))
    diagonal = max(math.dist((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))), 1000.0)
    min_radius = diagonal * _MIN_TUBE_RADIUS_FRACTION

    notes: List[str] = []
    enlarged = False
    for run in manifest["pipe_runs"]:
        system = SYSTEMS_BY_ID[run["system"]]
        color = _hex_to_rgb(system["svg"])
        radius = max(run["dn_mm"] / 2, min_radius)
        enlarged |= radius > run["dn_mm"] / 2
        for index, seg in enumerate(run["segments"], start=1):
            a = (seg["start_mm"]["x"], seg["start_mm"]["y"], seg["start_mm"]["z"])
            b = (seg["end_mm"]["x"], seg["end_mm"]["y"], seg["end_mm"]["z"])
            dz = b[2] - a[2]
            info = [f"Sistema: {system['label']}", f"DN {run['dn_mm']:g} · {run['material']}",
                    f"Segmento {index} de {len(run['segments'])}: {_fmt(seg['length_mm'] / 1000)} m",
                    f"Trecho completo: {_fmt(run['length_mm'] / 1000)} m · ordem {run['sequence']}"]
            if abs(dz) > 0.5:
                info.append(f"Desnível: {'+' if dz > 0 else '−'}{_fmt(abs(dz) / 1000)} m")
            if run["start_ref"] or run["end_ref"]:
                info.append(f"De {run['start_ref'] or 'coordenadas'} para {run['end_ref'] or '—'}")
            solids.append(Solid(f"{run['run_id']}#{index}", "pipe", f"{run['run_id']} · {system['label']}", info,
                                color, tube(a, b, radius), group=run["run_id"], axis=(a, b, radius)))
            if index < len(run["segments"]):
                # Nó na mudança de direção, para a tubulação não parecer quebrada.
                solids.append(Solid(f"{run['run_id']}#{index}n", "pipe", f"{run['run_id']} · {system['label']}", info,
                                    color, prism(regular_polygon(radius * 1.08, _TUBE_SIDES), (b[0], b[1], b[2] - radius * 1.08), radius * 2.16),
                                    pickable=False, group=run["run_id"], axis=(b, b, radius)))
    if enlarged:
        notes.append("Tubos de DN pequeno desenhados com espessura ampliada para visualização.")

    low, high = _bounds_of(solids)
    margin = diagonal * 0.08
    ground = [[(low[0] - margin, low[1] - margin, 0.0), (high[0] + margin, low[1] - margin, 0.0),
               (high[0] + margin, high[1] + margin, 0.0), (low[0] - margin, high[1] + margin, 0.0)]]
    solids.insert(0, Solid("TERRENO", "ground", "Terreno (cota 0,00)", [], _COLORS["ground"], ground,
                           opacity=0.22, outline=True, pickable=False))
    if any(s.info and "estimado" in " ".join(s.info) for s in solids):
        notes.append("Reservatórios sem Ø e altura informados: dimensões estimadas pela capacidade.")
    return Scene(str(manifest["project"]["name"]), solids, _bounds_of(solids), notes)


def _hex_to_rgb(value: str) -> Color:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
