"""Testes para geração de layout 3D a partir dos dados do estudo."""

import pytest

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
        "discard": 2.0,
        "floors": 3,
    }
    layout = generate_study_layout(project_data)
    # Inclui FP-01, FF-01, CI-01, B-01, RS-01
    comp_ids = [c["instance_id"] for c in layout["bim_components"]]
    assert comp_ids == ["FP-01", "FF-01", "CI-01", "B-01", "RS-01"]
    assert len(layout["bim_components"]) == 5
    assert len(layout["pipe_runs"]) == 6
    assert layout["building_volume"]["floors"] == 3

    # Verifica parâmetros calculados
    ff_comp = next(c for c in layout["bim_components"] if c["instance_id"] == "FF-01")
    assert ff_comp["parameters"]["VOLUME_L"] == 500.0  # 2.0 mm * 250 m² = 500 L
    assert ff_comp["parameters"]["DESCARTE_MM"] == 2.0

    fp_comp = next(c for c in layout["bim_components"] if c["instance_id"] == "FP-01")
    assert fp_comp["parameters"]["DN_MM"] == 150.0  # área > 200 m²
    assert fp_comp["parameters"]["MALHA_MM"] == 0.35

    pump_comp = next(c for c in layout["bim_components"] if c["instance_id"] == "B-01")
    assert pump_comp["parameters"]["POTENCIA_KW"] > 0
    assert pump_comp["parameters"]["VAZAO_L_MIN"] > 0

    full_project = dict(project_data, **layout)
    manifest = build_bim_manifest(full_project)
    errors = validate_bim_manifest(manifest)
    assert errors == []
    assert manifest["validation"]["warnings"] == []

    # Valida geração de volumetria 3D e esquema SVG
    scene = build_volumetry(full_project)
    assert len(scene.solids) > 12

    # Verifica se os sólidos contêm informações técnicas ricas
    pump_solid = next(s for s in scene.solids if s.key == "B-01")
    assert any("Potência nominal" in line for line in pump_solid.info)
    assert any("Vazão de operação" in line for line in pump_solid.info)
    assert any("Forchheimer" in line for line in pump_solid.info)

    ff_solid = next(s for s in scene.solids if s.key == "FF-01")
    assert any("Volume de descarte calculado" in line for line in ff_solid.info)

    fp_solid = next(s for s in scene.solids if s.key == "FP-01")
    assert any("Malha filtrante" in line for line in fp_solid.info)

    svg = generate_schematic_3d_svg(full_project)
    assert "Esquema 3D da tubulação" in svg
    assert "CI-01" in svg and "RS-01" in svg and "FP-01" in svg and "FF-01" in svg


def test_generate_study_layout_with_defaults():
    layout = generate_study_layout({})
    assert len(layout["bim_components"]) == 5
    assert len(layout["pipe_runs"]) == 6
    comp_ids = [c["instance_id"] for c in layout["bim_components"]]
    assert comp_ids == ["FP-01", "FF-01", "CI-01", "B-01", "RS-01"]
    manifest = build_bim_manifest(layout)
    assert validate_bim_manifest(manifest) == []


@pytest.mark.parametrize("rotulo, cv, kw", [
    ("1/2", 0.5, 0.37), ("3/4", 0.75, 0.55), ("1", 1.0, 0.75), ("1 1/2", 1.5, 1.1),
    ("1.1/2", 1.5, 1.1), ("1/3", 1 / 3, 0.25), ("2 CV", 2.0, 1.5), ("", 0.5, 0.37),
])
def test_o_rotulo_da_bomba_vira_a_potencia_certa(rotulo, cv, kw):
    """«1 1/2» era lido como ½ CV, e «1/3» como 1 CV (teste por substring)."""
    from netuno.core.study_layout import potencia_da_motobomba

    assert potencia_da_motobomba(rotulo) == (pytest.approx(cv), pytest.approx(kw))


def test_o_kw_informado_prevalece_sobre_o_rotulo():
    from netuno.core.study_layout import potencia_da_motobomba

    assert potencia_da_motobomba("1/2", 0.55)[1] == pytest.approx(0.55)


def test_a_captacao_nasce_no_telhado_e_desce_no_filtro():
    """O trecho do telhado começava no ar, além do filtro, apontando para fora."""
    layout = generate_study_layout({"lower_vol": 10000, "area": 180, "floors": 3})
    predio = layout["building_volume"]
    t01 = next(r for r in layout["pipe_runs"] if r["run_id"] == "T-01")
    inicio = t01["start"]
    assert inicio["z"] == pytest.approx(predio["height_mm"])  # na cota da cobertura
    assert 0 < inicio["x"] < predio["width_mm"] and 0 < inicio["y"] < predio["depth_mm"]  # sobre o telhado
    filtro = next(c for c in layout["bim_components"] if c["instance_id"] == "FP-01")["position_mm"]
    assert filtro["x"] < 0 < inicio["x"]  # corre do telhado para fora, em direção ao filtro
    # E o manifesto continua válido, com o trecho chegando ao topo do filtro.
    cena = build_volumetry({"project_name": "Telhado", **layout})
    assert any(s.key.startswith("T-01#") for s in cena.solids)
