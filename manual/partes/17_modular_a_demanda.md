# Modular a demanda por calendário

> **Pergunta que este guia responde:** e quando o consumo não é o mesmo todo dia?

Escolas fecham em janeiro e julho, hotéis de praia enchem no verão e escritórios esvaziam
nos fins de semana. Tratar qualquer uma dessas edificações como se tivesse consumo
uniforme erra nos dois sentidos simultaneamente: superestima a demanda nos períodos
vazios e a subestima nos períodos de pico. ==O erro não se compensa ao longo do ano,
porque o que importa ao sistema pluvial não é o total consumido e sim o encontro entre o
consumo e a chuva disponível naquele dia.==

---

## Os quatro modos

| Modo | Você informa | Quando usar |
| :--- | :--- | :--- |
| **constante** | um valor | residência, e o padrão |
| **semanal** | sete valores, segunda a domingo | escritório, comércio, escola |
| **mensal** | doze valores | hotel, sazonalidade climática |
| **diário** | a série inteira | quando há medição real, dia a dia |

Em qualquer um deles você pode modular três coisas de forma independente: a
**demanda per capita**, o **número de ocupantes** e a **fração atendível por água
pluvial**.

Modular a ocupação costuma ser mais fiel que modular a demanda: numa escola em
férias não é o aluno que bebe menos água, é que não há aluno.

---

## Como preencher

Na etapa **2. Edificação Consumo**, escolha o modo. Abre-se a tabela do período.

- Célula vazia ou zerada **cai para o valor constante**. Isso é deliberado: permite
  modular só os meses que interessam e deixar o resto no padrão.
- Os valores podem ser digitados ou carregados de CSV.
- No modo diário, o primeiro dia da série de demanda alinha com o primeiro dia da
  **série de chuva**. Se as duas tiverem tamanhos diferentes, a de demanda é
  reciclada ciclicamente.

---

## Por que isso muda o resultado

Modular a demanda não altera apenas o total anual consumido; altera o casamento temporal
entre oferta e demanda, que é precisamente o problema que o reservatório existe para
resolver. Dois casos opostos ilustram o alcance desse efeito, e ambos são comuns no
Brasil.

**A favor.** Uma escola que fecha em julho, no sul do país, fecha justamente quando
chove menos. A cisterna atravessa a estiagem sem ser solicitada e chega cheia em
agosto. O sistema rende **mais** do que a média anual sugeriria.

**Contra.** Um hotel de praia enche em janeiro e fevereiro, quando chove mais no
litoral sul. Parece bom, mas a demanda concentrada esvazia a cisterna em dias, e o
resto do ano ela fica ociosa. O sistema rende **menos**.

> **A regra geral:** demanda em fase com a chuva rende mais; demanda em
> contrafase rende menos. E o efeito é invisível no cálculo por médias anuais, que é
> justamente por que o Netuno simula dia a dia.

---

## A fração atendível também pode variar

Menos óbvio e às vezes mais importante. Numa escola, o percentual de uso não potável
muda entre período letivo e férias: em férias sobra lavagem de piso e rega de
jardim, que são usos **integralmente** atendíveis por chuva.

Modular a fração captura isso. Manter fração constante subestima o aproveitamento no
período de baixa ocupação.

---

## Cuidados

**Não module o que você não mediu.** Uma modulação inventada acrescenta precisão
aparente sem acrescentar informação alguma, e transfere ao leitor a impressão de um rigor
que o dado não tem. Na dúvida, demanda constante explicitamente declarada é mais honesta
que um perfil mensal arbitrado.

**Declare a origem do perfil.** Ele pode vir de medição própria, de doze contas de água
mensais, de referência bibliográfica ou de estimativa, e essas quatro origens não têm o
mesmo peso probatório num estudo publicado.

**Confira o total anual depois de modular.** O programa exibe a demanda média diária
resultante da modulação, e a divergência entre esse valor e o que se esperava é o
indicador mais rápido de erro de preenchimento da tabela.

---

## O caminho mais simples, quando existe

Se você tem **doze contas de água** da edificação, tem o perfil mensal medido,
que é a melhor fonte possível. Divida o consumo de cada mês pelo número de dias e
pelo número de ocupantes, e use o modo mensal.

Doze contas valem mais que qualquer referência de literatura.
