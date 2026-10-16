# Known limitations

> Where the program does not serve, and why. A program that declares its own limits is more
> trustworthy than one that seems to serve for everything, because the second leaves users to
> discover them for themselves.

This section derives from the issue register the research group keeps, and reflects the state of
the current beta version, 0.1.0. A limitation leaves this list when it is actually resolved, not when it stops being
mentioned — a distinction that seems obvious and that the documentation of scientific programs often
does not observe.

The limitations are grouped by origin, because the remedy each group admits is different. Those of
the model follow from representation choices and only change with a revision of the model itself.
Those of the data depend on surveying, and can be supplied by the user. The methodological ones are
declared departures from a reference formulation. And those of implementation are pending work, with
no conceptual obstacle.

---

## Limitations of the model

**There is no hourly sub-step.** A 40 mm rain concentrated in two hours and the same depth spread
over twenty-four hours produce the same result. For tanks very small relative to the catchment area,
this underestimates the overflow.

**There are no losses in the tank.** Evaporation and leakage are not modelled.

**The initial condition is an empty tank.** In series of less than a year, this penalises the result
noticeably.

**The runoff coefficient is single and constant.** It does not vary with rainfall intensity or with
the time since the last event, when in reality the first event after a dry spell has a lower
coefficient.

**The first flush is a depth, not a device.** The program calculates the volume and cost of the
device, `A × d_f`, but not its hydraulic arrangement, which requires a design of its own.

---

## Limitations of the tariff data

The International Edition has no tariff catalogue: the tariff is typed in, and its accuracy is the
user's.

**One structure is entered at a time.** A study of a school, shop or factory calculates the saving
with whatever structure was typed in. If that is the residential one, the saving is usually
**underestimated**, because non-residential categories tend to be dearer. The error is conservative
and its direction is known, but it must be declared. The program warns when the building type is not
residential; the structure of the right category is then entered as described in section {{n:16}}.

**Sewerage charges are approximated.** Sewerage billed by blocks of its own is represented by a single
percentage of the water bill, or by a fixed value or a price per cubic metre. It is a declared
approximation.

**No social tariff and no seasonal or scarcity surcharges.** A low-income class, a drought surcharge
or a seasonal price are not modelled unless the user folds them into the structure entered. For a
study of social housing the difference can invert the conclusion.

---

## Limitations of the life cycle assessment

**It is a screening assessment**, not an inventory conforming to ISO 14040.

**A single impact category.** Carbon only. There is no eutrophication, acidification, land use or
toxicity.

**The manufacturing emission of the pump set is an approximation by mass.** The program multiplies
the catalogue mass of each power rating by the intensity per kilogram of an environmental product
declaration of a pump of another class. The order of magnitude is defensible; the value for each
power rating is not a measurement.

**Direct pressurisation is modelled by mean values.** The energy uses a single working pressure,
the mean of the pressure switch range, and not the on-off cycle of each use; and no start-up energy
or standby consumption is added, which a pressure pump with a variable-frequency drive would have.
Old projects without an upper tank open with the arrangement «not stated» and receive no energy
until one is chosen.

**There is no end of life.** Neither credit for recycling nor burden for disposal.

**There is no maintenance.** Component replacements over the service life do not enter.

---

## Limitations of water quality

**Classes 2 to 4 are adaptations of the program**, not classes of a standard. The matrix of
parameters by use is an internal convention; declare it as such.

**The constants of the roof wash-off model are not calibrated.** The resulting water quality is an
**assumption**, not a measurement. The program does not replace laboratory testing.

---

## Declared methodological limitations

**The R95p percentile is calculated over the whole series**, not over the fixed ETCCDI base period
1961–1990. Series of different lengths are not directly comparable on this index.

**Opricovic's conditions C1 and C2 are not implemented** in VIKOR. The compromise solution should be
read with the weight sensitivity analysis alongside.

**The TOPSIS normalisation is a variant** with translation by `x − min(x)`, to admit a negative net
present value.

**The tariff adjustment is a single percentage** over the whole analysis period, which makes the
twenty-year projection fragile. It is the assumption that most moves the economic result.

---

## Limitations of implementation

**Six fields are saved in the file and never read.** Among them the **installation month**, so the
cash flow always starts in month 1.



**The pump start-up time, of 108 s per start**, represents the priming time of a pump whose suction
line has drained, and is applied to **every** start. It is conservative.

**There is no option to treat the first flush as an event threshold**, as some other tools do. To
compare with such a tool, use a first flush of zero, where the two rules coincide, or the series
transformation of section {{n:35}}.

---

## What to do with this list

In a published work, cite the limitations that affect your case — not all of them, which would
turn the method section into a defensive list, but those that actually bear on the conclusions
presented. ==A declared limitation is a caveat; an omitted limitation, when discovered, is an
error.==

Three examples guide the selection. A study of a school needs to cite the tariff category issue,
because it shifts the whole economic result. A study of environmental performance needs to cite the
single impact category and the approximation by mass of the pump set emission factor. And a study
of social housing needs to cite the absence of a social tariff, which in that context can invert
the conclusion.

A reviewer who finds one of these limitations left unsaid is entirely right to raise it, and
raising it usually costs more time than declaring it would have cost.
