# What quality the use requires

> By the end of this section the project will have a treatment line defined, and you will
> be able to tell what a standard requires from what the program recommends.

Up to this point the tutorial has treated rainwater only as volume: how much is
collected, how much is stored, how much is consumed. Water, however, is also a quality,
and quality costs money — in equipment at installation and in consumables every month.
This section defines the quality class of the project and sizes the corresponding
treatment line.

---

## What standards say, and what they do not say

Rainwater harvesting standards differ from one country to another, and the program does
not decide which one applies to your project. In general, a standard for non-potable use
sets a short list of minimum parameters: a microbiological indicator such as *E. coli*,
turbidity and pH, and, if chlorine is used, a range for the free residual. Disinfection
is often left to the designer's discretion, and monitoring is asked for at a stated
interval. Some standards divide the non-potable uses into classes with different
requirements; others set a single set of parameters for all of them; others set no
quality table and let the use and a risk assessment decide whether treatment beyond the
filter is needed. Check the standard of the jurisdiction of the project and enter its
limits as the criterion.

The program, in turn, offers four classes, and the reason is practical: toilet flushing
and garden watering do not expose the user in the same way, even if a standard does not
distinguish them ({{fig:fig36_classes}}).

> **Reuse is not harvesting.** Parameters set for the **reuse** of wastewater are usually
> much stricter than those for rainwater harvesting: absence of coliforms, a higher
> residual chlorine and lower turbidity. Rainwater is not reuse, and the table that
> applies to harvesting is the one in the rainwater standard, not the one in the reuse
> standard.

![The program's four quality classes](../figuras/fig36_classes.png)

*Figure 99 — The program's four quality classes and the status of each one. Class 1 is the minimum reference set, with the least demanding parameters; classes 2 to 4 are adaptations made by the program, suitable for comparing treatments and unsuitable for presentation as a normative requirement.*


> **Classes 2 to 4 are adaptations made by the program, not by a standard.** Triton
> itself says so on the screen and in the report. In a published study, do not present
> them as a normative requirement: present them as the criterion adopted, and cite the
> source.

---

## The class recommends, you decide

Choosing a class imposes no equipment on the project. The class expresses a
recommendation of the program, based on the typical requirement of the intended use, and
the decision to adopt it or not remains with whoever signs the project.

<!-- inclui: _tabelas/cap09_etap.md -->

The second table reveals the point: without the polishing filter, the four classes cost
exactly the same. The target class changes a single thing, which is whether the program
recommends fine filtration or not, and the corresponding filter only enters the budget
when the user ticks it explicitly.

When the class recommends polishing and the user declines it, the program records the
refusal in the report, instead of imposing the equipment silently or letting the decision
go unrecorded. ==It is the right conduct in any design program: whoever signs decides,
and the decision is documented for whoever comes later.==

---

## Disinfection

Disinfection is the stage on which the microbiological safety of the stored water
depends, and the program offers three technologies. The difference between them is large,
both in cost and in behaviour, and the criterion that separates them is not the
effectiveness of disinfection — all three disinfect — but the persistence of the effect.

**Tablet chlorination.** A feeder with calcium hypochlorite tablets in the line, in one
stage. It is the default option. It leaves a **residual** in the water, which protects
the tank and the internal network against recontamination. The edition carries no
equipment catalogue, so the cost of the line is whatever you enter in the economic step,
from your own quotations; this manual quotes no price for treatment equipment.

**Ultraviolet.** A reactor with a UV lamp, in a second stage after chlorination. The lamp
and the reactor use 37.5 kWh per year in this project. **It leaves no residual**: it
disinfects what passes through it, and nothing protects the water afterwards.

**Ozonation.** Also a second stage after chlorination, also without residual.

> **Warning.** In the program, ultraviolet and ozone enter as an **additional** barrier to
> chlorination, not as substitutes. It is the right practice: without a residual, the
> treated water becomes contaminated again on the way to the point of use.
>
> That is why the UV and ozone lines add to the chlorine line instead of replacing it.
> Anyone who expected that replacing chlorine with UV would **reduce** the cost will see
> the opposite.

The carbon impact follows the same order: 0.2 kg CO₂e per year with chlorination, 18.2
with ultraviolet and 15.2 with ozonation, for the volume treated in this project, at the
illustrative grid factor of 0.40 kg CO₂e/kWh. The difference is in the electricity
consumed by the lamp and the ozone generator, since the chemical consumable of
chlorination has a modest manufacturing emission by comparison.

---

## The inlet filter

Before any disinfection comes the mechanical inlet filter, which removes leaves and coarse
solids from the water before it reaches the tank. The program sizes it by the roof area,
not by the intended quality class, because what this filter has to cope with is the peak
flow of the roof — a quantity that does not depend on the final destination of the water.

<!-- tabela: Mechanical inlet filter sized by the roof area -->
| Roof | Filter | Mesh |
| :--- | :--- | ---: |
| up to 200 m² | self-cleaning vortex DN 100 | 350 µm |
| up to 500 m² | self-cleaning vortex DN 150 | 400 µm |
| above | basket or cyclonic DN 200 | 500 µm |

Our 150 m² roof is in the first range. These filters retain particles of a few hundred
micrometres, well below a millimetre.

---

## The incremental cost rule

The investment in the treatment line is not added in full to the total investment of the
system, and the reason is to avoid double counting. The budget of a rainwater system
already sets aside a generic treatment allowance within the accessories item, because no
designer prices a system without some filtering; adding the detailed line on top of that
allowance would charge treatment twice. The program deducts the generic allowance and adds
only the increment, as Equation {{eq:capex_etap}} formalises in section {{n:27}}.

The same goes for the running cost: chlorination is already paid in the chemical
consumables line of the cash flow, and the treatment line deducts that part so as not to
charge the hypochlorite twice.

And in the life cycle assessment, the treatment line **replaces** the chlorination term
instead of adding to it. Section {{n:27}} details the rule.

---

## The tutorial's decision

**Class 1, tablet chlorination, no polishing filter.**

The water goes to the toilet and the outdoor area. Class 1, the program's minimum
reference set (an *E. coli* limit, turbidity and pH, with a free-chlorine range),
covers both. A project that adds the washing machine goes beyond the uses most standards
list, and the responsible professional must define and declare the quality criterion for
it, as section {{n:5}} records. Chlorination leaves a residual, it is the simplest of the
three lines, and it has the lowest energy and carbon: 0.2 kg CO₂e per year. The first
flush is sized in the same step; its chamber is the 300 L of section {{n:4}}.

<!-- tabela: State of the tutorial project after defining the quality class -->
| Project so far | |
| :--- | ---: |
| volume | 4,000 L |
| quality class | 1, minimum reference set |
| disinfection | tablet chlorination |
| polishing filter | no |
| annual carbon of the treatment line | 0.2 kg CO₂e |

We have volume, arrangement and quality. Now the question that decides whether the
project leaves the drawing board.
