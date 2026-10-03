# What it costs and how fast it pays back

> By the end of this section you will have the twenty-year cash flow, and you will know
> why the **tariff regime of your municipality** decides the feasibility more than any
> parameter of the project.

> **International Edition.** The tutorial is priced in Brazilian reais, with the CASAN
> tariff of Florianópolis. In the International Edition the costs start at zero and the
> tariff is typed in, in the currency of the project; the calculation that follows is the
> same, and so is the lesson about tariff structures.

---

## The saving is the difference between two bills

The most common mistake in the economic analysis of rainwater systems is to multiply the
volume saved by an average tariff. The result is almost never right, and the reason lies
in the structure of Brazilian tariffs — and of many tariffs elsewhere —, which are
progressive by consumption block, as section {{n:16}} details: ==the cubic metre that is
no longer consumed is the last one on the bill, the most expensive, not the average one.==

Netuno avoids the problem by calculating two complete bills — the one the building would
pay without the system and the one it pays with it — and taking the difference between
the two.

<!-- inclui: _tabelas/cap10_economico.md -->

The result deserves attention. The system saves 4.99 m³ per month and the bill falls by
R$ 142.69, which is R$ 28.60 per cubic metre saved — well above the R$ 14.31 of the block
in which consumption fell. The difference has two origins acting together: progressivity,
which makes the saved cubic metre worth the price of the highest block, and sewage, which
in Florianópolis is charged at 100% of the water value and therefore doubles the value of
each cubic metre saved.

> **Sewage is a percentage of the water part, not of the total bill.** One hundred per
> cent of the water means that the sewage part equals the water part, and so sewage is
> half of the bill. Saving water saves both parts, and that is why the effective value of
> the saved cubic metre almost doubles.

---

## The CASAN tariff regime

Florianópolis uses the availability-charge regime, in which the utility charges a fixed
monthly fee of R$ 46.34 that adds to the metered consumption, and charges the progressive
blocks from the first cubic metre consumed.

For a rainwater harvesting project, this is the most favourable configuration there is:
each cubic metre saved produces a discount from the first one, because the fixed fee is
charged for making the network available, not for an included volume. It is still paid,
and it does not prevent the saving on consumption.

Not every municipality adopts this regime, and the difference between them decides the
feasibility of entire projects. The program distinguishes six.

<!-- tabela: The six tariff regimes and the effect of each one on the saving -->
| Regime | What happens when saving | Municipalities in the database |
| :--- | :--- | ---: |
| availability charge | each m³ saved is deducted | 122 |
| exponential formula | each m³ saved is deducted, at the base price raised to the exponent | 34 |
| no minimum | likewise | 165 |
| allowance in the minimum | saving below the allowance **deducts nothing** | 329 |
| retroactive allowance | beyond the allowance, everything from zero is charged | 2 |
| payment floor | the bill does not go below the floor | 0 |

> **Warning, and it is the point that brings down most studies.** In a municipality with
> an **allowance in the minimum** — most of the database, 329 of the 652 — the utility
> charges a fixed value that already includes, say, 10 m³. A house that consumes 12 m³ and
> saves 3 goes down to 9, enters the allowance, and **the bill stops falling**. The system
> saves water and does not save money.
>
> Running that case with the Florianópolis tariff would produce a payback that does not
> exist. Section {{n:16}} teaches how to build the structure of your municipality
> correctly.

---

## The investment

R$ 14,061.19, split as follows:

<!-- tabela: Make-up of the initial investment of the tutorial project -->
| Item | Value |
| :--- | ---: |
| 4,000 L concrete cistern | R$ 5,304 |
| 1,000 L polyethylene upper tank | R$ 460 |
| two half-hp pump sets, duty and standby | R$ 600 |
| labour and excavation | R$ 3,500 |
| piping | R$ 1,200 |
| accessories | R$ 1,800 |
| treatment line, increment | R$ 580 |
| first flush: 300 L chamber and leaf separator | R$ 617 |

Tank prices come from the program's database, which has values by volume and by material,
with a declared source. For volumes outside the table, the program interpolates; it only
extrapolates beyond it if the regression has an R² above 0.90, and warns when it does not.

**The first-flush chamber.** The first flush is not only the depth subtracted from the
rain: it is a physical component, with a cost. Step **3. Quality & Treatment** sizes it by
default, and in the tutorial the 2 mm depth over 150 m² needs a 300 L chamber, which with
the leaf separator costs R$ 616.90 of investment and R$ 40 per year of running cost.
Without it, the investment would be R$ 13,444.29, the net present value R$ 4,032 and the
discounted payback 14.8 years: leaving out the first flush brings the payback forward by
a year and a half, and that is why a study that leaves it out looks more feasible than the
system that gets built. Section {{n:27}} details the sizing.

---

## The result

<!-- tabela: Economic indicators of the tutorial project over twenty years -->
| Indicator | Value |
| :--- | ---: |
| net present value | R$ 2,745 |
| internal rate of return | 7.54% per year |
| discounted payback | 16.3 years |

The project pays for itself, but only just. It returns 7.5% per year against a minimum
rate of 6.2%, and pays back the investment in the seventeenth year of twenty. What
sustains it is the Florianópolis tariff, which is high, and sewage at 100%; what squeezes
it is the 28% fraction, which limits the saving to less than five cubic metres a month,
and the concrete cistern, which is the most expensive per litre after stainless steel.
Section {{n:11}} shows that changing the material changes the account.

**The running cost is small:** R$ 48.82 per year, of which R$ 3.45 of chlorine tablets,
R$ 40 of first-flush maintenance and R$ 5.36 of pumping energy, the 7.7 kWh per year of
section {{n:8}}. The energy comes from the same function that feeds the environmental
assessment, according to the arrangement declared in step **4. Reservoir & Costs**:
pumping to an upper tank, direct pressurisation or gravity.

---

The result of an isolated volume says little without its neighbours. The economic tab
repeats the calculation for all the volumes of the sweep and plots the curve, and it is
there that you can see whether the technical optimum and the economic optimum fall in the
same place ({{fig:fig49_programa_vpl}}).

![The net present value against the tank volume](../figuras/fig49_programa_vpl.png)

*Figure 99 — The chart of the economic tab: the net present value of each volume of the sweep, with a concrete cistern, with the economic maximum and the technical optimum marked. When the two coincide, the program marks them with a single symbol. Figure generated by the program itself.*

---
## What the projection assumes

Twenty years is a long time, and the projection depends on assumptions worth declaring:

<!-- tabela: Assumptions of the economic projection and the weight of each one in the result -->
| Assumption | Value adopted | Where it weighs |
| :--- | ---: | :--- |
| minimum attractive rate of return | 0.5% per month | discounts the flow; the higher, the worse the NPV |
| cost inflation | 0.35% per month | applies only to the running cost |
| water tariff escalation | 5% per year | applies to the saving |
| sewage tariff escalation | 5% per year | likewise, and indexed separately |
| escalation interval | 12 months | in steps, not continuously |
| analysis period | 20 years | minimum design life of the plumbing system, Table 25 of ABNT NBR 15575-1:2025 |

> **The water and sewage escalations are separate**, not a single index on the aggregate
> bill. The two parts are adjusted by different acts of the utility, and treating them
> together indexes half of the bill by the wrong index.

The tariff escalation is the most fragile assumption of the list. Five per cent a year
for twenty years multiplies the tariff by 2.65. If the real tariff rises more than that,
the project returns more; if it rises less, it returns less. A serious study declares the
value adopted and shows the sensitivity — section {{n:20}} teaches how.

---

## What we have so far

<!-- tabela: State of the tutorial project after the economic analysis -->
| Project so far | |
| :--- | ---: |
| volume | 4,000 L, concrete |
| arrangement | pumping to a 1,000 L upper tank |
| investment | R$ 14,061 |
| annual saving | R$ 1,712 |
| NPV over 20 years | R$ 2,745 |
| payback | 16.3 years |

Money says yes, with no margin.

It remains to hear the carbon. And it will disagree.
