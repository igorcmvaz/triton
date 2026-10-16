# Como executar

> **Pergunta a que esta secção responde:** quais são os passos, no ecrã e na linha de comandos?

## Na interface

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
   sobre uma delas mostra o que representa. A secção {{n:41}} descreve cada grupo.
2. **Distribuições.** Um cartão por variável marcada, com o valor do estudo, a distribuição, os
   parâmetros, os limites e a curva. O botão **Valores de triagem** devolve todas as distribuições
   ao padrão centrado no projeto.
3. **Execução.** O número de realizações (1 000 por omissão), a semente (42) e a variação diária
   opcional. **Simular** executa em segundo plano, com barra de progresso, tempo restante e botão
   **Cancelar**; se for cancelada, a análise mostra as realizações já feitas.
4. **Resultados.** Tabelas e figuras numeradas, explicadas na secção {{n:43}}.

A disposição reorganiza-se com a largura da janela — três, duas ou uma coluna —, e não há
deslocamento lateral. As distribuições, o número de realizações e a semente são gravados no
projeto e regressam ao reabri-lo; os resultados não, porque se refazem iguais com a mesma semente.

O tempo cresce com o número de realizações, de volumes e de anos de chuva. Cada realização refaz a
cadeia técnica, económica, ambiental e TOPSIS para todos os volumes; a aceitabilidade SMAA-VIKOR
(secção {{n:32}}), que sorteia vinte mil vetores de pesos, fica de fora das realizações, porque a
modulação só usa o vencedor do TOPSIS. No tutorial, com 21 volumes e trinta anos de chuva, a barra
de progresso estima o tempo restante a partir das primeiras realizações. O botão **Exportar
(CSV + JSON)** grava as amostras, uma linha por realização, e o resumo completo, com a semente e as
distribuições.

## Na linha de comandos

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
