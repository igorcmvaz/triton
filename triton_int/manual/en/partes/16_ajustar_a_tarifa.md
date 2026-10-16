# Adjusting the tariff of your city

> **Question this guide answers:** is the tariff in my project the one the building is
> billed on, and is it entered correctly?

> **International Edition.** The program carries no tariff catalogue. The tariff is typed in,
> in the economic step, with a block table, a set of codes and six minimum-charge regimes. This
> guide describes them, so it is also the reference for entering any tariff structure. The three
> example projects (New York, London and Cape Town) each carry the published tariff of their
> city, with source and date.

This is the guide that changes results the most. The tariff structure decides the economic
feasibility of a rainwater system more than any design parameter, and it is also the input
that most often appears wrong in published studies on the subject.

---

## How a water and sewage bill is made up

Before entering a tariff, it is worth understanding what is being entered. A water bill is
not the product of consumption by a single price, and five features set it apart from the
electricity bill, which is the reference most familiar to most readers.

**Provision is local, and so is the price.** Each city is served by one provider, public or
private, and each provider publishes its own table, approved by a regulator or by a public
board. There is no universal water tariff. The three example cities show it: New York charges
one price per volume, London charges a standing charge plus one price per volume, and Cape Town
charges four increasing steps plus a standing charge.

**The tariff may be progressive by consumption block.** Where it is, a cubic metre does not
cost the same at any quantity: consumption is divided into blocks, and each block has its own,
increasing price. ==Progressivity makes saving water more valuable than it seems:== the cubic
metre no longer consumed is the one of the highest block on the bill, the most expensive one.

**There may be a part that does not depend on consumption.** Many utilities charge something
even to those who consume nothing: a standing charge, a minimum bill or both. It is the subject
of the subsection on the six regimes, below, and it is the point that most decides whether a
rainwater system pays for itself.

**Sewage is charged on the water.** Providers bill sewage by applying a percentage to the
water part, by a price per cubic metre, or by blocks of its own. In New York the sewer charge is
a percentage of the water charge, so that each cubic metre saved is worth the water price
and the sewer charge together. In London, wastewater has a price per cubic metre of its own. In
Cape Town, sanitation is charged by four steps on 70% of the water consumed.

**There are different categories of consumer.** Utilities publish separate tables for
residential, commercial and other categories, often at higher prices than the residential one.
The program's tariff screen holds one structure per project: to study a school, a shop or an
industry, enter the structure of the category the building is billed in. Section {{n:18}} shows
the procedure.

---

## Start by checking what is in the project

In the economic step, open the tariff screen. The program shows the structure in force in the
project: the block table, the sewage mode, the standing charges, the effective date and the
source recorded. In the example projects, the source and the date are filled in; in a new
project, you enter them. Three items deserve checking against your utility's current tariff
document, and the order matters because the first invalidates the others.

1. **the effective date**: tariffs are adjusted every year;
2. **the block values**;
3. **the minimum-charge regime**, which is item {{n:16.4}}.

If any of the three differs, edit the table. The edit applies to your project and is saved
inside the `.triton` file, which means whoever receives your project will reproduce the same
calculation, with the same table.

---

## How the table is built

Each row of the tariff structure is represented in the program by a quadruple of values:
the minimum volume of the block, the maximum volume, a monetary value and a code. The code is
the decisive element, because it is what says what that value means, and structures that
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

The London example, taken as an illustration of the notation, has two rows: one availability
charge (the water standing charge, spread by month) and one open consumption block.

```
(0.00 ; 0.00   ; standing charge per month ; -1)   availability charge, always added
(0.00 ; 999999 ; price per m³               ;  1)   one open consumption block
```

The Cape Town structure has the same availability row followed by four consumption blocks, one
for each step of the published table. The New York structure has one open block and, for the
minimum daily charge, a payment-floor row (code −3).

---

## The six regimes, and why they decide projects

A minimum charge appears on the bill of many utilities, and it means **different** things in
each one. The program distinguishes six regimes:

<!-- tabela: The six tariff regimes and what happens when saving in each one -->
| Regime | What happens when saving | Where it appears in the examples |
| :--- | :--- | :--- |
| **no minimum** | each m³ saved is deducted | none of the three |
| **availability charge** | likewise; the fixed fee remains, but it does not prevent the saving | London (standing charge); Cape Town (standing charge, with steps) |
| **exponential formula** | likewise; the m³ saved is worth the base price raised to the exponent | none of the three |
| **allowance in the minimum** | below the allowance, saving **deducts nothing** | none of the three |
| **retroactive allowance** | beyond the allowance, everything from zero is charged | none of the three |
| **payment floor** | the bill does not go below the floor | New York (minimum daily charge; it does not bind at the tutorial consumption) |

**The case that brings down studies.** Compare two hypothetical structures side by side, for the
same consumption. The prices are round numbers in currency units (cu), chosen to make the
arithmetic easy to follow; they are an illustration, not a tariff:

<!-- tabela: Effect of the water saving on the bill in two opposite tariff regimes (hypothetical structures, in currency units) -->
| Consumption | Structure A, allowance in the minimum (50 cu for the first 10 m³, then 5 cu/m³) | Structure B, availability charge (40 cu plus 5 cu/m³) |
| ---: | ---: | ---: |
| 14 m³ | 70 cu | 110 cu |
| 12 m³ | 60 cu | 100 cu |
| 10 m³ | 50 cu | 90 cu |
| 8 m³ | **50 cu** | 80 cu |
| 5 m³ | **50 cu** | 65 cu |

In structure A, the bill **stops falling at 10 m³**. A house that consumes 12 m³ and installs a
system that saves 4 goes down to 8, and saves 10 cu, not the 20 cu the average price of
5 cu/m³ would suggest. If it saved 7, it would go down to 5 and save the **same** 10 cu: the three
additional cubic metres are worth nothing.

In structure B, each cubic metre saved reduces the bill, down to the first one.

> Running a case of structure A with the data of structure B produces a payback that does not
> exist. Check the regime before trusting any economic result.

The three example cities are all in the second family: in each, every cubic metre saved reduces
the bill. In New York, for the tutorial house, the bill without the system is for 18.26 m³ a
month, US$ 89.37; with the system, 13.31 m³ and US$ 65.15; the saving is 4.95 m³ and
US$ 24.21 a month. The two prices (water and sewer) are both earned on every cubic metre saved,
which is why the saving per cubic metre is more than twice the water price alone.

{{fig:fig05_regimes}} shows the three responses side by side. What distinguishes the regimes
is not the price charged, but the shape of the curve: ==where the curve is horizontal,
saving water does not reduce the bill at all.==

![The water part of the bill against consumption, in three minimum-charge regimes](../figuras/fig05_regimes.png)

*Figure 99 — Water part of the monthly bill as a function of consumption, in three minimum-charge regimes. Sewage is not in the chart because it is charged as a percentage of this part and only multiplies the curve, without changing its shape. With the availability charge and with no minimum, each cubic metre saved reduces the bill from the first one; with the allowance in the minimum, the horizontal stretch marks the consumption range in which saving water does not reduce the bill.*

---

## The exponential formula

Some utilities do not charge water by blocks. The water part of the bill is given by a formula:

```
Water = PB × Cⁿ + SB
```

where `PB` is the base price, in currency per m³; `C` is the month's consumption, in m³; `n` is
the exponent that the utility's **exponent table** gives to that consumption; and `SB` is the
basic service, charged even without consumption. Typically `n` is 1.00 up to a threshold and rises
with consumption from there on.

Two differences from the blocks decide the calculation:

- **The exponent applies to the whole consumption.** With blocks, each cubic metre is charged
  at the price of the block it falls in; with the formula, the `n` of the row in which the
  total consumption falls applies to the whole volume. Going over a threshold therefore raises
  the cost of the cubic metres below it as well.
- **There is no price step, there is a curve.** The mean price of a cubic metre of water is
  `PB × Cⁿ⁻¹`: constant while `n` is 1 and growing after that.

For rainwater harvesting, the consequence is that **every saving is deducted from the first
cubic metre**, and deducted more where the exponent is larger.

None of the three example cities uses this regime. In the program, the formula enters the same
table of quadruples, with two codes of its own: a row of code 2 holds the base price `PB`, and
one row of code 3 for each interval of the exponent table holds the `n`.

```
(0.00 ; 0.00   ; SB  ; -1)   basic service, always added
(0.00 ; 999999 ; PB  ;  2)   base price PB
(0.00 ; 20.00  ; 1.00 ; 3)   n for consumption in (0, 20]
...                          one row per interval of the exponent table
```

In the **Tariff Manager**, the structure appears with the label «Exponential formula», the
«Exponent n» rows can be edited, the simulator shows the `PB × Cⁿ` calculation for the chosen
consumption, and the upper chart shows the mean price `PB × Cⁿ⁻¹` instead of the steps. The
sewage field becomes «Sewage (per m³ consumed)», and the economic step offers the same mode,
«Per m³ consumed», next to the fixed value and the percentage of water.

---

## When the minimum is diluted into the tariff

A frequent error in tariff tables: the utility states «minimum bill of 50 for 10 m³», and
whoever registers it records it as 5 per m³ up to 10 m³.

The difference is enormous. In the first reading, someone who consumes 4 m³ pays 50; in the
second, 20. And, worse for a rainwater study, in the second reading saving below 10 m³
**is deducted**, when in reality it is not.

If you register a new tariff, **check this**: a minimum stated as a bill is an availability
charge or an allowance, not a price per cubic metre.

---

## Sewage

The sewage percentage applies to the **water part** of the bill, not to the total bill.

In New York the sewer charge is 159% of the water charge, so the sewer part is larger than the
water part, and the two together are the cost of each cubic metre. Where the percentage is
100%, the sewage part equals the water part and sewage is **half the bill**. Saving water saves
both parts, and that is why the effective value of the cubic metre saved is higher than the
water price.

Some utilities charge sewage by a price per cubic metre (London) or by blocks of its own on a
fraction of the water volume (Cape Town, on 70% of the water consumed). The program has one mode
for each: percentage of the water part, price per cubic metre, and blocks on a fraction of the
volume. Choose the one that matches the document.

---

## Effective date, escalation and alternative tables

A table applies from the date of the document it came from, and there is not always a newer one.
The tariff dialogue shows that date next to the **Study base date**, which is stored in the
project. Between the two, the program applies the escalations already due, at the configured
escalation rate, and the following ones fall on the anniversaries of the table, not twelve
months after the study starts. This is an estimate, because the escalation actually granted may
have been different; with the current table at hand, type it in with its own date. An old
project, without the dates, stays as it was.

Some cities have more than one residential table, for example by property size, by meter size or
by area. Choose the table that matches the property, and record in the project why it represents
it. Anyone with the property's own bill can, as always, type the table in.

## Where to find the data

In order of reliability:

1. **Tariff document** of the regulator, the public board or the utility. It is the official
   document, and it has the effective date.
2. **Table published by the utility**, usually under «charges» or «tariffs» on its website.
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
wrong, and that is exactly the error that most compromises a rainwater study.
