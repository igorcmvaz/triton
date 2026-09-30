"""
Módulo Core para Cálculo de Indicadores Climatológicos da Série de Precipitação (Netuno 5).
Calcula 9 indicadores pluviometricos: oito do conjunto ETCCDI (PRCPTOT, R95p, RX1day,
RX5day, SDII, R20mm, CDD, CWD) mais o Indice de Sazonalidade de Walsh & Lawler (1981),
que NAO pertence ao ETCCDI. O R10mm, que pertence, nao e calculado aqui.
"""

from collections.abc import Sequence
from datetime import datetime
import numpy as np
import pandas as pd


def find_max_consecutive_run_length(series: pd.Series) -> int:
    """
    Encontra o comprimento máximo de dias consecutivos verdadeiros (ex: dias secos ou dias chuvosos).
    """
    values = series.fillna(False).astype(bool)
    if not values.any():
        return 0
    runs = values.ne(values.shift(fill_value=False)).cumsum()
    return int(values.groupby(runs).sum().max())


def compute_seasonality_index(df: pd.DataFrame) -> float:
    """
    Calcula o Índice de Sazonalidade (Walsh & Lawler) para um determinado ano de precipitação.
    """
    yearly_precipitation: float = df["precipitation"].sum()
    if yearly_precipitation <= 0:
        return np.nan
    # Meses sem registro de chuva precisam entrar como zero; sem esse reindex o
    # índice é subestimado em séries parciais ou anos com meses totalmente secos.
    monthly_precipitation = df.groupby("month")["precipitation"].sum().reindex(range(1, 13), fill_value=0.0)
    return (1 / yearly_precipitation) * (
        monthly_precipitation - (yearly_precipitation / 12)).abs().sum()


class IndicesCalculator:
    """
    Calculador dos 9 Indicadores Climatológicos Médios da Série Histórica de Chuva.
    """
    df: pd.DataFrame
    prcptot: pd.Series
    r95p: pd.Series
    rx1day: pd.Series
    rx5day: pd.Series
    sdii: pd.Series
    r20mm: pd.Series
    cdd: pd.Series
    cwd: pd.Series
    seasonality_indices: pd.Series

    def __init__(
            self,
            data_series: Sequence[tuple[datetime, float]],
            variable_name: str = "precipitation",
            exclude_incomplete: bool = True) -> None:
        self.df = pd.DataFrame(data_series, columns=["date", variable_name])
        if variable_name != "precipitation":
            self.df = self.df.rename(columns={variable_name: "precipitation"})
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df = self.df.dropna(subset=["date"]).copy()
        
        if exclude_incomplete and not self.df.empty:
            years_counts = self.df["date"].dt.year.value_counts()
            complete_years = []
            for y, count in years_counts.items():
                is_leap = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
                expected = 366 if is_leap else 365
                if count >= expected:
                    complete_years.append(y)
            self.df = self.df[self.df["date"].dt.year.isin(complete_years)].copy()
            
        self._set_auxiliary_columns()

    def _set_auxiliary_columns(self) -> None:
        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month
        self.df["dry_days"] = self.df["precipitation"] < 1
        self.df["wet_days"] = self.df["precipitation"] >= 1
        # RX5day é anual: a janela não pode usar precipitação do ano anterior.
        self.df["rolling_5day"] = self.df.groupby("year")["precipitation"].transform(
            lambda values: values.rolling(window=5, min_periods=1).sum()
        )

    def compute_climate_indices(self) -> pd.DataFrame:
        all_years = sorted(self.df["year"].unique())
        
        self.rx1day = self.df.groupby("year")["precipitation"].max().reindex(all_years, fill_value=0.0)
        self.rx5day = self.df.groupby("year")["rolling_5day"].max().reindex(all_years, fill_value=0.0)
        self.sdii = self.df[self.df["wet_days"]].groupby("year")["precipitation"].mean().reindex(all_years, fill_value=np.nan)
        self.r20mm = self.df[self.df["precipitation"] >= 20].groupby("year").size().reindex(all_years, fill_value=0)
        self.cdd = self.df.groupby("year")["dry_days"].apply(
            find_max_consecutive_run_length).reindex(all_years, fill_value=0)
        self.cwd = self.df.groupby("year")["wet_days"].apply(
            find_max_consecutive_run_length).reindex(all_years, fill_value=0)
        
        # R95p considera somente dias úmidos no período de referência; incluir
        # dias secos desloca o percentil para baixo em séries sazonais.
        wet_precipitation = self.df.loc[self.df["wet_days"], "precipitation"]
        q95 = wet_precipitation.quantile(0.95) if not wet_precipitation.empty else np.inf
        self.r95p = self.df[
            self.df["precipitation"] > q95
            ].groupby("year")["precipitation"].sum().reindex(all_years, fill_value=0.0)
            
        self.prcptot = self.df[self.df["wet_days"]].groupby("year")["precipitation"].sum().reindex(all_years, fill_value=0.0)
        
        try:
            self.seasonality_indices = self.df.groupby(
                "year")[["month", "precipitation"]].apply(compute_seasonality_index, include_groups=False).reindex(all_years, fill_value=np.nan)
        except TypeError:
            self.seasonality_indices = self.df.groupby(
                "year")[["month", "precipitation"]].apply(compute_seasonality_index).reindex(all_years, fill_value=np.nan)

        precipitation_indices = pd.DataFrame({
            "year": all_years,
            "PRCPTOT": self.prcptot.values,
            "R95p": self.r95p.values,
            "RX1day": self.rx1day.values,
            "RX5day": self.rx5day.values,
            "SDII": self.sdii.values,
            "R20mm": self.r20mm.values,
            "CDD": self.cdd.values,
            "CWD": self.cwd.values,
            "Seasonality_Index": self.seasonality_indices.values
            })
        return precipitation_indices
