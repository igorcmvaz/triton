"""Regressões da interface de linha de comando, sem dependência da GUI."""

import json
from argparse import Namespace
import numpy as np

from netuno.cli import _json_default, _run_project_matrix, _validate_config, run_analysis
from netuno.core.parser import NetunoConfig, export_netuno_json


def test_cli_full_analysis_supports_seasonality_and_json_output():
    cfg = NetunoConfig(
        area=100.0,
        demand_value=100.0,
        residents_count=3,
        demand_monthly=[100.0] * 12,
        residents_monthly=[3] * 12,
        rainwater_share=0.4,
        runoff_coeff=0.9,
        lower_tank_mode=1,
        lower_tank_max=1000.0,
        lower_tank_step=500.0,
        analysis_period_years=20,
    )
    rainfall = np.array([8.0] * 60, dtype=float)

    assert _validate_config(cfg, rainfall) == []
    report = run_analysis(cfg, rainfall, "all", source="test", weight_sensitivity=8, seed=7)

    assert len(report["technical"]["alternatives"]) == 3
    assert "economic" in report and "environmental" in report and "topsis" in report
    assert report["topsis"]["best_volume_l"] in {0.0, 500.0, 1000.0}
    assert len(report["topsis"]["criteria"]) == 7
    assert set(report["topsis"]["ranking"][0]["criterion_values"]) == {
        "technical_potential_pct", "technical_overflow_m3_yr",
        "economic_npv_brl", "economic_discounted_payback_years", "economic_irr_pct",
        "environmental_lifecycle_co2_kg", "environmental_potable_water_m3_yr",
    }
    assert report["topsis"]["weight_sensitivity"]["samples"] == 8
    json.dumps(report, default=_json_default)


def test_cli_validation_rejects_incomplete_monthly_seasonality():
    cfg = NetunoConfig(demand_monthly=[100.0] * 11, residents_monthly=[3] * 12)
    errors = _validate_config(cfg, np.array([1.0], dtype=float))
    assert any("demand_monthly" in error for error in errors)


def test_cli_reports_requested_and_effective_sweep_grid():
    cfg = NetunoConfig(
        area=100.0, demand_value=100.0, residents_count=3,
        rainwater_share=0.4, runoff_coeff=0.9, lower_tank_mode=1,
        lower_tank_max=10001.0, lower_tank_step=250.0,
    )

    report = run_analysis(cfg, np.array([0.0, 8.0], dtype=float), "technical", source="test-grid")
    grid = report["technical"]["summary"]["sweep_grid"]

    assert grid["requested_step_l"] == 250.0
    assert grid["effective_step_l"] == 500.0
    assert grid["step_adjusted"] is True
    assert grid["positive_volume_count"] == 21
    assert report["technical"]["alternatives"][-1]["lower_tank_volume_l"] == 10001.0


def _project_matrix_args(project, output_dir, rainfall_dir=None, ignore_project_factors=False):
    return Namespace(
        projects=[str(project)], rainfall_dir=str(rainfall_dir) if rainfall_dir else None,
        recursive=False, ignore_project_factors=ignore_project_factors,
        analysis="technical", weights=None, weight_sensitivity=0, seed=42,
        output_dir=str(output_dir), quiet=True,
    )


def test_cli_project_matrix_expands_factorial_block_and_rainfall_folder(tmp_path):
    cfg = NetunoConfig(
        area=100.0, demand_value=100.0, residents_count=3, rainwater_share=0.4,
        runoff_coeff=0.9, lower_tank_mode=1, lower_tank_max=1000.0, lower_tank_step=1000.0,
    )
    project = tmp_path / "modelo.netuno"
    export_netuno_json(cfg, str(project), precip_data=np.array([8.0] * 30, dtype=float), analysis={})
    raw = json.loads(project.read_text(encoding="utf-8"))
    raw["cli_factorial"] = {"factors": {"area": [80.0, 120.0], "residents_count": [2, 4]}, "rainfall_files": []}
    project.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")

    factorial_output = tmp_path / "factorial"
    _run_project_matrix(_project_matrix_args(project, factorial_output))
    with (factorial_output / "netuno-matriz-detalhado.json").open(encoding="utf-8") as stream:
        factorial = json.load(stream)
    assert len(factorial["reports"]) == 4

    rainfall_dir = tmp_path / "climas"
    rainfall_dir.mkdir()
    (rainfall_dir / "cidade_a.csv").write_text("5\n0\n12\n", encoding="utf-8")
    (rainfall_dir / "cidade_b.csv").write_text("0\n8\n2\n", encoding="utf-8")
    folder_output = tmp_path / "folder"
    _run_project_matrix(_project_matrix_args(project, folder_output, rainfall_dir, ignore_project_factors=True))
    with (folder_output / "netuno-matriz-detalhado.json").open(encoding="utf-8") as stream:
        folder = json.load(stream)
    assert len(folder["reports"]) == 2
    assert {item["rainfall_name"] for item in folder["reports"]} == {"cidade_a", "cidade_b"}
