"""
Framework de Testes Estruturados do Triton (InputRainfall, InputData, Output)
Permite executar simulações de balanço hídrico diário passo a passo (dia por dia)
e verificar com precisão os resultados agregados e diários.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np

from triton.core.simulation import run_single_simulation, SingleTankSimulationResult, SimulationDayResult


@dataclass
class InputRainfall:
    """Precipitação diária de entrada (série em mm)."""
    rainfall_mm: List[float]

    @property
    def total_days(self) -> int:
        return len(self.rainfall_mm)


@dataclass
class InputData:
    """Parâmetros físicos e de consumo para o balanço hídrico do Triton."""
    area: float                          # Área de captação (m²)
    runoff_coeff: float                  # Coeficiente de escoamento superficial (C) [0 a 1]
    discard_mm: float                    # Descarte do escoamento inicial (mm)
    residents: int                       # Número de moradores
    demand_per_capita: float             # Demanda total per capita (litros/morador/dia)
    rainwater_share: float               # Percentual da demanda a ser substituída por água pluvial (ex: 0.40 para 40%)
    lower_tank_vol: float                # Volume do reservatório inferior (litros)
    upper_tank_vol: float = 0.0          # Volume do reservatório superior (litros)
    upper_tank_used: bool = False        # Utiliza reservatório superior (duplo reservatório)?
    pumping_threshold: float = 0.0       # Limiar de acionamento da bomba (litros)

    @property
    def total_demand_per_day(self) -> float:
        return self.residents * self.demand_per_capita

    @property
    def pluvial_demand_per_day(self) -> float:
        return self.total_demand_per_day * self.rainwater_share


@dataclass
class DailyOutputDetail:
    """Detalhamento das variáveis do balanço hídrico para 1 dia específico."""
    day_index: int
    precip_mm: float
    eff_precip_mm: float
    harvested_liters: float
    pluvial_consumed_liters: float
    potable_consumed_liters: float
    spilled_liters: float
    lower_tank_end_liters: float
    upper_tank_end_liters: float
    satisfaction_type: str  # "TOTAL", "PARCIAL", "NULO"


@dataclass
class Output:
    """Resultados agregados da simulação do balanço hídrico diário."""
    potential_savings_pct: float                # Potencial de economia de água potável (%)
    avg_pluvial_consumed_l_day: float           # Consumo médio de água pluvial (L/dia)
    avg_potable_consumed_l_day: float           # Consumo médio de água potável (L/dia)
    avg_spilled_l_day: float                    # Volume médio extravasado (L/dia)
    pct_days_full_satisfaction: float           # % de dias com atendimento total
    pct_days_partial_satisfaction: float        # % de dias com atendimento parcial
    pct_days_null_satisfaction: float           # % de dias com atendimento nulo
    daily_details: List[DailyOutputDetail] = field(default_factory=list)


@dataclass
class WaterBalanceTestCase:
    """Caso de teste completo encapsulando entradas e resultados esperados."""
    test_id: str
    name: str
    input_rainfall: InputRainfall
    input_data: InputData
    expected_output: Optional[Output] = None

    def run(self) -> Output:
        """Executa o balanço hídrico diário iteração a iteração."""
        precip_arr = np.array(self.input_rainfall.rainfall_mm, dtype=np.float64)
        
        sim_res = run_single_simulation(
            precip_data=precip_arr,
            lower_tank_vol=self.input_data.lower_tank_vol,
            area=self.input_data.area,
            runoff_coeff=self.input_data.runoff_coeff,
            discard_mm=self.input_data.discard_mm,
            total_demand_per_day=self.input_data.total_demand_per_day,
            rainwater_share=self.input_data.rainwater_share,
            upper_tank_vol=self.input_data.upper_tank_vol,
            upper_tank_used=self.input_data.upper_tank_used,
            pumping_threshold=self.input_data.pumping_threshold,
            store_daily_details=True
        )
        
        sat_map = {2: "TOTAL", 1: "PARCIAL", 0: "NULO"}
        
        daily_details = [
            DailyOutputDetail(
                day_index=d.day_index + 1,  # 1-indexed para fácil leitura
                precip_mm=round(d.precip_mm, 4),
                eff_precip_mm=round(d.eff_precip_mm, 4),
                harvested_liters=round(d.harvested_liters, 4),
                pluvial_consumed_liters=round(d.pluvial_consumed_liters, 4),
                potable_consumed_liters=round(d.potable_consumed_liters, 4),
                spilled_liters=round(d.spilled_liters, 4),
                lower_tank_end_liters=round(d.lower_tank_end_liters, 4),
                upper_tank_end_liters=round(d.upper_tank_end_liters, 4),
                satisfaction_type=sat_map.get(d.satisfaction_type, "NULO")
            )
            for d in sim_res.daily_results
        ]
        
        return Output(
            potential_savings_pct=round(sim_res.potential_potable_savings_pct, 4),
            avg_pluvial_consumed_l_day=round(sim_res.avg_pluvial_consumed_l_day, 4),
            avg_potable_consumed_l_day=round(sim_res.avg_potable_consumed_l_day, 4),
            avg_spilled_l_day=round(sim_res.avg_spilled_l_day, 4),
            pct_days_full_satisfaction=round(sim_res.pct_days_full_satisfaction, 4),
            pct_days_partial_satisfaction=round(sim_res.pct_days_partial_satisfaction, 4),
            pct_days_null_satisfaction=round(sim_res.pct_days_null_satisfaction, 4),
            daily_details=daily_details
        )
