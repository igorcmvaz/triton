"""Importador Triton para execução dentro do pyRevit.

Este script deve ser iniciado pelo Revit/pyRevit, pois somente esse processo
disponibiliza ``Autodesk.Revit.DB`` e um documento RVT ativo.

A partir do manifesto 1.1, os trechos de tubulação são criados como ``Pipe``
nativos, segmento a segmento e na ordem organizada pelo projetista; segmentos
consecutivos são unidos por curva (mudança de direção) ou luva (colineares).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from Autodesk.Revit.DB import (  # type: ignore
    BuiltInParameter,
    FamilySymbol,
    FilteredElementCollector,
    Level,
    StorageType,
    Transaction,
    UnitTypeId,
    UnitUtils,
    XYZ,
)
from Autodesk.Revit.DB.Plumbing import Pipe, PipeType, PipingSystemType  # type: ignore
from Autodesk.Revit.DB.Structure import StructuralType  # type: ignore
from pyrevit import forms, revit  # type: ignore


def _symbols(document):
    return list(FilteredElementCollector(document).OfClass(FamilySymbol))


def _levels(document):
    return {level.Name: level for level in FilteredElementCollector(document).OfClass(Level)}


SUPPORTED_SCHEMA_VERSIONS = ("1.0", "1.1")


def _mm(value):
    return UnitUtils.ConvertToInternalUnits(float(value), UnitTypeId.Millimeters)


def _point(raw):
    return XYZ(_mm(raw["x"]), _mm(raw["y"]), _mm(raw["z"]))


def _by_name(document, cls):
    return {element.Name: element for element in FilteredElementCollector(document).OfClass(cls)}


def _resolve_symbol(symbols, mapping, type_id):
    target = mapping.get(type_id, {})
    family_name = target.get("family")
    type_name = target.get("type")
    return next(
        (
            symbol
            for symbol in symbols
            if symbol.Family.Name == family_name and symbol.Name == type_name
        ),
        None,
    )


def _set_parameter(element, name, value):
    parameter = element.LookupParameter(name)
    if parameter is None or parameter.IsReadOnly:
        return False
    if parameter.StorageType == StorageType.String:
        parameter.Set(str(value))
    elif parameter.StorageType == StorageType.Integer:
        parameter.Set(int(round(float(value))))
    elif parameter.StorageType == StorageType.Double:
        number = float(value)
        if name.endswith("_MM"):
            number = UnitUtils.ConvertToInternalUnits(number, UnitTypeId.Millimeters)
        parameter.Set(number)
    else:
        return False
    return True


def import_manifest(document, manifest_path, mapping_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if manifest.get("schema_version") not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError("Versão do manifesto Triton não suportada.")
    mapping = json.loads(Path(mapping_path).read_text(encoding="utf-8-sig"))
    symbols = _symbols(document)
    levels = _levels(document)
    missing, created = [], []
    unjoined = []

    transaction = Transaction(document, "Importar componentes Triton")
    try:
        transaction.Start()
        for item in manifest.get("instances", []):
            symbol = _resolve_symbol(symbols, mapping, item["type_id"])
            level = levels.get(item.get("level"))
            if symbol is None or level is None:
                missing.append(item["instance_id"])
                continue
            if not symbol.IsActive:
                symbol.Activate()
                document.Regenerate()
            point = _point(item["position_mm"])
            element = document.Create.NewFamilyInstance(point, symbol, level, StructuralType.NonStructural)
            rotation = math.radians(float(item.get("rotation_deg", 0.0)))
            if abs(rotation) > 1e-9:
                from Autodesk.Revit.DB import ElementTransformUtils, Line  # type: ignore
                axis = Line.CreateBound(point, point + XYZ.BasisZ)
                ElementTransformUtils.RotateElement(document, element.Id, axis, rotation)
            _set_parameter(element, "TRITON_ID", item["instance_id"])
            for name, value in item.get("parameters", {}).items():
                _set_parameter(element, name, value)
            created.append(item["instance_id"])
        _import_pipe_runs(document, manifest, mapping, levels, created, missing, unjoined)
        transaction.Commit()
    except Exception:
        if transaction.HasStarted():
            transaction.RollBack()
        raise
    finally:
        transaction.Dispose()
    return created, missing, unjoined


def _connector_at(pipe, point):
    return min(pipe.ConnectorManager.Connectors, key=lambda connector: connector.Origin.DistanceTo(point))


def _import_pipe_runs(document, manifest, mapping, levels, created, missing, unjoined):
    """Cria os trechos na ordem do manifesto; nada é trocado silenciosamente."""
    config = mapping.get("_tubulacoes", {})
    systems = _by_name(document, PipingSystemType)
    pipe_types = _by_name(document, PipeType)
    for run in manifest.get("pipe_runs", []):
        system = systems.get(config.get("sistemas", {}).get(run["system"]))
        type_name = config.get("tipos_por_material", {}).get(run.get("material")) or config.get("tipo_padrao")
        pipe_type = pipe_types.get(type_name)
        level = levels.get(run.get("level"))
        if system is None or pipe_type is None or level is None:
            missing.append(run["run_id"])
            continue
        previous = None
        for index, segment in enumerate(run["segments"], start=1):
            start, end = _point(segment["start_mm"]), _point(segment["end_mm"])
            pipe = Pipe.Create(document, system.Id, pipe_type.Id, level.Id, start, end)
            pipe.get_Parameter(BuiltInParameter.RBS_PIPE_DIAMETER_PARAM).Set(_mm(run["dn_mm"]))
            _set_parameter(pipe, "TRITON_ID", "{}.{}".format(run["run_id"], index))
            if previous is not None:
                first, second = _connector_at(previous, start), _connector_at(pipe, start)
                try:
                    before = (previous.Location.Curve.GetEndPoint(1) - previous.Location.Curve.GetEndPoint(0)).Normalize()
                    after = (end - start).Normalize()
                    if before.IsAlmostEqualTo(after):
                        document.Create.NewUnionFitting(first, second)
                    else:
                        document.Create.NewElbowFitting(first, second)
                except Exception:
                    # Sem preferência de roteamento para a conexão, o Revit
                    # recusa a peça; a junta fica listada para o projetista.
                    unjoined.append("{}.{}".format(run["run_id"], index))
            previous = pipe
        created.append(run["run_id"])


if __name__ == "__main__":
    manifest_file = forms.pick_file(file_ext="json", title="Selecione o manifesto BIM do Triton")
    if manifest_file:
        default_mapping = Path(__file__).with_name("family_mapping.json")
        mapping_file = forms.pick_file(file_ext="json", title="Selecione o mapa de famílias", init_dir=str(default_mapping.parent))
        if mapping_file:
            inserted, unresolved, unjoined = import_manifest(revit.doc, manifest_file, mapping_file)
            forms.alert(
                "Importação concluída: {} inseridos; {} pendentes.\n\nPendentes: {}\nJuntas sem conexão: {}".format(
                    len(inserted), len(unresolved), ", ".join(unresolved) or "nenhum", ", ".join(unjoined) or "nenhuma"
                ),
                title="Triton → Revit",
            )
