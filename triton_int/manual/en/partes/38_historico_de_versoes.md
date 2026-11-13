# Version history and what changed

This section records what changed between versions of the program and, above all, **which changes
alter results already published**. The distinction matters more than it seems: a fix to the
interface affects no earlier study, whereas a fix to a calculation can shift every number of a
paper already submitted. Anyone who has published with Triton needs to know into which category
each change falls, and that is why the history below separates the two explicitly.

==The rule guiding this whole section is simple: a calculation fix obliges you to declare the
version used; an interface fix does not.==

---

## The version you are using

The version number appears in the sidebar, in the footer and in the **About Triton** menu. It is
also saved inside each project file and printed in each report, so that an old study always
carries with it the identification of the program that produced it. The redundancy is deliberate:
reports circulate separately from files, and the question «which version was this done with?»
usually comes up months later, when nobody remembers.

The numbering scheme follows the usual software engineering convention. The first number indicates
the generation of the program, and changing it means a reformulation of the conceptual model; the
second indicates a set of new features; and the third indicates fixes and adjustments that do not
change the architecture. A first number of zero marks a beta: the program is usable and verified as section {{n:34}}
describes, but its interface, file format and defaults may still change, and a change may alter
results.

The current version is the beta **0.2.0**. The only earlier version is the beta 0.1.0, published
on 5 November 2026 with its own DOI, 10.5281/zenodo.23402916. Version 0.2.0 changes the
multi-criteria decision, so a study made with 0.1.0 is reproduced with 0.1.0.

---

## How this history is kept

From now on, each version released gets an entry of its own in this section, with the release date
and what changed, always split into two lists: ==what alters the results of studies already done and
what does not.== The most recent entry comes first.

Each entry follows the same model, so that two versions can be compared without rereading: a
one-sentence summary, the new features, the fixes that alter results, those that do not, and what
changed in the documentation. Sections with no content in that version simply do not appear.

The same list is distributed with the code, in the `CHANGELOG.md` file at the root of the
repository, and feeds the versions page of the documentation site.  It is written here first,
and the maintainers keep the other two equal to it. Those following the program through the
repository, the site or the manual read the same record.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Version 0.2.0 (beta) — 11 November 2026

> **In one sentence.** The multi-criteria decision moves from seven criteria in three dimensions to eight criteria in four — technical, economic, environmental and structural — and the program now calculates the weight of the system.

### What is new

- **Eight criteria in four dimensions.** Technical: volumetric reliability and storage efficiency. Economic: net financial savings (the NPV against the baseline without a cistern), the levelised cost of water (LCOW) and the discounted payback. Environmental: the net life-cycle CO₂e. Structural: the dry mass of the materials and the annual overflow. Section {{n:32}} defines each one as the program computes it, with the LCOW equation.
- **Weights by dimension, with criterion shares.** Four dimension weights, 25% each by default, each shared among the criteria of its dimension by the criterion shares, equal by default. Eight direct weights, one per criterion, are also accepted. TOPSIS, VIKOR and PROMETHEE II use the same rule; SMAA-VIKOR draws eight weights, with 25% expected on each dimension, and gives the central weights per criterion and per dimension.
- **The decision tab.** One card per dimension (Technical, Economic, Environmental, Structural), with the dimension weight at the top and the criterion shares of its criteria below; the «Equal shares» and «Recalculate» buttons below the cards; the profiles «Balanced: 25% on each dimension», «Prioritise …» with 70% on one dimension and 10% on each of the others, including «Prioritise Lightness and Drainage», and «Objective weights (CRITIC), computed from the results».
- **Command line, project file and declarative study.** `--weights t,e,a,s` (or eight values, or `critic`), `--criterion-shares` with eight values (default `1,1,1,1,1,1,1,1`) and `--score-band` (default `0.05`); `analysis.topsis_weights` (four or eight values, or `"critic"`), `analysis.topsis_criterion_shares` (eight) and `analysis.topsis_score_band` in the project file; `analise.pesos` (four or eight, or `"critic"`), `analise.partes_no_eixo` (eight) and `analise.tolerancia_faixa` in `estudo.json`, with the metrics `faixa_topsis_min_l` and `faixa_topsis_max_l`.
- **Objective weights by CRITIC.** Instead of declaring the weights, the analysis can compute them from its own results by the CRITIC method (Diakoulaki, D.; Mavrotas, G.; Papayannakis, L., 1995. Determining objective weights in multiple criteria problems: the CRITIC method. *Computers & Operations Research*, 22(7), 763–770, doi:10.1016/0305-0548(94)00059-H): each criterion weighs by its contrast across the volumes times its independence from the other criteria. The weights hold for TOPSIS, VIKOR and PROMETHEE II, are recomputed at every analysis and change with the set of volumes evaluated. It is a choice of method, not a default: the default is still 25% on each dimension. In the decision tab, the profile «Objective weights (CRITIC), computed from the results»; on the command line, `--weights critic`; in the project file, `analysis.topsis_weights: "critic"`; in the declarative study, `analise.pesos: "critic"`.
- **A choice band instead of a single volume.** When several volumes score alike, the program no longer names one «best volume»: it reports the volumes whose score, rescaled from the worst (0) to the best (1) of the volumes evaluated, lies within a tolerance of the best — 5% of the score range by default — and the volume with the highest score as information. The rule holds for TOPSIS, VIKOR, PROMETHEE II and SMAA. The decision tab, the text, HTML and JSON outputs of the command line and the metrics of the declarative study show the band; the tolerance is set with `--score-band`, `analysis.topsis_score_band` or `analise.tolerancia_faixa`.
- **Weight of the system.** `triton analyze … --analysis all` (and `--analysis system_weight`) reports the dry mass, the water load and the operating load, in kg and kN, split into basement or lower level, roof or upper level, and risers and network. The HTML report, the spreadsheet (sheet `system_weight`) and the terminal text show the block. Its warnings are attention thresholds of the program, not of any standard — 500 kg on the roof with the upper tank full, an upper tank above 1,500 L, a cistern above 3,000 kg dry, and any concrete cistern — and ask for a check with the structural or foundation design.

### Fixes that change results

The multi-criteria model was replaced. A study that ranked volumes with version 0.1.0 can rank them differently with this version.

<!-- tabela: Fixes that change results in version 0.2.0 -->
| What was corrected | Effect on the result |
| :--- | :--- |
| The multi-criteria decision used seven criteria in three dimensions, and three of them — the saving potential, the potable water consumption and, through the bill, the NPV — measured the same water saved. It now uses eight criteria in four dimensions, with the weight of the system. | The volume chosen by TOPSIS, VIKOR, PROMETHEE II and SMAA-VIKOR can change. In the New York tutorial, with equal weights, TOPSIS moves from 4,000 L to 2,000 L. Three weights from a project or study of version 0.1.0 are still accepted: the structural dimension receives their mean, so equal weights stay equal. Seven values, weights or shares of the old model, are refused with a message that says why. SMAA-VIKOR now draws the eight weights with 25% expected on each dimension; version 0.1.0 drew them uniformly over the criteria, so a dimension with more criteria weighed more on average, and every acceptability changes. To reproduce a study made with version 0.1.0, use version 0.1.0 (DOI 10.5281/zenodo.23402916). |

### Fixes that do not change results

None.

### Documentation

Sections {{n:12}}, {{n:19}}, {{n:32}} and {{n:37}} describe the eight criteria, the LCOW, the weight rule, the objective weights of CRITIC, the choice band, the options of the command line and the weight of the system; section {{n:13}} asks a study to report the band and its tolerance, and the CRITIC weights when it used them. Section {{n:12}} now says plainly that the multi-criteria analysis with equal weights indicates a band of 2,000 to 3,000 L, why the tutorial keeps the 4,000 L of the hydraulic criterion, and what that choice gives up. The interactive figure of the decision on the site has four dimension weights, the criterion shares and the choice band. The release notes are in `docs/NOTAS_DE_LANCAMENTO_0.2.0.md`. Version 0.2.0 has no DOI of its own yet: cite the DOI of all versions, 10.5281/zenodo.23402915, which always resolves to the most recent one.

---

## Version 0.1.0 (beta) — 5 November 2026

> **In one sentence.** First beta of Triton, with its own name for each edition, in the same repository and with the same version numbering.

### What is new

Triton simulates rainwater harvesting day by day and carries the simulation engine, the life-cycle
assessment, the treatment line, the multi-criteria decision and the probabilistic modulation. This is
the first version of the International Edition, which has its own name and logo and shares the repository and version numbering with the other editions.
The Fewkes operating rule (φ) is available as an option in every module.

**What the International Edition brings in this version.**

- **A region-neutral program.** It ships no regional rainfall database, no tariff catalogue, no cost catalogue and no emission-factor series, and it applies no national standard and no predefined currency. You supply the rainfall series of the site, the tariffs, the costs and the currency.
- **Three worked examples.** New York, London and Cape Town, with one building and three rainfall series (ERA5 reanalysis via Open-Meteo, 1991 to 2020, CC BY 4.0) and three tariff structures, each checked by hand against its printed bill.
- **The analysis chain.** Daily water balance, volume sweep and ideal volume, economic analysis with block tariffs and six tariff regimes, life-cycle assessment, treatment line, certification scoring, multi-criteria ranking, reports in PDF and spreadsheet, CAD and BIM exports.
- **Batch studies from JSON.** The `triton estudo` subcommand organises a study in an `estudo.json` (base project, cases by typology, parameter substitutions by alias, analysis and outputs), runs every case in a stable order, with resume and parallel execution, and writes paper-ready tables: tidy CSV, JSON with provenance (version, edition, SHA-256, rainfall source and licence), Markdown, LaTeX (booktabs) and XLSX. A text template with markers receives the real numbers and leaves «XX» where a result is missing. A worked study is in `examples/estudos/`.
- **Documentation.** The complete manual in English, an offline site, short volumes and `docs/DADOS.md`, which describes every dataset with its source, licence and quality.

**What this version does not have.**

- **Regional data.** No rainfall database, no climate projections, no tariff catalogue.
- **Prices.** The program does not calculate an investment from prices. Cistern, tank, piping, accessories, labour, pump and maintenance costs start at zero, and so do the electricity tariff and the price of chlorine; the water tariff is empty. Section {{n:10}} says what a new project contains and what you enter.
- **Emission factors.** The grid factor is zero until you enter the factor of your grid.
- **Verified example tariffs.** The three example tariffs are illustrative.

**Known limitations.**

- The address of each tariff document, its access date and its checksum were not recorded when the examples were built, so the figures cannot be traced to a stored copy; the effective dates of the London and Cape Town tariffs are inferred. The payback and the net present value shown for the example projects are not results.
- The example rainfall series are reanalysis grid cells of about 9 km, not rain-gauge records.
- The CAPEX dialog has no field for the cistern price and sets it back to zero on confirming; section {{n:10}} gives the way round. With no price list, the cistern price you enter applies to every volume of the volume sweep. The price of chlorine can be set only in the project file.
- In Spanish and Chinese the interface is partly translated, and the reports in those languages contain passages in another language; English is complete.
- The life-cycle steps warn that country factors are missing, by design.

### Fixes that change results

None: this is the first beta, and there is no earlier version to correct.

<!-- tabela: Fixes that change results in version 0.1.0 -->
| What was corrected | Effect on the result |
| :--- | :--- |

### Fixes that do not change results

None.

### Documentation

The manual gained the sections «CAPEX in this edition», «What goes into the running cost (OPEX)», «Regional and national particulars» and «Description of the data and how far to trust it».

---

## How to tell whether your version has a fix

The procedure is direct and does not depend on asking anyone: open one of the example files that
come with the program, described in appendix {{n:J}}, run it, and compare the result obtained with
the value printed in this manual. Each example case was generated by the same version of the program
that generated this manual, and each published number has a matching automatic check, as section
{{n:34}} describes. A divergence, therefore, indicates that the installed program is not that of this
manual's version.

==If the numbers match, your installation corresponds exactly to the manual you have in hand.== If
they do not, the difference is not a defect of your installation, but a version difference that
needs to be identified before any study.

---

## What to declare in a published work

Good practice in computational reproducibility requires a paper to identify unambiguously the
program that produced the results. In Triton's case, four items of information are enough, and all
are available without effort: the version of the program, which appears in the report; the source of
the precipitation series, with the period used; the tariff structure adopted, with its effective
date; and a statement of which parameters were changed from the default values. Section {{n:13}}
gives the full list, with a ready-made method paragraph to adapt.

Attaching the `.triton` file to the supplementary material settles all four at once, because the file
is self-contained and carries the rainfall series inside it. It is the most economical way of
making a study verifiable by others, and costs a small attachment.
