# Triton CLI — guia prático

Use a linha de comando para execuções reproduzíveis, automação e comparação em lote. Ela aceita projetos CSV legados e projetos estruturados `.triton` (JSON).

Execute os exemplos a partir da raiz do repositório, com o mesmo ambiente usado pela aplicação desktop. Consulte a ajuda efetiva da versão instalada com:

```powershell
python -m triton.cli --help
python -m triton.cli analyze --help
```

## Escolha do formato de projeto

| Formato | Uso recomendado | Rastreabilidade |
| --- | --- | --- |
| `.triton` | novos estudos, intercâmbio e automação | preserva entradas técnicas, econômicas, ambientais e TOPSIS; pode incorporar a chuva |
| CSV legado | compatibilidade e casos técnicos existentes | possui estrutura mais limitada; documente externamente as premissas não representadas |

Prefira `.triton` com `--embed-rainfall` quando o estudo precisar ser reproduzido em outro computador. Mesmo autocontido, o arquivo não substitui o registro de fonte, período, tratamento e controle de qualidade da série.

## Fluxo recomendado

```powershell
# 1. Crie um projeto portátil, incorporando a chuva diária.
python -m triton.cli init .\projeto.triton --rainfall NewYork.csv --embed-rainfall

# 2. Valide o arquivo antes de calcular.
python -m triton.cli validate .\projeto.triton

# 3. Rode técnica, economia, ACV e TOPSIS, com resultado auditável.
python -m triton.cli analyze .\projeto.triton --analysis all --format json --output .\saida\resultado.json
```

O comando `run` executa o balanço hídrico técnico. `analyze --analysis all` aplica, para cada volume da varredura, o balanço técnico, a análise econômica, o balanço ambiental e o ranking TOPSIS. Assim, todas as escolhas usam as mesmas alternativas simuladas.

## Comandos mais usados

| Objetivo | Comando |
| --- | --- |
| Simular um volume específico | `python -m triton.cli run .\projeto.triton --volume 5000 --analysis all` |
| Alterar premissas sem editar o projeto | `python -m triton.cli analyze .\projeto.triton --set area=150 --set rainwater_share=0.5` |
| Ajustar pesos TOPSIS | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weights 0.40,0.35,0.25` |
| Avaliar robustez dos pesos | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weight-sensitivity 1000 --seed 42 --format json --output .\saida\pesos.json` |
| Propagar incertezas | `python -m triton.cli uncertainty .\projeto.triton --samples 1000 --rainfall-cv 10 --demand-cv 15 --capex-cv 20 --format json --output .\saida\monte-carlo.json` |
| Gerar HTML ou XLSX | Troque `--format json` por `html` ou `xlsx` e informe `--output` |
| Executar planilha de cenários | `python -m triton.cli batch .\cenarios.xlsx --base .\projeto.triton --analysis all --format xlsx --output .\saida\lote.xlsx` |
| Combinar vários projetos e chuvas | `python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\saida\matriz` |

Os valores de `--weights` são, nesta ordem: técnico, econômico e ambiental. A CLI normaliza a soma automaticamente. As saídas gerais aceitam `text`, `json`, `csv`, `html` e `xlsx`; o comando `uncertainty` aceita `text`, `json` e `csv`. Formatos estruturados exigem `--output`. XLSX requer `pandas` e `openpyxl`.

`--set CAMPO=VALOR` pode ser repetido e altera a premissa somente para aquela execução. Registre o comando completo no protocolo do estudo, pois o arquivo de origem permanece inalterado.

## Matriz edifícios × climas

Mantenha os dois catálogos independentes: um de premissas do edifício e outro de arquivos climáticos. Isso permite comparar várias cidades para o mesmo edifício, ou vários edifícios para a mesma cidade, sem duplicar dados.

```powershell
python -m triton.cli init-catalog premises .\premissas.json
python -m triton.cli init-catalog climates .\climas.json
python -m triton.cli matrix .\premissas.json .\climas.json --analysis all --output-dir .\resultado-matriz
```

O terminal informa progresso, combinações concluídas, tempo decorrido e ETA. A pasta de saída contém `triton-matriz-resumo.csv` (uma decisão por combinação), `triton-matriz-alternativas.csv` (todos os volumes), `triton-matriz-detalhado.json` (auditoria) e `triton-matriz-painel.html` (leitura consolidada).

### Matriz de projetos

Use `matrix-projects` quando cada configuração já estiver em um ou mais arquivos `.triton`, ou quando o próprio projeto declarar fatores experimentais em `cli_factorial`:

```powershell
python -m triton.cli matrix-projects --projects .\projetos --output-dir .\resultado-projetos
python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\resultado-climas
```

Use `--ignore-project-factors` para desconsiderar temporariamente o bloco fatorial gravado nos projetos. Fixe `--seed` quando houver sensibilidade estocástica dos pesos.

## Cenários em planilha

`batch` lê CSV ou XLSX. Com `--base`, as linhas herdam do projeto-base as premissas econômicas e ambientais que a planilha não substitui:

```powershell
python -m triton.cli batch .\examples\triton-cli-scenarios.csv --base .\projeto.triton --analysis all --format csv --output .\saida\cenarios.csv
```

Valide primeiro o projeto-base e preserve a planilha de entrada junto do resultado. Um lote compara cenários declarados; ele não cria automaticamente distribuições de incerteza.

## Simulação em massa e comparação com TesteMassivo

Para rodar em massa a separação de séries futuras e comparar a nova versão do motor contra a base de dados de referência (`TesteMassivo/`):

```powershell
# 1. Separe as séries climáticas futuras em Near Future (2015-2059) e Far Future (2060-2100):
python scripts/split_climates.py

# 2. Execute a simulação paralela multi-core dos 4 casos de reservatórios combinados da Tabela 2 e gera o relatório comparativo:
python -m triton.cli compare-mass
```

Parâmetros opcionais de `compare-mass`:

- `--input-dir`: Pasta com os arquivos de chuva divididos (`TesteMassivo/Triton_future_files_split`)
- `--reference-dir`: Pasta com os arquivos CSVs consolidados de referência (`TesteMassivo`)
- `--output-dir`: Pasta de destino dos novos CSVs consolidados e relatórios (`TesteMassivo/nova_versao`)
- `--area`, `--residents`, `--demand`, `--share`, `--runoff` e `--discard`: premissas do caso comparado
- `--workers`: Número de núcleos de CPU para processamento em paralelo

## Estudo massivo de tipologias residenciais de Vaz

Para executar a divisão em quatro horizontes temporais (Histórico, Near, Middle e Far) e rodar o estudo completo em Parquet:

```powershell
# 1. Separar séries climáticas futuras em Near (2015-2044), Middle (2045-2074) e Far Future (2075-2100):
python scripts/split_climates_vaz.py

# 2. Executar o estudo massivo das cinco tipologias e exportar em Parquet:
python -m triton.cli run-vaz-study
```

Parâmetros opcionais de `run-vaz-study`:

- `--input-dir`: Pasta com as séries climáticas divididas (`TesteMassivo/Triton_vaz_files_split`)
- `--output-dir`: Pasta de destino para o arquivo Parquet e relatórios (`TesteMassivo/estudo_vaz`)
- `--workers`: Número de processos paralelos; por padrão, o comando preserva um núcleo para o sistema quando possível

O estudo Vaz requer `pyarrow` para Parquet. Avalie espaço em disco, memória e temperatura da máquina antes de aumentar `--workers`; mais processos não garantem ganho linear.

## Batch studies from JSON

To compare many buildings by typology (schools, commercial buildings, houses, hospitals, airports) and take the results to a paper, organise the study in an `estudo.json` file and run everything with `triton estudo`. The file gathers the base project, the cases, what changes from one case to the next, the analysis and the outputs; the program runs the cases in a stable order and writes tables ready for the text (tidy CSV, JSON with provenance, Markdown, LaTeX, XLSX).

```powershell
# 1. A skeleton study, with the labels of the typology and no value filled in.
python -m triton.cli estudo init .\schools --tipologia escolar

# 2. Fill in schools\estudo.json (the «XX» and null entries) and put the .triton files and series in schools\casos.
python -m triton.cli estudo validate .\schools\estudo.json

# 3. Run every case (in a stable order); --paralelo N uses N processes and does not change the result.
python -m triton.cli estudo run .\schools\estudo.json --saida .\out\schools --paralelo 4

# 4. Rebuild the tables without recomputing (for example after changing metrics or decimal places).
python -m triton.cli estudo resumo .\out\schools

# 5. Fill the conference abstract template with the real numbers.
python -m triton.cli estudo texto .\out\schools --modelo .\schools\modelo_texto.md

# 6. Several studies (a folder with estudo*.json files), with the comparison between typologies.
python -m triton.cli estudo lote .\studies --saida .\out\comparison

# 7. Gather the resultados.csv of many runs into one table (typology, case, metric: minimum, mean, median, maximum).
python -m triton.cli estudo consolidar .\out --saida .\out\consolidated
```

The typologies (`escolar` school, `comercial` commercial, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar` hospital, `aeroportuario` airport) are structure and labels only: `estudo init --tipologia` writes the label, the `grupo` of the cases and, in a comment, what `usuarios` means in that typology. No number comes with the typology: area, demand, users and share come from your cases, with the source of each.

The `consolidar` action searches every `resultados.csv` under the given folders (several studies, batches, repeated runs) and writes `consolidado.csv` and `consolidado.md` to the output folder: one row per typology (`grupo`), case and metric, with `n`, minimum, mean, median and maximum of the values of the cases that finished (`status` ok). The unit is part of the group key, so different currencies are never mixed. Numbers have the same format as in `resultados.csv` (decimal point, ten significant digits); the Markdown table follows `--idioma`. If the optional `duckdb` package is installed (`pip install "triton-int[analise]"`, not part of the installer), it reads and groups the files; without it the standard library does the same, and the two paths give the same bytes (`--motor csv` forces the second; `--motor duckdb` demands the package).

`estudo run` and `estudo lote` show their progress on the error stream. `--progresso simples` writes one line per case (`[i/N] id: ok (t s)`); `--progresso rich` draws a progress bar and needs the optional `rich` package (`pip install "triton-int[cli]"`; without it the program warns once and uses `simples`); the default `auto` uses `rich` only if it is installed and the error stream is a terminal. The result files are identical in bytes in every mode, and `--quiet` turns the progress off.

### The estudo.json file

<!-- tabela: Sections of the estudo.json file (schema triton-estudo, version 1) -->
| Section | Content |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; any other version is refused |
| `estudo` | `id` (letters, digits, dot, hyphen and underscore), `titulo` (title), `tipologia` (`escolar` school, `comercial` commercial, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar` hospital, `aeroportuario` airport or `outra` other), `tipologia_rotulo`, `autores` (authors), `nota` (note) |
| `projeto_base` | `arquivo`: a `.triton`, with a path relative to `estudo.json`; or `modelo`: `"edicao"`, the project template of the edition (each case must then give area, demand, share and rainfall: nothing is assumed) |
| `padroes` | `substituicoes` (substitutions) and `clima` (climate) applied to every case; what a case declares wins over the default |
| `casos` | list; each case has `id`, `nome` (name), `grupo` (group; by default the typology), `projeto` (another `.triton` for this case), `clima` and `substituicoes` |
| `clima` | `arquivo` (daily rainfall series, CSV), `data_inicio` (dd/mm/yyyy), `nome` and `fonte` (labels that go into the provenance) |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` or `all`), `volume` (`otimo_tecnico` technical optimum, `topsis` or a volume in litres), `pesos` (TOPSIS weights) and `semente` (seed) |
| `saidas` | `formatos` (`csv`, `json`, `md`, `tex`, `xlsx`), `metricas`, `casas_decimais` (one integer or one per metric), `idioma` (`auto`, `pt-BR`, `pt-PT`, `en`, `es`, `zh`), `milhar` (thousands separator), `legenda` (caption) and `orientacao` (`casos_nas_linhas` or `metricas_nas_linhas`) |

Keys that start with `_` are comments and the program ignores them. An empty field, `null` or «XX» means «to be filled in»: the validation refuses it and says where it is. An unknown key is an error, with the closest match suggested. `triton estudo esquema` prints the JSON Schema of the file, for completion and checking in an editor.

### Aliases of the substitutions

<!-- tabela: Aliases of the substitutions and the project field each one changes -->
| Alias | Project field | Unit |
| :--- | :--- | :--- |
| `area_captacao_m2` | `area` | m² |
| `coeficiente_escoamento` | `runoff_coeff` | 0 to 1 |
| `descarte_mm` | `discard` | mm |
| `usuarios` (also `populacao`, `pessoas`, `ocupantes`, `users`, `residents`) | `residents_count` | people |
| `demanda_per_capita_l_dia` | `demand_value` | L/person·day |
| `demanda_total_l_dia` | `demand_value` (the total demand divided by the users) | L/day |
| `fracao_pluvial_pct` or `fracao_pluvial` | `rainwater_share` | % or 0 to 1 |
| `volume_reservatorio_l` | `lower_tank_fixed` (and `lower_tank_mode` = fixed volume) | L |
| `volume_maximo_l`, `passo_volume_l` | `lower_tank_max` (sweep), `lower_tank_step` | L |
| `reservatorio_superior_l` | `upper_tank_vol` (and `upper_tank_used`) | L |
| `limiar_bombeamento_l`, `economias`, `irrigacao_l_dia` | `pumping_threshold`, `num_economias`, `irrigation_liters_per_day` | L, units, L/day |
| `data_inicio`, `regra_phi`, `delta_ideal_pct` | `start_date`, `phi_operation_rule`, `delta_ideal` | dd/mm/yyyy, 0 to 1, %/m³ |
| `periodo_analise_anos`, `tma_pct_mes`, `tarifa_energia` | `analysis_period_years`, `tma`, `elec_tariff` | years, % per month, currency/kWh |

Besides the aliases, the key of a substitution can be **any field that `--set` accepts** (for example `cost_labor`) or a **dotted path of the `.triton` file itself**, such as `inputs.building_and_demand.catchment_area_m2`. The path must exist in the project and the value must have the same type as what is already there; otherwise the case ends with a clear error that lists the available keys. An unknown alias is also refused, with the closest match suggested. Two names for the same parameter in the same case (`area_captacao_m2` and `area_m2`, or `fracao_pluvial` and `fracao_pluvial_pct`) are a conflict. The fraction from 0 to 1 refuses 40 (probably a percentage); the percentage refuses anything outside 0 to 100.

The substitutions go through the same fraction reconciliation as `--set`, and the preliminary cost fill (CAPEX) runs **after** them, so the price of the tank follows the volume of the case. `triton estudo apelidos` lists every alias and metric, in the language of the edition.

### Outputs for the paper

<!-- tabela: Files that triton estudo run writes to the output folder -->
| File | Content |
| :--- | :--- |
| `resultados.csv` | **tidy** format: one row per case and metric (`estudo_id`, `caso_id`, `caso`, `grupo`, `metrica`, `rotulo`, `valor`, `unidade`, `status`); decimal point, no thousands separator, UTF-8 |
| `resultados.json` | the same values plus the **provenance**: Triton version, edition, SHA-256 of `estudo.json` and of each project and rainfall series, rainfall source, credit and licence, warnings and the run date |
| `tabela.md` | Markdown table, with the numbers in the format of the language (decimal comma in Portuguese and Spanish, point in English and Chinese) |
| `tabela.tex` | LaTeX table with `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), ready to paste; needs `\usepackage{booktabs}` |
| `tabela.xlsx` | optional (`xlsx` in `formatos`): real, formatted numbers, plus the `tidy` and `proveniencia` sheets |
| `resumo.md` | short summary: cases, range of each result, warnings, sources and licences |
| `casos/<id>/resultado.json` and `analise.json` | every metric of the case and the full analysis of the engine (this is what `resumo` and `texto` read) |
| `estudo.json` | copy of the study that produced the folder |

The outputs carry no absolute path: projects appear with a path relative to `estudo.json` (or just the name). Two runs of the same study give identical files; the run date is the only difference, and the environment variable `SOURCE_DATE_EPOCH` fixes it. The `xlsx` stores its creation date in the file properties and is identical in content, not byte for byte.

**Resuming and exit codes.** In an output folder that already has results, `run` requires `--retomar` (skips the finished and unchanged cases: the fingerprint of a case includes the study, the files, the version and the edition) or `--sobrescrever` (redoes everything). The exit code is 0 if every case was computed, 1 if some case ended with an error (the outputs of the others are written and the failed case shows `status` `erro`) and 2 if the study or the arguments are invalid.

**Metrics.** The volume of each case is, by default, the technical optimum of the sweep (`volume: "otimo_tecnico"`); with `"topsis"`, the first of the ranking; with a number, the fixed volume. The available metrics include `volume_l`, `economia_agua_potavel_pct` (potable water saving), `agua_pluvial_m3_ano` (rainwater used), `agua_potavel_m3_ano`, `extravasamento_m3_ano` (overflow), the days with full, partial and no supply, `capex`, `vpl` (net present value), `economia_anual_agua` (annual saving on the water bill), `opex_anual`, `tir_anual_pct` (IRR), `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` and `aceitabilidade_smaa_pct`, plus the inputs of the case (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). The economic metrics need `analise.tipo` `economic` or `all`; the environmental ones, `environmental` or `all`. The raw names of the report (`potable_savings_pct`) are also accepted. Monetary values come out in the currency of each project; if the cases have different currencies, the summary warns that they are not comparable and the comparison does not aggregate them. With CAPEX equal to zero (costs not entered), the summary warns that NPV, IRR and payback are not results.

**Text with the numbers.** `triton estudo texto` replaces, in your `.md` template, the markers in double braces: `{{economia_agua_potavel_pct:caso-01}}` (the value of one case), `{{economia_agua_potavel_pct:@min}}`, `@max`, `@media` (mean), `@mediana` (median) (over the computed cases; `@media(escolar)` restricts to one group), `{{n_casos}}` and, after a vertical bar, the decimal places (`{{vpl:caso-01|0}}`). Where a result is missing the marker becomes «XX» and the command lists the gaps (with `--estrito`, it exits with code 1). An unknown metric is an error.

### Rainfall source and licence

The ERA5 example series carry the Open-Meteo/Copernicus credit (CC BY 4.0), which the outputs inherit from `analyze` and repeat in the summary, in the tables and in `resultados.json`. Record the source, period and treatment of any series of your own in the protocol of the study.

### Example

The example `examples/estudos/residencial-unifamiliar-exemplo/` runs the tutorial house in New York, London and Cape Town (`new_york.triton`, `london.triton`, `cape_town.triton`): `python -m triton.cli estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida out\example`.

The example uses the projects already shipped and invents no numbers. To add a case, copy a block of `casos` and change `id`, `nome` and the `projeto` (or the `clima.arquivo` and the `substituicoes`); record the source of every value you fill in.

## Reprodutibilidade e auditoria

Para cada execução usada em relatório ou publicação, preserve:

- arquivo `.triton`, catálogos ou planilha de cenários efetivamente usados;
- série de chuva e sua proveniência, salvo quando incorporada ao projeto;
- comando completo, versão do Triton e versão do Python;
- semente de qualquer análise estocástica;
- arquivos de saída sem edição manual e um registro das interpretações posteriores.

Sensibilidade de pesos e Monte Carlo respondem a perguntas diferentes. A primeira mede estabilidade do ranking diante das preferências; a segunda propaga incerteza das entradas declaradas. Nenhuma delas corrige dados de baixa qualidade ou hipóteses omitidas.

## Boas práticas

- Use `--embed-rainfall` quando o projeto precisar circular entre computadores.
- Execute `validate` antes de processar lotes.
- Use caminhos de saída diferentes para cenários diferentes e não sobrescreva evidências sem revisão.
- Fixe `--seed` em análises de pesos e Monte Carlo para reproduzir exatamente uma execução.
- Comece lotes grandes com uma amostra pequena e confira unidades, colunas e ordem de grandeza.
- Use `python -m triton.cli <comando> --help` quando este guia e a versão instalada divergirem.
