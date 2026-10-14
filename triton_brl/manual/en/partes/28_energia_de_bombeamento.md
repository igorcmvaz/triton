# Pumping energy

> This section gives the complete chain from the shaft to the socket, and explains why the
> nameplate power is **not** what the meter records.

Three versions of this calculation have existed in the program, and the first two made the mistakes
described in the item «Why the complete chain matters»: treating the nameplate power as electrical
power and deducting the pump efficiency twice. Anyone reading a study made with an old version needs
to know this.

---

## Nameplate power is shaft power

ABNT NBR 17094-2:2016 requires the **efficiency** to be marked on the motor's nameplate, as a
quantity separate from the power. That only makes sense if the nameplate power is the mechanical
power **at the shaft**.

Hence the chain has two efficiencies, not one:

<!-- tabela: The two efficiencies of the pumping chain and what each one converts -->
| Efficiency | What it converts |
| :--- | :--- |
| **of the pump**, `η_b` | shaft power into hydraulic power delivered to the water |
| **of the motor**, `η_m` | electrical power from the socket into mechanical power at the shaft |

The program asks for both, in separate fields.

---

## The equations

**Specific pumping energy**, per cubic metre lifted:

```equacao:energia_especifica
e = ( ρ × g × H ) ÷ ( η_b × η_m )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `e` | specific energy consumption per volume pumped | kWh/m³ |
| `ρ` | density of water, taken as 1,000 | kg/m³ |
| `g` | acceleration of gravity, taken as 9.81 | m/s² |
| `H` | total manometric head of the pumping | m head |
| `η_b` | hydraulic efficiency of the pump | dimensionless |
| `η_m` | efficiency of the electric motor | dimensionless |

==Equation {{eq:energia_especifica}} does not depend on the flow rate or the installed power.==
Lifting one cubic metre of water to a given height costs the same energy with a large or a small
pump, because the work done is the same; what changes with the power is the time taken to do it, not
the specific consumption.

**When the operating flow rate is declared**, the equivalent form:

```equacao:energia_por_vazao
e = P ÷ ( Q × η_m )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `e` | specific energy consumption per volume pumped | kWh/m³ |
| `P` | nameplate power of the pump set, which is shaft power | kW |
| `Q` | pumping flow rate entered or deduced | m³/h |
| `η_m` | efficiency of the electric motor | dimensionless |

The hydraulic efficiency of the pump does not appear in Equation {{eq:energia_por_vazao}}, and the
absence is deliberate: it is already built into the fact that a motor of `P` kilowatts at the shaft
makes the pump deliver `Q` cubic metres per hour at that head. Dividing by it again would count the
hydraulic loss twice.

**Flow rate, when not declared:**

```equacao:vazao_deduzida
Q = ( P × η_b ) ÷ ( ρ × g × H )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `Q` | deduced pumping flow rate | m³/h |
| `P` | nameplate power of the pump set, which is shaft power | kW |
| `η_b` | hydraulic efficiency of the pump | dimensionless |
| `ρ` | density of water, taken as 1,000 | kg/m³ |
| `g` | acceleration of gravity, taken as 9.81 | m/s² |
| `H` | total manometric head of the pumping | m head |

**Energy of the start-ups:**

```equacao:energia_partida
E_part = ( P × t_part ) ÷ η_m
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_part` | energy consumed by all the start-ups of the period | kWh |
| `P` | nameplate power of the pump set, which is shaft power | kW |
| `t_part` | total start-up time accumulated in the period | h |
| `η_m` | efficiency of the electric motor | dimensionless |

The pump efficiency is absent from Equation {{eq:energia_partida}} for the physical reason that
distinguishes it from the previous ones: during start-up there is no useful flow, and therefore no
hydraulic loss to deduct. The motor draws energy from the socket, and that is all the utility's meter
records.

The annual energy of the pump set is the sum of the two parts: that of the actual pumping, which
depends on the volume lifted, and that of the start-ups, which depends on the number of starts.

```equacao:energia_anual
E_ano = e × V_rec + ( P × t_part ) ÷ η_m
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_ano` | electrical energy consumed by the pump set in the year | kWh/year |
| `e` | specific energy consumption per volume pumped | kWh/m³ |
| `V_rec` | volume pumped in the year | m³/year |
| `P` | nameplate power of the pump set, which is shaft power | kW |
| `t_part` | total start-up time accumulated in the year | h/year |
| `η_m` | efficiency of the electric motor | dimensionless |

---

The nameplate power of a pump set is the mechanical power at the shaft, not the electrical power
recorded by the meter ({{fig:fig00k_energia}}). A 0.5 hp (0.37 kW) pump set with a motor of 60.5%
efficiency draws about 0.61 kW from the mains: calculating the energy with the nameplate power would
underestimate consumption by about 40%, and the energy running cost is precisely the part that
reduces the saving of the system.

![The chain of efficiencies between the socket and the lifted water](../figuras/fig00k_energia.png)

*Figure 99 — Energy chain of pumping. The nameplate power is the power at the shaft, in the middle of the chain: between it and the energy meter is the motor efficiency, η_m, and between it and the hydraulic power delivered to the water is the pump efficiency, η_b.*

The hydraulic power depends on the manometric head, which adds the head losses of the flow to the
geometric difference in level between the water surfaces ({{fig:fig00l_manometrica}}). Head loss is
the energy dissipated per unit weight of fluid and has two parts: the continuous loss, along the
pipe, given by the Darcy-Weisbach equation, `h_f = f · (L/D) · v²/2g`, where `f` is the friction
factor, `L` the length, `D` the internal diameter and `v` the mean velocity; and the local losses in
fittings, valves and bends, `h_loc = K · v²/2g`, where `K` is the coefficient of the singularity. In
short building rising mains, the losses typically add 10% to 30% of the geometric difference in
level.

![The manometric head broken down into level difference and losses](../figuras/fig00l_manometrica.png)

*Figure 99 — (a) Manometric head of a building rising main: geometric difference in level between the water surfaces of the cistern and the upper tank, plus the head losses; (b) energy line along a stretch of pipe, with the continuous friction loss (h_f) and the local losses at a valve and an elbow (h_loc).*

---

## The motor efficiency, when not entered

Table 13 of ABNT NBR 17094-2:2016 applies, line IR1, two-pole motors — which is what residential pump
sets are, at 3,450 rpm ({{fig:fig31_motores}}):

![The efficiency of induction motors by power and class](../figuras/fig31_motores.png)

*Figure 99 — Minimum efficiency of two-pole single-phase induction motors, according to Table 13 of ABNT NBR 17094-2:2016. The program adopts class IR1 when the project does not enter the efficiency, as the least demanding and therefore the conservative assumption.*


The two values that appear most in building installations are those of half a horsepower, with
**60.5%** efficiency in class IR1, and of one horsepower, with **69.3%**. The difference between them
is almost nine percentage points, and it carries over entirely to the energy running cost, because it
is the efficiency that separates the shaft power from the power actually drawn from the mains.

**IR1** is adopted because it is the normative floor and what is found in off-the-shelf pump sets.
Anyone with a high-efficiency motor enters the value marked on the nameplate.

For powers not in the table, the standard says to adopt the larger of the two neighbouring
efficiencies when the power is at the midpoint or above, and the smaller when it is below.

---

## Why the complete chain matters

The specific consumption of the reference case — half a horsepower, 12 m of manometric head, 82 m³
pumped and 98 starts per year — is 0.1080 kWh/m³. ==Ignoring the motor efficiency, or deducting the
pump efficiency twice, changes that number by tens of percentage points,== and those are precisely the
two most frequent mistakes in sizing spreadsheets.

The first mistake is to treat the nameplate power as the power consumed at the socket; the second, to
apply the hydraulic efficiency in a calculation that already starts from the flow actually delivered,
which counts it twice. The chain presented in this section is explicit precisely to make both visible.

---

## The pump sizing wizard

When the power, flow rate and manometric head of the pump set are not known, the *Pump Sizing Wizard*
button, in step **4. Reservoir & Costs** and in the economic dialog, estimates the three values and
selects a commercial model. The wizard follows the usual sizing sequence of a building rising main:

1. **Pumping flow rate.** `Q = V_sup ÷ t_ench`, with the volume of the upper tank and the desired
   filling time, 45 minutes by default.
2. **Economic diameter.** By Forchheimer's formula, `D = 1,3 · (t_op ÷ 24)^0,25 · √Q` (1.3 and 0.25
   in decimal-point notation), with `D` in metres, `Q` in m³/s and `t_op` the daily operating time,
   2 h by default. The diameter adopted is the smallest commercial solvent-weld PVC pipe whose internal
   diameter meets the calculated value, and never smaller than the outlet of the selected pump set;
   the suction gets one commercial size above the delivery.
3. **Velocity.** `v = Q ÷ (π · D_i² ÷ 4)`, highlighted when it falls outside the range of 0.6 m/s to
   2.5 m/s.
4. **Head loss.** By the Hazen-Williams formula, `J = 10,643 · Q^1,852 · C^−1,852 · D_i^−4,87`, with
   `C = 140` for PVC, multiplied by the length of the piping and increased by 30% for the local losses.
5. **Manometric head and power.** `H_man = H_geo + h_f` and `P = ρ · g · Q · H_man ÷ η`, with a set
   efficiency of 55% by default.
6. **Selection.** The first model of the internal catalogue whose flow rate, maximum head and power
   meet the operating point, with the pump curve plotted against the calculated point.

The calculated manometric head and head loss go back to the project and feed the energy calculation of
this section, in place of the fallback value.

---

## The fallback values

Used when the project does not declare them:

<!-- tabela: Fallback values adopted when the project does not declare them -->
| Parameter | Value | Origin |
| :--- | ---: | :--- |
| manometric head | 12 m head | two-storey house with a buried cistern: ~8 m of geometric level difference and ~30% of head loss give 10 to 12 m; the conservative end is adopted |
| pump efficiency | 55% | residential pump sets from half to one horsepower lie between 40% and 60% at the operating point |
| start-up time | 108 s | see the caveat below |

> **In depth: the manometric head is the parameter that weighs most.** Anyone who knows the project's
> level difference should enter it. Doubling the head doubles the energy.

> **In depth: the 108 s start-up time.** It represents the priming time of a self-priming pump whose
> suction line has drained. In an installation with a foot valve in working order, the line stays
> primed and the following starts are immediate. In the reference case, start-ups account for 19% of
> the annual consumption; with a 3 s transient, they would account for 0.5%. The value is
> conservative and is recorded as an open issue of the program.

---

## Direct pressurisation: the energy is time switched on

Everything said so far applies to pumping to a tank, in which the pump fills the upper tank in one go,
at its own flow rate, and switches off. The pressure pump works another way. It starts at each flush
and stays on while the toilet cistern fills, and it is the cistern's float valve, not the pump, that
decides the flow. A larger pump does not fill the cistern faster: it stays on for the same time,
drawing more power.

That is why the program does not calculate the energy of the pressure pump by the specific energy
`ρ·g·H/(η_b·η_m)`, which assumes the pump at its best-efficiency point. It calculates it by the time
switched on:

```equacao:energia_pressurizador
E = (P ÷ η_m) · [V ÷ min(Q_b(H), Q_p) + N · t_r]
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E` | annual energy of the pressure pump | kWh/year |
| `P` | nameplate power, at the shaft | kW |
| `η_m` | motor efficiency, from Table 13 of ABNT NBR 17094-2 | dimensionless |
| `V` | rainwater volume consumed | m³/year |
| `Q_b(H)` | flow rate of the model's curve at the working pressure `H` | m³/h |
| `Q_p` | flow rate of the point of use | m³/h |
| `N` | starts per year: residents × 5.05 flushes × 365.25 | 1/year |
| `t_r` | switch-off delay of the electronic control | h |

It is the form of the «simple method» Ward, Butler and Memon (2012) describe, power times operating
duration, with two corrections: the effective flow rate is the smaller of that of the pump and that of
the point, and the delay of electronic controls enters at each start. The nameplate power is that of
the nominal point, and at low flow the motor draws a little less; the estimate tends to overestimate
the energy, but it ranks the models among themselves.

The default point flow rate is 0.15 L/s, that is, 9 L/min: the design flow rate of a toilet with a
flushing cistern in Table A.1 of ABNT NBR 5626:1998. The 2020 edition dropped the table and left to the
design the task of stating the flow rates at the points of use (item 6.7.1); anyone with the toilet
manufacturer's figure should use it.

### The catalogue

Step **4. Reservoir & Costs** has six residential pressure pumps from five manufacturers, each with the
flow × pressure curve from its manual, kept among the documents consulted: Komeco TP 820T and TP 825T,
Cardal Potenza, Jacuzzi AcquaHouse, with a curve tested at the Pump Labelling Laboratory of UNIFEI,
Syllent Impulse Press and Rowa Max Press 20E. For another model, the «Custom» option asks for the
nameplate power, the flow rate read on the manufacturer's curve at the working pressure and the
switch-off delay.

The table applies the catalogue to the tutorial's direct pressurisation: the 4,000 L cistern without an
upper tank, four residents and the toilet flow rate of 9 L/min.

<!-- inclui: _tabelas/cap28_pressurizadores.md -->

At 18 m head, five of the six models deliver more than the toilet's 9 L/min, and all stay on for the
same 110 hours a year. What separates them is the power: the 1/4 hp one uses 40 kWh, the 1/2 hp ones,
67. The sixth, with little more than 7 L/min at 18 m, works almost at the end of its curve, stays on
longer and also adds ten seconds of delay to each of the 7,373 starts of the year.

At 24 m head the order reverses. The 1/4 hp model drops to 4.4 L/min, and the time switched on doubles;
three models do not even reach the pressure. The best becomes a 1/2 hp one. ==The rule the table teaches
is to choose the smallest model that delivers the point's flow rate at the working pressure,== and it is
what item 6.5.11.12 of ABNT NBR 5626:2020 asks for: that the energy consumption of pumping and
pressurisation pumps be minimised by the choice of pump, among the alternatives considered. The screen
points to that model and shows the energy of all the others next to it.

> **Two pumps, not one.** Item 6.5.11.2 of the same standard requires at least two pumps, operating
> independently, in pumping and pressurisation systems. The tutorial follows the standard, and the
> investment counts the duty pump and the standby. EN 16941-1:2024 asks for a standby pump «if
> necessary».

---

## Why the energy of pumping to a tank is small, and that of the pressure pump is not

Lifting one cubic metre twelve metres costs about 0.033 kWh of hydraulic energy. With the two
efficiencies, it comes to 0.11 kWh per cubic metre delivered, and the tutorial's pumping, with the
start-ups, to 0.13 kWh/m³.

Direct pressurisation of the same project uses 0.68 to 1.66 kWh/m³, depending on the model: five to
thirteen times more. The numbers reproduce a difference the literature had already measured. In the
review by Vieira et al. (2014), the median of the theoretical studies was 0.20 kWh/m³, and that of the
empirical ones, 1.40 kWh/m³, because the former ignored the start-ups, standby mode and the real
efficiency of motor and pump. The same review reports 1.70 kWh/m³ to feed a toilet cistern directly
with a 450 W pump, and a mean of 1.52 kWh/m³ in nineteen Australian homes with direct feed.

The tutorial's pumping stays close to the theoretical median because it works as the theoretical
studies assume: few starts per year, at the pump's own flow rate. The pressure pump falls in the
empirical range because it works as the measured homes do: one start per use, at the flow rate of the
point.

Even so, the energy is small compared with the saving on the bill. The 40 kWh of the smallest pressure
pump cost less than thirty reais a year at the tutorial's tariff. The argument that «pumping uses more
than it saves» does not hold in small buildings, but the choice of arrangement and model can multiply
the energy part by ten, and it is that part that weighs in the carbon of section {{n:30}}.

In a tall building, with thirty metres of pumping, the calculation changes, and it is worth redoing it.
