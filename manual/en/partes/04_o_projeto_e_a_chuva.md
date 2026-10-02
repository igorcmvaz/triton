# The project and the rain

> By the end of this section you will have a project created, a precipitation series
> loaded and the catchment defined. And you will know why each of these three numbers
> matters more than it seems.

The ten sections of this chapter build **a single project**, from start to finish. With
each section the study gains a layer, and the result changes. Keep the file: it is the
same up to section {{n:13}}.

## The project

A single-family house in Florianópolis, in southern Brazil. Four residents, a 150 m²
roof in ceramic tiles, a cistern buried in the back yard. It is the most common case in
Brazil, and the most studied.

The choice of Florianópolis is not sentimental. The available precipitation series is
long; the tariff structure of CASAN, the water and sewage utility of the state of Santa
Catarina, is public and auditable; and the local rainfall regime is well distributed
over the year, which — as section {{n:7}} will show — changes the choice of volume
profoundly.

> **International Edition.** The tutorial uses Brazilian data because it is the case the
> program's results were checked against. In the International Edition you can follow it
> with the Florianópolis series that comes with the program and type in the tariff of
> section {{n:10}}; the hydraulic results are the same in both editions.

---

## The precipitation series

Open step **1. Project & Rainfall**. There are two ways to provide the rain.

**Your own file.** A CSV with one daily reading per line, in millimetres, in a single
column. It is the way for anyone with data from a specific station — in Brazil, from
INMET or from the National Water Agency; elsewhere, from the national meteorological
service.

**National database (Brazil Edition).** 652 Brazilian cities, 19 CMIP6 climate models
and two emission scenarios, with the historical simulation of each model. It is the way
for anyone studying other cities or future scenarios, and section {{n:15}} shows how to
use it.

For our project, use the Florianópolis series that comes with the program and trim the
**first 30 years**.

<!-- inclui: _tabelas/cap04_serie.md -->

Three numbers in this table decide the project, and it is worth looking at them before
any simulation.

**1,795 mm per year** is a lot of rain. Florianópolis is among the rainiest state
capitals in Brazil, and that means the limiting factor of the system will not be the
supply of water, but the demand and the size of the tank.

**It rains on 46% of the days.** Frequent, well-distributed rain favours small tanks:
the cistern fills many times a year instead of having to get through a long dry
spell. Compare with Brasília, in section {{n:14}}, where the rain concentrates from
October to April and the same tank yields little more than half.

**Seven per cent of the days have rain, but below 2 mm.** Those days will be diverted
entirely, and the item on the first flush, further on, explains why.

> **How many years of series to use.** Thirty is comfortable. Below ten, the result
> starts to depend on the stretch chosen; below five, the bias of the empty tank at the
> start of the simulation weighs noticeably. Section {{n:33}} deals with this mistake in
> detail.

---

It is worth looking at a whole series before using it. Thirty years of Florianópolis are
not thirty similar years: the driest year is almost a third below the wettest, and it
is this variation between years that an annual mean erases. The daily distribution
tells the rest of the story — most days have no rain at all, and the annual volume is
delivered by a small number of intense days ({{fig:fig15_serie}}).

![Thirty years of series, and the distribution of rainy days](../figuras/fig15_serie.png)

*Figure 99 — Florianópolis precipitation series used throughout the tutorial: (a) total precipitation of each year, with the thirty-year mean as a solid line and the years above the mean in blue and below it in orange; (b) frequency distribution of daily precipitation on wet days, on a logarithmic scale, which shows how few days account for the largest volumes.*

---

## The catchment area

The tutorial project adopts a catchment area of 150 m², and this is the first field
where people often go wrong.

The catchment area is the **horizontal projection** of the roof, not the sloping area of
the roof. A roof with a 30% slope over a 150 m² plan has about 157 m² of tiled surface,
and still collects the same 150 m² of rain: precipitation falls vertically, and what it
meets is the shadow of the roof projected on the ground. The definition is that of item
3.6 of ABNT NBR 15527:2019: the catchment area is the «horizontally projected area of
the impermeable roof surface where the water is collected», and it is this area `A` that
enters the availability equation of item 4.1.6. The European standard EN 16941-1:2024
uses the same horizontal projection.

> **Catchment area is not contributing area.** ABNT NBR 10844:1989 uses another area,
> for another purpose. To size gutters and downpipes by the peak flow, its item 5.2.1
> adds to the projection the increments due to the roof slope, `(a + h/2)·b` in its
> Figure 2, and the walls that intercept wind-driven rain. That area serves the design
> flow of a five-minute storm (item 5.3.1), and it overestimates the volume the roof
> collects over the year. In Netuno, enter the horizontal projection; the contributing
> area belongs to the gutter design, which the program does not do.

> **Warning.** Using the sloping area overestimates the collection by the ratio
> `1/cos(slope)`. On a 30% roof it gives 4.4% more water that does not exist. On steeper
> roofs the error grows quickly.

---

Once the series is loaded, the program already shows the regime it describes. It is
worth checking this drawing before going on: a series from the wrong city, or with the
wrong unit, usually shows up in the seasonal cycle of {{fig:fig55_programa_sazonal}}
before it shows up in any result.

![The mean seasonal cycle of the loaded series](../figuras/fig55_programa_sazonal.png)

*Figure 99 — The mean seasonal cycle of the series, calculated and drawn by the program as soon as the precipitation is loaded. In Florianópolis, July receives about a third of what November receives, and it is this difference that the tank has to get through. Figure generated by the program itself.*

---
## The runoff coefficient

The tutorial types 0.85 in the coefficient field. The program, in turn, opens with
ceramic tiles selected and applies 0.75, the value the list of materials gives them,
which is also the value it assumes when no material is entered. ==Take care when
reproducing the tutorial: to get the numbers of this manual, choose «Other / Custom» and
type 0.85.==

The origin of 0.85 deserves precision, because it is often quoted as a runoff
coefficient and it is not one. ABNT NBR 15527:2019, in item 4.1.6, writes the available
volume as the product of four terms — precipitation, area, surface runoff coefficient C
and efficiency of the collection system η — and recommends 0.85 **for η**, in the
absence of manufacturer data. That η already accounts for the solids diversion device and
for the diversion of the initial runoff. Netuno has a single field for the fraction of
the rain that reaches the cistern and models the first flush separately, in millimetres.
Typing the standard's η there and also applying the 2 mm first flush counts the loss of
the initial runoff twice, so the tutorial is conservative. In a study, declare the value
adopted in the field, its origin and the first flush, and do not attribute to the
standard a runoff coefficient it does not set.

> **International Edition.** EN 16941-1:2024 writes the yield as the product of a
> surface yield coefficient `e`, given by roof type in its Table 2, and a filter
> efficiency `η`, 0.9 by default, with no first-flush depth. Netuno keeps its own list of
> coefficients and the first flush in both editions; to approach the European standard,
> type `e × η` as a custom value and set the first-flush depth to zero. The repository
> document `docs/normas_nbr_x_en16941.md` lists the differences.

The surface runoff coefficient represents the fraction of the incident rain that
actually reaches the cistern, and the difference to one corresponds to what is lost on
the way. The losses have four origins: absorption by the roof material, evaporation on
the heated surface, splashing out of the gutter and the initial wetting of the tiles at
each new rain event. {{fig:fig35_escoamento}} shows the coefficient the program gives to
each roof material.

![The runoff coefficient by type of roof](../figuras/fig35_escoamento.png)

*Figure 99 — The runoff coefficient the program gives to each roof material, with the values of the study of materials published in the journal MIX Sustentável (2020). The dashed line marks 0.85, the collection factor of ABNT NBR 15527 adopted in the tutorial. The green roof is the only one that departs from the group, because it retains part of the rain in the substrate.*


The program accepts any value between zero and one, and refuses values outside that
interval naming the field — a coefficient larger than one would mean that the roof
delivers more water than the rain brings it. Step **11. Documentation** has the same
table, with the source of the values. For a mixed roof, the coefficient to type is the
mean of the coefficients of each material weighted by their areas.

---

## The first flush

The tutorial diverts 2.0 mm on every rain event.

The first water that washes the roof carries dust, leaves, bird droppings and everything
else that has settled since the previous rain. Diverting it, instead of leading it to
the cistern, is the cheapest and most effective quality measure a rainwater system has,
and that is why it is practically universal in well-run projects. ABNT NBR 15527
recommends a 2 mm first flush when there is no local data to justify another value, and
that is the value adopted here.

The program offers three ways of applying the first flush, which correspond to three
types of self-cleaning device.

<!-- tabela: The three ways of applying the first flush -->
| Mode | When it diverts | When to use |
| :--- | :--- | :--- |
| 1 | on every rain event | the default, and the most conservative |
| 2 | only on the first event after a dry spell | a device that does not empty by itself between close rains |
| 3 | every X days | a device with scheduled emptying |

> **Warning, and this is the point that surprises the most.** When the first flush
> applies and the day's rain **does not exceed** the depth, the **whole** day is lost,
> not the difference. A day of 1.6 mm with a 2.0 mm first flush collects **zero**.
>
> In the Florianópolis series this affects 7% of the days. In climates with frequent
> drizzle, such as the southern Brazilian coast in winter, it can exceed 20%.

The reason for this behaviour is physical, not conventional: the self-cleaning device
has to fill completely before any water goes on to the cistern. When the day's rain is
not enough to fill it, nothing passes, and the retained volume is lost to the drainage
together with the dirt it washed.

> **The depth is not the device.** `d_f` is a depth in millimetres. The hydraulic volume
> of the self-cleaning chamber is `A × d_f`, which in our project gives 150 × 2 =
> **300 litres**. Step **3. Quality & Treatment** sizes and prices that chamber (section
> {{n:27}}), and section {{n:10}} shows its cost in the investment.

---

## What we have so far

<!-- tabela: State of the tutorial project at the end of defining the rain and the catchment -->
| Item | Value |
| :--- | ---: |
| series | Florianópolis, 30 years |
| catchment area | 150 m² |
| runoff coefficient | 0.85 |
| first-flush depth | 2.0 mm, every event |

With this the program already knows **how much water comes in**. It remains to say how
much goes out, which is section {{n:5}}.

A back-of-the-envelope calculation, to calibrate the expectation: 1,795 mm per year on
150 m² at a coefficient of 0.85 gives about 229 m³ per year of raw water, before the
first flush. Section {{n:6}} shows how much of that volume turns into an actual saving —
and the difference between the two numbers is the most important lesson of the tutorial.
