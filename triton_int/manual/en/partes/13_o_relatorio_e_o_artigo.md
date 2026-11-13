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
component, the carbon balance over the service life and how the project fits the
frameworks dealt with in section {{n:31}} — LEED, EDGE and GRI 303. It is the document attached to
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

- **Triton version**, with the full number, and the **edition** (International).
  Calculation fixes between versions shift results, and without the
  declared version there is no way of knowing which calculation produced the published
  number.

### Precipitation series

- **Source**: station, reanalysis, or climate model.
- If a reanalysis or a model: **product, scenario and time window**, and the grid
  resolution.
- **Trimming**: start and end dates, and number of years.
- **Treatment of gaps** and the criterion for dropping an incomplete year.

### Building and demand

- Catchment area and **how it was obtained** — horizontal projection.
- Runoff coefficient and its origin.
- Per capita consumption and whether it is **measured or a reference value**.
- **Fraction suppliable by rainwater** and the end uses that make it up. It is the
  ceiling of the result, and without it the potential cannot be interpreted.
- Whether any use is outside the list that the applicable national standard admits, such
  as the washing machine, and which quality criterion was adopted for it.

### Supply arrangement

- **Arrangement**: pumping to an upper tank, direct pressurisation or gravity. It defines
  the energy and the pump sets in the cost and in the carbon.
- With pumping to a tank: tank volume, trigger level and manometric head.
- With direct pressurisation: working pressure and starts per person per day.

### First flush

- Depth adopted and **mode** among the three.
- **The treatment of the depth**, if the study compares Triton with another tool: some
  tools treat the depth as an event threshold, Triton subtracts it from the day's rain,
  and the two give different results.

### Volume and choice criterion

- If it came from a sweep: **the marginal-gain threshold adopted**. Without it, «ideal
  volume» means nothing.
- If it came from multi-criteria: **the four dimension weights and the criterion shares**
  (or the eight criterion weights) and the method, TOPSIS or SMAA-VIKOR.
- If the weights came from **CRITIC**, say so and report the weights it computed, at least
  summed per dimension: they belong to that set of volumes and do not carry over to another.
- **The choice band and its tolerance**, not a single volume: «volumes from A to B L have
  similar TOPSIS scores (within 5% of the score range)». The volume with the highest score
  can follow as information.
- If the volume adopted lies outside the band the multi-criteria analysis gave, **both**:
  the volume and the band, and the criterion that decided.
- The version of the program: the eight criteria are those of version 0.2.0, and a study
  made with version 0.1.0 used seven.
- That the TOPSIS normalisation is a **variant** with a shift by `x − min(x)`.

### Economic analysis

- **City and utility**, with the effective date of the tariff table.
- **Minimum-charge regime** among the six. It is what changes results most between
  utilities.
- Sewage percentage, and that it applies to the **water part** of the bill.
- Minimum attractive rate of return, inflation, analysis period.
- **Tariff escalations** for water, sewage and energy, with the interval.

### Life cycle assessment

- **Boundary**: water delivered, not produced.
- **Service life** adopted and its justification.
- **Material** of the tank, and whether the prices are quotations or illustrative. It
  reverses the sign of the result, as section {{n:11}}
  shows.
- Basis of the electricity grid emission factor, **with the year**.
- Which factors are **approximations** and which carry a **screening label**.

### Certifications

- That quality classes 2 to 4 are **adaptations made by the program**, not by a standard.
- For LEED, the **version** of the framework: v4/v4.1 or v5.
- For EDGE, that the program assesses **only the water bar**, and that the base case used
  is the declared one or the modelled demand.

---

## The ready-made paragraph

For our project, the method would read like this:

> The simulation was carried out in Triton 0.2.0, International Edition, with a daily-step
> behavioural model (overflow calculated before the demand is withdrawn, with the day's
> rain available for the day's consumption, an order between YAS and YBS), on a
> 30-year ERA5 reanalysis precipitation series for New York (10,958 days, mean of 1,125
> mm/year). A catchment area of 150 m² in horizontal projection was adopted, with a
> coefficient of 0.85, a round figure for the combined collection efficiency, and a 2.0 mm
> first flush on every event, subtracted from the daily depth. The total demand adopted
> was 600 L/day (4 residents, 150 L/person·day), with a fraction suppliable by rainwater
> of 28%, corresponding to the toilet and the outdoor uses. The 4,000 L volume resulted
> from the marginal-gain criterion with a 1 %/m³ threshold. A TOPSIS multi-criteria
> analysis with eight criteria in four dimensions (technical, economic, environmental and
> structural, 25% each, with equal criterion shares), with normalisation in a variant of
> Hwang and Yoon shifted by x − min(x), gave instead a choice band of 2,000 to 3,000 L
> (volumes within 5% of the score range from the highest score, at 2,000 L); 4,000 L was kept
> for its higher volumetric reliability and lower overflow, at a higher levelised cost of water.
> The points of use are supplied by pumping to a 1,000 L upper tank,
> with a 100 L trigger level, a 0.5 hp pump, a manometric head of 12 m and the program's
> default motor efficiency. The economic analysis used the New York City Water Board
> tariff in force from 1 July 2026 (a single volumetric water rate and sewer at 159% of
> the water charge), a minimum attractive rate of return of 0.4% per month, inflation of
> 0.2% per month, escalations of 3% per year at 12-month intervals and a 20-year period;
> all costs were illustrative round figures, not market prices. The life cycle assessment
> adopted the boundary of water delivered, illustrative emission factors of 0.40 kg
> CO₂e/kWh and 0.50 kg CO₂e/m³, a polyethylene tank and a service life of 20 years.

That is about three hundred and fifty words, and they are the difference between a study
another researcher can repeat and a loose number nobody can check. The length is modest
compared with what is gained: a method written this way answers in advance most of the
questions a reviewer would ask.

---

## The end of the tutorial

Ten sections, a single project followed from start to finish, and a complete study: it
started from a house without a system and arrived at a recommendation of volume, material,
quality class and a verdict on economic and environmental feasibility — negative on the
first, at the illustrative costs, and positive on the second once the material was
changed — with each decision justified by the number that supported it. The table of section {{n:12}} brings together the
consolidated result.

The way forward depends on what you intend to do next:

- **Solve a case different from the tutorial** — chapter {{c:3}}, the task guides.
- **Understand where each number comes from** — chapter {{c:4}}, the method.
- **Not make the mistakes the program does not prevent** — section {{n:33}}.
- **Defend the study before a reviewer** — chapter {{c:6}}.
