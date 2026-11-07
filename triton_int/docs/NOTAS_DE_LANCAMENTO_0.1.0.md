# Triton, International Edition (INT): release notes for version 0.1.0

Version 0.1.0 (beta), release date to be set. This is the first version of Triton and the first of the International Edition. These notes say what the version brings, what it does not, what is known not to be perfect and what was not verified. The datasets are described in [`DADOS.md`](DADOS.md); the full history is in [`../CHANGELOG.md`](../CHANGELOG.md); the manual is [`../manual/en/Triton-User-Manual.pdf`](../manual/en/Triton-User-Manual.pdf).

**In short: this edition is region-neutral.** It ships no regional rainfall, tariff, cost or emission-factor data. You supply them. Three worked examples (New York, London, Cape Town) are included so that the program opens with something to run.

## What it is

Triton sizes rainwater harvesting systems for buildings. It runs a daily water balance over a precipitation series, sweeps a range of tank volumes, and reports what each volume delivers in potable water saved, money and life-cycle carbon, then ranks the alternatives by multi-criteria decision analysis (TOPSIS and SMAA-VIKOR).

## Install

| | |
| :--- | :--- |
| Windows installer | `Triton_Internacional_Setup_v0.1.0.exe`, published in the Zenodo record (DOI 10.5281/zenodo.23402916), not code-signed: Windows may show a SmartScreen warning. The SHA-256 of each installer is in the record's `SHA256SUMS.txt` (the installer is not bit-for-bit reproducible: each build records the date). No Python needed. |
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

## Data and licences in one line

Example rainfall: Open-Meteo / ERA5, CC BY 4.0, attribution required. Example tariffs: published prices transcribed with the source cited; the utilities' documents are not redistributed and the licence of their websites was not checked. 3D viewer: CC0 1.0 (sky) and MIT (three.js). Detail in [`DADOS.md`](DADOS.md).

## What was verified and what was not

Verified: the three example projects open, run through the 13 steps, recompute the economics and the decision, produce the three reports and the audit spreadsheet, save the `.triton` file and reopen it with the same result; the command line works; the four interface languages open without error; the New York, London and Cape Town bills are recomputed by automatic tests.

Verified on 25 Oct 2026, on the installer and the frozen program of this build: the installer (final name) was run silently into a temporary folder, installed, the installed program ran `--diagnostico` and `cli validate`/`cli run` with numerical results equal to those of the source code, and it uninstalled cleanly. The frozen program also ran with a reduced PATH, away from the repository. SHA-256 of the files tested: installer `28ee7c901ae156d574a957729761986ceaf0a859efb91d49c72a7d59a058e3c3`; program `a9e0c49c808c388be928d256b99bc19df933f7b3bd98c4f048738c7714fa667e`. The installers are **not bit-for-bit reproducible** (each build records the date and the revision): the hash holds for these files, and the installer to be published must be measured again.

Not verified: the window on a real display beyond its title (the window opened and stayed responsive for 30 s; the checks otherwise used an off-screen display), the WebGL 3D view, printing the PDFs, a real clean machine (a virtual machine without Python), Windows Defender/SmartScreen, code signing, an all-users installation, the `.triton` file association and the Start-menu shortcuts.

## Report a problem

State the version (0.1.0), the edition and the steps, and attach the `.triton` file. Contact: igor.catao@posgrad.ufsc.br.

## How to cite

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings.* Federal University of Santa Catarina (UFSC). When a study uses the example rainfall, also credit Open-Meteo.com (CC BY 4.0) and Hersbach et al. (2020).
