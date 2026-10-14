# How Triton is verified

Verification asks whether the software solves its equations correctly. Validation asks
whether those equations describe the world. This document is mostly about the first, and
it says plainly where the second has not been done.

The full report, with the measurement dates, the defect histories and the tariff audit, is
[`../verificacao_e_validacao.md`](../verificacao_e_validacao.md), in Portuguese.

---

## 1. Five layers

```bash
pytest
```

collects **1,200 tests**:

| Layer | Tests | Files | What it establishes |
| :--- | ---: | ---: | :--- |
| unit | 944 | 86 | each function returns its expected value |
| invariants | 197 | 11 | statements that must hold over whole families of parameters |
| integration | 49 | 8 | complete analyses run end to end and agree with each other |
| interface | 8 | 4 | the desktop application builds, translates and responds |
| benchmarking | 7 | 1 | replication of Netuno 4 over 4,050 published reference cases |

The benchmarking layer is slow and is deselected by default through the `replicacao`
marker. Run it with `pytest -m replicacao`.

Line coverage of the core package is **85%**, with no module below 50%. The 72% of
`simulation.py` is a measurement artefact rather than a gap: 167 of its lines are JIT
kernels that the coverage tool does not instrument even when they execute. Those kernels
are verified by comparison against the reference kernel instead.

---

## 2. Nine properties of the hydrological engine

A case test checks one number. A **property** checks a statement that must hold for every
parameterisation, so a violation indicates a structural error in the balance rather than
numerical divergence in an isolated scenario. The nine properties live in
[`tests/test_essencial.py`](../../tests/test_essencial.py) (section «Motor hidrológico»)
and run on every pass of the suite.

| # | Property | Statement |
| :-- | :--- | :--- |
| P1 | monotonicity in volume | `V₁ ≤ V₂ ⟹ savings(V₁) ≤ savings(V₂)` |
| P2 | physical bounds | `0 ≤ savings ≤ non-potable fraction ≤ 100%` |
| P2b | null volume | `V = 0 ⟹ savings = 0` |
| P3 | saturation | `savings(V)` converges to a finite ceiling |
| P4 | determinism | same input ⟹ bit-identical output |
| P5 | monotonicity in area | `A₁ ≤ A₂ ⟹ savings(A₁) ≤ savings(A₂)` |
| P6 | inverse monotonicity in discard | larger discard ⟹ savings no larger |
| P7 | overflow | larger `V` ⟹ overflow no larger |
| P8 | mass conservation on a grid | closes over 12 combinations of `V × A × discard` |
| P9 | rainless series | zero precipitation ⟹ zero capture, savings and overflow |

All nine pass.

### Why two hydrological regimes

Sensitivity depends on the regime, and a test run in the wrong one can pass without
discriminating anything:

- **Demand-limited** (capture abundant): savings saturate at the non-potable fraction, and
  the response between the smallest and largest tank spans only **0.02 percentage
  points**. The regime is almost insensitive to the parameters.
- **Supply-limited** (capture scarce): savings saturate far below the ceiling, and the
  response spans **3.80 percentage points** — about 190 times more.

Each property is therefore exercised in both. A balance error invisible in the first
regime would be caught in the second.

### Mass conservation

Checked day by day, not only in the annual aggregate:

```text
store(t−1) + captured(t) = store(t) + consumed(t) + overflowed(t)
```

Over 12 combinations of volume, catchment area and discard depth, across 1,825 days each,
the maximum closure error was **0.000 L** — exact equality in floating point, not merely
within tolerance. Pumping to the upper tank is an internal transfer and cancels in the
combined balance.

---

## 3. Netuno 4 as an instrument

Netuno 4 has been in use since 2014 and its results are published. It is therefore usable
as an independent implementation of the same underlying model — not as ground truth, but
as a second opinion.

`data/simulation_outputs/**/Planilha.csv` preserves **4,050 cases** exported from Netuno 4,
byte for byte, across Florianópolis, Brasília, Manaus and São Paulo.

Comparing one program's optimum with the other's mixes three distinct differences: the
water balance, the criterion that selects the optimum, and the treatment of the
first-flush discard. An aggregate metric over that mixture cannot say whether the engine
replicates Netuno 4 — only that the two programs, taken whole, differ. So the divergence
is decomposed, over the 2,583 cases of Manaus and São Paulo:

| Configuration | MAE | Bias | ≤ 5 pp |
| :--- | ---: | ---: | ---: |
| 1. Triton optimum against Netuno 4 optimum | 2.71 pp | −2.71 pp | 88.6% |
| 2. Evaluated at the volume Netuno 4 declared optimal | 1.60 pp | −1.60 pp | 96.4% |
| 3. Idem, adopting Netuno 4's threshold discard rule | **0.25 pp** | **−0.25 pp** | **100.0%** |

which attributes:

| Source of divergence | Share | Nature |
| :--- | ---: | :--- |
| criterion selecting the optimal volume | 1.11 pp (41%) | design difference |
| first-flush discard treatment | 1.36 pp (50%) | deliberate methodological difference |
| residual of the water balance | 0.25 pp (9%) | — |

**With the two known differences neutralised, the Triton engine reproduces Netuno 4
with a mean absolute error of 0.25 pp and 100% of cases within 5 percentage points.** The
residual is compatible with the two-decimal precision of the reference spreadsheet itself,
which means the daily balance computes — within what the data can distinguish — the same
thing as an independent implementation of the model.

The 2.71 pp of configuration 1 does not measure error. It measures the sum of two
deliberate, documented design decisions.

### Measured without touching the engine

To measure Netuno 4's threshold rule (`P_ef = P_t` if `P_t ≥ d`) without modifying the
balance code, the input series is transformed instead:

```text
P′ = P_t + d   when P_t ≥ d
P′ = 0         otherwise
```

so that `max(0, P′ − d)` returns exactly `P_t` on accepted events and `0` on discarded
ones. The measurement never runs against a modified engine, and therefore never risks
comparing against code that is not the code shipped.

### The divergence is systematic, not scattered

In configuration 1 the **signed** mean error equals the absolute mean error in magnitude,
in both independent data sets:

```text
Florianópolis / Brasília:  bias = −2.29 pp   MAE = 2.29 pp   |bias| / MAE = 1.00
Manaus / São Paulo:        bias = −2.71 pp   MAE = 2.71 pp   |bias| / MAE = 1.00
```

Practically every deviation has the same sign: Triton consistently estimates less
savings. It was that pattern — displacement rather than dispersion — that indicated a
structural cause rather than numerical noise, and that prompted the decomposition above.

### Null reference cases

In some rows Netuno 4 exported `0.00` where Triton computes a positive value. The
incidence differs sharply between sets — 0.35% in Manaus/São Paulo against 34.98% in
Florianópolis/Brasília — which points to a characteristic of the reference data rather
than an error in Triton, which never returns zero in those cases. They are segregated
from the statistics so as not to dominate them.

---

## 4. Consequence for publication

Studies that compare results across the two versions **must declare the first-flush
discard difference**. A study published with Netuno 4 remains valid; it was produced under
a stated rule. Re-running it under Triton without saying which rule applied would make
the two incomparable for reasons that have nothing to do with the phenomenon.

---

## 5. What has not been done

The agreement reported here is **verification**: the software computes what its equations
say, and two independent implementations of those equations agree.

**Validation against measured field data has not been performed.** No comparison exists
between a Triton prediction and metered consumption from an instrumented installation
over a comparable period. Until it does, the reported savings are the output of a model
whose internal consistency is established and whose external accuracy is not.

The same reservation applies, more sharply, to the screening life-cycle assessment: the
pump emission factors have no primary source and four of six are extrapolated, and the
module labels them accordingly.
