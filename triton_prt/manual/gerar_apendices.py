# -*- coding: utf-8 -*-
"""Gera os apêndices A, B e D do manual da Edição Portugal (PRT), em português europeu.

Os apêndices A (parâmetros) e B (processos) saem do código: `TritonConfig` e a matriz de
processos de `processos.py`. Transcrever isso à mão significa divergir do programa no dia
seguinte à publicação. O apêndice D lê os tarifários transcritos em
`triton/data/portugal_tarifarios.json`.

A edição é a Portugal: os padrões impressos no apêndice A são os do projeto com que a
edição abre (`configuracao_da_edicao()` com `TRITON_EDITION=PRT`), e os campos que existem
só para esquemas nacionais de outras edições ficam de fora e são contados.

Saída: manual/apendices/A_parametros.md, B_processos.md e D_regimes_tarifarios.md
"""

from __future__ import annotations

import ast
import os

os.environ["TRITON_EDITION"] = "PRT"

from escrita_segura import gravar  # não desfaz revisão feita à mão
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
for _p in (BASE, AQUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)
PKG = os.path.join(BASE, "triton")
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

#: Telas que a janela principal nunca abre. Ficam fora do apêndice para que ele não
#: cite tela inexistente. As últimas, `tab_single_sim.py`, `tab_economic.py` e
#: `tab_reports.py`, foram removidas em 18/09/2026; a tupla fica para a asserção abaixo.
TELAS_ORFAS = ()

TELAS = {
    "tab_project.py": "Projeto", "tab_building.py": "Edificação",
    "tab_water_quality.py": "Qualidade",
    "tab_tanks_simulation.py": "Varredura",
    "tab_economic_integrated.py": "Econômico",
    "tab_economic_global_optimizer.py": "Otimizador", "tab_environmental.py": "Ambiental",
    "tab_tariffs_manager.py": "Tarifas",
    "tab_reports_pdf.py": "Relatórios",
    "tab_charts_triton.py": "Gráficos", "tab_export.py": "Exportação",
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
    ("first_flush", "Captação"),
    ("irrigation", "Irrigação"),
    ("chlorine", "Qualidade da água"), ("water_quality", "Qualidade da água"),
    ("etap", "Qualidade da água"),
    ("pump", "Motobomba"), ("pressurizer", "Motobomba"), ("supply_arrangement", "Motobomba"),
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
    "pressurizer_pressure_m": "m.c.a.", "pressurizer_starts_per_person_day": "1/pessoa·dia",
    "pressurizer_model": "código", "pressurizer_point_flow_l_min": "L/min",
    "pressurizer_power_kw": "kW", "pressurizer_flow_l_min": "L/min",
    "pressurizer_post_run_s": "s", "supply_arrangement": "código",
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
    "chlorine_co2_kg_per_kg": "kg CO₂e/kg", "tma": "% ao mês", "inflation": "% ao mês",
    "analysis_period_years": "anos", "sewage_rate": "% da água",
    "water_tax_fixed": "R$/mês", "water_tax_var": "%", "elec_tariff": "R$/kWh",
    "elec_tax_fixed": "R$/mês", "elec_tax_var": "%", "iptu_annual_value": "R$/ano",
    "iptu_discount_pct": "%", "cost_lower_tank": "R$", "cost_upper_tank": "R$",
    "cost_labor": "R$", "cost_piping": "R$", "cost_accessories": "R$",
    "water_tariff_escalation": "% por período", "sewage_tariff_escalation": "% por período",
    "elec_tariff_escalation": "% por período", "tariff_escalation": "meses",
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


def campos_do_projeto():
    """Os campos de `TritonConfig`, com o padrão cru, a nota do código e onde cada um aparece.

    Os nomes de seção, de tela e de módulo saem em português; o manual em inglês os
    traduz em `manual/en/apendices_en.py`.
    """
    src = open(os.path.join(PKG, "core", "parser.py"), encoding="utf-8").read()
    linhas_fonte = src.split(NL)
    arv = ast.parse(src)
    FONTES = fontes()

    campos = []
    for no in ast.walk(arv):
        if isinstance(no, ast.ClassDef) and no.name == "TritonConfig":
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
                    "n": nome, "cru": padrao, "u": UNIDADES.get(nome, ""),
                    "nota": nota, "sec": secao(nome),
                    "mods": sorted(mods - {"Arquivo do projeto"}),
                    "telas": sorted(telas),
                })
    return campos


def _limpa(t):
    t = re.sub(r"<code>(.*?)</code>", r"`\1`", t)
    t = re.sub(r"<b>(.*?)</b>", r"**\1**", t)
    t = re.sub(r"<i>(.*?)</i>", r"*\1*", t)
    t = t.replace("&rarr;", "→").replace("&nbsp;", " ").replace("&mdash;", "—")
    t = re.sub(r"<[^>]+>", "", t)
    return t



#: Seções, ecrãs e módulos, como o apêndice A os nomeia em português europeu.
SECOES_PT = {
    "Identificação": "Identificação", "Chuva": "Chuva", "Captação": "Captação",
    "Edificação": "Edificação", "Demanda": "Procura", "Irrigação": "Rega",
    "Qualidade da água": "Qualidade da água", "Reservatórios": "Reservatórios",
    "Motobomba": "Eletrobomba", "Tubulação": "Tubagem", "Investimento": "Investimento",
    "Operação": "Exploração", "Tarifas": "Tarifário", "Energia": "Energia",
    "Incentivos": "Incentivos", "Financeiro": "Financeiro", "Certificações": "Certificações",
    "Outros": "Outros",
}

NOMES = {
    "ACV": "ACV", "Ambiental": "Ambiental", "Assistente da bomba": "Assistente da bomba",
    "Automação": "Automação", "Balanço diário": "Balanço diário", "CAD e BIM": "CAD e BIM",
    "Caixa superior": "Reservatório superior", "Cenários": "Cenários", "Clima": "Clima",
    "Documentação": "Documentação", "ETAP": "ETAP", "Econômico": "Económico",
    "Edificação": "Edificação", "Exportação": "Exportação", "Gráficos": "Gráficos",
    "Janela principal": "Janela principal", "Motobomba": "Eletrobomba",
    "Multicritério": "Multicritério", "Otimizador": "Otimizador",
    "Planilhas": "Folhas de cálculo", "Preços": "Preços", "Projeto": "Projeto",
    "Qualidade": "Qualidade", "Relatórios": "Relatórios", "Tarifas": "Tarifário",
    "Tarifas e custos": "Tarifário e custos", "Varredura": "Varrimento",
    "Certificações": "Certificações", "Índices de chuva": "Índices de chuva",
    "Valores mensais": "Valores mensais", "Entrada variável": "Entrada variável",
    "Validação": "Validação",
}

UNIDADES = {
    "1/pessoa·dia": "1/pessoa·dia", "código": "código", "dias": "dias", "%/m³": "%/m³",
    "un": "un", "L/dia": "L/dia", "hab": "residentes", "fração": "fração",
    "L/m²·dia": "L/m²·dia", "mm/dia": "mm/dia", "% ao mês": "% por mês", "anos": "anos",
    "% da água": "% da água", "R$/mês": "€/mês", "R$/ano": "€/ano", "R$": "€",
    "R$/kg": "€/kg", "R$/kWh": "€/kWh", "% por período": "% por período",
    "meses": "meses", "mês": "mês", "L/pessoa·dia": "L/pessoa·dia", "m.c.a.": "m c.a.",
}

#: Campos do ficheiro de projeto que servem a esquemas nacionais de outras edições (a bandeira
#: tarifária da eletricidade e o incentivo fiscal predial de um município de outra edição). Não
#: têm efeito nesta e não são listados; o apêndice A diz quantos são.
FORA_DESTA_EDICAO = ("tariff_flag", "iptu_green_enabled", "iptu_annual_value", "iptu_discount_pct")

#: Padrões que o projeto inicial da edição ainda herda do código comum e que nomeiam um produto
#: de outro mercado; saem como «—».
PADRAO_NAO_DEFINIDO = {"pressurizer_model": "—"}

PADROES = {"Novo projeto Triton": "Novo projeto Triton", "CUSTOM": "personalizado",
           "constant": "constant"}

#: As observações do código em `TritonConfig`, em português europeu. A chave é o campo; a nota
#: original fica ao lado: quando a nota muda no código, a tradução é recusada até ser revista.
NOTAS = {
    "climate_source_mode": ('"national_db" (base nacional) ou "custom_file" (arquivo próprio)',
                            '"national_db" (a base E-OBS por concelho) ou "custom_file" (ficheiro do utilizador)'),
    "discard": ("mm", "mm"),
    "discard_mode": ("1 = todos os eventos, 2 = 1º evento após estiagem, 3 = a cada X dias",
                     "1 = todos os eventos, 2 = 1.º evento após período seco, 3 = a cada X dias"),
    "discard_days_interval": ("intervalo para modo 3", "intervalo para o modo 3"),
    "area": ("m²", "m²"),
    "irrigation_garden_area_m2": ("Área de jardim em m² para o assistente de dimensionamento",
                                  "Área de jardim em m² para o assistente de dimensionamento"),
    "runoff_coeff": ("ver hydrology_defaults", "ver hydrology_defaults"),
    "num_economias": ("Número de economias / apartamentos com micromedição individual",
                      "Número de frações autónomas com contador individual"),
    "demand_mode": ('"constant", "weekly", "monthly", "daily"', '"constant", "weekly", "monthly", "daily"'),
    "demand_value": ("L/dia, por habitante ou total", "L/dia, por residente ou total"),
    "potable_indoor_share": ("Fração potável do consumo interno; 1 − non_potable_indoor_share",
                             "Fração potável do consumo interior; 1 − non_potable_indoor_share"),
    "non_potable_indoor_share": ("Fração não potável do consumo interno (bacias, máquina); ver fracao_atendivel",
                                 "Fração não potável do consumo interior (autoclismos, máquina de lavar); ver fracao_atendivel"),
    "rainwater_share": ("fração de 0 a 1 (0,4 = 40%)", "fração de 0 a 1 (0,4 = 40%)"),
    "irrigation_liters_per_day": ("Demanda externa (rega, lavagem de áreas externas), L/dia",
                                  "Procura exterior (rega, lavagem de zonas exteriores), L/dia"),
    "irrigation_rain_threshold_mm": ("Limiar diário de precipitação para supressão da irrigação (mm/dia)",
                                     "Limiar diário de precipitação para suspender a rega (mm/dia)"),
    "irrigation_potable_backup": ("Se True, a rede pública atende a irrigação em dias secos se a cisterna secar",
                                  "Se True, a rede pública abastece a rega em dias secos se a cisterna secar"),
    "irrigation_rate_l_m2_day": ("Taxa diária de rega (L/m²/dia)", "Taxa diária de rega (L/m²/dia)"),
    "water_quality_disinfection": ('"cloro", "uv", "ozonio", "nenhum"',
                                   '"cloro", "uv", "ozonio" (ozono), "nenhum"'),
    "chlorine_dose_mg_l": ("mg de Cl2 ativo por litro", "mg de Cl2 ativo por litro"),
    "chlorine_product_purity": ("kg Cl2 ativo por kg de produto", "kg de Cl2 ativo por kg de produto"),
    "chlorine_cost_per_kg": ("R$ por kg de PRODUTO comercial", "€ por kg de PRODUTO comercial"),
    "upper_tank_vol": ("L", "L"),
    "upper_tank_used": ("0 = sem caixa superior, 1 = com caixa superior",
                        "0 = sem reservatório superior, 1 = com reservatório superior"),
    "lower_tank_max": ("L", "L"),
    "lower_tank_step": ("L", "L"),
    "lower_tank_mode": ("0 = volume fixo, 1 = varredura", "0 = volume fixo, 1 = varrimento"),
    "lower_tank_fixed": ("usado no modo de volume fixo", "usado no modo de volume fixo"),
    "delta_ideal": ("limiar de ganho marginal para o volume ideal, em %/m³",
                    "limiar de ganho marginal para o volume ideal, em %/m³"),
    "lower_tank_material": ('"PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"',
                            '"PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)'),
    "upper_tank_material": ('"PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"',
                            '"PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)'),
    "pumping_threshold": ("L, nível de acionamento do recalque", "L, nível de acionamento da elevação"),
    "pump_count": ("principal + reserva como configuração inicial recomendada",
                   "principal + reserva como configuração inicial recomendada"),
    "pump_power_kw": ("kW (1 CV = 0,7355 kW; 1/2 CV = 0,36775 kW)", "kW (1 cv = 0,7355 kW; 1/2 cv = 0,36775 kW)"),
    "pump_efficiency": ("%, 0 = deduzir do porte", "%, 0 = deduzir da potência"),
    "pump_startup_time_h": ("h", "h"),
    "pump_motor_efficiency": ("%", "%"),
    "pump_unit_cost": ("R$, referência de mercado para motobomba periférica 1/2 CV",
                       "preço de uma eletrobomba, em euros (zero até o utilizador o introduzir)"),
    "sewage_mode": ("0 = valor fixo em R$, 1 = percentual da parcela de água, 2 = R$/m³ consumido, 3 = escalões",
                    "0 = valor fixo em €, 1 = percentagem da parcela de água, 2 = €/m³ consumido, 3 = escalões"),
    "water_tax_fixed": ("R$", "€ por mês"),
    "water_tax_var": ("%", "% (o IVA da água, nas faturas portuguesas)"),
    "tariff_escalation": ("meses; comprimento do período de reajuste", "meses; duração do período de atualização"),
    "water_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                "% por período de atualização; com 12 meses, % por ano"),
    "sewage_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                                 "% por período de atualização; com 12 meses, % por ano"),
    "elec_tariff_escalation": ("% por período de reajuste; com 12 meses, % ao ano",
                               "% por período de atualização; com 12 meses, % por ano"),
    "elec_tariff": ("R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)",
                    "preço da eletricidade por kWh, em euros (zero até o utilizador o introduzir)"),
    "elec_tax_fixed": ("R$", "€ por mês"),
    "elec_tax_var": ("%", "%"),
    "inflation": ("% ao mês; inflação dos custos de O&M", "% por mês; inflação dos custos de exploração e manutenção"),
    "analysis_period_years": ("anos", "anos"),
    "tariff_category": ('categoria da tabela tarifária aplicada; "personalizada" quando digitada',
                        'categoria da tabela tarifária aplicada; "personalizada" quando introduzida pelo utilizador'),
    "tma": ("% ao mês; taxa mínima de atratividade", "% por mês; taxa de atualização"),
}


def _nome(rotulo):
    if rotulo not in NOMES:
        raise SystemExit(f"apêndice A: falta nomear o rótulo «{rotulo}» em NOMES")
    return NOMES[rotulo]


def padrao_em_portugues(padrao):
    if isinstance(padrao, (list, tuple)):
        return "vazio" if not padrao else f"{len(padrao)} itens"
    if isinstance(padrao, bool):
        return "sim" if padrao else "não"
    if isinstance(padrao, float):
        return f"{padrao:g}".replace(".", ",")
    if padrao is None or padrao == "":
        return "—"
    return PADROES.get(str(padrao), str(padrao))


def apendice_a():
    from triton.core.edition import configuracao_da_edicao
    todos = campos_do_projeto()
    campos = [c for c in todos if c["n"] not in FORA_DESTA_EDICAO]
    fora = len(todos) - len(campos)
    inicial = configuracao_da_edicao()
    for c in campos:
        if c["n"] in PADRAO_NAO_DEFINIDO:
            c["cru"] = PADRAO_NAO_DEFINIDO[c["n"]]
        elif c["cru"] is not None and hasattr(inicial, c["n"]):
            c["cru"] = getattr(inicial, c["n"])
        c["p"] = padrao_em_portugues(c["cru"])
    faltam = []
    for c in campos:
        if c["nota"]:
            par = NOTAS.get(c["n"])
            if par is None or par[0] != c["nota"]:
                faltam.append(f"{c['n']}: {c['nota']}")
    if faltam:
        raise SystemExit("apêndice A: nota do código sem tradução revista em NOTAS:" + NL
                         + NL.join("  " + f for f in faltam))

    por_sec = {}
    for c in campos:
        por_sec.setdefault(c["sec"], []).append(c)

    L = [
        "# Os parâmetros do projeto",
        "",
        f"São **{len(campos)} parâmetros**. É a lista completa do que um projeto guarda nesta",
        "edição, com o nome exato de cada campo dentro do ficheiro `.triton`.",
        "",
        "A lista não foi transcrita à mão: é extraída do próprio programa a cada versão, e por",
        "isso não pode divergir dele.",
        "",
        "A coluna **onde se introduz** diz em que ecrã o campo aparece; a coluna **quem consome**",
        "diz que cálculo o usa. Um campo sem nenhuma das duas é um campo gravado no ficheiro e",
        "nunca lido, e está listado na secção {{n:36}}.",
        "",
        "Os padrões são os do projeto com que a Edição Portugal abre: a chuva é a normal 1991-2020",
        "do concelho de Lisboa na base E-OBS, e os custos, os preços e a tarifa de eletricidade",
        "partem de zero ou vazios, para o utilizador os introduzir em euros. Um traço significa",
        "que o campo não tem valor inicial.",
        "",
    ]
    if fora:
        L += [f"O ficheiro de projeto guarda ainda {fora} campos de esquemas nacionais de outras",
              "edições. Não têm efeito nesta e não são listados.", ""]
    for sec in ORDEM:
        if sec not in por_sec:
            continue
        grupo = por_sec[sec]
        nome = SECOES_PT[sec]
        L += [f"## {nome}", "",
              f"{len(grupo)} parâmetro{'s' if len(grupo) != 1 else ''}.", "",
              f"<!-- tabela: Parâmetros do projeto: {nome.lower()} -->",
              "| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |",
              "| :--- | ---: | :--- | :--- | :--- |"]
        for c in grupo:
            telas = ", ".join(sorted(_nome(t) for t in c["telas"])) or "—"
            mods = ", ".join(sorted(_nome(m) for m in c["mods"])) or "—"
            unidade = UNIDADES.get(c["u"], c["u"]) or "—"
            L.append(f"| `{c['n']}` | {c['p']} | {unidade} | {telas} | {mods} |")
        notas = [c for c in grupo if c["nota"]]
        if notas:
            L += ["", "Observações do código:", ""]
            for c in notas:
                L.append(f"- `{c['n']}`: {NOTAS[c['n']][1]}")
        L.append("")
    return NL.join(L), len(campos)


def apendice_b():
    caminho = os.path.join(AQUI, "processos.py")
    if not os.path.exists(caminho):
        return None, 0
    espaco = {}
    exec(compile(open(caminho, encoding="utf-8").read(), caminho, "exec"), espaco)
    PROCESSOS = espaco["PROCESSOS"]
    FAMILIAS = espaco["FAMILIAS"]

    L = [
        "# Os processos do programa",
        "",
        f"São **{len(PROCESSOS)} processos**, do ficheiro de chuva ao relatório. Cada um declara o",
        "que o desencadeia, o que recebe, as regras com as suas ramificações, o que produz e o",
        "que acontece quando falha.",
        "",
        "É o apêndice mais técnico do manual, e serve a duas pessoas: quem revê um estudo feito",
        "com o programa e precisa de saber exatamente que conta foi feita, e quem encontrou um",
        "resultado estranho e quer saber por onde o número passou.",
        "",
        "Os nomes em `código` são os campos do ficheiro de projeto, listados no apêndice {{n:A}}.",
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
        # instala um executável, e nome de função só ajuda a quem tem o código-fonte.
        L += ["", f"**Exceção.** {_limpa(excecao)}", ""]
    return NL.join(L), len(PROCESSOS)


# ── apêndice D ───────────────────────────────────────────────────────────────

NBSP = " "
ARTIGO = {"Funchal": "do Funchal", "Porto": "do Porto"}


def _num(v, casas=None):
    """Número em português de Portugal: vírgula decimal e espaço inseparável nos milhares."""
    if casas is None:
        texto = f"{v:.4f}".rstrip("0").rstrip(".")
        if "." not in texto and float(v) != int(v):
            texto = f"{v}"
    else:
        texto = f"{v:.{casas}f}"
    inteiro, _, dec = texto.partition(".")
    sinal = "−" if inteiro.startswith("-") else ""
    inteiro = inteiro.lstrip("-")
    if len(inteiro) > 4:
        inteiro = f"{int(inteiro):,}".replace(",", NBSP)
    return sinal + inteiro + ("," + dec if dec else "")


def _preco(v):
    return _num(v, 4) if round(v, 4) != round(v, 2) else _num(v, 2)


def _eur(v, casas=None):
    return f"{_num(v, casas)}{NBSP}€"


REGIMES = [
    ("Sem mínimo", "Só escalões progressivos.", "Cada m³ poupado reduz a fatura."),
    ("Tarifa de disponibilidade", "Um valor fixo que **soma** ao consumo medido.",
     "Cada m³ poupado reduz a fatura; a parte fixa mantém-se. É a estrutura dos três tarifários transcritos."),
    ("Franquia no mínimo", "O valor fixo já inclui um volume.",
     "Poupar **abaixo** da franquia não desconta nada."),
    ("Franquia retroativa", "Até à franquia paga-se o valor fixo; passando-a, "
     "**tudo desde zero** é cobrado pelos escalões.",
     "Ao passar a franquia, todo o volume é faturado desde zero."),
    ("Piso de pagamento", "A fatura **não fica** abaixo do piso.",
     "Não soma: limita. A poupança que leve a fatura abaixo do piso não rende nada."),
    ("Fórmula exponencial", "Serviço básico mais `PB × Cⁿ`, com o expoente `n` dado pelo consumo do mês.",
     "Cada m³ poupado reduz a fatura, mas não a um preço fixo por m³."),
]

#: Concelhos cujos documentos tarifários foram recolhidos e ainda não foram transcritos
#: (tarifas_portugal/LEIA.md). O programa não os oferece.
RECOLHIDOS = [
    ("Coimbra", "Águas de Coimbra", "editais n.º 433 e 438/2025"),
    ("Braga", "AGERE", "tarifário de fevereiro de 2026"),
    ("Setúbal", "SMS Setúbal", "água, saneamento e resíduos 2026"),
    ("Leiria", "SMAS Leiria", "tarifário 2026"),
    ("Faro", "FAGAR", "tarifário 2026"),
    ("Aveiro", "AdRA", "tarifário 2026"),
    ("Viseu", "Águas de Viseu", "tarifários de abril de 2026"),
    ("Beja", "EMAS Beja", "tarifário 2025"),
    ("Évora", "Câmara Municipal de Évora", "tarifário 2025"),
    ("Castelo Branco", "SM Castelo Branco", "tarifário em vigor (publicado em 24/02/2026)"),
    ("Santarém", "Águas de Santarém", "tarifários geral e do saneamento 2026"),
    ("Ponta Delgada", "SMAS Ponta Delgada", "tarifário 2026"),
    ("Viana do Castelo", "Águas do Alto Minho", "cartaz do tarifário 2026"),
    ("Portalegre", "SMAT Portalegre", "edital 2026"),
    ("Guarda", "Câmara Municipal da Guarda", "edital n.º 16/2026"),
    ("Vila Real", "ADIN e Câmara Municipal", "tarifas 2026 e resíduos 2026"),
]


def _fontes_registadas():
    """{caminho relativo: (endereço, SHA-256, data da recolha)} de tarifas_portugal/fontes/FONTES.tsv."""
    caminho = os.path.join(BASE, "tarifas_portugal", "fontes", "FONTES.tsv")
    out = {}
    if not os.path.exists(caminho):
        return out
    for linha in open(caminho, encoding="utf-8"):
        partes = linha.rstrip("\n").split("\t")
        if len(partes) >= 4:
            out[partes[0]] = (partes[1], partes[2], partes[3])
    return out


def _caminho_da_fonte(texto):
    m = re.search(r"tarifas_portugal/fontes/([^)\s]+)", texto)
    return m.group(1) if m else None


def _tabela_de_escaloes(servico, rotulo, coef=None):
    L = []
    esc = servico["escaloes"]
    L += ["| Parte | De (m³/mês) | Até (m³/mês) | Preço (€/m³, sem IVA) |",
          "| :--- | ---: | ---: | ---: |"]
    for a, b, p in esc:
        fim = "sem limite" if b is None else _num(b)
        L.append(f"| {rotulo} | {_num(a)} | {fim} | {_preco(p)} |")
    return L


def _bloco_do_concelho(nome, d, fontes):
    agua, san = d["agua"], d.get("saneamento") or {}
    L = [f"### {nome}: {d['entidades']}", "",
         f"Vigência a partir de {d['vigencia']}. Utilizador doméstico, tarifário geral, contador até "
         + ("15 mm" if nome == "Funchal" else "25 mm") + ", meses de 30 dias.", "",
         "Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):", ""]
    for f in d["fontes"]:
        rel = _caminho_da_fonte(f)
        reg = fontes.get(rel) if rel else None
        L.append(f"- {re.sub(r' [(]tarifas_portugal/[^)]*[)]', '', f)}")
        if reg:
            L.append(f"  Endereço: {reg[0]}; SHA-256 `{reg[1]}`; recolhido em {reg[2][8:10]}/{reg[2][5:7]}/{reg[2][:4]}.")
    L += ["", f"<!-- tabela: Estrutura do tarifário {ARTIGO.get(nome, 'de ' + nome)} -->",
          "| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |",
          "| :--- | ---: | ---: | ---: | ---: |",
          f"| água, tarifa fixa por mês | — | — | {_eur(agua['fixa_mes'])} | {_num(agua['iva_pct'])}% |"]
    for a, b, p in agua["escaloes"]:
        fim = "sem limite" if b is None else _num(b)
        L.append(f"| água, escalão | {_num(a)} | {fim} | {_preco(p)} €/m³ | {_num(agua['iva_pct'])}% |")
    if san.get("escaloes"):
        L.append(f"| saneamento, tarifa fixa por mês | — | — | {_eur(san['fixa_mes'])} | {_num(san['iva_pct'])}% |")
        for a, b, p in san["escaloes"]:
            fim = "sem limite" if b is None else _num(b)
            L.append(f"| saneamento, escalão (sobre {_num(san['coef_recolha'] * 100)}% do volume de água) | {_num(a)} | {fim} | {_preco(p)} €/m³ | {_num(san['iva_pct'])}% |")
        if san.get("trh_m3"):
            L.append(f"| saneamento, taxa de recursos hídricos | — | — | {_preco(san['trh_m3'])} €/m³ recolhido | {_num(san['iva_pct'])}% |")
    for p in d.get("parcelas", []):
        if p.get("fixa"):
            L.append(f"| {p['nome']}, fixa por mês | — | — | {_eur(p['fixa'])} | {_num(p['iva_pct'])}% |")
        if p.get("por_m3"):
            L.append(f"| {p['nome']}, por m³ de água | — | — | {_preco(p['por_m3'])} €/m³ | {_num(p['iva_pct'])}% |")
    L += ["", "Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):", "",
          f"<!-- tabela: Contas mensais de conferência do tarifário {ARTIGO.get(nome, 'de ' + nome)} -->",
          "| Consumo | Conta |", "| ---: | ---: |"]
    for c in d.get("conferencia", []):
        L.append(f"| {_num(c['m3'])} m³/mês | {_eur(c['conta'], 4)} |")
    L += ["", "Hipóteses e dúvidas registadas ao transcrever:", ""]
    L += [f"- {n}" for n in d.get("notas", [])]
    L.append("")
    return L


def _confianca_por_concelho():
    """A secção «Confiança dos valores tarifários por concelho» (verde, amarelo, cinza, por serviço).

    Vem de ``tarifas_portugal/procedencia_pt.py``, ferramenta de desenvolvimento que fica fora do Git:
    sem ela, a secção é omitida (e o apêndice D não a perde se o ficheiro já a tiver: ``gravar`` não desfaz
    revisão feita à mão). Os dados são ``entidades.json``, ``fontes/FONTES.tsv`` e ``portugal_tarifarios.json``.
    """
    pasta = os.path.join(BASE, "tarifas_portugal")
    if not os.path.isfile(os.path.join(pasta, "procedencia_pt.py")) or not os.path.isfile(os.path.join(pasta, "entidades.json")):
        return []
    import importlib.util
    espec = importlib.util.spec_from_file_location("procedencia_pt", os.path.join(pasta, "procedencia_pt.py"))
    modulo = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(modulo)
    return modulo.texto_manual()


def apendice_d():
    caminho = os.path.join(PKG, "data", "portugal_tarifarios.json")
    if not os.path.exists(caminho):
        return None, 0
    import json
    from tabela_de_faixas import secao
    base = json.load(open(caminho, encoding="utf-8"))
    tarifarios = {k: v for k, v in base.items() if not k.startswith("_")}
    fontes = _fontes_registadas()

    L = [
        "# Regimes tarifários",
        "",
        f"A Edição Portugal traz o tarifário doméstico de **{len(tarifarios)} concelhos**, transcrito",
        "dos documentos das entidades gestoras: " + ", ".join(sorted(tarifarios)) + ". Para qualquer",
        "outro concelho, o utilizador introduz o tarifário do projeto, na janela de tarifário (etapa 5),",
        "e o programa calcula a fatura com e sem o sistema. Este apêndice descreve a estrutura que o",
        "programa aceita, os seis regimes que reconhece e os tarifários transcritos.",
        "",
        "## Os códigos de escalão",
        "",
        "Cada linha da tabela de água é uma quádrupla `(mínimo, máximo, valor, código)`, em m³ por mês",
        "e euros por m³ (ou euros por mês nos códigos fixos).",
        "",
        "<!-- tabela: Os códigos da tabela tarifária de água -->",
        "| Código | Significado |",
        "| ---: | :--- |",
        "| 1 ou 0 | escalão progressivo: cobrado só sobre o volume dentro dele |",
        "| −1 | tarifa de disponibilidade: valor fixo por mês que se soma ao consumo medido |",
        "| −2 | franquia retroativa: até à franquia paga-se o valor fixo; depois, todo o volume desde zero é cobrado pelos escalões |",
        "| −3 | piso de pagamento: a fatura não pode ficar abaixo do valor |",
        "",
        "O efeito de cada código na fatura está desenhado na secção {{n:29}}, e não se repete aqui.",
        "",
        "## A fatura portuguesa",
        "",
        "Uma fatura doméstica soma, por mês, a água (tarifa fixa e escalões por m³), o saneamento de",
        "águas residuais, os resíduos urbanos, a taxa de recursos hídricos (TRH, por m³) e o IVA de",
        "cada parcela, **à taxa que o próprio tarifário declara**. Nenhuma taxa de IVA fica no código.",
        "O programa trata cada parcela assim:",
        "",
        "<!-- tabela: Como o programa guarda cada parcela da fatura portuguesa -->",
        "| Parcela | Como entra no projeto |",
        "| :--- | :--- |",
        "| água | escalões em `water_tariffs`; o IVA da água em `water_tax_var` |",
        "| saneamento por escalões | modo 3 do saneamento, sobre o volume recolhido (coeficiente de recolha × volume de água); a TRH e o IVA entram no preço de cada escalão |",
        "| saneamento ou resíduos por m³ | modo 2 do saneamento, com um preço único por m³ de água, IVA incluído |",
        "| tarifas fixas das outras parcelas | taxa fixa mensal (`water_tax_fixed`), com IVA |",
        "",
        "Os resíduos por escalões (como no Funchal) ainda não têm campo próprio: a parte variável soma-se",
        "à do saneamento, e só a parte fixa fica numa parcela à parte. A atualização tarifária é",
        "introduzida em separado para a água, o saneamento e a energia (apêndice {{n:A}}).",
        "",
        "## As quatro formas do saneamento",
        "",
        "<!-- tabela: As quatro formas de introduzir o saneamento -->",
        "| Modo | O saneamento é |",
        "| ---: | :--- |",
        "| 0 | um valor fixo |",
        "| 1 | uma percentagem da parcela de água (e não da fatura toda) |",
        "| 2 | um valor por m³ consumido |",
        "| 3 | escalões, aplicados a uma fração do volume de água que o utilizador declara |",
        "",
        "## Os seis regimes",
        "",
        "O programa classifica uma tabela de água num de seis regimes. O regime diz quanto vale poupar",
        "água, que é o que um estudo de aproveitamento de água de chuva precisa de ver.",
        "",
        "<!-- tabela: Os seis regimes tarifários e o que acontece ao poupar -->",
        "| Regime | Estrutura | O que acontece ao poupar |",
        "| :--- | :--- | :--- |",
    ]
    for nome, estrutura, efeito in REGIMES:
        L.append(f"| **{nome}** | {estrutura} | {efeito} |")
    L += ["",
          "**Teste rápido.** Simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os",
          "com uma fatura real. Se só um coincidir, o regime está errado. A secção {{n:16}} ensina o",
          "teste que identifica uma estrutura errada.",
          "",
          "## Os tarifários transcritos",
          "",
          "Os valores abaixo são os impressos nos documentos das entidades gestoras, transcritos em",
          "`triton/data/portugal_tarifarios.json` e recolhidos em 07/10/2026. São exemplos fiéis de",
          "como se introduz um tarifário, e não um catálogo: os tarifários mudam todos os anos, e é",
          "preciso verificar o documento em vigor da sua entidade gestora antes de qualquer conclusão",
          "económica. Os três têm a estrutura da tarifa de disponibilidade com escalões progressivos.",
          ""]
    L += secao(tarifarios, _num, _preco)
    L += [""]
    for nome in sorted(tarifarios):
        L += _bloco_do_concelho(nome, tarifarios[nome], fontes)
    L += ["### Eletricidade", "",
          "O Funchal leva ainda a tarifa de eletricidade, para o custo de bombagem: tarifa Base da",
          "Empresa de Eletricidade da Madeira, 6,90 kVA, 0,1673 €/kWh sem IVA. A fonte é um comparador",
          "(luzegas.pt, atualizado em 20/02/2025), **secundária**: confirme na EEM ou na ERSE. Lisboa e",
          "Porto não têm tarifa de eletricidade registada, e o custo de bombagem fica a zero até o",
          "utilizador introduzir a sua.", "",
          "## Documentos recolhidos e ainda não transcritos", "",
          "Os documentos abaixo estão arquivados com o endereço de origem e a impressão digital, mas",
          "ainda não foram transcritos para o programa, que por isso não os oferece. Neles, introduza o",
          "tarifário à mão. O tarifário de Bragança, em vigor, continua por obter.", "",
          "<!-- tabela: Concelhos com documento tarifário recolhido e ainda por transcrever -->",
          "| Concelho | Entidade | Documento |", "| :--- | :--- | :--- |"]
    L += [f"| {c} | {e} | {doc} |" for c, e, doc in RECOLHIDOS]
    L += [""] + _confianca_por_concelho()
    L += ["## Introduzir o seu tarifário", "",
          "1. Obtenha o documento tarifário em vigor da sua entidade gestora e anote a data.",
          "2. Introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5).",
          "3. Confira a fatura que o programa calcula com uma fatura real do edifício.",
          "4. Declare no estudo a entidade gestora, a data de vigência, o regime e a moeda.",
          ""]
    return NL.join(L), len(tarifarios)


def main():
    texto, n = apendice_a()
    gravar(os.path.join(SAIDA, "A_parametros.md"), texto + NL)
    print(f"  A_parametros.md — {n} parâmetros")

    texto, n = apendice_b()
    if texto is None:
        print("  B_processos.md — pulado: falta manual/processos.py")
    else:
        gravar(os.path.join(SAIDA, "B_processos.md"), texto + NL)
        print(f"  B_processos.md — {n} processos")

    texto, n = apendice_d()
    if texto is None:
        print("  D_regimes_tarifarios.md — pulado: tarifários não encontrados")
    else:
        gravar(os.path.join(SAIDA, "D_regimes_tarifarios.md"), texto + NL)
        print(f"  D_regimes_tarifarios.md — {n} concelhos")

    # C, E, F, G, H, I e J são escritos à mão (J sai de casos/resultados.json e casos/README.md).


if __name__ == "__main__":
    print("apêndices do manual (Edição Portugal):")
    main()
