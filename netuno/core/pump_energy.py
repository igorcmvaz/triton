"""
Cálculo compartilhado de consumo elétrico da motobomba a partir da simulação
hidrica (Etapa 3) e parâmetros do NetunoConfig — mesma física usada na Etapa 4/5.
"""

from dataclasses import dataclass
from typing import Optional

from netuno.core.parser import NetunoConfig
from netuno.core.pump_hydraulics import (
    rendimento_do_motor,
    ALTURA_MANOMETRICA_PADRAO_M,
    TEMPO_DE_PARTIDA_H,
    energia_especifica_a_partir_da_vazao,
    energia_especifica_kwh_por_m3,
    ponto_de_operacao,
    rendimento_tipico,
    vazao_l_por_h,
)
from netuno.core.pressurizer_catalog import (
    POR_CHAVE,
    VAZAO_DO_PONTO_PADRAO_L_MIN,
    energia,
    energia_personalizada,
)
from netuno.core.simulation import SingleTankSimulationResult
from netuno.core.supply_arrangement import (
    ACIONAMENTOS_POR_PESSOA_DIA,
    NAO_INFORMADO,
    PRESSAO_DE_TRABALHO_PADRAO_M,
    PRESSURIZACAO,
    RECALQUE,
    arranjo_de,
    usa_bomba,
    usa_caixa_superior,
)

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
    arrangement: str = NAO_INFORMADO


def _rendimentos(config: NetunoConfig, altura: float):
    eta = (
        max(0.01, config.pump_efficiency / 100.0)
        if config.pump_efficiency > 0
        else rendimento_tipico(config.pump_power_kw)
    )
    # A placa e de eixo: falta o rendimento do motor para chegar ao que o
    # medidor registra. Sem valor informado, vale a Tabela 13 da NBR 17094-2.
    eta_motor = float(getattr(config, "pump_motor_efficiency", 0.0) or 0.0)
    eta_motor = (
        max(0.01, min(1.0, eta_motor / 100.0))
        if eta_motor > 0
        else rendimento_do_motor(config.pump_power_kw)
    )
    vazao = (
        config.pump_flow_rate
        if config.pump_flow_rate > 0
        else vazao_l_por_h(config.pump_power_kw, altura, eta)
    )
    return eta, eta_motor, vazao


def compute_annual_pump_energy(
    config: NetunoConfig,
    sim_result: Optional[SingleTankSimulationResult],
    upper_tank_used: Optional[bool] = None,
    arrangement: Optional[str] = None,
) -> PumpEnergyResult:
    """
    Energia anual de abastecimento, conforme o arranjo do projeto.

    É a única fonte de kWh do programa: o econômico, a ACV e os relatórios a
    leem daqui, e por isso não podem divergir.

    - **Recalque**: ``e = ρ·g·H/(η_bomba·η_motor)`` por m³ elevado à caixa, ou
      ``P/(Q·η_motor)`` com vazão declarada, mais as partidas por ``P·t/η_motor``.
    - **Pressurização direta**: tempo ligado vezes potência elétrica, com o
      modelo escolhido em ``pressurizer_catalog``. O pressurizador fica ligado
      enquanto o ponto de uso consome, e a vazão efetiva é a menor entre a da
      curva do modelo na pressão de trabalho e a do ponto; somam-se os retardos
      de desligamento dos controles eletrônicos. Todo o volume pluvial consumido
      passa pela bomba.
    - **Gravidade** e **não informado**: zero.

    ``upper_tank_used`` existe para chamadas antigas: sem arranjo declarado,
    ``False`` equivale a «não informado».
    """
    if arrangement is None:
        arrangement = arranjo_de(config)
        if upper_tank_used is not None and not str(getattr(config, "supply_arrangement", "") or ""):
            arrangement = RECALQUE if upper_tank_used else NAO_INFORMADO

    result = PumpEnergyResult(
        pump_power_cv=config.pump_power_kw / CV_TO_KW if config.pump_power_kw > 0 else 0.0,
        upper_tank_used=usa_caixa_superior(arrangement),
        arrangement=arrangement,
    )

    if sim_result is None or not usa_bomba(arrangement):
        return result
    if arrangement != PRESSURIZACAO and config.pump_power_kw <= 0:
        return result

    # Anos pela média diária, sem piso de um ano: com o piso, uma série de 30 dias
    # dividia o recalque de um mês por um ano inteiro.
    num_years = max(1, sim_result.total_days) / 365.25

    if arrangement == PRESSURIZACAO:
        e = energia_do_pressurizador(config, float(sim_result.annual_pluvial_consumed_m3))
        result.annual_pumped_m3 = float(sim_result.annual_pluvial_consumed_m3)
        result.annual_cycles = int(round(e.partidas_ano))
        result.pump_hours_year = e.horas_ano
        result.annual_kwh = e.kwh_ano
        result.specific_kwh_per_m3 = e.kwh_por_m3
        result.pump_power_cv = _potencia_do_pressurizador_cv(config)
        return result

    result.annual_pumped_m3 = (sim_result.total_pumped_liters / num_years) / 1000.0
    ciclos_por_ano = sim_result.total_pump_cycles / num_years
    result.annual_cycles = int(round(ciclos_por_ano))

    # Rendimento e vazão vêm da potência e da altura quando não forem
    # informados. Fixá-los desacoplava a bomba da própria escolha do usuário.
    altura_informada = float(getattr(config, "pump_manometric_head_m", 0.0) or 0.0)
    altura = altura_informada if altura_informada > 0 else ALTURA_MANOMETRICA_PADRAO_M
    eta, eta_motor, vazao = _rendimentos(config, altura)
    if vazao <= 0:
        return result

    t_rec = (sim_result.total_pumped_liters / num_years) / vazao
    # Ciclos sem arredondar: o econômico somava assim, e os dois têm de coincidir.
    t_part = ciclos_por_ano * config.pump_startup_time_h

    result.pump_hours_year = t_rec + t_part
    # Com vazão informada, a energia por m³ é P/Q, direto. Sem vazão informada,
    # ela vem de ρ·g·H/η. Quando o assistente determinou o desnível, é ele que
    # manda: a vazão do catálogo é o valor nominal do modelo.
    if altura_informada > 0:
        especifica = energia_especifica_kwh_por_m3(altura_informada, eta, eta_motor)
    elif config.pump_flow_rate > 0:
        especifica = energia_especifica_a_partir_da_vazao(
            config.pump_power_kw, vazao, eta_motor)
    else:
        especifica = energia_especifica_kwh_por_m3(altura, eta, eta_motor)
    energia_recalque = especifica * result.annual_pumped_m3
    # Na partida a bomba nao entrega vazao util, mas o motor puxa da tomada:
    # placa / rendimento do MOTOR, sem o rendimento da bomba.
    energia_partidas = (config.pump_power_kw * t_part) / eta_motor
    result.annual_kwh = energia_recalque + energia_partidas

    if result.annual_pumped_m3 > 0:
        result.specific_kwh_per_m3 = result.annual_kwh / result.annual_pumped_m3

    return result


def _partidas_ano(config) -> float:
    acionamentos = float(getattr(config, "pressurizer_starts_per_person_day",
                                 ACIONAMENTOS_POR_PESSOA_DIA) or 0.0)
    moradores = max(0, int(getattr(config, "residents_count", 0) or 0))
    return moradores * acionamentos * 365.25


def _potencia_do_pressurizador_cv(config) -> float:
    modelo = POR_CHAVE.get(str(getattr(config, "pressurizer_model", "") or ""))
    if modelo is not None:
        return modelo.potencia_cv
    return float(getattr(config, "pressurizer_power_kw", 0.0) or 0.0) / CV_TO_KW


def energia_do_pressurizador(config, volume_m3_ano: float):
    """Energia anual do pressurizador do projeto, pelo catálogo ou pelos dados digitados."""
    pressao = float(getattr(config, "pressurizer_pressure_m", 0.0) or 0.0)
    if pressao <= 0:
        pressao = PRESSAO_DE_TRABALHO_PADRAO_M
    q_ponto = float(getattr(config, "pressurizer_point_flow_l_min", 0.0) or 0.0)
    if q_ponto <= 0:
        q_ponto = VAZAO_DO_PONTO_PADRAO_L_MIN
    partidas = _partidas_ano(config)
    modelo = POR_CHAVE.get(str(getattr(config, "pressurizer_model", "") or ""))
    if modelo is not None:
        return energia(modelo, volume_m3_ano, pressao, partidas, q_ponto)
    potencia = float(getattr(config, "pressurizer_power_kw", 0.0) or 0.0)
    vazao = float(getattr(config, "pressurizer_flow_l_min", 0.0) or 0.0)
    vazao = min(vazao, q_ponto) if vazao > 0 else q_ponto
    eta_motor = float(getattr(config, "pump_motor_efficiency", 0.0) or 0.0) / 100.0
    return energia_personalizada(
        potencia, vazao, float(getattr(config, "pressurizer_post_run_s", 0.0) or 0.0),
        volume_m3_ano, partidas, eta_motor or None)


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

    Resolve pela mesma física do caminho principal: ``ρ·g·H/(η_bomba·η_motor)``
    para o recalque, mais as partidas por ``placa/η_motor``. Com a altura de
    recurso de 12 m, o rendimento de bomba de meio CV e o rendimento de motor da
    Tabela 13 da ABNT NBR 17094-2, dá cerca de 0,11 kWh/m³.

    Até a versão 5.0.8 este valor era 0,40 e depois 0,333, ambos derivados de uma
    vazão e um rendimento fixos que, juntos, implicavam 67 m de altura
    manométrica — cerca de cinco vezes o desnível de uma casa com cisterna
    enterrada.
    """
    potencia_kw = BOMBA_PADRAO_CV * CV_TO_KW
    eta = rendimento_tipico(potencia_kw)
    eta_motor = rendimento_do_motor(potencia_kw)
    ponto = ponto_de_operacao(potencia_kw, ALTURA_MANOMETRICA_PADRAO_M, eta)

    # `ponto` devolve energia de eixo; o motor ainda separa eixo de tomada.
    recalque = ponto.energia_especifica_kwh_m3 / eta_motor
    # Na partida não há vazão útil, então não há perda hidráulica a descontar:
    # divide-se pelo rendimento do motor, e não pelo da bomba.
    partidas = BOMBA_PADRAO_PARTIDAS_POR_M3 * TEMPO_DE_PARTIDA_H * potencia_kw / eta_motor
    return recalque + partidas
