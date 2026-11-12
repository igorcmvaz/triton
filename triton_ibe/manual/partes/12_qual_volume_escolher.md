# Que volume escolher, afinal

> No fim desta secção, tem um volume recomendado e sabe que ele depende de pesos que **o utilizador** declarou — e não de uma verdade que o programa descobriu.

---

## Oito critérios, respostas diferentes

As secções anteriores fizeram ao mesmo projeto três perguntas — quanta água entrega, quanto dinheiro rende, quanto carbono evita — e receberam três respostas que não coincidem. O multicritério do programa junta-lhes uma quarta, estrutural: quanto pesa o sistema e quanta água deita fora. São oito critérios em quatro eixos, calculados para os sete volumes candidatos, todos em polietileno.

<!-- inclui: _tabelas/cap12_multicriterio.md -->

Leia as colunas por eixo, porque cada eixo junta critérios que puxam em sentidos opostos:

- **Técnico.** A fiabilidade volumétrica — a parte da procura pluvial que a cisterna satisfaz — sobe com o volume, de 44,0% a 77,9%. A eficiência de armazenamento — a água entregue por dia sobre o volume construído — cai, de 7,39% para 1,09% ao dia: a cisterna grande guarda água que ninguém usa.
- **Económico.** O VAL é negativo em todos os volumes (os custos são ilustrativos, não são preços de mercado), e a menor perda está em 1 000 L. O custo nivelado da água (LCOW) desenha um U, com o mínimo em 3 000 L (15,65 €/m³). Nenhum volume recupera o investimento: o período de recuperação entra com a mesma penalização em todos e não pesa na escolha.
- **Ambiental.** As emissões líquidas são mínimas em 2 000 L (−31 kg CO₂e em vinte anos). A partir dos 5 000 L, o polietileno acrescenta mais carbono do que a água evitada retira.
- **Estrutural.** A massa a seco do sistema sobe com o volume, de 91 kg para 333 kg; o extravasamento desce, de 44,3 para 23,1 m³ por ano.

==Nenhum volume vence em todos os critérios.== Cada um tem o ótimo num ponto diferente da curva, e a escolha entre eles não é uma questão técnica com resposta única: é uma questão de prioridade, que quem decide tem de declarar. É essa a lacuna que o método multicritério preenche.

---

## Como o TOPSIS resolve

O programa ordena os volumes pelo TOPSIS sobre os oito critérios:

<!-- tabela: Os oito critérios do multicritério, o eixo e o sentido de preferência de cada um -->
| Eixo | Critério | Sentido |
| :--- | :--- | :--- |
| técnico | fiabilidade volumétrica | maximizar |
| técnico | eficiência de armazenamento | maximizar |
| económico | economia financeira líquida (VAL) | maximizar |
| económico | custo nivelado da água (LCOW) | minimizar |
| económico | período de recuperação descontado | minimizar |
| ambiental | CO₂e de ciclo de vida | minimizar |
| estrutural | massa a seco dos materiais | minimizar |
| estrutural | extravasamento anual | minimizar |

O método funciona em quatro passos encadeados. Primeiro, normaliza a matriz de decisão, para que critérios medidos em unidades incomparáveis — percentagens, euros, quilogramas e anos — passem a ocupar a mesma escala. Depois, aplica os pesos declarados. Calcula então, para cada volume, a distância euclidiana à solução ideal, formada pelos melhores valores de cada critério, e à solução anti-ideal, formada pelos piores. Por fim, ordena os volumes pela proximidade relativa ao ideal, conforme a formulação da secção {{n:32}}.

**Os pesos têm dois níveis.** Cada eixo recebe um peso — 25% em cada um, por omissão — e o peso do eixo reparte-se pelos seus critérios segundo as *partes no eixo*, iguais por omissão. Com os quatro eixos iguais, os dois critérios técnicos e os dois estruturais valem 12,5% cada, os três económicos 8,3% cada e o ambiental 25%. No separador de decisão, os quatro pesos têm um controlo cada, e as partes ficam na linha «Partes no eixo», com o botão «Partes iguais»; na linha de comandos, são as opções `--weights` e `--criterion-shares` (secção {{n:19}}).

Aplicado ao projeto do tutorial com os quatro eixos a 25% e partes iguais, o método indica **3 000 L**. A margem é mínima: 3 000 L ficam à frente de 2 000 L por 0,0004 de pontuação (secção {{n:32}}), uma diferença que nenhum dado de entrada sustenta. Para efeitos práticos, os dois volumes empatam.

> **Três declarações que um estudo publicado tem de fazer.**
>
> A normalização do programa é uma **variante** de Hwang e Yoon: translada por `x − min(x)` antes da normalização vetorial, para admitir um VAL negativo. É uma escolha deliberada, e apresentá-la como TOPSIS canónico seria incorreto.
>
> O SMAA-VIKOR, disponível ao lado, sorteia oito pesos e devolve a probabilidade de cada volume ocupar cada posição. É a resposta certa quando não há consenso sobre os pesos.
>
> As condições C1 e C2 de Opricovic, de vantagem aceitável e de estabilidade, **não estão implementadas**. A secção {{n:32}} detalha.

---

O separador de decisão apresenta a pontuação de cada volume candidato ({{fig:fig51_programa_topsis}}).

![A pontuação multicritério de cada volume candidato](../figuras/fig51_programa_topsis.png)

*Figura 99 — O gráfico do separador de decisão: a pontuação de proximidade ao ideal de cada volume candidato, com o vencedor destacado, para os quatro eixos a 25%. Pontuações próximas entre si significam alternativas equivalentes, e nesse caso a escolha passa a depender do peso declarado. Figura gerada pelo próprio programa.*

---
## O peso muda a resposta

A tabela seguinte mostra o que acontece quando um eixo recebe 70% do peso e os outros três 10% cada, os perfis «Priorizar …» do separador de decisão.

<!-- inclui: _tabelas/cap12_pesos.md -->

Com 70% no eixo técnico, a escolha **desce** para 1 000 L — o contrário do que o nome sugere. O eixo técnico já não mede só a água entregue: junta a fiabilidade, que sobe com o volume, à eficiência de armazenamento, que cai. Os dois puxam para extremos opostos, e a eficiência, que varia mais depressa nos volumes pequenos (de 7,39% para 4,45% ao dia entre 1 000 e 2 000 L), puxa com mais força. O critério técnico isolado — a maior fiabilidade — continua a apontar para 12 000 L, e o critério hidráulico da secção {{n:7}}, pelo limiar de ganho marginal, para 5 000 L. São três perguntas técnicas diferentes: quanto da procura se satisfaz, quanto do volume construído trabalha, e onde o metro cúbico seguinte deixa de compensar.

Os outros eixos respondem como os seus critérios fazem esperar. Com 70% no económico, vence 3 000 L, o mínimo do LCOW; com 70% no ambiental, 2 000 L, o mínimo das emissões; com 70% no estrutural, 4 000 L, onde a massa que cresce e o extravasamento que desce se equilibram. Nas quatro ponderações da tabela sem o peso técnico dominante, o TOPSIS fica entre 2 000 e 4 000 L.

O ordenamento multicritério escolhe um volume; não diz se se deve construir. Neste tutorial, todos os volumes têm VAL negativo e nenhum período de recuperação, com os custos ilustrativos, pelo que a dimensão financeira argumenta contra construir seja o que for. Se o projeto avançar, é pelas razões que os outros eixos apresentam ou por um fim que o fluxo de caixa não mede, e o relatório tem de o dizer.

> **Declare os pesos.** «Volume ótimo pelo TOPSIS» sem os quatro pesos de eixo e as partes no eixo é uma afirmação impossível de reproduzir. Dois artigos com pesos diferentes chegam a volumes diferentes, e ambos estão certos.

---

Uma solução de compromisso cede em alguma coisa, e convém saber em quê. O programa desdobra a pontuação em oito proximidades, uma por critério, e mostra a distância de cada volume ao melhor valor alcançado em cada critério ({{fig:fig52_programa_proximidade}}).

![A proximidade de cada volume ao ótimo de cada critério](../figuras/fig52_programa_proximidade.png)

*Figura 99 — O segundo gráfico do separador de decisão: o quanto cada volume se aproxima do melhor valor observado em cada um dos oito critérios (100% é o melhor, 0% o pior), com o volume eleito pelo TOPSIS marcado. O período de recuperação, igual em todos os volumes, fica nos 100%; a legenda usa os rótulos do programa, em que a fiabilidade volumétrica aparece como «Confiabilidade volumétrica». É a figura que mostra o que cada volume cede, e em que critério. Figura gerada pelo próprio programa.*

---
## A recomendação do tutorial

O tutorial mantém o reservatório de **5 000 L em polietileno**, o volume que o critério hidráulico da secção {{n:7}} indicou com o limiar de ganho marginal de 1 %/m³. O multicritério de oito critérios, com os quatro eixos iguais, indica um volume menor, 3 000 L. Manter os 5 000 L é uma escolha, e esta secção diz o que ela cede.

Na figura de proximidade, os 5 000 L ganham aos 3 000 L no que depende de mais água: a fiabilidade volumétrica sobe de 58,7% para 65,3%, e o extravasamento desce de 35,1 para 31,0 m³ por ano. Perdem em tudo o resto. A eficiência de armazenamento cai de 3,29% para 2,19% ao dia, o LCOW sobe de 15,65 para 16,22 €/m³, o VAL passa de −5 140 € para −6 053 € (ilustrativos), as emissões líquidas passam de −27 para +8 kg CO₂e, e a massa a seco sobe de 135 para 179 kg. Com os quatro eixos iguais, os 5 000 L ficam em quinto lugar entre sete.

Os 3 000 L são a escolha defensável quando o estudo dá ao dinheiro, ao carbono e ao peso do sistema pelo menos tanto peso como à água, que é o que os pesos iguais declaram. São também a escolha natural quando o espaço ou a estrutura limitam o volume. Os 5 000 L defendem-se quando o objetivo declarado é a água — satisfazer mais procura e deitar menos fora —, aceitando um custo maior por metro cúbico e um sistema mais pesado.

Sob a incerteza dos pesos, nenhum dos dois se impõe. No SMAA-VIKOR, com cinco mil vetores de oito pesos sorteados, 5 000 L ficam em primeiro lugar em 22,2% dos sorteios, 3 000 L em 22,0% e 2 000 L em 19,3% (secção {{n:32}}). Abaixo de 40%, pela régua da secção {{n:20}}, ==a escolha depende dos pesos, e o estudo tem de os declarar==, junto com a segunda opção.

Na versão 0.1.0, com sete critérios, os 5 000 L venciam com pesos iguais, e o critério hidráulico e o multicritério concordavam. Os oito critérios deixam de contar três vezes a mesma água economizada e passam a pesar o volume ocioso, o custo por metro cúbico e a massa do sistema, e a concordância desapareceu. Ela nunca esteve garantida: é por isso que o tutorial fez o caminho longo em vez de parar na secção {{n:7}}.

---

## O projeto, fechado

<!-- tabela: Resumo do projeto do tutorial, com todos os parâmetros e resultados -->
| Triton · moradia unifamiliar em Lisboa (custos ilustrativos, não são preços de mercado) | |
| :--- | ---: |
| série de precipitação | Lisboa, 30 anos, 746 mm/ano |
| área de captação | 150 m² |
| coeficiente de escoamento | 0,85 |
| descarte das primeiras águas | 2,0 mm, todas as chuvadas |
| moradores | 4 |
| procura total | 600 L/dia |
| fração atendível pela chuva | 28% |
| reservatório inferior | 5 000 L, polietileno |
| arranjo de abastecimento | elevação para reservatório superior |
| reservatório superior | 1 000 L, limiar de acionamento de 100 L |
| classe de qualidade | 1, cloragem por pastilhas |
| descarte inicial | câmara de 300 L |
| **potencial de economia de água potável** | **18,28%** |
| dias de atendimento pleno | 64,3% |
| água da chuva consumida | 40,1 m³/ano |
| energia da elevação | 5,3 kWh/ano |
| investimento (ilustrativo) | 6 900 € |
| **valor atual líquido a 20 anos (ilustrativo)** | **−6 053 €** |
| período de recuperação descontado | sem recuperação |
| **emissões líquidas em 20 anos** | **+8 kg CO₂e** |
| retorno do carbono | 20,4 anos |
| **multicritério (quatro eixos a 25%, partes iguais)** | **3 000 L; o tutorial mantém 5 000 L** |

Resta uma etapa, que é comunicar o resultado: um estudo que não é relatado de forma verificável não se distingue, para quem o lê, de um palpite bem apresentado. É o assunto da secção seguinte.
