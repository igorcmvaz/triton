"""Geração de traçado 3D e componentes BIM pré-preenchidos a partir do estudo.

Permite que o projetista visualize a planta e a volumetria 3D imediatamente a
partir dos parâmetros calculados na simulação e nas diretrizes normativas
(ABNT NBR 15527:2019, ABNT NBR 5626:2020 e ABNT NBR 10844:1989), sem ter que
começar de uma tela em branco ou digitar coordenadas manualmente.

Inclui os 5 elementos normativos essenciais de aproveitamento de água de chuva:
1. Filtro pluvial autolimpante de primeiro estágio (FP-01);
2. Reservatório / dispositivo de descarte de primeiras águas - first flush (FF-01);
3. Cisterna de armazenamento inferior (CI-01);
4. Conjunto motobomba de recalque dimensionado (B-01);
5. Reservatório superior de distribuição não potável com backup (RS-01).
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Optional, Tuple

from netuno.core.component_geometry import tank_dimensions_mm
from netuno.core.cad_exporter import _extract_upper_vol, calculate_forchheimer_pumping_diameters
from netuno.core.pump_energy import CV_TO_KW


def _number(value: Any, default: float = 0.0) -> float:
    if value is None or value == "" or value == "-":
        return default
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        num = float(value)
        return num if math.isfinite(num) and num > 0 else default
    except (ValueError, TypeError):
        return default


#: Distância do ralo da cobertura à borda do telhado (mm), onde nasce a captação.
RECUO_DO_RALO_MM = 300.0

#: Potência de placa usual (kW) dos motores de catálogo, por potência em CV.
_KW_DE_PLACA = {1 / 3: 0.25, 0.5: 0.37, 0.75: 0.55, 1.0: 0.75, 1.5: 1.1, 2.0: 1.5, 3.0: 2.2}


def cv_do_rotulo(rotulo: Any) -> Optional[float]:
    """Lê «1/2», «3/4», «1», «1 1/2», «1.1/2» ou «2» como potência em CV.

    O teste por substring (``"1/2" in rotulo``) lia «1 1/2» como meio CV e
    «1/3» como 1 CV.
    """
    texto = str(rotulo or "").strip().lower().replace("cv", "").replace("hp", "").replace(",", ".").strip()
    m = re.fullmatch(r"(?:(\d+)[\s.]+)?(\d+)/(\d+)", texto)
    if m:
        inteiro, num, den = int(m.group(1) or 0), int(m.group(2)), int(m.group(3))
        return inteiro + num / den if den else None
    try:
        valor = float(texto)
    except ValueError:
        return None
    return valor if valor > 0 else None


def potencia_da_motobomba(rotulo: Any, kw_informado: float = 0.0) -> Tuple[float, float]:
    """(CV, kW) da motobomba. O kW informado prevalece; sem nada, ½ CV (0,37 kW)."""
    cv = cv_do_rotulo(rotulo)
    if kw_informado and kw_informado > 0:
        return (cv if cv else kw_informado / CV_TO_KW), kw_informado
    if cv is None:
        cv = 0.5
    kw = next((k for c, k in _KW_DE_PLACA.items() if abs(c - cv) < 1e-6), round(cv * CV_TO_KW, 2))
    return cv, kw


def generate_study_layout(project_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Gera um layout BIM 3D completo e válido baseado nos dados do estudo.

    Parâmetros considerados:
    - ``lower_vol``: volume calculado da cisterna inferior (L).
    - ``upper_vol``: volume do reservatório superior (L).
    - ``area``: área de captação da cobertura (m²).
    - ``discard``: lâmina de descarte inicial (mm; padrão 2 mm conforme NBR 15527).
    - ``floors``: número de pavimentos (padrão 2).
    - Hidráulica da motobomba e diâmetros econômicos de Forchheimer (NBR 5626).
    """
    data = dict(project_data or {})

    # Volumes dimensionados
    lower_vol = _number(data.get("lower_vol"), 5000.0)
    upper_vol = _extract_upper_vol(data, 1000.0)
    area = _number(data.get("area"), 150.0)
    discard = _number(data.get("discard"), 2.0)

    # Volume de descarte inicial (NBR 15527:2019 item 4.3.5)
    ff_vol = round(discard * area, 1)

    # Pavimentos e dimensões da edificação
    bldg_vol = data.get("building_volume") or {}
    floors = int(_number(data.get("floors") or bldg_vol.get("floors"), 2.0))
    floors = max(1, min(floors, 40))
    bldg_h = float(floors * 3000.0)

    # Largura e profundidade proporcionais à área de captação
    bldg_w = max(8000.0, round(math.sqrt(area * 1.5) * 1000.0 / 500.0) * 500.0)
    bldg_d = max(6000.0, round((area / (bldg_w / 1000.0)) * 1000.0 / 500.0) * 500.0)

    # Geometria dos reservatórios (NBR 15527 / NBR 5626)
    d_ci, h_ci, _, _ = tank_dimensions_mm("cisterna_inferior", {}, lower_vol)
    d_rs, h_rs, _, _ = tank_dimensions_mm("reservatorio_superior", {}, upper_vol)
    alt_ci = max(1000.0, round(h_ci / 50.0) * 50.0)
    diam_ci = max(800.0, round(d_ci / 50.0) * 50.0)
    alt_rs = max(600.0, round(h_rs / 50.0) * 50.0)
    diam_rs = max(800.0, round(d_rs / 50.0) * 50.0)

    # Diâmetros de sucção e recalque (Forchheimer / NBR 5626)
    daily_l = _number(data.get("pluv_day"), 800.0)
    pump_hp = str(data.get("pump_hp") or "1/2")
    flow_m3_h = _number(data.get("pump_flow_rate_m3_h"), 0.0)
    pumping = calculate_forchheimer_pumping_diameters(
        pump_flow_rate_m3_h=flow_m3_h,
        daily_pumped_volume_l=daily_l,
        pump_hp=pump_hp
    )
    dn_rec = float(pumping.get("dn_recalque_comercial_mm") or 25.0)
    dn_suc = float(pumping.get("dn_succao_comercial_mm") or 32.0)

    # Potência do motor: a informada em kW prevalece; o rótulo completa o que faltar.
    pump_cv, pump_kw = potencia_da_motobomba(pump_hp, _number(data.get("pump_power_kw"), 0.0))

    flow_l_min = (flow_m3_h * 1000.0 / 60.0) if flow_m3_h > 0 else 60.0
    head_mca = round((bldg_h + alt_ci + 500.0) / 1000.0 + 4.0, 1)

    # Coordenadas dos componentes (em mm, z para cima)
    # Cisterna enterrada no recuo externo
    x_ci = -1500.0 - diam_ci / 4.0
    y_ci = 1500.0 + diam_ci / 4.0
    z_ci = -alt_ci

    # Motobomba no abrigo térreo
    x_b = 500.0
    y_b = y_ci
    z_b = 0.0

    # Reservatório superior na cobertura (barrilete sobre a laje superior)
    x_rs = min(bldg_w - 2000.0, max(3000.0, bldg_w * 0.5))
    y_rs = min(bldg_d - 2000.0, max(2500.0, bldg_d * 0.5))
    z_rs = bldg_h + 500.0

    # Filtro pluvial e reservatório de descarte na descida da prumada pluvial
    x_fp = x_ci - 1500.0
    y_fp = y_ci
    z_fp = 1200.0
    h_fp = 600.0
    diam_fp = 320.0

    x_ff = x_fp
    y_ff = y_fp - 900.0
    z_ff = 0.0
    h_ff = 900.0
    diam_ff = 400.0

    dn_capt = 150.0 if area > 200.0 else 100.0

    components: List[Dict[str, Any]] = [
        {
            "instance_id": "FP-01",
            "type_id": "filtro_pluvial",
            "level": "Área externa / Térreo",
            "position_mm": {"x": x_fp, "y": y_fp, "z": z_fp},
            "rotation_deg": 0.0,
            "parameters": {
                "DN_MM": dn_capt,
                "MALHA_MM": 0.35,
                "EFICIENCIA_PCT": 90.0,
                "DIAMETRO_MM": diam_fp,
                "ALTURA_MM": h_fp,
                "TIPO": "Filtro Pluvial Autolimpante Vórtex (Aço Inox 304)",
            },
        },
        {
            "instance_id": "FF-01",
            "type_id": "first_flush",
            "level": "Área externa / Térreo",
            "position_mm": {"x": x_ff, "y": y_ff, "z": z_ff},
            "rotation_deg": 0.0,
            "parameters": {
                "VOLUME_L": ff_vol,
                "DESCARTE_MM": discard,
                "DIAMETRO_MM": diam_ff,
                "ALTURA_MM": h_ff,
                "MECANISMO": "Boia flutuante de vedação por esfera e válvula de purga lenta calibrada",
            },
        },
        {
            "instance_id": "CI-01",
            "type_id": "cisterna_inferior",
            "level": "Subsolo / Enterrada",
            "position_mm": {"x": x_ci, "y": y_ci, "z": z_ci},
            "rotation_deg": 0.0,
            "parameters": {
                "CAPACIDADE_L": lower_vol,
                "DIAMETRO_MM": diam_ci,
                "ALTURA_MM": alt_ci,
                "MATERIAL": "PEAD rotomoldado com proteção UV",
            },
        },
        {
            "instance_id": "B-01",
            "type_id": "motobomba",
            "level": "Térreo",
            "position_mm": {"x": x_b, "y": y_b, "z": z_b},
            "rotation_deg": 0.0,
            "parameters": {
                "POTENCIA_KW": round(pump_kw, 2),
                "POTENCIA_CV": round(pump_cv, 2),
                "POTENCIA_HP_LABEL": pump_hp,
                "VAZAO_L_MIN": round(flow_l_min, 1),
                "VAZAO_M3_H": round(flow_l_min * 0.06, 2),
                "ALTURA_MCA": head_mca,
                "DN_SUCCAO_MM": dn_suc,
                "DN_RECALQUE_MM": dn_rec,
            },
        },
        {
            "instance_id": "RS-01",
            "type_id": "reservatorio_superior",
            "level": f"Cobertura (+{bldg_h/1000:.1f} m)",
            "position_mm": {"x": x_rs, "y": y_rs, "z": z_rs},
            "rotation_deg": 0.0,
            "parameters": {
                "CAPACIDADE_L": upper_vol,
                "DIAMETRO_MM": diam_rs,
                "ALTURA_MM": alt_rs,
                "MATERIAL": "Polietileno de Alta Densidade (PEAD)",
            },
        },
    ]

    # Geometria dos trechos de tubulação
    offset_rec = 900.0
    dx_shaft = (x_rs - offset_rec) - x_b
    dy_shaft = y_rs - y_b
    h_topo = z_rs + alt_rs
    dz_sobe = h_topo + 300.0

    # Distância horizontal do filtro para a cisterna
    dx_fp_ci = x_ci - (x_fp + diam_fp / 2.0)
    dz_fp_ci = (z_fp + h_fp * 0.85 - 20.0) - (z_ci + alt_ci)

    runs: List[Dict[str, Any]] = [
        {
            "run_id": "T-01",
            "system": "captacao",
            "dn_mm": dn_capt,
            "material": "PVC",
            "level": "Cobertura",
            # Nasce no ralo da cobertura, junto à borda do telhado do lado do
            # filtro, e corre para fora até a vertical do filtro. Antes começava
            # no ar, 1,5 m além do filtro, e apontava para longe da edificação.
            "start": {"x": RECUO_DO_RALO_MM, "y": y_fp, "z": bldg_h},
            "route": f"d {x_fp - RECUO_DO_RALO_MM:g} 0 -20; desce {(bldg_h - 20.0) - (z_fp + h_fp):g}",
            "end": "FP-01:topo",
        },
        {
            "run_id": "T-02",
            "system": "descarte",
            "dn_mm": dn_capt,
            "material": "PVC",
            "level": "Térreo",
            "start": "FP-01:fundo",
            "route": f"d 0 -900 -15; desce {(z_fp - 15.0) - (z_ff + h_ff):g}",
            "end": "FF-01:topo",
        },
        {
            "run_id": "T-03",
            "system": "captacao",
            "dn_mm": dn_capt,
            "material": "PVC",
            "level": "Térreo",
            "start": "FP-01:sup+x",
            "route": f"d {dx_fp_ci:g} 0 -20; desce {dz_fp_ci:g}",
            "end": "CI-01:topo",
        },
        {
            "run_id": "T-04",
            "system": "succao",
            "dn_mm": dn_suc,
            "material": "PVC",
            "level": "Térreo",
            "start": "CI-01",
            "route": f"sobe {alt_ci:g}; +x {x_b - x_ci:g}",
            "end": "B-01",
        },
        {
            "run_id": "T-05",
            "system": "recalque",
            "dn_mm": dn_rec,
            "material": "PVC",
            "level": "Prumada",
            "start": "B-01",
            "route": f"+x {dx_shaft:g}; +y {dy_shaft:g}; sobe {dz_sobe:g}; +x {offset_rec:g}; desce 300",
            "end": "RS-01:topo",
        },
        {
            "run_id": "T-06",
            "system": "distribuicao",
            "dn_mm": 25.0,
            "material": "PVC",
            "level": "Barrilete",
            "start": "RS-01:fundo",
            "route": f"desce {z_rs - 1000.0:g}; -y 2000",
            "end": None,
        },
    ]

    building_volume: Dict[str, Any] = {
        "origin_mm": {"x": 0.0, "y": 0.0, "z": 0.0},
        "width_mm": bldg_w,
        "depth_mm": bldg_d,
        "height_mm": bldg_h,
        "floors": floors,
    }

    return {
        "bim_components": components,
        "pipe_runs": runs,
        "building_volume": building_volume,
    }
