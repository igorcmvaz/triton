"""Testes para geração de layout 3D a partir dos dados do estudo."""

import pytest

from netuno.core.bim_exporter import build_bim_manifest, validate_bim_manifest
from netuno.core.schematic_3d import generate_schematic_3d_svg
from netuno.core.study_layout import generate_study_layout
from netuno.core.volumetry import build_volumetry

#: Arranjo gerado pelo estudo, na ordem do manifesto.
ARRANJO = ["FP-01", "FF-01", "CI-01", "B-01", "RS-01",
           "FR-01", "SF-01", "VP-01", "SN-01", "RP-01", "LS-01",
           "RG-03", "VR-01", "RG-01", "QC-01",
           "SN-02", "SN-03", "RP-02", "AG-01",
           "HD-01", "RG-02", "VS-01",
           "RG-05", "RG-04", "VR-02", "PNP-01"]

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
    comp_ids = [c["instance_id"] for c in layout["bim_components"]]
    assert comp_ids == ARRANJO
    assert len(layout["pipe_runs"]) == 19
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
    assert [c["instance_id"] for c in layout["bim_components"]] == ARRANJO
    manifest = build_bim_manifest(layout)
    assert validate_bim_manifest(manifest) == []
    assert manifest["validation"]["warnings"] == []


@pytest.mark.parametrize("volume, area, pavimentos, caixa", [
    (1500, 60, 1, 500), (5000, 150, 2, 1000), (10000, 180, 3, 1000), (30000, 400, 6, 3000), (2000, 400, 1, 3000),
])
def test_o_arranjo_normativo_fecha_sem_erros_nem_avisos(volume, area, pavimentos, caixa):
    """Da cisterna pequena ao prédio: todo trecho chega onde declara, sem colisão."""
    layout = generate_study_layout({"lower_vol": volume, "area": area, "floors": pavimentos, "upper_vol": caixa})
    manifest = build_bim_manifest({"project_name": "Grade", **layout})
    assert validate_bim_manifest(manifest) == []
    assert manifest["validation"]["warnings"] == []


def test_o_arranjo_tem_o_que_a_instalacao_pede():
    """Freio d'água, sucção flutuante, extravasor, retenção e o backup potável."""
    layout = generate_study_layout({"lower_vol": 10000, "area": 180, "floors": 2})
    tipos = {c["instance_id"]: c["type_id"] for c in layout["bim_components"]}
    trechos = {r["run_id"]: r for r in layout["pipe_runs"]}
    # Entrada calma: a captação termina no freio d'água, dentro da cisterna.
    assert tipos["FR-01"] == "freio_dagua" and trechos["T-03"]["end"] == "FR-01:topo"
    # A bomba puxa pela válvula de pé com crivo, pendurada na boia, e não pelo fundo.
    assert tipos["SF-01"] == "succao_flutuante" and tipos["VP-01"] == "valvula_pe_crivo"
    assert trechos["T-04"]["start"] == "VP-01:topo"
    # Registro de manutenção dos dois lados da bomba; retenção no recalque.
    assert [trechos[t]["start"] for t in ("T-05", "T-06", "T-07", "T-08")] == ["RG-03", "B-01", "VR-01", "RG-01"]
    assert tipos["RG-03"] == tipos["RG-01"] == "registro_gaveta" and tipos["VR-01"] == "valvula_retencao"
    # Extravasor da cisterna: ladrão sifonado e antirrefluxo antes da rede pluvial.
    assert trechos["T-11"]["end"] == "LS-01:sup+y" and trechos["T-12"]["end"] == "VR-02"
    # Caixa superior: registro na saída, extravasor com aviso, limpeza com registro.
    assert trechos["T-09"]["start"] == "RS-01:inf-y" and trechos["T-09"]["end"] == "RG-05"
    assert trechos["T-10"]["end"] == "PNP-01:topo"
    assert trechos["T-14"]["start"] == "RS-01:sup+y" and trechos["T-14"]["system"] == "extravasor"
    assert trechos["T-15"]["start"] == "RS-01:inf+x" and trechos["T-15"]["end"] == "RG-04"
    # Respiros com tela nas duas caixas, e o quadro de comando junto à bomba.
    assert tipos["RP-01"] == tipos["RP-02"] == "respiro" and tipos["QC-01"] == "quadro_comando"
    # Backup potável: hidrômetro → registro → solenoide → air gap sobre a caixa.
    potavel = [r for r in layout["pipe_runs"] if r["system"] == "alimentacao_potavel"]
    assert [r["start"] for r in potavel] == ["HD-01", "RG-02", "VS-01"]
    assert potavel[-1]["end"] == "AG-01:topo" and tipos["VS-01"] == "valvula_solenoide"
    # Chaves de nível: cisterna, e duas na caixa (partida acima, backup abaixo).
    assert tipos["SN-01"] == tipos["SN-02"] == tipos["SN-03"] == "sensor_nivel"
    cota = {c["instance_id"]: c["position_mm"]["z"] for c in layout["bim_components"]}
    assert cota["SN-03"] < cota["SN-02"]


def test_o_comando_aparece_como_cabos_do_quadro_e_logica_na_ficha():
    """Boias → quadro → bomba e solenoide: é assim que o backup sabe quando abrir."""
    layout = generate_study_layout({"lower_vol": 10000, "area": 180, "floors": 2})
    cena = build_volumetry({"project_name": "Comando", **layout})
    ligacoes = {s.group for s in cena.solids if s.kind == "cable"}
    assert ligacoes == {"CABO SN-01-QC-01", "CABO SN-02-QC-01", "CABO SN-03-QC-01",
                        "CABO QC-01-B-01", "CABO QC-01-VS-01"}
    quadro = next(s for s in cena.solids if s.key == "QC-01")
    ficha = " ".join(quadro.info)
    assert "Lógica de comando" in ficha and "abre a solenoide" in ficha and "Intertravamento" in ficha

    # Sem quadro de comando, não há cabos inventados.
    sem_quadro = dict(layout, bim_components=[c for c in layout["bim_components"] if c["type_id"] != "quadro_comando"])
    assert not [s for s in build_volumetry({"project_name": "x", **sem_quadro}).solids if s.kind == "cable"]


def test_as_valvulas_seguem_a_direcao_do_trecho():
    """As peças do backup correm em y: giro de 90°, senão ficam atravessadas no tubo."""
    layout = generate_study_layout({"lower_vol": 10000, "area": 180, "floors": 2})
    giro = {c["instance_id"]: c["rotation_deg"] for c in layout["bim_components"]}
    assert giro["HD-01"] == giro["RG-02"] == giro["VS-01"] == giro["RG-05"] == giro["VR-02"] == 90.0
    assert giro["VR-01"] == giro["RG-01"] == giro["RG-03"] == 0.0  # recalque e sucção correm em x


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


def test_a_prancha_do_arranjo_completo_nao_embola():
    """Um plano de cota por nível principal, e o tipo das peças pequenas vai para a tabela."""
    import re

    layout = generate_study_layout({"lower_vol": 10000, "upper_vol": 1000, "area": 180, "floors": 2})
    svg = generate_schematic_3d_svg({"project_name": "Prancha", **layout})
    cotas = re.findall(r">Cota ([^<]+) m<", svg)
    assert len(cotas) <= 6, cotas  # eram 14, um por acessório
    assert "Peças e acessórios" in svg
    # As 21 peças pequenas aparecem no desenho só pelo código.
    assert svg.count("Registro de gaveta ·") == 5  # uma vez cada, na tabela
    assert 'width="1680" height="1188"' in svg  # folha A3 deitada
