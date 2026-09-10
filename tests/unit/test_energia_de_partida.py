"""A energia das partidas não divide a potência de placa pelo rendimento.

O módulo `pump_hydraulics` fixa a convenção e a escreve na docstring de
`energia_especifica_a_partir_da_vazao`: a potência de placa é o que o motor
**consome**, e o rendimento já está embutido no fato de uma bomba de P kW
entregar Q m³/h naquela altura. Dividir por η outra vez conta a perda duas vezes.

O termo de recalque segue essa convenção desde a correção anterior. O termo das
partidas, dentro da **mesma expressão**, continuava fazendo `P × t / η` — a
fórmula que a própria docstring descreve como defeituosa. Em três lugares:
`compute_annual_pump_energy`, `consumo_especifico_padrao_kwh_por_m3` e o motor
econômico.

No caso padrão (meio CV, 12 m.c.a., rendimento 0,50, 98 ciclos/ano) as partidas
pesavam 2,18 kWh/ano contra 1,09 corretos, sobre 5,72 kWh/ano de recalque: 14% do
consumo anual da motobomba, que atravessa para o custo de energia no fluxo de
caixa e para a emissão operacional na avaliação de ciclo de vida.

O **tempo** de partida não foi tocado: é premissa de projeto, está anotado nas
pendências e continua valendo o que o usuário informar.
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


def test_a_energia_e_recalque_mais_partidas_sem_dividir_por_rendimento(sim):
    cfg = _config()
    r = compute_annual_pump_energy(cfg, sim)

    eta = rendimento_tipico(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta)
    t_part = r.annual_cycles * cfg.pump_startup_time_h
    esperado = especifica * r.annual_pumped_m3 + cfg.pump_power_kw * t_part

    assert r.annual_kwh == pytest.approx(esperado, rel=1e-9)


def test_a_formula_antiga_daria_mais_energia(sim):
    """Guarda a diferença: se alguém repuser o 1/η, este teste cai."""
    cfg = _config()
    r = compute_annual_pump_energy(cfg, sim)

    eta = rendimento_tipico(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta)
    t_part = r.annual_cycles * cfg.pump_startup_time_h
    antiga = especifica * r.annual_pumped_m3 + (cfg.pump_power_kw * t_part) / eta

    assert antiga > r.annual_kwh
    assert antiga / r.annual_kwh > 1.10


def test_sem_partidas_a_energia_e_so_o_recalque(sim):
    cfg = _config()
    cfg.pump_startup_time_h = 0.0
    r = compute_annual_pump_energy(cfg, sim)
    eta = rendimento_tipico(cfg.pump_power_kw)
    especifica = energia_especifica_kwh_por_m3(cfg.pump_manometric_head_m, eta)
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
