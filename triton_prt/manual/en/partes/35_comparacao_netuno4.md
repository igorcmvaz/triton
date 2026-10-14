# Comparison with Netuno 4

> This section presents the measurement against 4,050 reference cases and, more importantly, the
> **breakdown** of the difference by cause.

---

## The role of the comparison

It is worth starting by making clear what this comparison is **not**. ==Netuno 4 is not a fidelity
target for Triton.== The current version adopts different modelling decisions, deliberate and
documented, and it would be a cause for concern, not satisfaction, if the results coincided
exactly.

The value of Netuno 4 in this verification is another, and a greater one: it offers an independent
set of results, produced by another implementation of the same conceptual model, by other hands and
in another language. Without an external reference of this kind, verification would be limited to
internal properties of the program — necessary, as section {{n:34}} describes, and unable to detect
a systematic error that respected them all.

---

## The reference data

The comparison between the two versions rests on four thousand and fifty cases exported from
Netuno 4 and preserved since then, byte for byte, precisely so that the reference would not change
during development. They are spread over two sets, with different cities and parameter ranges.

<!-- tabela: The sets of reference cases exported from Netuno 4 -->
| Set | Cases | Cities |
| :--- | ---: | :--- |
| Floripa/Brasília | 1,458 | Florianópolis, Brasília |
| Manaus/São Paulo | 2,592 | Manaus, São Paulo |

---

## The total divergence

<!-- tabela: Divergence measured between the two versions, by set of cases -->
| Set | Mean absolute error | Bias | Maximum error | ≤ 5 pp |
| :--- | ---: | ---: | ---: | ---: |
| Floripa/Brasília | 2.29 pp | −2.29 pp | 7.43 pp | 97.4% |
| Manaus/São Paulo | 2.71 pp | −2.71 pp | 10.60 pp | 88.6% |

The bias is systematically negative in both sets, that is, Triton estimates less saving than
Netuno 4 in practically every case. The result is expected, and the next subsection breaks the
difference down into its attributable causes.

---

## The breakdown, which is the number that matters

Comparing the potential at the optimal volume of one program directly with that of the other mixes
three differences of different kinds, and the resulting number does not say which one accounts for
what. The breakdown separates them by comparing the two programs in three successively more
controlled configurations, over the 2,583 cases of Manaus and São Paulo.

<!-- tabela: Divergence in three successively more controlled configurations -->
| Configuration | Mean absolute error | Bias | ≤ 5 pp |
| :--- | ---: | ---: | ---: |
| 1. Triton optimum against Netuno 4 optimum | 2.71 pp | −2.71 pp | 88.6% |
| 2. evaluated at the volume Netuno 4 declared optimal | 1.60 pp | −1.60 pp | 96.4% |
| 3. likewise, adopting Netuno 4's threshold first flush | **0.25 pp** | **−0.25 pp** | **100.0%** |

The three configurations use the same cases, excluding the nine with a null reference dealt with
below. In each one, Triton estimates less than Netuno 4 in almost every case, and that is why the
mean absolute error practically coincides with the bias.

The resulting attribution:

<!-- tabela: Attribution of the divergence to its three sources -->
| Source of the divergence | Contribution | Nature |
| :--- | ---: | :--- |
| optimal volume selection criterion | 1.11 pp (41%) | design difference |
| treatment of the first flush | 1.36 pp (50%) | deliberate methodological difference |
| **residual of the water balance** | **0.25 pp (9%)** | — |

> **With the two known differences neutralised, the Triton engine reproduces Netuno 4 with a
> mean absolute error of 0.25 percentage points and 100% of the cases within 5 points.**
>
> The residual is consistent with the two-decimal precision of the reference spreadsheet itself.
> It is **this** number that verifies the engine. The total bias of 2.71 pp does not measure error:
> it measures the sum of two design decisions, both deliberate.

---

{{fig:fig25_cascata}} breaks the total divergence down into the three sources of the table.

![The divergence broken down to the residual](../figuras/fig25_cascata.png)

*Figure 42 — The mean divergence relative to Netuno 4, broken down. The first bar is the total observed; the two orange ones are declared method differences, one of design criterion and the other of first-flush treatment; the last is the residual of the water balance, which is the number that actually verifies the engine.*

---

## The two differences, in detail

### The first flush

Netuno 4 treats the first-flush depth as an event threshold: when the day's precipitation is below
it, nothing is collected; when it exceeds it, the whole rain is collected, with no subtraction at
all. The Netuno 4 manual is explicit about it, stating that a daily precipitation below that value
makes the program consider that there was no precipitation.

Triton subtracts the depth from the day's precipitation, a physically more faithful treatment
because the water diverted to the self-cleaning device does not reach the cistern. The change
accounts for half of the total divergence measured between the two versions.

### The optimal volume criterion

Both programs choose the ideal volume by marginal-gain criteria, but the implementations and the
search grids differ, so each one elects a different volume and the comparison comes to include that
difference of choice. Evaluating the two programs at the same volume — the one Netuno 4 declared
optimal — the bias falls from 2.71 to 1.60 percentage points, which attributes 41% of the total
difference to the selection criterion.

---

## How to measure the difference without changing the engine

The emulation of the old rule is done by transforming the input precipitation series, not by
changing the water balance code. The methodological distinction is essential: measuring the
divergence with modified code would validate a program that is not the one distributed to the
user, which would defeat the purpose of the verification.

```equacao:emulacao
P′ = P + d_f se P ≥ d_f ; P′ = 0 caso contrário
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `P′` | transformed precipitation, to be supplied to Triton | mm |
| `P` | precipitation observed on the day | mm |
| `d_f` | first-flush depth | mm |

With this transformation applied, the Triton calculation `P_ef = max(0, P′ − d_f)` reproduces the
threshold semantics exactly. The measurement does not run the risk of validating code that is not
the one distributed.

> **A documentation caveat.** The internal verification protocol says to use an automatic option
> for this emulation. That option **is not implemented**. Use the series transformation, or compare
> with a first flush of zero, where the two rules coincide.

---

## The null-reference cases

In some of the rows, Netuno 4 exported zero while Triton calculates a positive value. The
incidence differs greatly between sets: 0.35% in Manaus and São Paulo against 34.98% in Floripa and
Brasília.

The disparity points to a feature of the **reference data** — probably Netuno 4 did not find an
optimal volume under its own criterion — and not to an error of Triton, which never returns zero
in these cases. They are kept apart from the statistics so as not to dominate them.

---

## What to declare in a comparative study

- the **two numbers**: the total divergence and the residual after the breakdown;
- the two deliberate differences, named;
- whether the comparison was made with a zero first flush, with threshold emulation, or without
  neutralisation;
- the version of each program.

Presenting only the total divergence, without breaking it down, suggests an engine error that does
not exist.
