# 28. Energia de bombeamento

> Este capítulo traz a cadeia completa do eixo à tomada, e explica por que a
> potência de placa **não** é o que o medidor registra.

Três versões desta conta já existiram no programa, e as duas primeiras estavam
erradas. O capítulo diz quais eram e por quê, porque quem lê um estudo feito numa
versão antiga precisa saber.

---

## 28.1. A potência de placa é de eixo

A ABNT NBR 17094-2:2016 manda marcar o **rendimento** na placa de identificação do
motor, como grandeza separada da potência. Isso só faz sentido se a potência de
placa for a potência mecânica **no eixo**.

Daí a cadeia ter dois rendimentos, e não um:

| Rendimento | O que converte |
| :--- | :--- |
| **da bomba**, `η_b` | potência de eixo em potência hidráulica entregue à água |
| **do motor**, `η_m` | potência elétrica da tomada em potência mecânica no eixo |

O programa pede os dois, em campos separados.

---

## 28.2. As equações

**Energia específica do recalque**, por metro cúbico elevado:

```
e = ρ · g · H ÷ (η_b · η_m)          [kWh/m³]
```

com `ρ` = 1.000 kg/m³, `g` = 9,81 m/s² e `H` a altura manométrica em metros de
coluna d'água. Não depende da vazão nem da potência: elevar um metro cúbico a uma
dada altura custa a mesma energia, com bomba grande ou pequena. O que muda com a
potência é o **tempo**, não o consumo específico.

**Quando a vazão de operação é declarada**, a forma equivalente:

```
e = P ÷ (Q · η_m)                    [kWh/m³]
```

com `P` em kW e `Q` em m³/h. O rendimento da bomba já está embutido no fato de um
motor de `P` kW no eixo fazer a bomba entregar `Q` m³/h naquela altura; dividir por
ele outra vez contaria a perda hidráulica duas vezes.

**Vazão, quando não declarada:**

```
Q = P · η_b ÷ (ρ · g · H)
```

**Energia das partidas:**

```
E_part = P · t_part ÷ η_m            [kWh]
```

Sem `η_b`, porque na partida não há vazão útil e portanto não há perda hidráulica a
descontar. O motor puxa da tomada, e é só isso que o medidor registra.

**Total anual:**

```
E = e · V_recalcado + P · t_part ÷ η_m
```

---

## 28.3. O rendimento do motor, quando não informado

Vale a Tabela 13 da ABNT NBR 17094-2:2016, linha IR1, motores de dois polos — que é
o que são as motobombas residenciais, a 3.450 rpm:

| Potência | Rendimento IR1 | Rendimento IR2 |
| :--- | ---: | ---: |
| 1/4 CV, 0,18 kW | 50,0% | 64,0% |
| 1/3 CV, 0,25 kW | 55,5% | 68,0% |
| **1/2 CV, 0,37 kW** | **60,5%** | 72,0% |
| 3/4 CV, 0,55 kW | 64,0% | 74,0% |
| 1 CV, 0,75 kW | 69,3% | 75,5% |
| 1,5 CV, 1,10 kW | 71,5% | 82,5% |
| 2 CV, 1,50 kW | 72,4% | 84,0% |

Adota-se a **IR1** por ser o piso normativo e o que se encontra em motobomba de
prateleira. Quem tem motor de alto rendimento informa o valor marcado na placa.

Para potências fora da tabela, a norma manda adotar o maior dos dois rendimentos
vizinhos quando a potência estiver no ponto médio ou acima, e o menor quando estiver
abaixo.

---

## 28.4. As três versões desta conta

| Versão | Recalque | Partidas | O erro |
| :--- | :--- | :--- | :--- |
| até 5.0.7 | `P × horas ÷ η_b` | `P × t ÷ η_b` | descontava a perda hidráulica duas vezes **e** ignorava o motor |
| 5.0.8 | `ρgH ÷ η_b` | `P × t ÷ η_b` | corrigiu o recalque e deixou as partidas |
| atual | `ρgH ÷ (η_b · η_m)` | `P × t ÷ η_m` | — |

No caso de referência — meio CV, 12 m.c.a., 82 m³ recalcados, 98 acionamentos por
ano — o consumo específico passou de 0,0654 para 0,1080 kWh/m³ entre a 5.0.8 e a
atual.

> **Quem cita um estudo feito em versão anterior precisa saber disso.** A diferença
> não é de arredondamento.

---

## 28.5. Os valores de recurso

Usados quando o projeto não declara:

| Parâmetro | Valor | Origem |
| :--- | ---: | :--- |
| altura manométrica | 12 m.c.a. | casa de dois pavimentos com cisterna enterrada: ~8 m de desnível geométrico mais ~30% de perda de carga |
| rendimento da bomba | 55% | motobombas residenciais de meio a um CV ficam entre 40% e 60% no ponto de operação |
| tempo de partida | 108 s | ver a ressalva abaixo |

> **A altura manométrica é o parâmetro que mais pesa no consumo.** Quem conhece o
> desnível do projeto deve informá-lo. Dobrar a altura dobra a energia.

> **O tempo de partida de 108 s merece atenção.** Ele representa o tempo de escorva
> de uma bomba autoaspirante cuja linha de sucção drenou. Numa instalação com válvula
> de pé em ordem, a linha permanece escorvada e as partidas seguintes são imediatas.
> No caso de referência, as partidas respondem por 19% do consumo anual; com um
> transitório de 3 s, responderiam por 0,5%. O valor é conservador e está registrado
> como pendência aberta do programa.

---

## 28.6. Por que a energia é pequena

Elevar um metro cúbico a doze metros custa cerca de 0,033 kWh de energia hidráulica.
Com os dois rendimentos, chega a 0,11 kWh por metro cúbico entregue.

Água é pesada, mas doze metros é pouco. Por isso o custo energético do aproveitamento
pluvial é desprezível diante da economia da conta de água em edificação de pequeno
porte — e por isso o argumento de que «bombear gasta mais do que economiza» não se
sustenta nessa escala.

Em prédio alto, com trinta metros de recalque, a conta muda, e vale refazê-la.
