# Climate database

![Logo of the CLIMBra dataset](../figuras/CLIMBra.jpg)

> **Brazil Edition only.** The International Edition does not ship this database; there, the user
> loads the rainfall series of the site as a file of their own (section {{n:4}}).

---

## What the database contains

<!-- tabela: Contents of the national climate database -->
| What the database holds | Quantity |
| :--- | ---: |
| Brazilian cities | 652 |
| CMIP6 climate models | 19 |
| emission scenarios | 2, SSP2-4.5 and SSP5-8.5 |
| simulations per city and model | 3: historical, SSP2-4.5 and SSP5-8.5 |
| total time series | 37,164 series |
| original uncompressed format | ~6.5 GB (CSVs) |
| compiled Netuno 5 format | compressed SQLite database (`climbra.db`) |

Each series is a continuous daily record of precipitation, in millimetres, for a combination of
city, model and simulation: 652 cities × 19 models × 3 simulations give the 37,164 series. The series
come from **CLIMBra** (Ballarin et al., 2023, [*Scientific Data / Nature*](https://www.nature.com/articles/s41597-023-01956-z), [doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z); repository [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316), [doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)),
bias-corrected by *Quantile Delta Mapping* against the daily grid of Xavier, King and Scanlon (2016),
at a resolution of 0.25°. The historical series covers 1980 to 2013 (12,419 days) and the future
ones, 2015 to 2100 (31,411 days); the study windows are free cuts of these series. All are in the
Gregorian calendar. The HadGEM3-GC31-LL, KACE and UKESM1-0-LL models, which originally use 360-day
years, have one day fewer at the end of each series, which does not affect the cut.

---

## Shipping in the executable and optimised format

To avoid the slow handling of tens of thousands of text files and to allow direct distribution in the
Netuno 5 installer and executable, the 37,164 series were compiled and indexed in a **high-efficiency
SQLite** database (`climbra.db`), with binary compression per series via `zlib`.

- **Access speed:** indexed access to the database takes **less than 1 millisecond** per series,
  against tens of milliseconds to open and parse CSV files on disk.
- **Transparency:** the Netuno 5 climate data engine gives priority to the compiled database and falls
  back automatically to the folder of loose `.csv` files if the database is not found.
- **Portability:** it lets the Netuno 5 installer provide the national database ready to use, without
  requiring the user to download and unpack 6.5 GB by hand.

---

## The scenarios

The two CMIP6 Shared Socioeconomic Pathways available in the database are drawn in section {{n:15}}:
SSP2-4.5 is the intermediate pathway and SSP5-8.5 assumes high emissions without mitigation. CLIMBra
does not include strong mitigation scenarios, such as SSP1-2.6.


---

## The historical series that come with the program

Independently of the CMIP6 database, four long historical series come with the installation, in the
program's `data/rainfall` folder:

<!-- tabela: Historical precipitation series distributed with the program -->
| City | Files |
| :--- | ---: |
| Florianópolis | 3 |
| Brasília | 3 |
| Manaus | 3 |
| São Paulo | 3 |

The Florianópolis series used in the tutorial has 86 years; the first thirty years add up to a mean of
1,795 mm a year, with rain on 46% of the days.

---

## What to declare in a study

- the **model or models**, by name, and the selection criterion;
- the SSP **scenario**;
- the **time window**, with the years;
- the **historical series** used as reference;
- whether there was downscaling or bias correction, and which;
- the **provenance and version** of the database.

Section {{n:15}} deals with conducting the study with future scenarios, and warns against the mistake
of choosing the model by the result.
