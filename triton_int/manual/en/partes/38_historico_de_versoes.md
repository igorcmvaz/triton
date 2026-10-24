# Version history and what changed

This section records what changed between versions of the program and, above all, **which changes
alter results already published**. The distinction matters more than it seems: a fix to the
interface affects no earlier study, whereas a fix to a calculation can shift every number of a
paper already submitted. Anyone who has published with Triton needs to know into which category
each change falls, and that is why the history below separates the two explicitly.

==The rule guiding this whole section is simple: a calculation fix obliges you to declare the
version used; an interface fix does not.==

---

## The version you are using

The version number appears in the sidebar, in the footer and in the **About Triton** menu. It is
also saved inside each project file and printed in each report, so that an old study always
carries with it the identification of the program that produced it. The redundancy is deliberate:
reports circulate separately from files, and the question «which version was this done with?»
usually comes up months later, when nobody remembers.

The numbering scheme follows the usual software engineering convention. The first number indicates
the generation of the program, and changing it means a reformulation of the conceptual model; the
second indicates a set of new features; and the third indicates fixes and adjustments that do not
change the architecture. A first number of zero marks a beta: the program is usable and verified as section {{n:34}}
describes, but its interface, file format and defaults may still change, and a change may alter
results.

The current version is the beta **0.1.0**. No earlier version circulated, and no study was done
with one.

---

## How this history is kept

From now on, each version released gets an entry of its own in this section, with the release date
and what changed, always split into two lists: ==what alters the results of studies already done and
what does not.== The most recent entry comes first.

Each entry follows the same model, so that two versions can be compared without rereading: a
one-sentence summary, the new features, the fixes that alter results, those that do not, and what
changed in the documentation. Sections with no content in that version simply do not appear.

The same list is distributed with the code, in the `CHANGELOG.md` file at the root of the
repository, and feeds the versions page of the documentation site.  It is written here first,
and the maintainers keep the other two equal to it. Those following the program through the
repository, the site or the manual read the same record.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Version 0.1.0 (beta) — October 2026

> **In one sentence.** First beta of Triton, with its own name, versioning and repository for
> each edition.

### What is new

Triton simulates rainwater harvesting day by day and carries the simulation engine, the life-cycle
assessment, the treatment line, the multi-criteria decision and the probabilistic modulation. This is
the first version of the International Edition, which has its own repository, logo and numbering.
The Fewkes operating rule (φ) is available as an option in every module.

**What the International Edition brings in this version.**

- **A region-neutral program.** It ships no regional rainfall database, no tariff catalogue, no cost catalogue and no emission-factor series, and it applies no national standard and no predefined currency. You supply the rainfall series of the site, the tariffs, the costs and the currency.
- **Three worked examples.** New York, London and Cape Town, with one building and three rainfall series (ERA5 reanalysis via Open-Meteo, 1991 to 2020, CC BY 4.0) and three tariff structures, each checked by hand against its printed bill.
- **The analysis chain.** Daily water balance, volume sweep and ideal volume, economic analysis with block tariffs and six tariff regimes, life-cycle assessment, treatment line, certification scoring, multi-criteria ranking, reports in PDF and spreadsheet, CAD and BIM exports.
- **Documentation.** The complete manual in English, an offline site, short volumes and `docs/DADOS.md`, which describes every dataset with its source, licence and quality.

**What this version does not have.**

- **Regional data.** No rainfall database, no climate projections, no tariff catalogue.
- **Prices.** The program does not calculate an investment from prices. Cistern, tank, piping, accessories, labour, pump and maintenance costs start at zero, and so do the electricity tariff and the price of chlorine; the water tariff is empty. Section {{n:10}} says what a new project contains and what you enter.
- **Emission factors.** The grid factor is zero until you enter the factor of your grid.
- **Verified example tariffs.** The three example tariffs are illustrative.

**Known limitations.**

- The address of each tariff document, its access date and its checksum were not recorded when the examples were built, so the figures cannot be traced to a stored copy; the effective dates of the London and Cape Town tariffs are inferred. The payback and the net present value shown for the example projects are not results.
- The example rainfall series are reanalysis grid cells of about 9 km, not rain-gauge records.
- The CAPEX dialog has no field for the cistern price and sets it back to zero on confirming; section {{n:10}} gives the way round. With no price list, the cistern price you enter applies to every volume of the volume sweep. The price of chlorine can be set only in the project file.
- In Spanish and Chinese the interface is partly translated, and the reports in those languages contain passages in another language; English is complete.
- The life-cycle steps warn that country factors are missing, by design.

### Fixes that change results

None: this is the first beta, and there is no earlier version to correct.

<!-- tabela: Fixes that change results in version 0.1.0 -->
| What was corrected | Effect on the result |
| :--- | :--- |

### Fixes that do not change results

None.

### Documentation

The manual gained the sections «CAPEX in this edition», «What goes into the running cost (OPEX)», «Regional and national particulars» and «Description of the data and how far to trust it».

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
program that produced the results. In Triton's case, four items of information are enough, and all
are available without effort: the version of the program, which appears in the report; the source of
the precipitation series, with the period used; the tariff structure adopted, with its effective
date; and a statement of which parameters were changed from the default values. Section {{n:13}}
gives the full list, with a ready-made method paragraph to adapt.

Attaching the `.triton` file to the supplementary material settles all four at once, because the file
is self-contained and carries the rainfall series inside it. It is the most economical way of
making a study verifiable by others, and costs a small attachment.
