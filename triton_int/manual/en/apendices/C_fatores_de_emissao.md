# Emission factors

Every factor used by the life cycle assessment, with its provenance, boundary and degree of
confidence. The assessment is a **screening** one, not an inventory conforming to ISO 14040
(appendix {{n:G}}).

The International Edition separates the factors in two kinds.

- **User-supplied.** The factor of the electricity grid and the factor of the mains water delivered
  to the building depend on the place and the year of the project. The edition has no default for
  either: the fields start empty, and the life cycle assessment is not calculated until you enter
  them. You must obtain them from the supplier of the project's site or from a local inventory, and
  declare the source, the year and the boundary.
- **Screening factors of the program.** The factors for tank materials, pipes, the pump set and the
  treatment consumables are starting values, editable on screen. Each is listed below with the
  reference the program's source records for it. These references have not been re-verified for this
  edition of the manual (pending, see below), so treat every value as a screening assumption and
  replace it by an Environmental Product Declaration (EPD) of the product you specify whenever one
  exists.

---

## User-supplied factors

<!-- tabela: Emission factors that the user supplies, and what to declare for each -->
| Factor | Unit | Default | What to declare |
| :--- | :--- | :--- | :--- |
| electricity grid | kg CO₂e/kWh | none (empty) | source, **year**, whether it is CO₂ or CO₂e, and whether it covers generation only or also losses and upstream fuel |
| mains potable water delivered to the building | kg CO₂e/m³ | none (empty) | source, boundary, and whether the figure is per m³ **delivered** or per m³ produced |
| tank material, when you replace the preset | kg CO₂e/kg and kg/m³ | see below | source, version, boundary of the product system |

**The boundary is per cubic metre delivered to the building**, not per cubic metre produced at the
works. A factor given at the outlet of the works must be divided by the share of the produced volume
that reaches the building (one minus the distribution losses of the supplier), or the avoided
emission is underestimated.

**The grid factor changes every year**, and a study without the year declared cannot be reproduced.
A factor for CO₂ alone and a factor for CO₂-equivalent are different quantities: a life cycle
assessment needs the latter.

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
polyethylene. The masses are geometric scenarios of the program, not the weight of a product.

<!-- tabela: Reference recorded in the program for each tank-material factor, and its status -->
| Material | Reference recorded in the program | Status |
| :--- | :--- | :--- |
| polyethylene | Franklin Associates for the American Chemistry Council (October 2020), *Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin*, Table 6: 1,612 kg CO₂e per 1,000 kg of resin (TRACI 2.1, IPCC 2013 GWP-100, United States scope) | recorded; re-verification pending |
| concrete | screening value of 0.14 kg CO₂e/kg; Hammond and Jones (2008, doi:10.1680/ener.2008.161.2.87) publish a concrete value but the exact adopted value is not traced to it | screening, no source traced |
| fibreglass | Composites UK, *Embodied carbon data for composites*: typical range 2.5 to 4.0 kg CO₂e/kg; the midpoint is adopted | recorded; re-verification pending |
| stainless steel | worldstainless (World Steel Association), CO₂ emissions report of 24/09/2024, cradle to gate: 1.95 kg CO₂/kg at 85% scrap, 2.45 at 75%, 3.70 at 50%, 6.80 at 30%; the 50% scrap case is adopted | recorded; re-verification pending |

> **Practical consequence, shown in section {{n:11}}:** the material decides the **sign** of the
> environmental result. With concrete and a twenty-year service life, the tutorial system does not
> pay off its carbon debt.

---

## Pipes and pump set

PVC pipe is taken at 2.36 kg CO₂e per kilogram of installed pipe, modules A1 to A3 of an Environmental
Product Declaration (EPD Australasia S-P-05503, 25/11/2022, EN 15804+A2), multiplied by the linear
mass of the pipe for its nominal diameter. The linear masses are screening values: replace them with
the data sheet of the pipe you specify.

The pump set is taken at an intensity of 4.77 kg CO₂e per kilogram of pump, from the Grundfos EPD
EPD-GRU-20250340-CBA1-EN (2025, modules A1 to A3), applied to the mass of the pump. Enter the mass
of the pump you specify; where you hold the manufacturer's EPD for it, that prevails.

> **Declare it in the study.** The EPD is for a European circulator with on-board electronics, and
> its reference mass includes the packaging. The intensity per kilogram is an order-of-magnitude
> approximation, not an inventory of the installed pump.

Status of both references: recorded in the program, re-verification pending.

---

## Treatment consumables

<!-- tabela: Emission factors of the treatment consumables -->
| Consumable | Factor |
| :--- | ---: |
| calcium hypochlorite tablet at 65% | 1.72 kg CO₂e/kg of product |
| ultraviolet lamp | grid energy |
| ozone generator | grid energy |

The mass is of **product**, not of active chlorine. Tablets have about 65% active chlorine.

The hypochlorite factor is an approximation from a commercial database (ecoinvent 3.8, *cutoff*,
sodium hypochlorite in 15% solution, rest-of-world geography, EF 3.1 *Climate change*: 2.522 kg
CO₂e per kg of NaOCl, converted to an active-chlorine basis and to a 65% tablet). It has no calcium
hypochlorite process, and the database is not open: the factor is a **screening** value. If you hold
an open factor for the product you use, enter it in the field `chlorine_co2_kg_per_kg`.

---

## Factors with a screening label

Not every parameter has a primary source, and those without one are marked in the report: the masses
per useful cubic metre of polyethylene, concrete and stainless steel, which are geometric scenarios,
the concrete factor, the hypochlorite factor, and any factor typed in without a source. Factors you
enter without a source also receive the screening label. An inventory that presents all factors with
the same degree of confidence hides where the weakness lies.

---

## What to consult before publishing

1. the EPD or the data sheet of each product you specify;
2. the Documentation tab, life cycle assessment chapter, for the justifications shown to the user;
3. the inventory of the environmental report, which lists each item with the factor applied.
