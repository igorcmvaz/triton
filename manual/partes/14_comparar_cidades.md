# Comparar cidades

> **Pergunta que este guia responde:** o mesmo projeto renderia o mesmo em outra cidade?

Não renderia, e a diferença não segue a direção que a intuição sugere. A expectativa
corrente é a de que mais chuva implique mais aproveitamento, e essa expectativa está
errada com frequência suficiente para merecer uma seção inteira.

---

## Como fazer a comparação

O procedimento é simples e consiste em manter todos os parâmetros do projeto e trocar
apenas a série de precipitação. Na etapa **1. Projeto e Chuva**, escolha outra cidade da
base climática nacional ou carregue um arquivo próprio, e execute novamente a simulação.
Para comparar várias cidades sem refazer o projeto a cada uma, salve um arquivo por
cidade, conforme a seção {{n:19}} recomenda.

---

## O resultado

O projeto do tutorial — 150 m² de captação, 600 L/dia de demanda, 40% de fração
atendível e cisterna de 5.000 L — levado a quatro capitais brasileiras produz a tabela
abaixo.

<!-- inclui: _tabelas/cap14_cidades.md -->

![Chuva anual e potencial de economia nas quatro capitais](../figuras/fig03_cidades.png)

*Figura 3 — As barras azuis são a chuva anual; as laranjas, o potencial de economia. Manaus tem a maior barra azul e não tem a maior laranja.*

---

## O regime manda mais que a lâmina

Lidas lado a lado, as colunas de chuva anual e de potencial de economia não andam
juntas, e os dois casos extremos da tabela mostram por quê. Manaus recebe 20% mais chuva
que Florianópolis — 2.155 mm anuais contra 1.795 mm — e ainda assim rende 25% menos:
27,92% contra 37,46% de potencial. Brasília, no extremo oposto, recebe 23% menos chuva
que Florianópolis e rende quase a metade, com 20,80%.

A explicação está na razão entre o mês mais chuvoso e o mês menos chuvoso de cada
cidade, que mede o quanto a chuva se concentra ao longo do ano.

<!-- tabela: Razão entre o mês mais chuvoso e o menos chuvoso nas quatro capitais -->
| Cidade | Razão | O que significa |
| :--- | ---: | :--- |
| Florianópolis | 3,2× | chove o ano inteiro, com estação mais úmida |
| São Paulo | 4,0× | idem, um pouco mais marcado |
| Manaus | 17,3× | seca amazônica curta mas real |
| Brasília | 1.192× | **o mês mais seco é seco de verdade** |

Em Brasília, os meses de junho, julho e agosto praticamente não registram chuva. Um
reservatório dimensionado para atravessar noventa dias de estiagem precisaria armazenar
noventa dias de demanda pluvial, o que neste projeto corresponderia a 21.600 litros —
volume que nenhuma cisterna residencial comporta. A consequência é que o sistema
permanece ocioso durante um trimestre inteiro por ano, e o potencial anual reflete essa
ociosidade.

> **A conclusão prática.** ==O aproveitamento pluvial rende mais onde a chuva é
> frequente do que onde ela é abundante.== Cidades de clima subtropical úmido com chuva
> bem distribuída constituem o melhor caso brasileiro; cidades de clima tropical com
> estação seca marcada constituem o pior, por mais intensa que seja a chuva da estação
> úmida.

---

## O que mais muda entre cidades

A precipitação não é a única grandeza que varia entre municípios, e as outras duas podem
inverter a conclusão econômica de um estudo comparativo.

A primeira é a **tarifa**. O preço do metro cúbico varia consideravelmente pelo país, e o
regime de mínimo varia ainda mais. Um potencial de 20% em município de tarifa elevada e
regime de disponibilidade pode render mais dinheiro que um potencial de 37% em município
que pratique franquia sobre o consumo mínimo, e a seção {{n:16}} trata dessa mecânica em
detalhe.

A segunda é o **fator de emissão da rede elétrica**, que altera simultaneamente a
emissão evitada por metro cúbico de água substituída e o custo ambiental do bombeamento.
O programa traz o fator discriminado por região.

> **Ao comparar cidades num estudo, deixe claro o que variou.** Comparar apenas a
> precipitação, mantendo tarifa e fator de emissão fixos, isola o efeito climático e
> constitui comparação legítima, desde que declarada como tal. Variar todas as grandezas
> simultaneamente produz um número que não se consegue explicar, porque nele se somam
> efeitos de sinais possivelmente opostos.

---

## O volume ideal também muda, mas pouco

A última coluna da tabela reserva uma surpresa: o volume ideal varia de 5.000 a 6.000 L
entre as quatro capitais, uma amplitude modesta diante da diferença de regime que as
separa.

A explicação está na natureza do critério. O volume ideal pelo ganho marginal localiza o
joelho da curva de aproveitamento, e a posição desse joelho é governada pelo **tamanho
típico dos eventos de chuva**, que é razoavelmente parecido entre as quatro cidades. O
que varia fortemente é o **patamar** que a curva atinge depois do joelho, e não o ponto
em que ela dobra.

Dito de outro modo: em Brasília acerta-se o mesmo volume que em Florianópolis e colhe-se
consideravelmente menos água com ele.
