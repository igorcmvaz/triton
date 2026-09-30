# -*- coding: utf-8 -*-
"""As três frações da demanda atendível: interna, externa e total.

A fração interna e a demanda externa são dados; a total é derivada delas. Estes
testes fixam a regra em cada ponta por onde uma fração entra no programa: a
leitura de um arquivo, a alteração pela linha de comando e o motor de cálculo.
Ver netuno/core/fracao_atendivel.py.
"""
import json
from pathlib import Path

import numpy as np
import pytest

from netuno.core.fracao_atendivel import (
    conciliar_fracoes, fracao_interna_da_total, fracao_total)
from netuno.core.parser import NetunoConfig, load_netuno_project
from netuno.core.simulation import build_detailed_daily_demand_vectors

RAIZ = Path(__file__).resolve().parents[2]
CASO = RAIZ / "manual" / "casos" / "02_tutorial_varredura.netuno"


def test_total_derivada_da_interna_e_da_externa():
    # 600 L/dia internos a 30% e 150 L/dia externos: (180 + 150) / 750 = 44%
    assert fracao_total(600.0, 0.30, 150.0) == pytest.approx(0.44)
    assert fracao_total(600.0, 0.30, 0.0) == pytest.approx(0.30)
    assert fracao_interna_da_total(600.0, 0.44, 150.0) == pytest.approx(0.30)


def test_total_impossivel_e_recusada():
    # a externa sozinha já é 20% da demanda; 10% de total não tem interna possível
    with pytest.raises(ValueError, match="impossível"):
        fracao_interna_da_total(600.0, 0.10, 150.0)


def _arquivo(tmp_path, interna, externa, jardim=0.0):
    d = json.loads(CASO.read_text(encoding="utf-8"))
    i = d["inputs"]
    i["incentives_and_shares"]["non_potable_indoor_share"] = interna
    i["incentives_and_shares"]["potable_indoor_share"] = 1 - interna
    i["irrigation"]["liters_per_day"] = externa
    i["irrigation"]["garden_area_m2"] = jardim
    p = tmp_path / "caso.netuno"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


def test_arquivo_antigo_com_padroes_vazados_vale_a_total(tmp_path):
    """Até a 5.0.0 a interna e a externa eram gravadas com os padrões."""
    r = load_netuno_project(str(_arquivo(tmp_path, 0.35, 50.0)))
    c = r["config"]
    assert (c.rainwater_share, c.non_potable_indoor_share, c.irrigation_liters_per_day) == (0.28, 0.28, 0.0)
    assert r["aviso_fracoes"] and "vale a total" in r["aviso_fracoes"]


def test_arquivo_coerente_com_demanda_externa_e_preservado(tmp_path):
    # 600 L/dia internos a 20% e 100 L/dia de rega: total (120 + 100) / 700
    d = json.loads(CASO.read_text(encoding="utf-8"))
    total = (0.20 * 600 + 100) / 700
    d["inputs"]["building_and_demand"]["rainwater_share"] = total
    p = _arquivo(tmp_path, 0.20, 100.0, jardim=30.0)
    d2 = json.loads(p.read_text(encoding="utf-8"))
    d2["inputs"]["building_and_demand"]["rainwater_share"] = total
    p.write_text(json.dumps(d2), encoding="utf-8")
    r = load_netuno_project(str(p))
    c = r["config"]
    assert c.non_potable_indoor_share == pytest.approx(0.20)
    assert c.irrigation_liters_per_day == pytest.approx(100.0)
    assert r["aviso_fracoes"] is None


def test_alterar_a_total_recalcula_a_interna():
    c = load_netuno_project(str(CASO))["config"]
    c.rainwater_share = 0.40                      # como faz --set rainwater_share=0.40
    conciliar_fracoes(c)
    assert c.non_potable_indoor_share == pytest.approx(0.40)


def test_alterar_a_interna_recalcula_a_total():
    c = load_netuno_project(str(CASO))["config"]
    c.non_potable_indoor_share = 0.20
    c.irrigation_liters_per_day = 150.0           # 600 L/dia internos
    conciliar_fracoes(c)
    assert c.rainwater_share == pytest.approx((0.20 * 600 + 150) / 750)


def test_alterar_as_duas_em_desacordo_e_erro():
    c = load_netuno_project(str(CASO))["config"]
    c.rainwater_share, c.non_potable_indoor_share = 0.50, 0.20
    with pytest.raises(ValueError, match="Altere só uma"):
        conciliar_fracoes(c)


def test_config_montada_no_codigo_vale_a_total():
    c = NetunoConfig(rainwater_share=0.55)
    conciliar_fracoes(c)
    assert c.non_potable_indoor_share == pytest.approx(0.55)
    assert c.potable_indoor_share == pytest.approx(0.45)


@pytest.mark.parametrize("modo", ["constant", "weekly", "monthly"])
def test_motor_aplica_a_interna_a_demanda_interna_em_todos_os_modos(modo):
    """A total inclui a externa; aplicada ao consumo interno, contaria a externa duas vezes."""
    n = 60
    b = {"demand": 150.0, "residents": 4, "share": 0.44, "non_potable_indoor_share": 0.30,
         "irrigation_liters_per_day": 150.0, "irrigation_rain_threshold_mm": 2.0,
         "demand_mode": modo}
    if modo == "weekly":
        b.update(weekly_demands=[150.0] * 7, weekly_residents=[4] * 7, weekly_shares=None)
    if modo == "monthly":
        b.update(monthly_demands=[150.0] * 12, monthly_residents=[4] * 12, monthly_shares=None)
    tot, pluv, pot_in, non_pot_in, irr, _ = build_detailed_daily_demand_vectors(
        n_days=n, building_config=b, precip_data=np.zeros(n))
    assert np.allclose(non_pot_in, 600.0 * 0.30)
    assert np.allclose(irr, 150.0)
    assert np.allclose(pluv / tot, 0.44)


def test_projetos_distribuidos_sao_coerentes():
    """Nenhum projeto que acompanha o programa precisa de conciliação ao abrir."""
    arquivos = sorted((RAIZ / "manual" / "casos").glob("*.netuno")) + sorted((RAIZ / "examples").glob("estudo_caso_*.netuno"))
    assert arquivos
    for arq in arquivos:
        assert load_netuno_project(str(arq))["aviso_fracoes"] is None, arq.name
