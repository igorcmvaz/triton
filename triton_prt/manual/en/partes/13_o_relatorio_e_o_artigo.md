# The report, and what to declare in a paper

> By the end of this section you will have the report issued and, if you intend to
> publish, the list of what must appear in the method of the paper. That list is the
> shortest and the most important part of the manual.

---

## The three reports

The program issues three different reports, and the difference is not one of length but
of audience and purpose. Choosing the wrong report for the right reader is the most
common way of producing a document nobody reads: a client does not go through a life
cycle inventory item by item, and a certification assessor is not satisfied with a
four-page conclusion.

The **executive report** takes four to six pages and brings together the technical
result, the investment, the return and an objective conclusion. It is the document handed
to the client, and its virtue is that it fits in a single reading, without requiring the
reader to know the method.

The **environmental and ESG report** presents the life cycle inventory broken down by
component, the carbon balance over the service life and how the project fits the five
frameworks dealt with in section {{n:31}} — LEED, AQUA-HQE, Selo Casa Azul, EDGE and GRI
303 (in the International Edition, LEED, EDGE and GRI 303). It is the document attached to
a certification process, and the breakdown by component exists precisely because an
assessor checks item by item.

The **research report** has the complete method, the declared assumptions, the series used
and the results with the precision a paper requires. It is the basis on which a
publication is written, and it is the only one of the three that includes the analytical
figures.

Besides the three, step **10. Export** generates the schematic drawing in DXF, the BIM
model in JSON and spreadsheets with the complete daily series and with the volume sweep,
as section {{n:22}} details.

---

## What the report does not decide for you

==The report carries the numbers; the context that makes them reproducible is yours.==
No automatically generated document can declare why that precipitation series was chosen,
whether the per capita consumption adopted was measured or taken from the literature, or
what justifies the service life considered in the environmental assessment. It is that
information that allows a third party to repeat the study and reach the same result, and
it is what the rest of this section deals with.

---

## The declaration list

A study carried out in Triton that fails to declare any of the items below is not
reproducible by third parties and, which is usually worse, is not comparable with another
study done in the same program — because two simulations with different assumptions
produce numbers that look comparable and are not. The list is organised in the order in
which the decisions appear in the work, and can be followed as a script for writing the
method.

### Program and version

- **Triton version**, with the full number, and the **edition** (Brazil or
  International). Calculation fixes between versions shift results, and without the
  declared version there is no way of knowing which calculation produced the published
  number.

### Precipitation series

- **Source**: station, national database, or climate model.
- If the national database: **model, scenario and time window**.
- **Trimming**: start and end dates, and number of years.
- **Treatment of gaps** and the criterion for dropping an incomplete year.

### Building and demand

- Catchment area and **how it was obtained** — horizontal projection.
- Runoff coefficient and its origin.
- Per capita consumption and whether it is **measured or a reference value**.
- **Fraction suppliable by rainwater** and the end uses that make it up. It is the
  ceiling of the result, and without it the potential cannot be interpreted.
- Whether any use is outside the list of item 4.1.7 of ABNT NBR 15527:2019, such as the
  washing machine, and which quality criterion was adopted for it.

### Supply arrangement

- **Arrangement**: pumping to an upper tank, direct pressurisation or gravity. It defines
  the energy and the pump sets in the cost and in the carbon.
- With pumping to a tank: tank volume, trigger level and manometric head.
- With direct pressurisation: working pressure and starts per person per day.

### First flush

- Depth adopted and **mode** among the three.
- **The divergence from Netuno 4**, if the study compares the versions: Netuno 4 treats
  the depth as an event threshold, Triton subtracts it, and the difference is worth 2.3
  to 2.7 percentage points of saving over 4,050 reference cases.

### Volume and choice criterion

- If it came from a sweep: **the marginal-gain threshold adopted**. Without it, «ideal
  volume» means nothing.
- If it came from multi-criteria: **the weights of the seven criteria** and the method,
  TOPSIS or SMAA-VIKOR.
- That the TOPSIS normalisation is a **variant** with a shift by `x − min(x)`.

### Economic analysis

- **Municipality and utility**, with the effective date of the tariff table.
- **Minimum-charge regime** among the six. It is what changes results most between
  municipalities.
- Sewage percentage, and that it applies to the **water part** of the bill.
- Minimum attractive rate of return, inflation, analysis period.
- **Tariff escalations** for water, sewage and energy, with the interval.

### Life cycle assessment

- **Boundary**: water delivered, not produced.
- **Service life** adopted and its justification.
- **Material** of the tank. It reverses the sign of the result, as section {{n:11}}
  shows.
- Basis of the electricity grid emission factor, **with the year**.
- Which factors are **approximations** and which carry a **screening label**.

### Certifications

- That quality classes 2 to 4 are **adaptations made by the program**, not by NBR 15527.
- For LEED, the **version** of the framework: v4/v4.1 or v5.
- For EDGE, that the program assesses **only the water bar**, and that the base case used
  is the declared one or the modelled demand.

---

## The ready-made paragraph

For our project, the method would read like this:

> The simulation was carried out in Triton 1.0.0, Brazil Edition, with a daily-step
> behavioural model (overflow calculated before the demand is withdrawn, with the day's
> rain available for the day's consumption, an order between YAS and YBS), on a
> 30-year precipitation series for Florianópolis (10,950 days, mean of 1,795 mm/year). A
> catchment area of 150 m² in horizontal projection was adopted, with a runoff
> coefficient of 0.85, taken from the collection efficiency η that ABNT NBR 15527:2019
> recommends in item 4.1.6, and a 2.0 mm first flush on every event, subtracted from the
> daily depth — a deliberate divergence from Netuno 4, which treats the value as an event
> threshold. The total demand adopted was 600 L/day (4 residents, 150 L/person·day), with
> a fraction suppliable by rainwater of 28%, corresponding to the toilet and the outdoor
> uses, within the list of item 4.1.7 of ABNT NBR 15527:2019. The 4,000 L volume resulted
> from the marginal-gain criterion with a 1 %/m³ threshold and was confirmed by a TOPSIS
> multi-criteria analysis with seven criteria and equal weights across the technical,
> economic and environmental dimensions, with normalisation in a variant of Hwang and Yoon
> shifted by x − min(x). The points of use are supplied by pumping to a 1,000 L upper tank,
> with a 100 L trigger level, a 0.5 hp pump, a manometric head of 12 m and the motor
> efficiency of Table 13 of ABNT NBR 17094-2. The economic analysis used the CASAN tariff
> structure in force since 01/04/2026, an availability-charge regime, sewage at 100% of the
> water value, a minimum attractive rate of return of 0.5% per month, inflation of 0.35%
> per month, escalations of 5% per year at 12-month intervals and a 20-year period. The
> life cycle assessment adopted the boundary of water delivered, a polyethylene tank and a
> service life of 20 years.

That is about two hundred and fifty words, and they are the difference between a study
another researcher can repeat and a loose number nobody can check. The length is modest
compared with what is gained: a method written this way answers in advance most of the
questions a reviewer would ask.

---

## The end of the tutorial

Ten sections, a single project followed from start to finish, and a complete study: it
started from a house without a system and arrived at a recommendation of volume, material,
quality class and economic and environmental feasibility, with each decision justified by
the number that supported it. The table of section {{n:12}} brings together the
consolidated result.

The way forward depends on what you intend to do next:

- **Solve a case different from the tutorial** — chapter {{c:3}}, the task guides.
- **Understand where each number comes from** — chapter {{c:4}}, the method.
- **Not make the mistakes the program does not prevent** — section {{n:33}}.
- **Defend the study before a reviewer** — chapter {{c:6}}.
