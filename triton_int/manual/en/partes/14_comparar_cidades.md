# Comparing cities

> **Question this guide answers:** would the same project yield the same in another city?

It would not, and the difference is larger than the rain alone suggests. The common
expectation is that more rain means more yield. That holds as a ranking, but it fails as a
proportion, and it fails for a reason that deserves a whole section.

> **Your own cities.** The program ships three sample series: New York, London and Cape
> Town. For any other city, use a rainfall file of your own, one per city; everything else
> in the guide applies as written.

---

## How to make the comparison

The procedure is simple: keep all the parameters of the project and change only the
precipitation series. In step **1. Project & Rainfall**, load another series and run the
simulation again. To compare several cities without redoing the project for each one,
save one file per city, as section {{n:19}} recommends.

---

## The result

The tutorial project — 150 m² of catchment, 600 L/day of demand, a 28% suppliable fraction
and a 4,000 L cistern — taken to the three sample cities produces the table below.

<!-- inclui: _tabelas/cap14_cidades.md -->

{{fig:fig03_cidades}} separates the two quantities, each one on its own scale.

![Annual rain and saving potential in the three cities](../figuras/fig03_cidades.png)

*Figure 99 — (a) Mean annual precipitation and (b) potable water saving potential of the tutorial project, with 150 m² of catchment, 600 L/day of demand, a 28% suppliable fraction and a 4,000 L cistern, in New York, London and Cape Town. The potential falls faster than the rain does from London to Cape Town.*

---

## The regime matters more than the depth

Read side by side, the annual rain and saving potential columns do not move in proportion.
New York receives 73% more rain than London (1,125 mm against 649 mm) and yields 6.75
percentage points more: 26.83% against 20.08%. London receives 31% more rain than Cape
Town (649 mm against 495 mm) and yields 5.6 points more, 20.08% against 14.52%. Set
against the 28% ceiling, New York reaches 96% of it, London 72% and Cape Town 52%.

The explanation lies in how the rain is spread, and the table above shows it twice. The
share of days with rain is 44% in New York, 50% in London and only 28% in Cape Town. And the
ratio between the wettest and the driest month, which measures how much the rain
concentrates over the year, is 1.4 in New York, 1.5 in London and 8.3 in Cape Town.

<!-- tabela: Ratio between the wettest and the driest month in the three cities -->
| City | Ratio | What it means |
| :--- | ---: | :--- |
| New York | 1.4× | it rains all year round, with only a mild seasonal swing |
| London | 1.5× | likewise: modest depth, but well distributed |
| Cape Town | 8.3× | **a marked wet season, and a long dry one** |

London rains less than New York but rains often and evenly, so the cistern is refilled
all year round and full supply reaches 69.1% of the days. In Cape Town the rain comes in a
few winter weeks, and the cistern, which refills in winter, runs short in the dry
summer: full supply falls to 49.9% of the days, against 95.3% in New York with the same
tank. Were the dry season three months long, a tank sized to get through it would have to
store ninety days of rainwater demand, which in this project is 15,120 litres — a volume
no residential cistern can hold. The system then stays idle for part of every year, and
the annual potential reflects that idleness.

> **The practical conclusion.** ==Rainwater harvesting yields more where rain is frequent
> than where it is abundant.== London shows it against New York's depth, and Cape Town
> shows it against London's: a climate with a marked dry season is the worst case, however
> intense the rain of the wet season.

---

{{fig:fig18_capitais}} presents the monthly regime of the three cities on the same scale.

![The monthly regime of the three cities](../figuras/fig18_capitais.png)

*Figure 99 — Mean monthly precipitation in (a) New York, (b) London and (c) Cape Town, on the same scale; the dashed line is the monthly mean of each series. New York and London spread the rain over the whole year; Cape Town concentrates it in winter and has a dry summer. It is this distribution, not the annual total, that decides the performance of the tank.*

---

## Do not carry a result from another city

The comparison above is not a peculiarity of this tutorial, and the lesson for anyone
comparing cities is the same in every study: the local series decides, and a volume or a
potential brought from another city, even a neighbouring one, does not replace the
simulation. A published figure for a climate that is not yours is a hypothesis to test,
not a result to adopt.

### Many cities at once

To compare more than three or four cities, changing the series by hand stops being
practical. The scenario spreadsheet of section {{n:19}} runs the same project against
several series in a single run, saving one result per row. Keep the same building and tank
parameters on all rows of the spreadsheet, and vary only the series: that is what isolates
the effect of the climate.

---

## What else changes between cities

Precipitation is not the only quantity that varies between cities, and the other two can
reverse the economic conclusion of a comparative study.

The first is the **tariff**. The price of a cubic metre varies considerably from one
utility to another, and so does its structure: a flat rate with a sewer surcharge, as in
New York, or stepped blocks, as in Cape Town, where the last cubic metre is the dearest.
A 15% potential under a steep tariff can yield more money than a 27% potential under a
low one, and section {{n:16}} deals with that mechanism in detail. The sample cities
carry their own published tariffs, but only the New York tutorial carries costs, so this
guide compares them on saving potential, not on payback.

The second is the **electricity grid emission factor**, which changes at the same time the
emission avoided per cubic metre of water replaced and the environmental cost of pumping.
In the International Edition it is entered for each project.

> **When comparing cities in a study, make clear what varied.** Comparing only the
> precipitation, keeping tariff and emission factor fixed, isolates the climate effect and
> is a legitimate comparison, as long as it is declared as such. Varying all the quantities
> at once produces a number that cannot be explained, because it adds effects of possibly
> opposite signs.

---

## The ideal volume does not change here

The last column of the table holds a surprise: with the 1 %/m³ threshold, the ideal
volume is 4,000 L in all three cities, despite regimes that differ as much as these.

The explanation lies in the nature of the criterion. The ideal volume by marginal gain
locates the knee of the yield curve, and the position of that knee depends on how the first
cubic metres of storage fill and empty against a daily demand of 168 L, which is the same
in all three cities. What varies strongly is the **plateau** the curve reaches after the
knee, 26.83%, 20.08% and 14.52%, not the point at which it bends. The coincidence belongs to
this house, this threshold and these three cities; it is not a law, and another demand or
another threshold can separate them.

Put another way: in Cape Town you get the same volume right as in New York and harvest
barely more than half the water with it.
