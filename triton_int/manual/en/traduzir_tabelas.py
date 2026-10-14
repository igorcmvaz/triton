# -*- coding: utf-8 -*-
"""Translates the numeric tables of the manual into English, from the Portuguese ones.

`manual/gerar_tabelas.py` runs the program and writes the tables of the chapters in
`manual/partes/_tabelas`. The numbers there are the ones the tests check against the
program. The English manual does not compute them again: it takes the same files and
translates the words and the number format. A number can therefore never differ between
the two manuals.

Every caption and every text cell must be in the dictionaries below. Anything that is not
stops the run and is listed: a new table, or a changed caption, cannot reach the English
manual in Portuguese.

Output: manual/en/partes/_tabelas/*.md
"""

from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.dirname(AQUI)
ORIGEM = os.path.join(MANUAL, "partes", "_tabelas")
DESTINO = os.path.join(AQUI, "partes", "_tabelas")
NL = chr(10)

#: Whole captions, without the number when there is one.
LEGENDAS = {
    # cap40 a cap43, modulação probabilística
    'Parte da variância do resultado explicada por cada variável sorteada no exemplo do tutorial, no volume escolhido (η²; as variáveis contínuas agrupadas em decis)': 'Share of the variance of the result explained by each drawn variable in the tutorial example, at the chosen volume (η²; continuous variables grouped in deciles)',
    'Parte da variância do resultado explicada por cada fonte de incerteza no exemplo dos modelos climáticos, no volume escolhido (η²; as variáveis contínuas agrupadas em decis)': 'Share of the variance of the result explained by each source of uncertainty in the climate-model example, at the chosen volume (η²; continuous variables grouped in deciles)',
    'Resultados no volume escolhido (5 m³) por modelo climático sorteado, em Florianópolis no cenário SSP2-4.5 de 2025 a 2054, com as três variáveis de consumo também sorteadas': 'Results at the chosen volume (5 m³) by drawn climate model, in Florianópolis under scenario SSP2-4.5 from 2025 to 2054, with the three consumption variables also drawn',
    'As variáveis que a modulação probabilística pode sortear, com a distribuição de triagem que a tela propõe': 'The variables that probabilistic modulation can draw, with the screening distribution the screen proposes',
    'As variáveis sorteadas no exemplo do tutorial: distribuição declarada e estatísticas das realizações': 'The variables drawn in the tutorial example: declared distribution and statistics of the realisations',
    'Resultados no volume escolhido pelo estudo do tutorial: estudo determinístico e estatísticas das realizações': 'Results at the volume chosen by the tutorial study: deterministic study and statistics of the realisations',
    'Probabilidades no volume escolhido, com o intervalo de confiança de 95% de Wilson': 'Probabilities at the chosen volume, with the Wilson 95% confidence interval',
    'Frequência com que cada volume é escolhido nas realizações do exemplo, por critério (%)': 'Frequency with which each volume is chosen in the realisations of the example, by criterion (%)',
    'Sensibilidade no volume escolhido: força e sentido da influência de cada variável sorteada sobre os resultados do tutorial': 'Sensitivity at the chosen volume: strength and direction of the influence of each drawn variable on the tutorial results',
    "Caracterização da série de precipitação de Florianópolis adotada no tutorial":
        "Characteristics of the Florianópolis precipitation series used in the tutorial",
    "Resultado da primeira simulação do tutorial, com reservatório de 3.000 L":
        "Result of the first tutorial simulation, with a 3,000 L tank",
    "Volume ideal obtido com cada limiar de ganho marginal, para o mesmo projeto":
        "Ideal volume obtained with each marginal-gain threshold, for the same project",
    "Custo e desempenho comparados entre o volume ideal e o volume máximo varrido":
        "Cost and performance compared between the ideal volume and the largest volume swept",
    "Varredura de volumes do projeto do tutorial, com o ganho marginal de cada metro cúbico acrescentado":
        "Volume sweep of the tutorial project, with the marginal gain of each added cubic metre",
    "Efeito do limiar de acionamento da motobomba sobre o potencial de economia e sobre o número de acionamentos":
        "Effect of the pump trigger level on the saving potential and on the number of starts",
    "Comparação entre reservatório único e reservatório duplo, mantido o mesmo armazenamento total":
        "Single tank compared with two tanks, keeping the same total storage",
    "Custo da linha de tratamento conforme a tecnologia de desinfecção adotada":
        "Cost of the treatment line according to the disinfection technology adopted",
    "Recomendação de filtração fina e custo da linha por classe de qualidade":
        "Fine-filtration recommendation and cost of the line by quality class",
    "Composição da fatura de água e esgoto antes e depois do sistema pluvial":
        "Make-up of the water and sewage bill before and after the rainwater system",
    "Indicadores econômicos do projeto do tutorial em vinte anos de análise":
        "Economic indicators of the tutorial project over twenty years of analysis",
    "Emissões líquidas de carbono do projeto do tutorial conforme o material do reservatório":
        "Net carbon emissions of the tutorial project according to the tank material",
    "Efeito do volume da cisterna de concreto sobre as emissões líquidas de carbono":
        "Effect of the concrete cistern volume on the net carbon emissions",
    "Matriz de decisão multicritério: cada volume da varredura avaliado nas três dimensões de análise":
        "Multi-criteria decision matrix: each sweep volume assessed in the three dimensions of analysis",
    "Volume vencedor segundo cada critério isolado":
        "Winning volume under each criterion taken alone",
    "Volume escolhido pelo TOPSIS conforme a dimensão que recebe peso dominante, e o segundo colocado":
        "Volume chosen by TOPSIS according to the dimension given the dominant weight, and the runner-up",
    "O mesmo projeto do tutorial simulado em quatro capitais brasileiras":
        "The same tutorial project simulated in four Brazilian state capitals",
    "Potencial, valor presente líquido e retorno do projeto fechado do tutorial com cada premissa variada sozinha, do valor baixo ao alto":
        "Potential, net present value and payback of the final tutorial project with each assumption varied alone, from the low to the high value",
    "Balanço hídrico diário do caso resolvido, dia a dia, com as parcelas de captação, consumo, extravasamento e armazenamento":
        "Daily water balance of the worked case, day by day, with collection, consumption, overflow and storage",
    "Verificação do fechamento do balanço de massa nos dez dias":
        "Check of the mass balance closure over the ten days",
    "Indicadores resultantes do caso resolvido de dez dias":
        "Indicators of the ten-day worked case",
    "Dados de entrada do caso resolvido de dez dias":
        "Input data of the ten-day worked case",
    "Série de precipitação dos dez dias do caso resolvido":
        "Precipitation series of the ten days of the worked case",
    "Volumes dados pelos métodos do Anexo A da ABNT NBR 15527:2007 para o projeto do tutorial, arredondados a 250 L, e o potencial que cada um produz na simulação diária":
        "Volumes given by the methods of Annex A of ABNT NBR 15527:2007 for the tutorial project, rounded to 250 L, and the potential each one yields in the daily simulation",
    "Fração de armazenamento dos volumes da varredura e o passo de simulação que Fewkes e Butler (2000) recomendam para cada faixa":
        "Storage fraction of the sweep volumes and the simulation time step Fewkes and Butler (2000) recommend for each range",
    "Energia anual de seis pressurizadores de catálogo na pressurização direta do tutorial, com a vazão da bacia sanitária limitando a da bomba":
        "Annual energy of six catalogue pressure pumps in the tutorial's direct pressurisation, with the toilet flow limiting the pump flow",
    "Inventário de carbono do projeto fechado do tutorial, item a item, com a parcela de cada componente no carbono incorporado; valores anuais negativos são crédito":
        "Carbon inventory of the final tutorial project, item by item, with the share of each component in the embodied carbon; negative annual values are credits",
    "Escore de proximidade TOPSIS com pesos iguais entre as dimensões e aceitabilidade de primeiro lugar no SMAA-VIKOR, com 5.000 vetores de pesos sorteados, para os volumes do tutorial":
        "TOPSIS closeness score with equal weights across the dimensions and first-rank acceptability in SMAA-VIKOR, with 5,000 random weight vectors, for the tutorial volumes",
    "Panorama das versões publicadas": "Overview of the published versions",
}

#: Whole cells (bold markers removed before lookup) and the loose text lines.
CELULAS = {
    "Primeiro lançamento oficial do Triton, programa derivado do Netuno 5.0.1, com nome, versionamento e repositório próprios para cada edição.": "First official release of Triton, a program derived from Netuno 5.0.1, with its own name, versioning and repository for each edition.",
    "Corrige a demanda mensal e semanal igual a zero, que o programa trocava pela demanda padrão, e acrescenta a regra de operação de Fewkes como opção, em todos os módulos.": "Fixes monthly and weekly demand equal to zero, which the program replaced with the default demand, and adds the Fewkes operating rule as an option, in every module.",
    # cap40 a cap43, modulação probabilística
    'Tarifas': 'Tariffs',
    'Custos': 'Costs',
    'Fluxo de caixa': 'Cash flow',
    'Ambiente': 'Environment',
    'Fator do esgoto': 'Sewerage factor',
    'Reajuste da energia': 'Electricity escalation',
    'Fator do preço da cisterna': 'Cistern price factor',
    'Fator do custeio (O&M)': 'Running cost factor (O&M)',
    'Inflação do custeio': 'Running cost inflation',
    'Período de análise': 'Analysis period',
    'Fator da emissão da água potável': 'Potable water emission factor',
    'Fator da emissão da rede elétrica': 'Grid electricity emission factor',
    'lognormal, média 1, desvio de 0,25': 'lognormal, mean 1, deviation of 0.25',
    'normal, média do projeto, desvio de 0,10 ponto': 'normal, project mean, deviation of 0.10 point',
    'triangular, do projeto −5 ao projeto +5 anos; inteiro, ao menos 1': 'triangular, from project −5 to project +5 years; integer, at least 1',
    'normal, média 1, desvio de 0,20': 'normal, mean 1, deviation of 0.20',
    'Fonte de incerteza': 'Source of uncertainty',
    'η² da economia': 'η² of savings',
    'η² do VPL': 'η² of NPV',
    'η² do saldo de CO₂': 'η² of CO₂ balance',
    'Soma': 'Sum',
    'Modelo climático': 'Climate model',
    'Realizações': 'Realisations',
    'Chuva média (mm/ano)': 'Mean rainfall (mm/year)',
    'Economia média (%)': 'Mean savings (%)',
    'VPL médio (R$)': 'Mean NPV (R$)',
    'P(VPL > 0) (%)': 'P(NPV > 0) (%)',
    'Variável': 'Variable',
    'Distribuição de triagem': 'Screening distribution',
    'Marcada ao abrir': 'Ticked on opening',
    'L/hab.dia': 'L/person/day',
    'lognormal, média do projeto, CV de 20%': 'lognormal, project mean, CV of 20%',
    'Número de pessoas': 'Number of occupants',
    'normal, média do projeto, desvio de 1 pessoa; inteiro de 1 ao dobro': 'normal, project mean, deviation of 1 occupant; integer from 1 to double',
    'Fração não potável interna': 'Indoor non-potable fraction',
    'normal, média do projeto, desvio de 5 pontos; 0 a 100%': 'normal, project mean, deviation of 5 points; 0 to 100%',
    'normal, média do projeto, CV de 30%': 'normal, project mean, CV of 30%',
    'Captação': 'Catchment',
    'Área de captação': 'Catchment area',
    'normal, média do projeto, CV de 5%': 'normal, project mean, CV of 5%',
    'Coeficiente de escoamento': 'Runoff coefficient',
    'triangular, do projeto −0,10 ao projeto +0,05; 0 a 1': 'triangular, from project −0.10 to project +0.05; 0 to 1',
    'Lâmina de descarte': 'First-flush depth',
    'uniforme, do projeto −1 mm ao projeto +1 mm': 'uniform, from project −1 mm to project +1 mm',
    'Fator da chuva': 'Rainfall factor',
    'normal, média 1, desvio de 0,10': 'normal, mean 1, deviation of 0.10',
    'Fator das tarifas de água e esgoto': 'Water and sewerage tariff factor',
    'Reajuste tarifário': 'Tariff escalation',
    '% por período': '% per period',
    'normal, média do projeto, desvio de 2 pontos': 'normal, project mean, deviation of 2 points',
    'Taxa mínima de atratividade': 'Minimum attractive rate of return',
    '% ao mês': '% per month',
    'normal, média do projeto, desvio de 0,25 ponto': 'normal, project mean, deviation of 0.25 point',
    'lognormal, média 1, desvio de 0,15': 'lognormal, mean 1, deviation of 0.15',
    'Tarifa de energia': 'Energy tariff',
    'normal, média do projeto, CV de 10%': 'normal, project mean, CV of 10%',
    'Distribuição': 'Distribution',
    'Média': 'Mean',
    'Desvio-padrão': 'Standard deviation',
    'Consumo per capita (L/hab.dia)': 'Per capita consumption (L/person/day)',
    'Número de pessoas (pessoas)': 'Number of occupants (occupants)',
    'Fração não potável interna (%)': 'Indoor non-potable fraction (%)',
    'Fator da chuva (×)': 'Rainfall factor (×)',
    'Fator das tarifas de água e esgoto (×)': 'Water and sewerage tariff factor (×)',
    'Fator do investimento (×)': 'Investment factor (×)',
    'Fator do investimento': 'Investment factor',
    'Ideal técnico': 'Technical ideal',
    'Ótimo econômico (payback)': 'Economic optimum (payback)',
    'Vencedor TOPSIS': 'TOPSIS winner',
    'nenhum se paga': 'none pays back',
    'o saldo de CO₂ no ciclo de vida é positivo': 'the life-cycle CO₂ balance is positive',
    'o investimento se paga (VPL > 0)': 'the investment pays back (NPV > 0)',
    'Evento': 'Event',
    'Probabilidade (%)': 'Probability (%)',
    'IC 95%, limite inferior (%)': '95% CI, lower bound (%)',
    'IC 95%, limite superior (%)': '95% CI, upper bound (%)',
    'Estudo determinístico': 'Deterministic study',
    'Economia de água potável (%)': 'Potable water savings (%)',
    'Payback descontado (anos)': 'Discounted payback (years)',
    'Saldo de CO₂ no ciclo de vida (kg)': 'Life-cycle CO₂ balance (kg)',
    'ρ com a economia': 'ρ with savings',
    'ρ com o VPL': 'ρ with NPV',
    'ρ com o saldo de CO₂': 'ρ with CO₂ balance',
    'No estudo': 'In the study',
    'Grupo': 'Group',
    'Unidade': 'Unit',
    'Demanda': 'Demand',
    'Economia': 'Economics',
    'Consumo per capita': 'Per capita consumption',
    'Demanda externa': 'Outdoor demand',
    'L/dia': 'L/day',
    'Grandeza': 'Quantity',
    'sim': 'yes',
    'não': 'no',
    'pessoas': 'occupants',
    # cap04
    "A série de Florianópolis": "The Florianópolis series", "Valor": "Value",
    "dias na série": "days in the series", "anos": "years",
    "precipitação média anual": "mean annual precipitation", "dias com chuva": "days with rain",
    "chuva média nos dias chuvosos": "mean rain on rainy days", "maior chuva diária": "largest daily rain",
    "dias abaixo da lâmina de descarte": "days below the first-flush depth",
    # cap06
    "Resultado com 3,000 L": "Result with 3,000 L",
    "potencial de economia de água potável": "potable water saving potential",
    "água pluvial consumida": "rainwater consumed", "água da rede consumida": "mains water consumed",
    "água extravasada": "water overflowed", "dias de atendimento pleno": "days of full supply",
    "dias de atendimento parcial": "days of partial supply", "dias de atendimento nulo": "days of no supply",
    "demanda pluvial pretendida": "intended rainwater demand", "volume anual poupado": "annual volume saved",
    # cap07
    "Limiar declarado": "Declared threshold", "Volume ideal": "Ideal volume", "Potencial": "Potential",
    "potencial de economia": "saving potential", "preço da cisterna de concreto": "price of the concrete cistern",
    "massa de concreto": "mass of concrete", "carbono incorporado do sistema": "embodied carbon of the system",
    "razão de preço": "price ratio", "ganho de potencial": "potential gain",
    "Volume": "Volume", "Ganho sobre o anterior": "Gain over the previous one",
    "Ganho por m³ acrescentado": "Gain per added m³", "Extravasado": "Overflowed", "Dias plenos": "Full days",
    "pontos percentuais": "percentage points",
    # cap08
    "Limiar de acionamento": "Trigger level", "Acionamentos por ano": "Starts per year",
    "Mesmo armazenamento de 5.000 L": "Same storage of 5,000 L", "Um tanque só": "One tank only",
    "4.000 embaixo + 1.000 em cima": "4,000 below + 1,000 above",
    "volume recalcado": "volume pumped", "acionamentos da bomba": "pump starts",
    "horas de bomba": "pump hours", "energia": "energy", "custo da energia": "energy cost",
    "diferença de potencial": "potential difference",
    # cap09
    "Desinfecção": "Disinfection", "CAPEX": "CAPEX", "Custeio anual": "Annual running cost",
    "CO₂e anual": "Annual CO₂e", "Cloração por pastilhas": "Tablet chlorination",
    "Cloração + ultravioleta": "Chlorination + ultraviolet", "Cloração + ozonização": "Chlorination + ozonation",
    "Classe alvo": "Target class", "Recomenda filtração fina?": "Fine filtration recommended?",
    "CAPEX sem": "CAPEX without", "CAPEX com": "CAPEX with",
    "classe 1": "class 1", "classe 2": "class 2", "classe 3": "class 3", "classe 4": "class 4",
    "não": "no", "sim": "yes",
    # cap10
    "A fatura da CASAN": "The CASAN bill", "Consumo": "Consumption",
    "sem o sistema": "without the system", "com o sistema": "with the system", "economia": "saving",
    "Análise de 20 anos": "20-year analysis", "investimento inicial": "initial investment",
    "economia anual com água": "annual saving on water", "custeio anual": "annual running cost",
    "valor presente líquido": "net present value", "taxa interna de retorno": "internal rate of return",
    "payback descontado": "discounted payback",
    # cap11
    "Material da cisterna": "Cistern material", "Massa": "Mass", "Carbono incorporado": "Embodied carbon",
    "Payback de carbono": "Carbon payback", "Emissões líquidas em 20 anos": "Net emissions over 20 years",
    "Preço": "Price", "Polietileno (PEAD)": "Polyethylene (HDPE)", "Concreto armado": "Reinforced concrete",
    "Fibra de vidro": "Glass fibre", "Aço inoxidável": "Stainless steel", "Volume em concreto": "Volume in concrete",
    # cap12
    "VPL": "NPV", "VPL (R$)": "NPV (R$)", "Payback": "Payback", "Saldo de carbono em 20 anos": "Carbon balance over 20 years",
    "Investimento": "Investment", "Critério isolado": "Criterion alone", "Volume que vence": "Winning volume",
    "maior potencial de economia": "largest saving potential",
    "menor payback descontado, desempate pelo VPL": "shortest discounted payback, NPV as tie-breaker",
    "maior saldo de carbono": "largest carbon balance", "compromisso, pesos iguais": "compromise, equal weights",
    "Peso dominante": "Dominant weight", "Segundo colocado": "Runner-up", "pesos iguais": "equal weights",
    "técnico, 60%": "technical, 60%", "econômico, 60%": "economic, 60%", "ambiental, 60%": "environmental, 60%",
    # cap14
    "Cidade": "City", "Chuva anual": "Annual rain", "Dias com chuva": "Days with rain",
    "Razão entre o mês mais e o menos chuvoso": "Ratio between the wettest and the driest month",
    "Potencial com 4.000 L": "Potential with 4,000 L",
    # cap20
    "Premissa": "Assumption", "Baixa": "Low", "Provável": "Likely", "Alta": "High",
    "VPL em 20 anos": "NPV over 20 years", "Payback descontado": "Discounted payback",
    "reajuste das tarifas de água e esgoto, % ao ano": "water and sewage tariff escalation, % per year",
    "taxa mínima de atratividade, % ao mês": "minimum attractive rate of return, % per month",
    "consumo per capita, L/hab·dia": "per capita consumption, L/person·day",
    "fração atendível, %": "rainwater-suppliable fraction, %",
    "preço da cisterna, % do orçamento": "cistern price, % of the quotation",
    # cap23
    "Dia": "Day", "Chuva": "Rain", "Descarte": "First flush", "Chuva efetiva": "Effective rain",
    "Captado": "Collected", "Demanda pluvial": "Rainwater demand", "Consumido": "Consumed",
    "No reservatório": "In the tank", "Atendimento": "Supply", "nulo": "none", "pleno": "full",
    "parcial": "partial", "soma": "sum",
    "Verificação do fechamento": "Closure check", "Litros": "Litres",
    "captado no período": "collected in the period", "menos o extravasado": "minus the overflow",
    "menos o consumido": "minus the consumption", "menos o que ficou no reservatório": "minus what stayed in the tank",
    "resíduo": "residual", "Indicador dos dez dias": "Ten-day indicator",
    "média diária de pluvial consumida": "daily mean of rainwater consumed",
    "média diária de potável consumida": "daily mean of potable water consumed",
    "média diária extravasada": "daily mean overflow",
    "Dado de entrada": "Input", "área de captação": "catchment area",
    "coeficiente de escoamento": "runoff coefficient", "lâmina de descarte": "first-flush depth",
    "demanda total": "total demand", "fração atendível por água pluvial": "fraction suppliable by rainwater",
    "volume do reservatório inferior": "lower tank volume", "reservatório superior": "upper tank",
    "não há": "none", "2,0 mm, em todo evento": "2.0 mm, on every event",
    "A série de chuva dos dez dias, em milímetros:": "The rainfall series of the ten days, in millimetres:",
    # cap24
    "Método": "Method", "Regra": "Rule", "Potencial simulado": "Simulated potential",
    "prático alemão": "German practical", "6% do menor entre oferta e demanda anuais": "6% of the smaller of annual supply and demand",
    "Rippl, série mensal": "Rippl, monthly series", "maior déficit acumulado, meses": "largest cumulative deficit, months",
    "Azevedo Neto, T = 1 mês": "Azevedo Neto, T = 1 month", "Rippl, série diária": "Rippl, daily series",
    "maior déficit acumulado, dias": "largest cumulative deficit, days", "prático inglês": "English practical",
    "simulação diária, ganho marginal de 1 %/m³": "daily simulation, marginal gain of 1 %/m³",
    "varredura": "sweep", "Fração de armazenamento S/(A·R)": "Storage fraction S/(A·R)",
    "Passo recomendado por Fewkes e Butler": "Time step recommended by Fewkes and Butler",
    "horário": "hourly", "diário": "daily",
    # cap28
    "Modelo": "Model", "Controle": "Control", "Vazão da curva a 18 m.c.a.": "Curve flow at 18 m head",
    "Horas por ano": "Hours per year", "kWh por ano": "kWh per year", "kWh/m³": "kWh/m³",
    "kWh por ano a 24 m.c.a.": "kWh per year at 24 m head", "pressostato": "pressure switch",
    "fluxostato": "flow switch", "eletrônico": "electronic", "não alcança": "does not reach",
    # cap30
    "Item": "Item", "Incorporado": "Embodied", "Parcela do incorporado": "Share of embodied", "Anual": "Annual",
    "cisterna de 4.000 L, polietileno": "4,000 L cistern, polyethylene",
    "caixa superior de 1.000 L, polietileno": "1,000 L upper tank, polyethylene",
    "tubulação de PVC, DN 100 mm": "PVC piping, DN 100 mm", "tubulação de PVC, DN 32 mm": "PVC piping, DN 32 mm",
    "tubulação de PVC, DN 25 mm": "PVC piping, DN 25 mm", "duas motobombas de meio CV": "two half-hp pump sets",
    "descarte inicial: reservatório de 300 L e separador de folhas": "first flush: 300 L chamber and leaf separator",
    "energia do recalque": "pumping energy", "cloração por pastilhas": "tablet chlorination",
    "água potável evitada": "potable water avoided", "total": "total",
    # cap32
    "Escore TOPSIS": "TOPSIS score", "Posição TOPSIS": "TOPSIS rank",
    "Primeiro lugar no SMAA-VIKOR, b¹": "First rank in SMAA-VIKOR, b¹",
    # cap38
    "Versão": "Version", "Data": "Date", "O que trouxe": "What it brought",
    "Correções que alteram resultados": "Fixes that change results",
    "Primeiro lançamento público do Triton: o motor de simulação reescrito em Python e separado da interface, com avaliação de ciclo de vida, linha de tratamento, decisão multicritério, planta 3D da tubulação e a documentação em três formatos.":
        "First public release of Triton: the simulation engine rewritten in Python and separated from the interface, with life cycle assessment, treatment line, multi-criteria decision, 3D piping layout and the documentation in three formats.",
}

#: Units and short words inside numeric cells, applied after the number conversion.
UNIDADES = [
    ("L/dia", "L/day"), ("m³/ano", "m³/year"), ("m³/mês", "m³/month"), ("kg/ano", "kg/year"),
    ("h/ano", "h/year"), ("kWh/ano", "kWh/year"), ("/ano", "/year"), ("% ao ano", "% per year"),
    (" por ano", " per year"), (" anos", " years"), (" pontos", " points"), ("não retorna", "no payback"),
]

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

_NUMERO = re.compile(r"(?<![\w.,])(-?\d{1,3}(?:[\u00a0.]\d{3})+(?:,\d+)?|-?\d+,\d+)(?![\w])")
_ORDINAL = re.compile(r"\b(\d+)º")
_PORTUGUES = re.compile(r"[ãõçâêôáéíóú]|\b(de|da|dos|das|com|sem|por|para|os|em|na|ao|ano|anos|dia|dias|mês|não|sim)\b",
                        re.IGNORECASE)
#: Proper names that keep their accents.
_NOMES_PROPRIOS = ("Florianópolis", "São Paulo", "Brasília", "Azevedo Neto")


def numero_em_ingles(m):
    """Portuguese uses a point or a no-break space for thousands and a comma for decimals."""
    inteiro, sep, decimal = m.group(1).partition(",")
    inteiro = inteiro.replace("\u00a0", ",").replace(".", ",")
    return inteiro + ("." + decimal if sep else "")


def _ordinal(m):
    n = int(m.group(1))
    sufixo = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{sufixo}"


def _data(texto):
    m = re.fullmatch(r"(\d{1,2}) de (\w+) de (\d{4})", texto)
    if m and m.group(2).lower() in MESES:
        return f"{int(m.group(1))} {MONTHS[MESES.index(m.group(2).lower())]} {m.group(3)}"
    return None


def _residuo(texto):
    limpo = texto
    for nome in _NOMES_PROPRIOS:
        limpo = limpo.replace(nome, "")
    limpo = re.sub(r"`[^`]*`", "", limpo)
    return _PORTUGUES.search(limpo)


def traduzir_celula(celula, faltam):
    bruto = celula.strip()
    if not bruto or bruto in ("—", "−", "-"):
        return celula
    negrito = bruto.startswith("**") and bruto.endswith("**") and len(bruto) > 4
    miolo = bruto[2:-2] if negrito else bruto
    convertido = _NUMERO.sub(numero_em_ingles, miolo)
    if miolo in CELULAS:
        novo = CELULAS[miolo]
    elif convertido in CELULAS:
        novo = CELULAS[convertido]
    elif _data(miolo):
        novo = _data(miolo)
    else:
        novo = _NUMERO.sub(numero_em_ingles, miolo)
        novo = _ORDINAL.sub(_ordinal, novo)
        for pt, en in UNIDADES:
            novo = novo.replace(pt, en)
        novo = novo.replace(" a R$", " to R$").replace(" a ", " to ")
        if _residuo(novo):
            faltam.append(miolo)
    if negrito:
        novo = f"**{novo}**"
    return " " + novo + " "


def traduzir(texto, faltam):
    saida = []
    for linha in texto.split(NL):
        m = re.match(r"^<!--\s*tabela:\s*(?:\*\*Tabela \d+\*\* — )?(.+?)\s*-->\s*$", linha)
        if m:
            legenda = m.group(1)
            if legenda not in LEGENDAS:
                faltam.append(legenda)
                saida.append(linha)
            else:
                numerada = re.match(r"^<!--\s*tabela:\s*\*\*Tabela (\d+)\*\*", linha)
                prefixo = f"**Table {numerada.group(1)}** — " if numerada else ""
                saida.append(f"<!-- tabela: {prefixo}{LEGENDAS[legenda]} -->")
            continue
        if linha.startswith("|"):
            if re.match(r"^\|[\s:\-|]+\|$", linha.rstrip()):
                saida.append(linha)
                continue
            celulas = linha.strip().strip("|").split("|")
            saida.append("|" + "|".join(traduzir_celula(c, faltam) for c in celulas) + "|")
            continue
        if linha.strip():
            if linha.strip() in CELULAS:
                saida.append(CELULAS[linha.strip()])
            else:
                faltam.append(linha.strip())
                saida.append(linha)
            continue
        saida.append(linha)
    return NL.join(saida)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    faltam = []
    nomes = sorted(n for n in os.listdir(ORIGEM) if n.endswith(".md"))
    for nome in nomes:
        texto = open(os.path.join(ORIGEM, nome), encoding="utf-8").read()
        novo = traduzir(texto, faltam)
        with open(os.path.join(DESTINO, nome), "w", encoding="utf-8", newline="") as f:
            f.write(novo)
    for nome in os.listdir(DESTINO):
        if nome.endswith(".md") and nome not in nomes:
            os.remove(os.path.join(DESTINO, nome))
    if faltam:
        print("traduzir_tabelas: sem tradução (acrescente em manual/en/traduzir_tabelas.py):")
        for f in dict.fromkeys(faltam):
            print("  " + f)
        return 1
    print(f"traduzir_tabelas: {len(nomes)} arquivos em manual/en/partes/_tabelas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
