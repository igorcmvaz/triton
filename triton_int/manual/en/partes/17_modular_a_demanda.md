# Modulating the demand by calendar

> **Question this guide answers:** and when consumption is not the same every day?

Schools close for holidays, beach hotels fill up in summer and offices empty at
weekends. Treating any of these buildings as if it had a uniform consumption errs in both
directions at once: it overestimates the demand in the empty periods and underestimates it
at the peaks. ==The error does not cancel out over the year, because what matters to the
rainwater system is not the total consumed but the match between consumption and the rain
available on that day.==

---

## The four modes

The program offers four modes of demand modulation, which differ in the number of values
the user enters and in the situation in which each one is justified ({{fig:fig40_modos}}).



![The four modes of demand modulation](../figuras/fig40_modos.png)

*Figure 99 — The four modulation modes, what each one asks of the user and the situation in which each one is justified. The daily mode only makes sense when there is real measurement, because inventing a daily series adds apparent precision without adding information.*


In any of them you can modulate three things independently: the **per capita demand**, the
**number of occupants** and the **fraction suppliable by rainwater**.

Modulating occupancy is usually more faithful than modulating demand: in a school on
holiday it is not that the pupil drinks less water, it is that there is no pupil.

---

## How to fill it in

In step **2. Building & Demand**, choose the mode. The table of the period opens.

- An empty or zero cell **falls back to the constant value**. This is deliberate: it lets
  you modulate only the months of interest and leave the rest at the default.
- The values can be typed or loaded from CSV.
- In the daily mode, the first day of the demand series lines up with the first day of the
  **rainfall series**. If the two have different lengths, the demand series is recycled
  cyclically.

---

## Why this changes the result

Modulating the demand does not change only the annual total consumed; it changes the timing
match between supply and demand, which is precisely the problem the tank exists to solve. Two
cases from the manual illustrate the reach of this effect.

**A school that closes for holidays.** The cistern is not drawn on while the pupils are away.
Whether that helps depends on when the holiday falls relative to the rain. In the London school
of the manual (300 pupils, 40 L per pupil per day, demand modulated by day of the week, a
30,000 L tank), the weekly profile yields 12.58%, against 12.63% for the same annual demand
spread evenly: 0.05 percentage points. Rain in London is well distributed through the year, so
the weekly rhythm of a school changes almost nothing. A school profile with term and holiday
months would test the idea of a closing during the dry season; the manual has no such case.

**A beach hotel with concentrated occupancy.** In the Cape Town hotel of the manual (800 m² of
roof, 60 guests, 200 L per guest per day, 45% suppliable by rainwater, a 25,000 L tank),
occupancy runs from 95% in January to 20% in June, and the hotel is fullest from December to
February, the dry season. Run with the Cape Town series, the monthly profile yields 9.83%
against 10.97% for the same annual demand spread evenly (a mean of 5,779.9 L/day): 1.14
percentage points less. The demand is concentrated in the months with the least rain, and the
tank, which fills in winter, is drawn down in the dry summer.

The two cases look different, and the rule they support has two parts. ==A demand spread over the
year makes better use of the same tank; a demand concentrated in a few months loses yield, and
loses more when those months are the dry ones.== The Cape Town hotel combines both effects,
concentration and phase: its peak falls in the dry season, and it is not possible to separate the
two with this one run. To isolate the effect of concentration, compare the same profile shifted by
six months, or against a constant demand.

A difference of more than one percentage point is large for a change that does not alter a
single litre of the annual consumption, and it is entirely invisible to any calculation made on
means, which is exactly why Triton simulates day by day. The profiles are in
{{fig:fig19_modulacao}}, and the yield of each one in {{fig:fig20_tipologias}}.

![Three demand profiles with the same annual consumption](../figuras/fig19_modulacao.png)

*Figure 36 — Demand profiles used in the comparison, expressed as the ratio between the month's demand and the mean demand. All have exactly the same annual consumption; what changes is how it is spread over the twelve months.*

![The demand against the rain, and what each profile yields](../figuras/fig20_tipologias.png)

*Figure 99 — (a) Demand profiles of the school and the hotel over the mean monthly precipitation of the city of each case; (b) saving potential of each profile against the same annual demand spread evenly. The hotel profile concentrates the demand in the dry months, and it is this concentration that costs it 1.14 percentage points.*

---

## The suppliable fraction can also vary

Less obvious and sometimes more important. In a school, the percentage of non-potable use
changes between term time and holidays: during the holidays, floor washing and garden
watering remain, and they are uses **entirely** suppliable by rain.

Modulating the fraction captures this. Keeping the fraction constant underestimates the yield
in the period of low occupancy.

In the table, the «Indoor Non-Potable (%)» column is a percentage, like every field you type
in: 28 means 28%. In the project file, the same column is saved as a fraction, 0.28, and
section {{n:5}} explains why. A cell with a value between 0 and 1 turns orange.

---

## Precautions

**Do not modulate what you have not measured.** An invented modulation adds apparent precision
without adding any information, and passes on to the reader the impression of a rigour the
data do not have. When in doubt, an explicitly declared constant demand is more honest than an
arbitrary monthly profile.

**Declare the origin of the profile.** It may come from your own measurement, from twelve
monthly water and sewage bills, from a bibliographic reference or from an estimate, and those
four origins do not carry the same weight of evidence in a published study.

**Check the annual total after modulating.** The program shows the mean daily demand
resulting from the modulation, and a difference between that value and what was expected is
the quickest indicator of an error in filling the table.

---

## The simplest way, when there is one

If you have **twelve water and sewage bills** of the building, you have the measured monthly
profile, which is the best possible source. Divide each month's consumption by the number of
days and by the number of occupants, and use the monthly mode.

Twelve bills are worth more than any reference from the literature.
