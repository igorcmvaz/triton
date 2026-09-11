# Fatores de emissão

Todo fator usado pela avaliação de ciclo de vida, com procedência, fronteira e grau
de confiança. O detalhamento completo, com as fontes item a item, está em
`docs/procedencia_fatores_co2.md`.

---

## Materiais de reservatório

<!-- tabela: Fatores de emissão dos materiais de reservatório, com massa e fronteira -->
| Material | Massa por m³ útil | Fator | Fronteira |
| :--- | ---: | ---: | :--- |
| polietileno de alta densidade | 22 kg/m³ | 1,612 kg CO₂e/kg | berço ao portão |
| concreto armado | 1.200 kg/m³ | 0,140 kg CO₂e/kg | berço ao portão |
| fibra de vidro | 15 kg/m³ | 3,250 kg CO₂e/kg | berço ao portão |
| aço inoxidável AISI 304 | 38 kg/m³ | 3,700 kg CO₂e/kg | berço ao portão |

A massa por metro cúbico útil é a que converte volume de reservatório em massa de
material. É ela, e não o fator, que faz o concreto dominar o inventário: 1.200 kg
por metro cúbico contra 22 do polietileno.

> **Consequência prática, demonstrada na seção {{n:11}}:** o material decide o **sinal**
> do resultado ambiental. Com concreto e vida útil de vinte anos, o sistema do
> tutorial não paga a dívida de carbono.

---

## Água potável de rede

Dezenove rotas de produção disponíveis, por macrorregião e tipo de manancial.

**A fronteira é por metro cúbico entregue na edificação**, e não por metro cúbico
produzido na estação. A conversão usa as perdas de distribuição:

<!-- tabela: Perdas de distribuição por macrorregião e volume entregue por metro cúbico produzido -->
| Macrorregião | Perdas | 1 m³ produzido entrega |
| :--- | ---: | ---: |
| Sudeste | 33,9% | 0,66 m³ |
| Sul | ~35% | ~0,65 m³ |
| Centro-Oeste | ~40% | ~0,60 m³ |
| Nordeste | ~45% | ~0,55 m³ |
| Norte | 46,9% | 0,53 m³ |

Um fator de saída de estação aplicado ao volume entregue subestima a emissão evitada
em até um terço.

---

## Rede elétrica

O fator da matriz elétrica brasileira muda **todo ano**, e um estudo sem o ano
declarado é irreprodutível. O programa traz cinco bases de referência e registra qual
foi usada.

---

## Insumos de tratamento

<!-- tabela: Fatores de emissão dos insumos de tratamento -->
| Insumo | Fator |
| :--- | ---: |
| hipoclorito de cálcio, produto | conforme cadeia única de cloração |
| lâmpada ultravioleta | energia da rede |
| gerador de ozônio | energia da rede |

A massa é de **produto**, e não de cloro ativo. Pastilhas têm cerca de 65% de cloro
ativo.

---

## Fatores com rótulo de triagem

Nem todo fator tem fonte primária. Os que não têm são marcados, e o relatório exibe a
marca.

<!-- tabela: Fatores que carregam rótulo de triagem, por ausência de fonte primária -->
| Fator | Situação |
| :--- | :--- |
| **emissão de fabricação da motobomba** | quatro dos seis valores são extrapolação aritmética a partir do valor de meio CV |

> **Num estudo publicado, declare quais fatores carregam rótulo de triagem.** Um
> inventário que apresenta todos os fatores com o mesmo grau de confiança esconde
> onde está a fragilidade.

---

## O que consultar antes de publicar

1. `docs/procedencia_fatores_co2.md`, para a fonte item a item;
2. a aba de Documentação, capítulo de avaliação de ciclo de vida, para as
   justificativas exibidas ao usuário;
3. o inventário do relatório ambiental, que lista cada item com o fator aplicado.
