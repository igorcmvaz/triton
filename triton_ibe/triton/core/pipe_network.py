"""Trechos de tubulação organizados pelo projetista e resolvidos em sequência.

O Triton não traça tubulação sozinho: posição de parede, forro, shaft e
interferências são decisões de projeto. O que ele faz é aceitar os trechos na
ordem em que o projetista os organiza e resolver cada um a partir do ponto em que
o anterior terminou, como quem desenha à mão. Assim o projetista descreve o
percurso por direções e comprimentos ("+x 3000; desce 1200") em vez de digitar
coordenadas absolutas de cada vértice.

Convenções:

* coordenadas locais em milímetros, eixo ``z`` para cima;
* a lista ``pipe_runs`` é a sequência: a ordem dela é a ordem de montagem;
* a origem de um trecho pode ser um componente (``"CI-01"``), o fim de um trecho
  anterior (``"T-01"``), coordenadas explícitas ou, se omitida, o fim do trecho
  imediatamente anterior;
* origem e destino num componente aceitam um ponto de conexão após ``:``
  (``RS-01:topo``, ``RS-01:inf+x``; ver :mod:`triton.core.component_geometry`);
* o destino, quando informado, é conferido, nunca completado: um trecho que não
  chega ao componente declarado é um erro, não um segmento inventado;
* dois tubos não ocupam o mesmo espaço: sobreposição, cruzamento ou saída
  quase paralela do mesmo ponto é erro de interferência (:func:`find_clashes`).
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from .component_geometry import port_position, split_reference


Point = Tuple[float, float, float]

# Tolerância de coincidência entre o fim do percurso e o destino declarado.
CONNECTION_TOLERANCE_MM = 1.0
# Declividade mínima de trechos horizontais por gravidade (ABNT NBR 10844: 0,5 %).
MIN_GRAVITY_SLOPE = 0.005


PIPE_SYSTEMS: List[Dict[str, Any]] = [
    {"system_id": "captacao", "label": "Captação pluvial", "gravity": True, "layer": "NETUNO_3D_CAPTACAO", "color": 5, "svg": "#2563eb"},
    {"system_id": "descarte", "label": "Descarte (first flush)", "gravity": True, "layer": "NETUNO_3D_DESCARTE", "color": 30, "svg": "#b45309"},
    {"system_id": "extravasor", "label": "Extravasor", "gravity": True, "layer": "NETUNO_3D_EXTRAVASOR", "color": 8, "svg": "#64748b"},
    {"system_id": "succao", "label": "Sucção", "gravity": False, "layer": "NETUNO_3D_SUCCAO", "color": 4, "svg": "#0891b2"},
    {"system_id": "recalque", "label": "Recalque", "gravity": False, "layer": "NETUNO_3D_RECALQUE", "color": 1, "svg": "#dc2626"},
    {"system_id": "distribuicao", "label": "Distribuição não potável", "gravity": False, "layer": "NETUNO_3D_DISTRIBUICAO", "color": 6, "svg": "#9333ea"},
    {"system_id": "alimentacao_potavel", "label": "Alimentação potável (backup)", "gravity": False, "layer": "NETUNO_3D_POTAVEL", "color": 3, "svg": "#16a34a"},
]
SYSTEMS_BY_ID = {item["system_id"]: item for item in PIPE_SYSTEMS}

_AXES = {
    "+x": (1.0, 0.0, 0.0), "-x": (-1.0, 0.0, 0.0),
    "+y": (0.0, 1.0, 0.0), "-y": (0.0, -1.0, 0.0),
    "+z": (0.0, 0.0, 1.0), "-z": (0.0, 0.0, -1.0),
    "leste": (1.0, 0.0, 0.0), "oeste": (-1.0, 0.0, 0.0),
    "norte": (0.0, 1.0, 0.0), "sul": (0.0, -1.0, 0.0),
    "sobe": (0.0, 0.0, 1.0), "desce": (0.0, 0.0, -1.0),
}
_AXES.update({"x": _AXES["+x"], "y": _AXES["+y"], "z": _AXES["+z"]})


def _number(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def parse_route(route: Any) -> List[Point]:
    """Converte um percurso em deslocamentos (dx, dy, dz) em mm.

    Aceita uma lista de dicionários ou texto com passos separados por ``;``:

    * ``+x 3000`` / ``-y 1500`` / ``sobe 1200`` / ``desce 800`` / ``norte 500``;
    * ``d 3000 0 -15`` — deslocamento livre, útil para trechos com declividade.

    No texto, os números usam ponto como separador decimal; vírgula é aceita
    apenas no formato de dicionário.
    """
    if route is None or route == "":
        return []
    if isinstance(route, str):
        steps: List[Any] = [step for step in re.split(r"[;\n]+", route) if step.strip()]
    else:
        steps = list(route)

    deltas: List[Point] = []
    for index, step in enumerate(steps, start=1):
        if isinstance(step, dict):
            if "direction" in step:
                deltas.append(_axis_step(str(step["direction"]), step.get("length_mm"), index))
            else:
                values = [_number(step.get(key), None) for key in ("dx", "dy", "dz")]
                if any(v is None for v in values):
                    raise ValueError(f"Passo {index}: informe dx, dy e dz em mm.")
                deltas.append((values[0], values[1], values[2]))  # type: ignore[arg-type]
            continue
        tokens = str(step).strip().lower().split()
        if tokens and tokens[0] in {"d", "delta"}:
            values = [_number(token, None) for token in tokens[1:]]
            if len(values) != 3 or any(v is None for v in values):
                raise ValueError(f"Passo {index} ('{step.strip()}'): use 'd dx dy dz' em mm.")
            deltas.append((values[0], values[1], values[2]))  # type: ignore[arg-type]
        elif len(tokens) == 2:
            deltas.append(_axis_step(tokens[0], tokens[1], index))
        else:
            raise ValueError(f"Passo {index} ('{str(step).strip()}'): use '+x 3000', 'desce 1200' ou 'd dx dy dz'.")
    return deltas


def _axis_step(direction: str, length: Any, index: int) -> Point:
    axis = _AXES.get(direction.strip().lower())
    if axis is None:
        raise ValueError(f"Passo {index}: direção '{direction}' desconhecida (use ±x, ±y, ±z, sobe, desce, norte, sul, leste, oeste).")
    size = _number(length, None)
    if size is None or size <= 0:
        raise ValueError(f"Passo {index}: comprimento deve ser positivo, em mm.")
    return (axis[0] * size, axis[1] * size, axis[2] * size)


def format_route(deltas: Sequence[Point]) -> str:
    """Inverso de :func:`parse_route`, para exibir o percurso ao projetista."""
    parts = []
    for dx, dy, dz in deltas:
        nonzero = [(axis, value) for axis, value in (("x", dx), ("y", dy), ("z", dz)) if abs(value) > 1e-9]
        if len(nonzero) == 1:
            axis, value = nonzero[0]
            parts.append(f"{'+' if value > 0 else '-'}{axis} {_compact(abs(value))}")
        else:
            parts.append(f"d {_compact(dx)} {_compact(dy)} {_compact(dz)}")
    return "; ".join(parts)


def _compact(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".") or "0"


def _as_point(raw: Any) -> Optional[Point]:
    if not isinstance(raw, dict) or not {"x", "y", "z"} <= set(raw):
        return None
    values = [_number(raw.get(key), None) for key in ("x", "y", "z")]
    if any(v is None for v in values):
        return None
    return (values[0], values[1], values[2])  # type: ignore[return-value]


def _reference(raw: Any) -> Optional[str]:
    if isinstance(raw, dict):
        raw = raw.get("instance_id") or raw.get("run_id")
    text = str(raw).strip() if raw is not None else ""
    return text or None


def _distance(a: Point, b: Point) -> float:
    return math.dist(a, b)


def resolve_pipe_network(
    instances: Iterable[Dict[str, Any]],
    pipe_runs: Iterable[Dict[str, Any]],
    fallbacks: Optional[Dict[str, float]] = None,
) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
    """Resolve os trechos na ordem dada e devolve ``(trechos, erros, avisos)``.

    ``instances`` são as instâncias já normalizadas do manifesto BIM (com
    ``position_mm``). Um trecho com erro não é resolvido, e os trechos que
    dependem dele também não, porque não teriam de onde partir.
    ``fallbacks`` são os volumes calculados, usados para dimensionar os
    reservatórios sem medidas quando um trecho usa os seus pontos de conexão.
    Depois de resolvidos, os trechos passam pela verificação de interferência.
    """
    items = {str(item["instance_id"]): item for item in instances}
    anchors: Dict[str, Point] = {}
    for key, item in items.items():
        pos = item.get("position_mm") or {}
        anchors[key] = (float(pos["x"]), float(pos["y"]), float(pos["z"]))

    def anchor(reference: str) -> Tuple[Optional[Point], Optional[str]]:
        """Ponto de um componente (com porta opcional) ou ``(None, motivo)``."""
        name, port = split_reference(reference)
        if name not in items:
            return None, None
        try:
            return port_position(items[name], port, fallbacks), None
        except ValueError as exc:
            return None, str(exc)

    resolved: List[Dict[str, Any]] = []
    errors: List[str] = []
    warnings: List[str] = []
    run_ends: Dict[str, Optional[Point]] = {}
    previous_end: Optional[Point] = None
    previous_id: Optional[str] = None

    for sequence, raw in enumerate(pipe_runs, start=1):
        run_id = str(raw.get("run_id") or f"T-{sequence:02d}").strip()
        label = f"Trecho {run_id}"
        if run_id in run_ends or run_id in anchors:
            errors.append(f"{label}: identificador repetido ou igual ao de um componente.")
            previous_end, previous_id = None, run_id
            continue

        failed = False
        system = str(raw.get("system") or "").strip()
        if system not in SYSTEMS_BY_ID:
            errors.append(f"{label}: sistema '{system or '<vazio>'}' desconhecido.")
            failed = True
        dn = _number(raw.get("dn_mm"), None)
        if dn is None or dn <= 0:
            errors.append(f"{label}: DN deve ser positivo, em mm.")
            failed = True
        try:
            deltas = parse_route(raw.get("route"))
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            deltas, failed = [], True
        if not failed and not deltas:
            errors.append(f"{label}: percurso vazio.")
            failed = True

        start_raw = raw.get("start")
        start_point = _as_point(start_raw)
        start_ref = None if start_point else _reference(start_raw)
        if start_point is None:
            if start_ref is None:
                if previous_id is None:
                    errors.append(f"{label}: o primeiro trecho precisa de origem (componente ou coordenadas).")
                    failed = True
                else:
                    start_ref = previous_id
                    start_point = previous_end
                    if start_point is None:
                        errors.append(f"{label}: continua o trecho {previous_id}, que não foi resolvido.")
                        failed = True
            elif split_reference(start_ref)[0] in anchors:
                start_point, problem = anchor(start_ref)
                if start_point is None:
                    errors.append(f"{label}: origem {start_ref}: {problem}.")
                    failed = True
            elif start_ref in run_ends:
                start_point = run_ends[start_ref]
                if start_point is None:
                    errors.append(f"{label}: parte do trecho {start_ref}, que não foi resolvido.")
                    failed = True
            else:
                errors.append(f"{label}: origem '{start_ref}' não é componente nem trecho anterior.")
                failed = True

        if failed or start_point is None:
            run_ends[run_id] = None
            previous_end, previous_id = None, run_id
            continue

        vertices: List[Point] = [start_point]
        for dx, dy, dz in deltas:
            x, y, z = vertices[-1]
            vertices.append((x + dx, y + dy, z + dz))

        segments = []
        for index, (a, b) in enumerate(zip(vertices, vertices[1:]), start=1):
            length = _distance(a, b)
            if length < CONNECTION_TOLERANCE_MM:
                errors.append(f"{label}: segmento {index} com comprimento nulo.")
                failed = True
            segments.append({"start_mm": _xyz(a), "end_mm": _xyz(b), "length_mm": round(length, 3)})

        end_ref = _reference(raw.get("end"))
        if end_ref is not None:
            target, problem = anchor(end_ref)
            if target is None:
                errors.append(f"{label}: destino {end_ref}: {problem}." if problem
                              else f"{label}: destino '{end_ref}' não é um componente posicionado.")
                failed = True
            else:
                gap = _distance(vertices[-1], target)
                if gap > CONNECTION_TOLERANCE_MM:
                    dx, dy, dz = (t - v for t, v in zip(target, vertices[-1]))
                    errors.append(
                        f"{label}: termina a {gap:.0f} mm de {end_ref}; falta 'd {_compact(dx)} {_compact(dy)} {_compact(dz)}'."
                    )
                    failed = True

        if failed:
            run_ends[run_id] = None
            previous_end, previous_id = None, run_id
            continue

        if SYSTEMS_BY_ID[system]["gravity"]:
            warnings.extend(_gravity_warnings(label, segments))

        total = sum(seg["length_mm"] for seg in segments)
        resolved.append({
            "run_id": run_id,
            "sequence": sequence,
            "system": system,
            "dn_mm": dn,
            "material": str(raw.get("material") or "PVC"),
            "level": str(raw.get("level") or "Nível 0"),
            "start_ref": start_ref,
            "end_ref": end_ref,
            "route": format_route(deltas),
            "vertices_mm": [_xyz(v) for v in vertices],
            "segments": segments,
            "length_mm": round(total, 3),
        })
        run_ends[run_id] = vertices[-1]
        previous_end, previous_id = vertices[-1], run_id

    errors.extend(find_clashes(resolved, anchors))
    return resolved, errors, warnings


# ── Interferência entre tubos ────────────────────────────────────────────────

# Numa junção (fim de um segmento sobre outro), o contato natural vai até 2·d
# no tubo que passa (tê a 90°). Acima de 2,5·d, os tubos seguem juntos: é
# sobreposição, ou saída do mesmo ponto com menos de ~24° entre eles.
_JUNCTION_ALLOWANCE = 2.5


def _vec(p: Dict[str, float]) -> Tuple[float, float, float]:
    return (p["x"], p["y"], p["z"])


def _point_segment_distance(p, a, b) -> float:
    ab = [bb - aa for aa, bb in zip(a, b)]
    denom = sum(c * c for c in ab)
    t = 0.0 if denom == 0 else max(0.0, min(1.0, sum((pp - aa) * c for pp, aa, c in zip(p, a, ab)) / denom))
    return math.dist(p, [aa + t * c for aa, c in zip(a, ab)])


def segment_distance(a0, a1, b0, b1) -> Tuple[float, float]:
    """Menor distância entre dois segmentos e o parâmetro ``t`` em ``a0→a1``."""
    d1 = [q - p for p, q in zip(a0, a1)]
    d2 = [q - p for p, q in zip(b0, b1)]
    r = [p - q for p, q in zip(a0, b0)]
    a, e, f = sum(c * c for c in d1), sum(c * c for c in d2), sum(x * y for x, y in zip(d2, r))
    if a <= 1e-12 and e <= 1e-12:
        return math.dist(a0, b0), 0.0
    if a <= 1e-12:
        s, t = 0.0, max(0.0, min(1.0, f / e))
    else:
        c = sum(x * y for x, y in zip(d1, r))
        if e <= 1e-12:
            t, s = 0.0, max(0.0, min(1.0, -c / a))
        else:
            b = sum(x * y for x, y in zip(d1, d2))
            denom = a * e - b * b
            s = max(0.0, min(1.0, (b * f - c * e) / denom)) if denom > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0:
                t, s = 0.0, max(0.0, min(1.0, -c / a))
            elif t > 1:
                t, s = 1.0, max(0.0, min(1.0, (b - c) / a))
    pa = [p + s * q for p, q in zip(a0, d1)]
    pb = [p + t * q for p, q in zip(b0, d2)]
    return math.dist(pa, pb), s


def _contact_interval(a0, a1, b0, b1, limit: float, s_star: float) -> Tuple[float, float]:
    """Trecho de ``a0→a1`` a menos de ``limit`` do outro segmento.

    A distância de um ponto de A até o segmento B é convexa ao longo de A, então
    o conjunto é um intervalo em torno do ponto mais próximo: basta bisseção.
    """
    def dist(t):
        return _point_segment_distance([p + t * (q - p) for p, q in zip(a0, a1)], b0, b1)

    def edge(inside, outside):
        if dist(outside) <= limit:
            return outside
        for _ in range(40):
            mid = (inside + outside) / 2
            inside, outside = (mid, outside) if dist(mid) <= limit else (inside, mid)
        return inside

    return edge(s_star, 0.0), edge(s_star, 1.0)


def find_clashes(resolved_runs: Sequence[Dict[str, Any]], anchors: Optional[Dict[str, Point]] = None) -> List[str]:
    """Pares de tubos que ocupam o mesmo espaço, com local e extensão.

    Dois segmentos colidem quando os eixos ficam mais próximos que a soma dos
    raios (DN/2). Onde eles se encontram de propósito — continuação, curva, tê —
    o contato perto da junção é aceito; além disso, é sobreposição.
    """
    segs = []
    for run in resolved_runs:
        for index, seg in enumerate(run["segments"], start=1):
            a, b = _vec(seg["start_mm"]), _vec(seg["end_mm"])
            segs.append((run, index, a, b, run["dn_mm"] / 2))
    names = {tuple(round(c, 3) for c in point): name for name, point in (anchors or {}).items()}
    messages: List[str] = []
    reported = set()
    for i in range(len(segs)):
        run_a, ia, a0, a1, ra = segs[i]
        for j in range(i + 1, len(segs)):
            run_b, ib, b0, b1, rb = segs[j]
            if run_a is run_b and abs(ia - ib) == 1 and _straight_turn(a0, a1, b0, b1):
                continue  # curva comum dentro do próprio trecho
            limit = ra + rb - 0.5
            if any(max(p[k] for p in (a0, a1)) + limit < min(p[k] for p in (b0, b1)) or
                   max(p[k] for p in (b0, b1)) + limit < min(p[k] for p in (a0, a1)) for k in range(3)):
                continue  # caixas envolventes afastadas
            distance, s_star = segment_distance(a0, a1, b0, b1)
            if distance >= limit:
                continue
            junction = _junction(a0, a1, b0, b1)
            t0, t1 = _contact_interval(a0, a1, b0, b1, limit, s_star)
            u0, u1 = _contact_interval(b0, b1, a0, a1, limit, segment_distance(b0, b1, a0, a1)[1])
            contact = max((t1 - t0) * math.dist(a0, a1), (u1 - u0) * math.dist(b0, b1))
            if junction is not None and contact <= _JUNCTION_ALLOWANCE * (ra + rb) + 1.0:
                continue
            pair = (run_a["run_id"], run_b["run_id"])
            if pair in reported:
                continue
            reported.add(pair)
            where = [p + (t0 + t1) / 2 * (q - p) for p, q in zip(a0, a1)]
            place = f"x {_br(where[0])} · y {_br(where[1])} · cota {_br(where[2])} m"
            who = (f"Trecho {run_a['run_id']}" if run_a is run_b else
                   f"Trechos {run_a['run_id']} ({SYSTEMS_BY_ID[run_a['system']]['label'].lower()}) e "
                   f"{run_b['run_id']} ({SYSTEMS_BY_ID[run_b['system']]['label'].lower()})")
            overlap = contact > 2 * (ra + rb)
            if junction is not None:
                contact -= ra + rb  # o contato natural da própria junção não é sobreposição
            if run_a is run_b:
                what = f"volta sobre si mesmo em {_br(contact)} m" if overlap else "cruza a si mesmo"
            else:
                what = f"se sobrepõem em {_br(contact)} m" if overlap else "se cruzam"
            hint = ""
            node = names.get(junction) if junction is not None else None
            if node:
                hint = f"; ligue-os em pontos distintos de {node} (ex.: {node}:topo e {node}:fundo)"
            elif overlap:
                hint = "; afaste os percursos"
            messages.append(f"{who} {what} perto de {place} (segmentos {ia} e {ib}){hint}.")
    return messages


def _straight_turn(a0, a1, b0, b1) -> bool:
    """Segmentos consecutivos que não voltam sobre si mesmos (ângulo > ~24°)."""
    if math.dist(a1, b0) > CONNECTION_TOLERANCE_MM:
        return False
    u = [q - p for p, q in zip(a0, a1)]
    v = [q - p for p, q in zip(b0, b1)]
    nu, nv = math.sqrt(sum(c * c for c in u)), math.sqrt(sum(c * c for c in v))
    if nu == 0 or nv == 0:
        return True
    # Direções que saem do nó: -u (de volta pelo primeiro) e v (pelo segundo).
    cos_between = -sum(x * y for x, y in zip(u, v)) / (nu * nv)
    return cos_between < math.cos(math.radians(24))


def _junction(a0, a1, b0, b1) -> Optional[Point]:
    """Ponto onde um segmento termina sobre o outro (continuação, curva ou tê)."""
    for p, other in ((a0, (b0, b1)), (a1, (b0, b1)), (b0, (a0, a1)), (b1, (a0, a1))):
        if _point_segment_distance(p, *other) <= CONNECTION_TOLERANCE_MM:
            return (round(p[0], 3), round(p[1], 3), round(p[2], 3))
    return None


junction_point = _junction


def _br(mm: float) -> str:
    return f"{mm / 1000:.2f}".replace(".", ",")


def _gravity_warnings(label: str, segments: Sequence[Dict[str, Any]]) -> List[str]:
    notes = []
    for index, seg in enumerate(segments, start=1):
        a, b = seg["start_mm"], seg["end_mm"]
        dz = b["z"] - a["z"]
        horizontal = math.hypot(b["x"] - a["x"], b["y"] - a["y"])
        if dz > CONNECTION_TOLERANCE_MM:
            notes.append(f"{label}, segmento {index}: sobe {dz:.0f} mm em sistema por gravidade; confira o sentido do escoamento.")
        elif horizontal > CONNECTION_TOLERANCE_MM and -dz / horizontal < MIN_GRAVITY_SLOPE:
            slope = f"{(-dz / horizontal) * 100 + 0.0:.2f}".replace(".", ",")
            minimum = f"{MIN_GRAVITY_SLOPE * 100:.1f}".replace(".", ",")
            notes.append(f"{label}, segmento {index}: declividade {slope} % abaixo de {minimum} %; use 'd dx dy dz' com desnível.")
    return notes


def _xyz(point: Point) -> Dict[str, float]:
    return {"x": round(point[0], 3), "y": round(point[1], 3), "z": round(point[2], 3)}


def lengths_by_dn(resolved_runs: Iterable[Dict[str, Any]]) -> Dict[float, float]:
    """Comprimento total em metros por DN, para conferir o quantitativo de tubos."""
    totals: Dict[float, float] = {}
    for run in resolved_runs:
        totals[run["dn_mm"]] = totals.get(run["dn_mm"], 0.0) + run["length_mm"] / 1000.0
    return {dn: round(value, 3) for dn, value in sorted(totals.items())}
