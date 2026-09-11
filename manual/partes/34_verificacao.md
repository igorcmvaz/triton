# Como o programa é verificado

> Este capítulo descreve a suíte de verificação, para que um revisor possa julgar o
> grau de confiança de um resultado produzido pelo programa.

Um programa científico sem verificação declarada é uma afirmação sem evidência. Este
capítulo é a evidência.

---

## A suíte

Novecentas asserções em noventa arquivos, organizadas em cinco famílias:

| Família | Arquivos | O que guarda |
| :--- | ---: | :--- |
| unitários | 63 | o comportamento de cada módulo isolado |
| invariantes | 11 | propriedades que **não podem** ser violadas |
| integração | 8 | o percurso da informação entre módulos |
| interface | 4 | que o controle da tela chega ao cálculo |
| desempenho | 4 | que o núcleo compilado não regride |

A suíte roda inteira a cada alteração do código. Nenhuma alteração é aceita com um
teste vermelho.

---

## As invariantes

São a família mais importante, porque testam **propriedades**, e não valores.

**Conservação de massa.** Sobre séries de dez anos, o captado tem de igualar o
extravasado mais o consumido mais o armazenado. O resíduo medido é da ordem de
10⁻¹⁴ por cento do captado.

**Fechamento do balanço de demanda.** A demanda total tem de ser a soma de três
parcelas: pluvial consumido, potável comprado e demanda não atendida.

**Faixa do potencial.** O potencial de economia tem de ficar em [0, 100], para toda
combinação de volume, coeficiente e área. Sessenta combinações são verificadas.

**Teto da fração atendível.** O potencial nunca ultrapassa a fração de demanda
atendível por chuva, verificado até volumes de 100 m³.

**Paridade entre motores.** O núcleo compilado e o laço de referência têm de
devolver o mesmo número, para reservatório único e duplo, com e sem suprimento de
reserva da irrigação. A tolerância exigida é 10⁻⁹.

**Monotonicidade.** Mais volume nunca reduz o potencial; mais demanda nunca o
aumenta.

---

## Casos analíticos

Um conjunto de casos com **solução fechada**, em que o resultado correto é conhecido
sem simular: chuva constante, demanda constante, reservatório infinito, reservatório
nulo. São o teste mais forte que existe, porque não dependem de valor de referência
produzido pelo próprio programa.

---

## Testes de percurso

A família que nasceu do defeito mais persistente deste programa: **um valor
calculado corretamente que não chega a quem deveria consumi-lo**.

São invisíveis a testes de fórmula, porque cada parte isolada está certa. Só um teste
de **percurso** os pega: mudar a entrada na tela e verificar que o resultado final
se move.

Exemplos de defeitos que esta família encontrou e hoje guarda:

- a escolha de desinfecção não chegava à avaliação de ciclo de vida;
- desmarcar o filtro de polimento não surtia efeito nas classes 2 a 4;
- os quatro campos de imposto eram zerados pela tela ao fechar;
- a bandeira do suprimento de reserva da irrigação não chegava aos núcleos
  compilados;
- trinta dos oitenta e sete campos de então não sobreviviam a salvar e reabrir o
  projeto.

---

## Os números do manual

Uma família própria, criada com este manual: **cada valor impresso tem asserção**.

Os números da seção {{n:23}}, os do tutorial inteiro, cada linha da tabela dos dez dias,
e a exigência de que certos capítulos declarem certas ressalvas. Quando o programa
muda, o teste falha e aponta a página.

É o que impede um manual inteiro de envelhecer em silêncio.

---

## Verificação contra o Netuno 4

Quatro mil e cinquenta casos de referência, com a decomposição da diferença por
causa. A seção {{n:35}} trata.

---

## O que a verificação **não** prova

Distinção que um revisor cobra, e com razão.

**Verificação** responde: o programa resolve corretamente as equações que
implementa? Isso é o que a suíte testa.

**Validação** responde: as equações representam a realidade? Isso exige **medição em
campo** — sistemas instalados, monitorados, comparados com a simulação.

O programa é verificado. A validação do modelo comportamental de base diária apoia-se
na literatura da área, e não em medição própria. Um estudo que apresente resultados
do programa como medição estaria errado.

---

## Quem roda a suíte, e quando

A suíte acompanha o **código-fonte** do programa, e não a instalação: ela é executada
pelo grupo de pesquisa a cada alteração, antes de qualquer versão ser publicada.

O que isso significa para você, que usa o programa instalado: a versão que está na sua
máquina passou pelas novecentas asserções descritas neste capítulo, incluindo as que
conferem cada número impresso neste manual.

> **Aprofundamento: verificar por conta própria.** O código-fonte é público, sob
> licença GPL v3, e a suíte roda com um único comando no ambiente de
> desenvolvimento. Um revisor que queira conferir as invariantes — fechamento de
> massa, monotonicidade, paridade entre os dois motores de cálculo — encontra no
> repositório os arquivos de teste organizados por tema, e a seção {{n:B}} liga cada
> processo do programa ao que o verifica.
