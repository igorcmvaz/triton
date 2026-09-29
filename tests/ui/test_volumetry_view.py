"""Visualizador girável: desenha, enquadra, gira e seleciona sem OpenGL."""

import numpy as np
from PySide6.QtCore import QPointF

from netuno.core.volumetry import build_volumetry
from netuno.ui.volumetry_view import VolumetryPanel
from tests.unit.test_volumetry import _project


def _panel(qapp):
    panel = VolumetryPanel()
    panel.resize(1000, 600)
    panel.set_scene(build_volumetry(_project()))
    panel.show()
    qapp.processEvents()
    return panel


def test_view_renders_every_preset_and_fits_the_scene(qapp):
    panel = _panel(qapp)
    view = panel.view
    for name in ("persp", "top", "front", "side"):
        view.set_view(name)
        image = view.grab().toImage()
        assert not image.isNull()
        project, *_ = view._projector()
        pts = np.vstack([f.points for f in view._faces if view.scene.solids[f.solid].kind != "ground"])
        sx, sy, _ = project(pts)
        # Cena inteira dentro da área, ocupando boa parte dela.
        assert sx.min() >= -1 and sx.max() <= view.width() + 1 and sy.min() >= -1 and sy.max() <= view.height() + 1
        assert max((sx.max() - sx.min()) / view.width(), (sy.max() - sy.min()) / view.height()) > 0.6


def test_click_selects_component_and_whole_run(qapp):
    panel = _panel(qapp)
    view = panel.view
    view.set_view("top")
    view.grab()
    project, *_ = view._projector()
    rs = next(s for s in view.scene.solids if s.key == "RS-01")
    centre = np.mean([p for f in rs.faces for p in f], axis=0)
    sx, sy, _ = project(np.array([centre]))
    assert view.select_at(QPointF(float(sx[0]), float(sy[0]))).key == "RS-01"
    assert "Capacidade: 1.000 L" in panel.lbl_info.text()
    pipe = next(s for s in view.scene.solids if s.key == "T-02#1")
    a, b, _ = pipe.axis
    sx, sy, _ = project(np.array([[(a[i] + b[i]) / 2 for i in range(3)]]))
    view.grab()
    hit = view.select_at(QPointF(float(sx[0]), float(sy[0])))
    assert hit is not None and hit.group == "T-02"
    assert view._is_selected(next(s for s in view.scene.solids if s.key == "T-02#3"))
    assert view.select_at(QPointF(2, 2)) is None


def test_empty_scene_shows_placeholder(qapp):
    panel = VolumetryPanel()
    panel.set_scene(None)
    assert not panel.view.grab().toImage().isNull()


def test_keyboard_switches_views_and_clears_selection(qapp):
    from PySide6.QtCore import QEvent, Qt
    from PySide6.QtGui import QKeyEvent

    panel = _panel(qapp)
    view = panel.view
    view.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_2, Qt.NoModifier))
    assert view.ortho and view.pitch > 1.5
    view.selected = view.scene.solids[1]
    view.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Escape, Qt.NoModifier))
    assert view.selected is None
