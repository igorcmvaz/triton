# Using a future climate scenario

> **Question this guide answers:** will the system I size today still serve in 2060?

> **Your own projections.** The International Edition carries no climate projection
> database. The method of this guide applies as it stands to projected series that you
> load as rainfall files: for example, bias-corrected daily series from a national
> climate service or from a regional downscaling study. The guide says what to ask of
> such series and how to compare them.

A rainwater tank lasts thirty years or more, and the rain that will fall on the building
over that period will not be the same as the rain that fell in the recent past. Sizing a
long-lived system only on the historical series implicitly assumes a stationary climate — an
assumption the available projections do not support. Triton cannot supply the projections
for your site, but it can run the same project on any series you give it, so that the
sizing can take this question into account explicitly.

---

## What the projected series must be

Check four things about any projected series before loading it.

**It must be daily and in millimetres.** The program reads one value per day, as for any
rainfall file (appendix {{n:F}}). Monthly projections do not serve: the tank responds to
the distribution of the days.

**It should be bias-corrected.** Global climate models have a resolution of tens to
hundreds of kilometres and reproduce local rain poorly: they tend to get the frequency of
rainy days, the intensity and the extremes wrong. A series that has not been adjusted to
the observed distribution will misstate the yield, usually in a direction you cannot tell
in advance. A correction improves the statistics; it does not turn a bad model into a
good one, and it cannot correct an implausible trend.

**It represents a grid cell, not a station.** The series of a place is that of the cell
that contains it, so it describes the mean rain over an area, not the rain at a gauge. In
rugged terrain or on the coast, the difference between the cell and the plot can be large.
The three sample series of the program (New York, London, Cape Town) are of this kind.

**Its history is simulated.** The historical part of a model series is not the observed
rain, but the model's simulation for that period, corrected to have the same
**statistics** as the observation. The chronology does not coincide: a rainy day in the
model series does not correspond to a real rainy day. That is why the right comparison for
a future scenario is with the **history of the same model**, not with the observed series.
Mixing the two would attribute to the future climate the difference between observation
and model.

---

## Choosing scenario and window

The **scenario** represents the future path of greenhouse gas emissions. Scenarios are
not forecasts, but coherent hypotheses about global socioeconomic behaviour over the
century ({{fig:fig44_cenarios}}). A middle path stabilises and then reduces emissions; a
fossil-fuel-intensive path assumes high and growing emissions without effective
mitigation.

![Two emission pathways, as an example of the shape of scenarios](../figuras/fig44_cenarios.png)

*Figure 99 — The shape of two typical emission pathways. The intermediate pathway has emissions that stabilise and then fall; the fossil-fuel-intensive one assumes high and growing emissions, without effective mitigation. The figure shows the shape of each one, not projected values.*

The **time window** is the slice of the future series on which the study is made. The
program lets you trim any period, with the start and end dates of step **1. Project &
Rainfall**. The most common convention is to take thirty-year windows, the same length as
climatological normals. The step warns when the slice is shorter than ten years. The
choice of window should relate to the intended service life of the system: assessing a
twenty-year tank, installed now, against the end of the century assesses a period in
which it will already have been replaced.

The choice of the **climate model** is the most delicate of the decisions, and a
subsection of its own is devoted to it further on.

---

## How to conduct the study

The right procedure is to run the same project in each combination of interest and compare
the results with one another, instead of sizing directly on the projected series. Four
steps summarise it.

1. Close the sizing with the **historical** series. It is the reference.
2. Run the same project on the **simulated history** of each model you will use. It is
   against it, not against the observed series, that the future is compared.
3. Keep all the other parameters and change only the series, for each scenario and window.
4. Compare the **saving potential** and the **days of full supply**, always as a difference
   between the future and the history of the same model. The second usually degrades more
   than the first, because what changes first is the distribution, not the total.

> **An example of reading.** Suppose that, with one model, the potential is 36% in the
> simulated history and 33% in a future window, and that the observed series gives 37%.
> The change attributable to the climate is three points, not four: the remaining point is
> the difference between model and observation, which also exists in the past. (The
> numbers are hypothetical, to show the arithmetic.)

> **What not to do.** Size directly on the future series and present the result as a
> design. The future series is a projection with large uncertainty; it serves to test the
> **robustness** of a sizing done on the historical series, not to replace it.

---

## The choice of model, and why it matters so much

Different climate models project different futures for the same city under the same
emission scenario, and that spread is not noise to be removed: it is the honest expression
of the physical uncertainty of the problem. For rain, the spread between models is often
larger than the difference between emission scenarios, which means that the choice of
model can weigh more on the result than the choice of socioeconomic future. The
consequence for the design is direct: running both scenarios with a single model informs
less than running one scenario with several models.

Three courses of action are defensible in the face of this spread, presented here in
decreasing order of rigour.

**Ensemble.** Run all the available models and report the range of results, with the
median. It is the most rigorous and the most expensive in computing time. Section {{n:19}}
shows how to do it in batch.

**Justified subset.** Choose a few models with documented good performance for your
region, and declare the selection criterion and the source.

**Single model, declared as such.** Acceptable for an exploratory analysis, as long as the
text does not present the result as a robust projection.

> **What never to do:** run several models, pick the one that gives the most convenient
> result, and report only that one.

---

## What the three sample cities suggest about a future climate

Studies that simulate rainwater harvesting systems under climate projections tend to
agree on one point: the change in the annual total of rain matters less than the change in
its **distribution**. Section {{n:14}} shows the same thing across space: Cape Town has
76% of London's rain and a ratio of 8.3 between its wettest and driest months, and its
potential is 14.52% against 20.08% with the same tank. A future climate with longer dry
spells behaves, for the tank, like a change of city, and a tank that is adequate today
may need to be larger to deliver the same reliability.

---

## What to declare

A study with a climate scenario must state, in the method:

- the **model or models**, by name, and the selection criterion;
- the **scenario**;
- the **time window**, with the years;
- the **historical series** used as the reference;
- whether there was downscaling or bias correction, and which method, against which
  observed dataset;
- the **source of the series**, with the version;
- that the future was compared with the **simulated history of the same model**.

Without this, the result is not reproducible.

---

## A caveat of method

Climate projections carry two stacked uncertainties of different kinds: that of the
scenario, which is socioeconomic and concerns future human choices, and that of the model,
which is physical and concerns the representation of the climate system. Neither is reduced
by running more simulations with the same material, because it is not sampling
uncertainty.

A study conducted honestly presents the result as a range, not as a single number, and
avoids conclusions that depend on the third decimal place of a projection for 2060.
