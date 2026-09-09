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

# ---------------------------------------------------------------------------
# Consumo específico de recurso
# ---------------------------------------------------------------------------
# Quando há simulação, o consumo vem da física acima, com o tempo de recalque e
# o número de partidas que a simulação produziu. Sem simulação, o módulo
# ambiental precisava de um valor de partida, e usava 0,40 kWh/m³ — número sem
# origem, e 36% acima do que a mesma física dá para a bomba padrão.
#
# Deriva-se agora do mesmo cálculo, com as premissas declaradas, para que os
# dois caminhos não possam divergir por construção.

BOMBA_PADRAO_CV = 0.50
BOMBA_PADRAO_VAZAO_L_H = 2280.0
BOMBA_PADRAO_RENDIMENTO = 0.55
BOMBA_PADRAO_TEMPO_DE_PARTIDA_H = 0.03
BOMBA_PADRAO_PARTIDAS_POR_M3 = 2.0


def consumo_especifico_padrao_kwh_por_m3() -> float:
    """kWh por m³ recalcado, para a bomba padrão, sem simulação disponível.

    ``E = P / (Q x eta) + n_partidas x t_partida x P / eta``

    Com 0,5 CV, 2.280 L/h, rendimento de 55% e duas partidas por m³, dá cerca de
    0,333 kWh/m³. As duas partidas por m³ correspondem a um reservatório
    superior de 500 L consumido em ciclos de meia carga, que é o arranjo
    residencial corrente.
    """
    potencia_kw = BOMBA_PADRAO_CV * CV_TO_KW
    vazao_m3_h = BOMBA_PADRAO_VAZAO_L_H / 1000.0
    recalque = potencia_kw / (vazao_m3_h * BOMBA_PADRAO_RENDIMENTO)
    partidas = (
        BOMBA_PADRAO_PARTIDAS_POR_M3
        * BOMBA_PADRAO_TEMPO_DE_PARTIDA_H
        * potencia_kw
        / BOMBA_PADRAO_RENDIMENTO
    )
    return recalque + partidas
