# Example rainfall series (INT)

| File | Location | Period | Source |
|---|---|---|---|
| `NewYork.csv` | New York (grid point in Manhattan, 40.81 N, 74.02 W) | 01/01/1991 to 31/12/2020, 10,958 days | Open-Meteo, ERA5 reanalysis |
| `London.csv` | London (51.49 N, 0.16 W) | same | same |
| `CapeTown.csv` | Cape Town (33.99 S, 18.43 E) | same | same |

Format: one value per line, daily precipitation in millimetres, no date (the start date, 01/01/1991, comes from the project).

These are **reanalysis** data (a grid point of about 9 km), not rain-gauge records. They serve as examples and starting points; for a real project, use the series measured at the site.

Attribution: weather data from Open-Meteo.com (CC BY 4.0), based on the ECMWF ERA5 reanalysis (Copernicus Climate Change Service: Hersbach et al., 2020, *Q. J. R. Meteorol. Soc.* 146, 1999-2049). Retrieved on 14/10/2026 from the archive API (`archive-api.open-meteo.com`).
