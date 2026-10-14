"""
Suíte de testes de verificação e auditoria da regra operacional do balanço hídrico.

A regra padrão (phi_rule=None) é a do Triton, a que o manual da 1.0.0 documenta: o
extravasamento sai antes do consumo e a chuva do dia já atende o consumo do dia. Um phi
numérico seleciona a família de Fewkes (2000b) para reservatório único: 0 é a YAS estrita
e 1 é a YBS.

Verifica:
1. Validação física dos limites de phi (0.0 <= phi <= 1.0) e recusa com reservatório superior.
2. Conservação estrita de massa para a regra do Triton e para phi = 0, 0.25, 0.5, 0.75 e 1.
3. Hierarquia teórica do rendimento: YAS estrita <= Triton <= YBS.
4. Equivalência numérica entre kernel Numba JIT e pure Python.
5. Propagação da regra no resultado da simulação pontual e da varredura.
6. O padrão da configuração, do motor e do arquivo de projeto é o mesmo (paridade interface e CLI).
"""

import numpy as np
import pytest
from triton.core.simulation import (
    run_single_simulation,
    run_sweep_simulation,
    validar_parametros_fisicos,
    nome_regra_operacional,
    SingleTankSimulationResult,
    SweepSimulationResult,
)


def test_validar_parametros_fisicos_phi():
    """Garante que phi fora do intervalo [0.0, 1.0] levanta ValueError."""
    # Valores válidos não devem levantar exceção
    validar_parametros_fisicos(
        lower_tank_vol=5000.0,
        area=150.0,
        runoff_coeff=0.85,
        discard_mm=2.0,
        total_demand_per_day=300.0,
        rainwater_share=0.5,
        phi_rule=0.0,
    )
    validar_parametros_fisicos(
        lower_tank_vol=5000.0,
        area=150.0,
        runoff_coeff=0.85,
        discard_mm=2.0,
        total_demand_per_day=300.0,
        rainwater_share=0.5,
        phi_rule=0.5,
    )
    validar_parametros_fisicos(
        lower_tank_vol=5000.0,
        area=150.0,
        runoff_coeff=0.85,
        discard_mm=2.0,
        total_demand_per_day=300.0,
        rainwater_share=0.5,
        phi_rule=1.0,
    )

    # Valores inválidos devem levantar ValueError
    with pytest.raises(ValueError, match="operacional phi"):
        validar_parametros_fisicos(
            lower_tank_vol=5000.0,
            area=150.0,
            runoff_coeff=0.85,
            discard_mm=2.0,
            total_demand_per_day=300.0,
            rainwater_share=0.5,
            phi_rule=-0.1,
        )

    with pytest.raises(ValueError, match="operacional phi"):
        validar_parametros_fisicos(
            lower_tank_vol=5000.0,
            area=150.0,
            runoff_coeff=0.85,
            discard_mm=2.0,
            total_demand_per_day=300.0,
            rainwater_share=0.5,
            phi_rule=1.05,
        )


def test_nome_regra_operacional():
    """Testa identificação amigável da regra operacional."""
    assert "Triton" in nome_regra_operacional(None)
    assert "YAS" in nome_regra_operacional(0.0)
    assert "YBS" in nome_regra_operacional(1.0)
    assert "0.35" in nome_regra_operacional(0.35)
    # 0,5 é uma regra de Fewkes como outra qualquer; a do Triton é outra (phi=None)
    assert "Triton" not in nome_regra_operacional(0.5)


@pytest.mark.parametrize("phi", [None, 0.0, 0.25, 0.5, 0.75, 1.0])
def test_conservacao_estrita_massa_com_phi(phi):
    """
    Verifica balanço de massa no modo detalhado dia a dia:
    Para cada dia: V_{t} = V_{t-1} + Q_t - Y_t - O_t
    Total do período: V_{fim} - V_0 = sum(Q) - sum(Y) - sum(O)
    """
    np.random.seed(42)
    # Série sintética com eventos pluviométricos variados
    precip = np.zeros(100)
    chuva_dias = [3, 4, 10, 15, 16, 25, 30, 45, 50, 60, 75, 80, 85, 90]
    for d in chuva_dias:
        precip[d] = 25.0

    lower_vol = 3000.0
    area = 120.0
    runoff = 0.85
    demand = 400.0
    share = 0.5  # Demanda pluvial = 200 L/dia

    res = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        discard_mm=2.0,
        discard_mode=1,
        total_demand_per_day=demand,
        rainwater_share=share,
        store_daily_details=True,
        phi_rule=phi,
    )

    assert res.phi_rule == (phi if phi is None else pytest.approx(phi))
    assert len(res.daily_results) == 100

    v_prev = 0.0
    for day in res.daily_results:
        # Balanço do dia: V_t = V_{t-1} + Q_t - Y_t - O_t
        q_t = day.harvested_liters
        y_t = day.pluvial_consumed_liters
        o_t = day.spilled_liters
        v_curr = day.lower_tank_end_liters
        
        delta_v = v_curr - v_prev
        residuo = delta_v + y_t + o_t - q_t
        assert abs(residuo) < 1e-6, f"Desbalanço hídrico no dia {day.day_index}: {residuo}"
        v_prev = v_curr


def test_hierarquia_de_rendimento_fewkes():
    """
    Teorema de Fewkes (2000b) / Latham (1983):
    Como YBS permite o consumo antes do extravasamento, seu rendimento é o limitante
    superior teórico, enquanto YAS é o limitante inferior conservador:
    Yield(YBS, phi=1.0) >= Yield(Triton, phi=None) >= Yield(YAS estrita, phi=0.0)
    """
    np.random.seed(123)
    precip = np.random.exponential(scale=5.0, size=365)
    lower_vol = 2000.0
    area = 150.0
    runoff = 0.8
    demand = 500.0
    share = 0.4

    res_yas = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        total_demand_per_day=demand,
        rainwater_share=share,
        phi_rule=0.0,
    )

    res_triton = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        total_demand_per_day=demand,
        rainwater_share=share,
    )

    res_ybs = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        total_demand_per_day=demand,
        rainwater_share=share,
        phi_rule=1.0,
    )

    # Economia potencial de água potável
    pot_yas = res_yas.potential_potable_savings_pct
    pot_triton = res_triton.potential_potable_savings_pct
    pot_ybs = res_ybs.potential_potable_savings_pct

    assert pot_ybs >= pot_triton - 1e-6, f"Esperado pot_ybs >= pot_triton, obtido {pot_ybs} < {pot_triton}"
    assert pot_triton >= pot_yas - 1e-6, f"Esperado pot_triton >= pot_yas, obtido {pot_triton} < {pot_yas}"


def test_sweep_simulation_com_phi():
    """Verifica se run_sweep_simulation propaga phi_rule para os resultados."""
    np.random.seed(99)
    precip = np.random.exponential(scale=6.0, size=200)

    sweep = run_sweep_simulation(
        precip_data=precip,
        lower_tank_max=5000.0,
        lower_tank_step=1000.0,
        area=150.0,
        runoff_coeff=0.8,
        total_demand_per_day=400.0,
        rainwater_share=0.5,
        phi_rule=0.5,
    )

    assert sweep.phi_rule == 0.5
    assert "Fewkes" in sweep.operation_rule_name
    assert len(sweep.results_by_volume) > 0

    for r in sweep.results_by_volume:
        assert r.phi_rule == 0.5
        assert "Fewkes" in r.operation_rule_name


@pytest.mark.parametrize("phi", [None, 0.0, 0.3, 0.5, 0.8, 1.0])
def test_equivalencia_numba_pure_python_com_phi(phi):
    """
    Garante equivalência numérica estrita entre o kernel Numba (store_daily_details=False)
    e o loop de alta resolução Pure Python (store_daily_details=True).
    """
    np.random.seed(777)
    precip = np.random.exponential(scale=7.0, size=365)
    lower_vol = 3000.0
    area = 180.0
    runoff = 0.85
    demand = 450.0
    share = 0.45

    res_fast = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        total_demand_per_day=demand,
        rainwater_share=share,
        store_daily_details=False,
        phi_rule=phi,
    )

    res_detailed = run_single_simulation(
        precip_data=precip,
        lower_tank_vol=lower_vol,
        area=area,
        runoff_coeff=runoff,
        total_demand_per_day=demand,
        rainwater_share=share,
        store_daily_details=True,
        phi_rule=phi,
    )

    assert res_fast.potential_potable_savings_pct == pytest.approx(res_detailed.potential_potable_savings_pct, abs=1e-5)
    assert res_fast.avg_pluvial_consumed_l_day == pytest.approx(res_detailed.avg_pluvial_consumed_l_day, abs=1e-5)
    assert res_fast.avg_potable_consumed_l_day == pytest.approx(res_detailed.avg_potable_consumed_l_day, abs=1e-5)
    assert res_fast.avg_spilled_l_day == pytest.approx(res_detailed.avg_spilled_l_day, abs=1e-5)


def _serie():
    rng = np.random.default_rng(1)
    return np.where(rng.random(1825) < 0.3, rng.gamma(0.8, 12.0, 1825), 0.0)


def test_padrao_do_motor_e_a_regra_do_triton_e_nao_a_yas():
    """O padrão preserva os números publicados: a regra do Triton difere da YAS estrita."""
    kw = dict(precip_data=_serie(), lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
              total_demand_per_day=400.0, rainwater_share=0.5)
    padrao = run_single_simulation(**kw)
    assert padrao.phi_rule is None
    assert "Triton" in padrao.operation_rule_name
    yas = run_single_simulation(**kw, phi_rule=0.0)
    assert padrao.annual_pluvial_consumed_m3 > yas.annual_pluvial_consumed_m3 + 1e-6
    # nenhum phi reproduz a regra do Triton: ela não é um ponto da família de Fewkes
    for phi in (0.25, 0.5, 0.75):
        outra = run_single_simulation(**kw, phi_rule=phi)
        assert outra.annual_pluvial_consumed_m3 != pytest.approx(padrao.annual_pluvial_consumed_m3, abs=1e-6)


def test_tanque_zero_nao_tem_economia_na_regra_do_triton():
    kw = dict(precip_data=_serie(), lower_tank_vol=0.0, area=120.0, runoff_coeff=0.85,
              total_demand_per_day=400.0, rainwater_share=0.5)
    assert run_single_simulation(**kw).annual_pluvial_consumed_m3 == pytest.approx(0.0, abs=1e-9)


def test_phi_explicito_com_reservatorio_superior_e_recusado():
    kw = dict(precip_data=_serie(), lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
              total_demand_per_day=400.0, rainwater_share=0.5,
              upper_tank_used=True, upper_tank_vol=500.0, pumping_threshold=375.0)
    with pytest.raises(ValueError, match="reservatório único"):
        run_single_simulation(**kw, phi_rule=0.5)
    # sem phi, o reservatório duplo roda pela regra do Triton
    assert run_single_simulation(**kw).phi_rule is None


def test_padrao_da_configuracao_e_do_arquivo_de_projeto_e_o_mesmo_do_motor():
    """Interface e linha de comando partem do mesmo padrão: sem phi, regra do Triton."""
    from triton.core.parser import TritonConfig
    assert TritonConfig().phi_operation_rule is None


def test_phi_do_projeto_chega_ao_motor_pelo_building_config():
    """O φ gravado no projeto vale sem ser repassado à mão (paridade interface, arquivo e CLI)."""
    kw = dict(precip_data=_serie(), lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
              total_demand_per_day=400.0, rainwater_share=0.5)
    base = {"area": 120.0}
    via_arg = run_single_simulation(**kw, building_config=base, phi_rule=0.0)
    via_cfg = run_single_simulation(**kw, building_config={**base, "phi_operation_rule": 0.0})
    assert via_cfg.phi_rule == 0.0
    assert via_cfg.annual_pluvial_consumed_m3 == pytest.approx(via_arg.annual_pluvial_consumed_m3)
    sweep = run_sweep_simulation(precip_data=_serie(), lower_tank_max=4000.0, lower_tank_step=1000.0,
                                 area=120.0, runoff_coeff=0.85, total_demand_per_day=400.0,
                                 rainwater_share=0.5, building_config={"phi_operation_rule": 1.0})
    assert sweep.phi_rule == 1.0


def test_phi_do_projeto_com_reservatorio_superior_cai_na_regra_do_triton_com_aviso():
    kw = dict(precip_data=_serie(), lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
              total_demand_per_day=400.0, rainwater_share=0.5,
              upper_tank_used=True, upper_tank_vol=500.0, pumping_threshold=375.0)
    with pytest.warns(UserWarning, match="reservatório superior"):
        r = run_single_simulation(**kw, building_config={"phi_operation_rule": 0.5})
    assert r.phi_rule is None


def test_regra_efetiva_do_projeto():
    from triton.core.parser import TritonConfig, regra_operacional_efetiva
    cfg = TritonConfig()
    assert regra_operacional_efetiva(cfg) is None
    cfg.phi_operation_rule = 0.0
    cfg.upper_tank_used = 0
    assert regra_operacional_efetiva(cfg) == 0.0
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = 500.0
    assert regra_operacional_efetiva(cfg) is None


def test_cli_aplica_o_phi_do_projeto_e_o_set(tmp_path):
    from triton.cli import _apply_overrides, _parametros_de_simulacao
    from triton.core.parser import TritonConfig
    cfg = TritonConfig()
    cfg.upper_tank_used = 0     # φ explícito só vale para reservatório único
    assert _parametros_de_simulacao(cfg)["phi_rule"] is None
    _apply_overrides(cfg, ["phi_operation_rule=0"])
    assert cfg.phi_operation_rule == 0.0
    assert _parametros_de_simulacao(cfg)["phi_rule"] == 0.0
    _apply_overrides(cfg, ["phi_operation_rule=triton"])
    assert cfg.phi_operation_rule is None
    with pytest.raises(ValueError):
        _apply_overrides(cfg, ["phi_operation_rule=1,5"])


def test_demanda_zero_no_mes_e_no_dia_da_semana_e_valida():
    """Férias: um mês (ou dia da semana) com demanda 0 não vira a demanda padrão."""
    p = np.zeros(365)
    kw = dict(precip_data=p, lower_tank_vol=3000.0, area=100.0, runoff_coeff=0.8, discard_mm=1.0,
              total_demand_per_day=200.0, rainwater_share=1.0, store_daily_details=True)
    mensal = run_single_simulation(**kw, demand_mode="monthly", monthly_demands=[0.0] + [200.0] * 11,
                                   monthly_residents=[1] * 12, monthly_shares=[1.0] * 12)
    janeiro = sum(d.total_demand_liters for d in mensal.daily_results[:31])
    assert janeiro == pytest.approx(0.0)
    fevereiro = sum(d.total_demand_liters for d in mensal.daily_results[31:59])
    assert fevereiro == pytest.approx(200.0 * 28)
    semanal = run_single_simulation(**kw, demand_mode="weekly", weekly_demands=[200.0] * 5 + [0.0, 0.0],
                                    weekly_residents=[1] * 7, weekly_shares=[1.0] * 7)
    dias_sem_demanda = sum(1 for d in semanal.daily_results if d.total_demand_liters == 0.0)
    assert 100 <= dias_sem_demanda <= 106   # 52 fins de semana: ~104 dias

