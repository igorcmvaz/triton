# The program's processes

There are **24 processes**, from the rainfall file to the report. Each
one declares what triggers it, what it receives, the rules with their branches, what
it produces and what happens when it fails.

It is the most technical appendix of the manual, and it serves two people: whoever
reviews a study made with the program and needs to know exactly which calculation was
done, and whoever found a strange result and wants to know where the number went through.

The names in `code` are the project file fields, listed in appendix {{n:A}}.

## PROC-01 — Load the precipitation series

*Rainfall*

**Trigger.** Project tab: open a rainfall file (CSV), or load a series stored in a project.

**Inputs**

- Daily CSV file, in millimetres per day (the series that ships in `data/rainfall`, or your own)
- `climate_start_date` and `climate_end_date`, which trim the series
- `start_date`, the date of the first day of the series

**Rules**

1. The series becomes a `numpy` vector of millimetres per day; the vector index is the day, and the date only serves to know the weekday and the month.
2. An incomplete year is dropped on reading, so as not to bias annual totals.
3. The series is always a file of the user: the edition ships three example series in `data/rainfall` (ERA5 reanalysis) and no regional rainfall database.

**Outputs**

- `precip_data`: vector of mm/day, which is the input of **two** distinct processes — PROC-04 (first flush and collection) and PROC-03 (irrigation suppression)

**Exception.** An unreadable file or one without a rainfall column stops loading with a message; the simulation does not run on an empty series.

## PROC-02 — Build the daily demand

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

## PROC-03 — Suppress irrigation on rainy days

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

## PROC-04 — Divert the first flush

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

## PROC-05 — Convert depth into collected volume

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

## PROC-06 — Store and overflow

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

## PROC-07 — Supply from a single tank

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

## PROC-08 — Supply with pumping to an upper tank

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

## PROC-09 — Split the supply and top up with potable water

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

## PROC-10 — Classify the day's supply

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

## PROC-11 — Validate the physical input

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

## PROC-12 — Aggregate the period and compute the indicators

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

## PROC-13 — Sweep volumes and find the ideal volume

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

## PROC-14 — Compute the rainfall indices

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

## PROC-15 — Size the treatment plant

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

## PROC-16 — Compute the pumping energy

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
3. Nameplate power is shaft power and **already includes** the pump efficiency; that is why `P × hours / η_pump` counts that efficiency twice, and what is missing is to divide by the motor efficiency, entered by the user or taken from the typical value for the rated power. Four copies of that old formula survived in the program and overestimated consumption by 1.68 times — the worst of them ranked volumes in the multi-criteria decision.
4. Start-up energy is added separately, by the number of cycles.
5. Flow rate and efficiency not entered fall back to typical values **for the chosen power**, not to fixed constants.

**Outputs**

- `annual_kwh`, which becomes cost in the economic analysis and emission in the LCA
- `pump_hours_year`, `annual_cycles`

**Exception.** Gravity arrangement, an arrangement not stated in an old project, or zero power: the energy is zero.

## PROC-17 — Compute the water and sewage bill

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
5. Code **−3**, payment floor: it does not add, it **bounds from below**. With a floor of 40 currency units and a charged consumption of 55, saving up to 15 reduces nothing — and that is exactly what a rainwater harvesting study needs to see.
6. Sewage is a percentage of the **water part**, not of the total bill: where the sewer charge is 100% of the water charge, it is half the bill.
7. The six tariff regimes are described in appendix D; the user enters the table of the project.

**Outputs**

- Value of the water and sewage bill per month, for the projection of PROC-18

**Exception.** An empty table gives a zero bill: the program does not assume a tariff. An incomplete structure is flagged by the validation gate, which separates errors from warnings.

## PROC-18 — Project the cash flow

*Economic*

**Trigger.** Economic tab, after the technical simulation.

**Inputs**

- CAPEX of the five items plus pump and treatment line
- monthly water and sewage saving from PROC-17
- running costs: pumping, chlorination, treatment line and declared operating costs
- `tma`, `inflation`, `analysis_period_years`
- separate escalations for water, sewage and energy, and the interval between them

**Rules**

1. Water and sewage are escalated by **separate** indices, not by the aggregate bill.
2. Inflation applies only to running costs; tariff escalations apply only to the bill.
3. The escalation is applied every `tariff_escalation` months, in steps.
4. The payback is the first month in which the discounted cumulative cash flow crosses zero.

**Outputs**

- `vpl`, `tir_monthly_pct`, `tir_annual_pct`, `payback_months`
- `monthly_cash_flows`, month by month
- `annual_pump_kwh`, `annual_chlorine_kg`, `etap_capex_brl`

**Exception.** A negative monthly saving is truncated at zero before entering the cash flow. An IRR without a real root returns null instead of an invented number.

## PROC-19 — Assess the life cycle

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
5. The avoided water is the water **delivered**, not produced: distribution losses mean that producing 1 m³ delivers less than 1 m³, and a factor given at the plant outlet must be converted to the volume delivered. The user enters the emission factor of the water delivered to the building and the factor of the local grid; the edition has no default for either.
6. The carbon payback is the embodied carbon divided by the net annual saving; without a positive net saving, it returns 999 years instead of infinity.

**Outputs**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, which is a multi-criteria criterion
- `environmental_payback_years`
- `inventory_items`, the item-by-item inventory

**Exception.** A factor without a primary source receives a screening label, and the label is shown — the gap is declared, not hidden.

## PROC-20 — Map onto certifications

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
3. **EDGE**: **does not score points**. It measures a percentage against a local base case and compares it with 20%, in three independent bars. The advanced level raises the *energy* bar to 40%, not the water one. The program assesses only the water bar, by measure WEM14, and says that the other two are outside its reach.
4. Without a declared base case, EDGE uses the modelled demand and warns that the number is a **floor**.
5. **GRI 303**: avoided withdrawal and circularity rate.

**Outputs**

- `credit_details`: the credit matrix that feeds the on-screen table and the reports
- `esg_summary_text`
- cards for LEED, EDGE and GRI

**Exception.** A null total demand returns zero per cent without dividing by zero.

## PROC-21 — Rank volumes by multiple criteria

*Multi-criteria*

**Trigger.** Optimiser tab, with the sweep done.

**Inputs**

- one candidate per sweep volume, each with volumetric reliability, storage efficiency, net financial savings, LCOW, discounted payback, life-cycle CO₂, dry mass and annual overflow
- four dimension weights (technical, economic, environmental, structural) and eight criterion shares, eight criterion weights, or `critic` for objective weights
- tolerance of the choice band, 5% of the score range by default

**Rules**

1. Eight criteria in four dimensions: **maximise** volumetric reliability, storage efficiency and net financial savings; **minimise** LCOW, payback, CO₂, dry mass and overflow.
2. Each dimension weight is shared among its criteria by the criterion shares (equal by default). Three weights, from version 0.1.0, give the structural dimension their mean; seven values are refused.
3. With `critic`, the weights are computed from the results by the CRITIC method: the contrast of each criterion across the volumes times its independence from the others.
4. A volume that does not pay back receives the worst payback observed plus 10% (at least one year more and at least 20 years); the volume with no cistern receives the worst LCOW plus 10%.
5. Normalisation shifts by `x − min(x)` **before** the vector normalisation of Hwang and Yoon, to admit a negative NPV. It is a deliberate variant, and must be declared as a variant.
6. SMAA-VIKOR draws eight weights, with 25% expected on each dimension, and returns the probabilities of each volume taking each rank.
7. The choice band gathers the volumes whose score lies within the tolerance of the best, on a scale from the worst (0) to the best (1) of the volumes evaluated.
8. Opricovic's conditions C1 and C2 are not implemented.

**Outputs**

- Ranking of the volumes, distance to the ideal per criterion, choice band and highest score

**Exception.** A single candidate returns a trivial ranking. A criterion constant across candidates does not contribute to the distance.

## PROC-22 — Save and reopen the project

*Project file*

**Trigger.** Save and open menu.

**Inputs**

- the whole `TritonConfig`, with the fields of appendix {{n:A}}
- interface state
- current analysis

**Rules**

1. JSON format, in named sections.
2. Reading uses a default value field by field, so an old file keeps opening.
3. `created_at` and `precip_file` describe the act of saving, not the project: that is why they do not come back.
4. It is the fifth crossing of the program — the one that crosses **time** rather than modules. Thirty of the 87 fields of the time did not survive the round trip, including the whole treatment-line choice, the manometric head, the tank materials and irrigation.

**Outputs**

- `.triton` file
- rebuilt `TritonConfig`

**Exception.** A section missing from the file falls back to the class defaults. Invalid JSON stops opening with a message.

## PROC-23 — Issue reports and exports

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

## PROC-24 — Automation for large-scale studies

*Automation*

**Trigger.** The `triton` command line, described in section {{n:19}}; it comes with the installation as a Python package, not with the Windows installer.

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

