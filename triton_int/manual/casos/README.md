# Project files from the manual (International Edition)

Each file reproduces a result printed in the manual. Open it with **File > Open project**, then run.

The rainfall series is embedded **inside** each file (daily rainfall of 1991-2020, ERA5 reanalysis, from `data/rainfall`): the file opens without the original CSV, on any computer. Cities: New York (the tutorial), London and Cape Town; each file carries the water and sewer tariff of its city.

Costs are **illustrative, not market prices**: only the New York tutorial files (01, 04, 06, 09 and 10) carry them, in US$, as rounded figures to follow the method. The other files compare rainfall, demand and tariff and leave the costs at zero. Enter your own in stage 5 before drawing any economic conclusion.

Files 09 and 10 open with **Probabilistic Modulation** (stage 13) already set up: go to stage 13 and click **Simulate**. The other files use a fixed volume, except 04, so the modulation tool shows only the volume of the study on them.

| File | Section | What it shows | Result |
| :--- | :--- | :--- | ---: |
| `01_tutorial_new_york.triton` | 4.1 to 4.10 | the closed tutorial project in New York: a 4,000 L polyethylene cistern and a pumped feed to a 1,000 L upper tank (illustrative costs, not market prices) | 27.09% with 4,000 L |
| `02_london.triton` | 3.1 | the tutorial building taken to London, with the London rainfall and the Thames Water tariff (no costs set) | 20.08% with 4,000 L |
| `03_cape_town.triton` | 3.1 | the tutorial building taken to Cape Town, with winter-concentrated rain and the City of Cape Town stepped tariff (no costs set) | 14.52% with 4,000 L |
| `04_tutorial_sweep.triton` | 4.4 and 2.2 | the project before the upper tank, in sweep mode, from 0 to 20,000 L in 1,000 L steps (New York) | ideal volume 4,000 L, 26.83% |
| `05_ten_days.triton` | 2.1 | the didactic ten-day case, 21 to 30 September 2018 of the New York series, that fits in a spreadsheet | 25.70% with 2,000 L |
| `06_upper_tank.triton` | 4.5 | 4,000 L below plus 1,000 above, the comparison of section 4.5 against 5,000 L in one tank (New York) | 27.09% with 4,000 L |
| `07_school_weekly.triton` | 3.4 and 3.5 | a 300-pupil school in London with demand modulated by day of the week | 12.58% with 30,000 L |
| `08_hotel_monthly.triton` | 3.4 | a beach hotel in Cape Town with monthly occupancy concentrated in the dry summer | 9.83% with 25,000 L |
| `09_modulation_tutorial.triton` | 7.3 and 7.4 | the tutorial sweep with probabilistic modulation set up: the three consumption variables, the rain, the tariff and the investment, 1,000 realisations, seed 42 | ideal volume 4,000 L, 26.83% |
| `10_modulation_catchment.triton` | 7.4 | the same sweep with the uncertainty on the catchment (area, runoff coefficient, first flush), the rain factor on the New York series, the tariff and the investment; 1,000 realisations, seed 42 | ideal volume 4,000 L, 26.83% |

The figures in the last column come from **re-reading the saved file** and simulating what was read. If a field does not survive the file, the number changes and the matching test fails.
