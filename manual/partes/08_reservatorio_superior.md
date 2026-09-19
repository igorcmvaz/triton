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

Na pressurização direta, a etapa 4 pede o modelo do pressurizador, escolhido num
catálogo de seis modelos com curva vazão × pressão do fabricante, a pressão de trabalho
e a vazão do ponto de uso. O pressurizador liga a cada descarga, 5,05 por pessoa por dia
segundo o levantamento de usos finais de Mayer et al. (1999), e fica ligado enquanto a
caixa acoplada enche, no ritmo da boia. A energia é esse tempo vezes a potência
elétrica. No tutorial, o menor modelo do catálogo gastaria 40,5 kWh por ano, cinco vezes
os 7,7 kWh do recalque; a seção {{n:28}} explica por quê, e mostra que o modelo escolhido
pesa mais que a pressão.

O recalque para caixa elevada tem três vantagens práticas reais. A motobomba liga poucas vezes por
dia, em vez de dezenas, o que prolonga a vida do equipamento; a pressão nos pontos de
consumo é constante, porque decorre da altura da coluna d'água e não do funcionamento da
bomba; e existe reserva disponível durante uma falta de energia. ==Nenhuma dessas três
vantagens é economia de água,== e é justamente essa a confusão que a seção desfaz.

---

## A comparação justa

Comparar um sistema de 4.000 L sem caixa elevada com outro de 4.000 L mais 1.000 L de
caixa é uma armadilha metodológica, porque o segundo dispõe de mais armazenamento total e
venceria por essa razão, e não pelo arranjo. Para isolar o efeito do arranjo é preciso
manter constante o armazenamento: comparam-se, portanto, 5.000 L num único reservatório
contra 4.000 L embaixo mais 1.000 L em cima.

<!-- inclui: _tabelas/cap08_reservatorio_superior.md -->

Mantido o mesmo armazenamento, o arranjo com caixa elevada entrega cerca de um sexto de
ponto percentual a menos de economia que o reservatório único. A diferença não é erro de
arredondamento, e tem uma causa: **a cisterna extravasa enquanto a caixa superior ainda
tem espaço**.

A chuva entra só pela cisterna, e o extravasamento é calculado nela antes do consumo do
dia. O recalque, porém, só acontece quando há consumo e a caixa superior desce abaixo do
limiar de acionamento. Assim, num dia chuvoso com a cisterna cheia, a água que excede os
4.000 L de baixo é perdida mesmo que a caixa de cima tenha centenas de litros livres. Um
reservatório único de 5.000 L guardaria essa água.

É também por isso que o limiar de acionamento maior rende mais: com ele, a bomba enche a
caixa mais cedo, a cisterna fica mais vazia quando a chuva chega, e extravasa menos. A
reserva abaixo do limiar não é imobilizada, porque é consumida logo depois de cada
recalque e quando a cisterna seca.

> **A caixa superior não aumenta a economia de água. Ela custa.** No nosso projeto,
> custa a caixa, custa a bomba, custa 7,7 kWh por ano de energia, e custa um sexto
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
potencial sobe 0,15 ponto e os acionamentos quase dobram, de 62 para 121 por ano.

A troca é entre um ganho hídrico marginal e o desgaste da motobomba. Motobombas
residenciais suportam bem alguns acionamentos por dia; o que as mata é o
liga-desliga contínuo. Cento e vinte e um acionamentos por ano é um a cada três
dias, e nenhum dos valores da tabela chega perto de ser problema.

> **Onde o limiar importa de verdade** é em edificações com demanda concentrada, em
> que a caixa esvazia rápido. Aí ele pode passar de mil acionamentos por ano, e
> convém dimensionar a caixa em vez de mexer no limiar.

---

## A energia, e por que ela é pequena

Sete vírgula sete quilowatt-hora por ano. Cinco reais e trinta e sete centavos.

Parece pouco demais, e vale entender por quê. Elevar um metro cúbico de água a doze
metros custa, em energia hidráulica, cerca de 0,033 kWh. Com o rendimento da bomba e
o do motor, e somadas as partidas da bomba, chega a cerca de 0,13 kWh por metro cúbico recalcado. Sessenta metros cúbicos por
ano dão os 7,7 quilowatt-hora da tabela.

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
energia e faz a motobomba partir 68 vezes por ano, em vez das mais de sete mil partidas de um
pressurizador acionado a cada descarga por quatro moradores, que gastaria de 40 a 99 kWh
por ano conforme o modelo. O preço é o que a tabela mostra: a caixa, as bombas,
7,7 kWh por ano e um sexto de ponto de potencial frente a um tanque único de 5.000 L.
As bombas são duas, a principal e a reserva, como exige o item 6.5.11.2 da ABNT NBR
5626:2020 para sistemas de recalque e de pressurização.

Em relação à cisterna sozinha de 4.000 L, o potencial sobe de 27,12% para 27,30%,
porque a caixa acrescenta 1.000 L de armazenamento. Daqui em diante, o custo, o carbono
e a decisão do tutorial incluem a caixa, as duas motobombas e a energia do recalque.

<!-- tabela: Estado do projeto do tutorial após a decisão sobre o reservatório superior -->
| Projeto até aqui | |
| :--- | ---: |
| volume do reservatório inferior | 4.000 L |
| arranjo | recalque para caixa superior |
| reservatório superior | 1.000 L, limiar de 100 L |
| potencial de economia | 27,30% |

Agora sabemos quanta água o sistema entrega. Falta saber **que água** é essa.
