# How to report a problem

Simulation programs have defects, and Netuno is no exception. The review carried out before this
release found a dozen calculation defects, none of them accompanied by an error message, and most of
them discovered not by reading the code but by comparing two points of the program itself that
should agree and did not. The practical lesson is that the attentive user is the best source of
detection a scientific program has, and that is why this section exists.

==A good report is one that allows the problem to be reproduced without you being there.== Everything
asked for below serves that single aim.

---

## What to send

A useful report has four components, and the absence of any of them usually turns the investigation
into an exchange of messages that takes more of everyone's time than the fix itself.

**The project file.** It is the most important item, and on its own it replaces pages of
description. The `.netuno` file is self-contained: it carries all the parameters and the whole
rainfall series inside it, so whoever receives it reproduces your simulation exactly, on the same
machine or any other. Without it, the investigation starts by trying to guess the inputs, and
guessing inputs is the most efficient way of not finding a defect.

**What you expected and what you got.** This is the part only you can provide. Describe the number
that appeared and the number that should have appeared, with the reason for the second — be it a
hand calculation, a result from an earlier version, a value from the literature or simply the order
of magnitude experience suggests. A report that only says «the result is wrong» leaves the recipient
to discover which of the forty numbers on the screen is the wrong one.

**The version of the program.** It appears in the sidebar, in the footer and in the **About Netuno**
menu, and is already saved inside the project file and any exported report. State it anyway, because
it is the first filter of the investigation: half the problems reported in scientific programs are
defects already fixed in a version later than the one the user has installed. State the edition too,
Brazil or International.

**The error message, if there is one.** Copy the full text, not a summary. Section {{n:37}} lists the
messages the program raises deliberately, with the meaning of and the action for each one; if your
message is there, the problem is probably one of input and has an immediate solution.

---

## What to check before reporting

A considerable share of the results that look wrong are correct results of wrong inputs, and the check
below takes a few minutes. It is not there to discourage the report, but so that your time and that
of whoever investigates is spent on what really is a defect.

Start with section {{n:33}}, which gathers the ten design mistakes the program has no way of
preventing. Three of them account for most unexpected results: the catchment area entered as the
sloping area of the roof instead of the horizontal projection, the first-flush depth entered in
litres instead of millimetres, and the municipality's tariff regime treated as a minimum consumption
when it is an availability charge — or the reverse.

Then check whether the behaviour observed is not a declared limitation. Section {{n:36}} lists what
the program admittedly does not do, and some of those limitations give exactly the impression of a
defect. The most frequent case involves the tariff category: the catalogue covers the residential
category of the 652 municipalities and the others only where the provider's official table has been
transcribed, so that, in the other municipalities, a study of a school or a shop comes out with the
residential tariff until the user enters that of the right category. The program warns about this
instead of correcting it on its own, because the right table is public and specific to each utility.

---

## Where to send it

Netuno is developed by the Sustainable Environments Research Group, in the Department of Civil
Engineering of the Federal University of Santa Catarina. The group's contact is the reporting
channel, and it serves for defects as well as for feature suggestions and requests for clarification
of the method. Reports may be written in English.

Reports that come with the project file go straight into the verification suite described in section
{{n:34}}: a case that reproduces a defect becomes a test, and the test then keeps that defect from
coming back. That is why the file matters so much, and it is also the most complete answer that can
be given to whoever reported — the problem was not only fixed, it is now watched.

> **In depth: what makes a defect hard to find.** The defects that survive for years in a scientific
> program all have the same signature: they produce plausible numbers. An error that generates a
> negative value, or one a thousand times larger than expected, is found on the first run. But an
> efficiency factor applied twice, or a unit converted once more than necessary, produces a number
> that passes any visual inspection and survives years of use. That is why the program's verification
> rests on invariants — the mass balance that must close, the monotonicity that must hold, the
> ceiling the curve cannot cross — and not only on expected values. When you suspect a number, the
> quickest way to confirm the suspicion is to look for one of those identities it violates.
