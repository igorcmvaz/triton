# Triton, Iberian Edition (IBE): sizing and simulation of building rainwater harvesting systems

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/Licence-academic%20source--available-lightgrey.svg)](../../LICENSE.md)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Environments%20Research%20Group-005a36)](https://sustainability.ufsc.br/)

**Triton** sizes rainwater harvesting systems for buildings. It runs a daily water balance
over a precipitation series, sweeps a grid of tank capacities and reports what each capacity
delivers in potable water saved, money and life-cycle carbon. It then ranks the candidates by
multi-criteria decision analysis (TOPSIS and SMAA-VIKOR).

It is developed by the Sustainable Environments Research Group (*Grupo de Pesquisa em Ambientes
Sustentáveis*, GPAS) at the Federal University of Santa Catarina (UFSC), and succeeds the Netuno programme (Netuno 4 is the reference of its validation).

This is the **Iberian Edition (IBE, Triton IBE)**. It opens in European Portuguese and works in euros.
For now it carries data for Portugal only (Spain: no sites). It brings E-OBS daily rainfall for 278 of the
308 Portuguese municipalities (1950 to 2025, with a quality level A, B or C for each), and the water and
sewer tariffs of Lisbon, Porto and Funchal with the managing entity, validity period and source of each
value. It carries no price database and no emission factors: costs and the grid emission factor start at
zero and are yours to enter. The user manual is written in European Portuguese, and so is the interface
on opening; the other interface languages are English, Spanish and Chinese (the last two only partly
translated). This English documentation is a summary for reviewers and reusers.

The other editions use the same engine and the same version number; see
[`editions.md`](editions.md) for what differs. Version 0.1.0 is a beta.

---

## What the software does

| Stage | What it computes |
| :--- | :--- |
| **Rainfall** | reads a daily precipitation series (CSV), or takes the E-OBS series of a Portuguese municipality from the embedded base `data/portugal_eobs.db`; computes rainfall indices |
| **Building** | catchment area, runoff coefficient, first-flush discard depth, non-potable demand (constant, weekly, monthly or a full daily series) |
| **Daily balance** | yield-after-spillage balance, day by day, for every candidate tank capacity; one or two tanks |
| **Indicators** | potable water savings, volumetric and temporal reliability, days of full, partial and no supply, overflow |
| **Water quality** | use classes, a screening treatment train, and the operating cost and energy of disinfection |
| **Economics** | parametric CAPEX, progressive water and sewer tariffs, electricity tariffs, OPEX, NPV, IRR, simple and discounted payback |
| **Carbon** | screening life-cycle assessment: embodied carbon, operational carbon of pumping and treatment, and the credit of mains water avoided (needs emission factors that you enter) |
| **Decision** | TOPSIS and SMAA-VIKOR over the candidate capacities, and placement against LEED v4/v4.1, LEED v5, EDGE and GRI 303 |
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
- The E-OBS base covers the 278 mainland municipalities. The 30 island municipalities have no series:
  the 19 in the Azores lie outside the E-OBS domain, and the 11 in Madeira have more than 1% of missing
  days in 1991-2020. For them, use your own series. The Funchal example uses an ERA5 reanalysis series,
  labelled as such, and its electricity tariff comes from a secondary source (a price comparison site)
  and is flagged yellow in `docs/DADOS.md`.

---

## Installation

There is no installer yet: the Windows installer is not published and is not signed. The release
page will give its address and SHA-256 checksum when it exists (the DOI will be assigned when
the release is published). Until then, run Triton from the source code.

Triton needs **Python 3.12 or later** and runs from source on Windows, Linux and macOS.

The repository is private at this stage: ask the maintainers for access.

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

If you use Triton in academic work, cite it as declared in [`CITATION.cff`](../../CITATION.cff).
The DOI will be assigned when the release is published.

## Contributing and support

The repository is private at this stage; send reports to the maintainers (sustainability@contato.ufsc.br). For a bug
report, attach the `.triton` project file and the precipitation series that reproduce it: the project
file carries every premise.

## Licence

Academic source-available, all rights reserved, free for non-commercial use; see
[`LICENSE.md`](../../LICENSE.md). Third-party data keep their own licences (see
[`DADOS.md`](../DADOS.md) and `infos_licenses/AVISOS_DE_TERCEIROS.txt`). In particular, the E-OBS rainfall
is licensed for non-commercial research and education only.
