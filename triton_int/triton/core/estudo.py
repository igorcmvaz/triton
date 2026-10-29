# -*- coding: utf-8 -*-
"""Estudos em lote por JSON: organizar, rodar e relatar vários edifícios (``triton estudo``).

Um *estudo* é um arquivo ``estudo.json`` (esquema ``triton-estudo``, versão 1) que reúne, num só lugar,
o projeto base, os casos (edifícios, cidades), o que muda de um caso para o outro (``substituicoes``,
por apelidos amigáveis ou por caminhos do ``.triton``), a análise a rodar e as saídas desejadas.
O motor é o mesmo da linha de comando (``triton.cli.run_analysis``): este módulo só organiza a entrada,
extrai as métricas e escreve tabelas prontas para um artigo (CSV tidy, JSON com proveniência, Markdown,
LaTeX com booktabs, XLSX).

Regras que valem aqui:

* nenhum valor é inventado: campo vazio, ``null`` ou «XX» é «a preencher» e a validação recusa;
* as saídas não levam caminho absoluto, e duas execuções do mesmo estudo dão arquivos iguais
  (a data de execução é a única diferença; ``SOURCE_DATE_EPOCH`` a fixa);
* CSV e JSON têm sempre ponto decimal; Markdown, LaTeX e XLSX seguem o idioma pedido.

O módulo importa ``triton.cli`` só dentro das funções que simulam (a CLI é a camada que já sabe abrir
projetos); a ordem das importações não muda o comportamento das demais edições.
"""

from __future__ import annotations

import copy
import csv
import difflib
import hashlib
import io
import json
import math
import os
import re
import statistics
import tempfile
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

from triton import __version__
from triton.cli_textos import t as _t
from triton.core.edition import (get_current_edition, is_brl_edition, is_ibe_edition, is_int_edition, rotulo_da_edicao,
                                 usa_dados_do_brasil)

ESQUEMA_NOME = "triton-estudo"
ESQUEMA_VERSAO = 1
ESQUEMA_RESULTADOS = "triton-estudo-resultados"
ESQUEMA_CASO = "triton-estudo-caso"
ESQUEMA_COMPARATIVO = "triton-estudo-comparativo"

FORMATOS = ("csv", "json", "md", "tex", "xlsx")
FORMATOS_PADRAO = ("csv", "json", "md", "tex")
TIPOS_DE_ANALISE = ("technical", "economic", "environmental", "topsis", "all")
_NIVEL_DA_ANALISE = {"technical": 0, "economic": 1, "environmental": 2, "topsis": 3, "all": 3}
IDIOMAS = ("auto", "pt", "pt-BR", "pt-PT", "en", "es", "zh")
ORIENTACOES = ("casos_nas_linhas", "metricas_nas_linhas")
_RE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_RE_DATA = re.compile(r"^\d{2}/\d{2}/\d{4}$")
_SEM_DADO = "XX"
_RE_IBGE = re.compile(r"^\d{7}$")
CENARIOS_CLIMBRA = ("HIST", "SSP245", "SSP585")
CHAVES_DO_CLIMBRA = ("municipio", "uf", "ibge", "modelo", "cenario", "inicio", "fim")
CHAVES_DA_TARIFA = ("municipio", "uf", "categoria", "se_ausente")
CHAVES_DA_EXPANSAO = ("municipios", "uf", "modelos", "recortes")


def _m(modelo: str, *args: Any) -> str:
    """Mensagem na língua da edição (``cli_textos.t``), com os argumentos nas posições {0}, {1}…"""
    return _t(modelo).format(*args)


class ErroDeEstudo(ValueError):
    """Estudo inválido; ``erros`` traz todas as mensagens, uma por linha."""

    def __init__(self, erros: Sequence[str]):
        self.erros = list(erros)
        super().__init__(_m("estudo inválido:") + "\n- " + "\n- ".join(self.erros))


# ══ Tipologias: só estrutura e rótulos, nenhum número ═══════════════════════════════════════════

TIPOLOGIAS: Dict[str, Dict[str, Any]] = {
    "escolar": {
        "rotulo": {"pt": "Escolar", "en": "School", "es": "Escolar", "zh": "学校"},
        "sinonimos": ("escola", "escolas", "escolares", "school", "schools", "educacional"),
        "usuarios": ("alunos, professores e funcionários presentes (defina o critério e cite a fonte)",
                     "pupils, teachers and staff present (state the criterion and cite the source)"),
    },
    "comercial": {
        "rotulo": {"pt": "Comercial", "en": "Commercial", "es": "Comercial", "zh": "商业"},
        "sinonimos": ("comercio", "comércio", "escritorio", "escritório", "commercial", "office"),
        "usuarios": ("ocupantes e visitantes (defina o critério e cite a fonte)",
                     "occupants and visitors (state the criterion and cite the source)"),
    },
    "residencial-unifamiliar": {
        "rotulo": {"pt": "Residencial unifamiliar", "en": "Single-family residential",
                   "es": "Residencial unifamiliar", "zh": "独户住宅"},
        "sinonimos": ("unifamiliar", "casa", "single-family", "single_family", "moradia"),
        "usuarios": ("moradores da habitação", "residents of the dwelling"),
    },
    "residencial-multifamiliar": {
        "rotulo": {"pt": "Residencial multifamiliar", "en": "Multi-family residential",
                   "es": "Residencial multifamiliar", "zh": "多户住宅"},
        "sinonimos": ("multifamiliar", "multi-family", "multi_family", "edificio-residencial", "prédio"),
        "usuarios": ("moradores de todas as unidades; o número de unidades vai em «economias»",
                     "residents of all the units; put the number of units in «economias»"),
    },
    "hospitalar": {
        "rotulo": {"pt": "Hospitalar", "en": "Hospital", "es": "Hospitalario", "zh": "医院"},
        "sinonimos": ("hospital", "hospitais", "saude", "saúde", "healthcare"),
        "usuarios": ("pacientes, acompanhantes e equipe (defina o critério e cite a fonte)",
                     "patients, visitors and staff (state the criterion and cite the source)"),
    },
    "aeroportuario": {
        "rotulo": {"pt": "Aeroportuário", "en": "Airport", "es": "Aeroportuario", "zh": "机场"},
        "sinonimos": ("aeroporto", "aeroportos", "airport", "airports", "aeroportuário"),
        "usuarios": ("passageiros e funcionários por dia, em equivalentes (defina o critério e cite a fonte)",
                     "passengers and staff per day, as equivalents (state the criterion and cite the source)"),
    },
}
TIPOLOGIA_OUTRA = "outra"


def tipologia_canonica(valor: Any) -> Optional[str]:
    """O id canônico da tipologia (aceita sinônimos e maiúsculas), ``outra`` ou ``None`` se desconhecida."""
    texto = str(valor or "").strip().lower().replace("_", "-")
    if texto in TIPOLOGIAS or texto == TIPOLOGIA_OUTRA:
        return texto
    for chave, dados in TIPOLOGIAS.items():
        if texto in {s.lower().replace("_", "-") for s in dados["sinonimos"]}:
            return chave
    return None


# ══ Apelidos: nomes amigáveis dos parâmetros ═══════════════════════════════════════════════════
# Cada apelido aponta para campos reais do TritonConfig (os mesmos do .triton). A ordem do dicionário é a
# ordem de aplicação; a demanda total vem por último porque depende do número de usuários.

APELIDOS: Dict[str, Dict[str, Any]] = {
    "area_captacao_m2": dict(sin=("area_m2", "area", "catchment_area_m2"), tipo="float", min=0.0, min_aberto=True,
                             alvos=("area",), un="m²",
                             desc=("Área de captação da cobertura", "Roof catchment area")),
    "coeficiente_escoamento": dict(sin=("coef_escoamento", "runoff_coeff"), tipo="float", min=0.0, max=1.0,
                                   alvos=("runoff_coeff",), un="–",
                                   desc=("Coeficiente de escoamento superficial, de 0 a 1", "Runoff coefficient, 0 to 1")),
    "descarte_mm": dict(sin=("descarte_das_primeiras_aguas_mm", "discard"), tipo="float", min=0.0,
                        alvos=("discard",), un="mm",
                        desc=("Descarte das primeiras águas", "First-flush discard")),
    "usuarios": dict(sin=("populacao", "população", "pessoas", "residentes", "ocupantes", "users", "residents"),
                     tipo="int", min=0, alvos=("residents_count",), un="pessoas",
                     desc=("Número de usuários (moradores, alunos, ocupantes…)", "Number of users (residents, pupils, occupants…)")),
    "demanda_per_capita_l_dia": dict(sin=("consumo_per_capita_l_dia", "per_capita_l_dia", "demand_value"),
                                     tipo="float", min=0.0, alvos=("demand_value",), un="L/pessoa·dia",
                                     desc=("Demanda diária por usuário", "Daily demand per user")),
    "demanda_total_l_dia": dict(sin=("demanda_l_dia", "total_demand_l_day"), tipo="float", min=0.0,
                                alvos=("demand_value",), un="L/dia",
                                desc=("Demanda diária total do edifício (dividida pelos usuários, se informados)",
                                      "Total daily demand of the building (divided by the users, if given)")),
    "fracao_pluvial_pct": dict(sin=("fracao_nao_potavel_pct", "rainwater_share_pct"), tipo="pct",
                               alvos=("rainwater_share",), un="%",
                               desc=("Parcela da demanda que a água de chuva pode atender, em %", "Share of the demand that rainwater may serve, in %")),
    "fracao_pluvial": dict(sin=("rainwater_share",), tipo="fracao", alvos=("rainwater_share",), un="0–1",
                           desc=("A mesma parcela, como fração de 0 a 1", "The same share, as a fraction from 0 to 1")),
    "volume_reservatorio_l": dict(sin=("volume_inferior_l", "lower_tank_fixed"), tipo="float", min=0.0,
                                  alvos=("lower_tank_fixed", "lower_tank_mode"), un="L",
                                  desc=("Volume fixo do reservatório inferior (desliga a varredura)",
                                        "Fixed volume of the lower tank (turns the sweep off)")),
    "volume_maximo_l": dict(sin=("lower_tank_max",), tipo="float", min=0.0, min_aberto=True,
                            alvos=("lower_tank_max", "lower_tank_mode"), un="L",
                            desc=("Maior volume da varredura (liga a varredura)", "Largest volume of the sweep (turns the sweep on)")),
    "passo_volume_l": dict(sin=("lower_tank_step",), tipo="float", min=0.0, min_aberto=True,
                           alvos=("lower_tank_step",), un="L",
                           desc=("Passo da varredura de volumes", "Step of the volume sweep")),
    "reservatorio_superior_l": dict(sin=("upper_tank_vol",), tipo="float", min=0.0,
                                    alvos=("upper_tank_vol", "upper_tank_used"), un="L",
                                    desc=("Volume do reservatório superior (zero o desliga)", "Volume of the upper tank (zero turns it off)")),
    "limiar_bombeamento_l": dict(sin=("pumping_threshold",), tipo="float", min=0.0, alvos=("pumping_threshold",), un="L",
                                 desc=("Limiar de bombeamento", "Pumping threshold")),
    "economias": dict(sin=("unidades", "num_economias"), tipo="int", min=1, alvos=("num_economias",), un="unidades",
                      desc=("Número de economias (unidades) do edifício", "Number of units (dwellings) of the building")),
    "irrigacao_l_dia": dict(sin=("irrigation_liters_per_day",), tipo="float", min=0.0,
                            alvos=("irrigation_liters_per_day",), un="L/dia",
                            desc=("Demanda externa (irrigação, lavagens)", "Outdoor demand (irrigation, washing)")),
    "data_inicio": dict(sin=("start_date",), tipo="data", alvos=("start_date",), un="dd/mm/aaaa",
                        desc=("Data do primeiro dia da série de chuva", "Date of the first day of the rainfall series")),
    "regra_phi": dict(sin=("phi_operation_rule",), tipo="phi", alvos=("phi_operation_rule",), un="0–1",
                      desc=("Regra operacional de Fewkes (φ de 0 a 1) ou «triton»", "Fewkes operating rule (φ from 0 to 1) or «triton»")),
    "delta_ideal_pct": dict(sin=("delta_ideal",), tipo="float", min=0.0, min_aberto=True, alvos=("delta_ideal",), un="%/m³",
                            desc=("Limiar de ganho marginal do volume ideal", "Marginal-gain threshold of the ideal volume")),
    "periodo_analise_anos": dict(sin=("analysis_period_years",), tipo="int", min=1, alvos=("analysis_period_years",), un="anos",
                                 desc=("Período da análise econômica", "Period of the economic analysis")),
    "tma_pct_mes": dict(sin=("tma",), tipo="float", min=0.0, alvos=("tma",), un="% ao mês",
                        desc=("Taxa mínima de atratividade, em % ao mês", "Minimum acceptable rate of return, in % per month")),
    "tarifa_energia": dict(sin=("elec_tariff",), tipo="float", min=0.0, alvos=("elec_tariff",), un="moeda/kWh",
                           desc=("Tarifa de energia elétrica", "Electricity tariff")),
}
_SINONIMO_DE_APELIDO: Dict[str, str] = {}
for _chave, _dados in APELIDOS.items():
    _SINONIMO_DE_APELIDO[_chave] = _chave
    for _s in _dados["sin"]:
        _SINONIMO_DE_APELIDO[_s.lower()] = _chave

#: Seções do arquivo .triton que um caminho pontilhado pode alcançar.
SECOES_DO_TRITON = ("inputs", "rainfall", "ui_state", "analysis", "metadata", "bim_layout")


def campos_do_config() -> Tuple[str, ...]:
    """Campos do projeto que ``--set`` já aceita; valem também como chave de substituição."""
    from triton.cli import CONFIG_OVERRIDES
    return tuple(sorted(CONFIG_OVERRIDES))


# ══ Métricas ═══════════════════════════════════════════════════════════════════════════════════
# (id, origem, chave na origem, unidade, casas decimais, nível mínimo da análise, rótulos pt/en/es/zh, sinônimos)

_M = "moeda"   # a unidade é a moeda do projeto de cada caso


def _met(id_, origem, chave, unidade, casas, nivel, pt, en, es, zh, sin=()):
    return dict(id=id_, origem=origem, chave=chave, unidade=unidade, casas=casas, nivel=nivel,
                rotulos={"pt": pt, "en": en, "es": es, "zh": zh}, sin=tuple(sin))


METRICAS: Dict[str, Dict[str, Any]] = {m["id"]: m for m in (
    _met("area_captacao_m2", "entrada", "area", "m²", 1, 0, "Área de captação", "Catchment area",
         "Área de captación", "集水面积", ("area",)),
    _met("usuarios", "entrada", "usuarios", "pessoas", 0, 0, "Usuários", "Users", "Usuarios", "使用人数",
         ("residents",)),
    _met("demanda_total_l_dia", "entrada", "demanda", "L/dia", 0, 0, "Demanda total", "Total demand",
         "Demanda total", "总需水量"),
    _met("fracao_pluvial_pct", "entrada", "fracao", "%", 1, 0, "Fração atendível por chuva",
         "Rainwater-eligible share", "Fracción atendible con lluvia", "可用雨水比例"),
    _met("chuva_media_anual_mm", "entrada", "chuva_anual", "mm/ano", 0, 0, "Chuva média anual",
         "Mean annual rainfall", "Lluvia media anual", "年均降雨量"),
    _met("dias_da_serie", "entrada", "dias", "dias", 0, 0, "Dias da série de chuva", "Days in the rainfall series",
         "Días de la serie de lluvia", "降雨序列天数"),
    _met("volume_l", "tec", "lower_tank_volume_l", "L", 0, 0, "Volume do reservatório", "Cistern volume",
         "Volumen del depósito", "水箱容积", ("lower_tank_volume_l",)),
    _met("volume_otimo_tecnico_l", "resumo", "optimal_volume_l", "L", 0, 0, "Volume ótimo técnico",
         "Technical optimum volume", "Volumen óptimo técnico", "技术最优容积", ("optimal_volume_l",)),
    _met("economia_agua_potavel_pct", "tec", "potable_savings_pct", "%", 1, 0, "Economia de água potável",
         "Potable water saving", "Ahorro de agua potable", "饮用水节约率", ("potable_savings_pct",)),
    _met("agua_pluvial_m3_ano", "tec", "annual_rainwater_m3", "m³/ano", 1, 0, "Água de chuva aproveitada",
         "Rainwater used", "Agua de lluvia aprovechada", "雨水利用量", ("annual_rainwater_m3",)),
    _met("agua_potavel_m3_ano", "tec", "annual_potable_consumed_m3", "m³/ano", 1, 0, "Água potável consumida",
         "Potable water consumed", "Agua potable consumida", "饮用水消耗量", ("annual_potable_consumed_m3",)),
    _met("extravasamento_m3_ano", "tec", "annual_overflow_m3", "m³/ano", 1, 0, "Extravasamento",
         "Overflow", "Rebose", "溢流量", ("annual_overflow_m3",)),
    _met("dias_atendimento_total_pct", "tec", "full_supply_days_pct", "%", 1, 0, "Dias com atendimento total",
         "Days fully supplied", "Días con abastecimiento total", "完全供水天数占比", ("full_supply_days_pct",)),
    _met("dias_atendimento_parcial_pct", "tec", "partial_supply_days_pct", "%", 1, 0,
         "Dias com atendimento parcial", "Days partly supplied", "Días con abastecimiento parcial",
         "部分供水天数占比", ("partial_supply_days_pct",)),
    _met("dias_sem_atendimento_pct", "tec", "no_supply_days_pct", "%", 1, 0, "Dias sem atendimento",
         "Days without supply", "Días sin abastecimiento", "无供水天数占比", ("no_supply_days_pct",)),
    _met("ganho_marginal_pct_m3", "tec", "marginal_gain_pct_per_m3", "%/m³", 2, 0, "Ganho marginal",
         "Marginal gain", "Ganancia marginal", "边际收益", ("marginal_gain_pct_per_m3",)),
    _met("capex", "eco", "capex_brl", _M, 0, 1, "Investimento (CAPEX)", "Investment (CAPEX)",
         "Inversión (CAPEX)", "投资（CAPEX）", ("capex_brl",)),
    _met("vpl", "eco", "npv_brl", _M, 0, 1, "Valor presente líquido", "Net present value",
         "Valor actual neto", "净现值", ("npv_brl", "vpl", "npv", "val")),
    _met("economia_anual_agua", "eco", "annual_water_savings_brl", _M, 0, 1, "Economia anual na fatura de água",
         "Annual saving on the water bill", "Ahorro anual en la factura de agua", "年度水费节约",
         ("annual_water_savings_brl",)),
    _met("opex_anual", "eco", "annual_opex_brl", _M, 0, 1, "Custo anual de operação (OPEX)", "Annual operating cost (OPEX)",
         "Coste anual de operación (OPEX)", "年运行成本（OPEX）", ("annual_opex_brl",)),
    _met("tir_anual_pct", "eco", "irr_annual_pct", "%", 1, 1, "TIR anual", "Annual IRR", "TIR anual", "年内部收益率",
         ("irr_annual_pct",)),
    _met("payback_descontado_meses", "eco", "discounted_payback_months", "meses", 0, 1, "Payback descontado",
         "Discounted payback", "Payback descontado", "折现回收期", ("discounted_payback_months",)),
    _met("energia_bomba_kwh_ano", "eco", "annual_pump_kwh", "kWh/ano", 1, 1, "Energia de bombeamento",
         "Pumping energy", "Energía de bombeo", "水泵能耗", ("annual_pump_kwh",)),
    _met("co2_incorporado_kg", "amb", "embodied_co2_kg", "kg CO2e", 0, 2, "Carbono incorporado",
         "Embodied carbon", "Carbono incorporado", "隐含碳", ("embodied_co2_kg",)),
    _met("co2_evitado_ano_kg", "amb", "annual_avoided_co2_kg", "kg CO2e/ano", 1, 2, "Emissões evitadas por ano",
         "Emissions avoided per year", "Emisiones evitadas por año", "年减排量", ("annual_avoided_co2_kg",)),
    _met("co2_liquido_vida_kg", "amb", "lifetime_net_co2_saved_kg", "kg CO2e", 0, 2,
         "Emissões líquidas evitadas na vida útil", "Net emissions avoided over the lifespan",
         "Emisiones netas evitadas en la vida útil", "寿命期净减排量", ("lifetime_net_co2_saved_kg",)),
    _met("payback_ambiental_anos", "amb", "environmental_payback_years", "anos", 1, 2, "Payback ambiental",
         "Environmental payback", "Payback ambiental", "环境回收期", ("environmental_payback_years",)),
    _met("volume_topsis_l", "topsis", "best_volume_l", "L", 0, 3, "Volume indicado pelo TOPSIS",
         "Volume ranked first by TOPSIS", "Volumen indicado por TOPSIS", "TOPSIS推荐容积", ("best_volume_l",)),
    _met("indice_topsis", "rank", "score", "–", 3, 3, "Índice TOPSIS do volume", "TOPSIS score of the volume",
         "Índice TOPSIS del volumen", "容积的TOPSIS得分"),
    _met("aceitabilidade_smaa_pct", "smaa", "first_rank_pct", "%", 1, 3, "Aceitabilidade SMAA-VIKOR",
         "SMAA-VIKOR acceptability", "Aceptabilidad SMAA-VIKOR", "SMAA-VIKOR可接受度"),
)}
_SINONIMO_DE_METRICA: Dict[str, str] = {}
for _id, _dados in METRICAS.items():
    _SINONIMO_DE_METRICA[_id] = _id
    for _s in _dados["sin"]:
        _SINONIMO_DE_METRICA[_s.lower()] = _id

#: Métricas que dependem de custos informados: com CAPEX zero, não são resultado (aviso no resumo).
METRICAS_DE_CUSTO = ("capex", "vpl", "opex_anual", "tir_anual_pct", "payback_descontado_meses")

METRICAS_PADRAO = {
    0: ("volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano", "extravasamento_m3_ano"),
    1: ("volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano", "extravasamento_m3_ano", "economia_anual_agua"),
    2: ("volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano", "extravasamento_m3_ano", "economia_anual_agua",
        "co2_liquido_vida_kg"),
    3: ("volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano", "extravasamento_m3_ano", "economia_anual_agua",
        "co2_liquido_vida_kg"),
}


def metrica_canonica(valor: Any) -> Optional[str]:
    return _SINONIMO_DE_METRICA.get(str(valor or "").strip().lower())


# ══ Textos das saídas, em quatro línguas ═══════════════════════════════════════════════════════

_TXT: Dict[str, Dict[str, str]] = {
    "caso": {"pt": "Caso", "en": "Case", "es": "Caso", "zh": "案例"},
    "grupo": {"pt": "Grupo", "en": "Group", "es": "Grupo", "zh": "分组"},
    "metrica": {"pt": "Métrica", "en": "Metric", "es": "Métrica", "zh": "指标"},
    "minimo": {"pt": "Mínimo", "en": "Minimum", "es": "Mínimo", "zh": "最小值"},
    "mediana": {"pt": "Mediana", "en": "Median", "es": "Mediana", "zh": "中位数"},
    "media": {"pt": "Média", "en": "Mean", "es": "Media", "zh": "平均值"},
    "maximo": {"pt": "Máximo", "en": "Maximum", "es": "Máximo", "zh": "最大值"},
    "n": {"pt": "n", "en": "n", "es": "n", "zh": "n"},
    "tipologia": {"pt": "Tipologia", "en": "Typology", "es": "Tipología", "zh": "类型"},
    "resumo": {"pt": "Resumo do estudo", "en": "Study summary", "es": "Resumen del estudio", "zh": "研究摘要"},
    "casos": {"pt": "Casos", "en": "Cases", "es": "Casos", "zh": "案例数"},
    "rodados": {"pt": "calculados", "en": "computed", "es": "calculados", "zh": "已计算"},
    "com_erro": {"pt": "com erro", "en": "with errors", "es": "con errores", "zh": "出错"},
    "pendentes": {"pt": "pendentes", "en": "pending", "es": "pendientes", "zh": "待处理"},
    "analise": {"pt": "Análise", "en": "Analysis", "es": "Análisis", "zh": "分析"},
    "volume_criterio": {"pt": "Volume de cada caso", "en": "Volume of each case", "es": "Volumen de cada caso",
                        "zh": "各案例的容积"},
    "crit_otimo_tecnico": {"pt": "ótimo técnico", "en": "technical optimum", "es": "óptimo técnico", "zh": "技术最优"},
    "crit_topsis": {"pt": "primeiro do TOPSIS", "en": "first by TOPSIS", "es": "primero según TOPSIS", "zh": "TOPSIS第一名"},
    "crit_fixo": {"pt": "volume fixo informado", "en": "fixed volume given", "es": "volumen fijo indicado", "zh": "指定的固定容积"},
    "faixa": {"pt": "Faixa dos resultados (mínimo a máximo)", "en": "Range of the results (minimum to maximum)",
              "es": "Rango de los resultados (mínimo a máximo)", "zh": "结果范围（最小值至最大值）"},
    "fontes": {"pt": "Fontes da chuva e licenças", "en": "Rainfall sources and licences",
               "es": "Fuentes de la lluvia y licencias", "zh": "降雨数据来源与许可"},
    "avisos": {"pt": "Avisos", "en": "Warnings", "es": "Avisos", "zh": "提示"},
    "gerado": {"pt": "Gerado por", "en": "Generated by", "es": "Generado por", "zh": "生成工具"},
    "edicao": {"pt": "edição", "en": "edition", "es": "edición", "zh": "版本"},
    "arquivos": {"pt": "Tabelas e dados", "en": "Tables and data", "es": "Tablas y datos", "zh": "表格与数据"},
    "falhas": {"pt": "Casos com erro", "en": "Cases with errors", "es": "Casos con errores", "zh": "出错的案例"},
    "sem_custos": {"pt": "Custos não informados em {0}: CAPEX igual a zero; VPL, TIR e payback não são resultados.",
                   "en": "Costs not entered in {0}: CAPEX is zero; NPV, IRR and payback are not results.",
                   "es": "Costes no informados en {0}: CAPEX igual a cero; VAN, TIR y payback no son resultados.",
                   "zh": "{0} 未输入成本：CAPEX 为零；净现值、内部收益率和回收期不是有效结果。"},
    "moedas_mistas": {"pt": "Os casos usam moedas diferentes ({0}): valores monetários não são comparáveis nem agregados.",
                      "en": "The cases use different currencies ({0}): monetary values are neither comparable nor aggregated.",
                      "es": "Los casos usan monedas distintas ({0}): los valores monetarios no son comparables ni se agregan.",
                      "zh": "各案例使用不同货币（{0}）：货币数值不可比较，也不汇总。"},
    "eobs": {"pt": "A E-OBS só pode ser usada em pesquisa e educação não comerciais.",
             "en": "E-OBS may only be used for non-commercial research and education.",
             "es": "E-OBS solo puede usarse en investigación y educación no comerciales.",
             "zh": "E-OBS 仅可用于非商业的研究和教育。"},
    "moeda_nd": {"pt": "moeda não declarada", "en": "currency not declared", "es": "moneda no declarada",
                 "zh": "未声明货币"},
    "tabela_de": {"pt": "Resultados do estudo", "en": "Results of the study", "es": "Resultados del estudio",
                  "zh": "研究结果"},
    "comparativo": {"pt": "Comparativo entre tipologias", "en": "Comparison between typologies",
                    "es": "Comparación entre tipologías", "zh": "类型之间的比较"},
    "media_faixa": {"pt": "média (mínimo a máximo)", "en": "mean (minimum to maximum)",
                    "es": "media (mínimo a máximo)", "zh": "平均值（最小值至最大值）"},
    "estudos": {"pt": "Estudos", "en": "Studies", "es": "Estudios", "zh": "研究数"},
}


def resolver_idioma(valor: Any = "auto") -> str:
    """Idioma das saídas: ``pt-BR``, ``pt-PT``, ``en``, ``es`` ou ``zh``. ``auto`` segue a edição (BRL pt-BR, IBE pt-PT, INT en)."""
    texto = str(valor or "auto").strip()
    baixo = texto.lower()
    if baixo in ("", "auto"):
        return "en" if is_int_edition() else ("pt-PT" if is_ibe_edition() else "pt-BR")
    if baixo in ("pt", "pt-br", "pt_br"):
        return "pt-PT" if (baixo == "pt" and is_ibe_edition()) else "pt-BR"
    if baixo in ("pt-pt", "pt_pt"):
        return "pt-PT"
    if baixo in ("en", "en-gb", "en-us"):
        return "en"
    if baixo in ("es", "zh"):
        return baixo
    raise ValueError(_m("idioma desconhecido: {0}. Use auto, pt-BR, pt-PT, en, es ou zh.", texto))


def _lingua(idioma: str) -> str:
    return "pt" if idioma.startswith("pt") else idioma


def _txt(chave: str, idioma: str, *args: Any) -> str:
    texto = _TXT[chave][_lingua(idioma)]
    if idioma == "pt-PT":
        from triton.cli_textos import em_portugues_de_portugal
        texto = em_portugues_de_portugal(texto)
    return texto.format(*args) if args else texto


def rotulo_da_metrica(metrica: str, idioma: str) -> str:
    texto = METRICAS[metrica]["rotulos"][_lingua(idioma)]
    if idioma == "pt-PT":
        from triton.cli_textos import em_portugues_de_portugal
        texto = em_portugues_de_portugal(texto)
    return texto


def rotulo_da_tipologia(tipologia: str, idioma: str) -> str:
    if tipologia in TIPOLOGIAS:
        return TIPOLOGIAS[tipologia]["rotulo"][_lingua(idioma)]
    return {"pt": "Outra", "en": "Other", "es": "Otra", "zh": "其他"}[_lingua(idioma)]


def formatar_numero(valor: Any, casas: int, idioma: str, milhar: bool = True) -> Optional[str]:
    """O número no formato do idioma: vírgula decimal em pt/es, ponto em en/zh. ``None`` se não for número."""
    if valor is None or isinstance(valor, bool):
        return None
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(v):
        return None
    arredondado = round(v, casas)
    if arredondado == 0:
        arredondado = 0.0   # sem «-0,0»
    texto = f"{arredondado:,.{casas}f}" if milhar else f"{arredondado:.{casas}f}"
    if _lingua(idioma) in ("pt", "es"):
        texto = texto.replace(",", "\0").replace(".", ",").replace("\0", ".")
    return texto


# ══ Utilidades de arquivos e de texto ══════════════════════════════════════════════════════════

def sha256_do_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _json_texto(valor: Any) -> str:
    return json.dumps(valor, ensure_ascii=False, indent=2) + "\n"


def _escrever(caminho: Path, texto: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def _num_limpo(v: Any) -> Any:
    """Número para CSV/JSON: sem ruído de ponto flutuante (10 algarismos significativos) e sem NaN."""
    if v is None or isinstance(v, bool):
        return v
    try:
        x = float(v)
    except (TypeError, ValueError):
        return v
    if not math.isfinite(x):
        return None
    return float(f"{x:.10g}")


def _relativo(caminho: Path, base: Path) -> str:
    """Caminho relativo à pasta do estudo, com barras normais; sem caminho absoluto (só o nome, se não houver relativo)."""
    try:
        return Path(os.path.relpath(Path(caminho).resolve(), Path(base).resolve())).as_posix()
    except ValueError:      # outro disco no Windows
        return Path(caminho).name


_RE_ABSOLUTO = re.compile(r"(?:[A-Za-z]:[\\/][^\s'\"<>|]*|(?<![\w.])/(?:home|Users|tmp|var|private|mnt|root|opt)/[^\s'\"<>|]*)")


def limpar_caminhos(texto: str, *bases: Path) -> str:
    """Troca por nomes relativos os caminhos absolutos de uma mensagem (as saídas não levam o caminho da máquina)."""
    texto = str(texto)
    for b in bases:
        for variante in {str(Path(b)), str(Path(b).resolve()), Path(b).resolve().as_posix()}:
            texto = texto.replace(variante + os.sep, "").replace(variante + "/", "").replace(variante, ".")
    return _RE_ABSOLUTO.sub(lambda m: Path(m.group(0).replace("\\", "/")).name, texto)


def data_de_execucao() -> str:
    """Data (AAAA-MM-DD, UTC) da execução; ``SOURCE_DATE_EPOCH`` a fixa, para saídas reproduzíveis byte a byte."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH", "").strip()
    try:
        instante = datetime.fromtimestamp(int(epoch), tz=timezone.utc) if epoch else datetime.now(timezone.utc)
    except (ValueError, OverflowError, OSError):
        instante = datetime.now(timezone.utc)
    return instante.date().isoformat()


def _pendente(v: Any) -> bool:
    """Campo a preencher: vazio, ``null`` ou «XX»."""
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip().strip("«»").strip().upper() in ("", _SEM_DADO)
    return False


def _sugestao(chave: str, opcoes: Iterable[str]) -> str:
    perto = difflib.get_close_matches(str(chave).lower(), [o.lower() for o in opcoes], n=1, cutoff=0.6)
    if not perto:
        return ""
    for o in opcoes:
        if o.lower() == perto[0]:
            return _m(" Quis dizer «{0}»?", o)
    return ""


# ══ Validação do esquema ═══════════════════════════════════════════════════════════════════════

def _eh_numero(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def validar_valor_de_apelido(chave: str, valor: Any) -> Any:
    """Confere e normaliza o valor de um apelido (ou campo). Levanta ``ValueError`` com a razão."""
    dados = APELIDOS[chave]
    tipo = dados["tipo"]
    if _pendente(valor):
        raise ValueError(_m("ainda não preenchido (use um número; «XX» e null são lacunas)"))
    if tipo in ("float", "int", "pct", "fracao"):
        if not _eh_numero(valor):
            raise ValueError(_m("esperado um número, recebido {0!r}", valor))
        v = float(valor)
        if tipo == "int":
            if abs(v - round(v)) > 1e-9:
                raise ValueError(_m("esperado um inteiro, recebido {0}", valor))
            v = int(round(v))
        if tipo == "pct" and not 0.0 <= v <= 100.0:
            raise ValueError(_m("percentual fora de [0, 100]: {0}", valor))
        if tipo == "fracao":
            if 1.0 < v <= 100.0:
                raise ValueError(_m("{0} parece um percentual; aqui a fração vai de 0 a 1 (0,4 é 40%); para percentual use fracao_pluvial_pct", valor))
            if not 0.0 <= v <= 1.0:
                raise ValueError(_m("fração fora de [0, 1]: {0}", valor))
        minimo, maximo = dados.get("min"), dados.get("max")
        if minimo is not None and (v <= minimo if dados.get("min_aberto") else v < minimo):
            raise ValueError(_m("deve ser {0} {1}, recebido {2}", ">" if dados.get("min_aberto") else "≥", minimo, valor))
        if maximo is not None and v > maximo:
            raise ValueError(_m("deve ser no máximo {0}, recebido {1}", maximo, valor))
        return v
    if tipo == "data":
        if not isinstance(valor, str) or not _RE_DATA.match(valor.strip()):
            raise ValueError(_m("esperada uma data dd/mm/aaaa, recebido {0!r}", valor))
        try:
            datetime.strptime(valor.strip(), "%d/%m/%Y")
        except ValueError:
            raise ValueError(_m("data inexistente: {0}", valor)) from None
        return valor.strip()
    if tipo == "phi":
        if isinstance(valor, str):
            if valor.strip().lower() == "triton":
                return None
            raise ValueError(_m("regra_phi aceita um número de 0 a 1 ou «triton»"))
        if not _eh_numero(valor) or not 0.0 <= float(valor) <= 1.0:
            raise ValueError(_m("regra_phi aceita um número de 0 a 1 ou «triton»"))
        return float(valor)
    raise ValueError("tipo desconhecido")  # pragma: no cover


def classificar_chave(chave: str) -> Tuple[str, str]:
    """(tipo, nome canônico) de uma chave de substituição: ``apelido``, ``campo``, ``caminho`` ou ``desconhecida``."""
    baixo = str(chave).strip().lower()
    if baixo in _SINONIMO_DE_APELIDO:
        return "apelido", _SINONIMO_DE_APELIDO[baixo]
    if "." in str(chave):
        primeiro = str(chave).split(".", 1)[0]
        if primeiro == "config":
            resto = str(chave).split(".", 1)[1]
            return ("campo", resto) if resto in campos_do_config() else ("desconhecida", chave)
        return ("caminho", str(chave)) if primeiro in SECOES_DO_TRITON else ("desconhecida", chave)
    if str(chave) in campos_do_config():
        return "campo", str(chave)
    return "desconhecida", str(chave)


def _erro_de_chave(chave: str) -> str:
    opcoes = list(APELIDOS) + list(campos_do_config())
    if "." in chave:
        return _m("caminho desconhecido «{0}»: um caminho pontilhado começa por uma seção do .triton ({1}) ou por config.<campo>",
                  chave, ", ".join(SECOES_DO_TRITON))
    return (_m("apelido desconhecido «{0}».", chave) + _sugestao(chave, opcoes)
            + " " + _m("Apelidos: {0}. Veja também «triton estudo apelidos».", ", ".join(APELIDOS)))


def _validar_chaves(obj: Any, permitidas: Sequence[str], caminho: str, erros: List[str]) -> bool:
    if not isinstance(obj, dict):
        erros.append(_m("{0}: esperado um objeto JSON", caminho))
        return False
    for k in obj:
        if str(k).startswith("_"):
            continue
        if k not in permitidas:
            erros.append(_m("{0}: chave desconhecida «{1}».", caminho, k) + _sugestao(k, permitidas)
                         + " " + _m("Chaves aceitas: {0}", ", ".join(permitidas)))
    return True


def _validar_substituicoes(sub: Any, caminho: str, erros: List[str]) -> Dict[str, Any]:
    """Valida o dicionário de substituições e devolve ``{chave canônica: valor normalizado}`` (só as válidas)."""
    saida: Dict[str, Any] = {}
    if not isinstance(sub, dict):
        erros.append(_m("{0}: esperado um objeto JSON", caminho))
        return saida
    alvos: Dict[str, str] = {}
    for chave, valor in sub.items():
        if str(chave).startswith("_"):
            continue
        tipo, canon = classificar_chave(chave)
        onde = f"{caminho}.{chave}"
        if tipo == "desconhecida":
            erros.append(f"{onde}: " + _erro_de_chave(str(chave)))
            continue
        try:
            if tipo == "apelido":
                novo = validar_valor_de_apelido(canon, valor)
                meus_alvos = APELIDOS[canon]["alvos"]
            elif tipo == "campo":
                if _pendente(valor):
                    raise ValueError(_m("ainda não preenchido (use um número; «XX» e null são lacunas)"))
                novo, meus_alvos = valor, (canon,)
            else:
                if _pendente(valor):
                    raise ValueError(_m("ainda não preenchido (use um número; «XX» e null são lacunas)"))
                novo, meus_alvos = valor, (canon,)
        except ValueError as exc:
            erros.append(f"{onde}: {exc}")
            continue
        repetido = [a for a in meus_alvos if a in alvos]
        if canon in saida or repetido:
            outro = alvos.get(repetido[0]) if repetido else canon
            erros.append(_m("{0}: «{1}» e «{2}» definem o mesmo parâmetro; informe só um deles", onde, chave, outro))
            continue
        for a in meus_alvos:
            alvos[a] = str(chave)
        saida[canon if tipo == "apelido" else f"{'campo' if tipo == 'campo' else 'caminho'}:{canon}"] = novo
    if "demanda_total_l_dia" in saida and "demanda_per_capita_l_dia" in saida:
        pass   # já coberto pelo alvo repetido
    return saida


def _so_brasil(caminho: str, erros: List[str]) -> bool:
    """As referências ao CLIMBra e ao catálogo de tarifas são da Edição Brasil; fora dela a validação as recusa."""
    if usa_dados_do_brasil():
        return True
    erros.append(_m("{0}: o CLIMBra e o catálogo de tarifas municipais só existem na Edição Brasil; use «arquivo» com a série de chuva", caminho))
    return False


def _validar_climbra(ref: Any, caminho: str, erros: List[str]) -> Dict[str, Any]:
    """``clima.climbra``: município, UF, modelo, cenário e recorte da base CLIMBra (resolvidos na execução)."""
    if not _so_brasil(caminho, erros) or not _validar_chaves(ref, CHAVES_DO_CLIMBRA, caminho, erros):
        return {}
    from triton.core.climate_database import CLIMATE_MODELS
    saida: Dict[str, Any] = {}
    for k in ("municipio", "uf", "modelo", "cenario", "ibge", "inicio", "fim"):
        if k not in ref:
            continue
        v = ref[k]
        if _pendente(v):
            erros.append(_m("{0}.{1}: ainda não preenchido", caminho, k))
        elif not isinstance(v, str):
            erros.append(_m("{0}.{1}: esperado texto", caminho, k))
        elif k == "modelo" and v not in CLIMATE_MODELS:
            erros.append(_m("{0}.modelo: «{1}» desconhecido. Use: {2}", caminho, v, ", ".join(CLIMATE_MODELS)) + _sugestao(v, CLIMATE_MODELS))
        elif k == "cenario" and v not in CENARIOS_CLIMBRA:
            erros.append(_m("{0}.cenario: «{1}» desconhecido. Use: {2}", caminho, v, ", ".join(CENARIOS_CLIMBRA)))
        elif k == "ibge" and not _RE_IBGE.match(v.strip()):
            erros.append(_m("{0}.ibge: esperado o código IBGE de sete dígitos, entre aspas", caminho))
        elif k in ("inicio", "fim"):
            try:
                saida[k] = validar_valor_de_apelido("data_inicio", v)
            except ValueError as exc:
                erros.append(f"{caminho}.{k}: {exc}")
        else:
            saida[k] = v.strip()
    return saida


def _validar_tarifa(tar: Any, caminho: str, erros: List[str]) -> Dict[str, Any]:
    """``tarifa``: o município (e a categoria) do catálogo de tarifas do programa; sem preços digitados."""
    if not _so_brasil(caminho, erros) or not _validar_chaves(tar, CHAVES_DA_TARIFA, caminho, erros):
        return {}
    from triton.core.tariffs_database import CATEGORIAS_TARIFARIAS
    saida: Dict[str, Any] = {}
    for k in CHAVES_DA_TARIFA:
        if k not in tar:
            continue
        v = tar[k]
        if _pendente(v):
            erros.append(_m("{0}.{1}: ainda não preenchido", caminho, k))
        elif not isinstance(v, str):
            erros.append(_m("{0}.{1}: esperado texto", caminho, k))
        elif k == "categoria" and v.strip().lower() not in CATEGORIAS_TARIFARIAS:
            erros.append(_m("{0}.categoria: «{1}» desconhecida. Use: {2}", caminho, v, ", ".join(CATEGORIAS_TARIFARIAS)))
        elif k == "se_ausente" and v.strip().lower() not in ("erro", "residencial"):
            erros.append(_m("{0}.se_ausente: use «erro» ou «residencial»", caminho))
        else:
            saida[k] = v.strip().lower() if k in ("categoria", "se_ausente") else v.strip()
    return saida


def _validar_clima(clima: Any, caminho: str, erros: List[str]) -> Dict[str, Any]:
    if clima is None:
        return {}
    if not _validar_chaves(clima, ("arquivo", "climbra", "data_inicio", "nome", "fonte"), caminho, erros):
        return {}
    saida: Dict[str, Any] = {}
    for k in ("arquivo", "nome", "fonte"):
        if k in clima:
            if _pendente(clima[k]):
                erros.append(_m("{0}.{1}: ainda não preenchido", caminho, k))
            elif not isinstance(clima[k], str):
                erros.append(_m("{0}.{1}: esperado texto", caminho, k))
            else:
                saida[k] = clima[k].strip()
    if "climbra" in clima:
        if "arquivo" in clima:
            erros.append(_m("{0}: informe «{1}» ou «{2}», não os dois", caminho, "arquivo", "climbra"))
        else:
            ref = _validar_climbra(clima["climbra"], f"{caminho}.climbra", erros)
            if ref:
                saida["climbra"] = ref
    if "data_inicio" in clima:
        try:
            saida["data_inicio"] = validar_valor_de_apelido("data_inicio", clima["data_inicio"])
        except ValueError as exc:
            erros.append(f"{caminho}.data_inicio: {exc}")
    return saida


def _fundir_blocos(padrao: Dict[str, Any], caso: Dict[str, Any], excludentes: Sequence[Tuple[str, str]] = ()) -> Dict[str, Any]:
    """Fusão de um bloco (clima, tarifa): o caso vence; ``climbra`` e ``tarifa`` se completam campo a campo.

    ``excludentes``: pares (a, b) em que informar um no caso descarta o outro vindo dos padrões (arquivo × climbra).
    """
    base = dict(padrao)
    for a, b in excludentes:
        if a in caso:
            base.pop(b, None)
        if b in caso:
            base.pop(a, None)
    saida = {**base, **caso}
    for k, v in caso.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            saida[k] = {**base[k], **v}
    return saida


def _metricas_da_analise(nivel: int) -> Tuple[str, ...]:
    return METRICAS_PADRAO[nivel]


def validar_documento(doc: Any, base_dir: Optional[Path] = None, verificar_arquivos: bool = True
                      ) -> Tuple[Optional[Dict[str, Any]], List[str], List[str]]:
    """Valida o ``estudo.json`` já lido. Devolve ``(plano, erros, avisos)``; o plano é ``None`` se há erros."""
    erros: List[str] = []
    avisos: List[str] = []
    if not isinstance(doc, dict):
        return None, [_m("o estudo deve ser um objeto JSON")], avisos
    _validar_chaves(doc, ("esquema", "estudo", "projeto_base", "padroes", "casos", "expansao", "analise", "saidas"), "$", erros)

    # esquema
    esq = doc.get("esquema")
    if not isinstance(esq, dict) or esq.get("nome") != ESQUEMA_NOME:
        erros.append(_m("esquema: esperado {{\"nome\": \"{0}\", \"versao\": {1}}}", ESQUEMA_NOME, ESQUEMA_VERSAO))
    elif esq.get("versao") != ESQUEMA_VERSAO:
        erros.append(_m("esquema.versao: a versão {0!r} não é suportada; esta edição do Triton lê a versão {1}",
                        esq.get("versao"), ESQUEMA_VERSAO))

    # estudo
    est = doc.get("estudo")
    meta: Dict[str, Any] = {"id": "", "titulo": "", "tipologia": TIPOLOGIA_OUTRA, "autores": [], "nota": ""}
    if _validar_chaves(est, ("id", "titulo", "tipologia", "tipologia_rotulo", "autores", "nota"), "estudo", erros):
        eid = est.get("id")
        if not isinstance(eid, str) or not _RE_ID.match(eid):
            erros.append(_m("estudo.id: obrigatório, só letras, números, ponto, hífen e sublinhado (até 64 caracteres)"))
        else:
            meta["id"] = eid
        titulo = est.get("titulo", "")
        if _pendente(titulo):
            avisos.append(_m("estudo.titulo: ainda não preenchido"))
        elif not isinstance(titulo, str):
            erros.append(_m("estudo.titulo: esperado texto"))
        meta["titulo"] = titulo if isinstance(titulo, str) else ""
        canon = tipologia_canonica(est.get("tipologia"))
        if canon is None:
            erros.append(_m("estudo.tipologia: «{0}» desconhecida. Use: {1} ou outra.", est.get("tipologia"), ", ".join(TIPOLOGIAS))
                         + _sugestao(str(est.get("tipologia")), list(TIPOLOGIAS)))
        else:
            meta["tipologia"] = canon
        meta["tipologia_rotulo"] = str(est.get("tipologia_rotulo", "") or "")
        autores = est.get("autores", [])
        if not isinstance(autores, list) or not all(isinstance(a, str) for a in autores):
            erros.append(_m("estudo.autores: esperada uma lista de textos"))
        else:
            meta["autores"] = [a for a in autores if not _pendente(a)]
        meta["nota"] = str(est.get("nota", "") or "")
    elif est is None:
        pass

    # projeto base
    base: Dict[str, Any] = {}
    base_pendente = False
    pb = doc.get("projeto_base")
    if pb is not None:
        if _validar_chaves(pb, ("arquivo", "modelo"), "projeto_base", erros):
            if "arquivo" in pb and "modelo" in pb:
                erros.append(_m("{0}: informe «{1}» ou «{2}», não os dois", "projeto_base", "arquivo", "modelo"))
            elif "arquivo" in pb:
                if _pendente(pb["arquivo"]):
                    base_pendente = True
                    erros.append(_m("{0}: ainda não preenchido", "projeto_base.arquivo"))
                elif not isinstance(pb["arquivo"], str):
                    erros.append(_m("{0}: esperado texto", "projeto_base.arquivo"))
                else:
                    base["arquivo"] = pb["arquivo"].strip()
            elif "modelo" in pb:
                if pb["modelo"] != "edicao":
                    erros.append(_m("projeto_base.modelo: o único modelo é «edicao» (o modelo de projeto da edição, como «triton init»)"))
                else:
                    base["modelo"] = "edicao"
            else:
                erros.append(_m("{0}: informe «{1}» (um .triton) ou «{2}»", "projeto_base", "arquivo", "modelo"))

    # padrões
    padroes: Dict[str, Any] = {"substituicoes": {}, "clima": {}, "tarifa": {}}
    pd_ = doc.get("padroes")
    if pd_ is not None and _validar_chaves(pd_, ("substituicoes", "clima", "tarifa"), "padroes", erros):
        padroes["substituicoes"] = _validar_substituicoes(pd_.get("substituicoes", {}), "padroes.substituicoes", erros)
        padroes["clima"] = _validar_clima(pd_.get("clima"), "padroes.clima", erros)
        if pd_.get("tarifa") is not None:
            padroes["tarifa"] = _validar_tarifa(pd_["tarifa"], "padroes.tarifa", erros)

    # análise
    analise = {"tipo": "technical", "volume": "otimo_tecnico", "pesos": None, "semente": 42}
    an = doc.get("analise")
    if an is not None and _validar_chaves(an, ("tipo", "volume", "pesos", "semente"), "analise", erros):
        tipo = an.get("tipo", "technical")
        if tipo not in TIPOS_DE_ANALISE:
            erros.append(_m("analise.tipo: «{0}» desconhecido. Use: {1}", tipo, ", ".join(TIPOS_DE_ANALISE)))
        else:
            analise["tipo"] = tipo
        vol = an.get("volume", "otimo_tecnico")
        if vol in ("otimo_tecnico", "topsis"):
            analise["volume"] = vol
        elif _eh_numero(vol) and float(vol) >= 0:
            analise["volume"] = float(vol)
        else:
            erros.append(_m("analise.volume: use «otimo_tecnico», «topsis» ou um volume em litros (número ≥ 0)"))
        if an.get("pesos") is not None:
            pesos = an["pesos"]
            if (not isinstance(pesos, list) or len(pesos) != 3 or not all(_eh_numero(p) and p >= 0 for p in pesos)
                    or sum(pesos) <= 0):
                erros.append(_m("analise.pesos: três números não negativos (técnico, econômico, ambiental), com soma positiva"))
            else:
                analise["pesos"] = [float(p) for p in pesos]
        sem = an.get("semente", 42)
        if not isinstance(sem, int) or isinstance(sem, bool):
            erros.append(_m("analise.semente: esperado um inteiro"))
        else:
            analise["semente"] = sem
    if analise["volume"] == "topsis" and _NIVEL_DA_ANALISE.get(analise["tipo"], 0) < 3:
        erros.append(_m("analise.volume = «topsis» exige analise.tipo = «all» (ou «topsis»)"))
    nivel = _NIVEL_DA_ANALISE.get(analise["tipo"], 0)

    # saídas
    saidas: Dict[str, Any] = {"formatos": list(FORMATOS_PADRAO), "metricas": None, "casas_decimais": {},
                              "idioma": "auto", "milhar": True, "legenda": "", "orientacao": "casos_nas_linhas",
                              "gravar_analise": True}
    sd = doc.get("saidas")
    if sd is not None and _validar_chaves(sd, ("formatos", "metricas", "casas_decimais", "idioma", "milhar", "legenda", "orientacao",
                                           "gravar_analise"), "saidas", erros):
        if "gravar_analise" in sd:
            if isinstance(sd["gravar_analise"], bool):
                saidas["gravar_analise"] = sd["gravar_analise"]
            else:
                erros.append(_m("saidas.gravar_analise: esperado verdadeiro ou falso"))
        if "formatos" in sd:
            fm = sd["formatos"]
            if not isinstance(fm, list) or not fm or not all(isinstance(f, str) for f in fm):
                erros.append(_m("saidas.formatos: lista não vazia com {0}", ", ".join(FORMATOS)))
            else:
                ruins = [f for f in fm if f.lower() not in FORMATOS]
                if ruins:
                    erros.append(_m("saidas.formatos: formato desconhecido «{0}». Use: {1}", ruins[0], ", ".join(FORMATOS))
                                 + _sugestao(ruins[0], FORMATOS))
                else:
                    saidas["formatos"] = list(dict.fromkeys(f.lower() for f in fm))
        if "metricas" in sd:
            ms = sd["metricas"]
            if not isinstance(ms, list) or not ms or not all(isinstance(x, str) for x in ms):
                erros.append(_m("saidas.metricas: lista não vazia de métricas (veja «triton estudo apelidos»)"))
            else:
                canon_ms: List[str] = []
                for x in ms:
                    c = metrica_canonica(x)
                    if c is None:
                        erros.append(_m("saidas.metricas: métrica desconhecida «{0}».", x) + _sugestao(x, list(METRICAS))
                                     + " " + _m("Métricas: {0}", ", ".join(METRICAS)))
                    elif METRICAS[c]["nivel"] > nivel:
                        erros.append(_m("saidas.metricas: «{0}» exige analise.tipo «{1}» ou mais completo; o estudo executa «{2}»",
                                        c, {1: "economic", 2: "environmental", 3: "all"}[METRICAS[c]["nivel"]], analise["tipo"]))
                    elif c not in canon_ms:
                        canon_ms.append(c)
                saidas["metricas"] = canon_ms
        if saidas["metricas"] is None:
            saidas["metricas"] = list(_metricas_da_analise(nivel))
        cd = sd.get("casas_decimais", {})
        if isinstance(cd, int) and not isinstance(cd, bool) and 0 <= cd <= 8:
            saidas["casas_decimais"] = {"padrao": cd}
        elif isinstance(cd, dict):
            novo: Dict[str, int] = {}
            for k, v in cd.items():
                if str(k).startswith("_"):
                    continue
                alvo = "padrao" if k == "padrao" else metrica_canonica(k)
                if alvo is None:
                    erros.append(_m("saidas.casas_decimais: métrica desconhecida «{0}».", k) + _sugestao(k, list(METRICAS)))
                elif not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 8:
                    erros.append(_m("saidas.casas_decimais.{0}: inteiro de 0 a 8", k))
                else:
                    novo[alvo] = v
            saidas["casas_decimais"] = novo
        else:
            erros.append(_m("saidas.casas_decimais: inteiro de 0 a 8 ou objeto {{métrica: casas}}"))
        idioma = sd.get("idioma", "auto")
        if idioma not in IDIOMAS:
            erros.append(_m("saidas.idioma: «{0}» desconhecido. Use: {1}", idioma, ", ".join(IDIOMAS)))
        else:
            saidas["idioma"] = idioma
        if "milhar" in sd:
            if isinstance(sd["milhar"], bool):
                saidas["milhar"] = sd["milhar"]
            else:
                erros.append(_m("saidas.milhar: esperado verdadeiro ou falso"))
        saidas["legenda"] = str(sd.get("legenda", "") or "")
        ori = sd.get("orientacao", "casos_nas_linhas")
        if ori not in ORIENTACOES:
            erros.append(_m("saidas.orientacao: use {0}", " ou ".join(ORIENTACOES)))
        else:
            saidas["orientacao"] = ori
    else:
        saidas["metricas"] = list(_metricas_da_analise(nivel))

    # casos
    casos_plano: List[Dict[str, Any]] = []
    casos = doc.get("casos")
    if casos is None and doc.get("expansao") is not None:
        casos = []
    if not isinstance(casos, list) or (not casos and doc.get("expansao") is None):
        erros.append(_m("casos: lista não vazia de casos"))
        casos = []
    if doc.get("expansao") is not None:
        casos = list(casos) + expandir_casos(doc["expansao"], "expansao", erros)
        if not casos:
            erros.append(_m("expansao: não gerou nenhum caso"))
    vistos: Dict[str, int] = {}
    for i, caso in enumerate(casos):
        onde = f"casos[{i}]"
        if not _validar_chaves(caso, ("id", "nome", "grupo", "projeto", "clima", "tarifa", "substituicoes", "dimensoes"), onde, erros):
            continue
        cid = caso.get("id")
        if not isinstance(cid, str) or not _RE_ID.match(cid):
            erros.append(_m("{0}.id: obrigatório, só letras, números, ponto, hífen e sublinhado (até 64 caracteres)", onde))
            continue
        onde = f"casos[{i}] ({cid})"
        if cid.lower() in vistos:
            erros.append(_m("{0}: id repetido (igual ao do caso {1})", onde, vistos[cid.lower()]))
            continue
        vistos[cid.lower()] = i
        nome = caso.get("nome", cid)
        if _pendente(nome):
            avisos.append(_m("{0}.nome: ainda não preenchido (usado: {1})", onde, cid))
            nome = cid
        grupo = caso.get("grupo", meta["tipologia"])
        if _pendente(grupo):
            grupo = meta["tipologia"]
        projeto = caso.get("projeto")
        if projeto is not None and (_pendente(projeto) or not isinstance(projeto, str)):
            erros.append(_m("{0}.projeto: ainda não preenchido", onde) if _pendente(projeto) else _m("{0}.projeto: esperado texto", onde))
            projeto = None
        sub = _validar_substituicoes(caso.get("substituicoes", {}), f"{onde}.substituicoes", erros)
        cl = _validar_clima(caso.get("clima"), f"{onde}.clima", erros)
        tf = _validar_tarifa(caso["tarifa"], f"{onde}.tarifa", erros) if caso.get("tarifa") is not None else {}
        dim = caso.get("dimensoes") or {}
        if not isinstance(dim, dict) or not all(isinstance(k, str) and isinstance(v, (str, int, float)) for k, v in dim.items()):
            erros.append(_m("{0}.dimensoes: esperado um objeto com textos ou números", onde))
            dim = {}
        casos_plano.append({"id": cid, "nome": str(nome), "grupo": str(grupo), "projeto": projeto,
                            "clima": cl, "tarifa": tf, "dimensoes": dim, "substituicoes": sub, "_indice": i})

    # fusão com os padrões e exigências do modelo
    _municipios_conferidos: Dict[Tuple[str, str, str], List[str]] = {}
    for caso in casos_plano:
        caso["substituicoes_efetivas"] = _fundir_substituicoes(padroes["substituicoes"], caso["substituicoes"])
        caso["clima_efetivo"] = _fundir_blocos(padroes["clima"], caso["clima"], (("arquivo", "climbra"),))
        caso["tarifa_efetiva"] = _fundir_blocos(padroes["tarifa"], caso["tarifa"])
        onde = f"casos[{caso['_indice']}] ({caso['id']})"
        origem_do_projeto = caso["projeto"] or base.get("arquivo")
        if not origem_do_projeto and not base.get("modelo") and not base_pendente:
            erros.append(_m("{0}: sem projeto. Informe projeto_base ou o campo «projeto» do caso", onde))
        if not origem_do_projeto and base.get("modelo"):
            ef = caso["substituicoes_efetivas"]
            falta = []
            if "area_captacao_m2" not in ef:
                falta.append("area_captacao_m2")
            if "fracao_pluvial_pct" not in ef and "fracao_pluvial" not in ef:
                falta.append("fracao_pluvial_pct")
            if "demanda_total_l_dia" not in ef and not ("demanda_per_capita_l_dia" in ef and "usuarios" in ef):
                falta.append("demanda_total_l_dia (ou demanda_per_capita_l_dia e usuarios)")
            if "arquivo" not in caso["clima_efetivo"] and "climbra" not in caso["clima_efetivo"]:
                falta.append("clima.arquivo")
            if falta:
                erros.append(_m("{0}: com o modelo da edição nenhum valor é assumido; informe {1}", onde, ", ".join(falta)))
        ref = caso["clima_efetivo"].get("climbra")
        if ref is not None and not ref.get("municipio"):
            erros.append(_m("{0}: clima.climbra sem «municipio»", onde))
        if caso["tarifa_efetiva"] and not (caso["tarifa_efetiva"].get("municipio") or (ref or {}).get("municipio")):
            erros.append(_m("{0}: tarifa sem «municipio» (e sem clima.climbra para herdá-lo)", onde))
        if verificar_arquivos and ref and ref.get("municipio"):
            erros.extend(f"{onde}: {e}" for e in _conferir_municipio(ref, caso["tarifa_efetiva"], _municipios_conferidos))
        if verificar_arquivos and base_dir is not None:
            if origem_do_projeto and not _pendente(origem_do_projeto):
                p = resolver_caminho(base_dir, origem_do_projeto)
                if not p.is_file():
                    erros.append(_m("{0}: projeto não encontrado: {1}", onde, origem_do_projeto))
            ca = caso["clima_efetivo"].get("arquivo")
            if ca and resolver_serie(base_dir, ca) is None:
                erros.append(_m("{0}: arquivo de chuva não encontrado: {1}", onde, ca))
    if base.get("arquivo") and verificar_arquivos and base_dir is not None and not resolver_caminho(base_dir, base["arquivo"]).is_file():
        if not any(c["projeto"] for c in casos_plano) or any(not c["projeto"] for c in casos_plano):
            erros.append(_m("{0}: arquivo não encontrado: {1}", "projeto_base.arquivo", base["arquivo"]))

    if erros:
        return None, erros, avisos
    plano = {"estudo": meta, "base": base, "padroes": padroes, "casos": casos_plano, "analise": analise, "saidas": saidas}
    return plano, [], avisos


def _slug(texto: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize("NFD", str(texto))
    limpo = "".join(c for c in nfkd if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", limpo).strip("-")


def expandir_casos(exp: Any, caminho: str, erros: List[str]) -> List[Dict[str, Any]]:
    """``expansao``: um caso por município × modelo × recorte (nessa ordem), gerado na leitura do estudo.

    Cada caso nasce com ``clima.climbra`` preenchido e ``dimensoes`` (município, IBGE, modelo, recorte, cenário,
    início, fim), que o CSV tidy traz como colunas. Os valores de edificação, a tarifa e a análise vêm dos
    ``padroes`` do estudo. Só na Edição Brasil.
    """
    if not _so_brasil(caminho, erros) or not _validar_chaves(exp, CHAVES_DA_EXPANSAO, caminho, erros):
        return []
    from triton.core.climate_database import CLIMATE_MODELS
    municipios = exp.get("municipios")
    uf_padrao = exp.get("uf")
    if uf_padrao is not None and (not isinstance(uf_padrao, str) or _pendente(uf_padrao)):
        erros.append(_m("{0}.uf: esperado texto", caminho))
        uf_padrao = None
    lista: List[Dict[str, str]] = []
    if not isinstance(municipios, list) or not municipios:
        erros.append(_m("{0}.municipios: lista não vazia de municípios", caminho))
    else:
        for j, m in enumerate(municipios):
            onde = f"{caminho}.municipios[{j}]"
            if not _validar_chaves(m, ("municipio", "uf", "ibge"), onde, erros):
                continue
            nome = m.get("municipio")
            if not isinstance(nome, str) or _pendente(nome):
                erros.append(_m("{0}.municipio: obrigatório", onde))
                continue
            item = {"municipio": nome.strip()}
            uf = m.get("uf", uf_padrao)
            if uf:
                item["uf"] = str(uf).strip()
            if m.get("ibge") is not None:
                if not isinstance(m["ibge"], str) or not _RE_IBGE.match(m["ibge"].strip()):
                    erros.append(_m("{0}.ibge: esperado o código IBGE de sete dígitos, entre aspas", onde))
                    continue
                item["ibge"] = m["ibge"].strip()
            lista.append(item)
    modelos = exp.get("modelos", "todos")
    if modelos == "todos":
        modelos = list(CLIMATE_MODELS)
    elif not isinstance(modelos, list) or not modelos or not all(isinstance(x, str) and x in CLIMATE_MODELS for x in modelos):
        erros.append(_m("{0}.modelos: «todos» ou uma lista de modelos entre: {1}", caminho, ", ".join(CLIMATE_MODELS)))
        modelos = []
    recortes = exp.get("recortes")
    rec_ok: List[Dict[str, str]] = []
    if not isinstance(recortes, list) or not recortes:
        erros.append(_m("{0}.recortes: lista não vazia de recortes (id, cenario, inicio, fim)", caminho))
    else:
        for j, r in enumerate(recortes):
            onde = f"{caminho}.recortes[{j}]"
            if not _validar_chaves(r, ("id", "rotulo", "cenario", "inicio", "fim"), onde, erros):
                continue
            rid = r.get("id")
            if not isinstance(rid, str) or not _RE_ID.match(rid):
                erros.append(_m("{0}.id: obrigatório, só letras, números, ponto, hífen e sublinhado (até 64 caracteres)", onde))
                continue
            sub = _validar_climbra({k: r[k] for k in ("cenario", "inicio", "fim") if k in r}, onde, erros)
            if "cenario" not in sub or "inicio" not in sub or "fim" not in sub:
                erros.append(_m("{0}: informe cenario, inicio e fim", onde))
                continue
            rec_ok.append({"id": rid, "rotulo": str(r.get("rotulo") or rid), **sub})
    casos: List[Dict[str, Any]] = []
    for m in lista:
        for modelo in modelos:
            for r in rec_ok:
                ref = {**m, "modelo": modelo, "cenario": r["cenario"], "inicio": r["inicio"], "fim": r["fim"]}
                cid = f"{_slug(m['municipio'])}__{modelo}__{r['id']}"
                dim = {"municipio": m["municipio"], "ibge": m.get("ibge", ""), "modelo": modelo, "recorte": r["id"],
                       "cenario": r["cenario"], "inicio": r["inicio"], "fim": r["fim"]}
                casos.append({"id": cid, "nome": f"{m['municipio']} · {modelo} · {r['rotulo']}", "grupo": r["id"],
                              "clima": {"climbra": ref}, "dimensoes": dim})
    return casos


def _conferir_municipio(ref: Dict[str, Any], tarifa: Dict[str, Any], memoria: Dict[Tuple[str, str, str], List[str]]) -> List[str]:
    """O município existe na CLIMBra e (com UF) no catálogo de tarifas; a conferência é guardada por município."""
    chave = (ref.get("municipio", ""), ref.get("uf", ""), (tarifa or {}).get("categoria", ""))
    if chave in memoria:
        return memoria[chave]
    erros: List[str] = []
    from triton.core.climate_database import find_matching_climate_city_name
    if not find_matching_climate_city_name(ref["municipio"]):
        erros.append(_m("município «{0}» não está na base CLIMBra", ref["municipio"]))
    elif ref.get("uf"):
        from triton.core.tariffs_database import get_city_data
        if not get_city_data(ref["uf"], ref["municipio"]):
            erros.append(_m("município «{0}» não consta na UF {1} do catálogo (nome repetido em outra UF?)", ref["municipio"], ref["uf"]))
    memoria[chave] = erros
    return erros


def _chave_de_alvo(canon: str) -> Tuple[str, ...]:
    if canon.startswith("campo:"):
        return (canon[6:],)
    if canon.startswith("caminho:"):
        return (canon,)
    return tuple(APELIDOS[canon]["alvos"])


def _fundir_substituicoes(padroes: Dict[str, Any], caso: Dict[str, Any]) -> Dict[str, Any]:
    """Os padrões valem para todos os casos; o caso vence, inclusive quando usa outro apelido para o mesmo parâmetro."""
    alvos_do_caso = {a for c in caso for a in _chave_de_alvo(c)}
    fundidas = {c: v for c, v in padroes.items() if not (set(_chave_de_alvo(c)) & alvos_do_caso)}
    fundidas.update(caso)
    return fundidas


def resolver_caminho(base_dir: Path, texto: str) -> Path:
    p = Path(texto)
    return p if p.is_absolute() else (Path(base_dir) / p)


def resolver_serie(base_dir: Path, texto: str) -> Optional[Path]:
    """O arquivo de chuva: ao lado do estudo ou, como no ``load_precipitation``, no diretório atual ou em ``data/rainfall``."""
    candidatos = [resolver_caminho(base_dir, texto), Path(texto), Path(Path(texto).name)]
    raiz = Path(__file__).resolve().parent.parent.parent
    candidatos.append(raiz / "data" / "rainfall" / Path(texto).name)
    for c in candidatos:
        if c.is_file():
            return c.resolve()
    return None


# ══ Leitura do estudo ══════════════════════════════════════════════════════════════════════════

def ler_documento(caminho: Path) -> Tuple[Any, str]:
    """Lê o JSON do estudo e devolve ``(objeto, sha256 do arquivo)``."""
    caminho = Path(caminho)
    if not caminho.is_file():
        raise FileNotFoundError(_m("Estudo não encontrado: {0}", caminho.name))
    dados = caminho.read_bytes()
    try:
        doc = json.loads(dados.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(_m("{0} não é um JSON válido: {1}", caminho.name, exc)) from None
    return doc, hashlib.sha256(dados).hexdigest()


def carregar_plano(caminho: Path, verificar_arquivos: bool = True) -> Tuple[Dict[str, Any], List[str]]:
    """Lê e valida o estudo; levanta :class:`ErroDeEstudo` com todos os erros. Devolve ``(plano, avisos)``."""
    caminho = Path(caminho)
    doc, sha = ler_documento(caminho)
    plano, erros, avisos = validar_documento(doc, caminho.resolve().parent, verificar_arquivos)
    if erros:
        raise ErroDeEstudo(erros)
    plano["caminho"] = caminho.resolve()
    plano["base_dir"] = caminho.resolve().parent
    plano["sha256"] = sha
    return plano, avisos


# ══ Montagem de um caso ════════════════════════════════════════════════════════════════════════

def _definir_campo(cfg: Any, campo: str, valor: Any) -> None:
    """Como ``--set``: o valor assume o tipo do campo."""
    atual = getattr(cfg, campo, None)
    if campo == "phi_operation_rule":
        cfg.phi_operation_rule = None if valor in (None, "triton") else float(valor)
        return
    if isinstance(atual, bool):
        if not isinstance(valor, bool):
            raise ValueError(_m("o campo {0} é verdadeiro/falso; recebido {1!r}", campo, valor))
        setattr(cfg, campo, valor)
    elif isinstance(atual, int):
        if not _eh_numero(valor) or abs(float(valor) - round(float(valor))) > 1e-9:
            raise ValueError(_m("o campo {0} é inteiro; recebido {1!r}", campo, valor))
        setattr(cfg, campo, int(round(float(valor))))
    elif isinstance(atual, float):
        if not _eh_numero(valor):
            raise ValueError(_m("o campo {0} é numérico; recebido {1!r}", campo, valor))
        setattr(cfg, campo, float(valor))
    elif isinstance(atual, str):
        if not isinstance(valor, str):
            raise ValueError(_m("o campo {0} é texto; recebido {1!r}", campo, valor))
        setattr(cfg, campo, valor)
    else:
        setattr(cfg, campo, valor)


def _aplicar_apelido(cfg: Any, chave: str, v: Any) -> None:
    if chave == "area_captacao_m2":
        cfg.area = float(v)
    elif chave == "coeficiente_escoamento":
        cfg.runoff_coeff = float(v)
    elif chave == "descarte_mm":
        cfg.discard = float(v)
    elif chave == "usuarios":
        cfg.residents_count = int(v)
    elif chave == "demanda_per_capita_l_dia":
        cfg.demand_value = float(v)
    elif chave in ("fracao_pluvial_pct",):
        cfg.rainwater_share = float(v) / 100.0
    elif chave == "fracao_pluvial":
        cfg.rainwater_share = float(v)
    elif chave == "volume_reservatorio_l":
        cfg.lower_tank_mode = 0
        cfg.lower_tank_fixed = float(v)
    elif chave == "volume_maximo_l":
        cfg.lower_tank_mode = 1
        cfg.lower_tank_max = float(v)
    elif chave == "passo_volume_l":
        cfg.lower_tank_step = float(v)
    elif chave == "reservatorio_superior_l":
        cfg.upper_tank_vol = float(v)
        cfg.upper_tank_used = int(float(v) > 0)
    elif chave == "limiar_bombeamento_l":
        cfg.pumping_threshold = float(v)
    elif chave == "economias":
        cfg.num_economias = int(v)
    elif chave == "irrigacao_l_dia":
        cfg.irrigation_liters_per_day = float(v)
    elif chave == "data_inicio":
        cfg.start_date = str(v)
    elif chave == "regra_phi":
        cfg.phi_operation_rule = v
    elif chave == "delta_ideal_pct":
        cfg.delta_ideal = float(v)
    elif chave == "periodo_analise_anos":
        cfg.analysis_period_years = int(v)
    elif chave == "tma_pct_mes":
        cfg.tma = float(v)
    elif chave == "tarifa_energia":
        cfg.elec_tariff = float(v)
    elif chave != "demanda_total_l_dia":      # esta vem depois, com os usuários já definidos
        raise ValueError(_m("apelido sem aplicação: {0}", chave))   # pragma: no cover


def _aplicar_caminho(raw: Dict[str, Any], caminho: str, valor: Any) -> None:
    """Troca um valor do JSON do projeto por um caminho pontilhado (``inputs.building_and_demand.catchment_area_m2``)."""
    partes = caminho.split(".")
    no: Any = raw
    for p in partes[:-1]:
        if isinstance(no, dict) and p in no:
            no = no[p]
        elif isinstance(no, list) and p.isdigit() and int(p) < len(no):
            no = no[int(p)]
        else:
            raise ValueError(_m("o caminho «{0}» não existe no projeto (parou em «{1}»)", caminho, p) + _sugestao_de_filhos(no, p))
    ultimo = partes[-1]
    if isinstance(no, dict) and ultimo in no:
        antigo = no[ultimo]
        if antigo is not None and type(antigo) is not type(valor) and not (_eh_numero(antigo) and _eh_numero(valor)):
            raise ValueError(_m("o caminho «{0}» guarda {1}; o valor dado é {2}", caminho,
                                type(antigo).__name__, type(valor).__name__))
        no[ultimo] = valor
    elif isinstance(no, list) and ultimo.isdigit() and int(ultimo) < len(no):
        no[int(ultimo)] = valor
    else:
        raise ValueError(_m("o caminho «{0}» não existe no projeto (parou em «{1}»)", caminho, ultimo) + _sugestao_de_filhos(no, ultimo))


def _sugestao_de_filhos(no: Any, chave: str) -> str:
    if isinstance(no, dict):
        sug = _sugestao(chave, [str(k) for k in no])
        return sug or " " + _m("Chaves disponíveis: {0}", ", ".join(map(str, list(no)[:12])))
    return ""


def _carregar_bundle_sem_prefill(cli: Any, caminho: Path) -> Dict[str, Any]:
    """``cli._load_bundle`` sem o preenchimento de CAPEX: ele roda depois, com as substituições já aplicadas."""
    original = cli._prefill_preliminary_capex
    cli._prefill_preliminary_capex = lambda cfg: None
    try:
        return cli._load_bundle(str(caminho))
    finally:
        cli._prefill_preliminary_capex = original


def _bundle_do_modelo(cli: Any) -> Dict[str, Any]:
    """O modelo de projeto da edição (o de «triton init»), sem série de chuva."""
    from triton.cli import COEFICIENTE_DE_ESCOAMENTO_PADRAO
    from triton.core.edition import configuracao_da_edicao
    cfg = configuracao_da_edicao()
    for campo, valor in dict(area=100.0, demand_value=120.0, residents_count=4, rainwater_share=0.40,
                             runoff_coeff=COEFICIENTE_DE_ESCOAMENTO_PADRAO, lower_tank_max=10000.0,
                             lower_tank_step=500.0, upper_tank_vol=500.0, upper_tank_used=1).items():
        setattr(cfg, campo, valor)
    if not is_brl_edition():
        cfg.iptu_annual_value = 0.0
        cfg.iptu_discount_pct = 0.0
    return {"config": cfg, "precip_data": None, "analysis": cli._template_analysis(), "raw": {}, "source_path": "",
            "is_json": False}


def impressao_da_serie(precip: Any) -> Dict[str, Any]:
    from triton.core.parser import impressao_da_serie as _imp
    return _imp(precip)


@lru_cache(maxsize=None)
def _sha256_em_cache(caminho: str) -> str:
    return sha256_do_arquivo(Path(caminho))


def _aplicar_climbra(cfg: Any, bundle: Dict[str, Any], ref: Dict[str, Any], arquivos: List[Dict[str, str]],
                     alertas: List[str]) -> None:
    """A série do município, do modelo, do cenário e do recorte, lida da base CLIMBra (só na Edição Brasil)."""
    if not usa_dados_do_brasil():
        raise ValueError(_m("o CLIMBra e o catálogo de tarifas municipais só existem na Edição Brasil; use «arquivo» com a série de chuva"))
    from triton.core import climate_database as cdb
    cidade = cdb.find_matching_climate_city_name(ref["municipio"])
    if not cidade:
        raise ValueError(_m("município «{0}» não está na base CLIMBra", ref["municipio"]))
    modelo = ref.get("modelo") or cdb.DEFAULT_CLIMATE_MODEL
    cenario = ref.get("cenario") or "HIST"
    inicio = ref.get("inicio") or cdb.CLIMATE_SCENARIOS[cenario]["start_date"]
    fim = ref.get("fim") or cdb.CLIMATE_SCENARIOS[cenario]["end_date"]
    serie, ini_efetivo, fim_efetivo, _total, _sel, _ = cdb.load_national_climate_series(cidade, modelo, cenario, inicio, fim)
    cfg.climate_source_mode = "national_db"
    cfg.precip_file = ""
    cfg.climate_city_name, cfg.climate_city_uf = cidade, ref.get("uf") or getattr(cfg, "climate_city_uf", "")
    cfg.climate_model, cfg.climate_scenario = modelo, cenario
    cfg.climate_start_date, cfg.climate_end_date = ini_efetivo, fim_efetivo
    cfg.start_date = ini_efetivo
    bundle["precip_data"] = serie
    if ini_efetivo != inicio or fim_efetivo != fim:
        alertas.append(_m("recorte pedido {0} a {1}; a série do modelo cobre {2} a {3}", inicio, fim, ini_efetivo, fim_efetivo))
    bancos = cdb._caminhos_dos_bancos(modelo, cenario)
    if bancos:
        arquivos.append({"papel": "base-climbra", "caminho": Path(bancos[0]).name, "sha256": _sha256_em_cache(bancos[0])})


def _aplicar_tarifa(cfg: Any, tar: Dict[str, Any], ref: Dict[str, Any], arquivos: List[Dict[str, str]],
                    alertas: List[str]) -> None:
    """A tarifa de água, esgoto e energia do município, do catálogo do programa (como a aba Projeto faz)."""
    if not usa_dados_do_brasil():
        raise ValueError(_m("o CLIMBra e o catálogo de tarifas municipais só existem na Edição Brasil; use «arquivo» com a série de chuva"))
    from triton.core import tariffs_database as tdb
    from triton.core.vigencia_tarifaria import data_da_vigencia
    municipio = tar.get("municipio") or ref.get("municipio")
    uf = tar.get("uf") or ref.get("uf") or getattr(cfg, "climate_city_uf", "")
    categoria = tar.get("categoria", "residencial")
    if not municipio:
        raise ValueError(_m("tarifa sem município"))
    dados = tdb.get_city_tariffs_by_category(uf, municipio, categoria)
    if dados is None and categoria != "residencial" and tar.get("se_ausente") == "residencial":
        dados = tdb.get_city_tariffs_by_category(uf, municipio, "residencial")
        if dados is not None:
            alertas.append(_m("sem tabela «{0}» coletada para {1}: usada a residencial do catálogo", categoria, municipio))
            categoria = "residencial"
    if dados is None:
        raise ValueError(_m("sem tarifa «{0}» no catálogo para {1} ({2})", categoria, municipio, uf))
    cfg.tariff_city_uf, cfg.tariff_city_name = uf, dados.get("municipio", municipio)
    cfg.elec_city_uf, cfg.elec_city_name = uf, dados.get("municipio", municipio)
    cfg.tariff_category = categoria
    cfg.water_tariffs = dados.get("faixas", cfg.water_tariffs)
    cfg.sewage_mode, cfg.sewage_rate = tdb.esgoto_do_municipio(dados)
    vig = data_da_vigencia(dados.get("vigencia_saneamento", ""))
    cfg.tariff_vigencia = vig.strftime("%d/%m/%Y") if vig else ""
    if dados.get("energia_r_kwh", 0.0) > 0:
        cfg.elec_tariff = dados["energia_r_kwh"]
    banco = tdb._find_database_file()
    arquivos.append({"papel": "tarifas", "caminho": Path(banco).name, "sha256": _sha256_em_cache(banco)})


def montar_caso(plano: Dict[str, Any], caso: Dict[str, Any]) -> Dict[str, Any]:
    """Abre o projeto do caso, aplica o clima e as substituições, e confere. Devolve ``bundle`` e metadados; levanta ``ValueError``."""
    from triton import cli
    base_dir: Path = plano["base_dir"]
    origem = caso["projeto"] or plano["base"].get("arquivo")
    efetivas = caso["substituicoes_efetivas"]
    clima = caso["clima_efetivo"]
    arquivos: List[Dict[str, str]] = []
    alertas: List[str] = []

    caminhos = {c: v for c, v in efetivas.items() if c.startswith("caminho:")}
    if origem:
        projeto = resolver_caminho(base_dir, origem)
        if not projeto.is_file():
            raise ValueError(_m("projeto não encontrado: {0}", origem))
        arquivos.append({"papel": "projeto", "caminho": _relativo(projeto, base_dir), "sha256": sha256_do_arquivo(projeto)})
        if caminhos:
            if projeto.suffix.lower() not in (".triton", ".json"):
                raise ValueError(_m("caminhos pontilhados só valem para projetos .triton"))
            raw = json.loads(projeto.read_text(encoding="utf-8"))
            for c, v in caminhos.items():
                _aplicar_caminho(raw, c[len("caminho:"):], v)
            with tempfile.TemporaryDirectory(prefix="triton-estudo-") as tmp:
                copia = Path(tmp) / projeto.name
                copia.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
                bundle = _carregar_bundle_sem_prefill(cli, copia)
            cfg = bundle["config"]
            if bundle.get("precip_data") is None and cfg.precip_file and not os.path.isabs(cfg.precip_file):
                vizinho = projeto.parent / cfg.precip_file
                if vizinho.is_file():
                    cfg.precip_file = str(vizinho)
            bundle["source_path"] = str(projeto)
        else:
            bundle = _carregar_bundle_sem_prefill(cli, projeto)
    else:
        bundle = _bundle_do_modelo(cli)
    cfg = bundle["config"]

    # clima
    serie_arquivo = clima.get("arquivo")
    if serie_arquivo:
        achada = resolver_serie(base_dir, serie_arquivo)
        if achada is None:
            raise ValueError(_m("arquivo de chuva não encontrado: {0}", serie_arquivo))
        cfg.precip_file = str(achada)
        cfg.climate_source_mode = "custom_file"
        bundle["precip_data"] = None
        arquivos.append({"papel": "chuva", "caminho": _relativo(achada, base_dir), "sha256": sha256_do_arquivo(achada)})
    if clima.get("climbra"):
        _aplicar_climbra(cfg, bundle, clima["climbra"], arquivos, alertas)
    if caso.get("tarifa_efetiva"):
        _aplicar_tarifa(cfg, caso["tarifa_efetiva"], clima.get("climbra") or {}, arquivos, alertas)
    if clima.get("data_inicio"):
        cfg.start_date = clima["data_inicio"]
    if clima.get("nome"):
        cfg.climate_city_name = clima["nome"]
    if clima.get("fonte"):
        cfg.climate_model = clima["fonte"]

    cli._prefill_preliminary_capex(cfg)

    # substituições, na ordem fixa dos apelidos
    for c, v in efetivas.items():
        if c.startswith("campo:"):
            _definir_campo(cfg, c[len("campo:"):], v)
    for chave in APELIDOS:
        if chave in efetivas:
            _aplicar_apelido(cfg, chave, efetivas[chave])
    if "demanda_total_l_dia" in efetivas:
        usuarios = cfg.residents_count if cfg.residents_count > 0 else 1
        cfg.demand_value = float(efetivas["demanda_total_l_dia"]) / usuarios
    if efetivas and (getattr(cfg, "demand_mode", "constant") not in ("constant", "", None)
                     or cfg.demand_monthly or cfg.weekly_demands or cfg.daily_demands):
        if any(k in efetivas for k in ("demanda_total_l_dia", "demanda_per_capita_l_dia", "usuarios")):
            alertas.append(_m("o projeto usa modulação da demanda: as substituições de demanda e de usuários podem não ter efeito sobre a modulação"))

    precip = cli._get_precipitation(bundle)
    erros = cli._validate_config(cfg, precip) + cli._validate_analysis_config(bundle.get("analysis"))
    if erros:
        raise ValueError(_m("projeto inválido:") + " " + "; ".join(erros))
    return {"bundle": bundle, "cfg": cfg, "precip": precip, "arquivos": arquivos, "alertas": alertas}


def chave_do_caso(plano: Dict[str, Any], caso: Dict[str, Any], arquivos: List[Dict[str, str]]) -> str:
    """Impressão digital do que determina o resultado do caso: retomar só pula o caso se ela não mudou."""
    carga = {"triton": __version__, "edicao": get_current_edition(), "analise": plano["analise"],
             "caso": {"id": caso["id"], "projeto": caso["projeto"] or plano["base"].get("arquivo") or "<modelo>",
                      "clima": caso["clima_efetivo"], "tarifa": caso.get("tarifa_efetiva") or {},
                      "substituicoes": caso["substituicoes_efetivas"]},
             "arquivos": arquivos}
    return hashlib.sha256(json.dumps(carga, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def arquivos_do_caso(plano: Dict[str, Any], caso: Dict[str, Any]) -> List[Dict[str, str]]:
    """Projeto e série de chuva do caso, com SHA-256 (sem abrir o projeto)."""
    base_dir = plano["base_dir"]
    saida = []
    origem = caso["projeto"] or plano["base"].get("arquivo")
    if origem:
        p = resolver_caminho(base_dir, origem)
        if p.is_file():
            saida.append({"papel": "projeto", "caminho": _relativo(p, base_dir), "sha256": sha256_do_arquivo(p)})
    ca = caso["clima_efetivo"].get("arquivo")
    if ca:
        p = resolver_serie(base_dir, ca)
        if p is not None:
            saida.append({"papel": "chuva", "caminho": _relativo(p, base_dir), "sha256": sha256_do_arquivo(p)})
    ref = caso["clima_efetivo"].get("climbra")
    if ref and usa_dados_do_brasil():
        try:
            from triton.core import climate_database as cdb
            bancos = cdb._caminhos_dos_bancos(ref.get("modelo") or cdb.DEFAULT_CLIMATE_MODEL, ref.get("cenario") or "HIST")
            if bancos:
                saida.append({"papel": "base-climbra", "caminho": Path(bancos[0]).name, "sha256": _sha256_em_cache(bancos[0])})
        except Exception:
            pass
    if (ref or caso.get("tarifa_efetiva")) and usa_dados_do_brasil():
        try:
            from triton.core import tariffs_database as tdb
            banco = tdb._find_database_file()
            saida.append({"papel": "tarifas", "caminho": Path(banco).name, "sha256": _sha256_em_cache(banco)})
        except Exception:
            pass
    return saida


def verificar_casos(plano: Dict[str, Any]) -> List[str]:
    """Abre cada caso (projeto, chuva e substituições) sem simular, e junta os erros: é a parte funda de ``estudo validate``."""
    erros: List[str] = []
    for caso in plano["casos"]:
        try:
            montar_caso(plano, caso)
        except Exception as exc:
            erros.append(f"casos[{caso['_indice']}] ({caso['id']}): " + limpar_caminhos(str(exc), plano["base_dir"]))
    return erros


# ══ Execução de um caso ════════════════════════════════════════════════════════════════════════

def _f(v: Any) -> Optional[float]:
    if v is None or isinstance(v, bool):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _linhas_por_volume(report: Dict[str, Any]) -> Dict[float, Dict[str, Dict[str, Any]]]:
    linhas: Dict[float, Dict[str, Dict[str, Any]]] = {}
    for origem, bloco in (("tec", report["technical"]["alternatives"]),
                          ("eco", report.get("economic", {}).get("alternatives", [])),
                          ("amb", report.get("environmental", {}).get("alternatives", [])),
                          ("rank", report.get("topsis", {}).get("ranking", []))):
        for linha in bloco:
            v = float(linha.get("lower_tank_volume_l"))
            linhas.setdefault(v, {})[origem] = linha
    return linhas


def extrair_metricas(report: Dict[str, Any], cfg: Any, precip: Any, plano: Dict[str, Any]) -> Dict[str, Any]:
    """Escolhe o volume do caso e tira do relatório todas as métricas disponíveis (as demais ficam ``None``)."""
    import numpy as np
    resumo = report["technical"]["summary"]
    linhas = _linhas_por_volume(report)
    criterio = plano["analise"]["volume"]
    notas: List[str] = []
    if isinstance(criterio, float):
        escolhido, criterio_txt = criterio, "fixo"
    elif criterio == "topsis":
        escolhido, criterio_txt = report.get("topsis", {}).get("best_volume_l"), "topsis"
    else:
        criterio_txt = "otimo_tecnico"
        escolhido = resumo.get("optimal_volume_l")
        if escolhido is None and resumo.get("mode") == "fixed":
            escolhido, criterio_txt = resumo.get("selected_volume_l"), "fixo"
        elif escolhido is None:
            positivos = [(r["tec"]["potable_savings_pct"], v) for v, r in linhas.items() if v > 0]
            escolhido = max(positivos)[1] if positivos else min(linhas)
            notas.append(_m("o volume ótimo técnico não foi definido; usado o de maior economia de água potável"))
    if escolhido is None:
        raise ValueError(_m("não foi possível escolher o volume do caso"))
    volume = min(linhas, key=lambda v: abs(v - float(escolhido)))
    linha = linhas[volume]

    demanda = cfg.demand_value * (cfg.residents_count if cfg.residents_count > 0 else 1)
    serie = np.asarray(precip, dtype=float)
    chuva_anual = float(np.nanmean(serie)) * 365.25 if len(serie) else None
    entradas = {"area": cfg.area, "usuarios": cfg.residents_count, "demanda": demanda,
                "fracao": cfg.rainwater_share * 100.0, "chuva_anual": chuva_anual, "dias": len(serie)}
    topsis = report.get("topsis", {})
    smaa = {a["lower_tank_volume_l"]: a for a in report.get("smaa_vikor", {}).get("acceptabilities", [])}
    valores: Dict[str, Optional[float]] = {}
    for mid, m in METRICAS.items():
        o, k = m["origem"], m["chave"]
        if o == "entrada":
            v = entradas.get(k)
        elif o == "resumo":
            v = resumo.get(k)
        elif o == "topsis":
            v = topsis.get(k)
        elif o == "smaa":
            v = smaa.get(volume, {}).get(k)
        else:
            v = linha.get(o, {}).get(k)
        valores[mid] = _f(v)
    return {"volume_l": volume, "criterio": criterio_txt, "valores": valores, "notas": notas}


def _moeda(report: Dict[str, Any]) -> Dict[str, Any]:
    """A moeda do projeto; sem declaração, a única moeda da edição (BRL: real; IBE: euro) ou nenhuma (INT)."""
    m = (report.get("provenance") or {}).get("currency") or {}
    codigo, simbolo = m.get("code") or "", m.get("symbol") or ""
    if codigo:
        return {"codigo": codigo, "simbolo": simbolo, "declarada": True}
    padrao = ("BRL", "R$") if is_brl_edition() else (("EUR", "€") if is_ibe_edition() else ("", ""))
    return {"codigo": padrao[0], "simbolo": padrao[1], "declarada": False}


def executar_caso(plano: Dict[str, Any], caso: Dict[str, Any]) -> Dict[str, Any]:
    """Roda um caso e devolve o resultado (sempre um dicionário; ``status`` ``ok`` ou ``erro``). Não escreve nada."""
    from triton import cli
    arquivos = arquivos_do_caso(plano, caso)
    base = {"esquema": {"nome": ESQUEMA_CASO, "versao": 1}, "id": caso["id"], "nome": caso["nome"], "grupo": caso["grupo"],
            "chave": chave_do_caso(plano, caso, arquivos)}
    if caso.get("dimensoes"):
        base["dimensoes"] = dict(caso["dimensoes"])
    try:
        montado = montar_caso(plano, caso)
        cfg, precip, bundle = montado["cfg"], montado["precip"], montado["bundle"]
        analise = plano["analise"]
        analysis_cfg = bundle.get("analysis", {}) or {}
        pesos = tuple(analise["pesos"] or analysis_cfg.get("topsis_weights", cli.PESOS_PADRAO))
        volume_fixo = analise["volume"] if isinstance(analise["volume"], float) else None
        origem_txt = Path(montado["arquivos"][0]["caminho"]).name if montado["arquivos"] and montado["arquivos"][0]["papel"] == "projeto" else ""
        import contextlib
        import warnings
        saidas_cfg = plano.get("saidas") or {}
        precisa_smaa = bool(saidas_cfg.get("gravar_analise", True)
                            or "aceitabilidade_smaa_pct" in saidas_cfg.get("metricas", ()))
        # avisos de frações vão para «alertas»; avisos do motor (limites físicos do passo diário) para «avisos_do_motor»
        with warnings.catch_warnings(record=True) as do_motor, contextlib.redirect_stderr(io.StringIO()) as ruido:
            warnings.simplefilter("always")
            relatorio = cli.run_analysis(cfg, precip, analise["tipo"], volume_fixo, pesos,
                                         analysis_cfg.get("environmental", {}), origem_txt, 0, analise["semente"],
                                         smaa=precisa_smaa)
        # só os avisos do modelo; os da plataforma (arquivo não fechado, depreciação) e os endereços de memória ficam de fora,
        # para que duas execuções deem o mesmo arquivo
        ruido_da_plataforma = (ResourceWarning, DeprecationWarning, PendingDeprecationWarning, ImportWarning, FutureWarning)
        avisos_do_motor = sorted({f"{w.category.__name__}: {re.sub(r'0x[0-9A-Fa-f]+', '0x…', str(w.message).strip())[:300]}"
                                  for w in do_motor if not issubclass(w.category, ruido_da_plataforma)})
        for linha in ruido.getvalue().splitlines():
            if linha.strip():
                montado["alertas"].append(limpar_caminhos(linha.strip(), plano["base_dir"]))
        relatorio["provenance"]["currency"] = cli._moeda_do_bundle(bundle)
        relatorio.pop("generated_at_utc", None)
        extr = extrair_metricas(relatorio, cfg, precip, plano)
        moeda = _moeda(relatorio)
        fonte = dict((relatorio.get("provenance") or {}).get("rainfall_source") or {})
        fonte["serie"] = {**impressao_da_serie(precip), "inicio": cfg.start_date}
        base.update({
            "status": "ok", "volume_selecionado_l": extr["volume_l"], "criterio_do_volume": extr["criterio"],
            "metricas": {k: _num_limpo(v) for k, v in extr["valores"].items()},
            "moeda": moeda, "fonte_da_chuva": fonte, "arquivos": montado["arquivos"],
            "substituicoes": {k: v for k, v in caso["substituicoes_efetivas"].items()},
            "alertas": montado["alertas"] + extr["notas"], "avisos_do_motor": avisos_do_motor,
            "analise_completa": relatorio,
        })
    except Exception as exc:    # um caso com erro não derruba o estudo; o erro vai para o resultado, sem caminhos absolutos
        base.update({"status": "erro", "erro": limpar_caminhos(f"{exc}", plano["base_dir"]) or type(exc).__name__,
                     "arquivos": arquivos})
    return base


def _trabalhar_caso(argumentos: Tuple[str, int]) -> Dict[str, Any]:
    """Ponto de entrada do processo filho (``--paralelo``): relê o estudo e roda o caso de índice dado."""
    caminho, indice = argumentos
    plano = _plano_do_processo(caminho)
    res = executar_caso(plano, plano["casos"][indice])
    if not (plano.get("saidas") or {}).get("gravar_analise", True):
        res.pop("analise_completa", None)
    return res


@lru_cache(maxsize=2)
def _plano_do_processo(caminho: str) -> Dict[str, Any]:
    """O plano lido uma vez por processo filho (estudos com milhares de casos não o releem a cada caso)."""
    return carregar_plano(Path(caminho))[0]


# ══ Pasta de saída ═════════════════════════════════════════════════════════════════════════════

def pasta_do_caso(saida: Path, caso_id: str) -> Path:
    return Path(saida) / "casos" / caso_id


def _gravar_caso(saida: Path, resultado: Dict[str, Any], com_analise: bool = True) -> None:
    pasta = pasta_do_caso(saida, resultado["id"])
    completo = resultado.get("analise_completa") if com_analise else None
    leve = {k: v for k, v in resultado.items() if k != "analise_completa"}
    _escrever(pasta / "resultado.json", _json_texto(leve))
    if completo is not None:
        _escrever(pasta / "analise.json", json.dumps(completo, ensure_ascii=False, indent=2, default=_json_padrao) + "\n")
    elif (pasta / "analise.json").exists():
        (pasta / "analise.json").unlink()


def _json_padrao(v: Any) -> Any:
    if hasattr(v, "item"):
        return v.item()
    if isinstance(v, Path):
        return v.as_posix()
    raise TypeError(type(v).__name__)


def ler_resultado_do_caso(saida: Path, caso_id: str) -> Optional[Dict[str, Any]]:
    arq = pasta_do_caso(saida, caso_id) / "resultado.json"
    if not arq.is_file():
        return None
    try:
        return json.loads(arq.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


class Execucao:
    """O que ``rodar_estudo`` fez: contagens e o código de saída."""

    def __init__(self) -> None:
        self.calculados: List[str] = []
        self.pulados: List[str] = []
        self.erros: List[str] = []
        self.resultados: List[Dict[str, Any]] = []
        self.arquivos: List[str] = []
        self.avisos: List[str] = []

    @property
    def codigo(self) -> int:
        return 1 if self.erros else 0


def rodar_estudo(caminho: Path, saida: Path, retomar: bool = False, sobrescrever: bool = False, paralelo: int = 1,
                 log: Optional[Callable[[str], None]] = None) -> Execucao:
    """Executa todos os casos (em ordem estável) e escreve as saídas. ``retomar`` pula casos prontos e inalterados."""
    log = log or (lambda _msg: None)
    plano, avisos = carregar_plano(caminho)
    saida = Path(saida)
    ja_tem = (saida / "casos").is_dir() and any((saida / "casos").iterdir())
    if ja_tem and not (retomar or sobrescrever):
        raise ValueError(_m("a pasta de saída já tem resultados; use --retomar para ignorar os casos prontos ou --sobrescrever para refazê-los"))
    if paralelo < 1:
        raise ValueError(_m("--paralelo deve ser um inteiro positivo"))
    saida.mkdir(parents=True, exist_ok=True)
    execucao = Execucao()
    execucao.avisos.extend(avisos)

    casos = plano["casos"]
    prontos: Dict[int, Dict[str, Any]] = {}
    pendentes: List[int] = []
    for i, caso in enumerate(casos):
        if retomar and not sobrescrever:
            anterior = ler_resultado_do_caso(saida, caso["id"])
            if anterior and anterior.get("status") == "ok" and anterior.get("chave") == chave_do_caso(plano, caso, arquivos_do_caso(plano, caso)):
                prontos[i] = anterior
                continue
        pendentes.append(i)

    resultados: Dict[int, Dict[str, Any]] = dict(prontos)
    total = len(casos)

    def concluir(i: int, resultado: Dict[str, Any], tempo: float) -> None:
        resultados[i] = resultado
        _gravar_caso(saida, resultado, plano["saidas"]["gravar_analise"])
        resultado.pop("analise_completa", None)      # fora da memória: o estudo pode ter milhares de casos
        estado = "ok" if resultado["status"] == "ok" else _m("erro: {0}", resultado.get("erro", ""))
        log(f"[{len(resultados)}/{total}] {resultado['id']}: {estado} ({tempo:.1f} s)")
        (execucao.calculados if resultado["status"] == "ok" else execucao.erros).append(resultado["id"])

    for i in sorted(prontos):
        execucao.pulados.append(casos[i]["id"])
        log(f"[{casos[i]['id']}] " + _m("pronto, ignorado"))

    if paralelo > 1 and len(pendentes) > 1:
        from concurrent.futures import ProcessPoolExecutor
        inicio = time.perf_counter()
        n_workers = min(paralelo, len(pendentes))
        janela = n_workers * 4
        it = iter(pendentes)
        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futuros = {}
            for _ in range(min(janela, len(pendentes))):
                idx = next(it)
                futuros[idx] = pool.submit(_trabalhar_caso, (str(plano["caminho"]), idx))
            for i in pendentes:                       # na ordem do estudo, qualquer que seja a ordem de término
                res = futuros.pop(i).result()
                try:
                    prox = next(it)
                    futuros[prox] = pool.submit(_trabalhar_caso, (str(plano["caminho"]), prox))
                except StopIteration:
                    pass
                concluir(i, res, time.perf_counter() - inicio)
    else:
        for i in pendentes:
            t0 = time.perf_counter()
            concluir(i, executar_caso(plano, casos[i]), time.perf_counter() - t0)

    ordenados = [resultados[i] for i in range(total)]
    execucao.resultados = ordenados
    # cópia do estudo: o «resumo» e o «texto» leem dela, sem precisar dos projetos
    _escrever(saida / "estudo.json", Path(plano["caminho"]).read_bytes().decode("utf-8-sig"))
    execucao.arquivos = escrever_saidas(saida, plano, ordenados)
    return execucao


# ══ Tabelas e saídas ═══════════════════════════════════════════════════════════════════════════

def _casas(plano: Dict[str, Any], metrica: str) -> int:
    cd = plano["saidas"]["casas_decimais"]
    return cd.get(metrica, cd.get("padrao", METRICAS[metrica]["casas"]))


_UNIDADES = {
    "en": {"dias": "days", "meses": "months", "anos": "years", "pessoas": "people", "L/dia": "L/day", "mm/ano": "mm/year",
           "m³/ano": "m³/year", "kg CO2e/ano": "kg CO2e/year", "kWh/ano": "kWh/year"},
    "es": {"dias": "días", "anos": "años", "pessoas": "personas", "L/dia": "L/día", "mm/ano": "mm/año",
           "m³/ano": "m³/año", "kg CO2e/ano": "kg CO2e/año", "kWh/ano": "kWh/año"},
    "zh": {"dias": "天", "meses": "月", "anos": "年", "pessoas": "人", "L/dia": "L/天", "mm/ano": "mm/年",
           "m³/ano": "m³/年", "kg CO2e/ano": "kg CO2e/年", "kWh/ano": "kWh/年"},
}


def unidade_da_metrica(metrica: str, resultado: Optional[Dict[str, Any]], idioma: str) -> str:
    un = METRICAS[metrica]["unidade"]
    if un != _M:
        return _UNIDADES.get(_lingua(idioma), {}).get(un, un)
    if resultado and resultado.get("moeda", {}).get("codigo"):
        return resultado["moeda"]["codigo"]
    return _txt("moeda_nd", idioma)


def _idioma_do_plano(plano: Dict[str, Any], idioma: Optional[str] = None) -> str:
    return resolver_idioma(idioma if idioma else plano["saidas"]["idioma"])


def _valor(resultado: Optional[Dict[str, Any]], metrica: str) -> Optional[float]:
    if not resultado or resultado.get("status") != "ok":
        return None
    return _f(resultado.get("metricas", {}).get(metrica))


def moedas_dos_casos(resultados: Sequence[Optional[Dict[str, Any]]]) -> List[str]:
    return sorted({r["moeda"]["codigo"] or "?" for r in resultados if r and r.get("status") == "ok" and r.get("moeda")})


def fontes_e_licencas(resultados: Sequence[Optional[Dict[str, Any]]]) -> List[str]:
    vistas: List[str] = []
    for r in resultados:
        if r and r.get("status") == "ok":
            for linha in (r.get("fonte_da_chuva") or {}).get("credit_and_licence", []):
                if linha not in vistas:
                    vistas.append(linha)
    return vistas


def avisos_do_estudo(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> List[str]:
    avisos: List[str] = []
    ok = [r for r in resultados if r and r.get("status") == "ok"]
    pede_custo = [m for m in plano["saidas"]["metricas"] if m in METRICAS_DE_CUSTO]
    if pede_custo:
        zerados = [r["id"] for r in ok if (r.get("metricas", {}).get("capex") in (0, 0.0))]
        if zerados:
            avisos.append(_txt("sem_custos", idioma, ", ".join(zerados)))
    moedas = moedas_dos_casos(ok)
    if len(moedas) > 1 and any(METRICAS[m]["unidade"] == _M for m in plano["saidas"]["metricas"]):
        avisos.append(_txt("moedas_mistas", idioma, ", ".join(moedas)))
    if any("E-OBS" in linha for linha in fontes_e_licencas(ok)):
        avisos.append(_txt("eobs", idioma))
    seen = set()
    for r in ok:
        for a in r.get("alertas", []):
            tag = f"{r['id']}: {a}"
            if tag not in seen:
                seen.add(tag)
                avisos.append(tag)
    return avisos


def _celula(valor: Optional[float], casas: int, idioma: str, milhar: bool, vazio: str) -> str:
    texto = formatar_numero(valor, casas, idioma, milhar)
    return vazio if texto is None else texto


def montar_tabela(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str,
                  vazio: str = "—") -> Dict[str, Any]:
    """A tabela para o artigo: cabeçalho, linhas de texto e as unidades. Respeita ``saidas.orientacao``."""
    metricas = plano["saidas"]["metricas"]
    milhar = plano["saidas"]["milhar"]
    casos = plano["casos"]
    com_grupo = len({c["grupo"] for c in casos}) > 1
    cab: List[str] = [_txt("caso", idioma)] + ([_txt("grupo", idioma)] if com_grupo else [])
    unidades_comuns: Dict[str, Optional[str]] = {}
    for m in metricas:
        unidades = {unidade_da_metrica(m, r, idioma) for r in resultados if r and r.get("status") == "ok"}
        unidades_comuns[m] = next(iter(unidades)) if len(unidades) == 1 else (None if unidades else unidade_da_metrica(m, None, idioma))
    colunas = []
    for m in metricas:
        un = unidades_comuns[m]
        colunas.append(f"{rotulo_da_metrica(m, idioma)} ({un})" if un else rotulo_da_metrica(m, idioma))
    linhas: List[List[str]] = []
    for caso, r in zip(casos, resultados):
        linha = [caso["nome"]] + ([caso["grupo"]] if com_grupo else [])
        for m in metricas:
            txt = _celula(_valor(r, m), _casas(plano, m), idioma, milhar, vazio)
            if txt != vazio and unidades_comuns[m] is None:
                txt = f"{txt} {unidade_da_metrica(m, r, idioma)}"
            linha.append(txt)
        linhas.append(linha)
    cabecalho = cab + colunas
    if plano["saidas"]["orientacao"] == "metricas_nas_linhas":
        cabecalho = [_txt("metrica", idioma)] + [linha[0] for linha in linhas]
        transposta = []
        for j, m in enumerate(metricas):
            ncol = len(cab) + j
            transposta.append([colunas[j]] + [linha[ncol] for linha in linhas])
        if com_grupo:
            transposta.insert(0, [_txt("grupo", idioma)] + [c["grupo"] for c in casos])
        linhas = transposta
    return {"cabecalho": cabecalho, "linhas": linhas, "numericas_a_partir_de": 1 if plano["saidas"]["orientacao"] == "metricas_nas_linhas"
            else len(cab)}


def _legenda(plano: Dict[str, Any], idioma: str) -> str:
    e = plano["estudo"]
    if plano["saidas"]["legenda"]:
        return plano["saidas"]["legenda"]
    titulo = e["titulo"] if e["titulo"] and not _pendente(e["titulo"]) else e["id"]
    return f"{_txt('tabela_de', idioma)}: {titulo}"


def _md_escape(texto: str) -> str:
    return str(texto).replace("|", "\\|").replace("\n", " ")


def tabela_md(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> str:
    tab = montar_tabela(plano, resultados, idioma)
    n0 = tab["numericas_a_partir_de"]
    cab = "| " + " | ".join(_md_escape(c) for c in tab["cabecalho"]) + " |"
    sep = "| " + " | ".join(":---" if i < n0 else "---:" for i in range(len(tab["cabecalho"]))) + " |"
    corpo = ["| " + " | ".join(_md_escape(c) for c in linha) + " |" for linha in tab["linhas"]]
    notas = []
    fontes = fontes_e_licencas(resultados)
    for a in avisos_do_estudo(plano, resultados, idioma):
        notas.append(f"- {a}")
    notas += [f"- {f}" for f in fontes]
    partes = [f"**{_legenda(plano, idioma)}**", "", cab, sep, *corpo]
    if notas:
        partes += ["", *notas]
    return "\n".join(partes) + "\n"


_TEX_ESPECIAIS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
                  "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def tex_escape(texto: str) -> str:
    """Escapa um texto para LaTeX (pdflatex): especiais, ²/³, φ, travessões e CO2."""
    saida = "".join(_TEX_ESPECIAIS.get(ch, ch) for ch in str(texto))
    saida = (saida.replace("CO2", "CO$_2$").replace("m³", "m$^3$").replace("m²", "m$^2$").replace("²", "$^2$").replace("³", "$^3$")
             .replace("φ", "$\\varphi$").replace("—", "---").replace("–", "--").replace("≥", "$\\geq$").replace("·", r"\textperiodcentered{}")
             .replace("°", r"\textdegree{}").replace("«", "``").replace("»", "''"))
    return saida


def tabela_tex(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> str:
    tab = montar_tabela(plano, resultados, idioma, vazio="--")
    n0 = tab["numericas_a_partir_de"]
    cols = "".join("l" if i < n0 else "r" for i in range(len(tab["cabecalho"])))
    linhas = ["% " + _txt("gerado", idioma) + f" Triton {__version__} ({rotulo_da_edicao(True)}); " + "estudo " + plano["estudo"]["id"],
              "% requires \\usepackage{booktabs}",
              "\\begin{table}[ht]", "\\centering", f"\\caption{{{tex_escape(_legenda(plano, idioma))}}}",
              f"\\label{{tab:{re.sub(r'[^A-Za-z0-9:_-]', '-', plano['estudo']['id'])}}}",
              "\\small", f"\\begin{{tabular}}{{{cols}}}", "\\toprule",
              " & ".join(tex_escape(c) for c in tab["cabecalho"]) + " \\\\", "\\midrule"]
    for linha in tab["linhas"]:
        linhas.append(" & ".join(tex_escape(c) for c in linha) + " \\\\")
    linhas += ["\\bottomrule", "\\end{tabular}"]
    notas = avisos_do_estudo(plano, resultados, idioma) + fontes_e_licencas(resultados)
    if notas:
        linhas += ["\\par\\smallskip", "{\\footnotesize " + " ".join(tex_escape(n) for n in notas) + "}"]
    linhas.append("\\end{table}")
    return "\n".join(linhas) + "\n"


def csv_tidy(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> str:
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    dims = list(dict.fromkeys(k for c in plano["casos"] for k in c.get("dimensoes", {})))
    w.writerow(["estudo_id", "caso_id", "caso", "grupo", *dims, "metrica", "rotulo", "valor", "unidade", "status"])
    for caso, r in zip(plano["casos"], resultados):
        status = r.get("status", "pendente") if r else "pendente"
        colunas_dim = [caso.get("dimensoes", {}).get(k, "") for k in dims]
        for m in plano["saidas"]["metricas"]:
            v = _valor(r, m)
            w.writerow([plano["estudo"]["id"], caso["id"], caso["nome"], caso["grupo"], *colunas_dim, m, rotulo_da_metrica(m, idioma),
                        "" if v is None else repr(_num_limpo(v)), unidade_da_metrica(m, r, idioma), status])
    return buf.getvalue()


def montar_json(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> Dict[str, Any]:
    e = plano["estudo"]
    arquivos: List[Dict[str, str]] = []
    for r in resultados:
        for a in (r or {}).get("arquivos", []):
            if a not in arquivos:
                arquivos.append(a)
    casos = []
    for caso, r in zip(plano["casos"], resultados):
        item: Dict[str, Any] = {"id": caso["id"], "nome": caso["nome"], "grupo": caso["grupo"],
                                "status": (r or {}).get("status", "pendente")}
        if caso.get("dimensoes"):
            item["dimensoes"] = caso["dimensoes"]
        if r and r.get("status") == "ok":
            item.update({"volume_selecionado_l": r.get("volume_selecionado_l"), "criterio_do_volume": r.get("criterio_do_volume"),
                         "metricas": {m: _num_limpo(_valor(r, m)) for m in plano["saidas"]["metricas"]},
                         "unidades": {m: unidade_da_metrica(m, r, idioma) for m in plano["saidas"]["metricas"]},
                         "moeda": r.get("moeda"), "fonte_da_chuva": r.get("fonte_da_chuva"),
                         "arquivos": r.get("arquivos", []), "alertas": r.get("alertas", [])})
        elif r:
            item["erro"] = r.get("erro", "")
        casos.append(item)
    return {
        "esquema": {"nome": ESQUEMA_RESULTADOS, "versao": 1},
        "estudo": {"id": e["id"], "titulo": e["titulo"], "tipologia": e["tipologia"], "autores": e["autores"], "nota": e["nota"]},
        "analise": plano["analise"],
        "metricas": [{"id": m, "rotulo": rotulo_da_metrica(m, idioma), "unidade_padrao": METRICAS[m]["unidade"],
                      "casas_decimais": _casas(plano, m)} for m in plano["saidas"]["metricas"]],
        "proveniencia": {
            "triton": {"versao": __version__, "edicao": get_current_edition(), "nome_da_edicao": rotulo_da_edicao()},
            "estudo": {"arquivo": "estudo.json", "sha256": plano["sha256"], "esquema_versao": ESQUEMA_VERSAO},
            "arquivos": arquivos,
            "data_de_execucao": data_de_execucao(),
        },
        "fontes_da_chuva_e_licencas": fontes_e_licencas(resultados),
        "avisos": avisos_do_estudo(plano, resultados, idioma),
        "casos": casos,
    }


def estatisticas(valores: Sequence[float]) -> Dict[str, Optional[float]]:
    v = [x for x in valores if x is not None]
    if not v:
        return {"n": 0, "minimo": None, "mediana": None, "media": None, "maximo": None}
    return {"n": len(v), "minimo": min(v), "mediana": statistics.median(v), "media": statistics.fmean(v), "maximo": max(v)}


def resumo_md(plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str, formatos: Sequence[str]) -> str:
    e = plano["estudo"]
    ok = [r for r in resultados if r and r.get("status") == "ok"]
    erros = [r for r in resultados if r and r.get("status") == "erro"]
    pend = [c for c, r in zip(plano["casos"], resultados) if r is None]
    titulo = e["titulo"] if e["titulo"] and not _pendente(e["titulo"]) else e["id"]
    rot_tip = e.get("tipologia_rotulo") or rotulo_da_tipologia(e["tipologia"], idioma)
    crit = plano["analise"]["volume"]
    crit_txt = _txt("crit_topsis", idioma) if crit == "topsis" else (_txt("crit_otimo_tecnico", idioma) if crit == "otimo_tecnico"
                                                                       else f"{formatar_numero(crit, 0, idioma)} L ({_txt('crit_fixo', idioma)})")
    linhas = [f"# {_txt('resumo', idioma)}: {titulo}", "",
              f"- {_txt('tipologia', idioma)}: {rot_tip}",
              f"- {_txt('casos', idioma)}: {len(plano['casos'])} ({len(ok)} {_txt('rodados', idioma)}"
              + (f", {len(erros)} {_txt('com_erro', idioma)}" if erros else "")
              + (f", {len(pend)} {_txt('pendentes', idioma)}" if pend else "") + ")",
              f"- {_txt('analise', idioma)}: {plano['analise']['tipo']}; {_txt('volume_criterio', idioma)}: {crit_txt}"]
    if e["autores"]:
        linhas.append("- " + ", ".join(e["autores"]))
    if e["nota"]:
        linhas.append(f"- {e['nota']}")
    # faixa dos principais resultados
    faixa = []
    for m in plano["saidas"]["metricas"]:
        if m == "volume_l":
            continue
        vals = [_valor(r, m) for r in ok]
        un = {unidade_da_metrica(m, r, idioma) for r in ok}
        if len(un) != 1 or not any(v is not None for v in vals):
            continue
        s = estatisticas([v for v in vals if v is not None])
        c = _casas(plano, m)
        mi, ma = formatar_numero(s["minimo"], c, idioma, plano["saidas"]["milhar"]), formatar_numero(s["maximo"], c, idioma, plano["saidas"]["milhar"])
        faixa.append(f"- {rotulo_da_metrica(m, idioma)}: {mi} – {ma} {next(iter(un))}")
    if faixa:
        linhas += ["", f"## {_txt('faixa', idioma)}", "", *faixa]
    avisos = avisos_do_estudo(plano, resultados, idioma)
    if avisos:
        linhas += ["", f"## {_txt('avisos', idioma)}", "", *[f"- {a}" for a in avisos]]
    fontes = fontes_e_licencas(resultados)
    if fontes:
        linhas += ["", f"## {_txt('fontes', idioma)}", "", *[f"- {f}" for f in fontes]]
    if erros:
        linhas += ["", f"## {_txt('falhas', idioma)}", "", *[f"- {r['id']}: {r.get('erro', '')}" for r in erros]]
    nomes = {"csv": "resultados.csv", "json": "resultados.json", "md": "tabela.md", "tex": "tabela.tex", "xlsx": "tabela.xlsx"}
    linhas += ["", f"## {_txt('arquivos', idioma)}", "", *[f"- {nomes[f]}" for f in formatos if f in nomes]]
    linhas += ["", f"{_txt('gerado', idioma)} Triton {__version__} ({_txt('edicao', idioma)} {rotulo_da_edicao(True)}); "
                   f"estudo.json SHA-256 {plano['sha256'][:12]}."]
    return "\n".join(linhas) + "\n"


def tabela_xlsx(caminho: Path, plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]], idioma: str) -> bool:
    """Grava o XLSX (valores numéricos de verdade). Devolve ``False`` se o openpyxl não está instalado."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError:
        return False
    wb = Workbook()
    wb.properties.creator = f"Triton {__version__}"
    wb.properties.created = wb.properties.modified = datetime.strptime(data_de_execucao(), "%Y-%m-%d")
    ws = wb.active
    ws.title = "tabela"
    metricas = plano["saidas"]["metricas"]
    com_grupo = len({c["grupo"] for c in plano["casos"]}) > 1
    cab = [_txt("caso", idioma)] + ([_txt("grupo", idioma)] if com_grupo else [])
    for m in metricas:
        un = {unidade_da_metrica(m, r, idioma) for r in resultados if r and r.get("status") == "ok"}
        cab.append(f"{rotulo_da_metrica(m, idioma)} ({next(iter(un))})" if len(un) == 1 else rotulo_da_metrica(m, idioma))
    ws.append(cab)
    for c in ws[1]:
        c.font = Font(bold=True)
    for caso, r in zip(plano["casos"], resultados):
        linha = [caso["nome"]] + ([caso["grupo"]] if com_grupo else [])
        linha += [_num_limpo(_valor(r, m)) for m in metricas]
        ws.append(linha)
        for j, m in enumerate(metricas):
            cel = ws.cell(row=ws.max_row, column=len(cab) - len(metricas) + j + 1)
            casas = _casas(plano, m)
            cel.number_format = "0" if casas == 0 else "0." + "0" * casas
    ws.freeze_panes = "B2"
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = min(48, max(10, max(len(str(c.value or "")) for c in col) + 2))
    tidy = wb.create_sheet("tidy")
    for linha in csv.reader(io.StringIO(csv_tidy(plano, resultados, idioma))):
        tidy.append(linha)
    prov = wb.create_sheet("proveniencia")
    dados = montar_json(plano, resultados, idioma)
    pv = dados["proveniencia"]
    for k, v in (("triton", pv["triton"]["versao"]), ("edicao", pv["triton"]["edicao"]), ("estudo_sha256", pv["estudo"]["sha256"]),
                 ("data_de_execucao", pv["data_de_execucao"])):
        prov.append([k, v])
    for a in pv["arquivos"]:
        prov.append([a["papel"], a["caminho"], a["sha256"]])
    for linha in dados["fontes_da_chuva_e_licencas"]:
        prov.append(["fonte", linha])
    caminho.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(caminho))
    return True


def escrever_saidas(saida: Path, plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]],
                    idioma: Optional[str] = None) -> List[str]:
    """Escreve resultados.csv/json, tabela.md/tex/xlsx e resumo.md na pasta de saída. Devolve os nomes gravados."""
    saida = Path(saida)
    lingua = _idioma_do_plano(plano, idioma)
    formatos = plano["saidas"]["formatos"]
    gravados: List[str] = []
    if "csv" in formatos:
        _escrever(saida / "resultados.csv", csv_tidy(plano, resultados, lingua))
        gravados.append("resultados.csv")
    if "json" in formatos:
        _escrever(saida / "resultados.json", _json_texto(montar_json(plano, resultados, lingua)))
        gravados.append("resultados.json")
    if "md" in formatos:
        _escrever(saida / "tabela.md", tabela_md(plano, resultados, lingua))
        gravados.append("tabela.md")
    if "tex" in formatos:
        _escrever(saida / "tabela.tex", tabela_tex(plano, resultados, lingua))
        gravados.append("tabela.tex")
    if "xlsx" in formatos:
        if tabela_xlsx(saida / "tabela.xlsx", plano, resultados, lingua):
            gravados.append("tabela.xlsx")
    _escrever(saida / "resumo.md", resumo_md(plano, resultados, lingua, formatos))
    gravados.append("resumo.md")
    return gravados


# ══ Resumo: refaz as tabelas de uma pasta de saída ═════════════════════════════════════════════

def carregar_saida(pasta: Path, estudo_alternativo: Optional[Path] = None) -> Tuple[Dict[str, Any], List[Optional[Dict[str, Any]]]]:
    """Lê o ``estudo.json`` copiado na pasta de saída e os resultados dos casos (``None`` para o que não foi calculado)."""
    pasta = Path(pasta)
    arq = Path(estudo_alternativo) if estudo_alternativo else pasta / "estudo.json"
    if not arq.is_file():
        raise FileNotFoundError(_m("{0} não tem estudo.json; é a pasta de saída de «triton estudo run»?", pasta.name))
    doc, sha = ler_documento(arq)
    plano, erros, _ = validar_documento(doc, arq.resolve().parent, verificar_arquivos=False)
    if erros:
        raise ErroDeEstudo(erros)
    plano["sha256"] = sha
    plano["caminho"] = arq.resolve()
    plano["base_dir"] = arq.resolve().parent
    return plano, [ler_resultado_do_caso(pasta, c["id"]) for c in plano["casos"]]


def refazer_resumo(pasta: Path, estudo_alternativo: Optional[Path] = None, idioma: Optional[str] = None) -> List[str]:
    plano, resultados = carregar_saida(pasta, estudo_alternativo)
    if not any(resultados):
        raise ValueError(_m("a pasta de saída não tem resultados de casos; execute «triton estudo run» primeiro"))
    return escrever_saidas(Path(pasta), plano, resultados, idioma)


# ══ Texto: marcadores {{metrica:caso}} ═════════════════════════════════════════════════════════

_RE_MARCADOR = re.compile(r"\{\{\s*([^{}]*?)\s*\}\}")
_RE_AGREGADO = re.compile(r"^@(min|max|media|mediana)(?:\(([^)]+)\))?$")


def substituir_marcadores(modelo: str, plano: Dict[str, Any], resultados: Sequence[Optional[Dict[str, Any]]],
                          idioma: str) -> Tuple[str, List[str]]:
    """Troca ``{{metrica:caso}}``, ``{{metrica:@min}}``, ``{{metrica:@media(grupo)}}`` e ``{{n_casos}}`` por números reais.

    Onde falta resultado o marcador vira «XX» e entra na lista de pendências. Métrica desconhecida é erro.
    """
    por_id = {c["id"]: (c, r) for c, r in zip(plano["casos"], resultados)}
    ok = [(c, r) for c, r in zip(plano["casos"], resultados) if r and r.get("status") == "ok"]
    faltas: List[str] = []
    milhar = plano["saidas"]["milhar"]

    def trocar(m: "re.Match[str]") -> str:
        corpo = m.group(1)
        marcador = m.group(0)
        if corpo == "n_casos":
            return str(len(ok))
        partes = [p.strip() for p in corpo.split(":", 1)]
        if len(partes) != 2:
            raise ValueError(_m("marcador inválido: {0}. Use a forma metrica:caso, metrica:@min, metrica:@max, metrica:@media, metrica:@mediana ou n_casos.", marcador))
        nome, resto = partes
        casas_pedidas = None
        if "|" in resto:
            resto, ps = [x.strip() for x in resto.split("|", 1)]
            try:
                casas_pedidas = int(ps)
            except ValueError:
                raise ValueError(_m("marcador inválido: {0} (as casas depois de | devem ser um inteiro)", marcador)) from None
        metrica = metrica_canonica(nome)
        if metrica is None:
            raise ValueError(_m("marcador {0}: métrica desconhecida «{1}».", marcador, nome) + _sugestao(nome, list(METRICAS)))
        casas = casas_pedidas if casas_pedidas is not None else _casas(plano, metrica)
        ag = _RE_AGREGADO.match(resto)
        if ag:
            tipo, grupo = ag.group(1), ag.group(2)
            vals = [_valor(r, metrica) for c, r in ok if grupo is None or c["grupo"] == grupo]
            vals = [v for v in vals if v is not None]
            if not vals:
                faltas.append(marcador)
                return "«XX»"
            v = {"min": min, "max": max, "media": statistics.fmean, "mediana": statistics.median}[tipo](vals)
        else:
            achado = por_id.get(resto)
            if achado is None:
                faltas.append(marcador)
                return "«XX»"
            v = _valor(achado[1], metrica)
        texto = formatar_numero(v, casas, idioma, milhar)
        if texto is None:
            faltas.append(marcador)
            return "«XX»"
        return texto

    return _RE_MARCADOR.sub(trocar, modelo), faltas


# ══ Lote: vários estudos e o comparativo entre tipologias ═════════════════════════════════════

def descobrir_estudos(pasta: Path, recursivo: bool = False) -> List[Path]:
    pasta = Path(pasta)
    if not pasta.is_dir():
        raise FileNotFoundError(_m("Pasta não encontrada: {0}", pasta.name))
    achados = sorted(pasta.rglob("estudo*.json") if recursivo else pasta.glob("estudo*.json"),
                     key=lambda p: p.relative_to(pasta).as_posix())
    achados = [p for p in achados if p.is_file()]
    if not achados:
        raise ValueError(_m("nenhum estudo*.json em {0} (use --recursivo para procurar nas subpastas)", pasta.name))
    return achados


def comparativo(planos: Sequence[Dict[str, Any]], resultados: Sequence[Sequence[Optional[Dict[str, Any]]]], idioma: str
                ) -> Dict[str, Any]:
    comuns = [m for m in planos[0]["saidas"]["metricas"] if all(m in p["saidas"]["metricas"] for p in planos)]
    if not comuns:
        raise ValueError(_m("os estudos não têm nenhuma métrica em comum para comparar"))
    linhas = []
    for plano, res in zip(planos, resultados):
        ok = [r for r in res if r and r.get("status") == "ok"]
        item = {"estudo_id": plano["estudo"]["id"], "tipologia": plano["estudo"]["tipologia"],
                "titulo": plano["estudo"]["titulo"], "casos": len(plano["casos"]), "casos_calculados": len(ok), "metricas": {}}
        for m in comuns:
            unidades = {unidade_da_metrica(m, r, idioma) for r in ok}
            monetaria = METRICAS[m]["unidade"] == _M
            if monetaria and len(unidades) > 1:
                est, un = estatisticas([]), "—"
            else:
                est = estatisticas([_valor(r, m) for r in ok])
                un = next(iter(unidades)) if unidades else unidade_da_metrica(m, None, idioma)
            item["metricas"][m] = {**{k: (v if k == "n" else _num_limpo(v)) for k, v in est.items()}, "unidade": un}
        linhas.append(item)
    return {"metricas": comuns, "estudos": linhas}


def comparativo_csv(comp: Dict[str, Any], idioma: str) -> str:
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["estudo_id", "tipologia", "metrica", "rotulo", "n", "minimo", "mediana", "media", "maximo", "unidade"])
    for e in comp["estudos"]:
        for m in comp["metricas"]:
            s = e["metricas"][m]
            w.writerow([e["estudo_id"], e["tipologia"], m, rotulo_da_metrica(m, idioma), s["n"]]
                       + ["" if s[k] is None else repr(s[k]) for k in ("minimo", "mediana", "media", "maximo")] + [s["unidade"]])
    return buf.getvalue()


def _tabela_do_comparativo(comp: Dict[str, Any], planos: Sequence[Dict[str, Any]], idioma: str, vazio: str) -> Dict[str, Any]:
    cab = [_txt("tipologia", idioma), _txt("casos", idioma)]
    for m in comp["metricas"]:
        un = {e["metricas"][m]["unidade"] for e in comp["estudos"]}
        cab.append(f"{rotulo_da_metrica(m, idioma)} ({next(iter(un))})" if len(un) == 1 else rotulo_da_metrica(m, idioma))
    linhas = []
    for e, plano in zip(comp["estudos"], planos):
        nome = plano["estudo"].get("tipologia_rotulo") or rotulo_da_tipologia(e["tipologia"], idioma)
        linha = [nome, f"{e['casos_calculados']}/{e['casos']}"]
        for m in comp["metricas"]:
            s = e["metricas"][m]
            c = _casas(plano, m)
            if s["n"] == 0 or s["media"] is None:
                linha.append(vazio)
            else:
                f = lambda v: formatar_numero(v, c, idioma, plano["saidas"]["milhar"])
                linha.append(f"{f(s['media'])} ({f(s['minimo'])}–{f(s['maximo'])})")
        linhas.append(linha)
    return {"cabecalho": cab, "linhas": linhas}


def comparativo_md(comp: Dict[str, Any], planos: Sequence[Dict[str, Any]], resultados, idioma: str) -> str:
    tab = _tabela_do_comparativo(comp, planos, idioma, "—")
    partes = [f"**{_txt('comparativo', idioma)}** — {_txt('media_faixa', idioma)}", "",
              "| " + " | ".join(_md_escape(c) for c in tab["cabecalho"]) + " |",
              "| :--- | ---: " + "| ---: " * len(comp["metricas"]) + "|",
              *["| " + " | ".join(_md_escape(c) for c in l) + " |" for l in tab["linhas"]]]
    todos = [r for res in resultados for r in res]
    notas = [f"- {f}" for f in fontes_e_licencas(todos)]
    if any("E-OBS" in f for f in fontes_e_licencas(todos)):
        notas.insert(0, f"- {_txt('eobs', idioma)}")
    if notas:
        partes += ["", *notas]
    return "\n".join(partes) + "\n"


def comparativo_tex(comp: Dict[str, Any], planos: Sequence[Dict[str, Any]], resultados, idioma: str) -> str:
    tab = _tabela_do_comparativo(comp, planos, idioma, "--")
    cols = "ll" + "r" * len(comp["metricas"])
    linhas = ["% requires \\usepackage{booktabs}", "\\begin{table}[ht]", "\\centering",
              f"\\caption{{{tex_escape(_txt('comparativo', idioma))}: {tex_escape(_txt('media_faixa', idioma))}}}",
              "\\label{tab:comparativo}", "\\small", f"\\begin{{tabular}}{{{cols}}}", "\\toprule",
              " & ".join(tex_escape(c) for c in tab["cabecalho"]) + " \\\\", "\\midrule"]
    linhas += [" & ".join(tex_escape(c) for c in l).replace("–", "--") + " \\\\" for l in tab["linhas"]]
    linhas += ["\\bottomrule", "\\end{tabular}"]
    todos = [r for res in resultados for r in res]
    notas = fontes_e_licencas(todos)
    if any("E-OBS" in f for f in notas):
        notas.insert(0, _txt("eobs", idioma))
    if notas:
        linhas += ["\\par\\smallskip", "{\\footnotesize " + " ".join(tex_escape(n) for n in notas) + "}"]
    linhas.append("\\end{table}")
    return "\n".join(linhas) + "\n"


def rodar_lote(pasta: Path, saida: Path, recursivo: bool = False, retomar: bool = False, sobrescrever: bool = False,
               paralelo: int = 1, idioma: Optional[str] = None, log: Optional[Callable[[str], None]] = None
               ) -> Tuple[List[Execucao], List[str]]:
    """Roda cada ``estudo*.json`` da pasta e escreve o comparativo entre tipologias na raiz da saída."""
    log = log or (lambda _m_: None)
    arquivos = descobrir_estudos(pasta, recursivo)
    planos = []
    for a in arquivos:
        plano, _ = carregar_plano(a)
        planos.append(plano)
    ids = [p["estudo"]["id"].lower() for p in planos]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise ValueError(_m("ids de estudo repetidos no lote: {0}", ", ".join(repetidos)))
    saida = Path(saida)
    execucoes: List[Execucao] = []
    for plano in planos:
        log(_m("Estudo {0} ({1} casos)", plano["estudo"]["id"], len(plano["casos"])))
        execucoes.append(rodar_estudo(plano["caminho"], saida / plano["estudo"]["id"], retomar, sobrescrever, paralelo, log))
    lingua = resolver_idioma(idioma if idioma else planos[0]["saidas"]["idioma"])
    resultados = [e.resultados for e in execucoes]
    comp = comparativo(planos, resultados, lingua)
    _escrever(saida / "comparativo.csv", comparativo_csv(comp, lingua))
    _escrever(saida / "comparativo.md", comparativo_md(comp, planos, resultados, lingua))
    _escrever(saida / "comparativo.tex", comparativo_tex(comp, planos, resultados, lingua))
    _escrever(saida / "comparativo.json", _json_texto({
        "esquema": {"nome": ESQUEMA_COMPARATIVO, "versao": 1},
        "triton": {"versao": __version__, "edicao": get_current_edition()},
        "data_de_execucao": data_de_execucao(),
        "estudos": [{"estudo_id": p["estudo"]["id"], "estudo_sha256": p["sha256"]} for p in planos],
        "metricas": [{"id": m, "rotulo": rotulo_da_metrica(m, lingua)} for m in comp["metricas"]],
        "comparativo": comp["estudos"],
        "fontes_da_chuva_e_licencas": fontes_e_licencas([r for res in resultados for r in res]),
    }))
    return execucoes, ["comparativo.csv", "comparativo.md", "comparativo.tex", "comparativo.json"]


# ══ Esqueleto (estudo init) e esquema JSON ════════════════════════════════════════════════════

def identificador_da_pasta(nome: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", nome.strip()).strip("-._") or "estudo"
    return base[:64]


def esqueleto(pasta: Path, tipologia: str = "residencial-unifamiliar") -> Dict[str, Any]:
    """O ``estudo.json`` de partida: estrutura e rótulos da tipologia, nenhum valor preenchido (null, vazio ou «XX»)."""
    canon = tipologia_canonica(tipologia) or TIPOLOGIA_OUTRA
    dica = TIPOLOGIAS[canon]["usuarios"][1 if is_int_edition() else 0] if canon in TIPOLOGIAS else ""
    caso = lambda n: {
        "id": f"caso-{n:02d}", "nome": _SEM_DADO, "grupo": canon,
        "clima": {"arquivo": _SEM_DADO, "nome": _SEM_DADO},
        "substituicoes": {"area_captacao_m2": None, "usuarios": None, "demanda_per_capita_l_dia": None, "fracao_pluvial_pct": None},
    }
    return {
        "_comentario": _m("Esqueleto de «triton estudo init»: nenhum valor foi preenchido pelo programa. Substitua os «XX» e os null pelos dados do seu estudo (com a fonte de cada um) e execute «triton estudo validate». Chaves iniciadas por _ são comentários."),
        "esquema": {"nome": ESQUEMA_NOME, "versao": ESQUEMA_VERSAO},
        "estudo": {"id": identificador_da_pasta(Path(pasta).name), "titulo": _SEM_DADO, "tipologia": canon, "autores": [], "nota": "",
                   "_comentario": _m("tipologia: só rótulo e estrutura; os números vêm dos casos. usuarios, nesta tipologia: {0}", dica)},
        "projeto_base": {"arquivo": _SEM_DADO,
                         "_comentario": _m("Caminho do .triton base, relativo a este arquivo (ou {{\"modelo\": \"edicao\"}} para partir do modelo da edição, caso em que cada caso informa área, demanda, fração e chuva). Um caso pode usar outro projeto no campo «projeto».")},
        "padroes": {"_comentario": _m("Tudo o que vale para todos os casos: substituicoes e clima. O que o caso declara vence o padrão."),
                    "substituicoes": {}, "clima": {}},
        "casos": [caso(1), caso(2), caso(3)],
        "analise": {"tipo": "technical", "volume": "otimo_tecnico", "semente": 42,
                    "_comentario": _m("tipo: technical, economic ou all. volume: otimo_tecnico, topsis ou um volume em litros.")},
        "saidas": {"formatos": list(FORMATOS_PADRAO), "metricas": list(METRICAS_PADRAO[0]), "casas_decimais": {"padrao": 1},
                   "idioma": "auto",
                   "_comentario": _m("formatos: csv, json, md, tex, xlsx. Métricas e apelidos: «triton estudo apelidos».")},
    }


def modelo_de_texto(tipologia: str) -> str:
    """Modelo de resumo com marcadores; o texto é só estrutura, os números vêm dos resultados."""
    canon = tipologia_canonica(tipologia) or TIPOLOGIA_OUTRA
    rotulo = rotulo_da_tipologia(canon, "en" if is_int_edition() else "pt-BR").lower()
    return _m("# Modelo de texto: resumo para congresso\n\nEste estudo avaliou {{{{n_casos}}}} edifícios (tipologia: {0}). Com o reservatório no volume de cada caso, a economia de água potável variou de {{{{economia_agua_potavel_pct:@min}}}}% a {{{{economia_agua_potavel_pct:@max}}}}% (mediana de {{{{economia_agua_potavel_pct:@mediana}}}}%). XX\n\nSubstitua o texto livre pela sua redação; cada marcador vira o número real depois de «triton estudo texto». Onde faltar resultado fica «XX».\n", rotulo)


def esquema_json() -> Dict[str, Any]:
    """JSON Schema (rascunho 2020-12) da estrutura do ``estudo.json``; a validação completa (apelidos, faixas) é a do Triton."""
    substituicoes = {"type": "object", "propertyNames": {"anyOf": [{"enum": list(APELIDOS)}, {"pattern": "^_"}, {"pattern": r"^(" + "|".join(SECOES_DO_TRITON) + r")\."},
                                                                  {"pattern": "^config\\."}, {"enum": list(campos_do_config())}]},
                     "description": "apelido, campo do projeto ou caminho pontilhado do .triton -> valor"}
    clima = {"type": "object", "additionalProperties": False, "patternProperties": {"^_": {}},
             "properties": {"arquivo": {"type": "string"}, "data_inicio": {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"},
                            "nome": {"type": "string"}, "fonte": {"type": "string"},
                            "climbra": {"type": "object", "additionalProperties": False, "patternProperties": {"^_": {}},
                                        "properties": {k: {"type": "string"} for k in CHAVES_DO_CLIMBRA}}}}
    tarifa = {"type": "object", "additionalProperties": False, "patternProperties": {"^_": {}},
              "properties": {"municipio": {"type": "string"}, "uf": {"type": "string"}, "categoria": {"type": "string"},
                             "se_ausente": {"enum": ["erro", "residencial"]}}}
    expansao = {"type": "object", "additionalProperties": False, "patternProperties": {"^_": {}},
                "required": ["municipios", "recortes"],
                "properties": {"uf": {"type": "string"},
                               "municipios": {"type": "array", "minItems": 1,
                                              "items": {"type": "object", "required": ["municipio"],
                                                        "properties": {"municipio": {"type": "string"}, "uf": {"type": "string"},
                                                                       "ibge": {"type": "string", "pattern": "^\\d{7}$"}}}},
                               "modelos": {"anyOf": [{"const": "todos"}, {"type": "array", "items": {"type": "string"}, "minItems": 1}]},
                               "recortes": {"type": "array", "minItems": 1,
                                            "items": {"type": "object", "required": ["id", "cenario", "inicio", "fim"],
                                                      "properties": {"id": {"type": "string", "pattern": _RE_ID.pattern},
                                                                     "rotulo": {"type": "string"},
                                                                     "cenario": {"enum": list(CENARIOS_CLIMBRA)},
                                                                     "inicio": {"type": "string"}, "fim": {"type": "string"}}}}}}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "triton-estudo (versão 1)",
        "type": "object",
        "required": ["esquema", "estudo"],
        "anyOf": [{"required": ["casos"]}, {"required": ["expansao"]}],
        "properties": {
            "esquema": {"type": "object", "required": ["nome", "versao"],
                        "properties": {"nome": {"const": ESQUEMA_NOME}, "versao": {"const": ESQUEMA_VERSAO}}},
            "estudo": {"type": "object", "required": ["id", "tipologia"],
                       "properties": {"id": {"type": "string", "pattern": _RE_ID.pattern},
                                      "titulo": {"type": "string"},
                                      "tipologia": {"type": "string"},
                                      "tipologia_rotulo": {"type": "string"},
                                      "autores": {"type": "array", "items": {"type": "string"}},
                                      "nota": {"type": "string"}}},
            "projeto_base": {"type": "object", "properties": {"arquivo": {"type": "string"}, "modelo": {"const": "edicao"}}},
            "padroes": {"type": "object", "properties": {"substituicoes": substituicoes, "clima": clima, "tarifa": tarifa}},
            "expansao": expansao,
            "casos": {"type": "array", "minItems": 1,
                      "items": {"type": "object", "required": ["id"],
                                "properties": {"id": {"type": "string", "pattern": _RE_ID.pattern}, "nome": {"type": "string"},
                                               "grupo": {"type": "string"}, "projeto": {"type": "string"},
                                               "clima": clima, "tarifa": tarifa, "substituicoes": substituicoes,
                                               "dimensoes": {"type": "object"}}}},
            "analise": {"type": "object", "properties": {
                "tipo": {"enum": list(TIPOS_DE_ANALISE)},
                "volume": {"anyOf": [{"enum": ["otimo_tecnico", "topsis"]}, {"type": "number", "minimum": 0}]},
                "pesos": {"type": "array", "items": {"type": "number", "minimum": 0}, "minItems": 3, "maxItems": 3},
                "semente": {"type": "integer"}}},
            "saidas": {"type": "object", "properties": {
                "formatos": {"type": "array", "items": {"enum": list(FORMATOS)}, "minItems": 1},
                "metricas": {"type": "array", "items": {"enum": list(METRICAS)}, "minItems": 1},
                "casas_decimais": {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 8}, {"type": "object"}]},
                "idioma": {"enum": list(IDIOMAS)}, "milhar": {"type": "boolean"}, "legenda": {"type": "string"},
                "gravar_analise": {"type": "boolean"},
                "orientacao": {"enum": list(ORIENTACOES)}}},
        },
    }


def texto_do_catalogo(ingles: bool) -> str:
    """As tabelas de apelidos e de métricas para o terminal e para a documentação."""
    i = 1 if ingles else 0
    linhas = [_m("Apelidos de substituição (em substituicoes; valem também campos do projeto e caminhos pontilhados do .triton):"), ""]
    for chave, d in APELIDOS.items():
        sin = f" [{', '.join(d['sin'])}]" if d["sin"] else ""
        linhas.append(f"  {chave:<26} {d['un']:<12} {d['desc'][i]}{sin}")
    linhas += ["", _m("Métricas (em saidas.metricas):"), ""]
    idioma = "en" if ingles else "pt-BR"
    for mid, m in METRICAS.items():
        un = _m("moeda do projeto") if m["unidade"] == _M else m["unidade"]
        linhas.append(f"  {mid:<30} {un:<12} {rotulo_da_metrica(mid, idioma)}")
    return "\n".join(linhas) + "\n"
