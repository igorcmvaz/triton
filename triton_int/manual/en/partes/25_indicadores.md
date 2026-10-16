# Efficiency indicators

> This section formally defines each indicator the program reports, with its unit, and says
> **what each one does not measure**.

A misread indicator is worse than none, and those of this section are often confused in the
literature. The first two start from the same numerator — the rainwater actually consumed —
and differ only in the denominator: a small arithmetic difference and a large difference in
meaning, because each denominator asks a different question. The third is not a ratio between
volumes but a count of days, and it answers a question neither of the other two reaches: how
often the system can be counted on ({{fig:fig00g_indicadores}}).

![The three indicators and the denominator of each one](../figuras/fig00g_indicadores.png)

*Figure 99 — The three efficiency indicators and what each one counts. The saving potential and the volumetric reliability share the numerator and are related by the identity Epot = Rv × f, where f is the suppliable fraction; the time reliability counts days, not litres.*

---

## Potable water saving potential

The potable water saving potential is the program's central indicator and the one that appears
in the summary of any study. It expresses the fraction of the **total** consumption of the
building that rainwater managed to replace over the whole simulated series, not only of the part
rain could supply.

```equacao:potencial
Epot = ( Σ V_con,t ÷ Σ D_t ) × 100
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `Epot` | potable water saving potential | % |
| `V_con,t` | rainwater volume consumed on day `t` | L |
| `D_t` | total demand of the building on day `t` | L |
| `Σ` | sum over all the days of the simulated series | — |

The denominator of Equation {{eq:potencial}} is the **total** demand, and that choice is the
origin of the most common confusion when reading results. A system that fully met all the demand
assigned to it, without failing on a single day, would still show a saving potential equal to the
declared suppliable fraction, not one hundred per cent. The ceiling, therefore, is not a
limitation of the system: it is an arithmetic consequence of the definition of the indicator.

---

## Volumetric reliability

Volumetric reliability answers a different, complementary question: of the water the system
**should** supply, how much did it actually supply? The denominator here is the rainwater demand,
not the total demand.

```equacao:confiabilidade
Rv = ( Σ V_con,t ÷ Σ D_pl,t ) × 100
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `Rv` | volumetric reliability of the system | % |
| `V_con,t` | rainwater volume consumed on day `t` | L |
| `D_pl,t` | rainwater demand of day `t`, that is, the part rain can supply | L |
| `Σ` | sum over all the days of the simulated series | — |

Equations {{eq:potencial}} and {{eq:confiabilidade}} differ only in the denominator, and that
difference is enough for them to be related by an exact identity, useful as a quick check of any
result.

```equacao:relacao_indicadores
Epot = Rv × f
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `Epot` | potable water saving potential | % |
| `Rv` | volumetric reliability | % |
| `f` | fraction of the total demand suppliable by rainwater | dimensionless |

==A system with 93% reliability and a 28% suppliable fraction saves 26% of the total
consumption, and the three numbers say the same thing in three ways.== That is the case of the
New York tutorial with a 3,000 L cistern, the first simulation of section {{n:6}}: the saving
potential is 25.99%, and dividing by the suppliable fraction of 0.28 gives a volumetric
reliability of about 92.8%. Reporting only one of them, without declaring the suppliable
fraction adopted, makes the result impossible to compare with that of another study, and it is
the most frequent cause of improper comparisons in the literature of the field.

The literature uses different names for the same ratio. Fewkes and Butler (2000) call **water
saving efficiency** the quotient between the rainwater volume supplied and the demand the system
should meet, which is the volumetric reliability of this section. Other authors call efficiency
what here is saving potential; some standards call it the coverage rate. When comparing with
another work, check the denominator, not the name.

---

## Time reliability

Time reliability classifies each day of the series into one of three mutually exclusive classes,
according to the relation between the rainwater volume consumed and the day's rainwater demand,
defined in Equation {{eq:classificacao}}. The day is **full** when rainwater fully meets the
rainwater demand; **partial**, when it meets part of it and the mains supplies the rest; and
**none**, when the tank is empty and the mains supplies all the demand
({{fig:fig29_atendimento}}). The three percentages add up to 100%. The classification counts days,
not volume: a day on which one litre was missing to meet the demand is partial, not almost full,
and that is why time reliability does not convert directly into volume saved.

![The three supply classes of a day](../figuras/fig29_atendimento.png)

*Figure 99 — Daily supply classes: full (V_con,t = D_pl,t), partial (0 < V_con,t < D_pl,t) and none (V_con,t = 0). The filled height represents the fraction of the day's rainwater demand supplied by rainwater.*

Formally, the day is **full** when `V_con,t = D_pl,t`, with a tolerance of 10⁻⁵ L; **partial**
when `0 < V_con,t < D_pl,t`; and **none** when `V_con,t = 0`.


In the tutorial with a 3,000 L cistern, 91.9% of the days are full, 1.7% partial and 6.4% with no
supply. Notice that the time reliability, 91.9%, is lower than the volumetric one, about 92.8%.
There is no contradiction: partial days do not count as full, but they contribute volume, and it
is that water the volumetric reliability adds and the time reliability does not. The difference
between the two is therefore an indirect measure of how far the failure days are partial
failures. With a 4,000 L cistern the full days rise to 95.3%.

**What it measures:** how often the user can count on the system.

**What it does not measure:** volume. A system can have 95% full days and a low potential if the
rainwater demand is small, and the opposite also happens.

> Time reliability is the indicator that matters most for the **plumbing design**. Many days with
> no supply require a well-sized automatic backup supply, and the user notices the switching
> between the two sources.

---

## Overflow

```equacao:extravasamento_medio
V_ext,med = ( Σ V_ext,t ) ÷ n
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_ext,med` | mean daily overflow | L/day |
| `V_ext,t` | volume overflowed on day `t` | L |
| `n` | number of days of the simulated series | day |

**What it measures:** how small the cistern is relative to the rain events.

**What it does not measure:** waste. The water that overflows goes to the urban drainage, as it
would without the system. There is no loss compared with the no-system scenario — only an
opportunity not taken.

> The overflow **never reaches zero** in a real system. It tends to a floor that is the difference
> between what the roof collects and what the demand consumes, and in the tutorial the roof supplies 2.3 times
> the rainwater demand, so that the floor is a large share of the water collected. Anyone who wants flood retention needs a detention tank,
> which is another project with another logic.

---

## Efficiency of use of the collected water

The program does not print this indicator, but it follows directly from the previous ones and
helps to understand the overflow. It is the fraction of the water that reached the cistern, after
the first flush, that ended up consumed.

```equacao:uso_da_captacao
η_cap = ( Σ V_con,t ÷ Σ V_cap,t ) × 100
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `η_cap` | efficiency of use of the collected water | % |
| `V_con,t` | rainwater volume consumed on day `t` | L |
| `V_cap,t` | volume collected on day `t`, after the first flush | L |
| `Σ` | sum over all the days of the simulated series | — |

In the tutorial's 3,000 L cistern, the system consumes 57.0 m³ a year and overflows a mean of
150.8 L/day, about 55 m³ a year; the mass balance closes with what stays in the tank, which is
small. About half of the water that reached the cistern is therefore consumed. The number
explains why enlarging the cistern yields so little beyond a certain point: water is not
missing on the roof, **demand** to consume it is. The gross supply of the roof, 143 m³ a year,
is 2.3 times the rainwater demand of 61 m³ a year; when supply greatly exceeds the rainwater
demand, the efficiency of use of the collected water is necessarily low, whatever the volume.

---

## Duration and intensity of failures

The previous indicators say how much and how often the system fails, but not **how** it fails.
Hashimoto, Stedinger and Loucks (1982) proposed, for water resource systems in general, three
complementary criteria that are now used in rainwater harvesting too: **reliability**, which is
the probability of the system being in a satisfactory state; **resilience**, which measures how
quickly it recovers from a failure; and **vulnerability**, which measures the severity of failures
when they occur.

The program reports the first and not the other two, but both can be calculated from the detailed
daily series, exported to a spreadsheet: count the sequences of days that are not full and take
their mean duration, whose inverse is a measure of resilience; and take the mean shortfall on the
failure days as a fraction of the rainwater demand, a measure of vulnerability.

The design reading is direct. If the failures are long and almost total, the backup supply from the
mains must be automatic and sized for the full flow of the rainwater points of use, not just to top
up small shortfalls. The tutorial's days of no supply (6.4% with 3,000 L)
are of this kind: the cistern is empty, not slightly short.

---

## Annual volume saved

```equacao:volume_poupado
V_poup = ( V_con,med × 365.25 ) ÷ 1000
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_poup` | volume of potable water saved per year | m³/year |
| `V_con,med` | mean daily rainwater consumption | L/day |
| `365.25` | length of the mean year, including leap years (365.25) | day/year |
| `1000` | conversion from litres to cubic metres | L/m³ |

**What it measures:** the basis of calculation of the economic analysis and the life cycle
assessment.

> **In depth: the 365.25 is not carelessness.** The conversion uses the mean year, including leap
> years, because long series contain them. Using 365 would introduce a systematic bias of 0.07% —
> small, but for nothing.

---

## Marginal gain

The formal definition of the marginal gain, with the grid of volumes made explicit, is in
Equation {{eq:ganho_marginal}}, in section {{n:24}}.

Defined in section {{n:24}}. It is the indicator that decides the ideal volume, and it **only
exists in a sweep** — a single-volume simulation does not produce it.

---

## Unmet demand

```equacao:nao_atendida
V_nao,med = ( Σ V_nao,t ) ÷ n
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `V_nao,med` | mean daily demand met by no source | L/day |
| `V_nao,t` | unmet demand on day `t` | L |
| `n` | number of days of the simulated series | day |

The third part of the demand balance. It is zero in the default configuration and stops being zero
when the irrigation backup supply is off.

**Why it exists:** without it, the balance would close by construction, attributing to the mains
all the demand rain did not meet. Section {{n:23}} gives the details.

---

## Summary table

<!-- tabela: Summary of the indicators, with the denominator and the question each one answers -->
| Indicator | Unit | Denominator | Answers |
| :--- | :--- | :--- | :--- |
| saving potential | % | total demand | how much potable consumption falls |
| volumetric reliability | % | rainwater demand | how much of what was intended was supplied |
| full, partial, no-supply days | % | days of the series | how often it can be counted on |
| overflow | L/day | — | is the tank small? |
| volume saved | m³/year | — | basis of the money and the carbon |
| marginal gain | %/m³ | — | is it worth enlarging? |
| unmet demand | L/day | — | what nobody supplied |
