"""Geração de traçado 3D e componentes BIM pré-preenchidos a partir do estudo.

Permite que o projetista visualize a planta e a volumetria 3D imediatamente a
partir dos parâmetros calculados na simulação e nas diretrizes normativas
(ABNT NBR 15527:2019, ABNT NBR 5626:2020 e ABNT NBR 10844:1989), sem ter que
começar de uma tela em branco ou digitar coordenadas manualmente.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from netuno.core.component_geometry import tank_dimensions_mm
from netuno.core.cad_exporter import _extract_upper_vol, calculate_forchheimer_pumping_diameters


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

    components: List[Dict[str, Any]] = [
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
            },
        },
        {
            "instance_id": "B-01",
            "type_id": "motobomba",
            "level": "Térreo",
            "position_mm": {"x": x_b, "y": y_b, "z": z_b},
            "rotation_deg": 0.0,
            "parameters": {
                "POTENCIA_KW": 0.37,
                "VAZAO_L_MIN": 60.0,
                "ALTURA_MCA": 12.0,
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
            },
        },
    ]

    # Geometria dos trechos de tubulação
    offset_rec = 900.0
    dx_shaft = (x_rs - offset_rec) - x_b
    dy_shaft = y_rs - y_b
    h_topo = z_rs + alt_rs
    dz_sobe = h_topo + 300.0

    runs: List[Dict[str, Any]] = [
        {
            "run_id": "T-01",
            "system": "captacao",
            "dn_mm": 100.0,
            "material": "PVC",
            "level": "Cobertura",
            "start": {"x": x_ci - 1500.0, "y": y_ci, "z": bldg_h},
            "route": f"d 1500 0 -20; desce {bldg_h - 20:g}",
            "end": "CI-01:topo",
        },
        {
            "run_id": "T-02",
            "system": "succao",
            "dn_mm": dn_suc,
            "material": "PVC",
            "level": "Térreo",
            "start": "CI-01",
            "route": f"sobe {alt_ci:g}; +x {x_b - x_ci:g}",
            "end": "B-01",
        },
        {
            "run_id": "T-03",
            "system": "recalque",
            "dn_mm": dn_rec,
            "material": "PVC",
            "level": "Prumada",
            "start": "B-01",
            "route": f"+x {dx_shaft:g}; +y {dy_shaft:g}; sobe {dz_sobe:g}; +x {offset_rec:g}; desce 300",
            "end": "RS-01:topo",
        },
        {
            "run_id": "T-04",
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
