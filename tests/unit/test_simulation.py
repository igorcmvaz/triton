import os
import pytest
import numpy as np

from netuno.core.simulation import (
    build_sweep_volume_grid,
    run_single_simulation,
    run_sweep_simulation,
)
from netuno.core.parser import load_precipitation

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def fpolis_precip():
    path = os.path.join(WORKSPACE_DIR, "Additional_Material", "Precipitation_Samples", "precFpolis_2002_2011.csv")
    if not os.path.exists(path):
        path = os.path.join(WORKSPACE_DIR, "data", "rainfall", "Florianopolis1.csv")
    return load_precipitation(path)

def test_zero_rain_simulation():
    """Verify that zero rain results in 0% potential savings and 100% null satisfaction."""
    zero_precip = np.zeros(365, dtype=np.float64)
    res = run_single_simulation(
        precip_data=zero_precip,
        lower_tank_vol=2000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=1.0,
        total_demand_per_day=300.0,
        rainwater_share=0.4
    )
    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.pct_days_null_satisfaction == 100.0
    assert res.pct_days_full_satisfaction == 0.0

def test_extreme_rain_simulation():
    """Verify that constant high rain fills tank, maximizes potential savings, and generates spillover."""
    heavy_precip = np.full(365, 100.0, dtype=np.float64) # 100 mm rain every day
    res = run_single_simulation(
        precip_data=heavy_precip,
        lower_tank_vol=2000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=1.0,
        total_demand_per_day=300.0,
        rainwater_share=0.4 # 120 L/day target
    )
    assert abs(res.avg_pluvial_consumed_l_day - 120.0) < 0.1
    assert abs(res.potential_potable_savings_pct - 40.0) < 0.1
    assert res.pct_days_full_satisfaction == 100.0
    assert res.avg_spilled_l_day > 8000.0

def test_dual_tank_pumping(fpolis_precip):
    """Verify dual tank pumping threshold logic."""
    res = run_single_simulation(
        precip_data=fpolis_precip,
        lower_tank_vol=2000.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=1.0,
        total_demand_per_day=300.0,
        rainwater_share=0.4,
        upper_tank_vol=500.0,
        upper_tank_used=True,
        pumping_threshold=375.0
    )
    assert res.total_pumped_liters > 0.0
    assert res.total_pump_cycles > 0
    assert res.potential_potable_savings_pct > 30.0


def test_higher_pump_threshold_increases_starts_and_reduces_batch_size():
    """Higher triggers start earlier; they do not prescribe total annual transfer."""
    regular_rain = np.full(30, 10.0, dtype=np.float64)
    common = dict(
        precip_data=regular_rain,
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.8,
        discard_mm=0.0,
        total_demand_per_day=1000.0,
        rainwater_share=0.4,
        upper_tank_vol=500.0,
        upper_tank_used=True,
    )
    responsive = run_single_simulation(**common, pumping_threshold=50.0)
    conservative = run_single_simulation(**common, pumping_threshold=250.0)

    assert conservative.total_pump_cycles > responsive.total_pump_cycles
    assert conservative.average_pumped_liters_per_cycle < responsive.average_pumped_liters_per_cycle
    # Transfer total follows consumption plus the final upper-tank inventory.
    # It can change slightly, but is not expected to vary proportionally to the trigger.
    assert abs(conservative.total_pumped_liters - responsive.total_pumped_liters) <= 500.0


@pytest.mark.parametrize("threshold", [0.0, 50.0, 250.0, 500.0, 900.0])
def test_pump_threshold_is_bounded_and_internal_transfer_is_mass_conservative(threshold):
    result = run_single_simulation(
        precip_data=np.full(30, 10.0, dtype=np.float64),
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.8,
        discard_mm=0.0,
        total_demand_per_day=1000.0,
        rainwater_share=0.4,
        upper_tank_vol=500.0,
        upper_tank_used=True,
        pumping_threshold=threshold,
        store_daily_details=True,
    )

    final_upper = result.daily_results[-1].upper_tank_end_liters
    total_consumed_from_upper = sum(day.pluvial_consumed_liters for day in result.daily_results)
    assert 0.0 <= final_upper <= 500.0
    assert result.total_pumped_liters == pytest.approx(total_consumed_from_upper + final_upper)
    # Uma partida nunca transfere mais que a capacidade da caixa superior.
    assert result.max_pump_batch_liters <= 500.0
    # Um dia pode conter mais de uma partida; por isso o total diário é
    # limitado por número de partidas × capacidade, não por uma única caixa.
    assert all(day.pumped_liters <= day.pump_cycles * 500.0 for day in result.daily_results)


@pytest.mark.parametrize("upper_volume", [320.0, 500.0, 1000.0])
def test_pump_batch_is_limited_by_each_configured_upper_tank_volume(upper_volume):
    result = run_single_simulation(
        precip_data=np.full(30, 10.0, dtype=np.float64),
        lower_tank_vol=5000.0,
        area=100.0,
        runoff_coeff=0.8,
        discard_mm=0.0,
        total_demand_per_day=1000.0,
        rainwater_share=0.4,
        upper_tank_vol=upper_volume,
        upper_tank_used=True,
        pumping_threshold=upper_volume * 0.50,
        store_daily_details=True,
    )

    assert result.total_pump_cycles > 0
    assert result.max_pump_batch_liters <= upper_volume
    assert all(day.upper_tank_end_liters <= upper_volume for day in result.daily_results)
    assert all(day.pumped_liters <= day.pump_cycles * upper_volume for day in result.daily_results)

def test_sweep_optimal_volume_determination(fpolis_precip):
    """Verify lower tank range sweep and optimal volume determination algorithm."""
    sweep = run_sweep_simulation(
        precip_data=fpolis_precip,
        lower_tank_max=10000.0,
        lower_tank_step=250.0,
        area=100.0,
        runoff_coeff=0.9,
        discard_mm=1.0,
        total_demand_per_day=300.0,
        rainwater_share=0.4,
        delta_ideal_threshold=1.0
    )
    assert sweep.optimal_lower_tank_vol is not None
    assert sweep.optimal_lower_tank_vol in [2250.0, 2500.0, 2750.0, 3000.0, 3250.0, 3500.0, 3750.0, 4000.0, 4500.0]
    assert sweep.optimal_potential_pct > 35.0
    assert len(sweep.results_by_volume) == 41 # (10000 / 250) + 1
    assert sweep.effective_step_l == 250.0
    assert sweep.step_adjusted is False


def test_sweep_grid_allows_40_positive_volumes_plus_zero_reference():
    grid = build_sweep_volume_grid(10000.0, 250.0)

    assert grid.positive_volume_count == 40
    assert len(grid.volumes_l) == 41
    assert grid.volumes_l[0] == 0.0
    assert grid.volumes_l[-1] == 10000.0
    assert grid.effective_step_l == 250.0
    assert grid.step_adjusted is False


def test_sweep_grid_doubles_step_above_40_and_keeps_exact_maximum():
    grid = build_sweep_volume_grid(10001.0, 250.0)

    assert grid.effective_step_l == 500.0
    assert grid.step_adjusted is True
    assert grid.positive_volume_count == 21
    assert grid.volumes_l[-2] == 10000.0
    assert grid.volumes_l[-1] == 10001.0
    assert grid.volumes_l[-1] - grid.volumes_l[-2] == 1.0


def test_sweep_grid_rounds_step_up_to_250_l_multiple_before_doubling():
    grid = build_sweep_volume_grid(25000.0, 300.0)

    assert grid.effective_step_l == 1000.0
    assert grid.effective_step_l % 250.0 == 0.0
    assert grid.positive_volume_count == 25
    assert grid.volumes_l[-1] == 25000.0


def test_monthly_potable_use_tracks_each_days_variable_demand():
    result = run_single_simulation(
        precip_data=np.zeros(32, dtype=np.float64),
        lower_tank_vol=1000.0,
        total_demand_per_day=999.0,  # deve ser ignorada quando há série mensal completa
        rainwater_share=0.4,
        monthly_demands=[100.0, 200.0] + [100.0] * 10,
        monthly_residents=[1] * 12,
        start_date_str="01/01/2024",
        store_daily_details=True,
    )
    assert result.daily_results[0].potable_consumed_liters == pytest.approx(100.0)
    assert result.daily_results[30].potable_consumed_liters == pytest.approx(100.0)
    assert result.daily_results[31].potable_consumed_liters == pytest.approx(200.0)


def test_suggested_sweep_residential_sizing(qapp):
    """Garante que para residência simples o volume máximo é >= 8.000L e o passo sugerido é 500L."""
    from netuno.ui.tab_tanks_simulation import TabTanksSimulation

    tab = TabTanksSimulation()
    # Edificação residencial padrão: 4 pessoas, 200 L/dia, 40% não potável (320 L/dia), telhado 100m²
    building = {
        "area": 100.0,
        "demand": 200.0,
        "residents": 4.0,
        "runoff": 0.8,
        "share": 0.4,
    }
    res = tab._calculate_suggested_sweep(building, sdii_mm_day=10.0)

    # Volume máximo deve ser de pelo menos o dobro de 3.750L (ou seja, >= 7.500L / 8.000L)
    assert res["sweep_max_l"] >= 8000.0
    # Passo adaptativo deve ser de 500L para essa faixa
    assert res["sweep_step_l"] == 500.0
    # Quantidade de simulações positiva deve ser moderada (entre 15 e 40)
    assert 15 <= res["positive_volume_count"] <= 40

