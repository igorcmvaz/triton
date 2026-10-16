# The variables and the distributions

> **Question this section answers:** what can I draw, and how do I describe the
> uncertainty of each assumption?

## The catalogue of variables

The tool draws twenty assumptions, organised in seven groups. On opening, only the three consumption ones are ticked —
per capita consumption, number of occupants and non-potable fraction — because they are the
most uncertain in a new project and the ones the literature shows to move the result (Silva
and Ghisi, 2016). The others keep the study value until the user ticks them.

<!-- inclui: _tabelas/cap40_catalogo.md -->

Each group acts at a different point of the calculation chain:

- **Demand** changes the daily consumption and the fraction that rainwater can supply. The
  total suppliable fraction is recalculated at every draw from the indoor fraction and the
  outdoor demand, by the same rule as the study (section {{n:5}}). In the weekly, monthly
  and daily modes, the series receive the drawn factor: the calendar profile is kept, and
  the level changes.
- **Catchment** changes the volume of rain that reaches the cistern: area, runoff
  coefficient and first-flush depth.
- **Rain** multiplies the whole daily series by a factor. It is the simplest way to
  represent future rainfall drier or wetter than the historical record. Drawing amongst
  climate models, described below, replaces the series itself.
- **Tariffs** changes the price of water, sewerage and electricity and their escalation.
- **Costs** changes the initial investment and the annual operation and maintenance cost.
- **Cash flow** changes the discount rate and the analysis horizon.
- **Environment** changes the emission factors of the life-cycle assessment.

## What each economic variable multiplies or replaces

The economic variables are of two kinds. Those with their own unit — escalations, rate,
inflation, electricity tariff, period — **replace** the project value by the drawn one. The
**factors** (×) multiply a project value and equal 1 in the study: a drawn factor of 1.15
represents a cost 15% above the estimate. The table states what each one acts on and what
it leaves out.

<!-- tabela: What each economic and environmental variable does in the calculation, and what it does not touch -->
| Variable | Acts on | Does not touch |
| :--- | :--- | :--- |
| Water and sewerage tariff factor | every monetary value of the water structure — bands, fixed charge, minimum bill, base price of the exponential curve — and sewerage charged in currency units (fixed or per m³) | the exponent of the exponential curve; sewerage as a % of water, which already follows the water |
| Sewerage factor | the sewerage tariff, in the mode the project declares: the percentage, the fixed value or the price per m³ | the water tariff |
| Tariff escalation | the escalation of water and sewerage in each escalation period, instead of the declared one | the electricity escalation |
| Electricity tariff | the price of the pumping kWh, instead of the declared one; the tariff flag is still added | — |
| Electricity escalation | the escalation of the electricity tariff in each period | — |
| Investment factor | the **whole** initial investment of each volume: cistern, upper tank, pump, piping, accessories, labour and treatment line | the annual running cost |
| Cistern price factor | only the cistern price of each volume, the part of the investment that grows with volume; with automatic labour, labour follows it, by the program's rule | the other items of the investment |
| Running cost factor (O&M) | the annual operation and maintenance cost: the items declared in the economic step, the running cost of the treatment line and chlorine | pumping energy, which has its own variables |
| Running cost inflation | the annual adjustment of the running cost, instead of the declared one | the tariffs |
| Minimum attractive rate of return | the discount rate of the cash flow | — |
| Analysis period | the horizon of the cash flow and of the environmental assessment, in whole years | the rainfall series, which remains that of the study |
| Potable water emission factor | the emission per m³ of the mains water the cistern avoids | the embodied carbon of the materials |
| Grid electricity emission factor | the emission factor of the pumping energy | the embodied carbon of the materials |

The two investment factors combine. Ticked together, the cistern receives the product of
both, and the rest of the investment only the investment factor. In practice, the
investment factor represents the uncertainty of the estimate as a whole — region, date,
contingencies — and the cistern factor that of the item that defines the optimum: since the
cistern price is the part of the cost that grows with volume, it is the one that shifts the
volume with the shortest payback.

## Rainfall uncertainty

The International Edition has no database of climate-model series, so rainfall uncertainty enters
through the **rainfall factor**. The factor multiplies the whole daily series of the project — a
file the user supplies, or one of the bundled example series — and so keeps its temporal
structure: the sequence of dry spells and rainy days does not change, only the level. A factor
drawn with mean 1 and a deviation of 0.10 represents rain 10% wetter or drier than the record, which
is how to represent a future climate drier or wetter than the past. To test a different sequence of
dry spells, run the study once with each alternative series and compare.

## The four distributions

Each ticked variable receives a distribution and its parameters:

<!-- tabela: The four distributions the tool offers, their parameters and when to use each -->
| Distribution | Parameters | When to use |
| :--- | :--- | :--- |
| normal | mean and standard deviation | symmetric uncertainty around a likely value |
| lognormal | mean and standard deviation | positive quantity with an upper tail, such as consumption and construction cost |
| triangular | minimum, mode and maximum | when the range and the most likely value are known, but not the shape |
| uniform | minimum and maximum | when only the range is known |

For the lognormal, the mean and standard deviation entered are those of the variable
itself, not of its logarithm: the program computes the lognormal parameters that return
exactly the requested mean and standard deviation. Any distribution can be **truncated** by
a lower and an upper bound; a value drawn outside them is drawn again. The number of
occupants and the analysis period are rounded to integers and never fall below 1; the
non-potable fraction and the runoff coefficient stay between 0 and 100% and between 0 and
1; factors, prices, areas and consumptions are never negative.

Each card on the screen shows the curve of the chosen distribution, drawn with 4,000
samples, and its 5th and 95th percentiles. It is the quickest way to check whether the
declared width is plausible: a P95 of 400 L/person/day for a dwelling indicates an
exaggerated deviation.

## The level, not the noise of the day

The variables are drawn **once per realisation**: in each realisation, the house has one
per capita consumption, one occupancy and one fraction, valid for the whole rainfall
series. This represents the uncertainty about **how much** the building consumes, which is
the one that matters. Day-to-day variation around that level, optional (field «Daily
variation»), barely moves the result: drawn independently every day, it cancels out over
thirty years of series (Silva and Ghisi, 2016; section {{n:19}}, `stochastic-demand`
subcommand).
