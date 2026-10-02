# Tariff regimes

> **Brazil Edition.** The tariff catalogue is Brazilian and ships only with the Brazil
> Edition. In the International Edition the tariff is entered by the user, in one of
> the same six regimes, and this appendix serves as a description of them.

The database holds **652 municipalities** with tariff structure, sewage
percentage, minimum-charge regime, effective date and source. This list is extracted
from the program's own database, not transcribed.

## The block codes

Each row of the tariff table is a quadruple `(minimum, maximum, value, code)`.

The six codes and the effect of each on the bill are drawn in section {{n:29}}, and are not repeated here.


## The six regimes

<!-- tabela: Distribution of the catalogue municipalities across the six tariff regimes -->
| Regime | Municipalities | What happens when saving |
| :--- | ---: | :--- |
| **No minimum** | 165 | Each m³ saved reduces the bill. |
| **Availability charge** | 122 | A fixed value that **adds** on top of the metered consumption. Each m³ saved is deducted. |
| **Allowance in the minimum** | 329 | The fixed value already includes a volume. Saving **below** the allowance deducts nothing. |
| **Retroactive allowance** | 2 | Up to the allowance the fixed value is paid; beyond it, **everything from zero** is charged. |
| **Payment floor** | 0 | The bill does **not** go below the floor. It does not add: it bounds. |
| **Exponential formula** | 34 | Basic service plus `PB × Cⁿ`, with `n` set by the month's consumption (CORSAN). Each m³ saved is deducted. |

> The payment floor is implemented, and no municipality in the database had been
> classified under it as of this version.

## Distribution by state

The catalogue coverage follows the population, not the territory: the state capitals and the metropolitan regions are almost all registered, and the interior of the North and Centre-West regions concentrates the municipalities still missing ({{fig:fig42_uf}}).

![The catalogue municipalities, by state](../figuras/fig42_uf.png)

*Figure 99 — The distribution of the 652 catalogued municipalities across the Brazilian states, with colours identifying the macro-region. São Paulo and Minas Gerais alone account for almost a third of the catalogue.*


## Updating and auditing the database

The tariff database is maintained by the group with an update routine run outside the interface, before each version. The routine has three components.

**Electricity.** The residential tariffs of subgroup B1 are read from the open database of approved distributor tariffs published by the Brazilian Electricity Regulatory Agency (ANEEL), and associated with the distributor of each catalogue municipality.

**Water and sewage.** A register of primary evidence associates each provider with the regulatory agency, the official tariff page and the type of act that publishes them. Providers with a standard portal are read automatically; the others are flagged for manual checking of the decree or resolution, and the resulting structure goes through the same regime validation described in this appendix.

**Change detection.** Each monitored official page is recorded with the SHA-256 signature of its content and the `ETag` and `Last-Modified` headers. A new check compares the signatures and points out the pages changed since the last collection, which are the candidates for a tariff revision.

The routine can simulate the update without writing the database, run only the change detection, restrict itself to one state or one municipality, and separate electricity from sanitation. Each run writes an audit report in Markdown and an HTML panel with the status of each municipality.

## Confidence grade

Each record carries the confidence grade of the collection:

<!-- tabela: Confidence grade of the tariff records in the catalogue -->
| Grade | Records |
| :--- | ---: |
| A — high | 580 |
| B — good | 63 |
| C — structure to be checked | 5 |
| D — incomplete structure | 4 |

> **Always check the effective date** of your municipality's record against the
> utility's resolution. Tariffs are adjusted every year, and section {{n:16}}
> teaches the test that identifies a wrong structure.

