# Como rodar

> **Pergunta que esta seção responde:** quais são os passos, na tela e na linha de
> comando?

## Na interface

A ferramenta fica no fim da barra lateral, em **13. Modulação Probabilística**, nas duas
edições. Ela parte do estudo que as etapas 1 a 4 descrevem — a mesma configuração que o
programa grava no arquivo `.triton` —, com os pesos do TOPSIS (os quatro pesos de eixo e as partes no eixo) e as premissas
ambientais da tela. Com o perfil do CRITIC, os pesos objetivos são recalculados em cada realização, dos resultados sorteados. Sem série de chuva carregada, a ferramenta avisa e não roda. Para começar, abra o
caso `10_modulacao_tutorial.triton` ou o `11_modulacao_climbra.triton` (apêndice J): os
dois chegam com a ferramenta montada, e basta clicar em **Simular**.

As distribuições partem da triagem do estudo aberto. Ao abrir outro projeto, ou ao mudar
uma premissa nas etapas 1 a 4, os cartões que não foram editados acompanham o novo valor;
os editados ficam como estão. Num estudo de volume fixo, a ferramenta mostra só o volume do
estudo: as figuras e a tabela por volume pedem a varredura da etapa 4.

A tela tem quatro blocos, de cima para baixo:

1. **O que variar.** As vinte variáveis, em sete grupos, com caixas de marcar. Passar o
   cursor sobre uma delas mostra o que ela representa. Abaixo dos grupos, na Edição
   Brasil, a lista dos dezenove modelos climáticos, com os botões **Marcar todos** e
   **Desmarcar todos** (seção {{n:41}}).
2. **Distribuições.** Um cartão por variável marcada, com o valor do estudo, a
   distribuição, os parâmetros, os limites e a curva. O botão **Valores de triagem**
   devolve todas as distribuições ao padrão centrado no projeto.
3. **Execução.** O número de realizações (1.000 por padrão), a semente (42) e a variação
   diária opcional. **Simular** roda em segundo plano, com barra de progresso, tempo
   restante e botão **Cancelar**; cancelada, a análise mostra as realizações já feitas.
4. **Resultados.** Tabelas e figuras numeradas, explicadas na seção {{n:43}}.

O layout se reorganiza com a largura da janela — três, duas ou uma coluna —, e não há
rolagem lateral. As distribuições, os modelos marcados, o número de realizações e a
semente são gravados no projeto e voltam ao reabri-lo; os resultados não, porque se refazem iguais com a mesma
semente.

O tempo cresce com o número de realizações, de volumes e de anos de chuva. Cada
realização refaz a cadeia técnica, econômica, ambiental e TOPSIS para todos os volumes; a
aceitabilidade SMAA-VIKOR (seção {{n:32}}), que sorteia vinte mil vetores de pesos, fica de
fora das realizações, porque a modulação só usa o vencedor do TOPSIS. No tutorial, com 21
volumes e trinta anos de chuva, as mil realizações levam cerca de meio minuto no computador
em que este manual foi gerado; a barra de progresso dá a estimativa do tempo restante. O botão **Exportar (CSV + JSON)** grava as amostras, uma linha por
realização, e o resumo completo, com a semente e as distribuições.

## Na linha de comando

O comando `probabilistic-study` usa o mesmo núcleo da tela e dá os mesmos números com o mesmo
projeto e a mesma semente:

```
triton probabilistic-study 02_tutorial_varredura.triton --samples 1000 --seed 42
triton probabilistic-study 02_tutorial_varredura.triton --list-variables
triton probabilistic-study projeto.triton --var fator_chuva=normal:1:0,1 --var fator_investimento=lognormal:1:0,15
triton probabilistic-study projeto.triton --var fator_cisterna=lognormal:1:0,15 --var fator_om=lognormal:1:0,25
triton probabilistic-study projeto.triton --climate-models todos
triton probabilistic-study projeto.triton --format json --output modulacao.json
```

Sem opções de distribuição, o comando lê as que a tela gravou no projeto, ou, na falta
delas, os valores de triagem. `--var VARIÁVEL=DISTRIBUIÇÃO` liga qualquer variável do
catálogo e pode ser repetida; as distribuições se escrevem `normal:média:desvio`,
`lognormal:média:desvio`, `triangular:mínimo:moda:máximo`, `uniforme:mínimo:máximo` ou
`fixo`. Os atalhos `--per-capita`, `--people` e `--non-potable` valem para as três de
consumo, e `--daily-cv` para a variação diária. `--climate-models` recebe os modelos
climáticos separados por vírgula, `todos` ou `nenhum`, e pede um projeto com a chuva da
base CLIMBra; `--list-variables` lista também os nomes dos modelos. O formato `csv` grava
as amostras; o `json`, o resultado inteiro. O nome antigo do comando, `stochastic-study`,
continua aceito.
