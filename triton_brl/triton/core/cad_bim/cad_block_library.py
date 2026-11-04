"""Biblioteca CAD de blocos Triton para inserção em plantas, em escala 1:1 mm."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

from triton.core.bim_exporter import COMPONENT_TYPES, write_bim_manifest


APP_ID = "TRITON"
BLOCK_LIBRARY_VERSION = "1.0"


def _number(value: Any, default: float) -> float:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        return float(value)
    except (TypeError, ValueError):
        return default


def configure_cad_document(doc) -> None:
    """Declara unidades e variáveis mínimas para intercâmbio previsível."""
    doc.units = units.MM
    doc.header["$INSUNITS"] = units.MM
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LUNITS"] = 2
    doc.header["$LUPREC"] = 2
    if APP_ID not in doc.appids:
        doc.appids.add(APP_ID)


def _add_attributes(block, specs: Iterable[Tuple[str, str, Tuple[float, float]]]) -> None:
    for tag, default, point in specs:
        # Somente o identificador aparece por padrão na planta. Os demais
        # atributos continuam editáveis/extraíveis, mas não poluem o desenho.
        flags = 0 if tag == "ID" else 1
        block.add_attdef(tag, point, default, height=90, dxfattribs={"layer": "0", "prompt": tag, "flags": flags})


def _new_block(doc, name: str):
    return doc.blocks.get(name) if name in doc.blocks else doc.blocks.new(name=name, base_point=(0, 0))


def register_plan_blocks(doc) -> None:
    """Registra símbolos 2D paramétricos por atributos, todos com origem funcional."""
    configure_cad_document(doc)

    b = _new_block(doc, "TRITON_CISTERNA_PLANTA")
    if not list(b):
        b.add_circle((0, 0), 1000, dxfattribs={"layer": "0"})
        b.add_circle((0, 0), 850, dxfattribs={"layer": "0"})
        b.add_line((-1000, 0), (1000, 0), dxfattribs={"layer": "0"})
        b.add_text("CI", height=220, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "CI-01", (-1000, -1250)), ("CAPACIDADE_L", "5000", (-1000, -1370))])

    b = _new_block(doc, "TRITON_RES_SUP_PLANTA")
    if not list(b):
        b.add_lwpolyline([(-600, -600), (600, -600), (600, 600), (-600, 600)], close=True, dxfattribs={"layer": "0"})
        b.add_line((-600, -600), (600, 600), dxfattribs={"layer": "0"})
        b.add_line((-600, 600), (600, -600), dxfattribs={"layer": "0"})
        b.add_text("RS", height=180, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "RS-01", (-600, -850)), ("CAPACIDADE_L", "500", (-600, -970))])

    b = _new_block(doc, "TRITON_FILTRO_PLUVIAL")
    if not list(b):
        b.add_lwpolyline([(-400, -300), (400, -300), (400, 300), (-400, 300)], close=True, dxfattribs={"layer": "0"})
        for x in (-250, -125, 0, 125, 250):
            b.add_line((x - 100, -250), (x + 100, 250), dxfattribs={"layer": "0"})
        b.add_text("FP", height=150, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "FP-01", (-400, -520)), ("DN_MM", "100", (-400, -640)), ("MALHA_MM", "1.0", (-400, -760))])

    b = _new_block(doc, "TRITON_FIRST_FLUSH")
    if not list(b):
        b.add_circle((0, 0), 350, dxfattribs={"layer": "0"})
        b.add_line((0, 350), (0, 700), dxfattribs={"layer": "0"})
        b.add_line((0, -350), (0, -650), dxfattribs={"layer": "0"})
        b.add_text("FF", height=150, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "FF-01", (-350, -850)), ("VOLUME_L", "300", (-350, -970)), ("DESCARTE_MM", "2.0", (-350, -1090))])

    b = _new_block(doc, "TRITON_MOTOBOMBA")
    if not list(b):
        b.add_circle((0, 0), 300, dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-380, -300), (380, -300), (480, -430), (-480, -430)], close=True, dxfattribs={"layer": "0"})
        b.add_text("B", height=180, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "B-01", (-480, -620)), ("POTENCIA_KW", "0.37", (-480, -740)), ("VAZAO_L_MIN", "0", (-480, -860)), ("ALTURA_MCA", "0", (-480, -980))])

    for name, label, extra in (
        ("TRITON_REG_GAVETA", "RG", [("DN_MM", "25", (-300, -500))]),
        ("TRITON_REG_ESFERA", "RE", [("DN_MM", "25", (-300, -500))]),
    ):
        b = _new_block(doc, name)
        if not list(b):
            b.add_line((-300, -200), (300, 200), dxfattribs={"layer": "0"})
            b.add_line((-300, 200), (300, -200), dxfattribs={"layer": "0"})
            b.add_line((-300, -200), (-300, 200), dxfattribs={"layer": "0"})
            b.add_line((300, -200), (300, 200), dxfattribs={"layer": "0"})
            if name.endswith("ESFERA"):
                b.add_circle((0, 0), 90, dxfattribs={"layer": "0"})
            b.add_text(label, height=90, dxfattribs={"layer": "0"}).set_placement((0, 320), align=TextEntityAlignment.BOTTOM_CENTER)
            _add_attributes(b, [("ID", f"{label}-01", (-300, -380)), *extra])

    b = _new_block(doc, "TRITON_VALV_RETENCAO")
    if not list(b):
        b.add_lwpolyline([(-300, -220), (300, -220), (300, 220), (-300, 220)], close=True, dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-220, -180), (160, 0), (-220, 180)], close=True, dxfattribs={"layer": "0"})
        b.add_line((180, -180), (180, 180), dxfattribs={"layer": "0"})
        _add_attributes(b, [("ID", "VR-01", (-300, -410)), ("DN_MM", "25", (-300, -530))])

    b = _new_block(doc, "TRITON_AIR_GAP")
    if not list(b):
        b.add_line((-350, 350), (0, 350), dxfattribs={"layer": "0"})
        b.add_line((0, 350), (0, 100), dxfattribs={"layer": "0"})
        b.add_line((-400, -100), (400, -100), dxfattribs={"layer": "0"})
        b.add_line((-400, -100), (-400, -450), dxfattribs={"layer": "0"})
        b.add_line((400, -100), (400, -450), dxfattribs={"layer": "0"})
        b.add_line((-120, 100), (120, 100), dxfattribs={"layer": "0", "linetype": "DASHED"})
        _add_attributes(b, [("ID", "AG-01", (-400, -620)), ("FOLGA_MM", "50", (-400, -740)), ("DN_MM", "20", (-400, -860))])

    b = _new_block(doc, "TRITON_LADRAO_SIFONADO")
    if not list(b):
        b.add_lwpolyline([(-600, 200), (-100, 200), (-100, -300), (250, -300), (250, 0), (650, 0)], dxfattribs={"layer": "0"})
        b.add_line((650, -130), (650, 130), dxfattribs={"layer": "0"})
        b.add_line((610, -100), (690, 100), dxfattribs={"layer": "0"})
        b.add_line((610, 100), (690, -100), dxfattribs={"layer": "0"})
        _add_attributes(b, [("ID", "LS-01", (-600, -500)), ("DN_MM", "100", (-600, -620)), ("MALHA_MM", "0.5", (-600, -740))])

    b = _new_block(doc, "TRITON_PONTO_NAO_POTAVEL")
    if not list(b):
        b.add_circle((0, 0), 250, dxfattribs={"layer": "0"})
        b.add_line((-175, -175), (175, 175), dxfattribs={"layer": "0"})
        b.add_line((-175, 175), (175, -175), dxfattribs={"layer": "0"})
        b.add_text("NP", height=100, dxfattribs={"layer": "0"}).set_placement((0, 340), align=TextEntityAlignment.BOTTOM_CENTER)
        _add_attributes(b, [("ID", "NP-01", (-250, -430)), ("USO", "A DEFINIR", (-250, -550)), ("DN_MM", "20", (-250, -670))])

    # Freio d'água: curva 90° no fundo da cisterna com o bocal voltado para cima.
    b = _new_block(doc, "TRITON_FREIO_DAGUA")
    if not list(b):
        b.add_lwpolyline([(-80, 500), (-80, 80), (0, 0), (300, 0)], dxfattribs={"layer": "0"})
        b.add_lwpolyline([(80, 500), (80, 160), (300, 160)], dxfattribs={"layer": "0"})
        b.add_line((300, -40), (300, 200), dxfattribs={"layer": "0"})
        b.add_text("FR", height=90, dxfattribs={"layer": "0"}).set_placement((0, 560), align=TextEntityAlignment.BOTTOM_CENTER)
        _add_attributes(b, [("ID", "FR-01", (-300, -250)), ("DN_MM", "100", (-300, -370))])

    # Sucção flutuante: boia com o crivo pendurado a ~15 cm da lâmina.
    b = _new_block(doc, "TRITON_SUCCAO_FLUTUANTE")
    if not list(b):
        b.add_circle((0, 150), 180, dxfattribs={"layer": "0"})
        b.add_line((0, -30), (0, -250), dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-90, -250), (90, -250), (90, -420), (-90, -420)], close=True, dxfattribs={"layer": "0"})
        b.add_line((-90, -335), (90, -335), dxfattribs={"layer": "0", "linetype": "DASHED"})
        _add_attributes(b, [("ID", "SF-01", (-300, -560)), ("DN_MM", "32", (-300, -680)), ("PROFUNDIDADE_MM", "150", (-300, -800))])

    # Chave de nível (boia elétrica) que comanda bomba e solenoide.
    b = _new_block(doc, "TRITON_SENSOR_NIVEL")
    if not list(b):
        b.add_line((0, 400), (0, 120), dxfattribs={"layer": "0"})
        b.add_ellipse((0, 0), major_axis=(0, 120), ratio=0.6, dxfattribs={"layer": "0"})
        b.add_text("LS", height=90, dxfattribs={"layer": "0"}).set_placement((0, 440), align=TextEntityAlignment.BOTTOM_CENTER)
        _add_attributes(b, [("ID", "SN-01", (-300, -250)), ("FUNCAO", "NIVEL", (-300, -370))])

    # Válvula solenoide: corpo de válvula com o atuador elétrico (S) acima.
    b = _new_block(doc, "TRITON_VALV_SOLENOIDE")
    if not list(b):
        b.add_lwpolyline([(-300, -200), (300, 200), (300, -200), (-300, 200)], close=True, dxfattribs={"layer": "0"})
        b.add_line((0, 0), (0, 320), dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-130, 320), (130, 320), (130, 560), (-130, 560)], close=True, dxfattribs={"layer": "0"})
        b.add_text("S", height=150, dxfattribs={"layer": "0"}).set_placement((0, 440), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "VS-01", (-300, -420)), ("DN_MM", "25", (-300, -540)), ("TENSAO_V", "220", (-300, -660))])

    # Hidrômetro do ramal predial (entrada da rede pública).
    b = _new_block(doc, "TRITON_HIDROMETRO")
    if not list(b):
        b.add_line((-500, 0), (-220, 0), dxfattribs={"layer": "0"})
        b.add_line((220, 0), (500, 0), dxfattribs={"layer": "0"})
        b.add_circle((0, 0), 220, dxfattribs={"layer": "0"})
        b.add_text("HD", height=110, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "HD-01", (-500, -380)), ("DN_MM", "25", (-500, -500)), ("VAZAO_NOMINAL_M3_H", "1.5", (-500, -620))])

    # Válvula de pé com crivo: mantém a sucção escorvada e retém sólidos.
    b = _new_block(doc, "TRITON_VALV_PE_CRIVO")
    if not list(b):
        b.add_line((0, 500), (0, 200), dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-150, 200), (150, 200), (0, 50)], close=True, dxfattribs={"layer": "0"})
        b.add_lwpolyline([(-150, 50), (150, 50), (150, -300), (-150, -300)], close=True, dxfattribs={"layer": "0"})
        for x in (-75, 0, 75):
            b.add_line((x, 50), (x, -300), dxfattribs={"layer": "0", "linetype": "DASHED"})
        _add_attributes(b, [("ID", "VP-01", (-300, -450)), ("DN_MM", "32", (-300, -570))])

    # Respiro do reservatório: curva de 180° com tela contra insetos.
    b = _new_block(doc, "TRITON_RESPIRO")
    if not list(b):
        b.add_line((0, -300), (0, 300), dxfattribs={"layer": "0"})
        b.add_arc((150, 300), 150, 0, 180, dxfattribs={"layer": "0"})
        b.add_line((300, 300), (300, 150), dxfattribs={"layer": "0"})
        b.add_line((240, 150), (360, 150), dxfattribs={"layer": "0", "linetype": "DASHED"})
        _add_attributes(b, [("ID", "RP-01", (-300, -450)), ("DN_MM", "50", (-300, -570))])

    # Quadro de comando da motobomba.
    b = _new_block(doc, "TRITON_QUADRO_COMANDO")
    if not list(b):
        b.add_lwpolyline([(-300, -400), (300, -400), (300, 400), (-300, 400)], close=True, dxfattribs={"layer": "0"})
        b.add_line((-300, 250), (300, 250), dxfattribs={"layer": "0"})
        b.add_text("QC", height=150, dxfattribs={"layer": "0"}).set_placement((0, 0), align=TextEntityAlignment.MIDDLE_CENTER)
        _add_attributes(b, [("ID", "QC-01", (-300, -560)), ("TENSAO_V", "220", (-300, -680)), ("FUNCAO", "COMANDO", (-300, -800))])


def generate_block_library_dxf(project_data: Dict[str, Any], output_path: str) -> str:
    """Gera catálogo DXF auditável e um manifesto BIM JSON com o mesmo nome-base."""
    doc = ezdxf.new(dxfversion="R2018", setup=True, units=units.MM)
    configure_cad_document(doc)
    for name, color, weight in (("TRITON_BLOCOS", 4, 35), ("TRITON_TEXTOS", 7, 18), ("TRITON_GUIAS", 8, 13)):
        if name not in doc.layers:
            doc.layers.add(name, color=color, lineweight=weight)
    register_plan_blocks(doc)
    msp = doc.modelspace()
    title = str(project_data.get("project_name") or "Projeto Triton")
    ref = str(project_data.get("ref_code") or "SEM-REFERENCIA")
    msp.add_text("TRITON — BIBLIOTECA DE BLOCOS PARA PLANTAS", height=260, dxfattribs={"layer": "TRITON_TEXTOS"}).set_placement((0, 3500))
    msp.add_text(f"Projeto: {title} | Ref.: {ref} | Unidades: mm | Blocos em escala 1:1", height=140, dxfattribs={"layer": "TRITON_TEXTOS"}).set_placement((0, 3150))
    msp.add_text("Geometria esquemática. Confirmar dimensões, famílias e especificações no projeto executivo.", height=120, dxfattribs={"layer": "TRITON_TEXTOS"}).set_placement((0, 2850))

    lower_volume = _number(project_data.get("lower_vol"), 5000.0)
    upper_volume = _number(project_data.get("upper_vol"), 500.0)
    discard_depth = _number(project_data.get("discard"), 2.0)
    catchment_area = _number(project_data.get("area"), 150.0)
    defaults = {
        "CAPACIDADE_L": str(round(lower_volume)),
        "DESCARTE_MM": str(discard_depth),
        "VOLUME_L": str(round(catchment_area * discard_depth)),
        "POTENCIA_KW": "0.37" if lower_volume <= 10000 else "0.55",
    }
    for index, item in enumerate(COMPONENT_TYPES):
        col, row = index % 4, index // 4
        x, y = col * 3500.0, 1800.0 - row * 3000.0
        values = {"ID": f"NET-{index + 1:02d}"}
        values.update({key: defaults.get(key, "0") for key in item["parameters"]})
        if item["type_id"] == "reservatorio_superior":
            values["CAPACIDADE_L"] = str(round(upper_volume))
        insert = msp.add_blockref(item["cad_block"], (x, y), dxfattribs={"layer": "TRITON_BLOCOS"})
        insert.add_auto_attribs(values)
        insert.set_xdata(APP_ID, [(1000, item["type_id"]), (1000, BLOCK_LIBRARY_VERSION), (1000, ref)])
        msp.add_text(f"{item['cad_block']}  |  base: 0,0", height=115, dxfattribs={"layer": "TRITON_TEXTOS"}).set_placement((x - 1100, y - 1500))

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    from triton.core.dados_do_relatorio import documento_dxf_de_exportacao
    documento_dxf_de_exportacao(doc)
    doc.saveas(path)
    write_bim_manifest(project_data, str(path.with_name(path.stem + "_triton-bim.json")))
    return str(path)
