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

METRICAS = ["volume_l", "economia_agua_potavel_pct", "agua_pluvial_m3_ano", "extravasamento_m3_ano",
            "dias_atendimento_total_pct", "economia_anual_agua", "capex", "vpl", "payback_descontado_meses"]

#: Arquétipos por tipologia. TODOS os números são estimativas de arquétipo (nenhum é dado medido nem de norma):
#: o autor os substitui pelos seus, com fonte. ``tarifa`` é só a categoria do catálogo de tarifas do programa.
ARQUETIPOS = {
    "escolar": dict(
        pasta="escolar", id="sc-escolar", tipologia="escolar", municipios="climbra",
        titulo="Edifícios escolares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="escola pública de ensino básico de porte médio",
        area_captacao_m2=1500, usuarios=600, demanda_per_capita_l_dia=50, fracao_pluvial_pct=40,
        volume_maximo_l=40000, passo_volume_l=1000, reservatorio_superior_l=5000, tarifa="publica",
        usuarios_texto="alunos, professores e funcionários presentes por dia"),
    "comercial": dict(
        pasta="comercial", id="sc-comercial", tipologia="comercial", municipios="climbra",
        titulo="Edifícios comerciais em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="edifício de escritórios e serviços de porte médio",
        area_captacao_m2=1200, usuarios=300, demanda_per_capita_l_dia=45, fracao_pluvial_pct=50,
        volume_maximo_l=20000, passo_volume_l=500, reservatorio_superior_l=3000, tarifa="comercial",
        usuarios_texto="ocupantes e visitantes presentes por dia"),
    "residencial-unifamiliar": dict(
        pasta="residencial-unifamiliar", id="sc-residencial-unifamiliar", tipologia="residencial-unifamiliar", municipios="climbra",
        titulo="Residências unifamiliares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="casa unifamiliar de padrão médio",
        area_captacao_m2=120, usuarios=4, demanda_per_capita_l_dia=150, fracao_pluvial_pct=40,
        volume_maximo_l=10000, passo_volume_l=250, reservatorio_superior_l=500, tarifa="residencial",
        usuarios_texto="moradores"),
    "residencial-multifamiliar": dict(
        pasta="residencial-multifamiliar", id="sc-residencial-multifamiliar", tipologia="residencial-multifamiliar",
        municipios="climbra",
        titulo="Residências multifamiliares em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="prédio residencial de 16 unidades",
        area_captacao_m2=600, usuarios=48, economias=16, demanda_per_capita_l_dia=150, fracao_pluvial_pct=40,
        volume_maximo_l=20000, passo_volume_l=500, reservatorio_superior_l=2500, tarifa="residencial",
        usuarios_texto="moradores de todas as unidades"),
    "hospitalar": dict(
        pasta="hospitalar", id="sc-hospitalar", tipologia="hospitalar", municipios="climbra",
        titulo="Hospitais em Santa Catarina: municípios da CLIMBra, 19 modelos, 7 recortes",
        descricao="hospital geral de porte médio",
        area_captacao_m2=4000, usuarios=300, demanda_per_capita_l_dia=250, fracao_pluvial_pct=25,
        volume_maximo_l=60000, passo_volume_l=1500, reservatorio_superior_l=10000, tarifa="publica",
        usuarios_texto="pacientes, acompanhantes e equipe presentes por dia, em equivalentes"),
    "aeroportuario": dict(
        pasta="aeroportos", id="sc-aeroportuario", tipologia="aeroportuario", municipios="aeroportos",
        titulo="Aeroportos de Santa Catarina com voos regulares: municípios da CLIMBra com aeroporto, 19 modelos, 7 recortes",
        descricao="terminal de passageiros e apoio de aeroporto regional",
        area_captacao_m2=8000, usuarios=3000, demanda_per_capita_l_dia=25, fracao_pluvial_pct=50,
        volume_maximo_l=120000, passo_volume_l=3000, reservatorio_superior_l=10000, tarifa="comercial",
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

def estudo_json(a: dict, lista: list) -> dict:
    subs = {"_origem": ROTULO_ARQUETIPO + "; ver LEIA.md",
            "area_captacao_m2": a["area_captacao_m2"], "usuarios": a["usuarios"],
            "demanda_per_capita_l_dia": a["demanda_per_capita_l_dia"], "fracao_pluvial_pct": a["fracao_pluvial_pct"],
            "volume_maximo_l": a["volume_maximo_l"], "passo_volume_l": a["passo_volume_l"],
            "reservatorio_superior_l": a["reservatorio_superior_l"]}
    if "economias" in a:
        subs["economias"] = a["economias"]
    return {
        "esquema": {"nome": "triton-estudo", "versao": 1},
        "estudo": {"id": a["id"], "titulo": a["titulo"], "tipologia": a["tipologia"], "autores": [],
                   "nota": ("Valores de edificação = estimativas de arquétipo, a refinar pelo autor (LEIA.md). Clima: CLIMBra, "
                            "19 modelos × 7 recortes sugeridos pelo programa. Tarifas e custos preliminares: os do programa.")},
        "projeto_base": {"modelo": "edicao"},
        "padroes": {"substituicoes": subs,
                    "tarifa": {"categoria": a["tarifa"], "se_ausente": "residencial",
                               "_origem": "categoria do catálogo de tarifas do programa; sem tabela coletada, usa a residencial e registra alerta"}},
        "expansao": {"uf": UF, "modelos": "todos", "recortes": RECORTES, "municipios": lista},
        "analise": {"tipo": "economic", "volume": "otimo_tecnico", "semente": 42},
        "saidas": {"formatos": ["csv", "json", "md", "tex"], "metricas": METRICAS,
                   "casas_decimais": {"padrao": 1, "volume_l": 0, "capex": 0, "vpl": 0, "payback_descontado_meses": 0},
                   "idioma": "pt-BR", "gravar_analise": False},
    }


def modelo_texto(a: dict) -> str:
    return (f"# Modelo de texto: {a['titulo']}\n\n"
            f"Nos {{{{n_casos}}}} casos (município × modelo climático × recorte), a economia de água potável do arquétipo «{a['descricao']}» "
            "ficou entre {{economia_agua_potavel_pct:@min}}% e {{economia_agua_potavel_pct:@max}}% "
            "(média de {{economia_agua_potavel_pct:@media}}%), com o reservatório no ótimo técnico de cada caso "
            "(mediana de {{volume_l:@mediana}} L). Valores de edificação são estimativas de arquétipo, a refinar pelo autor.\n")


def leia(a: dict, lista: list, mun: dict, aer: dict) -> str:
    n = len(lista)
    ncasos = n * 19 * len(RECORTES)
    linhas = [f"# {a['titulo']}", "",
              f"Estudo `{a['id']}` (esquema `triton-estudo`, versão 1), gerado por `scripts/gerar_estudos_sc.py`. "
              f"Arquétipo: **{a['descricao']}**. Não edite o `estudo.json` à mão sem registrar: o gerador o reescreve.", "",
              "## Escopo", ""]
    if a["municipios"] == "climbra":
        linhas += [f"- Municípios: os **{n}** de Santa Catarina presentes na base CLIMBra (de 295 do IBGE; 263 não têm série). "
                   "A lista, com o código IBGE e os ausentes, está em `../_fontes/municipios_sc_climbra.json`."]
    else:
        linhas += [f"- Municípios: os **{n}** com aeroporto de voos regulares e série na CLIMBra. Critério e lista completa "
                   "(inclusive os excluídos e o motivo) em `../_fontes/aeroportos_sc.json`:", ""]
        for x in aer["aeroportos"]:
            if x["regular"] or x["meses_com_voo_regular_2025"]:
                st = "no estudo" if x["regular"] and x["municipio_na_climbra"] else x.get("motivo", "")
                linhas.append(f"  - {x['icao']} {x['nome']} ({x['municipio_anac']}): {x['movimentos_regulares_2025']} movimentos "
                              f"regulares em 2025, {x['meses_com_voo_regular_2025']} meses com voo; {st}.")
        linhas.append(f"  - Critério: {aer['criterio']}.")
    linhas += [f"- Clima: CLIMBra (Ballarin et al., 2023, doi:10.1038/s41597-023-01956-z; CC0), **19 modelos** × **{len(RECORTES)} recortes** "
               f"(`expansao.recortes`): histórico 1981–2010 e, para SSP2-4.5 e SSP5-8.5, futuro próximo 2021–2050, meados 2041–2070 e fim 2071–2100, "
               "os atalhos de `RECORTES_SUGERIDOS`. A série é a da célula de 0,25° do município; o histórico é simulado, não observado.",
               f"- Casos: {n} × 19 × {len(RECORTES)} = **{ncasos}** simulações (cada uma varre os volumes do reservatório).",
               "- Análise: `economic`, volume no ótimo técnico, semente 42. Custos: estimativa preliminar do próprio programa (catálogo de preços), "
               "tarifas: catálogo municipal do programa.", "",
               "## Arquétipo (todos os valores: estimativa de arquétipo, a refinar pelo autor)", "",
               "| Parâmetro | Valor | Origem |", "| --- | ---: | --- |"]
    rot = [("area_captacao_m2", "Área de captação (m²)"), ("usuarios", f"Usuários ({a['usuarios_texto']})"),
           ("economias", "Economias (unidades)"), ("demanda_per_capita_l_dia", "Demanda por usuário (L/dia)"),
           ("fracao_pluvial_pct", "Fração atendível por chuva (%)"), ("volume_maximo_l", "Maior volume da varredura (L)"),
           ("passo_volume_l", "Passo da varredura (L)"), ("reservatorio_superior_l", "Reservatório superior (L)")]
    for k, r in rot:
        if k in a:
            linhas.append(f"| {r} | {a[k]} | {ROTULO_ARQUETIPO} |")
    linhas += [f"| Categoria tarifária | {a['tarifa']} | escolha de arquétipo; sem tabela coletada para o município, usa a residencial (alerta no resultado) |",
               "| Coeficiente de escoamento, descarte, demais campos | os do modelo da edição | padrão do programa |", "",
               "Nenhum desses valores é medido nem tirado de norma. Para refinar, edite `padroes.substituicoes` (ou os do script) e cite a fonte de cada um; "
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
        "}", "```", ""])


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
    vistos = set()
    for x in aer["aeroportos"]:
        if x["regular"] and x["municipio_na_climbra"] and x["ibge"] not in vistos:
            vistos.add(x["ibge"])
            dos_aeroportos.append({"municipio": x["nome_climbra"], "ibge": x["ibge"]})
    estudos = {}
    for k, a in ARQUETIPOS.items():
        lista = na_climbra if a["municipios"] == "climbra" else dos_aeroportos
        estudos[k] = (a, lista)
        d = PASTA / a["pasta"]
        arquivos[d / "estudo.json"] = dump(estudo_json(a, lista))
        arquivos[d / "LEIA.md"] = leia(a, lista, mun, aer)
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
