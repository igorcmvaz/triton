# Method, statistics and limits

> **Question this section answers:** how does the modulation compute, and how far can it be
> trusted?

## The procedure

The modulation is a Monte Carlo simulation over the program's full chain. For N
realisations with seed s:

1. the program runs the base case, with the study assumptions;
2. it draws, at once, N values of each ticked variable, with the pseudo-random generator
   initialised by the seed;
3. for each realisation, it copies the project, replaces the assumptions by the drawn values
   and reruns the technical,
   economic, environmental and TOPSIS chain for **every** volume of the sweep;
4. it gathers the N realisations into statistics per volume and at the chosen volume.

The comparison between volumes is **paired**: in one realisation, every volume faces the same
drawn assumptions, and the difference between two of them is an effect of the volume, not of
the draw. This is what allows counting how often each volume wins. The volume grid is that of
the study, and the program stops the analysis if it changes between realisations.

## The statistics

The percentiles are empirical, computed over the realisations; the standard deviation is the
sample one, and the coefficient of variation the ratio between it and the magnitude of the
mean. The probabilities come with Wilson's (1927) 95% interval. Sensitivity is Spearman's
(1904) ρ, with ties at the mean rank. The share of variance explained is the correlation
ratio η², the variance between class means divided by the total variance; the classes are
the deciles of the drawn variable, or its own values when it has up to ten distinct values,
as for the number of occupants. It is the class-based estimator of
the first-order index (Saltelli et al., 2008), computed from the same realisations at no
extra cost.

Convergence is tracked by the cumulative mean of the net present value at the chosen volume
and its 95% interval, whose half-width is 1.96 times the standard deviation divided by the
square root of the number of realisations. The band narrows with the inverse square root of
N: quadrupling the realisations halves the sampling uncertainty. If the band still oscillates
at the end of the curve, increase N before publishing.

## Limits

- **The variables are independent.** The program imposes no correlation between them. In
  many projects this is reasonable; when two assumptions move together — more occupants and
  more outdoor demand, for instance — drawing them independently widens the band beyond reality
  in some combinations and narrows it in others.
- **The uncertainty is the declared one.** The output band is never more reliable than the
  input distributions. The screening values are generic; adjust them with data from the
  building, from metering or from the literature, and declare the source.
- **Rainfall varies by factor.** The rainfall factor scales the whole series and
  preserves its temporal structure — the sequence of dry and rainy days. A change in that
  structure, or a different climate scenario, is not drawn: compare them by running the
  modulation once for each series. The effect of series length has its own study (section {{n:24}}).
- **What is not in the catalogue stays fixed.** The price of each material separately, the
  pump parameters, the chlorine dose and the other assumptions follow the study.
  The sensitivity analysis of section {{n:20}} covers the missing ones, one at a time.
- **Class-based η² is biased.** With k classes and N realisations, it overestimates the
  explained share by about (k − 1)/N — 0.009 with ten classes and a thousand realisations.
  Values of that order do not distinguish a variable with no effect.

Probabilistic modulation gives the uncertainty of the result from the uncertainty of the
assumptions; it is not a validation of the model, which section {{n:34}} discusses. For an
introduction to the method and its variants — stratified sampling, variance-based
sensitivity indices — see Saltelli et al. (2008).
