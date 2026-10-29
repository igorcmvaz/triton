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
    'Resultado salvo em:': 'Result saved to:',
    'Aviso:': 'Warning:',
    'Saídas consolidadas:': 'Consolidated outputs:',
    '- triton-matriz-resumo.csv (uma decisão por combinação)': '- triton-matriz-resumo.csv (one decision per combination)',
    '- triton-matriz-alternativas.csv (todos os volumes)': '- triton-matriz-alternativas.csv (all volumes)',
    '- triton-matriz-detalhado.json (resultados auditáveis completos)': '- triton-matriz-detalhado.json (full auditable results)',
    '- triton-matriz-painel.html (visualização consolidada)': '- triton-matriz-painel.html (consolidated view)',
    'Amostras salvas em:': 'Samples saved to:',
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
    # variáveis do estudo probabilístico
    'Consumo per capita': 'Per-capita consumption',
    'Número de pessoas': 'Number of people',
    'Fração não potável interna': 'Indoor non-potable fraction',
    'Demanda externa': 'Outdoor demand',
    'Área de captação': 'Catchment area',
    'Coeficiente de escoamento': 'Runoff coefficient',
    'Lâmina de descarte': 'First-flush depth',
    'Fator da chuva': 'Rainfall factor',
    'Fator das tarifas de água e esgoto': 'Water and sewage tariff factor',
    'Fator do esgoto': 'Sewage factor',
    'Reajuste tarifário': 'Tariff escalation',
    'Tarifa de energia': 'Energy tariff',
    'Reajuste da energia': 'Energy escalation',
    'Fator do investimento': 'Investment factor',
    'Fator do preço da cisterna': 'Cistern price factor',
    'Fator do custeio (O&M)': 'O&M cost factor',
    'Inflação do custeio': 'O&M inflation',
    'Taxa mínima de atratividade': 'Minimum acceptable rate of return',
    'Período de análise': 'Analysis period',
    'Fator da emissão da água potável': 'Potable-water emission factor',
    'Fator da emissão da rede elétrica': 'Grid emission factor',
    'Demanda': 'Demand',
    'Captação': 'Catchment',
    'Chuva': 'Rainfall',
    'Custos': 'Costs',
    'Fluxo de caixa': 'Cash flow',
    'Tarifas': 'Tariffs',
    'Ambiente': 'Environment',
    'pessoas': 'people',
    'anos': 'years',
    'L/hab.dia': 'L/person.day',
    'L/dia': 'L/day',
    '% ao mês': '% per month',
    '% por período': '% per period',
    # catálogos de exemplo
    'Residência base': 'Base residence',
}


# ── triton estudo (estudos em lote por JSON): inglês da Internacional; Portugal passa pelo glossário ─────
_EN.update({
    'Estudos em lote por JSON: organiza, executa e relata vários edifícios (tabelas para artigos)':
        'Batch studies from JSON: organises, runs and reports many buildings (tables for papers)',
    'Estudos em lote por JSON. Um estudo.json reúne projeto base, casos, substituições de parâmetros, análise e saídas; o programa executa todos os casos e escreve CSV, JSON, Markdown, LaTeX e XLSX.':
        'Batch studies from JSON. A study.json gathers the base project, cases, parameter substitutions, analysis and outputs; the program runs every case and writes CSV, JSON, Markdown, LaTeX and XLSX.',
    'Cria a pasta do estudo com um estudo.json esqueleto (sem valores inventados)':
        'Creates the study folder with a skeleton estudo.json (no invented values)',
    'Valida o estudo.json: esquema, apelidos, arquivos e projetos': 'Validates estudo.json: schema, aliases, files and projects',
    'Executa todos os casos do estudo e escreve as tabelas': 'Runs every case of the study and writes the tables',
    'Refaz as tabelas a partir da pasta de saída, sem recalcular': 'Rebuilds the tables from the output folder, without recomputing',
    'Executa vários estudo*.json de uma pasta e compara as tipologias': 'Runs several estudo*.json files of a folder and compares the typologies',
    'Preenche um modelo de texto (.md) com os números reais dos resultados': 'Fills a text template (.md) with the real numbers of the results',
    'Imprime o esquema JSON (JSON Schema) do estudo.json': 'Prints the JSON Schema of estudo.json',
    'Lista os apelidos de parâmetros e as métricas disponíveis': 'Lists the parameter aliases and the available metrics',
    'Pasta do estudo (criada se não existir)': 'Study folder (created if missing)',
    'escolar, comercial, residencial-unifamiliar, residencial-multifamiliar, hospitalar ou aeroportuario':
        'escolar (school), comercial (commercial), residencial-unifamiliar, residencial-multifamiliar, hospitalar (hospital) or aeroportuario (airport)',
    'Sobrescreve um estudo.json existente': 'Overwrites an existing estudo.json',
    'Arquivo estudo.json': 'The estudo.json file',
    'Só a estrutura do JSON, sem abrir projetos nem séries de chuva': 'Only the JSON structure, without opening projects or rainfall series',
    'Pasta de saída (resultados.csv, resultados.json, tabela.md, tabela.tex, resumo.md)':
        'Output folder (resultados.csv, resultados.json, tabela.md, tabela.tex, resumo.md)',
    'Ignora os casos já calculados e inalterados': 'Skips the cases already computed and unchanged',
    'Refaz todos os casos numa pasta de saída que já tem resultados': 'Recomputes every case in an output folder that already has results',
    'Casos em N processos (o resultado não muda)': 'Cases in N processes (the result does not change)',
    'Pasta de saída de «triton estudo run»': 'Output folder of «triton estudo run»',
    'Outro estudo.json (por exemplo com outras métricas ou casas decimais) no lugar da cópia da pasta':
        'Another estudo.json (for example with other metrics or decimal places) in place of the copy in the folder',
    'Idioma das tabelas (padrão: o do estudo)': 'Language of the tables (default: the study\'s)',
    'Pasta com os arquivos estudo*.json': 'Folder with the estudo*.json files',
    'Pasta de saída (uma subpasta por estudo, mais comparativo.*)': 'Output folder (one subfolder per study, plus comparativo.*)',
    'Procura estudo*.json também nas subpastas': 'Also looks for estudo*.json in subfolders',
    'Idioma do comparativo (padrão: o do primeiro estudo)': 'Language of the comparison (default: the first study\'s)',
    'Arquivo .md com marcadores de chaves duplas: metrica:caso, metrica:@min, metrica:@max, metrica:@media, n_casos':
        '.md file with double-brace markers: metrica:caso, metrica:@min, metrica:@max, metrica:@media, n_casos',
    'Arquivo de saída (padrão: texto.md na pasta de saída; «-» imprime)': 'Output file (default: texto.md in the output folder; «-» prints)',
    'Termina com código 1 se algum marcador ficar sem resultado (XX)': 'Exits with code 1 if any marker is left without a result (XX)',
    'Idioma dos números (padrão: o do estudo)': 'Language of the numbers (default: the study\'s)',
    'Grava no arquivo em vez de imprimir': 'Writes to the file instead of printing',
    'Informe um inteiro positivo.': 'Give a positive integer.',
    'tipologia desconhecida: {0}. Use: {1}': 'unknown typology: {0}. Use: {1}',
    '{0} já existe; use --forcar para sobrescrevê-lo': '{0} already exists; use --forcar to overwrite it',
    'Estudo criado em: {0}': 'Study created at: {0}',
    'Próximos passos: preencha o estudo.json, execute «triton estudo validate» e depois «triton estudo run».':
        'Next steps: fill in estudo.json, run «triton estudo validate» and then «triton estudo run».',
    '# Projetos e séries de chuva do estudo\n\nColoque aqui os arquivos .triton (um por edifício ou um só, como projeto base) e as séries diárias de chuva (.csv). O estudo.json refere estes arquivos por caminho relativo a esta pasta, por exemplo casos/predio.triton.\n\nNada neste esqueleto foi preenchido pelo programa: substitua os «XX» e os null pelos dados do seu estudo e indique a fonte de cada um.\n':
        '# Projects and rainfall series of the study\n\nPut here the .triton files (one per building, or a single one as the base project) and the daily rainfall series (.csv). The estudo.json cites them by a path relative to this folder, for example casos/building.triton.\n\nNothing in this skeleton was filled in by the program: replace the «XX» and the null values with the data of your study and record the source of each.\n',
    'Estudo válido: {0} casos, tipologia {1}, análise {2}.': 'Valid study: {0} cases, typology {1}, analysis {2}.',
    'Estudo concluído: {0} calculados, {1} ignorados, {2} com erro.': 'Study finished: {0} computed, {1} skipped, {2} with errors.',
    'Saídas em: {0}': 'Outputs in: {0}',
    'Casos com erro: {0}': 'Cases with errors: {0}',
    'Tabelas refeitas em: {0}': 'Tables rebuilt in: {0}',
    'Lote concluído: {0} estudos, {1} casos calculados, {2} ignorados, {3} com erro.':
        'Batch finished: {0} studies, {1} cases computed, {2} skipped, {3} with errors.',
    'Modelo não encontrado: {0}': 'Template not found: {0}',
    'Texto gravado em: {0}': 'Text written to: {0}',
    '{0} marcador(es) sem resultado, deixados como «XX»: {1}': '{0} marker(s) without a result, left as «XX»: {1}',
    'Esquema gravado em: {0}': 'Schema written to: {0}',
    # mensagens do núcleo
    'estudo inválido:': 'invalid study:',
    '# Modelo de texto: resumo para congresso\n\nEste estudo avaliou {{{{n_casos}}}} edifícios (tipologia: {0}). Com o reservatório no volume de cada caso, a economia de água potável variou de {{{{economia_agua_potavel_pct:@min}}}}% a {{{{economia_agua_potavel_pct:@max}}}}% (mediana de {{{{economia_agua_potavel_pct:@mediana}}}}%). XX\n\nSubstitua o texto livre pela sua redação; cada marcador vira o número real depois de «triton estudo texto». Onde faltar resultado fica «XX».\n':
        '# Text template: conference abstract\n\nThis study assessed {{{{n_casos}}}} buildings (typology: {0}). With the tank at the volume of each case, potable water saving ranged from {{{{economia_agua_potavel_pct:@min}}}}% to {{{{economia_agua_potavel_pct:@max}}}}% (median {{{{economia_agua_potavel_pct:@mediana}}}}%). XX\n\nReplace the free text with your own wording; each marker becomes the real number after «triton estudo texto». Where a result is missing, «XX» stays.\n',
    'idioma desconhecido: {0}. Use auto, pt-BR, pt-PT, en, es ou zh.': 'unknown language: {0}. Use auto, pt-BR, pt-PT, en, es or zh.',
    'caminho desconhecido «{0}»: um caminho pontilhado começa por uma seção do .triton ({1}) ou por config.<campo>':
        'unknown path «{0}»: a dotted path starts with a section of the .triton file ({1}) or with config.<field>',
    'Apelidos: {0}. Veja também «triton estudo apelidos».': 'Aliases: {0}. See also «triton estudo apelidos».',
    'Esqueleto de «triton estudo init»: nenhum valor foi preenchido pelo programa. Substitua os «XX» e os null pelos dados do seu estudo (com a fonte de cada um) e execute «triton estudo validate». Chaves iniciadas por _ são comentários.':
        'Skeleton from «triton estudo init»: the program filled in no value. Replace the «XX» and null entries with the data of your study (with the source of each) and run «triton estudo validate». Keys starting with _ are comments.',
    'Apelidos de substituição (em substituicoes; valem também campos do projeto e caminhos pontilhados do .triton):':
        'Substitution aliases (in substituicoes; project fields and dotted paths of the .triton file are also accepted):',
    'Métricas (em saidas.metricas):': 'Metrics (in saidas.metricas):',
    ' Quis dizer «{0}»?': ' Did you mean «{0}»?',
    'ainda não preenchido (use um número; «XX» e null são lacunas)': 'not filled in yet (give a number; «XX» and null are blanks)',
    '{0}: esperado um objeto JSON': '{0}: a JSON object is expected',
    'esquema: esperado {{"nome": "{0}", "versao": {1}}}': 'esquema: expected {{"nome": "{0}", "versao": {1}}}',
    'analise.volume = «topsis» exige analise.tipo = «all» (ou «topsis»)': 'analise.volume = «topsis» requires analise.tipo = «all» (or «topsis»)',
    'casos: lista não vazia de casos': 'casos: a non-empty list of cases',
    'Estudo não encontrado: {0}': 'Study not found: {0}',
    'não foi possível escolher o volume do caso': 'could not choose the volume of the case',
    'a pasta de saída já tem resultados; use --retomar para ignorar os casos prontos ou --sobrescrever para refazê-los':
        'the output folder already has results; use --retomar to skip the finished cases or --sobrescrever to redo them',
    '--paralelo deve ser um inteiro positivo': '--paralelo must be a positive integer',
    'erro: {0}': 'error: {0}',
    '{0} não tem estudo.json; é a pasta de saída de «triton estudo run»?': '{0} has no estudo.json; is it the output folder of «triton estudo run»?',
    'a pasta de saída não tem resultados de casos; execute «triton estudo run» primeiro': 'the output folder has no case results; run «triton estudo run» first',
    'Pasta não encontrada: {0}': 'Folder not found: {0}',
    'nenhum estudo*.json em {0} (use --recursivo para procurar nas subpastas)': 'no estudo*.json in {0} (use --recursivo to search the subfolders)',
    'os estudos não têm nenhuma métrica em comum para comparar': 'the studies have no metric in common to compare',
    'ids de estudo repetidos no lote: {0}': 'study ids repeated in the batch: {0}',
    'Estudo {0} ({1} casos)': 'Study {0} ({1} cases)',
    'tipologia: só rótulo e estrutura; os números vêm dos casos. usuarios, nesta tipologia: {0}':
        'tipologia: label and structure only; the numbers come from the cases. usuarios, in this typology: {0}',
    'Caminho do .triton base, relativo a este arquivo (ou {{"modelo": "edicao"}} para partir do modelo da edição, caso em que cada caso informa área, demanda, fração e chuva). Um caso pode usar outro projeto no campo «projeto».':
        'Path of the base .triton, relative to this file (or {{"modelo": "edicao"}} to start from the edition template, in which case each case gives area, demand, share and rainfall). A case may use another project in its «projeto» field.',
    'Tudo o que vale para todos os casos: substituicoes e clima. O que o caso declara vence o padrão.':
        'Everything that holds for all cases: substituicoes and clima. What a case declares wins over the default.',
    'tipo: technical, economic ou all. volume: otimo_tecnico, topsis ou um volume em litros.':
        'tipo: technical, economic or all. volume: otimo_tecnico, topsis or a volume in litres.',
    'formatos: csv, json, md, tex, xlsx. Métricas e apelidos: «triton estudo apelidos».': 'formatos: csv, json, md, tex, xlsx. Metrics and aliases: «triton estudo apelidos».',
    'moeda do projeto': 'project currency',
    'esperado um número, recebido {0!r}': 'a number is expected, got {0!r}',
    'percentual fora de [0, 100]: {0}': 'percentage outside [0, 100]: {0}',
    'deve ser {0} {1}, recebido {2}': 'must be {0} {1}, got {2}',
    'deve ser no máximo {0}, recebido {1}': 'must be at most {0}, got {1}',
    'esperada uma data dd/mm/aaaa, recebido {0!r}': 'a date dd/mm/yyyy is expected, got {0!r}',
    'regra_phi aceita um número de 0 a 1 ou «triton»': 'regra_phi accepts a number from 0 to 1 or «triton»',
    'apelido desconhecido «{0}».': 'unknown alias «{0}».',
    '{0}: «{1}» e «{2}» definem o mesmo parâmetro; informe só um deles': '{0}: «{1}» and «{2}» set the same parameter; give only one of them',
    'o estudo deve ser um objeto JSON': 'the study must be a JSON object',
    'esquema.versao: a versão {0!r} não é suportada; esta edição do Triton lê a versão {1}':
        'esquema.versao: version {0!r} is not supported; this edition of Triton reads version {1}',
    'estudo.id: obrigatório, só letras, números, ponto, hífen e sublinhado (até 64 caracteres)':
        'estudo.id: required; letters, digits, dot, hyphen and underscore only (up to 64 characters)',
    'estudo.titulo: ainda não preenchido': 'estudo.titulo: not filled in yet',
    'estudo.autores: esperada uma lista de textos': 'estudo.autores: a list of texts is expected',
    'analise.tipo: «{0}» desconhecido. Use: {1}': 'analise.tipo: «{0}» is unknown. Use: {1}',
    'analise.semente: esperado um inteiro': 'analise.semente: an integer is expected',
    'saidas.idioma: «{0}» desconhecido. Use: {1}': 'saidas.idioma: «{0}» is unknown. Use: {1}',
    'saidas.orientacao: use {0}': 'saidas.orientacao: use {0}',
    '{0}.id: obrigatório, só letras, números, ponto, hífen e sublinhado (até 64 caracteres)':
        '{0}.id: required; letters, digits, dot, hyphen and underscore only (up to 64 characters)',
    '{0}: id repetido (igual ao do caso {1})': '{0}: repeated id (same as case {1})',
    '{0}.nome: ainda não preenchido (usado: {1})': '{0}.nome: not filled in yet (using: {1})',
    '{0}: sem projeto. Informe projeto_base ou o campo «projeto» do caso': '{0}: no project. Give projeto_base or the «projeto» field of the case',
    '{0}: arquivo não encontrado: {1}': '{0}: file not found: {1}',
    '{0} não é um JSON válido: {1}': '{0} is not valid JSON: {1}',
    'o campo {0} é verdadeiro/falso; recebido {1!r}': 'the field {0} is true/false; got {1!r}',
    'o caminho «{0}» guarda {1}; o valor dado é {2}': 'the path «{0}» holds {1}; the given value is {2}',
    'Chaves disponíveis: {0}': 'Available keys: {0}',
    'projeto não encontrado: {0}': 'project not found: {0}',
    'arquivo de chuva não encontrado: {0}': 'rainfall file not found: {0}',
    'o projeto usa modulação da demanda: as substituições de demanda e de usuários podem não ter efeito sobre a modulação':
        'the project uses demand modulation: the demand and user substitutions may have no effect on the modulation',
    'pronto, ignorado': 'already done, skipped',
    '{0}: o CLIMBra e o catálogo de tarifas municipais só existem na Edição Brasil; use «arquivo» com a série de chuva': '{0}: CLIMBra and the municipal tariff catalogue exist only in the Brazil edition; use «arquivo» with the rainfall series',
    'o CLIMBra e o catálogo de tarifas municipais só existem na Edição Brasil; use «arquivo» com a série de chuva': 'CLIMBra and the municipal tariff catalogue exist only in the Brazil edition; use «arquivo» with the rainfall series',
    '{0}.modelo: «{1}» desconhecido. Use: {2}': '{0}.modelo: «{1}» unknown. Use: {2}',
    '{0}.cenario: «{1}» desconhecido. Use: {2}': '{0}.cenario: «{1}» unknown. Use: {2}',
    '{0}.ibge: esperado o código IBGE de sete dígitos, entre aspas': '{0}.ibge: expected the seven-digit IBGE code, in quotes',
    '{0}.categoria: «{1}» desconhecida. Use: {2}': '{0}.categoria: «{1}» unknown. Use: {2}',
    '{0}.se_ausente: use «erro» ou «residencial»': '{0}.se_ausente: use «erro» or «residencial»',
    'saidas.gravar_analise: esperado verdadeiro ou falso': 'saidas.gravar_analise: expected true or false',
    '{0}.dimensoes: esperado um objeto com textos ou números': '{0}.dimensoes: expected an object with texts or numbers',
    '{0}: clima.climbra sem «municipio»': '{0}: clima.climbra without «municipio»',
    '{0}: tarifa sem «municipio» (e sem clima.climbra para herdá-lo)': '{0}: tarifa without «municipio» (and no clima.climbra to inherit it from)',
    'expansao: não gerou nenhum caso': 'expansao: generated no case',
    '{0}.uf: esperado texto': '{0}.uf: expected text',
    '{0}.municipios: lista não vazia de municípios': '{0}.municipios: non-empty list of municipalities',
    '{0}.municipio: obrigatório': '{0}.municipio: required',
    '{0}.modelos: «todos» ou uma lista de modelos entre: {1}': '{0}.modelos: «todos» or a list of models among: {1}',
    '{0}.recortes: lista não vazia de recortes (id, cenario, inicio, fim)': '{0}.recortes: non-empty list of slices (id, cenario, inicio, fim)',
    '{0}: informe cenario, inicio e fim': '{0}: give cenario, inicio and fim',
    'município «{0}» não está na base CLIMBra': 'municipality «{0}» is not in the CLIMBra base',
    'município «{0}» não consta na UF {1} do catálogo (nome repetido em outra UF?)': 'municipality «{0}» is not listed under state {1} of the catalogue (same name in another state?)',
    'recorte pedido {0} a {1}; a série do modelo cobre {2} a {3}': 'requested slice {0} to {1}; the model series covers {2} to {3}',
    'sem tabela «{0}» coletada para {1}: usada a residencial do catálogo': 'no «{0}» table collected for {1}: the catalogue residential table was used',
    'sem tarifa «{0}» no catálogo para {1} ({2})': 'no «{0}» tariff in the catalogue for {1} ({2})',
    'tarifa sem município': 'tariff without municipality',
    'marcador inválido: {0}. Use a forma metrica:caso, metrica:@min, metrica:@max, metrica:@media, metrica:@mediana ou n_casos.':
        'invalid marker: {0}. Use the form metrica:caso, metrica:@min, metrica:@max, metrica:@media, metrica:@mediana or n_casos.',
    'esperado um inteiro, recebido {0}': 'an integer is expected, got {0}',
    '{0} parece um percentual; aqui a fração vai de 0 a 1 (0,4 é 40%); para percentual use fracao_pluvial_pct':
        '{0} looks like a percentage; here the fraction goes from 0 to 1 (0.4 is 40%); for a percentage use fracao_pluvial_pct',
    'fração fora de [0, 1]: {0}': 'fraction outside [0, 1]: {0}',
    'data inexistente: {0}': 'nonexistent date: {0}',
    'Chaves aceitas: {0}': 'Accepted keys: {0}',
    '{0}.{1}: ainda não preenchido': '{0}.{1}: not filled in yet',
    'estudo.titulo: esperado texto': 'estudo.titulo: text is expected',
    'estudo.tipologia: «{0}» desconhecida. Use: {1} ou outra.': 'estudo.tipologia: «{0}» is unknown. Use: {1} or outra (other).',
    '{0}: informe «{1}» ou «{2}», não os dois': '{0}: give «{1}» or «{2}», not both',
    'analise.volume: use «otimo_tecnico», «topsis» ou um volume em litros (número ≥ 0)':
        'analise.volume: use «otimo_tecnico», «topsis» or a volume in litres (number ≥ 0)',
    'analise.pesos: três números não negativos (técnico, econômico, ambiental), com soma positiva':
        'analise.pesos: three non-negative numbers (technical, economic, environmental) with a positive sum',
    'saidas.formatos: lista não vazia com {0}': 'saidas.formatos: a non-empty list with {0}',
    'saidas.metricas: lista não vazia de métricas (veja «triton estudo apelidos»)': 'saidas.metricas: a non-empty list of metrics (see «triton estudo apelidos»)',
    'saidas.casas_decimais: inteiro de 0 a 8 ou objeto {{métrica: casas}}': 'saidas.casas_decimais: an integer from 0 to 8 or an object {{metric: places}}',
    'saidas.milhar: esperado verdadeiro ou falso': 'saidas.milhar: true or false is expected',
    '{0}: com o modelo da edição nenhum valor é assumido; informe {1}': '{0}: with the edition template no value is assumed; give {1}',
    '{0}: arquivo de chuva não encontrado: {1}': '{0}: rainfall file not found: {1}',
    'o campo {0} é inteiro; recebido {1!r}': 'the field {0} is an integer; got {1!r}',
    'o caminho «{0}» não existe no projeto (parou em «{1}»)': 'the path «{0}» does not exist in the project (stopped at «{1}»)',
    'caminhos pontilhados só valem para projetos .triton': 'dotted paths only work with .triton projects',
    'projeto inválido:': 'invalid project:',
    'marcador {0}: métrica desconhecida «{1}».': 'marker {0}: unknown metric «{1}».',
    '{0}.{1}: esperado texto': '{0}.{1}: text is expected',
    '{0}: projeto não encontrado: {1}': '{0}: project not found: {1}',
    'o campo {0} é numérico; recebido {1!r}': 'the field {0} is numeric; got {1!r}',
    'o volume ótimo técnico não foi definido; usado o de maior economia de água potável':
        'the technical optimum volume was not defined; the one with the largest potable water saving was used',
    'marcador inválido: {0} (as casas depois de | devem ser um inteiro)': 'invalid marker: {0} (the places after | must be an integer)',
    '{0}: chave desconhecida «{1}».': '{0}: unknown key «{1}».',
    '{0}: ainda não preenchido': '{0}: not filled in yet',
    '{0}: informe «{1}» (um .triton) ou «{2}»': '{0}: give «{1}» (a .triton) or «{2}»',
    'saidas.formatos: formato desconhecido «{0}». Use: {1}': 'saidas.formatos: unknown format «{0}». Use: {1}',
    'o campo {0} é texto; recebido {1!r}': 'the field {0} is text; got {1!r}',
    '{0}: esperado texto': '{0}: text is expected',
    'projeto_base.modelo: o único modelo é «edicao» (o modelo de projeto da edição, como «triton init»)':
        'projeto_base.modelo: the only template is «edicao» (the edition\'s project template, as in «triton init»)',
    'Métricas: {0}': 'Metrics: {0}',
    'saidas.metricas: «{0}» exige analise.tipo «{1}» ou mais completo; o estudo executa «{2}»':
        'saidas.metricas: «{0}» requires analise.tipo «{1}» or a more complete one; the study runs «{2}»',
    'saidas.casas_decimais: métrica desconhecida «{0}».': 'saidas.casas_decimais: unknown metric «{0}».',
    'saidas.casas_decimais.{0}: inteiro de 0 a 8': 'saidas.casas_decimais.{0}: an integer from 0 to 8',
    'saidas.metricas: métrica desconhecida «{0}».': 'saidas.metricas: unknown metric «{0}».',
    'apelido sem aplicação: {0}': 'alias without an implementation: {0}',
    '{0}.projeto: esperado texto': '{0}.projeto: text is expected',
    '{0}.projeto: ainda não preenchido': '{0}.projeto: not filled in yet',
})


def em_portugues_de_portugal(texto: str) -> str:
    """O texto com o glossário de Portugal (para o núcleo, que não importa a interface)."""
    from triton.ui.portugues_de_portugal import para_portugal
    return para_portugal(texto)


def t(texto: str) -> str:
    """O texto da edição ativa: o original na Brasil, o inglês na Internacional, o glossário na Portugal."""
    if is_int_edition():
        return _EN.get(texto, texto)
    if is_ibe_edition():
        from triton.ui.portugues_de_portugal import para_portugal
        return para_portugal(texto)
    return texto
