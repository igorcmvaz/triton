# What it costs and how fast it pays back

> By the end of this section you will have the twenty-year cash flow, and you will know
> why the **tariff structure of your water utility** decides the feasibility more than any
> parameter of the project.

> **Costs in this manual are illustrative.** The International Edition carries no price
> list. Every cost in the tutorial is a round number, in US dollars, chosen so that you
> can follow the method; it is **illustrative, not a market price**. The tariff is the
> exception: it is the New York water and sewer tariff stored in the example project. In
> your own study, type your quotations, your tariff and your currency in the economic
> step. The calculation that follows is the same, and so is the lesson about tariff
> structures.

---

## The saving is the difference between two bills

The most common mistake in the economic analysis of rainwater systems is to multiply the
volume saved by an average tariff. The result is often wrong, and the reason lies in the
structure of tariffs, which in many places are progressive by consumption block, as
section {{n:16}} details: ==the cubic metre that is no longer consumed is the last one on
the bill, the most expensive, not the average one.== Sewerage charges add a second
effect, as the New York tariff shows below.

Triton avoids the problem by calculating two complete bills — the one the building would
pay without the system and the one it pays with it — and taking the difference between
the two.

<!-- inclui: _tabelas/cap10_economico.md -->

The result deserves attention. The system saves 4.95 m³ per month and the bill falls by
US$ 24.21, which is US$ 4.89 per cubic metre saved. That is 2.59 times the water charge
of US$ 1.89 per cubic metre, and the difference is the sewer: New York charges sewerage
at 159% of the water charge, so each cubic metre that is not drawn from the mains is not
discharged either.

> **Sewage is a percentage of the water part, not of the total bill.** A sewer charge of
> 159% of the water means that the sewer part is 1.59 times the water part, so the sewer
> is more than three fifths of the bill. Saving water saves both parts, and that is why
> the effective value of the saved cubic metre is well above the water rate.

---

## The New York tariff regime

New York charges the water by volume at a single rate from the first cubic metre
consumed (US$ 5.35 per hundred cubic feet, the rate recorded in the example project from
the New York City Water Board), adds the sewer at 159% of that charge, and applies a
minimum daily charge that does not bind at this house's consumption.

For a rainwater harvesting project, this is a favourable structure: each cubic metre
saved produces a discount from the first one. It is not progressive, so the saved cubic
metre is worth the average one, which is why the value per cubic metre above is simply
the water rate times 2.59. Cape Town, in section {{n:14}}, has stepped blocks, and there
the cubic metre saved is worth the price of the highest block the house reaches.

Not every utility works like this, and the difference between them decides the
feasibility of entire projects. The program distinguishes six regimes.

<!-- tabela: The six tariff regimes and the effect of each one on the saving -->
| Regime | What happens when saving |
| :--- | :--- |
| availability charge | each m³ saved is deducted |
| exponential formula | each m³ saved is deducted, at the base price raised to the exponent |
| no minimum | likewise |
| allowance in the minimum | saving below the allowance **deducts nothing** |
| retroactive allowance | beyond the allowance, everything from zero is charged |
| payment floor | the bill does not go below the floor |

> **Warning, and it is the point that brings down most studies.** Where the utility
> charges a fixed value that already includes an **allowance**, say 10 m³, a house that
> consumes 12 m³ and saves 3 goes down to 9, enters the allowance, and **the bill stops
> falling**. The system saves water and does not save money.
>
> Running that case with an average tariff would produce a payback that does not exist.
> Section {{n:16}} teaches how to build the structure of your own utility correctly.

---

## The investment

US$ 6,250, split as follows (every value illustrative, not a market price):

<!-- tabela: Make-up of the initial investment of the tutorial project (illustrative, not a market price) -->
| Item | Value (illustrative, not a market price) |
| :--- | ---: |
| 4,000 L concrete cistern | US$ 2,200 |
| 1,000 L polyethylene upper tank | US$ 650 |
| two half-hp pump sets, duty and standby | US$ 500 |
| labour and excavation | US$ 1,500 |
| piping | US$ 600 |
| accessories | US$ 800 |
| **total** | **US$ 6,250** |

The tank prices follow a simple illustrative rule, a fixed part plus a part per litre,
different for each material: polyethylene 100 + 0.55 per litre, concrete 600 + 0.40,
glass fibre 120 + 0.65 and stainless steel 300 + 2.00. A 4,000 L concrete cistern is
therefore 600 + 1,600 = 2,200. These are not catalogue prices, and **the program does not
apply this rule**: it is the way the author arrived at the figures typed into the tutorial
project. In a real study you replace them with quotations.

**The first-flush chamber.** The first flush is not only the depth subtracted from the
rain: it is a physical component, with a cost. Step **3. Quality & Treatment** sizes it by
default, and in the tutorial the 2 mm depth over 150 m² needs a 300 L chamber. In this
illustrative budget its cost sits inside the accessories line. A study that leaves the
first flush out of the budget, while subtracting it from the rain, looks more feasible
than the system that gets built. Section {{n:27}} details the sizing.

---

## CAPEX in this edition: what you enter and what the program calculates

The International Edition carries no price list, so **it does not calculate an investment from
prices**. It sizes the system, calculates the saving on the bill, the pumping energy and the
quantity of chlorine, and multiplies those quantities by the prices you type. The investment is
the sum of the values you enter. Nothing in the cost chain is filled in on your behalf, and no
price was invented to fill the gap.

The table shows what a new project contains, read from the program.

<!-- tabela: What a new project of the International Edition contains, and what is left for you to enter -->
| Field of the new project | Starting value | What it means |
| :--- | ---: | :--- |
| lower tank (cistern) and upper tank | 0.00 | to be entered by you |
| piping, accessories and labour | 0.00 | to be entered by you |
| price of each pump set | 0.00 | to be entered by you; the project starts with 2 pump sets, duty and standby |
| electricity tariff | 0.0000 per kWh | to be entered by you; with no tariff, the pump energy costs nothing |
| water and sewer tariff | none | to be entered by you (section {{n:16}}); with no tariff, the bill is zero |
| price of chlorine | 0.00 per kg | to be entered by you; with no price, chlorine costs nothing |
| maintenance routines | 3 routines, every 12 months, 0.00 in total | the names stay as a checklist; the costs are yours |
| automatic budget of the 3D layout | off | the program does not price the parts of the layout |
| automatic labour | off | the program does not estimate labour as a share of the materials |
| catalogue prices (tanks, treatment line) | off | the treatment line is sized but adds no cost |
| chlorine dose and tablet purity | 1.5 mg/L and 65% | technical parameters, not prices |
| minimum attractive rate of return | 2.0% per month | generic starting value of the program, not data of any country |
| cost inflation | 0.2% per month | likewise |
| escalation of the water, sewer and electricity tariffs | 5.0%, 5.0% and 5.0% per year | likewise |
| analysis period | 20 years | the service life adopted; declare and justify it |

**What this means for you.** Without your values the investment is zero, and the economic
analysis shows only the saving on the water bill, and only after you enter a tariff. The net
present value and the payback, in those conditions, say little: they are not results. The treatment
line and the first flush are sized, and enter the carbon balance, but they cost nothing until you
price them in the investment. You have an economic analysis when you enter real quotations and the
tariff you pay.

The internal cost file (`costs_database.json`) exists in every edition of the program, but in
this one it holds only the structure: no prices, no currency and no regional factors. No
calculation uses it; the costs are the ones you enter.

### How to enter your values

In step **4. Reservoir & Costs**, the button *1. Initial Investment (CAPEX)* has fields for the upper
tank, labour, piping and accessories; the button *2. Motor Pump & Energy Cost* has the price of the
pump set and the electricity tariff; the button *3. Other Operational Costs* has the maintenance
routines; and the button *4. Water and Sewage Tariffs* has the tariff. Enter the values of your
own quotations, with the taxes you will pay if the investment is borne by the final consumer, in
the currency of the project.

Three limitations of this version are worth knowing.

- **The cistern price has no field in the CAPEX dialog.** On confirming, the dialog sets that price
  back to zero. Until it is corrected, add the price of the cistern to one of the lines of the dialog,
  for example the accessories, and say so in the report; or write the value in the field
  `cost_lower_tank` of the block `capex_and_opex` of the project file, and do not confirm the CAPEX
  dialog afterwards.
- **One cistern price serves every volume of the sweep.** With no price list, the program cannot
  scale the price with the volume: the price you enter is used as it stands for each volume
  analysed, and in the volume sweep for all of them. The net present value curve against the volume
  ({{fig:fig49_programa_vpl}}) then shows how the saving changes with the volume against a fixed
  cistern price. To compare volumes on cost, run the project once per volume, each with its own
  quotation.
- **The price of chlorine has no field in the interface.** It exists only in the project file, in
  the block `water_quality_and_etap`, as `chlorine_cost_per_kg`. Alternatively, add in *3. Other
  Operational Costs* a routine with a variable cost per cubic metre of rainwater.

---

## The result

The second table above gives the indicators.

**The project does not pay for itself, and that is the honest result.** Over twenty years,
with these illustrative costs and the New York tariff, the net present value is
−US$ 2,919.90, the internal rate of return is −1.23% per year, and there is no discounted
payback within the period. We did not adjust the costs until a payback appeared.

The reason is not a defect of the example. Water is cheap in New York relative to what a
tank, two pumps and the labour cost, and the 28% fraction limits the saving to less than
five cubic metres a month, US$ 290.53 a year. A tariff that rewards the cubic metre more,
a larger suppliable fraction or a cheaper installation changes the account, and section
{{n:20}} varies each of these in turn. It also shows that none of the assumptions tested,
taken alone, produces a payback in this case. Only the tutorial carries costs, so
section {{n:14}} compares the three cities on saving potential, not on payback.

**The running cost is small:** US$ 2.63 per year, of which US$ 1.54 is pumping energy, the
7.7 kWh per year of section {{n:8}} at an illustrative US$ 0.20 per kilowatt-hour, and US$ 1.10
is chlorine, 0.14 kg of product per year at an illustrative US$ 8 per kilogram. The
energy comes from the same function that feeds the environmental assessment, according to
the arrangement declared in step **4. Reservoir & Costs**: pumping to an upper tank,
direct pressurisation or gravity. This figure does not include the three maintenance routines of
US$ 90 per year, which enter the cash flow separately; the next section shows how much they weigh.

---

The result of an isolated volume says little without its neighbours. The economic tab
repeats the calculation for all the volumes of the sweep and plots the curve, and it is
there that you can see whether the technical optimum and the economic optimum fall in the
same place ({{fig:fig49_programa_vpl}}).

![The net present value against the tank volume](../figuras/fig49_programa_vpl.png)

*Figure 99 — The chart of the economic tab: the net present value of each volume of the sweep, with the economic maximum and the technical optimum marked. When the two coincide, the program marks them with a single symbol. All costs are illustrative, not market prices. Figure generated by the program itself.*

---

## What goes into the running cost (OPEX)

Here too the program fills in no price. The running cost of a new project adds the energy of the
pump, the chlorine, the cost of the treatment line and the maintenance routines, and **every
one of those prices starts at zero**: the electricity tariff, the price of chlorine and the cost of
each routine. The three routines exist as a checklist, with a period of 12 months, and you give
them a cost.

<!-- tabela: Where each part of the running cost comes from in the International Edition -->
| Part of the running cost | What the program calculates | What you supply | Illustrative in the tutorial |
| :--- | :--- | :--- | :--- |
| pump energy | the annual energy of the pump set, from the chain of section {{n:28}} | electricity tariff, taxes on it, annual escalation | US$ 0.20 per kWh |
| chlorine | the kilograms of product per year, from the dose, the purity of the tablet and the rainwater volume used | price per kilogram (project file only) | US$ 8 per kg |
| treatment line | the sizing: class, disinfection, filter, first-flush chamber | the price of the equipment, inside the investment | none: catalogue prices are off |
| maintenance routines | the month in which each falls due (every 12 months, from month 12) | a fixed cost and, if you wish, a cost per cubic metre | US$ 20, 40 and 30 per year |

The program calculates only the **quantities**: the annual energy of the pump set, by the chain of
section {{n:28}}, and the kilograms of chlorine, by the dose and the purity of the tablet. The cost is
the quantity times the price you enter. With a price of zero the cost is zero, and not a
figure left out.

**The routines weigh more than the rest.** The annual running cost that the summary of the analysis
shows adds only the energy, the chlorine and the treatment line. The routines enter the cash flow
separately, in months 12, 24, 36 and so on, corrected for inflation. In the tutorial, with illustrative
values, they move the result:

<!-- tabela: Effect of the three illustrative maintenance routines on the running cost in the summary and on the result of the tutorial (illustrative costs, not market prices) -->
| Tutorial project (illustrative costs, not market prices) | With the routines | Without the routines |
| :--- | ---: | ---: |
| maintenance routines per year | US$ 90.00 | US$ 0.00 |
| annual running cost in the summary: energy, chlorine and treatment | US$ 2.63 | US$ 2.63 |
| net present value | −US$ 2,919.90 | −US$ 1,509.27 |

**Energy.** The electricity tariff starts empty. Use your own bill. The tutorial's US$ 0.20 per
kilowatt-hour is a round number chosen to follow the method, not a tariff of any country.

**What does not enter.** The cash flow has no replacement of equipment over the 20 years, no
residual value, no laboratory analysis of the water and no insurance. If the pump or the filter is
replaced within the period, add the replacement as a routine in *3. Other Operational Costs*.

**How to change or switch off.** Routines are edited, deleted or added with the button *3. Other
Operational Costs*. Set the cost of a routine you do not want to zero rather than deleting every
routine: with an empty list, the economic step may restore a starting list whose costs are
reference values of the program's internal file, not yours. The dose of chlorine and the physical
first flush are chosen in step **3. Quality & Treatment**. The electricity tariff and its taxes are in
*2. Motor Pump & Energy Cost*.

---
## What the projection assumes

Twenty years is a long time, and the projection depends on assumptions worth declaring:

<!-- tabela: Assumptions of the economic projection and the weight of each one in the result -->
| Assumption | Value adopted | Where it weighs |
| :--- | ---: | :--- |
| minimum attractive rate of return | 0.4% per month | discounts the flow; the higher, the worse the NPV |
| cost inflation | 0.2% per month | applies only to the running cost |
| water tariff escalation | 3% per year | applies to the saving |
| sewage tariff escalation | 3% per year | likewise, and indexed separately |
| escalation interval | 12 months | in steps, not continuously |
| analysis period | 20 years | the service life adopted; declare and justify it |

All of these values are illustrative choices of the tutorial, not data of any country.

> **The water and sewage escalations are separate**, not a single index on the aggregate
> bill. The two parts are often adjusted by different decisions of the utility, and
> treating them together indexes part of the bill by the wrong index.

The tariff escalation is the most fragile assumption of the list. Three per cent a year
for twenty years multiplies the tariff by 1.81. If the real tariff rises more than that,
the project returns more; if it rises less, it returns less. A serious study declares the
value adopted and shows the sensitivity — section {{n:20}} teaches how.

---

## What we have so far

<!-- tabela: State of the tutorial project after the economic analysis (illustrative, not a market price) -->
| Project so far (illustrative, not a market price) | |
| :--- | ---: |
| volume | 4,000 L, concrete |
| arrangement | pumping to a 1,000 L upper tank |
| investment | US$ 6,250 |
| annual saving | US$ 290.53 |
| NPV over 20 years | −US$ 2,919.90 |
| payback | none within 20 years |

Money says no.

It remains to hear the carbon. And it will not simply agree.
