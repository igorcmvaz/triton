# 24. Volume ideal e a varredura

> Este capítulo formaliza o que o capítulo 7 fez na prática: como o programa monta a
> grade de volumes e como aplica o critério de volume ideal.

---

## 24.1. A grade discreta

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

## 24.2. O ganho marginal

Para cada volume da grade a partir do segundo, o programa calcula:

```
Δ(V_i) = [ Epot(V_i) − Epot(V_i−1) ] ÷ [ (V_i − V_i−1) ÷ 1000 ]
```

em que `Epot` é o potencial de economia de água potável em percentual e o
denominador converte a diferença de volume para metros cúbicos. A unidade de `Δ` é
**por cento por metro cúbico acrescentado**.

É uma derivada discreta, e por isso depende do passo: uma grade mais fina dá um
`Δ` mais local; uma grade grossa dá a média de um intervalo maior.

---

## 24.3. O critério de volume ideal

```
V_ideal = menor V_i > 0 tal que Δ(V_i) ≤ limiar
```

O limiar é declarado pelo usuário. O padrão é 1 %/m³.

Se nenhum volume da grade satisfizer a condição — porque a faixa varrida terminou
antes de a curva achatar — o programa adota o **maior volume da grade** e assim o
reporta. O capítulo 7 do Manual do Netuno 4 trata o mesmo caso, e a conduta aqui é a
mesma.

> **O critério é hidráulico e só hidráulico.** Ele ignora custo, tarifa e carbono.
> Um volume ideal por este critério não é uma recomendação de projeto; é o ponto em
> que a curva de aproveitamento deixa de compensar **em água**. O capítulo 32 trata
> da escolha com os demais critérios.

---

## 24.4. A sensibilidade ao passo

O volume ideal depende do passo da varredura, e convém saber quanto.

Um passo grosso salta o joelho da curva: com passo de 5.000 L, o primeiro ponto
avaliado após o zero já tem ganho marginal médio de todo o intervalo, que é alto, e
o segundo pode já estar abaixo do limiar. O ideal sai deslocado para cima.

Um passo fino resolve melhor o joelho, ao custo de tempo.

**Recomendação prática:** passo entre 500 e 1.000 L para reservatórios residenciais,
e entre 2.000 e 5.000 L para edificações de grande porte, sempre declarando o passo
adotado junto do volume ideal.

---

## 24.5. Por que a curva tem esta forma

A curva de aproveitamento pluvial é côncava e assintótica, sempre. Duas razões:

**Os eventos pequenos são a maioria.** Os primeiros litros de armazenamento capturam
as chuvas frequentes e pequenas, que respondem pela maior parte dos dias. Os últimos
litros só servem para os poucos eventos extremos.

**A fração atendível é um teto.** O potencial não pode ultrapassar a fração da
demanda que a chuva atende, definida no capítulo 5. A curva se aproxima desse teto e
nunca o cruza — invariante que a suíte de testes verifica até volumes de 100 m³.

---

## 24.6. O que a varredura não responde

- **Qual volume comprar.** Reservatórios existem em volumes comerciais; o ideal
  calculado deve ser arredondado para o volume disponível mais próximo, e a
  varredura já ajuda ao trabalhar em múltiplos de 250 L.
- **Se o sistema vale a pena.** Isso é o capítulo 29.
- **Se o volume cabe no terreno.** O programa não conhece o sítio.
