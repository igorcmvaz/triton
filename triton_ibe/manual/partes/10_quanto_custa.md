# Quanto custa e em quanto tempo se paga

> No fim desta secção, tem o fluxo de caixa a vinte anos e sabe porque a **estrutura tarifária da entidade gestora** decide a viabilidade mais do que qualquer parâmetro do projeto.

> **Os custos deste manual são ilustrativos.** A Edição Ibérica não traz lista de preços. Todos os custos do tutorial são números redondos, em euros, escolhidos para se poder seguir o método; são **ilustrativos, não são preços de mercado**. A tarifa é a exceção: é o tarifário de Lisboa guardado no projeto de exemplo. No seu estudo, introduza na etapa económica os seus orçamentos e a tarifa que paga. O cálculo que se segue é o mesmo, e a lição sobre as estruturas tarifárias também.

---

## A poupança é a diferença entre duas faturas

O erro mais comum na análise económica de sistemas pluviais é multiplicar o volume poupado por uma tarifa média. O resultado quase nunca está certo, e a razão está na estrutura das tarifas, que em muitos concelhos são progressivas por escalões de consumo, como detalha a secção {{n:16}}: ==o metro cúbico que se deixa de consumir é o último da fatura, o mais caro, e não o médio.== A fatura portuguesa soma ainda várias parcelas — água, saneamento e resíduos —, o que acrescenta um segundo efeito.

O Triton evita o problema calculando duas faturas completas — a que o edifício pagaria sem o sistema e a que paga com ele — e tomando a diferença entre as duas.

<!-- inclui: _tabelas/cap10_economico.md -->

O resultado merece atenção. O sistema poupa 3,34 m³ por mês e a fatura baixa 11,32 €, o que dá 3,39 € por metro cúbico poupado. É mais do que a média da fatura sem o sistema, 2,53 € por metro cúbico (46,25 € para 18,26 m³). A diferença vem de a poupança incidir sobre os escalões mais altos e de a fatura de Lisboa somar à água o saneamento e os resíduos, ambos cobrados em função do volume de água: cada metro cúbico que não é tirado da rede também não é descarregado nem contado para os resíduos.

> **O saneamento acompanha a parcela da água, não a fatura total.** Poupar água poupa as duas parcelas, e é por isso que o valor efetivo do metro cúbico poupado fica acima do preço da água.

---

## O tarifário de Lisboa

A fatura de Lisboa soma três tarifários. A água é da EPAL, com IVA a 6% e o adicional da Câmara Municipal de Lisboa. O saneamento e os resíduos urbanos são tarifários da Câmara. Os três estão transcritos em `triton/data/portugal_tarifarios.json` a partir dos documentos de 2026: EPAL, *Preços de venda de água* (https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0), e Câmara Municipal de Lisboa, tarifários do saneamento e dos resíduos urbanos (https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf e https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf; recolhidos em 07/10/2026). Com 10 m³ por mês, a fatura completa é de 25,87 €.

Há dúvidas por resolver no tratamento do IVA do saneamento e dos resíduos, e o adicional da Câmara vem impresso na tabela da EPAL sem indicar se leva IVA (ver `examples/LEIA.md`). O programa trata-os sem IVA. Não verificado nesta versão: o tratamento do IVA nestas parcelas junto da EPAL e da Câmara Municipal de Lisboa.

Nem todas as entidades gestoras adotam a mesma estrutura, e a diferença decide a viabilidade de projetos inteiros. O programa distingue seis regimes.

<!-- tabela: Os seis regimes tarifários e o efeito de cada um sobre a poupança -->
| Regime | O que acontece ao poupar |
| :--- | :--- |
| tarifa de disponibilidade | cada m³ poupado desconta |
| fórmula exponencial | cada m³ poupado desconta, pelo preço-base elevado ao expoente |
| sem mínimo | idem |
| franquia no mínimo | poupar abaixo da franquia **não desconta nada** |
| franquia retroativa | ao passar a franquia, tarifa-se tudo desde zero |
| piso de pagamento | a fatura não desce abaixo do piso |

> **Atenção, e é o ponto que deita abaixo mais estudos.** Quando a entidade gestora cobra um valor fixo que já inclui uma **franquia**, digamos 10 m³, uma casa que consome 12 m³ e poupa 3 desce para 9, entra na franquia, e **a fatura deixa de baixar**. O sistema poupa água e não poupa dinheiro.
>
> Correr esse caso com uma tarifa média produziria um período de recuperação que não existe. A secção {{n:16}} ensina a montar corretamente a estrutura do seu tarifário.

---

## O investimento

6 650 €, assim distribuídos (todos os valores ilustrativos, não são preços de mercado):

<!-- tabela: Composição do investimento inicial do projeto do tutorial (ilustrativo, não é preço de mercado) -->
| Rubrica | Valor (ilustrativo, não é preço de mercado) |
| :--- | ---: |
| cisterna de betão de 5 000 L | 2 600 € |
| reservatório superior de 1 000 L em polietileno | 650 € |
| duas eletrobombas de meio cv, principal e de reserva | 500 € |
| mão de obra e escavação | 1 500 € |
| tubagem | 600 € |
| acessórios | 800 € |
| **total** | **6 650 €** |

Os preços dos reservatórios seguem uma regra ilustrativa simples, uma parte fixa mais uma parte por litro, diferente para cada material: polietileno 100 + 0,55 por litro, betão 600 + 0,40, fibra de vidro 120 + 0,65 e aço inoxidável 300 + 2,00. Uma cisterna de betão de 5 000 L fica, assim, em 600 + 2 000 = 2 600. Não são preços de catálogo; num estudo real, substitua-os por orçamentos.

**A câmara de descarte.** O descarte das primeiras águas não é só a lâmina subtraída à chuva: é um componente físico, com custo. A etapa **3. Qualidade & ETAP** dimensiona-o por predefinição, e no tutorial a lâmina de 2 mm sobre 150 m² exige uma câmara de 300 L. Neste orçamento ilustrativo, o seu custo está dentro da linha dos acessórios. Um estudo que deixe o descarte fora do orçamento, mas o subtraia à chuva, parece mais viável do que o sistema que se constrói. A secção {{n:27}} detalha o dimensionamento.

---

## O CAPEX nesta edição: o programa não calcula preços de Portugal

Noutras edições do Triton, o investimento de um projeto novo vem preenchido por uma cadeia de cálculo que parte de preços de mercado. **Nesta edição essa cadeia não existe.** Os preços de reservatórios, tubagem, eletrobombas, mão de obra e acessórios ficam a zero, por decisão: não se encontrou fonte oficial aberta para eles e nenhum foi inventado. O programa dimensiona o sistema, calcula a poupança na fatura e a energia, mas o investimento é o que o utilizador introduzir.

<!-- inclui: _tabelas/cap10_custos_estado.md -->

A única coisa que o programa insere sozinho, nesta matéria, é o tarifário de água, saneamento e resíduos de Lisboa, transcrito dos documentos de 2026 (secção {{n:16}}). Tudo o que é preço de obra, de equipamento ou de manutenção, e a tarifa de eletricidade, está por definir.

### O que isto significa para si

Sem os seus valores, o investimento é zero e a análise económica mostra apenas a poupança na fatura de água. O valor atual líquido e o período de recuperação, nessas condições, dizem pouco: não são resultados. A linha de tratamento e o descarte são dimensionados, entram no balanço de carbono, mas não custam nada. Só tem uma análise económica quando introduzir orçamentos reais.

A base de custos interna do programa (`costs_database.json`) existe nas três edições, mas nesta só traz a estrutura: sem preços, sem moeda e sem fatores regionais (os valores em reais e os fatores por estado são os da edição do Brasil). Nesta edição não é usado em nenhum cálculo; os custos são os que o utilizador introduz.

### Como introduzir os seus valores

Na etapa **4. Reservatório & Custos**, o botão *1. Investimento Inicial (CAPEX)* tem campos para o reservatório superior, a mão de obra, a tubagem e os acessórios; o botão *2. Eletrobomba e Custo de Energia* tem o preço da eletrobomba e a tarifa de eletricidade; e o botão *3. Outros Custos Operacionais* tem as rotinas de manutenção. Introduza ali os valores dos seus orçamentos, com IVA se o investimento for suportado pelo consumidor final.

Há duas limitações a conhecer. O diálogo do CAPEX **não tem campo para o preço da cisterna** e, ao confirmar, repõe esse preço a zero. Enquanto isso não for corrigido, some o preço da cisterna a uma das linhas do diálogo, por exemplo os acessórios, e registe a escolha no relatório, ou escreva o valor no campo `cost_lower_tank` do bloco `capex_and_opex` do ficheiro do projeto e não confirme o diálogo do CAPEX depois disso. O mesmo acontece com o preço do cloro, que só existe no ficheiro do projeto, no bloco `water_quality_and_etap`; em alternativa, acrescente em *3. Outros Custos Operacionais* uma rotina de custo variável por metro cúbico de água de chuva.

Os valores do tutorial deste capítulo são ilustrativos. Não os copie para um estudo real:

<!-- inclui: _tabelas/cap10_custos_ilustrativos.md -->

### Uma tabela de preços de Portugal: planeada, não implementada

O plano é uma tabela opcional, que o utilizador ligaria de propósito, com cinco itens em euros: reservatório por volume, tubagem, eletrobomba, mão de obra e acessórios. Cada preço levaria o endereço da fonte, a data de acesso e a soma de verificação do documento. A tabela não teria indexação nem faixa percentual inventada, recusaria extrapolar fora da faixa de volumes recolhida e mostraria uma tarja vermelha quando os preços tivessem mais de 18 meses. Espanha ficaria vazia até haver recolha. **Nada disto existe no programa.** O que existe é o plano, em `PLANO_AUTOMACAO_TARIFAS_E_CUSTOS_IBE.md`, e o princípio: nenhum preço entra sem documento aberto.

---

## O resultado

A segunda tabela acima dá os indicadores.

**O projeto não se paga, e esse é o resultado honesto.** Ao fim de vinte anos, com estes custos ilustrativos e o tarifário de Lisboa, o valor atual líquido (VAL) é de −5 802,56 €, a taxa interna de rentabilidade é de −11,11% ao ano, e não há período de recuperação descontado dentro do horizonte. Não ajustámos os custos até aparecer uma recuperação.

A razão não é um defeito do exemplo. A água é barata em Lisboa em relação ao que custam uma cisterna, duas bombas e a mão de obra, e a fração de 28% limita a poupança a pouco mais de três metros cúbicos por mês, 135,88 € por ano. Um tarifário que premeie mais o metro cúbico, uma fração atendível maior ou uma instalação mais barata mudam a conta, e a secção {{n:20}} varia cada um deles por sua vez. Mostra também que nenhuma das premissas testadas, isoladamente, produz recuperação neste caso. Só o tutorial leva custos, pelo que a secção {{n:14}} compara as três cidades pelo potencial de poupança, e não pela recuperação.

**O custo de exploração é pequeno:** 1,79 € por ano, dos quais 1,05 € são a energia da elevação, os 5,3 kWh por ano da secção {{n:8}} a 0,20 € por quilowatt-hora (valor ilustrativo, não é preço de mercado). A energia vem da mesma função que alimenta a avaliação ambiental, conforme o arranjo indicado na etapa **4. Reservatório & Custos**: elevação, pressurização direta ou gravidade. Este valor não inclui as três rotinas de manutenção ilustrativas, que somam 90,00 € por ano e entram no fluxo de caixa à parte; a secção seguinte mostra o peso delas.

---

O resultado de um volume isolado diz pouco sem os vizinhos. O separador económico repete a conta para todos os volumes da varredura e traça a curva, e é nela que se vê se o ótimo técnico e o ótimo económico caem no mesmo sítio ({{fig:fig49_programa_vpl}}).

![O valor atual líquido contra o volume do reservatório](../figuras/fig49_programa_vpl.png)

*Figura 99 — O gráfico do separador económico: o valor atual líquido de cada volume da varredura, com o máximo económico e o ótimo técnico marcados. Quando os dois coincidem, o programa assinala-os com um único símbolo. Todos os custos são ilustrativos, não são preços de mercado. Figura gerada pelo próprio programa.*

---

## O que entra no custo de exploração (OPEX)

Também aqui o programa não pré-preenche preços. O custo de exploração de um projeto novo soma a energia da eletrobomba, o cloro, a linha de tratamento e as rotinas de manutenção, e **todos esses preços partem de zero**: a tarifa de eletricidade, o preço do cloro e o custo de cada rotina. As três rotinas de manutenção existem como roteiro, com periodicidade de 12 meses, e o utilizador dá-lhes o custo.

O que o programa calcula sozinho são as quantidades: a energia anual da eletrobomba, pela cadeia da secção {{n:28}}, e os quilogramas de cloro, pela dose e pela pureza da pastilha. O custo é a quantidade vezes o preço que o utilizador introduzir. Com preço zero, o custo é zero, e não um valor omitido.

**As rotinas pesam mais que o resto.** O campo de custo anual que o resumo da análise mostra soma só a energia, o cloro e a linha de tratamento. As rotinas de manutenção entram no fluxo de caixa à parte, no fim de cada período, corrigidas pela inflação. No tutorial, com valores ilustrativos, elas movem o resultado:

<!-- inclui: _tabelas/cap10_custos_peso.md -->

**Energia.** Hoje a tarifa de eletricidade é um campo vazio. O exemplo do Funchal traz 0,1673 €/kWh, a Tarifa Base da Empresa de Eletricidade da Madeira, sem IVA, recolhida num comparador de preços (atualizado em 20/02/2025) e por isso de **fonte secundária, a amarelo**: não foi confirmada na EEM nem na ERSE; Lisboa e Porto ficam a zero. Para um estudo, use a sua fatura.

Recolheram-se séries públicas que servirão de ponto de partida, mas **ainda não estão ligadas ao programa**: nenhum valor da tabela seguinte é inserido sozinho. O preço do Eurostat é a média de um domicílio inteiro, na banda de 2 500 a 4 999 kWh por ano, e não o preço marginal de uma eletrobomba; a fatura do utilizador prevalece sempre.

<!-- inclui: _tabelas/cap10_custos_series_publicas.md -->

O plano é pré-preencher a tarifa com o valor do Eurostat do país, rotulado como média de um domicílio inteiro e editável, a inflação com o IPCH e a taxa de atualização com uma referência do BCE. **Não está implementado.** O cloro e as manutenções continuarão sem custo até haver fonte aberta para eles, e o índice de custos de construção, que serviria para atualizar preços já recolhidos, ainda nem foi localizado na fonte oficial.

**O que não entra.** O fluxo de caixa não traz reposição de equipamentos ao longo dos 20 anos, valor residual, análises laboratoriais da água nem seguro. Se a eletrobomba ou o filtro forem substituídos no período, acrescente a substituição como uma rotina em *3. Outros Custos Operacionais*.

**Como alterar ou desligar.** As rotinas editam-se, excluem-se ou acrescentam-se no botão *3. Outros Custos Operacionais*. A dose de cloro e o descarte físico escolhem-se na etapa **3. Qualidade & ETAP**. A tarifa e os impostos da eletricidade ficam em *2. Eletrobomba e Custo de Energia*.

---
## O que a projeção assume

Vinte anos são muito tempo, e a projeção depende de premissas que convém declarar:

<!-- tabela: Premissas da projeção económica e o peso de cada uma no resultado -->
| Premissa | Valor adotado | Onde pesa |
| :--- | ---: | :--- |
| taxa de atualização | 0,4% ao mês | desconta o fluxo; quanto maior, pior o VAL |
| inflação dos custos | 0,2% ao mês | incide só sobre o custo de exploração |
| atualização da tarifa da água | 3% ao ano | incide sobre a poupança |
| atualização da tarifa do saneamento | 3% ao ano | idem, e é indexada à parte |
| intervalo de atualização | 12 meses | em degraus, não de forma contínua |
| período de análise | 20 anos | a vida útil adotada; declare-a e justifique-a |

Todos estes valores são escolhas ilustrativas do tutorial, não dados de um país.

> **As atualizações da água e do saneamento são separadas**, e não um índice único sobre a fatura agregada. As duas parcelas são muitas vezes atualizadas por decisões diferentes das entidades que as cobram, e tratá-las em conjunto indexa parte da conta pelo índice errado.

A atualização da tarifa é a premissa mais frágil da lista. Três por cento ao ano durante vinte anos multiplicam a tarifa por 1,81. Se a tarifa real subir mais do que isso, o projeto rende mais; se subir menos, rende menos. Um estudo sério declara o valor adotado e mostra a sensibilidade — a secção {{n:20}} ensina como.

---

## O que temos até aqui

<!-- tabela: Estado do projeto do tutorial depois da análise económica (ilustrativo, não é preço de mercado) -->
| Projeto até aqui (ilustrativo, não é preço de mercado) | |
| :--- | ---: |
| volume | 5 000 L, betão |
| arranjo | elevação para reservatório superior de 1 000 L |
| investimento | 6 650 € |
| poupança anual | 135,88 € |
| VAL a 20 anos | −5 802,56 € |
| período de recuperação | sem recuperação em 20 anos |

O dinheiro diz não.

Falta ouvir o carbono. E ele não vai simplesmente concordar.
