# -*- coding: utf-8 -*-
"""Gera os arquivos de projeto que acompanham o manual da Edição Internacional.

O manual imprime resultados; estes arquivos são o que o leitor abre para reproduzi-los. Não são
escritos à mão: saem dos mesmos parâmetros declarados em `manual/gerar_tabelas.py` e das cidades de
`scripts/gerar_exemplos_int.py` (chuva ERA5 1991-2020 de `data/rainfall` e tarifa de cada cidade), de
modo que capítulo, tabela e arquivo de projeto não possam divergir.

Cidades: **Nova York** (o tutorial), **Londres** e **Cidade do Cabo** (a comparação e os casos de
calendário). Os custos são **ilustrativos, não preços de mercado**, e só o tutorial de Nova York os
traz; os demais casos comparam hidrologia e tarifa.

Cada caso é gravado, **relido pelo programa** e simulado a partir do que foi relido. O resultado dessa
releitura é o que vai para `resultados.json`. Um campo que não sobreviva ao arquivo aparece aqui como
número errado, e não como silêncio.

Executar a partir da raiz do programa:
    python manual/gerar_casos.py
"""

from __future__ import annotations

import os

os.environ["TRITON_EDITION"] = "INT"

import json
import sys

import numpy as np

from escrita_segura import gravar  # não desfaz revisão feita à mão

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from gerar_tabelas import (                                   # noqa: E402
    CASO_23, CHUVA_23, CUSTOS_TUTORIAL, MANUTENCAO_TUTORIAL, TUTORIAL, estimate_tank_price,
)
from gerar_exemplos_int import (                              # noqa: E402
    _cidade_do_cabo, _londres, _nova_york, projeto,
)

from triton.core.parser import (                               # noqa: E402
    TritonConfig, export_triton_json, load_triton_project,
)
from triton.core.simulation import (                           # noqa: E402
    run_single_simulation, run_sweep_simulation,
)

CASOS = os.path.join(AQUI, "casos")
NL = chr(10)

#: A modulação probabilística dos exemplos: mil realizações, semente 42 (as mesmas do capítulo).
REALIZACOES, SEMENTE = 1000, 42
#: O primeiro exemplo: as três variáveis de consumo, a chuva, a tarifa e o investimento.
VARIAVEIS_DO_TUTORIAL = ("per_capita_l_dia", "pessoas", "fracao_nao_potavel_pct", "fator_chuva",
                         "fator_tarifa", "fator_investimento")
#: O segundo exemplo: a captação (área, escoamento, descarte), a chuva, a tarifa e o investimento.
VARIAVEIS_DA_CAPTACAO = ("area_m2", "coef_escoamento", "descarte_mm", "fator_chuva",
                         "fator_tarifa", "fator_investimento")

AVISO_DE_CUSTOS_ILUSTRATIVOS = (
    "Costs of works, pump, maintenance, electricity and chlorine are illustrative, not market prices "
    "(US$, rounded figures declared in manual/gerar_tabelas.py): enter your own in stage 5.")
AVISO_SEM_CUSTOS = (
    "This case compares rainfall, demand and tariff; costs of works, pump and maintenance are not set "
    "(stage 5). Enter your own to run the economic analysis.")


# ──────────────────────────────────────────────────────────────────────────────
# Peças comuns
# ──────────────────────────────────────────────────────────────────────────────

def base(nome_do_projeto, cidade):
    """Configuração comum: a cidade do `scripts/gerar_exemplos_int.py` (chuva, tarifa, moeda), volume fixo.

    `cidade` é uma das fábricas `_nova_york`, `_londres`, `_cidade_do_cabo`. Devolve a configuração, a
    série de chuva de 1991-2020, o estado da interface (moeda) e as notas de fonte da tarifa.
    """
    c = cidade()
    cfg, chuva, estado, notas = projeto(c)
    cfg.project_name = nome_do_projeto
    cfg.lower_tank_mode = 0              # volume fixo, salvo quando o caso diz outra coisa
    # Sem caixa superior, os casos declaram pressurização direta com uma bomba:
    # o arranjo precisa estar dito, ou o arquivo abre pedindo a escolha.
    cfg.supply_arrangement = "pressurizacao"
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pumping_threshold = 0.0
    cfg.pump_count = 1
    notas = dict(notas)
    notas["costs"] = AVISO_SEM_CUSTOS
    notas["example"] = nome_do_projeto
    return cfg, chuva, estado, notas, c


def com_tutorial(cfg):
    """Aplica a edificação do tutorial: 150 m², quatro moradores, 150 L/hab·dia."""
    t = TUTORIAL
    cfg.area = t["area"]
    cfg.runoff_coeff = t["runoff_coeff"]
    cfg.discard = t["discard_mm"]
    cfg.discard_mode = t["discard_mode"]
    cfg.residents_count = t["moradores"]
    cfg.demand_value = t["per_capita"]
    cfg.rainwater_share = t["rainwater_share"]
    # O descarte físico dimensionado na etapa 3, como a interface faz por padrão.
    cfg.first_flush_system_enabled = True
    return cfg


def com_custos_ilustrativos(cfg, notas):
    """Os custos do tutorial de Nova York: ilustrativos, em US$, nunca preços de mercado."""
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    cfg.op_costs = list(MANUTENCAO_TUTORIAL)
    notas["costs"] = AVISO_DE_CUSTOS_ILUSTRATIVOS
    return cfg


def com_custo(cfg, volume_l, material="PEAD"):
    cfg.lower_tank_material = material
    cfg.cost_lower_tank = estimate_tank_price(float(volume_l), material)
    cfg.cost_upper_tank = 0.0
    cfg.econ_lower_tank_vol = float(volume_l)
    return cfg


# ──────────────────────────────────────────────────────────────────────────────
# Os casos
# ──────────────────────────────────────────────────────────────────────────────

def caso_tutorial():
    """O projeto fechado do tutorial: cisterna de 4.000 L e recalque para caixa superior, em Nova York."""
    cfg, chuva, estado, notas, _ = base("Manual, tutorial - house in New York", _nova_york)
    com_tutorial(cfg)
    com_custos_ilustrativos(cfg, notas)
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = TUTORIAL["caixa_superior_l"]
    cfg.pumping_threshold = TUTORIAL["limiar_recalque_l"]
    cfg.cost_upper_tank = estimate_tank_price(TUTORIAL["caixa_superior_l"], "PEAD")
    cfg.pump_count = TritonConfig().pump_count
    return cfg, chuva, estado, notas


def caso_tutorial_varredura():
    """A varredura da seção de escolha do volume, antes da decisão pela caixa superior."""
    cfg, chuva, estado, notas, _ = base("Manual, tutorial - volume sweep (New York)", _nova_york)
    com_tutorial(cfg)
    com_custos_ilustrativos(cfg, notas)
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 20000.0
    cfg.lower_tank_step = 1000.0
    cfg.delta_ideal = 1.0
    return cfg, chuva, estado, notas


def _estado_da_modulacao(cfg, estado, variaveis):
    """A Modulação Probabilística já montada no projeto: variáveis marcadas, N e semente."""
    import copy
    from triton.core import modulacao_estocastica as M
    from triton.core.fracao_atendivel import conciliar_fracoes
    # As frações como o arquivo as grava (e o programa as relê): centrar a triagem na
    # fração ainda não conciliada daria um cartão longe do estudo.
    cfg = copy.deepcopy(cfg)
    conciliar_fracoes(cfg)
    par = M.padroes_do_projeto(cfg)
    for chave, dist in par.variaveis.items():
        dist.variar = chave in variaveis
    par.modelos_climaticos = []
    novo = dict(estado)
    novo["modulacao_estocastica"] = {"parametros": par.para_dict(), "amostras": REALIZACOES,
                                     "semente": SEMENTE}
    return novo


def caso_modulacao_tutorial():
    """A varredura do tutorial com a modulação da seção de resultados já montada."""
    cfg, chuva, estado, notas = caso_tutorial_varredura()
    cfg.project_name = "Manual, probabilistic modulation - tutorial (New York)"
    notas["example"] = cfg.project_name
    return cfg, chuva, _estado_da_modulacao(cfg, estado, VARIAVEIS_DO_TUTORIAL), notas


def caso_modulacao_captacao():
    """A mesma varredura, com a incerteza na captação e na chuva (a chuva da própria série de Nova York).

    Substitui o antigo caso dos modelos climáticos: a edição não traz base de modelos climáticos; a
    incerteza da chuva entra pelo fator de chuva sorteado sobre a série de `data/rainfall`.
    """
    cfg, chuva, estado, notas = caso_tutorial_varredura()
    cfg.project_name = "Manual, probabilistic modulation - catchment and rainfall (New York)"
    notas["example"] = cfg.project_name
    return cfg, chuva, _estado_da_modulacao(cfg, estado, VARIAVEIS_DA_CAPTACAO), notas


def caso_dez_dias():
    """Dez dias consecutivos da série de Nova York (21 a 30 de setembro de 2018), que cabem numa planilha."""
    c = CASO_23
    cfg, chuva, estado, notas, _ = base(f"Manual, section {sec('23')} - ten worked days (New York)", _nova_york)
    cfg.area = c["area"]
    cfg.runoff_coeff = c["runoff_coeff"]
    cfg.discard = c["discard_mm"]
    cfg.discard_mode = c["discard_mode"]
    cfg.first_flush_system_enabled = False
    # A demanda do caso é total, e não por morador: um "morador" que consome os
    # 200 L do dia é como o programa representa demanda total declarada.
    cfg.residents_count = 1
    cfg.demand_value = c["demanda_total"]
    cfg.rainwater_share = c["rainwater_share"]
    cfg.lower_tank_fixed = c["volume"]
    cfg.start_date = c["inicio"]
    cfg.climate_start_date, cfg.climate_end_date = c["inicio"], "30/09/2018"
    cfg.lower_tank_material = "PEAD"
    i = c["dia_na_serie"]
    dez = np.array(chuva[i:i + 10], dtype=float)
    assert np.allclose(dez, CHUVA_23), "a janela de dez dias não é a de gerar_tabelas.CHUVA_23"
    estado = dict(estado)
    estado["project"] = dict(estado["project"], start_date=c["inicio"], end_date="30/09/2018")
    notas["rainfall"] = "NewYork.csv, 21 to 30 September 2018 (ERA5 reanalysis, data/rainfall/LEIA.md)."
    return cfg, dez, estado, notas


def caso_reservatorio_superior():
    cfg, chuva, estado, notas = caso_tutorial()
    cfg.project_name = f"Manual, section {sec('08')} - with an upper tank (New York)"
    notas["example"] = cfg.project_name
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = 1000.0
    cfg.pumping_threshold = 100.0     # 10% do superior, o padrão da tela
    cfg.supply_arrangement = "recalque"
    cfg.pump_count = 1
    cfg.pump_power_str = "1/2 CV"
    cfg.pump_power_kw = 0.37
    cfg.pump_flow_rate = 3000.0
    cfg.pump_manometric_head_m = 12.0
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    return cfg, chuva, estado, notas


def caso_cidade(cidade, nome):
    """O projeto do tutorial levado a outra cidade: a chuva e a tarifa dela, sem custos."""
    cfg, chuva, estado, notas, _ = base(f"Manual, section {sec('14')} - the same project in {nome}", cidade)
    com_tutorial(cfg)
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    cfg.lower_tank_material = "PEAD"
    return cfg, chuva, estado, notas


def caso_escola():
    """Escola com demanda semanal, que fecha no fim de semana (Londres)."""
    cfg, chuva, estado, notas, _ = base(f"Manual, section {sec('18')} - school with weekly demand (London)", _londres)
    cfg.building_template_id = "escola"
    cfg.area = 1200.0
    cfg.runoff_coeff = 0.90           # laje impermeabilizada
    cfg.discard = 2.0
    cfg.residents_count = 300         # alunos
    cfg.demand_value = 40.0           # L/aluno·dia
    cfg.rainwater_share = 0.70        # bacia e limpeza dominam o consumo
    cfg.demand_mode = "weekly"
    # Segunda a sexta em aula; sábado com metade do movimento; domingo fechado,
    # com a limpeza semanal apenas.
    cfg.weekly_demands = [40.0] * 5 + [20.0, 5.0]
    cfg.weekly_residents = [300] * 5 + [150, 20]
    cfg.weekly_shares = [0.70] * 5 + [0.85, 1.0]
    cfg.lower_tank_fixed = 30000.0
    cfg.lower_tank_material = "CONCRETO"
    return cfg, chuva, estado, notas


#: Ocupação mensal do hotel de praia da Cidade do Cabo: cheio de dezembro a fevereiro (verão do hemisfério
#: sul, a estação seca da cidade), vazio no inverno, que é quando a chuva cai.
OCUPACAO_DO_HOTEL = [0.95, 0.90, 0.55, 0.35, 0.25, 0.20, 0.30, 0.25, 0.30, 0.40, 0.55, 0.80]


def caso_hotel():
    """Hotel com demanda mensal concentrada no verão seco (Cidade do Cabo), o caso que rende menos."""
    cfg, chuva, estado, notas, _ = base(f"Manual, section {sec('17')} - hotel with monthly demand (Cape Town)",
                                        _cidade_do_cabo)
    cfg.building_template_id = "hotel"
    cfg.area = 800.0
    cfg.runoff_coeff = 0.90
    cfg.discard = 2.0
    cfg.residents_count = 60          # hóspedes na ocupação plena
    cfg.demand_value = 200.0          # L/hóspede·dia
    cfg.rainwater_share = 0.45
    cfg.demand_mode = "monthly"
    cfg.demand_monthly = [200.0] * 12
    cfg.residents_monthly = [max(1, int(round(60 * o))) for o in OCUPACAO_DO_HOTEL]
    cfg.monthly_shares = [0.45] * 12
    cfg.lower_tank_fixed = 25000.0
    cfg.lower_tank_material = "CONCRETO"
    return cfg, chuva, estado, notas


# Os números de seção vêm da estrutura do manual, e não são escritos à mão.
from gerar import indice_das_marcas  # noqa: E402
_MARCAS = indice_das_marcas()


def sec(marca):
    return _MARCAS[marca]


# (arquivo, seção do manual, o que demonstra, construtor)
LISTA = [
    ("01_tutorial_new_york.triton", f"{sec('04')} to {sec('13')}",
     "the closed tutorial project in New York: a 4,000 L polyethylene cistern and a pumped feed to a 1,000 L "
     "upper tank (illustrative costs, not market prices)",
     caso_tutorial),
    ("02_london.triton", sec("14"),
     "the tutorial building taken to London, with the London rainfall and the Thames Water tariff (no costs set)",
     lambda: caso_cidade(_londres, "London")),
    ("03_cape_town.triton", sec("14"),
     "the tutorial building taken to Cape Town, with winter-concentrated rain and the City of Cape Town "
     "stepped tariff (no costs set)",
     lambda: caso_cidade(_cidade_do_cabo, "Cape Town")),
    ("04_tutorial_sweep.triton", f"{sec('07')} and {sec('24')}",
     "the project before the upper tank, in sweep mode, from 0 to 20,000 L in 1,000 L steps (New York)",
     caso_tutorial_varredura),
    ("05_ten_days.triton", sec("23"),
     "the didactic ten-day case, 21 to 30 September 2018 of the New York series, that fits in a spreadsheet",
     caso_dez_dias),
    ("06_upper_tank.triton", sec("08"),
     f"4,000 L below plus 1,000 above, the comparison of section {sec('08')} against 5,000 L in one tank (New York)",
     caso_reservatorio_superior),
    ("07_school_weekly.triton", f"{sec('17')} and {sec('18')}",
     "a 300-pupil school in London with demand modulated by day of the week",
     caso_escola),
    ("08_hotel_monthly.triton", sec("17"),
     "a beach hotel in Cape Town with monthly occupancy concentrated in the dry summer",
     caso_hotel),
    ("09_modulation_tutorial.triton", f"{sec('42')} and {sec('43')}",
     "the tutorial sweep with probabilistic modulation set up: the three consumption variables, the rain, "
     "the tariff and the investment, 1,000 realisations, seed 42",
     caso_modulacao_tutorial),
    ("10_modulation_catchment.triton", sec("43"),
     "the same sweep with the uncertainty on the catchment (area, runoff coefficient, first flush), the rain "
     "factor on the New York series, the tariff and the investment; 1,000 realisations, seed 42",
     caso_modulacao_captacao),
]


# ──────────────────────────────────────────────────────────────────────────────
# Gravação, releitura e conferência
# ──────────────────────────────────────────────────────────────────────────────

def demanda_total(cfg):
    return cfg.demand_value * (cfg.residents_count if cfg.residents_count > 0 else 1)


def _argumentos(cfg, chuva):
    return dict(
        precip_data=chuva, area=cfg.area, runoff_coeff=cfg.runoff_coeff,
        discard_mm=cfg.discard, discard_mode=cfg.discard_mode,
        discard_days_interval=cfg.discard_days_interval,
        total_demand_per_day=demanda_total(cfg),
        rainwater_share=cfg.rainwater_share,
        upper_tank_vol=cfg.upper_tank_vol,
        upper_tank_used=bool(cfg.upper_tank_used),
        pumping_threshold=cfg.pumping_threshold,
        demand_mode=getattr(cfg, "demand_mode", "constant") or "constant",
        monthly_demands=cfg.demand_monthly or None,
        monthly_residents=cfg.residents_monthly or None,
        monthly_shares=cfg.monthly_shares or None,
        weekly_demands=cfg.weekly_demands or None,
        weekly_residents=cfg.weekly_residents or None,
        weekly_shares=cfg.weekly_shares or None,
        daily_demands=cfg.daily_demands or None,
        daily_residents=cfg.daily_residents or None,
        daily_shares=cfg.daily_shares or None,
        start_date_str=cfg.start_date,
    )


def simular_do_arquivo(caminho):
    """Simula o projeto **como o programa o relê**, e não como foi construído."""
    proj = load_triton_project(caminho)
    cfg, chuva = proj["config"], proj["precip_data"]
    comum = _argumentos(cfg, chuva)
    if cfg.lower_tank_mode == 1:
        s = run_sweep_simulation(
            lower_tank_max=cfg.lower_tank_max, lower_tank_step=cfg.lower_tank_step,
            delta_ideal_threshold=cfg.delta_ideal, **comum)
        melhor = next(r for r in s.results_by_volume
                      if r.lower_tank_vol == s.optimal_lower_tank_vol)
        return {
            "modo": "varredura",
            "volume_ideal_l": s.optimal_lower_tank_vol,
            "potencial_pct": round(melhor.potential_potable_savings_pct, 2),
            "volumes_simulados": len(s.results_by_volume),
        }
    r = run_single_simulation(lower_tank_vol=cfg.lower_tank_fixed, **comum)
    return {
        "modo": "volume fixo",
        "volume_l": cfg.lower_tank_fixed,
        "potencial_pct": round(r.potential_potable_savings_pct, 2),
        "pluvial_l_dia": round(r.avg_pluvial_consumed_l_day, 1),
        "extravasado_l_dia": round(r.avg_spilled_l_day, 1),
        "atendimento_pleno_pct": round(r.pct_days_full_satisfaction, 1),
    }


def _demanda_diaria_media(cfg):
    """Médias diárias (total, pluvial) de um perfil mensal ou semanal, para o caso de demanda constante."""
    if cfg.demand_mode == "monthly":
        dias = np.array([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], dtype=float)
        total = np.array(cfg.demand_monthly) * np.array(cfg.residents_monthly)
        pluvial = total * np.array(cfg.monthly_shares)
        return float((total * dias).sum() / dias.sum()), float((pluvial * dias).sum() / dias.sum())
    total = np.array(cfg.weekly_demands) * np.array(cfg.weekly_residents)
    pluvial = total * np.array(cfg.weekly_shares)
    return float(total.mean()), float(pluvial.mean())


def comparacoes(caminho, arquivo):
    """Números extras de alguns casos: a mesma obra sob outra hipótese, para o capítulo citar."""
    proj = load_triton_project(caminho)
    cfg, chuva = proj["config"], proj["precip_data"]
    extra = {}
    if arquivo == "06_upper_tank.triton":
        a = _argumentos(cfg, chuva)
        a.update(upper_tank_vol=0.0, upper_tank_used=False, pumping_threshold=0.0)
        r = run_single_simulation(lower_tank_vol=cfg.lower_tank_fixed + cfg.upper_tank_vol, **a)
        extra["potencial_tanque_unico_pct"] = round(r.potential_potable_savings_pct, 2)
        extra["volume_tanque_unico_l"] = cfg.lower_tank_fixed + cfg.upper_tank_vol
    if arquivo in ("07_school_weekly.triton", "08_hotel_monthly.triton"):
        total, pluvial = _demanda_diaria_media(cfg)
        a = _argumentos(cfg, chuva)
        a.update(demand_mode="constant", total_demand_per_day=total, rainwater_share=pluvial / total,
                 monthly_demands=None, monthly_residents=None, monthly_shares=None,
                 weekly_demands=None, weekly_residents=None, weekly_shares=None)
        r = run_single_simulation(lower_tank_vol=cfg.lower_tank_fixed, **a)
        extra["potencial_demanda_constante_pct"] = round(r.potential_potable_savings_pct, 2)
        extra["demanda_media_l_dia"] = round(total, 1)
        extra["fracao_pluvial_media"] = round(pluvial / total, 4)
    return extra


def gravar_casos():
    os.makedirs(CASOS, exist_ok=True)
    resultados = {}
    # A série dos dez dias também vai em CSV, para quem quer refazer a planilha.
    gravar(os.path.join(CASOS, "cap23_dez_dias.csv"), "".join(f"{p:.1f}" + NL for p in CHUVA_23))
    for arquivo, capitulo, demonstra, construir in LISTA:
        cfg, chuva, estado, notas = construir()
        caminho = os.path.join(CASOS, arquivo)
        export_triton_json(
            config=cfg, file_path=caminho, precip_data=chuva,
            building_data={"demand_mode": getattr(cfg, "demand_mode", "constant")},
            ui_state=estado, analysis=notas,
        )
        r = simular_do_arquivo(caminho)
        r.update({"capitulo": capitulo, "demonstra": demonstra,
                  "projeto": cfg.project_name, "dias_de_chuva": int(len(chuva))})
        r.update(comparacoes(caminho, arquivo))
        resultados[arquivo] = r
        print(f"  {arquivo}: {r['potencial_pct']}%")
    return resultados


# ──────────────────────────────────────────────────────────────────────────────
# Saídas em texto
# ──────────────────────────────────────────────────────────────────────────────

def en(v, casas=2):
    return f"{v:,.{casas}f}"


def escrever_readme(resultados):
    linhas = [
        "# Project files from the manual (International Edition)",
        "",
        "Each file reproduces a result printed in the manual. Open it with **File > Open project**, then run.",
        "",
        "The rainfall series is embedded **inside** each file (daily rainfall of 1991-2020, ERA5 reanalysis, "
        "from `data/rainfall`): the file opens without the original CSV, on any computer. Cities: New York "
        "(the tutorial), London and Cape Town; each file carries the water and sewer tariff of its city.",
        "",
        "Costs are **illustrative, not market prices**: only the New York tutorial files (01, 04, 06, 09 and "
        "10) carry them, in US$, as rounded figures to follow the method. The other files compare rainfall, "
        "demand and tariff and leave the costs at zero. Enter your own in stage 5 before drawing any economic "
        "conclusion.",
        "",
        "Files 09 and 10 open with **Probabilistic Modulation** (stage 13) already set up: go to stage 13 "
        "and click **Simulate**. The other files use a fixed volume, except 04, so the modulation tool shows "
        "only the volume of the study on them.",
        "",
        "| File | Section | What it shows | Result |",
        "| :--- | :--- | :--- | ---: |",
    ]
    for arquivo, _, _, _ in LISTA:
        r = resultados[arquivo]
        if r["modo"] == "varredura":
            valor = f"ideal volume {en(r['volume_ideal_l'], 0)} L, {en(r['potencial_pct'])}%"
        else:
            valor = f"{en(r['potencial_pct'])}% with {en(r['volume_l'], 0)} L"
        linhas += [f"| `{arquivo}` | {r['capitulo']} | {r['demonstra']} | {valor} |"]
    linhas += [
        "",
        "The figures in the last column come from **re-reading the saved file** and simulating what was read. "
        "If a field does not survive the file, the number changes and the matching test fails.",
        "",
    ]
    caminho = os.path.join(CASOS, "README.md")
    gravar(caminho, NL.join(linhas))
    return caminho


def main():
    print("project files of the manual (International Edition):")
    resultados = gravar_casos()
    gravar(os.path.join(CASOS, "resultados.json"),
           json.dumps(resultados, indent=2, ensure_ascii=False) + NL)
    print(" ", escrever_readme(resultados))


if __name__ == "__main__":
    main()
