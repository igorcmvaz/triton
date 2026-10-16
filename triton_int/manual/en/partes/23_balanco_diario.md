# The daily water balance

> By the end of this section you will be able to redo, in a spreadsheet, exactly what
> Triton does on each day of the series, and to say why the program reached the number it
> reached.

> **Before you start.** Chapter {{c:4}} is the technical layer of the manual: it shows the
> calculations from the inside. You do not need it to use the program — chapter {{c:2}} is
> enough — but you do need it to **defend** a result, whether before an examining board, in
> a review or in front of a client who asked where the number came from.

This is the section on which all the others depend. The saving potential, the cash flow, the
avoided emission and the multi-criteria ranking all come from the numbers the daily balance
produces. Whoever understands this section understands the program.

Triton uses a **daily-step behavioural model**: for each day of the precipitation series, the
program works out what enters the tank, what leaves it, what overflows and what stays stored.
There is no probability distribution and no annual mean. There is the series, day after day,
and the same calculation repeated.

---

## The order of operations

For each day `t`, the program always runs, in this order:

1. **decides whether to divert** the first flush, according to the chosen mode;
2. **converts the depth into collected volume**, with the area and the coefficient;
3. **adds it to what was left from yesterday** and checks the overflow;
4. **supplies the rainwater demand** with what is stored;
5. **splits** the supply between indoor use and irrigation;
6. **tops up with mains water** what the rain did not supply;
7. **classifies** the day as one of full, partial or no supply.

The order is not arbitrary, and swapping two steps changes the result. Item {{n:23.4}} returns
to this.

---

## The worked case

Ten days, one house, no upper tank. The numbers were chosen to fit in a spreadsheet.

<!-- inclui: _tabelas/cap23_entrada.md -->

Without outdoor demand, the daily rainwater demand is the indoor demand times the indoor
non-potable fraction, which here coincides with the total suppliable fraction:
200 × 0.40 = **80 L/day**. That is the volume the system tries to deliver every day.

### The table, day by day

<!-- inclui: _tabelas/cap23_dez_dias.md -->

---

## Reading the table

Five things happen in these ten days, and each one teaches a rule of the program.

### Day 1: empty tank

The simulation starts with the tank **empty**. There is no rain on day 1, nothing is stored,
and the 80 L of rainwater demand are not met by a single drop: the day is one of **no**
supply, and the 200 L of the whole day come from the mains.

This is not a defect of the chosen series. It is the initial condition of the model, and it
matters: in short series, the first days penalise the result. With thirty years of series the
effect disappears; with ten days, it is one of the reasons the potential obtained, 25.7%,
falls so far below the suppliable fraction of 40%. Days 3 and 4 add two more days of no supply.

### Days 2 and 3: the first flush at work

On day 2 it rained 2.4 mm. After the 2.0 mm first flush, 0.4 mm remain, which on 100 m² at a
coefficient of 0.85 give 34 L. All 34 L are consumed, and the day is one of **partial**
supply: 34 L of the 80 L wanted.

On day 3 it rained 1.9 mm, less than the first-flush depth of 2.0 mm. The program does not
subtract 1.9 and collect zero: it **diverts the whole day**.

> **Warning.** When the first-flush rule applies and the day's rain does not exceed the depth,
> the **whole** day is lost, not the difference. The calculation is `P_ef = P − d_f` when
> `P > d_f`, and **zero** otherwise.

The reason is physical: the diversion device has to fill before the water reaches the
cistern. If the rain does not fill the device, nothing passes. In climates of light, frequent
rain, this weighs far more than intuition suggests: in the New York series of the tutorial,
17% of the days are below the first-flush depth, and that is why the first-flush mode
deserves attention in section {{n:4}}.

> **A note for those who compare tools.** Some simulation tools treat `d_f` as an **event
> threshold**: below it nothing is collected, above it the **whole** rain is collected, without
> subtraction. Triton subtracts the depth. The difference is deliberate, it lowers the estimated
> saving, and studies comparing the two rules must declare it. Section {{n:35}} deals with the
> comparison.

### Day 5: overflow comes before consumption

It rained 59.8 mm. After the 2.0 mm first flush, 57.8 mm of effective rain remain, which on
100 m² at a coefficient of 0.85 give 4,913 L collected.

The tank was empty. The tank holds 2,000 L, so **2,913 L overflow**. Only after that does the
program withdraw the 80 L of demand, leaving 1,920 L for the next day.

> **Warning.** This order defines the model. The overflow is calculated **before** the demand
> is withdrawn, as in the **YAS** rule (*yield after spillage*), but the day's own rain can
> already supply the day's demand, as in the **YBS** rule. Triton therefore sits between the
> two, and the subsection «YAS, YBS and Triton's order», further on, shows why.
>
> If consumption came before the overflow, the tank would accept water that would physically
> have overflowed already, and the program would overestimate the yield. The difference shows
> up precisely on days of heavy rain, which are those that weigh most in the annual total.

Day 6 follows the same rule: the tank holds 1,920 L, receives 612 L, and 532 L overflow. On day 7
the tank is already full, and 218 L of a 298 L collection overflow.

### Day 8: a tank too small for the event

It rained 32.9 mm, and the system collected 2,626 L. The tank was already at 1,920 L and holds
2,000. **2,546 L overflowed**, nearly the whole collection.

In a single day, the system threw away the equivalent of almost thirty-two days of rainwater
demand. It is the portrait of the mismatch between the rain, which arrives concentrated, and the
demand, which is constant. Enlarging the tank recovers part of it, and that is exactly the
question the volume sweep of section {{n:24}} answers. {{fig:fig01_dez_dias}} sums up the ten
days.

![Collected and overflowed volumes and stored volume over the ten days](../figuras/fig01_dez_dias.png)

*Figure 1 — The ten days of the worked case: (a) collected volume, in blue, and overflowed volume, in orange, by day: on day 8 the overflow almost equals the collection; (b) volume stored in the lower tank at the end of each day, after consumption, with the 2,000 L capacity dashed; on days 5 to 8 the tank reaches capacity, overflows and ends the day with 1,920 L.*

### The sum: the balance closes

The last row of the table and the check table show the closure:

```equacao:fechamento
V_cap = V_ext + V_con + V_res
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_cap` | total volume collected in the period | L |
| `V_ext` | total volume overflowed in the period | L |
| `V_con` | total rainwater volume consumed in the period | L |
| `V_res` | volume left in the tank at the end of the period | L |

In the ten days of the worked case, Equation {{eq:fechamento}} holds with 8,483 L collected,
6,209 L overflowed, 514 L consumed and 1,760 L left.

Zero residual. The program neither creates nor loses water, and this check is made
automatically by the test suite at every change of the code, on ten-year series, with a
residual of the order of 10⁻¹⁴ per cent of the collection.

---

## The equations

The daily balance is written in five chained equations, which the program solves in this
order for each day of the series. The notation follows that of section {{n:4}} for the
collection part, and the index `t` always designates the current day of the simulation, so
that `t−1` is the day immediately before.

### The collected volume

Converting the precipitated depth into volume is the first operation of the day, and the
simplest of all: the effective rain is multiplied by the catchment area and by the surface
runoff coefficient.

```equacao:volume_captado
V_cap,t = P_ef,t × A × C
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_cap,t` | volume collected on day `t` | L |
| `P_ef,t` | effective rain on day `t`, after deducting the first-flush depth | mm |
| `A` | catchment area, in horizontal projection | m² |
| `C` | surface runoff coefficient of the roof | dimensionless |

The result of Equation {{eq:volume_captado}} comes out directly in litres, with no conversion
factor, because one millimetre of depth over one square metre of surface is exactly one litre
of water. It is the only dimensional simplification of the model, and it is exact.

### The overflow and the storage

The volume available before any consumption is the sum of what was left in the tank at the
end of the previous day and what was collected today, as in Equation {{eq:disponivel}}. Two
parts follow from that sum, calculated in this order: the surplus that does not fit in the
tank and therefore overflows, and the volume actually stored.

```equacao:disponivel
D_t = V_res,t−1 + V_cap,t
```

```equacao:extravasado
V_ext,t = max(0 ; D_t − V_max)
```

```equacao:armazenado
V_arm,t = min(D_t ; V_max)
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `D_t` | volume available on day `t`, before consumption | L |
| `V_res,t−1` | volume left in the tank at the end of the previous day | L |
| `V_cap,t` | volume collected on day `t`, from Equation {{eq:volume_captado}} | L |
| `V_ext,t` | volume overflowed on day `t` | L |
| `V_arm,t` | volume stored on day `t`, before consumption | L |
| `V_max` | useful capacity of the lower tank | L |

==The order in which Equations {{eq:extravasado}} and {{eq:armazenado}} appear defines the
model.== The overflow is calculated **before** the day's consumption is withdrawn, and that is
why the program is usually described by the YAS rule, from *yield after spillage*. The
description is approximate, and the next subsection says where it falls short. Reversing the
order would make the tank accept, as consumption, water that would physically have overflowed
already, and would overestimate the yield precisely on days of intense rain, which are those
that weigh most in the annual total.

The difference between the two orders is invisible on most days and decisive on the few that
matter. While the tank does not fill, overflowing before or after consuming gives exactly the
same result, because there is no overflow at all; on days of intense rain, when the tank
reaches capacity, the order determines whether a part of the water is counted as consumed or
as lost. Those are precisely the days that weigh most in the annual total, and that is why a
choice that looks like a formality shifts the whole result. {{fig:fig00f_yas}} compares the
two sequences in the notation of the equations of this section.

![The same rain, two orders of calculation](../figuras/fig00f_yas.png)

*Figure 99 — Sequence of operations of the daily balance: (a) the order adopted by the program, with the overflow calculated before consumption; (b) the reversed order (YBS), with consumption withdrawn before the overflow. The two sequences only diverge on days when the tank reaches capacity, and YBS assumes a consumption before the day's rain, which overestimates the yield.*

### YAS, YBS and Triton's order

In the literature, YAS and YBS have a precise definition (Fewkes and Butler, 2000). With `Y_t`
the volume withdrawn in the day, `Q_t` the collected volume, `S_t` the volume stored at the end
of the day and `V_max` the capacity:

<!-- tabela: Withdrawal of the day and volume stored at the end of the day under strict YAS, strict YBS and in Triton -->
| Rule | Withdrawal of the day | Stored at the end of the day |
| :--- | :--- | :--- |
| strict YAS | `Y_t = min(D_pl,t ; S_t−1)` | `S_t = min(S_t−1 + Q_t − Y_t ; V_max − Y_t)` |
| strict YBS | `Y_t = min(D_pl,t ; S_t−1 + Q_t)` | `S_t = min(S_t−1 + Q_t − Y_t ; V_max)` |
| Triton | `Y_t = min(D_pl,t ; min(S_t−1 + Q_t ; V_max))` | `S_t = min(S_t−1 + Q_t ; V_max) − Y_t` |

Under strict YAS, the day's withdrawal comes only from what was stored the day before:
today's rain only serves tomorrow. Under strict YBS, today's rain supplies the demand before
the tank overflows. Triton does the overflow first, as YAS does, and then lets the day's rain,
up to the capacity, supply the day's demand.

An inequality follows that holds for any series: the volume consumed by Triton is never
smaller than that of strict YAS nor larger than that of strict YBS. The result lies **between
the two**, closer to YAS for large tanks, where the previous day almost always suffices, and
further from it for small ones, where the day's rain weighs. Anyone comparing Triton with a
program or a standard that uses strict YAS should expect from Triton a slightly higher saving potential for the same volume.

The program keeps this order by decision: it keeps continuity with the earlier studies of the
research group, and a change here would shift every published result.

### Supplying the demand

Once it is established how much is in the tank, the program withdraws the smaller of the day's
rainwater demand and the available volume, and passes on to the next day what is left.

```equacao:consumido
V_con,t = min(D_pl,t ; V_arm,t)
```

```equacao:sobra
V_res,t = V_arm,t − V_con,t
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_con,t` | rainwater volume consumed on day `t` | L |
| `D_pl,t` | rainwater demand of day `t`, built as in section {{n:5}} | L |
| `V_arm,t` | volume stored on day `t`, from Equation {{eq:armazenado}} | L |
| `V_res,t` | remaining volume, carried to the next day | L |

Equation {{eq:sobra}} is what makes the daily simulation necessary and irreplaceable: it links
each day to the next and makes the tank a memory of what happened before. No calculation based
on monthly or annual means can represent this chaining, and the whole mismatch between the
concentrated supply and the spread-out demand follows from it.

### The mains top-up

What the rain did not supply is bought from the utility, and that part brings together three
different origins.

```equacao:potavel
V_pot,t = D_pot,t + ΔD_int,t + ΔD_irr,t
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_pot,t` | volume of potable water consumed from the mains on day `t` | L |
| `D_pot,t` | demand that requires potable water by the nature of the use | L |
| `ΔD_int,t` | deficit of the indoor non-potable use, not met by the rain | L |
| `ΔD_irr,t` | irrigation deficit, **only** if the backup supply is on | L |

The third part of Equation {{eq:potavel}} deserves attention because it depends on a user
choice. With the backup supply on, the mains comes to the rescue of irrigation on days when the
cistern runs dry, and the deficit is met with potable water; with it off, the garden is simply
not watered, the building does not buy that water, and the corresponding volume is counted as
**unmet demand**, which is the third part of the demand balance dealt with later in this
section.

### Classifying the day

Finally, each day is classified by the degree of supply achieved, and it is from this
classification that the percentages of days of full, partial and no supply reported in section
{{n:25}} are calculated.

```equacao:classificacao
pleno: V_con,t = D_pl,t ; parcial: 0 < V_con,t < D_pl,t ; nulo: V_con,t = 0
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_con,t` | rainwater volume consumed on day `t` | L |
| `D_pl,t` | rainwater demand of day `t` | L |

In the equation, «pleno», «parcial» and «nulo» are the program's labels for full, partial and
no supply. The comparison of Equation {{eq:classificacao}} is made with a tolerance of
10⁻⁵ L, not by exact equality. The reason is arithmetic, not conceptual: the balance works with
floating-point numbers, and a difference of the order of the rounding error would classify as
partial a day that was fully supplied.

## The demand balance has three parts

The total demand of a day splits into three, not two:

```equacao:demanda_tres
D_t = V_con,t + V_pot,t + V_nao,t
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `D_t` | total demand of the building on day `t` | L |
| `V_con,t` | part supplied with rainwater | L |
| `V_pot,t` | part bought from the mains | L |
| `V_nao,t` | part nobody supplied, that is, unmet demand | L |

The three parts are the rainwater consumption, the mains consumption and the **unmet demand**.
The third is zero in the default configuration, in which the mains comes to the rescue of
irrigation on dry days. It stops being zero when the user switches that rescue off, and then
the program must show it: without it, the balance would close by construction, hiding the water
nobody supplied.

---

## With an upper tank

When the project has an upper water tank, step 4 changes. Instead of consuming directly from
the lower tank, the program:

1. consumes from the upper tank what lies **above the trigger level**;
2. if something is still missing and there is water below, **starts the pump**: it transfers
   the smaller of what is in the lower tank and the free space above, and counts **one cycle**;
3. consumes again from what has just arrived;
4. repeats until the demand is met or the water runs out.

The trigger level is the reserve volume that is not consumed, and it serves to keep the pump
from starting for every litre. It is capped at the volume of the upper tank: entering a trigger
level larger than the tank does not make the program refuse it, it makes it adopt the full tank.

> **The upper tank does not increase the water saving.** It changes **when** the water is
> delivered, not **how much**. What it adds is cost: the investment in the tank and the pump,
> the pumping energy and the associated emission. Section {{n:8}} shows this with numbers.

The number of cycles and the volume pumped come from here and feed the energy calculation of
section {{n:28}}.

---

## What the model does not represent

- **There is no hourly sub-step.** A 40 mm rain concentrated in two hours and the same depth
  spread over twenty-four hours produce the same result. For tanks very small relative to the
  catchment area, this underestimates the overflow.
- **There is no loss by evaporation or leakage** in the tank.
- **The initial condition is an empty tank.** In series shorter than one year, this penalises
  the result noticeably.
- **The runoff coefficient is single and constant.** It does not vary with the intensity of
  the rain or with the time since the last event.
- **In the balance, the first flush is a depth, not a device with its own dynamics.** The
  first-flush chamber is sized and priced by the volume `A × d_f` (section {{n:27}}), but its
  emptying between events is not simulated: the depth is applied according to the chosen
  first-flush mode.

Section {{n:36}} brings together these and the other known limitations.

---

## To check

The worked case of this section is in the file `05_ten_days.triton`, in the cases folder that
comes with the program. Open it, run it, and compare with the printed table.

If any number differs, it is the manual that is out of date relative to the program. And in that
case the automatic check will already have warned, because every number in this table has a
corresponding assertion in the test suite described in section {{n:34}}.
