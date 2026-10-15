# Roadmap

> Where the program should go, and on what evidence. A roadmap that separates what is decided
> from what is intended lets users plan a study with the version they have today, not the one they
> would like to have.

This section summarises the `ROADMAP.md` at the root of the Triton repository, which covers all three editions and reflects the state of version
1.0.0. Nothing below the line «Stable» exists in this version: these are intentions of the research
group, with no delivery date. When an item is implemented, it leaves this list and enters the version
history, with a note on whether it changes the results of studies already done.

The direction comes from two sources. The first is the systematic literature review the group is
conducting: 762 quantitative studies on the simulation of rainwater harvesting, of which 56 use
Triton. It shows where published studies omit the operating rule, the definition of reliability and
the economic parameters. The second is the program's own issue register, described in the section
«Known limitations».

---

## What is already stable in 1.0.0

**Climate series.** 652 Brazilian municipalities with continuous projected series (CLIMBra base,
CMIP6). **Tariffs.** 652 municipalities with a catalogue of tariffs transcribed from official
sources. **Water balance.** Daily simulation by the Triton rule, with strict YAS, YBS and the Fewkes
(2000b) parameter φ as options for a single tank. **Decision.** Multi-criteria by TOPSIS and by
SMAA-VIKOR. **Uncertainty.** Probabilistic modulation of the assumptions (section «What probabilistic
modulation is»). **Editions.** Brazil, International and Portugal.

---

## Version 1.1: consolidation and reliability

<!-- tabela: Items planned for version 1.1 -->
| Axis | Item | Method |
| :--- | :--- | :--- |
| International Edition | Global rainfall providers | ERA5-Land and NOAA GHCN-Daily reanalyses |
| International Edition | Metric and imperial units | Conversion without residual, with mass conservation checked in both |
| International Edition | Seasonal and scarcity tariffs | Dynamic blocks, drought surcharge, separate sewer charge |
| Multi-criteria decision | Full ranking with the GAIA plane | PROMETHEE II |
| Multi-criteria decision | Veto thresholds and viability classes | ELECTRE Tri |
| Multi-criteria decision | More consistent weights | Best-Worst Method (BWM) |
| Probability and risk | Dependence between rainfall and demand | Bivariate copulas (Clayton, Gumbel) |
| Probability and risk | Which variables govern the result | First-order and total Sobol indices |
| Probability and risk | Synthetic rainfall | Block bootstrap, preserving consecutive dry days |
| Costs and engineering | Installation cost by material and soil | Parametric curves by technology and soil class |
| Costs and engineering | Detailed operating cost | Filters, disinfection, pump degradation curve |

## Version 2.0: methodological frontier

<!-- tabela: Items planned for version 2.0 -->
| Axis | Item | Method |
| :--- | :--- | :--- |
| System physics | Hourly time step | Hourly model with rain-gauge data |
| System physics | Root-zone water balance | FAO-56 Penman-Monteith, for irrigation |
| System physics | Variable runoff coefficient | Depends on depth and antecedent dry spell |
| Territorial | Urban catchment scale | GeoJSON vectors |

---

## How to read this roadmap

**The order is not a commitment of dates.** The order follows the consequence for the result of a
study. The hourly step, for example, only arrives in 2.0 because it needs rain-gauge data that most
municipalities do not have.

**An item enters on evidence.** Each method listed answers a gap measured in the literature review,
not an implementation preference.

**A change that alters results is declared.** Anyone publishing with the program must record the
version used. That is why the version history separates the correction that changes a number in a
study already done from the one that changes only the interface.
