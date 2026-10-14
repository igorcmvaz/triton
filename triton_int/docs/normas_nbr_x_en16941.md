# ABNT NBR 15527 / NBR 5626 × EN 16941-1:2024 — o que muda e o que o Triton faz

Este documento lista as diferenças entre as normas brasileiras que o Triton segue e a
norma europeia EN 16941-1:2024 (*On-site non-potable water systems — Part 1: Systems for
the use of rainwater*). Ele existe para a International Edition. **O modelo não muda**:
as duas edições calculam do mesmo jeito, e cada linha diz o que o programa faz.

Decisões tomadas (out/2026):

- o descarte inicial (lâmina de 2 mm) continua, também na INT;
- os coeficientes de escoamento continuam os da Edição Brasil, por material;
- o comprimento da série de chuva continua avaliado pelo método de Geraldi e Ghisi,
  sem a exigência de um número mínimo de anos.

A EN 16941-1 é uma norma licenciada. Aqui aparecem apenas os números dos itens e os
valores, sem reprodução do texto. Quem precisar do texto deve consultar a norma.

Legenda da última coluna: **=** o Triton já atende ou é compatível; **≠** o Triton faz
diferente, por decisão; **—** é tema de projeto ou de obra, fora do cálculo.

---

## 1. Escopo e usos admitidos

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Usos admitidos | NBR 15527:2019, 4.1.7: sete usos (resfriamento, bacias e mictórios, veículos, pisos, reserva de incêndio, ornamental, irrigação). Outros usos exigem estudo (4.1.8). | 5.2.1: bacias sanitárias, lavagem de roupa e jardim sem tratamento adicional, salvo se a avaliação de risco (5.9) pedir. O escopo exclui beber, preparo de alimentos e higiene pessoal. | Os usos são do usuário. O tutorial fica nos usos da NBR e trata a máquina de lavar como uso que pede estudo. | ≠ |
| Lavagem de roupa | Fora da lista; depende do 4.1.8. | Admitida como uso básico. | Disponível como uso; o manual avisa sobre a NBR. | = |
| Avaliação de risco | Não tem um item equivalente; a qualidade é tratada pela Tabela 1. | 5.9: avaliação de risco por instalação. | Não calcula. As classes de qualidade (cap. 9) servem de apoio. | — |

## 2. Captação e coeficientes

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Área de captação | NBR 15527, 3.6: projeção horizontal. | Fórmula (1): área de cada superfície, em projeção horizontal. | Projeção horizontal. | = |
| Fórmula do volume captado | 4.1.6: V = P·A·C·η, com η = 0,85 na falta de dado. | Fórmula (1): Y = Σ(A·e)·h·η, com η = 0,9 por padrão (eficiência do pré-tratamento). | V = P_efetiva·A·C, com um coeficiente único C. Não há um η separado. | ≠ |
| Coeficientes por superfície | Sem tabela; o valor é do projetista. | Tabela 2: 0,9 inclinado liso; 0,8 inclinado rugoso ou telha de concreto; 0,8 plano sem brita; 0,7 plano com brita; 0,5 telhado verde extensivo; 0,3 intensivo; 0,8 piso selado; 0,5 não selado. | Coeficientes por material do estudo da MIX Sustentável (2020): cerâmica 0,75 (padrão), metálica 0,88, fibrocimento 0,73, telhado verde 0,24, alumínio 0,70, policarbonato 0,94, concreto asfáltico 0,90, aço galvanizado 0,92. **Mantidos na INT.** | ≠ |
| Efeito combinado típico | Cerâmica: C·η ≈ 0,75 × 0,85. | Telha de concreto: e·η = 0,8 × 0,9 = 0,72. | Cerâmica: 0,75 aplicado direto. Os resultados ficam na mesma ordem de grandeza. | ≈ |

## 3. Descarte inicial e pré-tratamento

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Primeira chuva | 4.1.5: descarte de 2 mm na falta de dado local. | Não prevê lâmina de descarte. 5.2.2 exige um pré-tratamento (filtro) com eficiência ≥ 0,9 e retenção de partículas > 1 mm. | Descarte de 2 mm por padrão, com modos de aplicação configuráveis. **Mantido na INT.** | ≠ |
| Filtro | Previsto no arranjo. | 5.2.2: obrigatório, com o desempenho acima. | O arranjo inclui filtro e descarte inicial. | = |

## 4. Qualidade e tratamento

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Parâmetros de qualidade | Tabela 1: *E. coli* < 200/100 mL, turbidez < 5 uT, pH 6–9; monitoramento semestral (4.6.7). | Sem tabela de parâmetros. A qualidade decorre do uso e da avaliação de risco (5.9). | Quatro classes de qualidade próprias (cap. 9). | ≠ |
| Desinfecção | 4.6.4 a critério do projetista; com cloro, residual de 0,5 a 2,0 mg/L (4.6.5). | Só se a avaliação de risco pedir. | Desinfecção opcional (cloro, UV, ozônio) com custo e CO₂. | = |

## 5. Reservatório

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Proteção | 4.3.x: tampa, respiro telado, sem luz. | 5.3.1: proteção contra gelo e luz solar. | Arranjo com respiro telado; o gelo não é modelado. | — |
| Entrada | Freio d'água. | 5.3.7: entrada calma e proteção contra animais. | Freio d'água no arranjo. | = |
| Abertura de inspeção | — | 5.3.8: abertura ≥ 400 mm. | Não verifica. | — |
| Distância de árvores | — | 7: reservatório a ≥ 3 m de árvores. | Não verifica. | — |
| Reservatórios lado a lado | 4.5.10/4.5.11: potável e não potável a 60 cm; não potável embaixo quando sobrepostos. | Sem requisito equivalente; o que vale é a separação atmosférica. | Arranjo segue a NBR. | = |

## 6. Extravasor

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Destino | Rede pluvial, com proteção contra refluxo. | 5.3.9: preferência por infiltração ou corpo d'água; esgoto só se inevitável, com fecho hídrico e dispositivo antirrefluxo (EN 13564); tela em reservatório elevado; sem sifonamento. | Extravasor com ladrão sifonado e retenção antirrefluxo para a rede pluvial. O volume extravasado é calculado, mas o destino é do projetista. | = |

## 7. Suprimento de reserva (água potável)

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Onde entra | Na caixa superior, por separação atmosférica. | 5.4.1: em caixa de quebra, caixa intermediária ou no próprio reservatório, com o menor volume possível e alarme para falha da válvula. | Solenoide enche a caixa superior até uma boia de reserva mais baixa. | = |
| Separação atmosférica | NBR 5626:2020, 6.15.2. | 5.4.2: tipo AA (EN 13076, folga = 2·D, mín. 20 mm) ou AB (EN 13077); categoria 5 da EN 1717. | Separação atmosférica no arranjo; a dimensão não é verificada. | — |

## 8. Bombeamento e controle

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Bombas | 4.5.2 remete à NBR 5626 (6.5.11.2: duas bombas). | 5.5: proteção contra marcha a seco, registros, retenção, reserva "se necessário", operação alternada; bomba autoescorvante preferível; sucção flutuante. | Bomba reserva automática; sucção flutuante, chave de nível, retenção e registros no arranjo. | = |
| Vaso de expansão | — | 5.5.4. | Não incluso no arranjo. | — |
| Quadro e alarmes | — | 5.5.5 e 5.6. | Quadro de comando no arranjo; alarmes não modelados. | — |
| Medição | — | 5.7: hidrômetros conforme EN ISO 4064. | Hidrômetro no suprimento de reserva. | = |

## 9. Identificação

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Tubulações | 4.5.5: cor roxa e "ÁGUA NÃO POTÁVEL" a cada 3 m. | 8: identificação por cor ou faixa, conforme a regra nacional. | Exportação CAD/BIM em roxo com a legenda da NBR. | ≠ |
| Pontos de uso | 4.5.9: placa nos pontos de uso restrito. | 8: placas de "água não potável", torneira com manopla removível, placa junto ao cavalete. | Ponto não potável identificado. | = |
| Conexão cruzada | 4.5.8: proibida. | 5.4.2 e 5.8. | Arranjo sem conexão cruzada. | = |

## 10. Dimensionamento do reservatório

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Método | NBR 15527:2007, Anexo A, trazia seis métodos (Rippl, simulação, Azevedo Neto, alemão, inglês, australiano). A edição de 2019 deixa o método ao projetista. | A.2.1, método simplificado: V = min(Y_a, D_a)·dd/365, com dd = 15 (NL), 18 (IE/UK) ou 21 (DE). A.2.2, método detalhado: simulação diária. | Simulação diária (balanço hídrico) e busca do volume ideal (cap. 24). | = (detalhado) |
| Série de chuva | — | A.2.2: no mínimo 5 anos de dados diários. | Comprimento avaliado pelo método de Geraldi e Ghisi (2017–2019), por projeto, sem mínimo fixo. **Mantido na INT.** | ≠ |
| Ordem do balanço diário | — | A.3: retirada = min(demanda, volume do dia anterior). A chuva do dia só serve no dia seguinte (YAS estrito). | Entra a chuva, extravasa o excesso e depois atende a demanda com o estoque, **incluída a chuva do dia** (`triton/core/simulation.py`). Pela definição de Fewkes, fica entre YAS e YBS: o extravasamento é calculado antes do consumo (como no YAS), mas a chuva do dia já pode ser consumida. | ≠ |
| Indicador | Potencial de economia de água potável. | A.5: taxa de cobertura Cr(V); volume inicial zero. | Potencial de economia (equivale à taxa de cobertura da demanda pluvial); volume inicial zero. | = |
| Demanda por pessoa | Do projetista. | 6.1.3: 50 L/pessoa·dia para bacia e lavanderia, na falta de dado. | Demanda do projetista; perfis de uso por aparelho. | ≠ |

## 11. Comissionamento e manutenção

| Tema | NBR | EN 16941-1 | Triton | |
| :--- | :--- | :--- | :--- | :-: |
| Comissionamento | — | 9: ensaio com corante ou de pressão para provar que não há conexão cruzada. | Fora do cálculo. | — |
| Intervalos de manutenção | Monitoramento da qualidade semestral (4.6.7). | Anexo E: pré-tratamento, calhas e filtros a cada 6 meses; reservatório a cada 12; bombas a cada 6; módulo de reserva a cada 6; demais itens a cada 12. | Custos de operação anuais informados pelo usuário; não há calendário de manutenção. | — |

---

## O que isso significa para a International Edition

1. **Cálculo**: idêntico ao da Edição Brasil. A INT continua com descarte inicial,
   coeficientes por material e avaliação da série pelo método de Geraldi e Ghisi. Quem
   projeta sob a EN 16941-1 pode chegar mais perto da norma digitando o coeficiente
   e·η como valor personalizado e zerando a lâmina de descarte.
2. **Ordem do balanço**: um volume dimensionado pelo Triton tende a render uma
   cobertura um pouco maior que a do método A.2.2 da EN, porque a chuva do dia já
   atende a demanda do mesmo dia. A diferença é maior com reservatórios pequenos.
3. **Arranjo e identificação**: o arranjo sugerido e a exportação CAD/BIM seguem a NBR
   (cor roxa, legenda em português, 60 cm entre reservatórios). Para um projeto
   europeu, o projetista ajusta a identificação à regra nacional.
