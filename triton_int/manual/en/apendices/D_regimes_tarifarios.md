# Tariff regimes

The International Edition ships **no tariff catalogue**. You enter the water and sewage
tariff of the project, in the currency you choose, and the program calculates the bill
with and without the harvesting system. This appendix describes the structure the
program accepts, the six regimes it recognises, and the three example tariffs that come
with the edition.

## The block codes

Each row of the water tariff table is a quadruple `(minimum, maximum, value, code)`, in
m³ per month and currency per m³ (or currency per month for the fixed codes).

<!-- tabela: The block codes of the water tariff table -->
| Code | Meaning |
| ---: | :--- |
| 1 or 0 | progressive block: charged only on the volume inside it |
| −1 | availability charge: a fixed value per month that adds to the metered consumption |
| −2 | retroactive allowance: up to the allowance the fixed value is paid; beyond it, all the volume from zero is charged by the blocks |
| −3 | payment floor: the bill is not allowed to fall below the value |

The effect of each code on the bill is drawn in section {{n:29}}, and is not repeated here.

## The sewage part

<!-- tabela: The four ways of entering the sewage charge -->
| Mode | The sewage charge is |
| ---: | :--- |
| 0 | a fixed amount |
| 1 | a percentage of the water part (not of the whole bill) |
| 2 | an amount per m³ consumed |
| 3 | blocks (steps), applied to a fraction of the water volume that you declare |

Fixed and variable taxes can be added to the water part and to the electricity part. Tariff
escalation is entered separately for water, sewage and energy (appendix {{n:A}}).

## The six regimes

The program classifies a water tariff table into one of six regimes. The regime tells you
what saving water is worth, which is what a rainwater harvesting study needs to see.

<!-- tabela: The six tariff regimes and what happens when saving -->
| Regime | Structure | What happens when saving |
| :--- | :--- | :--- |
| **No minimum** | Progressive blocks only. | Each m³ saved reduces the bill. |
| **Availability charge** | A fixed value that **adds** on top of the metered consumption. | Each m³ saved reduces the bill; the fixed part remains. |
| **Allowance in the minimum** | The fixed value already includes a volume. | Saving **below** the allowance deducts nothing. |
| **Retroactive allowance** | Up to the allowance the fixed value is paid; beyond it, **everything from zero** is charged by the blocks. | Going past the allowance, the whole volume is billed from zero. |
| **Payment floor** | The bill does **not** go below the floor. | It does not add: it bounds. Savings that bring the bill under the floor earn nothing. |
| **Exponential formula** | Basic service plus `PB × Cⁿ`, with the exponent `n` set by the consumption of the month. | Each m³ saved reduces the bill, but not at a fixed price per m³. |

**Quick test.** Simulate two consumptions, one inside and one outside the minimum block, and
compare them with a real bill. If only one matches, the regime is wrong. Section {{n:16}}
teaches the test that identifies a wrong structure.

## The example tariffs that come with the edition

Three example projects (`examples/new_york.triton`, `london.triton` and `cape_town.triton`)
carry the water and sewage tariff of their city, as published by the utility and entered by
the maintainers on 14/10/2026. They are examples of how to enter a tariff, not a catalogue:
tariffs change every year, and you must check the current document of your utility before
any economic conclusion. The document address and file signature of each source have not
been recorded yet, so each value below is to be confirmed against the utility's current tariff.

### New York: NYC Water Board / NYC DEP

Currency USD; effective 01/07/2026 (as stated by the maintainers; confirm).

NYC Water Board and NYC Department of Environmental Protection (DEP), Water and Sewer Rates FY2027, in force from 1 July 2026: water US$ 5.35 per CCF (100 ft3 = 2.8316847 m3), sewer 159% of the water charge, minimum charge US$ 0.49 per day.

<!-- tabela: Tariff structure of the New York example -->
| Part | From (m³/month) | To (m³/month) | Value | Code |
| :--- | ---: | ---: | ---: | ---: |
| water | 0 | 0 | 14.9144 | -3 |
| water | 0 | open | 1.8893 | 1 |
| sewage | — | — | 159% of the water part | — |

Assumptions made when entering it:

- US$ 5.35 per CCF converted at 1 CCF = 2.8316847 m3 (US$ 1.8894 per m3).
- Sewer = 159% of the water charge (percentage of the water parcel, mode 1).
- The US$ 0.49 per day minimum charge is entered as a monthly floor on the water parcel (US$ 0.49 x 30.4375 days = US$ 14.91 per month); it does not bind at the example's consumption.

### London: Thames Water

Currency GBP; effective 01/04/2026 (as stated by the maintainers; confirm).

Thames Water, charges 2026-27, metered household: water GBP 2.7346 per m3 and wastewater GBP 1.4721 per m3; standing charges GBP 66.87 per year (water) and GBP 128.13 per year (wastewater; GBP 80.43 with the surface-water drainage rebate). No VAT on household water and sewerage.

<!-- tabela: Tariff structure of the London example -->
| Part | From (m³/month) | To (m³/month) | Value | Code |
| :--- | ---: | ---: | ---: | ---: |
| water | 0 | 0 | 5.5725 | -1 |
| water | 0 | open | 2.7346 | 1 |
| sewage | — | — | 1.4721 per m³ | — |
| fixed amount, per month | — | — | 10.6775 | — |

Assumptions made when entering it:

- Water standing charge GBP 66.87/12 per month on the water parcel; wastewater standing charge GBP 128.13/12 per month as a fixed amount (it cancels in the saving).
- Wastewater charged on 100% of the metered volume (no return-to-sewer allowance applied: none was supplied). The GBP 80.43 rebate case is not applied.
- Charging year 2026-27 taken to start on 1 April 2026 (inferred; confirm).

### Cape Town: City of Cape Town

Currency ZAR; effective 01/07/2026 (as stated by the maintainers; confirm).

City of Cape Town, Tariffs 2026/27, domestic (non-indigent), no restrictions, VAT included, R/kl: water 0-6 kl 25.05; 6-10.5 kl 34.42; 10.5-35 kl 54.60; >35 kl 109.98. Sanitation: 70% of the water consumption, up to 35 kl: 0-4.2 kl 18.28; 4.2-7.35 kl 25.11; 7.35-24.5 kl 42.18; 24.5-35 kl 73.91. Monthly standing charges (domestic 12-20 mm, VAT included): water R 103.65, sanitation R 56.66 (total R 160.31).

<!-- tabela: Tariff structure of the Cape Town example -->
| Part | From (m³/month) | To (m³/month) | Value | Code |
| :--- | ---: | ---: | ---: | ---: |
| water | 0 | 0 | 103.65 | -1 |
| water | 0 | 6 | 25.05 | 1 |
| water | 6 | 10.5 | 34.42 | 1 |
| water | 10.5 | 35 | 54.6 | 1 |
| water | 35 | open | 109.98 | 1 |
| sewage (on 70% of the water volume) | 0 | 4.2 | 18.28 | — |
| sewage (on 70% of the water volume) | 4.2 | 7.35 | 25.11 | — |
| sewage (on 70% of the water volume) | 7.35 | 24.5 | 42.18 | — |
| sewage (on 70% of the water volume) | 24.5 | 35 | 73.91 | — |
| fixed amount, per month | — | — | 56.66 | — |

Assumptions made when entering it:

- 1 kl = 1 m3; prices already include VAT (no extra tax is added).
- Sanitation volume = 70% of the water consumed, charged by the four steps up to 35 kl of sanitation volume; above that nothing more is charged (the cap is read from 'up to 35 kl'; confirm).
- Monthly standing charges (domestic 12-20 mm, VAT included): water R 103.65 on the water parcel and sanitation R 56.66 as a fixed amount (total R 160.31 per month; they cancel in the saving).
- Tariff year 2026/27 taken to start on 1 July 2026 (inferred; confirm).

## Entering your own tariff

1. Take the current tariff document of your water utility and write down its date.
2. Enter the blocks, the fixed charges and the sewage rule in the tariff dialog (stage 5).
3. Check the bill the program calculates against a real bill of the building.
4. Declare in the study the utility, the effective date, the regime and the currency.

