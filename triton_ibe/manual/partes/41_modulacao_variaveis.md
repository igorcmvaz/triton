# As variáveis e as distribuições

> **Pergunta a que esta secção responde:** o que posso sortear, e como descrevo a incerteza de cada
> premissa?

## O catálogo de variáveis

A ferramenta sorteia vinte premissas, organizadas em sete grupos. Ao abrir, só as três de consumo
vêm marcadas — o consumo per capita, o número de pessoas e a fração não potável —, porque são as
mais incertas num projeto novo e as que a literatura mostra moverem o resultado (Silva e Ghisi,
2016). As restantes ficam com o valor do estudo até o utilizador as marcar.

<!-- inclui: _tabelas/cap40_catalogo.md -->

Cada grupo atua num ponto diferente da cadeia de cálculo:

- **Procura** muda o consumo diário e a fração que a água da chuva pode satisfazer. A fração
  satisfazível total é recalculada a cada sorteio a partir da fração interior e da procura
  exterior, pela mesma regra do estudo (secção {{n:5}}). Nos modos semanal, mensal e diário, as
  séries recebem o fator sorteado: o perfil do calendário mantém-se, e o nível muda.
- **Captação** muda o volume de chuva que chega à cisterna: área, coeficiente de escoamento e
  lâmina de descarte.
- **Chuva** multiplica toda a série diária por um fator. É a forma mais simples de representar uma
  chuva futura mais seca ou mais húmida do que a histórica.
- **Tarifas** muda o preço da água, do saneamento e da energia e as respetivas atualizações.
- **Custos** muda o investimento inicial e o custo anual de exploração e manutenção.
- **Fluxo de caixa** muda a taxa de atualização e o horizonte da análise.
- **Ambiente** muda os fatores de emissão da avaliação de ciclo de vida.

## O que cada variável económica multiplica ou substitui

As variáveis económicas são de dois tipos. As que têm unidade própria — atualizações, taxa,
inflação, tarifa de energia, período — **substituem** o valor do projeto pelo sorteado. Os
**fatores** (×) multiplicam um valor do projeto e valem 1 no estudo: um fator sorteado de 1,15
representa um custo 15% acima do orçamentado. A tabela diz sobre o que atua cada um e o que deixa
de fora.

<!-- tabela: O que cada variável económica e ambiental faz no cálculo, e o que não toca -->
| Variável | Atua sobre | Não toca |
| :--- | :--- | :--- |
| Fator das tarifas de água e saneamento | todos os valores monetários da estrutura da água — escalões, parcela fixa, fatura mínima, preço-base da curva exponencial — e o saneamento cobrado em euros (fixo ou por m³) | o expoente da curva exponencial; o saneamento em % da água, que já acompanha a água |
| Fator do saneamento | a tarifa de saneamento, no modo declarado no projeto: a percentagem, o valor fixo ou o preço por m³ | a tarifa da água |
| Atualização tarifária | a atualização da água e do saneamento em cada período de atualização, no lugar da declarada | a atualização da energia |
| Tarifa de energia | o preço do kWh da bombagem, no lugar do declarado | — |
| Atualização da energia | a atualização da tarifa de energia em cada período | — |
| Fator do investimento | o investimento inicial **inteiro** de cada volume: cisterna, reservatório superior, eletrobomba, tubagem, acessórios, mão de obra e linha de tratamento | o custo anual de exploração |
| Fator do preço da cisterna | só o preço da cisterna de cada volume, a parte do investimento que cresce com o volume; com a mão de obra automática, esta acompanha-o, pela regra do programa | os restantes itens do investimento |
| Fator do custo de exploração (O&M) | o custo anual de exploração e manutenção: os itens declarados na etapa económica, o custo de exploração da linha de tratamento e o cloro | a energia da bombagem, que tem variáveis próprias |
| Inflação do custo de exploração | a atualização anual do custo de exploração, no lugar da declarada | as tarifas |
| Taxa de atualização | a taxa de desconto do fluxo de caixa | — |
| Período de análise | o horizonte do fluxo de caixa e da avaliação ambiental, em anos inteiros | a série de chuva, que continua a ser a do estudo |
| Fator da emissão da água potável | a emissão por m³ da água da rede que a cisterna evita | o carbono incorporado dos materiais |
| Fator da emissão da rede elétrica | o fator de emissão da energia da bombagem | o carbono incorporado dos materiais |

Os dois fatores de investimento combinam-se. Marcados em conjunto, a cisterna recebe o produto dos
dois, e o resto do investimento só o fator do investimento. Na prática, o fator do investimento
representa a incerteza do orçamento como um todo — região, época, imprevistos —, e o fator da
cisterna a do item que define o ótimo: como o preço da cisterna é a parte do custo que cresce com
o volume, é ele que desloca o volume de menor período de recuperação.

## A incerteza da chuva

A Edição Ibérica não tem base de séries de modelos climáticos, pelo que a incerteza da chuva
entra pelo **fator da chuva**. O fator multiplica toda a série diária do projeto — a série E-OBS
do concelho, a do Funchal ou um ficheiro do utilizador — e por isso mantém a sua estrutura
temporal: a sequência de estiagens e de dias chuvosos não muda, só o nível. Um fator sorteado com
média 1 e desvio de 0,10 representa uma chuva 10% mais húmida ou mais seca do que o registo, que
é a maneira de representar um clima futuro mais seco ou mais húmido do que o passado. Para testar
uma sequência diferente de estiagens, execute o estudo uma vez com cada série alternativa e
compare.

## As quatro distribuições

Cada variável marcada recebe uma distribuição e os respetivos parâmetros:

<!-- tabela: As quatro distribuições que a ferramenta oferece, os seus parâmetros e quando usar cada uma -->
| Distribuição | Parâmetros | Quando usar |
| :--- | :--- | :--- |
| normal | média e desvio-padrão | incerteza simétrica em torno de um valor provável |
| lognormal | média e desvio-padrão | grandeza positiva com cauda para cima, como o consumo e o preço da obra |
| triangular | mínimo, moda e máximo | quando se conhecem o intervalo e o valor mais provável, mas não a forma |
| uniforme | mínimo e máximo | quando só se conhece o intervalo |

Na lognormal, a média e o desvio introduzidos são os da própria variável, e não os do seu
logaritmo: o programa calcula os parâmetros da lognormal que devolvem exatamente a média e o
desvio pedidos. Qualquer distribuição pode ser **truncada** por um limite inferior e um superior;
o valor sorteado fora deles é sorteado de novo. O número de pessoas e o período de análise são
arredondados para inteiro e nunca ficam abaixo de 1; a fração não potável e o coeficiente de
escoamento ficam entre 0 e 100% e entre 0 e 1; fatores, preços, áreas e consumos nunca ficam
negativos.

Cada cartão do ecrã mostra a curva da distribuição escolhida, desenhada com 4 000 sorteios, e os
respetivos percentis 5 e 95. É a maneira mais rápida de verificar se a largura declarada é
plausível: um P95 de 400 L/hab.dia para uma habitação indica um desvio exagerado.

## O nível, e não o ruído do dia

As variáveis são sorteadas **uma vez por realização**: em cada realização, a casa tem um consumo
per capita, uma ocupação e uma fração, válidos para toda a série de chuva. Isto representa a
incerteza sobre **quanto** o edifício consome, que é a que importa. A variação de um dia para o
outro em torno desse nível, opcional (campo «Variação diária»), quase não move o resultado:
sorteada de forma independente a cada dia, anula-se ao longo de trinta anos de série (Silva e
Ghisi, 2016; secção {{n:19}}, subcomando `stochastic-demand`).
