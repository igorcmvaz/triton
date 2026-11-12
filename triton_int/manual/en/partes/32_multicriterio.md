# Multi-criteria decision

> This section formalises the two ranking methods the program offers and declares three departures
> from the canonical formulation that a published study needs to cite.

Multi-criteria analysis is the branch of operations research that deals with choosing between
alternatives when the evaluation criteria disagree with one another and cannot be reduced to a
single number without someone declaring what is worth more. That is exactly the situation of a
rainwater harvesting project: the volume that delivers most water is not the one that yields most
money, and neither is usually the one with the lowest carbon impact.

What the methods of this section do is not discover the right answer. ==They make explicit the
weighting that would otherwise remain implicit in the choice of whoever decides.== That is the
whole difference between a study that declares its values and one that hides them behind an
apparently objective result.

---

## The eight criteria

The program evaluates each volume of the sweep by eight criteria, grouped into four dimensions:
technical, economic, environmental and structural. Each criterion has a direction of preference:
in some, more is better; in others, less.

Version 0.2.0 replaced the seven criteria in three dimensions of version 0.1.0. Three of the old
criteria — the saving potential, the potable water consumption and, through the bill, the net
present value — measured the same water saved, so the same effect was counted three times. The
new set gives each dimension criteria that pull in different directions, and adds the weight of
the system.

<!-- tabela: The eight decision criteria, their dimension, the direction of preference and the definition the program uses -->
| # | Criterion | Dimension | Direction | Definition in the program |
| :-- | :--- | :--- | :--- | :--- |
| 1 | volumetric reliability | technical | maximise | rainwater consumed ÷ rainwater demand (non-potable use plus irrigation), in % |
| 2 | storage efficiency | technical | maximise | rainwater delivered per day ÷ volume of the lower cistern, in %: the daily turnover of the volume, the annual turnover ÷ 365. It falls with the volume and curbs oversizing. It is not the mean occupancy, which rises with the volume in a wet climate because a large cistern stays full of standing water |
| 3 | net financial savings | economic | maximise | the net present value of the system against the baseline without a cistern: avoided water bill minus investment and running costs, discounted |
| 4 | levelised cost of water (LCOW) | economic | minimise | Equation {{eq:lcow}}, in the project currency per m³. U-shaped in the volume. The alternative with no cistern receives the worst LCOW observed plus 10% |
| 5 | discounted payback | economic | minimise | as in version 0.1.0; an alternative that does not pay back receives the worst payback observed plus 10%, at least one year more and at least 20 years |
| 6 | net life-cycle CO₂e | environmental | minimise | the net CO₂e at the end of the service life (negative = avoided), as in version 0.1.0 |
| 7 | dry mass of materials | structural | minimise | dry mass of the system from the program's weight calculator (`triton.core.system.system_weight`): cisterns, pipes, pump and fittings |
| 8 | annual overflow | structural | minimise | volume overflowed per year, in m³/year |

The levelised cost divides everything the system costs over its life by all the rainwater it
delivers, both discounted at the same rate and over the same horizon as the project:

```equacao:lcow
LCOW = ( CAPEX + Σ [ OPEX_m ÷ ( 1 + MARR )^m ] ) ÷ Σ [ V_m ÷ ( 1 + MARR )^m ]
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `LCOW` | levelised cost of the rainwater delivered | currency/m³ |
| `CAPEX` | initial investment (section {{n:29}}) | currency |
| `OPEX_m` | running cost of month `m`: pumping energy, operation and maintenance, chlorine and the treatment line | currency |
| `V_m` | rainwater delivered in month `m` | m³ |
| `MARR` | minimum attractive rate of return of the project, per month | dimensionless |
| `m` | month of the analysis horizon | — |

A small cistern spreads the fixed costs over little water; a large one pays for volume that stands
idle. Between the two the LCOW reaches a minimum, which is why it does not simply follow the
investment.

The alternatives submitted to the ranking are the volumes simulated in the sweep, and each of them
appears with the eight values above, calculated in sections {{n:23}}, {{n:25}}, {{n:29}} and
{{n:30}} and by the weight calculator. No criterion is invented at this stage: the method only
ranks what the previous analyses have already produced.

> **The weight of the system.** `triton analyze … --analysis all` (and `--analysis system_weight`) also
> reports the dry mass, the water load and the operating load, in kg and kN, split into three
> positions: basement or lower level, roof or upper level, and risers and network. The HTML
> report, the spreadsheet (sheet `system_weight`, with the summary of the chosen volume; the values
> per volume are in the sheet `alternatives`) and the terminal text show the block. Its warnings
> use attention thresholds of the **program**, not of any standard: 500 kg on the roof with the
> upper tank full, an upper tank above 1,500 L, a cistern above 3,000 kg dry, and any concrete
> cistern. Each asks you to confirm the load with the structural or foundation design.

---

## TOPSIS

TOPSIS — *Technique for Order of Preference by Similarity to Ideal Solution*, proposed by Hwang and
Yoon in 1981 — starts from a simple geometric idea. If each alternative is a point in an
eight-dimensional space, one axis per criterion, then there are two reference points: the
**ideal solution**, made up of the best value of each criterion, and the **anti-ideal solution**,
made up of the worst. No real alternative occupies either of them, because none wins at everything
or loses at everything, and the best alternative is the one that is at the same time closest to
the ideal and furthest from the worst case.

The method carries out five steps. It builds the decision matrix, with the alternatives in the rows
and the criteria in the columns; normalises that matrix, so that criteria measured in currency units, in
percentage points and in kilograms come to occupy comparable scales; applies the declared weights;
identifies the ideal and anti-ideal solutions; and ranks the alternatives by relative closeness to
the ideal.

```equacao:topsis
C_i = d_i⁻ ÷ ( d_i⁺ + d_i⁻ )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `C_i` | closeness coefficient of alternative `i`, between 0 and 1 | dimensionless |
| `d_i⁺` | Euclidean distance from alternative `i` to the ideal solution | dimensionless |
| `d_i⁻` | Euclidean distance from alternative `i` to the anti-ideal solution | dimensionless |

The coefficient of Equation {{eq:topsis}} would be 1 for an alternative that coincided with the
ideal solution on all criteria, and 0 for one that coincided with the anti-ideal. As no real
alternative occupies these extremes, what matters is not the absolute value of the coefficient but
the ranking it produces.

---

Applied to a full sweep of the tutorial project (New York) in steps of 1 m³ with the four
dimensions weighted equally, the score peaks at a small volume and falls steadily at the larger
ones, where the investment, the embodied carbon, the idle volume and the mass come to weigh more
than the gain in water ({{fig:fig22_topsis}}). In this project the peak of the full sweep is the
volume section {{n:12}} obtained with seven candidates, but that is not guaranteed: the ideal and
the anti-ideal are built from the set evaluated, so adding or removing alternatives shifts the
reference points and can change the ranking, a phenomenon known as rank reversal.

![The TOPSIS score along the full sweep](../figuras/fig22_topsis.png)

*Figure 99 — TOPSIS score of each volume of the sweep of the tutorial project, with a polyethylene cistern, the four dimensions weighted equally and equal criterion shares; the star marks the volume with the highest score. Figure generated by the program itself.*

---

## Three departures to declare

The program's implementation departs from the canonical formulation in three points, all
deliberate, and a published study needs to declare them so as not to attribute to the original
methods a behaviour that belongs to the program.

**The normalisation is a variant.** Hwang and Yoon's canonical formulation uses vector
normalisation, which assumes non-negative values on all criteria. The net present value, however, is
often negative at small volumes, where the investment does not pay off. The program works around
the restriction by translating each criterion by `x − min(x)` before normalising. The choice is
necessary and deliberate, but presenting the result as canonical TOPSIS would be incorrect: declare
the variant.

**Opricovic's conditions are not implemented.** The VIKOR method, in Opricovic's formulation,
requires two checks on the compromise solution found — acceptable advantage and acceptable
stability — and, when either fails, returns a **set** of equivalent solutions instead of a single
winner. The program always returns the best alternative, without carrying out the test. In
practice, this means that the VIKOR compromise solution should be read alongside the weight
sensitivity analysis, and never alone.

**The attribution of the code.** The implementation of VIKOR and SMAA-VIKOR was written
independently and checked against the `crispyn` library, by Aleksandra Bączkiewicz. TOPSIS was
checked against Hwang and Yoon's original formulation in a case with all values positive, in which
the translation described above is harmless and the two formulations must coincide.

---

## SMAA-VIKOR

SMAA — *Stochastic Multicriteria Acceptability Analysis* — exists to answer the question TOPSIS does
not: what if the weights were different? Instead of requiring a set of weights defined beforehand,
the method draws thousands of weight combinations and returns, for each alternative, the
probability of it occupying each position of the ranking.

Reading the result is direct and informative. A volume that wins in 80% of the draws is a robust
recommendation, which does not depend on a specific weighting to hold. A volume that wins in 30% is
a fragile recommendation, and the text of the study needs to say so instead of presenting the
winner as if it were consensual.

> It is the right tool when there is no consensus on the weights — which is the normal case in real
> projects, where the client, the designer and the regulator usually value different
> dimensions.

---

The most useful reading of the stochastic analysis is not the winner but the margin by which it
wins. A volume that comes first in three quarters of the weight draws is a stable choice, which
survives a change in the decision-maker's priorities; two technically tied volumes indicate the
opposite, and in that case declaring the weight adopted stops being a formality and becomes the
only information supporting the recommendation ({{fig:fig23_smaa}}).

![The first-rank acceptability of each volume](../figuras/fig23_smaa.png)

*Figure 99 — First-rank acceptability (b¹) of each candidate volume, obtained with five thousand weight vectors drawn on the simplex. The highlighted volume is the one that most often comes first, and the others share the rest.*

### The tutorial, by both methods

The table sets side by side the TOPSIS score, with the four dimensions weighted equally, and the
SMAA-VIKOR first-rank acceptability, with five thousand vectors of eight criterion weights drawn,
for the seven volumes of the tutorial in polyethylene with an upper tank. The investment and the
carbon behind the scores are the illustrative figures of section {{n:10}} (illustrative, not a
market price).

<!-- inclui: _tabelas/cap32_decisao.md -->

The two methods agree on the winner, 2,000 L, and disagree on the margin. TOPSIS separates first
from second place, 3,000 L, by under two hundredths of score, a difference no input data supports.
SMAA measures that fragility: 2,000 L wins in 39.2% of the draws, 3,000 L in 25.0%, 4,000 L in 18.2%
and 1,000 L in 14.2%. By the yardstick of section {{n:20}}, a winner below 40% is a choice that
depends on the weights, and the study should say so and declare 3,000 L and 4,000 L as the
alternatives. The largest volumes, 8,000 L and 12,000 L, win in almost no draw: no plausible
weighting recommends them, and that is also a result.

---

## The weights

The program takes four dimension weights — technical, economic, environmental and structural, 25%
each by default — and shares each one among the criteria of its dimension by the **criterion
shares**. The shares are equal by default; only the proportion within the dimension matters, and a
share of zero removes the criterion from the calculation. With the default, each technical and
each structural criterion weighs 12.5%, each economic criterion 8.33% and the single environmental
criterion 25%.

```equacao:pesos_dos_criterios
w_j = W_d × s_j ÷ Σ s_k
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `w_j` | weight of criterion `j` in TOPSIS, VIKOR and PROMETHEE II | dimensionless |
| `W_d` | weight of the dimension `d` of criterion `j`, normalised so that the four add up to 1 | dimensionless |
| `s_j` | share of criterion `j` within its dimension | dimensionless |
| `Σ s_k` | sum of the shares of the criteria `k` of the same dimension | dimensionless |

Eight direct weights, one per criterion, are also accepted, and then the shares do not apply.
VIKOR, PROMETHEE II and TOPSIS use the same rule. SMAA-VIKOR draws eight weights on the simplex,
and gives the central weight vector of each volume per criterion and summed into the four dimensions.

**Weights from version 0.1.0.** Three weights — technical, economic, environmental, as projects and
studies up to version 0.1.0 declared them — are still accepted: the structural dimension receives
their mean, so equal weights stay equal. Seven values, weights or shares of the old seven-criterion
model, are refused with a message that says why (section {{n:37}}): they cannot be mapped onto the
eight new criteria. To reproduce a study made with version 0.1.0, use version 0.1.0.

**Where the weights are declared.**

<!-- tabela: Where the multi-criteria weights and the criterion shares are declared -->
| Where | Dimension weights | Criterion shares |
| :--- | :--- | :--- |
| decision tab | four boxes, Technical, Economic, Environmental and Structural, 25% each; the profiles «Balanced: 25% on each dimension» and «Prioritise …» with 70% on one dimension and 10% on each of the others | the «Criterion shares» row, with eight boxes (Reliability, Efficiency, Savings, LCOW, Payback, CO₂, Mass, Overflow) and the «Equal shares» button |
| command line | `--weights t,e,a,s`, or eight values; three are still accepted | `--criterion-shares` with eight values, default `1,1,1,1,1,1,1,1` |
| project file | `analysis.topsis_weights`, four or eight values | `analysis.topsis_criterion_shares`, eight values |
| declarative study | `analise.pesos`, four or eight values; three are still accepted | `analise.partes_no_eixo`, eight values |

The choice of weights, however, is not technical: it is a statement of value, and therefore needs to
appear in the text of the study, with the four dimension weights and the criterion shares. ==The statement «optimal volume by
TOPSIS», without the weights, is impossible to reproduce,== and two studies with different weights
reach different volumes without either of them being wrong.

Three courses are defensible, and the choice between them depends on how much is known about the
priorities of whoever decides. Equal weights, explicitly declared as an absence of preference, are
the neutral position. Justified weights, with the reason for each one, are preferable when the
priorities are known. And SMAA, reporting the range of results instead of a single winner, is the
most complete course when there is no consensus.

---

## The best by each criterion alone

Besides the weighted ranking, the program identifies the winner of the technical, financial and
environmental dimensions taken alone — the most reliable volume, the one with the shortest payback
(ties broken by the net saving) and the one with the lowest life-cycle carbon — and reports the three
separately. They are numbers worth
publishing together, because each one answers a legitimate and different question.

When the three coincide, the recommendation is strong and the decision needs no weighting. When
they diverge, which is the common case and that of the tutorial, ==the divergence **is** the
result:== hiding it behind a single weighted number impoverishes the study and hands the reader a
conclusion they have no way of evaluating.

---

## What the method does not do

It is worth ending with the limits, because multi-criteria methods are often presented with an
authority they do not have.

**They do not choose the weights.** The weighting belongs to the analyst, and it is a decision of
value, not of technique. No statistical procedure replaces it.

**They do not validate the criteria.** If the net present value is wrong because the tariff
structure was entered incorrectly, TOPSIS will rank the error with impeccable precision. The
method ranks what it receives.

**They do not incorporate constraints.** Space available on the site, maximum budget, a regulatory
requirement: all of these are filters prior to the ranking, applied by the designer when deciding
which volumes even enter the comparison.
