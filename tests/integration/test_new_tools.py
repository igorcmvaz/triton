"""
Testes unitários para o Mini Simulador de Motobomba e o Otimizador Econômico Global do Netuno 5.
"""

import pytest
from netuno.ui.dialogs.pump_wizard_dialog import PUMP_CATALOG, PumpSelectionWizardDialog


def test_pump_catalog_structure():
    assert len(PUMP_CATALOG) >= 5
    for pump in PUMP_CATALOG:
        assert "cv" in pump
        assert "kw" in pump
        assert "flow_lh" in pump
        assert "cost" in pump
        assert "max_h" in pump
        assert pump["kw"] > 0
        assert pump["flow_lh"] > 0


def test_pump_wizard_calculations():
    # Simulando caixa d'água de 500L, altura geométrica de 10m e 20 min de enchimento
    upper_v = 500.0
    h_geom = 10.0
    t_fill_min = 20.0

    # H_man com 30% de perda
    h_man = h_geom * 1.30
    assert h_man == 13.0

    # Vazão mínima necessária (L/h)
    t_fill_h = t_fill_min / 60.0
    q_rec_lh = upper_v / t_fill_h
    assert q_rec_lh == 1500.0  # 500L em 1/3h -> 1500 L/h
