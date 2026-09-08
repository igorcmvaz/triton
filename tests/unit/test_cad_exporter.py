"""Testes de integridade e intercâmbio das exportações CAD/BIM."""

import json

import ezdxf

from netuno.core.bim_exporter import build_bim_manifest, validate_bim_manifest
from netuno.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram


PROJECT = {
    "project_name": "Edifício Residencial Teste",
    "ref_code": "N5-2026-CAD-TEST",
    "organization": "Escritório Exemplo",
    "technical_responsible": "Responsável a validar — CREA 000000",
    "area": 250.0,
    "runoff": 0.85,
    "discard": 2.0,
    "lower_vol": 10000.0,
    "upper_vol": 1000.0,
    "tot_demand": 2500.0,
    "share": 45.0,
    "potential_pct": 48.0,
    "audit_context": {"climate_location": "Florianópolis / SC"},
}


def _read_clean(path):
    doc = ezdxf.readfile(path)
    auditor = doc.audit()
    assert not auditor.errors
    return doc


def test_generate_technical_a3_dxf(tmp_path):
    output = tmp_path / "technical.dxf"
    generate_project_dxf(PROJECT, str(output), mode="technical_a3")
    doc = _read_clean(output)
    assert doc.dxfversion == "AC1032"
    assert doc.header["$INSUNITS"] == 4
    assert {"00_folha_e_margem", "00_selo", "06_equipamentos", "08_cotas"} <= set(doc.layers.entries)
    text = " ".join(entity.dxf.text for entity in doc.modelspace().query("TEXT"))
    assert "ESCRITÓRIO EXEMPLO" in text
    assert "Responsável a validar" in text
    assert "250,0 m²" in text
    assert "10.000 Litros" in text
    assert "UNIVERSIDADE FEDERAL" not in text
    # Verificações dos ajustes solicitados pelo usuário:
    # 1. Inclinação do telhado deixada em branco
    assert "i = ___%" in text
    assert "i = 30%" not in text
    # 2. Cisterna com texto limpo (sem Economia Estimada)
    assert "Cisterna: 10.000 L" in text
    assert "Economia Estimada:" not in text
    # 3. Sucção e recalque com quebra de linha (textos separados)
    texts_list = [e.dxf.text for e in doc.modelspace().query("TEXT")]
    assert "Sucção" in texts_list
    assert any(t.startswith("DN ") for t in texts_list)
    assert "Recalque" in texts_list
    # 4. Distribuição sem diâmetro (apenas DISTRIBUIÇÃO NÃO POTÁVEL)
    assert "DISTRIBUIÇÃO NÃO POTÁVEL" in texts_list
    assert not any("DISTRIBUIÇÃO DN" in t for t in texts_list)
    # 5. Backup potável
    assert "BACKUP POTÁVEL (AIR-GAP >= 50 mm)" in text
    # 6. Sem símbolo de norte
    inserts = [e.dxf.name for e in doc.modelspace().query("INSERT")]
    assert "SIMBOLO_NORTE" not in inserts


def test_generate_simple_dxf_and_svg(tmp_path):
    output = tmp_path / "simple.dxf"
    generate_project_dxf(PROJECT, str(output), mode="simple")
    doc = _read_clean(output)
    assert doc.header["$INSUNITS"] == 4
    text = " ".join(entity.dxf.text for entity in doc.modelspace().query("TEXT"))
    assert "ESQUEMA UNIFILAR" in text
    assert "Escritório Exemplo" in text
    svg = generate_project_svg_diagram(PROJECT, mode="simple")
    assert "<svg" in svg and "Escritório Exemplo" in svg
    assert "Igor Catão" not in svg


def test_fractional_share_from_web_is_normalised():
    data = dict(PROJECT)
    data["share"] = 0.45
    data["audit_context"] = None
    svg = generate_project_svg_diagram(data, mode="technical_a3")
    assert "1.125 L/dia (45%)" in svg
    assert "NÃO INFORMADA" in svg


def test_block_library_is_reusable_and_auditable(tmp_path):
    output = tmp_path / "biblioteca.dxf"
    generate_project_dxf(PROJECT, str(output), mode="block_library")
    doc = _read_clean(output)
    names = set(doc.blocks.block_names())
    expected = {
        "netuno_cisterna_planta", "netuno_res_sup_planta", "netuno_filtro_pluvial",
        "netuno_first_flush", "netuno_motobomba", "netuno_reg_gaveta",
        "netuno_reg_esfera", "netuno_valv_retencao", "netuno_air_gap",
        "netuno_ladrao_sifonado", "netuno_ponto_nao_potavel",
    }
    assert expected <= names
    assert len(doc.modelspace().query("INSERT")) == len(expected)
    for name in expected:
        entities = list(doc.blocks.get(name))
        assert any(entity.dxftype() == "ATTDEF" for entity in entities)
        assert all(entity.dxf.layer == "0" for entity in entities)
    for insert in doc.modelspace().query("INSERT"):
        assert insert.has_xdata("NETUNO5")

    manifest_path = output.with_name("biblioteca_netuno-bim.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0"
    assert len(manifest["component_types"]) == 11
    assert manifest["instances"] == []
    assert validate_bim_manifest(manifest) == []


def test_bim_manifest_preserves_explicit_placements():
    data = dict(PROJECT)
    data["bim_components"] = [{
        "instance_id": "CI-01",
        "type_id": "cisterna_inferior",
        "level": "Térreo",
        "position_mm": {"x": 12500, "y": 8200, "z": 0},
        "rotation_deg": 90,
        "parameters": {"CAPACIDADE_L": 10000},
    }]
    manifest = build_bim_manifest(data)
    assert manifest["instances"][0]["position_mm"]["x"] == 12500.0
    assert manifest["instances"][0]["parameters"]["CAPACIDADE_L"] == 10000
    assert validate_bim_manifest(manifest) == []


def test_invalid_cad_mode_is_rejected(tmp_path):
    try:
        generate_project_dxf(PROJECT, str(tmp_path / "bad.dxf"), mode="unknown")
    except ValueError as error:
        assert "Modo CAD inválido" in str(error)
    else:
        raise AssertionError("Modo desconhecido deveria ser rejeitado")


def test_forchheimer_calculation_and_materials_list(tmp_path):
    from netuno.core.cad_exporter import calculate_forchheimer_pumping_diameters

    # 1. Teste da função de cálculo da fórmula de Forchheimer
    calc = calculate_forchheimer_pumping_diameters(
        pump_flow_rate_m3_h=3.6,
        daily_pumped_volume_l=2500.0,
        pump_hp="3/4",
    )
    assert calc["dn_rec"] in (25, 32, 40)
    assert calc["dn_suc"] > calc["dn_rec"]
    assert calc["v_rec"] < 2.5
    assert calc["v_suc"] < 1.5

    # 2. Teste da prancha técnica DXF gerada
    output = tmp_path / "prancha_forchheimer.dxf"
    generate_project_dxf(PROJECT, str(output), mode="technical_a3")
    doc = _read_clean(output)
    text = " ".join(entity.dxf.text for entity in doc.modelspace().query("TEXT"))

    assert "Conf. Projeto" in text
    assert "ECONÔMICO" in text or "Econômico" in text
    assert "Recalque" in text
    assert "Sucção" in text or "SUCÇÃO" in text

    # 3. Teste do SVG da prancha técnica
    svg = generate_project_svg_diagram(PROJECT, mode="technical_a3")
    assert "Conf. Projeto" in svg
    assert "ECONÔMICO" in svg or "Econômico" in svg
    assert "Recalque" in svg
    assert "Sucção" in svg or "SUCÇÃO" in svg
