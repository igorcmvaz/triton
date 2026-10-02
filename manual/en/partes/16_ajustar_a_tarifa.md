# Adjusting the tariff of your municipality

> **Question this guide answers:** is my municipality's tariff in the database, and is it
> right?

> **Edition.** The catalogue of 652 municipalities and step **12. Tariff Manager** come
> only with the Brazil Edition. In the International Edition the tariff is typed in, in the
> economic step, with the same block table, the same codes and the same six regimes
> described here — so this guide is also the reference for entering any tariff structure.

This is the guide that changes results the most. The tariff structure decides the economic
feasibility of a rainwater system more than any design parameter, and it is also the input
that most often appears wrong in published studies on the subject.

---

## How the water and sewage bill is made up in Brazil

Before checking the municipality's tariff, it is worth understanding what is being checked.
The water bill in Brazil is not the product of consumption by a single price, and five
features set it apart from the electricity bill, which is the reference most familiar to
most readers.

**Provision is local, and so is the price.** Each municipality is served by a state
company, a municipal authority or a private concessionaire, and each provider has its own
table, approved by a regulatory agency — state, municipal or intermunicipal. There is no
national water tariff, and the difference between two neighbouring municipalities can be
more than double.

**The tariff is progressive by consumption block.** A cubic metre does not cost the same at
any quantity: consumption is divided into blocks, and each block has its own, increasing
price. In the CASAN table in force in Florianópolis, the first ten cubic metres cost
R$ 3.08 each and the next fifteen cost R$ 14.31 each. ==Progressivity is what makes saving
water more valuable than it seems:== the cubic metre no longer consumed is always that of
the highest block on the bill, the most expensive one.

**There is a part that does not depend on consumption.** Almost every utility charges
something even to those who consume nothing, and the name and nature of that part vary from
place to place. It is the subject of the subsection on the six regimes, below, and it is
the point that most decides whether a rainwater system pays for itself.

**Sewage is charged as a percentage of water.** Most providers bill sewage by applying a
percentage to the water part, commonly 80% or 100%, on the argument that the volume
discharged is proportional to the volume consumed. When that percentage is 100%, the sewage
part equals the water part, and sewage accounts for half of the bill — which means each
cubic metre saved is worth twice the price of water.

**There are different categories of consumer.** Every utility publishes separate tables for
the residential, commercial, industrial and public categories, with prices that are often
double the residential one or more. In the CASAN table, the first block costs R$ 3.08/m³ for
residential and R$ 6.81/m³ for commercial.

> **What the program brings, and what you need to enter.** The program's catalogue of 652
> municipalities records the **residential category** of each one. The other categories
> exist, are public and are in the resolutions of the regulatory agencies — what does not
> exist is a national catalogue of them, which would be a survey in its own right. To study
> a school, a shop or an industry, enter the structure of the right category in the custom
> mode of this same screen: the program accepts any block table, with any minimum-charge
> regime, and section {{n:18}} shows the procedure.

---

## Start by checking what is already in the database

The program comes with a catalogue of 652 Brazilian municipalities, and each record has the
complete tariff structure, the sewage percentage charged, the minimum-charge regime adopted,
the effective date of the table and the documentary source from which the data were taken.
The catalogue covers the residential category, as the previous subsection explains.

In step **12. Tariff Manager**, choose the state and the municipality. Besides the
structure, the program shows the **confidence grade** given to the record, which sums up the
quality of the source and the date of the survey. Three items deserve checking against your
utility's current resolution, and the order matters because the first invalidates the
others.

1. **the effective date** — tariffs are adjusted every year;
2. **the block values**;
3. **the minimum-charge regime**, which is item {{n:16.4}}.

If any of the three differs, edit the record. The edit applies to your project, does not
change the catalogue of other users, and is saved inside the `.netuno` file — which means
whoever receives your project will reproduce the same calculation, with the same table.

---

## How the table is built

Each row of the tariff structure is represented in the program by a quadruple of values:
the minimum volume of the block, the maximum volume, a monetary value and a code. The code is
the decisive element, because it is what says what that value means — and structures that
look alike charge in very different ways depending on the code of each row.

<!-- tabela: The six tariff block codes and the effect of each one on the bill -->
| Code | What it is | How it enters the bill |
| ---: | :--- | :--- |
| 1 or 0 | consumption block | the price is charged on the volume that falls **within** each consumption block |
| −1 | availability charge | fixed value **added** to the consumption part |
| −2 | retroactive allowance | up to the allowance volume, the fixed value is paid; beyond it, **everything from zero** is charged |
| −3 | payment floor | the bill does **not** go below this value |
| 2 | exponential base price | `PB` of the formula `PB × Cⁿ`, valid up to the row's maximum |
| 3 | exponent of the exponential table | the `n` applied to the consumption **of the whole month** that falls in the row |

The Florianópolis structure, taken as an example, has five rows: one availability charge and
four progressive blocks.

```
(0.00 ; 0.00 ; 46.34 ; -1)     availability charge, always added
(0.00 ; 10.00 ;  3.08 ;  1)    first block
(10.00 ; 25.00 ; 14.31 ; 1)    second block
(25.00 ; 50.00 ; 19.14 ; 1)    third
(50.00 ; 999999 ; 24.08 ; 1)   last
```

---

## The six regimes, and why they decide projects

The «minimum consumption» appears on the bill of almost every Brazilian municipality, and it
means **different** things in each one. The program distinguishes six regimes:

<!-- tabela: The six tariff regimes and what happens when saving in each one -->
| Regime | What happens when saving | Municipalities in the database |
| :--- | :--- | ---: |
| **no minimum** | each m³ saved is deducted | 165 |
| **availability charge** | likewise; the fixed fee remains, but it does not prevent the saving | 122 |
| **exponential formula** | likewise; the m³ saved is worth the base price raised to the exponent | 34 |
| **allowance in the minimum** | below the allowance, saving **deducts nothing** | 329 |
| **retroactive allowance** | beyond the allowance, everything from zero is charged | 2 |
| **payment floor** | the bill does not go below the floor | 0 |

**The case that brings down studies.** Compare two real structures of the database, side by
side, for the same consumption:

<!-- tabela: Effect of the water saving on the bill in two opposite tariff regimes -->
| Consumption | Floriano (PI), allowance in the minimum | Florianópolis (SC), availability charge |
| ---: | ---: | ---: |
| 14 m³ | R$ 92.15 | R$ 134.38 |
| 12 m³ | R$ 72.52 | R$ 105.76 |
| 10 m³ | R$ 52.89 | R$ 77.14 |
| 8 m³ | **R$ 52.89** | R$ 70.98 |
| 5 m³ | **R$ 52.89** | R$ 61.74 |

In Floriano, the bill **stops falling at 10 m³**. A house that consumes 12 m³ and installs a
system that saves 4 goes down to 8, and saves R$ 19.63 — not the R$ 24.17 the average tariff
of R$ 6.04/m³ would suggest. If it saved 7, it would go down to 5 and save the **same**
R$ 19.63: the three additional cubic metres are worth nothing.

In Florianópolis, each cubic metre saved reduces the bill, down to the first one.

> Running the Floriano case with the Florianópolis structure produces a payback that does
> not exist. Three hundred and twenty-nine of the 652 municipalities of the database are in
> the allowance regime. It is the majority, and it is the most common scenario in the
> country.

{{fig:fig05_regimes}} shows the three responses side by side. What distinguishes the regimes
is not the price charged, but the shape of the curve: ==where the curve is horizontal,
saving water does not reduce the bill at all.==

![The water part of the bill against consumption, in three minimum-charge regimes](../figuras/fig05_regimes.png)

*Figure 99 — Water part of the monthly bill as a function of consumption, in three minimum-charge regimes. Sewage is not in the chart because it is charged as a percentage of this part and only multiplies the curve, without changing its shape. With the availability charge and with no minimum, each cubic metre saved reduces the bill from the first one; with the allowance in the minimum, the horizontal stretch marks the consumption range in which saving water does not reduce the bill.*

---

## The CORSAN exponential formula

The 34 municipalities of Rio Grande do Sul in the database served by CORSAN do not charge
water by blocks. The water part of the bill is given by a formula:

```
Water = PB × Cⁿ + SB
```

where `PB` is the base price of the municipality, in R$/m³; `C` is the month's consumption,
in m³; `n` is the exponent the utility's **Exponent Table** gives to that consumption; and
`SB` is the basic service, charged even without consumption. In the residential category,
`n` is 1.00 up to 20 m³ and rises with each cubic metre from there on:

<!-- tabela: Exponent n of the CORSAN Exponent Table, residential category -->
| Month's consumption | `n` | Month's consumption | `n` |
| :--- | ---: | :--- | ---: |
| up to 20 m³ | 1.00 | 36 to 45 m³ | 1.10 |
| 21 m³ | 1.01 | 46 to 100 m³ | 1.11 |
| 22 to 27 m³ | 1.02 to 1.07 | 101 to 150 m³ | 1.13 |
| 28 and 29 m³ | 1.08 | 151 to 1,000 m³ | 1.1287 to 1.12 |
| 30 to 35 m³ | 1.09 | above 1,000 m³ | 1.11 to 1.0858 |

The table continues beyond 1,000 m³: only the industrial category has a cap at that volume,
above which the excess is charged at its own prices. **Sewage** is not in the formula: it is
charged per cubic metre consumed, without the basic service and without the exponent —
R$ 6.40/m³ treated in the municipalities of ANNEX 5, 70% of the base price truncated to the
centavo.

Two differences from the blocks decide the calculation:

- **The exponent applies to the whole consumption.** With blocks, each cubic metre is charged
  at the price of the block it falls in; with the formula, the `n` of the row in which the
  total consumption falls applies to the whole volume. Going from 20 to 21 m³ costs R$ 15.09
  of water, not the R$ 9.15 of the base price, because the whole 21 m³ are now raised to
  1.01.
- **There is no price step, there is a curve.** The mean price of a cubic metre of water is
  `PB × Cⁿ⁻¹`: constant up to 20 m³ and growing after that.

<!-- tabela: Monthly bill in Alegrete (RS) by the exponential formula, effective 01/07/2026 -->
| Consumption | `n` | Water | Water and sewage | Mean water price |
| ---: | ---: | ---: | ---: | ---: |
| 10 m³ | 1.00 | R$ 134.89 | R$ 198.89 | R$ 13.49/m³ |
| 20 m³ | 1.00 | R$ 226.39 | R$ 354.39 | R$ 11.32/m³ |
| 25 m³ | 1.05 | R$ 312.08 | R$ 472.08 | R$ 12.48/m³ |
| 30 m³ | 1.09 | R$ 416.20 | R$ 608.20 | R$ 13.87/m³ |

The R$ 134.89 for 10 m³ are exactly the «minimum tariff without a water meter» of the CORSAN
table, 43.39 + 9.15 × 10, which confirms the transcription. For rainwater harvesting, the
consequence is that **every saving is deducted from the first cubic metre**, and deducted more
where the exponent is larger: a house that goes down from 30 to 20 m³ saves R$ 253.81 per
month. The straight line used up to 5.0.0, with 70% sewage on the whole bill, gave R$ 155.55
for the same reduction.

In the program, the formula enters the same table of quadruples, with two codes of its own.
The Alegrete structure starts like this:

```
(0.00 ; 0.00   ; 43.39 ; -1)   basic service, always added
(0.00 ; 999999 ;  9.15 ;  2)   base price PB
(0.00 ; 20.00  ;  1.00 ;  3)   n for consumption in (0, 20]
(20.00 ; 21.00 ;  1.01 ;  3)   n for consumption in (20, 21]
...                            one row per interval of the Exponent Table
```

In the **Tariff Manager**, the structure appears with the label «Exponential formula», the
«Exponent n» rows can be edited, the simulator shows the `PB × Cⁿ` calculation for the
chosen consumption, and the upper chart shows the mean price `PB × Cⁿ⁻¹` instead of the
steps. The sewage field becomes «Sewage (R$/m³ consumed)», and the economic step offers the
same mode, «Per m³ consumed», next to the fixed value and the percentage of water.

---

## When the minimum is diluted into the tariff

A frequent error in public databases: the utility states «minimum tariff of R$ 52.89 for
10 m³», and whoever registers it records it as R$ 5.289 per m³ up to 10 m³.

The difference is enormous. In the first reading, someone who consumes 4 m³ pays R$ 52.89;
in the second, R$ 21.16. And, worse for a rainwater study, in the second reading saving below
10 m³ **is deducted**, when in reality it is not.

The program audits the database for this pattern and recodes the cases found, recording the
correction. If you register a new municipality, **check this**.

---

## Sewage

The sewage percentage applies to the **water part** of the bill, not to the total bill.

One hundred per cent, as in Florianópolis, means that the sewage part equals the water part —
and so sewage is **half the bill**. Saving water saves both parts, and that is why the
effective value of the cubic metre saved almost doubles.

Some municipalities charge sewage by blocks of their own, not by a single percentage. In
those cases the single percentage is an approximation, and the program records the
limitation.

---

## Where to find the data

In order of reliability:

1. **Tariff resolution** of the state or municipal regulatory agency. It is the official
   document, and it has the effective date.
2. **Table published by the utility**, usually under «tariffs» on its website.
3. **Bill simulator** of the utility, when there is one. Good for checking: simulate two
   consumptions and see whether your table reproduces both values.
4. **Real water and sewage bill**, of the property itself. It is the best evidence, and it
   allows the whole structure to be checked.

> **Always record the effective date and the source.** A study that does not say when the
> tariff dates from cannot be reproduced two years from now.

---

## Check before you trust

After building the table, do the test that item {{n:16.7}} suggests: simulate two
consumptions, one inside and one outside the minimum block, and compare with the real bill or
with the utility's simulator.

If both match, the structure is right. If only one matches, the minimum-charge regime is
wrong — and that is exactly the error that most compromises a rainwater study.
