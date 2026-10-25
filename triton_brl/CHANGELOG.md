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

## Versão 0.1.0 (beta) — 24 de outubro de 2026

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
- **Custos.** O CAPEX e o OPEX de um projeto novo são calculados automaticamente a partir do catálogo de referência, em reais (seção 4.7); o usuário pode digitar os seus valores.
- **Normas.** A ABNT NBR 15527:2019 no que ela fixa (seção 4.6), e a comparação com a EN 16941-1:2024 em `docs/normas_nbr_x_en16941.md`.
- **Documentação.** O manual completo em português do Brasil, o site de documentação, volumes curtos e `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e qualidade.

**O que a versão ainda não tem.**

- Série de chuva **medida**: as séries da base e as dos exemplos são do CLIMBra, isto é, modeladas e com correção de viés, e não registros de pluviômetro.
- Tarifa de energia com tributos e bandeiras: o valor é o da B1 sem ICMS, PIS/Pasep, Cofins, COSIP nem bandeira, e 140 municípios têm a referência de energia expirada (guardam o último valor oficial, marcado).
- Estrutura tarifária conferida nos cinco municípios do Tocantins (grau C).
- Fonte e data registradas para todos os preços de referência do CAPEX: só os preços de reservatório as têm.

**Limitações conhecidas.**

- O custo anual que o resumo da análise mostra soma só a energia, o cloro e a linha de tratamento; as rotinas de manutenção entram no fluxo de caixa à parte (seção 4.7).
- Em espanhol e em chinês, a interface está traduzida em parte e os laudos saem com trechos em português; o português e o inglês estão completos.
- Em janelas estreitas, alguns cabeçalhos de tabela aparecem cortados.
- A licença de reutilização dos portais dos prestadores, a das planilhas do Netuno 4 e a do logotipo do CLIMBra não foram verificadas; a base aberta da ANEEL declara a ODbL e o fator do MCTI/SIRENE, o CC BY-ND 3.0 para o site. Em 25/10/2026 o titular aprovou o uso dos JSON extraídos da ANEEL e do MCTI/SIRENE, com atribuição, e manteve as planilhas do Netuno 4 e o logotipo do CLIMBra, com a autorização dos criadores registada pelo titular (sem documento anexo); ver `docs/DADOS.md`.
- O metadado `source_article` dentro das 19 partes do CLIMBra ainda diz «art. 48»; o artigo é Scientific Data 10, art. 47. O texto corrigido está no programa e na documentação, e as partes serão regeradas quando houver outra razão.

### Correções que alteram resultados

Nenhuma em relação ao Netuno 5.0.1, de que o Triton 0.1.0 parte.

| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

O nome, o logo, o pacote (`triton`) e a extensão dos arquivos de projeto (`.triton`) mudaram; o cálculo não.

### Documentação

O manual ganhou as seções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice E, e o texto sobre a base CLIMBra passou a descrever os 19 bancos por modelo e a origem das séries de exemplo (recortes do CLIMBra, e não do INMET).

---
