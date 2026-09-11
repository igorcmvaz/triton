# Usar cenário climático futuro

> **Pergunta que este guia responde:** o sistema que dimensiono hoje ainda serve em
> 2060?

Um reservatório de água pluvial dura trinta anos ou mais, e a chuva que cairá sobre a
edificação ao longo desse período não será a mesma que caiu no passado recente. Dimensionar
um sistema de vida longa exclusivamente sobre a série histórica supõe, implicitamente, um
clima estacionário — suposição que as projeções disponíveis não sustentam. O Netuno traz
uma base de projeções climáticas justamente para que o dimensionamento possa incorporar
essa questão de forma explícita.

---

## O que a base tem

| | |
| :--- | ---: |
<!-- tabela: Conteúdo da base climática nacional distribuída com o programa -->
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 3 |
| janelas temporais | 3 |

O CMIP6 é a sexta fase do *Coupled Model Intercomparison Project*, o exercício
coordenado internacionalmente que alimenta os relatórios do IPCC. Cada modelo é um
modelo climático global de um centro de pesquisa diferente.

> **A base é distribuída à parte do programa**, porque ocupa cerca de 6,5 GB em
> trinta e sete mil arquivos. Sem ela instalada, a etapa de Projeto e Chuva oferece apenas o
> carregamento de arquivo próprio, e as etapas dependentes avisam. A seção {{n:2}} explica
> como obtê-la.

---

## Escolher modelo, cenário e janela

O **cenário** representa a trajetória futura de emissões de gases de efeito estufa, e os
três disponíveis seguem as *Shared Socioeconomic Pathways* adotadas pelo IPCC. Eles não
são previsões, e sim hipóteses coerentes sobre o comportamento socioeconômico global ao
longo do século.

| Cenário | Trajetória |
| :--- | :--- |
| SSP1-2.6 | emissões caem rápido; aquecimento contido perto de 2 °C |
| SSP2-4.5 | trajetória intermediária, próxima das políticas atuais |
| SSP5-8.5 | emissões altas, sem mitigação efetiva |

A **janela temporal** define o período de trinta anos sobre o qual a projeção é tomada,
e as três disponíveis correspondem a futuro próximo, médio e distante. A escolha da
janela deve guardar relação com a vida útil pretendida do sistema: projetar um
reservatório de vinte anos contra a janela distante avalia um período em que ele já terá
sido substituído.

A escolha do **modelo climático** é a decisão mais delicada das três, e a ela se dedica
uma subseção própria adiante.

---

## Como conduzir o estudo

O procedimento correto consiste em executar o mesmo projeto em cada combinação de
interesse e comparar os resultados entre si, em vez de dimensionar diretamente sobre a
série projetada. Quatro passos o resumem.

1. Feche o dimensionamento com a série **histórica**. É a referência.
2. Mantenha todos os demais parâmetros e troque só a série.
3. Rode para cada cenário e janela.
4. Compare **potencial de economia** e **dias de atendimento pleno**. O segundo
   costuma se degradar mais que o primeiro, porque o que muda primeiro é a
   distribuição, não o total.

> **O que não fazer.** Dimensionar direto na série futura e apresentar o resultado
> como projeto. A série futura é uma projeção com incerteza grande; ela serve para
> testar a **robustez** de um dimensionamento feito no histórico, não para substituí-lo.

---

## A escolha do modelo, e por que ela importa tanto

Dezenove modelos climáticos projetam dezenove futuros distintos para a mesma cidade sob
o mesmo cenário de emissões, e essa dispersão não é ruído a ser eliminado: ela é a
expressão honesta da incerteza física do problema. ==Nas janelas próxima e média, a
dispersão entre modelos costuma superar a diferença entre cenários de emissão,== o que
significa que a escolha do modelo pesa mais sobre o resultado do que a escolha do futuro
socioeconômico.

Três condutas são defensáveis diante dessa dispersão, apresentadas aqui em ordem
decrescente de rigor.

**Ensemble.** Rode todos os modelos disponíveis e reporte a faixa de resultados, com
mediana. É o mais rigoroso e o mais caro em tempo de máquina. A seção {{n:19}} mostra como
fazer em lote.

**Subconjunto justificado.** Escolha três a cinco modelos com bom desempenho
documentado para a América do Sul, e declare o critério de escolha e a fonte.

**Modelo único, declarado como tal.** Aceitável para uma análise exploratória, desde
que o texto não apresente o resultado como projeção robusta.

> **O que jamais fazer:** rodar vários modelos, escolher o que dá o resultado mais
> conveniente, e reportar só ele.

---

## O que declarar

Um estudo com cenário climático precisa trazer, no método:

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual;
- a **procedência da base**, com versão.

Sem isso, o resultado não é reproduzível. A seção {{n:E}} traz a procedência da base do
programa.

---

## Uma ressalva de método

Projeções climáticas carregam duas incertezas empilhadas, de naturezas distintas: a do
cenário, que é socioeconômica e diz respeito a escolhas humanas futuras, e a do modelo,
que é física e diz respeito à representação do sistema climático. Nenhuma das duas se
reduz executando mais simulações com o mesmo material, porque não se trata de incerteza
amostral.

Um estudo conduzido com honestidade apresenta o resultado como faixa, e não como número
único, e evita conclusões que dependam da terceira casa decimal de uma projeção para
2060.
