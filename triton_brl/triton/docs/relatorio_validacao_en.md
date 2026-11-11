# TECHNICAL AND COMPUTATIONAL VERIFICATION REPORT — TRITON

**Sustainable Environments Research Group**  
*Faithful Replication and Engineering Validation of Triton*  
**Scope:** automated regression and invariant evidence | **How to reproduce:** `python -m pytest tests -v`

---

## 1. EXECUTIVE SUMMARY

This report describes automated **internal verification** evidence for Triton. It is not external validation: the tests exercise the software's own equations and regressions but do not replace independent comparison with measurements, certification, detailed design, or professional review of local assumptions.

| Evidence | Automated case | Acceptance criterion | Scope |
| :--- | :--- | :--- | :--- |
| **Daily mass conservation** | 100 synthetic days, two tanks | absolute residual ≤ `1×10⁻⁷ L` per day | internal invariant |
| **Optional legacy-output comparison** | up to 20 rows of `Planilha.csv`, when available | MAE < 3 percentage points for optimum potential | sample regression, not 4,050 cases |
| **Tiered tariff and sewage** | unit cases with analytical answers | `pytest.approx` numerical tolerance | equation verification |
| **Pump, CAPEX, O&M, chlorine and LCA** | unit cases and three-model study | residuals shown in the generated study | equations/assumptions |
| **TOPSIS** | ranking, invalid weights, translation invariance, gaps and rendering | analytical answers and `[0,1]` ranges | implemented-method verification |

---

## 2. DAILY WATER BALANCE VALIDATION METHODOLOGY

The invariant test uses a reproducible 100-day synthetic series and checks non-negativity, tank bounds and equality between inputs and outputs on every day. The three-model study adds long working rainfall series and one audited day per climate. The legacy-spreadsheet regression runs only when its external dataset is present; it samples up to 20 rows and uses the criterion declared by the test itself.

### Key Mass Conservation Equations:
1. **Effective rainfall and daily capturable volume** (the first-flush depth is subtracted):
   $$P_{\text{eff},t}=\max(0,\,P_t-d_f)\;\text{when the rule applies};\quad P_{\text{eff},t}=P_t\;\text{otherwise}$$
   $$V_{\text{harvested},t}=P_{\text{eff},t}\,C_{\text{runoff}}\,A_{\text{catchment}}$$
   The engine subtracts $d_f$ from the rainfall of each day on which the rule applies, so a day with rainfall at or below $d_f$ yields no capture. This differs deliberately from Netuno 4, which treated $d_f$ as an event threshold.
2. **YAS lower-tank balance**:
   $$I_t=\min(V_{\text{inf,max}},S_{t-1}+V_{\text{harvested},t});\quad O_t=\max(0,S_{t-1}+V_{\text{harvested},t}-V_{\text{inf,max}})$$
   $$Y_t=\min(D_{\text{rainwater},t},I_t);\quad S_t=I_t-Y_t$$
3. **Two-tank invariant** (pumping is an internal transfer):
   $$S_{\text{inf},t-1}+S_{\text{sup},t-1}+V_{\text{harvested},t}=S_{\text{inf},t}+S_{\text{sup},t}+Y_t+O_t$$

---

## 3. ECONOMIC ANALYSIS VALIDATION METHODOLOGY

The suite verifies the implemented financial model by numerical substitution. Netuno 4 reference routines guide tariff and O&M semantics, while the current robust flow uses an explicit annual projection.

### 3.1. Multi-Tier Tariff Structure (Equations 5.1 to 5.4)
The calculation of the monthly water bill $C_{\text{water}}$ respects the tier-accumulated cost and sewage $C_{\text{sewage}}$:
$$C_{\text{total}} = C_{\text{water}} + C_{\text{sewage}} + C_{\text{tax,var}} + C_{\text{tax,fixed}}$$

### 3.2. Pump Electricity Consumption (Equations 5.6 to 5.10)
The monthly pump operation time $t_{\text{total}}$ considers continuous pumping and startup time $t_{\text{startup}}$:
$$t_{\text{rec}} = \frac{V_{\text{pumping,month}}}{Q_{\text{pump}}}$$
$$t_{\text{startup}} = n_{\text{cycles,month}} \cdot t_{\text{startup,s}}$$
$$E_{\text{kWh}} = \frac{P_{\text{kW}} \cdot (t_{\text{rec}} + t_{\text{startup}})}{\eta_{\text{pump}}}$$

### 3.3. Financial Indicators (NPV, IRR and Discounted Payback)
$$\text{NPV} = - \text{CAPEX} + \sum_{t=1}^{N} \frac{\Delta C_{\text{water},t}+\Delta C_{\text{sewage},t}-C_{\text{pump},t}-C_{\text{O\&M},t}-C_{\text{chlorine},t}}{(1 + i_{\text{MARR}})^t}$$

---

## 4. AUTOMATED TEST SUITE AND ACCEPTANCE CRITERIA

Run `python -m pytest tests -v` in the project environment to obtain the current count and outcome. The suite is arranged by purpose: mass-conservation and financial invariants; unit tests for simulation, parser, economics, LCA and TOPSIS; and integrations for reports, scenarios and the interface. The cases below are traceable examples; the displayed outcome must always be the result of the current execution.

```text
tests/test_batch_validation.py::test_daily_water_balance_validation_sample PASSED
tests/test_daily_water_balance.py::test_simple_3day_water_balance PASSED
tests/test_economic.py::test_water_bill_multi_tier_calculation PASSED
tests/test_economic.py::test_sewage_fixed_and_water_taxes PASSED
tests/test_economic.py::test_pump_operational_electricity_costs PASSED
tests/test_economic.py::test_additional_operational_costs PASSED
tests/test_economic.py::test_economic_vpl_and_payback_favorable PASSED
tests/test_economic.py::test_economic_unfavorable_scenario_negative_vpl PASSED
tests/test_parser.py::test_parse_float_and_int PASSED
tests/test_parser.py::test_load_precipitation_file PASSED
tests/test_parser.py::test_parse_triton_project_csv PASSED
tests/test_parser.py::test_export_netuno4_csv_roundtrip PASSED
tests/test_simulation.py::test_zero_rain_simulation PASSED
tests/test_simulation.py::test_extreme_rain_simulation PASSED
tests/test_simulation.py::test_dual_tank_pumping PASSED
tests/test_sweep_optimal_volume_determination PASSED
```

---

## 5. CONCLUSION AND LIMIT OF EVIDENCE

The tests provide evidence that the covered behaviour remains stable. The application is decision support: rainfall series, tariffs, quotes, applicable standards, materials and final sizing must be reviewed by a qualified professional.
