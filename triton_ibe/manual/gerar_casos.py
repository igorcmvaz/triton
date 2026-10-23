# -*- coding: utf-8 -*-
"""Gera os ficheiros de projeto que acompanham o manual da Edição Ibérica.

O manual imprime resultados; estes ficheiros são o que o leitor abre para os reproduzir. Não são
escritos à mão: saem dos mesmos parâmetros declarados em `manual/gerar_tabelas.py` e das cidades de
`scripts/gerar_exemplos_prt.py` (chuva E-OBS por concelho ou ERA5 do Funchal, e o tarifário transcrito
de cada cidade), de modo que capítulo, tabela e ficheiro de projeto não possam divergir.

Cidades: **Lisboa** (o tutorial), **Porto** e **Funchal** (a comparação). Os custos são **ilustrativos,
não são preços de mercado**, e só o tutorial de Lisboa os traz; os restantes casos comparam hidrologia,
procura e tarifário.

Cada caso é gravado, **relido pelo programa** e simulado a partir do que foi relido. O resultado dessa
releitura é o que vai para `resultados.json`. Um campo que não sobreviva ao ficheiro aparece aqui como
número errado, e não como silêncio.

Executar a partir da raiz do programa:
    python manual/gerar_casos.py
"""

from __future__ import annotations

import os

os.environ["TRITON_EDITION"] = "IBE"

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
from gerar_exemplos_prt import (                              # noqa: E402
    _funchal, _lisboa, _porto, projeto,
)

from triton.core.parser import (                               # noqa: E402
    TritonConfig, export_triton_json, load_triton_project,
)
from triton.core.simulation import (                           # noqa: E402
    run_single_simulation, run_sweep_simulation,
)

CASOS = os.path.join(AQUI, "casos")
NL = chr(10)
NBSP = chr(160)

#: A modulação probabilística dos exemplos: mil realizações, semente 42 (as mesmas do capítulo).
REALIZACOES, SEMENTE = 1000, 42
#: O primeiro exemplo: as três variáveis de consumo, a chuva, o tarifário e o investimento.
VARIAVEIS_DO_TUTORIAL = ("per_capita_l_dia", "pessoas", "fracao_nao_potavel_pct", "fator_chuva",
                         "fator_tarifa", "fator_investimento")
#: O segundo exemplo: a captação (área, escoamento, descarte), a chuva, o tarifário e o investimento.
VARIAVEIS_DA_CAPTACAO = ("area_m2", "coef_escoamento", "descarte_mm", "fator_chuva",
                         "fator_tarifa", "fator_investimento")

AVISO_DE_CUSTOS_ILUSTRATIVOS = (
    "Os custos de obra, de bomba, de manutenção, de eletricidade e de cloro são ilustrativos, não são "
    "preços de mercado (euros, valores redondos declarados em manual/gerar_tabelas.py): introduza os seus "
    "na etapa 5.")
AVISO_SEM_CUSTOS = (
    "Este caso compara chuva, procura e tarifário; os custos de obra, de bomba e de manutenção não estão "
    "definidos (etapa 5). Introduza os seus para fazer a análise económica.")


# ──────────────────────────────────────────────────────────────────────────────
# Peças comuns
# ──────────────────────────────────────────────────────────────────────────────

def base(nome_do_projeto, cidade):
    """Configuração comum: a cidade do `scripts/gerar_exemplos_prt.py` (chuva, tarifário, moeda), volume fixo.

    `cidade` é uma das fábricas `_lisboa`, `_porto`, `_funchal`. Devolve a configuração, a série de chuva
    de 1991-2020, o estado da interface (moeda) e as notas de fonte do tarifário.
    """
    c = cidade()
    cfg, chuva, estado, notas = projeto(c)
    cfg.project_name = nome_do_projeto
    cfg.lower_tank_mode = 0              # volume fixo, salvo quando o caso diz outra coisa
    # Sem reservatório superior, os casos declaram pressurização direta com uma bomba:
    # o arranjo precisa de estar dito, ou o ficheiro abre a pedir a escolha.
    cfg.supply_arrangement = "pressurizacao"
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pumping_threshold = 0.0
    cfg.pump_count = 1
    notas = dict(notas)
    notas["custos"] = AVISO_SEM_CUSTOS
    notas["exemplo"] = nome_do_projeto
    return cfg, chuva, estado, notas, c


def com_tutorial(cfg):
    """Aplica a edificação do tutorial: 150 m², quatro residentes, 150 L/hab·dia."""
    t = TUTORIAL
    cfg.area = t["area"]
    cfg.runoff_coeff = t["runoff_coeff"]
    cfg.discard = t["discard_mm"]
    cfg.discard_mode = t["discard_mode"]
    cfg.residents_count = t["moradores"]
    cfg.demand_value = t["per_capita"]
    cfg.rainwater_share = t["rainwater_share"]
    # O descarte físico dimensionado na etapa 3, como a interface faz por omissão.
    cfg.first_flush_system_enabled = True
    return cfg


def com_custos_ilustrativos(cfg, notas):
    """Os custos do tutorial de Lisboa: ilustrativos, em euros, nunca preços de mercado."""
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    cfg.op_costs = list(MANUTENCAO_TUTORIAL)
    notas["custos"] = AVISO_DE_CUSTOS_ILUSTRATIVOS
    notas["eletricidade"] = (
        "0,20 €/kWh, valor ilustrativo, não é preço de mercado (o tarifário de eletricidade de Lisboa não "
        "está registado na edição): introduza o seu na etapa 5.")
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
    """O projeto fechado do tutorial: cisterna de 5.000 L e elevação para reservatório superior, em Lisboa."""
    cfg, chuva, estado, notas, _ = base("Manual, tutorial - moradia em Lisboa", _lisboa)
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
    """A varredura da secção de escolha do volume, antes da decisão pelo reservatório superior."""
    cfg, chuva, estado, notas, _ = base("Manual, tutorial - varredura de volumes (Lisboa)", _lisboa)
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
    # As frações como o ficheiro as grava (e o programa as relê): centrar a triagem na
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
    """A varredura do tutorial com a modulação da secção de resultados já montada."""
    cfg, chuva, estado, notas = caso_tutorial_varredura()
    cfg.project_name = "Manual, modulação probabilística - tutorial (Lisboa)"
    notas["exemplo"] = cfg.project_name
    return cfg, chuva, _estado_da_modulacao(cfg, estado, VARIAVEIS_DO_TUTORIAL), notas


def caso_modulacao_captacao():
    """A mesma varredura, com a incerteza na captação e na chuva (a chuva da própria série de Lisboa).

    Substitui o antigo caso dos modelos climáticos: a edição não traz base de modelos climáticos; a
    incerteza da chuva entra pelo fator de chuva sorteado sobre a série E-OBS de Lisboa.
    """
    cfg, chuva, estado, notas = caso_tutorial_varredura()
    cfg.project_name = "Manual, modulação probabilística - captação e chuva (Lisboa)"
    notas["exemplo"] = cfg.project_name
    return cfg, chuva, _estado_da_modulacao(cfg, estado, VARIAVEIS_DA_CAPTACAO), notas


def caso_dez_dias():
    """Dez dias consecutivos da série de Lisboa (11 a 20 de dezembro de 2019), que cabem numa folha de cálculo."""
    c = CASO_23
    cfg, chuva, estado, notas, _ = base(f"Manual, secção {sec('23')} - dez dias resolvidos (Lisboa)", _lisboa)
    cfg.area = c["area"]
    cfg.runoff_coeff = c["runoff_coeff"]
    cfg.discard = c["discard_mm"]
    cfg.discard_mode = c["discard_mode"]
    cfg.first_flush_system_enabled = False
    # A procura do caso é total, e não por residente: um «residente» que consome os
    # 200 L do dia é como o programa representa a procura total declarada.
    cfg.residents_count = 1
    cfg.demand_value = c["demanda_total"]
    cfg.rainwater_share = c["rainwater_share"]
    cfg.lower_tank_fixed = c["volume"]
    cfg.start_date = c["inicio"]
    cfg.lower_tank_material = "PEAD"
    i = c["dia_na_serie"]
    dez = np.array([round(float(x), 1) for x in chuva[i:i + 10]], dtype=float)
    assert np.allclose(dez, CHUVA_23), "a janela de dez dias não é a de gerar_tabelas.CHUVA_23"
    # Os dez dias vão dentro do ficheiro (já não são uma referência à base E-OBS).
    cfg.climate_source_mode = "custom_file"
    cfg.climate_city_uf, cfg.climate_city_name = "", "Lisboa"
    cfg.climate_model, cfg.climate_scenario = "E-OBS v33.0e", "EOBS"
    cfg.precip_file = ""
    cfg.climate_start_date, cfg.climate_end_date = c["inicio"], "20/12/2019"
    estado = dict(estado)
    estado["project"] = {"source_mode": "custom_file", "start_date": c["inicio"], "end_date": "20/12/2019"}
    notas["chuva"] = ("Lisboa, 11 a 20 de dezembro de 2019 (E-OBS v33.0e, concelho de Lisboa, arredondada "
                      "ao décimo de milímetro; data/portugal_eobs.db).")
    return cfg, dez, estado, notas


def caso_reservatorio_superior():
    cfg, chuva, estado, notas = caso_tutorial()
    cfg.project_name = f"Manual, secção {sec('08')} - com reservatório superior (Lisboa)"
    notas["exemplo"] = cfg.project_name
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = 1000.0
    cfg.pumping_threshold = 100.0     # 10% do superior, o padrão do ecrã
    cfg.supply_arrangement = "recalque"
    cfg.pump_count = 1
    cfg.pump_power_str = "1/2 CV"
    cfg.pump_power_kw = 0.37
    cfg.pump_flow_rate = 3000.0
    cfg.pump_manometric_head_m = 12.0
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    return cfg, chuva, estado, notas


def caso_cidade(cidade, nome):
    """O projeto do tutorial levado a outra cidade: a chuva e o tarifário dela, sem custos."""
    cfg, chuva, estado, notas, _ = base(f"Manual, secção {sec('14')} - o mesmo projeto no {nome}", cidade)
    com_tutorial(cfg)
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    cfg.lower_tank_material = "PEAD"
    return cfg, chuva, estado, notas


def caso_escola():
    """Escola com procura semanal, que fecha ao fim de semana (Porto)."""
    cfg, chuva, estado, notas, _ = base(f"Manual, secção {sec('18')} - escola com procura semanal (Porto)", _porto)
    cfg.building_template_id = "escola"
    cfg.area = 1200.0
    cfg.runoff_coeff = 0.90           # laje impermeabilizada
    cfg.discard = 2.0
    cfg.residents_count = 300         # alunos
    cfg.demand_value = 40.0           # L/aluno·dia
    cfg.rainwater_share = 0.70        # autoclismos e limpeza dominam o consumo
    cfg.demand_mode = "weekly"
    # Segunda a sexta com aulas; sábado com metade do movimento; domingo fechado,
    # com a limpeza semanal apenas.
    cfg.weekly_demands = [40.0] * 5 + [20.0, 5.0]
    cfg.weekly_residents = [300] * 5 + [150, 20]
    cfg.weekly_shares = [0.70] * 5 + [0.85, 1.0]
    cfg.lower_tank_fixed = 30000.0
    cfg.lower_tank_material = "CONCRETO"
    return cfg, chuva, estado, notas


#: Ocupação mensal ilustrativa do hotel de Lisboa: cheio de junho a setembro (o verão seco da cidade),
#: quase vazio no inverno, que é quando a chuva cai.
OCUPACAO_DO_HOTEL = [0.40, 0.45, 0.55, 0.70, 0.80, 0.90, 0.95, 1.00, 0.90, 0.75, 0.50, 0.45]


def caso_hotel():
    """Hotel com procura mensal concentrada no verão seco (Lisboa), o caso que rende menos."""
    cfg, chuva, estado, notas, _ = base(f"Manual, secção {sec('17')} - hotel com procura mensal (Lisboa)", _lisboa)
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


# Os números de secção vêm da estrutura do manual, e não são escritos à mão.
from gerar import indice_das_marcas  # noqa: E402
_MARCAS = indice_das_marcas()


def sec(marca):
    return _MARCAS[marca]


# (ficheiro, secção do manual, o que demonstra, construtor)
LISTA = [
    ("01_tutorial_lisboa.triton", f"{sec('04')} a {sec('13')}",
     "o projeto fechado do tutorial em Lisboa: cisterna de 5.000 L em polietileno e elevação para um "
     "reservatório superior de 1.000 L (custos ilustrativos, não são preços de mercado)",
     caso_tutorial),
    ("02_porto.triton", sec("14"),
     "a moradia do tutorial levada ao Porto, com a chuva E-OBS do Porto e o tarifário da Águas e Energia do "
     "Porto (sem custos definidos)",
     lambda: caso_cidade(_porto, "Porto")),
    ("03_funchal.triton", sec("14"),
     "a moradia do tutorial levada ao Funchal, com a chuva ERA5 do Funchal, o tarifário da Câmara Municipal "
     "do Funchal e a eletricidade da EEM (sem custos definidos)",
     lambda: caso_cidade(_funchal, "Funchal")),
    ("04_tutorial_varredura.triton", f"{sec('07')} e {sec('24')}",
     "o projeto antes do reservatório superior, em modo varredura, de 0 a 20.000 L em passos de 1.000 L (Lisboa)",
     caso_tutorial_varredura),
    ("05_dez_dias.triton", sec("23"),
     "o caso didático de dez dias, 11 a 20 de dezembro de 2019 da série de Lisboa, que cabe numa folha de cálculo",
     caso_dez_dias),
    ("06_reservatorio_superior.triton", sec("08"),
     f"5.000 L em baixo mais 1.000 em cima, a comparação da secção {sec('08')} contra os 6.000 L de um "
     "reservatório só (Lisboa)",
     caso_reservatorio_superior),
    ("07_escola_semanal.triton", f"{sec('17')} e {sec('18')}",
     "uma escola do Porto, com 300 alunos e procura modulada por dia da semana",
     caso_escola),
    ("08_hotel_mensal.triton", sec("17"),
     "um hotel de Lisboa com ocupação mensal ilustrativa, concentrada no verão seco",
     caso_hotel),
    ("09_modulacao_tutorial.triton", f"{sec('42')} e {sec('43')}",
     "a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, "
     "o tarifário e o investimento, mil realizações, semente 42",
     caso_modulacao_tutorial),
    ("10_modulacao_captacao.triton", sec("43"),
     "a mesma varredura com a incerteza na captação (área, coeficiente de escoamento, descarte), o fator de "
     "chuva sobre a série de Lisboa, o tarifário e o investimento; mil realizações, semente 42",
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
    """Médias diárias (total, pluvial) de um perfil mensal ou semanal, para o caso de procura constante."""
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
    if arquivo == "06_reservatorio_superior.triton":
        a = _argumentos(cfg, chuva)
        a.update(upper_tank_vol=0.0, upper_tank_used=False, pumping_threshold=0.0)
        r = run_single_simulation(lower_tank_vol=cfg.lower_tank_fixed + cfg.upper_tank_vol, **a)
        extra["potencial_tanque_unico_pct"] = round(r.potential_potable_savings_pct, 2)
        extra["volume_tanque_unico_l"] = cfg.lower_tank_fixed + cfg.upper_tank_vol
    if arquivo in ("07_escola_semanal.triton", "08_hotel_mensal.triton"):
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
    # A série dos dez dias também vai em CSV, para quem quer refazer a folha de cálculo.
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

def pt(v, casas=2):
    return f"{v:,.{casas}f}".replace(",", NBSP).replace(".", ",")


def escrever_readme(resultados):
    linhas = [
        "# Ficheiros de projeto do manual (Edição Ibérica)",
        "",
        "Cada ficheiro reproduz um resultado impresso no manual. Abra-o com **Ficheiro > Abrir projeto** e "
        "carregue em **Simular**.",
        "",
        "A chuva de Lisboa e do Porto é a da base E-OBS por concelho (normal 1991-2020, `data/portugal_eobs.db`): "
        "o ficheiro guarda a referência da série e a impressão digital dos valores, e o programa recompõe-na "
        "da base ao abrir. O Funchal usa a série ERA5 de `data/rainfall/Funchal.csv`, incorporada no ficheiro. "
        "O caso dos dez dias traz os seus dez valores dentro do ficheiro. Cidades: Lisboa (o tutorial), Porto "
        "e Funchal; cada ficheiro leva o tarifário de água e saneamento da sua cidade, transcrito em "
        "`triton/data/portugal_tarifarios.json`.",
        "",
        "Os custos são **ilustrativos, não são preços de mercado**: só os ficheiros do tutorial de Lisboa (01, "
        "04, 06, 09 e 10) os trazem, em euros, como valores redondos para acompanhar o método. Os outros "
        "ficheiros comparam chuva, procura e tarifário e deixam os custos a zero. Introduza os seus na etapa 5 "
        "antes de tirar qualquer conclusão económica.",
        "",
        "Os ficheiros 09 e 10 abrem com a **Modulação Probabilística** (etapa 13) já montada: vá à etapa 13 e "
        "carregue em **Simular**. Os restantes têm volume fixo, com exceção do 04, e por isso a ferramenta de "
        "modulação mostra neles só o volume do estudo.",
        "",
        "| Ficheiro | Secção | O que demonstra | Resultado |",
        "| :--- | :--- | :--- | ---: |",
    ]
    for arquivo, _, _, _ in LISTA:
        r = resultados[arquivo]
        if r["modo"] == "varredura":
            valor = f"volume ideal {pt(r['volume_ideal_l'], 0)} L, {pt(r['potencial_pct'])}%"
        else:
            valor = f"{pt(r['potencial_pct'])}% com {pt(r['volume_l'], 0)} L"
        linhas += [f"| `{arquivo}` | {r['capitulo']} | {r['demonstra']} | {valor} |"]
    linhas += [
        "",
        "Os números da última coluna obtêm-se **relendo o ficheiro gravado** e simulando o que foi relido. "
        "Se um campo não sobreviver ao ficheiro, o número muda e o teste correspondente falha.",
        "",
    ]
    caminho = os.path.join(CASOS, "README.md")
    gravar(caminho, NL.join(linhas))
    return caminho


def main():
    print("ficheiros de projeto do manual (Edição Ibérica):")
    resultados = gravar_casos()
    gravar(os.path.join(CASOS, "resultados.json"),
           json.dumps(resultados, indent=2, ensure_ascii=False) + NL)
    print(" ", escrever_readme(resultados))


if __name__ == "__main__":
    main()
