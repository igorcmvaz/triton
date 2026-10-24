# Triton — International Edition

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/licence-academic%20source--available-lightgrey.svg)](LICENSE.md)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Environments%20Research%20Group-005a36)](https://sustainability.ufsc.br/)

**Triton** sizes rainwater harvesting systems for buildings. It runs a daily water balance over a
precipitation series, sweeps a range of tank volumes, and reports what each volume delivers in water
saved, money and life-cycle carbon, then ranks the alternatives by multi-criteria decision analysis
(TOPSIS and SMAA-VIKOR).

This is the **International Edition**: the region-neutral core. It ships no regional rainfall, no tariff
and no cost database. You supply the rainfall series, the water, sewer and energy tariffs, the costs and the
currency of your choice. The user interface opens in English. Daily rainfall series for three worked
examples (New York, London and Cape Town) are included in `data/rainfall/`.

The regional editions share this engine and the version number, and add data for their regions. See the
[repository README](../README.md).

---

## What it does

- **Water balance.** Daily simulation of the tank with mass-closure checks, first-flush discard, and one or
  two tanks (lower tank plus a pumped upper tank).
- **Sizing.** Volume sweeps, the ideal volume by marginal gain, and sensitivity to demand and catchment.
- **Economics.** Water, sewer and energy tariffs (including block tariffs), CAPEX and OPEX, payback, net
  present value and internal rate of return, in the currency you choose.
- **Environment.** Simplified life-cycle assessment and carbon balance, and scoring against LEED v4/v4.1
  (up to 8 points in Water Efficiency; WEc2 indoor water use scores 1 to 6 points for reductions of 25% to 50%,
  with a 20% prerequisite), EDGE and GRI 303.
- **Decision.** Multi-criteria ranking with TOPSIS and SMAA-VIKOR.
- **Outputs.** Executive report, environmental audit and technical dossier in PDF; spreadsheet, CAD
  (DXF) and BIM exports; 3D plant and glTF/HTML models of the piping.

The interface and the reports follow the language and currency of the project. The interface is complete in
English and Portuguese and largely translated into Spanish and Chinese; the reports are complete in English and
Portuguese, and in Spanish and Chinese they are only partly translated (some sentences stay in Portuguese). The
precipitation series comes from a file you choose (CSV with daily values), from a template, or from the
examples.

## Status of version 0.1.0

**Ready.** The daily water balance, volume sweep, economics (block tariffs, NPV, IRR, payback), life-cycle
assessment, treatment line, certification scoring, multi-criteria ranking, probabilistic modulation, reports
(PDF), spreadsheet, DXF/glTF/BIM exports, the manual in English and the documentation of every dataset.
Three worked examples open and run end to end.

**Not there, by design.** Regional rainfall databases, climate projections, tariff and cost catalogues, emission
factors and national standards: you supply them. A new project starts with every cost at zero, an empty water
tariff and a zero grid emission factor; until you enter your own values, payback and net present value say little.

**Known limitations.** The three example tariffs are illustrative and were not traced to stored copies of the
documents; the example rainfall is a reanalysis grid cell, not a gauge record; the CAPEX dialog has no field for
the cistern price (the manual gives the way round); Spanish and Chinese are partly translated. The full list is
in the [release notes](docs/NOTAS_DE_LANCAMENTO_0.1.0.md) and the [changelog](CHANGELOG.md).

## Install and run

**Windows installer.** Published on [Zenodo](../README.md#download), together with its SHA-256 checksum:
`Triton_INT_Setup_0_1_0.exe`. No Python is needed.

**From source** (Python 3.12 or later):

```bash
cd triton_int
pip install -r requirements.txt
python main.py                      # graphical interface
python -m triton.cli --help         # command line
```

Optional: `pip install -e ".[acelerado]"` installs `numba`, which speeds up batch studies (the results are
the same).

## Tests

```bash
cd triton_int
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=INT python -m pytest tests/unit tests/test_essencial.py
```

On Windows PowerShell: `$env:TRITON_EDITION = "INT"; python -m pytest tests/unit tests/test_essencial.py`.
The Qt interface tests are collected only when PySide6 is installed.

## Build the installer

```bash
python build_exe.py --installer      # dist/Triton_INT/ and dist/Triton_INT_Setup_0_1_0.exe
```

It needs Python 3.12 or later, PyInstaller (`requirements-dev.txt`) and [Inno Setup 6](https://jrsoftware.org/isinfo.php).
The package carries no regional database.

**Requirements.** Windows for the installer (the checks of this version were made on Windows); Python 3.12 or later and the packages in `requirements.txt` to run from source.

## Documentation

- [User manual (PDF)](manual/en/Triton-User-Manual.pdf)
- [Release notes 0.1.0](docs/NOTAS_DE_LANCAMENTO_0.1.0.md) and [changelog](CHANGELOG.md)
- [Getting started](docs/en/getting-started.md), [model](docs/en/model.md), [verification](docs/en/verification.md)
  and [the three editions](docs/en/editions.md)
- [Data: what ships, sources, licences and quality](docs/DADOS.md)
- [Command-line guide](infos_licenses/CLI_USAGE.md)

## Repository layout

```text
triton_int/
├── triton/            Python package: calculation engine, interface and command line
├── tests/             Automated suite (unit, integration, invariants, interface)
├── manual/            The finished manual: PDFs, offline site, short volumes and worked cases
├── docs/              Technical documentation (method, equations, verification)
├── examples/          Worked examples and project templates (.triton)
├── data/              Language packs and the example rainfall series
├── templates/         Project and spreadsheet templates
├── scripts/           Maintenance tools (see scripts/README.md)
├── infos_licenses/    Licence texts, installer texts and third-party notices
├── pyproject.toml     Package metadata
├── build_exe.py       Executable (PyInstaller) and installer (Inno Setup) build
└── main.py            Entry point of the desktop application
```

## Licence and citation

Academic source-available, all rights reserved, free for non-commercial use. Citing the program is
mandatory in any work that uses its results. The full terms are in [`LICENSE.md`](LICENSE.md); how to cite is in
[`CITATION.cff`](CITATION.cff):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings.* Federal University of Santa Catarina (UFSC).

Developed by the Sustainable Environments Research Group (GPAS), Federal University of Santa Catarina.
Questions and bug reports: igor.catao@posgrad.ufsc.br.
