# How the program is verified

> This section describes Triton's verification suite, so that a reviewer has what they need to
> judge how far a result produced by the program can be trusted.

A scientific program whose verification is not declared is like a claim without evidence: it may
be right, but whoever uses it has no way of knowing, and whoever reviews work done with it has no
way of judging. This section is the evidence behind the numbers presented in the rest of the
manual, and it was written to be read by those who need to decide whether to trust them.

---

## The suite

The program's verification consists of 1,544 automated tests, spread over 135 files and organised
into five complementary families ({{fig:fig45_suite}}): unit tests, invariant tests, integration
tests, graphical interface tests and the test that replicates the results of Netuno 4. The
separation is not merely organisational: each family catches a distinct class of defect, and the
absence of any of them would leave a flank exposed.

![The five families of the verification suite](../figuras/fig45_suite.png)

*Figure 99 — Number of tests and of files in each family of the verification suite, as collected in this version. Unit tests account for more than four fifths of the total, because they run fast and locate the error close to its origin.*


The whole suite runs at every change to the code, and no change is merged while a test is failing.
That discipline is what allows us to say that a fixed defect does not come back: the fix comes with
the test that watches over it.

---

The verification layers of the program form a hierarchy, and each one catches a kind of error the
others would not reach. A unit test does not detect a model error, because it checks the function
against what is expected of it; and a manual check, which would detect that error, does not cover a
thousand input combinations ({{fig:fig00m_verificacao}}).

![The verification layers of the program](../figuras/fig00m_verificacao.png)

*Figure 99 — The five verification layers of the program, from the unit tests, numerous and aimed at local errors, to the manual check, occasional and aimed at model errors. No layer replaces another: it is the overlap of the five that supports the published result.*

---

## The invariants

The invariants are the most important family of the suite, and the reason lies in the nature of
what they check. A value test checks whether the program produces a specific number for a specific
input; an invariant checks whether a **property** holds for any admissible input. The first detects
that a calculation has changed; the second detects that the model is no longer physically
consistent.

**Mass conservation** requires that, over ten-year series, the volume collected equals the sum of
the volume overflowed, consumed and left in storage. The residual measured is of the order of 10⁻¹⁴
per cent of the volume collected, that is, the rounding error of floating-point arithmetic itself.
**Closure of the demand balance** does the same on the consumption side: the total demand must be
exactly the sum of three parts, which are the rainwater consumed, the potable water bought and the
unmet demand.

The **range of the potential** checks that the saving potential stays between zero and one hundred
per cent for every combination of volume, runoff coefficient and area, which is checked over sixty
combinations. The **ceiling of the suppliable fraction** is more specific and more revealing: the
potential can never exceed the fraction of the demand rain can supply, and the check extends to
volumes of one hundred cubic metres, far beyond any plausible building application.

**Parity between engines** compares the compiled core with the reference loop and requires both to
return the same number, for single and double tanks, with and without the irrigation backup supply,
within a tolerance of 10⁻⁹. **Monotonicity**, finally, requires that more volume never reduces the
potential and that more demand never increases it — two properties any correct implementation
satisfies and a defective implementation violates conspicuously.

---

## Analytical cases

A separate set gathers **closed-form** cases, that is, situations in which the correct result is
known by deduction, with no need to simulate: constant rain, constant demand, a tank of infinite
capacity and a tank of zero capacity. ==They are the strongest test available, because they do not
depend on any reference value produced by the program itself.== A test that compares today's output
with yesterday's detects a regression, but perpetuates an error that already existed in both; an
analytical case cannot do that.

---

## Path tests

This family was born from the most persistent defect this program has shown over its history: a
value calculated correctly that does not reach whoever should consume it. It is a class of error
that escapes formula tests entirely, because each part on its own is correct — the source calculates
well, the destination would calculate well if it received the value, and what fails is the stretch
between the two. Only a path test catches it: change the input on the screen and check that the
final result actually moves.

Five real defects found by this family, and now watched by it, illustrate the pattern: the choice of
disinfection technology did not reach the life cycle assessment; unticking the polishing filter had
no effect in classes 2 to 4; the four tax fields were zeroed by the screen itself when it was
closed; the irrigation backup supply option did not reach the compiled cores; and thirty of the
eighty-seven fields of the time did not survive saving and reopening the project.

---

## The numbers of the manual

With the writing of this manual a verification family of its own was created, meant to keep the
document and the program from diverging: **each printed value has a matching assertion**. The
numbers of section {{n:23}}, those of the whole tutorial and each row of the ten-day table are
covered, as is the requirement that certain sections declare certain caveats. When the program
changes, the test fails and points to the page to correct.

It is the mechanism that keeps a whole manual from ageing silently, which is the usual fate of the
documentation of scientific programs.

---

## Verification against Netuno 4

The verification extends to the comparison with the previous version of the program, over four
thousand and fifty reference cases, with the difference broken down by attributable cause. Section
{{n:35}} presents the result of that comparison and the two deliberate methodological divergences
that explain it.

---

## What the verification does **not** prove

The distinction between verification and validation is demanded by any competent reviewer, and
rightly so, because the two answer different questions and only one of them is within the reach of
a test suite.

**Verification** answers whether the program correctly solves the equations it implements, and
that is exactly what the suite described in this section tests. **Validation** answers whether the
equations implemented adequately represent physical reality, and that requires field measurement:
systems installed, monitored over time and compared with what the simulation predicted.

Triton is verified. The validation of the daily behavioural model rests on the literature of the
field, not on measurement of its own carried out by this group. ==A study that presented the
program's results as if they were measurements would be making a methodological error.==

---

## The verification report in the interface

The **Help → Verification Report** menu opens, inside the program, the verification report of the
version: the distinction between verification and validation, the kernels exercised, the
invariants, the analytical cases and the comparison with Netuno 4. It is the reference to cite when
a study needs to declare how the program was verified.

---

## Who runs the suite, and when

The suite comes with the program's source code, not with the installation: it is run by the
research group at every change, before any version is released. What this means for those using the
installed program is that the version on their machine has passed the 1,544 tests described here,
including those that check each number printed in this manual.

> **In depth: checking for yourself.** The source code is public, under the GPL v3 licence, and the
> suite runs with a single command in the development environment. A reviewer who wants to check the
> invariants — mass closure, monotonicity, parity between the two calculation engines — finds the
> test files organised by subject, and appendix {{n:B}} links each process of the program to what
> verifies it.
