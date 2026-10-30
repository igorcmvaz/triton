"""
Módulo Core de Exportação de Esquemas Técnicos em CAD (DXF) e Vetorial (SVG).
Utiliza a biblioteca de engenharia `ezdxf` para gerar pranchas técnicas completas
no formato ABNT A3 (420 x 297 mm) em DXF R2018 (UTF-8) e diagramas esquemáticos
unifilares, em conformidade com as normas ABNT NBR 15527:2019, NBR 5626 e NBR 6492.

Os campos de instituição e responsabilidade técnica são dados do projeto; o
exportador não atribui autoria ou responsabilidade automaticamente.
"""

from triton.core.fracao_atendivel import fracao_para_percentual
from triton.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
import os
import math
from html import escape
from typing import Dict, Any, Optional
from datetime import datetime

import ezdxf
from ezdxf.enums import TextEntityAlignment
from triton.core.pump_hydraulics import vazao_l_por_h
from triton.core.pump_energy import CV_TO_KW

from .cad_block_library import configure_cad_document, generate_block_library_dxf
from .dados_do_relatorio import documento_dxf_de_exportacao, svg_de_exportacao
from .plant_3d import generate_plant_3d_dxf
from .schematic_3d import generate_schematic_3d_svg


def _safe_float(val: Any, default: float = 0.0) -> float:
    """Converte valores com segurança prevenindo erros em strings vazias, '-' ou nulas."""
    if val is None or val == "" or val == "-":
        return default
    try:
        if isinstance(val, str):
            from triton.core.numero import usa_ponto_decimal, normalizar
            if usa_ponto_decimal():
                val = normalizar(val)
            else:
                val = val.replace(".", "").replace(",", ".") if val.count(",") == 1 and val.count(".") > 1 else val.replace(",", ".").strip()
        return float(val)
    except (ValueError, TypeError):
        return default


#: O que a prancha escreve quando o projeto não traz o dado.
NAO_INFORMADO = "Não informado"
NAO_CALCULADO = "Não calculado"


def _presente(val: Any) -> bool:
    """O dado veio do projeto (número maior que zero)? «-», vazio e None não vieram."""
    return _safe_float(val, 0.0) > 0


def demanda_total_do_desenho(project_data: Dict[str, Any]) -> Optional[float]:
    """Demanda total diária da edificação, L/dia: a do estudo, ou moradores × per capita.

    ``None`` quando o projeto não a traz. A prancha escrevia 1.000 L/dia, valor de
    nenhum projeto, e dimensionava o recalque com ele.
    """
    total = _safe_float(project_data.get("tot_demand"), 0.0)
    if total > 0:
        return total
    moradores = _safe_float(project_data.get("residents"), 0.0)
    per_capita = _safe_float(project_data.get("demand"), 0.0)
    return moradores * per_capita if moradores > 0 and per_capita > 0 else None


def textos_do_quadro(project_data: Dict[str, Any]) -> Dict[str, str]:
    """Os valores do quadro de parâmetros, como texto: o do projeto, ou «Não informado».

    Área, volume e potencial que faltam não viram 150 m², 5.000 L e 42,5%.
    """
    area = _safe_float(project_data.get("area"), 0.0)
    vol = _safe_float(project_data.get("lower_vol"), 0.0)
    pot = project_data.get("potential_pct")
    pot_ok = pot not in (None, "", "-") and _safe_float(pot, -1.0) >= 0
    dem = demanda_total_do_desenho(project_data)
    share_pct = fracao_para_percentual("A fração atendível", _safe_float(project_data.get("share"), 0.0))
    return {
        "area": f"{_fmt_ptbr(area, 1)} m²" if area > 0 else NAO_INFORMADO,
        "area_int": f"{_fmt_milhar(area)} m²" if area > 0 else NAO_INFORMADO,
        "volume": f"{_fmt_milhar(vol)} Litros" if vol > 0 else NAO_INFORMADO,
        "volume_l": f"{_fmt_milhar(vol)} L" if vol > 0 else NAO_INFORMADO,
        "potencial": f"{_fmt_ptbr(_safe_float(pot), 1)} %" if pot_ok else NAO_CALCULADO,
        "potencial_curto": f"{_fmt_ptbr(_safe_float(pot), 1)}%" if pot_ok else NAO_CALCULADO,
        "demanda": f"{_fmt_milhar(dem)} L/dia" if dem else NAO_INFORMADO,
        "alvo": (f"{_fmt_milhar(dem * share_pct / 100.0)} L/dia ({_fmt_milhar(share_pct)}%)"
                 if dem and share_pct > 0 else NAO_INFORMADO),
    }


def _fmt_ptbr(val: float, decimals: int = 1) -> str:
    """Formata número com vírgula como separador decimal (padrão brasileiro ABNT)."""
    return f"{val:.{decimals}f}".replace(".", ",")


def _fmt_milhar(val: float) -> str:
    """Formata valor inteiro com ponto como separador de milhar (ex: 5.000)."""
    return f"{int(round(val)):,}".replace(",", ".")


def _extract_upper_vol(project_data: Dict[str, Any], default: float = 500.0) -> float:
    """Extrai com fidelidade a capacidade do reservatório superior configurado pelo projetista."""
    if not project_data:
        return default
    # 1. Chaves diretas de primeiro nível
    for k in ("upper_vol", "upper_volume", "upper_volume_l", "upper_tank_vol", "upper_tank_volume_l"):
        val = project_data.get(k)
        if val is not None:
            f_val = _safe_float(val, 0.0)
            if f_val > 0:
                return f_val
    # 2. Chaves aninhadas em subestruturas (system_design, technical_design, optima)
    for nest_key in ("system_design", "technical_design", "optima"):
        nested = project_data.get(nest_key)
        if isinstance(nested, dict):
            for k in ("upper_volume_l", "upper_vol", "upper_volume", "upper_tank_vol", "upper_tank_volume_l"):
                val = nested.get(k)
                if val is not None:
                    f_val = _safe_float(val, 0.0)
                    if f_val > 0:
                        return f_val
    return default


def calculate_forchheimer_pumping_diameters(
    pump_flow_rate_m3_h: float = 0.0,
    daily_pumped_volume_l: float = 1000.0,
    pump_hp: str = "1/2",
) -> Dict[str, Any]:
    """
    Calcula os diâmetros econômicos de recalque e sucção pela Fórmula de Forchheimer (NBR 5626 / NBR 12214).

    Fórmula de Forchheimer:
        D_rec = 1,3 · (T / 24)^0,25 · √Q

    Onde:
        - Q: Vazão de recalque da motobomba em m³/s
        - T: Horas de funcionamento diário (h/dia)
        - D_rec: Diâmetro interno teórico em metros

    Critério de Sucção (ABNT NBR 5626 / NBR 12214):
        - Adota-se o diâmetro comercial de bitola imediatamente superior ao recalque (DN_suc > DN_rec)
          para limitar as perdas de carga e manter a velocidade v_suc <= 1,0 a 1,5 m/s, prevenindo
          cavitação (NPSH) e desgaste prematuro da motobomba.
    """
    # 1. Vazão de bombeamento Q (m³/h -> m³/s)
    q_m3_h = float(pump_flow_rate_m3_h or 0.0)
    if q_m3_h <= 0.05:
        # A vazao vem da equacao da bomba, e nao de uma tabela propria deste
        # modulo. Antes desta revisao havia aqui uma segunda tabela - 2,4 m3/h
        # para meio CV - que discordava dos 2.280 L/h usados no calculo de
        # energia para a mesma bomba.
        potencias_cv = [
            ("1 1/2", 1.5), ("1.5", 1.5), ("3/4", 0.75), ("0.75", 0.75),
            ("1/2", 0.5), ("0.5", 0.5), ("2", 2.0), ("1", 1.0),
        ]
        hp_str = str(pump_hp).strip()
        cv = next((v for k, v in potencias_cv if k in hp_str), 0.5)
        q_m3_h = vazao_l_por_h(cv * CV_TO_KW) / 1000.0

    q_m3_s = q_m3_h / 3600.0
    q_l_s = q_m3_s * 1000.0

    # 2. Horas de funcionamento diário da bomba T (h/dia)
    vol_l = float(daily_pumped_volume_l or 0.0)
    if vol_l > 0 and q_m3_h > 0:
        t_hours = vol_l / (q_m3_h * 1000.0)
        t_hours = max(0.5, min(24.0, t_hours))
    else:
        t_hours = 3.5

    # 3. Fórmula de Forchheimer: D_rec = 1.3 * (T/24)^0.25 * sqrt(Q)
    factor_t = (t_hours / 24.0) ** 0.25
    d_rec_calc_m = 1.3 * factor_t * math.sqrt(q_m3_s)
    d_rec_calc_mm = d_rec_calc_m * 1000.0

    # 4. Série Comercial de Tubos PVC Soldável Água Fria (NBR 5626)
    # (DN nominal mm, diâmetro interno aproximado mm, bitola comercial polegadas)
    pvc_sizes = [
        (20, 17.0, '1/2"'),
        (25, 21.6, '3/4"'),
        (32, 27.8, '1"'),
        (40, 35.2, '1 1/4"'),
        (50, 44.0, '1 1/2"'),
        (60, 53.4, '2"'),
        (75, 66.6, '2 1/2"'),
        (85, 76.2, '3"'),
        (110, 98.8, '4"'),
    ]

    # Seleção de Recalque: menor bitola cujo diâmetro interno atenda satisfatoriamente
    # e cuja velocidade de escoamento respeite os limites normativos da NBR 5626 (v <= 2.2 m/s)
    dn_rec = 25
    di_rec = 21.6
    pol_rec = '3/4"'
    rec_idx = 1
    for idx, (dn, di, pol) in enumerate(pvc_sizes):
        area_test = math.pi * ((di / 1000.0) ** 2) / 4.0
        v_test = q_m3_s / area_test if area_test > 0 else 99.0
        if di >= d_rec_calc_mm * 0.90 and v_test <= 2.2:
            dn_rec = dn
            di_rec = di
            pol_rec = pol
            rec_idx = idx
            break

    # Normas de instalações prediais recomendam diâmetro mínimo de DN 25 para linhas pressurizadas
    if dn_rec < 25:
        dn_rec = 25
        di_rec = 21.6
        pol_rec = '3/4"'
        rec_idx = 1

    area_rec = math.pi * ((di_rec / 1000.0) ** 2) / 4.0
    v_rec = q_m3_s / area_rec if area_rec > 0 else 0.0

    # Seleção de Sucção: imediatamente superior ao recalque (DN_suc > DN_rec)
    if rec_idx + 1 < len(pvc_sizes):
        dn_suc, di_suc, pol_suc = pvc_sizes[rec_idx + 1]
    else:
        dn_suc, di_suc, pol_suc = pvc_sizes[rec_idx]

    if dn_suc < 32:
        dn_suc = 32
        di_suc = 27.8
        pol_suc = '1"'

    area_suc = math.pi * ((di_suc / 1000.0) ** 2) / 4.0
    v_suc = q_m3_s / area_suc if area_suc > 0 else 0.0

    return {
        "q_m3_h": q_m3_h,
        "q_l_s": q_l_s,
        "t_hours": t_hours,
        "d_rec_calc_mm": d_rec_calc_mm,
        "dn_rec": dn_rec,
        "di_rec_mm": di_rec,
        "pol_rec": pol_rec,
        "v_rec": v_rec,
        "dn_suc": dn_suc,
        "di_suc_mm": di_suc,
        "pol_suc": pol_suc,
        "v_suc": v_suc,
        "formula_str": "D = 1,3 · (T/24)^0,25 · √Q",
    }


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DE LAYERS E ESTILOS NORMATIVOS ABNT
# ─────────────────────────────────────────────────────────────────────────────

def _setup_abnt_layers(doc: ezdxf.document.Drawing):
    """
    Configura a tabela de Layers com cores ACI e espessuras normativas (NBR 6492).
    Lineweights em centésimos de milímetro (ex: 70 = 0.70 mm, 50 = 0.50 mm).
    """
    layers_config = [
        ("00_FOLHA_E_MARGEM", 7, 70),       # Borda externa A3 e margem interna (0.70 mm)
        ("00_SELO", 7, 35),                 # Selo e carimbo técnico ABNT (0.35 mm)
        ("01_ALVENARIA_COBERTURA", 8, 35),   # Telhado, calha e estruturas civis (0.35 mm cinza/branco)
        ("02_TUB_PLUVIAL_BRUTA", 3, 50),     # Condutores e filtro (0.50 mm Verde)
        ("03_TUB_RECALQUE", 30, 50),         # Prumada de recalque da bomba (0.50 mm Laranja)
        ("04_TUB_DISTRIBUICAO", 6, 35),      # Ramais de água não potável (0.35 mm Magenta)
        ("05_TUB_EXTRAVASOR_DRENO", 1, 35),  # Extravasores, ladrão e dreno (0.35 mm Vermelho)
        ("06_EQUIPAMENTOS", 4, 35),          # Bomba, cisterna e caixas d'água (0.35 mm Ciano)
        ("07_HACHURAS", 8, 18),              # Concreto, água e hachuras (0.18 mm Cinza)
        ("08_COTAS", 2, 18),                 # Linhas de cota e medidas (0.18 mm Amarelo)
        ("09_TEXTOS_E_NOTAS", 7, 25),        # Anotações gerais e notas de norma (0.25 mm Branco)
        ("10_LEGENDA_E_QUADROS", 7, 25),     # Quadros de dimensionamento e materiais (0.25 mm)
    ]
    for name, color, lweight in layers_config:
        if name not in doc.layers:
            doc.layers.add(name, color=color, lineweight=lweight)


def _setup_technical_blocks(doc: ezdxf.document.Drawing):
    """
    Registra os símbolos usados internamente nas pranchas técnicas:
    - Válvulas (gaveta, esfera, retenção)
    - Motobomba centrífuga
    - Freio d'água (dispersor de fundo)
    - Ladrão sifonado com tela
    - Símbolo de Norte

    A biblioteca reutilizável para plantas, incluindo filtro e air-gap, fica em
    ``cad_block_library.py`` e usa nomes prefixados por ``TRITON_``.
    """
    # 1. Bloco: REGISTRO DE GAVETA (Válvula gaveta)
    if "REGISTRO_GAVETA" not in doc.blocks:
        b = doc.blocks.new("REGISTRO_GAVETA")
        b.add_line((-2.5, -1.8), (2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-2.5, 1.8), (2.5, -1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-2.5, -1.8), (-2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((2.5, -1.8), (2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((0, 0), (0, 3.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-1.8, 3.0), (1.8, 3.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})

    # 2. Bloco: REGISTRO DE ESFERA
    if "REGISTRO_ESFERA" not in doc.blocks:
        b = doc.blocks.new("REGISTRO_ESFERA")
        b.add_line((-2.5, -1.8), (2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-2.5, 1.8), (2.5, -1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-2.5, -1.8), (-2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((2.5, -1.8), (2.5, 1.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_circle((0, 0), radius=0.9, dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((0, 0), (0, 2.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((0, 2.8), (2.5, 2.8), dxfattribs={"layer": "06_EQUIPAMENTOS"})

    # 3. Bloco: VÁLVULA DE RETENÇÃO (Check Valve)
    if "VALVULA_RETENCAO" not in doc.blocks:
        b = doc.blocks.new("VALVULA_RETENCAO")
        b.add_lwpolyline([(-3.0, -2.0), (3.0, -2.0), (3.0, 2.0), (-3.0, 2.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-3.0, -2.0), (3.0, 2.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((-1.0, 0.0), (1.0, 0.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((0.0, -1.0), (1.0, 0.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((0.0, 1.0), (1.0, 0.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})

    # 4. Bloco: MOTOBOMBA CENTRÍFUGA
    if "MOTOBOMBA" not in doc.blocks:
        b = doc.blocks.new("MOTOBOMBA")
        b.add_circle((0, 0), radius=3.5, dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_lwpolyline([(-4.0, -3.5), (4.0, -3.5), (5.0, -4.8), (-5.0, -4.8)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((2.5, 2.5), (2.5, 5.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
        b.add_line((3.5, 0.0), (3.5, 5.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})

    # 5. Bloco: FREIO D'ÁGUA (Calming Inlet)
    if "FREIO_DAGUA" not in doc.blocks:
        b = doc.blocks.new("FREIO_DAGUA")
        b.add_line((-1.5, 10.0), (-1.5, 2.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_line((1.5, 10.0), (1.5, 2.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_arc((4.0, 2.0), radius=5.5, start_angle=180, end_angle=360, dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_arc((4.0, 2.0), radius=2.5, start_angle=180, end_angle=360, dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_line((6.5, 2.0), (6.5, 5.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_line((9.5, 2.0), (9.5, 5.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
        b.add_line((6.5, 5.0), (9.5, 5.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})

    # 6. Bloco: LADRÃO SIFONADO COM TELA
    if "LADRAO_SIFONADO" not in doc.blocks:
        b = doc.blocks.new("LADRAO_SIFONADO")
        pts = [(0, 0), (6.0, 0), (6.0, -8.0), (12.0, -8.0), (12.0, -3.0), (18.0, -3.0)]
        b.add_lwpolyline(pts, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
        b.add_line((18.0, -4.5), (18.0, -1.5), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO", "color": 1})
        b.add_line((17.5, -4.0), (18.5, -2.0), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO", "color": 1})
        b.add_line((17.5, -2.0), (18.5, -4.0), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO", "color": 1})

    # 7. Bloco: SÍMBOLO DE NORTE
    if "SIMBOLO_NORTE" not in doc.blocks:
        b = doc.blocks.new("SIMBOLO_NORTE")
        b.add_circle((0, 0), radius=4.0, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"})
        b.add_lwpolyline([(0, 4.0), (-1.2, -1.0), (0, -0.2)], close=True, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"})
        h = b.add_hatch(color=7, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"})
        h.set_solid_fill()
        h.paths.add_polyline_path([(0, 4.0), (1.2, -1.0), (0, -0.2)], is_closed=True)
        b.add_text("N", height=2.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((0, 4.8), align=TextEntityAlignment.BOTTOM_CENTER)


def _estilo_de_cota() -> str:
    """O nome do estilo de cotas: «ABNT_TRITON» na Brasil (como sempre); «TRITON_COTAS» fora dela."""
    from triton.core.edition import usa_dados_do_brasil
    return "ABNT_TRITON" if usa_dados_do_brasil() else "TRITON_COTAS"


def _setup_dimension_style(doc: ezdxf.document.Drawing):
    """Configura o estilo de cotas normativo ABNT com vírgula como separador decimal."""
    dimstyle = doc.dimstyles.new(_estilo_de_cota())
    dimstyle.dxf.dimtxt = 1.8
    dimstyle.dxf.dimasz = 1.5
    dimstyle.dxf.dimexe = 1.0
    dimstyle.dxf.dimexo = 0.8
    dimstyle.dxf.dimgap = 0.8
    dimstyle.dxf.dimdsep = ord(",")
    dimstyle.dxf.dimdec = 1
    dimstyle.dxf.dimclrd = 2
    dimstyle.dxf.dimclre = 2
    dimstyle.dxf.dimclrt = 7


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR DE PRANCHA TÉCNICA A3 COM EZDXF (NBR 15527 / NBR 5626)
# ─────────────────────────────────────────────────────────────────────────────

def _generate_technical_a3_ezdxf(project_data: Dict[str, Any], output_path: str):
    """Gera prancha técnica A3 completa em formato DXF R2018 com ezdxf."""
    doc = ezdxf.new(dxfversion="R2018")
    configure_cad_document(doc)
    msp = doc.modelspace()

    # 1. Configuração inicial de layers, blocos e cotas
    _setup_abnt_layers(doc)
    _setup_technical_blocks(doc)
    _setup_dimension_style(doc)

    # 2. Dados do projeto e tratamento de números
    proj_name = project_data.get("project_name", "Projeto Sem Nome") or "Projeto Triton"
    ref_code = project_data.get("ref_code", "N5-2026-CAD")
    city_uf = (project_data.get("audit_context") or {}).get("climate_location", "Não informada")
    today_str = datetime.now().strftime("%d/%m/%Y")
    organization = str(project_data.get("organization") or "ORGANIZAÇÃO / ESCRITÓRIO A DEFINIR")
    department = str(project_data.get("department") or "PROJETO HIDROSSANITÁRIO • TRITON")
    technical_responsible = str(project_data.get("technical_responsible") or "A DEFINIR PELO PROJETISTA")

    # Os números abaixo dão a geometria do desenho; o que a prancha escreve sai de
    # textos_do_quadro, que diz «Não informado» quando o projeto não traz o dado.
    tx = textos_do_quadro(project_data)
    area = _safe_float(project_data.get("area"), 150.0)
    runoff = _safe_float(project_data.get("runoff"), COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard_mm = _safe_float(project_data.get("discard"), 2.0)
    vol_lower = _safe_float(project_data.get("lower_vol"), 5000.0)
    upper_vol = _extract_upper_vol(project_data, 500.0)
    tot_demand = demanda_total_do_desenho(project_data)
    tem_demanda = tot_demand is not None
    share_pct = fracao_para_percentual("A fração atendível", _safe_float(project_data.get("share"), 0.40))
    potential_pct = _safe_float(project_data.get("potential_pct"), 0.0)

    vol_discard = area * discard_mm if _presente(project_data.get("area")) else 0.0
    target_pluvial = (tot_demand or 0.0) * (share_pct / 100.0)

    # Informações da bomba e cálculo de diâmetros pela Fórmula de Forchheimer
    pump_hp_raw = project_data.get("pump_power_cv") or project_data.get("system_design", {}).get("pump_power_cv")
    if not pump_hp_raw or pump_hp_raw == "-":
        pump_hp = "1/2" if vol_lower <= 10000 else "3/4" if vol_lower <= 20000 else "1.0"
    else:
        pump_hp = str(pump_hp_raw)

    pump_kw_raw = project_data.get("pump_power_kw") or project_data.get("system_design", {}).get("pump_power_kw")
    pump_kw = _safe_float(pump_kw_raw, 0.37 if pump_hp == "1/2" else 0.55 if pump_hp == "3/4" else 0.75)

    pump_flow_raw = project_data.get("pump_flow_l_h") or project_data.get("system_design", {}).get("pump_flow_l_h")
    pump_flow_m3_h = (_safe_float(pump_flow_raw, 0.0) / 1000.0) if pump_flow_raw else 0.0

    # Dimensionamento econômico de recalque e sucção (Fórmula de Forchheimer)
    forch = calculate_forchheimer_pumping_diameters(
        pump_flow_rate_m3_h=pump_flow_m3_h,
        daily_pumped_volume_l=target_pluvial,
        pump_hp=pump_hp,
    )
    dn_rec = forch["dn_rec"]
    dn_suc = forch["dn_suc"]
    if not tem_demanda:
        # Sem a demanda do projeto, Forchheimer não tem o tempo de bombeamento.
        dn_rec = dn_suc = f"({NAO_CALCULADO.lower()})"
    d_rec_calc_mm = forch["d_rec_calc_mm"]
    v_rec = forch["v_rec"]
    v_suc = forch["v_suc"]
    q_m3h = forch["q_m3_h"]
    q_ls = forch["q_l_s"]
    t_h = forch["t_hours"]

    # 3. Moldura e margens normativas ABNT A3 (420 x 297 mm)
    msp.add_lwpolyline([(0, 0), (420, 0), (420, 297), (0, 297)], close=True, dxfattribs={"layer": "00_FOLHA_E_MARGEM"})
    msp.add_lwpolyline([(25, 10), (410, 10), (410, 287), (25, 287)], close=True, dxfattribs={"layer": "00_FOLHA_E_MARGEM"})

    # 4. Selo Técnico Profissional ABNT (X: 235 a 410, Y: 10 a 65 -> 175 x 55 mm)
    xs, ys, ws, hs = 235.0, 10.0, 175.0, 55.0
    msp.add_lwpolyline([(xs, ys), (xs + ws, ys), (xs + ws, ys + hs), (xs, ys + hs)], close=True, dxfattribs={"layer": "00_SELO"})
    msp.add_line((xs, ys + 42.0), (xs + ws, ys + 42.0), dxfattribs={"layer": "00_SELO"})
    msp.add_line((xs, ys + 30.0), (xs + ws, ys + 30.0), dxfattribs={"layer": "00_SELO"})
    msp.add_line((xs, ys + 18.0), (xs + ws, ys + 18.0), dxfattribs={"layer": "00_SELO"})
    msp.add_line((xs + 115.0, ys), (xs + 115.0, ys + 30.0), dxfattribs={"layer": "00_SELO"})
    msp.add_line((xs + 145.0, ys), (xs + 145.0, ys + 18.0), dxfattribs={"layer": "00_SELO"})

    msp.add_text(organization.upper()[:70], height=2.4, dxfattribs={"layer": "00_SELO", "color": 7}).set_placement((xs + 4.0, ys + 49.0))
    msp.add_text(department.upper()[:78], height=1.9, dxfattribs={"layer": "00_SELO", "color": 7}).set_placement((xs + 4.0, ys + 44.5))

    msp.add_text(f"PROJETO: APROVEITAMENTO DE ÁGUA DE CHUVA (NBR 15527) — {proj_name.upper()}", height=2.1, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 36.5))
    msp.add_text(f"REF. AUDITORIA: {ref_code} | MUNICÍPIO: {city_uf.upper()}", height=1.7, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 32.5))

    msp.add_text("ESQUEMA HIDRÁULICO E DETALHAMENTO DO SISTEMA PLUVIAL", height=2.2, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 24.5))
    msp.add_text("CORTE ESQUEMÁTICO INTEGRADO, QUADRO DE DIMENSIONAMENTO E MATERIAIS", height=1.6, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 20.5))

    msp.add_text("RESPONSÁVEIS TÉCNICOS:", height=1.6, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 13.0))
    msp.add_text(technical_responsible[:72], height=2.1, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 4.0, ys + 7.0))

    msp.add_text(f"DATA: {today_str}", height=1.8, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 118.0, ys + 24.0))
    msp.add_text("ESCALA: INDICADA", height=1.8, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 118.0, ys + 20.0))
    msp.add_text("PRANCHA:", height=1.5, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 118.0, ys + 13.0))
    msp.add_text("01 / 01", height=2.8, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 118.0, ys + 6.0))
    msp.add_text("FORMATO:", height=1.5, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 148.0, ys + 13.0))
    msp.add_text("A3", height=2.8, dxfattribs={"layer": "00_SELO"}).set_placement((xs + 148.0, ys + 6.0))

    # 5. Quadro 1 — Parâmetros de Projeto e Dimensionamento (NBR 15527 / NBR 5626)
    xq, yq, wq, hq = 235.0, 185.0, 175.0, 102.0
    msp.add_lwpolyline([(xq, yq), (xq + wq, yq), (xq + wq, yq + hq), (xq, yq + hq)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_line((xq, yq + hq - 8.0), (xq + wq, yq + hq - 8.0), dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("QUADRO 1 — PARÂMETROS DE PROJETO (NBR 15527:2019)", height=2.1, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq + 4.0, yq + hq - 5.5))

    quadro1_items = [
        ("Área de Captação da Cobertura:", tx["area"]),
        ("Coeficiente de Escoamento (Runoff C):", f"{_fmt_ptbr(runoff, 2)}"),
        ("Lâmina de Descarte Inicial (First Flush):", f"{_fmt_ptbr(discard_mm, 1)} mm"),
        ("Volume Estimado de Descarte Inicial:", f"{_fmt_milhar(vol_discard)} Litros" if vol_discard > 0 else NAO_INFORMADO),
        ("Capacidade da Cisterna Inferior:", tx["volume"]),
        ("Capacidade do Reservatório Superior:", f"{_fmt_milhar(upper_vol)} Litros"),
        ("Demanda Total Diária da Edificação:", tx["demanda"]),
        ("Demanda Pluvial Substituível Alvo:", tx["alvo"]),
        ("Potencial de Economia de Água Potável:", tx["potencial"]),
        ("Motobomba Recomendada e Vazão (Q):", f"{pump_hp} cv ({_fmt_ptbr(pump_kw, 2)} kW) · {_fmt_ptbr(q_m3h, 1)} m³/h"),
        # Sem a demanda, o tempo de bombeamento e o recalque econômico não se calculam.
        ("Tempo Estimado de Funcionamento (T):", f"{_fmt_ptbr(t_h, 1)} h/dia" if tem_demanda else NAO_CALCULADO),
        ("Diâmetro Recalque Econômico:", f"DN {dn_rec} mm (d_calc = {_fmt_ptbr(d_rec_calc_mm, 1)} mm, v = {_fmt_ptbr(v_rec, 2)} m/s)" if tem_demanda else NAO_CALCULADO),
        ("Diâmetro Sucção (NBR 5626, D_suc > D_rec):", f"DN {dn_suc} mm (v_suc = {_fmt_ptbr(v_suc, 2)} m/s)"),
    ]

    for i, (label, val) in enumerate(quadro1_items):
        y_row = yq + hq - 13.0 - (i * 6.8)
        msp.add_text(label, height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq + 4.0, y_row))
        msp.add_text(val, height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS", "color": 7}).set_placement((xq + wq - 4.0, y_row), align=TextEntityAlignment.TOP_RIGHT)
        if i < len(quadro1_items) - 1:
            msp.add_line((xq + 4.0, y_row - 1.2), (xq + wq - 4.0, y_row - 1.2), dxfattribs={"layer": "10_LEGENDA_E_QUADROS", "color": 8})

    # 6. Quadro 2 — Lista Estimativa de Conexões e Materiais
    xq2, yq2, wq2, hq2 = 235.0, 70.0, 175.0, 110.0
    msp.add_lwpolyline([(xq2, yq2), (xq2 + wq2, yq2), (xq2 + wq2, yq2 + hq2), (xq2, yq2 + hq2)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_line((xq2, yq2 + hq2 - 7.0), (xq2 + wq2, yq2 + hq2 - 7.0), dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("QUADRO 2 — LISTA ESTIMATIVA DE CONEXÕES E MATERIAIS", height=2.0, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + 4.0, yq2 + hq2 - 5.0))

    y_hdr = yq2 + hq2 - 12.0
    msp.add_text("ITEM", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + 4.0, y_hdr))
    msp.add_text("ESPECIFICAÇÃO NORMATIVA", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + 18.0, y_hdr))
    msp.add_text("QUANT.", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + wq2 - 4.0, y_hdr), align=TextEntityAlignment.TOP_RIGHT)
    msp.add_line((xq2 + 4.0, y_hdr - 1.5), (xq2 + wq2 - 4.0, y_hdr - 1.5), dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})

    materiais = [
        ("01", "Calha Semicircular de Alumínio / Aluzinco", "Conf. Beiral"),
        ("02", "Tubo PVC Esgoto/Pluvial Série Normal DN 100 mm", "Conf. Projeto"),
        ("03", f"Tubo PVC Soldável Água Fria DN {dn_rec} mm (Recalque Econômico)", "Conf. Projeto"),
        ("04", f"Tubo PVC Soldável Água Fria DN {dn_suc} mm (Sucção — NBR 5626)", "Conf. Projeto"),
        ("05", "Tubo PVC Soldável Água Fria DN 25 mm (Distribuição Não Potável)", "Conf. Projeto"),
        ("06", "Caixa de Descarte Inicial First Flush com Dreno", "1 un"),
        ("07", "Filtro Mecânico Autolimpante com Tela Inox 0,5 mm", "1 un"),
        ("08", "Freio d'Água Dispersor de Entrada Cisterna DN 100", "1 un"),
        ("09", f"Motobomba Centrífuga {pump_hp} cv ({_fmt_ptbr(q_m3h, 1)} m³/h) c/ Base Antivibratória", "1 un"),
        ("10", f"Válvula de Retenção Vertical Soldável DN {dn_rec} mm", "1 un"),
        ("11", f"Válvula de Pé com Crivo em Latão DN {dn_suc} mm", "1 un"),
        ("12", f"Registros de Gaveta e Esfera Brutos DN {dn_rec} e DN 25", "6 un"),
        ("13", "Torneiras de Bóia com Vedação Estanque DN 25 mm", "2 un"),
        ("14", "Extravasor / Ladrão com Sifão e Tela Anti-insetos", "1 un"),
    ]

    for i, (item, desc, qtd) in enumerate(materiais):
        y_r = y_hdr - 5.0 - (i * 6.3)
        msp.add_text(item, height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + 4.0, y_r))
        msp.add_text(desc, height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + 18.0, y_r))
        msp.add_text(qtd, height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xq2 + wq2 - 4.0, y_r), align=TextEntityAlignment.TOP_RIGHT)
        if i < len(materiais) - 1:
            msp.add_line((xq2 + 4.0, y_r - 1.0), (xq2 + wq2 - 4.0, y_r - 1.0), dxfattribs={"layer": "10_LEGENDA_E_QUADROS", "color": 8})

    msp.add_text("* Distâncias de tubulação conforme traçado executivo do projeto arquitetônico.", height=1.1, dxfattribs={"layer": "10_LEGENDA_E_QUADROS", "color": 8}).set_placement((xq2 + 4.0, yq2 + 4.0))
    msp.add_text("* Diâmetros calculados por dimensionamento econômico (recalque) e NBR 5626 (sucção).", height=1.1, dxfattribs={"layer": "10_LEGENDA_E_QUADROS", "color": 8}).set_placement((xq2 + 4.0, yq2 + 2.0))

    # 7. Legenda de Símbolos Hidráulicos (X: 25 a 125, Y: 10 a 65)
    xl, yl, wl, hl = 25.0, 10.0, 100.0, 55.0
    msp.add_lwpolyline([(xl, yl), (xl + wl, yl), (xl + wl, yl + hl), (xl, yl + hl)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_line((xl, yl + hl - 7.0), (xl + wl, yl + hl - 7.0), dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("LEGENDA DE SÍMBOLOS HIDRÁULICOS", height=2.0, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 4.0, yl + hl - 5.0))

    msp.add_line((xl + 5.0, yl + 39.0), (xl + 25.0, yl + 39.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_text("Tubulação Água Pluvial Bruta (AP)", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 28.0, yl + 38.0))

    msp.add_line((xl + 5.0, yl + 30.0), (xl + 25.0, yl + 30.0), dxfattribs={"layer": "03_TUB_RECALQUE"})
    msp.add_text(f"Tubulação Recalque Pluvial DN {dn_rec} (REC)", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 28.0, yl + 29.0))

    msp.add_line((xl + 5.0, yl + 21.0), (xl + 25.0, yl + 21.0), dxfattribs={"layer": "04_TUB_DISTRIBUICAO"})
    msp.add_text("Tubulação Distribuição Não Potável (NP)", height=1.5, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 28.0, yl + 20.0))

    msp.add_blockref("REGISTRO_GAVETA", (xl + 12.0, yl + 11.0))
    msp.add_text("Reg. Gaveta", height=1.4, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 22.0, yl + 10.0))

    msp.add_blockref("MOTOBOMBA", (xl + 60.0, yl + 11.0))
    msp.add_text("Motobomba", height=1.4, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xl + 70.0, yl + 10.0))

    # 8. Notas Técnicas (X: 130 a 230, Y: 10 a 65)
    xn, yn, wn, hn = 130.0, 10.0, 100.0, 55.0
    msp.add_lwpolyline([(xn, yn), (xn + wn, yn), (xn + wn, yn + hn), (xn, yn + hn)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_line((xn, yn + hn - 7.0), (xn + wn, yn + hn - 7.0), dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("NOTAS TÉCNICAS (ABNT NBR 15527 / NBR 5626)", height=1.9, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xn + 4.0, yn + hn - 5.0))

    notas = [
        "1. Separação Física Obrigatória (Air-Gap):",
        "   Proibida interconexão direta entre potável e pluvial (folga >= 50 mm).",
        "2. Identificação e Segurança Sanitária:",
        "   Pontos de consumo devem conter aviso 'ÁGUA NÃO POTÁVEL'.",
        "3. Extravasores com Sifão e Tela Milimétrica:",
        "   Proteção contra entrada de roedores, mosquitos e retorno de odores.",
        "4. Descarte e Filtro Autolimpante:",
        "   Descarte inicial First Flush obrigatório antes do reservatório.",
        "5. Dimensionamento Hidráulico (NBR 5626):",
        f"   D_rec = 1,3*(T/24)^0,25*sqrt(Q) -> Recalque DN {dn_rec} mm | Sucção DN {dn_suc} mm.",
        "   Distâncias e traçado de tubulações conforme projeto executivo.",
    ]
    for i, line in enumerate(notas):
        msp.add_text(line, height=1.15, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xn + 4.0, yn + hn - 11.0 - (i * 3.7)))

    # 9. Corte Esquemático Geral (X: 30 a 150, Y: 75 a 285)
    msp.add_text("CORTE ESQUEMÁTICO HIDRÁULICO DO SISTEMA PREDIAL", height=2.6, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((30.0, 280.0))
    msp.add_text("DIMENSIONAMENTO CONFORME ABNT NBR 15527:2019 E NBR 5626 | ESCALA INDICADA", height=1.6, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((30.0, 275.5))

    # Telhado
    msp.add_lwpolyline([(30.0, 250.0), (55.0, 265.0), (80.0, 250.0), (77.0, 250.0), (55.0, 262.5), (33.0, 250.0)], close=True, dxfattribs={"layer": "01_ALVENARIA_COBERTURA"})
    msp.add_text(f"COBERTURA DE CAPTAÇÃO: {tx['area_int']} (C = {_fmt_ptbr(runoff, 2)})", height=1.8, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((55.0, 267.0), align=TextEntityAlignment.BOTTOM_CENTER)
    # Inclinação do telhado posicionada mais à esquerda e deixada em branco para o usuário definir
    msp.add_text("i = ___%", height=1.4, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((34.0, 258.0))

    # Calha
    msp.add_lwpolyline([(78.0, 248.0), (84.0, 248.0), (84.0, 252.0), (78.0, 252.0)], close=True, dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_text("CALHA (i >= 0,5%)", height=1.4, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((86.0, 251.0))

    # TQP
    msp.add_line((81.0, 248.0), (81.0, 215.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_text("TQP DN 100 mm", height=1.5, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((84.0, 232.0))

    # Filtro
    msp.add_lwpolyline([(76.0, 208.0), (86.0, 208.0), (86.0, 215.0), (76.0, 215.0)], close=True, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_line((76.0, 213.0), (86.0, 210.0), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_text("FILTRO AUTOLIMPANTE (Tela Inox 0,5 mm)", height=1.4, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((74.0, 212.0), align=TextEntityAlignment.MIDDLE_RIGHT)

    # First Flush
    msp.add_line((81.0, 208.0), (81.0, 182.0), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_circle((81.0, 180.5), radius=1.5, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_text(f"FIRST FLUSH ({_fmt_ptbr(discard_mm, 1)} mm = {_fmt_milhar(vol_discard)} L)", height=1.4, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((78.0, 195.0), align=TextEntityAlignment.MIDDLE_RIGHT)
    msp.add_text("Dreno c/ Registro de Limpeza", height=1.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((78.0, 180.5), align=TextEntityAlignment.MIDDLE_RIGHT)

    # Tubo para a cisterna
    msp.add_lwpolyline([(86.0, 212.0), (95.0, 212.0), (95.0, 140.0)], dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})

    # Cisterna
    msp.add_lwpolyline([(88.0, 95.0), (130.0, 95.0), (130.0, 140.0), (88.0, 140.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_lwpolyline([(86.0, 93.0), (132.0, 93.0), (132.0, 142.0), (86.0, 142.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})

    hatch_conc = msp.add_hatch(color=8, dxfattribs={"layer": "07_HACHURAS"})
    hatch_conc.set_solid_fill()
    hatch_conc.paths.add_polyline_path([(86.0, 93.0), (132.0, 93.0), (132.0, 142.0), (86.0, 142.0)], is_closed=True)
    hatch_conc.paths.add_polyline_path([(88.0, 95.0), (130.0, 95.0), (130.0, 140.0), (88.0, 140.0)], is_closed=True)

    msp.add_line((88.0, 130.0), (130.0, 130.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
    # Texto somente cisterna: e o volume, centralizado no espaço livre (afastado da tubulação de entrada em x=95)
    msp.add_text(f"Cisterna: {tx['volume_l']}", height=1.8, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((113.0, 120.0), align=TextEntityAlignment.MIDDLE_CENTER)

    msp.add_blockref("FREIO_DAGUA", (95.0, 97.0))
    msp.add_text("Freio d'Água (Dispersor)", height=1.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((97.0, 98.0))

    msp.add_blockref("LADRAO_SIFONADO", (88.0, 132.0), dxfattribs={"rotation": 180})
    msp.add_text("LADRÃO SIFONADO C/ TELA", height=1.2, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"}).set_placement((85.0, 136.0), align=TextEntityAlignment.MIDDLE_RIGHT)

    msp.add_lwpolyline([(103.0, 140.0), (115.0, 140.0), (115.0, 143.0), (103.0, 143.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_text("Tampa Hermética DN 600", height=1.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((109.0, 145.0), align=TextEntityAlignment.BOTTOM_CENTER)

    # Bomba, sucção e recalque (com quebra de linha para o DN)
    msp.add_line((125.0, 105.0), (135.0, 105.0), dxfattribs={"layer": "03_TUB_RECALQUE"})
    msp.add_text("Sucção", height=1.2, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((130.0, 110.5), align=TextEntityAlignment.BOTTOM_CENTER)
    msp.add_text(f"DN {dn_suc}", height=1.2, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((130.0, 107.0), align=TextEntityAlignment.BOTTOM_CENTER)

    msp.add_blockref("MOTOBOMBA", (138.0, 105.0))
    msp.add_text(f"BOMBA {pump_hp} cv", height=1.3, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((138.0, 98.0), align=TextEntityAlignment.TOP_CENTER)

    msp.add_lwpolyline([(141.5, 105.0), (146.0, 105.0), (146.0, 240.0), (120.0, 240.0)], dxfattribs={"layer": "03_TUB_RECALQUE"})
    # Recalque em duas linhas, em posição livre (y=122-126) sem sobrepor os pontos de distribuição (y=150-190)
    msp.add_text("Recalque", height=1.3, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((148.5, 126.0), align=TextEntityAlignment.BOTTOM_LEFT)
    msp.add_text(f"DN {dn_rec}", height=1.3, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((148.5, 122.5), align=TextEntityAlignment.BOTTOM_LEFT)

    # Reservatório Superior
    msp.add_lwpolyline([(95.0, 220.0), (120.0, 220.0), (120.0, 245.0), (95.0, 245.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_text(f"SUPERIOR: {_fmt_milhar(upper_vol)} L", height=1.8, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((107.5, 237.0), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("Água Não Potável", height=1.4, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((107.5, 228.0), align=TextEntityAlignment.MIDDLE_CENTER)

    # Backup Potável: reposicionado para a direita e para cima
    msp.add_lwpolyline([(88.0, 250.0), (102.0, 250.0), (102.0, 246.0)], dxfattribs={"layer": "06_EQUIPAMENTOS", "color": 4})
    msp.add_text("BACKUP POTÁVEL (AIR-GAP >= 50 mm)", height=1.3, dxfattribs={"layer": "06_EQUIPAMENTOS", "color": 4}).set_placement((104.0, 251.5), align=TextEntityAlignment.BOTTOM_LEFT)

    # Distribuição: sem diâmetro fixado (não calculado e dependente dos aparelhos)
    msp.add_lwpolyline([(120.0, 225.0), (125.0, 225.0), (125.0, 150.0)], dxfattribs={"layer": "04_TUB_DISTRIBUICAO"})
    msp.add_text("DISTRIBUIÇÃO NÃO POTÁVEL", height=1.4, dxfattribs={"layer": "04_TUB_DISTRIBUICAO"}).set_placement((127.0, 210.0))

    pontos = [
        (190.0, "Bacias Sanitárias (VS/MT) [NÃO POTÁVEL]"),
        (170.0, "Máquina de Lavar / Tanque [NÃO POTÁVEL]"),
        (150.0, "Jardim / Calçadas [NÃO POTÁVEL]"),
    ]
    for y_pt, txt_pt in pontos:
        msp.add_line((125.0, y_pt), (133.0, y_pt), dxfattribs={"layer": "04_TUB_DISTRIBUICAO"})
        msp.add_lwpolyline([(133.0, y_pt - 2.0), (145.0, y_pt - 2.0), (145.0, y_pt + 2.0), (133.0, y_pt + 2.0)], close=True, dxfattribs={"layer": "04_TUB_DISTRIBUICAO"})
        msp.add_text(txt_pt, height=1.3, dxfattribs={"layer": "04_TUB_DISTRIBUICAO"}).set_placement((148.0, y_pt))

    # 10. Detalhamentos Construtivos (X: 155 a 230, Y: 75 a 285)
    # Detalhe 01
    xd1, yd1, wd1, hd1 = 155.0, 215.0, 75.0, 65.0
    msp.add_lwpolyline([(xd1, yd1), (xd1 + wd1, yd1), (xd1 + wd1, yd1 + hd1), (xd1, yd1 + hd1)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("DETALHE 01 — FREIO D'ÁGUA (DISPERSOR)", height=1.8, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd1 + 3.0, yd1 + hd1 - 4.5))
    msp.add_text("ESCALA 1:10 | NBR 15527", height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd1 + 3.0, yd1 + hd1 - 8.5))

    msp.add_line((xd1 + 25.0, yd1 + hd1 - 15.0), (xd1 + 25.0, yd1 + 20.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_line((xd1 + 31.0, yd1 + hd1 - 15.0), (xd1 + 31.0, yd1 + 20.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_arc((xd1 + 36.0, yd1 + 20.0), radius=11.0, start_angle=180, end_angle=360, dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_arc((xd1 + 36.0, yd1 + 20.0), radius=5.0, start_angle=180, end_angle=360, dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_line((xd1 + 41.0, yd1 + 20.0), (xd1 + 41.0, yd1 + 28.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_line((xd1 + 47.0, yd1 + 20.0), (xd1 + 47.0, yd1 + 28.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_line((xd1 + 41.0, yd1 + 28.0), (xd1 + 47.0, yd1 + 28.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})

    msp.add_line((xd1 + 10.0, yd1 + 8.0), (xd1 + 65.0, yd1 + 8.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_text("Fundo da Cisterna (Lodo Estabilizado)", height=1.3, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((xd1 + 37.0, yd1 + 5.0), align=TextEntityAlignment.TOP_CENTER)
    msp.add_text("Entrada suave sem ressuspensão", height=1.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((xd1 + 48.0, yd1 + 32.0))

    dim1 = msp.add_linear_dim(
        base=(xd1 + 18.0, yd1 + 14.0),
        p1=(xd1 + 25.0, yd1 + 8.0),
        p2=(xd1 + 25.0, yd1 + 9.0),
        dimstyle=_estilo_de_cota(),
        dxfattribs={"layer": "08_COTAS"}
    )
    dim1.render()

    # Detalhe 02
    xd2, yd2, wd2, hd2 = 155.0, 145.0, 75.0, 65.0
    msp.add_lwpolyline([(xd2, yd2), (xd2 + wd2, yd2), (xd2 + wd2, yd2 + hd2), (xd2, yd2 + hd2)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("DETALHE 02 — LADRÃO SIFONADO C/ TELA", height=1.8, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd2 + 3.0, yd2 + hd2 - 4.5))
    msp.add_text("ESCALA 1:10 | BARREIRA DE VETORES", height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd2 + 3.0, yd2 + hd2 - 8.5))

    pts_sifao = [
        (xd2 + 10.0, yd2 + 35.0), (xd2 + 30.0, yd2 + 35.0), (xd2 + 30.0, yd2 + 18.0),
        (xd2 + 45.0, yd2 + 18.0), (xd2 + 45.0, yd2 + 28.0), (xd2 + 65.0, yd2 + 28.0)
    ]
    msp.add_lwpolyline(pts_sifao, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_line((xd2 + 65.0, yd2 + 24.0), (xd2 + 65.0, yd2 + 32.0), dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO", "color": 1})
    msp.add_text("Tela Inox Malha 0,5 mm", height=1.2, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"}).set_placement((xd2 + 65.0, yd2 + 34.0), align=TextEntityAlignment.BOTTOM_RIGHT)
    msp.add_text("Selo hídrico anti-odores", height=1.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((xd2 + 37.0, yd2 + 14.0), align=TextEntityAlignment.TOP_CENTER)

    # Detalhe 03
    xd3, yd3, wd3, hd3 = 155.0, 75.0, 75.0, 65.0
    msp.add_lwpolyline([(xd3, yd3), (xd3 + wd3, yd3), (xd3 + wd3, yd3 + hd3), (xd3, yd3 + hd3)], close=True, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"})
    msp.add_text("DETALHE 03 — SEPARAÇÃO FÍSICA AIR-GAP", height=1.8, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd3 + 3.0, yd3 + hd3 - 4.5))
    msp.add_text("ESCALA 1:15 | NBR 5626 E NBR 15527", height=1.3, dxfattribs={"layer": "10_LEGENDA_E_QUADROS"}).set_placement((xd3 + 3.0, yd3 + hd3 - 8.5))

    msp.add_line((xd3 + 15.0, yd3 + 52.0), (xd3 + 40.0, yd3 + 52.0), dxfattribs={"layer": "06_EQUIPAMENTOS", "color": 4})
    msp.add_line((xd3 + 40.0, yd3 + 52.0), (xd3 + 40.0, yd3 + 42.0), dxfattribs={"layer": "06_EQUIPAMENTOS", "color": 4})
    msp.add_line((xd3 + 25.0, yd3 + 28.0), (xd3 + 65.0, yd3 + 28.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_line((xd3 + 25.0, yd3 + 28.0), (xd3 + 25.0, yd3 + 10.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_line((xd3 + 65.0, yd3 + 28.0), (xd3 + 65.0, yd3 + 10.0), dxfattribs={"layer": "06_EQUIPAMENTOS"})

    dim3 = msp.add_linear_dim(
        base=(xd3 + 48.0, yd3 + 35.0),
        p1=(xd3 + 40.0, yd3 + 42.0),
        p2=(xd3 + 40.0, yd3 + 28.0),
        dimstyle=_estilo_de_cota(),
        dxfattribs={"layer": "08_COTAS"}
    )
    dim3.render()
    msp.add_text("Folga de Ar >= 50 mm", height=1.3, dxfattribs={"layer": "08_COTAS"}).set_placement((xd3 + 52.0, yd3 + 35.0))
    msp.add_text("Sem contato direto (anti-contaminação)", height=1.1, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((xd3 + 40.0, yd3 + 22.0), align=TextEntityAlignment.TOP_CENTER)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    documento_dxf_de_exportacao(doc)
    doc.saveas(output_path)
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR DE ESQUEMÁTICO UNIFILAR SIMPLES COM EZDXF
# ─────────────────────────────────────────────────────────────────────────────

def _generate_simple_ezdxf(project_data: Dict[str, Any], output_path: str):
    """Gera esquema unifilar simplificado em DXF R2018 com ezdxf para apresentação."""
    doc = ezdxf.new(dxfversion="R2018")
    configure_cad_document(doc)
    msp = doc.modelspace()

    _setup_abnt_layers(doc)
    _setup_technical_blocks(doc)

    proj_name = project_data.get("project_name", "Projeto Triton")
    ref_code = project_data.get("ref_code", "N5-SIMPLES")
    organization = str(project_data.get("organization") or "TRITON")
    technical_responsible = str(project_data.get("technical_responsible") or "A DEFINIR PELO PROJETISTA")

    tx = textos_do_quadro(project_data)
    area = _safe_float(project_data.get("area"), 150.0)
    runoff = _safe_float(project_data.get("runoff"), COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard_mm = _safe_float(project_data.get("discard"), 2.0)
    vol_lower = _safe_float(project_data.get("lower_vol"), 5000.0)
    upper_vol = _extract_upper_vol(project_data, 500.0)

    msp.add_text("ESQUEMA UNIFILAR — APROVEITAMENTO DE ÁGUA DE CHUVA (NBR 15527)", height=3.2, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((10.0, 140.0))
    msp.add_text(f"Projeto: {proj_name} | Ref: {ref_code} | Organização: {organization} | Resp.: {technical_responsible}", height=1.8, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((10.0, 134.0))

    msp.add_lwpolyline([(10.0, 90.0), (35.0, 110.0), (60.0, 90.0)], close=True, dxfattribs={"layer": "01_ALVENARIA_COBERTURA"})
    msp.add_text(f"Área: {tx['area']} (C = {_fmt_ptbr(runoff, 2)})", height=1.6, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((35.0, 112.0), align=TextEntityAlignment.BOTTOM_CENTER)

    msp.add_line((60.0, 90.0), (60.0, 60.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_lwpolyline([(55.0, 50.0), (65.0, 50.0), (65.0, 60.0), (55.0, 60.0)], close=True, dxfattribs={"layer": "05_TUB_EXTRAVASOR_DRENO"})
    msp.add_text("Filtro + First Flush", height=1.5, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((60.0, 62.0), align=TextEntityAlignment.BOTTOM_CENTER)
    msp.add_text(f"Descarte: {_fmt_ptbr(discard_mm, 1)} mm", height=1.3, dxfattribs={"layer": "09_TEXTOS_E_NOTAS"}).set_placement((60.0, 46.0), align=TextEntityAlignment.TOP_CENTER)

    msp.add_lwpolyline([(75.0, 30.0), (115.0, 30.0), (115.0, 70.0), (75.0, 70.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_line((65.0, 55.0), (75.0, 55.0), dxfattribs={"layer": "02_TUB_PLUVIAL_BRUTA"})
    msp.add_text(f"Cisterna Inferior: {tx['volume_l']}", height=1.8, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((95.0, 55.0), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text(f"Economia: {tx['potencial_curto']}", height=1.6, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((95.0, 45.0), align=TextEntityAlignment.MIDDLE_CENTER)

    # O recalque econômico sai da demanda pluvial do projeto; supor que se bombeiam
    # 20% da cisterna por dia era fórmula de ninguém.
    dem_s = demanda_total_do_desenho(project_data)
    share_s = fracao_para_percentual("A fração atendível", _safe_float(project_data.get("share"), 0.0))
    if dem_s and share_s > 0:
        forch_s = calculate_forchheimer_pumping_diameters(
            daily_pumped_volume_l=dem_s * share_s / 100.0,
            pump_hp="1/2" if vol_lower <= 10000 else "3/4",
        )
        dn_rec_s = forch_s["dn_rec"]
    else:
        dn_rec_s = f"({NAO_CALCULADO})"

    msp.add_blockref("MOTOBOMBA", (125.0, 40.0))
    msp.add_line((115.0, 40.0), (122.0, 40.0), dxfattribs={"layer": "03_TUB_RECALQUE"})
    msp.add_lwpolyline([(128.5, 40.0), (135.0, 40.0), (135.0, 105.0), (145.0, 105.0)], dxfattribs={"layer": "03_TUB_RECALQUE"})
    msp.add_text(f"Recalque DN {dn_rec_s} (Econômico)", height=1.4, dxfattribs={"layer": "03_TUB_RECALQUE"}).set_placement((137.0, 70.0))

    msp.add_lwpolyline([(145.0, 90.0), (175.0, 90.0), (175.0, 115.0), (145.0, 115.0)], close=True, dxfattribs={"layer": "06_EQUIPAMENTOS"})
    msp.add_text(f"Superior: {_fmt_milhar(upper_vol)} L", height=1.7, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((160.0, 105.0), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("Air-Gap >= 50 mm", height=1.3, dxfattribs={"layer": "06_EQUIPAMENTOS"}).set_placement((160.0, 96.0), align=TextEntityAlignment.MIDDLE_CENTER)

    msp.add_lwpolyline([(175.0, 95.0), (185.0, 95.0), (185.0, 30.0)], dxfattribs={"layer": "04_TUB_DISTRIBUICAO"})
    msp.add_text("Distribuição Não Potável", height=1.4, dxfattribs={"layer": "04_TUB_DISTRIBUICAO"}).set_placement((187.0, 65.0))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    documento_dxf_de_exportacao(doc)
    doc.saveas(output_path)
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# API PRINCIPAL DE EXPORTAÇÃO DXF
# ─────────────────────────────────────────────────────────────────────────────

def generate_project_dxf(project_data: Dict[str, Any], output_path: str, mode: str = "technical_a3") -> str:
    """
    Exporta o projeto em formato CAD DXF R2018 (UTF-8 nativo) via ezdxf.
    
    Parâmetros:
      - project_data: Dicionário contendo dados de simulação e projeto.
      - output_path: Caminho de gravação do arquivo .dxf.
      - mode: 'technical_a3' (prancha técnica), 'simple' (esquema unifilar)
              'block_library' (biblioteca 1:1 mm + manifesto BIM JSON)
              ou 'plant_3d' (trechos organizados pelo projetista, em 3D).
    """
    if mode == "simple":
        return _generate_simple_ezdxf(project_data, output_path)
    if mode in {"block_library", "blocks", "biblioteca_blocos"}:
        return generate_block_library_dxf(project_data, output_path)
    if mode in {"plant_3d", "planta_3d"}:
        return generate_plant_3d_dxf(project_data, output_path)
    if mode != "technical_a3":
        raise ValueError(f"Modo CAD inválido: {mode}")
    return _generate_technical_a3_ezdxf(project_data, output_path)


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR VETORIAL SVG (PRÉVIA TÉCNICA EM ALTA DEFINIÇÃO)
# ─────────────────────────────────────────────────────────────────────────────

def _generate_technical_a3_svg(project_data: Dict[str, Any]) -> str:
    """Gera a prancha A3 técnica completa em SVG mantendo fidelidade absoluta ao DXF do ezdxf."""
    proj_name = project_data.get("project_name", "Projeto Sem Nome") or "Projeto Triton"
    ref_code = project_data.get("ref_code", "N5-2026-CAD")
    city_uf = (project_data.get("audit_context") or {}).get("climate_location", "Não informada")
    today_str = datetime.now().strftime("%d/%m/%Y")
    organization = escape(str(project_data.get("organization") or "ORGANIZAÇÃO / ESCRITÓRIO A DEFINIR"))
    department = escape(str(project_data.get("department") or "PROJETO HIDROSSANITÁRIO • TRITON"))
    technical_responsible = escape(str(project_data.get("technical_responsible") or "A DEFINIR PELO PROJETISTA"))
    proj_name = escape(str(proj_name))
    ref_code = escape(str(ref_code))
    city_uf = escape(str(city_uf))

    # Os números abaixo dão a geometria do desenho; o que a prancha escreve sai de
    # textos_do_quadro, que diz «Não informado» quando o projeto não traz o dado.
    tx = textos_do_quadro(project_data)
    area = _safe_float(project_data.get("area"), 150.0)
    runoff = _safe_float(project_data.get("runoff"), COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard_mm = _safe_float(project_data.get("discard"), 2.0)
    vol_lower = _safe_float(project_data.get("lower_vol"), 5000.0)
    upper_vol = _extract_upper_vol(project_data, 500.0)
    tot_demand = demanda_total_do_desenho(project_data)
    tem_demanda = tot_demand is not None
    share_pct = fracao_para_percentual("A fração atendível", _safe_float(project_data.get("share"), 0.40))
    potential_pct = _safe_float(project_data.get("potential_pct"), 0.0)

    vol_discard = area * discard_mm if _presente(project_data.get("area")) else 0.0
    target_pluvial = (tot_demand or 0.0) * (share_pct / 100.0)

    # Informações da motobomba e diâmetros pela Fórmula de Forchheimer
    pump_hp_raw = project_data.get("pump_power_cv") or project_data.get("system_design", {}).get("pump_power_cv")
    if not pump_hp_raw or pump_hp_raw == "-":
        pump_hp = "1/2" if vol_lower <= 10000 else "3/4" if vol_lower <= 20000 else "1.0"
    else:
        pump_hp = str(pump_hp_raw)

    pump_kw_raw = project_data.get("pump_power_kw") or project_data.get("system_design", {}).get("pump_power_kw")
    pump_kw = _safe_float(pump_kw_raw, 0.37 if pump_hp == "1/2" else 0.55 if pump_hp == "3/4" else 0.75)

    pump_flow_raw = project_data.get("pump_flow_l_h") or project_data.get("system_design", {}).get("pump_flow_l_h")
    pump_flow_m3_h = (_safe_float(pump_flow_raw, 0.0) / 1000.0) if pump_flow_raw else 0.0

    # Dimensionamento de recalque e sucção (Fórmula de Forchheimer / NBR 5626)
    forch = calculate_forchheimer_pumping_diameters(
        pump_flow_rate_m3_h=pump_flow_m3_h,
        daily_pumped_volume_l=target_pluvial,
        pump_hp=pump_hp,
    )
    dn_rec = forch["dn_rec"]
    dn_suc = forch["dn_suc"]
    if not tem_demanda:
        # Sem a demanda do projeto, Forchheimer não tem o tempo de bombeamento.
        dn_rec = dn_suc = f"({NAO_CALCULADO.lower()})"
    d_rec_calc_mm = forch["d_rec_calc_mm"]
    v_rec = forch["v_rec"]
    v_suc = forch["v_suc"]
    q_m3h = forch["q_m3_h"]
    t_h = forch["t_hours"]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 990" width="1400" height="990" style="background:#ffffff; font-family:'Segoe UI', Inter, Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="cardShadow" x="-3%" y="-3%" width="106%" height="108%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity="0.06" />
    </filter>
  </defs>

  <!-- MOLDURA NORMATIVA A3 (Margem Esquerda 25 mm = 83px, Demais 10 mm = 33px) -->
  <rect x="15" y="15" width="1370" height="960" fill="none" stroke="#0f172a" stroke-width="2.5" />
  <rect x="85" y="33" width="1285" height="924" fill="none" stroke="#0f172a" stroke-width="1.2" />

  <!-- SELO TÉCNICO ABNT (Canto Inferior Direito: 580px x 180px) -->
  <g transform="translate(790, 777)">
    <rect x="0" y="0" width="580" height="180" fill="#ffffff" stroke="#0f172a" stroke-width="1.8" />
    <line x1="0" y1="42" x2="580" y2="42" stroke="#0f172a" stroke-width="1" />
    <line x1="0" y1="84" x2="580" y2="84" stroke="#0f172a" stroke-width="1" />
    <line x1="0" y1="126" x2="580" y2="126" stroke="#0f172a" stroke-width="1" />
    <line x1="390" y1="42" x2="390" y2="180" stroke="#0f172a" stroke-width="1" />
    <line x1="485" y1="126" x2="485" y2="180" stroke="#0f172a" stroke-width="1" />

    <text x="15" y="22" font-size="12" font-weight="800" fill="#0f172a">{organization[:70]}</text>
    <text x="15" y="36" font-size="9.5" font-weight="600" fill="#475569">{department[:82]}</text>

    <text x="15" y="56" font-size="8.5" fill="#64748b">PROJETO:</text>
    <text x="15" y="69" font-size="10.5" font-weight="700" fill="#0f172a">APROVEITAMENTO DE ÁGUA DE CHUVA (NBR 15527)</text>
    <text x="15" y="80" font-size="9" font-weight="600" fill="#475569">{proj_name.upper()[:30]} | REF: {ref_code[:18]} | {city_uf.upper()[:20]}</text>
    <text x="395" y="60" font-size="8.5" fill="#64748b">DATA:</text>
    <text x="395" y="73" font-size="10.5" font-weight="700" fill="#0f172a">{today_str}</text>

    <text x="15" y="100" font-size="11" font-weight="700" fill="#0369a1">ESQUEMA HIDRÁULICO E DETALHAMENTO DO SISTEMA PLUVIAL</text>
    <text x="15" y="116" font-size="9.5" fill="#475569">CORTE ESQUEMÁTICO INTEGRADO, QUADRO DE DIMENSIONAMENTO E MATERIAIS</text>
    <text x="395" y="102" font-size="8.5" fill="#64748b">ESCALA:</text>
    <text x="395" y="117" font-size="10.5" font-weight="700" fill="#0f172a">INDICADA</text>

    <text x="15" y="142" font-size="9" fill="#64748b">RESPONSÁVEIS TÉCNICOS:</text>
    <text x="15" y="160" font-size="12" font-weight="800" fill="#064e3b">{technical_responsible[:72]}</text>

    <text x="400" y="142" font-size="9.5" fill="#64748b">PRANCHA:</text>
    <text x="400" y="162" font-size="14" font-weight="800" fill="#0f172a">01 / 01</text>
    <text x="495" y="142" font-size="9.5" fill="#64748b">FORMATO:</text>
    <text x="495" y="162" font-size="13" font-weight="800" fill="#0f172a">A3</text>
  </g>

  <!-- QUADRO 1 — PARÂMETROS DE PROJETO E DIMENSIONAMENTO -->
  <g transform="translate(850, 50)" filter="url(#cardShadow)">
    <rect x="0" y="0" width="515" height="350" fill="#ffffff" stroke="#0f172a" stroke-width="1.4" rx="4" />
    <rect x="0" y="0" width="515" height="30" fill="#064e3b" rx="4" />
    <text x="15" y="20" font-size="11.5" font-weight="700" fill="#ffffff">QUADRO 1 — PARÂMETROS DE PROJETO (NBR 15527:2019)</text>

    <g font-size="10" fill="#1e293b" transform="translate(15, 48)">
      <text y="0">Área de Captação da Cobertura:</text><text x="480" y="0" text-anchor="end" font-weight="700">{tx['area']}</text><line x1="0" y1="5" x2="485" y2="5" stroke="#e2e8f0" />
      <text y="20">Coeficiente de Escoamento Superficial (Runoff C):</text><text x="480" y="20" text-anchor="end" font-weight="700">{_fmt_ptbr(runoff, 2)}</text><line x1="0" y1="25" x2="485" y2="25" stroke="#e2e8f0" />
      <text y="40">Lâmina de Descarte Inicial (First Flush):</text><text x="480" y="40" text-anchor="end" font-weight="700">{_fmt_ptbr(discard_mm, 1)} mm</text><line x1="0" y1="45" x2="485" y2="45" stroke="#e2e8f0" />
      <text y="60">Volume Estimado de Descarte Inicial:</text><text x="480" y="60" text-anchor="end" font-weight="700" fill="#dc2626">{f"{_fmt_milhar(vol_discard)} Litros" if vol_discard > 0 else NAO_INFORMADO}</text><line x1="0" y1="65" x2="485" y2="65" stroke="#e2e8f0" />
      <text y="80">Capacidade da Cisterna Inferior:</text><text x="480" y="80" text-anchor="end" font-weight="800" fill="#0284c7">{tx['volume']}</text><line x1="0" y1="85" x2="485" y2="85" stroke="#e2e8f0" />
      <text y="100">Capacidade do Reservatório Superior Não Potável:</text><text x="480" y="100" text-anchor="end" font-weight="700" fill="#0284c7">{_fmt_milhar(upper_vol)} Litros</text><line x1="0" y1="105" x2="485" y2="105" stroke="#e2e8f0" />
      <text y="120">Demanda Total Diária da Edificação:</text><text x="480" y="120" text-anchor="end" font-weight="700">{tx['demanda']}</text><line x1="0" y1="125" x2="485" y2="125" stroke="#e2e8f0" />
      <text y="140">Demanda Pluvial Substituível Alvo:</text><text x="480" y="140" text-anchor="end" font-weight="700">{tx['alvo']}</text><line x1="0" y1="145" x2="485" y2="145" stroke="#e2e8f0" />
      <text y="160">Potencial de Economia de Água Potável:</text><text x="480" y="160" text-anchor="end" font-weight="800" fill="#059669">{tx['potencial']}</text><line x1="0" y1="165" x2="485" y2="165" stroke="#e2e8f0" />
      <text y="180">Motobomba Recomendada e Vazão (Q):</text><text x="480" y="180" text-anchor="end" font-weight="700" fill="#d97706">{pump_hp} cv ({_fmt_ptbr(pump_kw, 2)} kW) · {_fmt_ptbr(q_m3h, 1)} m³/h</text><line x1="0" y1="185" x2="485" y2="185" stroke="#e2e8f0" />
      <text y="200">Tempo Estimado de Bombeamento (T):</text><text x="480" y="200" text-anchor="end" font-weight="700">{f"{_fmt_ptbr(t_h, 1)} h/dia" if tem_demanda else NAO_CALCULADO}</text><line x1="0" y1="205" x2="485" y2="205" stroke="#e2e8f0" />
      <text y="220">Diâmetro Recalque Econômico:</text><text x="480" y="220" text-anchor="end" font-weight="700" fill="#0284c7">{f"DN {dn_rec} mm (d_calc = {_fmt_ptbr(d_rec_calc_mm, 1)} mm, v = {_fmt_ptbr(v_rec, 2)} m/s)" if tem_demanda else NAO_CALCULADO}</text><line x1="0" y1="225" x2="485" y2="225" stroke="#e2e8f0" />
      <text y="240">Diâmetro Sucção (NBR 5626, D_suc &gt; D_rec):</text><text x="480" y="240" text-anchor="end" font-weight="700" fill="#0284c7">DN {dn_suc} mm (v_suc = {_fmt_ptbr(v_suc, 2)} m/s)</text>
    </g>
  </g>

  <!-- QUADRO 2 — QUANTITATIVO ESTIMADO DE MATERIAIS -->
  <g transform="translate(850, 415)" filter="url(#cardShadow)">
    <rect x="0" y="0" width="515" height="350" fill="#ffffff" stroke="#0f172a" stroke-width="1.4" rx="4" />
    <rect x="0" y="0" width="515" height="28" fill="#1e293b" rx="4" />
    <text x="15" y="19" font-size="11" font-weight="700" fill="#ffffff">QUADRO 2 — LISTA ESTIMATIVA DE CONEXÕES E MATERIAIS</text>

    <g font-size="9.5" font-weight="700" fill="#64748b" transform="translate(15, 44)">
      <text>ITEM</text><text x="40">ESPECIFICAÇÃO NORMATIVA</text><text x="480" text-anchor="end">QUANTIDADE</text>
      <line x1="0" y1="6" x2="485" y2="6" stroke="#0f172a" stroke-width="1.2" />
    </g>

    <g font-size="9" fill="#334155" transform="translate(15, 64)">
      <text y="0">01</text><text x="40" y="0">Calha Semicircular de Alumínio / Aluzinco</text><text x="480" y="0" text-anchor="end">Conf. Beiral</text><line x1="0" y1="4" x2="485" y2="4" stroke="#f1f5f9" />
      <text y="18">02</text><text x="40" y="18">Tubulação Pluvial PVC Série Normal DN 100 mm</text><text x="480" y="18" text-anchor="end" font-weight="600" fill="#0369a1">Conf. Projeto</text><line x1="0" y1="22" x2="485" y2="22" stroke="#f1f5f9" />
      <text y="36">03</text><text x="40" y="36">Tubo PVC Soldável DN {dn_rec} mm (Recalque Econômico)</text><text x="480" y="36" text-anchor="end" font-weight="600" fill="#0369a1">Conf. Projeto</text><line x1="0" y1="40" x2="485" y2="40" stroke="#f1f5f9" />
      <text y="54">04</text><text x="40" y="54">Tubo PVC Soldável DN {dn_suc} mm (Sucção — NBR 5626)</text><text x="480" y="54" text-anchor="end" font-weight="600" fill="#0369a1">Conf. Projeto</text><line x1="0" y1="58" x2="485" y2="58" stroke="#f1f5f9" />
      <text y="72">05</text><text x="40" y="72">Tubo PVC Soldável DN 25 mm (Distribuição Não Potável)</text><text x="480" y="72" text-anchor="end" font-weight="600" fill="#0369a1">Conf. Projeto</text><line x1="0" y1="76" x2="485" y2="76" stroke="#f1f5f9" />
      <text y="90">06</text><text x="40" y="90">Caixa de Descarte Inicial First Flush com Dreno</text><text x="480" y="90" text-anchor="end">1 un</text><line x1="0" y1="94" x2="485" y2="94" stroke="#f1f5f9" />
      <text y="108">07</text><text x="40" y="108">Filtro Mecânico Autolimpante Tela Inox 0,5 mm</text><text x="480" y="108" text-anchor="end">1 un</text><line x1="0" y1="112" x2="485" y2="112" stroke="#f1f5f9" />
      <text y="126">08</text><text x="40" y="126">Freio d'Água Dispersor de Entrada Cisterna DN 100</text><text x="480" y="126" text-anchor="end">1 un</text><line x1="0" y1="130" x2="485" y2="130" stroke="#f1f5f9" />
      <text y="144">09</text><text x="40" y="144">Motobomba Centrífuga {pump_hp} cv c/ Base Antivibratória</text><text x="480" y="144" text-anchor="end">1 un</text><line x1="0" y1="148" x2="485" y2="148" stroke="#f1f5f9" />
      <text y="162">10</text><text x="40" y="162">Válvula de Retenção Vertical Soldável DN {dn_rec} mm</text><text x="480" y="162" text-anchor="end">1 un</text><line x1="0" y1="166" x2="485" y2="166" stroke="#f1f5f9" />
      <text y="180">11</text><text x="40" y="180">Válvula de Pé com Crivo em Latão DN {dn_suc} mm</text><text x="480" y="180" text-anchor="end">1 un</text><line x1="0" y1="184" x2="485" y2="184" stroke="#f1f5f9" />
      <text y="198">12</text><text x="40" y="198">Registros de Gaveta e Esfera Brutos DN {dn_rec} e DN 25</text><text x="480" y="198" text-anchor="end">6 un</text><line x1="0" y1="202" x2="485" y2="202" stroke="#f1f5f9" />
      <text y="216">13</text><text x="40" y="216">Torneiras de Bóia Estanques DN 25 mm (1")</text><text x="480" y="216" text-anchor="end">2 un</text><line x1="0" y1="220" x2="485" y2="220" stroke="#f1f5f9" />
      <text y="234">14</text><text x="40" y="234">Extravasor / Ladrão com Sifão e Tela Anti-insetos</text><text x="480" y="234" text-anchor="end">1 un</text>
    </g>
    <text x="15" y="324" font-size="8.5" fill="#64748b">* Distâncias de tubulação conforme traçado executivo do projeto arquitetônico.</text>
    <text x="15" y="337" font-size="8.5" fill="#0284c7" font-weight="600">* Diâmetros pré-selecionados de acordo com a motobomba via dimensionamento econômico.</text>
  </g>

  <!-- LEGENDA DE SÍMBOLOS HIDRÁULICOS (Canto Inferior Esquerdo) -->
  <g transform="translate(100, 777)">
    <rect x="0" y="0" width="320" height="180" fill="#ffffff" stroke="#0f172a" stroke-width="1.4" rx="4" />
    <rect x="0" y="0" width="320" height="26" fill="#1e293b" rx="4" />
    <text x="12" y="18" font-size="11" font-weight="700" fill="#ffffff">LEGENDA DE SÍMBOLOS HIDRÁULICOS</text>

    <g font-size="9.5" fill="#334155" transform="translate(15, 42)">
      <line x1="0" y1="0" x2="35" y2="0" stroke="#059669" stroke-width="4" />
      <text x="45" y="4">Tubulação Água Pluvial Bruta (AP)</text>

      <line x1="0" y1="25" x2="35" y2="25" stroke="#d97706" stroke-width="4" />
      <text x="45" y="29">Tubulação Recalque Pluvial DN {dn_rec} (REC)</text>

      <line x1="0" y1="50" x2="35" y2="50" stroke="#c026d3" stroke-width="3" />
      <text x="45" y="54">Tubulação Distribuição Não Potável (NP)</text>

      <line x1="0" y1="75" x2="35" y2="75" stroke="#0284c7" stroke-width="3" />
      <text x="45" y="79">Alimentador / Backup Potável (AF)</text>

      <polygon points="12,105 18,100 18,110" fill="#64748b" />
      <polygon points="24,105 18,100 18,110" fill="#64748b" />
      <text x="35" y="108">Reg. Gaveta</text>

      <circle cx="150" cy="105" r="7" fill="none" stroke="#d97706" stroke-width="2" />
      <text x="165" y="108">Motobomba</text>
    </g>
  </g>

  <!-- NOTAS TÉCNICAS (ABNT NBR 15527 / NBR 5626) -->
  <g transform="translate(435, 777)">
    <rect x="0" y="0" width="340" height="180" fill="#ffffff" stroke="#0f172a" stroke-width="1.4" rx="4" />
    <rect x="0" y="0" width="340" height="26" fill="#1e293b" rx="4" />
    <text x="12" y="18" font-size="11" font-weight="700" fill="#ffffff">NOTAS TÉCNICAS (ABNT NBR 15527 / NBR 5626)</text>

    <g font-size="8.5" fill="#334155" transform="translate(12, 38)">
      <text y="0" font-weight="700">1. Separação Física Obrigatória (Air-Gap):</text>
      <text y="13" fill="#64748b">Proibida interconexão direta entre potável e pluvial (folga &gt;= 50 mm).</text>

      <text y="30" font-weight="700">2. Identificação e Segurança Sanitária:</text>
      <text y="43" fill="#64748b">Pontos de consumo devem conter placa indelével 'ÁGUA NÃO POTÁVEL'.</text>

      <text y="60" font-weight="700">3. Extravasores com Sifão e Tela Milimétrica:</text>
      <text y="73" fill="#64748b">Proteção contra entrada de roedores, mosquitos e retorno de odores.</text>

      <text y="90" font-weight="700">4. Dimensionamento Hidráulico (NBR 5626):</text>
      <text y="103" fill="#64748b">D_rec = 1,3·(T/24)^0,25·√Q: Recalque DN {dn_rec} mm | Sucção DN {dn_suc} mm.</text>
      <text y="116" fill="#64748b">Distâncias de tubulação conforme traçado executivo do projeto.</text>
    </g>
  </g>

  <!-- ÁREA GRÁFICA PRINCIPAL — CORTE ESQUEMÁTICO DE ENGENHARIA -->
  <g transform="translate(100, 60)">
    <text x="0" y="20" font-size="15" font-weight="800" fill="#0f172a">CORTE ESQUEMÁTICO HIDRÁULICO DO SISTEMA PREDIAL</text>
    <text x="0" y="38" font-size="11" font-weight="600" fill="#64748b">DIMENSIONAMENTO CONFORME ABNT NBR 15527:2019 E NBR 5626 | ESCALA INDICADA</text>

    <!-- 1. Telhado Cerâmico com Caimento (x=30 a 260) -->
    <polygon points="30,160 145,80 260,160 245,160 145,95 45,160" fill="#e2e8f0" stroke="#0f172a" stroke-width="2" />
    <text x="145" y="70" text-anchor="middle" font-size="11" font-weight="700" fill="#064e3b">COBERTURA DE CAPTAÇÃO: {tx['area_int']} (C = {_fmt_ptbr(runoff, 2)})</text>
    <text x="55" y="115" font-size="10" font-weight="600" fill="#64748b">i = ___%</text>

    <!-- Calha e Bocal -->
    <rect x="255" y="155" width="22" height="15" rx="3" fill="#059669" stroke="#064e3b" stroke-width="1.5" />
    <text x="282" y="167" font-size="10" font-weight="700" fill="#059669">CALHA (i &gt;= 0,5%)</text>

    <!-- Tubo de Queda Pluvial (TQP DN 100 mm) -->
    <line x1="266" y1="170" x2="266" y2="300" stroke="#059669" stroke-width="6" stroke-linecap="round" />
    <text x="278" y="235" font-size="10" font-weight="600" fill="#059669">TQP DN 100 mm</text>

    <!-- Filtro Autolimpante -->
    <rect x="245" y="300" width="45" height="35" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="2" />
    <line x1="245" y1="325" x2="290" y2="310" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3" />
    <text x="235" y="322" text-anchor="end" font-size="10" font-weight="700" fill="#dc2626">FILTRO AUTOLIMPANTE (Tela Inox 0,5 mm)</text>

    <!-- Tubo First Flush e Dreno -->
    <line x1="266" y1="335" x2="266" y2="430" stroke="#dc2626" stroke-width="6" />
    <circle cx="266" cy="435" r="5" fill="#dc2626" />
    <text x="255" y="380" text-anchor="end" font-size="10" font-weight="600" fill="#dc2626">FIRST FLUSH ({_fmt_ptbr(discard_mm, 1)} mm = {_fmt_milhar(vol_discard)} L)</text>
    <text x="255" y="440" text-anchor="end" font-size="9" fill="#64748b">Dreno c/ Registro de Limpeza</text>

    <!-- Tubo da Água Filtrada para a Cisterna -->
    <path d="M 290 315 L 345 315 L 345 520" fill="none" stroke="#0284c7" stroke-width="6" stroke-linecap="round" />

    <!-- 2. Cisterna Inferior de Concreto Armado (x=320 a 500, y=480 a 630) -->
    <g transform="translate(320, 480)">
      <rect x="-6" y="-6" width="192" height="162" fill="#e2e8f0" stroke="#475569" stroke-width="2" rx="8" />
      <rect x="0" y="0" width="180" height="150" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="6" />
      <rect x="5" y="35" width="170" height="110" fill="#bae6fd" opacity="0.85" rx="4" />
      <line x1="5" y1="35" x2="175" y2="35" stroke="#0369a1" stroke-width="1.5" stroke-dasharray="4" />
      <text x="100" y="65" text-anchor="middle" font-size="13" font-weight="800" fill="#0369a1">Cisterna: {tx['volume_l']}</text>

      <!-- Freio d'Água (Dispersor) no Fundo -->
      <path d="M 25 0 L 25 135 A 8 8 0 0 0 41 135" fill="none" stroke="#0284c7" stroke-width="5" stroke-linecap="round" />
      <text x="35" y="148" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0369a1">Freio d'Água (Dispersor)</text>

      <!-- Tampa Hermética -->
      <rect x="65" y="-14" width="50" height="12" rx="3" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.5" />
      <text x="90" y="-18" text-anchor="middle" font-size="9" fill="#475569">Tampa Hermética DN 600</text>

      <!-- Extravasor / Ladrão Sifonado com Tela (Lado Esquerdo da Cisterna) -->
      <path d="M 0 40 L -35 40 L -35 90 L -55 90" fill="none" stroke="#64748b" stroke-width="3.5" />
      <line x1="-55" y1="85" x2="-55" y2="95" stroke="#dc2626" stroke-width="2" />
      <text x="-40" y="30" text-anchor="end" font-size="9" font-weight="700" fill="#475569">LADRÃO C/ SIFÃO E TELA</text>
      <text x="-40" y="105" text-anchor="end" font-size="8.5" fill="#64748b">-&gt; Drenagem Pluvial</text>
    </g>

    <!-- 3. Conjunto Motobomba e Recalque (x=530, y=560) -->
    <g transform="translate(530, 560)">
      <path d="M -30 0 L 10 0" fill="none" stroke="#059669" stroke-width="4" />
      <text x="-10" y="-14" text-anchor="middle" font-size="8.5" font-weight="700" fill="#059669">Sucção</text>
      <text x="-10" y="-3" text-anchor="middle" font-size="8.5" font-weight="700" fill="#059669">DN {dn_suc}</text>
      <circle cx="20" cy="0" r="14" fill="#fef3c7" stroke="#d97706" stroke-width="2" />
      <text x="20" y="4" text-anchor="middle" font-size="8.5" font-weight="800" fill="#d97706">BOMBA</text>
      <text x="20" y="24" text-anchor="middle" font-size="9" font-weight="700" fill="#d97706">{pump_hp} cv</text>

      <line x1="34" y1="0" x2="55" y2="0" stroke="#d97706" stroke-width="4" />
      <!-- Prumada de Recalque subindo até o Reservatório Superior -->
      <path d="M 55 0 L 55 -410 L -40 -410" fill="none" stroke="#d97706" stroke-width="4" stroke-linecap="round" />
      <text x="65" y="-320" font-size="10" font-weight="700" fill="#d97706">Recalque</text>
      <text x="65" y="-306" font-size="10" font-weight="700" fill="#d97706">DN {dn_rec}</text>
    </g>

    <!-- 4. Reservatório Superior Não Potável (x=410 a 530, y=100 a 190) -->
    <g transform="translate(410, 100)">
      <rect x="0" y="0" width="120" height="90" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" rx="4" />
      <rect x="5" y="25" width="110" height="60" fill="#bae6fd" opacity="0.8" rx="3" />
      <text x="60" y="18" text-anchor="middle" font-size="11" font-weight="800" fill="#0369a1">SUPERIOR: {_fmt_milhar(upper_vol)} L</text>
      <text x="60" y="55" text-anchor="middle" font-size="11" font-weight="700" fill="#0284c7">Água Não Potável</text>

      <!-- Backup de Água Potável com AIR-GAP: à direita e para cima -->
      <path d="M -70 -15 L -20 -15 L -20 10" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round" />
      <text x="5" y="-18" text-anchor="start" font-size="8.5" font-weight="700" fill="#0284c7">BACKUP POTÁVEL (AIR-GAP &gt;= 50 mm)</text>
    </g>

    <!-- 5. Barrilete e Ramais de Distribuição Não Potável (x=530 para a direita) -->
    <g transform="translate(530, 145)">
      <path d="M 0 0 L 80 0 L 80 320" fill="none" stroke="#c026d3" stroke-width="4" stroke-linecap="round" />
      <text x="88" y="100" font-size="9" font-weight="700" fill="#c026d3">DISTRIBUIÇÃO NÃO POTÁVEL</text>

      <!-- Ramal 1: Bacias Sanitárias (y=140) -->
      <line x1="80" y1="140" x2="110" y2="140" stroke="#c026d3" stroke-width="3" />
      <rect x="110" y="130" width="90" height="28" rx="4" fill="#fdf4ff" stroke="#c026d3" stroke-width="1.2" />
      <text x="155" y="144" text-anchor="middle" font-size="8.5" font-weight="700" fill="#86198f">🚽 Bacias (VS/MT)</text>
      <text x="155" y="154" text-anchor="middle" font-size="7.5" font-weight="700" fill="#c026d3">[NÃO POTÁVEL]</text>

      <!-- Ramal 2: Máquina de Lavar / Tanque (y=210) -->
      <line x1="80" y1="210" x2="110" y2="210" stroke="#c026d3" stroke-width="3" />
      <rect x="110" y="200" width="90" height="28" rx="4" fill="#fdf4ff" stroke="#c026d3" stroke-width="1.2" />
      <text x="155" y="214" text-anchor="middle" font-size="8.5" font-weight="700" fill="#86198f">🧺 Máquina / Tanque</text>
      <text x="155" y="224" text-anchor="middle" font-size="7.5" font-weight="700" fill="#c026d3">[NÃO POTÁVEL]</text>

      <!-- Ramal 3: Torneiras de Jardim e Calçadas (y=280) -->
      <line x1="80" y1="280" x2="110" y2="280" stroke="#c026d3" stroke-width="3" />
      <rect x="110" y="270" width="90" height="28" rx="4" fill="#fdf4ff" stroke="#c026d3" stroke-width="1.2" />
      <text x="155" y="284" text-anchor="middle" font-size="8.5" font-weight="700" fill="#86198f">🌿 Jardim / Calçadas</text>
      <text x="155" y="294" text-anchor="middle" font-size="7.5" font-weight="700" fill="#c026d3">[NÃO POTÁVEL]</text>
    </g>

    <!-- BOXES DE DETALHES CONSTRUTIVOS NORMATIVOS (Canto Inferior Esquerdo do Desenho) -->
    <g transform="translate(0, 480)">
      <rect x="0" y="0" width="145" height="75" fill="#ffffff" stroke="#0f172a" stroke-width="1.2" rx="4" />
      <text x="8" y="16" font-size="9" font-weight="800" fill="#0f172a">DET. 01 — FREIO D'ÁGUA</text>
      <path d="M 35 25 L 35 55 A 10 10 0 0 0 55 55 L 55 45" fill="none" stroke="#0284c7" stroke-width="3" />
      <text x="70" y="38" font-size="8" fill="#475569">Entrada suave sem</text>
      <text x="70" y="50" font-size="8" fill="#475569">ressuspensão de lodo</text>

      <rect x="0" y="85" width="145" height="75" fill="#ffffff" stroke="#0f172a" stroke-width="1.2" rx="4" />
      <text x="8" y="101" font-size="9" font-weight="800" fill="#0f172a">DET. 02 — SIFÃO C/ TELA INOX</text>
      <path d="M 25 125 L 45 125 L 45 145 L 60 145 L 60 135 L 75 135" fill="none" stroke="#475569" stroke-width="2.5" />
      <line x1="75" y1="130" x2="75" y2="140" stroke="#dc2626" stroke-width="2" />
      <text x="78" y="132" font-size="7.5" fill="#475569">Proteção anti-insetos</text>
      <text x="78" y="144" font-size="7.5" fill="#475569">e barreira de odores</text>
    </g>
  </g>
</svg>"""


def _generate_simple_svg(project_data: Dict[str, Any]) -> str:
    """Gera esquema unifilar simples e moderno em SVG."""
    proj_name = project_data.get("project_name", "Projeto Sem Nome") or "Projeto Triton"
    ref_code = project_data.get("ref_code", "N5-SIMPLES")
    organization = escape(str(project_data.get("organization") or "TRITON"))
    technical_responsible = escape(str(project_data.get("technical_responsible") or "A DEFINIR PELO PROJETISTA"))
    proj_name = escape(str(proj_name))
    ref_code = escape(str(ref_code))

    tx = textos_do_quadro(project_data)
    area = _safe_float(project_data.get("area"), 150.0)
    runoff = _safe_float(project_data.get("runoff"), COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard_mm = _safe_float(project_data.get("discard"), 2.0)
    vol_lower = _safe_float(project_data.get("lower_vol"), 5000.0)
    upper_vol = _extract_upper_vol(project_data, 500.0)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 540" width="920" height="540" style="background:#f8fafc; font-family:'Segoe UI', Inter, Helvetica, Arial, sans-serif;">
  <defs>
    <linearGradient id="gradHeader" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="gradRoof" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="gradCistern" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0369a1" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.08" />
    </filter>
  </defs>

  <rect x="20" y="15" width="880" height="55" rx="8" fill="url(#gradHeader)" />
  <text x="40" y="42" fill="#ffffff" font-size="15" font-weight="700">ESQUEMA UNIFILAR — SISTEMA DE APROVEITAMENTO PLUVIAL (NBR 15527)</text>
  <text x="40" y="58" fill="#a7f3d0" font-size="11">Projeto: {proj_name} | Ref: {ref_code} | Organização: {organization} | Resp.: {technical_responsible}</text>

  <g filter="url(#shadow)">
    <polygon points="60,200 190,120 320,200" fill="url(#gradRoof)" stroke="#0f172a" stroke-width="2" />
    <rect x="50" y="196" width="280" height="10" rx="3" fill="#64748b" />
    <rect x="310" y="194" width="22" height="20" rx="4" fill="#087f6b" />
  </g>
  <text x="190" y="175" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="600">Telhado de Captação</text>
  <text x="190" y="190" text-anchor="middle" fill="#94a3b8" font-size="10">Área: {tx['area_int']} | Runoff: {_fmt_ptbr(runoff, 2)}</text>

  <path d="M 321 214 L 321 280 L 370 280" fill="none" stroke="#0284c7" stroke-width="5" stroke-linecap="round" />
  <rect x="360" y="260" width="80" height="40" rx="6" fill="#ffffff" stroke="#0284c7" stroke-width="2" filter="url(#shadow)" />
  <text x="400" y="278" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Filtro + Descarte</text>
  <text x="400" y="292" text-anchor="middle" fill="#64748b" font-size="9.5">First Flush: {_fmt_ptbr(discard_mm, 1)} mm</text>

  <path d="M 440 280 L 490 280 L 490 350" fill="none" stroke="#0284c7" stroke-width="5" stroke-linecap="round" />

  <g filter="url(#shadow)">
    <rect x="440" y="350" width="160" height="130" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
    <rect x="445" y="380" width="150" height="95" rx="6" fill="url(#gradCistern)" opacity="0.85" />
  </g>
  <text x="520" y="372" text-anchor="middle" fill="#0f172a" font-size="13" font-weight="700">Cisterna Inferior</text>
  <text x="520" y="420" text-anchor="middle" fill="#ffffff" font-size="15" font-weight="800">{tx['volume_l']}</text>
  <text x="520" y="440" text-anchor="middle" fill="#e0f2fe" font-size="11">Economia: {tx['potencial_curto']}</text>

  <circle cx="640" cy="460" r="20" fill="#087f6b" stroke="#064e3b" stroke-width="2" filter="url(#shadow)" />
  <text x="640" y="464" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="bold">BOMBA</text>
  <path d="M 570 450 L 620 450 L 620 460" fill="none" stroke="#059669" stroke-width="4" />
  <path d="M 660 460 L 730 460 L 730 180 L 750 180" fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" />

  <g filter="url(#shadow)">
    <rect x="740" y="120" width="120" height="90" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2" />
    <rect x="745" y="145" width="110" height="60" rx="4" fill="url(#gradCistern)" opacity="0.8" />
  </g>
  <text x="800" y="138" text-anchor="middle" fill="#0f172a" font-size="11" font-weight="700">Caixa Superior</text>
  <text x="800" y="178" text-anchor="middle" fill="#ffffff" font-size="13" font-weight="800">{_fmt_milhar(upper_vol)} L</text>
  <text x="800" y="225" text-anchor="middle" fill="#64748b" font-size="9.5">Air-Gap &gt;= 50 mm</text>

  <path d="M 800 210 L 800 480" fill="none" stroke="#d946ef" stroke-width="4" />
  <path d="M 800 310 L 840 310" fill="none" stroke="#d946ef" stroke-width="3" />
  <rect x="840" y="298" width="60" height="24" rx="4" fill="#fdf4ff" stroke="#d946ef" />
  <text x="870" y="314" text-anchor="middle" fill="#86198f" font-size="9" font-weight="bold">🚽 Bacias</text>

  <path d="M 800 380 L 840 380" fill="none" stroke="#d946ef" stroke-width="3" />
  <rect x="840" y="368" width="60" height="24" rx="4" fill="#fdf4ff" stroke="#d946ef" />
  <text x="870" y="384" text-anchor="middle" fill="#86198f" font-size="9" font-weight="bold">🧺 Máquina</text>

  <path d="M 800 450 L 840 450" fill="none" stroke="#d946ef" stroke-width="3" />
  <rect x="840" y="438" width="60" height="24" rx="4" fill="#fdf4ff" stroke="#d946ef" />
  <text x="870" y="454" text-anchor="middle" fill="#86198f" font-size="9" font-weight="bold">🌿 Jardim</text>
</svg>"""


def generate_project_svg_diagram(project_data: Dict[str, Any], output_path: Optional[str] = None, mode: str = "technical_a3") -> str:
    """Gera diagrama vetorial SVG no modo selecionado ('technical_a3', 'simple' ou 'plant_3d')."""
    if mode in {"plant_3d", "planta_3d"}:
        svg_content = generate_schematic_3d_svg(project_data)
    elif mode == "simple":
        svg_content = _generate_simple_svg(project_data)
    else:
        svg_content = _generate_technical_a3_svg(project_data)

    svg_content = svg_de_exportacao(svg_content)

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

    return svg_content
