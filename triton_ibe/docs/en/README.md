# Triton, Iberian Edition (IBE): sizing and simulation of building rainwater harvesting systems

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/Licence-academic%20source--available-lightgrey.svg)](../../LICENSE.md)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Environments%20Research%20Group-005a36)](https://sustainability.ufsc.br/)

**Triton** sizes rainwater harvesting systems for buildings. It runs a daily water balance
over a precipitation series, sweeps a grid of tank capacities and reports what each capacity
delivers in potable water saved, money, life-cycle carbon and system weight. It then ranks the
candidates by multi-criteria decision analysis (TOPSIS and SMAA-VIKOR) over eight criteria on four axes.

It is developed by the Sustainable Environments Research Group (*Grupo de Pesquisa em Ambientes
Sustentáveis*) at the Federal University of Santa Catarina (UFSC), and succeeds the Netuno programme (Netuno 4 is the reference of its validation).

This is the **Iberian Edition (IBE, Triton IBE)**. It opens in European Portuguese and works in euros.
It covers Portugal (308 municipalities) and Spain (8,131 municipalities). Daily rainfall comes from
Iberia01 v1.0 (ODbL, 1971 to 2015) for mainland Portugal, peninsular Spain and the Balearic Islands
(8,319 municipalities); the Canary Islands, Madeira and the Azores (118 municipalities) use the ERA5
reanalysis, always at quality level C; Ceuta and Melilla have no series. Every municipality has a quality
level A, B or C. E-OBS (1950 to 2025, non-commercial use only) is an optional source for mainland Portugal.
It brings the water and sewer tariffs of Lisbon, Porto and Funchal with the managing entity, validity
period and source of each value; in Spain, seven municipalities have a transcribed tariff not yet
double-checked, and the others use the INE regional average, which is only indicative. It carries no price database and no emission factors: costs and the grid emission factor start at
zero and are yours to enter. The user manual is written in European Portuguese, and so is the interface
on opening; the other interface languages are English, Spanish and Chinese (the last two only partly
translated). This English documentation is a summary for reviewers and reusers.

The other editions use the same engine and the same version number; see
[`editions.md`](editions.md) for what differs. Version 0.2.0 is a beta. It replaces the seven-criterion,
three-axis multi-criteria model of version 0.1.0 with eight criteria on four axes and adds the system-weight
calculator; the volume the ranking selects can change (see the [release notes](../NOTAS_DE_LANCAMENTO_0.2.0.md),
in European Portuguese). To reproduce a study made with 0.1.0, use 0.1.0.

---

## What the software does

| Stage | What it computes |
| :--- | :--- |
| **Rainfall** | reads a daily precipitation series (CSV), or takes the series of a Portuguese or Spanish municipality from the embedded Iberia01 and ERA5 bases (or, optionally, E-OBS in `data/portugal_eobs.db`); computes rainfall indices |
| **Building** | catchment area, runoff coefficient, first-flush discard depth, non-potable demand (constant, weekly, monthly or a full daily series) |
| **Daily balance** | yield-after-spillage balance, day by day, for every candidate tank capacity; one or two tanks |
| **Indicators** | potable water savings, volumetric and temporal reliability, days of full, partial and no supply, overflow |
| **Water quality** | use classes, a screening treatment train, and the operating cost and energy of disinfection |
| **Economics** | parametric CAPEX, progressive water and sewer tariffs, electricity tariffs, OPEX, NPV, IRR, simple and discounted payback |
| **Carbon** | screening life-cycle assessment: embodied carbon, operational carbon of pumping and treatment, and the credit of mains water avoided (needs emission factors that you enter) |
| **System weight** | dry mass, water load and operating load (kg and kN) in the basement or lower level, on the roof or upper level and in the risers and network, with alerts when a load passes one of the programme's own attention thresholds (not a standard's) |
| **Decision** | TOPSIS, VIKOR, SMAA-VIKOR and PROMETHEE II over the candidate capacities, on eight criteria in four axes: technical (volumetric reliability, storage efficiency), economic (net financial savings, levelised cost of water, discounted payback), environmental (life-cycle CO₂e) and structural (dry material mass, annual overflow); and placement against LEED v4/v4.1, LEED v5, EDGE and GRI 303 |
| **Piping in 3D** | pipe runs from component connection points, with gravity slopes and clash checks; DXF, glTF, interactive HTML and a BIM manifest |

The technical, economic and environmental optima do not in general coincide. Triton computes
all three on one sweep so that the divergence is visible.

### What it deliberately does not do

- It is **not** an urban drainage model: it does not route catchment runoff.
- It is **not** a hydraulic design tool: it does not size pipework by head loss and produces no
  construction drawings.
- The carbon assessment is a **screening** assessment, not an inventory compliant with
  ISO 14040/14044.
- It supplies **no prices or emission factors**. A new project starts with every cost at zero and no grid
  emission factor, and payback and NPV say little until you enter your own values.
- Gridded rainfall is not a gauge record. The island series (ERA5, level C) underestimated the rainfall
  of the island stations tested by 8% to 47%: for a real project there, use the station series. The
  Funchal example uses the ERA5 island base, labelled as such, and its electricity tariff comes from a
  secondary source (a price comparison site) and is flagged yellow in `docs/DADOS.md`.

---

## Installation

The Zenodo records are gathered under the all-versions DOI
[10.5281/zenodo.23402915](https://doi.org/10.5281/zenodo.23402915), which always resolves to the latest
version. The Windows installer of version 0.1.0 (`Triton_Iberica_Setup_v0.1.0.exe`) is in the 0.1.0 record,
DOI [10.5281/zenodo.23402916](https://doi.org/10.5281/zenodo.23402916), with its SHA-256 checksum in
`SHA256SUMS.txt`; version 0.2.0 has no record of its own yet. The installer is not code-signed and needs no
Python. To run from the source code:

Triton needs **Python 3.12 or later** and runs from source on Windows, Linux and macOS.

The repository is public at https://github.com/igorcmvaz/triton.

```bash
git clone https://github.com/igorcmvaz/triton.git
cd triton/triton_ibe
pip install -r requirements.txt
python main.py                      # graphical interface
python -m triton.cli --help         # command line
```

For the test suite, add `requirements-dev.txt`. Full instructions are in
[`getting-started.md`](getting-started.md).

---

## Documentation

| Document | Language | Content |
| :--- | :--- | :--- |
| [`getting-started.md`](getting-started.md) | English | installation, first run, project file, worked example |
| [`editions.md`](editions.md) | English | the three editions: what differs, where in the code |
| [`model.md`](model.md) | English | the computational model: equations, conventions, assumptions and limits |
| [`verification.md`](verification.md) | English | how the software is verified, and against what |
| [`../DADOS.md`](../DADOS.md) | European Portuguese | data that ships with the edition: sources, licences, coverage, quality |
| `../../manual/Manual-Triton.pdf` | European Portuguese | the user manual |
| [`../metodologia.md`](../metodologia.md) | Portuguese | the same model, in full |

---

## Citing

If you use Triton in academic work, cite it as declared in [`CITATION.cff`](../../CITATION.cff), with
the version you used and the all-versions DOI 10.5281/zenodo.23402915, which always resolves to the latest
version (0.2.0 has no DOI of its own yet; 0.1.0 is 10.5281/zenodo.23402916).

## Contributing and support

Send reports to the maintainers (igorcmvaz@gmail.com). For a bug
report, attach the `.triton` project file and the precipitation series that reproduce it: the project
file carries every premise.

## Licence

Academic source-available, all rights reserved, free for non-commercial use; see
[`LICENSE.md`](../../LICENSE.md). Third-party data keep their own licences (see
[`DADOS.md`](../DADOS.md) and `infos_licenses/AVISOS_DE_TERCEIROS.txt`). In particular, the Iberia01 rainfall
is under the ODbL (attribution: «Contains information from Iberia01, made available under the Open Database
License (ODbL 1.0)»), the ERA5 island rainfall under CC BY 4.0, and the optional E-OBS rainfall is licensed
for non-commercial research and education only.
