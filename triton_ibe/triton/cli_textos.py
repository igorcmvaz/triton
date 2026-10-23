# -*- coding: utf-8 -*-
"""Textos da linha de comando por edição.

Os textos-fonte da CLI estão em português do Brasil. Fora da Edição Brasil, a ajuda (``--help``)
e as mensagens fixas passam por aqui: a Internacional recebe o inglês, e a Portugal o glossário
de português de Portugal. A Brasil não muda nada: ``t`` devolve o texto como veio.

Só estão aqui os textos que o usuário lê antes de rodar um estudo (ajuda e mensagens de criação de
modelos). Os relatórios impressos pela análise seguem o idioma do código-fonte.
"""

from __future__ import annotations

from triton.core.edition import is_int_edition, is_ibe_edition

_EN = {
    'Triton CLI: simulação, economia, ACV, TOPSIS e automação reproduzível.':
        'Triton CLI: simulation, economics, LCA, TOPSIS and reproducible automation.',
    'Simula; padrão técnico compatível com o legado': 'Simulates; technical analysis by default (legacy-compatible)',
    'Executa cadeia completa de análises': 'Runs the complete chain of analyses',
    'Atalho legado para análise econômica': 'Legacy shortcut for the economic analysis',
    'Valida a estrutura e as premissas de um projeto': 'Validates the structure and assumptions of a project',
    'Cria um template .triton estruturado e editável': 'Creates a structured, editable .triton template',
    'Destino .triton': '.triton destination',
    'Arquivo de chuva de referência': 'Reference rainfall file',
    'Incorpora a série no .triton': 'Embeds the series in the .triton file',
    'Cria catálogo JSON de premissas ou de climas': 'Creates a JSON catalogue of assumptions or climates',
    'Destino JSON do catálogo': 'JSON destination of the catalogue',
    'Combina premissas de edifício com catálogo climático': 'Combines building assumptions with a climate catalogue',
    'Catálogo JSON com schema triton-premises-catalog': 'JSON catalogue with the triton-premises-catalog schema',
    'Catálogo JSON com schema triton-climate-catalog': 'JSON catalogue with the triton-climate-catalog schema',
    'Oculta a barra de progresso e ETA': 'Hides the progress bar and ETA',
    'Executa arquivos .triton em lista, pasta de chuva ou matriz fatorial declarada no projeto':
        'Runs .triton files from a list, a rainfall folder or a factorial matrix declared in the project',
    'Arquivos .triton/.json ou pastas contendo arquivos .triton': '.triton/.json files or folders containing .triton files',
    'Pasta de séries CSV/TXT/DAT; combina cada projeto com cada série': 'Folder of CSV/TXT/DAT series; pairs each project with each series',
    'Ignora o bloco cli_factorial dos projetos': 'Ignores the cli_factorial block of the projects',
    'Procura projetos e séries também nas subpastas': 'Also looks for projects and series in subfolders',
    'Executa cenários de uma planilha CSV/XLSX': 'Runs the scenarios of a CSV/XLSX spreadsheet',
    'Planilha de cenários': 'Scenario spreadsheet',
    'Projeto .triton/CSV com parâmetros econômicos e ambientais base': '.triton/CSV project with the base economic and environmental parameters',
    'Arquivo de saída': 'Output file',
    'Propaga incertezas por Monte Carlo para uma decisão de volume': 'Propagates uncertainty by Monte Carlo to a volume decision',
    'Projeto CSV, .triton ou JSON': 'CSV project, .triton or JSON',
    'Volume analisado; padrão: ótimo técnico do caso-base': 'Volume analysed; default: technical optimum of the base case',
    'CV percentual da chuva': 'Rainfall coefficient of variation, %',
    'CV percentual da área': 'Area coefficient of variation, %',
    'CV percentual da demanda': 'Demand coefficient of variation, %',
    'CV percentual de CAPEX': 'CAPEX coefficient of variation, %',
    'Responde de quantos anos de chuva este projeto precisa (Geraldi e Ghisi)':
        'Answers how many years of rainfall this project needs (Geraldi and Ghisi)',
    'Maior volume da grade, em litros': 'Largest volume of the grid, in litres',
    'Passo da grade, em litros': 'Grid step, in litres',
    'Limiar de ganho marginal que define o volume ideal, em %%/m³': 'Marginal-gain threshold that defines the ideal volume, in %%/m³',
    'Tolerância do potencial, em pontos percentuais': 'Tolerance of the potential, in percentage points',
    'Tolerância do volume ideal, em passos da grade': 'Tolerance of the ideal volume, in grid steps',
    'Frequência mínima de resultados semelhantes, em %%': 'Minimum frequency of similar results, in %%',
    'Janelas sorteadas por comprimento; sem isto, usa todas': 'Windows drawn for each length; without this, all of them are used',
    'Sorteia o consumo diário e devolve o desempenho como faixa (Silva e Ghisi)':
        'Draws the daily consumption and returns the performance as a range (Silva and Ghisi)',
    'CV do consumo de um dia para o outro, em %%': 'Coefficient of variation of consumption from one day to the next, in %%',
    'Incerteza do nível médio do consumo, em %%; é o que move o resultado': 'Uncertainty of the mean consumption level, in %%; this is what moves the result',
    'Probabilidade de dia sem consumo, em %%': 'Probability of a day without consumption, in %%',
    'Também apura o volume ideal de cada realização': 'Also finds the ideal volume of each realisation',
    'Modulação probabilística: refaz o estudo com as premissas escolhidas sorteadas':
        'Probabilistic modulation: repeats the study drawing the chosen assumptions at random',
    'Realizações; padrão: o salvo no projeto ou 1000': 'Realisations; default: the one saved in the project, or 1000',
    'Semente; padrão: a salva no projeto ou 42': 'Seed; default: the one saved in the project, or 42',
    'Qualquer variável do catálogo (per_capita_l_dia, pessoas, fracao_nao_potavel_pct, demanda_externa_l_dia, area_m2, coef_escoamento, descarte_mm, fator_chuva, fator_tarifa, reajuste_tarifa_pct, tma_pct_mes, fator_investimento, tarifa_energia); pode ser repetida. Ex.: --var fator_chuva=normal:1:0,1':
        'Any variable of the catalogue (per_capita_l_dia, pessoas, fracao_nao_potavel_pct, demanda_externa_l_dia, area_m2, coef_escoamento, descarte_mm, fator_chuva, fator_tarifa, reajuste_tarifa_pct, tma_pct_mes, fator_investimento, tarifa_energia); may be repeated. E.g. --var fator_chuva=normal:1:0.1',
    'Lista o catálogo e sai': 'Lists the catalogue and exits',
    'Variação de um dia para o outro, em %% (padrão 0)': 'Variation from one day to the next, in %% (default 0)',
    'Oculta o progresso': 'Hides the progress',
    'Projeto CSV legado, .triton ou JSON estruturado': 'Legacy CSV project, .triton or structured JSON',
    'Força um volume de cisterna inferior (L)': 'Forces a lower tank volume (L)',
    'Pesos TOPSIS: técnico,econômico,ambiental': 'TOPSIS weights: technical,economic,environmental',
    'Substitui a chuva do projeto por este arquivo': 'Replaces the project rainfall with this file',
    'Data inicial dd/mm/aaaa; necessária para sazonalidade mensal': 'Start date dd/mm/yyyy; needed for monthly seasonality',
    'Sobrescreve campo do projeto; pode ser repetido': 'Overrides a project field; may be repeated',
    'Arquivo de saída obrigatório para json/csv/html/xlsx': 'Output file, required for json/csv/html/xlsx',
    'Amostra N combinações de pesos TOPSIS e informa a frequência vencedora': 'Samples N combinations of TOPSIS weights and reports the winning frequency',
    'Semente para análises estocásticas': 'Seed for stochastic analyses',
    # mensagens fixas de main()
    'Template .triton criado em:': '.triton template created at:',
    'Catálogo de': 'Catalogue of',
    'criado em:': 'created at:',
    'Projeto válido: estrutura, chuva e premissas essenciais verificadas.':
        'Valid project: structure, rainfall and essential assumptions checked.',
    'Erro:': 'Error:',
    'Distribuição do consumo per capita, L/hab.dia': 'Distribution of the per-capita consumption, L/person/day',
    'Distribuição do número de pessoas': 'Distribution of the number of people',
    'Distribuição do fração não potável interna, %%': 'Distribution of the indoor non-potable fraction, %%',
    'normal:média:desvio, lognormal:média:desvio, triangular:mín:moda:máx, uniforme:mín:máx ou fixo':
        'normal:mean:deviation, lognormal:mean:deviation, triangular:min:mode:max, uniform:min:max or fixed',
    # relatório impresso
    'alternativa(s)': 'alternative(s)',
    'Volume técnico indicado:': 'Recommended technical volume:',
    'de economia': 'savings',
    'Melhor alternativa econômica (Menor Payback):': 'Best economic alternative (shortest payback):',
    'VPL': 'NPV',
    'Melhor alternativa ambiental:': 'Best environmental alternative:',
    'em': 'in',
    'simulações': 'simulations',
    'relatório de análise': 'analysis report',
    'Gerado:': 'Generated:',
    'Valores monetários em:': 'Monetary values in:',
    '(moeda do projeto)': '(project currency)',
    'não declarada': 'not declared',
    # catálogos de exemplo
    'Residência base': 'Base residence',
}


def t(texto: str) -> str:
    """O texto da edição ativa: o original na Brasil, o inglês na Internacional, o glossário na Portugal."""
    if is_int_edition():
        return _EN.get(texto, texto)
    if is_ibe_edition():
        from triton.ui.portugues_de_portugal import para_portugal
        return para_portugal(texto)
    return texto
