# Dez enganos que o programa não impede

> Estes não são defeitos do programa. São erros de **engenharia** que ele aceita sem
> reclamar, porque não tem como saber. Cada um traz o engano, por que ele é
> tentador, o que faz ao resultado, e como evitar.

---

## Usar a área inclinada do telhado

**O engano.** Informar a área da superfície do telhado em vez da projeção horizontal.

**Por que é tentador.** É a área que aparece no quantitativo de telhas, e é a que o
pedreiro conhece.

**O que faz ao resultado.** Superestima a captação na razão `1 ÷ cos(inclinação)`.
Num telhado de 30% de caimento, 4,4% de água que não existe; em 60%, 16,6%.

**Como evitar.** O item 3.6 da NBR 15527:2019 define a área de captação como a
projeção horizontal, e a EN 16941-1:2024 faz o mesmo. Não use a área de contribuição da NBR 10844, que soma a metade da
altura do telhado e as paredes para dimensionar calhas.
A chuva cai na vertical, e o que ela vê é a sombra da cobertura no chão. Se você tem a área inclinada, multiplique por `cos(inclinação)`, como na {{fig:fig00i_projecao}}.

---

![A chuva cai na vertical, e a área que capta é a projeção do telhado](../figuras/fig00i_projecao.png)

*Figura 99 — Área de captação como projeção horizontal da cobertura, conforme o item 3.6 da ABNT NBR 15527:2019. Para inclinação de 30%, θ = 16,7° e a área inclinada é 4,4% maior que a projeção horizontal; usar a área inclinada superestima o volume captado nessa proporção em todos os dias da série.*

---

## Dimensionar pela chuva média mensal

**O engano.** Usar a média mensal de precipitação num cálculo de planilha, em vez da
série diária.

**Por que é tentador.** A média mensal é o dado publicado nas normais
climatológicas, e a planilha cabe numa página.

**O que faz ao resultado.** Superestima sistematicamente. A média esconde que a
chuva chega concentrada: um mês com 200 mm distribuídos em cinco eventos enche e
faz a cisterna extravasar cinco vezes, enquanto o cálculo médio supõe um fluxo contínuo
que a cisterna absorveria inteiro.

**Como evitar.** É a razão de existir deste programa. A seção {{n:23}} mostra o
extravasamento acontecendo dia a dia; o cálculo por médias não o enxerga.

---

## Confundir a lâmina de descarte com o volume do dispositivo

**O engano.** Informar no campo de descarte o volume do reservatório de autolimpeza,
em litros.

**Por que é tentador.** O dispositivo é dimensionado em litros, e o campo pede um
número.

**O que faz ao resultado.** O campo espera **milímetros**. Informar 300, pensando nos
300 litros do dispositivo, produz um descarte de 300 mm — maior que quase toda chuva
diária já registrada no Brasil. O sistema capta **praticamente zero**.

**Como evitar.** `d_f` é uma lâmina. O volume do dispositivo é `A × d_f`: no projeto
do tutorial, 150 m² × 2 mm = 300 litros. São a mesma decisão expressa em duas
unidades, e o programa quer a primeira.

---

## Ignorar o regime de mínimo tarifário

**O engano.** Montar a tabela tarifária com as faixas progressivas e esquecer como a
concessionária trata o consumo mínimo.

**Por que é tentador.** As faixas são o que está publicado em destaque. O regime de
mínimo está numa nota de rodapé, quando está.

**O que faz ao resultado.** Em município de **franquia no mínimo**, que são 371 dos
652 da base, economizar abaixo da franquia **não desconta nada**. Um estudo que
suponha desconto linear produz um payback que não existe.

**Como evitar.** A seção {{n:16}}. E o teste prático: simule dois consumos, um dentro e um
fora da faixa mínima, e compare com uma fatura real da edificação.

---

## Simular escola ou hospital com tarifa residencial

**O engano.** Usar a tarifa residencial do catálogo para edificação não residencial.

**Por que é tentador.** O catálogo traz 652 municípios prontos, quase todos só com a
categoria residencial, e o programa não impede.

**O que faz ao resultado.** Subestima a economia. As categorias não residenciais são
mais caras: na CASAN de abril de 2026, a primeira faixa custa R$ 6,81/m³ no
comercial contra R$ 3,08/m³ no residencial.

**Como evitar.** O programa **avisa** quando a tipologia não é residencial, e diz o
sentido do erro. Escolha a categoria da edificação onde o catálogo a traz, hoje nos
municípios da CORSAN; nos demais, lance a estrutura da categoria correta no modo
personalizado. A seção {{n:18}} trata do assunto. Na International Edition, a tarifa é sempre
digitada; digite a da categoria da edificação.

---

## Esperar que o reservatório superior aumente a economia

**O engano.** Adotar a caixa elevada esperando mais água.

**Por que é tentador.** É o arranjo clássico brasileiro, e «mais reservatório» soa
como «mais água».

**O que faz ao resultado.** Com o mesmo armazenamento total, o arranjo com caixa
elevada entrega **menos**: a cisterna extravasa enquanto a caixa de cima ainda tem
espaço, porque o recalque só acontece quando há consumo. No tutorial, cerca de um sexto de ponto percentual a menos, mais
7,7 kWh por ano de energia.

**Como evitar.** Decida a caixa por critério **hidráulico** — pressão por gravidade,
reserva contra falta de energia — e não hídrico. A seção {{n:8}} faz a comparação justa.

---

## Adotar série curta demais

**O engano.** Simular com dois ou três anos de série.

**Por que é tentador.** É o que se consegue rápido de uma estação próxima.

**O que faz ao resultado.** Dois efeitos somados. O **viés do reservatório vazio**,
porque a simulação começa com a cisterna seca e os primeiros meses penalizam o
resultado; e a **dependência do trecho**, porque uma série curta pode cair num
período atipicamente seco ou chuvoso.

**Como evitar.** Trinta anos é confortável, dez é o mínimo defensável. Abaixo disso,
declare a limitação e mostre o resultado como faixa.

---

## Escolher a classe de qualidade pelo custo

**O engano.** Adotar a classe 1 porque é a mais barata, para um uso que exigiria
mais.

**Por que é tentador.** O programa deixa, e a diferença de custo é visível
imediatamente.

**O que faz ao resultado.** Não muda o número; muda a **validade** do projeto. Um
sistema que alimenta máquina de lavar roupas com água tratada ao mínimo normativo é
uma decisão de qualidade, não de orçamento.

**Como evitar.** Escolha pela **exigência do uso**. E lembre que as classes 2 a 4 são
adaptações do programa, não requisitos da NBR 15527: use-as como critério declarado, e
não como norma.

---

## Comparar com o Netuno 4 sem declarar a divergência

**O engano.** Apresentar resultados das duas versões lado a lado como se fossem
comparáveis.

**Por que é tentador.** São o mesmo programa, em versões diferentes.

**O que faz ao resultado.** O Triton estima, em média, de **2,3 a 2,7 pontos
percentuais menos** economia que o Netuno 4 sobre 4.050 casos de referência, e cerca
de **metade** dessa diferença vem do tratamento do descarte, que mudou
deliberadamente.

**Como evitar.** Declare a divergência, e compare com descarte igual a zero, em que
as duas regras coincidem. As seções {{n:21}} e {{n:35}} detalham o assunto.

---

## Publicar o volume de maior economia como recomendado

**O engano.** Escolher da varredura o volume de maior potencial.

**Por que é tentador.** É a coluna que o estudo de aproveitamento pluvial reporta, e
mais é melhor.

**O que faz ao resultado.** No tutorial, 20.000 L dão o maior potencial, o mesmo que
12.000 L já davam. Também custam **3,9 vezes mais** que os 4.000 L e carregam **4,1
vezes mais carbono incorporado**, para entregar 0,88 ponto percentual a mais. E, em concreto, o
volume maior é ambientalmente **pior** em termos absolutos.

**Como evitar.** Declare o critério de escolha. Se for hidráulico, o limiar de ganho
marginal; se for multicritério, os quatro pesos de eixo, as partes no eixo e a faixa de escolha, com a tolerância. E reporte os vencedores de cada critério
isolado, porque a divergência entre eles **é** o resultado.

---

## O engano de fundo

Os dez acima têm uma raiz comum: **tratar o programa como uma calculadora em vez de
um modelo**.

Uma calculadora recebe números e devolve números. Um modelo recebe premissas e
devolve consequências dessas premissas. Todo resultado do Triton é condicional ao que
foi declarado, e a qualidade do estudo está na qualidade e na explicitação dessas
declarações.

É por isso que a seção {{n:13}} traz a lista do que declarar, e é por isso que a seção {{n:36}} traz as limitações conhecidas. Um estudo que não declara premissas não é
reproduzível, por mais correto que o cálculo esteja.
