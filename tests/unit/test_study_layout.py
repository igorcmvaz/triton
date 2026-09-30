"""Testes para geração de layout 3D a partir dos dados do estudo."""

from netuno.core.bim_exporter import build_bim_manifest, validate_bim_manifest
from netuno.core.schematic_3d import generate_schematic_3d_svg
from netuno.core.study_layout import generate_study_layout
from netuno.core.volumetry import build_volumetry


def test_generate_study_layout_creates_valid_bim_manifest():
    project_data = {
        "project_name": "Edifício Residencial Teste",
        "lower_vol": 8000.0,
        "upper_vol": 2000.0,
        "area": 250.0,
        "floors": 3,
    }
    layout = generate_study_layout(project_data)
    assert len(layout["bim_components"]) == 3
    assert len(layout["pipe_runs"]) == 4
    assert layout["building_volume"]["floors"] == 3

    full_project = dict(project_data, **layout)
    manifest = build_bim_manifest(full_project)
    errors = validate_bim_manifest(manifest)
    assert errors == []
    assert manifest["validation"]["warnings"] == []

    # Valida geração de volumetria 3D e esquema SVG
    scene = build_volumetry(full_project)
    assert len(scene.solids) > 10

    svg = generate_schematic_3d_svg(full_project)
    assert "Esquema 3D da tubulação" in svg
    assert "CI-01" in svg and "RS-01" in svg


def test_generate_study_layout_with_defaults():
    layout = generate_study_layout({})
    assert len(layout["bim_components"]) == 3
    assert len(layout["pipe_runs"]) == 4
    manifest = build_bim_manifest(layout)
    assert validate_bim_manifest(manifest) == []
