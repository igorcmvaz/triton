# Análise de sensibilidade

> **Pergunta que este guia responde:** qual premissa mais move o meu resultado, e o
> quanto ele aguenta?

Todo estudo pluvial repousa sobre premissas incertas. A tarifa vai mesmo subir 5% ao
ano? A demanda é mesmo 150 litros por pessoa? A cisterna custa mesmo isso?

A análise de sensibilidade mede quanto dessas dúvidas chega ao resultado. Ela não
elimina a incerteza; ela mostra o tamanho dela, que é o que um leitor precisa saber
para confiar no número.

---

## O procedimento, em três passos

Não é preciso nenhuma ferramenta especial. O método é o mesmo que se usa em qualquer
análise de engenharia:

1. **Escolha a premissa** que você suspeita ser a mais influente.
2. **Rode o projeto três vezes**: com o valor provável, com um valor baixo e com um
   alto.
3. **Anote o resultado das três** e compare.

Repita para cada premissa duvidosa. Ao fim, você sabe quais delas movem o resultado e
quais não movem — e essa é a informação que vale.

A seção {{n:19}} mostra como organizar os arquivos para que isso não vire confusão.

---

## Que faixa adotar para cada premissa

A faixa não é palpite: ela vem do que você sabe sobre a origem do dado.

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

Em estudos econômicos de aproveitamento pluvial, quem mais move o resultado costuma
ser o **reajuste tarifário**.

Cinco por cento ao ano durante vinte anos multiplica a tarifa por 2,65. Três por cento
multiplica por 1,81; sete por cento, por 3,87. O valor presente líquido acompanha,
quase proporcionalmente.

Faça o teste no seu caso: na etapa **6. Resultados Econômicos**, mude o reajuste anual
para 3%, anote o VPL, repita com 5% e com 7%. Três rodadas, três minutos, e uma faixa
em vez de um número.

> **Num artigo, mostre essa faixa.** Um valor presente líquido único, calculado com
> reajuste de 5% ao ano e apresentado sem sensibilidade, sugere uma precisão que a
> premissa não tem.

---

## A sensibilidade que o programa faz sozinho

Há um caso em que não é preciso rodar três vezes: a **escolha do volume pelos pesos**
do multicritério.

Na etapa **8. Decisão Multicritério**, a coluna de **aceitabilidade SMAA-VIKOR** já é uma
análise de sensibilidade pronta. Ela responde: se os pesos das dimensões fossem
sorteados em vez de fixados, com que frequência cada volume ficaria em primeiro lugar?

Leia assim:

| Aceitabilidade do volume vencedor | O que significa |
| :--- | :--- |
| acima de 70% | recomendação robusta; os pesos quase não importam |
| entre 40 e 70% | recomendação razoável, e vale declarar a segunda opção |
| abaixo de 40% | a escolha depende dos pesos, e o texto precisa dizer isso |

Um volume que vence em 80% dos sorteios é uma recomendação; um que vence em 30% é uma
preferência. A seção {{n:32}} explica o método.

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
