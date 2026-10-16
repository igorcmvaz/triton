# Ideal volume and the sweep

> This section formalises what section {{n:7}} did in practice: how the program builds the
> grid of volumes and how it applies the ideal-volume criterion.

---

## The discrete grid

The sweep simulates a **finite** set of volumes, and building that set follows three rules.

**The step is rounded up to a multiple of 250 litres.** It is the commercial quantum: tanks
are sold in standard volumes, and an optimum at 1,300 L cannot be bought. When the step
asked for is not a multiple of 250, the program adjusts it and records the adjustment in
`step_adjusted`, so that the report can declare the effective step.

**The number of positive volumes is limited to 40.** A sweep from 0 to 50,000 L with a
100 L step would be 500 thirty-year simulations, and the gain in information does not pay
the cost. When the limit is reached, the effective step grows.

**The maximum volume entered is always kept** as the last point of the grid. Only the last
interval can therefore be smaller than the effective step.

Volume **zero** enters the grid as the reference alternative: it is the no-system scenario,
against which the others are compared.

---

The practical consequence appears in {{fig:fig14_grade}}. With a fine step, the curve shows
the knee where the return starts to fall off; with a coarse step, the knee falls between two
points of the grid and the criterion picks the first tabulated volume after it, which may lie
several cubic metres beyond the volume that really matters.

![The same curve seen through two sweep grids](../figuras/fig14_grade.png)

*Figure 99 — Saving potential curve of the same building, swept with a 250 L step and with a 5,000 L step. The coarse grid calculates each point it contains correctly, but it does not contain the stretch of greatest curvature, between 1 and 5 m³.*

---

## The marginal gain

The curve of saving potential against volume is monotonic and concave: each cubic metre added
to the tank yields less than the previous one, and the yield tends to zero as the system
approaches the ceiling set by the suppliable fraction. The program quantifies this
diminishing yield by the discrete derivative of the curve, calculated for each volume of the
grid from the second one on.

```equacao:ganho_marginal
Δ(V_i) = [ Epot(V_i) − Epot(V_i−1) ] ÷ [ (V_i − V_i−1) ÷ 1000 ]
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `Δ(V_i)` | marginal gain of volume `V_i` relative to the previous one | %/m³ |
| `Epot(V_i)` | potable water saving potential obtained with volume `V_i` | % |
| `Epot(V_i−1)` | saving potential obtained with the next smaller volume | % |
| `V_i` | tank volume at position `i` of the grid | L |
| `V_i−1` | next smaller volume of the grid | L |
| `1000` | conversion from litres to cubic metres | L/m³ |

The division by one thousand in the denominator of Equation {{eq:ganho_marginal}} is there so
that the result comes out in percentage points per added cubic metre, which is the unit in
which the decision is made — tanks are bought and priced in cubic metres, not in litres.

==Being a discrete derivative, the marginal gain depends on the grid step.== A fine grid
produces a more local value, close to the true derivative at that point; a coarse grid
produces the mean yield over a larger interval. The subsection on sensitivity to the step,
further on, measures the size of that effect.

---

## The ideal-volume criterion

The ideal volume is defined as the smallest positive volume of the grid whose marginal gain has
already fallen below a threshold declared by the user.

```equacao:volume_ideal
V_ideal = min { V_i > 0 : Δ(V_i) ≤ Δ_lim }
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_ideal` | ideal volume by the marginal-gain criterion | L |
| `V_i` | tank volume at position `i` of the grid | L |
| `Δ(V_i)` | marginal gain of volume `V_i`, from Equation {{eq:ganho_marginal}} | %/m³ |
| `Δ_lim` | marginal-gain threshold declared by the user; the program opens with 5.0, and the tutorial adopts 1.0 | %/m³ |

When no volume of the grid meets the condition of Equation {{eq:volume_ideal}} — which happens
when the swept range ends before the curve flattens — the program adopts the largest volume of
the grid and records that circumstance in the report, so that the reader knows that the optimum
found is a limit of the search and not a turning point of the curve.

### An example, step by step

The sweep table of the tutorial, in section {{n:7}}, lets you redo the calculation by hand.
Between 3,000 L and 4,000 L the potential rises from 25.99% to 26.83%, that is, 0.84
percentage points for one more cubic metre. Since 0.84 is below the 1.0 %/m³ threshold, and
the previous gain, between 2,000 L and 3,000 L, was 1.75 %/m³, the first volume to cross the
threshold is 4,000 L, and it is the ideal volume. With the looser threshold of 3 %/m³ the ideal
volume would be 3,000 L (25.99%), and with the stricter 0.5 %/m³ it would be 5,000 L (27.24%).

Notice what happens further on. Between 6,000 L and 8,000 L the potential rises by 0.25
points, the same as in the previous interval, from 5,000 to 6,000 L, and yet the gain **per
cubic metre** halves, from 0.24 to 0.13 %/m³, because the interval spans two cubic metres. That
is why the criterion uses the gain per cubic metre, and not the gain between consecutive points
of the grid: the latter depends on the step, and the former much less.

> **The criterion is hydraulic and only hydraulic.** It ignores cost, tariff and carbon. An
> ideal volume by this criterion is not a design recommendation; it is the point at which the
> yield curve stops paying off **in water**. Section {{n:32}} deals with the choice with the
> other criteria, which often point to different volumes.

---

This is one criterion among others equally defensible, and it is worth making that explicit. A
designer who wants maximum water performance will choose the largest volume of the sweep; one
answering for a budget will choose the volume with the largest net present value; the
marginal-gain criterion lies between the two, as the one that identifies where the curve stops
paying off. The three read the same sweep and need not coincide: in this project they point to
three different volumes, and the maximum-performance one is the largest of the three. None of
the three is wrong — what is wrong is not saying which one was used. {{fig:fig09_criterios}}
marks the volume chosen by each criterion, with the value noted in the chart legend.

![The same sweep read by three criteria](../figuras/fig09_criterios.png)

*Figure 99 — Sweep of the tutorial project read by three criteria: (a) saving potential and (b) net present value of the same set of volumes. The vertical lines mark the volume chosen by marginal gain below 1 %/m³, by maximum NPV and by maximum potential; the volume of each is noted in the legend, because it depends on the swept grid and on the economic assumptions in force.*

---

## Why the program simulates: the empirical methods

Standards and handbooks have long offered a set of methods to size the tank: Rippl's, the
simulation, and several practical rules, such as the German, the British and the Australian.
They are still in common use in projects and academic work, and it is worth understanding what
each one answers before comparing them with the program's sweep. Some standards also have a
simplified method of the same kind, a number of days of the smaller of annual yield and demand,
next to the detailed daily simulation.

**Rippl's method** is the mass diagram applied to the tank: it accumulates, period by period,
the difference between demand and usable rain, and adopts as the volume the largest cumulative
deficit of the series. The resulting volume is the one that would meet **all** the demand even
in the worst dry spell on record, and so it grows with the length of the series and with its
resolution: with daily data, dry sequences appear whole; with monthly data, part of them is
diluted in the monthly mean.

**The practical methods** are rules of thumb. The German one takes 6% of the smaller of annual
usable rain and annual demand; the British one takes 5% of the product `P × A`, with `P` the mean
annual precipitation and `A` the collection area; the Australian one does a monthly balance by
trial until the desired confidence is reached. Neither of the first two uses the distribution of
rain over time, and the British one does not even use the demand.

The table below applies five sizing approaches to the New York tutorial project, rounds each
volume to a multiple of 250 L and simulates, in the program itself, the potential each one
produces.

<!-- inclui: _tabelas/cap24_metodos.md -->

The first table shows what the concave curve of section {{n:7}} already announced. The methods
that size for the worst dry spell, such as Rippl with a daily series (8,000 L), and those that
ignore demand, such as the British one (8,500 L), lead to tanks of 8 to 8.5 m³, which deliver at
most 0.95 percentage points more than the 4,000 L of the simulation (27.78% against 26.83%) at
twice the volume. The German method (3,750 L, 26.66%) and Rippl with a monthly series
(5,750 L, 27.43%) get the order of magnitude right in this case, but by coincidence: the German
method has no way of knowing how the rain is distributed, and would give the same volume for a
city with six dry months.

==The essential difference is that the empirical methods answer a fixed question, and the
simulation answers the question the designer declares.== Rippl asks which volume never fails;
the British method asks what fraction of the rain to store; the sweep with marginal gain asks
from which volume on the next cubic metre stops paying off. The right volume varies with local
rain, roof area, number of residents and demands, and sizing tanks by local tradition, without
simulation, can lead to low-efficiency systems. In the three example cities the sweep happens to
give the same ideal volume, 4,000 L, but only because the tutorial house is the same in all
three and the marginal-gain threshold is the same; change the roof, the demand or the threshold
and the volume moves.

---

## The time step and the storage fraction

The program simulates day by day, and that choice has a known range of validity. Fewkes and
Butler (2000) compared behavioural models with steps of one minute, one hour, one day and one
month, took the hourly model with the YAS rule (section {{n:23}}) as the reference, and showed
that the right step depends on a dimensionless quantity, the **storage fraction**.

```equacao:fracao_de_armazenamento
F_S = S ÷ (A × R)
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `F_S` | storage fraction | dimensionless |
| `S` | tank capacity | m³ |
| `A` | catchment area in horizontal projection | m² |
| `R` | mean annual precipitation | m |

According to those authors' results, the hourly model is the one indicated for fractions up to
0.01; the daily one, for fractions between 0.01 and 0.125; and the monthly one, only above
0.125. The physical reason is simple: the smaller the tank relative to the rain it receives, the
more it fills and overflows **within** a single rainy day, while the demand is withdrawn over the
hours; a daily step adds up in a single inflow what, hour by hour, would have come in and gone
out little by little.

The second table calculates the fraction for the volumes of the tutorial sweep. The chosen
4,000 L cistern has a fraction of 0.0237, within the range of the daily model; the 1,000 L
tank (0.0059) falls below 0.01, and for it the daily result should be read as an
approximation. Fewkes and Butler recommend the hourly step for that volume and the daily step for the others. Campisano and Modica (2015), who simulated a residential system with daily and
sub-daily steps from measured discharges, reached a complementary conclusion: the daily step is
reliable for estimating **water saving**, but steps of at most one hour are needed when the
objective is **stormwater retention**, above all in small tanks with high demand.

> **In practice.** For potable water saving in buildings, the program's daily step is adequate
> in the usual design range. If the storage fraction of your study falls below 0.01, declare the
> limitation; and if the objective is to attenuate peak flows in urban drainage, the program is
> not the right tool.

---

## What the literature says about the ideal volume

There is no single definition of ideal volume, and the systematic review by Semaan et al. (2020)
helps to place the program's criterion. Examining optimisation studies of domestic systems, the
authors observed that sizing the tank is the most important optimisation objective, but that cost
is the most used criterion; that undersizing produces systems unable to supply a reliable
volume; and that oversizing raises the investment for a small marginal benefit and may even
compromise water quality, as the water is stored for longer.

Campisano et al. (2017), in a broad review of urban rainwater harvesting systems, bring together
criteria from three families: **water efficiency**, such as saving potential and reliability;
**economic**, such as net present value and payback; and **drainage performance**, such as
retention. The program covers the first two families and declares that it does not cover the
third.

The marginal-gain criterion belongs to the first family and has an advantage over fixed
reliability, as in Rippl's: it does not require the designer to choose an acceptable failure
level, which rarely has a technical justification, but a level of diminishing return, which is
read directly in cubic metres of tank. The disadvantage is symmetrical: the 1 %/m³ threshold, or
the 5 %/m³ one, is also a choice, and must be declared.

---

## Sensitivity to the step

The ideal volume depends on the sweep step, and it is worth knowing by how much.

A coarse step jumps over the knee of the curve: with a 5,000 L step, the first point assessed
after zero already has the mean marginal gain of the whole interval, and the second may already
be below the threshold. The ideal is shifted upwards.

A fine step resolves the knee better, at the cost of time.

**Practical recommendation:** a step between 500 and 1,000 L for residential tanks, and between
2,000 and 5,000 L for large buildings, always declaring the step adopted together with the ideal
volume.

---

## Why the curve has this shape

The rainwater yield curve is concave and asymptotic, always. Two reasons:

**Small events are the majority.** The first litres of storage capture the frequent, small rains,
which account for most of the days. The last litres only serve the few extreme events.

**The suppliable fraction is a ceiling.** The potential cannot exceed the fraction of the demand
that rain supplies, defined in section {{n:5}}. The curve approaches that ceiling and never
crosses it — an invariant the test suite checks up to volumes of 100 m³.

---

## Is the series long enough?

Every result of this section depends on the rainfall series loaded, and the question the reviewer
asks first is whether it is enough. Geraldi and Ghisi answered it in three papers: sub-series
are extracted from a long series, each one is simulated, and it is counted how often they
reproduce the result of the whole series. The representative length is the shortest that
reproduces the result in most windows, and that **keeps reproducing** it at longer lengths — an
isolated hit in a short sub-series is not worth a recommendation.

The program has this analysis in the sweep step, in the «is the rainfall series long enough?»
button. It uses the same grid of volumes and the same marginal-gain threshold as the sweep,
because the answer depends on them, and it returns the verdict in one sentence, with the
frequency table by length.

==The answer belongs to this project, not to the city.== It is the point the papers do not
isolate and that the analysis makes visible: the length of series needed depends on how much of
the demand the rain is asked to supply. The larger the share to be covered, the more the cistern
depends on rare dry spells, and the longer the series that contains them must be. A short series
does not get the mean potential wrong; it gets the volume wrong, which is what is bought.

The program returns the verdict for your project, with its roof, demand and suppliable fraction.
Run it for each city of a comparison: the three example cities, with thirty years of daily data
each, are a good test. [A COMPLETAR: the representative series length for New York, London and
Cape Town has not yet been run for this edition; run the analysis on the three example projects
and tabulate it here.]

> **Warning: a short series does not become a long one by averaging.** If the analysis says the
> project needs more years than the series has, the ideal volume calculated is provisional, and
> that is what is declared in the work. Repeating the simulation with another window of the same
> data does not solve it: what is missing is record, not processing. Some standards fix a
> minimum number of years of daily data; Triton keeps the Geraldi and Ghisi analysis, which
> answers for each project instead of fixing a minimum.

---

## What the sweep does not answer

- **Which volume to buy.** Tanks exist in commercial volumes; the ideal calculated must be
  rounded to the nearest available volume, and the sweep already helps by working in multiples of
  250 L.
- **Whether the system is worth it.** That is section {{n:29}}.
- **Whether the volume fits on the plot.** The program does not know the site.
- **How much the cistern attenuates the drainage.** The daily step does not represent peak flows,
  and retention needs an hourly step or less, as Campisano and Modica (2015) show.
