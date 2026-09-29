"""Planta 3D montada a partir dos trechos organizados pelo projetista.

Cada trecho é desenhado na ordem em que foi organizado, a partir do ponto em que
o anterior terminou (ver :mod:`netuno.core.pipe_network`). O DXF resultante tem,
por sistema, um layer com o eixo da tubulação (POLYLINE 3D) e outro com o tubo
em malha cilíndrica no diâmetro nominal, além dos blocos Netuno posicionados na
cota de cada componente. A prévia SVG é uma perspectiva isométrica do mesmo
modelo, para conferência antes de abrir o CAD.
"""

from __future__ import annotations

import math
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
from ezdxf.render import forms

from .bim_exporter import COMPONENT_TYPES, build_bim_manifest, validate_bim_manifest, write_bim_manifest
from .cad_block_library import APP_ID, configure_cad_document, register_plan_blocks
from .pipe_network import SYSTEMS_BY_ID, lengths_by_dn


_BLOCK_BY_TYPE = {item["type_id"]: item["cad_block"] for item in COMPONENT_TYPES}
_CYLINDER_SIDES = 16


def _checked_manifest(project_data: Dict[str, Any]) -> Dict[str, Any]:
    manifest = build_bim_manifest(project_data)
    errors = validate_bim_manifest(manifest)
    if errors:
        raise ValueError("Planta 3D não gerada:\n- " + "\n- ".join(errors))
    if not manifest["pipe_runs"] and not manifest["instances"]:
        raise ValueError(
            "Planta 3D não gerada: nenhum componente posicionado nem trecho de tubulação organizado. "
            "Organize os trechos antes de exportar."
        )
    return manifest


def generate_plant_3d_dxf(project_data: Dict[str, Any], output_path: str) -> str:
    """Gera a planta 3D em DXF (mm, z para cima) e o manifesto BIM ao lado."""
    manifest = _checked_manifest(project_data)
    doc = ezdxf.new(dxfversion="R2018", setup=True, units=units.MM)
    configure_cad_document(doc)
    register_plan_blocks(doc)
    for name, color in (("NETUNO_3D_EQUIPAMENTOS", 4), ("NETUNO_3D_TEXTOS", 7)):
        doc.layers.add(name, color=color)
    msp = doc.modelspace()

    for run in manifest["pipe_runs"]:
        system = SYSTEMS_BY_ID[run["system"]]
        axis_layer, tube_layer = system["layer"], system["layer"] + "_TUBO"
        for name in (axis_layer, tube_layer):
            if name not in doc.layers:
                doc.layers.add(name, color=system["color"])
        points = [(v["x"], v["y"], v["z"]) for v in run["vertices_mm"]]
        axis = msp.add_polyline3d(points, dxfattribs={"layer": axis_layer})
        axis.set_xdata(APP_ID, [(1000, run["run_id"]), (1070, run["sequence"]), (1000, run["system"])])
        radius = run["dn_mm"] / 2.0
        for a, b in zip(points, points[1:]):
            tube = forms.cylinder_2p(count=_CYLINDER_SIDES, radius=radius, base_center=a, top_center=b)
            tube.render_mesh(msp, dxfattribs={"layer": tube_layer})
        a, b = points[0], points[1]
        mid = tuple((p + q) / 2.0 for p, q in zip(a, b))
        label = f"{run['sequence']:02d} {run['run_id']} {system['label']} DN{run['dn_mm']:g}"
        msp.add_text(label, height=max(60.0, run["dn_mm"] * 1.5), dxfattribs={"layer": "NETUNO_3D_TEXTOS"}).set_placement(
            (mid[0], mid[1], mid[2] + radius + 40.0), align=TextEntityAlignment.BOTTOM_LEFT
        )

    for item in manifest["instances"]:
        pos = item["position_mm"]
        insert = msp.add_blockref(
            _BLOCK_BY_TYPE[item["type_id"]], (pos["x"], pos["y"], pos["z"]),
            dxfattribs={"layer": "NETUNO_3D_EQUIPAMENTOS", "rotation": item["rotation_deg"]},
        )
        values = {"ID": item["instance_id"], **{k: str(v) for k, v in item["parameters"].items()}}
        insert.add_auto_attribs(values)
        insert.set_xdata(APP_ID, [(1000, item["type_id"]), (1000, item["instance_id"])])

    _add_notes(msp, manifest)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)
    write_bim_manifest(project_data, str(path.with_name(path.stem + "_netuno-bim.json")))
    return str(path)


def _add_notes(msp, manifest: Dict[str, Any]) -> None:
    xs, ys, zs = _bounds(manifest)
    x0, y0, z0 = xs[0], ys[0] - 1500.0, zs[0]
    lines = [
        f"NETUNO 5 — PLANTA 3D | {manifest['project']['name']} | Ref.: {manifest['project']['reference']}",
        "Unidades: mm | eixo z para cima | coordenadas locais não georreferenciadas.",
        "Trechos desenhados na sequência organizada pelo projetista; confirmar interferências no projeto executivo.",
    ]
    for dn, meters in lengths_by_dn(manifest["pipe_runs"]).items():
        lines.append(f"DN {dn:g}: {meters:.2f} m".replace(".", ","))
    for warning in manifest["validation"]["warnings"]:
        lines.append(f"ATENÇÃO: {warning}")
    for offset, text in enumerate(lines):
        msp.add_text(text, height=100, dxfattribs={"layer": "NETUNO_3D_TEXTOS"}).set_placement((x0, y0 - offset * 180.0, z0))


def _all_points(manifest: Dict[str, Any]) -> List[Tuple[float, float, float]]:
    points = [(v["x"], v["y"], v["z"]) for run in manifest["pipe_runs"] for v in run["vertices_mm"]]
    points += [(i["position_mm"]["x"], i["position_mm"]["y"], i["position_mm"]["z"]) for i in manifest["instances"]]
    return points


def _bounds(manifest: Dict[str, Any]):
    points = _all_points(manifest) or [(0.0, 0.0, 0.0)]
    return tuple((min(values), max(values)) for values in zip(*points))


# ── Prévia isométrica ────────────────────────────────────────────────────────

_COS30, _SIN30 = math.cos(math.radians(30)), 0.5


def _iso(x: float, y: float, z: float) -> Tuple[float, float]:
    return (x - y) * _COS30, (x + y) * _SIN30 - z


def generate_plant_3d_svg(project_data: Dict[str, Any], output_path: Optional[str] = None) -> str:
    """Perspectiva isométrica da planta 3D, numerada na ordem dos trechos."""
    manifest = _checked_manifest(project_data)
    width, height, margin, legend_w = 1000.0, 700.0, 60.0, 250.0
    projected = [_iso(*p) for p in _all_points(manifest)]
    us, vs = [p[0] for p in projected], [p[1] for p in projected]
    span_u, span_v = max(max(us) - min(us), 1.0), max(max(vs) - min(vs), 1.0)
    scale = min((width - legend_w - 2 * margin) / span_u, (height - 2 * margin - 40) / span_v)

    def screen(x: float, y: float, z: float) -> Tuple[float, float]:
        u, v = _iso(x, y, z)
        return margin + (u - min(us)) * scale, margin + 40 + (v - min(vs)) * scale

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" font-family="Segoe UI, Arial, sans-serif">',
        f'<rect width="{width:.0f}" height="{height:.0f}" fill="#ffffff"/>',
        f'<text x="{margin}" y="32" font-size="18" font-weight="700" fill="#0f172a">Planta 3D — {escape(manifest["project"]["name"])}</text>',
    ]
    for run in manifest["pipe_runs"]:
        system = SYSTEMS_BY_ID[run["system"]]
        pts = [screen(v["x"], v["y"], v["z"]) for v in run["vertices_mm"]]
        stroke = max(2.0, min(9.0, run["dn_mm"] * scale * 4))
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polyline points="{path}" fill="none" stroke="{system["svg"]}" stroke-width="{stroke:.1f}" stroke-linejoin="round" stroke-linecap="round"/>')
        mx, my = (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2
        parts.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="11" fill="#ffffff" stroke="{system["svg"]}" stroke-width="2"/>')
        parts.append(f'<text x="{mx:.1f}" y="{my + 4:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="#0f172a">{run["sequence"]}</text>')
    for item in manifest["instances"]:
        pos = item["position_mm"]
        x, y = screen(pos["x"], pos["y"], pos["z"])
        parts.append(f'<rect x="{x - 6:.1f}" y="{y - 6:.1f}" width="12" height="12" fill="#0f172a"/>')
        parts.append(f'<text x="{x + 10:.1f}" y="{y - 8:.1f}" font-size="12" fill="#0f172a">{escape(item["instance_id"])}</text>')

    lx, ly = width - legend_w + 10, margin + 40
    parts.append(f'<text x="{lx}" y="{ly}" font-size="13" font-weight="700" fill="#0f172a">Sequência de trechos</text>')
    for offset, run in enumerate(manifest["pipe_runs"], start=1):
        system = SYSTEMS_BY_ID[run["system"]]
        y = ly + offset * 20
        parts.append(f'<rect x="{lx}" y="{y - 10}" width="14" height="4" fill="{system["svg"]}"/>')
        meters = f'{run["length_mm"] / 1000:.2f}'.replace(".", ",")
        text = f'{run["sequence"]}. {run["run_id"]} — DN {run["dn_mm"]:g} — {meters} m'
        parts.append(f'<text x="{lx + 20}" y="{y}" font-size="11" fill="#334155">{escape(text)}</text>')
    for index, warning in enumerate(manifest["validation"]["warnings"][:6]):
        parts.append(f'<text x="{margin}" y="{height - 110 + index * 16}" font-size="11" fill="#b45309">⚠ {escape(warning)}</text>')
    parts.append(f'<text x="{margin}" y="{height - 10}" font-size="10" fill="#64748b">Isométrica sem escala · unidades em mm · z para cima</text>')
    parts.append("</svg>")
    svg = "\n".join(parts)
    if output_path:
        Path(output_path).write_text(svg, encoding="utf-8")
    return svg
