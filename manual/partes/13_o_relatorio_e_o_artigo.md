# O relatório, e o que declarar num artigo

> Ao terminar esta seção você terá o relatório emitido e, se pretende publicar, a
> lista do que precisa constar no método do artigo. Essa lista é a parte mais
> curto e o mais importante do manual.

---

## Os três relatórios

O programa emite três relatórios distintos, e a distinção não é de extensão, mas de
público e de finalidade. Escolher o relatório errado para o destinatário certo é a
forma mais comum de produzir um documento que ninguém lê: um cliente não percorre um
inventário de ciclo de vida item a item, e um avaliador de certificação não se satisfaz
com uma conclusão de quatro páginas.

O **relatório executivo** ocupa de quatro a seis páginas e reúne o resultado técnico, o
investimento, o retorno e uma conclusão objetiva. É o documento de entrega ao cliente, e
sua virtude é a de caber numa leitura única, sem exigir que o leitor conheça o método.

O **relatório ambiental e ESG** apresenta o inventário de ciclo de vida discriminado por
componente, o saldo de carbono ao longo da vida útil e o enquadramento do projeto nos
cinco referenciais tratados na seção {{n:31}} — LEED, AQUA-HQE, Selo Casa Azul, EDGE e
GRI 303. É o documento que se anexa a um processo de certificação, e a discriminação por
componente existe justamente porque um avaliador confere item a item.

O **relatório científico** traz o método completo, as premissas declaradas, a série
utilizada e os resultados com a precisão que um artigo exige. É a base sobre a qual se
redige uma publicação, e é o único dos três que inclui as figuras analíticas.

Além dos três, a etapa **10. Exportação** gera o desenho esquemático em DXF, o modelo
BIM em JSON e planilhas com a série diária completa e com a varredura de volumes, conforme a
seção {{n:22}} detalha.

---

## O que o relatório não decide por você

==O relatório traz os números; o contexto que os torna reproduzíveis é seu.== Nenhum
documento gerado automaticamente pode declarar por que aquela série de precipitação foi
escolhida, se o consumo per capita adotado foi medido ou tomado da literatura, ou qual
a justificativa da vida útil considerada na avaliação ambiental. São essas informações
que permitem a um terceiro repetir o estudo e chegar ao mesmo resultado, e é delas que
trata o restante desta seção.

---

## A lista de declaração

Um estudo conduzido no Netuno que deixe de declarar qualquer dos itens abaixo não é
reproduzível por terceiros e, o que costuma ser pior, não é comparável com outro estudo
feito no mesmo programa — porque duas simulações com premissas diferentes produzem
números que parecem comparáveis e não são. A lista está organizada na ordem em que as
decisões aparecem no trabalho, e pode ser percorrida como roteiro de redação do método.

### Programa e versão

- **Versão do Netuno**, com o número completo. Correções de cálculo entre versões
  deslocam resultados, e sem a versão declarada não há como saber qual conta produziu o
  número publicado.

### Série de precipitação

- **Origem**: estação, base nacional, ou modelo climático.
- Se for base nacional: **modelo, cenário e janela temporal**.
- **Recorte**: datas de início e fim, e número de anos.
- **Tratamento de falhas** e critério de descarte de ano incompleto.

### Edificação e demanda

- Área de captação e **como foi obtida** — projeção horizontal.
- Coeficiente de escoamento e sua origem.
- Consumo per capita e se é **medido ou de referência**.
- **Fração atendível por água pluvial** e os usos finais que a compõem. É o teto do
  resultado, e sem ele o potencial não se interpreta.

### Descarte de primeiras águas

- Lâmina adotada e **modo** entre os três.
- **A divergência em relação ao Netuno 4**, se o estudo comparar as versões: o
  Netuno 4 trata a lâmina como limiar do evento, o Netuno 5 a subtrai, e a diferença
  vale de 2,3 a 2,7 pontos percentuais de economia sobre 4.050 casos de referência.

### Volume e critério de escolha

- Se veio de varredura: **limiar de ganho marginal adotado**. Sem ele, «volume
  ideal» não significa nada.
- Se veio de multicritério: **os pesos dos sete critérios** e o método, TOPSIS ou
  SMAA-VIKOR.
- Que a normalização do TOPSIS é uma **variante** com translação por `x − min(x)`.

### Análise econômica

- **Município e concessionária**, com a data de vigência da tabela tarifária.
- **Regime de mínimo** entre os cinco. É o que mais muda resultado entre municípios.
- Percentual de esgoto, e que ele incide sobre a **parcela de água** da fatura.
- Taxa mínima de atratividade, inflação, período de análise.
- **Reajustes tarifários** de água, esgoto e energia, com o intervalo.

### Avaliação de ciclo de vida

- **Fronteira**: água entregue, e não produzida.
- **Vida útil** adotada e sua justificativa.
- **Material** do reservatório. Ele inverte o sinal do resultado, como a seção {{n:11}}
  mostra.
- Base do fator de emissão da rede elétrica, **com o ano**.
- Quais fatores carregam **rótulo de triagem**.

### Certificações

- Que as classes 2 a 4 de qualidade são **adaptações do programa**, não da NBR 15527.
- No caso do LEED, a **versão** do referencial: v4/v4.1 ou v5.
- No caso do EDGE, que o programa avalia **apenas a barra de água**, e que o
  caso-base usado é o declarado ou a demanda modelada.

---

## O parágrafo pronto

Para o nosso projeto, o método ficaria assim:

> A simulação foi conduzida no Netuno 5.0.0, com modelo comportamental de base
> diária (YAS, extravasamento anterior à retirada da demanda), sobre série de
> precipitação de Florianópolis com 30 anos (10.950 dias, média de 1.795 mm/ano).
> Adotou-se área de captação de 150 m² em projeção horizontal, coeficiente de
> escoamento de 0,85, adotado a partir da eficiência de captação η que a ABNT NBR 15527:2019
> recomenda no item 4.1.6, e descarte de primeiras águas de 2,0 mm em
> todo evento, subtraído da lâmina diária — divergência deliberada em relação ao
> Netuno 4, que trata o valor como limiar do evento. A demanda total adotada foi de
> 600 L/dia (4 moradores, 150 L/hab·dia), com fração atendível por água pluvial de
> 40%, correspondente a bacia sanitária, máquina de lavar e usos externos. O volume
> de 5.000 L resultou do critério de ganho marginal com limiar de 1 %/m³ e foi
> confirmado por análise multicritério TOPSIS com pesos iguais sobre sete critérios,
> com normalização em variante de Hwang e Yoon translada por x − min(x). A análise
> econômica utilizou a estrutura tarifária da CASAN vigente desde 01/04/2026, regime
> de disponibilidade, esgoto a 100% do valor da água, TMA de 0,5% ao mês, inflação
> de 0,35% ao mês, reajustes de 5% ao ano em intervalos de 12 meses e período de 20
> anos. A avaliação de ciclo de vida adotou fronteira de água entregue, reservatório
> em polietileno e vida útil de 20 anos.

São cerca de duzentas e cinquenta palavras, e elas são a diferença entre um estudo que
outro pesquisador consegue repetir e um número solto que ninguém pode verificar. A
extensão é modesta diante do que se ganha: um método assim redigido responde
antecipadamente à maior parte das perguntas que um parecerista faria.

---

## O fim do tutorial

Dez seções, um único projeto acompanhado do início ao fim, e um estudo completo: partiu
de uma residência sem sistema e chegou a uma recomendação de volume, material, classe de
qualidade e viabilidade econômica e ambiental, com cada decisão justificada pelo número
que a sustentou. A tabela da seção {{n:12}} reúne o resultado consolidado.

O caminho a seguir depende do que você pretende fazer em seguida:

- **Resolver um caso diferente do tutorial** — o capítulo {{c:3}}, os guias de tarefa.
- **Entender de onde vem cada número** — o capítulo {{c:4}}, o método.
- **Não cometer os erros que o programa não impede** — a seção {{n:33}}.
- **Defender o estudo diante de um revisor** — o capítulo {{c:6}}.
