# Netuno 5

## User Manual

Igor Catão Martins Vaz and Enedir Ghisi

Sustainable Environments Research Group
Federal University of Santa Catarina

Florianópolis, Brazil, 2026

Version 5.0.0 · revised 2026-10-02

---

### Publication record

| Element | Content |
| :--- | :--- |
| **Title** | Netuno 5: user manual |
| **Authors** | Igor Catão Martins Vaz; Enedir Ghisi |
| **Edition** | Version 5.0.0, English translation |
| **Place** | Florianópolis, SC, Brazil |
| **Publisher** | Federal University of Santa Catarina |
| **Research group** | Sustainable Environments |
| **Year** | 2026 |
| **Licence** | GNU General Public License v3.0 |

### How to cite

**Author-date style**

> Vaz, I. C. M., & Ghisi, E. (2026). *Netuno 5: user manual*
> (Version 5.0.0). Federal University of Santa Catarina.

**BibTeX**

```
@manual{netuno5manual2026en,
  title     = {Netuno 5: user manual},
  author    = {Vaz, Igor Catão Martins and Ghisi, Enedir},
  edition   = {Version 5.0.0},
  address   = {Florianópolis},
  publisher = {Federal University of Santa Catarina},
  year      = {2026}
}
```

When citing results obtained with the program, also state the version used and
the source of the rainfall series, following the list in section 4.10.

---

### About this translation

This is the English translation of the Portuguese manual, chapter by chapter, with
the same section numbers, figures, tables and equations. The Portuguese text is the
reference: where the two differ, the Portuguese one prevails, and the difference is
a defect to be reported (section 6.4).

Netuno comes in two editions built from the same code (section 1.2). The
**Brazil Edition (BRL)** ships with Brazilian data: the CLIMBra climate database,
the catalogue of municipal water and electricity tariffs, the grid emission factors
and the Brazilian certifications. The **International Edition (INT)** ships without
them, and the user supplies the rainfall series, the tariff, the currency and the
emission factors. Both editions calculate in the same way. Where a section describes
a feature that only the Brazil Edition offers, it says so at the top.

The figures are shared with the Portuguese manual, and the labels drawn inside some
of them are in Portuguese; each caption, in English, says what the figure shows.
Numbers follow the English convention (a point for decimals, a comma for
thousands). Brazilian standards are cited by their Portuguese titles, with an
English description where needed.

---

### How to use this manual

It was not written to be read from cover to cover. Section 1.3 tells you where
to enter, depending on what you want to do.

| You want to | Read |
| :--- | :--- |
| learn to use the program | chapter 4, the tutorial |
| solve a case | chapter 3, the guides |
| publish a study | chapter 2, the method; and section 4.10 |
| review a study | chapter 5, and appendices A and B |
| avoid mistakes | section 5.1 |

The manual assumes an engineering reader who does not yet know the subject: concepts
are introduced before they are used, and the vocabulary is in appendix G. Two
kinds of box appear throughout the text:

| The box | When it appears |
| :--- | :--- |
| with a **blue** rule | a warning or remark that changes what you do |
| with an **orange** rule, marked *In depth* | the technical detail behind it; can be skipped on a first reading |

> **Every number printed in this manual is calculated by the program.** The tables
> and figures were not typed: they are produced by running Netuno with the input
> data each section declares. Each published value has a matching automatic check,
> so that a fix in the program cannot leave the manual lying. Section 5.3
> explains how this is done.

---

## Contents

**1 Start here**

1.1 What Netuno does, and what it does not

1.2 Installation and first run

1.3 Where to start, depending on your goal


**2 The method**

2.1 The daily water balance

2.2 Ideal volume and the sweep

2.3 Efficiency indicators

2.4 Rainfall indices

2.5 Sizing the treatment line

2.6 Pumping energy

2.7 Economic analysis and tariff regimes

2.8 Life cycle assessment

2.9 Certifications

2.10 Multi-criteria decision


**3 Guides available in the program**

3.1 Comparing cities

3.2 Using a future climate scenario

3.3 Adjusting the tariff of your municipality

3.4 Modulating the demand by calendar

3.5 Simulating schools, hospitals and shops

3.6 Comparing many cases at once

3.7 Sensitivity analysis

3.8 Importing a Netuno 4 project

3.9 Exporting to CAD, BIM and spreadsheets


**4 Tutorial: one example from start to finish**

4.1 The project and the rain

4.2 The building and the demand

4.3 The first simulation

4.4 Choosing the volume

4.5 Is an upper tank needed?

4.6 What quality the use requires

4.7 What it costs and how fast it pays back

4.8 How much carbon it avoids

4.9 Which volume to choose, after all

4.10 The report, and what to declare in a paper


**5 Mistakes, limitations and reliability**

5.1 Ten mistakes the program does not prevent

5.2 Known limitations

5.3 How the program is verified


**6 Fixes, bugs and versioning**

6.1 Comparison with Netuno 4

6.2 Error messages and what to do

6.3 Version history and what changed

6.4 How to report a problem


**Appendices**

Appendix A — The project parameters

Appendix B — The program's processes

Appendix C — Emission factors

Appendix D — Tariff regimes

Appendix E — Climate database

Appendix F — Files, folders and formats

Appendix G — Glossary

Appendix H — References

Appendix I — One-page summaries

Appendix J — Example files



## List of figures

Figure 1 — The distribution of the 652 catalogued municipalities across the Brazilian states, with colours identifying the macro-region

---

## List of tables

Table 1 — Project parameters: identification

Table 2 — Project parameters: rainfall

Table 3 — Project parameters: catchment

Table 4 — Project parameters: building

Table 5 — Project parameters: demand

Table 6 — Project parameters: irrigation

Table 7 — Project parameters: water quality

Table 8 — Project parameters: tanks

Table 9 — Project parameters: pump set

Table 10 — Project parameters: piping

Table 11 — Project parameters: investment

Table 12 — Project parameters: operation

Table 13 — Project parameters: tariffs

Table 14 — Project parameters: energy

Table 15 — Project parameters: incentives

Table 16 — Project parameters: financial

Table 17 — Project parameters: certifications

Table 18 — Project parameters: other

Table 19 — Distribution of the catalogue municipalities across the six tariff regimes

Table 20 — Confidence grade of the tariff records in the catalogue

---


---
# 1. Start here

---

## 1.1. What Netuno does, and what it does not

> **Section not yet written.**

---

## 1.2. Installation and first run

> **Section not yet written.**

---

## 1.3. Where to start, depending on your goal

> **Section not yet written.**

---

# 2. The method

---

## 2.1. The daily water balance

> **Section not yet written.**

---

## 2.2. Ideal volume and the sweep

> **Section not yet written.**

---

## 2.3. Efficiency indicators

> **Section not yet written.**

---

## 2.4. Rainfall indices

> **Section not yet written.**

---

## 2.5. Sizing the treatment line

> **Section not yet written.**

---

## 2.6. Pumping energy

> **Section not yet written.**

---

## 2.7. Economic analysis and tariff regimes

> **Section not yet written.**

---

## 2.8. Life cycle assessment

> **Section not yet written.**

---

## 2.9. Certifications

> **Section not yet written.**

---

## 2.10. Multi-criteria decision

> **Section not yet written.**

---

# 3. Guides available in the program

---

## 3.1. Comparing cities

> **Section not yet written.**

---

## 3.2. Using a future climate scenario

> **Section not yet written.**

---

## 3.3. Adjusting the tariff of your municipality

> **Section not yet written.**

---

## 3.4. Modulating the demand by calendar

> **Section not yet written.**

---

## 3.5. Simulating schools, hospitals and shops

> **Section not yet written.**

---

## 3.6. Comparing many cases at once

> **Section not yet written.**

---

## 3.7. Sensitivity analysis

> **Section not yet written.**

---

## 3.8. Importing a Netuno 4 project

> **Section not yet written.**

---

## 3.9. Exporting to CAD, BIM and spreadsheets

> **Section not yet written.**

---

# 4. Tutorial: one example from start to finish

---

## 4.1. The project and the rain

> **Section not yet written.**

---

## 4.2. The building and the demand

> **Section not yet written.**

---

## 4.3. The first simulation

> **Section not yet written.**

---

## 4.4. Choosing the volume

> **Section not yet written.**

---

## 4.5. Is an upper tank needed?

> **Section not yet written.**

---

## 4.6. What quality the use requires

> **Section not yet written.**

---

## 4.7. What it costs and how fast it pays back

> **Section not yet written.**

---

## 4.8. How much carbon it avoids

> **Section not yet written.**

---

## 4.9. Which volume to choose, after all

> **Section not yet written.**

---

## 4.10. The report, and what to declare in a paper

> **Section not yet written.**

---

# 5. Mistakes, limitations and reliability

---

## 5.1. Ten mistakes the program does not prevent

> **Section not yet written.**

---

## 5.2. Known limitations

> **Section not yet written.**

---

## 5.3. How the program is verified

> **Section not yet written.**

---

# 6. Fixes, bugs and versioning

---

## 6.1. Comparison with Netuno 4

> **Section not yet written.**

---

## 6.2. Error messages and what to do

> **Section not yet written.**

---

## 6.3. Version history and what changed

> **Section not yet written.**

---

## 6.4. How to report a problem

> **Section not yet written.**

---

# Appendices

---

## Appendix A — The project parameters

There are **115 parameters**. This is the complete list of what a project
stores, with the exact name of each field inside the `.netuno` file.

The list was not transcribed by hand: it is extracted from the program itself for
each version, and therefore cannot diverge from it.

The column **where it is entered** says on which screen the field appears; the
column **who consumes it** says which calculation uses it. A field with neither is a
field stored in the file and never read, and is listed in section 5.2.

Defaults in currency are the Brazil Edition ones, in reais (R$); the International
Edition starts the costs and tariffs at zero, for the user to enter in the currency
of the project.

### A.1. Identification

3 parameters.

<!-- tabela: **Table 1** — Project parameters: identification -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | New Netuno project | — | Export, Main window, Reports | Automation, CAD and BIM, Reports, Spreadsheets |
| `project_id` | — | — | Main window, Reports | Automation |
| `created_at` | — | — | Main window | — |

### A.2. Rainfall

9 parameters.

<!-- tabela: **Table 2** — Project parameters: rainfall -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Main window, Project | Automation, Scenarios, Spreadsheets |
| `climate_source_mode` | national_db | — | — | — |
| `climate_city_uf` | SC | — | Project, Reports | — |
| `climate_city_name` | Florianópolis | — | Project, Reports | — |
| `climate_model` | INM-CM4 | — | Project, Reports | — |
| `climate_scenario` | HIST | — | Project, Reports | — |
| `climate_start_date` | 1980-01-01 | — | Reports | — |
| `climate_end_date` | 2013-12-31 | — | Project, Reports | — |
| `start_date` | 1980-01-01 | — | Main window, Project, Tariffs and costs | Automation, Climate |

Notes from the code:

- `climate_source_mode`: "national_db" (national database, Brazil Edition) or "custom_file" (own file)

### A.3. Catchment

7 parameters.

<!-- tabela: **Table 3** — Project parameters: catchment -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | — | mm | Charts, Documentation, Environmental, Main window, Project, Quality, Reports | Automation, CAD and BIM, LCA, Reports, Scenarios, Spreadsheets, Treatment line |
| `discard_mode` | 1 | code | Main window, Project, Sweep | Automation, Daily balance, Scenarios |
| `discard_days_interval` | 7 | days | Main window, Project, Sweep | Automation, Daily balance, Scenarios |
| `area` | 100 | m² | Building, Charts, Documentation, Environmental, Main window, Quality, Reports, Sweep | Automation, CAD and BIM, Daily balance, LCA, Reports, Scenarios, Spreadsheets, Treatment line |
| `irrigation_garden_area_m2` | 0 | m² | — | — |
| `runoff_coeff` | — | — | Building, Main window, Quality, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `first_flush_system_enabled` | no | — | Environmental, Quality | Automation, LCA, Treatment line |

Notes from the code:

- `discard`: mm
- `discard_mode`: 1 = every event, 2 = first event after a dry spell, 3 = every X days
- `discard_days_interval`: interval for mode 3
- `area`: m²
- `irrigation_garden_area_m2`: Garden area in m² for the sizing wizard
- `runoff_coeff`: see hydrology_defaults

### A.4. Building

2 parameters.

<!-- tabela: **Table 4** — Project parameters: building -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | units | Building, Environmental | Automation, Economic |
| `building_template_id` | res_medio | — | Building | Automation, Tariffs |

Notes from the code:

- `num_economias`: Number of dwelling units / apartments with individual metering

### A.5. Demand

17 parameters.

<!-- tabela: **Table 5** — Project parameters: demand -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `demand_type` | 0 | code | — | — |
| `demand_mode` | constant | — | Building, Environmental, Main window, Reports, Sweep | Automation, Daily balance |
| `demand_value` | 200 | L/day | Documentation, Economic, Main window | Automation, Daily balance |
| `demand_monthly` | — | — | Main window | Automation |
| `residents_type` | 0 | code | — | — |
| `residents_count` | 4 | residents | Economic, Environmental, Main window | Automation, Daily balance, Pump set |
| `residents_monthly` | — | — | Main window | Automation |
| `potable_indoor_share` | 0.6 | fraction | Building, Main window | Automation |
| `non_potable_indoor_share` | 0.4 | fraction | Building, Main window | Automation, Daily balance |
| `rainwater_share` | 0.4 | fraction | Documentation, Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `weekly_demands` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `weekly_residents` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `weekly_shares` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `monthly_shares` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `daily_demands` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `daily_residents` | — | — | Building, Main window, Sweep | Automation, Daily balance |
| `daily_shares` | — | — | Building, Main window, Sweep | Automation, Daily balance |

Notes from the code:

- `demand_mode`: "constant", "weekly", "monthly", "daily"
- `demand_value`: L/day, per resident or total
- `potable_indoor_share`: Potable fraction of indoor consumption; 1 − non_potable_indoor_share
- `non_potable_indoor_share`: Non-potable fraction of indoor consumption (toilets, washing machine); see fracao_atendivel
- `rainwater_share`: fraction from 0 to 1 (0.4 = 40%)

### A.6. Irrigation

4 parameters.

<!-- tabela: **Table 6** — Project parameters: irrigation -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `irrigation_liters_per_day` | 0 | L/day | Building, Environmental, Main window, Reports | Automation, Daily balance |
| `irrigation_rain_threshold_mm` | 2 | mm/day | Building, Main window | Automation, Daily balance |
| `irrigation_potable_backup` | yes | — | Building, Main window | Automation, Daily balance |
| `irrigation_rate_l_m2_day` | 3 | L/m²·day | — | — |

Notes from the code:

- `irrigation_liters_per_day`: Outdoor demand (watering, washing outdoor areas), L/day
- `irrigation_rain_threshold_mm`: Daily precipitation threshold that suppresses irrigation (mm/day)
- `irrigation_potable_backup`: If True, the mains supplies irrigation on dry days when the cistern runs dry
- `irrigation_rate_l_m2_day`: Daily watering rate (L/m²/day)

### A.7. Water quality

9 parameters.

<!-- tabela: **Table 7** — Project parameters: water quality -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `water_quality_target_class` | classe_1 | — | Environmental, Quality | Automation, LCA, Treatment line |
| `water_quality_disinfection` | cloro | — | Environmental, Quality | Automation, LCA, Treatment line |
| `water_quality_polishing` | no | — | Environmental, Quality | Automation, LCA, Treatment line |
| `etap_enabled` | yes | — | Economic, Environmental, Optimiser | Automation, LCA, Treatment line |
| `chlorine_treatment_enabled` | yes | — | Economic, Environmental, Optimiser, Quality | Automation, Economic, LCA |
| `chlorine_dose_mg_l` | — | mg Cl₂/L | Economic, Environmental, Optimiser, Quality | Automation, Economic, LCA, Reports, Treatment line |
| `chlorine_product_purity` | — | kg/kg | Environmental, Quality | Automation, Economic, LCA, Treatment line |
| `chlorine_cost_per_kg` | 25 | R$/kg | Economic, Optimiser, Quality | Automation, Economic, Prices, Treatment line |
| `chlorine_co2_kg_per_kg` | — | kg CO₂e/kg | Environmental, Quality | Automation, LCA, Treatment line |

Notes from the code:

- `water_quality_disinfection`: "cloro" (chlorine), "uv", "ozonio" (ozone), "nenhum" (none)
- `chlorine_dose_mg_l`: mg of active Cl2 per litre
- `chlorine_product_purity`: kg of active Cl2 per kg of product
- `chlorine_cost_per_kg`: price per kg of commercial PRODUCT

### A.8. Tanks

12 parameters.

<!-- tabela: **Table 8** — Project parameters: tanks -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | L | Economic, Environmental, Export, Main window, Optimiser, Pump wizard, Reports, Sweep, Tariffs and costs, Upper tank | Automation, CAD and BIM, Daily balance, Multi-criteria, Scenarios, Spreadsheets |
| `upper_tank_used` | 1 | code | Economic, Environmental, Main window, Optimiser, Reports, Sweep, Tariffs and costs | Automation, Daily balance, LCA, Pump set, Scenarios, Spreadsheets |
| `lower_tank_max` | 10000 | L | Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `lower_tank_step` | 250 | L | Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `lower_tank_mode` | 1 | code | Main window, Sweep | Automation |
| `lower_tank_fixed` | 2000 | L | Main window, Sweep, Tariffs and costs | Automation |
| `delta_ideal` | 5 | %/m³ | Main window, Optimiser, Sweep | Automation, Scenarios |
| `econ_lower_tank_vol` | 2000 | L | Economic, Environmental, Sweep, Tariffs and costs | Automation |
| `lower_tank_material` | PEAD | — | Economic, Optimiser, Tariffs and costs | Automation, LCA |
| `upper_tank_material` | PEAD | — | Economic, Optimiser, Tariffs and costs | Automation, LCA |
| `cost_lower_tank` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |
| `cost_upper_tank` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |

Notes from the code:

- `upper_tank_vol`: L
- `upper_tank_used`: 0 = no upper tank, 1 = with upper tank
- `lower_tank_max`: L
- `lower_tank_step`: L
- `lower_tank_mode`: 0 = fixed volume, 1 = sweep
- `lower_tank_fixed`: used in fixed-volume mode
- `delta_ideal`: marginal-gain threshold for the ideal volume, in %/m³
- `lower_tank_material`: "PEAD" (HDPE), "CONCRETO" (concrete), "FIBRA" (GRP), "ACO_INOX" (stainless steel)
- `upper_tank_material`: "PEAD" (HDPE), "CONCRETO" (concrete), "FIBRA" (GRP), "ACO_INOX" (stainless steel)

### A.9. Pump set

18 parameters.

<!-- tabela: **Table 9** — Project parameters: pump set -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `pumping_threshold` | 50 | L | Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `supply_arrangement` | — | code | Economic, Environmental, Sweep | Automation, Economic, LCA, Pump set |
| `pressurizer_pressure_m` | 18 | m head | Sweep | Pump set |
| `pressurizer_starts_per_person_day` | 5.05 | 1/person·day | Sweep | Pump set |
| `pressurizer_model` | komeco_tp820t | code | Sweep | Pump set |
| `pressurizer_point_flow_l_min` | 9 | L/min | Sweep | Pump set |
| `pressurizer_power_kw` | 0.18 | kW | Sweep | Pump set |
| `pressurizer_flow_l_min` | 13.3 | L/min | Sweep | Pump set |
| `pressurizer_post_run_s` | 0 | s | Sweep | Pump set |
| `pump_count` | 2 | units | Economic, Environmental, Optimiser, Reports, Tariffs and costs | Automation, Economic, LCA, Prices, Reports |
| `pump_power_str` | 1/2 | — | Reports | — |
| `pump_power_kw` | 0.36775 | kW | Charts, Economic, Optimiser, Reports, Sweep, Tariffs and costs | Automation, CAD and BIM, Economic, Prices, Pump set, Reports |
| `pump_manometric_head_m` | 0 | m head | Sweep | Automation, Pump set |
| `pump_efficiency` | 0 | % | Charts, Sweep, Tariffs and costs | Automation, Pump set |
| `pump_flow_rate` | 0 | L/h | Charts, Economic, Optimiser, Reports, Sweep, Tariffs and costs | Automation, Pump set |
| `pump_startup_time_h` | 0.03 | h | Charts, Economic, Optimiser, Tariffs and costs | Automation, Pump set |
| `pump_motor_efficiency` | 0 | % | Tariffs and costs | Automation, Pump set |
| `pump_unit_cost` | 300 | R$ | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic, Prices |

Notes from the code:

- `pumping_threshold`: L, pump trigger level
- `pump_count`: duty + standby as the recommended initial configuration
- `pump_power_kw`: kW (1 hp (metric) = 0.7355 kW; 1/2 hp = 0.36775 kW)
- `pump_efficiency`: %, 0 = deduce from the size
- `pump_startup_time_h`: h
- `pump_motor_efficiency`: %
- `pump_unit_cost`: R$, Brazilian market reference for a 1/2 hp peripheral pump (zero in the International Edition)

### A.10. Piping

1 parameter.

<!-- tabela: **Table 10** — Project parameters: piping -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Economic, Tariffs and costs | Automation, LCA |

### A.11. Investment

3 parameters.

<!-- tabela: **Table 11** — Project parameters: investment -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |
| `cost_piping` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |
| `cost_accessories` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic, Treatment line |

### A.12. Operation

1 parameter.

<!-- tabela: **Table 12** — Project parameters: operation -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |

### A.13. Tariffs

14 parameters.

<!-- tabela: **Table 13** — Project parameters: tariffs -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | no | — | Project | — |
| `water_tariffs` | — | — | Project, Sweep, Tariffs, Tariffs and costs | Economic |
| `tariff_city_uf` | SC | — | Main window, Project, Reports, Tariffs, Tariffs and costs | — |
| `tariff_city_name` | Florianópolis | — | Main window, Project, Reports, Tariffs, Tariffs and costs | — |
| `sewage_rate` | 100 | % of water | Project, Tariffs, Tariffs and costs | Automation, Economic, Tariffs |
| `sewage_mode` | 1 | code | Economic, Optimiser, Project, Tariffs, Tariffs and costs | Automation, Economic, Tariffs |
| `water_tax_fixed` | 0 | R$/month | Tariffs and costs | Automation, Economic |
| `water_tax_var` | 0 | % | Tariffs and costs | Automation, Economic |
| `tariff_escalation` | 12 | months | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `water_tariff_escalation` | 5 | % per period | Economic, Optimiser, Sweep | Automation, Economic |
| `sewage_tariff_escalation` | 5 | % per period | Economic, Optimiser | Automation, Economic |
| `elec_tariff_escalation` | 5 | % per period | Economic, Optimiser, Sweep | Automation, Economic |
| `tariff_flag` | verde | — | Economic | Automation, Economic |
| `elec_tariff` | 0.6957 | R$/kWh | Charts, Economic, Optimiser, Project, Sweep, Tariffs and costs | Automation, Economic |

Notes from the code:

- `sewage_mode`: 0 = fixed amount, 1 = percentage of the water part, 2 = amount per m³ consumed
- `water_tax_fixed`: currency
- `water_tax_var`: %
- `tariff_escalation`: months; length of the escalation period
- `water_tariff_escalation`: % per escalation period; with 12 months, % per year
- `sewage_tariff_escalation`: % per escalation period; with 12 months, % per year
- `elec_tariff_escalation`: % per escalation period; with 12 months, % per year
- `tariff_flag`: "verde" (green), "amarela" (yellow), "vermelha_1" (red 1), "vermelha_2" (red 2), "branca" (white); Brazil Edition
- `elec_tariff`: per kWh (Brazil Edition default: residential B1 tariff, CELESC, Florianópolis)

### A.14. Energy

4 parameters.

<!-- tabela: **Table 14** — Project parameters: energy -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | SC | — | Main window, Project, Tariffs and costs | — |
| `elec_city_name` | Florianópolis | — | Main window, Project, Tariffs and costs | — |
| `elec_tax_fixed` | 0 | R$/month | Tariffs and costs | Automation, Economic |
| `elec_tax_var` | 0 | % | Tariffs and costs | Automation, Economic |

Notes from the code:

- `elec_tax_fixed`: currency
- `elec_tax_var`: %

### A.15. Incentives

3 parameters.

<!-- tabela: **Table 15** — Project parameters: incentives -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `iptu_green_enabled` | no | — | Economic, Optimiser | Automation, Economic |
| `iptu_annual_value` | 4000 | R$/year | Economic, Optimiser | Automation, Economic |
| `iptu_discount_pct` | 5 | % | Economic, Optimiser | Automation, Economic |

Notes from the code:

- `iptu_annual_value`: Annual municipal property tax (IPTU) of the building, per year; Brazil Edition
- `iptu_discount_pct`: Municipal green property-tax discount (IPTU Verde, %); Brazil Edition

### A.16. Financial

4 parameters.

<!-- tabela: **Table 16** — Project parameters: financial -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0.2 | % per month | Documentation, Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `analysis_period_years` | 20 | years | Economic, Optimiser, Reports, Sweep, Tariffs and costs | Automation, Economic, LCA, Reports |
| `tma` | 2 | % per month | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic, Spreadsheets |
| `install_month` | 0 | month | — | — |

Notes from the code:

- `inflation`: % per month; inflation of O&M costs
- `analysis_period_years`: years
- `tma`: % per month; minimum attractive rate of return

### A.17. Certifications

1 parameter.

<!-- tabela: **Table 17** — Project parameters: certifications -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | L/person·day | Environmental | — |

### A.18. Other

3 parameters.

<!-- tabela: **Table 18** — Project parameters: other -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `bim_layout` | — | — | Export, Main window | — |
| `capex_do_arranjo` | no | — | Main window, Sweep, Tariffs and costs | Treatment line |
| `mao_de_obra_automatica` | no | — | Main window, Sweep, Tariffs and costs | — |

---

## Appendix B — The program's processes

There are **24 processes**, from the rainfall file to the report. Each
one declares what triggers it, what it receives, the rules with their branches, what
it produces and what happens when it fails.

It is the most technical appendix of the manual, and it serves two people: whoever
reviews a study made with the program and needs to know exactly which calculation was
done, and whoever found a strange result and wants to know where the number went through.

The names in `code` are the project file fields, listed in appendix A.

### B.1. PROC-01 — Load the precipitation series

*Rainfall*

**Trigger.** Project tab: choose a city in the national database or open a CSV file.

**Inputs**

- Daily CSV file, or a city of the CMIP6 database (652 cities, 19 models, historical plus SSP2-4.5 and SSP5-8.5)
- `climate_start_date` and `climate_end_date`, which trim the series
- `start_date`, the date of the first day of the series

**Rules**

1. The series becomes a `numpy` vector of millimetres per day; the vector index is the day, and the date only serves to know the weekday and the month.
2. An incomplete year is dropped on reading, so as not to bias annual totals.
3. The climate database ships embedded in the Brazil Edition, in `climbra.db`; in the International Edition, which does not include it, the series is always a user file.

**Outputs**

- `precip_data`: vector of mm/day, which is the input of **two** distinct processes — PROC-04 (first flush and collection) and PROC-03 (irrigation suppression)

**Exception.** An unreadable file or one without a rainfall column stops loading with a message; the simulation does not run on an empty series.

### B.2. PROC-02 — Build the daily demand

*Demand*

**Trigger.** Start of the simulation, once per run.

**Inputs**

- `demand_mode`: constant, weekly, monthly or daily
- `demand_value` (L/day per person), `residents_count`
- `rainwater_share` or `non_potable_indoor_share`
- vectors `weekly_*`, `monthly_*`, `daily_*` when the mode uses them

**Rules**

1. Base demand of the day = `demand_value × residents_count`, with the multiplier of the weekday, month or day, depending on the mode.
2. The non-potable fraction splits the demand in two: indoor potable and indoor non-potable.
3. When the mode is weekly, monthly or daily, the fraction comes from the period vector itself; otherwise `non_potable_indoor_share` applies, and only then `rainwater_share`.
4. A null or zero value at any position of the vector falls back to the constant value.

**Outputs**

- `tot_arr`: total demand of the day
- `pot_in_arr`: indoor potable, which rain never supplies
- `non_pot_in_arr`: indoor non-potable, rain priority 1
- `pluv_arr` = indoor non-potable + active irrigation

**Exception.** An unreadable start date falls back to 01/01/1980 instead of stopping, because it only affects the weekday.

### B.3. PROC-03 — Suppress irrigation on rainy days

*Demand*

**Trigger.** Demand composition, one test per day of the series.

**Inputs**

- `irrigation_liters_per_day`
- `irrigation_rain_threshold_mm` (default 2 mm/day)
- `precip_data`, the **same** vector that feeds the collection

**Rules**

1. If the day's rain ≥ threshold, the day's irrigation is **zero** and the day is counted as suppressed.
2. Otherwise, the day's irrigation is the nominal volume.
3. It is the second reading of the rainfall file, independent of the first: a day can suppress irrigation and still yield collection.

**Outputs**

- `irr_arr`: irrigation of the day
- `irr_suppressed_mask`: suppressed days, which become `total_irrigation_days_suppressed` in the result

**Exception.** Without an irrigation volume, the vector is zero and the mask is false on every day.

### B.4. PROC-04 — Divert the first flush

*Water balance*

**Trigger.** Every day with rain, inside the daily loop.

**Inputs**

- `precip_mm` of the day
- `discard_mm`
- `discard_mode` (1, 2 or 3)
- `discard_days_interval`

**Rules**

1. **Mode 1**: diverts on every rain event.
2. **Mode 2**: diverts only on the first event after a dry spell, defined as a previous day with less than 1 mm.
3. **Mode 3**: diverts when `discard_days_interval` days have passed since the last diversion.
4. When the diversion applies: `p_eff = p − discard_mm` if `p > discard_mm`, otherwise **zero**: all the day's rain goes to the diverter.
5. When it does not apply: `p_eff = p`, the whole rain is usable.

**Outputs**

- `p_eff`: effective depth of the day, in mm, which goes **only** to PROC-05
- `eff_precip_mm` in the detailed daily series, when it is kept

**Exception.** A negative first-flush depth is rejected at the validation gate, before the loop.

### B.5. PROC-05 — Convert depth into collected volume

*Water balance*

**Trigger.** Every day, after the first flush.

**Inputs**

- `p_eff` from PROC-04
- `area` (m²)
- `runoff_coeff`

**Rules**

1. `v_ac = p_eff × area × runoff_coeff`, in litres.
2. This is where the rainfall file becomes volume, and the only place where it happens.
3. The coefficient is dimensionless and lies in [0, 1]; outside it the simulation does not start.

**Outputs**

- `v_ac`: volume collected in the day, which goes to PROC-06
- `harvested_liters` in the daily series

**Exception.** A negative area or a coefficient outside [0, 1] raises `ValueError` naming the field, in PROC-11.

### B.6. PROC-06 — Store and overflow

*Water balance*

**Trigger.** Every day, after collection.

**Inputs**

- `v_ac`
- volume left from the previous day
- `lower_tank_vol`

**Rules**

1. **Overflow before consumption**, as in the YAS rule; the day's rain, up to the capacity, already supplies the day's demand, which places the model between strict YAS and YBS.
2. `available = v_lower + v_ac`. If it exceeds the capacity, the surplus overflows and the tank is full.
3. The order matters: withdrawing the demand first would let the tank accept water that would physically have overflowed already, overestimating the yield.

**Outputs**

- `v_spill_today`, summed into `avg_spilled_l_day`, which becomes the overflow criterion in the multi-criteria decision
- `v_in_tank`, the volume available for supply

**Exception.** Zero volume is valid and represents the no-system scenario; a negative one is rejected.

### B.7. PROC-07 — Supply from a single tank

*Water balance*

**Trigger.** Every day, when there is no upper tank.

**Inputs**

- `v_in_tank`
- `pluvial_demand_per_day` from PROC-02

**Rules**

1. `v_c = min(rainwater demand, volume in the tank)`.
2. The remaining volume stays for the next day: `v_lower = v_in_tank − v_c`.

**Outputs**

- `v_c`: rainwater volume consumed in the day

**Exception.** None: the minimum already handles an empty tank and a null demand.

### B.8. PROC-08 — Supply with pumping to an upper tank

*Water balance*

**Trigger.** Every day, when `upper_tank_used` and the upper volume is positive.

**Inputs**

- `v_lower`, `v_upper`
- `upper_tank_vol`
- `pumping_threshold`, the reserve volume that is not consumed

**Rules**

1. Loop until the demand is met or the water runs out.
2. First consumes from the upper tank what lies **above** the pump trigger level.
3. If something is still missing and there is water below, starts the pump: transfers `min(v_lower, free space above)`, counts **one cycle** and records the batch.
4. After pumping, consumes again.
5. The trigger level is capped at the upper tank volume at the start of the process.

**Outputs**

- `v_c`
- `v_rec_today`, summed into `total_pumped_liters`
- `cycles_today`, summed into `total_pump_cycles`
- `max_pump_batch_liters`

**Exception.** A negative upper volume is rejected at validation. The loop has a guaranteed exit: if there is no water below or above, it stops.

### B.9. PROC-09 — Split the supply and top up with potable water

*Water balance*

**Trigger.** Every day, after supply.

**Inputs**

- `v_c`
- `non_pot_in_day`
- `irr_day`
- `pot_in_day`
- `irrigation_potable_backup`

**Rules**

1. **Priority 1**, indoor non-potable use: `c_pluv_in = min(v_c, indoor non-potable)`.
2. **Priority 2**, irrigation: `c_pluv_irr = min(v_c − c_pluv_in, irrigation of the day)`.
3. The potable water consumed is the sum of three parts: the indoor potable, the deficit of the indoor non-potable and — only if the backup supply is on — the irrigation deficit.
4. With the backup supply off, the garden is simply not watered on the dry day, and the mains is not used.

**Outputs**

- `potable_consumed_liters` of the day
- `avg_pluvial_indoor_consumed_l_day` and `avg_pluvial_irrigation_consumed_l_day`, which separate indoor from outdoor use for credits WEc1 and WEc2 of LEED v4 and Options 2 and 4 of WEc2 of LEED v5

**Exception.** None: all parts are minima and maxima with zero.

### B.10. PROC-10 — Classify the day's supply

*Water balance*

**Trigger.** Every day, at the end of supply.

**Inputs**

- `v_c`
- `pluvial_demand_per_day`

**Rules**

1. **Full** when the consumption equals the rainwater demand, with a tolerance of 10⁻⁵ L.
2. **Partial** when something was consumed, but less than the demand.
3. **Null** when nothing was consumed.

**Outputs**

- `pct_days_full_satisfaction`, `pct_days_partial_satisfaction` and `pct_days_null_satisfaction`, which are the system's time reliability

**Exception.** None.

### B.11. PROC-11 — Validate the physical input

*Water balance*

**Trigger.** First line of `run_single_simulation`, before any calculation.

**Inputs**

- lower and upper volume
- area
- runoff coefficient
- first-flush depth
- daily demand
- rainwater fraction

**Rules**

1. Negative volume, negative area, negative first flush and negative demand are refused.
2. Runoff coefficient and rainwater fraction must lie in [0, 1].
3. **Zero volume remains valid**: it is the «no system» reference of the sweep.
4. The message names the field and the value received, instead of silently correcting it.

**Outputs**

- No output: it either passes or raises `ValueError`

**Exception.** It is the handling itself. Before this gate, a volume of −1,000 L returned −166.67% saving, and the number went on to the economic analysis, the LCA and the report.

### B.12. PROC-12 — Aggregate the period and compute the indicators

*Water balance*

**Trigger.** End of the daily loop.

**Inputs**

- loop accumulators
- `n_days`

**Rules**

1. **Saving potential** = rainwater consumed in the period ÷ total demand in the period × 100.
2. The daily means divide the totals by the number of simulated days.
3. Conversions to a year use **365.25** days, not 365, to absorb the leap years of the series.
4. The potential always lies in [0, 100] — an invariant the validation gate exists to guarantee.

**Outputs**

- `SingleTankSimulationResult`, with 21 fields, which is the object **all** downstream modules consume

**Exception.** A null total demand returns zero potential instead of dividing by zero.

### B.13. PROC-13 — Sweep volumes and find the ideal volume

*Water balance*

**Trigger.** Sweep tab: simulate button.

**Inputs**

- `lower_tank_max`
- `lower_tank_step`
- `delta_ideal` (%/m³)

**Rules**

1. The discrete grid rounds the step **up** to a multiple of 250 L, the commercial quantum of tanks, and limits it to 40 positive volumes.
2. The maximum volume entered is always kept as the last point, so that only the last interval can be smaller than the step.
3. Zero enters the grid as the reference alternative.
4. Runs PROC-04 to PROC-12 once per volume.
5. The **ideal volume** is the first whose marginal gain `Δpotential/Δm³` falls below the threshold: from there on, more storage does not pay.

**Outputs**

- `SweepSimulationResult`: one result per volume, the ideal volume, and the record that the step was adjusted
- The list of volumes is the list of multi-criteria **candidates**

**Exception.** A step larger than the maximum returns a one-point grid. The step adjustment is recorded in `step_adjusted`, not silenced.

### B.14. PROC-14 — Compute the rainfall indices

*Rainfall*

**Trigger.** Charts tab and research report.

**Inputs**

- `precip_data`
- dates of the series

**Rules**

1. Nine indices: PRCPTOT, R95p, RX1day, RX5day, SDII, R20mm, CDD, CWD and the Walsh and Lawler seasonality index.
2. The set is **not** pure ETCCDI: seasonality is not in the set, and R10mm, which is, is missing.
3. The 95th percentile is computed over the **whole loaded series**, not over the fixed 1961–1990 base of ETCCDI.
4. RX5day uses `min_periods=1`, so the first windows of the year have 1 to 4 days.

**Outputs**

- Nine annual series, for chart and report

**Exception.** A series shorter than one year returns the indices that can be computed, without stopping.

### B.15. PROC-15 — Size the treatment plant

*Quality and treatment*

**Trigger.** A change in the Water Quality tab, or the start of the economic analysis and the LCA.

**Inputs**

- `water_quality_target_class` (4 use classes)
- `water_quality_disinfection`: chlorine, ultraviolet or ozone
- `water_quality_polishing`, polishing filter
- `annual_pluvial_m3` from PROC-12
- `area`
- chlorine dose, purity, price and CO₂ factor
- `discard` and `first_flush_system_enabled`, for the first-flush diverter

**Rules**

1. The target class defines the mandatory stages; the chosen disinfection defines the equipment and the running cost.
2. The polishing filter is applied **if and only if** ticked; when the class would recommend it and the user declines, this is recorded in `polishing_recommended_but_declined` instead of being imposed.
3. What is bought is the **product** — tablets with 65% active chlorine — not pure chlorine. Charging the mass of active chlorine, rather than that of the product, underestimates the cost by about 35%.
4. **Incremental rule**: the CAPEX of the line deducts the generic treatment allowance already included in «Accessories», and the running cost deducts chlorination, which the cash flow already pays. The rule lives in one place, consumed by **both** economic engines.
5. With `first_flush_system_enabled`, the first-flush diverter, of volume `discard × area`, enters the CAPEX and the running cost of the line.
6. In the LCA, the treatment line **replaces** the chlorination term; it never adds to it.
7. With `etap_enabled = False`, the treatment line enters no calculation: not the CAPEX, not the running cost, not the environmental assessment.

**Outputs**

- `total_etap_capex`, which enters the CAPEX
- `total_etap_annual_opex`, which enters the running cost
- `total_etap_co2e_kg_yr`, which replaces chlorination in the LCA
- `disinfection_stages`, shown in the report

**Exception.** A purity outside (0, 1] is refused by the validator of the chlorination chain.

### B.16. PROC-16 — Compute the pumping energy

*Pump set*

**Trigger.** Economic analysis and LCA, from the same simulation result.

**Inputs**

- `supply_arrangement`: pumping to an upper tank, direct pressurisation or gravity
- `total_pumped_liters` and `total_pump_cycles` from PROC-08
- `pressurizer_pressure_m`, `pressurizer_starts_per_person_day`, `residents_count`
- `pump_power_kw`, `pump_efficiency`, `pump_flow_rate`
- `pump_manometric_head_m`
- `pump_startup_time_h`

**Rules**

1. The arrangement decides what is pumped. **Pumping to an upper tank**: the volume sent to the upper tank. **Direct pressurisation**: all the rainwater consumed, with the working pressure in place of the head and no start-up energy. **Gravity**: nothing. It is the only source of kWh of the economic analysis and the LCA.
2. Specific energy `e = ρgH/(η_pump·η_motor)` per m³ pumped, or `P/(Q·η_motor)` when the flow rate is declared.
3. Nameplate power is shaft power and **already includes** the pump efficiency; that is why `P × hours / η_pump` counts that efficiency twice, and what is missing is to divide by the motor efficiency, from ABNT NBR 17094-2. Four copies of that old formula survived in the program and overestimated consumption by 1.68 times — the worst of them ranked volumes in the multi-criteria decision.
4. Start-up energy is added separately, by the number of cycles.
5. Flow rate and efficiency not entered fall back to typical values **for the chosen power**, not to fixed constants.

**Outputs**

- `annual_kwh`, which becomes cost in the economic analysis and emission in the LCA
- `pump_hours_year`, `annual_cycles`

**Exception.** Gravity arrangement, an arrangement not stated in an old project, or zero power: the energy is zero.

### B.17. PROC-17 — Compute the water and sewage bill

*Economic*

**Trigger.** Twice per projected month: with and without harvesting.

**Inputs**

- monthly volume in litres
- `water_tariffs`: quadruples (minimum, maximum, value, code)
- `sewage_mode` and `sewage_rate`
- fixed and variable taxes
- `num_economias`

**Rules**

1. Consumption is evaluated **at the level of one dwelling unit** and multiplied by the number of units, so as not to distort the progressive blocks in a building with individual metering.
2. Code **1** or **0**: progressive block, charged only on the volume within it.
3. Code **−1**, availability charge: a fixed value that **adds** on top of the metered consumption.
4. Code **−2**, retroactive allowance: up to the allowance volume the fixed value is paid; beyond it, **all** the volume from zero is charged by the blocks.
5. Code **−3**, payment floor: it does not add, it **bounds from below**. With a floor of R$ 40 and a charged consumption of R$ 55, saving up to R$ 15 reduces nothing — and that is exactly what a rainwater harvesting study needs to see.
6. Sewage is a percentage of the **water part**, not of the total bill. In Florianópolis it is 100% of the water, which is half the bill.
7. The six tariff regimes are named and audited in the database of 652 municipalities.

**Outputs**

- Value of the water and sewage bill per month, for the projection of PROC-18

**Exception.** An empty table falls back to the CASAN structure. An incomplete structure is flagged by the validation gate, which separates errors from warnings.

### B.18. PROC-18 — Project the cash flow

*Economic*

**Trigger.** Economic tab, after the technical simulation.

**Inputs**

- CAPEX of the five items plus pump and treatment line
- monthly water and sewage saving from PROC-17
- running costs: pumping, chlorination, treatment line and declared operating costs
- `tma`, `inflation`, `analysis_period_years`
- separate escalations for water, sewage and energy, and the interval between them
- green property-tax discount (IPTU Verde), when enabled

**Rules**

1. Water and sewage are escalated by **separate** indices, not by the aggregate bill.
2. Inflation applies only to running costs; tariff escalations apply only to the bill.
3. The escalation is applied every `tariff_escalation` months, in steps.
4. The tariff flag adjusts the electricity tariff: yellow, red 1, red 2, or the off-peak discount in the white tariff (Brazil Edition).
5. The green property-tax discount enters as an annual saving divided by twelve.
6. The payback is the first month in which the discounted cumulative cash flow crosses zero.

**Outputs**

- `vpl`, `tir_monthly_pct`, `tir_annual_pct`, `payback_months`
- `monthly_cash_flows`, month by month
- `annual_pump_kwh`, `annual_chlorine_kg`, `etap_capex_brl`

**Exception.** A negative monthly saving is truncated at zero before entering the cash flow. An IRR without a real root returns null instead of an invented number.

### B.19. PROC-19 — Assess the life cycle

*LCA*

**Trigger.** Environmental tab, after the technical simulation.

**Inputs**

- `tank_vol_liters`
- `annual_pluvial_m3` from PROC-12
- materials and masses of the two tanks
- lengths per pipe diameter
- `pump_count`
- grid electricity factor
- production route of the potable water
- treatment line result from PROC-15

**Rules**

1. Seven stages: lower cistern, upper tank, piping, pump set, pumping operation, treatment operation and avoided potable water.
2. Zero volume **without** rainwater volume is the no-system scenario, and receives no fixed impact for tank, pipe or pump.
3. The treatment line **replaces** the chlorination term; it does not add to it. Chlorination follows the treatment, not the upper tank.
4. Upper tank only in the pumping arrangement; pump sets in every arrangement with a pump; energy from PROC-16.
5. The avoided water is the water **delivered**, not produced: distribution losses in Brazil range from 33.9% in the Southeast to 46.9% in the North, so producing 1 m³ delivers 0.53 to 0.66 m³. The published factor of 0.236 kg CO₂e/m³ is at the plant outlet; per m³ delivered it becomes 0.336 to 0.461 depending on the region. In the International Edition the user enters the factor for the delivered water.
6. The carbon payback is the embodied carbon divided by the net annual saving; without a positive net saving, it returns 999 years instead of infinity.

**Outputs**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, which is a multi-criteria criterion
- `environmental_payback_years`
- `inventory_items`, the item-by-item inventory

**Exception.** A factor without a primary source receives a screening label, and the label is shown — the gap is declared, not hidden.

### B.20. PROC-20 — Map onto certifications

*ESG and certifications*

**Trigger.** Environmental tab and reports.

**Inputs**

- `potential_potable_savings_pct`
- annual rainwater and potable volumes
- indoor/outdoor split from PROC-09
- CO₂ avoided over the life cycle
- `area`, for the catchment area of WEM14
- EDGE base case, when declared

**Rules**

1. **LEED v4**: WEc1 up to 2 points for outdoor use, WEc2 up to 6 points for indoor use, on the official scale. Without an outdoor demand, WEc1 is zero and says why.
2. **LEED v5 BD+C** (rating system of November 2025): WEc2 up to 8 points, by Option 1 (whole project, 30% to 65%, +1 with an alternative source) or by the sum of Options 2 (fixtures and fittings, 30% to 40%), 4 (outdoor, 50% and 100%) and 6 (on-site reuse, 2 points), new construction only. SSc3 recorded as not assessed; its reuse point does not exceed the cap of 3.
3. **AQUA-HQE Residential** (reference of 22/11/2024, Brazil Edition): items EAU.1.2 (HQE, 20% saving), EAU.1.3 (HQE 3, 40%) and EAU.1.5 (HQE 3, existence of a rainwater system).
4. **Casa Azul + CAIXA** (guide V023, 29/04/2026, Brazil Edition): criterion 3.6 met by the existence of the system; 2, 4 or 5 points depending on the scope of use, only when stated.
5. **EDGE**: **does not score points**. It measures a percentage against a local base case and compares it with 20%, in three independent bars. The advanced level raises the *energy* bar to 40%, not the water one. The program assesses only the water bar, by measure WEM14, and says that the other two are outside its reach.
6. Without a declared base case, EDGE uses the modelled demand and warns that the number is a **floor**.
7. **GRI 303**: avoided withdrawal and circularity rate.

**Outputs**

- `credit_details`: the credit matrix that feeds the on-screen table and the reports
- `esg_summary_text`
- cards for LEED, AQUA, Casa Azul, EDGE and GRI

**Exception.** A null total demand returns zero per cent without dividing by zero.

### B.21. PROC-21 — Rank volumes by multiple criteria

*Multi-criteria*

**Trigger.** Optimiser tab, with the sweep done.

**Inputs**

- one candidate per sweep volume, each with potential, overflow, NPV, discounted payback, IRR, life-cycle CO₂ and potable consumption
- weights of the seven criteria

**Rules**

1. Seven criteria: **maximise** potential, NPV and IRR; **minimise** overflow, payback, CO₂ and potable consumption.
2. Normalisation shifts by `x − min(x)` **before** the vector normalisation of Hwang and Yoon, to admit a negative NPV. It is a deliberate variant, and must be declared as a variant.
3. SMAA-VIKOR draws weights and returns the probabilities of each volume taking each rank.
4. Opricovic's conditions C1 and C2 are not implemented.

**Outputs**

- Ranking of the volumes, distance to the ideal per criterion, compromise volume

**Exception.** A single candidate returns a trivial ranking. A criterion constant across candidates does not contribute to the distance.

### B.22. PROC-22 — Save and reopen the project

*Project file*

**Trigger.** Save and open menu.

**Inputs**

- the whole `NetunoConfig`, with the fields of appendix A
- interface state
- current analysis

**Rules**

1. JSON format, in named sections.
2. Reading uses a default value field by field, so an old file keeps opening.
3. `created_at` and `precip_file` describe the act of saving, not the project: that is why they do not come back.
4. It is the fifth crossing of the program — the one that crosses **time** rather than modules. Thirty of the 87 fields of the time did not survive the round trip, including the whole treatment-line choice, the manometric head, the tank materials, irrigation and the property tax.

**Outputs**

- `.netuno` file
- rebuilt `NetunoConfig`

**Exception.** A section missing from the file falls back to the class defaults. Invalid JSON stops opening with a message.

### B.23. PROC-23 — Issue reports and exports

*Reports*

**Trigger.** Reports tab; Export tab.

**Inputs**

- results of PROC-12, PROC-18, PROC-19, PROC-20 and PROC-21
- project data

**Rules**

1. Three reports: executive, environmental with ESG, and research.
2. Export to CAD and BIM from the sizing.
3. Spreadsheets with the daily series and the sweep.

**Outputs**

- HTML, PDF, DXF, JSON for BIM and XLSX

**Exception.** Conversion to PDF tries the Qt engine and falls back to the alternative generator when it is not available.

### B.24. PROC-24 — Automation for large-scale studies

*Automation*

**Trigger.** The `netuno` command line, described in section 3.6; it comes with the installation as a Python package, not with the Windows installer.

**Inputs**

- project file
- rainfall file

**Rules**

1. Calls the **same** calculation core as the window, without a screen.
2. Only part of the parameters can be reached through it; the others exist only in the interface, and the way is to build the project in the window and vary by automation only what changes between cases.
3. It serves factorial matrices of thousands of cases and uncertainty propagation by sampling, which are the instruments of the studies published by the group.

**Outputs**

- JSON and CSV with the results

**Exception.** A parameter out of range is refused before simulating, with the same validation gate as the interface.

---

## Appendix C — Emission factors

> **Section not yet written.**

---

## Appendix D — Tariff regimes

> **Brazil Edition.** The tariff catalogue is Brazilian and ships only with the Brazil
> Edition. In the International Edition the tariff is entered by the user, in one of
> the same six regimes, and this appendix serves as a description of them.

The database holds **652 municipalities** with tariff structure, sewage
percentage, minimum-charge regime, effective date and source. This list is extracted
from the program's own database, not transcribed.

### D.1. The block codes

Each row of the tariff table is a quadruple `(minimum, maximum, value, code)`.

The six codes and the effect of each on the bill are drawn in section 2.7, and are not repeated here.


### D.2. The six regimes

<!-- tabela: **Table 19** — Distribution of the catalogue municipalities across the six tariff regimes -->
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

### D.3. Distribution by state

The catalogue coverage follows the population, not the territory: the state capitals and the metropolitan regions are almost all registered, and the interior of the North and Centre-West regions concentrates the municipalities still missing (Figure 1).

![The catalogue municipalities, by state](../figuras/fig42_uf.png)

*Figure 1 — The distribution of the 652 catalogued municipalities across the Brazilian states, with colours identifying the macro-region. São Paulo and Minas Gerais alone account for almost a third of the catalogue.*


### D.4. Updating and auditing the database

The tariff database is maintained by the group with an update routine run outside the interface, before each version. The routine has three components.

**Electricity.** The residential tariffs of subgroup B1 are read from the open database of approved distributor tariffs published by the Brazilian Electricity Regulatory Agency (ANEEL), and associated with the distributor of each catalogue municipality.

**Water and sewage.** A register of primary evidence associates each provider with the regulatory agency, the official tariff page and the type of act that publishes them. Providers with a standard portal are read automatically; the others are flagged for manual checking of the decree or resolution, and the resulting structure goes through the same regime validation described in this appendix.

**Change detection.** Each monitored official page is recorded with the SHA-256 signature of its content and the `ETag` and `Last-Modified` headers. A new check compares the signatures and points out the pages changed since the last collection, which are the candidates for a tariff revision.

The routine can simulate the update without writing the database, run only the change detection, restrict itself to one state or one municipality, and separate electricity from sanitation. Each run writes an audit report in Markdown and an HTML panel with the status of each municipality.

### D.5. Confidence grade

Each record carries the confidence grade of the collection:

<!-- tabela: **Table 20** — Confidence grade of the tariff records in the catalogue -->
| Grade | Records |
| :--- | ---: |
| A — high | 580 |
| B — good | 63 |
| C — structure to be checked | 5 |
| D — incomplete structure | 4 |

> **Always check the effective date** of your municipality's record against the
> utility's resolution. Tariffs are adjusted every year, and section 3.3
> teaches the test that identifies a wrong structure.

---

## Appendix E — Climate database

> **Section not yet written.**

---

## Appendix F — Files, folders and formats

> **Section not yet written.**

---

## Appendix G — Glossary

> **Section not yet written.**

---

## Appendix H — References

> **Section not yet written.**

---

## Appendix I — One-page summaries

> **Section not yet written.**

---

## Appendix J — Example files

> **Section not yet written.**
