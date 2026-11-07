# The project and the rain

> By the end of this section you will have a project created, a precipitation series
> loaded and the catchment defined. And you will know why each of these three numbers
> matters more than it seems.

The ten sections of this chapter build **a single project**, from start to finish. With
each section the study gains a layer, and the result changes. Keep the file: it is the
same up to section {{n:13}}.

## The project

A single-family house in New York. Four residents, a 150 m² pitched roof, a cistern
buried in the back yard. It is a deliberately ordinary case, so that the method stands
out rather than the building.

New York is chosen for three reasons. The rainfall series is long and complete, 30 years
of daily values. The water and sewer tariff, set by the city's Water Board, is public and
auditable. And the local rainfall regime is well distributed over the year, which — as
section {{n:7}} will show — shapes the choice of volume. Section {{n:14}} takes the same
building to London and Cape Town and shows how much the climate alone changes.

> **Your own site.** The tutorial runs on the sample series and the tariff that come with
> the program. For a real project, replace them with the series measured at the site and
> the tariff you pay, as section {{n:10}} explains; the hydraulic method is the same.
---

## The precipitation series

Open step **1. Project & Rainfall**. There are two ways to provide the rain.

**Your own file.** A CSV with one daily reading per line, in millimetres, in a single
column. It is the way for anyone with data from a specific station, such as the national
meteorological service of the country concerned.

**A sample series.** The program ships with three: New York, London and Cape Town, daily
precipitation for 1991 to 2020 from the ERA5 reanalysis. They are grid-point data, not
rain-gauge records, so they suit tutorials and first studies; for a design, use the
measured series of the site. Section {{n:15}} shows how to test a climate scenario.

For our project, use the New York series that comes with the program. It has exactly 30
years, and no trimming is needed.

<!-- inclui: _tabelas/cap04_serie.md -->

Three numbers in this table decide the project, and it is worth looking at them before
any simulation.

**1,125 mm per year** is a generous supply for this roof. The gross supply, about 143 m³
per year, is more than twice the rainwater demand of the house (section {{n:5}}), which
means the limiting factor of the system will not be the supply of water, but the demand
and the size of the tank.

**It rains on 44% of the days.** Frequent, well-distributed rain favours small tanks: the
cistern fills many times a year instead of having to get through a long dry spell.
Compare with Cape Town, in section {{n:14}}, where the rain concentrates in winter (the
wettest month receives 8.3 times the driest) and the same tank yields about half.

**Seventeen per cent of the days have rain, but below 2 mm.** Those days will be diverted
entirely, and the item on the first flush, further on, explains why.

> **How many years of series to use.** Thirty is comfortable. Below ten, the result
> starts to depend on the stretch chosen; below five, the bias of the empty tank at the
> start of the simulation weighs noticeably. Section {{n:33}} deals with this mistake in
> detail.
---

It is worth looking at a whole series before using it. Thirty years of New York are
not thirty similar years: the annual totals differ from year to year, and it is this
variation that an annual mean erases. The daily distribution
tells the rest of the story — most days have no rain at all, and the annual volume is
delivered by a small number of intense days ({{fig:fig15_serie}}).

![Thirty years of series, and the distribution of rainy days](../figuras/fig15_serie.png)

*Figure 99 — New York precipitation series used throughout the tutorial (ERA5 reanalysis, 1991 to 2020): (a) total precipitation of each year, with the thirty-year mean as a solid line and the years above the mean in blue and below it in orange; (b) frequency distribution of daily precipitation on wet days, on a logarithmic scale, which shows how few days account for the largest volumes.*

---

## The catchment area

The tutorial project adopts a catchment area of 150 m², and this is the first field
where people often go wrong.

The catchment area is the **horizontal projection** of the roof, not the sloping area of
the roof. A roof with a 30% slope over a 150 m² plan has about 157 m² of tiled surface,
and still collects the same 150 m² of rain: precipitation falls vertically, and what it
meets is the shadow of the roof projected on the ground. Most rainwater guidance defines it so: the horizontally
projected area of the impermeable roof surface where the water is collected. It is this
area `A` that enters the availability equation.

> **Catchment area is not contributing area.** Gutter and downpipe design standards use
> another area, for another purpose. To size the drainage by the peak flow of a short,
> intense storm, they add to the projection the increments due to the roof slope and to
> the walls that intercept wind-driven rain. That area overestimates the volume the roof
> collects over the year. In Triton, enter the horizontal projection; the contributing
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

*Figure 99 — The mean seasonal cycle of the series, calculated and drawn by the program as soon as the precipitation is loaded. In New York the wettest month receives about 1.4 times what the driest month receives, a mild cycle that the tank gets through easily. Figure generated by the program itself.*

---
## The runoff coefficient

The tutorial types 0.85 in the coefficient field. The program, in turn, opens with
ceramic tiles selected and applies 0.75, the value the list of materials gives them,
which is also the value it assumes when no material is entered. ==Take care when
reproducing the tutorial: to get the numbers of this manual, choose «Other / Custom» and
type 0.85.==

The origin of 0.85 deserves precision, because it is often quoted as a runoff
coefficient and it is not quite one. Rainwater guidance commonly writes the available
volume as the product of the precipitation, the area, a surface runoff coefficient and
an efficiency of the collection system (filter and diversion), and 0.85 is a round figure
sometimes suggested for that efficiency in the absence of manufacturer data. That
efficiency already accounts for the diversion of the initial runoff. Triton has a single
field for the fraction of the rain that reaches the cistern and models the first flush
separately, in millimetres. Typing a combined figure there and also applying the 2 mm
first flush counts the loss of the initial runoff twice, so the tutorial is conservative.
In a study, declare the value adopted in the field, its origin and the first flush, and
do not attribute to a standard a runoff coefficient it does not set.

The surface runoff coefficient represents the fraction of the incident rain that
actually reaches the cistern, and the difference to one corresponds to what is lost on
the way. The losses have four origins: absorption by the roof material, evaporation on
the heated surface, splashing out of the gutter and the initial wetting of the tiles at
each new rain event. {{fig:fig35_escoamento}} shows the coefficient the program gives to
each roof material.

![The runoff coefficient by type of roof](../figuras/fig35_escoamento.png)

*Figure 99 — The runoff coefficient the program gives to each roof material, with the values the program uses. The dashed line marks 0.85, the collection factor adopted in the tutorial. The green roof is the only one that departs from the group, because it retains part of the rain in the substrate.*


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
and that is why it is practically universal in well-run projects. The tutorial adopts 2
mm, a round value for when there is no local data to justify another; in a study, justify
the depth you adopt.

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
> In the New York series this affects 17% of the days. In climates with more frequent
> drizzle the share is larger.

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
| series | New York, 30 years |
| catchment area | 150 m² |
| runoff coefficient | 0.85 |
| first-flush depth | 2.0 mm, every event |

With this the program already knows **how much water comes in**. It remains to say how
much goes out, which is section {{n:5}}.

A back-of-the-envelope calculation, to calibrate the expectation: 1,125 mm per year on
150 m² at a coefficient of 0.85 gives about 143 m³ per year of raw water, before the
first flush. Section {{n:6}} shows how much of that volume turns into an actual saving —
and the difference between the two numbers is the most important lesson of the tutorial.
