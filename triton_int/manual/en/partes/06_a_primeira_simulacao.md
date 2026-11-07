# The first simulation

> By the end of this section you will have the first result on screen and will know how
> to **read** the four numbers that matter. Reading is the hard part: the program
> delivers many numbers, and three of them answer different questions.

One input is missing before simulating: the volume of the tank. Let us guess.

**3,000 litres.** A 3 m³ cistern is a common back-yard size, and what a designer would propose
without much thought. Section {{n:7}} will ask
whether it is the right volume. Here we only want to see the program run.

In step **4. Reservoir & Costs**, choose a fixed volume, enter 3,000 L, leave the upper
tank unticked, and run.

---

## The result

<!-- inclui: _tabelas/cap06_primeira_simulacao.md -->

The screen returns several dozen values, and four of them are enough to judge the project
at this stage. Each one answers a different question, and it is precisely because they
answer different questions that they do not replace one another: a project can be good
by the first and bad by the third, and reading them together is what avoids a hasty
conclusion.

---

## The saving potential: 25.99%

This indicator answers the question that motivates most projects: how much of the water
and sewage bill stops being paid. It is the central value the program produces and the
one that appears in the summary of any study, and it is the ratio between the rainwater
consumed and the total demand of the building over the whole series, as in Equation
{{eq:potencial}}.

The denominator deserves attention, because everything else follows from it: it is the
**total** demand, not the rainwater demand. It is this choice that sets the ceiling of
the indicator at 28%, which is the suppliable fraction defined in section {{n:5}}, and
not at one hundred per cent.

The system reached 25.99% against a ceiling of 28%, which means it delivers 93% of what
it set out to deliver. The remaining 7% correspond to the days when the cistern did not
have enough water to meet that day's rainwater demand.

> **Do not confuse the two percentages.** «A saving of 26%» and «93% of the rainwater
> demand met» describe the same system and are different numbers. Published studies
> sometimes swap one for the other. Declare which one you are using.

---

## The overflow: 150.8 L/day

**It answers: is the tank big enough?**

About 151 litres per day, on average over the thirty years, overflow from the cistern
and go to the drainage system. ==That is almost as much as the 168 L/day the system
intends to consume,== and the tank lets through nearly as much water as it uses.

It looks like an argument for enlarging the tank, and it is a weak one. The roof offers
2.3 times what the house intends to use (section {{n:5}}), so a good part of that surplus
would overflow from any cistern, however large. The overflow only says something about the volume when
compared with that of other volumes, and that comparison is what section {{n:7}} does.

> A high overflow is not a defect of the program or of the project. It is the signature
> of the mismatch between the rain, which arrives concentrated in a few days, and the
> demand, which is constant. The tank exists to buffer this, and every finite tank fails
> in some event.

---

## The days of supply: 91.9% full

**It answers: how often can I count on the system?**

This is the **time** reliability of the system, and it answers a question the saving
potential does not reach: how often rainwater can be counted on. Each day of the
simulation receives one of three classifications, according to the degree of supply
achieved.

<!-- tabela: Classification of each day of the simulation by the degree of supply -->
| Class | What it means |
| :--- | :--- |
| full | rain met **all** the rainwater demand of the day |
| partial | it met part of it, and the mains made up the rest |
| none | the cistern was empty; everything came from the mains |

On 91.9% of the days the system met the rainwater demand on its own, and on the
remaining 8.1% the mains came in, fully or partly (1.7% of the days partial, 6.4% none). The distinction has a direct
consequence on the plumbing design: a system with many days of no supply needs a
well-sized automatic backup supply, and the user notices the switching between the two
sources over the year. A system with 99% full days is, in practice, independent of the
mains for the uses it supplies.

> **Potential and reliability do not go together.** It is possible to have a high
> potential with low reliability: a tank that fills in the rainy season and dries out in
> the dry season delivers a lot of volume over the year and fails half the days. The
> table of section {{n:7}} shows the two columns diverging.

---

## The annual volume saved

**It answers: how much is this worth in money and in carbon?**

This is the value that carries over to sections {{n:10}} and {{n:11}}, because both the
saving on the water and sewage bill and the avoided carbon emission are calculated from
it. It is 57.0 m³/year, less than half of the 143 m³/year the roof makes available
before the first flush; the first flush and the overflow account for most of the
difference.

---

Before discussing why the potential does not reach 28%, it is worth seeing the tank at
work. The results tab has the daily series of the cistern level, and it is there that
the two regimes limiting the yield can be seen at once: overflow and shortage
({{fig:fig48_programa_serie_diaria}}).

![The level of the cistern, day by day, over one year](../figuras/fig48_programa_serie_diaria.png)

*Figure 99 — The level of the cistern over the first year of the series, with the daily rain in the background. The plateaus at the top are the days when the tank is full and overflows; the valleys at zero are the days when it ran dry and the mains supplied everything. Figure generated by the program itself.*

---
## Why we do not reach 28%

Section {{n:5}} ended with an apparently favourable comparison: 143 m³ per year of supply
against 61 m³ of rainwater demand, that is, 2.3 times what is needed. Faced with this
surplus, it would be reasonable to expect full supply, and yet the system delivers 93% of
what was intended.

The explanation lies entirely in **time**. The surplus does not occur when the water is
needed: precipitation arrives concentrated, fills the 3,000 L cistern in a single day of
intense rain, overflows on the same day, and is missing two weeks later. The annual
surplus and the daily supply are quantities that do not communicate, and it is precisely
this lack of communication that makes the daily simulation indispensable.

The 3,000 L tank stores the equivalent of eighteen days of rainwater demand. Any dry
spell longer than that empties it, and from then on the system depends entirely on the
mains until the next rain.

That is why enlarging the tank works — and that is why enlarging has a limit. Section
{{n:7}} measures exactly where that limit lies.

---

## What we have so far

<!-- tabela: State of the tutorial project after the first simulation -->
| Result with 3,000 L | |
| :--- | ---: |
| saving potential | 25.99% |
| out of a ceiling of | 28% |
| overflow | 150.8 L/day |
| days of full supply | 91.9% |

A defensible result, and already close to the ceiling. But we chose 3,000 L by guesswork:
it may be too little, and it may be too much.

What would be right?
