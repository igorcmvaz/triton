# Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

## Ficha 1 — O fluxo de um estudo completo

```
1. Projeto e chuva ......... série, área, coeficiente, descarte      cap. 4
2. Edificação .............. tipologia, demanda, fração atendível    cap. 5
3. Primeira simulação ...... um volume de palpite, para ver          cap. 6
4. Varredura ............... curva de retorno, volume ideal          cap. 7
5. Arranjo ................. precisa de caixa superior?              cap. 8
6. Qualidade ............... classe, desinfecção, filtros            cap. 9
7. Economia ................ tarifa real, CAPEX, fluxo de caixa      cap. 10
8. Carbono ................. inventário, material, payback           cap. 11
9. Decisão ................. sete critérios, pesos declarados        cap. 12
10. Relatório .............. saídas e lista de declaração            cap. 13
```

**Antes de publicar:** seção {{n:13}}, a lista de declaração. Capítulo 33, os dez
enganos. Capítulo 36, as limitações que afetam o seu caso.

---

## Ficha 2 — As armadilhas, em uma linha cada

<!-- tabela: Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada -->
| Armadilha | Onde |
| :--- | :--- |
| área **inclinada** em vez da projeção horizontal | 33.1 |
| chuva **média mensal** em vez da série diária | 33.2 |
| descarte em **litros** quando o campo quer milímetros | 33.3 |
| **regime de mínimo** tarifário ignorado | 33.4 |
| escola ou hospital com **tarifa residencial** | 33.5 |
| esperar mais **água** da caixa superior | 33.6 |
| **série curta** demais | 33.7 |
| classe de qualidade escolhida pelo **custo** | 33.8 |
| comparar com o **Netuno 4** sem declarar a divergência | 33.9 |
| publicar o volume de **maior economia** como recomendado | 33.10 |

---

## Ficha 3 — Os cinco regimes tarifários

<!-- tabela: Ficha de consulta: os cinco regimes tarifários e o efeito da economia -->
| Regime | Ao economizar | Municípios |
| :--- | :--- | ---: |
| sem mínimo | cada m³ desconta | 165 |
| disponibilidade | cada m³ desconta; o fixo continua | 156 |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** | **329** |
| franquia retroativa | passando dela, tarifa tudo desde zero | 2 |
| piso de pagamento | a conta não desce abaixo do piso | 0 |

**Teste rápido:** simule dois consumos, um dentro e um fora da faixa mínima, e
compare com uma conta real. Se só um bater, o regime está errado.

---

## Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | demanda **total** | quanto da conta cai |
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

**Volume:** critério de escolha — limiar de ganho marginal, ou pesos do
multicritério.

**Economia:** município, concessionária, vigência da tabela, **regime de mínimo**,
percentual de esgoto, TMA, inflação, reajustes e período.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no EDGE, que só a
barra de água foi avaliada.
