# Comparing many cases at once

> **Question this guide answers:** how do I compare dozens of alternatives without redoing
> the whole project for each one?

The program was built to compare alternatives, and it offers three different ways of doing
it. The choice between them is not a matter of preference: each way answers a different
question, and using the wrong one costs time without producing the information wanted.

---

## The three ways

<!-- tabela: The three ways of comparing alternatives depending on what varies between them -->
| If what changes is | Use | Where |
| :--- | :--- | :--- |
| **only the cistern volume** | the sweep | step 4. Tank & Costs |
| **the volume, and you want to decide** | the multi-criteria table | step 8. Multi-Criteria Decision |
| **any other assumption** | saved projects, one per case | `.triton` file |

The first is automatic, the second too, and the third needs organisation.

---

## The sweep: dozens of volumes in one pass

In step **4. Tank & Costs**, choose the **sweep** mode and enter the maximum volume and
the step. The program simulates all the volumes of the grid and draws the curve.

The sweep is the normal way of working, not an advanced function reserved for special cases:
it is almost always the right answer, because «which volume should I adopt?» is the central
question of every rainwater harvesting project. Section {{n:7}} goes through a complete sweep
step by step, and section {{n:24}} formalises how the grid of volumes is built.

The computational cost is modest and does not justify hesitation: a sweep from 0 to 20,000 L
with a 1,000 L step means twenty-one simulations of thirty years each, and it finishes in a
few seconds on an ordinary computer.

---

## The multi-criteria table: all volumes, all dimensions

Step **8. Multi-Criteria Decision** shows, in a single table, each volume of the sweep with:

- the water saving and the days of supply;
- the net present value, the discounted payback and the internal rate of return;
- the net carbon at the end of the service life and the environmental payback;
- the TOPSIS score and the SMAA-VIKOR acceptability.

It is the densest way of comparing alternatives the program offers: ten answer columns for
each volume row. The ranking itself uses the eight criteria of section {{n:32}}, in four
dimensions — technical, economic, environmental and structural. The weights sit in four cards, one
per dimension: the dimension weight at the top, 25% by default, and below it the criterion shares
of its criteria; the **Equal shares** and **Recalculate** buttons sit below the cards. The
**decision profile** sets the four weights at once — equal, 70% on one dimension and 10% on each of
the others, or objective weights computed from the results by CRITIC — and the table is re-ranked
on the spot. The conclusion gives, for each method, the **choice band** — the volumes whose result
lies within 5% of the score range of the best — and the volume with the highest score, as in
«TOPSIS band (equal weights): 2000–3000 L · highest score: 2000 L (0.78)». Section {{n:32}}
explains the methods behind it.

---

## When something other than the volume changes

City, tariff, demand, tank material and building type are parameters the sweep does not go
through, and to vary any of them the way is to keep one saved project per case. The procedure
below looks bureaucratic at first sight and saves hours of rework, above all when the study is
picked up again weeks later.

1. Build the complete project once, in full detail.
2. Save it with a name that describes the case: `school_london_30000.triton`.
3. Change **one** thing, and save it under another name.
4. Run each one, and note the result in a spreadsheet of your own.

The example files of the manual were made this way: `01_tutorial_new_york.triton`,
`02_london.triton` and `03_cape_town.triton` are the same project, with the rainfall series and
the tariff swapped. That is what section {{n:14}} compares. (Swapping the city swaps two
things at once; the manual does it on purpose, because the tariff does not change the water
result, and the water result is what the comparison is about.)

> **Change one thing at a time.** If you change the city and the tariff together, the result
> changes and there is no way of knowing which of the two moved it. It seems obvious, and it
> is the most common error in comparative studies.

---

## How to organise the files

A naming convention saves more time than it seems:

```
school_study/
   base.triton
   city_new_york.triton
   city_cape_town.triton
   tariff_commercial.triton
   demand_measured.triton
   results.xlsx
```

And three habits that avoid rework:

**Keep the project, not just the result.** The `.triton` file has the rain inside it and
reproduces the whole study; the results spreadsheet does not.

**Note what changes in the file name.** Six months later, `test3.triton` means nothing.

**Export to a spreadsheet at the end of each round.** Step **10. Export** saves the tables
in `.xlsx`, and that is where the comparison between cases is put together.

---

## How many cases fit

The program imposes no limit on the number of cases compared, and the real limit is the
analyst's patience: each thirty-year simulation takes fractions of a second, but building and
checking each project takes minutes, and it is the checking that takes the time.

In practice, a well-run comparative study gathers between five and twenty cases. When the
number grows far beyond that, it is usually a sign that the research question was not
narrowed down enough — or that the work is a large-scale study, which needs other tools.

For large-scale studies — factorial matrices of city, area, demand and volume, or uncertainty
propagation — the program offers a command-line interface, described next.

---

## The command line

Installing the program as a Python package registers the `triton` command, which runs the
same calculation routines as the graphical interface without opening the window; the Windows
installer with the graphical interface does not include it. The command line reads `.triton`
files, projects in structured JSON and a legacy semicolon-separated text format, and writes the results in
text, JSON, CSV, HTML or XLSX. It is the interface suited to reproducible studies, because the
command itself documents the assumptions changed.

<!-- tabela: Subcommands of the command line and the purpose of each one -->
| Subcommand | Purpose |
| :--- | :--- |
| `validate` | checks the structure of the project, the rainfall series and the essential assumptions, without simulating |
| `run` | simulates the project; by default, only the technical analysis |
| `analyze` | runs the complete chain: technical, economic, environmental, weight of the system and TOPSIS |
| `econ` | runs the economic analysis |
| `init` | creates a template `.triton` project, editable, with the rainfall series referenced or embedded |
| `init-catalog` | creates a template JSON catalogue of building or climate assumptions |
| `matrix` | combines a catalogue of assumptions with a catalogue of climates and simulates every combination |
| `matrix-projects` | runs a list of projects, a folder of rainfall series or the factorial matrix declared in the project |
| `batch` | runs the scenarios of a CSV or XLSX spreadsheet, from a base project |
| `uncertainty` | propagates uncertainties by Monte Carlo for one tank volume |
| `series-length` | answers how many years of rain the project needs, by the method of Geraldi and Ghisi |
| `stochastic-demand` | draws the daily consumption at random and returns the performance as a range, not as a single number |
| `estudo` | organises, runs and reports batch studies from JSON (`estudo.json`): many buildings per typology, with paper-ready tables |

The subcommands `run`, `analyze` and `econ` accept the same options: `--analysis` chooses the
analysis (`technical`, `economic`, `environmental`, `system_weight`, `topsis` or `all`); `--volume`
fixes the lower tank volume, in litres; `--rainfall` replaces the project's rainfall series;
`--set FIELD=VALUE` changes a project field and can be repeated; `--weights t,e,a,s` gives the
four TOPSIS dimension weights — technical, economic, environmental and structural — or eight
weights, one per criterion, or `critic` for objective weights computed from the results by the
CRITIC method (three weights, as in version 0.1.0, are still accepted, and the structural dimension
receives their mean; seven are refused); `--criterion-shares` gives the eight criterion shares, in
the order reliability, storage efficiency, net saving, LCOW, payback, CO₂, dry mass and overflow
(default `1,1,1,1,1,1,1,1`); `--score-band T` sets the tolerance of the choice band, from 0 to 1
(default `0.05`, 5% of the score range); `--weight-sensitivity N` draws N weight vectors and
reports how often each volume wins (with `critic`, it draws the four dimension weights);
`--format` and `--output` set the output format and file; and `--seed` fixes the seed of the
stochastic analyses, so that the result is reproducible. `--score-band` is accepted by every
subcommand that takes `--weights`. In the project file, the same weights go in
`analysis.topsis_weights` (four or eight values, or `"critic"`), the shares in
`analysis.topsis_criterion_shares` (eight values) and the tolerance in
`analysis.topsis_score_band`.

The ranking comes out as a band, not as a single volume. The text output reads «TOPSIS: volumes
from A to B L have similar scores (within 5% of the range, from the highest) | highest score at
X L (s)»; the HTML report has a «Choice band (TOPSIS)» paragraph; and the JSON carries
`topsis.choice_band` — the volumes of the band, the tolerance, whether the band is contiguous and
the volume of the highest score — with `topsis.choice_band_min_volume_l`,
`topsis.choice_band_max_volume_l` and `smaa_vikor.choice_band`. With `critic`, the weights the
program computed are in `topsis.criteria`, one per criterion.

With `--analysis all` (or `system_weight`), `analyze` also reports the **weight of the system**: the
dry mass, the water load and the operating load, in kg and kN, split into basement or lower level,
roof or upper level, and risers and network. The HTML report, the spreadsheet (sheet
`system_weight` for the chosen volume; the values per volume are in the sheet `alternatives`) and
the terminal text show it. Its warnings are attention thresholds of the program, not limits of any
standard — 500 kg on the roof with the upper tank full, an upper tank above 1,500 L, a cistern
above 3,000 kg dry, and any concrete cistern — and each asks you to confirm the load with the
structural or foundation design.

Applied to the tutorial project, `validate` and `run` look like this (the command line prints
a confirmation in the language of the program's interface):

```
triton validate 04_tutorial_sweep.triton

triton run 04_tutorial_sweep.triton --volume 4000 --format json --output r.json
```

The file `r.json` records the provenance (source project, number of days of the series and start
date) and, for the 4,000 L volume, the saving potential of 26.83% and the classification of the
days into full, partial and no supply, with 95.3% full days.

The `uncertainty` subcommand draws, in each sample, the precipitation, the catchment area, the
demand and the investment with a distribution of declared coefficient of variation, and reports
the 5%, 50% and 95% percentiles of the saving potential and of the net present value, with the
probability of the net present value being positive. Run it on the tutorial with a modest number
of samples and a fixed `--seed`, and read the percentiles of the potential as a range, not as a
single number. Because the tutorial system already works close to the 28% ceiling, a moderate
variation in rain or demand moves the potential little, whereas the net present value, which in
the tutorial is negative with the illustrative costs of section {{n:10}}, moves in proportion to
the investment and the tariff. The probabilistic modulation, described in its own chapters, does the same job from
the graphical interface.

The `series-length` subcommand does, with no screen time limit, the analysis the sweep step
offers in the «is the rainfall series long enough?» button, described in section {{n:24}}.
Without `--windows`, it goes through **all** the possible windows, which is the exhaustive mode
of the papers; with `--windows N`, it draws N windows per length, with the declared seed. The
options `--max-volume`, `--step` and `--threshold` define the grid and the marginal-gain
threshold, and `--confidence` and `--tolerance` define the similarity criterion.

The `stochastic-demand` subcommand draws the consumption **day by day** and runs the simulation
many times, returning the saving potential, the days of full supply and the overflow as a range
between the 5% and 95% percentiles. There are two variation parameters, and the difference
between them is what the subcommand has to teach: `--daily-cv` is the variation from one day to
the next, and `--level-uncertainty` is the uncertainty about how much the building consumes on
average. ==The first hardly moves the result — drawn independently every day, it cancels out
over a thirty-year series —, and the second does.== With `--absence` you declare the probability
of a day with no consumption at all, such as a trip, and with `--ideal-volume` the program also
works out the ideal volume of each realisation, which is what measures whether the design
decision withstands the uncertainty of consumption.

This subcommand has no equivalent in the graphical interface, and that is a design decision:
there are many parameters, reading them requires care, and on the screen they would confuse
more than they would help.

> The subcommands `compare-mass` and `run-vaz-study` run research studies of the group on climate
> databases of tens of thousands of series, and require the files of those databases; they are not
> part of the everyday use of the program.

---

## Batch studies from JSON

When the comparison is by **typology** (schools, commercial buildings, single-family and multi-family housing, hospitals, airports) and the result goes into a paper or a conference abstract, keeping one saved project per case and building the spreadsheet by hand stops paying off. The `estudo` subcommand of the command line organises the study in an `estudo.json` file: the base project, the cases, what changes from one case to the next, the analysis and the outputs. The program runs every case in a stable order and writes ready tables.

```powershell
# 1. A skeleton study, with the labels of the typology and no value filled in.
triton estudo init .\schools --tipologia escolar

# 2. Fill in schools\estudo.json (the «XX» and null entries) and put the .triton files and series in schools\casos.
triton estudo validate .\schools\estudo.json

# 3. Run every case (in a stable order); --paralelo N uses N processes and does not change the result.
triton estudo run .\schools\estudo.json --saida .\out\schools --paralelo 4

# 4. Rebuild the tables without recomputing (for example after changing metrics or decimal places).
triton estudo resumo .\out\schools

# 5. Fill the conference abstract template with the real numbers.
triton estudo texto .\out\schools --modelo .\schools\modelo_texto.md

# 6. Several studies (a folder with estudo*.json files), with the comparison between typologies.
triton estudo lote .\studies --saida .\out\comparison

# 7. Gather the resultados.csv of many runs into one table (typology, case, metric: minimum, mean, median, maximum).
triton estudo consolidar .\out --saida .\out\consolidated
```

The typologies (`escolar` school, `comercial` commercial, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar` hospital, `aeroportuario` airport) are structure and labels only: `estudo init --tipologia` writes the label, the `grupo` of the cases and, in a comment, what `usuarios` means in that typology. No number comes with the typology: area, demand, users and share come from your cases, with the source of each.

The `consolidar` action searches every `resultados.csv` under the given folders (several studies, batches, repeated runs) and writes `consolidado.csv` and `consolidado.md` to the output folder: one row per typology (`grupo`), case and metric, with `n`, minimum, mean, median and maximum of the values of the cases that finished (`status` ok). The unit is part of the group key, so different currencies are never mixed. Numbers have the same format as in `resultados.csv` (decimal point, ten significant digits); the Markdown table follows `--idioma`. If the optional `duckdb` package is installed (optional `analise` extra, not part of the installer), it reads and groups the files; without it the standard library does the same, and the two paths give the same bytes (`--motor csv` forces the second; `--motor duckdb` demands the package).

`estudo run` and `estudo lote` show their progress on the error stream. `--progresso simples` writes one line per case (`[i/N] id: ok (t s)`); `--progresso rich` draws a progress bar and needs the optional `rich` package (optional `cli` extra; without it the program warns once and uses `simples`); the default `auto` uses `rich` only if it is installed and the error stream is a terminal. The result files are identical in bytes in every mode, and `--quiet` turns the progress off.

In the `analise` section, `pesos` takes the four dimension weights, eight criterion weights or `"critic"` (three weights, from studies made up to version 0.1.0, are still accepted), `partes_no_eixo` the eight criterion shares and `tolerancia_faixa` the tolerance of the choice band, from 0 to 1 (default 0.05); a study that declares seven values, from the model of version 0.1.0, is refused at validation. The metrics `faixa_topsis_min_l` and `faixa_topsis_max_l` give the ends of the TOPSIS choice band of each case, so that the tables of a paper report a band and not a single volume.

What each section of `estudo.json` contains, the aliases of the substitutions (catchment area, demand, users, share, tank volume and others) and the output files are in the appendix «Files, folders and formats». The example `examples/estudos/residencial-unifamiliar-exemplo/` runs the tutorial house in New York, London and Cape Town (`new_york.triton`, `london.triton`, `cape_town.triton`): `triton estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida out\example`.

The ERA5 example series carry the Open-Meteo/Copernicus credit (CC BY 4.0), which the outputs inherit from `analyze` and repeat in the summary, in the tables and in `resultados.json`. Record the source, period and treatment of any series of your own in the protocol of the study.

> **The program organises; the analyst decides.** No field of the skeleton comes filled in, and an «XX» or a `null` stops the run. The area, demand, number of users and eligible share of each building must come from a source that the study cites. The summary warns when the costs were not entered (CAPEX equal to zero), because then the net present value and the payback are not results.
