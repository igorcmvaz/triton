# What probabilistic modulation is

> **Question this chapter answers:** is the volume the study chose still a good choice
> when the assumptions are not exactly the ones I declared?

The Triton study answers with one number per volume. That number holds for the declared
assumptions: one per capita consumption, one number of occupants, one non-potable
fraction, one catchment area, one tariff, one discount rate. None of them is known exactly
at the design stage. The per capita consumption of a house that does not yet exist is
estimated; occupancy changes over the service life; the rainfall of the next twenty years
does not repeat that of the last thirty; tariffs are revised.

Tool **13. Probabilistic Modulation** measures how much of that uncertainty reaches the
result. It reruns the finished study many times — a thousand, by default — each time with
the chosen assumptions drawn from distributions declared by the user, and returns the
**distribution** of the result instead of a single value: bands of savings and of net
present value per volume, the probability that the investment pays back and the frequency
with which each volume would be chosen.

==The deterministic study does not change.== Steps 5 to 9, the reports and the command
line keep using it. The modulation is a robustness layer on top of the study: it does not
choose another volume, it says how well the choice holds.

---

## When to use it

The modulation answers three questions the deterministic study does not:

1. **How wide is the result?** With what margin does the study's saving hold? The band
   between the 5th and 95th percentiles of the realisations is the number that should
   accompany the published result.
2. **With what probability does the investment pay back?** A positive net present value
   in the base case may hide a sizeable chance of loss; the modulation gives that chance and
   its confidence interval.
3. **Is the design decision stable?** If the chosen volume wins in a minority of the
   realisations, next to neighbours with similar frequencies, the choice is fragile and the
   text must say so.

In the tutorial example, in section {{n:43}}, the three answers appear in numbers.

It is the natural continuation of the sensitivity analysis of section {{n:20}}. Sensitivity
varies one assumption at a time; the modulation varies all the chosen ones at once, with
weights that come from the distributions, and reveals combinations that a tornado chart
does not show.

## What it does not do

The modulation does not replace measured data. A wide distribution around a wrong value is
still centred on the wrong value: when consumption has been metered, the measurement is
worth more than any draw. The starting distributions the screen proposes are **screening
values** — centred on the project, with generic widths — and must be adjusted to what is
known about the building. Section {{n:44}} discusses the limits of the method.
