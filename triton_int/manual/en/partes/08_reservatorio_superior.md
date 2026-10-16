# Is an upper tank needed?

> By the end of this section you will be able to answer the question with a number, not
> with habit. The answer usually surprises.

The classic rainwater harvesting arrangement uses two tanks: a buried cistern,
which receives the water from the roof, and an elevated water tank, which feeds the points
of use by gravity; between the two, a pump lifts the water. The arrangement is so
widespread that almost every project adopts it without examining why, and this section
examines it.

---

## What the upper tank is for

==The upper tank is not for storing more water; it is for delivering it.== The
distinction seems subtle and decides the whole analysis, because everything that follows
depends on not confusing storage capacity with distribution capacity.

The cistern is buried, and the points of use — toilet, utility sink, garden tap — are
above it. Something has to overcome that difference in level, and there are two ways of
doing it with a pump.

- **Direct pressurisation.** A small pump with a pressure switch starts whenever a point
  is opened. There is no upper tank.
- **Pumping to an elevated tank.** The pump fills the tank from time to time, and gravity
  does the rest.

When the cistern is above the points of use, there is a third one: **gravity**, with no
pump. Step **4. Reservoir & Costs** asks which of the three arrangements the project
adopts, and it is this answer that defines the energy and the pump sets in the cost and
in the carbon.

<!-- tabela: The three supply arrangements and what each one adds to the project -->
| Arrangement | Energy calculated | Upper tank and pump sets |
| :--- | :--- | :--- |
| pumping to an upper tank | volume pumped, at the manometric head, plus the start-ups | enter the cost and the carbon |
| direct pressurisation | all the rainwater consumed, at the working pressure | only the pump sets |
| gravity | none | none |

In direct pressurisation, step 4 asks for the model of the pressure pump, chosen from a
catalogue of six generic reference models, A to F, each with an illustrative flow × pressure
curve (none is a real product), the working pressure and the flow at the point of use. The
pressure pump starts at each flush, 5.05 per person per day according to the end-use
survey of Mayer et al. (1999), and stays on while the cistern of the toilet fills, at the
pace of its float valve. The energy is that time multiplied by the electrical power. In
the tutorial, at a head of 18 m, the smallest model would use 40.0 kWh per year, about
five times the 7.7 kWh of pumping to a tank;
section {{n:28}} explains why, and shows that the model chosen weighs more than the
pressure.

Pumping to an elevated tank has three real practical advantages. The pump starts a few
times a day, instead of dozens, which extends the life of the equipment; the pressure at
the points of use is constant, because it comes from the height of the water column and
not from the pump running; and there is a reserve available during a power cut. ==None of
these three advantages is a water saving,== and that is precisely the confusion this
section clears up.

---

## The fair comparison

Comparing a 4,000 L system without an elevated tank with another of 4,000 L plus a
1,000 L tank is a methodological trap, because the second has more total storage and
would win for that reason, not because of the arrangement. To isolate the effect of the
arrangement, the storage must be kept constant: so 5,000 L in a single tank is compared
with 4,000 L below plus 1,000 L above.

<!-- inclui: _tabelas/cap08_reservatorio_superior.md -->

Keeping the same storage, the arrangement with an elevated tank delivers 0.15 percentage
points less saving than the single tank. The difference is not a rounding
error, and it has a cause: **the cistern overflows while the upper tank still has room**.

Rain enters only through the cistern, and the overflow is calculated there before the
day's consumption. Pumping, however, only happens when there is consumption and the upper
tank falls below the trigger level. So, on a rainy day with the cistern full, the water
exceeding the 4,000 L below is lost even if the tank above has hundreds of litres free. A
single 5,000 L tank would keep that water.

That is also why a higher trigger level yields more: with it, the pump fills the tank
earlier, the cistern is emptier when the rain arrives, and it overflows less. The reserve
below the trigger level is not locked away, because it is consumed right after each
pumping and when the cistern runs dry.

> **The upper tank does not increase the water saving. It costs.** In our project it
> costs the tank, it costs the pump, it costs 7.7 kWh per year of energy, and it costs
> 0.15 points of potential compared with a single tank of the same total volume.
>
> That does not make it wrong. It makes the decision **hydraulic**, not one of water
> yield: adopt it if the project needs gravity pressure or a reserve against power cuts,
> and not expecting it to yield more water.

---

## The trigger level

If you adopt the tank, there is a parameter to adjust: the reserve volume that is not
consumed, below which the pump starts.

<!-- inclui: _tabelas/cap08_limiar.md -->

A higher trigger level means **more potential and more starts**, for the reason above.
From 0 to 500 L, the potential rises by 0.11 points and the starts almost double, from 62
to 120 per year.

The trade-off is between a marginal water gain and the wear of the pump. Residential pump
sets cope well with a few starts a day; what kills them is continuous on-off cycling. One
hundred and twenty starts a year is one every three days, and none of the values in
the table comes close to being a problem.

> **Where the trigger level really matters** is in buildings with concentrated demand,
> where the tank empties quickly. There it can exceed a thousand starts a year, and it is
> better to size the tank than to adjust the trigger level.

---

## The energy, and why it is small

Seven point seven kilowatt-hours a year. At an illustrative US$ 0.20 per kilowatt-hour, that is US$ 1.54 a year (illustrative, not a market price).

It looks too little, and it is worth understanding why. Lifting one cubic metre of water
twelve metres costs, in hydraulic energy, about 0.033 kWh. With the efficiency of the pump
and that of the motor, and adding the pump start-ups, it comes to about 0.13 kWh per cubic
metre pumped. Sixty cubic metres a year give the 7.7 kilowatt-hours of the table.

Water is heavy, but twelve metres is little. That is why the energy cost of rainwater
harvesting is negligible compared with the saving on the water and sewage bill — and that
is also why the argument that «pumping water uses more energy than it saves» does not
hold in small buildings.

> **Warning about the nameplate power.** The program asks for the efficiency **of the
> pump** and the efficiency **of the motor** separately. The nameplate power is the
> mechanical power at the shaft, and the motor efficiency is what separates what the shaft
> delivers from what the meter records. Left blank, the program adopts a default motor
> efficiency that depends on the rated power; replace it with the figure on the motor
> data sheet. Section {{n:28}} gives the details.

---

## The tutorial's decision

**We adopt pumping to a 1,000 L upper tank, with a 100 L trigger level.**

The decision is hydraulic, not one of water yield. The elevated tank gives constant
pressure at the points of use without depending on the pump at each flush, keeps water
available during a power cut and makes the pump start 69 times a year, instead of the more
than seven thousand starts of a pressure pump triggered at each flush by four residents,
which would use 40 to 98 kWh per year depending on the generic model. The price is what the table
shows: the tank, the pumps, 7.7 kWh per year and 0.15 points of potential compared
with a single 5,000 L tank. There are two pumps, the duty pump and the standby, the usual
precaution for a pumped system that the building cannot do without.

Compared with the 4,000 L cistern on its own, the potential rises from 26.83% to 27.09%,
because the tank adds 1,000 L of storage. From here on, the cost, the carbon and the
tutorial's decision include the tank, the two pump sets and the pumping energy.

<!-- tabela: State of the tutorial project after the decision on the upper tank -->
| Project so far | |
| :--- | ---: |
| lower tank volume | 4,000 L |
| arrangement | pumping to an upper tank |
| upper tank | 1,000 L, 100 L trigger level |
| saving potential | 27.09% |

Now we know how much water the system delivers. It remains to know **what water** it is.
