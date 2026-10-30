# Comparar muitos casos de uma vez

> **Pergunta que este guia responde:** como comparar dezenas de alternativas sem refazer o
> projeto inteiro para cada uma?

O programa foi construído para comparar alternativas, e oferece três formas distintas de o
fazer. A escolha entre elas não é questão de gosto: cada forma responde a uma pergunta diferente,
e usar a errada gasta tempo sem produzir a informação desejada.

---

## As três formas

<!-- tabela: As três formas de comparar alternativas conforme o que varia entre elas -->
| Se o que muda é | Use | Onde |
| :--- | :--- | :--- |
| **só o volume da cisterna** | a varredura | etapa 4. Reservatório & Custos |
| **o volume, e quer decidir** | a tabela multicritério | etapa 8. Decisão Multicritério |
| **qualquer outro pressuposto** | projetos guardados, um por caso | ficheiro `.triton` |

A primeira é automática, a segunda também, e a terceira exige organização.

---

## A varredura: dezenas de volumes de uma só vez

Na etapa **4. Reservatório & Custos**, escolha o modo **varredura** e informe o volume máximo e
o passo. O programa simula todos os volumes da grelha e desenha a curva.

A varredura é o modo normal de trabalho, e não uma função avançada reservada a casos especiais:
é quase sempre a resposta certa, porque «que volume adotar?» é a pergunta central de todo o
projeto de aproveitamento pluvial. A secção {{n:7}} percorre uma varredura completa passo a
passo, e a secção {{n:24}} formaliza como se constrói a grelha de volumes.

O custo computacional é modesto e não justifica hesitação: uma varredura de 0 a 20 000 L com
passo de 1 000 L corresponde a vinte e uma simulações de trinta anos cada, e conclui-se em poucos
segundos num computador comum.

---

## A tabela multicritério: todos os volumes, todas as dimensões

A etapa **8. Decisão Multicritério** mostra, numa só tabela, cada volume da varredura com:

- a poupança de água e os dias de abastecimento;
- o valor atual líquido, o período de recuperação descontado e a taxa interna de rentabilidade;
- o carbono líquido no fim da vida útil e o retorno ambiental;
- a pontuação TOPSIS e a aceitabilidade SMAA-VIKOR.

É a forma mais densa de comparar alternativas que o programa oferece: dez colunas de resposta
para cada linha de volume. O **perfil de decisão** troca os pesos das dimensões e reordena a
tabela no momento. A secção {{n:32}} explica os métodos por trás.

---

## Quando muda outra coisa que não o volume

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
tarifário trocados. É o que a secção {{n:14}} compara. (Trocar a cidade troca duas coisas ao
mesmo tempo; o manual fá-lo de propósito, porque o tarifário não altera o resultado hídrico, e o
resultado hídrico é o objeto da comparação.)

> **Mude uma coisa de cada vez.** Se trocar a cidade e o tarifário em conjunto, o resultado
> muda e não há como saber qual dos dois o moveu. Parece óbvio, e é o erro mais comum nos estudos
> comparativos.

---

## Como organizar os ficheiros

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

## Quantos casos cabem

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

## A linha de comandos

A instalação do programa como pacote Python regista o comando `triton`, que executa as mesmas
rotinas de cálculo da interface gráfica sem abrir a janela; o instalador de Windows com interface
gráfica não o inclui. A linha de comandos lê ficheiros `.triton`, projetos em JSON estruturado e
um formato de texto antigo, separado por ponto e vírgula, e grava os resultados em texto, JSON,
CSV, HTML ou XLSX. É a interface indicada para estudos reprodutíveis, porque o próprio comando
documenta os pressupostos alterados.

<!-- tabela: Subcomandos da linha de comandos e finalidade de cada um -->
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
| `estudo` | organiza, roda e relata estudos em lote por JSON (`estudo.json`): vários edifícios por tipologia, com tabelas para artigos |

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
tutorial com os custos ilustrativos da secção {{n:10}}, move-se em proporção ao investimento e ao
tarifário. A modulação probabilística, descrita nos seus capítulos próprios, faz o mesmo trabalho
a partir da interface gráfica.

O subcomando `series-length` faz, sem limite de tempo de ecrã, a análise que a etapa da varredura
oferece no botão «a série de chuva é suficientemente longa?», descrita na secção {{n:24}}. Sem
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

## Estudos em lote por JSON

Quando a comparação é por **tipologia** (escolas, comerciais, residências unifamiliares e multifamiliares, hospitais, aeroportos) e o resultado vai para um artigo ou para o resumo de um congresso, manter um projeto guardado por caso e montar a folha de cálculo à mão deixa de compensar. O subcomando `estudo` da linha de comando organiza o estudo num ficheiro `estudo.json`: o projeto base, os casos, o que muda de um caso para o outro, a análise e as saídas. O programa roda todos os casos numa ordem estável e grava tabelas prontas.

```powershell
# 1. Esqueleto do estudo, com os rótulos da tipologia e nenhum valor preenchido.
triton estudo init .\escolas --tipologia escolar

# 2. Preencha escolas\estudo.json (os «XX» e null) e coloque os .triton e as séries em escolas\casos.
triton estudo validate .\escolas\estudo.json

# 3. Execute todos os casos (em ordem estável); --paralelo N usa N processos e não muda o resultado.
triton estudo run .\escolas\estudo.json --saida .\saida\escolas --paralelo 4

# 4. Refaça as tabelas sem recalcular (por exemplo, depois de mudar métricas ou casas decimais).
triton estudo resumo .\saida\escolas

# 5. Preencha o texto do resumo do congresso com os números reais.
triton estudo texto .\saida\escolas --modelo .\escolas\modelo_texto.md

# 6. Vários estudos (uma pasta com estudo*.json), com o comparativo entre tipologias.
triton estudo lote .\estudos --saida .\saida\comparativo

# 7. Reúne os resultados.csv de várias execuções numa só tabela (tipologia, caso, métrica: mínimo, média, mediana, máximo).
triton estudo consolidar .\saida --saida .\saida\consolidado
```

As tipologias (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario`) são só estrutura e rótulos: `estudo init --tipologia` grava o rótulo, o `grupo` dos casos e, num comentário, o que `usuarios` significa naquela tipologia. Nenhum número vem com a tipologia: área, demanda, utilizadores e fração vêm dos seus casos, com a fonte de cada um.

A ação `consolidar` procura todos os `resultados.csv` sob as pastas indicadas (vários estudos, lotes, execuções repetidas) e grava `consolidado.csv` e `consolidado.md` na pasta de saída: uma linha por tipologia (`grupo`), caso e métrica, com `n`, mínimo, média, mediana e máximo dos valores dos casos concluídos (`status` ok). A unidade faz parte da chave do grupo, pelo que moedas diferentes nunca se misturam. Os números têm o mesmo formato do `resultados.csv` (ponto decimal, dez algarismos significativos); a tabela em Markdown segue `--idioma`. Se o pacote opcional `duckdb` estiver instalado (extra opcional `analise`, que não faz parte do instalador), é ele que lê e agrupa os ficheiros; sem ele a biblioteca padrão faz o mesmo, e os dois caminhos dão os mesmos bytes (`--motor csv` força o segundo; `--motor duckdb` exige o pacote).

`estudo run` e `estudo lote` mostram o progresso na saída de erro. `--progresso simples` escreve uma linha por caso (`[i/N] id: ok (t s)`); `--progresso rich` desenha uma barra de progresso e precisa do pacote opcional `rich` (extra opcional `cli`; sem ele o programa avisa uma vez e usa `simples`); o padrão `auto` só usa `rich` se este estiver instalado e a saída de erro for um terminal. Os ficheiros de resultado são idênticos em bytes em qualquer modo, e `--quiet` desliga o progresso.

O que cada secção do `estudo.json` contém, os apelidos das substituições (área de captação, demanda, utilizadores, fração, volume do reservatório e outros) e os ficheiros de saída estão no apêndice «Ficheiros, pastas e formatos». O exemplo `examples/estudos/residencial-unifamiliar-exemplo/` roda a moradia do tutorial em Lisboa, no Porto e no Funchal (`portugal/lisboa.triton`, `portugal/porto.triton`, `portugal/funchal.triton`): `triton estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida saida\exemplo`.

Quando a chuva vem da E-OBS (uso restrito a pesquisa e educação não comerciais), as saídas herdam do `analyze` o aviso de licença e a citação que ele regista em `provenance`: o resumo, a `tabela.md`, a `tabela.tex` e o `resultados.json` os repetem, e o aviso sobre o uso não comercial vai primeiro. As séries ERA5 do exemplo trazem o crédito Open-Meteo (CC BY 4.0). Projetos com a chuva de outra origem (série própria) não levam o bloco da E-OBS.

> **O programa organiza; quem decide é o analista.** Nenhum campo do esqueleto vem preenchido, e um «XX» ou um `null` impede a execução. Área, demanda, número de utilizadores e fração atendível de cada edifício precisam vir de uma fonte que o estudo cite. O resumo avisa quando os custos não foram informados (CAPEX igual a zero), porque então o valor atual líquido e o retorno não são resultados.
