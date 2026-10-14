# Modulating the demand by calendar

> **Question this guide answers:** and when consumption is not the same every day?

Schools close in January and July, beach hotels fill up in summer and offices empty at
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
opposite cases illustrate the reach of this effect, and both are common in Brazil.

**For.** A school that closes in July, in the south of the country, closes precisely when it
rains least. The cistern gets through the dry spell without being drawn on and arrives full
in August. The system yields **more** than the annual mean would suggest.

**Against.** A beach hotel fills up in January and February, when it rains most on the
southern coast. It looks good, but the concentrated demand empties the cistern in days, and
for the rest of the year it stays idle. The system yields **less**.

The two cases look opposite and are not, and it is worth stating the rule carefully, because
the intuitive wording — «demand in phase with the rain yields more» — does not survive the
second example. The hotel has a demand **in phase** with the rain, since both peak in summer,
and still yields less. What separates the two cases is not the phase, it is the
**concentration**.

==A demand spread over the year makes better use of the same tank; a demand concentrated in a
few months empties it in days and leaves it idle for the rest of the year, even if those
months are the wettest.== The school benefits because its idle period coincides with the dry
spell, not because it is in phase with the rain.

Run with the Florianópolis series, the same annual consumption and the same 4,000 L tank, the
three hypotheses separate: a constant demand yields 27.1%, the school profile yields 27.3% and
the beach hotel profile yields 25.7%. A difference of almost one and a half percentage points,
against a ceiling of 28%, is large for a change that does not alter a single litre of the
annual consumption, and it is entirely invisible to any calculation made on means — which is
exactly why Triton simulates day by day. The three profiles are in
{{fig:fig19_modulacao}}, and the yield of each one in {{fig:fig20_tipologias}}.

![Three demand profiles with the same annual consumption](../figuras/fig19_modulacao.png)

*Figure 36 — The three demand profiles used in the comparison, expressed as the ratio between the month's demand and the mean demand. All three have exactly the same annual consumption; what changes is how it is spread over the twelve months.*

![The demand against the rain, and what each profile yields](../figuras/fig20_tipologias.png)

*Figure 99 — (a) Monthly demand profiles of the school and the beach hotel over the mean monthly precipitation of Florianópolis; (b) saving potential of each profile with the same 4,000 L tank. The hotel profile concentrates almost a third of the annual consumption in two months, and it is this concentration, not the phase, that costs it almost one and a half percentage points.*

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
