"""
A energia da motobomba, do eixo à tomada.

A potência de placa de um motor é a potência mecânica **no eixo**: a ABNT NBR
17094-2:2016 manda marcar o rendimento na placa como grandeza separada, o que só
faz sentido se a potência for a de eixo. Daí a cadeia completa:

    recalque:  e = ρ·g·H / (η_bomba · η_motor)   kWh por m³ elevado
    partidas:  E = placa · t / η_motor           sem η_bomba, porque não há vazão

Três versões desta conta já existiram no programa:

  antes   P × horas / η_bomba, nos dois termos. Errava nos dois sentidos ao mesmo
          tempo: descontava a perda hidráulica duas vezes e ignorava o motor.
  depois  corrigiu o recalque e deixou as partidas com o η_bomba.
  agora   os dois termos, com o rendimento do motor no lugar certo.

Conferência que sustenta a leitura de eixo: a Dancor CP-4R de 1/2 CV dá 8,4 m³/h a
6 m.c.a. e 0,4 m³/h a 22 m.c.a.; ajustada a parábola H = H₀ − kQ², a 12 m.c.a. ela
entrega 6,65 m³/h, o que são 217 W hidráulicos contra 370 W de placa. A razão de
0,59 é rendimento de bomba, não de conjunto fio-a-água.

O **tempo** de partida não foi tocado: é premissa de projeto e está na pendência 14.
"""

from __future__ import annotations

import numpy as np
import pytest

from netuno.core.parser import NetunoConfig
from netuno.core.pump_energy import (
    compute_annual_pump_energy,
    consumo_especifico_padrao_kwh_por_m3,
)
from netuno.core.pump_hydraulics import (
    ALTURA_MANOMETRICA_PADRAO_M,
    energia_especifica_kwh_por_m3,
    rendimento_do_motor,
    rendimento_tipico,
)
from netuno.core.simulation import run_single_simulation


@pytest.fixture(scope="module")
def sim():
    rng = np.random.default_rng(11)
    chuva = np.clip(rng.gamma(0.55, 8.0, 1826), 0, None)
    return run_single_simulation(
        precip_data=chuva, lower_tank_vol=5000.0, area=150.0, runoff_coeff=0.85,
        discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4,
        upper_tank_vol=1000.0, upper_tank_used=True, pumping_threshold=100.0,
    )


def _config():
    cfg = NetunoConfig()
    cfg.upper_tank_used = True
    cfg.pump_power_kw = 0.37
    cfg.pump_efficiency = 0.0
    cfg.pump_flow_rate = 0.0
    cfg.pump_manometric_head_m = ALTURA_MANOMETRICA_PADRAO_M
    cfg.pump_startup_time_h = 0.03
    return cfg


def test_a_energia_e_recalque_mais_partidas_pelo_rendimento_do_motor(sim):
    """Recalque por ρgH/(η_bomba·η_motor); partidas por placa/η_motor."""
    cfg = _config()
    r = compute_annual_pump_energy(cfg, sim)

    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    # Ciclos por ano sem arredondar, como o econômico soma.
    t_part = sim.total_pump_cycles / (sim.total_days / 365.25) * cfg.pump_startup_time_h
    esperado = especifica * r.annual_pumped_m3 + (cfg.pump_power_kw * t_part) / eta_motor

    assert r.annual_kwh == pytest.approx(esperado, rel=1e-9)


def test_o_rendimento_do_motor_sai_da_tabela_da_norma():
    """Tabela 13 da ABNT NBR 17094-2:2016, motores de 2 polos, linha IR1."""
    assert rendimento_do_motor(0.37) == pytest.approx(0.605)   # 1/2 CV
    assert rendimento_do_motor(0.75) == pytest.approx(0.693)   # 1 CV
    assert rendimento_do_motor(0.18) == pytest.approx(0.500)   # 1/4 CV


def test_o_rendimento_do_motor_informado_prevalece(sim):
    """Quem lê a placa informa o valor dela, e o programa obedece."""
    cfg = _config()
    padrao = compute_annual_pump_energy(cfg, sim).annual_kwh
    cfg.pump_motor_efficiency = 72.0        # linha IR2, alto rendimento
    melhor = compute_annual_pump_energy(cfg, sim).annual_kwh
    assert melhor < padrao
    assert melhor / padrao == pytest.approx(rendimento_do_motor(0.37) / 0.72, rel=1e-9)


def test_as_partidas_nao_dividem_pelo_rendimento_da_bomba(sim):
    """Na partida não há vazão, logo não há perda hidráulica a descontar."""
    cfg = _config()
    r = compute_annual_pump_energy(cfg, sim)

    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    t_part = r.annual_cycles * cfg.pump_startup_time_h
    com_bomba = especifica * r.annual_pumped_m3 + (cfg.pump_power_kw * t_part) / (eta * eta_motor)

    assert com_bomba > r.annual_kwh


def test_sem_partidas_a_energia_e_so_o_recalque(sim):
    cfg = _config()
    cfg.pump_startup_time_h = 0.0
    r = compute_annual_pump_energy(cfg, sim)
    eta = rendimento_tipico(cfg.pump_power_kw)
    eta_motor = rendimento_do_motor(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta, eta_motor)
    assert r.annual_kwh == pytest.approx(especifica * r.annual_pumped_m3, rel=1e-9)


def test_o_consumo_especifico_de_recurso_segue_a_mesma_convencao():
    """O valor de recurso usado quando não há simulação vem da mesma conta."""
    assert 0.0 < consumo_especifico_padrao_kwh_por_m3() < 0.30


def test_o_economico_e_a_acv_calculam_a_mesma_energia(sim):
    """Duas cópias da fórmula divergiriam, e foi assim que ela se espalhou."""
    from netuno.core.economic import run_economic_analysis

    cfg = _config()
    cfg.water_tariffs = [(0.0, 10.0, 3.08, 1), (10.0, 999999.0, 6.81, 1)]
    econ = run_economic_analysis(cfg, sim)
    bomba = compute_annual_pump_energy(cfg, sim)

    assert econ.annual_pump_kwh == pytest.approx(bomba.annual_kwh, rel=0.02)
