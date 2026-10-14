# Where to start, depending on your goal

This manual brings together fifty-four sections in eight chapters, and it was not
designed to be read from cover to cover. It works best as a reference work, in which
each reader enters at the point that matches what they need to do, and this section
exists precisely to show that entry point.

---

## Route by goal

The table below lists the five most common purposes of people who open the program,
with the reading path for each one.

<!-- tabela: Recommended reading path depending on the reader's goal -->
| You want to | Read |
| :--- | :--- |
| **learn to use** the program | the whole of chapter {{c:2}}, sections {{n:4}} to {{n:13}}, in order |
| **solve a case** today | the three questions below, and then the guide of chapter {{c:3}} that fits |
| **publish** a study | chapter {{c:4}}, which has the method, and section {{n:13}}, with the declaration list |
| **review** someone else's study | chapter {{c:6}}, and appendices {{n:A}} and {{n:B}} |
| **migrate** from Netuno 4 | sections {{n:21}} and {{n:35}} |
| **avoid mistakes** | section {{n:33}}, with the ten most common mistakes |

Anyone with an hour and no previous familiarity should read the tutorial of chapter
{{c:2}}. It builds a complete study around a single project, and each section ends by
showing where that project has got to, so that the reader follows the construction
instead of receiving the finished result.

---

## The three questions that define a study

Even before opening the program, it is worth answering three questions, because they
determine a good part of the later decisions and because answering them afterwards
usually means redoing work.

### Which uses will rainwater supply?

The answer defines the **rainwater-suppliable fraction**, and that fraction is the
ceiling of everything else: a system whose fraction is 28% will never save more than 28%
of the total consumption, however large the cistern and however much it rains. No later
design decision changes this limit, which is why it deserves to be set before anything
else. {{fig:fig46_atendivel}} brings together the usual ranges of the suppliable
fraction depending on the intended uses.

![The suppliable fraction depending on the intended uses](../figuras/fig46_atendivel.png)

*Figure 99 — Which part of the total consumption rainwater can supply, depending on the uses the project intends. It is the ceiling of the saving potential: no tank, however large, exceeds this fraction.*

The residential cases are dealt with in section {{n:5}}, and the commercial case in
section {{n:18}}. The dashed line marks the 28% of the tutorial, which keeps to the uses
that item 4.1.7 of ABNT NBR 15527:2019 admits.


### Will you compare volumes or assess just one?

The distinction between assessing a known volume and looking for the right volume
determines the simulation mode and, with it, the computing time and the richness of the
result.

<!-- tabela: Choice between fixed volume and sweep depending on the question of the study -->
| If you want to | Use | Where it is dealt with |
| :--- | :--- | :--- |
| assess a cistern that already exists | fixed volume | section {{n:6}} |
| find out which volume to buy | **sweep** | sections {{n:7}} and {{n:24}} |
| choose between criteria that disagree | sweep and multi-criteria | sections {{n:12}} and {{n:32}} |

==The sweep is almost always the right answer.== It costs more computing time, in the
order of seconds, and it produces the curve of diminishing returns, which is the
strongest argument any study can have when justifying a volume.

### Is an upper tank needed?

The third question is hydraulic, and the answer depends on the height of the building
and on the pressure required at the points of use.

<!-- tabela: Hydraulic criteria to decide on the upper tank -->
| If the building | Then | Where it is dealt with |
| :--- | :--- | :--- |
| is single-storey and the points are close to the cistern | direct pressurisation, no tank | section {{n:8}} |
| is a two-storey house or a multi-storey building | elevated tank, for **pressure** | section {{n:8}} |
| needs a reserve against power cuts | elevated tank | section {{n:8}} |

> The elevated tank **does not increase** the water saving. Keeping the same total
> storage, it delivers slightly less and consumes pumping energy. The decision to adopt
> it must be hydraulic, and never based on the expectation of a larger yield.

---

## The order of work in the program

The program's sidebar is numbered, and the numbering matches the order in which you
work. The first four steps are data input, the next four show results, and the last
four produce outputs or support the study ({{fig:fig28_etapas}}).

![The twelve steps of the program, in the order of work](../figuras/fig28_etapas.png)

*Figure 99 — The twelve steps of the program, grouped by nature. The first four are input and must be filled in order, because each one uses what the previous one defined; the next four are for reading results; the last four produce outputs or give support, and can be used at any time.*

Where this manual deals with each one: step 1 in section {{n:4}}, step 2 in {{n:5}},
step 3 in {{n:9}}, step 4 in sections {{n:6}}, {{n:7}} and {{n:10}}, step 5 in {{n:6}},
step 6 in {{n:10}}, step 7 in {{n:11}}, step 8 in {{n:12}}, step 9 in {{n:13}}, step 10
in {{n:22}}, step 12 in {{n:16}} and step 13, Probabilistic Modulation, in sections {{n:40}} to {{n:44}}. Step 11 is the documentation built into the program
itself, and has no corresponding section here. In the International Edition, step 12,
the Tariff Manager, does not appear, because the Brazilian tariff catalogue does not
come with it.


It is worth saving the project at the end of each step. The parameters of appendix
{{n:A}} are saved and read back in full, and the resulting file is the documentary
evidence of the study, both for whoever will redo it in the future and for whoever will
assess it.

---

## Before publishing

Three readings are mandatory for anyone who intends to publish results, and none of them
is long. Section {{n:13}} has the list of what to declare in a paper, together with a
method paragraph ready to adapt. Section {{n:33}} brings together the ten design
mistakes that the program has no way of preventing. And section {{n:36}} lists the known
limitations — of which it is worth reading not all, but those that affect the case in
hand.

Appendix {{n:I}} condenses the three into one-page summaries, for quick reference.
