# Comparar muitos casos de uma vez

> **Pergunta que este guia responde:** como comparar dezenas de alternativas sem
> refazer o projeto inteiro a cada uma?

O programa foi construído para comparar alternativas, e oferece três formas distintas de
fazê-lo. A escolha entre elas não é questão de preferência: cada forma responde a uma
pergunta diferente, e usar a errada custa tempo sem produzir a informação desejada.

---

## As três formas

| Se o que muda é | Use | Onde |
| :--- | :--- | :--- |
| **só o volume da cisterna** | a varredura | Reservatório e Custos |
| **o volume, e você quer decidir** | a tabela multicritério | Multi-Critério |
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

> **Aprofundamento: estudos de larga escala.** O grupo de pesquisa executa séries de
> milhares de simulações para trabalhos publicados — matrizes fatoriais de cidade,
> área, demanda e volume, com propagação de incerteza por Monte Carlo. Isso é feito
> por uma interface de automação que acompanha a distribuição de código-fonte do
> programa, e não pela janela. Se o seu trabalho chegou a essa escala, o caminho é
> entrar em contato com o grupo: a interface existe, é a mesma usada para verificar o
> programa, e a seção {{n:34}} descreve o que ela verifica.
