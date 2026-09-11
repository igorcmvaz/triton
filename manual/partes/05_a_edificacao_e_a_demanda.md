# A edificação e a demanda

> Ao terminar esta seção o programa saberá **quanta água sai** e, mais importante,
> **qual parte dela a chuva pode atender**. Essa fração é o teto de tudo o que vem
> depois.

A seção {{n:4}} definiu a oferta. Este define a demanda. E há uma assimetria que
convém entender desde já: **a chuva não pode atender toda a demanda**, por mais
água que haja. Existe um teto, ele é definido aqui, e nenhum reservatório o
ultrapassa.

---

## A tipologia

Na etapa **2. Edificação Consumo**, escolha *Residencial unifamiliar*. O programa traz oito
tipologias, cada uma com o consumo per capita de referência e a repartição usual dos
usos finais:

<!-- tabela: Consumo per capita de referência por tipologia de edificação -->
| Tipologia | Per capita usual |
| :--- | ---: |
| residencial unifamiliar | 120 a 200 L/hab·dia |
| residencial multifamiliar | 100 a 180 L/hab·dia |
| escola | 10 a 50 L/aluno·dia |
| escritório | 50 a 80 L/pessoa·dia |
| hospital | 250 a 600 L/leito·dia |
| hotel | 100 a 300 L/hóspede·dia |
| indústria | conforme processo |
| comércio | 8 a 20 L/pessoa·dia |

A tipologia serve de ponto de partida, não de imposição: o valor continua editável.
A seção {{n:18}} trata dos casos não residenciais, que têm uma armadilha própria na tarifa.

---

## Os moradores e o consumo

**Quatro moradores, 150 L/hab·dia.** Total de **600 L/dia**.

O valor de 150 L/hab·dia é o consumo de uma residência de classe média com
abastecimento regular. Se você tem a conta de água da edificação, use-a: divida o
consumo mensal em litros por trinta e pelo número de moradores. O número medido vale
mais que qualquer referência.

O programa aceita demanda **constante** ou modulada por semana, mês ou dia. O
tutorial usa constante; a seção {{n:17}} mostra a modulação, que importa em escola, hotel e
qualquer edificação com sazonalidade.

---

## A fração que a chuva pode atender

**40%.** É o número mais importante desta seção.

Água de chuva não vai para o chuveiro, para a pia da cozinha nem para beber. Vai
para bacia sanitária, máquina de lavar roupa, lavagem de piso, rega de jardim e
lavagem de veículo. A fração desses usos no consumo total é o **teto do potencial
de economia**.

Repartição usual numa residência brasileira:

<!-- tabela: Repartição do consumo residencial por uso final e atendimento por água pluvial -->
| Uso final | Fração do consumo | Atende com chuva? |
| :--- | ---: | :---: |
| chuveiro | 25 a 35% | não |
| bacia sanitária | 20 a 30% | **sim** |
| máquina de lavar roupa | 10 a 15% | **sim** |
| pia da cozinha | 10 a 15% | não |
| lavatório | 5 a 10% | não |
| usos externos | 5 a 15% | **sim** |

Somando os três que a chuva atende, chega-se aos 40% do tutorial. É um valor
defensável para residência unifamiliar sem jardim grande.

![A repartição do consumo numa residência, e a parte que a chuva pode atender](../figuras/fig00c_fracao.png)

*Figura 3 — Em cinza, os usos que exigem água potável; em verde, os que não exigem. A soma dos verdes é a fração atendível, e é o teto do potencial de economia.*

> **Este número é o teto.** Com 40% de fração atendível, o potencial de economia
> **jamais** passa de 40%, por maior que seja o reservatório e por mais que chova.
> A tabela da seção {{n:7}} mostra a curva se aproximando exatamente desse limite e
> nunca o cruzando.
>
> Quem quer passar de 40% precisa mudar o **uso**, não o reservatório: acrescentar a
> lavagem de piso, tratar a água a uma classe superior, ou reduzir o consumo
> potável.

---

## Discretizar os usos, ou não

O programa aceita dois níveis de detalhe na descrição da demanda, e a escolha entre eles
depende do que o estudo pretende responder.

No **modo simplificado**, informa-se uma fração única — os 40% deste tutorial — e o
programa trata toda a demanda atendível como um bloco homogêneo. É o modo adotado aqui e
é suficiente para a maior parte dos estudos, porque o resultado agregado não depende de
como as parcelas se distribuem internamente.

No **modo discretizado**, a demanda é separada em três parcelas: a potável interna, que a
chuva nunca atende; a não potável interna, que é a prioridade do sistema; e a irrigação,
atendida por último. A separação muda duas coisas. Altera a ordem de atendimento nos dias
de escassez, em que o uso interno tem precedência sobre o jardim; e permite distinguir uso
interno de uso externo nos créditos de certificação, distinção que o LEED exige em
créditos separados, conforme a seção {{n:31}} descreve.

Vale discretizar quando há jardim de área relevante, quando a certificação está no
horizonte do projeto, ou quando a irrigação pode ser suprimida em dias de chuva — situação
que o item seguinte trata.

---

## A irrigação e a supressão por chuva

Declarado um volume de irrigação, o programa oferece um limiar de supressão por chuva:
nos dias em que a precipitação supera esse limiar, o jardim não é regado. O comportamento
reproduz o de qualquer controlador de irrigação dotado de sensor de chuva, equipamento
corrente e barato, e ignorá-lo superestimaria a demanda externa ao longo do ano inteiro. O
limiar adotado por padrão é de 2 mm diários.

> **A série de chuva é lida duas vezes.** Uma leitura vira volume captado, depois do
> descarte. A outra decide se o jardim é regado. As duas são independentes: um dia
> pode suprimir a irrigação **e** render captação.

Resta uma escolha que merece atenção particular, porque altera o resultado econômico e
não é neutra: o **suprimento de reserva** da irrigação. Com ele ligado, a rede pública
rega o jardim nos dias secos em que a cisterna não dá conta, e esse volume entra na conta
de água como consumo potável. Com ele desligado, o jardim simplesmente não é regado
naquele dia, a edificação não compra essa água, e o volume correspondente aparece no
balanço como *demanda não atendida* — a terceira parcela tratada na seção {{n:23}}.

==A distinção entre as duas configurações é conceitual antes de ser numérica.== Um jardim
que precisa ser regado todos os dias representa uma demanda real, que alguém pagará; um
jardim que aceita não ser regado num dia seco representa uma conveniência, e tratá-lo como
demanda infla tanto o consumo quanto a economia aparente do sistema.

---

## O que temos até aqui

<!-- tabela: Estado do projeto do tutorial ao fim da definição da demanda -->
| Dado | Valor |
| :--- | ---: |
| tipologia | residencial unifamiliar |
| moradores | 4 |
| consumo per capita | 150 L/hab·dia |
| demanda total | 600 L/dia |
| fração atendível por chuva | 40% |
| **demanda pluvial** | **240 L/dia** |

O programa agora sabe a oferta e a demanda. Antes de simular, um confronto que vale
guardar:

<!-- tabela: Confronto entre a oferta anual de água pluvial e a demanda atendível -->
| | m³/ano |
| :--- | ---: |
| água bruta que cai na cobertura | 229 |
| o que sobra depois do descarte | 187 |
| **demanda pluvial do ano** | **88** |

Sobra água. Sobra **o dobro** da que se pretende usar. Se o único limite fosse a
oferta, o sistema atenderia 100% da demanda pluvial e chegaria aos 40% de teto.

Ele não chega, e a seção {{n:6}} mostra por quê.
