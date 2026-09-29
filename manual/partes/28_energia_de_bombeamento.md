# Energia de bombeamento

> Esta seção traz a cadeia completa do eixo à tomada, e explica por que a
> potência de placa **não** é o que o medidor registra.

Três versões desta conta já existiram no programa, e as duas primeiras cometiam os enganos descritos no item «Por que a cadeia completa importa»: tratar a potência de placa como potência elétrica e descontar o rendimento da bomba duas vezes. Quem lê um estudo feito numa versão antiga precisa saber disso.

---

## A potência de placa é de eixo

A ABNT NBR 17094-2:2016 manda marcar o **rendimento** na placa de identificação do
motor, como grandeza separada da potência. Isso só faz sentido se a potência de
placa for a potência mecânica **no eixo**.

Daí a cadeia ter dois rendimentos, e não um:

<!-- tabela: Os dois rendimentos da cadeia de bombeamento e o que cada um converte -->
| Rendimento | O que converte |
| :--- | :--- |
| **da bomba**, `η_b` | potência de eixo em potência hidráulica entregue à água |
| **do motor**, `η_m` | potência elétrica da tomada em potência mecânica no eixo |

O programa pede os dois, em campos separados.

---

## As equações

**Energia específica do recalque**, por metro cúbico elevado:

```equacao:energia_especifica
e = ( ρ × g × H ) ÷ ( η_b × η_m )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `e` | consumo específico de energia por volume recalcado | kWh/m³ |
| `ρ` | massa específica da água, adotada como 1.000 | kg/m³ |
| `g` | aceleração da gravidade, adotada como 9,81 | m/s² |
| `H` | altura manométrica total do recalque | m.c.a. |
| `η_b` | rendimento hidráulico da bomba | adimensional |
| `η_m` | rendimento do motor elétrico | adimensional |

==A Equação {{eq:energia_especifica}} não depende da vazão nem da potência instalada.==
Elevar um metro cúbico de água a uma dada altura custa a mesma energia com bomba grande
ou pequena, porque o trabalho realizado é o mesmo; o que muda com a potência é o tempo
gasto para realizá-lo, e não o consumo específico.

**Quando a vazão de operação é declarada**, a forma equivalente:

```equacao:energia_por_vazao
e = P ÷ ( Q × η_m )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `e` | consumo específico de energia por volume recalcado | kWh/m³ |
| `P` | potência de placa da motobomba, que é potência de eixo | kW |
| `Q` | vazão de recalque informada ou deduzida | m³/h |
| `η_m` | rendimento do motor elétrico | adimensional |

O rendimento hidráulico da bomba não comparece na Equação {{eq:energia_por_vazao}}, e a
ausência é proposital: ele já está embutido no fato de um motor de `P` quilowatts no
eixo fazer a bomba entregar `Q` metros cúbicos por hora naquela altura. Dividir por ele
outra vez contabilizaria a perda hidráulica duas vezes.

**Vazão, quando não declarada:**

```equacao:vazao_deduzida
Q = ( P × η_b ) ÷ ( ρ × g × H )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Q` | vazão de recalque deduzida | m³/h |
| `P` | potência de placa da motobomba, que é potência de eixo | kW |
| `η_b` | rendimento hidráulico da bomba | adimensional |
| `ρ` | massa específica da água, adotada como 1.000 | kg/m³ |
| `g` | aceleração da gravidade, adotada como 9,81 | m/s² |
| `H` | altura manométrica total do recalque | m.c.a. |

**Energia das partidas:**

```equacao:energia_partida
E_part = ( P × t_part ) ÷ η_m
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_part` | energia consumida no conjunto das partidas do período | kWh |
| `P` | potência de placa da motobomba, que é potência de eixo | kW |
| `t_part` | tempo total de partida acumulado no período | h |
| `η_m` | rendimento do motor elétrico | adimensional |

O rendimento da bomba está ausente da Equação {{eq:energia_partida}} pela razão física
que a distingue das anteriores: durante a partida não há vazão útil, e portanto não há
perda hidráulica a descontar. O motor puxa energia da tomada, e é apenas isso que o
medidor da concessionária registra.

A energia anual da motobomba é a soma das duas parcelas: a do recalque efetivo, que
depende do volume elevado, e a das partidas, que depende do número de acionamentos.

```equacao:energia_anual
E_ano = e × V_rec + ( P × t_part ) ÷ η_m
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E_ano` | energia elétrica consumida pela motobomba no ano | kWh/ano |
| `e` | consumo específico de energia por volume recalcado | kWh/m³ |
| `V_rec` | volume recalcado no ano | m³/ano |
| `P` | potência de placa da motobomba, que é potência de eixo | kW |
| `t_part` | tempo total de partida acumulado no ano | h/ano |
| `η_m` | rendimento do motor elétrico | adimensional |

---

A potência de placa de uma motobomba é a potência mecânica no eixo, e não a potência elétrica registrada pelo medidor ({{fig:fig00k_energia}}). Uma motobomba de 0,5 CV (0,37 kW) com motor de rendimento 60,5% absorve da rede cerca de 0,61 kW: calcular a energia com a potência de placa subestimaria o consumo em cerca de 40%, e o custeio de energia é justamente a parcela que reduz a economia do sistema.

![A cadeia de rendimentos entre a tomada e a água elevada](../figuras/fig00k_energia.png)

*Figura 99 — Cadeia de energia do bombeamento. A potência de placa é a potência no eixo, no meio da cadeia: entre ela e o medidor de energia está o rendimento do motor, η_m, e entre ela e a potência hidráulica entregue à água está o rendimento da bomba, η_b.*

A potência hidráulica depende da altura manométrica, que soma ao desnível geométrico entre as lâminas d'água as perdas de carga do escoamento ({{fig:fig00l_manometrica}}). A perda de carga é a energia dissipada por unidade de peso do fluido e tem duas parcelas: a perda contínua, ao longo da tubulação, dada pela equação de Darcy-Weisbach, `h_f = f · (L/D) · v²/2g`, em que `f` é o fator de atrito, `L` o comprimento, `D` o diâmetro interno e `v` a velocidade média; e as perdas localizadas em conexões, registros e válvulas, `h_loc = K · v²/2g`, em que `K` é o coeficiente da singularidade. Em recalques prediais curtos, as perdas somam tipicamente de 10% a 30% do desnível geométrico.

![A altura manométrica decomposta em desnível e perdas](../figuras/fig00l_manometrica.png)

*Figura 99 — (a) Altura manométrica de um recalque predial: desnível geométrico entre as lâminas d'água da cisterna e do reservatório superior, somado às perdas de carga; (b) linha de energia ao longo de um trecho de tubulação, com a perda contínua por atrito (h_f) e as perdas localizadas em registro e cotovelo (h_loc).*

---

## O rendimento do motor, quando não informado

Vale a Tabela 13 da ABNT NBR 17094-2:2016, linha IR1, motores de dois polos — que é o que são as motobombas residenciais, a 3.450 rpm ({{fig:fig31_motores}}):

![O rendimento de motores de indução por potência e classe](../figuras/fig31_motores.png)

*Figura 99 — Rendimento mínimo de motores de indução monofásicos de dois polos, conforme a Tabela 13 da ABNT NBR 17094-2:2016. O programa adota a classe IR1 quando o projeto não informa o rendimento, por ser a de menor exigência e, portanto, a hipótese conservadora.*


Os dois valores que mais aparecem em instalação predial são o de meio CV, com
**60,5%** de rendimento na classe IR1, e o de um CV, com **69,3%**. A diferença entre
eles é de quase nove pontos percentuais, e ela se propaga inteira para o custeio de
energia, porque é o rendimento que separa a potência de eixo da potência efetivamente
puxada da rede.

Adota-se a **IR1** por ser o piso normativo e o que se encontra em motobomba de
prateleira. Quem tem motor de alto rendimento informa o valor marcado na placa.

Para potências fora da tabela, a norma manda adotar o maior dos dois rendimentos
vizinhos quando a potência estiver no ponto médio ou acima, e o menor quando estiver
abaixo.

---

## Por que a cadeia completa importa

O consumo específico do caso de referência — meio cavalo, 12 m.c.a. de altura
manométrica, 82 m³ recalcados e 98 acionamentos por ano — é de 0,1080 kWh/m³.
==Ignorar o rendimento do motor, ou descontar o rendimento da bomba duas vezes,
altera esse número em dezenas de pontos percentuais,== e esses são precisamente os dois
enganos mais frequentes em planilhas de dimensionamento.

O primeiro engano consiste em tratar a potência de placa como potência consumida na
tomada; o segundo, em aplicar o rendimento hidráulico numa conta que já parte da vazão
efetivamente entregue, o que o contabiliza duas vezes. A cadeia apresentada nesta seção
é explícita justamente para tornar ambos visíveis.

---

## O assistente de dimensionamento da motobomba

Quando a potência, a vazão e a altura manométrica da motobomba não são conhecidas, o botão *Assistente de Dimensionamento de Motobomba*, na etapa **4. Reservatório & Custos** e no diálogo econômico, estima os três valores e seleciona um modelo comercial. O assistente segue a sequência usual de dimensionamento de um recalque predial:

1. **Vazão de recalque.** `Q = V_sup ÷ t_ench`, com o volume do reservatório superior e o tempo de enchimento desejado, de 45 minutos por padrão.
2. **Diâmetro econômico.** Pela fórmula de Forchheimer, `D = 1,3 · (t_op ÷ 24)^0,25 · √Q`, com `D` em metros, `Q` em m³/s e `t_op` o tempo diário de funcionamento, de 2 h por padrão. O diâmetro adotado é o menor tubo comercial de PVC soldável cujo diâmetro interno atende ao valor calculado, e nunca inferior ao bocal da motobomba selecionada; a sucção recebe uma bitola comercial acima do recalque.
3. **Velocidade.** `v = Q ÷ (π · D_i² ÷ 4)`, destacada quando fica fora do intervalo de 0,6 m/s a 2,5 m/s.
4. **Perda de carga.** Pela fórmula de Hazen-Williams, `J = 10,643 · Q^1,852 · C^−1,852 · D_i^−4,87`, com `C = 140` para PVC, multiplicada pelo comprimento da tubulação e acrescida de 30% para as perdas localizadas.
5. **Altura manométrica e potência.** `H_man = H_geo + h_f` e `P = ρ · g · Q · H_man ÷ η`, com rendimento de conjunto de 55% por padrão.
6. **Seleção.** O primeiro modelo do catálogo interno cuja vazão, altura máxima e potência atendem ao ponto de operação, com a curva da bomba traçada contra o ponto calculado.

A altura manométrica e a perda de carga calculadas retornam ao projeto e passam a alimentar o cálculo de energia desta seção, no lugar do valor de recurso.

---

## Os valores de recurso

Usados quando o projeto não declara:

<!-- tabela: Valores de recurso adotados quando o projeto não os declara -->
| Parâmetro | Valor | Origem |
| :--- | ---: | :--- |
| altura manométrica | 12 m.c.a. | casa de dois pavimentos com cisterna enterrada: ~8 m de desnível geométrico e ~30% de perda de carga dão de 10 a 12 m; adota-se o extremo conservador |
| rendimento da bomba | 55% | motobombas residenciais de meio a um CV ficam entre 40% e 60% no ponto de operação |
| tempo de partida | 108 s | ver a ressalva abaixo |

> **Aprofundamento: a altura manométrica é o parâmetro que mais pesa.** Quem conhece o
> desnível do projeto deve informá-lo. Dobrar a altura dobra a energia.

> **Aprofundamento: o tempo de partida de 108 s.** Ele representa o tempo de escorva
> de uma bomba autoaspirante cuja linha de sucção drenou. Numa instalação com válvula
> de pé em ordem, a linha permanece escorvada e as partidas seguintes são imediatas.
> No caso de referência, as partidas respondem por 19% do consumo anual; com um
> transitório de 3 s, responderiam por 0,5%. O valor é conservador e está registrado
> como pendência aberta do programa.

---

## A pressurização direta: a energia é tempo ligado

Tudo o que se disse até aqui vale para o recalque, em que a bomba enche a caixa
superior de uma vez, na vazão dela, e desliga. O pressurizador trabalha de outro
modo. Ele liga a cada descarga e fica ligado enquanto a caixa acoplada enche, e quem
decide a vazão é a boia da caixa, e não a bomba. Uma bomba maior não enche a caixa mais
depressa: fica o mesmo tempo ligada, puxando mais potência.

Por isso o programa não calcula a energia do pressurizador pela energia específica
`ρ·g·H/(η_b·η_m)`, que pressupõe a bomba no ponto de melhor rendimento. Calcula pelo
tempo ligado:

```equacao:energia_pressurizador
E = (P ÷ η_m) · [V ÷ min(Q_b(H), Q_p) + N · t_r]
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `E` | energia anual do pressurizador | kWh/ano |
| `P` | potência de placa, no eixo | kW |
| `η_m` | rendimento do motor, da Tabela 13 da ABNT NBR 17094-2 | adimensional |
| `V` | volume pluvial consumido | m³/ano |
| `Q_b(H)` | vazão da curva do modelo na pressão de trabalho `H` | m³/h |
| `Q_p` | vazão do ponto de uso | m³/h |
| `N` | acionamentos por ano: moradores × 5,05 descargas × 365,25 | 1/ano |
| `t_r` | retardo de desligamento do controle eletrônico | h |

É a forma do «método simples» que Ward, Butler e Memon (2012) descrevem, potência vezes
duração de operação, com duas correções: a vazão efetiva é a menor entre a da bomba e
a do ponto, e o retardo dos controles eletrônicos entra a cada partida. A potência de
placa é a do ponto nominal, e em vazão baixa o motor puxa um pouco menos; a estimativa
tende a superestimar a energia, mas ordena os modelos entre si.

A vazão do ponto padrão é de 0,15 L/s, isto é, 9 L/min: a vazão de projeto da bacia com
caixa de descarga na Tabela A.1 da ABNT NBR 5626:1998. A edição de 2020 retirou a tabela
e passou ao projeto a tarefa de explicitar as vazões nos pontos de utilização (item
6.7.1); quem tiver o dado do fabricante da bacia deve usá-lo.

### O catálogo

A etapa **4. Reservatório & Custos** traz seis pressurizadores residenciais de cinco
fabricantes, cada um com a curva vazão × pressão do manual, guardado nos documentos
consultados: Komeco TP 820T e TP 825T, Cardal Potenza, Jacuzzi AcquaHouse, com curva
ensaiada no Laboratório de Etiquetagem de Bombas da UNIFEI, Syllent Impulse Press e Rowa
Max Press 20E. Para outro modelo, a opção «Personalizado» pede a potência de placa, a
vazão lida na curva do fabricante na pressão de trabalho e o retardo de desligamento.

A tabela aplica o catálogo à pressurização direta do tutorial: a cisterna de 4.000 L sem
caixa superior, quatro moradores e a vazão da bacia de 9 L/min.

<!-- inclui: _tabelas/cap28_pressurizadores.md -->

A 18 m.c.a., cinco dos seis modelos entregam mais que os 9 L/min da bacia, e todos
ficam as mesmas 110 horas por ano ligados. O que os separa é a potência: o de 1/4 CV
gasta 40 kWh, os de 1/2 CV, 67. O sexto, com pouco mais de 7 L/min a 18 m.c.a., opera
quase no fim da curva, fica mais tempo ligado e ainda soma dez segundos de retardo a
cada uma das 7.373 partidas do ano.

A 24 m.c.a. a ordem se inverte. O modelo de 1/4 CV chega a 4,4 L/min, e o tempo ligado
dobra; três modelos nem alcançam a pressão. O melhor passa a ser um de 1/2 CV. ==A
regra que a tabela ensina é escolher o menor modelo que entrega a vazão do ponto na
pressão de trabalho,== e é o que o item 6.5.11.12 da ABNT NBR 5626:2020 pede: que o
consumo de energia das bombas de recalque e de pressurização seja minimizado pela escolha
da bomba, entre as alternativas consideradas. A tela aponta esse modelo e mostra a
energia de todos os outros ao lado.

> **Duas bombas, e não uma.** O item 6.5.11.2 da mesma norma exige no mínimo duas bombas,
> de funcionamento independente, nos sistemas de recalque e de pressurização. O tutorial
> segue a norma, e o investimento conta a principal e a reserva.

---

## Por que a energia do recalque é pequena, e a do pressurizador não

Elevar um metro cúbico a doze metros custa cerca de 0,033 kWh de energia hidráulica.
Com os dois rendimentos, chega a 0,11 kWh por metro cúbico entregue, e o recalque do
tutorial, com as partidas, a 0,13 kWh/m³.

A pressurização direta do mesmo projeto gasta de 0,68 a 1,66 kWh/m³, conforme o modelo:
cinco a treze vezes mais. Os números reproduzem uma diferença que a literatura já
tinha medido. Na revisão de Vieira et al. (2014), a mediana dos estudos teóricos foi de
0,20 kWh/m³, e a dos empíricos, de 1,40 kWh/m³, porque os primeiros ignoravam as partidas,
o modo de espera e o rendimento real de motor e bomba. A mesma revisão relata 1,70 kWh/m³
para abastecer uma caixa acoplada diretamente com uma bomba de 450 W, e 1,52 kWh/m³ em
média em dezenove residências australianas com alimentação direta.

O recalque do tutorial fica perto da mediana teórica porque trabalha como os estudos
teóricos supõem: poucas partidas por ano, na vazão da própria bomba. O pressurizador fica
na faixa empírica porque trabalha como as casas medidas: uma partida por uso, na vazão
do ponto.

Mesmo assim, a energia é pequena diante da economia na fatura. Os 40 kWh do menor
pressurizador custam menos de trinta reais por ano na tarifa do tutorial. O argumento de
que «bombear gasta mais do que economiza» não se sustenta em edificação de pequeno porte,
mas a escolha do arranjo e do modelo pode multiplicar por dez a parcela de energia, e é
ela que pesa no carbono da seção {{n:30}}.

Em prédio alto, com trinta metros de recalque, a conta muda, e vale refazê-la.
