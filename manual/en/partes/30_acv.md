# Life cycle assessment

> This section presents the seven stages of the inventory and the boundary adopted, and declares
> what is measured and what is a screening assumption.

Life cycle assessment is the method that accounts for the environmental impacts of a product over
its whole existence, from the extraction of raw materials to final disposal. Applied to a
rainwater harvesting system, it answers whether the carbon emitted to manufacture the tank, the
piping and the pump set is offset by the carbon no longer emitted by not consuming water from the
utility.

==Netuno's assessment is a screening one, not a full inventory.== The distinction matters and the
standard recognises it: a screening assessment ranks alternatives and identifies what dominates
the result, whereas an inventory conforming to ISO 14040 documents each elementary flow with
traceable provenance and undergoes external critical review. The first serves to decide between
polyethylene and concrete; the second, to declare an environmental performance publicly.

---

## The four phases of the standard, and where the program stands

The ISO 14040 and ISO 14044 standards, published in Brazil as ABNT NBR ISO 14040 and ABNT NBR ISO
14044, organise every life cycle assessment into four phases that feed back into one another. It is
worth going through them, because each one corresponds to a decision the program has already made
for you, and that a published study needs to declare.

**1. Goal and scope.** Defines what the study is for, the **functional unit** and the system
boundary. The functional unit is the quantity of service being compared, and it is what makes
different alternatives comparable. In the program, the implicit unit is the **harvesting system of
a project over the adopted service life**, and the comparison is made against the supply of the
same volume of water by the utility. Anyone wanting to compare with the literature can convert it
to the most used unit, the cubic metre of water delivered, by dividing the balance by the volume of
the service life, as Equation {{eq:emissao_especifica}} does.

**2. Inventory.** Surveys the input and output flows of each process: masses of material, energy,
consumables. In the program, the inventory is the masses of the components, the pumping energy,
the mass of chlorine product and the volume of water replaced.

**3. Impact assessment.** Converts the flows into category indicators by characterisation factors.
The program assesses **one** category, climate change, in kilograms of carbon dioxide equivalent,
with the emission factors of appendix {{n:C}}.

**4. Interpretation.** Identifies what dominates the result, tests the sensitivity to the
assumptions and draws conclusions within the limits of the scope. That is what sections {{n:11}}
and {{n:20}} do with the tank material and with the other assumptions.

---

## The building modules

For buildings, the European standard EN 15978 subdivides the life cycle into modules, and the same
nomenclature is used in environmental product declarations according to EN 15804. Declaring which
modules the study covers is the shortest and most precise way of declaring the boundary, and it is
what a reviewer expects to find.

<!-- tabela: EN 15978 life cycle modules and what the program's assessment covers in each one -->
| Module | Stage | Covered by the program |
| :--- | :--- | :--- |
| A1 to A3 | product: raw material, transport to the factory, manufacture | yes, for tanks, piping, pump sets, first flush and all the parts, fittings and cables of the 3D layout |
| A4 and A5 | construction: transport to the site and installation | no; the excavation for the buried cistern is left out |
| B1 to B5 | use, maintenance, repair, replacement and refurbishment | no; pump and component replacements do not enter |
| B6 | operational energy | yes, the pumping energy |
| B7 | operational water | yes, as the credit for the potable water avoided and the treatment consumables |
| C1 to C4 | end of life: demolition, transport, processing and disposal | no |
| D | benefits and loads beyond the boundary, such as recycling | no |

The reading of the table is that the program does a **cradle-to-gate assessment, plus
operation**. It is the most common boundary in studies of rainwater harvesting in buildings, but
not the only one, and comparing the program's balance with that of a study that includes end of
life or replacements requires adjusting the boundaries before comparing the numbers.

---

## The seven stages

The inventory is organised into seven stages, grouped by the nature of the emission
({{fig:fig34_inventario}}). The carbon balance is the sum of the emissions of the first six minus
the credit of the seventh, the only term with a negative sign, and it is this credit that decides
whether the system offsets the carbon embodied in its construction.



![The seven stages of the life cycle inventory](../figuras/fig34_inventario.png)

*Figure 99 — The seven stages of the inventory, grouped by the nature of the emission. The first four are embodied and occur only once; the fifth and sixth are operational and repeat every year; the seventh is the credit, and it is the only one that enters with a negative sign.*


The first four stages account for the **embodied carbon**, that is, the emissions that occurred in
manufacturing the components, before the system goes into operation; when the physical first flush
is sized, the first-flush chamber and the leaf separator are added to them. The next two account
for the operational emissions, which repeat in each year of use. And the seventh is the
**credit**: the emission the utility no longer generated because that water did not have to be
abstracted, treated and distributed.

Volume zero without rainwater consumption represents the no-system scenario and, by construction,
receives no fixed impact of tank, piping or pump set — it is the reference against which all the
other alternatives are compared.

---

## Embodied carbon

```equacao:emissao_componente
E_comp = m_comp × FE_mat
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_comp` | embodied emission of the component | kg CO₂e |
| `m_comp` | mass of the component | kg |
| `FE_mat` | emission factor of the material, cradle to gate | kg CO₂e/kg |

The mass of each component follows from its sizing. For the tank, it is obtained from the useful
volume multiplied by the characteristic mass density of the material, which varies by more than an
order of magnitude between polyethylene and reinforced concrete — and a good part of the
environmental result of the project follows from that variation.

<!-- tabela: Mass per useful cubic metre of each tank material -->
| Material | Mass per useful m³ | What this means in 5 m³ |
| :--- | ---: | ---: |
| polyethylene | 22 kg/m³ | 110 kg |
| fibreglass | 15 kg/m³ | 75 kg |
| stainless steel | 38 kg/m³ | 190 kg |
| reinforced concrete | 1,200 kg/m³ | 6,000 kg |

> **Mass is carbon.** Reinforced concrete is by far the most massive material on the list, and
> that is why it dominates the inventory when chosen. Section {{n:11}} shows the consequence: with
> concrete, the tutorial system does not pay off its carbon debt within the service life.

### The inventory of the tutorial project, item by item

The table below breaks down the carbon of the final tutorial project: a 4,000 L polyethylene
cistern, a 1,000 L upper tank, two pump sets, the standard piping and the first flush.

<!-- inclui: _tabelas/cap30_inventario.md -->

Three readings matter. The first is that, even in polyethylene, the cistern accounts for almost
half of the embodied carbon, and the tanks together for more than half. The second is that the
piping and the pump sets, which are usually forgotten in simplified calculations, add up to almost
two fifths of the total: a study that counted only the tank would underestimate the embodied carbon
by almost half. The third is in the annual column: the credit of the water avoided is about 23
times larger than the annual emissions of pumping and chlorination together, and that is why, with
the right material, the manufacturing debt pays off.

---

## Operation

**Pumping:**

```equacao:emissao_energia
E_ener = C_ano × FE_rede
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_ener` | annual emission of the pumping energy | kg CO₂e/year |
| `C_ano` | annual energy consumption of the pump set | kWh/year |
| `FE_rede` | emission factor of the electricity grid, by region and year | kg CO₂e/kWh |

The annual energy consumption comes from the calculation presented in section {{n:28}}, according
to the supply arrangement declared, and the grid emission factor comes from one of the program's
databases. The default database, at 0.085 kg CO₂e/kWh, is a declared choice among the values
published for the Brazilian grid: it is close to the SIDAC and CaDI values, and above the annual
MCTI series, which covers only the carbon dioxide of generation. The alternative databases include
the values of Vaz, Scolaro and Ghisi (2025) for the 2022 grid, 0.104 kg CO₂e/kWh for the fossil
indicator and 0.151 for the total indicator, useful for the sensitivity analysis. In the
International Edition the factor is typed in.

Energy is small in the program, but it is worth knowing that it tends to be larger in practice.
Vieira et al. (2014), in a review of the energy intensity of rainwater harvesting systems, found a
median of 0.20 kWh/m³ in theoretical studies and of 1.40 kWh/m³ in empirical studies, and
attributed part of the difference to start-ups, standby consumption and real efficiencies worse
than catalogue ones. The tutorial, at 0.13 kWh/m³, is in the range of theoretical studies. Ghimire
et al. (2014, 2017) reached a converging conclusion by life cycle assessment: in the systems they
analysed, the pump set and the pumping energy were the components that weighed most in most of the
impact categories, and the pumpless version outperformed the public supply in almost all of them.

> **When energy decides.** With the Brazilian grid factor, multiplying the tutorial's energy by
> ten, taking it close to the empirical median of Vieira et al., would add about 6 kg CO₂e a year
> to the emissions and reduce the annual balance from 20.1 to about 14.1 kg CO₂e. The annual
> balance would remain positive, but the carbon payback would go from 16.3 to about 23 years,
> beyond the twenty years of service life adopted: the system would end its life owing carbon. On
> grids more fossil-based than the Brazilian one, the effect is even larger.

**Treatment:** the treatment line **replaces** the chlorination term instead of adding to it. It is
the same rule as in section {{n:27}}, and it exists so that the hypochlorite is not counted twice.

---

## What the boundary includes, and what it leaves out

Before discussing any emission factor, it is worth fixing the scope. The program's assessment is a
**screening** one: it serves to rank alternatives against each other, not to replace a life cycle
inventory conforming to ISO 14040. What enters the calculation and what is left out is declared,
because an environmental balance without a declared boundary can be neither checked nor contested
({{fig:fig00h_fronteira}}). The most limiting exclusion is that of the impact categories beyond
global warming: a system with good carbon performance can perform unfavourably in another category,
and the assessment does not record it.

![What the environmental assessment includes and what it leaves out](../figuras/fig00h_fronteira.png)

*Figure 99 — Boundary of the program's environmental assessment: (a) processes included — embodied carbon of the tanks, the piping and the pump set, operational emissions of pumping and of treatment consumables, and the credit for the potable water avoided; (b) processes excluded — civil works, maintenance and replacement, end of life and impact categories beyond global warming.*

---

## The boundary: water delivered, not produced

The emission factor of potable water is per cubic metre **delivered to the building**, not per
cubic metre produced at the treatment works.

The difference is the distribution losses, which in Brazil range from **33.9% in the Southeast to
46.9% in the North**. Producing one cubic metre delivers between 0.53 and 0.66.

A published factor at the outlet of the works, applied to the volume delivered, **underestimates
the avoided emission by up to a third**. The program makes the conversion and declares the
macro-region adopted.

Appendix {{n:C}} lists the 19 water production routes available, with the provenance and boundary
of each one.

---

## The indicators

**Net annual balance:**

```equacao:saldo_liquido
E_liq = E_evit − E_ener − E_trat
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_liq` | net annual emission balance | kg CO₂e/year |
| `E_evit` | emission avoided by the utility water no longer consumed | kg CO₂e/year |
| `E_ener` | annual emission of the pumping energy | kg CO₂e/year |
| `E_trat` | annual emission of the treatment consumables | kg CO₂e/year |

**Carbon payback:**

```equacao:payback_carbono
PB_amb = E_inc ÷ E_liq
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `PB_amb` | environmental payback time of the system | year |
| `E_inc` | carbon embodied in the manufacture of the components | kg CO₂e |
| `E_liq` | net annual emission balance, from Equation {{eq:saldo_liquido}} | kg CO₂e/year |

When the net annual balance is not positive — a real situation, not a hypothetical one, in systems
with a large concrete tank — there is no environmental payback, because the debt is never paid off.
The program returns 999 years in that case, instead of infinity, so that the value can still be
ranked in comparisons; the meaning, however, is that the system ends its service life owing
carbon.

**Balance at the end of life:**

```equacao:saldo_vida
S_vida = ( E_liq × n_anos ) − E_inc
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `S_vida` | carbon balance at the end of the adopted service life | kg CO₂e |
| `E_liq` | net annual emission balance, from Equation {{eq:saldo_liquido}} | kg CO₂e/year |
| `n_anos` | service life adopted for the system | year |
| `E_inc` | carbon embodied in the manufacture of the components | kg CO₂e |

Negative means the system **emitted more than it avoided** over the adopted life. It is not a
theoretical hypothesis: it happens with a concrete cistern and a twenty-year service life, as
section {{n:11}} shows.

**Specific avoided emission:**

```equacao:emissao_especifica
E_esp = S_vida ÷ V_vida
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `E_esp` | specific emission of the system over the service life | g CO₂e/L |
| `S_vida` | carbon balance at the end of the service life, from Equation {{eq:saldo_vida}} | kg CO₂e |
| `V_vida` | total volume of rainwater delivered over the service life | m³ |

---

## What carries a screening label

Not every factor of the inventory has a primary source. The program marks those that do not, and
the report shows the mark.

The masses per useful cubic metre of polyethylene, concrete and stainless steel, which are still
geometric scenarios, carry the label, as does any factor typed in without a source. The default
emission factors have declared provenance; the last to receive it was that of **hypochlorite**,
which now comes from Ecoinvent 3.8: as the database has no calcium hypochlorite, the program uses
the sodium one on an active-chlorine basis, 2.65 kg CO₂e per kg, which gives 1.72 kg CO₂e per kg of
65% tablet. The manufacturing emission of the pump set, which until the September 2026 revision was
an arithmetic extrapolation in four of the six power ratings, now combines the catalogue mass with
the intensity of an environmental product declaration; it is an order-of-magnitude approximation,
and appendix {{n:C}} declares the caveat.

> **In a published study, declare which factors carry a screening label.** An inventory that
> presents all factors with the same degree of confidence hides where the weakness lies.

---

## What the literature shows

Life cycle assessment of rainwater harvesting systems is an active field without a single method.
Vaz et al. (2023), in an integrative review conducted under the PRISMA protocol, concluded that
residential buildings are the most studied case, but that there is no consensus on a uniform
analytical framework; that several benefits of rainwater, such as runoff reduction, rarely enter
the assessment; and that integration with life cycle costing is a promising way of showing the
benefits more directly.

For the Brazilian case, Marinoski and Ghisi (2018) assessed a social housing unit in Florianópolis
and compared fibreglass, high-density polyethylene and reinforced concrete tanks. The fibreglass
ones were the most favourable from the environmental point of view, and the concrete ones, from the
point of view of investment. The result converges with that of section {{n:11}} in the essentials:
the tank material weighs on the carbon, and the environmental and economic dimensions can point in
different directions.

Ghimire et al. (2017), comparing a commercial system with the municipal supply in eleven impact
categories, showed something else this assessment does not reach: the rainwater system outperformed
the municipal one in ten of the eleven categories, but not in all, and the result of each category
depended on the energy intensity of pumping. It is the strongest argument for declaring that the
program's assessment covers a single category.

---

## What the assessment does not cover

- **end of life.** There is no credit for recycling nor burden for disposal. The boundary is
  cradle to gate plus operation.
- **excavation and civil works.** The earthworks of the buried cistern do not enter.
- **maintenance.** Component replacements over the service life do not enter.
- **impacts beyond carbon.** There is no eutrophication, acidification, land use or toxicity. It is
  an assessment of **one** impact category.

The last point is the most important. A system with good carbon performance can perform poorly in
another category, and this assessment would not see it.
