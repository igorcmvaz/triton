# Error messages and what to do

> What each message means, what triggered it, and how to resolve it.

The program follows a deliberate policy towards impossible inputs: it rejects them instead of
silently correcting them. The reason is that a negative catchment area is not a user preference to
be accommodated, but a typing error that needs to be seen by whoever made it. ==Silently correcting
it would produce a plausible result from a wrong input, which is the worst possible combination in a
simulation program.==

> **The messages of the calculation core are in Portuguese.** The interface is
> translated, but the checks that run inside the calculation raise their messages in the language
> they were written in. The tables below quote each message as the program prints it, in
> Portuguese, followed by its meaning in English in brackets, so that you can recognise it on the
> screen.

---

## Physical validation of the input

The messages below are raised before any calculation starts, and all of them name the field
responsible and the value received, so that the correction does not require a search.

<!-- tabela: Physical input validation messages and the action for each one -->
| Message | What triggered it | What to do |
| :--- | :--- | :--- |
| «Volume do reservatório inferior negativo» (negative lower tank volume) | volume below zero | correct it; **zero is valid** and represents the no-system scenario |
| «Volume do reservatório superior negativo» (negative upper tank volume) | likewise, in the elevated tank | correct it; zero means no upper tank |
| «Área de captação negativa» (negative catchment area) | area below zero | correct it; use the horizontal projection in m² |
| «Coeficiente de escoamento fora de [0, 1]» (runoff coefficient outside [0, 1]) | negative coefficient or above 1 | above 1 the roof would deliver more water than the rain brings; usual roofs are between 0.80 and 0.95 |
| «Lâmina de descarte negativa» (negative first-flush depth) | first flush below zero | the first flush removes water from the catchment, it does not add any |
| «Demanda diária negativa» (negative daily demand) | demand below zero | correct it |
| «Fração atendível por água pluvial fora de [0, 1]» (rainwater-suppliable fraction outside [0, 1]) | fraction above 1 | enter 0.4 for 40%, not 40 |
| «… não é um número finito» (… is not a finite number) | field that reached the calculation empty, as text or infinite | fill in the named field with a number |
| «Modo de descarte desconhecido» (unknown first-flush mode) | mode other than 1, 2 or 3 | choose one of the three modes; for no first flush, enter a depth of zero |
| «Intervalo de descarte inválido» (invalid first-flush interval) | mode 3 with an interval below 1 day | enter the interval in whole days |
| «Nível de acionamento da motobomba negativo» (negative pump start level) | level below zero | correct it; zero means starting with the tank empty |

> The suppliable fraction is the most frequent message, and the rule that avoids it is a single
> one: where you type, a percentage from 0 to 100; where it is stored, a fraction from 0 to 1.
> Section {{n:5}} justifies the split. When the message appears, the value arrived as 40 in a place
> that stores 0.4 — typically a hand-edited parameter file or an automation call.

<!-- tabela: Suppliable fraction messages and the action for each one -->
| Message | What triggered it | What to do |
| :--- | :--- | :--- |
| «… parece estar em percentual» (… seems to be a percentage) | fraction between 1 and 100 in the file, in the weekly, monthly or daily vector, or in automation | enter 0.4 for 40% |
| «… fora de [0, 100]» (… outside [0, 100]) | negative percentage or above 100 on the screen, in the scenario table, in the spreadsheet or in `--share` | correct it; 40 means 40% |
| orange field, or the question «Simulate anyway?» | percentage between 0 and 1 | if you meant 40%, type 40; if you really meant less than 1%, confirm |

---

## Precipitation series

The program does not distinguish a dry day from a day without a record, and so it does not guess: a
gap in the series stops the calculation, saying where it is. Filling the gap, or trimming the series
to a period without gaps, is a decision for whoever conducts the study, and the decision must be
stated in the study.

<!-- tabela: Precipitation series error messages and the action for each one -->
| Message | Cause | What to do |
| :--- | :--- | :--- |
| «A série de precipitação está vazia» (the precipitation series is empty) | file with no numeric line | check that the file has a column of daily values, one per line |
| «… dia(s) sem valor numérico, o primeiro no dia N» (… day(s) without a numeric value, the first on day N) | record gap: empty line or text in the middle of the series | fill the gaps or trim the series, and declare the treatment |
| «… valor(es) negativo(s), o primeiro de X mm no dia N» (… negative value(s), the first of X mm on day N) | missing-data sentinel, such as −999 | treat it as a gap: fill or trim |

A header line before the data, such as «Date;Precipitation», is not an error: it is ignored and
reading starts at the first numeric line.

---

## Sweep

<!-- tabela: Volume sweep error messages -->
| Message | Cause | Solution |
| :--- | :--- | :--- |
| «O volume máximo da varredura deve ser finito e não negativo» (the maximum sweep volume must be finite and non-negative) | empty or negative field | enter the maximum volume in litres |
| «O passo de varredura deve ser finito e maior que zero» (the sweep step must be finite and greater than zero) | step zero or empty | enter the step; it will be rounded to the multiple of 250 L |

There is also a warning that is not an error and should not be mistaken for one: when the sweep step
is adjusted to the multiple of 250 L, or when the limit of forty volumes forces it to be widened, the
program records the adjustment and carries on normally. All that warning requires of the user is to
declare in the study the step actually used, not the step originally requested.

---

## Chlorination

<!-- tabela: Chlorination parameter error messages -->
| Message | Cause | Solution |
| :--- | :--- | :--- |
| «Pureza deve ficar em (0, 1]» (purity must be in (0, 1]) | purity entered as a percentage | enter 0.65 for 65%, not 65 |
| «A dose não pode ser negativa» (the dose cannot be negative) | dose below zero | correct it |
| «O fator de emissão não pode ser negativo» (the emission factor cannot be negative) | emission factor of the product below zero | correct it; the factor is per kilogram of commercial product |

---

## Economic analysis

<!-- tabela: Economic analysis error messages and the action for each one -->
| Message | Cause | Solution |
| :--- | :--- | :--- |
| «… deve ser um número finito e não negativo» (… must be a finite, non-negative number) | investment, tariff, cost, power or volume empty, negative or infinite | the message names the field; fill it in with a number equal to or greater than zero |
| «O período de análise deve ser um número inteiro de anos» (the analysis period must be a whole number of years) | fractional, zero or negative period | enter the period in whole years |
| «… deve ser um número finito e maior que -100%» (… must be a finite number greater than −100%) | adjustment, inflation or discount rate of −100% or less | check the sign of the rate |
| «… parece estar em percentual» (… seems to be a percentage) | annual rate entered as 5 in a function expecting a decimal fraction | enter 0.05 for 5% |

> **Unit of the rates.** In the interface and in the project file, every rate is entered as a
> percentage, with the unit next to the field: the minimum attractive rate of return and inflation
> in % per month (p.m.) or in % per year (p.a.), according to the button beside them, and the tariff
> adjustments in % per adjustment period, whose length in months is in the neighbouring field. The
> project stores the minimum attractive rate and inflation in % per month. The conversion between
> month and year is compound, (1 + i)^12 − 1, not a multiplication by twelve: 1% a month is
> equivalent to 12.68% a year. In automation, the annual calculation functions receive the rates as
> a decimal fraction, 0.05 for 5%, and reject a value that looks like a percentage instead of
> reinterpreting it.

---

## Multi-criteria decision

<!-- tabela: Multi-criteria decision error messages and the action for each one -->
| Message | Cause | Solution |
| :--- | :--- | :--- |
| «Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural) ou 8 pesos de critério TOPSIS» (enter 4 dimension weights (technical, economic, environmental, structural) or 8 TOPSIS criterion weights) | number of weights other than 3, 4, 7 or 8 | enter one weight per dimension or one per criterion; three weights from a project of version 0.1.0 are still accepted, and the structural dimension receives their mean |
| «O multicritério da versão 0.2.0 tem oito critérios em quatro eixos, e os sete valores do modelo anterior não correspondem a eles. Informe quatro pesos de eixo (técnico, econômico, ambiental, estrutural) ou oito pesos de critério.» (the multi-criteria analysis of version 0.2.0 has eight criteria in four dimensions, and the seven values of the previous model do not correspond to them; enter four dimension weights or eight criterion weights) | seven weights or seven criterion shares, from the model of version 0.1.0 | rewrite the weights as four dimension weights or eight criterion weights (section {{n:32}}); to reproduce a study made with version 0.1.0, use version 0.1.0 |
| «Informe 4 pesos de eixo (técnico, econômico, ambiental, estrutural).» (enter 4 dimension weights) | dimension weights of the wrong length where only dimension weights are accepted | enter four values |
| «Os pesos TOPSIS devem ser finitos e não negativos» (TOPSIS weights must be finite and non-negative) | empty or negative weight | correct it; a weight of zero is valid and excludes the criterion |
| «Ao menos um peso TOPSIS deve ser maior que zero» (at least one TOPSIS weight must be greater than zero) | all weights zero | give weight to at least one criterion |
| «Informe 8 partes, uma por critério TOPSIS (na ordem dos critérios).» (enter 8 shares, one per TOPSIS criterion, in the order of the criteria) | criterion shares with a number of values other than eight | enter eight shares in the order reliability, efficiency, net saving, LCOW, payback, CO₂, mass, overflow; the default is 1,1,1,1,1,1,1,1 |
| «As partes no eixo devem ser finitas e não negativas.» (criterion shares must be finite and non-negative) | empty or negative share | correct it; a share of zero is valid and removes the criterion from the calculation |
| «Ao menos um critério do eixo … deve ter parte maior que zero.» (at least one criterion of the … dimension must have a share greater than zero) | every criterion of a dimension with a share of zero | give a share to at least one criterion of the dimension named, or set the weight of that dimension to zero instead |
| «analysis.topsis_weights deve ser uma lista com quatro valores (eixos) ou oito (critérios)» (analysis.topsis_weights must be a list of four values, dimensions, or eight, criteria) | weights of the wrong length in the project file read by the command line | correct the list in the project file |
| «analysis.topsis_criterion_shares: …» | invalid criterion shares in the project file; the message continues with one of the share messages above | correct the list of eight shares in the project file |
| «O critério TOPSIS … da alternativa N não é finito» (TOPSIS criterion … of alternative N is not finite) | undefined indicator in an alternative, typically a payback with no return | check the alternative indicated before deciding |

The declarative study (section {{n:19}}) reports its own errors in English: `analise.pesos` must be four
non-negative numbers (technical, economic, environmental, structural) or eight (one per criterion) with
a positive sum, and `analise.partes_no_eixo` must be eight shares that pass the checks above.

---

## Pump set

<!-- tabela: Pump set parameter error messages -->
| Message | Cause | Solution |
| :--- | :--- | :--- |
| «Rendimento deve ficar em (0, 1]» (efficiency must be in (0, 1]) | efficiency as a percentage in the core | use 0.55 for 55% |
| «Rendimento do motor deve ficar em (0, 1]» (motor efficiency must be in (0, 1]) | likewise, in the motor field | leave it blank for the program to adopt its default efficiency table |

---

## Files

<!-- tabela: Error situations when reading and saving files -->
| Situation | What happens | What to do |
| :--- | :--- | :--- |
| unreadable rainfall series | reading stops with a message | check the format: one reading per line, in mm, single column |
| `.triton` file with invalid JSON | opening stops | the file may be truncated; use the backup copy |
| section missing in the file | the fields fall back to the class default | expected when opening a file from an earlier version; review the corresponding tab |
| no climate database in this edition | the tab offers only a file of your own | supply the series as described in section {{n:2}} |

---

## Warnings that do not stop the calculation

The warnings gathered in this table do not prevent the calculation and do not indicate a defect: they
are remarks the program makes about the conditions under which the result was produced. All of them
need to be carried over into the text of the study, because all of them affect the interpretation of
the number and none of them is evident in the result on its own.

<!-- tabela: Warnings that do not stop the calculation and must be stated in the study -->
| Warning | What it means |
| :--- | :--- |
| non-residential building type with a residential tariff | the economic result is **underestimated**; see section {{n:18}} |
| the target class recommends fine filtration and it was declined | decision recorded in the report |
| emission factor with a screening label | the factor has no primary source; declare it |
| incomplete tariff structure | the structure typed in has a gap; check it against the published tariff |
| sweep step adjusted | the effective step differs from the one requested |
| price extrapolation with low R² | the volume is outside the price table and the regression is not reliable |

---

## When the result looks wrong

Before suspecting a defect in the program, three checks resolve most of the cases in which the
result is surprising, and each one corresponds to an input error with a signature of its own.

When the **potential comes out higher than expected**, the immediate suspect is the suppliable
fraction: it is the ceiling of the whole result, and a too generous fraction inflates everything
that comes after without anything in the report revealing the origin.

When the **potential comes out much lower**, check the first-flush depth. The corresponding mistake
is described in section {{n:33.3}}, and consists in entering the first flush in litres when the
field asks for millimetres — which discards, typically, the whole rain of every day.

When the **payback comes out absurd**, in either direction, check the tariff regime (allowance, minimum charge, availability charge).
It is the most frequent cause of an implausible economic result, and section {{n:16}} gives the test
that identifies it in two minutes.

It is also worth going through the four input steps before accepting any result. The sidebar marks
those still pending, and checking four screens takes less time than discovering the mistake after
the report has been issued.
