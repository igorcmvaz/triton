# 15. Usar cenário climático futuro

> **Pergunta que este guia responde:** o sistema que dimensiono hoje ainda serve em
> 2060?

Um reservatório dura trinta anos ou mais. A chuva de 2060 não será a de hoje. O
Netuno traz uma base de projeções climáticas para que o dimensionamento possa
considerar isso.

---

## 15.1. O que a base tem

| | |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 3 |
| janelas temporais | 3 |

O CMIP6 é a sexta fase do *Coupled Model Intercomparison Project*, o exercício
coordenado internacionalmente que alimenta os relatórios do IPCC. Cada modelo é um
modelo climático global de um centro de pesquisa diferente.

> **A base é distribuída à parte do programa**, porque ocupa cerca de 6,5 GB em
> trinta e sete mil arquivos. Sem ela instalada, a aba de Projeto oferece apenas o
> carregamento de arquivo próprio, e as abas dependentes avisam. O capítulo 2 explica
> como obtê-la.

---

## 15.2. Escolher modelo, cenário e janela

**O cenário** é a trajetória de emissões. Os três seguem as *Shared Socioeconomic
Pathways*:

| Cenário | Trajetória |
| :--- | :--- |
| SSP1-2.6 | emissões caem rápido; aquecimento contido perto de 2 °C |
| SSP2-4.5 | trajetória intermediária, próxima das políticas atuais |
| SSP5-8.5 | emissões altas, sem mitigação efetiva |

**A janela** é o período de trinta anos projetado: próximo, médio e distante.

**O modelo** é a parte difícil, e o item 15.4 trata dela.

---

## 15.3. Como conduzir o estudo

Rode **o mesmo projeto** em cada combinação que interessar, e compare. O
procedimento:

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

## 15.4. A escolha do modelo, e por que ela importa tanto

Dezenove modelos projetam dezenove futuros diferentes para a mesma cidade e o mesmo
cenário. A dispersão entre modelos costuma ser **maior** que a diferença entre
cenários de emissão nas janelas próxima e média.

Três condutas defensáveis, em ordem de rigor:

**Ensemble.** Rode todos os modelos disponíveis e reporte a faixa de resultados, com
mediana. É o mais rigoroso e o mais caro em tempo de máquina. O guia 19 mostra como
fazer em lote.

**Subconjunto justificado.** Escolha três a cinco modelos com bom desempenho
documentado para a América do Sul, e declare o critério de escolha e a fonte.

**Modelo único, declarado como tal.** Aceitável para uma análise exploratória, desde
que o texto não apresente o resultado como projeção robusta.

> **O que jamais fazer:** rodar vários modelos, escolher o que dá o resultado mais
> conveniente, e reportar só ele.

---

## 15.5. O que declarar

Um estudo com cenário climático precisa trazer, no método:

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual;
- a **procedência da base**, com versão.

Sem isso, o resultado não é reproduzível. O apêndice E traz a procedência da base do
programa.

---

## 15.6. Uma ressalva de método

Projeções climáticas trazem duas incertezas empilhadas: a do cenário, que é
socioeconômica, e a do modelo, que é física. Nenhuma das duas é reduzida rodando
mais simulações.

Um estudo honesto apresenta o resultado como **faixa**, não como número, e evita
conclusões que dependam da terceira casa decimal de uma projeção para 2060.
