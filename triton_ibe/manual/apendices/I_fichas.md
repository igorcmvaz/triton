# Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

## Ficha 1 — O fluxo de um estudo completo

<!-- tabela: Ficha de consulta: os dez passos de um estudo completo e a secção que trata de cada um -->
| # | Passo | O que se decide nele | Secção |
| ---: | :--- | :--- | ---: |
| 1 | Projeto e chuva | série, área, coeficiente, descarte | {{n:4}} |
| 2 | Edificação | tipologia, procura, fração atendível | {{n:5}} |
| 3 | Primeira simulação | um volume de palpite, para ver | {{n:6}} |
| 4 | Varrimento | curva de retorno, volume ideal | {{n:7}} |
| 5 | Arranjo | precisa de reservatório superior? | {{n:8}} |
| 6 | Qualidade | classe, desinfeção, filtros | {{n:9}} |
| 7 | Economia | tarifa real, CAPEX, fluxo de caixa | {{n:10}} |
| 8 | Carbono | inventário, material, período de recuperação | {{n:11}} |
| 9 | Decisão | oito critérios em quatro eixos, pesos declarados | {{n:12}} |
| 10 | Relatório | saídas e lista de declaração | {{n:13}} |

**Antes de publicar:** secção {{n:13}}, a lista de declaração. Secção {{n:33}}, os dez erros. Secção {{n:36}}, as limitações que afetam o seu caso.

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
| esperar mais **água** do reservatório superior | {{n:33.6}} |
| **série curta** demais | {{n:33.7}} |
| classe de qualidade escolhida pelo **custo** | {{n:33.8}} |
| comparar com **outro programa** sem declarar as diferenças de método | {{n:33.9}} |
| publicar o volume de **maior economia** como recomendado | {{n:33.10}} |

---

## Ficha 3 — Os seis regimes tarifários

<!-- tabela: Ficha de consulta: os seis regimes tarifários e o efeito de poupar -->
| Regime | Ao poupar |
| :--- | :--- |
| sem mínimo | cada m³ desconta |
| tarifa de disponibilidade | cada m³ desconta; a parte fixa mantém-se |
| fórmula exponencial | cada m³ desconta; a conta é PB × Cⁿ + serviço básico |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** |
| franquia retroativa | passando-a, cobra tudo desde zero |
| piso de pagamento | a fatura não fica abaixo do piso |

**Teste rápido:** simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os com uma fatura
real. Se só um coincidir, o regime está errado.

Os tarifários de Lisboa, do Porto e do Funchal têm a estrutura da tarifa de disponibilidade com escalões
progressivos (apêndice {{n:D}}).

---

## Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | procura **total** | quanto do consumo de água potável cai |
| fiabilidade volumétrica | procura **pluvial** | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | dias da série | com que frequência se pode contar |
| extravasamento | — | o reservatório é pequeno? |
| ganho marginal | — | vale ampliar? |

`Epot = fiabilidade volumétrica × fração atendível`

---

## Ficha 5 — A cadeia de energia da eletrobomba

```
elevação:  e = ρ · g · H ÷ (η_bomba · η_motor)      kWh/m³
partidas:  E = placa × tempo ÷ η_motor              kWh
```

A placa é a potência **no eixo**. O rendimento do motor separa o eixo da tomada. Se o deixar
em branco, vale o valor típico para a potência nominal; introduza o rendimento do seu motor quando
tiver a ficha técnica.

---

## Ficha 6 — A lista de declaração, resumida

**Programa:** versão, com revisão.

**Chuva:** origem, recorte, anos; se projeção, modelo, cenário e janela.

**Edificação:** área e como foi obtida, coeficiente, per capita e origem, **fração
atendível** e os usos que a compõem.

**Descarte:** lâmina e modo; e a diferença de método, se comparar programas.

**Volume:** critério de escolha — limiar de ganho marginal, ou os quatro pesos
de eixo, as partes no eixo e os candidatos do multicritério.

**Economia:** concelho, entidade gestora, vigência da tabela, **regime de mínimo**,
regra do saneamento, taxas de IVA de cada parcela, taxa de atualização, inflação, atualizações e período, e a moeda.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores **aproximados** ou com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no LEED, a versão; no EDGE, que só a
barra de água foi avaliada.
