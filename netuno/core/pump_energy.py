"""
Cálculo compartilhado de consumo elétrico da motobomba a partir da simulação
hidrica (Etapa 3) e parâmetros do NetunoConfig — mesma física usada na Etapa 4/5.
"""

from dataclasses import dataclass
from typing import Optional

from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult

CV_TO_KW = 0.735499


@dataclass
class PumpEnergyResult:
    annual_kwh: float = 0.0
    annual_pumped_m3: float = 0.0
    specific_kwh_per_m3: float = 0.0
    annual_cycles: int = 0
    pump_hours_year: float = 0.0
    pump_power_cv: float = 0.0
    upper_tank_used: bool = False


def compute_annual_pump_energy(
    config: NetunoConfig,
    sim_result: Optional[SingleTankSimulationResult],
    upper_tank_used: Optional[bool] = None,
) -> PumpEnergyResult:
    """
    Estima kWh/ano da motobomba com base nos resultados da simulação:
    E = P_kW * (t_recalque + t_partida) / eta
    """
    result = PumpEnergyResult(
        pump_power_cv=config.pump_power_kw / CV_TO_KW if config.pump_power_kw > 0 else 0.0,
        upper_tank_used=upper_tank_used if upper_tank_used is not None else bool(config.upper_tank_used),
    )

    if sim_result is None:
        return result

    num_years = max(1.0, sim_result.total_days / 365.25)
    result.annual_pumped_m3 = (sim_result.total_pumped_liters / num_years) / 1000.0
    result.annual_cycles = int(round(sim_result.total_pump_cycles / num_years))

    if not result.upper_tank_used or config.pump_flow_rate <= 0:
        return result

    t_rec = (sim_result.total_pumped_liters / num_years) / config.pump_flow_rate
    t_part = result.annual_cycles * config.pump_startup_time_h
    eta = max(0.01, config.pump_efficiency / 100.0) if config.pump_efficiency > 0 else 0.55

    result.pump_hours_year = t_rec + t_part
    result.annual_kwh = (config.pump_power_kw * result.pump_hours_year) / eta

    if result.annual_pumped_m3 > 0:
        result.specific_kwh_per_m3 = result.annual_kwh / result.annual_pumped_m3

    return result


def nearest_pump_cv(power_cv: float) -> float:
    """Retorna a potência tabulada mais próxima para lookup de CO2 incorporado."""
    from netuno.core.environmental import PUMP_EMBEDDED_CO2

    if not PUMP_EMBEDDED_CO2:
        return power_cv
    return min(PUMP_EMBEDDED_CO2.keys(), key=lambda cv: abs(cv - power_cv))
