"""
Testes unitários para calculator.py e IndicesCalculator (Indicadores Climatológicos).
"""

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pytest

from netuno.core.calculator import IndicesCalculator, find_max_consecutive_run_length, compute_seasonality_index
from netuno.core.parser import load_precipitation

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_find_max_consecutive_run_length():
    assert find_max_consecutive_run_length(pd.Series([1, 1, 0, 0, 1, 1, 1, 1, 0])) == 4
    assert find_max_consecutive_run_length(pd.Series([0, 0, 0])) == 0
    assert find_max_consecutive_run_length(pd.Series([True, True, False, True])) == 2


def test_compute_seasonality_index():
    df = pd.DataFrame({
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "precipitation": [10.0] * 12
    })
    # Rain is perfectly uniform, seasonality index should be 0.0
    si = compute_seasonality_index(df)
    assert abs(si) < 1e-5

    # Zero rainfall returns NaN
    df_zero = pd.DataFrame({
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "precipitation": [0.0] * 12
    })
    assert np.isnan(compute_seasonality_index(df_zero))

    # Meses ausentes representam chuva zero e devem entrar na soma anual.
    df_one_month = pd.DataFrame({"month": [1], "precipitation": [120.0]})
    assert compute_seasonality_index(df_one_month) == pytest.approx(11.0 / 6.0)


def test_indices_calculator_synthetic():
    start_dt = datetime(2020, 1, 1)
    # 365 days of synthetic data
    # 10 mm every 5th day
    rain = [10.0 if i % 5 == 0 else 0.0 for i in range(365)]
    data_series = [(start_dt + timedelta(days=i), float(val)) for i, val in enumerate(rain)]

    calc = IndicesCalculator(data_series, exclude_incomplete=False)
    df_indices = calc.compute_climate_indices()

    assert not df_indices.empty
    assert len(df_indices) == 1
    assert "PRCPTOT" in df_indices.columns
    assert "R95p" in df_indices.columns
    assert "RX1day" in df_indices.columns
    assert "RX5day" in df_indices.columns
    assert "SDII" in df_indices.columns
    assert "R20mm" in df_indices.columns
    assert "CDD" in df_indices.columns
    assert "CWD" in df_indices.columns
    assert "Seasonality_Index" in df_indices.columns

    row = df_indices.iloc[0]
    assert row["year"] == 2020
    assert row["RX1day"] == 10.0
    assert row["CDD"] == 4  # max consecutive dry days (0.0) is 4
    assert row["CWD"] == 1  # max consecutive wet days (10.0) is 1


def test_indices_use_wet_day_percentile_and_keep_windows_inside_year():
    """Protege R95p contra dias secos e RX5day contra vazamento entre anos."""
    start_dt = datetime(2020, 12, 29)
    rain = [10.0, 10.0, 10.0, 10.0, 10.0]
    calc = IndicesCalculator([(start_dt + timedelta(days=i), value) for i, value in enumerate(rain)], exclude_incomplete=False)
    indices = calc.compute_climate_indices().set_index("year")
    assert indices.loc[2020, "RX5day"] == 30.0
    assert indices.loc[2021, "RX5day"] == 20.0

    # Com 80 dias secos e 20 úmidos (1..20 mm), o percentil de dias úmidos é
    # 19,05 mm; somente o evento de 20 mm compõe R95p.
    start_dt = datetime(2022, 1, 1)
    wet_day_reference = [0.0] * 80 + [float(value) for value in range(1, 21)]
    calc = IndicesCalculator([
        (start_dt + timedelta(days=i), value)
        for i, value in enumerate(wet_day_reference)
    ], variable_name="rain_mm", exclude_incomplete=False)
    row = calc.compute_climate_indices().iloc[0]
    assert row["R95p"] == 20.0


def test_indices_calculator_real_file():
    path = os.path.join(WORKSPACE_DIR, "data", "rainfall", "Florianopolis2.csv")
    precip = load_precipitation(path)
    start_dt = datetime(2002, 1, 1)
    data_series = [(start_dt + timedelta(days=i), float(val)) for i, val in enumerate(precip)]

    calc = IndicesCalculator(data_series)
    df_indices = calc.compute_climate_indices()

    assert len(df_indices) > 0  # Multiple years calculated
    assert (df_indices["PRCPTOT"] > 100).all()
    assert (df_indices["PRCPTOT"] > 500).all()
    assert (df_indices["RX1day"] > 10.0).all()
    assert (df_indices["CDD"] >= 5).all()


def test_exclude_incomplete_years():
    # 2021: completo (365 dias)
    # 2022: incompleto (10 dias)
    start_dt = datetime(2021, 1, 1)
    rain = [5.0] * 365 + [2.0] * 10
    data_series = [(start_dt + timedelta(days=i), float(val)) for i, val in enumerate(rain)]

    # Com exclude_incomplete=True (padrão), apenas 2021 deve ser calculado
    calc_exclude = IndicesCalculator(data_series)
    df_exclude = calc_exclude.compute_climate_indices()
    assert list(df_exclude["year"]) == [2021]

    # Com exclude_incomplete=False, ambos 2021 e 2022 devem ser calculados
    calc_include = IndicesCalculator(data_series, exclude_incomplete=False)
    df_include = calc_include.compute_climate_indices()
    assert list(df_include["year"]) == [2021, 2022]
