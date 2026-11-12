# Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

## Ficha 1 — O fluxo de um estudo completo

<!-- tabela: Ficha de consulta: os dez passos de um estudo completo e a seção que trata de cada um -->
| # | Passo | O que se decide nele | Seção |
| ---: | :--- | :--- | ---: |
| 1 | Projeto e chuva | série, área, coeficiente, descarte | {{n:4}} |
| 2 | Edificação | tipologia, demanda, fração atendível | {{n:5}} |
| 3 | Primeira simulação | um volume de palpite, para ver | {{n:6}} |
| 4 | Varredura | curva de retorno, volume ideal | {{n:7}} |
| 5 | Arranjo | precisa de caixa superior? | {{n:8}} |
| 6 | Qualidade | classe, desinfecção, filtros | {{n:9}} |
| 7 | Economia | tarifa real, CAPEX, fluxo de caixa | {{n:10}} |
| 8 | Carbono | inventário, material, payback | {{n:11}} |
| 9 | Decisão | oito critérios em quatro eixos, pesos e partes declarados | {{n:12}} |
| 10 | Relatório | saídas e lista de declaração | {{n:13}} |

**Antes de publicar:** seção {{n:13}}, a lista de declaração. Seção {{n:33}}, os dez
enganos. Seção {{n:36}}, as limitações que afetam o seu caso.

---

## Ficha 2 — As armadilhas, em uma linha cada

<!-- tabela: Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada -->
| Armadilha | Onde |
| :--- | :--- |
| área **inclinada** em vez da projeção horizontal | {{n:33.1}} |
| chuva **média mensal** em vez da série diária | {{n:33.2}} |
| descarte em **litros** quando o campo quer milímetros | {{n:33.3}} |
| **regime de mínimo** tarifário ignorado | {{n:33.4}} |
| escola ou hospital com **tarifa residencial** | {{n:33.5}} |
| esperar mais **água** da caixa superior | {{n:33.6}} |
| **série curta** demais | {{n:33.7}} |
| classe de qualidade escolhida pelo **custo** | {{n:33.8}} |
| comparar com o **Netuno 4** sem declarar a divergência | {{n:33.9}} |
| publicar o volume de **maior economia** como recomendado | {{n:33.10}} |

---

## Ficha 3 — Os seis regimes tarifários

<!-- tabela: Ficha de consulta: os seis regimes tarifários e o efeito da economia -->
| Regime | Ao economizar | Municípios |
| :--- | :--- | ---: |
| sem mínimo | cada m³ desconta | 165 |
| disponibilidade | cada m³ desconta; o fixo continua | 122 |
| fórmula exponencial (CORSAN) | cada m³ desconta; a conta é PB × Cⁿ + serviço básico | 34 |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** | **329** |
| franquia retroativa | passando dela, tarifa tudo desde zero | 2 |
| piso de pagamento | a fatura não fica abaixo do piso | 0 |

**Teste rápido:** simule dois consumos, um dentro e um fora da faixa mínima, e
compare com uma fatura real. Se só um bater, o regime está errado.

---

## Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | demanda **total** | quanto do consumo de água potável cai |
| confiabilidade volumétrica | demanda **pluvial** | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | dias da série | com que frequência se pode contar |
| extravasamento | — | o reservatório é pequeno? |
| ganho marginal | — | vale ampliar? |

`Epot = confiabilidade volumétrica × fração atendível`

---

## Ficha 5 — A cadeia de energia da motobomba

```
recalque:  e = ρ · g · H ÷ (η_bomba · η_motor)      kWh/m³
partidas:  E = placa × tempo ÷ η_motor              kWh
```

A placa é a potência **no eixo**. O rendimento do motor separa o eixo da tomada. Em
branco, vale a Tabela 13 da NBR 17094-2: 60,5% em meio CV, 69,3% em um CV.

---

## Ficha 6 — A lista de declaração, resumida

**Programa:** versão, com revisão.

**Chuva:** origem, recorte, anos; se projeção, modelo, cenário e janela.

**Edificação:** área e como foi obtida, coeficiente, per capita e origem, **fração
atendível** e os usos que a compõem.

**Descarte:** lâmina e modo; a divergência contra o Netuno 4, se comparar versões.

**Volume:** critério de escolha — limiar de ganho marginal, ou os quatro pesos de eixo e
as partes no eixo do multicritério.

**Economia:** município, concessionária, vigência da tabela, **regime de mínimo**,
percentual de esgoto, TMA, inflação, reajustes e período.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores **aproximados** ou com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no LEED, a versão; no EDGE, que só a
barra de água foi avaliada.
