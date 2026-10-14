# Emission factors

Every factor used by the life cycle assessment, with its provenance, boundary and degree of
confidence. The full detail, with the sources item by item, is in `docs/procedencia_fatores_co2.md`
(in Portuguese).

The material, treatment and pump factors below are the defaults of both editions. The water and
grid factors are Brazilian, and the International Edition does not ship them: there, the user enters
the emission factor of the local water supply and of the local grid.

---

## Tank materials

<!-- tabela: Emission factors of the tank materials, with mass and boundary -->
| Material | Mass per useful m³ | Factor | Boundary |
| :--- | ---: | ---: | :--- |
| high-density polyethylene | 22 kg/m³ | 1.612 kg CO₂e/kg | cradle to gate |
| reinforced concrete | 1,200 kg/m³ | 0.140 kg CO₂e/kg | cradle to gate |
| fibreglass | 15 kg/m³ | 3.250 kg CO₂e/kg | cradle to gate |
| stainless steel AISI 304 | 38 kg/m³ | 3.700 kg CO₂e/kg | cradle to gate |

The mass per useful cubic metre is what converts tank volume into mass of material. It is that, and
not the factor, that makes concrete dominate the inventory: 1,200 kg per cubic metre against 22 for
polyethylene.

> **Practical consequence, shown in section {{n:11}}:** the material decides the **sign** of the
> environmental result. With concrete and a twenty-year service life, the tutorial system does not
> pay off its carbon debt.

---

## Mains potable water

Nineteen production routes available, by macro-region and type of source.

**The boundary is per cubic metre delivered to the building**, not per cubic metre produced at the
works. The conversion uses the distribution losses of each macro-region ({{fig:fig43_perdas}}):

![The distribution losses by macro-region](../figuras/fig43_perdas.png)

*Figure 99 — How much of each cubic metre produced actually reaches the building, by Brazilian macro-region. It is this fraction that converts an emission factor at the outlet of the works into a factor per cubic metre delivered, and ignoring it underestimates the avoided emission by up to a third.*


---

## Electricity grid

The emission factor of the Brazilian grid changes **every year**, and a study without the year
declared cannot be reproduced. The program carries five reference databases and records which one
was used.

---

## Treatment consumables

<!-- tabela: Emission factors of the treatment consumables -->
| Consumable | Factor |
| :--- | ---: |
| calcium hypochlorite tablet at 65% | 1.72 kg CO₂e/kg of product |
| ultraviolet lamp | grid energy |
| ozone generator | grid energy |

The mass is of **product**, not of active chlorine. Tablets have about 65% active chlorine.

---

## Pump set

There is no Environmental Product Declaration for a Brazilian residential pump set. The program
builds the value from two sources it has read: the mass of each power rating, from the Dancor
catalogue, and the intensity of 4.77 kg CO₂e per kilogram of pump, from the Grundfos EPD
EPD-GRU-20250340-CBA1-EN (2025, modules A1 to A3).

<!-- tabela: Manufacturing emission of the pump set by power rating, with the catalogue mass -->
| Power | Mass | Manufacturing emission |
| ---: | ---: | ---: |
| 1/4 hp | 6.1 kg | 29.1 kg CO₂e |
| 1/2 hp | 6.4 kg | 30.5 kg CO₂e |
| 3/4 hp | 13.5 kg | 64.4 kg CO₂e |
| 1 hp | 15.3 kg | 73.0 kg CO₂e |
| 1 1/2 hp | 17.5 kg | 83.5 kg CO₂e |
| 2 hp | 20.7 kg | 98.8 kg CO₂e |

> **Declare it in the study.** The EPD is for a European circulator with on-board electronics, and
> the reference mass includes the packaging. The intensity per kilogram is an order-of-magnitude
> approximation, not an inventory of the installed pump; where there is an EPD from the manufacturer
> used, it prevails. The previous values, from 12 to 55 kg CO₂e, were 1.7 to 2.7 times below these,
> and four of them were arithmetic extrapolations.

---

## Factors with a screening label

Not every parameter has a primary source, and those without one are marked in the report: today, the
masses per useful cubic metre of polyethylene, concrete and stainless steel, which are geometric
scenarios, and any factor typed in without a source. In the September 2026 revision, the last default
emission factor without provenance, that of hypochlorite, received it:

<!-- tabela: Provenance of the hypochlorite emission factor -->
| Step | Value |
| :--- | :--- |
| database and model | Ecoinvent 3.8, *cutoff* |
| process | *sodium hypochlorite production, product in 15% solution state*, geography RoW (rest of the world) |
| method | EF 3.1, *Climate change* category |
| result | 2.522 kg CO₂e per kg of pure NaOCl |
| conversion | 0.9525 kg of active chlorine per kg of NaOCl, hence 2.65 kg CO₂e per kg of active chlorine |
| factor adopted | 2.65 × 0.65 = **1.72 kg CO₂e per kg of tablet** |

> **Declare the approximation.** Ecoinvent 3.8 has no calcium hypochlorite, and the factor is that of
> sodium hypochlorite brought to an active-chlorine basis. Factors entered by the user without a
> source still receive the screening label, and an inventory that presents all factors with the same
> degree of confidence hides where the weakness lies.

---

## What to consult before publishing

1. `docs/procedencia_fatores_co2.md`, for the source item by item;
2. the Documentation tab, life cycle assessment chapter, for the justifications shown to the user;
3. the inventory of the environmental report, which lists each item with the factor applied.
