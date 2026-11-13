# O relatório, e o que declarar num artigo

> No fim desta secção, tem o relatório emitido e, se pretende publicar, a lista do que tem de constar no método do artigo. Essa lista é a parte mais curta e mais importante do manual.

---

## Os três relatórios

O programa emite três relatórios distintos, e a distinção não é de extensão, mas de público e de finalidade. Escolher o relatório errado para o destinatário certo é a forma mais comum de produzir um documento que ninguém lê: um cliente não percorre um inventário de ciclo de vida item a item, e um avaliador de certificação não se satisfaz com uma conclusão de quatro páginas.

O **relatório executivo** tem de quatro a seis páginas e reúne o resultado técnico, o investimento, o retorno e uma conclusão objetiva. É o documento de entrega ao cliente, e a sua virtude é caber numa só leitura, sem exigir que o leitor conheça o método.

O **relatório ambiental e ESG** apresenta o inventário de ciclo de vida discriminado por componente, o saldo de carbono ao longo da vida útil e o enquadramento do projeto nos referenciais tratados na secção {{n:31}} — LEED, EDGE e GRI 303. É o documento que se anexa a um processo de certificação, e a discriminação por componente existe justamente porque um avaliador confere item a item.

O **relatório científico** traz o método completo, as premissas declaradas, a série utilizada e os resultados com a precisão que um artigo exige. É a base sobre a qual se redige uma publicação, e é o único dos três que inclui as figuras analíticas.

Além dos três, a etapa **10. Exportação** gera o desenho esquemático em DXF, o modelo BIM em JSON e folhas de cálculo com a série diária completa e com a varredura de volumes, como detalha a secção {{n:22}}.

---

## O que o relatório não decide por si

==O relatório traz os números; o contexto que os torna reproduzíveis é seu.== Nenhum documento gerado automaticamente pode declarar porque se escolheu aquela série de precipitação, se o consumo per capita adotado foi medido ou tirado da literatura, ou o que justifica a vida útil considerada na avaliação ambiental. É esta informação que permite a um terceiro repetir o estudo e chegar ao mesmo resultado, e é dela que trata o resto desta secção.

---

## A lista de declaração

Um estudo feito no Triton que deixe de declarar qualquer dos itens abaixo não é reproduzível por terceiros e, o que costuma ser pior, não é comparável com outro estudo feito no mesmo programa — porque duas simulações com premissas diferentes produzem números que parecem comparáveis e não são. A lista está organizada pela ordem em que as decisões aparecem no trabalho, e pode seguir-se como roteiro de redação do método.

### Programa e versão

- **Versão do Triton**, com o número completo, e a **edição** (Portugal). As correções de cálculo entre versões deslocam resultados, e sem a versão declarada não há como saber que cálculo produziu o número publicado.

### Série de precipitação

- **Origem**: estação, base ibérica (Iberia01), base de concelhos (E-OBS) ou reanálise.
- Se for a base ibérica ou a de concelhos: **município (com o código) ou concelho, fonte e versão (Iberia01 v1.0 ou E-OBS) e janela temporal**; se for reanálise ou modelo: **produto, cenário, janela temporal** e a resolução da grelha.
- **Recorte**: datas de início e fim, e número de anos.
- **Tratamento de falhas** e critério para descartar um ano incompleto.

### Edifício e procura

- Área de captação e **como foi obtida** — projeção horizontal.
- Coeficiente de escoamento e a sua origem.
- Consumo per capita, e se é **medido ou de referência**.
- **Fração atendível pela água da chuva** e os usos finais que a compõem. É o teto do resultado, e sem ela o potencial não se interpreta.
- Se algum uso está fora da lista que a norma aplicável admite, como a máquina de lavar roupa, e que critério de qualidade foi adotado para ele.

### Arranjo de abastecimento

- **Arranjo**: elevação para reservatório superior, pressurização direta ou gravidade. Define a energia e as eletrobombas no custo e no carbono.
- Na elevação: volume do reservatório, limiar de acionamento e altura manométrica.
- Na pressurização direta: pressão de trabalho e arranques por pessoa e por dia.

### Descarte das primeiras águas

- Lâmina adotada e **modo**, entre os três.
- **O tratamento da lâmina**, se o estudo comparar o Triton com outra ferramenta: algumas ferramentas tratam a lâmina como limiar do evento, o Triton subtrai-a à chuva do dia, e os dois dão resultados diferentes.

### Volume e critério de escolha

- Se veio de uma varredura: **o limiar de ganho marginal adotado**. Sem ele, «volume ideal» não significa nada.
- Se veio do multicritério: **os quatro pesos de eixo e as partes no eixo** (ou os oito pesos de critério), o conjunto de volumes candidatos e o método, TOPSIS ou SMAA-VIKOR.
- **A faixa de escolha e a tolerância**, e não um volume só: «volumes de 2 000 a 3 000 L têm resultados multicritério semelhantes (tolerância de 5% da amplitude das pontuações)». O volume de maior pontuação vai como informação, ao lado da faixa. A faixa depende da grade de volumes avaliada, que também se declara.
- Se usou os **pesos objetivos do CRITIC**: que os usou, e os pesos calculados, por critério ou por eixo. Saem dos resultados do próprio estudo e mudam com o conjunto de volumes avaliado.
- Que a normalização do TOPSIS é uma **variante**, com translação por `x − min(x)`.

### Análise económica

- **Concelho e entidade gestora**, com a data de entrada em vigor do tarifário.
- **Regime de mínimo**, entre os seis. É o que mais altera resultados entre entidades gestoras.
- Percentagem do saneamento, e que incide sobre a **parcela da água** da fatura.
- Taxa de atualização, inflação, período de análise.
- **Atualizações tarifárias** da água, do saneamento e da energia, com o intervalo.
- Se os custos são orçamentos ou valores ilustrativos.

### Avaliação do ciclo de vida

- **Fronteira**: água entregue, e não produzida.
- **Vida útil** adotada e a sua justificação.
- **Material** do reservatório. Pesa muito no resultado, como a secção {{n:11}} mostra.
- Base do fator de emissão da rede elétrica, **com o ano**.
- Que fatores são **aproximações** e quais levam **etiqueta de triagem**.

### Certificações

- Que as classes 2 a 4 de qualidade são **adaptações do programa**, e não de uma norma.
- No caso do LEED, a **versão** do referencial: v4/v4.1 ou v5.
- No caso do EDGE, que o programa avalia **apenas a barra da água**, e que o caso de base usado é o declarado ou a procura modelada.

---

## O parágrafo pronto

Para o nosso projeto, o método ficaria assim:

> A simulação foi conduzida no Triton 0.2.0, Edição Ibérica, com um modelo comportamental de passo diário (extravasamento calculado antes da retirada da procura, com a chuva do dia disponível para o consumo do dia, uma ordem intermédia entre YAS e YBS), sobre uma série de precipitação de 30 anos para Lisboa (Iberia01, município de Lisboa [PT-1106], 1986 a 2015; 10 957 dias, média de 746 mm/ano). Adotou-se uma área de captação de 150 m² em projeção horizontal, um coeficiente de 0,85, valor redondo para a eficiência de captação combinada, e um descarte das primeiras águas de 2,0 mm em todas as chuvadas, subtraído à lâmina diária. A procura total adotada foi de 600 L/dia (4 moradores, 150 L/hab·dia), com uma fração atendível pela água da chuva de 28%, correspondente ao autoclismo e aos usos exteriores. O volume de 5 000 L resultou do critério do ganho marginal com limiar de 1 %/m³. Uma análise multicritério TOPSIS com oito critérios em quatro eixos (técnico, económico, ambiental e estrutural), pesos de 25% por eixo e partes iguais no eixo, com normalização numa variante de Hwang e Yoon transladada por x − min(x), deu uma faixa de escolha de 2 000 a 3 000 L entre sete volumes candidatos de 1 000 a 12 000 L (volumes com pontuação a até 5% da amplitude da maior); manteve-se o volume hidráulico, que satisfaz mais procura pluvial e extravasa menos, à custa de um custo nivelado da água e de uma massa maiores. Os pontos de uso são abastecidos por elevação para um reservatório superior de 1 000 L, com limiar de acionamento de 100 L, duas eletrobombas de 0,5 cv e o rendimento de motor predefinido do programa. A análise económica usou o tarifário de Lisboa em vigor desde 01/01/2026 (água da EPAL com o adicional da Câmara Municipal, saneamento e resíduos da Câmara), uma taxa de atualização de 0,4% ao mês, uma inflação de 0,2% ao mês, atualizações de 3% ao ano com intervalos de 12 meses e um período de 20 anos; todos os custos foram valores redondos ilustrativos, não são preços de mercado. A avaliação do ciclo de vida adotou a fronteira da água entregue, fatores de emissão ilustrativos de 0,40 kg CO₂e/kWh e 0,50 kg CO₂e/m³, um reservatório de polietileno e uma vida útil de 20 anos.

São menos de quatrocentas palavras, e são a diferença entre um estudo que outro investigador consegue repetir e um número solto que ninguém pode verificar. A extensão é modesta perante o que se ganha: um método assim redigido responde antecipadamente à maior parte das perguntas que um revisor faria.

---

## O fim do tutorial

Dez secções, um único projeto acompanhado do princípio ao fim, e um estudo completo: partiu de uma moradia sem sistema e chegou a uma recomendação de volume, material, classe de qualidade e a um veredicto sobre a viabilidade económica e ambiental — negativo em ambas, com os custos ilustrativos e a tarifa de Lisboa, mesmo depois de trocar o material —, com cada decisão justificada pelo número que a sustentou. O quadro da secção {{n:12}} reúne o resultado consolidado.

O caminho a seguir depende do que pretende fazer a seguir:

- **Resolver um caso diferente do tutorial** — o capítulo {{c:3}}, os guias de tarefa.
- **Perceber de onde vem cada número** — o capítulo {{c:4}}, o método.
- **Não cometer os erros que o programa não impede** — a secção {{n:33}}.
- **Defender o estudo perante um revisor** — o capítulo {{c:6}}.
