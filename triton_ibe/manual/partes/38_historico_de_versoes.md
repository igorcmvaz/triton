# Histórico de versões e o que mudou

Esta secção regista o que mudou entre as versões do programa e, sobretudo, **que mudanças alteram
resultados já publicados**. A distinção importa mais do que parece: uma correção de interface não
afeta nenhum estudo anterior, ao passo que uma correção de cálculo pode deslocar cada número de um
trabalho já submetido. Quem publicou com o Triton precisa de saber em que categoria cai cada
alteração, e é por isso que o histórico abaixo separa as duas coisas de forma explícita.

==A regra que orienta toda esta secção é simples: uma correção de cálculo obriga a declarar a
versão usada; uma correção de interface, não.==

---

## A versão que está a usar

O número da versão aparece na barra lateral, no rodapé e no menu **Sobre o Triton**. É também
gravado dentro de cada ficheiro de projeto e impresso em cada relatório, de modo que um estudo
antigo leva sempre consigo a identificação do programa que o produziu. Esta redundância é
deliberada: os relatórios circulam separados dos ficheiros, e a pergunta «com que versão foi isto
feito?» costuma surgir meses depois, quando já ninguém se lembra.

O esquema de numeração segue a convenção corrente em engenharia de software. O primeiro número
indica a geração do programa, e a sua mudança significa uma reformulação do modelo conceptual; o
segundo indica um conjunto de funcionalidades novas; e o terceiro indica correções e ajustes que
não alteram a arquitetura. Um primeiro número igual a zero marca uma versão beta: o programa é
utilizável e está verificado como a secção {{n:34}} descreve, mas a interface, o formato de
ficheiro e os valores por omissão ainda podem mudar, e uma mudança pode alterar resultados.

A versão atual é a beta **0.1.0**. Nenhuma versão anterior circulou, e nenhum estudo foi feito com
alguma.

---

## Como este histórico é mantido

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

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Versão 0.1.0 (beta) — 15 de outubro de 2026

> **Numa frase.** Primeira versão beta do Triton, com nome, numeração e repositório próprios para
> cada edição.

### Novidades

O Triton simula o aproveitamento de águas pluviais dia a dia e inclui o motor de simulação, a
avaliação de ciclo de vida, a linha de tratamento, a decisão multicritério e a modulação
probabilística. Esta é a primeira versão da Edição Ibérica (IBE, antes Edição Portugal), que tem repositório, logótipo e
numeração próprios, com a chuva E-OBS por concelho, os tarifários de Lisboa, do Porto e do Funchal
e os valores em euros. A regra de operação de Fewkes (φ) está disponível como opção em todos os
módulos.

### Correções que alteram resultados

Nenhuma: esta é a primeira versão beta, e não há versão anterior a corrigir.

<!-- tabela: Correções que alteram resultados na versão 0.1.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

Nenhuma.

---

## Como saber se a sua versão tem uma correção

O procedimento é direto e não depende de consultar ninguém: abra um dos ficheiros de exemplo que
acompanham o programa, descritos no apêndice {{n:J}}, execute-o e compare o resultado obtido com o
valor impresso neste manual. Cada caso de exemplo foi gerado pela mesma versão do programa que
gerou este manual, e cada número publicado tem a verificação automática correspondente, como a
secção {{n:34}} descreve. Uma divergência, portanto, indica que o programa instalado não é o da
versão deste manual.

==Se os números coincidirem, a sua instalação corresponde exatamente ao manual que tem em mãos.==
Se não coincidirem, a diferença não é um defeito da sua instalação, mas uma diferença de versão que
é preciso identificar antes de qualquer estudo.

---

## O que declarar num trabalho publicado

A boa prática de reprodutibilidade computacional exige que um trabalho identifique de forma
inequívoca o programa que produziu os resultados. No caso do Triton, bastam quatro informações, e
todas estão disponíveis sem esforço: a versão do programa, que aparece no relatório; a origem da
série de precipitação, com o período utilizado; a estrutura tarifária adotada, com a data de
entrada em vigor; e a declaração de quais os parâmetros alterados em relação aos valores por
omissão. A secção {{n:13}} traz a lista completa, com um parágrafo de método pronto a adaptar.

Anexar o ficheiro `.triton` ao material suplementar resolve as quatro de uma só vez, porque o
ficheiro é autocontido: traz a série de chuva dentro dele ou, com a chuva E-OBS por concelho, a
referência da série e a sua impressão digital, que o programa recompõe a partir da base. É a forma
mais económica de tornar um estudo verificável por terceiros, e custa um pequeno anexo.
