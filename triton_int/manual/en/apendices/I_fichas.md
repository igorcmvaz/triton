# One-page summaries

Detachable summaries. Each sheet fits on one page and serves as a quick reference beside the
computer.

---

## Sheet 1 — The flow of a complete study

<!-- tabela: Reference sheet: the ten steps of a complete study and the section that deals with each one -->
| # | Step | What is decided in it | Section |
| ---: | :--- | :--- | ---: |
| 1 | Project and rain | series, area, coefficient, first flush | {{n:4}} |
| 2 | Building | building type, demand, suppliable fraction | {{n:5}} |
| 3 | First simulation | a guessed volume, to see | {{n:6}} |
| 4 | Sweep | return curve, ideal volume | {{n:7}} |
| 5 | Arrangement | is an upper tank needed? | {{n:8}} |
| 6 | Quality | class, disinfection, filters | {{n:9}} |
| 7 | Economics | real tariff, CAPEX, cash flow | {{n:10}} |
| 8 | Carbon | inventory, material, payback | {{n:11}} |
| 9 | Decision | eight criteria in four dimensions, declared weights | {{n:12}} |
| 10 | Report | outputs and the list of what to declare | {{n:13}} |

**Before publishing:** section {{n:13}}, the list of what to declare. Section {{n:33}}, the ten
mistakes. Section {{n:36}}, the limitations that affect your case.

---

## Sheet 2 — The pitfalls, one line each

<!-- tabela: Reference sheet: the ten design pitfalls and where each one is dealt with -->
| Pitfall | Where |
| :--- | :--- |
| **sloping** area instead of the horizontal projection | {{n:33.1}} |
| **mean monthly** rain instead of the daily series | {{n:33.2}} |
| first flush in **litres** when the field wants millimetres | {{n:33.3}} |
| tariff **minimum-charge regime** ignored | {{n:33.4}} |
| school or hospital with a **residential tariff** | {{n:33.5}} |
| expecting more **water** from the upper tank | {{n:33.6}} |
| too **short a series** | {{n:33.7}} |
| quality class chosen by **cost** | {{n:33.8}} |
| comparing with **another program** without declaring the differences of method | {{n:33.9}} |
| publishing the volume with the **highest saving** as the recommendation | {{n:33.10}} |

---

## Sheet 3 — The six tariff regimes

<!-- tabela: Reference sheet: the six tariff regimes and the effect of saving -->
| Regime | When saving |
| :--- | :--- |
| no minimum | every m³ earns a discount |
| availability charge | every m³ earns a discount; the fixed part remains |
| exponential formula | every m³ earns a discount; the bill is PB × Cⁿ + basic service |
| **allowance within the minimum** | **below the allowance there is no discount at all** |
| retroactive allowance | going past it, everything is billed from zero |
| payment floor | the bill does not go below the floor |

**Quick test:** simulate two consumptions, one inside and one outside the minimum block, and compare
them with a real bill. If only one matches, the regime is wrong.

The International Edition has no tariff catalogue: the regime is the one of the table you enter
(appendix {{n:D}}).

---

## Sheet 4 — The indicators, and what each one answers

<!-- tabela: Reference sheet: the indicators and the question each one answers -->
| Indicator | Denominator | Answers |
| :--- | :--- | :--- |
| saving potential | **total** demand | how much potable water consumption falls |
| volumetric reliability | **rainwater** demand | how much of what was intended was supplied |
| full, partial, no-supply days | days of the series | how often it can be counted on |
| overflow | — | is the tank small? |
| marginal gain | — | is it worth enlarging? |

`Epot = volumetric reliability × suppliable fraction`

---

## Sheet 5 — The pump set energy chain

```
pumping:   e = ρ · g · H ÷ (η_pump · η_motor)       kWh/m³
start-ups: E = plate × time ÷ η_motor              kWh
```

The plate gives the power **at the shaft**. The motor efficiency separates the shaft from the socket.
If left blank, the typical value for the rated power applies; enter the efficiency of your motor when
you have its data sheet.

---

## Sheet 6 — The list of what to declare, summarised

**Program:** version and edition, with revision.

**Rain:** source, cut, years; if a projection, model, scenario and window.

**Building:** area and how it was obtained, coefficient, per capita consumption and its source,
**suppliable fraction** and the uses that make it up.

**First flush:** depth and mode; and how it differs from the other program, if you compare programs.

**Volume:** selection criterion — marginal-gain threshold, or multi-criteria weights.

**Economics:** utility, effective date of the table, **minimum-charge regime**, sewage
percentage, minimum attractive rate of return, inflation, adjustments and period, and the
currency.

**Carbon:** boundary (water delivered), service life, tank material, grid factor with its source and year,
**approximate** factors or those with a **screening label**.

**Certification:** that classes 2 to 4 are adaptations of the program; for LEED, the version; for
EDGE, that only the water bar was assessed.
