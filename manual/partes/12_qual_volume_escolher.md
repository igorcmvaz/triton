# Qual volume escolher, afinal

> Ao terminar este capítulo você terá um volume recomendado, e saberá que ele
> depende de pesos que **você** declarou — não de uma verdade que o programa
> descobriu.

---

## Três critérios, três respostas

Os capítulos anteriores fizeram três perguntas diferentes e receberam três respostas
diferentes.

<!-- inclui: _tabelas/cap12_multicriterio.md -->

A primeira tabela é o retrato do problema. Repare em como as colunas discordam:

- O **potencial** cresce monotonicamente: quanto maior a cisterna, mais água.
  Máximo em 12.000 L.
- O **VPL** sobe, achata e começa a cair: máximo em 8.000 L, praticamente empatado
  com 5.000 L, e caindo em 12.000 L, porque o investimento adicional deixa de se
  pagar.
- O **carbono** sobe e cai bem antes: máximo em 3.000 L. Depois disso, cada metro
  cúbico de polietileno acrescenta mais dívida do que crédito.

Não existe volume que vença nos três. Escolher exige declarar o que importa mais.

---

## Como o TOPSIS resolve

O programa usa TOPSIS sobre **sete critérios**:

| Critério | Direção |
| :--- | :--- |
| potencial de economia | maximizar |
| extravasamento | minimizar |
| valor presente líquido | maximizar |
| payback descontado | minimizar |
| taxa interna de retorno | maximizar |
| CO₂e no fim da vida | minimizar |
| consumo de água potável | minimizar |

O método normaliza a matriz de decisão, aplica os pesos, calcula a distância de cada
alternativa à solução ideal e à anti-ideal, e ordena pela proximidade relativa ao
ideal.

Com **pesos iguais**, o vencedor é **5.000 L**.

> **Três declarações que um estudo publicado precisa fazer.**
>
> A normalização do programa é uma **variante** de Hwang e Yoon: ela translada por
> `x − min(x)` antes da normalização vetorial, para admitir VPL negativo. É uma
> escolha deliberada, e apresentá-la como TOPSIS canônico seria incorreto.
>
> O SMAA-VIKOR, disponível ao lado, sorteia pesos e devolve a probabilidade de cada
> volume ocupar cada posição. É a resposta certa quando não há consenso sobre os
> pesos.
>
> As condições C1 e C2 de Opricovic, de vantagem aceitável e de estabilidade, **não
> estão implementadas**. A seção {{n:32}} detalha.

---

## O peso muda a resposta

A segunda tabela mostra o que acontece ao deslocar o peso.

| Peso dominante | Volume |
| :--- | ---: |
| pesos iguais | 5.000 L |
| técnico, 60% | 8.000 L |
| econômico, 60% | 5.000 L |
| ambiental, 60% | 5.000 L |

Privilegiar o critério técnico empurra para 8.000 L. Os outros dois convergem em
5.000 L.

Essa convergência não é regra geral: aqui ela acontece porque 5.000 L está numa
região plana do VPL e ainda com saldo de carbono confortável. Em outro município,
com tarifa mais baixa, o ponto econômico cairia e a divergência apareceria.

> **Declare os pesos.** «Volume ótimo pelo TOPSIS» sem os pesos é uma afirmação
> impossível de reproduzir. Dois artigos com pesos diferentes chegam a volumes
> diferentes e ambos estão certos.

---

## A recomendação do tutorial

**5.000 L, em polietileno.**

Ele vence com pesos iguais, vence com peso econômico, vence com peso ambiental, e
fica em segundo por pouco com peso técnico. É uma escolha robusta: não depende de
uma ponderação específica para se sustentar.

E vale reparar que **é o mesmo volume que o critério hidráulico da seção {{n:7}} já
tinha indicado**, com o limiar de 1 %/m³. As duas rotas chegaram ao mesmo lugar por
caminhos independentes, o que aumenta a confiança na resposta.

Isso não é coincidência garantida. É por isso que o tutorial fez o caminho longo:
para saber que as rotas concordam **neste caso**, e não supor que concordam sempre.

---

## O projeto, fechado

| Netuno 5 · residência unifamiliar em Florianópolis | |
| :--- | ---: |
| série de precipitação | Florianópolis, 30 anos, 1.795 mm/ano |
| área de captação | 150 m² |
| coeficiente de escoamento | 0,85 |
| descarte de primeiras águas | 2,0 mm, todo evento |
| moradores | 4 |
| demanda total | 600 L/dia |
| fração atendível por chuva | 40% |
| reservatório inferior | 5.000 L, polietileno |
| reservatório superior | não |
| classe de qualidade | 1, cloração por pastilhas |
| **potencial de economia de água potável** | **37,46%** |
| dias de atendimento pleno | 92,9% |
| água poupada | 82,1 m³/ano |
| investimento | R$ 10.080 |
| **valor presente líquido em 20 anos** | **R$ 18.595** |
| payback descontado | 6,5 anos |
| **saldo de carbono em 20 anos** | **+248 kg CO₂e** |
| payback de carbono | 10,9 anos |

Falta uma coisa: contar isso a alguém.
