"""
Teste automatizado para as 3 Abordagens de Descarte Inicial (First Flush) no Netuno 5.
"""

import numpy as np
import pytest

from netuno.core.simulation import run_single_simulation


def test_discard_mode_1_all_events():
    # 3 dias de chuva: 1mm (descartada <= 2mm), 5mm (aproveitada), 10mm (aproveitada).
    precip = np.array([1.0, 5.0, 10.0])
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=10000.0,
        area=100.0,
        runoff_coeff=1.0,
        discard_mm=2.0,
        discard_mode=1,  # Modo 1: Todos os eventos
        total_demand_per_day=0.0,
        rainwater_share=0.0,
        store_daily_details=True
    )
    
    # Dia 0: 1.0 mm <= 2.0 mm -> p_eff = 0.0 mm -> 0L
    # Dia 1: 5.0 mm - 2.0 mm = 3.0 mm -> Aproveitado 300L
    # Dia 2: 10.0 mm - 2.0 mm = 8.0 mm -> Aproveitado 800L (Total acumulado: 1100L)
    assert res.daily_results[0].lower_tank_end_liters == pytest.approx(0.0)
    assert res.daily_results[1].lower_tank_end_liters == pytest.approx(300.0)
    assert res.daily_results[2].lower_tank_end_liters == pytest.approx(1100.0)


def test_discard_mode_2_after_dry_spell():
    # 3 dias de chuva: 1mm (descartada no 1º dia), 1mm (aproveitada pois dia anterior já choveu), 5mm.
    precip = np.array([1.0, 1.0, 5.0])
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=10000.0,
        area=100.0,
        runoff_coeff=1.0,
        discard_mm=2.0,
        discard_mode=2,  # Modo 2: Apenas 1º evento após estiagem
        total_demand_per_day=0.0,
        rainwater_share=0.0,
        store_daily_details=True
    )
    
    # Dia 0 (após dia seco 0mm): 1.0 mm <= 2.0 mm -> Descartado 0L
    # Dia 1 (já choveu ontem): 1.0 mm aproveitado sem descarte -> 100L
    # Dia 2 (já choveu ontem): 5.0 mm aproveitado sem descarte -> 500L
    # Total acumulado = 0 + 100 + 500 = 600 L
    assert res.daily_results[0].lower_tank_end_liters == pytest.approx(0.0)
    assert res.daily_results[1].lower_tank_end_liters == pytest.approx(100.0)
    assert res.daily_results[2].lower_tank_end_liters == pytest.approx(600.0)


def test_discard_mode_3_every_x_days():
    # 5 dias de chuva: 1mm cada dia. Descarte = 2mm a cada 3 dias (X = 3).
    precip = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=10000.0,
        area=100.0,
        runoff_coeff=1.0,
        discard_mm=2.0,
        discard_mode=3,  # Modo 3: A cada X dias
        discard_days_interval=3,
        total_demand_per_day=0.0,
        rainwater_share=0.0,
        store_daily_details=True
    )
    
    # Dia 0 (descarte aplicado): 1.0 <= 2.0 mm -> Descartado 0L
    # Dia 1 (1 dia decorrido < 3): 1.0 mm aproveitado sem descarte -> 100L
    # Dia 2 (2 dias decorridos < 3): 1.0 mm aproveitado sem descarte -> 100L
    # Dia 3 (3 dias decorridos >= 3, descarte aplicado): 1.0 <= 2.0 mm -> Descartado 0L
    # Dia 4 (1 dia decorrido < 3): 1.0 mm aproveitado sem descarte -> 100L
    assert res.daily_results[0].lower_tank_end_liters == pytest.approx(0.0)
    assert res.daily_results[1].lower_tank_end_liters == pytest.approx(100.0)
    assert res.daily_results[2].lower_tank_end_liters == pytest.approx(200.0)
    assert res.daily_results[3].lower_tank_end_liters == pytest.approx(200.0)
    assert res.daily_results[4].lower_tank_end_liters == pytest.approx(300.0)

