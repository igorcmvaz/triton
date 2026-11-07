# Simulating schools, hospitals and shops

> **Question this guide answers:** does the program work for non-residential buildings?

It does, and it works well for the water side. There is, however, a weighty caveat about
the economic side, and it must be known before the study starts, not after it is finished.

---

## The caveat: the tariff category

Utilities charge different tariffs depending on the consumer category (residential,
commercial, industrial, public), and the non-residential categories often cost more than the
residential one. The program has no catalogue of tariffs: the tariff is always typed in.
Enter directly the tariff of the category the building is billed in. The three example
projects carry a **residential** tariff, so they are right for a house and would be the wrong
tariff for a school, a hotel or a shop.

> **What to do, in five minutes.** Look up your utility's current tariff document, which is
> usually on its website under «charges» or «tariffs». Find the table of the category of
> interest. Enter the blocks in the custom mode of the tariff screen, with the corresponding
> minimum-charge regime. Section {{n:16}} describes each field. Once that is done, the economic
> result becomes that of your case, and not a residential approximation.

The two non-residential cases of the manual, the London school and the Cape Town hotel, keep
the residential tariff of their city and leave the costs at zero: they compare rainfall and
demand, not money. Take their percentages as water results, and do not read an economic
conclusion into them.

Declare which category the tariff belongs to. A study that applies a residential tariff to a
non-residential building states a limitation, and the direction of the error is usually
conservative, because non-residential categories tend to be dearer; but that is a property of
the tariff document, and you must check it in yours.

---

## The available building types

The program's eight building types are grouped by the tariff category the utility bills them
in, and each one has its own unit of consumption ({{fig:fig39_tipologias}}). The unit of
consumption changes the meaning of the per capita value entered, and the category decides the
block structure of the bill: simulating a school with a residential tariff is one of the
mistakes described in section {{n:33}}.



![The building types, the tariff category and the unit of consumption of each one](../figuras/fig39_tipologias.png)

*Figure 99 — The eight available building types, grouped by the tariff category the utility charges. The unit of consumption changes with the building type, and it is what gives meaning to the per capita value entered.*


---

## What changes with each building type

**School.** It is a favourable case for rainwater harvesting for two reasons that add up. The
non-potable share of consumption is high, because the toilet dominates use and many units have
neither showers nor a kitchen. And the roof area per pupil is usually large, so supply is rarely
the limiting factor.

Modulation by calendar, however, has an effect that depends on the climate, and it is better to
simulate it than to assume the result. The manual's school is in London: 1,200 m² of roof, 300
pupils, 40 L per pupil per day, 70% suppliable, a demand modulated by day of the week (40 L on
five days, 20 L and 5 L on the weekend days) and a 30,000 L tank. It yields 12.58%, against
12.63% for a constant demand of the same annual total (a mean of 9,014.3 L/day). The weekly
rhythm alone changes almost nothing, because London rain is spread through the year and the
tank refills during the weekend. A school that closes in a dry season would behave differently,
and the monthly profile of section {{n:17}} is the tool for that case; the manual has no
monthly school profile to quote. Section {{n:14}} shows how the distribution of rain changes
from one city to another.

**Hospital.** The most delicate case. High, continuous consumption, without relevant
seasonality, which is good for harvesting. But the **quality requirement** is different:
there are uses that do not admit rainwater under any circumstances, and the cooling tower,
which would be an ideal use, requires microbiological control against Legionella. Treat the
quality class with care, and do not use the program's classes 2 to 4 as if they were a
normative requirement: they are criteria adopted by the program, and the requirement of the
case is set by the health authority and the applicable standard.

**Office and shop.** Demand concentrated on working days, five days out of seven. Modulate by
week. The non-potable share is high because almost all consumption is toilets, urinals and
cleaning. The suppliable fraction varies a great deal between offices, even within one city, and
it should come from the building studied whenever possible: measure it, or survey it as
described below, before taking a value from a reference.

**Hotel.** Strong seasonality, and the case in which monthly modulation matters most. See the
Cape Town hotel of section {{n:17}}: with occupancy concentrated in the dry summer, it yields
9.83% against 10.97% for the same annual demand spread evenly, a loss of 1.14 percentage
points. A concentrated demand wastes tank capacity, and the loss is larger when the
concentration falls in the dry season.

---

## Where to get the non-potable fraction from

The suppliable fraction is the ceiling of the saving potential, as section {{n:25}} shows,
and it is therefore the parameter that weighs most on the result of a non-residential
building. There are three ways of obtaining it, in decreasing order of reliability.

**Measuring the end uses.** Sub-meters or flow loggers on the branches, for a few
representative weeks. It is the only way that produces a number for the building, and not an
average.

**Survey by interview and flow.** Ask the occupants
the frequency and duration of each use and multiply by the measured flows of the fixtures. It
costs little and captures the real behaviour of the building, but it depends on the memory of
those interviewed.

**Reference value from the literature.** Acceptable in a preliminary study, as long as the
reference is of the same building type, from the same country and, ideally, from the same
region. Avoid transposing residential fractions to other building types, and even among
dwellings the variation is large, and the toilet share of a household differs a lot from that
of an office or a school.

> **Declare the route.** «Suppliable fraction of 60%, measured» and «suppliable fraction of
> 60%, from a reference» are different studies, and the reader needs to know which of the
> two they are reading.

---

## Individual metering and the number of dwelling units

In a multi-family building with individual metering, enter the **number of dwelling units**.
The program evaluates consumption at the level of **one** unit and multiplies by the number
of units.

This matters because of the progressive blocks: a building of twenty apartments with
individual metering pays twenty bills in the first block, not one bill that adds up all the
consumption and falls in the most expensive block. Treating the building as a single unit
would grossly overestimate the saving.

---

## What to declare

Besides what section {{n:13}} already asks for:

- the **building type** and the unit of consumption adopted;
- the **origin** of the per capita consumption — measurement, reference or standard;
- the **tariff category** entered, and whether it is the one the building is billed in;
- the **modulation profile** and its origin;
- for a hospital, the quality class adopted and what it covers.
