# 1. O que o Netuno faz, e o que ele não faz

O Netuno simula sistemas de aproveitamento de água pluvial em edificações. Dado o
regime de chuva de um lugar, a cobertura de um edifício e o consumo de quem o ocupa,
ele responde **quanto de água potável o sistema substitui**, e a que custo, com que
qualidade e com que impacto de carbono.

---

## 1.1. O método, em dois parágrafos

O programa usa um **modelo comportamental de base diária**. Para cada dia da série de
precipitação, ele resolve o que entra no reservatório, o que transborda, o que é
consumido e o que sobra para o dia seguinte. Não há distribuição de probabilidade nem
valor médio anual: há a série, dia após dia, e a mesma conta repetida.

Isso importa porque a chuva **não** chega distribuída. Ela chega concentrada em
poucos dias, enche a cisterna de uma vez, transborda, e depois faz falta duas semanas
mais tarde. Um cálculo por médias mensais não enxerga esse descasamento e
superestima sistematicamente o aproveitamento. O capítulo 23 mostra o fenômeno
acontecendo, dia a dia, numa tabela de dez dias que o leitor pode refazer na
planilha.

---

## 1.2. As seis dimensões

| Dimensão | Pergunta que responde | Capítulos |
| :--- | :--- | :--- |
| **técnica** | quanta água o sistema entrega, e com que confiabilidade | 23 a 26 |
| **qualidade** | que tratamento o uso exige, e quanto custa | 27 |
| **econômica** | em quanto tempo se paga, e quanto rende | 29 |
| **ambiental** | quanto carbono evita, e em quanto tempo | 30 |
| **certificação** | onde o projeto se enquadra em cinco referenciais | 31 |
| **decisão** | qual volume escolher, entre critérios que discordam | 32 |

A última é a que distingue o programa de uma planilha. As outras cinco produzem
respostas que **discordam entre si**, e a sexta existe para escolher com os pesos
declarados em vez de escondidos.

---

## 1.3. O que o programa **não** faz

Começar pelos limites é incomum, e é deliberado. Poupa o tempo de quem abriu o
programa esperando outra coisa.

**Não dimensiona a instalação hidráulica.** Não calcula traçado, diâmetro por trecho,
perda de carga nem declividade. O esquema exportado em DXF é um esquema, e o projeto
executivo é do projetista.

**Não dimensiona o dispositivo de descarte.** A lâmina `d_f` é um parâmetro do
balanço; o reservatório de autolimpeza, de volume `A × d_f`, exige dimensionamento
hidráulico à parte.

**Não substitui ensaio de qualidade de água.** Ele dimensiona equipamento de
tratamento a partir de premissas. As constantes do modelo de lavagem da cobertura não
são calibradas contra medição, e a qualidade resultante é premissa, não resultado.

**Não modela sub-passo horário.** Uma chuva de 40 mm em duas horas e a mesma lâmina
em vinte e quatro horas dão o mesmo resultado.

**Não faz inventário completo de ciclo de vida.** A avaliação é de **triagem**, numa
única categoria de impacto — carbono. Não há eutrofização, acidificação, uso do solo
nem toxicidade.

**Não certifica.** Ele mostra onde o projeto se enquadraria. A certificação é
decidida pelo organismo certificador, com a documentação completa do empreendimento.

**Não conhece o sítio.** Não sabe se o volume cabe no terreno, se há lençol freático
alto, nem se a estrutura suporta a caixa elevada.

O capítulo 36 traz a lista completa de limitações conhecidas, com as consequências de
cada uma.

---

## 1.4. Para quem serve

| Quem | O que encontra aqui |
| :--- | :--- |
| **estudante** | o tutorial da Parte 2, um estudo do começo ao fim |
| **projetista** | os guias da Parte 3, e o roteiro do capítulo 3 |
| **pesquisador** | o método da Parte 4, com procedência de cada número |
| **revisor** | a Parte 6, verificação e limites declarados |

---

## 1.5. O que mudou do Netuno 4

O Netuno 4 é o antecessor, publicado em 2014 pelo mesmo grupo. O Netuno 5 mantém o
modelo conceitual — balanço comportamental diário — e acrescenta seis dimensões de
análise que não existiam.

Há **duas diferenças deliberadas de método**, e quem comparar resultados das duas
versões precisa declará-las:

**O tratamento do descarte.** O Netuno 4 trata a lâmina como **limiar do evento**:
abaixo dela nada é captado, acima dela capta-se a chuva inteira. O Netuno 5
**subtrai** a lâmina, o que é fisicamente mais fiel.

**O critério de volume ótimo.** As implementações e as grades diferem.

Juntas, as duas respondem por 91% da divergência medida entre os programas. Sobre
4.050 casos de referência, o Netuno 5 estima de 2,3 a 2,7 pontos percentuais menos
economia. **Neutralizadas as duas, o motor reproduz o Netuno 4 com erro médio de 0,25
ponto percentual e 100% dos casos dentro de 5 pontos.**

O capítulo 35 traz a decomposição completa.

---

## 1.6. Uma palavra sobre resultados

Todo número que o programa produz é **condicional às premissas declaradas**. Ele não
descobre verdades; ele calcula consequências.

Por isso o manual insiste tanto em declaração. O capítulo 13 traz a lista do que
precisa constar num artigo, o capítulo 33 traz os dez enganos que o programa não
impede, e o 36 traz o que ele não cobre.

Um estudo que declara suas premissas e seus limites é mais útil — e mais defensável —
que um que apresenta um número sozinho.
