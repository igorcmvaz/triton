# 7. Escolher o volume

> Ao terminar este capítulo você terá a curva de retorno do reservatório, saberá
> onde ela deixa de compensar, e entenderá por que **não existe** um volume ótimo
> absoluto — existe um volume ótimo para um critério declarado.

O capítulo 6 chutou 3.000 L e viu 303 L/dia transbordando. A pergunta agora é
direta: **quanto reservatório vale a pena?**

O Netuno responde rodando a mesma simulação para muitos volumes. É a **varredura**.

---

## 7.1. Rodar a varredura

Na aba **Varredura**, informe o volume máximo e o passo. Para o nosso projeto:
máximo de 20.000 L, passo de 1.000 L.

Duas coisas acontecem que convém saber:

**O passo é arredondado para cima**, até o múltiplo de 250 L. É o quantum comercial
de reservatório: não se compra cisterna de 1.300 L. Se você pedir um passo que não
seja múltiplo de 250, o programa ajusta e **registra que ajustou**.

**A grade é limitada a 40 volumes positivos.** Uma varredura de 0 a 50.000 L com
passo de 100 L seriam 500 simulações de trinta anos cada, e o ganho de informação
não paga o tempo. O volume máximo informado é sempre preservado como último ponto,
de modo que só o último intervalo pode ser menor que o passo.

O volume **zero** entra na grade como referência: é o cenário sem sistema, contra o
qual tudo se compara.

---

## 7.2. A curva

<!-- inclui: _tabelas/cap07_varredura.md -->

![Curva de potencial e curva de ganho marginal](../figuras/fig02_curva_de_retorno.png)

*Figura 2 — À esquerda, o potencial se aproximando do teto de 40% e nunca o cruzando. À direita, o ganho marginal em escala logarítmica: três ordens de grandeza entre o primeiro metro cúbico e o vigésimo.*

Leia a coluna **ganho por m³ acrescentado**. Ela é a derivada da curva, e é onde
está a decisão.

| De → para | Ganho por m³ |
| :--- | ---: |
| 0 → 1.000 L | 25,32 %/m³ |
| 1.000 → 2.000 L | 6,59 %/m³ |
| 2.000 → 3.000 L | 3,01 %/m³ |
| 3.000 → 4.000 L | 1,61 %/m³ |
| 5.000 → 6.000 L | 0,64 %/m³ |
| 10.000 → 12.000 L | 0,15 %/m³ |
| 16.000 → 20.000 L | 0,02 %/m³ |

O primeiro metro cúbico entrega 25 pontos percentuais. O décimo sexto entrega dois
centésimos. **Mil vezes menos**, pelo mesmo metro cúbico de concreto e pela mesma
escavação.

Isso não é peculiaridade de Florianópolis. É a forma de toda curva de
aproveitamento pluvial, e vem de dois fatos: os primeiros litros de armazenamento
capturam os eventos pequenos, que são a maioria; e o teto de 40% da fração
atendível puxa a curva para a horizontal.

---

## 7.3. O volume ideal

O Netuno adota o critério do **ganho marginal**: o volume ideal é o **menor** volume
cujo ganho por metro cúbico acrescentado cai abaixo de um limiar que você define.

O limiar padrão é **1 %/m³**. Na nossa varredura, o primeiro volume a cair abaixo
disso é o de **5.000 L**, com 0,93 %/m³.

| | |
| :--- | ---: |
| volume ideal, limiar de 1 %/m³ | 5.000 L |
| potencial nesse volume | 37,46% |
| de um teto de | 40% |
| dias de atendimento pleno | 92,9% |

**O limiar é uma escolha sua, e ela decide o resultado:**

<!-- inclui: _tabelas/cap07_limiar_e_custo.md -->

O programa não tem opinião sobre qual limiar é o certo — ele aplica o que você
declarar.

> **Num estudo publicado, declare o limiar.** Dois artigos com «volume ideal» de
> limiares diferentes não são comparáveis, e a diferença aqui é de 3.000 L e dois
> pontos percentuais.

---

## 7.4. Por que o critério do ganho marginal não basta

O critério de 7.3 é puramente **hidráulico**. Ele não sabe quanto custa o
reservatório, quanto vale o metro cúbico de água na sua cidade, nem quanto carbono
o concreto carrega.

Repare no que ele ignora:

- Se a água for muito cara, o ganho de 0,64 %/m³ do sexto metro cúbico pode se pagar
  bem, e o volume econômico será **maior** que o hidráulico.
- Se a cisterna for cara ou o espaço for escasso, o inverso.
- Uma cisterna de concreto de 20 m³ pesa vinte e quatro toneladas e carrega, com o
  resto do sistema, cerca de **3,5 toneladas de CO₂e** incorporado, contra menos de
  uma tonelada na de 5 m³. O ganho ambiental de 0,02 %/m³ do último metro cúbico não
  chega perto de compensar a diferença.

Três critérios, três respostas diferentes para a mesma pergunta.

É por isso que o tutorial não para aqui. Os capítulos 10 e 11 acrescentam o dinheiro
e o carbono, e o capítulo 12 põe os três na mesma mesa, com pesos declarados, para
escolher um volume de compromisso.

> **O engano mais comum, e está no capítulo 33.** Publicar o volume de maior economia
> de água como se fosse o volume recomendado. Pela tabela, 20.000 L dão o maior
> potencial, 39,98%. Também custam **3,3 vezes mais** que os 5.000 L, e carregam
> **3,6 vezes mais carbono incorporado**, para entregar 2,53 pontos percentuais a
> mais.

---

## 7.5. Duas leituras a mais da tabela

**O extravasamento nunca zera.** De 513 L/dia sem reservatório, cai para 272 L/dia
com 20 m³ e para por aí. Mais da metade da água que cai na cobertura vai continuar
indo para a drenagem, porque a demanda simplesmente não a consome. Sistemas de
aproveitamento pluvial não retêm água da chuva por retê-la — quem quer amortecimento
de cheia precisa de um reservatório de detenção, que é outro projeto.

**A confiabilidade sobe mais depressa que o potencial.** De 3.000 para 5.000 L o
potencial ganha 2,5 pontos, mas os dias plenos vão de 85,7% para 92,9%. Se o
critério do projeto for conforto de uso e não economia de conta, a leitura da tabela
muda.

---

## 7.6. O que temos até aqui

Adote **5.000 L** e siga. É o volume ideal pelo critério hidráulico padrão, e é o
que o tutorial carrega até o capítulo 12 — onde ele será questionado de novo, agora
com dinheiro e carbono na conta.

| Projeto até aqui | |
| :--- | ---: |
| série | Florianópolis, 30 anos |
| área de captação | 150 m² |
| demanda total | 600 L/dia |
| fração atendível | 40% |
| **volume do reservatório** | **5.000 L** |
| potencial de economia | 37,46% |
| dias de atendimento pleno | 92,9% |

Falta decidir uma coisa antes de falar de dinheiro: essa água precisa subir para
uma caixa d'água? É o capítulo 8.
