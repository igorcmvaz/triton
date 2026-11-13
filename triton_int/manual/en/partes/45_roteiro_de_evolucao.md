# Roadmap

> Where the program should go, and on what evidence. A roadmap that separates what is decided
> from what is intended lets users plan a study with the version they have today, not the one they
> would like to have.

This section summarises the `ROADMAP.md` at the root of the Triton repository and reflects the state of the
beta version 0.2.0. Nothing below the line «Stable» exists in this version: these are intentions of the research
group, with no delivery date. When an item is implemented, it leaves this list and enters the version
history, with a note on whether it changes the results of studies already done.

The direction comes from two sources. The first is the systematic literature review the group is
conducting on the simulation of rainwater harvesting. It shows where published studies omit the operating rule, the definition of reliability and
the economic parameters. The second is the program's own issue register, described in the section
«Known limitations».

---

## What is already stable in 0.2.0

**Climate series.** Daily series supplied by the user, plus ERA5 example series for New York,
London and Cape Town. **Tariffs.** Entered by the user, with progressive blocks, fixed charges,
allowances and escalation. **Water balance.** Daily simulation by the Triton rule, with strict YAS, YBS and the Fewkes
(2000b) parameter φ as options for a single tank. **Decision.** Multi-criteria by TOPSIS and by
SMAA-VIKOR, with eight criteria in four dimensions (technical, economic, environmental and structural),
declared criterion shares or objective weights by CRITIC, and a choice band instead of a single volume. **Weight of the system.** Dry mass, water load and operating load by
position, with attention thresholds of the program. **Uncertainty.** Probabilistic modulation of the assumptions (section «What probabilistic
modulation is»). **Edition.** International.

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
