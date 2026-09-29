"""Trechos organizados pelo projetista e a planta 3D montada em sequência."""

import json

import ezdxf
import pytest

from netuno.core.bim_exporter import build_bim_manifest, validate_bim_manifest
from netuno.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram
from netuno.core.parser import NetunoConfig, export_netuno_json, load_netuno_project
from netuno.core.pipe_network import format_route, lengths_by_dn, parse_route


COMPONENTS = [
    {"instance_id": "CI-01", "type_id": "cisterna_inferior", "position_mm": {"x": 0, "y": 0, "z": -1500}},
    {"instance_id": "B-01", "type_id": "motobomba", "position_mm": {"x": 1500, "y": 0, "z": 0}},
    {"instance_id": "RS-01", "type_id": "reservatorio_superior", "position_mm": {"x": 4500, "y": 2000, "z": 6500}},
]
RUNS = [
    {"run_id": "T-01", "system": "succao", "dn_mm": 32, "start": "CI-01", "route": "sobe 1500; +x 1500", "end": "B-01"},
    # Sem origem: continua do fim de T-01, que está na bomba.
    {"run_id": "T-02", "system": "recalque", "dn_mm": 25, "route": "+x 3000; +y 2000; sobe 6500", "end": "RS-01"},
    {"run_id": "T-03", "system": "distribuicao", "dn_mm": 25, "start": "RS-01", "route": "desce 3000; -y 4000"},
]


def _project(runs=RUNS, components=COMPONENTS):
    return {"project_name": "Casa 3D", "ref_code": "N5-3D", "bim_components": components, "pipe_runs": runs}


def test_parse_route_accepts_axes_aliases_and_free_deltas():
    assert parse_route("+x 3000; desce 1200; norte 500; d 2000 0 -20") == [
        (3000.0, 0.0, 0.0), (0.0, 0.0, -1200.0), (0.0, 500.0, 0.0), (2000.0, 0.0, -20.0),
    ]
    assert parse_route([{"direction": "-y", "length_mm": "1,5"}, {"dx": 1, "dy": 2, "dz": 3}]) == [(0.0, -1.5, 0.0), (1.0, 2.0, 3.0)]
    assert format_route(parse_route("+x 3000; desce 1200; d 2000 0 -20")) == "+x 3000; -z 1200; d 2000 0 -20"
    for bad in ("+w 100", "+x -5", "d 1 2", "sobe"):
        with pytest.raises(ValueError):
            parse_route(bad)


def test_runs_are_resolved_in_sequence_from_the_previous_end():
    manifest = build_bim_manifest(_project())
    assert validate_bim_manifest(manifest) == []
    runs = {run["run_id"]: run for run in manifest["pipe_runs"]}
    assert [run["sequence"] for run in manifest["pipe_runs"]] == [1, 2, 3]
    assert runs["T-02"]["start_ref"] == "T-01"
    assert runs["T-02"]["vertices_mm"][0] == {"x": 1500, "y": 0, "z": 0}
    assert runs["T-02"]["vertices_mm"][-1] == {"x": 4500, "y": 2000, "z": 6500}
    assert runs["T-02"]["length_mm"] == 11500
    assert lengths_by_dn(manifest["pipe_runs"]) == {25.0: 18.5, 32.0: 3.0}


def test_reordering_changes_the_plant_and_is_reported():
    manifest = build_bim_manifest(_project(runs=[RUNS[1], RUNS[0], RUNS[2]]))
    errors = validate_bim_manifest(manifest)
    assert any("T-02" in e and "primeiro trecho precisa de origem" in e for e in errors)


def test_declared_destination_is_checked_not_completed():
    runs = [dict(RUNS[0], route="sobe 1500; +x 1400")]
    errors = validate_bim_manifest(build_bim_manifest(_project(runs=runs)))
    assert errors == ["Trecho T-01: termina a 100 mm de B-01; falta 'd 100 0 0'."]


def test_dependent_run_is_not_resolved_when_its_origin_failed():
    runs = [dict(RUNS[0], dn_mm=0), RUNS[1]]
    errors = validate_bim_manifest(build_bim_manifest(_project(runs=runs)))
    assert any("T-02: continua o trecho T-01" in e for e in errors)


def test_gravity_systems_warn_about_rising_or_flat_segments():
    runs = [{"run_id": "C-01", "system": "captacao", "dn_mm": 100, "start": {"x": 0, "y": 0, "z": 3000},
             "route": "+x 2000; d 2000 0 -20; sobe 100"}]
    manifest = build_bim_manifest(_project(runs=runs, components=[]))
    assert validate_bim_manifest(manifest) == []
    warnings = manifest["validation"]["warnings"]
    assert len(warnings) == 2
    assert "segmento 1: declividade 0,00 % abaixo de 0,5 %" in warnings[0]
    assert "segmento 3: sobe 100 mm" in warnings[1]


def test_plant_3d_dxf_has_axes_tubes_components_and_manifest(tmp_path):
    output = tmp_path / "planta.dxf"
    generate_project_dxf(_project(), str(output), mode="plant_3d")
    doc = ezdxf.readfile(output)
    assert not doc.audit().errors
    msp = doc.modelspace()
    axes = msp.query("POLYLINE")
    assert len(axes) == 3 and all(axis.is_3d_polyline for axis in axes)
    assert [axis.get_xdata("NETUNO5")[0].value for axis in axes] == ["T-01", "T-02", "T-03"]
    assert len(msp.query("MESH")) == 2 + 3 + 2
    assert all(name in doc.layers for name in ("NETUNO_3D_SUCCAO", "NETUNO_3D_RECALQUE_TUBO"))
    assert len(msp.query("INSERT")) == 3
    manifest = json.loads((tmp_path / "planta_netuno-bim.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.1"
    assert [run["run_id"] for run in manifest["pipe_runs"]] == ["T-01", "T-02", "T-03"]


def test_plant_3d_refuses_invalid_or_empty_organisation(tmp_path):
    with pytest.raises(ValueError, match="nenhum componente"):
        generate_project_dxf(_project(runs=[], components=[]), str(tmp_path / "vazio.dxf"), mode="plant_3d")
    with pytest.raises(ValueError, match="falta"):
        generate_project_dxf(_project(runs=[dict(RUNS[0], route="sobe 1500")]), str(tmp_path / "x.dxf"), mode="plant_3d")
    assert not (tmp_path / "x.dxf").exists()


def test_plant_3d_svg_numbers_runs_in_sequence():
    svg = generate_project_svg_diagram(_project(), mode="plant_3d")
    assert svg.startswith("<svg") and "Sequência de trechos" in svg
    assert svg.index("1. T-01") < svg.index("2. T-02") < svg.index("3. T-03")


def test_bim_layout_round_trips_through_netuno_file(tmp_path):
    path = tmp_path / "projeto.netuno"
    export_netuno_json(NetunoConfig(), str(path), bim_layout={"bim_components": COMPONENTS, "pipe_runs": RUNS})
    loaded = load_netuno_project(str(path))
    assert loaded["bim_layout"] == {"bim_components": COMPONENTS, "pipe_runs": RUNS}
    export_netuno_json(NetunoConfig(), str(path))
    assert load_netuno_project(str(path))["bim_layout"] == {"bim_components": [], "pipe_runs": []}
