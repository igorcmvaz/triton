# Exporting to CAD, BIM and spreadsheets

> **Question this guide answers:** how do I take the result to the construction design and
> to my own analysis?

---

## What each format carries

<!-- tabela: Export formats and the purpose of each one -->
| Format | Extension | What it carries | What for |
| :--- | :--- | :--- | :--- |
| report | HTML, PDF | complete result and assumptions | delivery |
| spreadsheet | XLSX | daily series and sweep | re-analysis |
| audit | XLSX | every field of the assumptions, the tariff, the treatment, the LCA, the economics and the arrangement | checking |
| drawing | DXF | sized hydraulic diagram | construction design |
| BIM manifest | JSON | components with type, position, level and parameters | import into Revit |
| project | TRITON | all the steps and the rainfall series | reopening and auditing |

---

## The project file

The `.triton` format is the only one that keeps the whole study: the nine steps, the
multi-criteria weights, the LCA routes and the **daily rainfall series**, embedded in the
file itself. A `.triton` file reopens on another computer without the source CSV and
reproduces the same number; it is with it that the cases of appendix {{n:J}} are
distributed. The legacy CSV format of the earlier tool is still available in the export, marked as legacy,
because it does not keep the steps added since then.

---

## Spreadsheet

Exporting to a spreadsheet is the way for anyone who intends to do their own analysis of the
results, whether to build a chart the program does not offer, or to combine Triton's numbers
with data from another source. Two data sets are available, and they answer different
questions.

The **daily series** has one row per simulated day, with the recorded rain, the effective rain
after the first flush, the collected volume, the day's demand, the rainwater consumption, the
mains consumption, the overflow, the volume stored in both tanks, the volume pumped and the
supply class. It is the basis of any chart or statistic the program does not offer ready-made,
and it is what is used when the intended analysis differs from the one the program does.

The **sweep** has one row per simulated volume, with all the indicators calculated for each.
It is the basis of the diminishing-returns curve presented in section {{n:7}}, and the right
format for anyone who wants to redraw it with another presentation.

Step **10. Export** builds the spreadsheet from six sets, ticked one by one: the executive
summary with the project metadata, the daily water balance, the sweep curve with reliability,
the year-by-year cash flow, the life cycle inventory and the multi-criteria decision matrix.
Three choices complete the export:

<!-- tabela: Spreadsheet export options and when to use each one -->
| Option | Choices | When to use |
| :--- | :--- | :--- |
| format | XLSX, CSV or JSON | XLSX to open in Excel; CSV for R, Python or another program; JSON for integration |
| CSV separator | semicolon or comma | semicolon in Excel set to a decimal-comma locale; comma in R and most international tools |
| time filter | first typical year or full series | the year to illustrate; the full series for any statistic |
| economic horizon | 10, 20, 25 or 30 years | 20 years, a common design life for plumbing components, unless the study justifies another |

### Exporting everything, for audit

The **Export EVERYTHING (audit)** button, next to the spreadsheet export, saves a single Excel
file with the six sheets above and, besides them, sheets nobody chooses: they go through
**every** field of what the program used. They are the project assumptions, one row per
parameter, with the value and the description taken from the code itself; the tariff applied,
with the meaning of each block code, the regime, the sewage mode and the bill for
consumptions from 0 to 50 m³; the treatment line sized in the quality step, with the stages,
the doses and the carbon the LCA adds; the life cycle inventory item by item; the results of
the simulation, the economics and the multi-criteria decision; and the 3D arrangement, with
each part, each run and the take-off by diameter. The «0_Leia_me» (read-me) sheet says what is
in each one.

It is the file for anyone who needs to check a calculation from start to finish, or to answer
an assessor who asks what went into the carbon or the saving. A new parameter in the program
appears in it without anyone having to remember to add it.

> **A warning about size.** Thirty years of daily series are 10,950 rows per simulation. A
> sweep of twelve volumes with a detailed series generates a hundred and thirty thousand rows.
> Export the detailed series only for the volume of interest.

---

## Drawing in DXF

The program generates the hydraulic diagram of the sized system: cistern, filter, first
flush, pump when there is one, upper tank, and the piping with the diameters adopted.

What the program produces is a **diagram**, not a construction design. It represents the
components of the system and the logical connections between them, with the diameters
adopted, and serves as a basis for the designer to draw the installation in plan, with the
levels, the routing and the real clashes of the building. ==A diagram does not replace a
plumbing design, and delivering it as one would be an error of professional responsibility.==

Nor does the diagram carry, and the construction design must add, the installation
requirements that the applicable national rules set for non-potable water:

- rainwater piping identified by colour and by an inscription such as «NON-POTABLE WATER», at
  regular intervals on exposed pipes;
- a distribution system independent of the potable one, without cross-connection, with an air gap
  on the backup supply from the mains;
- restricted-use points, such as the garden tap, with a non-potable sign;
- separate potable and non-potable tanks, with a clear separation between them;
- pumping according to the rules for building water supply, which usually call for a standby
  pump.

The colours, the wording and the distances differ from one country to the next; check the rule of
the place of the building and write it on the drawing.

What the program does **not** size:

- routing and slope of the piping;
- real head loss of the installation;
- hydraulic arrangement of the first-flush device, of which the program calculates only the volume, `A × d_f`, and the cost;
- overflow and connection to the drainage;
- foundation and waterproofing of the cistern.

---

## Block library and BIM manifest

In step **10. Export**, the *Block Library for Plans + BIM JSON* mode saves the DXF blocks of
the components at 1:1 scale, in millimetres, and, next to them, the `*_triton-bim.json` file.
The program does not export IFC. The JSON manifest is the contract between the sizing and the
model: each instance declares the component type, the level, the local position in
millimetres, the rotation and the sized parameters, such as capacity and diameter, and the
structure is validated before saving.

The integration with Autodesk Revit is done by an importer distributed with the program, run
in the CPython 3 engine of pyRevit, with a document open in Revit 2022 or later, and it inserts
the instances of the manifest using the families indicated in `family_mapping.json`, which
associates each program type — cistern, upper tank, filter, first flush, pump set, valves,
non-return valve, air gap, overflow, non-potable point of use, calmed inlet, floating suction,
level switch, solenoid valve, water meter, foot valve with strainer, vent and control panel —
with a family and a type of the office.

With no saved organisation, the program pre-fills the usual arrangement of these
installations, from the study: roof collection, filter and first flush; cistern with a calmed
inlet, abstraction by floating suction with a foot valve and strainer, a level switch against
dry running, a screened vent and an overflow with a trapped outlet and anti-backflow valve to
the storm drain; isolation valves on both sides of the pump set, a non-return valve on the
rising main and a control panel; an upper tank with a level switch, screened vent, overflow
with visible discharge, cleaning outlet with a valve and distribution with a valve to an
identified point of use; and the potable backup supply — water meter, valve and solenoid
valve — which only opens when rainwater runs out and discharges into the upper tank through an
air gap, as good practice requires. The control panel decides: with the upper tank at the
start level and water in the cistern, it starts the pump; with the cistern at the minimum, it
blocks the pump and opens the solenoid, which fills the tank only up to the backup float,
lower, so as to leave room for the next rain. Pump and solenoid never run together. In the
volumetry, the control cables — from the level switches to the panel and from it to the pump
and the solenoid — appear dashed, and the complete logic is on the panel's data sheet. The
arrangement is a starting point: positions, routes and parts belong to the designer.

The arrangement follows two choices of the project:

- **Number of pump sets.** With two, the standby is drawn in parallel with the duty pump, with
  its own isolation valve on the suction, non-return valve and isolation valve on the delivery.
  It connects to the duty pump's lines by tees.
- **Supply arrangement.** It changes what exists in the installation:
  - **Pumping to an upper tank:** it is the arrangement described above.
  - **Direct pressurisation:** there is no upper tank. The pressure pump takes the water from
    the cistern straight to the point of use. The potable backup supply discharges into the
    cistern itself, also through an air gap, and only up to a backup float installed in it.
  - **Gravity:** there is no pump. The cistern sits on a base, above the point of use, and the
    water leaves by a low side outlet with a valve. The potable backup supply discharges into
    the cistern, as with pressurisation.

While the runs have not been organised, the arrangement is rebuilt at each change of the
volume, the supply or the number of pumps.

With these data the program also builds the sheet of the 3D diagram, not to scale and on an
A3 landscape sheet. Only the levels that organise the installation — cistern, upper tank,
pump set, filter and first flush — get a level plane; the small parts appear on the drawing by
their code, and the type and level of each one are in the «Parts and accessories» table, next
to the assembly sequence and the take-off by diameter.

The importer does not create families or replace components by approximation: an instance
without a family or without a corresponding level is listed as pending at the end of the
import. The coordinates are local, and the tie to the project base point and north is done in
Revit, by the designer. The manifest serves coordination and quantity take-off, and does not
replace the modelling of the plumbing installation.

### From the arrangement to the CAPEX and the LCA

The same arrangement feeds the cost and the carbon. The program takes off, part by part:

- the metres of pipe per diameter;
- the bends, one per change of direction of the route;
- the fittings, one at each end of a route connected to a part;
- each part of the manifest, by type;
- the metres of control cable.

Each item has a mass and, in an edition that carries a price list, a price that goes to the
CAPEX: pipes and fittings under *Piping*, parts and cables under *Accessories*. **In the
International Edition the layout sets no prices**: piping and accessories are the values you type
in the economic step (section {{n:10}}). The mass, times the material factor, goes to
the LCA in stage A1–A3. Cistern, upper tank and pump set already have their own line in both
analyses and are not counted again. The filter and the first flush enter the CAPEX through the
treatment line, when it is active, and the LCA through the first-flush subsystem, when it is
active.

An automatic test checks that no part, no metre of pipe, no bend, no tee and no cable of the
arrangement is left without cost or without carbon. The test covers the three supply
arrangements, with one and with two pump sets. The `Auditoria_Quantitativo` sheet of *Export
everything* lists each item with its destination in the CAPEX and the LCA, and closes the sum
against the values the analyses used. The same sheet also checks whether the arrangement is
consistent with the project: an arrangement organised by hand can fall behind when the project
changes the supply or the number of pumps, and the divergence shows up there.

The masses and the reference prices of the parts are a scenario, not a quotation or a
measurement. They are in `costs_database.json`, under the `pecas_do_arranjo` key. The reference
prices of the cost database are not applied in the International Edition: the costs, including
those of piping and accessories, are typed in the economic step, in the currency of the project,
and the manual's own cases use round figures stated as illustrative, not market prices.

---

## Reports

The three of section {{n:13}}: executive, environmental with ESG, and research. In HTML for
consultation and in PDF for delivery.

> The program has two PDF generators and uses the most complete one the computer allows. When
> it falls back to the alternative, the document comes out simpler, with the same content and
> the same numbers.

---

## A filing tip

When closing a study, keep together, in the same folder:

1. the `.triton` file;
2. the **rainfall series** used, or its exact identification in the database;
3. the research report in PDF;
4. the sweep spreadsheet;
5. if there was a batch, the **script** with the commands;
6. a text file with the **program version**.

Six items that make the study reproducible five years from now. Without them, the PDF report
is just a claim.
