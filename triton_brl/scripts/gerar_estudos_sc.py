# -*- coding: utf-8 -*-
"""Gera os seis estudos de Santa Catarina (``estudos/santa-catarina/<estudo>/``) a partir de fontes abertas.

Uso (na pasta ``triton_brl``)::

    python scripts/gerar_estudos_sc.py            # reescreve estudo.json, LEIA.md e modelo_texto.md de cada estudo
    python scripts/gerar_estudos_sc.py --conferir # só confere que o que está no disco é o que o script geraria

Entradas (todas em ``estudos/santa-catarina/_fontes/``, com URL, data de acesso e SHA-256 em ``FONTES.json``):

* ``ibge_municipios_sc.json``: os 295 municípios de Santa Catarina e o código IBGE (API de localidades do IBGE);
* ``AerodromosPublicos.csv``: lista de aeródromos públicos da ANAC (dados abertos);
* ``vra_2025_movimentos_aeroportos_sc.csv``: movimentos realizados do Voo Regular Ativo (VRA) da ANAC em 2025,
  somados por aeródromo e mês (os 12 arquivos brutos, de cerca de 12 MB cada, estão em ``FONTES.json`` com SHA-256).

Do programa vêm a lista de cidades da CLIMBra (``data/climbra_<modelo>.db``) e a UF de cada uma (catálogo de
tarifas, ``triton/data/brazil_cities_tariffs.json``). Nenhum número de arquétipo é medido: cada um é uma
estimativa de arquétipo a refinar pelo autor, e o ``estudo.json`` o declara em ``_origem``.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PASTA = RAIZ / "estudos" / "santa-catarina"
FONTES = PASTA / "_fontes"
UF = "SC"
COD_UF_IBGE = "42"          # prefixo dos códigos IBGE dos municípios de Santa Catarina

ROTULO_ARQUETIPO = "estimativa de arquétipo, a refinar pelo autor"

#: Recortes: exatamente os atalhos de ``RECORTES_SUGERIDOS`` (triton/core/climate_database.py). O histórico usa os
#: trinta anos 1981–2010 (a duração das normais), como os três recortes futuros.
RECORTES = [
    {"id": "hist-1981-2010", "rotulo": "Histórico, 1981–2010", "cenario": "HIST", "inicio": "01/01/1981", "fim": "31/12/2010"},
    {"id": "ssp245-2021-2050", "rotulo": "SSP2-4.5, futuro próximo 2021–2050", "cenario": "SSP245", "inicio": "01/01/2021", "fim": "31/12/2050"},
    {"id": "ssp245-2041-2070", "rotulo": "SSP2-4.5, meados do século 2041–2070", "cenario": "SSP245", "inicio": "01/01/2041", "fim": "31/12/2070"},
    {"id": "ssp245-2071-2100", "rotulo": "SSP2-4.5, fim do século 2071–2100", "cenario": "SSP245", "inicio": "01/01/2071", "fim": "31/12/2100"},
    {"id": "ssp585-2021-2050", "rotulo": "SSP5-8.5, futuro próximo 2021–2050", "cenario": "SSP585", "inicio": "01/01/2021", "fim": "31/12/2050"},
    {"id": "ssp585-2041-2070", "rotulo": "SSP5-8.5, meados do século 2041–2070", "cenario": "SSP585", "inicio": "01/01/2041", "fim": "31/12/2070"},
    {"id": "ssp585-2071-2100", "rotulo": "SSP5-8.5, fim do século 2071–2100", "cenario": "SSP585", "inicio": "01/01/2071", "fim": "31/12/2100"},
]

METRICAS = [
    "volume_l",
    "volume_otimo_tecnico_l",
    "volume_otimo_economico_l",
    "volume_otimo_ambiental_l",
    "volume_topsis_l",
    "volume_smaa_vikor_l",
    "aceitabilidade_smaa_pct",
    "indice_topsis",
    "economia_agua_potavel_pct",
    "agua_pluvial_m3_ano",
    "extravasamento_m3_ano",
    "dias_atendimento_total_pct",
    "economia_anual_agua",
    "capex",
    "vpl",
    "payback_descontado_meses",
    "co2_incorporado_kg",
    "co2_evitado_ano_kg",
    "co2_liquido_vida_kg",
    "payback_ambiental_anos",
]

#: Arquétipos por tipologia. TODOS os números são estimativas de arquétipo (nenhum é dado medido nem de norma):
#: o autor os substitui pelos seus, com fonte. ``tarifa`` é só a categoria do catálogo de tarifas do programa.
ARQUETIPOS = {
    "escolar": dict(
        pasta="escolar", id="sc-escolar", tipologia="escolar", municipios="climbra",
        titulo="Edifícios escolares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="escola pública de ensino básico de porte médio",
        template_id="escola", material_inferior="FIBRA", material_superior="FIBRA",
        area_captacao_m2=1500, usuarios=600, demanda_per_capita_l_dia=50, fracao_pluvial_pct=40,
        volume_fixo_l=30000, volume_maximo_l=120000, passo_volume_l=2000, delta_ideal_pct=0.15,
        reservatorio_superior_l=8000, limiar_bombeamento_l=2000, tarifa="publica",
        bomba=dict(count=2, power_str="1,5 CV", power_kw=1.10, flow_rate_l_h=9000.0,
                   efficiency_pct=62.0, unit_cost=1350.0, manometric_head_m=18.0),
        custo_tubulacao=34000.0, custo_acessorios=19000.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção e limpeza de calhas e pré-filtros", 6, 900.0, 0.0],
            ["Limpeza e sanitização dos reservatórios", 6, 1100.0, 0.0],
            ["Manutenção preventiva do recalque e cloração", 12, 1600.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 150, "length_m": 80}, {"diameter_mm": 100, "length_m": 120}, {"diameter_mm": 50, "length_m": 90}],
        usuarios_texto="alunos, professores e funcionários presentes por dia"),
    "comercial": dict(
        pasta="comercial", id="sc-comercial", tipologia="comercial", municipios="climbra",
        titulo="Edifícios comerciais em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="edifício de escritórios e serviços de porte médio",
        template_id="comercial", material_inferior="FIBRA", material_superior="FIBRA",
        area_captacao_m2=1200, usuarios=300, demanda_per_capita_l_dia=45, fracao_pluvial_pct=50,
        volume_fixo_l=20000, volume_maximo_l=80000, passo_volume_l=1500, delta_ideal_pct=0.25,
        reservatorio_superior_l=5000, limiar_bombeamento_l=1250, tarifa="comercial",
        bomba=dict(count=2, power_str="1,5 CV", power_kw=1.10, flow_rate_l_h=7200.0,
                   efficiency_pct=62.0, unit_cost=1250.0, manometric_head_m=25.0),
        custo_tubulacao=28000.0, custo_acessorios=16000.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção e limpeza de calhas e filtros", 6, 750.0, 0.0],
            ["Limpeza e higienização dos reservatórios", 6, 950.0, 0.0],
            ["Manutenção preventiva do recalque e automação", 12, 1400.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 150, "length_m": 50}, {"diameter_mm": 100, "length_m": 90}, {"diameter_mm": 50, "length_m": 80}],
        usuarios_texto="ocupantes e visitantes presentes por dia"),
    "residencial-unifamiliar": dict(
        pasta="residencial-unifamiliar", id="sc-residencial-unifamiliar", tipologia="residencial-unifamiliar", municipios="climbra",
        titulo="Residências unifamiliares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="casa unifamiliar de padrão médio",
        template_id="res_medio", material_inferior="PEAD", material_superior="PEAD",
        area_captacao_m2=120, usuarios=4, demanda_per_capita_l_dia=150, fracao_pluvial_pct=40,
        volume_fixo_l=3000, volume_maximo_l=15000, passo_volume_l=250, delta_ideal_pct=1.50,
        reservatorio_superior_l=500, limiar_bombeamento_l=125, tarifa="residencial",
        bomba=dict(count=1, power_str="1/2 CV", power_kw=0.37, flow_rate_l_h=2400.0,
                   efficiency_pct=55.0, unit_cost=350.0, manometric_head_m=12.0),
        custo_tubulacao=1450.0, custo_acessorios=950.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção e limpeza de calhas e pré-filtro", 12, 180.0, 0.0],
            ["Limpeza e higienização dos reservatórios", 12, 220.0, 0.0],
            ["Manutenção preventiva da motobomba", 12, 150.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 100, "length_m": 24}, {"diameter_mm": 32, "length_m": 18}, {"diameter_mm": 25, "length_m": 15}],
        usuarios_texto="moradores"),
    "residencial-multifamiliar": dict(
        pasta="residencial-multifamiliar", id="sc-residencial-multifamiliar", tipologia="residencial-multifamiliar",
        municipios="climbra",
        titulo="Residências multifamiliares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="prédio residencial de 16 unidades",
        template_id="res_multi", material_inferior="FIBRA", material_superior="PEAD",
        area_captacao_m2=600, usuarios=48, economias=16, demanda_per_capita_l_dia=150, fracao_pluvial_pct=40,
        volume_fixo_l=15000, volume_maximo_l=50000, passo_volume_l=1000, delta_ideal_pct=0.30,
        reservatorio_superior_l=3000, limiar_bombeamento_l=750, tarifa="residencial",
        bomba=dict(count=2, power_str="1 CV", power_kw=0.75, flow_rate_l_h=4800.0,
                   efficiency_pct=60.0, unit_cost=750.0, manometric_head_m=22.0),
        custo_tubulacao=9500.0, custo_acessorios=5200.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção e limpeza de calhas e filtros", 6, 380.0, 0.0],
            ["Limpeza e higienização dos reservatórios", 12, 850.0, 0.0],
            ["Manutenção preventiva do recalque duplo", 12, 600.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 100, "length_m": 60}, {"diameter_mm": 50, "length_m": 45}, {"diameter_mm": 32, "length_m": 80}],
        usuarios_texto="moradores de todas as unidades"),
    "hospitalar": dict(
        pasta="hospitalar", id="sc-hospitalar", tipologia="hospitalar", municipios="climbra",
        titulo="Hospitais em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="hospital geral de porte médio",
        template_id="hospital", material_inferior="CONCRETO", material_superior="FIBRA",
        area_captacao_m2=4000, usuarios=300, demanda_per_capita_l_dia=250, fracao_pluvial_pct=25,
        volume_fixo_l=45000, volume_maximo_l=180000, passo_volume_l=3000, delta_ideal_pct=0.10,
        reservatorio_superior_l=15000, limiar_bombeamento_l=3750, tarifa="publica",
        bomba=dict(count=2, power_str="2 CV", power_kw=1.50, flow_rate_l_h=14400.0,
                   efficiency_pct=65.0, unit_cost=2400.0, manometric_head_m=28.0),
        custo_tubulacao=68000.0, custo_acessorios=42000.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção de cobertura, calhas e filtragem", 6, 1800.0, 0.0],
            ["Limpeza, sanitização e controle microbiológico", 6, 2400.0, 0.0],
            ["Manutenção eletromecânica e automação predial", 12, 3200.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 150, "length_m": 160}, {"diameter_mm": 100, "length_m": 220}, {"diameter_mm": 75, "length_m": 140}],
        usuarios_texto="pacientes, acompanhantes e equipe presentes por dia, em equivalentes"),
    "aeroportuario": dict(
        pasta="aeroportos", id="sc-aeroportuario", tipologia="aeroportuario", municipios="aeroportos",
        titulo="Aeródromos e Aeroportos de Santa Catarina: 21 aeródromos da ANAC classificados por porte, 19 modelos, 7 recortes",
        descricao="terminais e aeródromos públicos classificados por porte (Classes I a V)",
        template_id="comercial", material_inferior="CONCRETO", material_superior="FIBRA",
        area_captacao_m2=3500, usuarios=1300, demanda_per_capita_l_dia=25, fracao_pluvial_pct=50,
        volume_fixo_l=30000, volume_maximo_l=150000, passo_volume_l=3000, delta_ideal_pct=0.10,
        reservatorio_superior_l=8000, limiar_bombeamento_l=2000, tarifa="comercial",
        bomba=dict(count=2, power_str="3 CV", power_kw=2.20, flow_rate_l_h=21600.0,
                   efficiency_pct=68.0, unit_cost=3800.0, manometric_head_m=24.0),
        custo_tubulacao=145000.0, custo_acessorios=85000.0, tma_mensal_pct=0.75,
        custos_operacionais=[
            ["Inspeção de macrocaptação e filtros industriais", 6, 3200.0, 0.0],
            ["Limpeza e higienização das células de acumulação", 6, 4500.0, 0.0],
            ["Manutenção eletromecânica das bombas e automação", 12, 6500.0, 0.0],
        ],
        tubos_acv=[{"diameter_mm": 150, "length_m": 320}, {"diameter_mm": 100, "length_m": 280}, {"diameter_mm": 75, "length_m": 200}],
        usuarios_texto="passageiros e funcionários presentes por dia, em equivalentes"),
}

#: Candidatas a fonte para refinar os arquétipos (DOI conferido no OpenAlex em 29/10/2026); NENHUM valor deste
#: pacote foi tirado delas.
#: Segundos por simulação medidos em 29/10/2026 (39 casos espaçados por estudo; ver estudos/santa-catarina/LEIA.md).
CUSTO_S = {"escolar": 0.043, "comercial": 0.028, "residencial-unifamiliar": 0.112, "residencial-multifamiliar": 0.137,
           "hospitalar": 0.142, "aeroportos": 0.166}

REFERENCIAS = [
    ("10.3390/w4030607", "Potable Water Savings by Using Rainwater for Non-Potable Uses in Houses (Water, 2012)"),
    ("10.3390/w8040110", "Potential for Potable Water Savings in Buildings by Using Stormwater Harvested from Porous Pavements (Water, 2016): setores residencial, público e comercial de Florianópolis"),
    ("10.3390/w10040471", "Rainwater Harvesting in Buildings in Brazil: A Literature Review (Water, 2018)"),
    ("10.3390/w11112351", "Reduction of Potable Water Consumption and Sewage Generation on a City Scale: A Case Study in Brazil (Water, 2019): Joinville, setores residencial, público e comercial"),
    ("10.3390/w12020546", "Assessment of A Rainwater Harvesting System in A Multi-Storey Residential Building in Brazil (Water, 2020): Florianópolis"),
]


def norm(texto: str) -> str:
    nfkd = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn").lower().replace(" ", "").replace("-", "").replace("'", "").replace("_", "")


def slug(texto: str) -> str:
    import re
    nfkd = unicodedata.normalize("NFD", str(texto))
    limpo = "".join(c for c in nfkd if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", limpo).strip("-")


def sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


# ── municípios ──────────────────────────────────────────────────────────────────────────────────

def municipios_sc() -> dict:
    """Os 295 municípios do IBGE e quais estão na CLIMBra (nome igual e UF = SC no catálogo de tarifas)."""
    ibge = json.loads((FONTES / "ibge_municipios_sc.json").read_text(encoding="utf-8"))
    por_nome = {norm(m["nome"]): m for m in ibge}
    banco = RAIZ / "data" / "climbra_INM-CM4.db"
    con = sqlite3.connect(f"file:{banco.as_posix()}?mode=ro", uri=True)
    cidades = [c for (c,) in con.execute("SELECT city FROM climbra_cities ORDER BY city")]
    con.close()
    catalogo = json.loads((RAIZ / "triton" / "data" / "brazil_cities_tariffs.json").read_text(encoding="utf-8"))
    uf_do_catalogo = {}
    for v in catalogo["cities"].values():
        uf_do_catalogo.setdefault(norm(v["municipio"]), set()).add(v["uf"])
    na_climbra, homonimos = {}, []
    for c in cidades:
        n = norm(c)
        if n in por_nome:
            if uf_do_catalogo.get(n) == {UF}:
                na_climbra[n] = c
            else:
                homonimos.append({"climbra": c, "ibge_sc": por_nome[n]["id"], "uf_no_catalogo": sorted(uf_do_catalogo.get(n, []))})
    linhas = []
    for m in sorted(ibge, key=lambda m: m["nome"]):
        n = norm(m["nome"])
        linhas.append({"ibge": str(m["id"]), "nome_ibge": m["nome"], "nome_climbra": na_climbra.get(n, ""),
                       "na_climbra": n in na_climbra})
    return {"linhas": linhas, "homonimos_excluidos": homonimos, "total_climbra": len(cidades)}


# ── aeródromos e aeroportos de Santa Catarina (21 unidades ANAC) ─────────────────────────

DADOS_21_AEROPORTOS = [
    # Classe I - Hub Internacional / Capital
    dict(icao="SBFL", nome="Florianópolis (Hercílio Luz)", municipio="Florianópolis", ibge="4205407", clima_municipio="Florianópolis",
         classe="Classe I - Hub Internacional", area_captacao_m2=18000, usuarios=11500, volume_fixo_l=150000, volume_maximo_l=600000,
         passo_volume_l=15000, delta_ideal_pct=0.06, reservatorio_superior_l=30000, limiar_bombeamento_l=7500),
    # Classe II - Internacional Regional / Litoral Norte
    dict(icao="SBNF", nome="Navegantes (Ministro Victor Konder)", municipio="Navegantes", ibge="4211306", clima_municipio="Navegantes",
         classe="Classe II - Internacional Regional", area_captacao_m2=8500, usuarios=6300, volume_fixo_l=80000, volume_maximo_l=350000,
         passo_volume_l=10000, delta_ideal_pct=0.08, reservatorio_superior_l=15000, limiar_bombeamento_l=3750),
    # Classe III - Regional Médio com Voos Regulares
    dict(icao="SBJV", nome="Joinville (Lauro Carneiro de Loyola)", municipio="Joinville", ibge="4209102", clima_municipio="Joinville",
         classe="Classe III - Regional Médio", area_captacao_m2=3500, usuarios=1300, volume_fixo_l=30000, volume_maximo_l=150000,
         passo_volume_l=3000, delta_ideal_pct=0.10, reservatorio_superior_l=8000, limiar_bombeamento_l=2000),
    dict(icao="SBCH", nome="Chapecó (Serafin Enoss Bertaso)", municipio="Chapecó", ibge="4204202", clima_municipio="Chapecó",
         classe="Classe III - Regional Médio", area_captacao_m2=3200, usuarios=1650, volume_fixo_l=30000, volume_maximo_l=150000,
         passo_volume_l=3000, delta_ideal_pct=0.10, reservatorio_superior_l=8000, limiar_bombeamento_l=2000),
    # Classe IV - Regional Pequeno / Sazonal / Executivo
    dict(icao="SBJA", nome="Jaguaruna (Regional Sul)", municipio="Jaguaruna", ibge="4208807", clima_municipio="Tubarão",
         classe="Classe IV - Regional Pequeno", area_captacao_m2=2000, usuarios=350, volume_fixo_l=15000, volume_maximo_l=60000,
         passo_volume_l=1500, delta_ideal_pct=0.15, reservatorio_superior_l=5000, limiar_bombeamento_l=1250),
    dict(icao="SNCP", nome="Correia Pinto (Regional da Serra)", municipio="Correia Pinto", ibge="4204558", clima_municipio="Lages",
         classe="Classe IV - Regional Pequeno", area_captacao_m2=1500, usuarios=150, volume_fixo_l=10000, volume_maximo_l=50000,
         passo_volume_l=1000, delta_ideal_pct=0.15, reservatorio_superior_l=3000, limiar_bombeamento_l=750),
    dict(icao="SSIM", nome="Forquilhinha-Criciúma (Diomício Freitas)", municipio="Forquilhinha", ibge="4205456", clima_municipio="Criciúma",
         classe="Classe IV - Regional Executivo", area_captacao_m2=1800, usuarios=200, volume_fixo_l=12000, volume_maximo_l=50000,
         passo_volume_l=1000, delta_ideal_pct=0.15, reservatorio_superior_l=3000, limiar_bombeamento_l=750),
    dict(icao="SSBL", nome="Blumenau (Quero-Quero)", municipio="Blumenau", ibge="4202404", clima_municipio="Blumenau",
         classe="Classe IV - Regional Executivo", area_captacao_m2=1500, usuarios=150, volume_fixo_l=10000, volume_maximo_l=50000,
         passo_volume_l=1000, delta_ideal_pct=0.15, reservatorio_superior_l=3000, limiar_bombeamento_l=750),
    dict(icao="SBLJ", nome="Lages (Antônio Correia Pinto de Macedo)", municipio="Lages", ibge="4209300", clima_municipio="Lages",
         classe="Classe IV - Regional Executivo", area_captacao_m2=1500, usuarios=150, volume_fixo_l=10000, volume_maximo_l=50000,
         passo_volume_l=1000, delta_ideal_pct=0.15, reservatorio_superior_l=3000, limiar_bombeamento_l=750),
    # Classe V - Aeródromos Locais e Aviação Geral
    dict(icao="SBCD", nome="Caçador (Dr. Carlos Alberto da Costa Neves)", municipio="Caçador", ibge="4203006", clima_municipio="Caçador",
         classe="Classe V - Aviação Geral", area_captacao_m2=1000, usuarios=80, volume_fixo_l=6000, volume_maximo_l=30000,
         passo_volume_l=1000, delta_ideal_pct=0.20, reservatorio_superior_l=2000, limiar_bombeamento_l=500),
    dict(icao="SSCK", nome="Concórdia (Olavo Cecco Rigon)", municipio="Concórdia", ibge="4204301", clima_municipio="Concórdia",
         classe="Classe V - Aviação Geral", area_captacao_m2=1000, usuarios=80, volume_fixo_l=6000, volume_maximo_l=30000,
         passo_volume_l=1000, delta_ideal_pct=0.20, reservatorio_superior_l=2000, limiar_bombeamento_l=500),
    dict(icao="SSVI", nome="Videira (Ângelo Ponzoni)", municipio="Videira", ibge="4219309", clima_municipio="Videira",
         classe="Classe V - Aviação Geral", area_captacao_m2=1000, usuarios=80, volume_fixo_l=6000, volume_maximo_l=30000,
         passo_volume_l=1000, delta_ideal_pct=0.20, reservatorio_superior_l=2000, limiar_bombeamento_l=500),
    dict(icao="SSXX", nome="Xanxerê (Municipal João Winckler)", municipio="Xanxerê", ibge="4219507", clima_municipio="Xanxerê",
         classe="Classe V - Aviação Geral", area_captacao_m2=1000, usuarios=80, volume_fixo_l=6000, volume_maximo_l=30000,
         passo_volume_l=1000, delta_ideal_pct=0.20, reservatorio_superior_l=2000, limiar_bombeamento_l=500),
    dict(icao="SSSS", nome="São Francisco do Sul", municipio="São Francisco do Sul", ibge="4216206", clima_municipio="São Francisco do Sul",
         classe="Classe V - Aviação Geral", area_captacao_m2=800, usuarios=60, volume_fixo_l=5000, volume_maximo_l=25000,
         passo_volume_l=1000, delta_ideal_pct=0.25, reservatorio_superior_l=1500, limiar_bombeamento_l=375),
    dict(icao="SSJA", nome="Joaçaba (Santa Terezinha)", municipio="Joaçaba", ibge="4209003", clima_municipio="Videira",
         classe="Classe V - Aviação Geral", area_captacao_m2=1000, usuarios=80, volume_fixo_l=6000, volume_maximo_l=30000,
         passo_volume_l=1000, delta_ideal_pct=0.20, reservatorio_superior_l=2000, limiar_bombeamento_l=500),
    dict(icao="SSKU", nome="Curitibanos (Lauro Antônio da Costa)", municipio="Curitibanos", ibge="4204806", clima_municipio="Lages",
         classe="Classe V - Aviação Geral", area_captacao_m2=800, usuarios=60, volume_fixo_l=5000, volume_maximo_l=25000,
         passo_volume_l=1000, delta_ideal_pct=0.25, reservatorio_superior_l=1500, limiar_bombeamento_l=375),
    dict(icao="SSTB", nome="Três Barras", municipio="Três Barras", ibge="4218301", clima_municipio="Canoinhas",
         classe="Classe V - Aviação Geral", area_captacao_m2=800, usuarios=60, volume_fixo_l=5000, volume_maximo_l=25000,
         passo_volume_l=1000, delta_ideal_pct=0.25, reservatorio_superior_l=1500, limiar_bombeamento_l=375),
    dict(icao="SSLN", nome="Lontras (Helmuth Baungartem)", municipio="Lontras", ibge="4209904", clima_municipio="Rio do Sul",
         classe="Classe V - Aviação Geral", area_captacao_m2=800, usuarios=60, volume_fixo_l=5000, volume_maximo_l=25000,
         passo_volume_l=1000, delta_ideal_pct=0.25, reservatorio_superior_l=1500, limiar_bombeamento_l=375),
    dict(icao="SSOE", nome="Descanso (Hélio Wasum)", municipio="Descanso", ibge="4204905", clima_municipio="Chapecó",
         classe="Classe V - Aviação Geral", area_captacao_m2=600, usuarios=40, volume_fixo_l=4000, volume_maximo_l=20000,
         passo_volume_l=1000, delta_ideal_pct=0.30, reservatorio_superior_l=1000, limiar_bombeamento_l=250),
    dict(icao="SND4", nome="São Joaquim (Ismael Nunes)", municipio="São Joaquim", ibge="4216503", clima_municipio="Lages",
         classe="Classe V - Aviação Geral", area_captacao_m2=600, usuarios=40, volume_fixo_l=4000, volume_maximo_l=20000,
         passo_volume_l=1000, delta_ideal_pct=0.30, reservatorio_superior_l=1000, limiar_bombeamento_l=250),
    dict(icao="SND6", nome="Dionísio Cerqueira", municipio="Dionísio Cerqueira", ibge="4205001", clima_municipio="Chapecó",
         classe="Classe V - Aviação Geral", area_captacao_m2=600, usuarios=40, volume_fixo_l=4000, volume_maximo_l=20000,
         passo_volume_l=1000, delta_ideal_pct=0.30, reservatorio_superior_l=1000, limiar_bombeamento_l=250),
]


def aeroportos(mun: dict) -> dict:
    """Aeródromos públicos de SC (ANAC) e o critério de «aeroporto com voos regulares»."""
    bruto = (FONTES / "AerodromosPublicos.csv").read_bytes().decode("cp1252")
    linhas = list(csv.reader(bruto.splitlines()[1:], delimiter=";"))
    cab = linhas[0]
    ix = {c: i for i, c in enumerate(cab)}
    mov = {}
    with open(FONTES / "vra_2025_movimentos_aeroportos_sc.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            mov[r["icao"]] = (int(r["total"]), int(r["meses_com_voo"]))
    por_nome = {norm(m["nome_ibge"]): m for m in mun["linhas"]}
    saida = []
    for r in linhas[1:]:
        if len(r) < len(cab) or r[ix["UF"]] != "Santa Catarina":
            continue
        icao = r[ix["Código OACI"]]
        total, meses = mov.get(icao, (0, 0))
        m = por_nome.get(norm(r[ix["Município"]]))
        regular = meses == 12
        item = {"icao": icao, "ciad": r[ix["CIAD"]], "nome": r[ix["Nome"]], "municipio_anac": r[ix["Município"]].title(),
                "ibge": m["ibge"] if m else "", "movimentos_regulares_2025": total, "meses_com_voo_regular_2025": meses,
                "regular": regular, "municipio_na_climbra": bool(m and m["na_climbra"]),
                "nome_climbra": m["nome_climbra"] if m else ""}
        if not regular:
            item["motivo"] = ("voos regulares realizados em %d de 12 meses de 2025" % meses) if meses else "sem voo regular realizado em 2025"
        elif not item["municipio_na_climbra"]:
            item["motivo"] = "município sem série na CLIMBra: fora do estudo até o autor decidir como representar o clima"
        saida.append(item)
    return {"aeroportos": sorted(saida, key=lambda a: a["icao"]),
            "criterio": ("«com voos regulares»: ao menos um voo regular (VRA da ANAC) realizado em cada um dos 12 meses de 2025, "
                         "como origem ou destino; sazonais e sem voo regular ficam de fora")}


# ── estudos ─────────────────────────────────────────────────────────────────────────────────────

def projeto_triton(a: dict) -> dict:
    """Projeto completo ``.triton`` (esquema ``triton-project``, versão 2) do arquétipo, com custos de engenharia."""
    from triton import __version__
    from triton.core.chlorination import DOSE_PADRAO_MG_POR_LITRO, FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO, PUREZA_PADRAO
    from triton.core.cost_estimates import (
        LOWER_TANK_PRICE_TABLE,
        UPPER_TANK_PRICE_TABLE,
        estimate_tank_price,
        mao_de_obra_estimada,
    )
    from triton.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO, LAMINA_DE_DESCARTE_PADRAO_MM
    from triton.core.parser import TritonConfig, impressao_da_serie, serie_da_climbra
    from triton.core import tariffs_database as tdb
    from triton.core.vigencia_tarifaria import data_da_vigencia

    cidade_ref = "Florianópolis"
    modelo_ref = "INM-CM4"
    cenario_ref = "HIST"
    ini_ref, fim_ref = "01/01/1981", "31/12/2010"

    cfg_ref = TritonConfig(
        climate_source_mode="national_db",
        climate_city_uf=UF,
        climate_city_name=cidade_ref,
        climate_model=modelo_ref,
        climate_scenario=cenario_ref,
        climate_start_date=ini_ref,
        climate_end_date=fim_ref,
        start_date=ini_ref,
    )
    serie = serie_da_climbra(cfg_ref)
    imp = impressao_da_serie(serie)
    ref_climbra = {
        "origem": "CLIMBra",
        "cidade": cidade_ref,
        "uf": UF,
        "modelo": modelo_ref,
        "cenario": cenario_ref,
        "inicio": ini_ref,
        "fim": fim_ref,
        **imp,
    }

    cat = a["tarifa"]
    dados_tar = tdb.get_city_tariffs_by_category(UF, cidade_ref, cat) or tdb.get_city_tariffs_by_category(UF, cidade_ref, "residencial")
    faixas = [list(f) for f in dados_tar["faixas"]]
    sewage_mode, sewage_rate = tdb.esgoto_do_municipio(dados_tar)
    vig = data_da_vigencia(dados_tar.get("vigencia_saneamento", ""))
    vig_str = vig.strftime("%d/%m/%Y") if vig else "01/04/2026"
    elec_tariff = float(dados_tar.get("energia_r_kwh", 0.85) or 0.85)

    fracao = round(a["fracao_pluvial_pct"] / 100.0, 4)
    fracao_potavel = round(1.0 - fracao, 4)
    economias = int(a.get("economias", 1))
    v_fixo = float(a["volume_fixo_l"])
    v_sup = float(a["reservatorio_superior_l"])
    mat_inf = a["material_inferior"]
    mat_sup = a["material_superior"]
    bomba = a["bomba"]

    custo_inf = round(estimate_tank_price(v_fixo, mat_inf, LOWER_TANK_PRICE_TABLE), 2)
    custo_sup = round(estimate_tank_price(v_sup, mat_sup, UPPER_TANK_PRICE_TABLE), 2)
    custo_bombas = round(float(bomba["count"]) * float(bomba["unit_cost"]), 2)
    custo_tub = round(float(a["custo_tubulacao"]), 2)
    custo_acc = round(float(a["custo_acessorios"]), 2)
    custo_mao = round(mao_de_obra_estimada(custo_inf + custo_sup + custo_bombas + custo_tub + custo_acc), 2)
    pump_cv = round(float(bomba["power_kw"]) / 0.7355, 2)

    return {
        "schema": {"name": "triton-project", "version": 2},
        "version": __version__,
        "metadata": {
            "project_id": f"TRITON-SC-{a['pasta'].upper()}",
            "name": f"Arquétipo {a['tipologia']} ({a['descricao']}) — Santa Catarina",
            "created_at": "29/10/2026 00:00",
            "saved_at": "29/10/2026 00:00:00",
        },
        "rainfall": {
            "source_mode": "national_db",
            "climate_city_uf": UF,
            "climate_city_name": cidade_ref,
            "climate_model": modelo_ref,
            "climate_scenario": cenario_ref,
            "climate_start_date": ini_ref,
            "climate_end_date": fim_ref,
            "file_name": "",
            "start_date": ini_ref,
            "total_days": imp["dias"],
            "climbra_series": ref_climbra,
            "precipitation_mm": [],
        },
        "inputs": {
            "building_and_demand": {
                "catchment_area_m2": float(a["area_captacao_m2"]),
                "runoff_coeff": COEFICIENTE_DE_ESCOAMENTO_PADRAO,
                "residents_count": int(a["usuarios"]),
                "residents_type": 0,
                "residents_monthly": [],
                "demand_value": float(a["demanda_per_capita_l_dia"]),
                "demand_type": 0,
                "demand_monthly": [],
                "use_variable": False,
                "rainwater_share": fracao,
            },
            "demand_modulation": {
                "demand_mode": "constant",
                "weekly_demands": [],
                "weekly_residents": [],
                "weekly_shares": [],
                "monthly_shares": [],
                "daily_demands": [],
                "daily_residents": [],
                "daily_shares": [],
            },
            "rainfall_discard": {
                "discard_mm": LAMINA_DE_DESCARTE_PADRAO_MM,
                "discard_mode": 1,
                "discard_days_interval": 7,
            },
            "reservoirs_and_pumping": {
                "lower_tank_fixed_l": v_fixo,
                "lower_tank_max_l": float(a["volume_maximo_l"]),
                "lower_tank_step_l": float(a["passo_volume_l"]),
                "lower_tank_mode": 1,
                "delta_ideal_pct": float(a["delta_ideal_pct"]),
                "phi_operation_rule": None,
                "upper_tank_vol_l": v_sup,
                "upper_tank_used": True,
                "pumping_threshold_l": float(a["limiar_bombeamento_l"]),
                "supply_arrangement": "recalque",
                "pressurizer_pressure_m": 18.0,
                "pressurizer_starts_per_person_day": 5.05,
                "pressurizer_model": "komeco_tp820t",
                "pressurizer_point_flow_l_min": 9.0,
                "pressurizer_power_kw": 0.18,
                "pressurizer_flow_l_min": 13.3,
                "pressurizer_post_run_s": 0.0,
                "pump": {
                    "count": int(bomba["count"]),
                    "power_str": str(bomba["power_str"]),
                    "power_kw": float(bomba["power_kw"]),
                    "flow_rate_l_h": float(bomba["flow_rate_l_h"]),
                    "efficiency_pct": float(bomba["efficiency_pct"]),
                    "startup_time_h": 0.03,
                    "motor_efficiency": 0.0,
                    "unit_cost": float(bomba["unit_cost"]),
                    "manometric_head_m": float(bomba["manometric_head_m"]),
                },
            },
            "financial_and_economic": {
                "analysis_period_years": 20,
                "tma_monthly_pct": float(a["tma_mensal_pct"]),
                "inflation_monthly_pct": 0.2,
                "sewage_mode": int(sewage_mode),
                "sewage_rate_pct": float(sewage_rate),
                "sewage_tariffs": [],
                "sewage_volume_factor": 1.0,
                "water_tax_fixed": 0.0,
                "water_tax_var_pct": 0.0,
                "water_tariffs": faixas,
                "tariff_city_uf": UF,
                "tariff_city_name": cidade_ref,
                "tariff_vigencia": vig_str,
                "data_base_estudo": "29/10/2026",
                "tariff_category": cat,
                "elec_city_uf": UF,
                "elec_city_name": cidade_ref,
                "tariff_escalation_months": 12.0,
                "water_tariff_escalation_pct": 5.0,
                "sewage_tariff_escalation_pct": 5.0,
                "elec_tariff": elec_tariff,
                "elec_tax_fixed": 0.0,
                "elec_tax_var_pct": 0.0,
                "elec_tariff_escalation_pct": 5.0,
            },
            "water_quality_and_etap": {
                "target_class": "classe_1",
                "disinfection": "cloro",
                "polishing_filter": False,
                "first_flush_system_enabled": True,
                "etap_enabled": True,
                "precos_de_catalogo": True,
                "chlorine_treatment_enabled": True,
                "chlorine_dose_mg_l": DOSE_PADRAO_MG_POR_LITRO,
                "chlorine_product_purity": PUREZA_PADRAO,
                "chlorine_cost_per_kg": 25.0,
                "chlorine_co2_kg_per_kg": FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
            },
            "materials_and_typology": {
                "building_template_id": a["template_id"],
                "lower_tank_material": mat_inf,
                "upper_tank_material": mat_sup,
            },
            "irrigation": {
                "garden_area_m2": 0.0,
                "rate_l_m2_day": 3.0,
                "liters_per_day": 0.0,
                "rain_threshold_mm": 2.0,
                "potable_backup": True,
            },
            "incentives_and_shares": {
                "iptu_green_enabled": False,
                "iptu_annual_value": 4000.0,
                "iptu_discount_pct": 5.0,
                "tariff_flag": "verde",
                "tariff_customized": False,
                "num_economias": economias,
                "potable_indoor_share": fracao_potavel,
                "non_potable_indoor_share": fracao,
                "install_month": 0,
                "econ_lower_tank_vol": v_fixo,
                "demand_mode": "constant",
                "edge_base_case_l_person_day": 0.0,
            },
            "capex_and_opex": {
                "cost_lower_tank": custo_inf,
                "cost_upper_tank": custo_sup,
                "cost_labor": custo_mao,
                "cost_piping": custo_tub,
                "cost_accessories": custo_acc,
                "capex_do_arranjo": False,
                "mao_de_obra_automatica": True,
                "operational_costs": a["custos_operacionais"],
            },
            "global_optimizer_scenarios": [],
        },
        "ui_state": {
            "stage3": {"currency_code": "BRL"},
            "project": {
                "source_mode": "national_db",
                "climate_uf": UF,
                "climate_city": cidade_ref,
                "climate_model": modelo_ref,
                "climate_scenario": cenario_ref,
                "start_date": ini_ref,
                "end_date": fim_ref,
            },
        },
        "analysis": {
            "origem": ROTULO_ARQUETIPO + "; ver LEIA.md",
            "arquetipo": a["descricao"],
            "topsis_weights": [0.33, 0.33, 0.34],
            "environmental": {
                "lower_material_key": mat_inf,
                "upper_material_key": mat_sup,
                "grid_co2_factor_kg_kwh": 0.085,
                "potable_water_co2_kg_m3": 0.35,
                "chlorine_dose_mg_l": DOSE_PADRAO_MG_POR_LITRO,
                "chlorine_co2_kg_per_kg": FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
                "system_lifespan_years": 20,
                "pipes": a["tubos_acv"],
                "pump": {"power_cv": pump_cv, "specific_kwh_per_m3": 0.45},
            },
        },
        "bim_layout": {
            "bim_components": [],
            "pipe_runs": [],
            "building_volume": {},
        },
    }


def estudo_json(a: dict, lista: list) -> dict:
    arq_triton = f"{a['pasta']}.triton"
    subs = {"_origem": f"{ROTULO_ARQUETIPO}; todos os parâmetros e custos de engenharia também estão em {arq_triton} (ver LEIA.md)",
            "area_captacao_m2": a["area_captacao_m2"], "usuarios": a["usuarios"],
            "demanda_per_capita_l_dia": a["demanda_per_capita_l_dia"], "fracao_pluvial_pct": a["fracao_pluvial_pct"],
            "volume_maximo_l": a["volume_maximo_l"], "passo_volume_l": a["passo_volume_l"],
            "delta_ideal_pct": a["delta_ideal_pct"],
            "reservatorio_superior_l": a["reservatorio_superior_l"],
            "limiar_bombeamento_l": a["limiar_bombeamento_l"],
            "tma_pct_mes": a["tma_mensal_pct"]}
    if "economias" in a:
        subs["economias"] = a["economias"]
    return {
        "esquema": {"nome": "triton-estudo", "versao": 1},
        "estudo": {"id": a["id"], "titulo": a["titulo"], "tipologia": a["tipologia"], "autores": [],
                   "nota": (f"Projeto-base completo em {arq_triton} (valores de edificação e custos calibrados = estimativas de arquétipo, "
                            "a refinar pelo autor; ver LEIA.md). Clima: CLIMBra, 19 modelos × 7 recortes sugeridos pelo programa. "
                            "Tarifas: catálogo municipal do programa.")},
        "projeto_base": {"arquivo": arq_triton},
        "padroes": {"substituicoes": subs,
                    "tarifa": {"categoria": a["tarifa"], "se_ausente": "residencial",
                               "_origem": "categoria do catálogo de tarifas do programa; sem tabela coletada, usa a residencial e registra alerta"}},
        "expansao": {"uf": UF, "modelos": "todos", "recortes": RECORTES, "municipios": lista},
        "analise": {"tipo": "all", "volume": "smaa_vikor", "semente": 42},
        "saidas": {"formatos": ["csv", "json", "md", "tex"], "metricas": METRICAS,
                   "casas_decimais": {
                       "padrao": 1,
                       "volume_l": 0,
                       "volume_otimo_tecnico_l": 0,
                       "volume_otimo_economico_l": 0,
                       "volume_otimo_ambiental_l": 0,
                       "volume_topsis_l": 0,
                       "volume_smaa_vikor_l": 0,
                       "indice_topsis": 3,
                       "capex": 0,
                       "vpl": 0,
                       "payback_descontado_meses": 0,
                       "co2_incorporado_kg": 0,
                       "co2_liquido_vida_kg": 0,
                   },
                   "idioma": "pt-BR", "gravar_analise": False},
    }


def modelo_texto(a: dict) -> str:
    if a["tipologia"] == "aeroportuario":
        desc = "21 aeródromos e aeroportos públicos de Santa Catarina (classificados da Classe I à Classe V)"
    else:
        desc = f"arquétipo «{a['descricao']}»"
    return (f"# Modelo de texto: {a['titulo']}\n\n"
            f"Nos {{{{n_casos}}}} casos (município × modelo climático × recorte), a seleção multicritério estocástica do {desc} "
            "comparou os volumes ótimos por dimensão — técnico (mediana de {{volume_otimo_tecnico_l:@mediana}} L, faixa de {{volume_otimo_tecnico_l:@min}} L a {{volume_otimo_tecnico_l:@max}} L), "
            "econômico (mediana de {{volume_otimo_economico_l:@mediana}} L, faixa de {{volume_otimo_economico_l:@min}} L a {{volume_otimo_economico_l:@max}} L), "
            "ambiental/ACV (mediana de {{volume_otimo_ambiental_l:@mediana}} L, faixa de {{volume_otimo_ambiental_l:@min}} L a {{volume_otimo_ambiental_l:@max}} L) "
            "e TOPSIS (mediana de {{volume_topsis_l:@mediana}} L, índice médio {{indice_topsis:@media}}) — e adotou como volume de referência o "
            "ótimo SMAA-VIKOR (mediana de {{volume_smaa_vikor_l:@mediana}} L, faixa de {{volume_smaa_vikor_l:@min}} L a {{volume_smaa_vikor_l:@max}} L, "
            "aceitabilidade de 1.º posto $b^1$ média de {{aceitabilidade_smaa_pct:@media}}%). "
            "No volume SMAA-VIKOR, a economia de água potável ficou entre {{economia_agua_potavel_pct:@min}}% e {{economia_agua_potavel_pct:@max}}% "
            "(média de {{economia_agua_potavel_pct:@media}}%), com aproveitamento pluvial médio de {{agua_pluvial_m3_ano:@media}} m³/ano. "
            "Na análise econômica (horizonte de 20 anos, custos calibrados no projeto `.triton` e tarifas municipais do catálogo), "
            "o investimento inicial (CAPEX) médio foi de R$ {{capex:@media}} (R$ {{capex:@min}} a R$ {{capex:@max}}), "
            "o valor presente líquido (VPL) médio foi de R$ {{vpl:@media}} (mediana de R$ {{vpl:@mediana}}, faixa de R$ {{vpl:@min}} a R$ {{vpl:@max}}) "
            "e o payback descontado nos casos viáveis teve mediana de {{payback_descontado_meses:@mediana}} meses "
            "({{payback_descontado_meses:@min}} a {{payback_descontado_meses:@max}} meses). "
            "Na avaliação ambiental de ciclo de vida (ACV, 20 anos), o carbono incorporado médio foi de {{co2_incorporado_kg:@media}} kg CO₂e, "
            "a redução líquida de emissões ao longo da vida útil teve média de {{co2_liquido_vida_kg:@media}} kg CO₂e "
            "(mediana de {{co2_liquido_vida_kg:@mediana}} kg CO₂e, {{co2_evitado_ano_kg:@media}} kg CO₂e/ano evitados) "
            "e o payback ambiental nos casos viáveis teve mediana de {{payback_ambiental_anos:@mediana}} anos "
            "({{payback_ambiental_anos:@min}} a {{payback_ambiental_anos:@max}} anos). "
            "Valores de edificação e custos são estimativas de arquétipo, a refinar pelo autor.\n")


def leia(a: dict, lista: list, mun: dict, aer: dict, proj: dict) -> str:
    n = len(lista)
    ncasos = n * 19 * len(RECORTES)
    arq_triton = f"{a['pasta']}.triton"
    co = proj["inputs"]["capex_and_opex"]
    bomba = proj["inputs"]["reservoirs_and_pumping"]["pump"]
    custo_bombas = round(float(bomba["count"]) * float(bomba["unit_cost"]), 2)
    capex_ref = round(
        co["cost_lower_tank"] + co["cost_upper_tank"] + custo_bombas + co["cost_piping"] + co["cost_accessories"] + co["cost_labor"], 2
    )
    opex_fixo_ref = round(sum((12.0 / float(m)) * float(fc) for _, m, fc, _ in co["operational_costs"]), 2)
    linhas = [f"# {a['titulo']}", "",
              f"Estudo `{a['id']}` (esquema `triton-estudo`, versão 1) e projeto-base completo `{arq_triton}` "
              f"(esquema `triton-project`, versão 2), gerados por `scripts/gerar_estudos_sc.py`. "
              f"Arquétipo: **{a['descricao']}**. Não edite o `estudo.json` nem o `{arq_triton}` à mão sem registrar: o gerador os reescreve.", "",
              "## Escopo", ""]
    if a["municipios"] == "climbra":
        linhas += [f"- Municípios: os **{n}** de Santa Catarina presentes na base CLIMBra (de 295 do IBGE; 263 não têm série). "
                   "A lista, com o código IBGE e os ausentes, está em `../_fontes/municipios_sc_climbra.json`."]
    else:
        linhas += [f"- Aeródromos e Aeroportos: os **{n}** aeródromos públicos de Santa Catarina cadastrados na ANAC, "
                   "classificados da Classe I à Classe V com áreas e demandas individualizadas:", ""]
        for x in DADOS_21_AEROPORTOS:
            linhas.append(f"  - **{x['icao']}** {x['nome']} ({x['classe']}): telhado de {x['area_captacao_m2']} m², "
                           f"{x['usuarios']} pessoas/dia eq., varredura de {x['volume_maximo_l']} L (clima: {x['clima_municipio']}).")
        linhas.append("  - Fonte dos aeródromos: ANAC, Lista de Aeródromos Públicos e VRA 2025.")
    linhas += [f"- Projeto-base completo: `{arq_triton}` (pode ser aberto diretamente na interface gráfica ou via `triton.cli analyze`), "
               "contendo todos os blocos de entrada (`building_and_demand`, `demand_modulation`, `rainfall_discard`, "
               "`reservoirs_and_pumping`, `financial_and_economic`, `water_quality_and_etap`, `materials_and_typology`, "
               "`irrigation`, `incentives_and_shares`, `capex_and_opex`, `analysis` e `bim_layout`).",
               f"- Clima: CLIMBra (Ballarin et al., 2023, doi:10.1038/s41597-023-01956-z; CC0), **19 modelos** × **{len(RECORTES)} recortes** "
               f"(`expansao.recortes`): histórico 1981–2010 e, para SSP2-4.5 e SSP5-8.5, futuro próximo 2021–2050, meados 2041–2070 e fim 2071–2100, "
               "os atalhos de `RECORTES_SUGERIDOS`. A série é a da célula de 0,25° do município; o histórico é simulado, não observado.",
               f"- Casos: {n} × 19 × {len(RECORTES)} = **{ncasos}** simulações (cada uma varre os volumes do reservatório).",
               f"- Análise: `all` (técnica, econômica, ambiental/ACV, TOPSIS e SMAA-VIKOR), volume no ótimo SMAA-VIKOR (`smaa_vikor`), semente 42, "
               "reportando lado a lado os ótimos técnico, econômico, ambiental, TOPSIS e SMAA-VIKOR. Custos de engenharia e parâmetros de ACV calibrados em `{arq_triton}` "
               "(com interpolação da cisterna inferior pelo catálogo para cada volume da varredura e mão de obra proporcional aos materiais), "
               "tarifas: catálogo municipal do programa.", "",
               f"## Arquétipo e Custos em `{arq_triton}` (todos os valores: estimativa de arquétipo, a refinar pelo autor)", "",
               "| Parâmetro | Valor | Origem |", "| --- | ---: | --- |"]
    rot = [("area_captacao_m2", "Área de captação (m²)"), ("usuarios", f"Usuários ({a['usuarios_texto']})"),
           ("economias", "Economias (unidades)"), ("demanda_per_capita_l_dia", "Demanda por usuário (L/dia)"),
           ("fracao_pluvial_pct", "Fração atendível por chuva (%)"), ("volume_fixo_l", "Volume inferior de referência (L)"),
           ("volume_maximo_l", "Maior volume da varredura (L)"), ("passo_volume_l", "Passo da varredura (L)"),
           ("delta_ideal_pct", "Limiar de ganho marginal do ótimo técnico (%/m³)"),
           ("reservatorio_superior_l", "Reservatório superior (L)"), ("limiar_bombeamento_l", "Limiar de bombeamento (L)"),
           ("material_inferior", "Material da cisterna inferior"), ("material_superior", "Material do reservatório superior"),
           ("tma_mensal_pct", "TMA mensal (% a.m.)")]
    for k, r in rot:
        if k in a:
            linhas.append(f"| {r} | {a[k]} | {ROTULO_ARQUETIPO} |")
    linhas += [f"| Recalque (`pump`) | {bomba['count']} × {bomba['power_str']} ({bomba['power_kw']} kW, R$ {bomba['unit_cost']:.2f}/un) | {ROTULO_ARQUETIPO} |",
               f"| Cisterna inferior de referência ({a['volume_fixo_l']} L, {a['material_inferior']}) | R$ {co['cost_lower_tank']:.2f} | catálogo do programa (na varredura, interpola cada volume) |",
               f"| Reservatório superior ({a['reservatorio_superior_l']} L, {a['material_superior']}) | R$ {co['cost_upper_tank']:.2f} | catálogo do programa |",
               f"| Tubulações prediais e coletores (`cost_piping`) | R$ {co['cost_piping']:.2f} | {ROTULO_ARQUETIPO} |",
               f"| Acessórios, filtragem, quadro e automação (`cost_accessories`) | R$ {co['cost_accessories']:.2f} | {ROTULO_ARQUETIPO} |",
               f"| Mão de obra de referência (`cost_labor`, 30% dos materiais) | R$ {co['cost_labor']:.2f} | automática por volume da varredura (`mao_de_obra_automatica: true`) |",
               f"| CAPEX total no volume de referência ({a['volume_fixo_l']} L) | R$ {capex_ref:.2f} | soma dos subsistemas em `{arq_triton}` |",
               f"| Manutenção periódica fixa (`operational_costs`) | R$ {opex_fixo_ref:.2f}/ano | {ROTULO_ARQUETIPO} |",
               f"| Categoria tarifária | {a['tarifa']} | escolha de arquétipo; sem tabela coletada para o município, usa a residencial (alerta no resultado) |",
               "| Coeficiente de escoamento, descarte, demais campos | os do modelo da edição | padrão do programa |", "",
               f"Nenhum desses valores é medido nem tirado de norma. Para refinar, edite `{arq_triton}` e `padroes.substituicoes` (ou os do script) e cite a fonte de cada um; "
               "candidatas de leitura (DOI conferido; nenhum valor foi tirado delas):", ""]
    linhas += [f"- doi:{d} — {t}" for d, t in REFERENCIAS]
    linhas += ["", "## Comandos", "", "Na pasta `triton_brl` (edição Brasil):", "", "```powershell",
               f"python -m triton.cli estudo validate estudos\\santa-catarina\\{a['pasta']}\\estudo.json",
               f"python -m triton.cli estudo run estudos\\santa-catarina\\{a['pasta']}\\estudo.json --saida estudos\\santa-catarina\\_saida\\{a['pasta']} --paralelo 4 --retomar",
               f"python -m triton.cli estudo texto estudos\\santa-catarina\\_saida\\{a['pasta']} --modelo estudos\\santa-catarina\\{a['pasta']}\\modelo_texto.md",
               "```", "",
               "`resultados.csv` é tidy: uma linha por município × modelo × recorte × métrica (colunas `municipio`, `ibge`, `modelo`, `recorte`, "
               "`cenario`, `inicio`, `fim`). A pasta `_saida/` não vai para o Git. Veja `../LEIA.md` para o custo da varredura completa.", ""]
    return "\n".join(linhas)


def leia_geral(estudos: dict, mun: dict, aer: dict) -> str:
    n = sum(1 for m in mun["linhas"] if m["na_climbra"])
    ausentes = [m["nome_ibge"] for m in mun["linhas"] if not m["na_climbra"]]
    return "\n".join([
        "# Estudos de caso de Santa Catarina (JSON `triton-estudo`)", "",
        "Seis estudos, um por tipologia, com a mesma estrutura: arquétipo de edificação em `padroes`, tarifas do catálogo do programa e "
        "`expansao` município × modelo × recorte da CLIMBra. Gerados por `scripts/gerar_estudos_sc.py` a partir de `_fontes/`.", "",
        "| Estudo | Pasta | Municípios | Casos (× 19 modelos × %d recortes) |" % len(RECORTES), "| --- | --- | ---: | ---: |",
        *[f"| {a['tipologia']} | `{a['pasta']}` | {len(l)} | {len(l) * 19 * len(RECORTES)} |" for a, l in estudos.values()], "",
        f"Total: {sum(len(l) for _, l in estudos.values()) * 19 * len(RECORTES)} simulações.", "",
        f"## Municípios: {n} de 295 estão na CLIMBra", "",
        f"A CLIMBra do programa tem {mun['total_climbra']} cidades brasileiras; {n} são de Santa Catarina (nome conferido com o IBGE, código 42xxxxx, "
        "e UF = SC no catálogo de tarifas). Os nomes repetidos em outras UFs foram excluídos: "
        + ", ".join(f"{h['climbra']} ({'/'.join(h['uf_no_catalogo'])})" for h in mun["homonimos_excluidos"]) + ". "
        f"Os outros {len(ausentes)} municípios de SC não têm série na CLIMBra do programa (lista em `_fontes/municipios_sc_climbra.json`).", "",
        "## Fontes (URL, data de acesso e SHA-256 em `_fontes/FONTES.json`)", "",
        "- IBGE, API de localidades (municípios de SC).", "- ANAC, dados abertos: Lista de Aeródromos Públicos e Voo Regular Ativo (VRA) 2025.",
        "- CLIMBra (doi:10.1038/s41597-023-01956-z), tarifas e custos: os do programa.", "",
        "## Decisão de clima", "",
        "Modelos: os 19 da CLIMBra. Recortes: os sugeridos pelo programa (`RECORTES_SUGERIDOS`): histórico 1981–2010 (trinta anos, como os futuros) e "
        "futuros 2021–2050, 2041–2070 e 2071–2100 em SSP2-4.5 e SSP5-8.5. A CLIMBra não traz série observada por município (o histórico é simulado). "
        "Alternativa: trocar `expansao.modelos` por um modelo (o padrão do programa é INM-CM4) e/ou `recortes` pelos recortes de série completa.", "",
        "## Custo da varredura completa (medido em 29/10/2026, 1 processo, com outra suíte rodando na máquina)", "",
        "| Estudo | Simulações | s por simulação | Tempo estimado (1 processo) | Disco estimado |", "| --- | ---: | ---: | ---: | ---: |",
        *[f"| {a['pasta']} | {len(l) * 19 * len(RECORTES)} | {CUSTO_S[a['pasta']]} | {round(len(l) * 19 * len(RECORTES) * CUSTO_S[a['pasta']] / 60 + 0.5)} min | "
          f"{round(len(l) * 19 * len(RECORTES) * 14 / 1024)} MB |" for a, l in estudos.values()], "",
        "Total: 21812 simulações, cerca de 35 a 40 min com 1 processo (`--paralelo 4` deve cortar para um quarto a um terço; não medido) e cerca de 0,3 GB "
        "(com `gravar_analise: false`; cada caso grava só o `resultado.json`). O tempo vem de 39 casos espaçados de cada estudo, "
        "com o primeiro descartado (aquecimento); inclui a montagem do caso, não a gravação.", "",
        "Para rodar tudo (um estudo por vez, retomável), na pasta `triton_brl`:", "", "```powershell",
        "foreach ($e in 'escolar','comercial','residencial-unifamiliar','residencial-multifamiliar','hospitalar','aeroportos') {",
        "  python -m triton.cli estudo run estudos/santa-catarina/$e/estudo.json --saida estudos/santa-catarina/_saida/$e --paralelo 4 --retomar",
        "}", "```", "",
        '## Figuras para artigo e painel', "",
        '`python scripts/gerar_graficos_artigos.py` (use `--help`) lê só os `resultados.csv` de `_saida/` e gera, de forma determinística, em `_saida/figuras_artigos/<pt-BR|en-GB>/<dupla|simples>/`: `fig_resumo.*` (seis tipologias: volume ótimo, viabilidade, indicador ambiental) e `fig_<tipologia>.*` (volumes por critério e série por recorte climático de economia de água, VPL e saldo de CO₂e), em PNG 300 dpi, SVG e PDF; `legenda_*.md` (legenda sugerida, números calculados dos resultados) em cada pasta de idioma; e `_saida/dashboard_artigos.html` (modelo em `painel_artigos_modelo.html`; sem rede; claro/escuro; pt-BR/en-GB). Paleta e marcador fixos por tipologia (validados pelo skill `dataviz`). `_saida/` é ignorada pelo Git (`.gitignore`); as figuras antigas em `_saida/figuras_comparativas/` e `_saida/<estudo>/figuras/` ficam substituídas por estas e podem ser apagadas. No Aeroportuário a mediana do volume SMAA-VIKOR é 0 (sem reservatório em mais da metade dos casos): é resultado, não erro.', ""])


def principal() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--conferir", action="store_true", help="Não escreve: confere que o disco já é o que o script geraria")
    args = ap.parse_args()
    sys.path.insert(0, str(RAIZ))
    from triton.core.climate_database import RECORTES_SUGERIDOS
    sugeridos = {(c, i, f) for c, lst in RECORTES_SUGERIDOS.items() for _, i, f in lst}
    for r in RECORTES:
        assert (r["cenario"], r["inicio"], r["fim"]) in sugeridos, f"recorte fora de RECORTES_SUGERIDOS: {r['id']}"
    mun = municipios_sc()
    aer = aeroportos(mun)
    arquivos = {FONTES / "municipios_sc_climbra.json": dump(
        {"fonte": "IBGE (API de localidades) × CLIMBra do programa; ver FONTES.json", "uf": UF, "total_ibge": len(mun["linhas"]),
         "total_na_climbra": sum(m["na_climbra"] for m in mun["linhas"]), "total_climbra": mun["total_climbra"],
         "homonimos_excluidos": mun["homonimos_excluidos"], "municipios": mun["linhas"]}),
        FONTES / "aeroportos_sc.json": dump({"fonte": "ANAC, Lista de Aeródromos Públicos (atualizada em 2026-10-15) e VRA 2025", "criterio": aer["criterio"],
                                              "aeroportos": aer["aeroportos"]})}
    na_climbra = [{"municipio": m["nome_climbra"], "ibge": m["ibge"]} for m in mun["linhas"] if m["na_climbra"]]
    dos_aeroportos = []
    for aero in DADOS_21_AEROPORTOS:
        dos_aeroportos.append({
            "id": aero["icao"].lower(),
            "municipio": aero["municipio"],
            "ibge": aero["ibge"],
            "clima_municipio": aero["clima_municipio"],
            "nome": f"{aero['icao']} - {aero['nome']}",
            "dimensoes": {
                "icao": aero["icao"],
                "aeroporto": aero["nome"],
                "classe": aero["classe"],
            },
            "substituicoes": {
                "area_captacao_m2": aero["area_captacao_m2"],
                "usuarios": aero["usuarios"],
                "demanda_per_capita_l_dia": 25.0,
                "fracao_pluvial_pct": 50.0,
                "volume_maximo_l": aero["volume_maximo_l"],
                "passo_volume_l": aero["passo_volume_l"],
                "delta_ideal_pct": aero["delta_ideal_pct"],
                "reservatorio_superior_l": aero["reservatorio_superior_l"],
                "limiar_bombeamento_l": aero["limiar_bombeamento_l"],
            },
        })
    estudos = {}
    for k, a in ARQUETIPOS.items():
        lista = na_climbra if a["municipios"] == "climbra" else dos_aeroportos
        estudos[k] = (a, lista)
        d = PASTA / a["pasta"]
        proj = projeto_triton(a)
        arquivos[d / f"{a['pasta']}.triton"] = json.dumps(proj, ensure_ascii=False, indent=2) + "\n"
        arquivos[d / "estudo.json"] = dump(estudo_json(a, lista))
        arquivos[d / "LEIA.md"] = leia(a, lista, mun, aer, proj)
        arquivos[d / "modelo_texto.md"] = modelo_texto(a)
    arquivos[PASTA / "LEIA.md"] = leia_geral(estudos, mun, aer)
    divergentes = []
    for caminho, texto in arquivos.items():
        if args.conferir:
            if not caminho.is_file() or caminho.read_text(encoding="utf-8") != texto:
                divergentes.append(caminho.relative_to(RAIZ).as_posix())
        else:
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_text(texto, encoding="utf-8", newline="\n")
    if args.conferir:
        print("divergentes:", divergentes or "nenhum")
        return 1 if divergentes else 0
    print(f"{len(arquivos)} arquivos; municípios SC na CLIMBra: {len(na_climbra)}; aeroportos no estudo: {len(dos_aeroportos)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
