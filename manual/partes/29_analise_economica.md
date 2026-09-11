# 29. Análise econômica e os regimes tarifários

> Este capítulo formaliza o fluxo de caixa e detalha os cinco regimes de mínimo
> tarifário — o dado que mais decide a viabilidade de um sistema pluvial no Brasil.

---

## 29.1. A economia é a diferença entre duas contas

O programa **não** multiplica o volume poupado por uma tarifa. Ele monta duas contas
completas para cada mês da projeção e subtrai:

```
economia_mês = conta(volume total) − conta(volume potável)
```

A razão é a progressividade. O metro cúbico que se deixa de consumir é o **último**,
o mais caro, e não o médio. Num município com faixa inicial de R$ 3,08/m³ e segunda
faixa de R$ 14,31/m³, usar a tarifa média subestima a economia em mais da metade.

---

## 29.2. A conta de água

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

```
parcela de esgoto = tarifa de água × percentual
```

O percentual incide sobre a **tarifa de água**, e não sobre a fatura. Cem por cento
significa que a parcela de esgoto iguala a de água, e portanto o esgoto é **metade
da fatura**.

---

## 29.3. Os cinco regimes na base

| Regime | Municípios |
| :--- | ---: |
| franquia no mínimo | 329 |
| sem mínimo | 165 |
| disponibilidade | 156 |
| franquia retroativa | 2 |
| piso de pagamento | 0 |

O piso está implementado e nenhum município da base foi classificado nele até agora.

O guia 16 traz o exemplo numérico comparando Floriano e Florianópolis, e a lição
prática: em regime de franquia, economizar abaixo da franquia não desconta nada.

---

## 29.4. O investimento

```
CAPEX = cisterna + caixa superior + mão de obra + tubulação
        + acessórios + (custo unitário da bomba × número de bombas)
        + CAPEX incremental da ETAP
```

O último termo segue a regra incremental do capítulo 27.

Os preços de reservatório vêm da base do programa, com procedência declarada. Para
volumes fora da tabela, o programa interpola linearmente; para extrapolar além da
tabela, só o faz se a regressão tiver **R² acima de 0,90**, e avisa quando não tem.

---

## 29.5. O custeio anual

| Parcela | Origem |
| :--- | :--- |
| energia de bombeamento | capítulo 28, com a bandeira tarifária aplicada |
| cloração | massa de **produto**, não de cloro ativo |
| ETAP | custeio incremental, sem contar a cloração duas vezes |
| custos operacionais declarados | lista livre do usuário |

A bandeira tarifária ajusta a tarifa de energia: amarela, vermelha 1, vermelha 2, ou
desconto fora de ponta na branca.

---

## 29.6. A projeção mês a mês

Para cada mês `m` do período de análise:

**A inflação incide só sobre o custeio:**

```
fator_inflação = (1 + i)^(m−1)
```

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

## 29.7. Os indicadores

**Valor presente líquido:**

```
VPL = −CAPEX + Σ [ fluxo_m ÷ (1 + TMA)^m ]
```

**Taxa interna de retorno:** a taxa que zera o VPL. Quando não há raiz real — o que
acontece quando o fluxo nunca se torna positivo — o programa devolve nulo, em vez de
um número inventado.

**Payback descontado:** o primeiro mês em que o acumulado descontado cruza zero.

---

## 29.8. As premissas frágeis

Duas merecem sensibilidade, e o guia 20 mostra como.

**O reajuste tarifário.** Cinco por cento ao ano por vinte anos multiplica a tarifa
por 2,65; três por cento, por 1,81; sete por cento, por 3,87. O VPL varia
proporcionalmente. É a premissa que mais move o resultado, e a mais incerta.

**A vida útil.** Vinte anos é a adoção padrão. Cisterna de concreto dura mais;
componentes de polietileno expostos ao sol duram menos. A vida útil entra tanto no
período de análise quanto no payback de carbono do capítulo 30.
