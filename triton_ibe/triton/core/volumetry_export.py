"""Exportação da volumetria: glTF binário (.glb) e página HTML interativa.

* ``.glb`` (glTF 2.0) abre no Visualizador 3D do Windows, no Blender, no
  SketchUp (com extensão) e em qualquer visualizador web. Cada sólido é um nó
  nomeado com a sua ficha em ``extras``.
* ``.html`` é autocontido: o visualizador three.js de ``web/volumetria``
  (empacotado em ``triton/data/volumetria``), o céu HDRI e a cena num único
  arquivo, sem internet, para girar, cortar, medir, clicar nas peças e
  compartilhar.
"""

from __future__ import annotations

import base64
import json
import math
import re
import struct
from html import escape
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .pipe_network import PIPE_SYSTEMS
from .volumetry import CONTROL_SYSTEM, Point, Scene, Solid, build_volumetry, face_normal

_ANGLE_FEATURE_DEG = 25.0
# Cascas abertas ou translúcidas de propósito: as duas faces são visíveis.
_DOUBLE_SIDED = {"building", "slab", "ground"}


def _key(p: Point) -> Tuple[float, float, float]:
    return (round(p[0], 3), round(p[1], 3), round(p[2], 3))


def feature_edges(solid: Solid) -> List[List[Tuple[Point, Point]]]:
    """Arestas que marcam a forma, por face: bordas livres e dobras acentuadas.

    Omite as arestas entre faces quase coplanares, como as geratrizes de um
    cilindro facetado, que só poluiriam o desenho.
    """
    normals = [face_normal(face) for face in solid.faces]
    owners: Dict[Tuple, List[int]] = {}
    for index, face in enumerate(solid.faces):
        for a, b in zip(face, list(face[1:]) + [face[0]]):
            owners.setdefault(tuple(sorted((_key(a), _key(b)))), []).append(index)
    limit = math.cos(math.radians(_ANGLE_FEATURE_DEG))
    result: List[List[Tuple[Point, Point]]] = [[] for _ in solid.faces]
    for index, face in enumerate(solid.faces):
        for a, b in zip(face, list(face[1:]) + [face[0]]):
            faces = owners[tuple(sorted((_key(a), _key(b))))]
            others = [f for f in faces if f != index]
            if not others or any(sum(x * y for x, y in zip(normals[index], normals[o])) < limit for o in others):
                result[index].append((a, b))
    return result


def _triangles(face: Sequence[Point]) -> List[Tuple[Point, Point, Point]]:
    return [(face[0], face[i], face[i + 1]) for i in range(1, len(face) - 1)]


# ── glTF binário ─────────────────────────────────────────────────────────────

def _to_gltf(p: Point) -> Tuple[float, float, float]:
    # Triton: mm, z para cima. glTF: metros, y para cima (rotação própria, preserva a orientação das faces).
    return (p[0] / 1000.0, p[2] / 1000.0, -p[1] / 1000.0)


def write_glb(scene: Scene, output_path: str) -> str:
    binary = bytearray()
    buffer_views, accessors, meshes, nodes, materials = [], [], [], [], []
    material_index: Dict[Tuple, int] = {}

    def add_view(data: bytes, target: int) -> int:
        while len(binary) % 4:
            binary.append(0)
        buffer_views.append({"buffer": 0, "byteOffset": len(binary), "byteLength": len(data), "target": target})
        binary.extend(data)
        return len(buffer_views) - 1

    for solid in scene.solids:
        positions: List[float] = []
        normals: List[float] = []
        for face in solid.faces:
            n = _to_gltf(tuple(c * 1000.0 for c in face_normal(face)))  # type: ignore[arg-type]
            for tri in _triangles(face):
                for p in tri:
                    positions.extend(_to_gltf(p))
                    normals.extend(n)
        if not positions:
            continue
        count = len(positions) // 3
        xs, ys, zs = positions[0::3], positions[1::3], positions[2::3]
        pos_view = add_view(struct.pack(f"<{len(positions)}f", *positions), 34962)
        nor_view = add_view(struct.pack(f"<{len(normals)}f", *normals), 34962)
        accessors.append({"bufferView": pos_view, "componentType": 5126, "count": count, "type": "VEC3",
                          "min": [min(xs), min(ys), min(zs)], "max": [max(xs), max(ys), max(zs)]})
        accessors.append({"bufferView": nor_view, "componentType": 5126, "count": count, "type": "VEC3"})
        mat_key = (solid.color, round(solid.opacity, 3), solid.kind in _DOUBLE_SIDED)
        if mat_key not in material_index:
            r, g, b = (c / 255.0 for c in solid.color)
            material = {"name": f"triton_{len(materials)}", "doubleSided": solid.kind in _DOUBLE_SIDED,
                        "pbrMetallicRoughness": {"baseColorFactor": [r, g, b, solid.opacity], "metallicFactor": 0.0, "roughnessFactor": 0.8}}
            if solid.opacity < 1.0:
                material["alphaMode"] = "BLEND"
            materials.append(material)
            material_index[mat_key] = len(materials) - 1
        meshes.append({"name": solid.key, "primitives": [{"attributes": {"POSITION": len(accessors) - 2, "NORMAL": len(accessors) - 1},
                                                           "material": material_index[mat_key]}]})
        nodes.append({"name": solid.key, "mesh": len(meshes) - 1,
                      "extras": {"titulo": solid.title, "ficha": solid.info, "tipo": solid.kind}})

    while len(binary) % 4:
        binary.append(0)
    document = {
        "asset": {"version": "2.0", "generator": "Triton — volumetria"},
        "scene": 0,
        "scenes": [{"name": scene.title, "nodes": list(range(len(nodes))), "extras": {"notas": scene.notes, "unidades": "m, y para cima"}}],
        "nodes": nodes, "meshes": meshes, "materials": materials, "accessors": accessors,
        "bufferViews": buffer_views, "buffers": [{"byteLength": len(binary)}],
    }
    json_chunk = json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    json_chunk += b" " * ((4 - len(json_chunk) % 4) % 4)
    total = 12 + 8 + len(json_chunk) + 8 + len(binary)
    data = b"".join([
        struct.pack("<4sII", b"glTF", 2, total),
        struct.pack("<I4s", len(json_chunk), b"JSON"), json_chunk,
        struct.pack("<I4s", len(binary), b"BIN\x00"), bytes(binary),
    ])
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


def write_volumetry_package(project_data: Dict, stem: str, texts: Optional[Dict[str, str]] = None) -> Tuple[str, str]:
    """Grava ``<stem>_volumetria.glb`` e ``<stem>_volumetria.html`` da mesma cena."""
    scene = build_volumetry(project_data)
    return write_glb(scene, f"{stem}_volumetria.glb"), write_html_viewer(scene, f"{stem}_volumetria.html", texts)


# ── HTML interativo ──────────────────────────────────────────────────────────

def scene_payload(scene: Scene) -> Dict:
    """Cena em metros, pronta para o visualizador: triângulos, arestas e fichas."""
    solids = []
    for solid in scene.solids:
        tris: List[float] = []
        norms: List[float] = []
        for face in solid.faces:
            n = face_normal(face)
            for tri in _triangles(face):
                for p in tri:
                    tris.extend(round(c / 1000.0, 4) for c in p)
                    norms.extend(round(c, 4) for c in n)
        edges: List[float] = []
        if solid.outline:
            seen = set()
            for face_edges in feature_edges(solid):
                for a, b in face_edges:
                    k = tuple(sorted((_key(a), _key(b))))
                    if k not in seen:
                        seen.add(k)
                        edges.extend(round(c / 1000.0, 4) for c in (*a, *b))
        points = [p for face in solid.faces for p in face]
        box = [[round(min(p[k] for p in points) / 1000.0, 4) for k in range(3)],
               [round(max(p[k] for p in points) / 1000.0, 4) for k in range(3)]] if points else None
        solids.append({
            "key": solid.key, "kind": solid.kind, "title": solid.title, "info": solid.info,
            "color": list(solid.color), "opacity": solid.opacity, "pickable": solid.pickable, "group": solid.group,
            "label": [round(c / 1000.0, 4) for c in solid.label_at] if solid.label_at else None,
            "tris": tris, "norms": norms, "edges": edges,
            "type": solid.type_id, "rotation": solid.rotation_deg, "system": solid.system, "box": box,
            "dn": solid.dn_mm,
            "axis": ([round(c / 1000.0, 4) for c in (*solid.axis[0], *solid.axis[1])] + [round(solid.axis[2] / 1000.0, 5)]
                     if solid.axis else None),
        })
    low, high = scene.bounds
    return {"title": scene.title, "notes": scene.notes, "solids": solids,
            "bounds": [[c / 1000.0 for c in low], [c / 1000.0 for c in high]],
            "systems": [{"id": s["system_id"], "label": s["label"], "color": s["svg"], "gravity": bool(s.get("gravity"))}
                        for s in PIPE_SYSTEMS] + [dict(CONTROL_SYSTEM, gravity=False, cable=True)]}


#: Visualizador empacotado (web/volumetria, three.js) e céu HDRI (Poly Haven, CC0).
VIEWER_DIR = Path(__file__).resolve().parents[1] / "data" / "volumetria"
VIEWER_BUNDLE = VIEWER_DIR / "triton_volumetria.js"
VIEWER_SKY = VIEWER_DIR / "ceu_quarry_01_1k.hdr"


def _script_safe(text: str) -> str:
    return text.replace("</", "<\\/")


def viewer_html(scene: Scene, texts: Optional[Dict[str, str]] = None, theme: Optional[str] = None) -> str:
    """Página única e autocontida: visualizador, céu e cena no mesmo arquivo.

    Nada é buscado na internet: o three.js vai empacotado e o céu vai em base64.
    O mesmo HTML abre no navegador e na aba do programa (QtWebEngine).
    """
    bundle = VIEWER_BUNDLE.read_text(encoding="utf-8")
    sky = base64.b64encode(VIEWER_SKY.read_bytes()).decode("ascii") if VIEWER_SKY.is_file() else ""
    payload = _script_safe(json.dumps(scene_payload(scene), ensure_ascii=False, separators=(",", ":")))
    options = _script_safe(json.dumps({"texts": texts or {}, "theme": theme}, ensure_ascii=False, separators=(",", ":")))
    title = escape((texts or {}).get("titulo", "Volumetria 3D") + " — " + scene.title)
    values = {"TITLE": title, "BUNDLE": bundle, "SCENE": payload, "SKY": sky, "OPTIONS": options}
    # Uma passada só: o texto de um campo (o nome do projeto, por exemplo) nunca
    # é lido como marcador de outro.
    return re.sub(r"__(TITLE|BUNDLE|SCENE|SKY|OPTIONS)__", lambda m: values[m.group(1)], _HTML_TEMPLATE)


def write_html_viewer(scene: Scene, output_path: str, texts: Optional[Dict[str, str]] = None) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(viewer_html(scene, texts), encoding="utf-8")
    return str(path)


_HTML_TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>html,body{margin:0;height:100%;overflow:hidden;background:#f5f7fa}#nv{height:100%}</style>
</head>
<body>
<div id="nv"></div>
<script>
__BUNDLE__
const SCENE = __SCENE__;
const SKY = "__SKY__";
const OPTIONS = __OPTIONS__;
TritonVolumetria.mount(document.getElementById("nv"), Object.assign({scene: SCENE, hdr: SKY || null}, OPTIONS));
</script>
</body>
</html>
"""
