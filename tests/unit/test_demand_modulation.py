import pytest
import numpy as np
from netuno.core.simulation import build_daily_demand_vectors, run_single_simulation, run_sweep_simulation


def test_build_daily_demand_vectors_constant():
    tot, pluv = build_daily_demand_vectors(
        n_days=10,
        demand_mode="constant",
        demand_value=150.0,
        residents_count=3.0,
        rainwater_share=0.4
    )
    assert len(tot) == 10
    assert len(pluv) == 10
    assert np.allclose(tot, 450.0)
    assert np.allclose(pluv, 180.0)


def test_build_daily_demand_vectors_weekly():
    weekly_d = [100, 100, 100, 100, 100, 200, 200]
    weekly_r = [2, 2, 2, 2, 2, 4, 4]
    weekly_s = [0.5] * 7
    tot, pluv = build_daily_demand_vectors(
        n_days=7,
        start_date_str="03/01/2000",  # Monday
        demand_mode="weekly",
        weekly_demands=weekly_d,
        weekly_residents=weekly_r,
        weekly_shares=weekly_s
    )
    assert len(tot) == 7
    assert tot[0] == 200.0  # Monday: 100*2
    assert pluv[0] == 100.0
    assert tot[5] == 800.0  # Saturday: 200*4
    assert pluv[5] == 400.0


def test_build_daily_demand_vectors_monthly():
    monthly_d = [100 + i*10 for i in range(12)]
    monthly_r = [4] * 12
    monthly_s = [0.3] * 12
    tot, pluv = build_daily_demand_vectors(
        n_days=60,
        start_date_str="01/01/2000",
        demand_mode="monthly",
        monthly_demands=monthly_d,
        monthly_residents=monthly_r,
        monthly_shares=monthly_s
    )
    assert len(tot) == 60
    assert tot[0] == 100.0 * 4  # Jan
    assert tot[31] == 110.0 * 4  # Feb


def test_build_daily_demand_vectors_daily():
    daily_d = [100.0, 150.0, 200.0]
    daily_r = [2.0, 3.0, 4.0]
    daily_s = [0.4, 0.5, 0.6]
    tot, pluv = build_daily_demand_vectors(
        n_days=3,
        demand_mode="daily",
        daily_demands=daily_d,
        daily_residents=daily_r,
        daily_shares=daily_s
    )
    assert len(tot) == 3
    assert np.isclose(tot[0], 200.0)
    assert np.isclose(pluv[0], 80.0)
    assert np.isclose(tot[1], 450.0)
    assert np.isclose(pluv[1], 225.0)
    assert np.isclose(tot[2], 800.0)
    assert np.isclose(pluv[2], 480.0)


def test_simulation_with_modulated_demand():
    precip = np.array([0.0, 10.0, 25.0, 0.0, 5.0, 15.0, 0.0])
    b_cfg = {
        "area": 100.0,
        "demand": 200.0,
        "residents": 4,
        "runoff": 0.8,
        "share": 0.4,
        "demand_mode": "weekly",
        "weekly_demands": [150, 150, 150, 150, 150, 250, 250],
        "weekly_residents": [4, 4, 4, 4, 4, 4, 4],
        "weekly_shares": [0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5]
    }
    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=5000.0,
        building_config=b_cfg
    )
    assert res.n_days_simulated == 7
    assert res.potential_potable_savings_pct >= 0.0
