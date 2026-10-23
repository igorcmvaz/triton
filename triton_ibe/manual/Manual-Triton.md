# Triton IBE

## Manual do Utilizador

Igor Catão Martins Vaz e Enedir Ghisi

Grupo de Pesquisa em Ambientes Sustentáveis
Universidade Federal de Santa Catarina

Florianópolis, 2026

Versão 0.1.0 · revisão de 23/10/2026

---

### Ficha de publicação

| Elemento | Conteúdo |
| :--- | :--- |
| **Título** | Triton: manual do utilizador |
| **Autores** | Igor Catão Martins Vaz; Enedir Ghisi |
| **Edição** | Triton IBE (Edição Ibérica), versão 0.1.0 |
| **Local** | Florianópolis, SC, Brasil |
| **Editora** | Universidade Federal de Santa Catarina |
| **Grupo de pesquisa** | Ambientes Sustentáveis |
| **Ano de publicação** | 2026 |
| **Licença** | Código-fonte acadêmico (uso não comercial), ver LICENSE.md |

### Como citar

**ABNT NBR 6023:2018**

> VAZ, Igor Catão Martins; GHISI, Enedir. **Triton: manual do utilizador**.
> Versão 0.1.0. Florianópolis: Universidade Federal de Santa Catarina, 2026.

**Estilo autor-data**

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: manual do utilizador*
> (Versão 0.1.0). Universidade Federal de Santa Catarina.

**BibTeX**

```
@manual{tritonmanual2026,
  title     = {Triton: manual do utilizador},
  author    = {Vaz, Igor Catão Martins and Ghisi, Enedir},
  edition   = {Versão 0.1.0},
  address   = {Florianópolis},
  publisher = {Universidade Federal de Santa Catarina},
  year      = {2026}
}
```

Ao citar resultados obtidos com o programa, declare também a versão usada e a
origem da série de precipitação, conforme a lista da seção 4.10.

---

### Como usar este manual

Ele não foi feito para ser lido do começo ao fim. A seção 1.3 diz por onde
entrar conforme o que você quer fazer. Para mandar só uma parte, o manual também
sai em oito volumes avulsos, um por capítulo, na pasta `manual/mini` da
instalação; a numeração das seções é a mesma nos volumes e aqui.

| Você quer | Leia |
| :--- | :--- |
| aprender a usar | o capítulo 4, o tutorial |
| resolver um caso | o capítulo 3, os guias |
| publicar um estudo | o capítulo 2, o método; e a seção 4.10 |
| revisar um estudo | o capítulo 5, e os apêndices A e B |
| não errar | a seção 5.1 |

O manual supõe um leitor de engenharia que ainda não conhece o assunto: os
conceitos são apresentados antes de serem usados, e o vocabulário está no
apêndice G. Duas caixas aparecem ao longo do texto, e elas se distinguem:

| A caixa | Quando aparece |
| :--- | :--- |
| de régua **azul** | aviso ou observação que muda o que você faz |
| de régua **laranja**, marcada *Aprofundamento* | o detalhe técnico por trás; pode ser pulada numa primeira leitura |

> **Todo número impresso neste manual é calculado pelo programa.** As tabelas
> e as figuras não foram digitadas: são produzidas rodando o Triton com os
> dados de entrada que cada seção declara. Cada valor publicado tem uma
> verificação automática correspondente, de modo que uma correção no programa
> não possa deixar o manual mentindo. A seção 5.3 explica como isso é feito.

---

## Sumário

**1 Comece aqui**

1.1 O que o Triton faz, e o que ele não faz

1.2 Instalação e primeira execução

1.3 Por onde começar, conforme o seu objetivo


**2 O método**

2.1 O balanço hídrico diário

2.2 Volume ideal e a varredura

2.3 Indicadores de eficiência

2.4 Índices pluviométricos

2.5 Dimensionamento da ETAP

2.6 Energia de bombeamento

2.7 Análise econômica e os regimes tarifários

2.8 Avaliação de ciclo de vida

2.9 Certificações

2.10 Decisão multicritério


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


**4 Tutorial: um exemplo do começo ao fim**

4.1 O projeto e a chuva

4.2 A edificação e a demanda

4.3 A primeira simulação

4.4 Escolher o volume

4.5 Precisa de reservatório superior?

4.6 Que qualidade o uso exige

4.7 Quanto custa e em quanto se paga

4.8 Quanto carbono evita

4.9 Qual volume escolher, afinal

4.10 O relatório, e o que declarar num artigo


**5 Enganos, limitações e confiabilidade**

5.1 Dez enganos que o programa não impede

5.2 Limitações conhecidas

5.3 Como o programa é verificado


**6 Correções, bugs e versionamento**

6.1 Comparação com o Netuno 4

6.2 Mensagens de erro e o que fazer

6.3 Histórico de versões e o que mudou

6.4 Como relatar um problema

6.5 Roteiro de evolução


**7 Modulação probabilística**

7.1 O que é a modulação probabilística

7.2 As variáveis e as distribuições

7.3 Como rodar

7.4 Como ler os resultados

7.5 Método, estatística e limites


**Apêndices**

Apêndice A — Os parâmetros do projeto

Apêndice B — Os processos do programa

Apêndice C — Fatores de emissão

Apêndice D — Regimes tarifários

Apêndice E — Base climática

Apêndice F — Arquivos, pastas e formatos

Apêndice G — Glossário

Apêndice H — Referências

Apêndice I — Fichas de uma página

Apêndice J — Arquivos de exemplo



## Lista de figuras

Figura 1 — Componentes de um sistema predial de aproveitamento de água da chuva e percurso da água, da captação ao ponto de uso

Figura 2 — O mesmo sistema visto em corte

Figura 3 — Destino da precipitação de um dia

Figura 4 — Sequência de operações do balanço diário, na ordem em que o programa as executa, na notação das equações da secção do balanço diário

Figura 5 — As seis dimensões de análise e a questão avaliada em cada uma

Figura 6 — Os quatro percursos de leitura do manual

Figura 7 — Que parte do consumo total a água da chuva pode atender, conforme os usos que o projeto prevê. É o teto do potencial de economia: nenhum reservatório, por maior que seja, ultrapassa esta fração

Figura 8 — As etapas do programa, agrupadas por natureza

Figura 9 — Os dez dias do caso resolvido, com a chuva de Lisboa de 11 a 20 de dezembro de 2019: (a) volume captado, a azul, e volume extravasado, a laranja, por dia; nos dias 9 e 10 o extravasamento é quase igual ao captado; (b) volume armazenado no reservatório inferior no fim de cada dia, depois do consumo, com a capacidade de 2 000 L a tracejado; nos dias 9 e 10 o reservatório atinge a capacidade, extravasa e termina o dia com 1 920 L

Figura 10 — Sequência de operações do balanço diário: (a) a ordem adotada pelo programa, com o extravasamento calculado antes do consumo; (b) a ordem invertida (YBS), com o consumo retirado antes do extravasamento

Figura 11 — Curva de potencial de poupança do mesmo edifício, varrida com passo de 250 L e com passo de 5 000 L. A grelha grossa calcula corretamente cada ponto que contém, mas não contém o troço de maior curvatura, entre 1 e 5 m³

Figura 12 — Varredura do projeto do tutorial lida por três critérios: (a) potencial de poupança e (b) valor atual líquido do mesmo conjunto de volumes

Figura 13 — Os três indicadores de eficiência e o que cada um conta

Figura 14 — Classes de abastecimento diário: pleno (V_con,t = D_pl,t), parcial (0 < V_con,t < D_pl,t) e nulo (V_con,t = 0). A altura preenchida representa a fração da procura pluvial do dia satisfeita por água da chuva

Figura 15 — Quatro dos nove índices marcados sobre um ano da série de Lisboa: PRCPTOT e SDII, no alto; RX1day, o maior valor diário do ano; CDD, a maior sequência de dias secos, na faixa sombreada; e R20mm, os dias com 20 mm ou mais, marcados na base

Figura 16 — Índice de sazonalidade de Walsh e Lawler (1981) nas três cidades de exemplo (Lisboa, Porto e Funchal), com as classes do índice ao fundo e a precipitação média anual sob o nome de cada cidade

Figura 17 — Precipitação total anual (PRCPTOT) da série de Lisboa, com a média do período a tracejado, no separador de índices

Figura 18 — Maior sequência anual de dias secos (CDD) e de dias chuvosos (CWD) da série de Lisboa, no separador de índices

Figura 19 — Componentes da linha de tratamento dimensionada pelo programa, na ordem do escoamento, e destino do material retido

Figura 20 — As três tecnologias de desinfeção, o efeito residual de cada uma e a composição do custeio anual (OPEX). O efeito residual distingue a cloração das restantes: protege a água armazenada na cisterna e na rede, enquanto a radiação ultravioleta e o ozono atuam apenas sobre a água que atravessa o reator

Figura 21 — Cadeia energética da bombagem predial

Figura 22 — (a) Altura manométrica de um sistema elevatório predial: desnível geométrico entre os níveis da cisterna e do reservatório superior somado às perdas de carga totais; (b) linha piezométrica ao longo de um troço de tubagem com perda de carga contínua por atrito e singularidades localizadas

Figura 23 — Rendimento indicativo de motores de indução por escalão de potência e classe de eficiência

Figura 24 — Fatura mensal de água e saneamento do projeto do tutorial, discriminada por parcelas, com e sem o sistema pluvial

Figura 25 — Os códigos de escalão tarifário e o respetivo impacto na faturação mensal

Figura 26 — Caracterização conceptual dos regimes tarifários suportados pelo motor de cálculo

Figura 27 — Estrutura do investimento inicial por componente para diferentes capacidades de reservatório

Figura 28 — Projeção do fluxo de caixa acumulado do projeto do tutorial ao longo de 20 anos, demonstrando o comportamento do investimento inicial face à poupança anual na fatura

Figura 29 — As sete componentes do inventário de ciclo de vida do programa: as quatro primeiras correspondem ao carbono incorporado nos materiais; as duas seguintes às emissões operacionais anuais; e a sétima ao crédito ambiental anual pela água evitada (único termo dedutivo)

Figura 30 — Delimitação da fronteira da avaliação ambiental: (a) processos incluídos — carbono incorporado dos reservatórios, tubagens e eletrobombas, emissões elétricas operacionais, produtos de tratamento e crédito da água potável poupada; (b) processos excluídos — movimentos de terras em obra civil, manutenção corretiva, fim de vida e outras categorias de impacte

Figura 31 — Os limiares de redução do consumo de água potável com que o programa enquadra o projeto no LEED v4 (créditos WEc1 e WEc2), no LEED v5 (crédito WEc2, opções 1, 2 e 4) e no EDGE, na mesma escala

Figura 32 — Escore TOPSIS de cada volume da varredura do projeto do tutorial, de 1 a 20 m³, com cisterna de polietileno e pesos iguais entre os sete critérios; a estrela marca o volume de maior escore

Figura 33 — Aceitabilidade de primeiro lugar (b¹) de cada volume candidato, obtida com cinco mil vetores de pesos sorteados no simplex

Figura 34 — (a) Precipitação média anual e (b) potencial de economia de água potável do projeto do tutorial, com 150 m² de captação, 600 L/dia de procura, fração atendível de 28% e cisterna de 5 000 L, em Lisboa, no Porto e no Funchal

Figura 35 — Precipitação média mensal em (a) Lisboa, (b) Porto e (c) Funchal, na mesma escala; a linha a tracejado é a média mensal de cada série

Figura 36 — A forma de duas trajetórias de emissão típicas

Figura 37 — Parte da água na fatura mensal em função do consumo, em três regimes de valor mínimo

Figura 38 — Os quatro modos de modulação, o que cada um pede ao utilizador e a situação em que cada um se justifica

Figura 39 — Perfis de procura usados na comparação, expressos como a razão entre a procura do mês e a procura média

Figura 40 — (a) Perfis de procura da escola e do hotel sobre a precipitação média mensal da cidade de cada caso; (b) potencial de poupança de cada perfil contra a mesma procura anual repartida por igual

Figura 41 — As oito tipologias disponíveis, agrupadas pela categoria tarifária que a entidade gestora cobra

Figura 42 — Intervalo de variação plausível de cada pressuposto numa análise de sensibilidade, com a origem da incerteza

Figura 43 — A variação do valor atual líquido quando cada pressuposto é alterado em 30% para mais e para menos, mantidos os restantes

Figura 44 — Série de precipitação de Lisboa usada em todo o tutorial (E-OBS, concelho de Lisboa, 1991 a 2020): (a) precipitação total de cada ano, com a média dos trinta anos em linha contínua e os anos acima da média a azul e abaixo dela a laranja; (b) distribuição de frequência da precipitação diária nos dias de chuva, em escala logarítmica, que mostra como poucos dias respondem pelos maiores volumes

Figura 45 — O ciclo sazonal médio da série, calculado e desenhado pelo programa assim que a precipitação é carregada

Figura 46 — O coeficiente de escoamento que o programa atribui a cada material da cobertura

Figura 47 — As gamas habituais de consumo per capita por tipologia de edifício

Figura 48 — Repartição típica do consumo de uma moradia por uso final

Figura 49 — Estados do campo de fração atendível na interface

Figura 50 — O nível da cisterna ao longo do primeiro ano da série de Lisboa, com a chuva diária ao fundo

Figura 51 — (a) Potencial de economia em função do volume do reservatório, que continua a subir aos 20 000 L (24,01%) sem alcançar o teto de 28%, com o volume ideal marcado; (b) ganho marginal, em escala logarítmica, com o limiar de 1 %/m³ adotado no tutorial

Figura 52 — O primeiro gráfico do separador de resultados: o potencial de economia de água potável em função do volume do reservatório inferior

Figura 53 — O segundo gráfico: o ganho marginal, em pontos percentuais por metro cúbico acrescentado

Figura 54 — O terceiro gráfico: o volume extravasado e o volume pluvial consumido, ambos anuais, na mesma escala

Figura 55 — O quarto gráfico: a repartição dos dias do período em atendidos por inteiro, atendidos em parte e não atendidos

Figura 56 — Uso da capacidade do reservatório inferior no projeto do tutorial, com procura pluvial de 168 L/dia: (a) curvas de permanência da autonomia armazenada no fim de cada dia, em dias de procura pluvial, para vários volumes; (b) renovações anuais do volume, dadas pela razão entre o consumo pluvial anual e a capacidade, com a fração de dias em que o reservatório termina vazio (até 5% da capacidade) indicada sob cada volume

Figura 57 — As quatro classes de qualidade do programa e a situação de cada uma

Figura 58 — O gráfico do separador económico: o valor atual líquido de cada volume da varredura, com o máximo económico e o ótimo técnico marcados

Figura 59 — O gráfico do separador ambiental para o mesmo projeto, com cisterna de betão: as parcelas do balanço de carbono em vinte anos, com fatores ilustrativos

Figura 60 — Emissões líquidas acumuladas da cisterna de 5 000 L ao longo da vida útil, para polietileno e betão, com fatores ilustrativos

Figura 61 — Emissões líquidas em vinte anos da cisterna de 5 000 L, por material, com fatores ilustrativos

Figura 62 — Emissões líquidas em vinte anos contra o volume da cisterna, para (a) polietileno e (b) betão, no projeto do tutorial, com fatores ilustrativos

Figura 63 — O gráfico do separador de decisão: o escore de proximidade ao ideal de cada volume candidato, com o vencedor destacado

Figura 64 — O segundo gráfico do separador de decisão: o quanto o volume escolhido se aproxima do melhor valor possível em cada um dos sete critérios

Figura 65 — Área de captação como projeção horizontal da cobertura

Figura 66 — Número de testes e de ficheiros de cada família da suíte de verificação, conforme a recolha da suíte nesta versão

Figura 67 — As cinco camadas de verificação do programa, dos testes unitários, numerosos e dirigidos a erros locais, à conferência manual, pontual e dirigida a erros de modelo

Figura 68 — Decomposição da divergência média entre o programa e uma referência independente

Figura 69 — Poupança de água potável por volume do reservatório inferior no exemplo do tutorial: gama entre os percentis 5 e 95 das realizações, mediana e estudo determinístico

Figura 70 — Valor atual líquido por volume do reservatório inferior no mesmo exemplo (custos ilustrativos, não são preços de mercado). Uma gama que atravessa o zero em todos os volumes indica que nenhum deles se paga com certeza; uma mediana abaixo do estudo determinístico, que o caso-base é otimista

Figura 71 — Frequência, em percentagem das realizações, com que cada volume é o ideal técnico, o ótimo económico e o vencedor do TOPSIS no exemplo do tutorial

Figura 72 — Correlação de postos de Spearman de cada variável sorteada com a poupança de água potável e com o valor atual líquido no volume escolhido pelo estudo do tutorial, da maior para a menor influência no valor atual líquido

---

## Lista de tabelas

Tabela 1 — Requisitos de sistema para instalar e executar o programa

Tabela 2 — O que a Edição Ibérica traz e o que deixa ao utilizador

Tabela 3 — Formatos de ficheiro que o programa grava e o conteúdo de cada um

Tabela 4 — Ficheiros de exemplo distribuídos com o programa

Tabela 5 — Percurso de leitura recomendado conforme o objetivo do leitor

Tabela 6 — Escolha entre volume fixo e varredura conforme a pergunta do estudo

Tabela 7 — Critérios hidráulicos para decidir sobre o reservatório superior

Tabela 8 — Dados de entrada do caso resolvido de dez dias

Tabela 9 — Série de precipitação dos dez dias do caso resolvido (Lisboa, dezembro de 2019)

Tabela 10 — Balanço hídrico diário do caso resolvido, dia a dia, com captação, consumo, extravasamento e armazenamento

Tabela 11 — Verificação do fecho do balanço de massa nos dez dias

Tabela 12 — Indicadores do caso resolvido de dez dias

Tabela 13 — Variáveis da Equação 1

Tabela 14 — Variáveis da Equação 2

Tabela 15 — Variáveis da Equação 5

Tabela 16 — Retirada do dia e volume armazenado no fim do dia nas regras YAS e YBS estritas e no Triton

Tabela 17 — Variáveis da Equação 7

Tabela 18 — Variáveis da Equação 8

Tabela 19 — Variáveis da Equação 9

Tabela 20 — Variáveis da Equação 10

Tabela 21 — Variáveis da Equação 11

Tabela 22 — Variáveis da Equação 12

Tabela 23 — Volumes dados por regras clássicas de dimensionamento para o projeto do tutorial, arredondados a 250 L, e o potencial que cada um produz na simulação diária

Tabela 24 — Fração de armazenamento dos volumes da varredura e o passo de simulação que Fewkes e Butler (2000) recomendam para cada gama

Tabela 25 — Variáveis da Equação 13

Tabela 26 — Variáveis da Equação 14

Tabela 27 — Variáveis da Equação 15

Tabela 28 — Variáveis da Equação 16

Tabela 29 — Variáveis da Equação 17

Tabela 30 — Variáveis da Equação 18

Tabela 31 — Variáveis da Equação 19

Tabela 32 — Variáveis da Equação 20

Tabela 33 — Quadro-resumo dos indicadores, com o denominador e a pergunta a que cada um responde

Tabela 34 — Variáveis da Equação 21

Tabela 35 — Variáveis da Equação 22

Tabela 36 — Variáveis da Equação 23

Tabela 37 — Variáveis da Equação 24

Tabela 38 — Variáveis da Equação 25

Tabela 39 — Variáveis da Equação 26

Tabela 40 — Variáveis da Equação 27

Tabela 41 — Variáveis da Equação 28

Tabela 42 — Variáveis da Equação 29

Tabela 43 — Filtro mecânico de entrada dimensionado pela área de cobertura

Tabela 44 — Variáveis da Equação 30

Tabela 45 — Recomendação de filtro de polimento por classe de qualidade alvo

Tabela 46 — Dimensionamento do descarte inicial no projeto do tutorial

Tabela 47 — Variáveis da Equação 31

Tabela 48 — Os dois rendimentos da cadeia de bombeamento e o que cada um converte

Tabela 49 — Variáveis da Equação 32

Tabela 50 — Variáveis da Equação 33

Tabela 51 — Variáveis da Equação 34

Tabela 52 — Variáveis da Equação 35

Tabela 53 — Variáveis da Equação 36

Tabela 54 — Variáveis da Equação 37

Tabela 55 — Energia anual de seis sobrepressores genéricos (curvas ilustrativas, sem marca) na pressurização direta do tutorial, com o caudal do autoclismo a limitar o caudal da bomba

Tabela 56 — Variáveis da Equação 38

Tabela 57 — Variáveis da Equação 39

Tabela 58 — Codificação dos regimes tarifários

Tabela 59 — Variáveis da Equação 40

Tabela 60 — Variáveis da Equação 42

Tabela 61 — Variáveis da Equação 43

Tabela 62 — Módulos do ciclo de vida da EN 15978 e o que a avaliação do programa cobre em cada um

Tabela 63 — Variáveis da Equação 44

Tabela 64 — Massa por metro cúbico útil de cada material de reservatório

Tabela 65 — Inventário de carbono do projeto final do tutorial, item a item, com a parcela de cada componente no carbono incorporado; os valores anuais negativos são créditos (fatores da rede e da água ilustrativos, não são valores medidos)

Tabela 66 — Variáveis da Equação 45

Tabela 67 — Variáveis da Equação 46

Tabela 68 — Variáveis da Equação 47

Tabela 69 — Variáveis da Equação 49

Tabela 70 — Opções do crédito WEc2 do LEED v5 a que o aproveitamento pluvial contribui

Tabela 71 — Os sete critérios de decisão, a direção de preferência e o grupo de cada um

Tabela 72 — Variáveis da Equação 50

Tabela 73 — Pontuação de proximidade TOPSIS com pesos iguais nas dimensões e aceitabilidade do primeiro lugar no SMAA-VIKOR, com 5 000 vetores de pesos aleatórios, para os volumes do tutorial

Tabela 74 — O mesmo projeto do tutorial simulado em Lisboa, no Porto e no Funchal

Tabela 75 — Razão entre o mês mais chuvoso e o menos chuvoso nas três cidades

Tabela 76 — Os seis códigos de escalão tarifário e o efeito de cada um na fatura

Tabela 77 — Os seis regimes tarifários e o que acontece ao poupar em cada um

Tabela 78 — Efeito da poupança de água na fatura em dois regimes tarifários opostos (estruturas hipotéticas, em unidades monetárias)

Tabela 79 — Fatura mensal doméstica de água, saneamento e resíduos nos três concelhos, tarifários de 2026 transcritos pelo programa

Tabela 80 — As três formas de comparar alternativas conforme o que varia entre elas

Tabela 81 — Subcomandos da linha de comandos e finalidade de cada um

Tabela 82 — Potencial, valor atual líquido e período de recuperação do projeto final do tutorial com cada premissa variada isoladamente, do valor baixo ao alto (os custos são ilustrativos, não são preços de mercado)

Tabela 83 — Leitura da aceitabilidade SMAA-VIKOR do volume vencedor

Tabela 84 — Dados do formato antigo recuperados pela importação

Tabela 85 — Formatos de exportação e finalidade de cada um

Tabela 86 — Opções da exportação para folha de cálculo e quando usar cada uma

Tabela 87 — Caracterização da série de precipitação de Lisboa adotada no tutorial

Tabela 88 — Os três modos de aplicação do descarte de primeiras águas

Tabela 89 — Estado do projeto do tutorial no fim da definição da chuva e da captação

Tabela 90 — Estado do projeto do tutorial no fim da definição da procura

Tabela 91 — Comparação entre a oferta anual de água da chuva e a procura atendível

Tabela 92 — Resultado da primeira simulação do tutorial, com um reservatório de 3 000 L

Tabela 93 — Classificação de cada dia da simulação quanto ao grau de atendimento

Tabela 94 — Estado do projeto do tutorial depois da primeira simulação

Tabela 95 — Varredura de volumes do projeto do tutorial, com o ganho marginal de cada metro cúbico acrescentado

Tabela 96 — Ganho marginal de economia por cada metro cúbico acrescentado ao reservatório

Tabela 97 — Indicadores do volume ideal obtido com o limiar de 1 %/m³ adotado no tutorial

Tabela 98 — Volume ideal obtido com cada limiar de ganho marginal, para o mesmo projeto

Tabela 99 — Custo e desempenho comparados entre o volume ideal e o maior volume varrido (os preços são ilustrativos, não são preços de mercado)

Tabela 100 — Estado do projeto do tutorial depois da escolha do volume

Tabela 101 — Os três arranjos de abastecimento e o que cada um acrescenta ao projeto

Tabela 102 — Reservatório único comparado com dois reservatórios, mantido o mesmo armazenamento total (o custo da energia é ilustrativo, não é preço de mercado)

Tabela 103 — Efeito do limiar de arranque da bomba no potencial de poupança e no número de arranques

Tabela 104 — Estado do projeto do tutorial depois da decisão sobre o reservatório superior

Tabela 105 — Linha de tratamento conforme a tecnologia de desinfeção adotada: etapas, energia ultravioleta e carbono anual

Tabela 106 — Recomendação de filtração fina por classe de qualidade

Tabela 107 — Filtro mecânico de entrada dimensionado pela área da cobertura

Tabela 108 — Estado do projeto do tutorial depois da definição da classe de qualidade

Tabela 109 — Composição da fatura de água, saneamento e resíduos de Lisboa antes e depois do sistema pluvial

Tabela 110 — Indicadores económicos do projeto do tutorial em vinte anos de análise (todos os custos são ilustrativos, não são preços de mercado)

Tabela 111 — Os seis regimes tarifários e o efeito de cada um sobre a poupança

Tabela 112 — Composição do investimento inicial do projeto do tutorial (ilustrativo, não é preço de mercado)

Tabela 113 — O que um projeto novo da Edição Ibérica traz preenchido e o que fica por definir pelo utilizador

Tabela 114 — Parâmetros ilustrativos do tutorial, que não são preços de mercado, e onde o utilizador os troca pelos seus

Tabela 115 — Efeito das três rotinas de manutenção ilustrativas sobre o custo do resumo e sobre o resultado do tutorial (custos ilustrativos, não são preços de mercado)

Tabela 116 — Séries públicas recolhidas fora do programa, ainda não ligadas a ele, com a data de acesso e o início da soma de verificação

Tabela 117 — Premissas da projeção económica e o peso de cada uma no resultado

Tabela 118 — Estado do projeto do tutorial depois da análise económica (ilustrativo, não é preço de mercado)

Tabela 119 — Balanço de carbono do projeto do tutorial com cisterna de betão (fatores ilustrativos)

Tabela 120 — Emissões líquidas de carbono do projeto do tutorial conforme o material do reservatório (os preços são ilustrativos, não são preços de mercado)

Tabela 121 — Efeito do volume da cisterna de betão nas emissões líquidas de carbono

Tabela 122 — Efeito da troca de betão por polietileno nas três dimensões de análise (ilustrativo, não é preço de mercado)

Tabela 123 — Estado do projeto do tutorial depois da análise ambiental (ilustrativo, não é preço de mercado)

Tabela 124 — Matriz de decisão multicritério: cada volume da varredura avaliado nas três dimensões de análise (os custos são ilustrativos, não são preços de mercado)

Tabela 125 — Volume vencedor segundo cada critério isolado

Tabela 126 — Os sete critérios do multicritério e o sentido de preferência de cada um

Tabela 127 — Volume escolhido pelo TOPSIS conforme a dimensão com peso dominante, e o segundo classificado

Tabela 128 — Resumo do projeto do tutorial, com todos os parâmetros e resultados

Tabela 129 — Variáveis da Equação 51

Tabela 130 — Mensagens de validação física da entrada e a providência de cada uma

Tabela 131 — Mensagens da fração atendível e a providência de cada uma

Tabela 132 — Mensagens de erro da série de precipitação e a providência de cada uma

Tabela 133 — Mensagens de erro da varredura de volumes

Tabela 134 — Mensagens de erro dos parâmetros de cloragem

Tabela 135 — Mensagens de erro da análise económica e a providência de cada uma

Tabela 136 — Mensagens de erro da decisão multicritério e a providência de cada uma

Tabela 137 — Mensagens de erro dos parâmetros da eletrobomba

Tabela 138 — Situações de erro na leitura e na gravação de ficheiros

Tabela 139 — Avisos que não interrompem o cálculo e têm de constar do estudo

Tabela 140 — **Tabela 99** — Panorama das versões publicadas

Tabela 141 — Correções que alteram resultados na versão 0.1.0

Tabela 142 — Itens previstos para a versão 1.1

Tabela 143 — Itens previstos para a versão 2.0

Tabela 144 — As variáveis que a modulação probabilística pode sortear, com a distribuição de triagem que o ecrã propõe

Tabela 145 — O que cada variável económica e ambiental faz no cálculo, e o que não toca

Tabela 146 — As quatro distribuições que a ferramenta oferece, os seus parâmetros e quando usar cada uma

Tabela 147 — As variáveis sorteadas no exemplo do tutorial: distribuição declarada e estatísticas das realizações

Tabela 148 — Resultados no volume escolhido pelo estudo do tutorial: estudo determinístico e estatísticas das realizações (valores em €, ilustrativos, não são preços de mercado)

Tabela 149 — Probabilidades no volume escolhido, com o intervalo de confiança de 95% de Wilson

Tabela 150 — Frequência com que cada volume é escolhido nas realizações do exemplo, por critério (%)

Tabela 151 — Sensibilidade no volume escolhido: força e sentido da influência de cada variável sorteada sobre os resultados do tutorial

Tabela 152 — Parte da variância do resultado explicada por cada variável sorteada no exemplo do tutorial, no volume escolhido (η²; as variáveis contínuas agrupadas em decis)

Tabela 153 — Parâmetros do projeto: identificação

Tabela 154 — Parâmetros do projeto: chuva

Tabela 155 — Parâmetros do projeto: captação

Tabela 156 — Parâmetros do projeto: edificação

Tabela 157 — Parâmetros do projeto: procura

Tabela 158 — Parâmetros do projeto: rega

Tabela 159 — Parâmetros do projeto: qualidade da água

Tabela 160 — Parâmetros do projeto: reservatórios

Tabela 161 — Parâmetros do projeto: eletrobomba

Tabela 162 — Parâmetros do projeto: tubagem

Tabela 163 — Parâmetros do projeto: investimento

Tabela 164 — Parâmetros do projeto: exploração

Tabela 165 — Parâmetros do projeto: tarifário

Tabela 166 — Parâmetros do projeto: energia

Tabela 167 — Parâmetros do projeto: financeiro

Tabela 168 — Parâmetros do projeto: certificações

Tabela 169 — Parâmetros do projeto: outros

Tabela 170 — Fatores de emissão que o utilizador indica, e o que declarar em cada um

Tabela 171 — Fatores de emissão dos materiais dos reservatórios, com massa e fronteira

Tabela 172 — Referência registada no programa para cada fator de material, e a sua situação

Tabela 173 — Fatores de emissão dos consumíveis de tratamento

Tabela 174 — Os códigos da tabela tarifária de água

Tabela 175 — Como o programa guarda cada parcela da fatura portuguesa

Tabela 176 — As quatro formas de introduzir o saneamento

Tabela 177 — Os seis regimes tarifários e o que acontece ao poupar

Tabela 178 — Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço

Tabela 179 — Estrutura do tarifário do Funchal

Tabela 180 — Contas mensais de conferência do tarifário do Funchal

Tabela 181 — Estrutura do tarifário de Lisboa

Tabela 182 — Contas mensais de conferência do tarifário de Lisboa

Tabela 183 — Estrutura do tarifário do Porto

Tabela 184 — Contas mensais de conferência do tarifário do Porto

Tabela 185 — Concelhos com documento tarifário recolhido e ainda por transcrever

Tabela 186 — Estados de confiança dos valores tarifários e respetivos critérios

Tabela 187 — Concelhos e serviços por estado de confiança dos valores tarifários

Tabela 188 — Concelhos por distrito e estado de confiança dos valores tarifários

Tabela 189 — Concelhos com tarifário transcrito e o estado de cada serviço

Tabela 190 — Conteúdo da base de precipitação por concelho da Edição Ibérica

Tabela 191 — Concelhos de Portugal continental por nível de qualidade da chuva

Tabela 192 — Série de precipitação distribuída com a Edição Ibérica

Tabela 193 — Formatos que o programa lê e onde cada um é carregado

Tabela 194 — Formatos que o programa escreve e onde cada um é gerado

Tabela 195 — As sete secções do ficheiro de projeto e o que cada uma guarda

Tabela 196 — Localização dos ficheiros do programa e dos ficheiros do utilizador

Tabela 197 — Compatibilidade entre versões do ficheiro de projeto

Tabela 198 — Padronização terminológica de água de chuva e água pluvial

Tabela 199 — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial

Tabela 200 — Ficha de consulta: os dez passos de um estudo completo e a secção que trata de cada um

Tabela 201 — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada

Tabela 202 — Ficha de consulta: os seis regimes tarifários e o efeito de poupar

Tabela 203 — Ficha de consulta: os indicadores e a pergunta que cada um responde

Tabela 204 — Os casos de exemplo e o que cada um demonstra

Tabela 205 — Resultado que cada caso de exemplo produz ao ser relido e simulado

---

## Lista de equações

Equação 1 — Fechamento do balanço de massa

Equação 2 — Volume captado no dia

Equação 3 — Volume disponível antes do consumo

Equação 4 — Volume extravasado

Equação 5 — Volume armazenado antes do consumo

Equação 6 — Volume de água pluvial consumido

Equação 7 — Volume remanescente para o dia seguinte

Equação 8 — Complemento de água potável da rede

Equação 9 — Classificação do dia quanto ao atendimento

Equação 10 — As três parcelas da demanda diária

Equação 11 — Ganho marginal por metro cúbico acrescentado

Equação 12 — Volume ideal pelo critério de ganho marginal

Equação 13 — Fração de armazenamento

Equação 14 — Potencial de economia de água potável

Equação 15 — Confiabilidade volumétrica

Equação 16 — Relação entre potencial e confiabilidade

Equação 17 — Extravasamento médio diário

Equação 18 — Eficiência de uso da água captada

Equação 19 — Volume anual de água potável poupado

Equação 20 — Demanda média diária não atendida

Equação 21 — Precipitação total anual, PRCPTOT

Equação 22 — Precipitação em dias muito úmidos, R95p

Equação 23 — Máxima precipitação em um dia, RX1day

Equação 24 — Máxima precipitação em cinco dias, RX5day

Equação 25 — Índice simples de intensidade diária, SDII

Equação 26 — Dias de precipitação intensa, R20mm

Equação 27 — Dias secos consecutivos, CDD

Equação 28 — Dias úmidos consecutivos, CWD

Equação 29 — Índice de sazonalidade, SI

Equação 30 — Massa de produto clorado por metro cúbico

Equação 31 — Investimento incremental da linha de tratamento

Equação 32 — Consumo específico de energia de recalque

Equação 33 — Consumo específico a partir da vazão

Equação 34 — Vazão de recalque deduzida da potência

Equação 35 — Energia consumida nas partidas

Equação 36 — Energia anual da motobomba

Equação 37 — Energia anual do pressurizador

Equação 38 — Economia mensal na fatura

Equação 39 — Parcela de esgoto da fatura

Equação 40 — Investimento inicial total

Equação 41 — Fator acumulado de inflação

Equação 42 — Fator acumulado de reajuste tarifário

Equação 43 — Valor presente líquido

Equação 44 — Emissão incorporada de um componente

Equação 45 — Emissão anual da energia de bombeamento

Equação 46 — Saldo líquido anual de emissões

Equação 47 — Tempo de retorno ambiental

Equação 48 — Saldo de carbono ao fim da vida útil

Equação 49 — Emissão específica por litro entregue

Equação 50 — Coeficiente de proximidade do TOPSIS

Equação 51 — Transformação da série para emular o Netuno 4

---


---
# 1. Comece aqui

---

## 1.1. O que o Triton faz, e o que não faz

O Triton simula sistemas de aproveitamento de água da chuva em edifícios. Dado o regime de chuva de um lugar, a cobertura de um edifício e o consumo de quem o ocupa, responde **quanta água potável o sistema substitui**, a que custo, com que qualidade e com que impacto de carbono.

Esta secção começa pelo princípio. As duas primeiras subsecções tratam do próprio objeto, antes do programa. Quem já projeta redes prediais de água acha-as elementares e pode ir direto às seis dimensões de análise, onde o Triton aparece. Quem chega agora ao assunto encontra aí o vocabulário que o resto do manual usa sem o explicar de novo.

---

### 1.1.1. O que é um sistema de aproveitamento de água da chuva

É um sistema que **recolhe a chuva que cai na cobertura e a usa no lugar da água da rede pública**, nos usos que não exigem água potável.

A ideia é velha e simples. Só uma coisa a torna difícil: a chuva não cai quando é precisa. Por isso o sistema precisa de um reservatório, e por isso o tamanho desse reservatório é a pergunta central de todo o projeto — e deste manual. A Figura 1 mostra os componentes do sistema e o percurso da água, da captação ao ponto de uso.

![O caminho da água, da cobertura ao ponto de uso](../figuras/fig00_sistema.png)

*Figura 1 — Componentes de um sistema predial de aproveitamento de água da chuva e percurso da água, da captação ao ponto de uso. O reservatório superior aparece a tracejado porque é opcional: num edifício de um só piso, a eletrobomba pode pressurizar diretamente os pontos de uso, e o reservatório superior altera o momento em que a água é fornecida, não o volume disponível.*

Da esquerda para a direita:

**A cobertura** é a área de captação. Conta a **projeção horizontal** do telhado, não a área inclinada: é a sombra do telhado no chão que recebe a chuva. Errar aqui é o primeiro dos dez enganos da secção 5.1.

**As caleiras e os tubos de queda** levam a água até à cisterna. O programa não os dimensiona. Isso é projeto de drenagem pluvial predial e segue a regulamentação portuguesa aplicável (ver o fim desta secção).

**O dispositivo de descarte das primeiras águas** desvia os primeiros milímetros de cada chuvada, que arrastam o pó, as folhas e os dejetos de aves acumulados na cobertura. É a medida de controlo de qualidade mais barata. A secção 4.6 mostra quanto muda a água que chega ao reservatório.

**A cisterna**, ou reservatório inferior, armazena a água captada. Quando a afluência excede a capacidade, o excedente **extravasa** para a rede de drenagem. Este extravasamento não é desperdício por descuido: é a consequência inevitável de guardar um recurso que chega concentrado.

**A eletrobomba e o reservatório superior** distribuem a água. Num edifício de um só piso, a eletrobomba pode pressurizar diretamente os pontos de uso. Em edifícios de dois ou mais pisos, costuma adotar-se um reservatório elevado: a água é elevada até ele e distribuída por gravidade.

**Os usos não potáveis** são o destino: autoclismos e urinóis, lavagem de pavimentos e de veículos, rega de jardins. Quando a água da chuva não chega, a **rede pública** fornece o complemento, e o abastecimento nunca é interrompido.

O diagrama da Figura 1 mostra o encadeamento das peças, que é o que interessa para seguir o cálculo. Falta-lhe a informação que decide metade das dúvidas de projeto: onde fica cada peça em relação às outras, e a que altura. O corte da Figura 2 repõe essa geometria. O desnível decide se a água desce por gravidade ou precisa de bomba, e a posição da cisterna em relação ao terreno é uma decisão de obra, não de cálculo.

![O sistema em corte, com as peças na altura em que realmente ficam](../figuras/fig00d_corte.png)

*Figura 2 — O mesmo sistema visto em corte. A área de captação é a projeção horizontal da cobertura, não a área inclinada do telhado. O reservatório elevado recebe a água elevada da cisterna e devolve-a aos pontos de uso por gravidade; a rede pública alimenta-o, com separação atmosférica, no volume que a água da chuva não cobre. O extravasor da cisterna conduz o excedente à rede de drenagem.*

> **Vocabulário que o manual usa o tempo todo.** *Cisterna* e *reservatório inferior* designam o mesmo componente. *Extravasamento* é o volume excedente que o extravasor conduz à rede de drenagem. *Procura pluvial* é a parte do consumo que a água da chuva pode atender; *procura total* é o consumo inteiro do edifício. O apêndice G traz o glossário completo.

---

### 1.1.2. O que o programa calcula, num dia

O programa faz uma conta de entradas e saídas, todos os dias, para cada dia da série de chuva. A Figura 3 mostra como a precipitação de um dia se reparte. A conta é esta:

![Como a chuva de um dia se reparte](../figuras/fig00b_destino.png)

*Figura 3 — Destino da precipitação de um dia. Cada caixa é uma parcela do balanço, e a soma do volume extravasado, do volume consumido e do volume armazenado é igual ao volume captado. O extravasamento é calculado antes do consumo do dia, e a chuva do dia já pode atender o consumo do dia: uma ordem intermédia entre as regras YAS e YBS, explicada na secção do balanço diário.*

Lendo o desenho:

1. **Desconta-se o descarte.** Com 12 mm de precipitação e 2 mm de descarte, restam 10 mm de precipitação efetiva.
2. **Converte-se em volume.** Dez milímetros sobre 100 m² de telhado, com coeficiente de escoamento de 0,85, dão 850 litros. A conta é `mm × m² × coeficiente` e sai diretamente em litros, porque um milímetro sobre um metro quadrado é exatamente um litro.
3. **Soma-se ao volume armazenado na cisterna.** O que exceder a capacidade **extravasa** para a rede de drenagem.
4. **Retira-se o consumo do dia**, até ao limite da procura pluvial.
5. **O volume remanescente passa para o dia seguinte.** É esta dependência entre dias consecutivos que torna necessária a simulação diária.

Os cinco passos formam um ciclo, não uma lista: o volume que sobra no fim do quinto passo é exatamente o volume de que o terceiro parte no dia seguinte. Esta ligação entre um dia e o outro é a única coisa que uma conta sobre a média anual não reproduz, e é a razão de a simulação ser diária. A Figura 4 representa a sequência na notação das equações do balanço diário.

![A ordem das operações de um dia, e a memória que liga um dia ao seguinte](../figuras/fig00e_balanco_do_dia.png)

*Figura 4 — Sequência de operações do balanço diário, na ordem em que o programa as executa, na notação das equações da secção do balanço diário. A ligação a roxo, que contorna o desenho, representa a dependência entre dias consecutivos: o volume remanescente V_res,t é o volume inicial do dia seguinte.*

> **Aprofundamento: porque não basta a média anual.** É tentador dividir a chuva anual por 365 e fazer a conta de uma vez. O resultado é sempre otimista, e por vezes muito. A chuva chega **concentrada**: enche a cisterna num dia, extravasa, e depois falta durante duas semanas. A média não representa nem o extravasamento nem o défice, e ambos reduzem o aproveitamento. A secção 2.1 mostra isto numa tabela de dez dias que pode refazer numa folha de cálculo, e a secção 4.4 mostra o tamanho do erro.

Repetida ao longo de trinta anos de série, esta conta produz a resposta central do programa: o **potencial de economia de água potável**, a fração do consumo total do edifício que a chuva conseguiu substituir.

---

### 1.1.3. As seis dimensões

O volume de água fornecido é a primeira questão de um projeto, mas não a única. O programa avalia o sistema em seis dimensões, que em geral conduzem a volumes ótimos distintos (Figura 5).

![As seis dimensões de análise do programa](../figuras/fig26_dimensoes.png)

*Figura 5 — As seis dimensões de análise e a questão avaliada em cada uma. O programa percorre-as por esta ordem, e cada uma é tratada numa secção própria do capítulo do método.*

Cada dimensão tem tratamento próprio no capítulo do método: a técnica nas secções 2.1 a 2.4, a qualidade na 2.5, a económica na 2.7, a ambiental na 2.8, a certificação na 2.9 e a decisão na 2.10.


A sexta dimensão distingue o programa de uma folha de cálculo. As cinco primeiras dão resultados **divergentes**: o volume de maior poupança de água raramente é o de maior retorno financeiro, e nenhum dos dois costuma ser o de melhor desempenho ambiental. A decisão multicritério torna explícitos os pesos atribuídos a cada critério.

---

### 1.1.4. O que o programa **não** faz

Começar pelos limites é invulgar, e deliberado. Poupa tempo a quem abriu o programa à espera de outra coisa.

**Não dimensiona a instalação hidráulica.** Não calcula o traçado, o diâmetro de cada troço nem a inclinação da rede. O assistente de eletrobomba estima o diâmetro e a perda de carga da conduta de elevação para escolher o equipamento, mas não substitui o projeto da instalação. O esquema exportado em DXF é um esquema; o projeto de execução é do projetista.

**Não detalha o dispositivo de descarte.** O programa calcula o volume do reservatório de descarte, igual à área de captação vezes a lâmina, e orça-o com o separador de folhas. A disposição das ligações, a purga e a ligação à drenagem são projeto hidráulico à parte.

**Não substitui ensaios de qualidade da água.** Dimensiona o equipamento de tratamento a partir de premissas. As constantes do modelo de lavagem da cobertura não estão calibradas com medições, e a qualidade resultante é uma premissa, não um resultado.

**Não modela o passo horário.** Uma chuva de 40 mm em duas horas e a mesma lâmina em vinte e quatro horas dão o mesmo resultado.

**Não faz o inventário completo do ciclo de vida.** A avaliação é de **triagem**, numa única categoria de impacto — o carbono. Não há eutrofização, acidificação, uso do solo nem toxicidade.

**Não certifica.** Mostra onde o projeto se enquadraria. A certificação cabe ao organismo certificador, com a documentação completa do empreendimento.

**Não conhece o local.** Não sabe se o volume cabe no terreno, se o nível freático é alto, nem se a estrutura aguenta o reservatório elevado.

A secção 5.2 traz a lista completa das limitações conhecidas, com as consequências de cada uma.

---

### 1.1.5. Para quem serve

O manual serve quatro perfis de leitor, com percursos de leitura independentes entre si (Figura 6).



![Os quatro perfis de leitor e o percurso de cada um](../figuras/fig27_leitores.png)

*Figura 6 — Os quatro percursos de leitura do manual. São independentes entre si, e o manual foi organizado para que cada um se possa seguir isoladamente.*

Em números de secção: o estudante segue o capítulo 4, o tutorial do princípio ao fim; o projetista usa os guias do capítulo 3 e o roteiro da secção 1.3; o investigador vai ao método do capítulo 2; e o revisor encontra no capítulo 5 a verificação e os limites declarados.


Quem começa agora deve percorrer o capítulo 4 inteiro, pela ordem em que está escrito. Constrói um projeto de raiz, em Lisboa, e acompanha-o até à decisão final. Cada secção termina a mostrar onde o projeto chegou, para o leitor ver o estudo a formar-se em vez de o receber concluído.

---

### 1.1.6. Normas e entidades de referência

A norma europeia de referência para estes sistemas é a EN 16941-1, sobre sistemas de água não potável no local (sistemas de aproveitamento de água da chuva). Cobre o projeto, o dimensionamento, a instalação, a identificação, a colocação em serviço e a manutenção, com exclusão da água para beber e para a preparação de alimentos. A edição de 2018 foi retirada em 22 de março de 2024 (BSI, https://knowledge.bsigroup.com/products/on-site-non-potable-water-systems-systems-for-the-use-of-rainwater, consultado em 16/10/2026). [A COMPLETAR: confirmar o ano da edição em vigor da EN 16941-1 e a transposição para a norma portuguesa NP EN 16941-1, no catálogo do IPQ.]

Em Portugal, a especificação técnica ETA 0701 da ANQIP (Associação Nacional para a Qualidade nas Instalações Prediais) estabelece critérios para estes sistemas em edifícios, para fins que não o consumo humano. Recomenda o desvio de um volume correspondente a 2 mm de precipitação, e remete o projeto de redes prediais para o Regulamento Geral dos Sistemas Públicos e Prediais de Distribuição de Água e de Drenagem de Águas Residuais (Decreto Regulamentar n.º 23/95, de 23 de agosto). A versão consultada é a 7, com validade indicada de 23/01/2009 a 23/01/2014 (cópia no repositório do IPL, https://repositorio.ipl.pt/bitstreams/27266c84-d607-4ad7-9c68-9b51a215314f/download). [A COMPLETAR: confirmar no sítio da ANQIP a revisão em vigor da ETA 0701, e se o Decreto Regulamentar n.º 23/95 continua em vigor sem alterações relevantes para este uso.]

---

### 1.1.7. Uma palavra sobre os resultados

Todo o número que o programa produz é **condicional às premissas declaradas**. O programa não descobre verdades; calcula consequências.

Por isso o manual insiste tanto na declaração. A secção 4.10 traz a lista do que deve constar num artigo, a secção 5.1 os dez enganos que o programa não impede, e a secção 5.2 o que ele não cobre.

Um estudo que declara as suas premissas e os seus limites é mais útil — e mais defensável — do que um que apresenta um número isolado.

---

## 1.2. Instalação e primeira execução

> No fim desta secção, tem o programa instalado e aberto, e uma simulação concluída com um resultado que pode conferir contra este manual.

---

### 1.2.1. O que é preciso

<!-- tabela: **Tabela 1** — Requisitos de sistema para instalar e executar o programa -->
| Requisito | O que é preciso |
| :--- | :--- |
| sistema | Windows 10 ou 11, 64 bits |
| espaço em disco | cerca de 0,7 GB |
| memória | 4 GB chegam; 8 GB deixam o varrimento mais folgado |
| privilégios | de administrador, para instalar para todos os utilizadores; sem eles, a instalação vai para a pasta do utilizador |

Não é preciso instalar mais nada. O programa é distribuído já montado, com todos os componentes de que depende para calcular, e não exige a instalação prévia de interpretadores, bibliotecas ou pacotes auxiliares. Também não precisa de ligação à internet: tudo o que consulta durante uma simulação está no próprio computador.

---

### 1.2.2. A edição

Esta é a Edição Ibérica (IBE), o «Triton IBE», que se chamou Edição Portugal (PRT). Está em português de Portugal, trabalha em euros e, por agora, só traz dados de Portugal (a linha de cobertura do programa diz: Espanha, 0 locais): a chuva diária por concelho e os tarifários de água de Lisboa, do Porto e do Funchal. O selo vermelho no topo da barra lateral, o título da janela e o rodapé de cada relatório e de cada exportação dizem de que edição saiu o estudo.

<!-- tabela: **Tabela 2** — O que a Edição Ibérica traz e o que deixa ao utilizador -->
| | Edição Ibérica (IBE) |
| :--- | :--- |
| instalador | `Triton_IBE_Setup_0_1_0.exe` |
| idioma ao abrir | português de Portugal |
| chuva | base E-OBS por concelho (278 concelhos do Continente) ou série própria; Açores e Madeira só com série própria; série de exemplo do Funchal |
| tarifas de água, saneamento e resíduos | tarifários de Lisboa, do Porto e do Funchal; nos outros concelhos, digitadas |
| eletricidade | digitada (o Funchal traz a tarifa da EEM) |
| moeda e custos | euro, a única oferecida; custos digitados |
| fator de emissão da rede e da água potável | do local do projeto, obrigatórios |
| certificações e incentivos | LEED, EDGE, GRI |
| etapa 12 | Modulação Probabilística |
| custo da tubagem e da mão de obra | digitado |
| manual que o programa abre | este manual |
| preferências guardadas | `Triton-IBE` |

O método é o mesmo em qualquer país: o balanço diário, o descarte inicial, os coeficientes de escoamento, a análise económica e a avaliação do ciclo de vida são um só motor. O que muda de país para país são os **dados**. Os custos de obra, de bomba, de tratamento e de manutenção não vêm definidos: dependem do local e do mercado, e o utilizador introduz os seus. Os custos que este manual usa nos casos são **ilustrativos, não são preços de mercado**.

Sem os fatores de emissão do local, o programa não calcula a avaliação ambiental: um fator de outra rede elétrica daria um resultado errado sem qualquer aviso.

Quando uma exigência de uma norma nacional importa, o manual descreve-a em termos gerais e pede que consulte a norma aplicável ao local do edifício (ver a secção 1.1).

---

### 1.2.3. A instalação

1. Execute **`Triton_IBE_Setup_0_1_0.exe`**. O instalador pergunta se a instalação é para todos os utilizadores, o que exige administrador, ou só para si.
2. Escolha o idioma da instalação, leia e aceite a licença (código-fonte académico, uso não comercial).
3. Escolha o tipo de instalação. A **padrão** traz o programa, o manual, os casos, os exemplos e todos os idiomas. A **personalizada** permite desmarcar os pacotes de idioma espanhol e chinês.
4. Aceite a pasta sugerida, `C:\Program Files\Triton IBE`, ou escolha outra.
5. Marque, se quiser, **criar ícone no ambiente de trabalho**. A opção **abrir ficheiros .triton com o Triton** vem desmarcada, para não tomar os ficheiros de outra edição do Triton instalada no mesmo computador; marque-a se quiser abrir um projeto com um duplo clique.
6. No fim, o instalador oferece-se para abrir o programa.

Depois, o menu Iniciar tem dois atalhos: o programa e o seu manual em PDF (este documento). Para desinstalar, use *Aplicações e funcionalidades* do Windows, como com qualquer programa; os seus projetos ficam onde os guardou.

> **O que o instalador põe no computador.** O programa, a base de chuva diária por concelho (E-OBS), a série de exemplo do Funchal, a base de tarifários, os ficheiros de exemplo e este manual. Nada é transferido durante a utilização: o Triton funciona sem ligação à internet.

---

### 1.2.4. Onde ficam os seus ficheiros

O programa nunca decide por si onde guardar. De cada vez que grava um projeto, um relatório ou uma exportação, pergunta a pasta.

<!-- tabela: **Tabela 3** — Formatos de ficheiro que o programa grava e o conteúdo de cada um -->
| O que grava | Extensão | Contém |
| :--- | :--- | :--- |
| projeto | `.triton` | todos os dados de entrada **e a série de chuva** |
| relatório | `.pdf` | o documento completo do estudo |
| resultados | `.xlsx`, `.csv` | as tabelas, para folha de cálculo |
| esquema | `.dxf` | o desenho esquemático, para CAD |

Destes formatos, o `.triton` é o que mais importa guardar. É autocontido: leva dentro de si a série de chuva e, por isso, abre em qualquer outro computador mesmo sem os ficheiros que lhe deram origem. Uma exceção: a chuva da base E-OBS, que acompanha o programa. O ficheiro guarda a referência da série — concelho e intervalo de datas —, com o número de dias, o total e uma impressão digital (SHA-256) dos valores, e o programa recompõe-na a partir da base ao abrir o projeto, conferindo a impressão. Uma série alterada depois de carregada, ou uma base indisponível ao gravar, continua a ir inteira para o ficheiro. ==É também o ficheiro a anexar a um artigo para que outra pessoa reproduza o estudo,== e é esta propriedade que separa um trabalho verificável de um trabalho apenas relatado.

---

### 1.2.5. A base climática

O programa traz a chuva diária de 278 concelhos do Continente, extraída da E-OBS v33.0e (Copernicus/KNMI, grelha de 0,1°, 1950 a 2025). A série de um concelho é a média das células da grelha com centro dentro dos seus limites. Os Açores e a Madeira não têm série na base e pedem uma série própria. Aceita ainda qualquer série própria em CSV: precipitação diária em milímetros, um valor por dia, como descreve o apêndice F.

A E-OBS é uma grelha interpolada de observações, não um registo de pluviómetro. Serve para estudos e para os exemplos deste manual. Num projeto real, use a série medida no local sempre que a tiver.

> **Dados de reanálise no Funchal.** A E-OBS não dá uma série utilizável para o Funchal (faltam dados em 22% dos dias de 1991 a 2020, e o critério admite no máximo 1%). A série de exemplo do Funchal é por isso reanálise ERA5, de uma célula de cerca de 9 km, e pode diferir da média medida na estação.

---

### 1.2.6. Os ficheiros de exemplo

O manual vem acompanhado de projetos prontos, que reproduzem os resultados impressos aqui.

<!-- tabela: **Tabela 4** — Ficheiros de exemplo distribuídos com o programa -->
| Ficheiro | Para que serve |
| :--- | :--- |
| `casos\01_tutorial_lisboa.triton` | o projeto que o capítulo 4 constrói, pronto |
| `casos\05_dez_dias.triton` | o caso didático de dez dias da secção 2.1 |
| `casos\02_porto.triton` e `casos\03_funchal.triton` | a mesma moradia noutras cidades |
| `exemplos\portugal\*.triton` | três estudos completos: Lisboa, Porto e Funchal |

Ficam na pasta do programa. O apêndice J lista os dez casos do manual, com o capítulo de cada um e o resultado que produzem.

Convém começar pelo caso de dez dias. Abra-o, execute a simulação e compare o resultado com a tabela impressa na secção 2.1. Se coincidirem, a instalação corresponde exatamente a este manual. Se divergirem, o manual e o programa são de versões diferentes, e a secção 6.3 explica o que fazer.

---

### 1.2.7. A primeira simulação, em cinco minutos

O programa organiza-se em **etapas**, na barra lateral esquerda, pela ordem em que se trabalha. Para a primeira simulação bastam quatro.

1. **Projeto e Chuva.** Escolha o concelho de Lisboa na base climática. Indique a área de captação de 150 m², o coeficiente de escoamento de 0,85 e o descarte de 2,0 mm.
2. **Edificação e Consumo.** Escolha moradia unifamiliar, 4 moradores, 150 litros por habitante e dia, e fração atendível de 28%.
3. **Reservatório & Custos.** Indique um volume fixo de 3.000 L.
4. Simule e vá a **Resultados Técnicos**.

Deve obter um potencial de economia próximo de **15%** (15,39% com a série de Lisboa).

A secção 4.3 explica o que este número significa, e a secção 4.4 faz a pergunta seguinte: serão 3.000 L o volume certo?

---

### 1.2.8. Se algo correr mal

**O programa não abre.** Verifique se a instalação terminou sem erros e reinstale por cima; a reinstalação preserva os seus ficheiros, porque não ficam na pasta do programa.

**A lista de concelhos está vazia.** Confirme que a base de chuva (`data\portugal_eobs.db`) está na pasta do programa; se faltar, reinstale. Nos Açores e na Madeira, use um ficheiro de chuva próprio.

**Falta alguma parte do programa, como a volumetria 3D.** Execute, na Linha de Comandos, `"C:\Program Files\Triton IBE\Triton_IBE.exe" --diagnostico` (com a pasta predefinida). O programa lista o que a instalação traz: o visualizador 3D, a base de chuva, a base de tarifários e o manual. Cada item sai marcado OK ou FALTA. A lista fica também gravada em `triton_diagnostico.txt`, na pasta temporária do Windows. Envie esse ficheiro com a descrição do problema.

**O resultado não bate com o manual.** Confira, por esta ordem: a série de chuva carregada, a área, o coeficiente, a lâmina de descarte, a procura e a fração atendível. Uma divergência de resultado é quase sempre uma divergência de entrada, e a secção 5.1 lista os enganos mais comuns.

**Apareceu uma mensagem de erro.** A secção 6.2 traz as mensagens do programa, o que cada uma significa e o que fazer.

---

## 1.3. Por onde começar, conforme o seu objetivo

Este manual reúne cinquenta e quatro secções em oito capítulos e não foi pensado para se ler do princípio ao fim. Funciona melhor como obra de consulta: cada leitor entra pelo ponto que corresponde ao que precisa de fazer. Esta secção existe para indicar esse ponto de entrada.

---

### 1.3.1. Roteiro por objetivo

A tabela abaixo relaciona os cinco propósitos mais comuns de quem abre o programa com o percurso de leitura de cada um.

<!-- tabela: **Tabela 5** — Percurso de leitura recomendado conforme o objetivo do leitor -->
| Quer | Leia |
| :--- | :--- |
| **aprender a usar** o programa | o capítulo 4 inteiro, secções 4.1 a 4.10, por ordem |
| **resolver um caso** hoje | as três perguntas abaixo e, depois, o guia do capítulo 3 que servir |
| **publicar** um estudo | o capítulo 2, que traz o método, e a secção 4.10, com a lista de declaração |
| **rever** um estudo alheio | o capítulo 5 e os apêndices A e B |
| **exportar** para CAD, BIM ou folha de cálculo | a secção 3.9 |
| **não errar** | a secção 5.1, com os dez enganos mais comuns |

Quem tem uma hora e nenhuma familiaridade prévia deve ler o tutorial do capítulo 4. Constrói um estudo completo em torno de um único projeto, em Lisboa, e cada secção termina a mostrar onde o projeto chegou. O leitor acompanha a construção em vez de receber o resultado feito.

---

### 1.3.2. As três perguntas que definem um estudo

Antes de abrir o programa, convém responder a três perguntas. Elas determinam boa parte das decisões seguintes, e responder-lhes depois costuma obrigar a refazer trabalho.

#### 1.3.2.1. Que usos vai a água da chuva atender?

A resposta define a **fração atendível**, e a fração atendível é o teto de tudo o resto: um sistema com fração de 28% nunca poupará mais de 28% do consumo total, por maior que seja a cisterna e por mais que chova. Nenhuma decisão de projeto posterior altera este limite, e por isso convém fixá-lo primeiro. A Figura 7 reúne as gamas habituais da fração atendível conforme os usos previstos.

![A fração atendível conforme os usos previstos](../figuras/fig46_atendivel.png)

*Figura 7 — Que parte do consumo total a água da chuva pode atender, conforme os usos que o projeto prevê. É o teto do potencial de economia: nenhum reservatório, por maior que seja, ultrapassa esta fração.*

Os casos residenciais tratam-se na secção 4.2 e o caso comercial na secção 3.5. A linha a tracejado marca os 28% do tutorial, que ficam nos usos não potáveis que a orientação sobre águas pluviais em geral admite: autoclismos, lavagens e rega. [A COMPLETAR: citar, com a fonte aberta, o artigo da ETA 0701 da ANQIP (ou da norma portuguesa em vigor) que lista os usos admitidos.]


#### 1.3.2.2. Vai comparar volumes ou avaliar um só?

A diferença entre avaliar um volume conhecido e procurar o volume adequado determina o modo de simulação e, com ele, o tempo de cálculo e a riqueza do resultado.

<!-- tabela: **Tabela 6** — Escolha entre volume fixo e varredura conforme a pergunta do estudo -->
| Se quer | Use | Onde se trata |
| :--- | :--- | :--- |
| avaliar uma cisterna que já existe | volume fixo | secção 4.3 |
| descobrir o volume a comprar | **varredura** | secções 4.4 e 2.2 |
| escolher entre critérios que discordam | varredura e multicritério | secções 4.9 e 2.10 |

==A varredura é quase sempre a resposta certa.== Custa mais tempo de cálculo, da ordem dos segundos, e produz a curva de retorno decrescente, o argumento mais forte de que um estudo dispõe para justificar um volume.

#### 1.3.2.3. Precisa de reservatório superior?

A terceira pergunta é hidráulica. A resposta depende da altura do edifício e da pressão exigida nos pontos de consumo.

<!-- tabela: **Tabela 7** — Critérios hidráulicos para decidir sobre o reservatório superior -->
| Se o edifício | Então | Onde se trata |
| :--- | :--- | :--- |
| é térreo e os pontos ficam perto da cisterna | pressurização direta, sem reservatório superior | secção 4.5 |
| é moradia de dois pisos ou prédio | reservatório superior, por **pressão** | secção 4.5 |
| precisa de reserva contra falhas de energia | reservatório superior | secção 4.5 |

> O reservatório superior **não aumenta** a poupança de água. Com o mesmo armazenamento total, entrega um pouco menos e gasta energia de elevação. A decisão de o adotar deve ser hidráulica, nunca fundada na expectativa de um aproveitamento maior. No tutorial de Lisboa, a diferença é de 0,31 pontos percentuais (secção 4.5).

---

### 1.3.3. A ordem de trabalho no programa

A barra lateral do programa está numerada, e a numeração segue a ordem em que se trabalha. As quatro primeiras etapas são de entrada de dados, as cinco seguintes apresentam resultados, e as restantes produzem saídas ou dão apoio ao estudo (Figura 8).

![As etapas do programa, na ordem de trabalho](../figuras/fig28_etapas.png)

*Figura 8 — As etapas do programa, agrupadas por natureza. As quatro primeiras são de entrada e devem ser preenchidas por ordem, porque cada uma usa o que a anterior definiu; as cinco seguintes são de leitura de resultados; as restantes produzem saídas ou dão apoio, e podem ser usadas a qualquer momento.*

Onde este manual trata cada uma: a etapa 1 na secção 4.1, a 2 na 4.2, a 3 na 4.6, a 4 nas secções 4.3, 4.4 e 4.7, a 5 na 4.3, a 6 na 4.7, a 7 na 4.8, a 8 na 4.9, a 9 na 4.10, a 10 na 3.9 e a 12, a Modulação Probabilística, nas secções 7.1 a 7.5. A etapa 11 é a documentação incorporada no programa e não tem secção correspondente aqui. A Edição Ibérica não traz catálogo de tarifários de todos os concelhos, e por isso não tem etapa de gestão de tarifas: os tarifários de Lisboa, do Porto e do Funchal vêm já nos projetos de exemplo, e nos restantes concelhos digita as tarifas do seu projeto na etapa económica. A numeração não tem salto.


Convém guardar o projeto no fim de cada etapa. Os parâmetros do apêndice A são gravados e relidos na íntegra, e o ficheiro resultante é a prova documental do estudo, tanto para quem o refizer no futuro como para quem o avaliar.

---

### 1.3.4. Antes de publicar

Três leituras são obrigatórias para quem pretende publicar resultados, e nenhuma é longa. A secção 4.10 traz a lista do que declarar num artigo, com um parágrafo de método pronto a adaptar. A secção 5.1 reúne os dez enganos de projeto que o programa não consegue impedir. E a secção 5.2 lista as limitações conhecidas — das quais interessa ler não todas, mas as que afetam o caso em mãos.

O apêndice I condensa as três em fichas de uma página, para consulta rápida.

---

# 2. O método

---

## 2.1. O balanço hídrico diário

> No fim desta secção, será capaz de refazer, numa folha de cálculo, exatamente o que o Triton
> faz em cada dia da série, e de dizer por que razão o programa chegou ao número a que chegou.

> **Antes de começar.** O capítulo 2 é a camada técnica do manual: mostra as contas por
> dentro. Não precisa dele para usar o programa, porque o capítulo 4 basta, mas precisa
> dele para **defender** um resultado, seja perante um júri, numa revisão ou diante de um cliente
> que perguntou de onde saiu o número.

Esta é a secção de que todas as outras dependem. O potencial de poupança, o fluxo de caixa, a
emissão evitada e a ordenação multicritério saem, todos, dos números que o balanço diário produz.
Quem entende esta secção entende o programa.

O Triton usa um **modelo comportamental de passo diário**: para cada dia da série de precipitação,
o programa resolve o que entra no reservatório, o que sai, o que extravasa e o que fica
armazenado. Não há distribuição de probabilidade nem valor médio anual. Há a série, dia após dia,
e a mesma conta repetida.

---

### 2.1.1. A ordem das operações

O programa executa, para cada dia `t`, sempre por esta ordem:

1. **decide se descarta** a primeira chuva, conforme o modo escolhido;
2. **converte a lâmina em volume** captado, com a área e o coeficiente;
3. **soma ao que sobrou de ontem** e verifica o extravasamento;
4. **satisfaz a procura pluvial** com o que está armazenado;
5. **reparte** o abastecimento entre uso interior e rega;
6. **completa com água da rede** o que a chuva não satisfez;
7. **classifica** o dia como de abastecimento pleno, parcial ou nulo.

A ordem não é arbitrária, e trocar dois passos muda o resultado. O item 2.1.4 volta a este
ponto.

---

### 2.1.2. O caso resolvido

Dez dias, uma moradia, sem reservatório superior. A chuva é a de Lisboa, de 11 a 20 de dezembro
de 2019, na base E-OBS por concelho. A janela foi escolhida por busca determinística entre os
trinta anos da série, por reunir num só período os cinco fenómenos que a secção ensina. Os
números cabem numa folha de cálculo.

<!-- tabela: **Tabela 8** — Dados de entrada do caso resolvido de dez dias -->
| Dado de entrada | Valor |
| :--- | ---: |
| área de captação | 100 m² |
| coeficiente de escoamento | 0,85 |
| lâmina de descarte | 2,0 mm, em todo o evento |
| procura total | 200 L/dia |
| fração suprível por água da chuva | 40% = 80 L/dia |
| volume do reservatório inferior | 2 000 L |
| reservatório superior | nenhum |
| chuva | Lisboa, 11 a 20 de dezembro de 2019 (E-OBS, por concelho) |

A série de chuva dos dez dias, em milímetros:

<!-- tabela: **Tabela 9** — Série de precipitação dos dez dias do caso resolvido (Lisboa, dezembro de 2019) -->
| Dia | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Chuva | 0,0 | 2,1 | 0,0 | 1,2 | 6,0 | 13,5 | 0,7 | 8,1 | 35,7 | 25,8 |

Sem procura exterior, a procura pluvial diária é a procura interior vezes a fração não potável
interior, que aqui coincide com a fração suprível total: 200 × 0,40 = **80 L/dia**. É este o
volume que o sistema tenta entregar todos os dias.

#### 2.1.2.1. A tabela, dia a dia

<!-- tabela: **Tabela 10** — Balanço hídrico diário do caso resolvido, dia a dia, com captação, consumo, extravasamento e armazenamento -->
| Dia | Chuva | Descarte | Chuva efetiva | Captado | Procura pluvial | Consumido | Extravasado | No reservatório | Abastecimento |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| | mm | mm | mm | L | L | L | L | L | |
| 1 | 0,0 | 0,0 | 0,0 | 0 | 80 | 0 | 0 | 0 | nulo |
| 2 | 2,1 | 2,0 | 0,1 | 9 | 80 | 9 | 0 | 0 | parcial |
| 3 | 0,0 | 0,0 | 0,0 | 0 | 80 | 0 | 0 | 0 | nulo |
| 4 | 1,2 | 1,2 | 0,0 | 0 | 80 | 0 | 0 | 0 | nulo |
| 5 | 6,0 | 2,0 | 4,0 | 340 | 80 | 80 | 0 | 260 | pleno |
| 6 | 13,5 | 2,0 | 11,5 | 978 | 80 | 80 | 0 | 1 158 | pleno |
| 7 | 0,7 | 0,7 | 0,0 | 0 | 80 | 80 | 0 | 1 078 | pleno |
| 8 | 8,1 | 2,0 | 6,1 | 518 | 80 | 80 | 0 | 1 516 | pleno |
| 9 | 35,7 | 2,0 | 33,7 | 2 865 | 80 | 80 | 2 380 | 1 920 | pleno |
| 10 | 25,8 | 2,0 | 23,8 | 2 023 | 80 | 80 | 1 943 | 1 920 | pleno |
| **soma** | | | | **6 732** | | **488** | **4 324** | 1 920 | |

<!-- tabela: **Tabela 11** — Verificação do fecho do balanço de massa nos dez dias -->
| Verificação do fecho | Litros |
| :--- | ---: |
| captado no período | 6 732 |
| menos o extravasado | −4 324 |
| menos o consumido | −488 |
| menos o que ficou no reservatório | −1 920 |
| **resíduo** | **0** |

<!-- tabela: **Tabela 12** — Indicadores do caso resolvido de dez dias -->
| Indicador dos dez dias | Valor |
| :--- | ---: |
| potencial de poupança de água potável | 24,4% |
| média diária de água pluvial consumida | 48,9 L/dia |
| média diária de água da rede consumida | 151,2 L/dia |
| média diária extravasada | 432,4 L/dia |
| dias de abastecimento pleno | 60% |
| dias de abastecimento parcial | 10% |
| dias de abastecimento nulo | 30% |

---

### 2.1.3. Ler a tabela

Cinco coisas acontecem nestes dez dias, e cada uma ensina uma regra do programa.

#### 2.1.3.1. O dia 1: reservatório vazio

A simulação começa com o reservatório **vazio**. No dia 1 não chove, não há nada armazenado, e a
procura pluvial de 80 L não é satisfeita por uma gota: o dia é de abastecimento **nulo**, e os
200 L do dia inteiro vêm da rede.

Isto não é um defeito da série escolhida. É a condição inicial do modelo, e conta: em séries
curtas, os primeiros dias penalizam o resultado. Com trinta anos de série o efeito desaparece;
com dez dias, é uma das razões por que o potencial obtido, 24,4%, fica tão abaixo da fração
suprível de 40%. Os dias 3 e 4 juntam mais dois dias de abastecimento nulo, e são 30% dos dez.

#### 2.1.3.2. Os dias 2 e 4: o descarte em ação

No dia 2 choveu 2,1 mm. Depois do descarte de 2,0 mm, ficam 0,1 mm, que sobre 100 m² com o
coeficiente de 0,85 dão 9 L. Os 9 L são consumidos, e o dia é de abastecimento **parcial**: 9 L
dos 80 L pretendidos.

No dia 4 choveu 1,2 mm, menos do que a lâmina de descarte de 2,0 mm. O programa não subtrai 1,2 e
capta zero: **descarta o dia inteiro**. O mesmo se passa no dia 7, com 0,7 mm, e a diferença é que
nesse dia o reservatório tem água de reserva e o abastecimento é pleno à mesma.

> **Atenção.** Quando a regra de descarte se aplica e a chuva do dia não excede a lâmina, perde-se
> o dia **inteiro**, e não a diferença. A conta é `P_ef = P − d_f` quando `P > d_f`, e **zero**
> no caso contrário.

A razão é física: o dispositivo de descarte tem de encher antes de a água chegar à cisterna. Se a
chuva não enche o dispositivo, nada passa. Em climas de chuva fraca e frequente, isto pesa muito
mais do que a intuição sugere, e é por isso que o modo de descarte merece atenção na secção
4.1. Na série de Lisboa do tutorial, chove em 22% dos dias, e 4% dos dias ficam abaixo da lâmina de
descarte.

> **Uma nota para quem compara ferramentas.** Algumas ferramentas de simulação tratam `d_f` como
> **limiar do evento**: abaixo dele nada é captado, acima dele capta-se a chuva **inteira**, sem
> subtração. O Triton subtrai a lâmina. A diferença é deliberada, baixa a poupança estimada, e os
> estudos que comparem as duas regras têm de a declarar. A secção 6.1 trata da comparação.

#### 2.1.3.3. O dia 9: o extravasamento vem antes do consumo

Choveu 35,7 mm. Descontados os 2,0 mm de descarte, restam 33,7 mm efetivos, que sobre 100 m² com
o coeficiente de 0,85 dão 2 865 L captados.

O reservatório tinha 1 516 L e comporta 2 000 L, pelo que **extravasam 2 380 L**, mais do que o
reservatório inteiro comporta. Só depois disso o programa retira os 80 L da procura, deixando
1 920 L para o dia seguinte.

> **Atenção.** Esta ordem define o modelo. O extravasamento é calculado **antes** da retirada da
> procura, como na regra **YAS** (*yield after spillage*), mas a chuva do próprio dia já pode
> satisfazer a procura do dia, como na regra **YBS**. O Triton fica, por isso, entre as duas, e a
> subsecção «YAS, YBS e a ordem do Triton», adiante, mostra porquê.
>
> Se o consumo viesse antes do extravasamento, o reservatório aceitaria água que fisicamente já
> teria extravasado, e o programa sobrestimaria o aproveitamento. A diferença aparece justamente
> nos dias de chuva forte, que são os que mais pesam no total anual.

Num único dia, o sistema deitou fora o equivalente a quase trinta dias de procura pluvial. É o
retrato do desencontro entre a chuva, que chega concentrada, e a procura, que é constante.

#### 2.1.3.4. O dia 10: o reservatório já está cheio

Choveu 25,8 mm, e o sistema captou 2 023 L. O reservatório começava o dia com 1 920 L, de modo que
**extravasam 1 943 L**: quase tudo o que foi captado. Entre os dias 9 e 10, o reservatório
terminou ambos os dias com os mesmos 1 920 L, e perdeu 4 324 L em dois dias, mais de cinquenta
dias de procura pluvial. Aumentar o reservatório recupera parte disto, e é exatamente esta a
pergunta a que a varredura de volumes da secção 2.2 responde. A Figura 9
resume os dez dias.

![Volumes captado e extravasado e volume armazenado ao longo dos dez dias](../figuras/fig01_dez_dias.png)

*Figura 9 — Os dez dias do caso resolvido, com a chuva de Lisboa de 11 a 20 de dezembro de 2019: (a) volume captado, a azul, e volume extravasado, a laranja, por dia; nos dias 9 e 10 o extravasamento é quase igual ao captado; (b) volume armazenado no reservatório inferior no fim de cada dia, depois do consumo, com a capacidade de 2 000 L a tracejado; nos dias 9 e 10 o reservatório atinge a capacidade, extravasa e termina o dia com 1 920 L.*

#### 2.1.3.5. A soma: o balanço fecha

A última linha da tabela e o quadro de verificação mostram o fecho:

```equacao:fechamento:1
V_cap = V_ext + V_con + V_res
```

<!-- tabela: **Tabela 13** — Variáveis da Equação 1 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_cap` | volume total captado no período | L |
| `V_ext` | volume total extravasado no período | L |
| `V_con` | volume total de água da chuva consumido no período | L |
| `V_res` | volume remanescente no reservatório no fim do período | L |

Nos dez dias do caso resolvido, a Equação 1 verifica-se com 6 732 L captados,
4 324 L extravasados, 488 L consumidos e 1 920 L remanescentes.

Resíduo zero. O programa não cria nem perde água, e esta verificação é feita automaticamente pela
bateria de testes a cada alteração do código, sobre séries de dez anos, com um resíduo da ordem
de 10⁻¹⁴ por cento do captado.

---

### 2.1.4. As equações

O balanço diário escreve-se em cinco equações encadeadas, que o programa resolve por esta ordem
para cada dia da série. A notação segue a da secção 4.1 para a parte da captação, e o índice
`t` designa sempre o dia corrente da simulação, de modo que `t−1` é o dia imediatamente anterior.

#### 2.1.4.1. O volume captado

A conversão da lâmina precipitada em volume é a primeira operação do dia, e a mais simples de
todas: multiplica-se a chuva efetiva pela área de captação e pelo coeficiente de escoamento
superficial.

```equacao:volume_captado:2
V_cap,t = P_ef,t × A × C
```

<!-- tabela: **Tabela 14** — Variáveis da Equação 2 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_cap,t` | volume captado no dia `t` | L |
| `P_ef,t` | chuva efetiva no dia `t`, já descontada a lâmina de descarte | mm |
| `A` | área de captação, em projeção horizontal | m² |
| `C` | coeficiente de escoamento superficial da cobertura | adimensional |

O resultado da Equação 2 sai diretamente em litros, sem fator de conversão,
porque um milímetro de lâmina sobre um metro quadrado de superfície corresponde exatamente a um
litro de água. É a única simplificação dimensional do modelo, e é exata.

#### 2.1.4.2. O extravasamento e o armazenamento

O volume disponível antes de qualquer consumo é a soma do que sobrou no reservatório no fim do
dia anterior com o que foi captado hoje, como na Equação 3. Desta soma decorrem
duas parcelas, calculadas por esta ordem: o excedente que não cabe no reservatório e por isso
extravasa, e o volume que fica efetivamente armazenado.

```equacao:disponivel:3
D_t = V_res,t−1 + V_cap,t
```

```equacao:extravasado:4
V_ext,t = max(0 ; D_t − V_max)
```

```equacao:armazenado:5
V_arm,t = min(D_t ; V_max)
```

<!-- tabela: **Tabela 15** — Variáveis da Equação 5 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `D_t` | volume disponível no dia `t`, antes do consumo | L |
| `V_res,t−1` | volume que sobrou no reservatório no fim do dia anterior | L |
| `V_cap,t` | volume captado no dia `t`, da Equação 2 | L |
| `V_ext,t` | volume extravasado no dia `t` | L |
| `V_arm,t` | volume armazenado no dia `t`, antes do consumo | L |
| `V_max` | capacidade útil do reservatório inferior | L |

==A ordem em que as Equações 4 e 5 aparecem define o modelo.== O
extravasamento é calculado **antes** da retirada do consumo do dia, e é por isso que o programa
costuma ser descrito pela regra YAS, do inglês *yield after spillage*, isto é, rendimento
posterior ao extravasamento. A descrição é aproximada, e a subsecção seguinte diz em que falha.
Inverter a ordem faria o reservatório aceitar, sob a forma de consumo, água que fisicamente já
teria extravasado, e sobrestimaria o aproveitamento justamente nos dias de chuva intensa, que são
os que mais pesam no total anual.

A diferença entre as duas ordens é invisível na maior parte dos dias e decisiva nos poucos que
importam. Enquanto o reservatório não enche, extravasar antes ou depois de consumir dá exatamente
o mesmo resultado, porque não há extravasamento algum; nos dias de chuva intensa, em que o
reservatório atinge a capacidade, a ordem determina se uma parcela de água é contabilizada como
consumida ou como perdida. São justamente estes os dias que mais pesam no total anual, e por isso
uma escolha que parece formalidade desloca o resultado inteiro. A Figura 10 compara as
duas sequências na notação das equações desta secção.

![A mesma chuva, duas ordens de cálculo](../figuras/fig00f_yas.png)

*Figura 10 — Sequência de operações do balanço diário: (a) a ordem adotada pelo programa, com o extravasamento calculado antes do consumo; (b) a ordem invertida (YBS), com o consumo retirado antes do extravasamento. As duas sequências só divergem nos dias em que o reservatório atinge a capacidade, e a YBS supõe um consumo anterior à chuva do dia, o que sobrestima o aproveitamento.*

#### 2.1.4.3. YAS, YBS e a ordem do Triton

Na literatura, a YAS e a YBS têm definição precisa (Fewkes e Butler, 2000). Com `Y_t` o volume
retirado no dia, `Q_t` o volume captado, `S_t` o volume armazenado no fim do dia e `V_max` a
capacidade:

<!-- tabela: **Tabela 16** — Retirada do dia e volume armazenado no fim do dia nas regras YAS e YBS estritas e no Triton -->
| Regra | Retirada do dia | Armazenado no fim do dia |
| :--- | :--- | :--- |
| YAS estrita | `Y_t = min(D_pl,t ; S_t−1)` | `S_t = min(S_t−1 + Q_t − Y_t ; V_max − Y_t)` |
| YBS estrita | `Y_t = min(D_pl,t ; S_t−1 + Q_t)` | `S_t = min(S_t−1 + Q_t − Y_t ; V_max)` |
| Triton | `Y_t = min(D_pl,t ; min(S_t−1 + Q_t ; V_max))` | `S_t = min(S_t−1 + Q_t ; V_max) − Y_t` |

Na YAS estrita, a retirada do dia sai só do que estava guardado na véspera: a chuva de hoje só
serve amanhã. Na YBS estrita, a chuva de hoje satisfaz a procura antes de o reservatório
extravasar. O Triton faz primeiro o extravasamento, como a YAS, e depois deixa a chuva do dia,
até ao limite da capacidade, satisfazer a procura do dia.

Daqui decorre uma desigualdade que vale para qualquer série: o volume consumido pelo Triton nunca
é menor do que o da YAS estrita nem maior do que o da YBS estrita. O resultado fica **entre as
duas**, mais perto da YAS nos reservatórios grandes, em que a véspera quase sempre basta, e mais
longe dela nos pequenos, em que a chuva do dia pesa. Quem compara o Triton com um programa ou com
uma norma que use a YAS estrita deve esperar do Triton um potencial de poupança ligeiramente
maior para o mesmo volume.

O programa mantém esta ordem por decisão: garante a continuidade com os estudos anteriores do
grupo de investigação, e uma mudança aqui deslocaria todos os resultados publicados.

#### 2.1.4.4. A satisfação da procura

Estabelecido quanto há no reservatório, o programa retira dele o menor valor entre a procura
pluvial do dia e o volume disponível, e devolve ao dia seguinte o que restar.

```equacao:consumido:6
V_con,t = min(D_pl,t ; V_arm,t)
```

```equacao:sobra:7
V_res,t = V_arm,t − V_con,t
```

<!-- tabela: **Tabela 17** — Variáveis da Equação 7 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_con,t` | volume de água da chuva consumido no dia `t` | L |
| `D_pl,t` | procura pluvial do dia `t`, montada como na secção 4.2 | L |
| `V_arm,t` | volume armazenado no dia `t`, da Equação 5 | L |
| `V_res,t` | volume remanescente, transferido para o dia seguinte | L |

A Equação 7 é o que torna a simulação diária necessária e insubstituível: liga cada
dia ao seguinte e faz do reservatório uma memória do que aconteceu antes. Nenhum cálculo baseado
em médias mensais ou anuais consegue representar este encadeamento, e é dele que decorre todo o
desencontro entre a oferta concentrada e a procura distribuída.

#### 2.1.4.5. O complemento da rede pública

O que a chuva não satisfez é comprado à entidade gestora, e esta parcela reúne três origens
distintas.

```equacao:potavel:8
V_pot,t = D_pot,t + ΔD_int,t + ΔD_irr,t
```

<!-- tabela: **Tabela 18** — Variáveis da Equação 8 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_pot,t` | volume de água potável consumido da rede no dia `t` | L |
| `D_pot,t` | procura que exige água potável pela natureza do uso | L |
| `ΔD_int,t` | défice do uso interior não potável, não satisfeito pela chuva | L |
| `ΔD_irr,t` | défice da rega, **somente** se o abastecimento de reserva estiver ligado | L |

A terceira parcela da Equação 8 merece atenção porque depende de uma escolha do
utilizador. Com o abastecimento de reserva ligado, a rede socorre a rega nos dias em que a
cisterna seca, e o défice é suprido com água potável; com ele desligado, o jardim simplesmente
não é regado, o edifício não compra essa água, e o volume correspondente é contabilizado como
**procura não satisfeita**, que é a terceira parcela do balanço da procura tratada adiante nesta
secção.

#### 2.1.4.6. A classificação do dia

Por fim, cada dia recebe uma classificação segundo o grau de abastecimento alcançado, e é a partir
dessa classificação que se calculam as percentagens de dias de abastecimento pleno, parcial e
nulo relatadas na secção 2.3.

```equacao:classificacao:9
pleno: V_con,t = D_pl,t ; parcial: 0 < V_con,t < D_pl,t ; nulo: V_con,t = 0
```

<!-- tabela: **Tabela 19** — Variáveis da Equação 9 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_con,t` | volume de água da chuva consumido no dia `t` | L |
| `D_pl,t` | procura pluvial do dia `t` | L |

A comparação da Equação 9 é feita com tolerância de 10⁻⁵ L, e não por igualdade
exata. A razão é aritmética e não conceptual: o balanço trabalha com números de vírgula
flutuante, e uma diferença da ordem do erro de arredondamento classificaria como parcial um dia
que foi plenamente abastecido.

### 2.1.5. O balanço da procura tem três parcelas

A procura total de um dia reparte-se em três, e não em duas:

```equacao:demanda_tres:10
D_t = V_con,t + V_pot,t + V_nao,t
```

<!-- tabela: **Tabela 20** — Variáveis da Equação 10 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `D_t` | procura total do edifício no dia `t` | L |
| `V_con,t` | parcela satisfeita com água da chuva | L |
| `V_pot,t` | parcela comprada à rede pública | L |
| `V_nao,t` | parcela que ninguém forneceu, isto é, procura não satisfeita | L |

As três parcelas são o consumo de água da chuva, o consumo da rede pública e a **procura não
satisfeita**. A terceira é zero na configuração de partida, em que a rede socorre a rega nos
dias secos. Deixa de ser zero quando o utilizador desliga esse socorro, e então o programa tem de
a mostrar: sem ela, o balanço fecharia por construção, escondendo a água que ninguém forneceu.

---

### 2.1.6. Com reservatório superior

Quando o projeto tem reservatório superior, o passo 4 muda. Em vez de consumir diretamente do
reservatório inferior, o programa:

1. consome do reservatório superior o que estiver **acima do limiar de acionamento**;
2. se ainda falta e há água em baixo, **aciona a eletrobomba**: transfere o menor valor entre o
   que há no inferior e o espaço livre em cima, e conta **um ciclo**;
3. consome de novo do que acabou de chegar;
4. repete até satisfazer a procura ou acabar a água.

O limiar de acionamento é o volume de reserva que não se consome, e serve para a bomba não ligar a
cada litro. Está limitado ao volume do reservatório superior: informar um limiar maior do que o
reservatório não faz o programa recusá-lo, faz com que adote o reservatório cheio.

> **O reservatório superior não aumenta a poupança de água.** Muda **quando** a água é entregue,
> não **quanta**. O que acrescenta é custo: o investimento no reservatório e na bomba, a energia da
> elevação e a emissão associada. A secção 4.5 mostra-o com números.

O número de ciclos e o volume elevado saem daqui e alimentam o cálculo de energia da secção
2.6.

---

### 2.1.7. O que o modelo não representa

- **Não há subpasso horário.** Uma chuva de 40 mm concentrada em duas horas e a mesma lâmina
  repartida por vinte e quatro horas produzem o mesmo resultado. Para reservatórios muito
  pequenos em relação à área de captação, isto subestima o extravasamento.
- **Não há perda por evaporação ou fuga** no reservatório.
- **A condição inicial é reservatório vazio.** Em séries com menos de um ano, isto penaliza
  sensivelmente o resultado.
- **O coeficiente de escoamento é único e constante.** Não varia com a intensidade da chuva nem
  com o tempo desde o último evento.
- **No balanço, o descarte é uma lâmina, e não um dispositivo com dinâmica própria.** O
  reservatório de descarte é dimensionado e orçamentado pelo volume `A × d_f` (secção 2.5),
  mas o seu esvaziamento entre eventos não é simulado: a lâmina é aplicada conforme o modo de
  descarte escolhido.

A secção 5.2 reúne estas e as restantes limitações conhecidas.

---

### 2.1.8. Para conferir

O caso resolvido desta secção está no ficheiro `05_dez_dias.triton`, na pasta de casos que
acompanha o programa. Abra-o, execute-o e compare com a tabela impressa.

Se algum número divergir, é o manual que está desatualizado em relação ao programa. E nesse caso a
verificação automática já terá avisado, porque cada número desta tabela tem uma asserção
correspondente na bateria de testes descrita na secção 5.3.

---

## 2.2. Volume ideal e a varredura

> Esta secção formaliza o que a secção 4.4 fez na prática: como o programa constrói a grelha
> de volumes e como aplica o critério de volume ideal.

---

### 2.2.1. A grelha discreta

A varredura simula um conjunto **finito** de volumes, e a construção desse conjunto obedece a
três regras.

**O passo é arredondado por excesso ao múltiplo de 250 litros.** É o quantum comercial: os
reservatórios vendem-se em volumes normalizados, e um ótimo de 1 300 L não se compra. Quando o
passo pedido não é múltiplo de 250, o programa ajusta-o e regista o ajuste em `step_adjusted`,
para que o relatório possa declarar o passo efetivo.

**O número de volumes positivos está limitado a 40.** Uma varredura de 0 a 50 000 L com passo de
100 L seriam 500 simulações de trinta anos, e o ganho de informação não paga o custo. Quando o
limite é atingido, o passo efetivo cresce.

**O volume máximo informado é sempre preservado** como último ponto da grelha. Só o último
intervalo pode, portanto, ser menor do que o passo efetivo.

O volume **zero** entra na grelha como alternativa de referência: é o cenário sem sistema, contra
o qual os restantes se comparam.

---

A consequência prática aparece na Figura 11. Com um passo fino, a curva mostra o
joelho onde o retorno começa a decair; com um passo grosseiro, o joelho cai entre dois pontos da
grelha e o critério elege o primeiro volume tabelado depois dele, que pode estar vários metros
cúbicos além do volume que de facto interessa.

![A mesma curva vista por duas grelhas de varredura](../figuras/fig14_grade.png)

*Figura 11 — Curva de potencial de poupança do mesmo edifício, varrida com passo de 250 L e com passo de 5 000 L. A grelha grossa calcula corretamente cada ponto que contém, mas não contém o troço de maior curvatura, entre 1 e 5 m³.*

---

### 2.2.2. O ganho marginal

A curva de potencial de poupança contra o volume é monótona e côncava: cada metro cúbico
acrescentado ao reservatório rende menos do que o anterior, e o rendimento tende para zero à
medida que o sistema se aproxima do teto imposto pela fração suprível. O programa quantifica este
rendimento decrescente pela derivada discreta da curva, calculada para cada volume da grelha a
partir do segundo.

```equacao:ganho_marginal:11
Δ(V_i) = [ Epot(V_i) − Epot(V_i−1) ] ÷ [ (V_i − V_i−1) ÷ 1000 ]
```

<!-- tabela: **Tabela 21** — Variáveis da Equação 11 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Δ(V_i)` | ganho marginal do volume `V_i` em relação ao anterior | %/m³ |
| `Epot(V_i)` | potencial de poupança de água potável obtido com o volume `V_i` | % |
| `Epot(V_i−1)` | potencial de poupança obtido com o volume imediatamente menor | % |
| `V_i` | volume do reservatório na posição `i` da grelha | L |
| `V_i−1` | volume imediatamente menor da grelha | L |
| `1000` | conversão de litros para metros cúbicos | L/m³ |

A divisão por mil no denominador da Equação 11 existe para que o resultado saia
em pontos percentuais por metro cúbico acrescentado, que é a unidade em que a decisão se toma:
os reservatórios compram-se e orçamentam-se em metros cúbicos, não em litros.

==Por ser uma derivada discreta, o ganho marginal depende do passo da grelha.== Uma grelha fina
produz um valor mais local, próximo da derivada verdadeira nesse ponto; uma grelha grossa produz
a média do rendimento ao longo de um intervalo maior. A subsecção sobre a sensibilidade ao passo,
adiante, mede o tamanho deste efeito.

---

### 2.2.3. O critério de volume ideal

O volume ideal define-se como o menor volume positivo da grelha cujo ganho marginal já caiu abaixo
de um limiar declarado pelo utilizador.

```equacao:volume_ideal:12
V_ideal = min { V_i > 0 : Δ(V_i) ≤ Δ_lim }
```

<!-- tabela: **Tabela 22** — Variáveis da Equação 12 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_ideal` | volume ideal pelo critério do ganho marginal | L |
| `V_i` | volume do reservatório na posição `i` da grelha | L |
| `Δ(V_i)` | ganho marginal do volume `V_i`, da Equação 11 | %/m³ |
| `Δ_lim` | limiar de ganho marginal declarado pelo utilizador; o programa abre com 5,0, e o tutorial adota 1,0 | %/m³ |

Quando nenhum volume da grelha satisfaz a condição da Equação 12, o que acontece
quando a gama varrida termina antes de a curva achatar, o programa adota o maior volume da grelha
e regista essa circunstância no relatório, para que o leitor saiba que o ótimo encontrado é um
limite da busca e não um ponto de inflexão da curva.

#### 2.2.3.1. Um exemplo, passo a passo

A tabela da varredura do tutorial, na secção 4.4, permite refazer a conta à mão. Entre
3 000 L e 4 000 L o potencial sobe de 15,39% para 16,60%, isto é, 1,21 pontos percentuais por
mais um metro cúbico. Como 1,21 é maior do que o limiar de 1,0 %/m³, o volume não é ainda o ideal.
Entre 4 000 L e 5 000 L o potencial sobe de 16,60% para 17,49%, isto é, 0,89 pontos por metro
cúbico, já abaixo do limiar: o primeiro volume a cruzá-lo é 5 000 L, e é ele o volume ideal. Com o
limiar mais folgado de 3 %/m³, o volume ideal seria 3 000 L (15,39%), e com o mais exigente de
0,5 %/m³ seria 10 000 L (20,37%).

Repare no que se passa logo a seguir. Entre 6 000 L e 8 000 L o potencial sobe 1,20 pontos, mais
do que os 0,70 do intervalo anterior, de 5 000 para 6 000 L, e no entanto o ganho **por metro
cúbico** desce, de 0,70 para 0,60 %/m³, porque o intervalo tem dois metros cúbicos. É por isso que
o critério usa o ganho por metro cúbico, e não o ganho entre pontos consecutivos da grelha: o
segundo depende do passo, e o primeiro muito menos.

Em Lisboa, a escolha do limiar pesa mais do que noutros climas. A curva não satura: sobe ainda
de 20,37% a 10 000 L para 24,01% a 20 000 L, por causa do verão seco, e o ganho marginal desce
devagar, de 1,84 %/m³ aos 3 000 L para 0,32 %/m³ aos 20 000 L. O volume ideal sai do limiar
declarado, e não de um patamar da curva: declare o limiar junto do volume.

> **O critério é hidráulico e só hidráulico.** Ignora custo, tarifário e carbono. Um volume ideal
> por este critério não é uma recomendação de projeto; é o ponto em que a curva de aproveitamento
> deixa de compensar **em água**. A secção 2.10 trata da escolha com os restantes critérios,
> que muitas vezes apontam para volumes diferentes.

---

Este é um critério entre outros igualmente defensáveis, e convém dizê-lo com clareza. Um
projetista que queira o máximo desempenho hídrico escolherá o maior volume da varredura; um que
responda por um orçamento escolherá o volume de maior valor atual líquido; o critério do ganho
marginal fica entre os dois, por ser o que identifica onde a curva deixa de compensar. Os três
leem a mesma varredura e não têm de coincidir: neste projeto apontam volumes muito diferentes, de
1 000 L pelo critério financeiro a 12 000 L pelo técnico, com 5 000 L pelo ganho marginal.
Nenhum dos três está errado; errado é não dizer qual deles se usou. A Figura 12
marca o volume eleito por cada critério, com o valor anotado na legenda do gráfico.

![A mesma varredura lida por três critérios](../figuras/fig09_criterios.png)

*Figura 12 — Varredura do projeto do tutorial lida por três critérios: (a) potencial de poupança e (b) valor atual líquido do mesmo conjunto de volumes. As linhas verticais marcam o volume eleito pelo ganho marginal abaixo de 1 %/m³, pelo VAL máximo e pelo potencial máximo; o volume de cada um vai anotado na legenda, porque depende da grelha varrida e dos pressupostos económicos em vigor.*

---

### 2.2.4. Por que o programa simula: os métodos empíricos

Normas e manuais oferecem há muito um conjunto de métodos para dimensionar o reservatório: o de
Rippl, a simulação e várias regras práticas, como a alemã e a britânica. Continuam em uso corrente
em projetos e em trabalhos académicos, e convém perceber o que cada um responde antes de os
comparar com a varredura do programa. Algumas normas trazem ainda um método simplificado do mesmo
género, um número de dias do menor valor entre a produção anual e a procura, a par da simulação
diária detalhada.

**O método de Rippl** é o diagrama de massas aplicado ao reservatório: acumula, período a período,
a diferença entre a procura e a chuva aproveitável, e adota como volume o maior défice acumulado
da série. O volume resultante é o que satisfaria **toda** a procura mesmo na pior estiagem
registada, e por isso cresce com o comprimento da série e com a sua resolução: com dados diários,
as sequências secas aparecem inteiras; com dados mensais, parte delas dilui-se na média do mês.

**Os métodos práticos** são regras de bolso. O alemão toma 6% do menor valor entre a chuva
aproveitável anual e a procura anual; o britânico toma 5% do produto `P × A`, com `P` a
precipitação média anual e `A` a área de captação. Nenhum dos dois usa a distribuição da chuva no
tempo, e o britânico nem sequer usa a procura.

A tabela seguinte aplica cinco abordagens de dimensionamento ao projeto do tutorial de Lisboa,
arredonda cada volume a um múltiplo de 250 L e simula, no próprio programa, o potencial que cada
uma produz.

<!-- tabela: **Tabela 23** — Volumes dados por regras clássicas de dimensionamento para o projeto do tutorial, arredondados a 250 L, e o potencial que cada um produz na simulação diária -->
| Método | Regra | Volume | Potencial simulado |
| :--- | :--- | ---: | ---: |
| regra prática alemã | 6% do menor entre a oferta e a procura anuais | 3 750 L | 16,32% |
| Rippl, série mensal | maior défice acumulado, meses | 47 000 L | 26,78% |
| Rippl, série diária | maior défice acumulado, dias | 51 500 L | 26,92% |
| regra prática britânica | 0,05 × P × A | 5 500 L | 17,85% |
| **simulação diária, ganho marginal de 1 %/m³** | varredura | **5 000 L** | **17,49%** |

<!-- tabela: **Tabela 24** — Fração de armazenamento dos volumes da varredura e o passo de simulação que Fewkes e Butler (2000) recomendam para cada gama -->
| Volume | Fração de armazenamento S/(A·R) | Passo de tempo recomendado por Fewkes e Butler |
| ---: | ---: | :--- |
| 1 000 L | 0,0093 | horário |
| 2 000 L | 0,0185 | diário |
| 3 000 L | 0,0278 | diário |
| 4 000 L | 0,0371 | diário |
| 8 000 L | 0,0741 | diário |
| 12 000 L | 0,1112 | diário |
| 20 000 L | 0,1854 | mensal |

A primeira tabela mostra o que a curva côncava da secção 4.4 já anunciava, com uma diferença
de peso: em Lisboa, o verão seco faz do método de Rippl um pedido enorme. Com série diária, pede
51 500 L, e com série mensal, 47 000 L: perto de dez vezes os 5 000 L da simulação. Esses
reservatórios entregam de facto mais, 26,92% e 26,78% contra 17,49%, e chegam perto do teto de
28%, porque são dimensionados para que quase nunca falte água. Mas cada metro cúbico acima de
5 000 L rende pouco, e uma cisterna de 47 a 52 m³ é impraticável numa moradia como a do tutorial. As regras práticas ficam do outro lado: a alemã (3 750 L, 16,32%) dá menos do que a
simulação, e a britânica (5 500 L, 17,85%) acerta a ordem de grandeza por coincidência, porque
nenhuma das duas tem como saber que a chuva de Lisboa se concentra no inverno, e dariam o mesmo
volume a uma cidade de chuva bem repartida.

==A diferença essencial é que os métodos empíricos respondem a uma pergunta fixa, e a simulação
responde à pergunta que o projetista declara.== Rippl pergunta que volume nunca falha; o método
britânico pergunta que fração da chuva guardar; a varredura com ganho marginal pergunta a partir
de que volume o metro cúbico seguinte deixa de compensar. O volume adequado varia com a chuva
local, a área de cobertura, o número de moradores e as procuras, e dimensionar reservatórios pela
tradição local, sem simulação, pode levar a sistemas de baixa eficiência. Nas três cidades de
exemplo, a varredura dá volumes ideais diferentes, 5 000 L em Lisboa e no Porto e 4 000 L no
Funchal, com a mesma moradia e o mesmo limiar: a diferença vem só da chuva.

---

### 2.2.5. O passo de tempo e a fração de armazenamento

O programa simula dia a dia, e esta escolha tem uma gama de validade conhecida. Fewkes e Butler
(2000) compararam modelos comportamentais com passos de um minuto, uma hora, um dia e um mês,
tomaram como referência o modelo horário com a regra YAS, descrita na secção 2.1, e
mostraram que o passo adequado depende de uma grandeza adimensional, a **fração de
armazenamento**.

```equacao:fracao_de_armazenamento:13
F_S = S ÷ (A × R)
```

<!-- tabela: **Tabela 25** — Variáveis da Equação 13 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `F_S` | fração de armazenamento | adimensional |
| `S` | capacidade do reservatório | m³ |
| `A` | área de captação em projeção horizontal | m² |
| `R` | precipitação média anual | m |

Pelos resultados daqueles autores, o modelo horário é o indicado para frações até 0,01; o diário,
para frações entre 0,01 e 0,125; e o mensal, só acima de 0,125. A razão física é simples: quanto
menor o reservatório relativamente à chuva que recebe, mais enche e extravasa **dentro** de um
mesmo dia chuvoso, enquanto a procura é retirada ao longo das horas; um passo diário soma numa só
entrada o que, hora a hora, teria entrado e saído aos poucos.

A segunda tabela calcula a fração para os volumes da varredura do tutorial. A cisterna escolhida,
de 5 000 L, tem uma fração de cerca de 0,046, dentro da gama do modelo diário; o reservatório de
1 000 L (0,0093) fica abaixo de 0,01, e para ele o resultado diário deve ler-se como uma
aproximação. Fewkes e Butler recomendam o passo horário para esse volume e o diário para os
outros. Campisano e Modica (2015), que simularam um sistema residencial com passos diários e
subdiários a partir de caudais medidos, chegaram a uma conclusão complementar: o passo diário é
fiável para estimar a **poupança de água**, mas são precisos passos de, no máximo, uma hora quando
o objetivo é a **retenção de águas pluviais**, sobretudo em reservatórios pequenos e com procura
alta.

> **Na prática.** Para a poupança de água potável em edifícios, o passo diário do programa é
> adequado na gama habitual de projeto. Se a fração de armazenamento do seu estudo ficar abaixo de
> 0,01, declare a limitação; e se o objetivo for amortecer caudais de ponta na drenagem urbana, o
> programa não é a ferramenta adequada.

---

### 2.2.6. O que a literatura diz sobre o volume ideal

Não há uma definição única de volume ideal, e a revisão sistemática de Semaan et al. (2020) ajuda
a situar o critério do programa. Examinando estudos de otimização de sistemas domésticos, os
autores observaram que o dimensionamento do reservatório é o objetivo de otimização mais
importante, mas que o custo é o critério mais usado; que o subdimensionamento produz sistemas
incapazes de fornecer um volume fiável; e que o sobredimensionamento eleva o investimento com um
benefício marginal pequeno e pode até comprometer a qualidade da água, que fica armazenada por
mais tempo.

Campisano et al. (2017), numa revisão ampla sobre sistemas urbanos de aproveitamento pluvial,
reúnem critérios de três famílias: os de **eficiência hídrica**, como o potencial de poupança e a
fiabilidade; os **económicos**, como o valor atual líquido e o período de recuperação; e os de
**desempenho na drenagem**, como a retenção. O programa cobre as duas primeiras famílias e declara
não cobrir a terceira.

O critério do ganho marginal pertence à primeira família e tem uma vantagem sobre a fiabilidade
fixa, como a de Rippl: não exige que o projetista escolha um nível de falha aceitável, que
raramente tem justificação técnica, mas sim um nível de retorno decrescente, que se lê
diretamente em metros cúbicos de reservatório. A desvantagem é simétrica: o limiar de 1 %/m³, ou
de 5 %/m³, também é uma escolha, e tem de ser declarado.

---

### 2.2.7. A sensibilidade ao passo

O volume ideal depende do passo da varredura, e convém saber quanto.

Um passo grosso salta o joelho da curva: com um passo de 5 000 L, o primeiro ponto avaliado depois
do zero já tem o ganho marginal médio de todo o intervalo, que é alto, e o segundo pode já estar
abaixo do limiar. O ideal sai deslocado para cima.

Um passo fino resolve melhor o joelho, ao custo de tempo.

**Recomendação prática:** passo entre 500 e 1 000 L para reservatórios residenciais, e entre
2 000 e 5 000 L para edifícios de grande porte, declarando sempre o passo adotado junto do volume
ideal.

---

### 2.2.8. Por que a curva tem esta forma

A curva de aproveitamento pluvial é côncava e assintótica, sempre. Duas razões:

**Os eventos pequenos são a maioria.** Os primeiros litros de armazenamento captam as chuvas
frequentes e pequenas, que respondem pela maior parte dos dias. Os últimos litros só servem para
os poucos eventos extremos.

**A fração suprível é um teto.** O potencial não pode ultrapassar a fração da procura que a chuva
satisfaz, definida na secção 4.2. A curva aproxima-se desse teto e nunca o cruza, invariante
que a bateria de testes verifica até volumes de 100 m³. Em Lisboa, o teto é de 28% e a curva
chega a 24,01% aos 20 000 L: ainda longe dele.

---

### 2.2.9. A série é suficientemente longa?

Todo o resultado desta secção depende da série de chuva carregada, e a pergunta que o revisor faz
primeiro é se ela basta. Geraldi e Ghisi responderam-lhe em três artigos: extraem-se subséries de
uma série longa, simula-se cada uma e conta-se com que frequência reproduzem o resultado da série
inteira. O comprimento representativo é o menor que reproduz o resultado na maior parte das
janelas, e que **continua a reproduzi-lo** nos comprimentos maiores: um acerto isolado numa
subsérie curta não vale como recomendação.

O programa tem esta análise na etapa da varredura, no botão «a série de chuva é suficientemente
longa?». Usa a mesma grelha de volumes e o mesmo limiar de ganho marginal da varredura, porque a
resposta depende deles, e devolve o veredicto numa frase, com a tabela de frequência por
comprimento.

==A resposta é deste projeto, e não da cidade.== É o ponto que os artigos não isolam e que a
análise torna visível: o comprimento de série necessário depende de quanto da procura se pede à
chuva. Quanto maior a parte a cobrir, mais a cisterna depende das estiagens raras, e mais longa
tem de ser a série que as contém. Uma série curta não erra o potencial médio; erra o volume, que é
o que se compra.

O programa devolve o veredicto para o seu projeto, com a sua cobertura, a sua procura e a sua
fração suprível. Execute-o para cada cidade de uma comparação: as três cidades de exemplo, com
trinta anos de dados diários cada uma, são um bom teste. [A COMPLETAR: o comprimento de série
representativo para Lisboa, Porto e Funchal ainda não foi calculado para esta edição; correr a
análise nos três projetos de exemplo e tabelar aqui.]

> **Atenção: uma série curta não se torna longa por tirar médias.** Se a análise disser que o
> projeto precisa de mais anos do que a série tem, o volume ideal calculado é provisório, e é isso
> que se declara no trabalho. Repetir a simulação com outra janela dos mesmos dados não resolve: o
> que falta é registo, não processamento. Algumas normas fixam um número mínimo de anos de dados
> diários; o Triton mantém a análise de Geraldi e Ghisi, que responde para cada projeto em vez de
> fixar um mínimo.

---

### 2.2.10. O que a varredura não responde

- **Que volume comprar.** Os reservatórios existem em volumes comerciais; o ideal calculado deve
  ser arredondado para o volume disponível mais próximo, e a varredura já ajuda ao trabalhar em
  múltiplos de 250 L.
- **Se o sistema compensa.** Isso é a secção 2.7.
- **Se o volume cabe no terreno.** O programa não conhece o local.
- **Quanto a cisterna amortece a drenagem.** O passo diário não representa os caudais de ponta, e
  a retenção exige um passo horário ou menor, como mostram Campisano e Modica (2015).

---

## 2.3. Indicadores de eficiência

> Esta secção define formalmente cada indicador que o programa reporta, com a sua unidade, e diz
> **o que cada um não mede**.

Um indicador mal interpretado é pior do que nenhum, e os desta secção confundem-se com frequência
na literatura. Os dois primeiros partem do mesmo numerador, a água da chuva efetivamente
consumida, e diferem apenas no denominador: uma diferença aritmética pequena e uma diferença de
significado grande, porque cada denominador formula uma pergunta distinta. O terceiro não é uma
razão entre volumes, e sim uma contagem de dias, e responde a uma pergunta que nenhum dos outros
dois alcança: com que frequência se pode contar com o sistema (Figura 13).

![Os três indicadores e o denominador de cada um](../figuras/fig00g_indicadores.png)

*Figura 13 — Os três indicadores de eficiência e o que cada um conta. O potencial de poupança e a fiabilidade volumétrica partilham o numerador e relacionam-se pela identidade Epot = Rv × f, em que f é a fração suprível; a fiabilidade temporal conta dias, e não litros.*

---

### 2.3.1. Potencial de poupança de água potável

O potencial de poupança de água potável é o indicador central do programa e o que figura no
resumo de qualquer estudo. Exprime a fração do consumo **total** do edifício que a água da chuva
conseguiu substituir ao longo de toda a série simulada, e não apenas da parte que a chuva poderia
satisfazer.

```equacao:potencial:14
Epot = ( Σ V_con,t ÷ Σ D_t ) × 100
```

<!-- tabela: **Tabela 26** — Variáveis da Equação 14 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Epot` | potencial de poupança de água potável | % |
| `V_con,t` | volume de água da chuva consumido no dia `t` | L |
| `D_t` | procura total do edifício no dia `t` | L |
| `Σ` | somatório sobre todos os dias da série simulada | — |

O denominador da Equação 14 é a procura **total**, e esta escolha é a origem da
confusão mais comum na leitura dos resultados. Um sistema que satisfizesse integralmente toda a
procura que lhe cabe, sem falhar um único dia, ainda assim apresentaria um potencial de poupança
igual à fração suprível declarada, e não cem por cento. O teto, portanto, não é uma limitação do
sistema: é uma consequência aritmética da definição do indicador.

---

### 2.3.2. Fiabilidade volumétrica

A fiabilidade volumétrica responde a uma pergunta diferente e complementar: da água que o sistema
**devia** fornecer, quanto forneceu de facto? O denominador aqui é a procura pluvial, e não a
procura total.

```equacao:confiabilidade:15
Rv = ( Σ V_con,t ÷ Σ D_pl,t ) × 100
```

<!-- tabela: **Tabela 27** — Variáveis da Equação 15 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Rv` | fiabilidade volumétrica do sistema | % |
| `V_con,t` | volume de água da chuva consumido no dia `t` | L |
| `D_pl,t` | procura pluvial do dia `t`, isto é, a parte suprível pela chuva | L |
| `Σ` | somatório sobre todos os dias da série simulada | — |

As Equações 14 e 15 diferem apenas no denominador, e essa
diferença basta para que se relacionem por uma identidade exata, útil como conferência rápida de
qualquer resultado.

```equacao:relacao_indicadores:16
Epot = Rv × f
```

<!-- tabela: **Tabela 28** — Variáveis da Equação 16 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Epot` | potencial de poupança de água potável | % |
| `Rv` | fiabilidade volumétrica | % |
| `f` | fração da procura total suprível por água da chuva | adimensional |

==Um sistema com 55% de fiabilidade e 28% de fração suprível poupa 15,4% do consumo total, e os
três números dizem a mesma coisa de três maneiras.== É o caso da moradia de Lisboa do tutorial com
uma cisterna de 3 000 L, a primeira simulação da secção 4.3: o potencial de poupança é de
15,39%, e dividindo pela fração suprível de 0,28 obtém-se uma fiabilidade volumétrica de cerca de
55,0%. Relatar apenas um deles, sem declarar a fração suprível adotada, torna o resultado
impossível de comparar com o de outro estudo, e é a causa mais frequente de comparações indevidas
na literatura da área.

A literatura usa nomes diferentes para a mesma razão. Fewkes e Butler (2000) chamam **eficiência
de poupança de água** ao quociente entre o volume de água da chuva fornecido e a procura que o
sistema devia satisfazer, que é a fiabilidade volumétrica desta secção. Outros autores chamam
eficiência ao que aqui é potencial de poupança; algumas normas chamam-lhe taxa de cobertura. Ao
comparar com outro trabalho, confira o denominador, e não o nome.

---

### 2.3.3. Fiabilidade temporal

A fiabilidade temporal classifica cada dia da série numa de três classes mutuamente exclusivas,
conforme a relação entre o volume de água da chuva consumido e a procura pluvial do dia, definida
na Equação 9. O dia é **pleno** quando a água da chuva satisfaz integralmente a
procura pluvial; **parcial**, quando satisfaz parte dela e a rede pública fornece o resto; e
**nulo**, quando o reservatório está vazio e a rede fornece toda a procura
(Figura 14). As três percentagens somam 100%. A classificação conta dias, e não
volume: um dia em que faltou um litro para satisfazer a procura é parcial, e não quase pleno, e
por isso a fiabilidade temporal não se converte diretamente em volume poupado.

![As três classes de abastecimento de um dia](../figuras/fig29_atendimento.png)

*Figura 14 — Classes de abastecimento diário: pleno (V_con,t = D_pl,t), parcial (0 < V_con,t < D_pl,t) e nulo (V_con,t = 0). A altura preenchida representa a fração da procura pluvial do dia satisfeita por água da chuva.*

Formalmente, o dia é **pleno** quando `V_con,t = D_pl,t`, com tolerância de 10⁻⁵ L; **parcial**
quando `0 < V_con,t < D_pl,t`; e **nulo** quando `V_con,t = 0`.


No tutorial de Lisboa com a cisterna de 3 000 L, 53,3% dos dias são plenos, 2,9% parciais e 43,8%
nulos. Repare que a fiabilidade temporal, 53,3%, é menor do que a volumétrica, cerca de 55,0%.
Não há contradição: os dias parciais não contam como plenos, mas contribuem com volume, e é essa
água que a fiabilidade volumétrica soma e a temporal não. A diferença entre as duas é, por isso,
uma medida indireta de quanto as falhas são falhas parciais. Com uma cisterna de 4 000 L os dias
plenos sobem para 58,0%, e com 5 000 L para 61,3%.

**O que mede:** com que frequência o utilizador pode contar com o sistema.

**O que não mede:** o volume. Um sistema pode ter 95% de dias plenos e um potencial baixo se a
procura pluvial for pequena, e o contrário também acontece.

> A fiabilidade temporal é o indicador que mais importa para o **projeto de águas**. Muitos dias
> nulos exigem uma alimentação automática de reserva bem dimensionada, e o utilizador nota a
> alternância entre as duas fontes.

---

### 2.3.4. Extravasamento

```equacao:extravasamento_medio:17
V_ext,med = ( Σ V_ext,t ) ÷ n
```

<!-- tabela: **Tabela 29** — Variáveis da Equação 17 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_ext,med` | extravasamento médio diário | L/dia |
| `V_ext,t` | volume extravasado no dia `t` | L |
| `n` | número de dias da série simulada | dia |

**O que mede:** quão pequena é a cisterna em relação aos eventos de chuva.

**O que não mede:** desperdício. A água que extravasa vai para a drenagem urbana, como iria sem o
sistema. Não há perda em relação ao cenário sem sistema; há apenas uma oportunidade não
aproveitada.

> O extravasamento **nunca se anula** num sistema real. Tende para um piso que é a diferença entre
> o que a cobertura capta e o que a procura consome. No tutorial de Lisboa, a oferta bruta da
> cobertura é 1,5 vez a procura pluvial, e mesmo com 20 000 L o extravasamento médio ainda é de
> 54 L/dia. Quem quer retenção de cheias precisa de um reservatório de detenção, que é outro
> projeto com outra lógica.

---

### 2.3.5. Eficiência de uso da água captada

O programa não imprime este indicador, mas ele sai diretamente dos anteriores e ajuda a perceber o
extravasamento. É a fração da água que chegou à cisterna, já descontado o descarte das primeiras
águas, que acabou consumida.

```equacao:uso_da_captacao:18
η_cap = ( Σ V_con,t ÷ Σ V_cap,t ) × 100
```

<!-- tabela: **Tabela 30** — Variáveis da Equação 18 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `η_cap` | eficiência de uso da água captada | % |
| `V_con,t` | volume de água da chuva consumido no dia `t` | L |
| `V_cap,t` | volume captado no dia `t`, depois do descarte | L |
| `Σ` | somatório sobre todos os dias da série simulada | — |

Na cisterna de 3 000 L do tutorial, o sistema consome 33,7 m³ por ano e extravasa em média
106,4 L/dia, cerca de 39 m³ por ano; as duas parcelas, com o pouco que fica no reservatório,
fecham o balanço de massa. Chegam assim à cisterna cerca de 73 m³ por ano, e é consumido pouco
menos de metade, cerca de 46%. O número explica por que aumentar a cisterna rende tão pouco a
partir de certo ponto: a água não falta na cobertura, falta **procura** para a consumir. A oferta
bruta da cobertura, de 92 m³ por ano, é 1,5 vez a procura pluvial de 61 m³ por ano; quando a
oferta excede largamente a procura pluvial, a eficiência de uso da água captada é
necessariamente baixa, qualquer que seja o volume.

---

### 2.3.6. Duração e intensidade das falhas

Os indicadores anteriores dizem quanto e com que frequência o sistema falha, mas não **como**
falha. Hashimoto, Stedinger e Loucks (1982) propuseram, para sistemas de recursos hídricos em
geral, três critérios complementares que hoje se usam também no aproveitamento pluvial: a
**fiabilidade**, que é a probabilidade de o sistema estar num estado satisfatório; a
**resiliência**, que mede a rapidez com que recupera de uma falha; e a **vulnerabilidade**, que
mede a gravidade das falhas quando ocorrem.

O programa reporta a primeira e não reporta as outras duas, mas ambas podem calcular-se a partir
da série diária detalhada, exportada para folha de cálculo: conte as sequências de dias não
plenos e tome a sua duração média, cujo inverso é uma medida de resiliência; e tome o défice
médio nos dias de falha como fração da procura pluvial, uma medida de vulnerabilidade.

A leitura para o projeto é direta. Se as falhas são longas e quase totais, o abastecimento de
reserva pela rede pública tem de ser automático e dimensionado para o caudal total dos pontos de
utilização pluviais, e não apenas para completar pequenas faltas. Os dias nulos do tutorial
(43,8% com 3 000 L) são deste tipo: a cisterna está vazia, e não ligeiramente em falta.

---

### 2.3.7. Volume anual poupado

```equacao:volume_poupado:19
V_poup = ( V_con,med × 365,25 ) ÷ 1000
```

<!-- tabela: **Tabela 31** — Variáveis da Equação 19 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_poup` | volume de água potável poupado por ano | m³/ano |
| `V_con,med` | consumo médio diário de água da chuva | L/dia |
| `365,25` | duração do ano médio, incluindo os bissextos | dia/ano |
| `1000` | conversão de litros para metros cúbicos | L/m³ |

**O que mede:** a base de cálculo da análise económica e da avaliação de ciclo de vida.

> **Aprofundamento: o 365,25 não é descuido.** A conversão usa o ano médio, incluindo os
> bissextos, porque as séries longas os contêm. Usar 365 introduziria um viés sistemático de
> 0,07%, pequeno, mas gratuito.

---

### 2.3.8. Ganho marginal

A definição formal do ganho marginal, com a grelha de volumes explicitada, está na Equação
11, na secção 2.2.

Definido na secção 2.2. É o indicador que decide o volume ideal, e **só existe numa
varredura**: uma simulação de volume único não o produz.

---

### 2.3.9. Procura não satisfeita

```equacao:nao_atendida:20
V_nao,med = ( Σ V_nao,t ) ÷ n
```

<!-- tabela: **Tabela 32** — Variáveis da Equação 20 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `V_nao,med` | procura média diária não satisfeita por nenhuma fonte | L/dia |
| `V_nao,t` | procura não satisfeita no dia `t` | L |
| `n` | número de dias da série simulada | dia |

Terceira parcela do balanço da procura. É zero na configuração de partida e deixa de ser zero
quando o abastecimento de reserva da rega está desligado.

**Por que existe:** sem ela, o balanço fecharia por construção, atribuindo à rede toda a procura
que a chuva não satisfez. A secção 2.1 detalha.

---

### 2.3.10. Quadro-resumo

<!-- tabela: **Tabela 33** — Quadro-resumo dos indicadores, com o denominador e a pergunta a que cada um responde -->
| Indicador | Unidade | Denominador | Responde |
| :--- | :--- | :--- | :--- |
| potencial de poupança | % | procura total | quanto do consumo de água potável desce |
| fiabilidade volumétrica | % | procura pluvial | quanto do pretendido foi satisfeito |
| dias plenos, parciais, nulos | % | dias da série | com que frequência se pode contar com ele |
| extravasamento | L/dia | — | o reservatório é pequeno? |
| volume poupado | m³/ano | — | base do dinheiro e do carbono |
| ganho marginal | %/m³ | — | vale a pena ampliar? |
| procura não satisfeita | L/dia | — | o que ninguém forneceu |

---

## 2.4. Índices pluviométricos

> Esta secção traz a equação de cada um dos nove índices que o programa calcula, e declara três
> divergências em relação ao padrão ETCCDI.

Os índices pluviométricos não participam no balanço hídrico e não alteram nenhum resultado de
simulação. A sua função é caracterizar a série de precipitação, e uma caracterização honesta é o
que permite comparar estudos de cidades diferentes.

---

### 2.4.1. Os nove índices

Os índices calculam-se **ano a ano** sobre a série carregada, e o programa reporta a média e a
dispersão do conjunto de anos. Em toda esta secção, `P_i` designa a precipitação do dia `i` do
ano, e um **dia húmido** é aquele em que `P_i ≥ 1 mm`, convenção do ETCCDI adotada porque lâminas
inferiores a um milímetro são da ordem do erro de medição dos udómetros convencionais.

#### 2.4.1.1. Precipitação total anual, PRCPTOT

Soma da precipitação de todos os dias húmidos do ano. Difere do total anual bruto por excluir os
dias de lâmina desprezável, o que evita que o ruído do instrumento se acumule no total.

```equacao:prcptot:21
PRCPTOT = Σ P_i , para P_i ≥ 1 mm
```

<!-- tabela: **Tabela 34** — Variáveis da Equação 21 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `PRCPTOT` | precipitação total dos dias húmidos do ano | mm |
| `P_i` | precipitação do dia `i` | mm |
| `Σ` | somatório sobre os dias do ano que satisfazem a condição | — |

#### 2.4.1.2. Precipitação em dias muito húmidos, R95p

Soma da precipitação dos dias cuja lâmina excede o percentil 95 dos dias húmidos. Mede quanto do
total anual chega nos eventos extremos, e é o índice mais diretamente ligado ao extravasamento das
cisternas.

```equacao:r95p:22
R95p = Σ P_i , para P_i > q_95
```

<!-- tabela: **Tabela 35** — Variáveis da Equação 22 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `R95p` | precipitação acumulada nos dias muito húmidos | mm |
| `P_i` | precipitação do dia `i` | mm |
| `q_95` | percentil 95 da precipitação dos dias húmidos da série | mm |

#### 2.4.1.3. Máxima precipitação num dia, RX1day

O maior valor diário registado no ano. É o índice que dimensiona o ladrão e a caleira, e não o
reservatório.

```equacao:rx1day:23
RX1day = max ( P_i )
```

<!-- tabela: **Tabela 36** — Variáveis da Equação 23 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `RX1day` | maior precipitação diária do ano | mm |
| `P_i` | precipitação do dia `i` | mm |
| `max` | valor máximo sobre todos os dias do ano | — |

#### 2.4.1.4. Máxima precipitação em cinco dias, RX5day

O maior acumulado de cinco dias consecutivos no ano. Importa mais ao aproveitamento pluvial do
que o RX1day, porque um reservatório enche ao longo de um evento prolongado e não apenas no pico
diário.

```equacao:rx5day:24
RX5day = max ( Σ P_j ) , para j de i a i + 4
```

<!-- tabela: **Tabela 37** — Variáveis da Equação 24 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `RX5day` | maior acumulado de cinco dias consecutivos no ano | mm |
| `P_j` | precipitação do dia `j` da janela | mm |
| `i` | primeiro dia de cada janela de cinco dias | — |
| `max` | valor máximo sobre todas as janelas do ano | — |

#### 2.4.1.5. Índice simples de intensidade diária, SDII

Precipitação média dos dias húmidos. Separa dois regimes que o total anual confunde: muita chuva
em poucos dias e pouca chuva em muitos dias podem produzir o mesmo PRCPTOT e SDII muito
diferentes.

```equacao:sdii:25
SDII = PRCPTOT ÷ n_húmidos
```

<!-- tabela: **Tabela 38** — Variáveis da Equação 25 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `SDII` | intensidade média dos dias húmidos | mm/dia |
| `PRCPTOT` | precipitação total dos dias húmidos, da Equação 21 | mm |
| `n_húmidos` | número de dias húmidos do ano | dia |

#### 2.4.1.6. Dias de precipitação intensa, R20mm

Contagem dos dias em que a lâmina atinge ou excede vinte milímetros. Num sistema de aproveitamento
pluvial, são tipicamente os dias de extravasamento.

```equacao:r20mm:26
R20mm = # { i : P_i ≥ 20 mm }
```

<!-- tabela: **Tabela 39** — Variáveis da Equação 26 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `R20mm` | número de dias com precipitação intensa no ano | dia |
| `P_i` | precipitação do dia `i` | mm |
| `# { }` | contagem dos dias que satisfazem a condição | — |

#### 2.4.1.7. Dias secos consecutivos, CDD

Maior sequência de dias consecutivos com precipitação inferior a um milímetro. ==É o índice que
melhor prevê o desempenho de um sistema pluvial,== porque a estiagem mais longa é o que esvazia a
cisterna.

```equacao:cdd:27
CDD = max ( L ) , com P_i < 1 mm em toda a sequência L
```

<!-- tabela: **Tabela 40** — Variáveis da Equação 27 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CDD` | maior sequência de dias secos consecutivos no ano | dia |
| `L` | comprimento de uma sequência de dias secos consecutivos | dia |
| `P_i` | precipitação do dia `i` | mm |

#### 2.4.1.8. Dias húmidos consecutivos, CWD

Maior sequência de dias consecutivos com precipitação igual ou superior a um milímetro.
Caracteriza a persistência da chuva, e as sequências longas favorecem o enchimento completo do
reservatório.

```equacao:cwd:28
CWD = max ( L ) , com P_i ≥ 1 mm em toda a sequência L
```

<!-- tabela: **Tabela 41** — Variáveis da Equação 28 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CWD` | maior sequência de dias húmidos consecutivos no ano | dia |
| `L` | comprimento de uma sequência de dias húmidos consecutivos | dia |
| `P_i` | precipitação do dia `i` | mm |

#### 2.4.1.9. Índice de sazonalidade, SI

Mede o afastamento entre a distribuição mensal real da chuva e a distribuição perfeitamente
uniforme ao longo do ano. Ao contrário dos oito anteriores, não pertence ao conjunto ETCCDI: foi
proposto por Walsh e Lawler em 1981.

```equacao:sazonalidade:29
SI = ( 1 ÷ R ) × Σ | X_m − R ÷ 12 |
```

<!-- tabela: **Tabela 42** — Variáveis da Equação 29 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `SI` | índice de sazonalidade de Walsh e Lawler | adimensional |
| `R` | precipitação total do ano | mm |
| `X_m` | precipitação total do mês `m`, com `m` de 1 a 12 | mm |
| `R ÷ 12` | precipitação mensal que haveria se a chuva fosse uniforme | mm |
| `Σ` | somatório sobre os doze meses do ano | — |
| `\| \|` | valor absoluto da diferença | — |

O índice da Equação 29 vale zero quando todos os meses recebem a mesma lâmina e
tende para 1,83 quando toda a chuva do ano cai num único mês. Entre estes extremos, Walsh e
Lawler (1981) classificam o regime em muito uniforme (abaixo de 0,20), uniforme com estação
húmida definida (0,20 a 0,39), sazonal com estação seca curta (0,40 a 0,59), sazonal (0,60 a
0,79), marcadamente sazonal com estação seca longa (0,80 a 0,99), com a maior parte da chuva em
até três meses (1,00 a 1,19) e extremo (1,20 ou mais).

O índice de sazonalidade é o que mais importa ao aproveitamento pluvial, e a secção 3.1
mostra porquê: é a distribuição da chuva ao longo do ano, e não o total precipitado, que decide o
rendimento do sistema.

---

Os nove índices ficam abstratos enquanto permanecem em forma de tabela, e a Figura 15
posiciona-os sobre um ano da série. Postos sobre um ano real de série, cada um passa a apontar um
troço identificável do registo: o dia mais intenso, os dias acima do limiar, a maior estiagem, o
total acumulado.

![Os índices marcados sobre um ano de série](../figuras/fig16_indices.png)

*Figura 15 — Quatro dos nove índices marcados sobre um ano da série de Lisboa: PRCPTOT e SDII, no alto; RX1day, o maior valor diário do ano; CDD, a maior sequência de dias secos, na faixa sombreada; e R20mm, os dias com 20 mm ou mais, marcados na base.*

A sazonalidade é o índice que menos se parece com os restantes, porque não descreve intensidade
nem frequência: descreve quanto a chuva do ano se concentra numa parte dele. É também o índice que
mais separa cidades com totais anuais semelhantes, e o que melhor prevê se um reservatório terá de
atravessar uma estiagem longa (Figura 16).

![O índice de sazonalidade nas três cidades de exemplo](../figuras/fig17_sazonalidade.png)

*Figura 16 — Índice de sazonalidade de Walsh e Lawler (1981) nas três cidades de exemplo (Lisboa, Porto e Funchal), com as classes do índice ao fundo e a precipitação média anual sob o nome de cada cidade. Precipitação anual elevada e distribuição uniforme ao longo do ano são propriedades independentes.*

---

### 2.4.2. Três divergências que têm de ser declaradas

O programa chama ao conjunto «ETCCDI mais sazonalidade», e a precisão da expressão importa.

**Primeira: o conjunto não é ETCCDI puro.** O índice de sazonalidade é de Walsh e Lawler, e não
pertence ao conjunto do *Expert Team on Climate Change Detection and Indices*. Em compensação, o
**R10mm**, que é ETCCDI, **não** está implementado.

Oito dos nove índices são ETCCDI; o nono não é; e falta um que seria.

**Segunda: o período de base do percentil.** O R95p exige um percentil 95 dos dias húmidos. O
ETCCDI define o período de base fixo de 1961 a 1990. O programa calcula o percentil sobre **toda a
série carregada**.

A consequência é que o R95p de duas séries de comprimentos diferentes **não é diretamente
comparável**, porque o limiar de cada uma é próprio. Para uma comparação estrita com a literatura
ETCCDI, corte a série no período de base.

O programa calcula o percentil **apenas sobre os dias húmidos**, o que está correto: incluir os
dias secos deslocaria o percentil para baixo em séries sazonais.

**Terceira: as janelas incompletas do RX5day.** A soma móvel de cinco dias usa janelas parciais no
início de cada ano, de modo que as primeiras janelas têm de um a quatro dias. O efeito é pequeno e
vai sempre no sentido de subestimar o RX5day dos primeiros dias do ano.

---

O separador de índices do programa apresenta cada indicador ano a ano: a precipitação total anual
(Figura 17) e as maiores sequências de dias secos e chuvosos
(Figura 18).

![A precipitação total anual, ano a ano, no ecrã do programa](../figuras/fig53_programa_prcptot.png)

*Figura 17 — Precipitação total anual (PRCPTOT) da série de Lisboa, com a média do período a tracejado, no separador de índices. Figura gerada pelo próprio programa.*

---
![As estiagens e as sequências chuvosas, ano a ano](../figuras/fig54_programa_cdd_cwd.png)

*Figura 18 — Maior sequência anual de dias secos (CDD) e de dias chuvosos (CWD) da série de Lisboa, no separador de índices. São os dois índices mais diretamente ligados ao volume de reservatório que o regime de chuva exige. Figura gerada pelo próprio programa.*

---
### 2.4.3. Para que servem no estudo

**Caracterizar a série** no método do artigo. PRCPTOT, SDII e SI descrevem o regime melhor do que
a média anual sozinha.

**Explicar o resultado.** Um CDD alto, ou um regime fortemente sazonal, explica um desempenho
inferior ao que o total anual sugere: na secção 3.1, Lisboa recebe chuva em 22% dos dias, o
seu mês mais chuvoso tem 47,3 vezes a chuva do mais seco, e a mesma moradia rende 17,49% com
5 000 L, contra 22,04% no Porto, onde chove em 31% dos dias e a razão entre o mês mais e o menos
chuvoso é de 9,8.

**Comparar cenários climáticos.** Entre a série histórica e a projetada, o que costuma mudar
primeiro é o SDII e o CDD, e não o PRCPTOT. Reportar só o total anual esconde a mudança que mais
afeta o sistema.

---

### 2.4.4. O que os índices não fazem

Não entram no balanço. Não alteram o dimensionamento. Não substituem a simulação diária, que é
justamente o argumento do programa contra os métodos por valores médios.

Um índice é um resumo. O balanço usa a série inteira.

---

## 2.5. Dimensionamento da ETAP

> Esta secção formaliza como o programa dimensiona a estação de tratamento de água
> pluvial (ETAP) e explica a **regra incremental**, que impede o tratamento de ser contado
> duas vezes no orçamento e no fluxo de caixa.

A água que escoa de uma cobertura transporta poeiras, folhas, partículas e dejetos de aves, e
nenhum uso — nem mesmo a alimentação de autoclismos — admite que chegue ao ponto de consumo
tal como sai do telhado. A estação de tratamento de água pluvial, abreviada como ETAP, é o
conjunto de equipamentos que realiza essa adequação, e o programa dimensiona-a a partir
de três entradas: a classe de qualidade exigida pelo uso, a área de captação e o volume
pluvial anual efetivamente consumido, este último resultante do balanço diário
apresentado na secção 2.1.

A linha de tratamento dimensionada pelo programa possui quatro componentes em série: o **descarte inicial** desvia a primeira lâmina de cada evento de precipitação, que transporta as impurezas acumuladas na cobertura; o **filtro mecânico de entrada** retém folhas e sólidos grosseiros antes que cheguem ao reservatório; a **desinfeção** é o estágio obrigatório, do qual depende a segurança microbiológica da água armazenada; e o **filtro de polimento** é opcional, destinando-se a utilizações em que a limpidez ou a ausência de resíduos dissolvidos é requerida.

---

A linha de tratamento é uma sequência, e a ordem dos estágios não é arbitrária: cada
um remove aquilo que tornaria o seguinte ineficaz. Convém ter o encadeamento inteiro à vista antes de discutir cada componente (Figura 19). A ordem não é intercambiável: desinfetar antes de filtrar consome o reagente na matéria orgânica em suspensão e deixa microrganismos protegidos no interior das partículas. A turbidez é, por isso, condição de eficácia da desinfeção, e não apenas um parâmetro estético.

![A sequência de estágios da linha de tratamento](../figuras/fig00j_etap.png)

*Figura 19 — Componentes da linha de tratamento dimensionada pelo programa, na ordem do escoamento, e destino do material retido. O descarte inicial e o filtro de entrada atuam antes da cisterna; a desinfeção atua depois deles porque o reagente seria consumido pela matéria orgânica em suspensão que os estágios anteriores removem; o filtro de polimento é opcional.*

---

### 2.5.1. O filtro de entrada

O filtro de entrada é dimensionado pela área de cobertura, e não pela classe de
qualidade pretendida, porque tem de acomodar o caudal de ponta produzido pela cobertura
— grandeza independente do destino final da água. As três faixas adotadas pelo
programa correspondem às capacidades nominais que os fabricantes declaram para equipamentos
usuais de mercado (filtros mecânicos em linha e vórtex autolimpantes).

<!-- tabela: **Tabela 43** — Filtro mecânico de entrada dimensionado pela área de cobertura -->
| Cobertura | Equipamento | Malha |
| :--- | :--- | ---: |
| até 200 m² | vórtex autolimpante DN 100 | 350 µm |
| até 500 m² | vórtex autolimpante DN 150 | 400 µm |
| acima de 500 m² | cesto ou ciclónico DN 200 | 500 µm |

> Os limites de faixa acompanham a área nominal que o fabricante declara atender, e não
> uma margem arbitrária. É a razão pela qual uma cobertura de 180 m² recebe o filtro de
> DN 100: o equipamento é suficiente para até 200 m², e impor
> o escalão seguinte encareceria a instalação sem fundamento técnico.

---

### 2.5.2. A desinfeção

A desinfeção é o estágio que o programa nunca dispensa, e a razão reside no conceito de
residual desinfetante. Entre as três tecnologias disponíveis, apenas a cloração deixa na água um
agente desinfetante que permanece ativo após a passagem pelo equipamento; a radiação ultravioleta e a ozonização atuam no instante da passagem e nada deixam a jusante (Figura 20).

![As três tecnologias de desinfecção disponíveis](../figuras/fig30_desinfeccao.png)

*Figura 20 — As três tecnologias de desinfeção, o efeito residual de cada uma e a composição do custeio anual (OPEX). O efeito residual distingue a cloração das restantes: protege a água armazenada na cisterna e na rede, enquanto a radiação ultravioleta e o ozono atuam apenas sobre a água que atravessa o reator.*


==A radiação ultravioleta e o ozono entram como barreira adicional à cloração, e não como
substitutos desta.== Sem residual, a água tratada volta a contaminar-se ao longo da rede
de distribuição interior, e as boas práticas de engenharia sanitária — em harmonia com a
norma EN 16941-1 e as recomendações técnicas da ANQIP (ETA 0701) — mantêm a cloração residual
livre para proteção do armazenamento e tubagens. A consequência económica é direta: as duas opções adicionais
somam o seu custo ao do cloro, e optar por qualquer uma delas não reduz o custeio operacional.

#### 2.5.2.1. A massa de cloro

O consumo de desinfetante é dimensionado pela massa de produto comercial necessária por metro
cúbico tratado, resultante da dosagem aplicada e do teor de cloro ativo do produto adquirido.

```equacao:massa_cloro:30
m_prod = ( C_Cl ÷ 1000 ) ÷ p
```

<!-- tabela: **Tabela 44** — Variáveis da Equação 30 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `m_prod` | massa de produto comercial consumida por metro cúbico tratado | kg/m³ |
| `C_Cl` | dose de cloro ativo aplicada à água | mg Cl₂/L |
| `1000` | conversão de miligramas por litro para quilogramas por metro cúbico | — |
| `p` | pureza do produto, em massa de cloro ativo por massa de produto | adimensional |

> **Adquire-se o produto comercial, e não o cloro puro.** As pastilhas de hipoclorito de
> cálcio contêm habitualmente cerca de 65% de cloro ativo, e o preço de mercado por quilograma refere-se
> ao produto embalado, não ao princípio ativo. Dimensionar o custo pela massa de cloro
> puro subestimaria a despesa na proporção inversa da concentração (~35%).

---

### 2.5.3. O filtro de polimento

O filtro de polimento é opcional e constitui o único ponto do dimensionamento em que a
classe de qualidade pretendida orienta a escolha do equipamento. Para utilizações mais
exigentes, o programa recomenda a sua inclusão, variando também o
meio filtrante: usos que envolvam contacto próximo exigem carvão ativado em bloco, ao passo que
usos gerais se satisfazem com filtro de areia ou cartucho de polipropileno de vinte micrómetros.

<!-- tabela: **Tabela 45** — Recomendação de filtro de polimento por classe de qualidade alvo -->
| Classe | Recomenda polimento? | Equipamento quando selecionado |
| :--- | :---: | :--- |
| 1 — Usos não potáveis gerais e autoclismos | não | filtro de areia ou cartucho de 20 µm |
| 2 — Rega e lavagem de pavimentos | sim | idem |
| 3 — Torres de arrefecimento e climatização | sim | idem |
| 4 — Lavagem de roupa | sim | **carvão ativado em bloco** |

A recomendação não é uma imposição cega: o filtro só integra o orçamento se o
utilizador o selecionar explicitamente. Quando a classe o recomenda e o utilizador não o seleciona,
o programa regista a opção no relatório técnico, garantindo a rastreabilidade da decisão.

---

### 2.5.4. O descarte de primeiras águas

O descarte de primeiras águas entra no cálculo em duas vertentes. No balanço hídrico diário,
é a lâmina subtraída à precipitação de cada dia com chuva, descrita na secção 2.1. No orçamento,
quando o dimensionamento físico do dispositivo de primeira lavagem está ativado na etapa
**3. Qualidade & ETAP**, constitui um subsistema com investimento, manutenção e pegada de carbono próprios,
composto pelo separador de folhas e pela câmara de desvio.

O volume da câmara de descarte é o produto da lâmina de desvio pela área de captação,
`V_desc = d × A`, em litros, com `d` em milímetros e `A` em metros quadrados. Para pequenos volumes,
o sistema prevê tubagem vertical de desvio com válvula de drenagem lenta; para volumes maiores,
uma câmara dedicada com boia de vedação. Na edição para Portugal, os custos de investimento e
manutenção do subsistema são parametrizáveis na interface ou adotam valores ilustrativos de referência.

<!-- tabela: **Tabela 46** — Dimensionamento do descarte inicial no projeto do tutorial -->
| Parâmetro | Valor |
| :--- | ---: |
| lâmina de descarte | 2 mm |
| área de captação | 150 m² |
| volume da câmara de descarte | 300 L |
| carbono incorporado da câmara e separador | 21,1 kg CO₂e |

O investimento do subsistema integra o orçamento da linha de tratamento e entra no
fluxo de caixa através da regra incremental apresentada a seguir.

---

### 2.5.5. A regra incremental

A regra incremental impede o erro frequente de duplicar parcelas de tratamento no orçamento
e no custeio operacional. Aplica-se em três níveis distintos:

**No investimento inicial.** O orçamento global de um sistema de aproveitamento de águas pluviais
já inclui habitualmente uma verba preliminar de filtragem e acessórios. Somar o custo da linha de
tratamento detalhada sem abater essa verba duplicaria a despesa. O programa calcula apenas o acréscimo:

```equacao:capex_etap:31
CAPEX_inc = CAPEX_linha − V_gen
```

<!-- tabela: **Tabela 47** — Variáveis da Equação 31 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CAPEX_inc` | investimento incremental da linha de tratamento | € |
| `CAPEX_linha` | custo total dos equipamentos da linha dimensionada | € |
| `V_gen` | verba genérica de tratamento já incluída na rubrica de acessórios | € |

**No custeio anual.** O consumo de cloro já é contabilizado na linha de reagentes operacionais
do fluxo de caixa. O custeio incremental da ETAP deduz essa parcela para que o produto químico não seja
orçado duas vezes.

**Na avaliação de ciclo de vida.** A linha de tratamento detalhada **substitui** o termo expedito
de cloração, assegurando que o inventário de materiais reflita a configuração física exata sem sobreposições.

---

### 2.5.6. Desativação da ETAP

O dimensionamento da linha de tratamento pode ser desligado na interface. Nesse caso,
nem o investimento nem os custos operacionais da ETAP incidem sobre a análise económica.
Essa opção destina-se a estudos em que a edificação já dispõe de tratamento pré-existente
ou em que se pretende isolar o custo hidráulico do armazenamento. Desativá-la no programa
não significa que a água pluvial dispense tratamento sanitário: significa unicamente que o tratamento
não está a ser imputado a este orçamento.

---

### 2.5.7. Limites do dimensionamento

O dimensionamento automático do programa concentra-se nos equipamentos funcionais da linha.
Ficam sob responsabilidade do projetista: o traçado detalhado da tubagem de ligação e drenagem,
a verificação rigorosa das perdas de carga localizadas no circuito de tratamento, o plano
sistemático de manutenção preventiva (limpeza periódica de malhas, desobstrução de vórtex e calibração de dosadores)
e a monitorização analítica laboratorial da qualidade da água, conforme estipulado pela regulamentação
técnica e sanitária em vigor.

---

## 2.6. Energia de bombagem

> Esta secção formaliza a cadeia energética completa do eixo à tomada elétrica e explica por que a
> potência nominal de placa **não** é o valor medido pelo contador de energia.

Três versões deste modelo existiram ao longo da evolução do programa, e as versões preliminares
cometiam os enganos descritos no item «Por que a cadeia completa importa»: tomar a potência mecânica
de placa como consumo elétrico e descontar o rendimento da bomba duas vezes. Quem consulta estudos
elaborados em versões antigas necessita de ter presente esta distinção.

---

### 2.6.1. A potência de placa é a potência de eixo

As normas de motores elétricos (norma internacional IEC 60034-30-1 e norma europeia EN 60034-1)
estipulam que o **rendimento** venha expressamente indicado na placa de identificação do motor,
como grandeza distinta da potência nominal. Esta distinção reflete o facto físico de a potência
de placa representar a potência mecânica disponível **no veio (eixo)**.

A cadeia de bombagem integra, por conseguinte, dois rendimentos complementares:

<!-- tabela: **Tabela 48** — Os dois rendimentos da cadeia de bombeamento e o que cada um converte -->
| Rendimento | Conversão efetuada |
| :--- | :--- |
| **da bomba**, `η_b` | potência mecânica no veio em potência hidráulica transmitida ao fluido |
| **do motor elétrico**, `η_m` | potência elétrica absorvida da rede em potência mecânica no veio |

O programa solicita ambos os parâmetros em campos diferenciados.

---

### 2.6.2. As equações de cálculo

**Consumo específico de energia na elevação**, por metro cúbico bombeado:

```equacao:energia_especifica:32
e = ( ρ × g × H ) ÷ ( η_b × η_m )
```

<!-- tabela: **Tabela 49** — Variáveis da Equação 32 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `e` | consumo específico de energia por volume elevado | kWh/m³ |
| `ρ` | massa volúmica da água, adotada como 1.000 | kg/m³ |
| `g` | aceleração da gravidade, adotada como 9,81 | m/s² |
| `H` | altura manométrica total da instalação | m c.a. |
| `η_b` | rendimento hidráulico da bomba | adimensional |
| `η_m` | rendimento do motor elétrico | adimensional |

==A Equação 32 é independente do caudal de serviço e da potência instalada.==
Elevar um metro cúbico de água a uma dada altura manométrica requer a mesma quantidade de energia
teórica quer se utilize um grupo elevatório pequeno ou sobredimensionado; a variação na potência
determina o tempo necessário para completar a bombagem, não o consumo específico do processo.

**Quando o caudal de funcionamento é expressamente declarado:**

```equacao:energia_por_vazao:33
e = P ÷ ( Q × η_m )
```

<!-- tabela: **Tabela 50** — Variáveis da Equação 33 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `e` | consumo específico de energia por volume elevado | kWh/m³ |
| `P` | potência de placa da eletrobomba, medida no veio | kW |
| `Q` | caudal de bombagem introduzido ou deduzido | m³/h |
| `η_m` | rendimento do motor elétrico | adimensional |

O rendimento da bomba hidráulica não surge na Equação 33 porque
já está implicitamente refletido no facto de um veio com potência `P` permitir fornecer o caudal `Q`
à altura manométrica considerada. Dividir novamente por `η_b` duplicaria as perdas hidráulicas.

**Caudal deduzido, quando não declarado:**

```equacao:vazao_deduzida:34
Q = ( P × η_b ) ÷ ( ρ × g × H )
```

<!-- tabela: **Tabela 51** — Variáveis da Equação 34 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Q` | caudal de bombagem deduzido | m³/h |
| `P` | potência de placa do grupo elevatório | kW |
| `η_b` | rendimento hidráulico da bomba | adimensional |
| `ρ` | massa volúmica da água (1.000) | kg/m³ |
| `g` | aceleração da gravidade (9,81) | m/s² |
| `H` | altura manométrica total | m c.a. |

**Energia consumida nos arranques:**

```equacao:energia_partida:35
E_part = ( P × t_part ) ÷ η_m
```

<!-- tabela: **Tabela 52** — Variáveis da Equação 35 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_part` | energia consumida nos arranques acumulados do período | kWh |
| `P` | potência nominal no veio | kW |
| `t_part` | tempo acumulado de arranque transitório no período | h |
| `η_m` | rendimento do motor elétrico | adimensional |

O rendimento da bomba hidráulica não intervém na Equação 35 pelo facto
de durante o curto intervalo de arranque não existir débito útil estável, correspondendo
a energia consumida ao regime de transição do motor elétrico.

A energia elétrica anual total consumida pelo grupo de bombagem corresponde à soma do
consumo do volume efetivamente transferido com o dispêndio dos ciclos de arranque:

```equacao:energia_anual:36
E_ano = e × V_rec + ( P × t_part ) ÷ η_m
```

<!-- tabela: **Tabela 53** — Variáveis da Equação 36 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_ano` | energia elétrica anual consumida pela eletrobomba | kWh/ano |
| `e` | consumo específico de energia | kWh/m³ |
| `V_rec` | volume anual bombeado para o reservatório superior | m³/ano |
| `P` | potência nominal no veio | kW |
| `t_part` | tempo acumulado de arranques durante o ano | h/ano |
| `η_m` | rendimento do motor elétrico | adimensional |

---

A potência de placa de uma eletrobomba expressa a potência mecânica no veio, e não o consumo elétrico
registado no contador (Figura 21). A título de exemplo, uma eletrobomba de 0,37 kW (0,5 cv)
com motor elétrico de rendimento 60,5% absorve da rede cerca de 0,61 kW: calcular a despesa energética
apenas com a potência de placa subestimaria o consumo em cerca de 40%, distorcendo a análise económica.

![A cadeia de rendimentos entre a tomada e a água elevada](../figuras/fig00k_energia.png)

*Figura 21 — Cadeia energética da bombagem predial. A potência nominal indicada na placa é a potência no veio, posicionada no centro da cadeia: entre esta e o contador elétrico situa-se o rendimento do motor (η_m); entre o veio e a potência hidráulica útil entregue à água situa-se o rendimento da bomba (η_b).*

A potência hidráulica necessária é determinada pela altura manométrica total, que combina
o desnível geométrico real com as perdas de carga contínuas e singulares da instalação (Figura 22).
As perdas de carga contínuas na tubagem são calculadas pela formulação universal de Darcy-Weisbach
(`h_f = f · (L/D) · v²/2g`), e as perdas localizadas em válvulas, curvas e uniões pela equação
geral `h_loc = K · v²/2g`. Em circuitos prediais habituais de elevação, as perdas somam tipicamente entre 10% e 30% do desnível geométrico.

![A altura manométrica decomposta em desnível e perdas](../figuras/fig00l_manometrica.png)

*Figura 22 — (a) Altura manométrica de um sistema elevatório predial: desnível geométrico entre os níveis da cisterna e do reservatório superior somado às perdas de carga totais; (b) linha piezométrica ao longo de um troço de tubagem com perda de carga contínua por atrito e singularidades localizadas.*

---

### 2.6.3. O rendimento do motor elétrico

Caso o utilizador não especifique o rendimento no projeto, o programa adota valores de
referência baseados na classe de eficiência standard (IE1) da IEC 60034-30-1 para pequenos
motores de indução monofásicos de dois polos (~2.900 rpm / 50 Hz em Portugal) (Figura 23):

![O rendimento de motores de indução por potência e classe](../figuras/fig31_motores.png)

*Figura 23 — Rendimento indicativo de motores de indução por escalão de potência e classe de eficiência. O programa adota valores conservadores da classe standard quando o utilizador não insere dados específicos da ficha técnica.*

Os dois valores mais frequentes em instalações residenciais são 0,5 cv (0,37 kW),
com cerca de **60,5%** de rendimento standard, e 1,0 cv (0,75 kW), com cerca de **69,3%**.
A diferença de quase nove pontos percentuais repercute-se de modo direto no custeio energético.

---

### 2.6.4. Por que a cadeia completa importa

O consumo específico do sistema do tutorial (0,5 cv, 12 m c.a. de altura manométrica,
com reservatório superior) situa-se em torno de 0,11 kWh/m³. Descurar o rendimento
do motor ou descontar indevidamente o rendimento da bomba altera esse resultado em dezenas de pontos percentuais.

A formulação transparente adotada pelo programa visa exatamente evidenciar cada elo
físico da conversão de energia, permitindo auditorias técnicas consistentes.

---

### 2.6.5. O assistente de dimensionamento de eletrobombas

Quando o utilizador não dispõe das especificações exatas de catálogo da eletrobomba,
o botão *Assistente de Dimensionamento de Eletrobomba* (na etapa **4. Reservatório & Custos**)
permite estimar os parâmetros a partir dos dados do edifício:

1. **Caudal de elevação.** `Q = V_sup ÷ t_ench`, considerando o volume do reservatório superior e o tempo de enchimento de referência (habitualmente 45 minutos).
2. **Diâmetro económico.** Estimado por formulações hidráulicas usuais para regimes descontínuos em tubagem de polietileno de alta densidade (PEAD) ou PVC.
3. **Velocidade de escoamento.** Mantida na faixa de boa prática técnica (entre 0,6 m/s e 2,0 m/s).
4. **Perdas de carga.** Estimadas com base no comprimento do traçado e acessórios da instalação.
5. **Altura manométrica e potência.** Determinação do ponto de funcionamento de projeto `(Q, H_man)`.
6. **Seleção de equipamento.** Cruzamento do ponto de funcionamento com curvas de modelos comerciais integrados.

---

### 2.6.6. Pressurização hidropneumática direta

Nos sistemas sem reservatório superior, em que a distribuição não potável é efetuada
por bombagem direta com grupo sobrepressor hidropneumático, o ciclo de funcionamento difere
substancialmente. A bomba arranca em cada abertura de torneira ou descarga de autoclismo,
sendo o caudal limitado pelo ponto de utilização e não pela capacidade máxima do equipamento.

O programa calcula o consumo da pressurização direta considerando o tempo efetivo de funcionamento:

```equacao:energia_pressurizador:37
E = (P ÷ η_m) · [V ÷ min(Q_b(H), Q_p) + N · t_r]
```

<!-- tabela: **Tabela 54** — Variáveis da Equação 37 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E` | energia elétrica anual do sobrepressor | kWh/ano |
| `P` | potência nominal no veio | kW |
| `η_m` | rendimento do motor elétrico | adimensional |
| `V` | volume pluvial consumido no ano | m³/ano |
| `Q_b(H)` | caudal fornecido pela bomba à pressão de serviço `H` | m³/h |
| `Q_p` | caudal do dispositivo de utilização | m³/h |
| `N` | número anual de acionamentos | 1/ano |
| `t_r` | tempo de pós-circulação / retardo eletrónico de desligamento | h |

<!-- tabela: **Tabela 55** — Energia anual de seis sobrepressores genéricos (curvas ilustrativas, sem marca) na pressurização direta do tutorial, com o caudal do autoclismo a limitar o caudal da bomba -->
| Modelo | Comando | Caudal da curva a 18 m de altura manométrica | Horas por ano | kWh por ano | kWh/m³ | kWh por ano a 24 m |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Modelo A, 0,25 cv | pressostato | 10,1 L/min | 71 | 26,1 | 0,68 | 163,1 |
| Modelo B, 0,33 cv | fluxostato | 18,0 L/min | 71 | 31,4 | 0,82 | não atinge |
| Modelo C, 0,5 cv | pressostato | 27,5 L/min | 71 | 43,1 | 1,13 | 43,1 |
| Modelo D, 0,5 cv | pressostato | 26,0 L/min | 71 | 43,1 | 1,13 | 43,1 |
| Modelo F, 0,5 cv | eletrónico | 12,8 L/min | 71 | 43,1 | 1,13 | não atinge |
| Modelo E, 0,5 cv | eletrónico | 7,0 L/min | 112 | 67,9 | 1,77 | não atinge |

A comparação dos regimes evidencia que a pressurização hidropneumática direta consome
significativamente mais energia por metro cúbico fornecido do que a elevação pontual para
um reservatório superior por gravidade. Embora o custo financeiro absoluto da eletricidade
possa ser reduzido em moradias unifamiliares, a energia operacional constitui uma parcela
relevante na pegada ecológica do ciclo de vida analisada na secção 2.8.

---

## 2.7. Análise económica e regimes tarifários

> Esta secção formaliza o modelo de fluxo de caixa e detalha os regimes
> tarifários — o fator determinante na viabilidade económico-financeira de um sistema de aproveitamento de águas pluviais.

---

### 2.7.1. A poupança resulta da diferença entre duas faturas reais

O programa não calcula a poupança financeira multiplicando simplesmente o volume pluvial
poupado por uma tarifa unitária média. Essa distinção é crítica: para cada mês do horizonte
de projeto, o programa simula duas faturas completas — uma correspondente ao consumo total
que a edificação teria sem o sistema pluvial e outra associada à água potável da rede pública
efetivamente adquirida —, apurando a poupança através da diferença entre ambas.

```equacao:economia_mensal:38
E_mês = F(V_tot) − F(V_pot)
```

<!-- tabela: **Tabela 56** — Variáveis da Equação 38 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_mês` | poupança mensal obtida | € |
| `F(·)` | função de cálculo da fatura (água, saneamento e taxas) para um dado volume | € |
| `V_tot` | consumo mensal total que a edificação teria sem o sistema | m³ |
| `V_pot` | volume mensal de água potável adquirido da rede | m³ |

A razão desta metodologia assenta na estrutura progressiva por escalões e na existência
de componentes fixas nos tarifários. ==O metro cúbico poupado abate sempre nos escalões superiores de consumo, que são os mais onerosos por unidade de volume.== No tutorial de Lisboa, a fatura mensal desce de 46,25 € para 35,06 €, gerando uma poupança mensal de 11,19 €. Utilizar uma tarifa média linear induziria distorções significativas nos resultados.

---

### 2.7.2. A fatura dos serviços de águas

A estrutura tarifária dos serviços municipais de água e águas residuais é representada no
programa por uma sequência de patamares, em que cada patamar associa intervalos de volume,
preços e regras específicas de faturação.

A fatura mensal engloba parcelas de natureza distinta: uma tarifa fixa (quota de serviço),
que remunera a disponibilidade das infraestruturas e não varia com o consumo; os escalões
variáveis de consumo de água potável; e as tarifas de saneamento (águas residuais) e gestão de
resíduos associadas. A poupança gerada pela água pluvial incide de forma assimétrica sobre essas parcelas, tal como ilustrado na Figura 24.

![A fatura aberta em parcelas, com e sem o sistema](../figuras/fig07_fatura.png)

*Figura 24 — Fatura mensal de água e saneamento do projeto do tutorial, discriminada por parcelas, com e sem o sistema pluvial. A quota de serviço fixa permanece invariável; a redução financeira reflete-se nos escalões superiores de consumo volumétrico e na redução proporcional da tarifa variável de saneamento.*

O código associado a cada escalão no programa determina a sua aplicação no cálculo (Figura 25):
os códigos 1 ou 0 correspondem a escalões de consumo volumétrico; o código −1 representa a quota fixa de serviço
(tarifa de disponibilidade); o código −2 representa franquias retroativas; o código −3 define pisos mínimos de faturação;
e os códigos 2 e 3 correspondem a regimes de progressividade analítica.

![Os seis códigos de faixa tarifária](../figuras/fig32_codigos.png)

*Figura 25 — Os códigos de escalão tarifário e o respetivo impacto na faturação mensal. Estruturas com valores numéricos similares podem gerar resultados divergentes consoante a formulação regulamentar de cada escalão.*

#### 2.7.2.1. Saneamento e taxas proporcionais

```equacao:esgoto:39
T_esg = T_agua × s
```

<!-- tabela: **Tabela 57** — Variáveis da Equação 39 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `T_esg` | parcela de saneamento/águas residuais indexada | € |
| `T_agua` | parcela variável de consumo de água potável | € |
| `s` | rácio proporcional ou percentual regulamentar de saneamento | adimensional |

Quando o serviço de saneamento é cobrado em percentagem do valor da água ou por tarifa volumétrica proporcional aos metros cúbicos medidos, cada metro cúbico pluvial consumido gera benefício duplo: reduz a fatura do abastecimento e reduz a fatura do saneamento.

---

### 2.7.3. Os seis regimes tarifários suportados

O motor de cálculo suporta seis modalidades fundamentais de tarifação, detalhadas na secção 3.3 (Figura 26):

<!-- tabela: **Tabela 58** — Codificação dos regimes tarifários -->
| Regime | Descrição no programa | Aplicação matemática | Impacto da poupança de água |
| :--- | :--- | :--- | :--- |
| sem mínimo | escalões de consumo simples | soma volumétrica por escalão | cada metro cúbico poupado reduz a fatura |
| quota fixa (disponibilidade) | quota fixa (−1) mais escalões | valor fixo somado ao consumo | o consumo reduz-se; a quota fixa mantém-se |
| franquia no mínimo | quota fixa (−1) com 1.º escalão nulo | franquia incluída na tarifa base | poupar dentro da franquia não reduz a fatura |
| franquia retroativa | franquia comutativa (−2) | consumo acima cobra desde 0 m³ | baixar da franquia reduz abruptamente a fatura |
| piso de pagamento | limite inferior garantido (−3) | fatura limitada por um mínimo | reduções abaixo do piso não geram poupança |
| fórmula progressiva | base polinomial/exponencial | progressividade contínua | redução diferenciada pelo nível de consumo |

![Distribuição dos regimes tarifários](../figuras/fig33_regimes_base.png)

*Figura 26 — Caracterização conceptual dos regimes tarifários suportados pelo motor de cálculo.*

---

### 2.7.4. Investimento inicial (CAPEX)

O investimento inicial do sistema resulta do somatório das rubricas orçamentais da instalação:

```equacao:capex:40
CAPEX = C_cist + C_sup + C_mo + C_tub + C_ace + ( C_bomba × n_b ) + CAPEX_inc
```

<!-- tabela: **Tabela 59** — Variáveis da Equação 40 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CAPEX` | investimento inicial total do sistema | € |
| `C_cist` | custo do reservatório inferior (cisterna) | € |
| `C_sup` | custo do reservatório superior (quando existente) | € |
| `C_mo` | custo de mão de obra e montagem | € |
| `C_tub` | custo das tubagens e conexões | € |
| `C_ace` | acessórios, válvulas, quadro e cablagens | € |
| `C_bomba` | custo unitário da eletrobomba | € |
| `n_b` | número de eletrobombas instaladas (serviço e reserva) | unidade |
| `CAPEX_inc` | investimento incremental da linha de tratamento (ETAP) | € |

Nesta edição, as rubricas do CAPEX partem de zero e são introduzidas pelo utilizador: o programa não traz preços de Portugal nem de Espanha. A secção 4.7, em «O CAPEX nesta edição», descreve o estado verdadeiro, como introduzir os valores e o que está apenas planeado.

No caso de estudo do tutorial (Lisboa, cisterna de 5.000 L em polietileno com reservatório superior de 1.000 L), o investimento total ilustrativo ascende a 6.650 €. A Figura 27 apresenta a decomposição orçamental por componente.

![O investimento aberto por rubrica, em três volumes](../figuras/fig21_investimento.png)

*Figura 27 — Estrutura do investimento inicial por componente para diferentes capacidades de reservatório. Em volumes domésticos moderados, a tubagem, mão de obra e acessórios representam uma fração significativa do custo total.*

---

### 2.7.5. Custeio operacional anual (OPEX)

O custeio operacional anual agrega:
1. A energia elétrica consumida pelas eletrobombas (secção 2.6).
2. O consumo de reagentes desinfetantes (cloração).
3. A manutenção periódica da ETAP e do dispositivo de primeiras águas.
4. Outros custos operacionais declarados pelo utilizador.

Num projeto novo, nenhum destes custos vem preenchido: os preços partem de zero, e as rotinas de manutenção existem só como roteiro. A secção 4.7, em «O que entra no custo de exploração (OPEX)», diz o que é calculado sozinho (as quantidades), o que é do utilizador (os preços) e o que está planeado e não implementado. O campo de custo anual do resumo não inclui as rotinas de manutenção.

---

### 2.7.6. Projeção temporal do fluxo de caixa

A projeção económica é calculada mês a mês ao longo do período de vida útil analisado (habitualmente 20 anos), atualizando os custos operacionais pela inflação e as faturas pelas taxas de atualização tarifária:

```equacao:inflacao:41
f_inf = ( 1 + i )^( m − 1 )
```

```equacao:reajuste:42
f_j = ( 1 + r_j )^k
```

<!-- tabela: **Tabela 60** — Variáveis da Equação 42 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `f_inf` | fator acumulado de inflação no mês `m` | adimensional |
| `i` | taxa de inflação mensal estimada | adimensional |
| `f_j` | fator de atualização tarifária acumulado no período | adimensional |
| `r_j` | taxa de atualização tarifária anual | adimensional |
| `k` | número de anos decorridos até ao mês de cálculo | adimensional |

A Figura 28 sintetiza o fluxo de caixa acumulado ao longo do horizonte temporal.

![O saldo descontado acumulado ao longo de vinte anos](../figuras/fig08_fluxo_de_caixa.png)

*Figura 28 — Projeção do fluxo de caixa acumulado do projeto do tutorial ao longo de 20 anos, demonstrando o comportamento do investimento inicial face à poupança anual na fatura.*

---

### 2.7.7. Indicadores de rentabilidade

**Valor Atual Líquido (VAL):**

```equacao:vpl:43
VPL = − CAPEX + Σ [ FC_m ÷ ( 1 + TMA )^m ]
```

<!-- tabela: **Tabela 61** — Variáveis da Equação 43 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `VPL` | valor atual líquido do investimento (VAL) | € |
| `CAPEX` | investimento inicial total | € |
| `FC_m` | fluxo de caixa líquido verificado no mês `m` | € |
| `TMA` | taxa de atualização mensal de referência | adimensional |
| `m` | índice mensal de 1 até ao horizonte de cálculo | mês |

**Taxa Interna de Rentabilidade (TIR):** taxa que anula o VAL da série financeira. Caso o investimento não seja amortizável dentro do horizonte, o programa assinala a ausência de solução real.

**Período de recuperação do investimento (Payback):** mês em que o saldo acumulado descontado cruza o valor zero. No tutorial de Lisboa, aos custos de referência ilustrativos (6.650 € de investimento para uma poupança anual de cerca de 134 €), o VAL obtido é de −5.828,77 €, não existindo período de amortização no horizonte de 20 anos. Este resultado ilustra com clareza que, em climas com verão seco e tarifários moderados, o aproveitamento pluvial deve ser equacionado sob a perspetiva de resiliência e sustentabilidade ambiental, e não apenas de retorno financeiro imediato.

---

## 2.8. Avaliação de ciclo de vida e pegada de carbono

> Esta secção descreve as etapas do inventário ambiental, a fronteira do sistema adotada e
> explicita as premissas de triagem da pegada de carbono.

A avaliação de ciclo de vida (ACV) contabiliza os impactes ambientais de um produto ou
sistema ao longo do seu ciclo existencial, desde a extração das matérias-primas até ao descarte
ou reciclagem. Aplicada a um sistema de aproveitamento de águas pluviais, permite verificar
se as emissões de gases com efeito de estufa associadas ao fabrico e montagem dos reservatórios,
tubagens e eletrobombas são efetivamente compensadas pelas emissões evitadas ao prescindir do
fornecimento convencional de água potável da rede pública.

==A avaliação integrada no programa é uma ACV de triagem (*screening*), e não um estudo exaustivo de conformidade normativa.==
A sua finalidade é ordenar alternativas de dimensionamento (por exemplo, comparar o polietileno com o betão armado)
e identificar os processos dominantes, permitindo escolhas técnicas informadas em fase de projeto.

---

### 2.8.1. Estrutura da ACV segundo as normas internacionais

Em conformidade com a NP EN ISO 14040 e a NP EN ISO 14044, a avaliação estrutura-se em quatro fases:

1. **Definição do objetivo e âmbito.** Estabelece a finalidade do estudo, as fronteiras do sistema e a **unidade funcional**. A unidade funcional de referência no programa é o sistema completo concebido para responder às necessidades de um dado edifício ao longo da sua vida útil de projeto (tipicamente 20 anos), comparado com o abastecimento pela rede pública.
2. **Análise de inventário (ICV).** Quantifica os fluxos de matéria e energia: massa de componentes fabricados, consumo de eletricidade na bombagem, produtos químicos de desinfeção e volume de água potável evitado.
3. **Avaliação do impacte.** Converte os fluxos do inventário em indicadores ambientais. O programa calcula a categoria das **alterações climáticas**, expressa em quilogramas de dióxido de carbono equivalente (kg CO₂e), através dos fatores de emissão documentados no apêndice C.
4. **Interpretação dos resultados.** Analisa a robustez dos resultados e a sensibilidade do balanço de emissões face ao material do reservatório e à intensidade carbónica da rede elétrica.

---

### 2.8.2. Módulos do ciclo de vida segundo a norma EN 15978

Para instalações no setor da construção, a norma europeia EN 15978 define a partição temporal do ciclo de vida:

<!-- tabela: **Tabela 62** — Módulos do ciclo de vida da EN 15978 e o que a avaliação do programa cobre em cada um -->
| Módulo | Etapa do ciclo de vida | Cobertura pelo programa |
| :--- | :--- | :--- |
| A1 a A3 | Fabrico: extração de matérias-primas, transporte à fábrica e produção | Sim: reservatórios, tubagens, eletrobombas, descarte inicial e acessórios |
| A4 e A5 | Construção: transporte até à obra e instalação no edifício | Não considerado (a escavação e movimentação de terras não estão incluídas) |
| B1 a B5 | Uso, manutenção, reparação e substituição de componentes | Não considerado |
| B6 | Consumo de energia operacional | Sim: eletricidade consumida na bombagem |
| B7 | Consumo de água operacional | Sim: crédito ambiental da água potável evitada e reagentes da ETAP |
| C1 a C4 | Fim de vida: demolição, transporte, valorização e deposição final | Não considerado |
| D | Benefícios e encargos potenciais para além da fronteira (reciclagem) | Não considerado |

A fronteira de análise do programa classifica-se, assim, como **do berço ao portão da fábrica somada à fase de exploração (*cradle-to-gate with operational stage*)**.

---

### 2.8.3. As sete etapas do inventário de emissões

O inventário de emissões do programa reparte-se em sete parcelas funcionais (Figura 29):

![As sete etapas do inventário de ciclo de vida](../figuras/fig34_inventario.png)

*Figura 29 — As sete componentes do inventário de ciclo de vida do programa: as quatro primeiras correspondem ao carbono incorporado nos materiais; as duas seguintes às emissões operacionais anuais; e a sétima ao crédito ambiental anual pela água evitada (único termo dedutivo).*

---

### 2.8.4. Carbono incorporado nos materiais

```equacao:emissao_componente:44
E_comp = m_comp × FE_mat
```

<!-- tabela: **Tabela 63** — Variáveis da Equação 44 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_comp` | emissão de carbono incorporado no componente | kg CO₂e |
| `m_comp` | massa estimada do componente | kg |
| `FE_mat` | fator de emissão do material (*cradle-to-gate*) | kg CO₂e/kg |

<!-- tabela: **Tabela 64** — Massa por metro cúbico útil de cada material de reservatório -->
| Material | Massa indicativa por m³ útil | Massa para 5 m³ |
| :--- | ---: | ---: |
| Polietileno de alta densidade (PEAD) | 22 kg/m³ | 110 kg |
| Fibra de vidro (PRFV) | 15 kg/m³ | 75 kg |
| Aço inoxidável | 38 kg/m³ | 190 kg |
| Betão armado | 1.200 kg/m³ | 6.000 kg |

> **A massa condiciona o balanço de carbono.** O betão armado é o material mais massivo da lista. Em sistemas de pequena escala, um reservatório de betão de capacidade excessiva pode acumular uma dívida carbónica que não chega a ser amortizada ao longo dos 20 anos de vida útil do projeto.

#### 2.8.4.1. Inventário do projeto do tutorial

A tabela seguinte ilustra a repartição das emissões para o caso de estudo do tutorial (Lisboa, cisterna de 5.000 L em polietileno com reservatório superior de 1.000 L):

<!-- tabela: **Tabela 65** — Inventário de carbono do projeto final do tutorial, item a item, com a parcela de cada componente no carbono incorporado; os valores anuais negativos são créditos (fatores da rede e da água ilustrativos, não são valores medidos) -->
| Item | Incorporado | Parcela do incorporado | Anual |
| :--- | ---: | ---: | ---: |
| cisterna de 5 000 L, polietileno | 177,3 kg | 48,9% | — |
| reservatório superior de 1 000 L, polietileno | 35,5 kg | 9,8% | — |
| tubagem de PVC, DN 100 mm | 55,5 kg | 15,3% | — |
| tubagem de PVC, DN 32 mm | 3,5 kg | 1,0% | — |
| tubagem de PVC, DN 25 mm | 8,9 kg | 2,5% | — |
| duas eletrobombas de 0,5 cv | 61,0 kg | 16,8% | — |
| descarte das primeiras águas: reservatório de 300 L e separador de folhas | 21,1 kg | 5,8% | — |
| energia de elevação | — | — | 2,05 kg/ano |
| cloragem por pastilhas | — | — | 0,16 kg/ano |
| água da rede evitada | — | — | −19,59 kg/ano |
| **total** | **362,9 kg** | **100%** | **−17,38 kg/ano** |

---

### 2.8.5. Emissões operacionais e crédito ambiental

**Bombagem:**

```equacao:emissao_energia:45
E_ener = C_ano × FE_rede
```

<!-- tabela: **Tabela 66** — Variáveis da Equação 45 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_ener` | emissões anuais associadas à energia de bombagem | kg CO₂e/ano |
| `C_ano` | consumo anual de eletricidade da instalação | kWh/ano |
| `FE_rede` | fator de emissão da rede elétrica | kg CO₂e/kWh |

No estudo do tutorial, adotam-se fatores ilustrativos consistentes de referência (0,40 kg CO₂e/kWh para a rede e 0,50 kg CO₂e/m³ para a água potável evitada).

---

### 2.8.6. Fronteiras e processos excluídos

A Figura 30 sintetiza os limites da análise ambiental efetuada pelo programa:

![O que a avaliação ambiental inclui e o que ela deixa de fora](../figuras/fig00h_fronteira.png)

*Figura 30 — Delimitação da fronteira da avaliação ambiental: (a) processos incluídos — carbono incorporado dos reservatórios, tubagens e eletrobombas, emissões elétricas operacionais, produtos de tratamento e crédito da água potável poupada; (b) processos excluídos — movimentos de terras em obra civil, manutenção corretiva, fim de vida e outras categorias de impacte.*

---

### 2.8.7. Indicadores de desempenho ambiental

**Saldo líquido anual:**

```equacao:saldo_liquido:46
E_liq = E_evit − E_ener − E_trat
```

<!-- tabela: **Tabela 67** — Variáveis da Equação 46 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_liq` | saldo líquido anual de emissões evitadas | kg CO₂e/ano |
| `E_evit` | emissão evitada pela água potável substituída | kg CO₂e/ano |
| `E_ener` | emissão associada ao consumo elétrico da bombagem | kg CO₂e/ano |
| `E_trat` | emissões devidas aos consumíveis de tratamento | kg CO₂e/ano |

**Período de recuperação carbónica (Payback ambiental):**

```equacao:payback_carbono:47
PB_amb = E_inc ÷ E_liq
```

<!-- tabela: **Tabela 68** — Variáveis da Equação 47 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `PB_amb` | período de recuperação ambiental do sistema | ano |
| `E_inc` | carbono incorporado total no fabrico dos componentes | kg CO₂e |
| `E_liq` | saldo líquido anual de emissões evitadas | kg CO₂e/ano |

**Saldo acumulado ao fim da vida útil:**

```equacao:saldo_vida:48
S_vida = ( E_liq × n_anos ) − E_inc
```

```equacao:emissao_especifica:49
E_esp = S_vida ÷ V_vida
```

<!-- tabela: **Tabela 69** — Variáveis da Equação 49 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `S_vida` | saldo líquido total acumulado na vida útil | kg CO₂e |
| `n_anos` | vida útil de projeto adotada (tipicamente 20 anos) | ano |
| `E_inc` | carbono incorporado inicial | kg CO₂e |
| `E_esp` | emissão específica líquida evitada por volume | g CO₂e/L |
| `V_vida` | volume total de água pluvial fornecido na vida útil | m³ |

Caso o saldo anual não seja positivo (quando a energia de bombagem ou o tratamento superam o crédito da água evitada), a dívida de fabrico não é amortizada. O programa assinala essa ocorrência devolvendo o código convencional de 999 anos para permitir a ordenação comparativa em varreduras de projeto.

---

## 2.9. Certificações

> Esta secção reúne as regras de enquadramento dos referenciais de sustentabilidade que o
> programa avalia e distingue, em cada um, o que é requisito do referencial do que é critério
> adotado pelo programa.

Os sistemas de aproveitamento de águas pluviais aparecem em praticamente todos os referenciais
de certificação ambiental de edifícios, e em cada um com uma métrica própria. Uns medem a
poupança contra o consumo total do edifício, outros contra um caso-base de referência, e outros
ainda exigem a comparação em mais de uma dimensão em simultâneo. O programa calcula o
enquadramento nos referenciais internacionais abaixo a partir dos resultados da simulação, e fá-lo
sempre com a mesma ressalva: ==o programa mostra onde o projeto se enquadraria, e não certifica
coisa alguma.== A certificação é decidida pelo organismo certificador, com a documentação
completa do empreendimento, da qual o desempenho hídrico é apenas uma peça.

A Edição Ibérica mostra o LEED, o EDGE e o GRI. Os referenciais nacionais e europeus (ANQIP,
LiderA, BREEAM, Level(s)) não estão incorporados: descrevem-se mais abaixo, para que o
utilizador saiba o que cada um pede, e a poupança de água potável que o relatório do programa
fornece aplica-se com as regras de cada um, fora do programa.

Antes de os percorrer um a um, convém vê-los lado a lado. Os limiares de cada referencial estão
em escalas que parecem incomparáveis enquanto ficam em tabelas separadas, e passam a comparar-se
quando postos sobre a mesma régua de poupança (Figura 31). Os limiares abaixo
são os codificados no programa; confirme-os no texto vigente de cada referencial antes de os
citar. O LEED v4 pontua em separado a redução do uso exterior (WEc1: 1 ponto a partir de 50% e 2
pontos com 100%) e a do uso interior (WEc2: de 1 a 6 pontos entre 25% e 50%); o LEED v5 reúne a
categoria no crédito WEc2, em que a redução em aparelhos sanitários e torneiras vale de 1 a 3 pontos entre 30% e
40% e a redução do projeto inteiro, de 1 a 8 pontos entre 30% e 65%; e o EDGE exige uma redução
mínima de 20% em simultâneo na água, na energia e na energia incorporada nos materiais, sem
pontuação.

![Os limiares de poupança dos referenciais, na mesma régua](../figuras/fig37_certificacoes.png)

*Figura 31 — Os limiares de redução do consumo de água potável com que o programa enquadra o projeto no LEED v4 (créditos WEc1 e WEc2), no LEED v5 (crédito WEc2, opções 1, 2 e 4) e no EDGE, na mesma escala. Os referenciais cujo critério pontua a existência de um sistema, e não uma percentagem, não entram na régua. Um mesmo projeto cruza referenciais diferentes em pontos diferentes, e é por isso que declarar a poupança obtida vale mais do que declarar a certificação pretendida.*

---

### 2.9.1. LEED v4 e v4.1, categoria Water Efficiency

O LEED é o referencial do U.S. Green Building Council (<https://www.usgbc.org/leed>, consultado a
16 de outubro de 2026), o mais difundido a nível internacional; a página oficial dá-o como o
sistema de classificação de edifícios sustentáveis mais utilizado e lista as versões v5, v4.1 e v4,
com os níveis Certified (40 a 49 pontos), Silver (50 a 59), Gold (60 a 79) e Platinum (80 ou
mais). A versão 5 coexiste com as versões 4 e 4.1; o programa enquadra o projeto nas duas, e o
estudo deve declarar qual usou. Nas versões 4 e 4.1, a eficiência hídrica ocupa uma categoria
própria, que vale oito pontos repartidos por dois créditos. A distinção fundamental que impõe é
entre uso interior e uso exterior da água, e é dessa separação que decorre toda a pontuação.

O crédito WEc1 trata da redução do uso exterior, isto é, da rega e das restantes procuras das
áreas descobertas, e vale até dois pontos. O programa concede os dois pontos com 100% de redução
do uso exterior de água potável e um ponto a partir de 50%, tomando a água da chuva destinada à
rega do próprio balanço diário; e um projeto sem procura exterior registada não pontua, situação
em que o programa regista explicitamente a razão, para que o utilizador não interprete o zero
como falha de desempenho.

O crédito WEc2 trata da redução do uso interior e vale até seis pontos, repartidos numa escala de
cinco em cinco pontos percentuais a partir de 25% de poupança. Antecede-o um pré-requisito, o
WEp2, que exige 20% de redução interior e é obrigatório: sem ele o empreendimento não é elegível
para certificação, e não confere pontuação alguma.

> A separação entre uso interior e exterior depende inteiramente da **discriminação da procura**
> descrita na secção 4.2. O programa não inventa essa separação: usa a água da chuva que o
> balanço diário destinou à rega, que é satisfeita depois do uso interior. Sem procura exterior
> discriminada, o crédito WEc1 aparece como não avaliado, e a poupança interior é tomada,
> por prudência, igual à poupança total.

> A etiqueta da pontuação dá apenas os pontos da categoria da água. O nível do LEED — Certified,
> Silver, Gold ou Platinum — resulta da soma de todas as categorias, e a água sozinha não o
> define.

---

### 2.9.2. LEED v5, crédito WEc2 Enhanced Water Efficiency

Na versão 5, os créditos de uso interior e exterior foram reunidos no crédito WEc2, *Enhanced Water
Efficiency*, que vale até oito pontos em construção nova e até sete em *Core and Shell*; o
programa avalia apenas a construção nova. O código WEc1 passou a designar outro crédito, *Water
Metering and Leak Detection*, de contagem setorizada e deteção de fugas, e não deve ser confundido
com o WEc1 de uso exterior do LEED v4. O pré-requisito WEp2 exige, entre outras condições, uma
redução de 20% no consumo de aparelhos sanitários e torneiras em relação à linha de base do referencial, e o
pré-requisito WEp1 exige que a fonte alternativa de água, como a cisterna pluvial, tenha um
contador próprio, separado do da rede pública. O projeto pontua por uma de duas vias: a Opção 1,
que mede a redução do uso de água do projeto inteiro, ou a soma das Opções 2 a 6, que tratam cada
parcela em separado.

<!-- tabela: **Tabela 70** — Opções do crédito WEc2 do LEED v5 a que o aproveitamento pluvial contribui -->
| Opção | O que mede | Pontuação |
| :--- | :--- | :--- |
| 1. Projeto inteiro | redução do uso de água do projeto contra a linha de base | 30% 1 ponto, e 1 ponto por cada 5%, até 65% 8 pontos; com fonte alternativa de água, cada escalão vale 1 ponto a mais, até 8 |
| 2. Louças e torneiras | redução calculada contra a linha de base do WEp2, que pode incluir fonte alternativa | 30% 1 ponto, 35% 2 pontos, 40% 3 pontos |
| 4. Uso exterior, via 2 | redução da necessidade teórica de rega | 50% 1 ponto, 100% 2 pontos |
| 6. Reutilização, via 2 | sistema de reutilização no local que sirva a rega, os autoclismos, a reposição ou o processo | 2 pontos |

O programa calcula as duas vias e adota a de maior pontuação: a Opção 1 com a poupança total, e a
soma das Opções 2, 4 e 6 com a poupança interior, a poupança exterior e a existência do sistema,
que o programa trata como o sistema de reutilização da Opção 6. O teto de oito pontos vale para
as duas. As Opções 3 e 5, de equipamentos e de água de processo, e a via 1 da Opção 4, de
paisagismo sem rega, não dependem do aproveitamento pluvial e ficam fora do cálculo. Como no
LEED v4, as reduções do referencial medem-se contra uma linha de base de caudais de aparelhos e de
rega, e não contra a procura modelada, pelo que o enquadramento é indicativo.

O aproveitamento pluvial pode ainda contribuir para o crédito SSc3, *Rainwater Management*. Pela
Opção 1, concede 1, 2 ou 3 pontos pela retenção no lote do volume correspondente ao percentil 80,
85 ou 90 das chuvas locais (70, 75 ou 80 em lote sem recuos), e 1 ponto adicional quando parte
desse volume é reutilizada, sem exceder o teto de 3 pontos; pela Opção 2, concede 3 pontos a quem
retém o acréscimo de escoamento em relação à cobertura natural do terreno. O programa não avalia
este crédito, porque depende do escoamento de todo o terreno, e não só da cobertura; a matriz de
critérios regista-o como não avaliado.

[A COMPLETAR: confirmar, no texto vigente do *LEED v4.1 BD+C* e do *LEED v5 BD+C Rating System*, os
limiares e as pontuações dos créditos WEc1, WEc2 (v4) e WEc2 (v5), e o crédito SSc3. A página
<https://www.usgbc.org/leed> confirma o sistema, as versões e os níveis, mas não os créditos.]

---

### 2.9.3. EDGE, o único que não pontua

O EDGE, desenvolvido pela International Finance Corporation (IFC) do Banco Mundial, segue uma
lógica distinta da de todos os anteriores. Em vez de atribuir pontos a desempenhos crescentes, mede
a percentagem de poupança contra um caso-base local em três dimensões independentes — energia,
água e energia incorporada nos materiais — e exige que **cada uma** delas cruze o limiar
estabelecido. Não há compensação entre dimensões: um desempenho hídrico excecional não supre uma
deficiência na energia.

O EDGE tem ainda dois níveis acima do primeiro. O **EDGE Advanced** exige, além dos 20% nas três
dimensões, uma poupança de energia de pelo menos 40% no local; o **Zero Carbon** exige o anterior
mais 100% de energia renovável, no local ou fora dele, ou a compra de compensações de carbono para
completar os 100%. Os níveis e os requisitos conferem com a página oficial do EDGE
(<https://edgebuildings.com/certify/certification/>, consultada a 16 de outubro de 2026).

Vale notar qual é a barra que o nível avançado eleva. ==O EDGE Advanced sobe a exigência de
energia, e não a de água.== A consequência prática para quem projeta sistemas pluviais é que o
sistema garante a barra hídrica com relativa folga, ao passo que o nível de certificação
alcançado se decide inteiramente fora do âmbito do projeto de água. O programa avalia apenas a
barra de água, pela medida WEM14, cuja entrada na aplicação do IFC é a área de captação em metros
quadrados.

> **O limite honesto está no denominador.** O caso-base do EDGE é local, varia com o país e com a
> tipologia, e é fixado pela própria aplicação do IFC. O programa aceita o caso-base declarado
> pelo utilizador; na sua ausência, adota a procura modelada do projeto e adverte que a
> percentagem resultante é um **piso**, e não o valor que a certificação reconhecerá.
>
> As barras de energia e de energia incorporada nos materiais estão fora do alcance do programa,
> que declara essa limitação no relatório. Afirmar que um projeto é EDGE Certified dispondo de um
> terço da evidência necessária seria irresponsável.

[A COMPLETAR: confirmar com o guia da medida WEM14 da aplicação EDGE a definição da medida e o
dado de entrada; a página de certificação não a descreve.]

---

### 2.9.4. GRI 303

A Global Reporting Initiative não é um referencial de certificação de edifícios, mas uma norma de
divulgação empresarial de desempenho socioambiental. A sua série 303 trata da água e dos efluentes
(<https://www.globalreporting.org/standards/standards-development/topic-standard-project-for-water-and-effluents/>,
consultada a 16 de outubro de 2026), e dois dos seus indicadores são alimentados diretamente pelos
resultados do programa: o GRI 303-3, que reporta a captação evitada em metros cúbicos por ano e
acumulada ao longo do período, e o GRI 303-5, que exprime a taxa de circularidade hídrica do
empreendimento.

[A COMPLETAR: confirmar, no texto do GRI 303:2018, a redação exata das divulgações 303-3 e 303-5; a
página consultada apresenta o projeto da norma, não as divulgações.]

---

### 2.9.5. Referenciais nacionais e europeus fora do programa

O programa não avalia estes referenciais. Descrevem-se aqui só os factos verificados nas páginas
oficiais, para que o utilizador saiba onde procurar os requisitos.

**ANQIP.** A Associação Nacional para a Qualidade nas Instalações Prediais
(<https://www.anqip.pt>, consultada a 16 de outubro de 2026) certifica produtos, sistemas de
águas pluviais e de águas cinzentas, e instalações hidráulicas prediais (CertIHP, certificação
voluntária). A página de produtos certificados (<https://www.anqip.pt/pt/produtos-certificacao>)
exibe a **etiqueta de eficiência hídrica**, com classes por produto: de A++ a B nos autoclismos e
de A+ a D nos chuveiros. A especificação técnica ANQIP ETA 0701, de sistemas de aproveitamento de
águas pluviais em edifícios (SAAP), é a referência portuguesa de projeto para usos não potáveis; a
certificação da instalação rege-se por uma especificação própria, a ETA 0702.

[A COMPLETAR: as indicações sobre a ETA 0701 e a ETA 0702 vêm de documentos de versões antigas
(validade 2009 a 2014) obtidos por pesquisa; confirmar na ANQIP a versão vigente de ambas, o
âmbito da certificação do SAAP e as classes em vigor da etiqueta de eficiência hídrica.]

**LiderA.** Sistema voluntário que orienta e certifica ambientes construídos sustentáveis, com
vinte áreas e uma escala de classes de A++ a E (<https://lidera.info>, consultado a 16 de outubro de
2026).

[A COMPLETAR: critérios e indicadores de água do LiderA (a página inicial não os lista; ver as
especificações da versão 4 no mesmo sítio).]

**BREEAM.** Método de avaliação da sustentabilidade do ambiente construído, associado ao grupo BRE
(<https://breeam.com>, consultado a 16 de outubro de 2026).

[A COMPLETAR: critérios de água do BREEAM aplicáveis ao aproveitamento pluvial, níveis de
classificação e versão aplicável em Portugal; a página consultada não os apresenta.]

**Level(s).** Quadro europeu voluntário de indicadores de sustentabilidade de edifícios de
escritórios e residenciais, do Centro Comum de Investigação da Comissão Europeia. O indicador 3.1,
consumo de água na fase de utilização (m³ por ocupante e por ano), traz uma lista de verificação
de projeto que inclui o aproveitamento de águas pluviais e a reutilização de águas cinzentas
(manual do utilizador, versão 1.1, janeiro de 2021:
<https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2021-01/UM3_Indicator_3.1_v1.1_31pp.pdf>).

[A COMPLETAR: confirmar se existe versão mais recente do manual do indicador 3.1.]

> **Declare-o no estudo.** O enquadramento só é defensável com a versão vigente do referencial à
> mão, e o programa não substitui essa verificação.

---

### 2.9.6. O que declarar

Qualquer estudo que reporte enquadramento em sistemas de certificação precisa de explicitar quatro
pontos, e a omissão de qualquer um deles compromete a verificabilidade do resultado. O primeiro é
que as classes 2 a 4 de qualidade da água adotadas pelo programa são adaptações internas, e não
classes de uma norma. O segundo diz respeito ao EDGE, e consiste em declarar que apenas a barra de
água foi avaliada, identificando o caso-base utilizado. O terceiro aplica-se ao LEED, e consiste
em declarar a versão do referencial adotada e informar se a partição entre uso interior e exterior
foi discriminada a partir de dados do projeto ou se, na falta dela, a poupança interior foi tomada
igual à poupança total. O quarto, por fim, é a ressalva geral: o enquadramento produzido pelo
programa é indicativo, e a certificação é decidida pelo organismo certificador à luz da
documentação completa do empreendimento.

---

## 2.10. Decisão multicritério

> Esta secção formaliza os dois métodos de ordenação que o programa oferece e declara três
> desvios em relação à formulação canónica que um estudo publicado precisa de citar.

A análise multicritério é o ramo da investigação operacional que trata de escolher entre
alternativas quando os critérios de avaliação discordam entre si e não se podem reduzir a um único
número sem que alguém declare o que vale mais. É exatamente a situação de um projeto de
aproveitamento pluvial: o volume que entrega mais água não é o que rende mais dinheiro, e nenhum
dos dois costuma ser o de menor impacto de carbono.

O que os métodos desta secção fazem não é descobrir a resposta certa. ==Tornam explícita a
ponderação que, de outro modo, ficaria implícita na escolha de quem decide.== É essa a diferença
toda entre um estudo que declara os seus valores e um que os esconde atrás de um resultado
aparentemente objetivo.

---

### 2.10.1. Os sete critérios

O programa avalia cada volume da varredura segundo sete critérios, agrupados em três dimensões.
Cada critério tem uma direção de preferência: em uns, mais é melhor; noutros, menos.

<!-- tabela: **Tabela 71** — Os sete critérios de decisão, a direção de preferência e o grupo de cada um -->
| # | Critério | Direção | Grupo |
| :-- | :--- | :--- | :--- |
| 1 | potencial de poupança | maximizar | técnico |
| 2 | extravasamento | minimizar | técnico |
| 3 | valor atual líquido | maximizar | económico |
| 4 | período de recuperação descontado | minimizar | económico |
| 5 | taxa interna de rentabilidade | maximizar | económico |
| 6 | CO₂e no fim da vida | minimizar | ambiental |
| 7 | consumo de água potável | minimizar | ambiental |

As alternativas submetidas à ordenação são os volumes simulados na varredura, e cada uma
comparece com os sete valores acima, calculados nas secções 2.1, 2.7 e 2.8. Não há
critério inventado nesta etapa: o método limita-se a ordenar o que as dimensões anteriores já
produziram.

---

### 2.10.2. TOPSIS

O TOPSIS — *Technique for Order of Preference by Similarity to Ideal Solution*, proposto por Hwang
e Yoon em 1981 — parte de uma ideia geométrica simples. Se cada alternativa é um ponto num espaço
de sete dimensões, uma por critério, existem dois pontos de referência: a **solução ideal**,
composta pelo melhor valor de cada critério, e a **solução anti-ideal**, composta pelos piores.
Nenhuma alternativa real ocupa qualquer deles, porque nenhuma vence em tudo nem perde em tudo, e a
melhor alternativa é a que está em simultâneo mais perto do ideal e mais longe do pior caso.

O método executa cinco passos. Monta a matriz de decisão, com as alternativas nas linhas e os
critérios nas colunas; normaliza essa matriz, para que critérios medidos em euros, em pontos
percentuais e em quilogramas passem a ocupar escalas comparáveis; aplica os pesos declarados;
identifica as soluções ideal e anti-ideal; e ordena as alternativas pela proximidade relativa ao
ideal.

```equacao:topsis:50
C_i = d_i⁻ ÷ ( d_i⁺ + d_i⁻ )
```

<!-- tabela: **Tabela 72** — Variáveis da Equação 50 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `C_i` | coeficiente de proximidade da alternativa `i`, entre 0 e 1 | adimensional |
| `d_i⁺` | distância euclidiana da alternativa `i` à solução ideal | adimensional |
| `d_i⁻` | distância euclidiana da alternativa `i` à solução anti-ideal | adimensional |

O coeficiente da Equação 50 valeria 1 para uma alternativa que coincidisse com a
solução ideal em todos os critérios, e 0 para uma que coincidisse com a anti-ideal. Como nenhuma
alternativa real ocupa esses extremos, o que interessa não é o valor absoluto do coeficiente, mas a
ordenação que ele produz.

---

Aplicado à varredura completa do projeto do tutorial (Lisboa), de 1 a 20 m³ em passos de 1 m³ e com
pesos iguais, o escore cresce até um máximo interior e decresce nos volumes maiores, em que o
investimento e o carbono incorporado passam a pesar mais do que o ganho de água
(Figura 32). O máximo da varredura completa pode diferir do volume obtido na secção
4.9 com sete candidatos, porque o ideal e o anti-ideal se constroem a partir do conjunto
avaliado: acrescentar ou retirar alternativas desloca os pontos de referência e pode alterar a
ordenação, fenómeno conhecido como inversão de ordem (*rank reversal*).

![O escore TOPSIS ao longo da varredura completa](../figuras/fig22_topsis.png)

*Figura 32 — Escore TOPSIS de cada volume da varredura do projeto do tutorial, de 1 a 20 m³, com cisterna de polietileno e pesos iguais entre os sete critérios; a estrela marca o volume de maior escore. Os custos que alimentam os critérios económicos são ilustrativos, não são preços de mercado. Figura gerada pelo próprio programa.*

---

### 2.10.3. Três desvios a declarar

A implementação do programa afasta-se da formulação canónica em três pontos, todos deliberados, e
um estudo publicado precisa de os declarar para não atribuir aos métodos originais um
comportamento que é do programa.

**A normalização é uma variante.** A formulação canónica de Hwang e Yoon emprega a normalização
vetorial, que pressupõe valores não negativos em todos os critérios. O valor atual líquido, porém,
é com frequência negativo nos volumes pequenos, em que o investimento não se paga. O programa
contorna a restrição transladando cada critério por `x − min(x)` antes de normalizar. A escolha é
necessária e deliberada, mas apresentar o resultado como TOPSIS canónico seria incorreto: declare
a variante.

**As condições de Opricovic não estão implementadas.** O método VIKOR, na formulação de Opricovic,
exige duas verificações sobre a solução de compromisso encontrada — a de vantagem aceitável e a de
estabilidade aceitável — e, quando qualquer uma falha, devolve um **conjunto** de soluções
equivalentes em vez de um único vencedor. O programa devolve sempre a melhor alternativa, sem
realizar o teste. Na prática, isto significa que a solução de compromisso do VIKOR deve ser lida
ao lado da análise de sensibilidade aos pesos, e nunca sozinha.

**A atribuição do código.** A implementação do VIKOR e do SMAA-VIKOR foi escrita de forma
independente e verificada contra a biblioteca `crispyn`, de Aleksandra Bączkiewicz. O TOPSIS foi
verificado contra a formulação original de Hwang e Yoon num caso de valores todos positivos, em que
a translação descrita acima é inócua e as duas formulações têm de coincidir.

---

### 2.10.4. SMAA-VIKOR

O SMAA — *Stochastic Multicriteria Acceptability Analysis* — existe para responder à pergunta a
que o TOPSIS não responde: e se os pesos fossem outros? Em vez de exigir um conjunto de pesos
definido de antemão, o método sorteia milhares de combinações de pesos e devolve, para cada
alternativa, a probabilidade de ocupar cada posição da ordenação.

A leitura do resultado é direta e informativa. Um volume que vence em 80% dos sorteios é uma
recomendação robusta, que não depende de uma ponderação específica para se sustentar. Um volume
que vence em 30% é uma recomendação frágil, e o texto do estudo tem de o dizer em vez de
apresentar o vencedor como se fosse consensual.

> É a ferramenta certa quando não há consenso sobre os pesos — que é o caso normal em projetos
> reais, nos quais o cliente, o projetista e a entidade licenciadora costumam valorizar dimensões
> diferentes.

---

A leitura mais útil da análise estocástica não é o vencedor, mas a margem com que vence. Um volume
que fica em primeiro lugar em três quartos dos sorteios de pesos é uma escolha estável, que
sobrevive a uma mudança de prioridades do decisor; dois volumes tecnicamente empatados indicam o
contrário, e nesse caso declarar o peso adotado deixa de ser formalidade e passa a ser a única
informação que sustenta a recomendação (Figura 33).

![A aceitabilidade de primeiro lugar de cada volume](../figuras/fig23_smaa.png)

*Figura 33 — Aceitabilidade de primeiro lugar (b¹) de cada volume candidato, obtida com cinco mil vetores de pesos sorteados no simplex. O volume destacado é o que mais vezes fica em primeiro lugar, e os restantes repartem o resto.*

#### 2.10.4.1. O tutorial, pelos dois métodos

A tabela põe lado a lado o escore TOPSIS, com pesos iguais entre as três dimensões, e a
aceitabilidade de primeiro lugar do SMAA-VIKOR, com cinco mil vetores de pesos sorteados, para os
sete volumes do tutorial de Lisboa em polietileno com reservatório superior. O investimento e o
carbono por trás dos escores são os valores ilustrativos da secção 4.7 (ilustrativo, não é
preço de mercado).

<!-- tabela: **Tabela 73** — Pontuação de proximidade TOPSIS com pesos iguais nas dimensões e aceitabilidade do primeiro lugar no SMAA-VIKOR, com 5 000 vetores de pesos aleatórios, para os volumes do tutorial -->
| Volume | Pontuação TOPSIS | Posição no TOPSIS | Primeiro lugar no SMAA-VIKOR, b¹ |
| ---: | ---: | ---: | ---: |
| 1 000 L | 0,429 | 7.º | 0,0% |
| 2 000 L | 0,549 | 6.º | 1,2% |
| 3 000 L | 0,620 | 4.º | 5,7% |
| 4 000 L | 0,673 | 2.º | 15,6% |
| 5 000 L | 0,699 | 1.º | 34,1% |
| 8 000 L | 0,665 | 3.º | 30,6% |
| 12 000 L | 0,552 | 5.º | 12,8% |

Os dois métodos concordam no vencedor, 5 000 L, e discordam na margem. O TOPSIS separa o primeiro
do segundo classificado (4 000 L) por 0,026 de escore, diferença que nenhum dado de entrada
sustenta. O SMAA mede essa fragilidade: 5 000 L vence em 34,1% dos sorteios e 8 000 L em 30,6%,
quase empatados, e com os 4 000 L (15,6%) os três somam quatro em cada cinco sorteios. Pela régua
desta secção, a recomendação é frágil, e o estudo deve declarar 8 000 L e 4 000 L como as
alternativas. Os extremos não fazem melhor: 1 000 L não vence em sorteio algum, e 2 000 L em 1,2%
deles. Nenhuma ponderação plausível recomenda o menor volume, e isso também é resultado.

---

### 2.10.5. Os pesos

O programa aceita um peso por dimensão, técnica, económica e ambiental, ou um peso por critério.
Com pesos iguais entre as dimensões, cada uma vale um terço, repartido igualmente pelos seus
critérios: os dois técnicos e os dois ambientais valem um sexto cada, e os três económicos, um
nono cada. A escolha, contudo, não é técnica: é uma declaração de valor, e por isso tem de constar
do texto do estudo. ==A afirmação «volume ótimo pelo TOPSIS», sem os pesos, é impossível de
reproduzir,== e dois estudos com pesos diferentes chegam a volumes diferentes sem que nenhum dos
dois esteja errado.

No tutorial, a escolha dos pesos desloca o resultado. Com pesos iguais, o TOPSIS recomenda 5 000 L
(com 4 000 L em segundo); com 60% no peso técnico, recomenda 8 000 L (com 12 000 L em segundo); com
60% no económico ou no ambiental, volta a 5 000 L (com 4 000 L em segundo).

Três condutas são defensáveis, e a escolha entre elas depende do que se sabe sobre as prioridades
de quem decide. Pesos iguais, declarados explicitamente como ausência de preferência, constituem a
posição neutra. Pesos justificados, com a razão de cada um, são preferíveis quando as prioridades
são conhecidas. E o SMAA, que reporta a gama de resultados em vez de um vencedor único, é a conduta
mais completa quando não há consenso.

---

### 2.10.6. Os melhores por critério isolado

Além da ordenação ponderada, o programa identifica o vencedor de cada grupo de critérios — técnico,
financeiro e ambiental — e reporta os três em separado. São números que vale a pena publicar em
conjunto, porque cada um responde a uma pergunta legítima e diferente.

Quando os três coincidem, a recomendação é forte e a decisão dispensa ponderação. Quando divergem,
que é o caso comum e o do tutorial, ==a divergência **é** o resultado:== escondê-la atrás de um
único número ponderado empobrece o estudo e transfere para o leitor uma conclusão que ele não tem
como avaliar. No tutorial de Lisboa, o critério técnico escolhe 12 000 L, o ambiental 2 000 L e o
financeiro 1 000 L (nenhum volume recupera o investimento com a tarifa de Lisboa e estes custos
ilustrativos, pelo que o critério financeiro se decide pelo valor atual líquido menos mau); o
compromisso de pesos iguais escolhe 5 000 L.

---

### 2.10.7. O que o método não faz

Convém terminar pelos limites, porque os métodos multicritério são frequentemente apresentados com
uma autoridade que não têm.

**Não escolhem os pesos.** A ponderação é do analista, e é uma decisão de valor, não de técnica.
Nenhum procedimento estatístico a substitui.

**Não validam os critérios.** Se o valor atual líquido estiver errado porque a estrutura tarifária
foi mal introduzida, o TOPSIS ordenará o erro com precisão impecável. O método ordena o que recebe.

**Não incorporam restrições.** O espaço disponível no terreno, o orçamento máximo, uma exigência
regulamentar: tudo isso são filtros anteriores à ordenação, aplicados pelo projetista ao decidir
quais volumes chegam sequer a entrar na comparação.

---

# 3. Guias disponíveis no programa

---

## 3.1. Comparar cidades

> **Pergunta a que este guia responde:** o mesmo projeto renderia o mesmo noutra cidade?

Não renderia, e a diferença não é a que a chuva sozinha sugere. A expectativa corrente é que mais chuva dê mais aproveitamento. Isso vale como ordenação, mas falha como proporção, e falha por uma razão que merece uma secção inteira.

> **As suas cidades.** O programa traz a chuva diária de 278 concelhos do Continente (E-OBS) e a série de exemplo do Funchal. Para qualquer outro local, use um ficheiro de chuva próprio, um por cidade; tudo o resto do guia vale como está escrito.

---

### 3.1.1. Como fazer a comparação

O procedimento é simples: manter todos os parâmetros do projeto e mudar apenas a série de precipitação. Na etapa **1. Projeto e Chuva**, escolha outro concelho da base ou carregue um ficheiro próprio, e execute de novo a simulação. Para comparar várias cidades sem refazer o projeto de cada vez, guarde um ficheiro por cidade, como a secção 3.6 recomenda.

---

### 3.1.2. O resultado

O projeto do tutorial — 150 m² de captação, 600 L/dia de procura, 28% de fração atendível e cisterna de 5 000 L — levado ao Porto e ao Funchal dá a tabela abaixo, ao lado de Lisboa.

<!-- tabela: **Tabela 74** — O mesmo projeto do tutorial simulado em Lisboa, no Porto e no Funchal -->
| Cidade | Chuva anual | Dias com chuva | Razão entre o mês mais e o menos chuvoso | Potencial com 5 000 L | Volume ideal |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Lisboa | 719 mm | 22% | 47,3× | 17,49% | 5 000 L |
| Porto | 1 199 mm | 31% | 9,8× | 22,04% | 5 000 L |
| Funchal | 538 mm | 42% | 14,8× | 12,98% | 4 000 L |

A Figura 34 separa as duas grandezas, cada uma na sua escala.

![Chuva anual e potencial de economia nas três cidades](../figuras/fig03_cidades.png)

*Figura 34 — (a) Precipitação média anual e (b) potencial de economia de água potável do projeto do tutorial, com 150 m² de captação, 600 L/dia de procura, fração atendível de 28% e cisterna de 5 000 L, em Lisboa, no Porto e no Funchal. O potencial acompanha a chuva anual, mas não proporcionalmente.*

---

### 3.1.3. A oferta em relação à procura, e o seu calendário

Lidas lado a lado, as colunas de chuva anual e de potencial de economia ordenam as cidades da mesma maneira, mas não andam em proporção. O Porto recebe 67% mais chuva do que Lisboa (1 199 mm contra 719 mm) e rende 4,55 pontos percentuais a mais: 22,04% contra 17,49%. Lisboa recebe 34% mais chuva do que o Funchal (719 mm contra 538 mm) e rende 4,51 pontos a mais, 17,49% contra 12,98%. Face ao teto de 28%, o Porto chega a 79%, Lisboa a 62% e o Funchal a 46%.

A explicação está em dois eixos. O primeiro é a **oferta em relação à procura**. Com 150 m² e coeficiente de 0,85, a chuva anual dá cerca de 153 m³ no Porto, 92 m³ em Lisboa e 69 m³ no Funchal, contra uma procura pluvial de 61 m³ por ano. O Porto tem 2,5 vezes o que precisa, Lisboa 1,5 vez e o Funchal pouco mais do que 1 vez. Onde a oferta sobra, a cisterna enche com facilidade e o potencial aproxima-se do teto; onde mal chega, a oferta limita-o, por maior que seja o reservatório.

O segundo eixo é o **calendário**. A tabela acima mostra-o duas vezes. A fração de dias com chuva é de 31% no Porto, 22% em Lisboa e 42% no Funchal. E a razão entre o mês mais chuvoso e o menos chuvoso, que mede quanto a chuva se concentra ao longo do ano, é de 9,8 no Porto, 14,8 no Funchal e 47,3 em Lisboa.

<!-- tabela: **Tabela 75** — Razão entre o mês mais chuvoso e o menos chuvoso nas três cidades -->
| Cidade | Razão | O que significa |
| :--- | ---: | :--- |
| Porto | 9,8× | chove o ano todo, com uma estação mais húmida marcada |
| Funchal | 14,8× | chuva frequente, mas com um verão claramente mais seco |
| Lisboa | 47,3× | **um verão quase sem chuva depois de um inverno húmido** |

Em Lisboa, o verão é o que pesa. A cisterna enche no inverno e seca na estiagem: o atendimento pleno chega a 61,3% dos dias com 5 000 L, contra 77,9% no Porto e 44,5% no Funchal com o mesmo reservatório. Um reservatório dimensionado para atravessar noventa dias de estiagem teria de armazenar noventa dias de procura pluvial, o que neste projeto são 15 120 litros — um volume que nenhuma cisterna residencial comporta. É por isso que a curva de volume de Lisboa não satura (secção 4.4) e que o sistema fica parado durante parte de cada ano.

> **A conclusão prática.** ==O potencial do aproveitamento pluvial depende de a chuva chegar, e de chegar quando é precisa.== O Porto mostra o que a abundância faz; Lisboa mostra o que um verão seco tira a uma chuva razoável; o Funchal mostra o que acontece quando a chuva, mesmo frequente, quase não excede a procura.

---

A Figura 35 apresenta o regime mensal das três cidades na mesma escala.

![O regime mensal das três cidades](../figuras/fig18_capitais.png)

*Figura 35 — Precipitação média mensal em (a) Lisboa, (b) Porto e (c) Funchal, na mesma escala; a linha a tracejado é a média mensal de cada série. Lisboa concentra a chuva no inverno e tem um verão quase seco (a razão entre o mês mais e o menos chuvoso é de 47,3); o Porto é mais repartido (9,8); o Funchal fica entre os dois (14,8). É esta distribuição, e não o total anual sozinho, que decide o comportamento do reservatório.*

---

### 3.1.4. Atenção ao Funchal

A série do Funchal é de natureza diferente das outras duas. Lisboa e o Porto usam a E-OBS, uma grelha interpolada de observações, média das células dentro do concelho. A E-OBS não dá uma série utilizável para o Funchal (faltam dados em 22% dos dias de 1991 a 2020, e o critério admite no máximo 1%), pelo que o exemplo usa a reanálise ERA5, uma célula de grelha de cerca de 9 km, e não um registo de estação. Comparar o Funchal com Lisboa e o Porto mistura, por isso, dois produtos. É a série menos fiável das três, e o seu valor serve para ilustrar o método, não para dimensionar. Num projeto real, use a série medida no local.

---

### 3.1.5. Não leve um resultado de outra cidade

A comparação acima não é peculiaridade deste tutorial, e a lição para quem compara cidades é a mesma em qualquer estudo: a série local decide, e um volume ou um potencial trazido de outra cidade, ainda que vizinha, não substitui a simulação. Um número publicado para um clima que não é o seu é uma hipótese a testar, não um resultado a adotar.

#### 3.1.5.1. Muitas cidades de uma vez

Para comparar mais de três ou quatro cidades, trocar a série à mão deixa de ser prático. A folha de cenários da secção 3.6 corre o mesmo projeto contra várias séries numa única execução, gravando um resultado por linha. Mantenha na folha os mesmos parâmetros de edifício e de reservatório em todas as linhas, e varie apenas a série: é o que isola o efeito do clima.

---

### 3.1.6. O que mais muda entre cidades

A precipitação não é a única grandeza que varia entre cidades, e as outras duas podem inverter a conclusão económica de um estudo comparativo.

A primeira é a **tarifa**. O preço do metro cúbico varia de uma entidade gestora para outra, e a estrutura também: Lisboa soma à água da EPAL o saneamento e os resíduos da Câmara Municipal; o Porto tem o tarifário da Águas e Energia do Porto; o Funchal, o da Câmara Municipal do Funchal (os três de 2026, transcritos em `triton/data/portugal_tarifarios.json`). Um potencial de 15% sob uma tarifa íngreme pode render mais dinheiro do que um de 27% sob uma tarifa baixa, e a secção 3.3 trata do mecanismo em pormenor. As cidades de exemplo levam os seus tarifários publicados, mas só o tutorial de Lisboa leva custos, pelo que este guia as compara pelo potencial de poupança, e não pelo período de recuperação. O IVA do Funchal (4%) está por confirmar; ver `examples/LEIA.md`.

A segunda é o **fator de emissão da rede elétrica**, que altera em simultâneo a emissão evitada por metro cúbico de água substituída e o custo ambiental da bombagem. Na Edição Ibérica, introduz-se em cada projeto. A eletricidade só vem tabelada para o Funchal (tarifa da Empresa de Eletricidade da Madeira, fonte secundária, a confirmar).

> **Ao comparar cidades num estudo, deixe claro o que variou.** Comparar só a precipitação, mantendo fixos a tarifa e o fator de emissão, isola o efeito climático e é uma comparação legítima, desde que declarada como tal. Variar todas as grandezas ao mesmo tempo produz um número que não se consegue explicar, porque nele se somam efeitos de sinais possivelmente opostos.

---

### 3.1.7. O volume ideal também muda, mas pouco

A última coluna da tabela guarda uma surpresa menor: com o limiar de 1 %/m³, o volume ideal é de 5 000 L em Lisboa e no Porto e de 4 000 L no Funchal, uma amplitude modesta perante a diferença de regimes que as separa.

A explicação está na natureza do critério. O volume ideal pelo ganho marginal localiza o joelho da curva de aproveitamento, e a posição desse joelho depende de como os primeiros metros cúbicos de armazenamento enchem e esvaziam contra uma procura diária de 168 L, que é a mesma nas três cidades. O que varia fortemente é o **patamar** que a curva atinge depois do joelho (17,49%, 22,04% e 12,98%), e não o ponto em que dobra. A coincidência pertence a esta casa, a este limiar e a estas três cidades; não é uma lei, e outra procura ou outro limiar podem separá-las.

Dito de outro modo: no Funchal acerta-se quase o mesmo volume que no Porto e colhe-se bastante menos água com ele.

---

## 3.2. Usar um cenário climático futuro

> **Pergunta a que este guia responde:** o sistema que dimensiono hoje ainda serve em 2060?

> **As suas projeções.** A Edição Ibérica não traz base de projeções climáticas. A base E-OBS que acompanha o programa é observada (1950 a 2025) e não contém futuro. O método deste guia aplica-se tal como está a séries projetadas que carregue como ficheiros de chuva: por exemplo, séries diárias com correção de viés de um serviço climático nacional ou de um estudo de regionalização. O guia diz o que pedir a essas séries e como compará-las. O sítio do Instituto Português do Mar e da Atmosfera (IPMA, https://www.ipma.pt, consultado em 16/10/2026) tem uma ligação para o «Portal do Clima». [A COMPLETAR: abrir o Portal do Clima e confirmar se disponibiliza séries diárias de precipitação projetada para Portugal, com que modelos, cenários e resolução, e em que condições de utilização; este manual não afirma nada sobre o seu conteúdo.]

Um reservatório de água da chuva dura trinta anos ou mais, e a chuva que cairá sobre o edifício durante esse período não será a mesma que caiu no passado recente. Dimensionar um sistema de vida longa só sobre a série histórica supõe, implicitamente, um clima estacionário — uma suposição que as projeções disponíveis não sustentam. O Triton não pode fornecer as projeções para o seu local, mas corre o mesmo projeto sobre qualquer série que lhe dê, para que o dimensionamento possa incorporar esta questão de forma explícita.

---

### 3.2.1. O que a série projetada tem de ser

Verifique quatro coisas em qualquer série projetada antes de a carregar.

**Tem de ser diária e em milímetros.** O programa lê um valor por dia, como em qualquer ficheiro de chuva (apêndice F). Projeções mensais não servem: o reservatório responde à distribuição dos dias.

**Deve ter correção de viés.** Os modelos climáticos globais têm uma resolução de dezenas a centenas de quilómetros e reproduzem mal a chuva local: tendem a errar a frequência dos dias de chuva, a intensidade e os extremos. Uma série que não tenha sido ajustada à distribuição observada vai falsear o rendimento, normalmente num sentido que não se sabe prever. A correção melhora a estatística; não transforma um mau modelo num bom, e não consegue corrigir uma tendência implausível.

**Representa uma célula de grelha, não uma estação.** A série de um lugar é a da célula que o contém, pelo que descreve a chuva média de uma área e não a de um pluviómetro. Em relevo acidentado ou no litoral, a diferença entre a célula e o lote pode ser grande. A série do Funchal que acompanha o programa é deste tipo (reanálise ERA5, célula de cerca de 9 km), e a E-OBS é uma grelha de 0,1°.

**O seu histórico é simulado.** A parte histórica de uma série de modelo não é a chuva observada, mas a simulação do modelo para esse período, corrigida para ter a mesma **estatística** que a observação. A cronologia não coincide: um dia de chuva na série do modelo não corresponde a um dia de chuva real. Por isso, a comparação certa para um cenário futuro é com o **histórico do mesmo modelo**, não com a série observada. Misturar as duas atribuiria ao clima futuro a diferença entre a observação e o modelo.

---

### 3.2.2. Escolher cenário e janela

O **cenário** representa a trajetória futura das emissões de gases com efeito de estufa. Os cenários não são previsões, mas hipóteses coerentes sobre o comportamento socioeconómico global ao longo do século (Figura 36). Uma trajetória intermédia estabiliza e depois reduz as emissões; uma trajetória intensiva em combustíveis fósseis supõe emissões altas e crescentes, sem mitigação efetiva.

![Duas trajetórias de emissão, como exemplo da forma dos cenários](../figuras/fig44_cenarios.png)

*Figura 36 — A forma de duas trajetórias de emissão típicas. A trajetória intermédia tem emissões que se estabilizam e depois caem; a intensiva em combustíveis fósseis supõe emissões altas e crescentes, sem mitigação efetiva. A figura mostra a forma de cada uma, não valores projetados.*

A **janela temporal** é o recorte da série futura sobre o qual o estudo se faz. O programa deixa recortar qualquer período, nas datas inicial e final da etapa **1. Projeto e Chuva**. A convenção mais usada é tomar janelas de trinta anos, a mesma duração das normais climatológicas; a etapa avisa quando o recorte tem menos de dez anos. A escolha da janela deve ter relação com a vida útil pretendida do sistema: avaliar um reservatório de vinte anos, instalado agora, contra o fim do século avalia um período em que já terá sido substituído.

A escolha do **modelo climático** é a mais delicada das decisões, e dedica-se-lhe adiante uma subsecção própria.

---

### 3.2.3. Como conduzir o estudo

O procedimento certo é correr o mesmo projeto em cada combinação de interesse e comparar os resultados entre si, em vez de dimensionar diretamente sobre a série projetada. Quatro passos resumem-no.

1. Feche o dimensionamento com a série **histórica**. É a referência.
2. Corra o mesmo projeto sobre o **histórico simulado** de cada modelo que for usar. É contra ele, e não contra a série observada, que o futuro se compara.
3. Mantenha todos os outros parâmetros e troque só a série, para cada cenário e janela.
4. Compare o **potencial de economia** e os **dias de atendimento pleno**, sempre como diferença entre o futuro e o histórico do mesmo modelo. O segundo costuma degradar-se mais do que o primeiro, porque o que muda primeiro é a distribuição, não o total.

> **Um exemplo de leitura.** Suponha que, com um modelo, o potencial é de 15% no histórico simulado e de 13% numa janela futura, e que a série observada dá 17%. A mudança atribuível ao clima é de dois pontos, e não de quatro: os dois pontos restantes são a diferença entre o modelo e a observação, que existe também no passado. (Os números são hipotéticos, para mostrar a aritmética.)

> **O que não fazer.** Dimensionar diretamente sobre a série futura e apresentar o resultado como projeto. A série futura é uma projeção com grande incerteza; serve para testar a **robustez** de um dimensionamento feito sobre o histórico, não para o substituir.

---

### 3.2.4. A escolha do modelo, e porque pesa tanto

Modelos climáticos diferentes projetam futuros diferentes para a mesma cidade sob o mesmo cenário de emissões, e essa dispersão não é ruído a eliminar: é a expressão honesta da incerteza física do problema. Para a chuva, a dispersão entre modelos costuma ser maior do que a diferença entre cenários de emissão, o que significa que a escolha do modelo pode pesar mais no resultado do que a escolha do futuro socioeconómico. A consequência para o projeto é direta: correr os dois cenários com um só modelo informa menos do que correr um cenário com vários modelos.

Três condutas são defensáveis perante esta dispersão, apresentadas aqui por ordem decrescente de rigor.

**Conjunto.** Corra todos os modelos disponíveis e reporte a gama de resultados, com a mediana. É o mais rigoroso e o mais caro em tempo de cálculo. A secção 3.6 mostra como fazê-lo em lote.

**Subconjunto justificado.** Escolha alguns modelos com bom desempenho documentado para a sua região, e declare o critério de escolha e a fonte.

**Modelo único, declarado como tal.** Aceitável numa análise exploratória, desde que o texto não apresente o resultado como uma projeção robusta.

> **O que nunca fazer:** correr vários modelos, escolher o que dá o resultado mais conveniente e reportar só esse.

---

### 3.2.5. O que as três cidades sugerem sobre um clima futuro

Os estudos que simulam sistemas de aproveitamento pluvial sob projeções climáticas tendem a concordar num ponto: a mudança no total anual de chuva importa menos do que a mudança na sua **distribuição**. A secção 3.1 mostra o mesmo no espaço: Lisboa tem 60% da chuva do Porto e uma razão de 47,3 entre o mês mais e o menos chuvoso, contra 9,8 no Porto, e o seu potencial é de 17,49% contra 22,04% com o mesmo reservatório de 5 000 L. Um clima futuro com estiagens mais longas comporta-se, para o reservatório, como uma mudança de cidade, e um reservatório adequado hoje pode precisar de ser maior para dar a mesma fiabilidade. [A COMPLETAR: se se quiser apoiar esta afirmação em literatura, indicar estudos sobre aproveitamento pluvial sob projeções climáticas com fonte aberta (DOI); este manual não os cita.]

---

### 3.2.6. O que declarar

Um estudo com cenário climático tem de indicar, no método:

- o **modelo ou modelos**, pelo nome, e o critério de seleção;
- o **cenário**;
- a **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve regionalização ou correção de viés, e com que método, contra que conjunto observado;
- a **origem da série**, com a versão;
- que o futuro foi comparado com o **histórico simulado do mesmo modelo**.

Sem isto, o resultado não é reproduzível.

---

### 3.2.7. Uma ressalva de método

As projeções climáticas carregam duas incertezas sobrepostas, de natureza diferente: a do cenário, que é socioeconómica e diz respeito a escolhas humanas futuras, e a do modelo, que é física e diz respeito à representação do sistema climático. Nenhuma se reduz com mais simulações do mesmo material, porque não é uma incerteza de amostragem.

Um estudo conduzido com honestidade apresenta o resultado como uma gama, e não como um número único, e evita conclusões que dependam da terceira casa decimal de uma projeção para 2060.

---

## 3.3. Ajustar o tarifário do seu concelho

> **Pergunta que este guia responde:** o tarifário do meu projeto é aquele em que o edifício
> é faturado, e está bem introduzido?

> **Edição Ibérica.** O programa traz transcritos os tarifários de três concelhos, Lisboa,
> Porto e Funchal, com a fonte e a data de cada um. Para qualquer outro concelho, o tarifário
> introduz-se à mão, com a mesma tabela de escalões, os mesmos códigos e os mesmos seis regimes
> de valor mínimo descritos aqui. Este guia é, por isso, também a referência para lançar
> qualquer estrutura tarifária.

Este é o guia que mais altera resultados. A estrutura tarifária decide a viabilidade
económica de um sistema pluvial mais do que qualquer parâmetro de projeto, e é também o dado
que mais vezes aparece errado nos estudos publicados sobre o tema.

---

### 3.3.1. Como se compõe a fatura de água, saneamento e resíduos

Antes de conferir um tarifário, convém perceber o que se confere. A fatura de água não é o
produto do consumo por um preço único, e cinco características distinguem-na da fatura de
eletricidade, que é a referência mais familiar para a maioria dos leitores.

**O serviço é local, e o preço também.** Cada concelho é servido por uma entidade gestora,
municipal, intermunicipal ou empresarial, e cada entidade publica o seu tarifário. Não há tarifa
nacional de água. Os três exemplos do programa mostram-no. Em Lisboa, a água é vendida pela EPAL
e o saneamento e os resíduos são cobrados pela Câmara Municipal. No Porto, a água e o saneamento
são da Águas e Energia do Porto, EM, e os resíduos ficam de fora da fatura dessa entidade. No
Funchal, os três serviços constam da tabela de taxas da Câmara Municipal.

**A tarifa é progressiva por escalões de consumo.** O metro cúbico não custa o mesmo em
qualquer quantidade: o consumo divide-se em escalões, e cada escalão tem preço próprio,
crescente. Em Lisboa, os primeiros 5 m³ de água custam 0,4634 €/m³ e o escalão acima de 25 m³
custa 2,5961 €/m³, antes de IVA. ==A progressividade torna a poupança de água mais valiosa do que
parece:== o metro cúbico que se deixa de consumir é o do escalão mais alto atingido na fatura, o
mais caro.

**Há uma parte que não depende do consumo.** As três entidades cobram uma tarifa fixa mensal,
mesmo a quem não consome nada: a água de Lisboa tem 5,82 €/mês, a do Porto 3,726 €/mês
(0,1242 €/dia, em meses de 30 dias) e a do Funchal 4,12 €/mês. É o assunto da secção sobre os
seis regimes, adiante.

**O saneamento e os resíduos cobram-se sobre a água.** Nos três concelhos, a parte variável do
saneamento tem escalões próprios. Em Lisboa, os escalões aplicam-se ao volume recolhido, que o
tarifário fixa em 90% da água consumida. Os resíduos têm uma parte fixa e, em Lisboa e no
Funchal, uma parte indexada ao volume de água. Poupar um metro cúbico de água poupa também estas
parcelas, e é por isso que o valor do metro cúbico poupado excede o preço da água sozinho.

**O IVA é declarado parcela a parcela.** A água de Lisboa e do Porto leva IVA de 6%, taxa que a
tabela da EPAL declara e que o tarifário do Porto não imprime. O saneamento e os resíduos de
Lisboa não levam IVA nos documentos da Câmara. No Funchal, o programa aplica 4% a todas as
parcelas, valor ainda **por confirmar** (ver abaixo). Há ainda a taxa de recursos hídricos,
cobrada pela Agência Portuguesa do Ambiente e repercutida nas tarifas: no Porto entra com
0,0392 €/m³; em Lisboa, a do saneamento entra com 0,032 €/m³ recolhido.

> **O que o programa traz, e o que tem de lançar.** O tarifário transcrito cobre o
> **utilizador doméstico** no tarifário geral, com o contador de pequeno calibre. As categorias
> não domésticas existem, são públicas e constam dos documentos de cada entidade, mas o
> programa não as traz: para estudar uma escola, um comércio ou uma indústria, lance a estrutura
> da categoria correta no modo personalizado deste mesmo ecrã. A secção 3.5 mostra o
> procedimento. Os documentos de outras capitais de distrito já estão reunidos na base de fontes
> do programa, por transcrever; até lá, nesses concelhos o tarifário também se lança à mão.

---

### 3.3.2. Comece por conferir o que já está no projeto

Na etapa **1. Projeto e Chuva**, no quadro «Concelho de referência & tarifário (água, saneamento
e resíduos)», escolha o concelho. Para Lisboa, Porto e Funchal, o programa mostra as entidades
gestoras, a vigência do tarifário e as fontes, e assinala que o tarifário foi transcrito dos
documentos oficiais. Para um concelho sem tarifário transcrito, avisa que a tarifa se informa em
«Editar». Três itens merecem conferência com o documento em vigor da sua entidade gestora, e a
ordem importa, porque o primeiro invalida os restantes.

1. **a data de vigência**: os tarifários atualizam-se todos os anos;
2. **os valores dos escalões**;
3. **o regime de valor mínimo**, que é o item 3.3.4.

Havendo divergência em qualquer dos três, carregue em «Editar / Detalhar Tarifas da Cidade…» e
corrija a tabela. A correção vale para o seu projeto e fica guardada dentro do ficheiro
`.triton`, o que significa que quem receber o projeto reproduz o mesmo cálculo, com a mesma
tabela. O botão «Repor o tarifário transcrito do concelho» devolve a tabela de origem.

---

### 3.3.3. Como a tabela é construída

Cada linha da estrutura tarifária é representada no programa por uma quádrupla de valores: o
volume mínimo do escalão, o volume máximo, um valor monetário e um código. O código é o elemento
decisivo, porque é ele que diz o que aquele valor significa, e estruturas parecidas cobram de
maneiras muito diferentes conforme o código de cada linha.

<!-- tabela: **Tabela 76** — Os seis códigos de escalão tarifário e o efeito de cada um na fatura -->
| Código | O que é | Como entra na fatura |
| ---: | :--- | :--- |
| 1 ou 0 | escalão de consumo | cobra-se o preço por volume que cai **dentro** de cada escalão de consumo |
| −1 | tarifa de disponibilidade | valor fixo **somado** à parte de consumo |
| −2 | franquia retroativa | até ao volume da franquia, paga-se o valor fixo; acima dele, tarifa-se **tudo desde zero** |
| −3 | piso de pagamento | a fatura **não desce** abaixo deste valor |
| 2 | preço de base exponencial | `PB` da fórmula `PB × Cⁿ`, válido até ao máximo da linha |
| 3 | expoente da tabela exponencial | o `n` aplicado ao consumo **do mês inteiro** que cai na linha |

A água de Lisboa, tomada como exemplo, tem cinco linhas: uma de disponibilidade e quatro
escalões progressivos. O IVA de 6% é um campo à parte, aplicado sobre a soma.

```
(0,00 ; 0,00   ; 5,82   ; -1)   disponibilidade, soma sempre
(0,00 ; 5,00   ; 0,4634 ;  1)   primeiro escalão
(5,00 ; 15,00  ; 0,8666 ;  1)   segundo escalão
(15,00 ; 25,00 ; 2,0398 ;  1)   terceiro escalão
(25,00 ; 999999 ; 2,5961 ; 1)   último escalão
```

O saneamento de Lisboa tem os seus próprios escalões, aplicados a 90% do volume de água, e a
fatura de resíduos tem uma parte fixa e uma parte por metro cúbico. O programa guarda tudo isto
nos campos tarifários do projeto, e a conta mensal que o programa calcula coincide com a soma
parcela a parcela, conferida por teste.

---

### 3.3.4. Os seis regimes, e por que decidem projetos

O valor mínimo aparece na fatura de quase todas as entidades, e significa coisas **diferentes**
em cada uma. O programa distingue seis regimes:

<!-- tabela: **Tabela 77** — Os seis regimes tarifários e o que acontece ao poupar em cada um -->
| Regime | O que acontece ao poupar | Onde aparece nos exemplos |
| :--- | :--- | :--- |
| **sem mínimo** | cada m³ poupado desconta | nenhum dos três |
| **disponibilidade** | idem; a tarifa fixa mantém-se, mas não impede a poupança | Lisboa, Porto e Funchal (tarifa fixa mensal da água) |
| **fórmula exponencial** | idem; o m³ poupado vale pelo preço de base elevado ao expoente | nenhum dos três |
| **franquia no mínimo** | abaixo da franquia, poupar **não desconta nada** | nenhum dos três |
| **franquia retroativa** | acima da franquia, tarifa-se tudo desde zero | nenhum dos três |
| **piso de pagamento** | a fatura não desce abaixo do piso | nenhum dos três |

**O caso que deita abaixo um estudo.** Compare duas estruturas hipotéticas, lado a lado, para o
mesmo consumo. Os preços são números redondos em unidades monetárias (u.m.), escolhidos para
facilitar a conta; são uma ilustração, não um tarifário:

<!-- tabela: **Tabela 78** — Efeito da poupança de água na fatura em dois regimes tarifários opostos (estruturas hipotéticas, em unidades monetárias) -->
| Consumo | Estrutura A, franquia no mínimo (50 u.m. pelos primeiros 10 m³, depois 5 u.m./m³) | Estrutura B, disponibilidade (40 u.m. mais 5 u.m./m³) |
| ---: | ---: | ---: |
| 14 m³ | 70 u.m. | 110 u.m. |
| 12 m³ | 60 u.m. | 100 u.m. |
| 10 m³ | 50 u.m. | 90 u.m. |
| 8 m³ | **50 u.m.** | 80 u.m. |
| 5 m³ | **50 u.m.** | 65 u.m. |

Na estrutura A, a fatura **deixa de descer aos 10 m³**. Uma casa que consome 12 m³ e instala um
sistema que poupa 4 desce para 8 e poupa 10 u.m., e não as 20 u.m. que o preço médio de
5 u.m./m³ sugeriria. Se poupasse 7, desceria para 5 e pouparia as **mesmas** 10 u.m.: os três
metros cúbicos adicionais não valem nada.

Na estrutura B, cada metro cúbico poupado reduz a fatura, desde o primeiro.

> Correr um caso da estrutura A com os dados da estrutura B produz um período de recuperação
> que não existe. Verifique o regime antes de confiar em qualquer resultado económico.

Os três concelhos do programa pertencem todos à segunda família: em cada um, todos os metros
cúbicos poupados reduzem a fatura. Em Lisboa, para a moradia do tutorial, a fatura sem o
sistema corresponde a 18,26 m³ por mês e custa 46,25 €; com o sistema, a 15,00 m³ e 35,06 €.
A poupança é de 3,27 m³ e 11,19 € por mês, ou seja, 3,42 € por metro cúbico poupado, contra
os 2,53 € por metro cúbico que o preço médio da fatura sem sistema sugeriria. Cada metro cúbico
poupado desconta o escalão mais alto da água e as parcelas do saneamento e dos resíduos que o
acompanham.

A Figura 37 mostra as três respostas lado a lado. O que distingue os regimes não é o
preço praticado, e sim a forma da curva: ==onde a curva é horizontal, poupar água não reduz a
fatura em nada.==

![A parte da água na fatura contra o consumo, em três regimes de valor mínimo](../figuras/fig05_regimes.png)

*Figura 37 — Parte da água na fatura mensal em função do consumo, em três regimes de valor mínimo. O saneamento não entra no gráfico porque acompanha a água e apenas multiplica a curva, sem lhe mudar a forma. Na tarifa de disponibilidade e sem valor mínimo, cada metro cúbico poupado reduz a fatura desde o primeiro; na franquia no mínimo, o troço horizontal marca a gama de consumo em que poupar água não reduz a fatura.*

---

### 3.3.5. O que os três tarifários dizem, lado a lado

Os valores abaixo vêm dos documentos oficiais transcritos pelo programa (utilizador doméstico,
tarifário geral, meses de 30 dias). Servem para ver como estruturas parecidas dão contas
diferentes, e não para substituir a consulta do documento em vigor.

<!-- tabela: **Tabela 79** — Fatura mensal doméstica de água, saneamento e resíduos nos três concelhos, tarifários de 2026 transcritos pelo programa -->
| Concelho | Entidades | Fatura de 10 m³ | Fatura de 30 m³ | IVA aplicado |
| :--- | :--- | ---: | ---: | :--- |
| Lisboa | EPAL (água); Câmara Municipal (saneamento e resíduos) | 25,8683 € | 94,3767 € | 6% na água; sem IVA no saneamento e nos resíduos |
| Porto | Águas e Energia do Porto, EM | 20,2995 € | 93,3293 € | 6% na água, no saneamento e na taxa de recursos hídricos |
| Funchal | Câmara Municipal do Funchal | 17,0872 € | 67,5272 € | 4%, por confirmar |

A 10 m³, Lisboa é a mais cara; a 30 m³, Lisboa e Porto quase se igualam, porque o Porto tem
escalões superiores mais caros. Quem compara concelhos pelo preço do primeiro escalão chega a
conclusões erradas: compare faturas para o consumo do edifício.

Três dúvidas ficam registadas, por honestidade, e o programa não as esconde:

- **Lisboa.** O «Adicional C.M. Lisboa» (0,1483 €/m³) vem impresso na tabela da EPAL sem dizer
  se leva IVA; o programa trata-o sem IVA. O saneamento e os resíduos da Câmara estão tratados
  sem IVA, como os documentos declaram.
- **Porto.** A tarifa de disponibilidade de água é a da secção dos utilizadores domésticos; o
  documento repete a tabela noutra página com um valor mais alto, lido como o dos não domésticos
  por inferência do desenho da página, a confirmar com a entidade. A taxa de 6% é a reduzida do
  Continente e não vem impressa no documento. Os resíduos urbanos não constam deste tarifário e
  ficam fora da fatura.
- **Funchal.** O IVA de 4% **não foi confirmado**: com 5%, a fatura de 10 m³ passaria de
  17,0872 € para 17,2515 €. O primeiro escalão do saneamento e dos resíduos não tem valor
  impresso e foi tratado como zero. A parte variável dos resíduos foi somada à do saneamento,
  porque o programa ainda não tem campo para resíduos por escalões; no ecrã, o «saneamento» do
  Funchal inclui, por isso, os resíduos variáveis.

---

### 3.3.6. A fórmula exponencial

Algumas entidades não cobram a água por escalões. A parte da água é dada por uma fórmula:

```
Água = PB × Cⁿ + SB
```

em que `PB` é o preço de base, em €/m³; `C` é o consumo do mês, em m³; `n` é o expoente que a
**tabela de expoentes** da entidade atribui a esse consumo; e `SB` é o serviço de base, cobrado
mesmo sem consumo. Tipicamente, `n` vale 1,00 até um limiar e sobe com o consumo a partir daí.

Duas diferenças em relação aos escalões decidem o cálculo:

- **O expoente aplica-se ao consumo inteiro.** Nos escalões, cada metro cúbico paga o preço do
  escalão em que cai; na fórmula, o `n` da linha em que cai o consumo total aplica-se a todo o
  volume. Passar um limiar encarece, por isso, também os metros cúbicos abaixo dele.
- **Não há degrau de preço, há curva.** O preço médio do metro cúbico de água é `PB × Cⁿ⁻¹`:
  constante enquanto `n` vale 1 e crescente depois.

Para o aproveitamento pluvial, a consequência é que **toda a poupança desconta desde o primeiro
metro cúbico**, e desconta mais onde o expoente é maior.

Nenhum dos três concelhos do programa usa este regime. No programa, a fórmula entra na mesma
tabela de quádruplas, com dois códigos próprios: uma linha de código 2 guarda o preço de base
`PB`, e uma linha de código 3 por cada intervalo da tabela de expoentes guarda o `n`.

```
(0,00 ; 0,00   ; SB   ; -1)   serviço de base, soma sempre
(0,00 ; 999999 ; PB   ;  2)   preço de base PB
(0,00 ; 20,00  ; 1,00 ;  3)   n para o consumo em (0, 20]
...                           uma linha por intervalo da tabela de expoentes
```

No diálogo do tarifário, a estrutura aparece com o rótulo «Fórmula exponencial», as linhas
«Expoente n» podem ser editadas e o simulador mostra o cálculo `PB × Cⁿ` do consumo escolhido.
O campo do saneamento passa a «Saneamento (por m³ consumido)», e a etapa económica oferece o
mesmo modo, «Por m³ consumido», ao lado do valor fixo e da percentagem da água.

---

### 3.3.7. Quando o mínimo é diluído na tarifa

Um erro frequente ao registar tarifas: a entidade informa «fatura mínima de 50 para 10 m³», e
quem regista grava 5 por m³ até 10 m³.

A diferença é enorme. Na primeira leitura, quem consome 4 m³ paga 50; na segunda, paga 20. E,
pior para um estudo pluvial, na segunda leitura poupar abaixo de 10 m³ **desconta**, quando na
realidade não desconta.

Se registar um tarifário novo, **verifique isto**: um mínimo declarado como fatura é uma tarifa
de disponibilidade ou uma franquia, e não um preço por metro cúbico.

---

### 3.3.8. O saneamento

A percentagem de saneamento, quando existe, incide sobre a **parte da água** da fatura, e não
sobre a fatura total.

Cem por cento significa que a parte do saneamento iguala a da água, e portanto que o saneamento
é **metade da fatura**. Poupar água poupa as duas partes, e é por isso que o valor efetivo do
metro cúbico poupado é superior ao preço da água.

Os três concelhos do programa cobram o saneamento por escalões próprios, sobre o volume de água
consumido ou sobre uma fração dele (90% em Lisboa), e não por uma percentagem única. O programa
tem um modo para cada forma: percentagem da parte da água, preço por metro cúbico, e escalões
sobre uma fração do volume. Escolha o que corresponde ao documento.

---

### 3.3.9. Vigência, atualização e tabelas alternativas

Um tarifário vale desde a data do documento de onde saiu, e nem sempre há um mais recente. O
diálogo do tarifário mostra essa data em **Tabela vigente desde**, ao lado da **Data-base do
estudo**, guardada no projeto. Entre as duas, o programa aplica as atualizações que já caíram,
com a taxa de atualização configurada, e as seguintes vêm nos aniversários da vigência, e não
doze meses depois do início do estudo. É uma estimativa, porque a atualização que de facto
houve pode ter sido outra; com o tarifário atual à mão, introduza-o com a sua vigência. Um
projeto antigo, sem as datas, fica como estava.

Alguns concelhos têm mais de uma tabela residencial, por exemplo por calibre do contador. Os
três tarifários do programa são os do contador de pequeno calibre. Escolha a tabela que
corresponde ao imóvel e registe no projeto a razão. Quem tiver a fatura do próprio imóvel pode,
como sempre, introduzir a tabela.

### 3.3.10. Onde encontrar os dados

Por ordem de fiabilidade:

1. **Tarifário publicado pela entidade gestora**, em regra no seu sítio ou no do município. É o
   documento oficial e traz a data de vigência. As entidades de titularidade municipal enviam o
   tarifário à ERSAR, entidade reguladora, para parecer.
2. **Simulador de fatura** da entidade, quando existir. Bom para conferir: simule dois consumos
   e veja se a sua tabela reproduz os dois valores.
3. **Fatura real de água, saneamento e resíduos**, do próprio imóvel. É a melhor evidência, e
   permite conferir a estrutura inteira.

> **Registe sempre a data de vigência e a fonte.** Um estudo que não diz de quando é a tarifa
> não pode ser reproduzido daqui a dois anos.

---

### 3.3.11. Confira antes de confiar

Depois de montar a tabela, faça o teste que o item 3.3.7 sugere: simule dois consumos, um
dentro e outro fora do escalão mínimo, e compare com a fatura real ou com o simulador da
entidade. Os tarifários transcritos do programa foram conferidos assim: a conta de 10 m³ e a de
30 m³ de cada concelho foram refeitas à mão, só com os números impressos nos documentos.

Se os dois valores coincidirem, a estrutura está certa. Se só um coincidir, o regime de valor
mínimo está errado, e é exatamente esse o erro que mais compromete um estudo pluvial.

---

## 3.4. Modular a procura por calendário

> **Pergunta que este guia responde:** e quando o consumo não é o mesmo todos os dias?

As escolas fecham para férias, os hotéis enchem no verão e os escritórios esvaziam ao fim de
semana. Tratar qualquer um destes edifícios como se tivesse um consumo uniforme erra nos dois
sentidos ao mesmo tempo: sobrestima a procura nos períodos vazios e subestima-a nos picos.
==O erro não se compensa ao longo do ano, porque o que importa ao sistema pluvial não é o total
consumido, e sim o encontro entre o consumo e a chuva disponível nesse dia.==

---

### 3.4.1. Os quatro modos

O programa oferece quatro modos de modulação da procura, que diferem no número de valores que o
utilizador informa e na situação em que cada um se justifica (Figura 38).



![Os quatro modos de modulação da procura](../figuras/fig40_modos.png)

*Figura 38 — Os quatro modos de modulação, o que cada um pede ao utilizador e a situação em que cada um se justifica. O modo diário só faz sentido quando existe medição real, porque inventar uma série diária acrescenta precisão aparente sem acrescentar informação.*


Em qualquer um deles pode modular três coisas de forma independente: a **procura per capita**, o
**número de ocupantes** e a **fração suprível por água da chuva**.

Modular a ocupação costuma ser mais fiel do que modular a procura: numa escola em férias, não é
o aluno que bebe menos água, é que não há aluno.

---

### 3.4.2. Como preencher

Na etapa **2. Edificação e Consumo**, escolha o modo. Abre-se a tabela do período.

- Uma célula vazia ou a zero **cai para o valor constante**. É deliberado: permite modular só os
  meses que interessam e deixar o resto no valor de partida.
- Os valores podem ser digitados ou carregados de um ficheiro CSV.
- No modo diário, o primeiro dia da série de procura alinha com o primeiro dia da **série de
  chuva**. Se as duas tiverem comprimentos diferentes, a de procura é reciclada ciclicamente.

---

### 3.4.3. Por que isto muda o resultado

Modular a procura não altera apenas o total anual consumido; altera o encontro no tempo entre
oferta e procura, que é precisamente o problema que o reservatório existe para resolver. Dois
casos do manual ilustram o alcance deste efeito.

**Uma escola com perfil semanal.** Na escola do Porto do manual (300 alunos, 40 L por aluno e por
dia, procura modulada por dia da semana, reservatório de 30 000 L), o perfil semanal rende 23,03%,
contra 23,16% para a mesma procura anual repartida por igual: 0,13 pontos percentuais. O ritmo
semanal de uma escola quase nada muda neste caso. O ganho que se imagina quando a escola fecha na estação seca
exigiria um perfil mensal de escola, com períodos letivos e férias, e o manual não tem esse caso.

**Um hotel com ocupação concentrada.** No hotel de Lisboa do manual (800 m² de cobertura, 60
hóspedes, 200 L por hóspede e por dia, 45% suprível por água da chuva, reservatório de 25 000 L),
a ocupação, ilustrativa, vai de 40% em janeiro a 100% em agosto e volta a 45% em dezembro. Com a
série de chuva de Lisboa, o perfil mensal rende 10,36%, contra 11,07% para a mesma procura anual
repartida por igual (média de 8 365,1 L/dia): menos 0,71 pontos percentuais. A procura concentra-se
de junho a setembro, o verão seco de Lisboa, enquanto a chuva cai sobretudo de outubro a março. O
reservatório enche no inverno, quando o hotel está meio vazio, e esvazia-se no verão, quando a
procura é máxima e já não chove.

Os dois casos parecem diferentes, e a regra que sustentam tem duas partes. ==Uma procura repartida
ao longo do ano aproveita melhor o mesmo reservatório; uma procura concentrada em poucos meses
perde rendimento, e perde mais quando esses meses são os secos.== O hotel de Lisboa junta os dois
efeitos, concentração e desfasamento: o pico cai na estação seca, e uma só simulação não consegue
separar um do outro. Para isolar o efeito da concentração, compare o mesmo perfil deslocado seis
meses, ou contra uma procura constante.

Uma diferença de 0,71 pontos é considerável para uma alteração que não muda um único litro do
consumo anual, e é totalmente invisível a qualquer cálculo feito sobre médias, que é justamente
por isso que o Triton simula dia a dia. Os perfis estão na Figura 39, e o rendimento
de cada um, na Figura 40.

![Três perfis de procura com o mesmo consumo anual](../figuras/fig19_modulacao.png)

*Figura 39 — Perfis de procura usados na comparação, expressos como a razão entre a procura do mês e a procura média. Todos têm exatamente o mesmo consumo anual; o que muda é a forma como se reparte pelos doze meses.*

![A procura contra a chuva, e o que cada perfil rende](../figuras/fig20_tipologias.png)

*Figura 40 — (a) Perfis de procura da escola e do hotel sobre a precipitação média mensal da cidade de cada caso; (b) potencial de poupança de cada perfil contra a mesma procura anual repartida por igual. O perfil do hotel concentra a procura nos meses secos, e é essa concentração que lhe custa 0,71 pontos percentuais. A ocupação do hotel é ilustrativa.*

---

### 3.4.4. A fração suprível também pode variar

Menos óbvio e, por vezes, mais importante. Numa escola, a percentagem de uso não potável muda
entre o período letivo e as férias: nas férias mantêm-se a lavagem de pavimentos e a rega do
jardim, que são usos **inteiramente** supríveis por chuva.

Modular a fração capta isto. Manter a fração constante subestima o aproveitamento no período de
baixa ocupação.

Na tabela, a coluna «Não Potável Interno (%)» é uma percentagem, como todos os campos digitados:
28 significa 28%. No ficheiro de projeto, a mesma coluna é guardada como fração, 0,28, e a secção
4.2 explica porquê. Uma célula com um valor entre 0 e 1 fica laranja.

---

### 3.4.5. Cuidados

**Não module o que não mediu.** Uma modulação inventada acrescenta precisão aparente sem
acrescentar informação alguma, e transmite ao leitor a impressão de um rigor que os dados não
têm. Na dúvida, uma procura constante declarada com clareza é mais honesta do que um perfil mensal
arbitrado. Foi o que se fez com a ocupação do hotel: está declarada como ilustrativa.

**Declare a origem do perfil.** Pode vir de medição própria, de doze faturas mensais de água, de
uma referência bibliográfica ou de uma estimativa, e estas quatro origens não têm o mesmo peso
como prova num estudo publicado.

**Confira o total anual depois de modular.** O programa mostra a procura média diária resultante
da modulação, e a divergência entre esse valor e o que se esperava é o indicador mais rápido de
um erro de preenchimento da tabela.

---

### 3.4.6. O caminho mais simples, quando existe

Se tem **doze faturas de água** do edifício, tem o perfil mensal medido, que é a melhor fonte
possível. Divida o consumo de cada mês pelo número de dias e pelo número de ocupantes, e use o
modo mensal.

Doze faturas valem mais do que qualquer referência da literatura.

---

## 3.5. Simular escola, hospital e comércio

> **Pergunta que este guia responde:** o programa serve para edifícios não residenciais?

Serve, e serve bem para a parte hídrica. Há, porém, uma ressalva de peso quanto à parte
económica, e é preciso conhecê-la antes de o estudo começar, e não depois de concluído.

---

### 3.5.1. A ressalva: a categoria tarifária

As entidades gestoras cobram tarifários diferentes conforme a categoria do utilizador
(doméstico, comercial, industrial, Estado e outros), e as categorias não domésticas costumam
custar mais do que a doméstica. O tarifário transcrito de Lisboa, do Porto e do Funchal é o do
**utilizador doméstico**. É o certo para uma moradia e seria o errado para uma escola, um hotel ou
uma loja.

> **O que fazer, em cinco minutos.** Procure o tarifário em vigor da sua entidade gestora, que
> costuma estar no sítio dela, e localize a tabela da categoria que interessa. Lance os escalões
> no modo personalizado do diálogo do tarifário, na etapa **1. Projeto e Chuva**, com o regime de
> valor mínimo correspondente. A secção 3.3 descreve cada campo. Feito isto, o resultado
> económico passa a ser o do seu caso, e não uma aproximação doméstica.

Os dois casos não residenciais do manual, a escola do Porto e o hotel de Lisboa, mantêm o
tarifário doméstico do concelho respetivo e deixam os custos por definir: comparam chuva e
procura, não dinheiro. Tome as suas percentagens como resultados hídricos, e não leia nelas
nenhuma conclusão económica.

Declare a que categoria pertence o tarifário. Um estudo que aplica um tarifário doméstico a um
edifício não doméstico assume uma limitação, e o sentido do erro é, em regra, conservador,
porque as categorias não domésticas tendem a ser mais caras. Mas essa é uma propriedade do
documento tarifário, e tem de a verificar no seu.

---

### 3.5.2. As tipologias disponíveis

As oito tipologias do programa agrupam-se pela categoria tarifária em que a entidade gestora as
enquadra, e cada uma tem uma unidade de consumo própria (Figura 41). A unidade de
consumo muda o significado do valor per capita informado, e a categoria decide a estrutura de
escalões da fatura: simular uma escola com tarifário doméstico é um dos enganos descritos na
secção 5.1.



![As tipologias, a categoria tarifária e a unidade de consumo de cada uma](../figuras/fig39_tipologias.png)

*Figura 41 — As oito tipologias disponíveis, agrupadas pela categoria tarifária que a entidade gestora cobra. A unidade de consumo muda com a tipologia, e é ela que dá sentido ao valor per capita informado.*


---

### 3.5.3. O que muda em cada tipologia

**Escola.** É um caso favorável ao aproveitamento pluvial por duas razões que se somam. A fração
não potável do consumo é alta, porque o autoclismo domina o uso e muitas unidades não têm
duche nem cozinha. E a área de cobertura por aluno costuma ser grande, pelo que a oferta raramente
é o fator limitante.

A modulação por calendário tem, porém, um efeito que depende do clima, e convém simulá-la em vez
de supor o resultado. A escola do Porto do manual tem 1 200 m² de cobertura, 300 alunos, 40 L por
aluno e por dia, 70% suprível, uma procura modulada por dia da semana (40 L em cinco dias, 20 L e
5 L nos dias de fim de semana) e um reservatório de 30 000 L. Rende 23,03%, contra 23,16% para
uma procura constante com o mesmo total anual (média de 9 014,3 L/dia). O ritmo semanal, sozinho,
quase nada muda. Uma escola que fecha na estação seca comportar-se-ia de outro modo, e o perfil
mensal da secção 3.4 é a ferramenta para esse caso; o manual não tem um perfil mensal de
escola para citar. A secção 3.1 mostra como a distribuição da chuva muda de uma cidade para
outra.

**Hospital.** O caso mais delicado. Consumo alto e contínuo, sem sazonalidade relevante, o que é
bom para o aproveitamento. Mas a **exigência de qualidade** é outra: há usos que não admitem água
da chuva em circunstância alguma, e a torre de arrefecimento, que seria um uso ideal, exige
controlo microbiológico contra a legionela. Trate a classe de qualidade com cuidado, e não use as
classes 2 a 4 do programa como se fossem requisito normativo: são critérios adotados pelo
programa, e a exigência de cada caso é fixada pela autoridade de saúde e pela regulamentação
aplicável.

**Escritório e comércio.** Procura concentrada em dias úteis, cinco dias em sete. Module por
semana. A fração não potável é alta, porque quase todo o consumo é autoclismo, urinol e
limpeza. A fração suprível varia muito entre escritórios, mesmo dentro de uma cidade, e deve
vir do edifício estudado sempre que possível: meça-a, ou levante-a como se descreve adiante,
antes de tomar um valor de uma referência.

**Hotel.** Sazonalidade forte, e é o caso em que modular por mês mais importa. Veja o hotel de
Lisboa da secção 3.4: com a ocupação concentrada no verão seco, rende 10,36%, contra 11,07%
para a mesma procura anual repartida por igual, uma perda de 0,71 pontos percentuais. Uma procura
concentrada desperdiça capacidade do reservatório, e a perda é maior quando a concentração cai na
estação seca. A ocupação desse hotel é ilustrativa.

---

### 3.5.4. De onde tirar a fração não potável

A fração suprível é o teto do potencial de poupança, como a secção 2.3 mostra, e é por isso
o parâmetro que mais pesa no resultado de um edifício não residencial. Há três caminhos para a
obter, por ordem decrescente de fiabilidade.

**Medição dos usos finais.** Contadores setoriais ou registadores de caudal nos ramais, durante
algumas semanas representativas. É o único caminho que produz um número do edifício, e não de uma
média.

**Levantamento por entrevista e caudal.** Pergunte aos ocupantes a frequência e a duração de cada
uso e multiplique pelos caudais medidos dos aparelhos. Custa pouco e capta o comportamento real
do edifício, mas depende da memória dos entrevistados.

**Valor de referência da literatura.** Aceitável num estudo preliminar, desde que a referência
seja da mesma tipologia, do mesmo país e, idealmente, da mesma região. Evite transpor frações
residenciais para outras tipologias, e mesmo entre habitações a variação é grande: a quota do
autoclismo numa casa difere muito da de um escritório ou de uma escola.

> **Declare o caminho.** «Fração suprível de 60%, medida» e «fração suprível de 60%, de
> referência» são estudos diferentes, e o leitor precisa de saber qual dos dois está a ler.

---

### 3.5.5. Contagem individual e o número de frações autónomas

Num edifício multifamiliar com contagem individual, informe o **número de frações autónomas**.
O programa avalia o consumo ao nível de **uma** unidade e multiplica pelo número de frações.

Isto importa por causa dos escalões progressivos: um prédio de vinte apartamentos com contagem
individual paga vinte faturas no primeiro escalão, e não uma fatura que soma todo o consumo e
cai no escalão mais caro. Tratar o prédio como uma só unidade sobrestimaria grosseiramente a
poupança.

---

### 3.5.6. O que declarar

Além do que a secção 4.10 já pede:

- a **tipologia** e a unidade de consumo adotada;
- a **origem** do consumo per capita: medição, referência ou norma;
- a **categoria tarifária** introduzida, e se é aquela em que o edifício é faturado;
- o **perfil de modulação** e a sua origem;
- para um hospital, a classe de qualidade adotada e o que ela cobre.

---

## 3.6. Comparar muitos casos de uma vez

> **Pergunta que este guia responde:** como comparar dezenas de alternativas sem refazer o
> projeto inteiro para cada uma?

O programa foi construído para comparar alternativas, e oferece três formas distintas de o
fazer. A escolha entre elas não é questão de gosto: cada forma responde a uma pergunta diferente,
e usar a errada gasta tempo sem produzir a informação desejada.

---

### 3.6.1. As três formas

<!-- tabela: **Tabela 80** — As três formas de comparar alternativas conforme o que varia entre elas -->
| Se o que muda é | Use | Onde |
| :--- | :--- | :--- |
| **só o volume da cisterna** | a varredura | etapa 4. Reservatório & Custos |
| **o volume, e quer decidir** | a tabela multicritério | etapa 8. Decisão Multicritério |
| **qualquer outro pressuposto** | projetos guardados, um por caso | ficheiro `.triton` |

A primeira é automática, a segunda também, e a terceira exige organização.

---

### 3.6.2. A varredura: dezenas de volumes de uma só vez

Na etapa **4. Reservatório & Custos**, escolha o modo **varredura** e informe o volume máximo e
o passo. O programa simula todos os volumes da grelha e desenha a curva.

A varredura é o modo normal de trabalho, e não uma função avançada reservada a casos especiais:
é quase sempre a resposta certa, porque «que volume adotar?» é a pergunta central de todo o
projeto de aproveitamento pluvial. A secção 4.4 percorre uma varredura completa passo a
passo, e a secção 2.2 formaliza como se constrói a grelha de volumes.

O custo computacional é modesto e não justifica hesitação: uma varredura de 0 a 20 000 L com
passo de 1 000 L corresponde a vinte e uma simulações de trinta anos cada, e conclui-se em poucos
segundos num computador comum.

---

### 3.6.3. A tabela multicritério: todos os volumes, todas as dimensões

A etapa **8. Decisão Multicritério** mostra, numa só tabela, cada volume da varredura com:

- a poupança de água e os dias de abastecimento;
- o valor atual líquido, o período de recuperação descontado e a taxa interna de rentabilidade;
- o carbono líquido no fim da vida útil e o retorno ambiental;
- a pontuação TOPSIS e a aceitabilidade SMAA-VIKOR.

É a forma mais densa de comparar alternativas que o programa oferece: dez colunas de resposta
para cada linha de volume. O **perfil de decisão** troca os pesos das dimensões e reordena a
tabela no momento. A secção 2.10 explica os métodos por trás.

---

### 3.6.4. Quando muda outra coisa que não o volume

Cidade, tarifário, procura, material do reservatório e tipologia do edifício são parâmetros que
a varredura não percorre, e para variar qualquer um deles o caminho é manter um projeto guardado
por caso. O procedimento abaixo parece burocrático à primeira vista e poupa horas de trabalho
repetido, sobretudo quando o estudo é retomado semanas depois.

1. Construa o projeto completo uma vez, com todo o pormenor.
2. Guarde-o com um nome que descreva o caso: `escola_porto_30000.triton`.
3. Mude **uma** coisa, e guarde-o com outro nome.
4. Corra cada um e anote o resultado numa folha de cálculo sua.

Os ficheiros de exemplo do manual foram feitos assim: `02_porto.triton` e `03_funchal.triton`
são a mesma moradia do tutorial de Lisboa (`01_tutorial_lisboa.triton`), com a série de chuva e o
tarifário trocados. É o que a secção 3.1 compara. (Trocar a cidade troca duas coisas ao
mesmo tempo; o manual fá-lo de propósito, porque o tarifário não altera o resultado hídrico, e o
resultado hídrico é o objeto da comparação.)

> **Mude uma coisa de cada vez.** Se trocar a cidade e o tarifário em conjunto, o resultado
> muda e não há como saber qual dos dois o moveu. Parece óbvio, e é o erro mais comum nos estudos
> comparativos.

---

### 3.6.5. Como organizar os ficheiros

Uma convenção de nomes poupa mais tempo do que parece:

```
estudo_escola/
   base.triton
   cidade_porto.triton
   cidade_lisboa.triton
   tarifa_nao_domestica.triton
   procura_medida.triton
   resultados.xlsx
```

E três hábitos que evitam trabalho repetido:

**Guarde o projeto, e não só o resultado.** O `.triton` traz a chuva dentro de si e reproduz o
estudo inteiro; a folha de cálculo de resultados, não.

**Anote no nome do ficheiro o que muda.** Seis meses depois, `teste3.triton` não quer dizer
nada.

**Exporte para folha de cálculo no fim de cada ronda.** A etapa **10. Exportação** grava as
tabelas em `.xlsx`, e é aí que se monta a comparação entre casos.

---

### 3.6.6. Quantos casos cabem

O programa não impõe limite ao número de casos comparados, e o limite real é a paciência do
analista: cada simulação de trinta anos demora frações de segundo, mas montar e conferir cada
projeto demora minutos, e é a conferência que consome o tempo.

Na prática, um estudo comparativo bem conduzido reúne entre cinco e vinte casos. Quando o número
cresce muito para além disso, costuma ser sinal de que a pergunta de investigação não foi
suficientemente delimitada, ou de que o trabalho é um estudo de grande escala, que pede outros
instrumentos.

Para estudos de grande escala, como matrizes fatoriais de cidade, área, procura e volume, ou a
propagação de incerteza, o programa oferece uma interface de linha de comandos, descrita a seguir.

---

### 3.6.7. A linha de comandos

A instalação do programa como pacote Python regista o comando `triton`, que executa as mesmas
rotinas de cálculo da interface gráfica sem abrir a janela; o instalador de Windows com interface
gráfica não o inclui. A linha de comandos lê ficheiros `.triton`, projetos em JSON estruturado e
um formato de texto antigo, separado por ponto e vírgula, e grava os resultados em texto, JSON,
CSV, HTML ou XLSX. É a interface indicada para estudos reprodutíveis, porque o próprio comando
documenta os pressupostos alterados.

<!-- tabela: **Tabela 81** — Subcomandos da linha de comandos e finalidade de cada um -->
| Subcomando | Finalidade |
| :--- | :--- |
| `validate` | confere a estrutura do projeto, a série de chuva e os pressupostos essenciais, sem simular |
| `run` | simula o projeto; por omissão, apenas a análise técnica |
| `analyze` | executa a cadeia completa: técnica, económica, ambiental e TOPSIS |
| `econ` | executa a análise económica |
| `init` | cria um projeto `.triton` modelo, editável, com a série de chuva referenciada ou incorporada |
| `init-catalog` | cria um catálogo JSON modelo de pressupostos de edifício ou de climas |
| `matrix` | combina um catálogo de pressupostos com um catálogo de climas e simula todas as combinações |
| `matrix-projects` | executa uma lista de projetos, uma pasta de séries de chuva ou a matriz fatorial declarada no projeto |
| `batch` | executa os cenários de uma folha de cálculo CSV ou XLSX, a partir de um projeto de base |
| `uncertainty` | propaga incertezas por Monte Carlo para um volume de reservatório |
| `series-length` | responde a quantos anos de chuva o projeto precisa, pelo método de Geraldi e Ghisi |
| `stochastic-demand` | sorteia o consumo diário e devolve o desempenho como intervalo, e não como número único |

Os subcomandos `run`, `analyze` e `econ` aceitam as mesmas opções: `--analysis` escolhe a análise
(`technical`, `economic`, `environmental`, `topsis` ou `all`); `--volume` fixa o volume do
reservatório inferior, em litros; `--rainfall` substitui a série de chuva do projeto;
`--set CAMPO=VALOR` altera um campo do projeto e pode repetir-se; `--weights` informa os pesos
técnico, económico e ambiental do TOPSIS; `--weight-sensitivity N` sorteia N vetores de pesos e
indica a frequência com que cada volume vence; `--format` e `--output` definem o formato e o
ficheiro de saída; e `--seed` fixa a semente das análises estocásticas, para que o resultado seja
reprodutível.

Aplicados ao projeto da varredura do tutorial, `validate` e `run` ficam assim (a linha de comandos
imprime a confirmação no idioma da interface do programa):

```
triton validate 04_tutorial_varredura.triton

triton run 04_tutorial_varredura.triton --volume 5000 --format json --output r.json
```

O ficheiro `r.json` regista a proveniência (projeto de origem, número de dias da série e data
inicial) e, para o volume de 5 000 L, o potencial de poupança de 17,49%, com 61,3% de dias de
abastecimento pleno.

O subcomando `uncertainty` sorteia, em cada amostra, a precipitação, a área de captação, a
procura e o investimento com uma distribuição de coeficiente de variação declarado, e indica os
percentis de 5%, 50% e 95% do potencial de poupança e do valor atual líquido, com a probabilidade
de o valor atual líquido ser positivo. Corra-o sobre o tutorial com um número modesto de amostras
e uma `--seed` fixa, e leia os percentis do potencial como um intervalo, e não como um número
único. Em Lisboa, o potencial do tutorial (17,49% a 5 000 L) está bem abaixo do teto de 28%, e a
curva ainda sobe aos 20 000 L; por isso, uma variação da chuva ou da procura desloca o potencial
mais do que deslocaria num sistema que já opera junto do teto. O valor atual líquido, negativo no
tutorial com os custos ilustrativos da secção 4.7, move-se em proporção ao investimento e ao
tarifário. A modulação probabilística, descrita nos seus capítulos próprios, faz o mesmo trabalho
a partir da interface gráfica.

O subcomando `series-length` faz, sem limite de tempo de ecrã, a análise que a etapa da varredura
oferece no botão «a série de chuva é suficientemente longa?», descrita na secção 2.2. Sem
`--windows`, percorre **todas** as janelas possíveis, que é o modo exaustivo dos artigos; com
`--windows N`, sorteia N janelas por comprimento, com a semente declarada. As opções
`--max-volume`, `--step` e `--threshold` definem a grelha e o limiar de ganho marginal, e
`--confidence` e `--tolerance` definem o critério de semelhança.

O subcomando `stochastic-demand` sorteia o consumo **dia a dia** e executa a simulação muitas
vezes, devolvendo o potencial de poupança, os dias de abastecimento pleno e o extravasamento
como intervalo entre os percentis de 5% e 95%. São dois os parâmetros de variação, e a diferença
entre eles é o que o subcomando tem para ensinar: `--daily-cv` é a variação de um dia para o
seguinte, e `--level-uncertainty` é a incerteza sobre quanto o edifício consome em média. ==O
primeiro quase não move o resultado, porque, sorteado de forma independente em cada dia,
cancela-se ao longo de uma série de trinta anos; o segundo move.== Com `--absence` declara-se a
probabilidade de um dia sem consumo nenhum, como uma viagem, e com `--ideal-volume` o programa
apura também o volume ideal de cada realização, que é o que mede se a decisão de projeto resiste
à incerteza do consumo.

Este subcomando não tem equivalente na interface gráfica, e é uma decisão de projeto: são muitos
parâmetros, a leitura exige cuidado, e no ecrã confundiriam mais do que ajudariam.

> Os subcomandos `compare-mass` e `run-vaz-study` executam estudos de investigação do grupo sobre
> bases climáticas de dezenas de milhares de séries, e exigem os ficheiros dessas bases; não fazem
> parte do uso corrente do programa.

---

## 3.7. Análise de sensibilidade

> **Pergunta que este guia responde:** que pressuposto mais move o meu resultado, e quanto aguenta
> ele?

Todo o estudo de aproveitamento pluvial assenta em pressupostos incertos, e os três mais
influentes são, em regra, justamente os menos verificáveis: o tarifário subirá mesmo 3% ao ano
durante vinte anos? A procura é de facto 150 litros por pessoa e por dia? A cisterna custará o
que o orçamento prevê?

A análise de sensibilidade mede quanto destas dúvidas chega ao resultado final. ==Não elimina a
incerteza, nem se propõe fazê-lo; mede o tamanho da incerteza,== que é exatamente a informação de
que o leitor precisa para decidir quanto confiar no número apresentado.

---

### 3.7.1. O procedimento, em três passos

O procedimento não exige ferramenta especializada, e é o mesmo que se emprega em qualquer análise
de engenharia perante um parâmetro mal conhecido: varia-se uma coisa de cada vez e observa-se o
efeito.

1. **Escolha o pressuposto** que suspeita ser o mais influente.
2. **Corra o projeto três vezes**: com o valor provável, com um valor baixo e com um alto.
3. **Anote o resultado das três** e compare.

Repita o procedimento para cada pressuposto duvidoso. No fim, terá identificado quais deles movem
de facto o resultado e quais são irrelevantes, e essa separação vale mais do que qualquer
refinamento do valor central, porque indica onde investir o esforço de recolha de dados. A secção
3.6 mostra como organizar os ficheiros para que o conjunto de execuções não se transforme em
confusão.

---

### 3.7.2. Que intervalo adotar para cada pressuposto

O intervalo de variação a adotar para cada pressuposto não é matéria de palpite: decorre do que
se sabe sobre a origem do dado, e um dado medido admite um intervalo muito mais estreito do que um
dado tomado da literatura (Figura 42). A atualização das tarifas exprime-se em
pontos percentuais por ano; os restantes intervalos, em percentagem do valor adotado.

![O intervalo de variação plausível de cada pressuposto](../figuras/fig41_premissas.png)

*Figura 42 — Intervalo de variação plausível de cada pressuposto numa análise de sensibilidade, com a origem da incerteza. Os intervalos maiores correspondem a pressupostos adotados de referência, e não medidos no projeto.*


> **Não perturbe o que conhece.** Se a área foi medida num levantamento, o intervalo é estreito;
> alargá-lo produz uma incerteza artificial que dilui o resultado e esconde o pressuposto que
> realmente importa.

---

### 3.7.3. Os pressupostos que dominam o resultado económico

Nos estudos económicos de aproveitamento pluvial, os pressupostos que mais movem o resultado são
os que atuam ao longo de todo o horizonte de análise: o próprio período de análise, o volume de
água da chuva efetivamente consumido, a taxa de atualização e a **atualização das tarifas**. A
atualização das tarifas merece atenção particular porque é a menos verificável e atua de forma
composta: cinco por cento ao ano durante vinte anos multiplicam a tarifa por 2,65; três por
cento, por 1,81; e sete por cento, por 3,87. A poupança dos últimos anos acompanha esse fator, e
a escolha da taxa pode decidir boa parte da conclusão económica do estudo.

Experimente no seu caso: na etapa **6. Resultados Económicos**, mude a atualização anual das
tarifas para 1%, anote o VAL, repita com 3% e com 5%. Três execuções, três minutos, e um
intervalo em vez de um número.

> **Num artigo, mostre esse intervalo.** Um valor atual líquido único, calculado com uma
> atualização de 3% ao ano e apresentado sem sensibilidade, sugere uma precisão que o pressuposto
> não tem.

#### 3.7.3.1. O tutorial, pressuposto a pressuposto

A tabela seguinte aplica o procedimento ao projeto final do tutorial, em Lisboa: 5 000 L em
polietileno, elevação para um reservatório superior de 1 000 L, com os custos ilustrativos do
manual (ilustrativos, não são preços de mercado). O VAL provável é negativo, de −6 079 €. A
tabela varia cinco pressupostos, um de cada vez, entre um valor baixo e um alto.

<!-- tabela: **Tabela 82** — Potencial, valor atual líquido e período de recuperação do projeto final do tutorial com cada premissa variada isoladamente, do valor baixo ao alto (os custos são ilustrativos, não são preços de mercado) -->
| Premissa | Baixo | Provável | Alto | Potencial | VAL a 20 anos (ilustrativo, não é preço de mercado) | Período de recuperação descontado |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| atualização das tarifas de água e saneamento, % ao ano | 1,0 | 3,0 | 5,0 | 17,88% a 17,88% | −6 456 € a −5 601 € | sem recuperação a sem recuperação |
| taxa de atualização mínima, % ao mês | 0,2 | 0,4 | 0,6 | 17,88% a 17,88% | −5 873 € a −6 231 € | sem recuperação a sem recuperação |
| consumo per capita, L/hab·dia | 120,0 | 150,0 | 180,0 | 19,86% a 16,23% | −7 258 € a −5 621 € | sem recuperação a sem recuperação |
| fração suprível, % | 20,0 | 28,0 | 40,0 | 14,85% a 21,03% | −6 417 € a −5 870 € | sem recuperação a sem recuperação |
| preço da cisterna, % do orçamento | 70,0 | 100,0 | 130,0 | 17,88% a 17,88% | −5 224 € a −6 934 € | sem recuperação a sem recuperação |

A primeira coisa a ler é o que **não** acontece: nenhum pressuposto, no valor baixo ou no alto,
torna o VAL positivo, e nenhum produz período de recuperação. Com o tarifário de Lisboa e estes
custos, o sistema do tutorial não se paga em vinte anos, e nenhuma dúvida isolada sobre os dados
de entrada o altera. A razão é o preço da água, baixo face ao custo da obra; não é um defeito do
exemplo. Leia o resto da tabela com isto em mente: a pergunta não é que pressuposto torna o
projeto viável, mas qual deles mais move o resultado.

**O que mais move o VAL é o preço da cisterna.** De 70% a 130% do orçamento, o VAL passa de
−5 224 € a −6 934 €, a maior amplitude das cinco (1 710 €). Quando a poupança é pequena, quem
decide o saldo é o investimento: a cisterna de polietileno de 5 000 L, de 2 850 € (ilustrativo, não é preço de
mercado), pesa nele de forma direta, ao contrário do que acontece num caso em que o sistema se
paga com folga.

**O consumo per capita vem logo atrás.** De 120 a 180 L por pessoa e por dia, o potencial desce
de 19,86% para 16,23% enquanto o VAL sobe de −7 258 € para −5 621 €, uma amplitude de 1 637 €.
Com mais consumo, a fração suprível aplica-se a uma procura maior, a cisterna falta mais vezes,
o potencial desce um pouco e a poupança em dinheiro sobe.

**Os pressupostos decididos pelo mercado pesam menos.** A atualização das tarifas desloca o VAL de
−6 456 € (1% ao ano) para −5 601 € (5% ao ano), e a taxa de atualização de −5 873 € (0,2% ao mês)
para −6 231 € (0,6% ao mês); nenhuma toca no potencial.

**A fração suprível é o pressuposto que mais move o potencial.** De 20% a 40%, o potencial vai
de 14,85% a 21,03%, mas o VAL só vai de −6 417 € a −5 870 €, porque cada ponto percentual de
poupança vale pouco em euros ao preço da água de Lisboa. É o pressuposto que a secção 4.2
fixou e que depende da decisão sobre usos, e não de medição: incluir ou não a máquina de lavar
roupa, face ao critério de qualidade aplicável ao caso, move o resultado hídrico mais do que
qualquer parâmetro económico.

O resultado contraria a intuição de quem orça antes de simular? Em parte. Aqui, cotar a cisterna
vale a pena, porque o investimento domina o saldo; mas nenhuma cotação, por favorável que seja,
inverte o sinal do VAL. Gastar tempo a definir os usos continua a ser o que mais melhora o
resultado hídrico.

---

### 3.7.4. A sensibilidade que o programa faz sozinho

Há um caso em que a análise de sensibilidade já vem pronta e não exige execuções adicionais, e diz
respeito à decisão final do estudo: a escolha do volume em função dos pesos atribuídos aos
critérios.

Na etapa **8. Decisão Multicritério**, a coluna de **aceitabilidade SMAA-VIKOR** é já uma análise
de sensibilidade pronta. Responde: se os pesos das dimensões fossem sorteados em vez de fixados,
com que frequência ficaria cada volume em primeiro lugar?

Leia-a assim:

<!-- tabela: **Tabela 83** — Leitura da aceitabilidade SMAA-VIKOR do volume vencedor -->
| Aceitabilidade do volume vencedor | O que significa |
| :--- | :--- |
| acima de 70% | recomendação robusta; os pesos quase não importam |
| entre 40 e 70% | recomendação razoável, e vale a pena declarar a segunda opção |
| abaixo de 40% | a escolha depende dos pesos, e o texto tem de o dizer |

A distinção que esta coluna permite é de natureza epistemológica, e não apenas estatística: um
volume que vence em 80% dos sorteios de pesos constitui uma recomendação, ao passo que um volume
que vence em 30% constitui uma preferência do analista, legítima desde que apresentada como tal.
No tutorial de Lisboa, o volume vencedor, 5 000 L, tem uma aceitabilidade de 34,1%, com 8 000 L
em segundo, com 30,6%, e 4 000 L em terceiro, com 15,6%: abaixo de 40%, a escolha depende dos
pesos, e o texto tem de o dizer. A secção 2.10 expõe o método que produz este número.

---

O gráfico de tornado (Figura 43) é a forma consagrada de apresentar este conjunto:
uma barra por pressuposto, ordenada pela amplitude, com as duas variações em cores distintas.
Lido de cima para baixo, responde à pergunta que o revisor fará primeiro, que é de que pressuposto
depende o resultado.

![O tornado de sensibilidade do projeto do tutorial](../figuras/fig24_tornado.png)

*Figura 43 — A variação do valor atual líquido quando cada pressuposto é alterado em 30% para mais e para menos, mantidos os restantes. A cor identifica a variação aplicada, e não o sinal do efeito: é o que permite ver que subir a taxa de atualização reduz o valor atual, ao passo que subir a tarifa o aumenta. O caso de base desta figura sai do modelo económico simplificado do programa, que desconta um fluxo anual com tarifa marginal única e atualização declarada; por isso o valor atual do caso de base não coincide com o do fluxo de caixa mensal do tutorial. O que o tornado mede é a sensibilidade relativa, e não o valor absoluto.*

---

### 3.7.5. Como apresentar

Três formas, da mais simples à mais completa:

**Tabela de cenários.** Pessimista, provável e otimista, com os pressupostos de cada um
declarados. Simples, honesta e suficiente para a maior parte dos trabalhos.

**Gráfico de tornado.** Uma barra por pressuposto, mostrando quanto o resultado varia quando ele
varia sozinho. Ordena os pressupostos por importância e é a apresentação mais informativa por
área de página.

**Distribuição.** O intervalo completo do resultado, quando todos os pressupostos variam
juntos. Exige declarar as distribuições adotadas, e não apenas os intervalos.

> **Aprofundamento: propagação por Monte Carlo.** A terceira forma faz-se sorteando milhares de
> combinações de pressupostos e acumulando a distribuição do resultado. O programa faz esta
> propagação com o subcomando `uncertainty` da linha de comandos, descrito na secção 3.6.
> Para um estudo de curso ou de projeto, a tabela de cenários do primeiro item responde à mesma
> pergunta com uma fração do esforço, e é mais fácil de defender, porque cada cenário tem
> pressupostos que se podem ler.

---

### 3.7.6. O que declarar

- os **intervalos** adotados e a origem de cada um;
- quantas execuções foram feitas, e com que valores;
- para a escolha do volume, a **aceitabilidade** do vencedor;
- **que pressupostos não foram perturbados**, e porquê.

O último é o que mais se esquece, e o que um revisor mais cobra.

---

## 3.8. Importar um projeto antigo

> **Pergunta que este guia responde:** os meus estudos antigos abrem no Triton?

Os estudos guardados no formato de texto antigo de uma ferramenta de simulação anterior abrem no
Triton, e a maior parte dos dados atravessa a conversão sem perdas. O cuidado que esta secção
pede decorre de dois factos que convivem mal: alguns campos não atravessam, e a importação não
diz quais. Um estudo reaproveitado sem conferência pode, por isso, continuar a parecer o estudo
original enquanto simula outra coisa.

---

### 3.8.1. Como importar

Basta abrir o ficheiro antigo pelo menu de abertura de projetos. O programa reconhece o formato
antigo, que é texto separado por ponto e vírgula, e converte-o para a estrutura interna da versão
atual. Feita a conversão, guarde o projeto: passa a ser gravado no formato JSON do Triton, com os
campos descritos no apêndice A, e o ficheiro original permanece intacto no disco, o que
convém preservar como prova do estudo anterior.

---

### 3.8.2. O que vem na conversão

Praticamente todo o núcleo de entrada do formato antigo tem correspondente direto na versão
atual, e é convertido sem intervenção do utilizador. A tabela seguinte indica o que a importação
recupera.

<!-- tabela: **Tabela 84** — Dados do formato antigo recuperados pela importação -->
| Dado | Vem? |
| :--- | :---: |
| ficheiro e data inicial da chuva | sim |
| área de captação, coeficiente de escoamento | sim |
| descarte das primeiras águas e modo | sim |
| procura total e número de moradores | sim |
| percentagem suprível por água da chuva | sim |
| reservatório superior, limiar de elevação | sim |
| reservatório inferior, intervalo e passo | sim |
| diferença entre potenciais | sim |
| tarifas de água e saneamento, impostos | sim |
| custos iniciais: mão de obra, tubagem, acessórios | sim |
| eletrobomba: potência, rendimento, caudal, tempo de arranque, custo | sim |
| tarifa de energia e impostos | sim |
| inflação, atualização, período de análise, taxa de atualização | sim |
| custos de exploração | sim |

---

### 3.8.3. O que não vem

> **Atenção, e confira sempre.** O leitor de ficheiros antigos **não reconhece nenhuma chave de
> procura variável**. Um projeto antigo que usasse uma procura mensal ou diária é importado como
> procura **constante**, sem aviso algum.

A consequência desta limitação merece ser explicitada, porque altera resultados sem alterar o
aspeto do projeto. Se o estudo original modulava a procura por calendário (uma escola em férias,
um hotel de época), a importação degrada-o para um consumo uniforme, e o desencontro entre oferta
e procura que a modulação representava desaparece do cálculo. No hotel de Lisboa do manual, essa
degradação transformaria 10,36% em 11,07%. Confira o modo de procura logo após importar, e
reintroduza o perfil à mão se estiver em «constante» quando não devia. A secção 3.4 mostra
como.

Há ainda um conjunto de parâmetros que não vêm por outra razão: simplesmente não existiam no
formato antigo. São a rega e a supressão da rega por chuva, a classe de qualidade da água e a
linha de tratamento, os materiais dos reservatórios e os comprimentos de tubagem por diâmetro, os
parâmetros da avaliação de ciclo de vida, a tipologia do edifício e o número de frações
autónomas. Todos assumem o valor de partida da versão atual, e todos merecem revisão antes de o
projeto importado ser considerado pronto.

---

### 3.8.4. Por que o resultado muda

Mesmo que a importação recupere na perfeição todos os dados de entrada, o resultado da simulação
pode não ser idêntico ao da ferramenta anterior. A diferença é deliberada e tem causa conhecida.

A causa principal está no **tratamento do descarte das primeiras águas**. A regra antiga trata a
lâmina de descarte como limiar do evento: quando a chuva do dia não a atinge, nada é captado;
quando a ultrapassa, capta-se a chuva inteira, sem subtração. O Triton subtrai a lâmina à
precipitação do dia, o que é fisicamente mais fiel, porque a água desviada para o dispositivo de
autolimpeza não chega, de facto, à cisterna. Com as mesmas entradas, a regra antiga devolve, por
isso, um potencial de poupança mais alto do que o Triton, e a diferença é maior onde é comum a
chuva fraca em muitos dias. A secção 6.1 trata da comparação.

---

### 3.8.5. Comparar as duas ferramentas corretamente

Quando o trabalho compara explicitamente as duas ferramentas, há um procedimento simples que
isola o comportamento do balanço hídrico da divergência metodológica deliberada, e não exige
nenhum recurso do programa: **corra ambas com descarte igual a zero**. Sem descarte, as duas
regras coincidem por construção, e qualquer diferença que sobre é atribuível à implementação, e
não ao método.

Feita essa comparação, repita-a com o descarte real do projeto, para medir a diferença total. Os
dois números, tomados em conjunto, separam o que é mudança deliberada de método do que seria uma
eventual divergência de implementação, e essa separação é justamente o que um revisor pede.

> O programa não tem opção para emular a regra antiga de descarte. Use o caminho do descarte
> zero, que produz o mesmo resultado com um pouco mais de trabalho e nenhuma surpresa.

---

### 3.8.6. Depois de importar

Sete conferências bastam para transformar um projeto importado num projeto fiável, e devem fazer-se
pela ordem abaixo, porque as primeiras afetam o resultado das seguintes.

1. **Modo de procura**: foi degradado para constante?
2. **Tipologia** do edifício: é a correta?
3. **Materiais** dos reservatórios: o valor de partida é o polietileno.
4. **Classe de qualidade** da água e tecnologia de desinfeção.
5. **Regime tarifário**: o formato antigo não distinguia os regimes de valor mínimo, e a secção
   3.3 mostra o que isso muda.
6. **Rendimento do motor** da eletrobomba, que o formato antigo não tinha.
7. **Corra o projeto e confira o potencial** com o resultado antigo antes de confiar no ficheiro
   importado.

E guarde o ficheiro original: é a prova documental do estudo anterior, e nenhuma conversão o
substitui.

---

## 3.9. Exportar para CAD, BIM e folha de cálculo

> **Pergunta que este guia responde:** como levar o resultado para o projeto de execução e para a
> análise própria?

---

### 3.9.1. O que cada formato leva

<!-- tabela: **Tabela 85** — Formatos de exportação e finalidade de cada um -->
| Formato | Extensão | O que leva | Para quê |
| :--- | :--- | :--- | :--- |
| relatório | HTML, PDF | resultado completo e pressupostos | entregar |
| folha de cálculo | XLSX | série diária e varredura | reanalisar |
| auditoria | XLSX | todos os campos dos pressupostos, do tarifário, do tratamento, da ACV, da economia e do arranjo | conferir |
| desenho | DXF | esquema hidráulico dimensionado | projeto de execução |
| manifesto BIM | JSON | componentes com tipo, posição, nível e parâmetros | importação no Revit |
| projeto | TRITON | todas as etapas e a série de chuva | reabrir e auditar |

---

### 3.9.2. O ficheiro de projeto

O formato `.triton` é o único que guarda o estudo inteiro: as nove etapas, os pesos do
multicritério, as rotas de ACV e a **série diária de chuva**, incorporada no próprio ficheiro.
Um `.triton` reabre noutro computador sem o CSV de origem e reproduz o mesmo número; é com ele
que se distribuem os casos do apêndice J. O formato CSV antigo de uma ferramenta anterior
continua disponível na exportação, assinalado como legado, porque não preserva as etapas
acrescentadas desde então.

---

### 3.9.3. Folha de cálculo

A exportação para folha de cálculo é o caminho de quem pretende fazer análise própria dos
resultados, seja para construir um gráfico que o programa não oferece, seja para combinar os
números do Triton com dados de outra origem. Estão disponíveis dois conjuntos de dados, que
respondem a perguntas diferentes.

A **série diária** traz uma linha por dia simulado, com a chuva registada, a chuva efetiva depois
do descarte, o volume captado, a procura do dia, o consumo pluvial, o consumo da rede, o
extravasamento, o volume armazenado nos dois reservatórios, o volume elevado e a classe de
abastecimento. É a base de qualquer gráfico ou estatística que o programa não ofereça pronta, e é
o que se usa quando a análise pretendida difere da que o programa faz.

A **varredura** traz uma linha por volume simulado, com todos os indicadores calculados para cada
um. É a base da curva de retorno decrescente apresentada na secção 4.4, e o formato adequado
para quem a queira redesenhar com outra apresentação.

A etapa **10. Exportação** monta a folha de cálculo a partir de seis conjuntos, que se marcam um
a um: o resumo executivo com os metadados do projeto, o balanço hídrico diário, a curva da
varredura com a fiabilidade, o fluxo de caixa ano a ano, o inventário de ciclo de vida e a matriz
de decisão multicritério. Três escolhas completam a exportação:

<!-- tabela: **Tabela 86** — Opções da exportação para folha de cálculo e quando usar cada uma -->
| Opção | Escolhas | Quando usar |
| :--- | :--- | :--- |
| formato | XLSX, CSV ou JSON | XLSX para abrir no Excel; CSV para R, Python ou outro programa; JSON para integração |
| separador do CSV | ponto e vírgula ou vírgula | ponto e vírgula no Excel em português; vírgula no R e na maior parte das ferramentas internacionais |
| filtro temporal | primeiro ano típico ou série completa | o ano para ilustrar; a série completa para qualquer estatística |
| horizonte económico | 10, 20, 25 ou 30 anos | 20 anos, uma vida útil de projeto habitual para componentes de canalização, salvo justificação em contrário |

#### 3.9.3.1. Exportar tudo, para auditoria

O botão **Exportar TUDO (auditoria)**, ao lado da exportação para folha de cálculo, grava um só
ficheiro Excel com as seis folhas acima e, além delas, folhas que ninguém escolhe: percorrem
**todos** os campos do que o programa usou. São os pressupostos do projeto, uma linha por
parâmetro, com o valor e a descrição tirada do próprio código; o tarifário aplicado, com o
significado de cada código de escalão, o regime, o modo do saneamento e a fatura para consumos de
0 a 50 m³; a linha de tratamento dimensionada na etapa da qualidade, com os estágios, as doses e
o carbono que a ACV soma; o inventário de ciclo de vida item a item; os resultados da simulação,
da economia e do multicritério; e o arranjo 3D, com cada peça, cada troço e o quantitativo por
diâmetro. A folha «0_Leia_me» diz o que há em cada uma.

É o ficheiro para quem precisa de conferir uma conta do princípio ao fim, ou de responder a um
avaliador que pergunte o que entrou no carbono ou na economia. Um parâmetro novo no programa
aparece nele sem que ninguém tenha de se lembrar de o acrescentar.

> **Um aviso de tamanho.** Trinta anos de série diária são 10 950 linhas por simulação. Uma
> varredura de doze volumes com série detalhada gera cento e trinta mil linhas. Exporte a série
> detalhada só do volume que interessa.

---

### 3.9.4. Desenho em DXF

O programa gera o esquema hidráulico do sistema dimensionado: cisterna, filtro, descarte, bomba
quando houver, reservatório superior, e a tubagem com os diâmetros adotados.

O que o programa produz é um **esquema**, e não um projeto de execução. Representa os componentes
do sistema e as ligações lógicas entre eles, com os diâmetros adotados, e serve de base para que
o projetista desenhe a instalação em planta, com as cotas, o traçado e as interferências reais do
edifício. ==Um esquema não substitui o projeto de águas, e entregá-lo como tal seria um erro de
responsabilidade técnica.==

O esquema também não traz, e o projeto de execução tem de acrescentar, os requisitos de instalação
predial para água não potável. Em Portugal, o ponto de partida para os sistemas de aproveitamento
de águas pluviais em edifícios são a especificação técnica **ETA 0701** da ANQIP (Associação
Nacional para a Qualidade nas Instalações Prediais), na versão 12 que a associação disponibiliza,
e a norma europeia **EN 16941-1**, que trata do projeto, dimensionamento, instalação,
identificação, entrada em serviço e manutenção destes sistemas para usos não potáveis. Os
requisitos habituais, a verificar nesses documentos e na regulamentação em vigor, são:

- tubagem de água da chuva identificada por cor e por inscrição de água não potável, a
  intervalos regulares nos troços à vista;
- rede de distribuição independente da de água potável, sem ligação cruzada, com separação
  atmosférica na alimentação de reserva a partir da rede pública;
- pontos de utilização de uso restrito, como a torneira do jardim, com placa de água não
  potável;
- reservatórios de água potável e não potável separados, com separação clara entre eles;
- bombagem de acordo com as regras de abastecimento de água a edifícios, que em regra pedem uma
  bomba de reserva.

[A COMPLETAR: cores, inscrições, distâncias de separação e requisitos de bombagem exatos da ETA
0701 (versão 12) e da EN 16941-1, e do regulamento nacional de distribuição predial de água; não
foram lidos nesta revisão. Ver `auditoria/pendencias_manual_prt_cap16-30.md`.]

O que o programa **não** dimensiona:

- traçado e inclinação da tubagem;
- perda de carga real da instalação;
- arranjo hidráulico do dispositivo de descarte, de que o programa calcula apenas o volume,
  `A × d_f`, e o custo;
- descarga de superfície e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

### 3.9.5. Biblioteca de blocos e manifesto BIM

Na etapa **10. Exportação**, o modo *Biblioteca de Blocos para Plantas + BIM JSON* grava os
blocos DXF dos componentes à escala 1:1, em milímetros, e, ao lado deles, o ficheiro
`*_triton-bim.json`. O programa não exporta IFC. O manifesto JSON é o contrato entre o
dimensionamento e o modelo: cada instância declara o tipo do componente, o nível, a posição local
em milímetros, a rotação e os parâmetros dimensionados, como a capacidade e o diâmetro, e a
estrutura é validada antes de ser gravada.

A integração com o Autodesk Revit faz-se por um importador distribuído com o programa, executado
no motor CPython 3 do pyRevit, com um documento aberto no Revit 2022 ou posterior, e insere as
instâncias do manifesto usando as famílias indicadas em `family_mapping.json`, que associa cada
tipo do programa (cisterna, reservatório superior, filtro, descarte inicial, grupo
eletrobomba, válvulas de seccionamento, válvula de retenção, separação atmosférica, descarga de
superfície, ponto de utilização não potável, entrada tranquilizada, aspiração flutuante,
interruptor de nível, eletroválvula, contador de água, válvula de pé com ralo, respiro e quadro
de comando) a uma família e a um tipo do gabinete.

Sem organização guardada, o programa pré-preenche o arranjo habitual destas instalações, a partir
do estudo: captação da cobertura, filtro e descarte inicial; cisterna com entrada tranquilizada,
aspiração flutuante com válvula de pé e ralo, interruptor de nível contra o funcionamento a seco,
respiro com rede e descarga de superfície com sifão e válvula antirretorno para a rede pluvial;
válvulas de seccionamento dos dois lados do grupo eletrobomba, válvula de retenção na elevação e
quadro de comando; reservatório superior com interruptor de nível, respiro com rede, descarga de
superfície com saída visível, esgoto de limpeza com válvula junto à saída e distribuição com
válvula até um ponto de utilização identificado; e o abastecimento potável de reserva (contador,
válvula e eletroválvula), que só abre quando falta água da chuva e descarrega no reservatório
superior por separação atmosférica, como a boa prática pede. Quem decide é o quadro de comando:
com o reservatório superior no nível de arranque e água na cisterna, liga a eletrobomba; com a
cisterna no mínimo, bloqueia a eletrobomba e abre a eletroválvula, que enche o reservatório só até
à bóia de reserva, mais baixa, para sobrar volume para a chuva seguinte. Eletrobomba e
eletroválvula nunca funcionam juntas. Na volumetria, os cabos de comando (dos interruptores de
nível ao quadro e deste à eletrobomba e à eletroválvula) aparecem a tracejado, e a lógica
completa está na ficha do quadro. O arranjo é um ponto de partida: posições, percursos e peças
são do projetista.

O arranjo segue duas escolhas do projeto:

- **Número de eletrobombas.** Com duas, a de reserva é desenhada em paralelo com a principal, com
  válvula de seccionamento na aspiração, válvula de retenção e válvula de seccionamento na
  elevação próprias. Liga-se às linhas da principal por tês.
- **Arranjo de abastecimento.** Muda o que existe na instalação:
  - **Elevação para reservatório superior:** é o arranjo descrito acima.
  - **Pressurização direta:** não há reservatório superior. O sobrepressor leva a água da cisterna
    diretamente ao ponto de utilização. O abastecimento potável de reserva descarrega na própria
    cisterna, também por separação atmosférica, e só até uma bóia de reserva instalada nela.
  - **Gravidade:** não há bomba. A cisterna fica sobre uma base, acima do ponto de utilização, e a
    água sai por uma saída lateral baixa com válvula. O abastecimento potável de reserva
    descarrega na cisterna, como na pressurização.

Enquanto os troços não estão organizados, o arranjo é refeito a cada mudança do volume, do
abastecimento ou do número de bombas.

Com estes dados, o programa monta também a prancha do esquema 3D, fora de escala e em folha A3 na
horizontal. Só os níveis que organizam a instalação (cisterna, reservatório superior, grupo
eletrobomba, filtro e descarte) ganham plano de cota; as peças pequenas aparecem no desenho pelo
código, e o tipo e a cota de cada uma estão na tabela «Peças e acessórios», ao lado da sequência
de montagem e do quantitativo por diâmetro.

O importador não cria famílias nem substitui componentes por aproximação: uma instância sem
família ou sem nível correspondente fica listada como pendente no fim da importação. As
coordenadas são locais, e a amarração ao ponto de base e ao norte do projeto faz-se no Revit,
pelo projetista. O manifesto serve a coordenação e o levantamento de quantidades, e não substitui
a modelação da instalação de águas.

#### 3.9.5.1. Do arranjo ao CAPEX e à ACV

O mesmo arranjo alimenta o custo e o carbono. O programa levanta, peça a peça:

- os metros de tubo por diâmetro;
- as curvas, uma por mudança de direção do percurso;
- as ligações, uma em cada extremo de percurso ligado a uma peça;
- cada peça do manifesto, por tipo;
- os metros de cabo de comando.

Cada item recebe um preço e uma massa. O preço vai para o CAPEX: tubos e ligações em *Tubagem*,
peças e cabos em *Acessórios*. A massa, vezes o fator do material, vai para a ACV na etapa A1–A3.
Cisterna, reservatório superior e grupo eletrobomba já têm linha própria nas duas análises e não
são contados de novo. O filtro e o descarte inicial entram no CAPEX pela linha de tratamento,
quando está ativa, e na ACV pelo subsistema de descarte, quando está ativo.

Um teste automático confere que nenhuma peça, nenhum metro de tubo, nenhuma curva, nenhum tê e
nenhum cabo do arranjo fica sem custo ou sem carbono. O teste cobre os três arranjos de
abastecimento, com uma e com duas eletrobombas. A folha `Auditoria_Quantitativo` do *Exportar
tudo* lista cada item com o seu destino no CAPEX e na ACV, e fecha a soma contra os valores que as
análises usaram. A mesma folha confere ainda se o arranjo é coerente com o projeto: um arranjo
organizado à mão pode ficar para trás quando o projeto muda o abastecimento ou o número de
bombas, e a divergência aparece aí.

Os preços e as massas das peças são um cenário de referência, e não uma cotação. Estão em
`costs_database.json`, na chave `pecas_do_arranjo`, e podem ser alterados aí. Na etapa económica,
o projetista pode também digitar outros valores de tubagem e acessórios: a partir daí o programa
usa os valores digitados. Um projeto novo parte do arranjo. Um ficheiro antigo mantém os custos
que já declarava. Na Edição Ibérica o programa não aplica os preços de referência da base de
custos: os custos são digitados, em euros, e os casos do próprio manual usam números redondos
declarados como ilustrativos, não como preços de mercado.

---

### 3.9.6. Relatórios

Os três da secção 4.10: executivo, ambiental com ESG, e científico. Em HTML para consulta e em
PDF para entrega.

> O programa tem dois geradores de PDF e usa o mais completo que o computador permitir. Quando
> recorre ao alternativo, o documento sai mais simples, com o mesmo conteúdo e os mesmos números.

---

### 3.9.7. Um conselho de arquivo

Ao fechar um estudo, guarde junto, na mesma pasta:

1. o ficheiro `.triton`;
2. a **série de chuva** usada, ou a sua identificação exata na base;
3. o relatório científico em PDF;
4. a folha de cálculo da varredura;
5. se houve execução em lote, o **script** com os comandos;
6. um ficheiro de texto com a **versão do programa**.

São seis itens que tornam o estudo reprodutível daqui a cinco anos. Sem eles, o relatório em PDF
é só uma afirmação.

---

# 4. Tutorial: um exemplo do começo ao fim

---

## 4.1. O projeto e a chuva

> No fim desta secção, tem um projeto criado, uma série de precipitação carregada e a captação definida. E sabe porque cada um destes três números importa mais do que parece.

As dez secções deste capítulo constroem **um só projeto**, do princípio ao fim. A cada secção o estudo ganha uma camada, e o resultado muda. Guarde o ficheiro: é o mesmo até à secção 4.10.

### 4.1.1. O projeto

Uma moradia unifamiliar em Lisboa. Quatro moradores, cobertura de 150 m², cisterna enterrada no logradouro. É um caso deliberadamente comum, para que o método se destaque, e não o edifício.

Lisboa tem três razões a favor. A série de precipitação é longa e completa: 30 anos de valores diários, de 1991 a 2020. O tarifário da água é público e verificável: a EPAL fornece a água e a Câmara Municipal cobra o saneamento e os resíduos. E o regime de chuva tem um verão muito seco, o que — como a secção 4.4 mostrará — decide a escolha do volume. A secção 3.1 leva a mesma moradia ao Porto e ao Funchal e mostra quanto muda só pelo clima.

> **O seu local.** O tutorial corre sobre a série de Lisboa e o tarifário que acompanham o programa. Num projeto real, substitua-os pela série medida no local e pela tarifa que paga, como explica a secção 4.7. O método hidráulico é o mesmo.

---

### 4.1.2. A série de precipitação

Abra a etapa **1. Projeto e Chuva**. Há dois caminhos para a chuva.

**Ficheiro próprio.** Um CSV com uma leitura diária por linha, em milímetros, numa só coluna. É o caminho de quem tem dados de uma estação concreta. A ETA 0701 da ANQIP recomenda dados de fontes oficiais, de preferência séries históricas de pelo menos 10 anos, e indica o Sistema Nacional de Informação de Recursos Hídricos (SNIRH) para as precipitações médias mensais de estações do país (item 4.1, versão 7 da ETA; ver a secção 1.1).

**Base de concelhos (E-OBS).** O programa traz a precipitação diária de 278 concelhos do Continente, de 1950 a 2025, extraída da E-OBS v33.0e. A série de um concelho é a média das células da grelha com centro dentro dos seus limites. É o caminho de quem estuda outros concelhos, e a secção 3.2 mostra como testar um cenário climático.

Para o nosso projeto, escolha o concelho de **Lisboa** e recorte os **30 anos** de 1991 a 2020.

<!-- tabela: **Tabela 87** — Caracterização da série de precipitação de Lisboa adotada no tutorial -->
| A série de Lisboa | Valor |
| :--- | ---: |
| dias na série | 10 958 |
| anos | 30,0 |
| precipitação média anual | 719 mm |
| dias com chuva | 22% |
| chuva média nos dias chuvosos | 9,0 mm |
| maior chuva diária | 91,2 mm |
| dias abaixo da lâmina de descarte | 4% |

Três números desta tabela decidem o projeto, e vale a pena olhar para eles antes de qualquer simulação.

**719 mm por ano** é pouca chuva para esta cobertura, e muito concentrada no inverno. A oferta bruta, cerca de 92 m³ por ano, é 1,5 vez a procura pluvial da casa (61 m³ por ano, secção 4.2). Há água a mais no ano, mas no momento errado: o fator limitante será o verão seco e o tamanho do reservatório, não o total anual.

**Chove em 22% dos dias.** Chuva rara obriga a cisterna a atravessar longas estiagens. Compare com o Porto, na secção 3.1, onde chove em 31% dos dias e a mesma casa poupa mais. Em Lisboa, o mês mais chuvoso recebe 47,3 vezes o que recebe o mais seco.

**Quatro por cento dos dias têm chuva, mas abaixo de 2 mm.** Esses dias serão descartados por inteiro, e o ponto sobre o descarte das primeiras águas, mais adiante, explica porquê.

> **Quantos anos de série usar.** Trinta é confortável. Abaixo de dez, o resultado começa a depender do troço escolhido; abaixo de cinco, o viés do reservatório vazio no início da simulação passa a pesar de forma sensível. A secção 5.1 trata este engano em pormenor.

---

Vale a pena olhar para uma série inteira antes de a usar. Trinta anos de Lisboa não são trinta anos parecidos: os totais variam de ano para ano, e é essa variação que a média anual apaga. A distribuição diária conta o resto da história — a maior parte dos dias não tem chuva nenhuma, e o volume anual é entregue por um número pequeno de dias intensos (Figura 44).

![Trinta anos de série, e a distribuição dos dias de chuva](../figuras/fig15_serie.png)

*Figura 44 — Série de precipitação de Lisboa usada em todo o tutorial (E-OBS, concelho de Lisboa, 1991 a 2020): (a) precipitação total de cada ano, com a média dos trinta anos em linha contínua e os anos acima da média a azul e abaixo dela a laranja; (b) distribuição de frequência da precipitação diária nos dias de chuva, em escala logarítmica, que mostra como poucos dias respondem pelos maiores volumes. O maior dia da série tem 91,2 mm.*

---

### 4.1.3. A área de captação

O projeto do tutorial adota 150 m² de área de captação, e este é o primeiro campo em que se erra com frequência.

A área de captação é a **projeção horizontal** da cobertura, não a área inclinada do telhado. Um telhado com 30% de inclinação sobre uma planta de 150 m² tem cerca de 157 m² de superfície de telha e capta, ainda assim, os mesmos 150 m² de chuva: a precipitação cai na vertical, e o que encontra é a sombra da cobertura projetada no chão. A ETA 0701 da ANQIP define-a assim: a projeção em planta do local onde é recolhida a água da chuva. É esta área `A` que entra na equação da disponibilidade.

> **Área de captação não é área de contribuição.** O dimensionamento de caleiras e tubos de queda usa outra área, para outro fim. Para dimensionar a drenagem pelo caudal de ponta de uma chuvada curta e intensa, acrescentam-se à projeção os acréscimos devidos à inclinação da cobertura e às paredes que intercetam a chuva empurrada pelo vento. Essa área sobrestima o volume que a cobertura capta ao longo do ano. No Triton, indique a projeção horizontal; a área de contribuição fica para o projeto das caleiras, que o programa não faz. A ETA 0701 remete as caleiras e os tubos de queda para o Regulamento Geral português ou para a norma europeia EN 12056-3. [A COMPLETAR: confirmar no texto do Decreto Regulamentar n.º 23/95 (Diário da República) os artigos aplicáveis ao cálculo de caudais pluviais antes de os citar por número.]

> **Atenção.** Usar a área inclinada sobrestima a captação na razão `1/cos(inclinação)`. Num telhado de 30% dá 4,4% a mais de água que não existe. Em telhados mais inclinados, o erro cresce depressa.

---

Carregada a série, o programa já mostra o regime que ela descreve. Vale a pena conferir este desenho antes de seguir: uma série trocada de concelho, ou com a unidade errada, costuma aparecer no ciclo sazonal da Figura 45 antes de aparecer em qualquer resultado.

![O ciclo sazonal médio da série carregada](../figuras/fig55_programa_sazonal.png)

*Figura 45 — O ciclo sazonal médio da série, calculado e desenhado pelo programa assim que a precipitação é carregada. Em Lisboa, o mês mais chuvoso recebe cerca de 47 vezes o que recebe o mais seco (47,3), e é esta diferença que o reservatório tem de atravessar: o verão é quase sem chuva. Figura gerada pelo próprio programa.*

---
### 4.1.4. O coeficiente de escoamento

O tutorial escreve 0,85 no campo do coeficiente. O programa, por seu lado, abre com a telha cerâmica selecionada e aplica 0,75, o valor que a lista de materiais lhe atribui, e que é também o valor que assume quando nenhum material é indicado. ==Atenção ao reproduzir o tutorial: para chegar aos números deste manual, escolha «Outro / Personalizado» e escreva 0,85.==

A origem do 0,85 merece rigor, porque é citado com frequência como coeficiente de escoamento e não o é. Em Portugal, a ETA 0701 da ANQIP escreve o volume anual aproveitável como o produto da precipitação média anual, da área de captação, de um coeficiente de escoamento inicial da cobertura `C` e da eficiência hidráulica da filtragem `ηf`. Recomenda `C` = 0,8 para coberturas impermeáveis (telha, betão, etc.), 0,6 para coberturas planas com gravilha, 0,3 para coberturas verdes extensivas e 0,5 para as intensivas, e admite `ηf` = 0,9 em filtros com manutenção e limpeza regulares (itens 4.3.1 a 4.3.3 da versão 7). O 0,85 do tutorial é, assim, um valor redondo entre estes, e não um valor de norma. O Triton tem um só campo para a fração da chuva que chega à cisterna e modela o descarte à parte, em milímetros. Escrever aí um valor que já inclua a perda do escoamento inicial e aplicar também o descarte de 2 mm conta essa perda duas vezes. Num estudo, declare o valor adotado no campo, a sua origem e o descarte, e não atribua a uma norma um coeficiente que ela não fixa.

> **A norma europeia.** A EN 16941-1 também escreve o rendimento da captação como produto de um coeficiente da superfície da cobertura e de uma eficiência do filtro. [A COMPLETAR: confirmar, na edição em vigor da EN 16941-1 (catálogo do IPQ ou do CEN), os valores tabelados antes de os citar; o manual não os reproduz.] O Triton mantém a sua lista de coeficientes e o descarte inicial; para se aproximar de uma norma, escreva o produto como valor personalizado e ajuste a lâmina de descarte.

O coeficiente de escoamento representa a fração da chuva incidente que chega, de facto, à cisterna, e a diferença até à unidade é o que se perde no caminho. As perdas têm quatro origens: a absorção pelo material da cobertura, a evaporação na superfície aquecida, o salpico para fora da caleira e a molhagem inicial da telha em cada nova chuvada. A Figura 46 mostra o coeficiente que o programa atribui a cada material de cobertura.

![O coeficiente de escoamento por tipo de cobertura](../figuras/fig35_escoamento.png)

*Figura 46 — O coeficiente de escoamento que o programa atribui a cada material da cobertura. A linha a tracejado marca 0,85, o fator de captação adotado no tutorial. A cobertura verde é a única que se afasta do grupo, porque retém parte da chuva no substrato.*


O programa aceita qualquer valor entre zero e um, e recusa valores fora deste intervalo, indicando o campo — um coeficiente maior do que a unidade significaria que a cobertura entrega mais água do que a chuva lhe traz. A etapa **11. Documentação** traz a mesma tabela, com a fonte dos valores. Para uma cobertura mista, o coeficiente a escrever é a média dos coeficientes de cada material, ponderada pelas respetivas áreas.

---

### 4.1.5. O descarte das primeiras águas

O tutorial descarta 2,0 mm em todas as chuvadas.

A primeira água que lava a cobertura leva pó, folhas, dejetos de aves e tudo o que se depositou desde a chuva anterior. Descartá-la, em vez de a conduzir à cisterna, é a medida de qualidade mais barata e mais eficaz de que um sistema pluvial dispõe, e por isso é praticamente universal em projetos bem conduzidos. Em Portugal, a ETA 0701 recomenda um dispositivo automático de desvio do escoamento inicial, tendo em conta as longas estiagens de verão, e, na falta de dados ou de estudos locais, o desvio de um volume correspondente a 2 mm de precipitação, podendo adotar-se um valor inferior em casos justificados (itens 4.2.2 e 4.2.4). É esse o valor adotado aqui. Num estudo, justifique a lâmina que adotar.

O programa oferece três modos de aplicar o descarte, que correspondem a três tipos de dispositivo de autolimpeza.

<!-- tabela: **Tabela 88** — Os três modos de aplicação do descarte de primeiras águas -->
| Modo | Quando descarta | Quando usar |
| :--- | :--- | :--- |
| 1 | em todas as chuvadas | o padrão, e o mais conservador |
| 2 | só na primeira chuvada após uma estiagem | dispositivo que não se esvazia sozinho entre chuvas próximas |
| 3 | de X em X dias | dispositivo com esvaziamento programado |

> **Atenção, e este é o ponto que mais surpreende.** Quando o descarte se aplica e a chuva do dia **não excede** a lâmina, perde-se o dia **inteiro**, não a diferença. Um dia de 1,6 mm com descarte de 2,0 mm capta **zero**.
>
> Na série de Lisboa, isto atinge 4% dos dias. Em climas de chuvisco frequente, a parcela é maior.

A razão deste comportamento é física, não convencional: o dispositivo de autolimpeza tem de encher por completo antes de qualquer água seguir para a cisterna. Quando a chuva do dia não chega para o encher, nada passa, e o volume retido perde-se para a drenagem, juntamente com a sujidade que lavou.

> **A lâmina não é o dispositivo.** `d_f` é uma lâmina em milímetros. O volume hidráulico do reservatório de autolimpeza é `A × d_f`, que no nosso projeto dá 150 × 2 = **300 litros**. A etapa **3. Qualidade & ETAP** dimensiona e orça esse reservatório (secção 2.5), e a secção 4.7 mostra o seu custo no investimento.

---

### 4.1.6. O que temos até aqui

<!-- tabela: **Tabela 89** — Estado do projeto do tutorial no fim da definição da chuva e da captação -->
| Dado | Valor |
| :--- | ---: |
| série | Lisboa, 30 anos |
| área de captação | 150 m² |
| coeficiente de escoamento | 0,85 |
| lâmina de descarte | 2,0 mm, todas as chuvadas |

Com isto, o programa já sabe **quanta água entra**. Falta dizer quanta sai, o que é a secção 4.2.

Uma conta de algibeira, para calibrar a expectativa: 719 mm por ano sobre 150 m² com coeficiente de 0,85 dão cerca de 92 m³ por ano de água bruta, antes do descarte. A secção 4.3 mostra quanto desse volume se converte em poupança efetiva — e a diferença entre os dois números é a lição mais importante do tutorial.

---

## 4.2. A edificação e a procura

> No fim desta secção, o programa sabe **quanta água sai** e, mais importante, **que parte dela a chuva pode atender**. Essa fração é o teto de tudo o que vem a seguir.

A secção 4.1 definiu a oferta. Esta define a procura. E há uma assimetria que convém perceber desde já: **a chuva não pode atender toda a procura**, por mais água que haja. Existe um teto, é definido aqui, e nenhum reservatório o ultrapassa.

---

### 4.2.1. A tipologia

Na etapa **2. Edificação e Consumo**, escolha *Residencial unifamiliar*. O programa traz oito tipologias, cada uma com o consumo per capita de referência (Figura 47) e a repartição habitual dos usos finais. A indústria não tem gama de referência, porque o consumo depende do processo produtivo e não da ocupação: nesse caso, o valor tem de vir de medição.

![O consumo per capita de referência por tipologia](../figuras/fig38_per_capita.png)

*Figura 47 — As gamas habituais de consumo per capita por tipologia de edifício. A amplitude de cada gama é grande de propósito: são valores de referência para quem ainda não mediu, e a medição, quando existe, prevalece sempre.*


A tipologia é um ponto de partida, não uma imposição: o valor continua editável. A secção 3.5 trata dos casos não residenciais, que têm uma armadilha própria na tarifa.

---

### 4.2.2. Os moradores e o consumo

**Quatro moradores, 150 L/hab·dia.** Total de **600 L/dia**.

O valor de 150 L/hab·dia é uma referência redonda para uma moradia com abastecimento regular, não uma medição. Se tem a fatura da água e do saneamento do edifício, use-a: divida o consumo mensal, em litros, por trinta e pelo número de moradores. O número medido vale mais do que qualquer referência.

O programa aceita procura **constante** ou modulada por semana, mês ou dia. O tutorial usa a constante; a secção 3.4 mostra a modulação, que importa em escolas, hotéis e em qualquer edifício com sazonalidade.

---

### 4.2.3. A fração que a chuva pode atender

**28%.** É o número mais importante desta secção.

A água da chuva não vai para o duche, para a pia da cozinha nem para beber. Numa moradia, vai para o autoclismo, a lavagem de pavimentos, a rega do jardim e a lavagem do automóvel. O peso destes usos no consumo total é o **teto do potencial de economia**.

A repartição adotada no tutorial está representada na Figura 48, com os usos que a chuva atende assinalados. O autoclismo pesa 20% do consumo e a limpeza e a rega 8%; o duche, a pia da cozinha, o lavatório e a máquina de lavar roupa, que pesam o resto, ficam com a água potável.

Somando os dois usos que a chuva atende, chega-se aos 28% do tutorial. É um valor conservador para uma moradia sem jardim grande, e é conservador de propósito: limita-se aos usos que a orientação sobre águas pluviais admite com mais facilidade.

> **A máquina de lavar roupa é uma escolha que o tutorial não faz.** A ETA 0701 da ANQIP (versão 12) inclui a lavagem em máquinas de lavar roupa entre os usos possíveis da água da chuva, ao lado das descargas de autoclismo, da lavagem de pavimentos e automóveis, da rega de zonas verdes e de outros usos (torres de arrefecimento, redes de incêndio, AVAC). Para a máquina de lavar sem tratamento específico, o item 4.6.6 só a admite quando a água de lavagem atinge pelo menos 55 °C, e pede um microfiltro de malha mínima de 100 µm. O uso na máquina é comum na literatura e na prática, e por isso muitos estudos trabalham com frações atendíveis maiores do que a deste tutorial. O tutorial **não** o adota: a máquina fica com a água potável, e a fração atendível fica nos 28% do autoclismo e dos usos exteriores. Um projeto que inclua a lavagem de roupa tem de declarar essa escolha e o critério de qualidade adotado, e confrontá-la com a norma em vigor no local do edifício. [A COMPLETAR: confirmar a revisão em vigor da ETA 0701 e o que a EN 16941-1 diz sobre a lavagem de roupa.]

![A repartição do consumo numa moradia, e a parte que a chuva pode atender](../figuras/fig00c_fracao.png)

*Figura 48 — Repartição típica do consumo de uma moradia por uso final. A cinzento, os usos que exigem água potável; a verde, os que podem usar água da chuva, cuja soma é a fração atendível e o teto do potencial de economia: nenhum reservatório, por maior que seja, poupa mais do que esta fração.*

> **Este número é o teto.** Com 28% de fração atendível, o potencial de economia **nunca** passa de 28%, por maior que seja o reservatório e por mais que chova. A tabela da secção 4.4 mostra a curva a aproximar-se desse limite sem o atingir: em Lisboa, a 20.000 L ainda só chega a 24,01%.
>
> Quem quer passar dos 28% tem de mudar o **uso**, não o reservatório: acrescentar um uso, como a lavagem de roupa, com o critério de qualidade declarado, ou reduzir o consumo potável.

#### 4.2.3.1. Percentagem no ecrã, fração no ficheiro

A mesma grandeza aparece com duas grafias, e cada uma tem o seu lugar. Em todos os campos em que se escreve — as frações do ecrã da edificação, as tabelas semanal e mensal, as tabelas de cenários, a folha de cálculo de lote e o argumento `--share` da linha de comandos — a fração é uma **percentagem, de 0 a 100**: 28 significa 28%. No ficheiro de projeto, no ficheiro de parâmetros e em `rainwater_share` e `non_potable_indoor_share`, é uma **fração, de 0 a 1**: 0,28.

A divisão não é arbitrária. A percentagem é a forma em que a grandeza circula entre projetistas, normas e faturas da água, e é a forma em que menos se erra ao escrever. A fração é a forma em que entra na equação do balanço, a multiplicar a procura interior (secção 2.1), e é a forma que dispensa conversões a quem lê o ficheiro com outro programa.

O que não se admite é a mistura. Até esta versão, doze pontos do programa aceitavam as duas grafias e decidiam pela regra «acima de 1 é percentagem». A regra falha justamente nos valores pequenos, onde o erro não se vê: 1 passava a 100%, e não a 1%; 0,5 escrito numa coluna em percentagem passava a 50%. ==Agora a unidade é fixada pelo lugar, nunca adivinhada pelo valor.== Uma percentagem acima de 100 é recusada; uma fração acima de 1 é recusada com a indicação de que parece uma percentagem. A Figura 49 mostra os três estados do campo na interface.

![O campo em percentagem e o marcador de valor suspeito](../figuras/fig46b_percentual.png)

*Figura 49 — Estados do campo de fração atendível na interface. O campo recebe uma percentagem de 0 a 100; no ficheiro de projeto e nos parâmetros de cálculo a grandeza é guardada como fração de 0 a 1. Um valor entre 0 e 1 escrito no campo fica assinalado a laranja, sem bloquear o cálculo, porque 0,4% é possível, embora raro.*

> **O marcador laranja.** Um valor entre 0 e 1 num campo em percentagem é aceite, porque uma substituição inferior a 1% é possível, mas o campo fica laranja e a dica explica o que foi entendido. Nas tabelas de cenários e na folha de cálculo de lote, o programa pergunta antes de simular.

---

### 4.2.4. Discriminar os usos, ou não

O programa aceita dois níveis de pormenor na descrição da procura, e a escolha depende do que o estudo quer responder.

No **modo simplificado**, indicam-se duas coisas: a fração não potável do consumo interior — autoclismos e lavagem de roupa — e, se existir, a procura exterior em litros por dia. A fração atendível **total** sai das duas,

```text
f = (fração interior × procura interior + procura exterior) ÷ (procura interior + procura exterior)
```

e aparece num campo que não se edita, porque é resultado e não dado. Sem procura exterior, a total é a própria fração interior: os 28% deste tutorial. É o modo adotado aqui, e chega para a maior parte dos estudos.

> **Porque a total não se escreve.** Em versões anteriores, o campo da fração total era editável, mas a simulação usava a fração interior; e, ao abrir um projeto, o ecrã repunha a interior em 35% e a exterior em zero, fossem quais fossem as guardadas. Um projeto que declarava 28% era simulado com 35%. Hoje o ecrã restaura as duas, a total é calculada, e um ficheiro antigo cujas frações discordem abre com a total que declara, com um aviso.

No **modo discriminado**, a procura divide-se em três parcelas: a potável interior, que a chuva nunca atende; a não potável interior, que é a prioridade do sistema; e a rega, atendida em último lugar. A divisão muda duas coisas. Altera a ordem de atendimento nos dias de escassez, em que o uso interior tem precedência sobre o jardim; e permite distinguir o uso interior do exterior nos créditos de certificação, distinção que o LEED exige em créditos separados, como descreve a secção 2.9.

Vale a pena discriminar quando há um jardim de área relevante, quando a certificação está no horizonte do projeto, ou quando a rega pode ser suprimida nos dias de chuva — situação que o ponto seguinte trata.

---

### 4.2.5. A rega e a supressão por chuva

Declarado um volume de rega, o programa oferece um limiar de supressão por chuva: nos dias em que a precipitação excede esse limiar, o jardim não é regado. O comportamento reproduz o de qualquer programador de rega com sensor de chuva, equipamento corrente e barato, e ignorá-lo sobrestimaria a procura exterior ao longo do ano inteiro. O limiar predefinido é de 2 mm por dia.

> **A série de chuva é lida duas vezes.** Uma leitura converte-se em volume captado, depois do descarte. A outra decide se o jardim é regado. As duas são independentes: um dia pode suprimir a rega **e** render captação.

Resta uma escolha que merece atenção particular, porque altera o resultado económico e não é neutra: o **fornecimento de reserva** da rega. Com ele ligado, a rede pública rega o jardim nos dias secos em que a cisterna não chega, e esse volume entra na fatura da água e do saneamento como consumo potável. Com ele desligado, o jardim simplesmente não é regado nesse dia, o edifício não compra essa água, e o volume correspondente aparece no balanço como *procura não atendida* — a terceira parcela tratada na secção 2.1.

==A distinção entre as duas configurações é conceptual antes de ser numérica.== Um jardim que tem de ser regado todos os dias representa uma procura real, que alguém pagará; um jardim que aceita não ser regado num dia seco representa uma comodidade, e tratá-lo como procura infla tanto o consumo como a poupança aparente do sistema.

---

### 4.2.6. O que temos até aqui

<!-- tabela: **Tabela 90** — Estado do projeto do tutorial no fim da definição da procura -->
| Dado | Valor |
| :--- | ---: |
| tipologia | residencial unifamiliar |
| moradores | 4 |
| consumo per capita | 150 L/hab·dia |
| procura total | 600 L/dia |
| fração atendível pela chuva | 28% |
| **procura pluvial** | **168 L/dia** |

O programa sabe agora a oferta e a procura. Antes de simular, uma comparação que vale a pena guardar:

<!-- tabela: **Tabela 91** — Comparação entre a oferta anual de água da chuva e a procura atendível -->
| | m³/ano |
| :--- | ---: |
| oferta bruta de água da chuva (precipitação × área × coeficiente) | 92 |
| **procura pluvial do ano** | **61** |

A oferta excede a procura: o volume bruto é **1,5 vez** o que se pretende usar, antes de deduzir o descarte. Se a oferta fosse o único limite, o sistema atenderia 100% da procura pluvial e chegaria ao teto de 28%.

Não chega, e a secção 4.3 mostra porquê.

---

## 4.3. A primeira simulação

> No fim desta secção, tem o primeiro resultado no ecrã e sabe **ler** os quatro números que importam. Ler é a parte difícil: o programa entrega muitos números, e três deles respondem a perguntas diferentes.

Falta um dado para simular: o volume do reservatório. Vamos arriscar um palpite.

**3 000 litros.** Uma cisterna de betão de 3 m³ é um tamanho comum de logradouro e é o que um projetista proporia sem pensar muito. A secção 4.4 vai perguntar se é o volume certo. Aqui só queremos ver o programa a correr.

Na etapa **4. Reservatório & Custos**, escolha volume fixo, indique 3 000 L, deixe o reservatório superior por assinalar e simule.

---

### 4.3.1. O resultado

<!-- tabela: **Tabela 92** — Resultado da primeira simulação do tutorial, com um reservatório de 3 000 L -->
| Resultado com 3 000 L | Valor |
| :--- | ---: |
| potencial de poupança de água potável | **15,39%** |
| água da chuva consumida | 92,3 L/dia |
| água da rede consumida | 507,7 L/dia |
| água extravasada | 106,4 L/dia |
| dias de abastecimento pleno | 53,3% |
| dias de abastecimento parcial | 2,9% |
| dias de abastecimento nulo | 43,8% |
| procura pluvial pretendida | 168 L/dia |
| volume anual poupado | 33,7 m³/ano |

O ecrã devolve várias dezenas de valores, e quatro bastam para julgar o projeto nesta etapa. Cada um responde a uma pergunta distinta, e é justamente por isso que não se substituem: um projeto pode ser bom pelo primeiro e mau pelo terceiro, e a leitura conjunta é o que evita conclusões apressadas.

---

### 4.3.2. O potencial de economia: 15,39%

Este indicador responde à pergunta que motiva a maior parte dos projetos: quanto da fatura da água e do saneamento deixa de se pagar. É o valor central do programa e o que consta do resumo de qualquer estudo. Corresponde à razão entre a água da chuva consumida e a procura total do edifício ao longo de toda a série, como na Equação 14.

O denominador merece atenção, porque dele decorre tudo o resto: é a procura **total**, não a procura pluvial. É esta escolha que fixa o teto do indicador nos 28%, a fração atendível definida na secção 4.2, e não em cem por cento.

O sistema alcançou 15,39% contra um teto de 28%, o que significa que entrega 55% do que se propunha entregar (92,3 L/dia de chuva consumida, contra 168 L/dia de procura pluvial). Os 45% em falta correspondem aos dias em que a cisterna não tinha água suficiente para atender à procura pluvial do dia.

> **Não confunda as duas percentagens.** «Economia de 15%» e «atendimento de 55% da procura pluvial» descrevem o mesmo sistema e são números diferentes. Estudos publicados trocam por vezes um pelo outro. Declare qual está a usar.

---

### 4.3.3. O extravasamento: 106,4 L/dia

**Responde: o reservatório é suficientemente grande?**

Em média, ao longo dos trinta anos, extravasam da cisterna 106,4 litros por dia, que seguem para a rede de drenagem. Menos do que os 168 L/dia que o sistema pretende consumir, mas ainda assim muita água a perder.

Parece o argumento definitivo a favor de aumentar o reservatório, e é um argumento fraco. A cobertura oferece 1,5 vez o que a casa consome (secção 4.2), e boa parte desse excedente extravasaria de qualquer cisterna: a secção 4.4 mostra que nem 20 000 L o reduzem abaixo de 54 L/dia. O extravasamento só diz algo sobre o volume quando comparado com o de outros volumes, e é essa comparação que a secção 4.4 faz.

> Um extravasamento elevado não é defeito do programa nem do projeto. É a assinatura do desencontro entre a chuva, que chega concentrada em poucos dias, e a procura, que é constante. O reservatório existe para amortecer isso, e todo o reservatório finito falha em algum episódio.

---

### 4.3.4. Os dias de atendimento: 53,3% plenos

**Responde: com que frequência posso contar com o sistema?**

É a fiabilidade **temporal** do sistema, e responde a uma pergunta que o potencial de economia não alcança: com que frequência se pode contar com a água da chuva. Cada dia da simulação recebe uma de três classificações, conforme o grau de atendimento alcançado.

<!-- tabela: **Tabela 93** — Classificação de cada dia da simulação quanto ao grau de atendimento -->
| Classe | O que significa |
| :--- | :--- |
| pleno | a chuva atendeu **toda** a procura pluvial do dia |
| parcial | atendeu parte, e a rede completou |
| nulo | a cisterna estava vazia; tudo veio da rede |

Em 53,3% dos dias o sistema deu conta sozinho da procura pluvial. Nos restantes 46,7%, a rede pública entrou, total ou parcialmente: 2,9% dos dias foram parciais e 43,8% nulos. A distinção tem consequência direta no projeto hidráulico. Um sistema com muitos dias de atendimento nulo exige um abastecimento automático de reserva bem dimensionado, e o utilizador nota a alternância entre as duas origens ao longo do ano. Um sistema com 99% de dias plenos é, na prática, independente da rede para os usos que atende.

> **Potencial e fiabilidade não andam juntos.** É possível ter um potencial alto com fiabilidade baixa: um reservatório que enche na estação chuvosa e seca na estiagem entrega muito volume no ano e falha metade dos dias. A tabela da secção 4.4 mostra as duas colunas a divergir.

---

### 4.3.5. O volume anual poupado

**Responde: quanto vale isto em dinheiro e em carbono?**

É o valor que passa para as secções 4.7 e 4.8, porque tanto a poupança na fatura da água e do saneamento como a emissão de carbono evitada se calculam a partir dele. Vale 33,7 m³/ano, bem menos de metade dos 92 m³/ano que a cobertura disponibiliza antes do descarte; o descarte e o extravasamento explicam a diferença.

---

Antes de discutir porque o potencial não chega aos 28%, convém ver o reservatório a trabalhar. O separador de resultados traz a série diária do nível da cisterna, e é nela que se veem de uma só vez os dois regimes que limitam o aproveitamento: o extravasamento e a falta (Figura 50).

![O nível da cisterna, dia a dia, ao longo de um ano](../figuras/fig48_programa_serie_diaria.png)

*Figura 50 — O nível da cisterna ao longo do primeiro ano da série de Lisboa, com a chuva diária ao fundo. Os planaltos no topo são os dias em que o reservatório está cheio e extravasa; os vales no zero são os dias em que secou e a rede atendeu tudo. Em Lisboa, os vales concentram-se no verão. Figura gerada pelo próprio programa.*

---
### 4.3.6. Porque não chegamos aos 28%

A secção 4.2 terminou com uma comparação aparentemente favorável: 92 m³ anuais de oferta contra 61 m³ de procura pluvial, isto é, 1,5 vez o necessário. Perante este excedente, seria razoável esperar atendimento integral, e no entanto o sistema entrega apenas 55% do pretendido.

A explicação está inteiramente no **tempo**. O excedente não ocorre quando a água faz falta: a precipitação chega concentrada, enche a cisterna de 3 000 L num único dia de chuva intensa, extravasa no mesmo dia, e falta duas semanas depois. Em Lisboa, a falta é longa: o verão quase não tem chuva. O excedente anual e o atendimento diário são grandezas que não comunicam, e é precisamente esta incomunicabilidade que torna a simulação diária indispensável.

A cisterna de 3 000 L armazena o equivalente a dezoito dias de procura pluvial. Qualquer estiagem mais longa esvazia-a, e a partir daí o sistema depende inteiramente da rede até à chuva seguinte.

É por isso que aumentar o reservatório funciona — e é por isso que aumentar tem limite. A secção 4.4 mede exatamente onde fica esse limite.

---

### 4.3.7. O que temos até aqui

<!-- tabela: **Tabela 94** — Estado do projeto do tutorial depois da primeira simulação -->
| Resultado com 3 000 L | |
| :--- | ---: |
| potencial de economia | 15,39% |
| de um teto de | 28% |
| extravasamento | 106,4 L/dia |
| dias de atendimento pleno | 53,3% |

Um resultado defensável, mas longe do teto. E escolhemos 3 000 L por palpite: pode ser pouco, e pode ser demais.

Quanto seria o certo?

---

## 4.4. Escolher o volume

> No fim desta secção, tem a curva de retorno do reservatório, sabe onde deixa de compensar, e percebe porque **não existe** um volume ótimo absoluto — existe um volume ótimo para um critério declarado.

A secção 4.3 adotou 3 000 L como primeiro palpite e encontrou 106,4 L/dia a extravasar e um atendimento pleno em apenas 53,3% dos dias. A pergunta que se impõe é quanto reservatório vale a pena ter. Não se responde com uma tentativa isolada: responde-se simulando o mesmo projeto para muitos volumes e vendo como o resultado evolui. É o que o programa chama **varredura**.

---

### 4.4.1. Executar a varredura

Na etapa **4. Reservatório & Custos**, escolha o modo varredura e indique o volume máximo e o passo. Para o nosso projeto: máximo de 20 000 L, passo de 1 000 L.

Há duas particularidades na montagem da grelha que convém conhecer antes de interpretar o resultado. A primeira é que o passo indicado é arredondado para cima até ao múltiplo de 250 L, o quantum comercial dos reservatórios — ninguém compra uma cisterna de 1 300 L, e um ótimo apontado para esse volume seria inexequível. Quando o passo pedido não é múltiplo de 250, o programa ajusta-o e regista o ajuste, para que o relatório possa declarar o passo realmente usado.

A segunda é que a grelha se limita a quarenta volumes positivos. Uma varredura de 0 a 50 000 L com passo de 100 L exigiria quinhentas simulações de trinta anos cada, e o ganho de informação não compensa o tempo de cálculo, porque a curva é suave e quarenta pontos descrevem-na com folga. O volume máximo indicado é sempre mantido como último ponto da grelha, pelo que só o último intervalo pode ser menor do que o passo efetivo.

O volume zero faz parte da grelha como alternativa de referência: representa o cenário sem sistema, com o qual todos os outros se comparam.

---

### 4.4.2. A curva

<!-- tabela: **Tabela 95** — Varredura de volumes do projeto do tutorial, com o ganho marginal de cada metro cúbico acrescentado -->
| Volume | Potencial | Ganho sobre o anterior | Ganho por metro cúbico acrescentado | Extravasado | Dias plenos |
| ---: | ---: | ---: | ---: | ---: | ---: |
| L | % | pontos percentuais | %/m³ | L/dia | % |
| 0 | 0,00 | — | — | 199 | 0,0 |
| 1 000 | 10,39 | 10,39 | 10,39 | 136 | 33,6 |
| 2 000 | 13,55 | 3,16 | 3,16 | 117 | 46,1 |
| 3 000 | 15,39 | 1,84 | 1,84 | 106 | 53,3 |
| 4 000 | 16,60 | 1,21 | 1,21 | 99 | 58,0 |
| 5 000 | 17,49 | 0,89 | 0,89 | 94 | 61,3 |
| 6 000 | 18,19 | 0,70 | 0,70 | 89 | 64,0 |
| 8 000 | 19,39 | 1,21 | 0,60 | 82 | 68,4 |
| 10 000 | 20,37 | 0,98 | 0,49 | 76 | 72,0 |
| 12 000 | 21,23 | 0,86 | 0,43 | 70 | 75,2 |
| 16 000 | 22,73 | 1,50 | 0,38 | 61 | 80,6 |
| 20 000 | 24,01 | 1,27 | 0,32 | 54 | 85,2 |

A Figura 51 traça os resultados da tabela: o potencial de economia sobe em direção à fração atendível sem a atingir, e o ganho marginal cai mais de trinta vezes ao longo da varredura.

![Curva de potencial e curva de ganho marginal](../figuras/fig02_curva_de_retorno.png)

*Figura 51 — (a) Potencial de economia em função do volume do reservatório, que continua a subir aos 20 000 L (24,01%) sem alcançar o teto de 28%, com o volume ideal marcado; (b) ganho marginal, em escala logarítmica, com o limiar de 1 %/m³ adotado no tutorial.*

A coluna decisiva da tabela é a do **ganho por metro cúbico acrescentado**, a derivada discreta da curva de potencial, que exprime quanto cada metro cúbico adicional de reservatório acrescenta de economia. A tabela abaixo destaca alguns intervalos, e o padrão que revela é o argumento central desta secção.

<!-- tabela: **Tabela 96** — Ganho marginal de economia por cada metro cúbico acrescentado ao reservatório -->
| De → para | Ganho por m³ |
| :--- | ---: |
| 0 → 1 000 L | 10,39 %/m³ |
| 1 000 → 2 000 L | 3,16 %/m³ |
| 2 000 → 3 000 L | 1,84 %/m³ |
| 3 000 → 4 000 L | 1,21 %/m³ |
| 4 000 → 5 000 L | 0,89 %/m³ |
| 10 000 → 12 000 L | 0,43 %/m³ |
| 16 000 → 20 000 L | 0,32 %/m³ |

==O primeiro metro cúbico de reservatório entrega mais de 10 pontos percentuais de economia; os de 16 para 20 m³ entregam menos de um terço de ponto cada um.== A diferença é de mais de trinta vezes, e os metros cúbicos custam o mesmo betão, a mesma escavação e a mesma mão de obra.

Aqui Lisboa difere de um clima de chuva bem repartida. A curva **não satura**: a 20 000 L ainda sobe, e só 85,2% dos dias são plenos. A razão é o verão seco. O mês mais chuvoso recebe 47,3 vezes o que recebe o mais seco, e uma cisterna maior continua a ganhar, porque guarda mais inverno para atravessar mais verão. O ganho é pequeno, mas não chega a zero.

O comportamento tem, ainda assim, a forma característica de toda a curva de aproveitamento pluvial, e decorre de dois factos que atuam em conjunto. Os primeiros litros de armazenamento captam os episódios pequenos e frequentes, que são a maioria das chuvas em qualquer regime; e o teto imposto pela fração atendível, de 28% neste projeto, puxa a curva para a horizontal à medida que o sistema dele se aproxima, de modo que o espaço restante para ganho se vai esgotando.

---

#### 4.4.2.1. Os quatro gráficos que o ecrã mostra

A varredura não devolve apenas a curva de potencial. O separador de resultados traz quatro gráficos que respondem a perguntas diferentes sobre o mesmo conjunto de simulações, reproduzidos a seguir com os dados deste tutorial: o potencial de economia (Figura 52), o ganho marginal (Figura 53), os volumes extravasado e consumido (Figura 54) e a classificação dos dias (Figura 55).

![O potencial de economia contra o volume, no ecrã do programa](../figuras/fig10_programa_potencial.png)

*Figura 52 — O primeiro gráfico do separador de resultados: o potencial de economia de água potável em função do volume do reservatório inferior. A estrela marca o volume selecionado. Figura gerada pelo próprio programa, com os dados do tutorial.*

![O ganho marginal contra o volume, no ecrã do programa](../figuras/fig11_programa_delta.png)

*Figura 53 — O segundo gráfico: o ganho marginal, em pontos percentuais por metro cúbico acrescentado. É a derivada da curva anterior, e é sobre ela que opera o critério do volume ideal. Figura gerada pelo próprio programa.*

![Extravasamento e consumo pluvial contra o volume](../figuras/fig12_programa_extravasamento.png)

*Figura 54 — O terceiro gráfico: o volume extravasado e o volume pluvial consumido, ambos anuais, na mesma escala. As duas curvas explicam-se uma à outra, porque toda a água que deixa de extravasar passa a ser consumida. Figura gerada pelo próprio programa.*

![O atendimento dos dias contra o volume](../figuras/fig13_programa_dias.png)

*Figura 55 — O quarto gráfico: a repartição dos dias do período em atendidos por inteiro, atendidos em parte e não atendidos. É a leitura temporal da mesma varredura, e a única que responde à pergunta com que frequência se pode contar com o sistema. Figura gerada pelo próprio programa.*

---

### 4.4.3. O volume ideal

Perante uma curva cujo rendimento decai desta forma, a pergunta «qual é o volume ideal?» só admite resposta depois de se estabelecer o que significa deixar de compensar. O Triton adota para isso o critério do ganho marginal: o volume ideal é o menor volume cujo ganho por metro cúbico acrescentado já desceu abaixo de um limiar declarado pelo utilizador, conforme a formulação da secção 2.2.

O programa abre com um limiar de 5 %/m³, e o tutorial adota um mais exigente, de 1 %/m³. A diferença não é um pormenor: com o valor predefinido, o volume ideal deste projeto seria de 2 000 L (ganho de 3,16 %/m³); com o limiar do tutorial, o primeiro volume a descer abaixo dele é o de 5 000 L, com um ganho marginal de 0,89 %/m³. Quem refizer o tutorial tem, por isso, de alterar o limiar no programa antes de executar a varredura.

<!-- tabela: **Tabela 97** — Indicadores do volume ideal obtido com o limiar de 1 %/m³ adotado no tutorial -->
| Indicador | Valor |
| :--- | ---: |
| volume ideal, limiar de 1 %/m³ | 5 000 L |
| potencial nesse volume | 17,49% |
| de um teto de | 28% |
| dias de atendimento pleno | 61,3% |

O limiar, contudo, é uma escolha do analista, e decide o resultado tanto como os dados de entrada. A tabela abaixo mostra o volume ideal que cada limiar plausível produziria para este mesmo projeto.

<!-- tabela: **Tabela 98** — Volume ideal obtido com cada limiar de ganho marginal, para o mesmo projeto -->
| Limiar declarado | Volume ideal | Potencial |
| ---: | ---: | ---: |
| 3,0 %/m³ | 3 000 L | 15,39% |
| 1,0 %/m³ | 5 000 L | 17,49% |
| 0,5 %/m³ | 10 000 L | 20,37% |

<!-- tabela: **Tabela 99** — Custo e desempenho comparados entre o volume ideal e o maior volume varrido (os preços são ilustrativos, não são preços de mercado) -->
| | 5 000 L | 20 000 L |
| :--- | ---: | ---: |
| potencial de poupança | 17,49% | 24,01% |
| preço da cisterna de betão (ilustrativo, não é preço de mercado) | 2 600 € | 8 600 € |
| massa de betão | 6 000 kg | 24 000 kg |
| carbono incorporado do sistema | 1 026 kg CO₂e | 3 546 kg CO₂e |
| **razão de preços** | | **3,3×** |
| **ganho de potencial** | | **+6,52 pontos** |

O programa não emite opinião sobre qual seria o limiar correto, e não poderia: a escolha depende do custo do reservatório, do valor da água no concelho e do espaço disponível no terreno, nenhum dos quais é um dado hidrológico. O que o programa faz é aplicar fielmente o limiar declarado e registá-lo no relatório.

> **Num estudo publicado, declare o limiar.** Dois artigos com «volume ideal» de limiares diferentes não são comparáveis. Entre o primeiro e o último limiares da tabela, a diferença é de 7 000 L de reservatório, que compram 4,98 pontos percentuais de economia.

---

### 4.4.4. Porque o critério do ganho marginal não basta

O critério do ganho marginal é puramente hidráulico: olha para a curva de aproveitamento e para mais nada. Não sabe quanto custa o reservatório, quanto vale o metro cúbico de água no concelho em causa, nem quanto carbono traz consigo o material escolhido. Desta cegueira decorrem três consequências, e cada uma pode deslocar a recomendação num sentido diferente.

- Se a água for muito cara, o ganho de 0,89 %/m³ do quinto metro cúbico pode pagar-se bem, e o volume económico será **maior** do que o hidráulico.
- Se a cisterna for cara ou o espaço escasso, o inverso.
- Uma cisterna de betão de 20 m³ pesa 24 toneladas e traz, com o resto do sistema, cerca de **3,5 toneladas de CO₂e** incorporado (3 546 kg), contra cerca de uma tonelada na de 5 m³ (1 026 kg). Os últimos metros cúbicos acrescentam pouca economia, e não têm como compensar a diferença.

São três critérios e três respostas diferentes para a mesma pergunta, e nenhuma é mais legítima do que as outras em abstrato. É por isso que o tutorial não acaba aqui: as secções 4.7 e 4.8 acrescentam à análise, respetivamente, o dinheiro e o carbono, e a secção 4.9 põe as três dimensões na mesma mesa, com pesos declarados, para chegar a um volume de compromisso que se possa defender.

> **O engano mais comum, e está na secção 5.1.** Publicar o volume de maior economia de água como se fosse o volume recomendado. Pela tabela, 20 000 L dão o maior potencial, 24,01%. A cisterna de betão custa **3,3 vezes mais** do que a de 5 000 L (2 600 € contra 8 600 €; preços ilustrativos, não são preços de mercado) e traz **3,5 vezes mais carbono incorporado**, para entregar 6,52 pontos percentuais a mais.

---

A varredura tem ainda uma leitura que a tabela não mostra: quanto da capacidade o consumo realmente usa. Medir o reservatório pelo nível engana, porque a cisterna grande parece sempre cheia justamente por guardar água que a procura nunca chega a retirar. A Figura 56 mede a capacidade pelo consumo, de duas maneiras. A primeira é a **autonomia armazenada**, o volume no fim de cada dia dividido pela procura pluvial diária de 168 L, apresentada como curva de permanência. A segunda é o número de **renovações por ano**, a razão entre o consumo pluvial anual e a capacidade, que diz quantas vezes o volume da cisterna é realmente consumido e reposto.

A cisterna pequena renova o seu volume muitas vezes por ano e termina o dia vazia com frequência: a capacidade é inteiramente usada, e falta água. A grande renova-o poucas vezes e raramente se esvazia, mas guarda, na maior parte dos dias, semanas de procura, mais do que a estiagem registada exigiria. Essa reserva que o consumo não chega a mobilizar é o que o investimento adicional compra, e é a leitura física do retorno decrescente da curva de potencial. Em Lisboa, onde o verão é longo, esta leitura é menos severa do que numa chuva bem repartida: parte da reserva é de facto consumida em agosto.

![A permanência do nível do reservatório](../figuras/fig47_permanencia.png)

*Figura 56 — Uso da capacidade do reservatório inferior no projeto do tutorial, com procura pluvial de 168 L/dia: (a) curvas de permanência da autonomia armazenada no fim de cada dia, em dias de procura pluvial, para vários volumes; (b) renovações anuais do volume, dadas pela razão entre o consumo pluvial anual e a capacidade, com a fração de dias em que o reservatório termina vazio (até 5% da capacidade) indicada sob cada volume.*

---
### 4.4.5. Mais duas leituras da tabela

**O extravasamento não chega a zero.** Parte de 199 L/dia sem reservatório e desce para 54 L/dia com vinte metros cúbicos, e ainda não estabilizou. Parte da água que a cobertura capta continuará a ir para a drenagem, por uma razão que nenhum aumento do reservatório resolve: a procura simplesmente não a consome. Os sistemas de aproveitamento pluvial não retêm água por reter, e quem procura amortecer cheias precisa de um reservatório de retenção, que é outro projeto, com outro critério de dimensionamento.

**A fiabilidade cresce mais depressa do que o potencial.** Ao passar de 3 000 para 4 000 L, o potencial de economia ganha 1,21 pontos percentuais, ao passo que os dias de atendimento pleno sobem de 53,3% para 58,0%. Quando o critério de projeto é o conforto de uso — não faltar água da chuva nos pontos que a utilizam — e não a poupança na fatura, a leitura da mesma tabela leva a outra escolha.

---

### 4.4.6. O que temos até aqui

O tutorial adota 5 000 L e segue. É o volume ideal pelo critério hidráulico com o limiar de 1 %/m³, e é o valor que o projeto leva até à secção 4.9, onde será posto em causa outra vez, agora com o dinheiro e o carbono incorporados na análise.

<!-- tabela: **Tabela 100** — Estado do projeto do tutorial depois da escolha do volume -->
| Projeto até aqui | |
| :--- | ---: |
| série | Lisboa, 30 anos |
| área de captação | 150 m² |
| procura total | 600 L/dia |
| fração atendível | 28% |
| **volume do reservatório** | **5 000 L** |
| potencial de economia | 17,49% |
| dias de atendimento pleno | 61,3% |

Resta uma decisão hidráulica antes de se poder falar de dinheiro: esta água precisa de subir para um reservatório elevado, ou pode ser pressurizada diretamente a partir da cisterna? É o assunto da secção 4.5.

---

## 4.5. Precisa de reservatório superior?

> No fim desta secção, sabe responder à pergunta com um número, e não por hábito. A resposta costuma surpreender.

O arranjo clássico do aproveitamento pluvial emprega dois reservatórios: uma cisterna enterrada, que recebe a água da cobertura, e um reservatório elevado, que alimenta os pontos de consumo por gravidade; entre os dois, uma eletrobomba faz a elevação. O arranjo é tão difundido que quase todos os projetos o adotam sem examinar a razão, e esta secção examina-a.

---

### 4.5.1. Para que serve o reservatório superior

==O reservatório superior não serve para guardar mais água; serve para a entregar.== A distinção parece subtil e decide toda a análise, porque tudo o que se segue depende de não confundir capacidade de armazenamento com capacidade de distribuição.

A cisterna está enterrada, e os pontos de consumo — autoclismo, tanque, torneira de jardim — ficam acima dela. Alguma coisa tem de vencer esse desnível, e há duas maneiras de o fazer com bomba.

- **Pressurização direta.** Uma bomba pequena com pressostato liga sempre que se abre um ponto de consumo. Não há reservatório superior.
- **Elevação para um reservatório elevado.** A bomba enche o reservatório de tempos a tempos, e a gravidade faz o resto.

Quando a cisterna fica acima dos pontos de uso, há ainda uma terceira: a **gravidade**, sem bomba. A etapa **4. Reservatório & Custos** pergunta qual dos três arranjos o projeto adota, e é esta resposta que define a energia e as eletrobombas no custo e no carbono.

<!-- tabela: **Tabela 101** — Os três arranjos de abastecimento e o que cada um acrescenta ao projeto -->
| Arranjo | Energia calculada | Reservatório superior e eletrobombas |
| :--- | :--- | :--- |
| elevação para reservatório superior | volume elevado, pela altura manométrica, mais os arranques | entram no custo e no carbono |
| pressurização direta | todo o volume pluvial consumido, pela pressão de trabalho | só as eletrobombas |
| gravidade | nenhuma | nenhuma |

Na pressurização direta, a etapa 4 pede o modelo do sobrepressor, escolhido num catálogo de seis modelos genéricos de referência, de A a F, cada um com uma curva caudal × pressão ilustrativa (nenhum é um produto real), a pressão de trabalho e o caudal do ponto de uso. O sobrepressor liga a cada descarga, 5,05 por pessoa e por dia segundo o levantamento de usos finais de Mayer et al. (1999), e fica ligado enquanto o autoclismo acoplado enche, ao ritmo da torneira de bóia. A energia é esse tempo vezes a potência elétrica. No tutorial, a uma pressão de 18 m, o menor modelo gastaria 26,1 kWh por ano, cerca de cinco vezes os 5,1 kWh da elevação; a secção 2.6 explica porquê e mostra que o modelo escolhido pesa mais do que a pressão. [A COMPLETAR: confirmar a referência de Mayer et al. (1999) e o valor de 5,05 descargas por pessoa e por dia numa fonte aberta.]

A elevação para um reservatório elevado tem três vantagens práticas reais. A eletrobomba liga poucas vezes por dia, em vez de dezenas, o que prolonga a vida do equipamento; a pressão nos pontos de consumo é constante, porque decorre da altura da coluna de água e não do funcionamento da bomba; e há reserva disponível durante uma falha de energia. ==Nenhuma destas três vantagens é poupança de água==, e é justamente essa a confusão que a secção desfaz.

---

### 4.5.2. A comparação justa

Comparar um sistema de 5 000 L sem reservatório elevado com outro de 5 000 L mais 1 000 L de reservatório superior é uma armadilha metodológica, porque o segundo dispõe de mais armazenamento total e ganharia por essa razão, não pelo arranjo. Para isolar o efeito do arranjo, é preciso manter o armazenamento constante: comparam-se, portanto, 6 000 L num único reservatório contra 5 000 L em baixo mais 1 000 L em cima.

<!-- tabela: **Tabela 102** — Reservatório único comparado com dois reservatórios, mantido o mesmo armazenamento total (o custo da energia é ilustrativo, não é preço de mercado) -->
| Mesmo armazenamento de 6 000 L | Um só reservatório | 5 000 em baixo + 1 000 em cima |
| :--- | ---: | ---: |
| potencial de poupança | 18,19% | 17,88% |
| dias de abastecimento pleno | 64,0% | 62,8% |
| volume elevado | — | 39,2 m³/ano |
| arranques da bomba | — | 49 por ano |
| horas de bomba | — | 8,4 h/ano |
| energia | — | 5,1 kWh/ano |
| custo da energia (ilustrativo, não é preço de mercado) | — | 1,03 €/ano |
| **diferença de potencial** | | **−0,31 pontos** |

Com o mesmo armazenamento, o arranjo com reservatório elevado entrega 0,31 pontos percentuais a menos de economia do que o reservatório único (17,88% contra 18,19%). A diferença não é erro de arredondamento, e tem uma causa: **a cisterna extravasa enquanto o reservatório superior ainda tem espaço**.

A chuva entra só pela cisterna, e o extravasamento é calculado nela antes do consumo do dia. A elevação, porém, só acontece quando há consumo e o reservatório superior desce abaixo do limiar de acionamento. Assim, num dia de chuva com a cisterna cheia, a água que excede os 5 000 L de baixo perde-se mesmo que o reservatório de cima tenha centenas de litros livres. Um reservatório único de 6 000 L guardá-la-ia.

É também por isso que um limiar de acionamento maior rende mais: com ele, a bomba enche o reservatório mais cedo, a cisterna está mais vazia quando a chuva chega, e extravasa menos. A reserva abaixo do limiar não fica imobilizada, porque é consumida logo a seguir a cada elevação e quando a cisterna seca.

> **O reservatório superior não aumenta a poupança de água. Custa.** No nosso projeto, custa o reservatório, custa a bomba, custa 5,1 kWh por ano de energia, e custa 0,31 pontos de potencial em relação a um reservatório único do mesmo volume total.
>
> Isto não o torna errado. Torna a decisão **hidráulica**, e não hídrica: adote-o se o projeto precisa de pressão por gravidade ou de reserva contra falhas de energia, e não à espera de que renda mais água.

---

### 4.5.3. O limiar de acionamento

Se adotar o reservatório superior, há um parâmetro a ajustar: o volume de reserva que não se consome, abaixo do qual a bomba arranca.

<!-- tabela: **Tabela 103** — Efeito do limiar de arranque da bomba no potencial de poupança e no número de arranques -->
| Limiar de arranque | Potencial | Arranques por ano |
| ---: | ---: | ---: |
| 0 L | 17,78% | 45 |
| 100 L | 17,88% | 49 |
| 300 L | 17,95% | 61 |
| 500 L | 18,01% | 80 |

Um limiar maior significa **mais potencial e mais arranques**, pela razão acima. De 0 para 500 L, o potencial sobe 0,23 pontos (de 17,78% para 18,01%) e os arranques passam de 45 para 80 por ano.

A troca é entre um ganho hídrico marginal e o desgaste da eletrobomba. As eletrobombas residenciais suportam bem alguns arranques por dia; o que as mata é o liga-desliga contínuo. Oitenta arranques por ano são menos de dois por semana, e nenhum dos valores da tabela chega perto de ser um problema.

> **Onde o limiar importa a sério** é nos edifícios com procura concentrada, em que o reservatório esvazia depressa. Aí pode passar dos mil arranques por ano, e convém dimensionar o reservatório em vez de mexer no limiar.

---

### 4.5.4. A energia, e porque é pequena

Cinco vírgula um quilowatts-hora por ano. A 0,20 € por quilowatt-hora, valor ilustrativo, não é preço de mercado, são 1,03 € por ano.

Parece pouco demais, e vale a pena perceber porquê. Elevar um metro cúbico de água a dez metros custa, em energia hidráulica, cerca de 0,027 kWh. Com os rendimentos da bomba e do motor, e somados os arranques, o programa chega a cerca de 0,13 kWh por metro cúbico elevado. Os 39,2 metros cúbicos elevados por ano dão os 5,1 quilowatts-hora da tabela.

A água é pesada, mas a altura de um edifício pequeno é pouca. É por isso que o custo energético do aproveitamento pluvial é desprezável face à poupança na fatura da água e do saneamento — e é por isso também que o argumento de que «bombear água gasta mais energia do que poupa» não se sustenta num edifício de pequeno porte.

> **Atenção à potência de placa.** O programa pede o rendimento **da bomba** e o rendimento **do motor** em separado. A potência de placa é a potência mecânica no veio, e o rendimento do motor é o que separa o que o veio entrega do que o contador regista. Em branco, o programa adota um rendimento de motor por omissão, que depende da potência nominal; substitua-o pelo valor da ficha técnica do motor. A secção 2.6 detalha.

---

### 4.5.5. A decisão do tutorial

**Adotamos a elevação para um reservatório superior de 1 000 L, com limiar de 100 L.**

A decisão é hidráulica, e não hídrica. O reservatório elevado dá pressão constante nos pontos de uso sem depender da bomba a cada descarga, mantém água disponível durante uma falha de energia e faz a eletrobomba arrancar 49 vezes por ano, em vez das mais de sete mil partidas de um sobrepressor acionado a cada descarga por quatro moradores, que gastaria entre 26 e 68 kWh por ano conforme o modelo genérico. O preço é o que a tabela mostra: o reservatório, as bombas, 5,1 kWh por ano e 0,31 pontos de potencial face a um reservatório único de 6 000 L. As bombas são duas, a principal e a de reserva, a precaução habitual num sistema de elevação de que o edifício não pode prescindir.

Em relação à cisterna de 5 000 L sozinha, o potencial sobe de 17,49% para 17,88%, porque o reservatório acrescenta 1 000 L de armazenamento. Daqui em diante, o custo, o carbono e a decisão do tutorial incluem o reservatório superior, as duas eletrobombas e a energia da elevação.

<!-- tabela: **Tabela 104** — Estado do projeto do tutorial depois da decisão sobre o reservatório superior -->
| Projeto até aqui | |
| :--- | ---: |
| volume do reservatório inferior | 5 000 L |
| arranjo | elevação para reservatório superior |
| reservatório superior | 1 000 L, limiar de 100 L |
| potencial de economia | 17,88% |

Já sabemos quanta água o sistema entrega. Falta saber **que água** é essa.

---

## 4.6. Que qualidade o uso exige

> No fim desta secção, o projeto tem uma linha de tratamento definida, e sabe distinguir o que a norma exige do que o programa recomenda.

Até aqui, o tutorial tratou a água da chuva apenas como volume: quanto se capta, quanto se armazena, quanto se consome. A água é também uma qualidade, e a qualidade custa dinheiro — em equipamento, na instalação, e em consumíveis, todos os meses. Esta secção define a classe de qualidade do projeto e dimensiona a linha de tratamento correspondente.

---

### 4.6.1. O que a norma diz, e o que não diz

Em Portugal, a ETA 0701 da ANQIP (versão 7; ver a secção 1.1) trata a qualidade em função do uso. Para a rega de zonas verdes e a lavagem de pavimentos, admite que a água da chuva, cumpridas as prescrições de instalação, pode dispensar qualquer tratamento complementar físico-químico ou bacteriológico (item 4.6.3). Para o autoclismo, só admite a água sem tratamento quando respeita, no mínimo, as normas de qualidade das águas balneares (item 4.6.4); se os valores máximos dos parâmetros microbiológicos não forem cumpridos, prevê a desinfeção por ultravioletas, cloro ou outro processo adequado, e recomenda, no caso do cloro, um residual livre entre 0,2 e 0,6 mg/L (item 4.6.5). Os tratamentos básicos que admite são a filtragem, no filtro de montante, e a sedimentação, na cisterna (item 4.6.2). [A COMPLETAR: a versão 7 da ETA 0701 cita o Decreto-Lei n.º 236/98 e a Diretiva 76/160/CEE para as águas balneares; confirmar a legislação hoje em vigor sobre a qualidade das águas balneares e os valores-limite aplicáveis antes de os usar como critério, e confirmar a revisão em vigor da ETA 0701.]

A norma europeia EN 16941-1 também trata do tema, sem dispensar o cumprimento da regulamentação nacional ou local. [A COMPLETAR: ler a edição em vigor da EN 16941-1 (catálogo do IPQ ou do CEN) e indicar o que fixa para a qualidade da água e a desinfeção, com o número do capítulo.]

Em geral, uma norma para uso não potável fixa uma lista curta de parâmetros mínimos: um indicador microbiológico como a *E. coli*, a turvação e o pH, e, se houver cloro, um intervalo para o residual livre. A desinfeção fica muitas vezes a critério do projetista, e a monitorização pede-se com uma periodicidade indicada. Verifique a norma aplicável ao local do projeto e introduza os seus limites como critério.

O programa, por seu lado, oferece quatro classes, e a razão é prática: o autoclismo e a rega do jardim não expõem o utilizador da mesma maneira, ainda que uma norma os não distinga (Figura 57).

> **Reutilização não é aproveitamento.** Os parâmetros fixados para a **reutilização** de águas residuais tratadas costumam ser muito mais restritivos do que os do aproveitamento da água da chuva: ausência de coliformes, residual de cloro mais alto e turvação mais baixa. A água da chuva não é reutilização, e a tabela que se aplica ao aproveitamento é a da norma da água da chuva, não a da norma de reutilização.

![As quatro classes de qualidade do programa](../figuras/fig36_classes.png)

*Figura 57 — As quatro classes de qualidade do programa e a situação de cada uma. A classe 1 é o conjunto mínimo de referência, com os parâmetros menos exigentes; as classes 2 a 4 são adaptações do programa, adequadas para comparar tratamentos e impróprias para apresentar como exigência normativa.*


> **As classes 2 a 4 são adaptações do programa, não de uma norma.** O próprio Triton o declara no ecrã e no relatório. Num estudo publicado, não as apresente como exigência normativa: apresente-as como critério adotado, e cite a origem.

---

### 4.6.2. A classe recomenda, o utilizador decide

Escolher uma classe não impõe nenhum equipamento ao projeto. A classe exprime uma recomendação do programa, fundada na exigência típica do uso pretendido, e a decisão de a adotar ou não fica com quem assina o projeto.

<!-- tabela: **Tabela 105** — Linha de tratamento conforme a tecnologia de desinfeção adotada: etapas, energia ultravioleta e carbono anual -->
| Desinfeção | Etapas | Energia UV anual | CO₂e anual |
| :--- | :---: | ---: | ---: |
| Cloragem por pastilhas | 1 | 0,0 kWh | 0,2 kg |
| Cloragem + ultravioleta | 2 | 37,5 kWh | 18,2 kg |
| Cloragem + ozonização | 2 | 0,0 kWh | 15,2 kg |

<!-- tabela: **Tabela 106** — Recomendação de filtração fina por classe de qualidade -->
| Classe de destino | Recomenda-se filtração fina? |
| :--- | :---: |
| classe 1 | não |
| classe 2 | sim |
| classe 3 | sim |
| classe 4 | sim |

A segunda tabela revela o ponto: sem o filtro de polimento, as quatro classes custam exatamente o mesmo. A classe-alvo altera uma única coisa, que é se o programa recomenda ou não a filtração fina, e o filtro correspondente só entra no orçamento quando o utilizador o assinala explicitamente.

Quando a classe recomenda o polimento e o utilizador o recusa, o programa regista a recusa no relatório, em vez de impor o equipamento em silêncio ou de deixar a decisão passar sem registo. ==É a conduta correta em qualquer programa de projeto: quem assina decide, e a decisão fica documentada para quem vier depois.==

---

### 4.6.3. A desinfeção

A desinfeção é a etapa de que depende a segurança microbiológica da água armazenada, e o programa oferece três tecnologias. A diferença entre elas é grande, em custo e em comportamento, e o critério que as separa não é a eficácia de desinfeção — as três desinfetam — mas a persistência do efeito.

**Cloragem por pastilhas.** Um doseador com pastilhas de hipoclorito de cálcio na linha, numa só etapa. É a opção predefinida. Deixa **residual** na água, o que protege o reservatório e a rede interior contra a recontaminação. A edição não traz catálogo de equipamentos, pelo que o custo da linha é o que indicar na etapa económica, a partir dos seus orçamentos; este manual não cita nenhum preço de equipamento de tratamento.

**Ultravioleta.** Um reator com lâmpada UV, numa segunda etapa a seguir à cloragem. A lâmpada e o reator consomem 37,5 kWh por ano neste projeto. **Não deixa residual**: desinfeta o que passa por ele, e nada protege a água depois.

**Ozonização.** Também uma segunda etapa a seguir à cloragem, também sem residual.

> **Atenção.** No programa, o ultravioleta e o ozono entram como barreira **adicional** à cloragem, não como substitutos. É a prática correta: sem residual, a água tratada volta a contaminar-se no caminho até ao ponto de uso.
>
> Por isso, as linhas de UV e de ozono somam-se à do cloro em vez de a substituir. Quem esperava que trocar o cloro pelo UV **reduzisse** o custo verá o contrário.

O impacto de carbono segue a mesma ordem: 0,2 kg CO₂e por ano com cloragem, 18,2 com ultravioleta e 15,2 com ozonização, para o volume tratado neste projeto, com o fator de rede ilustrativo de 0,40 kg CO₂e/kWh. A diferença está toda na eletricidade consumida pela lâmpada e pelo gerador de ozono, já que o consumível químico da cloragem tem uma emissão de fabrico modesta em comparação.

---

### 4.6.4. O filtro de entrada

Antes de qualquer desinfeção vem o filtro mecânico de entrada, que retira folhas e sólidos grosseiros da água antes de ela chegar ao reservatório. O programa dimensiona-o pela área da cobertura, e não pela classe de qualidade pretendida, porque o que este filtro tem de vencer é o caudal de ponta da cobertura — uma grandeza que não depende do destino final da água.

<!-- tabela: **Tabela 107** — Filtro mecânico de entrada dimensionado pela área da cobertura -->
| Cobertura | Filtro | Malha |
| :--- | :--- | ---: |
| até 200 m² | vórtex autolimpante DN 100 | 350 µm |
| até 500 m² | vórtex autolimpante DN 150 | 400 µm |
| acima | cesto ou ciclónico DN 200 | 500 µm |

A nossa cobertura de 150 m² fica no primeiro escalão. Estes filtros retêm partículas de algumas centenas de micrómetros, muito abaixo de um milímetro; a ETA 0701 recomenda, para o filtro a montante da cisterna, uma malha entre 0,2 mm e 0,8 mm (item 4.4.2).

---

### 4.6.5. A regra incremental do custo

O investimento na linha de tratamento não se soma por inteiro ao investimento total do sistema, para evitar a dupla contagem. O orçamento de um sistema pluvial já reserva uma verba genérica de tratamento na rubrica dos acessórios, porque nenhum projetista orça um sistema sem prever alguma filtragem; somar a linha detalhada por cima dessa verba cobraria o tratamento duas vezes. O programa desconta a verba genérica e soma só o incremento, como a Equação 31 formaliza na secção 2.5.

O mesmo vale para o custo de exploração: a cloragem já se paga na linha de consumíveis químicos do fluxo de caixa, e a linha de tratamento desconta essa parcela para não cobrar duas vezes o hipoclorito.

E na avaliação do ciclo de vida, a linha de tratamento **substitui** o termo da cloragem em vez de se lhe somar. A secção 2.5 detalha a regra.

---

### 4.6.6. A decisão do tutorial

**Classe 1, cloragem por pastilhas, sem filtro de polimento.**

A água vai para o autoclismo e para a área exterior. A classe 1, o conjunto mínimo de referência do programa (um limite de *E. coli*, a turvação e o pH, com um intervalo de cloro livre), cobre ambos. Um projeto que acrescente a máquina de lavar roupa sai dos usos que a maioria das normas lista, e o responsável tem de definir e declarar o critério de qualidade para ela, como a secção 4.2 regista. A cloragem deixa residual, é a mais simples das três linhas, e tem a energia e o carbono mais baixos: 0,2 kg CO₂e por ano. O descarte inicial dimensiona-se na mesma etapa; a sua câmara é a de 300 L da secção 4.1.

<!-- tabela: **Tabela 108** — Estado do projeto do tutorial depois da definição da classe de qualidade -->
| Projeto até aqui | |
| :--- | ---: |
| volume | 5 000 L |
| classe de qualidade | 1, conjunto mínimo de referência |
| desinfeção | cloragem por pastilhas |
| filtro de polimento | não |
| carbono anual da linha de tratamento | 0,2 kg CO₂e |

Temos volume, arranjo e qualidade. Agora, a pergunta que decide se o projeto sai do papel.

---

## 4.7. Quanto custa e em quanto tempo se paga

> No fim desta secção, tem o fluxo de caixa a vinte anos e sabe porque a **estrutura tarifária da entidade gestora** decide a viabilidade mais do que qualquer parâmetro do projeto.

> **Os custos deste manual são ilustrativos.** A Edição Ibérica não traz lista de preços. Todos os custos do tutorial são números redondos, em euros, escolhidos para se poder seguir o método; são **ilustrativos, não são preços de mercado**. A tarifa é a exceção: é o tarifário de Lisboa guardado no projeto de exemplo. No seu estudo, introduza na etapa económica os seus orçamentos e a tarifa que paga. O cálculo que se segue é o mesmo, e a lição sobre as estruturas tarifárias também.

---

### 4.7.1. A poupança é a diferença entre duas faturas

O erro mais comum na análise económica de sistemas pluviais é multiplicar o volume poupado por uma tarifa média. O resultado quase nunca está certo, e a razão está na estrutura das tarifas, que em muitos concelhos são progressivas por escalões de consumo, como detalha a secção 3.3: ==o metro cúbico que se deixa de consumir é o último da fatura, o mais caro, e não o médio.== A fatura portuguesa soma ainda várias parcelas — água, saneamento e resíduos —, o que acrescenta um segundo efeito.

O Triton evita o problema calculando duas faturas completas — a que o edifício pagaria sem o sistema e a que paga com ele — e tomando a diferença entre as duas.

<!-- tabela: **Tabela 109** — Composição da fatura de água, saneamento e resíduos de Lisboa antes e depois do sistema pluvial -->
| A fatura de água, saneamento e resíduos de Lisboa | Consumo | Valor |
| :--- | ---: | ---: |
| sem o sistema | 18,26 m³/mês | 46,25 € |
| com o sistema | 15,00 m³/mês | 35,06 € |
| **poupança** | 3,27 m³/mês | **11,19 €** |

<!-- tabela: **Tabela 110** — Indicadores económicos do projeto do tutorial em vinte anos de análise (todos os custos são ilustrativos, não são preços de mercado) -->
| Análise a vinte anos (custos ilustrativos, não são preços de mercado) | Valor |
| :--- | ---: |
| investimento inicial | 6 650,00 € |
| poupança anual na água | 134,28 € |
| custo anual de exploração | 1,75 € |
| valor atual líquido | −5 828,77 € |
| taxa interna de rentabilidade | −11,30% ao ano |
| período de recuperação descontado | sem recuperação |

O resultado merece atenção. O sistema poupa 3,27 m³ por mês e a fatura baixa 11,19 €, o que dá 3,42 € por metro cúbico poupado. É mais do que a média da fatura sem o sistema, 2,53 € por metro cúbico (46,25 € para 18,26 m³). A diferença vem de a poupança incidir sobre os escalões mais altos e de a fatura de Lisboa somar à água o saneamento e os resíduos, ambos cobrados em função do volume de água: cada metro cúbico que não é tirado da rede também não é descarregado nem contado para os resíduos.

> **O saneamento acompanha a parcela da água, não a fatura total.** Poupar água poupa as duas parcelas, e é por isso que o valor efetivo do metro cúbico poupado fica acima do preço da água.

---

### 4.7.2. O tarifário de Lisboa

A fatura de Lisboa soma três tarifários. A água é da EPAL, com IVA a 6% e o adicional da Câmara Municipal de Lisboa. O saneamento e os resíduos urbanos são tarifários da Câmara. Os três estão transcritos em `triton/data/portugal_tarifarios.json` a partir dos documentos de 2026: EPAL, *Preços de venda de água* (https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0), e Câmara Municipal de Lisboa, tarifários do saneamento e dos resíduos urbanos (https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf e https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf; recolhidos em 07/10/2026). Com 10 m³ por mês, a fatura completa é de 25,87 €.

Há dúvidas por resolver no tratamento do IVA do saneamento e dos resíduos, e o adicional da Câmara vem impresso na tabela da EPAL sem indicar se leva IVA (ver `examples/LEIA.md`). O programa trata-os sem IVA. [A COMPLETAR: confirmar com a EPAL e com a Câmara Municipal de Lisboa o tratamento do IVA nestas parcelas.]

Nem todas as entidades gestoras adotam a mesma estrutura, e a diferença decide a viabilidade de projetos inteiros. O programa distingue seis regimes.

<!-- tabela: **Tabela 111** — Os seis regimes tarifários e o efeito de cada um sobre a poupança -->
| Regime | O que acontece ao poupar |
| :--- | :--- |
| tarifa de disponibilidade | cada m³ poupado desconta |
| fórmula exponencial | cada m³ poupado desconta, pelo preço-base elevado ao expoente |
| sem mínimo | idem |
| franquia no mínimo | poupar abaixo da franquia **não desconta nada** |
| franquia retroativa | ao passar a franquia, tarifa-se tudo desde zero |
| piso de pagamento | a fatura não desce abaixo do piso |

> **Atenção, e é o ponto que deita abaixo mais estudos.** Quando a entidade gestora cobra um valor fixo que já inclui uma **franquia**, digamos 10 m³, uma casa que consome 12 m³ e poupa 3 desce para 9, entra na franquia, e **a fatura deixa de baixar**. O sistema poupa água e não poupa dinheiro.
>
> Correr esse caso com uma tarifa média produziria um período de recuperação que não existe. A secção 3.3 ensina a montar corretamente a estrutura do seu tarifário.

---

### 4.7.3. O investimento

6 650 €, assim distribuídos (todos os valores ilustrativos, não são preços de mercado):

<!-- tabela: **Tabela 112** — Composição do investimento inicial do projeto do tutorial (ilustrativo, não é preço de mercado) -->
| Rubrica | Valor (ilustrativo, não é preço de mercado) |
| :--- | ---: |
| cisterna de betão de 5 000 L | 2 600 € |
| reservatório superior de 1 000 L em polietileno | 650 € |
| duas eletrobombas de meio cv, principal e de reserva | 500 € |
| mão de obra e escavação | 1 500 € |
| tubagem | 600 € |
| acessórios | 800 € |
| **total** | **6 650 €** |

Os preços dos reservatórios seguem uma regra ilustrativa simples, uma parte fixa mais uma parte por litro, diferente para cada material: polietileno 100 + 0,55 por litro, betão 600 + 0,40, fibra de vidro 120 + 0,65 e aço inoxidável 300 + 2,00. Uma cisterna de betão de 5 000 L fica, assim, em 600 + 2 000 = 2 600. Não são preços de catálogo; num estudo real, substitua-os por orçamentos.

**A câmara de descarte.** O descarte das primeiras águas não é só a lâmina subtraída à chuva: é um componente físico, com custo. A etapa **3. Qualidade & ETAP** dimensiona-o por predefinição, e no tutorial a lâmina de 2 mm sobre 150 m² exige uma câmara de 300 L. Neste orçamento ilustrativo, o seu custo está dentro da linha dos acessórios. Um estudo que deixe o descarte fora do orçamento, mas o subtraia à chuva, parece mais viável do que o sistema que se constrói. A secção 2.5 detalha o dimensionamento.

---

### 4.7.4. O CAPEX nesta edição: o programa não calcula preços de Portugal

Na Edição Brasil, o investimento de um projeto novo vem preenchido por uma cadeia de cálculo que parte de preços de mercado. **Nesta edição essa cadeia não existe.** Os preços de reservatórios, tubagem, eletrobombas, mão de obra e acessórios ficam a zero, por decisão: não se encontrou fonte oficial aberta para eles e nenhum foi inventado. O programa dimensiona o sistema, calcula a poupança na fatura e a energia, mas o investimento é o que o utilizador introduzir.

<!-- tabela: **Tabela 113** — O que um projeto novo da Edição Ibérica traz preenchido e o que fica por definir pelo utilizador -->
| Campo do projeto novo | Valor | O que significa |
| :--- | ---: | :--- |
| cisterna e reservatório superior | 0,00 € | por definir pelo utilizador |
| tubagem, acessórios e mão de obra | 0,00 € | por definir pelo utilizador |
| preço de cada eletrobomba | 0,00 € | por definir; o projeto parte de 2 eletrobombas, serviço e reserva |
| tarifa de eletricidade | 0,0000 €/kWh | por definir; sem ela a energia da bomba custa zero |
| preço do cloro | 0,00 €/kg | por definir; sem ele o cloro custa zero |
| rotinas de manutenção | 3 rotinas, periodicidade de 12 meses, 0,00 € no total | os nomes ficam como roteiro; os custos são do utilizador |
| orçamento automático do arranjo 3D | desligado | os preços das peças são em reais, de origem brasileira |
| mão de obra automática | desligado | idem |
| preços de catálogo (reservatórios, tratamento) | desligado | a linha de tratamento é dimensionada, mas não custa nada |
| base de custos interna (`costs_database.json`) | 27 fatores regionais | valores em reais, de origem brasileira; não são usados nesta edição |
| dose de cloro e pureza da pastilha | 1,5 mg/L e 65% | parâmetros técnicos, não são preços |
| tarifário de água, saneamento e resíduos | Lisboa, desde 01/01/2026 | **inserido automaticamente**; transcrito dos documentos de 2026 |
| taxa de atualização | 2,0% ao mês | valor genérico do núcleo, não é dado de Portugal |
| inflação dos custos | 0,2% ao mês | idem |
| atualização das tarifas de água, saneamento e eletricidade | 5,0%, 5,0% e 5,0% ao ano | idem |

A única coisa que o programa insere sozinho, nesta matéria, é o tarifário de água, saneamento e resíduos de Lisboa, transcrito dos documentos de 2026 (secção 3.3). Tudo o que é preço de obra, de equipamento ou de manutenção, e a tarifa de eletricidade, está por definir.

#### 4.7.4.1. O que isto significa para si

Sem os seus valores, o investimento é zero e a análise económica mostra apenas a poupança na fatura de água. O valor atual líquido e o período de recuperação, nessas condições, dizem pouco: não são resultados. A linha de tratamento e o descarte são dimensionados, entram no balanço de carbono, mas não custam nada. Só tem uma análise económica quando introduzir orçamentos reais.

A base de custos interna do programa (`costs_database.json`) existe nas três edições, mas os seus valores são em reais e de origem brasileira, com fatores regionais para as unidades federativas do Brasil. Nesta edição está desligada: não é usada em nenhum cálculo, e não deve ser tomada como referência de preços europeus.

#### 4.7.4.2. Como introduzir os seus valores

Na etapa **4. Reservatório & Custos**, o botão *1. Investimento Inicial (CAPEX)* tem campos para o reservatório superior, a mão de obra, a tubagem e os acessórios; o botão *2. Eletrobomba e Custo de Energia* tem o preço da eletrobomba e a tarifa de eletricidade; e o botão *3. Outros Custos Operacionais* tem as rotinas de manutenção. Introduza ali os valores dos seus orçamentos, com IVA se o investimento for suportado pelo consumidor final.

Há duas limitações a conhecer. O diálogo do CAPEX **não tem campo para o preço da cisterna** e, ao confirmar, repõe esse preço a zero. Enquanto isso não for corrigido, some o preço da cisterna a uma das linhas do diálogo, por exemplo os acessórios, e registe a escolha no relatório, ou escreva o valor no campo `cost_lower_tank` do bloco `capex_and_opex` do ficheiro do projeto e não confirme o diálogo do CAPEX depois disso. O mesmo acontece com o preço do cloro, que só existe no ficheiro do projeto, no bloco `water_quality_and_etap`; em alternativa, acrescente em *3. Outros Custos Operacionais* uma rotina de custo variável por metro cúbico de água de chuva.

Os valores do tutorial deste capítulo são ilustrativos. Não os copie para um estudo real:

<!-- tabela: **Tabela 114** — Parâmetros ilustrativos do tutorial, que não são preços de mercado, e onde o utilizador os troca pelos seus -->
| Parâmetro do tutorial | Valor ilustrativo | Onde o utilizador o troca |
| :--- | ---: | :--- |
| mão de obra e escavação | 1 500,00 € | CAPEX, mão de obra |
| tubagem | 600,00 € | CAPEX, tubagens |
| acessórios | 800,00 € | CAPEX, acessórios |
| eletrobomba, por unidade | 250,00 € | eletrobomba e custo de energia |
| tarifa de eletricidade | 0,20 €/kWh | eletrobomba e custo de energia |
| cloro, por quilograma de produto | 8,00 € | só no ficheiro do projeto |
| taxa de atualização | 0,4% ao mês | etapa 4 |
| inflação dos custos | 0,2% ao mês | etapa 4 |
| atualização das tarifas | 3,0% ao ano | etapa 4 |
| rotina: inspeção e limpeza das caleiras e do pré-filtro | 20,00 € a cada 12 meses | outros custos operacionais |
| rotina: limpeza e inspeção da cisterna | 40,00 € a cada 12 meses | outros custos operacionais |
| rotina: manutenção preventiva da bomba | 30,00 € a cada 12 meses | outros custos operacionais |
| reservatório de polietileno | 100,00 € mais 0,55 € por litro | só neste manual; o programa não tem esta regra |
| reservatório de betão | 600,00 € mais 0,40 € por litro | só neste manual; o programa não tem esta regra |
| reservatório de fibra de vidro | 120,00 € mais 0,65 € por litro | só neste manual; o programa não tem esta regra |
| reservatório de aço inoxidável | 300,00 € mais 2,00 € por litro | só neste manual; o programa não tem esta regra |

#### 4.7.4.3. Uma tabela de preços de Portugal: planeada, não implementada

O plano é uma tabela opcional, que o utilizador ligaria de propósito, com cinco itens em euros: reservatório por volume, tubagem, eletrobomba, mão de obra e acessórios. Cada preço levaria o endereço da fonte, a data de acesso e a soma de verificação do documento. A tabela não teria indexação nem faixa percentual inventada, recusaria extrapolar fora da faixa de volumes recolhida e mostraria uma tarja vermelha quando os preços tivessem mais de 18 meses. Espanha ficaria vazia até haver recolha. **Nada disto existe no programa.** O que existe é o plano, em `PLANO_AUTOMACAO_TARIFAS_E_CUSTOS_IBE.md`, e o princípio: nenhum preço entra sem documento aberto.

---

### 4.7.5. O resultado

A segunda tabela acima dá os indicadores.

**O projeto não se paga, e esse é o resultado honesto.** Ao fim de vinte anos, com estes custos ilustrativos e o tarifário de Lisboa, o valor atual líquido (VAL) é de −5 828,77 €, a taxa interna de rentabilidade é de −11,30% ao ano, e não há período de recuperação descontado dentro do horizonte. Não ajustámos os custos até aparecer uma recuperação.

A razão não é um defeito do exemplo. A água é barata em Lisboa em relação ao que custam uma cisterna, duas bombas e a mão de obra, e a fração de 28% limita a poupança a pouco mais de três metros cúbicos por mês, 134,28 € por ano. Um tarifário que premeie mais o metro cúbico, uma fração atendível maior ou uma instalação mais barata mudam a conta, e a secção 3.7 varia cada um deles por sua vez. Mostra também que nenhuma das premissas testadas, isoladamente, produz recuperação neste caso. Só o tutorial leva custos, pelo que a secção 3.1 compara as três cidades pelo potencial de poupança, e não pela recuperação.

**O custo de exploração é pequeno:** 1,75 € por ano, dos quais 1,03 € são a energia da elevação, os 5,1 kWh por ano da secção 4.5 a 0,20 € por quilowatt-hora (valor ilustrativo, não é preço de mercado). A energia vem da mesma função que alimenta a avaliação ambiental, conforme o arranjo indicado na etapa **4. Reservatório & Custos**: elevação, pressurização direta ou gravidade. Este valor não inclui as três rotinas de manutenção ilustrativas, que somam 90,00 € por ano e entram no fluxo de caixa à parte; a secção seguinte mostra o peso delas.

---

O resultado de um volume isolado diz pouco sem os vizinhos. O separador económico repete a conta para todos os volumes da varredura e traça a curva, e é nela que se vê se o ótimo técnico e o ótimo económico caem no mesmo sítio (Figura 58).

![O valor atual líquido contra o volume do reservatório](../figuras/fig49_programa_vpl.png)

*Figura 58 — O gráfico do separador económico: o valor atual líquido de cada volume da varredura, com o máximo económico e o ótimo técnico marcados. Quando os dois coincidem, o programa assinala-os com um único símbolo. Todos os custos são ilustrativos, não são preços de mercado. Figura gerada pelo próprio programa.*

---

### 4.7.6. O que entra no custo de exploração (OPEX)

Também aqui o programa não pré-preenche preços. O custo de exploração de um projeto novo soma a energia da eletrobomba, o cloro, a linha de tratamento e as rotinas de manutenção, e **todos esses preços partem de zero**: a tarifa de eletricidade, o preço do cloro e o custo de cada rotina. As três rotinas de manutenção existem como roteiro, com periodicidade de 12 meses, e o utilizador dá-lhes o custo.

O que o programa calcula sozinho são as quantidades: a energia anual da eletrobomba, pela cadeia da secção 2.6, e os quilogramas de cloro, pela dose e pela pureza da pastilha. O custo é a quantidade vezes o preço que o utilizador introduzir. Com preço zero, o custo é zero, e não um valor omitido.

**As rotinas pesam mais que o resto.** O campo de custo anual que o resumo da análise mostra soma só a energia, o cloro e a linha de tratamento. As rotinas de manutenção entram no fluxo de caixa à parte, no fim de cada período, corrigidas pela inflação. No tutorial, com valores ilustrativos, elas movem o resultado:

<!-- tabela: **Tabela 115** — Efeito das três rotinas de manutenção ilustrativas sobre o custo do resumo e sobre o resultado do tutorial (custos ilustrativos, não são preços de mercado) -->
| Projeto do tutorial (custos ilustrativos, não são preços de mercado) | Com as rotinas | Sem rotinas |
| :--- | ---: | ---: |
| rotinas de manutenção por ano | 90,00 € | 0,00 € |
| custo anual do resumo: energia, cloro e tratamento | 1,75 € | 1,75 € |
| valor atual líquido | −5 828,77 € | −4 418,13 € |

**Energia.** Hoje a tarifa de eletricidade é um campo vazio. O exemplo do Funchal traz 0,1673 €/kWh, a Tarifa Base da Empresa de Eletricidade da Madeira, sem IVA, recolhida num comparador de preços e por isso de fonte secundária; Lisboa e Porto ficam a zero. Para um estudo, use a sua fatura.

Recolheram-se séries públicas que servirão de ponto de partida, mas **ainda não estão ligadas ao programa**: nenhum valor da tabela seguinte é inserido sozinho. O preço do Eurostat é a média de um domicílio inteiro, na banda de 2 500 a 4 999 kWh por ano, e não o preço marginal de uma eletrobomba; a fatura do utilizador prevalece sempre.

<!-- tabela: **Tabela 116** — Séries públicas recolhidas fora do programa, ainda não ligadas a ele, com a data de acesso e o início da soma de verificação -->
| Série pública | Portugal | Espanha | Acesso | SHA-256 (início) |
| :--- | ---: | ---: | :--- | :--- |
| eletricidade doméstica, com impostos (2026-S1) | 0,2367 €/kWh | 0,2509 €/kWh | 2026-10-22 | `b92782d29f15` |
| eletricidade doméstica, sem impostos (2026-S1) | 0,1576 €/kWh | 0,1782 €/kWh | 2026-10-22 | `c9ad0130f1ef` |
| inflação anual (IPCH) (2025) | 2,2 % ao ano | 2,7 % ao ano | 2026-10-22 | `ad3c84f4b19c` |
| taxa de refinanciamento do BCE (2026-09-16) | 2,65 % | zona euro: o mesmo valor | 2026-10-22 | `0dedb876aea5` |

O plano é pré-preencher a tarifa com o valor do Eurostat do país, rotulado como média de um domicílio inteiro e editável, a inflação com o IPCH e a taxa de atualização com uma referência do BCE. **Não está implementado.** O cloro e as manutenções continuarão sem custo até haver fonte aberta para eles, e o índice de custos de construção, que serviria para atualizar preços já recolhidos, ainda nem foi localizado na fonte oficial.

**O que não entra.** O fluxo de caixa não traz reposição de equipamentos ao longo dos 20 anos, valor residual, análises laboratoriais da água nem seguro. Se a eletrobomba ou o filtro forem substituídos no período, acrescente a substituição como uma rotina em *3. Outros Custos Operacionais*.

**Como alterar ou desligar.** As rotinas editam-se, excluem-se ou acrescentam-se no botão *3. Outros Custos Operacionais*. A dose de cloro e o descarte físico escolhem-se na etapa **3. Qualidade & ETAP**. A tarifa e os impostos da eletricidade ficam em *2. Eletrobomba e Custo de Energia*.

---
### 4.7.7. O que a projeção assume

Vinte anos são muito tempo, e a projeção depende de premissas que convém declarar:

<!-- tabela: **Tabela 117** — Premissas da projeção económica e o peso de cada uma no resultado -->
| Premissa | Valor adotado | Onde pesa |
| :--- | ---: | :--- |
| taxa de atualização | 0,4% ao mês | desconta o fluxo; quanto maior, pior o VAL |
| inflação dos custos | 0,2% ao mês | incide só sobre o custo de exploração |
| atualização da tarifa da água | 3% ao ano | incide sobre a poupança |
| atualização da tarifa do saneamento | 3% ao ano | idem, e é indexada à parte |
| intervalo de atualização | 12 meses | em degraus, não de forma contínua |
| período de análise | 20 anos | a vida útil adotada; declare-a e justifique-a |

Todos estes valores são escolhas ilustrativas do tutorial, não dados de um país.

> **As atualizações da água e do saneamento são separadas**, e não um índice único sobre a fatura agregada. As duas parcelas são muitas vezes atualizadas por decisões diferentes das entidades que as cobram, e tratá-las em conjunto indexa parte da conta pelo índice errado.

A atualização da tarifa é a premissa mais frágil da lista. Três por cento ao ano durante vinte anos multiplicam a tarifa por 1,81. Se a tarifa real subir mais do que isso, o projeto rende mais; se subir menos, rende menos. Um estudo sério declara o valor adotado e mostra a sensibilidade — a secção 3.7 ensina como.

---

### 4.7.8. O que temos até aqui

<!-- tabela: **Tabela 118** — Estado do projeto do tutorial depois da análise económica (ilustrativo, não é preço de mercado) -->
| Projeto até aqui (ilustrativo, não é preço de mercado) | |
| :--- | ---: |
| volume | 5 000 L, betão |
| arranjo | elevação para reservatório superior de 1 000 L |
| investimento | 6 650 € |
| poupança anual | 134,28 € |
| VAL a 20 anos | −5 828,77 € |
| período de recuperação | sem recuperação em 20 anos |

O dinheiro diz não.

Falta ouvir o carbono. E ele não vai simplesmente concordar.

---

## 4.8. Quanto carbono evita

> No fim desta secção, tem o balanço de carbono do sistema e uma surpresa: com a cisterna que escolhemos, o projeto **emite mais do que evita** ao longo da vida útil. E a troca de material, ao contrário do que seria de esperar, não resolve o problema.

---

### 4.8.1. A conta

Um sistema de aproveitamento pluvial evita emissões porque cada metro cúbico que entrega deixa de ser captado, tratado e bombeado pela entidade gestora, e estas três operações consomem energia. O mesmo sistema, porém, emite carbono em três frentes próprias: o fabrico dos seus componentes, a energia consumida na bombagem interior e os consumíveis de tratamento aplicados à água.

O saldo ambiental do sistema é a diferença entre o que evita e o que emite, e a pergunta que organiza esta secção é em quantos anos o crédito anual líquido amortiza a dívida contraída no fabrico. Esse prazo é o **retorno do carbono**, e desempenha na dimensão ambiental o papel que o período de recuperação desempenha na dimensão económica.

> **Os fatores são ilustrativos.** A Edição Ibérica não traz fatores de emissão: a avaliação ambiental não é calculada até introduzir os do local do projeto (apêndice C). O tutorial usa dois números redondos, **0,40 kg CO₂e por quilowatt-hora** de eletricidade da rede e **0,50 kg CO₂e por metro cúbico** de água da rede evitada. São ilustrativos, não são dados de nenhum país, escolhidos para se poder seguir o método; a lição está na forma do resultado, não nos dígitos. [A COMPLETAR: se se quiser fatores portugueses, indicar a fonte oficial aberta (fator de emissão da eletricidade da rede e intensidade carbónica do abastecimento de água em Portugal) e o ano; este manual não os cita.]

Para o nosso projeto, uma cisterna de betão de 5 000 L com elevação para o reservatório superior de 1 000 L:

<!-- tabela: **Tabela 119** — Balanço de carbono do projeto do tutorial com cisterna de betão (fatores ilustrativos) -->
| Parcela | Valor |
| :--- | ---: |
| carbono incorporado no sistema | 1 026 kg CO₂e |
| emissão evitada por ano | 19,6 kg CO₂e |
| emissão anual de bombagem e tratamento | 2,2 kg CO₂e |
| saldo líquido anual | 17,4 kg CO₂e |
| **retorno do carbono** | **59,0 anos** |
| saldo ao fim de 20 anos | **+678 kg CO₂e** |

São 59 anos para amortizar a dívida de carbono, contra uma vida útil adotada de vinte. ==O sistema não se paga, portanto, do ponto de vista ambiental:== quando for desativado, terá emitido 678 kg CO₂e a mais do que evitou durante toda a operação.

E o resultado financeiro do mesmo projeto também foi negativo (secção 4.7). Os dois veredictos coincidem, mas por razões diferentes, e as secções seguintes mostram-no: o carbono é decidido pela massa da cisterna, o dinheiro pela tarifa. É por isso que as dimensões de análise devem ser mantidas separadas até ao momento da decisão.

---

### 4.8.2. Porque a poupança de carbono é tão pequena

Dezanove quilogramas e meio de CO₂e por ano parecem pouco para 39,2 metros cúbicos de água poupada, e com estes fatores são: 0,50 kg CO₂e por metro cúbico substituído, descontada a energia para o bombear.

A explicação está na natureza do produto substituído. A água tratada não é um bem intensivo em carbono. Captar, tratar e distribuir a água custa uma fração de quilograma de CO₂e por metro cúbico entregue, conforme o mix elétrico local e a origem da água, e isso é modesto quando comparado com o carbono do betão, do aço ou dos combustíveis. Substituir um produto de baixa intensidade de carbono por outro que exige o fabrico de um reservatório não produz, portanto, o ganho ambiental que a intuição sugere.

> **A fronteira importa.** O fator do programa é por metro cúbico **entregue** ao edifício, e não por metro cúbico produzido na estação. As perdas na distribuição fazem com que um metro cúbico produzido entregue menos de um: usar o fator à saída da estação subestimaria a emissão evitada. A secção 2.8 detalha.

---

O separador ambiental apresenta o mesmo balanço em forma gráfica, com as parcelas de emissão e o crédito da água evitada separados (Figura 59).

![O balanço de carbono em vinte anos, por componente](../figuras/fig50_programa_balanco_ambiental.png)

*Figura 59 — O gráfico do separador ambiental para o mesmo projeto, com cisterna de betão: as parcelas do balanço de carbono em vinte anos, com fatores ilustrativos. O sinal segue a convenção adotada em todo este capítulo: emissões positivas, água evitada negativa. Figura gerada pelo próprio programa.*

---
### 4.8.3. O material muda a dimensão, não o sinal

A dívida de carbono está quase toda na cisterna. E uma cisterna de 5 000 L pode pesar 75 kg ou 6 000 kg, conforme o material. A tabela seguinte e a Figura 60 mostram a trajetória das emissões líquidas ao longo da vida útil, e a Figura 61 o resultado final de cada material.

==Em todo este capítulo, **positivo emite e negativo retira**. É a convenção do gráfico de balanço do separador ambiental do programa, e a que mantém intuitiva a leitura de um gráfico de emissões: a linha que desce é a que melhora.==

<!-- tabela: **Tabela 120** — Emissões líquidas de carbono do projeto do tutorial conforme o material do reservatório (os preços são ilustrativos, não são preços de mercado) -->
| Material da cisterna | Massa | Carbono incorporado | Retorno do carbono | Emissões líquidas em 20 anos | Preço (ilustrativo, não é preço de mercado) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Polietileno (PEAD) | 110 kg | 363 kg CO₂e | 20,9 anos | 15 kg | 2 850 € |
| Betão armado | 6 000 kg | 1 026 kg CO₂e | 59,0 anos | 678 kg | 2 600 € |
| Fibra de vidro | 75 kg | 429 kg CO₂e | 24,7 anos | 81 kg | 3 370 € |
| Aço inoxidável | 190 kg | 889 kg CO₂e | 51,1 anos | 541 kg | 10 300 € |

<!-- tabela: **Tabela 121** — Efeito do volume da cisterna de betão nas emissões líquidas de carbono -->
| Volume em betão | Retorno do carbono | Emissões líquidas em 20 anos |
| ---: | ---: | ---: |
| 2 000 L | 37,1 anos | 240 kg CO₂e |
| 3 000 L | 44,4 anos | 379 kg CO₂e |
| 5 000 L | 59,0 anos | 678 kg CO₂e |
| 8 000 L | 80,0 anos | 1 147 kg CO₂e |

![Saldo de carbono acumulado ao longo da vida útil, por material](../figuras/fig06_carbono_no_tempo.png)

*Figura 60 — Emissões líquidas acumuladas da cisterna de 5 000 L ao longo da vida útil, para polietileno e betão, com fatores ilustrativos. A curva parte do carbono incorporado no fabrico, acima de zero, e desce com o crédito anual da água potável evitada; o polietileno cruza o zero aos 20,9 anos, logo depois do horizonte de vinte anos adotado, e o betão aos 59,0 anos.*

![Emissões líquidas em vinte anos, por material da cisterna](../figuras/fig04_materiais.png)

*Figura 61 — Emissões líquidas em vinte anos da cisterna de 5 000 L, por material, com fatores ilustrativos. Os quatro materiais encerram a vida útil a emitir mais do que evitaram; o polietileno fica praticamente na fronteira (+15 kg) e o betão, o mais pesado, longe dela (+678 kg).*

**A escolha do material muda a dimensão do problema, mas aqui não inverte o sinal.**

Com a chuva de Lisboa, que dá pouca água poupada, nenhum material paga o próprio fabrico em vinte anos. O polietileno leva 20,9 anos e termina os vinte anos a emitir ainda 15 kg: está praticamente na fronteira. A fibra de vidro leva 24,7 anos e termina com +81 kg. O aço inoxidável leva 51,1 anos e termina com +541 kg. O betão leva 59,0 anos e termina com +678 kg. Com 28% de fração atendível e 39,2 m³ poupados por ano, só os materiais leves chegam perto de pagar o fabrico.

A segunda tabela mostra o outro lado da mesma moeda: em betão, **quanto maior a cisterna, pior o carbono**. A de 2 000 L fecha os vinte anos a emitir 240 kg; a de 8 000 L, 1 147 kg, e o seu retorno do carbono estica-se até 80,0 anos. Cada metro cúbico de betão acrescenta cerca de 150 kg CO₂e e rende cada vez menos água.

---
### 4.8.4. Existe um volume ambientalmente ótimo

A observação anterior vale para o betão, mas é um caso particular de algo mais geral. O carbono incorporado cresce de forma quase afim com o volume; a água evitada cresce com o atendimento, que satura. A soma das duas parcelas tem um **mínimo interior**: existe um volume a partir do qual cada litro a mais de armazenamento emite mais do que evita. A Figura 62 mostra as duas curvas.

![Emissões líquidas em vinte anos contra o volume da cisterna](../figuras/fig06b_otimizacao_ambiental.png)

*Figura 62 — Emissões líquidas em vinte anos contra o volume da cisterna, para (a) polietileno e (b) betão, no projeto do tutorial, com fatores ilustrativos. Em polietileno (com o reservatório superior de 1 000 L), o balanço é o melhor, entre os volumes testados, aos 2 000 L, onde retira 25 kg; passa a emissão entre 4 000 e 5 000 L (retira 5 kg aos 4 000 L e emite 15 kg aos 5 000 L) e emite 194 kg aos 12 000 L. Em betão, as emissões líquidas são positivas em toda a gama.*

==Mais armazenamento não é monotonicamente melhor para o clima.== É o contrário do que a intuição corrente sugere, e decorre de uma propriedade simples: a saturação do atendimento. O volume que minimiza as emissões (2 000 L) não é o que maximiza a poupança de água, nem o que o critério do ganho marginal escolheu (5 000 L) — e a secção 4.9 trata de como decidir entre eles.

> **O material mais leve é também o melhor para o carbono, a um preço próximo.** Com os preços ilustrativos, o polietileno custa 2 850 € contra 2 600 € do betão (ilustrativo, não são preços de mercado) — o preço mal os separa —, mas pesa cerca de cinquenta e cinco vezes menos e é o material que fecha os vinte anos com as menores emissões líquidas dos quatro.
>
> Isto não é sorte. Massa é carbono, e o betão armado é, de longe, o material mais maciço da lista.

---

### 4.8.5. Quando o betão ainda faz sentido

A tabela não condena o betão. Diz que precisa de justificação.

- **Vida útil maior.** O programa adota 20 anos para todos os materiais. É um piso, não uma previsão: uma cisterna de betão bem executada pode durar muito mais, e num horizonte superior a 59 anos o retorno do carbono paga-se, embora sem folga. Se adotar uma vida útil diferente, **declare-a** e justifique-a. [A COMPLETAR: se se quiser fundamentar a vida útil por norma, indicar a fonte portuguesa ou europeia aberta; este manual não cita nenhuma.]
- **Volumes grandes.** Para volumes muito grandes, os reservatórios de polietileno de fábrica deixam de ser práticos e o betão moldado no local pode ser a única opção viável.
- **Restrição de espaço.** Uma cisterna enterrada de betão adapta-se ao terreno; a de polietileno vem em formatos fixos.
- **Estrutura já existente.** Um reservatório de betão reaproveitado de outra finalidade tem carbono incorporado **zero** para efeito deste projeto.

---

### 4.8.6. A decisão do tutorial

**Trocamos para polietileno.**

É o que um projetista faria perante esta tabela, e é o que torna este tutorial honesto: um estudo muda de rumo quando a análise mostra que o rumo estava errado. A troca não faz o sistema pagar-se, nem em dinheiro nem em carbono, mas faz a diferença onde ela importa:

<!-- tabela: **Tabela 122** — Efeito da troca de betão por polietileno nas três dimensões de análise (ilustrativo, não é preço de mercado) -->
| (ilustrativo, não é preço de mercado) | Betão | Polietileno |
| :--- | ---: | ---: |
| preço da cisterna | 2 600 € | 2 850 € |
| investimento total | 6 650 € | 6 900 € |
| período de recuperação | sem recuperação | sem recuperação |
| VAL a 20 anos | −5 829 € | −6 079 € |
| retorno do carbono | 59,0 anos | 20,9 anos |
| emissões líquidas em 20 anos | +678 kg | +15 kg |

A troca custa 250 € a mais e empurra o VAL para −6 079 €, mas reduz o retorno do carbono de 59,0 para 20,9 anos e as emissões líquidas de 678 para 15 kg. O potencial de poupança não muda.

<!-- tabela: **Tabela 123** — Estado do projeto do tutorial depois da análise ambiental (ilustrativo, não é preço de mercado) -->
| Projeto até aqui (ilustrativo, não é preço de mercado) | |
| :--- | ---: |
| volume | 5 000 L |
| **material** | **polietileno** |
| investimento | 6 900 € |
| VAL | −6 079 € |
| período de recuperação | sem recuperação |
| retorno do carbono | 20,9 anos |

---

### 4.8.7. O que declarar

A avaliação do ciclo de vida do Triton é de **triagem**, não um inventário completo. Todos os fatores predefinidos têm proveniência declarada, mas alguns são aproximações, como o da eletrobomba e o do hipoclorito, e um fator escrito sem fonte recebe uma etiqueta de triagem, que o programa mostra. Num estudo publicado:

- declare a **fronteira** adotada, água entregue e não produzida;
- declare a **vida útil** e justifique-a;
- declare quais os fatores que são aproximações e quais foram introduzidos sem fonte;
- declare a **base da rede elétrica** e o ano.

O apêndice C traz a proveniência de cada fator, e a secção 2.8 explica as sete etapas do inventário.

Temos agora três respostas. O potencial diz um volume, o dinheiro diz outro, o carbono diz um terceiro. É hora de escolher.

---

## 4.9. Que volume escolher, afinal

> No fim desta secção, tem um volume recomendado e sabe que ele depende de pesos que **o utilizador** declarou — e não de uma verdade que o programa descobriu.

---

### 4.9.1. Três critérios, três respostas

As secções anteriores deste tutorial fizeram ao mesmo projeto três perguntas distintas — quanta água entrega, quanto dinheiro rende e quanto carbono evita — e receberam três respostas que não coincidem. Esta discordância não é defeito da análise nem inconsistência dos dados: mostra que os três critérios medem coisas diferentes e se comportam de maneira diferente em relação ao volume do reservatório.

<!-- tabela: **Tabela 124** — Matriz de decisão multicritério: cada volume da varredura avaliado nas três dimensões de análise (os custos são ilustrativos, não são preços de mercado) -->
| Volume | Potencial | VAL (ilustrativo, não é preço de mercado) | Período de recuperação | Saldo de carbono em 20 anos | Investimento (ilustrativo, não é preço de mercado) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 000 L | 11,91% | −4 548 € | sem recuperação | 9 kg | 4 700 € |
| 2 000 L | 14,52% | −4 805 € | sem recuperação | 25 kg | 5 250 € |
| 3 000 L | 16,00% | −5 189 € | sem recuperação | 19 kg | 5 800 € |
| 4 000 L | 17,10% | −5 615 € | sem recuperação | 5 kg | 6 350 € |
| 5 000 L | 17,88% | −6 079 € | sem recuperação | −15 kg | 6 900 € |
| 8 000 L | 19,65% | −7 611 € | sem recuperação | −87 kg | 8 550 € |
| 12 000 L | 21,43% | −9 694 € | sem recuperação | −194 kg | 10 750 € |

<!-- tabela: **Tabela 125** — Volume vencedor segundo cada critério isolado -->
| Critério isolado | Volume vencedor |
| :--- | ---: |
| maior potencial de poupança | 12 000 L |
| menor período de recuperação descontado, desempate pelo VAL | 1 000 L |
| maior saldo de carbono | 2 000 L |
| **compromisso, pesos iguais** | **5 000 L** |

A primeira tabela é o retrato do problema. Repare em como as colunas discordam:

- O **potencial** cresce monotonicamente: quanto maior a cisterna, mais água. Máximo em 12 000 L (21,43%).
- O **VAL** é negativo em todos os volumes (os custos são ilustrativos, não são preços de mercado). O seu melhor valor, a menor perda, está em 1 000 L, e piora a cada volume acrescentado, porque cada metro cúbico adicional de reservatório custa mais do que a poupança que traz. Nenhum volume tem período de recuperação.
- O **carbono** sobe e cai muito mais cedo: máximo em 2 000 L (retira 25 kg em vinte anos). Depois disso, cada metro cúbico de polietileno acrescenta mais dívida do que crédito, e aos 5 000 L o saldo já passa a emissão.

==Não existe um volume que vença nos três critérios em simultâneo.== Cada um tem o seu ótimo num ponto diferente da curva, e a escolha entre eles não é uma questão técnica com resposta única: é uma questão de prioridade, que tem de ser declarada por quem decide e não pode ser descoberta pelo programa. É exatamente essa a lacuna que os métodos multicritério vêm preencher.

---

### 4.9.2. Como o TOPSIS resolve

O programa usa o TOPSIS sobre **sete critérios**:

<!-- tabela: **Tabela 126** — Os sete critérios do multicritério e o sentido de preferência de cada um -->
| Critério | Sentido |
| :--- | :--- |
| potencial de economia | maximizar |
| extravasamento | minimizar |
| valor atual líquido | maximizar |
| período de recuperação descontado | minimizar |
| taxa interna de rentabilidade | maximizar |
| CO₂e no fim da vida | minimizar |
| consumo de água potável | minimizar |

O método funciona em quatro passos encadeados. Primeiro, normaliza a matriz de decisão, para que critérios medidos em unidades incomparáveis — pontos percentuais, euros, quilogramas de dióxido de carbono equivalente e anos — passem a ocupar a mesma escala. Depois, aplica os pesos declarados. Calcula então, para cada alternativa de volume, a distância euclidiana à solução ideal, formada pelos melhores valores de cada critério, e à solução anti-ideal, formada pelos piores. Por fim, ordena as alternativas pela proximidade relativa ao ideal, conforme a formulação da secção 2.10.

Aplicado ao projeto do tutorial com pesos iguais entre as três dimensões, repartidos igualmente pelos critérios de cada uma, o método indica o volume de 5 000 L.

> **Três declarações que um estudo publicado tem de fazer.**
>
> A normalização do programa é uma **variante** de Hwang e Yoon: translada por `x − min(x)` antes da normalização vetorial, para admitir um VAL negativo. É uma escolha deliberada, e apresentá-la como TOPSIS canónico seria incorreto.
>
> O SMAA-VIKOR, disponível ao lado, sorteia pesos e devolve a probabilidade de cada volume ocupar cada posição. É a resposta certa quando não há consenso sobre os pesos.
>
> As condições C1 e C2 de Opricovic, de vantagem aceitável e de estabilidade, **não estão implementadas**. A secção 2.10 detalha.

---

O separador de decisão apresenta o escore de cada volume candidato (Figura 63).

![O escore multicritério de cada volume candidato](../figuras/fig51_programa_topsis.png)

*Figura 63 — O gráfico do separador de decisão: o escore de proximidade ao ideal de cada volume candidato, com o vencedor destacado. Escores próximos entre si significam alternativas tecnicamente equivalentes, e nesse caso a escolha passa a depender do peso declarado. Figura gerada pelo próprio programa.*

---
### 4.9.3. O peso muda a resposta

A tabela seguinte mostra o que acontece ao deslocar o peso.

<!-- tabela: **Tabela 127** — Volume escolhido pelo TOPSIS conforme a dimensão com peso dominante, e o segundo classificado -->
| Peso dominante | Volume | Segundo classificado |
| :--- | ---: | ---: |
| pesos iguais | 5 000 L | 4 000 L |
| técnico, 60% | 8 000 L | 12 000 L |
| económico, 60% | 5 000 L | 4 000 L |
| ambiental, 60% | 5 000 L | 4 000 L |

Privilegiar o critério técnico desloca a recomendação para 8 000 L, o que era de esperar: o potencial de economia cresce monotonicamente com o volume, e um peso dominante nessa dimensão empurra a escolha para cima. Os critérios económico e ambiental, por seu lado, ficam ambos nos 5 000 L dos pesos iguais.

Esta convergência, contudo, não é regra geral, e lê-la como tal seria generalizar indevidamente um caso particular. Isoladamente, o critério financeiro prefere 1 000 L e o ambiental 2 000 L; o ordenamento cai em 5 000 L porque o TOPSIS pesa também os restantes critérios de cada dimensão, entre os quais os hídricos (potencial, extravasamento, consumo de água potável), que favorecem volumes maiores. Com outro tarifário ou outros custos, o ótimo económico deslocar-se-ia, e a divergência entre os critérios apareceria com clareza.

O ordenamento multicritério escolhe um volume; não diz se se deve construir. Neste tutorial, todos os volumes têm VAL negativo e nenhum período de recuperação, com os custos ilustrativos, pelo que a dimensão financeira argumenta contra construir seja o que for. Se o projeto avançar, é pelas razões que as outras dimensões apresentam ou por um fim que o fluxo de caixa não mede, e o relatório tem de o dizer.

> **Declare os pesos.** «Volume ótimo pelo TOPSIS» sem os pesos é uma afirmação impossível de reproduzir. Dois artigos com pesos diferentes chegam a volumes diferentes, e ambos estão certos.

---

Uma solução de compromisso cede em alguma coisa, e convém saber em quê. O programa desdobra o escore único em sete, um por critério, e mostra a distância que separa a alternativa escolhida do melhor valor alcançado em cada um (Figura 64).

![A proximidade do volume escolhido ao ótimo de cada critério](../figuras/fig52_programa_proximidade.png)

*Figura 64 — O segundo gráfico do separador de decisão: o quanto o volume escolhido se aproxima do melhor valor possível em cada um dos sete critérios. É a figura que mostra o que a solução de compromisso está a ceder, e em que dimensão. Figura gerada pelo próprio programa.*

---
### 4.9.4. A recomendação do tutorial

A recomendação do tutorial, se o projeto for construído, é o reservatório de **5 000 L em polietileno**, e a razão para a adotar não é só vencer com pesos iguais. É o volume de compromisso, não o ótimo financeiro, que está em 1 000 L, nem o ótimo ambiental, que está em 2 000 L. Vence também com um peso económico dominante e com um peso ambiental dominante, e perde para os 8 000 L apenas com um peso técnico dominante. Sob a incerteza simulada dos pesos (SMAA), fica em primeiro lugar em 34,1% dos sorteios, contra 30,6% para 8 000 L e 15,6% para 4 000 L. ==Uma recomendação que sobrevive a três ponderações diferentes é robusta justamente porque não depende de nenhuma delas==, embora a margem do SMAA seja estreita.

Vale registar ainda que este é o mesmo volume que o critério hidráulico da secção 4.4 tinha indicado, com um limiar de ganho marginal de 1 %/m³. Duas vias metodologicamente independentes — uma que olha só para a curva de aproveitamento e outra que pondera sete critérios de três dimensões — chegaram ao mesmo resultado, e essa concordância reforça a confiança na recomendação.

A concordância, porém, não está garantida em nenhum outro caso, e é por isso que o tutorial fez o caminho longo em vez de parar na secção 4.4. O propósito não era chegar mais depressa ao volume, mas saber que as duas vias concordam **neste** projeto, em vez de supor que concordam sempre.

---

### 4.9.5. O projeto, fechado

<!-- tabela: **Tabela 128** — Resumo do projeto do tutorial, com todos os parâmetros e resultados -->
| Triton · moradia unifamiliar em Lisboa (custos ilustrativos, não são preços de mercado) | |
| :--- | ---: |
| série de precipitação | Lisboa, 30 anos, 719 mm/ano |
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
| **potencial de economia de água potável** | **17,88%** |
| dias de atendimento pleno | 62,8% |
| água da chuva consumida | 39,2 m³/ano |
| energia da elevação | 5,1 kWh/ano |
| investimento (ilustrativo) | 6 900 € |
| **valor atual líquido a 20 anos (ilustrativo)** | **−6 079 €** |
| período de recuperação descontado | sem recuperação |
| **emissões líquidas em 20 anos** | **+15 kg CO₂e** |
| retorno do carbono | 20,9 anos |

Resta uma etapa, que é comunicar o resultado: um estudo que não é relatado de forma verificável não se distingue, para quem o lê, de um palpite bem apresentado. É o assunto da secção seguinte.

---

## 4.10. O relatório, e o que declarar num artigo

> No fim desta secção, tem o relatório emitido e, se pretende publicar, a lista do que tem de constar no método do artigo. Essa lista é a parte mais curta e mais importante do manual.

---

### 4.10.1. Os três relatórios

O programa emite três relatórios distintos, e a distinção não é de extensão, mas de público e de finalidade. Escolher o relatório errado para o destinatário certo é a forma mais comum de produzir um documento que ninguém lê: um cliente não percorre um inventário de ciclo de vida item a item, e um avaliador de certificação não se satisfaz com uma conclusão de quatro páginas.

O **relatório executivo** tem de quatro a seis páginas e reúne o resultado técnico, o investimento, o retorno e uma conclusão objetiva. É o documento de entrega ao cliente, e a sua virtude é caber numa só leitura, sem exigir que o leitor conheça o método.

O **relatório ambiental e ESG** apresenta o inventário de ciclo de vida discriminado por componente, o saldo de carbono ao longo da vida útil e o enquadramento do projeto nos referenciais tratados na secção 2.9 — LEED, EDGE e GRI 303. É o documento que se anexa a um processo de certificação, e a discriminação por componente existe justamente porque um avaliador confere item a item.

O **relatório científico** traz o método completo, as premissas declaradas, a série utilizada e os resultados com a precisão que um artigo exige. É a base sobre a qual se redige uma publicação, e é o único dos três que inclui as figuras analíticas.

Além dos três, a etapa **10. Exportação** gera o desenho esquemático em DXF, o modelo BIM em JSON e folhas de cálculo com a série diária completa e com a varredura de volumes, como detalha a secção 3.9.

---

### 4.10.2. O que o relatório não decide por si

==O relatório traz os números; o contexto que os torna reproduzíveis é seu.== Nenhum documento gerado automaticamente pode declarar porque se escolheu aquela série de precipitação, se o consumo per capita adotado foi medido ou tirado da literatura, ou o que justifica a vida útil considerada na avaliação ambiental. É esta informação que permite a um terceiro repetir o estudo e chegar ao mesmo resultado, e é dela que trata o resto desta secção.

---

### 4.10.3. A lista de declaração

Um estudo feito no Triton que deixe de declarar qualquer dos itens abaixo não é reproduzível por terceiros e, o que costuma ser pior, não é comparável com outro estudo feito no mesmo programa — porque duas simulações com premissas diferentes produzem números que parecem comparáveis e não são. A lista está organizada pela ordem em que as decisões aparecem no trabalho, e pode seguir-se como roteiro de redação do método.

#### 4.10.3.1. Programa e versão

- **Versão do Triton**, com o número completo, e a **edição** (Portugal). As correções de cálculo entre versões deslocam resultados, e sem a versão declarada não há como saber que cálculo produziu o número publicado.

#### 4.10.3.2. Série de precipitação

- **Origem**: estação, base de concelhos (E-OBS) ou reanálise.
- Se for a base de concelhos: **concelho, versão da E-OBS e janela temporal**; se for reanálise ou modelo: **produto, cenário, janela temporal** e a resolução da grelha.
- **Recorte**: datas de início e fim, e número de anos.
- **Tratamento de falhas** e critério para descartar um ano incompleto.

#### 4.10.3.3. Edifício e procura

- Área de captação e **como foi obtida** — projeção horizontal.
- Coeficiente de escoamento e a sua origem.
- Consumo per capita, e se é **medido ou de referência**.
- **Fração atendível pela água da chuva** e os usos finais que a compõem. É o teto do resultado, e sem ela o potencial não se interpreta.
- Se algum uso está fora da lista que a norma aplicável admite, como a máquina de lavar roupa, e que critério de qualidade foi adotado para ele.

#### 4.10.3.4. Arranjo de abastecimento

- **Arranjo**: elevação para reservatório superior, pressurização direta ou gravidade. Define a energia e as eletrobombas no custo e no carbono.
- Na elevação: volume do reservatório, limiar de acionamento e altura manométrica.
- Na pressurização direta: pressão de trabalho e arranques por pessoa e por dia.

#### 4.10.3.5. Descarte das primeiras águas

- Lâmina adotada e **modo**, entre os três.
- **O tratamento da lâmina**, se o estudo comparar o Triton com outra ferramenta: algumas ferramentas tratam a lâmina como limiar do evento, o Triton subtrai-a à chuva do dia, e os dois dão resultados diferentes.

#### 4.10.3.6. Volume e critério de escolha

- Se veio de uma varredura: **o limiar de ganho marginal adotado**. Sem ele, «volume ideal» não significa nada.
- Se veio do multicritério: **os pesos dos sete critérios** e o método, TOPSIS ou SMAA-VIKOR.
- Que a normalização do TOPSIS é uma **variante**, com translação por `x − min(x)`.

#### 4.10.3.7. Análise económica

- **Concelho e entidade gestora**, com a data de entrada em vigor do tarifário.
- **Regime de mínimo**, entre os seis. É o que mais altera resultados entre entidades gestoras.
- Percentagem do saneamento, e que incide sobre a **parcela da água** da fatura.
- Taxa de atualização, inflação, período de análise.
- **Atualizações tarifárias** da água, do saneamento e da energia, com o intervalo.
- Se os custos são orçamentos ou valores ilustrativos.

#### 4.10.3.8. Avaliação do ciclo de vida

- **Fronteira**: água entregue, e não produzida.
- **Vida útil** adotada e a sua justificação.
- **Material** do reservatório. Pesa muito no resultado, como a secção 4.8 mostra.
- Base do fator de emissão da rede elétrica, **com o ano**.
- Que fatores são **aproximações** e quais levam **etiqueta de triagem**.

#### 4.10.3.9. Certificações

- Que as classes 2 a 4 de qualidade são **adaptações do programa**, e não de uma norma.
- No caso do LEED, a **versão** do referencial: v4/v4.1 ou v5.
- No caso do EDGE, que o programa avalia **apenas a barra da água**, e que o caso de base usado é o declarado ou a procura modelada.

---

### 4.10.4. O parágrafo pronto

Para o nosso projeto, o método ficaria assim:

> A simulação foi conduzida no Triton 0.1.0, Edição Ibérica, com um modelo comportamental de passo diário (extravasamento calculado antes da retirada da procura, com a chuva do dia disponível para o consumo do dia, uma ordem intermédia entre YAS e YBS), sobre uma série de precipitação de 30 anos para Lisboa (E-OBS, concelho de Lisboa, 1991 a 2020; 10 958 dias, média de 719 mm/ano). Adotou-se uma área de captação de 150 m² em projeção horizontal, um coeficiente de 0,85, valor redondo para a eficiência de captação combinada, e um descarte das primeiras águas de 2,0 mm em todas as chuvadas, subtraído à lâmina diária. A procura total adotada foi de 600 L/dia (4 moradores, 150 L/hab·dia), com uma fração atendível pela água da chuva de 28%, correspondente ao autoclismo e aos usos exteriores. O volume de 5 000 L resultou do critério do ganho marginal com limiar de 1 %/m³ e foi confirmado por uma análise multicritério TOPSIS com sete critérios e pesos iguais entre as dimensões técnica, económica e ambiental, com normalização numa variante de Hwang e Yoon transladada por x − min(x). Os pontos de uso são abastecidos por elevação para um reservatório superior de 1 000 L, com limiar de acionamento de 100 L, duas eletrobombas de 0,5 cv e o rendimento de motor predefinido do programa. A análise económica usou o tarifário de Lisboa em vigor desde 01/01/2026 (água da EPAL com o adicional da Câmara Municipal, saneamento e resíduos da Câmara), uma taxa de atualização de 0,4% ao mês, uma inflação de 0,2% ao mês, atualizações de 3% ao ano com intervalos de 12 meses e um período de 20 anos; todos os custos foram valores redondos ilustrativos, não são preços de mercado. A avaliação do ciclo de vida adotou a fronteira da água entregue, fatores de emissão ilustrativos de 0,40 kg CO₂e/kWh e 0,50 kg CO₂e/m³, um reservatório de polietileno e uma vida útil de 20 anos.

São cerca de trezentas palavras, e são a diferença entre um estudo que outro investigador consegue repetir e um número solto que ninguém pode verificar. A extensão é modesta perante o que se ganha: um método assim redigido responde antecipadamente à maior parte das perguntas que um revisor faria.

---

### 4.10.5. O fim do tutorial

Dez secções, um único projeto acompanhado do princípio ao fim, e um estudo completo: partiu de uma moradia sem sistema e chegou a uma recomendação de volume, material, classe de qualidade e a um veredicto sobre a viabilidade económica e ambiental — negativo em ambas, com os custos ilustrativos e a tarifa de Lisboa, mesmo depois de trocar o material —, com cada decisão justificada pelo número que a sustentou. O quadro da secção 4.9 reúne o resultado consolidado.

O caminho a seguir depende do que pretende fazer a seguir:

- **Resolver um caso diferente do tutorial** — o capítulo 3, os guias de tarefa.
- **Perceber de onde vem cada número** — o capítulo 2, o método.
- **Não cometer os erros que o programa não impede** — a secção 5.1.
- **Defender o estudo perante um revisor** — o capítulo 5.

---

# 5. Enganos, limitações e confiabilidade

---

## 5.1. Dez enganos que o programa não impede

> Estes não são defeitos do programa. São erros de **engenharia** que ele aceita sem reclamar,
> porque não tem como os conhecer. Cada um traz o engano, por que razão é tentador, o que faz ao
> resultado e como evitá-lo.

---

### 5.1.1. Usar a área inclinada da cobertura

**O engano.** Introduzir a área da superfície da cobertura em vez da projeção horizontal.

**Porque é tentador.** É a área que aparece nas medições de telha e a que o empreiteiro conhece.

**O que faz ao resultado.** Sobrestima a captação na razão `1 ÷ cos(inclinação)`. Numa cobertura
com 30% de pendente, 4,4% de água que não existe; com 60%, 16,6%.

**Como evitar.** A prática do aproveitamento de águas pluviais toma como área de captação a
projeção horizontal da cobertura. Não use a área de contribuição com que se dimensionam as
caleiras, que soma metade da altura da cobertura e as paredes. A chuva cai na vertical, e o que
ela vê é a sombra da cobertura no chão. Se tem a área inclinada, multiplique-a por
`cos(inclinação)`, como na Figura 65.

---

![A chuva cai na vertical, e a área que capta é a projeção da cobertura](../figuras/fig00i_projecao.png)

*Figura 65 — Área de captação como projeção horizontal da cobertura. Para uma pendente de 30%, θ = 16,7° e a área inclinada é 4,4% maior do que a projeção horizontal; usar a área inclinada sobrestima o volume captado nessa proporção em todos os dias da série.*

---

### 5.1.2. Dimensionar pela chuva média mensal

**O engano.** Usar a precipitação média mensal num cálculo de folha de cálculo, em vez da série
diária.

**Porque é tentador.** A média mensal é o dado publicado nas normais climatológicas, e a folha de
cálculo cabe numa página.

**O que faz ao resultado.** Sobrestima de forma sistemática. A média esconde que a chuva chega
concentrada: um mês com 200 mm repartidos por cinco eventos enche a cisterna e faz com que
extravase cinco vezes, ao passo que o cálculo por médias supõe um fluxo contínuo que a cisterna
absorveria por inteiro. Em Lisboa o efeito é ainda mais marcante, porque o verão é seco: o mês mais
chuvoso tem 47,3 vezes a chuva do menos chuvoso, e uma média anual não vê nada disto.

**Como evitar.** É a razão de existir deste programa. A secção 2.1 mostra o extravasamento a
acontecer dia a dia; o cálculo por médias não o vê.

---

### 5.1.3. Confundir a lâmina de descarte com o volume do dispositivo

**O engano.** Introduzir no campo do descarte o volume do reservatório de autolimpeza, em litros.

**Porque é tentador.** O dispositivo dimensiona-se em litros, e o campo pede um número.

**O que faz ao resultado.** O campo espera **milímetros**. Introduzir 300, a pensar nos 300 litros
do dispositivo, produz um descarte de 300 mm — maior do que qualquer chuva diária da série de
Lisboa do tutorial, cujo máximo é 91,2 mm. O sistema capta **praticamente nada**.

**Como evitar.** `d_f` é uma lâmina. O volume do dispositivo é `A × d_f`: no projeto do tutorial,
150 m² × 2 mm = 300 litros. São a mesma decisão expressa em duas unidades, e o programa quer a
primeira.

---

### 5.1.4. Ignorar a estrutura do tarifário

**O engano.** Montar o tarifário com um preço único por metro cúbico e esquecer a parte fixa, os
escalões e a forma como a entidade gestora trata cada componente da fatura.

**Porque é tentador.** O preço do metro cúbico é o que vem em destaque. A tarifa fixa e a forma
como o saneamento e os resíduos acompanham o consumo estão em quadros à parte, quando estão.

**O que faz ao resultado.** A poupança só incide sobre a parte variável da fatura, e cada metro
cúbico poupado vale o preço do escalão em que cai. Em Lisboa, a fatura do tutorial passa de
46,25 € por mês sem o sistema (18,26 m³) para 35,06 € com ele (15,00 m³): uma poupança de
3,27 m³ e de 11,19 € por mês. Um estudo que suponha um desconto linear sobre a fatura total produz
um período de recuperação que não existe.

**Como evitar.** A secção 3.3. E o teste prático: simule dois consumos, um num escalão e outro
noutro, e compare com uma fatura real do edifício.

---

### 5.1.5. Simular uma escola ou um hospital com tarifa doméstica

**O engano.** Usar a tarifa doméstica para um edifício que não é de habitação.

**Porque é tentador.** O tarifário doméstico é o que está à mão, e o programa não impede a sua
utilização noutra tipologia. Os tarifários que a edição traz transcritos (Lisboa, Porto e Funchal)
são de utilizador doméstico.

**O que faz ao resultado.** Subestima, em regra, a poupança, porque as categorias não domésticas
costumam ser mais caras do que a doméstica; o preço de cada entidade gestora é que decide.

**Como evitar.** O programa **avisa** quando a tipologia não é residencial e diz o sentido do erro.
Escolha a categoria do edifício no tarifário da entidade gestora e introduza a sua estrutura em
modo personalizado. A secção 3.5 trata do assunto.

---

### 5.1.6. Esperar que o reservatório superior aumente a poupança

**O engano.** Adotar o reservatório elevado à espera de mais água.

**Porque é tentador.** É um arranjo corrente, e «mais reservatório» soa a «mais água».

**O que faz ao resultado.** Com o mesmo armazenamento total, o arranjo com reservatório elevado
entrega **menos**: a cisterna extravasa enquanto o reservatório de cima ainda tem espaço, porque a
elevação só acontece quando há consumo. No tutorial, 0,31 pontos percentuais a menos (17,88%
contra 18,19% com um único reservatório de 6 000 L), mais 5,1 kWh por ano de energia.

**Como evitar.** Decida o reservatório por critério **hidráulico** — pressão por gravidade, reserva
contra falhas de energia — e não hídrico. A secção 4.5 faz a comparação justa.

---

### 5.1.7. Adotar uma série curta demais

**O engano.** Simular com dois ou três anos de série.

**Porque é tentador.** É o que se consegue depressa a partir de um posto próximo.

**O que faz ao resultado.** Dois efeitos somados. O **viés do reservatório vazio**, porque a
simulação começa com a cisterna seca e os primeiros meses penalizam o resultado; e a
**dependência do troço**, porque uma série curta pode cair num período atipicamente seco ou
chuvoso.

**Como evitar.** Trinta anos é confortável, dez é o mínimo defensável. Abaixo disso, declare a
limitação e apresente o resultado como uma gama.

---

### 5.1.8. Escolher a classe de qualidade pelo custo

**O engano.** Adotar a classe 1 por ser a mais barata, para um uso que exigiria mais.

**Porque é tentador.** O programa deixa, e a diferença de custo vê-se logo.

**O que faz ao resultado.** Não muda o número; muda a **validade** do projeto. Um sistema que
alimenta uma máquina de lavar roupa com água tratada ao mínimo é uma decisão de qualidade, não de
orçamento.

**Como evitar.** Escolha pela **exigência do uso**. E lembre que as classes 2 a 4 são adaptações
do programa, e não requisitos de uma norma: use-as como critério declarado, e não como norma.

---

### 5.1.9. Comparar com outra ferramenta sem declarar o método

**O engano.** Apresentar lado a lado os resultados de dois programas de aproveitamento pluvial
como se fossem comparáveis.

**Porque é tentador.** Ambos simulam o mesmo reservatório com as mesmas equações de balanço.

**O que faz ao resultado.** As ferramentas diferem em decisões de modelação que movem o número: se
o descarte das primeiras águas se subtrai à chuva do dia ou funciona como limiar do evento, como se
escolhe o volume ideal, que regra de operação se aplica. Uma diferença de alguns pontos percentuais
pode vir de qualquer uma delas, e nenhuma é um erro.

**Como evitar.** Declare a divergência e compare com um descarte igual a zero, em que as duas
regras de descarte coincidem. As secções 3.8 e 6.1 detalham o assunto.

---

### 5.1.10. Publicar o volume de maior poupança como recomendado

**O engano.** Escolher da varredura o volume de maior potencial.

**Porque é tentador.** É a coluna que o estudo de aproveitamento pluvial reporta, e mais é melhor.

**O que faz ao resultado.** No tutorial de Lisboa a curva não satura: 20 000 L dão o maior
potencial da varredura, 24,01%. Custam também **3,3 vezes mais** do que 5 000 L, em betão
(ilustrativo, não é preço de mercado: 8 600 € contra 2 600 €), e carregam **3,5 vezes mais carbono
incorporado** (3 546 contra 1 026 kg CO₂e), para entregar 6,52 pontos percentuais a mais. Escolher
o maior volume testado é escolher o limite da varredura, e não um ótimo.

**Como evitar.** Declare o critério de escolha. Se for hidráulico, o limiar de ganho marginal; se
for multicritério, os pesos. E reporte os vencedores de cada critério isolado, porque a divergência
entre eles **é** o resultado.

---

### 5.1.11. O engano de fundo

Os dez acima têm uma raiz comum: **tratar o programa como uma calculadora em vez de um modelo**.

Uma calculadora recebe números e devolve números. Um modelo recebe premissas e devolve as
consequências dessas premissas. Todo o resultado do Triton é condicional ao que foi declarado, e a
qualidade do estudo está na qualidade e na explicitação dessas declarações.

É por isso que a secção 4.10 traz a lista do que declarar, e é por isso que a secção 5.2
traz as limitações conhecidas. Um estudo que não declara as premissas não é reproduzível, por mais
correto que seja o cálculo.

---

## 5.2. Limitações conhecidas

> Onde o programa não serve, e porquê. Um programa que declara os próprios limites é mais
> fiável do que um que aparenta servir para tudo, porque o segundo deixa ao utilizador a tarefa de
> os descobrir por conta própria.

Esta secção deriva do registo de pendências que o grupo de investigação mantém, e reflete o estado
da versão beta atual, a 0.1.0. Uma limitação sai desta lista quando é efetivamente resolvida, e
não quando deixa de ser mencionada — distinção que parece óbvia e que a documentação dos programas
científicos muitas vezes não observa.

As limitações estão agrupadas por origem, porque a providência que cada grupo admite é diferente.
As do modelo decorrem de escolhas de representação e só mudam com uma revisão do próprio modelo.
As dos dados dependem de levantamento, e podem ser supridas pelo utilizador. As metodológicas são
desvios declarados em relação a uma formulação de referência. E as de implementação são trabalho
pendente, sem obstáculo conceptual.

---

### 5.2.1. Limitações do modelo

**Não há subpasso horário.** Uma chuva de 40 mm concentrada em duas horas e a mesma lâmina
repartida por vinte e quatro horas produzem o mesmo resultado. Para reservatórios muito pequenos
face à área de captação, isto subestima o extravasamento.

**Não há perdas no reservatório.** A evaporação e as fugas não são modeladas.

**A condição inicial é o reservatório vazio.** Em séries de menos de um ano, isto penaliza o
resultado de forma sensível.

**O coeficiente de escoamento é único e constante.** Não varia com a intensidade da chuva nem com o
tempo decorrido desde o último evento, quando na realidade o primeiro evento após uma estiagem tem
um coeficiente menor.

**O descarte é uma lâmina, e não um dispositivo.** O programa calcula o volume e o custo do
dispositivo, `A × d_f`, mas não o seu arranjo hidráulico, que exige um projeto à parte.

---

### 5.2.2. Limitações dos dados de chuva e de tarifário

**A chuva por concelho é uma média de grelha.** Em Lisboa e no Porto, a série é a média diária das
células da grelha E-OBS (0,1°) do concelho, e não o registo de um posto. A base cobre 278 dos 308
concelhos; os 30 restantes ficam de fora por estarem fora do domínio da E-OBS (Açores, a oeste de
25° W) ou por terem mais de 1% de dias sem dado em 1991–2020. O Funchal usa a reanálise ERA5, numa
célula de cerca de 9 km, com chuva em 42% dos dias, e é a série menos fiável das três. Para um
projeto real, use a série medida.

**O tarifário cobre três cidades e só o utilizador doméstico.** Estão transcritos os tarifários de
Lisboa (EPAL e Câmara Municipal de Lisboa), do Porto (Águas e Energia do Porto) e do Funchal
(Câmara Municipal do Funchal), todos do escalão geral de utilizador doméstico, com contador até
25 mm (no Funchal, até 15 mm). Noutros concelhos, ou noutras categorias, a estrutura tem de ser
introduzida à mão pelo utilizador, e a sua exatidão é dele. Um estudo de escola, comércio ou
indústria calcula a poupança com a estrutura que estiver introduzida; se for a doméstica, o
resultado é em regra **subestimado**: o erro é conservador e tem sentido conhecido, mas precisa de
ser declarado. O programa avisa quando a tipologia não é residencial, e a secção 3.3 descreve
como se introduz a estrutura da categoria certa.

**Há hipóteses de transcrição por confirmar.** No Funchal, a taxa de IVA de 4% não foi confirmada
(com 5%, a fatura de 10 m³ passaria de 17,0872 € para 17,2515 €), e o primeiro escalão (até 5 m³)
do saneamento e dos resíduos não tem valor impresso e foi tratado como zero. No Porto, a
disponibilidade de água de 0,1242 € por dia foi lida da página dos utilizadores domésticos, e a
taxa de recursos hídricos das águas residuais não foi incluída. Em Lisboa, o adicional da Câmara
foi tratado sem IVA. As hipóteses estão registadas junto dos exemplos da edição.

**O saneamento é aproximado.** O saneamento faturado por escalões próprios representa-se por uma
percentagem única da fatura da água, por um valor fixo ou por um preço por metro cúbico. É uma
aproximação declarada.

**Não há tarifa social nem sobretaxas sazonais ou de escassez.** Uma classe de baixos rendimentos,
uma sobretaxa de seca ou um preço sazonal não são modelados, a menos que o utilizador os incorpore
na estrutura introduzida. Num estudo de habitação social, a diferença pode inverter a conclusão.

**A eletricidade só tem tarifa registada no Funchal**, e de fonte secundária (a confirmar na
entidade). Em Lisboa e no Porto, o custo da bombagem depende do preço do quilowatt-hora que o
utilizador introduzir; os casos do manual usam um valor ilustrativo, que não é preço de mercado.

---

### 5.2.3. Limitações da avaliação de ciclo de vida

**É uma avaliação de triagem**, e não um inventário conforme a ISO 14040.

**Uma única categoria de impacto.** Só carbono. Não há eutrofização, acidificação, uso do solo nem
toxicidade.

**A emissão de fabrico da eletrobomba é uma aproximação por massa.** O programa multiplica a massa
de catálogo de cada potência pela intensidade por quilograma de uma declaração ambiental de produto
de uma bomba de outra classe. A ordem de grandeza é defensável; o valor de cada potência não é uma
medição.

**A pressurização direta é modelada por valores médios.** A energia usa uma pressão de trabalho
única, a média da gama do pressostato, e não o ciclo de ligar e desligar de cada uso; e não se
soma energia de arranque nem consumo em vazio, que um sobrepressor com variador de frequência
teria. Os projetos antigos sem reservatório superior abrem com o arranjo «não informado» e não
recebem energia até que um seja escolhido.

**Não há fim de vida.** Nem crédito por reciclagem, nem encargo por deposição.

**Não há manutenção.** As substituições de componentes ao longo da vida útil não entram.

---

### 5.2.4. Limitações da qualidade da água

**As classes 2 a 4 são adaptações do programa**, e não classes de uma norma. A matriz de
parâmetros por uso é uma convenção interna; declare-a como tal.

**As constantes do modelo de lavagem da cobertura não estão calibradas.** A qualidade da água que
daí resulta é uma **premissa**, e não uma medição. O programa não substitui o ensaio laboratorial.

---

### 5.2.5. Limitações metodológicas declaradas

**O percentil do R95p é calculado sobre a série inteira**, e não sobre o período-base fixo
1961–1990 do ETCCDI. As séries de comprimentos diferentes não são diretamente comparáveis neste
índice.

**As condições C1 e C2 de Opricovic não estão implementadas** no VIKOR. A solução de compromisso
deve ser lida com a análise de sensibilidade aos pesos ao lado.

**A normalização do TOPSIS é uma variante**, com translação por `x − min(x)`, para admitir um
valor atual líquido negativo.

**A atualização das tarifas é uma percentagem única** ao longo de todo o período de análise, o que
torna frágil a projeção a vinte anos. É a premissa que mais move o resultado económico.

---

### 5.2.6. Limitações de implementação

**Seis campos são gravados no ficheiro e nunca lidos.** Entre eles o **mês de instalação**, pelo
que o fluxo de caixa começa sempre no mês 1.

**O tempo de arranque da eletrobomba, de 108 s por acionamento**, representa o tempo de
escorvamento de uma bomba cuja linha de aspiração se esvaziou, e é aplicado a **todo** o arranque.
É conservador.

**Não há opção para tratar o descarte como limiar do evento**, como fazem algumas outras
ferramentas. Para comparar com uma delas, use um descarte igual a zero, em que as duas regras
coincidem, ou a transformação da série da secção 6.1.

---

### 5.2.7. O que fazer com esta lista

Num trabalho publicado, cite as limitações que afetam o seu caso — não todas, o que transformaria a
secção de método numa lista defensiva, mas as que incidem de facto sobre as conclusões
apresentadas. ==Uma limitação declarada é uma ressalva; uma limitação omitida, quando descoberta,
é um erro.==

Três exemplos orientam a seleção. Um estudo conduzido numa escola precisa de citar a questão da
categoria tarifária, porque ela desloca todo o resultado económico. Um estudo de desempenho
ambiental precisa de citar a categoria única de impacto e a aproximação por massa do fator de
emissão da eletrobomba. E um estudo em habitação social precisa de citar a ausência de tarifa
social, que nesse contexto pode inverter a conclusão.

Um parecerista que encontre uma destas limitações silenciada tem toda a razão em cobrá-la, e a
cobrança costuma custar mais tempo do que a declaração teria custado.

---

## 5.3. Como o programa é verificado

> Esta secção descreve a suíte de verificação do Triton, para que um revisor disponha dos
> elementos necessários para julgar o grau de confiança de um resultado produzido pelo programa.

Um programa científico cuja verificação não é declarada equivale a uma afirmação sem evidência:
pode estar correto, mas quem o utiliza não tem como o saber, e quem avalia um trabalho feito com
ele não tem como o julgar. Esta secção é a evidência que sustenta os números apresentados no resto
do manual, e foi escrita para ser lida por quem precisa de decidir se confia neles.

---

### 5.3.1. A suíte

A verificação do programa consiste em mais de mil testes automatizados, organizados em cinco
famílias que se complementam (Figura 66): testes unitários, testes de invariantes,
testes de integração, testes da interface gráfica e testes de referência contra resultados
independentes. A separação não é meramente organizativa: cada família apanha uma classe distinta
de defeito, e a ausência de qualquer uma delas deixaria um flanco a descoberto.

![As cinco famílias da suíte de verificação](../figuras/fig45_suite.png)

*Figura 66 — Número de testes e de ficheiros de cada família da suíte de verificação, conforme a recolha da suíte nesta versão. Os testes unitários respondem por mais de quatro quintos do total, por serem de execução rápida e localizarem o erro perto da origem.*


A suíte inteira é executada a cada alteração do código, e nenhuma alteração é incorporada enquanto
houver um teste a falhar. Esta disciplina é o que permite afirmar que um defeito corrigido não
regressa: a correção acompanha o teste que o vigia.

---

As camadas de verificação do programa formam uma hierarquia, e cada uma responde por um tipo de
erro que as restantes não alcançariam. Um teste unitário não deteta um erro de modelo, porque
confere a função com o que dela se espera; e uma conferência manual, que detetaria esse erro, não
cobre mil combinações de entrada (Figura 67).

![As camadas da verificação do programa](../figuras/fig00m_verificacao.png)

*Figura 67 — As cinco camadas de verificação do programa, dos testes unitários, numerosos e dirigidos a erros locais, à conferência manual, pontual e dirigida a erros de modelo. Nenhuma camada substitui outra: é a sobreposição das cinco que sustenta o resultado publicado.*

---

### 5.3.2. As invariantes

As invariantes constituem a família mais importante da suíte, e a razão está na natureza do que
verificam. Um teste de valor confere se o programa produz um número específico perante uma entrada
específica; uma invariante confere se uma **propriedade** vale para qualquer entrada admissível. O
primeiro deteta que uma conta mudou; a segunda deteta que o modelo deixou de ser fisicamente
consistente.

A **conservação de massa** exige que, em séries de dez anos, o volume captado iguale a soma do
extravasado, do consumido e do que permaneceu armazenado. O resíduo medido é da ordem de 10⁻¹⁴ por
cento do captado, isto é, o próprio erro de arredondamento da aritmética de vírgula flutuante. O
**fecho do balanço da procura** faz o mesmo do lado do consumo: a procura total tem de ser
exatamente a soma de três parcelas, que são a água da chuva consumida, a água potável comprada e a
procura não satisfeita.

A **gama do potencial** verifica que o potencial de poupança permaneça entre zero e cem por cento
para toda a combinação de volume, coeficiente de escoamento e área, o que se confere sobre
sessenta combinações. O **teto da fração satisfazível** é mais específico e mais revelador: o
potencial nunca pode ultrapassar a fração da procura que a chuva pode satisfazer, e a verificação
estende-se até volumes de cem metros cúbicos, muito além de qualquer aplicação predial plausível.

A **paridade entre motores** compara o núcleo compilado com o ciclo de referência e exige que
ambos devolvam o mesmo número, para reservatório único e duplo, com e sem fornecimento de reserva
da rega, dentro de uma tolerância de 10⁻⁹. A **monotonia**, por fim, exige que mais volume nunca
reduza o potencial e que mais procura nunca o aumente — duas propriedades que qualquer
implementação correta satisfaz e que uma implementação defeituosa viola de modo evidente.

---

### 5.3.3. Casos analíticos

Um conjunto à parte reúne casos de **solução fechada**, isto é, situações em que o resultado
correto se conhece por dedução, sem necessidade de simular: chuva constante, procura constante,
reservatório de capacidade infinita e reservatório de capacidade nula. ==São o teste mais forte de
que se dispõe, porque não dependem de nenhum valor de referência produzido pelo próprio programa.==
Um teste que compara a saída atual com a de ontem deteta regressão, mas perpetua um erro que já
existisse em ambas; um caso analítico não tem como o fazer.

---

### 5.3.4. Testes de percurso

Esta família nasceu do defeito mais persistente que este programa apresentou ao longo da sua
história: um valor calculado corretamente que não chega a quem o deveria consumir. É uma classe de
erro que escapa por inteiro aos testes de fórmula, porque cada parte isolada está correta — a
origem calcula bem, o destino calcularia bem se recebesse, e o que falha é o troço entre os dois.
Só um teste de percurso o apanha: alterar a entrada no ecrã e verificar que o resultado final se
move de facto.

Cinco defeitos reais encontrados por esta família, e hoje vigiados por ela, ilustram o padrão: a
escolha da tecnologia de desinfeção não chegava à avaliação de ciclo de vida; desmarcar o filtro de
polimento não surtia efeito nas classes 2 a 4; os quatro campos de imposto eram repostos a zero
pelo próprio ecrã ao ser fechado; a opção de fornecimento de reserva da rega não chegava aos
núcleos compilados; e trinta dos oitenta e sete campos de então não sobreviviam a guardar e
reabrir o projeto.

---

### 5.3.5. Os números do manual

Com a redação deste manual criou-se uma família própria de verificação, destinada a impedir que o
documento e o programa divirjam: **cada valor impresso tem uma asserção correspondente**. Estão
cobertos os números da secção 2.1, os do tutorial inteiro (Lisboa), cada linha da tabela dos
dez dias e ainda a exigência de que certas secções declarem certas ressalvas. Quando o programa
muda, o teste falha e indica qual a página a corrigir.

É o mecanismo que impede um manual inteiro de envelhecer em silêncio, que é o destino habitual da
documentação dos programas científicos.

---

### 5.3.6. Verificação contra referências independentes

A verificação estende-se a resultados que o programa não produziu: os casos analíticos acima e
comparações com cálculos de referência independentes. A secção 6.1 apresenta essa comparação e
o que ela pode e não pode mostrar.

---

### 5.3.7. O que a verificação **não** prova

A distinção entre verificação e validação é exigida por qualquer revisor competente, e com toda a
razão, porque as duas respondem a perguntas diferentes e só uma delas está ao alcance de uma suíte
de testes.

A **verificação** responde se o programa resolve corretamente as equações que implementa, e é
exatamente isso que a suíte descrita nesta secção testa. A **validação** responde se as equações
implementadas representam adequadamente a realidade física, e isso exige medição no terreno:
sistemas instalados, monitorizados ao longo do tempo e comparados com o que a simulação previu.

O Triton é verificado. A validação do modelo comportamental de base diária apoia-se na literatura
da área, e não em medição própria conduzida pelo grupo que desenvolve o programa. ==Um estudo que
apresentasse resultados do programa como se fossem medição estaria a incorrer num erro de
método.==

---

### 5.3.8. O relatório de verificação na interface

O menu **Ajuda → Relatório de Verificação** abre, dentro do programa, o relatório de verificação da
versão: a distinção entre verificação e validação, os núcleos exercitados, as invariantes, os casos
analíticos e a comparação com referências independentes. É a referência a citar quando um estudo
precisa de declarar como o programa foi verificado.

---

### 5.3.9. Quem executa a suíte, e quando

A suíte acompanha o código-fonte do programa, e não a instalação: é executada pelo grupo de
investigação a cada alteração, antes de qualquer versão ser publicada. O que isto significa para
quem usa o programa instalado é que a versão presente no seu computador passou pelos testes aqui
descritos, incluindo os que conferem cada número impresso neste manual.

> **Aprofundamento: verificar por conta própria.** O código-fonte é público, sob uma licença
> académica (uso não comercial; `LICENSE.md`), e a suíte executa-se com um único comando no
> ambiente de desenvolvimento. Um revisor que queira conferir as invariantes — fecho de massa,
> monotonia, paridade entre os dois motores de cálculo — encontra os ficheiros de teste organizados
> por tema, e o apêndice B liga cada processo do programa ao que o verifica.

---

# 6. Correções, bugs e versionamento

---

## 6.1. Verificação contra soluções analíticas e referências

> Esta secção mostra como o motor é conferido contra resultados que não produziu: soluções de
> forma fechada, um caso que se confere à mão, regras de dimensionamento publicadas e programas
> independentes, e o que cada conferência pode e não pode provar.

---

### 6.1.1. O papel da comparação

Uma comparação com outra ferramenta não é um alvo de fidelidade. ==Dois programas que coincidem até
à última casa decimal podem partilhar o mesmo erro; dois programas que diferem podem diferir por
boas razões.== O que a comparação oferece é um conjunto independente de resultados, produzido por
outras mãos, e a oportunidade de explicar cada diferença por uma causa. Sem uma referência externa
desta natureza, a verificação limitar-se-ia às propriedades internas da secção 5.3 —
necessárias, e incapazes de detetar um erro sistemático que as respeitasse todas.

As conferências abaixo vão da mais forte à mais fraca. As mais fortes dispensam qualquer programa
de referência.

---

### 6.1.2. Soluções de forma fechada

Em algumas situações a resposta correta decorre das equações, sem simulação. Com chuva constante e
procura constante, o reservatório enche até um nível conhecido; um reservatório de capacidade nula
só pode fornecer o que cai nesse dia; um reservatório de capacidade ilimitada satisfaz a procura
sempre que a oferta média a excede, e o potencial é então a totalidade da fração satisfazível. A
suíte afirma cada uma destas soluções dentro da tolerância numérica. Como o valor esperado vem da
dedução, e não de uma execução anterior do programa, um erro não se pode esconder em ambos.

---

### 6.1.3. Um caso que se confere à mão

O caso dos dez dias da secção 2.1 é pequeno o bastante para se acompanhar com papel e lápis:
100 m², coeficiente de escoamento 0,85, descarte de 2,0 mm, reservatório de 2 000 L, procura
pluvial de 80 L/dia, e a chuva de Lisboa de 11 a 20 de dezembro de 2019. O programa dá 6 732 L
captados, dos quais 4 324 L extravasam, 488 L são consumidos e 1 920 L ficam no reservatório. As
três saídas somam exatamente a entrada (6 732 − 4 324 − 488 = 1 920), e o resíduo do balanço é
zero. Repetir dois dias à mão — o dia de 35,7 mm, que capta 2 865 L e extravasa 2 380 L por
exceder o reservatório, e o dia de 1,2 mm, que fica abaixo da lâmina de descarte e não capta nada —
é a maneira mais rápida de aprender o que o programa faz com cada regra.

---

### 6.1.4. Regras de dimensionamento publicadas como referência

As regras práticas de dimensionamento não são exatas, mas delimitam a resposta. A moradia do
tutorial (150 m², 600 L/dia, 28% satisfazível) foi dimensionada por cinco métodos, e cada volume
foi depois passado pela simulação diária para obter o potencial que efetivamente entrega, com a
chuva de Lisboa.

- regra prática de 6% da procura anual (método alemão): 3 750 L, potencial 16,32%;
- simulação diária com critério de ganho marginal: 5 000 L, potencial 17,49%;
- regra prática de 0,05 vezes a precipitação vezes a área (método britânico): 5 500 L, potencial
  17,85%;
- diagrama de Rippl mensal: 47 000 L, potencial 26,78%;
- diagrama de Rippl diário: 51 500 L, potencial 26,92%.

Os métodos discordam por um fator superior a treze no volume. A dispersão é o resultado útil. As
duas regras práticas e a simulação ficam entre 3 750 e 5 500 L; o diagrama de Rippl pede 47 000 a
51 500 L, porque dimensiona contra o verão seco de Lisboa para garantir o fornecimento, e a curva da
secção 4.4 não satura nesse intervalo. Uma regra que dê um volume muito fora desta gama para as
mesmas entradas merece uma segunda análise, e a diferença entre o ótimo hidráulico e o volume de
Rippl é uma decisão de projeto, não um erro de nenhum dos dois.

---

### 6.1.5. Comparar com outro programa

Comparar com uma ferramenta independente responde a outra pergunta: duas implementações do mesmo
modelo conceptual concordam? A concordância só se espera quando as decisões de modelação
coincidem. Duas há que diferem com frequência suficiente para importar.

A primeira é o **descarte das primeiras águas**. Subtrair a lâmina à chuva do dia, como faz o
Triton, é fisicamente fiel, porque a água desviada nunca chega à cisterna. Algumas ferramentas
tratam, em vez disso, a lâmina como um limiar do evento: abaixo dele nada se capta, acima dele
capta-se a chuva inteira. A segunda é o **critério do volume**: as ferramentas escolhem o volume
ideal por ganho marginal sobre grelhas diferentes, e por isso elegem volumes diferentes. Comparar
ótimos mistura, pois, a diferença de critério com a diferença de motor; compare potenciais no
**mesmo** volume.

#### 6.1.5.1. Emular uma regra de limiar sem alterar o motor

A regra antiga emula-se transformando a série de precipitação de entrada, e não alterando o código
do balanço hídrico. Medir uma divergência com código modificado verificaria um programa que não é
o distribuído ao utilizador.

```equacao:emulacao:51
P′ = P + d_f se P ≥ d_f ; P′ = 0 caso contrário
```

<!-- tabela: **Tabela 129** — Variáveis da Equação 51 -->
| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `P′` | precipitação transformada, a fornecer ao Triton | mm |
| `P` | precipitação observada no dia | mm |
| `d_f` | lâmina de descarte das primeiras águas | mm |

Aplicada esta transformação, o cálculo `P_ef = max(0, P′ − d_f)` do Triton reproduz exatamente a
semântica do limiar. O programa não tem nenhuma opção que o faça automaticamente; use a
transformação da série, ou compare com um descarte igual a zero, em que as duas regras coincidem.

A Figura 68 ilustra como se decompõe, por causas, a divergência total entre dois
programas, até um resíduo.

![A divergência decomposta até ao resíduo](../figuras/fig25_cascata.png)

*Figura 68 — Decomposição da divergência média entre o programa e uma referência independente. A primeira barra é o total observado; as barras intermédias são diferenças de método declaradas, como o critério do volume ótimo e o tratamento do descarte; a última é o resíduo do balanço hídrico, que é o número que verifica efetivamente o motor.*

---

### 6.1.6. Linhas de referência com resultado nulo

As ferramentas de referência exportam por vezes zero onde o Triton calcula um valor positivo,
tipicamente porque a ferramenta não encontrou um volume ótimo pelo seu próprio critério. Tais
linhas apontam para uma característica dos **dados de referência**, e não para um erro do programa.
Mantenha-as à parte das estatísticas, para não deixar que dominem a média.

---

### 6.1.7. O que declarar num estudo comparativo

- os **dois números**: a divergência total e o resíduo depois da decomposição;
- as diferenças deliberadas de método, nomeadas;
- se a comparação usou descarte zero, emulação de limiar, ou nenhuma neutralização;
- a versão de cada programa.

Apresentar apenas a divergência total, sem a decompor, sugere um erro de motor que pode não
existir.

---

## 6.2. Mensagens de erro e o que fazer

> O que cada mensagem significa, o que a provocou e como a resolver.

O programa segue uma política deliberada perante entradas impossíveis: recusa-as em vez de as
corrigir em silêncio. A razão é que uma área de captação negativa não é uma preferência do
utilizador a acomodar, mas um erro de digitação que precisa de ser visto por quem o cometeu.
==Corrigir em silêncio produziria um resultado plausível a partir de uma entrada errada, que é a
pior combinação possível num programa de simulação.==

> **As mensagens do núcleo de cálculo são emitidas tal como o código as escreve.** As verificações
> que correm dentro do cálculo levantam as suas mensagens em português, por vezes sem acentos e com
> um vocabulário que pode diferir do deste manual (por exemplo, «motobomba» onde o manual diz
> «eletrobomba»). As tabelas abaixo citam cada mensagem com acentos, para facilitar a leitura, e
> explicam-na em seguida; reconhece-a pelo sentido e pelo nome do campo.

---

### 6.2.1. Validação física da entrada

As mensagens abaixo são emitidas antes de qualquer cálculo começar, e todas nomeiam o campo
responsável e o valor recebido, de modo que a correção não exija procura.

<!-- tabela: **Tabela 130** — Mensagens de validação física da entrada e a providência de cada uma -->
| Mensagem | O que a provocou | O que fazer |
| :--- | :--- | :--- |
| «Volume do reservatório inferior negativo» | volume menor do que zero | corrija; **zero é válido** e representa o cenário sem sistema |
| «Volume do reservatório superior negativo» | idem, no reservatório elevado | corrija; zero significa sem reservatório superior |
| «Área de captação negativa» | área menor do que zero | corrija; use a projeção horizontal em m² |
| «Coeficiente de escoamento fora de [0, 1]» | coeficiente negativo ou acima de 1 | acima de 1 a cobertura entregaria mais água do que a chuva traz; as coberturas usuais ficam entre 0,80 e 0,95 |
| «Lâmina de descarte negativa» | descarte menor do que zero | o descarte retira água à captação, não a acrescenta |
| «Demanda diária negativa» | procura menor do que zero | corrija |
| «Fração atendível por água pluvial fora de [0, 1]» | fração maior do que 1 | introduza 0,4 para 40%, e não 40 |
| «… não é um número finito» | campo que chegou ao cálculo vazio, como texto ou infinito | preencha o campo indicado com um número |
| «Modo de descarte desconhecido» | modo diferente de 1, 2 ou 3 | escolha um dos três modos; para não descartar, introduza uma lâmina zero |
| «Intervalo de descarte inválido» | modo 3 com um intervalo menor do que 1 dia | introduza o intervalo em dias inteiros |
| «Nível de acionamento da motobomba negativo» | nível menor do que zero | corrija; zero significa acionar com o reservatório vazio |

> A fração atendível é a mensagem mais frequente, e a regra que a evita é uma só: onde se digita,
> uma percentagem de 0 a 100; onde se guarda, uma fração de 0 a 1. A secção 4.2 justifica a
> divisão. Quando a mensagem surge, o valor chegou como 40 num sítio que guarda 0,4 — tipicamente
> um ficheiro de parâmetros editado à mão ou uma chamada de automação.

<!-- tabela: **Tabela 131** — Mensagens da fração atendível e a providência de cada uma -->
| Mensagem | O que a provocou | O que fazer |
| :--- | :--- | :--- |
| «… parece estar em percentual» | fração entre 1 e 100 no ficheiro, no vetor semanal, mensal ou diário, ou na automação | introduza 0,4 para 40% |
| «… fora de [0, 100]» | percentagem negativa ou acima de 100 no ecrã, na tabela de cenários, na folha de cálculo ou em `--share` | corrija; 40 significa 40% |
| campo laranja, ou pergunta «Simular mesmo assim?» | percentagem entre 0 e 1 | se queria 40%, digite 40; se queria mesmo menos de 1%, confirme |

---

### 6.2.2. Série de precipitação

O programa não distingue um dia seco de um dia sem registo, e por isso não adivinha: uma falha na
série interrompe o cálculo, com a indicação de onde está. Preencher a falha, ou recortar a série
para um período sem falhas, é uma decisão de quem conduz o estudo, e a decisão tem de constar do
estudo.

<!-- tabela: **Tabela 132** — Mensagens de erro da série de precipitação e a providência de cada uma -->
| Mensagem | Causa | O que fazer |
| :--- | :--- | :--- |
| «A série de precipitação está vazia» | ficheiro sem nenhuma linha numérica | confira se o ficheiro tem uma coluna de valores diários, um por linha |
| «… dia(s) sem valor numérico, o primeiro no dia N» | falha de registo: linha vazia ou texto a meio da série | preencha as falhas ou recorte a série, e declare o tratamento |
| «… valor(es) negativo(s), o primeiro de X mm no dia N» | sentinela de falha, como −999 | trate-o como falha: preencha ou recorte |

Uma linha de cabeçalho antes dos dados, como «Data;Precipitação», não é erro: é ignorada e a
leitura começa na primeira linha numérica.

---

### 6.2.3. Varredura

<!-- tabela: **Tabela 133** — Mensagens de erro da varredura de volumes -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «O volume máximo da varredura deve ser finito e não negativo» | campo vazio ou negativo | introduza o volume máximo em litros |
| «O passo de varredura deve ser finito e maior que zero» | passo zero ou vazio | introduza o passo; será arredondado para o múltiplo de 250 L |

Há ainda um aviso que não é um erro e convém não confundir com um: quando o passo da varredura é
ajustado para o múltiplo de 250 L, ou quando o limite de quarenta volumes obriga a alargá-lo, o
programa regista o ajuste e prossegue normalmente. O que esse aviso exige do utilizador é apenas
que declare no estudo o passo efetivamente utilizado, e não o passo originalmente pedido.

---

### 6.2.4. Cloragem

<!-- tabela: **Tabela 134** — Mensagens de erro dos parâmetros de cloragem -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Pureza deve ficar em (0, 1]» | pureza introduzida como percentagem | introduza 0,65 para 65%, e não 65 |
| «A dose não pode ser negativa» | dose menor do que zero | corrija |
| «O fator de emissão não pode ser negativo» | fator de emissão do produto menor do que zero | corrija; o fator é por quilograma de produto comercial |

---

### 6.2.5. Análise económica

<!-- tabela: **Tabela 135** — Mensagens de erro da análise económica e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «… deve ser um número finito e não negativo» | investimento, tarifa, custo, potência ou volume vazio, negativo ou infinito | a mensagem nomeia o campo; preencha-o com um número igual ou maior do que zero |
| «O período de análise deve ser um número inteiro de anos» | período fracionário, zero ou negativo | introduza o período em anos inteiros |
| «… deve ser um número finito e maior que -100%» | atualização, inflação ou taxa de atualização de −100% ou menos | confira o sinal da taxa |
| «… parece estar em percentual» | taxa anual introduzida como 5 numa função que espera uma fração decimal | introduza 0,05 para 5% |

> **Unidade das taxas.** Na interface e no ficheiro de projeto, toda a taxa é introduzida em
> percentagem, com a unidade ao lado do campo: a taxa de atualização e a inflação em % por mês ou
> em % por ano, conforme o botão ao lado, e as atualizações tarifárias em % por período de
> atualização, cujo comprimento em meses está no campo vizinho. O projeto grava a taxa de
> atualização e a inflação em % por mês. A conversão entre mês e ano é composta, (1 + i)^12 − 1, e
> não uma multiplicação por doze: 1% por mês equivale a 12,68% por ano. Na automação, as funções
> de cálculo anual recebem as taxas como fração decimal, 0,05 para 5%, e recusam um valor que
> pareça uma percentagem em vez de o reinterpretar.

---

### 6.2.6. Decisão multicritério

<!-- tabela: **Tabela 136** — Mensagens de erro da decisão multicritério e a providência de cada uma -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Informe 3 pesos de eixo ou 7 pesos de critérios TOPSIS» | número de pesos diferente de 3 ou de 7 | introduza um peso por eixo ou um por critério |
| «Os pesos TOPSIS devem ser finitos e não negativos» | peso vazio ou negativo | corrija; o peso zero é válido e exclui o critério |
| «Ao menos um peso TOPSIS deve ser maior que zero» | todos os pesos a zero | atribua peso a pelo menos um critério |
| «O critério TOPSIS … da alternativa N não é finito» | indicador indefinido numa alternativa, tipicamente um período de recuperação sem retorno | confira a alternativa indicada antes de decidir |

---

### 6.2.7. Eletrobomba

<!-- tabela: **Tabela 137** — Mensagens de erro dos parâmetros da eletrobomba -->
| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Rendimento deve ficar em (0, 1]» | rendimento como percentagem no núcleo | use 0,55 para 55% |
| «Rendimento do motor deve ficar em (0, 1]» | idem, no campo do motor | deixe em branco para o programa adotar a sua tabela de rendimentos predefinida |

---

### 6.2.8. Ficheiros

<!-- tabela: **Tabela 138** — Situações de erro na leitura e na gravação de ficheiros -->
| Situação | O que acontece | O que fazer |
| :--- | :--- | :--- |
| série de chuva ilegível | a leitura é interrompida com uma mensagem | confira o formato: uma leitura por linha, em mm, coluna única |
| ficheiro `.triton` com JSON inválido | a abertura é interrompida | o ficheiro pode estar truncado; recorra à cópia de segurança |
| secção em falta no ficheiro | os campos assumem o valor por omissão da classe | esperado ao abrir um ficheiro de versão anterior; reveja o separador correspondente |
| base de chuva por concelho não encontrada | o separador oferece só um ficheiro próprio | veja a secção 1.2 |

---

### 6.2.9. Avisos que não interrompem

Os avisos reunidos nesta tabela não impedem o cálculo e não indicam defeito: são observações que o
programa faz sobre as condições em que o resultado foi produzido. Todas têm de ser transportadas
para o texto do estudo, porque todas afetam a interpretação do número e nenhuma é evidente no
resultado isolado.

<!-- tabela: **Tabela 139** — Avisos que não interrompem o cálculo e têm de constar do estudo -->
| Aviso | O que significa |
| :--- | :--- |
| tipologia não residencial com tarifa residencial | o resultado económico está **subestimado**; veja a secção 3.5 |
| a classe-alvo recomenda filtração fina e esta foi dispensada | decisão registada no relatório |
| fator de emissão com etiqueta de triagem | o fator não tem fonte primária; declare-o |
| estrutura tarifária incompleta | a estrutura introduzida tem uma lacuna; confira-a com o tarifário publicado |
| passo de varredura ajustado | o passo efetivo difere do pedido |
| extrapolação de preço com R² baixo | o volume está fora da tabela de preços e a regressão não é fiável |

---

### 6.2.10. Quando o resultado parece errado

Antes de suspeitar de um defeito do programa, três conferências resolvem a maior parte dos casos em
que o resultado surpreende, e cada uma corresponde a um erro de entrada com assinatura própria.

Quando o **potencial sai maior do que o esperado**, o suspeito imediato é a fração satisfazível: é
o teto de todo o resultado, e uma fração demasiado generosa infla tudo o que vem depois sem que
nada no relatório denuncie a origem.

Quando o **potencial sai muito menor**, confira a lâmina de descarte. O engano correspondente está
descrito na secção 5.1.3, e consiste em introduzir o descarte em litros quando o campo pede
milímetros — o que descarta, tipicamente, a chuva inteira de todos os dias.

Quando o **retorno do investimento sai absurdo**, em qualquer das duas direções, confira a
estrutura tarifária (parte fixa, escalões, saneamento). É a causa mais frequente de um resultado
económico implausível, e a secção 3.3 traz o teste que a identifica em dois minutos.

Vale ainda percorrer as quatro etapas de entrada antes de aceitar qualquer resultado. A barra
lateral assinala as que continuam com pendência, e conferir quatro ecrãs custa menos tempo do que
descobrir o engano depois de o relatório estar emitido.

---

## 6.3. Histórico de versões e o que mudou

Esta secção regista o que mudou entre as versões do programa e, sobretudo, **que mudanças alteram
resultados já publicados**. A distinção importa mais do que parece: uma correção de interface não
afeta nenhum estudo anterior, ao passo que uma correção de cálculo pode deslocar cada número de um
trabalho já submetido. Quem publicou com o Triton precisa de saber em que categoria cai cada
alteração, e é por isso que o histórico abaixo separa as duas coisas de forma explícita.

==A regra que orienta toda esta secção é simples: uma correção de cálculo obriga a declarar a
versão usada; uma correção de interface, não.==

---

### 6.3.1. A versão que está a usar

O número da versão aparece na barra lateral, no rodapé e no menu **Sobre o Triton**. É também
gravado dentro de cada ficheiro de projeto e impresso em cada relatório, de modo que um estudo
antigo leva sempre consigo a identificação do programa que o produziu. Esta redundância é
deliberada: os relatórios circulam separados dos ficheiros, e a pergunta «com que versão foi isto
feito?» costuma surgir meses depois, quando já ninguém se lembra.

O esquema de numeração segue a convenção corrente em engenharia de software. O primeiro número
indica a geração do programa, e a sua mudança significa uma reformulação do modelo conceptual; o
segundo indica um conjunto de funcionalidades novas; e o terceiro indica correções e ajustes que
não alteram a arquitetura. Um primeiro número igual a zero marca uma versão beta: o programa é
utilizável e está verificado como a secção 5.3 descreve, mas a interface, o formato de
ficheiro e os valores por omissão ainda podem mudar, e uma mudança pode alterar resultados.

A versão atual é a beta **0.1.0**. Nenhuma versão anterior circulou, e nenhum estudo foi feito com
alguma.

---

### 6.3.2. Como este histórico é mantido

A partir daqui, cada versão publicada ganha uma entrada própria nesta secção, com a data de
lançamento e o que mudou, sempre separado em duas listas: ==o que altera os resultados de estudos
já feitos e o que não altera.== A entrada mais recente vem primeiro.

Cada entrada segue o mesmo modelo, para que duas versões se possam comparar sem reler: uma frase
de resumo, as novidades, as correções que alteram resultados, as que não alteram, e o que mudou na
documentação. As secções sem conteúdo nessa versão simplesmente não aparecem.

A mesma lista é distribuída com o código, no ficheiro `CHANGELOG.md` da raiz do repositório, e
alimenta a página de versões do sítio de documentação. Não é escrita três vezes: as três saem
desta secção, e uma verificação automática recusa a montagem se divergirem. Quem acompanha o
programa pelo repositório, pelo sítio ou pelo manual lê o mesmo registo.

<!-- tabela: **Tabela 140** — **Tabela 99** — Panorama das versões publicadas -->
| Versão | Data | O que trouxe | Correções que alteram resultados |
| :--- | :--- | :--- | ---: |
| **0.1.0** | 15 de outubro de 2026 | Primeira versão beta do Triton, com nome, numeração e repositório próprios para cada edição. | 0 |

---

### 6.3.3. Versão 0.1.0 (beta) — 15 de outubro de 2026

> **Numa frase.** Primeira versão beta do Triton, com nome, numeração e repositório próprios para
> cada edição.

#### 6.3.3.1. Novidades

O Triton simula o aproveitamento de águas pluviais dia a dia e inclui o motor de simulação, a
avaliação de ciclo de vida, a linha de tratamento, a decisão multicritério e a modulação
probabilística. Esta é a primeira versão da Edição Ibérica (IBE, antes Edição Portugal), que tem repositório, logótipo e
numeração próprios, com a chuva E-OBS por concelho, os tarifários de Lisboa, do Porto e do Funchal
e os valores em euros. A regra de operação de Fewkes (φ) está disponível como opção em todos os
módulos.

#### 6.3.3.2. Correções que alteram resultados

Nenhuma: esta é a primeira versão beta, e não há versão anterior a corrigir.

<!-- tabela: **Tabela 141** — Correções que alteram resultados na versão 0.1.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

#### 6.3.3.3. Correções que não alteram resultados

Nenhuma.

---

### 6.3.4. Como saber se a sua versão tem uma correção

O procedimento é direto e não depende de consultar ninguém: abra um dos ficheiros de exemplo que
acompanham o programa, descritos no apêndice J, execute-o e compare o resultado obtido com o
valor impresso neste manual. Cada caso de exemplo foi gerado pela mesma versão do programa que
gerou este manual, e cada número publicado tem a verificação automática correspondente, como a
secção 5.3 descreve. Uma divergência, portanto, indica que o programa instalado não é o da
versão deste manual.

==Se os números coincidirem, a sua instalação corresponde exatamente ao manual que tem em mãos.==
Se não coincidirem, a diferença não é um defeito da sua instalação, mas uma diferença de versão que
é preciso identificar antes de qualquer estudo.

---

### 6.3.5. O que declarar num trabalho publicado

A boa prática de reprodutibilidade computacional exige que um trabalho identifique de forma
inequívoca o programa que produziu os resultados. No caso do Triton, bastam quatro informações, e
todas estão disponíveis sem esforço: a versão do programa, que aparece no relatório; a origem da
série de precipitação, com o período utilizado; a estrutura tarifária adotada, com a data de
entrada em vigor; e a declaração de quais os parâmetros alterados em relação aos valores por
omissão. A secção 4.10 traz a lista completa, com um parágrafo de método pronto a adaptar.

Anexar o ficheiro `.triton` ao material suplementar resolve as quatro de uma só vez, porque o
ficheiro é autocontido: traz a série de chuva dentro dele ou, com a chuva E-OBS por concelho, a
referência da série e a sua impressão digital, que o programa recompõe a partir da base. É a forma
mais económica de tornar um estudo verificável por terceiros, e custa um pequeno anexo.

---

## 6.4. Como relatar um problema

Os programas de simulação têm defeitos, e o Triton não é exceção. A revisão conduzida antes desta
versão beta encontrou uma dúzia de defeitos de cálculo, nenhum acompanhado de mensagem de erro, e a
maioria descoberta não pela leitura do código mas pela comparação entre dois pontos do próprio
programa que deviam concordar e não concordavam. A lição prática é que o utilizador atento é a
melhor fonte de deteção de que um programa científico dispõe, e é por essa razão que esta secção
existe.

==Um bom relato é aquele que permite reproduzir o problema sem a sua presença.== Tudo o que se pede
abaixo serve esse único objetivo.

---

### 6.4.1. O que enviar

Um relato útil tem quatro componentes, e a ausência de qualquer um deles costuma transformar a
investigação numa troca de mensagens que consome mais tempo a todos do que a própria correção.

**O ficheiro do projeto.** É o item mais importante, e por si só substitui páginas de descrição. O
`.triton` é autocontido: traz todos os parâmetros e a série de chuva inteira dentro dele — ou,
com a chuva E-OBS por concelho, a referência exata da série e a sua impressão digital, que o
programa recompõe a partir da base —, de modo que quem o receber reproduz exatamente a sua
simulação, no mesmo computador ou noutro qualquer. Sem ele, a investigação começa por tentar
adivinhar as entradas, e adivinhar entradas é a maneira mais eficiente de não encontrar um defeito.

**O que esperava e o que obteve.** Esta é a parte que só o utilizador pode fornecer. Descreva o
número que apareceu e o número que devia ter aparecido, com a justificação do segundo — seja um
cálculo à mão, um resultado de uma versão anterior, um valor da literatura ou simplesmente a ordem
de grandeza que a experiência sugere. Um relato que diz apenas «o resultado está errado» deixa ao
destinatário a tarefa de descobrir qual dos quarenta números do ecrã é o errado.

**A versão do programa.** Aparece na barra lateral, no rodapé e no menu **Sobre o Triton**, e já
está gravada dentro do ficheiro de projeto e de qualquer relatório exportado. Indique-a mesmo
assim, porque é o primeiro filtro da investigação: metade dos problemas relatados em programas
científicos são defeitos já corrigidos numa versão posterior à que o utilizador tem instalada.
Indique também a edição.

**A mensagem de erro, se a houver.** Copie o texto integral, e não um resumo. A secção 6.2
lista as mensagens que o programa emite deliberadamente, com o significado e a providência de cada
uma; se a sua mensagem lá estiver, o problema é provavelmente de entrada e tem solução imediata.

---

### 6.4.2. O que conferir antes de relatar

Uma parte considerável dos resultados que parecem errados são resultados corretos de entradas
erradas, e a conferência abaixo leva poucos minutos. Não existe para desencorajar o relato, mas
para que o seu tempo e o de quem investiga sejam gastos no que é, de facto, um defeito.

Comece pela secção 5.1, que reúne os dez enganos de projeto que o programa não tem como
impedir. Três deles respondem pela maioria dos resultados inesperados: a área de captação
introduzida como a área inclinada da cobertura em vez da projeção horizontal, a lâmina de descarte
introduzida em litros em vez de milímetros, e a estrutura do tarifário tratada como um preço único
por metro cúbico quando tem parte fixa e escalões.

Confira em seguida se o comportamento observado não é uma limitação declarada. A secção 5.2
relaciona o que o programa reconhecidamente não faz, e algumas dessas limitações dão exatamente a
impressão de defeito. O caso mais frequente envolve a categoria tarifária: os tarifários que a
edição traz transcritos são os de utilizador doméstico de Lisboa, do Porto e do Funchal, pelo que
um estudo de escola ou de comércio sai com a tarifa doméstica enquanto o utilizador não introduzir
a da categoria correta. O programa avisa disso em vez de corrigir por conta própria, porque a
tabela certa é pública e específica de cada entidade gestora.

---

### 6.4.3. Para onde enviar

O Triton é desenvolvido por um grupo de investigação universitário. O contacto indicado no menu do
programa e no repositório é o canal de relato, e serve tanto para defeitos como para sugestões de
funcionalidades e pedidos de esclarecimento sobre o método. Os relatos podem ser escritos em
português ou em inglês.

Os relatos que vêm acompanhados do ficheiro de projeto entram diretamente na suíte de verificação
descrita na secção 5.3: um caso que reproduz um defeito transforma-se num teste, e o teste
passa a impedir que o defeito volte. É a razão pela qual o ficheiro importa tanto, e é também a
resposta mais completa que se pode dar a quem relatou — o problema não só foi corrigido, como
passou a ser vigiado.

> **Aprofundamento: o que torna um defeito difícil de encontrar.** Os defeitos que sobrevivem anos
> num programa científico têm todos a mesma assinatura: produzem números plausíveis. Um erro que
> gera um valor negativo, ou mil vezes maior do que o esperado, encontra-se à primeira execução. Já
> um fator de rendimento aplicado duas vezes, ou uma unidade convertida uma vez a mais do que o
> necessário, produz um número que passa em qualquer inspeção visual e atravessa anos de uso. É por
> isso que a verificação do programa se apoia em invariantes — o balanço de massa que tem de
> fechar, a monotonia que tem de valer, o teto que a curva não pode cruzar — e não apenas em
> valores esperados. Quando suspeitar de um número, a maneira mais rápida de confirmar a suspeita é
> procurar uma dessas identidades que ele viola.

---

## 6.5. Roteiro de evolução

> Para onde o programa deve ir, e com que evidência. Um roteiro que separa o que está decidido do
> que é intenção permite ao utilizador planear o estudo com a versão que tem hoje, e não com a que
> gostaria de ter.

Esta secção resume o `ROADMAP.md` da raiz do repositório do Triton, que vale para as três edições e
reflete o estado da versão beta 0.1.0. Nada do que está abaixo da linha «Estável» existe nesta
versão: são intenções do grupo de investigação, sem data de entrega. Quando um item é
implementado, sai daqui e entra no histórico de versões, com a indicação de se muda os resultados
de estudos já feitos.

A direção vem de duas fontes. A primeira é a revisão sistemática da literatura que o grupo conduz
sobre a simulação do aproveitamento de águas pluviais; mostra onde os estudos publicados omitem a
regra de operação, a definição de fiabilidade e os parâmetros económicos. A segunda é o registo de
pendências do próprio programa, descrito na secção «Limitações conhecidas».

---

### 6.5.1. O que já é estável na 0.1.0

**Série climática.** Chuva diária E-OBS por concelho (278 concelhos de Portugal, com base de 1950 a
2025), a série ERA5 do Funchal e séries diárias fornecidas pelo utilizador. **Tarifas.** Os
tarifários transcritos de Lisboa, do Porto e do Funchal, e estruturas introduzidas pelo utilizador,
com escalões progressivos, partes fixas e atualização. **Balanço hídrico.** Simulação diária pela
regra do Triton, com a YAS estrita, a YBS e o parâmetro φ de Fewkes (2000b) como opções para
reservatório único. **Decisão.** Multicritério por TOPSIS e por SMAA-VIKOR. **Incerteza.**
Modulação probabilística das premissas (secção «O que é a modulação probabilística»).
**Edição.** Portugal.

A versão 1.0 será a primeira versão oficial, depois dos ajustes das versões 0.x.

---

### 6.5.2. Versão 1.1: consolidação e fiabilidade

Os três primeiros itens vêm do roteiro comum e dizem respeito sobretudo à Edição Internacional.

<!-- tabela: **Tabela 142** — Itens previstos para a versão 1.1 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Dados e tarifas | Fornecedores globais de chuva | Reanálises ERA5-Land e NOAA GHCN-Daily |
| Dados e tarifas | Unidades métricas e imperiais | Conversão sem resíduo, com a conservação de massa conferida nas duas |
| Dados e tarifas | Tarifas sazonais e de escassez | Escalões dinâmicos, sobretaxa de seca, saneamento separado |
| Decisão multicritério | Ordenação completa com plano GAIA | PROMETHEE II |
| Decisão multicritério | Limiares de veto e classes de viabilidade | ELECTRE Tri |
| Decisão multicritério | Pesos mais consistentes | Best-Worst Method (BWM) |
| Probabilidade e risco | Dependência entre chuva e procura | Cópulas bivariadas (Clayton, Gumbel) |
| Probabilidade e risco | Que variáveis governam o resultado | Índices de Sobol de primeira ordem e totais |
| Probabilidade e risco | Chuva sintética | Bootstrap em blocos, com os dias secos consecutivos preservados |
| Custos e engenharia | Custo de instalação por material e por solo | Curvas paramétricas por tecnologia e por classe de solo |
| Custos e engenharia | Custo de exploração detalhado | Filtros, desinfeção, curva de degradação da bomba |

### 6.5.3. Versão 2.0: fronteira metodológica

<!-- tabela: **Tabela 143** — Itens previstos para a versão 2.0 -->
| Eixo | Item | Método |
| :--- | :--- | :--- |
| Física do sistema | Passo de tempo horário | Modelo horário com dados de udógrafo |
| Física do sistema | Balanço hídrico na zona radicular | FAO-56 Penman-Monteith, para a rega |
| Física do sistema | Coeficiente de escoamento variável | Depende da lâmina e da estiagem antecedente |
| Territorial | Escala de bacia urbana | Vetores GeoJSON |

---

### 6.5.4. Como ler este roteiro

**A ordem não é um compromisso de datas.** A ordem segue a consequência sobre o resultado de um
estudo. O passo horário, por exemplo, só chega na 2.0 porque exige dados de udógrafo que a maioria
dos concelhos não tem.

**Um item entra pela evidência.** Cada método listado responde a uma lacuna medida na revisão da
literatura, e não a uma preferência de implementação.

**Uma alteração que muda resultados é declarada.** Quem publica com o programa tem de registar a
versão usada. Por isso o histórico de versões separa a correção que muda um número de um estudo
já feito da que muda só a interface.

---

# 7. Modulação probabilística

---

## 7.1. O que é a modulação probabilística

> **Pergunta a que este capítulo responde:** o volume que o estudo escolheu continua a ser uma boa
> escolha quando as premissas não são exatamente as que declarei?

O estudo do Triton responde com um número por volume. Esse número vale para as premissas
declaradas: um consumo per capita, um número de pessoas, uma fração não potável, uma área de
captação, uma tarifa, uma taxa de atualização. Nenhuma delas é conhecida com exatidão na fase de
projeto. O consumo per capita de uma casa que ainda não existe é estimado; a ocupação muda ao longo
da vida útil; a chuva dos próximos vinte anos não repete a dos últimos trinta; os tarifários são
revistos.

A ferramenta **13. Modulação Probabilística** mede quanto dessas incertezas chega ao resultado.
Refaz o estudo pronto muitas vezes — mil, por omissão —, de cada vez com as premissas escolhidas
sorteadas a partir de distribuições declaradas pelo utilizador, e devolve a **distribuição** do
resultado em vez de um valor único: gamas de poupança e de valor atual líquido por volume, a
probabilidade de o investimento se pagar e a frequência com que cada volume seria o escolhido.

==O estudo determinístico não muda.== As etapas 5 a 9, os relatórios e a linha de comandos
continuam com ele. A modulação é uma camada de robustez por cima do estudo: não escolhe outro
volume, diz até que ponto a escolha resiste.

---

### 7.1.1. Quando usar

A modulação responde a três perguntas a que o estudo determinístico não responde:

1. **Quão largo é o resultado?** Com que margem vale a poupança do estudo? A gama entre os
   percentis 5 e 95 das realizações é o número que deve acompanhar o resultado publicado.
2. **Com que probabilidade se paga o investimento?** Um valor atual líquido positivo no caso-base
   pode esconder uma probabilidade considerável de prejuízo; a modulação dá essa probabilidade e o
   respetivo intervalo de confiança. No tutorial de Lisboa, com os custos ilustrativos (não são
   preços de mercado) e a tarifa de Lisboa, o valor atual líquido do caso-base já é negativo, e a
   pergunta passa a ser outra: haverá alguma gama de premissas plausível em que o sistema se pague?
3. **A decisão de projeto é estável?** Se o volume escolhido vence numa minoria das realizações,
   ao lado de vizinhos com frequências parecidas, a escolha é frágil e o texto tem de o dizer.

No exemplo do tutorial, na secção 7.4, mostra-se como se leem as três respostas.

É a continuação natural da análise de sensibilidade da secção 3.7. A sensibilidade varia uma
premissa de cada vez; a modulação varia em simultâneo todas as escolhidas, com pesos que vêm das
distribuições, e permite ver combinações que um gráfico de tornado não mostra.

### 7.1.2. O que ela não faz

A modulação não substitui um dado medido. Uma distribuição larga em torno de um valor errado
continua centrada no valor errado: quando houver medição de consumo, ela vale mais do que qualquer
sorteio. As distribuições iniciais que o ecrã propõe são **de triagem** — centradas no projeto,
com larguras genéricas — e têm de ser ajustadas ao que se sabe do edifício. A secção 7.5
discute os limites do método.

---

## 7.2. As variáveis e as distribuições

> **Pergunta a que esta secção responde:** o que posso sortear, e como descrevo a incerteza de cada
> premissa?

### 7.2.1. O catálogo de variáveis

A ferramenta sorteia vinte premissas, organizadas em sete grupos. Ao abrir, só as três de consumo
vêm marcadas — o consumo per capita, o número de pessoas e a fração não potável —, porque são as
mais incertas num projeto novo e as que a literatura mostra moverem o resultado (Silva e Ghisi,
2016). As restantes ficam com o valor do estudo até o utilizador as marcar.

<!-- tabela: **Tabela 144** — As variáveis que a modulação probabilística pode sortear, com a distribuição de triagem que o ecrã propõe -->
| Grupo | Variável | Unidade | Distribuição de triagem | Marcada ao abrir |
| :--- | :--- | :--- | :--- | :--- |
| Procura | Consumo per capita | L/hab.dia | lognormal, média do projeto, CV de 20% | sim |
| Procura | Número de pessoas | pessoas | normal, média do projeto, desvio de 1 pessoa; inteiro de 1 ao dobro | sim |
| Procura | Fração não potável interior | % | normal, média do projeto, desvio de 5 pontos; 0 a 100% | sim |
| Procura | Procura exterior | L/dia | normal, média do projeto, CV de 30% | não |
| Captação | Área de captação | m² | normal, média do projeto, CV de 5% | não |
| Captação | Coeficiente de escoamento | — | triangular, do projeto −0,10 ao projeto +0,05; 0 a 1 | não |
| Captação | Lâmina de descarte | mm | uniforme, do projeto −1 mm ao projeto +1 mm | não |
| Chuva | Fator da chuva | × | normal, média 1, desvio de 0,10 | não |
| Tarifas | Fator das tarifas de água e saneamento | × | normal, média 1, desvio de 0,10 | não |
| Tarifas | Fator do saneamento | × | normal, média 1, desvio de 0,10 | não |
| Tarifas | Atualização tarifária | % por período | normal, média do projeto, desvio de 2 pontos | não |
| Tarifas | Tarifa de energia | €/kWh | normal, média do projeto, CV de 10% | não |
| Tarifas | Atualização da energia | % por período | normal, média do projeto, desvio de 2 pontos | não |
| Custos | Fator do investimento | × | lognormal, média 1, desvio de 0,15 | não |
| Custos | Fator do preço da cisterna | × | lognormal, média 1, desvio de 0,15 | não |
| Custos | Fator do custo de exploração (O&M) | × | lognormal, média 1, desvio de 0,25 | não |
| Custos | Inflação do custo de exploração | % por mês | normal, média do projeto, desvio de 0,10 ponto | não |
| Fluxo de caixa | Taxa de atualização | % por mês | normal, média do projeto, desvio de 0,25 ponto | não |
| Fluxo de caixa | Período de análise | anos | triangular, do projeto −5 ao projeto +5 anos; inteiro, pelo menos 1 | não |
| Ambiente | Fator da emissão da água potável | × | normal, média 1, desvio de 0,20 | não |
| Ambiente | Fator da emissão da rede elétrica | × | normal, média 1, desvio de 0,20 | não |

Cada grupo atua num ponto diferente da cadeia de cálculo:

- **Procura** muda o consumo diário e a fração que a água da chuva pode satisfazer. A fração
  satisfazível total é recalculada a cada sorteio a partir da fração interior e da procura
  exterior, pela mesma regra do estudo (secção 4.2). Nos modos semanal, mensal e diário, as
  séries recebem o fator sorteado: o perfil do calendário mantém-se, e o nível muda.
- **Captação** muda o volume de chuva que chega à cisterna: área, coeficiente de escoamento e
  lâmina de descarte.
- **Chuva** multiplica toda a série diária por um fator. É a forma mais simples de representar uma
  chuva futura mais seca ou mais húmida do que a histórica.
- **Tarifas** muda o preço da água, do saneamento e da energia e as respetivas atualizações.
- **Custos** muda o investimento inicial e o custo anual de exploração e manutenção.
- **Fluxo de caixa** muda a taxa de atualização e o horizonte da análise.
- **Ambiente** muda os fatores de emissão da avaliação de ciclo de vida.

### 7.2.2. O que cada variável económica multiplica ou substitui

As variáveis económicas são de dois tipos. As que têm unidade própria — atualizações, taxa,
inflação, tarifa de energia, período — **substituem** o valor do projeto pelo sorteado. Os
**fatores** (×) multiplicam um valor do projeto e valem 1 no estudo: um fator sorteado de 1,15
representa um custo 15% acima do orçamentado. A tabela diz sobre o que atua cada um e o que deixa
de fora.

<!-- tabela: **Tabela 145** — O que cada variável económica e ambiental faz no cálculo, e o que não toca -->
| Variável | Atua sobre | Não toca |
| :--- | :--- | :--- |
| Fator das tarifas de água e saneamento | todos os valores monetários da estrutura da água — escalões, parcela fixa, fatura mínima, preço-base da curva exponencial — e o saneamento cobrado em euros (fixo ou por m³) | o expoente da curva exponencial; o saneamento em % da água, que já acompanha a água |
| Fator do saneamento | a tarifa de saneamento, no modo declarado no projeto: a percentagem, o valor fixo ou o preço por m³ | a tarifa da água |
| Atualização tarifária | a atualização da água e do saneamento em cada período de atualização, no lugar da declarada | a atualização da energia |
| Tarifa de energia | o preço do kWh da bombagem, no lugar do declarado | — |
| Atualização da energia | a atualização da tarifa de energia em cada período | — |
| Fator do investimento | o investimento inicial **inteiro** de cada volume: cisterna, reservatório superior, eletrobomba, tubagem, acessórios, mão de obra e linha de tratamento | o custo anual de exploração |
| Fator do preço da cisterna | só o preço da cisterna de cada volume, a parte do investimento que cresce com o volume; com a mão de obra automática, esta acompanha-o, pela regra do programa | os restantes itens do investimento |
| Fator do custo de exploração (O&M) | o custo anual de exploração e manutenção: os itens declarados na etapa económica, o custo de exploração da linha de tratamento e o cloro | a energia da bombagem, que tem variáveis próprias |
| Inflação do custo de exploração | a atualização anual do custo de exploração, no lugar da declarada | as tarifas |
| Taxa de atualização | a taxa de desconto do fluxo de caixa | — |
| Período de análise | o horizonte do fluxo de caixa e da avaliação ambiental, em anos inteiros | a série de chuva, que continua a ser a do estudo |
| Fator da emissão da água potável | a emissão por m³ da água da rede que a cisterna evita | o carbono incorporado dos materiais |
| Fator da emissão da rede elétrica | o fator de emissão da energia da bombagem | o carbono incorporado dos materiais |

Os dois fatores de investimento combinam-se. Marcados em conjunto, a cisterna recebe o produto dos
dois, e o resto do investimento só o fator do investimento. Na prática, o fator do investimento
representa a incerteza do orçamento como um todo — região, época, imprevistos —, e o fator da
cisterna a do item que define o ótimo: como o preço da cisterna é a parte do custo que cresce com
o volume, é ele que desloca o volume de menor período de recuperação.

### 7.2.3. A incerteza da chuva

A Edição Ibérica não tem base de séries de modelos climáticos, pelo que a incerteza da chuva
entra pelo **fator da chuva**. O fator multiplica toda a série diária do projeto — a série E-OBS
do concelho, a do Funchal ou um ficheiro do utilizador — e por isso mantém a sua estrutura
temporal: a sequência de estiagens e de dias chuvosos não muda, só o nível. Um fator sorteado com
média 1 e desvio de 0,10 representa uma chuva 10% mais húmida ou mais seca do que o registo, que
é a maneira de representar um clima futuro mais seco ou mais húmido do que o passado. Para testar
uma sequência diferente de estiagens, execute o estudo uma vez com cada série alternativa e
compare.

### 7.2.4. As quatro distribuições

Cada variável marcada recebe uma distribuição e os respetivos parâmetros:

<!-- tabela: **Tabela 146** — As quatro distribuições que a ferramenta oferece, os seus parâmetros e quando usar cada uma -->
| Distribuição | Parâmetros | Quando usar |
| :--- | :--- | :--- |
| normal | média e desvio-padrão | incerteza simétrica em torno de um valor provável |
| lognormal | média e desvio-padrão | grandeza positiva com cauda para cima, como o consumo e o preço da obra |
| triangular | mínimo, moda e máximo | quando se conhecem o intervalo e o valor mais provável, mas não a forma |
| uniforme | mínimo e máximo | quando só se conhece o intervalo |

Na lognormal, a média e o desvio introduzidos são os da própria variável, e não os do seu
logaritmo: o programa calcula os parâmetros da lognormal que devolvem exatamente a média e o
desvio pedidos. Qualquer distribuição pode ser **truncada** por um limite inferior e um superior;
o valor sorteado fora deles é sorteado de novo. O número de pessoas e o período de análise são
arredondados para inteiro e nunca ficam abaixo de 1; a fração não potável e o coeficiente de
escoamento ficam entre 0 e 100% e entre 0 e 1; fatores, preços, áreas e consumos nunca ficam
negativos.

Cada cartão do ecrã mostra a curva da distribuição escolhida, desenhada com 4 000 sorteios, e os
respetivos percentis 5 e 95. É a maneira mais rápida de verificar se a largura declarada é
plausível: um P95 de 400 L/hab.dia para uma habitação indica um desvio exagerado.

### 7.2.5. O nível, e não o ruído do dia

As variáveis são sorteadas **uma vez por realização**: em cada realização, a casa tem um consumo
per capita, uma ocupação e uma fração, válidos para toda a série de chuva. Isto representa a
incerteza sobre **quanto** o edifício consome, que é a que importa. A variação de um dia para o
outro em torno desse nível, opcional (campo «Variação diária»), quase não move o resultado:
sorteada de forma independente a cada dia, anula-se ao longo de trinta anos de série (Silva e
Ghisi, 2016; secção 3.6, subcomando `stochastic-demand`).

---

## 7.3. Como executar

> **Pergunta a que esta secção responde:** quais são os passos, no ecrã e na linha de comandos?

### 7.3.1. Na interface

A ferramenta fica no fim da barra lateral, em **13. Modulação Probabilística**. Parte do estudo que
as etapas 1 a 4 descrevem — a mesma configuração que o programa grava no ficheiro `.triton` —,
com os pesos do TOPSIS e as premissas ambientais do ecrã. Sem série de chuva carregada, a
ferramenta avisa e não executa. Para começar, abra o caso `09_modulacao_tutorial.triton` ou o
`10_modulacao_captacao.triton` (apêndice J): ambos são estudos de Lisboa que chegam com a
ferramenta montada, e basta carregar em **Simular**.

As distribuições partem da triagem do estudo aberto. Ao abrir outro projeto, ou ao mudar uma
premissa nas etapas 1 a 4, os cartões que não foram editados acompanham o novo valor; os editados
ficam como estão. Num estudo de volume fixo, a ferramenta mostra só o volume do estudo: as figuras
e a tabela por volume pedem a varredura da etapa 4.

O ecrã tem quatro blocos, de cima para baixo:

1. **O que variar.** As vinte variáveis, em sete grupos, com caixas de seleção. Passar o cursor
   sobre uma delas mostra o que representa. A secção 7.2 descreve cada grupo.
2. **Distribuições.** Um cartão por variável marcada, com o valor do estudo, a distribuição, os
   parâmetros, os limites e a curva. O botão **Valores de triagem** devolve todas as distribuições
   ao padrão centrado no projeto.
3. **Execução.** O número de realizações (1 000 por omissão), a semente (42) e a variação diária
   opcional. **Simular** executa em segundo plano, com barra de progresso, tempo restante e botão
   **Cancelar**; se for cancelada, a análise mostra as realizações já feitas.
4. **Resultados.** Tabelas e figuras numeradas, explicadas na secção 7.4.

A disposição reorganiza-se com a largura da janela — três, duas ou uma coluna —, e não há
deslocamento lateral. As distribuições, o número de realizações e a semente são gravados no
projeto e regressam ao reabri-lo; os resultados não, porque se refazem iguais com a mesma semente.

O tempo cresce com o número de realizações, de volumes e de anos de chuva. Cada realização refaz a
cadeia técnica, económica, ambiental e TOPSIS para todos os volumes; a aceitabilidade SMAA-VIKOR
(secção 2.10), que sorteia vinte mil vetores de pesos, fica de fora das realizações, porque a
modulação só usa o vencedor do TOPSIS. No tutorial, com 21 volumes e trinta anos de chuva, a barra
de progresso estima o tempo restante a partir das primeiras realizações. O botão **Exportar
(CSV + JSON)** grava as amostras, uma linha por realização, e o resumo completo, com a semente e as
distribuições.

### 7.3.2. Na linha de comandos

O comando `probabilistic-study` usa o mesmo núcleo do ecrã e dá os mesmos números com o mesmo
projeto e a mesma semente:

```
triton probabilistic-study 04_tutorial_varredura.triton --samples 1000 --seed 42
triton probabilistic-study 04_tutorial_varredura.triton --list-variables
triton probabilistic-study projeto.triton --var fator_chuva=normal:1:0.1 --var fator_investimento=lognormal:1:0.15
triton probabilistic-study projeto.triton --var fator_cisterna=lognormal:1:0.15 --var fator_om=lognormal:1:0.25

triton probabilistic-study projeto.triton --format json --output modulacao.json
```

Sem opções de distribuição, o comando lê as que o ecrã gravou no projeto ou, na falta delas, os
valores de triagem. `--var VARIÁVEL=DISTRIBUIÇÃO` liga qualquer variável do catálogo e pode ser
repetida; as distribuições escrevem-se `normal:média:desvio`, `lognormal:média:desvio`,
`triangular:mínimo:moda:máximo`, `uniforme:mínimo:máximo` ou `fixo`. Os atalhos `--per-capita`,
`--people` e `--non-potable` valem para as três variáveis de consumo, e `--daily-cv` para a
variação diária. `--list-variables` lista as variáveis do catálogo. O formato `csv` grava as
amostras; o `json`, o resultado inteiro. O nome antigo do comando, `stochastic-study`, continua a
ser aceite.

---

## 7.4. Como ler os resultados

> **Pergunta a que esta secção responde:** o que diz cada tabela e cada figura, e o que declarar num
> relatório ou num artigo?

O exemplo desta secção é o projeto do tutorial de Lisboa, gravado com a ferramenta já montada no
ficheiro `09_modulacao_tutorial.triton` (apêndice J), com seis variáveis sorteadas: as três de
consumo, o fator da chuva, o fator das tarifas e o fator do investimento, com as distribuições de
triagem, em mil realizações e semente 42. Os números das tabelas são os que o programa calcula;
executar a ferramenta com o mesmo projeto e a mesma semente reproduz-os. Os custos do projeto são
ilustrativos, não são preços de mercado.

### 7.4.1. O que entrou

A primeira tabela do ecrã diz o que foi de facto sorteado: o valor do estudo, a distribuição
declarada e as estatísticas da amostra. É a primeira a ler, porque confirma que as distribuições
produziram o que se pretendia — a média da amostra deve ficar perto da média declarada, e o
intervalo entre P5 e P95 deve ser plausível para o edifício.

<!-- tabela: **Tabela 147** — As variáveis sorteadas no exemplo do tutorial: distribuição declarada e estatísticas das realizações -->
| Variável | No estudo | Distribuição | Média | Desvio-padrão | P5 | P95 |
| :--- | ---: | :--- | ---: | ---: | ---: | ---: |
| Consumo per capita (L/hab.dia) | 150,0 | lognormal (150,0; 30,0) | 149,1 | 29,4 | 105,3 | 202,6 |
| Número de pessoas (pessoas) | 4 | normal (4; 1) | 3,9 | 1,0 | 2 | 6 |
| Fração não potável interior (%) | 28,0 | normal (28,0; 5,0) | 28,2 | 5,1 | 19,3 | 36,3 |
| Fator da chuva (×) | 1,00 | normal (1,00; 0,10) | 1,00 | 0,10 | 0,84 | 1,16 |
| Fator das tarifas de água e saneamento (×) | 1,00 | normal (1,00; 0,10) | 1,00 | 0,10 | 0,83 | 1,16 |
| Fator do investimento (×) | 1,00 | lognormal (1,00; 0,15) | 1,01 | 0,15 | 0,77 | 1,27 |

### 7.4.2. O resultado no volume escolhido

A segunda tabela resume o volume que o estudo escolheu — o vencedor do TOPSIS do caso-base —,
comparando o estudo determinístico com a média, o desvio-padrão, o coeficiente de variação e os
percentis das realizações.

<!-- tabela: **Tabela 148** — Resultados no volume escolhido pelo estudo do tutorial: estudo determinístico e estatísticas das realizações (valores em €, ilustrativos, não são preços de mercado) -->
| Grandeza | Estudo determinístico | Média | Desvio-padrão | CV (%) | P5 | P50 | P95 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Poupança de água potável (%) | 23,7 | 23,5 | 4,5 | 18,9 | 16,4 | 23,4 | 31,2 |
| VAL (€, ilustrativo, não é preço de mercado) | −4 839 | −5 150 | 1 440 | 28,0 | −7 485 | −5 167 | −2 828 |
| Período de recuperação descontado (anos) | — | 14,3 | 0,0 | 0,0 | 14,3 | 14,3 | 14,3 |
| Saldo de CO₂ no ciclo de vida (kg) | −803 | −803 | 1 | 0,1 | −804 | −803 | −801 |

Duas leituras importam. A primeira é a **largura**: o intervalo entre P5 e P95 contém 90% das
realizações e é o número que deve acompanhar o resultado publicado. A segunda é a **posição do
estudo determinístico** em relação à mediana. Quando a mediana fica abaixo do caso-base, as
não linearidades do sistema — a tarifa por escalões, a parte fixa da fatura, a cisterna que
transborda — fazem as realizações desfavoráveis pesar mais do que as favoráveis, e o caso-base é
otimista.

O período de recuperação descontado só existe quando o investimento se paga; a tabela calcula-o
sobre as realizações em que isso acontece, e o ecrã diz quantas foram. Com a tarifa de Lisboa e os
custos ilustrativos do tutorial, o caso-base não recupera o investimento (secção 4.7), e o
que a tabela de probabilidades acrescenta é a medida de quão perto, ou quão longe, as premissas
sorteadas levam esse resultado de uma recuperação.

<!-- tabela: **Tabela 149** — Probabilidades no volume escolhido, com o intervalo de confiança de 95% de Wilson -->
| Evento | Probabilidade (%) | IC 95%, limite inferior (%) | IC 95%, limite superior (%) |
| :--- | ---: | ---: | ---: |
| o investimento recupera-se (VAL > 0) | 0,1 | 0,0 | 0,6 |
| o saldo de CO₂ no ciclo de vida é positivo | 0,0 | 0,0 | 0,4 |

A probabilidade de o investimento se pagar é a proporção de realizações com valor atual líquido
positivo. O intervalo de confiança de 95% ao lado é o de Wilson (1927), adequado a amostras
pequenas e a proporções perto de 0% ou de 100%. Mede a incerteza do **sorteio**, e não a das
premissas: com mais realizações estreita-se; a probabilidade em si, não.

### 7.4.3. As gamas por volume

As figuras seguintes mostram a gama entre os percentis 5 e 95, a mediana e o estudo determinístico
ao longo de todos os volumes. A linha a tracejado marca o volume escolhido, e os valores escritos
são os dele (Figura 69 e Figura 70).

![A poupança de água potável por volume no exemplo do tutorial](../figuras/fig52_modulacao_economia.png)

*Figura 69 — Poupança de água potável por volume do reservatório inferior no exemplo do tutorial: gama entre os percentis 5 e 95 das realizações, mediana e estudo determinístico. Os valores marcados são os do volume escolhido pelo estudo (linha a tracejado).*

![O valor atual líquido por volume no exemplo do tutorial](../figuras/fig53_modulacao_vpl.png)

*Figura 70 — Valor atual líquido por volume do reservatório inferior no mesmo exemplo (custos ilustrativos, não são preços de mercado). Uma gama que atravessa o zero em todos os volumes indica que nenhum deles se paga com certeza; uma mediana abaixo do estudo determinístico, que o caso-base é otimista.*

### 7.4.4. A estabilidade da escolha

A tabela e a figura de frequência contam, em cada realização, qual volume seria o ideal técnico,
qual seria o ótimo económico — o de menor período de recuperação descontado, critério do programa
(secção 4.9) — e qual venceria o TOPSIS (Figura 71). Uma realização
em que nenhum volume se paga aparece como «nenhum se paga» na coluna económica.

<!-- tabela: **Tabela 150** — Frequência com que cada volume é escolhido nas realizações do exemplo, por critério (%) -->
| Volume (m³) | Ideal técnico | Ótimo económico (recuperação) | Vencedor TOPSIS |
| :--- | ---: | ---: | ---: |
| 3 | 0 | 0 | 0 |
| 4 | 13 | 0 | 0 |
| 5 | 57 | 0 | 0 |
| 6 | 25 | 0 | 0 |
| 7 | 4 | 0 | 1 |
| 8 | 1 | 0 | 1 |
| 9 | 0 | 0 | 1 |
| 10 | 0 | 0 | 3 |
| 11 | 0 | 0 | 3 |
| 12 | 0 | 0 | 5 |
| 13 | 0 | 0 | 8 |
| 14 | 0 | 0 | 10 |
| 15 | 0 | 0 | 11 |
| 16 | 0 | 0 | 11 |
| 17 | 0 | 0 | 10 |
| 18 | 0 | 0 | 11 |
| 19 | 0 | 0 | 8 |
| 20 | 0 | 0 | 19 |
| nenhum se paga | 0 | 100 | 0 |

![A frequência com que cada volume é escolhido no exemplo do tutorial](../figuras/fig54_modulacao_frequencia.png)

*Figura 71 — Frequência, em percentagem das realizações, com que cada volume é o ideal técnico, o ótimo económico e o vencedor do TOPSIS no exemplo do tutorial.*

A leitura é a mesma da aceitabilidade SMAA-VIKOR (secção 2.10): um volume que vence na maioria
das realizações é uma recomendação robusta; um que vence numa minoria, ao lado de vizinhos com
frequências parecidas, é uma preferência que depende das premissas, e o texto tem de o dizer.

### 7.4.5. O que mais pesa

A sensibilidade (Figura 72) mede-se pela correlação de postos de
Spearman (1904) entre cada variável sorteada e o resultado no volume escolhido. O coeficiente ρ
vai de −1 a 1: o sinal diz o sentido do efeito, e o módulo a sua força. Por usar postos, e não
valores, capta relações monótonas não lineares — como a da tarifa por escalões — e não é
distorcido por realizações extremas.

<!-- tabela: **Tabela 151** — Sensibilidade no volume escolhido: força e sentido da influência de cada variável sorteada sobre os resultados do tutorial -->
| Variável | ρ com a poupança | ρ com o VAL | ρ com o saldo de CO₂ |
| :--- | ---: | ---: | ---: |
| Número de pessoas | −0,57 | 0,57 | −0,67 |
| Fator do investimento | −0,07 | −0,55 | −0,04 |
| Consumo per capita | −0,41 | 0,42 | −0,44 |
| Fração não potável interior | 0,53 | 0,16 | −0,47 |
| Fator das tarifas de água e saneamento | −0,01 | 0,15 | −0,03 |
| Fator da chuva | 0,20 | 0,02 | −0,23 |

![A sensibilidade no volume escolhido no exemplo do tutorial](../figuras/fig55_modulacao_sensibilidade.png)

*Figura 72 — Correlação de postos de Spearman de cada variável sorteada com a poupança de água potável e com o valor atual líquido no volume escolhido pelo estudo do tutorial, da maior para a menor influência no valor atual líquido.*

A correlação de postos pode mostrar um efeito que a análise de uma premissa de cada vez esconde. A
fração não potável define a procura que a água da chuva pode satisfazer, pelo que é a candidata
natural a mover mais a poupança **percentual**. O número de pessoas e o consumo per capita
aumentam o consumo total: tendem a mover pouco a percentagem, e em sentido contrário, mas podem
mover muito o valor atual líquido, porque mais consumo empurra a fatura para os escalões mais
caros de uma tarifa por escalões e cada metro cúbico poupado passa a valer mais. Leia a tabela para
o seu caso, e verifique qual destes efeitos o tarifário que introduziu permite.

### 7.4.6. Quanto da incerteza vem de cada fonte

O ρ diz o sentido e a força de uma relação monótona, mas não diz que parte da incerteza do
resultado vem de cada variável. Essa parte é a razão de correlação, η²: a variância das médias do
resultado entre classes da variável, dividida pela variância total. As variáveis contínuas são
agrupadas em decis, e o número de pessoas pelos seus próprios valores. O η² estima o índice de
sensibilidade de primeira ordem (Saltelli et al., 2008), vai de 0 a 1 e capta também relações não
monótonas.

<!-- tabela: **Tabela 152** — Parte da variância do resultado explicada por cada variável sorteada no exemplo do tutorial, no volume escolhido (η²; as variáveis contínuas agrupadas em decis) -->
| Fonte de incerteza | η² da poupança | η² do VAL | η² do saldo de CO₂ |
| :--- | ---: | ---: | ---: |
| Fator do investimento | 0,01 | 0,33 | 0,01 |
| Número de pessoas | 0,32 | 0,30 | 0,53 |
| Consumo per capita | 0,18 | 0,19 | 0,20 |
| Fração não potável interior | 0,33 | 0,04 | 0,21 |
| Fator das tarifas de água e saneamento | 0,01 | 0,03 | 0,01 |
| Fator da chuva | 0,05 | 0,01 | 0,04 |
| Soma | 0,91 | 0,90 | 0,99 |

No exemplo, compare as colunas: as variáveis que dominam a variância da poupança raramente são as
que dominam a variância do valor atual líquido, e os fatores sorteados com larguras de triagem
estreitas, como os das tarifas, do investimento e da chuva, costumam pesar pouco. Com variáveis
independentes e efeitos aditivos, a soma fica perto de 1; uma soma bem abaixo de 1 indica
interação entre as variáveis. A estimativa por classes tem um pequeno viés para cima, da ordem do
número de classes dividido pelo número de realizações, e por isso a soma pode exceder ligeiramente
1.

### 7.4.7. A captação e a chuva

O segundo exemplo, gravado no ficheiro `10_modulacao_captacao.triton`, usa a mesma varredura de
Lisboa mas sorteia a incerteza da **captação** — área, coeficiente de escoamento e lâmina de
descarte — em conjunto com o fator da chuva, o fator das tarifas e o fator do investimento, em mil
realizações e semente 42. A Edição Ibérica não tem tabela por modelo climático, porque não tem
base de modelos climáticos: a incerteza da chuva entra pelo fator da chuva sobre a série E-OBS de
Lisboa, e a tabela da variância lista as variáveis sorteadas, entre elas o fator da chuva.

Leia este exemplo pelo que separa. Um coeficiente de escoamento ou uma área errados em alguns por
cento alteram todos os dias da série na mesma proporção, pelo que estas variáveis deslocam a
poupança aproximadamente ao ritmo do fator da chuva; um descarte mais profundo atua sobretudo nas
chuvas pequenas, que são os dias que enchem um reservatório vazio. A tabela de η² mostra a quais
delas a poupança e o valor atual líquido respondem de facto.

### 7.4.8. O que declarar

Num relatório ou num artigo, declare: as variáveis sorteadas e as suas distribuições (a primeira
tabela), o número de realizações e a semente, a gama P5–P95 e a mediana do resultado no volume
escolhido, a probabilidade de o investimento se pagar com o respetivo intervalo, a frequência com
que o volume escolhido vence e a parte da variância que cada fonte explica. O botão **Exportar**
grava tudo isto em JSON, e o CSV das amostras permite refazer qualquer estatística fora do
programa.

---

## 7.5. Método, estatística e limites

> **Pergunta a que esta secção responde:** como calcula a modulação, e até onde se pode confiar
> nela?

### 7.5.1. O procedimento

A modulação é uma simulação de Monte Carlo sobre a cadeia completa do programa. Para N realizações
com a semente s:

1. o programa executa o caso-base, com as premissas do estudo;
2. sorteia, de uma só vez, N valores de cada variável marcada, com o gerador pseudoaleatório
   iniciado pela semente;
3. para cada realização, copia o projeto, troca as premissas pelos valores sorteados e refaz a
   cadeia técnica, económica, ambiental e TOPSIS para **todos** os volumes da varredura;
4. reúne as N realizações em estatísticas por volume e no volume escolhido.

A comparação entre volumes é **emparelhada**: numa realização, todos os volumes enfrentam as mesmas
premissas sorteadas, e a diferença entre dois deles é efeito do volume, e não do sorteio. É o que
permite contar com que frequência cada volume vence. A grelha de volumes é a do estudo, e o
programa interrompe a análise se ela mudar entre realizações.

### 7.5.2. As estatísticas

Os percentis são empíricos, calculados sobre as realizações; o desvio-padrão é o amostral, e o
coeficiente de variação a razão entre ele e o módulo da média. As probabilidades vêm com o
intervalo de 95% de Wilson (1927). A sensibilidade é o ρ de Spearman (1904), com os empates no
posto médio. A parte da variância explicada é a razão de correlação η², a variância entre as
médias de classe dividida pela variância total; as classes são os decis da variável sorteada, ou
os seus próprios valores quando ela tem até dez valores distintos, como o número de pessoas. É o
estimador por classes do índice de primeira ordem (Saltelli et al., 2008), calculado com as mesmas
realizações, sem custo adicional.

A convergência acompanha-se pela média acumulada do valor atual líquido no volume escolhido e pelo
respetivo intervalo de 95%, cuja meia largura é igual a 1,96 vezes o desvio-padrão dividido pela
raiz quadrada do número de realizações. A faixa estreita-se com o inverso da raiz de N: quadruplicar
as realizações reduz para metade a incerteza do sorteio. Se a faixa ainda oscilar no fim da curva,
aumente N antes de publicar.

### 7.5.3. Limites

- **As variáveis são independentes.** O programa não impõe correlação entre elas. Em muitos
  projetos isso é razoável; quando duas premissas andam juntas — mais pessoas e mais procura
  exterior, por exemplo —, sortear de forma independente alarga a gama para além do real em
  algumas combinações e estreita-a noutras.
- **A incerteza é a declarada.** A gama de saída nunca é mais fiável do que as distribuições de
  entrada. Os valores de triagem são genéricos; ajuste-os com dados do edifício, de medição ou da
  literatura, e declare a fonte.
- **A chuva varia por fator.** O fator da chuva escala a série inteira e preserva a sua estrutura
  temporal — a sequência de dias secos e chuvosos. Uma alteração dessa estrutura, ou um cenário
  climático diferente, não é sorteada: compare-os executando a modulação uma vez para cada série.
  O efeito do comprimento da série tem estudo próprio (secção 2.2).
- **O que não está no catálogo fica fixo.** O preço de cada material em separado, os parâmetros da
  eletrobomba, a dose de cloro e as restantes premissas seguem o estudo. A análise de
  sensibilidade da secção 3.7 cobre as que faltam, uma de cada vez.
- **O η² por classes tem viés.** Com k classes e N realizações, sobrestima a parte explicada em
  cerca de (k − 1)/N — 0,009 com dez classes e mil realizações. Valores desta ordem não distinguem
  uma variável sem efeito.

A modulação probabilística dá a incerteza do resultado a partir da incerteza das premissas; não é
uma validação do modelo, que a secção 5.3 discute. Para uma introdução ao método e às suas
variantes — amostragem estratificada, índices de sensibilidade baseados na variância —, ver
Saltelli et al. (2008).

---

# Apêndices

---

## Apêndice A — Os parâmetros do projeto

São **118 parâmetros**. É a lista completa do que um projeto guarda nesta
edição, com o nome exato de cada campo dentro do ficheiro `.triton`.

A lista não foi transcrita à mão: é extraída do próprio programa a cada versão, e por
isso não pode divergir dele.

A coluna **onde se introduz** diz em que ecrã o campo aparece; a coluna **quem consome**
diz que cálculo o usa. Um campo sem nenhuma das duas é um campo gravado no ficheiro e
nunca lido, e está listado na secção 5.2.

Os padrões são os do projeto com que a Edição Ibérica abre: a chuva é a normal 1991-2020
do concelho de Lisboa na base E-OBS, e os custos, os preços e a tarifa de eletricidade
partem de zero ou vazios, para o utilizador os introduzir em euros. Um traço significa
que o campo não tem valor inicial.

O ficheiro de projeto guarda ainda 4 campos de esquemas nacionais de outras
edições. Não têm efeito nesta e não são listados.

### A.1. Identificação

3 parâmetros.

<!-- tabela: **Tabela 153** — Parâmetros do projeto: identificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | Novo projeto Triton | — | Exportação, Janela principal, Relatórios | Automação, CAD e BIM, Folhas de cálculo, Relatórios |
| `project_id` | — | — | Janela principal, Relatórios | Automação |
| `created_at` | — | — | Janela principal | — |

### A.2. Chuva

9 parâmetros.

<!-- tabela: **Tabela 154** — Parâmetros do projeto: chuva -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Janela principal, Projeto | Automação, Cenários, Folhas de cálculo |
| `climate_source_mode` | national_db | — | Janela principal, Projeto | — |
| `climate_city_uf` | Lisboa | — | Janela principal, Projeto, Relatórios | — |
| `climate_city_name` | Lisboa | — | Janela principal, Projeto, Relatórios | — |
| `climate_model` | E-OBS v33.0e | — | Janela principal, Projeto, Relatórios | — |
| `climate_scenario` | EOBS | — | Janela principal, Projeto, Relatórios | — |
| `climate_start_date` | 01/01/1991 | — | Janela principal, Projeto, Relatórios | — |
| `climate_end_date` | 31/12/2020 | — | Janela principal, Projeto, Relatórios | — |
| `start_date` | 01/01/1980 | — | Exportação, Janela principal, Projeto, Tarifário e custos | Automação, Clima, Folhas de cálculo |

Observações do código:

- `climate_source_mode`: "national_db" (a base E-OBS por concelho) ou "custom_file" (ficheiro do utilizador)

### A.3. Captação

7 parâmetros.

<!-- tabela: **Tabela 155** — Parâmetros do projeto: captação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | — | — | Ambiental, Documentação, Gráficos, Janela principal, Projeto, Qualidade, Relatórios | ACV, Automação, CAD e BIM, Cenários, ETAP, Folhas de cálculo, Relatórios |
| `discard_mode` | 1 | — | Janela principal, Projeto, Varrimento | Automação, Balanço diário, Cenários |
| `discard_days_interval` | 7 | — | Janela principal, Projeto, Varrimento | Automação, Balanço diário, Cenários |
| `area` | 100 | — | Ambiental, Documentação, Edificação, Gráficos, Janela principal, Qualidade, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Balanço diário, CAD e BIM, Cenários, ETAP, Folhas de cálculo, Relatórios |
| `irrigation_garden_area_m2` | 0 | — | — | — |
| `runoff_coeff` | — | — | Edificação, Janela principal, Qualidade, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `first_flush_system_enabled` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `discard`: mm
- `discard_mode`: 1 = todos os eventos, 2 = 1.º evento após período seco, 3 = a cada X dias
- `discard_days_interval`: intervalo para o modo 3
- `area`: m²
- `irrigation_garden_area_m2`: Área de jardim em m² para o assistente de dimensionamento
- `runoff_coeff`: ver hydrology_defaults

### A.4. Edificação

2 parâmetros.

<!-- tabela: **Tabela 156** — Parâmetros do projeto: edificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | — | Ambiental, Edificação | Automação, Económico |
| `building_template_id` | res_medio | — | Edificação | Automação, Tarifário |

Observações do código:

- `num_economias`: Número de frações autónomas com contador individual

### A.5. Procura

17 parâmetros.

<!-- tabela: **Tabela 157** — Parâmetros do projeto: procura -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `demand_type` | 0 | — | — | — |
| `demand_mode` | constant | — | Ambiental, Edificação, Janela principal, Relatórios, Varrimento | Automação, Balanço diário |
| `demand_value` | 200 | — | Documentação, Económico, Janela principal | Automação, Balanço diário |
| `demand_monthly` | — | — | Janela principal | Automação |
| `residents_type` | 0 | — | — | — |
| `residents_count` | 4 | — | Ambiental, Económico, Janela principal | Automação, Balanço diário, Eletrobomba |
| `residents_monthly` | — | — | Janela principal | Automação |
| `potable_indoor_share` | 0,6 | — | Edificação, Janela principal | Automação |
| `non_potable_indoor_share` | 0,4 | — | Edificação, Janela principal | Automação, Balanço diário |
| `rainwater_share` | 0,4 | — | Documentação, Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `weekly_demands` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `weekly_residents` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `weekly_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `monthly_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_demands` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_residents` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |

Observações do código:

- `demand_mode`: "constant", "weekly", "monthly", "daily"
- `demand_value`: L/dia, por residente ou total
- `potable_indoor_share`: Fração potável do consumo interior; 1 − non_potable_indoor_share
- `non_potable_indoor_share`: Fração não potável do consumo interior (autoclismos, máquina de lavar); ver fracao_atendivel
- `rainwater_share`: fração de 0 a 1 (0,4 = 40%)

### A.6. Rega

4 parâmetros.

<!-- tabela: **Tabela 158** — Parâmetros do projeto: rega -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `irrigation_liters_per_day` | 0 | — | Ambiental, Edificação, Janela principal, Relatórios | Automação, Balanço diário |
| `irrigation_rain_threshold_mm` | 2 | — | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_potable_backup` | sim | — | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_rate_l_m2_day` | 3 | — | — | — |

Observações do código:

- `irrigation_liters_per_day`: Procura exterior (rega, lavagem de zonas exteriores), L/dia
- `irrigation_rain_threshold_mm`: Limiar diário de precipitação para suspender a rega (mm/dia)
- `irrigation_potable_backup`: Se True, a rede pública abastece a rega em dias secos se a cisterna secar
- `irrigation_rate_l_m2_day`: Taxa diária de rega (L/m²/dia)

### A.7. Qualidade da água

9 parâmetros.

<!-- tabela: **Tabela 159** — Parâmetros do projeto: qualidade da água -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `water_quality_target_class` | classe_1 | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_disinfection` | cloro | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_polishing` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `etap_enabled` | sim | — | Ambiental, Económico, Otimizador | ACV, Automação, ETAP |
| `chlorine_treatment_enabled` | sim | — | Ambiental, Económico, Otimizador, Qualidade | ACV, Automação, Económico |
| `chlorine_dose_mg_l` | — | — | Ambiental, Económico, Otimizador, Qualidade | ACV, Automação, ETAP, Económico, Relatórios |
| `chlorine_product_purity` | — | — | Ambiental, Qualidade | ACV, Automação, ETAP, Económico |
| `chlorine_cost_per_kg` | 0 | — | Económico, Otimizador, Qualidade | Automação, ETAP, Económico, Preços |
| `chlorine_co2_kg_per_kg` | — | — | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `water_quality_disinfection`: "cloro", "uv", "ozonio" (ozono), "nenhum"
- `chlorine_dose_mg_l`: mg de Cl2 ativo por litro
- `chlorine_product_purity`: kg de Cl2 ativo por kg de produto
- `chlorine_cost_per_kg`: € por kg de PRODUTO comercial

### A.8. Reservatórios

12 parâmetros.

<!-- tabela: **Tabela 160** — Parâmetros do projeto: reservatórios -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | — | Ambiental, Assistente da bomba, Económico, Exportação, Janela principal, Otimizador, Relatórios, Reservatório superior, Tarifário e custos, Varrimento | Automação, Balanço diário, CAD e BIM, Cenários, Folhas de cálculo, Multicritério, Preços |
| `upper_tank_used` | 1 | — | Ambiental, Económico, Janela principal, Otimizador, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Balanço diário, Cenários, Eletrobomba, Folhas de cálculo, Preços |
| `lower_tank_max` | 10000 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `lower_tank_step` | 250 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `lower_tank_mode` | 1 | — | Janela principal, Varrimento | Automação |
| `lower_tank_fixed` | 2000 | — | Janela principal, Tarifário e custos, Varrimento | Automação |
| `delta_ideal` | 5 | — | Janela principal, Otimizador, Varrimento | Automação, Cenários |
| `econ_lower_tank_vol` | 2000 | — | Ambiental, Económico, Tarifário e custos, Varrimento | Automação |
| `lower_tank_material` | PEAD | — | Económico, Otimizador, Tarifário e custos | ACV, Automação, Preços |
| `upper_tank_material` | PEAD | — | Económico, Otimizador, Tarifário e custos | ACV, Automação, Preços |
| `cost_lower_tank` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico, Preços |
| `cost_upper_tank` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |

Observações do código:

- `upper_tank_vol`: L
- `upper_tank_used`: 0 = sem reservatório superior, 1 = com reservatório superior
- `lower_tank_max`: L
- `lower_tank_step`: L
- `lower_tank_mode`: 0 = volume fixo, 1 = varrimento
- `lower_tank_fixed`: usado no modo de volume fixo
- `delta_ideal`: limiar de ganho marginal para o volume ideal, em %/m³
- `lower_tank_material`: "PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)
- `upper_tank_material`: "PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)

### A.9. Eletrobomba

18 parâmetros.

<!-- tabela: **Tabela 161** — Parâmetros do projeto: eletrobomba -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pumping_threshold` | 50 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `supply_arrangement` | — | — | Ambiental, Económico, Varrimento | ACV, Automação, Económico, Eletrobomba |
| `pressurizer_pressure_m` | 18 | — | Varrimento | Eletrobomba |
| `pressurizer_starts_per_person_day` | 5,05 | — | Varrimento | Eletrobomba |
| `pressurizer_model` | — | — | Varrimento | Eletrobomba |
| `pressurizer_point_flow_l_min` | 9 | — | Varrimento | Eletrobomba |
| `pressurizer_power_kw` | 0,18 | — | Varrimento | Eletrobomba |
| `pressurizer_flow_l_min` | 13,3 | — | Varrimento | Eletrobomba |
| `pressurizer_post_run_s` | 0 | — | Varrimento | Eletrobomba |
| `pump_count` | 2 | — | Ambiental, Económico, Otimizador, Relatórios, Tarifário e custos | ACV, Automação, Económico, Preços, Relatórios |
| `pump_power_str` | 1/2 | — | Relatórios | — |
| `pump_power_kw` | 0,36775 | — | Económico, Gráficos, Otimizador, Relatórios, Tarifário e custos, Varrimento | Automação, CAD e BIM, Económico, Eletrobomba, Preços, Relatórios |
| `pump_manometric_head_m` | 0 | — | Varrimento | Automação, Eletrobomba |
| `pump_efficiency` | 0 | — | Gráficos, Tarifário e custos, Varrimento | Automação, Eletrobomba |
| `pump_flow_rate` | 0 | — | Económico, Gráficos, Otimizador, Relatórios, Tarifário e custos, Varrimento | Automação, Eletrobomba |
| `pump_startup_time_h` | 0,03 | — | Económico, Gráficos, Otimizador, Tarifário e custos | Automação, Eletrobomba |
| `pump_motor_efficiency` | 0 | — | Tarifário e custos | Automação, Eletrobomba |
| `pump_unit_cost` | 0 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico, Preços |

Observações do código:

- `pumping_threshold`: L, nível de acionamento da elevação
- `pump_count`: principal + reserva como configuração inicial recomendada
- `pump_power_kw`: kW (1 cv = 0,7355 kW; 1/2 cv = 0,36775 kW)
- `pump_efficiency`: %, 0 = deduzir da potência
- `pump_startup_time_h`: h
- `pump_motor_efficiency`: %
- `pump_unit_cost`: preço de uma eletrobomba, em euros (zero até o utilizador o introduzir)

### A.10. Tubagem

1 parâmetro.

<!-- tabela: **Tabela 162** — Parâmetros do projeto: tubagem -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Económico, Tarifário e custos | ACV, Automação |

### A.11. Investimento

3 parâmetros.

<!-- tabela: **Tabela 163** — Parâmetros do projeto: investimento -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_piping` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_accessories` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, ETAP, Económico |

### A.12. Exploração

1 parâmetro.

<!-- tabela: **Tabela 164** — Parâmetros do projeto: exploração -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |

### A.13. Tarifário

17 parâmetros.

<!-- tabela: **Tabela 165** — Parâmetros do projeto: tarifário -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | não | — | Projeto | — |
| `water_tariffs` | — | — | Projeto, Tarifário, Tarifário e custos, Varrimento | Económico |
| `tariff_city_uf` | personalizado | — | Janela principal, Projeto, Relatórios, Tarifário, Tarifário e custos | — |
| `tariff_city_name` | personalizado | — | Janela principal, Projeto, Relatórios, Tarifário, Tarifário e custos | — |
| `tariff_vigencia` | — | — | Projeto, Tarifário e custos | — |
| `tariff_category` | residencial | — | Económico, Tarifário, Tarifário e custos | Tarifário |
| `sewage_rate` | 100 | — | Projeto, Tarifário, Tarifário e custos | Automação, Económico, Tarifário |
| `sewage_mode` | 1 | — | Económico, Otimizador, Projeto, Tarifário, Tarifário e custos | Automação, Económico, Tarifário |
| `sewage_tariffs` | — | — | — | Económico, Tarifário |
| `sewage_volume_factor` | 1 | — | — | Automação, Económico, Tarifário |
| `water_tax_fixed` | 0 | — | Tarifário e custos | Automação, Económico |
| `water_tax_var` | 0 | — | Tarifário e custos | Automação, Económico |
| `tariff_escalation` | 12 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `water_tariff_escalation` | 5 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `sewage_tariff_escalation` | 5 | — | Económico, Otimizador, Tarifário e custos | Automação, Económico |
| `elec_tariff_escalation` | 5 | — | Económico, Otimizador, Varrimento | Automação, Económico |
| `elec_tariff` | 0 | — | Económico, Gráficos, Otimizador, Projeto, Relatórios, Tarifário e custos, Varrimento | Automação, Económico |

Observações do código:

- `tariff_category`: categoria da tabela tarifária aplicada; "personalizada" quando introduzida pelo utilizador
- `sewage_mode`: 0 = valor fixo em €, 1 = percentagem da parcela de água, 2 = €/m³ consumido, 3 = escalões
- `water_tax_fixed`: € por mês
- `water_tax_var`: % (o IVA da água, nas faturas portuguesas)
- `tariff_escalation`: meses; duração do período de atualização
- `water_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `sewage_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `elec_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `elec_tariff`: preço da eletricidade por kWh, em euros (zero até o utilizador o introduzir)

### A.14. Energia

4 parâmetros.

<!-- tabela: **Tabela 166** — Parâmetros do projeto: energia -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_city_name` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_tax_fixed` | 0 | — | Tarifário e custos | Automação, Económico |
| `elec_tax_var` | 0 | — | Tarifário e custos | Automação, Económico |

Observações do código:

- `elec_tax_fixed`: € por mês
- `elec_tax_var`: %

### A.15. Financeiro

4 parâmetros.

<!-- tabela: **Tabela 167** — Parâmetros do projeto: financeiro -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0,2 | — | Documentação, Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `analysis_period_years` | 20 | — | Económico, Otimizador, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Económico, Relatórios |
| `tma` | 2 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `install_month` | 0 | — | — | — |

Observações do código:

- `inflation`: % por mês; inflação dos custos de exploração e manutenção
- `analysis_period_years`: anos
- `tma`: % por mês; taxa de atualização

### A.16. Certificações

1 parâmetro.

<!-- tabela: **Tabela 168** — Parâmetros do projeto: certificações -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | — | Ambiental | — |

### A.17. Outros

6 parâmetros.

<!-- tabela: **Tabela 169** — Parâmetros do projeto: outros -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `phi_operation_rule` | — | — | Janela principal, Varrimento | Automação, Balanço diário, Folhas de cálculo |
| `data_base_estudo` | — | — | Tarifário e custos | — |
| `precos_de_catalogo` | não | — | Assistente da bomba, Económico, Otimizador, Qualidade, Tarifário e custos, Varrimento | Automação, ETAP, Preços |
| `bim_layout` | — | — | Exportação, Janela principal | — |
| `capex_do_arranjo` | não | — | Janela principal, Tarifário e custos, Varrimento | ETAP |
| `mao_de_obra_automatica` | não | — | Janela principal, Tarifário e custos, Varrimento | — |

---

## Apêndice B — Os processos do programa

São **24 processos**, do ficheiro de chuva ao relatório. Cada um declara o
que o desencadeia, o que recebe, as regras com as suas ramificações, o que produz e o
que acontece quando falha.

É o apêndice mais técnico do manual, e serve a duas pessoas: quem revê um estudo feito
com o programa e precisa de saber exatamente que conta foi feita, e quem encontrou um
resultado estranho e quer saber por onde o número passou.

Os nomes em `código` são os campos do ficheiro de projeto, listados no apêndice A.

### B.1. PROC-01 — Carregar a série de precipitação

*Chuva*

**Gatilho.** Separador Projeto: escolher o concelho na base E-OBS ou abrir um ficheiro CSV.

**Entradas**

- Concelho da base E-OBS v33.0e (278 concelhos com série, 1950 a 2025), ou ficheiro CSV diário em milímetros por dia
- `climate_start_date` e `climate_end_date`, que recortam a série (a normal 1991-2020 é o recorte inicial)
- `start_date`, data do primeiro dia da série

**Regras**

1. A série vira um vetor `numpy` de milímetros por dia; o índice do vetor é o dia, e a data serve só para saber o dia da semana e o mês.
2. A série de um concelho é a média diária das células da grelha E-OBS (0,1°) com centro dentro do concelho (limites da CAOP2025). Os Açores ficam fora do domínio da E-OBS e a Madeira não cumpre o limite de 1% de dias sem dado: 30 concelhos ficam sem série na base, e nenhum recebe a série de um vizinho. Para esses, a série é um ficheiro do utilizador.
3. Dia sem dado em todas as células é uma falha (NaN), e a simulação recusa a série em vez de o tratar como dia seco.
4. Ano incompleto é descartado na leitura, para não enviesar totais anuais.
5. A base vem no programa, em `data/portugal_eobs.db`; o exemplo do Funchal usa uma série ERA5 em `data/rainfall/Funchal.csv`.

**Saídas**

- `precip_data`: vetor de mm/dia, que é a entrada de **dois** processos distintos — PROC-04 (descarte e captação) e PROC-03 (suspensão da rega)

**Exceção.** Ficheiro ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; a simulação não corre com série vazia ou com falhas.

### B.2. PROC-02 — Compor a procura diária

*Procura*

**Gatilho.** Início da simulação, uma vez por execução.

**Entradas**

- `demand_mode`: constante, semanal, mensal ou diária
- `demand_value` (L/dia por pessoa), `residents_count`
- `rainwater_share` ou `non_potable_indoor_share`
- vetores `weekly_*`, `monthly_*`, `daily_*` quando o modo os usa

**Regras**

1. Procura-base do dia = `demand_value × residents_count`, com o multiplicador do dia da semana, do mês ou do dia, conforme o modo.
2. A fração não potável separa a procura em duas: interna potável e interna não potável.
3. Quando o modo é semanal, mensal ou diário, a fração vem do próprio vetor do período; fora disso, vale `non_potable_indoor_share`, e só então `rainwater_share`.
4. Valor nulo ou zero em qualquer posição do vetor cai para o valor constante.

**Saídas**

- `tot_arr`: procura total do dia
- `pot_in_arr`: potável interna, que a chuva nunca atende
- `non_pot_in_arr`: não potável interna, prioridade 1 da chuva
- `pluv_arr` = não potável interna + rega ativa

**Exceção.** Data inicial ilegível cai para 01/01/1980 em vez de interromper, porque só afeta o dia da semana.

### B.3. PROC-03 — Suprimir a rega nos dias de chuva

*Procura*

**Gatilho.** Composição da procura, um teste por dia da série.

**Entradas**

- `irrigation_liters_per_day`
- `irrigation_rain_threshold_mm` (padrão 2 mm/dia)
- `precip_data`, o **mesmo** vetor que alimenta a captação

**Regras**

1. Se a chuva do dia ≥ limiar, a rega do dia é **zero** e o dia entra na contagem de dias suprimidos.
2. Caso contrário, a rega do dia é o volume nominal.
3. É a segunda leitura do ficheiro de chuva, e independente da primeira: um dia pode suprimir a rega e ainda assim render captação.

**Saídas**

- `irr_arr`: rega do dia
- `irr_suppressed_mask`: dias suprimidos, que viram `total_irrigation_days_suppressed` no resultado

**Exceção.** Sem volume de rega registado, o vetor é zero e a máscara é falsa em todos os dias.

### B.4. PROC-04 — Descartar as primeiras águas

*Balanço hídrico*

**Gatilho.** Todo dia com chuva, dentro do ciclo diário.

**Entradas**

- `precip_mm` do dia
- `discard_mm`
- `discard_mode` (1, 2 ou 3)
- `discard_days_interval`

**Regras**

1. **Modo 1**: descarta em todo evento de chuva.
2. **Modo 2**: descarta apenas no primeiro evento após período seco, definida como véspera com menos de 1 mm.
3. **Modo 3**: descarta quando passaram `discard_days_interval` dias desde o último descarte.
4. Quando o descarte se aplica: `p_eff = p − discard_mm` se `p > discard_mm`, senão **zero**: toda a chuva do dia vai para o descarte.
5. Quando não se aplica: `p_eff = p`, a chuva inteira é aproveitável.

**Saídas**

- `p_eff`: lâmina efetiva do dia, em mm, que segue **só** para PROC-05
- `eff_precip_mm` na série diária detalhada, quando ela é guardada

**Exceção.** Lâmina de descarte negativa é rejeitada na barreira de validação, antes do ciclo.

### B.5. PROC-05 — Converter lâmina em volume captado

*Balanço hídrico*

**Gatilho.** Todo dia, depois do descarte.

**Entradas**

- `p_eff` de PROC-04
- `area` (m²)
- `runoff_coeff`

**Regras**

1. `v_ac = p_eff × area × runoff_coeff`, em litros.
2. É aqui que o ficheiro de chuva vira volume, e é o único ponto onde isso acontece.
3. O coeficiente é adimensional e fica em [0, 1]; fora disso a simulação nem começa.

**Saídas**

- `v_ac`: volume captado do dia, que segue para PROC-06
- `harvested_liters` na série diária

**Exceção.** Área negativa ou coeficiente fora de [0, 1] levantam `ValueError` nomeando o campo, em PROC-11.

### B.6. PROC-06 — Armazenar e extravasar

*Balanço hídrico*

**Gatilho.** Todo dia, depois da captação.

**Entradas**

- `v_ac`
- volume remanescente do dia anterior
- `lower_tank_vol`

**Regras**

1. **Extravasamento antes do consumo**, como na regra YAS; a chuva do dia, até a capacidade, já atende a procura do dia, o que põe o modelo entre a YAS e a YBS estritas.
2. `disponível = v_lower + v_ac`. Se passar da capacidade, o excedente extravasa e o reservatório fica cheio.
3. A ordem importa: retirar a procura antes faria o reservatório aceitar água que fisicamente já teria extravasado, sobrestimando o aproveitamento.

**Saídas**

- `v_spill_today`, somado em `avg_spilled_l_day`, que vira critério de extravasamento no multicritério
- `v_in_tank`, o volume disponível para atendimento

**Exceção.** Volume zero é válido e representa o cenário sem sistema; negativo é rejeitado.

### B.7. PROC-07 — Atender com reservatório único

*Balanço hídrico*

**Gatilho.** Todo dia, quando não há reservatório superior.

**Entradas**

- `v_in_tank`
- `pluvial_demand_per_day` de PROC-02

**Regras**

1. `v_c = min(procura pluvial, volume no reservatório)`.
2. O volume remanescente permanece para o dia seguinte: `v_lower = v_in_tank − v_c`.

**Saídas**

- `v_c`: volume pluvial consumido no dia

**Exceção.** Nenhuma: o mínimo já trata reservatório vazio e procura nula.

### B.8. PROC-08 — Atender com elevação para reservatório superior

*Balanço hídrico*

**Gatilho.** Todo dia, quando `upper_tank_used` e o volume superior é positivo.

**Entradas**

- `v_lower`, `v_upper`
- `upper_tank_vol`
- `pumping_threshold`, o volume de reserva que não se consome

**Regras**

1. Laço até a procura ser atendida ou a água acabar.
2. Primeiro consome do reservatório superior o que estiver **acima** do limiar de acionamento.
3. Se ainda falta e há água em baixo, aciona a bomba: transfere `min(v_lower, espaço livre em cima)`, conta **um ciclo** e regista a lote.
4. Depois do elevação, consome de novo.
5. O limiar é limitado ao volume do reservatório superior na entrada do processo.

**Saídas**

- `v_c`
- `v_rec_today`, somado em `total_pumped_liters`
- `cycles_today`, somado em `total_pump_cycles`
- `max_pump_batch_liters`

**Exceção.** Volume superior negativo é rejeitado na validação. O ciclo tem saída garantida: se não há água em baixo nem em cima, interrompe.

### B.9. PROC-09 — Repartir o atendimento e completar com potável

*Balanço hídrico*

**Gatilho.** Todo dia, depois do atendimento.

**Entradas**

- `v_c`
- `non_pot_in_day`
- `irr_day`
- `pot_in_day`
- `irrigation_potable_backup`

**Regras**

1. **Prioridade 1**, uso interno não potável: `c_pluv_in = min(v_c, não potável interna)`.
2. **Prioridade 2**, rega: `c_pluv_irr = min(v_c − c_pluv_in, rega do dia)`.
3. O potável consumido é a soma de três parcelas: o potável interno, o déficit do não potável interno e — só se o suprimento de reserva estiver ligado — o déficit da rega.
4. Com o suprimento de reserva desligado, o jardim simplesmente não é regado no dia seco, e a rede não é acionada.

**Saídas**

- `potable_consumed_liters` do dia
- `avg_pluvial_indoor_consumed_l_day` e `avg_pluvial_irrigation_consumed_l_day`, que separam o uso interno do externo para os créditos WEc1 e WEc2 do LEED v4 e as Opções 2 e 4 do WEc2 do LEED v5

**Exceção.** Nenhuma: todas as parcelas são mínimos e máximos com zero.

### B.10. PROC-10 — Classificar o atendimento do dia

*Balanço hídrico*

**Gatilho.** Todo dia, ao fim do atendimento.

**Entradas**

- `v_c`
- `pluvial_demand_per_day`

**Regras**

1. **Pleno** quando o consumido iguala a procura pluvial, com tolerância de 10⁻⁵ L.
2. **Parcial** quando consumiu algo, mas menos que a procura.
3. **Nulo** quando não consumiu nada.

**Saídas**

- `pct_days_full_satisfaction`, `pct_days_partial_satisfaction` e `pct_days_null_satisfaction`, que são a confiabilidade temporal do sistema

**Exceção.** Nenhuma.

### B.11. PROC-11 — Validar a entrada física

*Balanço hídrico*

**Gatilho.** Primeira linha de `run_single_simulation`, antes de qualquer conta.

**Entradas**

- volume inferior e superior
- área
- coeficiente de escoamento
- lâmina de descarte
- procura diária
- fração pluvial

**Regras**

1. Volume negativo, área negativa, descarte negativo e procura negativa são recusados.
2. Coeficiente de escoamento e fração pluvial têm de ficar em [0, 1].
3. **Volume zero continua válido**: é a referência «sem sistema» da varrimento.
4. A mensagem nomeia o campo e o valor recebido, em vez de corrigir por baixo dos panos.

**Saídas**

- Nenhuma saída: ou passa, ou levanta `ValueError`

**Exceção.** É o próprio tratamento. Antes desta porta, volume de −1.000 L devolvia −166,67% de economia, e o número seguia para o económico, para a ACV e para o relatório.

### B.12. PROC-12 — Agregar o período e calcular os indicadores

*Balanço hídrico*

**Gatilho.** Fim do ciclo diário.

**Entradas**

- acumuladores do ciclo
- `n_days`

**Regras**

1. **Potencial de economia** = pluvial consumido no período ÷ procura total do período × 100.
2. As médias diárias dividem os acumulados pelo número de dias simulados.
3. As conversões para o ano usam **365,25** dias, e não 365, para absorver os bissextos da série.
4. O potencial fica sempre em [0, 100] — invariante que a barreira de validação existe para garantir.

**Saídas**

- `SingleTankSimulationResult`, com 21 campos, que é o objeto que **todos** os módulos a jusante consomem

**Exceção.** Procura total nula devolve potencial zero em vez de dividir por zero.

### B.13. PROC-13 — Varrer volumes e achar o volume ideal

*Balanço hídrico*

**Gatilho.** Separador Varrimento: botão de simular.

**Entradas**

- `lower_tank_max`
- `lower_tank_step`
- `delta_ideal` (%/m³)

**Regras**

1. A grade discreta arredonda o passo **para cima** até o múltiplo de 250 L, que é o quantum comercial de reservatório, e limita a 40 volumes positivos.
2. O volume máximo informado é sempre preservado como último ponto, de modo que só o último intervalo pode ser menor que o passo.
3. Zero entra na grade como alternativa de referência.
4. Roda PROC-04 a PROC-12 uma vez por volume.
5. O **volume ideal** é o primeiro cujo ganho marginal `Δpotencial/Δm³` cai abaixo do limiar: a partir dali, mais reservatório não compensa.

**Saídas**

- `SweepSimulationResult`: um resultado por volume, o volume ideal, e o registo de que o passo foi ajustado
- A lista de volumes é a lista de **candidatos** do multicritério

**Exceção.** Passo maior que o máximo devolve grade com um ponto. O ajuste do passo é registado em `step_adjusted`, e não silenciado.

### B.14. PROC-14 — Calcular os índices pluviométricos

*Chuva*

**Gatilho.** Separador Gráficos e relatório científico.

**Entradas**

- `precip_data`
- datas da série

**Regras**

1. Nove índices: PRCPTOT, R95p, RX1day, RX5day, SDII, R20mm, CDD, CWD e o índice de sazonalidade de Walsh e Lawler.
2. O conjunto **não** é ETCCDI puro: a sazonalidade não é do conjunto, e o R10mm, que é, está ausente.
3. O percentil 95 é calculado sobre a **série inteira carregada**, e não sobre a base fixa 1961–1990 do ETCCDI.
4. O RX5day usa `min_periods=1`, de modo que as primeiras janelas do ano têm de 1 a 4 dias.

**Saídas**

- Nove séries anuais, para gráfico e relatório

**Exceção.** Série menor que um ano devolve os índices possíveis, sem interromper.

### B.15. PROC-15 — Dimensionar a estação de tratamento

*Qualidade e ETAP*

**Gatilho.** Mudança na separador Qualidade da Água, ou início do económico e da ACV.

**Entradas**

- `water_quality_target_class` (4 classes de uso)
- `water_quality_disinfection`: cloro, ultravioleta ou ozono
- `water_quality_polishing`, filtro de polimento
- `annual_pluvial_m3` de PROC-12
- `area`
- dose, pureza, preço e fator de CO₂ do cloro
- `discard` e `first_flush_system_enabled`, para o descarte inicial

**Regras**

1. A classe alvo define as etapas obrigatórias; a desinfeção escolhida define o equipamento e o exploração.
2. O filtro de polimento é aplicado **se e somente se** marcado; quando a classe o recomendaria e o utilizador recusa, isso fica registado em `polishing_recommended_but_declined` em vez de ser imposto.
3. O que se compra é o **produto** — pastilha a 65% de cloro ativo — e não o cloro puro. Faturar a massa de cloro ativo, e não a do produto, subestima o custo em cerca de 35%.
4. **Regra incremental**: o CAPEX da linha desconta a verba genérica de tratamento já embutida em «Acessórios», e os custos de exploração descontam a cloragem, que o fluxo de caixa já paga. A regra vive num lugar só, consumida pelos **dois** motores económicos.
5. Com `first_flush_system_enabled`, o dispositivo de descarte inicial, de volume `discard × area`, entra no CAPEX e no exploração da linha.
6. Na ACV, a linha de tratamento **substitui** o termo de cloragem; nunca soma a ele.
7. Com `etap_enabled = False`, a linha de tratamento não entra em conta alguma: nem no CAPEX, nem no exploração, nem na avaliação ambiental.

**Saídas**

- `total_etap_capex`, que entra no CAPEX
- `total_etap_annual_opex`, que entra no exploração
- `total_etap_co2e_kg_yr`, que substitui a cloragem na ACV
- `disinfection_stages`, exibido no relatório

**Exceção.** Pureza fora de (0, 1] é recusada pelo validador da cadeia de cloragem.

### B.16. PROC-16 — Calcular a energia de bombeamento

*Eletrobomba*

**Gatilho.** Económico e ACV, a partir do mesmo resultado de simulação.

**Entradas**

- `supply_arrangement`: elevação, pressurização direta ou gravidade
- `total_pumped_liters` e `total_pump_cycles` de PROC-08
- `pressurizer_pressure_m`, `pressurizer_starts_per_person_day`, `residents_count`
- `pump_power_kw`, `pump_efficiency`, `pump_flow_rate`
- `pump_manometric_head_m`
- `pump_startup_time_h`

**Regras**

1. O arranjo decide o que se bombeia. **Elevação**: o volume enviado ao reservatório superior. **Pressurização direta**: todo o volume pluvial consumido, com a pressão de trabalho no lugar da altura e sem energia de partida. **Gravidade**: nada. É a única fonte de kWh do económico e da ACV.
2. Energia específica `e = ρgH/(η_bomba·η_motor)` por m³ elevado, ou `P/(Q·η_motor)` quando a caudal é declarada.
3. A potência de placa é potência de eixo e **já embute** o rendimento da bomba; por isso `P × horas / η_bomba` conta esse rendimento duas vezes, e o que falta é dividir pelo rendimento do motor. Quatro cópias dessa fórmula antiga sobreviviam no programa e sobrestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no multicritério.
4. A energia de partida entra à parte, pelo número de ciclos.
5. Caudal e rendimento não informados caem para valores típicos **da potência escolhida**, e não para constantes fixas.

**Saídas**

- `annual_kwh`, que vira custo no económico e emissão na ACV
- `pump_hours_year`, `annual_cycles`

**Exceção.** Arranjo por gravidade, arranjo não informado num projeto antigo, ou potência zero: a energia é zero.

### B.17. PROC-17 — Calcular a fatura de água, saneamento e resíduos

*Económico*

**Gatilho.** Duas vezes por mês de projeção: com e sem aproveitamento.

**Entradas**

- volume mensal em litros
- `water_tariffs`: quádruplas (mínimo, máximo, valor, código)
- `sewage_mode` e `sewage_rate`
- taxas fixa e variável (nelas entram o IVA e as parcelas fixas)
- `num_economias`, o número de frações autónomas com contador individual

**Regras**

1. O consumo é avaliado **no patamar de uma fração** e multiplicado pelo número de frações, para não distorcer os escalões progressivos em prédio com contadores individuais.
2. Código **1** ou **0**: escalão progressivo, cobrado só sobre o volume dentro dele.
3. Código **−1**, tarifa de disponibilidade: valor fixo que **soma** ao consumo medido.
4. Código **−2**, franquia retroativa: até ao volume da franquia paga-se o valor fixo; passando-o, **todo** o volume desde zero é tarifado pelos escalões.
5. Código **−3**, piso de pagamento: não soma, **limita por baixo**. Com piso de 40 € e consumo tarifado de 55 €, poupar até 15 € não reduz nada — e é exatamente isso que um estudo de aproveitamento pluvial precisa de ver.
6. A fatura portuguesa soma a água (tarifa fixa mensal e escalões por m³), o saneamento, os resíduos urbanos, a taxa de recursos hídricos (TRH) e o IVA de cada parcela, à taxa que o tarifário declara. Nenhuma taxa de IVA fica no código.
7. O saneamento pode ser cobrado por escalões próprios sobre o volume recolhido (coeficiente de recolha × volume de água; em Lisboa, 90%), com a TRH por m³ recolhido, ou como percentagem da **parcela de água**, e não da fatura total.
8. As tarifas fixas das parcelas que não são a água entram como taxa fixa mensal. Não variam com o consumo e anulam-se na poupança; entram para a conta mensal sair igual à impressa.
9. Os seis regimes tarifários são descritos no apêndice D; os tarifários transcritos (Lisboa, Porto e Funchal) estão nesse mesmo apêndice.

**Saídas**

- Valor da fatura de água, saneamento e resíduos em €/mês, para a projeção de PROC-18

**Exceção.** Tabela vazia dá fatura zero: o programa não presume tarifário. Estrutura incompleta é sinalizada pela barreira de validação, que separa erro de aviso. Os resíduos por escalões (Funchal) ainda não têm campo próprio: a parte variável soma-se à do saneamento.

### B.18. PROC-18 — Projetar o fluxo de caixa

*Económico*

**Gatilho.** Separador Económico, após a simulação técnica.

**Entradas**

- CAPEX das cinco rubricas mais bomba e ETAP
- poupança mensal de água e saneamento de PROC-17
- custos de exploração: bombagem, cloragem, ETAP e custos operacionais declarados
- `tma` (taxa de atualização), `inflation`, `analysis_period_years`
- atualizações separadas de água, saneamento e energia, e o intervalo entre atualizações

**Regras**

1. Água e saneamento são atualizados por índices **separados**, e não pela fatura agregada.
2. A inflação incide só sobre os custos de exploração; as atualizações tarifárias incidem só sobre a fatura.
3. A atualização é aplicada a cada `tariff_escalation` meses, em degraus.
4. O período de recuperação é o primeiro mês em que o acumulado descontado cruza zero.

**Saídas**

- `vpl` (VAL), `tir_monthly_pct`, `tir_annual_pct`, `payback_months`
- `monthly_cash_flows`, série mês a mês
- `annual_pump_kwh`, `annual_chlorine_kg`

**Exceção.** Poupança mensal negativa é truncada em zero antes de entrar no fluxo. TIR sem raiz real devolve nulo em vez de um número inventado.

### B.19. PROC-19 — Avaliar o ciclo de vida

*ACV*

**Gatilho.** Separador Ambiental, após a simulação técnica.

**Entradas**

- `tank_vol_liters`
- `annual_pluvial_m3` de PROC-12
- materiais e massas dos dois reservatórios
- comprimentos por diâmetro de tubo
- `pump_count`
- fator da rede elétrica
- fator de emissão da água potável entregue
- resultado da ETAP de PROC-15

**Regras**

1. Sete etapas: cisterna inferior, reservatório superior, tubagem, eletrobomba, operação de bombeamento, operação de tratamento e potável evitada.
2. Volume zero **sem** volume pluvial é o cenário sem sistema, e não recebe impacto fixo de caixa, tubo ou bomba.
3. A linha de tratamento **substitui** o termo de cloragem; não soma a ele. A cloragem acompanha o tratamento, e não o reservatório superior.
4. Reservatório superior só no arranjo de elevação; eletrobombas em todo arranjo com bomba; energia de PROC-16.
5. A água evitada é a **entregue**, não a produzida: as perdas de distribuição fazem com que produzir 1 m³ entregue menos de 1 m³, e um fator dado à saída da estação tem de ser convertido para o volume entregue. O utilizador indica o fator de emissão da água entregue ao edifício e o da rede elétrica local; a edição não traz valor predefinido para nenhum dos dois.
6. O período de retorno do carbono é o carbono incorporado dividido pela economia anual líquida; sem economia líquida positiva, devolve 999 anos em vez de infinito.

**Saídas**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, que é critério do multicritério
- `environmental_payback_years`
- `inventory_items`, o inventário item a item

**Exceção.** Fator sem procedência primária recebe rótulo de triagem, e o rótulo é exibido — a lacuna é declarada, não escondida.

### B.20. PROC-20 — Enquadrar nas certificações

*ESG e certificações*

**Gatilho.** Separador Ambiental e relatórios.

**Entradas**

- `potential_potable_savings_pct`
- volume pluvial e potável anuais
- repartição interno/externo de PROC-09
- CO₂ evitado no ciclo de vida
- `area`, para a área de captação da WEM14
- caso-base do EDGE, quando declarado

**Regras**

1. **LEED v4**: WEc1 até 2 pontos pelo uso externo, WEc2 até 6 pontos pelo uso interno, pela escala oficial. Sem procura externa registada, WEc1 é zero e diz porquê.
2. **LEED v5 BD+C** (rating system de novembro de 2025): WEc2 até 8 pontos, pela Opção 1 (projeto inteiro, 30% a 65%, +1 com fonte alternativa) ou pela soma das Opções 2 (louças e metais, 30% a 40%), 4 (externo, 50% e 100%) e 6 (reutilização no lote, 2 pontos), só em construção nova. SSc3 registado como não avaliado; o ponto de reutilização dele não ultrapassa o teto de 3.
3. **EDGE**: **não pontua**. Mede percentual contra um caso-base local e compara com 20%, em três barras independentes. O nível avançado sobe a barra de *energia* para 40%, e não a de água. O programa avalia só a barra de água, pela medida WEM14, e diz que as outras duas estão fora do seu alcance.
4. Sem caso-base declarado, o EDGE usa a procura modelada e avisa que o número é **piso**.
5. **GRI 303**: captação evitada e taxa de circularidade.

**Saídas**

- `credit_details`: a matriz de créditos que alimenta a tabela do ecrã e os relatórios
- `esg_summary_text`
- cartões de LEED, EDGE e GRI

**Exceção.** Procura total nula devolve zero por cento sem dividir por zero.

### B.21. PROC-21 — Ordenar volumes por múltiplos critérios

*Multicritério*

**Gatilho.** Separador Otimizador, com a varrimento pronta.

**Entradas**

- um candidato por volume da varrimento, cada um com potencial, extravasamento, VAL, período de recuperação descontado, TIR, CO₂ de ciclo de vida e consumo de potável
- pesos dos sete critérios

**Regras**

1. Sete critérios: **maximizar** potencial, VAL e TIR; **minimizar** extravasamento, período de recuperação, CO₂ e consumo de potável.
2. A normalização translada por `x − min(x)` **antes** da normalização vetorial de Hwang e Yoon, para admitir VAL negativo. É variante deliberada, e precisa ser declarada como variante.
3. O SMAA-VIKOR sorteia pesos e devolve as probabilidades de cada volume ocupar cada posição.
4. As condições C1 e C2 de Opricovic não estão implementadas.

**Saídas**

- Ordenação dos volumes, distância ao ideal por critério, volume de compromisso

**Exceção.** Candidato único devolve ordenação trivial. Critério constante entre candidatos não contribui para a distância.

### B.22. PROC-22 — Gravar e reabrir o projeto

*Ficheiro do projeto*

**Gatilho.** Menu de guardar e de abrir.

**Entradas**

- `TritonConfig` inteiro, com os campos do apêndice A
- estado da interface
- análise corrente

**Regras**

1. Formato JSON, em secções nomeadas.
2. A leitura usa valor por defeito campo a campo, de modo que ficheiro antigo continua abrindo.
3. `created_at` e `precip_file` descrevem o ato de guardar, e não o projeto: por isso não voltam.
4. É a quinta travessia do programa — a que atravessa o **tempo** em vez dos módulos. Trinta dos 87 campos de então não sobreviviam ao ciclo, inclusive a escolha inteira da ETAP, a altura manométrica, os materiais dos reservatórios, a rega e a água de rega.

**Saídas**

- Ficheiro `.triton`
- `TritonConfig` reconstruída

**Exceção.** Secção ausente no ficheiro cai para os valores por defeito da classe. JSON inválido interrompe a abertura com mensagem.

### B.23. PROC-23 — Emitir relatórios e exportações

*Relatórios*

**Gatilho.** Separador Relatórios; separador Exportação.

**Entradas**

- resultados de PROC-12, PROC-18, PROC-19, PROC-20 e PROC-21
- dados do projeto

**Regras**

1. Três relatórios: executivo, ambiental com ESG, e científico.
2. Exportação para CAD e BIM a partir do dimensionamento.
3. Folhas de cálculo com a série diária e a varrimento.

**Saídas**

- HTML, PDF, DXF, JSON para BIM e XLSX

**Exceção.** A conversão para PDF tenta o motor do Qt e cai para o gerador alternativo quando ele não está disponível.

### B.24. PROC-24 — Automação para estudos de larga escala

*Automação*

**Gatilho.** Linha de comandos `triton`, descrita na secção 3.6; acompanha a instalação como pacote Python, e não o instalador de Windows.

**Entradas**

- ficheiro de projeto
- ficheiro de chuva

**Regras**

1. Chama o **mesmo** núcleo de cálculo da janela, sem ecrã.
2. Só parte dos parâmetros é alcançável por ela; os demais só existem na interface, e o caminho é montar o projeto na janela e variar por automação só o que muda entre os casos.
3. Serve a matrizes fatoriais de milhares de casos e à propagação de incerteza por sorteio, que são o instrumental dos trabalhos publicados pelo grupo.

**Saídas**

- JSON e CSV com os resultados

**Exceção.** Parâmetro fora do intervalo admitido é recusado antes de simular, com a mesma barreira de validação da interface.

---

## Apêndice C — Fatores de emissão

Todos os fatores que a avaliação de ciclo de vida usa, com a procedência, a fronteira e o grau
de confiança. A avaliação é de **triagem**, e não um inventário conforme a ISO 14040 (apêndice G).

A Edição Ibérica separa os fatores em dois tipos.

- **A indicar pelo utilizador.** O fator da rede elétrica e o fator da água potável entregue ao
  edifício dependem do local e do ano do projeto. A edição não traz valor predefinido para nenhum
  deles: os campos partem de zero, e a avaliação de ciclo de vida só tem sentido depois de os
  introduzir. O utilizador obtém-nos junto de uma fonte do local do projeto, e declara a fonte, o ano
  e a fronteira. Esta edição do manual não fixa nenhuma fonte nacional: uma série oficial portuguesa só
  entrará aqui depois de verificada (ver as pendências).
- **Fatores de triagem do programa.** Os fatores dos materiais dos reservatórios, das tubagens, da
  eletrobomba e dos consumíveis de tratamento são valores de partida, editáveis no ecrã. Cada um vem
  listado abaixo com a referência que o código-fonte regista. Essas referências não foram reverificadas
  para esta edição do manual (pendente, ver abaixo): trate cada valor como hipótese de triagem e
  substitua-o por uma Declaração Ambiental de Produto (EPD) do produto que especificar, sempre que
  existir.

---

### C.1. Fatores a indicar pelo utilizador

<!-- tabela: **Tabela 170** — Fatores de emissão que o utilizador indica, e o que declarar em cada um -->
| Fator | Unidade | Padrão | O que declarar |
| :--- | :--- | :--- | :--- |
| rede elétrica | kg CO₂e/kWh | nenhum (zero) | fonte, **ano**, se é CO₂ ou CO₂e, e se cobre só a produção ou também perdas e combustíveis a montante |
| água potável de rede entregue ao edifício | kg CO₂e/m³ | nenhum (zero) | fonte, fronteira, e se o valor é por m³ **entregue** ou por m³ produzido |
| material do reservatório, quando substitui o predefinido | kg CO₂e/kg e kg/m³ | ver abaixo | fonte, versão, fronteira do sistema de produto |

**A fronteira é por metro cúbico entregue ao edifício**, e não por metro cúbico produzido na estação.
Um fator dado à saída da estação tem de ser dividido pela fração do volume produzido que chega ao
edifício (um menos as perdas na distribuição da entidade gestora), ou a emissão evitada fica
subestimada.

**O fator da rede muda todos os anos**, e um estudo sem o ano declarado é irreprodutível. Um fator só
de CO₂ e um fator de CO₂ equivalente são grandezas diferentes: a avaliação de ciclo de vida precisa do
segundo.

---

### C.2. Materiais dos reservatórios

<!-- tabela: **Tabela 171** — Fatores de emissão dos materiais dos reservatórios, com massa e fronteira -->
| Material | Massa por m³ útil | Fator | Fronteira |
| :--- | ---: | ---: | :--- |
| polietileno de alta densidade | 22 kg/m³ | 1,612 kg CO₂e/kg | berço ao portão |
| betão armado | 1 200 kg/m³ | 0,140 kg CO₂e/kg | berço ao portão |
| fibra de vidro | 15 kg/m³ | 3,250 kg CO₂e/kg | berço ao portão |
| aço inoxidável AISI 304 | 38 kg/m³ | 3,700 kg CO₂e/kg | berço ao portão |

A massa por metro cúbico útil é o que converte o volume do reservatório em massa de material. É ela, e
não o fator, que faz o betão dominar o inventário: 1 200 kg por metro cúbico contra 22 do polietileno.
As massas são cenários geométricos do programa, e não o peso de um produto.

<!-- tabela: **Tabela 172** — Referência registada no programa para cada fator de material, e a sua situação -->
| Material | Referência registada no programa | Situação |
| :--- | :--- | :--- |
| polietileno | Franklin Associates para o American Chemistry Council (outubro de 2020), *Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin*, Tabela 6: 1 612 kg CO₂e por 1 000 kg de resina (TRACI 2.1, IPCC 2013 GWP-100, âmbito dos Estados Unidos) | registada; reverificação pendente |
| betão | valor de triagem de 0,14 kg CO₂e/kg; Hammond e Jones (2008, doi:10.1680/ener.2008.161.2.87) publicam um valor para o betão, mas o valor exato adotado não está rastreado até ele | triagem, sem fonte rastreada |
| fibra de vidro | Composites UK, *Embodied carbon data for composites*: intervalo típico de 2,5 a 4,0 kg CO₂e/kg; adota-se o ponto médio | registada; reverificação pendente |
| aço inoxidável | worldstainless (World Steel Association), relatório de emissões de CO₂ de 24/09/2024, berço ao portão: 1,95 kg CO₂/kg com 85% de sucata, 2,45 com 75%, 3,70 com 50%, 6,80 com 30%; adota-se o caso de 50% de sucata | registada; reverificação pendente |

> **Consequência prática, demonstrada na secção 4.8:** o material pode decidir o **sinal** do
> resultado ambiental. Com a chuva de Lisboa e os fatores ilustrativos do tutorial, nenhum dos quatro
> materiais paga a dívida de carbono em vinte anos; a secção conta o resultado tal como saiu.

---

### C.3. Tubagens e eletrobomba

A tubagem de PVC toma-se a 2,36 kg CO₂e por quilograma de tubo instalado, módulos A1 a A3 de uma
Declaração Ambiental de Produto (EPD Australasia S-P-05503, 25/11/2022, EN 15804+A2), multiplicado pela
massa linear do tubo para o seu diâmetro nominal. As massas lineares são valores de triagem: substitua-as
pela ficha técnica do tubo que especificar.

A eletrobomba toma-se a uma intensidade de 4,77 kg CO₂e por quilograma de bomba, da EPD da Grundfos
EPD-GRU-20250340-CBA1-EN (2025, módulos A1 a A3), aplicada à massa da bomba. Indique a massa da bomba que
especificar; havendo EPD do fabricante, é ela que prevalece.

> **Declare no estudo.** A EPD é de um circulador europeu com eletrónica integrada, e a sua massa de
> referência inclui a embalagem. A intensidade por quilograma é uma aproximação de ordem de grandeza, e
> não o inventário da bomba instalada.

Situação das duas referências: registadas no programa, reverificação pendente.

---

### C.4. Consumíveis de tratamento

<!-- tabela: **Tabela 173** — Fatores de emissão dos consumíveis de tratamento -->
| Consumível | Fator |
| :--- | ---: |
| pastilha de hipoclorito de cálcio a 65% | 1,72 kg CO₂e/kg de produto |
| lâmpada ultravioleta | energia da rede |
| gerador de ozono | energia da rede |

A massa é de **produto**, e não de cloro ativo. As pastilhas têm cerca de 65% de cloro ativo.

O fator do hipoclorito é uma aproximação tirada de uma base comercial (ecoinvent 3.8, *cutoff*, hipoclorito
de sódio em solução a 15%, geografia resto do mundo, EF 3.1 *Climate change*: 2,522 kg CO₂e por kg de NaOCl,
convertido para base de cloro ativo e para uma pastilha a 65%). Não há processo de hipoclorito de cálcio, e a
base não é aberta: o fator é um valor de **triagem**. Se dispuser de um fator aberto para o produto que usa,
introduza-o no campo `chlorine_co2_kg_per_kg`.

---

### C.5. Fatores com rótulo de triagem

Nem todo o parâmetro tem fonte primária, e os que não a têm são assinalados no relatório: as massas por
metro cúbico útil do polietileno, do betão e do aço inoxidável, que são cenários geométricos, o fator do
betão, o fator do hipoclorito e qualquer fator introduzido sem fonte. Os fatores que o utilizador introduz
sem fonte recebem também o rótulo de triagem. Um inventário que apresenta todos os fatores com o mesmo grau
de confiança esconde onde está a fragilidade.

---

### C.6. O que consultar antes de publicar

1. a EPD ou a ficha técnica de cada produto que especificar;
2. o separador Documentação, capítulo de avaliação de ciclo de vida, para as justificações mostradas ao utilizador;
3. o inventário do relatório ambiental, que lista cada item com o fator aplicado.

---

## Apêndice D — Regimes tarifários

A Edição Ibérica traz o tarifário doméstico de **3 concelhos**, transcrito
dos documentos das entidades gestoras: Funchal, Lisboa, Porto. Para qualquer
outro concelho, o utilizador introduz o tarifário do projeto, na janela de tarifário (etapa 5),
e o programa calcula a fatura com e sem o sistema. Este apêndice descreve a estrutura que o
programa aceita, os seis regimes que reconhece e os tarifários transcritos.

### D.1. Os códigos de escalão

Cada linha da tabela de água é uma quádrupla `(mínimo, máximo, valor, código)`, em m³ por mês
e euros por m³ (ou euros por mês nos códigos fixos).

<!-- tabela: **Tabela 174** — Os códigos da tabela tarifária de água -->
| Código | Significado |
| ---: | :--- |
| 1 ou 0 | escalão progressivo: cobrado só sobre o volume dentro dele |
| −1 | tarifa de disponibilidade: valor fixo por mês que se soma ao consumo medido |
| −2 | franquia retroativa: até à franquia paga-se o valor fixo; depois, todo o volume desde zero é cobrado pelos escalões |
| −3 | piso de pagamento: a fatura não pode ficar abaixo do valor |

O efeito de cada código na fatura está desenhado na secção 2.7, e não se repete aqui.

### D.2. A fatura portuguesa

Uma fatura doméstica soma, por mês, a água (tarifa fixa e escalões por m³), o saneamento de
águas residuais, os resíduos urbanos, a taxa de recursos hídricos (TRH, por m³) e o IVA de
cada parcela, **à taxa que o próprio tarifário declara**. Nenhuma taxa de IVA fica no código.
O programa trata cada parcela assim:

<!-- tabela: **Tabela 175** — Como o programa guarda cada parcela da fatura portuguesa -->
| Parcela | Como entra no projeto |
| :--- | :--- |
| água | escalões em `water_tariffs`; o IVA da água em `water_tax_var` |
| saneamento por escalões | modo 3 do saneamento, sobre o volume recolhido (coeficiente de recolha × volume de água); a TRH e o IVA entram no preço de cada escalão |
| saneamento ou resíduos por m³ | modo 2 do saneamento, com um preço único por m³ de água, IVA incluído |
| tarifas fixas das outras parcelas | taxa fixa mensal (`water_tax_fixed`), com IVA |

Os resíduos por escalões (como no Funchal) ainda não têm campo próprio: a parte variável soma-se
à do saneamento, e só a parte fixa fica numa parcela à parte. A atualização tarifária é
introduzida em separado para a água, o saneamento e a energia (apêndice A).

### D.3. As quatro formas do saneamento

<!-- tabela: **Tabela 176** — As quatro formas de introduzir o saneamento -->
| Modo | O saneamento é |
| ---: | :--- |
| 0 | um valor fixo |
| 1 | uma percentagem da parcela de água (e não da fatura toda) |
| 2 | um valor por m³ consumido |
| 3 | escalões, aplicados a uma fração do volume de água que o utilizador declara |

### D.4. Os seis regimes

O programa classifica uma tabela de água num de seis regimes. O regime diz quanto vale poupar
água, que é o que um estudo de aproveitamento de água de chuva precisa de ver.

<!-- tabela: **Tabela 177** — Os seis regimes tarifários e o que acontece ao poupar -->
| Regime | Estrutura | O que acontece ao poupar |
| :--- | :--- | :--- |
| **Sem mínimo** | Só escalões progressivos. | Cada m³ poupado reduz a fatura. |
| **Tarifa de disponibilidade** | Um valor fixo que **soma** ao consumo medido. | Cada m³ poupado reduz a fatura; a parte fixa mantém-se. É a estrutura dos três tarifários transcritos. |
| **Franquia no mínimo** | O valor fixo já inclui um volume. | Poupar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | Até à franquia paga-se o valor fixo; passando-a, **tudo desde zero** é cobrado pelos escalões. | Ao passar a franquia, todo o volume é faturado desde zero. |
| **Piso de pagamento** | A fatura **não fica** abaixo do piso. | Não soma: limita. A poupança que leve a fatura abaixo do piso não rende nada. |
| **Fórmula exponencial** | Serviço básico mais `PB × Cⁿ`, com o expoente `n` dado pelo consumo do mês. | Cada m³ poupado reduz a fatura, mas não a um preço fixo por m³. |

**Teste rápido.** Simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os
com uma fatura real. Se só um coincidir, o regime está errado. A secção 3.3 ensina o
teste que identifica uma estrutura errada.

### D.5. Os tarifários transcritos

Os valores abaixo são os impressos nos documentos das entidades gestoras, transcritos em
`triton/data/portugal_tarifarios.json` e recolhidos em 07/10/2026. São exemplos fiéis de
como se introduz um tarifário, e não um catálogo: os tarifários mudam todos os anos, e é
preciso verificar o documento em vigor da sua entidade gestora antes de qualquer conclusão
económica. Os três têm a estrutura da tarifa de disponibilidade com escalões progressivos.

<!-- tabela: **Tabela 178** — Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço -->
| Concelho | Serviço | 0–5 | 5–15 | 15–25 | 25–50 | mais de 50 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Funchal | água | 0,39 | 0,69 | 1,28 | 2,87 | 5,02 |
| Funchal | saneamento | 0,00 | 0,55 | 1,01 | 1,01 | 1,01 |
| Lisboa | água | 0,4634 | 0,8666 | 2,0398 | 2,5961 | 2,5961 |
| Lisboa | saneamento | 0,2198 | 0,5787 | 1,3621 | 1,7165 | 1,7165 |
| Porto | água | 0,4945 | 0,9649 | 1,7657 | 3,0016 | 3,0016 |
| Porto | saneamento | 0,3875 | 0,7606 | 1,4608 | 2,4423 | 2,4423 |

#### D.5.1. Funchal: Câmara Municipal do Funchal

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 15 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Câmara Municipal do Funchal, Tabela de Taxas e Outras Receitas Municipais 2026
  Endereço: https://cmfdoc.funchal.pt/media/k2/attachments/Tabela_de_Taxas_Municipais_2026_.pdf (entregue pelo autor); SHA-256 `97084c0265bfcb75c75e7b9e2d95aebab3417973f3cd0964b34696d3eea76f87`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 179** — Estrutura do tarifário do Funchal -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 4,12 € | 4% |
| água, escalão | 0 | 5 | 0,39 €/m³ | 4% |
| água, escalão | 5 | 15 | 0,69 €/m³ | 4% |
| água, escalão | 15 | 25 | 1,28 €/m³ | 4% |
| água, escalão | 25 | 50 | 2,87 €/m³ | 4% |
| água, escalão | 50 | sem limite | 5,02 €/m³ | 4% |
| saneamento, tarifa fixa por mês | — | — | 1,97 € | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 0 | 5 | 0,00 €/m³ | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 5 | 15 | 0,55 €/m³ | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 15 | sem limite | 1,01 €/m³ | 4% |
| Resíduos urbanos (tarifa fixa), fixa por mês | — | — | 2,19 € | 4% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: **Tabela 180** — Contas mensais de conferência do tarifário do Funchal -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 17,0872 € |
| 30 m³/mês | 67,5272 € |

Hipóteses e dúvidas registadas ao transcrever:

- Tarifa de disponibilidade de água: 4,12 €/mês para contador até 15 mm (artigo 57.º).
- Água por escalões: até 5 m³ (0,39 €/m³), 6 a 15 m³ (0,69 €/m³), 16 a 25 m³ (1,28 €/m³), 26 a 50 m³ (2,87 €/m³) e > 50 m³ (5,02 €/m³) (artigo 56.º).
- Saneamento e resíduos urbanos têm escalões com cortes idênticos (0–5 m³ com valor zero, 6–15 m³ e > 15 m³). Como incidem sobre o volume de água consumida com a mesma taxa de IVA (4%), os componentes variáveis foram somados nos escalões de águas residuais: 0 a 5 m³ (0,00 €/m³), 5 a 15 m³ (0,33 + 0,22 = 0,55 €/m³) e > 15 m³ (0,41 + 0,60 = 1,01 €/m³).
- Tarifa fixa de saneamento: 1,97 €/mês (artigo 10.º); tarifa fixa de resíduos urbanos: 2,19 €/mês (artigo 6.º).
- IVA: o documento indica «Valor final sem IVA». Adotou-se 4%, que se tomou como a taxa reduzida do IVA na Região Autónoma da Madeira; a taxa, o diploma que a fixa e a sua aplicação à água, ao saneamento e aos resíduos NÃO foram verificados (sem consulta a fonte oficial) e ficam a confirmar. Com 5%, a conta de 10 m³ passaria de 17,0872 para 17,2515 €.
- Escalões de água, saneamento e resíduos aplicados por faixa (cada m³ paga o preço da sua faixa), como nos demais tarifários; a tabela não explicita se o preço do escalão atingido vale para todo o volume. A confirmar com a Câmara.
- O 1.º escalão (até 5 m³) de saneamento e de resíduos não tem valor impresso: tratado como zero, hipótese não confirmada (pode ser isenção ou omissão da tabela). O valor fixo mensal de cada um é cobrado em qualquer caso.
- A tabela não imprime Taxa de Recursos Hídricos (TRH 0 neste tarifário, a confirmar). O programa ainda não tem campo para resíduos por escalões, por isso a parte variável dos resíduos foi somada à do saneamento: na interface o «saneamento» do Funchal inclui os resíduos variáveis (só a parte fixa dos resíduos, 2,19 €/mês, fica numa parcela própria).

#### D.5.2. Lisboa: EPAL (água); Câmara Municipal de Lisboa (saneamento e resíduos urbanos)

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- EPAL, Preços de venda de água, 1.ª edição 2026
  Endereço: https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0; SHA-256 `d0ebc13e306944db42fc96b57544ade72625478e99b5b0dc26d81fc6f0b5f42d`; recolhido em 07/10/2026.
- CML, Tarifário do saneamento 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf (entregue pelo autor); SHA-256 `6c6295d9e5da3d09a7cd5476abe242757edd761b137359d5a4b561d1f080c37a`; recolhido em 07/10/2026.
- CML, Tarifário dos resíduos urbanos 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf (entregue pelo autor); SHA-256 `7fa873127affb4e33306166292c9da937f0d68b39987a97ead767a866e32e54f`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 181** — Estrutura do tarifário de Lisboa -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 5,82 € | 6% |
| água, escalão | 0 | 5 | 0,4634 €/m³ | 6% |
| água, escalão | 5 | 15 | 0,8666 €/m³ | 6% |
| água, escalão | 15 | 25 | 2,0398 €/m³ | 6% |
| água, escalão | 25 | sem limite | 2,5961 €/m³ | 6% |
| saneamento, tarifa fixa por mês | — | — | 2,999 € | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 0 | 5 | 0,2198 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 5 | 15 | 0,5787 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 15 | 25 | 1,3621 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 25 | sem limite | 1,7165 €/m³ | 0% |
| saneamento, taxa de recursos hídricos | — | — | 0,0320 €/m³ recolhido | 0% |
| Adicional C.M. Lisboa, por m³ de água | — | — | 0,1483 €/m³ | 0% |
| Resíduos urbanos, fixa por mês | — | — | 2,2333 € | 0% |
| Resíduos urbanos, por m³ de água | — | — | 0,1710 €/m³ | 0% |
| TGR (taxa de gestão de resíduos), por m³ de água | — | — | 0,0523 €/m³ | 0% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: **Tabela 182** — Contas mensais de conferência do tarifário de Lisboa -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 25,8683 € |
| 30 m³/mês | 94,3767 € |

Hipóteses e dúvidas registadas ao transcrever:

- IVA da água: 6%, declarado na tabela da EPAL (Código do IVA, Lista I, verba 1.7).
- Saneamento e resíduos: prestados pela própria Câmara; os documentos não cobram IVA, e a AT não aplica IVA a esses serviços quando prestados por entidade pública (posição contestada pela Provedora de Justiça, Público, 05/12/2024). Zero até haver fonte em contrário.
- Escalões do saneamento aplicados ao volume recolhido = 90% do volume de água (nota 1 do tarifário); a TRH do saneamento acresce por m³ recolhido (nota 4).
- Adicional C.M. Lisboa: por m³ de água, impresso na tabela da EPAL; a tabela não diz se leva IVA — tratado sem IVA, a confirmar numa fatura.
- Tarifas de disponibilidade por 30 dias tomadas como mensais.

#### D.5.3. Porto: Águas e Energia do Porto, EM

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Águas e Energia do Porto, Tarifário Geral 2026
  Endereço: https://www.aguasdoporto.pt/files/uploads/cms/Tarif%C3%A1rio%20Geral%202026.pdf; SHA-256 `7d6b5d0ceeef749d558018b4b1b24e661f3a415a1d55cab09f0de7aae340e0de`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 183** — Estrutura do tarifário do Porto -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 3,726 € | 6% |
| água, escalão | 0 | 5 | 0,4945 €/m³ | 6% |
| água, escalão | 5 | 15 | 0,9649 €/m³ | 6% |
| água, escalão | 15 | 25 | 1,7657 €/m³ | 6% |
| água, escalão | 25 | sem limite | 3,0016 €/m³ | 6% |
| saneamento, tarifa fixa por mês | — | — | 1,995 € | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 0 | 5 | 0,3875 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 5 | 15 | 0,7606 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 15 | 25 | 1,4608 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 25 | sem limite | 2,4423 €/m³ | 6% |
| Taxa de Recursos Hídricos (TRH), por m³ de água | — | — | 0,0392 €/m³ | 6% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: **Tabela 184** — Contas mensais de conferência do tarifário do Porto -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 20,2995 € |
| 30 m³/mês | 93,3293 € |

Hipóteses e dúvidas registadas ao transcrever:

- Tarifa de disponibilidade de água, utilizador doméstico, contador ≤ 20 mm (Q3 ≤ 4 m³/h): 0,1242 €/dia (pág. 2 do PDF, sob «Utilizadores domésticos») × 30 = 3,726 €/mês. O PDF repete a tabela na pág. 3 com 0,1367 €/dia para o mesmo escalão de contador; essa repetição vem depois da «Tarifa variável» dos utilizadores não domésticos (pág. 2) e sem cabeçalho próprio, e as demais linhas coincidem com as da pág. 2, por isso foi lida como a tarifa de disponibilidade dos não domésticos. Leitura por inferência do layout, a confirmar com a entidade gestora.
- Tarifa de disponibilidade de águas residuais: 0,0665 €/dia × 30 = 1,995 €/mês.
- IVA: 6% na água e nas águas residuais (Águas e Energia do Porto, EM).
- Taxa de Recursos Hídricos (TRH) da água: 0,0392 €/m³ devida à APA, com IVA a 6% (o PDF diz apenas que às tarifas acresce o IVA à taxa legal em vigor; os 6% são a taxa reduzida do Continente, não impressa no documento).
- Resíduos urbanos: não constam do tarifário da Águas e Energia do Porto (são da Porto Ambiente) e ficam de fora desta fatura. Meses de 30 dias, como nos escalões do PDF («/30 dias»).

#### D.5.4. Eletricidade

O Funchal leva ainda a tarifa de eletricidade, para o custo de bombagem: tarifa Base da
Empresa de Eletricidade da Madeira, 6,90 kVA, 0,1673 €/kWh sem IVA. A fonte é um comparador
(luzegas.pt, atualizado em 20/02/2025), **secundária**: confirme na EEM ou na ERSE. Lisboa e
Porto não têm tarifa de eletricidade registada, e o custo de bombagem fica a zero até o
utilizador introduzir a sua.

### D.6. Documentos recolhidos e ainda não transcritos

Os documentos abaixo estão arquivados com o endereço de origem e a impressão digital, mas
ainda não foram transcritos para o programa, que por isso não os oferece. Neles, introduza o
tarifário à mão. O tarifário de Bragança, em vigor, continua por obter.

<!-- tabela: **Tabela 185** — Concelhos com documento tarifário recolhido e ainda por transcrever -->
| Concelho | Entidade | Documento |
| :--- | :--- | :--- |
| Coimbra | Águas de Coimbra | editais n.º 433 e 438/2025 |
| Braga | AGERE | tarifário de fevereiro de 2026 |
| Setúbal | SMS Setúbal | água, saneamento e resíduos 2026 |
| Leiria | SMAS Leiria | tarifário 2026 |
| Faro | FAGAR | tarifário 2026 |
| Aveiro | AdRA | tarifário 2026 |
| Viseu | Águas de Viseu | tarifários de abril de 2026 |
| Beja | EMAS Beja | tarifário 2025 |
| Évora | Câmara Municipal de Évora | tarifário 2025 |
| Castelo Branco | SM Castelo Branco | tarifário em vigor (publicado em 24/02/2026) |
| Santarém | Águas de Santarém | tarifários geral e do saneamento 2026 |
| Ponta Delgada | SMAS Ponta Delgada | tarifário 2026 |
| Viana do Castelo | Águas do Alto Minho | cartaz do tarifário 2026 |
| Portalegre | SMAT Portalegre | edital 2026 |
| Guarda | Câmara Municipal da Guarda | edital n.º 16/2026 |
| Vila Real | ADIN e Câmara Municipal | tarifas 2026 e resíduos 2026 |

### D.7. Confiança dos valores tarifários por concelho

Nem todos os tarifários valem o mesmo. O Triton IBE traz transcritos 3 dos 280 concelhos que cobre (278 de Portugal continental, mais Funchal e Ponta Delgada), e para os restantes o utilizador introduz o tarifário do projeto. Para cada concelho, e para cada um dos três serviços (água, saneamento e resíduos urbanos), o programa de manutenção atribui um de três estados, com o motivo escrito.

Em Portugal a água, o saneamento de águas residuais e os resíduos urbanos são muitas vezes de entidades diferentes (em Lisboa, a EPAL fornece a água e a Câmara trata do saneamento e dos resíduos; no Porto, a Águas e Energia do Porto trata da água e do saneamento, e a EMAP dos resíduos). Por isso o estado é dado por serviço, cada um com a sua entidade e o seu documento. O saneamento cobra-se por escalões sobre uma fração do volume de água, o IVA vem de cada documento, a taxa de recursos hídricos (TRH) é uma parcela própria e a tarifa fixa depende do calibre do contador. Só se avalia o utilizador doméstico.

#### D.7.1. A escala e os critérios

<!-- tabela: **Tabela 186** — Estados de confiança dos valores tarifários e respetivos critérios -->
| Estado | Critério |
| :--- | :--- |
| 🟢 verde, verificado | Documento oficial arquivado com URL e SHA-256; `confirmado_em` há menos de 12 meses; transcrição conferida com as contas impressas; verificação independente registada em `verificado_por` (fatura real com tolerância de ±0,05 €, ou segunda leitura por uma pessoa diferente do transcritor; um modelo de IA nunca conta); e nenhuma pendência com efeito acima de 1 % na conta de 10 m³. |
| 🟡 amarelo, a validar | Há documento oficial arquivado ou transcrito, mas falta algum dos requisitos do verde: transcrição, conferência, reconfirmação nos últimos 12 meses, verificação independente, ou há pendência com efeito acima de 1 %. |
| ⚪ cinza, sem dado | Sem documento oficial arquivado, entidade gestora por identificar, ou dado ruim. O programa não traz tarifário e a ficha da ERSAR indica onde o procurar. |

O estado do concelho é verde quando os três serviços são verdes, cinza quando são todos cinza, e amarelo nos restantes casos. **Não há verde sem verificação independente**: a transcrição feita por quem leu o documento prova a aritmética, não a leitura. Uma **pendência** é uma hipótese que o documento não resolve (o IVA aplicado, um valor que não vem impresso, a leitura de uma tabela); cada uma traz o efeito estimado na conta de 10 m³ e, acima de 1 %, impede o verde.

#### D.7.2. Situação em 23/10/2026

<!-- tabela: **Tabela 187** — Concelhos e serviços por estado de confiança dos valores tarifários -->
| Estado | Concelhos | Água | Saneamento | Resíduos |
| :--- | ---: | ---: | ---: | ---: |
| 🟢 verde, verificado | 0 | 0 | 0 | 0 |
| 🟡 amarelo, a validar | 42 | 42 | 42 | 11 |
| ⚪ cinza, sem dado | 238 | 238 | 238 | 269 |
| **total** | **280** | **280** | **280** | **280** |

Por distrito (e região autónoma), com o estado do concelho:

<!-- tabela: **Tabela 188** — Concelhos por distrito e estado de confiança dos valores tarifários -->
| Distrito | 🟢 verde | 🟡 amarelo | ⚪ cinza | Total |
| :--- | ---: | ---: | ---: | ---: |
| Aveiro | 0 | 10 | 9 | 19 |
| Beja | 0 | 1 | 13 | 14 |
| Braga | 0 | 1 | 13 | 14 |
| Bragança | 0 | 3 | 9 | 12 |
| Castelo Branco | 0 | 1 | 10 | 11 |
| Coimbra | 0 | 1 | 16 | 17 |
| Évora | 0 | 1 | 13 | 14 |
| Faro | 0 | 1 | 15 | 16 |
| Guarda | 0 | 1 | 13 | 14 |
| Leiria | 0 | 1 | 15 | 16 |
| Lisboa | 0 | 1 | 15 | 16 |
| Portalegre | 0 | 1 | 14 | 15 |
| Porto | 0 | 1 | 17 | 18 |
| Região Autónoma da Madeira | 0 | 1 | 0 | 1 |
| Região Autónoma dos Açores | 0 | 1 | 0 | 1 |
| Santarém | 0 | 1 | 20 | 21 |
| Setúbal | 0 | 1 | 12 | 13 |
| Viana do Castelo | 0 | 7 | 3 | 10 |
| Vila Real | 0 | 6 | 8 | 14 |
| Viseu | 0 | 1 | 23 | 24 |

A tabela concelho a concelho (entidade gestora de cada serviço, estado de cada serviço, vigência, o que falta e a ligação ao documento ou à ficha tarifária da ERSAR) acompanha o programa em `tarifas_portugal/CONFIANCA_POR_CONCELHO.csv`, em formato aberto.

Os concelhos transcritos:

<!-- tabela: **Tabela 189** — Concelhos com tarifário transcrito e o estado de cada serviço -->
| Concelho | Água | Saneamento | Resíduos | O que falta |
| :--- | :--- | :--- | :--- | :--- |
| Funchal | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); pendência (efeito não quantificável): a tabela não diz se o preço do escalão atingido vale por faixa ou para todo o volume; água: pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; saneamento: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero; pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; resíduos: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero |
| Lisboa | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); saneamento: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 %; resíduos: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 % |
| Porto | 🟡 | 🟡 | ⚪ | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); água: pendência (efeito de 1,96 % na conta): tarifa de disponibilidade da água lida por inferência do layout (0,1242 €/dia; a outra leitura, 0,1367 €/dia, subiria a conta de 10 m³ 1,96 %); resíduos: entidade EMAP: sem documento arquivado |

#### D.7.3. Como ler o estado

1. Procure o concelho do projeto. A entidade gestora de cada serviço vem da ficha tarifária da ERSAR (e, no Funchal e em Ponta Delgada, do próprio documento); quando nenhuma fonte a indica, a tabela diz «a identificar».
2. Leia o estado de cada serviço, não só o do concelho: um concelho amarelo pode ter a água documentada e os resíduos sem dado.
3. Leia «o que falta». É a lista do que o utilizador deve verificar antes de apoiar uma conclusão económica.
4. Confira a vigência. Os tarifários portugueses mudam em regra todos os anos, em janeiro ou nos primeiros meses, e um tarifário com mais de 12 meses pode já ter sido substituído.

#### D.7.4. O que fazer em concelhos amarelos e cinzentos

- **Cinza.** Obtenha o tarifário em vigor da entidade gestora de cada serviço (a ficha da ERSAR indica a entidade e o ano), introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5) e confira a fatura que o programa calcula com uma fatura real do edifício.
- **Amarelo.** O valor tem documento oficial por trás, mas não foi verificado de modo independente. Confira a conta com uma fatura real e, se o programa lhe der um valor diferente por mais de 0,05 €, use o da fatura.
- **Em qualquer estado diferente de verde.** Declare no estudo a entidade gestora, a data de vigência e o estado de confiança, e acompanhe o resultado económico de uma análise de sensibilidade à tarifa.

### D.8. Introduzir o seu tarifário

1. Obtenha o documento tarifário em vigor da sua entidade gestora e anote a data.
2. Introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5).
3. Confira a fatura que o programa calcula com uma fatura real do edifício.
4. Declare no estudo a entidade gestora, a data de vigência, o regime e a moeda.

---

## Apêndice E — Base climática

> **A Edição Ibérica traz a base E-OBS por concelho.** A precipitação diária de 278 concelhos do
> Continente vem no programa, em `data/portugal_eobs.db`. Os Açores e a Madeira não têm série na base:
> para eles, a série é sempre um ficheiro do utilizador (secção 4.1). Um exemplo, o Funchal, vem com
> uma série de reanálise ERA5.

---

### E.1. O que a base contém

<!-- tabela: **Tabela 190** — Conteúdo da base de precipitação por concelho da Edição Ibérica -->
| O que a base traz | Valor |
| :--- | :--- |
| fonte | E-OBS v33.0e, precipitação diária (RR), média do conjunto, grelha regular de 0,1° |
| período | 01/01/1950 a 31/12/2025 (27 759 dias) |
| concelhos com série | 278, todos no Continente, em 18 distritos |
| concelhos sem série | 30: os 19 dos Açores e os 11 da Madeira |
| limites dos concelhos | CAOP2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR, 2.ª série, n.º 34, 18/02/2026) |
| formato | base SQLite (`portugal_eobs.db`), uma série comprimida por concelho |

**Como se obtém a série de um concelho.** É a média diária das células da grelha cujo centro cai dentro do
limite do concelho. Num concelho pequeno, sem nenhum centro de célula dentro do limite, usa-se a célula mais
próxima do centroide. Um dia sem dado em todas as células do concelho fica como falha (NaN), e a simulação
recusa a série, em vez de a tratar como dia seco. A grelha tem cerca de 10 km: a série de um concelho é uma
média de área, e suaviza as chuvadas intensas.

**Que concelhos ficam de fora, e porquê.** Os Açores situam-se a oeste de 25° W, fora do domínio da E-OBS.
Na Madeira, a E-OBS só tem a célula das estações que funcionavam em cada ano, e todos os concelhos faltam em
mais de 1% dos dias de 1991 a 2020 (o Funchal, em 22%). O critério da base é rejeitar o concelho com mais de
1% de dias sem dado nessa normal. Nenhum concelho recebe a série de um vizinho.

**Citação exigida pela fonte.** Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D.
(2018). An Ensemble Version of the E-OBS Temperature and Precipitation Data Sets. *Journal of Geophysical
Research: Atmospheres*, 123(17), 9391-9409. doi:10.1029/2017JD028200. Reconhecimento: *We acknowledge the E-OBS
dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the Copernicus Climate Change Service, and the
data providers in the ECA&D project (https://www.ecad.eu).*

**Recortes.** A normal climatológica de 1991 a 2020 é o recorte inicial. O programa oferece ainda as normais
de 1981-2010, 1971-2000 e 1961-1990 e o período dos últimos trinta anos (1996-2025); as janelas de estudo
são recortes livres da série.

---

### E.2. Quanto confiar na série da E-OBS

Comparámos a E-OBS (versão 33.0e) com o Iberia01, uma grelha de 0,1° feita com uma rede de 3 486 estações
da Península (AEMET, IPMA e APA), entre 1971 e 2000, célula a célula e dia a dia. Resultado:

- Em Portugal, a E-OBS dá em média 8% menos chuva que o Iberia01 (nos 10% de células mais afastadas, até 18%
  menos). Na Espanha, entre 10% e 16% menos.
- Os extremos saem alisados: o percentil 95 dos dias de chuva fica cerca de 9% abaixo em Portugal, e o máximo
  diário anual, 14% abaixo. Isto tende a subestimar o extravasamento de um reservatório.
- O calendário dos dias é bom (correlação diária mediana de 0,86 em Portugal).

Em três estações do GHCN-Daily que a E-OBS não usa (Faro, Évora e Castelo Branco), a E-OBS deu 19% a 22%
menos chuva. São poucas estações, por isso este resultado é preliminar. O Iberia01 termina em 2015 e os seus
autores avisam que não serve para análise de tendência histórica; por isso este manual não afirma nenhuma
tendência de longo prazo da chuva.

**Nível de qualidade por concelho.** O programa mostra um nível, A, B ou C, e o motivo. O nível é o pior de
duas medidas. *Concordância com o Iberia01*: A se a diferença do total anual é de 10% ou menos e a do máximo
diário anual de 15% ou menos; B se são de 20% e 25% ou menos; C no resto. Falamos de «diferença para o
Iberia01», e não de «viés»: o Iberia01 é também uma grelha interpolada, não uma medição. *Geometria*: só
rebaixa até B, quando o concelho tem menos de três células, quando nenhuma célula tem o centro lá dentro ou
quando a série é igual à de outro concelho.

<!-- tabela: **Tabela 191** — Concelhos de Portugal continental por nível de qualidade da chuva -->
| Nível | Concelhos | O que significa |
| :--- | ---: | :--- |
| A | 45 | três células ou mais e boa concordância com o Iberia01 |
| B | 159 | concordância razoável, ou poucas células |
| C | 74 | diferença grande para o Iberia01 |

Para 148 concelhos a geometria é o motivo de ficarem fora de A (menos de três células). O Algarve tem 15
dos 16 concelhos em C, e Braga, Vila Real e Santarém mais de metade. O nível não é uma nota de exatidão: diz
onde a base é mais frágil. Em C, valide com uma série local.

**E em Espanha?** O programa ainda não traz nenhum local espanhol: a linha de cobertura diz «Espanha: 0
locais», e é assim que deve ser lida. Como ensaio, feito fora do programa, aplicou-se a mesma fórmula às 52
capitais de província (incluindo Ceuta e Melilla). Quarenta e oito têm série e quatro ficam de fora, porque
estão fora da grelha do Iberia01 ou da E-OBS: Las Palmas de Gran Canaria, Santa Cruz de Tenerife, Ceuta e
Melilla. O critério de cobertura é, por isso, «48 capitais com série mais quatro exclusões documentadas», e não
«52 capitais». Cada capital foi tratada como um ponto (a célula da E-OBS mais próxima, a 14 km ou menos), e não
como a média de um município, que falta (o limite municipal ainda não foi incorporado). Resultado: 39 capitais
em B e 9 em C, nenhuma em A (a geometria de um só ponto limita o nível a B). As nove em C são Almería, Ávila,
A Coruña, Cuenca, Donostia/San Sebastián, Palencia, Santander, Segovia e Bilbao: nelas a E-OBS dá entre 20% e
34% menos chuva no total anual que o Iberia01. Estes resultados não estão na base do programa e não valem como
nível de nenhum município espanhol.

**Correção opcional.** A edição traz, em ficheiro separado, fatores mensais de correção do total, calibrados
com o Iberia01 em 1971–2000 (o período de referência que os autores recomendam) e **desligados por defeito**.
Ligá-los multiplica a chuva de cada mês pelo fator do concelho; o programa regista no projeto que a correção
foi usada. Os fatores derivam do Iberia01, que está sob a Open Database License, e por isso seguem sob a
mesma licença.

**Uso comercial.** A E-OBS é de uso estritamente não comercial em pesquisa e educação. No primeiro arranque o
programa pergunta o uso pretendido e o laudo repete a licença e a citação.

**Reprodutibilidade.** Cada projeto grava o identificador do pacote de chuva (`PT-EOBS-v33.0e-37fcba20`), a
versão da E-OBS e o SHA-256 do pacote, e por defeito leva a série dentro do ficheiro. Se reabrir um projeto
com um pacote diferente, o programa avisa e o laudo regista a mudança.

**Cobertura.** O ecrã inicial, o título da janela e o rodapé dos laudos mostram uma linha lida da base:
Portugal continental, 278 concelhos (A 45, B 159, C 74); Espanha: 0 locais. A grelha cobre a Península, mas a
edição só tem concelhos de Portugal por enquanto.

---

### E.3. A série que vem como ficheiro

Uma série diária acompanha o programa na pasta `data/rainfall`. É uma **reanálise**, e não um registo de
udómetro.

<!-- tabela: **Tabela 192** — Série de precipitação distribuída com a Edição Ibérica -->
| Ficheiro | Local | Período | Dias | Chuva média anual | Fonte |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `Funchal.csv` | Funchal (32,65° N, 16,90° O, célula de grelha a 323 m de altitude) | 01/01/1991 a 31/12/2020 | 10 958 | cerca de 538 mm | reanálise ERA5, via Open-Meteo |

O formato é um valor por linha: a precipitação diária em milímetros, sem data. A data do primeiro dia vem
do projeto (1 de janeiro de 1991 neste ficheiro).

**O que é.** A ERA5 é a reanálise global de quinta geração do Centro Europeu de Previsões Meteorológicas de
Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas (Hersbach et al., 2020,
*Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). A série foi extraída para uma
célula de grelha de cerca de 9 km, pela interface de arquivo da Open-Meteo.com (licença CC BY 4.0), em
14/10/2026. Uma célula é uma média de área: suaviza as chuvadas intensas e exagera o número de dias de
chuva fraca, e por isso é um ponto de partida, e não um substituto de um registo medido.

**Porque o Funchal usa a ERA5.** A E-OBS não serve ao Funchal (22% de dias sem dado em 1991-2020, acima do
limite de 1%). A média anual da reanálise pode diferir da média medida na estação. Num projeto real,
use a série medida.

**Os projetos de exemplo.** Lisboa e Porto usam a base E-OBS por concelho, e o ficheiro do projeto guarda a
referência da série e a impressão digital dos valores; por defeito a série vai dentro do ficheiro, com o identificador do pacote. O Funchal traz
a série ERA5 dentro do ficheiro.

---

### E.4. Usar a sua própria série

1. Obtenha um registo diário, em milímetros, do serviço meteorológico ou do udómetro mais próximo do local.
   Anote a estação, a distância ao local, o período e a fonte.
2. Guarde-o num CSV com um valor por dia. Aceita-se o ponto ou a vírgula como separador decimal, e uma linha
   de cabeçalho é ignorada.
3. Abra-o na etapa 1 (Projeto e chuva) e indique a data do primeiro dia.

Um ano incompleto é descartado na leitura, para não enviesar os totais anuais. Exigem-se dados diários: as
médias mensais escondem os períodos secos que decidem o volume (secção 5.1.2).

**Que extensão de série.** A extensão necessária para estabilizar o volume ideal não é uma constante
geográfica: cresce com a fração atendível e com a procura do edifício (glossário, apêndice G). A série
de cada concelho da base tem trinta anos na normal 1991-2020.

---

### E.5. Cenários futuros

A Edição Ibérica não traz projeções de modelos climáticos. Para estudar um clima futuro, prepare a série
diária projetada, a partir da fonte que escolher, e carregue-a como qualquer outro ficheiro. O fator de chuva
da modulação probabilística (secção 7.1) permite testar uma série mais seca ou mais húmida por uma
percentagem declarada. A secção 3.2 trata da condução do estudo.

---

### E.6. O que declarar num estudo

- a **fonte** da série (E-OBS v33.0e, estação ou produto de reanálise) e a sua versão;
- o **local**: o concelho da base, ou, para um udómetro, a distância ao local;
- o **período**, com o primeiro e o último ano;
- se a série foi **corrigida, preenchida ou regionalizada**, e como;
- para uma projeção, o modelo, o cenário e a janela, e o método de correção do enviesamento;
- o número de **anos** de dados;
- a citação e o reconhecimento exigidos pela E-OBS, e, para a ERA5, a atribuição à Open-Meteo.

---

## Apêndice F — Ficheiros, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

### F.1. O que o programa lê

<!-- tabela: **Tabela 193** — Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto guardado como tabela por uma versão inicial do programa | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia (a edição traz um exemplo em `data/rainfall`) | etapa 1. Projeto e Chuva |
| procura diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de procura, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um ficheiro desses, o programa avisa e adota os valores
> padrão para o que falta. A secção 3.8 mostra o que conferir depois de importar.

---

### F.2. O que o programa escreve

<!-- tabela: **Tabela 194** — Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Guardar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| folha de cálculo | `.xlsx` | série diária, varrimento e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV escolhe-se o separador: **ponto e vírgula** para abrir numa folha de cálculo
configurada em português, **vírgula** para o padrão internacional. Escolher mal faz a folha de
cálculo abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um ficheiro JSON com as
propriedades dos componentes, para compatibilização BIM. A secção 3.9 trata de todos.

---

### F.3. O ficheiro de projeto, por dentro

O `.triton` é um ficheiro de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete secções:

<!-- tabela: **Tabela 195** — As sete secções do ficheiro de projeto e o que cada uma guarda -->
| Secção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a eletrobomba |
| `water_quality_and_etap` | classe-alvo, desinfeção e tratamento |
| `financial_and_economic` | tarifas, impostos, atualizações e prazo |

O apêndice A lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do ficheiro.** É o que torna o projeto reproduzível:
> quem receber o ficheiro obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um ficheiro e muito para um anexo de e-mail com
> vinte deles.

---

### F.4. Onde ficam as coisas

<!-- tabela: **Tabela 196** — Localização dos ficheiros do programa e dos ficheiros do utilizador -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| os tarifários transcritos (Lisboa, Porto e Funchal) | dentro do programa, em `triton\data\portugal_tarifarios.json` |
| os casos do manual | na pasta do programa, em `casos` |
| os três projetos de exemplo (Lisboa, Porto e Funchal) | na pasta do programa, em `examples\portugal` |
| a base de precipitação por concelho (E-OBS) | na pasta do programa, em `data\portugal_eobs.db` |
| **os seus projetos e relatórios** | **onde escolher ao guardar** |

O programa não cria pasta de trabalho nem guarda ficheiros escondidos. Cada gravação
pergunta o destino, e nada do que se produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada do que é seu.

---

### F.5. Compatibilidade entre versões

<!-- tabela: **Tabela 197** — Compatibilidade entre versões do ficheiro de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o valor por defeito |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto legado em CSV | abre com aviso; confira o que a secção 3.8 lista |
| ficheiro JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um ficheiro JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores por defeito — e o utilizador
simularia 100 m² acreditando simular os 180 m² que o ficheiro descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.

---

## Apêndice G — Glossário

Termos técnicos e siglas, em português europeu, com o equivalente em inglês quando ele é usado na
literatura, acompanhados das diretrizes de padronização terminológica do Triton.

---

**AAC** (*aproveitamento de água de chuva*). Emprego da água precipitada sobre coberturas
para usos não potáveis em edifícios; a EN 16941-1 trata os sistemas de utilização de água
da chuva no local. Prefira-se o termo «aproveitamento» a «reutilização», porque a água de chuva captada
na cobertura é um recurso primário, e não um efluente gerado por um uso anterior.

**ACV** (*life cycle assessment*). Avaliação de ciclo de vida. Método que contabiliza os
impactos ambientais de um produto ao longo de toda a sua existência, da extração das
matérias-primas ao descarte. A do programa é de **triagem**, e não um inventário completo
conforme a ISO 14040.

**Água de chuva** (*rainwater*). Precipitação atmosférica recolhida diretamente em
superfícies impermeáveis de cobertura (telhados e lajes impermeabilizadas), antes de atingir
o solo ou as redes públicas. Designa o recurso natural e a fonte hídrica captada; evite-se a
forma coloquial «água da chuva».

**Água não potável** (*non-potable water*). Água que não se destina ao consumo humano direto,
mas cumpre os requisitos de qualidade exigidos para os usos admitidos: descargas de autoclismos e
mictórios, lavagem de veículos, pavimentos e roupa, rega de jardins e torres de arrefecimento.

**Água pluvial** (*stormwater*, *pluvial water*). Água de chuva que escoa superficialmente
por superfícies urbanas ou é conduzida por canalizações e sistemas prediais de drenagem. No Triton,
o termo aplica-se de preferência à infraestrutura predial e aos componentes de engenharia: *sistema
de aproveitamento de água pluvial (SAAP)*, *rede pluvial*, *procura pluvial*, *consumo de água pluvial*
e *extravasamento pluvial*.

**Água potável** (*potable water*, *drinking water*). Água que cumpre integralmente os
requisitos de qualidade da água para consumo humano em vigor no local do projeto, destinada à
ingestão direta, à preparação de alimentos e à higiene pessoal.

**Área de captação** (*catchment area*). Área projetada na **horizontal** da superfície
impermeável da cobertura onde a água é captada. Não é a área inclinada do telhado, nem a área
de contribuição usada para dimensionar caleiras e tubos de queda.

**BD+C** (*Building Design and Construction*). Família de referenciais do LEED
para projeto e construção de edificações novas ou em grande reforma. É a família
tratada neste manual, nas versões 4, 4.1 e 5.

**BIM** (*building information modeling*). Modelagem da informação da construção.
Representação digital da edificação em que cada componente carrega propriedades além da
geometria, o que permite compatibilizar projetos de disciplinas diferentes.

**CAD** (*computer-aided design*). Desenho assistido por computador. O programa exporta o
esquema hidráulico em DXF, formato de intercâmbio aceito pelos programas de CAD.

**CAOP** (*Carta Administrativa Oficial de Portugal*). Carta com os limites administrativos oficiais, publicada pela Direção-Geral do Território. A versão CAOP2025 define os limites dos 308 concelhos usados para calcular a série de chuva de cada concelho.

**CAPEX** (*capital expenditure*). Investimento inicial.

**CDD** (*consecutive dry days*). Maior sequência de dias consecutivos com chuva
abaixo de 1 mm.

**Coeficiente de escoamento** (*runoff coefficient*). Fração da chuva que
efetivamente chega ao reservatório, descontadas perdas por absorção, evaporação e
molhamento inicial da cobertura.

**Comprimento representativo de série de precipitação** (*representative rainfall time series length*, $N_{rep}$).
Menor período contínuo em anos de dados diários de chuva necessário para estabilizar
estatisticamente o dimensionamento e o desempenho do sistema (reproduzindo o volume ideal
e o potencial de economia da série completa sob confiança $\ge 90\%$), segundo a
metodologia de Geraldi e Ghisi (2017, 2018, 2019). O comprimento necessário não é uma
constante geográfica fixa: cresce com a fração atendível e com o nível de procura da edificação.

**E-OBS**. Conjunto europeu de dados meteorológicos diários em grelha, construído a partir de observações de estações (projeto ECA&D, serviço Copernicus de alterações climáticas). A Edição Ibérica usa a versão v33.0e da precipitação diária, em grelha de 0,1°, de 1950 a 2025, e obtém a série de cada concelho pela média das células dentro do seu limite (apêndice E).

**ERA5**. Reanálise global do Centro Europeu de Previsões Meteorológicas de Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas. Combina um modelo atmosférico com observações e dá uma série contínua em grelha. Usa-se no exemplo do Funchal; é uma média de área, e não um registo de udómetro.

**Fiabilidade temporal** ($C_t$). Percentual de dias em que o sistema atendeu
plenamente ($V_{con,t} = D_{pl,t}$), parcialmente ou não atendeu a procura pluvial.

**Fiabilidade volumétrica** ($C_v$). Fração da procura **pluvial** que o sistema atendeu
($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Não confundir com o potencial de economia,
que tem no denominador a procura total da edificação.

**CSV** (*comma-separated values*). Formato de ficheiro de texto em que cada linha é um
registo e as colunas são separadas por um caractere, tipicamente vírgula ou ponto e
vírgula. É o formato das séries de precipitação.

**cv**. Cavalo-vapor, unidade de potência equivalente a 0,7355 kW, usada na indicação de
eletrobombas. Uma eletrobomba de meio cv tem 0,37 kW de potência de eixo.

**CWD** (*consecutive wet days*). Maior sequência de dias consecutivos com chuva
igual ou superior a 1 mm.

**IVA**. Imposto sobre o valor acrescentado. Na fatura de água, cada parcela leva a taxa que o respetivo tarifário declara (6% na água de Lisboa e do Porto, 4% no Funchal, este último por confirmar); o programa não fixa nenhuma taxa no código (apêndice D).

**Procura estocástica** (*stochastic water demand*). Modelagem do consumo diário de água como
variável probabilística que varia dia a dia e entre realizações (Silva e Ghisi, 2016),
permitindo avaliar o escalão de incerteza do dimensionamento e dos indicadores de desempenho
sob variabilidade real de uso.

**Procura pluvial** (*pluvial demand*, $D_{pl}$). Parcela da procura diária de água da
edificação que pode ser suprida pelo sistema de aproveitamento ($D_{pl,t} = D_{tot,t} \times f$).
Corresponde aos pontos de consumo não potável interligados à rede pluvial.

**Descarte de primeiras águas** (*first flush*). Lâmina inicial de chuva desviada do
sistema, que arrasta a sujidade depositada na cobertura (o programa parte de 2 mm, que o utilizador
deve ajustar à sua cobertura). No Triton é **subtraída** da chuva do dia.

**Disponibilidade**. Regime tarifário em que um valor fixo **soma** por cima do
consumo medido. Cada metro cúbico economizado desconta.

**DN** (*diâmetro nominal*). Designação comercial do diâmetro de um tubo ou conexão, em
milímetros. Não corresponde exatamente ao diâmetro interno nem ao externo: é um número de
referência do qual decorrem as dimensões reais, tabeladas por norma.

**DXF** (*drawing exchange format*). Formato de intercâmbio de desenhos técnicos, lido
por praticamente todos os programas de CAD.

**EDGE** (*excellence in design for greater efficiencies*). Referencial de certificação
da International Finance Corporation, do Banco Mundial. Mede economia percentagem contra
um caso-base local em três dimensões independentes e exige que cada uma cruze o limiar.

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
de entrada, desinfeção e filtro de polimento.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). Grupo de trabalho
internacional que padronizou os índices de extremos climáticos, dos quais o programa
calcula oito.

**Extravasamento** (*spillage*, *overflow*). Volume que excede a capacidade do reservatório
e é conduzido pelo extravasor quando ele já está cheio.

**Fração atendível por água pluvial** (*non-potable demand share*, $f$). Percentual da procura
total de água da edificação ($D_{tot}$) passível de suprimento por água de chuva ($f = D_{pl} / D_{tot}$).
Representa o **teto assintótico intransponível** do potencial de economia de água potável
($E_{pot} \le f$): mesmo sob capacidade infinita de armazenamento e precipitação ilimitada,
a economia de potável nunca ultrapassa a fração atendível, pois o restante ($1 - f$) é
reservado aos usos nobres e potáveis. Distingue-se da fiabilidade volumétrica ($C_v = E_{pot} / f$),
que avalia o atendimento da parcela pluvial.

**Franquia no mínimo**. Regime tarifário em que o valor fixo já inclui um volume de
consumo. Economizar **abaixo** da franquia não reduz a fatura.

**Ganho marginal**. Variação do potencial de economia por metro cúbico acrescentado
ao reservatório, em %/m³ ($\Delta E_{pot} / \Delta V$). Critério de escolha do volume ideal.

**GRI** (*Global Reporting Initiative*). Padrão internacional de divulgação corporativa
de desempenho socioambiental. Sua série 303 trata de água e efluentes.

**IBE**. Sigla da Edição Ibérica do programa («Triton IBE», para a Península Ibérica): abre em português europeu, em euros, com a chuva E-OBS por concelho e os tarifários transcritos de Lisboa, Porto e Funchal. Hoje só os concelhos de Portugal têm dados; a linha de cobertura do programa diz quantos locais há em cada país (Espanha: 0). Os custos e os fatores de emissão são indicados pelo utilizador.

**IFC**. A sigla designa duas coisas distintas. Em certificação, é a *International
Finance Corporation*, do Banco Mundial, que desenvolve o EDGE. No contexto BIM, é o
*Industry Foundation Classes*, formato aberto de intercâmbio que o programa **não**
exporta: a exportação BIM do programa é um ficheiro JSON de propriedades.

**IPCC** (*Intergovernmental Panel on Climate Change*). Painel intergovernamental que
sintetiza o conhecimento científico sobre mudança do clima e organiza os relatórios de
avaliação a que as projeções climáticas se referem.

**ISO 14040**. Norma internacional que estabelece os princípios e a estrutura da
avaliação de ciclo de vida. Um inventário conforme a ISO 14040 exige rastreabilidade de
cada fluxo e revisão crítica externa, requisitos que uma avaliação de triagem não cumpre.

**JSON** (*JavaScript object notation*). Formato de ficheiro de texto estruturado, legível
por pessoas e por programas. É o formato interno do ficheiro `.triton`.

**LCOW** (*levelized cost of water*). Custo nivelado da água: razão entre o valor presente
de todos os custos do ciclo de vida do sistema (CAPEX, substituições, O&M, energia e
produtos químicos) e o volume descontado de água pluvial consumida ao longo do horizonte
de análise, em €/m³. Permite confrontar a viabilidade económica do sistema diretamente
com a tarifa da entidade gestora.

**LEED** (*leadership in energy and environmental design*). Referencial de certificação
ambiental de edificações do *U.S. Green Building Council*, o mais difundido
internacionalmente. Trata eficiência hídrica na categoria *Water Efficiency*: na versão 4,
pelos créditos WEc1 e WEc2; na versão 5, pelo crédito WEc2, *Enhanced Water Efficiency*.

**m.c.a.** Metro de coluna d'água, unidade de pressão equivalente à exercida por uma
coluna de água de um metro de altura, cerca de 9,81 kPa. É a unidade usual em instalações
prediais.

**Micromedição**. Medição individualizada por unidade habitacional em edifício
multifamiliar. Informada ao programa como número de economias.

**Manuais do Triton** (*Triton manual suite*). A documentação do programa, montada
das mesmas fontes em três formatos: o manual completo, oito volumes avulsos, cada um com
uma parte dele, e o sítio Web de documentação. Os volumes servem a quem precisa de uma parte
só, para consultar ou enviar:

1. **Manual completo**: todos os capítulos e apêndices.
   ![Capa do Manual Completo](../figuras/capas/capa_completo.png)
2. **Volume 1 — Comece aqui**: o que o programa faz, como instalá-lo e por onde entrar
   conforme o seu objetivo.
   ![Capa do Volume 1 — Comece Aqui](../figuras/capas/capa_1-comece-aqui.png)
3. **Volume 2 — O método**: as equações, os critérios e as fontes por trás de cada número
   que o programa publica.
   ![Capa do Volume 2 — O Método](../figuras/capas/capa_2-metodo.png)
4. **Volume 3 — Guias de uso**: outras cidades, clima futuro, tarifas, procura variável,
   lote, sensibilidade e exportação.
   ![Capa do Volume 3 — Guias Práticos](../figuras/capas/capa_3-guias.png)
5. **Volume 4 — Tutorial**: um projeto de moradia em Lisboa, do primeiro dado ao
   volume recomendado.
   ![Capa do Volume 4 — Tutorial](../figuras/capas/capa_4-tutorial.png)
6. **Volume 5 — Erros, limitações e fiabilidade**: os erros mais comuns, os limites
   do modelo e como o programa é verificado.
   ![Capa do Volume 5 — Fiabilidade](../figuras/capas/capa_5-fiabilidade.png)
7. **Volume 6 — Correções, erros e versões**: o que mudou entre versões, as
   mensagens de erro e como relatar um problema.
   ![Capa do Volume 6 — Versões](../figuras/capas/capa_6-versoes.png)
8. **Volume 7 — Modulação probabilística**: o estudo refeito com premissas sorteadas —
   variáveis, distribuições, leitura dos resultados e limites do método.
   ![Capa do Volume 7 — Modulação probabilística](../figuras/capas/capa_7-modulacao.png)
9. **Volume 8 — Apêndices**: parâmetros, processos, fatores de emissão, tarifas, base
   climática, formatos, glossário e referências.
   ![Capa do Volume 8 — Apêndices](../figuras/capas/capa_8-apendices.png)

Os PDFs acompanham o programa e abrem pela etapa 9. Documentação.

**Payback de carbono**. Tempo para a economia anual líquida de emissões pagar o
carbono incorporado na fabricação do sistema.

**Payback descontado**. Tempo para o fluxo de caixa descontado acumulado cruzar zero.

**PB**. Preço-base, em €/m³, da fórmula exponencial `PB × Cⁿ`, em que `C` é o consumo do mês e
`n` o expoente da tabela exponencial para esse consumo. É um dos seis regimes que o programa reconhece; os
tarifários transcritos para Portugal não o usam.

**PEAD**. Polietileno de alta densidade, material dos reservatórios de plástico mais comuns.
É o código do material no ficheiro de projeto.

**Piso de pagamento**. Regime tarifário em que a fatura **não fica** abaixo de um
valor. Diferente de disponibilidade: o piso limita por baixo, a disponibilidade soma
por cima.

**Potencial de economia de água potável** (*potable water saving potential*, $E_{pot}$).
Fração da procura **total** da edificação suprida por água pluvial ($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$).
É o indicador central do programa, limitado superiormente pela fração atendível ($E_{pot} \le f$).

**pp**. Pontos percentuais. Usado para exprimir a diferença entre dois percentuais: de
35% para 37% vão dois pontos percentuais, e não dois por cento.

**PRCPTOT**. Precipitação total anual em dias úmidos.

**PRFV**. Plástico reforçado com fibra de vidro, material de reservatórios de médio e
grande porte. Aparece no programa sob a designação «fibra».

**PRT**. Nome antigo da Edição Ibérica (IBE), de quando ela se chamava Edição Portugal. Projetos e scripts que ainda usam «PRT» (ou «POR») abrem como IBE.

**PVC**. Policloreto de vinilo, material das tubagens prediais de água fria e das colunas de
desvio do descarte inicial.

**R95p**. Soma da precipitação dos dias acima do percentil 95 dos dias úmidos.

**Rendimento da bomba**. Razão entre a potência hidráulica entregue à água e a
potência mecânica no eixo. Não inclui o motor.

**Rendimento do motor**. Razão entre a potência mecânica no eixo e a potência
elétrica consumida da rede.

**RX1day**, **RX5day**. Maior precipitação em um e em cinco dias consecutivos, no
ano.

**SAAP**. Sistema de aproveitamento de água pluvial. Conjunto integrado de componentes
prediais — área de captação, condutores, descarte inicial (*first flush*), estação de
tratamento (ETAP), cisterna inferior, reservatório superior, eletrobomba ou sobrepressor
e rede de distribuição independente — concebido para recolher, tratar, armazenar e fornecer
água não potável.

**SB**. Serviço básico: a parcela fixa mensal da fatura de água da fórmula exponencial, somada ao
resultado dessa fórmula.

**SDII** (*simple daily intensity index*). Precipitação média dos dias úmidos.

**SI** (*seasonality index*). Índice de sazonalidade de Walsh e Lawler. Zero quando a
chuva é uniforme ao longo do ano.

**SMAA** (*stochastic multicriteria acceptability analysis*). Método que sorteia
pesos e devolve a probabilidade de cada alternativa vencer.

**SSP** (*shared socioeconomic pathways*). Trajetórias socioeconómicas partilhadas,
que descrevem hipóteses coerentes de desenvolvimento global e as emissões correspondentes.
Combinam-se com os modelos climáticos para produzir projeções.

**TIR**. Taxa interna de retorno. A taxa de desconto que zera o valor presente
líquido.

**taxa de atualização**. Taxa de atualização. A taxa de desconto adotada.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*).
Método de ordenação multicritério de Hwang e Yoon.

**TRH** (*taxa de recursos hídricos*). Taxa por m³ que acresce à fatura de água e de águas residuais. No tarifário do Porto, a TRH da água é devida à Agência Portuguesa do Ambiente (APA) e leva IVA; no de Lisboa, a TRH do saneamento acresce por m³ recolhido.

**UV**. Radiação ultravioleta, empregada na desinfeção de água por inativação de
microrganismos. Atua apenas no instante da passagem pelo reator e não deixa residual, ao
contrário da cloragem.

**VIKOR**. Método de decisão multicritério proposto por Opricovic, que busca uma solução
de compromisso entre critérios conflitantes. Ver também *SMAA*.

**Volume ideal** (*optimal tank volume*). Menor volume de reservatório da grade de simulação
a partir do qual o ganho marginal de economia de água potável ($\Delta E_{pot} / \Delta V$)
cai abaixo de um limiar declarado (tipicamente $1,0\%/\text{m}^3$ ou $0,5\%/\text{m}^3$).
Evita o superdimensionamento de reservatórios, assegurando a melhor relação custo-benefício.

**VAL**. Valor atual líquido.

**WEM**. Codificação das medidas de eficiência hídrica do EDGE. A WEM14 é o sistema
de aproveitamento de água pluvial.

**XLSX**. Formato de pasta de trabalho do Microsoft Excel, baseado em XML compactado. É um
dos formatos de exportação de folhas de cálculo e de resultados da linha de comando.

**YAS** (*yield after spillage*). Regra de operação em que o extravasamento é
calculado **antes** da retirada da procura e, na forma estrita, a retirada do dia sai
só do volume guardado na véspera. O programa calcula o extravasamento antes, como a
YAS, mas deixa a chuva do dia atender a procura do dia; fica entre a YAS e a YBS
(secção 2.1).

**YBS** (*yield before spillage*). Regra de operação em que a procura é retirada **antes**
do cálculo do extravasamento. Supõe consumo anterior à chuva do dia e sobrestima o
aproveitamento; o programa não a adota, e o resultado dele fica entre a YAS e a YBS.

---

### G.1. Diretrizes de Padronização e Nomenclatura no Triton

A padronização terminológica é indispensável para assegurar a consistência e o rigor técnico
em artigos científicos, relatórios técnicos, na interface gráfica e na documentação do Triton.
As convenções a seguir detalham a distinção de termos correlatos frequentemente confundidos:

#### G.1.1. 1. Água de Chuva versus Água Pluvial versus «Água da Chuva»

<!-- tabela: **Tabela 198** — Padronização terminológica de água de chuva e água pluvial -->
| Termo | Definição e Contexto de Aplicação | Situação no Triton | Referência |
| :--- | :--- | :--- | :--- |
| **Água de chuva** (*rainwater*) | Precipitação atmosférica recolhida diretamente na cobertura (telhado/laje impermeabilizada), antes de atingir o solo ou as redes públicas. Refere-se à **fonte hídrica** e ao recurso ambiental. | **Canónico e preferencial** para o recurso captado («aproveitamento de água de chuva», «precipitação de água de chuva»). | Prática de redação técnica e científica. |
| **Água pluvial** (*stormwater* / *pluvial water*) | Água de chuva após escoamento superficial urbano ou quando conduzida por canalizações e sistemas prediais de drenagem e armazenamento. Aplica-se à **infraestrutura física** e aos componentes de engenharia. | **Canónico e preferencial** para sistemas, redes e balanço («sistema predial de água pluvial - SAAP», «rede pluvial», «procura pluvial», «extravasamento pluvial»). | Prática de redação técnica e científica. |
| **«Água da chuva»** | Expressão coloquial e informal. | **Desaconselhada**. Não deve ser empregada em publicações, textos normativos, relatórios do Triton ou código. | Prática de redação técnica e científica. |

#### G.1.2. 2. Fração Atendível, Procura Pluvial, Potencial e Fiabilidade

Para evitar ambiguidades matemáticas e conceituais frequentemente encontradas na literatura:

<!-- tabela: **Tabela 199** — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial -->
| Grandeza | Símbolo / Código | Definição | Fórmula | Relação / Teto |
| :--- | :--- | :--- | :--- | :--- |
| **Fração atendível por água pluvial** | $f$ / `rainwater_share` | Proporção da procura total da edificação correspondente a pontos de consumo não potável conectáveis ao SAAP. | $f = D_{pl} / D_{tot}$ | Parâmetro de projeto ($0 \le f \le 1$). Constitui o **teto assintótico** de $E_{pot}$. |
| **Procura pluvial** | $D_{pl}$ / `rainwater_demand` | Volume de água requerido pelos pontos não potáveis da edificação em um intervalo de tempo. | $D_{pl,t} = D_{tot,t} \times f$ | Em L/dia ou m³/ano. |
| **Volume de água pluvial consumido** | $V_{con}$ / `pluvial_consumed` | Volume de água não potável efetivamente suprido pelo reservatório pluvial aos pontos de consumo. | Determinado pelo balanço diário (secção 2.1) | $V_{con,t} \le D_{pl,t}$ e $V_{con,t} \le S_{t-1} + C_t$. |
| **Potencial de economia de água potável** | $E_{pot}$ / `potential_potable_savings_pct` | Percentual da procura **total** da edificação economizado pelo aproveitamento pluvial. | $E_{pot} = \frac{\sum V_{con}}{\sum D_{tot}} \times 100\%$ | **Indicador central**. Sempre $E_{pot} \le f$. |
| **Fiabilidade volumétrica** | $C_v$ / `volumetric_reliability_pct` | Percentual da procura **pluvial** suprido pela água de chuva armazenada. | $C_v = \frac{\sum V_{con}}{\sum D_{pl}} \times 100\%$ | $C_v = \frac{E_{pot}}{f}$. Pode atingir 100% mesmo quando $E_{pot} < 100\%$. |
| **Fiabilidade temporal** | $C_t$ / `temporal_reliability_pct` | Percentual de dias da série em que a procura pluvial foi 100% atendida ($V_{con,t} = D_{pl,t}$). | $C_t = \frac{N_{dias\_plenos}}{N_{total}} \times 100\%$ | Mede a segurança de abastecimento diário sem suplementação potável. |

#### G.1.3. 3. Síntese de Nomenclatura Recomendada para Artigos e Relatórios

- Utilize **«aproveitamento de água de chuva»** (e não «reutilização de água da chuva» — a água de chuva não é um efluente; o seu uso é *aproveitamento*, não *reutilização*).
- Utilize **«área de captação»** para o plano horizontal da cobertura e reserve **«área de contribuição»** para o dimensionamento hidráulico de caleiras e tubos de queda.
- Utilize **«descarte de primeiras águas»** ou *first flush* para a lâmina inicial desviada, e não «limiar de descarte».
- Utilize **«fração atendível»** (e não «procura relativa» ou «fração de economia») para expressar a partição de usos não potáveis no consumo total.
- Utilize **«comprimento representativo de série»** para a extensão mínima em anos necessária para estabilização estatística da simulação (metodologia de Geraldi e Ghisi).
- Utilize **«LCOW»** ou **«custo nivelado da água»** para a métrica de custo unitário ao longo do ciclo de vida descontado à taxa de atualização.

---

## Apêndice H — Referências

Normas, publicações e bases que sustentam as decisões do programa. A lista da Edição Ibérica só traz normas
internacionais e europeias e publicações de alcance geral, mais os documentos portugueses de que o programa
depende. A lista completa, com a proveniência de cada citação, está no módulo de bibliografia do programa e no
separador Documentação.

---

### H.1. Normas de aproveitamento de água de chuva

**EN 16941-1:2024** — On-site non-potable water systems — Part 1: Systems for the use of rainwater.
Bruxelas: CEN, 2024.

---

### H.2. Referenciais de certificação

**LEED v4 / v4.1 BD+C** — USGBC. Categoria *Water Efficiency*, créditos WEc1 e WEc2. Registo de projetos
comerciais até 30 jun. 2027.

**LEED v5 BD+C** — U.S. GREEN BUILDING COUNCIL. *LEED v5 Building Design and Construction: rating system*.
Washington, DC: USGBC, nov. 2025. Pré-requisitos WEp1 (*Water Metering and Reporting*) e WEp2 (*Minimum Water
Efficiency*), créditos WEc2 (*Enhanced Water Efficiency*) e SSc3 (*Rainwater Management*).

**EDGE** — IFC, Grupo Banco Mundial. *EDGE Certification Process*, e a codificação WEM das medidas de eficiência
hídrica. Administrado pelo GBCI em mais de 120 países.

**GRI 303** — Global Reporting Initiative. Água e efluentes, indicadores 303-3 e 303-5.

---

### H.3. Métodos

**Hwang, C.-L.; Yoon, K.** (1981). *Multiple Attribute Decision Making: Methods and Applications*. A formulação
original do TOPSIS.

**Opricovic, S.; Tzeng, G.-H.** O método VIKOR e as condições C1 e C2 de vantagem aceitável e estabilidade.

**Lahdelma, R.; Hokkanen, J.; Salminen, P.** (1998), e **Tervonen, T.; Figueira, J.** (2008). SMAA e SMAA-2.

**Walsh, R. P. D.; Lawler, D. M.** (1981). O índice de sazonalidade.

**ETCCDI** — *Expert Team on Climate Change Detection and Indices*, da OMM. Os índices de extremos climáticos.

---

### H.4. Usos finais da água

**Mayer, P. W.; DeOreo, W. B. et al.** (1999). *Residential End Uses of Water*. Denver: AWWA Research
Foundation. Frequência de uso dos aparelhos: 5,05 descargas e 0,37 ciclos de máquina de lavar roupa por pessoa
por dia; as descargas são a base dos acionamentos da pressurização direta.

---

### H.5. Normas de avaliação de ciclo de vida

**ISO 14040:2006** — Environmental management: life cycle assessment, principles and framework. As quatro fases
da avaliação.

**ISO 14044:2006** — Environmental management: life cycle assessment, requirements and guidelines.

**EN 15978:2011** — Sustainability of construction works: assessment of environmental performance of buildings,
calculation method. Os módulos A a D do ciclo de vida do edifício.

**EN 15804:2012+A2:2019** — Sustainability of construction works: environmental product declarations, core rules
for the product category of construction products.

---

### H.6. Dimensionamento e desempenho de sistemas de aproveitamento pluvial

**SOUZA, E. L.; GHISI, E.** (2012). Potable water savings by using rainwater for non-potable uses in houses.
*Water*, v. 4, n. 3, p. 607-628. doi:10.3390/w4030607.

**CAMPISANO, A. et al.** (2017). Urban rainwater harvesting systems: research, implementation and future
perspectives. *Water Research*, v. 115. doi:10.1016/j.watres.2017.02.056.

**CAMPISANO, A.; MODICA, C.** (2015). Appropriate resolution timescale to evaluate water saving and retention
potential of rainwater harvesting for toilet flushing in single houses. *Journal of Hydroinformatics*, v. 17,
n. 3. doi:10.2166/hydro.2015.022.

**FEWKES, A.; BUTLER, D.** (2000). Simulating the performance of rainwater collection and reuse systems using
behavioural models. *Building Services Engineering Research and Technology*, v. 21, n. 2, p. 99-106.
doi:10.1177/014362440002100204.

**GHISI, E.** (2010). Parameters influencing the sizing of rainwater tanks for use in houses. *Water Resources
Management*, v. 24, n. 10, p. 2381-2403. doi:10.1007/s11269-009-9557-4.

**HASHIMOTO, T.; STEDINGER, J. R.; LOUCKS, D. P.** (1982). Reliability, resiliency, and vulnerability criteria
for water resource system performance evaluation. *Water Resources Research*, v. 18, n. 1, p. 14-20.
doi:10.1029/WR018i001p00014.

**MATOS, C.; SANTOS, C.; PEREIRA, S. et al.** (2013). Rainwater storage tank sizing: case study of a commercial
building. *International Journal of Sustainable Built Environment*, v. 2, n. 2, p. 109-118.
doi:10.1016/j.ijsbe.2014.04.004.

**SEMAAN, M. et al.** (2020). Optimal sizing of rainwater harvesting systems for domestic water usages: a
systematic literature review. *Resources, Conservation & Recycling: X*, v. 6, 100033.
doi:10.1016/j.rcrx.2020.100033.

---

### H.7. Clima futuro

**HAWKINS, E.; SUTTON, R.** (2011). The potential to narrow uncertainty in projections of regional precipitation
change. *Climate Dynamics*, v. 37, p. 407-418. doi:10.1007/s00382-010-0810-6.

**KISAKYE, V.; VAN DER BRUGGEN, B.** (2018). Effects of climate change on water savings and water security from
rainwater harvesting systems. *Resources, Conservation and Recycling*. doi:10.1016/j.resconrec.2018.07.009.

**LASH, D. et al.** (2014). Robust rainwater harvesting: probabilistic tank sizing for climate change
adaptation. *Journal of Water and Climate Change*. doi:10.2166/wcc.2014.080.

**MARAUN, D.** (2016). Bias correcting climate change simulations: a critical review. *Current Climate Change
Reports*, v. 2, n. 4, p. 211-220. doi:10.1007/s40641-016-0050-x.

---

### H.8. Ciclo de vida e energia de sistemas pluviais

**GHIMIRE, S. R. et al.** (2014). Life cycle assessment of domestic and agricultural rainwater harvesting
systems. *Environmental Science & Technology*, v. 48. doi:10.1021/es500189f.

**GHIMIRE, S. R. et al.** (2017). Life cycle assessment of a commercial rainwater harvesting system compared
with a municipal water supply system. *Journal of Cleaner Production*. doi:10.1016/j.jclepro.2017.02.025.

**VAZ, I. C. M. et al.** (2023). Sustainable rainwater management and life cycle assessment: challenges and
perspectives. *Sustainability*, v. 15, n. 16, 12133. doi:10.3390/su151612133.

**VIEIRA, A. S. et al.** (2014). Energy intensity of rainwater harvesting systems: a review. *Renewable and
Sustainable Energy Reviews*, v. 34, p. 225-242. doi:10.1016/j.rser.2014.03.012.

**WARD, S.; BUTLER, D.; MEMON, F. A.** (2012). Benchmarking energy consumption and CO2 emissions from
rainwater-harvesting systems: an improved method by proxy. *Water and Environment Journal*, v. 26, n. 2,
p. 184-190. doi:10.1111/j.1747-6593.2011.00279.x.

---

### H.9. Incerteza e simulação de Monte Carlo

**SILVA, A. S.; GHISI, E.** (2016). Uncertainty analysis of daily potable water demand on the performance
evaluation of rainwater harvesting systems in residential buildings. *Journal of Environmental Management*,
v. 180, p. 82-93. doi:10.1016/j.jenvman.2016.05.028.

**WILSON, E. B.** (1927). Probable inference, the law of succession, and statistical inference. *Journal of the
American Statistical Association*, v. 22, n. 158, p. 209-212. doi:10.1080/01621459.1927.10502953.

**SPEARMAN, C.** (1904). The proof and measurement of association between two things. *The American Journal of
Psychology*, v. 15, n. 1, p. 72-101. doi:10.2307/1412159.

**SALTELLI, A.; RATTO, M.; ANDRES, T.; CAMPOLONGO, F.; CARIBONI, J.; GATELLI, D.; SAISANA, M.; TARANTOLA, S.**
(2008). *Global Sensitivity Analysis: The Primer*. Chichester: Wiley. doi:10.1002/9780470725184.

---

### H.10. Dados de precipitação

**CORNES, R. C.; VAN DER SCHRIER, G.; VAN DEN BESSELAAR, E. J. M.; JONES, P. D.** (2018). An ensemble version
of the E-OBS temperature and precipitation data sets. *Journal of Geophysical Research: Atmospheres*, v. 123,
n. 17, p. 9391-9409. doi:10.1029/2017JD028200. A base de precipitação por concelho (apêndice E).

**DIREÇÃO-GERAL DO TERRITÓRIO.** *Carta Administrativa Oficial de Portugal (CAOP2025)*. Aviso n.º 3502/2026/2,
Diário da República, 2.ª série, n.º 34, de 18/02/2026. Os limites dos concelhos.

**HERSBACH, H. et al.** (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological
Society*, v. 146, p. 1999-2049. A reanálise da série de exemplo do Funchal.

**Open-Meteo.com.** Weather data by Open-Meteo.com, licença CC BY 4.0, com base na reanálise ERA5 do ECMWF
(Copernicus Climate Change Service). Interface de arquivo consultada em 14/10/2026.

---

### H.11. Fatores de emissão

As fontes que o programa regista para os fatores de triagem do apêndice C. A sua reverificação para esta
edição está pendente.

**FRANKLIN ASSOCIATES** para o American Chemistry Council (2020). *Cradle-to-Gate Life Cycle Analysis of
High-Density Polyethylene (HDPE) Resin*. Tabela 6.

**HAMMOND, G. P.; JONES, C. I.** (2008). Embodied energy and carbon in construction materials. *Proceedings of
the Institution of Civil Engineers: Energy*, v. 161, n. 2, p. 87-98. doi:10.1680/ener.2008.161.2.87.

**EPD Australasia.** *Environmental product declaration: PVC pipes*, S-P-05503, 25/11/2022, EN 15804+A2.

**Grundfos.** *Environmental Product Declaration*, EPD-GRU-20250340-CBA1-EN, 2025, módulos A1 a A3.

**worldstainless** (World Steel Association). Relatório de emissões de CO₂, 24/09/2024.

**Composites UK.** *Embodied carbon data for composites*.

---

### H.12. Tarifários

Os documentos das entidades gestoras de onde se transcreveram os tarifários do apêndice D, com o endereço
de origem e a impressão digital SHA-256 registados em `tarifas_portugal/fontes/FONTES.tsv`:

**EPAL.** *Preços de venda de água*, 1.ª edição 2026 (Lisboa, água).

**Câmara Municipal de Lisboa.** *Tarifário do saneamento 2026* e *Tarifário dos resíduos urbanos 2026*,
Regulamento CML n.º 569-A/2014.

**Águas e Energia do Porto, EM.** *Tarifário Geral 2026*.

**Câmara Municipal do Funchal.** *Tabela de Taxas e Outras Receitas Municipais 2026*.

---

### H.13. Como citar o programa

Ao publicar um estudo feito com o Triton, cite o programa **com a versão** e a edição, e declare os itens da
secção 4.10. Um estudo que cita o programa sem versão não é reproduzível: as correções entre versões mudam
resultados, e a secção 2.6 traz o exemplo do consumo da eletrobomba, que mudou 65% entre duas versões
consecutivas.

---

## Apêndice I — Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

### I.1. Ficha 1 — O fluxo de um estudo completo

<!-- tabela: **Tabela 200** — Ficha de consulta: os dez passos de um estudo completo e a secção que trata de cada um -->
| # | Passo | O que se decide nele | Secção |
| ---: | :--- | :--- | ---: |
| 1 | Projeto e chuva | série, área, coeficiente, descarte | 4.1 |
| 2 | Edificação | tipologia, procura, fração atendível | 4.2 |
| 3 | Primeira simulação | um volume de palpite, para ver | 4.3 |
| 4 | Varrimento | curva de retorno, volume ideal | 4.4 |
| 5 | Arranjo | precisa de reservatório superior? | 4.5 |
| 6 | Qualidade | classe, desinfeção, filtros | 4.6 |
| 7 | Economia | tarifa real, CAPEX, fluxo de caixa | 4.7 |
| 8 | Carbono | inventário, material, período de recuperação | 4.8 |
| 9 | Decisão | sete critérios, pesos declarados | 4.9 |
| 10 | Relatório | saídas e lista de declaração | 4.10 |

**Antes de publicar:** secção 4.10, a lista de declaração. Secção 5.1, os dez erros. Secção 5.2, as limitações que afetam o seu caso.

---

### I.2. Ficha 2 — As armadilhas, em uma linha cada

<!-- tabela: **Tabela 201** — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada -->
| Armadilha | Onde |
| :--- | :--- |
| área **inclinada** em vez da projeção horizontal | 5.1.1 |
| chuva **média mensal** em vez da série diária | 5.1.2 |
| descarte em **litros** quando o campo quer milímetros | 5.1.3 |
| **regime de mínimo** tarifário ignorado | 5.1.4 |
| escola ou hospital com **tarifa residencial** | 5.1.5 |
| esperar mais **água** do reservatório superior | 5.1.6 |
| **série curta** demais | 5.1.7 |
| classe de qualidade escolhida pelo **custo** | 5.1.8 |
| comparar com **outro programa** sem declarar as diferenças de método | 5.1.9 |
| publicar o volume de **maior economia** como recomendado | 5.1.10 |

---

### I.3. Ficha 3 — Os seis regimes tarifários

<!-- tabela: **Tabela 202** — Ficha de consulta: os seis regimes tarifários e o efeito de poupar -->
| Regime | Ao poupar |
| :--- | :--- |
| sem mínimo | cada m³ desconta |
| tarifa de disponibilidade | cada m³ desconta; a parte fixa mantém-se |
| fórmula exponencial | cada m³ desconta; a conta é PB × Cⁿ + serviço básico |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** |
| franquia retroativa | passando-a, cobra tudo desde zero |
| piso de pagamento | a fatura não fica abaixo do piso |

**Teste rápido:** simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os com uma fatura
real. Se só um coincidir, o regime está errado.

Os tarifários de Lisboa, do Porto e do Funchal têm a estrutura da tarifa de disponibilidade com escalões
progressivos (apêndice D).

---

### I.4. Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: **Tabela 203** — Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | procura **total** | quanto do consumo de água potável cai |
| fiabilidade volumétrica | procura **pluvial** | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | dias da série | com que frequência se pode contar |
| extravasamento | — | o reservatório é pequeno? |
| ganho marginal | — | vale ampliar? |

`Epot = fiabilidade volumétrica × fração atendível`

---

### I.5. Ficha 5 — A cadeia de energia da eletrobomba

```
elevação:  e = ρ · g · H ÷ (η_bomba · η_motor)      kWh/m³
partidas:  E = placa × tempo ÷ η_motor              kWh
```

A placa é a potência **no eixo**. O rendimento do motor separa o eixo da tomada. Se o deixar
em branco, vale o valor típico para a potência nominal; introduza o rendimento do seu motor quando
tiver a ficha técnica.

---

### I.6. Ficha 6 — A lista de declaração, resumida

**Programa:** versão, com revisão.

**Chuva:** origem, recorte, anos; se projeção, modelo, cenário e janela.

**Edificação:** área e como foi obtida, coeficiente, per capita e origem, **fração
atendível** e os usos que a compõem.

**Descarte:** lâmina e modo; e a diferença de método, se comparar programas.

**Volume:** critério de escolha — limiar de ganho marginal, ou pesos do
multicritério.

**Economia:** concelho, entidade gestora, vigência da tabela, **regime de mínimo**,
regra do saneamento, taxas de IVA de cada parcela, taxa de atualização, inflação, atualizações e período, e a moeda.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores **aproximados** ou com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no LEED, a versão; no EDGE, que só a
barra de água foi avaliada.

---

## Apêndice J — Ficheiros de exemplo

O manual imprime resultados; estes ficheiros são o que se abre para
reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva
incorporada: abrem sem o CSV de origem, em qualquer computador. A chuva provém da base
E-OBS por concelho (1991–2020) para Lisboa e Porto, e da reanálise ERA5 para o Funchal,
que acompanham o programa (apêndice E); cada ficheiro traz o tarifário oficial da
sua localidade (apêndice D).

**Os custos são ilustrativos, não são preços de mercado.** Apenas os ficheiros do
tutorial de Lisboa (01, 04, 06, 09 e 10) trazem custos, em euros, com valores
arredondados que permitem acompanhar o método. Os restantes comparam chuva, procura e
tarifário, mantendo o investimento a zero. Antes de extrair qualquer conclusão económica,
introduza os seus próprios custos na etapa 5.

---

### J.1. Os casos do manual

<!-- tabela: **Tabela 204** — Os casos de exemplo e o que cada um demonstra -->
| Ficheiro | Secção | O que demonstra |
| :--- | :--- | :--- |
| `01_tutorial_lisboa.triton` | 4.1 a 4.10 | o projeto fechado do tutorial em Lisboa: cisterna de 5.000 L em polietileno e elevação para um reservatório superior de 1.000 L (custos ilustrativos, não são preços de mercado) |
| `02_porto.triton` | 3.1 | a moradia do tutorial levada ao Porto, com a chuva E-OBS do Porto e o tarifário da Águas e Energia do Porto (sem custos definidos) |
| `03_funchal.triton` | 3.1 | a moradia do tutorial levada ao Funchal, com a chuva ERA5 do Funchal, o tarifário da Câmara Municipal do Funchal e a eletricidade da EEM (sem custos definidos) |
| `04_tutorial_varredura.triton` | 4.4 e 2.2 | o projeto antes do reservatório superior, em modo varredura, de 0 a 20.000 L em passos de 1.000 L (Lisboa) |
| `05_dez_dias.triton` | 2.1 | o caso didático de dez dias, 11 a 20 de dezembro de 2019 da série de Lisboa, que cabe numa folha de cálculo |
| `06_reservatorio_superior.triton` | 4.5 | 5.000 L em baixo mais 1.000 em cima, a comparação da secção 4.5 contra os 6.000 L de um reservatório só (Lisboa) |
| `07_escola_semanal.triton` | 3.4 e 3.5 | uma escola do Porto, com 300 alunos e procura modulada por dia da semana |
| `08_hotel_mensal.triton` | 3.4 | um hotel de Lisboa com ocupação mensal ilustrativa, concentrada no verão seco |
| `09_modulacao_tutorial.triton` | 7.3 e 7.4 | a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, o tarifário e o investimento, mil realizações, semente 42 |
| `10_modulacao_captacao.triton` | 7.4 | a mesma varredura com a incerteza na captação (área, coeficiente de escoamento, descarte), o fator de chuva sobre a série de Lisboa, o tarifário e o investimento; mil realizações, semente 42 |

### J.2. O que cada um produz

Os valores abaixo são obtidos **relendo o ficheiro gravado** e simulando o
que foi relido, e não a configuração que o gerou. É a diferença que
importa: um parâmetro que não sobreviva à gravação aparece aqui como
número errado, em vez de passar despercebido.

<!-- tabela: **Tabela 205** — Resultado que cada caso de exemplo produz ao ser relido e simulado -->
| Ficheiro | Modo | Volume | Potencial | Pluvial consumida |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_lisboa.triton` | volume fixo | 5.000 L | 17,88% | 107,3 L/dia |
| `02_porto.triton` | volume fixo | 5.000 L | 22,04% | 132,3 L/dia |
| `03_funchal.triton` | volume fixo | 5.000 L | 12,98% | 77,9 L/dia |
| `04_tutorial_varredura.triton` | varredura | ideal: 5.000 L | 17,49% | 21 volumes |
| `05_dez_dias.triton` | volume fixo | 2.000 L | 24,43% | 48,9 L/dia |
| `06_reservatorio_superior.triton` | volume fixo | 5.000 L | 17,88% | 107,3 L/dia |
| `07_escola_semanal.triton` | volume fixo | 30.000 L | 23,03% | 2.076,2 L/dia |
| `08_hotel_mensal.triton` | volume fixo | 25.000 L | 10,36% | 866,7 L/dia |
| `09_modulacao_tutorial.triton` | varredura | ideal: 5.000 L | 17,49% | 21 volumes |
| `10_modulacao_captacao.triton` | varredura | ideal: 5.000 L | 17,49% | 21 volumes |

O caso 01 inclui o reservatório superior de 1.000 L, e o caso 06 compara-o com um único reservatório de 6.000 L, que obtém 18,19% (secção 4.5).

---

### J.3. Como abrir e simular

**Ficheiro, Abrir projeto**, escolha o ficheiro pretendido, e o programa carrega tudo:
a precipitação, a edificação, o tarifário, os custos e a configuração dos módulos de análise.
Percorra as etapas de resultado na barra lateral para analisar cada dimensão.

Os casos 09 e 10 abrem com a **Modulação Probabilística** configurada — as
variáveis, distribuições, número de realizações (1.000) e semente determinística (42) da
secção 7.4: vá à etapa 13 e clique em **Simular**. Ambos estão em modo varredura,
que permite traçar as curvas por volume; num caso de volume fixo, o módulo apresenta
apenas o volume de dimensionamento.

Os ficheiros situam-se na pasta `casos`, no diretório de instalação do programa.
Para modificá-los, **grave com outro nome**: dessa forma o ficheiro original continua a
reproduzir exatamente os números apresentados no manual.

---

### J.4. Os estudos de `exemplos`

Além dos casos didáticos do manual, o programa disponibiliza em `examples/portugal/` os
projetos de referência para Lisboa, Porto e Funchal. Permitem explorar a aplicação direta
dos tarifários locais em moradias unifamiliares completas.

---

### J.5. O que estes ficheiros não são

Não são modelos fechados de projeto de execução. São **casos de demonstração metodológica**:
os custos do tutorial são estritamente ilustrativos, o tarifário de base é o de Lisboa e as
categorias refletem as condições domésticas convencionais. Num projeto real de engenharia,
introduza a série pluviométrica local, os orçamentos reais de fornecedores e a tabela tarifária
em vigor do município.
