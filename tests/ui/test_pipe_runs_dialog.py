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
    assert dialog.preview.has_drawing()
    assert dialog.get_layout()["bim_components"][0]["parameters"] == {"CAPACIDADE_L": 5000}

    dialog.table_runs.setCurrentCell(1, 0)
    dialog.move_run(-1)
    runs = dialog.get_layout()["pipe_runs"]
    assert [run["run_id"] for run in runs] == ["T-02", "T-01"]
    assert runs[0]["route"] == "+x 3000"
    errors = dialog.refresh_preview()
    assert errors == ["Trecho T-02: o primeiro trecho precisa de origem (componente ou coordenadas)."]
    assert not dialog.preview.has_drawing()
    assert "não será exportada" in dialog.lbl_report.text()


def test_dialog_builds_volumetry_with_building_and_exports(qapp, tmp_path, monkeypatch):
    layout = dict(LAYOUT, building_volume={"origin_mm": {"x": -1000, "y": -3000, "z": 0},
                                           "width_mm": 8000, "depth_mm": 7000, "height_mm": 6000, "floors": 2})
    dialog = PipeRunsDialog(None, layout=layout, project_data={"project_name": "Teste", "lower_vol": 5000})
    assert dialog.get_layout()["building_volume"]["floors"] == 2
    keys = {s.key for s in dialog.volumetry.view.scene.solids}
    assert {"EDIFICACAO", "LAJE-1", "CI-01", "B-01", "T-01#1"} <= keys
    assert dialog.btn_glb.isEnabled() and dialog.btn_html.isEnabled()

    from PySide6.QtWidgets import QFileDialog
    for fmt in ("glb", "html"):
        target = tmp_path / f"vol.{fmt}"
        monkeypatch.setattr(QFileDialog, "getSaveFileName", staticmethod(lambda *a, t=target: (str(t), "")))
        assert dialog.export_volumetry(fmt) == str(target) and target.stat().st_size > 1000

    # Largura zerada = sem edificação; organização inválida desliga a volumetria.
    dialog.building_fields["width_mm"].setValue(0)
    assert dialog.get_layout()["building_volume"] == {}
    dialog.table_runs.setCurrentCell(1, 0)
    dialog.move_run(-1)
    dialog.refresh_preview()
    assert dialog.volumetry.view.scene is None and not dialog.btn_glb.isEnabled()


def test_organizacao_valida_abre_na_volumetria_com_o_editor_recolhido(qapp):
    """A volumetria é o que se quer ver; as tabelas aparecem só para editar."""
    dialog = PipeRunsDialog(None, layout=LAYOUT, project_data={"project_name": "Teste"})
    assert dialog.editor.isHidden() and not dialog.btn_editor.isChecked()
    dialog.btn_editor.setChecked(True)
    assert not dialog.editor.isHidden()

    # Tela cheia recolhe o editor e esconde os botões; ao sair, volta como estava.
    dialog.toggle_fullscreen()
    assert dialog.imersivo and dialog.editor.isHidden() and dialog._buttons.isHidden()
    dialog.toggle_fullscreen()
    assert not dialog.imersivo and not dialog.editor.isHidden() and not dialog._buttons.isHidden()
    dialog.close()


def test_organizacao_com_pendencias_abre_no_editor(qapp):
    runs = [dict(LAYOUT["pipe_runs"][1]), dict(LAYOUT["pipe_runs"][0])]  # o primeiro sem origem
    dialog = PipeRunsDialog(None, layout=dict(LAYOUT, pipe_runs=runs), project_data={"project_name": "Teste"})
    assert not dialog.editor.isHidden() and dialog.btn_editor.isChecked()


def test_dialog_prefills_from_study_when_layout_is_empty(qapp):
    project_data = {"project_name": "Casa Modelo Estudo", "lower_vol": 6000, "upper_vol": 1500, "floors": 2}
    dialog = PipeRunsDialog(None, layout=None, project_data=project_data)
    # Deve vir automaticamente pré-preenchido e válido
    assert dialog.refresh_preview() == []
    assert dialog.preview.has_drawing()
    assert dialog.volumetry.view.scene is not None
    # Arranjo normativo completo: 17 peças e 13 trechos (ver test_study_layout).
    assert len(dialog.get_layout()["bim_components"]) == 17
    assert len(dialog.get_layout()["pipe_runs"]) == 13

    # Testa o botão/método apply_study_layout
    dialog.table_runs.setRowCount(0)
    assert dialog.table_runs.rowCount() == 0
    dialog.apply_study_layout()
    assert dialog.table_runs.rowCount() == 13
    assert dialog.refresh_preview() == []

