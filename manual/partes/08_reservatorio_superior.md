# Precisa de reservatório superior?

> Ao terminar esta seção você saberá responder a pergunta com número, e não com
> hábito. A resposta costuma surpreender.

O arranjo clássico do aproveitamento pluvial brasileiro tem dois reservatórios: uma
cisterna enterrada que recebe a chuva, e uma caixa d'água elevada que alimenta os
pontos de consumo por gravidade. Entre as duas, uma motobomba.

Quase todo projeto adota esse arranjo sem perguntar por quê. Vamos perguntar.

---

## Para que serve a caixa superior

**Não serve para guardar mais água.** Serve para **entregar** água.

A cisterna está enterrada. Os pontos de consumo — bacia sanitária, tanque, torneira
de jardim — estão acima dela. Alguém precisa levar a água até lá, e há duas
maneiras:

- **Pressurização direta.** Uma bomba pequena com pressostato liga sempre que se
  abre um ponto. Não há caixa superior.
- **Recalque para caixa elevada.** A bomba enche a caixa de tempos em tempos, e a
  gravidade faz o resto.

O segundo arranjo tem vantagens práticas: a bomba liga poucas vezes por dia em vez
de dezenas, a pressão nos pontos é constante, e há reserva para falta de energia.
Nada disso é economia de água.

---

## A comparação justa

Comparar «5.000 L sem caixa» com «5.000 L mais 1.000 L de caixa» é armadilha: o
segundo tem mais armazenamento. Para isolar o efeito do **arranjo**, compare o mesmo
armazenamento total.

<!-- inclui: _tabelas/cap08_reservatorio_superior.md -->

O arranjo com caixa elevada entrega **0,33 ponto percentual a menos** que o mesmo
volume num tanque só. Não é erro de arredondamento, e tem duas causas.

**O limiar de acionamento imobiliza água.** Os 100 L de reserva na caixa superior
não são consumidos: existem para a bomba não ligar a cada litro. São 100 L a menos
de armazenamento útil.

**A sequência de atendimento perde oportunidades.** O programa consome primeiro da
caixa superior, depois recalca, depois consome de novo. Num dia de demanda alta com
a cisterna cheia, o ciclo pode não completar, e sobra demanda não atendida que um
tanque único teria coberto.

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
aproveitamento pluvial é desprezível diante da economia da conta de água — e é por
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
