# Climate database

> **The International Edition ships no regional climate database.** The rainfall series of a project
> is always a file of the user (section {{n:4}}). Three example series come with the program, so that
> the manual's cases can be reproduced. The last two sections of this appendix set out the
> particulars of the edition and describe the data it ships and how far to trust them.

---

## The series that come with the program

Three daily series are installed in the program's `data/rainfall` folder. They are **reanalysis**
data, not rain-gauge records.

<!-- tabela: Rainfall series distributed with the International Edition -->
| File | Place | Period | Days | Mean annual rain | Source |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `NewYork.csv` | New York (grid point over Manhattan, 40.81 N, 74.02 W) | 01/01/1991 to 31/12/2020 | 10,958 | 1,125 mm | ERA5 reanalysis via Open-Meteo |
| `London.csv` | London (51.49 N, 0.16 W) | same | 10,958 | 649 mm | same |
| `CapeTown.csv` | Cape Town (33.99 S, 18.43 E) | same | 10,958 | 495 mm | same |

The format is one value per line: daily precipitation in millimetres, with no date. The date of the
first day comes from the project (1 January 1991 for these three files).

**What they are.** ERA5 is the fifth-generation global reanalysis of the European Centre for
Medium-Range Weather Forecasts (ECMWF), produced by the Copernicus Climate Change Service (Hersbach
et al., 2020, *Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). The series
were extracted for one grid point of about 9 km through the archive interface of Open-Meteo.com
(licence CC BY 4.0) on 14/10/2026. A grid cell is an area average: it smooths intense showers and
overstates the number of days with light rain, so it is a starting point and not a substitute for
a measured record.

**Use for a real design.** Replace the example series with the record of a rain gauge near the site,
or declare explicitly that you use reanalysis and why.

---

## Using your own series

1. Obtain a daily record, in millimetres, from the meteorological service or the gauge closest to
   the site. Record the station, its distance from the site, the period and the source.
2. Save it as a CSV with one value per day. A point or a comma is accepted as the decimal separator,
   and a header line is ignored.
3. Open it in step 1 (Project & Rainfall) and set the date of the first day.

An incomplete year is dropped on reading, so as not to bias the annual totals. Daily data are
required: monthly means hide the dry spells that decide the volume (section {{n:33.2}}).

**How long a series.** The length needed to stabilise the ideal volume is not a geographical
constant: it grows with the suppliable fraction and with the demand of the building (glossary,
appendix {{n:G}}). The three example series have thirty years each.

---

## Future scenarios

The International Edition carries no climate-model projections. To study a future climate, prepare
the projected daily series yourself, from the source you choose, and load it as any other file. The
rain factor of the probabilistic modulation (section {{n:40}}) offers a simple way to test a drier or
wetter series by a declared percentage. Section {{n:15}} deals with conducting the study.

---

## What to declare in a study

- the **source** of the series (station or reanalysis product) and its version;
- the **location**, and for a gauge the distance from the site;
- the **period**, with the first and last years;
- whether the series was **corrected, filled or downscaled**, and how;
- for a projection, the model, the scenario and the window, and the method used to correct bias;
- the number of **years** of data.


---

## Regional and national particulars

The International Edition is neutral on purpose. It ships **no regional rainfall database, no tariff
catalogue, no cost catalogue and no emission-factor series**, and it applies no national standard,
no national tariff structure and no predefined currency. Everything that changes from one country
or region to another is entered by you, and the program calculates with what you enter.

<!-- tabela: What the user supplies in the International Edition, and what happens without it -->
| You supply | Where in the program | Without it |
| :--- | :--- | :--- |
| the daily rainfall series of the site (CSV, TXT or DAT; one value per line, in millimetres) | step 1, climate source «own file» | the simulation cannot run |
| the water and sewer tariffs, in the currency you choose | economic inputs, button *4. Water and Sewage Tariffs* | the water bill is zero, and the economic analysis shows nothing |
| the costs of works, pump, treatment and maintenance | step 4 and the economic inputs | costs are zero, so payback and net present value say little (section {{n:10}}) |
| the electricity tariff | button *2. Motor Pump & Energy Cost* | the pump energy costs nothing |
| the grid emission factor and the emission factor of the potable water you replace | life-cycle inputs | the life-cycle assessment credits no avoided emissions |

**Standards.** The program does not decide which standard applies to your project. Quality
requirements, permitted uses, the first-flush depth and the maintenance interval are set by the
standard or regulation of the place where the system is built. Look it up, enter its limits as the
quality criterion (section {{n:9}}) and cite it in the study. The four quality classes of the program
are a comparison scale, not the text of a standard.

**Currency and units.** There is no predefined currency: choose it in the economic step, and every
value in the project is read in that currency. Volumes are in cubic metres and litres, depths in
millimetres. A tariff published in other units is converted when entered: the New York example, for
instance, publishes its water charge per hundred cubic feet, and the project records it per cubic
metre.

**The three worked examples.** The edition carries three cities so that it opens with something to run,
and each is one end of a different tariff structure.

<!-- tabela: The worked examples of the International Edition: rainfall, currency and tariff structure -->
| City | Currency | Mean annual rainfall | Tariff structure |
| :--- | :--- | ---: | :--- |
| New York | US$ | 1,125 mm | water at a single rate, sewer at 159% of the water charge, minimum daily charge |
| London | £ | 649 mm | volumetric water and wastewater charges plus standing charges |
| Cape Town | R | 495 mm | stepped blocks for water and for sanitation, with monthly standing charges |

The three share one building, so that the results compare. They are examples, not a database of
those cities: their rainfall is a reanalysis grid cell and their tariffs are illustrative (next
section).

---

## Description of the data and how far to trust it

This section summarises the data the edition ships. The full inventory, with sizes, licences,
source addresses and the way to reproduce each item, is in `docs/DADOS.md` of the repository, and
every figure below is the one given there.

**What ships.** Three daily rainfall series, three example projects with their tariffs, the reports
made from them, a few reference files of the core, the 3D viewer and the manual. The largest data
file is 0.04 MiB. No tracked file of the repository exceeds 50 MiB.

<!-- tabela: Example rainfall series of the International Edition: description and quality -->
| Field | New York | London | Cape Town |
| :--- | :--- | :--- | :--- |
| file | `NewYork.csv` | `London.csv` | `CapeTown.csv` |
| location (grid point) | 40.81° N, 74.02° W | 51.49° N, 0.16° W | 33.99° S, 18.43° E |
| mean annual rainfall | 1,125 mm | 649 mm | 495 mm |
| days | 10,958 | 10,958 | 10,958 |
| missing values | none | none | none |
| period | 01/01/1991 to 31/12/2020 | same | same |

**Rainfall: source, licence and quality.** The series are daily precipitation from the ERA5
reanalysis, taken at one grid cell of about 9 km through the Open-Meteo archive interface and
retrieved on 14/10/2026. Licence: CC BY 4.0, with attribution (weather data from Open-Meteo.com,
based on the ERA5 reanalysis of the Copernicus Climate Change Service; Hersbach et al., 2020,
*Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). Redistribution is allowed
with that attribution. A reanalysis cell is not a rain-gauge record: it smooths intense showers and
overstates the days of light rain. The program does not fill gaps, so a series with missing values
must be completed by you before use. For a real design, use the series measured at the site.

**Example tariffs: illustrative, not verified.** The prices were read from each utility's published
tariff and entered as printed: New York from the NYC Water Board and the city's Department of
Environmental Protection, FY2027 rates, in force from 01/07/2026; London from Thames Water, charges
2026-27 for a metered household, taken as starting on 01/04/2026; Cape Town from the City of Cape
Town, Tariffs 2026/27 for a domestic, non-indigent customer, taken as starting on 01/07/2026. For the
last two the effective date is inferred, not printed. Each tariff was checked by hand, once,
against the bill it produces (for 18 m³ per month: US$ 88.08, £ 91.97 and R 1,252.32), and an
automatic test recomputes those bills. There is no independent second check. The address of each
document, the access date and a checksum of the file were not recorded when the examples were
built, so the figures cannot be traced to a stored copy of the document. **Use them to learn the
method, never for a real project:** enter the tariff of your own utility.

**What is left at zero, on purpose.** The costs of works, pump, treatment and maintenance, the
electricity tariff and the grid emission factor are zero or unset in the examples, because no
official source was used for them. The payback and the net present value shown for the three
example projects are therefore **not results**. The tutorial of the manual uses round, illustrative
figures, labelled as such wherever they appear.

**Reference files of the core.** Three small files ship with the program, none of which supplies a
value to your project: `costs_database.json` holds only the cost-file structure, with no prices, currency or regional
factors (costs start at zero and you enter your own); `rotas_producao_agua.json` lists
routes by which potable water is produced, with the emission avoided per cubic metre when rainwater
replaces it, and you declare the route you replace; `fatores_emissao_rede_padrao.json` is an empty
template, so the grid factor is zero until you enter the factor of the grid that supplies the
project.

**How to cite and attribute.** Cite the weather data as above whenever a study uses the example
series. The sky map of the 3D viewer is the «Quarry» map of Poly Haven (CC0 1.0) and the viewer
library is three.js (MIT).
