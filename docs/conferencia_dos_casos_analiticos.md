# Conferência das derivações analíticas

**Este documento pede revisão humana.** Os casos analíticos verificam o motor contra
contas feitas à mão. Se uma conta estiver errada, o teste passa a exigir do motor o
resultado errado — e a exigi-lo para sempre, com aparência de rigor.

As nove derivações estão reproduzidas abaixo em forma de conferência. Cada uma é
independente e verificável com papel. Implementação em
[`tests/invariants/test_casos_analiticos.py`](../tests/invariants/test_casos_analiticos.py).

> **Precedente.** Na primeira execução, o caso mensal reprovou: a soma das doze parcelas
> fora anotada como 237.400 L quando o correto era 238.400 L. O erro estava na derivação,
> não no motor. Foi corrigido, mas serve de aviso — estas contas precisam de um segundo
> par de olhos.

---

## Convenções do motor usadas em todas as derivações

| Grandeza | Regra |
| :--- | :--- |
| Captação do dia | `V_cap = P_ef × A × C` litros (1 mm sobre 1 m² = 1 L) |
| Chuva efetiva, modo 1 | `P_ef = max(0, P − df)` em todo dia com chuva |
| Ordem das operações | extravasa **antes** de consumir (*yield after spill*) |
| Consumo pluvial do dia | `min(demanda pluvial, volume disponível na cisterna)` |
| Demanda pluvial | `demanda total × fração pluvial` |
| Economia (%) | `consumo pluvial acumulado ÷ demanda total acumulada × 100` |

---

## 1. Regime limitado pela oferta

**Entradas** P = 2 mm/dia · A = 50 m² · C = 1,0 · descarte 0 · demanda 1.000 L/dia ·
fração pluvial 0,5 · cisterna 10.000 L · 365 dias

```
captação diária = 2 × 50 × 1,0 = 100 L
demanda pluvial = 1.000 × 0,5  = 500 L
100 < 500  →  consome-se tudo que entra; o estoque volta a zero todo dia
```

| Saída | Valor esperado |
| :--- | ---: |
| Consumo pluvial | 100 L/dia |
| Consumo potável | 1.000 − 100 = 900 L/dia |
| Extravasamento | 0 |
| Economia | 100 ÷ 1.000 = **10,0 %** |
| Dias com atendimento parcial | 100 % (pois 0 < 100 < 500) |

---

## 2. Enchimento e extravasamento

**Entradas** P = 10 mm/dia · A = 100 m² · C = 1,0 · descarte 0 · demanda 1.000 L/dia ·
fração 0,5 · **cisterna 5.000 L** · 365 dias

```
captação H = 10 × 100 × 1,0 = 1.000 L/dia
demanda  D = 500 L/dia          excedente H − D = 500 L/dia

Estoque ao fim do dia k, enquanto não extravasa: 500·k
  dia 9 : estoque inicial 4.000, +1.000 = 5.000 → NÃO excede 5.000, sem extravasar
          fecha em 5.000 − 500 = 4.500
  dia 10: estoque inicial 4.500, +1.000 = 5.500 → excede: extravasa 500
          fecha em 4.500, e assim permanece
```

| Grandeza | Conta | Valor |
| :--- | :--- | ---: |
| Dias com extravasamento | 365 − 9 | 356 |
| Extravasamento total | 356 × 500 | 178.000 L |
| Consumo pluvial total | 365 × 500 | 182.500 L |
| Captação total | 365 × 1.000 | 365.000 L |

**Conferência do balanço:** 182.500 + 178.000 + 4.500 (estoque final) = 365.000 ✓

Economia = 182.500 ÷ 365.000 = **50,0 %** · atendimento pleno em 100 % dos dias.

> O ponto delicado é o dia 9: como o extravasamento antecede o consumo, e 5.000 **não
> excede** 5.000, aquele dia ainda não extravasa. Um leitor apressado escreveria 355 dias.

---

## 3. Descarte subtrai a lâmina

**Entradas** P = 10 mm/dia · descarte 3 mm · modo 1 · A = 50 m² · C = 1,0 ·
demanda pluvial 1.000 L/dia (mantém o regime limitado pela oferta)

```
sem descarte: P_ef = 10 mm → 10 × 50 = 500 L/dia
com descarte: P_ef =  7 mm →  7 × 50 = 350 L/dia
razão = 7 ÷ 10 = 0,7 exatamente
```

**Sob a regra do Netuno 4** (limiar), 10 mm ≥ 3 mm implicaria captar os 10 mm integrais e
a razão seria 1,0. Este caso distingue as duas semânticas numericamente.

---

## 4. Descarte periódico (modo 3)

**Entradas** P = 10 mm todos os dias · descarte 4 mm · intervalo 5 dias · A = 50 m² ·
C = 1,0 · 100 dias

```
o motor descarta quando (dia − último descarte) ≥ 5, partindo de um último
descarte muito antigo → descarta nos dias 0, 5, 10, … 95 = 20 dias em 100

20 dias com descarte : (10 − 4) × 50 = 300 L   → 20 × 300 =  6.000 L
80 dias sem descarte :  10      × 50 = 500 L   → 80 × 500 = 40.000 L
captação total = 46.000 L em 100 dias → média 460 L/dia
```

Com demanda pluvial de 1.000 L/dia o regime é limitado pela oferta, logo
**consumo médio = 460 L/dia**.

---

## 5. Descarte após estiagem (modo 2)

**Entradas** padrão de 4 dias `[10, 10, 0, 0]` mm repetido 25 vezes (100 dias) ·
descarte 4 mm · A = 50 m² · C = 1,0

```
o motor descarta quando chove e a véspera teve menos de 1 mm
  1º dia do ciclo: véspera seca  → descarta   P_ef =  6 mm →  300 L
  2º dia do ciclo: véspera 10 mm → não        P_ef = 10 mm →  500 L
  3º e 4º: sem chuva                                       →    0 L

captação por ciclo = 800 L em 4 dias
total = 25 × 800 = 20.000 L → média 200 L/dia
```

O dia 0 não tem véspera; o motor a trata como 0 mm, e ele recebe descarte — coerente com
o padrão.

---

## 6. Modulação semanal

**Entradas** padrão de segunda a domingo `[100, 200, 300, 400, 500, 600, 700]` L/dia ·
364 dias = 52 semanas exatas · fração 0,5 · oferta abundante

```
soma do padrão = 2.800 L por semana
demanda total  = 52 × 2.800 = 145.600 L
```

Em 52 semanas exatas cada dia da semana ocorre 52 vezes, **qualquer que seja o dia
inicial** — por isso o resultado não depende de 01/01/1980 ser terça-feira.

Consumo pluvial = 0,5 × 145.600 = **72.800 L** · economia **50,0 %**.

---

## 7. Modulação mensal *(o caso que já falhou uma vez)*

**Entradas** demanda de 100 L/dia em janeiro crescendo até 1.200 em dezembro ·
ano de **1980, bissexto** · início em 01/01 · 366 dias · fração 0,5

| Mês | Dias | L/dia | Parcela |
| :--- | ---: | ---: | ---: |
| Janeiro | 31 | 100 | 3.100 |
| Fevereiro | **29** | 200 | 5.800 |
| Março | 31 | 300 | 9.300 |
| Abril | 30 | 400 | 12.000 |
| Maio | 31 | 500 | 15.500 |
| Junho | 30 | 600 | 18.000 |
| Julho | 31 | 700 | 21.700 |
| Agosto | 31 | 800 | 24.800 |
| Setembro | 30 | 900 | 27.000 |
| Outubro | 31 | 1.000 | 31.000 |
| Novembro | 30 | 1.100 | 33.000 |
| Dezembro | 31 | 1.200 | 37.200 |
| **Total** | **366** | — | **238.400** |

Consumo pluvial = 238.400 ÷ 2 = **119.200 L** · média **325,683 L/dia** · economia 50,0 %.

> Escolheu-se 1980 justamente porque é bissexto: um motor que tratasse todos os meses
> como tendo 30 dias, ou que ignorasse o 29 de fevereiro, produziria outro total.

---

## 8. Supressão de irrigação

**Entradas** padrão alternado `[5, 0]` mm ao longo de 100 dias · limiar de supressão
2 mm · irrigação 150 L/dia

```
dias com chuva ≥ 2 mm = 50 (os pares do padrão)
→ irrigação suprimida em 50 dias, ativa nos outros 50
volume suprimido = 50 × 150 = 7.500 L no período
```

---

## 9. Reservatório superior amplo

**Entradas** P = 3 mm/dia · A = 100 m² · C = 1,0 → 300 L/dia captados ·
demanda pluvial 500 L/dia · reservatório superior 10.000 L, limiar de recalque 0

O recalque transfere água entre reservatórios: não é entrada nem saída do sistema. Se o
reservatório superior nunca restringe o bombeamento, o consumo deve ser **idêntico** ao
do arranjo com reservatório único — 300 L/dia nos dois casos.

---

## O que revisar

Ao conferir, vale prestar atenção a três pontos onde é fácil errar:

1. **O dia do enchimento no caso 2.** Extravasar antes de consumir muda o dia em que o
   extravasamento começa.
2. **A soma das parcelas no caso 7.** Foi exatamente aí que a derivação falhou antes.
3. **A contagem dos dias de descarte nos casos 4 e 5.** Depende de como o motor trata o
   primeiro dia da série, que não tem véspera.

Se discordar de alguma conta, o teste correspondente é o lugar de registrar: a docstring
carrega a derivação, e alterá-la é alterar a afirmação sob verificação.
