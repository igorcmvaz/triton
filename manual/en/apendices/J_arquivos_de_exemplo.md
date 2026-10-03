# Example files

The manual prints results; these files are what you open to reproduce them. They are in the program's
`casos` folder, and each one carries its rainfall series embedded: they open without the original
CSV, on any machine.

---

## The nine cases of the manual

<!-- tabela: The nine example cases and what each one demonstrates -->
| File | Section | What it demonstrates |
| :--- | :--- | :--- |
| `01_tutorial_florianopolis.netuno` | 4.1 to 4.10 | the final tutorial project: a 4,000 L polyethylene cistern pumping to a 1,000 L upper tank |
| `02_tutorial_varredura.netuno` | 4.4 and 2.2 | the project before the upper tank, in sweep mode, from 0 to 20,000 L, in steps of 1,000 L |
| `03_dez_dias.netuno` | 2.1 | the ten-day teaching case, which fits in a spreadsheet |
| `04_reservatorio_superior.netuno` | 4.5 | 4,000 L below plus 1,000 above, the comparison of section 4.5 against the 5,000 L of a single tank |
| `05_manaus.netuno` | 3.1 | the tutorial project taken to Manaus, where it rains more and yields less |
| `06_brasilia.netuno` | 3.1 | the tutorial project taken to Brasília, with a marked dry season |
| `07_saopaulo.netuno` | 3.1 | the tutorial project taken to São Paulo |
| `08_escola_semanal.netuno` | 3.4 and 3.5 | a school of 300 pupils with demand modulated by day of the week |
| `09_hotel_mensal.netuno` | 3.4 | a seaside hotel with monthly occupancy in phase with the rain |

## What each one produces

The values below are obtained by **rereading the saved file** and simulating what was reread, not the
configuration that generated it. That is the difference that matters: a parameter that does not
survive saving shows up here as a wrong number, instead of going unnoticed.

<!-- tabela: Result each example case produces when reread and simulated -->
| File | Mode | Volume | Potential | Rainwater consumed |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_florianopolis.netuno` | fixed volume | 4,000 L | 27.30% | 163.8 L/day |
| `02_tutorial_varredura.netuno` | sweep | ideal: 4,000 L | 27.12% | 21 volumes |
| `03_dez_dias.netuno` | fixed volume | 2,000 L | 36.00% | 72.0 L/day |
| `04_reservatorio_superior.netuno` | fixed volume | 4,000 L | 27.30% | 163.8 L/day |
| `05_manaus.netuno` | fixed volume | 4,000 L | 20.96% | 125.8 L/day |
| `06_brasilia.netuno` | fixed volume | 4,000 L | 15.45% | 92.7 L/day |
| `07_saopaulo.netuno` | fixed volume | 4,000 L | 25.74% | 154.4 L/day |
| `08_escola_semanal.netuno` | fixed volume | 30,000 L | 34.34% | 3,095.8 L/day |
| `09_hotel_mensal.netuno` | fixed volume | 25,000 L | 32.11% | 1,854.9 L/day |

---

## How to run them

**File, Open Project**, choose the file, and the program loads everything: the rain, the building, the
costs and the configuration of the analyses. Go through the result steps in the sidebar to see each
dimension.

The files are in the `casos` folder, inside the program's installation folder. If you want to modify
them, **save them under another name**: that way the original case keeps reproducing the number
printed in the manual.

The water results above are the same in both editions. The cases carry Brazilian tariffs and costs in
reais; in the International Edition, replace them with your own before reading the economic results.

---

## The three studies in `exemplos`

Besides the manual's cases, the program comes with three reference studies in `exemplos`: a
single-family house in Florianópolis, an office building in Brasília and a public school in Manaus.
They are larger and less didactic than the manual's, and serve as a starting point for real projects.

> **They were re-saved in this version.** They were in an earlier flat schema, which the program read
> without recognising: they opened as a default project, with 100 m² and three occupants, and nothing
> warned. Opening now rejects an unknown format with a message of its own, and the three were
> converted to the current schema, with the rain embedded.

---

## What these files are not

They are not design templates. They are **demonstration cases**: the costs are those of the tutorial,
the tariff is CASAN's and the category is residential in all of them, including the school and the
hotel, because of the limitation section {{n:36}} describes. For a real study, replace the tariff,
costs and rainfall series with those of your case.
