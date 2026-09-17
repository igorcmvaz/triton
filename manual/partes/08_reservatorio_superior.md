# Precisa de reservatório superior?

> Ao terminar esta seção você saberá responder a pergunta com número, e não com
> hábito. A resposta costuma surpreender.

O arranjo clássico do aproveitamento pluvial brasileiro emprega dois reservatórios: uma
cisterna enterrada, que recebe a água da cobertura, e uma caixa d'água elevada, que
alimenta os pontos de consumo por gravidade; entre as duas, uma motobomba faz o recalque.
O arranjo é tão difundido que quase todo projeto o adota sem examinar a razão, e esta
seção examina.

---

## Para que serve a caixa superior

==A caixa superior não serve para guardar mais água; serve para entregá-la.== A distinção
parece sutil e decide a análise inteira, porque tudo o que se segue depende de não
confundir capacidade de armazenamento com capacidade de distribuição.

A cisterna fica enterrada, e os pontos de consumo — bacia sanitária, tanque, torneira de
jardim — situam-se acima dela. Alguma coisa precisa vencer esse desnível, e há duas
maneiras de fazê-lo com bomba.

- **Pressurização direta.** Uma bomba pequena com pressostato liga sempre que se
  abre um ponto. Não há caixa superior.
- **Recalque para caixa elevada.** A bomba enche a caixa de tempos em tempos, e a
  gravidade faz o resto.

Quando a cisterna fica acima dos pontos de uso, há ainda uma terceira: **gravidade**,
sem bomba. A etapa **4. Reservatório & Custos** pergunta qual dos três arranjos o projeto
adota, e é essa resposta que define a energia e as motobombas no custo e no carbono.

<!-- tabela: Os três arranjos de abastecimento e o que cada um acrescenta ao projeto -->
| Arranjo | Energia calculada | Caixa superior e motobombas |
| :--- | :--- | :--- |
| recalque para caixa superior | volume recalcado, pela altura manométrica, mais as partidas | entram no custo e no carbono |
| pressurização direta | todo o volume pluvial consumido, pela pressão de trabalho | só as motobombas |
| gravidade | nenhuma | nenhuma |

Na pressurização direta, a pressão de trabalho padrão é de 18 m.c.a., a média da faixa
do pressostato de um pressurizador residencial de 1/4 CV, que liga a 12 e desliga a
24 m.c.a. Os acionamentos por dia saem dos moradores: 5,05 descargas e 0,37 ciclos de
máquina de lavar por pessoa por dia, segundo o levantamento de usos finais de Mayer et
al. (1999). Não se soma energia de partida, porque o pressostato liga quando o uso começa
e a bomba já entrega vazão útil.

O recalque para caixa elevada tem três vantagens práticas reais. A motobomba liga poucas vezes por
dia, em vez de dezenas, o que prolonga a vida do equipamento; a pressão nos pontos de
consumo é constante, porque decorre da altura da coluna d'água e não do funcionamento da
bomba; e existe reserva disponível durante uma falta de energia. ==Nenhuma dessas três
vantagens é economia de água,== e é justamente essa a confusão que a seção desfaz.

---

## A comparação justa

Comparar um sistema de 5.000 L sem caixa elevada com outro de 5.000 L mais 1.000 L de
caixa é uma armadilha metodológica, porque o segundo dispõe de mais armazenamento total e
venceria por essa razão, e não pelo arranjo. Para isolar o efeito do arranjo é preciso
manter constante o armazenamento: comparam-se, portanto, 6.000 L num único reservatório
contra 5.000 L embaixo mais 1.000 L em cima.

<!-- inclui: _tabelas/cap08_reservatorio_superior.md -->

Mantido o mesmo armazenamento, o arranjo com caixa elevada entrega cerca de um terço de
ponto percentual a menos de economia que o reservatório único. A diferença não é erro de
arredondamento, e tem uma causa: **a cisterna extravasa enquanto a caixa superior ainda
tem espaço**.

A chuva entra só pela cisterna, e o extravasamento é calculado nela antes do consumo do
dia. O recalque, porém, só acontece quando há consumo e a caixa superior desce abaixo do
limiar de acionamento. Assim, num dia chuvoso com a cisterna cheia, a água que excede os
5.000 L de baixo é perdida mesmo que a caixa de cima tenha centenas de litros livres. Um
reservatório único de 6.000 L guardaria essa água.

É também por isso que o limiar de acionamento maior rende mais: com ele, a bomba enche a
caixa mais cedo, a cisterna fica mais vazia quando a chuva chega, e extravasa menos. A
reserva abaixo do limiar não é imobilizada, porque é consumida logo depois de cada
recalque e quando a cisterna seca.

> **A caixa superior não aumenta a economia de água. Ela custa.** No nosso projeto,
> custa a caixa, custa a bomba, custa 10,7 kWh por ano de energia, e custa um terço
> de ponto de potencial em relação a um tanque único do mesmo volume total.
>
> Isso não a torna errada. Torna a decisão **hidráulica**, e não hídrica: adote-a se
> o projeto precisa de pressão por gravidade ou de reserva contra falta de energia,
> e não esperando que ela renda mais água.

---

## O limiar de acionamento

Se você adotar a caixa, há um parâmetro a ajustar: o volume de reserva que não se
consome, abaixo do qual a bomba é acionada.

<!-- inclui: _tabelas/cap08_limiar.md -->

Limiar maior significa **mais potencial e mais acionamentos**, pela razão acima. De 0 para 500 L, o
potencial sobe 0,19 ponto e os acionamentos quase dobram, de 87 para 167 por ano.

A troca é entre um ganho hídrico marginal e o desgaste da motobomba. Motobombas
residenciais suportam bem alguns acionamentos por dia; o que as mata é o
liga-desliga contínuo. Cento e sessenta e sete acionamentos por ano é menos de um a
cada dois dias, e nenhum dos valores da tabela chega perto de ser problema.

> **Onde o limiar importa de verdade** é em edificações com demanda concentrada, em
> que a caixa esvazia rápido. Aí ele pode passar de mil acionamentos por ano, e
> convém dimensionar a caixa em vez de mexer no limiar.

---

## A energia, e por que ela é pequena

Dez vírgula sete quilowatt-hora por ano. Sete reais e quarenta e cinco centavos.

Parece pouco demais, e vale entender por quê. Elevar um metro cúbico de água a doze
metros custa, em energia hidráulica, cerca de 0,033 kWh. Com o rendimento da bomba e
o do motor, e somadas as partidas da bomba, chega a cerca de 0,13 kWh por metro cúbico recalcado. Oitenta e três metros
cúbicos por ano dão os 10,7 quilowatt-hora da tabela.

Água é pesada, mas doze metros é pouco. É por isso que o custo energético do
aproveitamento pluvial é desprezível diante da economia na fatura de água e esgoto — e é por
isso também que o argumento de que «bombear água gasta mais energia do que
economiza» não se sustenta em edificação de pequeno porte.

> **Atenção à potência de placa.** O programa pede o rendimento **da bomba** e o
> rendimento **do motor** separadamente. A potência de placa é a potência mecânica
> no eixo, e o rendimento do motor é o que separa o que o eixo entrega do que o
> medidor registra. Em branco, o programa adota a Tabela 13 da ABNT NBR 17094-2:
> 60,5% para meio CV. A seção {{n:28}} detalha.

---

## A decisão do tutorial

**Adotamos recalque para uma caixa superior de 1.000 L, com limiar de 100 L.**

A decisão é hidráulica, e não hídrica. A caixa elevada dá pressão constante nos pontos
de uso sem depender da bomba a cada descarga, mantém água disponível durante uma falta de
energia e faz a motobomba partir 96 vezes por ano, em vez das cerca de oito mil partidas de um
pressurizador acionado a cada uso por quatro moradores. O preço é o que a tabela mostra: a caixa, as bombas,
10,7 kWh por ano e um terço de ponto de potencial frente a um tanque único de 6.000 L.

Em relação à cisterna sozinha de 5.000 L, o potencial sobe de 37,46% para 37,76%,
porque a caixa acrescenta 1.000 L de armazenamento. Daqui em diante, o custo, o carbono
e a decisão do tutorial incluem a caixa, as duas motobombas e a energia do recalque.

<!-- tabela: Estado do projeto do tutorial após a decisão sobre o reservatório superior -->
| Projeto até aqui | |
| :--- | ---: |
| volume do reservatório inferior | 5.000 L |
| arranjo | recalque para caixa superior |
| reservatório superior | 1.000 L, limiar de 100 L |
| potencial de economia | 37,76% |

Agora sabemos quanta água o sistema entrega. Falta saber **que água** é essa.
