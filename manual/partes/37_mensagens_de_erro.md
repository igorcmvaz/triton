# 37. Mensagens de erro e o que fazer

> O que cada mensagem significa, o que a disparou, e como resolver.

O programa prefere **recusar** uma entrada impossível a corrigi-la em silêncio. Área
negativa é erro de digitação, e quem digitou precisa ver.

---

## 37.1. Validação física da entrada

Estas são levantadas antes de qualquer cálculo, e nomeiam o campo e o valor
recebido.

| Mensagem | O que a disparou | O que fazer |
| :--- | :--- | :--- |
| «Volume do reservatório inferior negativo» | volume menor que zero | corrija; **zero é válido** e representa o cenário sem sistema |
| «Volume do reservatório superior negativo» | idem, na caixa elevada | corrija; zero significa sem caixa |
| «Área de captação negativa» | área menor que zero | corrija; use a projeção horizontal em m² |
| «Coeficiente de escoamento fora de [0, 1]» | coeficiente negativo ou acima de 1 | acima de 1 a cobertura entregaria mais água do que a chuva traz; telhados usuais ficam entre 0,80 e 0,95 |
| «Lâmina de descarte negativa» | descarte menor que zero | o descarte retira água da captação, não acrescenta |
| «Demanda diária negativa» | demanda menor que zero | corrija |
| «Fração atendível fora de [0, 1]» | fração maior que 1 | informe 0,4 para 40%, e não 40 |

> A última é a mais frequente. O campo aceita fração **ou** percentual em alguns
> pontos da interface e só fração no núcleo; quando a mensagem aparecer, é porque o
> valor chegou como 40 em vez de 0,4.

---

## 37.2. Varredura

| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «O volume máximo da varredura deve ser finito e não negativo» | campo vazio ou negativo | informe o volume máximo em litros |
| «O passo de varredura deve ser finito e maior que zero» | passo zero ou vazio | informe o passo; ele será arredondado para o múltiplo de 250 L |

Um aviso que **não** é erro: quando o passo é ajustado para o múltiplo de 250 L ou
pelo limite de 40 volumes, o programa registra o ajuste e segue. Declare o passo
efetivo no seu estudo, e não o pedido.

---

## 37.3. Cloração

| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Pureza deve ficar em (0, 1]» | pureza informada como percentual | informe 0,65 para 65%, e não 65 |
| «Dose negativa» | dose menor que zero | corrija |

---

## 37.4. Motobomba

| Mensagem | Causa | Solução |
| :--- | :--- | :--- |
| «Rendimento deve ficar em (0, 1]» | rendimento como percentual no núcleo | use 0,55 para 55% |
| «Rendimento do motor deve ficar em (0, 1]» | idem, no campo do motor | deixe em branco para o programa adotar a tabela da NBR 17094-2 |

---

## 37.5. Arquivos

| Situação | O que acontece | O que fazer |
| :--- | :--- | :--- |
| série de chuva ilegível | a leitura é interrompida com mensagem | confira o formato: uma leitura por linha, em mm, coluna única |
| arquivo `.netuno` com JSON inválido | a abertura é interrompida | o arquivo pode estar truncado; recorra à cópia de segurança |
| seção ausente no arquivo | os campos caem no padrão da classe | esperado ao abrir arquivo de versão anterior; revise a aba correspondente |
| base climática não instalada | a aba oferece só arquivo próprio | veja o capítulo 2 |

---

## 37.6. Avisos que não interrompem

Estes não impedem o cálculo. São observações que o programa faz e que **precisam ir
para o estudo**.

| Aviso | O que significa |
| :--- | :--- |
| tipologia não residencial com tarifa residencial | o resultado econômico está **subestimado**; veja o guia 18 |
| a classe alvo recomenda filtração fina e ela foi dispensada | decisão registrada no relatório |
| fator de emissão com rótulo de triagem | o fator não tem fonte primária; declare-o |
| estrutura tarifária incompleta | a tabela do município tem lacuna; confira contra a resolução |
| passo de varredura ajustado | o passo efetivo difere do pedido |
| extrapolação de preço com R² baixo | o volume está fora da tabela de preços e a regressão não é confiável |

---

## 37.7. Quando o resultado parece errado

Antes de suspeitar do programa, três conferências que resolvem a maioria dos casos:

**O potencial saiu maior que o esperado.** Confira a fração atendível: ela é o teto,
e uma fração alta demais infla tudo.

**O potencial saiu muito menor.** Confira a lâmina de descarte, e lembre do capítulo
33.3: o campo quer **milímetros**, não litros.

**O payback saiu absurdo.** Confira o regime tarifário do município. É a causa mais
comum, e o guia 16 traz o teste que a identifica.

E percorra as etapas de entrada antes de acreditar no resultado. A barra lateral
marca as que ainda têm pendência, e é mais rápido conferir as quatro telas de entrada
do que descobrir o engano no relatório.
