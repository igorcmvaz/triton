# Sizing the treatment line

> This section formalises how the program sizes the rainwater treatment plant and explains the
> **incremental rule**, which keeps treatment from being counted twice in the budget and in the
> cash flow.

The water running off a roof carries dust, leaves, soot and bird droppings, and no use — not even
toilet flushing — admits it reaching the point of use as it left the roof. The rainwater
treatment plant of the program is the set of equipment that does this conditioning, and the program sizes it from three
inputs: the quality class the use requires, the roof area and the annual volume of rainwater
actually consumed, the latter a result of the daily balance presented in section {{n:23}}.

The treatment line sized by the program has four components in series. The **first flush** diverts
the first depth of each rain, which carries the dirt accumulated on the roof; the **mechanical inlet
filter** removes leaves and coarse solids before they reach the tank; **disinfection** is the
mandatory stage, on which the microbiological safety of the stored water depends; and the
**polishing filter** is optional, and meant for uses where appearance or the absence of dissolved
residue matters.

---

The treatment line is a sequence, and the order of the stages is not arbitrary: each one removes
what would make the next one ineffective. It is worth having the whole chain in view before
discussing each part ({{fig:fig00j_etap}}). The order is not interchangeable: disinfecting before
filtering consumes the reagent in suspended organic matter and leaves micro-organisms protected in
the particles. Turbidity is therefore a condition of the effectiveness of disinfection, not just an
aesthetic parameter.

![The sequence of stages of the treatment line](../figuras/fig00j_etap.png)

*Figure 99 — Components of the treatment line sized by the program, in the order of the flow, and destination of the material retained. The first flush and the inlet filter act before the cistern; disinfection acts after them because the reagent would be consumed by the suspended organic matter the previous stages remove; the polishing filter is optional.*

---

## The inlet filter

The inlet filter is sized by the roof area, not by the intended quality class, because what it has
to cope with is the peak flow the roof produces — a quantity that does not depend on the final
destination of the water. The three ranges adopted by the program are generic reference ranges, one equipment class per
range; check the capacity declared by the manufacturer of the equipment you specify.

<!-- tabela: Mechanical inlet filter sized by the roof area -->
| Roof | Equipment | Mesh |
| :--- | :--- | ---: |
| up to 200 m² | self-cleaning vortex DN 100 | 350 µm |
| up to 500 m² | self-cleaning vortex DN 150 | 400 µm |
| above 500 m² | basket or cyclonic DN 200 | 500 µm |

> The range limits follow the area a product of that class is declared to serve, not an
> arbitrary margin over it. That is why a 180 m² roof receives the DN 100 filter: the class is
> declared enough for up to 200 m², and imposing that of the next range would make the
> installation more expensive without technical grounds.

---

## Disinfection

Disinfection is the stage the program never dispenses with, and the reason lies in the concept of
residual. Among the three technologies available, only chlorination leaves in the water a
disinfecting agent that remains active after treatment; ultraviolet radiation and ozonation act at
the moment of passage and leave nothing behind ({{fig:fig30_desinfeccao}}).

![The three disinfection technologies available](../figuras/fig30_desinfeccao.png)

*Figure 99 — The three disinfection technologies, the residual effect of each one and the make-up of the annual running cost (OPEX). The residual effect distinguishes chlorination from the others: it protects the stored water, while ultraviolet radiation and ozone act only on the water passing through the equipment.*


==Ultraviolet and ozone come in as a barrier additional to chlorination, not as substitutes for
it.== Without a residual, the treated water becomes contaminated again on the way to the point of
use, and the right practice, which is to keep a free chlorine residual according to the applicable
guideline for the use, keeps chlorination to protect the tank and the internal network. The economic
consequence is direct: both options add the cost of chlorine to their own, and choosing either of
them never reduces the running cost. In the tutorial, tablet chlorination alone is a single stage
with no ultraviolet energy and 0.2 kg CO₂e a year; chlorination plus ultraviolet is two stages,
37.5 kWh a year and 18.2 kg CO₂e; chlorination plus ozonation is two stages and 15.2 kg CO₂e
(illustrative grid factor, not a measured value). The program carries no price catalogue for this
equipment in the International Edition, so these comparisons are about energy and carbon: enter
your own prices if you want cost.

### The mass of chlorine

The chlorination consumable is sized by the mass of commercial product consumed per cubic metre
treated, which follows from the dose applied and the purity of the product bought.

```equacao:massa_cloro
m_prod = ( C_Cl ÷ 1000 ) ÷ p
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `m_prod` | mass of commercial product consumed per cubic metre treated | kg/m³ |
| `C_Cl` | dose of active chlorine applied to the water | mg Cl₂/L |
| `1000` | conversion from milligrams per litre to kilograms per cubic metre | — |
| `p` | purity of the product, in mass of active chlorine per mass of product | dimensionless |

> **What is bought is the product, not pure chlorine.** The calcium hypochlorite tablet contains
> about 65% active chlorine, and the price per kilogram refers to the commercial product, not to
> the active ingredient. Calculating the cost by the mass of active chlorine would underestimate it
> by the inverse of the purity, that is, by about 35% — and it is a common mistake in budget
> spreadsheets.

---

## The polishing filter

The polishing filter is optional and is the only point of the sizing where the target quality
class influences the choice of equipment. For the more demanding classes, the program recommends
including it, and the recommendation also varies in the type of filter medium: laundry, because it
involves contact with fabric and skin, requires block activated carbon, whereas the other uses are
satisfied with a sand filter or a twenty-micrometre cartridge.

<!-- tabela: Polishing filter recommendation by target quality class -->
| Class | Polishing recommended? | Equipment when ticked |
| :--- | :---: | :--- |
| 1 — toilet flushing and general non-potable uses | no | sand filter or 20 µm cartridge |
| 2 — irrigation and washing | yes | likewise |
| 3 — cooling towers and boilers | yes | likewise |
| 4 — laundry | yes | **block activated carbon** |

The recommendation, however, is not an imposition: the filter only enters the sizing if the user
actually ticks it. When the class recommends it and the user declines, the program records the
refusal in a field of its own and the report shows it, so that the decision is documented instead
of disappearing.

> **Classes 2 to 4 are criteria adopted by the program, not by a standard.** The quality required
> for each end use is set by the health authority and the guideline that applies to the case. In a
> published study, present the classes as a criterion adopted by the author, never as a normative
> requirement.

---

## The first flush

The first flush enters the program in two ways. In the water balance, it is the depth subtracted
from each day's precipitation, described in section {{n:23}}. In the budget, when the physical sizing
of the first flush is enabled in step **3. Quality & Treatment** — the default in the interface —, it
is a subsystem with its own investment, running cost and embodied carbon, made up of the leaf
separator and the first-flush chamber.

The volume of the first-flush chamber is the product of the first-flush depth and the catchment
area, `V_ff = d × A`, in litres, with `d` in millimetres and `A` in square metres. The program
sizes a vertical diversion column for small volumes and a tank for larger ones, adds a leaf
separator sized by the catchment area, and gives the subsystem an annual running cost. In the
International Edition the prices are typed in; the manual's cases leave the first-flush subsystem
out of the cost table and count it in the carbon.

<!-- tabela: Sizing of the first flush in the tutorial project -->
| Item | Value |
| :--- | ---: |
| first-flush depth | 2 mm |
| catchment area | 150 m² |
| volume of the first-flush chamber | 300 L |
| embodied carbon of the chamber and the leaf separator | 21.1 kg CO₂e (6.5% of the project's embodied carbon) |

The investment of the subsystem is part of the investment of the treatment line and therefore enters
the cash flow through the incremental rule below.

---

## The incremental rule

The incremental rule is the part of the calculation most often got wrong in home-made
implementations, and the error is always the same: counting treatment twice. It applies on three
different fronts, and on each it takes its own form.

**In the investment.** The budget of a rainwater harvesting system already sets aside a generic
treatment allowance within the accessories item, because no designer prices a system without some
form of filtering. Adding the detailed line on top of that allowance would charge treatment twice,
and so the program deducts the generic allowance and adds only the increment.

```equacao:capex_etap
CAPEX_inc = CAPEX_line − V_gen
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `CAPEX_inc` | incremental investment of the treatment line | currency |
| `CAPEX_line` | total investment in the equipment of the sized line | currency |
| `V_gen` | generic treatment allowance already included in the accessories item | currency |

**In the running cost.** Chlorination is already paid in the chemical consumables line of the cash
flow, so the incremental running cost of the treatment line deducts that part and the hypochlorite
is paid once, not twice.

**In the life cycle assessment.** The treatment line **replaces** the chlorination term instead of
adding to it, and the different treatment between the cash flow and the emission inventory follows
from the two accounting for different quantities.

> The rule lives in a single module, consumed by **both** economic engines of the program. Two
> copies of the same rule diverge over time, and the divergence between them is invisible in the
> result: each engine responds consistently with itself.

---

## Switching the treatment line off

The sizing of the treatment line can be switched off entirely, and in that case neither the
investment nor the running cost of treatment enters the economic analysis. The purpose of the switch
is to allow the study of the hypothesis of treatment already existing in the building — in which case
the cost should not be attributed to the rainwater system — and to compare scenarios with and
without the line. ==Switching it off does not mean the water needs no treatment:== it means the
treatment is not being priced here.

---

## What the program does not size

The scope of the sizing ends at the equipment of the line, and four related items remain the
designer's responsibility. The **hydraulic arrangement of the first flush** — fittings, purge device
and connection to the drainage — is not designed: the program calculates only the volume of the
first-flush chamber and its cost. The **piping** of the treatment line and the head loss it imposes
are not calculated either. The **maintenance regime** — changing the filter element, cleaning the
vortex, replacing tablets — is not planned by the program, although it determines a good part of the
real running cost. And **quality control** remains entirely outside the scope: the program sizes
equipment from assumptions, and does not replace laboratory testing.

Standards for rainwater systems deal with control and maintenance, and the corresponding plan is
the designer's responsibility. Typical practice is to inspect and clean the pre-treatment, the
gutters, the filters and the pumps at intervals of months, and the tank at intervals of a year;
set the intervals from the manufacturer's instructions and the rule that applies to the building.
