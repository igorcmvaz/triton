# Triton, International Edition (INT): release notes for version 0.1.0

Version 0.1.0 (beta), 15 October 2026. This is the first version of Triton and the first of the International Edition. These notes say what the version brings, what it does not, what is known not to be perfect and what was not verified. The datasets are described in [`DADOS.md`](DADOS.md); the full history is in [`../CHANGELOG.md`](../CHANGELOG.md); the manual is [`../manual/en/Triton-User-Manual.pdf`](../manual/en/Triton-User-Manual.pdf).

**In short: this edition is region-neutral.** It ships no regional rainfall, tariff, cost or emission-factor data. You supply them. Three worked examples (New York, London, Cape Town) are included so that the program opens with something to run.

## What it is

Triton sizes rainwater harvesting systems for buildings. It runs a daily water balance over a precipitation series, sweeps a range of tank volumes, and reports what each volume delivers in potable water saved, money and life-cycle carbon, then ranks the alternatives by multi-criteria decision analysis (TOPSIS and SMAA-VIKOR).

## Install

| | |
| :--- | :--- |
| Windows installer | `Triton_INT_Setup_0_1_0.exe`, published on Zenodo with its SHA-256 checksum. No Python needed. [A COMPLETAR: Zenodo record address and installer SHA-256, after publication] |
| From source | Python 3.12 or later; `pip install -r requirements.txt`; `python main.py` (interface) or `python -m triton.cli --help` (command line) |
| Size | The tracked edition totals about 43 MiB, 28 MiB of which is the manual; the data files together are under 3 MiB |

The checks for this version were made on Windows. The licence is academic source-available, free for non-commercial use, and citing the program is mandatory (`LICENSE.md`, `CITATION.cff`).

## What the International Edition brings

- **A neutral core.** No regional database, no national standard, no predefined currency. The interface opens in English; every value is read in the currency of the project.
- **Three worked examples.** One building in three cities, with ERA5 reanalysis rainfall (1991 to 2020, CC BY 4.0) and three tariff structures: New York (US$, single rate with sewer at 159% of the water charge), London (£, volumetric charges with standing charges) and Cape Town (R, stepped blocks).
- **The analysis chain.** Daily water balance, volume sweep and ideal volume, economics with block tariffs and six tariff regimes (NPV, IRR, payback), simplified life-cycle assessment, treatment line, certification scoring (LEED, EDGE, GRI), multi-criteria ranking, probabilistic modulation.
- **Outputs.** PDF reports (executive, environmental/ESG and technical dossier), audit spreadsheet, DXF, glTF/HTML and BIM manifest.
- **Documentation.** The complete manual in English (PDF, offline site, short volumes), with the new sections «CAPEX in this edition», «What goes into the running cost (OPEX)», «Regional and national particulars» and «Description of the data and how far to trust it».

## What is not there

- **Regional data of any kind**: rainfall databases, climate projections, tariff or cost catalogues.
- **Prices.** The program does not calculate an investment from prices. Every cost, the electricity tariff and the price of chlorine start at zero, and the water tariff is empty. Without your values, payback and net present value say little (manual, section 10).
- **Emission factors.** The grid factor is zero until you enter yours.

## Known limitations

- The example tariffs are illustrative. The address of each tariff document, the access date and the SHA-256 were not recorded when the examples were built, and the effective dates of the London and Cape Town tariffs are inferred. The payback and NPV of the example projects are not results.
- The example rainfall series are reanalysis grid cells of about 9 km, not rain-gauge records.
- The CAPEX dialog has no field for the cistern price and sets it back to zero on confirming; section 10 of the manual gives the way round. With no price list, the cistern price you enter applies to every volume of the volume sweep. The price of chlorine can be set only in the project file.
- In Spanish and Chinese the interface is partly translated, and the reports in those languages contain passages in another language; English is complete.
- The life-cycle steps warn that country factors are missing, by design.
- `triton/data/costs_database.json`, a core file, carries reference-cost parameters of one particular region and currency. This edition does not apply it, but the file still ships with the package.

## Data and licences in one line

Example rainfall: Open-Meteo / ERA5, CC BY 4.0, attribution required. Example tariffs: published prices transcribed with the source cited; the utilities' documents are not redistributed and the licence of their websites was not checked. 3D viewer: CC0 1.0 (sky) and MIT (three.js). Detail in [`DADOS.md`](DADOS.md).

## What was verified and what was not

Verified: the three example projects open, run through the 13 steps, recompute the economics and the decision, produce the three reports and the audit spreadsheet, save the `.triton` file and reopen it with the same result; the command line works; the four interface languages open without error; the New York, London and Cape Town bills are recomputed by automatic tests.

Not verified: the window on a real display (the checks used an off-screen display), the WebGL 3D view, rebuilding the installers under the final name, and printing the PDFs.

## Report a problem

State the version (0.1.0), the edition and the steps, and attach the `.triton` file. Contact: igor.catao@posgrad.ufsc.br.

## How to cite

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings.* Federal University of Santa Catarina (UFSC). When a study uses the example rainfall, also credit Open-Meteo.com (CC BY 4.0) and Hersbach et al. (2020).
