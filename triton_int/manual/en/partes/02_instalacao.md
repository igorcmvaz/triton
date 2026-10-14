# Installation and first run

> By the end of this section you will have the program installed, open, and a
> simulation finished with a result you can check against this manual.

---

## What you need

<!-- tabela: System requirements to install and run the program -->
| Requirement | What is needed |
| :--- | :--- |
| system | Windows 10 or 11, 64-bit |
| disk space | about 1.5 GB for the Brazil Edition, with the national climate database; about 0.7 GB for the International Edition |
| memory | 4 GB is enough; 8 GB makes the sweep more comfortable |
| privileges | administrator, to install for all users; without them, the installation goes to the user's folder |

Nothing else needs to be installed. The program is distributed already assembled, with
all the components it depends on to calculate, and does not require any prior
installation of interpreters, libraries or auxiliary packages. Nor does it need an
internet connection to work: everything it consults during a simulation is on the
computer itself.

---

## The two editions

The program comes in two editions, with their own installers, which can be installed
side by side. The green (BRL) or blue (INT) badge at the top of the sidebar, the window
title and the footer of every report and export say which edition the study came from.

<!-- tabela: What changes between the Brazil Edition and the International Edition -->
| | Brazil Edition (BRL) | International Edition (INT) |
| :--- | :--- | :--- |
| installer | `Triton_Setup_1_0_0.exe` | `Triton_INT_Setup_1_0_0.exe` |
| language on opening | Portuguese | English |
| rainfall | CLIMBra database (652 cities) or your own series | your own series |
| water and sewage tariffs | catalogue of 652 municipalities, or typed in | typed in |
| electricity | ANEEL tariff or typed in; tariff flags | typed in |
| currency and costs | Brazilian reais, with reference prices | euro on opening, or another chosen currency; costs typed in |
| grid and potable water emission factors | Brazilian databases (MCTI, routes by region) | from the project's country, mandatory |
| certifications and incentives | LEED, EDGE, AQUA-HQE, Selo Casa Azul, IPTU Verde | LEED, EDGE |
| step 12, Tariff Manager | present | absent |
| step 13, Probabilistic Modulation | present | present |
| warning on non-residential tariff category | present ({{n:18}}) | absent: the tariff is the one typed in |
| cost of piping and labour | calculated from the arrangement, at Brazilian prices | typed in |
| manual the program opens | the Portuguese one; the English one in the other interface languages | the English one |
| stored preferences | `Triton` | `Triton-INT`, separate from the Brazil Edition |

Without the country's emission factors, the International Edition does not calculate the
environmental assessment: a Brazilian factor applied to another country would give a
wrong result without any warning.

Both editions calculate in exactly the same way: the daily balance, the first flush, the
runoff coefficients, the economic analysis and the life cycle assessment are the same
code. What the International Edition leaves out is Brazilian **data**, not method.
Throughout this manual, a «Brazil Edition (BRL) only» note marks what the International
Edition does not bring, and an «In the International Edition (INT)» note says how to
proceed in it. The
differences between the Brazilian standards the method follows and the European
standard EN 16941-1:2024 are listed, item by item, in the repository document
`docs/normas_nbr_x_en16941.md`.

---

## Installation

1. Run **`Triton_Setup_1_0_0.exe`** (Brazil Edition) or **`Triton_INT_Setup_1_0_0.exe`**
   (International Edition). The installer asks whether the installation is for all
   users, which requires administrator rights, or only for you.
2. Choose the installation language and accept the licence, the GPL version 3.
3. Choose the installation type. The **standard** one brings the program, the manual,
   the cases, the examples and all the languages. The **custom** one lets you untick the
   Spanish and Chinese language packs. In the Brazil Edition, the national climate
   database always comes along, embedded in the program.
4. Accept the suggested folder, `C:\Program Files\Triton` (Brazil Edition) or
   `C:\Program Files\Triton International` (International Edition), or choose another.
5. Tick, if you wish, **create a desktop icon**. The option **open .triton files with
   Triton** comes ticked in the Brazil Edition: with it, double-clicking a project
   opens it directly in the program. In the International Edition it comes unticked, so
   as not to take over the files of a Brazil Edition installed on the same computer.
6. When it finishes, the installer offers to open the program.

After that, the Start menu has two shortcuts: the program, and its manual in PDF —
this English manual in the International Edition, the Portuguese one in the Brazil
Edition. To uninstall, use Windows *Apps and features*, as with any program; your
projects stay where they were saved.

> **What the installer puts on the computer.** The program, the four historical rainfall
> series that come with the installation, the example files and, in the Brazil Edition,
> the tariff database of the 652 municipalities and the national climate database.
> Nothing is downloaded during use: Triton works without an internet connection.

---

## Where your files go

The program never decides for you where to save. Every time you save a project, a
report or an export, it asks for the folder.

<!-- tabela: File formats the program saves and the content of each one -->
| What you save | Extension | Contains |
| :--- | :--- | :--- |
| project | `.triton` | all the input data **and the rainfall series** |
| report | `.pdf` | the complete document of the study |
| results | `.xlsx`, `.csv` | the tables, for a spreadsheet |
| diagram | `.dxf` | the schematic drawing, for CAD |

Among these formats, `.triton` is the one that really matters to keep. It is
self-contained: it carries the whole rainfall series inside it, and therefore opens on
any other computer even without the files it came from. The exception is rainfall from the
CLIMBra database, which ships with the program: the file keeps the reference of the series —
city, model, scenario and date window — with the number of days, the total and a
fingerprint (SHA-256) of the values, and the program rebuilds it from the database when the
project is opened, checking the fingerprint. A series altered after loading, or a database
unavailable at saving time, is still written to the file in full. ==It is also the file to attach
to a paper so that someone else can reproduce the study,== and this property is what
separates a verifiable piece of work from one that is merely reported.

---

## The climate database

The program brings four long historical series ready to use — Florianópolis, Brasília,
Manaus and São Paulo — and accepts any series of your own in CSV.

> **Brazil Edition (BRL) only.** The national climate database ships only with the Brazil Edition.
> In the International Edition, the rainfall series is always a file of your own: daily
> precipitation in millimetres, one value per day, as appendix {{n:F}} describes.

Besides them, the Brazil Edition brings the **national climate database**: 652 cities,
19 CMIP6 climate models and 2 future scenarios, SSP2-4.5 and SSP5-8.5, extracted from the
CLIMBra dataset. The original files add up to about 6.5 GB. The program brings them
compressed into a single database of about 800 MB, embedded in the installer. There is
nothing to download or copy: the database appears on the first screen as a list of
cities.

Appendix {{n:E}} describes the database, and section {{n:15}} shows how to use a future
scenario.

---

## The example files

The manual comes with ready-made projects that reproduce the results printed here.

<!-- tabela: Example files distributed with the program -->
| File | What it is for |
| :--- | :--- |
| `casos\01_tutorial_florianopolis.triton` | the project that chapter {{c:2}} builds, ready |
| `casos\03_dez_dias.triton` | the ten-day teaching case of section {{n:23}} |
| `casos\05_manaus.triton` and the following | the same project in other state capitals |
| `exemplos\*.triton` | three complete studies: house, office and school |

They are in the program folder. Appendix {{n:J}} lists the nine cases of the manual,
with the chapter of each one and the result they produce.

It is worth starting with the ten-day case. Open it, run the simulation and compare the
result with the table printed in section {{n:23}}. If the two match, the installation
corresponds exactly to this manual; if they differ, the manual and the program are of
different versions, and section {{n:38}} explains what to do in that case.

---

## The first simulation, in five minutes

The program is organised in **steps**, in the left sidebar, in the order in which you
work. For the first simulation four of them are enough.

1. **Project & Rainfall.** Choose the city in the climate database, or load the file
   `Florianopolis1.csv` that comes with the program. Enter a catchment area of 150 m²,
   a runoff coefficient of 0.85 and a first flush of 2.0 mm.
2. **Building & Demand.** Choose a single-family house, 4 residents, 150 litres
   per person per day, and a rainwater-suppliable fraction of 28%.
3. **Reservoir & Costs.** Enter a fixed volume of 4,000 L.
4. Run it, and go to **Technical Results**.

You should get a saving potential of about **27%**.

Section {{n:6}} explains what this number means, and section {{n:7}} asks the next
question: is 4,000 L the right volume?

---

## If something goes wrong

**The program does not open.** Check that the installation finished without errors and
reinstall over it; reinstalling keeps your files, because they are not in the program
folder.

**The list of cities is empty.** The national climate database comes only with the
Brazil Edition. In the International Edition, use a rainfall file of your own.

**Some part of the program is missing, such as the 3D volumetry.** Run, in the Command
Prompt, `"C:\Program Files\Triton\Triton.exe" --diagnostico` (in the International
Edition, `"C:\Program Files\Triton International\Triton_INT.exe" --diagnostico`). The
program lists what the installation contains: the 3D viewer, the climate database, the
tariff database and the manual. Each item is marked OK or FALTA (missing). The list is
also saved in `triton_diagnostico.txt`, in the Windows temporary folder. Send that file
with the problem report.

**The result does not match the manual.** Check, in this order: the rainfall series
loaded, the area, the coefficient, the first-flush depth, the demand and the
rainwater-suppliable fraction. A difference in result is almost always a difference in
input, and section {{n:33}} lists the most common mistakes.

**An error message appeared.** Section {{n:37}} has the program's messages, what each one
means and what to do.
