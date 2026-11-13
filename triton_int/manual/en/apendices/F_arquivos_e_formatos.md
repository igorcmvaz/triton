# Files, folders and formats

Everything the program reads and writes, and where each thing is kept.

---

## What the program reads

<!-- tabela: Formats the program reads and where each one is loaded -->
| Format | Extension | What it is | Where it is loaded |
| :--- | :--- | :--- | :--- |
| project | `.triton` | a complete study, with the rain inside | Open Project |
| old project | `.json` | project from an earlier version, same content | Open Project |
| legacy project | `.csv` | project saved by an early version of the program, as a table | Open Project |
| rainfall series | `.csv` | one column of millimetres per day (the edition ships three examples in `data/rainfall`) | step 1. Project & Rainfall |
| daily demand | `.csv` | measured consumption, day by day | step 2. Building & Demand |
| scenarios | `.xlsx` | one row per scenario | Scenarios & Tools menu |

**The rainfall series in CSV** is the simplest format possible: one line per day, with the depth in
millimetres. The program accepts a point or a comma as the decimal separator, and ignores a header
line if there is one. An incomplete year is discarded on reading, so as not to bias the annual
totals.

> **Legacy project in CSV.** The old format does not keep everything the current version uses:
> demand modulation, materials, multi-criteria weights and the rainfall series are left out. When
> opening such a file, the program warns and adopts the default values for what is missing. Section
> {{n:21}} shows what to check after importing.

---

## What the program writes

<!-- tabela: Formats the program writes and where each one is generated -->
| Format | Extension | What it carries | Where it is generated |
| :--- | :--- | :--- | :--- |
| project | `.triton` | all the parameters and the rainfall series | Save Project |
| report | `.pdf` | the complete study, ready to hand over | step 9. PDF Reports |
| spreadsheet | `.xlsx` | daily series, sweep and indicators | step 10. Export |
| table | `.csv` | the same data, as delimited text | step 10. Export |
| data | `.json` | the results, for reprocessing | step 10. Export |
| drawing | `.dxf` | the hydraulic schematic, for CAD | step 10. Export |
| drawing | `.svg` | the same schematic, as a vector image | step 10. Export |

In CSV export you choose the separator: **semicolon** to open in a spreadsheet set to a language
that uses the decimal comma, **comma** for the international standard. Choosing wrongly
makes the spreadsheet open everything in a single column.

The drawing comes in three presentations: **A3 technical sheet**, **simple schematic** and **block
library**, the last accompanied by a JSON file with the properties of the components, for BIM
coordination. Section {{n:22}} deals with all of them.

---

## The project file, inside

The `.triton` file is a text file in JSON format. It can be opened in any text editor, and that is
deliberate: a published study needs to be inspectable without the program.

It has seven sections:

<!-- tabela: The seven sections of the project file and what each one holds -->
| Section | What it holds |
| :--- | :--- |
| `metadata` | project name, identifier and dates |
| `rainfall` | the city, the period and the **whole daily series** |
| `building_and_demand` | area, coefficient, occupants, consumption and fraction |
| `demand_modulation` | the weekly, monthly and daily profiles, when there are any |
| `reservoirs_and_pumping` | volumes, thresholds and the pump set |
| `water_quality_and_etap` | target class, disinfection and treatment |
| `financial_and_economic` | tariffs, taxes, adjustments and period |

Appendix {{n:A}} lists all the parameters, with the exact name of each field.

> **The rainfall series goes inside the file.** That is what makes the project reproducible: whoever
> receives the file obtains exactly your numbers, without needing the original rainfall file. On the
> other hand, a project with thirty years of series takes up about 160 kB — little for a file and a
> lot for an e-mail attachment with twenty of them.

---

## Where things are kept

<!-- tabela: Location of the program's files and of the user's files -->
| What | Where |
| :--- | :--- |
| the program | `C:\Program Files\Triton` |
| the rainfall series that come with it (New York, London, Cape Town) | in the program folder, in `data\rainfall` |
| the manual's cases | in the program folder, in `casos` |
| the three example projects (New York, London, Cape Town) | in the program folder, in `examples` |
| **your projects and reports** | **wherever you choose when saving** |

The program does not create a working folder or keep hidden files. Each save asks for the
destination, and nothing you produce stays inside the installation folder — which means that
reinstalling or updating the program deletes nothing of yours.

---

## The batch study file (`estudo.json`)

Used by `triton estudo` (chapter «Comparing many cases at once»). Schema `triton-estudo`, version 1.

<!-- tabela: Sections of the estudo.json file (schema triton-estudo, version 1) -->
| Section | Content |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; any other version is refused |
| `estudo` | `id` (letters, digits, dot, hyphen and underscore), `titulo` (title), `tipologia` (`escolar` school, `comercial` commercial, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar` hospital, `aeroportuario` airport or `outra` other), `tipologia_rotulo`, `autores` (authors), `nota` (note) |
| `projeto_base` | `arquivo`: a `.triton`, with a path relative to `estudo.json`; or `modelo`: `"edicao"`, the project template of the edition (each case must then give area, demand, share and rainfall: nothing is assumed) |
| `padroes` | `substituicoes` (substitutions) and `clima` (climate) applied to every case; what a case declares wins over the default |
| `casos` | list; each case has `id`, `nome` (name), `grupo` (group; by default the typology), `projeto` (another `.triton` for this case), `clima` and `substituicoes` |
| `clima` | `arquivo` (daily rainfall series, CSV), `data_inicio` (dd/mm/yyyy), `nome` and `fonte` (labels that go into the provenance) |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` or `all`), `volume` (`otimo_tecnico` technical optimum, `topsis`, `smaa_vikor` or a volume in litres), `pesos` (four dimension weights — technical, economic, environmental, structural — eight criterion weights, or `"critic"` for objective weights computed from the results; three, from studies up to version 0.1.0, are still accepted and seven are refused), `partes_no_eixo` (eight criterion shares, in the order of the criteria), `tolerancia_faixa` (tolerance of the choice band, 0 to 1, default 0.05) and `semente` (seed) |
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

### Outputs of the study

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
| `consolidado.csv` and `consolidado.md` | written by `triton estudo consolidar` (not by `run`): one row per typology (`grupo`), case, metric and unit, with `n`, minimum, mean, median and maximum over the `resultados.csv` files found |

The outputs carry no absolute path: projects appear with a path relative to `estudo.json` (or just the name). Two runs of the same study give identical files; the run date is the only difference, and the environment variable `SOURCE_DATE_EPOCH` fixes it. The `xlsx` stores its creation date in the file properties and is identical in content, not byte for byte.

**Resuming and exit codes.** In an output folder that already has results, `run` requires `--retomar` (skips the finished and unchanged cases: the fingerprint of a case includes the study, the files, the version and the edition) or `--sobrescrever` (redoes everything). The exit code is 0 if every case was computed, 1 if some case ended with an error (the outputs of the others are written and the failed case shows `status` `erro`) and 2 if the study or the arguments are invalid.

**Metrics.** The volume of each case is, by default, the technical optimum of the sweep (`volume: "otimo_tecnico"`); with `"topsis"`, the first of the ranking; with a number, the fixed volume. The available metrics include `volume_l`, `economia_agua_potavel_pct` (potable water saving), `agua_pluvial_m3_ano` (rainwater used), `agua_potavel_m3_ano`, `extravasamento_m3_ano` (overflow), the days with full, partial and no supply, `capex`, `vpl` (net present value), `economia_anual_agua` (annual saving on the water bill), `opex_anual`, `tir_anual_pct` (IRR), `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis`, `faixa_topsis_min_l` and `faixa_topsis_max_l` (the ends of the TOPSIS choice band) and `aceitabilidade_smaa_pct`, plus the inputs of the case (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). The economic metrics need `analise.tipo` `economic` or `all`; the environmental ones, `environmental` or `all`. The raw names of the report (`potable_savings_pct`) are also accepted. Monetary values come out in the currency of each project; if the cases have different currencies, the summary warns that they are not comparable and the comparison does not aggregate them. With CAPEX equal to zero (costs not entered), the summary warns that NPV, IRR and payback are not results.

**Text with the numbers.** `triton estudo texto` replaces, in your `.md` template, the markers wrapped in double braces (two on each side; the examples below are shown without them): `economia_agua_potavel_pct:caso-01` (the value of one case), `economia_agua_potavel_pct:@min`, `@max`, `@media` (mean), `@mediana` (median) (over the computed cases; `@media(escolar)` restricts to one group), `n_casos` and, after a vertical bar, the decimal places (`vpl:caso-01|0`). Where a result is missing the marker becomes «XX» and the command lists the gaps (with `--estrito`, it exits with code 1). An unknown metric is an error.

## Compatibility between versions

<!-- tabela: Compatibility between versions of the project file -->
| Situation | What happens |
| :--- | :--- |
| project from an earlier version | opens; new fields take the default |
| project from this version in an earlier version | may not open, or may lose fields |
| legacy project in CSV | opens with a warning; check what section {{n:21}} lists |
| JSON file from another program | **rejected**, with a message of its own |

The last row deserves an explanation. A JSON file that is not a Triton project could, in principle,
be accepted and filled in with default values — and the user would simulate 100 m² believing they
were simulating the 180 m² the file describes. The program prefers to stop the opening with a message
of its own, which is inconvenient and is correct: a project opened wrongly produces an entire study
that is wrong.
