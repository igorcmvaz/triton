# 26. Índices pluviométricos

> Este capítulo traz a equação de cada um dos nove índices que o programa calcula, e
> declara três divergências em relação ao padrão ETCCDI.

Os índices não entram no balanço hídrico. Servem para **caracterizar a série** — e
uma caracterização honesta é o que permite comparar estudos de cidades diferentes.

---

## 26.1. Os nove índices

Com `P_i` a precipitação do dia `i`, e «dia úmido» definido como `P_i ≥ 1 mm`:

| # | Índice | Definição | Unidade |
| :-- | :--- | :--- | :--- |
| 1 | **PRCPTOT** | `Σ P_i` sobre os dias úmidos do ano | mm |
| 2 | **R95p** | `Σ P_i` para `P_i > q95` | mm |
| 3 | **RX1day** | `max(P_i)` no ano | mm |
| 4 | **RX5day** | máximo da soma móvel de cinco dias | mm |
| 5 | **SDII** | `PRCPTOT ÷ número de dias úmidos` | mm/dia |
| 6 | **R20mm** | contagem de dias com `P_i ≥ 20 mm` | dias |
| 7 | **CDD** | maior sequência consecutiva de dias secos | dias |
| 8 | **CWD** | maior sequência consecutiva de dias úmidos | dias |
| 9 | **SI** | índice de sazonalidade de Walsh e Lawler | adimensional |

O índice de sazonalidade:

```
SI = (1/R) · Σ |X_m − R/12|      para m = 1..12
```

em que `X_m` é o total do mês `m` e `R` o total anual. Vale zero quando a chuva é
perfeitamente uniforme ao longo do ano e tende a 1,83 quando toda a chuva cai num
mês só.

O SI é o índice que mais importa para aproveitamento pluvial, e o guia 14 mostra
por quê: é a distribuição, e não o total, que decide o rendimento do sistema.

---

## 26.2. Três divergências que precisam ser declaradas

O programa chama o conjunto de «ETCCDI mais sazonalidade», e a precisão da expressão
importa.

**Primeira: o conjunto não é ETCCDI puro.** O índice de sazonalidade é de Walsh e
Lawler, e não pertence ao conjunto do *Expert Team on Climate Change Detection and
Indices*. Em compensação, o **R10mm**, que é ETCCDI, **não** está implementado.

Oito dos nove índices são ETCCDI; o nono não é; e falta um que seria.

**Segunda: o período-base do percentil.** O R95p exige um percentil 95 dos dias
úmidos. O ETCCDI define o período-base fixo de 1961 a 1990. O programa calcula o
percentil sobre **toda a série carregada**.

A consequência é que o R95p de duas séries de comprimentos diferentes **não é
diretamente comparável**, porque o limiar de cada uma é próprio. Para comparação
estrita com literatura ETCCDI, recorte a série no período-base.

O programa calcula o percentil **apenas sobre os dias úmidos**, o que está correto:
incluir dias secos deslocaria o percentil para baixo em séries sazonais.

**Terceira: as janelas incompletas do RX5day.** A soma móvel de cinco dias usa
janelas parciais no início de cada ano, de modo que as primeiras janelas têm de um a
quatro dias. O efeito é pequeno e sempre no sentido de subestimar o RX5day dos
primeiros dias do ano.

---

## 26.3. Para que servem no estudo

**Caracterizar a série** no método do artigo. PRCPTOT, SDII e SI descrevem o regime
melhor que a média anual sozinha.

**Explicar o resultado.** Um CDD alto explica um sistema de baixo desempenho apesar
de chuva abundante — é o caso de Brasília no guia 14.

**Comparar cenários climáticos.** Entre a série histórica e a projetada, o que
costuma mudar primeiro é o SDII e o CDD, e não o PRCPTOT. Reportar só o total anual
esconde a mudança que mais afeta o sistema.

---

## 26.4. O que os índices não fazem

Não entram no balanço. Não alteram o dimensionamento. Não substituem a simulação
diária — que é justamente o argumento do programa contra os métodos por valores
médios.

Um índice é um resumo. O balanço usa a série inteira.
