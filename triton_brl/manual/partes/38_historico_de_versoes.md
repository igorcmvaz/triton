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

A versão 1.0.0 é o primeiro lançamento público do Triton. Os números anteriores a
ela foram de desenvolvimento, e nunca chegaram a circular; nenhum estudo foi feito com
eles.

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

## Versão 1.0.0 — 14 de outubro de 2026

> **Em uma frase.** Primeiro lançamento oficial do Triton, programa derivado do Netuno 5.0.1, com
> nome, versionamento e repositório próprios para cada edição.

### Novidades

O Triton é o filho do Netuno. Mantém o motor de simulação, a avaliação de ciclo de vida, a linha de
tratamento, a decisão multicritério e a modulação probabilística do Netuno 5.0.1, e passa a ser
distribuído em três programas independentes, um por edição: Brasil, Internacional e Portugal. Cada um
tem repositório, logo e numeração próprios, e esta é a primeira versão de todos: 1.0.0.

O histórico do Netuno (versões 5.0.0 e 5.0.1) continua no manual do Netuno. O Triton 1.0.0 já inclui as
correções feitas até o Netuno 5.0.1, entre elas a da demanda mensal e semanal igual a zero, e a regra de
operação de Fewkes (φ) como opção em todos os módulos.

Na Edição Brasil, a base de tarifas de 652 municípios traz 617 conferências de conta, das quais 241 corrigidas, registradas em `tarifas/transcricoes/ALTERACOES.md`.

### Correções que alteram resultados

Nenhuma em relação ao Netuno 5.0.1, de que o Triton 1.0.0 parte.

<!-- tabela: Correções que alteram resultados na versão 1.0.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

O nome, o logo, o pacote (`triton`) e a extensão dos arquivos de projeto (`.triton`) mudaram; o cálculo não.

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
