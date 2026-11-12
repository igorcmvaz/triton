# Triton — sizing and simulation of building rainwater harvesting systems

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/Licence-academic%20source--available-lightgrey.svg)](../../LICENSE.md)
[![Research group](https://img.shields.io/badge/UFSC-Sustainable%20Space%20Management-005a36)](https://sustainability.ufsc.br/)

*Português: [README.md](../../README.md) — this is the English summary of that document.*

**Triton** sizes rainwater harvesting systems for buildings. It runs a daily water
balance over a precipitation series, sweeps a grid of tank capacities, and reports what
each capacity delivers technically, financially and in terms of life-cycle carbon — then
ranks the candidates by multi-criteria decision analysis.

It is developed by the **Sustainable Environments Research Group** (*Grupo de
Pesquisa em Ambientes Sustentáveis*) at the Federal University of Santa Catarina,
Brazil, and succeeds Netuno 4, in use since 2014.

The application interface is available in Portuguese, English, Spanish and Chinese; the user
manual is written in Portuguese and translated into English in full, section by section. This file, together with the documents under
[`docs/en/`](../../docs/en/), is the English entry point for readers, reviewers and reusers of
the code.

---

## Three editions: Brazil (BRL), International (INT) and Ibérica (IBE)

The program ships in three editions, built from the same code and with the same calculation
engine. The **Brazil Edition** carries the audited Brazilian data: the CLIMBra climate
database (652 cities, CMIP6), water and sewage tariffs of 652 municipalities with
provenance by document, ANEEL electricity tariffs, costs in reais, MCTI emission factors
and the national certifications and incentives (AQUA-HQE, Selo Casa Azul, IPTU Verde).
The **International Edition** is the neutral core: it opens in English, with the currency
chosen by the user and the tariff, costs and emission factors entered by them, and only
the international certifications (LEED, EDGE, GRI). The **Iberian Edition** opens in European
Portuguese, works in euros and carries rainfall by municipality for Portugal and Spain (Iberia01 and
ERA5) and Portuguese and Spanish tariffs. The full map — what the user sees,
where it is in the code, what goes into each package — is in
[`docs/en/editions.md`](../../docs/en/editions.md).

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
| **System weight** | dry mass, water load and operating load (kg and kN) on the lower level, the roof and the pipework, with the software's own load-attention alerts (not limits from any standard) |
| **Decision** | TOPSIS and SMAA-VIKOR over the candidate capacities on eight criteria in four axes — technical (volumetric reliability, storage efficiency), economic (net financial savings, levelised cost of water, discounted payback), environmental (life-cycle CO₂e) and structural (dry mass, annual overflow) — with four axis weights (25% each by default) split by the criterion shares, plus placement against LEED v4/v4.1 and LEED v5, EDGE, AQUA-HQE, Selo Casa Azul and GRI 303 |
| **Piping in 3D** | pipe runs organised by the designer from component connection points, with destination checks, gravity slopes and clash detection; 3D plant in DXF, a schematic with real measurements, an orbitable WebGL volumetric model (three.js, PBR materials, Poly Haven HDRI, shadows, animated flow, section by elevation, measuring), glTF and interactive HTML export, and a BIM manifest for Revit |

The three optima — technical, economic and environmental — do not in general coincide.
Triton computes all three on one sweep so that the divergence is visible rather than
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

The Windows installer needs no Python. Running from source requires **Python 3.12 or later**. It runs on Windows, Linux and macOS; the
packaged installer is Windows only.

```bash
git clone https://github.com/igorcmvaz/triton.git
cd triton
pip install -e .
```

For development, including the test suite:

```bash
pip install -r requirements-dev.txt
```

Runtime dependencies: PySide6, NumPy, pandas, Matplotlib, openpyxl, ReportLab, pydantic,
ezdxf, PyArrow. All are installed by the commands above.

Full instructions, including a worked example and the Windows installer, are in
[`docs/en/getting-started.md`](../../docs/en/getting-started.md).

---

## Running

**Desktop application**

```bash
triton-gui
```

**Command line**

```bash
triton --help
```

The command line exposes the same engine as the desktop application and adds the
reproducible workflows: factorial matrices over building premises and climates, batch
execution from a spreadsheet, Monte Carlo uncertainty propagation, the representative
series-length analysis, and stochastic daily demand.

```bash
triton init projeto.triton            # create an editable project template
triton run projeto.triton             # simulate; technical sizing
triton analyze projeto.triton         # full chain: technical, economic, LCA, system weight, TOPSIS
triton series-length projeto.triton   # how many years of rainfall this project needs
triton uncertainty projeto.triton     # Monte Carlo over the sizing decision
```

---

## Documentation

| Document | Language | Content |
| :--- | :--- | :--- |
| [`docs/en/getting-started.md`](../../docs/en/getting-started.md) | English | installation, first run, project file format, worked example |
| [`docs/en/editions.md`](../../docs/en/editions.md) | English | the Brazil and International editions: what differs, where in the code, what each package carries |
| [`docs/en/model.md`](../../docs/en/model.md) | English | the computational model: equations, conventions, assumptions and their limits |
| [`docs/en/verification.md`](../../docs/en/verification.md) | English | how the software is verified, and against what |
| [`docs/metodologia.md`](../../docs/metodologia.md) | Portuguese | the same model, in full, with the national data sources |
| [`docs/verificacao_e_validacao.md`](../../docs/verificacao_e_validacao.md) | Portuguese | the complete verification and validation report |
| `manual/Manual-Triton.pdf` | Portuguese | the user manual, with the worked case studies and the parameter appendices; also issued as seven standalone parts under `manual/mini/` |
| `manual/en/Triton-User-Manual.pdf` | English | the same user manual, translated; it is the one the International Edition installs and opens |

---

## Architecture

The engine is separate from the interface: `triton.core` has no dependency on Qt, and
both the desktop application and the command line call it through the same entry points.
Every result the interface displays can be reproduced from the command line on the same
project file.

| Module | Responsibility |
| :--- | :--- |
| [`triton.core.simulation`](../../triton/core/simulation.py) | daily YAS balance, first-flush discard, capacity sweep |
| [`triton.core.calculator`](../../triton/core/calculator.py) | rainfall indices and series characterisation |
| [`triton.core.economic`](../../triton/core/economic.py) | progressive tariffs, cash flow, NPV, IRR, payback |
| [`triton.core.cost_estimates`](../../triton/core/cost_estimates.py) | parametric costing, SINAPI compositions, regional factors |
| [`triton.core.tariffs_database`](../../triton/core/tariffs_database.py) | audited water, sewerage and electricity tariffs for 652 municipalities |
| [`triton.core.environmental`](../../triton/core/environmental.py) | emission factors and the carbon balance |
| [`triton.core.water_quality`](../../triton/core/water_quality.py) | use classes, treatment train, disinfection |
| [`triton.core.topsis`](../../triton/core/topsis.py) | TOPSIS ranking of the candidate capacities |
| [`triton.core.mcdm_methods`](../../triton/core/mcdm_methods.py) | VIKOR and stochastic multi-criteria acceptability analysis (SMAA-VIKOR) |
| [`triton.cli`](../../triton/cli.py) | command line and the reproducible batch workflows |

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

If you use Triton in academic work, please cite it as declared in
[`CITATION.cff`](../../CITATION.cff):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton* (version 0.2.0) [Computer software].
> Universidade Federal de Santa Catarina. https://doi.org/10.5281/zenodo.23402915

The DOI 10.5281/zenodo.23402915 covers every version and always resolves to the latest;
state the version you used. A study made with 0.1.0 cites 0.1.0, DOI
10.5281/zenodo.23402916, and is reproduced with it: version 0.2.0 replaced the
seven-criterion multi-criteria model with the eight-criterion one, and the capacity it
selects changes.

---

## Contributing and support

Issues and pull requests are welcome at
[github.com/igorcmvaz/triton](https://github.com/igorcmvaz/triton). For a bug report,
attach the `.triton` project file and the precipitation series that reproduce it — the
project file carries every premise, so the two together are enough to reproduce any
result.

Contact: igorcmvaz@gmail.com

---

## Licence

Academic source-available, all rights reserved, free for non-commercial use. See [`LICENSE.md`](../../LICENSE.md) for the full terms, including the mandatory citation.

The embedded climate base (CLIMBra) is public-domain data published by Ballarin, Sone,
Gesualdo, Schwamback, Reis, Almagro and Wendland (2023), *Scientific Data* 10(1), article
47, and is redistributed under its own terms.
