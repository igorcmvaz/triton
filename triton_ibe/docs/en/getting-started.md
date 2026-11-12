# Getting started with Triton

This guide takes you from a clean machine to a complete sizing study. It assumes no
previous contact with the software. The model behind the numbers is described separately,
in [`model.md`](model.md).

---

## 1. Install

Triton needs **Python 3.12 or later**. Check what you have:

```bash
python --version
```

### From source

The repository is public at https://github.com/igorcmvaz/triton; questions go to igorcmvaz@gmail.com.

```bash
git clone https://github.com/igorcmvaz/triton.git
cd triton/triton_ibe
pip install -r requirements.txt
python main.py                      # graphical interface
python -m triton.cli --help         # command line
```

To work on the code, or to run the test suite, install the development dependencies as
well and run the suite of the edition:

```bash
pip install -r requirements-dev.txt
TRITON_EDITION=IBE python -m pytest tests/unit tests/test_essencial.py
```

(On Windows PowerShell: `$env:TRITON_EDITION = "IBE"; python -m pytest tests/unit tests/test_essencial.py`.)

### Windows installer

The Zenodo records are gathered under the all-versions DOI
[10.5281/zenodo.23402915](https://doi.org/10.5281/zenodo.23402915), which always resolves to the latest
version. The installer of version 0.1.0 (`Triton_Iberica_Setup_v0.1.0.exe`) is in the 0.1.0 record, DOI
[10.5281/zenodo.23402916](https://doi.org/10.5281/zenodo.23402916), with its SHA-256 checksum in
`SHA256SUMS.txt`; version 0.2.0 has no record of its own yet. The installer is **not code-signed**, so
Windows may warn that the publisher is unknown.

The Iberian Edition ships daily rainfall by municipality for Portugal and Spain (Iberia01, ODbL, in four
parts of `data/chuva_iberia01_p*.db`; ERA5 for the islands, level C), the optional E-OBS base for mainland
Portugal (`data/portugal_eobs.db`, about 6 MB), the tariffs of Lisbon, Porto and Funchal, seven Spanish
municipal tariffs not yet double-checked and the INE regional average for the rest of Spain. Costs, other
tariffs and emission factors are yours to enter. Everything that differs between the editions is
listed in [`editions.md`](editions.md); the data, their licences and their quality are in
[`../DADOS.md`](../DADOS.md) (in European Portuguese).

---

## 2. First run

```bash
python main.py
```

The interface opens in European Portuguese. The language (Portuguese, English, Spanish or Chinese) can
be changed at any time; changing it restarts the application.

The window has a sidebar of steps on the left and the working area on the right: you start at
**1. Project & Rainfall**, then **2. Building & Demand**, **3. Quality & Treatment** and
**4. Tank & Costs**, and go on to the economic, environmental and export steps. The steps
follow the order of the data dependencies: changing the building invalidates the simulation that
used it, and the software says so rather than silently keeping a stale result. The user manual
(`manual/Manual-Triton.pdf`, in European Portuguese, opened from the Documentation tab) describes every step, and
**File > Open** loads the worked examples in `examples/portugal/` (`lisboa.triton`, `porto.triton`,
`funchal.triton`) and `examples/espanha/` (`madrid.triton`, `palma.triton`); all use the Iberia01 rainfall (ODbL), except Funchal (ERA5, level C).

---

## 3. The five inputs without which nothing can be simulated

Everything else has a documented default. These five do not:

1. **A daily precipitation series** — two columns, date and depth in millimetres, as CSV, or a Portuguese or Spanish municipality from the embedded rainfall bases (Iberia01, ERA5 for the islands, optional E-OBS).
   
2. **Catchment area**, in square metres, *in horizontal projection* — not the sloped area
   of the roof. Rain falls vertically; using the sloped area overestimates the yield.
3. **Runoff coefficient** — the fraction of rainfall that reaches the tank. The default is
   0.75 for standard ceramic tile.
4. **Non-potable demand** — occupants and per-capita consumption, or a measured series.
5. **The range of tank capacities** to test.

The first-flush discard depth defaults to **2.0 mm**, the standard reference value,
when it is not declared. Declare the depth measured on the actual roof
whenever you have it.

---

## 4. A worked example from the command line

The command line does everything the interface does, and it is what you want for a study
that must be reproducible.

The commands below use the `triton` command, which `pip install -e .` registers; without that
install, write `python -m triton.cli` instead.

**Create a project template.**

```bash
triton init study.triton
```

The template is a readable, editable file carrying every premise of the study: the
rainfall source, the building, the capacities to sweep, the costs, the tariffs and the
emission factors. It is the unit of reproducibility — the file plus the precipitation
series reproduce any result the software has ever produced for that study.

**Check it before spending time on it.**

```bash
triton validate study.triton
```

This reports missing data, premises outside a plausible range and internal
inconsistencies, without running a simulation.

**Simulate.**

```bash
triton run study.triton
```

The technical result: for every candidate capacity, the potable water savings, the
volumetric and temporal reliability, the days of full, partial and no supply, and the
overflow.

**Run the whole chain.**

```bash
triton analyze study.triton --analysis all --format xlsx --output results.xlsx
```

This adds the economic analysis, the screening life-cycle assessment, the system weight and the
multi-criteria ranking. `--format` accepts `text`, `json`, `csv`, `html` and `xlsx`; pass
`--seed` whenever the run involves sampling, so that the result is reproducible.

**Declare the weights.** The ranking uses eight criteria on four axes: technical (volumetric
reliability, storage efficiency), economic (net financial savings, levelised cost of water, discounted
payback), environmental (life-cycle CO₂e) and structural (dry material mass, annual overflow).
`--weights t,e,a,s` gives the four axis weights (25% each by default) or eight criterion weights;
`--criterion-shares` gives eight shares that split each axis weight among its criteria (equal by default,
`1,1,1,1,1,1,1,1`). Three axis weights, from projects and studies made up to version 0.1.0, are still
accepted, with the structural axis taking their mean; seven values, from the old seven-criterion model, are
refused. In the project file the same settings are `analysis.topsis_weights` and
`analysis.topsis_criterion_shares`.

**System weight.** `--analysis all` (or `--analysis system_weight`) also reports the dry mass, the water
load and the operating load of the system, in kg and kN, in the basement or lower level, on the roof or upper
level and in the risers and network. The HTML report, the XLSX workbook (sheet `system_weight` with the summary
of the selected capacity; the per-capacity values are in sheet `alternatives`) and the terminal text show it.
The alerts use the programme's own attention thresholds — 500 kg on the roof with the tank full, an upper tank
above 1,500 L, a lower tank above 3,000 kg dry, any concrete lower tank — and not those of any standard: they
ask you to confirm the load with the structural or foundation design.

---

## 5. The workflows that only the command line has

```bash
triton series-length study.triton
```

**How many years of rainfall does this project need?** The software cuts sub-series of
every possible length, simulates each one, and asks in how many of them the same capacity
and the same savings recur. The answer belongs to the *project*, not to the city: it moves
with catchment area, demand and the attainable fraction. Thirty years is the length most
used in the literature, by convention rather than by demonstrated requirement.

```bash
triton uncertainty study.triton --samples 5000 --seed 42
```

**Monte Carlo over the sizing decision.** Each premise is drawn from its declared range
and the sweep repeated, so that the recommendation comes back as a distribution rather
than a point.

```bash
triton init-catalog premises premises.json
triton matrix premises.json climates.json --analysis all --output-dir matrix/
triton matrix-projects --projects projects/ --recursive --analysis all
triton batch scenarios.xlsx --analysis all --format csv --output batch.csv
```

**Factorial studies.** Combine building premises with a climate catalogue, run a folder of
project files, or drive a sweep from a spreadsheet. These are what produce a multi-city
study: the same building across many climates, with one command.

```bash
triton stochastic-demand study.triton
```

**Stochastic daily demand.** Draws the daily consumption instead of holding it constant,
and returns the performance as a range.

Run `triton <command> --help` for the full options of any of them.

---

## 6. Reading the result

Three numbers deserve attention, and one warning.

**Potable water savings** is the share of *total* consumption that the system replaced
over the whole series. The denominator is total demand, not non-potable demand — so it is
bounded above by the attainable fraction, and a system that meets every non-potable use
perfectly still shows savings well below 100%.

**Reliability** comes in two forms, and they answer different questions. Volumetric
reliability is the fraction of the demanded volume that was met: *how much* water the
system delivered. Temporal reliability is the fraction of days fully met: *how often* it
did not fail.

**The marginal gain per cubic metre** is what shows the saturation. The first 500 L of
tank in the reference case returns 5.69 percentage points of savings; the step from 19.5
to 20 m³ returns 0.15. Thirty-eight times less.

**The warning.** The capacity the software labels the *ideal volume* is the first point on
the sweep whose marginal gain falls below a configured threshold. It is a stopping rule,
not the maximum or minimum of any objective function — two analysts using different
thresholds get different 'ideal volumes', and both are defensible. The economic optimum
(shortest discounted payback, with NPV as the tie-breaker) and the environmental optimum
(minimum carbon balance) *are* optima of a
function, and they generally fall elsewhere. Report which criterion governed the
recommendation; the criterion is part of the result.

---

## 7. When something goes wrong

| Symptom | Cause and fix |
| :--- | :--- |
| the sweep step is not the one you typed | the engine rounds the step up to a multiple of 250 L and caps the grid at 40 positive capacities; the effective step is reported and stored |
| savings look implausibly low | check that the precipitation series has no gaps read as zeros — a day without a record is not a day without rain, and the software discards incomplete years rather than filling them |
| savings look implausibly high | check the catchment area: it must be the horizontal projection, and the sloped area overestimates it |
| results differ from Netuno 4 | expected, and quantified: see [`verification.md`](verification.md). The first-flush discard rule changed deliberately |
| the interface opens in the wrong language | the setting is per user and persists; change it in the sidebar |

---

## 8. Reporting a problem

Send the report to the maintainers (igorcmvaz@gmail.com) and
attach the `.triton` project file and the precipitation series. The project file carries
every premise, so the two together are enough for anyone to reproduce what you saw.

Contact: igorcmvaz@gmail.com
