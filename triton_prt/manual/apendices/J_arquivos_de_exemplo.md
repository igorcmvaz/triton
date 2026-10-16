# Ficheiros de exemplo

O manual imprime resultados; estes ficheiros são o que se abre para
reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva
incorporada: abrem sem o CSV de origem, em qualquer computador. A chuva provém da base
E-OBS por concelho (1991–2020) para Lisboa e Porto, e da reanálise ERA5 para o Funchal,
que acompanham o programa (apêndice {{n:E}}); cada ficheiro traz o tarifário oficial da
sua localidade (apêndice {{n:D}}).

**Os custos são ilustrativos, não são preços de mercado.** Apenas os ficheiros do
tutorial de Lisboa (01, 04, 06, 09 e 10) trazem custos, em euros, com valores
arredondados que permitem acompanhar o método. Os restantes comparam chuva, procura e
tarifário, mantendo o investimento a zero. Antes de extrair qualquer conclusão económica,
introduza os seus próprios custos na etapa 5.

---

## Os casos do manual

<!-- tabela: Os casos de exemplo e o que cada um demonstra -->
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

## O que cada um produz

Os valores abaixo são obtidos **relendo o ficheiro gravado** e simulando o
que foi relido, e não a configuração que o gerou. É a diferença que
importa: um parâmetro que não sobreviva à gravação aparece aqui como
número errado, em vez de passar despercebido.

<!-- tabela: Resultado que cada caso de exemplo produz ao ser relido e simulado -->
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

O caso 01 inclui o reservatório superior de 1.000 L, e o caso 06 compara-o com um único reservatório de 6.000 L, que obtém 18,19% (secção {{n:8}}).

---

## Como abrir e simular

**Ficheiro, Abrir projeto**, escolha o ficheiro pretendido, e o programa carrega tudo:
a precipitação, a edificação, o tarifário, os custos e a configuração dos módulos de análise.
Percorra as etapas de resultado na barra lateral para analisar cada dimensão.

Os casos 09 e 10 abrem com a **Modulação Probabilística** configurada — as
variáveis, distribuições, número de realizações (1.000) e semente determinística (42) da
secção {{n:43}}: vá à etapa 13 e clique em **Simular**. Ambos estão em modo varredura,
que permite traçar as curvas por volume; num caso de volume fixo, o módulo apresenta
apenas o volume de dimensionamento.

Os ficheiros situam-se na pasta `casos`, no diretório de instalação do programa.
Para modificá-los, **grave com outro nome**: dessa forma o ficheiro original continua a
reproduzir exatamente os números apresentados no manual.

---

## Os estudos de `exemplos`

Além dos casos didáticos do manual, o programa disponibiliza em `examples/portugal/` os
projetos de referência para Lisboa, Porto e Funchal. Permitem explorar a aplicação direta
dos tarifários locais em moradias unifamiliares completas.

---

## O que estes ficheiros não são

Não são modelos fechados de projeto de execução. São **casos de demonstração metodológica**:
os custos do tutorial são estritamente ilustrativos, o tarifário de base é o de Lisboa e as
categorias refletem as condições domésticas convencionais. Num projeto real de engenharia,
introduza a série pluviométrica local, os orçamentos reais de fornecedores e a tabela tarifária
em vigor do município.
