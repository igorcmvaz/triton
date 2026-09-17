"""O arranjo de abastecimento é uma resposta só, lida igual pelo econômico e pela ACV."""

import json
import os
import tempfile

import numpy as np
import pytest

from netuno.core.economic import run_economic_analysis
from netuno.core.environmental import EnvironmentalConfig, calculate_lca
from netuno.core.parser import NetunoConfig, export_netuno_json, load_netuno_project
from netuno.core.pump_energy import compute_annual_pump_energy
from netuno.core.simulation import run_single_simulation
from netuno.core.supply_arrangement import (
    ACIONAMENTOS_POR_PESSOA_DIA,
    GRAVIDADE,
    NAO_INFORMADO,
    PRESSURIZACAO,
    RECALQUE,
    arranjo_de,
)


def _chuva(anos=3):
    rng = np.random.default_rng(7)
    dias = int(365 * anos)
    return np.where(rng.random(dias) < 0.4, rng.gamma(0.8, 12.0, dias), 0.0)


def _projeto(arranjo):
    cfg = NetunoConfig()
    cfg.supply_arrangement = arranjo
    cfg.upper_tank_used = 1 if arranjo == RECALQUE else 0
    cfg.residents_count = 4
    cfg.cost_lower_tank = 3000.0
    return cfg


def _simular(cfg):
    recalque = arranjo_de(cfg) == RECALQUE
    return run_single_simulation(
        precip_data=_chuva(), lower_tank_vol=5000.0, area=150.0, discard_mm=2.0,
        total_demand_per_day=600.0, rainwater_share=0.4,
        upper_tank_vol=500.0 if recalque else 0.0, upper_tank_used=recalque,
        pumping_threshold=150.0 if recalque else 0.0,
    )


@pytest.mark.parametrize("arranjo", [GRAVIDADE, NAO_INFORMADO])
def test_sem_bomba_nao_ha_energia_em_modulo_algum(arranjo):
    cfg = _projeto(arranjo)
    sim = _simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    assert energia.annual_kwh == 0.0
    assert run_economic_analysis(cfg, sim).annual_pump_kwh == 0.0
    acv = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3, EnvironmentalConfig(
        supply_arrangement=cfg.supply_arrangement, upper_tank_used=False))
    assert acv.annual_pumping_co2_kg == 0.0


@pytest.mark.parametrize("arranjo", [RECALQUE, PRESSURIZACAO])
def test_economico_e_acv_usam_a_mesma_energia(arranjo):
    cfg = _projeto(arranjo)
    sim = _simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    econ = run_economic_analysis(cfg, sim)
    assert energia.annual_kwh > 0
    assert econ.annual_pump_kwh == pytest.approx(energia.annual_kwh, rel=1e-9)


def test_pressurizacao_bombeia_todo_o_volume_pluvial():
    cfg = _projeto(PRESSURIZACAO)
    sim = _simular(cfg)
    energia = compute_annual_pump_energy(cfg, sim)
    assert energia.annual_pumped_m3 == pytest.approx(sim.annual_pluvial_consumed_m3)
    assert energia.annual_cycles == round(4 * ACIONAMENTOS_POR_PESSOA_DIA * 365.25)


def test_pressurizacao_cresce_com_a_pressao_de_trabalho():
    baixa, alta = _projeto(PRESSURIZACAO), _projeto(PRESSURIZACAO)
    baixa.pressurizer_pressure_m, alta.pressurizer_pressure_m = 12.0, 24.0
    sim = _simular(baixa)
    e_baixa = compute_annual_pump_energy(baixa, sim).annual_kwh
    e_alta = compute_annual_pump_energy(alta, sim).annual_kwh
    assert e_alta == pytest.approx(2.0 * e_baixa, rel=1e-9)


def test_gravidade_nao_compra_nem_fabrica_motobomba():
    com_bomba, sem_bomba = _projeto(PRESSURIZACAO), _projeto(GRAVIDADE)
    sim = _simular(sem_bomba)
    assert (run_economic_analysis(com_bomba, sim).capex_total
            - run_economic_analysis(sem_bomba, sim).capex_total) == pytest.approx(
        com_bomba.pump_unit_cost * com_bomba.pump_count)
    acv = calculate_lca(5000.0, sim.annual_pluvial_consumed_m3,
                        EnvironmentalConfig(supply_arrangement=GRAVIDADE, upper_tank_used=False))
    assert acv.pump_embodied_co2_kg == 0.0
    assert acv.upper_tank_mass_kg == 0.0


@pytest.mark.parametrize("arranjo", [RECALQUE, PRESSURIZACAO, GRAVIDADE])
def test_cloracao_entra_na_acv_em_qualquer_arranjo(arranjo):
    acv = calculate_lca(5000.0, 80.0, EnvironmentalConfig(
        supply_arrangement=arranjo, upper_tank_used=arranjo == RECALQUE))
    assert acv.annual_treatment_co2_kg > 0


def test_so_o_recalque_tem_caixa_superior_no_carbono():
    for arranjo, esperado in ((RECALQUE, True), (PRESSURIZACAO, False)):
        acv = calculate_lca(5000.0, 80.0, EnvironmentalConfig(supply_arrangement=arranjo))
        assert (acv.upper_tank_mass_kg > 0) is esperado


def test_arquivo_antigo_sem_caixa_abre_como_nao_informado():
    cfg = NetunoConfig()
    cfg.upper_tank_used = 0
    assert arranjo_de(cfg) == NAO_INFORMADO
    cfg.upper_tank_used = 1
    assert arranjo_de(cfg) == RECALQUE


def test_arranjo_sobrevive_a_gravar_e_reabrir():
    cfg = _projeto(PRESSURIZACAO)
    cfg.pressurizer_pressure_m = 21.0
    cfg.pressurizer_starts_per_person_day = 6.0
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "p.netuno")
        export_netuno_json(cfg, caminho, precip_data=_chuva(1))
        with open(caminho, encoding="utf-8") as f:
            assert json.load(f)["inputs"]["reservoirs_and_pumping"]["supply_arrangement"] == PRESSURIZACAO
        lido = load_netuno_project(caminho)["config"]
    assert arranjo_de(lido) == PRESSURIZACAO
    assert lido.pressurizer_pressure_m == 21.0
    assert lido.pressurizer_starts_per_person_day == 6.0
