# -*- coding: utf-8 -*-
"""O exemplo publicado no artigo do SoftwareX: quatro critérios, quatro volumes.

O projeto `examples/exemplo_quatro_criterios.netuno` é o caso ilustrativo do
artigo. Os números da Tabela 1 e das figuras saem dele; se o programa mudar de
modo a alterá-los, este teste falha antes que o artigo passe a descrever um
resultado que a versão distribuída não reproduz.
"""
from pathlib import Path

import pytest

from netuno import cli

EXEMPLO = Path(__file__).resolve().parents[2] / "examples" / "exemplo_quatro_criterios.netuno"


@pytest.fixture(scope="module")
def saida():
    b = cli._load_bundle(str(EXEMPLO))
    an = b.get("analysis") or {}
    return cli.run_analysis(b["config"], cli._get_precipitation(b), "all",
                            environmental=an.get("environmental"))


def test_fracoes_do_exemplo():
    c = cli._load_bundle(str(EXEMPLO))["config"]
    assert c.non_potable_indoor_share == pytest.approx(0.35)
    assert c.irrigation_liters_per_day == pytest.approx(90.0)
    assert c.rainwater_share == pytest.approx(200.0 / 460.0, abs=1e-6)   # (0,35·600 + 90) / 690


def test_quatro_otimos_distintos(saida):
    t = saida["topsis"]
    otimos = (t["technical_best_volume_l"], t["economic_best_volume_l"],
              t["environmental_best_volume_l"], t["best_volume_l"])
    assert otimos == (6000.0, 5000.0, 3000.0, 7000.0)
    assert len(set(otimos)) == 4
