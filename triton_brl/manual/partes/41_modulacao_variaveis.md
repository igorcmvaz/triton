# As variáveis e as distribuições

> **Pergunta que esta seção responde:** o que posso sortear, e como descrevo a incerteza
> de cada premissa?

## O catálogo de variáveis

A ferramenta sorteia vinte premissas, organizadas em sete grupos, e pode sortear também o
modelo climático que fornece a chuva. Ao abrir, só as três de consumo vêm marcadas — o per
capita, o número de pessoas e a fração não potável —, porque são as mais incertas num
projeto novo e as que a literatura mostra mover o resultado (Silva e Ghisi, 2016). As
demais ficam com o valor do estudo até que o usuário as marque.

<!-- inclui: _tabelas/cap40_catalogo.md -->

Cada grupo age num ponto diferente da cadeia de cálculo:

- **Demanda** muda o consumo diário e a fração que a água de chuva pode atender. A fração
  total atendível é recalculada a cada sorteio a partir da fração interna e da demanda
  externa, pela mesma regra do estudo (seção {{n:5}}). Nos modos semanal, mensal e diário,
  as séries recebem o fator sorteado: o perfil do calendário se mantém, e o nível muda.
- **Captação** muda o volume de chuva que chega à cisterna: área, coeficiente de
  escoamento e lâmina de descarte.
- **Chuva** multiplica toda a série diária por um fator. É a forma mais simples de
  representar uma chuva futura mais seca ou mais úmida que a histórica. O sorteio entre
  modelos climáticos, descrito adiante, troca a própria série.
- **Tarifas** muda o preço da água, do esgoto e da energia e os seus reajustes.
- **Custos** muda o investimento inicial e o custeio anual de operação e manutenção.
- **Fluxo de caixa** muda a taxa de desconto e o horizonte da análise.
- **Ambiente** muda os fatores de emissão da avaliação de ciclo de vida.

## O que cada variável econômica multiplica ou substitui

As variáveis econômicas são de dois tipos. As que têm unidade própria — reajustes, taxa,
inflação, tarifa de energia, período — **substituem** o valor do projeto pelo sorteado. Os
**fatores** (×) multiplicam um valor do projeto e valem 1 no estudo: um fator sorteado de
1,15 representa um custo 15% acima do orçado. A tabela diz em que cada um age e o que fica
de fora.

<!-- tabela: O que cada variável econômica e ambiental faz no cálculo, e o que ela não toca -->
| Variável | Age sobre | Não toca |
| :--- | :--- | :--- |
| Fator das tarifas de água e esgoto | todos os valores em reais da estrutura de água — faixas, parcela fixa, conta mínima, preço-base da curva exponencial — e o esgoto cobrado em reais (fixo ou por m³) | o expoente da curva exponencial; o esgoto em % da água, que já acompanha a água |
| Fator do esgoto | a tarifa de esgoto, no modo declarado no projeto: a porcentagem, o valor fixo ou o preço por m³ | a tarifa de água |
| Reajuste tarifário | o reajuste da água e do esgoto em cada período de reajuste, no lugar do declarado | o reajuste da energia |
| Tarifa de energia | o preço do kWh do bombeamento, no lugar do declarado; a bandeira tarifária continua somada | — |
| Reajuste da energia | o reajuste da tarifa de energia em cada período | — |
| Fator do investimento | o investimento inicial **inteiro** de cada volume: cisterna, reservatório superior, motobomba, tubulação, acessórios, mão de obra e linha de tratamento | o custeio anual |
| Fator do preço da cisterna | só o preço da cisterna de cada volume, a parte do investimento que cresce com o volume; com a mão de obra automática, ela acompanha, pela regra do programa | os demais itens do investimento |
| Fator do custeio (O&M) | o custo anual de operação e manutenção: os itens declarados na etapa econômica, o custeio da linha de tratamento e o cloro | a energia do bombeamento, que tem variáveis próprias |
| Inflação do custeio | a correção anual do custeio, no lugar da declarada | as tarifas |
| Taxa mínima de atratividade | a taxa de desconto do fluxo de caixa | — |
| Período de análise | o horizonte do fluxo de caixa e da avaliação ambiental, em anos inteiros | a série de chuva, que continua a do estudo |
| Fator da emissão da água potável | a emissão por m³ da água da rede que a cisterna evita | o carbono incorporado dos materiais |
| Fator da emissão da rede elétrica | o fator de emissão da energia do bombeamento | o carbono incorporado dos materiais |

Os dois fatores de investimento se combinam. Marcados juntos, a cisterna recebe o produto
dos dois, e o restante do investimento só o fator do investimento. Na prática, o fator do
investimento representa a incerteza do orçamento como um todo — região, época,
imprevistos —, e o fator da cisterna, a do item que define o ótimo: como o preço da
cisterna é a parte do custo que cresce com o volume, é ele que desloca o volume de menor
payback.

## Os modelos climáticos

> **Só na Edição Brasil (BRL).**

Quando a chuva do projeto vem da base CLIMBra (seção {{n:15}}), a ferramenta oferece a
lista dos dezenove modelos climáticos da base. Cada realização sorteia, com igual
probabilidade, a série de um dos modelos marcados, para a mesma cidade, o mesmo cenário e
o mesmo recorte de datas do projeto. O fator da chuva, se marcado, multiplica a série
sorteada.

O sorteio entre modelos representa a incerteza que um fator único não capta: os modelos
discordam não só no total anual, mas na sequência de estiagens e de dias chuvosos, que é o
que esvazia ou enche a cisterna. Marcar todos os modelos dá a cada um o mesmo peso — a
convenção usual quando não há razão para preferir um deles. Com nenhum marcado, todas as
realizações usam a série do projeto. O caso-base usa sempre a série do projeto.

Com a chuva lida de um arquivo próprio, a lista fica desativada: os dezenove modelos só
existem, para a mesma cidade, na base CLIMBra.

> **Na International Edition (INT).** A base CLIMBra não existe nesta edição, e a lista
> de modelos não aparece. A incerteza da chuva se representa pelo fator da chuva.

## As quatro distribuições

Cada variável marcada recebe uma distribuição e os seus parâmetros:

<!-- tabela: As quatro distribuições que a ferramenta oferece, os seus parâmetros e quando usar cada uma -->
| Distribuição | Parâmetros | Quando usar |
| :--- | :--- | :--- |
| normal | média e desvio-padrão | incerteza simétrica em torno de um valor provável |
| lognormal | média e desvio-padrão | grandeza positiva com cauda para cima, como o consumo e o preço da obra |
| triangular | mínimo, moda e máximo | quando se sabe o intervalo e o valor mais provável, mas não a forma |
| uniforme | mínimo e máximo | quando só se sabe o intervalo |

Na lognormal, a média e o desvio informados são os da própria variável, e não os do seu
logaritmo: o programa calcula os parâmetros da lognormal que devolvem exatamente a média e
o desvio pedidos. Qualquer distribuição pode ser **truncada** por um limite inferior e um
superior; o valor sorteado fora deles é sorteado de novo. O número de pessoas e o período
de análise são arredondados para inteiro e nunca ficam abaixo de 1; a fração não potável
e o coeficiente de escoamento ficam entre 0 e 100% e entre 0 e 1; fatores, preços, áreas
e consumos nunca ficam negativos.

Cada cartão da tela mostra a curva da distribuição escolhida, desenhada com 4.000
sorteios, e os seus percentis 5 e 95. É a forma mais rápida de conferir se a largura
declarada é plausível: um P95 de 400 L/hab.dia para uma residência indica um desvio
exagerado.

## O nível, e não o ruído do dia

As variáveis são sorteadas **uma vez por realização**: em cada realização, a casa tem um
per capita, uma ocupação e uma fração, válidos por toda a série de chuva. Isso representa
a incerteza sobre **quanto** a edificação consome, que é a que importa. A variação de um
dia para o outro em torno desse nível, opcional (campo «Variação diária»), quase não move
o resultado: sorteada de forma independente a cada dia, ela se cancela ao longo de trinta
anos de série (Silva e Ghisi, 2016; seção {{n:19}}, subcomando `stochastic-demand`).
