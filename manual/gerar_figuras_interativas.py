# -*- coding: utf-8 -*-
"""Os dados das figuras interativas do site de documentação.

Cada figura interativa é a mesma figura do manual, com os parâmetros que o
leitor quer mexer. Nada é calculado no navegador: o simulador roda aqui, numa
grade de valores, e a página só escolhe a célula. Por isso o site mostra os
mesmos números do programa e do PDF, e uma correção no motor chega às duas
coisas na mesma montagem.

As chaves do dicionário são os nomes dos arquivos das figuras estáticas, e é
por eles que o site encontra onde pôr cada uma.

Uso: chamado por gerar_site.py.
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
for p in (str(RAIZ), str(AQUI)):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402

from gerar_tabelas import (  # noqa: E402
    CHUVA_23, CIDADES_GUIA14, NOMES_CIDADES, TARIFA_CASAN, TUTORIAL,
    _config_ambiental, _config_economica, _config_projeto, _config_tutorial, _serie,
)
from netuno.core.parser import load_precipitation  # noqa: E402
from netuno.core.simulation import run_single_simulation  # noqa: E402

INICIO = datetime(1980, 1, 1)     # o mesmo calendário das figuras do manual
DIAS_MES = 30.4375
MATERIAIS = [("CONCRETO", "Concreto armado"), ("PEAD", "Polietileno (PEAD)"),
             ("FIBRA", "Fibra de vidro (PRFV)"), ("ACO_INOX", "Aço inoxidável")]


def _r(x, casas=0):
    return round(float(x), casas) if casas else int(round(float(x)))


# ── o balanço de dez dias ─────────────────────────────────────────────────────

def dez_dias():
    """Os dez dias do exemplo, com a capacidade e a lâmina de descarte variando."""
    capacidades = [1000, 1500, 2000, 2500, 3000]
    descartes = [0.0, 1.0, 2.0, 3.0]
    casos = {}
    for c in capacidades:
        for d in descartes:
            r = run_single_simulation(
                precip_data=np.array(CHUVA_23, dtype=float), lower_tank_vol=float(c),
                area=100.0, runoff_coeff=0.85, discard_mm=d, discard_mode=1,
                total_demand_per_day=200.0, rainwater_share=0.40,
                store_daily_details=True)
            casos[f"{c}|{d:g}"] = [
                [_r(x.eff_precip_mm, 1), _r(x.harvested_liters), _r(x.pluvial_demand_liters),
                 _r(x.pluvial_consumed_liters), _r(x.potable_consumed_liters),
                 _r(x.spilled_liters), _r(x.lower_tank_end_liters), x.satisfaction_type]
                for x in r.daily_results]
    return {"chuva": CHUVA_23, "capacidades": capacidades, "descartes": descartes,
            "padrao": [2000, 2.0], "area": 100.0, "coef": 0.85, "demanda": 200.0,
            "fracao": 0.40, "casos": casos}


# ── o nível da cisterna, dia a dia ────────────────────────────────────────────

def serie_diaria():
    """O nível ao fim de cada dia, em seis capacidades, nos trinta anos."""
    serie = _serie()
    volumes = [1000, 2000, 4000, 8000, 12000, 20000]
    anos = [(INICIO + timedelta(days=i)).year for i in range(len(serie))]
    primeiro = {}
    for i, a in enumerate(anos):
        primeiro.setdefault(a, i)
    lista_anos = sorted(primeiro)
    niveis, resumo = {}, {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  store_daily_details=True, **_config_tutorial())
        niv = [_r(d.lower_tank_end_liters) for d in r.daily_results]
        niveis[str(v)] = niv
        por_ano = []
        for a in lista_anos:
            dias = [d for i, d in enumerate(r.daily_results) if anos[i] == a]
            demanda = sum(d.pluvial_demand_liters for d in dias)
            usado = sum(d.pluvial_consumed_liters for d in dias)
            por_ano.append([
                _r(sum(d.precip_mm for d in dias)),
                _r(100.0 * usado / demanda, 1) if demanda else 0.0,
                _r(sum(d.spilled_liters for d in dias) / 1000.0, 1),
                sum(1 for d in dias if d.lower_tank_end_liters <= 0.05 * v),
                sum(1 for d in dias if d.satisfaction_type == 2),
                len(dias)])
        resumo[str(v)] = por_ano
    return {"inicio": INICIO.strftime("%Y-%m-%d"), "anos": lista_anos,
            "primeiro_dia": [primeiro[a] for a in lista_anos],
            "chuva": [_r(x, 1) for x in serie], "volumes": volumes,
            "padrao": 4000, "niveis": niveis, "resumo": resumo,
            "demanda_pluvial": _r(TUTORIAL["moradores"] * TUTORIAL["per_capita"]
                                  * TUTORIAL["rainwater_share"])}


# ── a permanência da autonomia ────────────────────────────────────────────────

def permanencia():
    """Curva de permanência da autonomia e renovações, de 500 L a 20.000 L."""
    serie = _serie()
    volumes = list(range(500, 20001, 500))
    pontos = list(range(0, 101, 2))
    curvas, estados = {}, {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                  store_daily_details=True, **_config_tutorial())
        demanda = r.daily_results[0].pluvial_demand_liters
        aut = np.array([d.lower_tank_end_liters / demanda for d in r.daily_results])
        # Permanência p: a autonomia igualada ou superada em p% do tempo.
        curvas[str(v)] = [_r(np.percentile(aut, 100 - p), 2) for p in pontos]
        niveis = np.array([d.lower_tank_end_liters for d in r.daily_results]) / v
        estados[str(v)] = [
            _r(r.avg_pluvial_consumed_l_day * 365.25 / v, 1),       # renovações/ano
            _r(np.mean(niveis <= 0.05) * 100.0, 1),                 # % vazia
            _r(np.mean(niveis >= 0.95) * 100.0, 1),                 # % cheia
            _r(np.median(aut), 1),                                  # autonomia mediana
            _r(r.potential_potable_savings_pct, 2)]
    return {"volumes": volumes, "pontos": pontos, "curvas": curvas,
            "estados": estados, "referencias": [2000, 4000, 10000, 20000],
            "padrao": 4000,
            "demanda_pluvial": _r(TUTORIAL["moradores"] * TUTORIAL["per_capita"]
                                  * TUTORIAL["rainwater_share"])}


# ── a fatura nos três regimes de mínimo ───────────────────────────────────────

def regimes():
    from netuno.core.economic import calculate_water_bill
    # As mesmas três estruturas da figura do manual (gerar_figuras.figura_regimes).
    disponibilidade = [(0.0, 0.0, 46.34, -1), (0.0, 10.0, 3.08, 1),
                       (10.0, 25.0, 14.31, 1), (25.0, 50.0, 19.14, 1),
                       (50.0, 999999.0, 24.08, 1)]
    franquia = [(0.0, 0.0, 52.89, -1), (0.0, 10.0, 0.0, 1),
                (10.0, 15.0, 9.815, 1), (15.0, 20.0, 10.917, 1),
                (20.0, 999999.0, 12.8, 1)]
    sem_minimo = [(0.0, 10.0, 5.29, 1), (10.0, 15.0, 9.815, 1),
                  (15.0, 20.0, 10.917, 1), (20.0, 999999.0, 12.8, 1)]
    consumos = [round(0.25 * i, 2) for i in range(0, 161)]
    curvas = []
    for chave, nome, exemplo, tarifa in [
            ("disp", "Tarifa de disponibilidade", "como na CASAN, em Florianópolis", disponibilidade),
            ("franq", "Franquia no valor mínimo", "como em Floriano (PI)", franquia),
            ("sem", "Sem valor mínimo", "a tarifa de Floriano sem a franquia", sem_minimo)]:
        curvas.append({"chave": chave, "nome": nome, "exemplo": exemplo,
                       "fatura": [_r(calculate_water_bill(c * 1000.0, tarifa, 1, 0.0, 0.0, 0.0), 2)
                                  for c in consumos]})
    r = run_single_simulation(precip_data=_serie(), lower_tank_vol=TUTORIAL["volume"],
                              **_config_projeto())
    antes = (r.avg_pluvial_consumed_l_day + r.avg_potable_consumed_l_day) * DIAS_MES / 1000.0
    depois = r.avg_potable_consumed_l_day * DIAS_MES / 1000.0
    return {"consumos": consumos, "curvas": curvas,
            "padrao": [round(antes * 4) / 4, round(depois * 4) / 4]}


# ── o fluxo de caixa ──────────────────────────────────────────────────────────

def fluxo_de_caixa():
    """Colunas anuais e saldo descontado, por volume e material da cisterna."""
    from netuno.core.economic import run_economic_analysis
    serie = _serie()
    volumes = [2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos = {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        for chave, _ in MATERIAIS:
            e = run_economic_analysis(_config_economica(v, chave), r)
            n = int(np.ceil(len(e.monthly_cash_flows) / 12.0))
            econ, custo, acum = [0.0] * (n + 1), [0.0] * (n + 1), [0.0] * (n + 1)
            custo[0], acum[0] = e.capex_total, -e.capex_total
            for f in e.monthly_cash_flows:
                a = (f.month - 1) // 12 + 1
                econ[a] += f.water_savings + f.iptu_savings
                custo[a] += f.pump_cost + f.om_cost + f.chlorine_cost
                acum[a] = f.cumulative_discounted
            casos[f"{v}|{chave}"] = {
                "economia": [_r(x) for x in econ], "custo": [_r(x) for x in custo],
                "acumulado": [_r(x) for x in acum], "capex": _r(e.capex_total),
                "vpl": _r(e.vpl), "retorno": (_r(e.payback_years, 1) if e.payback_years else None),
                "tir": _r(e.tir_annual_pct, 1) if e.tir_annual_pct == e.tir_annual_pct else None,
                "potencial": _r(r.potential_potable_savings_pct, 2)}
    return {"volumes": volumes, "materiais": MATERIAIS, "padrao": [4000, "CONCRETO"],
            "casos": casos, "tma": 0.5, "anos": 20}


# ── o carbono ao longo da vida útil ───────────────────────────────────────────

def carbono():
    from netuno.core.environmental import calculate_lca
    serie = _serie()
    volumes = [1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 16000, 20000]
    casos = {}
    for v in volumes:
        r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **_config_projeto())
        for chave, _ in MATERIAIS:
            cfg = _config_ambiental(r)
            cfg.lower_material_key = chave
            lca = calculate_lca(float(v), r.annual_pluvial_consumed_m3, cfg)
            ret = lca.environmental_payback_years
            casos[f"{v}|{chave}"] = [_r(lca.total_embodied_co2_kg, 1), _r(lca.net_annual_avoided_co2_kg, 3),
                                     _r(lca.lower_tank_mass_kg), _r(lca.annual_avoided_co2_kg, 1),
                                     _r(ret, 2) if ret and ret == ret and ret != float("inf") else None]
    return {"volumes": volumes, "materiais": MATERIAIS, "padrao": 4000,
            "casos": casos, "anos": 20}


# ── quatro capitais ───────────────────────────────────────────────────────────

def cidades():
    """Regime mensal e curva de potencial das quatro capitais do guia."""
    volumes = list(range(0, 20001, 1000))
    saida = []
    for chave in CIDADES_GUIA14:
        caminho = RAIZ / "data" / "rainfall" / f"{chave}.csv"
        if not caminho.exists():
            continue
        serie = load_precipitation(str(caminho))[: 30 * 365]
        anos = len(serie) / 365.25
        meses = np.zeros(12)
        for i, x in enumerate(serie):
            meses[(INICIO + timedelta(days=i)).month - 1] += float(x)
        pot = [_r(run_single_simulation(precip_data=serie, lower_tank_vol=float(v),
                                        **_config_tutorial()).potential_potable_savings_pct, 2)
               for v in volumes]
        saida.append({"chave": chave, "nome": NOMES_CIDADES.get(chave, chave),
                      "anual": _r(serie.sum() / anos),
                      "mensal": [_r(m / anos) for m in meses],
                      "dias_chuva": _r(np.mean(serie > 0.1) * 100.0, 1),
                      "potencial": pot})
    return {"volumes": volumes, "cidades": saida,
            "fracao": TUTORIAL["rainwater_share"], "padrao": 4000}


def dados():
    etapas = [("fig01_dez_dias.png", dez_dias),
              ("fig48_programa_serie_diaria.png", serie_diaria),
              ("fig47_permanencia.png", permanencia),
              ("fig05_regimes.png", regimes),
              ("fig08_fluxo_de_caixa.png", fluxo_de_caixa),
              ("fig06_carbono_no_tempo.png", carbono),
              ("fig03_cidades.png", cidades)]
    saida = {}
    for nome, f in etapas:
        print(f"  figura interativa: {nome}")
        saida[nome] = f()
    return saida


if __name__ == "__main__":
    import json
    import time
    t = time.time()
    d = dados()
    print(len(json.dumps(d)) // 1024, "KB em", round(time.time() - t), "s")
