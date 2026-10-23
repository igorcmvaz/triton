# Certificação EDGE no Triton

O EDGE (*Excellence in Design for Greater Efficiencies*) é uma criação do IFC, do
Grupo Banco Mundial, e a certificação é administrada pelo GBCI em mais de 120
países. No Brasil é a certificação de maior alcance em habitação, em boa medida
porque o aplicativo é gratuito e o limiar de entrada é único e explícito.

## O que o distingue das outras três já implementadas

O EDGE **não pontua**. O LEED soma pontos por crédito, o AQUA-HQE classifica
itens em níveis (PR, HQE, HQE 2, HQE 3), o Selo Casa Azul pontua critérios. O EDGE mede **percentual de
economia contra um caso-base local** em três barras independentes, e exige que
cada uma cruze o seu limiar.

| Nível | Exigência |
| :--- | :--- |
| EDGE Certified | ≥ 20% de economia em energia, em água **e** na energia incorporada aos materiais |
| EDGE Advanced (*Zero Carbon Ready*) | o anterior, mais ≥ 40% de economia de energia no local |
| Zero Carbon | o anterior, mais 100% de renovável, no local ou fora dele, ou compensação adquirida |

Fonte: IFC, *EDGE Certification Process*,
<https://edgebuildings.com/certify/certification/>, consultado em 10 de setembro
de 2026.

Repare que o nível avançado sobe **a barra de energia**, não a de água. Um
projeto de aproveitamento pluvial não muda de nível fazendo mais água: ele
garante a barra de água e o nível se decide na energia.

## A medida que este programa dimensiona

As medidas de água do EDGE são codificadas como WEM. A que interessa aqui é a
**WEM14, sistema de aproveitamento de água pluvial**, cuja entrada no aplicativo
é a **área de captação, em m²** — exatamente o parâmetro que o Triton já pede na
primeira aba.

| Código | Medida | O Triton modela? |
| :--- | :--- | :--- |
| WEM13 | Sistema eficiente de irrigação paisagística | Não. O programa modela o volume de irrigação e a supressão por chuva, não a eficiência do sistema de rega. |
| WEM14 | Sistema de aproveitamento de água pluvial | **Sim.** É o objeto do programa. |
| WEM15 | Tratamento e reúso de águas servidas | Não. Água cinza está fora do escopo. |

Os códigos foram conferidos contra um relatório de avaliação EDGE v3.0.0 emitido
para projeto residencial certificado, e não contra memória.

## O limite honesto: o caso-base

O numerador da barra de água é o volume de potável que a chuva substitui, e é o
que o Triton calcula dia a dia. O denominador é o **caso-base**, e esse o Triton
não tem como saber: ele é local, varia por país e por tipologia, e é fixado pelo
próprio aplicativo do IFC a partir de referências do mercado local.

Por isso a aba Ambiental tem um campo opcional, *Caso-base de consumo do EDGE
(L/pessoa·dia)*. Quando ele está preenchido, a barra é calculada contra ele.
Quando está em branco, o Triton usa a demanda modelada do projeto e diz que foi
isso que fez.

As duas coincidem quando a **única** medida de água do projeto é o sistema
pluvial. Se o projeto também tiver louças e metais eficientes, o caso-base do
EDGE é maior que a demanda modelada, e a contribuição da WEM14 medida contra ele
é percentualmente **menor** — embora a barra total do projeto seja maior. Nesse
caso o número do Triton é um **piso**, não o valor da certificação.

**A certificação sai do aplicativo EDGE, não daqui.** O que o Triton entrega é a
contribuição da WEM14, a área de captação a declarar no campo dela, e a distância
até o limiar.

## Onde aparece

- **Aba Ambiental → ESG:** cartão «EDGE (IFC): Barra de Água», com o percentual,
  se atende ao padrão e, no rótulo suspenso, a área de captação a declarar.
- **Matriz de créditos:** linha com código WEM14, ao lado do LEED, do AQUA-HQE,
  do Casa Azul e do GRI 303.
- **Relatório ambiental em HTML e PDF:** cartão próprio na seção de certificações.
- **Relatório executivo em texto:** uma linha com o percentual e a área.
- **Aba Documentação:** capítulo 5 da página de certificações, em português e
  inglês.

## O que ficou de fora, e por quê

O Triton não avalia as barras de **energia** e de **materiais**, e portanto não
diz se um projeto é EDGE Certified. Diria isso com base em um terço da evidência.
A barra de energia do EDGE cobre a edificação inteira — envoltória, climatização,
aquecimento de água, iluminação — e o programa só conhece o consumo do
bombeamento pluvial. A de materiais depende da composição construtiva completa,
enquanto a avaliação de ciclo de vida daqui cobre o sistema pluvial.

Informar as três barras exigiria um modelo de edificação que este programa não
tem e não pretende ter.
