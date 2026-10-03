# Ten mistakes the program does not prevent

> These are not defects of the program. They are **engineering** mistakes it accepts without
> complaint, because it has no way of knowing. Each one gives the mistake, why it is tempting, what
> it does to the result, and how to avoid it.

---

## Using the sloping area of the roof

**The mistake.** Entering the area of the roof surface instead of the horizontal projection.

**Why it is tempting.** It is the area that appears in the roof tile quantities, and the one the
builder knows.

**What it does to the result.** It overestimates the catchment in the ratio `1 ÷ cos(slope)`. On a
roof with a 30% pitch, 4.4% of water that does not exist; at 60%, 16.6%.

**How to avoid it.** Item 3.6 of NBR 15527:2019 defines the catchment area as the horizontal
projection; EN 16941-1:2024 does the same. Do not use the contributing area of NBR 10844, which adds
half the height of the roof and the walls to size gutters. Rain falls vertically, and what it sees
is the shadow of the roof on the ground. If you have the sloping area, multiply it by `cos(slope)`,
as in {{fig:fig00i_projecao}}.

---

![Rain falls vertically, and the catching area is the projection of the roof](../figuras/fig00i_projecao.png)

*Figure 99 — Catchment area as the horizontal projection of the roof, according to item 3.6 of ABNT NBR 15527:2019. For a 30% pitch, θ = 16.7° and the sloping area is 4.4% larger than the horizontal projection; using the sloping area overestimates the volume collected in that proportion on every day of the series.*

---

## Sizing by the mean monthly rainfall

**The mistake.** Using the mean monthly precipitation in a spreadsheet calculation, instead of the
daily series.

**Why it is tempting.** The monthly mean is the figure published in the climatological normals, and
the spreadsheet fits on one page.

**What it does to the result.** It systematically overestimates. The mean hides that rain arrives
concentrated: a month with 200 mm spread over five events fills the cistern and makes it overflow
five times, while the mean calculation assumes a continuous flow the cistern would absorb entirely.

**How to avoid it.** It is this program's reason for existing. Section {{n:23}} shows the overflow
happening day by day; a calculation by means does not see it.

---

## Confusing the first-flush depth with the volume of the device

**The mistake.** Entering in the first-flush field the volume of the self-cleaning chamber, in
litres.

**Why it is tempting.** The device is sized in litres, and the field asks for a number.

**What it does to the result.** The field expects **millimetres**. Entering 300, thinking of the
device's 300 litres, produces a first flush of 300 mm — larger than almost any daily rainfall ever
recorded in Brazil. The system collects **practically nothing**.

**How to avoid it.** `d_f` is a depth. The volume of the device is `A × d_f`: in the tutorial
project, 150 m² × 2 mm = 300 litres. They are the same decision expressed in two units, and the
program wants the first.

---

## Ignoring the minimum-charge regime

**The mistake.** Building the tariff table with the progressive blocks and forgetting how the
utility treats minimum consumption.

**Why it is tempting.** The blocks are what is published prominently. The minimum-charge regime is
in a footnote, when it is there at all.

**What it does to the result.** In a municipality with an **allowance within the minimum**, which
are 329 of the 652 in the database, saving below the allowance **discounts nothing**. A study that
assumes a linear discount produces a payback that does not exist.

**How to avoid it.** Section {{n:16}}. And the practical test: simulate two consumptions, one
inside and one outside the minimum block, and compare them with a real bill of the building.

---

## Simulating a school or hospital with a residential tariff

**The mistake.** Using the residential tariff of the catalogue for a non-residential building.

**Why it is tempting.** The catalogue has 652 municipalities ready to use, almost all of them only
with the residential category, and the program does not prevent it.

**What it does to the result.** It underestimates the saving. Non-residential categories are more
expensive: at CASAN in April 2026, the first block costs R$ 6.81/m³ for commercial against
R$ 3.08/m³ for residential.

**How to avoid it.** The program **warns** when the building type is not residential, and states
the direction of the error. Choose the building's category where the catalogue has it, today in the
CORSAN municipalities; elsewhere, enter the structure of the right category in custom mode. Section
{{n:18}} deals with the subject. In the International Edition the tariff is always typed in, so
type the one for the building's category.

---

## Expecting the upper tank to increase the saving

**The mistake.** Adopting the elevated tank expecting more water.

**Why it is tempting.** It is the classic Brazilian arrangement, and «more storage» sounds like
«more water».

**What it does to the result.** With the same total storage, the arrangement with an elevated tank
delivers **less**: the cistern overflows while the tank above still has room, because pumping only
happens when there is consumption. In the tutorial, about a sixth of a percentage point less, plus
7.7 kWh a year of energy.

**How to avoid it.** Decide on the tank by a **hydraulic** criterion — gravity pressure, a reserve
against power cuts — not a water-saving one. Section {{n:8}} makes the fair comparison.

---

## Adopting too short a series

**The mistake.** Simulating with two or three years of series.

**Why it is tempting.** It is what can be obtained quickly from a nearby station.

**What it does to the result.** Two effects added together. The **empty-tank bias**, because the
simulation starts with the cistern dry and the first months penalise the result; and the
**dependence on the stretch**, because a short series may fall in an atypically dry or wet period.

**How to avoid it.** Thirty years is comfortable, ten is the minimum defensible. Below that, declare
the limitation and show the result as a range.

---

## Choosing the quality class by cost

**The mistake.** Adopting class 1 because it is the cheapest, for a use that would require more.

**Why it is tempting.** The program allows it, and the cost difference is visible immediately.

**What it does to the result.** It does not change the number; it changes the **validity** of the
project. A system feeding a washing machine with water treated to the normative minimum is a quality
decision, not a budget one.

**How to avoid it.** Choose by the **requirement of the use**. And remember that classes 2 to 4 are
adaptations of the program, not requirements of NBR 15527: use them as a declared criterion, not as
a standard.

---

## Comparing with Netuno 4 without declaring the divergence

**The mistake.** Presenting results of the two versions side by side as if they were comparable.

**Why it is tempting.** They are the same program, in different versions.

**What it does to the result.** Netuno 5 estimates, on average, **2.3 to 2.7 percentage points
less** saving than Netuno 4 over 4,050 reference cases, and about **half** of that difference comes
from the treatment of the first flush, which changed deliberately.

**How to avoid it.** Declare the divergence, and compare with a first flush of zero, where the two
rules coincide. Sections {{n:21}} and {{n:35}} go into detail.

---

## Publishing the volume with the highest saving as the recommendation

**The mistake.** Choosing from the sweep the volume with the highest potential.

**Why it is tempting.** It is the column rainwater harvesting studies report, and more is better.

**What it does to the result.** In the tutorial, 20,000 L give the highest potential, the same 12,000
L already gave. They also cost **3.9 times more** than the 4,000 L and carry **4.1 times more
embodied carbon**, to deliver 0.88 percentage points more. And, in concrete, the larger volume is
environmentally **worse** in absolute terms.

**How to avoid it.** Declare the selection criterion. If it is hydraulic, the marginal-gain
threshold; if it is multi-criteria, the weights. And report the winners of each criterion alone,
because the divergence between them **is** the result.

---

## The underlying mistake

The ten above have a common root: **treating the program as a calculator instead of a model**.

A calculator receives numbers and returns numbers. A model receives assumptions and returns the
consequences of those assumptions. Every Netuno result is conditional on what was declared, and the
quality of the study lies in the quality and explicitness of those declarations.

That is why section {{n:13}} gives the list of what to declare, and why section {{n:36}} gives the
known limitations. A study that does not declare its assumptions is not reproducible, however
correct the calculation.
