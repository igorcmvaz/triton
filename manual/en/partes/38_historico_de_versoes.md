# Version history and what changed

This section records what changed between versions of the program and, above all, **which changes
alter results already published**. The distinction matters more than it seems: a fix to the
interface affects no earlier study, whereas a fix to a calculation can shift every number of a
paper already submitted. Anyone who has published with Netuno needs to know into which category
each change falls, and that is why the history below separates the two explicitly.

==The rule guiding this whole section is simple: a calculation fix obliges you to declare the
version used; an interface fix does not.==

---

## The version you are using

The version number appears in the sidebar, in the footer and in the **About Netuno** menu. It is
also saved inside each project file and printed in each report, so that an old study always
carries with it the identification of the program that produced it. The redundancy is deliberate:
reports circulate separately from files, and the question «which version was this done with?»
usually comes up months later, when nobody remembers.

The numbering scheme follows the usual software engineering convention. The first number indicates
the generation of the program, and changing it means a reformulation of the conceptual model; the
second indicates a set of new features; and the third indicates fixes and adjustments that do not
change the architecture. The move from Netuno 4 to Netuno 5, dealt with in section {{n:35}}, is the
only case of a change in the first number in the history of the program.

Version 5.0.0 is the first public release of Netuno 5. The numbers before it were development ones,
and never circulated; no study was done with them.

---

## How this history is kept

From now on, each version released gets an entry of its own in this section, with the release date
and what changed, always split into two lists: ==what alters the results of studies already done and
what does not.== The most recent entry comes first.

Each entry follows the same model, so that two versions can be compared without rereading: a
one-sentence summary, the new features, the fixes that alter results, those that do not, and what
changed in the documentation. Sections with no content in that version simply do not appear.

The same list is distributed with the code, in the `CHANGELOG.md` file at the root of the
repository, and feeds the versions page of the documentation site. It is not written three times:
all three come from this section, and an automatic check refuses the build if they diverge. Those
following the program through the repository, the site or the manual read the same record. The
`CHANGELOG.md` is in Portuguese; this section is its translation.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Version 5.0.0 — 29 September 2026

> **In one sentence.** First public release of Netuno 5: the simulation engine rewritten in Python
> and separated from the interface, with life cycle assessment, treatment line, multi-criteria
> decision, 3D piping layout and the documentation in three formats.

The version was the result of a systematic review of the program, carried out with a specific aim:
to find values that were calculated correctly in one module and discarded before reaching the next.
This class of defect is particularly dangerous because it produces no visible error — the program
responds, the number looks plausible, and only the comparison between two points of the program
itself reveals the inconsistency. The review went along five axes of propagation: from module to
module, from the screen to the calculation core, between the interface and automation, between
duplicated definitions of the same constant, and over time, that is, through saving and reopening a
project.

### New features

The program was rewritten in Python, with the simulation engine separated from the interface, and
gained what Netuno 4 did not have: life cycle assessment of carbon, a sized treatment line,
multi-criteria decision with stochastic acceptability analysis, a tariff database of 652
municipalities, an interface in four languages and export to CAD, BIM and spreadsheet. Section
{{n:35}} compares the two programs number by number, and section {{n:34}} describes the
verification suite that supports the comparison.

The demand now has two declared parts: the non-potable fraction of indoor consumption and the
outdoor demand in litres per day, suspended on rainy days. The total suppliable fraction is derived
from the two and appears in a field that cannot be edited. Section {{n:5}} describes the rule. A
layer of tests opens each distributed project at both ends of the program, the interface and the
command line, and requires them to agree, volume by volume, on the potential, the NPV, the payback,
the carbon and the five optima.

The piping is now organised by the designer, run by run and in assembly order, from the connection
points of the components (top, bottom and sides of the tank). The program checks whether each run
reaches the declared destination, rejects pipes occupying the same space and generates, with the
same data, the 3D plan in DXF, the 3D schematic with the real dimensions, the rotatable volumetric
view and the glTF and HTML files for sharing, as well as the BIM manifest read by Revit.

The Brazil Edition (BRL) and the International Edition (INT) come from the same code. The Brazil
Edition carries the audited Brazilian data. The International Edition is the neutral core: it opens
in English, with tariffs, costs, currency and emission factors entered by the user. The differences
are in section {{n:2}}.

### Fixes that alter results

The changes gathered in this table alter numbers relative to what the program calculated before
each fix. As 5.0.0 is the first public release, no study depends on them; the table is kept because
it describes what the program now calculates differently, and because it is the format the
following versions will use.

<!-- tabela: Fixes that alter the results of studies done with an earlier version -->
| What was fixed | Effect on the result |
| :--- | :--- |
| the rated power of the pump set was treated as electrical input power, when it is shaft power | specific pumping consumption went from 0.0654 to 0.1080 kWh/m³ |
| the start-up energy divided the rated power by the pump efficiency, although there is no flow at start-up | start-up share corrected, about 14% of the annual energy |
| the irrigation demand supplied by the mains did not appear in the summary | unmet demand is no longer underestimated by 10.85 L/day in the reference case |
| four tax fields were zeroed at each confirmation of the economic dialog | the water and energy bills now include the declared taxes |
| chlorination, ultraviolet and ozone were treated as mutually exclusive | the treatment line now combines stages, according to item 4.6.5 of ABNT NBR 15527:2019 |
| the economic analysis only charged energy with an upper tank, and the environmental assessment charged pumping in any arrangement and lost chlorination without an upper tank | the supply arrangement is now declared in step 4, and cost and carbon read the same energy; projects without an upper tank no longer have implicit pumping in the carbon and now have chlorination |
| the hypochlorite emission factor was 1.85 kg CO₂e/kg, with no declared process | it became 1.72 kg CO₂e/kg, from Ecoinvent 3.8 on an active-chlorine basis |
| the interface did not restore the indoor fraction or the outdoor demand when opening a project, and always simulated with 35% and 0 L/day | the interface simulates with the project's fraction; the tutorial, which declares 28%, gave a 32.85% potential at 4,000 L on the screen and now gives 27.12%, as the manual and the command line do |
| saving from the interface wrote 35% and 50 L/day as indoor fraction and outdoor demand, whatever those on the screen were | the file saves the simulated fractions; old files that disagree are opened with the total fraction they declare, with a warning |
| in the weekly, monthly and daily modes, the fallback fraction was the total one, which already includes the outdoor demand | the fallback fraction is the indoor one, and the outdoor demand is no longer counted twice |
| the interface ignored the fixed volume declared in the project and simulated the technical optimum of the sweep | in fixed-volume mode, the interface simulates the declared volume, as the command line does |
| the environmental tab of the interface used its own chlorine dose and factor, not those of the project | the environmental assessment reads the chlorine declared in the water quality step |
| the command line charged the same cistern price throughout the sweep | the price follows the volume, as in the interface; the NPV no longer grows indefinitely with capacity |
| the command line left the first-flush device out of the embodied carbon, converted the pump power by another rule and rebuilt the piping with only the 50, 75, 100 and 150 mm sizes | the command line's environmental assessment reads the first flush, the pump set and the piping from the project, as the interface does |
| the command line used 5,000 draws in SMAA-VIKOR and weights 0.33/0.33/0.34 in TOPSIS; the interface, 20,000 draws and 0.333/0.333/0.334 | both use 20,000 draws and the same weights |
| the no-cistern alternative entered the interface's multi-criteria analysis with a payback of zero, the best possible | an alternative that does not pay back enters without a payback, at both ends |
| the first-flush depth was 1.0 mm in the project file, in spreadsheet reading and in the engine, and 2.0 mm in the CAD exporter, the command line and the report | the fallback value became 2.0 mm on every path, according to item 4.1.5 of ABNT NBR 15527:2019; a project with no declared depth discards twice what it discarded, and the usable catchment falls in proportion to the days of light rain |
| the 34 CORSAN municipalities were stored as a straight line, `PB × C + basic service`, with sewage at 70% of the whole bill, although the utility charges `PB × Cⁿ + basic service` and sewage per m³ consumed | the water follows the Table of Exponents (`n` from 1.00 up to 20 m³ to 1.13 between 101 and 150 m³) and sewage, R$ 6.40/m³ in ANEXO-5; in Alegrete, reducing consumption from 30 to 20 m³ now saves R$ 253.81 a month, not R$ 155.55 |
| the commercial, industrial, public and social categories were the residential tariff multiplied by fixed factors, with no provider table at all: ×1.85 on commercial water, ×2.30 on industrial, ×1.65 on public and ×0.50 on social | a category only enters with the provider's official table; currently, commercial and public in the 34 CORSAN municipalities and industrial in 30. Elsewhere, the category appears disabled and the study uses the custom structure; when the category the building type requires is not available, the program warns that the residential tariff underestimates the saving |

### Fixes that do not alter results

The changes below fix the behaviour of the program without touching any calculated value. No result
changes because of them; it has only become harder to produce a wrong study.

<!-- tabela: Behaviour fixes that do not alter any calculated result -->
| What was fixed | What changes for you |
| :--- | :--- |
| the calendar demand modulation was not saved in the project file | a project with a weekly, monthly or daily profile reopens as it was saved |
| a JSON file of unknown schema was accepted and opened an entirely default project | opening stops with a message of its own |
| the standby pump checkbox forced two pumps in any situation | the quantity entered is respected |
| six fields were saved in the file and never read back | section {{n:36}} lists those that remain in that condition |
| A single name for the research group: Sustainable Environments Research Group, in Portuguese Grupo de Pesquisa em Ambientes Sustentáveis. | no calculated value changes |
| The Brasília and Manaus examples now use the official tariffs of each city, instead of those of Florianópolis. | no calculated value changes |
| A new example, `examples/exemplo_quatro_criterios.netuno`, in which the technical, economic, environmental and TOPSIS optima fall on four different volumes. | no calculated value changes |
| the spreadsheet scenario template cited rainfall series that are not distributed, and a scenario without its series was silently simulated with Florianópolis rain | the template uses the series in `data/rainfall`, and a missing series is an error naming the scenario and the file |
| the ANEEL tariff query had no overall timeout and wrote the file in use while downloading | the query gives up after three minutes, and an interrupted download does not leave the cache half written |
| the manual's equations lost the superscript: the NPV came out with `(1 + TMA) m` | exponents are superscript again |
| on the 3D schematic sheet, each accessory created a dimension plane and a two-line label, and the parts ended up on top of each other | the sheet became landscape A3, with dimension planes only at the main levels and the small parts identified by code, with type and level in a table alongside |
| the siphon overflow was drawn across the overflow pipe, with a gap on both sides | the siphon follows the direction of the pipe and touches the faces of the part |
| the volumetric view opened with building, ground, flow and shadows on, heavy on first opening | it opens with the labels only; the rest is turned on with the button |
| the text of the exponential formula widened the Tariff Manager column and narrowed the charts | the charts keep their width in any municipality |
| the Direct3D shader compiler warnings (X4122, X4000) appeared as «Qt warning» | they enter only the summary count; a compilation error still appears |
| the CAPEX of piping and accessories was an estimated allowance, and the LCA counted only the metres of pipe typed in; bends, fittings, parts and control cables of the 3D layout entered neither | in a new project, both now come from the layout, part by part, with the price and carbon of each item; old files keep the costs they declared |
| labour was fixed once, on generic allowances, and did not change with the volume in the sweep; the sweep also stopped charging the pressure pump when there was no upper tank | in a new project, labour is 30% of the materials of each volume, and the pump set enters every arrangement other than gravity, as in the economic engine |
| in the global optimiser, the currency symbol followed the language: in English, values in reais appeared as dollars | the symbol is that of the currency chosen in the project; in another currency, the 3D layout prices in reais and the automatic labour are no longer applied |
| the usual 3D layout was always the pumped one, with one pump set | the layout follows the project's supply (pumped, pressurised or gravity) and draws the standby pump set in parallel; the CAPEX and the LCA no longer charge upper-tank parts that do not exist and now charge those of the standby |

### Documentation

The documentation comes with the release in three formats, built from the same sources: the full
manual in PDF, seven separate volumes for those who only need one part, and a documentation site with
eighteen interactive figures, in which the reader changes the parameters and sees the result the
program calculated. All three, plus the `CHANGELOG.md` distributed with the code, come from the same
text files.

The manual now also exists in English, section by section, with the same numbers, figures, tables
and equations; it is the manual the International Edition installs and opens. An automatic check
refuses the build if the two versions diverge in structure. Three additions to the Portuguese text
came with the translation: section {{n:23}} explains where the order of Netuno's balance stands
between the YAS and YBS rules of the literature, which were previously given as equivalent to it;
appendix {{n:D}} gained the blocks of each municipality by category, with the audit status and the
date of each item of data; and the tariff material received is now registered in a control of its
own, in `tarifas/fontes/REGISTRO.md`, which says what has already arrived and what remains to be
collected.

> **In depth: why the pumping fix is the most relevant.** ABNT NBR 17094-2:2016 requires the motor
> efficiency to be marked on the plate **separately** from the power, which means that the rated
> power is the power available at the shaft, not the power drawn from the socket. Taking one for the
> other underestimates consumption by a factor equal to the motor efficiency, which for a half-hp
> two-pole machine is 60.5%. The effect is large in relative terms, though small in absolute terms,
> because the pumping energy of a building rainwater harvesting system is modest compared with the
> rest of the economic balance. Section {{n:28}} develops the full chain.

---

## How to tell whether your version has a fix

The procedure is direct and does not depend on asking anyone: open one of the example files that
come with the program, described in appendix {{n:J}}, run it, and compare the result obtained with
the value printed in this manual. Each example case was generated by the same version of the program
that generated this manual, and each published number has a matching automatic check, as section
{{n:34}} describes. A divergence, therefore, indicates that the installed program is not that of this
manual's version.

==If the numbers match, your installation corresponds exactly to the manual you have in hand.== If
they do not, the difference is not a defect of your installation, but a version difference that
needs to be identified before any study.

---

## What to declare in a published work

Good practice in computational reproducibility requires a paper to identify unambiguously the
program that produced the results. In Netuno's case, four items of information are enough, and all
are available without effort: the version of the program, which appears in the report; the source of
the precipitation series, with the period used; the tariff structure adopted, with its effective
date; and a statement of which parameters were changed from the default values. Section {{n:13}}
gives the full list, with a ready-made method paragraph to adapt.

Attaching the `.netuno` file to the supplementary material settles all four at once, because the file
is self-contained and carries the rainfall series inside it. It is the most economical way of making
a study verifiable by others, and costs an attachment of about 160 kB.
