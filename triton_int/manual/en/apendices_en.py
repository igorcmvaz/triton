# -*- coding: utf-8 -*-
"""Generates appendices A, B and D of the English manual from the source.

The same data as the Portuguese appendices (manual/gerar_apendices.py), with English
labels. A label or a code note without a translation stops the generation and names
what is missing: a new parameter added to `TritonConfig` cannot reach the English manual
in Portuguese.

Output: manual/en/apendices/A_parametros.md, B_processos.md, D_regimes_tarifarios.md
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.dirname(AQUI)
RAIZ = os.path.dirname(MANUAL)
for _p in (MANUAL, AQUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gerar_apendices as G  # noqa: E402
from escrita_segura import gravar  # noqa: E402

SAIDA = os.path.join(AQUI, "apendices")
NL = chr(10)

SECOES = {
    "Identificação": "Identification", "Chuva": "Rainfall", "Captação": "Catchment",
    "Edificação": "Building", "Demanda": "Demand", "Irrigação": "Irrigation",
    "Qualidade da água": "Water quality", "Reservatórios": "Tanks",
    "Motobomba": "Pump set", "Tubulação": "Piping", "Investimento": "Investment",
    "Operação": "Operation", "Tarifas": "Tariffs", "Energia": "Energy",
    "Incentivos": "Incentives", "Financeiro": "Financial", "Certificações": "Certifications",
    "Outros": "Other",
}

#: Screens and calculation modules, as appendix A names them.
NOMES = {
    "ACV": "LCA", "Ambiental": "Environmental", "Assistente da bomba": "Pump wizard",
    "Automação": "Automation", "Balanço diário": "Daily balance", "CAD e BIM": "CAD and BIM",
    "Caixa superior": "Upper tank", "Cenários": "Scenarios", "Clima": "Climate",
    "Documentação": "Documentation", "ETAP": "Treatment line", "Econômico": "Economic",
    "Edificação": "Building", "Exportação": "Export", "Gráficos": "Charts",
    "Janela principal": "Main window", "Motobomba": "Pump set", "Multicritério": "Multi-criteria",
    "Otimizador": "Optimiser", "Planilhas": "Spreadsheets", "Preços": "Prices",
    "Projeto": "Project", "Qualidade": "Quality", "Relatórios": "Reports", "Tarifas": "Tariffs",
    "Tarifas e custos": "Tariffs and costs", "Varredura": "Sweep", "Certificações": "Certifications",
    "Índices de chuva": "Rainfall indices", "Valores mensais": "Monthly values",
    "Entrada variável": "Variable input", "Validação": "Validation",
}

UNIDADES = {
    "1/pessoa·dia": "1/person·day", "código": "code", "dias": "days", "%/m³": "%/m³",
    "un": "units", "L/dia": "L/day", "hab": "residents", "fração": "fraction",
    "L/m²·dia": "L/m²·day", "mm/dia": "mm/day", "% ao mês": "% per month", "anos": "years",
    "% da água": "% of water", "R$/mês": "R$/month", "R$/ano": "R$/year",
    "% por período": "% per period", "meses": "months", "mês": "month",
    "L/pessoa·dia": "L/person·day", "m.c.a.": "m head",
}

PADROES = {"Novo projeto Triton": "New Triton project"}

#: The code notes of `TritonConfig`, translated. The key is the field name, and the
#: Portuguese note is kept beside it: when the note changes in the code, the English
#: one is refused until it is reviewed.
NOTAS = {
    "climate_source_mode": ('"national_db" (base nacional) ou "custom_file" (arquivo próprio)',
                            '"national_db" (national database, Brazil Edition) or "custom_file" (own file)'),
    "discard": ("mm", "mm"),
    "discard_mode": ("1 = todos os eventos, 2 = 1º evento após estiagem, 3 = a cada X dias",
                     "1 = every event, 2 = first event after a dry spell, 3 = every X days"),
    "discard_days_interval": ("intervalo para modo 3", "interval for mode 3"),
    "area": ("m²", "m²"),
    "irrigation_garden_area_m2": ("Área de jardim em m² para o assistente de dimensionamento",
                                  "Garden area in m² for the sizing wizard"),
    "runoff_coeff": ("ver hydrology_defaults", "see hydrology_defaults"),
    "num_economias": ("Número de economias / apartamentos com micromedição individual",
                      "Number of dwelling units / apartments with individual metering"),
    "demand_mode": ('"constant", "weekly", "monthly", "daily"', '"constant", "weekly", "monthly", "daily"'),
    "demand_value": ("L/dia, por habitante ou total", "L/day, per resident or total"),
    "potable_indoor_share": ("Fração potável do consumo interno; 1 − non_potable_indoor_share",
                             "Potable fraction of indoor consumption; 1 − non_potable_indoor_share"),
    "non_potable_indoor_share": ("Fração não potável do consumo interno (bacias, máquina); ver fracao_atendivel",
                                 "Non-potable fraction of indoor consumption (toilets, washing machine); see fracao_atendivel"),
    "rainwater_share": ("fração de 0 a 1 (0,4 = 40%)", "fraction from 0 to 1 (0.4 = 40%)"),
    "irrigation_liters_per_day": ("Demanda externa (rega, lavagem de áreas externas), L/dia",
                                  "Outdoor demand (watering, washing outdoor areas), L/day"),
    "irrigation_rain_threshold_mm": ("Limiar diário de precipitação para supressão da irrigação (mm/dia)",
                                     "Daily precipitation threshold that suppresses irrigation (mm/day)"),
    "irrigation_potable_backup": ("Se True, a rede pública atende a irrigação em dias secos se a cisterna secar",
                                  "If True, the mains supplies irrigation on dry days when the cistern runs dry"),
    "irrigation_rate_l_m2_day": ("Taxa diária de rega (L/m²/dia)", "Daily watering rate (L/m²/day)"),
    "water_quality_disinfection": ('"cloro", "uv", "ozonio", "nenhum"',
                                   '"cloro" (chlorine), "uv", "ozonio" (ozone), "nenhum" (none)'),
    "chlorine_dose_mg_l": ("mg de Cl2 ativo por litro", "mg of active Cl2 per litre"),
    "chlorine_product_purity": ("kg Cl2 ativo por kg de produto", "kg of active Cl2 per kg of product"),
    "chlorine_cost_per_kg": ("R$ por kg de PRODUTO comercial", "price per kg of commercial PRODUCT"),
    "upper_tank_vol": ("L", "L"),
    "upper_tank_used": ("0 = sem caixa superior, 1 = com caixa superior", "0 = no upper tank, 1 = with upper tank"),
    "lower_tank_max": ("L", "L"),
    "lower_tank_step": ("L", "L"),
    "lower_tank_mode": ("0 = volume fixo, 1 = varredura", "0 = fixed volume, 1 = sweep"),
    "lower_tank_fixed": ("usado no modo de volume fixo", "used in fixed-volume mode"),
    "delta_ideal": ("limiar de ganho marginal para o volume ideal, em %/m³",
                    "marginal-gain threshold for the ideal volume, in %/m³"),
    "lower_tank_material": ('"PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"',
                            '"PEAD" (HDPE), "CONCRETO" (concrete), "FIBRA" (GRP), "ACO_INOX" (stainless steel)'),
    "upper_tank_material": ('"PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"',
                            '"PEAD" (HDPE), "CONCRETO" (concrete), "FIBRA" (GRP), "ACO_INOX" (stainless steel)'),
    "pumping_threshold": ("L, nível de acionamento do recalque", "L, pump trigger level"),
    "pump_count": ("principal + reserva como configuração inicial recomendada",
                   "duty + standby as the recommended initial configuration"),
    "pump_power_kw": ("kW (1 CV = 0,7355 kW; 1/2 CV = 0,36775 kW)", "kW (1 hp (metric) = 0.7355 kW; 1/2 hp = 0.36775 kW)"),
    "pump_efficiency": ("%, 0 = deduzir do porte", "%, 0 = deduce from the size"),
    "pump_startup_time_h": ("h", "h"),
    "pump_motor_efficiency": ("%", "%"),
    "pump_unit_cost": ("R$, referência de mercado para motobomba periférica 1/2 CV",
                       "R$, Brazilian market reference for a 1/2 hp peripheral pump (zero in the International Edition)"),
    "sewage_mode": ("0 = valor fixo em R$, 1 = percentual da parcela de água, 2 = R$/m³ consumido, 3 = escalões",
                    "0 = fixed amount, 1 = percentage of the water part, 2 = amount per m³ consumed, 3 = tiers"),
    "water_tax_fixed": ("R$", "currency"),
    "water_tax_var": ("%", "%"),
    "tariff_escalation": ("meses; comprimento do período de reajuste", "months; length of the escalation period"),
    "water_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                "% per escalation period; with 12 months, % per year"),
    "sewage_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                 "% per escalation period; with 12 months, % per year"),
    "elec_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                               "% per escalation period; with 12 months, % per year"),
    "tariff_flag": ('"verde", "amarela", "vermelha_1", "vermelha_2", "branca"',
                    '"verde" (green), "amarela" (yellow), "vermelha_1" (red 1), "vermelha_2" (red 2), "branca" (white); Brazil Edition'),
    "elec_tariff": ("R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)",
                    "per kWh (Brazil Edition default: residential B1 tariff, CELESC, Florianópolis)"),
    "elec_tax_fixed": ("R$", "currency"),
    "elec_tax_var": ("%", "%"),
    "iptu_annual_value": ("Valor venal do IPTU anual da edificação (R$/ano)",
                          "Annual municipal property tax (IPTU) of the building, per year; Brazil Edition"),
    "iptu_discount_pct": ("Desconto municipal do IPTU Verde (%)", "Municipal green property-tax discount (IPTU Verde, %); Brazil Edition"),
    "inflation": ("% ao mês; inflação dos custos de O&M", "% per month; inflation of O&M costs"),
    "analysis_period_years": ("anos", "years"),
    "tariff_category": ('categoria da tabela tarifária aplicada; "personalizada" quando digitada',
                        'category of the tariff table applied; "personalizada" (custom) when typed in'),
    "tma": ("% ao mês; taxa mínima de atratividade", "% per month; minimum attractive rate of return"),
}


def _nome(rotulo):
    if rotulo not in NOMES:
        raise SystemExit(f"apêndice A em inglês: falta traduzir o rótulo «{rotulo}» em NOMES")
    return NOMES[rotulo]


def padrao_em_ingles(padrao):
    if isinstance(padrao, (list, tuple)):
        return "empty" if not padrao else f"{len(padrao)} items"
    if isinstance(padrao, bool):
        return "yes" if padrao else "no"
    if isinstance(padrao, float):
        return f"{padrao:g}"
    if padrao is None or padrao == "":
        return "—"
    texto = str(padrao)
    if len(texto) == 10 and texto[2] == "/" and texto[5] == "/":
        dia, mes, ano = texto.split("/")
        return f"{ano}-{mes}-{dia}"
    return PADROES.get(texto, texto)


def apendice_a():
    campos = G.campos_do_projeto()
    faltam = []
    for c in campos:
        if c["nota"]:
            par = NOTAS.get(c["n"])
            if par is None or par[0] != c["nota"]:
                faltam.append(f"{c['n']}: {c['nota']}")
    if faltam:
        raise SystemExit("apêndice A em inglês: nota do código sem tradução revisada em NOTAS:"
                         + NL + NL.join("  " + f for f in faltam))

    por_sec = {}
    for c in campos:
        por_sec.setdefault(c["sec"], []).append(c)

    L = [
        "# The project parameters",
        "",
        f"There are **{len(campos)} parameters**. This is the complete list of what a project",
        "stores, with the exact name of each field inside the `.triton` file.",
        "",
        "The list was not transcribed by hand: it is extracted from the program itself for",
        "each version, and therefore cannot diverge from it.",
        "",
        "The column **where it is entered** says on which screen the field appears; the",
        "column **who consumes it** says which calculation uses it. A field with neither is a",
        "field stored in the file and never read, and is listed in section {{n:36}}.",
        "",
        "Defaults in currency are the Brazil Edition ones, in reais (R$); the International",
        "Edition starts the costs and tariffs at zero, for the user to enter in the currency",
        "of the project.",
        "",
    ]
    for sec in G.ORDEM:
        if sec not in por_sec:
            continue
        grupo = por_sec[sec]
        nome = SECOES[sec]
        L += [f"## {nome}", "",
              f"{len(grupo)} parameter{'s' if len(grupo) != 1 else ''}.", "",
              f"<!-- tabela: Project parameters: {nome.lower()} -->",
              "| Parameter | Default | Unit | Where it is entered | Who consumes it |",
              "| :--- | ---: | :--- | :--- | :--- |"]
        for c in grupo:
            telas = ", ".join(sorted(_nome(t) for t in c["telas"])) or "—"
            mods = ", ".join(sorted(_nome(m) for m in c["mods"])) or "—"
            unidade = UNIDADES.get(c["u"], c["u"]) or "—"
            L.append(f"| `{c['n']}` | {padrao_em_ingles(c['cru'])} | {unidade} | {telas} | {mods} |")
        notas = [c for c in grupo if c["nota"]]
        if notas:
            L += ["", "Notes from the code:", ""]
            for c in notas:
                L.append(f"- `{c['n']}`: {NOTAS[c['n']][1]}")
        L.append("")
    return NL.join(L), len(campos)


def apendice_b():
    import processos_en as P
    PROCESSOS, FAMILIAS = P.PROCESSOS, P.FAMILIAS
    L = [
        "# The program's processes",
        "",
        f"There are **{len(PROCESSOS)} processes**, from the rainfall file to the report. Each",
        "one declares what triggers it, what it receives, the rules with their branches, what",
        "it produces and what happens when it fails.",
        "",
        "It is the most technical appendix of the manual, and it serves two people: whoever",
        "reviews a study made with the program and needs to know exactly which calculation was",
        "done, and whoever found a strange result and wants to know where the number went through.",
        "",
        "The names in `code` are the project file fields, listed in appendix {{n:A}}.",
        "",
    ]
    for pid, nome, fam, gatilho, entradas, regras, fns, saidas, excecao in PROCESSOS:
        rot = FAMILIAS[fam][0]
        L += [f"## {pid} — {nome}", "", f"*{rot}*", "",
              f"**Trigger.** {G._limpa(gatilho)}", "", "**Inputs**", ""]
        L += [f"- {G._limpa(e)}" for e in entradas]
        L += ["", "**Rules**", ""]
        L += [f"{i}. {G._limpa(r)}" for i, r in enumerate(regras, 1)]
        L += ["", "**Outputs**", ""]
        L += [f"- {G._limpa(s)}" for s in saidas]
        L += ["", f"**Exception.** {G._limpa(excecao)}", ""]
    return NL.join(L), len(PROCESSOS)


GRAUS = {
    "A — alta": "A — high", "B — boa": "B — good", "C — estrutura a conferir": "C — structure to be checked",
    "D — estrutura incompleta": "D — incomplete structure", "D — contradito por documento": "D — contradicted by a document", "não informado": "not stated",
}


TEXTOS_FAIXAS = dict(
    titulo="## The blocks by municipality and category",
    texto=[
        "The table below gives the price of water, in R$/m³, in each monthly consumption",
        "interval, for each structure of the catalogue. The columns are the finest split the",
        "catalogue needs: the union of the block limits of all providers, so that within each",
        "column no provider changes the price. Municipalities with the same table form one row,",
        "identified by the number in the first column, which repeats in the following parts.",
        "",
        "The residential category covers the 652 municipalities; the others appear where the",
        "provider's official table has been collected. The table is generated from the database",
        "for each version and grows with it. The fixed part adds on top of consumption; a zero",
        "price in the first blocks is the volume already included in the fixed value (allowance",
        "in the minimum).",
        "",
        "The colour of the row says how far the data can be trusted: **green** (🟢), audited",
        "against the primary source, the provider's resolution or official table; **yellow** (🟡),",
        "collected automatically or flagged for review, and so to be confirmed against the current",
        "resolution; **red** (🔴), incomplete structure, not to be used without correction.",
    ],
    data_texto="The second table gives, for the same rows, the effective date declared by the source and the date on which the official page was last checked by the database monitoring routine. A row without a date is a source the routine does not monitor yet. The effective dates are quoted as the sources state them, in Portuguese.",
    data_legenda="Effective date and last check of the source of each tariff structure, with the status of the data",
    data_cab=["No.", "Declared effective date", "Source checked on", "Status"],
    situacao_verde="audited", situacao_amarelo="to be confirmed", situacao_vermelho="incomplete structure",
    cob_texto="There are {0} municipalities and five categories, {1} combinations. The first table says, for each category, in how many municipalities the tariff table is audited, to be confirmed, incomplete or not yet collected; each municipality appears in full in the following tables, and the categories not yet collected are listed by provider at the end of the section.",
    cob_legenda="Coverage of the tariff catalogue: municipalities by category and status of the data",
    cob_cab=["Category", "🟢 audited", "🟡 to be confirmed", "🔴 incomplete", "🔴 not collected", "Municipalities"],
    falta_texto="The categories below do not yet have the provider's official table in the catalogue. In those municipalities the program does not offer them, and the way forward is to enter the table in Custom mode.",
    falta_legenda="Tariff categories not yet collected, by provider",
    falta_cab=["Provider: municipalities", "Categories not collected"],
    legenda_id="The tariff structures of the catalogue, numbered for the price-by-block tables that follow",
    legenda="Price of water by monthly consumption interval, in R$/m³, by municipality and category (part {0} of {1}: {2} to {3} m³)",
    n="No.", prestador="Provider: municipalities", categoria="Category", fixo="Fixed (R$/month)",
    esgoto="Sewage", e_mais=" and {0} more", retroativa="up to {0} m³: {1} (retroactive)",
    piso="floor {0}", esgoto_m3="R$ {0}/m³",
    cat_residencial="Residential", cat_comercial="Commercial", cat_publica="Public",
    cat_industrial="Industrial", cat_social="Social",
    exp_texto="The CORSAN municipalities charge by the exponential formula `PB × Cⁿ + SB` (section {{n:16}}), with no price per block; the exponent `n` is that of the category's column in the Exponent Table.",
    exp_legenda="The CORSAN exponential formula in each tariff table and collected category",
    exp_cab=["Municipalities", "Category", "PB (R$/m³)", "SB (R$/month)", "Sewage (R$/m³)"],
    conv_texto="Three providers charge the whole volume at the price of the block the consumption falls in (direct billing), and CESAN adds a fixed part that depends on the block of total consumption to a variable part in cascade. The program stores them as equivalent blocks of 1 m³ at the steps, which reproduce the bill for every whole cubic metre; the table shows the rule.",
    conv_legenda="The direct-billing and fixed-part-by-block structures",
    conv_cab=["Municipality", "Category", "Form", "Rule"],
    conv_direta="direct billing",
    conv_fixo_por_faixa="fixed part by block",
    conv_regra_direta="up to {0} m³, R$ {1}/month; above, the whole volume at R$ {2}–{3}/m³, by the price of the consumption",
    conv_regra_faixa="{0} m³: fixed R$ {1} + R$ {2}/m³",
)


def _num_en(v, casas):
    return f"{v:,.{casas}f}"


def apendice_d():
    caminho = os.path.join(RAIZ, "triton", "data", "brazil_cities_tariffs.json")
    if not os.path.exists(caminho):
        return None, 0
    cidades = json.load(open(caminho, encoding="utf-8"))["cities"]
    regimes = Counter(c.get("regime_tarifario") for c in cidades.values())
    NOMES_R = {
        "sem_minimo": ("No minimum", "Each m³ saved reduces the bill."),
        "disponibilidade": ("Availability charge",
                            "A fixed value that **adds** on top of the metered consumption. "
                            "Each m³ saved is deducted."),
        "franquia_no_minimo": ("Allowance in the minimum",
                               "The fixed value already includes a volume. Saving **below** "
                               "the allowance deducts nothing."),
        "franquia_retroativa": ("Retroactive allowance",
                                "Up to the allowance the fixed value is paid; beyond it, "
                                "**everything from zero** is charged."),
        "piso_de_pagamento": ("Payment floor",
                              "The bill does **not** go below the floor. It does not add: it bounds."),
        "exponencial": ("Exponential formula",
                        "Basic service plus `PB × Cⁿ`, with `n` set by the month's consumption "
                        "(CORSAN). Each m³ saved is deducted."),
    }
    L = [
        "# Tariff regimes",
        "",
        "> **Brazil Edition (BRL) only.** The tariff catalogue is Brazilian and ships only with the Brazil",
        "> Edition. In the International Edition the tariff is entered by the user, in one of",
        "> the same six regimes, and this appendix serves as a description of them.",
        "",
        f"The database holds **{len(cidades)} municipalities** with tariff structure, sewage",
        "percentage, minimum-charge regime, effective date and source. This list is extracted",
        "from the program's own database, not transcribed.",
        "",
        "## The block codes",
        "",
        "Each row of the tariff table is a quadruple `(minimum, maximum, value, code)`.",
        "",
        "The six codes and the effect of each on the bill are drawn in section {{n:29}}, and "
        "are not repeated here.",
        "",
        "",
        "## The six regimes",
        "",
        "<!-- tabela: Distribution of the catalogue municipalities across the six tariff regimes -->",
        "| Regime | Municipalities | What happens when saving |",
        "| :--- | ---: | :--- |",
    ]
    for chave, (nome, desc) in NOMES_R.items():
        L.append(f"| **{nome}** | {regimes.get(chave, 0)} | {desc} |")
    L += ["",
          "> The payment floor is implemented, and no municipality in the database had been",
          "> classified under it as of this version.",
          "",
          "## Distribution by state", "",
          "The catalogue coverage follows the population, not the territory: the state capitals "
          "and the metropolitan regions are almost all registered, and the interior of the North "
          "and Centre-West regions concentrates the municipalities still missing ({{fig:fig42_uf}}).", "",
          "![The catalogue municipalities, by state](../figuras/fig42_uf.png)",
          "",
          f"*Figure 99 — The distribution of the {len(cidades)} catalogued municipalities across the "
          "Brazilian states, with colours identifying the macro-region. São Paulo and Minas Gerais "
          "alone account for almost a third of the catalogue.*",
          "",
          "", "## Updating and auditing the database", "",
          "The tariff database is maintained by the group with an update routine run outside the "
          "interface, before each version. The routine has three components.", "",
          "**Electricity.** The residential tariffs of subgroup B1 are read from the open database of "
          "approved distributor tariffs published by the Brazilian Electricity Regulatory Agency "
          "(ANEEL), and associated with the distributor of each catalogue municipality.", "",
          "**Water and sewage.** A register of primary evidence associates each provider with the "
          "regulatory agency, the official tariff page and the type of act that publishes them. "
          "Providers with a standard portal are read automatically; the others are flagged for manual "
          "checking of the decree or resolution, and the resulting structure goes through the same "
          "regime validation described in this appendix.", "",
          "**Change detection.** Each monitored official page is recorded with the SHA-256 signature "
          "of its content and the `ETag` and `Last-Modified` headers. A new check compares the "
          "signatures and points out the pages changed since the last collection, which are the "
          "candidates for a tariff revision.", "",
          "The routine can simulate the update without writing the database, run only the change "
          "detection, restrict itself to one state or one municipality, and separate electricity from "
          "sanitation. Each run writes an audit report in Markdown and an HTML panel with the status "
          "of each municipality.",
          "", "## Confidence grade", "",
          "Each record carries the confidence grade of the collection:", "",
          "<!-- tabela: Confidence grade of the tariff records in the catalogue -->",
          "| Grade | Records |", "| :--- | ---: |"]
    conf = Counter(c.get("confianca_grau", "não informado") for c in cidades.values())
    for grau, n in conf.most_common():
        if grau not in GRAUS:
            raise SystemExit(f"apêndice D em inglês: falta traduzir o grau «{grau}»")
        L.append(f"| {GRAUS[grau]} | {n} |")
    L += ["",
          "> **Always check the effective date** of your municipality's record against the",
          "> utility's resolution. Tariffs are adjusted every year, and section {{n:16}}",
          "> teaches the test that identifies a wrong structure.", ""]
    from tabela_de_faixas import secao
    L += secao(cidades, TEXTOS_FAIXAS, _num_en)
    return NL.join(L), len(cidades)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    for nome, funcao in (("A_parametros.md", apendice_a), ("B_processos.md", apendice_b),
                         ("D_regimes_tarifarios.md", apendice_d)):
        texto, n = funcao()
        if texto is None:
            print(f"  {nome} — skipped: source not found")
            continue
        gravar(os.path.join(SAIDA, nome), texto + NL)
        print(f"  {nome} — {n}")


if __name__ == "__main__":
    print("appendices of the English manual:")
    main()
