# Getting started with Triton

This guide takes you from a clean machine to a complete sizing study. It assumes no
previous contact with the software. The model behind the numbers is described separately,
in [`model.md`](model.md).

---

## 1. Install

Triton needs **Python 3.10 or later**. Check what you have:

```bash
python --version
```

### From source

```bash
git clone https://github.com/igorcmvaz/triton.git
cd triton
pip install -e .
```

This registers two commands on your path: `triton-gui` for the desktop application and
`triton` for the command line.

To work on the code, or to run the test suite, install the development dependencies as
well:

```bash
pip install -r requirements-dev.txt
pytest
```

### From the Windows installer

Releases ship a signed Windows installer that bundles Python and every dependency. It
needs no Python installation. Download it from the repository releases page and run it;
the software is installed under *Program Files* and appears in the start menu.

The Brazil edition ships with the national climate base embedded: the 37,164 CLIMBra CSV
files (about 6.5 GB) compiled into a single database of about 800 MB. There is nothing
else to download. The International edition ships without it and works with your own
precipitation series, tariffs, costs and emission factors; everything that differs between
the two editions is listed in [`editions.md`](editions.md).

---

## 2. First run

```bash
triton-gui
```

On the first launch the software asks for an interface language: Portuguese, English or
Chinese. The choice can be changed at any time; changing it restarts the application.

The window has a sidebar of stages on the left and the working area on the right. The
stages are sequential by data dependency, not by rigidity: changing the building
invalidates the simulation that used it, and the software says so rather than silently
keeping a stale result.

| Stage | What you declare |
| :--- | :--- |
| 1 · Project | location, precipitation series, first-flush discard depth |
| 2 · Building | catchment area, occupants, non-potable demand |
| 3 · Simulation | the range of tank capacities to sweep |
| 4 · Quality | use class and treatment train |
| 5 · Economic | costs, tariffs, financial premises |
| 6 · Environmental | emission factors and the assessment horizon |
| 7 · Report | the final document and the exports |

---

## 3. The five inputs without which nothing can be simulated

Everything else has a documented default. These five do not:

1. **A daily precipitation series** — two columns, date and depth in millimetres, as CSV.
   Or a municipality from the embedded climate base.
2. **Catchment area**, in square metres, *in horizontal projection* — not the sloped area
   of the roof. Rain falls vertically; using the sloped area overestimates the yield.
3. **Runoff coefficient** — the fraction of rainfall that reaches the tank. The default is
   0.75 for the ceramic tile that dominates Brazilian residential roofs.
4. **Non-potable demand** — occupants and per-capita consumption, or a measured series.
5. **The range of tank capacities** to test.

The first-flush discard depth defaults to **2.0 mm**, the value of ABNT NBR 15527:2019
item 4.1.5, when it is not declared. Declare the depth measured on the actual roof
whenever you have it.

---

## 4. A worked example from the command line

The command line does everything the interface does, and it is what you want for a study
that must be reproducible.

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

This adds the economic analysis, the screening life-cycle assessment and the
multi-criteria ranking. `--format` accepts `text`, `json`, `csv`, `html` and `xlsx`; pass
`--seed` whenever the run involves sampling, so that the result is reproducible.

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
project files, or drive a sweep from a spreadsheet. These are what produce a national
study: the same building across 652 municipalities, with one command.

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

Open an issue at [github.com/igorcmvaz/triton](https://github.com/igorcmvaz/triton) and
attach the `.triton` project file and the precipitation series. The project file carries
every premise, so the two together are enough for anyone to reproduce what you saw.

Contact: sustainability@contato.ufsc.br
