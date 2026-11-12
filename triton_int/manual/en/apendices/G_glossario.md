# Glossary

Technical terms and acronyms used in the manual and in the program. The terminology guidelines of
Triton close the appendix.

---

**Allowance within the minimum**. Tariff regime in which the fixed value already includes a volume of
consumption. Saving **below** the allowance does not reduce the bill.

**Availability charge**. Tariff regime in which a fixed value is **added** on top of the metered
consumption. Every cubic metre saved earns a discount.

**BD+C** (*Building Design and Construction*). Family of LEED rating systems for the design and
construction of new or substantially refurbished buildings. It is the family dealt with in this
manual, in versions 4, 4.1 and 5.

**BIM** (*building information modelling*). Digital representation of the building in which each
component carries properties beyond geometry, which allows the designs of different disciplines to
be coordinated.

**CAD** (*computer-aided design*). The program exports the hydraulic schematic in DXF, an exchange
format accepted by CAD programs.

**CAPEX** (*capital expenditure*). Initial investment.

**Carbon payback**. Time for the net annual emission saving to pay off the carbon embodied in the
manufacture of the system.

**Catchment area**. **Horizontal** projection of the impermeable roof surface on which water is
collected, as in EN 16941-1:2024. It is not the sloping area of the roof, nor the contributing area
used to size gutters.

**CDD** (*consecutive dry days*). Longest sequence of consecutive days with rain below 1 mm.

**Criterion shares**. In the multi-criteria decision, how much of the weight of each dimension goes to
each of its criteria. Only the proportion within the dimension matters; the default is equal shares,
and a share of zero removes the criterion from the calculation.

**CSV** (*comma-separated values*). Text file format in which each line is a record and the columns
are separated by a character, typically a comma or a semicolon. It is the format of the
precipitation series.

**CWD** (*consecutive wet days*). Longest sequence of consecutive days with rain equal to or above
1 mm.

**Discounted payback**. Time for the cumulative discounted cash flow to cross zero.

**DN** (*nominal diameter*). Commercial designation of the diameter of a pipe or fitting, in
millimetres. It corresponds exactly to neither the internal nor the external diameter: it is a
reference number from which the real dimensions follow, tabulated by standard.

**Dry mass** (of the system). Mass of the cisterns, pipes, pump and fittings without water, given by
the program's weight calculator. It is a criterion of the structural dimension of the multi-criteria
decision.

**DXF** (*drawing exchange format*). Exchange format for technical drawings, read by practically all
CAD programs.

**EDGE** (*excellence in design for greater efficiencies*). Certification system of the World Bank's
International Finance Corporation. It measures the percentage saving against a local baseline in
three independent dimensions and requires each to cross the threshold.

**EN** (*Europäische Norm*, European standard). Standard published by the European Committee for
Standardization. In this manual, EN 15978, which defines the building life cycle modules, EN 15804,
which governs the environmental product declarations of construction products, and EN 16941-1, on
rainwater harvesting systems.

**EPD** (*Environmental Product Declaration*). Third-party verified document, according to ISO 14025
and, in construction, EN 15804, that publishes the life cycle impacts of a product per declared
unit. It is the preferred source of emission factors for materials and equipment.

**ESG** (*environmental, social and governance*). Set of environmental, social and governance
criteria used in assessing companies and developments. The program feeds environmental indicators
of that set.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). International working group that
standardised the indices of climate extremes, of which the program calculates eight.

**First flush**. Initial depth of rain diverted from the system, which carries the dirt deposited on
the roof. In Triton it is **subtracted** from the day's rain, in millimetres. The manual's examples
use 2 mm; the right value depends on the roof and on the local practice, and must be declared.

**GRI** (*Global Reporting Initiative*). International standard for corporate disclosure of social
and environmental performance. Its 303 series deals with water and effluents.

**IFC**. The acronym designates two different things. In certification, it is the World Bank's
*International Finance Corporation*, which develops EDGE. In the BIM context, it is *Industry
Foundation Classes*, an open exchange format the program does **not** export: the program's BIM
export is a JSON file of properties.

**Ideal volume** (optimal tank volume). Smallest tank volume of the simulation grid from which the
marginal gain in potable water saving ($\Delta E_{pot} / \Delta V$) falls below a declared threshold
(typically $1.0\%/\text{m}^3$ or $0.5\%/\text{m}^3$). It avoids oversizing tanks, securing the best
cost-benefit ratio.

**Individual metering**. Metering per dwelling unit in a multi-family building. Entered in the
program as the number of units.

**INT**. Acronym of the program's International Edition: it opens in English and ships no
national data. Rainfall series, tariffs, costs, currency and emission factors are entered by the
user; three example cities (New York, London and Cape Town) come with it.

**IPCC** (*Intergovernmental Panel on Climate Change*). Intergovernmental panel that synthesises
scientific knowledge on climate change and organises the assessment reports to which the climate
projections refer.

**IRR**. Internal rate of return. The discount rate that makes the net present value zero.

**ISO 14040**. International standard that sets out the principles and framework of life cycle
assessment. An inventory conforming to ISO 14040 requires traceability of each flow and external
critical review, requirements a screening assessment does not meet.

**JSON** (*JavaScript object notation*). Structured text file format, readable by people and by
programs. It is the internal format of the `.triton` file.

**LCA**. Life cycle assessment. Method that accounts for the environmental impacts of a product over
its whole existence, from the extraction of raw materials to disposal. The program's is a
**screening** one, not a full inventory conforming to ISO 14040.

**LCOW** (*levelised cost of water*). Ratio between the investment plus the discounted running costs
of the system (pumping energy, operation and maintenance, chlorine and the treatment line) and the
discounted volume of rainwater delivered over the analysis horizon, at the same rate, in currency per
m³. It allows the cost of the rainwater to be compared directly with the utility's tariff, and it is
one of the eight multi-criteria criteria (section {{n:32}}).

**LEED** (*leadership in energy and environmental design*). Environmental certification system for
buildings of the *U.S. Green Building Council*, the most widespread internationally. It deals with
water efficiency in the *Water Efficiency* category: in version 4, by credits WEc1 and WEc2; in
version 5, by credit WEc2, *Enhanced Water Efficiency*.

**Marginal gain**. Change in the saving potential per cubic metre added to the tank, in %/m³
($\Delta E_{pot} / \Delta V$). Selection criterion of the ideal volume.

**Metre of head** (m). Unit of pressure equal to that exerted by a column of water one metre high,
about 9.81 kPa. It is the usual unit in building installations. The project file and some screens
abbreviate it to «m.c.a.» (the abbreviation of the same unit in a few languages).

**MARR** (*minimum attractive rate of return*). The discount rate adopted in the economic analysis.
It is entered in the field `tma`, in per cent per month.

**Motor efficiency**. Ratio between the mechanical power at the shaft and the electrical power drawn
from the mains. Motor standards require it to be marked on the rating plate.

**Non-potable water**. Water not intended for direct human consumption, but which meets the quality
required by the applicable national standard for the uses admitted: flushing toilets and urinals,
washing vehicles, pavements and floors, landscape irrigation, laundry and cooling towers.

**NPV**. Net present value.

**Overflow** (spillage). Volume that exceeds the capacity of the tank and is led away by the overflow
pipe when the tank is already full.

**Payment floor**. Tariff regime in which the bill **does not go** below a value. Different from the
availability charge: the floor limits from below, the availability charge adds on top.

**PB** (*base price*). Base price, in currency per m³, of the exponential tariff formula `PB × Cⁿ`, in
which `C` is the month's consumption and `n` the exponent for that consumption.

**PEAD**. Code of the high-density polyethylene (HDPE) tank material in the project file.

**Pluvial demand** ($D_{pl}$). Part of the building's daily water demand that can be supplied by the
harvesting system ($D_{pl,t} = D_{tot,t} \times f$). It corresponds to the non-potable points of use
connected to the rainwater network.

**Potable water**. Water that fully meets the drinking-water standard of the country of the project,
intended for drinking, food preparation and personal hygiene.

**Potable water saving potential** ($E_{pot}$). Fraction of the **total** demand of the building
supplied by rainwater ($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$). It is the program's
central indicator, bounded above by the suppliable fraction ($E_{pot} \le f$).

**pp**. Percentage points. Used to express the difference between two percentages: from 35% to 37% is
two percentage points, not two per cent.

**PRCPTOT**. Total annual precipitation on wet days.

**PRFV**. Glass-fibre reinforced plastic (GRP), the material of medium and large tanks. It appears in
the program as «fibreglass» (code `FIBRA`).

**Pump efficiency**. Ratio between the hydraulic power delivered to the water and the mechanical
power at the shaft. It does not include the motor.

**PVC**. Polyvinyl chloride, the material of building cold-water piping and of the first-flush
diversion columns.

**R95p**. Sum of the precipitation of the days above the 95th percentile of the wet days.

**Rainwater**. Atmospheric precipitation collected directly on impermeable roof surfaces (roofs and
waterproofed slabs), before it reaches the ground or public drains.

**Rainwater harvesting**. Use of the water falling on roofs for non-potable uses in buildings.
«Harvesting» is preferred to «reuse», since rainwater collected on the roof is a primary resource and
not an effluent of earlier human use.

**Rainwater harvesting system**. Integrated set of building components — catchment area, pipes, first
flush, treatment line, lower cistern, upper tank, pump set or pressure pump and an independent
distribution network — designed to collect, treat, store and supply non-potable water.

**Representative rainfall series length** ($N_{rep}$). Shortest continuous period, in years of daily
rainfall data, needed to stabilise the sizing and performance of the system statistically
(reproducing the ideal volume and the saving potential of the full series with confidence
$\ge 90\%$), according to the method of Geraldi and Ghisi (2017, 2018, 2019). The length needed is not
a fixed geographical constant: it grows with the suppliable fraction and with the demand level of the
building.

**Retroactive allowance**. Tariff regime in which consumption up to the allowance pays a fixed value
and consumption above it is billed in full from 0 m³.

**Runoff coefficient**. Fraction of the rain that actually reaches the tank, after losses to
absorption, evaporation and initial wetting of the roof.

**RX1day**, **RX5day**. Largest precipitation in one and in five consecutive days, in the year.

**SB** (*basic service*). Basic service charge: the fixed monthly part of a water bill, added to the
result of the exponential formula.

**SDII** (*simple daily intensity index*). Mean precipitation of the wet days.

**SI** (*seasonality index*). Walsh and Lawler seasonality index. Zero when rain is uniform over the
year.

**SMAA** (*stochastic multicriteria acceptability analysis*). Method that draws weights and returns
the probability of each alternative winning.

**SSP** (*shared socioeconomic pathways*). Coherent hypotheses of global development and the
corresponding emissions. They are combined with the climate models to produce projections.

**Stochastic demand**. Modelling daily water consumption as a probabilistic variable that varies
from day to day and between realisations (Silva and Ghisi, 2016), allowing the uncertainty range of
the sizing and of the performance indicators to be assessed under real variability of use.

**Storage efficiency**. Rainwater delivered per day divided by the volume of the lower cistern, in %:
the daily turnover of the stored volume. It falls as the volume grows and is a technical criterion of
the multi-criteria decision. Not to be confused with the mean occupancy of the tank.

**Stormwater**. Rainwater after urban surface runoff, or when led by building drainage and storage
pipes and systems. In this manual the word is used only for drainage; the harvesting system,
the rainwater network, the pluvial demand, the rainwater consumption and the overflow all take
«rainwater» or «pluvial».

**Suppliable fraction** (non-potable demand share, $f$). Percentage of the building's total water
demand ($D_{tot}$) that can be supplied by rainwater ($f = D_{pl} / D_{tot}$). It is the
**insurmountable asymptotic ceiling** of the potable water saving potential ($E_{pot} \le f$): even
with infinite storage and unlimited rain, the potable saving never exceeds the suppliable fraction,
because the rest ($1 - f$) is reserved for potable uses. It is distinct from volumetric reliability
($C_v = E_{pot} / f$), which assesses the supply of the rainwater part.

**Time reliability** ($C_t$). Percentage of days on which the system fully ($V_{con,t} = D_{pl,t}$),
partly or not at all supplied the rainwater demand.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*). Multi-criteria
ranking method of Hwang and Yoon. In the program, it ranks the volumes by eight criteria in four
dimensions: technical, economic, environmental and structural.

**Treatment line** (code `ETAP`). In the program, the set of inlet filter, disinfection and polishing
filter that treats the rainwater before use.

**UV**. Ultraviolet radiation, used in water disinfection by inactivating micro-organisms. It acts
only at the moment of passage through the reactor and leaves no residual, unlike chlorination.

**VIKOR**. Multi-criteria decision method proposed by Opricovic, which seeks a compromise solution
between conflicting criteria. See also *SMAA*.

**Volumetric reliability** ($C_v$). Fraction of the **rainwater** demand the system supplied
($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Not to be confused with the saving potential,
whose denominator is the total demand of the building.

**WEM**. Coding of the EDGE water efficiency measures. WEM14 is the rainwater harvesting system.

**XLSX**. Microsoft Excel workbook format, based on compressed XML. It is one of the export formats
for spreadsheets and command-line results.

**YAS** (*yield after spillage*). Operating rule in which overflow is calculated **before** the demand
is withdrawn and, in the strict form, the day's withdrawal comes only from the volume stored the day
before. The program calculates overflow first, as YAS does, but lets the day's rain meet the day's
demand; it lies between YAS and YBS (section {{n:23}}).

**YBS** (*yield before spillage*). Operating rule in which the demand is withdrawn **before** overflow
is calculated. It assumes consumption before the day's rain and overestimates the yield; the program
does not adopt it, and its result lies between YAS and YBS.

---

## Triton's terminology and naming guidelines

Consistent terminology is essential to technical rigour in scientific papers, technical reports, the
graphical interface and Triton's documentation. The conventions below detail the distinction between
related terms that are often confused.

### 1. Rainwater and stormwater

<!-- tabela: Terminology for rainwater and stormwater -->
| Term | Definition and context of use | Status in Triton |
| :--- | :--- | :--- |
| *rainwater* | Precipitation collected directly on the roof (roof or waterproofed slab), before it reaches the ground or drains. It refers to the **water source** and the resource collected. | **Canonical and preferred**, also for systems, networks and the balance («rainwater network», «rainwater demand»). |
| *stormwater* | Rainwater after urban surface runoff, or when led by building drainage. It applies to the **drainage** infrastructure. | Used only for drainage. |

### 2. Suppliable fraction, pluvial demand, potential and reliability

To avoid the mathematical and conceptual ambiguities often found in the literature:

<!-- tabela: Fundamental quantities of the water balance and relations between fraction and potential -->
| Quantity | Symbol / Code | Definition | Formula | Relation / Ceiling |
| :--- | :--- | :--- | :--- | :--- |
| **Suppliable fraction** | $f$ / `rainwater_share` | Share of the building's total demand corresponding to non-potable points of use that can be connected to the harvesting system. | $f = D_{pl} / D_{tot}$ | Design parameter ($0 \le f \le 1$). It is the **asymptotic ceiling** of $E_{pot}$. |
| **Pluvial demand** | $D_{pl}$ / `rainwater_demand` | Volume of water required by the building's non-potable points of use over a time interval. | $D_{pl,t} = D_{tot,t} \times f$ | In L/day or m³/year. |
| **Rainwater volume consumed** | $V_{con}$ / `pluvial_consumed` | Volume of non-potable water actually supplied by the rainwater tank to the points of use. | Determined by the daily balance (section {{n:23}}) | $V_{con,t} \le D_{pl,t}$ and $V_{con,t} \le S_{t-1} + C_t$. |
| **Potable water saving potential** | $E_{pot}$ / `potential_potable_savings_pct` | Percentage of the building's **total** demand saved by rainwater harvesting. | $E_{pot} = \frac{\sum V_{con}}{\sum D_{tot}} \times 100\%$ | **Central indicator**. Always $E_{pot} \le f$. |
| **Volumetric reliability** | $C_v$ / `volumetric_reliability_pct` | Percentage of the **rainwater** demand supplied by the stored rainwater. | $C_v = \frac{\sum V_{con}}{\sum D_{pl}} \times 100\%$ | $C_v = \frac{E_{pot}}{f}$. It can reach 100% even when $E_{pot} < 100\%$. |
| **Time reliability** | $C_t$ / `temporal_reliability_pct` | Percentage of days of the series on which the rainwater demand was 100% supplied ($V_{con,t} = D_{pl,t}$). | $C_t = \frac{N_{full\_days}}{N_{total}} \times 100\%$ | It measures the security of daily supply without potable top-up. |

### 3. Recommended naming for papers and reports

- Use **«rainwater harvesting»** (not «rainwater reuse» — rainwater is not an effluent; its use is
  *harvesting*, not *reuse*).
- Use **«catchment area»** for the horizontal plane of the roof (EN 16941-1) and keep
  **«contributing area»** exclusively for the hydraulic sizing of gutters under wind.
- Use **«first flush»** for the initial depth diverted, declaring its value in millimetres, not
  «first-flush threshold».
- Use **«suppliable fraction»** or «non-potable demand share» (not «relative demand» or «saving
  fraction») to express the share of non-potable uses in total consumption.
- Use **«representative series length»** for the minimum length in years needed for the statistical
  stabilisation of the simulation (Geraldi and Ghisi method).
- Use **«LCOW»** or **«levelised cost of water»** for the unit cost metric over the life cycle
  discounted at the minimum attractive rate of return.
