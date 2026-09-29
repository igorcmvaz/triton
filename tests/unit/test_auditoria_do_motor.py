# -*- coding: utf-8 -*-
"""Casos da auditoria do motor de balanço hídrico.

Cada teste nasce de uma sonda que mostrou o motor aceitando uma entrada sem
sentido físico, ou dois caminhos do programa discordando sobre o mesmo projeto.
Os de conservação de massa e de casos-limite fixam o que a auditoria confirmou
estar correto, para que continue assim.
"""

import math
import os
import tempfile

import numpy as np
import pytest

from netuno.core.parser import load_precipitation
from netuno.core.simulation import (
    run_single_simulation,
    run_sweep_simulation,
    validar_serie_precipitacao,
)

BASE = dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
            total_demand_per_day=600.0, rainwater_share=0.40)


def _serie_sintetica(dias=3650, semente=7):
    """Chuva diária com cerca de metade dos dias secos e cauda longa."""
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=12.0, size=dias)
    chuva[rng.random(dias) < 0.55] = 0.0
    return chuva


def _arquivo(conteudo):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                    encoding="utf-8")
    f.write(conteudo)
    f.close()
    return f.name


# ══════════════════════════════════════════════════════════════════════════════
# Conservação de massa e casos-limite: o que está correto e deve continuar
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("volume", [0.0, 1000.0, 5000.0, 50000.0])
def test_massa_fecha_dia_a_dia_e_no_periodo(volume):
    """V(t-1) + captado = extravasado + consumido + V(t), em todo dia."""
    chuva = _serie_sintetica()
    r = run_single_simulation(precip_data=chuva, lower_tank_vol=volume,
                              store_daily_details=True, **BASE)
    anterior = 0.0
    entrou = saiu = 0.0
    for d in r.daily_results:
        residuo = (anterior + d.harvested_liters) - (
            d.spilled_liters + d.pluvial_consumed_liters + d.lower_tank_end_liters)
        assert abs(residuo) <= 1e-6, (d.day_index, residuo)
        assert -1e-9 <= d.lower_tank_end_liters <= volume + 1e-9
        entrou += d.harvested_liters
        saiu += d.spilled_liters + d.pluvial_consumed_liters
        anterior = d.lower_tank_end_liters
    assert math.isclose(entrou, saiu + anterior, rel_tol=1e-12, abs_tol=1e-6)


def test_serie_totalmente_seca():
    r = run_single_simulation(precip_data=np.zeros(730), lower_tank_vol=5000.0,
                              **BASE)
    assert r.potential_potable_savings_pct == 0.0
    assert r.pct_days_null_satisfaction == 100.0
    assert r.avg_spilled_l_day == 0.0


def test_evento_extremo_unico_extravasa_so_o_excedente():
    """500 mm num dia sobre 150 m² e C=0,85: capta 63.495 L; cabem 2.000 L."""
    chuva = np.zeros(10)
    chuva[0] = 500.0
    r = run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0,
                              store_daily_details=True, **BASE)
    d0 = r.daily_results[0]
    captado = (500.0 - 2.0) * 150.0 * 0.85
    assert d0.harvested_liters == pytest.approx(captado)
    # YAS: extravasa antes de consumir, e o consumo sai do reservatório cheio.
    assert d0.spilled_liters == pytest.approx(captado - 2000.0)
    assert d0.pluvial_consumed_liters == pytest.approx(240.0)
    assert d0.lower_tank_end_liters == pytest.approx(1760.0)


def test_descarte_consome_o_dia_inteiro_quando_a_chuva_nao_passa_da_lamina():
    """Modo 1: P <= d_f não produz captação nenhuma naquele dia."""
    r = run_single_simulation(precip_data=np.array([1.0, 2.0, 2.5]),
                              lower_tank_vol=5000.0, store_daily_details=True,
                              **BASE)
    assert [d.eff_precip_mm for d in r.daily_results] == pytest.approx([0.0, 0.0, 0.5])


# ══════════════════════════════════════════════════════════════════════════════
# Série de precipitação: falhas, cabeçalhos e sentinelas
# ══════════════════════════════════════════════════════════════════════════════

def test_leitor_pula_cabecalho_em_vez_de_devolver_serie_vazia():
    nome = _arquivo("Data;Precipitacao\n1,2\n3,4\n")
    try:
        assert load_precipitation(nome).tolist() == pytest.approx([1.2, 3.4])
    finally:
        os.unlink(nome)


def test_leitor_preserva_falha_como_nan_e_nao_como_dia_seco():
    nome = _arquivo("0\n5\n\nfalha\n4\n\n\n")
    try:
        serie = load_precipitation(nome)
    finally:
        os.unlink(nome)
    assert len(serie) == 5, "linhas vazias no fim do arquivo não são dias"
    assert np.isnan(serie[2]) and np.isnan(serie[3])
    assert serie[4] == 4.0


def test_leitor_para_no_bloco_de_configuracao_do_netuno4():
    nome = _arquivo("1\n2\nDescarte;2\nÁrea;100\n")
    try:
        assert load_precipitation(nome).tolist() == [1.0, 2.0]
    finally:
        os.unlink(nome)


@pytest.mark.parametrize("detalhe", [False, True])
def test_motor_recusa_falha_de_registro(detalhe):
    chuva = np.array([0.0, 20.0, float("nan"), 5.0])
    with pytest.raises(ValueError, match="dia 3"):
        run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0,
                              store_daily_details=detalhe, **BASE)


@pytest.mark.parametrize("detalhe", [False, True])
def test_motor_recusa_sentinela_negativo(detalhe):
    chuva = np.array([0.0, 20.0, -999.0, 0.0])
    with pytest.raises(ValueError, match="-999"):
        run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0,
                              store_daily_details=detalhe, **BASE)


def test_motor_recusa_serie_vazia_com_mensagem_e_nao_divisao_por_zero():
    with pytest.raises(ValueError, match="vazia"):
        run_single_simulation(precip_data=np.array([]), lower_tank_vol=2000.0,
                              **BASE)


def test_varredura_tambem_valida_a_serie():
    with pytest.raises(ValueError):
        run_sweep_simulation(precip_data=np.array([1.0, float("inf")]),
                             lower_tank_max=1000.0, lower_tank_step=500.0,
                             **BASE)


def test_serie_valida_passa():
    validar_serie_precipitacao([0.0, 0.0, 12.5])


# ══════════════════════════════════════════════════════════════════════════════
# Parâmetros não finitos e modos inválidos
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("campo,valor", [
    ("area", float("nan")),
    ("area", float("inf")),
    ("runoff_coeff", float("nan")),
    ("discard_mm", float("nan")),
    ("total_demand_per_day", float("nan")),
    ("rainwater_share", float("nan")),
])
def test_parametro_nao_finito_e_recusado(campo, valor):
    args = dict(BASE)
    args[campo] = valor
    with pytest.raises(ValueError):
        run_single_simulation(precip_data=_serie_sintetica(365),
                              lower_tank_vol=2000.0, **args)


def test_volume_nao_finito_e_recusado():
    with pytest.raises(ValueError):
        run_single_simulation(precip_data=_serie_sintetica(365),
                              lower_tank_vol=float("nan"), **BASE)


def test_modo_de_descarte_desconhecido_e_recusado():
    args = dict(BASE)
    args["discard_mode"] = 7
    with pytest.raises(ValueError, match="Modo de descarte"):
        run_single_simulation(precip_data=_serie_sintetica(365),
                              lower_tank_vol=2000.0, **args)


def test_modo_3_exige_intervalo_positivo():
    args = dict(BASE)
    args["discard_mode"] = 3
    with pytest.raises(ValueError, match="Intervalo"):
        run_single_simulation(precip_data=_serie_sintetica(365),
                              lower_tank_vol=2000.0, discard_days_interval=0,
                              **args)


# ══════════════════════════════════════════════════════════════════════════════
# Varredura e simulação única dizem o mesmo sobre o mesmo volume
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("reserva", [True, False])
def test_varredura_preserva_irrigacao_e_suprimento_de_reserva(reserva):
    """O volume da varredura e a simulação única do mesmo volume coincidem.

    Com a reserva desligada a varredura comprava da rede a irrigação que a
    simulação única deixava sem atender: 467 contra 445 L/dia de água potável
    no caso da auditoria, com a demanda não atendida zerada e os dias de
    irrigação suprimida também.
    """
    edificacao = dict(demand_mode="constant", demand=150.0, residents=4,
                      share=0.40, non_potable_indoor_share=0.35,
                      irrigation_liters_per_day=80.0,
                      irrigation_rain_threshold_mm=2.0,
                      irrigation_potable_backup=reserva)
    kw = dict(BASE, building_config=edificacao)
    chuva = _serie_sintetica()
    unica = run_single_simulation(precip_data=chuva, lower_tank_vol=2000.0, **kw)
    varredura = run_sweep_simulation(precip_data=chuva, lower_tank_max=2000.0,
                                     lower_tank_step=1000.0, **kw)
    mesmo = [x for x in varredura.results_by_volume
             if x.lower_tank_vol == 2000.0][0]
    for campo in ("potential_potable_savings_pct", "avg_potable_consumed_l_day",
                  "avg_unmet_demand_l_day", "avg_pluvial_irrigation_consumed_l_day",
                  "avg_pluvial_indoor_consumed_l_day",
                  "total_irrigation_days_suppressed"):
        assert getattr(mesmo, campo) == pytest.approx(getattr(unica, campo)), campo
