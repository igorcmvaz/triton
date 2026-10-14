# What Triton does, and what it does not

Triton simulates rainwater harvesting systems in buildings. Given the rainfall regime
of a place, the roof of a building and the consumption of the people who use it, it
answers **how much potable water the system replaces**, and at what cost, with what
quality and with what carbon impact.

This section starts from the beginning, so the first two subsections deal with the
object itself before dealing with the program. Readers who already design building
water systems will find them elementary and can go straight to the six dimensions of
analysis, which is where Triton appears; readers who are new to the subject will find
there the vocabulary that the rest of the manual uses without explaining again.

---

## What a rainwater harvesting system is

It is a system that **collects the rain falling on the roof and uses it instead of
mains water**, for the uses that do not need potable water.

The idea is old and simple. What makes it difficult is one thing only: rain does not
fall when you need it. That is why the system needs a tank, and that is why the size
of that tank is the central question of every project — and of this manual.
{{fig:fig00_sistema}} presents the components of the system and the path of the water,
from collection to the point of use.

![The path of the water, from the roof to the point of use](../figuras/fig00_sistema.png)

*Figure 99 — Components of a building rainwater harvesting system and the path of the water, from collection to the point of use. The upper tank is dashed because it is optional: in a single-storey building the pump can pressurise the points of use directly, and the upper tank changes when water is supplied, not the volume available.*

Following the drawing, from left to right:

**The roof** is the catchment area. What counts is the **horizontal projection** of the
roof, not the sloping area, as item 3.6 of ABNT NBR 15527:2019 defines it — it is the
roof's shadow on the ground that receives the rain. Getting this wrong is the first of
the ten mistakes in section {{n:33}}.

**The gutters and downpipes** carry the water to the cistern. The program does not size
them; that is hydraulic design, and in Brazil it follows ABNT NBR 10844.

**The first-flush device** diverts the first millimetres of each event, which carry the
dust, leaves and bird droppings accumulated on the roof. It is the cheapest quality
control measure, and section {{n:9}} shows how much it changes the water that reaches
the tank.

**The cistern**, or lower tank, stores the collected water. When the inflow exceeds the
capacity, the surplus **overflows** to the drainage system. This overflow is not waste
through carelessness: it is the unavoidable consequence of storing a resource that
arrives concentrated.

**The pump and the upper tank** distribute the water. In a single-storey building the
pump can pressurise the points of use directly. In buildings of two or more storeys an
elevated tank is usually adopted: the water is pumped up to it and distributed by
gravity.

**The non-potable uses** are the destination: toilets and urinals, floor and vehicle
washing, landscape irrigation. When rainwater is not enough, the **mains** supplies the
rest, and supply is never interrupted.

The diagram of {{fig:fig00_sistema}} shows how the parts are linked, which is what
matters to follow the calculation. It lacks, however, the information that settles half
of the design questions: where each part sits in relation to the others, and at what
height. The section of {{fig:fig00d_corte}} restores that geometry, because the
difference in level is what determines whether water flows by gravity or needs a pump,
and because the position of the cistern relative to the ground is a construction
decision, not a calculation one.

![The system in section, with the parts at the height where they actually sit](../figuras/fig00d_corte.png)

*Figure 2 — The same system seen in section. The catchment area is the horizontal projection of the roof, not the sloping area of the roof. The elevated tank receives the water pumped from the cistern and returns it to the points of use by gravity; the mains feeds it, through an air gap, supplying the volume that rainwater does not cover. The cistern overflow carries the surplus to the drainage system.*

> **Vocabulary the manual uses all the time.** *Cistern* and *lower tank* designate the
> same component. *Overflow* is the surplus volume that the overflow pipe carries to the
> drainage system. *Rainwater demand* is the part of the consumption that rainwater can
> supply; *total demand* is the whole consumption of the building. Appendix {{n:G}} has
> the complete glossary.

---

## What the program calculates, in one day

The program does an inflow and outflow account, every day, for each day of the
rainfall series. {{fig:fig00b_destino}} shows how the precipitation of one day is
split, and the account is this:

![How the rain of one day is split](../figuras/fig00b_destino.png)

*Figure 99 — Destination of the precipitation of one day. Each box is a part of the balance, and the sum of the overflow, the consumption and the stored volume equals the collected volume. The overflow is calculated before the day's consumption, and the day's rain can already supply the day's consumption: an order between the YAS and YBS rules, explained in the section on the daily balance.*

Reading the drawing:

1. **The first flush is deducted.** With 12 mm of precipitation and a 2 mm first flush, 10 mm of effective precipitation remain.
2. **It is converted into volume.** Ten millimetres on 100 m² of roof, with a runoff
   coefficient of 0.85, give 850 litres. The calculation is `mm × m² × coefficient`, and
   it comes out directly in litres, because one millimetre on one square metre is
   exactly one litre.
3. **It is added to the volume stored in the cistern**, and whatever exceeds the
   capacity **overflows** to the drainage system.
4. **The day's consumption is withdrawn**, up to the rainwater demand.
5. **The remaining volume is carried to the next day** — and it is this dependence
   between consecutive days that makes a daily simulation necessary.

The five steps form a cycle, not a list: the volume left at the end of the fifth step
is exactly the volume from which the third step starts on the next day. This link
between one day and the next is the one thing that a calculation on the annual mean
cannot reproduce, and it is the reason the simulation is daily.
{{fig:fig00e_balanco_do_dia}} represents this sequence in the notation of the daily
balance equations.

![The order of the operations of one day, and the memory that links one day to the next](../figuras/fig00e_balanco_do_dia.png)

*Figure 99 — Sequence of operations of the daily balance, in the order the program runs them, in the notation of the equations of the daily balance section. The purple link around the drawing represents the dependence between consecutive days: the remaining volume V_res,t is the starting volume of the next day.*

> **In depth: why the annual mean is not enough.** It is tempting to divide the annual
> rain by 365 and do the calculation in one go. The result is always optimistic, and
> sometimes very much so. The reason is that rain arrives **concentrated**: it fills the
> cistern in one day, overflows, and then is missing for two weeks. The mean represents
> neither the overflow nor the deficit, and both reduce the yield. Section {{n:23}} shows
> this happening in a ten-day table that you can redo in a spreadsheet, and section
> {{n:7}} shows the size of the error.

Repeated over thirty years of series, this calculation produces the program's central
answer: the **potable water saving potential**, the fraction of the building's total
consumption that rain managed to replace.

---

## The six dimensions

The volume of water supplied is the first question of a project, but not the only one.
The program assesses the system in six dimensions, which generally lead to different
optimal volumes ({{fig:fig26_dimensoes}}).

![The program's six dimensions of analysis](../figuras/fig26_dimensoes.png)

*Figure 99 — The six dimensions of analysis and the question assessed in each one. The program goes through them in this order, and each one is treated in a section of its own in the method chapter.*

Each dimension has its own treatment in the method chapter: the technical one in
sections {{n:23}} to {{n:26}}, quality in {{n:27}}, economics in {{n:29}}, the
environment in {{n:30}}, certification in {{n:31}} and the decision in {{n:32}}.


The sixth dimension is what sets the program apart from a spreadsheet. The first five
produce **diverging** results: the volume with the largest water saving is rarely the
one with the best financial return, and neither is usually the one with the best
environmental performance. The multi-criteria decision makes explicit the weights given
to each criterion.

---

## What the program does **not** do

Starting with the limits is unusual, and deliberate. It saves the time of anyone who
opened the program expecting something else.

**It does not size the plumbing.** It does not calculate the routing, the diameter of each run or the slope of the network. The pump wizard estimates the diameter and the head loss of the rising main to select the equipment, but it does not replace the plumbing design; the diagram exported in DXF is a diagram, and the construction design belongs to the designer.

**It does not detail the first-flush device.** The program calculates the volume of the first-flush chamber, equal to the catchment area times the depth, and prices it with the leaf separator; the arrangement of the fittings, the purge and the connection to the drainage are separate hydraulic design.

**It does not replace water quality testing.** It sizes treatment equipment from
assumptions. The constants of the roof wash-off model are not calibrated against
measurements, and the resulting quality is an assumption, not a result.

**It does not model an hourly sub-step.** A 40 mm rain in two hours and the same depth
over twenty-four hours give the same result.

**It does not do a complete life cycle inventory.** The assessment is a **screening**
one, in a single impact category — carbon. There is no eutrophication, acidification,
land use or toxicity.

**It does not certify.** It shows where the project would fit. Certification is decided
by the certification body, with the complete documentation of the development.

**It does not know the site.** It does not know whether the volume fits on the plot,
whether the water table is high, or whether the structure can carry the elevated tank.

Section {{n:36}} has the complete list of known limitations, with the consequences of
each one.

---

## Who it is for

The manual serves four reader profiles, with reading paths independent of one another
({{fig:fig27_leitores}}).



![The four reader profiles and the path of each one](../figuras/fig27_leitores.png)

*Figure 99 — The four reading paths of the manual. They are independent of one another, and the manual was organised so that each one can be followed on its own.*

In section numbers: the student follows chapter {{c:2}}, which is the tutorial from start to finish; the designer uses the guides of chapter {{c:3}} and the route of section {{n:3}}; the researcher goes to the method of chapter {{c:4}}; and the reviewer finds in chapter {{c:6}} the verification and the declared limits.


Anyone starting now should go through the whole of chapter {{c:2}}, in the order in
which it is written. It builds a project from scratch and follows it to the final
decision, and each section ends by showing where the project has got to, so that the
reader sees the study taking shape instead of receiving it finished.

---

## What changed from Netuno 4

Netuno 4 is the predecessor, published in 2014 by the same group. Triton keeps the
conceptual model — a daily behavioural balance — and adds six dimensions of analysis
that did not exist.

> **In depth: the two deliberate differences of method.** Anyone comparing results of
> the two versions must declare them.
>
> **The treatment of the first flush.** Netuno 4 treats the depth as an **event
> threshold**: below it nothing is collected, above it the whole rain is collected.
> Triton **subtracts** the depth, which is physically more faithful.
>
> **The optimal volume criterion.** The implementations and the search grids differ.
>
> Together, the two account for 91% of the divergence measured between the programs.
> Over 4,050 reference cases, Triton estimates 2.3 to 2.7 percentage points less
> saving. **With both neutralised, the engine reproduces Netuno 4 with a mean error of
> 0.25 percentage points and 100% of the cases within 5 points.** Section {{n:35}} has
> the complete breakdown.

---

## A word about results

Every number the program produces is **conditional on the declared assumptions**. It
does not discover truths; it calculates consequences.

That is why the manual insists so much on declaration. Section {{n:13}} has the list of
what must appear in a paper, section {{n:33}} has the ten mistakes the program does not
prevent, and section {{n:36}} has what it does not cover.

A study that declares its assumptions and its limits is more useful — and more
defensible — than one that presents a number on its own.
