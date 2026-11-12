# Triton CLI — practical guide

Use the command line for reproducible runs, automation and batch comparison. It accepts legacy CSV projects and structured `.triton` projects (JSON).

Run the examples from the edition folder, in the same environment as the desktop application. To see the help of the installed version:

```powershell
python -m triton.cli --help
python -m triton.cli analyze --help
```

## Choosing the project format

| Format | Recommended use | Traceability |
| --- | --- | --- |
| `.triton` | new studies, exchange and automation | keeps the technical, economic, environmental and TOPSIS inputs; can embed the rainfall |
| Legacy CSV | compatibility and existing technical cases | more limited structure; record outside the file the assumptions it cannot hold |

Prefer `.triton` with `--embed-rainfall` when the study must be reproduced on another computer. Even self-contained, the file does not replace the record of the source, period, treatment and quality control of the series.

## Recommended workflow

```powershell
# 1. Create a portable project with the daily rainfall embedded.
python -m triton.cli init .\project.triton --rainfall data\rainfall\NewYork.csv --embed-rainfall

# 2. Validate the file before calculating.
python -m triton.cli validate .\project.triton

# 3. Run the technical, economic, LCA, system-weight and TOPSIS analyses, with an auditable result.
python -m triton.cli analyze .\project.triton --analysis all --format json --output .\out\result.json
```

The `run` command runs the technical water balance. `analyze --analysis all` applies, to every volume of the sweep, the technical balance, the economic analysis, the environmental balance, the weight of the system and the TOPSIS ranking, so every choice uses the same simulated alternatives.

**Weight of the system.** `--analysis all` (and `--analysis system_weight`) reports `system_weight`: the dry mass, the water load and the operating load, in kg and kN, split into basement or lower level, roof or upper level, and risers and network. The HTML report, the XLSX (sheet `system_weight` with the summary of the chosen volume; the values per volume are in the sheet `alternatives`) and the terminal text show the block. Its warnings are attention thresholds of the program, not limits of any standard — 500 kg on the roof with the upper tank full, an upper tank above 1,500 L, a cistern above 3,000 kg dry, and any concrete cistern — and ask for a check by the structural or foundation design.

## Most-used commands

| Goal | Command |
| --- | --- |
| Simulate one volume | `python -m triton.cli run .\project.triton --volume 5000 --analysis all` |
| Change assumptions without editing the project | `python -m triton.cli analyze .\project.triton --set area=150 --set rainwater_share=0.5` |
| Set the TOPSIS weights | `python -m triton.cli analyze .\project.triton --analysis topsis --weights 0.40,0.30,0.20,0.10` |
| Set the criterion shares | `python -m triton.cli analyze .\project.triton --analysis topsis --criterion-shares 1,0,1,1,1,1,1,1` |
| Test the robustness of the weights | `python -m triton.cli analyze .\project.triton --analysis topsis --weight-sensitivity 1000 --seed 42 --format json --output .\out\weights.json` |
| Propagate uncertainty | `python -m triton.cli uncertainty .\project.triton --samples 1000 --rainfall-cv 10 --demand-cv 15 --capex-cv 20 --format json --output .\out\monte-carlo.json` |
| Produce HTML or XLSX | Replace `--format json` with `html` or `xlsx` and give `--output` |
| Run a scenario spreadsheet | `python -m triton.cli batch .\scenarios.xlsx --base .\project.triton --analysis all --format xlsx --output .\out\batch.xlsx` |
| Combine several projects and rainfall series | `python -m triton.cli matrix-projects --projects .\projects --rainfall-dir .\rainfall --recursive --output-dir .\out\matrix` |

The multi-criteria decision of version 0.2.0 has eight criteria in four dimensions. `--weights` takes four dimension weights, in this order: technical, economic, environmental and structural (default 0.25 each), or eight criterion weights; the CLI normalises their sum. Three weights, as in projects of version 0.1.0, are still accepted, and the structural dimension receives their mean; seven are refused. `--criterion-shares` takes eight shares, one per criterion, in the order volumetric reliability, storage efficiency, net financial savings, LCOW, payback, life-cycle CO₂, dry mass and annual overflow (default `1,1,1,1,1,1,1,1`); each dimension weight is shared among its criteria in proportion to them, and a share of zero removes the criterion. In the project file the same values go in `analysis.topsis_weights` (four or eight) and `analysis.topsis_criterion_shares` (eight). The general outputs accept `text`, `json`, `csv`, `html` and `xlsx`; `uncertainty` accepts `text`, `json` and `csv`. Structured formats need `--output`. XLSX needs `pandas` and `openpyxl`.

`--set FIELD=VALUE` can be repeated and changes the assumption for that run only. Record the full command in the study protocol, because the source file stays unchanged.

## Buildings × climates matrix

Keep the two catalogues separate: one of building assumptions and one of climate files. You can then compare several cities for the same building, or several buildings for the same city, without duplicating data.

```powershell
python -m triton.cli init-catalog premises .\premises.json
python -m triton.cli init-catalog climates .\climates.json
python -m triton.cli matrix .\premises.json .\climates.json --analysis all --output-dir .\matrix-result
```

The terminal shows the progress, the combinations finished, the elapsed time and the ETA. The output folder holds `triton-matriz-resumo.csv` (one decision per combination), `triton-matriz-alternativas.csv` (every volume), `triton-matriz-detalhado.json` (audit) and `triton-matriz-painel.html` (consolidated view).

### Projects matrix

Use `matrix-projects` when each configuration is already in one or more `.triton` files, or when the project itself declares experimental factors in `cli_factorial`:

```powershell
python -m triton.cli matrix-projects --projects .\projects --output-dir .\projects-result
python -m triton.cli matrix-projects --projects .\projects --rainfall-dir .\rainfall --recursive --output-dir .\climates-result
```

Use `--ignore-project-factors` to ignore, for that run, the factorial block saved in the projects. Fix `--seed` when the weights are perturbed at random.

## Scenarios in a spreadsheet

`batch` reads CSV or XLSX. With `--base`, the rows inherit from the base project the economic and environmental assumptions that the spreadsheet does not override:

```powershell
python -m triton.cli batch .\examples\triton-cli-scenarios.csv --base .\project.triton --analysis all --format csv --output .\out\scenarios.csv
```

Validate the base project first and keep the input spreadsheet with the result. A batch compares declared scenarios; it does not create uncertainty distributions.

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
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` or `all`), `volume` (`otimo_tecnico` technical optimum, `topsis`, `smaa_vikor` or a volume in litres), `pesos` (four dimension weights — technical, economic, environmental, structural — or eight criterion weights; three, from studies up to version 0.1.0, are still accepted and seven are refused), `partes_no_eixo` (eight criterion shares) and `semente` (seed) |
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

## Reproducibility and audit

For every run used in a report or a publication, keep:

- the `.triton` file, catalogues or scenario spreadsheet actually used;
- the rainfall series and its provenance, unless it is embedded in the project;
- the full command, the Triton version and the Python version;
- the seed of any stochastic analysis;
- the output files, unedited, and a record of any later interpretation.

Weight sensitivity and Monte Carlo answer different questions. The first measures how stable the ranking is to the preferences; the second propagates the uncertainty of the declared inputs. Neither corrects poor data or omitted assumptions.

## Good practice

- Use `--embed-rainfall` when the project has to move between computers.
- Run `validate` before processing batches.
- Use different output paths for different scenarios and do not overwrite evidence without review.
- Fix `--seed` in weight and Monte Carlo analyses to reproduce a run exactly.
- Start large batches with a small sample and check units, columns and orders of magnitude.
- Use `python -m triton.cli <command> --help` when this guide and the installed version differ.
