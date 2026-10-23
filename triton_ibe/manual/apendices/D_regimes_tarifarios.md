# Regimes tarifários

A Edição Ibérica traz o tarifário doméstico de **3 concelhos**, transcrito
dos documentos das entidades gestoras: Funchal, Lisboa, Porto. Para qualquer
outro concelho, o utilizador introduz o tarifário do projeto, na janela de tarifário (etapa 5),
e o programa calcula a fatura com e sem o sistema. Este apêndice descreve a estrutura que o
programa aceita, os seis regimes que reconhece e os tarifários transcritos.

## Os códigos de escalão

Cada linha da tabela de água é uma quádrupla `(mínimo, máximo, valor, código)`, em m³ por mês
e euros por m³ (ou euros por mês nos códigos fixos).

<!-- tabela: Os códigos da tabela tarifária de água -->
| Código | Significado |
| ---: | :--- |
| 1 ou 0 | escalão progressivo: cobrado só sobre o volume dentro dele |
| −1 | tarifa de disponibilidade: valor fixo por mês que se soma ao consumo medido |
| −2 | franquia retroativa: até à franquia paga-se o valor fixo; depois, todo o volume desde zero é cobrado pelos escalões |
| −3 | piso de pagamento: a fatura não pode ficar abaixo do valor |

O efeito de cada código na fatura está desenhado na secção {{n:29}}, e não se repete aqui.

## A fatura portuguesa

Uma fatura doméstica soma, por mês, a água (tarifa fixa e escalões por m³), o saneamento de
águas residuais, os resíduos urbanos, a taxa de recursos hídricos (TRH, por m³) e o IVA de
cada parcela, **à taxa que o próprio tarifário declara**. Nenhuma taxa de IVA fica no código.
O programa trata cada parcela assim:

<!-- tabela: Como o programa guarda cada parcela da fatura portuguesa -->
| Parcela | Como entra no projeto |
| :--- | :--- |
| água | escalões em `water_tariffs`; o IVA da água em `water_tax_var` |
| saneamento por escalões | modo 3 do saneamento, sobre o volume recolhido (coeficiente de recolha × volume de água); a TRH e o IVA entram no preço de cada escalão |
| saneamento ou resíduos por m³ | modo 2 do saneamento, com um preço único por m³ de água, IVA incluído |
| tarifas fixas das outras parcelas | taxa fixa mensal (`water_tax_fixed`), com IVA |

Os resíduos por escalões (como no Funchal) ainda não têm campo próprio: a parte variável soma-se
à do saneamento, e só a parte fixa fica numa parcela à parte. A atualização tarifária é
introduzida em separado para a água, o saneamento e a energia (apêndice {{n:A}}).

## As quatro formas do saneamento

<!-- tabela: As quatro formas de introduzir o saneamento -->
| Modo | O saneamento é |
| ---: | :--- |
| 0 | um valor fixo |
| 1 | uma percentagem da parcela de água (e não da fatura toda) |
| 2 | um valor por m³ consumido |
| 3 | escalões, aplicados a uma fração do volume de água que o utilizador declara |

## Os seis regimes

O programa classifica uma tabela de água num de seis regimes. O regime diz quanto vale poupar
água, que é o que um estudo de aproveitamento de água de chuva precisa de ver.

<!-- tabela: Os seis regimes tarifários e o que acontece ao poupar -->
| Regime | Estrutura | O que acontece ao poupar |
| :--- | :--- | :--- |
| **Sem mínimo** | Só escalões progressivos. | Cada m³ poupado reduz a fatura. |
| **Tarifa de disponibilidade** | Um valor fixo que **soma** ao consumo medido. | Cada m³ poupado reduz a fatura; a parte fixa mantém-se. É a estrutura dos três tarifários transcritos. |
| **Franquia no mínimo** | O valor fixo já inclui um volume. | Poupar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | Até à franquia paga-se o valor fixo; passando-a, **tudo desde zero** é cobrado pelos escalões. | Ao passar a franquia, todo o volume é faturado desde zero. |
| **Piso de pagamento** | A fatura **não fica** abaixo do piso. | Não soma: limita. A poupança que leve a fatura abaixo do piso não rende nada. |
| **Fórmula exponencial** | Serviço básico mais `PB × Cⁿ`, com o expoente `n` dado pelo consumo do mês. | Cada m³ poupado reduz a fatura, mas não a um preço fixo por m³. |

**Teste rápido.** Simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os
com uma fatura real. Se só um coincidir, o regime está errado. A secção {{n:16}} ensina o
teste que identifica uma estrutura errada.

## Os tarifários transcritos

Os valores abaixo são os impressos nos documentos das entidades gestoras, transcritos em
`triton/data/portugal_tarifarios.json` e recolhidos em 07/10/2026. São exemplos fiéis de
como se introduz um tarifário, e não um catálogo: os tarifários mudam todos os anos, e é
preciso verificar o documento em vigor da sua entidade gestora antes de qualquer conclusão
económica. Os três têm a estrutura da tarifa de disponibilidade com escalões progressivos.

<!-- tabela: Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço -->
| Concelho | Serviço | 0–5 | 5–15 | 15–25 | 25–50 | mais de 50 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Funchal | água | 0,39 | 0,69 | 1,28 | 2,87 | 5,02 |
| Funchal | saneamento | 0,00 | 0,55 | 1,01 | 1,01 | 1,01 |
| Lisboa | água | 0,4634 | 0,8666 | 2,0398 | 2,5961 | 2,5961 |
| Lisboa | saneamento | 0,2198 | 0,5787 | 1,3621 | 1,7165 | 1,7165 |
| Porto | água | 0,4945 | 0,9649 | 1,7657 | 3,0016 | 3,0016 |
| Porto | saneamento | 0,3875 | 0,7606 | 1,4608 | 2,4423 | 2,4423 |

### Funchal: Câmara Municipal do Funchal

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 15 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Câmara Municipal do Funchal, Tabela de Taxas e Outras Receitas Municipais 2026
  Endereço: https://cmfdoc.funchal.pt/media/k2/attachments/Tabela_de_Taxas_Municipais_2026_.pdf (entregue pelo autor); SHA-256 `97084c0265bfcb75c75e7b9e2d95aebab3417973f3cd0964b34696d3eea76f87`; recolhido em 07/10/2026.

<!-- tabela: Estrutura do tarifário do Funchal -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 4,12 € | 4% |
| água, escalão | 0 | 5 | 0,39 €/m³ | 4% |
| água, escalão | 5 | 15 | 0,69 €/m³ | 4% |
| água, escalão | 15 | 25 | 1,28 €/m³ | 4% |
| água, escalão | 25 | 50 | 2,87 €/m³ | 4% |
| água, escalão | 50 | sem limite | 5,02 €/m³ | 4% |
| saneamento, tarifa fixa por mês | — | — | 1,97 € | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 0 | 5 | 0,00 €/m³ | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 5 | 15 | 0,55 €/m³ | 4% |
| saneamento, escalão (sobre 100% do volume de água) | 15 | sem limite | 1,01 €/m³ | 4% |
| Resíduos urbanos (tarifa fixa), fixa por mês | — | — | 2,19 € | 4% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: Contas mensais de conferência do tarifário do Funchal -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 17,0872 € |
| 30 m³/mês | 67,5272 € |

Hipóteses e dúvidas registadas ao transcrever:

- Tarifa de disponibilidade de água: 4,12 €/mês para contador até 15 mm (artigo 57.º).
- Água por escalões: até 5 m³ (0,39 €/m³), 6 a 15 m³ (0,69 €/m³), 16 a 25 m³ (1,28 €/m³), 26 a 50 m³ (2,87 €/m³) e > 50 m³ (5,02 €/m³) (artigo 56.º).
- Saneamento e resíduos urbanos têm escalões com cortes idênticos (0–5 m³ com valor zero, 6–15 m³ e > 15 m³). Como incidem sobre o volume de água consumida com a mesma taxa de IVA (4%), os componentes variáveis foram somados nos escalões de águas residuais: 0 a 5 m³ (0,00 €/m³), 5 a 15 m³ (0,33 + 0,22 = 0,55 €/m³) e > 15 m³ (0,41 + 0,60 = 1,01 €/m³).
- Tarifa fixa de saneamento: 1,97 €/mês (artigo 10.º); tarifa fixa de resíduos urbanos: 2,19 €/mês (artigo 6.º).
- IVA: o documento indica «Valor final sem IVA». Adotou-se 4%, que se tomou como a taxa reduzida do IVA na Região Autónoma da Madeira; a taxa, o diploma que a fixa e a sua aplicação à água, ao saneamento e aos resíduos NÃO foram verificados (sem consulta a fonte oficial) e ficam a confirmar. Com 5%, a conta de 10 m³ passaria de 17,0872 para 17,2515 €.
- Escalões de água, saneamento e resíduos aplicados por faixa (cada m³ paga o preço da sua faixa), como nos demais tarifários; a tabela não explicita se o preço do escalão atingido vale para todo o volume. A confirmar com a Câmara.
- O 1.º escalão (até 5 m³) de saneamento e de resíduos não tem valor impresso: tratado como zero, hipótese não confirmada (pode ser isenção ou omissão da tabela). O valor fixo mensal de cada um é cobrado em qualquer caso.
- A tabela não imprime Taxa de Recursos Hídricos (TRH 0 neste tarifário, a confirmar). O programa ainda não tem campo para resíduos por escalões, por isso a parte variável dos resíduos foi somada à do saneamento: na interface o «saneamento» do Funchal inclui os resíduos variáveis (só a parte fixa dos resíduos, 2,19 €/mês, fica numa parcela própria).

### Lisboa: EPAL (água); Câmara Municipal de Lisboa (saneamento e resíduos urbanos)

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- EPAL, Preços de venda de água, 1.ª edição 2026
  Endereço: https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0; SHA-256 `d0ebc13e306944db42fc96b57544ade72625478e99b5b0dc26d81fc6f0b5f42d`; recolhido em 07/10/2026.
- CML, Tarifário do saneamento 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf (entregue pelo autor); SHA-256 `6c6295d9e5da3d09a7cd5476abe242757edd761b137359d5a4b561d1f080c37a`; recolhido em 07/10/2026.
- CML, Tarifário dos resíduos urbanos 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf (entregue pelo autor); SHA-256 `7fa873127affb4e33306166292c9da937f0d68b39987a97ead767a866e32e54f`; recolhido em 07/10/2026.

<!-- tabela: Estrutura do tarifário de Lisboa -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 5,82 € | 6% |
| água, escalão | 0 | 5 | 0,4634 €/m³ | 6% |
| água, escalão | 5 | 15 | 0,8666 €/m³ | 6% |
| água, escalão | 15 | 25 | 2,0398 €/m³ | 6% |
| água, escalão | 25 | sem limite | 2,5961 €/m³ | 6% |
| saneamento, tarifa fixa por mês | — | — | 2,999 € | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 0 | 5 | 0,2198 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 5 | 15 | 0,5787 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 15 | 25 | 1,3621 €/m³ | 0% |
| saneamento, escalão (sobre 90% do volume de água) | 25 | sem limite | 1,7165 €/m³ | 0% |
| saneamento, taxa de recursos hídricos | — | — | 0,0320 €/m³ recolhido | 0% |
| Adicional C.M. Lisboa, por m³ de água | — | — | 0,1483 €/m³ | 0% |
| Resíduos urbanos, fixa por mês | — | — | 2,2333 € | 0% |
| Resíduos urbanos, por m³ de água | — | — | 0,1710 €/m³ | 0% |
| TGR (taxa de gestão de resíduos), por m³ de água | — | — | 0,0523 €/m³ | 0% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: Contas mensais de conferência do tarifário de Lisboa -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 25,8683 € |
| 30 m³/mês | 94,3767 € |

Hipóteses e dúvidas registadas ao transcrever:

- IVA da água: 6%, declarado na tabela da EPAL (Código do IVA, Lista I, verba 1.7).
- Saneamento e resíduos: prestados pela própria Câmara; os documentos não cobram IVA, e a AT não aplica IVA a esses serviços quando prestados por entidade pública (posição contestada pela Provedora de Justiça, Público, 05/12/2024). Zero até haver fonte em contrário.
- Escalões do saneamento aplicados ao volume recolhido = 90% do volume de água (nota 1 do tarifário); a TRH do saneamento acresce por m³ recolhido (nota 4).
- Adicional C.M. Lisboa: por m³ de água, impresso na tabela da EPAL; a tabela não diz se leva IVA — tratado sem IVA, a confirmar numa fatura.
- Tarifas de disponibilidade por 30 dias tomadas como mensais.

### Porto: Águas e Energia do Porto, EM

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Águas e Energia do Porto, Tarifário Geral 2026
  Endereço: https://www.aguasdoporto.pt/files/uploads/cms/Tarif%C3%A1rio%20Geral%202026.pdf; SHA-256 `7d6b5d0ceeef749d558018b4b1b24e661f3a415a1d55cab09f0de7aae340e0de`; recolhido em 07/10/2026.

<!-- tabela: Estrutura do tarifário do Porto -->
| Parte | De (m³/mês) | Até (m³/mês) | Valor | IVA |
| :--- | ---: | ---: | ---: | ---: |
| água, tarifa fixa por mês | — | — | 3,726 € | 6% |
| água, escalão | 0 | 5 | 0,4945 €/m³ | 6% |
| água, escalão | 5 | 15 | 0,9649 €/m³ | 6% |
| água, escalão | 15 | 25 | 1,7657 €/m³ | 6% |
| água, escalão | 25 | sem limite | 3,0016 €/m³ | 6% |
| saneamento, tarifa fixa por mês | — | — | 1,995 € | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 0 | 5 | 0,3875 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 5 | 15 | 0,7606 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 15 | 25 | 1,4608 €/m³ | 6% |
| saneamento, escalão (sobre 100% do volume de água) | 25 | sem limite | 2,4423 €/m³ | 6% |
| Taxa de Recursos Hídricos (TRH), por m³ de água | — | — | 0,0392 €/m³ | 6% |

Conta mensal conferida à mão, só com números impressos nos documentos (os testes exigem que o programa as reproduza):

<!-- tabela: Contas mensais de conferência do tarifário do Porto -->
| Consumo | Conta |
| ---: | ---: |
| 10 m³/mês | 20,2995 € |
| 30 m³/mês | 93,3293 € |

Hipóteses e dúvidas registadas ao transcrever:

- Tarifa de disponibilidade de água, utilizador doméstico, contador ≤ 20 mm (Q3 ≤ 4 m³/h): 0,1242 €/dia (pág. 2 do PDF, sob «Utilizadores domésticos») × 30 = 3,726 €/mês. O PDF repete a tabela na pág. 3 com 0,1367 €/dia para o mesmo escalão de contador; essa repetição vem depois da «Tarifa variável» dos utilizadores não domésticos (pág. 2) e sem cabeçalho próprio, e as demais linhas coincidem com as da pág. 2, por isso foi lida como a tarifa de disponibilidade dos não domésticos. Leitura por inferência do layout, a confirmar com a entidade gestora.
- Tarifa de disponibilidade de águas residuais: 0,0665 €/dia × 30 = 1,995 €/mês.
- IVA: 6% na água e nas águas residuais (Águas e Energia do Porto, EM).
- Taxa de Recursos Hídricos (TRH) da água: 0,0392 €/m³ devida à APA, com IVA a 6% (o PDF diz apenas que às tarifas acresce o IVA à taxa legal em vigor; os 6% são a taxa reduzida do Continente, não impressa no documento).
- Resíduos urbanos: não constam do tarifário da Águas e Energia do Porto (são da Porto Ambiente) e ficam de fora desta fatura. Meses de 30 dias, como nos escalões do PDF («/30 dias»).

### Eletricidade

O Funchal leva ainda a tarifa de eletricidade, para o custo de bombagem: tarifa Base da
Empresa de Eletricidade da Madeira, 6,90 kVA, 0,1673 €/kWh sem IVA. A fonte é um comparador
(luzegas.pt, atualizado em 20/02/2025), **secundária**: confirme na EEM ou na ERSE. Lisboa e
Porto não têm tarifa de eletricidade registada, e o custo de bombagem fica a zero até o
utilizador introduzir a sua.

## Documentos recolhidos e ainda não transcritos

Os documentos abaixo estão arquivados com o endereço de origem e a impressão digital, mas
ainda não foram transcritos para o programa, que por isso não os oferece. Neles, introduza o
tarifário à mão. O tarifário de Bragança, em vigor, continua por obter.

<!-- tabela: Concelhos com documento tarifário recolhido e ainda por transcrever -->
| Concelho | Entidade | Documento |
| :--- | :--- | :--- |
| Coimbra | Águas de Coimbra | editais n.º 433 e 438/2025 |
| Braga | AGERE | tarifário de fevereiro de 2026 |
| Setúbal | SMS Setúbal | água, saneamento e resíduos 2026 |
| Leiria | SMAS Leiria | tarifário 2026 |
| Faro | FAGAR | tarifário 2026 |
| Aveiro | AdRA | tarifário 2026 |
| Viseu | Águas de Viseu | tarifários de abril de 2026 |
| Beja | EMAS Beja | tarifário 2025 |
| Évora | Câmara Municipal de Évora | tarifário 2025 |
| Castelo Branco | SM Castelo Branco | tarifário em vigor (publicado em 24/02/2026) |
| Santarém | Águas de Santarém | tarifários geral e do saneamento 2026 |
| Ponta Delgada | SMAS Ponta Delgada | tarifário 2026 |
| Viana do Castelo | Águas do Alto Minho | cartaz do tarifário 2026 |
| Portalegre | SMAT Portalegre | edital 2026 |
| Guarda | Câmara Municipal da Guarda | edital n.º 16/2026 |
| Vila Real | ADIN e Câmara Municipal | tarifas 2026 e resíduos 2026 |

## Confiança dos valores tarifários por concelho

Nem todos os tarifários valem o mesmo. O Triton IBE traz transcritos 3 dos 280 concelhos que cobre (278 de Portugal continental, mais Funchal e Ponta Delgada), e para os restantes o utilizador introduz o tarifário do projeto. Para cada concelho, e para cada um dos três serviços (água, saneamento e resíduos urbanos), o programa de manutenção atribui um de três estados, com o motivo escrito.

Em Portugal a água, o saneamento de águas residuais e os resíduos urbanos são muitas vezes de entidades diferentes (em Lisboa, a EPAL fornece a água e a Câmara trata do saneamento e dos resíduos; no Porto, a Águas e Energia do Porto trata da água e do saneamento, e a EMAP dos resíduos). Por isso o estado é dado por serviço, cada um com a sua entidade e o seu documento. O saneamento cobra-se por escalões sobre uma fração do volume de água, o IVA vem de cada documento, a taxa de recursos hídricos (TRH) é uma parcela própria e a tarifa fixa depende do calibre do contador. Só se avalia o utilizador doméstico.

### A escala e os critérios

<!-- tabela: Estados de confiança dos valores tarifários e respetivos critérios -->
| Estado | Critério |
| :--- | :--- |
| 🟢 verde, verificado | Documento oficial arquivado com URL e SHA-256; `confirmado_em` há menos de 12 meses; transcrição conferida com as contas impressas; verificação independente registada em `verificado_por` (fatura real com tolerância de ±0,05 €, ou segunda leitura por uma pessoa diferente do transcritor; um modelo de IA nunca conta); e nenhuma pendência com efeito acima de 1 % na conta de 10 m³. |
| 🟡 amarelo, a validar | Há documento oficial arquivado ou transcrito, mas falta algum dos requisitos do verde: transcrição, conferência, reconfirmação nos últimos 12 meses, verificação independente, ou há pendência com efeito acima de 1 %. |
| ⚪ cinza, sem dado | Sem documento oficial arquivado, entidade gestora por identificar, ou dado ruim. O programa não traz tarifário e a ficha da ERSAR indica onde o procurar. |

O estado do concelho é verde quando os três serviços são verdes, cinza quando são todos cinza, e amarelo nos restantes casos. **Não há verde sem verificação independente**: a transcrição feita por quem leu o documento prova a aritmética, não a leitura. Uma **pendência** é uma hipótese que o documento não resolve (o IVA aplicado, um valor que não vem impresso, a leitura de uma tabela); cada uma traz o efeito estimado na conta de 10 m³ e, acima de 1 %, impede o verde.

### Situação em 23/10/2026

<!-- tabela: Concelhos e serviços por estado de confiança dos valores tarifários -->
| Estado | Concelhos | Água | Saneamento | Resíduos |
| :--- | ---: | ---: | ---: | ---: |
| 🟢 verde, verificado | 0 | 0 | 0 | 0 |
| 🟡 amarelo, a validar | 42 | 42 | 42 | 11 |
| ⚪ cinza, sem dado | 238 | 238 | 238 | 269 |
| **total** | **280** | **280** | **280** | **280** |

Por distrito (e região autónoma), com o estado do concelho:

<!-- tabela: Concelhos por distrito e estado de confiança dos valores tarifários -->
| Distrito | 🟢 verde | 🟡 amarelo | ⚪ cinza | Total |
| :--- | ---: | ---: | ---: | ---: |
| Aveiro | 0 | 10 | 9 | 19 |
| Beja | 0 | 1 | 13 | 14 |
| Braga | 0 | 1 | 13 | 14 |
| Bragança | 0 | 3 | 9 | 12 |
| Castelo Branco | 0 | 1 | 10 | 11 |
| Coimbra | 0 | 1 | 16 | 17 |
| Évora | 0 | 1 | 13 | 14 |
| Faro | 0 | 1 | 15 | 16 |
| Guarda | 0 | 1 | 13 | 14 |
| Leiria | 0 | 1 | 15 | 16 |
| Lisboa | 0 | 1 | 15 | 16 |
| Portalegre | 0 | 1 | 14 | 15 |
| Porto | 0 | 1 | 17 | 18 |
| Região Autónoma da Madeira | 0 | 1 | 0 | 1 |
| Região Autónoma dos Açores | 0 | 1 | 0 | 1 |
| Santarém | 0 | 1 | 20 | 21 |
| Setúbal | 0 | 1 | 12 | 13 |
| Viana do Castelo | 0 | 7 | 3 | 10 |
| Vila Real | 0 | 6 | 8 | 14 |
| Viseu | 0 | 1 | 23 | 24 |

A tabela concelho a concelho (entidade gestora de cada serviço, estado de cada serviço, vigência, o que falta e a ligação ao documento ou à ficha tarifária da ERSAR) acompanha o programa em `tarifas_portugal/CONFIANCA_POR_CONCELHO.csv`, em formato aberto.

Os concelhos transcritos:

<!-- tabela: Concelhos com tarifário transcrito e o estado de cada serviço -->
| Concelho | Água | Saneamento | Resíduos | O que falta |
| :--- | :--- | :--- | :--- | :--- |
| Funchal | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); pendência (efeito não quantificável): a tabela não diz se o preço do escalão atingido vale por faixa ou para todo o volume; água: pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; saneamento: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero; pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; resíduos: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero |
| Lisboa | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); saneamento: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 %; resíduos: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 % |
| Porto | 🟡 | 🟡 | ⚪ | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); água: pendência (efeito de 1,96 % na conta): tarifa de disponibilidade da água lida por inferência do layout (0,1242 €/dia; a outra leitura, 0,1367 €/dia, subiria a conta de 10 m³ 1,96 %); resíduos: entidade EMAP: sem documento arquivado |

### Como ler o estado

1. Procure o concelho do projeto. A entidade gestora de cada serviço vem da ficha tarifária da ERSAR (e, no Funchal e em Ponta Delgada, do próprio documento); quando nenhuma fonte a indica, a tabela diz «a identificar».
2. Leia o estado de cada serviço, não só o do concelho: um concelho amarelo pode ter a água documentada e os resíduos sem dado.
3. Leia «o que falta». É a lista do que o utilizador deve verificar antes de apoiar uma conclusão económica.
4. Confira a vigência. Os tarifários portugueses mudam em regra todos os anos, em janeiro ou nos primeiros meses, e um tarifário com mais de 12 meses pode já ter sido substituído.

### O que fazer em concelhos amarelos e cinzentos

- **Cinza.** Obtenha o tarifário em vigor da entidade gestora de cada serviço (a ficha da ERSAR indica a entidade e o ano), introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5) e confira a fatura que o programa calcula com uma fatura real do edifício.
- **Amarelo.** O valor tem documento oficial por trás, mas não foi verificado de modo independente. Confira a conta com uma fatura real e, se o programa lhe der um valor diferente por mais de 0,05 €, use o da fatura.
- **Em qualquer estado diferente de verde.** Declare no estudo a entidade gestora, a data de vigência e o estado de confiança, e acompanhe o resultado económico de uma análise de sensibilidade à tarifa.

## Introduzir o seu tarifário

1. Obtenha o documento tarifário em vigor da sua entidade gestora e anote a data.
2. Introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5).
3. Confira a fatura que o programa calcula com uma fatura real do edifício.
4. Declare no estudo a entidade gestora, a data de vigência, o regime e a moeda.

