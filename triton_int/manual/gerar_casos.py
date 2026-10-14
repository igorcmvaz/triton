# -*- coding: utf-8 -*-
"""Gera os arquivos de projeto que acompanham o manual.

O manual imprime resultados; estes arquivos são o que o leitor abre para
reproduzi-los. Não são escritos à mão: saem dos mesmos parâmetros declarados em
`manual/gerar_tabelas.py`, de modo que capítulo, tabela e arquivo de projeto não
possam divergir.

Cada caso é gravado, **relido pelo programa** e simulado a partir do que foi
relido. O resultado dessa releitura é o que vai para `resultados.json` e para o
apêndice J. Um campo que não sobreviva ao arquivo aparece aqui como número
errado, e não como silêncio.

Executar a partir da raiz do programa:
    python manual/gerar_casos.py
"""

from __future__ import annotations

import json
import os

from escrita_segura import gravar  # não desfaz revisão feita à mão
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
sys.path.insert(0, AQUI)

from gerar_tabelas import (                                   # noqa: E402
    CASO_23, CHUVA_23, CUSTOS_TUTORIAL, TARIFA_CASAN, TUTORIAL,
)

from triton.core.cost_estimates import estimate_tank_price     # noqa: E402
from triton.core.parser import (                               # noqa: E402
    TritonConfig, export_triton_json, load_triton_project, load_precipitation,
)
from triton.core.simulation import (                           # noqa: E402
    run_single_simulation, run_sweep_simulation,
)

CASOS = os.path.join(AQUI, "casos")
CHUVAS = os.path.join(RAIZ, "data", "rainfall")
ANOS = 30
NL = chr(10)


def serie(nome, anos=ANOS):
    return load_precipitation(os.path.join(CHUVAS, f"{nome}.csv"))[: anos * 365]


def base(nome_do_projeto, cidade, uf="SC"):
    """Configuração comum a todos os casos do manual.

    A tarifa, os custos e o período de análise são os do tutorial, declarados
    uma única vez em `gerar_tabelas.py`.
    """
    cfg = TritonConfig()
    cfg.project_name = nome_do_projeto
    cfg.climate_source_mode = "custom_file"
    cfg.climate_city_name = cidade
    cfg.climate_city_uf = uf
    cfg.tariff_city_name, cfg.tariff_city_uf = cidade, uf
    cfg.elec_city_name, cfg.elec_city_uf = cidade, uf
    cfg.water_tariffs = list(TARIFA_CASAN)
    cfg.sewage_mode, cfg.sewage_rate = 1, 100.0
    for k, v in CUSTOS_TUTORIAL.items():
        setattr(cfg, k, v)
    cfg.lower_tank_mode = 0          # volume fixo, salvo quando o caso diz outra coisa
    # Sem caixa superior, os casos declaram pressurização direta com uma bomba:
    # o arranjo precisa estar dito, ou o arquivo abre pedindo a escolha.
    cfg.supply_arrangement = "pressurizacao"
    cfg.upper_tank_used = 0
    cfg.upper_tank_vol = 0.0
    cfg.pumping_threshold = 0.0
    cfg.pump_count = 1
    return cfg


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
    # O descarte físico dimensionado na etapa 3, como a interface faz por
    # padrão e como os capítulos do tutorial calculam.
    cfg.first_flush_system_enabled = True
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
    """O projeto fechado do tutorial: cisterna de 4.000 L e recalque para caixa superior."""
    cfg = com_tutorial(base("Manual, tutorial - residencia em Florianopolis",
                            "Florianópolis"))
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    cfg.supply_arrangement = "recalque"
    cfg.upper_tank_used = 1
    cfg.upper_tank_vol = TUTORIAL["caixa_superior_l"]
    cfg.pumping_threshold = TUTORIAL["limiar_recalque_l"]
    cfg.cost_upper_tank = estimate_tank_price(TUTORIAL["caixa_superior_l"], "PEAD")
    cfg.pump_count = TritonConfig().pump_count
    return cfg, serie("Florianopolis1")


def caso_tutorial_varredura():
    """A varredura da seção de escolha do volume, antes da decisão pela caixa superior."""
    cfg = com_tutorial(base("Manual, tutorial - varredura de volumes", "Florianópolis"))
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    chuva = serie("Florianopolis1")
    cfg.lower_tank_mode = 1
    cfg.lower_tank_max = 20000.0
    cfg.lower_tank_step = 1000.0
    cfg.delta_ideal = 1.0
    return cfg, chuva


def _estado_da_modulacao(cfg, variaveis, modelos=()):
    """A Modulação Probabilística já montada no projeto: variáveis marcadas, modelos, N e semente."""
    from gerar_modulacao import REALIZACOES, SEMENTE
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
    par.modelos_climaticos = list(modelos)
    return {"modulacao_estocastica": {"parametros": par.para_dict(), "amostras": REALIZACOES,
                                      "semente": SEMENTE}}


def caso_modulacao_tutorial():
    """A varredura do tutorial com a modulação da seção de resultados já montada."""
    from gerar_modulacao import VARIAVEIS_DO_EXEMPLO
    cfg, chuva = caso_tutorial_varredura()
    cfg.project_name = "Manual, modulacao probabilistica - tutorial"
    return cfg, chuva, _estado_da_modulacao(cfg, VARIAVEIS_DO_EXEMPLO)


def caso_modulacao_climbra():
    """A mesma varredura com a chuva da CLIMBra e os dezenove modelos marcados.

    O arquivo guarda a referência da série (cidade, modelo, cenário e recorte), e não os
    valores: o programa a recompõe da base ao abrir.
    """
    from gerar_modulacao import CENARIO_DO_EXEMPLO, CIDADE_DO_EXEMPLO, FIM_DO_EXEMPLO, INICIO_DO_EXEMPLO
    from triton.core import modulacao_estocastica as M
    from triton.core.climate_database import CLIMATE_MODELS
    from triton.core.parser import serie_da_climbra
    cfg, _ = caso_tutorial_varredura()
    cfg.project_name = "Manual, modulacao probabilistica - modelos climaticos"
    cfg.climate_source_mode = "national_db"
    cfg.climate_city_uf, cfg.climate_city_name = "SC", CIDADE_DO_EXEMPLO
    cfg.climate_scenario = CENARIO_DO_EXEMPLO
    cfg.climate_start_date, cfg.climate_end_date = INICIO_DO_EXEMPLO, FIM_DO_EXEMPLO
    cfg.start_date = INICIO_DO_EXEMPLO
    cfg.precip_file = ""
    estado = _estado_da_modulacao(cfg, M.PARAMETROS, CLIMATE_MODELS)
    estado["project"] = {"source_mode": "national_db", "climate_uf": "SC", "climate_city": CIDADE_DO_EXEMPLO,
                         "climate_model": cfg.climate_model, "climate_scenario": CENARIO_DO_EXEMPLO,
                         "start_date": INICIO_DO_EXEMPLO, "end_date": FIM_DO_EXEMPLO}
    return cfg, serie_da_climbra(cfg), estado


def caso_dez_dias():
    c = CASO_23
    cfg = base(f"Manual, secao {sec('23')} - dez dias resolvidos", "Florianópolis")
    cfg.area = c["area"]
    cfg.runoff_coeff = c["runoff_coeff"]
    cfg.discard = c["discard_mm"]
    cfg.discard_mode = c["discard_mode"]
    # A demanda do caso é total, e não por morador: um "morador" que consome os
    # 200 L do dia é como o programa representa demanda total declarada.
    cfg.residents_count = 1
    cfg.demand_value = c["demanda_total"]
    cfg.rainwater_share = c["rainwater_share"]
    cfg.lower_tank_fixed = c["volume"]
    cfg.start_date = "01/01/2020"
    com_custo(cfg, c["volume"], "PEAD")
    return cfg, np.array(CHUVA_23, dtype=float)


def caso_reservatorio_superior():
    cfg, chuva = caso_tutorial()
    cfg.project_name = f"Manual, secao {sec('08')} - com reservatorio superior"
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
    return cfg, chuva


def caso_cidade(chave, nome, uf):
    cfg = com_tutorial(base(f"Manual, secao {sec('14')} - o mesmo projeto em {nome}",
                            nome, uf))
    cfg.lower_tank_fixed = TUTORIAL["volume"]
    com_custo(cfg, TUTORIAL["volume"], "PEAD")
    return cfg, serie(chave)


def caso_escola():
    """Escola com demanda semanal, que fecha no fim de semana."""
    cfg = base(f"Manual, secao {sec('18')} - escola com demanda semanal", "Florianópolis")
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
    com_custo(cfg, 30000.0, "CONCRETO")
    return cfg, serie("Florianopolis1")


def caso_hotel():
    """Hotel com demanda mensal em fase com a chuva, o caso que rende menos."""
    cfg = base(f"Manual, secao {sec('17')} - hotel com demanda mensal", "Florianópolis")
    cfg.building_template_id = "hotel"
    cfg.area = 800.0
    cfg.runoff_coeff = 0.90
    cfg.discard = 2.0
    cfg.residents_count = 60          # hóspedes na ocupação plena
    cfg.demand_value = 200.0          # L/hóspede·dia
    cfg.rainwater_share = 0.45
    cfg.demand_mode = "monthly"
    # Ocupação do litoral catarinense: cheio em janeiro e fevereiro, vazio no
    # inverno. É a demanda em fase com a chuva, que é o caso desfavorável.
    ocupacao = [0.95, 0.90, 0.55, 0.35, 0.25, 0.20,
                0.30, 0.25, 0.30, 0.40, 0.55, 0.80]
    cfg.demand_monthly = [200.0] * 12
    cfg.residents_monthly = [max(1, int(round(60 * o))) for o in ocupacao]
    cfg.monthly_shares = [0.45] * 12
    cfg.lower_tank_fixed = 25000.0
    cfg.start_date = "01/01/1980"
    com_custo(cfg, 25000.0, "CONCRETO")
    return cfg, serie("Florianopolis1")


# Os números de seção vêm da estrutura do manual, e não são escritos à mão: a
# primeira versão desta lista trazia os números das antigas partes (capítulo 23,
# guia 14), que deixaram de existir na renumeração da ABNT.
from gerar import indice_das_marcas  # noqa: E402
_MARCAS = indice_das_marcas()


def sec(marca):
    return _MARCAS[marca]


# (arquivo, seção do manual, o que demonstra, construtor)
LISTA = [
    ("01_tutorial_florianopolis.triton", f"{sec('04')} a {sec('13')}",
     f"o projeto fechado do tutorial: cisterna de 4.000 L em polietileno e recalque para caixa superior de 1.000 L",
     caso_tutorial),
    ("02_tutorial_varredura.triton", f"{sec('07')} e {sec('24')}",
     "o projeto antes da caixa superior, em modo varredura, de 0 a 20.000 L, passo de 1.000 L",
     caso_tutorial_varredura),
    ("03_dez_dias.triton", sec("23"),
     "o caso didático de dez dias, que cabe numa planilha",
     caso_dez_dias),
    ("04_reservatorio_superior.triton", sec("08"),
     f"4.000 L embaixo mais 1.000 em cima, a comparação da seção {sec('08')} contra os 5.000 L de um tanque só",
     caso_reservatorio_superior),
    ("05_manaus.triton", sec("14"),
     "o projeto do tutorial levado a Manaus, que chove mais e rende menos",
     lambda: caso_cidade("Manaus1", "Manaus", "AM")),
    ("06_brasilia.triton", sec("14"),
     "o projeto do tutorial levado a Brasília, de estação seca marcada",
     lambda: caso_cidade("Brasilia1", "Brasília", "DF")),
    ("07_saopaulo.triton", sec("14"),
     "o projeto do tutorial levado a São Paulo",
     lambda: caso_cidade("SaoPaulo1", "São Paulo", "SP")),
    ("08_escola_semanal.triton", f"{sec('17')} e {sec('18')}",
     "escola de 300 alunos com demanda modulada por dia da semana",
     caso_escola),
    ("09_hotel_mensal.triton", sec("17"),
     "hotel de litoral com ocupação mensal em fase com a chuva",
     caso_hotel),
    ("10_modulacao_tutorial.triton", f"{sec('42')} e {sec('43')}",
     "a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, "
     "a tarifa e o investimento, mil realizações, semente 42",
     caso_modulacao_tutorial),
    ("11_modulacao_climbra.triton", sec("43"),
     "a mesma varredura com a chuva da CLIMBra (Florianópolis, SSP2-4.5, 2025 a 2054) e os dezenove modelos "
     "climáticos marcados; o arquivo guarda a referência da série, e não os valores",
     caso_modulacao_climbra),
]


# ──────────────────────────────────────────────────────────────────────────────
# Gravação, releitura e conferência
# ──────────────────────────────────────────────────────────────────────────────

def demanda_total(cfg):
    return cfg.demand_value * (cfg.residents_count if cfg.residents_count > 0 else 1)


def simular_do_arquivo(caminho):
    """Simula o projeto **como o programa o relê**, e não como foi construído."""
    proj = load_triton_project(caminho)
    cfg, chuva = proj["config"], proj["precip_data"]
    comum = dict(
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


def gravar_casos():
    os.makedirs(CASOS, exist_ok=True)
    resultados = {}
    for arquivo, capitulo, demonstra, construir in LISTA:
        cfg, chuva, *estado = construir()
        caminho = os.path.join(CASOS, arquivo)
        export_triton_json(
            config=cfg, file_path=caminho, precip_data=chuva,
            building_data={"demand_mode": getattr(cfg, "demand_mode", "constant")},
            ui_state=estado[0] if estado else None,
        )
        r = simular_do_arquivo(caminho)
        r.update({"capitulo": capitulo, "demonstra": demonstra,
                  "projeto": cfg.project_name, "dias_de_chuva": int(len(chuva))})
        resultados[arquivo] = r
        print(f"  {arquivo}: {r['potencial_pct']}%")
    return resultados


# ──────────────────────────────────────────────────────────────────────────────
# Os três estudos de `examples/`, gravados num esquema que o programa não lê
# ──────────────────────────────────────────────────────────────────────────────
#
# Eram do esquema plano de 2025. Abertos pelo programa, devolviam a configuração
# padrão inteira: o leitor simulava 100 m² achando que simulava 180. Agora a
# abertura recusa o formato, e estes três são regravados no esquema corrente.

MATERIAL_ANTIGO = {"PRFV": "FIBRA", "PEAD": "PEAD",
                   "CONCRETO": "CONCRETO", "ACO_INOX": "ACO_INOX"}


def converter_exemplos():
    pasta = os.path.join(RAIZ, "examples")
    convertidos = []
    for arquivo in sorted(os.listdir(pasta)):
        if not arquivo.endswith(".triton"):
            continue
        caminho = os.path.join(pasta, arquivo)
        d = json.load(open(caminho, encoding="utf-8"))
        if "inputs" in d or "schema" in d:
            continue                      # já está no esquema corrente
        cfg = TritonConfig()
        cfg.project_name = d.get("title", arquivo)
        cfg.area = float(d["area"])
        cfg.runoff_coeff = float(d["runoff"])
        cfg.discard = float(d["discard"])
        cfg.discard_mode = int(d.get("discard_mode", 1))
        cfg.discard_days_interval = int(d.get("discard_days", 7))
        cfg.residents_count = int(d["residents"])
        cfg.demand_value = float(d["demand"])
        # No esquema antigo a fração vinha em porcentagem.
        cfg.rainwater_share = float(d["share"]) / 100.0
        cfg.upper_tank_vol = float(d.get("upper_vol", 0.0))
        cfg.upper_tank_used = 1 if d.get("upper_used") else 0
        cfg.pumping_threshold = cfg.upper_tank_vol * float(
            d.get("pump_thresh_pct", 10.0)) / 100.0
        cfg.lower_tank_mode = 1
        cfg.lower_tank_max = float(d.get("sweep_max", 10000.0))
        cfg.lower_tank_step = float(d.get("sweep_step", 500.0))
        cfg.delta_ideal = float(d.get("delta_ideal", 5.0))
        # "PRFV" não é chave de material do programa; a chave é "FIBRA".
        cfg.lower_tank_material = MATERIAL_ANTIGO.get(
            d.get("lower_tank_material", "PEAD"), "PEAD")
        cfg.upper_tank_material = MATERIAL_ANTIGO.get(
            d.get("upper_tank_material", "PEAD"), "PEAD")
        cfg.water_tariffs = [tuple(t) for t in d.get("water_tariffs", [])] or \
            list(TARIFA_CASAN)
        cfg.sewage_mode = int(d.get("sewage_mode", 1))
        cfg.sewage_rate = float(d.get("sewage_rate", 100.0))
        cfg.elec_tariff = float(d.get("elec_tariff", 0.69568))
        cfg.pump_count = int(d.get("pump_count", 1))
        cfg.pump_power_kw = float(d.get("pump_power_kw", 0.37))
        cfg.pump_flow_rate = float(d.get("pump_flow_rate", 3000.0))
        cfg.pump_efficiency = float(d.get("pump_efficiency", 55.0))
        cfg.chlorine_treatment_enabled = bool(d.get("chlorine_treatment_enabled", True))
        cfg.chlorine_dose_mg_l = float(d.get("chlorine_dose_mg_l", 1.5))
        cfg.chlorine_cost_per_kg = float(d.get("chlorine_cost_per_kg", 25.0))
        cfg.pipes_list = [tuple(p) for p in d.get("pipes_list", [])] or cfg.pipes_list
        cfg.climate_source_mode = "custom_file"
        cfg.climate_city_name = d.get("climate_city", "")
        cfg.precip_file = d.get("rain_file", "")

        chuva = serie(os.path.splitext(d["rain_file"])[0])
        export_triton_json(config=cfg, file_path=caminho, precip_data=chuva)
        convertidos.append(arquivo)
        print(f"  {arquivo}: {d.get('area')} m2, {len(chuva)} dias")
    return convertidos


# ──────────────────────────────────────────────────────────────────────────────
# Saídas em texto
# ──────────────────────────────────────────────────────────────────────────────

def br(v, casas=2):
    return f"{v:,.{casas}f}".replace(",", "#").replace(".", ",").replace("#", ".")


def escrever_readme(resultados):
    linhas = [
        "# Arquivos de projeto do manual",
        "",
        "Cada arquivo reproduz um resultado impresso no manual. Abra pelo menu",
        "**Arquivo, Abrir projeto**, e rode.",
        "",
        "A série de chuva está **dentro** do arquivo: ele abre sem o CSV original,",
        "em qualquer máquina. A exceção é o `11_modulacao_climbra.triton`, com a",
        "chuva da base CLIMBra: ele guarda a referência da série e a impressão",
        "digital dos valores, e o programa a recompõe da base ao abrir.",
        "",
        "Os casos 10 e 11 abrem com a **Modulação Probabilística** (etapa 13) já",
        "montada: basta ir à etapa 13 e clicar em **Simular**. Os demais têm volume",
        "fixo, com exceção do 02, e por isso a modulação mostra neles só o volume",
        "do estudo.",
        "",
        "| Arquivo | Seção | O que demonstra | Resultado |",
        "| :--- | :--- | :--- | ---: |",
    ]
    for arquivo, _, _, _ in LISTA:
        r = resultados[arquivo]
        if r["modo"] == "varredura":
            valor = (f"volume ideal {br(r['volume_ideal_l'], 0)} L, "
                     f"{br(r['potencial_pct'])}%")
        else:
            valor = f"{br(r['potencial_pct'])}% com {br(r['volume_l'], 0)} L"
        linhas += [f"| `{arquivo}` | {r['capitulo']} | {r['demonstra']} | {valor} |"]
    linhas += [
        "",
        "Os números da última coluna são obtidos **relendo o arquivo gravado** e",
        "simulando o que foi relido. Se um campo não sobreviver ao arquivo, o",
        "número muda e o teste correspondente falha.",
        "",

    ]
    caminho = os.path.join(CASOS, "README.md")
    gravar(caminho, NL.join(linhas))
    return caminho


def escrever_apendice(resultados):
    linhas = [
        "# Arquivos de exemplo",
        "",
        "O manual imprime resultados; estes arquivos são o que se abre para",
        "reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva",
        "incorporada: abrem sem o CSV de origem, em qualquer máquina. A exceção é o",
        "`11_modulacao_climbra.triton`, que usa a chuva da base CLIMBra: ele guarda a",
        "referência da série — cidade, modelo, cenário e recorte — e o programa a recompõe",
        "da base ao abrir.",
        "",
        "---",
        "",
        "## Os casos do manual",
        "",
        "<!-- tabela: Os casos de exemplo e o que cada um demonstra -->",
        "| Arquivo | Seção | O que demonstra |",
        "| :--- | :--- | :--- |",
    ]
    for arquivo, _, _, _ in LISTA:
        r = resultados[arquivo]
        linhas.append(f"| `{arquivo}` | {r['capitulo']} | {r['demonstra']} |")

    linhas += [
        "",
        "## O que cada um produz",
        "",
        "Os valores abaixo são obtidos **relendo o arquivo gravado** e simulando o",
        "que foi relido, e não a configuração que o gerou. É a diferença que",
        "importa: um parâmetro que não sobreviva à gravação aparece aqui como",
        "número errado, em vez de passar despercebido.",
        "",
        "<!-- tabela: Resultado que cada caso de exemplo produz ao ser relido e simulado -->",
        "| Arquivo | Modo | Volume | Potencial | Pluvial consumida |",
        "| :--- | :--- | ---: | ---: | ---: |",
    ]
    for arquivo, _, _, _ in LISTA:
        r = resultados[arquivo]
        if r["modo"] == "varredura":
            vol = f"ideal: {br(r['volume_ideal_l'], 0)} L"
            pluvial = f"{r['volumes_simulados']} volumes"
        else:
            vol = f"{br(r['volume_l'], 0)} L"
            pluvial = f"{br(r['pluvial_l_dia'], 1)} L/dia"
        linhas.append(f"| `{arquivo}` | {r['modo']} | {vol} | "
                      f"{br(r['potencial_pct'])}% | {pluvial} |")

    linhas += [
        "",
        "---",
        "",
        "## Como rodar",
        "",
        "**Arquivo, Abrir projeto**, escolha o arquivo, e o programa carrega tudo: a",
        "chuva, a edificação, os custos e a configuração das análises. Percorra as",
        "etapas de resultado na barra lateral para ver cada dimensão.",
        "",
        "Os casos 10 e 11 abrem com a **Modulação Probabilística** já montada — as",
        "variáveis, as distribuições, os modelos climáticos, o número de realizações e",
        "a semente da seção {{n:43}}: vá à etapa 13 e clique em **Simular**. Os dois estão",
        "em modo varredura, que é o que dá sentido às figuras por volume; num caso de",
        "volume fixo, a ferramenta mostra só o volume do estudo.",
        "",
        "Os arquivos ficam na pasta `casos`, dentro da pasta de instalação do",
        "programa. Se quiser modificá-los, **salve com outro nome**: assim o caso",
        "original continua reproduzindo o número impresso no manual.",
        "",
        "---",
        "",
        "## Os três estudos de `exemplos`",
        "",
        "Além dos casos do manual, o programa traz três estudos de referência em",
        "`exemplos`: residência unifamiliar em Florianópolis, edifício",
        "corporativo em Brasília e escola pública em Manaus. São maiores e menos",
        "didáticos que os do manual, e servem de ponto de partida para projetos",
        "reais.",
        "",
        "> **Eles foram regravados nesta versão.** Estavam num esquema plano",
        "> anterior, que o programa lia sem reconhecer: abriam como projeto",
        "> padrão, com 100 m² e três moradores, e nada avisava. A abertura agora",
        "> recusa formato desconhecido com mensagem própria, e os três foram",
        "> convertidos para o esquema corrente, com a chuva incorporada.",
        "",
        "---",
        "",
        "## O que estes arquivos não são",
        "",
        "Não são gabarito de projeto. São **casos de demonstração**: os custos são",
        "os do tutorial, a tarifa é a da CASAN e a categoria é residencial em",
        "todos, inclusive na escola e no hotel, pela limitação que a seção {{n:36}}",
        "descreve. Para um estudo real, troque tarifa, custos e série de chuva",
        "pelos do seu caso.",
        "",
    ]
    caminho = os.path.join(AQUI, "apendices", "J_arquivos_de_exemplo.md")
    gravar(caminho, NL.join(linhas))
    return caminho


def main():
    print("arquivos de projeto do manual:")
    resultados = gravar_casos()
    print("estudos de examples/, convertidos para o esquema corrente:")
    convertidos = converter_exemplos()
    if not convertidos:
        print("  nenhum: já estavam no esquema corrente")

    with open(os.path.join(CASOS, "resultados.json"), "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(" ", escrever_readme(resultados))
    print(" ", escrever_apendice(resultados))


if __name__ == "__main__":
    main()
