# Rainfall indices

> This section gives the equation of each of the nine indices the program calculates, and
> declares three divergences from the ETCCDI standard.

The rainfall indices do not take part in the water balance and do not change any simulation
result. Their role is to characterise the precipitation series — and an honest
characterisation is what makes it possible to compare studies of different cities.

---

## The nine indices

The indices are calculated **year by year** over the loaded series, and the program reports the
mean and the spread of the set of years. Throughout this section, `P_i` designates the
precipitation of day `i` of the year, and a **wet day** is one on which `P_i ≥ 1 mm` — an ETCCDI
convention, adopted because depths below one millimetre are of the order of the measurement
error of conventional rain gauges.

### Total annual precipitation, PRCPTOT

Sum of the precipitation of all the wet days of the year. It differs from the gross annual total
by excluding days of negligible depth, which keeps instrument noise from accumulating in the
total.

```equacao:prcptot
PRCPTOT = Σ P_i , para P_i ≥ 1 mm
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `PRCPTOT` | total precipitation of the wet days of the year | mm |
| `P_i` | precipitation of day `i` | mm |
| `Σ` | sum over the days of the year that meet the condition | — |

### Precipitation on very wet days, R95p

Sum of the precipitation of the days whose depth exceeds the 95th percentile of the wet days. It
measures how much of the annual total arrives in extreme events, and it is the index most directly
linked to cistern overflow.

```equacao:r95p
R95p = Σ P_i , para P_i > q_95
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `R95p` | precipitation accumulated on very wet days | mm |
| `P_i` | precipitation of day `i` | mm |
| `q_95` | 95th percentile of the precipitation of the wet days of the series | mm |

### Maximum one-day precipitation, RX1day

The largest daily value recorded in the year. It is the index that sizes the overflow and the
gutter, not the tank.

```equacao:rx1day
RX1day = max ( P_i )
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `RX1day` | largest daily precipitation of the year | mm |
| `P_i` | precipitation of day `i` | mm |
| `max` | maximum value over all the days of the year | — |

### Maximum five-day precipitation, RX5day

The largest five-consecutive-day total of the year. It matters more to rainwater harvesting than
RX1day, because a tank fills over a prolonged event and not only at the daily peak.

```equacao:rx5day
RX5day = max ( Σ P_j ) , para j de i a i + 4
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `RX5day` | largest five-consecutive-day total of the year | mm |
| `P_j` | precipitation of day `j` of the window | mm |
| `i` | first day of each five-day window | — |
| `max` | maximum value over all the windows of the year | — |

### Simple daily intensity index, SDII

Mean precipitation of the wet days. It separates two regimes the annual total confuses: much rain
on few days and little rain on many days can produce the same PRCPTOT and very different SDII.

```equacao:sdii
SDII = PRCPTOT ÷ n_úmidos
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `SDII` | mean intensity of the wet days | mm/day |
| `PRCPTOT` | total precipitation of the wet days, from Equation {{eq:prcptot}} | mm |
| `n_úmidos` | number of wet days of the year | day |

### Days of heavy precipitation, R20mm

Count of the days on which the depth reaches or exceeds twenty millimetres. In a rainwater
harvesting system, these are typically the overflow days.

```equacao:r20mm
R20mm = # { i : P_i ≥ 20 mm }
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `R20mm` | number of days with heavy precipitation in the year | day |
| `P_i` | precipitation of day `i` | mm |
| `# { }` | count of the days that meet the condition | — |

### Consecutive dry days, CDD

Longest sequence of consecutive days with precipitation below one millimetre. ==It is the index
that best predicts the performance of a rainwater system,== because the longest dry spell is what
empties the cistern.

```equacao:cdd
CDD = max ( L ) , com P_i < 1 mm em toda a sequência L
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `CDD` | longest sequence of consecutive dry days in the year | day |
| `L` | length of a sequence of consecutive dry days | day |
| `P_i` | precipitation of day `i` | mm |

### Consecutive wet days, CWD

Longest sequence of consecutive days with precipitation equal to or above one millimetre. It
characterises the persistence of rain, and long sequences favour the complete filling of the tank.

```equacao:cwd
CWD = max ( L ) , com P_i ≥ 1 mm em toda a sequência L
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `CWD` | longest sequence of consecutive wet days in the year | day |
| `L` | length of a sequence of consecutive wet days | day |
| `P_i` | precipitation of day `i` | mm |

### Seasonality index, SI

It measures the departure of the actual monthly distribution of the rain from a perfectly uniform
distribution over the year. Unlike the previous eight, it does not belong to the ETCCDI set: it
was proposed by Walsh and Lawler in 1981.

```equacao:sazonalidade
SI = ( 1 ÷ R ) × Σ | X_m − R ÷ 12 |
```

| Symbol | Meaning | Unit |
| :--- | :--- | :--- |
| `SI` | Walsh and Lawler seasonality index | dimensionless |
| `R` | total precipitation of the year | mm |
| `X_m` | total precipitation of month `m`, with `m` from 1 to 12 | mm |
| `R ÷ 12` | monthly precipitation there would be if the rain were uniform | mm |
| `Σ` | sum over the twelve months of the year | — |
| `\| \|` | absolute value of the difference | — |

The index of Equation {{eq:sazonalidade}} is zero when all months receive the same depth and tends
to 1.83 when all the rain of the year falls in a single month. Between these extremes, Walsh and
Lawler (1981) classify the regime as very equable (below 0.20), equable with a definite wetter
season (0.20 to 0.39), rather seasonal with a short drier season (0.40 to 0.59), seasonal (0.60 to
0.79), markedly seasonal with a long drier season (0.80 to 0.99), most rain in three months or
less (1.00 to 1.19) and extreme (1.20 or more).

The seasonality index is the one that matters most to rainwater harvesting, and section {{n:14}}
shows why: it is the distribution of rain over the year, not the total precipitated, that decides
the yield of the system.

---

The nine indices remain abstract while they stay in table form, and {{fig:fig16_indices}} places
them over one year of the series. Placed over a real year of series, each one points to an
identifiable stretch of the record: the most intense day, the days above the threshold, the
longest dry spell, the accumulated total.

![The indices marked over one year of series](../figuras/fig16_indices.png)

*Figure 99 — Four of the nine indices marked over one year of the New York series: PRCPTOT and SDII, at the top; RX1day, the largest daily value of the year; CDD, the longest sequence of dry days, in the shaded band; and R20mm, the days with 20 mm or more, marked at the bottom.*

Seasonality is the index least like the others, because it describes neither intensity nor
frequency: it describes how much the rain of the year concentrates in part of it. It is also the
index that most separates cities with similar annual totals, and the one that best predicts
whether a tank will have to get through a long dry spell ({{fig:fig17_sazonalidade}}).

![The seasonality index in the three example cities](../figuras/fig17_sazonalidade.png)

*Figure 99 — Walsh and Lawler (1981) seasonality index in the three example cities (New York, London and Cape Town), with the classes of the index in the background and the mean annual precipitation under the name of each city. High annual precipitation and an even distribution over the year are independent properties.*

---

## Three divergences that must be declared

The program calls the set «ETCCDI plus seasonality», and the precision of the expression matters.

**First: the set is not pure ETCCDI.** The seasonality index is Walsh and Lawler's, and does not
belong to the set of the *Expert Team on Climate Change Detection and Indices*. Conversely,
**R10mm**, which is ETCCDI, is **not** implemented.

Eight of the nine indices are ETCCDI; the ninth is not; and one that would be is missing.

**Second: the base period of the percentile.** R95p requires a 95th percentile of the wet days.
ETCCDI defines the fixed base period of 1961 to 1990. The program calculates the percentile over
**the whole loaded series**.

The consequence is that the R95p of two series of different lengths is **not directly
comparable**, because each one has its own threshold. For strict comparison with ETCCDI
literature, trim the series to the base period.

The program calculates the percentile **only over the wet days**, which is correct: including dry
days would shift the percentile down in seasonal series.

**Third: the incomplete RX5day windows.** The five-day moving sum uses partial windows at the start
of each year, so that the first windows have one to four days. The effect is small and always in
the direction of underestimating the RX5day of the first days of the year.

---

The program's indices tab presents each indicator year by year: the total annual precipitation
({{fig:fig53_programa_prcptot}}) and the longest sequences of dry and wet days
({{fig:fig54_programa_cdd_cwd}}).

![The total annual precipitation, year by year, on the program's screen](../figuras/fig53_programa_prcptot.png)

*Figure 99 — Total annual precipitation (PRCPTOT) of the New York series, with the mean of the period as a dashed line, in the indices tab. Figure generated by the program itself.*

---
![The dry spells and the wet sequences, year by year](../figuras/fig54_programa_cdd_cwd.png)

*Figure 99 — Longest annual sequence of dry days (CDD) and of wet days (CWD) of the New York series, in the indices tab. They are the two indices most directly linked to the tank volume the rainfall regime requires. Figure generated by the program itself.*

---
## What they are for in the study

**Characterising the series** in the method of the paper. PRCPTOT, SDII and SI describe the regime
better than the annual mean alone.

**Explaining the result.** A high CDD, or a strongly seasonal regime, explains a performance below what the annual total suggests: in section {{n:14}}, Cape Town receives rain on only 28%
of the days, its wettest month has 8.3 times the rain of its driest, and the same house yields
14.52% there against 26.83% in New York.

**Comparing climate scenarios.** Between the historical and the projected series, what usually
changes first is SDII and CDD, not PRCPTOT. Reporting only the annual total hides the change that
most affects the system.

---

## What the indices do not do

They do not enter the balance. They do not change the sizing. They do not replace the daily
simulation — which is precisely the program's argument against methods based on mean values.

An index is a summary. The balance uses the whole series.
