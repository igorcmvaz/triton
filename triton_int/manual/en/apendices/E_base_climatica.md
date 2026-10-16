# Climate database

> **The International Edition ships no regional climate database.** The rainfall series of a project
> is always a file of the user (section {{n:4}}). Three example series come with the program, so that
> the manual's cases can be reproduced.

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
