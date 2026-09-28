# Netuno 5 — sizing and simulation of building rainwater harvesting systems

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Space%20Management-005a36)](https://sustainability.ufsc.br/)

*Português: [README.md](README.md) — this is the English summary of that document.*

**Netuno 5** sizes rainwater harvesting systems for buildings. It runs a daily water
balance over a precipitation series, sweeps a grid of tank capacities, and reports what
each capacity delivers technically, financially and in terms of life-cycle carbon — then
ranks the candidates by multi-criteria decision analysis.

It is developed by the **Sustainable Environments Research Group** (*Grupo de
Pesquisa em Ambientes Sustentáveis*) at the Federal University of Santa Catarina,
Brazil, and succeeds Netuno 4, in use since 2014.

The application interface is available in Portuguese, English and Chinese; the user
manual is written in Portuguese. This file, together with the documents under
[`docs/en/`](docs/en/), is the English entry point for readers, reviewers and reusers of
the code.

---

## What the software does

| Stage | What it computes |
| :--- | :--- |
| **Rainfall** | reads a daily precipitation series; computes nine rainfall indices; optionally draws on an embedded national climate base of 652 Brazilian municipalities under CMIP6 scenarios |
| **Building** | catchment area, runoff coefficient, first-flush discard depth, non-potable demand (constant, weekly, monthly or a full daily series) |
| **Daily balance** | *yield-after-spillage* (YAS) balance, day by day, over the whole series, for every candidate tank capacity |
| **Indicators** | potable water savings, volumetric and temporal reliability, days of full, partial and no supply, overflow |
| **Water quality** | four use classes, a screening treatment train, and the operating cost and energy of disinfection |
| **Economics** | parametric CAPEX, progressive water and sewerage tariffs for 652 municipalities, ANEEL electricity tariffs, OPEX, NPV, IRR, simple and discounted payback |
| **Carbon** | screening life-cycle assessment: embodied carbon in materials, operational carbon of pumping and treatment, and the credit of mains water avoided |
| **Decision** | TOPSIS and SMAA-VIKOR over the candidate capacities, plus placement against LEED, AQUA-HQE, Selo Casa Azul and GRI 303 |

The three optima — technical, economic and environmental — do not in general coincide.
Netuno 5 computes all three on one sweep so that the divergence is visible rather than
hidden by whichever criterion the analyst happened to choose.

### What it deliberately does not do

- It is **not** an urban drainage model. It does not route catchment runoff and does not
  represent the network effect of many systems. That is catchment scale, and other models
  address it.
- It is **not** a hydraulic design tool. It does not size pipework by head loss and does
  not produce construction drawings. It delivers design premises, not executive drawings.
- The carbon assessment is a **screening** assessment, not an inventory compliant with
  ISO 14040/14044.

Stating the boundary early saves the reader from asking the software for something it
does not claim.

---

## Installation

Netuno 5 requires **Python 3.10 or later**. It runs on Windows, Linux and macOS; the
packaged installer is Windows only.

```bash
git clone https://github.com/igorcmvaz/netuno.git
cd netuno
pip install -e .
```

For development, including the test suite:

```bash
pip install -r requirements-dev.txt
```

Runtime dependencies: PySide6, NumPy, pandas, Matplotlib, openpyxl, ReportLab, pydantic,
ezdxf, requests, BeautifulSoup, PyArrow. All are installed by the commands above.

Full instructions, including a worked example and the Windows installer, are in
[`docs/en/getting-started.md`](docs/en/getting-started.md).

---

## Running

**Desktop application**

```bash
netuno-gui
```

**Command line**

```bash
netuno --help
```

The command line exposes the same engine as the desktop application and adds the
reproducible workflows: factorial matrices over building premises and climates, batch
execution from a spreadsheet, Monte Carlo uncertainty propagation, the representative
series-length analysis, and stochastic daily demand.

```bash
netuno init projeto.netuno            # create an editable project template
netuno run projeto.netuno             # simulate; technical sizing
netuno analyze projeto.netuno         # full chain: technical, economic, LCA, TOPSIS
netuno series-length projeto.netuno   # how many years of rainfall this project needs
netuno uncertainty projeto.netuno     # Monte Carlo over the sizing decision
```

---

## Documentation

| Document | Language | Content |
| :--- | :--- | :--- |
| [`docs/en/getting-started.md`](docs/en/getting-started.md) | English | installation, first run, project file format, worked example |
| [`docs/en/model.md`](docs/en/model.md) | English | the computational model: equations, conventions, assumptions and their limits |
| [`docs/en/verification.md`](docs/en/verification.md) | English | how the software is verified, and against what |
| [`docs/metodologia.md`](docs/metodologia.md) | Portuguese | the same model, in full, with the national data sources |
| [`docs/verificacao_e_validacao.md`](docs/verificacao_e_validacao.md) | Portuguese | the complete verification and validation report |
| `manual/Manual-Netuno-5.pdf` | Portuguese | the user manual, with the worked case studies and the parameter appendices; also issued as seven standalone parts under `manual/mini/` |

---

## Architecture

The engine is separate from the interface: `netuno.core` has no dependency on Qt, and
both the desktop application and the command line call it through the same entry points.
Every result the interface displays can be reproduced from the command line on the same
project file.

| Module | Responsibility |
| :--- | :--- |
| [`netuno.core.simulation`](netuno/core/simulation.py) | daily YAS balance, first-flush discard, capacity sweep |
| [`netuno.core.calculator`](netuno/core/calculator.py) | rainfall indices and series characterisation |
| [`netuno.core.economic`](netuno/core/economic.py) | progressive tariffs, cash flow, NPV, IRR, payback |
| [`netuno.core.cost_estimates`](netuno/core/cost_estimates.py) | parametric costing, SINAPI compositions, regional factors |
| [`netuno.core.tariffs_database`](netuno/core/tariffs_database.py) | audited water, sewerage and electricity tariffs for 652 municipalities |
| [`netuno.core.environmental`](netuno/core/environmental.py) | emission factors and the carbon balance |
| [`netuno.core.water_quality`](netuno/core/water_quality.py) | use classes, treatment train, disinfection |
| [`netuno.core.topsis`](netuno/core/topsis.py) | TOPSIS ranking of the candidate capacities |
| [`netuno.core.mcdm_methods`](netuno/core/mcdm_methods.py) | VIKOR and stochastic multi-criteria acceptability analysis (SMAA-VIKOR) |
| [`netuno.cli`](netuno/cli.py) | command line and the reproducible batch workflows |

---

## Tests

```bash
pytest
```

The suite collects **1,200 tests** in five layers:

| Layer | Tests | Files | What it holds |
| :--- | ---: | ---: | :--- |
| unit | 944 | 86 | each function against its expected value |
| invariants | 197 | 11 | mass conservation, bounds, monotonicity |
| integration | 49 | 8 | whole analyses end to end |
| interface | 8 | 4 | the desktop application builds and responds |
| benchmarking | 7 | 1 | replication of Netuno 4 against 4,050 published reference cases |

The benchmarking layer is slow and is deselected by default through the `replicacao`
marker; run it with `pytest -m replicacao`.

---

## Citing

If you use Netuno 5 in academic work, please cite it as declared in
[`CITATION.cff`](CITATION.cff):

> Vaz, I. C. M., & Ghisi, E. (2026). *Netuno 5* (version 5.0.1) [Computer software].
> Universidade Federal de Santa Catarina. https://github.com/igorcmvaz/netuno

---

## Contributing and support

Issues and pull requests are welcome at
[github.com/igorcmvaz/netuno](https://github.com/igorcmvaz/netuno). For a bug report,
attach the `.netuno` project file and the precipitation series that reproduce it — the
project file carries every premise, so the two together are enough to reproduce any
result.

Contact: sustainability@contato.ufsc.br

---

## Licence

GNU General Public License v3.0 or later. See [`LICENSE`](LICENSE) for the full text.

The embedded climate base (CLIMBra) is public-domain data published by Ballarin, Sone,
Gesualdo, Schwamback, Reis, Almagro and Wendland (2023), *Scientific Data* 10(1), article
47, and is redistributed under its own terms.
