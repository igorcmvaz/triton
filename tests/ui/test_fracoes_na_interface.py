# -*- coding: utf-8 -*-
"""A interface simula com as frações do projeto, e as grava de volta.

Até a 5.0.0 a tela de edificação não restaurava a fração interna nem a demanda
externa ao abrir um projeto: voltava aos padrões (35% e 0 L/dia) e simulava com
eles, e a gravação escrevia esses padrões no arquivo. O caso do tutorial, que
declara 28%, saía com 32,85% de economia a 4.000 L na interface e 27,12% no
manual e na linha de comando.
"""
import sys
from pathlib import Path

import pytest
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from netuno.core.parser import load_netuno_project

RAIZ = Path(__file__).resolve().parents[2]
CASO = RAIZ / "manual" / "casos" / "02_tutorial_varredura.netuno"


@pytest.fixture(scope="module")
def janela(monkeypatch_module):
    app = QApplication.instance() or QApplication(sys.argv)
    from netuno.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(CASO))
    yield w
    w.close()
    app.processEvents()


@pytest.fixture(scope="module")
def monkeypatch_module():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ("information", "warning", "critical"):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, "question", staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    yield mp
    mp.undo()


def test_tela_mostra_as_fracoes_do_arquivo(janela):
    tb = janela.tab_building
    assert tb.txt_non_potable_indoor_share_simple.text() == "28"
    assert tb.txt_external_demand_l_day.text() == "0"
    assert tb.txt_share.text() == "28"
    assert tb.txt_share.isReadOnly()


def test_interface_e_linha_de_comando_dao_o_mesmo_potencial(janela):
    sim = janela.tab_tanks_simulation
    sim.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
    sim.run_simulation(force=True)
    r = sim.last_sweep_result.results_by_volume
    pares = r.items() if isinstance(r, dict) else [(x.lower_tank_vol, x) for x in r]
    por_volume = {int(v): x.potential_potable_savings_pct for v, x in pares}
    assert por_volume[4000] == pytest.approx(27.12, abs=0.005)   # o valor impresso no manual


def test_gravar_e_reabrir_preserva_as_fracoes(janela, tmp_path, monkeypatch_module):
    tb = janela.tab_building
    tb.txt_non_potable_indoor_share_simple.setText("30")
    tb.txt_external_demand_l_day.setText("150")
    destino = tmp_path / "salvo.netuno"
    monkeypatch_module.setattr(QFileDialog, "getSaveFileName",
                               staticmethod(lambda *a, **k: (str(destino), "")))
    janela.on_save_simulation()
    c = load_netuno_project(str(destino))
    cfg = c["config"]
    assert c["aviso_fracoes"] is None
    assert cfg.non_potable_indoor_share == pytest.approx(0.30)
    assert cfg.irrigation_liters_per_day == pytest.approx(150.0)
    assert cfg.rainwater_share == pytest.approx((0.30 * 600 + 150) / 750, abs=1e-4)
