# O que há de novo em cada versão do Triton

Este arquivo é **gerado** do capítulo de histórico do manual do usuário
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz as mesmas seções: o resumo em uma frase, as novidades, **as
correções que alteram resultados de estudos já feitos**, as que não alteram e o
que mudou na documentação. A distinção entre os dois tipos de correção é a que
mais importa para quem publica com o programa: uma correção de cálculo obriga a
declarar a versão usada num trabalho; uma correção de interface, não.

A versão atual é a 0.1.0. O manual completo está em `manual/Manual-Triton.pdf`
e o site de documentação, em `manual/site/index.html`.

---

## Versão 0.1.0 (beta) — 15 de outubro de 2026

> **Em uma frase.** Primeira versão beta do Triton, programa derivado do Netuno 5.0.1, com
> nome, versionamento e repositório próprios para cada edição; a 1.0.0, a primeira oficial, virá depois.

### Novidades

O Triton é o filho do Netuno. Mantém o motor de simulação, a avaliação de ciclo de vida, a linha de
tratamento, a decisão multicritério e a modulação probabilística do Netuno 5.0.1, e passa a ser
distribuído em três programas independentes, um por edição: Brasil, Internacional e Portugal. Cada um
tem repositório, logo e numeração próprios, e esta é a primeira versão de todos: 0.1.0, ainda em beta.

O histórico do Netuno (versões 5.0.0 e 5.0.1) continua no manual do Netuno. O Triton 0.1.0 já inclui as
correções feitas até o Netuno 5.0.1, entre elas a da demanda mensal e semanal igual a zero, e a regra de
operação de Fewkes (φ) como opção em todos os módulos.

Na Edição Brasil, a base de tarifas de 652 municípios traz 617 conferências de conta, das quais 241 corrigidas, registradas em `tarifas/transcricoes/ALTERACOES.md`.

### Correções que alteram resultados

Nenhuma em relação ao Netuno 5.0.1, de que o Triton 0.1.0 parte.

| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

O nome, o logo, o pacote (`triton`) e a extensão dos arquivos de projeto (`.triton`) mudaram; o cálculo não.

---
