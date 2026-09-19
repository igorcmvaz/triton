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


def test_a_pressao_so_pesa_quando_a_curva_limita_a_vazao():
    """Enquanto o modelo entrega mais que o ponto de uso, quem dita o tempo ligado
    é o ponto; acima disso, a curva estrangula a vazão e a bomba fica mais tempo ligada."""
    cfgs = {h: _projeto(PRESSURIZACAO) for h in (12.0, 18.0, 24.0)}
    for h, cfg in cfgs.items():
        cfg.pressurizer_pressure_m = h
    sim = _simular(cfgs[12.0])
    e = {h: compute_annual_pump_energy(cfg, sim).annual_kwh for h, cfg in cfgs.items()}
    # Komeco TP 820T: 22 L/min a 12 m.c.a. e 13 L/min a 18, acima dos 9 L/min da bacia
    assert e[12.0] == pytest.approx(e[18.0], rel=1e-9)
    # a 24 m.c.a. a curva dá 4,4 L/min, menos que o ponto pede
    assert e[24.0] == pytest.approx(e[12.0] * 9.0 / (40.0 * 3.0 / 27.0), rel=1e-6)


def test_o_modelo_maior_gasta_mais_quando_o_ponto_limita_a_vazao():
    """ABNT NBR 5626:2020, 6.5.11.12: a escolha da bomba é que minimiza a energia."""
    pequeno, grande = _projeto(PRESSURIZACAO), _projeto(PRESSURIZACAO)
    grande.pressurizer_model = "komeco_tp825t"
    sim = _simular(pequeno)
    e_p = compute_annual_pump_energy(pequeno, sim)
    e_g = compute_annual_pump_energy(grande, sim)
    assert e_g.pump_hours_year == pytest.approx(e_p.pump_hours_year)
    assert e_g.annual_kwh > e_p.annual_kwh


def test_o_retardo_eletronico_soma_tempo_a_cada_partida():
    from netuno.core.pressurizer_catalog import POR_CHAVE, energia
    syllent = POR_CHAVE["syllent_impulse"]
    sem = energia(syllent, 60.0, 12.0, 0.0)
    com = energia(syllent, 60.0, 12.0, 7373.0)
    assert com.horas_ano - sem.horas_ano == pytest.approx(7373.0 * 10.0 / 3600.0)


def test_personalizado_usa_os_dados_digitados():
    cfg = _projeto(PRESSURIZACAO)
    cfg.pressurizer_model = "personalizado"
    cfg.pressurizer_power_kw, cfg.pressurizer_flow_l_min = 0.37, 20.0
    cfg.pressurizer_point_flow_l_min, cfg.pressurizer_post_run_s = 10.0, 0.0
    sim = _simular(cfg)
    e = compute_annual_pump_energy(cfg, sim)
    horas = sim.annual_pluvial_consumed_m3 * 1000.0 / 10.0 / 60.0
    assert e.pump_hours_year == pytest.approx(horas)
    assert e.annual_kwh == pytest.approx(0.37 / 0.605 * horas)


def test_o_menor_modelo_que_atende():
    from netuno.core.pressurizer_catalog import menor_que_atende
    assert menor_que_atende(18.0).chave == "komeco_tp820t"
    assert menor_que_atende(24.0).chave == "komeco_tp825t"
    assert menor_que_atende(50.0) is None


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
