import os
import pytest
import numpy as np
from datetime import datetime

from netuno.core.parser import parse_float, parse_int, load_precipitation, parse_netuno_csv

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_project_filename_contains_name_date_and_stable_hash():
    from netuno import get_project_filename

    stamp = datetime(2026, 9, 1, 18, 30, 45)
    filename = get_project_filename("Edifício Águas do Sul", "N5-20260901-ABCDEF12", now=stamp)
    assert filename.startswith("netuno-projeto-edificio-aguas-do-sul-2026-09-01-183045-")
    assert filename.endswith(".netuno")
    assert filename == get_project_filename("Edifício Águas do Sul", "N5-20260901-ABCDEF12", now=stamp)


def test_parse_float_and_int():
    assert parse_float("12,34") == 12.34
    assert parse_float(" 100.5 ") == 100.5
    assert parse_float("", 1.0) == 1.0
    assert parse_float(None, 0.5) == 0.5
    assert parse_float(0, 5.0) == 0.0
    
    assert parse_int(" 10 ") == 10
    assert parse_int("12,34") == 12
    assert parse_int("", 3) == 3
    assert parse_int(0, 5) == 0

def test_load_precipitation_file():
    path = os.path.join(WORKSPACE_DIR, "data", "rainfall", "Florianopolis2.csv")
    arr = load_precipitation(path)
    assert isinstance(arr, np.ndarray)
    assert len(arr) == 31411

def test_parse_netuno_project_csv():
    path = os.path.join(WORKSPACE_DIR, "data", "simulation_outputs", "Florianopolis2_Descarte2_Area100_Consumo100_Pessoas4_Percentual90_Coefs08_Recalque20_5000_500_2.csv")
    cfg = parse_netuno_csv(path)
    assert cfg.area == 100.0
    assert cfg.demand_value == 200.0
    assert cfg.residents_count == 4
    assert cfg.rainwater_share == 0.4
    assert cfg.runoff_coeff == 0.75
    assert cfg.discard == 1.0

def test_export_netuno4_csv_roundtrip(tmp_path):
    from netuno.core.parser import NetunoConfig, export_netuno_csv, parse_netuno_csv
    from netuno.core.simulation import SingleTankSimulationResult

    cfg = NetunoConfig(
        area=120.0,
        demand_value=150.0,
        residents_count=4,
        rainwater_share=0.5,
        runoff_coeff=0.85,
        discard=2.0,
        lower_tank_fixed=3000.0,
        lower_tank_mode=0
    )
    results = [
        SingleTankSimulationResult(
            lower_tank_vol=3000.0,
            potential_potable_savings_pct=42.5,
            avg_pluvial_consumed_l_day=120.0,
            avg_potable_consumed_l_day=480.0,
            avg_spilled_l_day=50.0,
            pct_days_full_satisfaction=80.0,
            pct_days_partial_satisfaction=10.0,
            pct_days_null_satisfaction=10.0
        )
    ]

    out_file = str(tmp_path / "test_out_netuno4.csv")
    export_netuno_csv(cfg, results, out_file)
    assert os.path.exists(out_file)

    reparsed_cfg = parse_netuno_csv(out_file)
    assert reparsed_cfg.area == 120.0
    assert reparsed_cfg.demand_value == 150.0
    assert reparsed_cfg.residents_count == 4
    assert reparsed_cfg.rainwater_share == 0.5
    assert reparsed_cfg.runoff_coeff == 0.85
    assert reparsed_cfg.discard == 2.0


def test_export_and_load_netuno_json_project(tmp_path):
    from netuno.core.parser import NetunoConfig, export_netuno_json, load_netuno_project

    cfg = NetunoConfig(
        project_name="Residencial Horizonte",
        area=150.0,
        demand_value=120.0,
        residents_count=5,
        rainwater_share=0.45,
        runoff_coeff=0.88,
        discard=1.5
    )
    precip_data = np.array([0.0, 10.5, 25.0, 0.0, 5.2], dtype=np.float64)
    building_data = {
        "area": 150.0,
        "demand": 120.0,
        "residents": 5,
        "share": 0.45,
        "runoff": 0.88,
        "discard": 1.5
    }
    scenarios = [
        {"name": "Option 1", "lower_vol": 2000.0, "upper_vol": 500.0},
        {"name": "Option 2", "lower_vol": 3500.0, "upper_vol": 500.0}
    ]

    out_file = str(tmp_path / "meu_projeto.netuno")
    export_netuno_json(cfg, out_file, precip_data=precip_data, building_data=building_data, global_scenarios=scenarios)
    assert os.path.exists(out_file)

    proj = load_netuno_project(out_file)
    assert proj["is_json"] is True
    assert proj["config"].project_name == "Residencial Horizonte"
    assert proj["precip_data"] is not None
    assert len(proj["precip_data"]) == 5
    assert proj["building_data"]["area"] == 150.0
    assert proj["building_data"]["demand"] == 120.0
    assert proj["building_data"]["residents"] == 5
    assert len(proj["global_scenarios"]) == 2
    assert proj["global_scenarios"][1]["name"] == "Option 2"
