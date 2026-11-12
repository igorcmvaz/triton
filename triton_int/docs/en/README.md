# Triton, International Edition: sizing and simulation of building rainwater harvesting systems

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/Licence-academic%20source--available-lightgrey.svg)](../../LICENSE.md)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Environments%20Research%20Group-005a36)](https://sustainability.ufsc.br/)

**Triton** sizes rainwater harvesting systems for buildings. It runs a daily water balance
over a precipitation series, sweeps a grid of tank capacities and reports what each capacity
delivers in potable water saved, money, life-cycle carbon and system weight. It then ranks the
candidates by multi-criteria decision analysis (TOPSIS and SMAA-VIKOR) over eight criteria in four
dimensions: technical, economic, environmental and structural.

It is developed by the Sustainable Environments Research Group (*Grupo de Pesquisa em Ambientes
Sustentáveis*) at the Federal University of Santa Catarina (UFSC), and succeeds the Netuno programme (Netuno 4 is the reference of its validation).

This is the **International Edition (INT)**: the region-neutral core. It carries no regional
rainfall database, tariff catalogue, cost database or emission factors. You supply the rainfall
series, the water, sewer and energy tariffs, the costs, the emission factors and the currency.
The interface opens in English and is also available in Portuguese, Spanish and Chinese (the last two
only partly translated). The user manual is in English, and the program opens it.

The other editions use the same engine and the same version number; see
[`editions.md`](editions.md) for what differs. Version 0.2.0 is a beta; what changed from 0.1.0 is in
[`../NOTAS_DE_LANCAMENTO_0.2.0.md`](../NOTAS_DE_LANCAMENTO_0.2.0.md).

---

## What the software does

| Stage | What it computes |
| :--- | :--- |
| **Rainfall** | reads a daily precipitation series (CSV); computes rainfall indices; three example series (New York, London, Cape Town) ship in `data/rainfall/` |
| **Building** | catchment area, runoff coefficient, first-flush discard depth, non-potable demand (constant, weekly, monthly or a full daily series) |
| **Daily balance** | yield-after-spillage balance, day by day, for every candidate tank capacity; one or two tanks |
| **Indicators** | potable water savings, volumetric and temporal reliability, days of full, partial and no supply, overflow |
| **Water quality** | use classes, a screening treatment train, and the operating cost and energy of disinfection |
| **Economics** | parametric CAPEX, progressive water and sewer tariffs, electricity tariffs, OPEX, NPV, IRR, simple and discounted payback |
| **Carbon** | screening life-cycle assessment: embodied carbon, operational carbon of pumping and treatment, and the credit of mains water avoided (needs emission factors that you enter) |
| **Weight of the system** | dry mass, water load and operating load (kg and kN) at the lower level, on the roof and in the risers, with attention thresholds of the program, not of any standard |
| **Decision** | TOPSIS, VIKOR, PROMETHEE II and SMAA-VIKOR over the candidate capacities, with eight criteria in four dimensions and declared weights; placement against LEED v4/v4.1, LEED v5, EDGE and GRI 303 |
| **Piping in 3D** | pipe runs from component connection points, with gravity slopes and clash checks; DXF, glTF, interactive HTML and a BIM manifest |

The technical, economic and environmental optima do not in general coincide. Triton computes
all three on one sweep so that the divergence is visible.

### What it deliberately does not do

- It is **not** an urban drainage model: it does not route catchment runoff.
- It is **not** a hydraulic design tool: it does not size pipework by head loss and produces no
  construction drawings.
- The carbon assessment is a **screening** assessment, not an inventory compliant with
  ISO 14040/14044.
- It supplies **no prices, tariffs or emission factors**. A new project starts with every cost at zero,
  an empty water tariff and no grid emission factor, and payback and NPV say little until you enter
  your own values. The tariffs in the three examples are illustrative.

---

## Installation

The Windows installer is published in the Zenodo record and is not code-signed. The installer of
version 0.1.0 is in the record of DOI 10.5281/zenodo.23402916, with its SHA-256 in `SHA256SUMS.txt`;
version 0.2.0 has no DOI of its own yet, and the DOI of all versions, 10.5281/zenodo.23402915,
always resolves to the most recent one. You can also run Triton from the source code.

Triton needs **Python 3.12 or later** and runs from source on Windows, Linux and macOS.

The repository is public at https://github.com/igorcmvaz/triton.

```bash
git clone https://github.com/igorcmvaz/triton.git
cd triton/triton_int
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
| [`../DADOS.md`](../DADOS.md) | English | data that ships with the edition: sources, licences, quality |
| `../../manual/en/Triton-User-Manual.pdf` | English | the user manual |
| [`../metodologia.md`](../metodologia.md) | Portuguese | the same model, in full |

---

## Citing

If you use Triton in academic work, cite it as declared in [`CITATION.cff`](../../CITATION.cff),
with the version you used. The DOI of all versions is 10.5281/zenodo.23402915; version 0.1.0 has its
own, 10.5281/zenodo.23402916.

## Contributing and support

Send reports to the maintainers (igorcmvaz@gmail.com). For a bug
report, attach the `.triton` project file and the precipitation series that reproduce it: the project
file carries every premise.

## Licence

Academic source-available, all rights reserved, free for non-commercial use; see
[`LICENSE.md`](../../LICENSE.md). Third-party data keep their own licences (see
[`DADOS.md`](../DADOS.md) and `infos_licenses/AVISOS_DE_TERCEIROS.txt`).
