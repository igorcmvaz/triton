# -*- coding: utf-8 -*-
"""Gera os apêndices A e B a partir do fonte.

O apêndice A tem 102 parâmetros e o B tem 24 processos. Transcrever isso à mão
significa divergir do programa no dia seguinte à publicação. Por isso os dois saem
daqui, lendo `NetunoConfig` e varrendo o pacote atrás de cada nome de campo.

Saída: manual/apendices/A_parametros.md e B_processos.md
"""

from __future__ import annotations

import ast
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
PKG = os.path.join(BASE, "netuno")
SAIDA = os.path.join(AQUI, "apendices")
os.makedirs(SAIDA, exist_ok=True)
NL = chr(10)

# ── de que módulo cada arquivo faz parte ─────────────────────────────────────
PAPEL = {
    "core/simulation.py": "Balanço diário",
    "core/calculator.py": "Índices de chuva",
    "core/economic.py": "Econômico",
    "core/environmental.py": "ACV",
    "core/environmental_justifications.py": "ACV",
    "core/environmental_sync.py": "ACV",
    "core/water_supply_routes.py": "ACV",
    "core/grid_emission_factors.py": "ACV",
    "core/esg_certifications.py": "Certificações",
    "core/edge_certification.py": "Certificações",
    "core/topsis.py": "Multicritério",
    "core/mcdm_methods.py": "Multicritério",
    "core/water_quality.py": "ETAP",
    "core/etap_integration.py": "ETAP",
    "core/chlorination.py": "ETAP",
    "core/cost_estimates.py": "Preços",
    "core/tariffs_database.py": "Tarifas",
    "core/tariffs_structure.py": "Tarifas",
    "core/tariff_regimes.py": "Tarifas",
    "core/tariff_category.py": "Tarifas",
    "core/climate_database.py": "Clima",
    "core/hydrology_defaults.py": "Clima",
    "core/pump_energy.py": "Motobomba",
    "core/pump_hydraulics.py": "Motobomba",
    "core/report_generator.py": "Relatórios",
    "core/report_service.py": "Relatórios",
    "core/cad_exporter.py": "CAD e BIM",
    "core/bim_exporter.py": "CAD e BIM",
    "core/excel_scenarios.py": "Planilhas",
    "core/simulation_excel_exporter.py": "Planilhas",
    "core/scenarios.py": "Cenários",
    "core/parser.py": "Arquivo do projeto",
    "cli.py": "Automação",
}

#: Telas que a janela principal nunca abre. Existem no pacote, e o usuário não
#: chega a elas: `tab_single_sim.py`, `tab_matrix_sim.py` e
#: `tab_scenarios_modern.py`. Ficam fora do apêndice para que ele não cite tela
#: inexistente; o capítulo 36 registra a pendência.
TELAS_ORFAS = ("tab_single_sim.py", "tab_matrix_sim.py",
               "tab_scenarios_modern.py", "dialog_scenario_simulation.py")

TELAS = {
    "tab_project.py": "Projeto", "tab_building.py": "Edificação",
    "tab_water_quality.py": "Qualidade",
    "tab_tanks_simulation.py": "Varredura",
    "tab_economic.py": "Econômico", "tab_economic_integrated.py": "Econ. integrado",
    "tab_economic_global_optimizer.py": "Otimizador", "tab_environmental.py": "Ambiental",
    "tab_tariffs_manager.py": "Tarifas",
    "tab_reports.py": "Relatórios", "tab_reports_pdf.py": "Relatórios",
    "tab_charts_netuno.py": "Gráficos", "tab_export.py": "Exportação",
    "tab_documentation.py": "Documentação", "main_window.py": "Janela principal",
    "dialog_economic.py": "Tarifas e custos", "dialog_monthly_values.py": "Valores mensais",
    "dialog_upper_tank.py": "Caixa superior", "dialog_variable_input.py": "Entrada variável",
    "pump_wizard_dialog.py": "Assistente da bomba",
    "dialog_validation_report.py": "Validação",
}

assert not (set(TELAS_ORFAS) & set(TELAS)), (
    "tela inalcançável listada em TELAS: a janela principal não a abre, e o "
    "apêndice mandaria o leitor procurar uma tela que não existe"
)

SECOES = [
    ("project_id", "Identificação"), ("project_name", "Identificação"),
    ("created_at", "Identificação"),
    ("building_template_id", "Edificação"), ("num_economias", "Edificação"),
    ("climate", "Chuva"), ("precip", "Chuva"), ("start_date", "Chuva"),
    ("area", "Captação"), ("runoff", "Captação"), ("discard", "Captação"),
    ("irrigation", "Irrigação"),
    ("chlorine", "Qualidade da água"), ("water_quality", "Qualidade da água"),
    ("etap", "Qualidade da água"),
    ("pump", "Motobomba"),
    ("lower_tank", "Reservatórios"), ("upper_tank", "Reservatórios"),
    ("pumping", "Reservatórios"), ("delta_ideal", "Reservatórios"),
    ("pipe", "Tubulação"),
    ("cost_", "Investimento"), ("op_costs", "Operação"), ("maintenance", "Operação"),
    ("water_tariff", "Tarifas"), ("sewage", "Tarifas"), ("water_tax", "Tarifas"),
    ("tariff", "Tarifas"),
    ("elec", "Energia"),
    ("iptu", "Incentivos"),
    ("demand", "Demanda"), ("residents", "Demanda"), ("share", "Demanda"),
    ("weekly", "Demanda"), ("monthly", "Demanda"), ("daily", "Demanda"),
    ("tma", "Financeiro"), ("inflation", "Financeiro"),
    ("analysis_period", "Financeiro"), ("install_month", "Financeiro"),
    ("econ_", "Financeiro"), ("material", "Reservatórios"),
    ("edge_", "Certificações"),
]

ORDEM = ["Identificação", "Chuva", "Captação", "Edificação", "Demanda", "Irrigação",
         "Qualidade da água", "Reservatórios", "Motobomba", "Tubulação",
         "Investimento", "Operação", "Tarifas", "Energia", "Incentivos",
         "Financeiro", "Certificações", "Outros"]

UNIDADES = {
    "area": "m²", "runoff_coeff": "—", "discard": "mm", "discard_days_interval": "dias",
    "delta_ideal": "%/m³", "lower_tank_fixed": "L", "lower_tank_max": "L",
    "lower_tank_step": "L", "upper_tank_vol": "L", "pumping_threshold": "L",
    "econ_lower_tank_vol": "L", "pump_power_kw": "kW", "pump_flow_rate": "L/h",
    "pump_efficiency": "%", "pump_motor_efficiency": "%", "pump_startup_time_h": "h",
    "pump_unit_cost": "R$", "pump_manometric_head_m": "m.c.a.", "pump_count": "un",
    "demand_value": "L/dia", "residents_count": "hab", "num_economias": "un",
    "potable_indoor_share": "fração", "non_potable_indoor_share": "fração",
    "rainwater_share": "fração", "irrigation_garden_area_m2": "m²",
    "irrigation_rate_l_m2_day": "L/m²·dia", "irrigation_liters_per_day": "L/dia",
    "irrigation_rain_threshold_mm": "mm/dia", "chlorine_dose_mg_l": "mg Cl₂/L",
    "chlorine_product_purity": "kg/kg", "chlorine_cost_per_kg": "R$/kg",
    "chlorine_co2_kg_per_kg": "kg CO₂e/kg", "tma": "%/mês", "inflation": "%/mês",
    "analysis_period_years": "anos", "sewage_rate": "% da água",
    "water_tax_fixed": "R$/mês", "water_tax_var": "%", "elec_tariff": "R$/kWh",
    "elec_tax_fixed": "R$/mês", "elec_tax_var": "%", "iptu_annual_value": "R$/ano",
    "iptu_discount_pct": "%", "cost_lower_tank": "R$", "cost_upper_tank": "R$",
    "cost_labor": "R$", "cost_piping": "R$", "cost_accessories": "R$",
    "water_tariff_escalation": "%/ano", "sewage_tariff_escalation": "%/ano",
    "elec_tariff_escalation": "%/ano", "tariff_escalation": "meses",
    "install_month": "mês", "edge_base_case_l_person_day": "L/pessoa·dia",
    "discard_mode": "código", "demand_type": "código", "residents_type": "código",
    "upper_tank_used": "código", "lower_tank_mode": "código", "sewage_mode": "código",
}


def secao(nome):
    for chave, sec in SECOES:
        if nome.startswith(chave) or chave in nome:
            return sec
    return "Outros"


def fontes():
    out = {}
    for raiz, dirs, nomes in os.walk(PKG):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in sorted(nomes):
            if n.endswith(".py"):
                p = os.path.join(raiz, n)
                rel = os.path.relpath(p, PKG).replace("\\", "/")
                out[rel] = open(p, encoding="utf-8", errors="replace").read()
    return out


def apendice_a():
    src = open(os.path.join(PKG, "core", "parser.py"), encoding="utf-8").read()
    linhas_fonte = src.split(NL)
    arv = ast.parse(src)
    FONTES = fontes()

    campos = []
    for no in ast.walk(arv):
        if isinstance(no, ast.ClassDef) and no.name == "NetunoConfig":
            for item in no.body:
                if not (isinstance(item, ast.AnnAssign)
                        and isinstance(item.target, ast.Name)):
                    continue
                nome = item.target.id
                m = re.search(r"#\s*(.+)$", linhas_fonte[item.lineno - 1])
                nota = m.group(1).strip() if m else ""
                try:
                    padrao = ast.literal_eval(item.value) if item.value else None
                except (ValueError, TypeError, SyntaxError):
                    padrao = None
                if isinstance(padrao, (list, tuple)):
                    padrao = "vazio" if not padrao else f"{len(padrao)} itens"
                elif isinstance(padrao, bool):
                    padrao = "sim" if padrao else "não"
                elif isinstance(padrao, float):
                    padrao = f"{padrao:g}".replace(".", ",")
                elif padrao is None or padrao == "":
                    padrao = "—"
                else:
                    padrao = str(padrao)

                alvo = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(nome)
                                  + r"(?![A-Za-z0-9_])")
                mods, telas = set(), set()
                for rel, texto in FONTES.items():
                    if not alvo.search(texto):
                        continue
                    if rel in PAPEL:
                        mods.add(PAPEL[rel])
                    base = os.path.basename(rel)
                    if rel.startswith("ui/") and base in TELAS:
                        telas.add(TELAS[base])
                campos.append({
                    "n": nome, "p": padrao, "u": UNIDADES.get(nome, ""),
                    "nota": nota, "sec": secao(nome),
                    "mods": sorted(mods - {"Arquivo do projeto"}),
                    "telas": sorted(telas),
                })

    por_sec = {}
    for c in campos:
        por_sec.setdefault(c["sec"], []).append(c)

    L = [
        "# Apêndice A — Os parâmetros do projeto",
        "",
        f"São **{len(campos)} parâmetros**. É a lista completa do que um projeto",
        "guarda, com o nome exato de cada campo dentro do arquivo `.netuno`.",
        "",
        "A lista não foi transcrita à mão: é extraída do próprio programa a cada",
        "versão, e por isso não pode divergir dele.",
        "",
        "A coluna **onde se informa** diz em que tela o campo aparece; a coluna",
        "**quem consome** diz que cálculo o usa. Campo sem nenhuma das duas é campo",
        "gravado no arquivo e nunca lido, e está listado no capítulo 34.",
        "",
    ]
    for sec in ORDEM:
        if sec not in por_sec:
            continue
        grupo = por_sec[sec]
        L += [f"## A.{ORDEM.index(sec) + 1}. {sec}", "",
              f"{len(grupo)} parâmetros.", "",
              "| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |",
              "| :--- | ---: | :--- | :--- | :--- |"]
        for c in grupo:
            telas = ", ".join(c["telas"]) or "—"
            mods = ", ".join(c["mods"]) or "—"
            L.append(f"| `{c['n']}` | {c['p']} | {c['u'] or '—'} | {telas} | {mods} |")
        notas = [c for c in grupo if c["nota"]]
        if notas:
            L += ["", "Observações do fonte:", ""]
            for c in notas:
                L.append(f"- `{c['n']}`: {c['nota']}")
        L.append("")
    return NL.join(L), len(campos)


def apendice_b():
    sys.path.insert(0, os.path.join(BASE, "..", "..", "scratchpad"))
    caminho = os.path.join(AQUI, "processos.py")
    if not os.path.exists(caminho):
        return None, 0
    espaco = {}
    exec(compile(open(caminho, encoding="utf-8").read(), caminho, "exec"), espaco)
    PROCESSOS = espaco["PROCESSOS"]
    FAMILIAS = espaco["FAMILIAS"]

    L = [
        "# Apêndice B — Os processos do programa",
        "",
        f"São **{len(PROCESSOS)} processos**, do arquivo de chuva ao relatório. Cada",
        "um declara o que o dispara, o que recebe, as regras com suas ramificações, o",
        "que produz e o que acontece quando falha.",
        "",
        "É o apêndice mais técnico do manual, e serve a duas pessoas: quem revisa um",
        "estudo feito com o programa e precisa saber exatamente que conta foi feita, e",
        "quem encontrou um resultado estranho e quer saber por onde o número passou.",
        "",
        "Os nomes em `código` são os campos do arquivo de projeto, listados no",
        "apêndice A.",
        "",
    ]
    for pid, nome, fam, gatilho, entradas, regras, fns, saidas, excecao in PROCESSOS:
        rot = FAMILIAS[fam][0]
        L += [f"## {pid} — {nome}", "", f"*{rot}*", "",
              f"**Gatilho.** {_limpa(gatilho)}", "", "**Entradas**", ""]
        L += [f"- {_limpa(e)}" for e in entradas]
        L += ["", "**Regras**", ""]
        L += [f"{i}. {_limpa(r)}" for i, r in enumerate(regras, 1)]
        L += ["", "**Saídas**", ""]
        L += [f"- {_limpa(s)}" for s in saidas]
        # As funções internas de cada processo ficam fora do manual: o leitor
        # instala um executável, e nome de função só ajuda quem tem o fonte.
        L += ["", f"**Exceção.** {_limpa(excecao)}", ""]
    return NL.join(L), len(PROCESSOS)


def _limpa(t):
    t = re.sub(r"<code>(.*?)</code>", r"`\1`", t)
    t = re.sub(r"<b>(.*?)</b>", r"**\1**", t)
    t = re.sub(r"<i>(.*?)</i>", r"*\1*", t)
    t = t.replace("&rarr;", "→").replace("&nbsp;", " ").replace("&mdash;", "—")
    t = re.sub(r"<[^>]+>", "", t)
    return t


def apendice_d():
    """Regimes tarifários e a base dos 652 municípios, lidos da própria base."""
    import json
    from collections import Counter

    caminho = os.path.join(PKG, "data", "brazil_cities_tariffs.json")
    if not os.path.exists(caminho):
        return None, 0
    base = json.load(open(caminho, encoding="utf-8"))
    cidades = base["cities"]
    regimes = Counter(c.get("regime_tarifario") for c in cidades.values())

    NOMES = {
        "sem_minimo": ("Sem mínimo",
                       "Cada m³ economizado desconta na conta."),
        "disponibilidade": ("Disponibilidade",
                            "Valor fixo que **soma** por cima do consumo medido. "
                            "Cada m³ economizado desconta."),
        "franquia_no_minimo": ("Franquia no mínimo",
                               "O valor fixo já inclui um volume. Economizar **abaixo** "
                               "da franquia não desconta nada."),
        "franquia_retroativa": ("Franquia retroativa",
                                "Até a franquia paga-se o fixo; passando dela, "
                                "tarifa-se **tudo desde zero**."),
        "piso_de_pagamento": ("Piso de pagamento",
                              "A conta **não desce** abaixo do piso. Não soma: limita."),
    }
    CODIGOS = {
        "1 ou 0": "faixa progressiva, cobra só o volume dentro dela",
        "−1": "custo de disponibilidade, soma por cima",
        "−2": "franquia retroativa",
        "−3": "piso de pagamento",
    }

    L = [
        "# Apêndice D — Regimes tarifários",
        "",
        f"A base traz **{len(cidades)} municípios** com estrutura tarifária, percentual",
        "de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída",
        "da própria base do programa, e não transcrita.",
        "",
        "## D.1. Os códigos de faixa",
        "",
        "Cada linha da tabela tarifária é uma quádrupla "
        "`(mínimo, máximo, valor, código)`:",
        "",
        "| Código | Significado |",
        "| ---: | :--- |",
    ]
    for cod, desc in CODIGOS.items():
        L.append(f"| {cod} | {desc} |")

    L += ["", "## D.2. Os cinco regimes", "",
          "| Regime | Municípios | O que acontece ao economizar |",
          "| :--- | ---: | :--- |"]
    for chave, (nome, desc) in NOMES.items():
        L.append(f"| **{nome}** | {regimes.get(chave, 0)} | {desc} |")

    L += ["",
          "> O piso de pagamento está implementado e nenhum município da base foi",
          "> classificado nele até esta versão.",
          "",
          "## D.3. Distribuição por unidade da federação", "",
          "| UF | Municípios |", "| :--- | ---: |"]
    por_uf = Counter(c.get("uf") for c in cidades.values())
    for uf in sorted(x for x in por_uf if x):
        L.append(f"| {uf} | {por_uf[uf]} |")

    L += ["", "## D.4. Grau de confiança", "",
          "Cada registro traz o grau de confiança da coleta:", "",
          "| Grau | Registros |", "| :--- | ---: |"]
    conf = Counter(c.get("confianca_grau", "não informado") for c in cidades.values())
    for grau, n in conf.most_common():
        L.append(f"| {grau} | {n} |")

    L += ["",
          "> **Confira sempre a data de vigência** do registro do seu município contra a",
          "> resolução da concessionária. Tarifas são reajustadas anualmente, e o guia 16",
          "> ensina o teste que identifica estrutura errada.", ""]
    return NL.join(L), len(cidades)


def main():
    texto, n = apendice_a()
    p = os.path.join(SAIDA, "A_parametros.md")
    open(p, "w", encoding="utf-8").write(texto + NL)
    print(f"  A_parametros.md — {n} parâmetros")

    texto, n = apendice_b()
    if texto is None:
        print("  B_processos.md — pulado: falta manual/processos.py")
    else:
        p = os.path.join(SAIDA, "B_processos.md")
        open(p, "w", encoding="utf-8").write(texto + NL)
        print(f"  B_processos.md — {n} processos")

    texto, n = apendice_d()
    if texto is None:
        print("  D_regimes_tarifarios.md — pulado: base não encontrada")
    else:
        p = os.path.join(SAIDA, "D_regimes_tarifarios.md")
        open(p, "w", encoding="utf-8").write(texto + NL)
        print(f"  D_regimes_tarifarios.md — {n} municípios")

    # O apêndice F é escrito à mão: descreve arquivos, pastas e formatos do
    # programa instalado, e não há de onde extraí-lo automaticamente.


if __name__ == "__main__":
    print("apêndices do manual:")
    main()
