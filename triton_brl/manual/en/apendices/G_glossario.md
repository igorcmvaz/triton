# Glossary

Technical terms and acronyms, in English, with the Portuguese term in brackets where it appears in
the Brazilian literature, in the program's Portuguese interface or in this manual's figures. Many
acronyms are Portuguese; they are listed under the acronym itself, as the program prints it. The
terminology guidelines of Triton close the appendix.

---

**ABNT**. *Associação Brasileira de Normas Técnicas*, the body that publishes the Brazilian
standards. A standard is identified by the acronym NBR followed by the number and the year of the
edition, as in ABNT NBR 15527:2019.

**ANEEL**. *Agência Nacional de Energia Elétrica*, the Brazilian electricity regulator, which
approves the tariffs of the distribution companies. The Brazil Edition reads from them the price of
pumping energy, and the tariffs are updated from the agency's open data.

**AQUA-HQE**. Environmental certification system for buildings, the Brazilian adaptation of the
French HQE led by Fundação Vanzolini. In the 2024 residential scheme, water is dealt with in the
«Water consumption» theme, in items classified into the levels PR, HQE, HQE 2 and HQE 3.

**Availability charge** (*tarifa de disponibilidade*). Tariff regime in which a fixed value is
**added** on top of the metered consumption. Every cubic metre saved earns a discount.

**Allowance within the minimum** (*franquia no mínimo*). Tariff regime in which the fixed value
already includes a volume of consumption. Saving **below** the allowance does not reduce the bill.

**BD+C** (*Building Design and Construction*). Family of LEED rating systems for the design and
construction of new or substantially refurbished buildings. It is the family dealt with in this
manual, in versions 4, 4.1 and 5.

**BIM** (*building information modelling*). Digital representation of the building in which each
component carries properties beyond geometry, which allows the designs of different disciplines to
be coordinated.

**BRL**. Acronym of the program's Brazil Edition, the one with the Brazilian data: the CLIMBra
climate database, tariffs of 652 municipalities, ANEEL energy, costs in reais and national
certifications. Section {{n:2}} compares the two editions.

**CAD** (*computer-aided design*). The program exports the hydraulic schematic in DXF, an exchange
format accepted by CAD programs.

**CAPEX** (*capital expenditure*). Initial investment.

**CASAN**. *Companhia Catarinense de Águas e Saneamento*, the water and sewage utility of
Florianópolis and of much of Santa Catarina. Its tariff structure is the one adopted in this
manual's tutorial.

**Catchment area** (*área de captação*). **Horizontal** projection of the impermeable roof surface
on which water is collected, according to item 3.6 of NBR 15527:2019 and to EN 16941-1:2024. It is
not the sloping area of the roof, nor the contributing area of NBR 10844, which serves to size
gutters.

**Carbon payback** (*payback de carbono*). Time for the net annual emission saving to pay off the
carbon embodied in the manufacture of the system.

**CDD** (*consecutive dry days*). Longest sequence of consecutive days with rain below 1 mm.

**CEDAE** (*Companhia Estadual de Águas e Esgotos do Rio de Janeiro*). The Rio de Janeiro state water
and sewage company. Its tariff structure — a 15 m³ minimum bill (Tariff 1) and blocks priced as
multiples of a reference tariff — was inherited by Águas do Rio, Rio+ Saneamento and Águas da Imperatriz.

**CLIMBra** (*Climate Change Dataset for Brazil*). High-resolution gridded daily meteorological
dataset (0.25° × 0.25°, ~28 km) for the whole of Brazil, covering 19 CMIP6 global climate models and
the SSP2-4.5 and SSP5-8.5 emission scenarios. Developed by Ballarin et al. (2023) in [*Scientific Data* (Nature)](https://www.nature.com/articles/s41597-023-01956-z) ([doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)) and publicly available from the [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316) ([doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)).
The raw projections were bias-corrected by *Quantile Delta Mapping* (QDM) using the observational
dataset of Xavier, King and Scanlon (2016) as reference. In Triton, CLIMBra is the climate
database for 652 Brazilian cities (historical series from 1980 to 2013 and continuous future
projections from 2015 to 2100), shipped with the Brazil Edition only.

**CMIP6**. Sixth phase of the *Coupled Model Intercomparison Project*, the coordinated international
exercise that produces the climate projections used by the IPCC reports. The program's climate
database derives from it.

**CORSAN**. *Companhia Riograndense de Saneamento*, the water and sewage utility of much of Rio
Grande do Sul. It bills water by the exponential formula `PB × Cⁿ` plus the basic service charge,
not by consumption blocks.

**CSV** (*comma-separated values*). Text file format in which each line is a record and the columns
are separated by a character, typically a comma or a semicolon. It is the format of the
precipitation series.

**CV** (*cavalo-vapor*). Metric horsepower, a unit of power equal to 0.7355 kW, usual in the
Brazilian pump trade. A half-hp pump set has 0.37 kW of shaft power. This manual writes it as «hp».

**CWD** (*consecutive wet days*). Longest sequence of consecutive days with rain equal to or above
1 mm.

**Discounted payback** (*payback descontado*). Time for the cumulative discounted cash flow to cross
zero.

**DN** (*diâmetro nominal*, nominal diameter). Commercial designation of the diameter of a pipe or
fitting, in millimetres. It corresponds exactly to neither the internal nor the external diameter:
it is a reference number from which the real dimensions follow, tabulated by standard.

**DXF** (*drawing exchange format*). Exchange format for technical drawings, read by practically all
CAD programs.

**EAU**. Prefix of the items of the «Water consumption» theme in the AQUA-HQE rating system, from the
French *eau*, water. The items related to rainwater harvesting are EAU.1.2, EAU.1.3 and EAU.1.5.

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

**ETAP** (*estação de tratamento de água pluvial*). Rainwater treatment plant. In the program, the set
of inlet filter, disinfection and polishing filter.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). International working group that
standardised the indices of climate extremes, of which the program calculates eight.

**First flush** (*descarte de primeiras águas*). Initial depth of rain diverted from the system,
which carries the dirt deposited on the roof (a minimum of 2 mm according to NBR 15527:2019). In
Triton it is **subtracted** from the day's rain; in Netuno 4 it was treated as an event threshold.

**GRI** (*Global Reporting Initiative*). International standard for corporate disclosure of social
and environmental performance. Its 303 series deals with water and effluents.

**HQE** (*Haute Qualité Environnementale*). French high environmental quality rating system, basis of
AQUA-HQE. It also designates the levels of the rating system's items: HQE, HQE 2 and HQE 3, in
increasing order of requirement, above the prerequisite (PR).

**IFC**. The acronym designates two different things. In certification, it is the World Bank's
*International Finance Corporation*, which develops EDGE. In the BIM context, it is *Industry
Foundation Classes*, an open exchange format the program does **not** export: the program's BIM
export is a JSON file of properties.

**Ideal volume** (*volume ideal*, optimal tank volume). Smallest tank volume of the simulation grid
from which the marginal gain in potable water saving ($\Delta E_{pot} / \Delta V$) falls below a
declared threshold (typically $1.0\%/\text{m}^3$ or $0.5\%/\text{m}^3$). It avoids oversizing tanks,
securing the best cost-benefit ratio.

**Individual metering** (*micromedição*). Metering per dwelling unit in a multi-family building.
Entered in the program as the number of units (*economias*).

**INT**. Acronym of the program's International Edition: it opens in English and carries no Brazilian
data. Tariffs, costs, currency and emission factors are entered by the user.

**IPCC** (*Intergovernmental Panel on Climate Change*). Intergovernmental panel that synthesises
scientific knowledge on climate change and organises the assessment reports to which the climate
projections refer.

**IPTU verde** (green property tax). Discount on the municipal property tax granted by some Brazilian
municipalities to buildings that adopt sustainability measures, among them rainwater harvesting. The
percentage and the conditions vary with municipal legislation.

**IRR** (*taxa interna de retorno*, TIR). Internal rate of return. The discount rate that makes the
net present value zero.

**ISO 14040**. International standard that sets out the principles and framework of life cycle
assessment. An inventory conforming to ISO 14040 requires traceability of each flow and external
critical review, requirements a screening assessment does not meet.

**JSON** (*JavaScript object notation*). Structured text file format, readable by people and by
programs. It is the internal format of the `.triton` file.

**LCA** (*avaliação de ciclo de vida*, ACV). Life cycle assessment. Method that accounts for the
environmental impacts of a product over its whole existence, from the extraction of raw materials to
disposal. The program's is a **screening** one, not a full inventory conforming to ISO 14040.

**LCOW** (*levelized cost of water*). Ratio between the present value of all the life cycle costs of
the system (CAPEX, replacements, O&M, energy and chemicals) and the discounted volume of rainwater
consumed over the analysis horizon, in currency per m³. It allows the economic viability of the
system to be compared directly with the utility's tariff.

**LEED** (*leadership in energy and environmental design*). Environmental certification system for
buildings of the *U.S. Green Building Council*, the most widespread internationally. It deals with
water efficiency in the *Water Efficiency* category: in version 4, by credits WEc1 and WEc2; in
version 5, by credit WEc2, *Enhanced Water Efficiency*.

**m.c.a.** (*metro de coluna d'água*). Metre of water column, a unit of pressure equal to that
exerted by a column of water one metre high, about 9.81 kPa. It is the usual unit in building
installations; this manual writes it as «m».

**Marginal gain** (*ganho marginal*). Change in the saving potential per cubic metre added to the
tank, in %/m³ ($\Delta E_{pot} / \Delta V$). Selection criterion of the ideal volume.

**MCTI** (*Ministério da Ciência, Tecnologia e Inovação*). Brazilian Ministry of Science,
Technology and Innovation, which publishes the average emission factor of the national
interconnected grid used in the environmental assessment of the Brazil Edition.

**Motor efficiency** (*rendimento do motor*). Ratio between the mechanical power at the shaft and the
electrical power drawn from the mains. ABNT NBR 17094-2 requires it to be marked on the plate.

**NBR** (*Norma Brasileira*). Brazilian standard, published by ABNT. The most cited in this manual are
NBR 15527, on rainwater harvesting, NBR 10844, on building stormwater installations, NBR 5626, on
building cold and hot water systems, and NBR 17094-2, on induction motors.

**Triton manual suite** (*Manuais do Triton*). The program's documentation, built from the same
sources in three formats: the complete manual, eight separate volumes, each with a part of it, and
the documentation site. The volumes serve those who need only one part, to consult or send:

1. **Complete manual**: all the chapters and appendices.
   ![Cover of the Complete Manual](../figuras/capas/capa_completo.png)
2. **Volume 1 — Start here**: what the program does, how to install it and where to start depending
   on your goal.
   ![Cover of Volume 1 — Start here](../figuras/capas/capa_1-comece-aqui.png)
3. **Volume 2 — The method**: the equations, the criteria and the sources behind each number the
   program publishes.
   ![Cover of Volume 2 — The method](../figuras/capas/capa_2-metodo.png)
4. **Volume 3 — Guides**: other cities, future climate, tariffs, variable demand, batch,
   sensitivity and export.
   ![Cover of Volume 3 — Guides](../figuras/capas/capa_3-guias.png)
5. **Volume 4 — Tutorial**: a house project in Florianópolis, from the first input to the
   recommended volume.
   ![Cover of Volume 4 — Tutorial](../figuras/capas/capa_4-tutorial.png)
6. **Volume 5 — Mistakes, limitations and reliability**: the most common mistakes, the limits of the
   model and how the program is verified.
   ![Cover of Volume 5 — Reliability](../figuras/capas/capa_5-confiabilidade.png)
7. **Volume 6 — Fixes, bugs and versioning**: what changed since Netuno 4, the error messages and how
   to report a problem.
   ![Cover of Volume 6 — Versions](../figuras/capas/capa_6-versoes.png)
8. **Volume 7 — Probabilistic modulation**: the study rerun with drawn assumptions — variables,
   distributions, reading the results and the limits of the method.
   ![Cover of Volume 7 — Probabilistic modulation](../figuras/capas/capa_7-modulacao.png)
9. **Volume 8 — Appendices**: parameters, processes, emission factors, tariffs, climate database,
   formats, glossary and references.
   ![Cover of Volume 8 — Appendices](../figuras/capas/capa_8-apendices.png)

The covers shown are those of the Portuguese volumes, which are published in Portuguese only. The
complete manual exists in English too: it is this one, and the International Edition opens it from
step 9. Documentation.

**Non-potable water** (*água não potável*). Water not intended for direct human consumption, but which
meets the physical, chemical and microbiological quality standards set by specific standards (such
as Table 1 of ABNT NBR 15527:2019 and ABNT NBR 16783:2019) for the uses admitted: flushing toilets and
urinals, washing vehicles, pavements and floors, landscape irrigation, laundry and cooling towers.

**NPV** (*valor presente líquido*, VPL). Net present value.

**Overflow** (*extravasamento*, spillage). Volume that exceeds the capacity of the tank and is led
away by the overflow pipe when the tank is already full.

**Payment floor** (*piso de pagamento*). Tariff regime in which the bill **does not go** below a
value. Different from the availability charge: the floor limits from below, the availability charge
adds on top.

**PB** (*preço-base*). Base price, in R$/m³, of the CORSAN exponential formula, `PB × Cⁿ`, in which `C`
is the month's consumption and `n` the exponent of the exponential table for that consumption.

**PEAD** (*polietileno de alta densidade*). High-density polyethylene (HDPE), the material of the most
common plastic tanks on the Brazilian market.

**Pluvial demand** (*demanda pluvial*, $D_{pl}$). Part of the building's daily water demand that can be
supplied by the harvesting system ($D_{pl,t} = D_{tot,t} \times f$). It corresponds to the non-potable
points of use connected to the rainwater network.

**Potable water** (*água potável*). Water that fully meets the potability standards set by Ministry of
Health Ordinance GM/MS No. 888/2021, in Brazil, intended for drinking, food preparation and personal
hygiene.

**Potable water saving potential** (*potencial de economia de água potável*, $E_{pot}$). Fraction of
the **total** demand of the building supplied by rainwater
($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$). It is the program's central indicator, bounded
above by the suppliable fraction ($E_{pot} \le f$).

**pp**. Percentage points. Used to express the difference between two percentages: from 35% to 37% is
two percentage points, not two per cent.

**PR** (*pré-requisito*). Prerequisite: in AQUA-HQE, the level of a mandatory item, below the HQE,
HQE 2 and HQE 3 levels.

**PRCPTOT**. Total annual precipitation on wet days.

**PRFV** (*plástico reforçado com fibra de vidro*). Glass-fibre reinforced plastic, the material of
medium and large tanks. It appears in the program as «fibreglass».

**Pump efficiency** (*rendimento da bomba*). Ratio between the hydraulic power delivered to the water
and the mechanical power at the shaft. It does not include the motor.

**PVC**. Polyvinyl chloride, the material of building cold-water piping and of the first-flush
diversion columns. The dimensions of solvent-weld pipes follow ABNT NBR 5648.

**R95p**. Sum of the precipitation of the days above the 95th percentile of the wet days.

**Rainwater** (*água de chuva*). Atmospheric precipitation collected directly on impermeable roof
surfaces (roofs and waterproofed slabs), before it reaches the ground or public drains. It is the
official technical and normative term of ABNT NBR 15527:2019.

**Rainwater harvesting** (*aproveitamento de água de chuva*, AAC). Use of the water falling on roofs
for non-potable uses in buildings, regulated in Brazil by ABNT NBR 15527:2019. «Harvesting» is
preferred to «reuse», since rainwater collected on the roof is a primary resource and not an
effluent of earlier human use.

**Rainwater harvesting system** (*sistema de aproveitamento de água pluvial*, SAAP). Integrated set of
building components — catchment area, pipes, first flush, treatment plant (ETAP), lower cistern,
upper tank, pump set or pressure pump and an independent distribution network — designed to
collect, treat, store and supply non-potable water in accordance with ABNT NBR 15527 and ABNT NBR
5626.

**Representative rainfall series length** (*comprimento representativo de série de precipitação*,
$N_{rep}$). Shortest continuous period, in years of daily rainfall data, needed to stabilise the
sizing and performance of the system statistically (reproducing the ideal volume and the saving
potential of the full series with confidence $\ge 90\%$), according to the method of Geraldi and
Ghisi (2017, 2018, 2019). The length needed is not a fixed geographical constant: it grows with the
suppliable fraction and with the demand level of the building.

**Retroactive allowance** (*franquia retroativa*). Tariff regime in which consumption up to the
allowance pays a fixed value and consumption above it is billed in full from 0 m³.

**Runoff coefficient** (*coeficiente de escoamento*). Fraction of the rain that actually reaches the
tank, after losses to absorption, evaporation and initial wetting of the roof.

**RX1day**, **RX5day**. Largest precipitation in one and in five consecutive days, in the year.

**SB** (*serviço básico*). Basic service charge: the fixed monthly part of the CORSAN water bill, added
to the result of the exponential formula.

**SDII** (*simple daily intensity index*). Mean precipitation of the wet days.

**SI** (*seasonality index*). Walsh and Lawler seasonality index. Zero when rain is uniform over the
year.

**SMAA** (*stochastic multicriteria acceptability analysis*). Method that draws weights and returns
the probability of each alternative winning.

**SNIS** (*Sistema Nacional de Informações sobre Saneamento*). Brazil's national sanitation information
system, the official database of the sector's indicators, kept by the federal government. It is the
origin of the sanitation energy consumption indicators used in the environmental assessment.

**SSP** (*shared socioeconomic pathways*). Coherent hypotheses of global development and the
corresponding emissions. They are combined with the climate models to produce projections.

**Stochastic demand** (*demanda estocástica*). Modelling daily water consumption as a probabilistic
variable that varies from day to day and between realisations (Silva and Ghisi, 2016), allowing the
uncertainty range of the sizing and of the performance indicators to be assessed under real
variability of use.

**Stormwater** (*água pluvial*, pluvial water). Rainwater after urban surface runoff, or when led by
building drainage and storage pipes and systems (ABNT NBR 10844). In Triton's Portuguese text, the
term applies preferably to building infrastructure and engineering components: harvesting system,
rainwater network, pluvial demand, rainwater consumption and overflow.

**Suppliable fraction** (*fração atendível por água pluvial*, non-potable demand share, $f$).
Percentage of the building's total water demand ($D_{tot}$) that can be supplied by rainwater
($f = D_{pl} / D_{tot}$). It is the **insurmountable asymptotic ceiling** of the potable water saving
potential ($E_{pot} \le f$): even with infinite storage and unlimited rain, the potable saving never
exceeds the suppliable fraction, because the rest ($1 - f$) is reserved for potable uses. It is
distinct from volumetric reliability ($C_v = E_{pot} / f$), which assesses the supply of the
rainwater part.

**Tariff flag** (*bandeira tarifária*). Surcharge or discount on the Brazilian electricity tariff,
according to generation conditions. Green, yellow, red 1, red 2, and the white mode.

**TFDI** (*tarifa fixa de disponibilidade da infraestrutura*). Fixed infrastructure availability
tariff, the name some utilities give to the part of the bill charged regardless of consumption. See
*Availability charge*.

**Time reliability** (*confiabilidade temporal*, $C_t$). Percentage of days on which the system fully
($V_{con,t} = D_{pl,t}$), partly or not at all supplied the rainwater demand.

**TMA** (*taxa mínima de atratividade*). Minimum attractive rate of return. The discount rate adopted.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*). Multi-criteria
ranking method of Hwang and Yoon.

**UV**. Ultraviolet radiation, used in water disinfection by inactivating micro-organisms. It acts
only at the moment of passage through the reactor and leaves no residual, unlike chlorination.

**VIKOR**. Multi-criteria decision method proposed by Opricovic, which seeks a compromise solution
between conflicting criteria. See also *SMAA*.

**Volumetric reliability** (*confiabilidade volumétrica*, $C_v$). Fraction of the **rainwater** demand
the system supplied ($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Not to be confused with the
saving potential, whose denominator is the total demand of the building.

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
graphical interface and Triton's documentation. The conventions below detail the distinction
between related terms that are often confused, first in Portuguese, the language of the program's
reference text, and then in English.

### 1. Rainwater, stormwater and the colloquial form

<!-- tabela: Terminology for rainwater and stormwater, in Portuguese and English -->
| Term | Definition and context of use | Status in Triton | Reference |
| :--- | :--- | :--- | :--- |
| *água de chuva* (rainwater) | Precipitation collected directly on the roof (roof or waterproofed slab), before it reaches the ground or drains. It refers to the **water source** and the environmental resource. | **Canonical and preferred** for the resource collected. In English, «rainwater». | ABNT NBR 15527:2019, title and item 3.1. |
| *água pluvial* (stormwater, pluvial water) | Rainwater after urban surface runoff, or when led by building drainage and storage pipes and systems. It applies to the **physical infrastructure** and the engineering components. | **Canonical and preferred** for systems, networks and the balance. In English, «rainwater» is used for these too («rainwater network», «rainwater demand»), and «stormwater» only for drainage. | ABNT NBR 10844:1989; ABNT NBR 5626:2020. |
| *água da chuva* | Colloquial, informal expression. | **Discouraged**. Not to be used in publications, normative texts, Triton reports or code. | Practice of technical and scientific writing. |

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
- Use **«catchment area»** for the horizontal plane of the roof (NBR 15527, EN 16941-1) and keep
  **«contributing area»** exclusively for the hydraulic sizing of gutters under wind (NBR 10844).
- Use **«first flush»** for the initial depth diverted (a minimum of 2 mm according to NBR 15527), not
  «first-flush threshold».
- Use **«suppliable fraction»** or «non-potable demand share» (not «relative demand» or «saving
  fraction») to express the share of non-potable uses in total consumption.
- Use **«representative series length»** for the minimum length in years needed for the statistical
  stabilisation of the simulation (Geraldi and Ghisi method).
- Use **«LCOW»** or **«levelized cost of water»** for the unit cost metric over the life cycle
  discounted at the minimum attractive rate of return.
