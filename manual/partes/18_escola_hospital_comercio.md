# Simular escola, hospital e comércio

> **Pergunta que este guia responde:** o programa serve para edificação não
> residencial?

Serve, com uma ressalva grande que precisa ser lida antes, e não depois.

---

## A ressalva: a categoria tarifária

O catálogo de 652 municípios traz a **categoria residencial**, e só ela.

Concessionárias brasileiras cobram categorias diferentes de residência, comércio,
indústria e poder público, com tarifas que costumam ser **o dobro ou mais**. Na
tabela da CASAN de abril de 2026, a primeira faixa custa R$ 3,08/m³ no residencial e
R$ 6,81/m³ no comercial.

Quando você escolhe uma tipologia não residencial, o programa **avisa** e diz o
sentido do erro:

> A tipologia escolhida é «Escola», que a concessionária fatura na categoria
> Pública. O catálogo do programa tem apenas a categoria Residencial, de modo que a
> conta de água está sendo calculada com a tarifa errada. O erro tem sentido
> conhecido: as categorias não residenciais são mais caras, e portanto a economia e
> o retorno estão **subestimados**.

> **O que fazer.** Lance a estrutura da categoria correta da sua concessionária no
> modo personalizado do diálogo de tarifas. A seção {{n:16}} ensina. Sem isso, o resultado
> técnico é válido e o **econômico não é publicável**.

A boa notícia é que o erro é conservador: o projeto real rende **mais** do que o
programa mostra, e não menos.

---

## As tipologias disponíveis

| Tipologia | Categoria que a concessionária cobra | Unidade de consumo |
| :--- | :--- | :--- |
| residencial unifamiliar | residencial | L/hab·dia |
| residencial multifamiliar | residencial | L/hab·dia |
| escola | pública | L/aluno·dia |
| hospital | pública | L/leito·dia |
| escritório | comercial | L/pessoa·dia |
| hotel | comercial | L/hóspede·dia |
| comércio | comercial | L/pessoa·dia |
| indústria | industrial | conforme processo |

---

## O que muda em cada tipologia

**Escola.** O caso mais favorável do Brasil. A fração não potável é alta, porque
bacia sanitária domina o consumo e não há chuveiro nem cozinha em muitas unidades.
A demanda é modulada por calendário — use a seção {{n:17}} — e o fechamento nas férias
costuma coincidir com a estiagem no Sul e Sudeste, o que enche a cisterna de graça.

**Hospital.** O caso mais delicado. Consumo alto e contínuo, sem sazonalidade
relevante, o que é bom para o aproveitamento. Mas a **exigência de qualidade** é
outra: há usos que não admitem água pluvial em hipótese alguma, e a torre de
resfriamento, que seria um uso ideal, exige controle microbiológico contra
legionela. Trate a classe de qualidade com cuidado, e não use as classes adaptadas
2 a 4 como se fossem requisito normativo.

**Escritório e comércio.** Demanda concentrada em dias úteis, cinco dias em sete.
Module por semana. A fração não potável é altíssima, muitas vezes acima de 80%,
porque quase todo o consumo é bacia sanitária e limpeza.

**Hotel.** Sazonalidade forte, e é o caso em que modular por mês mais importa. Veja
a advertência da seção {{n:17}} sobre demanda em contrafase com a chuva.

---

## Micromedição e o número de economias

Em edifício multifamiliar com medição individualizada, informe o **número de
economias**. O programa avalia o consumo no patamar de **uma** unidade e multiplica
pelo número de economias.

Isso importa por causa das faixas progressivas: um prédio de vinte apartamentos com
medição individual paga vinte contas da primeira faixa, e não uma conta que soma
todo o consumo e cai na faixa mais cara. Tratar o prédio como uma unidade só
superestimaria a economia de forma grosseira.

---

## O que declarar

Além do que a seção {{n:13}} já pede:

- a **tipologia** e a unidade de consumo adotada;
- a **origem** do consumo per capita — medição, referência ou norma;
- se a **categoria tarifária** foi corrigida ou se ficou a residencial do catálogo,
  e neste caso que o resultado econômico está subestimado;
- o **perfil de modulação** e sua origem;
- para hospital, a classe de qualidade adotada e o que ela cobre.
