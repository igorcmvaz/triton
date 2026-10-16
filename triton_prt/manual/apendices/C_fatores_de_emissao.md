# Fatores de emissão

Todos os fatores que a avaliação de ciclo de vida usa, com a procedência, a fronteira e o grau
de confiança. A avaliação é de **triagem**, e não um inventário conforme a ISO 14040 (apêndice {{n:G}}).

A Edição Portugal separa os fatores em dois tipos.

- **A indicar pelo utilizador.** O fator da rede elétrica e o fator da água potável entregue ao
  edifício dependem do local e do ano do projeto. A edição não traz valor predefinido para nenhum
  deles: os campos partem de zero, e a avaliação de ciclo de vida só tem sentido depois de os
  introduzir. O utilizador obtém-nos junto de uma fonte do local do projeto, e declara a fonte, o ano
  e a fronteira. Esta edição do manual não fixa nenhuma fonte nacional: uma série oficial portuguesa só
  entrará aqui depois de verificada (ver as pendências).
- **Fatores de triagem do programa.** Os fatores dos materiais dos reservatórios, das tubagens, da
  eletrobomba e dos consumíveis de tratamento são valores de partida, editáveis no ecrã. Cada um vem
  listado abaixo com a referência que o código-fonte regista. Essas referências não foram reverificadas
  para esta edição do manual (pendente, ver abaixo): trate cada valor como hipótese de triagem e
  substitua-o por uma Declaração Ambiental de Produto (EPD) do produto que especificar, sempre que
  existir.

---

## Fatores a indicar pelo utilizador

<!-- tabela: Fatores de emissão que o utilizador indica, e o que declarar em cada um -->
| Fator | Unidade | Padrão | O que declarar |
| :--- | :--- | :--- | :--- |
| rede elétrica | kg CO₂e/kWh | nenhum (zero) | fonte, **ano**, se é CO₂ ou CO₂e, e se cobre só a produção ou também perdas e combustíveis a montante |
| água potável de rede entregue ao edifício | kg CO₂e/m³ | nenhum (zero) | fonte, fronteira, e se o valor é por m³ **entregue** ou por m³ produzido |
| material do reservatório, quando substitui o predefinido | kg CO₂e/kg e kg/m³ | ver abaixo | fonte, versão, fronteira do sistema de produto |

**A fronteira é por metro cúbico entregue ao edifício**, e não por metro cúbico produzido na estação.
Um fator dado à saída da estação tem de ser dividido pela fração do volume produzido que chega ao
edifício (um menos as perdas na distribuição da entidade gestora), ou a emissão evitada fica
subestimada.

**O fator da rede muda todos os anos**, e um estudo sem o ano declarado é irreprodutível. Um fator só
de CO₂ e um fator de CO₂ equivalente são grandezas diferentes: a avaliação de ciclo de vida precisa do
segundo.

---

## Materiais dos reservatórios

<!-- tabela: Fatores de emissão dos materiais dos reservatórios, com massa e fronteira -->
| Material | Massa por m³ útil | Fator | Fronteira |
| :--- | ---: | ---: | :--- |
| polietileno de alta densidade | 22 kg/m³ | 1,612 kg CO₂e/kg | berço ao portão |
| betão armado | 1 200 kg/m³ | 0,140 kg CO₂e/kg | berço ao portão |
| fibra de vidro | 15 kg/m³ | 3,250 kg CO₂e/kg | berço ao portão |
| aço inoxidável AISI 304 | 38 kg/m³ | 3,700 kg CO₂e/kg | berço ao portão |

A massa por metro cúbico útil é o que converte o volume do reservatório em massa de material. É ela, e
não o fator, que faz o betão dominar o inventário: 1 200 kg por metro cúbico contra 22 do polietileno.
As massas são cenários geométricos do programa, e não o peso de um produto.

<!-- tabela: Referência registada no programa para cada fator de material, e a sua situação -->
| Material | Referência registada no programa | Situação |
| :--- | :--- | :--- |
| polietileno | Franklin Associates para o American Chemistry Council (outubro de 2020), *Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin*, Tabela 6: 1 612 kg CO₂e por 1 000 kg de resina (TRACI 2.1, IPCC 2013 GWP-100, âmbito dos Estados Unidos) | registada; reverificação pendente |
| betão | valor de triagem de 0,14 kg CO₂e/kg; Hammond e Jones (2008, doi:10.1680/ener.2008.161.2.87) publicam um valor para o betão, mas o valor exato adotado não está rastreado até ele | triagem, sem fonte rastreada |
| fibra de vidro | Composites UK, *Embodied carbon data for composites*: intervalo típico de 2,5 a 4,0 kg CO₂e/kg; adota-se o ponto médio | registada; reverificação pendente |
| aço inoxidável | worldstainless (World Steel Association), relatório de emissões de CO₂ de 24/09/2024, berço ao portão: 1,95 kg CO₂/kg com 85% de sucata, 2,45 com 75%, 3,70 com 50%, 6,80 com 30%; adota-se o caso de 50% de sucata | registada; reverificação pendente |

> **Consequência prática, demonstrada na secção {{n:11}}:** o material pode decidir o **sinal** do
> resultado ambiental. Com a chuva de Lisboa e os fatores ilustrativos do tutorial, nenhum dos quatro
> materiais paga a dívida de carbono em vinte anos; a secção conta o resultado tal como saiu.

---

## Tubagens e eletrobomba

A tubagem de PVC toma-se a 2,36 kg CO₂e por quilograma de tubo instalado, módulos A1 a A3 de uma
Declaração Ambiental de Produto (EPD Australasia S-P-05503, 25/11/2022, EN 15804+A2), multiplicado pela
massa linear do tubo para o seu diâmetro nominal. As massas lineares são valores de triagem: substitua-as
pela ficha técnica do tubo que especificar.

A eletrobomba toma-se a uma intensidade de 4,77 kg CO₂e por quilograma de bomba, da EPD da Grundfos
EPD-GRU-20250340-CBA1-EN (2025, módulos A1 a A3), aplicada à massa da bomba. Indique a massa da bomba que
especificar; havendo EPD do fabricante, é ela que prevalece.

> **Declare no estudo.** A EPD é de um circulador europeu com eletrónica integrada, e a sua massa de
> referência inclui a embalagem. A intensidade por quilograma é uma aproximação de ordem de grandeza, e
> não o inventário da bomba instalada.

Situação das duas referências: registadas no programa, reverificação pendente.

---

## Consumíveis de tratamento

<!-- tabela: Fatores de emissão dos consumíveis de tratamento -->
| Consumível | Fator |
| :--- | ---: |
| pastilha de hipoclorito de cálcio a 65% | 1,72 kg CO₂e/kg de produto |
| lâmpada ultravioleta | energia da rede |
| gerador de ozono | energia da rede |

A massa é de **produto**, e não de cloro ativo. As pastilhas têm cerca de 65% de cloro ativo.

O fator do hipoclorito é uma aproximação tirada de uma base comercial (ecoinvent 3.8, *cutoff*, hipoclorito
de sódio em solução a 15%, geografia resto do mundo, EF 3.1 *Climate change*: 2,522 kg CO₂e por kg de NaOCl,
convertido para base de cloro ativo e para uma pastilha a 65%). Não há processo de hipoclorito de cálcio, e a
base não é aberta: o fator é um valor de **triagem**. Se dispuser de um fator aberto para o produto que usa,
introduza-o no campo `chlorine_co2_kg_per_kg`.

---

## Fatores com rótulo de triagem

Nem todo o parâmetro tem fonte primária, e os que não a têm são assinalados no relatório: as massas por
metro cúbico útil do polietileno, do betão e do aço inoxidável, que são cenários geométricos, o fator do
betão, o fator do hipoclorito e qualquer fator introduzido sem fonte. Os fatores que o utilizador introduz
sem fonte recebem também o rótulo de triagem. Um inventário que apresenta todos os fatores com o mesmo grau
de confiança esconde onde está a fragilidade.

---

## O que consultar antes de publicar

1. a EPD ou a ficha técnica de cada produto que especificar;
2. o separador Documentação, capítulo de avaliação de ciclo de vida, para as justificações mostradas ao utilizador;
3. o inventário do relatório ambiental, que lista cada item com o fator aplicado.
