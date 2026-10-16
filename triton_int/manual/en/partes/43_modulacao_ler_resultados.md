# How to read the results

> **Question this section answers:** what does each table and each figure say, and what
> should be declared in a report or a paper?

The example in this section is the New York tutorial project, saved with the tool already set up in the
file `09_modulation_tutorial.triton` (appendix J), with six variables drawn: the three
consumption ones, the rainfall factor, the tariff factor and the investment factor, with the
screening distributions, in a thousand realisations and seed 42. The numbers in the tables
are those the program computes; running the tool with the same project and the same seed
reproduces them.

## What went in

The first table on the screen states what was actually drawn: the study value, the declared
distribution and the sample statistics. It is the first to read, because it confirms that
the distributions produced what was intended — the sample mean should be close to the
declared mean, and the interval between P5 and P95 should be plausible for the building.

<!-- inclui: _tabelas/cap43_entradas.md -->

## The result at the chosen volume

The second table summarises the volume the study chose — the TOPSIS winner of the base case
— comparing the deterministic study with the mean, standard deviation, coefficient of
variation and percentiles of the realisations.

<!-- inclui: _tabelas/cap43_referencia.md -->

Two readings matter. The first is the **width**: the interval between P5 and P95 contains
90% of the realisations and is the number that should accompany the published result. The
second is the **position of the deterministic study** relative to the median. When the median
falls below the base case, the non-linearities of the system — the progressive tariff, the
minimum charge, the overflowing cistern — make unfavourable realisations weigh more than
favourable ones, and the base case is optimistic.

The discounted payback only exists when the investment pays back; the table computes it over
the realisations in which that happens, and the screen states how many there were.

<!-- inclui: _tabelas/cap43_probabilidades.md -->

The probability that the investment pays back is the proportion of realisations with a
positive net present value. The 95% confidence interval beside it is Wilson's (1927), suited
to small samples and to proportions close to 0% or 100%. It measures the uncertainty of the
**sampling**, not that of the assumptions: with more realisations it narrows; the probability
itself does not.

## The bands by volume

The following figures show the band between the 5th and 95th percentiles, the median and the
deterministic study across all volumes. The dotted line marks the chosen volume, and the
values written are its own.

![Potable water savings by volume in the tutorial example](../figuras/fig52_modulacao_economia.png)

*Figure 99 — Potable water savings by lower-tank volume in the tutorial example: band between the 5th and 95th percentiles of the realisations, median and deterministic study. The marked values are those of the volume chosen by the study (dotted line).*

![Net present value by volume in the tutorial example](../figuras/fig53_modulacao_vpl.png)

*Figure 99 — Net present value by lower-tank volume in the same example. A band that crosses zero at every volume indicates that none of them pays back with certainty; a median below the deterministic study, that the base case is optimistic.*

## The stability of the choice

The frequency table and figure count, in each realisation, which volume would be the
technical ideal, which would be the economic optimum — the one with the shortest discounted
payback, the program's criterion (section {{n:12}}) — and which would win TOPSIS. A
realisation in which no volume pays back appears as «none pays back» in the economic column.

<!-- inclui: _tabelas/cap43_frequencia.md -->

![The frequency with which each volume is chosen in the tutorial example](../figuras/fig54_modulacao_frequencia.png)

*Figure 99 — Frequency, as a percentage of the realisations, with which each volume is the technical ideal, the economic optimum and the TOPSIS winner in the tutorial example.*

The reading is the same as that of the SMAA-VIKOR acceptability (section {{n:32}}): a volume
that wins in most realisations is a robust recommendation; one that wins in a minority, next
to neighbours with similar frequencies, is a preference that depends on the assumptions, and
the text must say so.

## What weighs most

Sensitivity is measured by Spearman's (1904) rank correlation between each drawn variable
and the result at the chosen volume. The coefficient ρ ranges from −1 to 1: the sign gives
the direction of the effect and the magnitude its strength. Because it uses ranks rather than
values, it captures non-linear monotonic relations — such as that of the progressive tariff —
and is not distorted by extreme realisations.

<!-- inclui: _tabelas/cap43_sensibilidade.md -->

![The sensitivity at the chosen volume in the tutorial example](../figuras/fig55_modulacao_sensibilidade.png)

*Figure 99 — Spearman rank correlation of each drawn variable with potable water savings and with the net present value at the volume chosen by the tutorial study, from the largest to the smallest influence on the net present value.*

Rank correlation can show an effect that one-at-a-time analysis hides. The non-potable fraction
defines the demand that rainwater can supply, so it is the natural candidate to move the
**percentage** saving most. The number of occupants and the per capita consumption raise total
consumption: they tend to move the percentage little, and in the opposite direction, but they can
move the net present value a great deal, because more consumption pushes the bill into the
dearer bands of a progressive tariff and every cubic metre saved becomes worth more. Read the
table for your own case, and check which of these effects the tariff you typed in allows.

## How much of the uncertainty comes from each source

ρ gives the direction and strength of a monotonic relation, but not what share of the
uncertainty of the result comes from each variable. That share is the correlation ratio,
η²: the variance of the means of the result between classes of the variable, divided by the
total variance. Continuous variables are grouped in deciles, the number of occupants and
the climate model by their own values. η² estimates the first-order sensitivity index
(Saltelli et al., 2008), ranges from 0 to 1 and also captures non-monotonic relations.

<!-- inclui: _tabelas/cap43_variancia.md -->

In the example, compare the columns: the variables that dominate the variance of the savings are
rarely those that dominate the variance of the net present value, and factors drawn with narrow
screening widths, such as the tariff, investment and rainfall factors, usually weigh little. With independent variables and additive effects,
the sum is close to 1; a sum well below 1 indicates interaction between the variables. The
class-based estimate has a small upward bias, of the order of the number of classes divided
by the number of realisations, so the sum may slightly exceed 1.

## Catchment and rainfall

The second example, saved in the file `10_modulation_catchment.triton`, uses the same New York
sweep but draws the uncertainty of the **catchment** — area, runoff coefficient and first-flush
depth — together with the rainfall factor, the tariff factor and the investment factor, in a
thousand realisations and seed 42. The International Edition has no per-model table, because it has
no climate-model database: rainfall uncertainty enters through the rainfall factor, and the
variance table lists the drawn variables, the rainfall factor among them.

Read this example for what it separates. A runoff coefficient or an area off by a few per cent
changes every day of the series by the same proportion, so these variables shift the savings
roughly in step with the rainfall factor; a deeper first flush acts mainly on small rains, which
are the days that fill an empty tank. The η² table shows which of them the savings and the net
present value actually respond to.

## What to declare

In a report or a paper, declare: the drawn variables and their distributions (the first
table), the number of realisations and the seed, the P5–P95 band and the median of the result
at the chosen volume, the probability that the investment pays back with its interval, the
frequency with which the chosen volume wins and the share of variance each source explains.
The **Export** button writes all of this to
JSON, and the CSV of the samples allows any statistic to be recomputed outside the program.
