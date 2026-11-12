# What is new in each version of Triton (International Edition)

This file mirrors the version-history section of the user manual
(`manual/en/partes/38_historico_de_versoes.md`). Write there first, and keep the two equal.

Each version carries the same sections: a one-sentence summary, what is new, **the fixes that
change the results of studies already done**, those that do not, and what changed in the
documentation. The distinction between the two kinds of fix is the one that matters most to
anyone who publishes with the program: a calculation fix obliges you to declare the version
used in a work; an interface fix does not.

The current version is 0.2.0. The complete manual is `manual/en/Triton-User-Manual.pdf`, and
the data of the edition are described in `docs/DADOS.md`.

---

## Version 0.2.0 (beta) — 11 November 2026

> **In one sentence.** The multi-criteria decision moves from seven criteria in three dimensions to eight criteria in four — technical, economic, environmental and structural — and the program now calculates the weight of the system.

### What is new

- **Eight criteria in four dimensions.** Technical: volumetric reliability and storage efficiency. Economic: net financial savings (the NPV against the baseline without a cistern), the levelised cost of water (LCOW) and the discounted payback. Environmental: the net life-cycle CO₂e. Structural: the dry mass of the materials and the annual overflow. The manual's section «Multi-criteria decision» defines each one as the program computes it, with the LCOW equation.
- **Weights by dimension, with criterion shares.** Four dimension weights, 25% each by default, each shared among the criteria of its dimension by the criterion shares, equal by default. Eight direct weights, one per criterion, are also accepted. TOPSIS, VIKOR and PROMETHEE II use the same rule; SMAA-VIKOR draws eight weights and gives the central weights per criterion and per dimension.
- **The decision tab.** Four weight boxes (Technical, Economic, Environmental, Structural), the profiles «Balanced: 25% on each dimension» and «Prioritise …» with 70% on one dimension and 10% on each of the others, including «Prioritise Lightness and Drainage», and the «Criterion shares» row with eight boxes and the «Equal shares» button.
- **Command line, project file and declarative study.** `--weights t,e,a,s` (or eight values) and `--criterion-shares` with eight values (default `1,1,1,1,1,1,1,1`); `analysis.topsis_weights` (four or eight values) and `analysis.topsis_criterion_shares` (eight) in the project file; `analise.pesos` (four or eight) and `analise.partes_no_eixo` (eight) in `estudo.json`.
- **Weight of the system.** `triton analyze … --analysis all` (and `--analysis system_weight`) reports the dry mass, the water load and the operating load, in kg and kN, split into basement or lower level, roof or upper level, and risers and network. The HTML report, the spreadsheet (sheet `system_weight`) and the terminal text show the block. Its warnings are attention thresholds of the program, not of any standard — 500 kg on the roof with the upper tank full, an upper tank above 1,500 L, a cistern above 3,000 kg dry, and any concrete cistern — and ask for a check with the structural or foundation design.

### Fixes that change results

The multi-criteria model was replaced. A study that ranked volumes with version 0.1.0 can rank them differently with this version.

| What was corrected | Effect on the result |
| :--- | :--- |
| The multi-criteria decision used seven criteria in three dimensions, and three of them — the saving potential, the potable water consumption and, through the bill, the NPV — measured the same water saved. It now uses eight criteria in four dimensions, with the weight of the system. | The volume chosen by TOPSIS, VIKOR, PROMETHEE II and SMAA-VIKOR can change. In the New York tutorial, with equal weights, TOPSIS moves from 4,000 L to 2,000 L. Three weights from a project or study of version 0.1.0 are still accepted: the structural dimension receives their mean, so equal weights stay equal. Seven values, weights or shares of the old model, are refused with a message that says why. To reproduce a study made with version 0.1.0, use version 0.1.0 (DOI 10.5281/zenodo.23402916). |

### Fixes that do not change results

None.

### Documentation

The manual's sections «Which volume to choose, after all», «Comparing many cases at once», «Multi-criteria decision» and «Error messages and what to do» describe the eight criteria, the LCOW, the weight rule, the options of the command line and the weight of the system. The section «Which volume to choose, after all» now says plainly that the multi-criteria analysis with equal weights indicates 2,000 L, why the tutorial keeps the 4,000 L of the hydraulic criterion, and what that choice gives up. The interactive figure of the decision on the site has four dimension weights and the criterion shares. The release notes are in `docs/NOTAS_DE_LANCAMENTO_0.2.0.md`. Version 0.2.0 has no DOI of its own yet: cite the DOI of all versions, 10.5281/zenodo.23402915, which always resolves to the most recent one.

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
- **Prices.** The program does not calculate an investment from prices. Cistern, tank, piping, accessories, labour, pump and maintenance costs start at zero, and so do the electricity tariff and the price of chlorine; the water tariff is empty. The manual's section «What it costs and how fast it pays back» says what a new project contains and what you enter.
- **Emission factors.** The grid factor is zero until you enter the factor of your grid.
- **Verified example tariffs.** The three example tariffs are illustrative.

**Known limitations.**

- The address of each tariff document, its access date and its checksum were not recorded when the examples were built, so the figures cannot be traced to a stored copy; the effective dates of the London and Cape Town tariffs are inferred. The payback and the net present value shown for the example projects are not results.
- The example rainfall series are reanalysis grid cells of about 9 km, not rain-gauge records.
- The CAPEX dialog has no field for the cistern price and sets it back to zero on confirming; the manual's section «What it costs and how fast it pays back» gives the way round. With no price list, the cistern price you enter applies to every volume of the volume sweep. The price of chlorine can be set only in the project file.
- In Spanish and Chinese the interface is partly translated, and the reports in those languages contain passages in another language; English is complete.
- The life-cycle steps warn that country factors are missing, by design.

### Fixes that change results

None: this is the first beta, and there is no earlier version to correct.

### Fixes that do not change results

None.

### Documentation

The manual gained the sections «CAPEX in this edition», «What goes into the running cost (OPEX)», «Regional and national particulars» and «Description of the data and how far to trust it».
