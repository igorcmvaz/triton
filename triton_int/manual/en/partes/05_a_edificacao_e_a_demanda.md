# The building and the demand

> By the end of this section the program will know **how much water goes out** and,
> more importantly, **which part of it rain can supply**. That fraction is the ceiling
> of everything that follows.

Section {{n:4}} defined the supply. This one defines the demand. And there is an
asymmetry worth understanding from the start: **rain cannot supply all the demand**,
however much water there is. There is a ceiling, it is defined here, and no tank goes
beyond it.

---

## The building type

In step **2. Building & Demand**, choose *Single-family residential*. The program has
eight building types, each with its reference per capita consumption
({{fig:fig38_per_capita}}) and the usual split of end uses. Industry has no reference
range, because consumption depends on the production process, not on occupancy: in that
case, the value must come from measurement.

![The reference per capita consumption by building type](../figuras/fig38_per_capita.png)

*Figure 99 — The usual ranges of per capita consumption by building type. The width of each range is large on purpose: they are reference values for those who have not yet measured, and measurement, when it exists, always prevails.*


The building type is a starting point, not an imposition: the value remains editable.
Section {{n:18}} deals with non-residential cases, which have a trap of their own in the
tariff.

---

## The residents and the consumption

**Four residents, 150 L/person·day.** A total of **600 L/day**.

The value of 150 L/person·day is a round reference for a house with a regular supply,
not a measurement. If you have the building's water and sewage bill, use it: divide the
monthly consumption in litres by thirty and by the number of residents. The measured
number is worth more than any reference.

The program accepts a **constant** demand or one modulated by week, month or day. The
tutorial uses a constant one; section {{n:17}} shows the modulation, which matters in
schools, hotels and any building with seasonality.

---

## The fraction rain can supply

**28%.** It is the most important number in this section.

Rainwater does not go to the shower, the kitchen sink or for drinking. In a house, it
goes to the toilet, floor washing, garden watering and vehicle washing. The share of
these uses in the total consumption is the **ceiling of the saving potential**.

The split adopted in the tutorial is shown in {{fig:fig00c_fracao}}, with the uses rain
supplies marked. The toilet accounts for 20% of consumption and cleaning and watering
for 8%; shower, kitchen sink, washbasin and washing machine, which account for the
rest, stay on potable water.

Adding the two that rain supplies gives the 28% of the tutorial. It is a conservative
value for a single-family house without a large garden, and it is conservative on
purpose: it keeps to the uses that rainwater guidance most widely admits.

> **The washing machine is a choice that guidance does not settle.** National rainwater
> standards differ on laundry. Some list it among the permitted non-potable uses; others
> leave it out and ask the responsible professional to study the quality parameters and
> treatment for any use not listed. Use in the washing machine is common in the
> literature and in practice, and that is why many studies work with suppliable fractions
> larger than this tutorial's. The tutorial does **not** adopt it: the machine stays on
> potable water, and the suppliable fraction falls to the 28% of the toilet and the
> outdoor uses. A project that includes laundry must declare that choice and the quality
> criterion adopted for it, and check it against the standard that applies where the
> building stands.


![The split of consumption in a house, and the part rain can supply](../figuras/fig00c_fracao.png)

*Figure 99 — Typical split of the consumption of a house by end use. In grey, the uses that require potable water; in green, those where rainwater can be used, whose sum is the suppliable fraction and the ceiling of the saving potential: no tank, however large, saves more than this fraction.*

> **This number is the ceiling.** With a 28% suppliable fraction, the saving potential
> **never** exceeds 28%, however large the tank and however much it rains. The table of
> section {{n:7}} shows the curve approaching exactly this limit and never crossing it.
>
> Anyone who wants to go beyond 28% must change the **use**, not the tank: add a use,
> such as laundry, with a declared quality criterion, or reduce potable consumption.

### Percentage on screen, fraction in the file

The same quantity appears in two forms, and each one has its place. In every field where
you type — the fractions of the building screen, the weekly and monthly tables, the
scenario tables, the batch spreadsheet and the `--share` argument of the command line —
the fraction is a **percentage, from 0 to 100**: 28 means 28%. In the project file, in
the parameter file and in `rainwater_share` and `non_potable_indoor_share`, it is a
**fraction, from 0 to 1**: 0.28.

The split is not arbitrary. The percentage is the form in which the quantity circulates
among designers, standards and water bills, and it is the form least prone to typing
errors. The fraction is the form in which it enters the balance equation, multiplying
the indoor demand (section {{n:23}}), and it is the form that needs no conversion for
anyone reading the file with another program.

What is not allowed is mixing them. Up to this version, twelve places in the program
accepted both forms and decided by the rule «above 1 is a percentage». The rule fails
precisely on small values, where the error cannot be seen: 1 became 100%, not 1%; 0.5
typed in a percentage column became 50%. ==Now the unit is fixed by the place, and never
guessed from the value.== A percentage above 100 is refused; a fraction above 1 is
refused with the remark that it looks like a percentage. {{fig:fig46b_percentual}} shows
the three states of the field in the interface.

![The field in percentage and the suspicious-value marker](../figuras/fig46b_percentual.png)

*Figure 99 — States of the suppliable-fraction field in the interface. The field receives a percentage from 0 to 100; in the project file and in the calculation parameters the quantity is stored as a fraction from 0 to 1. A value between 0 and 1 typed in the field is flagged in orange, without blocking the calculation, because 0.4% is possible, although rare.*

> **The orange marker.** A value between 0 and 1 in a percentage field is accepted,
> because less than 1% replacement is possible, but the field turns orange and the tip
> explains what was understood. In the scenario tables and the batch spreadsheet, the
> program asks before simulating.

---

## Breaking down the uses, or not

The program accepts two levels of detail in the description of the demand, and the
choice between them depends on what the study intends to answer.

In the **simplified mode**, two things are entered: the non-potable fraction of indoor
consumption — toilets and laundry — and, if there is one, the outdoor demand in litres
per day. The **total** suppliable fraction comes from the two,

```text
f = (indoor fraction × indoor demand + outdoor demand) ÷ (indoor demand + outdoor demand)
```

and appears in a field that cannot be edited, because it is a result and not an input.
Without outdoor demand, the total is the indoor fraction itself: the 28% of this
tutorial. It is the mode adopted here and it is enough for most studies.

> **Why the total is not typed.** Up to version 1.0.0 the total-fraction field was
> editable, but the simulation used the indoor fraction; and, when a project was opened,
> the screen reset the indoor fraction to 35% and the outdoor one to zero, whatever had
> been saved. A project that declared 28% was simulated with 35%. Today the screen
> restores both, the total is calculated, and an old file whose fractions disagree is
> opened with the total it declares, with a warning.

In the **detailed mode**, the demand is split into three parts: the indoor potable,
which rain never supplies; the indoor non-potable, which is the system's priority; and
irrigation, supplied last. The split changes two things. It changes the order of supply
on days of scarcity, when indoor use takes precedence over the garden; and it makes it
possible to distinguish indoor from outdoor use in certification credits, a distinction
LEED requires in separate credits, as section {{n:31}} describes.

It is worth breaking down the uses when there is a garden of significant area, when
certification is on the project's horizon, or when irrigation can be suppressed on rainy
days — a situation the next item deals with.

---

## Irrigation and suppression by rain

Once an irrigation volume is declared, the program offers a rain suppression threshold:
on days when the precipitation exceeds that threshold, the garden is not watered. The
behaviour reproduces that of any irrigation controller with a rain sensor, a common and
cheap piece of equipment, and ignoring it would overestimate the outdoor demand over the
whole year. The default threshold is 2 mm per day.

> **The rainfall series is read twice.** One reading is converted into collected volume,
> after the first flush. The other decides whether the garden is watered. The two are
> independent: a day can suppress irrigation **and** yield collection.

One choice remains that deserves particular attention, because it changes the economic
result and is not neutral: the **backup supply** of irrigation. With it on, the mains
waters the garden on the dry days when the cistern cannot cope, and that volume enters
the water and sewage bill as potable consumption. With it off, the garden is simply not
watered on that day, the building does not buy that water, and the corresponding volume
appears in the balance as *unmet demand* — the third part dealt with in section
{{n:23}}.

==The distinction between the two settings is conceptual before it is numerical.== A
garden that must be watered every day represents a real demand, which someone will pay
for; a garden that accepts not being watered on a dry day represents a convenience, and
treating it as demand inflates both the consumption and the apparent saving of the
system.

---

## What we have so far

<!-- tabela: State of the tutorial project at the end of defining the demand -->
| Item | Value |
| :--- | ---: |
| building type | single-family residential |
| residents | 4 |
| per capita consumption | 150 L/person·day |
| total demand | 600 L/day |
| fraction suppliable by rain | 28% |
| **rainwater demand** | **168 L/day** |

The program now knows the supply and the demand. Before simulating, a comparison worth
keeping:

<!-- tabela: Comparison between the annual rainwater supply and the suppliable demand -->
| | m³/year |
| :--- | ---: |
| gross rainwater supply (precipitation × area × coefficient) | 143 |
| **rainwater demand of the year** | **61** |

Supply exceeds demand: the gross volume is **2.3 times** what is intended to be
used, before the first flush is deducted. If supply were the only limit, the system would meet 100% of the rainwater demand
and reach the 28% ceiling.

It does not, and section {{n:6}} shows why.
