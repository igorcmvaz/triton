# Economic analysis and tariff regimes

> This section formalises the cash flow and details the six tariff regimes — the data that most
> decides the viability of a rainwater system in Brazil.

---

## The saving is the difference between two bills

The program does not calculate the saving by multiplying the volume saved by a mean tariff, and
the distinction is not one of refinement: it is one of order of magnitude. For each month of the
projection it builds two complete bills, one with the consumption the building would have without
the rainwater system and another with the potable water actually bought, and takes the difference
between them.

```equacao:economia_mensal
E_mês = F(V_tot) − F(V_pot)
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_mês` | saving obtained in the month | R$ |
| `F(·)` | function that calculates the water and sewage bill for a volume | R$ |
| `V_tot` | monthly volume the building would consume without the rainwater system | m³ |
| `V_pot` | monthly volume of potable water actually bought from the mains | m³ |

The reason for proceeding this way lies in the progressiveness of Brazilian tariff structures.
==The cubic metre no longer consumed is always the last one on the bill, which is the most
expensive, and never the mean one.== In a municipality whose first block costs R$ 3.08/m³ and
whose second block costs R$ 14.31/m³, calculating the saving by the mean tariff underestimates it
by more than half, and the error grows with the consumption of the building.

---

## The water and sewage bill

The tariff structure of each municipality is represented in the program by a sequence of blocks,
and each block is a quadruple made up of the minimum volume, the maximum volume, a value and a
code. The code is what gives meaning to the value, because apparently similar structures charge in
very different ways.

Before the codes, it is worth seeing what the bill is made of. The monthly water and sewage bill
is the sum of parts that behave differently: a fixed part, which does not respond to consumption;
one or more consumption blocks, in which the price per volume applies to the volume allocated
within each block; and sewage, which in much of Brazil is a percentage of the water charge and
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

- **The availability charge adds.** A consumption part of R$ 55 plus R$ 46 of availability charge
  gives a bill of R$ 101, and saving R$ 15 of consumption leaves the bill at R$ 86.
- **The floor limits from below.** With a floor of R$ 40 and a billed consumption of R$ 55,
  saving up to R$ 15 **reduces nothing**.

The difference between the two regimes decides whether each cubic metre saved earns a discount
from the first one or whether the saving only starts to count after a threshold is passed, and a
viability study that confuses them reaches inverted conclusions. That is why the program codes the
regime explicitly instead of treating it as a detail of the table.

### The exponential formula

In the CORSAN municipalities the water part is not a sum of blocks but a power of the month's
consumption:

```equacao:exponencial
T_agua = PB × C^n + SB
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `T_agua` | water part of the bill | R$ |
| `PB` | base price of the municipality | R$/m³ |
| `C` | consumption of the month per dwelling unit | m³ |
| `n` | exponent from the Table of Exponents for consumption `C`: 1.00 up to 20 m³, 1.13 between 101 and 150 m³ | dimensionless |
| `SB` | basic service charge | R$ |

The exponent is read from the **total** consumption of the month and applied to the whole volume.
In the residential category there is no cap; only the industrial category, above 1,000 m³, charges
the excess at prices of its own, and the program represents that cap with an ordinary block from
there on. The monthly saving is the difference between the two bills, `PB × (C₁ⁿ¹ − C₂ⁿ²)`, each
consumption with its own exponent, and not the product of a unit price by the volume saved; with
`n` above 1, the cubic metre saved is worth more than the base price.

### Individual metering

In multi-family buildings with individual metering, consumption is evaluated at the level of a
single dwelling unit and the result is multiplied by the number of units. The treatment matters
because of progressiveness: a building of twenty flats treated as a single consumer would fall
entirely into the most expensive block of the table, and the resulting saving would come out
grossly overestimated, because each cubic metre saved would be valued at a tariff none of the
twenty units actually pays.

### Sewage

```equacao:esgoto
T_esg = T_agua × s
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `T_esg` | sewage part of the bill | R$ |
| `T_agua` | water part of the bill, already calculated by the progressive blocks | R$ |
| `s` | sewage percentage charged by the utility | dimensionless |

The sewage percentage applies to the water part of the bill, not to the total bill, and confusing
the two denominators doubles or halves the part calculated. One hundred per cent, the value
charged by many Brazilian utilities, means that the sewage part equals the water part, and
therefore that sewage accounts for half of the total bill.

There is a third mode, CORSAN's: sewage charged **per cubic metre consumed**, `T_esg = C × p_esg`,
without the basic service charge and without the exponent of the water part. Applying the
percentage on the water part there would charge sewage on the basic service and on the power, and
the bill would come out higher than the utility charges.

---

## The six regimes in the database

The catalogue spreads its 652 municipalities very unevenly across the six regimes. The allowance
within the minimum alone accounts for **329** of them, more than half; then come 165 with no
minimum at all, 122 with an availability charge and 34 on the CORSAN exponential formula, whereas
the retroactive allowance appears in only two and the payment floor in none
({{fig:fig33_regimes_base}}). The table below shows how each regime is coded and applied in the
calculation of the bill.

<!-- tabela: Coding and application of each minimum-charge regime in the calculation of the bill -->
| Regime | Coding of the blocks | Calculation of the water part | Effect of reducing consumption |
| :--- | :--- | :--- | :--- |
| no minimum charge | consumption blocks only (code 1 or 0) | sum, in each block, of the price per m³ applied to the volume allocated within it | every reduction in consumption reduces the bill |
| availability charge | fixed value (−1) and consumption blocks from 0 m³, with a positive price | fixed value added to the consumption part, billed from the first m³ | every reduction in consumption reduces the bill; the fixed value remains |
| allowance within the minimum | fixed value (−1) and a first block from 0 to N m³ at R$ 0.00/m³ | fixed value that includes the N m³ of the allowance; above them, consumption blocks | a reduction below N m³ does not change the bill |
| retroactive allowance | allowance (−2) from 0 to N m³ with a fixed value, and consumption blocks | up to N m³, fixed value; above, the whole volume billed from 0 m³ by the blocks | reducing consumption to N m³ or less replaces the consumption part by the fixed value |
| payment floor | floor (−3) and consumption blocks | consumption part by the blocks, limited from below to the value of the floor | a reduction that takes the part below the floor does not reduce the bill |
| exponential formula | basic service (−1), base price (2) and table of exponents (3) covering all consumption | basic service added to `PB × Cⁿ`, with `n` from the whole month's consumption | every reduction in consumption reduces the bill, by the difference between the two powers |

![The municipalities of the catalogue, by minimum-charge regime](../figuras/fig33_regimes_base.png)

*Figure 99 — Distribution of the 652 municipalities of the catalogue among the six tariff regimes. Half of them apply an allowance within the minimum, a regime in which reducing consumption below the allowance does not reduce the bill.*


The payment floor is implemented in the calculation engine and no municipality of the database
has so far been classified under it, a situation recorded here for transparency: the absence of
occurrences does not mean the regime does not exist in the country, only that the survey did not
find it among the 652 municipalities catalogued.

Section {{n:16}} presents the numerical example comparing Floriano and Florianópolis, from which
follows the most important practical lesson of this section: under an allowance regime, saving
water below the allowance volume earns no discount at all on the bill.

---

## The investment

```equacao:capex
CAPEX = C_cist + C_sup + C_mo + C_tub + C_ace + ( C_bomba × n_b ) + CAPEX_inc
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `CAPEX` | total initial investment of the system | R$ |
| `C_cist` | cost of the lower tank | R$ |
| `C_sup` | cost of the upper tank, when there is one | R$ |
| `C_mo` | cost of installation labour: in a new project, 30% of the materials, with a floor of R$ 1,400 | R$ |
| `C_tub` | cost of the piping: pipes, bends and fittings of the 3D layout | R$ |
| `C_ace` | cost of the accessories: the parts of the 3D layout, one by one, and the control cables | R$ |
| `C_bomba` | unit cost of the pump set | R$ |
| `n_b` | number of pump sets, including the standby when there is one | unit |
| `CAPEX_inc` | incremental investment of the treatment line, including the first flush when sized | R$ |

In a new project, `C_tub` and `C_ace` are not allowances: they come from the **bill of quantities
of the 3D layout** (section {{n:22}}). Each metre of pipe, each bend, each end fitting, each part —
valves, check and foot valves, solenoid, water meter, level switches, control panel, inlet
calming device, floating suction, vents, overflow, air gap, point of use — and each metre of
control cable has a price, and the sum is what enters here. Cistern, upper tank and pump set have
terms of their own; the inlet filter and the first flush enter through the treatment line when it
sizes them. The designer can type other values in the economic step; the project then uses the
typed ones, and the audit spreadsheet records the change. Projects saved before this rule keep the
costs they declare.

The labour of a new project is also recalculated at each run: 30% of the sum of cistern, upper
tank, pump sets, piping and accessories, with a floor of R$ 1,400 (key `labor_percentage` of
`costs_database.json`). It thus grows with the tank: in the volume sweep, each volume has its own
cistern, its own usual layout and its own labour. Previously, labour was fixed once, on generic
allowances for piping and accessories, and was the same for all volumes. A value typed in the
economic step prevails, as in the other items.

The last term follows the incremental rule of section {{n:27}} and includes, when the physical
sizing of the first flush is enabled, the first-flush chamber and the leaf separator; the annual
running cost of that subsystem enters the running cost of the treatment line.

Tank prices come from the program's cost database, with the source declared for each material.
When the requested volume is not in the table, the program interpolates linearly between the
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
| pumping energy | section {{n:28}}, with the tariff flag applied |
| chlorination | mass of **product**, not of active chlorine |
| treatment plant | incremental running cost, without counting chlorination twice |
| first flush | annual maintenance of the first-flush chamber and of the leaf separator, when sized |
| declared operating costs | the user's free list |

The tariff flag (*bandeira tarifária*) adjusts the electricity tariff according to the operating
condition of the Brazilian power system, and the program accepts the four current modes: yellow,
red level 1, red level 2 and white, the last with a discount in off-peak periods.

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

*Figure 99 — Cash flow of the tutorial project over twenty years: annual saving on the water and sewage bill and annual costs, with the initial investment in year zero, in nominal values; and cumulative balance discounted at the minimum attractive rate of return, which crosses zero at the payback time of 16.3 years. 4,000 L concrete cistern with an upper tank, as in section {{n:10}}.*

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

The green property tax incentive (*IPTU verde*), when the municipality offers it and the user
enables it, enters the cash flow as an annual saving divided by twelve, which spreads it evenly
over the months of the year. The simplification is deliberate: the discount is granted all at
once, when the tax is assessed each year, but spreading it keeps the cash flow from showing a step
that has nothing to do with the performance of the system.

---

## The indicators

**Net present value:**

```equacao:vpl
VPL = − CAPEX + Σ [ FC_m ÷ ( 1 + TMA )^m ]
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `VPL` | net present value of the investment | R$ |
| `CAPEX` | total initial investment, from Equation {{eq:capex}} | R$ |
| `FC_m` | net cash flow of month `m` | R$ |
| `TMA` | monthly minimum attractive rate of return, as a fraction: 0.5% a month enters as 0.005 | dimensionless |
| `m` | month of the cash flow, from 1 to the end of the analysis period | month |

**Internal rate of return:** the rate that makes the NPV zero. When there is no real root — which
happens when the flow never becomes positive — the program returns null, instead of an invented
number.

**Discounted payback:** the first month in which the discounted cumulative balance crosses zero.

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
