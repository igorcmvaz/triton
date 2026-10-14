# The project parameters

There are **122 parameters**. This is the complete list of what a project
stores, with the exact name of each field inside the `.triton` file.

The list was not transcribed by hand: it is extracted from the program itself for
each version, and therefore cannot diverge from it.

The column **where it is entered** says on which screen the field appears; the
column **who consumes it** says which calculation uses it. A field with neither is a
field stored in the file and never read, and is listed in section {{n:36}}.

Defaults in currency are the Brazil Edition ones, in reais (R$); the International
Edition starts the costs and tariffs at zero, for the user to enter in the currency
of the project.

## Identification

3 parameters.

<!-- tabela: Project parameters: identification -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | New Triton project | — | Export, Main window, Reports | Automation, CAD and BIM, Reports, Spreadsheets |
| `project_id` | — | — | Main window, Reports | Automation |
| `created_at` | — | — | Main window | — |

## Rainfall

9 parameters.

<!-- tabela: Project parameters: rainfall -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Main window, Project | Automation, Scenarios, Spreadsheets |
| `climate_source_mode` | national_db | — | Main window, Project | — |
| `climate_city_uf` | SC | — | Main window, Project, Reports | — |
| `climate_city_name` | Florianópolis | — | Main window, Project, Reports | — |
| `climate_model` | INM-CM4 | — | Main window, Project, Reports | — |
| `climate_scenario` | HIST | — | Main window, Project, Reports | — |
| `climate_start_date` | 1980-01-01 | — | Main window, Project, Reports | — |
| `climate_end_date` | 2013-12-31 | — | Main window, Project, Reports | — |
| `start_date` | 1980-01-01 | — | Export, Main window, Project, Tariffs and costs | Automation, Climate, Spreadsheets |

Notes from the code:

- `climate_source_mode`: "national_db" (national database, Brazil Edition) or "custom_file" (own file)

## Catchment

7 parameters.

<!-- tabela: Project parameters: catchment -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | — | mm | Charts, Documentation, Environmental, Main window, Project, Quality, Reports | Automation, CAD and BIM, LCA, Reports, Scenarios, Spreadsheets, Treatment line |
| `discard_mode` | 1 | code | Main window, Project, Sweep | Automation, Daily balance, Scenarios |
| `discard_days_interval` | 7 | days | Main window, Project, Sweep | Automation, Daily balance, Scenarios |
| `area` | 100 | m² | Building, Charts, Documentation, Environmental, Main window, Quality, Reports, Sweep, Tariffs and costs | Automation, CAD and BIM, Daily balance, LCA, Reports, Scenarios, Spreadsheets, Treatment line |
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

## Building

2 parameters.

<!-- tabela: Project parameters: building -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | units | Building, Environmental | Automation, Economic |
| `building_template_id` | res_medio | — | Building | Automation, Tariffs |

Notes from the code:

- `num_economias`: Number of dwelling units / apartments with individual metering

## Demand

17 parameters.

<!-- tabela: Project parameters: demand -->
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

## Irrigation

4 parameters.

<!-- tabela: Project parameters: irrigation -->
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

## Water quality

9 parameters.

<!-- tabela: Project parameters: water quality -->
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

## Tanks

12 parameters.

<!-- tabela: Project parameters: tanks -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | L | Economic, Environmental, Export, Main window, Optimiser, Pump wizard, Reports, Sweep, Tariffs and costs, Upper tank | Automation, CAD and BIM, Daily balance, Multi-criteria, Prices, Scenarios, Spreadsheets |
| `upper_tank_used` | 1 | code | Economic, Environmental, Main window, Optimiser, Reports, Sweep, Tariffs and costs | Automation, Daily balance, LCA, Prices, Pump set, Scenarios, Spreadsheets |
| `lower_tank_max` | 10000 | L | Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `lower_tank_step` | 250 | L | Main window, Sweep | Automation, Daily balance, Scenarios, Spreadsheets |
| `lower_tank_mode` | 1 | code | Main window, Sweep | Automation |
| `lower_tank_fixed` | 2000 | L | Main window, Sweep, Tariffs and costs | Automation |
| `delta_ideal` | 5 | %/m³ | Main window, Optimiser, Sweep | Automation, Scenarios |
| `econ_lower_tank_vol` | 2000 | L | Economic, Environmental, Sweep, Tariffs and costs | Automation |
| `lower_tank_material` | PEAD | — | Economic, Optimiser, Tariffs and costs | Automation, LCA, Prices |
| `upper_tank_material` | PEAD | — | Economic, Optimiser, Tariffs and costs | Automation, LCA, Prices |
| `cost_lower_tank` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic, Prices |
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

## Pump set

18 parameters.

<!-- tabela: Project parameters: pump set -->
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

## Piping

1 parameter.

<!-- tabela: Project parameters: piping -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Economic, Tariffs and costs | Automation, LCA |

## Investment

3 parameters.

<!-- tabela: Project parameters: investment -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |
| `cost_piping` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic |
| `cost_accessories` | 0 | R$ | Economic, Sweep, Tariffs and costs | Automation, Economic, Treatment line |

## Operation

1 parameter.

<!-- tabela: Project parameters: operation -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |

## Tariffs

18 parameters.

<!-- tabela: Project parameters: tariffs -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | no | — | Project | — |
| `water_tariffs` | — | — | Project, Sweep, Tariffs, Tariffs and costs | Economic |
| `tariff_city_uf` | SC | — | Main window, Project, Reports, Tariffs, Tariffs and costs | — |
| `tariff_city_name` | Florianópolis | — | Main window, Project, Reports, Tariffs, Tariffs and costs | — |
| `tariff_vigencia` | — | — | Project, Tariffs and costs | — |
| `tariff_category` | residencial | — | Economic, Tariffs, Tariffs and costs | Tariffs |
| `sewage_rate` | 100 | % of water | Project, Tariffs, Tariffs and costs | Automation, Economic, Tariffs |
| `sewage_mode` | 1 | code | Economic, Optimiser, Project, Tariffs, Tariffs and costs | Automation, Economic, Tariffs |
| `sewage_tariffs` | — | — | — | Economic, Tariffs |
| `sewage_volume_factor` | 1 | — | — | Automation, Economic, Tariffs |
| `water_tax_fixed` | 0 | R$/month | Tariffs and costs | Automation, Economic |
| `water_tax_var` | 0 | % | Tariffs and costs | Automation, Economic |
| `tariff_escalation` | 12 | months | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `water_tariff_escalation` | 5 | % per period | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `sewage_tariff_escalation` | 5 | % per period | Economic, Optimiser, Tariffs and costs | Automation, Economic |
| `elec_tariff_escalation` | 5 | % per period | Economic, Optimiser, Sweep | Automation, Economic |
| `tariff_flag` | verde | — | Economic | Automation, Economic |
| `elec_tariff` | 0.6957 | R$/kWh | Charts, Economic, Optimiser, Project, Sweep, Tariffs and costs | Automation, Economic |

Notes from the code:

- `tariff_category`: category of the tariff table applied; "personalizada" (custom) when typed in
- `sewage_mode`: 0 = fixed amount, 1 = percentage of the water part, 2 = amount per m³ consumed, 3 = tiers
- `water_tax_fixed`: currency
- `water_tax_var`: %
- `tariff_escalation`: months; length of the escalation period
- `water_tariff_escalation`: % per escalation period; with 12 months, % per year
- `sewage_tariff_escalation`: % per escalation period; with 12 months, % per year
- `elec_tariff_escalation`: % per escalation period; with 12 months, % per year
- `tariff_flag`: "verde" (green), "amarela" (yellow), "vermelha_1" (red 1), "vermelha_2" (red 2), "branca" (white); Brazil Edition
- `elec_tariff`: per kWh (Brazil Edition default: residential B1 tariff, CELESC, Florianópolis)

## Energy

4 parameters.

<!-- tabela: Project parameters: energy -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | SC | — | Main window, Project, Tariffs and costs | — |
| `elec_city_name` | Florianópolis | — | Main window, Project, Tariffs and costs | — |
| `elec_tax_fixed` | 0 | R$/month | Tariffs and costs | Automation, Economic |
| `elec_tax_var` | 0 | % | Tariffs and costs | Automation, Economic |

Notes from the code:

- `elec_tax_fixed`: currency
- `elec_tax_var`: %

## Incentives

3 parameters.

<!-- tabela: Project parameters: incentives -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `iptu_green_enabled` | no | — | Economic, Optimiser | Automation, Economic |
| `iptu_annual_value` | 4000 | R$/year | Economic, Optimiser | Automation, Economic |
| `iptu_discount_pct` | 5 | % | Economic, Optimiser | Automation, Economic |

Notes from the code:

- `iptu_annual_value`: Annual municipal property tax (IPTU) of the building, per year; Brazil Edition
- `iptu_discount_pct`: Municipal green property-tax discount (IPTU Verde, %); Brazil Edition

## Financial

4 parameters.

<!-- tabela: Project parameters: financial -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0.2 | % per month | Documentation, Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `analysis_period_years` | 20 | years | Economic, Optimiser, Reports, Sweep, Tariffs and costs | Automation, Economic, LCA, Reports |
| `tma` | 2 | % per month | Economic, Optimiser, Sweep, Tariffs and costs | Automation, Economic |
| `install_month` | 0 | month | — | — |

Notes from the code:

- `inflation`: % per month; inflation of O&M costs
- `analysis_period_years`: years
- `tma`: % per month; minimum attractive rate of return

## Certifications

1 parameter.

<!-- tabela: Project parameters: certifications -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | L/person·day | Environmental | — |

## Other

6 parameters.

<!-- tabela: Project parameters: other -->
| Parameter | Default | Unit | Where it is entered | Who consumes it |
| :--- | ---: | :--- | :--- | :--- |
| `phi_operation_rule` | — | — | Main window, Sweep | Automation, Daily balance, Spreadsheets |
| `data_base_estudo` | — | — | Tariffs and costs | — |
| `precos_de_catalogo` | yes | — | Economic, Optimiser, Pump wizard, Quality, Sweep, Tariffs and costs | Automation, Prices, Treatment line |
| `bim_layout` | — | — | Export, Main window | — |
| `capex_do_arranjo` | no | — | Main window, Sweep, Tariffs and costs | Treatment line |
| `mao_de_obra_automatica` | no | — | Main window, Sweep, Tariffs and costs | — |

