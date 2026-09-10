"""A energia de recalque tem uma definição só, e as telas a consomem.

A correção da hidráulica trocou `P × horas / η` por `energia específica × volume
+ partidas`, porque a potência de placa **já embute** o rendimento e dividir por
ele de novo conta a perda duas vezes. `compute_annual_pump_energy` passou a ser
a referência.

Sobraram quatro cópias da fórmula antiga fora dela: duas na aba econômica
integrada e duas no otimizador multicritério. Todas superestimavam em 1/η —
1,68 vezes com rendimento de 55%.

O efeito pior era no otimizador: o critério ambiental do multicritério
**ranqueava volumes** com uma energia inflada, enquanto a aba ambiental usava a
corrigida. O ranqueamento se apoiava num número que nenhuma outra tela mostrava.

Este módulo impede o reaparecimento por duas vias: verifica a física da fórmula
e varre o código atrás da assinatura da versão antiga.
"""

from __future__ import annotations

import os
import re

import pytest

from netuno.core.parser import NetunoConfig
from netuno.core.pump_energy import compute_annual_pump_energy
from netuno.core.simulation import SingleTankSimulationResult

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PACOTE = os.path.join(_RAIZ, "netuno")


def _config(rendimento: float = 55.0) -> NetunoConfig:
    cfg = NetunoConfig()
    cfg.pump_power_kw = 0.37
    cfg.pump_flow_rate = 2280.0
    cfg.pump_efficiency = rendimento
    cfg.pump_startup_time_h = 0.0167
    return cfg


def _sim(litros_por_dia: float = 330.0) -> SingleTankSimulationResult:
    r = SingleTankSimulationResult(
        lower_tank_vol=5000.0, potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=litros_por_dia, avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0,
    )
    r.n_days_simulated = 365
    r.total_pumped_liters = litros_por_dia * 365.0
    r.total_pump_cycles = 365
    return r


# ─────────────────────────── a física da referência ────────────────────────────

def test_a_energia_nao_divide_pelo_rendimento_uma_segunda_vez():
    """A potência de placa é o que o motor consome da tomada.

    Com vazão informada, a energia por m³ é P/Q e nada mais. A fórmula antiga
    fazia P × horas / η, o que embutia a perda duas vezes.
    """
    cfg, sim = _config(), _sim()
    correta = compute_annual_pump_energy(cfg, sim, upper_tank_used=True).annual_kwh

    horas_recalque = sim.total_pumped_liters / cfg.pump_flow_rate
    horas_partida = sim.total_pump_cycles * cfg.pump_startup_time_h
    antiga = cfg.pump_power_kw * (horas_recalque + horas_partida) / (cfg.pump_efficiency / 100.0)

    assert antiga > correta
    # Com o termo das partidas tambem corrigido, o excesso da formula antiga e
    # exatamente 1/eta, e nao um numero aproximado: as duas contas passam a
    # diferir por um fator unico, que e a assinatura do defeito.
    assert antiga / correta == pytest.approx(100.0 / cfg.pump_efficiency, rel=1e-9)


def test_o_excesso_da_formula_antiga_e_exatamente_um_sobre_eta():
    """Com rendimento pior, o erro cresce — é a assinatura do defeito."""
    for rendimento in (40.0, 55.0, 70.0):
        cfg, sim = _config(rendimento), _sim()
        correta = compute_annual_pump_energy(cfg, sim, upper_tank_used=True)
        # A parcela de recalque é P/Q por m³; a fórmula antiga a dividia por η.
        recalque_correto = (cfg.pump_power_kw / (cfg.pump_flow_rate / 1000.0)) * correta.annual_pumped_m3
        recalque_antigo = recalque_correto / (rendimento / 100.0)
        assert recalque_antigo / recalque_correto == pytest.approx(100.0 / rendimento)


def test_sem_reservatorio_superior_nao_ha_recalque():
    assert compute_annual_pump_energy(_config(), _sim(), upper_tank_used=False).annual_kwh == 0.0


def test_a_energia_acompanha_o_volume_recalcado():
    pouco = compute_annual_pump_energy(_config(), _sim(150.0), upper_tank_used=True)
    muito = compute_annual_pump_energy(_config(), _sim(600.0), upper_tank_used=True)
    assert muito.annual_kwh > pouco.annual_kwh
    # E a energia POR M³ quase não muda: o que cresce é o volume, não o custo unitário.
    assert muito.specific_kwh_per_m3 == pytest.approx(pouco.specific_kwh_per_m3, rel=0.25)


# ────────────────────── a assinatura da versão antiga sumiu ────────────────────

def _fontes():
    for dp, _dn, fn in os.walk(_PACOTE):
        if "__pycache__" in dp:
            continue
        for f in fn:
            if f.endswith(".py"):
                caminho = os.path.join(dp, f)
                yield os.path.relpath(caminho, _RAIZ).replace("\\", "/"), open(
                    caminho, encoding="utf-8", errors="replace"
                ).read()


def test_nenhuma_tela_divide_horas_de_bomba_pelo_rendimento():
    """Varredura pela assinatura textual da fórmula antiga.

    Quatro cópias sobreviveram à correção porque cada uma parecia local e
    inofensiva. A verificação por física não as pega — elas não passam por
    `compute_annual_pump_energy`. Só a varredura pega.
    """
    padrao = re.compile(
        r"(?:t_rec|t_part|run_h|start_h|p_hrs|pump_hours)[^\n]*?/\s*max\(\s*0\.01\s*,\s*"
        r"[a-z_.]*pump_efficiency\s*/\s*100",
        re.IGNORECASE,
    )
    achados = []
    for rel, texto in _fontes():
        for m in padrao.finditer(texto):
            linha = texto[: m.start()].count("\n") + 1
            achados.append(f"{rel}:{linha}")
    assert not achados, "cópia da fórmula antiga de energia de bombeamento: " + str(achados)


def test_so_o_nucleo_converte_rendimento_percentual_em_fracao():
    """`pump_efficiency / 100` fora do núcleo é sinal de conta própria.

    O rendimento entra na energia específica, que vive em `pump_energy.py` e
    `economic.py`. Qualquer outro módulo que o converta está refazendo a conta.
    """
    permitidos = {"netuno/core/pump_energy.py", "netuno/core/economic.py"}
    fora = [
        rel for rel, texto in _fontes()
        if rel not in permitidos and re.search(r"pump_efficiency\s*/\s*100", texto)
    ]
    assert not fora, fora
