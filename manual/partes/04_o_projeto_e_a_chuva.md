# 4. O projeto e a chuva

> Ao terminar este capítulo você terá um projeto criado, uma série de precipitação
> carregada e a captação definida. E saberá por que cada um desses três números
> importa mais do que parece.

Os dez capítulos desta parte constroem **um projeto só**, do começo ao fim. A cada
capítulo o estudo ganha uma camada, e o resultado muda. Guarde o arquivo: ele é o
mesmo até o capítulo 13.

## O projeto

Uma residência unifamiliar em Florianópolis. Quatro moradores, cobertura de
150 m² em telha cerâmica, cisterna enterrada no quintal. É o caso mais comum do
Brasil, e o mais estudado.

A escolha de Florianópolis não é sentimental: a série é longa, a estrutura tarifária
da CASAN é pública e auditável, e o regime de chuva é bem distribuído ao longo do
ano — o que, como o capítulo 7 vai mostrar, muda tudo na hora de escolher o volume.

---

## 4.1. A série de precipitação

Abra a etapa **1. Projeto e Chuva**. Há dois caminhos para a chuva.

**Arquivo próprio.** Um CSV com uma leitura diária por linha, em milímetros, em
coluna única. É o caminho de quem tem dados de uma estação específica, do INMET ou
da Agência Nacional de Águas.

**Base nacional.** 652 cidades brasileiras, 19 modelos climáticos do CMIP6 e três
cenários de emissão. É o caminho deste tutorial, e o guia 15 mostra como usar os
cenários futuros.

Para o nosso projeto, use a série de Florianópolis que acompanha o programa e recorte
os **30 primeiros anos**.

<!-- inclui: _tabelas/cap04_serie.md -->

Três números dessa tabela decidem o projeto, e vale olhar para eles antes de
qualquer simulação.

**1.795 mm por ano** é muita chuva. Florianópolis está entre as capitais mais
chuvosas do país, e isso significa que o fator limitante do sistema não será a
oferta de água, e sim a demanda e o tamanho do reservatório.

**Chove em 46% dos dias.** Chuva frequente e bem distribuída favorece
reservatórios pequenos: a cisterna se enche muitas vezes ao ano em vez de precisar
atravessar uma estiagem longa. Compare com Brasília, no guia 14, onde a mesma
lâmina anual cai concentrada em seis meses e exige o dobro do volume.

**Sete por cento dos dias têm chuva, mas abaixo de 2 mm.** Esses dias serão
descartados por inteiro, e o item 4.3 explica por quê.

> **Quantos anos de série usar.** Trinta é confortável. Abaixo de dez, o resultado
> começa a depender do trecho escolhido; abaixo de cinco, o viés do reservatório
> vazio no início da simulação passa a pesar de forma sensível. O capítulo 33 trata
> este engano em detalhe.

---

## 4.2. A área de captação

**150 m²**, e este é o primeiro lugar onde se erra.

A área de captação é a **projeção horizontal** da cobertura, e não a área
inclinada do telhado. Um telhado de 30% de inclinação sobre uma planta de 150 m²
tem cerca de 157 m² de superfície, mas capta os mesmos 150 m². A chuva cai na
vertical, e o que ela vê é a sombra da cobertura no chão.

A definição vem da NBR 10844: a soma das áreas das superfícies que, interceptando
chuva, conduzem as águas para determinado ponto da instalação, representada pela
projeção horizontal.

> **Atenção.** Usar a área inclinada superestima a captação na razão
> `1/cos(inclinação)`. Num telhado de 30% dá 4,4% a mais de água que não existe. Em
> telhados de maior caimento o erro cresce depressa.

---

## 4.3. O coeficiente de escoamento

**0,85**, para telha cerâmica.

O coeficiente representa a fração da chuva que efetivamente chega à cisterna.
Perde-se água por absorção do material, por evaporação na superfície quente, por
respingo e pelo molhamento inicial da telha a cada evento.

| Cobertura | Coeficiente usual |
| :--- | ---: |
| telha metálica | 0,90 a 0,95 |
| telha cerâmica | 0,80 a 0,90 |
| telha de fibrocimento | 0,80 a 0,90 |
| laje impermeabilizada | 0,80 a 0,85 |
| telhado verde | 0,20 a 0,50 |

O programa aceita valores entre 0 e 1, e recusa fora disso nomeando o campo. A aba
Documentação traz a tabela completa por material, inclusive coberturas mistas.

---

## 4.4. O descarte de primeiras águas

**2,0 mm, em todo evento de chuva.**

A primeira água que lava o telhado carrega poeira, folhas, fezes de aves e o que
mais tiver se depositado desde a última chuva. Descartá-la é a medida de qualidade
mais barata e mais eficaz de um sistema pluvial.

A NBR 15527 recomenda 2 mm quando não há dado local. É o valor deste tutorial.

O programa oferece **três modos**:

| Modo | Quando descarta | Quando usar |
| :--- | :--- | :--- |
| 1 | em todo evento de chuva | o padrão, e o mais conservador |
| 2 | só no primeiro evento após estiagem | dispositivo que não se esvazia sozinho entre chuvas próximas |
| 3 | a cada X dias | dispositivo com esvaziamento programado |

> **Atenção, e este é o ponto que mais surpreende.** Quando o descarte se aplica e a
> chuva do dia **não supera** a lâmina, perde-se o dia **inteiro**, e não a
> diferença. Um dia de 1,6 mm com descarte de 2,0 mm capta **zero**.
>
> Na série de Florianópolis, isso atinge 7% dos dias. Em climas de garoa frequente,
> como o litoral sul no inverno, pode passar de 20%.

A razão é física: o dispositivo de autolimpeza precisa encher antes de a água chegar
à cisterna. Se a chuva não o enche, nada passa adiante.

> **A lâmina não é o dispositivo.** `d_f` é uma lâmina em milímetros. O volume
> hidráulico do reservatório de autolimpeza é `A × d_f`, que no nosso projeto dá
> 150 × 2 = **300 litros**. Esse reservatório exige dimensionamento próprio, e o
> programa não o faz.

---

## 4.5. O que temos até aqui

| Dado | Valor |
| :--- | ---: |
| série | Florianópolis, 30 anos |
| área de captação | 150 m² |
| coeficiente de escoamento | 0,85 |
| lâmina de descarte | 2,0 mm, todo evento |

Com isso o programa já sabe **quanta água entra**. Falta dizer quanta sai, que é o
capítulo 5.

Um cálculo de guardanapo, para calibrar a expectativa: 1.795 mm por ano sobre 150 m²
a 0,85 de coeficiente dão cerca de 229 m³ por ano de água bruta, antes do descarte.
O capítulo 6 mostra quanto disso vira economia de verdade — e a diferença entre os
dois números é a lição mais importante do tutorial.
