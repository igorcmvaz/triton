# Histórico de versões e o que mudou

Esta seção registra o que mudou entre as versões do programa e, sobretudo, **quais
mudanças alteram resultados já publicados**. A distinção importa mais do que parece:
uma correção de interface não afeta nenhum estudo anterior, ao passo que uma correção
de cálculo pode deslocar cada número de um trabalho já submetido. Quem publicou com o
Triton precisa saber em que categoria cada alteração se encaixa, e é por isso que o
histórico abaixo separa as duas coisas de forma explícita.

==A regra que orienta toda esta seção é simples: correção de cálculo obriga a
declarar a versão usada; correção de interface, não.==

---

## A versão que você está usando

O número da versão aparece na barra lateral, no rodapé, e no menu **Sobre o Triton**.
Ele também é gravado dentro de cada arquivo de projeto e impresso em cada relatório,
de modo que um estudo antigo sempre carrega consigo a identificação do programa que o
produziu. Essa redundância é deliberada: relatórios circulam separados dos arquivos, e
a pergunta «com que versão isto foi feito?» costuma aparecer meses depois, quando
ninguém lembra.

O esquema de numeração segue a convenção corrente em engenharia de software. O
primeiro número indica a geração do programa, e sua troca significa reformulação do
modelo conceitual; o segundo indica um conjunto de funcionalidades novas; e o terceiro
indica correções e ajustes que não alteram a arquitetura. A passagem do Netuno 4 para
o Triton, tratada na seção {{n:35}}, é o único caso de troca do primeiro número na
história do programa.

A versão 0.1.0 é a primeira versão pública do Triton e é um beta: o programa ainda está em
desenvolvimento, e a numeração sobe (0.2.0, 0.3.0 e assim por diante) até a 1.0.0, que será a
primeira versão oficial. Os números anteriores à 0.1.0 foram de desenvolvimento, e nunca chegaram
a circular; nenhum estudo foi feito com eles.

---

## Como este histórico é mantido

Daqui em diante, cada versão publicada ganha uma entrada própria nesta seção, com a
data do lançamento e o que mudou, sempre separado em duas listas: ==o que altera
resultados de estudos já feitos e o que não altera.== A entrada mais recente vem
primeiro.

Cada entrada segue o mesmo modelo, para que duas versões possam ser comparadas sem
releitura: uma frase de resumo, as novidades, as correções que alteram resultados, as
que não alteram, e o que mudou na documentação. Seções sem conteúdo naquela versão
simplesmente não aparecem.

A mesma lista é distribuída com o código, no arquivo `CHANGELOG.md` da raiz do
repositório, e alimenta a página de versões do site de documentação. Ela não é escrita
três vezes: os três saem desta seção, e uma verificação automática recusa a montagem se
divergirem. Quem acompanha o programa pelo repositório, pelo site ou pelo manual lê o
mesmo registro.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Versão 0.1.0 (beta) — 5 de novembro de 2026

> **Em uma frase.** Primeira versão beta do Triton, programa derivado do Netuno 5.0.1, com
> nome próprio para cada edição, com o mesmo repositório e a mesma numeração; a 1.0.0, a primeira oficial, virá depois.

### Novidades

O Triton é o filho do Netuno. Mantém o motor de simulação, a avaliação de ciclo de vida, a linha de
tratamento, a decisão multicritério e a modulação probabilística do Netuno 5.0.1, e passa a ser
distribuído em três programas independentes, um por edição: Brasil, Internacional e Ibérica. Cada um
tem nome e logo próprios e todos compartilham o repositório e a numeração; esta é a primeira versão de todos: 0.1.0, ainda em beta.

O histórico do Netuno (versões 5.0.0 e 5.0.1) continua no manual do Netuno. O Triton 0.1.0 já inclui as
correções feitas até o Netuno 5.0.1, entre elas a da demanda mensal e semanal igual a zero, e a regra de
operação de Fewkes (φ) como opção em todos os módulos.

**O que a Edição Brasil traz nesta versão.**

- **Chuva.** A base CLIMBra para 652 municípios, 19 modelos do CMIP6 e três simulações (histórica, SSP2-4.5 e SSP5-8.5): 37.164 séries diárias, em 19 bancos, um por modelo (785,1 MiB, cada um abaixo de 50 MiB), com o SHA-256 de cada parte em `data/climbra_partes.json`.
- **Tarifas.** Água e esgoto de 652 municípios, por prestador, com 617 conferências de conta, das quais 241 corrigidas, e grau de confiança por município: 584 de grau A, 63 de B e 5 de C. Energia B1 da ANEEL por distribuidora. As conferências estão registradas em `tarifas/transcricoes/ALTERACOES.md`.
- **Custos.** O CAPEX e o OPEX de um projeto novo são calculados automaticamente a partir do catálogo de referência, em reais (seção {{n:10}}); o usuário pode digitar os seus valores.
- **Normas.** A ABNT NBR 15527:2019 no que ela fixa (seção {{n:9}}), e a comparação com a EN 16941-1:2024 em `docs/normas_nbr_x_en16941.md`.
- **Estudos em lote por JSON.** O subcomando `triton estudo` organiza um estudo num `estudo.json` (projeto base, casos por tipologia, substituições de parâmetros por apelidos, análise e saídas), roda todos os casos em ordem estável, com retomada e execução paralela, e grava tabelas para artigos: CSV tidy, JSON com proveniência (versão, edição, SHA-256, fonte e licença da chuva), Markdown, LaTeX (booktabs) e XLSX. Um modelo de texto com marcadores recebe os números reais e deixa «XX» onde faltar resultado. Há um estudo de exemplo em `examples/estudos/`.
- **Documentação.** O manual completo em português do Brasil, o site de documentação, volumes curtos e `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e qualidade.

**O que a versão ainda não tem.**

- Série de chuva **medida**: as séries da base e as dos exemplos são do CLIMBra, isto é, modeladas e com correção de viés, e não registros de pluviômetro.
- Tarifa de energia com tributos e bandeiras: o valor é o da B1 sem ICMS, PIS/Pasep, Cofins, COSIP nem bandeira, e 140 municípios têm a referência de energia expirada (guardam o último valor oficial, marcado).
- Estrutura tarifária conferida nos cinco municípios do Tocantins (grau C).
- Fonte e data registradas para todos os preços de referência do CAPEX: só os preços de reservatório as têm.

**Limitações conhecidas.**

- O custo anual que o resumo da análise mostra soma só a energia, o cloro e a linha de tratamento; as rotinas de manutenção entram no fluxo de caixa à parte (seção {{n:10}}).
- Em espanhol e em chinês, a interface está traduzida em parte e os laudos saem com trechos em português; o português e o inglês estão completos.
- Em janelas estreitas, alguns cabeçalhos de tabela aparecem cortados.
- A licença de reutilização dos portais dos prestadores, a das planilhas do Netuno 4 e a do logotipo do CLIMBra não foram verificadas; a base aberta da ANEEL declara a ODbL e o fator do MCTI/SIRENE, o CC BY-ND 3.0 para o site. Em 25/10/2026 o titular aprovou o uso dos JSON extraídos da ANEEL e do MCTI/SIRENE, com atribuição, e manteve as planilhas do Netuno 4 e o logotipo do CLIMBra, com a autorização dos criadores registada pelo titular (sem documento anexo); ver `docs/DADOS.md`.
- O metadado `source_article` dentro das 19 partes do CLIMBra ainda diz «art. 48»; o artigo é Scientific Data 10, art. 47. O texto corrigido está no programa e na documentação, e as partes serão regeradas quando houver outra razão.

### Correções que alteram resultados

Nenhuma em relação ao Netuno 5.0.1, de que o Triton 0.1.0 parte.

<!-- tabela: Correções que alteram resultados na versão 0.1.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

O nome, o logo, o pacote (`triton`) e a extensão dos arquivos de projeto (`.triton`) mudaram; o cálculo não.

### Documentação

O manual ganhou as seções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice {{n:E}}, e o texto sobre a base CLIMBra passou a descrever os 19 bancos por modelo e a origem das séries de exemplo (recortes do CLIMBra, e não do INMET).

---

## Como saber se a sua versão tem uma correção

O procedimento é direto e não depende de consultar ninguém: abra um dos arquivos de
exemplo que acompanham o programa, descritos no apêndice {{n:J}}, rode-o, e compare o
resultado obtido com o valor impresso neste manual. Cada caso de exemplo foi gerado
pela mesma versão do programa que gerou este manual, e cada número publicado tem
verificação automática correspondente, conforme a seção {{n:34}} descreve. Uma
divergência, portanto, indica que o programa instalado não é o da versão deste manual.

==Se os números baterem, a sua instalação corresponde exatamente ao manual que você
tem em mãos.== Se não baterem, a diferença não é um defeito da sua instalação, e sim
uma diferença de versão que precisa ser identificada antes de qualquer estudo.

---

## O que declarar num trabalho publicado

A boa prática de reprodutibilidade computacional exige que um trabalho identifique de
modo inequívoco o programa que produziu os resultados. No caso do Triton, quatro
informações bastam, e todas estão disponíveis sem esforço: a versão do programa, que
aparece no relatório; a origem da série de precipitação, com o período utilizado; a
estrutura tarifária adotada, com a data de vigência; e a declaração de quais parâmetros
foram alterados em relação aos valores padrão. A seção {{n:13}} traz a lista completa,
com um parágrafo de método pronto para ser adaptado.

Anexar o arquivo `.triton` ao material suplementar resolve as quatro de uma vez, porque
o arquivo é autocontido e traz a série de chuva dentro dele, ou, com a chuva da base
CLIMBra, a referência da série com a sua impressão digital. É a forma mais econômica de
tornar um estudo verificável por terceiros, e custa um anexo de cerca de 160 kB — bem
menos com a CLIMBra.
