# 35. Comparação com o Netuno 4

> Este capítulo traz a medição contra 4.050 casos de referência e, mais importante,
> a **decomposição** da diferença por causa.

---

## 35.1. O papel da comparação

O Netuno 4 **não é alvo de fidelidade**. O Netuno 5 adota decisões de modelagem
distintas, deliberadas e documentadas, e espera-se que os resultados difiram.

O que o Netuno 4 oferece é algo mais valioso: um conjunto **independente** de
resultados, produzido por outra implementação do mesmo modelo conceitual. Sem essa
referência externa, a verificação se limitaria a propriedades internas — necessárias,
mas incapazes de detectar um erro sistemático que as respeitasse todas.

---

## 35.2. Os dados de referência

Quatro mil e cinquenta casos exportados do Netuno 4, preservados no repositório:

| Conjunto | Casos | Cidades |
| :--- | ---: | :--- |
| Floripa/Brasília | 1.458 | Florianópolis, Brasília |
| Manaus/São Paulo | 2.592 | Manaus, São Paulo |

---

## 35.3. A divergência total

| Conjunto | Erro médio absoluto | Viés | Erro máximo | ≤ 5 pp |
| :--- | ---: | ---: | ---: | ---: |
| Floripa/Brasília | 2,29 pp | −2,29 pp | 7,43 pp | 97,4% |
| Manaus/São Paulo | 2,71 pp | −2,71 pp | 10,60 pp | 88,6% |

O viés é sistematicamente negativo: o Netuno 5 estima **menos** economia. Isso é
esperado, e a próxima seção diz por quê.

---

## 35.4. A decomposição, que é o número que importa

Comparar o ótimo de um programa com o do outro mistura três diferenças. A
decomposição as separa, comparando em três configurações sucessivamente mais
controladas, sobre os 2.583 casos de Manaus e São Paulo:

| Configuração | Erro médio | ≤ 5 pp |
| :--- | ---: | ---: |
| 1. ótimo do Netuno 5 contra ótimo do Netuno 4 | 2,81 pp | 88,6% |
| 2. avaliado no volume que o Netuno 4 declarou ótimo | 1,60 pp | 96,4% |
| 3. idem, adotando o descarte por limiar do Netuno 4 | **0,25 pp** | **100,0%** |

A atribuição resultante:

| Fonte da divergência | Contribuição | Natureza |
| :--- | ---: | :--- |
| critério de escolha do volume ótimo | 1,11 pp (41%) | diferença de projeto |
| tratamento do descarte de primeira chuva | 1,36 pp (50%) | diferença metodológica deliberada |
| **resíduo do balanço hídrico** | **0,25 pp (9%)** | — |

> **Neutralizadas as duas diferenças conhecidas, o motor do Netuno 5 reproduz o
> Netuno 4 com erro médio absoluto de 0,25 ponto percentual e 100% dos casos dentro
> de 5 pontos.**
>
> O resíduo é compatível com a precisão de duas casas decimais da própria planilha de
> referência. É **este** número que verifica o motor. A divergência total de 2,81 pp
> não mede erro: mede a soma de duas decisões de projeto, ambas deliberadas.

---

## 35.5. As duas diferenças, em detalhe

### O descarte

O Netuno 4 trata `d_f` como **limiar do evento**: abaixo dele nada é captado, acima
dele capta-se a chuva **inteira**. O manual do Netuno 4, seção 3.1, é explícito:
«caso a precipitação em um dado dia esteja abaixo desse valor, o Netuno considerará
que não houve precipitação».

O Netuno 5 **subtrai** a lâmina. A mudança é fisicamente mais fiel: a água desviada
para o dispositivo de autolimpeza não chega à cisterna.

Responde por metade da divergência.

### O critério de volume ótimo

Os dois programas escolhem o volume ideal por critérios de ganho marginal, mas com
implementações e grades diferentes. Avaliando os dois no **mesmo** volume, a
divergência cai de 2,81 para 1,60 pp.

Responde por 41% da divergência.

---

## 35.6. Como medir a diferença sem alterar o motor

A emulação da regra do Netuno 4 é feita **transformando a série de entrada**, e não
tocando no código do balanço:

```
P′ = P + d_f    quando P ≥ d_f
P′ = 0          caso contrário
```

Aplicada essa transformação, o cálculo `P_ef = max(0, P′ − d_f)` do Netuno 5
reproduz exatamente a semântica de limiar. A medição não corre o risco de validar
código que não é o distribuído.

> **Uma ressalva de documentação.** O protocolo de verificação do repositório
> instrui a usar uma opção de linha de comando para essa emulação. Essa opção
> **não está implementada**. Use a transformação da série, ou compare com descarte
> igual a zero, em que as duas regras coincidem.

---

## 35.7. Os casos de referência nula

Em parte das linhas, o Netuno 4 exportou zero enquanto o Netuno 5 calcula valor
positivo. A incidência difere muito entre conjuntos: 0,35% em Manaus e São Paulo
contra 34,98% em Floripa e Brasília.

A disparidade aponta para característica dos **dados de referência** — provavelmente
o Netuno 4 não encontrou volume ótimo sob o seu próprio critério — e não para erro do
Netuno 5, que nunca devolve zero nesses casos. São segregados das estatísticas para
não as dominar.

---

## 35.8. O que declarar num estudo comparativo

- os **dois números**: a divergência total e o resíduo depois da decomposição;
- as duas diferenças deliberadas, nomeadas;
- se a comparação foi feita com descarte zero, com emulação de limiar, ou sem
  neutralização;
- a versão de cada programa.

Apresentar apenas a divergência total, sem decompor, sugere um erro de motor que não
existe.
