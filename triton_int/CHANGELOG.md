# What is new in each version of Triton (International Edition)

This file mirrors the version-history section of the user manual
(`manual/en/partes/38_historico_de_versoes.md`). Write there first, and keep the two equal.

Each version carries the same sections: a one-sentence summary, what is new, **the fixes that
change the results of studies already done**, those that do not, and what changed in the
documentation. The distinction between the two kinds of fix is the one that matters most to
anyone who publishes with the program: a calculation fix obliges you to declare the version
used in a work; an interface fix does not.

The current version is 0.1.0. The complete manual is `manual/en/Triton-User-Manual.pdf`, and
the data of the edition are described in `docs/DADOS.md`.

---

## Version 0.1.0 (beta) — October 2026

> **In one sentence.** First beta of Triton, with its own name, versioning and repository for
> each edition.

### What is new

Triton simulates rainwater harvesting day by day and carries the simulation engine, the life-cycle
assessment, the treatment line, the multi-criteria decision and the probabilistic modulation. This is
the first version of the International Edition, which has its own repository, logo and numbering.
The Fewkes operating rule (φ) is available as an option in every module.

**What the International Edition brings in this version.**

- **A region-neutral program.** It ships no regional rainfall database, no tariff catalogue, no cost catalogue and no emission-factor series, and it applies no national standard and no predefined currency. You supply the rainfall series of the site, the tariffs, the costs and the currency.
- **Three worked examples.** New York, London and Cape Town, with one building and three rainfall series (ERA5 reanalysis via Open-Meteo, 1991 to 2020, CC BY 4.0) and three tariff structures, each checked by hand against its printed bill.
- **The analysis chain.** Daily water balance, volume sweep and ideal volume, economic analysis with block tariffs and six tariff regimes, life-cycle assessment, treatment line, certification scoring, multi-criteria ranking, reports in PDF and spreadsheet, CAD and BIM exports.
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
