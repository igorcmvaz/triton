# Installation and first run

> By the end of this section you will have the program installed, open, and a
> simulation finished with a result you can check against this manual.

---

## What you need

<!-- tabela: System requirements to install and run the program -->
| Requirement | What is needed |
| :--- | :--- |
| system | Windows 10 or 11, 64-bit |
| disk space | about 0.7 GB |
| memory | 4 GB is enough; 8 GB makes the sweep more comfortable |
| privileges | administrator, to install for all users; without them, the installation goes to the user's folder |

Nothing else needs to be installed. The program is distributed already assembled, with
all the components it depends on to calculate, and does not require any prior
installation of interpreters, libraries or auxiliary packages. Nor does it need an
internet connection to work: everything it consults during a simulation is on the
computer itself.

---

## The edition

This is the International Edition (INT). It carries no rainfall, tariff, price, standard
or emission factor of any one country: you enter those of your project, in the currency
you choose. The blue badge at the top of the sidebar, the window title and the footer of
every report and export say which edition the study came from.

<!-- tabela: What the International Edition brings and what it leaves to you -->
| | International Edition (INT) |
| :--- | :--- |
| installer | `Triton_INT_Setup_1_0_0.exe` |
| language on opening | English |
| rainfall | your own series; three sample series (New York, London, Cape Town) ship with the program |
| water and sewage tariffs | typed in |
| electricity | typed in |
| currency and costs | no default currency: you choose it; costs typed in |
| grid and potable water emission factors | from the project's country, mandatory |
| certifications and incentives | LEED, EDGE |
| step 12 | Probabilistic Modulation |
| cost of piping and labour | typed in |
| manual the program opens | this English manual |
| stored preferences | `Triton-INT` |

Without the emission factors of the project's country, the program does not calculate
the environmental assessment: a factor from the wrong grid would give a wrong result
without any warning.

The method is the same whatever the country: the daily balance, the first flush, the
runoff coefficients, the economic analysis and the life cycle assessment are one engine.
What changes from one country to another is **data**, and the program leaves it to you.
Where a requirement of a national standard matters, this manual describes it in general
terms and asks you to check the standard that applies where the building stands.
---

## Installation

1. Run **`Triton_INT_Setup_1_0_0.exe`**. The installer asks whether the installation is for all
   users, which requires administrator rights, or only for you.
2. Choose the installation language and read and accept the licence (academic source-available, non-commercial use).
3. Choose the installation type. The **standard** one brings the program, the manual,
   the cases, the examples and all the languages. The **custom** one lets you untick the
   Spanish and Chinese language packs.
4. Accept the suggested folder, `C:\Program Files\Triton International`, or choose
   another.
5. Tick, if you wish, **create a desktop icon**. The option **open .triton files with
   Triton** comes unticked, so as not to take over the project files of another Triton
   edition installed on the same computer; tick it if you want double-clicking a
   project to open it directly in the program.
6. When it finishes, the installer offers to open the program.

After that, the Start menu has two shortcuts: the program, and its manual in PDF
(this English manual). To uninstall, use Windows *Apps and features*, as with any program; your
projects stay where they were saved.

> **What the installer puts on the computer.** The program, the three sample rainfall
> series that come with the installation, the example files and this manual.
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
any other computer even without the files it came from. ==It is also the file to attach
to a paper so that someone else can reproduce the study,== and this property is what
separates a verifiable piece of work from one that is merely reported.

---

## The rainfall series

The program brings three long historical series ready to use — New York, London and
Cape Town, 1991 to 2020, from the ERA5 reanalysis — and accepts any series of your own
in CSV: daily precipitation in millimetres, one value per day, as appendix {{n:F}}
describes. The sample series are reanalysis grid-point data, not rain-gauge records.
They serve as examples and starting points; for a real project, use the series measured
at the site.
---

## The example files

The manual comes with ready-made projects that reproduce the results printed here.

<!-- tabela: Example files distributed with the program -->
| File | What it is for |
| :--- | :--- |
| `casos_tutorial_new_york.triton` | the project that chapter {{c:2}} builds, ready |
| `casos_ten_days.triton` | the ten-day teaching case of section {{n:23}} |
| `casos_london.triton` and `casos_cape_town.triton` | the same building in other cities |
| `examples\*.triton` | three complete studies: New York, London and Cape Town |

They are in the program folder. Appendix {{n:J}} lists the ten cases of the manual,
with the chapter of each one and the result they produce.

It is worth starting with the ten-day case. Open it, run the simulation and compare the
result with the table printed in section {{n:23}}. If the two match, the installation
corresponds exactly to this manual; if they differ, the manual and the program are of
different versions, and section {{n:38}} explains what to do in that case.

---

## The first simulation, in five minutes

The program is organised in **steps**, in the left sidebar, in the order in which you
work. For the first simulation four of them are enough.

1. **Project & Rainfall.** Load the file
   `NewYork.csv` that comes with the program. Enter a catchment area of 150 m²,
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

**There is no list of cities.** The program does not carry a rainfall database. Load one
of the three sample series, or a rainfall file of your own.

**Some part of the program is missing, such as the 3D volumetry.** Run, in the Command
Prompt, `"C:\Program Files\Triton International\Triton_INT.exe" --diagnostico` (with
the default folder). The
program lists what the installation contains: the 3D viewer, the sample rainfall series and the manual. Each item is marked OK or FALTA (missing). The list is
also saved in `triton_diagnostico.txt`, in the Windows temporary folder. Send that file
with the problem report.

**The result does not match the manual.** Check, in this order: the rainfall series
loaded, the area, the coefficient, the first-flush depth, the demand and the
rainwater-suppliable fraction. A difference in result is almost always a difference in
input, and section {{n:33}} lists the most common mistakes.

**An error message appeared.** Section {{n:37}} has the program's messages, what each one
means and what to do.
