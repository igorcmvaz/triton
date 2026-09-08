"""Importador Netuno 5 para execução dentro do pyRevit.

Este script deve ser iniciado pelo Revit/pyRevit, pois somente esse processo
disponibiliza ``Autodesk.Revit.DB`` e um documento RVT ativo.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from Autodesk.Revit.DB import (  # type: ignore
    FamilySymbol,
    FilteredElementCollector,
    Level,
    StorageType,
    Transaction,
    UnitTypeId,
    UnitUtils,
    XYZ,
)
from Autodesk.Revit.DB.Structure import StructuralType  # type: ignore
from pyrevit import forms, revit  # type: ignore


def _symbols(document):
    return list(FilteredElementCollector(document).OfClass(FamilySymbol))


def _levels(document):
    return {level.Name: level for level in FilteredElementCollector(document).OfClass(Level)}


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
    if manifest.get("schema_version") != "1.0":
        raise ValueError("Versão do manifesto Netuno não suportada.")
    mapping = json.loads(Path(mapping_path).read_text(encoding="utf-8-sig"))
    symbols = _symbols(document)
    levels = _levels(document)
    missing, created = [], []

    transaction = Transaction(document, "Importar componentes Netuno")
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
            pos = item["position_mm"]
            point = XYZ(
                UnitUtils.ConvertToInternalUnits(float(pos["x"]), UnitTypeId.Millimeters),
                UnitUtils.ConvertToInternalUnits(float(pos["y"]), UnitTypeId.Millimeters),
                UnitUtils.ConvertToInternalUnits(float(pos["z"]), UnitTypeId.Millimeters),
            )
            element = document.Create.NewFamilyInstance(point, symbol, level, StructuralType.NonStructural)
            rotation = math.radians(float(item.get("rotation_deg", 0.0)))
            if abs(rotation) > 1e-9:
                from Autodesk.Revit.DB import ElementTransformUtils, Line  # type: ignore
                axis = Line.CreateBound(point, point + XYZ.BasisZ)
                ElementTransformUtils.RotateElement(document, element.Id, axis, rotation)
            _set_parameter(element, "NETUNO_ID", item["instance_id"])
            for name, value in item.get("parameters", {}).items():
                _set_parameter(element, name, value)
            created.append(item["instance_id"])
        transaction.Commit()
    except Exception:
        if transaction.HasStarted():
            transaction.RollBack()
        raise
    finally:
        transaction.Dispose()
    return created, missing


if __name__ == "__main__":
    manifest_file = forms.pick_file(file_ext="json", title="Selecione o manifesto BIM do Netuno")
    if manifest_file:
        default_mapping = Path(__file__).with_name("family_mapping.json")
        mapping_file = forms.pick_file(file_ext="json", title="Selecione o mapa de famílias", init_dir=str(default_mapping.parent))
        if mapping_file:
            inserted, unresolved = import_manifest(revit.doc, manifest_file, mapping_file)
            forms.alert(
                "Importação concluída: {} inseridos; {} pendentes.\n\nPendentes: {}".format(
                    len(inserted), len(unresolved), ", ".join(unresolved) or "nenhum"
                ),
                title="Netuno 5 → Revit",
            )
