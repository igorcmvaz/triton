# 6. A primeira simulação

> Ao terminar este capítulo você terá o primeiro resultado na tela e saberá **ler**
> os quatro números que importam. Ler é a parte difícil: o programa entrega muitos
> números, e três deles respondem perguntas diferentes.

Falta um dado para simular: o volume do reservatório. Vamos chutar.

**3.000 litros.** Uma cisterna de concreto de 3 m³ é um tamanho comum de quintal,
cabe no orçamento e é o que um projetista proporia sem pensar muito. O capítulo 7
vai perguntar se é o volume certo. Aqui só queremos ver o programa rodar.

Na etapa **4. Reservatório & Custos**, escolha volume fixo, informe 3.000 L, deixe o reservatório
superior desmarcado, e rode.

---

## 6.1. O resultado

<!-- inclui: _tabelas/cap06_primeira_simulacao.md -->

Quatro números merecem atenção, e cada um responde uma pergunta diferente.

---

## 6.2. O potencial de economia: 34,92%

**Responde: quanto da conta de água deixo de pagar?**

É o indicador central do Netuno, e o que vai para o resumo de qualquer estudo. Ele é
a razão entre a água pluvial consumida e a demanda **total** da edificação, ao longo
de toda a série:

```
potencial = água pluvial consumida ÷ demanda total × 100
```

Repare no denominador: **demanda total**, e não demanda pluvial. Por isso o teto é
40%, a fração atendível definida no capítulo 5.

O sistema atingiu 34,92% de um teto de 40%. Dito de outro modo, ele entrega
**87% do que pretendia entregar**. Os 13% que faltam são os dias em que a cisterna
não tinha água suficiente.

> **Não confunda os dois percentuais.** «Economia de 35%» e «atendimento de 87% da
> demanda pluvial» descrevem o mesmo sistema e são números diferentes. Estudos
> publicados às vezes trocam um pelo outro. Declare qual está usando.

---

## 6.3. O extravasamento: 303 L/dia

**Responde: o reservatório é grande o bastante?**

Trezentos e três litros por dia, em média, transbordam da cisterna e vão para a
rede de drenagem. É **mais** do que os 240 L/dia que o sistema pretende consumir.

Esse número é o argumento mais forte a favor de aumentar o reservatório, e é
exatamente o que o capítulo 7 vai fazer. Guarde-o.

> Um extravasamento alto não é defeito do programa nem do projeto. É a assinatura do
> descasamento entre a chuva, que chega concentrada em poucos dias, e a demanda, que
> é constante. O reservatório existe para amortecer isso, e todo reservatório
> finito falha em algum evento.

---

## 6.4. Os dias de atendimento: 85,7% plenos

**Responde: com que frequência posso contar com o sistema?**

É a confiabilidade **temporal**, e ela responde uma pergunta que o potencial não
responde.

| Classe | O que significa |
| :--- | :--- |
| pleno | a chuva atendeu **toda** a demanda pluvial do dia |
| parcial | atendeu parte, e a rede completou |
| nulo | a cisterna estava vazia; tudo veio da rede |

Em 85,7% dos dias o sistema deu conta sozinho. Nos outros 14,3%, a rede entrou —
integral ou parcialmente.

A distinção importa para o projeto hidráulico: um sistema com muitos dias nulos
precisa de alimentação automática de reserva bem dimensionada, e o usuário vai
perceber a alternância. Um sistema com 99% de dias plenos é, na prática,
independente.

> **Potencial e confiabilidade não andam juntos.** É possível ter potencial alto com
> confiabilidade baixa: um reservatório que se enche na estação chuvosa e seca na
> estiagem entrega muito volume no ano e falha metade dos dias. A tabela do
> capítulo 7 mostra as duas colunas divergindo.

---

## 6.5. O volume anual poupado

**Responde: quanto vale isso em dinheiro e em carbono?**

É o número que atravessa para os capítulos 10 e 11. A economia da conta de água sai
dele, e a emissão evitada também.

Repare que ele é bem menor que os 187 m³/ano disponíveis depois do descarte. A
diferença toda virou extravasamento.

---

## 6.6. Por que não chegamos aos 40%

O capítulo 5 terminou com um confronto: 187 m³ de oferta contra 88 m³ de demanda.
Água sobrando. Ainda assim o sistema entrega 87% do pretendido, e não 100%.

A resposta está no **tempo**. A água não sobra quando é preciso. Ela chega toda de
uma vez, enche a cisterna de 3.000 L em um único dia de chuva forte, transborda, e
depois faz falta duas semanas mais tarde.

Os 3.000 L guardam **12 dias e meio** de demanda pluvial. Toda estiagem mais longa
que isso esvazia a cisterna, e o sistema passa a depender da rede.

É por isso que aumentar o reservatório funciona — e é por isso que aumentar tem
limite. O capítulo 7 mede exatamente onde fica esse limite.

---

## 6.7. O que temos até aqui

| Resultado com 3.000 L | |
| :--- | ---: |
| potencial de economia | 34,92% |
| de um teto de | 40% |
| extravasamento | 303 L/dia |
| dias de atendimento pleno | 85,7% |

Um resultado defensável. Mas escolhemos 3.000 L por palpite, e o extravasamento
sugere que é pouco.

Quanto seria o certo?
