"""O balanço de demanda fecha, e o suprimento de reserva da irrigação vale.

`irrigation_potable_backup` decide se a rede pública rega o jardim nos dias em que
a cisterna não dá conta. Desligado, o jardim não é regado e a edificação **não
compra** essa água.

O laço diário já respeitava a regra e acumulava o potável dia a dia. Mas o resumo
descartava o acumulador e recalculava por diferença:

    avg_potable = (demanda_total − pluvial_consumido) / n_dias

que atribui ao potável **toda** a demanda não atendida pela chuva, inclusive a
irrigação que a regra manda não fazer. Medido antes da correção: desligar a
reserva não mexia um litro no resumo, enquanto a série diária do mesmo objeto
mostrava 10,85 L/dia a menos. O módulo econômico consome o resumo, e portanto
subestimava a economia. Os núcleos compilados nem recebiam a bandeira.

Com a reserva **ligada**, que é o padrão, as duas formulas coincidem exatamente:
a correção só tem efeito no caso que era inerte.

O terceiro teste é o que dá nome ao arquivo: a demanda total tem de ser a soma de
três parcelas, e não de duas. Sem a parcela não atendida, o balanço só fechava
por construção, escondendo a água que ninguém forneceu.
"""

from __future__ import annotations

import numpy as np
import pytest

from netuno.core import simulation as S
from netuno.core.simulation import run_single_simulation

_CFG = {
    "demand": 150.0, "residents": 4, "share": 0.4,
    "non_potable_indoor_share": 0.35,
    "irrigation_liters_per_day": 120.0,
    "irrigation_rain_threshold_mm": 2.0,
}


@pytest.fixture(scope="module")
def chuva():
    rng = np.random.default_rng(19)
    return np.clip(rng.gamma(0.55, 8.0, 1826), 0, None)


def _rodar(chuva, backup=True, detalhe=False, duplo=False):
    kw = dict(
        precip_data=chuva, lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
        discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4,
        building_config=dict(_CFG, irrigation_potable_backup=backup),
        store_daily_details=detalhe,
    )
    if duplo:
        kw.update(upper_tank_vol=800.0, upper_tank_used=True, pumping_threshold=80.0)
    return run_single_simulation(**kw)


# ─────────────────────── a bandeira move o resultado ──────────────────────────

def test_desligar_a_reserva_reduz_o_potavel(chuva):
    """Era o defeito: a escolha não mexia um litro no resumo."""
    com = _rodar(chuva, backup=True)
    sem = _rodar(chuva, backup=False)
    assert sem.avg_potable_consumed_l_day < com.avg_potable_consumed_l_day


def test_o_resumo_concorda_com_a_serie_diaria(chuva):
    """Dois números do mesmo objeto não podem se contradizer."""
    for backup in (True, False):
        r = _rodar(chuva, backup=backup, detalhe=True)
        serie = sum(d.potable_consumed_liters for d in r.daily_results) / len(r.daily_results)
        assert r.avg_potable_consumed_l_day == pytest.approx(serie, rel=1e-9)


def test_com_a_reserva_ligada_nada_muda(chuva):
    """O padrão do programa: as duas fórmulas coincidem exatamente."""
    r = _rodar(chuva, backup=True, detalhe=True)
    por_diferenca = sum(
        d.total_demand_liters - d.pluvial_consumed_liters for d in r.daily_results
    ) / len(r.daily_results)
    assert r.avg_potable_consumed_l_day == pytest.approx(por_diferenca, rel=1e-9)
    assert r.avg_unmet_demand_l_day == pytest.approx(0.0)


# ──────────────────────────── o balanço fecha ─────────────────────────────────

@pytest.mark.parametrize("backup", [True, False])
@pytest.mark.parametrize("duplo", [False, True])
def test_a_demanda_e_a_soma_de_tres_parcelas(chuva, backup, duplo):
    """demanda total = pluvial + potável + não atendida."""
    r = _rodar(chuva, backup=backup, detalhe=True, duplo=duplo)
    demanda = sum(d.total_demand_liters for d in r.daily_results) / len(r.daily_results)
    soma = (r.avg_pluvial_consumed_l_day
            + r.avg_potable_consumed_l_day
            + r.avg_unmet_demand_l_day)
    assert soma == pytest.approx(demanda, rel=1e-9)


def test_a_nao_atendida_so_aparece_sem_reserva(chuva):
    assert _rodar(chuva, backup=True).avg_unmet_demand_l_day == pytest.approx(0.0)
    assert _rodar(chuva, backup=False).avg_unmet_demand_l_day > 0.0


def test_sem_irrigacao_nao_ha_demanda_nao_atendida(chuva):
    """Sem jardim cadastrado, a bandeira não tem sobre o que agir."""
    r = run_single_simulation(
        precip_data=chuva, lower_tank_vol=3000.0, area=120.0, runoff_coeff=0.85,
        discard_mm=2.0, total_demand_per_day=600.0, rainwater_share=0.4,
        building_config={"demand": 150.0, "residents": 4, "share": 0.4,
                         "irrigation_potable_backup": False},
    )
    assert r.avg_unmet_demand_l_day == pytest.approx(0.0)


# ─────────────────── os dois motores devolvem o mesmo número ──────────────────

@pytest.mark.skipif(not S.HAS_NUMBA, reason="núcleo compilado não instalado")
@pytest.mark.parametrize("backup", [True, False])
@pytest.mark.parametrize("duplo", [False, True])
def test_o_nucleo_compilado_concorda_com_o_python(chuva, backup, duplo):
    """O kernel não recebia a bandeira: com ele ativo, a escolha era ignorada."""
    kernel = _rodar(chuva, backup=backup, detalhe=False, duplo=duplo)
    puro = _rodar(chuva, backup=backup, detalhe=True, duplo=duplo)
    assert kernel.avg_potable_consumed_l_day == pytest.approx(
        puro.avg_potable_consumed_l_day, rel=1e-9)
    assert kernel.avg_unmet_demand_l_day == pytest.approx(
        puro.avg_unmet_demand_l_day, rel=1e-9)
    assert kernel.avg_pluvial_consumed_l_day == pytest.approx(
        puro.avg_pluvial_consumed_l_day, rel=1e-9)


# ──────────────── o balanço de massa do reservatório também fecha ─────────────

def test_o_reservatorio_nao_cria_nem_perde_agua(chuva):
    """captado = extravasado + consumido + armazenado no fim."""
    r = _rodar(chuva, detalhe=True)
    captado = sum(d.harvested_liters for d in r.daily_results)
    extravasado = sum(d.spilled_liters for d in r.daily_results)
    consumido = sum(d.pluvial_consumed_liters for d in r.daily_results)
    final = r.daily_results[-1].lower_tank_end_liters
    assert captado == pytest.approx(extravasado + consumido + final, rel=1e-9)
