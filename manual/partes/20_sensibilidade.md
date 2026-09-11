# Análise de sensibilidade

> **Pergunta que este guia responde:** qual premissa mais move o meu resultado, e o
> quanto ele aguenta?

Todo estudo de aproveitamento pluvial repousa sobre premissas incertas, e as três mais
influentes costumam ser justamente as menos verificáveis: a tarifa realmente subirá 5% ao
ano durante vinte anos? A demanda é de fato 150 litros por pessoa e dia? A cisterna
custará o que o orçamento prevê?

A análise de sensibilidade mede quanto dessas dúvidas chega ao resultado final. ==Ela não
elimina a incerteza, e não se propõe a isso; ela mede o tamanho da incerteza,== que é
exatamente a informação de que o leitor precisa para decidir o quanto confiar no número
apresentado.

---

## O procedimento, em três passos

O procedimento não exige ferramenta especializada, e é o mesmo que se emprega em qualquer
análise de engenharia diante de um parâmetro mal conhecido: varia-se uma coisa de cada
vez e observa-se o efeito.

1. **Escolha a premissa** que você suspeita ser a mais influente.
2. **Rode o projeto três vezes**: com o valor provável, com um valor baixo e com um
   alto.
3. **Anote o resultado das três** e compare.

Repita o procedimento para cada premissa duvidosa. Ao final, você terá identificado
quais delas efetivamente movem o resultado e quais são irrelevantes — e essa separação
vale mais que qualquer refinamento do valor central, porque orienta onde investir esforço
de levantamento de dados. A seção {{n:19}} mostra como organizar os arquivos para que o
conjunto de rodadas não se transforme em confusão.

---

## Que faixa adotar para cada premissa

A faixa de variação a adotar para cada premissa não é matéria de palpite: ela decorre do
que se sabe sobre a origem do dado, e um dado medido admite faixa muito mais estreita que
um dado tomado da literatura.

<!-- tabela: Faixa de variação plausível de cada premissa e a origem da incerteza -->
| Premissa | Variação plausível | Por quê |
| :--- | ---: | :--- |
| área de captação | 2 a 5% | é medida em projeto; o erro é de leitura |
| demanda, se medida | 5 a 10% | variação real entre meses |
| demanda, se de referência | 15 a 25% | a dispersão da literatura é grande |
| chuva | 10 a 20% | variabilidade entre anos |
| investimento | 15 a 30% | dispersão de orçamento é notória |
| reajuste da tarifa | 3 a 7% ao ano | depende da concessionária e do período |

> **Não perturbe o que você conhece.** Se a área foi medida em levantamento, a faixa é
> estreita; alargá-la produz uma incerteza artificial que dilui o resultado e esconde
> a premissa que realmente importa.

---

## A premissa que quase sempre domina

Em estudos econômicos de aproveitamento pluvial, a premissa que mais move o resultado
costuma ser o **reajuste tarifário**, e a razão é que ela atua de forma composta ao longo
de todo o horizonte de análise. Um reajuste de cinco por cento ao ano durante vinte anos
multiplica a tarifa por 2,65; três por cento a multiplicam por 1,81, e sete por cento,
por 3,87. O valor presente líquido acompanha essa variação de modo quase proporcional, de
maneira que a escolha de uma taxa de reajuste decide, sozinha, boa parte da conclusão
econômica do estudo.

Faça o teste no seu caso: na etapa **6. Resultados Econômicos**, mude o reajuste anual
para 3%, anote o VPL, repita com 5% e com 7%. Três rodadas, três minutos, e uma faixa
em vez de um número.

> **Num artigo, mostre essa faixa.** Um valor presente líquido único, calculado com
> reajuste de 5% ao ano e apresentado sem sensibilidade, sugere uma precisão que a
> premissa não tem.

---

## A sensibilidade que o programa faz sozinho

Há um caso em que a análise de sensibilidade já vem pronta e não exige rodadas
adicionais, e ele diz respeito à decisão final do estudo: a escolha do volume em função
dos pesos atribuídos aos critérios.

Na etapa **8. Decisão Multicritério**, a coluna de **aceitabilidade SMAA-VIKOR** já é uma
análise de sensibilidade pronta. Ela responde: se os pesos das dimensões fossem
sorteados em vez de fixados, com que frequência cada volume ficaria em primeiro lugar?

Leia assim:

<!-- tabela: Leitura da aceitabilidade SMAA-VIKOR do volume vencedor -->
| Aceitabilidade do volume vencedor | O que significa |
| :--- | :--- |
| acima de 70% | recomendação robusta; os pesos quase não importam |
| entre 40 e 70% | recomendação razoável, e vale declarar a segunda opção |
| abaixo de 40% | a escolha depende dos pesos, e o texto precisa dizer isso |

A distinção que essa coluna permite é de natureza epistemológica, e não apenas
estatística: um volume que vence em 80% dos sorteios de pesos constitui uma recomendação,
ao passo que um volume que vence em 30% constitui uma preferência do analista, legítima
desde que apresentada como tal. A seção {{n:32}} expõe o método que produz esse número.

---

## Como apresentar

Três formas, da mais simples à mais completa:

**Tabela de cenários.** Pessimista, provável e otimista, com as premissas de cada um
declaradas. Simples, honesta e suficiente para a maior parte dos trabalhos.

**Gráfico de tornado.** Uma barra por premissa, mostrando o quanto o resultado varia
quando ela varia sozinha. Ordena as premissas por importância e é a apresentação mais
informativa por área de página.

**Distribuição.** A faixa completa do resultado, quando todas as premissas variam
juntas. Exige declarar as distribuições adotadas, e não só as faixas.

> **Aprofundamento: propagação por Monte Carlo.** A terceira forma é feita sorteando
> milhares de combinações de premissas e acumulando a distribuição do resultado. O
> programa tem essa capacidade na interface de automação que acompanha a distribuição
> de código-fonte, usada nos trabalhos do grupo de pesquisa. Para um estudo de curso
> ou de projeto, a tabela de cenários do primeiro item responde a mesma pergunta com
> uma fração do esforço — e é mais fácil de defender, porque cada cenário tem
> premissas que se pode ler.

---

## O que declarar

- as **faixas** adotadas e a origem de cada uma;
- quantas rodadas foram feitas, e com que valores;
- para a escolha do volume, a **aceitabilidade** do vencedor;
- **quais premissas não foram perturbadas**, e por quê.

A última é a que mais se esquece, e a que um revisor mais cobra.
