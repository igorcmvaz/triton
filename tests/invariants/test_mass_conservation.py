"""
Teste de Invariante Física: Conservação de Massa Hídrica.
Garante que a quantidade de água que entra no sistema seja exatamente igual
à soma da variação de estoque nos reservatórios, consumo, descarte e extravasamento.
"""

import pytest
import numpy as np
from netuno.core.simulation import run_single_simulation


def test_water_mass_balance_conservation_invariant():
    """
    Invariante Fundamental:
    Chuva_Total_Capitada = (Estoque_Final - Estoque_Inicial) + Consumo_Pluvial_Total + Extravasamento_Total + Descarte_Total
    """
    # Série de chuva sintética com eventos variados (100 dias)
    np.random.seed(123)
    precip_data = np.random.exponential(scale=15.0, size=100)
    precip_data[precip_data < 2.0] = 0.0  # insere dias secos

    area = 150.0
    runoff = 0.85
    discard_mm = 2.0
    lower_vol = 5000.0
    tot_demand = 400.0
    share = 0.5

    res = run_single_simulation(
        precip_data=precip_data,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        discard_mm=discard_mm,
        discard_mode=1,
        total_demand_per_day=tot_demand,
        rainwater_share=share,
        upper_tank_vol=1000.0,
        upper_tank_used=True,
        pumping_threshold=200.0,
        store_daily_details=True
    )

    # Reconstitui a conservação diária a partir dos detalhes. O recalque é
    # transferência interna e por isso desaparece do balanço combinado.
    previous_lower = 0.0
    previous_upper = 0.0
    for day_res in res.daily_results:
        # Não-negatividade dos volumes
        assert day_res.lower_tank_end_liters >= 0.0
        assert day_res.upper_tank_end_liters >= 0.0
        assert day_res.pluvial_consumed_liters >= 0.0
        assert day_res.spilled_liters >= 0.0

        # Os volumes armazenados nunca devem exceder a capacidade máxima
        assert day_res.lower_tank_end_liters <= lower_vol + 1e-5
        assert day_res.upper_tank_end_liters <= 1000.0 + 1e-5

        inputs = previous_lower + previous_upper + day_res.harvested_liters
        outputs = (
            day_res.lower_tank_end_liters
            + day_res.upper_tank_end_liters
            + day_res.pluvial_consumed_liters
            + day_res.spilled_liters
        )
        assert inputs == pytest.approx(outputs, abs=1e-7)
        previous_lower = day_res.lower_tank_end_liters
        previous_upper = day_res.upper_tank_end_liters


def test_zero_rainfall_zero_pluvial_consumption_invariant():
    """Série sem nenhuma chuva deve resultar em consumo pluvial nulo e atendimento 0%."""
    precip_data = [0.0] * 365
    res = run_single_simulation(
        precip_data=precip_data,
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=1.0,
        total_demand_per_day=300.0,
        rainwater_share=0.4
    )

    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.total_overflow_liters == 0.0
