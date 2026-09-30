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
regras explícitas (ver :mod:`netuno.core.component_geometry`) e marcadas como estimadas na
ficha do sólido, nunca apresentadas como medida de projeto.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .component_geometry import TANK_HEIGHT_RATIO, component_envelope, fallback_volumes, regular_polygon
from .component_geometry import tank_dimensions_mm  # noqa: F401  (reexportado: parte da API da volumetria)
from .pipe_network import SYSTEMS_BY_ID, junction_point, segment_distance
from .plant_3d import _checked_manifest

Point = Tuple[float, float, float]
Color = Tuple[int, int, int]

_TUBE_SIDES = 8
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
    # Para o visualizador WebGL desenhar a peça detalhada no lugar do prisma:
    # o tipo do catálogo, o giro em planta e o sistema hidráulico do tubo.
    type_id: str = ""
    rotation_deg: float = 0.0
    system: str = ""
    dn_mm: float = 0.0  # diâmetro nominal real do tubo (o prisma pode estar ampliado)


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

def _fmt(value: float, decimals: int = 2) -> str:
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _component_solid(item: Dict[str, Any], project_data: Dict[str, Any]) -> Solid:
    solid = _component_solid_body(item, project_data)
    solid.type_id = item["type_id"]
    env = component_envelope(item, fallback_volumes(project_data))
    solid.rotation_deg = 0.0 if env.shape == "cylinder" else float(item.get("rotation_deg", 0.0) or 0.0)
    return solid


def _component_solid_body(item: Dict[str, Any], project_data: Dict[str, Any]) -> Solid:
    type_id = item["type_id"]
    params = item.get("parameters") or {}
    pos = item["position_mm"]
    base = (pos["x"], pos["y"], pos["z"])
    name = _TYPE_NAMES.get(type_id, type_id)
    color = _COLORS.get(type_id, (100, 116, 139))
    env = component_envelope(item, fallback_volumes(project_data))
    # Tanques e cilindros não giram: a planta circular é a mesma em qualquer ângulo.
    rotation = 0.0 if env.shape == "cylinder" else item.get("rotation_deg", 0.0)
    faces = prism(env.outline, base, env.height, rotation)
    label_at = (base[0], base[1], base[2] + env.height)
    level = item.get("level") or "Térreo"
    inst = item["instance_id"]

    if type_id == "motobomba":
        kw = _number(params.get("POTENCIA_KW"), None) or _number(project_data.get("pump_power_kw"), 0.37) or 0.37
        cv = _number(params.get("POTENCIA_CV"), None) or (kw / 0.735499 if kw else 0.50)
        hp_label = str(params.get("POTENCIA_HP_LABEL") or project_data.get("pump_hp") or "")
        if not hp_label or hp_label in ("None", "0.0"):
            if 0.35 <= cv <= 0.55:
                hp_label = "1/2"
            elif 0.70 <= cv <= 0.85:
                hp_label = "3/4"
            elif 0.90 <= cv <= 1.15:
                hp_label = "1"
            elif 0.20 <= cv <= 0.34:
                hp_label = "1/3"
            else:
                hp_label = f"{cv:.2f}"

        flow_l_min = _number(params.get("VAZAO_L_MIN"), None) or (_number(project_data.get("pump_flow_rate_m3_h"), 3.6) * 1000.0 / 60.0)
        flow_m3_h = _number(params.get("VAZAO_M3_H"), None) or (flow_l_min * 60.0 / 1000.0)
        head_mca = _number(params.get("ALTURA_MCA"), 12.0) or 12.0
        dn_suc = _number(params.get("DN_SUCCAO_MM"), 32.0) or 32.0
        dn_rec = _number(params.get("DN_RECALQUE_MM"), 25.0) or 25.0
        vol_dia = _number(project_data.get("pluv_day"), 800.0) or 800.0
        tempo_min = (vol_dia / max(flow_l_min, 1.0)) if vol_dia > 0 else 0.0

        info = [
            "Tipo: Conjunto Motobomba Centrífuga de Recalque",
            f"Potência nominal: {_fmt(kw, 2)} kW ({_fmt(cv, 2)} CV / {hp_label} HP)",
            f"Vazão de operação: {_fmt(flow_l_min, 1)} L/min ({_fmt(flow_m3_h, 2)} m³/h)",
            f"Altura manométrica total: {_fmt(head_mca, 1)} mca",
            f"Tubulação de sucção: DN {dn_suc:g} mm (econômico Forchheimer)",
            f"Tubulação de recalque: DN {dn_rec:g} mm (econômico Forchheimer)",
            f"Demanda diária bombeada: {_fmt(vol_dia, 0)} L/dia",
            f"Tempo estimado de operação: ~{tempo_min:.0f} min/dia",
            "Alimentação elétrica: Monofásico 220 V / 60 Hz",
            "Comando e controle: Chaves boia de nível elétricas contra marcha a seco",
            f"Posição: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível de instalação: {level}",
            "Normas de referência: ABNT NBR 5626:2020 e ABNT NBR 15527:2019",
        ]
        return Solid(inst, "pump", f"{inst} · Motobomba ({hp_label} HP / {_fmt(kw, 2)} kW)", info, color, faces,
                     outline=True, label_at=label_at)

    if type_id == "filtro_pluvial":
        dn = _number(params.get("DN_MM"), 100.0) or 100.0
        malha = _number(params.get("MALHA_MM"), 0.35) or 0.35
        efic = _number(params.get("EFICIENCIA_PCT"), 90.0) or 90.0
        tipo_str = str(params.get("TIPO") or "Filtro Pluvial Autolimpante Vórtex")
        info = [
            f"Tipo: {tipo_str}",
            f"Bitola de conexão: DN {dn:g} mm",
            f"Malha filtrante: {_fmt(malha, 2)} mm ({int(malha * 1000)} µm) em Aço Inox AISI 304",
            f"Eficiência hidráulica: {_fmt(efic, 0)}% de retenção e recuperação",
            "Sólidos retidos: Folhas, galhos, musgo e detritos grosseiros",
            "Operação: Autolimpante contínuo por arraste durante o fluxo pluvial",
            f"Dimensões do corpo: Ø {_fmt(env.half_x * 2 / 1000)} m × Altura {_fmt(env.height / 1000)} m",
            f"Posição: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível de instalação: {level}",
            "Norma de referência: ABNT NBR 15527:2019 item 4.3.4",
        ]
        return Solid(inst, "filter", f"{inst} · Filtro Pluvial Autolimpante (DN {dn:g})", info, color, faces,
                     opacity=0.85, outline=True, label_at=label_at)

    if type_id == "first_flush":
        vol_desc = _number(params.get("VOLUME_L"), None) or (env.capacity_l if env.capacity_l else 300.0)
        lamina = _number(params.get("DESCARTE_MM"), None) or _number(project_data.get("discard"), 2.0) or 2.0
        area = _number(project_data.get("area"), 150.0) or 150.0
        mecanismo = str(params.get("MECANISMO") or "Boia flutuante de vedação por esfera e válvula de purga lenta calibrada")
        info = [
            "Tipo: Dispositivo de Descarte de Escoamento Inicial (First Flush)",
            f"Volume de descarte calculado: {_fmt(vol_desc, 0)} L ({_fmt(vol_desc / 1000, 2)} m³)",
            f"Lâmina de descarte: {_fmt(lamina, 1)} mm (conforme ABNT NBR 15527:2019 item 4.3.5)",
            f"Área de captação contribuinte: {_fmt(area, 0)} m²",
            f"Dimensões do reservatório: Ø {_fmt(env.half_x * 2 / 1000)} m × Altura {_fmt(env.height / 1000)} m",
            f"Mecanismo de funcionamento: {mecanismo}",
            "Tempo de esvaziamento: Purga automática lenta em 24 a 48 horas de tempo seco",
            "Poluentes descartados: Poeira acumulada no telhado, fuligem e fezes de aves lavadas da cobertura",
            f"Posição: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível de instalação: {level}",
            "Norma de referência: ABNT NBR 15527:2019 item 4.3.5",
        ]
        return Solid(inst, "tank", f"{inst} · Descarte Inicial ({_fmt(vol_desc, 0)} L)", info, color, faces,
                     opacity=0.80, outline=True, label_at=label_at)

    if type_id == "cisterna_inferior":
        cap = env.capacity_l or _number(params.get("CAPACIDADE_L"), 5000.0) or 5000.0
        diam = env.diameter or _number(params.get("DIAMETRO_MM"), 1850.0) or 1850.0
        alt = env.height or _number(params.get("ALTURA_MM"), 1850.0) or 1850.0
        mat = str(params.get("MATERIAL") or "Polietileno de Alta Densidade (PEAD) com proteção UV")
        info = [
            "Tipo: Cisterna de Armazenamento Inferior (Água Pluvial)",
            f"Capacidade: {_fmt(cap, 0)} L ({_fmt(cap / 1000, 2)} m³)",
            f"Dimensões físicas: Ø {_fmt(diam / 1000)} m × Altura {_fmt(alt / 1000)} m" + (" (estimado pela capacidade)" if env.estimated else ""),
            f"Material construtivo: {mat}",
            f"Instalação: Enterrada no recuo técnico (cota de fundo: {_fmt(base[2] / 1000)} m)",
            "Dispositivos hidráulicos integrados:",
            " • Entrada: Tubo defletor calmo (freio d'água contra ressuspensão de sedimentos)",
            " • Sucção: Mangueira flexível com captação flutuante a 15 cm da superfície",
            " • Extravasor: Sifão ladrão com tela anti-inseto e proteção anti-refluxo",
            " • Tampa: Inspeção estanque com vedação contra luz solar e proliferação de algas",
            f"Posição da base: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível de instalação: {level}",
            "Norma de referência: ABNT NBR 15527:2019 item 4.4",
        ]
        return Solid(inst, "tank", f"{inst} · Cisterna Inferior ({_fmt(cap, 0)} L)", info, color, faces,
                     opacity=0.55, outline=True, label_at=label_at)

    if type_id == "reservatorio_superior":
        cap = env.capacity_l or _number(params.get("CAPACIDADE_L"), 1000.0) or 1000.0
        diam = env.diameter or _number(params.get("DIAMETRO_MM"), 1300.0) or 1300.0
        alt = env.height or _number(params.get("ALTURA_MM"), 750.0) or 750.0
        mat = str(params.get("MATERIAL") or "Polietileno de Alta Densidade (PEAD)")
        info = [
            "Tipo: Reservatório Superior de Não Potável (Barrilete)",
            f"Capacidade: {_fmt(cap, 0)} L ({_fmt(cap / 1000, 2)} m³)",
            f"Dimensões físicas: Ø {_fmt(diam / 1000)} m × Altura {_fmt(alt / 1000)} m" + (" (estimado pela capacidade)" if env.estimated else ""),
            f"Material construtivo: {mat}",
            "Instalação: Barrilete sobre a laje superior de cobertura (distribuição por gravidade)",
            "Dispositivos hidráulicos integrados:",
            " • Recalque: Entrada superior pelo topo com boia elétrica de comando da bomba",
            " • Backup potável: Alimentação da rede pública com Air Gap normativo (NBR 5626)",
            " • Distribuição: Saída inferior para barrilete de bacias sanitárias, rega e lavagem",
            " • Extravasor: Tubo de aviso e extravasor de emergência independentes",
            f"Posição da base: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
            f"Nível de instalação: {level}",
            "Normas de referência: ABNT NBR 15527:2019 e ABNT NBR 5626:2020",
        ]
        return Solid(inst, "tank", f"{inst} · Caixa Superior ({_fmt(cap, 0)} L)", info, color, faces,
                     opacity=0.55, outline=True, label_at=label_at)

    dn = _number(params.get("DN_MM"), None)
    info = [
        f"Tipo: {name}",
        f"Posição: x {_fmt(base[0] / 1000)} · y {_fmt(base[1] / 1000)} · cota {_fmt(base[2] / 1000)} m",
        f"Nível de instalação: {level}",
    ]
    if dn:
        info.append(f"Bitola nominal: DN {dn:g} mm")
    return Solid(inst, "accessory", f"{inst} · {name}", info, color, faces,
                 outline=True, label_at=label_at)


def _building_solids(building: Dict[str, Any]) -> List[Solid]:
    width, depth, height = (_number(building.get(k), None) for k in ("width_mm", "depth_mm", "height_mm"))
    if not (width and depth and height):
        return []
    origin = building.get("origin_mm") or {}
    # Origem pode ser negativa ou zero: _number só aceita positivos.
    x0, y0, z0 = (_signed(origin.get(k)) for k in ("x", "y", "z"))
    floors = int(_number(building.get("floors"), 1) or 1)
    rect = [(0, 0), (width, 0), (width, depth), (0, depth)]
    area_proj = width * depth / 1e6
    info = [
        f"Dimensões em planta: {_fmt(width / 1000)} × {_fmt(depth / 1000)} m",
        f"Área de projeção/cobertura: {_fmt(area_proj, 0)} m²",
        f"Altura total: {_fmt(height / 1000)} m ({floors} pavimento(s))",
        f"Pé-direito médio: {_fmt(height / (floors * 1000), 2)} m",
        "Coeficiente de escoamento (runoff): C = 0,85 (ABNT NBR 15527:2019)",
        f"Origem do canto: x {_fmt(x0 / 1000)} · y {_fmt(y0 / 1000)} · cota {_fmt(z0 / 1000)} m",
    ]
    solids = [Solid("EDIFICACAO", "building", "Edificação (volumetria)", info, _COLORS["building"],
                    prism(rect, (x0, y0, z0), height), opacity=0.16, outline=True)]
    for floor in range(1, floors):
        z = z0 + height * floor / floors
        slab = [[(x0 + x, y0 + y, z) for x, y in rect]]
        solids.append(Solid(f"LAJE-{floor}", "slab", f"Laje do {floor + 1}º pavimento",
                            [f"Cota de piso: {_fmt(z / 1000)} m", f"Área da laje: {_fmt(area_proj, 0)} m²"],
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
    clearance = _clearances(manifest["pipe_runs"], 4 * min_radius)
    for run in manifest["pipe_runs"]:
        system = SYSTEMS_BY_ID[run["system"]]
        color = _hex_to_rgb(system["svg"])
        # A espessura de visualização nunca encosta um tubo no vizinho: dois tubos
        # distintos precisam continuar parecendo dois tubos.
        radius = max(run["dn_mm"] / 2, min(min_radius, 0.45 * clearance.get(run["run_id"], math.inf)))
        enlarged |= radius > run["dn_mm"] / 2
        dn_val = run["dn_mm"]
        polegada = {20: '1/2"', 25: '3/4"', 32: '1"', 40: '1.1/4"', 50: '1.1/2"', 75: '2.1/2"', 100: '4"', 150: '6"'}.get(int(round(dn_val)), "")
        pol_txt = f" ({polegada})" if polegada else ""
        regime = "Gravitário por conduto livre" if system.get("gravity") else "Pressurizado por bombeamento"
        for index, seg in enumerate(run["segments"], start=1):
            a = (seg["start_mm"]["x"], seg["start_mm"]["y"], seg["start_mm"]["z"])
            b = (seg["end_mm"]["x"], seg["end_mm"]["y"], seg["end_mm"]["z"])
            dz = b[2] - a[2]
            seg_len = seg["length_mm"]
            info = [
                f"Sistema: {system['label']}",
                f"Diâmetro nominal: DN {dn_val:g} mm{pol_txt}",
                f"Material da tubulação: {run['material']}",
                f"Regime hidráulico: {regime}",
                f"Segmento {index} de {len(run['segments'])}: {_fmt(seg_len / 1000)} m",
                f"Extensão do trecho: {_fmt(run['length_mm'] / 1000)} m (ordem {run['sequence']})",
            ]
            if abs(dz) > 0.5:
                decliv = (abs(dz) / max(seg_len, 1.0)) * 100.0
                info.append(f"Desnível do segmento: {'+' if dz > 0 else '−'}{_fmt(abs(dz) / 1000)} m (declividade: {_fmt(decliv, 1)}%)")
            if run["start_ref"] or run["end_ref"]:
                info.append(f"Interligação: De {run['start_ref'] or 'coordenadas'} para {run['end_ref'] or 'extremidade livre'}")
            solids.append(Solid(f"{run['run_id']}#{index}", "pipe", f"{run['run_id']} · {system['label']} (DN {dn_val:g})", info,
                                color, tube(a, b, radius), group=run["run_id"], axis=(a, b, radius),
                                system=run["system"], dn_mm=dn_val))
            if index < len(run["segments"]):
                # Nó na mudança de direção, para a tubulação não parecer quebrada.
                solids.append(Solid(f"{run['run_id']}#{index}n", "pipe", f"{run['run_id']} · {system['label']}", info,
                                    color, prism(regular_polygon(radius * 1.08, _TUBE_SIDES), (b[0], b[1], b[2] - radius * 1.08), radius * 2.16),
                                    pickable=False, group=run["run_id"], axis=(b, b, radius), system=run["system"],
                                    dn_mm=dn_val))
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


def _clearances(runs: Sequence[Dict[str, Any]], horizon: float) -> Dict[str, float]:
    """Menor distância entre eixos de cada trecho e os de outros trechos.

    Ignora os pares que se encontram de propósito (junções). Só olha até
    ``horizon``: além disso, a ampliação não alcança o vizinho.
    """
    segs = [(run["run_id"], _xyz_tuple(seg["start_mm"]), _xyz_tuple(seg["end_mm"])) for run in runs for seg in run["segments"]]
    nearest: Dict[str, float] = {}
    for i, (ra, a0, a1) in enumerate(segs):
        for rb, b0, b1 in segs[i + 1:]:
            if ra == rb or any(min(a0[k], a1[k]) - horizon > max(b0[k], b1[k]) or
                               min(b0[k], b1[k]) - horizon > max(a0[k], a1[k]) for k in range(3)):
                continue
            if junction_point(a0, a1, b0, b1) is not None:
                continue
            distance, _ = segment_distance(a0, a1, b0, b1)
            for key in (ra, rb):
                nearest[key] = min(nearest.get(key, math.inf), distance)
    return nearest


def _xyz_tuple(p: Dict[str, float]) -> Point:
    return (p["x"], p["y"], p["z"])


def _hex_to_rgb(value: str) -> Color:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
