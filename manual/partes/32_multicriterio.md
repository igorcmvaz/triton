# Decisão multicritério

> Esta seção formaliza os dois métodos de ordenação, e declara três desvios em
> relação à formulação canônica que um estudo publicado precisa citar.

---

## Os sete critérios

| # | Critério | Direção | Grupo |
| :-- | :--- | :--- | :--- |
| 1 | potencial de economia | maximizar | técnico |
| 2 | extravasamento | minimizar | técnico |
| 3 | valor presente líquido | maximizar | econômico |
| 4 | payback descontado | minimizar | econômico |
| 5 | taxa interna de retorno | maximizar | econômico |
| 6 | CO₂e no fim da vida | minimizar | ambiental |
| 7 | consumo de água potável | minimizar | ambiental |

As alternativas são os **volumes** da varredura. Cada uma traz os sete valores,
vindos das seções {{n:23}}, 29 e 30.

---

## TOPSIS

*Technique for Order of Preference by Similarity to Ideal Solution*, de Hwang e Yoon
(1981). Cinco passos:

1. monta a matriz de decisão, alternativas × critérios;
2. normaliza;
3. aplica os pesos;
4. identifica a solução **ideal** e a **anti-ideal**, tomando o melhor e o pior valor
   de cada critério;
5. ordena pela proximidade relativa ao ideal:

```equacao:topsis
C_i = d_i⁻ ÷ ( d_i⁺ + d_i⁻ )
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `C_i` | coeficiente de proximidade da alternativa `i`, entre 0 e 1 | adimensional |
| `d_i⁺` | distância euclidiana da alternativa `i` à solução ideal | adimensional |
| `d_i⁻` | distância euclidiana da alternativa `i` à solução anti-ideal | adimensional |

O coeficiente da Equação {{eq:topsis}} vale 1 para uma alternativa que coincidisse com a
solução ideal em todos os critérios, e 0 para uma que coincidisse com a anti-ideal.
Como nenhuma alternativa real ocupa esses extremos, o que interessa é a ordenação: o
maior coeficiente indica a alternativa mais próxima do ideal e mais distante do pior
caso, considerados simultaneamente todos os critérios com os pesos declarados.

---

## Três desvios a declarar

**Primeiro: a normalização é uma variante.** A formulação canônica usa normalização
vetorial, que exige valores não negativos. O valor presente líquido pode ser
negativo, e é frequentemente negativo nos volumes pequenos. O programa translada por
`x − min(x)` antes de normalizar.

É uma escolha deliberada e necessária. Apresentar o resultado como TOPSIS canônico
seria incorreto: declare a variante.

**Segundo: as condições de Opricovic não estão implementadas.** O VIKOR canônico
exige duas verificações sobre a solução de compromisso — vantagem aceitável e
estabilidade aceitável — e, quando falham, devolve um **conjunto** de soluções em vez
de uma. O programa devolve sempre a melhor, sem o teste.

Na prática isso significa que a solução de compromisso do VIKOR deve ser lida com a
análise de sensibilidade de pesos ao lado, e não sozinha.

**Terceiro: a atribuição do código.** A implementação do VIKOR e do SMAA-VIKOR foi
escrita de forma independente e **verificada contra** a biblioteca `crispyn`, de
Aleksandra Bączkiewicz. O TOPSIS foi verificado contra a formulação original de
Hwang e Yoon num caso de valores todos positivos, em que a translação é inócua.

---

## SMAA-VIKOR

*Stochastic Multicriteria Acceptability Analysis*. Existe para responder a pergunta
que o TOPSIS não responde: **e se os pesos fossem outros?**

O método sorteia combinações de pesos e devolve, para cada alternativa, a
**probabilidade** de ela ocupar cada posição do ranking.

Um volume que vence em 80% dos sorteios é uma recomendação robusta. Um que vence em
30% é frágil, e o texto do estudo precisa dizer isso em vez de apresentar o vencedor
como se fosse consensual.

> É a ferramenta certa quando não há consenso sobre os pesos — que é o caso normal.

---

## Os pesos

O programa aceita pesos por critério. Com pesos iguais, cada critério vale 1/7.

**Declare os pesos.** «Volume ótimo pelo TOPSIS» sem os pesos é uma afirmação
impossível de reproduzir. Dois estudos com pesos diferentes chegam a volumes
diferentes, e ambos estão certos.

Três condutas defensáveis:

- **pesos iguais**, declarados como ausência de preferência;
- **pesos justificados**, com a razão de cada um;
- **SMAA**, reportando a faixa de resultados em vez de um vencedor.

---

## Os melhores por critério isolado

Além da ordenação ponderada, o programa identifica o vencedor de cada grupo:
técnico, financeiro e ambiental. São três números que valem ser reportados juntos.

Quando os três coincidem, a recomendação é forte. Quando divergem — que é o caso
comum, e o do tutorial — a divergência **é** o resultado, e escondê-la atrás de um
único número ponderado empobrece o estudo.

---

## O que o método não faz

- **não escolhe os pesos.** Isso é do analista, e é uma decisão de valor.
- **não valida os critérios.** Se o VPL estiver errado porque o regime tarifário
  está errado, o TOPSIS ordena o erro com precisão.
- **não incorpora restrições.** Espaço disponível, orçamento máximo, exigência
  normativa: tudo isso é filtro anterior, aplicado pelo projetista.
