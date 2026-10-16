# Economic analysis and tariff regimes

> This section formalises the cash flow and details the six tariff regimes — the data that most
> decides the viability of a rainwater system.

---

## The saving is the difference between two bills

The program does not calculate the saving by multiplying the volume saved by a mean tariff, and
the distinction is not one of refinement: it is one of order of magnitude. For each month of the
projection it builds two complete bills, one with the consumption the building would have without
the rainwater system and another with the potable water actually bought, and takes the difference
between them.

```equacao:economia_mensal
S_mo = F(V_tot) − F(V_pot)
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `S_mo` | saving obtained in the month | currency |
| `F(·)` | function that calculates the water and sewage bill for a volume | currency |
| `V_tot` | monthly volume the building would consume without the rainwater system | m³ |
| `V_pot` | monthly volume of potable water actually bought from the mains | m³ |

The reason for proceeding this way lies in the structure of the tariff: progressive blocks, a
sewage part that follows the water part, a standing charge that does not respond to
consumption. ==The cubic metre no longer consumed is always the last one on the bill, which is
the most expensive in a progressive tariff, and never the mean one.== In the New York tutorial, the
monthly saving of US$ 24.21 for 4.95 m³ is US$ 4.89 per cubic metre, because each cubic metre
saved earns both the water charge and the sewer charge, which is a percentage of it. Multiplying
the volume saved by the water price alone would understate the saving by more than half.

---

## The water and sewage bill

The tariff structure of each city is represented in the program by a sequence of blocks,
and each block is a quadruple made up of the minimum volume, the maximum volume, a value and a
code. The code is what gives meaning to the value, because apparently similar structures charge in
very different ways.

Before the codes, it is worth seeing what the bill is made of. The monthly water and sewage bill
is the sum of parts that behave differently: a fixed part, which does not respond to consumption;
one or more consumption blocks, in which the price per volume applies to the volume allocated
within each block; and sewage, which is often a percentage of the water charge and
therefore follows everything it does. Saving water affects each of these parts in a different way,
and it is this asymmetry that {{fig:fig07_fatura}} shows.

![The bill broken down into parts, with and without the system](../figuras/fig07_fatura.png)

*Figure 99 — Monthly water and sewage bill of the tutorial project, broken down into parts, without and with the system. The availability charge is identical in both cases; the reduction occurs in the upper consumption blocks, which have the highest price per cubic metre, and extends to sewage, charged as a percentage of the water charge.*

The code of each block defines how its value is applied ({{fig:fig32_codigos}}). In the
consumption blocks, code 1 or 0, the price per volume is charged on the volume allocated within
each block; in the availability charge, code −1, the fixed value is added to the consumption part;
in the retroactive allowance, code −2, consumption above the allowance makes the whole volume be
billed from 0 m³; in the payment floor, code −3, the declared value is the lower limit of the bill;
and in the exponential formula, code 2 holds the base price and the code 3 rows hold the table of
exponents.

![The six tariff block codes](../figuras/fig32_codigos.png)

*Figure 99 — The six tariff block codes and the effect of each one on the monthly water and sewage bill. Two structures with the same numerical values result in different bills depending on the code of each block.*


Two of these regimes are often confused with each other, although they have opposite effects on
the viability of a rainwater system. It is worth examining them with numbers.

- **The availability charge adds.** A consumption part of 55 currency units plus 46 of availability charge
  gives a bill of 101, and saving 15 of consumption leaves the bill at 86.
- **The floor limits from below.** With a floor of 40 and a billed consumption of 55,
  saving up to 15 **reduces nothing**.

The difference between the two regimes decides whether each cubic metre saved earns a discount
from the first one or whether the saving only starts to count after a threshold is passed, and a
viability study that confuses them reaches inverted conclusions. That is why the program codes the
regime explicitly instead of treating it as a detail of the table.

### The exponential formula

Some utilities do not charge water as a sum of blocks but as a power of the month's consumption:

```equacao:exponencial
B_water = PB × C^n + SB
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `B_water` | water part of the bill | currency |
| `PB` | base price | currency/m³ |
| `C` | consumption of the month per dwelling unit | m³ |
| `n` | exponent from the utility's table of exponents for consumption `C`; 1.00 up to a threshold, and rising above it | dimensionless |
| `SB` | basic service charge | currency |

The exponent is read from the **total** consumption of the month and applied to the whole volume.
Where the table ends with a cap, the program represents it with an ordinary block from there on. The
monthly saving is the difference between the two bills, `PB × (C₁ⁿ¹ − C₂ⁿ²)`, each consumption with
its own exponent, and not the product of a unit price by the volume saved; with `n` above 1, the
cubic metre saved is worth more than the base price.

Because the meter bills whole cubic metres and the fraction carries over to the next reading, a
simulation's fractional average consumption is charged along the straight line between the bills of
the two neighbouring integers. Without this rule the exponent would jump inside the cubic metre,
and the value of the cubic metre saved would swing with the decimal place of the average
consumption. None of the three example cities uses this regime.

### Individual metering

In multi-family buildings with individual metering, consumption is evaluated at the level of a
single dwelling unit and the result is multiplied by the number of units. The treatment matters
because of progressiveness: a building of twenty flats treated as a single consumer would fall
entirely into the most expensive block of the table, and the resulting saving would come out
grossly overestimated, because each cubic metre saved would be valued at a tariff none of the
twenty units actually pays.

### Sewage

```equacao:esgoto
B_sew = B_water × s
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `B_sew` | sewage part of the bill | currency |
| `B_water` | water part of the bill, already calculated by the progressive blocks | currency |
| `s` | sewage percentage charged by the utility | dimensionless |

The sewage percentage applies to the water part of the bill, not to the total bill, and confusing
the two denominators doubles or halves the part calculated. One hundred per cent
means that the sewage part equals the water part, and therefore that sewage accounts for half of
the total bill. In New York the percentage is 159%, so that the sewer part is the larger of the two.

There are two more modes: sewage charged **per cubic metre consumed**, `B_sew = C × p_sew`, as
in London, and sewage charged **by blocks of its own on a fraction of the water volume**, as in
Cape Town (70% of the water consumed, four steps). With the exponential formula, the per cubic
metre mode has no basic service charge and no exponent, and applying the percentage on the water
part there would charge sewage on the basic service and on the power.

---

## The six regimes

The program distinguishes six minimum-charge regimes, and which one applies to a building is a fact
about its tariff document, not a choice. The table below shows how each regime is coded and applied
in the calculation of the bill. The three example cities fall in two of them: London and Cape Town
have an availability charge (a standing charge), and New York has a payment floor in the form of a
minimum daily charge, which does not bind at the tutorial consumption. The other three regimes are
supported by the engine and described in section {{n:16}} ({{fig:fig33_regimes_base}}).

<!-- tabela: Coding and application of each minimum-charge regime in the calculation of the bill -->
| Regime | Coding of the blocks | Calculation of the water part | Effect of reducing consumption |
| :--- | :--- | :--- | :--- |
| no minimum charge | consumption blocks only (code 1 or 0) | sum, in each block, of the price per m³ applied to the volume allocated within it | every reduction in consumption reduces the bill |
| availability charge | fixed value (−1) and consumption blocks from 0 m³, with a positive price | fixed value added to the consumption part, billed from the first m³ | every reduction in consumption reduces the bill; the fixed value remains |
| allowance within the minimum | fixed value (−1) and a first block from 0 to N m³ at a zero price | fixed value that includes the N m³ of the allowance; above them, consumption blocks | a reduction below N m³ does not change the bill |
| retroactive allowance | allowance (−2) from 0 to N m³ with a fixed value, and consumption blocks | up to N m³, fixed value; above, the whole volume billed from 0 m³ by the blocks | reducing consumption to N m³ or less replaces the consumption part by the fixed value |
| payment floor | floor (−3) and consumption blocks | consumption part by the blocks, limited from below to the value of the floor | a reduction that takes the part below the floor does not reduce the bill |
| exponential formula | basic service (−1), base price (2) and table of exponents (3) covering all consumption | basic service added to `PB × Cⁿ`, with `n` from the whole month's consumption | every reduction in consumption reduces the bill, by the difference between the two powers |

![The tariff regimes of the example cities](../figuras/fig33_regimes_base.png)

*Figure 99 — Distribution of the example tariffs among the six tariff regimes. The allowance within the minimum is the regime in which reducing consumption below the allowance does not reduce the bill; none of the three example cities has it.*

Section {{n:16}} presents the numerical example that compares an allowance regime with an
availability charge, from which follows the most important practical lesson of this section: under
an allowance regime, saving water below the allowance volume earns no discount at all on the bill.

---

## The investment

```equacao:capex
CAPEX = C_cist + C_sup + C_lab + C_pipe + C_acc + ( C_pump × n_b ) + CAPEX_inc
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `CAPEX` | total initial investment of the system | currency |
| `C_cist` | cost of the lower tank | currency |
| `C_sup` | cost of the upper tank, when there is one | currency |
| `C_lab` | cost of installation labour: in a new project, a percentage of the materials, with a floor | currency |
| `C_pipe` | cost of the piping: pipes, bends and fittings of the 3D layout | currency |
| `C_acc` | cost of the accessories: the parts of the 3D layout, one by one, and the control cables | currency |
| `C_pump` | unit cost of the pump set | currency |
| `n_b` | number of pump sets, including the standby when there is one | unit |
| `CAPEX_inc` | incremental investment of the treatment line, including the first flush when sized | currency |

In a new project, `C_pipe` and `C_acc` are not allowances: they come from the **bill of quantities
of the 3D layout** (section {{n:22}}). Each metre of pipe, each bend, each end fitting, each part —
valves, check and foot valves, solenoid, water meter, level switches, control panel, inlet
calming device, floating suction, vents, overflow, air gap, point of use — and each metre of
control cable has a price, and the sum is what enters here. Cistern, upper tank and pump set have
terms of their own; the inlet filter and the first flush enter through the treatment line when it
sizes them. The designer can type other values in the economic step; the project then uses the
typed ones, and the audit spreadsheet records the change. Projects saved before this rule keep the
costs they declare.

The labour of a new project is also recalculated at each run: a percentage of the sum of cistern,
upper tank, pump sets, piping and accessories, with a floor. In the manual's tutorial the labour is
a round figure of US$ 1,500, illustrative, not a market price. It thus grows with the tank: in the volume sweep, each volume has its own
cistern, its own usual layout and its own labour. Previously, labour was fixed once, on generic
allowances for piping and accessories, and was the same for all volumes. A value typed in the
economic step prevails, as in the other items.

The last term follows the incremental rule of section {{n:27}} and includes, when the physical
sizing of the first flush is enabled, the first-flush chamber and the leaf separator; the annual
running cost of that subsystem enters the running cost of the treatment line.

Tank prices are typed in, as a fixed part plus a price per litre for each material. In the
manual's tutorial the figures are round numbers, illustrative and not market prices: polyethylene
100 plus 0.55 per litre, concrete 600 plus 0.40, fibreglass 120 plus 0.65 and stainless steel 300 plus
2.00, in US$. With them a 4,000 L polyethylene cistern costs US$ 2,300 and a concrete one US$ 2,200;
with the labour, the piping, the accessories and the two pumps, the investment of the tutorial is
US$ 6,250 (illustrative, not a market price). When the requested volume is not in the table, the program interpolates linearly between the
neighbouring points; when the volume exceeds the largest tabulated value, extrapolation is only
done if the regression over the known points has a coefficient of determination above 0.90, and
the program warns when that criterion is not met, instead of extrapolating silently.

---

The make-up of the investment surprises those who come to the subject expecting the tank to
dominate the bill. In small residential volumes it weighs less than labour and piping, and only
comes to dominate when the volume grows enough for the price of the tank to exceed the fixed sum
of the installation. The design consequence is direct: doubling the tank does not double the
investment, and that non-linearity is part of the reason why the net present value curve has an
interior maximum ({{fig:fig21_investimento}}).

![The investment broken down by item, for three volumes](../figuras/fig21_investimento.png)

*Figure 99 — Initial investment broken down into the seven items the program adds up, for three volumes of polyethylene tank. With the costs the tutorial declares, only the lower tank grows with the volume; upper tank, labour, piping, accessories, pump sets and treatment line do not change. The treatment line enters for what it adds beyond the filtering allowance already built into the accessories, so as not to count the filter twice. In a new project, piping and accessories come from the 3D layout, which has no such allowance, and labour follows the materials of each volume.*

---

## The annual running cost

<!-- tabela: Parts of the annual running cost and the origin of each one -->
| Part | Origin |
| :--- | :--- |
| pumping energy | section {{n:28}}, at the electricity tariff entered |
| chlorination | mass of **product**, not of active chlorine |
| treatment plant | incremental running cost, without counting chlorination twice |
| first flush | annual maintenance of the first-flush chamber and of the leaf separator, when sized |
| declared operating costs | the user's free list |

The electricity tariff is typed in, in the currency of the project. In the manual's tutorial it is
US$ 0.20 per kWh, illustrative, not a market price.

---

## The month-by-month projection

The projection is made month by month over the whole analysis period, and applies to each part
the inflation and adjustment factors defined below.

The result of this projection is a monthly series of balances, and what matters in it is the
moment the cumulative balance stops being negative. That moment is the payback time.
{{fig:fig08_fluxo_de_caixa}} aggregates the projection by year: in columns, the saving on the water
and sewage bill and the costs, with the investment in year zero; as a line, the discounted
cumulative balance, which crosses zero at the payback time.

![The discounted cumulative balance over twenty years](../figuras/fig08_fluxo_de_caixa.png)

*Figure 99 — Cash flow of the tutorial project over twenty years: annual saving on the water and sewage bill and annual costs, with the initial investment in year zero, in nominal values; and cumulative balance discounted at the minimum attractive rate of return, which does not cross zero within the twenty years: there is no payback. 4,000 L concrete cistern with an upper tank, as in section {{n:10}}; costs illustrative, not market prices.*

**Inflation applies only to the running cost:**

```equacao:inflacao
f_inf = ( 1 + i )^( m − 1 )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `f_inf` | cumulative inflation factor up to month `m` | dimensionless |
| `i` | declared monthly inflation rate, as a fraction: 0.35% a month enters as 0.0035 | dimensionless |
| `m` | month of the cash flow, counted from 1 | month |

**Tariff adjustments apply only to the bill, in steps:**

```equacao:degraus
k = ⌊ ( m − 1 ) ÷ I ⌋
```

```equacao:reajuste
f_j = ( 1 + r_j )^k
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `k` | number of adjustments already applied up to month `m` | dimensionless |
| `m` | month of the cash flow, counted from 1 | month |
| `I` | interval between adjustments, typically 12 | month |
| `⌊ ⌋` | integer part of the division | — |
| `f_j` | cumulative adjustment factor of part `j` | dimensionless |
| `r_j` | adjustment rate of part `j`, which can be water, sewage or energy | dimensionless |

Equation {{eq:reajuste}} is applied separately to each of the three parts, with rates of their
own, and the following remark is about that separation.

> **Water and sewage are adjusted by separate indices**, not by a single index on the aggregate
> bill. The two parts are the subject of separate acts of the utility, and treating them together
> indexes half the bill by the wrong index.

A tax or fee incentive for rainwater systems, where one exists and the user enters it, can be
added to the cash flow as an annual saving divided by twelve, which spreads it evenly over the
months of the year. The simplification is deliberate: such a discount is usually granted all at
once, but spreading it keeps the cash flow from showing a step that has nothing to do with the
performance of the system. The manual's cases enter no such incentive.

---

## The indicators

**Net present value:**

```equacao:vpl
NPV = − CAPEX + Σ [ CF_m ÷ ( 1 + MARR )^m ]
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `NPV` | net present value of the investment | currency |
| `CAPEX` | total initial investment, from Equation {{eq:capex}} | currency |
| `CF_m` | net cash flow of month `m` | currency |
| `MARR` | monthly minimum attractive rate of return, as a fraction: 0.5% a month enters as 0.005 | dimensionless |
| `m` | month of the cash flow, from 1 to the end of the analysis period | month |

**Internal rate of return:** the rate that makes the NPV zero. When there is no real root — which
happens when the flow never becomes positive — the program returns null, instead of an invented
number.

**Discounted payback:** the first month in which the discounted cumulative balance crosses zero.
When it never does within the analysis period, the program reports «no payback».

**What the tutorial shows.** With the New York tariff and the illustrative costs of the manual, the
tutorial (a 4,000 L concrete cistern with the 1,000 L upper tank) has an investment of US$ 6,250, an
annual saving of US$ 290.53, an annual running cost of US$ 2.63, a net present value of
−US$ 2,919.90 over twenty years, an internal rate of return of −1.23% a year and no payback. These
costs are illustrative, not market prices, and the result is not a verdict on New York; it shows how
the method works and what it takes for a rainwater system to pay for itself. Cheap water is the
reason: a saving of US$ 24.21 a month does not repay US$ 6,250 within twenty years at the minimum attractive rate adopted.
The method is the same where water is dearer or the works cheaper, and the program will show that
as well; enter your own tariff and costs before drawing any conclusion for a real building.

---

## The fragile assumptions

Two of them deserve a sensitivity analysis, and section {{n:20}} shows how.

**The tariff adjustment.** Five per cent a year for twenty years multiplies the tariff by 2.65;
three per cent, by 1.81; seven per cent, by 3.87. The saving of the last years grows in the same
proportion, and that is why the adjustment is among the assumptions that most move the net present
value, as the tornado of section {{n:20}} shows; it is also one of the most uncertain.

**The service life.** Twenty years is the default. A concrete cistern lasts longer; polyethylene
components exposed to the sun last less. The service life enters both the analysis period and the
carbon payback of section {{n:30}}.
