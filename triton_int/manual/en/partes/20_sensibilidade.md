# Sensitivity analysis

> **Question this guide answers:** which assumption moves my result the most, and how
> much can it take?

Every rainwater harvesting study rests on uncertain assumptions, and the three most
influential are usually precisely the least verifiable: will the tariff really rise 5% a
year for twenty years? Is the demand really 150 litres per person per day? Will the cistern
cost what the quotation says?

Sensitivity analysis measures how much of these doubts reaches the final result. ==It does
not remove the uncertainty, and does not try to; it measures the size of the uncertainty,==
which is exactly the information the reader needs to decide how far to trust the number
presented.

---

## The procedure, in three steps

The procedure needs no specialised tool, and it is the same as in any engineering analysis
faced with a poorly known parameter: vary one thing at a time and observe the effect.

1. **Choose the assumption** you suspect is the most influential.
2. **Run the project three times**: with the likely value, a low value and a high one.
3. **Note the result of the three** and compare.

Repeat the procedure for each doubtful assumption. In the end you will have identified
which of them actually move the result and which are irrelevant — and that separation is
worth more than any refinement of the central value, because it shows where to invest
data-collection effort. Section {{n:19}} shows how to organise the files so that the set of
runs does not turn into confusion.

---

## Which range to adopt for each assumption

The range of variation to adopt for each assumption is not a matter of guesswork: it
follows from what is known about the origin of the data, and a measured value admits a much
narrower range than a value taken from the literature ({{fig:fig41_premissas}}). The tariff
escalation is expressed in percentage points per year; the other ranges, as a percentage of
the value adopted.

![The plausible range of variation of each assumption](../figuras/fig41_premissas.png)

*Figure 99 — Plausible range of variation of each assumption in a sensitivity analysis, with the origin of the uncertainty. The widest ranges correspond to assumptions taken from a reference, not measured in the project.*


> **Do not perturb what you know.** If the area was measured in a survey, the range is
> narrow; widening it produces an artificial uncertainty that dilutes the result and hides
> the assumption that really matters.

---

## The assumptions that dominate the economic result

In economic studies of rainwater harvesting, the assumptions that move the result most are
those that act over the whole analysis horizon: the analysis period itself, the volume of
rainwater actually consumed, the minimum attractive rate of return and the **tariff
escalation**. The escalation deserves particular attention because it is the least
verifiable and it compounds: five per cent a year for twenty years multiplies the tariff by
2.65; three per cent, by 1.81; and seven per cent, by 3.87. The saving of the last years
follows that factor, and the choice of escalation rate can decide a good part of the
study's economic conclusion.

Try it on your case: in step **6. Economic Results**, change the annual escalation to 3%,
note the NPV, repeat with 5% and with 7%. Three runs, three minutes, and a range instead of a
number.

> **In a paper, show that range.** A single net present value, calculated with a 5% annual
> escalation and presented without sensitivity, suggests a precision the assumption does
> not have.

### The tutorial, assumption by assumption

The table below applies the procedure to the final tutorial project, in New York: 4,000 L in
polyethylene, pumping to a 1,000 L tank, with the illustrative costs of the manual (illustrative,
not market prices). The likely net present value is negative, about −US$ 3,020. The table varies
five assumptions, one at a time, between a low and a high value.

<!-- inclui: _tabelas/cap20_sensibilidade.md -->

The first thing to read is what does **not** happen: no assumption, at the low or at the high
value, makes the net present value positive, and none produces a payback. With the New York
tariff and these costs, the tutorial system does not pay for itself within twenty years, and no
single doubt in the inputs changes that. The reason is the price of water, which is low relative
to the cost of the works; it is not a defect of the example. Read the rest of the table with this
in mind: the question is not which assumption makes the project viable, but which one moves the
result most.

**The one that moves it most is the suppliable fraction.** From 20% to 40%, the potential goes
from 19.84% to 35.26% and the net present value from −US$ 4,289 to −US$ 1,590, the widest range
of the five. It is the assumption section {{n:5}} fixed and that depends on the decision about
uses, not on measurement: including or not the washing machine, against the quality criterion
applicable to the case, moves the result more than any economic parameter.

**Those decided by the market and the household weigh next.** The tariff escalation moves the net
present value from −US$ 3,760 (1% a year) to −US$ 2,093 (5% a year), and the minimum attractive
rate of return from −US$ 2,149 (0.2% a month) to −US$ 3,659 (0.6% a month); neither touches the
potential. Per capita consumption moves both: from 120 to 180 L per person per day, the
potential falls from 27.64% to 26.09% while the net present value rises from −US$ 3,892 to
−US$ 2,282. With more consumption the suppliable fraction applies to a larger demand, the
cistern runs short more often, the potential falls a little, and the saving in money rises.

**The one that seemed important hardly weighs.** Between 70% and 130% of the cistern price, the
net present value goes from −US$ 2,330 to −US$ 3,710, a range smaller than the others. The
polyethylene cistern is a small share of the investment, and labour, piping and accessories,
which do not vary with the volume, dominate the account.

The result reverses the intuition of anyone who prices before simulating: spending time
quoting the cistern is worth less than spending time defining the uses.

---

## The sensitivity the program does by itself

There is one case in which the sensitivity analysis comes ready and needs no additional
runs, and it concerns the final decision of the study: the choice of volume as a function
of the weights given to the criteria.

In step **8. Multi-Criteria Decision**, the **SMAA-VIKOR acceptability** column is already a
ready-made sensitivity analysis. It answers: if the weights were drawn at random instead of
fixed, with each dimension weighing 25% on average, how often would each volume come first?

Read it like this:

<!-- tabela: Reading the SMAA-VIKOR acceptability of the winning volume -->
| Acceptability of the winning volume | What it means |
| :--- | :--- |
| above 70% | robust recommendation; the weights hardly matter |
| between 40 and 70% | reasonable recommendation, and it is worth declaring the second option |
| below 40% | the choice depends on the weights, and the text must say so |

The distinction this column allows is epistemological, not only statistical: a volume that
wins in 80% of the weight draws is a recommendation, whereas a volume that wins in 30% is a
preference of the analyst, legitimate as long as it is presented as such. In the New York
tutorial the most accepted volume, 2,000 L, comes first in 39.6% of the draws, with 3,000 L second at
25.8% and 4,000 L third at 17.7%: below 40%, so the choice depends on the weights, and the text must
say so. Section {{n:32}} sets out the method that produces these numbers.

---

The tornado chart ({{fig:fig24_tornado}}) is the established way of presenting this set: one
bar per assumption, ordered by range, with the two variations in different colours. Read
from top to bottom, it answers the question the reviewer will ask first, which is on which
assumption the result depends.

![The sensitivity tornado of the tutorial project](../figuras/fig24_tornado.png)

*Figure 41 — The variation of the net present value when each assumption is changed by 30% up and down, keeping the others. The colour identifies the variation applied, not the sign of the effect: that is what makes it possible to see that raising the minimum attractive rate lowers the present value, whereas raising the tariff increases it. The base case of this figure comes from the program's simplified economic model, which discounts an annual flow with a single marginal tariff and the declared escalation; that is why the base-case present value does not match that of the tutorial's monthly cash flow. What the tornado measures is the relative sensitivity, not the absolute value.*

---

## How to present it

Three ways, from the simplest to the most complete:

**Scenario table.** Pessimistic, likely and optimistic, with the assumptions of each one
declared. Simple, honest and enough for most work.

**Tornado chart.** One bar per assumption, showing how much the result varies when it varies
alone. It ranks the assumptions by importance and is the most informative presentation per
area of page.

**Distribution.** The full range of the result, when all the assumptions vary together. It
requires declaring the distributions adopted, not just the ranges.

> **In depth: propagation by Monte Carlo.** The third way is done by drawing thousands of
> combinations of assumptions and accumulating the distribution of the result. The program
> does this propagation with the `uncertainty` subcommand of the command line, described in
> section {{n:19}}. For a course or design study, the scenario table of the first item
> answers the same question with a fraction of the effort — and it is easier to defend,
> because each scenario has assumptions that can be read.

---

## What to declare

- the **ranges** adopted and the origin of each one;
- how many runs were made, and with which values;
- for the choice of volume, the **choice band** with its tolerance and the **acceptability** of the most accepted volume;
- **which assumptions were not perturbed**, and why.

The last is the one most often forgotten, and the one a reviewer most often asks for.
