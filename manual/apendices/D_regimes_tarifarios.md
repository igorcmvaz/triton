# Regimes tarifários

A base traz **652 municípios** com estrutura tarifária, percentual
de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída
da própria base do programa, e não transcrita.

## Os códigos de faixa

Cada linha da tabela tarifária é uma quádrupla `(mínimo, máximo, valor, código)`:

Os quatro códigos e o efeito de cada um sobre a fatura estão desenhados na seção {{n:29}}, e não se repetem aqui.


## Os cinco regimes

<!-- tabela: Distribuição dos municípios do catálogo pelos cinco regimes de mínimo -->
| Regime | Municípios | O que acontece ao economizar |
| :--- | ---: | :--- |
| **Sem mínimo** | 165 | Cada m³ economizado desconta na conta. |
| **Disponibilidade** | 156 | Valor fixo que **soma** por cima do consumo medido. Cada m³ economizado desconta. |
| **Franquia no mínimo** | 329 | O valor fixo já inclui um volume. Economizar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | 2 | Até a franquia paga-se o fixo; passando dela, tarifa-se **tudo desde zero**. |
| **Piso de pagamento** | 0 | A conta **não desce** abaixo do piso. Não soma: limita. |

> O piso de pagamento está implementado e nenhum município da base foi
> classificado nele até esta versão.

## Distribuição por unidade da federação

![Os municípios do catálogo, por unidade da federação](../figuras/fig42_uf.png)

*Figura 99 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião. São Paulo e Minas Gerais respondem sozinhos por quase um terço do catálogo.*


## Grau de confiança

Cada registro traz o grau de confiança da coleta:

<!-- tabela: Grau de confiança dos registros tarifários do catálogo -->
| Grau | Registros |
| :--- | ---: |
| A — alta | 580 |
| B — boa | 63 |
| C — estrutura a conferir | 5 |
| D — estrutura incompleta | 4 |

> **Confira sempre a data de vigência** do registro do seu município contra a
> resolução da concessionária. Tarifas são reajustadas anualmente, e a seção {{n:16}}
> ensina o teste que identifica estrutura errada.

