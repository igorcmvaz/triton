# Comparação com o Netuno 4

> Esta seção traz a medição contra 4.050 casos de referência e, mais importante,
> a **decomposição** da diferença por causa.

---

## O papel da comparação

Convém começar esclarecendo o que esta comparação **não** é. ==O Netuno 4 não constitui
alvo de fidelidade para o Netuno 5.== A versão atual adota decisões de modelagem distintas,
deliberadas e documentadas, e seria motivo de preocupação, e não de satisfação, se os
resultados coincidissem exatamente.

O valor do Netuno 4 nesta verificação é outro, e é maior: ele oferece um conjunto
independente de resultados, produzido por outra implementação do mesmo modelo conceitual,
por outras mãos e em outra linguagem. Sem uma referência externa dessa natureza, a
verificação se limitaria a propriedades internas do programa — necessárias, conforme a
seção {{n:34}} descreve, e incapazes de detectar um erro sistemático que as respeitasse
todas.

---

## Os dados de referência

A comparação entre as duas versões apoia-se em quatro mil e cinquenta casos exportados do
Netuno 4 e preservados desde então, byte a byte, justamente para que a referência não se
alterasse ao longo do desenvolvimento. Eles se distribuem por três conjuntos, com
cidades e faixas de parâmetros distintas.

| Conjunto | Casos | Cidades |
| :--- | ---: | :--- |
| Floripa/Brasília | 1.458 | Florianópolis, Brasília |
| Manaus/São Paulo | 2.592 | Manaus, São Paulo |

---

## A divergência total

| Conjunto | Erro médio absoluto | Viés | Erro máximo | ≤ 5 pp |
| :--- | ---: | ---: | ---: | ---: |
| Floripa/Brasília | 2,29 pp | −2,29 pp | 7,43 pp | 97,4% |
| Manaus/São Paulo | 2,71 pp | −2,71 pp | 10,60 pp | 88,6% |

O viés é sistematicamente negativo nos dois conjuntos, isto é, o Netuno 5 estima menos
economia que o Netuno 4 em praticamente todos os casos. O resultado é esperado, e a
subseção seguinte decompõe a diferença em suas causas atribuíveis.

---

## A decomposição, que é o número que importa

Comparar diretamente o volume ótimo de um programa com o do outro mistura três
diferenças de naturezas distintas, e o número resultante não informa qual delas responde
pelo quê. A decomposição as separa comparando os dois programas em três configurações
sucessivamente mais controladas, sobre os 2.583 casos de Manaus e São Paulo.

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

## As duas diferenças, em detalhe

### O descarte

O Netuno 4 trata a lâmina de descarte como limiar do evento: quando a precipitação do dia
fica abaixo dela, nada é captado; quando a ultrapassa, capta-se a chuva inteira, sem
subtração alguma. O manual do Netuno 4 é explícito a respeito, ao afirmar que uma
precipitação diária abaixo desse valor faz o programa considerar que não houve
precipitação.

O Netuno 5 subtrai a lâmina da precipitação do dia, tratamento fisicamente mais fiel
porque a água desviada para o dispositivo de autolimpeza efetivamente não chega à
cisterna. A mudança responde por metade da divergência total medida entre as duas
versões.

### O critério de volume ótimo

Ambos os programas escolhem o volume ideal por critérios de ganho marginal, mas as
implementações e as grades de busca diferem entre si, de modo que cada um elege um volume
distinto e a comparação passa a incluir essa diferença de escolha. Avaliando os dois
programas no mesmo volume — o que o Netuno 4 declarou ótimo — a divergência cai de 2,81
para 1,60 ponto percentual, o que atribui 41% da diferença total ao critério de escolha.

---

## Como medir a diferença sem alterar o motor

A emulação da regra antiga é feita transformando a série de precipitação de entrada, e
não alterando o código do balanço hídrico. A distinção metodológica é essencial: medir a
divergência com um código modificado validaria um programa que não é o distribuído ao
usuário, o que anularia o propósito da verificação.

```equacao:emulacao
P′ = P + d_f se P ≥ d_f ; P′ = 0 caso contrário
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `P′` | precipitação transformada, a ser fornecida ao Netuno 5 | mm |
| `P` | precipitação observada no dia | mm |
| `d_f` | lâmina de descarte de primeiras águas | mm |

Aplicada essa transformação, o cálculo `P_ef = max(0, P′ − d_f)` do Netuno 5
reproduz exatamente a semântica de limiar. A medição não corre o risco de validar
código que não é o distribuído.

> **Uma ressalva de documentação.** O protocolo de verificação interno instrui a
> usar uma opção automática para essa emulação. Essa opção **não está
> implementada**. Use a transformação da série, ou compare com descarte igual a zero,
> em que as duas regras coincidem.

---

## Os casos de referência nula

Em parte das linhas, o Netuno 4 exportou zero enquanto o Netuno 5 calcula valor
positivo. A incidência difere muito entre conjuntos: 0,35% em Manaus e São Paulo
contra 34,98% em Floripa e Brasília.

A disparidade aponta para característica dos **dados de referência** — provavelmente
o Netuno 4 não encontrou volume ótimo sob o seu próprio critério — e não para erro do
Netuno 5, que nunca devolve zero nesses casos. São segregados das estatísticas para
não as dominar.

---

## O que declarar num estudo comparativo

- os **dois números**: a divergência total e o resíduo depois da decomposição;
- as duas diferenças deliberadas, nomeadas;
- se a comparação foi feita com descarte zero, com emulação de limiar, ou sem
  neutralização;
- a versão de cada programa.

Apresentar apenas a divergência total, sem decompor, sugere um erro de motor que não
existe.
