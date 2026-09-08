"""
Testes para sincronização inteligente da ACV e cálculo de energia da motobomba.
"""

import pytest
from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult, SimulationDayResult
from netuno.core.pump_energy import compute_annual_pump_energy, nearest_pump_cv
from netuno.core.environmental_sync import (
    infer_tank_material,
    estimate_pipe_lengths_m,
    build_sync_snapshot,
    material_preset_values,
)
from netuno.core.environmental import EnvironmentalConfig, calculate_lca, MATERIAL_PRESETS


def test_infer_tank_material_from_cost():
    assert infer_tank_material(5000, 2500) == "PEAD"
    assert infer_tank_material(5000, 9000) == "CONCRETO"
    assert infer_tank_material(3000, 7000) == "ACO_INOX"


def test_material_preset_values_match_catalog():
    density, co2 = material_preset_values("PEAD")
    assert density == MATERIAL_PRESETS["PEAD"].material_density_kg_per_m3_tank
    assert co2 == MATERIAL_PRESETS["PEAD"].co2_factor_kg_per_kg


def test_compute_annual_pump_energy_from_simulation():
    config = NetunoConfig()
    config.pump_power_kw = 0.7355
    config.pump_efficiency = 60.0
    config.pump_flow_rate = 3000.0
    config.pump_startup_time_h = 10.0 / 3600.0
    config.upper_tank_used = 1

    daily = [
        SimulationDayResult(
            day_index=d + 1, precip_mm=10.0, eff_precip_mm=10.0, harvested_liters=1000.0,
            total_demand_liters=1000.0, pluvial_demand_liters=1000.0, pluvial_consumed_liters=1000.0,
            potable_consumed_liters=0.0, spilled_liters=0.0, lower_tank_end_liters=1000.0,
            upper_tank_end_liters=500.0, pumped_liters=1000.0, pump_cycles=2, satisfaction_type=2,
        )
        for d in range(365)
    ]
    sim = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=80.0,
        avg_pluvial_consumed_l_day=1000.0,
        avg_potable_consumed_l_day=0.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=100.0,
        pct_days_partial_satisfaction=0.0,
        pct_days_null_satisfaction=0.0,
        total_pumped_liters=365000.0,
        total_pump_cycles=730,
        daily_results=daily,
    )

    result = compute_annual_pump_energy(config, sim)
    assert result.annual_kwh > 0
    assert result.specific_kwh_per_m3 > 0
    assert result.annual_pumped_m3 == pytest.approx(365.0, rel=0.01)


def test_build_sync_snapshot_uses_simulation_pump_data():
    config = NetunoConfig()
    config.pump_power_kw = 0.7355
    config.pump_efficiency = 60.0
    config.pump_flow_rate = 3000.0
    config.cost_lower_tank = 2800.0
    config.analysis_period_years = 25
    config.lower_tank_material = "PEAD"
    config.upper_tank_material = "FIBRA"

    sim = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=80.0,
        avg_pluvial_consumed_l_day=500.0,
        avg_potable_consumed_l_day=100.0,
        avg_spilled_l_day=50.0,
        pct_days_full_satisfaction=80.0,
        pct_days_partial_satisfaction=10.0,
        pct_days_null_satisfaction=10.0,
        total_pumped_liters=120000.0,
        total_pump_cycles=300,
        n_days_simulated=365,
    )

    snap = build_sync_snapshot(
        config, sim,
        upper_used=True,
        upper_vol_l=500.0,
        lower_vol_l=5000.0,
        capture_area_m2=120.0,
    )

    assert snap["lower_material_key"] == "PEAD"
    assert snap["upper_material_key"] == "FIBRA"
    assert snap["lifespan_years"] == 25
    assert snap["annual_pump_kwh"] > 0
    assert snap["specific_kwh_per_m3"] > 0
    assert snap["pipes_m"][100] > 0


def test_sync_never_changes_explicit_material_because_of_cost():
    config = NetunoConfig()
    config.lower_tank_material = "PEAD"
    config.upper_tank_material = "FIBRA"
    # Valores altos que a heurística legada classificaria como concreto/inox.
    config.cost_lower_tank = 25000.0
    config.cost_upper_tank = 5000.0

    snap = build_sync_snapshot(
        config, None,
        upper_used=True,
        upper_vol_l=500.0,
        lower_vol_l=5000.0,
        capture_area_m2=100.0,
    )

    assert snap["lower_material_key"] == "PEAD"
    assert snap["upper_material_key"] == "FIBRA"


def test_lca_uses_annual_pump_kwh_when_provided():
    config = EnvironmentalConfig(
        lower_material_key="PEAD",
        upper_tank_used=False,
        annual_pump_kwh=150.0,
        pump_count=1,
        system_lifespan_years=20.0,
    )
    res = calculate_lca(5000.0, 100.0, config)
    assert res.annual_pumping_co2_kg == pytest.approx(150.0 * 0.085, rel=1e-3)


def test_nearest_pump_cv_lookup():
    assert nearest_pump_cv(0.48) == 0.50
    assert nearest_pump_cv(1.2) == 1.00


def test_config_pipe_lengths_and_sync():
    cfg = NetunoConfig()
    # Verifica que o padrão inicial possui 45m (20m recalque DN 32 + 5m sucção DN 40 + 20m captação DN 100)
    assert cfg.total_pipe_length() == 45.0

    cfg.set_pipe_length(50, 20.0)
    cfg.set_pipe_length(75, 10.0)
    cfg.set_pipe_length(100, 30.0)
    cfg.set_pipe_length(150, 5.0)

    assert cfg.get_pipe_length(50) == 20.0
    assert cfg.get_pipe_length(75) == 10.0
    assert cfg.get_pipe_length(100) == 30.0
    assert cfg.get_pipe_length(150) == 5.0
    assert cfg.total_pipe_length() == 90.0

    snap = build_sync_snapshot(
        cfg, None,
        upper_used=True,
        upper_vol_l=500.0,
        lower_vol_l=5000.0,
        capture_area_m2=100.0,
    )

    assert snap["pipes_m"][50] == 20.0
    assert snap["pipes_m"][75] == 10.0
    assert snap["pipes_m"][100] == 30.0
    assert snap["pipes_m"][150] == 5.0
