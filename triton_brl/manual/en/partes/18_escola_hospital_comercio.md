# Simulating schools, hospitals and shops

> **Question this guide answers:** does the program work for non-residential buildings?

It does, and it works well for the water side. There is, however, a weighty caveat about
the economic side, and it must be known before the study starts, not after it is finished.

---

## The caveat: the tariff category

Brazilian utilities charge different tariffs depending on the consumer category —
residential, commercial, industrial and public —, and the non-residential categories usually
cost twice the residential one or more. In the CASAN table in force in April 2026, for
example, the first block costs R$ 3.08/m³ for a house and R$ 6.81/m³ for a commercial
establishment.

==These tables exist and are public:== they are in the resolutions of the regulatory agencies
and on the utilities' own websites. What the program's catalogue records, for the 652
municipalities, is the residential category of each one, because surveying the four
categories of every provider would be a job of another order of magnitude. ==The
non-residential tariff is not missing from the program: it is missing from the catalogue,
and you can enter it.==

When you choose a non-residential building type, the Brazil Edition **warns** you and says
in which direction the error goes:

> The building type chosen is «School», which the utility bills in the Public category. The
> program's catalogue has only the Residential category, so the water and sewage bill is
> being calculated with the wrong tariff. The error has a known direction: non-residential
> categories are more expensive, and therefore the saving and the return are
> **underestimated**.

> **What to do, in five minutes.** Look up your utility's current tariff resolution, which
> is usually on its website under «tariffs» or «tariff structure». Find the table of the
> category of interest. Enter the blocks in the custom mode of step **12. Tariff Manager**,
> with the corresponding minimum-charge regime. Section {{n:16}} describes each field. Once
> that is done, the economic result becomes that of your case, and not a residential
> approximation.

In the International Edition there is no catalogue: the tariff is always typed in, and so
the program does not show this warning. Enter directly the tariff of the category the
building is billed in.

There is a consolation in this limitation, and it is methodological: ==the error has a known
direction and it is conservative.== Non-residential categories are more expensive than the
residential one, so the real project returns more than the program indicates, and never less.
A study that declares the limitation therefore presents a feasibility floor — which is a
defensible position, unlike the reverse.

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

**School.** It is one of the most favourable cases for rainwater harvesting in Brazil, for
two reasons that add up. The non-potable share of consumption is high, because the toilet
dominates use and many units have neither showers nor a kitchen. And the roof area per pupil
is usually large, so supply is rarely the limiting factor.

Modulation by calendar, however, has an effect that depends on the region, and it is better
to simulate it than to assume the result. In the Brazilian Southeast and Centre-West, the
rains concentrate from October to March and the dry season runs from June to August. The July
break coincides with the dry season, and the cistern gets through the dry period without
being drawn on; the long holidays from December to February, on the contrary, coincide with
the peak of the rains, and during that period the cistern fills and overflows unused. In the
South, where rain is better distributed over the year, the school calendar weighs less.
Section {{n:17}} shows how to represent the school days, and section {{n:14}} shows how the
distribution of rain changes from one state capital to another.

**Hospital.** The most delicate case. High, continuous consumption, without relevant
seasonality, which is good for harvesting. But the **quality requirement** is different:
there are uses that do not admit rainwater under any circumstances, and the cooling tower,
which would be an ideal use, requires microbiological control against Legionella. Treat the
quality class with care, and do not use the adapted classes 2 to 4 as if they were a
normative requirement.

**Office and shop.** Demand concentrated on working days, five days out of seven. Modulate by
week. The non-potable share is high because almost all consumption is toilets, urinals and
cleaning: Proença and Ghisi (2010), who estimated the end uses of ten office buildings in
Florianópolis through interviews with the occupants and flow measurements, found 56% to 86%
of consumption in non-potable uses, and concluded that the toilet should be the first target
of any saving programme in these buildings. The width of the range is itself a warning: two
offices in the same city can differ by thirty percentage points, and the suppliable fraction
of a study should come from the building studied whenever possible.

**Hotel.** Strong seasonality, and the case in which monthly modulation matters most. See the
warning of section {{n:17}} about concentrated demand: a coastal hotel fills up precisely in
the wettest months and still yields less than a constant demand, because it empties the tank
in a few days and leaves it idle for the rest of the year.

---

## Where to get the non-potable fraction from

The suppliable fraction is the ceiling of the saving potential, as section {{n:25}} shows,
and it is therefore the parameter that weighs most on the result of a non-residential
building. There are three ways of obtaining it, in decreasing order of reliability.

**Measuring the end uses.** Sub-meters or flow loggers on the branches, for a few
representative weeks. It is the only way that produces a number for the building, and not an
average.

**Survey by interview and flow.** The method of Proença and Ghisi (2010): ask the occupants
the frequency and duration of each use and multiply by the measured flows of the fixtures. It
costs little and captures the real behaviour of the building, but it depends on the memory of
those interviewed.

**Reference value from the literature.** Acceptable in a preliminary study, as long as the
reference is of the same building type, from the same country and, ideally, from the same
region. Avoid transposing residential fractions to other building types, and even among
dwellings the variation is large: in a multi-family residential building in Florianópolis,
Maykot and Ghisi (2020) found the toilet with only 9.2% of consumption and the washing
machine with 21.3%, far below the fractions of offices and schools.

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
- whether the **tariff category** was corrected or remained the residential one of the
  catalogue, and in the latter case that the economic result is underestimated;
- the **modulation profile** and its origin;
- for a hospital, the quality class adopted and what it covers.
