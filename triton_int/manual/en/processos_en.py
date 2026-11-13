# -*- coding: utf-8 -*-
"""The Triton process matrix, in English: the source of appendix B of the English manual.

It is the translation of `manual/processos.py`, item by item, with the same identifiers and
the same functions. `tests/unit/test_manual_en.py` checks that the two lists name the same
processes, in the same order, citing the same functions: a process added or removed in the
Portuguese file without its translation fails the suite.
"""

# (id, name, family, trigger, [inputs], [rules], [(module, function)], [outputs], exception)
PROCESSOS = [
(
 "PROC-01", "Load the precipitation series", "chuva",
 "Project tab: open a rainfall file (CSV), or load a series stored in a project.",
 ["Daily CSV file, in millimetres per day (the series that ships in <code>data/rainfall</code>, or your own)",
  "<code>climate_start_date</code> and <code>climate_end_date</code>, which trim the series",
  "<code>start_date</code>, the date of the first day of the series"],
 ["The series becomes a <code>numpy</code> vector of millimetres per day; the vector index "
  "is the day, and the date only serves to know the weekday and the month.",
  "An incomplete year is dropped on reading, so as not to bias annual totals.",
  "The series is always a file of the user: the edition ships three example series in "
  "<code>data/rainfall</code> (ERA5 reanalysis) and no regional rainfall database."],
 [("climate_database.py", "load_national_climate_series"),
  ("climate_database.py", "get_climate_file_path"),
  ("parser.py", "load_precipitation")],
 ["<code>precip_data</code>: vector of mm/day, which is the input of <b>two</b> distinct "
  "processes — PROC-04 (first flush and collection) and PROC-03 (irrigation suppression)"],
 "An unreadable file or one without a rainfall column stops loading with a message; "
 "the simulation does not run on an empty series.",
),
(
 "PROC-02", "Build the daily demand", "demanda",
 "Start of the simulation, once per run.",
 ["<code>demand_mode</code>: constant, weekly, monthly or daily",
  "<code>demand_value</code> (L/day per person), <code>residents_count</code>",
  "<code>rainwater_share</code> or <code>non_potable_indoor_share</code>",
  "vectors <code>weekly_*</code>, <code>monthly_*</code>, <code>daily_*</code> when the mode uses them"],
 ["Base demand of the day = <code>demand_value × residents_count</code>, with the multiplier "
  "of the weekday, month or day, depending on the mode.",
  "The non-potable fraction splits the demand in two: indoor potable and indoor non-potable.",
  "When the mode is weekly, monthly or daily, the fraction comes from the period vector itself; "
  "otherwise <code>non_potable_indoor_share</code> applies, and only then <code>rainwater_share</code>.",
  "A null or zero value at any position of the vector falls back to the constant value."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>tot_arr</code>: total demand of the day",
  "<code>pot_in_arr</code>: indoor potable, which rain never supplies",
  "<code>non_pot_in_arr</code>: indoor non-potable, rain priority 1",
  "<code>pluv_arr</code> = indoor non-potable + active irrigation"],
 "An unreadable start date falls back to 01/01/1980 instead of stopping, because it only "
 "affects the weekday.",
),
(
 "PROC-03", "Suppress irrigation on rainy days", "demanda",
 "Demand composition, one test per day of the series.",
 ["<code>irrigation_liters_per_day</code>",
  "<code>irrigation_rain_threshold_mm</code> (default 2 mm/day)",
  "<code>precip_data</code>, the <b>same</b> vector that feeds the collection"],
 ["If the day's rain ≥ threshold, the day's irrigation is <b>zero</b> and the day is counted "
  "as suppressed.",
  "Otherwise, the day's irrigation is the nominal volume.",
  "It is the second reading of the rainfall file, independent of the first: a day can "
  "suppress irrigation and still yield collection."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>irr_arr</code>: irrigation of the day",
  "<code>irr_suppressed_mask</code>: suppressed days, which become "
  "<code>total_irrigation_days_suppressed</code> in the result"],
 "Without an irrigation volume, the vector is zero and the mask is false on every day.",
),
(
 "PROC-04", "Divert the first flush", "balanco",
 "Every day with rain, inside the daily loop.",
 ["<code>precip_mm</code> of the day", "<code>discard_mm</code>",
  "<code>discard_mode</code> (1, 2 or 3)", "<code>discard_days_interval</code>"],
 ["<b>Mode 1</b>: diverts on every rain event.",
  "<b>Mode 2</b>: diverts only on the first event after a dry spell, defined as a "
  "previous day with less than 1 mm.",
  "<b>Mode 3</b>: diverts when <code>discard_days_interval</code> days have passed "
  "since the last diversion.",
  "When the diversion applies: <code>p_eff = p − discard_mm</code> if <code>p > discard_mm</code>, "
  "otherwise <b>zero</b>: all the day's rain goes to the diverter.",
  "When it does not apply: <code>p_eff = p</code>, the whole rain is usable."],
 [("simulation.py", "run_single_simulation")],
 ["<code>p_eff</code>: effective depth of the day, in mm, which goes <b>only</b> to PROC-05",
  "<code>eff_precip_mm</code> in the detailed daily series, when it is kept"],
 "A negative first-flush depth is rejected at the validation gate, before the loop.",
),
(
 "PROC-05", "Convert depth into collected volume", "balanco",
 "Every day, after the first flush.",
 ["<code>p_eff</code> from PROC-04", "<code>area</code> (m²)", "<code>runoff_coeff</code>"],
 ["<code>v_ac = p_eff × area × runoff_coeff</code>, in litres.",
  "This is where the rainfall file becomes volume, and the only place where it happens.",
  "The coefficient is dimensionless and lies in [0, 1]; outside it the simulation does not start."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_ac</code>: volume collected in the day, which goes to PROC-06",
  "<code>harvested_liters</code> in the daily series"],
 "A negative area or a coefficient outside [0, 1] raises <code>ValueError</code> naming "
 "the field, in PROC-11.",
),
(
 "PROC-06", "Store and overflow", "balanco",
 "Every day, after collection.",
 ["<code>v_ac</code>", "volume left from the previous day", "<code>lower_tank_vol</code>"],
 ["<b>Overflow before consumption</b>, as in the YAS rule; the day's rain, up to the "
  "capacity, already supplies the day's demand, which places the model between strict YAS and YBS.",
  "<code>available = v_lower + v_ac</code>. If it exceeds the capacity, the surplus overflows "
  "and the tank is full.",
  "The order matters: withdrawing the demand first would let the tank accept water that "
  "would physically have overflowed already, overestimating the yield."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_spill_today</code>, summed into <code>avg_spilled_l_day</code>, which becomes "
  "the overflow criterion in the multi-criteria decision",
  "<code>v_in_tank</code>, the volume available for supply"],
 "Zero volume is valid and represents the no-system scenario; a negative one is rejected.",
),
(
 "PROC-07", "Supply from a single tank", "balanco",
 "Every day, when there is no upper tank.",
 ["<code>v_in_tank</code>", "<code>pluvial_demand_per_day</code> from PROC-02"],
 ["<code>v_c = min(rainwater demand, volume in the tank)</code>.",
  "The remaining volume stays for the next day: <code>v_lower = v_in_tank − v_c</code>."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>: rainwater volume consumed in the day"],
 "None: the minimum already handles an empty tank and a null demand.",
),
(
 "PROC-08", "Supply with pumping to an upper tank", "balanco",
 "Every day, when <code>upper_tank_used</code> and the upper volume is positive.",
 ["<code>v_lower</code>, <code>v_upper</code>", "<code>upper_tank_vol</code>",
  "<code>pumping_threshold</code>, the reserve volume that is not consumed"],
 ["Loop until the demand is met or the water runs out.",
  "First consumes from the upper tank what lies <b>above</b> the pump trigger level.",
  "If something is still missing and there is water below, starts the pump: transfers "
  "<code>min(v_lower, free space above)</code>, counts <b>one cycle</b> and records the batch.",
  "After pumping, consumes again.",
  "The trigger level is capped at the upper tank volume at the start of the process."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>", "<code>v_rec_today</code>, summed into <code>total_pumped_liters</code>",
  "<code>cycles_today</code>, summed into <code>total_pump_cycles</code>",
  "<code>max_pump_batch_liters</code>"],
 "A negative upper volume is rejected at validation. The loop has a guaranteed exit: "
 "if there is no water below or above, it stops.",
),
(
 "PROC-09", "Split the supply and top up with potable water", "balanco",
 "Every day, after supply.",
 ["<code>v_c</code>", "<code>non_pot_in_day</code>", "<code>irr_day</code>",
  "<code>pot_in_day</code>", "<code>irrigation_potable_backup</code>"],
 ["<b>Priority 1</b>, indoor non-potable use: <code>c_pluv_in = min(v_c, indoor non-potable)</code>.",
  "<b>Priority 2</b>, irrigation: <code>c_pluv_irr = min(v_c − c_pluv_in, irrigation of the day)</code>.",
  "The potable water consumed is the sum of three parts: the indoor potable, the deficit of the "
  "indoor non-potable and — only if the backup supply is on — the irrigation deficit.",
  "With the backup supply off, the garden is simply not watered on the dry day, "
  "and the mains is not used."],
 [("simulation.py", "run_single_simulation")],
 ["<code>potable_consumed_liters</code> of the day",
  "<code>avg_pluvial_indoor_consumed_l_day</code> and "
  "<code>avg_pluvial_irrigation_consumed_l_day</code>, which separate indoor from outdoor use "
  "for credits WEc1 and WEc2 of LEED v4 and Options 2 and 4 of WEc2 of LEED v5"],
 "None: all parts are minima and maxima with zero.",
),
(
 "PROC-10", "Classify the day's supply", "balanco",
 "Every day, at the end of supply.",
 ["<code>v_c</code>", "<code>pluvial_demand_per_day</code>"],
 ["<b>Full</b> when the consumption equals the rainwater demand, with a tolerance of 10⁻⁵ L.",
  "<b>Partial</b> when something was consumed, but less than the demand.",
  "<b>Null</b> when nothing was consumed."],
 [("simulation.py", "run_single_simulation")],
 ["<code>pct_days_full_satisfaction</code>, <code>pct_days_partial_satisfaction</code> "
  "and <code>pct_days_null_satisfaction</code>, which are the system's time reliability"],
 "None.",
),
(
 "PROC-11", "Validate the physical input", "balanco",
 "First line of <code>run_single_simulation</code>, before any calculation.",
 ["lower and upper volume", "area", "runoff coefficient",
  "first-flush depth", "daily demand", "rainwater fraction"],
 ["Negative volume, negative area, negative first flush and negative demand are refused.",
  "Runoff coefficient and rainwater fraction must lie in [0, 1].",
  "<b>Zero volume remains valid</b>: it is the «no system» reference of the sweep.",
  "The message names the field and the value received, instead of silently correcting it."],
 [("simulation.py", "validar_parametros_fisicos")],
 ["No output: it either passes or raises <code>ValueError</code>"],
 "It is the handling itself. Before this gate, a volume of −1,000 L returned −166.67% "
 "saving, and the number went on to the economic analysis, the LCA and the report.",
),
(
 "PROC-12", "Aggregate the period and compute the indicators", "balanco",
 "End of the daily loop.",
 ["loop accumulators", "<code>n_days</code>"],
 ["<b>Saving potential</b> = rainwater consumed in the period ÷ total demand in the period × 100.",
  "The daily means divide the totals by the number of simulated days.",
  "Conversions to a year use <b>365.25</b> days, not 365, to absorb the leap years "
  "of the series.",
  "The potential always lies in [0, 100] — an invariant the validation gate exists to guarantee."],
 [("simulation.py", "run_single_simulation")],
 ["<code>SingleTankSimulationResult</code>, with 21 fields, which is the object <b>all</b> "
  "downstream modules consume"],
 "A null total demand returns zero potential instead of dividing by zero.",
),
(
 "PROC-13", "Sweep volumes and find the ideal volume", "balanco",
 "Sweep tab: simulate button.",
 ["<code>lower_tank_max</code>", "<code>lower_tank_step</code>",
  "<code>delta_ideal</code> (%/m³)"],
 ["The discrete grid rounds the step <b>up</b> to a multiple of 250 L, the commercial "
  "quantum of tanks, and limits it to 40 positive volumes.",
  "The maximum volume entered is always kept as the last point, so that only the "
  "last interval can be smaller than the step.",
  "Zero enters the grid as the reference alternative.",
  "Runs PROC-04 to PROC-12 once per volume.",
  "The <b>ideal volume</b> is the first whose marginal gain <code>Δpotential/Δm³</code> falls "
  "below the threshold: from there on, more storage does not pay."],
 [("simulation.py", "build_sweep_volume_grid"), ("simulation.py", "run_sweep_simulation")],
 ["<code>SweepSimulationResult</code>: one result per volume, the ideal volume, and the "
  "record that the step was adjusted",
  "The list of volumes is the list of multi-criteria <b>candidates</b>"],
 "A step larger than the maximum returns a one-point grid. The step adjustment is recorded "
 "in <code>step_adjusted</code>, not silenced.",
),
(
 "PROC-14", "Compute the rainfall indices", "chuva",
 "Charts tab and research report.",
 ["<code>precip_data</code>", "dates of the series"],
 ["Nine indices: PRCPTOT, R95p, RX1day, RX5day, SDII, R20mm, CDD, CWD and the "
  "Walsh and Lawler seasonality index.",
  "The set is <b>not</b> pure ETCCDI: seasonality is not in the set, and R10mm, which is, "
  "is missing.",
  "The 95th percentile is computed over the <b>whole loaded series</b>, not over the fixed "
  "1961–1990 base of ETCCDI.",
  "RX5day uses <code>min_periods=1</code>, so the first windows of the year have "
  "1 to 4 days."],
 [("calculator.py", "IndicesCalculator"), ("calculator.py", "compute_seasonality_index"),
  ("calculator.py", "find_max_consecutive_run_length")],
 ["Nine annual series, for chart and report"],
 "A series shorter than one year returns the indices that can be computed, without stopping.",
),
(
 "PROC-15", "Size the treatment plant", "etap",
 "A change in the Water Quality tab, or the start of the economic analysis and the LCA.",
 ["<code>water_quality_target_class</code> (4 use classes)",
  "<code>water_quality_disinfection</code>: chlorine, ultraviolet or ozone",
  "<code>water_quality_polishing</code>, polishing filter",
  "<code>annual_pluvial_m3</code> from PROC-12", "<code>area</code>",
  "chlorine dose, purity, price and CO₂ factor",
  "<code>discard</code> and <code>first_flush_system_enabled</code>, for the first-flush diverter"],
 ["The target class defines the mandatory stages; the chosen disinfection defines the "
  "equipment and the running cost.",
  "The polishing filter is applied <b>if and only if</b> ticked; when the class would "
  "recommend it and the user declines, this is recorded in "
  "<code>polishing_recommended_but_declined</code> instead of being imposed.",
  "What is bought is the <b>product</b> — tablets with 65% active chlorine — not pure chlorine. "
  "Charging the mass of active chlorine, rather than that of the product, underestimates the cost by about 35%.",
  "<b>Incremental rule</b>: the CAPEX of the line deducts the generic treatment allowance already "
  "included in «Accessories», and the running cost deducts chlorination, which the cash flow already pays. "
  "The rule lives in one place, consumed by <b>both</b> economic engines.",
  "With <code>first_flush_system_enabled</code>, the first-flush diverter, of volume "
  "<code>discard × area</code>, enters the CAPEX and the running cost of the line.",
  "In the LCA, the treatment line <b>replaces</b> the chlorination term; it never adds to it.",
  "With <code>etap_enabled = False</code>, the treatment line enters no calculation: "
  "not the CAPEX, not the running cost, not the environmental assessment."],
 [("water_quality.py", "size_etap"), ("etap_integration.py", "dimensionar_etap_do_projeto"),
  ("etap_integration.py", "capex_incremental_da_etap"),
  ("etap_integration.py", "opex_anual_incremental_da_etap"),
  ("chlorination.py", "Cloracao")],
 ["<code>total_etap_capex</code>, which enters the CAPEX",
  "<code>total_etap_annual_opex</code>, which enters the running cost",
  "<code>total_etap_co2e_kg_yr</code>, which replaces chlorination in the LCA",
  "<code>disinfection_stages</code>, shown in the report"],
 "A purity outside (0, 1] is refused by the validator of the chlorination chain.",
),
(
 "PROC-16", "Compute the pumping energy", "bomba",
 "Economic analysis and LCA, from the same simulation result.",
 ["<code>supply_arrangement</code>: pumping to an upper tank, direct pressurisation or gravity",
  "<code>total_pumped_liters</code> and <code>total_pump_cycles</code> from PROC-08",
  "<code>pressurizer_pressure_m</code>, <code>pressurizer_starts_per_person_day</code>, "
  "<code>residents_count</code>",
  "<code>pump_power_kw</code>, <code>pump_efficiency</code>, <code>pump_flow_rate</code>",
  "<code>pump_manometric_head_m</code>", "<code>pump_startup_time_h</code>"],
 ["The arrangement decides what is pumped. <b>Pumping to an upper tank</b>: the volume sent to the upper tank. "
  "<b>Direct pressurisation</b>: all the rainwater consumed, with the working pressure in "
  "place of the head and no start-up energy. <b>Gravity</b>: nothing. It is the only source of kWh "
  "of the economic analysis and the LCA.",
  "Specific energy <code>e = ρgH/(η_pump·η_motor)</code> per m³ pumped, or "
  "<code>P/(Q·η_motor)</code> when the flow rate is declared.",
  "Nameplate power is shaft power and <b>already includes</b> the pump efficiency; that is why "
  "<code>P × hours / η_pump</code> counts that efficiency twice, and what is missing is to divide "
  "by the motor efficiency, entered by the user or taken from the typical value for the rated power. Four copies of that old formula survived in the "
  "program and overestimated consumption by 1.68 times — the worst of them ranked volumes in the "
  "multi-criteria decision.",
  "Start-up energy is added separately, by the number of cycles.",
  "Flow rate and efficiency not entered fall back to typical values <b>for the chosen power</b>, "
  "not to fixed constants."],
 [("pump_energy.py", "compute_annual_pump_energy"),
  ("pump_hydraulics.py", "energia_especifica_kwh_por_m3"),
  ("pump_hydraulics.py", "vazao_l_por_h"), ("pump_hydraulics.py", "rendimento_tipico")],
 ["<code>annual_kwh</code>, which becomes cost in the economic analysis and emission in the LCA",
  "<code>pump_hours_year</code>, <code>annual_cycles</code>"],
 "Gravity arrangement, an arrangement not stated in an old project, or zero power: the "
 "energy is zero.",
),
(
 "PROC-17", "Compute the water and sewage bill", "economico",
 "Twice per projected month: with and without harvesting.",
 ["monthly volume in litres", "<code>water_tariffs</code>: quadruples "
  "(minimum, maximum, value, code)", "<code>sewage_mode</code> and <code>sewage_rate</code>",
  "fixed and variable taxes", "<code>num_economias</code>"],
 ["Consumption is evaluated <b>at the level of one dwelling unit</b> and multiplied by the number of "
  "units, so as not to distort the progressive blocks in a building with individual metering.",
  "Code <b>1</b> or <b>0</b>: progressive block, charged only on the volume within it.",
  "Code <b>−1</b>, availability charge: a fixed value that <b>adds</b> on top of the metered consumption.",
  "Code <b>−2</b>, retroactive allowance: up to the allowance volume the fixed value is paid; "
  "beyond it, <b>all</b> the volume from zero is charged by the blocks.",
  "Code <b>−3</b>, payment floor: it does not add, it <b>bounds from below</b>. With a floor of 40 "
  "currency units and a charged consumption of 55, saving up to 15 reduces nothing — and that is exactly "
  "what a rainwater harvesting study needs to see.",
  "Sewage is a percentage of the <b>water part</b>, not of the total bill: where the sewer charge is "
  "100% of the water charge, it is half the bill.",
  "The six tariff regimes are described in appendix D; the user enters the table of the project."],
 [("economic.py", "calculate_water_bill"), ("tariff_regimes.py", "resumo_do_regime"),
  ("tariff_regimes.py", "validar_estrutura"), ("tariffs_structure.py", "CODIGOS_VALIDOS")],
 ["Value of the water and sewage bill per month, for the projection of PROC-18"],
 "An empty table gives a zero bill: the program does not assume a tariff. An incomplete structure is flagged by the "
 "validation gate, which separates errors from warnings.",
),
(
 "PROC-18", "Project the cash flow", "economico",
 "Economic tab, after the technical simulation.",
 ["CAPEX of the five items plus pump and treatment line",
  "monthly water and sewage saving from PROC-17",
  "running costs: pumping, chlorination, treatment line and declared operating costs",
  "<code>tma</code>, <code>inflation</code>, <code>analysis_period_years</code>",
  "separate escalations for water, sewage and energy, and the interval between them"],
 ["Water and sewage are escalated by <b>separate</b> indices, not by the aggregate bill.",
  "Inflation applies only to running costs; tariff escalations apply only to the bill.",
  "The escalation is applied every <code>tariff_escalation</code> months, in steps.",
  "The payback is the first month in which the discounted cumulative cash flow crosses zero."],
 [("economic.py", "run_economic_analysis"), ("economic.py", "calculate_effective_tariff")],
 ["<code>vpl</code>, <code>tir_monthly_pct</code>, <code>tir_annual_pct</code>, "
  "<code>payback_months</code>",
  "<code>monthly_cash_flows</code>, month by month",
  "<code>annual_pump_kwh</code>, <code>annual_chlorine_kg</code>, <code>etap_capex_brl</code>"],
 "A negative monthly saving is truncated at zero before entering the cash flow. An IRR without a "
 "real root returns null instead of an invented number.",
),
(
 "PROC-19", "Assess the life cycle", "acv",
 "Environmental tab, after the technical simulation.",
 ["<code>tank_vol_liters</code>", "<code>annual_pluvial_m3</code> from PROC-12",
  "materials and masses of the two tanks", "lengths per pipe diameter",
  "<code>pump_count</code>", "grid electricity factor", "production route of the potable water",
  "treatment line result from PROC-15"],
 ["Seven stages: lower cistern, upper tank, piping, pump set, pumping operation, "
  "treatment operation and avoided potable water.",
  "Zero volume <b>without</b> rainwater volume is the no-system scenario, and receives no fixed "
  "impact for tank, pipe or pump.",
  "The treatment line <b>replaces</b> the chlorination term; it does not add to it. Chlorination "
  "follows the treatment, not the upper tank.",
  "Upper tank only in the pumping arrangement; pump sets in every arrangement with a pump; energy "
  "from PROC-16.",
  "The avoided water is the water <b>delivered</b>, not produced: distribution losses mean "
  "that producing 1 m³ delivers less than 1 m³, and a factor given at the plant outlet must be "
  "converted to the volume delivered. The user enters the emission factor of the water delivered "
  "to the building and the factor of the local grid; the edition has no default for either.",
  "The carbon payback is the embodied carbon divided by the net annual saving; "
  "without a positive net saving, it returns 999 years instead of infinity."],
 [("environmental.py", "calculate_lca"), ("water_supply_routes.py", "co2_evitado_por_m3"),
  ("grid_emission_factors.py", "fator_co2eq")],
 ["<code>total_embodied_co2_kg</code>, <code>net_annual_avoided_co2_kg</code>",
  "<code>lifetime_net_co2_saved_kg</code>, which is a multi-criteria criterion",
  "<code>environmental_payback_years</code>", "<code>inventory_items</code>, the item-by-item inventory"],
 "A factor without a primary source receives a screening label, and the label is shown — the "
 "gap is declared, not hidden.",
),
(
 "PROC-20", "Map onto certifications", "esg",
 "Environmental tab and reports.",
 ["<code>potential_potable_savings_pct</code>", "annual rainwater and potable volumes",
  "indoor/outdoor split from PROC-09", "CO₂ avoided over the life cycle",
  "<code>area</code>, for the catchment area of WEM14",
  "EDGE base case, when declared"],
 ["<b>LEED v4</b>: WEc1 up to 2 points for outdoor use, WEc2 up to 6 points for indoor use, "
  "on the official scale. Without an outdoor demand, WEc1 is zero and says why.",
  "<b>LEED v5 BD+C</b> (rating system of November 2025): WEc2 up to 8 points, by Option 1 "
  "(whole project, 30% to 65%, +1 with an alternative source) or by the sum of Options 2 (fixtures "
  "and fittings, 30% to 40%), 4 (outdoor, 50% and 100%) and 6 (on-site reuse, 2 points), new "
  "construction only. SSc3 recorded as not assessed; its reuse point does not exceed the cap of 3.",
  "<b>EDGE</b>: <b>does not score points</b>. It measures a percentage against a local base case and "
  "compares it with 20%, in three independent bars. The advanced level raises the <i>energy</i> bar "
  "to 40%, not the water one. The program assesses only the water bar, by measure WEM14, and says "
  "that the other two are outside its reach.",
  "Without a declared base case, EDGE uses the modelled demand and warns that the number is a <b>floor</b>.",
  "<b>GRI 303</b>: avoided withdrawal and circularity rate."],
 [("esg_certifications.py", "calculate_esg_certifications"),
  ("edge_certification.py", "avaliar_agua_edge"),
  ("edge_certification.py", "consumo_base_anual_m3")],
 ["<code>credit_details</code>: the credit matrix that feeds the on-screen table and the "
  "reports", "<code>esg_summary_text</code>", "cards for LEED, EDGE and GRI"],
 "A null total demand returns zero per cent without dividing by zero.",
),
(
 "PROC-21", "Rank volumes by multiple criteria", "mcdm",
 "Optimiser tab, with the sweep done.",
 ["one candidate per sweep volume, each with volumetric reliability, storage efficiency, "
  "net financial savings, LCOW, discounted payback, life-cycle CO₂, dry mass and annual overflow",
  "four dimension weights (technical, economic, environmental, structural) and eight criterion "
  "shares, eight criterion weights, or <code>critic</code> for objective weights",
  "tolerance of the choice band, 5% of the score range by default"],
 ["Eight criteria in four dimensions: <b>maximise</b> volumetric reliability, storage efficiency "
  "and net financial savings; <b>minimise</b> LCOW, payback, CO₂, dry mass and overflow.",
  "Each dimension weight is shared among its criteria by the criterion shares (equal by default). "
  "Three weights, from version 0.1.0, give the structural dimension their mean; seven values are "
  "refused.",
  "With <code>critic</code>, the weights are computed from the results by the CRITIC method: "
  "the contrast of each criterion across the volumes times its independence from the others.",
  "A volume that does not pay back receives the worst payback observed plus 10% (at least one year "
  "more and at least 20 years); the volume with no cistern receives the worst LCOW plus 10%.",
  "Normalisation shifts by <code>x − min(x)</code> <b>before</b> the vector normalisation "
  "of Hwang and Yoon, to admit a negative NPV. It is a deliberate variant, and must be "
  "declared as a variant.",
  "SMAA-VIKOR draws eight weights, with 25% expected on each dimension, and returns the "
  "probabilities of each volume taking each rank.",
  "The choice band gathers the volumes whose score lies within the tolerance of the best, on a "
  "scale from the worst (0) to the best (1) of the volumes evaluated.",
  "Opricovic's conditions C1 and C2 are not implemented."],
 [("topsis.py", "calculate_topsis_scores"), ("mcdm_methods.py", "run_vikor")],
 ["Ranking of the volumes, distance to the ideal per criterion, choice band and highest score"],
 "A single candidate returns a trivial ranking. A criterion constant across candidates does not "
 "contribute to the distance.",
),
(
 "PROC-22", "Save and reopen the project", "arquivo",
 "Save and open menu.",
 ["the whole <code>TritonConfig</code>, with the fields of appendix {{n:A}}", "interface state", "current analysis"],
 ["JSON format, in named sections.",
  "Reading uses a default value field by field, so an old file keeps opening.",
  "<code>created_at</code> and <code>precip_file</code> describe the act of saving, not the "
  "project: that is why they do not come back.",
  "It is the fifth crossing of the program — the one that crosses <b>time</b> rather than modules. "
  "Thirty of the 87 fields of the time did not survive the round trip, including the whole "
  "treatment-line choice, the manometric head, the tank materials and irrigation."],
 [("parser.py", "export_triton_json"), ("parser.py", "load_triton_project")],
 ["<code>.triton</code> file", "rebuilt <code>TritonConfig</code>"],
 "A section missing from the file falls back to the class defaults. Invalid JSON stops "
 "opening with a message.",
),
(
 "PROC-23", "Issue reports and exports", "relatorio",
 "Reports tab; Export tab.",
 ["results of PROC-12, PROC-18, PROC-19, PROC-20 and PROC-21", "project data"],
 ["Three reports: executive, environmental with ESG, and research.",
  "Export to CAD and BIM from the sizing.",
  "Spreadsheets with the daily series and the sweep."],
 [("report_generator.py", "generate_executive_html_report"),
  ("report_generator.py", "generate_environmental_html_report"),
  ("report_generator.py", "generate_research_html_report"),
  ("report_generator.py", "save_pdf_report")],
 ["HTML, PDF, DXF, JSON for BIM and XLSX"],
 "Conversion to PDF tries the Qt engine and falls back to the alternative generator when it "
 "is not available.",
),
(
 "PROC-24", "Automation for large-scale studies", "cli",
 "The <code>triton</code> command line, described in section {{n:19}}; it comes with the "
 "installation as a Python package, not with the Windows installer.",
 ["project file", "rainfall file"],
 ["Calls the <b>same</b> calculation core as the window, without a screen.",
  "Only part of the parameters can be reached through it; the others exist only in the interface, "
  "and the way is to build the project in the window and vary by automation only what changes "
  "between cases.",
  "It serves factorial matrices of thousands of cases and uncertainty propagation by "
  "sampling, which are the instruments of the studies published by the group."],
 [],
 ["JSON and CSV with the results"],
 "A parameter out of range is refused before simulating, with the same validation gate "
 "as the interface.",
),
]

FAMILIAS = {
    "chuva": ("Rainfall", "dad"), "demanda": ("Demand", "ent"),
    "balanco": ("Water balance", "nuc"), "etap": ("Quality and treatment", "nuc"),
    "bomba": ("Pump set", "nuc"), "economico": ("Economic", "sai"),
    "acv": ("LCA", "sai"), "esg": ("ESG and certifications", "sai"),
    "mcdm": ("Multi-criteria", "sai"), "arquivo": ("Project file", "ent"),
    "relatorio": ("Reports", "sai"), "cli": ("Automation", "sai"),
}
