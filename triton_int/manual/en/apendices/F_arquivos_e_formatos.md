# Files, folders and formats

Everything the program reads and writes, and where each thing is kept.

---

## What the program reads

<!-- tabela: Formats the program reads and where each one is loaded -->
| Format | Extension | What it is | Where it is loaded |
| :--- | :--- | :--- | :--- |
| project | `.triton` | a complete study, with the rain inside | Open Project |
| old project | `.json` | project from an earlier version, same content | Open Project |
| legacy project | `.csv` | project saved by an early version of the program, as a table | Open Project |
| rainfall series | `.csv` | one column of millimetres per day (the edition ships three examples in `data/rainfall`) | step 1. Project & Rainfall |
| daily demand | `.csv` | measured consumption, day by day | step 2. Building & Demand |
| scenarios | `.xlsx` | one row per scenario | Scenarios & Tools menu |

**The rainfall series in CSV** is the simplest format possible: one line per day, with the depth in
millimetres. The program accepts a point or a comma as the decimal separator, and ignores a header
line if there is one. An incomplete year is discarded on reading, so as not to bias the annual
totals.

> **Legacy project in CSV.** The old format does not keep everything the current version uses:
> demand modulation, materials, multi-criteria weights and the rainfall series are left out. When
> opening such a file, the program warns and adopts the default values for what is missing. Section
> {{n:21}} shows what to check after importing.

---

## What the program writes

<!-- tabela: Formats the program writes and where each one is generated -->
| Format | Extension | What it carries | Where it is generated |
| :--- | :--- | :--- | :--- |
| project | `.triton` | all the parameters and the rainfall series | Save Project |
| report | `.pdf` | the complete study, ready to hand over | step 9. PDF Reports |
| spreadsheet | `.xlsx` | daily series, sweep and indicators | step 10. Export |
| table | `.csv` | the same data, as delimited text | step 10. Export |
| data | `.json` | the results, for reprocessing | step 10. Export |
| drawing | `.dxf` | the hydraulic schematic, for CAD | step 10. Export |
| drawing | `.svg` | the same schematic, as a vector image | step 10. Export |

In CSV export you choose the separator: **semicolon** to open in a spreadsheet set to a language
that uses the decimal comma, **comma** for the international standard. Choosing wrongly
makes the spreadsheet open everything in a single column.

The drawing comes in three presentations: **A3 technical sheet**, **simple schematic** and **block
library**, the last accompanied by a JSON file with the properties of the components, for BIM
coordination. Section {{n:22}} deals with all of them.

---

## The project file, inside

The `.triton` file is a text file in JSON format. It can be opened in any text editor, and that is
deliberate: a published study needs to be inspectable without the program.

It has seven sections:

<!-- tabela: The seven sections of the project file and what each one holds -->
| Section | What it holds |
| :--- | :--- |
| `metadata` | project name, identifier and dates |
| `rainfall` | the city, the period and the **whole daily series** |
| `building_and_demand` | area, coefficient, occupants, consumption and fraction |
| `demand_modulation` | the weekly, monthly and daily profiles, when there are any |
| `reservoirs_and_pumping` | volumes, thresholds and the pump set |
| `water_quality_and_etap` | target class, disinfection and treatment |
| `financial_and_economic` | tariffs, taxes, adjustments and period |

Appendix {{n:A}} lists all the parameters, with the exact name of each field.

> **The rainfall series goes inside the file.** That is what makes the project reproducible: whoever
> receives the file obtains exactly your numbers, without needing the original rainfall file. On the
> other hand, a project with thirty years of series takes up about 160 kB — little for a file and a
> lot for an e-mail attachment with twenty of them.

---

## Where things are kept

<!-- tabela: Location of the program's files and of the user's files -->
| What | Where |
| :--- | :--- |
| the program | `C:\Program Files\Triton` |
| the rainfall series that come with it (New York, London, Cape Town) | in the program folder, in `data\rainfall` |
| the manual's cases | in the program folder, in `casos` |
| the three example projects (New York, London, Cape Town) | in the program folder, in `examples` |
| **your projects and reports** | **wherever you choose when saving** |

The program does not create a working folder or keep hidden files. Each save asks for the
destination, and nothing you produce stays inside the installation folder — which means that
reinstalling or updating the program deletes nothing of yours.

---

## Compatibility between versions

<!-- tabela: Compatibility between versions of the project file -->
| Situation | What happens |
| :--- | :--- |
| project from an earlier version | opens; new fields take the default |
| project from this version in an earlier version | may not open, or may lose fields |
| legacy project in CSV | opens with a warning; check what section {{n:21}} lists |
| JSON file from another program | **rejected**, with a message of its own |

The last row deserves an explanation. A JSON file that is not a Triton project could, in principle,
be accepted and filled in with default values — and the user would simulate 100 m² believing they
were simulating the 180 m² the file describes. The program prefers to stop the opening with a message
of its own, which is inconvenient and is correct: a project opened wrongly produces an entire study
that is wrong.
