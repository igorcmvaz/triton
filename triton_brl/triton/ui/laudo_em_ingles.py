# -*- coding: utf-8 -*-
"""Tradução para o inglês dos trechos em português que sobram nos laudos.

Os três laudos (executivo, auditoria ambiental ESG e dossiê técnico) são escritos em português, com
variantes em inglês onde o gerador ``report_generator`` previu uma. O laudo executivo não previa
nenhuma, e os outros dois deixavam trechos em português (nomes de itens do inventário, rótulos de
critérios do TOPSIS, mensagens de certificações, etc.). Em inglês, este módulo traduz cada trecho
de texto entre tags: primeiro o trecho inteiro, depois as expressões, sempre nas fronteiras de
palavra. O CSS e as tags não são tocados.

Regra de manutenção: o teste ``tests/unit/test_laudos_em_ingles.py`` gera os três laudos em inglês
e falha se sobrar português; acrescente aqui a tradução do trecho que ele apontar.

Este módulo também traz ``laudo_em_portugal``, o ajuste de vocabulário do laudo em português da
Edição Portugal (o glossário da interface não cobre palavras de laudo como «laudo» e «edificação»).
"""

from __future__ import annotations

import re

#: Trecho inteiro (entre tags, sem as bordas em branco) -> tradução.
TRECHOS = {
    # ── executivo ──
    "Laudo Técnico Executivo - Triton": "Executive Technical Report - Triton",
    "Laudo Técnico Executivo (Paisagem A4)": "Executive Technical Report (A4 Landscape)",
    "Conformidade Normativa:": "Normative compliance:", "Moeda:": "Currency:", "Série observada": "Observed series",
    "Localidade climática": "Climate site", "Base climática": "Climate dataset",
    "Período da série": "Series period", "Horizonte econômico": "Economic horizon",
    "Volume Recomendado": "Recommended Volume", "Reservatório Inferior": "Lower Cistern",
    "Economia Potável": "Potable-Water Savings",
    "Substituição da Concessionária": "Mains-Water Replacement", "Substituição de Água da Rede": "Mains-Water Replacement",
    "Retorno Líquido Atualizado": "Net Present Return", "Payback Estimado": "Estimated Payback",
    "1. Edificação & Hidrologia": "1. Building & Hydrology", "Parâmetro Técnico": "Technical Parameter",
    "Valor": "Value", "Série Pluviométrica": "Rainfall Series", "Área de Captação": "Catchment Area",
    "Coef. Escoamento (C)": "Runoff Coeff. (C)", "Descarte First Flush": "First-Flush Discard",
    "População Atendida": "Population Served",
    "2. Balanço Hídrico Simulado": "2. Simulated Water Balance", "Indicador Operacional": "Operational Indicator",
    "Desempenho": "Performance", "Volume Cisterna": "Cistern Volume", "Economia de Potável": "Potable-Water Savings",
    "Consumo Médio Pluvial": "Mean Rainwater Use", "Consumo Médio Potável": "Mean Potable-Water Use",
    "Volume Extravasado": "Overflow Volume", "Garantia Plena (100%)": "Full Supply (100%)",
    "Atendimento Nulo (0%)": "No Supply (0%)",
    "3. Viabilidade Econômica": "3. Economic Feasibility", "Indicador Financeiro": "Financial Indicator",
    "Resultado": "Result", "Investimento CAPEX": "CAPEX Investment", "Economia Bruta 1º Ano": "Gross Savings, Year 1",
    "Payback Simples": "Simple Payback", "Payback Descontado": "Discounted Payback", "TIR (% a.a.)": "IRR (% p.a.)",
    "📌 Parecer Técnico de Engenharia Hídrica & Sustentabilidade": "📌 Technical Opinion on Water Engineering & Sustainability",
    "⚠️ Termo de Responsabilidade Técnica & Validação": "⚠️ Technical Responsibility & Validation Notice",
    "Triton — Aproveitamento de Água de Chuva | Empreendimento:": "Triton — Rainwater Harvesting | Project:",
    "O Triton é uma ferramenta computacional de auxílio ao dimensionamento.": "Triton is a computational sizing-support tool.",
    "validar as premissas executivas, interferências de rede e conformidade com a legislação local.":
        "validating the executive assumptions, network interferences and compliance with local legislation.",
    "Cabe ao(à) profissional habilitado(a)": "The licensed professional is responsible for",
    # ── capa e tabelas do dossiê ──
    "CENTRO TECNOLÓGICO — CTC": "TECHNOLOGY CENTRE — CTC",
    "GRUPO DE PESQUISA EM AMBIENTES SUSTENTÁVEIS": "SUSTAINABLE ENVIRONMENTS RESEARCH GROUP",
    "Código de Referência:": "Reference code:", "Nome do Projeto:": "Project name:",
    "Data de Emissão:": "Issue date:", "Responsabilidade Técnica:": "Technical responsibility:",
    "Pesquisador(a) / Engenheiro(a) Responsável": "Responsible Researcher / Engineer",
    "Diretrizes Normativas:": "Standards basis:",
    "Dado / Parâmetro": "Data / Parameter",
    "Fatores de materiais/equipamentos": "Materials and equipment factors",
    "Premissas editáveis de triagem; registrar EPD/inventário, versão, geografia, fronteira e transformação adotados.":
        "Screening parameters; document supplier EPD/inventory, version, boundary and dataset.",
    # ── critérios do TOPSIS ──
    "Potencial máximo": "Maximum potential", "Mínimo extravasamento": "Minimum overflow",
    "Maior VPL": "Highest NPV", "Menor payback descontado": "Shortest discounted payback",
    "Maior TIR": "Highest IRR", "Menor CO₂ no fim da vida": "Lowest end-of-life CO₂",
    "Menor consumo de água potável": "Lowest potable-water use",
}

#: Frases com número do texto (resultados do ESG que o núcleo escreve em português), aplicadas antes
#: das expressões. Em inglês fora da Brasil o número vai no formato inglês.
REGEXES = (
    (r"O empreendimento atinge substituição hídrica global de ([\d.,]+)% \(interno: ([\d.,]+)%, externo: ([\d.,]+)%\), "
     r"poupando ([\d.,]+) m³/ano de água tratada \(([\d.,]+) m³ acumulados em (\d+) anos\)\. "
     r"No Selo LEED v4 WE \(máximo de (\d+) pontos possíveis\), o projeto tirou (\d+) de (\d+) pontos"
     r"(?:\.|\s+e, no AQUA-HQE Residencial, alcança (.+?)\.)\s*"
     r"Na certificação EDGE, que não pontua e sim mede percentual contra um caso-base, a barra de água chega a ([\d.,]+)% — "
     r"(acima|abaixo) do limiar de ([\d.,]+)% exigido em cada uma das três barras\.",
     lambda m: (f"The project reaches an overall potable-water substitution of {m.group(1)}% (indoor: {m.group(2)}%, outdoor: {m.group(3)}%), "
                f"saving {m.group(4)} m³/yr of treated water ({m.group(5)} m³ accumulated over {m.group(6)} years). "
                f"Under LEED v4 WE (maximum of {m.group(7)} points), the project scored {m.group(8)} of {m.group(9)} points"
                f"{'' if not m.group(10) else ' and, under AQUA-HQE Residencial, reaches ' + m.group(10).replace('Abaixo de', 'below')}. "
                f"For EDGE, which awards no points but measures a percentage against a baseline case, the water bar reaches {m.group(11)}% — "
                f"{'above' if m.group(12) == 'acima' else 'below'} the {m.group(13)}% threshold required in each of the three bars.")),
    (r"Economia de ([\d.,]+)% de água potável\.", r"Savings of \1% of potable water."),
    (r"(\d+) de (\d+) pontos na categoria de água", r"\1 of \2 points in the water category"),
    (r"(\d+) de (\d+) pontos", r"\1 of \2 points"),
    (r"(\d+) de (\d+) points?", r"\1 of \2 points"),
)

#: Expressões (dentro de um trecho), da mais longa para a mais curta na aplicação.
EXPRESSOES = (
    ("Fator: worldstainless (programa de aço inoxidável da World Steel Association), relatório de emissões de CO2 divulgado em 24/09/2024, berço-ao-portão com escopos 1, 2 e 3.",
     "Factor: worldstainless (World Steel Association stainless-steel programme), CO2 emissions report published on 24/09/2024, cradle-to-gate, scopes 1, 2 and 3."),
    ("A emissão depende fortemente do teor de sucata da carga: 1,95 kg CO2/kg a 85% de sucata, 2,45 a 75%, 3,70 a 50% e 6,80 a 30%.",
     "Emissions depend strongly on the scrap content of the charge: 1.95 kg CO2/kg at 85% scrap, 2.45 at 75%, 3.70 at 50% and 6.80 at 30%."),
    ("Adota-se o ponto de 50%, que é o cenário intermediário do relatório.", "The 50% point is adopted, the intermediate scenario of the report."),
    ("O valor anterior deste programa, 2,89, correspondia a cerca de 66% de sucata, sem que isso estivesse declarado.",
     "The previous value in this programme, 2.89, corresponded to about 66% scrap, which was not stated."),
    ("Massa por m³ útil permanece cenário interno.", "Mass per useful m³ remains an internal scenario."),
    ("Fator corroborado por inventário público da construção:", "Factor corroborated by a public construction inventory:"),
    ("Fator corroborado pelo SIDAC (inventário brasileiro da construção):", "Factor corroborated by SIDAC (Brazilian construction inventory):"),
    ("concreto dosado em central de cerca de 310 kg CO2/m³ a 20 MPa a 480 kg CO2/m³ a 40 MPa; 0,14 kg CO2e/kg x 2.400 kg/m³ = 336 kg/m³, dentro da faixa de 25 a 30 MPa.",
     "ready-mixed concrete from about 310 kg CO2/m³ at 20 MPa to 480 kg CO2/m³ at 40 MPa; 0.14 kg CO2e/kg x 2,400 kg/m³ = 336 kg/m³, within the range for 25 to 30 MPa."),
    # fontes e textos próprios da Edição Brasil (o laudo em inglês da BRL também sai em inglês)
    ("ABNT NBR 5688:2018 Tab. 1, série reforçada: dem", "ABNT NBR 5688:2018 Table 1, reinforced series: OD"),
    ("Amanco Wavin FTC000021 (out/2025), tubo soldável", "Amanco Wavin FTC000021 (Oct/2025), solvent-weld pipe"),
    ("Massa de catálogo Dancor (60 Hz)", "Dancor catalogue mass (60 Hz)"), ("da EPD Grundfos", "from the Grundfos EPD"),
    ("aproximação de ordem de grandeza", "order-of-magnitude approximation"),
    ("a EPD do fabricante empregado prevalece", "the EPD of the manufacturer actually used prevails"),
    ("Fator de rede editável; usar a série MCTI/SIRENE do período do estudo", "Editable grid factor; use the MCTI/SIRENE series for the study period"),
    ("Fator de água potável editável; substituir pelo inventário da concessionária", "Editable potable-water factor; replace with the utility's inventory"),
    ("sistema de recuperação de águas pluviais", "rainwater recovery system"),
    ("redução de pelo menos 20% da água potável", "at least 20% potable-water reduction"),
    ("economia de 40% da água potável", "40% potable-water savings"),
    ("O sistema atende ao item EAU.1.5 (HQE 3) se seguir as NBR 15527 e 16783.", "The system meets item EAU.1.5 (HQE 3) if it follows NBR 15527 and 16783."),
    ("O referencial mede a economia contra o cenário de referência da planilha auxiliar da Fundação Vanzolini, que soma também os dispositivos economizadores: confira ali.",
     "The reference system measures savings against the baseline scenario of the Fundação Vanzolini auxiliary spreadsheet, which also adds up water-saving fixtures: check it there."),
    ("2 a 5 pontos, conforme a abrangência", "2 to 5 points, depending on scope"), ("2 a 5 pontos", "2 to 5 points"),
    ("Sem água pluvial aproveitada, não há sistema a enquadrar no critério 3.6.", "Without harvested rainwater there is no system to fit under criterion 3.6."),
    ("Critério 3.6 não atendido", "Criterion 3.6 not met"), ("Critério 3.6 atendido", "Criterion 3.6 met"),
    ("O indicador é a existência de sistema de aproveitamento de águas pluviais, com captação, tratamento, reservação e pontos de uso indicados. Pontuação pela abrangência: áreas comuns 2, unidades habitacionais 4, unidades e áreas comuns 5 (casas em loteamento com preparação, 2). Obrigatório para o nível Diamante. No Selo Casa Azul Uni, o critério equivalente (7) vale 1 ponto. Abrangência não informada: pontuação não atribuída.",
     "The indicator is the existence of a rainwater harvesting system, with catchment, treatment, storage and indicated points of use. Scoring by scope: common areas 2, dwelling units 4, units and common areas 5 (houses in a prepared subdivision, 2). Mandatory for the Diamond level. In the Casa Azul Uni seal, the equivalent criterion (7) is worth 1 point. Scope not informed: score not awarded."),
    ("Massa: catalogo tecnico Fortlev, &#x27;Caixa d&#x27;agua em fibra de vidro&#x27; (peso da caixa vazia por capacidade), reservatorios conforme ABNT NBR 13210.",
     "Mass: Fortlev technical catalogue, glass-fibre tank (empty tank weight by capacity), tanks to ABNT NBR 13210."),
    ("— Aproveitamento de água de chuva de coberturas para fins não potáveis — Requisitos.", "— Rainwater harvesting from roofs for non-potable purposes — Requirements."),
    ("— Série oficial de fatores médios de emissão do SIN; selecionar o arquivo correspondente ao período do estudo.",
     "— Official series of average emission factors of the national grid; select the file for the study period."),
    ("CREA / Matrícula Acadêmica / Registro Profissional", "CREA / Academic Enrolment / Professional Registration"),
    ("; fundamento do TOPSIS.", "; foundation of the TOPSIS method."),
    ("A massa por m³ útil (1.200 kg) segue sendo cenário geométrico interno; para a obra, use a EPD do concreto e o quantitativo de aço do projeto.",
     "The mass per useful m³ (1,200 kg) remains an internal geometric scenario; for the works, use the concrete EPD and the steel quantity of the design."),
    ("Massa: catálogo técnico de fabricante, caixa em fibra de vidro (peso da caixa vazia por capacidade), reservatorios conforme norma de referência.",
     "Mass: manufacturer technical catalogue, glass-fibre tank (empty tank weight by capacity), tanks to the reference standard."),
    ("Fator de emissao: Composites UK, &#x27;Embodied carbon data for composites&#x27; (atualizado em 22/04/2026), que da faixa tipica de 2,5 a 4,0 kg CO2e/kg para pecas de PRFV; adota-se o ponto medio de 3,25.",
     "Emission factor: Composites UK, &#x27;Embodied carbon data for composites&#x27; (updated 22/04/2026), which gives a typical range of 2.5 to 4.0 kg CO2e/kg for GRP parts; the mid-point of 3.25 is adopted."),
    ("O valor de 8,1 kg CO2e/kg que circula na literatura antiga vem da base ICE dos anos 1990 e foi removido na ICE v4.0 - quem o encontrar deve descarta-lo.",
     "The value of 8.1 kg CO2e/kg found in older literature comes from the ICE database of the 1990s and was removed in ICE v4.0; anyone who finds it should discard it."),
    ("1.612 kg CO2e por 1.000 kg de resina (TRACI 2.1 / IPCC 2013 GWP-100, escopo EUA).",
     "1,612 kg CO2e per 1,000 kg of resin (TRACI 2.1 / IPCC 2013 GWP-100, US scope)."),
    ("Substitui o valor interno anterior de 3,00, que não tinha fonte e declarava a mesma fronteira.",
     "Replaces the previous internal value of 3.00, which had no source and declared the same boundary."),
    ("A massa por m³ segue sendo cenário interno.", "The mass per m³ remains an internal scenario."),
    ("Dimensionamento em triton/core/water_quality.py", "Sized by the Triton water-quality module"),
    ("(1 Principal + 1 Reserva/Backup)", "(1 main + 1 standby)"), ("(Principal)", "(main)"), ("Litros", "litres"), ("un.", "pcs"), ("Estágios:", "Stages:"), ("kg CO2e/ano", "kg CO2e/yr"), ("produto/ano a", "product/yr at"),
    ("Moeda: não definida no projeto (valores sem símbolo)", "Currency: not set in the project (values shown without a symbol)"),
    ("Normas e regulamentos aplicáveis no local do projeto, a indicar pelo(a) engenheiro(a) responsável",
     "Codes and standards applicable at the project site, to be stated by the responsible engineer"),
    ("Nas premissas registradas, o sistema pluvial apresenta economia potável modelada de",
     "Under the recorded assumptions, the rainwater system shows modelled potable-water savings of"),
    ("a viabilidade econômica não foi calculada neste estudo", "the economic feasibility was not calculated in this study"),
    ("nas premissas adotadas, o investimento se paga no horizonte de análise", "under the assumptions adopted, the investment pays for itself within the analysis horizon"),
    ("nas premissas adotadas, o investimento não se paga no horizonte de análise", "under the assumptions adopted, the investment does not pay for itself within the analysis horizon"),
    ("O dimensionamento segue as diretrizes da ABNT NBR 15527.", "Sizing follows the ABNT NBR 15527 guidelines."),
    ("O dimensionamento segue as diretrizes da EN 16941-1.", "Sizing follows the EN 16941-1 guidelines."),
    ("O dimensionamento segue as normas técnicas e os regulamentos aplicáveis no local do projeto.",
     "Sizing follows the technical standards and regulations applicable at the project site."),
    ("Normas e regulamentos aplicáveis no local do projeto", "Standards and regulations applicable at the project site"),
    ("EN 16941-1 e regulamentação nacional aplicável", "EN 16941-1 and applicable national regulations"),
    ("Aproveitamento de Água de Chuva | Empreendimento:", "Rainwater Harvesting | Project:"),
    ("Demanda Pluvial Alvo", "Target Rainwater Demand"),
    ("e payback simples de", "and a simple payback of"),
    ("VPL de", "NPV of"), ("VPL (", "NPV ("), ("Ref. Projeto:", "Project ref.:"), ("Emissão:", "Issued:"),
    ("(descontado)", "(discounted)"), ("% dos dias", "% of days"), ("L/dia", "L/day"), ("L/hab/dia", "L/person/day"),
    ("pessoas", "people"), ("Anos", "Years"), ("anos", "years"), ("/ ano", "/ yr"), ("% a.a.", "% p.a."),
    ("Sem retorno no horizonte", "No return"), ("kg/ano", "kg/yr"), ("m³/ano", "m³/yr"), ("kWh/ano", "kWh/yr"),
    # ── inventário de ACV e certificações ──
    ("Cisterna Inferior", "Lower Cistern"), ("Caixa d'Água Superior", "Upper Tank"),
    ("Polietileno", "Polyethylene"), ("Concreto", "Concrete"), ("Poliéster", "Polyester"), ("Aço", "Steel"),
    ("Tubulação PVC Rígido", "Rigid PVC Pipe"),
    ("Motobomba de Pressurização", "Pressurising Pump"), ("Motobomba de Recalque", "Discharge Pump"),
    ("Ferro Fundido, Cobre & Alumínio", "Cast Iron, Copper & Aluminium"),
    ("Sistema de Descarte de 1ª Água (Filtro Folhas + Res.", "First-Flush Discard System (Leaf Filter + Tank"),
    ("Arranjo 3D:", "3D Layout:"),
    ("Consumo Elétrico do Bombeamento", "Pumping Electricity Use"),
    ("Linha de Tratamento (ETAP)", "Treatment Line"),
    ("Dosagem Química / Desinfecção (Caixa Superior)", "Chemical Dosing / Disinfection (Upper Tank)"),
    ("Água Potável Evitada da Rede Pública", "Mains Potable Water Avoided"),
    ("Cloração (dosador de pastilhas de hipoclorito de cálcio)", "Chlorination (calcium hypochlorite tablet feeder)"),
    ("produto/ano", "product/yr"), ("kg material", "kg material"),
    ("Abaixo do limiar LEED (Mín. 25%)", "Below the LEED threshold (min. 25%)"),
    ("Opções 2 a 6", "Options 2 to 6"), ("Opção 1", "Option 1"), ("2 de 8 points", "2 of 8 points"),
    ("Resina:", "Resin:"), ("Tabela 6", "Table 6"),
    ("Franklin Associates para o American Chemistry Council", "Franklin Associates for the American Chemistry Council"),
)

#: Número em formato português («1.793,14», «2,36») no texto que o núcleo escreve: em inglês fora da Brasil
#: vira «1,793.14» e «2.36». A fração de três dígitos é ambígua (milhar inglês) e fica como está.
_NUMERO_PT_COMPLETO = re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+),(\d+)(?![\d,])")
_NUMERO_PT_DECIMAL = re.compile(r"(?<![\d.,])(\d+),(\d{1,2}|\d{4,})(?![\d.,])")


def _numeros_em_ingles(texto: str) -> str:
    texto = _NUMERO_PT_COMPLETO.sub(lambda m: m.group(1).replace(".", ",") + "." + m.group(2), texto)
    return _NUMERO_PT_DECIMAL.sub(lambda m: m.group(1) + "." + m.group(2), texto)


_EXPRESSOES_ORDENADAS = tuple(sorted(EXPRESSOES, key=lambda par: len(par[0]), reverse=True))
_TRECHOS_LONGOS = tuple(sorted(((f, a) for f, a in TRECHOS.items() if len(f) > 12), key=lambda par: len(par[0]), reverse=True))


#: Número com ponto de milhar à frente de uma unidade («10.000 L», «1.612 kg»): no texto que o núcleo
#: escreve em português o ponto é de milhar; em inglês fora da Brasil vira vírgula.
_MILHAR_COM_UNIDADE = re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+)(?=\s*(?:L|kg|m³|mm|kWh|MPa)\b)")


def _fora_da_brasil() -> bool:
    from triton.core.edition import usa_dados_do_brasil
    return not usa_dados_do_brasil()


def _milhar_em_ingles(texto: str) -> str:
    from triton.core.edition import usa_dados_do_brasil
    if usa_dados_do_brasil():
        return texto
    return _MILHAR_COM_UNIDADE.sub(lambda m: m.group(1).replace(".", ","), texto)


def _traduz_no(texto: str) -> str:
    miolo = texto.strip()
    if not miolo:
        return texto
    if miolo in TRECHOS:
        return texto.replace(miolo, TRECHOS[miolo])
    saida = texto
    for padrao, alvo in REGEXES:
        saida = re.sub(padrao, alvo, saida)
    fora_da_brasil = _fora_da_brasil()
    if fora_da_brasil:
        saida = _numeros_em_ingles(saida)
    for fonte, alvo in _TRECHOS_LONGOS:
        if fonte in saida:
            saida = saida.replace(fonte, alvo)
    for fonte, alvo in _EXPRESSOES_ORDENADAS:
        if fora_da_brasil:
            fonte = _numeros_em_ingles(fonte)
        antes = r"(?<![\w])" if fonte[0].isalnum() else ""
        depois = r"(?![\w])" if fonte[-1].isalnum() else ""
        saida = re.sub(antes + re.escape(fonte) + depois, alvo, saida)
    return _milhar_em_ingles(saida)


#: Português de Portugal para palavras de laudo que o glossário da interface não cobre.
#: (português do Brasil, português de Portugal); a caixa é respeitada pelas duas formas.
_LAUDO_PT_PT = (
    ("Laudo", "Relatório"), ("laudo", "relatório"),
    ("Edificações", "Edifícios"), ("edificações", "edifícios"),
    ("Edificação", "Edifício"), ("edificação", "edifício"),
    ("Premissas", "Pressupostos"), ("premissas", "pressupostos"),
    ("Premissa", "Pressuposto"), ("premissa", "pressuposto"),
    ("Economia", "Poupança"), ("economia", "poupança"),
    ("Vazão", "Caudal"), ("vazão", "caudal"),
    ("Tubulações", "Tubagens"), ("tubulações", "tubagens"),
    ("Tubulação", "Tubagem"), ("tubulação", "tubagem"),
    ("Motobomba", "Eletrobomba"), ("motobomba", "eletrobomba"),
    ("Reúso", "Reutilização"), ("reúso", "reutilização"),
)
_LAUDO_PT_PT_ORDENADO = tuple(sorted(_LAUDO_PT_PT, key=lambda par: len(par[0]), reverse=True))


def laudo_em_portugal(html: str) -> str:
    """O laudo (HTML) em português com o vocabulário de Portugal que falta no glossário da interface."""
    partes = re.split(r"(<style.*?</style>|<svg.*?</svg>)", html, flags=re.S)
    for i, parte in enumerate(partes):
        if parte.startswith("<style") or parte.startswith("<svg"):
            continue

        def troca(m):
            texto = m.group(1)
            for fonte, alvo in _LAUDO_PT_PT_ORDENADO:
                texto = re.sub(r"(?<![\w])" + re.escape(fonte) + r"(?![\w])", alvo, texto)
            return ">" + texto + "<"

        partes[i] = re.sub(r">([^<>]+)<", troca, parte)
    return "".join(partes)


def laudo_em_ingles(html: str) -> str:
    """O laudo (HTML) com os trechos em português traduzidos para o inglês."""
    partes = re.split(r"(<style.*?</style>|<svg.*?</svg>)", html, flags=re.S)
    for i, parte in enumerate(partes):
        if parte.startswith("<style") or parte.startswith("<svg"):
            continue
        partes[i] = re.sub(r">([^<>]+)<", lambda m: ">" + _traduz_no(m.group(1)) + "<", parte)
    return "".join(partes)
