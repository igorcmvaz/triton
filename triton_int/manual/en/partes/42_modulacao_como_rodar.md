# How to run it

> **Question this section answers:** what are the steps, on the screen and on the command
> line?

## In the interface

The tool sits at the end of the sidebar, in **13. Probabilistic Modulation**, in both
editions. It starts from the study that steps 1 to 4 describe — the same configuration the
program writes to the `.triton` file — with the TOPSIS weights and the environmental
assumptions of the screen. With no rainfall series loaded, the tool warns and does not run. To
start, open the case `10_modulacao_tutorial.triton` or `11_modulacao_climbra.triton` (appendix J):
both arrive with the tool set up, and a click on **Simulate** is enough.

The distributions start from the screening of the open study. When another project is opened, or
an assumption changes in steps 1 to 4, the cards that have not been edited follow the new value; the
edited ones stay as they are. In a fixed-volume study, the tool shows only the study volume: the
per-volume figures and table require the step 4 sweep.

The screen has four blocks, from top to bottom:

1. **What to vary.** The twenty variables, in seven groups, with tick boxes. Hovering over
   one of them shows what it represents. Below the groups, in the Brazil Edition, the list
   of the nineteen climate models, with the **Select all** and **Clear all** buttons
   (section {{n:41}}).
2. **Distributions.** One card per ticked variable, with the study value, the distribution,
   the parameters, the bounds and the curve. The **Screening values** button returns every
   distribution to the default centred on the project.
3. **Run.** The number of realisations (1,000 by default), the seed (42) and the optional
   daily variation. **Simulate** runs in the background, with a progress bar, remaining time
   and a **Cancel** button; when cancelled, the analysis shows the realisations already
   done.
4. **Results.** Numbered tables and figures, explained in section {{n:43}}.

The layout rearranges itself with the window width — three, two or one column — and there
is no horizontal scrolling. The distributions, the ticked models, the number of realisations
and the seed are saved in the project and return when it is reopened; the results are not, because they are
reproduced identically with the same seed.

The time grows with the number of realisations, of volumes and of years of rainfall. Each
realisation reruns the technical, economic, environmental and TOPSIS chain for every volume;
the SMAA-VIKOR acceptability (section {{n:32}}), which draws twenty thousand weight vectors,
is left out of the realisations, because the modulation only uses the TOPSIS winner. In the
tutorial, with 21 volumes and thirty years of rainfall, the thousand realisations take
about half a minute on the computer on which this manual was generated; the progress bar
estimates the remaining time. The **Export (CSV + JSON)** button writes the samples, one
line per realisation, and the full summary, with the seed and the distributions.

## On the command line

The `probabilistic-study` command uses the same core as the screen and gives the same numbers
with the same project and the same seed:

```
triton probabilistic-study 02_tutorial_varredura.triton --samples 1000 --seed 42
triton probabilistic-study 02_tutorial_varredura.triton --list-variables
triton probabilistic-study project.triton --var fator_chuva=normal:1:0.1 --var fator_investimento=lognormal:1:0.15
triton probabilistic-study project.triton --var fator_cisterna=lognormal:1:0.15 --var fator_om=lognormal:1:0.25
triton probabilistic-study project.triton --climate-models todos
triton probabilistic-study project.triton --format json --output modulation.json
```

Without distribution options, the command reads the ones the screen saved in the project
or, failing those, the screening values. `--var VARIABLE=DISTRIBUTION` switches on any
variable of the catalogue and can be repeated; distributions are written
`normal:mean:deviation`, `lognormal:mean:deviation`, `triangular:minimum:mode:maximum`,
`uniforme:minimum:maximum` or `fixo`. The shortcuts `--per-capita`, `--people` and
`--non-potable` apply to the three consumption variables, and `--daily-cv` to the daily
variation. `--climate-models` takes the climate models separated by commas, `todos` (all)
or `nenhum` (none), and requires a project with rainfall from the CLIMBra database;
`--list-variables` also lists the model names. The `csv` format writes the samples;
`json`, the whole result. The old name of the command, `stochastic-study`, is still
accepted.
