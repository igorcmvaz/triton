# Volume ideal e a varredura

> Esta seção formaliza o que a seção {{n:7}} fez na prática: como o programa monta a
> grade de volumes e como aplica o critério de volume ideal.

---

## A grade discreta

A varredura simula um conjunto **finito** de volumes, e a montagem desse conjunto
tem três regras.

**O passo é arredondado para cima até o múltiplo de 250 litros.** É o quantum
comercial: reservatórios são vendidos em volumes padronizados, e um ótimo em 1.300 L
não é comprável. Quando o passo pedido não é múltiplo de 250, o programa ajusta e
registra o ajuste em `step_adjusted`, de modo que o relatório possa declarar o passo
efetivo.

**O número de volumes positivos é limitado a 40.** Uma varredura de 0 a 50.000 L com
passo de 100 L seriam 500 simulações de trinta anos, e o ganho de informação não paga
o custo. Quando o limite é atingido, o passo efetivo cresce.

**O volume máximo informado é sempre preservado** como último ponto da grade. Só o
último intervalo pode, portanto, ser menor que o passo efetivo.

O volume **zero** entra na grade como alternativa de referência: é o cenário sem
sistema, contra o qual os demais se comparam.

---

A consequência prática aparece na {{fig:fig14_grade}}. Com passo fino, a curva mostra o
joelho onde o retorno começa a decair; com passo grosseiro, o joelho cai entre dois
pontos da grade e o critério elege o primeiro volume tabulado depois dele, que pode estar
vários metros cúbicos adiante do volume que de fato interessa.

![A mesma curva vista por duas grades de varredura](../figuras/fig14_grade.png)

*Figura 99 — Curva de potencial de economia da mesma edificação, varrida com passo de 250 L e com passo de 5.000 L. A grade grossa calcula corretamente cada ponto que contém, mas não contém o trecho de maior curvatura, entre 1 e 5 m³.*

---

## O ganho marginal

A curva de potencial de economia contra volume é monotônica e côncava: cada metro
cúbico acrescentado ao reservatório rende menos que o anterior, e o rendimento tende a
zero à medida que o sistema se aproxima do teto imposto pela fração atendível. O
programa quantifica esse rendimento decrescente pela derivada discreta da curva,
calculada para cada volume da grade a partir do segundo.

```equacao:ganho_marginal
Δ(V_i) = [ Epot(V_i) − Epot(V_i−1) ] ÷ [ (V_i − V_i−1) ÷ 1000 ]
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Δ(V_i)` | ganho marginal do volume `V_i` em relação ao anterior | %/m³ |
| `Epot(V_i)` | potencial de economia de água potável obtido com o volume `V_i` | % |
| `Epot(V_i−1)` | potencial de economia obtido com o volume imediatamente menor | % |
| `V_i` | volume do reservatório na posição `i` da grade | L |
| `V_i−1` | volume imediatamente menor da grade | L |
| `1000` | conversão de litros para metros cúbicos | L/m³ |

A divisão por mil no denominador da Equação {{eq:ganho_marginal}} existe para que o
resultado saia em pontos percentuais por metro cúbico acrescentado, que é a unidade em
que a decisão é tomada — reservatórios são comprados e orçados em metros cúbicos, não
em litros.

==Por ser uma derivada discreta, o ganho marginal depende do passo da grade.== Uma
grade fina produz um valor mais local, próximo da derivada verdadeira naquele ponto;
uma grade grossa produz a média do rendimento ao longo de um intervalo maior. A
subseção sobre sensibilidade ao passo, adiante, mede o tamanho desse efeito.

---

## O critério de volume ideal

O volume ideal é definido como o menor volume positivo da grade cujo ganho marginal já
tenha caído abaixo de um limiar declarado pelo usuário.

```equacao:volume_ideal
V_ideal = min { V_i > 0 : Δ(V_i) ≤ Δ_lim }
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_ideal` | volume ideal pelo critério de ganho marginal | L |
| `V_i` | volume do reservatório na posição `i` da grade | L |
| `Δ(V_i)` | ganho marginal do volume `V_i`, da Equação {{eq:ganho_marginal}} | %/m³ |
| `Δ_lim` | limiar de ganho marginal declarado pelo usuário; o programa abre com 5,0, e o tutorial adota 1,0 | %/m³ |

Quando nenhum volume da grade satisfaz a condição da Equação {{eq:volume_ideal}} —
situação que ocorre quando a faixa varrida termina antes de a curva achatar — o
programa adota o maior volume da grade e registra essa circunstância no relatório, de
modo que o leitor saiba que o ótimo encontrado é um limite da busca e não um ponto de
inflexão da curva. O capítulo 7 do Manual do Netuno 4 trata o mesmo caso, e a conduta
adotada aqui é a mesma.

> **O critério é hidráulico e só hidráulico.** Ele ignora custo, tarifa e carbono. Um
> volume ideal por este critério não é uma recomendação de projeto; é o ponto em que a
> curva de aproveitamento deixa de compensar **em água**. A seção {{n:32}} trata da
> escolha com os demais critérios, que frequentemente apontam para volumes diferentes.

---

Este é um critério entre outros igualmente defensáveis, e convém deixar isso
explícito. Um projetista que queira o máximo desempenho hídrico escolherá o maior volume
da varredura; um que responda por um orçamento escolherá o volume de maior valor
presente líquido; o critério de ganho marginal fica entre os dois, por ser o que identifica
onde a curva deixa de compensar. Os três leem a mesma varredura e não precisam coincidir:
neste projeto o técnico e o econômico apontam o mesmo volume, e o de máximo desempenho
aponta outro. Nenhum dos três está errado — errado é não dizer qual deles foi usado. A {{fig:fig09_criterios}} marca o volume eleito por cada critério.

![A mesma varredura lida por três critérios](../figuras/fig09_criterios.png)

*Figura 99 — Varredura do projeto do tutorial lida por três critérios: (a) potencial de economia e (b) valor presente líquido do mesmo conjunto de volumes. As linhas verticais marcam o volume eleito pelo ganho marginal abaixo de 1 %/m³ e pelo VPL máximo, ambos em 5 m³, e pelo potencial máximo, em 20 m³.*

---

## A sensibilidade ao passo

O volume ideal depende do passo da varredura, e convém saber quanto.

Um passo grosso salta o joelho da curva: com passo de 5.000 L, o primeiro ponto
avaliado após o zero já tem ganho marginal médio de todo o intervalo, que é alto, e
o segundo pode já estar abaixo do limiar. O ideal sai deslocado para cima.

Um passo fino resolve melhor o joelho, ao custo de tempo.

**Recomendação prática:** passo entre 500 e 1.000 L para reservatórios residenciais,
e entre 2.000 e 5.000 L para edificações de grande porte, sempre declarando o passo
adotado junto do volume ideal.

---

## Por que a curva tem esta forma

A curva de aproveitamento pluvial é côncava e assintótica, sempre. Duas razões:

**Os eventos pequenos são a maioria.** Os primeiros litros de armazenamento capturam
as chuvas frequentes e pequenas, que respondem pela maior parte dos dias. Os últimos
litros só servem para os poucos eventos extremos.

**A fração atendível é um teto.** O potencial não pode ultrapassar a fração da
demanda que a chuva atende, definida na seção {{n:5}}. A curva se aproxima desse teto e
nunca o cruza — invariante que a suíte de testes verifica até volumes de 100 m³.

---

## O que a varredura não responde

- **Qual volume comprar.** Reservatórios existem em volumes comerciais; o ideal
  calculado deve ser arredondado para o volume disponível mais próximo, e a
  varredura já ajuda ao trabalhar em múltiplos de 250 L.
- **Se o sistema vale a pena.** Isso é a seção {{n:29}}.
- **Se o volume cabe no terreno.** O programa não conhece o sítio.
