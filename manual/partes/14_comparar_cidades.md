# 14. Comparar cidades

> **Pergunta que este guia responde:** o mesmo projeto renderia o mesmo em outra
> cidade?

Não. E a diferença não é a que a intuição sugere.

---

## 14.1. Como fazer

Mantenha todos os parâmetros do projeto e troque só a série de precipitação. Na aba
**Projeto**, escolha outra cidade da base nacional ou carregue outro arquivo, e rode
de novo.

Para comparar muitas cidades de uma vez, use a linha de comando em lote — o guia 19
mostra.

---

## 14.2. O resultado

O projeto do tutorial — 150 m², 600 L/dia, 40% de fração atendível, 5.000 L —
levado a quatro capitais:

<!-- inclui: _tabelas/cap14_cidades.md -->

---

![Chuva anual e potencial de economia nas quatro capitais](../figuras/fig03_cidades.png)

*Figura 3 — As barras azuis são a chuva anual; as laranjas, o potencial de economia. Manaus tem a maior barra azul e não tem a maior laranja.*

## 14.3. A lição: regime manda mais que lâmina

Leia as colunas de chuva anual e de potencial lado a lado. Elas **não** andam
juntas.

**Manaus chove 20% mais que Florianópolis e rende 25% menos.** Dois mil cento e
cinquenta e cinco milímetros por ano contra mil setecentos e noventa e cinco, e
ainda assim 27,92% contra 37,46%.

**Brasília chove 23% menos que Florianópolis e rende quase a metade.** Vinte vírgula
oito por cento.

A explicação está na quarta coluna, a razão entre o mês mais chuvoso e o menos
chuvoso:

| Cidade | Razão | O que significa |
| :--- | ---: | :--- |
| Florianópolis | 3,2× | chove o ano inteiro, com estação mais úmida |
| São Paulo | 4,0× | idem, um pouco mais marcado |
| Manaus | 17,3× | seca amazônica curta mas real |
| Brasília | 1.192× | **o mês mais seco é seco de verdade** |

Em Brasília, junho, julho e agosto praticamente não chovem. Um reservatório
dimensionado para atravessar noventa dias de estiagem teria que guardar noventa dias
de demanda pluvial: 21.600 litros no nosso projeto. Nenhuma cisterna residencial faz
isso, e por isso o sistema fica ocioso um trimestre por ano.

> **A conclusão prática.** Aproveitamento pluvial rende mais onde a chuva é
> **frequente**, e não onde ela é **abundante**. Cidades de clima subtropical úmido
> com chuva distribuída são o melhor caso do Brasil; cidades de clima tropical com
> estação seca marcada são o pior, por mais que chova na estação úmida.

---

## 14.4. O que mais muda entre cidades

A chuva não é a única coisa que muda, e as outras duas podem inverter a conclusão
econômica.

**A tarifa.** O metro cúbico custa muito diferente pelo país, e o **regime de
mínimo** mais ainda. Um potencial de 20% em município de tarifa alta e regime de
disponibilidade pode render mais dinheiro que 37% em município de franquia. O guia
16 trata disso.

**O fator de emissão da rede elétrica.** Muda a emissão evitada por metro cúbico e o
custo do bombeamento. O programa traz o fator por região.

> **Ao comparar cidades num estudo, deixe claro o que variou.** Comparar só a chuva,
> mantendo tarifa e fator de emissão fixos, isola o efeito climático e é uma
> comparação legítima — desde que declarada. Variar tudo ao mesmo tempo produz um
> número que não se sabe explicar.

---

## 14.5. O volume ideal também muda

Repare na última coluna: o volume ideal vai de 5.000 a 6.000 L entre as quatro
cidades, uma variação pequena.

Isso surpreende, e tem explicação. O volume ideal pelo critério do ganho marginal
encontra o joelho da curva, e o joelho é governado pelo **tamanho dos eventos de
chuva**, que é parecido entre as quatro. O que muda muito é o **patamar** que a
curva atinge, não onde ela dobra.

Dito de outro modo: em Brasília você acerta o mesmo volume e colhe menos.
