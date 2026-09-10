"""
Cálculo compartilhado de consumo elétrico da motobomba a partir da simulação
hidrica (Etapa 3) e parâmetros do NetunoConfig — mesma física usada na Etapa 4/5.
"""

from dataclasses import dataclass
from typing import Optional

from netuno.core.parser import NetunoConfig
from netuno.core.pump_hydraulics import (
    ALTURA_MANOMETRICA_PADRAO_M,
    TEMPO_DE_PARTIDA_H,
    energia_especifica_a_partir_da_vazao,
    energia_especifica_kwh_por_m3,
    ponto_de_operacao,
    rendimento_tipico,
    vazao_l_por_h,
)
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
    Estima kWh/ano da motobomba com base nos resultados da simulação.

    O recalque custa ``e = ρ·g·H/η`` por m³ elevado, ou ``P/Q`` quando a vazão
    de operação é declarada. As partidas somam ``P × t``: a potência de placa
    já é o que o motor consome, e dividi-la por η contaria a perda duas vezes.

    A fórmula antiga, ``E = P × (t_recalque + t_partida) / η``, superestimava
    o consumo em 1/η e sobrevivia aqui no termo das partidas.
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

    if not result.upper_tank_used:
        return result

    # Rendimento e vazão vêm da potência e da altura quando não forem
    # informados. Fixá-los desacoplava a bomba da própria escolha do usuário.
    altura_informada = float(getattr(config, "pump_manometric_head_m", 0.0) or 0.0)
    altura = altura_informada if altura_informada > 0 else ALTURA_MANOMETRICA_PADRAO_M
    eta = (
        max(0.01, config.pump_efficiency / 100.0)
        if config.pump_efficiency > 0
        else rendimento_tipico(config.pump_power_kw)
    )
    vazao = (
        config.pump_flow_rate
        if config.pump_flow_rate > 0
        else vazao_l_por_h(config.pump_power_kw, altura, eta)
    )
    if vazao <= 0:
        return result

    t_rec = (sim_result.total_pumped_liters / num_years) / vazao
    t_part = result.annual_cycles * config.pump_startup_time_h

    result.pump_hours_year = t_rec + t_part
    # O recalque custa ρ·g·H/η por m³, e as partidas somam energia sem entregar
    # vazão útil. Antes tudo saía de potência × horas, o que embutia a altura
    # nos números fixos de vazão e rendimento.
    # Com vazão informada, a energia por m³ é P/Q, direto. Sem vazão informada,
    # ela vem de ρ·g·H/η. As duas formas coincidem quando a vazão é a que a
    # bomba entrega naquela altura, e é a primeira que vale quando o usuário
    # declara o ponto de operação.
    if altura_informada > 0:
        # O assistente determinou o desnível: é ele que manda. A vazão do
        # catálogo é o valor nominal do modelo, não a vazão contra esta altura.
        especifica = energia_especifica_kwh_por_m3(altura_informada, eta)
    elif config.pump_flow_rate > 0:
        especifica = energia_especifica_a_partir_da_vazao(config.pump_power_kw, vazao)
    else:
        especifica = energia_especifica_kwh_por_m3(altura, eta)
    energia_recalque = especifica * result.annual_pumped_m3
    # A potencia de placa ja e o que o motor consome durante a partida:
    # dividir por eta aqui contaria a perda duas vezes, como diz a docstring
    # de energia_especifica_a_partir_da_vazao.
    energia_partidas = config.pump_power_kw * t_part
    result.annual_kwh = energia_recalque + energia_partidas

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
BOMBA_PADRAO_PARTIDAS_POR_M3 = 2.0


def consumo_especifico_padrao_kwh_por_m3() -> float:
    """kWh por m³ elevado, sem simulação disponível.

    Resolve pela mesma física do caminho principal: ``ρ·g·H/η`` para o recalque,
    mais o custo das partidas. Com a altura de recurso de 12 m e o rendimento
    típico de meio CV, dá cerca de 0,07 kWh/m³.

    Até a versão 5.0.8 este valor era 0,40 e depois 0,333, ambos derivados de uma
    vazão e um rendimento fixos que, juntos, implicavam 67 m de altura
    manométrica — cerca de cinco vezes o desnível de uma casa com cisterna
    enterrada.
    """
    potencia_kw = BOMBA_PADRAO_CV * CV_TO_KW
    eta = rendimento_tipico(potencia_kw)
    ponto = ponto_de_operacao(potencia_kw, ALTURA_MANOMETRICA_PADRAO_M, eta)

    recalque = ponto.energia_especifica_kwh_m3
    # Sem o 1/eta, pelo mesmo motivo do termo de partidas em
    # compute_annual_pump_energy.
    partidas = BOMBA_PADRAO_PARTIDAS_POR_M3 * TEMPO_DE_PARTIDA_H * potencia_kw
    return recalque + partidas
