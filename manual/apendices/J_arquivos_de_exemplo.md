# Arquivos de exemplo

O manual imprime resultados; estes arquivos são o que se abre para
reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva
incorporada: abrem sem o CSV de origem, em qualquer máquina.

---

## Os nove casos do manual

<!-- tabela: Os nove casos de exemplo e o que cada um demonstra -->
| Arquivo | Seção | O que demonstra |
| :--- | :--- | :--- |
| `01_tutorial_florianopolis.netuno` | 4.1 a 4.10 | o projeto do tutorial, com a cisterna escolhida na seção 4.9 |
| `02_tutorial_varredura.netuno` | 4.4 e 2.2 | o mesmo projeto em modo varredura, de 0 a 20.000 L, passo de 1.000 L |
| `03_dez_dias.netuno` | 2.1 | o caso didático de dez dias, que cabe numa planilha |
| `04_reservatorio_superior.netuno` | 4.5 | 5.000 L embaixo mais 1.000 em cima, a comparação da seção 4.5 contra os 6.000 L de um tanque só |
| `05_manaus.netuno` | 3.1 | o projeto do tutorial levado a Manaus, que chove mais e rende menos |
| `06_brasilia.netuno` | 3.1 | o projeto do tutorial levado a Brasília, de estação seca marcada |
| `07_saopaulo.netuno` | 3.1 | o projeto do tutorial levado a São Paulo |
| `08_escola_semanal.netuno` | 3.4 e 3.5 | escola de 300 alunos com demanda modulada por dia da semana |
| `09_hotel_mensal.netuno` | 3.4 | hotel de litoral com ocupação mensal em fase com a chuva |

## O que cada um produz

Os valores abaixo são obtidos **relendo o arquivo gravado** e simulando o
que foi relido, e não a configuração que o gerou. É a diferença que
importa: um parâmetro que não sobreviva à gravação aparece aqui como
número errado, em vez de passar despercebido.

<!-- tabela: Resultado que cada caso de exemplo produz ao ser relido e simulado -->
| Arquivo | Modo | Volume | Potencial | Pluvial consumida |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_florianopolis.netuno` | volume fixo | 5.000 L | 37,46% | 224,7 L/dia |
| `02_tutorial_varredura.netuno` | varredura | ideal: 5.000 L | 37,46% | 21 volumes |
| `03_dez_dias.netuno` | volume fixo | 2.000 L | 36,00% | 72,0 L/dia |
| `04_reservatorio_superior.netuno` | volume fixo | 5.000 L | 37,76% | 226,5 L/dia |
| `05_manaus.netuno` | volume fixo | 5.000 L | 27,92% | 167,5 L/dia |
| `06_brasilia.netuno` | volume fixo | 5.000 L | 20,80% | 124,8 L/dia |
| `07_saopaulo.netuno` | volume fixo | 5.000 L | 34,77% | 208,6 L/dia |
| `08_escola_semanal.netuno` | volume fixo | 30.000 L | 34,34% | 3.095,8 L/dia |
| `09_hotel_mensal.netuno` | volume fixo | 25.000 L | 32,11% | 1.854,9 L/dia |

---

## Como rodar

**Arquivo, Abrir projeto**, escolha o arquivo, e o programa carrega tudo: a
chuva, a edificação, os custos e a configuração das análises. Percorra as
etapas de resultado na barra lateral para ver cada dimensão.

Os arquivos ficam na pasta `casos`, dentro da pasta de instalação do
programa. Se quiser modificá-los, **salve com outro nome**: assim o caso
original continua reproduzindo o número impresso no manual.

---

## Os três estudos de `exemplos`

Além dos casos do manual, o programa traz três estudos de referência em
`exemplos`: residência unifamiliar em Florianópolis, edifício
corporativo em Brasília e escola pública em Manaus. São maiores e menos
didáticos que os do manual, e servem de ponto de partida para projetos
reais.

> **Eles foram regravados nesta versão.** Estavam num esquema plano
> anterior, que o programa lia sem reconhecer: abriam como projeto
> padrão, com 100 m² e três moradores, e nada avisava. A abertura agora
> recusa formato desconhecido com mensagem própria, e os três foram
> convertidos para o esquema corrente, com a chuva incorporada.

---

## O que estes arquivos não são

Não são gabarito de projeto. São **casos de demonstração**: os custos são
os do tutorial, a tarifa é a da CASAN e a categoria é residencial em
todos, inclusive na escola e no hotel, pela limitação que a seção {{n:36}}
descreve. Para um estudo real, troque tarifa, custos e série de chuva
pelos do seu caso.
