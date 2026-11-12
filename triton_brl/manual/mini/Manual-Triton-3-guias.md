# Triton

## Manual do Usuário — Guias de uso

Igor Catão Martins Vaz e Enedir Ghisi

Grupo de Pesquisa em Ambientes Sustentáveis
Universidade Federal de Santa Catarina

Florianópolis, 2026

---

### Sobre este volume

Este é um dos oito volumes em que o manual do Triton pode ser distribuído, e
reúne o capítulo 3 (Guias disponíveis no programa) e os apêndices D, F e G do manual completo. Serve para mandar
só a parte que interessa: o método a um revisor, o tutorial a uma turma, os guias
a quem já usa o programa.

A numeração das seções e das equações é a mesma do manual completo, de modo que
uma remissão vale nos dois. Quando o texto remete a uma seção que está em outro
volume, o nome do volume vem entre parênteses.

| Volume | Conteúdo |
| :--- | :--- |
| Comece aqui | o capítulo 1 (Comece aqui) e o apêndice G |
| O método | o capítulo 2 (O método) e os apêndices A, B, C, E, G e H |
| **Guias de uso** | o capítulo 3 (Guias disponíveis no programa) e os apêndices D, F e G |
| Tutorial | o capítulo 4 (Tutorial: um exemplo do começo ao fim) e os apêndices G, I e J |
| Enganos, limitações e confiabilidade | o capítulo 5 (Enganos, limitações e confiabilidade) e os apêndices G e H |
| Correções, bugs e versionamento | o capítulo 6 (Correções, bugs e versionamento) |
| Modulação probabilística | o capítulo 7 (Modulação probabilística) e os apêndices G e H |
| Apêndices | os apêndices |

### Como citar

> VAZ, Igor Catão Martins; GHISI, Enedir. **Triton: manual do usuário**.
> Guias de uso. Versão 0.2.0. Florianópolis: Universidade Federal de Santa
> Catarina, 2026.

---

## Sumário

**3 Guias disponíveis no programa**

3.1 Comparar cidades

3.2 Usar cenário climático futuro

3.3 Ajustar a tarifa do seu município

3.4 Modular a demanda por calendário

3.5 Simular escola, hospital e comércio

3.6 Comparar muitos casos de uma vez

3.7 Análise de sensibilidade

3.8 Importar um projeto do Netuno 4

3.9 Exportar para CAD, BIM e planilha


**Apêndices**

Apêndice D — Regimes tarifários

Apêndice F — Arquivos, pastas e formatos

Apêndice G — Glossário



## Lista de figuras

Figura 1 — (a) Precipitação média anual e (b) potencial de economia de água potável do projeto do tutorial, com 150 m² de captação, 600 L/dia de demanda, fração atendível de 28% e cisterna de 4.000 L, em quatro capitais

Figura 2 — Precipitação média mensal em (a) Florianópolis, (b) São Paulo, (c) Brasília e (d) Manaus, na mesma escala; a linha tracejada é a média mensal de cada série

Figura 3 — A forma das duas trajetórias de emissão disponíveis na base

Figura 4 — Parcela de água da fatura mensal em função do consumo, em três regimes de valor mínimo

Figura 5 — Os quatro modos de modulação, o que cada um pede ao usuário e a situação em que cada um se justifica

Figura 6 — Os três perfis de demanda usados na comparação, expressos como a razão entre a demanda do mês e a demanda média

Figura 7 — (a) Perfis mensais de demanda da escola e do hotel de praia sobre a precipitação média mensal de Florianópolis; (b) potencial de economia de cada perfil com o mesmo reservatório de 4.000 L. O perfil de hotel concentra em dois meses quase um terço do consumo anual, e é essa concentração, e não a fase, que lhe custa quase um ponto e meio percentual

Figura 8 — As oito tipologias disponíveis, agrupadas pela categoria tarifária que a concessionária cobra

Figura 9 — Faixa de variação plausível de cada premissa numa análise de sensibilidade, com a origem da incerteza

Figura 10 — A variação do valor presente líquido quando cada premissa é alterada em 30% para mais e para menos, mantidas as demais

Figura 11 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião

---

## Lista de tabelas

Tabela 1 — O mesmo projeto do tutorial simulado em quatro capitais brasileiras

Tabela 2 — Razão entre o mês mais chuvoso e o menos chuvoso nas quatro capitais

Tabela 3 — Conteúdo da base climática nacional distribuída com o programa

Tabela 4 — Os seis códigos de faixa tarifária e o efeito de cada um na fatura

Tabela 5 — Os seis regimes tarifários e o que acontece ao economizar em cada um

Tabela 6 — Efeito da economia de água na fatura em dois regimes tarifários opostos

Tabela 7 — Expoente n da Tabela de Exponenciais da CORSAN, categoria residencial

Tabela 8 — Fatura mensal em Alegrete (RS) pela fórmula exponencial, vigência 01/07/2026

Tabela 9 — As três formas de comparar alternativas conforme o que varia entre elas

Tabela 10 — Subcomandos da linha de comando e finalidade de cada um

Tabela 11 — Potencial, valor presente líquido e retorno do projeto fechado do tutorial com cada premissa variada sozinha, do valor baixo ao alto

Tabela 12 — Leitura da aceitabilidade SMAA-VIKOR do volume vencedor

Tabela 13 — Dados do Netuno 4 recuperados pela importação

Tabela 14 — Formatos de exportação e finalidade de cada um

Tabela 15 — Opções da exportação de planilha e quando usar cada uma

Tabela 16 — Distribuição dos municípios do catálogo pelos seis regimes tarifários

Tabela 17 — Grau de confiança dos registros tarifários do catálogo

Tabela 18 — Cobertura do catálogo tarifário: municípios por categoria e situação do dado

Tabela 19 — As estruturas tarifárias do catálogo, numeradas para as tabelas de preço por faixa que vêm a seguir

Tabela 20 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 1 de 6: 0–4 a 15–20 m³)

Tabela 21 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 2 de 6: 20–24 a 55–60 m³)

Tabela 22 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 3 de 6: 60–64 a 100–104 m³)

Tabela 23 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 4 de 6: 104–120 a 400–500 m³)

Tabela 24 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 5 de 6: 500–600 a 15.000–20.000 m³)

Tabela 25 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 6 de 6: 20.000–30.000 a 120.000 m³)

Tabela 26 — Categorias tarifárias ainda não coletadas, por prestador

Tabela 27 — Vigência e última verificação da fonte de cada estrutura tarifária, com a situação do dado

Tabela 28 — A fórmula exponencial da CORSAN em cada tabela tarifária e categoria coletada

Tabela 29 — As estruturas de cobrança direta e de parcela fixa por faixa

Tabela 30 — Formatos que o programa lê e onde cada um é carregado

Tabela 31 — Formatos que o programa escreve e onde cada um é gerado

Tabela 32 — As sete seções do arquivo de projeto e o que cada uma guarda

Tabela 33 — Localização dos arquivos do programa e dos arquivos do usuário

Tabela 34 — Seções do arquivo estudo.json (esquema triton-estudo, versão 1)

Tabela 35 — Apelidos das substituições e o campo do projeto que cada um altera

Tabela 36 — Arquivos que triton estudo run grava na pasta de saída

Tabela 37 — Compatibilidade entre versões do arquivo de projeto

Tabela 38 — Padronização terminológica de água de chuva e água pluvial

Tabela 39 — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial

---


---
# 3. Guias disponíveis no programa

---

## 3.1. Comparar cidades

> **Pergunta que este guia responde:** o mesmo projeto renderia o mesmo em outra cidade?

Não renderia, e a diferença não segue a direção que a intuição sugere. A expectativa
corrente é a de que mais chuva implique mais aproveitamento, e essa expectativa está
errada com frequência suficiente para merecer uma seção inteira.

> **Só na Edição Brasil (BRL).** As cidades brasileiras deste guia vêm da base climática
> nacional da Edição Brasil. Na International Edition, a mesma comparação se faz com
> arquivos de chuva próprios, um por cidade; todo o resto do guia vale como está escrito.

---

### 3.1.1. Como fazer a comparação

O procedimento é simples e consiste em manter todos os parâmetros do projeto e trocar
apenas a série de precipitação. Na etapa **1. Projeto e Chuva**, escolha outra cidade da
base climática nacional ou carregue um arquivo próprio, e execute novamente a simulação.
Para comparar várias cidades sem refazer o projeto a cada uma, salve um arquivo por
cidade, conforme a seção 3.6 recomenda.

---

### 3.1.2. O resultado

O projeto do tutorial — 150 m² de captação, 600 L/dia de demanda, 28% de fração
atendível e cisterna de 4.000 L — levado a quatro capitais brasileiras produz a tabela
abaixo.

<!-- tabela: **Tabela 1** — O mesmo projeto do tutorial simulado em quatro capitais brasileiras -->
| Cidade | Chuva anual | Dias com chuva | Razão entre o mês mais e o menos chuvoso | Potencial com 4.000 L | Volume ideal |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Florianópolis | 1 795 mm | 46% | 3,2× | 27,12% | 4 000 L |
| São Paulo | 1 624 mm | 42% | 4,0× | 25,74% | 5 000 L |
| Brasília | 1 376 mm | 35% | 1 191,7× | 15,45% | 4 000 L |
| Manaus | 2 155 mm | 51% | 17,3× | 20,96% | 5 000 L |

A Figura 1 separa as duas grandezas, cada uma na sua escala.

![Chuva anual e potencial de economia nas quatro capitais](../figuras/fig03_cidades.png)

*Figura 1 — (a) Precipitação média anual e (b) potencial de economia de água potável do projeto do tutorial, com 150 m² de captação, 600 L/dia de demanda, fração atendível de 28% e cisterna de 4.000 L, em quatro capitais. Manaus tem a maior precipitação anual e não tem o maior potencial de economia.*

---

### 3.1.3. O regime manda mais que a lâmina

Lidas lado a lado, as colunas de chuva anual e de potencial de economia não andam
juntas, e os dois casos extremos da tabela mostram por quê. Manaus recebe 20% mais chuva
que Florianópolis — 2.155 mm anuais contra 1.795 mm — e ainda assim rende 23% menos:
20,96% contra 27,12% de potencial. Brasília, no extremo oposto, recebe 23% menos chuva
que Florianópolis e rende pouco mais da metade, com 15,45%.

A explicação está na razão entre o mês mais chuvoso e o mês menos chuvoso de cada
cidade, que mede o quanto a chuva se concentra ao longo do ano.

<!-- tabela: **Tabela 2** — Razão entre o mês mais chuvoso e o menos chuvoso nas quatro capitais -->
| Cidade | Razão | O que significa |
| :--- | ---: | :--- |
| Florianópolis | 3,2× | chove o ano inteiro, com estação mais úmida |
| São Paulo | 4,0× | idem, um pouco mais marcado |
| Manaus | 17,3× | seca amazônica curta mas real |
| Brasília | 1.192× | **o mês mais seco é seco de verdade** |

Em Brasília, os meses de junho, julho e agosto praticamente não registram chuva. Um
reservatório dimensionado para atravessar noventa dias de estiagem precisaria armazenar
noventa dias de demanda pluvial, o que neste projeto corresponderia a 15.120 litros —
volume que nenhuma cisterna residencial comporta. A consequência é que o sistema
permanece ocioso durante um trimestre inteiro por ano, e o potencial anual reflete essa
ociosidade.

> **A conclusão prática.** ==O aproveitamento pluvial rende mais onde a chuva é
> frequente do que onde ela é abundante.== Cidades de clima subtropical úmido com chuva
> bem distribuída constituem o melhor caso brasileiro; cidades de clima tropical com
> estação seca marcada constituem o pior, por mais intensa que seja a chuva da estação
> úmida.

---

A Figura 2 apresenta o regime mensal das quatro capitais na mesma escala.

![O regime mensal das quatro capitais](../figuras/fig18_capitais.png)

*Figura 2 — Precipitação média mensal em (a) Florianópolis, (b) São Paulo, (c) Brasília e (d) Manaus, na mesma escala; a linha tracejada é a média mensal de cada série. Florianópolis e São Paulo distribuem a chuva ao longo de todo o ano; Manaus tem estação seca curta, de julho a outubro; e Brasília praticamente não recebe chuva de maio a setembro. É essa distribuição, e não o total anual, que decide o desempenho do reservatório.*

---

### 3.1.4. O que a literatura já tinha encontrado

O resultado das quatro capitais não é peculiaridade deste tutorial. Ghisi e Souza (2012)
simularam casas em treze cidades de países diferentes, com o próprio Triton, e chegaram à
mesma conclusão por outro caminho: o maior potencial de economia aparece onde a chuva é
constante, o que nem sempre coincide com a maior lâmina anual, e as cidades com
estiagem bem definida exigem reservatórios maiores para o mesmo desempenho.

No Brasil, dois levantamentos mostram a amplitude da variação dentro de um só estado ou
de uma só cidade. Ghisi, Lopes e Rupp (2016) fizeram 2.700 simulações para casas em 60
cidades de Santa Catarina, com séries diárias longas, e obtiveram reservatórios ideais de
1.000 a 16.000 L e economias médias de 75 a 461 litros por dia por casa. Ghisi e Custódio
(2019), com 33.720 cenários para o setor residencial de Joinville, encontraram potencial
médio de 18,5% com água de chuva só nas bacias sanitárias, e de 40,8% quando a máquina de
lavar roupa também a recebe — a mesma escolha de uso que a seção 4.2 (volume Tutorial) discute.

A lição para quem compara cidades é a mesma dos dois estudos: a série local decide, e um
volume ou um potencial trazido de outra cidade, mesmo vizinha, não substitui a simulação.

#### 3.1.4.1. Muitas cidades de uma vez

Para comparar mais de três ou quatro cidades, trocar a série à mão deixa de ser prático.
A base climática nacional traz séries para 652 municípios, e a planilha de cenários da
seção 3.6 roda o mesmo projeto contra várias delas numa única execução, gravando um
resultado por linha. Mantenha na planilha os mesmos parâmetros de edificação e de
reservatório em todas as linhas, e varie só a cidade: é o que isola o efeito do clima.

---

### 3.1.5. O que mais muda entre cidades

A precipitação não é a única grandeza que varia entre municípios, e as outras duas podem
inverter a conclusão econômica de um estudo comparativo.

A primeira é a **tarifa**. O preço do metro cúbico varia consideravelmente pelo país, e o
regime de mínimo varia ainda mais. Um potencial de 15% em município de tarifa elevada e
regime de disponibilidade pode render mais dinheiro que um potencial de 27% em município
que pratique franquia sobre o consumo mínimo, e a seção 3.3 trata dessa mecânica em
detalhe.

A segunda é o **fator de emissão da rede elétrica**, que altera simultaneamente a
emissão evitada por metro cúbico de água substituída e o custo ambiental do bombeamento.
A Edição Brasil traz o fator discriminado por região; na International Edition, ele é
informado em cada projeto.

> **Ao comparar cidades num estudo, deixe claro o que variou.** Comparar apenas a
> precipitação, mantendo tarifa e fator de emissão fixos, isola o efeito climático e
> constitui comparação legítima, desde que declarada como tal. Variar todas as grandezas
> simultaneamente produz um número que não se consegue explicar, porque nele se somam
> efeitos de sinais possivelmente opostos.

---

### 3.1.6. O volume ideal também muda, mas pouco

A última coluna da tabela reserva uma surpresa: o volume ideal varia de 4.000 a 5.000 L
entre as quatro capitais, uma amplitude modesta diante da diferença de regime que as
separa.

A explicação está na natureza do critério. O volume ideal pelo ganho marginal localiza o
joelho da curva de aproveitamento, e a posição desse joelho é governada pelo **tamanho
típico dos eventos de chuva**, que é razoavelmente parecido entre as quatro cidades. O
que varia fortemente é o **patamar** que a curva atinge depois do joelho, e não o ponto
em que ela dobra.

Dito de outro modo: em Brasília acerta-se o mesmo volume que em Florianópolis e colhe-se
consideravelmente menos água com ele.

---

## 3.2. Usar cenário climático futuro

> **Pergunta que este guia responde:** o sistema que dimensiono hoje ainda serve em
> 2060?

> **Só na Edição Brasil (BRL).** A base de projeções climáticas descrita aqui só acompanha a
> Edição Brasil. Na International Edition, o método deste guia vale como está para séries
> projetadas próprias — por exemplo, séries com correção de viés de um serviço climático
> nacional —, carregadas como arquivos de chuva.

Um reservatório de água pluvial dura trinta anos ou mais, e a chuva que cairá sobre a
edificação ao longo desse período não será a mesma que caiu no passado recente. Dimensionar
um sistema de vida longa exclusivamente sobre a série histórica supõe, implicitamente, um
clima estacionário — suposição que as projeções disponíveis não sustentam. O Triton traz
uma base de projeções climáticas justamente para que o dimensionamento possa incorporar
essa questão de forma explícita.

---

### 3.2.1. O que a base tem

<!-- tabela: **Tabela 3** — Conteúdo da base climática nacional distribuída com o programa -->
| O que a base traz | Quantidade |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 2, SSP2-4.5 e SSP5-8.5 |
| simulação histórica | 1980 a 2013 |
| simulação futura | 2015 a 2100 |

O CMIP6 é a sexta fase do *Coupled Model Intercomparison Project*, o exercício
coordenado internacionalmente que alimenta os relatórios do IPCC. Cada modelo é um
modelo climático global de um centro de pesquisa diferente.

### 3.2.2. De onde vêm as séries

![Logotipo do conjunto de dados CLIMBra](../figuras/CLIMBra.jpg)

*Figura — Logotipo oficial do CLIMbra (Climate Change Dataset for Brazil), desenvolvido para estudos hidroclimáticos e impactos das mudanças climáticas no Brasil.*

A base do programa é extraída do **CLIMBra** (*Climate Change Dataset for Brazil*), conjunto de dados de referência publicado por Ballarin et al. (2023) na revista [*Scientific Data* (Nature)](https://www.nature.com/articles/s41597-023-01956-z) ([doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)), com dados públicos disponibilizados no [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316) ([doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)) sob licença aberta CC0. Três características definem o que as séries representam, e convém conhecê-las antes de usá-las:

**São projeções corrigidas de viés.** Modelos globais têm resolução de dezenas a
centenas de quilômetros e reproduzem mal a chuva local: costumam errar a frequência de
dias chuvosos, a intensidade e os extremos. O CLIMBra corrigiu as séries diárias dos 19
modelos pelo método *Quantile Delta Mapping* (QDM), que ajusta a distribuição simulada à
observada e, ao mesmo tempo, preserva as variações relativas dos quantis entre o período
histórico e o futuro. A referência observada foi a grade diária de Xavier, King e
Scanlon (2016), construída com milhares de pluviômetros e estações do Brasil, com
resolução de 0,25°, isto é, cerca de 28 km.

**São células de grade, e não estações.** A série de uma cidade é a da célula de 0,25°
que a contém. Ela representa a chuva média de uma área da ordem de 700 km², e não a de
um pluviômetro. Em relevo acidentado ou no litoral, a diferença entre a chuva da célula e
a do lote pode ser grande.

**O histórico da base é simulado.** A série de 1980 a 2013 não é a chuva observada, e sim
a simulação de cada modelo para aquele período, corrigida para ter a mesma **estatística**
da observação. A cronologia não coincide: um dia chuvoso na série do modelo não
corresponde a um dia chuvoso real. Por isso, a comparação correta de um cenário futuro é
com o **histórico do mesmo modelo**, e não com a série observada que acompanha o
programa. Misturar as duas atribuiria ao clima futuro a diferença entre observação e
modelo.

Maraun (2016), numa revisão crítica sobre correção de viés, alerta para o limite do
procedimento: ele pressupõe que o modelo representa de forma plausível os processos e a
mudança do clima, e não consegue corrigir uma tendência implausível. A correção melhora a
estatística; não transforma um modelo ruim num modelo bom.

> **Base compactada e embarcada no programa:** os 37.164 arquivos de texto do CLIMBra
> (que originalmente ocupam cerca de 6,5 GB em formato CSV descompactado) foram consolidados
> e comprimidos pelo Triton em bancos de dados SQLite binários de alta performance, um por
> modelo (`climbra_<modelo>.db`). Esses bancos ficam integrados ao executável e ao instalador, permitindo consultas
> instantâneas (< 1 ms por série) e execução imediata para qualquer uma das 652 cidades
> sem a necessidade de downloads externos volumosos. Os CSV originais não são distribuídos
> nem precisam ser instalados.

---

### 3.2.3. Escolher modelo, cenário e janela

O **cenário** representa a trajetória futura de emissões de gases de efeito estufa, e os
dois disponíveis seguem as *Shared Socioeconomic Pathways* adotadas pelo IPCC. Eles não
são previsões, e sim hipóteses coerentes sobre o comportamento socioeconômico global ao
longo do século (Figura 3). O nome combina a trajetória socioeconômica, de 1
a 5, com o forçamento radiativo aproximado em 2100, em watts por metro quadrado: o
SSP2-4.5 é o caminho intermediário, com forçamento de 4,5 W/m², e o SSP5-8.5 é o de
desenvolvimento intensivo em combustíveis fósseis, com 8,5 W/m². Os cenários de mitigação
forte, como o SSP1-2.6, não fazem parte do CLIMBra.

![As duas trajetórias de emissão disponíveis na base](../figuras/fig44_cenarios.png)

*Figura 3 — A forma das duas trajetórias de emissão disponíveis na base. O SSP2-4.5 é a trajetória intermediária, com emissões que se estabilizam e depois caem; o SSP5-8.5 supõe emissões altas e crescentes, sem mitigação efetiva. A figura mostra o formato de cada uma, e não valores projetados.*

A **janela temporal** é o recorte da série futura, de 2015 a 2100, sobre o qual o estudo
é feito. O programa permite recortar qualquer período, nas datas inicial e final da
etapa **1. Projeto e Chuva**. A convenção mais usada é tomar janelas de trinta anos, a
mesma duração das normais climatológicas, e o campo **Atalho de recorte** preenche as
datas com três delas: 2021–2050, 2041–2070 e 2071–2100, além da série completa. O atalho
só preenche as datas, que continuam editáveis, e a etapa avisa quando o recorte tem menos
de dez anos. A escolha da janela deve guardar relação com a vida útil
pretendida do sistema: avaliar um reservatório de vinte anos, instalado agora, contra o
fim do século avalia um período em que ele já terá sido substituído.

A escolha do **modelo climático** é a decisão mais delicada das três, e a ela se dedica
uma subseção própria adiante.

---

### 3.2.4. Como conduzir o estudo

O procedimento correto consiste em executar o mesmo projeto em cada combinação de
interesse e comparar os resultados entre si, em vez de dimensionar diretamente sobre a
série projetada. Quatro passos o resumem.

1. Feche o dimensionamento com a série **histórica**. É a referência.
2. Rode o mesmo projeto na série **histórica simulada** de cada modelo que for usar, de
   1980 a 2013. É contra ela, e não contra a observada, que o futuro se compara.
3. Mantenha todos os demais parâmetros e troque só a série, para cada cenário e janela.
4. Compare **potencial de economia** e **dias de atendimento pleno**, sempre como
   diferença entre o futuro e o histórico do mesmo modelo. O segundo costuma se degradar
   mais que o primeiro, porque o que muda primeiro é a distribuição, não o total.

> **Um exemplo de leitura.** Suponha que, com um modelo, o potencial seja de 36% no
> histórico simulado e de 33% no SSP5-8.5 de 2041 a 2070, e que a série observada dê 37%.
> A mudança atribuível ao clima é de três pontos, e não de quatro: o ponto restante é a
> diferença entre o modelo e a observação, que existe também no passado.

> **O que não fazer.** Dimensionar direto na série futura e apresentar o resultado
> como projeto. A série futura é uma projeção com incerteza grande; ela serve para
> testar a **robustez** de um dimensionamento feito no histórico, não para substituí-lo.

---

### 3.2.5. A escolha do modelo, e por que ela importa tanto

Dezenove modelos climáticos projetam dezenove futuros distintos para a mesma cidade sob
o mesmo cenário de emissões, e essa dispersão não é ruído a ser eliminado: ela é a
expressão honesta da incerteza física do problema. ==Para a chuva, a dispersão entre
modelos costuma superar a diferença entre cenários de emissão,== o que significa que a
escolha do modelo pesa mais sobre o resultado do que a escolha do futuro socioeconômico.

Hawkins e Sutton (2011) decompuseram a incerteza das projeções de precipitação para
regiões da ordem de 2.500 km, com os modelos da fase anterior do exercício, o CMIP3, em
três fontes: a variabilidade interna do clima, a diferença entre modelos e a diferença
entre cenários. Para a precipitação, ao contrário da temperatura, a variabilidade interna
responde por 50% a 90% da incerteza na primeira década e continua dominante, em muitas
regiões, até a terceira; a incerteza entre modelos passa a dominar nos horizontes mais
longos; e a incerteza de cenário é pequena ou desprezível em todas as regiões e
horizontes, salvo perto dos polos no fim do século. Os autores mostram ainda que a razão
entre o sinal da mudança e o ruído é menor que um em quase todo o planeta, e concluem que
as decisões de adaptação terão de ser tomadas com incerteza alta sobre a chuva regional. A
consequência para o projeto é direta: rodar os dois cenários com um só modelo informa
menos do que rodar um cenário com vários modelos.

Três condutas são defensáveis diante dessa dispersão, apresentadas aqui em ordem
decrescente de rigor.

**Ensemble.** Rode todos os modelos disponíveis e reporte a faixa de resultados, com
mediana. É o mais rigoroso e o mais caro em tempo de máquina. A seção 3.6 mostra como
fazer em lote.

**Subconjunto justificado.** Escolha três a cinco modelos com bom desempenho
documentado para a América do Sul, e declare o critério de escolha e a fonte.

**Modelo único, declarado como tal.** Aceitável para uma análise exploratória, desde
que o texto não apresente o resultado como projeção robusta.

> **O que jamais fazer:** rodar vários modelos, escolher o que dá o resultado mais
> conveniente, e reportar só ele.

---

### 3.2.6. O que a literatura mostra sobre o reservatório no clima futuro

Os estudos que simulam sistemas de aproveitamento pluvial sob projeções climáticas
convergem num ponto: a mudança no total anual de chuva importa menos que a mudança na
**distribuição**. Kisakye et al. (2018), com seis modelos para um distrito de Uganda,
encontraram projeções conflitantes entre modelos, mas concordância quanto à estação: a
economia e a segurança hídrica cairiam nas estações que já eram secas e subiriam nas
chuvosas, com redução de mais de 50% numa das estações no fim do século. Lash et al.
(2014), ao dimensionar um reservatório para um edifício universitário no Reino Unido com
3.000 séries de chuva equiprováveis das projeções climáticas britânicas, concluíram que,
para ser provável atender em 2080 a mesma demanda de hoje, o reservatório precisaria ser
112% maior, e 225% maior para que isso fosse muito provável.

Os dois estudos ilustram o que a seção 3.1 mostrou para cidades brasileiras de hoje:
cidades com estação seca marcada exigem reservatórios muito maiores para o mesmo
desempenho. Um clima futuro com estiagens mais longas se comporta, para o reservatório,
como uma mudança de cidade.

---

### 3.2.7. O que declarar

Um estudo com cenário climático precisa trazer, no método:

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual; na base do programa, a do CLIMBra,
  por *Quantile Delta Mapping* contra a grade de Xavier et al. (2016);
- a **procedência da base**, com versão: Ballarin et al. (2023);
- que o futuro foi comparado com o **histórico simulado do mesmo modelo**.

Sem isso, o resultado não é reproduzível. O apêndice E (volume Apêndices) traz a procedência da base do
programa.

---

### 3.2.8. Uma ressalva de método

Projeções climáticas carregam duas incertezas empilhadas, de naturezas distintas: a do
cenário, que é socioeconômica e diz respeito a escolhas humanas futuras, e a do modelo,
que é física e diz respeito à representação do sistema climático. Nenhuma das duas se
reduz executando mais simulações com o mesmo material, porque não se trata de incerteza
amostral.

Um estudo conduzido com honestidade apresenta o resultado como faixa, e não como número
único, e evita conclusões que dependam da terceira casa decimal de uma projeção para
2060.

---

## 3.3. Ajustar a tarifa do seu município

> **Pergunta que este guia responde:** a tarifa do meu município está na base, e está
> certa?

> **Só na Edição Brasil (BRL).** O catálogo de 652 municípios e a etapa
> **12. Gestor de Tarifas** só acompanham a Edição Brasil. Na International Edition, a tarifa é digitada, na
> etapa econômica, com a mesma tabela de faixas, os mesmos códigos e os mesmos seis regimes
> descritos aqui — por isso este guia é também a referência para lançar qualquer estrutura
> tarifária.

Este é o guia que mais altera resultados. A estrutura tarifária decide a viabilidade
econômica de um sistema pluvial mais do que qualquer parâmetro de projeto, e é também o
dado que mais frequentemente aparece errado nos estudos publicados sobre o tema.

---

### 3.3.1. Como é composta a fatura de água e esgoto no Brasil

Antes de conferir a tarifa do município, convém entender o que se está conferindo. A
fatura de água no Brasil não é o produto do consumo por um preço único, e cinco
características a distinguem da fatura de energia elétrica, que é a referência mais familiar para
a maioria dos leitores.

**A prestação é local, e o preço também.** Cada município é atendido por uma companhia
estadual, por uma autarquia municipal ou por uma concessionária privada, e cada prestador
tem tabela própria, homologada por uma agência reguladora — estadual, municipal ou
intermunicipal. Não existe tarifa nacional de água, e a diferença entre dois municípios
vizinhos pode ultrapassar o dobro.

**A tarifa é progressiva por faixas de consumo.** O metro cúbico não custa o mesmo em
qualquer quantidade: o consumo é dividido em faixas, e cada faixa tem preço próprio,
crescente. Na tabela da CASAN vigente em Florianópolis, os primeiros dez metros cúbicos
custam R$ 3,08 cada e os quinze seguintes custam R$ 14,31 cada. ==A progressividade é o
que torna a economia de água mais valiosa do que parece:== o metro cúbico que se deixa de
consumir é sempre o da faixa mais alta da fatura, que é o mais caro.

**Existe uma parcela que independe do consumo.** Quase toda concessionária cobra algo
mesmo de quem não consome nada, e o nome e a natureza dessa parcela variam de um lugar
para outro. É o assunto da subseção sobre os seis regimes, adiante, e é o ponto que mais
decide se um sistema pluvial se paga.

**O esgoto é cobrado como percentual da água.** A maior parte dos prestadores fatura o
esgoto aplicando um percentual sobre a parcela de água, comumente de 80% ou 100%, sob o
argumento de que o volume esgotado é proporcional ao consumido. Quando esse percentual é
de 100%, a parcela de esgoto iguala a de água, e o esgoto responde por metade da fatura —
o que significa que cada metro cúbico economizado vale o dobro do preço da água.

**Há categorias distintas de consumidor.** Toda concessionária publica tabelas separadas
para as categorias residencial, comercial, industrial e pública, com preços que
frequentemente são o dobro ou mais da residencial. Na tabela da CASAN, a primeira faixa
custa R$ 3,08/m³ no residencial e R$ 6,81/m³ no comercial.

> **O que o programa traz, e o que você precisa lançar.** O catálogo de 652 municípios do
> programa registra a **categoria residencial** de cada um deles, e o diálogo de tarifas
> diz de onde ela veio: o documento oficial guardado, a tabela usada e a vigência, ou o
> aviso de que o valor ainda não tem documento. As categorias comercial, pública e
> industrial entram município a município, transcritas da tabela oficial do prestador, e
> só aparecem para escolha onde foram coletadas — em cerca de 390 municípios em outubro de
> 2026; nunca são estimadas a partir da residencial. As demais categorias
> existem, são públicas e estão nas resoluções das agências reguladoras — o que não há é
> um catálogo nacional delas, que seria um levantamento de porte próprio. Para estudar
> uma escola, um comércio ou uma indústria, lance a estrutura da categoria correta no
> modo personalizado desta mesma tela: o programa aceita qualquer tabela de faixas, com
> qualquer regime de mínimo, e a seção 3.5 mostra o procedimento.

---

### 3.3.2. Comece conferindo o que já está na base

O programa acompanha um catálogo de 652 municípios brasileiros, e cada registro traz a
estrutura tarifária completa, o percentual de esgoto praticado, o regime de mínimo
adotado, a data de vigência da tabela e a fonte documental de onde o dado foi extraído.
O catálogo cobre a categoria residencial, conforme a subseção anterior esclarece.

Na etapa **12. Gestor de Tarifas**, escolha o estado e o município. Além da estrutura, o
programa exibe o **grau de confiança** atribuído ao registro, que sintetiza a qualidade da
fonte e a data do levantamento. Três itens merecem conferência contra a resolução vigente
da sua concessionária, e a ordem importa porque o primeiro invalida os demais.

1. **a data de vigência** — tarifas são reajustadas anualmente;
2. **os valores das faixas**;
3. **o regime de mínimo**, que é o item 3.3.4.

Havendo divergência em qualquer dos três, edite o registro. A edição vale para o seu
projeto, não altera o catálogo dos demais usuários, e fica gravada dentro do arquivo
`.triton` — o que significa que quem receber o seu projeto reproduzirá a mesma conta, com
a mesma tabela.

---

### 3.3.3. Como a tabela é montada

Cada linha da estrutura tarifária é representada no programa por uma quádrupla de
valores: o volume mínimo da faixa, o volume máximo, um valor monetário e um código. O
código é o elemento decisivo, porque é ele que informa o que aquele valor significa — e
estruturas visualmente parecidas cobram de maneiras muito diferentes conforme o código de
cada linha.

<!-- tabela: **Tabela 4** — Os seis códigos de faixa tarifária e o efeito de cada um na fatura -->
| Código | O que é | Como entra na fatura |
| ---: | :--- | :--- |
| 1 ou 0 | faixa de consumo | é cobrado o preço por volume que está alocado **dentro** de cada faixa de consumo |
| −1 | tarifa de disponibilidade | valor fixo **somado** à parcela de consumo |
| −2 | franquia retroativa | até o volume da franquia, paga-se o fixo; passando dele, tarifa-se **tudo desde zero** |
| −3 | piso de pagamento | a fatura **não fica** abaixo deste valor |
| 2 | preço-base exponencial | `PB` da fórmula `PB × Cⁿ`, válida até o máximo da linha |
| 3 | expoente da tabela exponencial | o `n` aplicado ao consumo **do mês inteiro** que cai na linha |

A estrutura de Florianópolis, tomada como exemplo, tem cinco linhas: uma de
disponibilidade e quatro faixas progressivas.

```
(0,00 ; 0,00 ; 46,34 ; -1)     disponibilidade, soma sempre
(0,00 ; 10,00 ;  3,08 ;  1)    primeira faixa
(10,00 ; 25,00 ; 14,31 ; 1)    segunda faixa
(25,00 ; 50,00 ; 19,14 ; 1)    terceira
(50,00 ; 999999 ; 24,08 ; 1)   última
```

---

### 3.3.4. Os seis regimes, e por que isso decide projetos

O «consumo mínimo» aparece na conta de quase todo município brasileiro, e significa
coisas **diferentes** em cada um. O programa distingue seis regimes:

<!-- tabela: **Tabela 5** — Os seis regimes tarifários e o que acontece ao economizar em cada um -->
| Regime | O que acontece ao economizar | Municípios na base |
| :--- | :--- | ---: |
| **sem mínimo** | cada m³ economizado desconta | 100 |
| **disponibilidade** | idem; a taxa fixa continua, mas não impede a economia | 122 |
| **fórmula exponencial** | idem; o m³ poupado vale pelo preço-base elevado ao expoente | 36 |
| **franquia no mínimo** | abaixo da franquia, economizar **não desconta nada** | 371 |
| **franquia retroativa** | passando da franquia, tarifa-se tudo desde zero | 23 |
| **piso de pagamento** | a fatura não fica abaixo do piso | 0 |

**O caso que derruba estudo.** Compare duas estruturas reais da base, lado a lado,
para o mesmo consumo:

<!-- tabela: **Tabela 6** — Efeito da economia de água na fatura em dois regimes tarifários opostos -->
| Consumo | Floriano (PI), franquia no mínimo | Florianópolis (SC), disponibilidade |
| ---: | ---: | ---: |
| 14 m³ | R$ 92,15 | R$ 134,38 |
| 12 m³ | R$ 72,52 | R$ 105,76 |
| 10 m³ | R$ 52,89 | R$ 77,14 |
| 8 m³ | **R$ 52,89** | R$ 70,98 |
| 5 m³ | **R$ 52,89** | R$ 61,74 |

Em Floriano, a fatura **para de cair em 10 m³**. Uma residência que consome 12 m³ e
instala um sistema que poupa 4 desce para 8, e economiza R$ 19,63 — e não os R$ 24,17 que a tarifa média de R$ 6,04/m³ sugeriria. Se poupasse 7, desceria para 5 e economizaria os
**mesmos** R$ 19,63: os três metros cúbicos adicionais não valem nada.

Em Florianópolis, cada metro cúbico economizado reduz a fatura, até o primeiro.

> Rodar o caso de Floriano com a estrutura de Florianópolis produz um payback que
> não existe. Trezentos e vinte e nove dos 652 municípios da base estão no regime de
> franquia. É a maioria, e é o cenário mais comum do país.

A Figura 4 mostra as três respostas lado a lado. O que distingue os regimes não é
o preço praticado, e sim o formato da curva: ==onde a curva é horizontal, economizar água
não reduz a fatura em nada.==

![A parcela de água da fatura contra o consumo, em três regimes de mínimo](../figuras/fig05_regimes.png)

*Figura 4 — Parcela de água da fatura mensal em função do consumo, em três regimes de valor mínimo. O esgoto não entra no gráfico porque é cobrado como percentual desta parcela e apenas multiplica a curva, sem mudar-lhe o formato. Na tarifa de disponibilidade e sem valor mínimo, cada metro cúbico economizado reduz a fatura desde o primeiro; na franquia no mínimo, o trecho horizontal marca a faixa de consumo em que a economia de água não reduz a fatura.*

---

### 3.3.5. A fórmula exponencial da CORSAN

Os 34 municípios gaúchos da base atendidos pela CORSAN não cobram a água por faixas.
A parcela de água da fatura é dada por uma fórmula:

```
Água = PB × Cⁿ + SB
```

em que `PB` é o preço-base do município, em R$/m³; `C` é o consumo do mês, em m³; `n` é
o expoente que a **Tabela de Exponenciais** da concessionária atribui àquele consumo; e
`SB` é o serviço básico, cobrado mesmo sem consumo. Na categoria residencial, `n` vale
1,00 até 20 m³ e sobe a cada metro cúbico a partir daí:

<!-- tabela: **Tabela 7** — Expoente n da Tabela de Exponenciais da CORSAN, categoria residencial -->
| Consumo do mês | `n` | Consumo do mês | `n` |
| :--- | ---: | :--- | ---: |
| até 20 m³ | 1,00 | 36 a 45 m³ | 1,10 |
| 21 m³ | 1,01 | 46 a 100 m³ | 1,11 |
| 22 a 27 m³ | 1,02 a 1,07 | 101 a 150 m³ | 1,13 |
| 28 e 29 m³ | 1,08 | 151 a 1.000 m³ | 1,1287 a 1,12 |
| 30 a 35 m³ | 1,09 | acima de 1.000 m³ | 1,11 a 1,0858 |

A tabela segue além de 1.000 m³: só a categoria industrial tem teto nesse volume, acima
do qual o excedente é cobrado por preços próprios. O **esgoto** não entra na fórmula: é
cobrado por metro cúbico consumido, sem o serviço básico e sem o expoente — R$ 6,40/m³
tratado nos municípios do ANEXO-5, 70% do preço-base truncado no centavo.

Duas diferenças em relação às faixas decidem o cálculo:

- **O expoente vale para o consumo inteiro.** Nas faixas, cada metro cúbico é cobrado
  pelo preço da faixa em que cai; na fórmula, o `n` da linha em que o consumo total cai
  se aplica a todo o volume. Passar de 20 para 21 m³ custa R$ 15,09 de água, e não os
  R$ 9,15 do preço-base, porque os 21 m³ inteiros passam a ser elevados a 1,01.
- **Não há degrau de preço, há curva.** O preço médio do metro cúbico de água é
  `PB × Cⁿ⁻¹`: constante até 20 m³ e crescente depois.

<!-- tabela: **Tabela 8** — Fatura mensal em Alegrete (RS) pela fórmula exponencial, vigência 01/07/2026 -->
| Consumo | `n` | Água | Água e esgoto | Preço médio da água |
| ---: | ---: | ---: | ---: | ---: |
| 10 m³ | 1,00 | R$ 134,89 | R$ 198,89 | R$ 13,49/m³ |
| 20 m³ | 1,00 | R$ 226,39 | R$ 354,39 | R$ 11,32/m³ |
| 25 m³ | 1,05 | R$ 312,08 | R$ 472,08 | R$ 12,48/m³ |
| 30 m³ | 1,09 | R$ 416,20 | R$ 608,20 | R$ 13,87/m³ |

Os R$ 134,89 de 10 m³ são exatamente a «tarifa mínima sem hidrômetro» da tabela da
CORSAN, 43,39 + 9,15 × 10, o que confere a transcrição. Para o aproveitamento pluvial,
a consequência é que **toda economia desconta desde o primeiro metro cúbico**, e desconta
mais onde o expoente é maior: uma residência que desce de 30 para 20 m³ economiza
R$ 253,81 por mês. A reta usada antes da 0.1.0, com esgoto de 70% sobre a conta inteira,
dava R$ 155,55 para a mesma redução.

No programa, a fórmula entra na mesma tabela de quádruplas, com dois códigos próprios. A
estrutura de Alegrete começa assim:

```
(0,00 ; 0,00   ; 43,39 ; -1)   serviço básico, soma sempre
(0,00 ; 999999 ;  9,15 ;  2)   preço-base PB
(0,00 ; 20,00  ;  1,00 ;  3)   n para o consumo em (0, 20]
(20,00 ; 21,00 ;  1,01 ;  3)   n para o consumo em (20, 21]
...                            uma linha por intervalo da Tabela de Exponenciais
```

No **Gestor de Tarifas**, a estrutura aparece com o rótulo «Fórmula exponencial», as
linhas «Expoente n» podem ser editadas, o simulador mostra o cálculo `PB × Cⁿ` do consumo
escolhido, e o gráfico de cima traz o preço médio `PB × Cⁿ⁻¹` em vez dos degraus. O campo
do esgoto passa a ser «Esgoto (R$/m³ consumido)», e a etapa econômica oferece o mesmo
modo, «Por m³ consumido», ao lado do valor fixo e do percentual da água.

---

### 3.3.6. Quando o mínimo é diluído na tarifa

Um erro frequente nas bases públicas: a concessionária informa «tarifa mínima de
R$ 52,89 para 10 m³», e quem cadastra grava isso como R$ 5,289 por m³ até 10 m³.

A diferença é enorme. Na primeira leitura, quem consome 4 m³ paga R$ 52,89; na
segunda, paga R$ 21,16. E, pior para um estudo pluvial, na segunda leitura
economizar abaixo de 10 m³ **desconta**, quando na realidade não desconta.

O programa audita a base atrás desse padrão e recodifica os casos encontrados, com o
registro da correção. Se você cadastrar um município novo, **verifique isso**.

---

### 3.3.7. O esgoto

O percentual de esgoto incide sobre a **parcela de água** da fatura, e não sobre a fatura total.

Cem por cento, como em Florianópolis, significa que a parcela de esgoto iguala a de
água — e portanto o esgoto é **metade da fatura**. Economizar água economiza as duas
parcelas, e é por isso que o valor efetivo do metro cúbico poupado quase dobra.

Alguns municípios cobram esgoto por faixas próprias, e não por percentual único.
Nesses casos o percentual único é uma aproximação, e o programa registra a
limitação.

---

### 3.3.8. Vigência, reajuste e tabelas alternativas

A tabela de um município vale desde a data da resolução de onde saiu, e nem sempre há
uma mais recente: a de alguns prestadores é de 2024. O diálogo da tarifa mostra essa data
em **Tabela vigente desde**, ao lado da **Data-base do estudo**, gravada no projeto. Entre
as duas, o programa aplica os reajustes que já caíram, com a taxa de reajuste
configurada, e os seguintes vêm nos aniversários da vigência, não doze meses depois do
início do estudo. Uma tabela de dezembro de 2024, num estudo de outubro de 2026, entra
com um reajuste e recebe o próximo em dezembro. É uma estimativa, porque o reajuste que
de fato houve pode ter sido outro; com a tabela atual em mãos, digite-a com a vigência
dela. Projeto antigo, sem as datas, fica como era.

Alguns municípios têm mais de uma tabela residencial. No Rio de Janeiro, a tarifa muda
por bairro (Área A ou B, Região 1 ou 4, outra concessionária na Barra). Nesses casos a
base guarda uma **tabela representativa** e as demais como alternativas: a procedência
diz por que ela representa o município e qual é a conta de água e esgoto de 10 e de
20 m³ entre a mais barata e a mais cara, e o seletor **Tabela tarifária**, no diálogo,
carrega a que corresponder ao imóvel. Quem tiver a fatura do próprio imóvel pode, como
sempre, digitar a tabela.

### 3.3.9. Onde encontrar o dado

Em ordem de confiabilidade:

1. **Resolução tarifária** da agência reguladora estadual ou municipal. É o documento
   oficial, e traz a data de vigência.
2. **Tabela publicada pela concessionária**, geralmente em «tarifas» no sítio.
3. **Simulador de fatura** da concessionária, quando existir. Bom para conferir:
   simule dois consumos e veja se a sua tabela reproduz os dois valores.
4. **Fatura de água e esgoto real**, do próprio imóvel. É a melhor evidência, e permite
   conferir a estrutura inteira.

> **Sempre registre a data de vigência e a fonte.** Um estudo que não diz de quando
> é a tarifa não pode ser reproduzido daqui a dois anos.

---

### 3.3.10. Confira antes de confiar

Depois de montar a tabela, faça o teste que o item 3.3.7 sugere: simule dois
consumos, um dentro e um fora da faixa mínima, e compare com a fatura real ou com o
simulador da concessionária.

Se os dois baterem, a estrutura está certa. Se só um bater, o regime de mínimo está
errado — e é exatamente esse o erro que mais compromete estudo pluvial.

---

## 3.4. Modular a demanda por calendário

> **Pergunta que este guia responde:** e quando o consumo não é o mesmo todo dia?

Escolas fecham em janeiro e julho, hotéis de praia enchem no verão e escritórios esvaziam
nos fins de semana. Tratar qualquer uma dessas edificações como se tivesse consumo
uniforme erra nos dois sentidos simultaneamente: superestima a demanda nos períodos
vazios e a subestima nos períodos de pico. ==O erro não se compensa ao longo do ano,
porque o que importa ao sistema pluvial não é o total consumido e sim o encontro entre o
consumo e a chuva disponível naquele dia.==

---

### 3.4.1. Os quatro modos

O programa oferece quatro modos de modulação da demanda, que diferem no número de valores que o usuário informa e na situação em que cada um se justifica (Figura 5).



![Os quatro modos de modulação da demanda](../figuras/fig40_modos.png)

*Figura 5 — Os quatro modos de modulação, o que cada um pede ao usuário e a situação em que cada um se justifica. O modo diário só faz sentido quando existe medição real, porque inventar uma série diária acrescenta precisão aparente sem acrescentar informação.*


Em qualquer um deles você pode modular três coisas de forma independente: a
**demanda per capita**, o **número de ocupantes** e a **fração atendível por água
pluvial**.

Modular a ocupação costuma ser mais fiel que modular a demanda: numa escola em
férias não é o aluno que bebe menos água, é que não há aluno.

---

### 3.4.2. Como preencher

Na etapa **2. Edificação e Consumo**, escolha o modo. Abre-se a tabela do período.

- Célula vazia ou zerada **cai para o valor constante**. Isso é deliberado: permite
  modular só os meses que interessam e deixar o resto no padrão.
- Os valores podem ser digitados ou carregados de CSV.
- No modo diário, o primeiro dia da série de demanda alinha com o primeiro dia da
  **série de chuva**. Se as duas tiverem tamanhos diferentes, a de demanda é
  reciclada ciclicamente.

---

### 3.4.3. Por que isso muda o resultado

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

Os dois casos parecem opostos e não o são, e convém enunciar a regra com cuidado,
porque a formulação intuitiva — «demanda em fase com a chuva rende mais» — não
sobrevive ao segundo exemplo. O hotel tem demanda **em fase** com a chuva, já que
ambas culminam no verão, e ainda assim rende menos. O que separa os dois casos não é a
fase, é a **concentração**.

==Uma demanda distribuída ao longo do ano aproveita melhor um mesmo reservatório;
uma demanda concentrada em poucos meses o esvazia em dias e o deixa ocioso no resto do
ano, ainda que esses meses sejam os mais chuvosos.== A escola se beneficia porque o seu
período ocioso coincide com a estiagem, e não porque esteja em fase com a chuva.

Rodadas com a série de Florianópolis, o mesmo consumo anual e o mesmo reservatório de
4.000 L, as três hipóteses se separam: demanda constante rende 27,1%, o perfil escolar
rende 27,3% e o perfil de hotel de praia rende 25,7%. A diferença de quase um ponto e
meio percentual, num teto de 28%, é grande para uma mudança que não altera um único litro do consumo anual, e
é inteiramente invisível a qualquer cálculo feito sobre médias — que é justamente por que o Triton simula dia a dia. Os três perfis estão na Figura 6, e o rendimento de cada um, na Figura 7.

![Três perfis de demanda com o mesmo consumo anual](../figuras/fig19_modulacao.png)

*Figura 6 — Os três perfis de demanda usados na comparação, expressos como a razão entre a demanda do mês e a demanda média. Os três têm exatamente o mesmo consumo anual; o que muda é a distribuição dele ao longo dos doze meses.*

![A demanda contra a chuva, e o que cada perfil rende](../figuras/fig20_tipologias.png)

*Figura 7 — (a) Perfis mensais de demanda da escola e do hotel de praia sobre a precipitação média mensal de Florianópolis; (b) potencial de economia de cada perfil com o mesmo reservatório de 4.000 L. O perfil de hotel concentra em dois meses quase um terço do consumo anual, e é essa concentração, e não a fase, que lhe custa quase um ponto e meio percentual.*

---

### 3.4.4. A fração atendível também pode variar

Menos óbvio e às vezes mais importante. Numa escola, o percentual de uso não potável
muda entre período letivo e férias: em férias permanecem a lavagem de piso e a rega de
jardim, que são usos **integralmente** atendíveis por chuva.

Modular a fração captura isso. Manter fração constante subestima o aproveitamento no
período de baixa ocupação.

Na tabela, a coluna «Não-Potável Interno (%)» é percentual, como todo campo digitado:
28 significa 28%. No arquivo de projeto, a mesma coluna é gravada como fração, 0,28,
e a seção 4.2 (volume Tutorial) explica por quê. Uma célula com valor entre 0 e 1 fica laranja.

---

### 3.4.5. Cuidados

**Não module o que você não mediu.** Uma modulação inventada acrescenta precisão
aparente sem acrescentar informação alguma, e transfere ao leitor a impressão de um rigor
que o dado não tem. Na dúvida, demanda constante explicitamente declarada é mais honesta
que um perfil mensal arbitrado.

**Declare a origem do perfil.** Ele pode vir de medição própria, de doze faturas de água e esgoto
mensais, de referência bibliográfica ou de estimativa, e essas quatro origens não têm o
mesmo peso probatório num estudo publicado.

**Confira o total anual depois de modular.** O programa exibe a demanda média diária
resultante da modulação, e a divergência entre esse valor e o que se esperava é o
indicador mais rápido de erro de preenchimento da tabela.

---

### 3.4.6. O caminho mais simples, quando existe

Se você tem **doze faturas de água e esgoto** da edificação, tem o perfil mensal medido,
que é a melhor fonte possível. Divida o consumo de cada mês pelo número de dias e
pelo número de ocupantes, e use o modo mensal.

Doze faturas valem mais que qualquer referência de literatura.

---

## 3.5. Simular escola, hospital e comércio

> **Pergunta que este guia responde:** o programa serve para edificação não
> residencial?

Serve, e serve bem para a parte hídrica. Há, porém, uma ressalva de peso relativa à
parte econômica, e ela precisa ser conhecida antes de o estudo começar, e não depois de
ele estar concluído.

---

### 3.5.1. A ressalva: a categoria tarifária

As concessionárias brasileiras cobram tarifas distintas conforme a categoria do
consumidor — residencial, comercial, industrial e pública —, e as categorias não
residenciais costumam custar o dobro ou mais da residencial. Na tabela da CASAN vigente
em abril de 2026, por exemplo, a primeira faixa custa R$ 3,08/m³ para uma residência e
R$ 6,81/m³ para um estabelecimento comercial.

==Essas tabelas existem e são públicas:== estão nas resoluções das agências reguladoras e
nos sítios das próprias concessionárias. O que o catálogo do programa registra, para os
652 municípios, é a categoria residencial de cada um, porque levantar as quatro
categorias de cada prestador seria um trabalho de outra ordem de grandeza. ==A tarifa não
residencial não falta ao programa: ela falta ao catálogo, e você pode lançá-la.==

Quando você escolhe uma tipologia não residencial, a Edição Brasil **avisa** e diz o
sentido do erro:

> A tipologia escolhida é «Escola», que a concessionária fatura na categoria
> Pública. O catálogo do programa tem apenas a categoria Residencial, de modo que a
> fatura de água e esgoto está sendo calculada com a tarifa errada. O erro tem sentido
> conhecido: as categorias não residenciais são mais caras, e portanto a economia e
> o retorno estão **subestimados**.

> **O que fazer, em cinco minutos.** Procure a resolução tarifária vigente da sua
> concessionária, que costuma estar no sítio dela sob «tarifas» ou «estrutura tarifária».
> Localize a tabela da categoria que interessa. Lance as faixas no modo personalizado da
> etapa **12. Gestor de Tarifas**, com o regime de mínimo correspondente. A seção
> 3.3 descreve cada campo. Feito isso, o resultado econômico passa a ser o do seu
> caso, e não uma aproximação residencial.

Na International Edition não há catálogo: a tarifa é sempre digitada, e por isso o
programa não mostra esse aviso. Lance diretamente a tarifa da categoria em que a
edificação é faturada.

Há um consolo nessa limitação, e ele é metodológico: ==o erro tem sentido conhecido e é
conservador.== As categorias não residenciais são mais caras que a residencial, de modo
que o projeto real rende mais do que o programa indica, e nunca menos. Um estudo que
declare a limitação apresenta, portanto, um piso de viabilidade — o que é uma posição
defensável, ao contrário do inverso.

---

### 3.5.2. As tipologias disponíveis

As oito tipologias do programa agrupam-se pela categoria tarifária em que a concessionária as enquadra, e cada uma tem unidade de consumo própria (Figura 8). A unidade de consumo muda o significado do per capita informado, e a categoria decide a estrutura de faixas da fatura: simular uma escola com tarifa residencial é um dos enganos descritos na seção 5.1 (volume Enganos, limitações e confiabilidade).



![As tipologias, a categoria tarifária e a unidade de consumo de cada uma](../figuras/fig39_tipologias.png)

*Figura 8 — As oito tipologias disponíveis, agrupadas pela categoria tarifária que a concessionária cobra. A unidade de consumo muda com a tipologia, e é ela que dá sentido ao valor per capita informado.*


---

### 3.5.3. O que muda em cada tipologia

**Escola.** É um dos casos mais favoráveis ao aproveitamento pluvial no Brasil, por
duas razões que se somam. A fração não potável do consumo é alta, porque a bacia
sanitária domina o uso e muitas unidades não têm chuveiro nem cozinha. E a área de
cobertura por aluno costuma ser grande, de modo que a oferta raramente é o fator
limitante.

A modulação por calendário, porém, tem um efeito que depende da região, e convém
simulá-la em vez de supor o resultado. No Sudeste e no Centro-Oeste, as chuvas se
concentram de outubro a março e a estiagem vai de junho a agosto. O recesso de julho
coincide com a estiagem, e a cisterna atravessa o período seco sem ser solicitada; as
férias longas de dezembro a fevereiro, ao contrário, coincidem com o auge das chuvas, e
nesse período a cisterna enche e extravasa sem uso. No Sul, onde a chuva é mais bem
distribuída ao longo do ano, o calendário escolar pesa menos. A seção 3.4 mostra
como representar os dias letivos, e a seção 3.1 mostra como a distribuição da chuva
muda de uma capital para outra.

**Hospital.** O caso mais delicado. Consumo alto e contínuo, sem sazonalidade
relevante, o que é bom para o aproveitamento. Mas a **exigência de qualidade** é
outra: há usos que não admitem água pluvial em hipótese alguma, e a torre de
resfriamento, que seria um uso ideal, exige controle microbiológico contra
legionela. Trate a classe de qualidade com cuidado, e não use as classes adaptadas
2 a 4 como se fossem requisito normativo.

**Escritório e comércio.** Demanda concentrada em dias úteis, cinco dias em sete.
Module por semana. A fração não potável é alta porque quase todo o consumo é bacia
sanitária, mictório e limpeza: Proença e Ghisi (2010), que estimaram os usos finais de
dez edifícios de escritórios em Florianópolis por entrevistas com os ocupantes e medição
de vazões, encontraram de 56% a 86% do consumo em usos não potáveis, e concluíram que a
bacia sanitária deve ser o primeiro alvo de qualquer programa de economia nesses
edifícios. A amplitude da faixa é ela própria uma advertência: dois escritórios da mesma
cidade podem diferir em trinta pontos percentuais, e a fração atendível de um estudo
deve vir do edifício estudado sempre que possível.

**Hotel.** Sazonalidade forte, e é o caso em que modular por mês mais importa. Veja
a advertência da seção 3.4 sobre demanda concentrada: um hotel de litoral lota
justamente nos meses mais chuvosos e ainda assim rende menos que a demanda constante,
porque esvazia o reservatório em poucos dias e o deixa ocioso no resto do ano.

---

### 3.5.4. De onde tirar a fração não potável

A fração atendível é o teto do potencial de economia, como a seção 2.3 (volume O método) mostra, e é
por isso o parâmetro que mais pesa no resultado de uma tipologia não residencial. Há três
caminhos para obtê-la, em ordem decrescente de confiabilidade.

**Medição dos usos finais.** Hidrômetros setoriais ou registradores de vazão nos ramais,
durante algumas semanas representativas. É o único caminho que produz um número do
edifício, e não de uma média.

**Levantamento por entrevista e vazão.** O método de Proença e Ghisi (2010): perguntar aos
ocupantes a frequência e a duração de cada uso e multiplicar pelas vazões medidas dos
aparelhos. Custa pouco e captura o comportamento real do edifício, mas depende da
memória dos entrevistados.

**Valor de referência da literatura.** Aceitável em estudo preliminar, desde que a
referência seja da mesma tipologia, do mesmo país e, idealmente, da mesma região. Evite
transpor frações residenciais para outras tipologias, e mesmo entre residências a
variação é grande: num edifício residencial multifamiliar de Florianópolis, Maykot e
Ghisi (2020) encontraram a bacia sanitária com apenas 9,2% do consumo e a máquina de
lavar com 21,3%, muito abaixo das frações de escritórios e escolas.

> **Declare o caminho.** «Fração atendível de 60%, medida» e «fração atendível de 60%,
> de referência» são estudos diferentes, e o leitor precisa saber qual dos dois está
> lendo.

---

### 3.5.5. Micromedição e o número de economias

Em edifício multifamiliar com medição individualizada, informe o **número de
economias**. O programa avalia o consumo no patamar de **uma** unidade e multiplica
pelo número de economias.

Isso importa por causa das faixas progressivas: um prédio de vinte apartamentos com
medição individual paga vinte faturas na primeira faixa, e não uma fatura que soma
todo o consumo e cai na faixa mais cara. Tratar o prédio como uma unidade só
superestimaria a economia de forma grosseira.

---

### 3.5.6. O que declarar

Além do que a seção 4.10 (volume Tutorial) já pede:

- a **tipologia** e a unidade de consumo adotada;
- a **origem** do consumo per capita — medição, referência ou norma;
- se a **categoria tarifária** foi corrigida ou se ficou a residencial do catálogo,
  e neste caso que o resultado econômico está subestimado;
- o **perfil de modulação** e sua origem;
- para hospital, a classe de qualidade adotada e o que ela cobre.

---

## 3.6. Comparar muitos casos de uma vez

> **Pergunta que este guia responde:** como comparar dezenas de alternativas sem
> refazer o projeto inteiro a cada uma?

O programa foi construído para comparar alternativas, e oferece três formas distintas de
fazê-lo. A escolha entre elas não é questão de preferência: cada forma responde a uma
pergunta diferente, e usar a errada custa tempo sem produzir a informação desejada.

---

### 3.6.1. As três formas

<!-- tabela: **Tabela 9** — As três formas de comparar alternativas conforme o que varia entre elas -->
| Se o que muda é | Use | Onde |
| :--- | :--- | :--- |
| **só o volume da cisterna** | a varredura | etapa 4. Reservatório & Custos |
| **o volume, e você quer decidir** | a tabela multicritério | etapa 8. Decisão Multicritério |
| **qualquer outra premissa** | projetos salvos, um por caso | arquivo `.triton` |

A primeira é automática, a segunda também, e a terceira exige organização.

---

### 3.6.2. A varredura: dezenas de volumes numa passada

Na etapa **4. Reservatório & Custos**, escolha o modo **varredura** e informe o volume
máximo e o passo. O programa simula todos os volumes da grade e desenha a curva.

A varredura é o caminho normal de trabalho, e não uma função avançada reservada a casos
especiais: ela é quase sempre a resposta certa, porque «qual volume adotar?» é a pergunta
central de todo projeto de aproveitamento pluvial. A seção 4.4 (volume Tutorial) percorre uma varredura
completa passo a passo, e a seção 2.2 (volume O método) formaliza como a grade de volumes é montada.

O custo computacional é modesto e não justifica hesitação: uma varredura de 0 a 20.000 L
com passo de 1.000 L corresponde a vinte e uma simulações de trinta anos cada, e é
concluída em poucos segundos numa máquina comum.

---

### 3.6.3. A tabela multicritério: todos os volumes, todas as dimensões

A etapa **8. Decisão Multicritério** mostra, numa tabela só, cada volume da varredura com:

- a economia de água e os dias de atendimento;
- o valor presente líquido, o retorno descontado e a taxa interna de retorno;
- o carbono líquido ao fim da vida útil e o retorno ambiental;
- a pontuação TOPSIS e a aceitabilidade SMAA-VIKOR.

É a forma mais densa de comparar alternativas que o programa oferece: dez colunas de
resposta para cada linha de volume. O **perfil de decisão** troca os pesos dos quatro
eixos — técnico, econômico, ambiental e estrutural —, a linha **Partes no eixo** reparte cada
peso entre os critérios do eixo, e a tabela se reordena na hora. A seção 2.10 (volume O método) explica os
métodos por trás.

---

### 3.6.4. Quando muda outra coisa que não o volume

Cidade, tarifa, demanda, material do reservatório e tipologia da edificação são
parâmetros que a varredura não percorre, e para variar qualquer um deles o caminho é
manter um projeto salvo por caso. O procedimento abaixo parece burocrático à primeira
vista e economiza horas de retrabalho, sobretudo quando o estudo é retomado semanas
depois.

1. Monte o projeto completo uma vez, com todo o detalhe.
2. Salve com um nome que descreva o caso: `escola_florianopolis_5000.triton`.
3. Mude **uma** coisa, e salve com outro nome.
4. Rode cada um, e anote o resultado numa planilha sua.

Os arquivos de exemplo do manual foram feitos assim: `05_manaus.triton`,
`06_brasilia.triton` e `07_saopaulo.triton` são o mesmo projeto, com a série de chuva
trocada. É o que a seção 3.1 compara.

> **Mude uma coisa de cada vez.** Se você trocar a cidade e a tarifa juntas, o
> resultado muda e não há como saber qual das duas o moveu. Parece óbvio, e é o erro
> mais comum em estudos comparativos.

---

### 3.6.5. Como organizar os arquivos

Uma convenção de nomes poupa mais tempo do que parece:

```
estudo_escola/
   base.triton
   cidade_florianopolis.triton
   cidade_manaus.triton
   tarifa_comercial.triton
   demanda_medida.triton
   resultados.xlsx
```

E três hábitos que evitam retrabalho:

**Guarde o projeto, não só o resultado.** O `.triton` tem a chuva dentro dele e
reproduz o estudo inteiro; a planilha de resultados, não.

**Anote o que muda no nome do arquivo.** Seis meses depois, `teste3.triton` não
significa nada.

**Exporte para planilha ao fim de cada rodada.** A etapa **10. Exportação**
grava as tabelas em `.xlsx`, e é lá que a comparação entre casos é montada.

---

### 3.6.6. Quantos casos cabem

O programa não impõe limite ao número de casos comparados, e o limite real é de paciência
do analista: cada simulação de trinta anos leva frações de segundo, mas montar e conferir
cada projeto leva minutos, e é a conferência que consome o tempo.

Na prática, um estudo comparativo bem conduzido reúne entre cinco e vinte casos. Quando o
número cresce muito além disso, costuma ser sinal de que a pergunta de pesquisa não foi
suficientemente delimitada — ou de que o trabalho é um estudo de larga escala, que exige
outro instrumental.

Para estudos de larga escala — matrizes fatoriais de cidade, área, demanda e volume, ou propagação de incerteza — o programa oferece uma interface de linha de comando, descrita a seguir.

---

### 3.6.7. A linha de comando

A instalação do programa como pacote Python registra o comando `triton`, que executa as mesmas rotinas de cálculo da interface gráfica sem abrir a janela; o instalador de Windows com interface gráfica não o inclui. A linha de comando lê arquivos `.triton`, projetos em JSON estruturado e o formato CSV do Netuno 4, e grava os resultados em texto, JSON, CSV, HTML ou XLSX. É a interface indicada para estudos reprodutíveis, porque o próprio comando documenta as premissas alteradas.

<!-- tabela: **Tabela 10** — Subcomandos da linha de comando e finalidade de cada um -->
| Subcomando | Finalidade |
| :--- | :--- |
| `validate` | confere a estrutura do projeto, a série de chuva e as premissas essenciais, sem simular |
| `run` | simula o projeto; por padrão, apenas a análise técnica |
| `analyze` | executa a cadeia completa: técnica, econômica, ambiental, peso do sistema e TOPSIS |
| `econ` | executa a análise econômica |
| `init` | cria um projeto `.triton` modelo, editável, com a série de chuva referenciada ou incorporada |
| `init-catalog` | cria um catálogo JSON modelo de premissas de edificação ou de climas |
| `matrix` | combina um catálogo de premissas com um catálogo de climas e simula todas as combinações |
| `matrix-projects` | executa uma lista de projetos, uma pasta de séries de chuva ou a matriz fatorial declarada no projeto |
| `batch` | executa os cenários de uma planilha CSV ou XLSX, a partir de um projeto-base |
| `uncertainty` | propaga incertezas por Monte Carlo para um volume de reservatório |
| `series-length` | responde de quantos anos de chuva o projeto precisa, pelo método de Geraldi e Ghisi |
| `stochastic-demand` | sorteia o consumo diário e devolve o desempenho como faixa, e não como número único |
| `estudo` | organiza, roda e relata estudos em lote por JSON (`estudo.json`): vários edifícios por tipologia, com tabelas para artigos |

Os subcomandos `run`, `analyze` e `econ` aceitam as mesmas opções: `--analysis` escolhe a análise (`technical`, `economic`, `environmental`, `system_weight`, `topsis` ou `all`); `--volume` fixa o volume do reservatório inferior, em litros; `--rainfall` substitui a série de chuva do projeto; `--set CAMPO=VALOR` altera um campo do projeto e pode ser repetido; `--weights` informa os quatro pesos de eixo do TOPSIS, técnico, econômico, ambiental e estrutural, ou oito, um por critério (três, de projetos até a 0.1.0, ainda valem, e o eixo estrutural recebe a média deles); `--criterion-shares` informa as oito partes no eixo, na ordem dos critérios da seção 2.10 (volume O método), com padrão 1,1,1,1,1,1,1,1; `--weight-sensitivity N` sorteia N vetores de pesos e informa a frequência com que cada volume vence; `--format` e `--output` definem o formato e o arquivo de saída; e `--seed` fixa a semente das análises estocásticas, para que o resultado seja reprodutível.

Aplicados ao projeto do tutorial, `validate` e `run` produzem:

```
triton validate 01_tutorial_florianopolis.triton
Projeto válido: estrutura, chuva e premissas essenciais verificadas.

triton run 01_tutorial_florianopolis.triton --volume 4000 --format json --output r.json
```

O arquivo `r.json` registra a procedência — projeto de origem, número de dias da série e data inicial — e, para o volume de 4.000 L, o potencial de economia de 27,30%, o volume pluvial consumido de 59,8 m³/ano, o extravasamento de 127,5 m³/ano e a classificação dos dias em 97,3% plenos, 0,5% parciais e 2,2% nulos.

O subcomando `uncertainty` sorteia, em cada amostra, a precipitação, a área de captação, a demanda e o investimento com distribuição de coeficiente de variação declarado — por padrão, 10% para a precipitação, 0% para a área, 10% para a demanda e 15% para o investimento, em 200 amostras — e informa os percentis de 5%, 50% e 95% do potencial de economia e do valor presente líquido, com a probabilidade de o valor presente líquido ser positivo. No tutorial, com 50 amostras e 4.000 L, o potencial de economia fica entre 26,8% e 27,6%, com mediana de 27,3%. A faixa é estreita porque o sistema já opera perto do teto de 28%: uma variação de 10% na chuva ou na demanda pouco muda um reservatório que quase nunca seca.

O subcomando `series-length` faz, sem limite de tempo de tela, a análise que a etapa de varredura oferece no botão «a série de chuva é longa o bastante?», descrita na seção 2.2 (volume O método). Sem `--windows`, ele percorre **todas** as janelas possíveis, que é o modo exaustivo dos artigos; com `--windows N`, sorteia N janelas por comprimento, com a semente declarada. As opções `--max-volume`, `--step` e `--threshold` definem a grade e o limiar de ganho marginal, e `--confidence` e `--tolerance` definem o critério de semelhança.

O subcomando `stochastic-demand` sorteia o consumo **dia a dia** e roda a simulação muitas vezes, devolvendo o potencial de economia, os dias plenamente atendidos e o extravasamento como faixa entre os percentis de 5% e 95%. São dois parâmetros de variação, e a diferença entre eles é o que o subcomando tem a ensinar: `--daily-cv` é a variação de um dia para o outro, e `--level-uncertainty` é a incerteza de quanto a edificação consome em média. ==A primeira quase não move o resultado — sorteada de forma independente a cada dia, ela se cancela ao longo de uma série de trinta anos —, e a segunda move.== Com `--absence` declara-se a probabilidade de um dia sem consumo nenhum, como uma viagem, e com `--ideal-volume` o programa apura também o volume ideal de cada realização, que é o que mede se a decisão de projeto resiste à incerteza do consumo.

Esse subcomando não tem equivalente na interface gráfica, e é decisão de projeto: são muitos parâmetros, a leitura exige cuidado, e na tela eles confundiriam mais do que ajudariam.

> Os subcomandos `compare-mass` e `run-vaz-study` executam estudos de pesquisa do grupo sobre bases climáticas de dezenas de milhares de séries, e exigem os arquivos dessas bases; não fazem parte do uso corrente do programa.

---

### 3.6.8. Estudos em lote por JSON

Quando a comparação é por **tipologia** (escolas, comerciais, residências unifamiliares e multifamiliares, hospitais, aeroportos) e o resultado vai para um artigo ou para o resumo de um congresso, manter um projeto salvo por caso e montar a planilha à mão deixa de compensar. O subcomando `estudo` da linha de comando organiza o estudo num arquivo `estudo.json`: o projeto base, os casos, o que muda de um caso para o outro, a análise e as saídas. O programa roda todos os casos numa ordem estável e grava tabelas prontas.

```powershell
## 3.6. 1. Esqueleto do estudo, com os rótulos da tipologia e nenhum valor preenchido.
triton estudo init .\escolas --tipologia escolar

## 3.6. 2. Preencha escolas\estudo.json (os «XX» e null) e coloque os .triton e as séries em escolas\casos.
triton estudo validate .\escolas\estudo.json

## 3.6. 3. Execute todos os casos (em ordem estável); --paralelo N usa N processos e não muda o resultado.
triton estudo run .\escolas\estudo.json --saida .\saida\escolas --paralelo 4

## 3.6. 4. Refaça as tabelas sem recalcular (por exemplo, depois de mudar métricas ou casas decimais).
triton estudo resumo .\saida\escolas

## 3.6. 5. Preencha o texto do resumo do congresso com os números reais.
triton estudo texto .\saida\escolas --modelo .\escolas\modelo_texto.md

## 3.6. 6. Vários estudos (uma pasta com estudo*.json), com o comparativo entre tipologias.
triton estudo lote .\estudos --saida .\saida\comparativo

## 3.6. 7. Reúne os resultados.csv de várias execuções numa só tabela (tipologia, caso, métrica: mínimo, média, mediana, máximo).
triton estudo consolidar .\saida --saida .\saida\consolidado
```

As tipologias (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario`) são só estrutura e rótulos: `estudo init --tipologia` grava o rótulo, o `grupo` dos casos e, num comentário, o que `usuarios` significa naquela tipologia. Nenhum número vem com a tipologia: área, demanda, usuários e fração vêm dos seus casos, com a fonte de cada um.

A ação `consolidar` procura todo `resultados.csv` sob as pastas indicadas (vários estudos, lotes, execuções repetidas) e grava `consolidado.csv` e `consolidado.md` na pasta de saída: uma linha por tipologia (`grupo`), caso e métrica, com `n`, mínimo, média, mediana e máximo dos valores dos casos concluídos (`status` ok). A unidade faz parte da chave do grupo, então moedas diferentes nunca se misturam. Os números têm o mesmo formato do `resultados.csv` (ponto decimal, dez algarismos significativos); a tabela em Markdown segue `--idioma`. Se o pacote opcional `duckdb` estiver instalado (extra opcional `analise`, que não faz parte do instalador), ele lê e agrupa os arquivos; sem ele a biblioteca padrão faz o mesmo, e os dois caminhos dão os mesmos bytes (`--motor csv` força o segundo; `--motor duckdb` exige o pacote).

`estudo run` e `estudo lote` mostram o progresso na saída de erro. `--progresso simples` escreve uma linha por caso (`[i/N] id: ok (t s)`); `--progresso rich` desenha uma barra de progresso e precisa do pacote opcional `rich` (extra opcional `cli`; sem ele o programa avisa uma vez e usa `simples`); o padrão `auto` só usa `rich` se ele estiver instalado e a saída de erro for um terminal. Os arquivos de resultado são idênticos em bytes em qualquer modo, e `--quiet` desliga o progresso.

O que cada seção do `estudo.json` contém, os apelidos das substituições (área de captação, demanda, usuários, fração, volume do reservatório e outros) e os arquivos de saída estão no apêndice «Arquivos, pastas e formatos». O exemplo `examples/estudos/tres-tipologias-exemplo/` roda os casos 1 a 3 de `examples/` (residência unifamiliar, edifício corporativo e escola), um por `grupo`: `triton estudo run examples\estudos\tres-tipologias-exemplo\estudo.json --saida saida\exemplo`.

Na Edição Brasil o relatório da análise não traz bloco de fonte da chuva: registre, no protocolo do estudo, a fonte, o período e o tratamento de cada série. Quando a chuva vem da CLIMBra (`clima.climbra`), o próprio resultado registra o banco, o modelo, o cenário, o recorte e o SHA-256 da série.

> **O programa organiza; quem decide é o analista.** Nenhum campo do esqueleto vem preenchido, e um «XX» ou um `null` impede a execução. Área, demanda, número de usuários e fração atendível de cada edifício precisam vir de uma fonte que o estudo cite. O resumo avisa quando os custos não foram informados (CAPEX igual a zero), porque então o valor presente líquido e o retorno não são resultados.

#### 3.6.8.1. Um estudo por município e por modelo climático

Na Edição Brasil, um `estudo.json` pode ter uma `expansao` que gera um caso por município, por um dos 19 modelos da CLIMBra e por um dos sete recortes sugeridos pelo programa (histórico 1981–2010 e, em SSP2-4.5 e SSP5-8.5, 2021–2050, 2041–2070 e 2071–2100). Um estudo para a lista de municípios de um estado, por exemplo, tem milhares de casos (município × 19 modelos × 7 recortes): rode um estudo por vez e estime o custo antes, com `triton estudo validate`.

Os números da edificação (área de captação, usuários, demanda por usuário, fração atendível, volumes da varredura) são **estimativas de arquétipo, a refinar pelo autor**: não são dados medidos nem de norma. Edite `padroes.substituicoes` (ou, para variar por município, troque `expansao` por `casos` explícitos) e cite a fonte de cada valor. O programa não distribui estudos regionais prontos: o exemplo `examples/estudos/tres-tipologias-exemplo/` mostra o desenho do arquivo, e os estudos de Santa Catarina do grupo de pesquisa são trabalho próprio, publicado à parte.

```powershell
triton estudo validate meu-estudo\estudo.json
triton estudo run meu-estudo\estudo.json --saida meu-estudo\_saida --paralelo 4 --retomar
```

A pasta de saída reúne milhares de arquivos: mantenha-a fora do controle de versão.

---

## 3.7. Análise de sensibilidade

> **Pergunta que este guia responde:** qual premissa mais move o meu resultado, e o
> quanto ele aguenta?

Todo estudo de aproveitamento pluvial repousa sobre premissas incertas, e as três mais
influentes costumam ser justamente as menos verificáveis: a tarifa realmente subirá 5% ao
ano durante vinte anos? A demanda é de fato 150 litros por pessoa e dia? A cisterna
custará o que o orçamento prevê?

A análise de sensibilidade mede quanto dessas dúvidas chega ao resultado final. ==Ela não
elimina a incerteza, e não se propõe a isso; ela mede o tamanho da incerteza,== que é
exatamente a informação de que o leitor precisa para decidir o quanto confiar no número
apresentado.

---

### 3.7.1. O procedimento, em três passos

O procedimento não exige ferramenta especializada, e é o mesmo que se emprega em qualquer
análise de engenharia diante de um parâmetro mal conhecido: varia-se uma coisa de cada
vez e observa-se o efeito.

1. **Escolha a premissa** que você suspeita ser a mais influente.
2. **Rode o projeto três vezes**: com o valor provável, com um valor baixo e com um
   alto.
3. **Anote o resultado das três** e compare.

Repita o procedimento para cada premissa duvidosa. Ao final, você terá identificado
quais delas efetivamente movem o resultado e quais são irrelevantes — e essa separação
vale mais que qualquer refinamento do valor central, porque orienta onde investir esforço
de levantamento de dados. A seção 3.6 mostra como organizar os arquivos para que o
conjunto de rodadas não se transforme em confusão.

---

### 3.7.2. Que faixa adotar para cada premissa

A faixa de variação a adotar para cada premissa não é matéria de palpite: ela decorre do
que se sabe sobre a origem do dado, e um dado medido admite faixa muito mais estreita que um dado tomado da literatura (Figura 9). O reajuste tarifário é expresso em pontos percentuais ao ano; as demais faixas, em percentual do valor adotado.

![A faixa de variação plausível de cada premissa](../figuras/fig41_premissas.png)

*Figura 9 — Faixa de variação plausível de cada premissa numa análise de sensibilidade, com a origem da incerteza. As faixas maiores correspondem às premissas adotadas de referência, e não medidas no projeto.*


> **Não perturbe o que você conhece.** Se a área foi medida em levantamento, a faixa é
> estreita; alargá-la produz uma incerteza artificial que dilui o resultado e esconde
> a premissa que realmente importa.

---

### 3.7.3. As premissas que dominam o resultado econômico

Em estudos econômicos de aproveitamento pluvial, as premissas que mais movem o resultado são as que atuam ao longo de todo o horizonte de análise: o próprio período de análise, o volume de água pluvial efetivamente consumido, a taxa mínima de atratividade e o **reajuste tarifário**. O reajuste merece atenção particular porque é o menos verificável e atua de forma composta: cinco por cento ao ano durante vinte anos multiplicam a tarifa por 2,65; três por cento, por 1,81; e sete por cento, por 3,87. A economia dos últimos anos acompanha esse fator, e a escolha da taxa de reajuste pode decidir boa parte da conclusão econômica do estudo.

Faça o teste no seu caso: na etapa **6. Resultados Econômicos**, mude o reajuste anual
para 3%, anote o VPL, repita com 5% e com 7%. Três rodadas, três minutos, e uma faixa
em vez de um número.

> **Num artigo, mostre essa faixa.** Um valor presente líquido único, calculado com
> reajuste de 5% ao ano e apresentado sem sensibilidade, sugere uma precisão que a
> premissa não tem.

#### 3.7.3.1. O tutorial, premissa por premissa

A tabela a seguir aplica o procedimento ao projeto fechado do tutorial — 4.000 L em
polietileno, recalque para caixa de 1.000 L, VPL provável de R$ 5.524 — e varia cinco
premissas, uma de cada vez, entre um valor baixo e um alto.

<!-- tabela: **Tabela 11** — Potencial, valor presente líquido e retorno do projeto fechado do tutorial com cada premissa variada sozinha, do valor baixo ao alto -->
| Premissa | Baixa | Provável | Alta | Potencial | VPL em 20 anos | Payback descontado |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| reajuste das tarifas de água e esgoto, % ao ano | 3,0 | 5,0 | 7,0 | 27,30% a 27,30% | R$ 860 a R$ 11 360 | 16,8 anos a 10,8 anos |
| taxa mínima de atratividade, % ao mês | 0,3 | 0,5 | 0,7 | 27,30% a 27,30% | R$ 10 014 a R$ 2 241 | 10,9 anos a 15,5 anos |
| consumo per capita, L/hab·dia | 120,0 | 150,0 | 180,0 | 27,73% a 26,72% | R$ -51 a R$ 10 723 | 19,6 anos a 9,6 anos |
| fração atendível, % | 20,0 | 28,0 | 40,0 | 19,91% a 36,96% | R$ -2 532 a R$ 16 058 | não retorna a 7,7 anos |
| preço da cisterna, % do orçamento | 70,0 | 100,0 | 130,0 | 27,30% a 27,30% | R$ 6 282 a R$ 4 766 | 11,8 anos a 13,7 anos |

A leitura separa as premissas em três grupos.

**A que decide o projeto é a fração atendível.** De 20% a 40%, o VPL vai de negativo a
quase o triplo do provável, e o retorno de «não retorna» a menos de oito anos. É a
premissa que a seção 4.2 (volume Tutorial) fixou e que depende da decisão de uso, e não de medição:
incluir ou não a máquina de lavar roupa, com o critério de qualidade que o item 4.1.8 da
NBR 15527:2019 exige, move o resultado mais que qualquer parâmetro econômico.

**As que o mercado decide pesam em seguida.** O reajuste tarifário e a taxa mínima de
atratividade deslocam o VPL em milhares de reais cada um, mas não mexem no potencial. O
consumo per capita move os dois: com menos consumo, a fração atendível pesa sobre uma
demanda menor, a cisterna quase nunca falta, e o potencial sobe um pouco enquanto a
economia em reais cai.

**A que parecia importante quase não pesa.** Trinta por cento a mais ou a menos no preço
da cisterna mudam o VPL em R$ 760 e o retorno em um ano. A cisterna de polietileno é uma
parcela pequena do investimento, e a mão de obra, a tubulação e os acessórios, que não
variam com o volume, dominam a conta.

O resultado inverte a intuição de quem orça antes de simular: gastar tempo cotando a
cisterna vale menos que gastar tempo definindo os usos.

---

### 3.7.4. A sensibilidade que o programa faz sozinho

Há um caso em que a análise de sensibilidade já vem pronta e não exige rodadas
adicionais, e ele diz respeito à decisão final do estudo: a escolha do volume em função
dos pesos atribuídos aos critérios.

Na etapa **8. Decisão Multicritério**, a coluna de **aceitabilidade SMAA-VIKOR** já é uma
análise de sensibilidade pronta. Ela responde: se os pesos das dimensões fossem
sorteados em vez de fixados, com que frequência cada volume ficaria em primeiro lugar?

Leia assim:

<!-- tabela: **Tabela 12** — Leitura da aceitabilidade SMAA-VIKOR do volume vencedor -->
| Aceitabilidade do volume vencedor | O que significa |
| :--- | :--- |
| acima de 70% | recomendação robusta; os pesos quase não importam |
| entre 40 e 70% | recomendação razoável, e vale declarar a segunda opção |
| abaixo de 40% | a escolha depende dos pesos, e o texto precisa dizer isso |

A distinção que essa coluna permite é de natureza epistemológica, e não apenas
estatística: um volume que vence em 80% dos sorteios de pesos constitui uma recomendação,
ao passo que um volume que vence em 30% constitui uma preferência do analista, legítima
desde que apresentada como tal. A seção 2.10 (volume O método) expõe o método que produz esse número.

---

O gráfico de tornado (Figura 10) é a forma consagrada de apresentar esse conjunto: uma barra por
premissa, ordenada pela amplitude, com as duas variações em cores distintas. Lido de
cima para baixo, ele responde à pergunta que o revisor fará primeiro, que é de qual
premissa o resultado depende.

![O tornado de sensibilidade do projeto do tutorial](../figuras/fig24_tornado.png)

*Figura 10 — A variação do valor presente líquido quando cada premissa é alterada em 30% para mais e para menos, mantidas as demais. A cor identifica a variação aplicada, e não o sinal do efeito: é o que permite ver que elevar a taxa mínima de atratividade reduz o valor presente, ao passo que elevar a tarifa o aumenta. O caso-base desta figura sai do modelo econômico simplificado do programa, que desconta um fluxo anual com tarifa marginal única e reajuste declarado; por isso o valor presente do caso-base não coincide com o do fluxo de caixa mensal do tutorial. O que o tornado mede é a sensibilidade relativa, e não o valor absoluto.*

---

### 3.7.5. Como apresentar

Três formas, da mais simples à mais completa:

**Tabela de cenários.** Pessimista, provável e otimista, com as premissas de cada um
declaradas. Simples, honesta e suficiente para a maior parte dos trabalhos.

**Gráfico de tornado.** Uma barra por premissa, mostrando o quanto o resultado varia
quando ela varia sozinha. Ordena as premissas por importância e é a apresentação mais
informativa por área de página.

**Distribuição.** A faixa completa do resultado, quando todas as premissas variam
juntas. Exige declarar as distribuições adotadas, e não só as faixas.

> **Aprofundamento: propagação por Monte Carlo.** A terceira forma é feita sorteando milhares de combinações de premissas e acumulando a distribuição do resultado. O programa faz essa propagação pelo subcomando `uncertainty` da linha de comando, descrito na seção 3.6. Para um estudo de curso
> ou de projeto, a tabela de cenários do primeiro item responde a mesma pergunta com
> uma fração do esforço — e é mais fácil de defender, porque cada cenário tem
> premissas que se pode ler.

---

### 3.7.6. O que declarar

- as **faixas** adotadas e a origem de cada uma;
- quantas rodadas foram feitas, e com que valores;
- para a escolha do volume, a **aceitabilidade** do vencedor;
- **quais premissas não foram perturbadas**, e por quê.

A última é a que mais se esquece, e a que um revisor mais cobra.

---

## 3.8. Importar um projeto do Netuno 4

> **Pergunta que este guia responde:** meus estudos antigos abrem no Triton?

Abrem, e a maior parte dos dados atravessa a conversão sem perda. O cuidado que esta
seção pede decorre de dois fatos que convivem mal: alguns campos não atravessam, e a
importação não avisa quais foram. Um estudo reaproveitado sem conferência pode, por isso,
continuar parecendo o estudo original enquanto simula outra coisa.

---

### 3.8.1. Como importar

Basta abrir o arquivo antigo pelo menu de abertura de projetos. O programa reconhece o
formato legado, que é texto separado por ponto e vírgula, e o converte para a estrutura
interna da versão atual. Feita a conversão, salve o projeto: ele passa a ser gravado no
formato JSON do Triton, com os campos descritos no apêndice A (volume Apêndices), e o arquivo
original permanece intacto no disco, o que convém preservar como evidência do estudo
anterior.

---

### 3.8.2. O que vem na conversão

Praticamente todo o núcleo de entrada do Netuno 4 tem correspondente direto na versão
atual, e é convertido sem intervenção do usuário. A tabela abaixo relaciona o que a
importação recupera.

<!-- tabela: **Tabela 13** — Dados do Netuno 4 recuperados pela importação -->
| Dado | Vem? |
| :--- | :---: |
| arquivo e data inicial da chuva | sim |
| área de captação, coeficiente de escoamento | sim |
| descarte de primeiras águas e modo | sim |
| demanda total e número de moradores | sim |
| percentual atendível por água pluvial | sim |
| reservatório superior, limiar de recalque | sim |
| reservatório inferior, faixa e passo | sim |
| diferença entre potenciais | sim |
| tarifas de água e esgoto, impostos | sim |
| custos iniciais: mão de obra, tubulação, acessórios | sim |
| motobomba: potência, rendimento, vazão, tempo de partida, custo | sim |
| tarifa de energia e impostos | sim |
| inflação, reajuste, período de análise, TMA | sim |
| custos operacionais | sim |

---

### 3.8.3. O que não vem

> **Atenção, e confira sempre.** O leitor de arquivos antigos **não reconhece nenhuma
> chave de demanda variável**. Um projeto do Netuno 4 que utilizasse demanda mensal ou
> diária é importado como demanda **constante**, sem aviso algum.

A consequência dessa limitação merece ser explicitada, porque ela altera resultados sem
alterar a aparência do projeto. Se o estudo original modulava a demanda por calendário —
uma escola em férias, um hotel de temporada — a importação o degrada a consumo uniforme,
e o descasamento entre oferta e demanda que a modulação representava desaparece do
cálculo. Confira o modo de demanda logo após importar, e relance o perfil manualmente se
ele estiver em «constante» quando não deveria estar. A seção 3.4 mostra como.

Há ainda um conjunto de parâmetros que não vêm por razão diversa: eles simplesmente não
existiam no Netuno 4. São a irrigação e a supressão de rega por chuva, a classe de
qualidade da água e a linha de tratamento, os materiais dos reservatórios e os
comprimentos de tubulação por diâmetro, os parâmetros de avaliação de ciclo de vida, os
incentivos fiscais de IPTU verde, a tipologia da edificação e o número de economias.
Todos assumem o valor padrão da versão 5, e todos merecem revisão antes que o projeto
importado seja considerado pronto.

---

### 3.8.4. Por que o resultado muda

Ainda que a importação recupere perfeitamente todos os dados de entrada, o resultado da
simulação não será idêntico ao da versão anterior. A diferença é deliberada, tem causa
conhecida e está quantificada.

A causa principal está no **tratamento do descarte de primeiras águas**. O Netuno 4 trata
a lâmina de descarte como limiar do evento: quando a chuva do dia não atinge a lâmina,
nada é captado; quando a ultrapassa, capta-se a chuva inteira, sem subtração. O Triton
subtrai a lâmina da precipitação do dia, o que é fisicamente mais fiel, porque a água
desviada para o dispositivo de autolimpeza efetivamente não chega à cisterna.

Sobre 4.050 casos de referência, o Triton estima em média de **2,3 a 2,7 pontos
percentuais menos** economia de água potável que o Netuno 4. ==Metade dessa divergência
vem do tratamento do descarte:== 1,36 ponto percentual dos 2,71 medidos no conjunto de
Manaus e São Paulo. As demais causas estão decompostas na seção 6.1 (volume Correções, bugs e versionamento).

---

### 3.8.5. Comparar as duas versões corretamente

Quando o trabalho compara explicitamente as duas versões, existe um procedimento simples
que isola o comportamento do balanço hídrico da divergência metodológica deliberada, e
ele não exige recurso algum do programa: **rode ambas as versões com descarte igual a
zero**. Sem descarte, as duas regras coincidem por construção, e qualquer diferença
remanescente é atribuível à implementação, e não ao método.

Feita essa comparação, repita-a com o descarte real do projeto para medir a diferença
total. Os dois números tomados em conjunto separam o que é mudança deliberada de método
do que seria eventual divergência de implementação, e essa separação é justamente o que
um revisor pede.

> O protocolo de verificação interno menciona uma opção para emular automaticamente a
> regra antiga de descarte. **Essa opção não está implementada.** Use o caminho do
> descarte zero, que produz o mesmo resultado com um pouco mais de trabalho e nenhuma
> surpresa.

---

### 3.8.6. Depois de importar

Sete conferências bastam para transformar um projeto importado num projeto confiável, e
elas devem ser feitas na ordem abaixo, porque as primeiras afetam o resultado das
seguintes.

1. **Modo de demanda** — foi degradado para constante?
2. **Tipologia** da edificação — está na correta?
3. **Materiais** dos reservatórios — o padrão adotado é polietileno.
4. **Classe de qualidade** da água e tecnologia de desinfecção.
5. **Regime tarifário** do município — o Netuno 4 não distinguia os regimes, e a
   seção 3.3 mostra o que isso muda.
6. **Rendimento do motor** da motobomba, que o Netuno 4 não tinha.
7. **Rode o projeto e confira o potencial** contra o resultado antigo antes de confiar
   no arquivo importado.

E guarde o arquivo original: ele é a evidência documental do estudo anterior, e nenhuma
conversão o substitui.

---

## 3.9. Exportar para CAD, BIM e planilha

> **Pergunta que este guia responde:** como levar o resultado para o projeto
> executivo e para a análise própria?

---

### 3.9.1. O que cada formato leva

<!-- tabela: **Tabela 14** — Formatos de exportação e finalidade de cada um -->
| Formato | Extensão | O que leva | Para quê |
| :--- | :--- | :--- | :--- |
| relatório | HTML, PDF | resultado completo e premissas | entregar |
| planilha | XLSX | série diária e varredura | reanalisar |
| auditoria | XLSX | todos os campos das premissas, da tarifa, do tratamento, da ACV, da economia e do arranjo | conferir |
| desenho | DXF | esquema hidráulico dimensionado | projeto executivo |
| manifesto BIM | JSON | componentes com tipo, posição, nível e parâmetros | importação no Revit |
| projeto | TRITON | todas as etapas e a série de chuva | reabrir e auditar |

---

### 3.9.2. O arquivo de projeto

O formato `.triton` é o único que guarda o estudo inteiro: as nove etapas, os pesos do
multicritério, as rotas de ACV e a **série diária de chuva**, incorporada ao próprio
arquivo. Um `.triton` reabre em outra máquina sem o CSV de origem e reproduz o mesmo
número; é com ele que os casos do apêndice J (volume Apêndices) são distribuídos. O CSV do Netuno 4 continua
disponível na exportação, marcado como legado, porque não preserva as etapas acrescentadas
desde então.

---

### 3.9.3. Planilha

A exportação para planilha é o caminho de quem pretende fazer análise própria sobre os
resultados, seja para construir um gráfico que o programa não oferece, seja para
combinar os números do Triton com dados de outra origem. Dois conjuntos de dados estão
disponíveis, e eles respondem a perguntas diferentes.

A **série diária** traz uma linha por dia simulado, com a chuva registrada, a chuva
efetiva depois do descarte, o volume captado, a demanda do dia, o consumo pluvial, o
consumo de rede, o extravasamento, o volume armazenado nos dois reservatórios, o volume
recalcado e a classe de atendimento. É a base de qualquer gráfico ou estatística que o
programa não ofereça pronta, e é o que se usa quando a análise pretendida difere da que o
programa faz.

A **varredura** traz uma linha por volume simulado, com todos os indicadores calculados
para cada um. É a base da curva de retorno decrescente apresentada na seção 4.4 (volume Tutorial), e o
formato adequado para quem queira redesenhá-la com outra apresentação.

A etapa **10. Exportação** monta a planilha a partir de seis conjuntos, que se marcam
um a um: o resumo executivo com os metadados do projeto, o balanço hídrico diário, a
curva da varredura com a confiabilidade, o fluxo de caixa ano a ano, o inventário de
ciclo de vida e a matriz de decisão multicritério. Três escolhas completam a exportação:

<!-- tabela: **Tabela 15** — Opções da exportação de planilha e quando usar cada uma -->
| Opção | Escolhas | Quando usar |
| :--- | :--- | :--- |
| formato | XLSX, CSV ou JSON | XLSX para abrir no Excel; CSV para R, Python ou outro programa; JSON para integração |
| separador do CSV | ponto e vírgula ou vírgula | ponto e vírgula no Excel em português; vírgula no R e na maior parte das ferramentas internacionais |
| filtro temporal | primeiro ano típico ou série completa | o ano para ilustrar; a série completa para qualquer estatística |
| horizonte econômico | 10, 20, 25 ou 30 anos | 20 anos, a vida útil de projeto mínima do sistema hidrossanitário (ABNT NBR 15575-1:2025, Tabela 25), salvo justificativa |

#### 3.9.3.1. Exportar tudo, para auditoria

O botão **Exportar TUDO (auditoria)**, ao lado da exportação da planilha, grava um só
arquivo Excel com as seis abas acima e, além delas, abas que não são escolhidas por
ninguém: percorrem **todos** os campos do que o programa usou. São as premissas do
projeto, uma linha por parâmetro, com o valor e a descrição tirada do próprio código; a
tarifa aplicada, com o significado de cada código de faixa, o regime, o modo do esgoto e
a conta para consumos de 0 a 50 m³; a linha de tratamento dimensionada na etapa de
qualidade, com os estágios, as doses e o carbono que a ACV soma; o inventário de ciclo de
vida item por item; os resultados da simulação, da economia e do multicritério; e o
arranjo 3D, com cada peça, cada trecho e o quantitativo por diâmetro. A aba «0_Leia_me»
diz o que há em cada uma.

É o arquivo para quem precisa conferir uma conta do início ao fim, ou responder a um
avaliador que pergunte o que entrou no carbono ou na economia. Um parâmetro novo no
programa aparece nele sem que ninguém precise se lembrar de acrescentá-lo.

> **Um aviso de tamanho.** Trinta anos de série diária são 10.950 linhas por
> simulação. Uma varredura de doze volumes com série detalhada gera cento e trinta
> mil linhas. Exporte a série detalhada só do volume que interessa.

---

### 3.9.4. Desenho em DXF

O programa gera o esquema hidráulico do sistema dimensionado: cisterna, filtro,
descarte, bomba quando houver, reservatório superior, e a tubulação com os diâmetros
adotados.

O que o programa produz é um **esquema**, e não um projeto executivo. Ele representa os
componentes do sistema e as conexões lógicas entre eles, com os diâmetros adotados, e
serve de base para que o projetista desenhe a instalação em planta, com as cotas, o
traçado e as interferências reais da edificação. ==Um esquema não substitui projeto
hidráulico, e entregá-lo como tal seria erro de responsabilidade técnica.==

O esquema também não carrega, e o projeto executivo precisa acrescentar, os requisitos
de instalação predial da ABNT NBR 15527:2019 para água não potável:

- tubulação de água de chuva pintada ou identificada em **roxo** (Munsell 2.5RP 3/10 ou
  similar), com a inscrição «ÁGUA NÃO POTÁVEL» a cada 3 m nas aparentes (item 4.5.5);
- sistema de distribuição independente do de água potável, sem conexão cruzada
  (4.5.8), com separação atmosférica na alimentação de reserva pela rede, conforme a
  ABNT NBR 5626:2020 (6.15.2);
- pontos de consumo de uso restrito, como a torneira de jardim, com placa «ÁGUA NÃO
  POTÁVEL» (4.5.9);
- reservatórios de água potável e não potável separados, com no mínimo 60 cm entre as
  faces externas quando lado a lado, e o não potável embaixo quando sobrepostos (4.5.10
  e 4.5.11);
- bombeamento conforme a ABNT NBR 5626 (4.5.2), o que inclui as duas bombas do item
  6.5.11.2 daquela norma.

O que o programa **não** dimensiona:

- traçado e declividade da tubulação;
- perda de carga real da instalação;
- arranjo hidráulico do dispositivo de descarte, do qual o programa calcula apenas o volume, `A × d_f`, e o custo;
- extravasor e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

### 3.9.5. Biblioteca de blocos e manifesto BIM

Na etapa **10. Exportação**, o modo *Biblioteca de Blocos para Plantas + BIM JSON* grava os blocos DXF dos componentes em escala 1:1, em milímetros, e, ao lado deles, o arquivo `*_triton-bim.json`. O programa não exporta IFC. O manifesto JSON é o contrato entre o dimensionamento e o modelo: cada instância declara o tipo do componente, o nível, a posição local em milímetros, a rotação e os parâmetros dimensionados, como a capacidade e o diâmetro, e a estrutura é validada antes da gravação.

A integração com o Autodesk Revit é feita por um importador distribuído com o programa, executado no motor CPython 3 do pyRevit, com um documento aberto no Revit 2022 ou posterior, e insere as instâncias do manifesto usando as famílias indicadas em `family_mapping.json`, que associa cada tipo do programa — cisterna, reservatório superior, filtro, descarte inicial, motobomba, registros, válvula de retenção, separação atmosférica, extravasor, ponto de consumo não potável, freio d'água, sucção flutuante, chave de nível, válvula solenoide, hidrômetro, válvula de pé com crivo, respiro e quadro de comando — a uma família e a um tipo do escritório.

Sem organização salva, o programa pré-preenche o arranjo usual dessas instalações, a partir do estudo: captação do telhado, filtro e descarte inicial; cisterna com entrada calma pelo freio d'água, captação pela sucção flutuante com válvula de pé e crivo, chave de nível contra marcha a seco, respiro com tela e extravasor com ladrão sifonado e retenção antirrefluxo para a rede pluvial; registros de manutenção dos dois lados da motobomba, válvula de retenção no recalque e quadro de comando; caixa superior com chave de nível, respiro com tela, extravasor com descarga visível, limpeza com registro junto à saída e distribuição com registro até um ponto de utilização identificado; e o abastecimento potável de reserva — hidrômetro, registro e válvula solenoide — que só abre quando falta água de chuva e descarrega na caixa superior por separação atmosférica, como pede a ABNT NBR 5626:2020. Quem decide é o quadro de comando: com a caixa superior no nível de partida e água na cisterna, liga a motobomba; com a cisterna no mínimo, bloqueia a motobomba e abre a solenoide, que enche a caixa só até a boia de backup, mais baixa, para sobrar volume para a próxima chuva. Motobomba e solenoide nunca funcionam juntas. Na volumetria, os cabos de comando — das chaves de nível ao quadro e dele à motobomba e à solenoide — aparecem tracejados, e a lógica completa está na ficha do quadro. O arranjo é um ponto de partida: posições, percursos e peças são do projetista.

O arranjo segue duas escolhas do projeto:

- **Número de motobombas.** Com duas, a reserva é desenhada em paralelo com a principal, com registro na sucção, válvula de retenção e registro no recalque próprios. Ela se liga às linhas da principal por tês.
- **Arranjo de abastecimento.** Muda o que existe na instalação:
  - **Recalque para caixa superior:** é o arranjo descrito acima.
  - **Pressurização direta:** não há caixa superior. O pressurizador leva a água da cisterna direto ao ponto de utilização. O abastecimento potável de reserva descarrega na própria cisterna, também por separação atmosférica, e só até uma boia de backup instalada nela.
  - **Gravidade:** não há bomba. A cisterna fica sobre uma base, acima do ponto de utilização, e a água sai por uma saída lateral baixa com registro. O abastecimento potável de reserva descarrega na cisterna, como na pressurização.

Enquanto os trechos não são organizados, o arranjo é refeito a cada mudança do volume, do abastecimento ou do número de bombas.

Com esses dados o programa monta também a prancha do esquema 3D, fora de escala e em folha A3 deitada. Só os níveis que organizam a instalação — cisterna, reservatório superior, motobomba, filtro e descarte — ganham plano de cota; as peças pequenas aparecem no desenho pelo código, e o tipo e a cota de cada uma estão na tabela «Peças e acessórios», ao lado da sequência de montagem e do quantitativo por diâmetro.

O importador não cria famílias nem substitui componentes por aproximação: instância sem família ou sem nível correspondente é listada como pendente ao fim da importação. As coordenadas são locais, e a amarração ao ponto-base e ao norte do projeto é feita no Revit, pelo projetista. O manifesto serve à coordenação e ao levantamento de quantitativos, e não substitui a modelagem da instalação hidráulica.

#### 3.9.5.1. Do arranjo ao CAPEX e à ACV

O mesmo arranjo alimenta o custo e o carbono. O programa levanta, peça por peça:

- os metros de tubo por diâmetro;
- as curvas, uma por mudança de direção do percurso;
- as conexões, uma em cada ponta de percurso ligada a uma peça;
- cada peça do manifesto, pelo tipo;
- os metros de cabo de comando.

Cada item recebe preço e massa. O preço vai para o CAPEX: tubos e conexões em *Tubulações*, peças e cabos em *Acessórios*. A massa, vezes o fator do material, vai para a ACV na etapa A1–A3. Cisterna, reservatório superior e motobomba já têm linha própria nas duas análises e não são contados de novo. O filtro e o descarte inicial entram pela ETAP no CAPEX, quando a ETAP está ativa, e pelo subsistema de descarte na ACV, quando ele está ativo.

Um teste automático confere que nenhuma peça, nenhum metro de tubo, nenhuma curva, nenhum tê e nenhum cabo do arranjo fica sem custo ou sem carbono. O teste cobre os três arranjos de abastecimento, com uma e com duas motobombas. A aba `Auditoria_Quantitativo` do *Exportar tudo* lista cada item com o seu destino no CAPEX e na ACV, e fecha a soma contra os valores que as análises usaram. A mesma aba confere ainda se o arranjo está coerente com o projeto: um arranjo organizado à mão pode ficar para trás quando o projeto muda o abastecimento ou o número de bombas, e a divergência aparece ali.

Os preços e as massas das peças são um cenário de referência, e não uma cotação. Ficam em `costs_database.json`, na chave `pecas_do_arranjo`, e podem ser trocados ali. Na etapa econômica, o projetista também pode digitar outros valores de tubulação e acessórios: a partir daí o programa usa os valores digitados. Um projeto novo começa pelo arranjo. Um arquivo antigo mantém os custos que já declarava. Os preços de referência são brasileiros, em reais; na International Edition, e sempre que a moeda do projeto não for o real, o programa não os aplica, e os custos são digitados.

---

### 3.9.6. Relatórios

Os três da seção 4.10 (volume Tutorial): executivo, ambiental com ESG, e científico. Em HTML para
consulta e em PDF para entrega.

> O programa tem dois geradores de PDF e usa o mais completo que a máquina permitir.
> Quando cai para o alternativo, o documento sai mais simples, com o mesmo conteúdo e
> os mesmos números.

---

### 3.9.7. Um conselho de arquivo

Ao fechar um estudo, guarde junto, na mesma pasta:

1. o arquivo `.triton`;
2. a **série de chuva** usada, ou sua identificação exata na base;
3. o relatório científico em PDF;
4. a planilha da varredura;
5. se houve lote, o **script** com os comandos;
6. um arquivo de texto com a **versão do programa**.

São seis itens que tornam o estudo reproduzível daqui a cinco anos. Sem eles, o
relatório em PDF é só uma afirmação.

---

# Apêndices

---

## Apêndice D — Regimes tarifários

> **Só na Edição Brasil (BRL).** O catálogo tarifário é brasileiro e só acompanha a
> Edição Brasil. Na International Edition, a tarifa é informada pelo usuário, num dos
> mesmos seis regimes, e este apêndice serve de descrição deles.

A base traz **652 municípios** com estrutura tarifária, percentual
de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída
da própria base do programa, e não transcrita.

### D.1. Os códigos de faixa

Cada linha da tabela tarifária é uma quádrupla `(mínimo, máximo, valor, código)`.

Os seis códigos e o efeito de cada um sobre a fatura estão desenhados na seção 2.7 (volume O método), e não se repetem aqui.


### D.2. Os seis regimes

<!-- tabela: **Tabela 16** — Distribuição dos municípios do catálogo pelos seis regimes tarifários -->
| Regime | Municípios | O que acontece ao economizar |
| :--- | ---: | :--- |
| **Sem mínimo** | 100 | Cada m³ economizado reduz a fatura. |
| **Disponibilidade** | 122 | Valor fixo que **soma** por cima do consumo medido. Cada m³ economizado desconta. |
| **Franquia no mínimo** | 371 | O valor fixo já inclui um volume. Economizar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | 23 | Até a franquia paga-se o fixo; passando dela, tarifa-se **tudo desde zero**. |
| **Piso de pagamento** | 0 | A fatura **não fica** abaixo do piso. Não soma: limita. |
| **Fórmula exponencial** | 36 | Serviço básico mais `PB × Cⁿ`, com `n` pelo consumo do mês (CORSAN). Cada m³ economizado desconta. |

> O piso de pagamento está implementado e nenhum município da base foi
> classificado nele até esta versão.

### D.3. Distribuição por unidade da federação

A cobertura do catálogo acompanha a população, e não o território: as capitais e as regiões metropolitanas estão quase todas cadastradas, e o interior das regiões Norte e Centro-Oeste concentra os municípios ainda ausentes (Figura 11).

![Os municípios do catálogo, por unidade da federação](../figuras/fig42_uf.png)

*Figura 11 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião. São Paulo e Minas Gerais respondem sozinhos por quase um terço do catálogo.*


### D.4. Atualização e auditoria da base

A base tarifária é mantida pelo grupo com uma rotina de atualização executada fora da interface, antes de cada versão. A rotina tem três componentes.

**Energia elétrica.** As tarifas residenciais do subgrupo B1 são lidas da base aberta de tarifas homologadas das distribuidoras, publicada pela Agência Nacional de Energia Elétrica (ANEEL), e associadas à distribuidora de cada município do catálogo.

**Água e esgoto.** Um registro de evidências primárias associa cada prestador à agência reguladora, à página oficial de tarifas e ao tipo de ato que as publica. Os prestadores com portal padronizado têm leitura automática; os demais são marcados para conferência manual do decreto ou da resolução, e a estrutura resultante é submetida à mesma validação de regime descrita neste apêndice.

**Detecção de alterações.** Cada página oficial monitorada é registrada com a assinatura SHA-256 do conteúdo e os cabeçalhos `ETag` e `Last-Modified`. Uma nova verificação compara as assinaturas e aponta as páginas alteradas desde a última coleta, que são as candidatas a revisão tarifária.

A rotina pode simular a atualização sem gravar a base, executar apenas a detecção de alterações, restringir-se a uma unidade da federação ou a um município e separar energia de saneamento. Cada execução grava um relatório de auditoria em Markdown e um painel HTML com a situação de cada município.

### D.5. Grau de confiança

Cada registro traz o grau de confiança da coleta:

<!-- tabela: **Tabela 17** — Grau de confiança dos registros tarifários do catálogo -->
| Grau | Registros |
| :--- | ---: |
| A — alta | 584 |
| B — boa | 63 |
| C — estrutura a conferir | 5 |

> **Confira sempre a data de vigência** do registro do seu município contra a
> resolução da concessionária. Tarifas são reajustadas anualmente, e a seção 3.3
> ensina o teste que identifica estrutura errada.


### D.6. As faixas por município e categoria

A tabela abaixo traz o preço da água, em R$/m³, em cada intervalo de consumo mensal,
para cada estrutura do catálogo. As colunas são a maior discretização que o catálogo
pede: a união dos limites de faixa de todos os prestadores, de modo que dentro de cada
coluna nenhum prestador muda o preço. Municípios com a mesma tabela formam uma linha,
identificada pelo número da primeira coluna, que se repete nas partes seguintes.

A categoria residencial está nos 652 municípios; as demais aparecem onde a tabela oficial
do prestador foi coletada. A tabela é gerada da base a cada versão e cresce com ela.
A parcela fixa soma por cima do consumo; um preço zero nas primeiras faixas é o volume
já incluído no valor fixo (franquia no mínimo).

A cor da linha diz quanto o dado merece confiança: **verde** (🟢), auditado contra a
fonte primária, a resolução ou a tabela oficial do prestador; **amarelo** (🟡), coletado
automaticamente ou marcado para revisão, e por isso a confirmar contra a resolução
vigente; **vermelho** (🔴), estrutura incompleta, que não deve ser usada sem correção.

São 652 municípios e cinco categorias, 3260 combinações. A primeira tabela diz, para cada categoria, em quantos municípios a tabela tarifária está auditada, a confirmar, incompleta ou ainda não coletada; cada município aparece por extenso nas tabelas seguintes, e as categorias não coletadas estão listadas por prestador ao fim da seção.

<!-- tabela: **Tabela 18** — Cobertura do catálogo tarifário: municípios por categoria e situação do dado -->
| Categoria | 🟢 auditada | 🟡 a confirmar | 🔴 incompleta | 🔴 não coletada | Municípios |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Residencial | 604 | 48 | 0 | 0 | 652 |
| Comercial | 584 | 0 | 0 | 68 | 652 |
| Pública | 574 | 0 | 0 | 78 | 652 |
| Industrial | 578 | 0 | 0 | 74 | 652 |
| Social | 404 | 0 | 0 | 248 | 652 |

<!-- tabela: **Tabela 19** — As estruturas tarifárias do catálogo, numeradas para as tabelas de preço por faixa que vêm a seguir -->
| Nº | Prestador: municípios | Categoria | Fixo (R$/mês) | Esgoto |
| ---: | :--- | :--- | :--- | :--- |
| 🟢 1 | BRK Alagoas: Maceió (AL) | Residencial | 76,40 | 100% |
| 🟢 2 | BRK Alagoas: Marechal Deodoro (AL) | Residencial | 68,19 | 80% |
| 🟢 3 | BRK Alagoas: Rio Largo (AL) | Residencial | 76,40 | 80% |
| 🟢 4 | BRK Alagoas: Maceió (AL) | Comercial | 176,80 | 100% |
| 🟢 5 | BRK Alagoas: Marechal Deodoro (AL) | Comercial | 157,83 | 80% |
| 🟢 6 | BRK Alagoas: Rio Largo (AL) | Comercial | 176,80 | 80% |
| 🟢 7 | BRK Alagoas: Maceió (AL) | Pública | 149,10 | 100% |
| 🟢 8 | BRK Alagoas: Marechal Deodoro (AL) | Pública | 157,83 | 80% |
| 🟢 9 | BRK Alagoas: Rio Largo (AL) | Pública | 149,10 | 80% |
| 🟢 10 | BRK Alagoas: Maceió (AL) | Industrial | 198,50 | 100% |
| 🟢 11 | BRK Alagoas: Marechal Deodoro (AL) | Industrial | 171,90 | 80% |
| 🟢 12 | BRK Alagoas: Rio Largo (AL) | Industrial | 198,50 | 80% |
| 🟢 13 | BRK Alagoas: Maceió (AL) | Social | 38,20 | 100% |
| 🟢 14 | BRK Alagoas: Rio Largo (AL) | Social | 38,20 | 80% |
| 🟢 15 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Residencial | — | 80% |
| 🟢 16 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Comercial | — | 100% |
| 🟢 17 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Pública | — | 100% |
| 🟢 18 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Industrial | — | 100% |
| 🟢 19 | BRK Ambiental Limeira: Limeira (SP) | Residencial | 37,10 | 100% |
| 🟢 20 | BRK Ambiental Limeira: Limeira (SP) | Comercial | 82,40 | 100% |
| 🟢 21 | BRK Ambiental Limeira: Limeira (SP) | Pública | 49,40 | 100% |
| 🟢 22 | BRK Ambiental Limeira: Limeira (SP) | Industrial | 82,40 | 100% |
| 🟢 23 | BRK Ambiental Limeira: Limeira (SP) | Social | 18,55 | 100% |
| 🟡 24 | BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Residencial | 42,00 | 90% |
| 🟢 25 | BRK Ambiental Sumaré: Sumaré (SP) | Residencial | 36,35 | 100% |
| 🟢 26 | BRK Ambiental Sumaré: Sumaré (SP) | Comercial | 83,02 | 100% |
| 🟢 27 | BRK Ambiental Sumaré: Sumaré (SP) | Pública | 83,02 | 100% |
| 🟢 28 | BRK Ambiental Sumaré: Sumaré (SP) | Industrial | 105,64 | 100% |
| 🟢 29 | BRK Ambiental Sumaré: Sumaré (SP) | Social | 18,18 | 100% |
| 🟢 30 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Residencial | — | 70% |
| 🟢 31 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Comercial | — | 70% |
| 🟢 32 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Pública | — | 70% |
| 🟢 33 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Industrial | — | 70% |
| 🟢 34 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Residencial | — | 80% |
| 🟢 35 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Comercial | — | 80% |
| 🟢 36 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Pública | — | 80% |
| 🟢 37 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Industrial | — | 80% |
| 🟢 38 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Social | — | 80% |
| 🟢 39 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Residencial | 33,58 | 100% |
| 🟢 40 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Comercial | 174,42 | 100% |
| 🟢 41 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Pública | 179,16 | 100% |
| 🟢 42 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Industrial | 178,77 | 100% |
| 🟡 43 | CAER: Boa Vista (RR) | Residencial | 39,92 | 80% |
| 🟢 44 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Residencial | 57,51 | 70% |
| 🟢 45 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Comercial | 96,39 | 70% |
| 🟢 46 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Pública | 219,76 | 70% |
| 🟢 47 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Industrial | 143,61 | 70% |
| 🟢 48 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Social | 26,63 | 70% |
| 🟢 49 | CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN), Extremoz (RN), Macaíba (RN), Mossoró (RN), Parnamirim (RN) | Residencial | 56,96 | 70% |
| 🟢 50 | CAERN: Natal (RN) | Residencial | 54,99 | 70% |
| 🟢 51 | CAERN: Natal (RN) | Comercial | 84,61 | 70% |
| 🟢 52 | CAERN: Natal (RN) | Pública | 176,98 | 70% |
| 🟢 53 | CAERN: Natal (RN) | Industrial | 184,53 | 70% |
| 🟢 54 | CAERN: Natal (RN) | Social | 11,09 | 70% |
| 🟢 55 | CAESB: Brasília (DF) | Residencial | 11,62 | 100% |
| 🟢 56 | CAESB: Brasília (DF) | Comercial | 30,51 | 100% |
| 🟢 57 | CAESB: Brasília (DF) | Pública | 30,51 | 100% |
| 🟢 58 | CAESB: Brasília (DF) | Industrial | 30,51 | 100% |
| 🟢 59 | CAESB: Brasília (DF) | Social | 5,81 | 100% |
| 🟡 60 | CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Residencial | 32,50 | 80% |
| 🟢 61 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Residencial | 67,70 | 88% |
| 🟢 62 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Comercial | 169,90 | 88% |
| 🟢 63 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Pública | 148,50 | 88% |
| 🟢 64 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Industrial | 225,00 | 88% |
| 🟢 65 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Residencial | 54,82 | 80% |
| 🟢 66 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Comercial | 97,81 | 90% |
| 🟢 67 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Pública | 111,08 | 100% |
| 🟢 68 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Industrial | 118,47 | 90% |
| 🟢 69 | CASAL: Arapiraca (AL) | Residencial | 72,80 | 80% |
| 🟢 70 | CASAL: Arapiraca (AL) | Comercial | 168,30 | 80% |
| 🟢 71 | CASAL: Arapiraca (AL) | Pública | 141,13 | 80% |
| 🟢 72 | CASAL: Arapiraca (AL) | Industrial | 188,97 | 80% |
| 🟢 73 | CASAL: Arapiraca (AL) | Social | 36,40 | 80% |
| 🟢 74 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Residencial | 46,34 | 100% |
| 🟢 75 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Comercial | 46,34 | 100% |
| 🟢 76 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Pública | 46,34 | 100% |
| 🟢 77 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Industrial | 46,34 | 100% |
| 🟢 78 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Social | 8,63 | 100% |
| 🟢 79 | CEDAE: Barra do Piraí (RJ), Itaperuna (RJ), Macaé (RJ) | Residencial | até 15 m³: 73,69 (retroativa) | 100% |
| 🟢 80 | CEDAE: Barra do Piraí (RJ), Itaperuna (RJ), Macaé (RJ) | Comercial | — | 100% |
| 🟢 81 | CEDAE: Barra do Piraí (RJ), Itaperuna (RJ), Macaé (RJ) | Pública | — | 100% |
| 🟢 82 | CEDAE: Barra do Piraí (RJ), Itaperuna (RJ), Macaé (RJ) | Industrial | — | 100% |
| 🟡 83 | CEDAE/serviço local – validar área: Guapimirim (RJ), Valença (RJ) | Residencial | — | 100% |
| 🟢 84 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Residencial | 16,21 | 70% |
| 🟢 85 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Comercial | 37,31 | 70% |
| 🟢 86 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Pública | 38,04 | 70% |
| 🟢 87 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Industrial | 46,01 | 70% |
| 🟢 88 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Social | 8,10 | 70% |
| 🟢 89 | CODAU Uberaba: Uberaba (MG) | Residencial | — | 95% |
| 🟢 90 | CODAU Uberaba: Uberaba (MG) | Comercial | — | 95% |
| 🟢 91 | CODAU Uberaba: Uberaba (MG) | Pública | — | 95% |
| 🟢 92 | CODAU Uberaba: Uberaba (MG) | Industrial | — | 95% |
| 🟢 93 | CODAU Uberaba: Uberaba (MG) | Social | — | 95% |
| 🟢 94 | CODEN Nova Odessa: Nova Odessa (SP) | Residencial | 17,82 | 100% |
| 🟢 95 | CODEN Nova Odessa: Nova Odessa (SP) | Comercial | 22,33 | 100% |
| 🟢 96 | CODEN Nova Odessa: Nova Odessa (SP) | Industrial | 25,26 | 100% |
| 🟢 97 | CODEN Nova Odessa: Nova Odessa (SP) | Social | 8,91 | 100% |
| 🟢 98 | COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Residencial | 18,38 | 0% |
| 🟢 99 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Residencial | 36,96 | 100% |
| 🟢 100 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Comercial | 74,30 | 100% |
| 🟢 101 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Pública | 55,71 | 100% |
| 🟢 102 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Industrial | 89,17 | 100% |
| 🟢 103 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Social | 18,48 | 100% |
| 🟢 104 | Companhia Águas de Joinville: Joinville (SC) | Residencial | 34,93 | 80% |
| 🟢 105 | Companhia Águas de Joinville: Joinville (SC) | Comercial | 58,20 | 80% |
| 🟢 106 | Companhia Águas de Joinville: Joinville (SC) | Pública | 58,20 | 80% |
| 🟢 107 | Companhia Águas de Joinville: Joinville (SC) | Industrial | 58,20 | 80% |
| 🟢 108 | Companhia Águas de Joinville: Joinville (SC) | Social | 10,48 | 80% |
| 🟢 109 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Residencial | 61,77 | 100% |
| 🟢 110 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Comercial | 90,88 | 100% |
| 🟢 111 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Pública | 87,84 | 100% |
| 🟢 112 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Industrial | 113,88 | 100% |
| 🟢 113 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Social | 27,50 | 100% |
| 🟢 114 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Residencial | 25,77 | 74% |
| 🟢 115 | COPASA: Montes Claros (MG) | Residencial | 25,77 | 74% |
| 🟢 116 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Comercial | 42,86 | 74% |
| 🟢 117 | COPASA: Montes Claros (MG) | Comercial | 42,86 | 74% |
| 🟢 118 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Pública | 36,43 | 74% |
| 🟢 119 | COPASA: Montes Claros (MG) | Pública | 36,43 | 74% |
| 🟢 120 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Industrial | 42,86 | 74% |
| 🟢 121 | COPASA: Montes Claros (MG) | Industrial | 42,86 | 74% |
| 🟢 122 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Social | 9,02 | 74% |
| 🟢 123 | COPASA: Montes Claros (MG) | Social | 9,02 | 74% |
| 🟢 124 | COSAMA: Tabatinga (AM) | Residencial | 25,91 | 80% |
| 🟢 125 | COSAMA: Tabatinga (AM) | Comercial | 111,80 | 80% |
| 🟢 126 | COSAMA: Tabatinga (AM) | Pública | 145,70 | 80% |
| 🟢 127 | COSAMA: Tabatinga (AM) | Industrial | 487,88 | 80% |
| 🟢 128 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Baião (PA), Barcarena (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Residencial | — | 80% |
| 🟢 129 | COSANPA: Altamira (PA) | Residencial | — | 80% |
| 🟢 130 | COSANPA: Parauapebas (PA) | Residencial | — | 80% |
| 🟢 131 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Baião (PA), Barcarena (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Comercial | — | 80% |
| 🟢 132 | COSANPA: Altamira (PA) | Comercial | — | 80% |
| 🟢 133 | COSANPA: Parauapebas (PA) | Comercial | — | 80% |
| 🟢 134 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Baião (PA), Barcarena (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Pública | — | 80% |
| 🟢 135 | COSANPA: Altamira (PA) | Pública | — | 80% |
| 🟢 136 | COSANPA: Parauapebas (PA) | Pública | — | 80% |
| 🟢 137 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Baião (PA), Barcarena (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Industrial | — | 80% |
| 🟢 138 | COSANPA: Altamira (PA) | Industrial | — | 80% |
| 🟢 139 | COSANPA: Parauapebas (PA) | Industrial | — | 80% |
| 🟢 140 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Baião (PA), Barcarena (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Social | — | 80% |
| 🟢 141 | COSANPA: Altamira (PA) | Social | — | 80% |
| 🟢 142 | COSANPA: Parauapebas (PA) | Social | — | 80% |
| 🟢 143 | CSA Equatorial: Macapá (AP), Santana (AP) | Residencial | 45,71 | 100% |
| 🟢 144 | CSA Equatorial: Macapá (AP), Santana (AP) | Comercial | 118,81 | 100% |
| 🟢 145 | CSA Equatorial: Macapá (AP), Santana (AP) | Pública | 325,72 | 100% |
| 🟢 146 | CSA Equatorial: Macapá (AP), Santana (AP) | Industrial | 162,80 | 100% |
| 🟢 147 | CSA Equatorial: Macapá (AP), Santana (AP) | Social | 18,34 | 100% |
| 🟢 148 | DAAE Araraquara: Araraquara (SP) | Residencial | 22,70 | 100% |
| 🟢 149 | DAAE Araraquara: Araraquara (SP) | Comercial | 49,10 | 100% |
| 🟢 150 | DAAE Araraquara: Araraquara (SP) | Pública | 49,10 | 100% |
| 🟢 151 | DAAE Araraquara: Araraquara (SP) | Industrial | 58,30 | 100% |
| 🟢 152 | DAAE Araraquara: Araraquara (SP) | Social | 11,40 | 100% |
| 🟢 153 | DAAE Rio Claro: Rio Claro (SP) | Residencial | 35,36 | 100% |
| 🟢 154 | DAAE Rio Claro: Rio Claro (SP) | Comercial | 94,42 | 100% |
| 🟢 155 | DAAE Rio Claro: Rio Claro (SP) | Industrial | 179,87 | 100% |
| 🟢 156 | DAAE Rio Claro: Rio Claro (SP) | Social | 17,69 | 100% |
| 🟢 157 | DAE Bauru: Bauru (SP) | Residencial | 19,37 | 65% |
| 🟢 158 | DAE Jundiaí: Jundiaí (SP) | Residencial | 40,82 | 117% |
| 🟢 159 | DAE Jundiaí: Jundiaí (SP) | Comercial | 106,98 | 117% |
| 🟢 160 | DAE Jundiaí: Jundiaí (SP) | Pública | 46,95 | 117% |
| 🟢 161 | DAE Jundiaí: Jundiaí (SP) | Industrial | 720,24 | 117% |
| 🟢 162 | DAE Jundiaí: Jundiaí (SP) | Social | 20,42 | 117% |
| 🟡 163 | DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Residencial | — | 80% |
| 🟢 164 | DAE Santa Bárbara d'Oeste: Santa Bárbara d'Oeste (SP) | Residencial | 27,24 | 100% |
| 🟢 165 | DAE Santa Bárbara d'Oeste: Santa Bárbara d'Oeste (SP) | Comercial | 33,47 | 100% |
| 🟢 166 | DAE Santa Bárbara d'Oeste: Santa Bárbara d'Oeste (SP) | Pública | 33,47 | 100% |
| 🟢 167 | DAE Santa Bárbara d'Oeste: Santa Bárbara d'Oeste (SP) | Industrial | 33,47 | 100% |
| 🟢 168 | DAE Santa Bárbara d'Oeste: Santa Bárbara d'Oeste (SP) | Social | 13,62 | 100% |
| 🟡 169 | DAE/VG: Várzea Grande (MT) | Residencial | 31,20 | 80% |
| 🟢 170 | DAEB Bagé: Bagé (RS) | Residencial | 53,37 | 50% |
| 🟢 171 | DAEB Bagé: Bagé (RS) | Comercial | 53,37 | 50% |
| 🟢 172 | DAEB Bagé: Bagé (RS) | Pública | 53,37 | 50% |
| 🟢 173 | DAEB Bagé: Bagé (RS) | Industrial | 64,03 | 50% |
| 🟢 174 | DAEB Bagé: Bagé (RS) | Social | 8,54 | 25% |
| 🟢 175 | DAEP Penápolis: Penápolis (SP) | Residencial | 18,13 | 70% |
| 🟢 176 | DAEP Penápolis: Penápolis (SP) | Comercial | 36,26 | 70% |
| 🟢 177 | DAEP Penápolis: Penápolis (SP) | Pública | 36,26 | 70% |
| 🟢 178 | DAEP Penápolis: Penápolis (SP) | Industrial | 36,26 | 80% |
| 🟡 179 | DAEPA: Patrocínio (MG) | Residencial | — | 80% |
| 🟡 180 | DAESC Coruripe: Coruripe (AL) | Residencial | — | 80% |
| 🟡 181 | DAMAE São João del-Rei: São João del-Rei (MG) | Residencial | — | 80% |
| 🟡 182 | DEMSUR: Muriaé (MG) | Residencial | — | 80% |
| 🟢 183 | DMAE Poços de Caldas: Poços de Caldas (MG) | Residencial | — | 85% |
| 🟢 184 | DMAE Poços de Caldas: Poços de Caldas (MG) | Comercial | — | 85% |
| 🟢 185 | DMAE Poços de Caldas: Poços de Caldas (MG) | Pública | — | 85% |
| 🟢 186 | DMAE Poços de Caldas: Poços de Caldas (MG) | Industrial | — | 85% |
| 🟢 187 | DMAE Poços de Caldas: Poços de Caldas (MG) | Social | — | 85% |
| 🟡 188 | DMAE Uberlândia: Uberlândia (MG) | Residencial | — | 80% |
| 🟡 189 | DMAES Ponte Nova: Ponte Nova (MG) | Residencial | — | 80% |
| 🟢 190 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Residencial | 44,95 | 80% |
| 🟢 191 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Comercial | 66,65 | 80% |
| 🟢 192 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Pública | 66,65 | 80% |
| 🟢 193 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Industrial | 66,65 | 80% |
| 🟢 194 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Social | 7,87 | 80% |
| 🟢 195 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Residencial | 44,77 | 80% |
| 🟢 196 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Comercial | 129,94 | 80% |
| 🟢 197 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Pública | 129,94 | 80% |
| 🟢 198 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Industrial | 129,94 | 80% |
| 🟢 199 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Social | 16,28 | 80% |
| 🟢 200 | GS Inima SAMAR: Araçatuba (SP) | Residencial | 28,48 | 80% |
| 🟢 201 | GS Inima SAMAR: Araçatuba (SP) | Comercial | 55,68 | 80% |
| 🟢 202 | GS Inima SAMAR: Araçatuba (SP) | Pública | 61,63 | 80% |
| 🟢 203 | GS Inima SAMAR: Araçatuba (SP) | Industrial | 55,68 | 80% |
| 🟢 204 | GS Inima SAMAR: Araçatuba (SP) | Social | 9,69 | 80% |
| 🟢 205 | Iguá Sergipe: Aracaju (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Residencial | — | 80% |
| 🟢 206 | Iguá Sergipe: Estância (SE) | Residencial | — | 80% |
| 🟢 207 | Iguá Sergipe: Aracaju (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Comercial | — | 80% |
| 🟢 208 | Iguá Sergipe: Estância (SE) | Comercial | — | 80% |
| 🟢 209 | Iguá Sergipe: Aracaju (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Pública | — | 80% |
| 🟢 210 | Iguá Sergipe: Aracaju (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Industrial | — | 80% |
| 🟢 211 | Iguá Sergipe: Estância (SE) | Industrial | — | 80% |
| 🟢 212 | Iguá Sergipe: Aracaju (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Social | — | 80% |
| 🟢 213 | Iguá Sergipe: Estância (SE) | Social | — | 80% |
| 🟢 214 | Ourinhos Saneamento: Ourinhos (SP) | Residencial | 31,10 | 50% |
| 🟢 215 | Ourinhos Saneamento: Ourinhos (SP) | Comercial | 78,00 | 50% |
| 🟢 216 | Ourinhos Saneamento: Ourinhos (SP) | Pública | 139,80 | 50% |
| 🟢 217 | Ourinhos Saneamento: Ourinhos (SP) | Industrial | 78,00 | 50% |
| 🟢 218 | Ourinhos Saneamento: Ourinhos (SP) | Social | 15,60 | 50% |
| 🟡 219 | Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Residencial | 23,90 | 100% |
| 🟢 220 | Prefeitura de Cosmópolis: Cosmópolis (SP) | Residencial | 31,15 | 100% |
| 🟢 221 | Prefeitura de Cosmópolis: Cosmópolis (SP) | Comercial | 38,94 | 100% |
| 🟢 222 | Prefeitura de Cosmópolis: Cosmópolis (SP) | Industrial | 49,84 | 100% |
| 🟢 223 | Prefeitura de Cosmópolis: Cosmópolis (SP) | Social | 15,58 | 100% |
| 🟡 224 | Prestador municipal/local – Iranduba: Iranduba (AM) | Residencial | 32,50 | 80% |
| 🟡 225 | Prestador municipal/local – Manicoré: Manicoré (AM) | Residencial | 32,50 | 80% |
| 🟡 226 | Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Residencial | 32,50 | 80% |
| 🟡 227 | Prestador municipal/local – Tefé: Tefé (AM) | Residencial | 32,50 | 80% |
| 🟢 228 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Residencial | — | 100% |
| 🟢 229 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Comercial | — | 100% |
| 🟢 230 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Pública | — | 100% |
| 🟢 231 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Industrial | — | 100% |
| 🟢 232 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Social | — | 100% |
| 🟢 233 | RIC Ambiental: Marília (SP) | Residencial | 18,47 | 75% |
| 🟢 234 | RIC Ambiental: Marília (SP) | Comercial | 51,85 | 75% |
| 🟢 235 | RIC Ambiental: Marília (SP) | Pública | 51,85 | 75% |
| 🟢 236 | RIC Ambiental: Marília (SP) | Industrial | 51,85 | 75% |
| 🟢 237 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Residencial | até 15 m³: 84,54 (retroativa) | 100% |
| 🟢 238 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Comercial | — | 100% |
| 🟢 239 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Pública | — | 100% |
| 🟢 240 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Industrial | — | 100% |
| 🟡 241 | SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Residencial | 32,50 | 80% |
| 🟢 242 | SAAE Amparo: Amparo (SP) | Residencial | 29,47 | 90% |
| 🟢 243 | SAAE Amparo: Amparo (SP) | Comercial | 46,51 | 90% |
| 🟢 244 | SAAE Amparo: Amparo (SP) | Pública | 46,51 | 90% |
| 🟢 245 | SAAE Amparo: Amparo (SP) | Industrial | 57,41 | 90% |
| 🟢 246 | SAAE Amparo: Amparo (SP) | Social | 14,73 | 90% |
| 🟡 247 | SAAE Angra dos Reis: Angra dos Reis (RJ) | Residencial | — | 100% |
| 🟢 248 | SAAE Aracruz: Aracruz (ES) | Residencial | — | 80% |
| 🟢 249 | SAAE Aracruz: Aracruz (ES) | Comercial | — | 80% |
| 🟢 250 | SAAE Aracruz: Aracruz (ES) | Pública | — | 80% |
| 🟢 251 | SAAE Aracruz: Aracruz (ES) | Industrial | — | 80% |
| 🟢 252 | SAAE Aracruz: Aracruz (ES) | Social | — | 80% |
| 🟢 253 | SAAE Atibaia: Atibaia (SP) | Residencial | 52,97 | 100% |
| 🟢 254 | SAAE Atibaia: Atibaia (SP) | Comercial | 88,81 | 100% |
| 🟢 255 | SAAE Atibaia: Atibaia (SP) | Pública | 111,77 | 100% |
| 🟢 256 | SAAE Atibaia: Atibaia (SP) | Industrial | 111,77 | 100% |
| 🟢 257 | SAAE Atibaia: Atibaia (SP) | Social | 26,49 | 100% |
| 🟢 258 | SAAE Barra Mansa: Barra Mansa (RJ) | Residencial | — | 60% |
| 🟢 259 | SAAE Barra Mansa: Barra Mansa (RJ) | Comercial | — | 60% |
| 🟢 260 | SAAE Barra Mansa: Barra Mansa (RJ) | Pública | — | 60% |
| 🟢 261 | SAAE Barra Mansa: Barra Mansa (RJ) | Industrial | — | 60% |
| 🟢 262 | SAAE Cacoal: Cacoal (RO) | Residencial | 17,58 | 60% |
| 🟢 263 | SAAE Cacoal: Cacoal (RO) | Comercial | 43,68 | 60% |
| 🟢 264 | SAAE Cacoal: Cacoal (RO) | Pública | 45,46 | 60% |
| 🟢 265 | SAAE Cacoal: Cacoal (RO) | Industrial | 54,15 | 60% |
| 🟢 266 | SAAE Cacoal: Cacoal (RO) | Social | 5,97 | 60% |
| 🟢 267 | SAAE Capivari: Capivari (SP) | Residencial | 33,11 | 90% |
| 🟢 268 | SAAE Capivari: Capivari (SP) | Comercial | 78,09 | 90% |
| 🟢 269 | SAAE Capivari: Capivari (SP) | Industrial | 78,09 | 90% |
| 🟢 270 | SAAE Capivari: Capivari (SP) | Social | 16,56 | 90% |
| 🟡 271 | SAAE Cruzeiro: Cruzeiro (SP) | Residencial | 42,00 | 90% |
| 🟢 272 | SAAE Formiga: Formiga (MG) | Residencial | 22,50 | 50% |
| 🟢 273 | SAAE Formiga: Formiga (MG) | Comercial | 27,00 | 50% |
| 🟢 274 | SAAE Formiga: Formiga (MG) | Pública | 24,75 | 50% |
| 🟢 275 | SAAE Formiga: Formiga (MG) | Industrial | 28,13 | 50% |
| 🟢 276 | SAAE Formiga: Formiga (MG) | Social | 11,25 | 50% |
| 🟡 277 | SAAE Ibitinga: Ibitinga (SP) | Residencial | — | 100% |
| 🟢 278 | SAAE Indaiatuba: Indaiatuba (SP) | Residencial | 35,10 | 90% |
| 🟢 279 | SAAE Indaiatuba: Indaiatuba (SP) | Comercial | 63,00 | 90% |
| 🟢 280 | SAAE Indaiatuba: Indaiatuba (SP) | Pública | 35,10 | 90% |
| 🟢 281 | SAAE Indaiatuba: Indaiatuba (SP) | Industrial | 70,37 | 90% |
| 🟢 282 | SAAE Indaiatuba: Indaiatuba (SP) | Social | 17,55 | 92% |
| 🟢 283 | SAAE Itabira: Itabira (MG) | Residencial | 25,50 | 90% |
| 🟢 284 | SAAE Itabira: Itabira (MG) | Comercial | 32,37 | 90% |
| 🟢 285 | SAAE Itabira: Itabira (MG) | Pública | 26,53 | 90% |
| 🟢 286 | SAAE Itabira: Itabira (MG) | Industrial | 35,14 | 90% |
| 🟢 287 | SAAE Itabira: Itabira (MG) | Social | 12,74 | 90% |
| 🟢 288 | SAAE Itabirito: Itabirito (MG) | Residencial | 22,73 | 60% |
| 🟢 289 | SAAE Itabirito: Itabirito (MG) | Comercial | 30,66 | 60% |
| 🟢 290 | SAAE Itabirito: Itabirito (MG) | Pública | 28,15 | 60% |
| 🟢 291 | SAAE Itabirito: Itabirito (MG) | Industrial | 30,66 | 60% |
| 🟢 292 | SAAE Itabirito: Itabirito (MG) | Social | 11,36 | 60% |
| 🟡 293 | SAAE Itacoatiara: Itacoatiara (AM) | Residencial | 32,50 | 80% |
| 🟢 294 | SAAE Itapira: Itapira (SP) | Residencial | 22,71 | 100% |
| 🟢 295 | SAAE Itapira: Itapira (SP) | Comercial | 30,76 | 100% |
| 🟢 296 | SAAE Itapira: Itapira (SP) | Pública | 22,71 | 100% |
| 🟢 297 | SAAE Itapira: Itapira (SP) | Industrial | 30,76 | 100% |
| 🟢 298 | SAAE Itapira: Itapira (SP) | Social | 11,36 | 100% |
| 🟢 299 | SAAE Jaboticabal: Jaboticabal (SP) | Residencial | 28,91 | 100% |
| 🟢 300 | SAAE Jaboticabal: Jaboticabal (SP) | Comercial | 44,54 | 100% |
| 🟢 301 | SAAE Jaboticabal: Jaboticabal (SP) | Pública | 28,91 | 100% |
| 🟢 302 | SAAE Jaboticabal: Jaboticabal (SP) | Industrial | 44,54 | 100% |
| 🟢 303 | SAAE Jaboticabal: Jaboticabal (SP) | Social | 14,46 | 100% |
| 🟡 304 | SAAE Jacareí: Jacareí (SP) | Residencial | 42,00 | 90% |
| 🟢 305 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Residencial | 41,70 | 65% |
| 🟢 306 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Comercial | 54,41 | 65% |
| 🟢 307 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Pública | 54,41 | 65% |
| 🟢 308 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Industrial | 256,77 | 65% |
| 🟢 309 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Social | 20,85 | 65% |
| 🟡 310 | SAAE Lençóis Paulista: Lençóis Paulista (SP) | Residencial | 42,00 | 90% |
| 🟢 311 | SAAE Linhares: Linhares (ES) | Residencial | — | 80% |
| 🟢 312 | SAAE Linhares: Linhares (ES) | Comercial | — | 80% |
| 🟢 313 | SAAE Linhares: Linhares (ES) | Pública | — | 80% |
| 🟢 314 | SAAE Linhares: Linhares (ES) | Industrial | — | 80% |
| 🟡 315 | SAAE Manhuaçu: Manhuaçu (MG) | Residencial | — | 80% |
| 🟡 316 | SAAE Mariana: Mariana (MG) | Residencial | 29,82 | 100% |
| 🟡 317 | SAAE Maués: Maués (AM) | Residencial | 32,50 | 80% |
| 🟢 318 | SAAE Mogi Mirim: Mogi Mirim (SP) | Residencial | 20,25 | 140% |
| 🟢 319 | SAAE Mogi Mirim: Mogi Mirim (SP) | Comercial | 53,16 | 140% |
| 🟢 320 | SAAE Mogi Mirim: Mogi Mirim (SP) | Pública | 53,16 | 140% |
| 🟢 321 | SAAE Mogi Mirim: Mogi Mirim (SP) | Industrial | 89,44 | 140% |
| 🟢 322 | SAAE Nova Mutum: Nova Mutum (MT) | Residencial | 26,76 | 0% |
| 🟢 323 | SAAE Nova Mutum: Nova Mutum (MT) | Comercial | 66,90 | 0% |
| 🟢 324 | SAAE Nova Mutum: Nova Mutum (MT) | Pública | 83,40 | 0% |
| 🟢 325 | SAAE Nova Mutum: Nova Mutum (MT) | Industrial | 66,90 | 0% |
| 🟡 326 | SAAE Parintins: Parintins (AM) | Residencial | 32,50 | 80% |
| 🟢 327 | SAAE Passos: Passos (MG) | Residencial | 15,29 | 70% |
| 🟢 328 | SAAE Passos: Passos (MG) | Comercial | 21,90 | 70% |
| 🟢 329 | SAAE Passos: Passos (MG) | Pública | 17,44 | 70% |
| 🟢 330 | SAAE Passos: Passos (MG) | Industrial | 21,90 | 70% |
| 🟢 331 | SAAE Passos: Passos (MG) | Social | 7,65 | 70% |
| 🟢 332 | SAAE Pirapora: Pirapora (MG) | Residencial | 43,06 | 50% |
| 🟢 333 | SAAE Pirapora: Pirapora (MG) | Comercial | 51,67 | 50% |
| 🟢 334 | SAAE Pirapora: Pirapora (MG) | Pública | 51,67 | 50% |
| 🟢 335 | SAAE Pirapora: Pirapora (MG) | Industrial | 53,83 | 50% |
| 🟢 336 | SAAE Pirapora: Pirapora (MG) | Social | 21,53 | 50% |
| 🟢 337 | SAAE Porto Feliz: Porto Feliz (SP) | Residencial | 19,29 | 82% |
| 🟢 338 | SAAE Porto Feliz: Porto Feliz (SP) | Comercial | 28,21 | 82% |
| 🟢 339 | SAAE Porto Feliz: Porto Feliz (SP) | Pública | 19,29 | 82% |
| 🟢 340 | SAAE Porto Feliz: Porto Feliz (SP) | Industrial | 47,35 | 82% |
| 🟢 341 | SAAE Porto Feliz: Porto Feliz (SP) | Social | 9,65 | 82% |
| 🟢 342 | SAAE Salto: Salto (SP) | Residencial | 32,22 | 98% |
| 🟢 343 | SAAE Salto: Salto (SP) | Comercial | 46,08 | 98% |
| 🟢 344 | SAAE Salto: Salto (SP) | Pública | 32,22 | 98% |
| 🟢 345 | SAAE Salto: Salto (SP) | Industrial | 161,62 | 98% |
| 🟢 346 | SAAE Salto: Salto (SP) | Social | 16,11 | 98% |
| 🟢 347 | SAAE Sete Lagoas: Sete Lagoas (MG) | Residencial | 30,96 | 80% |
| 🟢 348 | SAAE Sete Lagoas: Sete Lagoas (MG) | Comercial | 72,23 | 80% |
| 🟢 349 | SAAE Sete Lagoas: Sete Lagoas (MG) | Pública | 62,66 | 80% |
| 🟢 350 | SAAE Sete Lagoas: Sete Lagoas (MG) | Industrial | 316,21 | 80% |
| 🟢 351 | SAAE Sorocaba: Sorocaba (SP) | Residencial | 22,00 | 92% |
| 🟢 352 | SAAE Sorocaba: Sorocaba (SP) | Social | 4,39 | 92% |
| 🟢 353 | SAAE São Carlos: São Carlos (SP) | Residencial | — | 100% |
| 🟢 354 | SAAE São Carlos: São Carlos (SP) | Comercial | — | 100% |
| 🟢 355 | SAAE São Carlos: São Carlos (SP) | Pública | — | 100% |
| 🟢 356 | SAAE São Carlos: São Carlos (SP) | Industrial | — | 100% |
| 🟢 357 | SAAE São Carlos: São Carlos (SP) | Social | — | 100% |
| 🟢 358 | SAAE São Mateus: São Mateus (ES) | Residencial | — | 80% |
| 🟢 359 | SAAE São Mateus: São Mateus (ES) | Comercial | — | 80% |
| 🟢 360 | SAAE São Mateus: São Mateus (ES) | Pública | — | 80% |
| 🟢 361 | SAAE São Mateus: São Mateus (ES) | Industrial | — | 80% |
| 🟢 362 | SAAE São Mateus: São Mateus (ES) | Social | — | 80% |
| 🟡 363 | SAAE Três Pontas: Três Pontas (MG) | Residencial | — | 80% |
| 🟡 364 | SAAE Três Rios: Três Rios (RJ) | Residencial | — | 100% |
| 🟡 365 | SAAE Vilhena: Vilhena (RO) | Residencial | 57,51 | 70% |
| 🟡 366 | SAAE Viçosa: Viçosa (MG) | Residencial | — | 50% |
| 🟡 367 | SAAE Volta Redonda: Volta Redonda (RJ) | Residencial | — | 100% |
| 🟢 368 | SAAEB Ambiental: Bebedouro (SP) | Residencial | 34,62 | 80% |
| 🟢 369 | SAAEB Ambiental: Bebedouro (SP) | Comercial | 43,45 | 80% |
| 🟢 370 | SAAEB Ambiental: Bebedouro (SP) | Industrial | 43,45 | 80% |
| 🟢 371 | SAAEB Barretos: Barretos (SP) | Residencial | 30,59 | 50% |
| 🟢 372 | SAAEB Barretos: Barretos (SP) | Comercial | 36,72 | 50% |
| 🟢 373 | SAAEB Barretos: Barretos (SP) | Pública | 30,59 | 50% |
| 🟢 374 | SAAEB Barretos: Barretos (SP) | Industrial | 42,83 | 50% |
| 🟢 375 | SAAEB Barretos: Barretos (SP) | Social | 15,29 | 50% |
| 🟢 376 | SAAEJA: Jaguariúna (SP) | Residencial | 22,81 | 100% |
| 🟢 377 | SAAEJA: Jaguariúna (SP) | Comercial | 54,29 | 100% |
| 🟢 378 | SAAEJA: Jaguariúna (SP) | Industrial | 109,26 | 100% |
| 🟢 379 | SAAEJA: Jaguariúna (SP) | Social | 11,40 | 100% |
| 🟡 380 | SAAET: Taquaritinga (SP) | Residencial | 42,00 | 90% |
| 🟢 381 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Suzano (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Residencial | 40,42 | 100% |
| 🟢 382 | SABESP: Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Campo Limpo Paulista (SP), Caçapava (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Lorena (SP), Mococa (SP), Monte Mor (SP), Paulínia (SP), Piedade (SP), Pindamonhangaba (SP), São José dos Campos (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Taubaté (SP), Tremembé (SP), Tupã (SP), Várzea Paulista (SP) | Residencial | 40,42 | 80% |
| 🟢 383 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Residencial | 40,42 | 100% |
| 🟢 384 | SABESP: Lins (SP) | Residencial | 32,27 | 80% |
| 🟢 385 | SABESP: Olímpia (SP) | Residencial | 25,34 | 80% |
| 🟢 386 | SABESP: Presidente Prudente (SP) | Residencial | 34,53 | 80% |
| 🟢 387 | SABESP: Registro (SP) | Residencial | 40,42 | 100% |
| 🟢 388 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Suzano (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Comercial | 81,57 | 100% |
| 🟢 389 | SABESP: Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Campo Limpo Paulista (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Mococa (SP), Monte Mor (SP), Paulínia (SP), Piedade (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Tupã (SP), Várzea Paulista (SP) | Comercial | 81,57 | 80% |
| 🟢 390 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Comercial | 81,57 | 100% |
| 🟢 391 | SABESP: Caçapava (SP), Lorena (SP), Pindamonhangaba (SP), São José dos Campos (SP), Taubaté (SP), Tremembé (SP) | Comercial | 81,57 | 80% |
| 🟢 392 | SABESP: Lins (SP) | Comercial | 64,96 | 80% |
| 🟢 393 | SABESP: Olímpia (SP) | Comercial | 36,22 | 80% |
| 🟢 394 | SABESP: Presidente Prudente (SP) | Comercial | 61,19 | 80% |
| 🟢 395 | SABESP: Registro (SP) | Comercial | 81,57 | 100% |
| 🟢 396 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Suzano (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Pública | 81,57 | 100% |
| 🟢 397 | SABESP: Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Campo Limpo Paulista (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Mococa (SP), Monte Mor (SP), Paulínia (SP), Piedade (SP), Presidente Prudente (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Tupã (SP), Várzea Paulista (SP) | Pública | 81,57 | 80% |
| 🟢 398 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Pública | 81,57 | 100% |
| 🟢 399 | SABESP: Caçapava (SP), Lorena (SP), Pindamonhangaba (SP), São José dos Campos (SP), Taubaté (SP), Tremembé (SP) | Pública | 81,57 | 80% |
| 🟢 400 | SABESP: Lins (SP) | Pública | 64,96 | 80% |
| 🟢 401 | SABESP: Olímpia (SP) | Pública | 78,18 | 80% |
| 🟢 402 | SABESP: Registro (SP) | Pública | 81,57 | 100% |
| 🟢 403 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Suzano (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Industrial | 81,57 | 100% |
| 🟢 404 | SABESP: Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Campo Limpo Paulista (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Mococa (SP), Monte Mor (SP), Paulínia (SP), Piedade (SP), Presidente Prudente (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Tupã (SP), Várzea Paulista (SP) | Industrial | 81,57 | 80% |
| 🟢 405 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Industrial | 81,57 | 100% |
| 🟢 406 | SABESP: Caçapava (SP), Lorena (SP), Pindamonhangaba (SP), São José dos Campos (SP), Taubaté (SP), Tremembé (SP) | Industrial | 81,57 | 80% |
| 🟢 407 | SABESP: Lins (SP) | Industrial | 64,96 | 80% |
| 🟢 408 | SABESP: Olímpia (SP) | Industrial | 72,43 | 80% |
| 🟢 409 | SABESP: Registro (SP) | Industrial | 81,57 | 100% |
| 🟢 410 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Suzano (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Social | 11,46 | 100% |
| 🟢 411 | SABESP: Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Campo Limpo Paulista (SP), Caçapava (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Lorena (SP), Mococa (SP), Monte Mor (SP), Paulínia (SP), Piedade (SP), Pindamonhangaba (SP), Presidente Prudente (SP), São José dos Campos (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Taubaté (SP), Tremembé (SP), Tupã (SP), Várzea Paulista (SP) | Social | 11,46 | 80% |
| 🟢 412 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Social | 11,46 | 100% |
| 🟢 413 | SABESP: Lins (SP) | Social | 9,91 | 80% |
| 🟢 414 | SABESP: Olímpia (SP) | Social | 12,67 | 80% |
| 🟢 415 | SABESP: Registro (SP) | Social | 11,46 | 100% |
| 🟢 416 | SAE Araguari: Araguari (MG) | Residencial | 33,89 | 80% |
| 🟢 417 | SAE Araguari: Araguari (MG) | Comercial | 47,84 | 80% |
| 🟢 418 | SAE Araguari: Araguari (MG) | Pública | 47,84 | 80% |
| 🟢 419 | SAE Araguari: Araguari (MG) | Industrial | 81,68 | 80% |
| 🟢 420 | SAE Araguari: Araguari (MG) | Social | 14,29 | 80% |
| 🟢 421 | SAE Ituiutaba: Ituiutaba (MG) | Residencial | 18,12 | 70% |
| 🟢 422 | SAE Ituiutaba: Ituiutaba (MG) | Comercial | 21,75 | 70% |
| 🟢 423 | SAE Ituiutaba: Ituiutaba (MG) | Pública | 22,65 | 70% |
| 🟢 424 | SAE Ituiutaba: Ituiutaba (MG) | Industrial | 158,58 | 70% |
| 🟢 425 | SAE Ituiutaba: Ituiutaba (MG) | Social | 9,06 | 70% |
| 🟢 426 | SAE Louveira: Louveira (SP) | Residencial | 27,93 | 85% |
| 🟢 427 | SAE Louveira: Louveira (SP) | Comercial | 37,68 | 85% |
| 🟢 428 | SAE Louveira: Louveira (SP) | Pública | 27,93 | 85% |
| 🟢 429 | SAE Louveira: Louveira (SP) | Industrial | 37,68 | 85% |
| 🟢 430 | SAE Louveira: Louveira (SP) | Social | 13,97 | 85% |
| 🟢 431 | SAEAN Artur Nogueira: Artur Nogueira (SP) | Residencial | 43,37 | 100% |
| 🟢 432 | SAEAN Artur Nogueira: Artur Nogueira (SP) | Comercial | 54,21 | 100% |
| 🟢 433 | SAEAN Artur Nogueira: Artur Nogueira (SP) | Pública | 54,21 | 100% |
| 🟢 434 | SAEAN Artur Nogueira: Artur Nogueira (SP) | Industrial | 65,08 | 100% |
| 🟢 435 | SAEAN Artur Nogueira: Artur Nogueira (SP) | Social | 21,69 | 100% |
| 🟢 436 | SAEC Catanduva: Catanduva (SP) | Residencial | — | 100% |
| 🟢 437 | SAEC Catanduva: Catanduva (SP) | Social | — | 100% |
| 🟢 438 | SAECIL Leme: Leme (SP) | Residencial | 35,33 | 85% |
| 🟢 439 | SAECIL Leme: Leme (SP) | Social | 17,67 | 85% |
| 🟢 440 | SAEG: Guaratinguetá (SP) | Residencial | 30,06 | 80% |
| 🟢 441 | SAEG: Guaratinguetá (SP) | Comercial | 60,38 | 80% |
| 🟢 442 | SAEG: Guaratinguetá (SP) | Pública | 60,38 | 80% |
| 🟢 443 | SAEG: Guaratinguetá (SP) | Industrial | 68,43 | 80% |
| 🟢 444 | SAEG: Guaratinguetá (SP) | Social | 15,03 | 80% |
| 🟢 445 | SAEMA Araras: Araras (SP) | Residencial | 25,71 | 80% |
| 🟢 446 | SAEMA Araras: Araras (SP) | Comercial | 44,87 | 80% |
| 🟢 447 | SAEMA Araras: Araras (SP) | Pública | 27,76 | 80% |
| 🟢 448 | SAEMA Araras: Araras (SP) | Industrial | 80,08 | 80% |
| 🟢 449 | SAEMA Araras: Araras (SP) | Social | 12,86 | 80% |
| 🟢 450 | SAEMAS Sertãozinho: Sertãozinho (SP) | Residencial | 25,31 | 80% |
| 🟢 451 | SAEMAS Sertãozinho: Sertãozinho (SP) | Social | 12,66 | 80% |
| 🟢 452 | SAEP Pirassununga: Pirassununga (SP) | Residencial | 29,91 | 100% |
| 🟢 453 | SAEP Pirassununga: Pirassununga (SP) | Comercial | 39,52 | 100% |
| 🟢 454 | SAEP Pirassununga: Pirassununga (SP) | Industrial | 58,69 | 100% |
| 🟢 455 | SAEP Pirassununga: Pirassununga (SP) | Social | 14,96 | 100% |
| 🟢 456 | SAERP Ribeirão Preto: Ribeirão Preto (SP) | Residencial | 14,06 | 128% |
| 🟢 457 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Residencial | 29,99 | 80% |
| 🟢 458 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Comercial | 46,47 | 80% |
| 🟢 459 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Pública | 46,47 | 80% |
| 🟢 460 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Industrial | 46,47 | 80% |
| 🟢 461 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Social | 9,00 | 80% |
| 🟡 462 | SAESA: São Caetano do Sul (SP) | Residencial | 42,00 | 90% |
| 🟢 463 | SAEV Ambiental: Votuporanga (SP) | Residencial | 28,22 | 100% |
| 🟢 464 | SAEV Ambiental: Votuporanga (SP) | Comercial | 62,76 | 100% |
| 🟢 465 | SAEV Ambiental: Votuporanga (SP) | Pública | 87,11 | 100% |
| 🟢 466 | SAEV Ambiental: Votuporanga (SP) | Industrial | 62,76 | 100% |
| 🟢 467 | SAEV Ambiental: Votuporanga (SP) | Social | 14,11 | 100% |
| 🟢 468 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Residencial | 47,43 | 112% |
| 🟢 469 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Comercial | 71,89 | 112% |
| 🟢 470 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Pública | 47,43 | 112% |
| 🟢 471 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Industrial | 71,89 | 112% |
| 🟢 472 | SAMAE Brusque: Brusque (SC) | Residencial | 42,38 | 0% |
| 🟢 473 | SAMAE Brusque: Brusque (SC) | Comercial | 100,33 | 0% |
| 🟢 474 | SAMAE Brusque: Brusque (SC) | Pública | 42,38 | 0% |
| 🟢 475 | SAMAE Brusque: Brusque (SC) | Industrial | 100,33 | 0% |
| 🟢 476 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Residencial | 38,30 | R$ 4,90/m³ |
| 🟢 477 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Comercial | 82,15 | R$ 5,26/m³ |
| 🟢 478 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Pública | 82,15 | R$ 5,26/m³ |
| 🟢 479 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Industrial | 217,65 | R$ 6,96/m³ |
| 🟢 480 | SAMAE Gaspar: Gaspar (SC) | Residencial | 50,58 | 0% |
| 🟢 481 | SAMAE Gaspar: Gaspar (SC) | Comercial | 65,35 | 0% |
| 🟢 482 | SAMAE Gaspar: Gaspar (SC) | Pública | 50,58 | 0% |
| 🟢 483 | SAMAE Gaspar: Gaspar (SC) | Industrial | 140,88 | 0% |
| 🟢 484 | SAMAE Gaspar: Gaspar (SC) | Social | 25,29 | 0% |
| 🟢 485 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Residencial | 30,16 | 80% |
| 🟢 486 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Comercial | 51,02 | 80% |
| 🟢 487 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Pública | 51,02 | 80% |
| 🟢 488 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Industrial | 51,02 | 80% |
| 🟢 489 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Residencial | 18,91 | 100% |
| 🟢 490 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Comercial | 46,91 | 100% |
| 🟢 491 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Pública | 63,05 | 100% |
| 🟢 492 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Industrial | 78,03 | 100% |
| 🟢 493 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Social | 9,46 | 100% |
| 🟢 494 | SAMAE São Bento do Sul: São Bento do Sul (SC) | Residencial | 30,08 | 80% |
| 🟢 495 | SAMAE São Bento do Sul: São Bento do Sul (SC) | Comercial | 62,38 | 80% |
| 🟡 496 | SAMAE Tangará da Serra: Tangará da Serra (MT) | Residencial | — | 80% |
| 🟢 497 | SANASA Campinas: Campinas (SP) | Residencial | 53,65 | 123% |
| 🟢 498 | SANASA Campinas: Campinas (SP) | Social | 26,83 | 123% |
| 🟢 499 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Residencial | 38,37 | 80% |
| 🟢 500 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Comercial | 77,59 | 80% |
| 🟢 501 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Pública | 264,62 | 80% |
| 🟢 502 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Industrial | 119,30 | 80% |
| 🟢 503 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Residencial | 17,46 | 100% |
| 🟢 504 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Comercial | 17,46 | 100% |
| 🟢 505 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Pública | 17,46 | 100% |
| 🟢 506 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Industrial | 17,46 | 100% |
| 🟢 507 | Saneaqua: Mairinque (SP) | Residencial | 47,10 | 100% |
| 🟢 508 | Saneaqua: Mairinque (SP) | Comercial | 94,20 | 100% |
| 🟢 509 | Saneaqua: Mairinque (SP) | Pública | 94,20 | 100% |
| 🟢 510 | Saneaqua: Mairinque (SP) | Industrial | 94,20 | 100% |
| 🟢 511 | Saneaqua: Mairinque (SP) | Social | 15,10 | 100% |
| 🟢 512 | SANEAR Colatina: Colatina (ES) | Residencial | — | 80% |
| 🟢 513 | SANEAR Colatina: Colatina (ES) | Comercial | — | 80% |
| 🟢 514 | SANEAR Colatina: Colatina (ES) | Pública | — | 80% |
| 🟢 515 | SANEAR Colatina: Colatina (ES) | Industrial | — | 80% |
| 🟡 516 | SANEAR Rondonópolis: Rondonópolis (MT) | Residencial | 36,50 | 80% |
| 🟢 517 | SANEBAVI Vinhedo: Vinhedo (SP) | Residencial | 40,20 | 100% |
| 🟢 518 | SANEBAVI Vinhedo: Vinhedo (SP) | Comercial | 47,91 | 100% |
| 🟢 519 | SANEBAVI Vinhedo: Vinhedo (SP) | Pública | 40,20 | 100% |
| 🟢 520 | SANEBAVI Vinhedo: Vinhedo (SP) | Industrial | 385,95 | 100% |
| 🟢 521 | SANEBAVI Vinhedo: Vinhedo (SP) | Social | 20,10 | 100% |
| 🟢 522 | Saneouro: Ouro Preto (MG) | Residencial | 23,60 | 95% |
| 🟢 523 | Saneouro: Ouro Preto (MG) | Social | 7,87 | 95% |
| 🟢 524 | SANEP Pelotas: Pelotas (RS) | Residencial | 24,01 | 80% |
| 🟢 525 | SANEP Pelotas: Pelotas (RS) | Comercial | 42,88 | 80% |
| 🟢 526 | SANEP Pelotas: Pelotas (RS) | Pública | 85,65 | 80% |
| 🟢 527 | SANEP Pelotas: Pelotas (RS) | Industrial | 85,65 | 80% |
| 🟢 528 | SANEPAR – Curitiba: Curitiba (PR) | Residencial | 55,09 | 85% |
| 🟢 529 | SANEPAR – Curitiba: Curitiba (PR) | Comercial | 99,17 | 85% |
| 🟢 530 | SANEPAR – Curitiba: Curitiba (PR) | Pública | 99,17 | 85% |
| 🟢 531 | SANEPAR – Curitiba: Curitiba (PR) | Industrial | 99,17 | 85% |
| 🟢 532 | SANEPAR – Curitiba: Curitiba (PR) | Social | 27,54 | 85% |
| 🟢 533 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Residencial | 55,09 | 80% |
| 🟢 534 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Comercial | 99,17 | 80% |
| 🟢 535 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Pública | 99,17 | 80% |
| 🟢 536 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Industrial | 99,17 | 80% |
| 🟢 537 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Social | 27,54 | 80% |
| 🟡 538 | Sanessol: Mirassol (SP) | Residencial | 42,00 | 90% |
| 🟢 539 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS) | Residencial | 17,60 | 50% |
| 🟢 540 | SANESUL: Três Lagoas (MS) | Residencial | 6,90 | 50% |
| 🟢 541 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS) | Comercial | 17,60 | 50% |
| 🟢 542 | SANESUL: Três Lagoas (MS) | Comercial | 6,90 | 50% |
| 🟢 543 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS) | Pública | 17,60 | 50% |
| 🟢 544 | SANESUL: Três Lagoas (MS) | Pública | 6,90 | 50% |
| 🟢 545 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS) | Industrial | 17,60 | 50% |
| 🟢 546 | SANESUL: Três Lagoas (MS) | Industrial | 6,90 | 50% |
| 🟢 547 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS) | Social | 5,11 | 50% |
| 🟢 548 | SANESUL: Três Lagoas (MS) | Social | 2,60 | 50% |
| 🟢 549 | SEMAE Mogi das Cruzes: Mogi das Cruzes (SP) | Residencial | 31,43 | 90% |
| 🟢 550 | SEMAE Mogi das Cruzes: Mogi das Cruzes (SP) | Comercial | 79,00 | 100% |
| 🟢 551 | SEMAE Mogi das Cruzes: Mogi das Cruzes (SP) | Pública | 79,00 | 100% |
| 🟢 552 | SEMAE Mogi das Cruzes: Mogi das Cruzes (SP) | Industrial | 79,00 | 100% |
| 🟢 553 | SEMAE Mogi das Cruzes: Mogi das Cruzes (SP) | Social | 15,71 | 90% |
| 🟢 554 | SEMAE Piracicaba: Piracicaba (SP) | Residencial | 33,52 | 100% |
| 🟢 555 | SEMAE Piracicaba: Piracicaba (SP) | Social | 16,76 | 100% |
| 🟢 556 | SeMAE Rio Preto: São José do Rio Preto (SP) | Residencial | 26,63 | 100% |
| 🟢 557 | SEMAE São Leopoldo: São Leopoldo (RS) | Residencial | 61,29 | 80% |
| 🟢 558 | SEMAE São Leopoldo: São Leopoldo (RS) | Comercial | 114,36 | 80% |
| 🟢 559 | SEMAE São Leopoldo: São Leopoldo (RS) | Pública | 194,44 | 80% |
| 🟢 560 | SEMAE São Leopoldo: São Leopoldo (RS) | Industrial | 194,44 | 80% |
| 🟢 561 | SEMAE São Leopoldo: São Leopoldo (RS) | Social | 24,53 | 50% |
| 🟢 562 | SEMASA Itajaí: Itajaí (SC) | Residencial | 41,70 | 80% |
| 🟢 563 | SEMASA Itajaí: Itajaí (SC) | Comercial | 58,00 | 80% |
| 🟢 564 | SEMASA Itajaí: Itajaí (SC) | Pública | 61,10 | 80% |
| 🟢 565 | SEMASA Itajaí: Itajaí (SC) | Industrial | 58,00 | 80% |
| 🟢 566 | SEMASA Lages: Lages (SC) | Residencial | 44,00 | 80% |
| 🟢 567 | SEMASA Lages: Lages (SC) | Comercial | 61,34 | 80% |
| 🟢 568 | SEMASA Lages: Lages (SC) | Pública | 61,34 | 80% |
| 🟢 569 | SEMASA Lages: Lages (SC) | Industrial | 61,34 | 80% |
| 🟡 570 | São Gabriel Saneamento S.A.: São Gabriel (RS) | Residencial | 33,89 | 80% |
| 🟢 571 | Tubarão Saneamento: Tubarão (SC) | Residencial | — | 100% |
| 🟢 572 | Tubarão Saneamento: Tubarão (SC) | Comercial | — | 100% |
| 🟢 573 | Tubarão Saneamento: Tubarão (SC) | Pública | — | 100% |
| 🟢 574 | Tubarão Saneamento: Tubarão (SC) | Industrial | — | 100% |
| 🟢 575 | Tubarão Saneamento: Tubarão (SC) | Social | — | 100% |
| 🟢 576 | Verde Alagoas: União dos Palmares (AL) | Residencial | 55,80 | 80% |
| 🟢 577 | Verde Alagoas: União dos Palmares (AL) | Comercial | 114,20 | 80% |
| 🟢 578 | Verde Alagoas: União dos Palmares (AL) | Pública | 87,90 | 80% |
| 🟢 579 | Verde Alagoas: União dos Palmares (AL) | Industrial | 123,50 | 80% |
| 🟢 580 | Verde Alagoas: União dos Palmares (AL) | Social | 27,90 | 80% |
| 🟢 581 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Residencial | — | 90% |
| 🟢 582 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Comercial | — | 90% |
| 🟢 583 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Pública | — | 90% |
| 🟢 584 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Industrial | — | 90% |
| 🟢 585 | Águas Cuiabá (Iguá): Cuiabá (MT) | Residencial | 49,20 | 90% |
| 🟢 586 | Águas Cuiabá (Iguá): Cuiabá (MT) | Comercial | 76,50 | 90% |
| 🟢 587 | Águas Cuiabá (Iguá): Cuiabá (MT) | Pública | 96,10 | 90% |
| 🟢 588 | Águas Cuiabá (Iguá): Cuiabá (MT) | Industrial | 89,70 | 90% |
| 🟢 589 | Águas da Imperatriz: Teresópolis (RJ) | Residencial | até 15 m³: 69,18 (retroativa) | 90% |
| 🟢 590 | Águas da Imperatriz: Teresópolis (RJ) | Comercial | — | 90% |
| 🟢 591 | Águas da Imperatriz: Teresópolis (RJ) | Pública | — | 90% |
| 🟢 592 | Águas da Imperatriz: Teresópolis (RJ) | Industrial | — | 90% |
| 🟡 593 | Águas das Agulhas Negras: Resende (RJ) | Residencial | — | 100% |
| 🟡 594 | Águas de Andradina: Andradina (SP) | Residencial | 42,00 | 90% |
| 🟢 595 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Residencial | — | 80% |
| 🟢 596 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Comercial | — | 80% |
| 🟢 597 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Pública | — | 80% |
| 🟢 598 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Industrial | — | 80% |
| 🟡 599 | Águas de Jahu: Jaú (SP) | Residencial | 42,00 | 90% |
| 🟢 600 | Águas de Juturnaíba: Araruama (RJ) | Residencial | — | 100% |
| 🟢 601 | Águas de Juturnaíba: Araruama (RJ) | Comercial | — | 100% |
| 🟢 602 | Águas de Juturnaíba: Araruama (RJ) | Pública | — | 100% |
| 🟢 603 | Águas de Juturnaíba: Araruama (RJ) | Industrial | — | 100% |
| 🟢 604 | Águas de Manaus: Manaus (AM) | Residencial | — | 80% |
| 🟢 605 | Águas de Manaus: Manaus (AM) | Comercial | — | 80% |
| 🟢 606 | Águas de Manaus: Manaus (AM) | Pública | — | 80% |
| 🟢 607 | Águas de Manaus: Manaus (AM) | Industrial | — | 80% |
| 🟢 608 | Águas de Manaus: Manaus (AM) | Social | — | 80% |
| 🟢 609 | Águas de Matão: Matão (SP) | Residencial | 45,32 | 100% |
| 🟢 610 | Águas de Matão: Matão (SP) | Comercial | 45,50 | 100% |
| 🟢 611 | Águas de Matão: Matão (SP) | Social | 22,66 | 100% |
| 🟡 612 | Águas de Niterói: Niterói (RJ) | Residencial | — | 100% |
| 🟡 613 | Águas de Nova Friburgo: Nova Friburgo (RJ) | Residencial | — | 100% |
| 🟡 614 | Águas de Pará de Minas: Pará de Minas (MG) | Residencial | — | 80% |
| 🟢 615 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Residencial | — | 90% |
| 🟢 616 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Comercial | — | 90% |
| 🟢 617 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Pública | — | 90% |
| 🟢 618 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Industrial | — | 90% |
| 🟢 619 | Águas de Sinop (Aegea): Sinop (MT) | Residencial | — | 100% |
| 🟢 620 | Águas de Sinop (Aegea): Sinop (MT) | Comercial | — | 100% |
| 🟢 621 | Águas de Sinop (Aegea): Sinop (MT) | Pública | — | 100% |
| 🟢 622 | Águas de Sinop (Aegea): Sinop (MT) | Industrial | — | 100% |
| 🟢 623 | Águas de Sorriso: Sorriso (MT) | Residencial | — | 80% |
| 🟢 624 | Águas de Sorriso: Sorriso (MT) | Comercial | — | 80% |
| 🟢 625 | Águas de Sorriso: Sorriso (MT) | Pública | — | 80% |
| 🟢 626 | Águas de Sorriso: Sorriso (MT) | Industrial | — | 80% |
| 🟢 627 | Águas de Teresina: Teresina (PI) | Residencial | 46,83 | 80% |
| 🟢 628 | Águas de Teresina: Teresina (PI) | Comercial | 96,11 | 80% |
| 🟢 629 | Águas de Teresina: Teresina (PI) | Pública | 96,11 | 80% |
| 🟢 630 | Águas de Teresina: Teresina (PI) | Industrial | 96,11 | 80% |
| 🟢 631 | Águas de Teresina: Teresina (PI) | Social | 20,54 | 80% |
| 🟢 632 | Águas de Valadares (Aegea): Governador Valadares (MG) | Residencial | 14,67 | 70% |
| 🟢 633 | Águas de Valadares (Aegea): Governador Valadares (MG) | Comercial | 19,11 | 70% |
| 🟢 634 | Águas de Valadares (Aegea): Governador Valadares (MG) | Pública | 19,11 | 70% |
| 🟢 635 | Águas de Valadares (Aegea): Governador Valadares (MG) | Industrial | 21,19 | 70% |
| 🟢 636 | Águas de Valadares (Aegea): Governador Valadares (MG) | Social | 7,34 | 70% |
| 🟢 637 | Águas de Votorantim: Votorantim (SP) | Residencial | 29,86 | 80% |
| 🟢 638 | Águas de Votorantim: Votorantim (SP) | Comercial | 88,39 | 80% |
| 🟢 639 | Águas de Votorantim: Votorantim (SP) | Pública | 88,39 | 80% |
| 🟢 640 | Águas de Votorantim: Votorantim (SP) | Industrial | 218,98 | 80% |
| 🟢 641 | Águas de Votorantim: Votorantim (SP) | Social | 14,93 | 80% |
| 🟡 642 | Águas do Imperador: Petrópolis (RJ) | Residencial | — | 100% |
| 🟢 643 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Residencial | — | 0% |
| 🟢 644 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Comercial | — | 0% |
| 🟢 645 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Pública | — | 0% |
| 🟢 646 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Industrial | — | 0% |
| 🟡 647 | Águas do Paraíba: Campos dos Goytacazes (RJ) | Residencial | — | 100% |
| 🟢 648 | Águas do Pará: Ananindeua (PA), Belém (PA), Marituba (PA) | Residencial | — | 80% |
| 🟢 649 | Águas do Pará: Ananindeua (PA), Belém (PA), Marituba (PA) | Comercial | — | 80% |
| 🟢 650 | Águas do Pará: Ananindeua (PA), Belém (PA), Marituba (PA) | Pública | — | 80% |
| 🟢 651 | Águas do Pará: Ananindeua (PA), Belém (PA), Marituba (PA) | Industrial | — | 80% |
| 🟢 652 | Águas do Pará: Ananindeua (PA), Belém (PA), Marituba (PA) | Social | — | 80% |
| 🟢 653 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Residencial | 52,89 | 80% |
| 🟢 654 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Comercial | 108,57 | 80% |
| 🟢 655 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Pública | 108,57 | 80% |
| 🟢 656 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Industrial | 108,57 | 80% |
| 🟢 657 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Social | 26,44 | 80% |
| 🟢 658 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), São João de Meriti (RJ) | Residencial | até 15 m³: 86,37 (retroativa) | 100% |
| 🟢 659 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ), Maricá (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ) | Residencial | até 15 m³: 85,41 (retroativa) | 100% |
| 🟢 660 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), São João de Meriti (RJ) | Comercial | — | 100% |
| 🟢 661 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ), Maricá (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ) | Comercial | — | 100% |
| 🟢 662 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), São João de Meriti (RJ) | Pública | — | 100% |
| 🟢 663 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ), Maricá (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ) | Pública | — | 100% |
| 🟢 664 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), São João de Meriti (RJ) | Industrial | — | 100% |
| 🟢 665 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ), Maricá (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ) | Industrial | — | 100% |
| 🟢 666 | Águas do Rio (tarifa representativa; Iguá na Barra e em Jacarepaguá): Rio de Janeiro (RJ) | Residencial | até 15 m³: 98,46 (retroativa) | 100% |
| 🟢 667 | Águas do Rio (tarifa representativa; Iguá na Barra e em Jacarepaguá): Rio de Janeiro (RJ) | Comercial | — | 100% |
| 🟢 668 | Águas do Rio (tarifa representativa; Iguá na Barra e em Jacarepaguá): Rio de Janeiro (RJ) | Pública | — | 100% |
| 🟢 669 | Águas do Rio (tarifa representativa; Iguá na Barra e em Jacarepaguá): Rio de Janeiro (RJ) | Industrial | — | 100% |
| 🟢 670 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL) | Residencial | 73,90 | 80% |
| 🟢 671 | Águas do Sertão: Penedo (AL) | Residencial | 61,40 | 80% |
| 🟢 672 | Águas do Sertão: São Miguel dos Campos (AL) | Residencial | 54,90 | 80% |
| 🟢 673 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL), Penedo (AL) | Comercial | 170,70 | 80% |
| 🟢 674 | Águas do Sertão: São Miguel dos Campos (AL) | Comercial | 126,90 | 80% |
| 🟢 675 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL), Penedo (AL) | Pública | 144,00 | 80% |
| 🟢 676 | Águas do Sertão: São Miguel dos Campos (AL) | Pública | 107,00 | 80% |
| 🟢 677 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL), Penedo (AL) | Industrial | 191,70 | 80% |
| 🟢 678 | Águas do Sertão: São Miguel dos Campos (AL) | Industrial | 142,40 | 80% |
| 🟢 679 | Águas Guariroba: Campo Grande (MS) | Residencial | 19,87 | 70% |
| 🟢 680 | Águas Guariroba: Campo Grande (MS) | Comercial | 30,14 | 70% |
| 🟢 681 | Águas Guariroba: Campo Grande (MS) | Pública | 100,56 | 70% |
| 🟢 682 | Águas Guariroba: Campo Grande (MS) | Industrial | 47,38 | 70% |
| 🟢 683 | Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Residencial | — | 90% |

<!-- tabela: **Tabela 20** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 1 de 6: 0–4 a 15–20 m³) -->
| Nº | 0–4 | 4–5 | 5–6 | 6–7 | 7–10 | 10–11 | 11–12 | 12–13 | 13–15 | 15–20 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,61 | 14,61 | 14,61 | 14,61 | 16,89 |
| 🟢 2 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,70 | 12,70 | 12,70 | 12,70 | 14,27 |
| 🟢 3 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,61 | 14,61 | 14,61 | 14,61 | 16,89 |
| 🟢 4 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 21,31 | 21,31 | 21,31 | 21,31 | 21,31 |
| 🟢 6 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 27,34 | 27,34 | 27,34 | 27,34 | 27,34 |
| 🟢 9 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,30 | 7,30 | 7,30 | 7,30 | 8,45 |
| 🟢 14 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,30 | 7,30 | 7,30 | 7,30 | 8,45 |
| 🟢 15 | 4,26 | 4,26 | 4,26 | 4,26 | 4,26 | 9,47 | 9,47 | 9,47 | 9,47 | 9,47 |
| 🟢 16 | 10,55 | 10,55 | 10,55 | 10,55 | 10,55 | 13,29 | 13,29 | 13,29 | 13,29 | 13,29 |
| 🟢 17 | 10,14 | 10,14 | 10,14 | 10,14 | 10,14 | 13,38 | 13,38 | 13,38 | 13,38 | 13,38 |
| 🟢 18 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 | 15,82 |
| 🟢 19 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,11 | 5,11 | 5,11 | 5,11 | 10,14 |
| 🟢 20 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟢 21 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 |
| 🟢 22 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,24 | 8,24 | 8,24 | 8,24 | 13,18 |
| 🟢 23 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,56 | 2,56 | 2,56 | 2,56 | 7,61 |
| 🟡 24 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 25 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 |
| 🟢 26 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,30 | 8,30 | 8,30 | 8,30 | 8,30 |
| 🟢 27 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,30 | 8,30 | 8,30 | 8,30 | 8,30 |
| 🟢 28 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,57 | 10,57 | 10,57 | 10,57 | 10,57 |
| 🟢 29 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,82 | 1,82 | 1,82 | 1,82 | 2,73 |
| 🟢 30 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,70 | 10,70 | 10,70 | 10,70 | 10,70 |
| 🟢 31 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,70 | 10,70 | 10,70 | 10,70 | 10,70 |
| 🟢 32 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,70 | 10,70 | 10,70 | 10,70 | 10,70 |
| 🟢 33 | 13,81 | 13,81 | 13,81 | 13,81 | 13,81 | 14,41 | 14,41 | 14,41 | 14,41 | 14,41 |
| 🟢 34 | 8,76 | 8,76 | 3,05 | 3,05 | 3,05 | 8,66 | 8,66 | 8,66 | 8,66 | 11,07 |
| 🟢 35 | 22,48 | 22,48 | 7,68 | 7,68 | 7,68 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 17,04 |
| 🟢 37 | 16,64 | 16,64 | 16,64 | 16,64 | 16,64 | 16,64 | 16,64 | 16,64 | 16,64 | 23,12 |
| 🟢 38 | 2,62 | 2,62 | 0,92 | 0,92 | 0,92 | 5,62 | 5,62 | 5,62 | 5,62 | 9,42 |
| 🟢 39 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 40 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,51 |
| 🟢 41 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 19,56 |
| 🟢 42 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,71 |
| 🟡 43 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,40 | 5,40 | 5,40 | 5,40 | 5,40 |
| 🟢 44 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,52 | 6,52 | 6,52 | 6,52 | 7,17 |
| 🟢 45 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 46 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 26,15 |
| 🟢 47 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,96 |
| 🟢 48 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,66 | 2,66 | 2,66 | 2,66 | 2,66 |
| 🟢 49 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,34 | 6,34 | 6,34 | 6,34 | 7,51 |
| 🟢 50 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,13 | 6,13 | 6,13 | 6,13 | 7,24 |
| 🟢 51 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,67 | 10,67 | 10,67 | 10,67 | 11,46 |
| 🟢 52 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 53 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 54 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,13 | 6,13 | 6,13 | 6,13 | 7,24 |
| 🟢 55 | 4,30 | 4,30 | 4,30 | 4,30 | 5,15 | 5,15 | 5,15 | 5,15 | 10,21 | 10,21 |
| 🟢 56 | 8,87 | 11,08 | 11,08 | 11,08 | 14,30 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 57 | 8,87 | 11,08 | 11,08 | 11,08 | 14,30 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 58 | 8,87 | 11,08 | 11,08 | 11,08 | 14,30 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 59 | 2,15 | 2,15 | 2,15 | 2,15 | 2,58 | 2,58 | 2,58 | 2,58 | 5,11 | 5,11 |
| 🟡 60 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 61 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,78 | 8,78 | 8,78 | 8,78 | 9,49 |
| 🟢 62 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,99 | 16,99 | 16,99 | 16,99 | 16,99 |
| 🟢 63 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,73 |
| 🟢 64 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 17,81 |
| 🟢 65 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,08 | 7,08 | 7,08 | 7,08 | 7,08 |
| 🟢 66 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,90 | 13,90 | 13,90 | 13,90 | 16,07 |
| 🟢 70 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,95 | 6,95 | 6,95 | 6,95 | 8,03 |
| 🟢 74 | 3,08 | 3,08 | 3,08 | 3,08 | 3,08 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 75 | 6,81 | 6,81 | 6,81 | 6,81 | 6,81 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 76 | 6,81 | 6,81 | 6,81 | 6,81 | 6,81 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 6,81 | 6,81 | 6,81 | 6,81 | 6,81 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 0,58 | 0,58 | 0,58 | 0,58 | 0,58 | 4,11 | 4,11 | 4,11 | 4,11 | 4,11 |
| 🟢 79 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 | 12,38 |
| 🟢 80 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 81 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 16,44 |
| 🟢 82 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 | 26,45 |
| 🟡 83 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟢 84 | 1,78 | 1,78 | 4,82 | 4,82 | 4,82 | 6,02 | 6,02 | 6,02 | 6,02 | 6,83 |
| 🟢 85 | 4,02 | 4,02 | 4,02 | 4,02 | 4,02 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 |
| 🟢 86 | 2,59 | 2,59 | 2,59 | 2,59 | 2,59 | 4,32 | 4,32 | 4,32 | 4,32 | 4,32 |
| 🟢 87 | 4,82 | 4,82 | 4,82 | 4,82 | 4,82 | 5,42 | 5,42 | 5,42 | 5,42 | 5,42 |
| 🟢 88 | 0,89 | 0,89 | 0,89 | 0,89 | 0,89 | 0,89 | 0,89 | 0,89 | 0,89 | 3,41 |
| 🟢 89 | 3,91 | 3,91 | 3,91 | 3,91 | 3,91 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 |
| 🟢 90 | 4,55 | 4,55 | 4,55 | 4,55 | 4,55 | 5,31 | 5,31 | 5,31 | 5,31 | 5,31 |
| 🟢 91 | 4,55 | 4,55 | 4,55 | 4,55 | 4,55 | 5,31 | 5,31 | 5,31 | 5,31 | 5,31 |
| 🟢 92 | 5,01 | 5,01 | 5,01 | 5,01 | 5,01 | 5,76 | 5,76 | 5,76 | 5,76 | 5,76 |
| 🟢 93 | 1,96 | 1,96 | 1,96 | 1,96 | 1,96 | 1,96 | 1,96 | 1,96 | 1,96 | 2,60 |
| 🟢 94 | 0,00 | 0,00 | 4,11 | 4,11 | 4,11 | 4,81 | 4,81 | 4,81 | 4,81 | 5,40 |
| 🟢 95 | 0,00 | 0,00 | 5,34 | 5,34 | 5,34 | 6,02 | 6,02 | 6,02 | 6,02 | 6,86 |
| 🟢 96 | 0,00 | 0,00 | 5,73 | 5,73 | 5,73 | 6,61 | 6,61 | 6,61 | 6,61 | 7,30 |
| 🟢 97 | 0,00 | 0,00 | 2,05 | 2,05 | 2,05 | 2,41 | 2,41 | 2,41 | 2,41 | 4,06 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,34 | 4,34 | 4,34 | 4,34 | 4,34 |
| 🟢 100 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,37 | 7,37 | 7,37 | 7,37 | 7,37 |
| 🟢 101 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,54 | 5,54 | 5,54 | 5,54 | 5,54 |
| 🟢 102 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,84 | 8,84 | 8,84 | 8,84 | 8,84 |
| 🟢 103 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,17 | 2,17 | 2,17 | 2,17 | 3,26 |
| 🟢 104 | 1,49 | 1,49 | 1,49 | 1,49 | 1,49 | 9,89 | 9,89 | 9,89 | 9,89 | 9,95 |
| 🟢 105 | 1,98 | 1,98 | 2,06 | 2,06 | 2,06 | 12,42 | 12,42 | 12,42 | 12,42 | 12,75 |
| 🟢 106 | 1,98 | 1,98 | 2,06 | 2,06 | 2,06 | 12,42 | 12,42 | 12,42 | 12,42 | 12,75 |
| 🟢 107 | 1,98 | 1,98 | 2,06 | 2,06 | 2,06 | 12,42 | 12,42 | 12,42 | 12,42 | 12,75 |
| 🟢 108 | 0,45 | 0,45 | 0,45 | 0,45 | 0,45 | 4,95 | 4,95 | 4,95 | 4,95 | 9,95 |
| 🟢 109 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,09 | 7,09 | 7,09 | 7,09 | 7,09 |
| 🟢 110 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,09 |
| 🟢 114 | 2,69 | 2,69 | 5,33 | 5,33 | 5,33 | 8,06 | 8,06 | 8,06 | 8,06 | 10,83 |
| 🟢 115 | 2,69 | 2,69 | 5,33 | 5,33 | 5,33 | 8,06 | 8,06 | 8,06 | 8,06 | 10,83 |
| 🟢 116 | 5,34 | 5,34 | 8,00 | 8,00 | 8,00 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 117 | 5,34 | 5,34 | 8,00 | 8,00 | 8,00 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 118 | 5,06 | 5,06 | 7,60 | 7,60 | 7,60 | 10,19 | 10,19 | 10,19 | 10,19 | 10,19 |
| 🟢 119 | 5,06 | 5,06 | 7,60 | 7,60 | 7,60 | 10,19 | 10,19 | 10,19 | 10,19 | 10,19 |
| 🟢 120 | 5,34 | 5,34 | 8,00 | 8,00 | 8,00 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 121 | 5,34 | 5,34 | 8,00 | 8,00 | 8,00 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 122 | 0,94 | 0,94 | 1,87 | 1,87 | 1,87 | 2,82 | 2,82 | 2,82 | 2,82 | 3,79 |
| 🟢 123 | 0,94 | 0,94 | 1,87 | 1,87 | 1,87 | 2,82 | 2,82 | 2,82 | 2,82 | 3,79 |
| 🟢 124 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,10 | 5,10 | 5,10 | 5,10 | 5,10 |
| 🟢 125 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 128 | 4,91 | 4,91 | 4,91 | 4,91 | 4,91 | 7,00 | 7,00 | 7,00 | 7,00 | 7,00 |
| 🟢 129 | 4,07 | 4,07 | 4,07 | 4,07 | 4,07 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 |
| 🟢 130 | 4,57 | 4,57 | 4,57 | 4,57 | 4,57 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 |
| 🟢 131 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 12,15 | 12,15 | 12,15 | 12,15 | 12,15 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 13,65 | 13,65 | 13,65 | 13,65 | 13,65 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 12,15 | 12,15 | 12,15 | 12,15 | 12,15 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 13,65 | 13,65 | 13,65 | 13,65 | 13,65 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 7,00 |
| 🟢 141 | 2,04 | 2,04 | 2,04 | 2,04 | 2,04 | 2,04 | 2,04 | 2,04 | 2,04 | 5,80 |
| 🟢 142 | 2,29 | 2,29 | 2,29 | 2,29 | 2,29 | 2,29 | 2,29 | 2,29 | 2,29 | 6,52 |
| 🟢 143 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,78 | 4,78 | 4,78 | 4,78 | 4,78 |
| 🟢 144 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,78 | 4,78 | 4,78 | 4,78 | 4,78 |
| 🟢 148 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,09 | 4,09 | 4,09 | 4,09 | 4,09 |
| 🟢 149 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,85 | 8,85 | 8,85 | 8,85 | 8,85 |
| 🟢 150 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,85 | 8,85 | 8,85 | 8,85 | 8,85 |
| 🟢 151 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 152 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,05 | 2,05 | 2,05 | 2,05 | 3,07 |
| 🟢 153 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,19 | 7,19 | 7,19 | 7,19 | 7,19 |
| 🟢 154 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,03 |
| 🟢 155 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 18,30 |
| 🟢 156 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,60 | 3,60 | 3,60 | 3,60 | 3,60 |
| 🟢 157 | 0,00 | 0,00 | 0,00 | 3,24 | 3,24 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 |
| 🟢 158 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,18 | 5,18 | 5,18 | 5,18 | 7,63 |
| 🟢 159 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,64 |
| 🟢 160 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,94 | 5,94 | 5,94 | 5,94 | 8,81 |
| 🟢 161 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 162 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,59 | 2,59 | 2,59 | 2,59 | 5,73 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,70 | 3,70 | 3,70 | 3,70 | 3,70 |
| 🟢 165 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 |
| 🟢 166 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 |
| 🟢 167 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 |
| 🟢 168 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,85 | 1,85 | 1,85 | 1,85 | 2,78 |
| 🟡 169 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,20 | 4,20 | 4,20 | 4,20 | 4,20 |
| 🟢 170 | 4,26 | 4,26 | 4,26 | 4,26 | 4,26 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 |
| 🟢 171 | 7,47 | 7,47 | 7,47 | 7,47 | 7,47 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 172 | 7,47 | 7,47 | 7,47 | 7,47 | 7,47 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 173 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,81 | 9,81 | 9,81 | 9,81 | 9,81 |
| 🟢 174 | 1,61 | 1,61 | 1,61 | 1,61 | 1,61 | 1,61 | 1,61 | 1,61 | 1,61 | 2,56 |
| 🟢 175 | 0,00 | 0,00 | 3,63 | 3,63 | 3,63 | 3,63 | 3,63 | 3,63 | 3,63 | 3,63 |
| 🟢 176 | 0,00 | 0,00 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 |
| 🟢 177 | 0,00 | 0,00 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 |
| 🟢 178 | 0,00 | 0,00 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 |
| 🟡 179 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟡 180 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 |
| 🟡 181 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟡 182 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟢 183 | 3,70 | 3,70 | 3,70 | 3,70 | 3,70 | 4,44 | 4,44 | 4,44 | 4,44 | 5,22 |
| 🟢 184 | 7,30 | 7,30 | 7,30 | 7,30 | 7,30 | 7,66 | 7,66 | 7,66 | 7,66 | 8,74 |
| 🟢 185 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 |
| 🟢 186 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 | 9,05 |
| 🟢 187 | 1,85 | 1,85 | 1,85 | 1,85 | 1,85 | 1,85 | 1,85 | 1,85 | 1,85 | 2,61 |
| 🟡 188 | 3,85 | 3,85 | 3,85 | 3,85 | 3,85 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟡 189 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟢 190 | 0,66 | 0,66 | 0,66 | 0,66 | 0,66 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟢 191 | 1,45 | 1,45 | 1,45 | 1,45 | 1,45 | 6,27 | 6,27 | 6,27 | 6,27 | 6,27 |
| 🟢 192 | 1,45 | 1,45 | 1,45 | 1,45 | 1,45 | 6,27 | 6,27 | 6,27 | 6,27 | 6,27 |
| 🟢 193 | 1,45 | 1,45 | 1,45 | 1,45 | 1,45 | 6,27 | 6,27 | 6,27 | 6,27 | 6,27 |
| 🟢 194 | 0,11 | 0,11 | 0,11 | 0,11 | 0,11 | 2,05 | 2,05 | 2,05 | 2,05 | 2,05 |
| 🟢 195 | 0,00 | 0,00 | 0,00 | 1,77 | 1,77 | 12,53 | 12,53 | 12,53 | 12,53 | 13,41 |
| 🟢 196 | 0,00 | 0,00 | 0,00 | 4,96 | 4,96 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 |
| 🟢 197 | 0,00 | 0,00 | 0,00 | 4,96 | 4,96 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 |
| 🟢 198 | 0,00 | 0,00 | 0,00 | 4,96 | 4,96 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 |
| 🟢 199 | 0,00 | 0,00 | 0,00 | 1,01 | 1,01 | 7,18 | 7,18 | 7,18 | 7,18 | 7,81 |
| 🟢 200 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,50 | 3,50 | 3,50 |
| 🟢 201 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,62 | 5,62 | 5,62 |
| 🟢 202 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,54 | 8,54 | 8,54 |
| 🟢 203 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,62 | 5,62 | 5,62 |
| 🟢 204 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,68 | 1,68 | 1,68 |
| 🟢 205 | 4,93 | 4,93 | 4,93 | 4,93 | 4,93 | 11,02 | 11,02 | 11,02 | 11,02 | 11,02 |
| 🟢 206 | 4,35 | 4,35 | 4,35 | 4,35 | 4,35 | 8,39 | 8,39 | 8,39 | 8,39 | 8,39 |
| 🟢 207 | 11,38 | 11,38 | 11,38 | 11,38 | 11,38 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 | 5,02 |
| 🟢 209 | 21,68 | 21,68 | 21,68 | 21,68 | 21,68 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |
| 🟢 211 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 |
| 🟢 212 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 7,72 | 7,72 | 7,72 | 7,72 | 8,81 |
| 🟢 213 | 2,65 | 2,65 | 2,65 | 2,65 | 2,65 | 8,39 | 8,39 | 8,39 | 8,39 | 8,39 |
| 🟢 214 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,17 | 6,17 | 6,17 | 6,17 | 6,17 |
| 🟢 215 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 |
| 🟢 216 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,87 |
| 🟢 217 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 |
| 🟢 218 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,56 | 1,56 | 1,56 | 1,56 | 6,12 |
| 🟡 219 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,90 | 2,90 | 2,90 | 2,90 | 2,90 |
| 🟢 220 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,16 | 3,16 | 3,16 | 3,16 | 3,22 |
| 🟢 221 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,92 | 3,92 | 3,92 | 3,92 | 3,96 |
| 🟢 222 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,74 | 4,74 | 4,74 | 4,74 | 4,60 |
| 🟢 223 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,58 | 1,58 | 1,58 | 1,58 | 2,42 |
| 🟡 224 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟡 225 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟡 226 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟡 227 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 228 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 22,32 | 22,32 | 22,32 | 22,32 | 35,74 |
| 🟢 229 | 44,15 | 44,15 | 44,15 | 44,15 | 44,15 | 55,11 | 55,11 | 55,11 | 55,11 | 55,11 |
| 🟢 230 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 | 23,80 |
| 🟢 231 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 | 84,72 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 0,00 | 0,00 | 2,17 | 2,17 | 2,17 | 2,17 | 2,17 | 2,17 | 2,17 | 5,85 |
| 🟢 234 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 |
| 🟢 235 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 |
| 🟢 236 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 |
| 🟢 237 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 14,21 |
| 🟢 238 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 | 21,95 |
| 🟢 239 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 18,85 |
| 🟢 240 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 | 30,35 |
| 🟡 241 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 242 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,17 | 4,17 | 4,17 |
| 🟢 243 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,12 | 5,12 | 5,12 |
| 🟢 244 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,12 | 5,12 | 5,12 |
| 🟢 245 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,58 | 6,58 | 6,58 |
| 🟢 246 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,09 | 2,09 | 3,13 |
| 🟡 247 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟢 248 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,29 | 4,29 | 4,29 | 4,29 | 5,32 |
| 🟢 249 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 9,90 |
| 🟢 250 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 9,90 |
| 🟢 251 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 252 | 1,01 | 1,01 | 1,01 | 1,01 | 1,01 | 1,07 | 1,07 | 1,07 | 1,07 | 2,66 |
| 🟢 253 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 |
| 🟢 254 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,93 | 11,93 | 11,93 | 11,93 | 11,93 |
| 🟢 255 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,69 | 13,69 | 13,69 | 13,69 | 13,69 |
| 🟢 256 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,45 | 14,45 | 14,45 | 14,45 | 14,45 |
| 🟢 257 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,99 | 3,99 | 3,99 | 3,99 | 5,98 |
| 🟢 258 | 4,87 | 4,87 | 4,87 | 4,87 | 4,87 | 8,35 | 8,35 | 8,35 | 8,35 | 14,69 |
| 🟢 259 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 260 | 8,81 | 8,81 | 8,81 | 8,81 | 8,81 | 8,81 | 8,81 | 8,81 | 8,81 | 19,49 |
| 🟢 261 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 262 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,11 | 2,11 | 2,11 | 2,11 | 2,43 |
| 🟢 263 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,24 | 5,24 | 5,24 | 5,24 | 5,24 |
| 🟢 264 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,45 | 5,45 | 5,45 | 5,45 | 5,45 |
| 🟢 265 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟢 266 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,68 | 0,68 | 0,68 | 0,68 | 0,78 |
| 🟢 267 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,33 | 5,33 | 5,33 | 5,33 | 5,33 |
| 🟢 268 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 |
| 🟢 269 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 |
| 🟢 270 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,66 | 2,66 | 2,66 | 2,66 | 4,00 |
| 🟡 271 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 272 | 0,63 | 0,63 | 0,89 | 0,89 | 0,89 | 2,96 | 2,96 | 2,96 | 2,96 | 4,52 |
| 🟢 273 | 0,76 | 0,76 | 1,07 | 1,07 | 1,07 | 3,55 | 3,55 | 3,55 | 3,55 | 5,42 |
| 🟢 274 | 0,69 | 0,69 | 0,98 | 0,98 | 0,98 | 3,26 | 3,26 | 3,26 | 3,26 | 4,97 |
| 🟢 275 | 0,79 | 0,79 | 1,11 | 1,11 | 1,11 | 3,70 | 3,70 | 3,70 | 3,70 | 5,65 |
| 🟢 276 | 0,32 | 0,32 | 0,32 | 0,32 | 0,32 | 0,32 | 0,32 | 0,32 | 0,32 | 2,26 |
| 🟡 277 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,99 |
| 🟢 278 | 0,00 | 0,00 | 0,52 | 0,52 | 0,52 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟢 279 | 0,00 | 0,00 | 0,92 | 0,92 | 0,92 | 9,02 | 9,02 | 9,02 | 9,02 | 9,02 |
| 🟢 280 | 0,00 | 0,00 | 0,52 | 0,52 | 0,52 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟢 281 | 0,00 | 0,00 | 1,00 | 1,00 | 1,00 | 12,71 | 12,71 | 12,71 | 12,71 | 12,71 |
| 🟢 282 | 0,00 | 0,00 | 0,26 | 0,26 | 0,26 | 2,35 | 2,35 | 2,35 | 2,35 | 3,53 |
| 🟢 283 | 1,74 | 1,74 | 2,62 | 2,62 | 2,62 | 3,99 | 3,99 | 3,99 | 3,99 | 5,07 |
| 🟢 284 | 3,78 | 3,78 | 4,43 | 4,43 | 4,43 | 5,24 | 5,24 | 5,24 | 5,24 | 5,24 |
| 🟢 285 | 3,06 | 3,06 | 3,78 | 3,78 | 3,78 | 4,36 | 4,36 | 4,36 | 4,36 | 4,36 |
| 🟢 286 | 4,39 | 4,39 | 5,03 | 5,03 | 5,03 | 5,68 | 5,68 | 5,68 | 5,68 | 5,68 |
| 🟢 287 | 0,88 | 0,88 | 0,88 | 0,88 | 0,88 | 0,88 | 0,88 | 0,88 | 0,88 | 2,53 |
| 🟢 288 | 1,66 | 1,66 | 1,95 | 1,95 | 1,95 | 3,84 | 3,84 | 3,84 | 3,84 | 5,64 |
| 🟢 289 | 2,24 | 2,24 | 2,58 | 2,58 | 2,58 | 5,16 | 5,16 | 5,16 | 5,16 | 7,65 |
| 🟢 290 | 1,93 | 1,93 | 2,20 | 2,20 | 2,20 | 4,40 | 4,40 | 4,40 | 4,40 | 6,50 |
| 🟢 291 | 2,65 | 2,65 | 3,05 | 3,05 | 3,05 | 6,12 | 6,12 | 6,12 | 6,12 | 9,03 |
| 🟢 292 | 0,83 | 0,83 | 0,83 | 0,83 | 0,83 | 0,83 | 0,83 | 0,83 | 0,83 | 2,82 |
| 🟡 293 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 294 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,29 |
| 🟢 295 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,91 |
| 🟢 296 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,29 |
| 🟢 297 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,91 |
| 🟢 298 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,47 |
| 🟢 299 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,48 | 3,48 | 3,48 | 3,48 | 3,48 |
| 🟢 300 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 |
| 🟢 301 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,48 | 3,48 | 3,48 | 3,48 | 3,48 |
| 🟢 302 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 |
| 🟢 303 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,74 | 1,74 | 1,74 | 1,74 | 2,61 |
| 🟡 304 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 305 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,58 |
| 🟢 306 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,63 |
| 🟢 307 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,63 |
| 🟢 308 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 309 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,79 |
| 🟡 310 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 311 | 2,45 | 2,45 | 2,45 | 2,45 | 2,45 | 3,40 | 3,40 | 3,40 | 3,40 | 3,40 |
| 🟢 312 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 6,57 |
| 🟢 313 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 4,75 | 6,57 |
| 🟢 314 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟡 315 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 318 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,22 | 2,22 | 2,22 | 2,22 | 9,09 |
| 🟢 319 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,86 | 5,86 | 5,86 | 5,86 | 10,66 |
| 🟢 320 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,86 | 5,86 | 5,86 | 5,86 | 10,66 |
| 🟢 321 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,84 | 9,84 | 9,84 | 9,84 | 11,31 |
| 🟢 322 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,63 | 5,63 | 5,63 | 5,63 | 5,63 |
| 🟢 323 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 324 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 325 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟡 326 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 |
| 🟢 327 | 1,18 | 1,18 | 1,62 | 1,62 | 1,62 | 2,68 | 2,68 | 2,68 | 2,68 | 4,14 |
| 🟢 328 | 2,42 | 2,42 | 2,73 | 2,73 | 2,73 | 3,04 | 3,04 | 3,04 | 3,04 | 3,04 |
| 🟢 329 | 1,97 | 1,97 | 2,37 | 2,37 | 2,37 | 2,77 | 2,77 | 2,77 | 2,77 | 2,77 |
| 🟢 330 | 2,42 | 2,42 | 2,73 | 2,73 | 2,73 | 3,04 | 3,04 | 3,04 | 3,04 | 3,04 |
| 🟢 331 | 0,59 | 0,59 | 0,59 | 0,59 | 0,59 | 0,59 | 0,59 | 0,59 | 0,59 | 2,07 |
| 🟢 332 | 1,01 | 1,01 | 1,30 | 1,30 | 1,30 | 2,44 | 2,44 | 2,44 | 2,44 | 4,16 |
| 🟢 333 | 1,21 | 1,21 | 1,55 | 1,55 | 1,55 | 2,93 | 2,93 | 2,93 | 2,93 | 4,99 |
| 🟢 334 | 1,21 | 1,21 | 1,55 | 1,55 | 1,55 | 2,93 | 2,93 | 2,93 | 2,93 | 4,99 |
| 🟢 335 | 1,26 | 1,26 | 1,62 | 1,62 | 1,62 | 3,05 | 3,05 | 3,05 | 3,05 | 5,20 |
| 🟢 336 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 0,50 | 2,08 |
| 🟢 337 | 0,00 | 0,00 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 |
| 🟢 338 | 0,00 | 0,00 | 7,78 | 7,78 | 7,78 | 7,78 | 7,78 | 7,78 | 7,78 | 7,78 |
| 🟢 339 | 0,00 | 0,00 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 | 5,05 |
| 🟢 340 | 0,00 | 0,00 | 12,59 | 12,59 | 12,59 | 12,59 | 12,59 | 12,59 | 12,59 | 12,59 |
| 🟢 341 | 0,00 | 0,00 | 2,53 | 2,53 | 2,53 | 2,53 | 2,53 | 2,53 | 2,53 | 3,79 |
| 🟢 342 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,60 | 3,60 | 3,60 | 3,60 | 3,92 |
| 🟢 343 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,57 | 5,57 | 5,57 | 5,57 | 5,57 |
| 🟢 344 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,60 | 3,60 | 3,60 | 3,60 | 3,92 |
| 🟢 345 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 346 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,80 | 1,80 | 1,80 | 1,80 | 2,35 |
| 🟢 347 | 0,00 | 0,00 | 0,00 | 0,88 | 5,53 | 5,53 | 6,71 | 6,71 | 6,71 | 8,84 |
| 🟢 348 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,66 | 9,66 | 9,66 | 9,66 | 9,66 |
| 🟢 349 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,66 | 9,66 | 9,66 | 9,66 | 9,66 |
| 🟢 350 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 351 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,30 | 3,30 | 3,30 | 3,30 | 4,81 |
| 🟢 352 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,98 | 0,98 | 0,98 | 0,98 | 1,93 |
| 🟢 353 | 2,56 | 2,56 | 2,56 | 2,56 | 2,56 | 6,41 | 6,41 | 6,41 | 6,41 | 6,41 |
| 🟢 354 | 5,58 | 5,58 | 5,58 | 5,58 | 5,58 | 9,43 | 9,43 | 9,43 | 9,43 | 9,43 |
| 🟢 355 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 1,41 | 1,41 | 1,41 | 1,41 | 1,41 |
| 🟢 356 | 7,09 | 7,09 | 7,09 | 7,09 | 7,09 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 |
| 🟢 357 | 0,76 | 0,76 | 0,76 | 0,76 | 0,76 | 1,93 | 1,93 | 1,93 | 1,93 | 1,93 |
| 🟢 358 | 3,87 | 3,87 | 3,87 | 3,87 | 3,87 | 6,11 | 6,11 | 6,11 | 6,11 | 7,44 |
| 🟢 359 | 8,04 | 8,04 | 8,04 | 8,04 | 8,04 | 8,04 | 8,04 | 8,04 | 8,04 | 10,84 |
| 🟢 360 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 10,75 |
| 🟢 361 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 |
| 🟢 362 | 1,54 | 1,54 | 1,54 | 1,54 | 1,54 | 3,66 | 3,66 | 3,66 | 3,66 | 5,95 |
| 🟡 363 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟡 364 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟡 365 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,85 | 7,85 | 7,85 | 7,85 | 7,85 |
| 🟡 366 | 2,82 | 2,82 | 2,93 | 2,93 | 2,93 | 3,14 | 3,14 | 3,14 | 3,14 | 7,03 |
| 🟡 367 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,85 | 4,85 | 4,85 | 4,85 | 4,85 |
| 🟢 368 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟢 369 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,81 | 5,81 | 5,81 | 5,81 | 5,81 |
| 🟢 370 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,81 | 5,81 | 5,81 | 5,81 | 5,81 |
| 🟢 371 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,34 | 6,34 | 6,34 | 6,34 | 7,10 |
| 🟢 372 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,61 | 7,61 | 7,61 | 7,61 | 8,52 |
| 🟢 373 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,34 | 6,34 | 6,34 | 6,34 | 7,10 |
| 🟢 374 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,88 | 8,88 | 8,88 | 8,88 | 9,94 |
| 🟢 375 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,18 | 3,18 | 3,18 | 3,18 | 5,32 |
| 🟢 376 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,76 | 2,76 | 2,76 | 2,76 | 3,22 |
| 🟢 377 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,56 | 6,56 | 6,56 | 6,56 | 7,84 |
| 🟢 378 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,54 | 12,54 | 12,54 | 12,54 | 14,33 |
| 🟢 379 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,09 | 2,09 | 2,09 | 2,09 | 2,42 |
| 🟡 380 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 381 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,40 | 6,40 | 6,40 | 6,40 | 6,40 |
| 🟢 382 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 |
| 🟢 383 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 |
| 🟢 384 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 |
| 🟢 385 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,09 | 5,09 | 5,09 | 5,09 | 5,09 |
| 🟢 386 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,87 | 4,87 | 4,87 | 4,87 | 4,87 |
| 🟢 387 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 |
| 🟢 388 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 |
| 🟢 389 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 390 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,67 | 10,67 | 10,67 | 10,67 | 10,67 |
| 🟢 391 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 392 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,69 | 7,69 | 7,69 | 7,69 | 7,69 |
| 🟢 393 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,36 | 6,36 | 6,36 | 6,36 | 6,36 |
| 🟢 394 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,25 | 7,25 | 7,25 | 7,25 | 7,25 |
| 🟢 395 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 396 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 |
| 🟢 397 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 398 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,67 | 10,67 | 10,67 | 10,67 | 10,67 |
| 🟢 399 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 400 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,69 | 7,69 | 7,69 | 7,69 | 7,69 |
| 🟢 401 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,62 | 7,62 | 7,62 | 7,62 | 7,62 |
| 🟢 402 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 403 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 |
| 🟢 404 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 405 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,67 | 10,67 | 10,67 | 10,67 | 10,67 |
| 🟢 406 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 407 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,69 | 7,69 | 7,69 | 7,69 | 7,69 |
| 🟢 408 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,07 | 7,07 | 7,07 | 7,07 | 7,07 |
| 🟢 409 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,70 | 9,70 | 9,70 | 9,70 | 9,70 |
| 🟢 410 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,18 | 2,18 | 2,18 | 2,18 | 2,18 |
| 🟢 411 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,98 | 1,98 | 1,98 | 1,98 | 1,98 |
| 🟢 412 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,98 | 1,98 | 1,98 | 1,98 | 1,98 |
| 🟢 413 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,74 | 1,74 | 1,74 | 1,74 | 1,74 |
| 🟢 414 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 2,55 | 3,82 |
| 🟢 415 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,98 | 1,98 | 1,98 | 1,98 | 1,98 |
| 🟢 416 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,34 | 2,34 | 2,34 | 2,34 | 2,34 |
| 🟢 417 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,94 | 2,94 | 2,94 | 2,94 | 2,94 |
| 🟢 418 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,94 | 2,94 | 2,94 | 2,94 | 2,94 |
| 🟢 419 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 420 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,99 | 0,99 | 0,99 | 0,99 | 0,99 |
| 🟢 421 | 1,67 | 1,67 | 2,88 | 2,88 | 2,88 | 4,08 | 4,08 | 4,08 | 4,08 | 5,04 |
| 🟢 422 | 2,01 | 2,01 | 3,45 | 3,45 | 3,45 | 4,90 | 4,90 | 4,90 | 4,90 | 6,05 |
| 🟢 423 | 1,84 | 1,84 | 3,17 | 3,17 | 3,17 | 4,49 | 4,49 | 4,49 | 4,49 | 5,55 |
| 🟢 424 | 2,09 | 2,09 | 3,60 | 3,60 | 3,60 | 5,10 | 5,10 | 5,10 | 5,10 | 6,30 |
| 🟢 425 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 0,84 | 2,52 |
| 🟢 426 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,78 | 3,78 | 3,78 | 3,78 | 3,78 |
| 🟢 427 | 0,00 | 0,00 | 0,00 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 |
| 🟢 428 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,78 | 3,78 | 3,78 | 3,78 | 3,78 |
| 🟢 429 | 0,00 | 0,00 | 0,00 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 |
| 🟢 430 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,89 | 1,89 | 1,89 | 1,89 | 1,89 |
| 🟢 431 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,45 | 5,45 | 5,45 | 5,45 | 5,45 |
| 🟢 432 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,97 | 5,97 | 5,97 | 5,97 | 5,97 |
| 🟢 433 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,97 | 5,97 | 5,97 | 5,97 | 5,97 |
| 🟢 434 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,16 | 7,16 | 7,16 | 7,16 | 7,16 |
| 🟢 435 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,73 | 2,73 | 2,73 | 2,73 | 4,09 |
| 🟢 436 | 2,63 | 2,63 | 2,63 | 2,63 | 2,63 | 3,25 | 3,25 | 3,25 | 3,25 | 3,25 |
| 🟢 437 | 1,31 | 1,31 | 1,31 | 1,31 | 1,31 | 1,62 | 1,62 | 1,62 | 1,62 | 2,44 |
| 🟢 438 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,03 | 4,03 | 4,03 | 4,03 | 4,03 |
| 🟢 439 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,03 | 2,03 | 2,03 | 2,03 | 3,03 |
| 🟢 440 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,12 | 4,12 | 4,12 | 4,12 | 4,12 |
| 🟢 441 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 |
| 🟢 442 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 |
| 🟢 443 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,45 | 8,45 | 8,45 | 8,45 | 8,45 |
| 🟢 444 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,06 | 2,06 | 2,06 | 2,06 | 2,06 |
| 🟢 445 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 |
| 🟢 446 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 447 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,75 | 3,75 | 3,75 | 3,75 | 3,75 |
| 🟢 448 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,40 | 14,40 | 14,40 | 14,40 | 14,40 |
| 🟢 449 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,61 | 1,61 | 1,61 | 1,61 | 2,42 |
| 🟢 450 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,05 |
| 🟢 451 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,54 |
| 🟢 452 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,01 | 3,01 | 3,01 | 3,01 | 4,12 |
| 🟢 453 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,35 | 4,35 | 4,35 | 4,35 | 5,60 |
| 🟢 454 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 455 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,51 | 1,51 | 1,51 | 1,51 | 3,09 |
| 🟢 456 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,48 | 2,48 | 2,48 | 2,48 | 3,93 |
| 🟢 457 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,67 | 3,67 | 3,67 | 3,67 | 3,67 |
| 🟢 458 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,49 | 5,49 | 5,49 | 5,49 | 5,49 |
| 🟢 459 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,49 | 5,49 | 5,49 | 5,49 | 5,49 |
| 🟢 460 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,49 | 5,49 | 5,49 | 5,49 | 5,49 |
| 🟢 461 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,10 | 1,10 | 1,10 | 1,10 | 1,10 |
| 🟡 462 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 463 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,87 | 4,87 | 4,87 | 4,87 | 4,87 |
| 🟢 464 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 465 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,12 | 10,12 | 10,12 | 10,12 | 10,12 |
| 🟢 466 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 467 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,41 | 1,41 | 1,41 | 1,41 | 4,87 |
| 🟢 468 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,63 | 8,63 | 8,63 | 8,63 | 8,63 |
| 🟢 469 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 470 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 |
| 🟢 471 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 472 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,80 | 7,80 | 7,80 | 7,80 | 10,01 |
| 🟢 473 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,53 | 9,53 | 9,53 | 9,53 | 9,53 |
| 🟢 474 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,80 | 7,80 | 7,80 | 7,80 | 10,01 |
| 🟢 475 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,53 | 9,53 | 9,53 | 9,53 | 9,53 |
| 🟢 476 | 0,00 | 0,00 | 8,77 | 8,77 | 8,77 | 10,54 | 10,54 | 10,54 | 10,54 | 16,56 |
| 🟢 477 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,54 | 10,54 | 10,54 | 10,54 | 16,56 |
| 🟢 478 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,54 | 10,54 | 10,54 | 10,54 | 16,56 |
| 🟢 479 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 480 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 |
| 🟢 481 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,79 | 8,79 | 8,79 | 8,79 | 11,68 |
| 🟢 482 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 |
| 🟢 483 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 12,63 |
| 🟢 484 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,53 | 2,53 | 2,53 | 2,53 | 7,81 |
| 🟢 485 | 1,59 | 1,59 | 1,80 | 1,80 | 1,80 | 8,05 | 8,05 | 8,05 | 8,05 | 10,23 |
| 🟢 486 | 2,25 | 2,25 | 3,87 | 3,87 | 3,87 | 11,83 | 11,83 | 11,83 | 11,83 | 11,83 |
| 🟢 487 | 2,25 | 2,25 | 3,87 | 3,87 | 3,87 | 11,83 | 11,83 | 11,83 | 11,83 | 11,83 |
| 🟢 488 | 2,25 | 2,25 | 3,87 | 3,87 | 3,87 | 11,83 | 11,83 | 11,83 | 11,83 | 11,83 |
| 🟢 489 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,29 | 2,29 | 2,29 | 2,29 | 2,82 |
| 🟢 490 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,15 | 8,15 | 8,15 | 8,15 | 8,15 |
| 🟢 491 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,99 | 8,99 | 8,99 | 8,99 | 8,99 |
| 🟢 492 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,13 | 10,13 | 10,13 | 10,13 | 10,13 |
| 🟢 493 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,15 | 1,15 | 1,15 | 1,15 | 2,12 |
| 🟢 494 | 2,26 | 2,26 | 2,44 | 2,44 | 2,44 | 8,46 | 8,46 | 8,46 | 8,46 | 9,00 |
| 🟢 495 | 4,00 | 4,00 | 4,39 | 4,39 | 4,39 | 12,79 | 12,79 | 12,79 | 12,79 | 12,79 |
| 🟡 496 | 5,85 | 5,85 | 5,85 | 5,85 | 5,85 | 7,90 | 7,90 | 7,90 | 7,90 | 7,90 |
| 🟢 497 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,96 | 9,96 | 9,96 | 9,96 | 10,18 |
| 🟢 498 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,98 | 4,98 | 4,98 | 4,98 | 7,64 |
| 🟢 499 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,68 |
| 🟢 500 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,85 |
| 🟢 501 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 502 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 503 | 5,77 | 5,77 | 5,77 | 5,77 | 5,77 | 6,51 | 6,51 | 6,51 | 6,51 | 7,45 |
| 🟢 504 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟢 508 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,10 | 11,10 | 11,10 | 11,10 | 11,10 |
| 🟢 509 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,10 | 11,10 | 11,10 | 11,10 | 11,10 |
| 🟢 510 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,10 | 11,10 | 11,10 | 11,10 | 11,10 |
| 🟢 511 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,44 | 2,44 | 2,44 | 2,44 | 2,44 |
| 🟢 512 | 2,85 | 2,85 | 2,85 | 2,85 | 2,85 | 5,92 | 5,92 | 5,92 | 5,92 | 8,50 |
| 🟢 513 | 5,16 | 5,16 | 5,16 | 5,16 | 5,16 | 7,63 | 7,63 | 7,63 | 7,63 | 10,60 |
| 🟢 514 | 7,59 | 7,59 | 7,59 | 7,59 | 7,59 | 8,00 | 8,00 | 8,00 | 8,00 | 10,25 |
| 🟢 515 | 7,05 | 7,05 | 7,05 | 7,05 | 7,05 | 11,16 | 11,16 | 11,16 | 11,16 | 12,13 |
| 🟡 516 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,10 | 5,10 | 5,10 | 5,10 | 5,10 |
| 🟢 517 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,56 | 4,56 | 4,56 | 4,56 | 5,73 |
| 🟢 518 | 0,00 | 0,00 | 0,00 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 |
| 🟢 519 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,56 | 4,56 | 4,56 | 4,56 | 5,73 |
| 🟢 520 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 521 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,29 | 2,29 | 2,29 | 2,29 | 4,30 |
| 🟢 522 | 1,92 | 1,92 | 1,92 | 1,92 | 1,92 | 5,27 | 5,27 | 5,27 | 5,27 | 11,43 |
| 🟢 523 | 1,56 | 1,56 | 1,56 | 1,56 | 1,56 | 3,21 | 3,21 | 3,21 | 3,21 | 5,83 |
| 🟢 524 | 5,08 | 5,08 | 5,08 | 5,08 | 5,08 | 5,84 | 5,84 | 5,84 | 5,84 | 5,84 |
| 🟢 525 | 5,77 | 5,77 | 5,77 | 5,77 | 5,77 | 6,63 | 6,63 | 6,63 | 6,63 | 7,61 |
| 🟢 526 | 5,77 | 5,77 | 5,77 | 5,77 | 5,77 | 7,61 | 7,61 | 7,61 | 7,61 | 7,61 |
| 🟢 527 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 |
| 🟢 528 | 0,00 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,49 | 9,54 |
| 🟢 529 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,63 | 12,63 | 12,63 | 12,63 | 12,73 |
| 🟢 530 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,63 | 12,63 | 12,63 | 12,63 | 12,73 |
| 🟢 531 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,17 | 12,17 | 12,17 | 12,17 | 12,36 |
| 🟢 532 | 0,00 | 0,00 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 9,54 |
| 🟢 533 | 0,00 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,49 | 9,54 |
| 🟢 534 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,63 | 12,63 | 12,63 | 12,63 | 12,73 |
| 🟢 535 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,63 | 12,63 | 12,63 | 12,63 | 12,73 |
| 🟢 536 | 0,00 | 0,00 | 2,55 | 2,55 | 2,55 | 12,17 | 12,17 | 12,17 | 12,17 | 12,36 |
| 🟢 537 | 0,00 | 0,00 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 5,51 | 9,54 |
| 🟡 538 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 539 | 6,70 | 6,70 | 6,70 | 6,70 | 6,70 | 7,92 | 7,92 | 7,92 | 7,92 | 9,13 |
| 🟢 540 | 6,09 | 6,09 | 6,09 | 6,09 | 6,09 | 7,69 | 7,69 | 7,69 | 7,69 | 8,35 |
| 🟢 541 | 8,66 | 8,66 | 8,66 | 8,66 | 8,66 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 542 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 16,31 | 16,31 | 16,31 | 16,31 | 16,31 |
| 🟢 543 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 | 9,34 |
| 🟢 544 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 | 7,86 |
| 🟢 545 | 13,25 | 13,25 | 13,25 | 13,25 | 13,25 | 25,60 | 25,60 | 25,60 | 25,60 | 25,60 |
| 🟢 546 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 24,19 | 24,19 | 24,19 | 24,19 | 24,19 |
| 🟢 547 | 1,23 | 1,23 | 1,23 | 1,23 | 1,23 | 3,54 | 3,54 | 3,54 | 3,54 | 3,91 |
| 🟢 548 | 2,30 | 2,30 | 2,30 | 2,30 | 2,30 | 2,90 | 2,90 | 2,90 | 2,90 | 3,15 |
| 🟢 549 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,14 | 6,14 | 6,14 | 6,14 | 6,14 |
| 🟢 550 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 |
| 🟢 551 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 |
| 🟢 552 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 |
| 🟢 553 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,07 | 3,07 | 3,07 | 3,07 | 3,07 |
| 🟢 554 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,75 | 5,75 | 5,75 | 5,75 | 8,26 |
| 🟢 555 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,88 | 2,88 | 2,88 | 2,88 | 6,20 |
| 🟢 556 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,84 | 3,84 | 3,84 | 3,84 | 3,84 |
| 🟢 557 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 11,45 |
| 🟢 558 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 12,58 |
| 🟢 559 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 13,73 |
| 🟢 560 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 13,73 |
| 🟢 561 | 2,58 | 2,58 | 2,58 | 2,58 | 2,58 | 2,58 | 2,58 | 2,58 | 2,58 | 11,45 |
| 🟢 562 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟢 563 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 566 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟢 567 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 5,25 | 5,25 | 5,25 | 5,25 | 5,25 | 9,68 | 9,68 | 9,68 | 9,68 | 9,68 |
| 🟢 572 | 7,79 | 7,79 | 7,79 | 7,79 | 7,79 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 7,79 | 7,79 | 7,79 | 7,79 | 7,79 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 7,79 | 7,79 | 7,79 | 7,79 | 7,79 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 0,97 | 0,97 | 0,97 | 0,97 | 0,97 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,25 | 10,25 | 10,25 | 10,25 | 11,14 |
| 🟢 577 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,12 | 5,12 | 5,12 | 5,12 | 5,57 |
| 🟢 581 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 6,32 | 6,32 | 6,32 | 6,32 | 6,32 |
| 🟢 582 | 9,68 | 9,68 | 9,68 | 9,68 | 9,68 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 11,37 | 11,37 | 11,37 | 11,37 | 11,37 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 |
| 🟢 586 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 11,62 |
| 🟢 590 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 | 17,96 |
| 🟢 591 | 6,97 | 6,97 | 6,97 | 6,97 | 6,97 | 6,97 | 6,97 | 6,97 | 6,97 | 15,43 |
| 🟢 592 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 | 24,83 |
| 🟡 593 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟡 594 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 595 | 4,33 | 4,33 | 4,33 | 4,33 | 4,33 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 |
| 🟢 596 | 10,13 | 10,13 | 10,13 | 10,13 | 10,13 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 11,52 | 11,52 | 11,52 | 11,52 | 11,52 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 11,86 | 11,86 | 11,86 | 11,86 | 11,86 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 |
| 🟢 600 | 13,79 | 13,79 | 13,79 | 13,79 | 13,79 | 17,71 | 17,71 | 17,71 | 17,71 | 26,45 |
| 🟢 601 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 43,89 | 43,89 | 43,89 | 43,89 | 43,89 |
| 🟢 602 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 | 19,77 |
| 🟢 603 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 | 70,93 |
| 🟢 604 | 6,42 | 6,42 | 6,42 | 6,42 | 6,42 | 12,43 | 12,43 | 12,43 | 12,43 | 12,43 |
| 🟢 605 | 22,76 | 22,76 | 22,76 | 22,76 | 22,76 | 22,76 | 22,76 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 |
| 🟢 608 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 12,43 |
| 🟢 609 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 |
| 🟢 610 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 6,76 | 6,76 | 6,76 | 6,76 | 6,76 |
| 🟢 611 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,27 | 2,27 | 2,27 | 2,27 | 3,40 |
| 🟡 612 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 14,13 |
| 🟡 613 | 4,25 | 4,25 | 4,25 | 4,25 | 4,25 | 7,10 | 7,10 | 7,10 | 7,10 | 7,10 |
| 🟡 614 | 4,10 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 |
| 🟢 615 | 5,76 | 5,76 | 5,76 | 5,76 | 5,76 | 8,64 | 8,64 | 8,64 | 8,64 | 8,64 |
| 🟢 616 | 8,06 | 8,06 | 8,06 | 8,06 | 8,06 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 9,16 | 9,16 | 9,16 | 9,16 | 9,16 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 9,45 | 9,45 | 9,45 | 9,45 | 9,45 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 | 8,54 | 8,54 | 8,54 | 8,54 | 8,54 |
| 🟢 620 | 12,27 | 12,27 | 12,27 | 12,27 | 12,27 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 12,27 | 12,27 | 12,27 | 12,27 | 12,27 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 3,06 | 3,06 | 3,06 | 3,06 | 3,06 | 4,59 | 4,59 | 4,59 | 4,59 | 4,59 |
| 🟢 624 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 8,11 | 8,11 | 8,11 | 8,11 | 8,11 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 8,36 | 8,36 | 8,36 | 8,36 | 8,36 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 |
| 🟢 628 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 629 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 630 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 631 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 |
| 🟢 632 | 1,79 | 1,79 | 1,83 | 1,83 | 1,83 | 5,24 | 5,24 | 5,24 | 5,24 | 5,57 |
| 🟢 633 | 2,19 | 2,19 | 2,43 | 2,43 | 2,43 | 5,33 | 5,33 | 5,33 | 5,33 | 7,61 |
| 🟢 634 | 1,92 | 1,92 | 2,54 | 2,54 | 2,54 | 5,56 | 5,56 | 5,56 | 5,56 | 6,51 |
| 🟢 635 | 2,63 | 2,63 | 3,26 | 3,26 | 3,26 | 6,74 | 6,74 | 6,74 | 6,74 | 7,50 |
| 🟢 636 | 0,89 | 0,89 | 0,92 | 0,92 | 0,92 | 2,62 | 2,62 | 2,62 | 2,62 | 2,78 |
| 🟢 637 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,26 | 4,26 | 4,26 | 4,26 | 4,26 |
| 🟢 638 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 |
| 🟢 639 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 |
| 🟢 640 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 641 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,13 | 2,13 | 2,13 | 2,13 | 3,20 |
| 🟡 642 | 4,80 | 4,80 | 4,80 | 4,80 | 4,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 643 | 3,92 | 3,92 | 3,92 | 3,92 | 3,92 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 644 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 11,62 | 11,62 | 11,62 | 11,62 | 11,62 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 11,62 | 11,62 | 11,62 | 11,62 | 11,62 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 4,85 | 4,85 | 4,85 | 4,85 | 4,85 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 648 | 4,91 | 4,91 | 4,91 | 4,91 | 4,91 | 7,00 | 7,00 | 7,00 | 7,00 | 7,00 |
| 🟢 649 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 14,66 | 14,66 | 14,66 | 14,66 | 14,66 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 2,46 | 7,00 |
| 🟢 653 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 9,81 | 9,81 | 9,81 | 9,81 | 10,92 |
| 🟢 654 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,21 | 16,21 | 16,21 | 16,21 | 17,98 |
| 🟢 655 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,21 | 16,21 | 16,21 | 16,21 | 17,98 |
| 🟢 656 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,21 | 16,21 | 16,21 | 16,21 | 17,98 |
| 🟢 657 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,91 | 4,91 | 4,91 | 4,91 | 10,92 |
| 🟢 658 | 6,60 | 6,60 | 6,60 | 6,60 | 6,60 | 6,60 | 6,60 | 6,60 | 6,60 | 14,51 |
| 🟢 659 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 | 6,52 | 14,35 |
| 🟢 660 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 | 22,43 |
| 🟢 661 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 |
| 🟢 662 | 8,71 | 8,71 | 8,71 | 8,71 | 8,71 | 8,71 | 8,71 | 8,71 | 8,71 | 19,26 |
| 🟢 663 | 8,61 | 8,61 | 8,61 | 8,61 | 8,61 | 8,61 | 8,61 | 8,61 | 8,61 | 19,05 |
| 🟢 664 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 |
| 🟢 665 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 | 30,66 |
| 🟢 666 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 16,54 |
| 🟢 667 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 | 25,57 |
| 🟢 668 | 9,93 | 9,93 | 9,93 | 9,93 | 9,93 | 9,93 | 9,93 | 9,93 | 9,93 | 21,96 |
| 🟢 669 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 | 39,10 |
| 🟢 670 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 14,10 | 14,10 | 14,10 | 14,10 | 16,30 |
| 🟢 671 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,68 | 10,68 | 10,68 | 10,68 | 12,17 |
| 🟢 672 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,48 | 10,48 | 10,48 | 10,48 | 12,11 |
| 🟢 673 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 8,03 | 8,03 | 8,03 | 8,03 | 8,03 | 10,28 | 10,28 | 10,28 | 10,28 | 10,46 |
| 🟢 680 | 11,09 | 11,09 | 11,09 | 11,09 | 11,09 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 | 10,06 |
| 🟢 682 | 17,31 | 17,31 | 17,31 | 17,31 | 17,31 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 3,03 | 3,03 | 3,03 | 3,03 | 3,03 | 4,55 | 4,55 | 4,55 | 4,55 | 4,55 |

<!-- tabela: **Tabela 21** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 2 de 6: 20–24 a 55–60 m³) -->
| Nº | 20–24 | 24–25 | 25–30 | 30–35 | 35–40 | 40–44 | 44–45 | 45–50 | 50–55 | 55–60 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,04 | 18,04 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,86 | 18,99 | 18,99 |
| 🟢 2 | 15,46 | 15,46 | 15,46 | 15,97 | 15,97 | 15,92 | 15,92 | 15,92 | 15,14 | 15,14 |
| 🟢 3 | 18,04 | 18,04 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,86 | 18,99 | 18,99 |
| 🟢 4 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 22,04 | 22,04 | 22,04 | 22,19 | 22,19 | 22,65 | 22,65 | 22,65 | 22,65 | 22,65 |
| 🟢 6 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 28,28 | 28,28 | 28,28 | 28,48 | 28,48 | 29,06 | 29,06 | 29,06 | 29,06 | 29,06 |
| 🟢 9 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 18,04 | 18,04 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,86 | 18,99 | 18,99 |
| 🟢 14 | 18,04 | 18,04 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,86 | 18,99 | 18,99 |
| 🟢 15 | 9,80 | 9,80 | 9,80 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 16 | 15,10 | 15,10 | 15,10 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 |
| 🟢 17 | 14,85 | 14,85 | 14,85 | 15,92 | 15,92 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 |
| 🟢 18 | 15,82 | 15,82 | 15,82 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 19 | 10,14 | 10,14 | 10,14 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 20 | 12,36 | 12,36 | 12,36 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟢 21 | 9,06 | 9,06 | 9,06 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 22 | 13,18 | 13,18 | 13,18 | 21,42 | 21,42 | 21,42 | 21,42 | 21,42 | 21,42 | 21,42 |
| 🟢 23 | 7,61 | 7,61 | 7,61 | 10,14 | 10,14 | 10,14 | 10,14 | 10,14 | 10,14 | 10,14 |
| 🟡 24 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 25 | 4,01 | 4,01 | 4,01 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 7,57 | 7,57 |
| 🟢 26 | 9,03 | 9,03 | 9,03 | 11,96 | 11,96 | 11,96 | 11,96 | 11,96 | 15,18 | 15,18 |
| 🟢 27 | 9,03 | 9,03 | 9,03 | 11,96 | 11,96 | 11,96 | 11,96 | 11,96 | 15,18 | 15,18 |
| 🟢 28 | 10,57 | 10,57 | 10,57 | 14,43 | 14,43 | 14,43 | 14,43 | 14,43 | 19,52 | 19,52 |
| 🟢 29 | 4,01 | 4,01 | 4,01 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 7,57 | 7,57 |
| 🟢 30 | 15,34 | 15,34 | 15,34 | 15,85 | 15,85 | 15,85 | 15,85 | 15,85 | 16,18 | 16,18 |
| 🟢 31 | 16,99 | 16,99 | 16,99 | 17,55 | 17,55 | 17,55 | 17,55 | 17,55 | 17,93 | 17,93 |
| 🟢 32 | 16,87 | 16,87 | 16,87 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,77 | 17,77 |
| 🟢 33 | 17,62 | 17,62 | 17,62 | 17,89 | 17,89 | 17,89 | 17,89 | 17,89 | 19,00 | 19,00 |
| 🟢 34 | 13,53 | 13,53 | 15,67 | 17,28 | 21,34 | 23,94 | 23,94 | 23,94 | 28,57 | 28,57 |
| 🟢 35 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 |
| 🟢 37 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 |
| 🟢 38 | 12,85 | 12,85 | 14,89 | 17,28 | 21,34 | 23,94 | 23,94 | 23,94 | 28,57 | 28,57 |
| 🟢 39 | 10,77 | 10,77 | 10,77 | 13,68 | 13,68 | 13,68 | 13,68 | 13,68 | 21,48 | 21,48 |
| 🟢 40 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 |
| 🟢 41 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 |
| 🟢 42 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 |
| 🟡 43 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 44 | 8,61 | 8,61 | 9,87 | 11,82 | 11,82 | 11,82 | 11,82 | 11,82 | 14,18 | 14,18 |
| 🟢 45 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 18,18 | 18,18 |
| 🟢 46 | 26,15 | 26,15 | 26,15 | 26,15 | 26,15 | 26,15 | 26,15 | 26,15 | 26,66 | 26,66 |
| 🟢 47 | 14,96 | 14,96 | 14,96 | 14,96 | 14,96 | 14,96 | 14,96 | 14,96 | 15,12 | 15,12 |
| 🟢 48 | 8,61 | 8,61 | 9,87 | 11,82 | 11,82 | 11,82 | 11,82 | 11,82 | 14,18 | 14,18 |
| 🟢 49 | 8,45 | 8,45 | 8,45 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 16,80 | 16,80 |
| 🟢 50 | 8,17 | 8,17 | 8,17 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 12,17 | 12,17 |
| 🟢 51 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 52 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 53 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 54 | 8,17 | 8,17 | 8,17 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 12,17 | 12,17 |
| 🟢 55 | 14,81 | 14,81 | 14,81 | 22,22 | 22,22 | 22,22 | 22,22 | 28,88 | 28,88 | 28,88 |
| 🟢 56 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 57 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 58 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 59 | 7,41 | 7,41 | 7,41 | 22,22 | 22,22 | 22,22 | 22,22 | 28,88 | 28,88 | 28,88 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 61 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 28,77 | 28,77 |
| 🟢 62 | 16,99 | 16,99 | 16,99 | 16,99 | 16,99 | 16,99 | 16,99 | 16,99 | 26,93 | 26,93 |
| 🟢 63 | 14,73 | 14,73 | 14,73 | 14,73 | 14,73 | 14,73 | 14,73 | 14,73 | 23,66 | 23,66 |
| 🟢 64 | 17,81 | 17,81 | 17,81 | 17,81 | 17,81 | 17,81 | 17,81 | 17,81 | 27,68 | 27,68 |
| 🟢 65 | 9,32 | 9,32 | 9,32 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 66 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 17,17 | 17,17 | 17,17 | 17,72 | 17,72 | 17,96 | 17,96 | 17,96 | 18,07 | 18,07 |
| 🟢 70 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 17,17 | 17,17 | 17,17 | 17,72 | 17,72 | 17,96 | 17,96 | 17,96 | 18,07 | 18,07 |
| 🟢 74 | 14,31 | 14,31 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 24,08 | 24,08 |
| 🟢 75 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 24,08 | 24,08 |
| 🟢 76 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 4,11 | 4,11 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 24,08 | 24,08 |
| 🟢 79 | 12,38 | 12,38 | 12,38 | 16,89 | 16,89 | 16,89 | 16,89 | 33,77 | 33,77 | 33,77 |
| 🟢 80 | 33,72 | 33,72 | 33,72 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 |
| 🟢 81 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 |
| 🟢 82 | 26,45 | 26,45 | 26,45 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 |
| 🟡 83 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 |
| 🟢 84 | 9,24 | 9,24 | 9,24 | 9,24 | 9,24 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 85 | 9,24 | 9,24 | 9,24 | 9,24 | 9,24 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 |
| 🟢 86 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 |
| 🟢 87 | 6,83 | 6,83 | 6,83 | 6,83 | 6,83 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 88 | 4,62 | 4,62 | 4,62 | 4,62 | 4,62 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 |
| 🟢 89 | 5,74 | 5,74 | 5,74 | 6,13 | 6,13 | 6,13 | 6,13 | 6,13 | 6,88 | 6,88 |
| 🟢 90 | 6,10 | 6,10 | 6,10 | 6,49 | 6,49 | 6,49 | 6,49 | 6,49 | 7,27 | 7,27 |
| 🟢 91 | 6,10 | 6,10 | 6,10 | 6,49 | 6,49 | 6,49 | 6,49 | 6,49 | 7,27 | 7,27 |
| 🟢 92 | 6,54 | 6,54 | 6,54 | 6,96 | 6,96 | 6,96 | 6,96 | 6,96 | 7,70 | 7,70 |
| 🟢 93 | 2,87 | 2,87 | 2,87 | 3,06 | 3,06 | 3,06 | 3,06 | 3,06 | 3,44 | 3,44 |
| 🟢 94 | 6,97 | 6,97 | 8,31 | 9,63 | 9,63 | 9,63 | 9,63 | 10,77 | 10,77 | 10,77 |
| 🟢 95 | 8,81 | 8,81 | 10,58 | 12,13 | 12,13 | 12,13 | 12,13 | 12,92 | 12,92 | 12,92 |
| 🟢 96 | 9,72 | 9,72 | 11,41 | 13,23 | 13,23 | 13,23 | 13,23 | 13,62 | 13,62 | 13,62 |
| 🟢 97 | 6,97 | 6,97 | 8,31 | 9,63 | 9,63 | 9,63 | 9,63 | 10,77 | 10,77 | 10,77 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 7,94 | 7,94 |
| 🟢 100 | 11,98 | 11,98 | 11,98 | 11,98 | 11,98 | 11,98 | 11,98 | 11,98 | 14,05 | 14,05 |
| 🟢 101 | 9,01 | 9,01 | 9,01 | 9,01 | 9,01 | 9,01 | 9,01 | 9,01 | 10,53 | 10,53 |
| 🟢 102 | 14,37 | 14,37 | 14,37 | 14,37 | 14,37 | 14,37 | 14,37 | 14,37 | 16,86 | 16,86 |
| 🟢 103 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 7,94 | 7,94 |
| 🟢 104 | 9,95 | 9,95 | 13,18 | 13,18 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 105 | 12,75 | 12,75 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,97 | 12,97 |
| 🟢 106 | 12,75 | 12,75 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,97 | 12,97 |
| 🟢 107 | 12,75 | 12,75 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,97 | 12,97 |
| 🟢 108 | 9,95 | 9,95 | 13,18 | 13,18 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 109 | 8,42 | 8,42 | 8,42 | 11,59 | 11,59 | 11,59 | 11,59 | 11,59 | 13,74 | 13,74 |
| 🟢 110 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 8,42 | 8,42 | 8,42 | 11,59 | 11,59 | 11,59 | 11,59 | 11,59 | 13,74 | 13,74 |
| 🟢 114 | 13,66 | 13,66 | 13,66 | 13,66 | 13,66 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 115 | 13,66 | 13,66 | 13,66 | 13,66 | 13,66 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 116 | 13,50 | 13,50 | 13,50 | 13,50 | 13,50 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 117 | 13,50 | 13,50 | 13,50 | 13,50 | 13,50 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 118 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 |
| 🟢 119 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 |
| 🟢 120 | 13,50 | 13,50 | 13,50 | 13,50 | 13,50 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 121 | 13,50 | 13,50 | 13,50 | 13,50 | 13,50 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 122 | 4,78 | 4,78 | 4,78 | 4,78 | 4,78 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 123 | 4,78 | 4,78 | 4,78 | 4,78 | 4,78 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 124 | 7,80 | 7,80 | 7,80 | 10,60 | 10,60 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 |
| 🟢 125 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 |
| 🟢 128 | 9,38 | 9,38 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 14,66 | 19,04 | 19,04 |
| 🟢 129 | 7,78 | 7,78 | 7,78 | 8,77 | 8,77 | 12,15 | 12,15 | 12,15 | 15,78 | 15,78 |
| 🟢 130 | 8,74 | 8,74 | 8,74 | 9,85 | 9,85 | 13,65 | 13,65 | 13,65 | 17,73 | 17,73 |
| 🟢 131 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 9,38 | 9,38 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 14,66 | 19,04 | 19,04 |
| 🟢 141 | 7,78 | 7,78 | 7,78 | 8,77 | 8,77 | 12,15 | 12,15 | 12,15 | 15,78 | 15,78 |
| 🟢 142 | 8,74 | 8,74 | 8,74 | 9,85 | 9,85 | 13,65 | 13,65 | 13,65 | 17,73 | 17,73 |
| 🟢 143 | 5,39 | 5,39 | 5,39 | 7,01 | 7,01 | 7,01 | 7,01 | 7,01 | 9,92 | 9,92 |
| 🟢 144 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 5,39 | 5,39 | 5,39 | 7,01 | 7,01 | 7,01 | 7,01 | 7,01 | 9,92 | 9,92 |
| 🟢 148 | 5,83 | 5,83 | 5,83 | 7,64 | 7,64 | 9,07 | 9,07 | 9,07 | 10,82 | 10,82 |
| 🟢 149 | 12,92 | 12,92 | 12,92 | 16,18 | 16,18 | 18,97 | 18,97 | 18,97 | 22,45 | 22,45 |
| 🟢 150 | 12,92 | 12,92 | 12,92 | 16,18 | 16,18 | 18,97 | 18,97 | 18,97 | 22,45 | 22,45 |
| 🟢 151 | 13,91 | 13,91 | 13,91 | 18,96 | 18,96 | 21,24 | 21,24 | 21,24 | 24,84 | 24,84 |
| 🟢 152 | 5,83 | 5,83 | 5,83 | 7,64 | 7,64 | 9,07 | 9,07 | 9,07 | 10,82 | 10,82 |
| 🟢 153 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 15,55 | 15,55 |
| 🟢 154 | 12,03 | 12,03 | 12,03 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 21,66 | 21,66 |
| 🟢 155 | 18,30 | 18,30 | 18,30 | 18,30 | 18,30 | 18,30 | 18,30 | 18,30 | 28,48 | 28,48 |
| 🟢 156 | 5,39 | 5,39 | 5,39 | 5,39 | 5,39 | 5,39 | 5,39 | 5,39 | 10,77 | 10,77 |
| 🟢 157 | 6,87 | 6,87 | 6,87 | 9,94 | 9,94 | 12,40 | 12,40 | 12,40 | 21,35 | 21,35 |
| 🟢 158 | 11,05 | 11,05 | 11,05 | 16,61 | 16,61 | 16,61 | 16,61 | 16,61 | 20,27 | 20,27 |
| 🟢 159 | 11,64 | 11,64 | 12,92 | 12,92 | 17,60 | 17,60 | 17,60 | 24,53 | 24,53 | 24,53 |
| 🟢 160 | 12,72 | 12,72 | 12,72 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 23,31 | 23,31 |
| 🟢 161 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 22,62 | 22,62 |
| 🟢 162 | 11,05 | 11,05 | 11,05 | 16,61 | 16,61 | 16,61 | 16,61 | 16,61 | 20,27 | 20,27 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 5,00 | 5,00 | 5,00 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 |
| 🟢 165 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 10,76 | 10,76 | 10,76 |
| 🟢 166 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 10,76 | 10,76 | 10,76 |
| 🟢 167 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 7,12 | 10,76 | 10,76 | 10,76 |
| 🟢 168 | 5,00 | 5,00 | 5,00 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 | 6,30 |
| 🟡 169 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 170 | 6,84 | 6,84 | 6,84 | 8,10 | 8,10 | 8,94 | 8,94 | 8,94 | 11,17 | 11,17 |
| 🟢 171 | 8,32 | 8,32 | 8,32 | 8,77 | 8,77 | 9,17 | 9,17 | 9,17 | 10,69 | 10,69 |
| 🟢 172 | 8,32 | 8,32 | 8,32 | 8,77 | 8,77 | 9,17 | 9,17 | 9,17 | 10,69 | 10,69 |
| 🟢 173 | 10,24 | 10,24 | 10,24 | 10,69 | 10,69 | 11,10 | 11,10 | 11,10 | 11,53 | 11,53 |
| 🟢 174 | 2,56 | 2,56 | 3,84 | 3,84 | 4,69 | 4,69 | 4,69 | 5,99 | 5,99 | 6,39 |
| 🟢 175 | 4,71 | 4,71 | 4,71 | 5,08 | 5,08 | 5,44 | 5,44 | 5,44 | 5,80 | 5,80 |
| 🟢 176 | 9,43 | 9,43 | 9,43 | 10,15 | 10,15 | 10,88 | 10,88 | 10,88 | 11,60 | 11,60 |
| 🟢 177 | 9,43 | 9,43 | 9,43 | 10,15 | 10,15 | 10,88 | 10,88 | 10,88 | 11,60 | 11,60 |
| 🟢 178 | 9,43 | 9,43 | 9,43 | 10,15 | 10,15 | 10,88 | 10,88 | 10,88 | 11,60 | 11,60 |
| 🟡 179 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 180 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 19,80 | 19,80 |
| 🟡 181 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 182 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 183 | 6,74 | 6,74 | 6,74 | 8,37 | 8,37 | 9,93 | 9,93 | 9,93 | 11,47 | 11,47 |
| 🟢 184 | 8,74 | 8,74 | 8,74 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 |
| 🟢 185 | 5,85 | 5,85 | 5,85 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 |
| 🟢 186 | 9,05 | 9,05 | 9,05 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 187 | 3,37 | 3,37 | 3,37 | 4,18 | 4,18 | 4,97 | 4,97 | 4,97 | 5,73 | 5,73 |
| 🟡 188 | 8,20 | 8,20 | 8,20 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 189 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 190 | 4,70 | 4,70 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 191 | 6,27 | 6,27 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 192 | 6,27 | 6,27 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 193 | 6,27 | 6,27 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 194 | 2,05 | 2,05 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 195 | 15,08 | 15,08 | 16,82 | 18,49 | 18,49 | 20,28 | 20,28 | 20,28 | 24,40 | 24,40 |
| 🟢 196 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 33,60 | 33,60 |
| 🟢 197 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 33,60 | 33,60 |
| 🟢 198 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 28,50 | 33,60 | 33,60 |
| 🟢 199 | 11,64 | 11,64 | 12,98 | 14,37 | 14,37 | 16,46 | 16,46 | 16,46 | 19,79 | 19,79 |
| 🟢 200 | 6,46 | 6,46 | 6,46 | 8,82 | 8,82 | 8,82 | 8,82 | 8,82 | 12,69 | 12,69 |
| 🟢 201 | 8,89 | 8,89 | 8,89 | 12,31 | 12,31 | 12,31 | 12,31 | 12,31 | 15,75 | 15,75 |
| 🟢 202 | 12,87 | 12,87 | 12,87 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 19,38 | 19,38 |
| 🟢 203 | 8,89 | 8,89 | 8,89 | 12,31 | 12,31 | 12,31 | 12,31 | 12,31 | 15,75 | 15,75 |
| 🟢 204 | 4,44 | 4,44 | 4,44 | 7,54 | 7,54 | 7,54 | 7,54 | 7,54 | 10,58 | 10,58 |
| 🟢 205 | 16,75 | 16,75 | 16,75 | 23,49 | 23,49 | 23,49 | 23,49 | 23,49 | 32,67 | 32,67 |
| 🟢 206 | 17,75 | 17,75 | 17,75 | 21,55 | 21,55 | 21,55 | 21,55 | 21,55 | 41,27 | 41,27 |
| 🟢 207 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 |
| 🟢 209 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 16,04 | 16,04 | 16,04 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 |
| 🟢 211 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 | 46,20 | 46,20 |
| 🟢 212 | 16,75 | 16,75 | 16,75 | 23,49 | 23,49 | 23,49 | 23,49 | 23,49 | 32,67 | 32,67 |
| 🟢 213 | 17,75 | 17,75 | 17,75 | 21,55 | 21,55 | 21,55 | 21,55 | 21,55 | 41,27 | 41,27 |
| 🟢 214 | 7,77 | 7,77 | 7,77 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 15,77 | 15,77 |
| 🟢 215 | 17,17 | 17,17 | 17,17 | 21,01 | 21,01 | 21,01 | 21,01 | 21,01 | 23,52 | 23,52 |
| 🟢 216 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 217 | 17,17 | 17,17 | 17,17 | 21,01 | 21,01 | 21,01 | 21,01 | 21,01 | 23,52 | 23,52 |
| 🟢 218 | 7,77 | 7,77 | 7,77 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 15,77 | 15,77 |
| 🟡 219 | 3,34 | 3,34 | 3,34 | 3,70 | 3,70 | 5,06 | 5,06 | 5,06 | 6,46 | 6,46 |
| 🟢 220 | 4,19 | 4,19 | 4,19 | 7,13 | 7,13 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟢 221 | 5,11 | 5,11 | 5,11 | 8,63 | 8,63 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 |
| 🟢 222 | 5,95 | 5,95 | 5,95 | 10,05 | 10,05 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 223 | 4,19 | 4,19 | 4,19 | 7,13 | 7,13 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟡 224 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 225 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 226 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 227 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 228 | 35,74 | 35,74 | 42,88 | 42,88 | 51,46 | 51,46 | 51,46 | 63,18 | 63,18 | 80,25 |
| 🟢 229 | 85,07 | 85,07 | 85,07 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 230 | 35,80 | 35,80 | 35,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 |
| 🟢 231 | 107,45 | 107,45 | 107,45 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 5,85 | 5,85 | 5,85 | 7,88 | 7,88 | 7,88 | 7,88 | 7,88 | 9,56 | 9,56 |
| 🟢 234 | 6,80 | 6,80 | 6,80 | 9,04 | 9,04 | 9,04 | 9,04 | 9,04 | 10,84 | 10,84 |
| 🟢 235 | 6,80 | 6,80 | 6,80 | 9,04 | 9,04 | 9,04 | 9,04 | 9,04 | 10,84 | 10,84 |
| 🟢 236 | 6,80 | 6,80 | 6,80 | 9,04 | 9,04 | 9,04 | 9,04 | 9,04 | 10,84 | 10,84 |
| 🟢 237 | 14,21 | 14,21 | 14,21 | 19,37 | 19,37 | 19,37 | 19,37 | 38,74 | 38,74 | 38,74 |
| 🟢 238 | 38,68 | 38,68 | 38,68 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 |
| 🟢 239 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 240 | 30,35 | 30,35 | 30,35 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 |
| 🟡 241 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 242 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 20,37 | 20,37 |
| 🟢 243 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 24,61 | 24,61 |
| 🟢 244 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 17,86 | 24,61 | 24,61 |
| 🟢 245 | 18,36 | 18,36 | 18,36 | 18,36 | 18,36 | 18,36 | 18,36 | 18,36 | 25,55 | 25,55 |
| 🟢 246 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 20,37 | 20,37 |
| 🟡 247 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 |
| 🟢 248 | 6,38 | 6,38 | 6,38 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 7,51 | 7,51 |
| 🟢 249 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 250 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 251 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 252 | 6,38 | 6,38 | 6,38 | 6,86 | 6,86 | 6,86 | 6,86 | 6,86 | 7,51 | 7,51 |
| 🟢 253 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 16,09 | 16,09 |
| 🟢 254 | 20,32 | 20,32 | 20,32 | 20,32 | 20,32 | 20,32 | 20,32 | 20,32 | 29,42 | 29,42 |
| 🟢 255 | 22,99 | 22,99 | 22,99 | 22,99 | 22,99 | 22,99 | 22,99 | 22,99 | 27,84 | 27,84 |
| 🟢 256 | 24,28 | 24,28 | 24,28 | 24,28 | 24,28 | 24,28 | 24,28 | 24,28 | 29,42 | 29,42 |
| 🟢 257 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 16,09 | 16,09 |
| 🟢 258 | 14,69 | 14,69 | 14,69 | 20,02 | 20,02 | 20,02 | 20,02 | 40,06 | 40,06 | 40,06 |
| 🟢 259 | 33,98 | 33,98 | 33,98 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 260 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 |
| 🟢 261 | 33,98 | 33,98 | 33,98 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 262 | 2,79 | 2,79 | 3,21 | 3,69 | 3,69 | 3,69 | 3,69 | 3,69 | 4,06 | 4,06 |
| 🟢 263 | 6,03 | 6,03 | 6,03 | 6,93 | 6,93 | 6,93 | 6,93 | 6,93 | 7,97 | 7,97 |
| 🟢 264 | 6,27 | 6,27 | 6,27 | 7,21 | 7,21 | 7,21 | 7,21 | 7,21 | 8,29 | 8,29 |
| 🟢 265 | 7,47 | 7,47 | 7,47 | 8,59 | 8,59 | 8,59 | 8,59 | 8,59 | 9,88 | 9,88 |
| 🟢 266 | 0,89 | 0,89 | 1,03 | 1,18 | 1,18 | 1,18 | 1,18 | 1,18 | 1,30 | 1,30 |
| 🟢 267 | 6,65 | 6,65 | 6,65 | 9,53 | 9,53 | 14,27 | 14,27 | 14,27 | 15,67 | 15,67 |
| 🟢 268 | 12,62 | 12,62 | 12,62 | 18,13 | 18,13 | 27,04 | 27,04 | 27,04 | 29,20 | 29,20 |
| 🟢 269 | 12,62 | 12,62 | 12,62 | 18,13 | 18,13 | 27,04 | 27,04 | 27,04 | 29,20 | 29,20 |
| 🟢 270 | 6,65 | 6,65 | 6,65 | 9,53 | 9,53 | 14,27 | 14,27 | 14,27 | 15,67 | 15,67 |
| 🟡 271 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 272 | 6,59 | 6,59 | 8,66 | 10,21 | 10,21 | 10,47 | 10,47 | 10,47 | 10,53 | 10,53 |
| 🟢 273 | 7,91 | 7,91 | 10,39 | 12,26 | 12,26 | 12,57 | 12,57 | 12,57 | 12,63 | 12,63 |
| 🟢 274 | 7,25 | 7,25 | 9,53 | 11,24 | 11,24 | 11,52 | 11,52 | 11,52 | 11,58 | 11,58 |
| 🟢 275 | 8,24 | 8,24 | 10,83 | 12,77 | 12,77 | 13,09 | 13,09 | 13,09 | 13,16 | 13,16 |
| 🟢 276 | 3,29 | 3,29 | 4,33 | 5,11 | 5,11 | 5,24 | 5,24 | 5,24 | 5,26 | 5,26 |
| 🟡 277 | 3,59 | 3,59 | 4,11 | 4,66 | 5,33 | 6,07 | 6,07 | 6,92 | 7,88 | 7,88 |
| 🟢 278 | 6,16 | 6,16 | 6,16 | 6,83 | 6,83 | 9,65 | 9,65 | 9,65 | 9,65 | 9,65 |
| 🟢 279 | 11,99 | 11,99 | 11,99 | 13,31 | 13,31 | 18,78 | 18,78 | 18,78 | 18,78 | 18,78 |
| 🟢 280 | 6,16 | 6,16 | 6,16 | 6,83 | 6,83 | 9,65 | 9,65 | 9,65 | 9,65 | 9,65 |
| 🟢 281 | 17,28 | 17,28 | 17,28 | 19,20 | 19,20 | 21,76 | 21,76 | 21,76 | 21,76 | 21,76 |
| 🟢 282 | 6,16 | 6,16 | 6,16 | 6,83 | 6,83 | 9,65 | 9,65 | 9,65 | 9,65 | 9,65 |
| 🟢 283 | 7,24 | 7,24 | 7,24 | 7,24 | 7,24 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 |
| 🟢 284 | 5,97 | 5,97 | 5,97 | 5,97 | 5,97 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 285 | 6,12 | 6,12 | 6,12 | 6,12 | 6,12 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 |
| 🟢 286 | 6,55 | 6,55 | 6,55 | 6,55 | 6,55 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 287 | 3,60 | 3,60 | 3,60 | 3,60 | 3,60 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 |
| 🟢 288 | 6,19 | 6,19 | 6,83 | 7,49 | 7,49 | 8,29 | 8,29 | 8,29 | 9,09 | 9,09 |
| 🟢 289 | 8,40 | 8,40 | 9,22 | 10,13 | 10,13 | 11,15 | 11,15 | 11,15 | 12,28 | 12,28 |
| 🟢 290 | 7,16 | 7,16 | 7,85 | 8,65 | 8,65 | 9,50 | 9,50 | 9,50 | 10,43 | 10,43 |
| 🟢 291 | 9,91 | 9,91 | 10,93 | 12,03 | 12,03 | 13,22 | 13,22 | 13,22 | 14,56 | 14,56 |
| 🟢 292 | 3,10 | 3,10 | 3,41 | 3,74 | 3,74 | 4,14 | 4,14 | 4,14 | 4,54 | 4,54 |
| 🟡 293 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 294 | 8,27 | 8,27 | 8,27 | 8,37 | 8,50 | 8,67 | 8,67 | 8,67 | 10,44 | 10,44 |
| 🟢 295 | 17,42 | 17,42 | 17,42 | 17,78 | 18,17 | 18,28 | 18,28 | 18,28 | 24,84 | 24,84 |
| 🟢 296 | 8,27 | 8,27 | 8,27 | 8,37 | 8,50 | 8,67 | 8,67 | 8,67 | 10,44 | 10,44 |
| 🟢 297 | 17,42 | 17,42 | 17,42 | 17,78 | 18,17 | 18,28 | 18,28 | 18,28 | 24,84 | 24,84 |
| 🟢 298 | 8,27 | 8,27 | 8,27 | 8,37 | 8,50 | 8,67 | 8,67 | 8,67 | 10,44 | 10,44 |
| 🟢 299 | 4,38 | 4,38 | 4,38 | 7,21 | 7,21 | 8,37 | 8,37 | 8,37 | 11,88 | 11,88 |
| 🟢 300 | 6,53 | 6,53 | 6,53 | 10,82 | 10,82 | 12,44 | 12,44 | 12,44 | 17,71 | 17,71 |
| 🟢 301 | 4,38 | 4,38 | 4,38 | 7,21 | 7,21 | 8,37 | 8,37 | 8,37 | 11,88 | 11,88 |
| 🟢 302 | 6,53 | 6,53 | 6,53 | 10,82 | 10,82 | 12,44 | 12,44 | 12,44 | 17,71 | 17,71 |
| 🟢 303 | 4,38 | 4,38 | 4,38 | 7,21 | 7,21 | 8,37 | 8,37 | 8,37 | 11,88 | 11,88 |
| 🟡 304 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 305 | 3,76 | 3,76 | 3,93 | 4,31 | 4,31 | 4,51 | 4,51 | 4,51 | 4,72 | 4,72 |
| 🟢 306 | 3,63 | 3,63 | 3,63 | 4,31 | 4,31 | 4,51 | 4,51 | 4,51 | 4,72 | 4,72 |
| 🟢 307 | 3,63 | 3,63 | 3,63 | 4,31 | 4,31 | 4,51 | 4,51 | 4,51 | 4,72 | 4,72 |
| 🟢 308 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 309 | 1,88 | 1,88 | 1,96 | 2,16 | 2,16 | 2,25 | 2,25 | 2,25 | 2,36 | 2,36 |
| 🟡 310 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 311 | 4,05 | 4,05 | 4,05 | 4,75 | 4,75 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 |
| 🟢 312 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 313 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 314 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 |
| 🟡 315 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 318 | 9,17 | 9,17 | 9,17 | 9,56 | 9,56 | 10,05 | 10,05 | 10,05 | 10,66 | 10,66 |
| 🟢 319 | 11,67 | 11,67 | 11,67 | 12,75 | 12,75 | 13,85 | 13,85 | 13,85 | 14,90 | 14,90 |
| 🟢 320 | 11,67 | 11,67 | 11,67 | 12,75 | 12,75 | 13,85 | 13,85 | 13,85 | 14,90 | 14,90 |
| 🟢 321 | 13,02 | 13,02 | 13,02 | 15,80 | 15,80 | 17,19 | 17,19 | 17,19 | 18,56 | 18,56 |
| 🟢 322 | 8,13 | 8,13 | 8,13 | 10,00 | 10,00 | 12,50 | 12,50 | 12,50 | 15,00 | 15,00 |
| 🟢 323 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 324 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 325 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 326 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 327 | 5,76 | 5,76 | 5,76 | 5,76 | 5,76 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 328 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 |
| 🟢 329 | 3,79 | 3,79 | 3,79 | 3,79 | 3,79 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 |
| 🟢 330 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 |
| 🟢 331 | 2,88 | 2,88 | 2,88 | 2,88 | 2,88 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 |
| 🟢 332 | 6,45 | 6,45 | 8,17 | 9,88 | 9,88 | 10,17 | 10,17 | 10,17 | 10,23 | 10,23 |
| 🟢 333 | 7,74 | 7,74 | 9,80 | 11,86 | 11,86 | 12,20 | 12,20 | 12,20 | 12,27 | 12,27 |
| 🟢 334 | 7,74 | 7,74 | 9,80 | 11,86 | 11,86 | 12,20 | 12,20 | 12,20 | 12,27 | 12,27 |
| 🟢 335 | 8,06 | 8,06 | 10,21 | 12,36 | 12,36 | 12,71 | 12,71 | 12,71 | 12,78 | 12,78 |
| 🟢 336 | 3,22 | 3,22 | 4,08 | 4,94 | 4,94 | 5,09 | 5,09 | 5,09 | 5,11 | 5,11 |
| 🟢 337 | 6,54 | 6,54 | 6,54 | 7,78 | 7,78 | 8,83 | 8,83 | 8,83 | 9,85 | 9,85 |
| 🟢 338 | 9,06 | 9,06 | 9,06 | 10,39 | 10,39 | 12,44 | 12,44 | 12,44 | 14,79 | 14,79 |
| 🟢 339 | 6,54 | 6,54 | 6,54 | 7,78 | 7,78 | 8,83 | 8,83 | 8,83 | 9,85 | 9,85 |
| 🟢 340 | 15,33 | 15,33 | 15,33 | 17,63 | 17,63 | 19,73 | 19,73 | 19,73 | 22,31 | 22,31 |
| 🟢 341 | 6,54 | 6,54 | 6,54 | 7,78 | 7,78 | 8,83 | 8,83 | 8,83 | 9,85 | 9,85 |
| 🟢 342 | 4,31 | 4,31 | 4,77 | 5,27 | 6,34 | 8,07 | 8,07 | 8,07 | 8,07 | 8,07 |
| 🟢 343 | 7,47 | 7,47 | 7,47 | 8,57 | 8,57 | 9,97 | 9,97 | 9,97 | 9,97 | 9,97 |
| 🟢 344 | 4,31 | 4,31 | 4,77 | 6,34 | 6,34 | 8,07 | 8,07 | 8,07 | 8,07 | 8,07 |
| 🟢 345 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 |
| 🟢 346 | 2,59 | 2,59 | 2,86 | 3,16 | 3,80 | 8,07 | 8,07 | 8,07 | 8,07 | 8,07 |
| 🟢 347 | 10,32 | 10,32 | 10,32 | 12,68 | 12,68 | 14,23 | 14,23 | 14,23 | 16,22 | 16,22 |
| 🟢 348 | 10,54 | 10,54 | 10,54 | 12,68 | 12,68 | 14,23 | 14,23 | 14,23 | 16,22 | 16,22 |
| 🟢 349 | 10,47 | 10,47 | 10,47 | 12,01 | 12,01 | 14,23 | 14,23 | 14,23 | 14,23 | 14,23 |
| 🟢 350 | 0,00 | 0,00 | 0,00 | 12,68 | 12,68 | 14,23 | 14,23 | 14,23 | 14,23 | 14,23 |
| 🟢 351 | 6,98 | 6,98 | 7,69 | 8,05 | 8,05 | 8,47 | 8,47 | 8,47 | 8,90 | 8,90 |
| 🟢 352 | 6,98 | 6,98 | 7,69 | 8,05 | 8,05 | 8,47 | 8,47 | 8,47 | 8,90 | 8,90 |
| 🟢 353 | 8,24 | 8,24 | 8,24 | 10,40 | 10,40 | 12,35 | 12,35 | 12,35 | 13,55 | 13,55 |
| 🟢 354 | 15,35 | 15,35 | 15,35 | 20,03 | 20,03 | 20,94 | 20,94 | 20,94 | 22,34 | 22,34 |
| 🟢 355 | 2,31 | 2,31 | 2,31 | 3,00 | 3,00 | 3,15 | 3,15 | 3,15 | 3,35 | 3,35 |
| 🟢 356 | 17,00 | 17,00 | 17,00 | 23,36 | 23,36 | 24,01 | 24,01 | 24,01 | 26,81 | 26,81 |
| 🟢 357 | 2,47 | 2,47 | 2,47 | 3,12 | 3,12 | 3,72 | 3,72 | 3,72 | 4,06 | 4,06 |
| 🟢 358 | 8,21 | 8,21 | 8,21 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟢 359 | 10,84 | 10,84 | 10,84 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 360 | 10,75 | 10,75 | 10,75 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 361 | 12,62 | 12,62 | 12,62 | 12,62 | 12,62 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 |
| 🟢 362 | 8,21 | 8,21 | 8,21 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 363 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 364 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 |
| 🟡 365 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 16,50 | 16,50 |
| 🟡 366 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 9,74 | 9,74 | 9,74 | 9,74 | 9,74 |
| 🟡 367 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 12,50 | 12,50 |
| 🟢 368 | 6,23 | 6,23 | 6,23 | 6,96 | 6,96 | 8,72 | 8,72 | 8,72 | 10,52 | 10,52 |
| 🟢 369 | 7,63 | 7,63 | 7,63 | 8,78 | 8,78 | 10,82 | 10,82 | 10,82 | 13,11 | 13,11 |
| 🟢 370 | 7,63 | 7,63 | 7,63 | 8,78 | 8,78 | 10,82 | 10,82 | 10,82 | 13,11 | 13,11 |
| 🟢 371 | 8,02 | 8,02 | 9,14 | 10,52 | 12,21 | 14,29 | 14,29 | 14,29 | 16,84 | 16,84 |
| 🟢 372 | 9,63 | 9,63 | 10,98 | 12,63 | 14,65 | 17,15 | 17,15 | 17,15 | 20,20 | 20,20 |
| 🟢 373 | 8,02 | 8,02 | 9,14 | 10,52 | 12,21 | 14,29 | 14,29 | 14,29 | 16,84 | 16,84 |
| 🟢 374 | 11,24 | 11,24 | 12,81 | 14,73 | 17,09 | 20,00 | 20,00 | 20,00 | 23,58 | 23,58 |
| 🟢 375 | 8,02 | 8,02 | 9,14 | 10,52 | 12,21 | 14,29 | 14,29 | 14,29 | 16,84 | 16,84 |
| 🟢 376 | 3,96 | 3,96 | 4,73 | 5,65 | 6,85 | 6,85 | 6,85 | 8,21 | 8,21 | 8,21 |
| 🟢 377 | 9,38 | 9,38 | 11,30 | 13,50 | 16,25 | 16,25 | 16,25 | 19,52 | 19,52 | 19,52 |
| 🟢 378 | 16,55 | 16,55 | 18,99 | 21,86 | 25,09 | 25,09 | 25,09 | 28,91 | 28,91 | 28,91 |
| 🟢 379 | 3,96 | 3,96 | 4,73 | 5,65 | 6,85 | 6,85 | 6,85 | 8,21 | 8,21 | 8,21 |
| 🟡 380 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 381 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 17,57 | 17,57 |
| 🟢 382 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 |
| 🟢 383 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 10,20 | 10,20 |
| 🟢 384 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 8,32 | 8,32 |
| 🟢 385 | 5,16 | 5,16 | 5,16 | 6,40 | 6,40 | 6,40 | 6,40 | 6,40 | 9,24 | 9,24 |
| 🟢 386 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 |
| 🟢 387 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 |
| 🟢 388 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 31,84 | 31,84 |
| 🟢 389 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 18,41 | 18,41 |
| 🟢 390 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 25,18 | 25,18 |
| 🟢 391 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 20,52 | 20,52 |
| 🟢 392 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 14,68 | 14,68 |
| 🟢 393 | 6,39 | 6,39 | 6,39 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 9,28 | 9,28 |
| 🟢 394 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 18,41 | 18,41 |
| 🟢 395 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 20,75 | 20,75 |
| 🟢 396 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 31,84 | 31,84 |
| 🟢 397 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 18,41 | 18,41 |
| 🟢 398 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 25,18 | 25,18 |
| 🟢 399 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 20,52 | 20,52 |
| 🟢 400 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 14,68 | 14,68 |
| 🟢 401 | 7,70 | 7,70 | 7,70 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 11,82 | 11,82 |
| 🟢 402 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 20,75 | 20,75 |
| 🟢 403 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 30,57 | 31,84 | 31,84 |
| 🟢 404 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 15,68 | 18,41 | 18,41 |
| 🟢 405 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 23,33 | 25,18 | 25,18 |
| 🟢 406 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 16,15 | 20,52 | 20,52 |
| 🟢 407 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 14,68 | 14,68 |
| 🟢 408 | 7,10 | 7,10 | 7,10 | 9,59 | 9,59 | 9,59 | 9,59 | 9,59 | 10,82 | 10,82 |
| 🟢 409 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 20,75 | 20,75 |
| 🟢 410 | 7,79 | 7,79 | 7,79 | 11,10 | 11,10 | 11,10 | 11,10 | 11,10 | 12,26 | 12,26 |
| 🟢 411 | 4,30 | 4,30 | 4,30 | 6,12 | 6,12 | 6,12 | 6,12 | 6,12 | 7,29 | 7,29 |
| 🟢 412 | 3,68 | 3,68 | 3,68 | 5,25 | 5,25 | 5,25 | 5,25 | 5,25 | 7,13 | 7,13 |
| 🟢 413 | 3,71 | 3,71 | 3,71 | 5,35 | 5,35 | 5,35 | 5,35 | 5,35 | 6,33 | 6,33 |
| 🟢 414 | 5,16 | 5,16 | 5,16 | 6,40 | 6,40 | 6,40 | 6,40 | 6,40 | 9,24 | 9,24 |
| 🟢 415 | 4,30 | 4,30 | 4,30 | 6,12 | 6,12 | 6,12 | 6,12 | 6,12 | 7,29 | 7,29 |
| 🟢 416 | 2,57 | 2,57 | 2,57 | 2,81 | 2,81 | 3,10 | 3,10 | 3,10 | 3,46 | 3,46 |
| 🟢 417 | 3,21 | 3,21 | 3,21 | 3,55 | 3,55 | 3,90 | 3,90 | 3,90 | 4,29 | 4,29 |
| 🟢 418 | 3,21 | 3,21 | 3,21 | 3,55 | 3,55 | 3,90 | 3,90 | 3,90 | 4,29 | 4,29 |
| 🟢 419 | 2,75 | 2,75 | 2,75 | 3,01 | 3,01 | 3,30 | 3,30 | 3,30 | 3,66 | 3,66 |
| 🟢 420 | 1,08 | 1,08 | 1,08 | 1,19 | 1,19 | 1,31 | 1,31 | 1,31 | 1,46 | 1,46 |
| 🟢 421 | 5,77 | 5,77 | 6,49 | 6,97 | 6,97 | 7,45 | 7,45 | 7,45 | 7,69 | 7,69 |
| 🟢 422 | 6,92 | 6,92 | 7,78 | 8,36 | 8,36 | 8,94 | 8,94 | 8,94 | 9,23 | 9,23 |
| 🟢 423 | 6,34 | 6,34 | 7,14 | 7,67 | 7,67 | 8,19 | 8,19 | 8,19 | 8,46 | 8,46 |
| 🟢 424 | 7,21 | 7,21 | 8,11 | 8,71 | 8,71 | 9,31 | 9,31 | 9,31 | 9,61 | 9,61 |
| 🟢 425 | 2,88 | 2,88 | 3,24 | 3,48 | 3,48 | 3,72 | 3,72 | 3,72 | 3,85 | 3,85 |
| 🟢 426 | 4,68 | 4,68 | 4,68 | 6,43 | 6,43 | 7,25 | 7,25 | 7,25 | 10,21 | 10,21 |
| 🟢 427 | 6,13 | 6,43 | 6,43 | 6,43 | 6,43 | 6,43 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 428 | 4,68 | 4,68 | 4,68 | 6,43 | 6,43 | 7,25 | 7,25 | 7,25 | 10,21 | 10,21 |
| 🟢 429 | 6,13 | 6,43 | 6,43 | 6,43 | 6,43 | 6,43 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 430 | 3,51 | 3,51 | 3,51 | 6,43 | 6,43 | 7,25 | 7,25 | 7,25 | 10,21 | 10,21 |
| 🟢 431 | 6,77 | 6,77 | 6,77 | 9,82 | 9,82 | 9,82 | 9,82 | 9,82 | 16,23 | 16,23 |
| 🟢 432 | 7,45 | 7,45 | 7,45 | 10,82 | 10,82 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 433 | 7,45 | 7,45 | 7,45 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 17,85 | 17,85 |
| 🟢 434 | 8,97 | 8,97 | 8,97 | 12,98 | 12,98 | 12,98 | 12,98 | 12,98 | 21,41 | 21,41 |
| 🟢 435 | 6,77 | 6,77 | 6,77 | 9,82 | 9,82 | 9,82 | 9,82 | 9,82 | 16,23 | 16,23 |
| 🟢 436 | 7,75 | 7,75 | 7,79 | 8,34 | 8,34 | 9,77 | 9,77 | 9,77 | 11,47 | 11,47 |
| 🟢 437 | 7,75 | 7,75 | 7,79 | 8,34 | 8,34 | 9,77 | 9,77 | 9,77 | 11,47 | 11,47 |
| 🟢 438 | 5,15 | 5,15 | 5,15 | 6,62 | 6,62 | 6,90 | 6,90 | 6,90 | 9,23 | 9,23 |
| 🟢 439 | 5,15 | 5,15 | 5,15 | 6,62 | 6,62 | 6,90 | 6,90 | 6,90 | 9,23 | 9,23 |
| 🟢 440 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 11,31 | 11,31 |
| 🟢 441 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 18,89 | 18,89 |
| 🟢 442 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 11,30 | 18,89 | 18,89 |
| 🟢 443 | 15,52 | 15,52 | 15,52 | 15,52 | 15,52 | 15,52 | 15,52 | 15,52 | 23,91 | 23,91 |
| 🟢 444 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 5,64 | 5,64 |
| 🟢 445 | 4,13 | 4,13 | 4,13 | 5,58 | 5,58 | 5,58 | 5,58 | 5,58 | 7,82 | 7,82 |
| 🟢 446 | 10,77 | 10,77 | 10,77 | 15,64 | 15,64 | 15,64 | 15,64 | 15,64 | 21,88 | 21,88 |
| 🟢 447 | 4,97 | 4,97 | 4,97 | 6,53 | 6,53 | 6,53 | 6,53 | 6,53 | 8,42 | 8,42 |
| 🟢 448 | 21,60 | 21,60 | 21,60 | 32,41 | 32,41 | 32,41 | 32,41 | 32,41 | 35,66 | 35,66 |
| 🟢 449 | 4,13 | 4,13 | 4,13 | 5,58 | 5,58 | 5,58 | 5,58 | 5,58 | 7,82 | 7,82 |
| 🟢 450 | 4,81 | 4,81 | 5,39 | 5,83 | 5,93 | 6,46 | 6,46 | 6,46 | 7,02 | 7,02 |
| 🟢 451 | 4,81 | 4,81 | 5,39 | 5,83 | 5,93 | 6,46 | 6,46 | 6,46 | 7,02 | 7,02 |
| 🟢 452 | 4,90 | 4,90 | 6,08 | 7,14 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 453 | 6,64 | 6,64 | 8,00 | 9,19 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 |
| 🟢 454 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 10,57 | 10,57 | 10,57 | 11,51 | 11,51 |
| 🟢 455 | 4,90 | 4,90 | 6,08 | 7,14 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 456 | 5,39 | 5,39 | 7,18 | 9,33 | 9,33 | 12,57 | 12,57 | 12,57 | 15,77 | 15,77 |
| 🟢 457 | 4,47 | 4,47 | 4,47 | 6,80 | 6,80 | 8,37 | 8,37 | 8,37 | 10,98 | 10,98 |
| 🟢 458 | 9,22 | 9,22 | 9,22 | 18,52 | 18,52 | 21,22 | 21,22 | 21,22 | 23,08 | 23,08 |
| 🟢 459 | 9,22 | 9,22 | 9,22 | 18,52 | 18,52 | 21,22 | 21,22 | 21,22 | 23,08 | 23,08 |
| 🟢 460 | 9,22 | 9,22 | 9,22 | 18,52 | 18,52 | 21,22 | 21,22 | 21,22 | 23,08 | 23,08 |
| 🟢 461 | 4,47 | 4,47 | 4,47 | 6,80 | 6,80 | 8,37 | 8,37 | 8,37 | 10,98 | 10,98 |
| 🟡 462 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 463 | 6,45 | 6,45 | 6,45 | 8,05 | 8,05 | 8,05 | 8,05 | 8,05 | 9,60 | 9,60 |
| 🟢 464 | 9,19 | 9,19 | 9,19 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 15,12 | 15,12 |
| 🟢 465 | 14,69 | 14,69 | 14,69 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 19,78 | 19,78 |
| 🟢 466 | 9,19 | 9,19 | 9,19 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 15,12 | 15,12 |
| 🟢 467 | 6,45 | 6,45 | 6,45 | 8,05 | 8,05 | 8,05 | 8,05 | 8,05 | 9,60 | 9,60 |
| 🟢 468 | 8,63 | 8,63 | 8,63 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 469 | 11,00 | 11,00 | 11,00 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 470 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 |
| 🟢 471 | 11,00 | 11,00 | 11,00 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 472 | 11,37 | 11,37 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 13,18 | 13,18 |
| 🟢 473 | 9,53 | 9,53 | 9,53 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 |
| 🟢 474 | 11,37 | 11,37 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 13,18 | 13,18 |
| 🟢 475 | 9,53 | 9,53 | 9,53 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 |
| 🟢 476 | 21,75 | 21,75 | 21,75 | 22,66 | 22,66 | 22,66 | 22,66 | 22,66 | 24,36 | 24,36 |
| 🟢 477 | 21,75 | 21,75 | 21,75 | 22,66 | 22,66 | 22,66 | 22,66 | 22,66 | 24,36 | 24,36 |
| 🟢 478 | 21,75 | 21,75 | 21,75 | 22,66 | 22,66 | 22,66 | 22,66 | 22,66 | 24,36 | 24,36 |
| 🟢 479 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 |
| 🟢 480 | 7,81 | 7,81 | 10,30 | 10,30 | 10,30 | 12,49 | 12,49 | 12,49 | 14,31 | 14,31 |
| 🟢 481 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 13,39 | 13,39 | 13,39 | 14,74 | 14,74 |
| 🟢 482 | 7,81 | 7,81 | 10,30 | 10,30 | 10,30 | 12,49 | 12,49 | 12,49 | 14,31 | 14,31 |
| 🟢 483 | 12,63 | 12,63 | 12,63 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 |
| 🟢 484 | 7,81 | 7,81 | 10,30 | 10,30 | 10,30 | 12,49 | 12,49 | 12,49 | 14,31 | 14,31 |
| 🟢 485 | 11,37 | 11,37 | 12,49 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 486 | 11,83 | 11,83 | 11,83 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 |
| 🟢 487 | 11,83 | 11,83 | 11,83 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 |
| 🟢 488 | 11,83 | 11,83 | 11,83 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 |
| 🟢 489 | 7,52 | 7,52 | 7,52 | 7,58 | 7,58 | 9,34 | 9,34 | 9,34 | 10,74 | 10,74 |
| 🟢 490 | 9,10 | 9,10 | 9,10 | 15,97 | 15,97 | 17,97 | 17,97 | 17,97 | 24,69 | 24,69 |
| 🟢 491 | 10,01 | 10,01 | 10,01 | 17,54 | 17,54 | 17,97 | 17,97 | 17,97 | 25,18 | 25,18 |
| 🟢 492 | 14,66 | 14,66 | 14,66 | 18,66 | 18,66 | 21,40 | 21,40 | 21,40 | 28,56 | 28,56 |
| 🟢 493 | 7,52 | 7,52 | 7,52 | 7,58 | 7,58 | 9,34 | 9,34 | 9,34 | 10,74 | 10,74 |
| 🟢 494 | 9,60 | 9,60 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 10,07 | 10,07 |
| 🟢 495 | 12,79 | 12,79 | 12,79 | 15,58 | 15,58 | 15,58 | 15,58 | 15,58 | 16,80 | 16,80 |
| 🟡 496 | 10,80 | 10,80 | 10,80 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 497 | 10,43 | 10,43 | 12,82 | 13,65 | 13,65 | 13,65 | 13,65 | 13,65 | 20,94 | 20,94 |
| 🟢 498 | 10,43 | 10,43 | 12,82 | 13,65 | 13,65 | 13,65 | 13,65 | 13,65 | 20,94 | 20,94 |
| 🟢 499 | 4,57 | 4,57 | 5,46 | 6,35 | 7,24 | 8,12 | 8,12 | 9,01 | 9,90 | 9,90 |
| 🟢 500 | 7,85 | 7,85 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,68 | 8,68 |
| 🟢 501 | 14,11 | 14,11 | 14,11 | 19,62 | 19,62 | 19,62 | 19,62 | 19,62 | 21,34 | 21,34 |
| 🟢 502 | 8,99 | 8,99 | 8,99 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 10,83 | 10,83 |
| 🟢 503 | 8,45 | 8,45 | 9,54 | 10,89 | 10,89 | 12,33 | 12,33 | 12,33 | 14,06 | 14,06 |
| 🟢 504 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 11,91 | 11,91 |
| 🟢 508 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 21,22 | 21,22 |
| 🟢 509 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 21,22 | 21,22 |
| 🟢 510 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 18,08 | 21,22 | 21,22 |
| 🟢 511 | 5,28 | 5,28 | 5,28 | 7,63 | 7,63 | 7,63 | 7,63 | 7,63 | 9,06 | 9,06 |
| 🟢 512 | 9,36 | 9,36 | 9,36 | 9,98 | 9,98 | 9,98 | 9,98 | 9,98 | 10,41 | 10,41 |
| 🟢 513 | 11,14 | 11,14 | 11,14 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,81 | 11,81 |
| 🟢 514 | 10,60 | 10,60 | 10,60 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,86 | 10,86 |
| 🟢 515 | 12,25 | 12,25 | 12,25 | 12,57 | 12,57 | 12,57 | 12,57 | 12,57 | 12,80 | 12,80 |
| 🟡 516 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 517 | 8,00 | 8,00 | 8,00 | 8,00 | 11,63 | 11,63 | 11,63 | 11,63 | 16,92 | 16,92 |
| 🟢 518 | 14,66 | 14,66 | 23,71 | 23,71 | 23,71 | 23,71 | 23,71 | 25,08 | 25,08 | 25,08 |
| 🟢 519 | 8,00 | 8,00 | 8,00 | 8,00 | 11,63 | 11,63 | 11,63 | 11,63 | 16,92 | 16,92 |
| 🟢 520 | 0,00 | 0,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 |
| 🟢 521 | 8,00 | 8,00 | 8,00 | 8,00 | 11,63 | 11,63 | 11,63 | 11,63 | 16,92 | 16,92 |
| 🟢 522 | 13,12 | 13,12 | 13,12 | 13,12 | 13,12 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 523 | 6,56 | 6,56 | 6,56 | 6,56 | 6,56 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 524 | 7,73 | 7,73 | 7,73 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 10,22 | 10,22 |
| 🟢 525 | 8,78 | 8,78 | 8,78 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 11,60 | 11,60 |
| 🟢 526 | 8,78 | 8,78 | 8,78 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 11,60 | 11,60 |
| 🟢 527 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 |
| 🟢 528 | 9,62 | 9,62 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 529 | 12,81 | 12,81 | 12,81 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 530 | 12,81 | 12,81 | 12,81 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 531 | 12,39 | 12,39 | 12,39 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 532 | 9,62 | 9,62 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 533 | 9,62 | 9,62 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 534 | 12,81 | 12,81 | 12,81 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 535 | 12,81 | 12,81 | 12,81 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 536 | 12,39 | 12,39 | 12,39 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 537 | 9,62 | 9,62 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 538 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 539 | 10,57 | 10,57 | 13,33 | 15,79 | 15,79 | 15,79 | 15,79 | 15,79 | 17,43 | 17,43 |
| 🟢 540 | 9,46 | 9,46 | 9,96 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,78 | 12,78 |
| 🟢 541 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 |
| 🟢 542 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 |
| 🟢 543 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 |
| 🟢 544 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 |
| 🟢 545 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 |
| 🟢 546 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 |
| 🟢 547 | 10,57 | 10,57 | 13,33 | 15,79 | 15,79 | 15,79 | 15,79 | 15,79 | 17,43 | 17,43 |
| 🟢 548 | 9,46 | 9,46 | 9,96 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,78 | 12,78 |
| 🟢 549 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 16,94 | 16,94 |
| 🟢 550 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 30,68 | 30,68 |
| 🟢 551 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 30,68 | 30,68 |
| 🟢 552 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 29,44 | 30,68 | 30,68 |
| 🟢 553 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 15,37 | 16,94 | 16,94 |
| 🟢 554 | 11,82 | 11,82 | 13,98 | 15,73 | 15,73 | 17,78 | 17,78 | 17,78 | 20,81 | 20,81 |
| 🟢 555 | 11,82 | 11,82 | 13,98 | 15,73 | 15,73 | 17,78 | 17,78 | 17,78 | 20,81 | 20,81 |
| 🟢 556 | 5,25 | 5,25 | 5,25 | 6,99 | 6,99 | 8,64 | 8,64 | 8,64 | 13,14 | 13,14 |
| 🟢 557 | 11,45 | 11,45 | 11,45 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 558 | 12,58 | 12,58 | 12,58 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 |
| 🟢 559 | 13,73 | 13,73 | 13,73 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 |
| 🟢 560 | 13,73 | 13,73 | 13,73 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 |
| 🟢 561 | 11,45 | 11,45 | 11,45 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 562 | 7,48 | 7,48 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 563 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 566 | 7,48 | 7,48 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 567 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 11,11 | 11,11 | 11,11 | 13,59 | 13,59 | 13,59 | 13,59 | 13,59 | 16,29 | 16,29 |
| 🟢 572 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 12,22 | 12,22 | 12,22 | 12,64 | 12,64 | 13,29 | 13,29 | 13,29 | 13,92 | 13,92 |
| 🟢 577 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 12,22 | 12,22 | 12,22 | 12,64 | 12,64 | 13,29 | 13,29 | 13,29 | 13,92 | 13,92 |
| 🟢 581 | 10,53 | 10,53 | 10,53 | 13,89 | 13,89 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 582 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 10,06 | 10,06 | 10,06 | 12,31 | 12,31 | 12,31 | 12,31 | 12,31 | 16,29 | 16,29 |
| 🟢 586 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 11,62 | 11,62 | 11,62 | 15,85 | 15,85 | 15,85 | 15,85 | 31,70 | 31,70 | 31,70 |
| 🟢 590 | 31,65 | 31,65 | 31,65 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 |
| 🟢 591 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 |
| 🟢 592 | 24,83 | 24,83 | 24,83 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 |
| 🟡 593 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 |
| 🟡 594 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 595 | 10,83 | 10,83 | 10,83 | 14,29 | 14,29 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 596 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 |
| 🟢 600 | 26,45 | 26,45 | 33,10 | 33,10 | 42,43 | 42,43 | 42,43 | 51,93 | 51,93 | 66,02 |
| 🟢 601 | 70,04 | 70,04 | 70,04 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 602 | 29,49 | 29,49 | 29,49 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 |
| 🟢 603 | 88,45 | 88,45 | 88,45 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 604 | 18,98 | 18,98 | 18,98 | 25,86 | 25,86 | 29,84 | 29,84 | 29,84 | 29,84 | 29,84 |
| 🟢 605 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 29,70 | 29,70 | 29,70 | 29,70 | 29,70 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 608 | 18,98 | 18,98 | 18,98 | 25,86 | 25,86 | 29,84 | 29,84 | 29,84 | 29,84 | 29,84 |
| 🟢 609 | 6,04 | 6,04 | 6,04 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 17,14 | 17,14 |
| 🟢 610 | 9,01 | 9,01 | 9,01 | 15,54 | 15,54 | 15,54 | 15,54 | 15,54 | 25,80 | 25,80 |
| 🟢 611 | 6,04 | 6,04 | 6,04 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 17,14 | 17,14 |
| 🟡 612 | 14,13 | 14,13 | 14,13 | 17,53 | 17,53 | 17,53 | 17,53 | 33,92 | 33,92 | 33,92 |
| 🟡 613 | 7,10 | 7,10 | 7,10 | 11,80 | 11,80 | 11,80 | 11,80 | 11,80 | 15,50 | 15,50 |
| 🟡 614 | 8,60 | 8,60 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 615 | 14,40 | 14,40 | 14,40 | 19,01 | 19,01 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 616 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 14,32 | 14,32 | 14,32 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 620 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 7,66 | 7,66 | 7,66 | 11,48 | 11,48 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 624 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 8,72 | 8,72 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 628 | 14,33 | 14,33 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 629 | 14,33 | 14,33 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 630 | 14,33 | 14,33 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 631 | 8,72 | 8,72 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 632 | 5,62 | 5,62 | 5,62 | 5,62 | 5,62 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟢 633 | 7,85 | 7,85 | 7,85 | 7,85 | 7,85 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 |
| 🟢 634 | 8,67 | 8,67 | 8,67 | 8,67 | 8,67 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 |
| 🟢 635 | 7,73 | 7,73 | 7,73 | 7,73 | 7,73 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 |
| 🟢 636 | 2,81 | 2,81 | 2,81 | 2,81 | 2,81 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 |
| 🟢 637 | 4,84 | 4,84 | 4,84 | 5,61 | 5,61 | 6,30 | 6,30 | 6,30 | 7,31 | 7,31 |
| 🟢 638 | 13,13 | 13,13 | 13,13 | 14,35 | 14,35 | 14,35 | 14,35 | 14,35 | 15,83 | 15,83 |
| 🟢 639 | 13,13 | 13,13 | 13,13 | 14,35 | 14,35 | 14,35 | 14,35 | 14,35 | 15,83 | 15,83 |
| 🟢 640 | 14,63 | 14,63 | 14,63 | 14,63 | 14,63 | 14,63 | 14,63 | 14,63 | 16,07 | 16,07 |
| 🟢 641 | 4,84 | 4,84 | 4,84 | 5,61 | 5,61 | 6,30 | 6,30 | 6,30 | 7,31 | 7,31 |
| 🟡 642 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 17,20 | 17,20 |
| 🟢 643 | 10,63 | 10,63 | 10,63 | 13,64 | 13,64 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 644 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 16,80 | 16,80 |
| 🟢 648 | 9,38 | 9,38 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 14,66 | 19,04 | 19,04 |
| 🟢 649 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 9,38 | 9,38 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 14,66 | 19,04 | 19,04 |
| 🟢 653 | 11,80 | 11,80 | 18,75 | 18,75 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 654 | 20,95 | 20,95 | 21,17 | 21,17 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 655 | 20,95 | 20,95 | 21,17 | 21,17 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 656 | 20,95 | 20,95 | 21,17 | 21,17 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 657 | 11,80 | 11,80 | 18,75 | 18,75 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 658 | 14,51 | 14,51 | 14,51 | 19,79 | 19,79 | 19,79 | 19,79 | 39,58 | 39,58 | 39,58 |
| 🟢 659 | 14,35 | 14,35 | 14,35 | 19,57 | 19,57 | 19,57 | 19,57 | 39,14 | 39,14 | 39,14 |
| 🟢 660 | 39,51 | 39,51 | 39,51 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 |
| 🟢 661 | 39,07 | 39,07 | 39,07 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 |
| 🟢 662 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 |
| 🟢 663 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 |
| 🟢 664 | 31,00 | 31,00 | 31,00 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 |
| 🟢 665 | 30,66 | 30,66 | 30,66 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 |
| 🟢 666 | 16,54 | 16,54 | 16,54 | 22,56 | 22,56 | 22,56 | 22,56 | 45,12 | 45,12 | 45,12 |
| 🟢 667 | 45,05 | 45,05 | 45,05 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 |
| 🟢 668 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 |
| 🟢 669 | 41,06 | 41,06 | 41,06 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 |
| 🟢 670 | 17,41 | 17,41 | 17,41 | 17,98 | 17,98 | 18,21 | 18,21 | 18,21 | 18,33 | 18,33 |
| 🟢 671 | 13,72 | 13,72 | 13,72 | 14,83 | 14,83 | 15,57 | 15,57 | 15,57 | 15,95 | 15,95 |
| 🟢 672 | 12,94 | 12,94 | 12,94 | 13,36 | 13,36 | 13,54 | 13,54 | 13,54 | 13,62 | 13,62 |
| 🟢 673 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 11,57 | 11,57 | 14,23 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 18,75 | 18,75 |
| 🟢 680 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 |
| 🟢 682 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 7,57 | 7,57 | 7,57 | 9,99 | 9,99 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: **Tabela 22** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 3 de 6: 60–64 a 100–104 m³) -->
| Nº | 60–64 | 64–65 | 65–70 | 70–75 | 75–80 | 80–84 | 84–90 | 90–99 | 99–100 | 100–104 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 |
| 🟢 2 | 15,14 | 15,14 | 15,14 | 15,14 | 15,14 | 15,14 | 15,14 | 16,96 | 16,96 | 16,96 |
| 🟢 3 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 |
| 🟢 4 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 |
| 🟢 6 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 |
| 🟢 9 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 |
| 🟢 14 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 |
| 🟢 15 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 16 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 |
| 🟢 17 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 |
| 🟢 18 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 19 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 20,60 |
| 🟢 20 | 28,84 | 28,84 | 28,84 | 28,84 | 28,84 | 28,84 | 28,84 | 28,84 | 28,84 | 37,08 |
| 🟢 21 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 24,72 |
| 🟢 22 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 37,90 |
| 🟢 23 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 16,48 |
| 🟡 24 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 25 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 26 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 27 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 28 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 |
| 🟢 29 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 30 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟢 31 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 32 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 |
| 🟢 33 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 |
| 🟢 34 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 35 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 |
| 🟢 37 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 |
| 🟢 38 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 39 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟢 40 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 13,47 |
| 🟢 41 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 |
| 🟢 42 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 15,71 | 13,47 |
| 🟡 43 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 44 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 45 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 |
| 🟢 46 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 |
| 🟢 47 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 48 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 49 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 50 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 13,83 |
| 🟢 51 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 52 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 53 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 54 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 12,17 | 13,83 |
| 🟢 55 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟢 56 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 57 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 58 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 59 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 61 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 62 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 |
| 🟢 63 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 |
| 🟢 64 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 |
| 🟢 65 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 66 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,18 | 18,18 | 18,18 |
| 🟢 70 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 | 18,18 | 18,18 | 18,18 |
| 🟢 74 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 75 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 76 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 79 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 |
| 🟢 80 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 |
| 🟢 81 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 |
| 🟢 82 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 | 30,39 |
| 🟡 83 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 84 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 85 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 |
| 🟢 86 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 |
| 🟢 87 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 88 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 |
| 🟢 89 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 | 7,03 |
| 🟢 90 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,51 |
| 🟢 91 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,27 | 7,51 |
| 🟢 92 | 7,70 | 7,70 | 7,70 | 7,70 | 7,70 | 7,70 | 7,70 | 7,70 | 7,70 | 7,95 |
| 🟢 93 | 3,44 | 3,44 | 3,44 | 3,44 | 3,44 | 3,44 | 3,44 | 3,44 | 3,44 | 3,52 |
| 🟢 94 | 11,41 | 11,41 | 11,41 | 11,41 | 11,41 | 12,08 | 12,08 | 12,08 | 12,08 | 12,67 |
| 🟢 95 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 15,27 | 15,27 | 15,27 | 15,27 | 16,23 |
| 🟢 96 | 15,69 | 15,69 | 15,69 | 15,69 | 15,69 | 16,58 | 16,58 | 16,58 | 16,58 | 17,50 |
| 🟢 97 | 11,41 | 11,41 | 11,41 | 11,41 | 11,41 | 12,08 | 12,08 | 12,08 | 12,08 | 12,67 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 100 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 |
| 🟢 101 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 |
| 🟢 102 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 |
| 🟢 103 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 104 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 105 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 106 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 107 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 108 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 109 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 26,40 | 26,40 | 26,40 |
| 🟢 110 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 | 26,40 | 26,40 | 26,40 |
| 🟢 114 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 115 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 116 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 117 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 118 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 |
| 🟢 119 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 |
| 🟢 120 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 121 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 |
| 🟢 122 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 123 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 124 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 |
| 🟢 125 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 |
| 🟢 128 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 129 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 130 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 131 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 141 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 142 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 143 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 144 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 148 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 12,76 |
| 🟢 149 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 26,71 |
| 🟢 150 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 22,45 | 26,71 |
| 🟢 151 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 29,66 |
| 🟢 152 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 | 12,76 |
| 🟢 153 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 17,91 |
| 🟢 154 | 21,66 | 21,66 | 21,66 | 21,66 | 21,66 | 21,66 | 21,66 | 21,66 | 21,66 | 24,00 |
| 🟢 155 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 |
| 🟢 156 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 15,55 |
| 🟢 157 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 31,00 | 18,19 |
| 🟢 158 | 20,27 | 20,27 | 20,27 | 20,27 | 20,27 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟢 159 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 |
| 🟢 160 | 23,31 | 23,31 | 23,31 | 23,31 | 23,31 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 |
| 🟢 161 | 22,62 | 22,62 | 22,62 | 22,62 | 22,62 | 22,62 | 22,62 | 22,62 | 22,62 | 26,46 |
| 🟢 162 | 20,27 | 20,27 | 20,27 | 20,27 | 20,27 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 14,02 |
| 🟢 165 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 14,33 |
| 🟢 166 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 14,33 |
| 🟢 167 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 10,76 | 14,33 |
| 🟢 168 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 14,02 |
| 🟡 169 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 170 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 171 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 172 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 173 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 174 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 |
| 🟢 175 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 |
| 🟢 176 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 177 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 178 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟡 179 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 180 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 181 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 182 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 183 | 13,08 | 13,08 | 13,08 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟢 184 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 |
| 🟢 185 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 |
| 🟢 186 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 15,13 |
| 🟢 187 | 6,54 | 6,54 | 6,54 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 |
| 🟡 188 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 189 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 190 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 191 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 192 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 193 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 194 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 195 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 196 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 197 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 198 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 199 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 |
| 🟢 200 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 16,79 |
| 🟢 201 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 19,44 |
| 🟢 202 | 19,38 | 19,38 | 19,38 | 19,38 | 19,38 | 19,38 | 19,38 | 19,38 | 19,38 | 22,92 |
| 🟢 203 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 19,44 |
| 🟢 204 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 13,37 |
| 🟢 205 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 42,08 |
| 🟢 206 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 56,22 |
| 🟢 207 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 28,15 | 35,17 |
| 🟢 209 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 |
| 🟢 211 | 46,20 | 46,20 | 46,20 | 46,20 | 46,20 | 46,20 | 46,20 | 46,20 | 46,20 | 67,67 |
| 🟢 212 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 | 42,27 |
| 🟢 213 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 41,27 | 56,22 |
| 🟢 214 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟢 215 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 216 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 217 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 218 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 219 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 | 8,12 |
| 🟢 220 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟢 221 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 |
| 🟢 222 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 223 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟡 224 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 225 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 226 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 227 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 228 | 80,25 | 80,25 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 229 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 230 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 |
| 🟢 231 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 9,56 | 9,56 | 9,56 | 9,56 | 9,56 | 9,56 | 9,56 | 9,56 | 9,56 | 10,90 |
| 🟢 234 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 12,69 |
| 🟢 235 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 12,69 |
| 🟢 236 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 10,84 | 12,69 |
| 🟢 237 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 |
| 🟢 238 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 |
| 🟢 239 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 240 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 | 34,87 |
| 🟡 241 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 242 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 25,49 | 25,49 |
| 🟢 243 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 27,53 | 27,53 |
| 🟢 244 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 24,61 | 27,53 | 27,53 |
| 🟢 245 | 25,55 | 25,55 | 25,55 | 25,55 | 25,55 | 25,55 | 25,55 | 25,55 | 28,87 | 28,87 |
| 🟢 246 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 | 25,49 | 25,49 |
| 🟡 247 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 248 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 249 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 250 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 251 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 252 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 253 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 254 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 255 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 |
| 🟢 256 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 257 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 258 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 |
| 🟢 259 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 260 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 |
| 🟢 261 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 262 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟢 263 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 |
| 🟢 264 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 |
| 🟢 265 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 |
| 🟢 266 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 |
| 🟢 267 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟢 268 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 269 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 270 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 271 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 272 | 10,53 | 10,53 | 10,53 | 10,53 | 10,58 | 10,58 | 10,58 | 10,58 | 10,58 | 10,63 |
| 🟢 273 | 12,63 | 12,63 | 12,63 | 12,63 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,75 |
| 🟢 274 | 11,58 | 11,58 | 11,58 | 11,58 | 11,63 | 11,63 | 11,63 | 11,63 | 11,63 | 11,69 |
| 🟢 275 | 13,16 | 13,16 | 13,16 | 13,16 | 13,22 | 13,22 | 13,22 | 13,22 | 13,22 | 13,29 |
| 🟢 276 | 5,26 | 5,26 | 5,26 | 5,26 | 5,29 | 5,29 | 5,29 | 5,29 | 5,29 | 5,31 |
| 🟡 277 | 7,88 | 7,88 | 7,88 | 8,99 | 8,99 | 8,99 | 8,99 | 8,99 | 8,99 | 10,22 |
| 🟢 278 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 279 | 25,23 | 25,23 | 25,23 | 25,23 | 25,23 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 |
| 🟢 280 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 281 | 28,10 | 28,10 | 28,10 | 28,10 | 28,10 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 |
| 🟢 282 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 283 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 |
| 🟢 284 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 285 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 |
| 🟢 286 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 287 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 |
| 🟢 288 | 9,09 | 9,09 | 9,09 | 9,09 | 9,99 | 9,99 | 9,99 | 9,99 | 9,99 | 10,99 |
| 🟢 289 | 12,28 | 12,28 | 12,28 | 12,28 | 13,49 | 13,49 | 13,49 | 13,49 | 13,49 | 14,78 |
| 🟢 290 | 10,43 | 10,43 | 10,43 | 10,43 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 12,64 |
| 🟢 291 | 14,56 | 14,56 | 14,56 | 14,56 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 17,62 |
| 🟢 292 | 4,54 | 4,54 | 4,54 | 4,54 | 5,00 | 5,00 | 5,00 | 5,00 | 5,00 | 5,49 |
| 🟡 293 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 294 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 295 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 296 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 297 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 298 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 299 | 13,03 | 13,03 | 13,03 | 14,36 | 14,36 | 15,93 | 15,93 | 17,47 | 17,47 | 19,22 |
| 🟢 300 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 23,18 |
| 🟢 301 | 13,03 | 13,03 | 13,03 | 14,36 | 14,36 | 15,93 | 15,93 | 17,47 | 17,47 | 19,22 |
| 🟢 302 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 17,71 | 23,18 |
| 🟢 303 | 13,03 | 13,03 | 13,03 | 14,36 | 14,36 | 15,93 | 15,93 | 17,47 | 17,47 | 19,22 |
| 🟡 304 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 305 | 4,72 | 4,72 | 4,72 | 4,72 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 |
| 🟢 306 | 4,72 | 4,72 | 4,72 | 4,72 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 |
| 🟢 307 | 4,72 | 4,72 | 4,72 | 4,72 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 |
| 🟢 308 | 4,28 | 4,28 | 4,28 | 4,28 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 |
| 🟢 309 | 2,36 | 2,36 | 2,36 | 2,36 | 2,55 | 2,55 | 2,55 | 2,55 | 2,55 | 2,77 |
| 🟡 310 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 311 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 |
| 🟢 312 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 313 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 314 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 |
| 🟡 315 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 318 | 10,66 | 10,66 | 10,66 | 10,66 | 11,67 | 11,67 | 11,67 | 11,67 | 11,67 | 12,75 |
| 🟢 319 | 14,90 | 14,90 | 14,90 | 14,90 | 15,98 | 15,98 | 15,98 | 15,98 | 15,98 | 17,07 |
| 🟢 320 | 14,90 | 14,90 | 14,90 | 14,90 | 15,98 | 15,98 | 15,98 | 15,98 | 15,98 | 17,07 |
| 🟢 321 | 18,56 | 18,56 | 18,56 | 18,56 | 19,90 | 19,90 | 19,90 | 19,90 | 19,90 | 22,44 |
| 🟢 322 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 323 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 324 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 325 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 326 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 327 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 328 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 |
| 🟢 329 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 |
| 🟢 330 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 |
| 🟢 331 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 |
| 🟢 332 | 10,23 | 10,23 | 10,23 | 10,23 | 10,29 | 10,29 | 10,29 | 10,29 | 10,29 | 10,34 |
| 🟢 333 | 12,27 | 12,27 | 12,27 | 12,27 | 12,34 | 12,34 | 12,34 | 12,34 | 12,34 | 12,41 |
| 🟢 334 | 12,27 | 12,27 | 12,27 | 12,27 | 12,34 | 12,34 | 12,34 | 12,34 | 12,34 | 12,41 |
| 🟢 335 | 12,78 | 12,78 | 12,78 | 12,78 | 12,86 | 12,86 | 12,86 | 12,86 | 12,86 | 12,93 |
| 🟢 336 | 5,11 | 5,11 | 5,11 | 5,11 | 5,14 | 5,14 | 5,14 | 5,14 | 5,14 | 5,17 |
| 🟢 337 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 338 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 339 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 340 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 341 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 342 | 10,21 | 10,21 | 10,21 | 10,21 | 10,21 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 343 | 13,03 | 13,03 | 13,03 | 13,03 | 13,03 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 |
| 🟢 344 | 10,21 | 10,21 | 10,21 | 10,21 | 10,21 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 345 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 | 10,89 |
| 🟢 346 | 10,21 | 10,21 | 10,21 | 10,21 | 10,21 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 347 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 348 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 349 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 18,28 |
| 🟢 350 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 16,22 | 18,28 |
| 🟢 351 | 8,90 | 8,90 | 8,90 | 8,90 | 9,12 | 9,12 | 9,12 | 9,12 | 9,12 | 10,95 |
| 🟢 352 | 8,90 | 8,90 | 8,90 | 8,90 | 9,12 | 9,12 | 9,12 | 9,12 | 9,12 | 10,95 |
| 🟢 353 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 |
| 🟢 354 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 |
| 🟢 355 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 |
| 🟢 356 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 |
| 🟢 357 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 |
| 🟢 358 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟢 359 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 360 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 361 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 |
| 🟢 362 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 363 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 364 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 365 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 366 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 |
| 🟡 367 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 368 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 369 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 370 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 371 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 372 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 |
| 🟢 373 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 374 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 |
| 🟢 375 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 376 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 11,75 |
| 🟢 377 | 23,38 | 23,38 | 23,38 | 23,38 | 23,38 | 23,38 | 23,38 | 23,38 | 23,38 | 28,05 |
| 🟢 378 | 33,25 | 33,25 | 33,25 | 33,25 | 33,25 | 33,25 | 33,25 | 33,25 | 33,25 | 38,20 |
| 🟢 379 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 9,78 | 11,75 |
| 🟡 380 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 381 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 382 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 383 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 384 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 385 | 9,37 | 9,37 | 9,37 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 386 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 387 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 388 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 389 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 390 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 391 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 392 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 393 | 9,37 | 9,37 | 9,37 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 394 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 395 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 396 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 397 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 398 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 399 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 400 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 401 | 11,93 | 11,93 | 11,93 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 402 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 403 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 404 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 405 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 406 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 407 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 408 | 10,87 | 10,87 | 10,87 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟢 409 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 410 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 |
| 🟢 411 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 412 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 413 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 |
| 🟢 414 | 9,37 | 9,37 | 9,37 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 415 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 416 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 417 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 418 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 419 | 3,66 | 3,66 | 3,66 | 4,03 | 4,03 | 4,03 | 4,03 | 4,03 | 4,03 | 4,41 |
| 🟢 420 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 |
| 🟢 421 | 7,69 | 7,69 | 7,69 | 7,69 | 7,93 | 7,93 | 7,93 | 7,93 | 7,93 | 8,17 |
| 🟢 422 | 9,23 | 9,23 | 9,23 | 9,23 | 9,52 | 9,52 | 9,52 | 9,52 | 9,52 | 9,81 |
| 🟢 423 | 8,46 | 8,46 | 8,46 | 8,46 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 | 8,99 |
| 🟢 424 | 9,61 | 9,61 | 9,61 | 9,61 | 9,91 | 9,91 | 9,91 | 9,91 | 9,91 | 10,21 |
| 🟢 425 | 3,85 | 3,85 | 3,85 | 3,85 | 3,97 | 3,97 | 3,97 | 3,97 | 3,97 | 4,09 |
| 🟢 426 | 10,21 | 10,21 | 10,21 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 427 | 7,13 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 10,90 | 10,90 | 10,90 | 10,90 |
| 🟢 428 | 10,21 | 10,21 | 10,21 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 429 | 7,13 | 8,52 | 8,52 | 8,52 | 8,52 | 8,52 | 10,90 | 10,90 | 10,90 | 10,90 |
| 🟢 430 | 10,21 | 10,21 | 10,21 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 431 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 432 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 433 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 434 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 |
| 🟢 435 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 436 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 13,46 |
| 🟢 437 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 13,46 |
| 🟢 438 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 10,87 |
| 🟢 439 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 10,87 |
| 🟢 440 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 441 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 442 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 443 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 |
| 🟢 444 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 |
| 🟢 445 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 11,34 |
| 🟢 446 | 21,88 | 21,88 | 21,88 | 21,88 | 21,88 | 21,88 | 21,88 | 21,88 | 21,88 | 29,55 |
| 🟢 447 | 8,42 | 8,42 | 8,42 | 8,42 | 8,42 | 8,42 | 8,42 | 8,42 | 8,42 | 10,73 |
| 🟢 448 | 35,66 | 35,66 | 35,66 | 35,66 | 35,66 | 35,66 | 35,66 | 35,66 | 35,66 | 39,23 |
| 🟢 449 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 | 11,34 |
| 🟢 450 | 7,67 | 7,67 | 7,67 | 9,92 | 9,92 | 12,03 | 12,03 | 12,81 | 12,81 | 13,20 |
| 🟢 451 | 7,67 | 7,67 | 7,67 | 9,92 | 9,92 | 12,03 | 12,03 | 12,81 | 12,81 | 13,20 |
| 🟢 452 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 453 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 |
| 🟢 454 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 11,51 | 14,54 |
| 🟢 455 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 456 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 19,02 | 19,02 | 19,02 | 19,02 | 21,87 |
| 🟢 457 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟢 458 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 459 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 460 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 461 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟡 462 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 463 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 464 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 465 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 |
| 🟢 466 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 467 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 468 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 469 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 470 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 |
| 🟢 471 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 472 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 473 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 13,75 |
| 🟢 474 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 475 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 11,45 | 13,75 |
| 🟢 476 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 28,35 |
| 🟢 477 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 28,35 |
| 🟢 478 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 | 28,35 |
| 🟢 479 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 | 26,58 |
| 🟢 480 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 481 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 482 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 483 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 17,14 | 19,46 |
| 🟢 484 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 485 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 486 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 14,79 |
| 🟢 487 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 14,79 |
| 🟢 488 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 12,95 | 14,79 |
| 🟢 489 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 490 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 |
| 🟢 491 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 492 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 |
| 🟢 493 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 494 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 |
| 🟢 495 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 20,43 |
| 🟡 496 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 497 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 498 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 499 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 500 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 |
| 🟢 501 | 21,34 | 21,34 | 21,34 | 21,34 | 21,34 | 21,34 | 21,34 | 21,34 | 21,34 | 25,26 |
| 🟢 502 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 |
| 🟢 503 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 504 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 508 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 509 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 510 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 511 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 |
| 🟢 512 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟢 513 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 |
| 🟢 514 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 |
| 🟢 515 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 516 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 517 | 16,92 | 16,92 | 16,92 | 16,92 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 518 | 25,08 | 25,08 | 25,08 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 |
| 🟢 519 | 16,92 | 16,92 | 16,92 | 16,92 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 520 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 42,00 | 49,82 |
| 🟢 521 | 16,92 | 16,92 | 16,92 | 16,92 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 522 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 523 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 524 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 11,75 |
| 🟢 525 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 13,35 |
| 🟢 526 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 13,35 |
| 🟢 527 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 | 9,96 |
| 🟢 528 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 529 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 530 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 531 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 532 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 533 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 534 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 535 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 536 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 537 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 538 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 539 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 540 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 541 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 |
| 🟢 542 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 |
| 🟢 543 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 |
| 🟢 544 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 |
| 🟢 545 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 |
| 🟢 546 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 |
| 🟢 547 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 548 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 549 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 550 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 551 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 552 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 553 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 554 | 20,81 | 20,81 | 20,81 | 20,81 | 20,81 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 555 | 20,81 | 20,81 | 20,81 | 20,81 | 20,81 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 556 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 | 14,59 |
| 🟢 557 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 558 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 |
| 🟢 559 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 |
| 🟢 560 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 |
| 🟢 561 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 562 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 563 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 566 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 567 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 572 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,96 | 13,96 | 13,96 |
| 🟢 577 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,96 | 13,96 | 13,96 |
| 🟢 581 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 582 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 586 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 590 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 |
| 🟢 591 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 |
| 🟢 592 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 | 28,53 |
| 🟡 593 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 594 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 595 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 596 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 600 | 66,02 | 66,02 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟢 601 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 602 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 |
| 🟢 603 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 604 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 605 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 608 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 609 | 17,14 | 17,14 | 17,14 | 20,95 | 20,95 | 20,95 | 20,95 | 20,95 | 20,95 | 26,16 |
| 🟢 610 | 25,80 | 25,80 | 25,80 | 31,05 | 31,05 | 31,05 | 31,05 | 31,05 | 31,05 | 39,07 |
| 🟢 611 | 17,14 | 17,14 | 17,14 | 20,95 | 20,95 | 20,95 | 20,95 | 20,95 | 20,95 | 26,16 |
| 🟡 612 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 613 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 614 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 615 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 616 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 620 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 624 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 628 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 629 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 630 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 631 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 632 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟢 633 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 | 7,92 | 7,99 |
| 🟢 634 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 | 8,77 | 8,80 |
| 🟢 635 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 | 8,00 | 8,40 |
| 🟢 636 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 |
| 🟢 637 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 10,03 |
| 🟢 638 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 17,37 |
| 🟢 639 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 15,83 | 17,37 |
| 🟢 640 | 16,07 | 16,07 | 16,07 | 16,07 | 16,07 | 16,07 | 16,07 | 16,07 | 16,07 | 17,63 |
| 🟢 641 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 10,03 |
| 🟡 642 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 643 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 644 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 648 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 649 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 653 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 654 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 655 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 656 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 657 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 658 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 |
| 🟢 659 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 |
| 🟢 660 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 |
| 🟢 661 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 |
| 🟢 662 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 |
| 🟢 663 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 |
| 🟢 664 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 | 35,62 |
| 🟢 665 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 | 35,22 |
| 🟢 666 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟢 667 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 |
| 🟢 668 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 |
| 🟢 669 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 |
| 🟢 670 | 18,33 | 18,33 | 18,33 | 18,33 | 18,33 | 18,33 | 18,33 | 18,44 | 18,44 | 18,44 |
| 🟢 671 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 16,01 | 16,01 | 16,01 |
| 🟢 672 | 13,62 | 13,62 | 13,62 | 13,62 | 13,62 | 13,62 | 13,62 | 13,70 | 13,70 | 13,70 |
| 🟢 673 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 |
| 🟢 680 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 |
| 🟢 682 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: **Tabela 23** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 4 de 6: 104–120 a 400–500 m³) -->
| Nº | 104–120 | 120–130 | 130–150 | 150–180 | 180–200 | 200–240 | 240–250 | 250–300 | 300–400 | 400–500 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 2 | 16,96 | 16,96 | 16,96 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 |
| 🟢 3 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 4 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 |
| 🟢 6 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 |
| 🟢 9 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 14 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 15 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 16 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 |
| 🟢 17 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 |
| 🟢 18 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 19 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟢 20 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 |
| 🟢 21 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 |
| 🟢 22 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 |
| 🟢 23 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 |
| 🟡 24 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 25 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 26 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 27 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 28 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 |
| 🟢 29 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 30 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟢 31 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 32 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 |
| 🟢 33 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 |
| 🟢 34 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 35 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 |
| 🟢 37 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 |
| 🟢 38 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 39 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟢 40 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟢 41 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 |
| 🟢 42 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟡 43 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 44 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 45 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 |
| 🟢 46 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 |
| 🟢 47 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 48 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 49 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 50 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 51 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 52 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 53 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 54 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 55 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟢 56 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 57 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 58 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 59 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 61 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 62 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 |
| 🟢 63 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 |
| 🟢 64 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 |
| 🟢 65 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 66 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 18,18 | 18,18 | 18,18 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 70 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 18,18 | 18,18 | 18,18 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 74 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 75 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 76 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 79 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 |
| 🟢 80 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 |
| 🟢 81 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 |
| 🟢 82 | 30,39 | 30,39 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 |
| 🟡 83 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 84 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 85 | 10,45 | 10,45 | 10,45 | 10,45 | 10,45 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 86 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 |
| 🟢 87 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 88 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 |
| 🟢 89 | 7,03 | 7,03 | 7,03 | 7,03 | 7,03 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 |
| 🟢 90 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 91 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 92 | 7,95 | 7,95 | 7,95 | 7,95 | 7,95 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 93 | 3,52 | 3,52 | 3,52 | 3,52 | 3,52 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 |
| 🟢 94 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 95 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 96 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 97 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 100 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 |
| 🟢 101 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 |
| 🟢 102 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 |
| 🟢 103 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 104 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 105 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 106 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 107 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 108 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 109 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 110 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 114 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 115 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 116 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 117 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 118 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 119 | 15,51 | 15,51 | 15,51 | 15,51 | 15,51 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 120 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 121 | 16,33 | 16,33 | 16,33 | 16,33 | 16,33 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 122 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 123 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 124 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 |
| 🟢 125 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 |
| 🟢 128 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 129 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 130 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 131 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 141 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 142 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 143 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 144 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 148 | 12,76 | 12,76 | 12,76 | 12,76 | 12,76 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 149 | 26,71 | 26,71 | 26,71 | 26,71 | 26,71 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 150 | 26,71 | 26,71 | 26,71 | 26,71 | 26,71 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 151 | 29,66 | 29,66 | 29,66 | 29,66 | 29,66 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 |
| 🟢 152 | 12,76 | 12,76 | 12,76 | 12,76 | 12,76 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 153 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 |
| 🟢 154 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 |
| 🟢 155 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 | 28,48 |
| 🟢 156 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 |
| 🟢 157 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 158 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟢 159 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 |
| 🟢 160 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 |
| 🟢 161 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 | 26,46 |
| 🟢 162 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟢 165 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 166 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 167 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 | 14,33 |
| 🟢 168 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟡 169 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 170 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 171 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 172 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 173 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 174 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 |
| 🟢 175 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 |
| 🟢 176 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 177 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 178 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟡 179 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 180 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 181 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 182 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 183 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟢 184 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 |
| 🟢 185 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 |
| 🟢 186 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 |
| 🟢 187 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 |
| 🟡 188 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 189 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 190 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 191 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 192 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 193 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 194 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 195 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 196 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 197 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 198 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 199 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 |
| 🟢 200 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 |
| 🟢 201 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 202 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 |
| 🟢 203 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 204 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 |
| 🟢 205 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 |
| 🟢 206 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 207 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 |
| 🟢 209 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 |
| 🟢 211 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 |
| 🟢 212 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 213 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 214 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟢 215 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 216 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 217 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 218 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 219 | 8,12 | 8,12 | 8,12 | 8,12 | 8,12 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 220 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟢 221 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 |
| 🟢 222 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 223 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟡 224 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 225 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 226 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 227 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 228 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 229 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 230 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 |
| 🟢 231 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 |
| 🟢 234 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 235 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 236 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 237 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 |
| 🟢 238 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 |
| 🟢 239 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 240 | 34,87 | 34,87 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 |
| 🟡 241 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 242 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟢 243 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 244 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 245 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 |
| 🟢 246 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟡 247 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 248 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 249 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 250 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 251 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 252 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 253 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 254 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 255 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 |
| 🟢 256 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 257 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 258 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 |
| 🟢 259 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 260 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 |
| 🟢 261 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 262 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟢 263 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 |
| 🟢 264 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 |
| 🟢 265 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 |
| 🟢 266 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 |
| 🟢 267 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟢 268 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 269 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 270 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 271 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 272 | 10,63 | 10,63 | 10,63 | 10,63 | 10,63 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 |
| 🟢 273 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 |
| 🟢 274 | 11,69 | 11,69 | 11,69 | 11,69 | 11,69 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 275 | 13,29 | 13,29 | 13,29 | 13,29 | 13,29 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 276 | 5,31 | 5,31 | 5,31 | 5,31 | 5,31 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 |
| 🟡 277 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 |
| 🟢 278 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 279 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 |
| 🟢 280 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 281 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 |
| 🟢 282 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 283 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 |
| 🟢 284 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 285 | 6,99 | 6,99 | 6,99 | 6,99 | 6,99 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 286 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 287 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 |
| 🟢 288 | 10,99 | 10,99 | 10,99 | 10,99 | 10,99 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 |
| 🟢 289 | 14,78 | 14,78 | 14,78 | 14,78 | 14,78 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 |
| 🟢 290 | 12,64 | 12,64 | 12,64 | 12,64 | 12,64 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 |
| 🟢 291 | 17,62 | 17,62 | 17,62 | 17,62 | 17,62 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 |
| 🟢 292 | 5,49 | 5,49 | 5,49 | 5,49 | 5,49 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 293 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 294 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 295 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 296 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 297 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 298 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 299 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 300 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 301 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 302 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 303 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟡 304 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 305 | 5,54 | 5,54 | 5,54 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 306 | 5,54 | 5,54 | 5,54 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 307 | 5,54 | 5,54 | 5,54 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 308 | 5,54 | 5,54 | 5,54 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 309 | 2,77 | 2,77 | 2,77 | 2,77 | 2,77 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 |
| 🟡 310 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 311 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 |
| 🟢 312 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 313 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 314 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 |
| 🟡 315 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 318 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 |
| 🟢 319 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 18,43 | 18,43 | 18,43 |
| 🟢 320 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 17,07 | 18,43 | 18,43 | 18,43 |
| 🟢 321 | 22,44 | 22,44 | 22,44 | 22,44 | 22,44 | 22,44 | 22,44 | 25,98 | 25,98 | 25,98 |
| 🟢 322 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 323 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 324 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 325 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 326 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 327 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 328 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 329 | 4,52 | 4,52 | 4,52 | 4,52 | 4,52 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 |
| 🟢 330 | 5,06 | 5,06 | 5,06 | 5,06 | 5,06 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 331 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 |
| 🟢 332 | 10,34 | 10,34 | 10,34 | 10,34 | 10,34 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 |
| 🟢 333 | 12,41 | 12,41 | 12,41 | 12,41 | 12,41 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 334 | 12,41 | 12,41 | 12,41 | 12,41 | 12,41 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 335 | 12,93 | 12,93 | 12,93 | 12,93 | 12,93 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 336 | 5,17 | 5,17 | 5,17 | 5,17 | 5,17 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 |
| 🟢 337 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 338 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 339 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 340 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 341 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 342 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 343 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 |
| 🟢 344 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 345 | 10,89 | 13,47 | 13,47 | 13,47 | 15,28 | 15,28 | 23,05 | 23,05 | 23,05 | 23,05 |
| 🟢 346 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 347 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 348 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 349 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 350 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 351 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 13,13 | 13,13 | 13,13 | 15,75 | 15,75 |
| 🟢 352 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 13,13 | 13,13 | 13,13 | 15,75 | 15,75 |
| 🟢 353 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 |
| 🟢 354 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 |
| 🟢 355 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 |
| 🟢 356 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 |
| 🟢 357 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 |
| 🟢 358 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟢 359 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 360 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 361 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 |
| 🟢 362 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 363 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 364 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 365 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 366 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,95 | 10,95 |
| 🟡 367 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 368 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 369 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 370 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 371 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 372 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 |
| 🟢 373 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 374 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 |
| 🟢 375 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 376 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 377 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 |
| 🟢 378 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 |
| 🟢 379 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟡 380 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 381 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 382 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 383 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 384 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 385 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 386 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 387 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 388 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 389 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 390 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 391 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 392 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 393 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 394 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 395 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 396 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 397 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 398 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 399 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 400 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 401 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 402 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 403 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 404 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 405 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 406 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 407 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 408 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟢 409 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 410 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 |
| 🟢 411 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 412 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 413 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 |
| 🟢 414 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 415 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 416 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 417 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 418 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 419 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 |
| 🟢 420 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 |
| 🟢 421 | 8,17 | 8,17 | 8,17 | 8,17 | 8,17 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 |
| 🟢 422 | 9,81 | 9,81 | 9,81 | 9,81 | 9,81 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 |
| 🟢 423 | 8,99 | 8,99 | 8,99 | 8,99 | 8,99 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 |
| 🟢 424 | 10,21 | 10,21 | 10,21 | 10,21 | 10,21 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 |
| 🟢 425 | 4,09 | 4,09 | 4,09 | 4,09 | 4,09 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 |
| 🟢 426 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 427 | 14,95 | 14,95 | 14,95 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 428 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 429 | 14,95 | 14,95 | 14,95 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 430 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 431 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 432 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 433 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 434 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 |
| 🟢 435 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 436 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 437 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 438 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 439 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 440 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 441 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 442 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 443 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 |
| 🟢 444 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 |
| 🟢 445 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 |
| 🟢 446 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 | 29,55 |
| 🟢 447 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 | 10,73 |
| 🟢 448 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 | 39,23 |
| 🟢 449 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 | 11,34 |
| 🟢 450 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 451 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 452 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 453 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 |
| 🟢 454 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 | 14,54 |
| 🟢 455 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 456 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 |
| 🟢 457 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟢 458 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 459 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 460 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 461 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟡 462 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 463 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 464 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 465 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 |
| 🟢 466 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 467 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 468 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 469 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 470 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 | 9,14 |
| 🟢 471 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 472 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 473 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 474 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 475 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 476 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 477 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 478 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 479 | 26,58 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 |
| 🟢 480 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 481 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 482 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 483 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 |
| 🟢 484 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 485 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 486 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 487 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 488 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 489 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 490 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 |
| 🟢 491 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 492 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 |
| 🟢 493 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 494 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 |
| 🟢 495 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 |
| 🟡 496 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 497 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 498 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 499 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 500 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 |
| 🟢 501 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 |
| 🟢 502 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 |
| 🟢 503 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 504 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 508 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 509 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 510 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 511 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 |
| 🟢 512 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟢 513 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 |
| 🟢 514 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 |
| 🟢 515 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 516 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 517 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 518 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 |
| 🟢 519 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 520 | 49,82 | 49,82 | 49,82 | 49,82 | 49,82 | 49,82 | 49,82 | 53,81 | 53,81 | 53,81 |
| 🟢 521 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 522 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 523 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 524 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 525 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 10,10 | 10,10 | 10,10 | 10,10 | 8,78 |
| 🟢 526 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 527 | 9,96 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 |
| 🟢 528 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 529 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 530 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 531 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 532 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 533 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 534 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 535 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 536 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 537 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 538 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 539 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 540 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 541 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 |
| 🟢 542 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 |
| 🟢 543 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 |
| 🟢 544 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 |
| 🟢 545 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 |
| 🟢 546 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 |
| 🟢 547 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 548 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 549 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 550 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 551 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 552 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 553 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 554 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 555 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 556 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 |
| 🟢 557 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 558 | 18,31 | 18,31 | 18,31 | 18,31 | 18,31 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 |
| 🟢 559 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 560 | 22,85 | 22,85 | 22,85 | 22,85 | 22,85 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 561 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 562 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 563 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 566 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 567 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 572 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 13,96 | 13,96 | 13,96 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 577 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 13,96 | 13,96 | 13,96 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 581 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 582 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 586 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 590 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 |
| 🟢 591 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 |
| 🟢 592 | 28,53 | 28,53 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 |
| 🟡 593 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 594 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 595 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 596 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 600 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟢 601 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 602 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 |
| 🟢 603 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 604 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 605 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 608 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 609 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟢 610 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 |
| 🟢 611 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟡 612 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 613 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 614 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 615 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 616 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 620 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 624 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 628 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 629 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 630 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 631 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 632 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟢 633 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 |
| 🟢 634 | 8,80 | 8,80 | 8,80 | 8,80 | 8,80 | 8,80 | 8,80 | 8,80 | 8,88 | 8,88 |
| 🟢 635 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 | 8,40 |
| 🟢 636 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 |
| 🟢 637 | 10,03 | 10,03 | 10,03 | 10,03 | 10,03 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 638 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 639 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 640 | 17,63 | 17,63 | 17,63 | 17,63 | 17,63 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 641 | 10,03 | 10,03 | 10,03 | 10,03 | 10,03 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟡 642 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 643 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 644 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 648 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 649 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 653 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 654 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 655 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 656 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 657 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 658 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 |
| 🟢 659 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 |
| 🟢 660 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 |
| 🟢 661 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 |
| 🟢 662 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 |
| 🟢 663 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 |
| 🟢 664 | 35,62 | 35,62 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 |
| 🟢 665 | 35,22 | 35,22 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 |
| 🟢 666 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟢 667 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 |
| 🟢 668 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 |
| 🟢 669 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 |
| 🟢 670 | 18,44 | 18,44 | 18,44 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 |
| 🟢 671 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 |
| 🟢 672 | 13,70 | 13,70 | 13,70 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 |
| 🟢 673 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 |
| 🟢 680 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 |
| 🟢 682 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: **Tabela 24** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 5 de 6: 500–600 a 15.000–20.000 m³) -->
| Nº | 500–600 | 600–750 | 750–1.000 | 1.000–2.500 | 2.500–3.000 | 3.000–5.000 | 5.000–7.500 | 7.500–10.000 | 10.000–15.000 | 15.000–20.000 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 2 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 |
| 🟢 3 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 4 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 | 22,70 |
| 🟢 6 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 | 29,13 |
| 🟢 9 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 14 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 15 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 16 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 | 16,32 |
| 🟢 17 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 | 17,26 |
| 🟢 18 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 19 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟢 20 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 | 37,08 |
| 🟢 21 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 | 24,72 |
| 🟢 22 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 | 37,90 |
| 🟢 23 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 | 16,48 |
| 🟡 24 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 25 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 26 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 27 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 28 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 | 19,52 |
| 🟢 29 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 30 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟢 31 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 32 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 | 17,77 |
| 🟢 33 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 | 19,00 |
| 🟢 34 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 35 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 | 17,04 |
| 🟢 37 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 | 23,12 |
| 🟢 38 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 39 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟢 40 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟢 41 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 | 19,56 |
| 🟢 42 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟡 43 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 44 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 45 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 | 18,18 |
| 🟢 46 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 | 26,66 |
| 🟢 47 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 48 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 49 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 50 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 51 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 52 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 53 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 54 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 55 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟢 56 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 57 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 58 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 59 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 61 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 62 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 | 26,93 |
| 🟢 63 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 | 23,66 |
| 🟢 64 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 | 27,68 |
| 🟢 65 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 66 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 70 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 74 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 75 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 76 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 79 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 | 45,03 |
| 🟢 80 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 | 36,02 |
| 🟢 81 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 | 16,44 |
| 🟢 82 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 | 32,08 |
| 🟡 83 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 84 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 85 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 86 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 | 7,43 |
| 🟢 87 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 88 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 | 6,03 |
| 🟢 89 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 | 7,28 |
| 🟢 90 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 91 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 92 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 93 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 |
| 🟢 94 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 95 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 96 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 97 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 100 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 | 14,05 |
| 🟢 101 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 | 10,53 |
| 🟢 102 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 | 16,86 |
| 🟢 103 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 104 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 105 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 106 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 107 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 108 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 109 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 110 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 114 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 115 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 116 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 117 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 118 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 119 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 120 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 121 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 122 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 123 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 124 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 | 13,91 |
| 🟢 125 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 | 16,75 |
| 🟢 128 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 129 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 130 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 131 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 141 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 142 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 143 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 144 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 148 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 149 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 150 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 151 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 | 34,98 |
| 🟢 152 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 153 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 |
| 🟢 154 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 | 24,00 |
| 🟢 155 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 | 30,56 |
| 🟢 156 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 |
| 🟢 157 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 158 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟢 159 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 | 24,53 |
| 🟢 160 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 | 26,91 |
| 🟢 161 | 29,59 | 29,59 | 29,59 | 29,59 | 29,59 | 29,59 | 29,59 | 29,59 | 32,21 | 32,21 |
| 🟢 162 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟢 165 | 14,57 | 14,57 | 14,57 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 166 | 14,57 | 14,57 | 14,57 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 167 | 14,57 | 14,57 | 14,57 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 168 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟡 169 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 170 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 171 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 172 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 173 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 174 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 | 6,39 |
| 🟢 175 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 | 5,80 |
| 🟢 176 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 177 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 178 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟡 179 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 180 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 181 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 182 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 183 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟢 184 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 | 13,53 |
| 🟢 185 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 | 11,68 |
| 🟢 186 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 | 15,13 |
| 🟢 187 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 | 7,31 |
| 🟡 188 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 189 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 190 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 191 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 192 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 193 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 194 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 195 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 196 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 197 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 198 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 199 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 | 19,79 |
| 🟢 200 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 |
| 🟢 201 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 202 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 | 22,92 |
| 🟢 203 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 204 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 | 13,37 |
| 🟢 205 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 |
| 🟢 206 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 207 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 | 35,17 |
| 🟢 209 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 | 25,17 |
| 🟢 211 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 | 67,67 |
| 🟢 212 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 213 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 214 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟢 215 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 216 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 217 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 218 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 219 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 220 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟢 221 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 | 19,67 |
| 🟢 222 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 223 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟡 224 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 225 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 226 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 227 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 228 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 229 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 230 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 | 55,80 |
| 🟢 231 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 | 10,90 |
| 🟢 234 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 235 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 236 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 237 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 | 51,66 |
| 🟢 238 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 | 41,32 |
| 🟢 239 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 240 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 | 36,80 |
| 🟡 241 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 242 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟢 243 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 244 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 245 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 | 28,87 |
| 🟢 246 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟡 247 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 248 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 249 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 250 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 251 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 252 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 253 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 254 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 255 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 | 27,84 |
| 🟢 256 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 257 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 258 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 | 53,41 |
| 🟢 259 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 260 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 | 19,49 |
| 🟢 261 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 262 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟢 263 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 |
| 🟢 264 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 | 8,29 |
| 🟢 265 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 | 9,88 |
| 🟢 266 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 | 1,30 |
| 🟢 267 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟢 268 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 269 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 270 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 271 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 272 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 | 10,68 |
| 🟢 273 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 | 12,82 |
| 🟢 274 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 275 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 276 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 | 5,34 |
| 🟡 277 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 |
| 🟢 278 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 279 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 | 33,63 |
| 🟢 280 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 281 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 | 35,49 |
| 🟢 282 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 283 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 | 12,37 |
| 🟢 284 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 285 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 286 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 287 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 | 6,16 |
| 🟢 288 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 | 12,09 |
| 🟢 289 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 | 16,35 |
| 🟢 290 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 | 13,93 |
| 🟢 291 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 | 19,35 |
| 🟢 292 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 293 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 294 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 295 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 296 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 297 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 298 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 299 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 300 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 301 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 302 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 303 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟡 304 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 305 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 306 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 307 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 308 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 309 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 | 2,86 |
| 🟡 310 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 311 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 | 5,19 |
| 🟢 312 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 313 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 314 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 | 7,96 |
| 🟡 315 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 318 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 |
| 🟢 319 | 19,91 | 19,91 | 21,50 | 23,21 | 25,07 | 25,07 | 27,08 | 29,26 | 31,58 | 34,11 |
| 🟢 320 | 19,91 | 19,91 | 21,50 | 23,21 | 25,07 | 25,07 | 27,08 | 29,26 | 31,58 | 34,11 |
| 🟢 321 | 28,05 | 28,05 | 30,30 | 32,72 | 35,34 | 35,34 | 38,17 | 41,23 | 44,53 | 48,08 |
| 🟢 322 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 323 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 324 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 325 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 326 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 327 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 328 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 329 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 | 5,83 |
| 🟢 330 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 331 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 | 3,96 |
| 🟢 332 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 | 10,40 |
| 🟢 333 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 334 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 335 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 336 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 |
| 🟢 337 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 338 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 339 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 340 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 341 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 342 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 343 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 | 17,47 |
| 🟢 344 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 345 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 | 23,05 |
| 🟢 346 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 347 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 348 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 349 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 350 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 351 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 352 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 353 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 | 15,01 |
| 🟢 354 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 | 26,94 |
| 🟢 355 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 | 4,05 |
| 🟢 356 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 | 33,57 |
| 🟢 357 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 | 4,51 |
| 🟢 358 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟢 359 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 360 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 361 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 | 14,19 |
| 🟢 362 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 363 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 364 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 365 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 366 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 | 10,95 |
| 🟡 367 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 368 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 369 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 370 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 371 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 372 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 | 20,20 |
| 🟢 373 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 374 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 | 23,58 |
| 🟢 375 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 376 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 377 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 | 28,05 |
| 🟢 378 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 | 38,20 |
| 🟢 379 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟡 380 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 381 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 382 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 383 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 384 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 385 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 386 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 387 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 388 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 389 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 390 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 391 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 392 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 393 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 394 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 395 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 396 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 397 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 398 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 399 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 400 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 401 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 402 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 403 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 404 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 405 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 406 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 407 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 408 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟢 409 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 410 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 | 12,26 |
| 🟢 411 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 412 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 413 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 | 6,33 |
| 🟢 414 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 415 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 416 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 417 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 418 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 419 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 | 4,41 |
| 🟢 420 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 | 1,46 |
| 🟢 421 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 | 8,41 |
| 🟢 422 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 | 10,10 |
| 🟢 423 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 | 9,25 |
| 🟢 424 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 | 10,52 |
| 🟢 425 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 | 4,21 |
| 🟢 426 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 427 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 25,51 | 26,91 |
| 🟢 428 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 429 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 24,09 | 25,51 | 26,91 |
| 🟢 430 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 431 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 432 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 433 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 434 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 | 21,41 |
| 🟢 435 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 436 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 437 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 438 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 439 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 440 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 441 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 442 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 443 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 | 23,91 |
| 🟢 444 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 | 5,64 |
| 🟢 445 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 26,39 | 26,39 | 26,39 | 26,39 |
| 🟢 446 | 38,40 | 38,40 | 38,40 | 38,40 | 38,40 | 38,40 | 47,97 | 47,97 | 47,97 | 47,97 |
| 🟢 447 | 13,39 | 13,39 | 13,39 | 13,39 | 13,39 | 13,39 | 16,45 | 16,45 | 16,45 | 16,45 |
| 🟢 448 | 43,14 | 43,14 | 43,14 | 43,14 | 43,14 | 43,14 | 47,46 | 47,46 | 47,46 | 47,46 |
| 🟢 449 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 17,02 | 26,39 | 26,39 | 26,39 | 26,39 |
| 🟢 450 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 451 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 452 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 453 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 | 11,24 |
| 🟢 454 | 16,83 | 16,83 | 16,83 | 21,33 | 21,33 | 21,33 | 21,33 | 21,33 | 21,33 | 21,33 |
| 🟢 455 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 456 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 |
| 🟢 457 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟢 458 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 459 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 460 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 461 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟡 462 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 463 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 464 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 465 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 | 19,78 |
| 🟢 466 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 467 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 468 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 469 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 470 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 471 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 472 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 473 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 474 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 475 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 476 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 477 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 478 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 479 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 | 31,16 |
| 🟢 480 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 481 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 482 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 483 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 | 19,46 |
| 🟢 484 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 485 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 486 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 487 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 488 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 489 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 490 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 | 24,69 |
| 🟢 491 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 492 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 | 28,56 |
| 🟢 493 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 494 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 | 10,07 |
| 🟢 495 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 | 20,43 |
| 🟡 496 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 497 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 498 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 499 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 500 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 | 8,68 |
| 🟢 501 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 | 25,26 |
| 🟢 502 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 | 10,83 |
| 🟢 503 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 504 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 508 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 509 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 510 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 511 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 | 9,06 |
| 🟢 512 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟢 513 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 | 11,81 |
| 🟢 514 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 | 10,86 |
| 🟢 515 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 516 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 517 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 518 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 | 30,22 |
| 🟢 519 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 520 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 | 53,81 |
| 🟢 521 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 522 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 523 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 524 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 525 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 | 8,78 |
| 🟢 526 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 527 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 | 6,11 | 5,26 | 5,26 | 5,26 | 5,26 |
| 🟢 528 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 529 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 530 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 531 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 532 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 533 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 534 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 535 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 536 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 537 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 538 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 539 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 540 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 541 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 | 21,35 |
| 🟢 542 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 | 17,76 |
| 🟢 543 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 | 38,58 |
| 🟢 544 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 | 36,01 |
| 🟢 545 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 | 28,09 |
| 🟢 546 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 | 26,36 |
| 🟢 547 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 548 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 549 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 550 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 551 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 552 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 553 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 554 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 555 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 556 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 |
| 🟢 557 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 558 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 | 27,43 |
| 🟢 559 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 560 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 561 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 562 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 563 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 9,87 | 7,94 | 7,94 | 7,22 | 7,22 |
| 🟢 566 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 567 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 572 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 577 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 581 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 582 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 586 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 590 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 | 33,81 |
| 🟢 591 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 | 15,43 |
| 🟢 592 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 | 30,12 |
| 🟡 593 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 594 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 595 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 596 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 600 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟢 601 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 602 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 | 46,01 |
| 🟢 603 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 604 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 605 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 608 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 609 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟢 610 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 | 39,07 |
| 🟢 611 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟡 612 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 613 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 614 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 615 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 616 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 620 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 624 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 628 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 629 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 630 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 631 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 632 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟢 633 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 | 7,99 |
| 🟢 634 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 | 8,88 |
| 🟢 635 | 8,40 | 8,51 | 8,51 | 8,51 | 8,51 | 8,51 | 8,51 | 8,51 | 8,51 | 8,51 |
| 🟢 636 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 | 5,18 |
| 🟢 637 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 638 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 639 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 640 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 641 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟡 642 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 643 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 644 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 648 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 649 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 653 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 654 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 655 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 656 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 657 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 658 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 | 52,77 |
| 🟢 659 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 | 52,18 |
| 🟢 660 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 | 42,22 |
| 🟢 661 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 | 41,75 |
| 🟢 662 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 | 19,26 |
| 🟢 663 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 | 19,05 |
| 🟢 664 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 | 37,60 |
| 🟢 665 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 | 37,18 |
| 🟢 666 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟢 667 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 | 48,13 |
| 🟢 668 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 | 21,96 |
| 🟢 669 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 | 48,05 |
| 🟢 670 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 |
| 🟢 671 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 |
| 🟢 672 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 |
| 🟢 673 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 | 18,75 |
| 🟢 680 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 | 41,78 |
| 🟢 682 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: **Tabela 25** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 6 de 6: 20.000–30.000 a 120.000 m³) -->
| Nº | 20.000–30.000 | 30.000–60.000 | 60.000–120.000 | > 120.000 |
| ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 2 | 19,88 | 19,88 | 19,88 | 19,88 |
| 🟢 3 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 4 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 5 | 22,70 | 22,70 | 22,70 | 22,70 |
| 🟢 6 | 28,11 | 28,11 | 28,11 | 28,11 |
| 🟢 7 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 8 | 29,13 | 29,13 | 29,13 | 29,13 |
| 🟢 9 | 38,39 | 38,39 | 38,39 | 38,39 |
| 🟢 10 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 11 | 27,85 | 27,85 | 27,85 | 27,85 |
| 🟢 12 | 36,29 | 36,29 | 36,29 | 36,29 |
| 🟢 13 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 14 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 15 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 16 | 16,32 | 16,32 | 16,32 | 16,32 |
| 🟢 17 | 17,26 | 17,26 | 17,26 | 17,26 |
| 🟢 18 | 18,16 | 18,16 | 18,16 | 18,16 |
| 🟢 19 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟢 20 | 37,08 | 37,08 | 37,08 | 37,08 |
| 🟢 21 | 24,72 | 24,72 | 24,72 | 24,72 |
| 🟢 22 | 37,90 | 37,90 | 37,90 | 37,90 |
| 🟢 23 | 16,48 | 16,48 | 16,48 | 16,48 |
| 🟡 24 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 25 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 26 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 27 | 15,18 | 15,18 | 15,18 | 15,18 |
| 🟢 28 | 19,52 | 19,52 | 19,52 | 19,52 |
| 🟢 29 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 30 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟢 31 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 32 | 17,77 | 17,77 | 17,77 | 17,77 |
| 🟢 33 | 19,00 | 19,00 | 19,00 | 19,00 |
| 🟢 34 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 35 | 20,69 | 20,69 | 20,69 | 20,69 |
| 🟢 36 | 17,04 | 17,04 | 17,04 | 17,04 |
| 🟢 37 | 23,12 | 23,12 | 23,12 | 23,12 |
| 🟢 38 | 28,57 | 28,57 | 28,57 | 28,57 |
| 🟢 39 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟢 40 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟢 41 | 19,56 | 19,56 | 19,56 | 19,56 |
| 🟢 42 | 13,47 | 13,47 | 13,47 | 13,47 |
| 🟡 43 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 44 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 45 | 18,18 | 18,18 | 18,18 | 18,18 |
| 🟢 46 | 26,66 | 26,66 | 26,66 | 26,66 |
| 🟢 47 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 48 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟢 49 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 50 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 51 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 52 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 53 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 54 | 13,83 | 13,83 | 13,83 | 13,83 |
| 🟢 55 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟢 56 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 57 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 58 | 20,92 | 20,92 | 20,92 | 20,92 |
| 🟢 59 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 61 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 62 | 26,93 | 26,93 | 26,93 | 26,93 |
| 🟢 63 | 23,66 | 23,66 | 23,66 | 23,66 |
| 🟢 64 | 27,68 | 27,68 | 27,68 | 27,68 |
| 🟢 65 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 66 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 67 | 18,64 | 18,64 | 18,64 | 18,64 |
| 🟢 68 | 18,87 | 18,87 | 18,87 | 18,87 |
| 🟢 69 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 70 | 26,75 | 26,75 | 26,75 | 26,75 |
| 🟢 71 | 36,53 | 36,53 | 36,53 | 36,53 |
| 🟢 72 | 34,54 | 34,54 | 34,54 | 34,54 |
| 🟢 73 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 74 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 75 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 76 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 77 | 19,14 | 19,14 | 19,14 | 19,14 |
| 🟢 78 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟢 79 | 45,03 | 45,03 | 45,03 | 45,03 |
| 🟢 80 | 36,02 | 36,02 | 36,02 | 36,02 |
| 🟢 81 | 16,44 | 16,44 | 16,44 | 16,44 |
| 🟢 82 | 32,08 | 32,08 | 32,08 | 32,08 |
| 🟡 83 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 84 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 85 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 86 | 7,43 | 7,43 | 7,43 | 7,43 |
| 🟢 87 | 11,65 | 11,65 | 11,65 | 11,65 |
| 🟢 88 | 6,03 | 6,03 | 6,03 | 6,03 |
| 🟢 89 | 7,28 | 7,28 | 7,28 | 7,28 |
| 🟢 90 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 91 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 92 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 93 | 3,64 | 3,64 | 3,64 | 3,64 |
| 🟢 94 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 95 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 96 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 97 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 98 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟢 99 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 100 | 14,05 | 14,05 | 14,05 | 14,05 |
| 🟢 101 | 10,53 | 10,53 | 10,53 | 10,53 |
| 🟢 102 | 16,86 | 16,86 | 16,86 | 16,86 |
| 🟢 103 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 104 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 105 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 106 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 107 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 108 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 109 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 110 | 18,02 | 18,02 | 18,02 | 18,02 |
| 🟢 111 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 112 | 24,14 | 24,14 | 24,14 | 24,14 |
| 🟢 113 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 114 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 115 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟢 116 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 117 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 118 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 119 | 18,24 | 18,24 | 18,24 | 18,24 |
| 🟢 120 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 121 | 19,21 | 19,21 | 19,21 | 19,21 |
| 🟢 122 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 123 | 5,79 | 5,79 | 5,79 | 5,79 |
| 🟢 124 | 13,91 | 13,91 | 13,91 | 13,91 |
| 🟢 125 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 126 | 16,37 | 16,37 | 16,37 | 16,37 |
| 🟢 127 | 16,75 | 16,75 | 16,75 | 16,75 |
| 🟢 128 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 129 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 130 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 131 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 132 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 133 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 134 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 135 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 136 | 17,03 | 17,03 | 17,03 | 17,03 |
| 🟢 137 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 138 | 19,40 | 19,40 | 19,40 | 19,40 |
| 🟢 139 | 21,79 | 21,79 | 21,79 | 21,79 |
| 🟢 140 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 141 | 15,78 | 15,78 | 15,78 | 15,78 |
| 🟢 142 | 17,73 | 17,73 | 17,73 | 17,73 |
| 🟢 143 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 144 | 14,25 | 14,25 | 14,25 | 14,25 |
| 🟢 145 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 146 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 147 | 9,92 | 9,92 | 9,92 | 9,92 |
| 🟢 148 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 149 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 150 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 151 | 34,98 | 34,98 | 34,98 | 34,98 |
| 🟢 152 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 153 | 17,91 | 17,91 | 17,91 | 17,91 |
| 🟢 154 | 24,00 | 24,00 | 24,00 | 24,00 |
| 🟢 155 | 30,56 | 30,56 | 30,56 | 30,56 |
| 🟢 156 | 15,55 | 15,55 | 15,55 | 15,55 |
| 🟢 157 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟢 158 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟢 159 | 24,53 | 24,53 | 24,53 | 24,53 |
| 🟢 160 | 26,91 | 26,91 | 26,91 | 26,91 |
| 🟢 161 | 32,21 | 32,21 | 32,21 | 32,21 |
| 🟢 162 | 23,42 | 23,42 | 23,42 | 23,42 |
| 🟡 163 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 164 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟢 165 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 166 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 167 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 168 | 14,02 | 14,02 | 14,02 | 14,02 |
| 🟡 169 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 170 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 171 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 172 | 10,69 | 10,69 | 10,69 | 10,69 |
| 🟢 173 | 11,53 | 11,53 | 11,53 | 11,53 |
| 🟢 174 | 6,39 | 6,39 | 6,39 | 6,39 |
| 🟢 175 | 5,80 | 5,80 | 5,80 | 5,80 |
| 🟢 176 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 177 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟢 178 | 11,60 | 11,60 | 11,60 | 11,60 |
| 🟡 179 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 180 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 181 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 182 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 183 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟢 184 | 13,53 | 13,53 | 13,53 | 13,53 |
| 🟢 185 | 11,68 | 11,68 | 11,68 | 11,68 |
| 🟢 186 | 15,13 | 15,13 | 15,13 | 15,13 |
| 🟢 187 | 7,31 | 7,31 | 7,31 | 7,31 |
| 🟡 188 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 189 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 190 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 191 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 192 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 193 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟢 194 | 6,85 | 6,85 | 6,85 | 6,85 |
| 🟢 195 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 196 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 197 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 198 | 33,60 | 33,60 | 33,60 | 33,60 |
| 🟢 199 | 19,79 | 19,79 | 19,79 | 19,79 |
| 🟢 200 | 16,79 | 16,79 | 16,79 | 16,79 |
| 🟢 201 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 202 | 22,92 | 22,92 | 22,92 | 22,92 |
| 🟢 203 | 19,44 | 19,44 | 19,44 | 19,44 |
| 🟢 204 | 13,37 | 13,37 | 13,37 | 13,37 |
| 🟢 205 | 42,08 | 42,08 | 42,08 | 42,08 |
| 🟢 206 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 207 | 20,10 | 20,10 | 20,10 | 20,10 |
| 🟢 208 | 35,17 | 35,17 | 35,17 | 35,17 |
| 🟢 209 | 33,13 | 33,13 | 33,13 | 33,13 |
| 🟢 210 | 25,17 | 25,17 | 25,17 | 25,17 |
| 🟢 211 | 67,67 | 67,67 | 67,67 | 67,67 |
| 🟢 212 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 213 | 56,22 | 56,22 | 56,22 | 56,22 |
| 🟢 214 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟢 215 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 216 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 217 | 23,52 | 23,52 | 23,52 | 23,52 |
| 🟢 218 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 219 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 220 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟢 221 | 19,67 | 19,67 | 19,67 | 19,67 |
| 🟢 222 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 223 | 16,39 | 16,39 | 16,39 | 16,39 |
| 🟡 224 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 225 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 226 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 227 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 228 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 229 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 230 | 55,80 | 55,80 | 55,80 | 55,80 |
| 🟢 231 | 134,98 | 134,98 | 134,98 | 134,98 |
| 🟢 232 | 8,44 | 8,44 | 8,44 | 8,44 |
| 🟢 233 | 10,90 | 10,90 | 10,90 | 10,90 |
| 🟢 234 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 235 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 236 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 237 | 51,66 | 51,66 | 51,66 | 51,66 |
| 🟢 238 | 41,32 | 41,32 | 41,32 | 41,32 |
| 🟢 239 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 240 | 36,80 | 36,80 | 36,80 | 36,80 |
| 🟡 241 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 242 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟢 243 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 244 | 27,53 | 27,53 | 27,53 | 27,53 |
| 🟢 245 | 28,87 | 28,87 | 28,87 | 28,87 |
| 🟢 246 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟡 247 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 248 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 249 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 250 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 251 | 12,05 | 12,05 | 12,05 | 12,05 |
| 🟢 252 | 7,51 | 7,51 | 7,51 | 7,51 |
| 🟢 253 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 254 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 255 | 27,84 | 27,84 | 27,84 | 27,84 |
| 🟢 256 | 29,42 | 29,42 | 29,42 | 29,42 |
| 🟢 257 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟢 258 | 53,41 | 53,41 | 53,41 | 53,41 |
| 🟢 259 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 260 | 19,49 | 19,49 | 19,49 | 19,49 |
| 🟢 261 | 38,46 | 38,46 | 38,46 | 38,46 |
| 🟢 262 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟢 263 | 7,97 | 7,97 | 7,97 | 7,97 |
| 🟢 264 | 8,29 | 8,29 | 8,29 | 8,29 |
| 🟢 265 | 9,88 | 9,88 | 9,88 | 9,88 |
| 🟢 266 | 1,30 | 1,30 | 1,30 | 1,30 |
| 🟢 267 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟢 268 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 269 | 29,20 | 29,20 | 29,20 | 29,20 |
| 🟢 270 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 271 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 272 | 10,68 | 10,68 | 10,68 | 10,68 |
| 🟢 273 | 12,82 | 12,82 | 12,82 | 12,82 |
| 🟢 274 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 275 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 276 | 5,34 | 5,34 | 5,34 | 5,34 |
| 🟡 277 | 10,22 | 10,22 | 10,22 | 10,22 |
| 🟢 278 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 279 | 33,63 | 33,63 | 33,63 | 33,63 |
| 🟢 280 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 281 | 35,49 | 35,49 | 35,49 | 35,49 |
| 🟢 282 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟢 283 | 12,37 | 12,37 | 12,37 | 12,37 |
| 🟢 284 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 285 | 7,87 | 7,87 | 7,87 | 7,87 |
| 🟢 286 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟢 287 | 6,16 | 6,16 | 6,16 | 6,16 |
| 🟢 288 | 12,09 | 12,09 | 12,09 | 12,09 |
| 🟢 289 | 16,35 | 16,35 | 16,35 | 16,35 |
| 🟢 290 | 13,93 | 13,93 | 13,93 | 13,93 |
| 🟢 291 | 19,35 | 19,35 | 19,35 | 19,35 |
| 🟢 292 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 293 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 294 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 295 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 296 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 297 | 24,84 | 24,84 | 24,84 | 24,84 |
| 🟢 298 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟢 299 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 300 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 301 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟢 302 | 23,18 | 23,18 | 23,18 | 23,18 |
| 🟢 303 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟡 304 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 305 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 306 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 307 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 308 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟢 309 | 2,86 | 2,86 | 2,86 | 2,86 |
| 🟡 310 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 311 | 5,19 | 5,19 | 5,19 | 5,19 |
| 🟢 312 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 313 | 6,57 | 6,57 | 6,57 | 6,57 |
| 🟢 314 | 7,96 | 7,96 | 7,96 | 7,96 |
| 🟡 315 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 316 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 317 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 318 | 12,75 | 12,75 | 12,75 | 12,75 |
| 🟢 319 | 34,11 | 34,11 | 34,11 | 34,11 |
| 🟢 320 | 34,11 | 34,11 | 34,11 | 34,11 |
| 🟢 321 | 48,08 | 48,08 | 48,08 | 48,08 |
| 🟢 322 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 323 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 324 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 325 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 326 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 327 | 7,91 | 7,91 | 7,91 | 7,91 |
| 🟢 328 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 329 | 5,83 | 5,83 | 5,83 | 5,83 |
| 🟢 330 | 6,72 | 6,72 | 6,72 | 6,72 |
| 🟢 331 | 3,96 | 3,96 | 3,96 | 3,96 |
| 🟢 332 | 10,40 | 10,40 | 10,40 | 10,40 |
| 🟢 333 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 334 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 335 | 13,00 | 13,00 | 13,00 | 13,00 |
| 🟢 336 | 5,20 | 5,20 | 5,20 | 5,20 |
| 🟢 337 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 338 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 339 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 340 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 341 | 9,85 | 9,85 | 9,85 | 9,85 |
| 🟢 342 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 343 | 17,47 | 17,47 | 17,47 | 17,47 |
| 🟢 344 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 345 | 23,05 | 23,05 | 23,05 | 23,05 |
| 🟢 346 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🟢 347 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 348 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 349 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 350 | 18,28 | 18,28 | 18,28 | 18,28 |
| 🟢 351 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 352 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 353 | 15,01 | 15,01 | 15,01 | 15,01 |
| 🟢 354 | 26,94 | 26,94 | 26,94 | 26,94 |
| 🟢 355 | 4,05 | 4,05 | 4,05 | 4,05 |
| 🟢 356 | 33,57 | 33,57 | 33,57 | 33,57 |
| 🟢 357 | 4,51 | 4,51 | 4,51 | 4,51 |
| 🟢 358 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟢 359 | 12,48 | 12,48 | 12,48 | 12,48 |
| 🟢 360 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 361 | 14,19 | 14,19 | 14,19 | 14,19 |
| 🟢 362 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 363 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 364 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 365 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 366 | 10,95 | 10,95 | 10,95 | 10,95 |
| 🟡 367 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🟢 368 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 369 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 370 | 15,94 | 15,94 | 15,94 | 15,94 |
| 🟢 371 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 372 | 20,20 | 20,20 | 20,20 | 20,20 |
| 🟢 373 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 374 | 23,58 | 23,58 | 23,58 | 23,58 |
| 🟢 375 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 376 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 377 | 28,05 | 28,05 | 28,05 | 28,05 |
| 🟢 378 | 38,20 | 38,20 | 38,20 | 38,20 |
| 🟢 379 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟡 380 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 381 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 382 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 383 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 384 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 385 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 386 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 387 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 388 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 389 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 390 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 391 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 392 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 393 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 394 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 395 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 396 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 397 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 398 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 399 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 400 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 401 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 402 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 403 | 31,84 | 31,84 | 31,84 | 31,84 |
| 🟢 404 | 18,41 | 18,41 | 18,41 | 18,41 |
| 🟢 405 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 406 | 20,52 | 20,52 | 20,52 | 20,52 |
| 🟢 407 | 14,68 | 14,68 | 14,68 | 14,68 |
| 🟢 408 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟢 409 | 20,75 | 20,75 | 20,75 | 20,75 |
| 🟢 410 | 12,26 | 12,26 | 12,26 | 12,26 |
| 🟢 411 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 412 | 7,13 | 7,13 | 7,13 | 7,13 |
| 🟢 413 | 6,33 | 6,33 | 6,33 | 6,33 |
| 🟢 414 | 9,42 | 9,42 | 9,42 | 9,42 |
| 🟢 415 | 7,29 | 7,29 | 7,29 | 7,29 |
| 🟢 416 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 417 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 418 | 4,29 | 4,29 | 4,29 | 4,29 |
| 🟢 419 | 4,41 | 4,41 | 4,41 | 4,41 |
| 🟢 420 | 1,46 | 1,46 | 1,46 | 1,46 |
| 🟢 421 | 8,41 | 8,41 | 8,41 | 8,41 |
| 🟢 422 | 10,10 | 10,10 | 10,10 | 10,10 |
| 🟢 423 | 9,25 | 9,25 | 9,25 | 9,25 |
| 🟢 424 | 10,52 | 10,52 | 10,52 | 10,52 |
| 🟢 425 | 4,21 | 4,21 | 4,21 | 4,21 |
| 🟢 426 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 427 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 428 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 429 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 430 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 431 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 432 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 433 | 17,85 | 17,85 | 17,85 | 17,85 |
| 🟢 434 | 21,41 | 21,41 | 21,41 | 21,41 |
| 🟢 435 | 16,23 | 16,23 | 16,23 | 16,23 |
| 🟢 436 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 437 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 438 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 439 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 440 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 441 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 442 | 18,89 | 18,89 | 18,89 | 18,89 |
| 🟢 443 | 23,91 | 23,91 | 23,91 | 23,91 |
| 🟢 444 | 5,64 | 5,64 | 5,64 | 5,64 |
| 🟢 445 | 26,39 | 26,39 | 26,39 | 26,39 |
| 🟢 446 | 47,97 | 47,97 | 47,97 | 47,97 |
| 🟢 447 | 16,45 | 16,45 | 16,45 | 16,45 |
| 🟢 448 | 47,46 | 47,46 | 47,46 | 47,46 |
| 🟢 449 | 26,39 | 26,39 | 26,39 | 26,39 |
| 🟢 450 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 451 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🟢 452 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 453 | 11,24 | 11,24 | 11,24 | 11,24 |
| 🟢 454 | 21,33 | 21,33 | 21,33 | 21,33 |
| 🟢 455 | 8,25 | 8,25 | 8,25 | 8,25 |
| 🟢 456 | 21,87 | 21,87 | 21,87 | 21,87 |
| 🟢 457 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟢 458 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 459 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 460 | 23,08 | 23,08 | 23,08 | 23,08 |
| 🟢 461 | 10,98 | 10,98 | 10,98 | 10,98 |
| 🟡 462 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 463 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 464 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 465 | 19,78 | 19,78 | 19,78 | 19,78 |
| 🟢 466 | 15,12 | 15,12 | 15,12 | 15,12 |
| 🟢 467 | 9,60 | 9,60 | 9,60 | 9,60 |
| 🟢 468 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 469 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 470 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 471 | 16,52 | 16,52 | 16,52 | 16,52 |
| 🟢 472 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 473 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 474 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 475 | 13,75 | 13,75 | 13,75 | 13,75 |
| 🟢 476 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 477 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 478 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 479 | 31,16 | 31,16 | 31,16 | 31,16 |
| 🟢 480 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 481 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 482 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 483 | 19,46 | 19,46 | 19,46 | 19,46 |
| 🟢 484 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 485 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 486 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 487 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 488 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 489 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 490 | 24,69 | 24,69 | 24,69 | 24,69 |
| 🟢 491 | 25,18 | 25,18 | 25,18 | 25,18 |
| 🟢 492 | 28,56 | 28,56 | 28,56 | 28,56 |
| 🟢 493 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 494 | 10,07 | 10,07 | 10,07 | 10,07 |
| 🟢 495 | 20,43 | 20,43 | 20,43 | 20,43 |
| 🟡 496 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 497 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 498 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 499 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 500 | 8,68 | 8,68 | 8,68 | 8,68 |
| 🟢 501 | 25,26 | 25,26 | 25,26 | 25,26 |
| 🟢 502 | 10,83 | 10,83 | 10,83 | 10,83 |
| 🟢 503 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 504 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 505 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟢 506 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 507 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 508 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 509 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 510 | 21,22 | 21,22 | 21,22 | 21,22 |
| 🟢 511 | 9,06 | 9,06 | 9,06 | 9,06 |
| 🟢 512 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟢 513 | 11,81 | 11,81 | 11,81 | 11,81 |
| 🟢 514 | 10,86 | 10,86 | 10,86 | 10,86 |
| 🟢 515 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 516 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 517 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 518 | 30,22 | 30,22 | 30,22 | 30,22 |
| 🟢 519 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 520 | 53,81 | 53,81 | 53,81 | 53,81 |
| 🟢 521 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 522 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 523 | 21,08 | 21,08 | 21,08 | 21,08 |
| 🟢 524 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟢 525 | 8,78 | 8,78 | 8,78 | 8,78 |
| 🟢 526 | 13,35 | 13,35 | 13,35 | 13,35 |
| 🟢 527 | 5,26 | 5,26 | 5,26 | 5,26 |
| 🟢 528 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 529 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 530 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 531 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 532 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 533 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟢 534 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 535 | 12,90 | 12,90 | 12,90 | 12,90 |
| 🟢 536 | 12,44 | 12,44 | 12,44 | 12,44 |
| 🟢 537 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 538 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 539 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 540 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 541 | 21,35 | 21,35 | 21,35 | 21,35 |
| 🟢 542 | 17,76 | 17,76 | 17,76 | 17,76 |
| 🟢 543 | 38,58 | 38,58 | 38,58 | 38,58 |
| 🟢 544 | 36,01 | 36,01 | 36,01 | 36,01 |
| 🟢 545 | 28,09 | 28,09 | 28,09 | 28,09 |
| 🟢 546 | 26,36 | 26,36 | 26,36 | 26,36 |
| 🟢 547 | 17,43 | 17,43 | 17,43 | 17,43 |
| 🟢 548 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 549 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 550 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 551 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 552 | 30,68 | 30,68 | 30,68 | 30,68 |
| 🟢 553 | 16,94 | 16,94 | 16,94 | 16,94 |
| 🟢 554 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 555 | 23,61 | 23,61 | 23,61 | 23,61 |
| 🟢 556 | 14,59 | 14,59 | 14,59 | 14,59 |
| 🟢 557 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 558 | 27,43 | 27,43 | 27,43 | 27,43 |
| 🟢 559 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 560 | 38,88 | 38,88 | 38,88 | 38,88 |
| 🟢 561 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 562 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 563 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 564 | 9,87 | 9,87 | 9,87 | 9,87 |
| 🟢 565 | 7,22 | 6,36 | 6,00 | 5,41 |
| 🟢 566 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 567 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 568 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟢 569 | 9,64 | 9,64 | 9,64 | 9,64 |
| 🟡 570 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 571 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 572 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 573 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 574 | 12,97 | 12,97 | 12,97 | 12,97 |
| 🟢 575 | 2,79 | 2,79 | 2,79 | 2,79 |
| 🟢 576 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 577 | 16,27 | 16,27 | 16,27 | 16,27 |
| 🟢 578 | 20,02 | 20,02 | 20,02 | 20,02 |
| 🟢 579 | 18,85 | 18,85 | 18,85 | 18,85 |
| 🟢 580 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟢 581 | 22,31 | 22,31 | 22,31 | 22,31 |
| 🟢 582 | 14,74 | 14,74 | 14,74 | 14,74 |
| 🟢 583 | 16,00 | 16,00 | 16,00 | 16,00 |
| 🟢 584 | 16,84 | 16,84 | 16,84 | 16,84 |
| 🟢 585 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 586 | 11,56 | 11,56 | 11,56 | 11,56 |
| 🟢 587 | 15,75 | 15,75 | 15,75 | 15,75 |
| 🟢 588 | 13,32 | 13,32 | 13,32 | 13,32 |
| 🟢 589 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟢 590 | 33,81 | 33,81 | 33,81 | 33,81 |
| 🟢 591 | 15,43 | 15,43 | 15,43 | 15,43 |
| 🟢 592 | 30,12 | 30,12 | 30,12 | 30,12 |
| 🟡 593 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 594 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 595 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟢 596 | 15,16 | 15,16 | 15,16 | 15,16 |
| 🟢 597 | 18,71 | 18,71 | 18,71 | 18,71 |
| 🟢 598 | 17,58 | 17,58 | 17,58 | 17,58 |
| 🟡 599 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 600 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟢 601 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 602 | 46,01 | 46,01 | 46,01 | 46,01 |
| 🟢 603 | 111,11 | 111,11 | 111,11 | 111,11 |
| 🟢 604 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 605 | 31,70 | 31,70 | 31,70 | 31,70 |
| 🟢 606 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 607 | 40,73 | 40,73 | 40,73 | 40,73 |
| 🟢 608 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 609 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟢 610 | 39,07 | 39,07 | 39,07 | 39,07 |
| 🟢 611 | 26,16 | 26,16 | 26,16 | 26,16 |
| 🟡 612 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 613 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 614 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 615 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 616 | 12,10 | 12,10 | 12,10 | 12,10 |
| 🟢 617 | 14,92 | 14,92 | 14,92 | 14,92 |
| 🟢 618 | 14,00 | 14,00 | 14,00 | 14,00 |
| 🟢 619 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 620 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 621 | 29,41 | 29,41 | 29,41 | 29,41 |
| 🟢 622 | 20,39 | 20,39 | 20,39 | 20,39 |
| 🟢 623 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 624 | 10,72 | 10,72 | 10,72 | 10,72 |
| 🟢 625 | 13,23 | 13,23 | 13,23 | 13,23 |
| 🟢 626 | 12,40 | 12,40 | 12,40 | 12,40 |
| 🟢 627 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 628 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 629 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 630 | 17,00 | 17,00 | 17,00 | 17,00 |
| 🟢 631 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 632 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟢 633 | 7,99 | 7,99 | 7,99 | 7,99 |
| 🟢 634 | 8,88 | 8,88 | 8,88 | 8,88 |
| 🟢 635 | 8,51 | 8,51 | 8,51 | 8,51 |
| 🟢 636 | 5,18 | 5,18 | 5,18 | 5,18 |
| 🟢 637 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟢 638 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 639 | 17,37 | 17,37 | 17,37 | 17,37 |
| 🟢 640 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 641 | 12,78 | 12,78 | 12,78 | 12,78 |
| 🟡 642 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 643 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 644 | 14,98 | 14,98 | 14,98 | 14,98 |
| 🟢 645 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟢 646 | 17,28 | 17,28 | 17,28 | 17,28 |
| 🟡 647 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 648 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 649 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 650 | 18,29 | 18,29 | 18,29 | 18,29 |
| 🟢 651 | 23,40 | 23,40 | 23,40 | 23,40 |
| 🟢 652 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 653 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 654 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 655 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 656 | 23,16 | 23,16 | 23,16 | 23,16 |
| 🟢 657 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 658 | 52,77 | 52,77 | 52,77 | 52,77 |
| 🟢 659 | 52,18 | 52,18 | 52,18 | 52,18 |
| 🟢 660 | 42,22 | 42,22 | 42,22 | 42,22 |
| 🟢 661 | 41,75 | 41,75 | 41,75 | 41,75 |
| 🟢 662 | 19,26 | 19,26 | 19,26 | 19,26 |
| 🟢 663 | 19,05 | 19,05 | 19,05 | 19,05 |
| 🟢 664 | 37,60 | 37,60 | 37,60 | 37,60 |
| 🟢 665 | 37,18 | 37,18 | 37,18 | 37,18 |
| 🟢 666 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟢 667 | 48,13 | 48,13 | 48,13 | 48,13 |
| 🟢 668 | 21,96 | 21,96 | 21,96 | 21,96 |
| 🟢 669 | 48,05 | 48,05 | 48,05 | 48,05 |
| 🟢 670 | 18,45 | 18,45 | 18,45 | 18,45 |
| 🟢 671 | 16,01 | 16,01 | 16,01 | 16,01 |
| 🟢 672 | 13,71 | 13,71 | 13,71 | 13,71 |
| 🟢 673 | 27,13 | 27,13 | 27,13 | 27,13 |
| 🟢 674 | 20,16 | 20,16 | 20,16 | 20,16 |
| 🟢 675 | 37,05 | 37,05 | 37,05 | 37,05 |
| 🟢 676 | 27,54 | 27,54 | 27,54 | 27,54 |
| 🟢 677 | 35,03 | 35,03 | 35,03 | 35,03 |
| 🟢 678 | 26,03 | 26,03 | 26,03 | 26,03 |
| 🟢 679 | 18,75 | 18,75 | 18,75 | 18,75 |
| 🟢 680 | 22,69 | 22,69 | 22,69 | 22,69 |
| 🟢 681 | 41,78 | 41,78 | 41,78 | 41,78 |
| 🟢 682 | 33,33 | 33,33 | 33,33 | 33,33 |
| 🟢 683 | 16,04 | 16,04 | 16,04 | 16,04 |

As categorias abaixo ainda não têm a tabela oficial do prestador no catálogo. Nesses municípios o programa não as oferece, e o caminho é lançar a tabela no modo Personalizado.

<!-- tabela: **Tabela 26** — Categorias tarifárias ainda não coletadas, por prestador -->
| Prestador: municípios | Categorias não coletadas |
| :--- | :--- |
| 🔴 BRK Alagoas: Marechal Deodoro (AL) | Social |
| 🔴 BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Social |
| 🔴 BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Uruguaiana: Uruguaiana (RS) | Social |
| 🔴 CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Social |
| 🔴 CAER: Boa Vista (RR) | Comercial, Pública, Industrial, Social |
| 🔴 CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN), Extremoz (RN), Macaíba (RN), Mossoró (RN), Parnamirim (RN) | Comercial, Pública, Industrial, Social |
| 🔴 CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Comercial, Pública, Industrial, Social |
| 🔴 CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Social |
| 🔴 CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Social |
| 🔴 CEDAE: Barra do Piraí (RJ), Itaperuna (RJ), Macaé (RJ) | Social |
| 🔴 CEDAE/serviço local – validar área: Guapimirim (RJ), Valença (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 CODEN Nova Odessa: Nova Odessa (SP) | Pública |
| 🔴 COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Comercial, Pública, Industrial, Social |
| 🔴 COMUSA Novo Hamburgo: Novo Hamburgo (RS) | Social |
| 🔴 CORSAN: Canoas (RS), Erechim (RS), Esteio (RS), Santa Cruz do Sul (RS) | Industrial |
| 🔴 CORSAN: Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Canoas (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Erechim (RS), Esteio (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Cruz do Sul (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Social |
| 🔴 COSAMA: Tabatinga (AM) | Social |
| 🔴 DAAE Rio Claro: Rio Claro (SP) | Pública |
| 🔴 DAE Bauru: Bauru (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Comercial, Pública, Industrial, Social |
| 🔴 DAE/VG: Várzea Grande (MT) | Comercial, Pública, Industrial, Social |
| 🔴 DAEP Penápolis: Penápolis (SP) | Social |
| 🔴 DAEPA: Patrocínio (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DAESC Coruripe: Coruripe (AL) | Comercial, Pública, Industrial, Social |
| 🔴 DAMAE São João del-Rei: São João del-Rei (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DEMSUR: Muriaé (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DMAE Porto Alegre: Porto Alegre (RS) | Comercial, Pública, Industrial, Social |
| 🔴 DMAE Uberlândia: Uberlândia (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DMAES Ponte Nova: Ponte Nova (MG) | Comercial, Pública, Industrial, Social |
| 🔴 Iguá Sergipe: Estância (SE) | Pública |
| 🔴 Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Prefeitura de Cosmópolis: Cosmópolis (SP) | Pública |
| 🔴 Prestador municipal/local – Iranduba: Iranduba (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – Manicoré: Manicoré (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – Tefé: Tefé (AM) | Comercial, Pública, Industrial, Social |
| 🔴 RIC Ambiental: Marília (SP) | Social |
| 🔴 Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Social |
| 🔴 SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Angra dos Reis: Angra dos Reis (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Barra Mansa: Barra Mansa (RJ) | Social |
| 🔴 SAAE Capivari: Capivari (SP) | Pública |
| 🔴 SAAE Cruzeiro: Cruzeiro (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Ibitinga: Ibitinga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Itacoatiara: Itacoatiara (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Jacareí: Jacareí (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Lençóis Paulista: Lençóis Paulista (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Linhares: Linhares (ES) | Social |
| 🔴 SAAE Manhuaçu: Manhuaçu (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Mariana: Mariana (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Maués: Maués (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Mogi Mirim: Mogi Mirim (SP) | Social |
| 🔴 SAAE Nova Mutum: Nova Mutum (MT) | Social |
| 🔴 SAAE Parintins: Parintins (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Sete Lagoas: Sete Lagoas (MG) | Social |
| 🔴 SAAE Sorocaba: Sorocaba (SP) | Comercial, Pública, Industrial |
| 🔴 SAAE Três Pontas: Três Pontas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Três Rios: Três Rios (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Vilhena: Vilhena (RO) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Viçosa: Viçosa (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Volta Redonda: Volta Redonda (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAEB Ambiental: Bebedouro (SP) | Pública, Social |
| 🔴 SAAEJA: Jaguariúna (SP) | Pública |
| 🔴 SAAET: Taquaritinga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEC Catanduva: Catanduva (SP) | Comercial, Pública, Industrial |
| 🔴 SAECIL Leme: Leme (SP) | Comercial, Pública, Industrial |
| 🔴 SAEMAS Sertãozinho: Sertãozinho (SP) | Comercial, Pública, Industrial |
| 🔴 SAEP Pirassununga: Pirassununga (SP) | Pública |
| 🔴 SAERP Ribeirão Preto: Ribeirão Preto (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAESA: São Caetano do Sul (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Social |
| 🔴 SAMAE Brusque: Brusque (SC) | Social |
| 🔴 SAMAE Caxias do Sul: Caxias do Sul (RS) | Social |
| 🔴 SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Social |
| 🔴 SAMAE São Bento do Sul: São Bento do Sul (SC) | Pública, Industrial, Social |
| 🔴 SAMAE Tangará da Serra: Tangará da Serra (MT) | Comercial, Pública, Industrial, Social |
| 🔴 SANASA Campinas: Campinas (SP) | Comercial, Pública, Industrial |
| 🔴 SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Social |
| 🔴 SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Social |
| 🔴 SANEAR Colatina: Colatina (ES) | Social |
| 🔴 SANEAR Rondonópolis: Rondonópolis (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Saneouro: Ouro Preto (MG) | Comercial, Pública, Industrial |
| 🔴 SANEP Pelotas: Pelotas (RS) | Social |
| 🔴 Sanessol: Mirassol (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SEMAE Piracicaba: Piracicaba (SP) | Comercial, Pública, Industrial |
| 🔴 SeMAE Rio Preto: São José do Rio Preto (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SEMASA Itajaí: Itajaí (SC) | Social |
| 🔴 SEMASA Lages: Lages (SC) | Social |
| 🔴 São Gabriel Saneamento S.A.: São Gabriel (RS) | Comercial, Pública, Industrial, Social |
| 🔴 Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Social |
| 🔴 Águas Cuiabá (Iguá): Cuiabá (MT) | Social |
| 🔴 Águas da Imperatriz: Teresópolis (RJ) | Social |
| 🔴 Águas das Agulhas Negras: Resende (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Andradina: Andradina (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Social |
| 🔴 Águas de Jahu: Jaú (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Juturnaíba: Araruama (RJ) | Social |
| 🔴 Águas de Matão: Matão (SP) | Pública, Industrial |
| 🔴 Águas de Niterói: Niterói (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Nova Friburgo: Nova Friburgo (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Pará de Minas: Pará de Minas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Primavera (Aegea): Primavera do Leste (MT) | Social |
| 🔴 Águas de Sinop (Aegea): Sinop (MT) | Social |
| 🔴 Águas de Sorriso: Sorriso (MT) | Social |
| 🔴 Águas do Imperador: Petrópolis (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Pantanal (autarquia municipal): Cáceres (MT) | Social |
| 🔴 Águas do Paraíba: Campos dos Goytacazes (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Rio: Belford Roxo (RJ), Cachoeiras de Macacu (RJ), Duque de Caxias (RJ), Itaboraí (RJ), Japeri (RJ), Magé (RJ), Maricá (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ), São João de Meriti (RJ) | Social |
| 🔴 Águas do Rio (tarifa representativa; Iguá na Barra e em Jacarepaguá): Rio de Janeiro (RJ) | Social |
| 🔴 Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL), Penedo (AL), São Miguel dos Campos (AL) | Social |
| 🔴 Águas Guariroba: Campo Grande (MS) | Social |
| 🔴 Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Comercial, Pública, Industrial, Social |

A segunda tabela traz, para as mesmas linhas, a vigência declarada pela fonte e a data em que a página oficial foi verificada pela última vez pela rotina de monitoramento da base. Linha sem data é fonte que a rotina ainda não monitora.

<!-- tabela: **Tabela 27** — Vigência e última verificação da fonte de cada estrutura tarifária, com a situação do dado -->
| Nº | Vigência declarada | Fonte verificada em | Situação |
| ---: | :--- | :--- | :--- |
| 🟢 1 | 08/12/2025 | — | auditada |
| 🟢 2 | 08/12/2025 | — | auditada |
| 🟢 3 | 08/12/2025 | — | auditada |
| 🟢 4 | 08/12/2025 | — | auditada |
| 🟢 5 | 08/12/2025 | — | auditada |
| 🟢 6 | 08/12/2025 | — | auditada |
| 🟢 7 | 08/12/2025 | — | auditada |
| 🟢 8 | 08/12/2025 | — | auditada |
| 🟢 9 | 08/12/2025 | — | auditada |
| 🟢 10 | 08/12/2025 | — | auditada |
| 🟢 11 | 08/12/2025 | — | auditada |
| 🟢 12 | 08/12/2025 | — | auditada |
| 🟢 13 | 08/12/2025 | — | auditada |
| 🟢 14 | 08/12/2025 | — | auditada |
| 🟢 15 | 01/02/2024 | — | auditada |
| 🟢 16 | 01/02/2024 | — | auditada |
| 🟢 17 | 01/02/2024 | — | auditada |
| 🟢 18 | 01/02/2024 | — | auditada |
| 🟢 19 | 29/05/2026 | — | auditada |
| 🟢 20 | 29/05/2026 | — | auditada |
| 🟢 21 | 29/05/2026 | — | auditada |
| 🟢 22 | 29/05/2026 | — | auditada |
| 🟢 23 | 29/05/2026 | — | auditada |
| 🟡 24 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 25 | 11/12/2025 | — | auditada |
| 🟢 26 | 11/12/2025 | — | auditada |
| 🟢 27 | 11/12/2025 | — | auditada |
| 🟢 28 | 11/12/2025 | — | auditada |
| 🟢 29 | 11/12/2025 | — | auditada |
| 🟢 30 | 30/08/2025 | — | auditada |
| 🟢 31 | 30/08/2025 | — | auditada |
| 🟢 32 | 30/08/2025 | — | auditada |
| 🟢 33 | 30/08/2025 | — | auditada |
| 🟢 34 | 05/12/2025 | — | auditada |
| 🟢 35 | 05/12/2025 | — | auditada |
| 🟢 36 | 05/12/2025 | — | auditada |
| 🟢 37 | 05/12/2025 | — | auditada |
| 🟢 38 | 05/12/2025 | — | auditada |
| 🟢 39 | 05/01/2024 | — | auditada |
| 🟢 40 | 05/01/2024 | — | auditada |
| 🟢 41 | 05/01/2024 | — | auditada |
| 🟢 42 | 05/01/2024 | — | auditada |
| 🟡 43 | Estrutura Tarifária CAER Oficial | 31/08/2026 | a confirmar |
| 🟢 44 | 19/06/2025 | — | auditada |
| 🟢 45 | 19/06/2025 | — | auditada |
| 🟢 46 | 19/06/2025 | — | auditada |
| 🟢 47 | 19/06/2025 | — | auditada |
| 🟢 48 | 19/06/2025 | — | auditada |
| 🟢 49 | Vigente desde 01/04/2025 | 31/08/2026 | auditada |
| 🟢 50 | 27/08/2026 | — | auditada |
| 🟢 51 | 27/08/2026 | — | auditada |
| 🟢 52 | 27/08/2026 | — | auditada |
| 🟢 53 | 27/08/2026 | — | auditada |
| 🟢 54 | 27/08/2026 | — | auditada |
| 🟢 55 | 01/06/2026 | — | auditada |
| 🟢 56 | 01/06/2026 | — | auditada |
| 🟢 57 | 01/06/2026 | — | auditada |
| 🟢 58 | 01/06/2026 | — | auditada |
| 🟢 59 | 01/06/2026 | — | auditada |
| 🟡 60 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 61 | 05/11/2025 | 31/08/2026 | auditada |
| 🟢 62 | 05/11/2025 | 31/08/2026 | auditada |
| 🟢 63 | 05/11/2025 | 31/08/2026 | auditada |
| 🟢 64 | 05/11/2025 | 31/08/2026 | auditada |
| 🟢 65 | 30/06/2025 | — | auditada |
| 🟢 66 | 30/06/2025 | — | auditada |
| 🟢 67 | 30/06/2025 | — | auditada |
| 🟢 68 | 30/06/2025 | — | auditada |
| 🟢 69 | 08/12/2025 | — | auditada |
| 🟢 70 | 08/12/2025 | — | auditada |
| 🟢 71 | 08/12/2025 | — | auditada |
| 🟢 72 | 08/12/2025 | — | auditada |
| 🟢 73 | 08/12/2025 | — | auditada |
| 🟢 74 | 01/04/2026 | 31/08/2026 | auditada |
| 🟢 75 | 01/04/2026 | 31/08/2026 | auditada |
| 🟢 76 | 01/04/2026 | 31/08/2026 | auditada |
| 🟢 77 | 01/04/2026 | 31/08/2026 | auditada |
| 🟢 78 | 01/04/2026 | 31/08/2026 | auditada |
| 🟢 79 | 22/01/2026 | — | auditada |
| 🟢 80 | 22/01/2026 | — | auditada |
| 🟢 81 | 22/01/2026 | — | auditada |
| 🟢 82 | 22/01/2026 | — | auditada |
| 🟡 83 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟢 84 | 01/05/2026 | — | auditada |
| 🟢 85 | 01/05/2026 | — | auditada |
| 🟢 86 | 01/05/2026 | — | auditada |
| 🟢 87 | 01/05/2026 | — | auditada |
| 🟢 88 | 01/05/2026 | — | auditada |
| 🟢 89 | 19/03/2026 | — | auditada |
| 🟢 90 | 19/03/2026 | — | auditada |
| 🟢 91 | 19/03/2026 | — | auditada |
| 🟢 92 | 19/03/2026 | — | auditada |
| 🟢 93 | 19/03/2026 | — | auditada |
| 🟢 94 | 27/02/2025 | — | auditada |
| 🟢 95 | 27/02/2025 | — | auditada |
| 🟢 96 | 27/02/2025 | — | auditada |
| 🟢 97 | 27/02/2025 | — | auditada |
| 🟢 98 | 29/12/2014 | — | auditada |
| 🟢 99 | 01/05/2026 | — | auditada |
| 🟢 100 | 01/05/2026 | — | auditada |
| 🟢 101 | 01/05/2026 | — | auditada |
| 🟢 102 | 01/05/2026 | — | auditada |
| 🟢 103 | 01/05/2026 | — | auditada |
| 🟢 104 | 01/03/2026 | — | auditada |
| 🟢 105 | 01/03/2026 | — | auditada |
| 🟢 106 | 01/03/2026 | — | auditada |
| 🟢 107 | 01/03/2026 | — | auditada |
| 🟢 108 | 01/03/2026 | — | auditada |
| 🟢 109 | 26/03/2025 | — | auditada |
| 🟢 110 | 26/03/2025 | — | auditada |
| 🟢 111 | 26/03/2025 | — | auditada |
| 🟢 112 | 26/03/2025 | — | auditada |
| 🟢 113 | 26/03/2025 | — | auditada |
| 🟢 114 | 22/01/2026 | — | auditada |
| 🟢 115 | 22/01/2026 | 31/08/2026 | auditada |
| 🟢 116 | 22/01/2026 | — | auditada |
| 🟢 117 | 22/01/2026 | 31/08/2026 | auditada |
| 🟢 118 | 22/01/2026 | — | auditada |
| 🟢 119 | 22/01/2026 | 31/08/2026 | auditada |
| 🟢 120 | 22/01/2026 | — | auditada |
| 🟢 121 | 22/01/2026 | 31/08/2026 | auditada |
| 🟢 122 | 22/01/2026 | — | auditada |
| 🟢 123 | 22/01/2026 | 31/08/2026 | auditada |
| 🟢 124 | 2025 | — | auditada |
| 🟢 125 | 2025 | — | auditada |
| 🟢 126 | 2025 | — | auditada |
| 🟢 127 | 2025 | — | auditada |
| 🟢 128 | 13/12/2024 | — | auditada |
| 🟢 129 | 13/12/2024 | — | auditada |
| 🟢 130 | 13/12/2024 | — | auditada |
| 🟢 131 | 13/12/2024 | — | auditada |
| 🟢 132 | 13/12/2024 | — | auditada |
| 🟢 133 | 13/12/2024 | — | auditada |
| 🟢 134 | 13/12/2024 | — | auditada |
| 🟢 135 | 13/12/2024 | — | auditada |
| 🟢 136 | 13/12/2024 | — | auditada |
| 🟢 137 | 13/12/2024 | — | auditada |
| 🟢 138 | 13/12/2024 | — | auditada |
| 🟢 139 | 13/12/2024 | — | auditada |
| 🟢 140 | 13/12/2024 | — | auditada |
| 🟢 141 | 13/12/2024 | — | auditada |
| 🟢 142 | 13/12/2024 | — | auditada |
| 🟢 143 | 30/08/2026 | — | auditada |
| 🟢 144 | 30/08/2026 | — | auditada |
| 🟢 145 | 30/08/2026 | — | auditada |
| 🟢 146 | 30/08/2026 | — | auditada |
| 🟢 147 | 30/08/2026 | — | auditada |
| 🟢 148 | 01/11/2025 | — | auditada |
| 🟢 149 | 01/11/2025 | — | auditada |
| 🟢 150 | 01/11/2025 | — | auditada |
| 🟢 151 | 01/11/2025 | — | auditada |
| 🟢 152 | 01/11/2025 | — | auditada |
| 🟢 153 | 01/02/2026 | — | auditada |
| 🟢 154 | 01/02/2026 | — | auditada |
| 🟢 155 | 01/02/2026 | — | auditada |
| 🟢 156 | 01/02/2026 | — | auditada |
| 🟢 157 | 14/02/2026 | — | auditada |
| 🟢 158 | 01/12/2025 | — | auditada |
| 🟢 159 | 01/12/2025 | — | auditada |
| 🟢 160 | 01/12/2025 | — | auditada |
| 🟢 161 | 01/12/2025 | — | auditada |
| 🟢 162 | 01/12/2025 | — | auditada |
| 🟡 163 | Referência vigente pesquisada em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 164 | 17/09/2025 | — | auditada |
| 🟢 165 | 17/09/2025 | — | auditada |
| 🟢 166 | 17/09/2025 | — | auditada |
| 🟢 167 | 17/09/2025 | — | auditada |
| 🟢 168 | 17/09/2025 | — | auditada |
| 🟡 169 | Estrutura Tarifária DAE/VG | 31/08/2026 | a confirmar |
| 🟢 170 | 2026 | — | auditada |
| 🟢 171 | 2026 | — | auditada |
| 🟢 172 | 2026 | — | auditada |
| 🟢 173 | 2026 | — | auditada |
| 🟢 174 | 2026 | — | auditada |
| 🟢 175 | 01/03/2026 | — | auditada |
| 🟢 176 | 01/03/2026 | — | auditada |
| 🟢 177 | 01/03/2026 | — | auditada |
| 🟢 178 | 01/03/2026 | — | auditada |
| 🟡 179 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 180 | Resolução ARSAL Nº 233 | 31/08/2026 | a confirmar |
| 🟡 181 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 182 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 183 | 01/06/2026 | — | auditada |
| 🟢 184 | 01/06/2026 | — | auditada |
| 🟢 185 | 01/06/2026 | — | auditada |
| 🟢 186 | 01/06/2026 | — | auditada |
| 🟢 187 | 01/06/2026 | — | auditada |
| 🟡 188 | Estrutura Tarifária DMAE / ARESAN | 31/08/2026 | a confirmar |
| 🟡 189 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 190 | 04/05/2026 | — | auditada |
| 🟢 191 | 04/05/2026 | — | auditada |
| 🟢 192 | 04/05/2026 | — | auditada |
| 🟢 193 | 04/05/2026 | — | auditada |
| 🟢 194 | 04/05/2026 | — | auditada |
| 🟢 195 | 20/07/2026 | 31/08/2026 | auditada |
| 🟢 196 | 20/07/2026 | 31/08/2026 | auditada |
| 🟢 197 | 20/07/2026 | 31/08/2026 | auditada |
| 🟢 198 | 20/07/2026 | 31/08/2026 | auditada |
| 🟢 199 | 20/07/2026 | 31/08/2026 | auditada |
| 🟢 200 | 01/03/2026 | — | auditada |
| 🟢 201 | 01/03/2026 | — | auditada |
| 🟢 202 | 01/03/2026 | — | auditada |
| 🟢 203 | 01/03/2026 | — | auditada |
| 🟢 204 | 01/03/2026 | — | auditada |
| 🟢 205 | 01/09/2025 | — | auditada |
| 🟢 206 | 01/09/2025 | — | auditada |
| 🟢 207 | 01/09/2025 | — | auditada |
| 🟢 208 | 01/09/2025 | — | auditada |
| 🟢 209 | 01/09/2025 | — | auditada |
| 🟢 210 | 01/09/2025 | — | auditada |
| 🟢 211 | 01/09/2025 | — | auditada |
| 🟢 212 | 01/09/2025 | — | auditada |
| 🟢 213 | 01/09/2025 | — | auditada |
| 🟢 214 | 01/11/2025 | — | auditada |
| 🟢 215 | 01/11/2025 | — | auditada |
| 🟢 216 | 01/11/2025 | — | auditada |
| 🟢 217 | 01/11/2025 | — | auditada |
| 🟢 218 | 01/11/2025 | — | auditada |
| 🟡 219 | Desde 03/2026 | 31/08/2026 | a confirmar |
| 🟢 220 | 01/06/2025 | — | auditada |
| 🟢 221 | 01/06/2025 | — | auditada |
| 🟢 222 | 01/06/2025 | — | auditada |
| 🟢 223 | 01/06/2025 | — | auditada |
| 🟡 224 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 225 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 226 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 227 | Estrutura Municipal Vigente | — | a confirmar |
| 🟢 228 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 229 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 230 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 231 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 232 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 233 | 01/05/2024 | — | auditada |
| 🟢 234 | 01/05/2024 | — | auditada |
| 🟢 235 | 01/05/2024 | — | auditada |
| 🟢 236 | 01/05/2024 | — | auditada |
| 🟢 237 | 01/12/2025 | — | auditada |
| 🟢 238 | 01/12/2025 | — | auditada |
| 🟢 239 | 01/12/2025 | — | auditada |
| 🟢 240 | 01/12/2025 | — | auditada |
| 🟡 241 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 242 | 24/04/2026 | — | auditada |
| 🟢 243 | 24/04/2026 | — | auditada |
| 🟢 244 | 24/04/2026 | — | auditada |
| 🟢 245 | 24/04/2026 | — | auditada |
| 🟢 246 | 24/04/2026 | — | auditada |
| 🟡 247 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟢 248 | 09/06/2026 | — | auditada |
| 🟢 249 | 09/06/2026 | — | auditada |
| 🟢 250 | 09/06/2026 | — | auditada |
| 🟢 251 | 09/06/2026 | — | auditada |
| 🟢 252 | 09/06/2026 | — | auditada |
| 🟢 253 | 01/12/2025 | — | auditada |
| 🟢 254 | 01/12/2025 | — | auditada |
| 🟢 255 | 01/12/2025 | — | auditada |
| 🟢 256 | 01/12/2025 | — | auditada |
| 🟢 257 | 01/12/2025 | — | auditada |
| 🟢 258 | 01/03/2026 | — | auditada |
| 🟢 259 | 01/03/2026 | — | auditada |
| 🟢 260 | 01/03/2026 | — | auditada |
| 🟢 261 | 01/03/2026 | — | auditada |
| 🟢 262 | 28/12/2025 | — | auditada |
| 🟢 263 | 28/12/2025 | — | auditada |
| 🟢 264 | 28/12/2025 | — | auditada |
| 🟢 265 | 28/12/2025 | — | auditada |
| 🟢 266 | 28/12/2025 | — | auditada |
| 🟢 267 | 29/05/2026 | — | auditada |
| 🟢 268 | 29/05/2026 | — | auditada |
| 🟢 269 | 29/05/2026 | — | auditada |
| 🟢 270 | 29/05/2026 | — | auditada |
| 🟡 271 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 272 | 01/09/2026 | — | auditada |
| 🟢 273 | 01/09/2026 | — | auditada |
| 🟢 274 | 01/09/2026 | — | auditada |
| 🟢 275 | 01/09/2026 | — | auditada |
| 🟢 276 | 01/09/2026 | — | auditada |
| 🟡 277 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 278 | 01/06/2026 | — | auditada |
| 🟢 279 | 01/06/2026 | — | auditada |
| 🟢 280 | 01/06/2026 | — | auditada |
| 🟢 281 | 01/06/2026 | — | auditada |
| 🟢 282 | 01/06/2026 | — | auditada |
| 🟢 283 | 31/03/2026 | — | auditada |
| 🟢 284 | 31/03/2026 | — | auditada |
| 🟢 285 | 31/03/2026 | — | auditada |
| 🟢 286 | 31/03/2026 | — | auditada |
| 🟢 287 | 31/03/2026 | — | auditada |
| 🟢 288 | 01/07/2026 | — | auditada |
| 🟢 289 | 01/07/2026 | — | auditada |
| 🟢 290 | 01/07/2026 | — | auditada |
| 🟢 291 | 01/07/2026 | — | auditada |
| 🟢 292 | 01/07/2026 | — | auditada |
| 🟡 293 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 294 | 01/06/2026 | — | auditada |
| 🟢 295 | 01/06/2026 | — | auditada |
| 🟢 296 | 01/06/2026 | — | auditada |
| 🟢 297 | 01/06/2026 | — | auditada |
| 🟢 298 | 01/06/2026 | — | auditada |
| 🟢 299 | 01/08/2026 | — | auditada |
| 🟢 300 | 01/08/2026 | — | auditada |
| 🟢 301 | 01/08/2026 | — | auditada |
| 🟢 302 | 01/08/2026 | — | auditada |
| 🟢 303 | 01/08/2026 | — | auditada |
| 🟡 304 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 305 | 30/12/2025 | — | auditada |
| 🟢 306 | 30/12/2025 | — | auditada |
| 🟢 307 | 30/12/2025 | — | auditada |
| 🟢 308 | 30/12/2025 | — | auditada |
| 🟢 309 | 30/12/2025 | — | auditada |
| 🟡 310 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 311 | 19/01/2026 | — | auditada |
| 🟢 312 | 19/01/2026 | — | auditada |
| 🟢 313 | 19/01/2026 | — | auditada |
| 🟢 314 | 19/01/2026 | — | auditada |
| 🟡 315 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 316 | Desde 01/2026 | 31/08/2026 | a confirmar |
| 🟡 317 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 318 | 01/07/2026 | — | auditada |
| 🟢 319 | 01/07/2026 | — | auditada |
| 🟢 320 | 01/07/2026 | — | auditada |
| 🟢 321 | 01/07/2026 | — | auditada |
| 🟢 322 | 01/10/2026 | — | auditada |
| 🟢 323 | 01/10/2026 | — | auditada |
| 🟢 324 | 01/10/2026 | — | auditada |
| 🟢 325 | 01/10/2026 | — | auditada |
| 🟡 326 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 327 | 01/06/2026 | — | auditada |
| 🟢 328 | 01/06/2026 | — | auditada |
| 🟢 329 | 01/06/2026 | — | auditada |
| 🟢 330 | 01/06/2026 | — | auditada |
| 🟢 331 | 01/06/2026 | — | auditada |
| 🟢 332 | 03/12/2025 | — | auditada |
| 🟢 333 | 03/12/2025 | — | auditada |
| 🟢 334 | 03/12/2025 | — | auditada |
| 🟢 335 | 03/12/2025 | — | auditada |
| 🟢 336 | 03/12/2025 | — | auditada |
| 🟢 337 | 26/05/2025 | — | auditada |
| 🟢 338 | 26/05/2025 | — | auditada |
| 🟢 339 | 26/05/2025 | — | auditada |
| 🟢 340 | 26/05/2025 | — | auditada |
| 🟢 341 | 26/05/2025 | — | auditada |
| 🟢 342 | 01/11/2025 | — | auditada |
| 🟢 343 | 01/11/2025 | — | auditada |
| 🟢 344 | 01/11/2025 | — | auditada |
| 🟢 345 | 01/11/2025 | — | auditada |
| 🟢 346 | 01/11/2025 | — | auditada |
| 🟢 347 | 03/03/2026 | — | auditada |
| 🟢 348 | 03/03/2026 | — | auditada |
| 🟢 349 | 03/03/2026 | — | auditada |
| 🟢 350 | 03/03/2026 | — | auditada |
| 🟢 351 | 01/07/2026 | — | auditada |
| 🟢 352 | 01/07/2026 | — | auditada |
| 🟢 353 | 21/08/2026 | — | auditada |
| 🟢 354 | 21/08/2026 | — | auditada |
| 🟢 355 | 21/08/2026 | — | auditada |
| 🟢 356 | 21/08/2026 | — | auditada |
| 🟢 357 | 21/08/2026 | — | auditada |
| 🟢 358 | 26/02/2026 | — | auditada |
| 🟢 359 | 26/02/2026 | — | auditada |
| 🟢 360 | 26/02/2026 | — | auditada |
| 🟢 361 | 26/02/2026 | — | auditada |
| 🟢 362 | 26/02/2026 | — | auditada |
| 🟡 363 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 364 | Regulação Oficial | — | a confirmar |
| 🟡 365 | Resoluções AGERO / CAERD | 31/08/2026 | a confirmar |
| 🟡 366 | Resolução ARIS-MG nº 227/2026 | 31/08/2026 | a confirmar |
| 🟡 367 | Decreto Municipal | — | a confirmar |
| 🟢 368 | 01/04/2026 | — | auditada |
| 🟢 369 | 01/04/2026 | — | auditada |
| 🟢 370 | 01/04/2026 | — | auditada |
| 🟢 371 | 01/09/2026 | — | auditada |
| 🟢 372 | 01/09/2026 | — | auditada |
| 🟢 373 | 01/09/2026 | — | auditada |
| 🟢 374 | 01/09/2026 | — | auditada |
| 🟢 375 | 01/09/2026 | — | auditada |
| 🟢 376 | 01/06/2026 | — | auditada |
| 🟢 377 | 01/06/2026 | — | auditada |
| 🟢 378 | 01/06/2026 | — | auditada |
| 🟢 379 | 01/06/2026 | — | auditada |
| 🟡 380 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 381 | 01/01/2026 | — | auditada |
| 🟢 382 | 01/01/2026 | — | auditada |
| 🟢 383 | 01/01/2026 | — | auditada |
| 🟢 384 | 01/01/2026 | — | auditada |
| 🟢 385 | 01/12/2025 | — | auditada |
| 🟢 386 | 01/01/2026 | — | auditada |
| 🟢 387 | 01/01/2026 | — | auditada |
| 🟢 388 | 01/01/2026 | — | auditada |
| 🟢 389 | 01/01/2026 | — | auditada |
| 🟢 390 | 01/01/2026 | — | auditada |
| 🟢 391 | 01/01/2026 | — | auditada |
| 🟢 392 | 01/01/2026 | — | auditada |
| 🟢 393 | 01/12/2025 | — | auditada |
| 🟢 394 | 01/01/2026 | — | auditada |
| 🟢 395 | 01/01/2026 | — | auditada |
| 🟢 396 | 01/01/2026 | — | auditada |
| 🟢 397 | 01/01/2026 | — | auditada |
| 🟢 398 | 01/01/2026 | — | auditada |
| 🟢 399 | 01/01/2026 | — | auditada |
| 🟢 400 | 01/01/2026 | — | auditada |
| 🟢 401 | 01/12/2025 | — | auditada |
| 🟢 402 | 01/01/2026 | — | auditada |
| 🟢 403 | 01/01/2026 | — | auditada |
| 🟢 404 | 01/01/2026 | — | auditada |
| 🟢 405 | 01/01/2026 | — | auditada |
| 🟢 406 | 01/01/2026 | — | auditada |
| 🟢 407 | 01/01/2026 | — | auditada |
| 🟢 408 | 01/12/2025 | — | auditada |
| 🟢 409 | 01/01/2026 | — | auditada |
| 🟢 410 | 01/01/2026 | — | auditada |
| 🟢 411 | 01/01/2026 | — | auditada |
| 🟢 412 | 01/01/2026 | — | auditada |
| 🟢 413 | 01/01/2026 | — | auditada |
| 🟢 414 | 01/12/2025 | — | auditada |
| 🟢 415 | 01/01/2026 | — | auditada |
| 🟢 416 | 03/12/2025 | — | auditada |
| 🟢 417 | 03/12/2025 | — | auditada |
| 🟢 418 | 03/12/2025 | — | auditada |
| 🟢 419 | 03/12/2025 | — | auditada |
| 🟢 420 | 03/12/2025 | — | auditada |
| 🟢 421 | 29/12/2025 | — | auditada |
| 🟢 422 | 29/12/2025 | — | auditada |
| 🟢 423 | 29/12/2025 | — | auditada |
| 🟢 424 | 29/12/2025 | — | auditada |
| 🟢 425 | 29/12/2025 | — | auditada |
| 🟢 426 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 427 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 428 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 429 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 430 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 431 | 01/10/2026 | — | auditada |
| 🟢 432 | 01/10/2026 | — | auditada |
| 🟢 433 | 01/10/2026 | — | auditada |
| 🟢 434 | 01/10/2026 | — | auditada |
| 🟢 435 | 01/10/2026 | — | auditada |
| 🟢 436 | 19/12/2025 | 31/08/2026 | auditada |
| 🟢 437 | 19/12/2025 | 31/08/2026 | auditada |
| 🟢 438 | 01/01/2026 | 31/08/2026 | auditada |
| 🟢 439 | 01/01/2026 | 31/08/2026 | auditada |
| 🟢 440 | 15/03/2026 | 31/08/2026 | auditada |
| 🟢 441 | 15/03/2026 | 31/08/2026 | auditada |
| 🟢 442 | 15/03/2026 | 31/08/2026 | auditada |
| 🟢 443 | 15/03/2026 | 31/08/2026 | auditada |
| 🟢 444 | 15/03/2026 | 31/08/2026 | auditada |
| 🟢 445 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 446 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 447 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 448 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 449 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 450 | 01/02/2026 | 31/08/2026 | auditada |
| 🟢 451 | 01/02/2026 | 31/08/2026 | auditada |
| 🟢 452 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 453 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 454 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 455 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 456 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 457 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 458 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 459 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 460 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 461 | 01/05/2026 | 31/08/2026 | auditada |
| 🟡 462 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 463 | 01/03/2026 | — | auditada |
| 🟢 464 | 01/03/2026 | — | auditada |
| 🟢 465 | 01/03/2026 | — | auditada |
| 🟢 466 | 01/03/2026 | — | auditada |
| 🟢 467 | 01/03/2026 | — | auditada |
| 🟢 468 | 01/01/2026 | — | auditada |
| 🟢 469 | 01/01/2026 | — | auditada |
| 🟢 470 | 01/01/2026 | — | auditada |
| 🟢 471 | 01/01/2026 | — | auditada |
| 🟢 472 | 17/05/2026 | 31/08/2026 | auditada |
| 🟢 473 | 17/05/2026 | 31/08/2026 | auditada |
| 🟢 474 | 17/05/2026 | 31/08/2026 | auditada |
| 🟢 475 | 17/05/2026 | 31/08/2026 | auditada |
| 🟢 476 | 01/07/2026 | — | auditada |
| 🟢 477 | 01/07/2026 | — | auditada |
| 🟢 478 | 01/07/2026 | — | auditada |
| 🟢 479 | 01/07/2026 | — | auditada |
| 🟢 480 | 01/07/2026 | 31/08/2026 | auditada |
| 🟢 481 | 01/07/2026 | 31/08/2026 | auditada |
| 🟢 482 | 01/07/2026 | 31/08/2026 | auditada |
| 🟢 483 | 01/07/2026 | 31/08/2026 | auditada |
| 🟢 484 | 01/07/2026 | 31/08/2026 | auditada |
| 🟢 485 | 2026 | 31/08/2026 | auditada |
| 🟢 486 | 2026 | 31/08/2026 | auditada |
| 🟢 487 | 2026 | 31/08/2026 | auditada |
| 🟢 488 | 2026 | 31/08/2026 | auditada |
| 🟢 489 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 490 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 491 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 492 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 493 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 494 | 01/08/2025 | — | auditada |
| 🟢 495 | 01/08/2025 | — | auditada |
| 🟡 496 | Resoluções AGER-MT / Concessões | 31/08/2026 | a confirmar |
| 🟢 497 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 498 | 01/12/2025 | 31/08/2026 | auditada |
| 🟢 499 | 14/04/2025 | — | auditada |
| 🟢 500 | 14/04/2025 | — | auditada |
| 🟢 501 | 14/04/2025 | — | auditada |
| 🟢 502 | 14/04/2025 | — | auditada |
| 🟢 503 | 01/04/2026 | — | auditada |
| 🟢 504 | 01/04/2026 | — | auditada |
| 🟢 505 | 01/04/2026 | — | auditada |
| 🟢 506 | 01/04/2026 | — | auditada |
| 🟢 507 | 01/05/2026 | — | auditada |
| 🟢 508 | 01/05/2026 | — | auditada |
| 🟢 509 | 01/05/2026 | — | auditada |
| 🟢 510 | 01/05/2026 | — | auditada |
| 🟢 511 | 01/05/2026 | — | auditada |
| 🟢 512 | 01/12/2025 | — | auditada |
| 🟢 513 | 01/12/2025 | — | auditada |
| 🟢 514 | 01/12/2025 | — | auditada |
| 🟢 515 | 01/12/2025 | — | auditada |
| 🟡 516 | Estrutura Tarifária SANEAR | 31/08/2026 | a confirmar |
| 🟢 517 | 26/06/2026 | 31/08/2026 | auditada |
| 🟢 518 | 26/06/2026 | 31/08/2026 | auditada |
| 🟢 519 | 26/06/2026 | 31/08/2026 | auditada |
| 🟢 520 | 26/06/2026 | 31/08/2026 | auditada |
| 🟢 521 | 26/06/2026 | 31/08/2026 | auditada |
| 🟢 522 | 01/01/2026 | — | auditada |
| 🟢 523 | 01/01/2026 | — | auditada |
| 🟢 524 | 2022 | — | auditada |
| 🟢 525 | 2022 | — | auditada |
| 🟢 526 | 2022 | — | auditada |
| 🟢 527 | 2022 | — | auditada |
| 🟢 528 | 15/04/2026 | — | auditada |
| 🟢 529 | 15/04/2026 | — | auditada |
| 🟢 530 | 15/04/2026 | — | auditada |
| 🟢 531 | 15/04/2026 | — | auditada |
| 🟢 532 | 15/04/2026 | — | auditada |
| 🟢 533 | 15/04/2026 | — | auditada |
| 🟢 534 | 15/04/2026 | — | auditada |
| 🟢 535 | 15/04/2026 | — | auditada |
| 🟢 536 | 15/04/2026 | — | auditada |
| 🟢 537 | 15/04/2026 | — | auditada |
| 🟡 538 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 539 | 01/01/2026 | — | auditada |
| 🟢 540 | 01/01/2026 | — | auditada |
| 🟢 541 | 01/01/2026 | — | auditada |
| 🟢 542 | 01/01/2026 | — | auditada |
| 🟢 543 | 01/01/2026 | — | auditada |
| 🟢 544 | 01/01/2026 | — | auditada |
| 🟢 545 | 01/01/2026 | — | auditada |
| 🟢 546 | 01/01/2026 | — | auditada |
| 🟢 547 | 01/01/2026 | — | auditada |
| 🟢 548 | 01/01/2026 | — | auditada |
| 🟢 549 | 01/10/2026 | — | auditada |
| 🟢 550 | 01/10/2026 | — | auditada |
| 🟢 551 | 01/10/2026 | — | auditada |
| 🟢 552 | 01/10/2026 | — | auditada |
| 🟢 553 | 01/10/2026 | — | auditada |
| 🟢 554 | 01/08/2026 | — | auditada |
| 🟢 555 | 01/08/2026 | — | auditada |
| 🟢 556 | 01/08/2026 | 31/08/2026 | auditada |
| 🟢 557 | 2026 | 31/08/2026 | auditada |
| 🟢 558 | 2026 | 31/08/2026 | auditada |
| 🟢 559 | 2026 | 31/08/2026 | auditada |
| 🟢 560 | 2026 | 31/08/2026 | auditada |
| 🟢 561 | 2026 | 31/08/2026 | auditada |
| 🟢 562 | 02/09/2025 | — | auditada |
| 🟢 563 | 02/09/2025 | — | auditada |
| 🟢 564 | 02/09/2025 | — | auditada |
| 🟢 565 | 02/09/2025 | — | auditada |
| 🟢 566 | 2026 | — | auditada |
| 🟢 567 | 2026 | — | auditada |
| 🟢 568 | 2026 | — | auditada |
| 🟢 569 | 2026 | — | auditada |
| 🟡 570 | 2026 vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 571 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 572 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 573 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 574 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 575 | 01/05/2026 | 31/08/2026 | auditada |
| 🟢 576 | 08/03/2026 | — | auditada |
| 🟢 577 | 08/03/2026 | — | auditada |
| 🟢 578 | 08/03/2026 | — | auditada |
| 🟢 579 | 08/03/2026 | — | auditada |
| 🟢 580 | 08/03/2026 | — | auditada |
| 🟢 581 | 01/04/2026 | — | auditada |
| 🟢 582 | 01/04/2026 | — | auditada |
| 🟢 583 | 01/04/2026 | — | auditada |
| 🟢 584 | 01/04/2026 | — | auditada |
| 🟢 585 | 20/03/2025 | 31/08/2026 | auditada |
| 🟢 586 | 20/03/2025 | 31/08/2026 | auditada |
| 🟢 587 | 20/03/2025 | 31/08/2026 | auditada |
| 🟢 588 | 20/03/2025 | 31/08/2026 | auditada |
| 🟢 589 | 06/01/2026 | — | auditada |
| 🟢 590 | 06/01/2026 | — | auditada |
| 🟢 591 | 06/01/2026 | — | auditada |
| 🟢 592 | 06/01/2026 | — | auditada |
| 🟡 593 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 594 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 595 | 2026 | — | auditada |
| 🟢 596 | 2026 | — | auditada |
| 🟢 597 | 2026 | — | auditada |
| 🟢 598 | 2026 | — | auditada |
| 🟡 599 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 600 | 01/12/2025 | — | auditada |
| 🟢 601 | 01/12/2025 | — | auditada |
| 🟢 602 | 01/12/2025 | — | auditada |
| 🟢 603 | 01/12/2025 | — | auditada |
| 🟢 604 | 2026 | 31/08/2026 | auditada |
| 🟢 605 | 2026 | 31/08/2026 | auditada |
| 🟢 606 | 2026 | 31/08/2026 | auditada |
| 🟢 607 | 2026 | 31/08/2026 | auditada |
| 🟢 608 | 2026 | 31/08/2026 | auditada |
| 🟢 609 | 01/01/2026 | — | auditada |
| 🟢 610 | 01/01/2026 | — | auditada |
| 🟢 611 | 01/01/2026 | — | auditada |
| 🟡 612 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 613 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 614 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 615 | 2026 | 31/08/2026 | auditada |
| 🟢 616 | 2026 | 31/08/2026 | auditada |
| 🟢 617 | 2026 | 31/08/2026 | auditada |
| 🟢 618 | 2026 | 31/08/2026 | auditada |
| 🟢 619 | 2026 | 31/08/2026 | auditada |
| 🟢 620 | 2026 | 31/08/2026 | auditada |
| 🟢 621 | 2026 | 31/08/2026 | auditada |
| 🟢 622 | 2026 | 31/08/2026 | auditada |
| 🟢 623 | 01/11/2025 | 31/08/2026 | auditada |
| 🟢 624 | 01/11/2025 | 31/08/2026 | auditada |
| 🟢 625 | 01/11/2025 | 31/08/2026 | auditada |
| 🟢 626 | 01/11/2025 | 31/08/2026 | auditada |
| 🟢 627 | 28/06/2026 | 31/08/2026 | auditada |
| 🟢 628 | 28/06/2026 | 31/08/2026 | auditada |
| 🟢 629 | 28/06/2026 | 31/08/2026 | auditada |
| 🟢 630 | 28/06/2026 | 31/08/2026 | auditada |
| 🟢 631 | 28/06/2026 | 31/08/2026 | auditada |
| 🟢 632 | 2026 | 31/08/2026 | auditada |
| 🟢 633 | 2026 | 31/08/2026 | auditada |
| 🟢 634 | 2026 | 31/08/2026 | auditada |
| 🟢 635 | 2026 | 31/08/2026 | auditada |
| 🟢 636 | 2026 | 31/08/2026 | auditada |
| 🟢 637 | 01/09/2026 | — | auditada |
| 🟢 638 | 01/09/2026 | — | auditada |
| 🟢 639 | 01/09/2026 | — | auditada |
| 🟢 640 | 01/09/2026 | — | auditada |
| 🟢 641 | 01/09/2026 | — | auditada |
| 🟡 642 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 643 | 27/09/2026 | — | auditada |
| 🟢 644 | 27/09/2026 | — | auditada |
| 🟢 645 | 27/09/2026 | — | auditada |
| 🟢 646 | 27/09/2026 | — | auditada |
| 🟡 647 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 648 | 2025 | — | auditada |
| 🟢 649 | 2025 | — | auditada |
| 🟢 650 | 2025 | — | auditada |
| 🟢 651 | 2025 | — | auditada |
| 🟢 652 | 2025 | — | auditada |
| 🟢 653 | 01/03/2026 | — | auditada |
| 🟢 654 | 01/03/2026 | — | auditada |
| 🟢 655 | 01/03/2026 | — | auditada |
| 🟢 656 | 01/03/2026 | — | auditada |
| 🟢 657 | 01/03/2026 | — | auditada |
| 🟢 658 | 01/12/2025 | — | auditada |
| 🟢 659 | 01/12/2025 | — | auditada |
| 🟢 660 | 01/12/2025 | — | auditada |
| 🟢 661 | 01/12/2025 | — | auditada |
| 🟢 662 | 01/12/2025 | — | auditada |
| 🟢 663 | 01/12/2025 | — | auditada |
| 🟢 664 | 01/12/2025 | — | auditada |
| 🟢 665 | 01/12/2025 | — | auditada |
| 🟢 666 | 01/12/2025 | — | auditada |
| 🟢 667 | 01/12/2025 | — | auditada |
| 🟢 668 | 01/12/2025 | — | auditada |
| 🟢 669 | 01/12/2025 | — | auditada |
| 🟢 670 | 04/02/2026 | — | auditada |
| 🟢 671 | 04/02/2026 | — | auditada |
| 🟢 672 | 04/02/2026 | — | auditada |
| 🟢 673 | 04/02/2026 | — | auditada |
| 🟢 674 | 04/02/2026 | — | auditada |
| 🟢 675 | 04/02/2026 | — | auditada |
| 🟢 676 | 04/02/2026 | — | auditada |
| 🟢 677 | 04/02/2026 | — | auditada |
| 🟢 678 | 04/02/2026 | — | auditada |
| 🟢 679 | 03/01/2026 | 31/08/2026 | auditada |
| 🟢 680 | 03/01/2026 | 31/08/2026 | auditada |
| 🟢 681 | 03/01/2026 | 31/08/2026 | auditada |
| 🟢 682 | 03/01/2026 | 31/08/2026 | auditada |
| 🟢 683 | Estrutura tarifária 2026; aplicação publicada para março de 2026 | 31/08/2026 | auditada |

Os municípios da CORSAN cobram pela fórmula exponencial `PB × Cⁿ + SB` (seção 3.3), sem preço por faixa; o expoente `n` é o da coluna da categoria na Tabela de Exponenciais.

<!-- tabela: **Tabela 28** — A fórmula exponencial da CORSAN em cada tabela tarifária e categoria coletada -->
| Municípios | Categoria | PB (R$/m³) | SB (R$/mês) | Esgoto (R$/m³) |
| :--- | :--- | ---: | ---: | ---: |
| Porto Alegre (RS) | Residencial | 5,50 | 0,00 | 4,40 |
| Erechim (RS) | Residencial | 6,95 | 32,95 | 4,86 |
| Erechim (RS) | Comercial | 7,90 | 58,79 | 5,53 |
| Erechim (RS) | Pública | 7,90 | 117,40 | 5,53 |
| Santa Cruz do Sul (RS) | Residencial | 7,91 | 37,50 | 5,53 |
| Canoas (RS), Esteio (RS) | Residencial | 8,68 | 41,20 | 6,07 |
| Santa Cruz do Sul (RS) | Comercial | 8,98 | 66,92 | 6,28 |
| Santa Cruz do Sul (RS) | Pública | 8,98 | 133,64 | 6,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Residencial | 9,15 | 43,39 | 6,40 |
| Novo Hamburgo (RS) | Residencial | 9,44 | 44,20 | 0,00 |
| Canoas (RS), Esteio (RS) | Comercial | 9,88 | 73,48 | 6,91 |
| Canoas (RS), Esteio (RS) | Pública | 9,88 | 146,79 | 6,91 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Comercial | 10,41 | 77,41 | 7,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Pública | 10,41 | 154,64 | 7,28 |
| Novo Hamburgo (RS) | Comercial | 10,70 | 78,79 | 0,00 |
| Novo Hamburgo (RS) | Pública | 10,70 | 158,29 | 0,00 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Industrial | 11,83 | 154,64 | 8,28 |
| Novo Hamburgo (RS) | Industrial | 12,15 | 158,29 | 0,00 |

Três prestadores cobram todo o volume pelo preço da faixa em que cai o consumo (cobrança direta), e a CESAN soma uma parcela fixa que depende da faixa do consumo total a uma parcela variável em cascata. O programa as guarda em faixas equivalentes de 1 m³ nos degraus, que reproduzem a conta de cada m³ inteiro; a tabela mostra a regra.

<!-- tabela: **Tabela 29** — As estruturas de cobrança direta e de parcela fixa por faixa -->
| Município | Categoria | Forma | Regra |
| :--- | :--- | :--- | :--- |
| Cariacica (ES) | Residencial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 2,42/m³; 10–15 m³: fixa R$ 30,62 + R$ 4,84/m³; 15–20 m³: fixa R$ 36,44 + R$ 8,71/m³; 20–30 m³: fixa R$ 43,36 + R$ 10,46/m³; 30–50 m³: fixa R$ 51,60 + R$ 12,02/m³; > 50 m³: fixa R$ 61,41 + R$ 13,23/m³ |
| Cariacica (ES) | Comercial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 5,29/m³; 10–15 m³: fixa R$ 30,88 + R$ 7,93/m³; 15–20 m³: fixa R$ 38,60 + R$ 10,31/m³; 20–30 m³: fixa R$ 46,32 + R$ 12,38/m³; 30–50 m³: fixa R$ 55,58 + R$ 13,61/m³; > 50 m³: fixa R$ 66,70 + R$ 14,97/m³ |
| Cariacica (ES) | Pública | parcela fixa por faixa | 0–10 m³: fixa R$ 28,31 + R$ 5,40/m³; 10–15 m³: fixa R$ 33,97 + R$ 7,56/m³; 15–20 m³: fixa R$ 42,46 + R$ 9,83/m³; 20–30 m³: fixa R$ 50,95 + R$ 11,80/m³; 30–50 m³: fixa R$ 58,59 + R$ 12,98/m³; > 50 m³: fixa R$ 67,38 + R$ 13,63/m³ |
| Cariacica (ES) | Industrial | parcela fixa por faixa | 0–10 m³: fixa R$ 56,61 + R$ 6,67/m³; 10–15 m³: fixa R$ 67,93 + R$ 10,00/m³; 15–20 m³: fixa R$ 81,52 + R$ 12,00/m³; 20–30 m³: fixa R$ 97,83 + R$ 13,20/m³; 30–50 m³: fixa R$ 112,50 + R$ 14,52/m³; > 50 m³: fixa R$ 129,37 + R$ 15,61/m³ |
| Cariacica (ES) | Social | parcela fixa por faixa | 0–10 m³: fixa R$ 6,43 + R$ 0,61/m³; 10–15 m³: fixa R$ 7,66 + R$ 1,21/m³; 15–20 m³: fixa R$ 9,11 + R$ 4,36/m³; 20–30 m³: fixa R$ 10,84 + R$ 10,46/m³; 30–50 m³: fixa R$ 12,90 + R$ 12,02/m³; > 50 m³: fixa R$ 15,35 + R$ 13,23/m³ |
| Guarapari (ES) | Residencial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 2,42/m³; 10–15 m³: fixa R$ 30,62 + R$ 4,84/m³; 15–20 m³: fixa R$ 36,44 + R$ 8,71/m³; 20–30 m³: fixa R$ 43,36 + R$ 10,46/m³; 30–50 m³: fixa R$ 51,60 + R$ 12,02/m³; > 50 m³: fixa R$ 61,41 + R$ 13,23/m³ |
| Guarapari (ES) | Comercial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 5,29/m³; 10–15 m³: fixa R$ 30,88 + R$ 7,93/m³; 15–20 m³: fixa R$ 38,60 + R$ 10,31/m³; 20–30 m³: fixa R$ 46,32 + R$ 12,38/m³; 30–50 m³: fixa R$ 55,58 + R$ 13,61/m³; > 50 m³: fixa R$ 66,70 + R$ 14,97/m³ |
| Guarapari (ES) | Pública | parcela fixa por faixa | 0–10 m³: fixa R$ 28,31 + R$ 5,40/m³; 10–15 m³: fixa R$ 33,97 + R$ 7,56/m³; 15–20 m³: fixa R$ 42,46 + R$ 9,83/m³; 20–30 m³: fixa R$ 50,95 + R$ 11,80/m³; 30–50 m³: fixa R$ 58,59 + R$ 12,98/m³; > 50 m³: fixa R$ 67,38 + R$ 13,63/m³ |
| Guarapari (ES) | Industrial | parcela fixa por faixa | 0–10 m³: fixa R$ 56,61 + R$ 6,67/m³; 10–15 m³: fixa R$ 67,93 + R$ 10,00/m³; 15–20 m³: fixa R$ 81,52 + R$ 12,00/m³; 20–30 m³: fixa R$ 97,83 + R$ 13,20/m³; 30–50 m³: fixa R$ 112,50 + R$ 14,52/m³; > 50 m³: fixa R$ 129,37 + R$ 15,61/m³ |
| Guarapari (ES) | Social | parcela fixa por faixa | 0–10 m³: fixa R$ 6,43 + R$ 0,61/m³; 10–15 m³: fixa R$ 7,66 + R$ 1,21/m³; 15–20 m³: fixa R$ 9,11 + R$ 4,36/m³; 20–30 m³: fixa R$ 10,84 + R$ 10,46/m³; 30–50 m³: fixa R$ 12,90 + R$ 12,02/m³; > 50 m³: fixa R$ 15,35 + R$ 13,23/m³ |
| Serra (ES) | Residencial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 2,42/m³; 10–15 m³: fixa R$ 30,62 + R$ 4,84/m³; 15–20 m³: fixa R$ 36,44 + R$ 8,71/m³; 20–30 m³: fixa R$ 43,36 + R$ 10,46/m³; 30–50 m³: fixa R$ 51,60 + R$ 12,02/m³; > 50 m³: fixa R$ 61,41 + R$ 13,23/m³ |
| Serra (ES) | Comercial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 5,29/m³; 10–15 m³: fixa R$ 30,88 + R$ 7,93/m³; 15–20 m³: fixa R$ 38,60 + R$ 10,31/m³; 20–30 m³: fixa R$ 46,32 + R$ 12,38/m³; 30–50 m³: fixa R$ 55,58 + R$ 13,61/m³; > 50 m³: fixa R$ 66,70 + R$ 14,97/m³ |
| Serra (ES) | Pública | parcela fixa por faixa | 0–10 m³: fixa R$ 28,31 + R$ 5,40/m³; 10–15 m³: fixa R$ 33,97 + R$ 7,56/m³; 15–20 m³: fixa R$ 42,46 + R$ 9,83/m³; 20–30 m³: fixa R$ 50,95 + R$ 11,80/m³; 30–50 m³: fixa R$ 58,59 + R$ 12,98/m³; > 50 m³: fixa R$ 67,38 + R$ 13,63/m³ |
| Serra (ES) | Industrial | parcela fixa por faixa | 0–10 m³: fixa R$ 56,61 + R$ 6,67/m³; 10–15 m³: fixa R$ 67,93 + R$ 10,00/m³; 15–20 m³: fixa R$ 81,52 + R$ 12,00/m³; 20–30 m³: fixa R$ 97,83 + R$ 13,20/m³; 30–50 m³: fixa R$ 112,50 + R$ 14,52/m³; > 50 m³: fixa R$ 129,37 + R$ 15,61/m³ |
| Serra (ES) | Social | parcela fixa por faixa | 0–10 m³: fixa R$ 6,43 + R$ 0,61/m³; 10–15 m³: fixa R$ 7,66 + R$ 1,21/m³; 15–20 m³: fixa R$ 9,11 + R$ 4,36/m³; 20–30 m³: fixa R$ 10,84 + R$ 10,46/m³; 30–50 m³: fixa R$ 12,90 + R$ 12,02/m³; > 50 m³: fixa R$ 15,35 + R$ 13,23/m³ |
| Vila Velha (ES) | Residencial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 2,42/m³; 10–15 m³: fixa R$ 30,62 + R$ 4,84/m³; 15–20 m³: fixa R$ 36,44 + R$ 8,71/m³; 20–30 m³: fixa R$ 43,36 + R$ 10,46/m³; 30–50 m³: fixa R$ 51,60 + R$ 12,02/m³; > 50 m³: fixa R$ 61,41 + R$ 13,23/m³ |
| Vila Velha (ES) | Comercial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 5,29/m³; 10–15 m³: fixa R$ 30,88 + R$ 7,93/m³; 15–20 m³: fixa R$ 38,60 + R$ 10,31/m³; 20–30 m³: fixa R$ 46,32 + R$ 12,38/m³; 30–50 m³: fixa R$ 55,58 + R$ 13,61/m³; > 50 m³: fixa R$ 66,70 + R$ 14,97/m³ |
| Vila Velha (ES) | Pública | parcela fixa por faixa | 0–10 m³: fixa R$ 28,31 + R$ 5,40/m³; 10–15 m³: fixa R$ 33,97 + R$ 7,56/m³; 15–20 m³: fixa R$ 42,46 + R$ 9,83/m³; 20–30 m³: fixa R$ 50,95 + R$ 11,80/m³; 30–50 m³: fixa R$ 58,59 + R$ 12,98/m³; > 50 m³: fixa R$ 67,38 + R$ 13,63/m³ |
| Vila Velha (ES) | Industrial | parcela fixa por faixa | 0–10 m³: fixa R$ 56,61 + R$ 6,67/m³; 10–15 m³: fixa R$ 67,93 + R$ 10,00/m³; 15–20 m³: fixa R$ 81,52 + R$ 12,00/m³; 20–30 m³: fixa R$ 97,83 + R$ 13,20/m³; 30–50 m³: fixa R$ 112,50 + R$ 14,52/m³; > 50 m³: fixa R$ 129,37 + R$ 15,61/m³ |
| Vila Velha (ES) | Social | parcela fixa por faixa | 0–10 m³: fixa R$ 6,43 + R$ 0,61/m³; 10–15 m³: fixa R$ 7,66 + R$ 1,21/m³; 15–20 m³: fixa R$ 9,11 + R$ 4,36/m³; 20–30 m³: fixa R$ 10,84 + R$ 10,46/m³; 30–50 m³: fixa R$ 12,90 + R$ 12,02/m³; > 50 m³: fixa R$ 15,35 + R$ 13,23/m³ |
| Vitória (ES) | Residencial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 2,42/m³; 10–15 m³: fixa R$ 30,62 + R$ 4,84/m³; 15–20 m³: fixa R$ 36,44 + R$ 8,71/m³; 20–30 m³: fixa R$ 43,36 + R$ 10,46/m³; 30–50 m³: fixa R$ 51,60 + R$ 12,02/m³; > 50 m³: fixa R$ 61,41 + R$ 13,23/m³ |
| Vitória (ES) | Comercial | parcela fixa por faixa | 0–10 m³: fixa R$ 25,73 + R$ 5,29/m³; 10–15 m³: fixa R$ 30,88 + R$ 7,93/m³; 15–20 m³: fixa R$ 38,60 + R$ 10,31/m³; 20–30 m³: fixa R$ 46,32 + R$ 12,38/m³; 30–50 m³: fixa R$ 55,58 + R$ 13,61/m³; > 50 m³: fixa R$ 66,70 + R$ 14,97/m³ |
| Vitória (ES) | Pública | parcela fixa por faixa | 0–10 m³: fixa R$ 28,31 + R$ 5,40/m³; 10–15 m³: fixa R$ 33,97 + R$ 7,56/m³; 15–20 m³: fixa R$ 42,46 + R$ 9,83/m³; 20–30 m³: fixa R$ 50,95 + R$ 11,80/m³; 30–50 m³: fixa R$ 58,59 + R$ 12,98/m³; > 50 m³: fixa R$ 67,38 + R$ 13,63/m³ |
| Vitória (ES) | Industrial | parcela fixa por faixa | 0–10 m³: fixa R$ 56,61 + R$ 6,67/m³; 10–15 m³: fixa R$ 67,93 + R$ 10,00/m³; 15–20 m³: fixa R$ 81,52 + R$ 12,00/m³; 20–30 m³: fixa R$ 97,83 + R$ 13,20/m³; 30–50 m³: fixa R$ 112,50 + R$ 14,52/m³; > 50 m³: fixa R$ 129,37 + R$ 15,61/m³ |
| Vitória (ES) | Social | parcela fixa por faixa | 0–10 m³: fixa R$ 6,43 + R$ 0,61/m³; 10–15 m³: fixa R$ 7,66 + R$ 1,21/m³; 15–20 m³: fixa R$ 9,11 + R$ 4,36/m³; 20–30 m³: fixa R$ 10,84 + R$ 10,46/m³; 30–50 m³: fixa R$ 12,90 + R$ 12,02/m³; > 50 m³: fixa R$ 15,35 + R$ 13,23/m³ |
| Lucas do Rio Verde (MT) | Residencial | cobrança direta | até 10 m³, R$ 24,30/mês; acima, todo o volume a R$ 3,12–8,20/m³, pelo preço do consumo |
| Lucas do Rio Verde (MT) | Comercial | cobrança direta | até 10 m³, R$ 55,90/mês; acima, todo o volume a R$ 7,72–9,17/m³, pelo preço do consumo |
| Lucas do Rio Verde (MT) | Pública | cobrança direta | até 10 m³, R$ 69,70/mês; acima, todo o volume a R$ 9,77–11,20/m³, pelo preço do consumo |
| Lucas do Rio Verde (MT) | Industrial | cobrança direta | até 10 m³, R$ 55,30/mês; acima, todo o volume a R$ 7,72–9,45/m³, pelo preço do consumo |
| Lucas do Rio Verde (MT) | Social | cobrança direta | até 10 m³, R$ 12,20/mês; acima, todo o volume a R$ 1,56–4,10/m³, pelo preço do consumo |
| Americana (SP) | Residencial | cobrança direta | até 6 m³, R$ 14,30/mês; acima, todo o volume a R$ 2,47–12,72/m³, pelo preço do consumo |
| Americana (SP) | Comercial | cobrança direta | até 10 m³, R$ 52,24/mês; acima, todo o volume a R$ 5,36–25,48/m³, pelo preço do consumo |
| Americana (SP) | Pública | cobrança direta | até 6 m³, R$ 14,30/mês; acima, todo o volume a R$ 2,47–12,72/m³, pelo preço do consumo |
| Americana (SP) | Industrial | cobrança direta | até 10 m³, R$ 78,36/mês; acima, todo o volume a R$ 8,04–38,20/m³, pelo preço do consumo |
| Americana (SP) | Social | cobrança direta | até 6 m³, R$ 7,14/mês; acima, todo o volume a R$ 1,24–12,72/m³, pelo preço do consumo |
| Valinhos (SP) | Residencial | cobrança direta | até 10 m³, R$ 23,73/mês; acima, todo o volume a R$ 4,40–22,18/m³, pelo preço do consumo |
| Valinhos (SP) | Comercial | cobrança direta | até 10 m³, R$ 94,91/mês; acima, todo o volume a R$ 15,06–41,00/m³, pelo preço do consumo |
| Valinhos (SP) | Pública | cobrança direta | até 10 m³, R$ 24,92/mês; acima, todo o volume a R$ 4,62–23,29/m³, pelo preço do consumo |
| Valinhos (SP) | Industrial | cobrança direta | até 10 m³, R$ 130,09/mês; acima, todo o volume a R$ 18,91–55,80/m³, pelo preço do consumo |
| Valinhos (SP) | Social | cobrança direta | até 10 m³, R$ 11,87/mês; acima, todo o volume a R$ 2,20–11,09/m³, pelo preço do consumo |

---

## Apêndice F — Arquivos, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

### F.1. O que o programa lê

<!-- tabela: **Tabela 30** — Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto do Netuno 4 ou da série 5.0 inicial | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia | etapa 1. Projeto e Chuva |
| demanda diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de demanda, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um arquivo desses, o programa avisa e adota os valores
> padrão para o que falta. A seção 3.8 mostra o que conferir depois de importar.

---

### F.2. O que o programa escreve

<!-- tabela: **Tabela 31** — Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Salvar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| planilha | `.xlsx` | série diária, varredura e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV você escolhe o separador: **ponto e vírgula** para abrir no Excel
em português, **vírgula** para o padrão internacional. Escolher errado faz a planilha
abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um arquivo JSON com as
propriedades dos componentes, para compatibilização BIM. A seção 3.9 trata de todos.

---

### F.3. O arquivo de projeto, por dentro

O `.triton` é um arquivo de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete seções:

<!-- tabela: **Tabela 32** — As sete seções do arquivo de projeto e o que cada uma guarda -->
| Seção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a motobomba |
| `water_quality_and_etap` | classe-alvo, desinfecção e tratamento |
| `financial_and_economic` | tarifas, impostos, reajustes e prazo |

O apêndice A (volume Apêndices) lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do arquivo.** É o que torna o projeto reproduzível:
> quem receber o arquivo obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um arquivo e muito para um anexo de e-mail com
> vinte deles.

---

### F.4. Onde ficam as coisas

<!-- tabela: **Tabela 33** — Localização dos arquivos do programa e dos arquivos do usuário -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| a base de tarifas dos 652 municípios | dentro do programa |
| os casos do manual | na pasta do programa, em `casos` |
| os três estudos de referência | na pasta do programa, em `exemplos` |
| a base climática nacional, se instalada | onde o instalador dela indicar |
| **os seus projetos e relatórios** | **onde você escolher ao salvar** |

O programa não cria pasta de trabalho nem guarda arquivos escondidos. Cada gravação
pergunta o destino, e nada do que você produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada seu.

---

### F.5. O arquivo de estudo em lote (`estudo.json`)

Usado por `triton estudo` (capítulo «Comparar muitos casos de uma vez»). Esquema `triton-estudo`, versão 1.

<!-- tabela: **Tabela 34** — Seções do arquivo estudo.json (esquema triton-estudo, versão 1) -->
| Seção | Conteúdo |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; outra versão é recusada |
| `estudo` | `id` (letras, números, ponto, hífen e sublinhado), `titulo`, `tipologia` (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario` ou `outra`), `tipologia_rotulo`, `autores`, `nota` |
| `projeto_base` | `arquivo`: um `.triton`, com caminho relativo ao `estudo.json`; ou `modelo`: `"edicao"`, o modelo de projeto da edição (então cada caso informa área, demanda, fração e chuva: nada é presumido) |
| `padroes` | `substituicoes`, `clima` e `tarifa` aplicados a todos os casos; o que o caso declara vence o padrão |
| `casos` | lista; cada caso tem `id`, `nome`, `grupo` (por padrão, a tipologia), `projeto` (outro `.triton` para este caso), `clima`, `tarifa`, `substituicoes` e `dimensoes` (rótulos livres que viram colunas do CSV). Pode faltar se houver `expansao` |
| `expansao` | **só na Edição Brasil.** Gera um caso por município × modelo × recorte da CLIMBra: `municipios` (lista de `municipio`, `uf`, `ibge`), `uf` (padrão dos municípios), `modelos` (`"todos"` ou uma lista dos 19) e `recortes` (lista de `id`, `rotulo`, `cenario` `HIST`, `SSP245` ou `SSP585`, `inicio`, `fim`). Os casos expandidos somam-se aos explícitos |
| `clima` | `arquivo` (série diária de chuva, CSV) **ou** `climbra` (só na Edição Brasil, veja abaixo), `data_inicio` (dd/mm/aaaa), `nome` e `fonte` (rótulos que vão para a procedência) |
| `tarifa` | **só na Edição Brasil.** `municipio`, `uf` (por padrão, os de `clima.climbra`), `categoria` (`residencial`, `comercial`, `publica`, `industrial` ou `social`) e `se_ausente` (`erro`, o padrão, ou `residencial`): aplica as tarifas de água, esgoto e energia do catálogo do programa, como a aba Projeto. Não aceita preços |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` ou `all`), `volume` (`otimo_tecnico`, `topsis` ou um volume em litros), `pesos` (TOPSIS: quatro pesos de eixo, técnico, econômico, ambiental e estrutural, ou oito, um por critério; três, de estudos até a 0.1.0, ainda valem, e o eixo estrutural recebe a média deles), `partes_no_eixo` (oito valores, na ordem dos critérios da seção 2.10 (volume O método); padrão: partes iguais) e `semente` |
| `saidas` | `formatos` (`csv`, `json`, `md`, `tex`, `xlsx`), `metricas`, `casas_decimais` (um inteiro ou uma por métrica), `idioma` (`auto`, `pt-BR`, `pt-PT`, `en`, `es`, `zh`), `milhar`, `legenda` `orientacao` (`casos_nas_linhas` ou `metricas_nas_linhas`) e `gravar_analise` (`true` por padrão; `false` não grava `analise.json` por caso, o que poupa disco em estudos com milhares de casos) |

Chaves que começam por `_` são comentários e o programa as ignora. Campo vazio, `null` ou «XX» é «a preencher»: a validação o recusa e diz onde está. Uma chave desconhecida é erro, com a sugestão da mais parecida. `triton estudo esquema` imprime o JSON Schema do arquivo, para completar e conferir no editor.

#### F.5.1. Clima da CLIMBra, tarifa e expansão (só na Edição Brasil)

`clima.climbra` busca a série diária na base CLIMBra do programa: `municipio` (nome como na base; obrigatório), `uf` (confere o município com o catálogo de tarifas e afasta nomes repetidos em outras UFs), `ibge` (código de sete dígitos, só informativo), `modelo` (um dos 19; padrão `INM-CM4`), `cenario` (`HIST`, `SSP245`, `SSP585`; padrão `HIST`) e `inicio`/`fim` (dd/mm/aaaa; padrão, a série inteira do cenário). `arquivo` e `climbra` não convivem no mesmo bloco. Nos `padroes`, `climbra` pode trazer só `modelo` e `cenario`, e o caso completa com o município: os campos se somam. Os modelos de calendário de 360 dias têm um dia a menos no fim do século, e o caso avisa quando a série devolvida é mais curta que o recorte pedido. As saídas registram o SHA-256 do banco `climbra_<modelo>.db` e do catálogo de tarifas usados, além do SHA-256 da série (dias, total e hash).

Na International e na Ibérica, `clima.climbra`, `tarifa` e `expansao` são recusados na validação com a mensagem de que só existem na Edição Brasil; `clima.arquivo` continua valendo.

Com `expansao`, o `resultados.csv` ganha as colunas `municipio`, `ibge`, `modelo`, `recorte`, `cenario`, `inicio` e `fim` entre `grupo` e `metrica`: uma linha por município, modelo, recorte e métrica.

#### F.5.2. Apelidos das substituições

<!-- tabela: **Tabela 35** — Apelidos das substituições e o campo do projeto que cada um altera -->
| Apelido | Campo do projeto | Unidade |
| :--- | :--- | :--- |
| `area_captacao_m2` | `area` | m² |
| `coeficiente_escoamento` | `runoff_coeff` | 0 a 1 |
| `descarte_mm` | `discard` | mm |
| `usuarios` (também `populacao`, `pessoas`, `ocupantes`) | `residents_count` | pessoas |
| `demanda_per_capita_l_dia` | `demand_value` | L/pessoa·dia |
| `demanda_total_l_dia` | `demand_value` (a demanda total dividida pelos usuários) | L/dia |
| `fracao_pluvial_pct` ou `fracao_pluvial` | `rainwater_share` | % ou 0 a 1 |
| `volume_reservatorio_l` | `lower_tank_fixed` (e `lower_tank_mode` = volume fixo) | L |
| `volume_maximo_l`, `passo_volume_l` | `lower_tank_max` (varredura), `lower_tank_step` | L |
| `reservatorio_superior_l` | `upper_tank_vol` (e `upper_tank_used`) | L |
| `limiar_bombeamento_l`, `economias`, `irrigacao_l_dia` | `pumping_threshold`, `num_economias`, `irrigation_liters_per_day` | L, unidades, L/dia |
| `data_inicio`, `regra_phi`, `delta_ideal_pct` | `start_date`, `phi_operation_rule`, `delta_ideal` | dd/mm/aaaa, 0 a 1, %/m³ |
| `periodo_analise_anos`, `tma_pct_mes`, `tarifa_energia` | `analysis_period_years`, `tma`, `elec_tariff` | anos, % ao mês, moeda/kWh |

Além dos apelidos, a chave de uma substituição pode ser **qualquer campo que `--set` aceita** (por exemplo `cost_labor`) ou um **caminho pontilhado do próprio `.triton`**, como `inputs.building_and_demand.catchment_area_m2`. O caminho precisa existir no projeto e o valor precisa ter o mesmo tipo do que já está lá; senão o caso termina com erro claro, que lista as chaves disponíveis. Um apelido desconhecido também é recusado, com a sugestão do mais parecido. Dois nomes para o mesmo parâmetro no mesmo caso (`area_captacao_m2` e `area_m2`, ou `fracao_pluvial` e `fracao_pluvial_pct`) são conflito. A fração em 0 a 1 recusa 40 (provável percentual); o percentual recusa fora de 0 a 100.

As substituições passam pela mesma conciliação de frações do `--set`, e o preenchimento preliminar de custos (CAPEX) roda **depois** delas, de modo que o preço da cisterna acompanha o volume do caso. `triton estudo apelidos` lista todos os apelidos e métricas, na língua da edição.

#### F.5.3. Saídas do estudo

<!-- tabela: **Tabela 36** — Arquivos que triton estudo run grava na pasta de saída -->
| Arquivo | Conteúdo |
| :--- | :--- |
| `resultados.csv` | formato **tidy**: uma linha por caso e métrica (`estudo_id`, `caso_id`, `caso`, `grupo`, `metrica`, `rotulo`, `valor`, `unidade`, `status`); ponto decimal, sem separador de milhar, UTF-8 |
| `resultados.json` | os mesmos valores, mais a **proveniência**: versão do Triton, edição, SHA-256 do `estudo.json` e de cada projeto e série de chuva, fonte, crédito e licença da chuva, avisos e a data de execução |
| `tabela.md` | tabela em Markdown, com os números no formato do idioma (vírgula decimal em português e espanhol, ponto em inglês e chinês) |
| `tabela.tex` | tabela LaTeX com `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), pronta para colar; precisa de `\usepackage{booktabs}` |
| `tabela.xlsx` | opcional (`xlsx` em `formatos`): números de verdade, formatados, mais as abas `tidy` e `proveniencia` |
| `resumo.md` | resumo curto: casos, faixa de cada resultado, avisos, fontes e licenças |
| `casos/<id>/resultado.json` e `analise.json` | todas as métricas do caso e a análise completa do motor (é o que o `resumo` e o `texto` leem) |
| `estudo.json` | cópia do estudo que gerou a pasta |
| `consolidado.csv` e `consolidado.md` | gravados por `triton estudo consolidar` (não pelo `run`): uma linha por tipologia (`grupo`), caso, métrica e unidade, com `n`, mínimo, média, mediana e máximo dos `resultados.csv` encontrados |

As saídas não levam caminho absoluto: os projetos aparecem com caminho relativo ao `estudo.json` (ou só o nome). Duas execuções do mesmo estudo dão arquivos idênticos; a data de execução é a única diferença, e a variável de ambiente `SOURCE_DATE_EPOCH` a fixa. O `xlsx` guarda a data de criação nas propriedades do arquivo e não é idêntico byte a byte, só no conteúdo.

**Retomada e códigos de saída.** Numa pasta de saída que já tem resultados, `run` exige `--retomar` (pula os casos prontos e inalterados: a impressão digital do caso inclui o estudo, os arquivos, a versão e a edição) ou `--sobrescrever` (refaz tudo). O código de saída é 0 se todos os casos foram calculados, 1 se algum caso terminou com erro (as saídas dos demais são gravadas e o caso com erro aparece com `status` `erro`) e 2 se o estudo ou os argumentos são inválidos.

**Métricas.** O volume de cada caso é, por padrão, o ótimo técnico da varredura (`volume: "otimo_tecnico"`); com `"topsis"`, o primeiro do ranking; com um número, o volume fixo. As métricas disponíveis incluem `volume_l`, `economia_agua_potavel_pct`, `agua_pluvial_m3_ano`, `agua_potavel_m3_ano`, `extravasamento_m3_ano`, os dias com atendimento total, parcial e nulo, `capex`, `vpl`, `economia_anual_agua`, `opex_anual`, `tir_anual_pct`, `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` e `aceitabilidade_smaa_pct`, além das entradas do caso (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). As métricas econômicas pedem `analise.tipo` `economic` ou `all`; as ambientais, `environmental` ou `all`. Os nomes crus do relatório (`potable_savings_pct`) também valem. Valores monetários saem na moeda de cada projeto; se os casos têm moedas diferentes, o resumo avisa que não são comparáveis e o comparativo não os agrega. Com CAPEX igual a zero (custos não informados), o resumo avisa que VPL, TIR e payback não são resultados.

**Texto com os números.** `triton estudo texto` substitui no seu modelo `.md` os marcadores cercados por chaves duplas (duas de cada lado; os exemplos abaixo vêm sem elas): `economia_agua_potavel_pct:caso-01` (o valor de um caso), `economia_agua_potavel_pct:@min`, `@max`, `@media`, `@mediana` (sobre os casos calculados; `@media(escolar)` restringe a um grupo), `n_casos` e, depois de uma barra vertical, as casas decimais (`vpl:caso-01|0`). Onde falta resultado o marcador vira «XX» e o comando lista as pendências (com `--estrito`, termina com código 1). Métrica desconhecida é erro.

### F.6. Compatibilidade entre versões

<!-- tabela: **Tabela 37** — Compatibilidade entre versões do arquivo de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o padrão |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto do Netuno 4 em CSV | abre com aviso; confira o que a seção 3.8 lista |
| arquivo JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um arquivo JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores padrão — e o usuário
simularia 100 m² acreditando simular os 180 m² que o arquivo descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.

---

## Apêndice G — Glossário

Termos técnicos e siglas, com o equivalente em inglês quando ele é usado na
literatura, acompanhados das diretrizes de padronização terminológica do Triton.

---

**AAC** (*aproveitamento de água de chuva*). Emprego de água precipitada sobre coberturas
para usos não potáveis em edificações, regulamentado no Brasil pela ABNT NBR 15527:2019.
Deve-se preferir o termo «aproveitamento» a «reúso», uma vez que a água de chuva captada
na cobertura é um recurso primário e não um efluente gerado por uso antrópico anterior.

**ABNT**. Associação Brasileira de Normas Técnicas, o organismo que publica as normas
brasileiras. Uma norma é identificada pela sigla NBR seguida do número e do ano da
edição, como em ABNT NBR 15527:2019.

**ACV** (*life cycle assessment*). Avaliação de ciclo de vida. Método que contabiliza os
impactos ambientais de um produto ao longo de toda a sua existência, da extração das
matérias-primas ao descarte. A do programa é de **triagem**, e não um inventário completo
conforme a ISO 14040.

**COSIP**. Contribuição para o Custeio do Serviço de Iluminação Pública, cobrada pelos municípios na fatura de energia elétrica. A tarifa B1 da base não a inclui.

**GFDL-CM4**. Modelo climático do Geophysical Fluid Dynamics Laboratory (NOAA), um dos modelos do CMIP6 de que a base CLIMBra traz séries.

**ICMS**. Imposto sobre Circulação de Mercadorias e Serviços, estadual, que incide sobre a energia elétrica. A tarifa B1 da base não o inclui.

**KACE**. Modelo climático KACE-1-0-G, do Serviço Meteorológico da Coreia (KMA), um dos modelos do CMIP6 da base CLIMBra; usa calendário de 360 dias.

**MS**. Mato Grosso do Sul, unidade da federação; aparece nas tabelas de custo por estado.

**OPEX** (*operational expenditure*). Custo anual de operação e manutenção: energia da bomba, cloro, manutenções periódicas e troca de componentes. Entra na análise econômica ao lado do CAPEX.

**PIS**. PIS/Pasep, contribuição federal que incide, com a Cofins, sobre a fatura de energia elétrica. A tarifa B1 da base não a inclui.

**RS**. Rio Grande do Sul, unidade da federação; aparece nas tabelas de custo por estado.

**SHA-256**. Função de resumo criptográfico (hash) de 256 bits. O programa a usa para registrar a identidade de cada arquivo de dados e de cada documento de fonte, de modo que uma alteração seja detectável.

**SIRENE**. Sistema de Registro Nacional de Emissões, do MCTI, que publica o fator médio de emissão da rede elétrica brasileira.

**Água de chuva** (*rainwater*). Precipitação atmosférica coletada diretamente em
superfícies impermeáveis de cobertura (telhados e lajes impermeabilizadas), antes de atingir
o solo ou galerias públicas. É o termo técnico-normativo oficial consagrado pela ABNT NBR
15527:2019. Deve-se utilizar rigorosamente «água de chuva» para designar o recurso natural
e a fonte hídrica captada, evitando a forma coloquial «água da chuva».

**Água não potável** (*non-potable water*). Água que não se destina ao consumo humano direto,
mas atende aos padrões de qualidade física, química e microbiológica estabelecidos por
normas específicas (como a Tabela 1 da ABNT NBR 15527:2019 e a ABNT NBR 16783:2019) para
usos admitidos: descargas em bacias sanitárias e mictórios, lavagem de veículos, calçadas e
pisos, irrigação paisagística, lavagem de roupas e torres de resfriamento.

**Água pluvial** (*stormwater*, *pluvial water*). Água de chuva que escoa superficialmente
por superfícies urbanas ou é conduzida por canalizações e sistemas prediais de drenagem
(ABNT NBR 10844). No Triton, o termo aplica-se preferencialmente à infraestrutura predial
e aos componentes de engenharia: *sistema de aproveitamento de água pluvial (SAAP)*, *rede
pluvial*, *demanda pluvial*, *consumo de água pluvial* e *extravasamento pluvial*.

**Água potável** (*potable water*, *drinking water*). Água que atende integralmente aos
padrões de potabilidade definidos pela Portaria GM/MS nº 888/2021 do Ministério da Saúde,
destinada à ingestão direta, preparação de alimentos e higiene pessoal.

**ANEEL**. Agência Nacional de Energia Elétrica, que homologa as tarifas das
distribuidoras de energia. O Triton lê delas o preço da energia do bombeamento, e a
atualização das tarifas é feita a partir dos dados abertos da agência.

**AQUA-HQE**. Referencial de certificação ambiental de edificações, adaptação brasileira
do francês HQE conduzida pela Fundação Vanzolini. No referencial residencial de 2024, a
água é tratada no tema «Consumo de água», em itens classificados nos níveis PR, HQE,
HQE 2 e HQE 3.

**Área de captação** (*catchment area*). Área projetada na **horizontal** da superfície
impermeável da cobertura onde a água é captada, conforme o item 3.6 da NBR 15527:2019.
Não é a área inclinada do telhado, nem a área de contribuição da NBR 10844, que serve
ao dimensionamento de calhas.

**Bandeira tarifária**. Acréscimo ou desconto sobre a tarifa de energia elétrica,
conforme as condições de geração. Verde, amarela, vermelha 1, vermelha 2, e a
modalidade branca.

**BD+C** (*Building Design and Construction*). Família de referenciais do LEED
para projeto e construção de edificações novas ou em grande reforma. É a família
tratada neste manual, nas versões 4, 4.1 e 5.

**BIM** (*building information modeling*). Modelagem da informação da construção.
Representação digital da edificação em que cada componente carrega propriedades além da
geometria, o que permite compatibilizar projetos de disciplinas diferentes.

**BRL**. Sigla da Edição Brasil do programa, a que traz os dados brasileiros: base
climática CLIMBra, tarifas de 652 municípios, energia da ANEEL, custos em reais e
certificações nacionais. A seção 1.2 (volume Comece aqui) compara as duas edições.

**CAD** (*computer-aided design*). Desenho assistido por computador. O programa exporta o
esquema hidráulico em DXF, formato de intercâmbio aceito pelos programas de CAD.

**CAPEX** (*capital expenditure*). Investimento inicial.

**CASAN**. Companhia Catarinense de Águas e Saneamento, a concessionária de água e esgoto
de Florianópolis e de boa parte de Santa Catarina. A estrutura tarifária dela é a adotada
no tutorial deste manual.

**CDD** (*consecutive dry days*). Maior sequência de dias consecutivos com chuva
abaixo de 1 mm.

**CEDAE**. Companhia Estadual de Águas e Esgotos do Rio de Janeiro. A estrutura tarifária
dela — conta mínima de 15 m³ (Tarifa 1) e faixas com multiplicadores da tarifa de
referência — foi herdada pela Águas do Rio, pela Rio+ Saneamento e pela Águas da
Imperatriz.

**CMIP6**. Sexta fase do *Coupled Model Intercomparison Project*, o exercício
internacional coordenado que produz as projeções climáticas usadas pelos relatórios do
IPCC. A base climática do programa deriva dele.

**CLIMBra** (*Climate Change Dataset for Brazil*). Conjunto de dados meteorológicos diários em grade de alta resolução (0,25° × 0,25°, ~28 km) para todo o Brasil, cobrindo 19 modelos climáticos globais do CMIP6 e cenários de emissões SSP2-4.5 e SSP5-8.5. Desenvolvido por Ballarin et al. (2023) na revista [*Scientific Data* (Nature)](https://www.nature.com/articles/s41597-023-01956-z) ([doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)) e disponibilizado publicamente no [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316) ([doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)). As projeções brutas foram corrigidas de viés pelo método *Quantile Delta Mapping* (QDM) utilizando como referência observacional a base de Xavier, King e Scanlon (2016). No Triton, o CLIMBra constitui a Base de dados CLIMBra para 652 cidades brasileiras (série histórica de 1980 a 2013 e projeções futuras contínuas de 2015 a 2100).

**Coeficiente de escoamento** (*runoff coefficient*). Fração da chuva que
efetivamente chega ao reservatório, descontadas perdas por absorção, evaporação e
molhamento inicial da cobertura.

**Comprimento representativo de série de precipitação** (*representative rainfall time series length*, $N_{rep}$).
Menor período contínuo em anos de dados diários de chuva necessário para estabilizar
estatisticamente o dimensionamento e o desempenho do sistema (reproduzindo o volume ideal
e o potencial de economia da série completa sob confiança $\ge 90\%$), segundo a
metodologia de Geraldi e Ghisi (2017, 2018, 2019). O comprimento necessário não é uma
constante geográfica fixa: cresce com a fração atendível e com o nível de demanda da edificação.

**Confiabilidade temporal** ($C_t$). Percentual de dias em que o sistema atendeu
plenamente ($V_{con,t} = D_{pl,t}$), parcialmente ou não atendeu a demanda pluvial.

**Confiabilidade volumétrica** ($C_v$). Fração da demanda **pluvial** que o sistema atendeu
($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Não confundir com o potencial de economia,
que tem no denominador a demanda total da edificação.

**CORSAN**. Companhia Riograndense de Saneamento, a concessionária de água e esgoto de boa
parte do Rio Grande do Sul. Fatura a água pela fórmula exponencial `PB × Cⁿ` somada ao
serviço básico, e não por faixas de consumo.

**CSV** (*comma-separated values*). Formato de arquivo de texto em que cada linha é um
registro e as colunas são separadas por um caractere, tipicamente vírgula ou ponto e
vírgula. É o formato das séries de precipitação.

**CV**. Cavalo-vapor, unidade de potência equivalente a 0,7355 kW, corrente no comércio
de motobombas no Brasil. Uma motobomba de meio CV tem 0,37 kW de potência de eixo.

**CWD** (*consecutive wet days*). Maior sequência de dias consecutivos com chuva
igual ou superior a 1 mm.

**Demanda estocástica** (*stochastic water demand*). Modelagem do consumo diário de água como
variável probabilística que varia dia a dia e entre realizações (Silva e Ghisi, 2016),
permitindo avaliar a faixa de incerteza do dimensionamento e dos indicadores de desempenho
sob variabilidade real de uso.

**Demanda pluvial** (*pluvial demand*, $D_{pl}$). Parcela da demanda diária de água da
edificação que pode ser suprida pelo sistema de aproveitamento ($D_{pl,t} = D_{tot,t} \times f$).
Corresponde aos pontos de consumo não potável interligados à rede pluvial.

**Descarte de primeiras águas** (*first flush*). Lâmina inicial de chuva desviada do
sistema, que carrega a sujeira depositada na cobertura (mínimo de 2 mm conforme a NBR
15527:2019). No Triton é **subtraída** da chuva do dia; no Netuno 4 era tratada como
limiar do evento.

**Disponibilidade**. Regime tarifário em que um valor fixo **soma** por cima do
consumo medido. Cada metro cúbico economizado desconta.

**DN** (*diâmetro nominal*). Designação comercial do diâmetro de um tubo ou conexão, em
milímetros. Não corresponde exatamente ao diâmetro interno nem ao externo: é um número de
referência do qual decorrem as dimensões reais, tabeladas por norma.

**DXF** (*drawing exchange format*). Formato de intercâmbio de desenhos técnicos, lido
por praticamente todos os programas de CAD.

**EAU**. Prefixo dos itens do tema «Consumo de água» no referencial AQUA-HQE, do francês
*eau*, água. Os itens ligados ao aproveitamento pluvial são o EAU.1.2, o EAU.1.3 e o
EAU.1.5.

**EDGE** (*excellence in design for greater efficiencies*). Referencial de certificação
da International Finance Corporation, do Banco Mundial. Mede economia percentual contra
um caso-base local em três dimensões independentes e exige que cada uma cruze o limiar.

**Eficiência de armazenamento**. Água de chuva entregue por dia dividida pelo volume da
cisterna inferior, em %: a renovação diária do volume construído. Cai com o volume, e é o
critério do multicritério que freia o superdimensionamento. Não é a ocupação média da
cisterna, que em clima úmido sobe com o volume.

**EN** (*Europäische Norm*, norma europeia). Norma publicada pelo Comitê Europeu de
Normalização. Neste manual, a EN 15978, que define os módulos do ciclo de vida da
edificação, e a EN 15804, que rege as declarações ambientais de produtos de construção.

**EPD** (*Environmental Product Declaration*). Declaração ambiental de produto: documento
verificado por terceiros, conforme a ISO 14025 e, na construção, a EN 15804, que publica
os impactos do ciclo de vida de um produto por unidade declarada. É a fonte preferida para
fatores de emissão de materiais e equipamentos.

**ESG** (*environmental, social and governance*). Conjunto de critérios ambientais,
sociais e de governança usado na avaliação de empresas e de empreendimentos. O programa
alimenta indicadores ambientais desse conjunto.

**ETAP**. Estação de tratamento de água pluvial. No programa, o conjunto de filtro
de entrada, desinfecção e filtro de polimento.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). Grupo de trabalho
internacional que padronizou os índices de extremos climáticos, dos quais o programa
calcula oito.

**Extravasamento** (*spillage*, *overflow*). Volume que excede a capacidade do reservatório
e é conduzido pelo extravasor quando ele já está cheio.

**Fração atendível por água pluvial** (*non-potable demand share*, $f$). Percentual da demanda
total de água da edificação ($D_{tot}$) passível de suprimento por água de chuva ($f = D_{pl} / D_{tot}$).
Representa o **teto assintótico intransponível** do potencial de economia de água potável
($E_{pot} \le f$): mesmo sob capacidade infinita de armazenamento e precipitação ilimitada,
a economia de potável nunca ultrapassa a fração atendível, pois o restante ($1 - f$) é
reservado aos usos nobres e potáveis. Distingue-se da confiabilidade volumétrica ($C_v = E_{pot} / f$),
que avalia o atendimento da parcela pluvial.

**Franquia no mínimo**. Regime tarifário em que o valor fixo já inclui um volume de
consumo. Economizar **abaixo** da franquia não reduz a fatura.

**Ganho marginal**. Variação do potencial de economia por metro cúbico acrescentado
ao reservatório, em %/m³ ($\Delta E_{pot} / \Delta V$). Critério de escolha do volume ideal.

**GRI** (*Global Reporting Initiative*). Padrão internacional de divulgação corporativa
de desempenho socioambiental. Sua série 303 trata de água e efluentes.

**HQE** (*Haute Qualité Environnementale*). Referencial francês de alta qualidade
ambiental, base do AQUA-HQE. Designa também os níveis dos itens do referencial: HQE,
HQE 2 e HQE 3, em ordem crescente de exigência, acima do pré-requisito (PR).

**IFC**. A sigla designa duas coisas distintas. Em certificação, é a *International
Finance Corporation*, do Banco Mundial, que desenvolve o EDGE. No contexto BIM, é o
*Industry Foundation Classes*, formato aberto de intercâmbio que o programa **não**
exporta: a exportação BIM do programa é um arquivo JSON de propriedades.

**INT**. Sigla da *International Edition* do programa: abre em inglês e não traz dados
brasileiros. Tarifas, custos, moeda e fatores de emissão são informados pelo usuário.

**IPCC** (*Intergovernmental Panel on Climate Change*). Painel intergovernamental que
sintetiza o conhecimento científico sobre mudança do clima e organiza os relatórios de
avaliação a que as projeções climáticas se referem.

**IPTU verde**. Desconto no imposto predial concedido por alguns municípios a edificações
que adotam medidas de sustentabilidade, entre elas o aproveitamento de água pluvial. O
percentual e as condições variam por legislação municipal.

**ISO 14040**. Norma internacional que estabelece os princípios e a estrutura da
avaliação de ciclo de vida. Um inventário conforme a ISO 14040 exige rastreabilidade de
cada fluxo e revisão crítica externa, requisitos que uma avaliação de triagem não cumpre.

**JSON** (*JavaScript object notation*). Formato de arquivo de texto estruturado, legível
por pessoas e por programas. É o formato interno do arquivo `.triton`.

**LCOW** (*levelized cost of water*). Custo nivelado da água: o investimento mais o custeio
anual descontado (energia, operação e manutenção, cloro e linha de tratamento), dividido pela
água de chuva entregue, descontada à mesma taxa e no mesmo horizonte de análise, em R$/m³.
É critério do eixo econômico do multicritério. Permite confrontar a viabilidade econômica do sistema diretamente
com a tarifa da concessionária.

**LEED** (*leadership in energy and environmental design*). Referencial de certificação
ambiental de edificações do *U.S. Green Building Council*, o mais difundido
internacionalmente. Trata eficiência hídrica na categoria *Water Efficiency*: na versão 4,
pelos créditos WEc1 e WEc2; na versão 5, pelo crédito WEc2, *Enhanced Water Efficiency*.

**Massa a seco do sistema**. Peso próprio do sistema vazio: cisternas, motobomba, tubos
e acessórios, pela calculadora de peso do programa. É critério do eixo estrutural do
multicritério; com a água, dá a carga em operação.

**m.c.a.** Metro de coluna d'água, unidade de pressão equivalente à exercida por uma
coluna de água de um metro de altura, cerca de 9,81 kPa. É a unidade usual em instalações
prediais.

**MCTI**. Ministério da Ciência, Tecnologia e Inovação, que publica o fator de emissão
médio do Sistema Interligado Nacional usado na avaliação ambiental da Edição Brasil.

**Micromedição**. Medição individualizada por unidade habitacional em edifício
multifamiliar. Informada ao programa como número de economias.

**Manuais do Triton** (*Triton manual suite*). A documentação do programa, montada
das mesmas fontes em três formatos: o manual completo, oito volumes avulsos, cada um com
uma parte dele, e o site de documentação. Os volumes servem a quem precisa de uma parte
só, para consultar ou enviar:

1. **Manual completo**: todos os capítulos e apêndices.
   ![Capa do Manual Completo](../figuras/capas/capa_completo.png)
2. **Volume 1 — Comece aqui**: o que o programa faz, como instalá-lo e por onde entrar
   conforme o seu objetivo.
   ![Capa do Volume 1 — Comece Aqui](../figuras/capas/capa_1-comece-aqui.png)
3. **Volume 2 — O método**: as equações, os critérios e as fontes por trás de cada número
   que o programa publica.
   ![Capa do Volume 2 — O Método](../figuras/capas/capa_2-metodo.png)
4. **Volume 3 — Guias de uso**: outras cidades, clima futuro, tarifas, demanda variável,
   lote, sensibilidade e exportação.
   ![Capa do Volume 3 — Guias Práticos](../figuras/capas/capa_3-guias.png)
5. **Volume 4 — Tutorial**: um projeto de residência em Florianópolis, do primeiro dado ao
   volume recomendado.
   ![Capa do Volume 4 — Tutorial](../figuras/capas/capa_4-tutorial.png)
6. **Volume 5 — Enganos, limitações e confiabilidade**: os enganos mais comuns, os limites
   do modelo e como o programa é verificado.
   ![Capa do Volume 5 — Confiabilidade](../figuras/capas/capa_5-confiabilidade.png)
7. **Volume 6 — Correções, bugs e versionamento**: o que mudou desde o Netuno 4, as
   mensagens de erro e como relatar um problema.
   ![Capa do Volume 6 — Versões](../figuras/capas/capa_6-versoes.png)
8. **Volume 7 — Modulação probabilística**: o estudo refeito com premissas sorteadas —
   variáveis, distribuições, leitura dos resultados e limites do método.
   ![Capa do Volume 7 — Modulação probabilística](../figuras/capas/capa_7-modulacao.png)
9. **Volume 8 — Apêndices**: parâmetros, processos, fatores de emissão, tarifas, base
   climática, formatos, glossário e referências.
   ![Capa do Volume 8 — Apêndices](../figuras/capas/capa_8-apendices.png)

Os PDFs acompanham o programa e abrem pela etapa 9. Documentação; o manual existe também
em inglês, na íntegra.

**NBR**. Norma Brasileira, publicada pela ABNT. As mais citadas neste manual são a NBR
15527, de aproveitamento de água de chuva, a NBR 10844, de instalações prediais de águas
pluviais, a NBR 5626, de sistemas prediais de água fria e quente, e a NBR 17094-2, de
motores de indução.

**Partes no eixo**. Proporção em que o peso de um eixo do multicritério se reparte entre
os critérios do eixo. Só a razão dentro do eixo importa; o padrão são partes iguais, e parte
zero tira o critério da conta.

**Payback de carbono**. Tempo para a economia anual líquida de emissões pagar o
carbono incorporado na fabricação do sistema.

**Payback descontado**. Tempo para o fluxo de caixa descontado acumulado cruzar zero.

**PB**. Preço-base, em R$/m³, da fórmula exponencial da CORSAN, `PB × Cⁿ`, em que `C` é o
consumo do mês e `n` o expoente da tabela exponencial para aquele consumo.

**PEAD**. Polietileno de alta densidade, material dos reservatórios plásticos mais
comuns no mercado brasileiro.

**Piso de pagamento**. Regime tarifário em que a fatura **não fica** abaixo de um
valor. Diferente de disponibilidade: o piso limita por baixo, a disponibilidade soma
por cima.

**Potencial de economia de água potável** (*potable water saving potential*, $E_{pot}$).
Fração da demanda **total** da edificação suprida por água pluvial ($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$).
É o indicador central do programa, limitado superiormente pela fração atendível ($E_{pot} \le f$).

**pp**. Pontos percentuais. Usado para exprimir a diferença entre dois percentuais: de
35% para 37% vão dois pontos percentuais, e não dois por cento.

**PR**. Pré-requisito: no AQUA-HQE, o nível de item de atendimento obrigatório, abaixo
dos níveis HQE, HQE 2 e HQE 3.

**PRCPTOT**. Precipitação total anual em dias úmidos.

**PRFV**. Plástico reforçado com fibra de vidro, material de reservatórios de médio e
grande porte. Aparece no programa sob a designação «fibra».

**PVC**. Policloreto de vinila, material das tubulações prediais de água fria e das
colunas de desvio do descarte inicial. As dimensões dos tubos soldáveis seguem a ABNT NBR 5648.

**R95p**. Soma da precipitação dos dias acima do percentil 95 dos dias úmidos.

**Rendimento da bomba**. Razão entre a potência hidráulica entregue à água e a
potência mecânica no eixo. Não inclui o motor.

**Rendimento do motor**. Razão entre a potência mecânica no eixo e a potência
elétrica consumida da rede. A ABNT NBR 17094-2 manda marcá-lo na placa.

**RX1day**, **RX5day**. Maior precipitação em um e em cinco dias consecutivos, no
ano.

**SAAP**. Sistema de aproveitamento de água pluvial. Conjunto integrado de componentes
prediais — área de captação, condutores, descarte inicial (first flush), estação de
tratamento (ETAP), cisterna inferior, reservatório superior, grupo motobomba ou pressurizador
e rede de distribuição independente — concebido para coletar, tratar, armazenar e fornecer
água não potável em conformidade com a ABNT NBR 15527 e a ABNT NBR 5626.

**SB**. Serviço básico: a parcela fixa mensal da fatura de água da CORSAN, somada ao
resultado da fórmula exponencial.

**SDII** (*simple daily intensity index*). Precipitação média dos dias úmidos.

**SI** (*seasonality index*). Índice de sazonalidade de Walsh e Lawler. Zero quando a
chuva é uniforme ao longo do ano.

**SMAA** (*stochastic multicriteria acceptability analysis*). Método que sorteia
pesos e devolve a probabilidade de cada alternativa vencer.

**SNIS**. Sistema Nacional de Informações sobre Saneamento, base oficial brasileira de
indicadores do setor, mantida pelo governo federal. É a origem dos indicadores de
consumo energético do saneamento usados na avaliação ambiental.

**SSP** (*shared socioeconomic pathways*). Trajetórias socioeconômicas compartilhadas,
que descrevem hipóteses coerentes de desenvolvimento global e as emissões correspondentes.
Combinam-se com os modelos climáticos para produzir projeções.

**TFDI**. Tarifa fixa de disponibilidade da infraestrutura, nome que algumas
concessionárias dão à parcela da fatura cobrada independentemente do consumo. Ver
*Disponibilidade*.

**TIR**. Taxa interna de retorno. A taxa de desconto que zera o valor presente
líquido.

**TMA**. Taxa mínima de atratividade. A taxa de desconto adotada.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*).
Método de ordenação multicritério de Hwang e Yoon.

**UV**. Radiação ultravioleta, empregada na desinfecção de água por inativação de
microrganismos. Atua apenas no instante da passagem pelo reator e não deixa residual, ao
contrário da cloração.

**VIKOR**. Método de decisão multicritério proposto por Opricovic, que busca uma solução
de compromisso entre critérios conflitantes. Ver também *SMAA*.

**Volume ideal** (*optimal tank volume*). Menor volume de reservatório da grade de simulação
a partir do qual o ganho marginal de economia de água potável ($\Delta E_{pot} / \Delta V$)
cai abaixo de um limiar declarado (tipicamente $1,0\%/\text{m}^3$ ou $0,5\%/\text{m}^3$).
Evita o superdimensionamento de reservatórios, assegurando a melhor relação custo-benefício.

**VPL**. Valor presente líquido.

**WEM**. Codificação das medidas de eficiência hídrica do EDGE. A WEM14 é o sistema
de aproveitamento de água pluvial.

**XLSX**. Formato de pasta de trabalho do Microsoft Excel, baseado em XML compactado. É um
dos formatos de exportação de planilhas e de resultados da linha de comando.

**YAS** (*yield after spillage*). Regra de operação em que o extravasamento é
calculado **antes** da retirada da demanda e, na forma estrita, a retirada do dia sai
só do volume guardado na véspera. O programa calcula o extravasamento antes, como a
YAS, mas deixa a chuva do dia atender a demanda do dia; fica entre a YAS e a YBS
(seção 2.1 (volume O método)).

**YBS** (*yield before spillage*). Regra de operação em que a demanda é retirada **antes**
do cálculo do extravasamento. Supõe consumo anterior à chuva do dia e superestima o
aproveitamento; o programa não a adota, e o resultado dele fica entre a YAS e a YBS.

---

### G.1. Diretrizes de Padronização e Nomenclatura no Triton

A padronização terminológica é indispensável para assegurar a consistência e o rigor técnico
em artigos científicos, relatórios técnicos, na interface gráfica e na documentação do Triton.
As convenções a seguir detalham a distinção de termos correlatos frequentemente confundidos:

#### G.1.1. 1. Água de Chuva versus Água Pluvial versus «Água da Chuva»

<!-- tabela: **Tabela 38** — Padronização terminológica de água de chuva e água pluvial -->
| Termo | Definição e Contexto de Aplicação | Situação no Triton | Referência |
| :--- | :--- | :--- | :--- |
| **Água de chuva** (*rainwater*) | Precipitação atmosférica coletada diretamente na cobertura (telhado/laje impermeabilizada), antes de atingir o solo ou galerias. Refere-se à **fonte hídrica** e ao recurso ambiental. | **Canônico e preferencial** para o recurso captado («aproveitamento de água de chuva», «precipitação de água de chuva»). | ABNT NBR 15527:2019, título e item 3.1. |
| **Água pluvial** (*stormwater* / *pluvial water*) | Água de chuva após escoamento superficial urbano ou quando conduzida por canalizações e sistemas prediais de drenagem e armazenamento. Aplica-se à **infraestrutura física** e aos componentes de engenharia. | **Canônico e preferencial** para sistemas, redes e balanço («sistema predial de água pluvial - SAAP», «rede pluvial», «demanda pluvial», «extravasamento pluvial»). | ABNT NBR 10844:1989; ABNT NBR 5626:2020. |
| **«Água da chuva»** | Expressão coloquial e informal. | **Desaconselhada**. Não deve ser empregada em publicações, textos normativos, relatórios do Triton ou código. | Prática de redação técnica e científica. |

#### G.1.2. 2. Fração Atendível, Demanda Pluvial, Potencial e Confiabilidade

Para evitar ambiguidades matemáticas e conceituais frequentemente encontradas na literatura:

<!-- tabela: **Tabela 39** — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial -->
| Grandeza | Símbolo / Código | Definição | Fórmula | Relação / Teto |
| :--- | :--- | :--- | :--- | :--- |
| **Fração atendível por água pluvial** | $f$ / `rainwater_share` | Proporção da demanda total da edificação correspondente a pontos de consumo não potável conectáveis ao SAAP. | $f = D_{pl} / D_{tot}$ | Parâmetro de projeto ($0 \le f \le 1$). Constitui o **teto assintótico** de $E_{pot}$. |
| **Demanda pluvial** | $D_{pl}$ / `rainwater_demand` | Volume de água requerido pelos pontos não potáveis da edificação em um intervalo de tempo. | $D_{pl,t} = D_{tot,t} \times f$ | Em L/dia ou m³/ano. |
| **Volume de água pluvial consumido** | $V_{con}$ / `pluvial_consumed` | Volume de água não potável efetivamente suprido pelo reservatório pluvial aos pontos de consumo. | Determinado pelo balanço diário (seção 2.1 (volume O método)) | $V_{con,t} \le D_{pl,t}$ e $V_{con,t} \le S_{t-1} + C_t$. |
| **Potencial de economia de água potável** | $E_{pot}$ / `potential_potable_savings_pct` | Percentual da demanda **total** da edificação economizado pelo aproveitamento pluvial. | $E_{pot} = \frac{\sum V_{con}}{\sum D_{tot}} \times 100\%$ | **Indicador central**. Sempre $E_{pot} \le f$. |
| **Confiabilidade volumétrica** | $C_v$ / `volumetric_reliability_pct` | Percentual da demanda **pluvial** suprido pela água de chuva armazenada. | $C_v = \frac{\sum V_{con}}{\sum D_{pl}} \times 100\%$ | $C_v = \frac{E_{pot}}{f}$. Pode atingir 100% mesmo quando $E_{pot} < 100\%$. |
| **Confiabilidade temporal** | $C_t$ / `temporal_reliability_pct` | Percentual de dias da série em que a demanda pluvial foi 100% atendida ($V_{con,t} = D_{pl,t}$). | $C_t = \frac{N_{dias\_plenos}}{N_{total}} \times 100\%$ | Mede a segurança de abastecimento diário sem suplementação potável. |

#### G.1.3. 3. Síntese de Nomenclatura Recomendada para Artigos e Relatórios

- Utilize **«aproveitamento de água de chuva»** (e não «reúso de água da chuva» — água de chuva não é efluente; seu uso é *aproveitamento*, não *reúso*).
- Utilize **«área de captação»** para o plano horizontal da cobertura (NBR 15527) e reserve **«área de contribuição»** exclusivamente para o dimensionamento hidráulico de calhas sob vento (NBR 10844).
- Utilize **«descarte de primeiras águas»** ou *first flush* para a lâmina inicial desviada (mínimo de 2 mm conforme NBR 15527), e não «limiar de descarte».
- Utilize **«fração atendível»** (e não «demanda relativa» ou «fração de economia») para expressar a partição de usos não potáveis no consumo total.
- Utilize **«comprimento representativo de série»** para a extensão mínima em anos necessária para estabilização estatística da simulação (método Geraldi & Ghisi).
- Utilize **«LCOW»** ou **«custo nivelado da água»** para a métrica de custo unitário ao longo do ciclo de vida descontado à TMA.
