# Comparar muitos casos de uma vez

> **Pergunta que este guia responde:** como comparar dezenas de alternativas sem
> refazer o projeto inteiro a cada uma?

O programa foi construído para comparar alternativas, e oferece três formas distintas de
fazê-lo. A escolha entre elas não é questão de preferência: cada forma responde a uma
pergunta diferente, e usar a errada custa tempo sem produzir a informação desejada.

---

## As três formas

<!-- tabela: As três formas de comparar alternativas conforme o que varia entre elas -->
| Se o que muda é | Use | Onde |
| :--- | :--- | :--- |
| **só o volume da cisterna** | a varredura | etapa 4. Reservatório & Custos |
| **o volume, e você quer decidir** | a tabela multicritério | etapa 8. Decisão Multicritério |
| **qualquer outra premissa** | projetos salvos, um por caso | arquivo `.netuno` |

A primeira é automática, a segunda também, e a terceira exige organização.

---

## A varredura: dezenas de volumes numa passada

Na etapa **4. Reservatório & Custos**, escolha o modo **varredura** e informe o volume
máximo e o passo. O programa simula todos os volumes da grade e desenha a curva.

A varredura é o caminho normal de trabalho, e não uma função avançada reservada a casos
especiais: ela é quase sempre a resposta certa, porque «qual volume adotar?» é a pergunta
central de todo projeto de aproveitamento pluvial. A seção {{n:7}} percorre uma varredura
completa passo a passo, e a seção {{n:24}} formaliza como a grade de volumes é montada.

O custo computacional é modesto e não justifica hesitação: uma varredura de 0 a 20.000 L
com passo de 1.000 L corresponde a vinte e uma simulações de trinta anos cada, e é
concluída em poucos segundos numa máquina comum.

---

## A tabela multicritério: todos os volumes, todas as dimensões

A etapa **8. Decisão Multicritério** mostra, numa tabela só, cada volume da varredura com:

- a economia de água e os dias de atendimento;
- o valor presente líquido, o retorno descontado e a taxa interna de retorno;
- o carbono líquido ao fim da vida útil e o retorno ambiental;
- a pontuação TOPSIS e a aceitabilidade SMAA-VIKOR.

É a forma mais densa de comparar alternativas que o programa oferece: dez colunas de
resposta para cada linha de volume. O **perfil de decisão** troca os pesos das
dimensões e reordena a tabela na hora. A seção {{n:32}} explica os métodos por trás.

---

## Quando muda outra coisa que não o volume

Cidade, tarifa, demanda, material do reservatório e tipologia da edificação são
parâmetros que a varredura não percorre, e para variar qualquer um deles o caminho é
manter um projeto salvo por caso. O procedimento abaixo parece burocrático à primeira
vista e economiza horas de retrabalho, sobretudo quando o estudo é retomado semanas
depois.

1. Monte o projeto completo uma vez, com todo o detalhe.
2. Salve com um nome que descreva o caso: `escola_florianopolis_5000.netuno`.
3. Mude **uma** coisa, e salve com outro nome.
4. Rode cada um, e anote o resultado numa planilha sua.

Os arquivos de exemplo do manual foram feitos assim: `05_manaus.netuno`,
`06_brasilia.netuno` e `07_saopaulo.netuno` são o mesmo projeto, com a série de chuva
trocada. É o que a seção {{n:14}} compara.

> **Mude uma coisa de cada vez.** Se você trocar a cidade e a tarifa juntas, o
> resultado muda e não há como saber qual das duas o moveu. Parece óbvio, e é o erro
> mais comum em estudos comparativos.

---

## Como organizar os arquivos

Uma convenção de nomes poupa mais tempo do que parece:

```
estudo_escola/
   base.netuno
   cidade_florianopolis.netuno
   cidade_manaus.netuno
   tarifa_comercial.netuno
   demanda_medida.netuno
   resultados.xlsx
```

E três hábitos que evitam retrabalho:

**Guarde o projeto, não só o resultado.** O `.netuno` tem a chuva dentro dele e
reproduz o estudo inteiro; a planilha de resultados, não.

**Anote o que muda no nome do arquivo.** Seis meses depois, `teste3.netuno` não
significa nada.

**Exporte para planilha ao fim de cada rodada.** A etapa **10. Exportação**
grava as tabelas em `.xlsx`, e é lá que a comparação entre casos é montada.

---

## Quantos casos cabem

O programa não impõe limite ao número de casos comparados, e o limite real é de paciência
do analista: cada simulação de trinta anos leva frações de segundo, mas montar e conferir
cada projeto leva minutos, e é a conferência que consome o tempo.

Na prática, um estudo comparativo bem conduzido reúne entre cinco e vinte casos. Quando o
número cresce muito além disso, costuma ser sinal de que a pergunta de pesquisa não foi
suficientemente delimitada — ou de que o trabalho é um estudo de larga escala, que exige
outro instrumental.

Para estudos de larga escala — matrizes fatoriais de cidade, área, demanda e volume, ou propagação de incerteza — o programa oferece uma interface de linha de comando, descrita a seguir.

---

## A linha de comando

A instalação do programa como pacote Python registra o comando `netuno`, que executa as mesmas rotinas de cálculo da interface gráfica sem abrir a janela; o instalador de Windows com interface gráfica não o inclui. A linha de comando lê arquivos `.netuno`, projetos em JSON estruturado e o formato CSV do Netuno 4, e grava os resultados em texto, JSON, CSV, HTML ou XLSX. É a interface indicada para estudos reprodutíveis, porque o próprio comando documenta as premissas alteradas.

<!-- tabela: Subcomandos da linha de comando e finalidade de cada um -->
| Subcomando | Finalidade |
| :--- | :--- |
| `validate` | confere a estrutura do projeto, a série de chuva e as premissas essenciais, sem simular |
| `run` | simula o projeto; por padrão, apenas a análise técnica |
| `analyze` | executa a cadeia completa: técnica, econômica, ambiental e TOPSIS |
| `econ` | executa a análise econômica |
| `init` | cria um projeto `.netuno` modelo, editável, com a série de chuva referenciada ou incorporada |
| `init-catalog` | cria um catálogo JSON modelo de premissas de edificação ou de climas |
| `matrix` | combina um catálogo de premissas com um catálogo de climas e simula todas as combinações |
| `matrix-projects` | executa uma lista de projetos, uma pasta de séries de chuva ou a matriz fatorial declarada no projeto |
| `batch` | executa os cenários de uma planilha CSV ou XLSX, a partir de um projeto-base |
| `uncertainty` | propaga incertezas por Monte Carlo para um volume de reservatório |

Os subcomandos `run`, `analyze` e `econ` aceitam as mesmas opções: `--analysis` escolhe a análise (`technical`, `economic`, `environmental`, `topsis` ou `all`); `--volume` fixa o volume do reservatório inferior, em litros; `--rainfall` substitui a série de chuva do projeto; `--set CAMPO=VALOR` altera um campo do projeto e pode ser repetido; `--weights` informa os pesos técnico, econômico e ambiental do TOPSIS; `--weight-sensitivity N` sorteia N vetores de pesos e informa a frequência com que cada volume vence; `--format` e `--output` definem o formato e o arquivo de saída; e `--seed` fixa a semente das análises estocásticas, para que o resultado seja reprodutível.

Aplicados ao projeto do tutorial, `validate` e `run` produzem:

```
netuno validate 01_tutorial_florianopolis.netuno
Projeto válido: estrutura, chuva e premissas essenciais verificadas.

netuno run 01_tutorial_florianopolis.netuno --volume 5000 --format json --output r.json
```

O arquivo `r.json` registra a procedência — projeto de origem, número de dias da série e data inicial — e, para o volume de 5.000 L, o potencial de economia de 37,46%, o volume pluvial consumido de 82,1 m³/ano, o extravasamento de 105,2 m³/ano e a classificação dos dias em 92,9% plenos, 1,4% parciais e 5,7% nulos.

O subcomando `uncertainty` sorteia, em cada amostra, a precipitação, a área de captação, a demanda e o investimento com distribuição de coeficiente de variação declarado — por padrão, 10% para a precipitação, 0% para a área, 10% para a demanda e 15% para o investimento, em 200 amostras — e informa os percentis de 5%, 50% e 95% do potencial de economia e do valor presente líquido, com a probabilidade de o valor presente líquido ser positivo. No tutorial, com 50 amostras e 5.000 L, o potencial de economia fica entre 36,1% e 38,6%, com mediana de 37,4%.

> Os subcomandos `compare-mass` e `run-vaz-study` executam estudos de pesquisa do grupo sobre bases climáticas de dezenas de milhares de séries, e exigem os arquivos dessas bases; não fazem parte do uso corrente do programa.
