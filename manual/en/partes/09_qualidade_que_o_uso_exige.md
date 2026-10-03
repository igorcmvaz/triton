# What quality the use requires

> By the end of this section the project will have a treatment line defined, and you will
> be able to tell what the standard requires from what the program recommends.

Up to this point the tutorial has treated rainwater only as volume: how much is
collected, how much is stored, how much is consumed. Water, however, is also a quality,
and quality costs money — in equipment at installation and in consumables every month.
This section defines the quality class of the project and sizes the corresponding
treatment line.

---

## What the standard says, and what it does not say

ABNT NBR 15527 is the Brazilian standard for rainwater harvesting for non-potable uses.
In the 2019 edition, its Table 1 sets three minimum parameters: *E. coli* below 200 per
100 mL, turbidity below 5.0 NTU and pH between 6.0 and 9.0 (item 4.6.3). Disinfection is
at the designer's discretion (4.6.4); if chlorine is used, the standard recommends a free
residual between 0.5 and 2.0 mg/L, with a maximum of 5 mg/L (4.6.5), and asks for
monitoring at least every six months (4.6.7). Apparent colour and total coliforms, which
the 2007 edition limited, left the table.

What the current standard does **not** do is divide non-potable uses into classes with
different requirements. That division existed in the 2007 version and did not survive the
2019 revision, which chose a single set of parameters applicable to all non-potable uses.

The program, in turn, offers four classes, and the reason is practical: toilet flushing
and garden watering do not expose the user in the same way, even if the standard does not
distinguish them ({{fig:fig36_classes}}).

> **Reuse is not harvesting.** ABNT NBR 15575-1:2025, in Table 26 of item 18.4.2, has much
> stricter parameters for non-potable uses — absence of total and thermotolerant
> coliforms, residual chlorine of 0.5 to 3.0 mg/L, turbidity below 2.0 NTU and colour below
> 15 Hazen units —, but they apply to the **reuse** of wastewater. Rainwater is not reuse:
> NBR 15527:2019 distinguishes the two terms (items 3.5 and 3.18), and it is its Table 1
> that applies to rainwater harvesting. The European standard EN 16941-1:2024 sets no
> quality table: it lets the use and a risk assessment decide whether treatment beyond the
> filter is needed.

![The program's four quality classes](../figuras/fig36_classes.png)

*Figure 99 — The program's four quality classes and the normative status of each one. Only class 1 corresponds to the parameters of ABNT NBR 15527:2019; classes 2 to 4 are adaptations made by the program, suitable for comparing treatments and unsuitable for presentation as a normative requirement.*


> **Classes 2 to 4 are adaptations made by the program, not by the standard.** Netuno
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

**Tablet chlorination.** A feeder with calcium hypochlorite tablets in the line. It is the
default option. For the 82 m³ of our project, the treatment line with chlorination costs
R$ 1,547 of investment and R$ 47 per year of running cost, values that include the first
flush sized in the same step — R$ 617 of investment and R$ 40 per year, as section {{n:27}}
details — and the tablets. It leaves a **residual** in the water, which protects the tank
and the internal network against recontamination.

**Ultraviolet.** A reactor with a UV lamp. The line rises to R$ 2,747 of investment and
R$ 263 per year of running cost, with the lamp and the reactor's energy. **It leaves no
residual**: it disinfects what passes through it, and nothing protects the water
afterwards.

**Ozonation.** The line rises to R$ 5,047 of investment and R$ 247 per year of running
cost. Also without residual.

> **Warning.** In the program, ultraviolet and ozone enter as an **additional** barrier to
> chlorination, not as substitutes. It is the right practice: without a residual, the
> treated water becomes contaminated again on the way to the point of use.
>
> That is why the UV and ozone lines add the cost of chlorine. Anyone who expected that
> replacing chlorine with UV would **reduce** the cost will see the opposite.

The carbon impact follows the same order: 0.4 kg CO₂e per year with chlorination, 6.5
with ultraviolet and 15.4 with ozonation, for the volume treated in this project. The
whole difference is in the electricity consumed by the lamp and the ozone generator, since
the chemical consumable of chlorination has a modest manufacturing emission by comparison.

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

Our 150 m² roof is in the first range. These filters retain particles well below the 1 mm
that EN 16941-1:2024 asks of the pre-treatment.

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

The water goes to the toilet and the outdoor area. Class 1, which reproduces Table 1 of
ABNT NBR 15527:2019 (*E. coli* below 200 per 100 mL, turbidity below 5.0 NTU and pH between
6.0 and 9.0), covers both, which are on the list of item 4.1.7 of the standard. A project
that adds the washing machine goes beyond that list, and item 4.1.8 asks the responsible
professional to define and declare the quality criterion for it, as section {{n:5}}
records. Chlorination leaves a residual, and its cost is the lowest of the three. An
incremental investment of R$ 1,197 over the allowance already planned, of which R$ 617 is
the first flush, and R$ 43.45 per year of running cost: R$ 3.45 of tablets and R$ 40 of
first-flush maintenance.

<!-- tabela: State of the tutorial project after defining the quality class -->
| Project so far | |
| :--- | ---: |
| volume | 4,000 L |
| quality class | 1, normative |
| disinfection | tablet chlorination |
| polishing filter | no |
| incremental treatment investment, with the first flush | R$ 1,197 |

We have volume, arrangement and quality. Now the question that decides whether the
project leaves the drawing board.
