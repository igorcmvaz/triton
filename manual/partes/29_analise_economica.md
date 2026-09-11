# Análise econômica e os regimes tarifários

> Esta seção formaliza o fluxo de caixa e detalha os cinco regimes de mínimo
> tarifário — o dado que mais decide a viabilidade de um sistema pluvial no Brasil.

---

## A economia é a diferença entre duas contas

O programa não calcula a economia multiplicando o volume poupado por uma tarifa média,
e a distinção não é de refinamento: é de ordem de grandeza. Para cada mês da projeção
ele monta duas faturas completas, uma com o consumo que a edificação teria sem o sistema
pluvial e outra com o consumo de água potável efetivamente comprado, e toma a diferença
entre elas.

```equacao:economia_mensal
E_mês = F(V_tot) − F(V_pot)
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_mês` | economia obtida no mês | R$ |
| `F(·)` | função que calcula a fatura de água e esgoto para um volume | R$ |
| `V_tot` | volume mensal que a edificação consumiria sem o sistema pluvial | m³ |
| `V_pot` | volume mensal de água potável efetivamente comprado da rede | m³ |

A razão de proceder assim está na progressividade das estruturas tarifárias brasileiras.
==O metro cúbico que se deixa de consumir é sempre o último da fatura, que é o mais
caro, e nunca o médio.== Num município cuja primeira faixa custa R$ 3,08/m³ e cuja
segunda faixa custa R$ 14,31/m³, calcular a economia pela tarifa média a subestima em
mais da metade, e o erro cresce com o consumo da edificação.

---

## A conta de água

A estrutura tarifária de cada município é representada no programa por uma sequência de
faixas, e cada faixa é uma quádrupla composta pelo volume mínimo, pelo volume máximo, por
um valor e por um código. O código é o elemento que dá sentido ao valor, porque
estruturas aparentemente semelhantes cobram de maneiras muito distintas.

<!-- tabela: Os quatro códigos de faixa e o efeito de cada um no cálculo da fatura -->
| Código | Regime | Efeito na conta |
| ---: | :--- | :--- |
| 1 ou 0 | faixa progressiva | cobra o valor por m³ do volume **dentro** da faixa |
| −1 | disponibilidade | valor fixo que **soma** por cima do consumo medido |
| −2 | franquia retroativa | até a franquia, paga-se o fixo; passando dela, tarifa-se **tudo desde zero** |
| −3 | piso de pagamento | a conta **não desce** abaixo do valor |

Dois desses regimes são frequentemente confundidos entre si, embora produzam efeitos
opostos sobre a viabilidade de um sistema pluvial. Vale examiná-los com números.

- **Disponibilidade soma.** Conta de R$ 55 mais R$ 46 de disponibilidade dá R$ 101,
  e economizar R$ 15 de consumo deixa a conta em R$ 86.
- **Piso limita por baixo.** Com piso de R$ 40 e consumo tarifado de R$ 55,
  economizar até R$ 15 **não reduz nada**.

A diferença entre os dois regimes decide se cada metro cúbico economizado gera desconto
desde o primeiro ou se a economia só começa a valer depois de vencido um patamar, e um
estudo de viabilidade que os confunda chega a conclusões invertidas. É por essa razão que
o programa codifica o regime de forma explícita, em vez de tratá-lo como detalhe da
tabela.

### Micromedição

Em edificações multifamiliares com medição individualizada, o consumo é avaliado no
patamar de uma única unidade habitacional e o resultado é multiplicado pelo número de
economias. O tratamento importa por causa da progressividade: um prédio de vinte
apartamentos tratado como consumidor único cairia inteiro na faixa mais cara da tabela, e
a economia resultante sairia grosseiramente superestimada, porque cada metro cúbico
poupado seria valorado a uma tarifa que nenhuma das vinte unidades efetivamente paga.

### O esgoto

```equacao:esgoto
T_esg = T_agua × s
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `T_esg` | parcela de esgoto da fatura | R$ |
| `T_agua` | parcela de água da fatura, já calculada pelas faixas progressivas | R$ |
| `s` | percentual de esgoto praticado pela concessionária | adimensional |

O percentual de esgoto incide sobre a parcela de água da fatura, e não sobre a fatura
total, e a confusão entre os dois denominadores dobra ou divide pela metade a parcela
calculada. Cem por cento, que é o valor praticado por boa parte das concessionárias
brasileiras, significa que a parcela de esgoto iguala a de água, e portanto que o esgoto
responde por metade da fatura total.

---

## Os cinco regimes na base

<!-- tabela: Distribuição dos 652 municípios do catálogo pelos cinco regimes de mínimo -->
| Regime | Municípios |
| :--- | ---: |
| franquia no mínimo | 329 |
| sem mínimo | 165 |
| disponibilidade | 156 |
| franquia retroativa | 2 |
| piso de pagamento | 0 |

O piso de pagamento está implementado no motor de cálculo e nenhum município da base foi
até agora classificado nele, situação que se registra aqui por transparência: a ausência
de ocorrências não significa que o regime não exista no país, e sim que o levantamento
não o encontrou entre os 652 municípios catalogados.

A seção {{n:16}} apresenta o exemplo numérico que compara Floriano e Florianópolis, do
qual decorre a lição prática mais importante desta seção: em regime de franquia,
economizar água abaixo do volume de franquia não produz desconto algum na fatura.

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

Os preços de reservatório provêm da base de custos do programa, com procedência
declarada para cada material. Quando o volume pedido não consta da tabela, o programa
interpola linearmente entre os pontos vizinhos; quando o volume excede o maior valor
tabelado, a extrapolação só é realizada se a regressão sobre os pontos conhecidos
apresentar coeficiente de determinação acima de 0,90, e o programa adverte quando esse
critério não é satisfeito, em vez de extrapolar em silêncio.

---

## O custeio anual

<!-- tabela: Parcelas do custeio anual e a origem de cada uma -->
| Parcela | Origem |
| :--- | :--- |
| energia de bombeamento | seção {{n:28}}, com a bandeira tarifária aplicada |
| cloração | massa de **produto**, não de cloro ativo |
| ETAP | custeio incremental, sem contar a cloração duas vezes |
| custos operacionais declarados | lista livre do usuário |

A bandeira tarifária ajusta a tarifa de energia conforme a condição de operação do
sistema elétrico nacional, e o programa aceita as quatro modalidades vigentes: amarela,
vermelha patamar 1, vermelha patamar 2 e branca, esta última com desconto nos períodos
fora de ponta.

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

```equacao:degraus
k = ⌊ ( m − 1 ) ÷ I ⌋
```

```equacao:reajuste
f_j = ( 1 + r_j )^k
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `k` | número de reajustes já aplicados até o mês `m` | adimensional |
| `m` | mês do fluxo de caixa, contado a partir de 1 | mês |
| `I` | intervalo entre reajustes, tipicamente 12 | mês |
| `⌊ ⌋` | parte inteira da divisão | — |
| `f_j` | fator acumulado de reajuste da parcela `j` | adimensional |
| `r_j` | taxa de reajuste da parcela `j`, que pode ser água, esgoto ou energia | adimensional |

A Equação {{eq:reajuste}} é aplicada separadamente a cada uma das três parcelas, com
taxas próprias, e é dessa separação que trata a observação seguinte.

> **Água e esgoto são reajustados por índices separados**, e não por um índice único
> sobre a conta agregada. As duas parcelas são objeto de atos distintos da
> concessionária, e tratá-las juntas indexa metade da conta pelo índice errado.

O incentivo de IPTU verde, quando o município o oferece e o usuário o habilita, entra no
fluxo de caixa como economia anual dividida por doze, o que o distribui uniformemente
pelos meses do ano. A simplificação é deliberada: o desconto é concedido de uma vez, no
lançamento anual do tributo, mas distribuí-lo evita que o fluxo de caixa apresente um
degrau que nada tem a ver com o desempenho do sistema.

---

## Os indicadores

**Valor presente líquido:**

```equacao:vpl
VPL = − CAPEX + Σ [ FC_m ÷ ( 1 + TMA )^m ]
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `VPL` | valor presente líquido do investimento | R$ |
| `CAPEX` | investimento inicial total, da Equação {{eq:capex}} | R$ |
| `FC_m` | fluxo de caixa líquido do mês `m` | R$ |
| `TMA` | taxa mínima de atratividade mensal | adimensional |
| `m` | mês do fluxo de caixa, de 1 até o fim do período de análise | mês |

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
