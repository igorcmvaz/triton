# Dez enganos que o programa não impede

> Estes não são defeitos do programa. São erros de **engenharia** que ele aceita sem reclamar,
> porque não tem como os conhecer. Cada um traz o engano, por que razão é tentador, o que faz ao
> resultado e como evitá-lo.

---

## Usar a área inclinada da cobertura

**O engano.** Introduzir a área da superfície da cobertura em vez da projeção horizontal.

**Porque é tentador.** É a área que aparece nas medições de telha e a que o empreiteiro conhece.

**O que faz ao resultado.** Sobrestima a captação na razão `1 ÷ cos(inclinação)`. Numa cobertura
com 30% de pendente, 4,4% de água que não existe; com 60%, 16,6%.

**Como evitar.** A prática do aproveitamento de águas pluviais toma como área de captação a
projeção horizontal da cobertura. Não use a área de contribuição com que se dimensionam as
caleiras, que soma metade da altura da cobertura e as paredes. A chuva cai na vertical, e o que
ela vê é a sombra da cobertura no chão. Se tem a área inclinada, multiplique-a por
`cos(inclinação)`, como na {{fig:fig00i_projecao}}.

---

![A chuva cai na vertical, e a área que capta é a projeção da cobertura](../figuras/fig00i_projecao.png)

*Figura 99 — Área de captação como projeção horizontal da cobertura. Para uma pendente de 30%, θ = 16,7° e a área inclinada é 4,4% maior do que a projeção horizontal; usar a área inclinada sobrestima o volume captado nessa proporção em todos os dias da série.*

---

## Dimensionar pela chuva média mensal

**O engano.** Usar a precipitação média mensal num cálculo de folha de cálculo, em vez da série
diária.

**Porque é tentador.** A média mensal é o dado publicado nas normais climatológicas, e a folha de
cálculo cabe numa página.

**O que faz ao resultado.** Sobrestima de forma sistemática. A média esconde que a chuva chega
concentrada: um mês com 200 mm repartidos por cinco eventos enche a cisterna e faz com que
extravase cinco vezes, ao passo que o cálculo por médias supõe um fluxo contínuo que a cisterna
absorveria por inteiro. Em Lisboa o efeito é ainda mais marcante, porque o verão é seco: o mês mais
chuvoso tem 22,7 vezes a chuva do menos chuvoso, e uma média anual não vê nada disto.

**Como evitar.** É a razão de existir deste programa. A secção {{n:23}} mostra o extravasamento a
acontecer dia a dia; o cálculo por médias não o vê.

---

## Confundir a lâmina de descarte com o volume do dispositivo

**O engano.** Introduzir no campo do descarte o volume do reservatório de autolimpeza, em litros.

**Porque é tentador.** O dispositivo dimensiona-se em litros, e o campo pede um número.

**O que faz ao resultado.** O campo espera **milímetros**. Introduzir 300, a pensar nos 300 litros
do dispositivo, produz um descarte de 300 mm — maior do que qualquer chuva diária da série de
Lisboa do tutorial, cujo máximo é 109,9 mm. O sistema capta **praticamente nada**.

**Como evitar.** `d_f` é uma lâmina. O volume do dispositivo é `A × d_f`: no projeto do tutorial,
150 m² × 2 mm = 300 litros. São a mesma decisão expressa em duas unidades, e o programa quer a
primeira.

---

## Ignorar a estrutura do tarifário

**O engano.** Montar o tarifário com um preço único por metro cúbico e esquecer a parte fixa, os
escalões e a forma como a entidade gestora trata cada componente da fatura.

**Porque é tentador.** O preço do metro cúbico é o que vem em destaque. A tarifa fixa e a forma
como o saneamento e os resíduos acompanham o consumo estão em quadros à parte, quando estão.

**O que faz ao resultado.** A poupança só incide sobre a parte variável da fatura, e cada metro
cúbico poupado vale o preço do escalão em que cai. Em Lisboa, a fatura do tutorial passa de
46,25 € por mês sem o sistema (18,26 m³) para 34,93 € com ele (14,92 m³): uma poupança de
3,34 m³ e de 11,32 € por mês. Um estudo que suponha um desconto linear sobre a fatura total produz
um período de recuperação que não existe.

**Como evitar.** A secção {{n:16}}. E o teste prático: simule dois consumos, um num escalão e outro
noutro, e compare com uma fatura real do edifício.

---

## Simular uma escola ou um hospital com tarifa doméstica

**O engano.** Usar a tarifa doméstica para um edifício que não é de habitação.

**Porque é tentador.** O tarifário doméstico é o que está à mão, e o programa não impede a sua
utilização noutra tipologia. Os tarifários que a edição traz transcritos (Lisboa, Porto e Funchal)
são de utilizador doméstico.

**O que faz ao resultado.** Subestima, em regra, a poupança, porque as categorias não domésticas
costumam ser mais caras do que a doméstica; o preço de cada entidade gestora é que decide.

**Como evitar.** O programa **avisa** quando a tipologia não é residencial e diz o sentido do erro.
Escolha a categoria do edifício no tarifário da entidade gestora e introduza a sua estrutura em
modo personalizado. A secção {{n:18}} trata do assunto.

---

## Esperar que o reservatório superior aumente a poupança

**O engano.** Adotar o reservatório elevado à espera de mais água.

**Porque é tentador.** É um arranjo corrente, e «mais reservatório» soa a «mais água».

**O que faz ao resultado.** Com o mesmo armazenamento total, o arranjo com reservatório elevado
entrega **menos**: a cisterna extravasa enquanto o reservatório de cima ainda tem espaço, porque a
elevação só acontece quando há consumo. No tutorial, 0,32 pontos percentuais a menos (18,28%
contra 18,59% com um único reservatório de 6 000 L), mais 5,3 kWh por ano de energia.

**Como evitar.** Decida o reservatório por critério **hidráulico** — pressão por gravidade, reserva
contra falhas de energia — e não hídrico. A secção {{n:8}} faz a comparação justa.

---

## Adotar uma série curta demais

**O engano.** Simular com dois ou três anos de série.

**Porque é tentador.** É o que se consegue depressa a partir de um posto próximo.

**O que faz ao resultado.** Dois efeitos somados. O **viés do reservatório vazio**, porque a
simulação começa com a cisterna seca e os primeiros meses penalizam o resultado; e a
**dependência do troço**, porque uma série curta pode cair num período atipicamente seco ou
chuvoso.

**Como evitar.** Trinta anos é confortável, dez é o mínimo defensável. Abaixo disso, declare a
limitação e apresente o resultado como uma gama.

---

## Escolher a classe de qualidade pelo custo

**O engano.** Adotar a classe 1 por ser a mais barata, para um uso que exigiria mais.

**Porque é tentador.** O programa deixa, e a diferença de custo vê-se logo.

**O que faz ao resultado.** Não muda o número; muda a **validade** do projeto. Um sistema que
alimenta uma máquina de lavar roupa com água tratada ao mínimo é uma decisão de qualidade, não de
orçamento.

**Como evitar.** Escolha pela **exigência do uso**. E lembre que as classes 2 a 4 são adaptações
do programa, e não requisitos de uma norma: use-as como critério declarado, e não como norma.

---

## Comparar com outra ferramenta sem declarar o método

**O engano.** Apresentar lado a lado os resultados de dois programas de aproveitamento pluvial
como se fossem comparáveis.

**Porque é tentador.** Ambos simulam o mesmo reservatório com as mesmas equações de balanço.

**O que faz ao resultado.** As ferramentas diferem em decisões de modelação que movem o número: se
o descarte das primeiras águas se subtrai à chuva do dia ou funciona como limiar do evento, como se
escolhe o volume ideal, que regra de operação se aplica. Uma diferença de alguns pontos percentuais
pode vir de qualquer uma delas, e nenhuma é um erro.

**Como evitar.** Declare a divergência e compare com um descarte igual a zero, em que as duas
regras de descarte coincidem. As secções {{n:21}} e {{n:35}} detalham o assunto.

---

## Publicar o volume de maior poupança como recomendado

**O engano.** Escolher da varredura o volume de maior potencial.

**Porque é tentador.** É a coluna que o estudo de aproveitamento pluvial reporta, e mais é melhor.

**O que faz ao resultado.** No tutorial de Lisboa a curva não satura: 20 000 L dão o maior
potencial da varredura, 24,35%. Custam também **3,3 vezes mais** do que 5 000 L, em betão
(ilustrativo, não é preço de mercado: 8 600 € contra 2 600 €), e carregam **3,5 vezes mais carbono
incorporado** (3 546 contra 1 026 kg CO₂e), para entregar 6,47 pontos percentuais a mais. Escolher
o maior volume testado é escolher o limite da varredura, e não um ótimo.

**Como evitar.** Declare o critério de escolha. Se for hidráulico, o limiar de ganho marginal; se
for multicritério, os quatro pesos de eixo, as partes no eixo, os volumes candidatos e a faixa de escolha com a tolerância. E reporte os vencedores de cada critério isolado, porque a divergência
entre eles **é** o resultado.

---

## O engano de fundo

Os dez acima têm uma raiz comum: **tratar o programa como uma calculadora em vez de um modelo**.

Uma calculadora recebe números e devolve números. Um modelo recebe premissas e devolve as
consequências dessas premissas. Todo o resultado do Triton é condicional ao que foi declarado, e a
qualidade do estudo está na qualidade e na explicitação dessas declarações.

É por isso que a secção {{n:13}} traz a lista do que declarar, e é por isso que a secção {{n:36}}
traz as limitações conhecidas. Um estudo que não declara as premissas não é reproduzível, por mais
correto que seja o cálculo.
