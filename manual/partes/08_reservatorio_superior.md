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
maneiras de fazê-lo.

- **Pressurização direta.** Uma bomba pequena com pressostato liga sempre que se
  abre um ponto. Não há caixa superior.
- **Recalque para caixa elevada.** A bomba enche a caixa de tempos em tempos, e a
  gravidade faz o resto.

O segundo arranjo tem três vantagens práticas reais. A motobomba liga poucas vezes por
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

Mantido o mesmo armazenamento, o arranjo com caixa elevada entrega 0,33 ponto percentual
a menos de economia que o reservatório único. A diferença não é erro de arredondamento, e
decorre de duas causas que se somam.

A primeira é que **o limiar de acionamento imobiliza água**. Os 100 L de reserva mantidos
na caixa superior nunca são consumidos: existem para que a motobomba não acione a cada
litro retirado. Na prática, são 100 L subtraídos do armazenamento útil do sistema.

A segunda é que **a sequência de atendimento perde oportunidades**. O programa consome
primeiro o que há na caixa superior, depois aciona o recalque, e então consome de novo.
Num dia de demanda elevada com a cisterna cheia, o ciclo pode não se completar dentro do
dia, e resta demanda não atendida que um reservatório único teria coberto sem
intermediação.

> **A caixa superior não aumenta a economia de água. Ela custa.** No nosso projeto,
> custa a caixa, custa a bomba, custa 10,7 kWh por ano de energia, e custa 0,33
> ponto de potencial.
>
> Isso não a torna errada. Torna a decisão **hidráulica**, e não hídrica: adote-a se
> o projeto precisa de pressão por gravidade ou de reserva contra falta de energia,
> e não esperando que ela renda mais água.

---

## O limiar de acionamento

Se você adotar a caixa, há um parâmetro a ajustar: o volume de reserva que não se
consome, abaixo do qual a bomba é acionada.

<!-- inclui: _tabelas/cap08_limiar.md -->

Limiar maior significa **mais potencial e mais acionamentos**. De 0 para 500 L, o
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

Dez vírgula sete quilowatt-hora por ano. Dez reais.

Parece pouco demais, e vale entender por quê. Elevar um metro cúbico de água a doze
metros custa, em energia hidráulica, cerca de 0,033 kWh. Com o rendimento da bomba e
o do motor, chega a 0,13 kWh por metro cúbico entregue. Oitenta e dois metros
cúbicos por ano dão dez quilowatt-hora.

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

**Seguimos sem caixa superior.**

A residência do tutorial é térrea, os pontos de consumo não pluviais ficam a menos
de dois metros acima da cisterna, e a pressurização direta resolve. Adotar a caixa
acrescentaria investimento e energia sem contrapartida hídrica.

Num sobrado, ou num prédio, a resposta mudaria — não por causa da água, mas por
causa da pressão.

<!-- tabela: Estado do projeto do tutorial após a decisão sobre o reservatório superior -->
| Projeto até aqui | |
| :--- | ---: |
| volume do reservatório | 5.000 L |
| reservatório superior | não |
| potencial de economia | 37,46% |

Agora sabemos quanta água o sistema entrega. Falta saber **que água** é essa.
