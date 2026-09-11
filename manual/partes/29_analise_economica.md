# Análise econômica e os regimes tarifários

> Este capítulo formaliza o fluxo de caixa e detalha os cinco regimes de mínimo
> tarifário — o dado que mais decide a viabilidade de um sistema pluvial no Brasil.

---

## A economia é a diferença entre duas contas

O programa **não** multiplica o volume poupado por uma tarifa. Ele monta duas contas
completas para cada mês da projeção e subtrai:

```equacao:economia_mensal
E_mês = F(V_tot) − F(V_pot)
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_mês` | economia obtida no mês | R$ |
| `F(·)` | função que calcula a fatura de água e esgoto para um volume | R$ |
| `V_tot` | volume mensal que a edificação consumiria sem o sistema pluvial | m³ |
| `V_pot` | volume mensal de água potável efetivamente comprado da rede | m³ |

A razão é a progressividade. O metro cúbico que se deixa de consumir é o **último**,
o mais caro, e não o médio. Num município com faixa inicial de R$ 3,08/m³ e segunda
faixa de R$ 14,31/m³, usar a tarifa média subestima a economia em mais da metade.

---

## A conta de água

Cada faixa da tabela é uma quádrupla `(mínimo, máximo, valor, código)`. O código diz
o que o valor significa:

| Código | Regime | Efeito na conta |
| ---: | :--- | :--- |
| 1 ou 0 | faixa progressiva | cobra o valor por m³ do volume **dentro** da faixa |
| −1 | disponibilidade | valor fixo que **soma** por cima do consumo medido |
| −2 | franquia retroativa | até a franquia, paga-se o fixo; passando dela, tarifa-se **tudo desde zero** |
| −3 | piso de pagamento | a conta **não desce** abaixo do valor |

Disponibilidade e piso são frequentemente confundidos, e são opostos:

- **Disponibilidade soma.** Conta de R$ 55 mais R$ 46 de disponibilidade dá R$ 101,
  e economizar R$ 15 de consumo deixa a conta em R$ 86.
- **Piso limita por baixo.** Com piso de R$ 40 e consumo tarifado de R$ 55,
  economizar até R$ 15 **não reduz nada**.

Um estudo de aproveitamento pluvial precisa enxergar essa diferença, e é por isso que
o programa a codifica explicitamente.

### Micromedição

Com `num_economias > 1`, o consumo é avaliado no patamar de **uma** unidade e o
resultado multiplicado pelo número de economias. Sem isso, um prédio de vinte
apartamentos cairia inteiro na faixa mais cara e a economia sairia grosseiramente
superestimada.

### O esgoto

```equacao:esgoto
T_esg = T_agua × s
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `T_esg` | parcela de esgoto da fatura | R$ |
| `T_agua` | parcela de água da fatura, já calculada pelas faixas progressivas | R$ |
| `s` | percentual de esgoto praticado pela concessionária | adimensional |

O percentual incide sobre a **tarifa de água**, e não sobre a fatura. Cem por cento
significa que a parcela de esgoto iguala a de água, e portanto o esgoto é **metade
da fatura**.

---

## Os cinco regimes na base

| Regime | Municípios |
| :--- | ---: |
| franquia no mínimo | 329 |
| sem mínimo | 165 |
| disponibilidade | 156 |
| franquia retroativa | 2 |
| piso de pagamento | 0 |

O piso está implementado e nenhum município da base foi classificado nele até agora.

A seção {{n:16}} traz o exemplo numérico comparando Floriano e Florianópolis, e a lição
prática: em regime de franquia, economizar abaixo da franquia não desconta nada.

---

## O investimento

```equacao:capex
CAPEX = C_cist + C_sup + C_mo + C_tub + C_ace + ( C_bomba × n_b ) + CAPEX_inc
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `CAPEX` | investimento inicial total do sistema | R$ |
| `C_cist` | custo do reservatório inferior | R$ |
| `C_sup` | custo do reservatório superior, quando houver | R$ |
| `C_mo` | custo de mão de obra de instalação | R$ |
| `C_tub` | custo da tubulação | R$ |
| `C_ace` | custo de acessórios, filtros e dispositivo de descarte | R$ |
| `C_bomba` | custo unitário da motobomba | R$ |
| `n_b` | número de motobombas, incluindo a reserva quando houver | unidade |
| `CAPEX_inc` | investimento incremental da linha de tratamento | R$ |

O último termo segue a regra incremental da seção {{n:27}}.

Os preços de reservatório vêm da base do programa, com procedência declarada. Para
volumes fora da tabela, o programa interpola linearmente; para extrapolar além da
tabela, só o faz se a regressão tiver **R² acima de 0,90**, e avisa quando não tem.

---

## O custeio anual

| Parcela | Origem |
| :--- | :--- |
| energia de bombeamento | seção {{n:28}}, com a bandeira tarifária aplicada |
| cloração | massa de **produto**, não de cloro ativo |
| ETAP | custeio incremental, sem contar a cloração duas vezes |
| custos operacionais declarados | lista livre do usuário |

A bandeira tarifária ajusta a tarifa de energia: amarela, vermelha 1, vermelha 2, ou
desconto fora de ponta na branca.

---

## A projeção mês a mês

Para cada mês `m` do período de análise:

**A inflação incide só sobre o custeio:**

```equacao:inflacao
f_inf = ( 1 + i )^( m − 1 )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `f_inf` | fator acumulado de inflação até o mês `m` | adimensional |
| `i` | taxa de inflação mensal declarada | adimensional |
| `m` | mês do fluxo de caixa, contado a partir de 1 | mês |

**Os reajustes tarifários incidem só sobre a conta, em degraus:**

```
degraus = (m − 1) ÷ intervalo_de_reajuste          (divisão inteira)
fator_água   = (1 + r_água)^degraus
fator_esgoto = (1 + r_esgoto)^degraus
fator_energia = (1 + r_energia)^degraus
```

> **Água e esgoto são reajustados por índices separados**, e não por um índice único
> sobre a conta agregada. As duas parcelas são objeto de atos distintos da
> concessionária, e tratá-las juntas indexa metade da conta pelo índice errado.

O IPTU verde, quando habilitado, entra como economia anual dividida por doze.

---

## Os indicadores

**Valor presente líquido:**

```
VPL = −CAPEX + Σ [ fluxo_m ÷ (1 + TMA)^m ]
```

**Taxa interna de retorno:** a taxa que zera o VPL. Quando não há raiz real — o que
acontece quando o fluxo nunca se torna positivo — o programa devolve nulo, em vez de
um número inventado.

**Payback descontado:** o primeiro mês em que o acumulado descontado cruza zero.

---

## As premissas frágeis

Duas merecem sensibilidade, e a seção {{n:20}} mostra como.

**O reajuste tarifário.** Cinco por cento ao ano por vinte anos multiplica a tarifa
por 2,65; três por cento, por 1,81; sete por cento, por 3,87. O VPL varia
proporcionalmente. É a premissa que mais move o resultado, e a mais incerta.

**A vida útil.** Vinte anos é a adoção padrão. Cisterna de concreto dura mais;
componentes de polietileno expostos ao sol duram menos. A vida útil entra tanto no
período de análise quanto no payback de carbono da seção {{n:30}}.
