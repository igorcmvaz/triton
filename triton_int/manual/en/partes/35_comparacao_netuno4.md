# Verification against analytical solutions and benchmarks

> This section shows how the engine is checked against results it did not produce: closed-form
> solutions, a hand-checkable case, published sizing rules and independent programs, and what each
> check can and cannot prove.

---

## The role of the comparison

A comparison with another tool is not a fidelity target. ==Two programs that agree to the last
decimal may share the same mistake; two programs that differ may differ for good reasons.== What a
comparison offers is an independent set of results, produced by another hand, and the chance to
explain every difference by a cause. Without an external reference of this kind, verification
would be limited to the internal properties of section {{n:34}} — necessary, and unable to detect
a systematic error that respected them all.

The checks below run from the strongest to the weakest. The strongest need no reference program at
all.

---

## Closed-form solutions

In a few situations the correct answer follows from the equations, with no simulation. Constant
rain and constant demand give a tank that fills to a known level; a tank of zero capacity can
supply only what falls on the day; a tank of unlimited capacity supplies the demand whenever the
mean supply exceeds it, and the potential is then the whole of the suppliable fraction. The suite
asserts each of these within numerical tolerance. Because the expected value comes from
deduction, not from an earlier run of the program, an error cannot hide in both.

---

## A case you can check by hand

The ten-day case of section {{n:23}} is small enough to follow with pencil and paper: 100 m²,
runoff coefficient 0.85, first flush 2.0 mm, 2,000 L tank, 80 L/day of rainwater demand, and the
New York rain of 21 to 30 September 2018. The program reports 8,483 L collected, of which 6,209 L
overflow, 514 L are consumed and 1,760 L remain in the tank. The three outputs sum to the input
exactly (8,483 − 6,209 − 514 = 1,760), and the residual of the balance is zero. Repeating two days
by hand — the 59.8 mm day that overflows the tank, the 1.9 mm day that falls under the first flush
and collects nothing — is the quickest way to learn what the program does with each rule.

---

## Published sizing rules as benchmarks

Sizing rules of thumb are not exact, but they bracket the answer. The tutorial house (150 m²,
600 L/day, 28% suppliable) was sized by five methods, and each volume was then run through the
daily simulation to obtain the potential it actually delivers.

- practical rule of 6% of annual demand: 3,750 L, potential 26.66%;
- daily simulation with a marginal-gain criterion: 4,000 L, potential 26.83%;
- monthly Rippl diagram: 5,750 L, potential 27.43%;
- daily Rippl diagram: 8,000 L, potential 27.74%;
- practical rule of 0.05 times rainfall times area: 8,500 L, potential 27.78%.

The methods disagree by a factor above two in volume and by 1.1 percentage points in potential. The
spread is the useful result: beyond about 4,000 L, the curve of section {{n:7}} is flat, and every
rule lands on it. A rule that gives a volume far outside this range for the same inputs deserves a
second look.

---

## Comparing with another program

Comparing with an independent tool answers a different question: do two implementations of the
same conceptual model agree? Agreement is expected only when the modelling decisions agree. Two
differ often enough to matter.

The first is the **first flush**. Subtracting the depth from the day's rain, as Triton does, is
physically faithful, because the diverted water never reaches the cistern. Some tools instead treat
the depth as an event threshold: below it nothing is collected, above it the whole rain is. The
second is the **volume criterion**: tools choose the ideal volume by marginal gain on different
grids, and so elect different volumes. Comparing optima therefore mixes the difference in
criterion with the difference in engine; compare potentials at the **same** volume.

### Emulating a threshold rule without changing the engine

The old rule is emulated by transforming the input rainfall series, not by changing the water
balance code. Measuring a divergence with modified code would verify a program that is not the one
distributed to the user.

```equacao:emulacao
P′ = P + d_f se P ≥ d_f ; P′ = 0 caso contrário
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `P′` | transformed precipitation, to be supplied to Triton | mm |
| `P` | precipitation observed on the day | mm |
| `d_f` | first-flush depth | mm |

With this transformation applied, the Triton calculation `P_ef = max(0, P′ − d_f)` reproduces the
threshold semantics exactly. The program has no option that does this automatically; use the series
transformation, or compare with a first flush of zero, where the two rules coincide.

{{fig:fig25_cascata}} illustrates how a total divergence between two programs is broken down by
cause, down to a residual.

![The divergence broken down to the residual](../figuras/fig25_cascata.png)

*Figure 42 — Breakdown of the mean divergence between the program and an independent reference. The first bar is the total observed; the intermediate bars are declared differences of method, such as the criterion for the optimal volume and the first-flush treatment; the last is the residual of the water balance, which is the number that actually verifies the engine.*

---

## Reference rows with a null result

Reference tools sometimes export zero where Triton calculates a positive value, typically because
the tool did not find an optimal volume under its own criterion. Such rows point to a feature of the
**reference data**, not to an error of the program. Keep them apart from the statistics, so as not to
let them dominate the mean.

---

## What to declare in a comparative study

- the **two numbers**: the total divergence and the residual after the breakdown;
- the deliberate differences of method, named;
- whether the comparison used a zero first flush, threshold emulation, or no neutralisation;
- the version of each program.

Presenting only the total divergence, without breaking it down, suggests an engine error that may not
exist.
