# Índices pluviométricos

> Esta seção traz a equação de cada um dos nove índices que o programa calcula, e
> declara três divergências em relação ao padrão ETCCDI.

Os índices pluviométricos não participam do balanço hídrico e não alteram nenhum
resultado de simulação. Sua função é caracterizar a série de precipitação — e
uma caracterização honesta é o que permite comparar estudos de cidades diferentes.

---

## Os nove índices

Os índices são calculados **ano a ano** sobre a série carregada, e o programa reporta a
média e a dispersão do conjunto de anos. Em toda esta seção, `P_i` designa a precipitação
do dia `i` do ano, e um **dia úmido** é aquele em que `P_i ≥ 1 mm` — convenção do ETCCDI,
adotada porque lâminas abaixo de um milímetro são da ordem do erro de medição dos
pluviômetros convencionais.

### Precipitação total anual, PRCPTOT

Soma da precipitação de todos os dias úmidos do ano. Difere do total anual bruto por
excluir os dias de lâmina desprezível, o que evita que ruído de instrumento se acumule
no total.

```equacao:prcptot
PRCPTOT = Σ P_i , para P_i ≥ 1 mm
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `PRCPTOT` | precipitação total dos dias úmidos do ano | mm |
| `P_i` | precipitação do dia `i` | mm |
| `Σ` | somatório sobre os dias do ano que satisfazem a condição | — |

### Precipitação em dias muito úmidos, R95p

Soma da precipitação dos dias cuja lâmina supera o percentil 95 dos dias úmidos. Mede
quanto do total anual chega nos eventos extremos, e é o índice mais diretamente ligado ao
extravasamento de cisternas.

```equacao:r95p
R95p = Σ P_i , para P_i > q_95
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `R95p` | precipitação acumulada nos dias muito úmidos | mm |
| `P_i` | precipitação do dia `i` | mm |
| `q_95` | percentil 95 da precipitação dos dias úmidos da série | mm |

### Máxima precipitação em um dia, RX1day

O maior valor diário registrado no ano. É o índice que dimensiona o extravasor e a
calha, e não o reservatório.

```equacao:rx1day
RX1day = max ( P_i )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `RX1day` | maior precipitação diária do ano | mm |
| `P_i` | precipitação do dia `i` | mm |
| `max` | valor máximo sobre todos os dias do ano | — |

### Máxima precipitação em cinco dias, RX5day

O maior acumulado de cinco dias consecutivos no ano. Importa ao aproveitamento pluvial
mais que o RX1day, porque um reservatório enche ao longo de um evento prolongado e não
apenas no pico diário.

```equacao:rx5day
RX5day = max ( Σ P_j ) , para j de i a i + 4
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `RX5day` | maior acumulado de cinco dias consecutivos no ano | mm |
| `P_j` | precipitação do dia `j` da janela | mm |
| `i` | primeiro dia de cada janela de cinco dias | — |
| `max` | valor máximo sobre todas as janelas do ano | — |

### Índice simples de intensidade diária, SDII

Precipitação média dos dias úmidos. Separa dois regimes que o total anual confunde: muita
chuva em poucos dias e pouca chuva em muitos dias podem produzir o mesmo PRCPTOT e SDII
bem diferentes.

```equacao:sdii
SDII = PRCPTOT ÷ n_úmidos
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `SDII` | intensidade média dos dias úmidos | mm/dia |
| `PRCPTOT` | precipitação total dos dias úmidos, da Equação {{eq:prcptot}} | mm |
| `n_úmidos` | número de dias úmidos do ano | dia |

### Dias de precipitação intensa, R20mm

Contagem dos dias em que a lâmina atinge ou supera vinte milímetros. Num sistema de
aproveitamento pluvial, esses são tipicamente os dias de extravasamento.

```equacao:r20mm
R20mm = # { i : P_i ≥ 20 mm }
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `R20mm` | número de dias com precipitação intensa no ano | dia |
| `P_i` | precipitação do dia `i` | mm |
| `# { }` | contagem dos dias que satisfazem a condição | — |

### Dias secos consecutivos, CDD

Maior sequência de dias consecutivos com precipitação abaixo de um milímetro. ==É o
índice que melhor prevê o desempenho de um sistema pluvial,== porque a estiagem mais
longa é o que esvazia a cisterna.

```equacao:cdd
CDD = max ( L ) , com P_i < 1 mm em toda a sequência L
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CDD` | maior sequência de dias secos consecutivos no ano | dia |
| `L` | comprimento de uma sequência de dias secos consecutivos | dia |
| `P_i` | precipitação do dia `i` | mm |

### Dias úmidos consecutivos, CWD

Maior sequência de dias consecutivos com precipitação igual ou superior a um milímetro.
Caracteriza a persistência da chuva, e sequências longas favorecem o enchimento completo
do reservatório.

```equacao:cwd
CWD = max ( L ) , com P_i ≥ 1 mm em toda a sequência L
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CWD` | maior sequência de dias úmidos consecutivos no ano | dia |
| `L` | comprimento de uma sequência de dias úmidos consecutivos | dia |
| `P_i` | precipitação do dia `i` | mm |

### Índice de sazonalidade, SI

Mede o afastamento entre a distribuição mensal real da chuva e a distribuição
perfeitamente uniforme ao longo do ano. Diferentemente dos oito anteriores, não pertence
ao conjunto ETCCDI: foi proposto por Walsh e Lawler em 1981.

```equacao:sazonalidade
SI = ( 1 ÷ R ) × Σ | X_m − R ÷ 12 |
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `SI` | índice de sazonalidade de Walsh e Lawler | adimensional |
| `R` | precipitação total do ano | mm |
| `X_m` | precipitação total do mês `m`, com `m` de 1 a 12 | mm |
| `R ÷ 12` | precipitação mensal que haveria se a chuva fosse uniforme | mm |
| `Σ` | somatório sobre os doze meses do ano | — |
| `\| \|` | valor absoluto da diferença | — |

O índice da Equação {{eq:sazonalidade}} vale zero quando todos os meses recebem a mesma
lâmina e tende a 1,83 quando toda a chuva do ano cai num único mês. Entre esses extremos,
a leitura usual classifica valores abaixo de 0,40 como regime equatorial, de 0,40 a 0,79
como estações úmida e seca pouco marcadas, e acima de 1,20 como regime de estação seca
longa.

O índice de sazonalidade é o que mais importa ao aproveitamento pluvial, e a seção
{{n:14}} mostra por quê: é a distribuição da chuva ao longo do ano, e não o total
precipitado, que decide o rendimento do sistema.

---

## Três divergências que precisam ser declaradas

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

## Para que servem no estudo

**Caracterizar a série** no método do artigo. PRCPTOT, SDII e SI descrevem o regime
melhor que a média anual sozinha.

**Explicar o resultado.** Um CDD alto explica um sistema de baixo desempenho apesar
de chuva abundante — é o caso de Brasília na seção {{n:14}}.

**Comparar cenários climáticos.** Entre a série histórica e a projetada, o que
costuma mudar primeiro é o SDII e o CDD, e não o PRCPTOT. Reportar só o total anual
esconde a mudança que mais afeta o sistema.

---

## O que os índices não fazem

Não entram no balanço. Não alteram o dimensionamento. Não substituem a simulação
diária — que é justamente o argumento do programa contra os métodos por valores
médios.

Um índice é um resumo. O balanço usa a série inteira.
