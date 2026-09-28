# -*- coding: utf-8 -*-
"""Interface e linha de comando dão o mesmo resultado para o mesmo projeto.

Cada projeto distribuído é aberto na janela principal (sem exibi-la) e rodado
pela linha de comando; os dois caminhos têm de concordar volume a volume no
potencial, no VPL, no payback descontado e no carbono do ciclo de vida, e nos
cinco ótimos: técnico, econômico, ambiental, TOPSIS e SMAA-VIKOR.

Os projetos cobrem os modos que o programa oferece: demanda constante,
semanal e mensal, com e sem demanda externa, com e sem reservatório superior.
Duas variantes montadas aqui cobrem o que nenhum arquivo distribuído tem:
demanda diária e uma alteração feita na tela e gravada.

Estes testes existem porque as duas pontas divergiram cinco vezes na 5.0.0:
a fração interna ignorada na tela, o preço da cisterna fixo na varredura da
linha de comando, o dispositivo de descarte e a potência da motobomba fora da
ACV da linha de comando, o SMAA-VIKOR com 5.000 sorteios contra 20.000, e o
payback «zero» da alternativa sem cisterna.
"""
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("PySide6")
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox  # noqa: E402

from netuno import cli  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PROJETOS = (sorted((RAIZ / "manual" / "casos").glob("*.netuno"))
            + sorted((RAIZ / "examples").glob("estudo_caso_*.netuno"))
            + [RAIZ / "examples" / "exemplo_quatro_criterios.netuno"])


@pytest.fixture(scope="module", autouse=True)
def _sem_dialogos():
    mp = pytest.MonkeyPatch()
    ok = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok)
    for nome in ("information", "warning", "critical"):
        mp.setattr(QMessageBox, nome, ok)
    mp.setattr(QMessageBox, "question", staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes))
    QApplication.instance() or QApplication(sys.argv)
    yield mp
    mp.undo()


def _abrir(caminho):
    from netuno.ui.main_window import MainWindow
    w = MainWindow()
    w.on_load_simulation(str(caminho))
    return w


def _rodar_janela(w):
    sim = w.tab_tanks_simulation
    sim.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
    sim.run_simulation(force=True)
    w.tab_economic.calculate_economics(force=True)
    w.tab_environmental.recalculate_and_update()
    g = w.tab_global_optimizer
    g.recalculate_all()
    t, smaa = g.last_topsis_result, g.last_smaa_vikor_result
    linhas = {round(x["vol"]): x for x in g.last_scenario_results}
    varredura = sim.last_sweep_result.results_by_volume
    pares = varredura.items() if isinstance(varredura, dict) else [(r.lower_tank_vol, r) for r in varredura]
    return {
        "unico": sim.last_single_result.potential_potable_savings_pct,
        "potencial": {round(v): r.potential_potable_savings_pct for v, r in pares},
        "vpl": {v: x["vpl"] for v, x in linhas.items()},
        "carbono": {v: x["lifecycle_co2"] for v, x in linhas.items()},
        "otimos": (t.candidates[t.technical_best_index].lower_tank_vol,
                   t.candidates[t.financial_best_index].lower_tank_vol,
                   t.candidates[t.environmental_best_index].lower_tank_vol,
                   t.best_candidate.lower_tank_vol,
                   smaa.best_candidate.lower_tank_vol),
        "topsis": float(t.scores[t.best_index]),
    }


def _rodar_cli(caminho, varredura=True):
    """Com ``varredura``, um projeto de volume fixo é varrido como a interface faz
    ao lado do volume fixo; sem ela, só o volume declarado é avaliado."""
    b = cli._load_bundle(str(caminho))
    if varredura:
        b["config"].lower_tank_mode = 1
    an = b.get("analysis") or {}
    o = cli.run_analysis(b["config"], cli._get_precipitation(b), "all",
                         environmental=an.get("environmental"))
    t = o["topsis"]
    return {
        "potencial": {round(a["lower_tank_volume_l"]): a["potable_savings_pct"] for a in o["technical"]["alternatives"]},
        "vpl": {round(a["lower_tank_volume_l"]): a["npv_brl"] for a in o["economic"]["alternatives"]},
        "carbono": {round(a["lower_tank_volume_l"]): -a["lifetime_net_co2_saved_kg"] for a in o["environmental"]["alternatives"]},
        "otimos": (t["technical_best_volume_l"], t["economic_best_volume_l"],
                   t["environmental_best_volume_l"], t["best_volume_l"],
                   o["smaa_vikor"]["best_volume_l"]),
        "topsis": t["best_score"],
    }


def _comparar(j, c, nome):
    comuns = sorted(set(j["potencial"]) & set(c["potencial"]))
    assert len(comuns) >= 3, f"{nome}: varreduras sem volumes em comum"
    for v in comuns:
        assert j["potencial"][v] == pytest.approx(c["potencial"][v], abs=0.01), f"{nome} {v} L: potencial"
        if v > 0 and v in j["vpl"] and v in c["vpl"]:
            assert j["vpl"][v] == pytest.approx(c["vpl"][v], rel=1e-3, abs=1.0), f"{nome} {v} L: VPL"
            assert j["carbono"][v] == pytest.approx(c["carbono"][v], rel=1e-3, abs=0.5), f"{nome} {v} L: carbono"
    rotulos = ("técnico", "econômico", "ambiental", "TOPSIS", "SMAA-VIKOR")
    for r, a, b in zip(rotulos, j["otimos"], c["otimos"]):
        assert a == b, f"{nome}: ótimo {r} {a} L na interface e {b} L na linha de comando"
    assert j["topsis"] == pytest.approx(c["topsis"], abs=1e-3), f"{nome}: escore TOPSIS"


@pytest.mark.parametrize("caminho", PROJETOS, ids=lambda p: p.stem)
def test_projeto_distribuido(caminho):
    w = _abrir(caminho)
    try:
        janela = _rodar_janela(w)
    finally:
        w.close()
    _comparar(janela, _rodar_cli(caminho), caminho.stem)
    if w.config.lower_tank_mode == 0:
        # o volume fixo declarado, avaliado sozinho pela linha de comando
        so_ele = _rodar_cli(caminho, varredura=False)["potencial"]
        assert len(so_ele) == 1
        assert janela["unico"] == pytest.approx(next(iter(so_ele.values())), abs=0.01),             f"{caminho.stem}: potencial do volume fixo"


def test_alteracao_feita_na_tela_e_gravada(tmp_path, _sem_dialogos):
    """Fração interna e demanda externa digitadas na tela chegam iguais à linha de comando."""
    w = _abrir(RAIZ / "manual" / "casos" / "02_tutorial_varredura.netuno")
    try:
        tb = w.tab_building
        tb.txt_non_potable_indoor_share_simple.setText("30")
        tb.txt_external_demand_l_day.setText("120")
        destino = tmp_path / "alterado.netuno"
        _sem_dialogos.setattr(QFileDialog, "getSaveFileName",
                              staticmethod(lambda *a, **k: (str(destino), "")))
        w.on_save_simulation()
        janela = _rodar_janela(w)
    finally:
        w.close()
    _comparar(janela, _rodar_cli(destino), "alterado na tela")


def test_modo_diario(tmp_path):
    """Demanda diária: a série do arquivo manda nos dois caminhos."""
    d = json.loads((RAIZ / "manual" / "casos" / "02_tutorial_varredura.netuno").read_text(encoding="utf-8"))
    n = len(d["rainfall"]["precipitation_mm"]) if "precipitation_mm" in d.get("rainfall", {}) else 3650
    mod = d["inputs"].setdefault("demand_modulation", {})
    mod.update(demand_mode="daily",
               daily_demands=[150.0 if i % 7 < 5 else 190.0 for i in range(n)],
               daily_residents=[4] * n,
               daily_shares=[0.28] * n)
    d["inputs"]["incentives_and_shares"]["demand_mode"] = "daily"
    p = tmp_path / "diario.netuno"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    w = _abrir(p)
    try:
        _comparar(_rodar_janela(w), _rodar_cli(p), "modo diário")
    finally:
        w.close()
