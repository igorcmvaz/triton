# 33. Dez enganos que o programa não impede

> Estes não são defeitos do programa. São erros de **engenharia** que ele aceita sem
> reclamar, porque não tem como saber. Cada um traz o engano, por que ele é
> tentador, o que faz ao resultado, e como evitar.

---

## 33.1. Usar a área inclinada do telhado

**O engano.** Informar a área da superfície do telhado em vez da projeção horizontal.

**Por que é tentador.** É a área que aparece no quantitativo de telhas, e é a que o
pedreiro conhece.

**O que faz ao resultado.** Superestima a captação na razão `1 ÷ cos(inclinação)`.
Num telhado de 30% de caimento, 4,4% de água que não existe; em 60%, 16,6%.

**Como evitar.** A NBR 10844 define a área de captação como a projeção horizontal.
A chuva cai na vertical, e o que ela vê é a sombra da cobertura no chão. Se você tem
a área inclinada, multiplique por `cos(inclinação)`.

---

## 33.2. Dimensionar pela chuva média mensal

**O engano.** Usar a média mensal de precipitação num cálculo de planilha, em vez da
série diária.

**Por que é tentador.** A média mensal é o dado publicado nas normais
climatológicas, e a planilha cabe numa página.

**O que faz ao resultado.** Superestima sistematicamente. A média esconde que a
chuva chega concentrada: um mês com 200 mm distribuídos em cinco eventos enche e
transborda a cisterna cinco vezes, enquanto o cálculo médio supõe um fluxo contínuo
que a cisterna absorveria inteiro.

**Como evitar.** É a razão de existir deste programa. O capítulo 23 mostra o
extravasamento acontecendo dia a dia; o cálculo por médias não o enxerga.

---

## 33.3. Confundir a lâmina de descarte com o volume do dispositivo

**O engano.** Informar no campo de descarte o volume do reservatório de autolimpeza,
em litros.

**Por que é tentador.** O dispositivo é dimensionado em litros, e o campo pede um
número.

**O que faz ao resultado.** O campo espera **milímetros**. Informar 300, pensando nos
300 litros do dispositivo, produz um descarte de 300 mm — maior que qualquer chuva
diária registrada no Brasil. O sistema capta **zero**.

**Como evitar.** `d_f` é uma lâmina. O volume do dispositivo é `A × d_f`: no projeto
do tutorial, 150 m² × 2 mm = 300 litros. São a mesma decisão expressa em duas
unidades, e o programa quer a primeira.

---

## 33.4. Ignorar o regime de mínimo tarifário

**O engano.** Montar a tabela tarifária com as faixas progressivas e esquecer como a
concessionária trata o consumo mínimo.

**Por que é tentador.** As faixas são o que está publicado em destaque. O regime de
mínimo está numa nota de rodapé, quando está.

**O que faz ao resultado.** Em município de **franquia no mínimo**, que são 329 dos
652 da base, economizar abaixo da franquia **não desconta nada**. Um estudo que
suponha desconto linear produz um payback que não existe.

**Como evitar.** O guia 16. E o teste prático: simule dois consumos, um dentro e um
fora da faixa mínima, e compare com uma conta real da edificação.

---

## 33.5. Simular escola ou hospital com tarifa residencial

**O engano.** Usar a tarifa do catálogo — que é residencial — para edificação não
residencial.

**Por que é tentador.** O catálogo traz 652 municípios prontos, e o programa não
impede.

**O que faz ao resultado.** Subestima a economia. As categorias não residenciais são
mais caras: na CASAN de abril de 2026, a primeira faixa custa R$ 6,81/m³ no
comercial contra R$ 3,08/m³ no residencial.

**Como evitar.** O programa **avisa** quando a tipologia não é residencial, e diz o
sentido do erro. Lance a estrutura da categoria correta no modo personalizado. O
guia 18 trata do assunto.

---

## 33.6. Esperar que o reservatório superior aumente a economia

**O engano.** Adotar a caixa elevada esperando mais água.

**Por que é tentador.** É o arranjo clássico brasileiro, e «mais reservatório» soa
como «mais água».

**O que faz ao resultado.** Com o mesmo armazenamento total, o arranjo com caixa
elevada entrega **menos**: o limiar de acionamento imobiliza água e a sequência de
atendimento perde oportunidades. No tutorial, 0,33 ponto percentual a menos, mais
10,7 kWh por ano de energia.

**Como evitar.** Decida a caixa por critério **hidráulico** — pressão por gravidade,
reserva contra falta de energia — e não hídrico. O capítulo 8 faz a comparação justa.

---

## 33.7. Adotar série curta demais

**O engano.** Simular com dois ou três anos de série.

**Por que é tentador.** É o que se consegue rápido de uma estação próxima.

**O que faz ao resultado.** Dois efeitos somados. O **viés do reservatório vazio**,
porque a simulação começa com a cisterna seca e os primeiros meses penalizam o
resultado; e a **dependência do trecho**, porque uma série curta pode cair num
período atipicamente seco ou chuvoso.

**Como evitar.** Trinta anos é confortável, dez é o mínimo defensável. Abaixo disso,
declare a limitação e mostre o resultado como faixa.

---

## 33.8. Escolher a classe de qualidade pelo custo

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

## 33.9. Comparar com o Netuno 4 sem declarar a divergência

**O engano.** Apresentar resultados das duas versões lado a lado como se fossem
comparáveis.

**Por que é tentador.** São o mesmo programa, em versões diferentes.

**O que faz ao resultado.** O Netuno 5 estima, em média, de **2,3 a 2,7 pontos
percentuais menos** economia que o Netuno 4 sobre 4.050 casos de referência, e cerca
de **metade** dessa diferença vem do tratamento do descarte, que mudou
deliberadamente.

**Como evitar.** Declare a divergência, e compare com descarte igual a zero, em que
as duas regras coincidem. Os capítulos 21 e 35 detalham.

---

## 33.10. Publicar o volume de maior economia como recomendado

**O engano.** Escolher da varredura o volume de maior potencial.

**Por que é tentador.** É a coluna que o estudo de aproveitamento pluvial reporta, e
mais é melhor.

**O que faz ao resultado.** No tutorial, 20.000 L dão o maior potencial. Também
custam **3,3 vezes mais** que os 5.000 L e carregam **3,6 vezes mais carbono
incorporado**, para entregar 2,53 pontos percentuais a mais. E, em concreto, o
volume maior é ambientalmente **pior** em termos absolutos.

**Como evitar.** Declare o critério de escolha. Se for hidráulico, o limiar de ganho
marginal; se for multicritério, os pesos. E reporte os vencedores de cada critério
isolado, porque a divergência entre eles **é** o resultado.

---

## 33.11. O engano de fundo

Os dez acima têm uma raiz comum: **tratar o programa como uma calculadora em vez de
um modelo**.

Uma calculadora recebe números e devolve números. Um modelo recebe premissas e
devolve consequências dessas premissas. Todo resultado do Netuno é condicional ao que
foi declarado, e a qualidade do estudo está na qualidade e na explicitação dessas
declarações.

É por isso que o capítulo 13 traz a lista do que declarar, e é por isso que o
capítulo 36 traz as limitações conhecidas. Um estudo que não declara premissas não é
reproduzível, por mais correto que o cálculo esteja.
