# Importing a legacy project

> **Question this guide answers:** do my old studies open in Triton?

Studies saved in the legacy text format of an earlier simulation tool open in Triton, and most of
the data cross the conversion without loss. The care this section asks for comes from two facts
that sit badly together: some fields do not cross, and the import does not say which. A study
reused without checking can therefore keep looking like the original study while simulating
something else.

---

## How to import

Just open the old file from the open-project menu. The program recognises the legacy format,
which is semicolon-separated text, and converts it into the internal structure of the current
version. Once converted, save the project: it is then saved in Triton's JSON format, with
the fields described in appendix {{n:A}}, and the original file stays intact on disk, which is
worth keeping as evidence of the previous study.

---

## What comes across

Practically the whole input core of the legacy format has a direct counterpart in the current
version, and is converted without user intervention. The table below lists what the import
recovers.

<!-- tabela: Legacy-format data recovered by the import -->
| Item | Comes across? |
| :--- | :---: |
| rainfall file and start date | yes |
| catchment area, runoff coefficient | yes |
| first flush and mode | yes |
| total demand and number of residents | yes |
| percentage suppliable by rainwater | yes |
| upper tank, pumping trigger level | yes |
| lower tank, range and step | yes |
| difference between potentials | yes |
| water and sewage tariffs, taxes | yes |
| initial costs: labour, piping, accessories | yes |
| pump: power, efficiency, flow rate, start-up time, cost | yes |
| electricity tariff and taxes | yes |
| inflation, escalation, analysis period, minimum attractive rate | yes |
| operating costs | yes |

---

## What does not come across

> **Warning, and always check.** The reader of old files **does not recognise any variable
> demand key**. A legacy project that used a monthly or daily demand is imported as a
> **constant** demand, without any warning.

The consequence of this limitation deserves to be spelled out, because it changes results
without changing the appearance of the project. If the original study modulated the demand
by calendar (a school on holiday, a seasonal hotel), the import degrades it to a uniform
consumption, and the mismatch between supply and demand that the modulation represented
disappears from the calculation. In the Cape Town hotel of the manual, that degradation would
turn 9.83% into 10.97%. Check the demand mode right after importing, and re-enter the profile
by hand if it is on «constant» when it should not be. Section {{n:17}} shows how.

There is also a set of parameters that do not come across for a different reason: they simply
did not exist in the legacy format. They are irrigation and the suppression of watering by rain,
the water quality class and the treatment line, the tank materials and the pipe lengths per
diameter, the life cycle assessment parameters, the building type and the number of dwelling
units. All take the default value of the current version, and all deserve review before the
imported project is considered ready.

---

## Why the result changes

Even if the import recovers all the input data perfectly, the simulation result may not be
identical to that of the previous tool. The difference is deliberate and has a known cause.

The main cause is the **treatment of the first flush**. The legacy rule treats the first-flush
depth as an event threshold: when the day's rain does not reach the depth, nothing is collected;
when it exceeds it, the whole rain is collected, without subtraction. Triton subtracts the depth
from the day's precipitation, which is physically more faithful, because the water diverted to
the self-cleaning device really does not reach the cistern. With the same inputs, the legacy
rule therefore returns a higher saving potential than Triton does, and the gap is larger where
light rain on many days is common. Section {{n:35}} deals with the comparison.

---

## Comparing the two tools correctly

When the work explicitly compares the two tools, there is a simple procedure that isolates the
behaviour of the water balance from the deliberate methodological divergence, and it needs no
feature of the program: **run both with a first flush of zero**. Without a first flush, the two
rules coincide by construction, and any remaining difference is attributable to the
implementation, not to the method.

Once that comparison is made, repeat it with the project's real first flush to measure the
total difference. Taken together, the two numbers separate what is a deliberate change of
method from what would be an eventual divergence of implementation, and that separation is
exactly what a reviewer asks for.

> The program has no option to emulate the old first-flush rule. Use the zero-first-flush
> route, which produces the same result with a little more work and no surprises.

---

## After importing

Seven checks are enough to turn an imported project into a reliable one, and they should be
done in the order below, because the first ones affect the result of the following ones.

1. **Demand mode**: was it degraded to constant?
2. **Building type**: is it the right one?
3. **Tank materials**: the default adopted is polyethylene.
4. **Water quality class** and disinfection technology.
5. **Tariff regime**: the legacy format did not distinguish the minimum-charge regimes, and
   section {{n:16}} shows what that changes.
6. **Motor efficiency** of the pump, which the legacy format did not have.
7. **Run the project and check the potential** against the old result before trusting the
   imported file.

And keep the original file: it is the documentary evidence of the previous study, and no
conversion replaces it.
