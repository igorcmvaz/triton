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

O programa aceita dois níveis de detalhe.

**Modo simplificado.** Você informa a fração única de 40%, e o programa trata tudo
como um bloco. É o modo do tutorial, e é suficiente para a maioria dos estudos.

**Modo discretizado.** Você separa a demanda em três parcelas: potável interna,
não potável interna e irrigação. O programa passa a atender com prioridade o uso
interno não potável e só depois a irrigação, e a distinguir as duas nos créditos de
certificação — o LEED separa uso interno de uso externo em créditos diferentes, como
a seção {{n:31}} mostra.

Vale discretizar quando há jardim relevante, quando a certificação está no
horizonte, ou quando a irrigação pode ser suprimida em dias de chuva.

---

## A irrigação e a supressão por chuva

Se você declarar um volume de irrigação, aparece um limiar de supressão: nos dias em
que a chuva superar esse limiar, o programa **não rega o jardim**. É o
comportamento de qualquer controlador com sensor de chuva, e ignorá-lo superestima
a demanda externa.

O limiar padrão é 2 mm por dia.

> **A série de chuva é lida duas vezes.** Uma leitura vira volume captado, depois do
> descarte. A outra decide se o jardim é regado. As duas são independentes: um dia
> pode suprimir a irrigação **e** render captação.

Há ainda uma escolha que merece atenção: **o suprimento de reserva**. Ligado, a rede
pública rega o jardim nos dias secos em que a cisterna não dá conta. Desligado, o
jardim simplesmente não é regado, e a edificação **não compra** essa água — o
volume aparece como *demanda não atendida*, a terceira parcela do balanço.

A escolha muda o resultado econômico, e não é neutra. Um jardim que precisa ser
regado todo dia é uma demanda; um jardim que aceita não ser regado num dia seco é
uma conveniência.

---

## O que temos até aqui

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

| | m³/ano |
| :--- | ---: |
| água bruta que cai na cobertura | 229 |
| o que sobra depois do descarte | 187 |
| **demanda pluvial do ano** | **88** |

Sobra água. Sobra **o dobro** da que se pretende usar. Se o único limite fosse a
oferta, o sistema atenderia 100% da demanda pluvial e chegaria aos 40% de teto.

Ele não chega, e a seção {{n:6}} mostra por quê.
