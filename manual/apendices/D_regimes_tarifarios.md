# Apêndice D — Regimes tarifários

A base traz **652 municípios** com estrutura tarifária, percentual
de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída
da própria base do programa, e não transcrita.

## D.1. Os códigos de faixa

Cada linha da tabela tarifária é uma quádrupla `(mínimo, máximo, valor, código)`:

| Código | Significado |
| ---: | :--- |
| 1 ou 0 | faixa progressiva, cobra só o volume dentro dela |
| −1 | custo de disponibilidade, soma por cima |
| −2 | franquia retroativa |
| −3 | piso de pagamento |

## D.2. Os cinco regimes

| Regime | Municípios | O que acontece ao economizar |
| :--- | ---: | :--- |
| **Sem mínimo** | 165 | Cada m³ economizado desconta na conta. |
| **Disponibilidade** | 156 | Valor fixo que **soma** por cima do consumo medido. Cada m³ economizado desconta. |
| **Franquia no mínimo** | 329 | O valor fixo já inclui um volume. Economizar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | 2 | Até a franquia paga-se o fixo; passando dela, tarifa-se **tudo desde zero**. |
| **Piso de pagamento** | 0 | A conta **não desce** abaixo do piso. Não soma: limita. |

> O piso de pagamento está implementado e nenhum município da base foi
> classificado nele até esta versão.

## D.3. Distribuição por unidade da federação

| UF | Municípios |
| :--- | ---: |
| AC | 2 |
| AL | 10 |
| AM | 12 |
| AP | 2 |
| BA | 41 |
| CE | 37 |
| DF | 1 |
| ES | 10 |
| GO | 24 |
| MA | 22 |
| MG | 71 |
| MS | 6 |
| MT | 13 |
| PA | 42 |
| PB | 10 |
| PE | 33 |
| PI | 5 |
| PR | 34 |
| RJ | 37 |
| RN | 8 |
| RO | 7 |
| RR | 1 |
| RS | 43 |
| SC | 32 |
| SE | 7 |
| SP | 137 |
| TO | 5 |

## D.4. Grau de confiança

Cada registro traz o grau de confiança da coleta:

| Grau | Registros |
| :--- | ---: |
| A — alta | 580 |
| B — boa | 63 |
| C — estrutura a conferir | 5 |
| D — estrutura incompleta | 4 |

> **Confira sempre a data de vigência** do registro do seu município contra a
> resolução da concessionária. Tarifas são reajustadas anualmente, e o guia 16
> ensina o teste que identifica estrutura errada.

