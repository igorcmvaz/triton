# -*- coding: utf-8 -*-
"""Generates appendices A, B and D of the English manual from the source.

The same data as the Portuguese appendices (manual/gerar_apendices.py), with English
labels. A label or a code note without a translation stops the generation and names
what is missing: a new parameter added to `TritonConfig` cannot reach the English manual
in Portuguese.

The International Edition is neutral: the defaults printed in appendix A are those of the
edition's own starting project (`configuracao_da_edicao()` with `TRITON_EDITION=INT`), and the
fields that exist only for the national schemes of other editions are left out and counted.
Appendix D describes the six tariff regimes and the three example tariffs the edition ships;
it reads no tariff catalogue.

Output: manual/en/apendices/A_parametros.md, B_processos.md, D_regimes_tarifarios.md
"""

from __future__ import annotations

import os
import sys

os.environ["TRITON_EDITION"] = "INT"

AQUI = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.dirname(AQUI)
RAIZ = os.path.dirname(MANUAL)
for _p in (MANUAL, AQUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
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
    "% da água": "% of water", "R$/mês": "currency/month", "R$/ano": "currency/year",
    "R$": "currency", "R$/kg": "currency/kg", "R$/kWh": "currency/kWh",
    "% por período": "% per period", "meses": "months", "mês": "month",
    "L/pessoa·dia": "L/person·day", "m.c.a.": "m head",
}

PADROES = {"Novo projeto Triton": "New Triton project", "CUSTOM": "custom"}

#: Fields stored in the project file for the national schemes of other editions (a regional
#: property-tax incentive and a regional electricity-tariff flag). They have no effect here and
#: are not listed; appendix A says how many there are.
FORA_DESTA_EDICAO = ("tariff_flag", "iptu_green_enabled", "iptu_annual_value", "iptu_discount_pct")

#: Defaults the starting project of the edition still carries from the shared code and that name
#: a product of another market; printed as unset.
PADRAO_NAO_DEFINIDO = {"pressurizer_model": "—"}

#: The code notes of `TritonConfig`, translated. The key is the field name, and the
#: Portuguese note is kept beside it: when the note changes in the code, the English
#: one is refused until it is reviewed.
NOTAS = {
    "climate_source_mode": ('"national_db" (base nacional) ou "custom_file" (arquivo próprio)',
                            '"custom_file" (own file): in this edition the rainfall series always comes from a file of the user'),
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
    "chlorine_cost_per_kg": ("R$ por kg de PRODUTO comercial", "price per kg of commercial PRODUCT, in the currency of the project"),
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
                       "price of one pump set, in the currency of the project (zero until you enter it)"),
    "sewage_mode": ("0 = valor fixo em R$, 1 = percentual da parcela de água, 2 = R$/m³ consumido, 3 = escalões",
                    "0 = fixed amount, 1 = percentage of the water part, 2 = amount per m³ consumed, 3 = tiers"),
    "water_tax_fixed": ("R$", "currency per month"),
    "water_tax_var": ("%", "%"),
    "tariff_escalation": ("meses; comprimento do período de reajuste", "months; length of the escalation period"),
    "water_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                "% per escalation period; with 12 months, % per year"),
    "sewage_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                 "% per escalation period; with 12 months, % per year"),
    "elec_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                               "% per escalation period; with 12 months, % per year"),
    "elec_tariff": ("R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)",
                    "price of electricity per kWh, in the currency of the project (zero until you enter it)"),
    "elec_tax_fixed": ("R$", "currency per month"),
    "elec_tax_var": ("%", "%"),
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


def _padrao_da_edicao():
    """Starting value of each field in this edition: the project the program opens with."""
    from triton.core.edition import configuracao_da_edicao
    return configuracao_da_edicao()


def apendice_a():
    todos = G.campos_do_projeto()
    campos = [c for c in todos if c["n"] not in FORA_DESTA_EDICAO]
    fora = len(todos) - len(campos)
    inicial = _padrao_da_edicao()
    for c in campos:
        if c["n"] in PADRAO_NAO_DEFINIDO:
            c["cru"] = PADRAO_NAO_DEFINIDO[c["n"]]
        elif c["cru"] is not None and hasattr(inicial, c["n"]):
            c["cru"] = getattr(inicial, c["n"])
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
        "stores in this edition, with the exact name of each field inside the `.triton` file.",
        "",
        "The list was not transcribed by hand: it is extracted from the program itself for",
        "each version, and therefore cannot diverge from it.",
        "",
        "The column **where it is entered** says on which screen the field appears; the",
        "column **who consumes it** says which calculation uses it. A field with neither is a",
        "field stored in the file and never read, and is listed in section {{n:36}}.",
        "",
        "The defaults are those of the project the International Edition opens with. Costs, prices,",
        "tariffs and the rainfall series start empty or at zero: you enter them, in the currency",
        "of the project, and the program never assumes a currency. A dash means that the field",
        "has no starting value.",
        "",
    ]
    if fora:
        L += [f"The project file also holds {fora} fields that belong to national schemes of other",
              "editions. They have no effect in this one and are not listed.", ""]
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


REGIMES = [
    ("No minimum", "Progressive blocks only.", "Each m³ saved reduces the bill."),
    ("Availability charge", "A fixed value that **adds** on top of the metered consumption.",
     "Each m³ saved reduces the bill; the fixed part remains."),
    ("Allowance in the minimum", "The fixed value already includes a volume.",
     "Saving **below** the allowance deducts nothing."),
    ("Retroactive allowance", "Up to the allowance the fixed value is paid; beyond it, "
     "**everything from zero** is charged by the blocks.",
     "Going past the allowance, the whole volume is billed from zero."),
    ("Payment floor", "The bill does **not** go below the floor.",
     "It does not add: it bounds. Savings that bring the bill under the floor earn nothing."),
    ("Exponential formula", "Basic service plus `PB × Cⁿ`, with the exponent `n` set by the "
     "consumption of the month.", "Each m³ saved reduces the bill, but not at a fixed price per m³."),
]


def _moeda(v):
    return f"{v:,.4f}".rstrip("0").rstrip(".") if v != int(v) else f"{int(v):,}"


def _exemplos():
    """The three example tariffs of the edition, as the example projects enter them."""
    sys.path.insert(0, os.path.join(RAIZ, "scripts"))
    import gerar_exemplos_int as E
    return [f() for f in E.CIDADES]


def _tabela_do_exemplo(ex):
    c = ex["campos"]
    agua = c["water_tariffs"]
    L = ["| Part | From (m³/month) | To (m³/month) | Value | Code |", "| :--- | ---: | ---: | ---: | ---: |"]
    for ini, fim, val, cod in agua:
        fim_t = "open" if fim >= 999999 else _moeda(fim)
        L.append(f"| water | {_moeda(ini)} | {fim_t} | {_moeda(val)} | {cod} |")
    modo = c["sewage_mode"]
    if modo == 1:
        L.append(f"| sewage | — | — | {_moeda(c['sewage_rate'])}% of the water part | — |")
    elif modo == 2:
        L.append(f"| sewage | — | — | {_moeda(c['sewage_rate'])} per m³ | — |")
    else:
        for ini, fim, val in c["sewage_tariffs"]:
            L.append(f"| sewage (on {c['sewage_volume_factor']:.0%} of the water volume) | {_moeda(ini)} | {_moeda(fim)} | {_moeda(val)} | — |")
    if c["water_tax_fixed"]:
        L.append(f"| fixed amount, per month | — | — | {_moeda(c['water_tax_fixed'])} | — |")
    return L


def apendice_d():
    L = [
        "# Tariff regimes",
        "",
        "The International Edition ships **no tariff catalogue**. You enter the water and sewage",
        "tariff of the project, in the currency you choose, and the program calculates the bill",
        "with and without the harvesting system. This appendix describes the structure the",
        "program accepts, the six regimes it recognises, and the three example tariffs that come",
        "with the edition.",
        "",
        "## The block codes",
        "",
        "Each row of the water tariff table is a quadruple `(minimum, maximum, value, code)`, in",
        "m³ per month and currency per m³ (or currency per month for the fixed codes).",
        "",
        "<!-- tabela: The block codes of the water tariff table -->",
        "| Code | Meaning |",
        "| ---: | :--- |",
        "| 1 or 0 | progressive block: charged only on the volume inside it |",
        "| −1 | availability charge: a fixed value per month that adds to the metered consumption |",
        "| −2 | retroactive allowance: up to the allowance the fixed value is paid; beyond it, all the volume from zero is charged by the blocks |",
        "| −3 | payment floor: the bill is not allowed to fall below the value |",
        "",
        "The effect of each code on the bill is drawn in section {{n:29}}, and is not repeated here.",
        "",
        "## The sewage part",
        "",
        "<!-- tabela: The four ways of entering the sewage charge -->",
        "| Mode | The sewage charge is |",
        "| ---: | :--- |",
        "| 0 | a fixed amount |",
        "| 1 | a percentage of the water part (not of the whole bill) |",
        "| 2 | an amount per m³ consumed |",
        "| 3 | blocks (steps), applied to a fraction of the water volume that you declare |",
        "",
        "Fixed and variable taxes can be added to the water part and to the electricity part. Tariff",
        "escalation is entered separately for water, sewage and energy (appendix {{n:A}}).",
        "",
        "## The six regimes",
        "",
        "The program classifies a water tariff table into one of six regimes. The regime tells you",
        "what saving water is worth, which is what a rainwater harvesting study needs to see.",
        "",
        "<!-- tabela: The six tariff regimes and what happens when saving -->",
        "| Regime | Structure | What happens when saving |",
        "| :--- | :--- | :--- |",
    ]
    for nome, estrutura, efeito in REGIMES:
        L.append(f"| **{nome}** | {estrutura} | {efeito} |")
    L += ["",
          "**Quick test.** Simulate two consumptions, one inside and one outside the minimum block, and",
          "compare them with a real bill. If only one matches, the regime is wrong. Section {{n:16}}",
          "teaches the test that identifies a wrong structure.",
          "",
          "## The example tariffs that come with the edition",
          "",
          "Three example projects (`examples/new_york.triton`, `london.triton` and `cape_town.triton`)",
          "carry the water and sewage tariff of their city, as published by the utility and entered by",
          "the maintainers on 14/10/2026. They are examples of how to enter a tariff, not a catalogue:",
          "tariffs change every year, and you must check the current document of your utility before",
          "any economic conclusion. The document address and file signature of each source have not",
          "been recorded yet, so each value below is to be confirmed against the utility's current tariff.",
          ""]
    for ex in _exemplos():
        L += [f"### {ex['cidade']}: {ex['entidade']}", "",
              f"Currency {ex['moeda']}; effective {ex['vigencia']} (as stated by the maintainers; confirm).", "",
              ex["fonte"], "",
              f"<!-- tabela: Tariff structure of the {ex['cidade']} example -->"]
        L += _tabela_do_exemplo(ex)
        L += ["", "Assumptions made when entering it:", ""]
        L += [f"- {h}" for h in ex["hipoteses"]]
        L.append("")
    L += ["## Entering your own tariff", "",
          "1. Take the current tariff document of your water utility and write down its date.",
          "2. Enter the blocks, the fixed charges and the sewage rule in the tariff dialog (stage 5).",
          "3. Check the bill the program calculates against a real bill of the building.",
          "4. Declare in the study the utility, the effective date, the regime and the currency.",
          ""]
    return NL.join(L), 3


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
