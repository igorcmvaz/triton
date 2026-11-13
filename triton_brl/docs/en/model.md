# The computational model

This document states what Triton computes, with the equations, the conventions and the
boundary of each one. It is the English counterpart of
[`../metodologia.md`](../metodologia.md), which carries the same model in full together
with the Brazilian data sources.

Every statement of a limit here is deliberate. A model is only usable if what it does not
represent is as legible as what it does.

---

## 1. Effective rainfall and capture

The first-flush discard depth `d` is a depth **actually subtracted** from the rainfall of
the event: the water diverted to the discard device does not reach the tank. On days when
the discard rule is active,

```text
P_ef,t = max(0, P_t − d)      if the discard rule applies on day t
P_ef,t = P_t                  otherwise
V_cap,t = P_ef,t × A × C
```

with `P` in mm/day, `A` in m², `C` dimensionless, and `V_cap` in litres, since 1 mm over
1 m² is 1 L.

`A` is the catchment area **in horizontal projection**, not the sloped area of the roof.
For a roof at 30% slope, using the sloped area overestimates capture by 4.4% on every
single day.

What varies between the three discard modes is not the formula but the days on which it
fires:

| Mode | Rule | Applies on |
| :--- | :--- | :--- |
| 1 | every event | every day with `P_t > 0` |
| 2 | first event after a dry spell | days with `P_t > 0` whose previous day had `P_t < 1 mm` |
| 3 | maintenance interval | days with `P_t > 0`, respecting a configured minimum interval since the last discard |

`d` is a **depth** in millimetres, not the hydraulic volume of the physical first-flush
device, which is `A × d` litres and must be sized separately. When it is not declared, `d`
defaults to **2.0 mm**, the value of ABNT NBR 15527:2019, item 4.1.5.

> **A deliberate difference from Netuno 4.** Netuno 4 treated `d` as an event threshold,
> capturing `P_t` in full whenever `P_t ≥ d`. Triton subtracts the depth, which is
> physically more faithful. The consequence is measurable and quantified in
> [`verification.md`](verification.md): Triton estimates on average 2.3 to 2.7
> percentage points less potable water savings than Netuno 4 over 4,050 reference cases,
> of which this change accounts for half. **Studies comparing results across the two
> versions must declare this difference.**

---

## 2. Demand and the daily balance

Demand has two parts. Indoor demand is `D_in,t = N × q`, with `N` occupants and `q` the
per-capita consumption; a monthly profile multiplies the corresponding days. Outdoor
demand (irrigation, washing of external areas) is a daily volume `Q_ex`, suspended on days
whose rainfall reaches a threshold (2 mm by default). Total demand is
`D_tot,t = D_in,t + D_ex,t`.

The rainwater call is `D_pl,t = f_in × D_in,t + D_ex,t`, where `f_in` is the non-potable
share of **indoor** use. The **total** replaceable fraction

```text
f = (f_in × D_in + Q_ex) / (D_in + Q_ex)
```

is derived from the two and is not an input: the interface shows it in a read-only field
and the project file stores it for reading. Without outdoor demand, `f = f_in`. Changing
`f` from the command line (`--share`, `--set rainwater_share=…`) recomputes `f_in`, keeping
the outdoor demand; changing `f_in` or `Q_ex` recomputes `f`; changing both inconsistently
is refused. The rule lives in `triton/core/fracao_atendivel.py`.

In the lower tank the program caps the store and computes the overflow *before*
withdrawing the demand, as in the **yield-after-spillage** (YAS) rule, but the same
day's rain is already available to that day's demand:

```text
Avail_t     = S_{t−1} + V_cap,t
S_before,t  = min(V, Avail_t)
Overflow_t  = max(0, Avail_t − V)
Supplied_t  = min(D_pl,t, S_before,t)
S_t         = S_before,t − Supplied_t
```

The order of these five lines is not an implementation detail: it decides how much the
system delivers. Under strict YAS (Fewkes and Butler, 2000) the day's yield comes only
from the previous day's store, `Supplied_t = min(D_pl,t, S_{t−1})`; under YBS the demand is
withdrawn before the overflow is computed. Triton sits between the two: its yield is never
below strict YAS nor above YBS, and it departs most from YAS with small tanks. EN
16941-1:2024 (Annex A.3) uses strict YAS, so for the same volume Triton reports a slightly
higher coverage.

Where an upper tank exists, pumping is an additional internal transfer bounded by both
stores and by a trigger level. The auditable balance over both tanks is

```text
initial store + capture = final store + rainwater consumed + overflow
```

and it is asserted by the invariant layer of the test suite on every simulated case.

### The capacity grid

The step you type is an editable reference. To bound computation time the engine builds
the grid by one reproducible rule:

```text
ΔV₀ = 250 × ceil(ΔV_requested / 250)
while ceil(V_max / ΔV) > 40:  ΔV = 2 × ΔV
grid = {0, ΔV, 2ΔV, …} ∪ {V_max}
```

The effective step is always a multiple of 250 L, there are at most 40 positive
capacities, and the user's maximum volume is never discarded. The software reports any
adjustment and stores `requested_step_l`, `effective_step_l` and `step_adjusted`
alongside the result.

---

## 3. What actually depends on tank capacity

| Relationship | Variables | Treatment |
| :--- | :--- | :--- |
| direct | price and embodied impact of the lower tank | interpolated from the price table and the material's mass factor |
| endogenous | water supplied, failures, overflow, volume pumped, pump starts, energy, chlorine, avoided revenue, variable O&M | each capacity is re-simulated day by day |
| independent input | upper tank, pipe lengths and diameters, pump rating, accessories | held constant across the sweep |

Costs and impacts are therefore **not** scaled indiscriminately by capacity. If pipework
or pump should change between capacities, declare distinct physical scenarios and record
the sizing rule used.

---

## 4. Indicators

```text
E_pot = Σ V_con,t / Σ D_tot,t        potable water savings
R_v   = Σ V_con,t / Σ D_pl,t         volumetric reliability
R_t   = (days fully supplied) / N    temporal reliability
```

The denominator of `E_pot` is **total** demand, not non-potable demand. A system meeting
every non-potable use perfectly is therefore bounded above by the attainable fraction,
typically 25% to 40% in a dwelling. Confusing the two is the most common misreading of a
Triton result.

The **technical optimum** is the first discrete point on the ordered sweep whose marginal
gain `Δ E_pot / ΔV` falls at or below a configured threshold. It depends on the step of
the sweep, and it is **not the maximum or minimum of any objective function** — it is a
stopping rule. Two analysts with different thresholds obtain different 'ideal volumes',
and both are defensible. The economic optimum (shortest discounted payback, with NPV as the
tie-breaker) and the environmental optimum
(minimum carbon balance) are optima of a function, and generally fall elsewhere.

---

## 5. Pumping and chlorination

```text
E = P × [(V_pumped / Q) + (n_starts × t_start)] / η
```

with `P` in kW, the bracketed term in hours and `η` the overall efficiency as a fraction.
With no upper tank, pumping energy is zero.

Note that `P` is the **shaft** power. ABNT NBR 17094-2:2016 requires the motor efficiency
to be marked on the nameplate *separately* from the power, so the nameplate figure is the
power available at the shaft, not the power drawn at the socket. Treating one as the other
underestimates consumption by a factor equal to the motor efficiency — 60.5% for a
half-horsepower two-pole machine.

```text
m_Cl2,active (kg/yr) = V_treated (m³/yr) × dose (mg/L) / 1000
m_product    (kg/yr) = m_Cl2,active / purity
```

**Purity is in the equation on purpose.** The dose is prescribed as active chlorine, but
what is bought, transported and manufactured is the tablet, at 65% active chlorine. Adding
an active-chlorine dose to a per-kilogram factor for the tablet underestimates by 35%.
The chain lives in `triton/core/chlorination.py`, and the environmental, economic and
water-quality modules all read from it.

This estimates **applied mass in chlorine equivalent**, not the chlorine demand of the
water. Chlorine demand is the difference between applied dose and residual after contact
time, and requires bench testing on the source water. The default dose serves an economic
and environmental scenario; it does not prescribe treatment.

---

## 6. Economics

Effective water and sewerage tariffs are **marginal differences**: the monthly bill for
the simulated total demand is compared with the bill after the rainwater saving,
preserving the consumption blocks, the fixed availability charge and the sewerage
charging mode. Savings therefore come out of the most expensive block, which is why
multiplying the saved volume by an average tariff overstates or understates the benefit
depending on where in the block structure the household sits.

```text
CF_t = water_saving_t + sewerage_saving_t − energy_t − O&M_t − chlorine_t
NPV  = −CAPEX + Σ CF_t / (1 + MARR)^t
```

Tariffs, electricity and O&M receive the configured escalation rates. The IRR zeroes the
NPV of the nominal flows; simple and discounted payback are the first year in which the
corresponding cumulative flow turns non-negative. Projections do **not** automatically
include taxes, financing, residual value or replacements; declare them as premises where
they matter.

---

## 7. Screening life-cycle assessment

For each alternative, the assessment sums tanks, pipework and pumps, adds operation and
subtracts the credit for mains water avoided:

```text
net_CO2_lifetime = embodied_CO2
                   − years × (avoided_CO2_water − CO2_pump − CO2_treatment)
```

**Sign convention: positive emits, negative removes.** A negative lifetime balance means
the system removes more carbon over its life than it emits. The convention is the same in
the equations, the tables, the figures and the software's own charts.

Because embodied carbon is affine in capacity while the yield function is concave, the
carbon balance is convex and has a unique minimum — and that minimum is frequently
*interior*. More tank is not monotonically better for the climate: past a certain
capacity, each additional litre of storage emits more than it avoids.

Emission factors have declared sources, item by item, in
[`../procedencia_fatores_co2.md`](../procedencia_fatores_co2.md). Two reservations stand:

- The grid factor is **CO₂-equivalent, not CO₂**. The MCTI/SIRENE series covers carbon
  dioxide only and generation only; using it here would underestimate pumping.
- The **pump** factors remain without a primary source, and four of the six values are
  arithmetic extrapolations. No catalogue consulted publishes mass by rating. They carry
  the screening label, and they should.

This is a screening assessment. It is **not** an inventory compliant with ISO 14040/14044.

---

## 8. Multi-criteria decision

Since version 0.2.0 there are **eight criteria on four axes**, three of benefit and five
of cost:

| Axis | Criterion | Sense | Definition in the software |
| :--- | :--- | :--- | :--- |
| technical | volumetric reliability | benefit | rainwater consumed ÷ rainwater demand (non-potable use plus irrigation), in % |
| technical | storage efficiency | benefit | rainwater delivered per day ÷ lower-tank capacity, in % (annual turnover ÷ 365); it falls with capacity and curbs oversizing |
| economic | net financial savings | benefit | the system NPV against the no-tank baseline |
| economic | levelised cost of water (LCOW) | cost | (investment + Σ discounted annual running costs: energy, O&M, chlorine, treatment line) ÷ Σ discounted rainwater delivered, at the project rate and horizon, per m³ in the project currency; the no-tank option takes the worst observed LCOW + 10% |
| economic | discounted payback | cost | an option that never pays back takes the worst observed payback + 10% (at least one more year, and at least 20 years) |
| environmental | life-cycle CO₂e | cost | net CO₂e at the end of the service life (negative = avoided) |
| structural | dry mass of the system | cost | dry mass of tanks, pipes, pump and fittings, from the system-weight calculator |
| structural | annual overflow | cost | overflow volume per year, in m³ |

> Up to 0.1.0 there were seven criteria on three axes: potable water savings and overflow;
> NPV, discounted payback and IRR; life-cycle CO₂ and potable water consumed. Savings,
> overflow and potable consumption measured the same saved water. The eight-criterion model
> reduces that collinearity and brings the weight of the system into the decision.

**Weights.** Four axis weights (technical, economic, environmental, structural; 25% each by
default) are split within each axis by the *criterion shares* (default: equal shares):
`w_j = W_e × p_j / Σ p_k`, with `k` running over the criteria of axis `e`. Eight direct
weights are used as given, normalised by their sum. Three weights (projects and studies up to
0.1.0) give the structural axis the mean of the three, so equal weights stay equal; seven
values are refused. VIKOR, PROMETHEE II and TOPSIS use the same rule; SMAA-VIKOR samples eight
weights with an expected 25% per axis and reports the central weights aggregated on the four
axes. On the command line, `--weights` and `--criterion-shares`; in the project file,
`analysis.topsis_weights` and `analysis.topsis_criterion_shares`; in a declarative study,
`analise.pesos` and `analise.partes_no_eixo`.

**Objective weights (CRITIC).** In place of the weights, the word `critic` (`--weights critic`,
`analysis.topsis_weights: "critic"`, `analise.pesos: "critic"`, or the decision tab's profile
for objective weights) asks for the weights of Diakoulaki, Mavrotas and Papayannakis (1995,
*Computers & Operations Research* 22(7), 763–770, doi:10.1016/0305-0548(94)00059-H). Each
criterion is normalised from 0 (worst observed value) to 1 (best); its information is
`C_j = σ_j × Σ_k (1 − r_jk)`, with `σ_j` the standard deviation of the normalised criterion and
`r_jk` the Pearson correlation between criteria, and the weight is `w_j = C_j / Σ C`. A constant
criterion weighs zero. The weights come from the alternatives with a tank larger than zero, are
recomputed at every analysis and apply to TOPSIS, VIKOR and PROMETHEE II; SMAA still samples its
weights. CRITIC measures contrast and independence in the results themselves, not importance:
the weights change with the set of volumes, express nobody's preference, and a criterion that
varies across volumes gains weight even if it matters little. It is a choice of method; the
default remains 25% per axis.

**Choice band.** When several volumes score alike, the software does not name "the best volume":
it reports the volumes larger than zero whose score, normalised between the worst (0) and the
best (1) of the volumes evaluated, lies within a tolerance of the best (default 5% of the
range), with the highest-scoring volume alongside. The same rule applies to the TOPSIS score,
the VIKOR index Q (lower is better), the PROMETHEE II net flow and the SMAA first-rank
acceptability. The tolerance is set with `--score-band` (0 to 1), `analysis.topsis_score_band`
or `analise.tolerancia_faixa`; the JSON output carries `topsis.choice_band` and
`smaa_vikor.choice_band`. The band depends on the grid of volumes and on the tolerance; a study
should state both.

**System weight.** `triton analyze --analysis system_weight` (or `all`) reports the dry
mass, the water load and the operating load (kg and kN) at three positions: lower level,
roof or upper level, and risers and pipework. Four alerts ask for confirmation with the
structural or foundation design: more than 500 kg on the roof with the tank full, an upper
tank above 1,500 L, a lower tank above 3,000 kg dry, and a concrete lower tank. These are the
software's own attention thresholds, not limits from any standard.

To admit negative values without a conditional correction, each column is translated by
its worst observed value, `z_ij = x_ij − min(x_j)`, then vector-normalised,
`r_ij = z_ij / √Σ z_ij²`. Non-negative normalised weights are applied, the Euclidean
distances `D⁺` and `D⁻` computed, and the score is `C_i = D⁻ / (D⁺ + D⁻)`.

> **This is a declared variant, not canonical TOPSIS.** Hwang and Yoon (1981) normalise by
> the Euclidean norm of the original values. Where all values of a criterion are positive
> and the minimum is zero the two coincide; where NPV is negative — the case that motivated
> the change — they diverge, and the scores are not comparable with a canonical
> implementation over the same matrix.

VIKOR, in `triton/core/mcdm_methods.py`, computes `S`, `R` and `Q` after Opricovic and
Tzeng (2004) but **does not apply conditions C1 (acceptable advantage) and C2 (acceptable
stability)**. The ranking is therefore an ordering by `Q`, not a claim that the leader is
a stable compromise.

SMAA-VIKOR follows Lahdelma and Salminen (2001), sampling the eight weights from a
Dirichlet with parameters (1, 1, 2/3, 2/3, 2/3, 2, 1, 1): each axis sums to 2, so each axis
has an expected weight of 25% and each criterion the TOPSIS default (a symmetric Dirichlet
would give the three-criterion economic axis 37.5% on average and the one-criterion
environmental axis 12.5%). It is an independent NumPy implementation following the design of the
`crispyn` library (A. Bączkiewicz, MIT licence), which serves as a comparison baseline and
not as the origin of the code.

Alongside the aggregate score the software reports a weight-independent gap:

```text
gap_ij       = [max(x_j) − x_ij] / [max(x_j) − min(x_j)]
proximity_ij = 1 − gap_ij
```

so that 100% is the best result observed on that criterion and 0% the worst. This
separates a winner that is close to every optimum from a compromise that loses heavily
on one axis. TOPSIS is sensitive to the weights and to the set of alternatives; use the
sensitivity analysis, and do not read the ranking as physical truth.

---

## 9. What the model does not represent

- **No urban drainage.** No catchment routing, no network effect of many systems.
- **No hydraulic design.** No head-loss sizing of pipework, no construction drawings.
- **No evaporation or leakage** from the tank, and no water quality decay in storage.
- **Rainfall is a daily total.** 20 mm in one hour and 20 mm over twenty-four hours give
  the same result.
- **Discard is a depth**, not a device with its own emptying dynamics between events.
- **The LCA is screening**, and the pump factors are extrapolated.
- **Chlorination is a scenario**, not a treatment prescription.

Agreement between the software's own outputs demonstrates internal verification of the
same equations. External validation requires measured data and an independent comparison.
