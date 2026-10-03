# Comparing cities

> **Question this guide answers:** would the same project yield the same in another city?

It would not, and the difference does not go in the direction intuition suggests. The
common expectation is that more rain means more yield, and that expectation is wrong often
enough to deserve a whole section.

> **Edition.** The Brazilian cities of this guide come from the national climate database
> of the Brazil Edition. In the International Edition the same comparison is made with
> rainfall files of your own, one per city; everything else in the guide applies as
> written.

---

## How to make the comparison

The procedure is simple: keep all the parameters of the project and change only the
precipitation series. In step **1. Project & Rainfall**, choose another city from the
national climate database or load a file of your own, and run the simulation again. To
compare several cities without redoing the project for each one, save one file per city,
as section {{n:19}} recommends.

---

## The result

The tutorial project — 150 m² of catchment, 600 L/day of demand, a 28% suppliable fraction
and a 4,000 L cistern — taken to four Brazilian state capitals produces the table below.

<!-- inclui: _tabelas/cap14_cidades.md -->

{{fig:fig03_cidades}} separates the two quantities, each one on its own scale.

![Annual rain and saving potential in the four capitals](../figuras/fig03_cidades.png)

*Figure 99 — (a) Mean annual precipitation and (b) potable water saving potential of the tutorial project, with 150 m² of catchment, 600 L/day of demand, a 28% suppliable fraction and a 4,000 L cistern, in four state capitals. Manaus has the highest annual precipitation and does not have the highest saving potential.*

---

## The regime matters more than the depth

Read side by side, the annual rain and saving potential columns do not move together, and
the two extreme cases of the table show why. Manaus receives 20% more rain than
Florianópolis — 2,155 mm a year against 1,795 mm — and still yields 23% less: 20.96%
against 27.12% potential. Brasília, at the opposite extreme, receives 23% less rain than
Florianópolis and yields little more than half, with 15.45%.

The explanation lies in the ratio between the wettest and the driest month of each city,
which measures how much the rain concentrates over the year.

<!-- tabela: Ratio between the wettest and the driest month in the four capitals -->
| City | Ratio | What it means |
| :--- | ---: | :--- |
| Florianópolis | 3.2× | it rains all year round, with a wetter season |
| São Paulo | 4.0× | likewise, slightly more marked |
| Manaus | 17.3× | a short but real Amazonian dry season |
| Brasília | 1,192× | **the driest month is truly dry** |

In Brasília, June, July and August record practically no rain. A tank sized to get
through ninety days of dry spell would have to store ninety days of rainwater demand,
which in this project would be 15,120 litres — a volume no residential cistern can hold.
The consequence is that the system stays idle for a whole quarter every year, and the
annual potential reflects that idleness.

> **The practical conclusion.** ==Rainwater harvesting yields more where rain is frequent
> than where it is abundant.== Cities with a humid subtropical climate and well-distributed
> rain are the best Brazilian case; cities with a tropical climate and a marked dry season
> are the worst, however intense the rain of the wet season.

---

{{fig:fig18_capitais}} presents the monthly regime of the four capitals on the same scale.

![The monthly regime of the four capitals](../figuras/fig18_capitais.png)

*Figure 99 — Mean monthly precipitation in (a) Florianópolis, (b) São Paulo, (c) Brasília and (d) Manaus, on the same scale; the dashed line is the monthly mean of each series. Florianópolis and São Paulo spread the rain over the whole year; Manaus has a short dry season, from July to October; and Brasília receives practically no rain from May to September. It is this distribution, not the annual total, that decides the performance of the tank.*

---

## What the literature had already found

The result of the four capitals is not a peculiarity of this tutorial. Ghisi and Souza
(2012) simulated houses in thirteen cities in different countries, with Netuno itself, and
reached the same conclusion by another route: the largest saving potential appears where
rain is constant, which does not always coincide with the largest annual depth, and cities
with a well-defined dry season need larger tanks for the same performance.

In Brazil, two surveys show the range of variation within a single state or a single city.
Ghisi, Lopes and Rupp (2016) ran 2,700 simulations for houses in 60 cities of Santa
Catarina, with long daily series, and obtained ideal tanks of 1,000 to 16,000 L and mean
savings of 75 to 461 litres per day per house. Ghisi and Custódio (2019), with 33,720
scenarios for the residential sector of Joinville, found a mean potential of 18.5% with
rainwater only in toilets, and of 40.8% when the washing machine also receives it — the
same choice of use that section {{n:5}} discusses.

The lesson for anyone comparing cities is the same in both studies: the local series
decides, and a volume or a potential brought from another city, even a neighbouring one,
does not replace the simulation.

### Many cities at once

To compare more than three or four cities, changing the series by hand stops being
practical. The national climate database has series for 652 municipalities, and the
scenario spreadsheet of section {{n:19}} runs the same project against several of them in
a single run, saving one result per row. Keep the same building and tank parameters on all
rows of the spreadsheet, and vary only the city: that is what isolates the effect of the
climate.

---

## What else changes between cities

Precipitation is not the only quantity that varies between municipalities, and the other
two can reverse the economic conclusion of a comparative study.

The first is the **tariff**. The price of a cubic metre varies considerably across the
country, and the minimum-charge regime varies even more. A 15% potential in a municipality
with a high tariff and an availability-charge regime can yield more money than a 27%
potential in a municipality with an allowance on the minimum consumption, and section
{{n:16}} deals with that mechanism in detail.

The second is the **electricity grid emission factor**, which changes at the same time the
emission avoided per cubic metre of water replaced and the environmental cost of pumping.
The Brazil Edition has the factor broken down by region; in the International Edition it is
entered for each project.

> **When comparing cities in a study, make clear what varied.** Comparing only the
> precipitation, keeping tariff and emission factor fixed, isolates the climate effect and
> is a legitimate comparison, as long as it is declared as such. Varying all the quantities
> at once produces a number that cannot be explained, because it adds effects of possibly
> opposite signs.

---

## The ideal volume also changes, but little

The last column of the table holds a surprise: the ideal volume varies from 4,000 to
5,000 L across the four capitals, a modest range compared with the difference in regime
that separates them.

The explanation lies in the nature of the criterion. The ideal volume by marginal gain
locates the knee of the yield curve, and the position of that knee is governed by the
**typical size of the rain events**, which is reasonably similar across the four cities.
What varies strongly is the **plateau** the curve reaches after the knee, not the point at
which it bends.

Put another way: in Brasília you get the same volume right as in Florianópolis and harvest
considerably less water with it.
