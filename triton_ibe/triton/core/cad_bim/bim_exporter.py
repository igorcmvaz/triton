"""Intercâmbio BIM neutro para CAD, Revit e outras ferramentas.

O arquivo JSON não finge ser um modelo ``.rvt``. Ele registra, em unidades e
campos explícitos, os tipos calculados pelo Triton e as instâncias posicionadas
que o projetista informou. A criação de elementos nativos deve ocorrer dentro
do Revit, onde a Autodesk Revit API está disponível.

A versão 1.1 acrescenta os trechos de tubulação organizados pelo projetista
(``pipe_runs``), já resolvidos em vértices 3D na ordem de montagem. A 1.0
continua legível: é a 1.1 sem trechos.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from triton.core.component_geometry import fallback_volumes
from triton.core.pipe_network import PIPE_SYSTEMS, resolve_pipe_network


BIM_SCHEMA = "https://triton.local/schemas/bim-interchange-1.1.json"
BIM_SCHEMA_VERSION = "1.1"
SUPPORTED_SCHEMA_VERSIONS = ("1.0", "1.1")


COMPONENT_TYPES: List[Dict[str, Any]] = [
    {"type_id": "cisterna_inferior", "cad_block": "TRITON_CISTERNA_PLANTA", "revit_category": "OST_PlumbingFixtures", "parameters": ["CAPACIDADE_L", "DIAMETRO_MM", "ALTURA_MM"]},
    {"type_id": "reservatorio_superior", "cad_block": "TRITON_RES_SUP_PLANTA", "revit_category": "OST_PlumbingFixtures", "parameters": ["CAPACIDADE_L", "LARGURA_MM", "COMPRIMENTO_MM", "ALTURA_MM"]},
    {"type_id": "filtro_pluvial", "cad_block": "TRITON_FILTRO_PLUVIAL", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "MALHA_MM"]},
    {"type_id": "first_flush", "cad_block": "TRITON_FIRST_FLUSH", "revit_category": "OST_PipeAccessory", "parameters": ["VOLUME_L", "DESCARTE_MM"]},
    {"type_id": "motobomba", "cad_block": "TRITON_MOTOBOMBA", "revit_category": "OST_MechanicalEquipment", "parameters": ["POTENCIA_KW", "VAZAO_L_MIN", "ALTURA_MCA"]},
    {"type_id": "registro_gaveta", "cad_block": "TRITON_REG_GAVETA", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM"]},
    {"type_id": "registro_esfera", "cad_block": "TRITON_REG_ESFERA", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM"]},
    {"type_id": "valvula_retencao", "cad_block": "TRITON_VALV_RETENCAO", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM"]},
    {"type_id": "air_gap", "cad_block": "TRITON_AIR_GAP", "revit_category": "OST_PipeAccessory", "parameters": ["FOLGA_MM", "DN_MM"]},
    {"type_id": "ladrao_sifonado", "cad_block": "TRITON_LADRAO_SIFONADO", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "MALHA_MM"]},
    {"type_id": "ponto_nao_potavel", "cad_block": "TRITON_PONTO_NAO_POTAVEL", "revit_category": "OST_PlumbingFixtures", "parameters": ["USO", "DN_MM"]},
    # Arranjo normativo completo (ABNT NBR 15527:2019 e NBR 5626:2020): entrada
    # calma na cisterna, captação flutuante, comando por nível e o backup potável
    # com hidrômetro e válvula solenoide descarregando por separação atmosférica.
    {"type_id": "freio_dagua", "cad_block": "TRITON_FREIO_DAGUA", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM"]},
    {"type_id": "succao_flutuante", "cad_block": "TRITON_SUCCAO_FLUTUANTE", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "PROFUNDIDADE_MM"]},
    {"type_id": "sensor_nivel", "cad_block": "TRITON_SENSOR_NIVEL", "revit_category": "OST_ElectricalFixtures", "parameters": ["FUNCAO"]},
    {"type_id": "valvula_solenoide", "cad_block": "TRITON_VALV_SOLENOIDE", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "TENSAO_V"]},
    {"type_id": "hidrometro", "cad_block": "TRITON_HIDROMETRO", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "VAZAO_NOMINAL_M3_H"]},
    {"type_id": "valvula_pe_crivo", "cad_block": "TRITON_VALV_PE_CRIVO", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM"]},
    {"type_id": "respiro", "cad_block": "TRITON_RESPIRO", "revit_category": "OST_PipeAccessory", "parameters": ["DN_MM", "ALTURA_MM"]},
    {"type_id": "quadro_comando", "cad_block": "TRITON_QUADRO_COMANDO", "revit_category": "OST_ElectricalEquipment", "parameters": ["TENSAO_V", "FUNCAO"]},
]


def _number(value: Any, default: float = 0.0) -> float:
    try:
        if isinstance(value, str):
            value = value.strip().replace(",", ".")
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalise_instances(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    known = {item["type_id"] for item in COMPONENT_TYPES}
    instances: List[Dict[str, Any]] = []
    for index, raw in enumerate(items):
        type_id = str(raw.get("type_id", "")).strip()
        if type_id not in known:
            raise ValueError(f"Tipo BIM desconhecido: {type_id or '<vazio>'}")
        position = raw.get("position_mm", {})
        rotation = _number(raw.get("rotation_deg"), 0.0)
        instances.append({
            "instance_id": str(raw.get("instance_id") or f"NET-{index + 1:03d}"),
            "type_id": type_id,
            "level": str(raw.get("level") or "Nível 0"),
            "position_mm": {
                "x": _number(position.get("x")),
                "y": _number(position.get("y")),
                "z": _number(position.get("z")),
            },
            "rotation_deg": rotation,
            "parameters": dict(raw.get("parameters") or {}),
        })
    return instances


def build_bim_manifest(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Monta o manifesto BIM auditável, sem inventar coordenadas de projeto."""
    project_name = str(project_data.get("project_name") or "Projeto Triton")
    ref_code = str(project_data.get("ref_code") or "SEM-REFERENCIA")
    lower_vol = _number(project_data.get("lower_vol"), 0.0)
    upper_vol = _number(project_data.get("upper_vol"), 0.0)
    discard_mm = _number(project_data.get("discard"), 0.0)
    area = _number(project_data.get("area"), 0.0)
    instances = _normalise_instances(project_data.get("bim_components") or [])
    pipe_runs, pipe_errors, pipe_warnings = resolve_pipe_network(
        instances, project_data.get("pipe_runs") or [], fallback_volumes(project_data)
    )

    return {
        "$schema": BIM_SCHEMA,
        "schema_version": BIM_SCHEMA_VERSION,
        "generator": {"application": "Triton", "format": "BIM interchange", "generated_at_utc": datetime.now(timezone.utc).isoformat()},
        "project": {
            "name": project_name,
            "reference": ref_code,
            "location": str((project_data.get("audit_context") or {}).get("climate_location") or "Não informada"),
            "coordinate_status": "local_unreferenced",
        },
        "units": {"axis_up": "z", "length": "millimetre", "volume": "litre", "flow": "litre_per_minute", "power": "kilowatt", "rotation": "degree"},
        "calculated_design": {
            "catchment_area_m2": area,
            "first_flush_depth_mm": discard_mm,
            "lower_storage_l": lower_vol,
            "upper_storage_l": upper_vol,
            "note": "Valores de cálculo; confirmar seleção comercial e compatibilização antes da execução.",
        },
        "component_types": COMPONENT_TYPES,
        "instances": instances,
        "pipe_systems": [{k: item[k] for k in ("system_id", "label", "gravity")} for item in PIPE_SYSTEMS],
        "pipe_runs": pipe_runs,
        "validation": {"errors": pipe_errors, "warnings": pipe_warnings},
    }


def validate_bim_manifest(manifest: Dict[str, Any]) -> List[str]:
    """Retorna problemas estruturais que impediriam a importação no Revit."""
    errors: List[str] = []
    if manifest.get("schema_version") not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append("Versão de esquema BIM não suportada.")
    if not manifest.get("project", {}).get("name"):
        errors.append("Nome do projeto ausente.")
    type_ids = {item.get("type_id") for item in manifest.get("component_types", [])}
    seen = set()
    for instance in manifest.get("instances", []):
        instance_id = instance.get("instance_id")
        if not instance_id or instance_id in seen:
            errors.append(f"Identificador de instância ausente ou duplicado: {instance_id!r}.")
        seen.add(instance_id)
        if instance.get("type_id") not in type_ids:
            errors.append(f"Tipo inexistente na instância {instance_id!r}.")
        if set((instance.get("position_mm") or {}).keys()) != {"x", "y", "z"}:
            errors.append(f"Coordenadas incompletas na instância {instance_id!r}.")
    errors.extend((manifest.get("validation") or {}).get("errors") or [])
    return errors


def write_bim_manifest(project_data: Dict[str, Any], output_path: str) -> str:
    """Grava o manifesto em UTF-8 e valida a estrutura antes da escrita."""
    manifest = build_bim_manifest(project_data)
    errors = validate_bim_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
