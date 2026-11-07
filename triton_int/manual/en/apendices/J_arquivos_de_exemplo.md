# Example files

The manual prints results; these files are what you open to reproduce them. They are in the program's
`casos` folder, and each one carries its rainfall series embedded: they open without the original
CSV, on any machine. The rainfall is the ERA5 reanalysis of 1991 to 2020 for New York, London and Cape
Town that ships in `data/rainfall` (appendix {{n:E}}); each file carries the water and sewage tariff of
its city (appendix {{n:D}}).

**Costs are illustrative, not market prices.** Only the New York tutorial files (01, 04, 06, 09 and
10) carry costs, in US$, as rounded figures that let you follow the method. The other files compare
rainfall, demand and tariff, and leave the costs at zero. Before you draw any economic conclusion,
enter your own costs in stage 5.

---

## The cases of the manual

<!-- tabela: The example cases and what each one demonstrates -->
| File | Section | What it demonstrates |
| :--- | :--- | :--- |
| `01_tutorial_new_york.triton` | 4.1 to 4.10 | the closed tutorial project in New York: a 4,000 L polyethylene cistern and a pumped feed to a 1,000 L upper tank (illustrative costs, not market prices) |
| `02_london.triton` | 3.1 | the tutorial building taken to London, with the London rainfall and the Thames Water tariff (no costs set) |
| `03_cape_town.triton` | 3.1 | the tutorial building taken to Cape Town, with winter-concentrated rain and the City of Cape Town stepped tariff (no costs set) |
| `04_tutorial_sweep.triton` | 4.4 and 2.2 | the project before the upper tank, in sweep mode, from 0 to 20,000 L in 1,000 L steps (New York) |
| `05_ten_days.triton` | 2.1 | the didactic ten-day case, 21 to 30 September 2018 of the New York series, that fits in a spreadsheet |
| `06_upper_tank.triton` | 4.5 | 4,000 L below plus 1,000 above, the comparison of section 4.5 against 5,000 L in one tank (New York) |
| `07_school_weekly.triton` | 3.4 and 3.5 | a 300-pupil school in London with demand modulated by day of the week |
| `08_hotel_monthly.triton` | 3.4 | a beach hotel in Cape Town with monthly occupancy concentrated in the dry summer |
| `09_modulation_tutorial.triton` | 7.3 and 7.4 | the tutorial sweep with probabilistic modulation set up: the three consumption variables, the rain, the tariff and the investment, 1,000 realisations, seed 42 |
| `10_modulation_catchment.triton` | 7.4 | the same sweep with the uncertainty on the catchment (area, runoff coefficient, first flush), the rain factor on the New York series, the tariff and the investment; 1,000 realisations, seed 42 |

## What each one produces

The values below are obtained by **rereading the saved file** and simulating what was reread, not the
configuration that generated it. That is the difference that matters: a parameter that does not
survive saving shows up here as a wrong number, instead of going unnoticed.

<!-- tabela: Result each example case produces when reread and simulated -->
| File | Mode | Volume | Potential | Rainwater consumed |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_new_york.triton` | fixed volume | 4,000 L | 27.09% | 162.6 L/day |
| `02_london.triton` | fixed volume | 4,000 L | 20.08% | 120.5 L/day |
| `03_cape_town.triton` | fixed volume | 4,000 L | 14.52% | 87.1 L/day |
| `04_tutorial_sweep.triton` | sweep | ideal: 4,000 L | 26.83% | 21 volumes |
| `05_ten_days.triton` | fixed volume | 2,000 L | 25.70% | 51.4 L/day |
| `06_upper_tank.triton` | fixed volume | 4,000 L | 27.09% | 162.6 L/day |
| `07_school_weekly.triton` | fixed volume | 30,000 L | 12.58% | 1,134.3 L/day |
| `08_hotel_monthly.triton` | fixed volume | 25,000 L | 9.83% | 567.9 L/day |
| `09_modulation_tutorial.triton` | sweep | ideal: 4,000 L | 26.83% | 21 volumes |
| `10_modulation_catchment.triton` | sweep | ideal: 4,000 L | 26.83% | 21 volumes |

Case 01 includes the 1,000 L upper tank, and case 06 compares it with a single 5,000 L tank, which gives
27.24% (section {{n:8}}).

---

## How to run them

**File, Open Project**, choose the file, and the program loads everything: the rain, the building, the
tariff, the costs and the configuration of the analyses. Go through the result steps in the sidebar to
see each dimension.

Cases 09 and 10 open with **Probabilistic Modulation** already set up: the variables, the
distributions, the number of realisations and the seed of section {{n:43}}. Go to step 13 and click
**Simulate**. Both are in sweep mode, which is what gives meaning to the per-volume figures; in a
fixed-volume case, the tool shows only the study volume. Case 09 draws the three consumption
variables, the rain, the tariff and the investment. Case 10 draws the catchment (area, runoff
coefficient, first flush), a rain factor applied to the New York series, the tariff and the
investment. Both use 1,000 realisations and seed 42.

The files are in the `casos` folder, inside the program's installation folder. If you want to modify
them, **save them under another name**: that way the original case keeps reproducing the number
printed in the manual.

---

## The three projects in `examples`

Besides the manual's cases, the program comes with three example projects in `examples`: the
tutorial house in New York, in London and in Cape Town (`new_york.triton`, `london.triton` and
`cape_town.triton`). The building is the same in the three, so that the results compare. They leave
the costs of works, pump, treatment and maintenance, and the electricity tariff, at zero, because they
depend on the site and the market. Enter your own before reading the economic results; until you do,
the economic analysis shows only the saving on the water bill, and the payback and the net present
value say little.

---

## What these files are not

They are not design templates. They are **demonstration cases**: the costs, where present, are
illustrative; the tariff of each file is the residential water and sewage tariff of its city, entered
as a user would enter it, and it is the residential one in all of them, including the school and the
hotel (see the limitations in section {{n:36}}). For a real study, replace the tariff,
costs and rainfall series with those of your case.
