# Pendências, melhorias e evolução — Netuno 5.0.0

Levantamento de **toda a estrutura** do projeto: 47.212 linhas em `netuno/`,
12.682 em `tests/`, 687 testes verdes. O que segue é o que **não** está resolvido,
ordenado por consequência sobre o resultado de um estudo, e não por esforço.

Cada item traz o que se sabe, o que falta e por que importa. Onde a decisão é
sua, está dito.

---

## Sumário

| # | Pendência | Consequência | Quem decide |
| :-- | :--- | :--- | :--- |
| 1 | Quatro municípios sem tarifa de excedente | payback nulo por defeito de cadastro | dado externo |
| 2 | Cinco municípios da BRK Tocantins com tarifa decrescente | conta subestimada no primeiro bloco | dado externo |
| 3 | Tipologia não residencial faturada com tarifa residencial | economia subestimada pela metade em escola e hospital | você |
| 4 | Esgoto por faixas próprias (14 municípios) | percentual único não representa a estrutura | eu |
| 5 | Emissão de fabricação da motobomba extrapolada | único fator sem fonte primária na ACV | dado externo |
| 6 | Reajuste tarifário como percentual único | projeção de 20 anos frágil | você |
| 7 | Sem tarifa social nem bandeiras de água | classe de baixa renda mal representada | você |
| 8 | Wash-off com constantes não calibradas | qualidade da água é premissa, não medida | você |
| 9 | `tariff_updater` com cobertura mínima | raspagem quebra em silêncio | eu |
| 10 | Percentil do P95 sobre a série toda | diverge do ETCCDI | você |
| 11 | Constantes de domínio repetidas | divergência futura | eu |
| 12 | Módulos de 2.000+ linhas | manutenção | eu |
| 13 | Seis campos gravados e nunca lidos | demanda antiga possivelmente multiplicada pelos moradores | você |
| 14 | Tempo de partida de 108 s por acionamento | 19% do consumo da motobomba | você |
| 15 | Lâmina de descarte padrão de 1 mm | a tela sugere 2 mm, e a norma também | você |
| 16 | `--descarte-como-limiar` citada no protocolo e não implementada | protocolo de verificação instrui usar bandeira inexistente | você |
| ~~17~~ | ~~Placa de eixo ou de tomada~~ | resolvido pela NBR 17094-2 | — |

---

## 1. Quatro municípios sem tarifa de excedente

**Situação.** Sete Lagoas (MG), Bebedouro, Pirassununga e São José do Rio Pardo
(SP) têm apenas o bloco mínimo cadastrado: até 6 ou 10 m³ o valor é conhecido, e
acima disso não há tarifa nenhuma na base.

**Efeito.** A conta não cresce com o consumo. Economizar água não a reduz, e o
aproveitamento pluvial aparece **sem retorno nenhum** — não porque seja inviável,
mas porque falta dado.

**O que foi feito.** Os quatro estão marcados com `estrutura_incompleta`,
rebaixados para confiança D, e a tela de tarifas avisa ao selecioná-los. Um teste
impede que um quinto apareça sem ser notado.

**O que falta.** A tarifa de excedente, das resoluções dos respectivos SAAEs.
Não a reconstruí porque qualquer número seria invenção.

---

## 2. Cinco municípios da BRK Tocantins com tarifa decrescente

**Situação.** Araguaína, Gurupi, Palmas, Paraíso do Tocantins e Porto Nacional
têm a primeira faixa a R$ 8,76/m³ e a segunda a R$ 3,05/m³.

**Efeito.** Tarifa decrescente não é usual e tem a assinatura de um mínimo mensal
diluído em tarifa unitária — o mesmo defeito corrigido em seis outros municípios.
Se for isso, R$ 8,76 × 5 m³ = R$ 43,80 seria o mínimo mensal, e consumir 2 m³
custaria R$ 43,80 e não R$ 17,52.

**Por que não corrigi.** Nos seis casos corrigidos a prova estava no próprio
registro: `tarifa_fixa_mensal` batia exatamente com tarifa × volume. Aqui o
registro não declara mínimo algum, então falta a prova. Corrigir por semelhança
seria adivinhar.

**O que falta.** A estrutura publicada pela BRK Tocantins. Marcados com
`estrutura_suspeita` e confiança C.

---

## 3. Tipologia não residencial faturada com tarifa residencial

**Não era «comercial fora do alcance». Era pior: o programa oferecia as
tipologias não residenciais e as faturava com a tarifa residencial, calado.**

**O que existe.** A aba de edificação tem oito tipologias, e cada uma ajusta
consumo per capita e fração não potável: Residencial Unifamiliar em três padrões,
Edifício Multifamiliar, Comercial/Escritórios, Escola/Creche, Hotel/Pousada e
Hospital/Clínica. A demanda que elas definem sempre atravessou o programa
corretamente.

**O que não existe.** As 652 estruturas tarifárias são todas da categoria
«Residencial normal». Confirmado nos três arquivos da coleta: o catálogo
auditado em XLSX, o CSV detalhado de 3.604 linhas e o banco em JSON. As 3.604
linhas do CSV são **faixas de consumo**, não categorias.

**A desconexão.** `template_id` era gravado num dicionário local da aba de
edificação e **nunca alcançava `NetunoConfig`**. Nenhum outro módulo sabia que
tipo de edificação estava sendo estudada, de modo que o econômico não tinha nem
como perceber que cobrava tarifa residencial de um hospital.

**O tamanho do erro.** Tabela Tarifária CASAN 04/2026, primeira faixa:

| Categoria | R$/m³ | TFDI R$/mês |
| :--- | ---: | ---: |
| Residencial | 3,08 | 46,34 |
| Residencial Social | 0,58 | 8,63 |
| Micro e Pequeno Comércio | 4,80 | 46,34 |
| Comercial, Industrial, Pública | 6,81 | 46,34 |
| Pública Especial | 2,04 | 13,89 |

Como a economia de água é avaliada pela tarifa, subestimá-la subestima a economia
na mesma proporção. Um estudo de escola ou hospital mostra **menos da metade** do
retorno na primeira faixa.

**O que foi feito.** A tipologia passou a chegar à configuração, e
`netuno/core/tariff_category.py` mapeia cada uma à categoria que a concessionária
usaria. Quando as duas não combinam, o aviso aparece em dois lugares: no diálogo
de tarifas, onde a escolha é feita, e acima dos indicadores do painel econômico,
onde o resultado contaminado é lido. O aviso diz o sentido do erro — os valores
estão subestimados — e o que fazer: lançar a estrutura da categoria correta no
modo Personalizado.

**O que falta.** As estruturas das demais categorias, para os municípios que
interessarem. Não são difíceis de coletar: aparecem na mesma tabela das
concessionárias, lado a lado com a residencial, como a da CASAN acima mostra. O
trabalho é de coleta, e a estrutura de dados suportaria uma chave `categorias`
por município com um seletor na tela.

**Decisão sua.** Se o alvo do programa é residencial, o aviso resolve: declara a
limitação onde ela importa. Se escola, hospital e comércio estão no horizonte —
e é onde o aproveitamento pluvial costuma render mais, pela escala — a coleta das
outras categorias é a tarefa de dado mais valiosa do projeto.

---

## 4. Esgoto: percentual único onde a estrutura tem faixas

**Corrigido em parte, e o resto está identificado.**

**O que se achou.** Mesmo padrão da tipologia: dado coletado que o programa não
usava. A coleta detalhada tem tarifa de esgoto **por m³** para 543 municípios, e
o banco de execução guarda só um percentual da conta de água.

Em 89 deles o percentual não reproduzia a tarifa coletada — todos com 80,0%, o
valor de recurso aplicado por cima do dado:

| Município | Guardado | Coletado |
| :--- | ---: | ---: |
| Goiânia e mais 62 da SANEAGO | 80% | 100% |
| Blumenau | 80% | 112% |
| Belo Horizonte (COPASA/ARSAE) | 80% | 74% |
| Caxias do Sul | 80% | 38% |

**Atenção ao denominador**, que é onde esta área produz erro: `esgoto_pct` é
percentual da tarifa de ÁGUA, não da fatura. A CASAN cobra 100% — o esgoto
iguala a água, e por isso responde por metade da fatura total. Como a parcela
de esgoto acompanha a de água metro cúbico a metro cúbico, um erro no
percentual se propaga inteiro para a economia atribuída ao sistema pluvial.

**O que foi feito.** 75 corrigidos, com a origem registrada em cada município.

**O que falta.** Catorze municípios têm percentual que **varia entre faixas** —
Caxias do Sul de 21,6% a 69,9%, os dez da CAGEPA na Paraíba de 79,9% a 100%.
Nenhum número único os representa. Ficam marcados, com ressalva na tela, e pedem
o que o motor ainda não tem: **faixas próprias de esgoto**, um `sewage_mode = 2`.

O dado para isso **já existe** na coleta, para 543 municípios. É a melhoria de
tarifa com melhor relação entre esforço e efeito que resta.

---

## 5. Emissão de fabricação da motobomba

**Situação.** É o **único** fator da avaliação de ciclo de vida que continua sem
fonte primária. Quatro dos seis valores são escalonamento aritmético do valor de
0,5 CV.

**O que foi feito.** A interface passou a marcá-los como VALOR EXTRAPOLADO na
justificativa do campo, de modo que o usuário vê o estatuto do número.

**O que falta.** Uma declaração ambiental de produto de fabricante de motobomba,
ou um inventário publicado por potência. Procurei e não encontrei na
granularidade necessária.

**Consequência prática.** É pequena: a bomba responde por parcela menor do
carbono incorporado que os reservatórios e a tubulação. Mas é a única lacuna
declarada do módulo, e num artigo ela será perguntada.

---

## 6. Reajuste tarifário como percentual único

**Situação.** A projeção de 20 anos usa um percentual anual fixo para água,
esgoto e energia, informado pelo usuário.

**Efeito.** O valor presente líquido a 20 anos é muito sensível a esse número, e
ele é o parâmetro menos fundamentado do módulo econômico. Reajustes reais variam
com IPCA, com revisões tarifárias quadrienais e com decisões das agências.

**Caminho.** Duas melhorias independentes: (a) alimentar o padrão com a série
histórica de reajustes da própria concessionária, que as agências publicam; (b)
oferecer análise de sensibilidade sobre esse parâmetro, mostrando a faixa de VPL
em vez de um número.

**A segunda é a mais valiosa** e não depende de coleta.

---

## 7. Sem tarifa social nem estrutura de bandeiras

**Situação.** A base traz a categoria Residencial comum. A **Residencial Social**
existe e é bem diferente — na CASAN, TFDI de R$ 8,63 contra R$ 46,34, e
R$ 0,58/m³ contra R$ 3,08 na primeira faixa.

**Efeito.** Habitação de interesse social é justamente onde o aproveitamento
pluvial tem apelo de política pública, e é onde o programa erra mais: com tarifa
social, a economia monetária é uma fração da calculada, e o payback estoura.

**Observação.** O valor da tarifa social já aparece na tabela da CASAN que
conferi. A coleta é viável para as concessionárias maiores.

---

## 8. Wash-off com constantes não calibradas

**Situação.** O modelo de lavagem do telhado usa constantes k de 1,6, 1,3 e
1,1 mm⁻¹. A documentação afirmava que foram «calibradas a partir de dados
experimentais» sem mostrar o ajuste.

**O que falta.** Ou mostrar a calibração, ou declarar que são premissa. A segunda
é honesta e barata; a primeira exige dados que talvez não existam.

**Efeito.** A eficiência de descarte alimenta a classe de qualidade alvo, que
agora move investimento e emissão pela ligação da linha de tratamento. Deixou de
ser um número decorativo.

---

## 9. `tariff_updater` com cobertura mínima

**Situação.** O subpacote de atualização automática tem 2.197 linhas em quatro
módulos. Até esta rodada não tinha teste nenhum.

**O que foi feito.** Uma porta de validação estrutural antes de gravar, com os
primeiros sete testes. A porta conserva o registro anterior do município cuja
estrutura nova tem erro e o manda para revisão manual.

**O que falta.** Teste dos raspadores em si, com páginas gravadas como fixture.
Sem isso, uma concessionária que mude o layout do site produz falha silenciosa —
a porta impede que o dado errado entre, mas não avisa que o dado parou de vir.

---

## 10. Percentil do P95 sobre a série inteira

**Situação.** O índice R95p calcula o percentil 95 sobre **toda a série
carregada**. O ETCCDI define período-base fixo de 1961 a 1990.

**Efeito.** Os valores não são diretamente comparáveis com a literatura de
extremos que usa a definição padrão. Com séries de projeção climática, a
diferença cresce.

**Caminho.** Ou implementar o período-base configurável, ou declarar a escolha
na documentação do índice. A segunda já está feita em parte.

**Nota relacionada.** O conjunto é chamado «ETCCDI + Sazonalidade» porque inclui
o índice de Walsh & Lawler, que não é ETCCDI, e omite o R10mm, que é. Está
declarado, mas o R10mm continua ausente e seria barato acrescentar.

---

## 11. Constantes de domínio repetidas

**Situação.** A varredura encontra `365.25` em 14 módulos e `0.85` em 10.
`hydrology_defaults.py` existe e define o coeficiente de escoamento padrão, mas
nem todos os módulos o consomem.

**Efeito.** Nenhum hoje. O risco é de amanhã: alterar um e não os outros produz
divergência entre telas, que foi exatamente como o cloro chegou a ter cinco
convenções nesta versão.

**Caminho.** Um módulo de constantes de domínio, com dias do ano, coeficiente de
escoamento e vida útil, e substituição gradual.

---

## 12. Módulos de 2.000 linhas ou mais

| Módulo | Linhas |
| :--- | ---: |
| `core/report_generator.py` | 2.404 |
| `ui/dialogs/dialog_economic.py` | 2.326 |
| `ui/translation.py` | 2.101 |
| `ui/tab_documentation.py` | 2.056 |
| `cli.py` | 2.021 |

**Efeito.** Nenhum sobre resultado. Sobre manutenção, sim: `dialog_economic.py`
concentra sete diálogos independentes, e `report_generator.py` três geradores de
relatório com HTML literal.

**Caminho.** Separar por diálogo e por relatório, sem mudar comportamento, com a
suíte atual como rede.

---

## 13. Seis campos gravados no arquivo e nunca lidos

O quadro de ligações desta rodada varreu os 78 arquivos do pacote atrás de cada
nome de campo de `NetunoConfig`. Seis aparecem **apenas** em `parser.py`: são
lidos do arquivo, escritos de volta, e nenhum cálculo os consulta.

| Campo | O que deveria significar | Consequência de ignorá-lo |
| :--- | :--- | :--- |
| `demand_type` | per capita ou total, no formato do Netuno 4 | a demanda é sempre `demand_value × residents_count` |
| `residents_type` | fixo ou variável, idem | nenhuma, o número mensal já tem campo próprio |
| `install_month` | mês em que o sistema entra em operação | o fluxo de caixa começa sempre no mês 1 |
| `climate_source_mode` | base nacional ou arquivo do usuário | nenhuma, a escolha se deduz do caminho do arquivo |
| `irrigation_garden_area_m2` | área de jardim, para o assistente | o assistente de irrigação nunca foi ligado |
| `irrigation_rate_l_m2_day` | taxa de rega, idem | idem |

**Dois pedem decisão sua.**

`install_month` é o mais direto: o mês de instalação existe no formato e o fluxo
de caixa o ignora. Implementar significa deslocar o início do fluxo, o que muda
o valor presente líquido de todo projeto que declare um mês diferente de janeiro.
É uma correção pequena no código e visível no resultado — por isso não a fiz sem
perguntar.

`demand_type` é o que me preocupa. O rótulo da linha antiga é
`Demanda de água total;<tipo>;1;<valor>;`, e a demanda hoje é sempre tratada como
per capita. Se o código `1` significar demanda **total** no Netuno 4, todo projeto
antigo importado com esse código tem a demanda multiplicada pelo número de
moradores — quatro vezes maior, numa residência típica. **Preciso de um arquivo
`.netuno` do Netuno 4 com demanda total declarada** para confirmar antes de mexer.
Não corrigi no escuro porque, se eu estiver errado sobre o significado do código,
a correção quebra a leitura dos arquivos que hoje funcionam.

Os outros quatro não pedem decisão: `residents_type` e `climate_source_mode` são
redundantes, e os dois de irrigação pertencem a um assistente de dimensionamento
que nunca foi ligado à tela. Ficam gravados para não quebrar arquivos existentes.

---
## 14. Tempo de partida da motobomba: 108 s por acionamento

`pump_startup_time_h` vale 0,03 h, ou **108 segundos por acionamento**, descritos
no fonte como «tempo perdido em cada partida, com a bomba consumindo sem entregar
vazão útil».

Medido no caso padrão — meio CV, 12 m.c.a., rendimento 0,50, 98 acionamentos por
ano, 87,5 m³ recalcados:

| Parcela | kWh/ano |
| :--- | ---: |
| recalque | 5,72 |
| partidas, com 108 s | 1,09 |
| partidas, com 3 s | 0,03 |

As partidas pesam **19% do consumo anual** da motobomba. Com um transitório de 3 s,
que é a ordem de grandeza do arranque de um conjunto pequeno, pesariam 0,5%.

Cento e oito segundos por partida é o tempo de **escorva** de uma bomba
autoaspirante cuja linha de sucção drenou. Numa instalação com válvula de pé em
ordem, a linha permanece escorvada e as partidas seguintes são imediatas. O padrão
atual trata o pior caso como norma.

**Não mexi**, porque é premissa de projeto e muda o resultado de todo estudo com
reservatório superior. A pergunta é sua: o valor de referência deve ser o tempo de
escorva, ou o transitório de partida?

---

## 15. Lâmina de descarte: o padrão é 1 mm, a tela sugere 2 mm

`NetunoConfig.discard` vale **1,0 mm**. O campo da aba Projeto abre vazio com a
dica «Ex: 2,0», o gerador de relatório assume 2,0 quando o dado falta, e a NBR
15527 recomenda 2 mm na ausência de dado local.

Quem não tocar no campo fica com 1 mm enquanto a própria tela sugere 2. Na série
sintética de dez anos usada na verificação, passar de 1 para 2 mm reduz a chuva
aproveitável de 1.303 para 1.091 mm/ano — 16% — embora o potencial de economia
caia apenas 0,12 ponto percentual, porque aquele caso é limitado pela demanda e
não pela oferta. Num caso limitado pela oferta, a diferença aparece inteira.

**Não mexi**: alterar o padrão muda o resultado de todo estudo novo.

---

## 16. Duas semânticas de descarte, e o programa documentava as duas

O código subtrai a lâmina da chuva bruta:

```
p_eff = p − d_f   se p > d_f,   senão   0
```

A aba de Documentação, no capítulo das equações, afirmava o contrário: que `d_f`
seria um **limiar do evento**, abaixo do qual o dia se perde inteiro e acima do
qual entra a «precipitação diária integral» — e que essa seria a leitura do
**Manual do Netuno 4**.

As duas leituras separam **35% da chuva aproveitável** com `d_f` = 2 mm: 1.091
contra 1.472 mm/ano na série de verificação. Não é diferença de redação.

Corrigi o texto da aba para descrever o que o programa faz, porque um programa não
pode documentar duas coisas incompatíveis.

**A divergência contra o Netuno 4 já estava resolvida, e eu não tinha visto.** O
Manual do Netuno 4 de junho de 2014 está no repositório, em
`additional_material/documentation/`, e a seção 3.1 dele diz: «caso a precipitação
em um dado dia esteja abaixo desse valor, o Netuno considerará que não houve
precipitação». É a regra de limiar. O `metodologia.md` §1 registra a diferença como
**deliberada**, com a justificativa física — a água desviada para o dispositivo de
descarte não chega à cisterna — e com o efeito quantificado sobre 4.050 casos de
referência: o Netuno 5 estima de 2,3 a 2,7 pontos percentuais menos economia, e
cerca de 46% dessa diferença vem daqui.

O parágrafo que eu corrigi na aba de Documentação descrevia corretamente o
**Netuno 4**, e errado o Netuno 5. A correção continua válida: aquela página fala
do que este programa faz.

**O que sobra de verdade é menor, e é uma ponta solta.** O `protocolo_netuno4.md`
§2 manda rodar toda comparação duas vezes, «com e sem `--descarte-como-limiar`»,
para isolar o balanço hídrico da diferença deliberada. **Essa opção não existe na
linha de comando.** Não há nenhuma ocorrência dela em `netuno/cli.py`. O protocolo
de verificação instrui a usar uma bandeira que ninguém implementou.

Duas saídas, e a escolha é sua: implementar a bandeira, que é pequena e transforma
a série de entrada sem tocar no motor; ou retirar a instrução do protocolo e
adotar a alternativa que o próprio documento oferece, rodar com descarte zero, caso
em que as duas regras coincidem.

---
## 17. A potência de placa é de eixo ou de tomada?

O módulo de hidráulica declara que o rendimento é «do conjunto motobomba, já
incluindo motor e parte hidráulica». Isso significa tratar a potência de placa
como **potência elétrica de entrada**, e o rendimento como fio-a-água.

A conferência contra uma bomba real diz outra coisa. Tomando a curva de catálogo
da Dancor CP-4R de 1/2 CV, que dá 8,4 m³/h a 6 m.c.a. e 0,4 m³/h a 22 m.c.a., e
ajustando a parábola usual `H = H₀ − kQ²`:

| Grandeza | Valor |
| :--- | ---: |
| vazão a 12 m.c.a. | 6,65 m³/h |
| potência hidráulica no ponto | 217 W |
| placa | 370 W |
| razão entre as duas | 0,59 |

Essa razão de 0,59 é o **rendimento da bomba**, não do conjunto. O programa adota
0,50 para essa faixa de potência e prevê 5,66 m³/h, quinze por cento abaixo do
catálogo: é um rendimento de bomba, conservador, e não um rendimento fio-a-água.

A norma de máquinas elétricas girantes define a potência nominal do motor como a
**potência mecânica no eixo**. Se a placa é de eixo, então `ρgH/η` devolve energia
de eixo por metro cúbico, e falta ainda dividir pelo rendimento do motor para
chegar à energia que o medidor registra:

| Leitura | kWh/m³ a 12 m.c.a. |
| :--- | ---: |
| placa de tomada, como está hoje | 0,0654 |
| placa de eixo, motor a 70% | 0,0934 |
| placa de eixo, motor a 65% | 0,1006 |
| placa de eixo, motor a 60% | 0,1090 |

A diferença é de 43% a 67% no consumo da motobomba, que atravessa para o custo de
energia no fluxo de caixa e para a emissão operacional na avaliação de ciclo de
vida.

**RESOLVIDO.** A placa é de eixo, e a fonte é normativa: a ABNT NBR 17094-2:2016
manda marcar o rendimento na placa de identificação como grandeza separada da
potência, o que só faz sentido se a potência for a mecânica no eixo.

A Tabela 13 da mesma norma dá o rendimento nominal mínimo a plena carga da linha
IR1, e a Tabela 14 o da linha IR2. Motobombas residenciais são de 2 polos:

| Potência | 2 polos, IR1 | 2 polos, IR2 |
| :--- | ---: | ---: |
| 1/4 CV, 0,18 kW | 50,0% | 64,0% |
| 1/3 CV, 0,25 kW | 55,5% | 68,0% |
| 1/2 CV, 0,37 kW | 60,5% | 72,0% |
| 3/4 CV, 0,55 kW | 64,0% | 74,0% |
| 1 CV, 0,75 kW | 69,3% | 75,5% |
| 1,5 CV, 1,10 kW | 71,5% | 82,5% |
| 2 CV, 1,50 kW | 72,4% | 84,0% |

Adotou-se a linha IR1 como referência, por ser o piso normativo e o que se
encontra em motobomba de prateleira. Quem tiver motor IR2 informa o valor da
placa no campo novo da tela de energia.

A cadeia ficou assim, nos dois motores de cálculo:

```
recalque:  e = ρ·g·H / (η_bomba · η_motor)     kWh por m³ elevado
partidas:  E = placa · t / η_motor             sem η_bomba, porque não há vazão
```

Efeito medido no caso de referência, meio CV a 12 m.c.a.: o consumo específico
passa de 0,0654 para 0,1080 kWh/m³, e o consumo anual da motobomba de 6,81 para
11,26 kWh. O valor de recurso usado quando não há simulação passa de 0,0874 para
0,1446 kWh/m³.

## 18. Telas que a janela nunca abre

`tab_matrix_sim.py`, `tab_scenarios_modern.py` e `dialog_scenario_simulation.py`
foram removidos em 17/09/2026: não eram instanciados pela janela principal, e a
importação de cenários em lote continua disponível pelo menu Cenários &
Ferramentas. Em 18/09/2026 saíram as três últimas: `tab_single_sim.py` (870 linhas),
`tab_economic.py` (150) e `tab_reports.py` (1.069), substituídas na janela por
`tab_tanks_simulation.py`, `tab_economic_integrated.py` e `tab_reports_pdf.py`. Nenhum
módulo as importava; a pendência está encerrada.

## 19. A linha de comando não acompanha o executável

O `Netuno.spec` empacota só `main.py`, a janela. A linha de comando existe no
código-fonte, é usada nos estudos de larga escala do grupo e **não chega ao
usuário que instala**.

O manual foi escrito para quem instala, e por isso deixou de documentá-la: o
apêndice F passou a descrever arquivos, pastas e formatos, e os guias 19 e 20
foram reescritos em torno do que a janela oferece. Onde a capacidade só existe
por automação — matriz de milhares de casos, Monte Carlo — o texto diz isso numa
caixa de aprofundamento, sem ensinar comando nenhum.

Se a decisão for distribuir a linha de comando, ela precisa de um segundo
executável no `Netuno.spec`, de uma entrada no instalador e de um capítulo
próprio no manual. Não é difícil; é decisão, não implementação.

---

## 20. O instalador não leva a base climática

A base de 6,5 GB é distribuída à parte, o que é acertado, mas hoje não há
instalador próprio dela nem verificação de integridade no programa: a tela
simplesmente oferece menos opções quando ela falta. O capítulo 2 e o apêndice E
do manual descrevem o comportamento como ele é.

Vale decidir se a base ganha instalador próprio — com verificação de soma de
conferência — ou se fica como pasta copiada à mão.

---

## O que esta rodada resolveu

Registrado para não gerar retrabalho.

- **Regimes de tarifa mínima** nomeados, declarados nos 652 municípios e
  validados por teste. O motor ganhou o piso de pagamento, que lhe faltava.
- **21 registros tarifários defeituosos**: 12 corrigidos com a reconstrução
  documentada, 9 sinalizados com confiança rebaixada e aviso na tela.
- **Florianópolis conferida** contra a Tabela Tarifária CASAN 04/2026: a TFDI de
  R$ 46,34 e as quatro faixas batem exatamente. É taxa de disponibilidade e não
  consumo mínimo, de modo que na área da CASAN **cada metro cúbico economizado
  gera desconto desde o primeiro**.
- **Porta de validação** antes do gravador automático de tarifas.
- **Duplicação de códigos de faixa** que eu havia introduzido, unificada.
- **Modulação por calendário gravada.** As sete listas de perfil semanal, mensal
  e diário não iam para o arquivo, e `demand_mode` nunca era escrito a partir da
  tela: um projeto de escola modulado por dia da semana reabria como demanda
  constante, sem aviso. Gravação, leitura, repovoamento das tabelas da tela e
  repasse para a simulação, com teste que falha se a modulação voltar inerte.
- **Projeto de esquema desconhecido recusado.** Um JSON sem as seções do Netuno
  era aceito e devolvia a configuração padrão inteira — o usuário abria um estudo
  de 180 m² e simulava 100 m². Agora a abertura para com mensagem própria. Os
  três estudos de `examples/` estavam nessa situação desde 2025 e foram
  convertidos para o esquema corrente.
- **Nove projetos de exemplo** que reproduzem os resultados impressos no manual,
  cada um com a série de chuva incorporada, verificados por teste que relê o
  arquivo gravado e refaz a simulação.
- **Manual em PDF**, composto do próprio Markdown, com desenhos explicativos do
  sistema e caixas de aprofundamento para o conteúdo avançado.

---

## Como eu ordenaria

1. **Item 3, categoria tarifária.** É a maior lacuna de dado, e decide se o
   programa serve para não residencial.
2. **Item 6b, sensibilidade do reajuste.** Não depende de coleta e melhora a
   honestidade do valor presente líquido de imediato.
3. **Itens 1 e 2**, os nove municípios, quando houver acesso às resoluções.
4. **Item 7, tarifa social**, se o uso em habitação de interesse social estiver
   no horizonte.
5. **Item 9**, fixtures dos raspadores, antes que uma concessionária mude o site.

O **item 13** entra logo depois do 3: `demand_type` decide se os estudos antigos
importados estão certos, e a confirmação custa um arquivo do Netuno 4.

Os itens 11 e 12 são meus e não precisam da sua decisão: entram quando houver
folga, sem alterar comportamento.
