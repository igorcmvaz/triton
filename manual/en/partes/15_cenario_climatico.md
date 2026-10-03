# Using a future climate scenario

> **Question this guide answers:** will the system I size today still serve in 2060?

> **Brazil Edition.** The climate projection database described here ships only with the
> Brazil Edition. In the International Edition, the method of this guide applies as it
> stands to projected series of your own — for example, bias-corrected series from a
> national climate service — loaded as rainfall files.

A rainwater tank lasts thirty years or more, and the rain that will fall on the building
over that period will not be the same as the rain that fell in the recent past. Sizing a
long-lived system only on the historical series implicitly assumes a stationary climate — an
assumption the available projections do not support. Netuno brings a database of climate
projections precisely so that the sizing can take this question into account explicitly.

---

## What the database has

<!-- tabela: Content of the national climate database distributed with the program -->
| What the database holds | Quantity |
| :--- | ---: |
| Brazilian cities | 652 |
| CMIP6 climate models | 19 |
| emission scenarios | 2, SSP2-4.5 and SSP5-8.5 |
| historical simulation | 1980 to 2013 |
| future simulation | 2015 to 2100 |

CMIP6 is the sixth phase of the *Coupled Model Intercomparison Project*, the
internationally coordinated exercise that feeds the IPCC reports. Each model is a global
climate model from a different research centre.

## Where the series come from

![Logo of the CLIMBra dataset](../figuras/CLIMBra.jpg)

*Figure — Official logo of CLIMBra (Climate Change Dataset for Brazil), developed for hydroclimatic studies and climate change impacts in Brazil.*

The program's database is extracted from **CLIMBra** (*Climate Change Dataset for Brazil*),
a reference dataset published by Ballarin et al. (2023) in the journal [*Scientific Data*
(Nature)](https://www.nature.com/articles/s41597-023-01956-z)
([doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)), with public
data available in the [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316)
([doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)) under the open
CC0 licence. Three features define what the series represent, and it is worth knowing them
before using them:

**They are bias-corrected projections.** Global models have a resolution of tens to
hundreds of kilometres and reproduce local rain poorly: they tend to get the frequency of
rainy days, the intensity and the extremes wrong. CLIMBra corrected the daily series of the
19 models by the *Quantile Delta Mapping* (QDM) method, which adjusts the simulated
distribution to the observed one and, at the same time, preserves the relative changes of
the quantiles between the historical and the future period. The observed reference was the
daily grid of Xavier, King and Scanlon (2016), built from thousands of rain gauges and
stations in Brazil, with a resolution of 0.25°, that is, about 28 km.

**They are grid cells, not stations.** The series of a city is that of the 0.25° cell that
contains it. It represents the mean rain over an area of the order of 700 km², not that of
a rain gauge. In rugged terrain or on the coast, the difference between the rain of the
cell and that of the plot can be large.

**The database's history is simulated.** The 1980 to 2013 series is not the observed rain,
but each model's simulation for that period, corrected to have the same **statistics** as
the observation. The chronology does not coincide: a rainy day in the model series does not
correspond to a real rainy day. That is why the right comparison for a future scenario is
with the **history of the same model**, not with the observed series that comes with the
program. Mixing the two would attribute to the future climate the difference between
observation and model.

Maraun (2016), in a critical review of bias correction, warns of the limit of the
procedure: it presupposes that the model represents the processes and the change of the
climate plausibly, and it cannot correct an implausible trend. The correction improves the
statistics; it does not turn a bad model into a good one.

> **Database compressed and embedded in the program:** the 37,164 text files of CLIMBra
> (which originally take up about 6.5 GB as uncompressed CSV) were consolidated and
> compressed by Netuno 5 into a high-performance binary SQLite database (`climbra.db`).
> That database is built into the executable and the installer, allowing instant queries
> (< 1 ms per series) and immediate runs for any of the 652 cities without large external
> downloads. The original CSV files are not distributed and do not need to be installed.

---

## Choosing model, scenario and window

The **scenario** represents the future path of greenhouse gas emissions, and the two
available follow the *Shared Socioeconomic Pathways* adopted by the IPCC. They are not
forecasts, but coherent hypotheses about global socioeconomic behaviour over the century
({{fig:fig44_cenarios}}). The name combines the socioeconomic pathway, from 1 to 5, with
the approximate radiative forcing in 2100, in watts per square metre: SSP2-4.5 is the
middle path, with a forcing of 4.5 W/m², and SSP5-8.5 is the fossil-fuel-intensive
development path, with 8.5 W/m². Strong mitigation scenarios, such as SSP1-2.6, are not
part of CLIMBra.

![The two emission pathways available in the database](../figuras/fig44_cenarios.png)

*Figure 99 — The shape of the two emission pathways available in the database. SSP2-4.5 is the intermediate pathway, with emissions that stabilise and then fall; SSP5-8.5 assumes high and growing emissions, without effective mitigation. The figure shows the shape of each one, not projected values.*

The **time window** is the slice of the future series, from 2015 to 2100, on which the study
is made. The program lets you trim any period, with the start and end dates of step
**1. Project & Rainfall**. The most common convention is to take thirty-year windows, the
same length as climatological normals, and the **Period shortcut** field fills the dates
with three of them: 2021–2050, 2041–2070 and 2071–2100, besides the full series. The
shortcut only fills the dates, which remain editable, and the step warns when the slice is
shorter than ten years. The choice of window should relate to the intended service life of
the system: assessing a twenty-year tank, installed now, against the end of the century
assesses a period in which it will already have been replaced.

The choice of the **climate model** is the most delicate of the three decisions, and a
subsection of its own is devoted to it further on.

---

## How to conduct the study

The right procedure is to run the same project in each combination of interest and compare
the results with one another, instead of sizing directly on the projected series. Four
steps summarise it.

1. Close the sizing with the **historical** series. It is the reference.
2. Run the same project on the **simulated history** of each model you will use, from 1980
   to 2013. It is against it, not against the observed series, that the future is compared.
3. Keep all the other parameters and change only the series, for each scenario and window.
4. Compare the **saving potential** and the **days of full supply**, always as a difference
   between the future and the history of the same model. The second usually degrades more
   than the first, because what changes first is the distribution, not the total.

> **An example of reading.** Suppose that, with one model, the potential is 36% in the
> simulated history and 33% in SSP5-8.5 for 2041 to 2070, and that the observed series
> gives 37%. The change attributable to the climate is three points, not four: the
> remaining point is the difference between model and observation, which also exists in the
> past.

> **What not to do.** Size directly on the future series and present the result as a
> design. The future series is a projection with large uncertainty; it serves to test the
> **robustness** of a sizing done on the historical series, not to replace it.

---

## The choice of model, and why it matters so much

Nineteen climate models project nineteen different futures for the same city under the same
emission scenario, and that spread is not noise to be removed: it is the honest expression
of the physical uncertainty of the problem. ==For rain, the spread between models usually
exceeds the difference between emission scenarios,== which means that the choice of model
weighs more on the result than the choice of socioeconomic future.

Hawkins and Sutton (2011) broke down the uncertainty of precipitation projections for
regions of the order of 2,500 km, with the models of the previous phase of the exercise,
CMIP3, into three sources: the internal variability of the climate, the difference between
models and the difference between scenarios. For precipitation, unlike temperature,
internal variability accounts for 50% to 90% of the uncertainty in the first decade and
remains dominant, in many regions, until the third; the uncertainty between models comes to
dominate at longer horizons; and the scenario uncertainty is small or negligible in all
regions and horizons, except near the poles at the end of the century. The authors also
show that the signal-to-noise ratio of the change is below one over almost the whole planet,
and conclude that adaptation decisions will have to be taken with high uncertainty about
regional rain. The consequence for the design is direct: running both scenarios with a
single model informs less than running one scenario with several models.

Three courses of action are defensible in the face of this spread, presented here in
decreasing order of rigour.

**Ensemble.** Run all the available models and report the range of results, with the
median. It is the most rigorous and the most expensive in computing time. Section {{n:19}}
shows how to do it in batch.

**Justified subset.** Choose three to five models with documented good performance for
South America, and declare the selection criterion and the source.

**Single model, declared as such.** Acceptable for an exploratory analysis, as long as the
text does not present the result as a robust projection.

> **What never to do:** run several models, pick the one that gives the most convenient
> result, and report only that one.

---

## What the literature shows about the tank in a future climate

Studies that simulate rainwater harvesting systems under climate projections converge on
one point: the change in the annual total of rain matters less than the change in its
**distribution**. Kisakye et al. (2018), with six models for a district of Uganda, found
conflicting projections between models, but agreement about the season: saving and water
security would fall in the seasons that were already dry and rise in the wet ones, with a
reduction of more than 50% in one of the seasons at the end of the century. Lash et al.
(2014), sizing a tank for a university building in the United Kingdom with 3,000
equiprobable rainfall series from the British climate projections, concluded that, for it to
be likely to meet in 2080 the same demand as today, the tank would need to be 112% larger,
and 225% larger for that to be very likely.

The two studies illustrate what section {{n:14}} showed for Brazilian cities today: cities
with a marked dry season need much larger tanks for the same performance. A future climate
with longer dry spells behaves, for the tank, like a change of city.

---

## What to declare

A study with a climate scenario must state, in the method:

- the **model or models**, by name, and the selection criterion;
- the SSP **scenario**;
- the **time window**, with the years;
- the **historical series** used as the reference;
- whether there was downscaling or bias correction, and which; in the program's database,
  that of CLIMBra, by *Quantile Delta Mapping* against the grid of Xavier et al. (2016);
- the **source of the database**, with the version: Ballarin et al. (2023);
- that the future was compared with the **simulated history of the same model**.

Without this, the result is not reproducible. Appendix {{n:E}} has the source of the
program's database.

---

## A caveat of method

Climate projections carry two stacked uncertainties of different kinds: that of the
scenario, which is socioeconomic and concerns future human choices, and that of the model,
which is physical and concerns the representation of the climate system. Neither is reduced
by running more simulations with the same material, because it is not sampling
uncertainty.

A study conducted honestly presents the result as a range, not as a single number, and
avoids conclusions that depend on the third decimal place of a projection for 2060.
