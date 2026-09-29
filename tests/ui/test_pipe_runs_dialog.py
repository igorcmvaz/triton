"""Diálogo em que o projetista organiza os trechos da planta 3D."""

from netuno.ui.dialogs.pipe_runs_dialog import PipeRunsDialog, format_origin, parse_origin


LAYOUT = {
    "bim_components": [
        {"instance_id": "CI-01", "type_id": "cisterna_inferior", "position_mm": {"x": 0, "y": 0, "z": -1500},
         "parameters": {"CAPACIDADE_L": 5000}},
        {"instance_id": "B-01", "type_id": "motobomba", "position_mm": {"x": 1500, "y": 0, "z": 0}},
    ],
    "pipe_runs": [
        {"run_id": "T-01", "system": "succao", "dn_mm": 32, "start": "CI-01", "route": "sobe 1500; +x 1500", "end": "B-01"},
        {"run_id": "T-02", "system": "recalque", "dn_mm": 25, "route": [{"direction": "+x", "length_mm": 3000}]},
    ],
}


def test_origin_text_distinguishes_continuation_coordinates_and_references():
    assert parse_origin("") is None
    assert parse_origin("100 0 -20,5") == {"x": 100.0, "y": 0.0, "z": -20.5}
    assert parse_origin("CI-01") == "CI-01"
    assert format_origin({"x": 100.0, "y": 0.0, "z": -20.5}) == "100 0 -20.5"


def test_dialog_keeps_parameters_and_revalidates_after_reordering(qapp):
    dialog = PipeRunsDialog(None, layout=LAYOUT, project_data={"project_name": "Teste"})
    assert dialog.refresh_preview() == []
    assert dialog.get_layout()["bim_components"][0]["parameters"] == {"CAPACIDADE_L": 5000}

    dialog.table_runs.setCurrentCell(1, 0)
    dialog.move_run(-1)
    runs = dialog.get_layout()["pipe_runs"]
    assert [run["run_id"] for run in runs] == ["T-02", "T-01"]
    assert runs[0]["route"] == "+x 3000"
    errors = dialog.refresh_preview()
    assert errors == ["Trecho T-02: o primeiro trecho precisa de origem (componente ou coordenadas)."]
