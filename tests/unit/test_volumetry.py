"""Volumetria 3D: sólidos coerentes, dimensões rastreáveis e arquivos válidos."""

import json
import math
import re
import struct

import pytest

from netuno.core.volumetry import build_volumetry, face_normal, prism, regular_polygon, tank_dimensions_mm, tube
from netuno.core.volumetry_export import feature_edges, scene_payload, write_glb, write_html_viewer


COMPONENTS = [
    {"instance_id": "CI-01", "type_id": "cisterna_inferior", "position_mm": {"x": 0, "y": 0, "z": -1500}},
    {"instance_id": "B-01", "type_id": "motobomba", "position_mm": {"x": 1500, "y": 0, "z": 0}, "rotation_deg": 30},
    {"instance_id": "RS-01", "type_id": "reservatorio_superior", "position_mm": {"x": 4500, "y": 2000, "z": 6500},
     "parameters": {"CAPACIDADE_L": 1000, "DIAMETRO_MM": 1400, "ALTURA_MM": 800}},
]
RUNS = [
    {"run_id": "T-01", "system": "succao", "dn_mm": 32, "start": "CI-01", "route": "sobe 1500; +x 1500", "end": "B-01"},
    {"run_id": "T-02", "system": "recalque", "dn_mm": 25, "route": "+x 3000; +y 2000; sobe 6500", "end": "RS-01"},
]
BUILDING = {"origin_mm": {"x": -1000, "y": -3000, "z": 0}, "width_mm": 8000, "depth_mm": 7000, "height_mm": 6000, "floors": 2}


def _project(**extra):
    data = {"project_name": "Casa 3D", "lower_vol": 5000, "upper_vol": 500,
            "bim_components": COMPONENTS, "pipe_runs": RUNS, "building_volume": BUILDING}
    data.update(extra)
    return data


def _outward(faces):
    pts = [p for f in faces for p in f]
    center = [sum(c) / len(pts) for c in zip(*pts)]
    for face in faces:
        n = face_normal(face)
        fc = [sum(c) / len(face) for c in zip(*face)]
        if sum(a * (b - c) for a, b, c in zip(n, fc, center)) <= 0:
            return False
    return True


def test_primitives_are_closed_with_outward_normals():
    assert _outward(prism(regular_polygon(900, 32), (0, 0, 0), 1800))
    assert _outward(prism([(300, 0), (0, 200), (-300, 0), (0, -200)], (10, 20, 30), 320, rotation_deg=45))
    for a, b in (((0, 0, 0), (3000, 0, 0)), ((0, 0, 0), (0, 0, -2000)), ((0, 0, 0), (1000, 2000, -30))):
        faces = tube(a, b, 50)
        assert len(faces) == 10 and _outward(faces)


def test_tank_dimensions_reproduce_the_capacity_or_keep_given_measures():
    d, h, capacity, estimated = tank_dimensions_mm("cisterna_inferior", {}, 5000)
    assert estimated and capacity == 5000 and h == pytest.approx(d)
    assert math.pi * d ** 2 / 4 * h == pytest.approx(5000e6)
    d, h, _, estimated = tank_dimensions_mm("reservatorio_superior", {"CAPACIDADE_L": "500"}, 9999)
    assert estimated and h == pytest.approx(0.55 * d) and math.pi * d ** 2 / 4 * h == pytest.approx(500e6)
    assert tank_dimensions_mm("reservatorio_superior", {"DIAMETRO_MM": 1400, "ALTURA_MM": 800}, 1)[:2] == (1400, 800)
    d, h, _, _ = tank_dimensions_mm("cisterna_inferior", {"DIAMETRO_MM": 2000}, 10000)
    assert d == 2000 and math.pi * d ** 2 / 4 * h == pytest.approx(10000e6)


def test_scene_uses_the_expected_volumes_and_declares_estimates():
    scene = build_volumetry(_project())
    by_key = {s.key: s for s in scene.solids}
    assert by_key["CI-01"].kind == "tank" and len(by_key["CI-01"].faces) == 34
    assert any("estimado" in line for line in by_key["CI-01"].info)
    assert not any("estimado" in line for line in by_key["RS-01"].info)
    # A base do reservatório fica na cota do componente e o topo, a H acima.
    zs = [p[2] for f in by_key["RS-01"].faces for p in f]
    assert (min(zs), max(zs)) == (6500, 7300)
    pump_xy = {(round(p[0]), round(p[1])) for f in by_key["B-01"].faces for p in f}
    assert len(pump_xy) == 4  # base losango
    assert by_key["EDIFICACAO"].opacity < 0.5 and "LAJE-1" in by_key
    assert [s.key for s in scene.solids if s.kind == "pipe" and s.pickable] == ["T-01#1", "T-01#2", "T-02#1", "T-02#2", "T-02#3"]
    assert scene.solids[0].kind == "ground"
    assert any("ampliada" in n for n in scene.notes)


def test_scene_without_building_or_with_invalid_layout():
    scene = build_volumetry(_project(building_volume={"width_mm": 0}))
    assert not any(s.kind == "building" for s in scene.solids)
    with pytest.raises(ValueError, match="falta"):
        build_volumetry(_project(pipe_runs=[dict(RUNS[0], route="sobe 1500")]))


def test_feature_edges_skip_cylinder_generatrices():
    box = prism([(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 0), 1)
    edges = {tuple(sorted((a, b))) for face in feature_edges(_solid(box)) for a, b in face}
    assert len(edges) == 12
    cylinder = prism(regular_polygon(1000, 32), (0, 0, 0), 1000)
    edges = {tuple(sorted((a, b))) for face in feature_edges(_solid(cylinder)) for a, b in face}
    assert len(edges) == 64  # só os dois aros


def _solid(faces):
    from netuno.core.volumetry import Solid
    return Solid("X", "tank", "X", [], (0, 0, 0), faces)


def test_glb_is_structurally_valid_gltf(tmp_path):
    path = write_glb(build_volumetry(_project()), str(tmp_path / "v.glb"))
    data = open(path, "rb").read()
    magic, version, total = struct.unpack_from("<4sII", data)
    assert (magic, version, total) == (b"glTF", 2, len(data))
    json_len, json_type = struct.unpack_from("<I4s", data, 12)
    assert json_type == b"JSON" and json_len % 4 == 0
    doc = json.loads(data[20:20 + json_len])
    bin_len, bin_type = struct.unpack_from("<I4s", data, 20 + json_len)
    assert bin_type == b"BIN\x00" and bin_len == doc["buffers"][0]["byteLength"] and bin_len % 4 == 0
    for acc in doc["accessors"]:
        view = doc["bufferViews"][acc["bufferView"]]
        assert view["byteLength"] == acc["count"] * 12 and view["byteOffset"] % 4 == 0
        assert view["byteOffset"] + view["byteLength"] <= bin_len
    names = [n["name"] for n in doc["nodes"]]
    assert "CI-01" in names and "T-02#3" in names
    assert doc["nodes"][names.index("RS-01")]["extras"]["titulo"].startswith("RS-01")
    blend = [m for m in doc["materials"] if m.get("alphaMode") == "BLEND"]
    assert blend and all(m["pbrMetallicRoughness"]["baseColorFactor"][3] < 1 for m in blend)


def test_html_viewer_is_self_contained_and_carries_the_scene(tmp_path):
    scene = build_volumetry(_project(project_name="Casa </script> 3D"))
    html = open(write_html_viewer(scene, str(tmp_path / "v.html")), encoding="utf-8").read()
    assert "http://" not in html.replace("http://www.w3.org", "") and "https://" not in html
    assert html.count("</script>") == 1  # o nome do projeto não fecha o script
    payload = re.search(r"const SCENE = (\{.*?\});\n", html, re.S).group(1)
    data = json.loads(payload.replace("<\\/", "</"))
    assert data["title"] == "Casa </script> 3D"
    assert {s["key"] for s in data["solids"]} >= {"CI-01", "B-01", "RS-01", "EDIFICACAO", "TERRENO"}
    tank = next(s for s in data["solids"] if s["key"] == "CI-01")
    assert len(tank["tris"]) == len(tank["norms"]) and len(tank["tris"]) % 9 == 0
    assert scene_payload(scene)["bounds"][0][2] == pytest.approx(-1.5)


def test_package_writes_both_files_next_to_the_drawing(tmp_path):
    from netuno.core.volumetry_export import write_volumetry_package

    glb, html = write_volumetry_package(_project(), str(tmp_path / "Casa_Planta_3D"))
    assert glb.endswith("Casa_Planta_3D_volumetria.glb") and html.endswith("Casa_Planta_3D_volumetria.html")
    assert open(glb, "rb").read(4) == b"glTF"


def test_visual_thickness_never_makes_close_pipes_look_merged():
    # Dois tubos DN 25 paralelos a 60 mm (sem interferência) numa cena de 30 m:
    # a espessura mínima de visualização (~100 mm) os fundiria num só.
    base = {"system": "distribuicao", "dn_mm": 25}
    runs = [dict(base, run_id="A", start={"x": 0, "y": 0, "z": 0}, route="+x 30000"),
            dict(base, run_id="B", start={"x": 0, "y": 60, "z": 0}, route="+x 30000")]
    scene = build_volumetry({"project_name": "Paralelos", "pipe_runs": runs})
    radii = {s.group: s.axis[2] for s in scene.solids if s.kind == "pipe" and s.pickable}
    assert radii["A"] + radii["B"] < 60
    assert radii["A"] >= 12.5  # nunca menor que o tubo real
