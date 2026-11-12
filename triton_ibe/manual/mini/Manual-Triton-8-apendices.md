# Triton IBE

## Manual do Utilizador — Apêndices

Igor Catão Martins Vaz e Enedir Ghisi

Grupo de Pesquisa em Ambientes Sustentáveis
Universidade Federal de Santa Catarina

2026

---

### Sobre este volume

Este é um dos oito volumes em que o manual do Triton pode ser distribuído, e
reúne os apêndices do manual completo. Serve para enviar
apenas a parte que interessa: o método a um revisor, o tutorial a uma turma, os guias
a quem já utiliza o programa.

A numeração das secções e das equações é a mesma do manual completo, de modo que
uma remissão vale nos dois. Quando o texto remete para uma secção que está noutro
volume, o nome do volume vem entre parênteses.

| Volume | Conteúdo |
| :--- | :--- |
| Comece aqui | o capítulo 1 (Comece aqui) e o apêndice G |
| O método | o capítulo 2 (O método) e os apêndices A, B, C, E, G e H |
| Guias de uso | o capítulo 3 (Guias disponíveis no programa) e os apêndices D, F e G |
| Tutorial | o capítulo 4 (Tutorial: um exemplo do começo ao fim) e os apêndices G, I e J |
| Enganos, limitações e confiabilidade | o capítulo 5 (Enganos, limitações e confiabilidade) e os apêndices G e H |
| Correções, bugs e versionamento | o capítulo 6 (Correções, bugs e versionamento) |
| Modulação probabilística | o capítulo 7 (Modulação probabilística) e os apêndices G e H |
| **Apêndices** | os apêndices |

### Como citar

> VAZ, Igor Catão Martins; GHISI, Enedir. **Triton: manual do utilizador**.
> Apêndices. Versão 0.2.0. Universidade Federal de Santa
> Catarina, 2026.

---

## Índice

**Apêndices**

Apêndice A — Os parâmetros do projeto

Apêndice B — Os processos do programa

Apêndice C — Fatores de emissão

Apêndice D — Regimes tarifários

Apêndice E — Base climática

Apêndice F — Arquivos, pastas e formatos

Apêndice G — Glossário

Apêndice H — Referências

Apêndice I — Fichas de uma página

Apêndice J — Arquivos de exemplo



## Lista de tabelas

Tabela 1 — Parâmetros do projeto: identificação

Tabela 2 — Parâmetros do projeto: chuva

Tabela 3 — Parâmetros do projeto: captação

Tabela 4 — Parâmetros do projeto: edificação

Tabela 5 — Parâmetros do projeto: procura

Tabela 6 — Parâmetros do projeto: rega

Tabela 7 — Parâmetros do projeto: qualidade da água

Tabela 8 — Parâmetros do projeto: reservatórios

Tabela 9 — Parâmetros do projeto: eletrobomba

Tabela 10 — Parâmetros do projeto: tubagem

Tabela 11 — Parâmetros do projeto: investimento

Tabela 12 — Parâmetros do projeto: exploração

Tabela 13 — Parâmetros do projeto: tarifário

Tabela 14 — Parâmetros do projeto: energia

Tabela 15 — Parâmetros do projeto: financeiro

Tabela 16 — Parâmetros do projeto: certificações

Tabela 17 — Parâmetros do projeto: outros

Tabela 18 — Fatores de emissão que o utilizador indica, e o que declarar em cada um

Tabela 19 — Fatores de emissão dos materiais dos reservatórios, com massa e fronteira

Tabela 20 — Referência registada no programa para cada fator de material, e a sua situação

Tabela 21 — Fatores de emissão dos consumíveis de tratamento

Tabela 22 — Os códigos da tabela tarifária de água

Tabela 23 — Como o programa guarda cada parcela da fatura portuguesa

Tabela 24 — As quatro formas de introduzir o saneamento

Tabela 25 — Os seis regimes tarifários e o que acontece ao poupar

Tabela 26 — Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço

Tabela 27 — Estrutura do tarifário do Funchal

Tabela 28 — Contas mensais de conferência do tarifário do Funchal

Tabela 29 — Estrutura do tarifário de Lisboa

Tabela 30 — Contas mensais de conferência do tarifário de Lisboa

Tabela 31 — Estrutura do tarifário do Porto

Tabela 32 — Contas mensais de conferência do tarifário do Porto

Tabela 33 — Concelhos com documento tarifário recolhido e ainda por transcrever

Tabela 34 — Estados de confiança dos valores tarifários e respetivos critérios

Tabela 35 — Concelhos e serviços por estado de confiança dos valores tarifários

Tabela 36 — Concelhos por distrito e estado de confiança dos valores tarifários

Tabela 37 — Concelhos com tarifário transcrito e o estado de cada serviço

Tabela 38 — Conteúdo da base de precipitação por concelho da Edição Ibérica

Tabela 39 — Concelhos de Portugal continental por nível de qualidade da chuva

Tabela 40 — Série de precipitação distribuída com a Edição Ibérica

Tabela 41 — Cobertura geográfica da Edição Ibérica nesta versão

Tabela 42 — Os conjuntos de dados da Edição Ibérica, a fonte e a licença

Tabela 43 — Formatos que o programa lê e onde cada um é carregado

Tabela 44 — Formatos que o programa escreve e onde cada um é gerado

Tabela 45 — As sete secções do ficheiro de projeto e o que cada uma guarda

Tabela 46 — Localização dos ficheiros do programa e dos ficheiros do utilizador

Tabela 47 — Secções do ficheiro estudo.json (esquema triton-estudo, versão 1)

Tabela 48 — Apelidos das substituições e o campo do projeto que cada um altera

Tabela 49 — Ficheiros que triton estudo run grava na pasta de saída

Tabela 50 — Compatibilidade entre versões do ficheiro de projeto

Tabela 51 — Padronização terminológica de água de chuva e água pluvial

Tabela 52 — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial

Tabela 53 — Ficha de consulta: os dez passos de um estudo completo e a secção que trata de cada um

Tabela 54 — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada

Tabela 55 — Ficha de consulta: os seis regimes tarifários e o efeito de poupar

Tabela 56 — Ficha de consulta: os indicadores e a pergunta que cada um responde

Tabela 57 — Os casos de exemplo e o que cada um demonstra

Tabela 58 — Resultado que cada caso de exemplo produz ao ser relido e simulado

---


---
# Apêndices

---

## Apêndice A — Os parâmetros do projeto

São **119 parâmetros**. É a lista completa do que um projeto guarda nesta
edição, com o nome exato de cada campo dentro do ficheiro `.triton`.

A lista não foi transcrita à mão: é extraída do próprio programa a cada versão, e por
isso não pode divergir dele.

A coluna **onde se introduz** diz em que ecrã o campo aparece; a coluna **quem consome**
diz que cálculo o usa. Um campo sem nenhuma das duas é um campo gravado no ficheiro e
nunca lido, e está listado na secção 5.2 (volume Enganos, limitações e confiabilidade).

Os padrões são os do projeto com que a Edição Ibérica abre: a chuva é a normal 1986-2015
do município de Lisboa [PT-1106] no Iberia01, e os custos, os preços e a tarifa de eletricidade
partem de zero ou vazios, para o utilizador os introduzir em euros. Um traço significa
que o campo não tem valor inicial.

O ficheiro de projeto guarda ainda 4 campos de esquemas nacionais de outras
edições. Não têm efeito nesta e não são listados.

### A.1. Identificação

3 parâmetros.

<!-- tabela: **Tabela 1** — Parâmetros do projeto: identificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | Novo projeto Triton | — | Exportação, Janela principal, Relatórios | Automação, CAD e BIM, Folhas de cálculo, Relatórios |
| `project_id` | — | — | Janela principal, Relatórios | Automação |
| `created_at` | — | — | Janela principal | — |

### A.2. Chuva

9 parâmetros.

<!-- tabela: **Tabela 2** — Parâmetros do projeto: chuva -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Janela principal, Projeto | Automação, Cenários, Folhas de cálculo |
| `climate_source_mode` | national_db | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_city_uf` | PT\|Lisboa | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_city_name` | Lisboa [PT-1106] | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_model` | Iberia01 v1.0 | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_scenario` | IBERIA01 | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_start_date` | 01/01/1986 | — | Janela principal, Projeto, Relatórios | Automação |
| `climate_end_date` | 31/12/2015 | — | Janela principal, Projeto, Relatórios | Automação |
| `start_date` | 01/01/1980 | — | Exportação, Janela principal, Projeto, Tarifário e custos | Automação, Clima, Folhas de cálculo |

Observações do código:

- `climate_source_mode`: "national_db" (a base de chuva por município: Iberia01, ou a E-OBS opcional) ou "custom_file" (ficheiro do utilizador)

### A.3. Captação

7 parâmetros.

<!-- tabela: **Tabela 3** — Parâmetros do projeto: captação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | — | — | Ambiental, Documentação, Gráficos, Janela principal, Projeto, Qualidade, Relatórios | ACV, Automação, CAD e BIM, Cenários, ETAP, Folhas de cálculo, Relatórios |
| `discard_mode` | 1 | — | Janela principal, Projeto, Varrimento | Automação, Balanço diário, Cenários |
| `discard_days_interval` | 7 | — | Janela principal, Projeto, Varrimento | Automação, Balanço diário, Cenários |
| `area` | 100 | — | Ambiental, Documentação, Edificação, Gráficos, Janela principal, Qualidade, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Balanço diário, CAD e BIM, Cenários, ETAP, Folhas de cálculo, Relatórios |
| `irrigation_garden_area_m2` | 0 | — | — | — |
| `runoff_coeff` | — | — | Edificação, Janela principal, Qualidade, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `first_flush_system_enabled` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `discard`: mm
- `discard_mode`: 1 = todos os eventos, 2 = 1.º evento após período seco, 3 = a cada X dias
- `discard_days_interval`: intervalo para o modo 3
- `area`: m²
- `irrigation_garden_area_m2`: Área de jardim em m² para o assistente de dimensionamento
- `runoff_coeff`: ver hydrology_defaults

### A.4. Edificação

2 parâmetros.

<!-- tabela: **Tabela 4** — Parâmetros do projeto: edificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | — | Ambiental, Edificação | Automação, Económico |
| `building_template_id` | res_medio | — | Edificação | Automação, Tarifário |

Observações do código:

- `num_economias`: Número de frações autónomas com contador individual

### A.5. Procura

17 parâmetros.

<!-- tabela: **Tabela 5** — Parâmetros do projeto: procura -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `demand_type` | 0 | — | — | — |
| `demand_mode` | constant | — | Ambiental, Edificação, Janela principal, Relatórios, Varrimento | Automação, Balanço diário |
| `demand_value` | 200 | — | Documentação, Económico, Janela principal | Automação, Balanço diário |
| `demand_monthly` | — | — | Janela principal | Automação |
| `residents_type` | 0 | — | — | — |
| `residents_count` | 4 | — | Ambiental, Económico, Janela principal | Automação, Balanço diário, Eletrobomba |
| `residents_monthly` | — | — | Janela principal | Automação |
| `potable_indoor_share` | 0,6 | — | Edificação, Janela principal | Automação |
| `non_potable_indoor_share` | 0,4 | — | Edificação, Janela principal | Automação, Balanço diário |
| `rainwater_share` | 0,4 | — | Documentação, Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `weekly_demands` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `weekly_residents` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `weekly_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `monthly_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_demands` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_residents` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |
| `daily_shares` | — | — | Edificação, Janela principal, Varrimento | Automação, Balanço diário |

Observações do código:

- `demand_mode`: "constant", "weekly", "monthly", "daily"
- `demand_value`: L/dia, por residente ou total
- `potable_indoor_share`: Fração potável do consumo interior; 1 − non_potable_indoor_share
- `non_potable_indoor_share`: Fração não potável do consumo interior (autoclismos, máquina de lavar); ver fracao_atendivel
- `rainwater_share`: fração de 0 a 1 (0,4 = 40%)

### A.6. Rega

4 parâmetros.

<!-- tabela: **Tabela 6** — Parâmetros do projeto: rega -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `irrigation_liters_per_day` | 0 | — | Ambiental, Edificação, Janela principal, Relatórios | Automação, Balanço diário |
| `irrigation_rain_threshold_mm` | 2 | — | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_potable_backup` | sim | — | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_rate_l_m2_day` | 3 | — | — | — |

Observações do código:

- `irrigation_liters_per_day`: Procura exterior (rega, lavagem de zonas exteriores), L/dia
- `irrigation_rain_threshold_mm`: Limiar diário de precipitação para suspender a rega (mm/dia)
- `irrigation_potable_backup`: Se True, a rede pública abastece a rega em dias secos se a cisterna secar
- `irrigation_rate_l_m2_day`: Taxa diária de rega (L/m²/dia)

### A.7. Qualidade da água

9 parâmetros.

<!-- tabela: **Tabela 7** — Parâmetros do projeto: qualidade da água -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `water_quality_target_class` | classe_1 | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_disinfection` | cloro | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_polishing` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `etap_enabled` | sim | — | Ambiental, Económico, Otimizador | ACV, Automação, ETAP |
| `chlorine_treatment_enabled` | sim | — | Ambiental, Económico, Otimizador, Qualidade | ACV, Automação, Económico |
| `chlorine_dose_mg_l` | — | — | Ambiental, Económico, Otimizador, Qualidade | ACV, Automação, ETAP, Económico, Relatórios |
| `chlorine_product_purity` | — | — | Ambiental, Qualidade | ACV, Automação, ETAP, Económico |
| `chlorine_cost_per_kg` | 0 | — | Económico, Otimizador, Qualidade | Automação, ETAP, Económico, Preços |
| `chlorine_co2_kg_per_kg` | — | — | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `water_quality_disinfection`: "cloro", "uv", "ozonio" (ozono), "nenhum"
- `chlorine_dose_mg_l`: mg de Cl2 ativo por litro
- `chlorine_product_purity`: kg de Cl2 ativo por kg de produto
- `chlorine_cost_per_kg`: € por kg de PRODUTO comercial

### A.8. Reservatórios

13 parâmetros.

<!-- tabela: **Tabela 8** — Parâmetros do projeto: reservatórios -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | — | Ambiental, Assistente da bomba, Económico, Exportação, Janela principal, Otimizador, Relatórios, Reservatório superior, Tarifário e custos, Varrimento | Automação, Balanço diário, CAD e BIM, Cenários, Folhas de cálculo, Multicritério, Preços |
| `upper_tank_used` | 1 | — | Ambiental, Económico, Janela principal, Otimizador, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Balanço diário, Cenários, Eletrobomba, Folhas de cálculo, Preços |
| `lower_tank_max` | 10000 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `lower_tank_step` | 250 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `lower_tank_mode` | 1 | — | Janela principal, Varrimento | Automação |
| `lower_tank_fixed` | 2000 | — | Janela principal, Tarifário e custos, Varrimento | Automação |
| `delta_ideal` | 5 | — | Janela principal, Otimizador, Varrimento | Automação, Cenários |
| `econ_lower_tank_vol` | 2000 | — | Ambiental, Económico, Tarifário e custos, Varrimento | Automação |
| `lower_tank_material` | PEAD | — | Económico, Otimizador, Tarifário e custos | ACV, Automação, Preços |
| `upper_tank_material` | PEAD | — | Económico, Otimizador, Tarifário e custos | ACV, Automação, Preços |
| `cost_lower_tank` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico, Preços |
| `cost_lower_tank_per_m3` | 0 | — | Tarifário e custos | Preços |
| `cost_upper_tank` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |

Observações do código:

- `upper_tank_vol`: L
- `upper_tank_used`: 0 = sem reservatório superior, 1 = com reservatório superior
- `lower_tank_max`: L
- `lower_tank_step`: L
- `lower_tank_mode`: 0 = volume fixo, 1 = varrimento
- `lower_tank_fixed`: usado no modo de volume fixo
- `delta_ideal`: limiar de ganho marginal para o volume ideal, em %/m³
- `lower_tank_material`: "PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)
- `upper_tank_material`: "PEAD" (polietileno), "CONCRETO" (betão), "FIBRA" (PRFV), "ACO_INOX" (aço inoxidável)

### A.9. Eletrobomba

18 parâmetros.

<!-- tabela: **Tabela 9** — Parâmetros do projeto: eletrobomba -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pumping_threshold` | 50 | — | Janela principal, Varrimento | Automação, Balanço diário, Cenários, Folhas de cálculo |
| `supply_arrangement` | — | — | Ambiental, Económico, Varrimento | ACV, Automação, Económico, Eletrobomba |
| `pressurizer_pressure_m` | 18 | — | Varrimento | Eletrobomba |
| `pressurizer_starts_per_person_day` | 5,05 | — | Varrimento | Eletrobomba |
| `pressurizer_model` | — | — | Varrimento | Eletrobomba |
| `pressurizer_point_flow_l_min` | 9 | — | Varrimento | Eletrobomba |
| `pressurizer_power_kw` | 0,18 | — | Varrimento | Eletrobomba |
| `pressurizer_flow_l_min` | 13,3 | — | Varrimento | Eletrobomba |
| `pressurizer_post_run_s` | 0 | — | Varrimento | Eletrobomba |
| `pump_count` | 2 | — | Ambiental, Económico, Otimizador, Relatórios, Tarifário e custos | ACV, Automação, Económico, Preços, Relatórios |
| `pump_power_str` | 1/2 | — | Relatórios | — |
| `pump_power_kw` | 0,36775 | — | Económico, Gráficos, Otimizador, Relatórios, Tarifário e custos, Varrimento | Automação, CAD e BIM, Económico, Eletrobomba, Preços, Relatórios |
| `pump_manometric_head_m` | 0 | — | Varrimento | Automação, Eletrobomba |
| `pump_efficiency` | 0 | — | Gráficos, Tarifário e custos, Varrimento | Automação, Eletrobomba |
| `pump_flow_rate` | 0 | — | Económico, Gráficos, Otimizador, Relatórios, Tarifário e custos, Varrimento | Automação, Eletrobomba |
| `pump_startup_time_h` | 0,03 | — | Económico, Gráficos, Otimizador, Tarifário e custos | Automação, Eletrobomba |
| `pump_motor_efficiency` | 0 | — | Tarifário e custos | Automação, Eletrobomba |
| `pump_unit_cost` | 0 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico, Preços |

Observações do código:

- `pumping_threshold`: L, nível de acionamento da elevação
- `pump_count`: principal + reserva como configuração inicial recomendada
- `pump_power_kw`: kW (1 cv = 0,7355 kW; 1/2 cv = 0,36775 kW)
- `pump_efficiency`: %, 0 = deduzir da potência
- `pump_startup_time_h`: h
- `pump_motor_efficiency`: %
- `pump_unit_cost`: preço de uma eletrobomba, em euros (zero até o utilizador o introduzir)

### A.10. Tubagem

1 parâmetro.

<!-- tabela: **Tabela 10** — Parâmetros do projeto: tubagem -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Económico, Tarifário e custos | ACV, Automação |

### A.11. Investimento

3 parâmetros.

<!-- tabela: **Tabela 11** — Parâmetros do projeto: investimento -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_piping` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_accessories` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, ETAP, Económico |

### A.12. Exploração

1 parâmetro.

<!-- tabela: **Tabela 12** — Parâmetros do projeto: exploração -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |

### A.13. Tarifário

17 parâmetros.

<!-- tabela: **Tabela 13** — Parâmetros do projeto: tarifário -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | não | — | Projeto | — |
| `water_tariffs` | — | — | Projeto, Tarifário, Tarifário e custos, Varrimento | Económico |
| `tariff_city_uf` | personalizado | — | Janela principal, Projeto, Relatórios, Tarifário, Tarifário e custos | — |
| `tariff_city_name` | personalizado | — | Janela principal, Projeto, Relatórios, Tarifário, Tarifário e custos | Automação |
| `tariff_vigencia` | — | — | Projeto, Tarifário e custos | — |
| `tariff_category` | residencial | — | Económico, Tarifário, Tarifário e custos | Tarifário |
| `sewage_rate` | 100 | — | Projeto, Tarifário, Tarifário e custos | Automação, Económico, Tarifário |
| `sewage_mode` | 1 | — | Económico, Otimizador, Projeto, Tarifário, Tarifário e custos | Automação, Económico, Tarifário |
| `sewage_tariffs` | — | — | — | Económico, Tarifário |
| `sewage_volume_factor` | 1 | — | — | Automação, Económico, Tarifário |
| `water_tax_fixed` | 0 | — | Tarifário e custos | Automação, Económico |
| `water_tax_var` | 0 | — | Tarifário e custos | Automação, Económico |
| `tariff_escalation` | 12 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `water_tariff_escalation` | 5 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `sewage_tariff_escalation` | 5 | — | Económico, Otimizador, Tarifário e custos | Automação, Económico |
| `elec_tariff_escalation` | 5 | — | Económico, Otimizador, Varrimento | Automação, Económico |
| `elec_tariff` | 0 | — | Económico, Gráficos, Otimizador, Projeto, Relatórios, Tarifário e custos, Varrimento | Automação, Económico |

Observações do código:

- `tariff_category`: categoria da tabela tarifária aplicada; "personalizada" quando introduzida pelo utilizador
- `sewage_mode`: 0 = valor fixo em €, 1 = percentagem da parcela de água, 2 = €/m³ consumido, 3 = escalões
- `water_tax_fixed`: € por mês
- `water_tax_var`: % (o IVA da água, nas faturas portuguesas)
- `tariff_escalation`: meses; duração do período de atualização
- `water_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `sewage_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `elec_tariff_escalation`: % por período de atualização; com 12 meses, % por ano
- `elec_tariff`: preço da eletricidade por kWh, em euros (zero até o utilizador o introduzir)

### A.14. Energia

4 parâmetros.

<!-- tabela: **Tabela 14** — Parâmetros do projeto: energia -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_city_name` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_tax_fixed` | 0 | — | Tarifário e custos | Automação, Económico |
| `elec_tax_var` | 0 | — | Tarifário e custos | Automação, Económico |

Observações do código:

- `elec_tax_fixed`: € por mês
- `elec_tax_var`: %

### A.15. Financeiro

4 parâmetros.

<!-- tabela: **Tabela 15** — Parâmetros do projeto: financeiro -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0,2 | — | Documentação, Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `analysis_period_years` | 20 | — | Económico, Otimizador, Relatórios, Tarifário e custos, Varrimento | ACV, Automação, Económico, Relatórios |
| `tma` | 2 | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |
| `install_month` | 0 | — | — | — |

Observações do código:

- `inflation`: % por mês; inflação dos custos de exploração e manutenção
- `analysis_period_years`: anos
- `tma`: % por mês; taxa de atualização

### A.16. Certificações

1 parâmetro.

<!-- tabela: **Tabela 16** — Parâmetros do projeto: certificações -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | — | Ambiental | — |

### A.17. Outros

6 parâmetros.

<!-- tabela: **Tabela 17** — Parâmetros do projeto: outros -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `phi_operation_rule` | — | — | Janela principal, Varrimento | Automação, Balanço diário, Folhas de cálculo |
| `data_base_estudo` | — | — | Tarifário e custos | — |
| `precos_de_catalogo` | não | — | Assistente da bomba, Económico, Otimizador, Qualidade, Tarifário e custos, Varrimento | Automação, ETAP, Preços |
| `bim_layout` | — | — | Exportação, Janela principal | — |
| `capex_do_arranjo` | não | — | Janela principal, Tarifário e custos, Varrimento | ETAP |
| `mao_de_obra_automatica` | não | — | Janela principal, Tarifário e custos, Varrimento | — |

---

## Apêndice B — Os processos do programa

São **24 processos**, do ficheiro de chuva ao relatório. Cada um declara o
que o desencadeia, o que recebe, as regras com as suas ramificações, o que produz e o
que acontece quando falha.

É o apêndice mais técnico do manual, e serve a duas pessoas: quem revê um estudo feito
com o programa e precisa de saber exatamente que conta foi feita, e quem encontrou um
resultado estranho e quer saber por onde o número passou.

Os nomes em `código` são os campos do ficheiro de projeto, listados no apêndice A.

### B.1. PROC-01 — Carregar a série de precipitação

*Chuva*

**Gatilho.** Separador Projeto: escolher o município na base ibérica (Iberia01), o concelho na E-OBS opcional, ou abrir um ficheiro CSV.

**Entradas**

- Município do Iberia01 v1.0 (8 319 municípios da Península e das Baleares, 1971 a 2015; ERA5 nas ilhas), concelho da E-OBS v33.0e opcional (278 concelhos, 1950 a 2025), ou ficheiro CSV diário em milímetros por dia
- `climate_start_date` e `climate_end_date`, que recortam a série (a normal 1986-2015 do Iberia01 é o recorte inicial)
- `start_date`, data do primeiro dia da série

**Regras**

1. A série vira um vetor `numpy` de milímetros por dia; o índice do vetor é o dia, e a data serve só para saber o dia da semana e o mês.
2. A série de um município é a média diária das células da grelha do Iberia01 (0,1°) com centro dentro do município (CAOP2025 em Portugal, LAU 2023 em Espanha); na E-OBS, a média das células da sua grelha. As ilhas ficam fora do domínio do Iberia01: Canárias, Madeira e Açores usam a reanálise ERA5 de 0,25° (nível C, com aviso); Ceuta e Melilla ficam sem série, e nenhum local recebe a série de um vizinho. Para esses, a série é um ficheiro do utilizador.
3. Dia sem dado em todas as células é uma falha (NaN), e a simulação recusa a série em vez de o tratar como dia seco.
4. Ano incompleto é descartado na leitura, para não enviesar totais anuais.
5. As bases vêm no programa, em `data/chuva_iberia01_p1.db` a `p4.db`, `data/chuva_ilhas_era5.db` e `data/portugal_eobs.db` (opcional); o exemplo do Funchal usa a ERA5 de ilha, e `data/rainfall/Funchal.csv` é a série de exemplo da edição.

**Saídas**

- `precip_data`: vetor de mm/dia, que é a entrada de **dois** processos distintos — PROC-04 (descarte e captação) e PROC-03 (suspensão da rega)

**Exceção.** Ficheiro ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; a simulação não corre com série vazia ou com falhas.

### B.2. PROC-02 — Compor a procura diária

*Procura*

**Gatilho.** Início da simulação, uma vez por execução.

**Entradas**

- `demand_mode`: constante, semanal, mensal ou diária
- `demand_value` (L/dia por pessoa), `residents_count`
- `rainwater_share` ou `non_potable_indoor_share`
- vetores `weekly_*`, `monthly_*`, `daily_*` quando o modo os usa

**Regras**

1. Procura-base do dia = `demand_value × residents_count`, com o multiplicador do dia da semana, do mês ou do dia, conforme o modo.
2. A fração não potável separa a procura em duas: interna potável e interna não potável.
3. Quando o modo é semanal, mensal ou diário, a fração vem do próprio vetor do período; fora disso, vale `non_potable_indoor_share`, e só então `rainwater_share`.
4. Valor nulo ou zero em qualquer posição do vetor cai para o valor constante.

**Saídas**

- `tot_arr`: procura total do dia
- `pot_in_arr`: potável interna, que a chuva nunca atende
- `non_pot_in_arr`: não potável interna, prioridade 1 da chuva
- `pluv_arr` = não potável interna + rega ativa

**Exceção.** Data inicial ilegível cai para 01/01/1980 em vez de interromper, porque só afeta o dia da semana.

### B.3. PROC-03 — Suprimir a rega nos dias de chuva

*Procura*

**Gatilho.** Composição da procura, um teste por dia da série.

**Entradas**

- `irrigation_liters_per_day`
- `irrigation_rain_threshold_mm` (padrão 2 mm/dia)
- `precip_data`, o **mesmo** vetor que alimenta a captação

**Regras**

1. Se a chuva do dia ≥ limiar, a rega do dia é **zero** e o dia entra na contagem de dias suprimidos.
2. Caso contrário, a rega do dia é o volume nominal.
3. É a segunda leitura do ficheiro de chuva, e independente da primeira: um dia pode suprimir a rega e ainda assim render captação.

**Saídas**

- `irr_arr`: rega do dia
- `irr_suppressed_mask`: dias suprimidos, que viram `total_irrigation_days_suppressed` no resultado

**Exceção.** Sem volume de rega registado, o vetor é zero e a máscara é falsa em todos os dias.

### B.4. PROC-04 — Descartar as primeiras águas

*Balanço hídrico*

**Gatilho.** Todo dia com chuva, dentro do ciclo diário.

**Entradas**

- `precip_mm` do dia
- `discard_mm`
- `discard_mode` (1, 2 ou 3)
- `discard_days_interval`

**Regras**

1. **Modo 1**: descarta em todo evento de chuva.
2. **Modo 2**: descarta apenas no primeiro evento após período seco, definida como véspera com menos de 1 mm.
3. **Modo 3**: descarta quando passaram `discard_days_interval` dias desde o último descarte.
4. Quando o descarte se aplica: `p_eff = p − discard_mm` se `p > discard_mm`, senão **zero**: toda a chuva do dia vai para o descarte.
5. Quando não se aplica: `p_eff = p`, a chuva inteira é aproveitável.

**Saídas**

- `p_eff`: lâmina efetiva do dia, em mm, que segue **só** para PROC-05
- `eff_precip_mm` na série diária detalhada, quando ela é guardada

**Exceção.** Lâmina de descarte negativa é rejeitada na barreira de validação, antes do ciclo.

### B.5. PROC-05 — Converter lâmina em volume captado

*Balanço hídrico*

**Gatilho.** Todo dia, depois do descarte.

**Entradas**

- `p_eff` de PROC-04
- `area` (m²)
- `runoff_coeff`

**Regras**

1. `v_ac = p_eff × area × runoff_coeff`, em litros.
2. É aqui que o ficheiro de chuva vira volume, e é o único ponto onde isso acontece.
3. O coeficiente é adimensional e fica em [0, 1]; fora disso a simulação nem começa.

**Saídas**

- `v_ac`: volume captado do dia, que segue para PROC-06
- `harvested_liters` na série diária

**Exceção.** Área negativa ou coeficiente fora de [0, 1] levantam `ValueError` nomeando o campo, em PROC-11.

### B.6. PROC-06 — Armazenar e extravasar

*Balanço hídrico*

**Gatilho.** Todo dia, depois da captação.

**Entradas**

- `v_ac`
- volume remanescente do dia anterior
- `lower_tank_vol`

**Regras**

1. **Extravasamento antes do consumo**, como na regra YAS; a chuva do dia, até a capacidade, já atende a procura do dia, o que põe o modelo entre a YAS e a YBS estritas.
2. `disponível = v_lower + v_ac`. Se passar da capacidade, o excedente extravasa e o reservatório fica cheio.
3. A ordem importa: retirar a procura antes faria o reservatório aceitar água que fisicamente já teria extravasado, sobrestimando o aproveitamento.

**Saídas**

- `v_spill_today`, somado em `avg_spilled_l_day`, que vira critério de extravasamento no multicritério
- `v_in_tank`, o volume disponível para atendimento

**Exceção.** Volume zero é válido e representa o cenário sem sistema; negativo é rejeitado.

### B.7. PROC-07 — Atender com reservatório único

*Balanço hídrico*

**Gatilho.** Todo dia, quando não há reservatório superior.

**Entradas**

- `v_in_tank`
- `pluvial_demand_per_day` de PROC-02

**Regras**

1. `v_c = min(procura pluvial, volume no reservatório)`.
2. O volume remanescente permanece para o dia seguinte: `v_lower = v_in_tank − v_c`.

**Saídas**

- `v_c`: volume pluvial consumido no dia

**Exceção.** Nenhuma: o mínimo já trata reservatório vazio e procura nula.

### B.8. PROC-08 — Atender com elevação para reservatório superior

*Balanço hídrico*

**Gatilho.** Todo dia, quando `upper_tank_used` e o volume superior é positivo.

**Entradas**

- `v_lower`, `v_upper`
- `upper_tank_vol`
- `pumping_threshold`, o volume de reserva que não se consome

**Regras**

1. Laço até a procura ser atendida ou a água acabar.
2. Primeiro consome do reservatório superior o que estiver **acima** do limiar de acionamento.
3. Se ainda falta e há água em baixo, aciona a bomba: transfere `min(v_lower, espaço livre em cima)`, conta **um ciclo** e regista a lote.
4. Depois do elevação, consome de novo.
5. O limiar é limitado ao volume do reservatório superior na entrada do processo.

**Saídas**

- `v_c`
- `v_rec_today`, somado em `total_pumped_liters`
- `cycles_today`, somado em `total_pump_cycles`
- `max_pump_batch_liters`

**Exceção.** Volume superior negativo é rejeitado na validação. O ciclo tem saída garantida: se não há água em baixo nem em cima, interrompe.

### B.9. PROC-09 — Repartir o atendimento e completar com potável

*Balanço hídrico*

**Gatilho.** Todo dia, depois do atendimento.

**Entradas**

- `v_c`
- `non_pot_in_day`
- `irr_day`
- `pot_in_day`
- `irrigation_potable_backup`

**Regras**

1. **Prioridade 1**, uso interno não potável: `c_pluv_in = min(v_c, não potável interna)`.
2. **Prioridade 2**, rega: `c_pluv_irr = min(v_c − c_pluv_in, rega do dia)`.
3. O potável consumido é a soma de três parcelas: o potável interno, o déficit do não potável interno e — só se o suprimento de reserva estiver ligado — o déficit da rega.
4. Com o suprimento de reserva desligado, o jardim simplesmente não é regado no dia seco, e a rede não é acionada.

**Saídas**

- `potable_consumed_liters` do dia
- `avg_pluvial_indoor_consumed_l_day` e `avg_pluvial_irrigation_consumed_l_day`, que separam o uso interno do externo para os créditos WEc1 e WEc2 do LEED v4 e as Opções 2 e 4 do WEc2 do LEED v5

**Exceção.** Nenhuma: todas as parcelas são mínimos e máximos com zero.

### B.10. PROC-10 — Classificar o atendimento do dia

*Balanço hídrico*

**Gatilho.** Todo dia, ao fim do atendimento.

**Entradas**

- `v_c`
- `pluvial_demand_per_day`

**Regras**

1. **Pleno** quando o consumido iguala a procura pluvial, com tolerância de 10⁻⁵ L.
2. **Parcial** quando consumiu algo, mas menos que a procura.
3. **Nulo** quando não consumiu nada.

**Saídas**

- `pct_days_full_satisfaction`, `pct_days_partial_satisfaction` e `pct_days_null_satisfaction`, que são a confiabilidade temporal do sistema

**Exceção.** Nenhuma.

### B.11. PROC-11 — Validar a entrada física

*Balanço hídrico*

**Gatilho.** Primeira linha de `run_single_simulation`, antes de qualquer conta.

**Entradas**

- volume inferior e superior
- área
- coeficiente de escoamento
- lâmina de descarte
- procura diária
- fração pluvial

**Regras**

1. Volume negativo, área negativa, descarte negativo e procura negativa são recusados.
2. Coeficiente de escoamento e fração pluvial têm de ficar em [0, 1].
3. **Volume zero continua válido**: é a referência «sem sistema» da varrimento.
4. A mensagem nomeia o campo e o valor recebido, em vez de corrigir por baixo dos panos.

**Saídas**

- Nenhuma saída: ou passa, ou levanta `ValueError`

**Exceção.** É o próprio tratamento. Antes desta porta, volume de −1.000 L devolvia −166,67% de economia, e o número seguia para o económico, para a ACV e para o relatório.

### B.12. PROC-12 — Agregar o período e calcular os indicadores

*Balanço hídrico*

**Gatilho.** Fim do ciclo diário.

**Entradas**

- acumuladores do ciclo
- `n_days`

**Regras**

1. **Potencial de economia** = pluvial consumido no período ÷ procura total do período × 100.
2. As médias diárias dividem os acumulados pelo número de dias simulados.
3. As conversões para o ano usam **365,25** dias, e não 365, para absorver os bissextos da série.
4. O potencial fica sempre em [0, 100] — invariante que a barreira de validação existe para garantir.

**Saídas**

- `SingleTankSimulationResult`, com 21 campos, que é o objeto que **todos** os módulos a jusante consomem

**Exceção.** Procura total nula devolve potencial zero em vez de dividir por zero.

### B.13. PROC-13 — Varrer volumes e achar o volume ideal

*Balanço hídrico*

**Gatilho.** Separador Varrimento: botão de simular.

**Entradas**

- `lower_tank_max`
- `lower_tank_step`
- `delta_ideal` (%/m³)

**Regras**

1. A grade discreta arredonda o passo **para cima** até o múltiplo de 250 L, que é o quantum comercial de reservatório, e limita a 40 volumes positivos.
2. O volume máximo informado é sempre preservado como último ponto, de modo que só o último intervalo pode ser menor que o passo.
3. Zero entra na grade como alternativa de referência.
4. Roda PROC-04 a PROC-12 uma vez por volume.
5. O **volume ideal** é o primeiro cujo ganho marginal `Δpotencial/Δm³` cai abaixo do limiar: a partir dali, mais reservatório não compensa.

**Saídas**

- `SweepSimulationResult`: um resultado por volume, o volume ideal, e o registo de que o passo foi ajustado
- A lista de volumes é a lista de **candidatos** do multicritério

**Exceção.** Passo maior que o máximo devolve grade com um ponto. O ajuste do passo é registado em `step_adjusted`, e não silenciado.

### B.14. PROC-14 — Calcular os índices pluviométricos

*Chuva*

**Gatilho.** Separador Gráficos e relatório científico.

**Entradas**

- `precip_data`
- datas da série

**Regras**

1. Nove índices: PRCPTOT, R95p, RX1day, RX5day, SDII, R20mm, CDD, CWD e o índice de sazonalidade de Walsh e Lawler.
2. O conjunto **não** é ETCCDI puro: a sazonalidade não é do conjunto, e o R10mm, que é, está ausente.
3. O percentil 95 é calculado sobre a **série inteira carregada**, e não sobre a base fixa 1961–1990 do ETCCDI.
4. O RX5day usa `min_periods=1`, de modo que as primeiras janelas do ano têm de 1 a 4 dias.

**Saídas**

- Nove séries anuais, para gráfico e relatório

**Exceção.** Série menor que um ano devolve os índices possíveis, sem interromper.

### B.15. PROC-15 — Dimensionar a estação de tratamento

*Qualidade e ETAP*

**Gatilho.** Mudança na separador Qualidade da Água, ou início do económico e da ACV.

**Entradas**

- `water_quality_target_class` (4 classes de uso)
- `water_quality_disinfection`: cloro, ultravioleta ou ozono
- `water_quality_polishing`, filtro de polimento
- `annual_pluvial_m3` de PROC-12
- `area`
- dose, pureza, preço e fator de CO₂ do cloro
- `discard` e `first_flush_system_enabled`, para o descarte inicial

**Regras**

1. A classe alvo define as etapas obrigatórias; a desinfeção escolhida define o equipamento e o exploração.
2. O filtro de polimento é aplicado **se e somente se** marcado; quando a classe o recomendaria e o utilizador recusa, isso fica registado em `polishing_recommended_but_declined` em vez de ser imposto.
3. O que se compra é o **produto** — pastilha a 65% de cloro ativo — e não o cloro puro. Faturar a massa de cloro ativo, e não a do produto, subestima o custo em cerca de 35%.
4. **Regra incremental**: o CAPEX da linha desconta a verba genérica de tratamento já embutida em «Acessórios», e os custos de exploração descontam a cloragem, que o fluxo de caixa já paga. A regra vive num lugar só, consumida pelos **dois** motores económicos.
5. Com `first_flush_system_enabled`, o dispositivo de descarte inicial, de volume `discard × area`, entra no CAPEX e no exploração da linha.
6. Na ACV, a linha de tratamento **substitui** o termo de cloragem; nunca soma a ele.
7. Com `etap_enabled = False`, a linha de tratamento não entra em conta alguma: nem no CAPEX, nem no exploração, nem na avaliação ambiental.

**Saídas**

- `total_etap_capex`, que entra no CAPEX
- `total_etap_annual_opex`, que entra no exploração
- `total_etap_co2e_kg_yr`, que substitui a cloragem na ACV
- `disinfection_stages`, exibido no relatório

**Exceção.** Pureza fora de (0, 1] é recusada pelo validador da cadeia de cloragem.

### B.16. PROC-16 — Calcular a energia de bombeamento

*Eletrobomba*

**Gatilho.** Económico e ACV, a partir do mesmo resultado de simulação.

**Entradas**

- `supply_arrangement`: elevação, pressurização direta ou gravidade
- `total_pumped_liters` e `total_pump_cycles` de PROC-08
- `pressurizer_pressure_m`, `pressurizer_starts_per_person_day`, `residents_count`
- `pump_power_kw`, `pump_efficiency`, `pump_flow_rate`
- `pump_manometric_head_m`
- `pump_startup_time_h`

**Regras**

1. O arranjo decide o que se bombeia. **Elevação**: o volume enviado ao reservatório superior. **Pressurização direta**: todo o volume pluvial consumido, com a pressão de trabalho no lugar da altura e sem energia de partida. **Gravidade**: nada. É a única fonte de kWh do económico e da ACV.
2. Energia específica `e = ρgH/(η_bomba·η_motor)` por m³ elevado, ou `P/(Q·η_motor)` quando a caudal é declarada.
3. A potência de placa é potência de eixo e **já embute** o rendimento da bomba; por isso `P × horas / η_bomba` conta esse rendimento duas vezes, e o que falta é dividir pelo rendimento do motor. Quatro cópias dessa fórmula antiga sobreviviam no programa e sobrestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no multicritério.
4. A energia de partida entra à parte, pelo número de ciclos.
5. Caudal e rendimento não informados caem para valores típicos **da potência escolhida**, e não para constantes fixas.

**Saídas**

- `annual_kwh`, que vira custo no económico e emissão na ACV
- `pump_hours_year`, `annual_cycles`

**Exceção.** Arranjo por gravidade, arranjo não informado num projeto antigo, ou potência zero: a energia é zero.

### B.17. PROC-17 — Calcular a fatura de água, saneamento e resíduos

*Económico*

**Gatilho.** Duas vezes por mês de projeção: com e sem aproveitamento.

**Entradas**

- volume mensal em litros
- `water_tariffs`: quádruplas (mínimo, máximo, valor, código)
- `sewage_mode` e `sewage_rate`
- taxas fixa e variável (nelas entram o IVA e as parcelas fixas)
- `num_economias`, o número de frações autónomas com contador individual

**Regras**

1. O consumo é avaliado **no patamar de uma fração** e multiplicado pelo número de frações, para não distorcer os escalões progressivos em prédio com contadores individuais.
2. Código **1** ou **0**: escalão progressivo, cobrado só sobre o volume dentro dele.
3. Código **−1**, tarifa de disponibilidade: valor fixo que **soma** ao consumo medido.
4. Código **−2**, franquia retroativa: até ao volume da franquia paga-se o valor fixo; passando-o, **todo** o volume desde zero é tarifado pelos escalões.
5. Código **−3**, piso de pagamento: não soma, **limita por baixo**. Com piso de 40 € e consumo tarifado de 55 €, poupar até 15 € não reduz nada — e é exatamente isso que um estudo de aproveitamento pluvial precisa de ver.
6. A fatura portuguesa soma a água (tarifa fixa mensal e escalões por m³), o saneamento, os resíduos urbanos, a taxa de recursos hídricos (TRH) e o IVA de cada parcela, à taxa que o tarifário declara. Nenhuma taxa de IVA fica no código.
7. O saneamento pode ser cobrado por escalões próprios sobre o volume recolhido (coeficiente de recolha × volume de água; em Lisboa, 90%), com a TRH por m³ recolhido, ou como percentagem da **parcela de água**, e não da fatura total.
8. As tarifas fixas das parcelas que não são a água entram como taxa fixa mensal. Não variam com o consumo e anulam-se na poupança; entram para a conta mensal sair igual à impressa.
9. Os seis regimes tarifários são descritos no apêndice D; os tarifários transcritos (Lisboa, Porto e Funchal) estão nesse mesmo apêndice.

**Saídas**

- Valor da fatura de água, saneamento e resíduos em €/mês, para a projeção de PROC-18

**Exceção.** Tabela vazia dá fatura zero: o programa não presume tarifário. Estrutura incompleta é sinalizada pela barreira de validação, que separa erro de aviso. Os resíduos por escalões (Funchal) ainda não têm campo próprio: a parte variável soma-se à do saneamento.

### B.18. PROC-18 — Projetar o fluxo de caixa

*Económico*

**Gatilho.** Separador Económico, após a simulação técnica.

**Entradas**

- CAPEX das cinco rubricas mais bomba e ETAP
- poupança mensal de água e saneamento de PROC-17
- custos de exploração: bombagem, cloragem, ETAP e custos operacionais declarados
- `tma` (taxa de atualização), `inflation`, `analysis_period_years`
- atualizações separadas de água, saneamento e energia, e o intervalo entre atualizações

**Regras**

1. Água e saneamento são atualizados por índices **separados**, e não pela fatura agregada.
2. A inflação incide só sobre os custos de exploração; as atualizações tarifárias incidem só sobre a fatura.
3. A atualização é aplicada a cada `tariff_escalation` meses, em degraus.
4. O período de recuperação é o primeiro mês em que o acumulado descontado cruza zero.

**Saídas**

- `vpl` (VAL), `tir_monthly_pct`, `tir_annual_pct`, `payback_months`
- `monthly_cash_flows`, série mês a mês
- `annual_pump_kwh`, `annual_chlorine_kg`

**Exceção.** Poupança mensal negativa é truncada em zero antes de entrar no fluxo. TIR sem raiz real devolve nulo em vez de um número inventado.

### B.19. PROC-19 — Avaliar o ciclo de vida

*ACV*

**Gatilho.** Separador Ambiental, após a simulação técnica.

**Entradas**

- `tank_vol_liters`
- `annual_pluvial_m3` de PROC-12
- materiais e massas dos dois reservatórios
- comprimentos por diâmetro de tubo
- `pump_count`
- fator da rede elétrica
- fator de emissão da água potável entregue
- resultado da ETAP de PROC-15

**Regras**

1. Sete etapas: cisterna inferior, reservatório superior, tubagem, eletrobomba, operação de bombeamento, operação de tratamento e potável evitada.
2. Volume zero **sem** volume pluvial é o cenário sem sistema, e não recebe impacto fixo de caixa, tubo ou bomba.
3. A linha de tratamento **substitui** o termo de cloragem; não soma a ele. A cloragem acompanha o tratamento, e não o reservatório superior.
4. Reservatório superior só no arranjo de elevação; eletrobombas em todo arranjo com bomba; energia de PROC-16.
5. A água evitada é a **entregue**, não a produzida: as perdas de distribuição fazem com que produzir 1 m³ entregue menos de 1 m³, e um fator dado à saída da estação tem de ser convertido para o volume entregue. O utilizador indica o fator de emissão da água entregue ao edifício e o da rede elétrica local; a edição não traz valor predefinido para nenhum dos dois.
6. O período de retorno do carbono é o carbono incorporado dividido pela economia anual líquida; sem economia líquida positiva, devolve 999 anos em vez de infinito.

**Saídas**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, que é critério do multicritério
- `environmental_payback_years`
- `inventory_items`, o inventário item a item

**Exceção.** Fator sem procedência primária recebe rótulo de triagem, e o rótulo é exibido — a lacuna é declarada, não escondida.

### B.20. PROC-20 — Enquadrar nas certificações

*ESG e certificações*

**Gatilho.** Separador Ambiental e relatórios.

**Entradas**

- `potential_potable_savings_pct`
- volume pluvial e potável anuais
- repartição interno/externo de PROC-09
- CO₂ evitado no ciclo de vida
- `area`, para a área de captação da WEM14
- caso-base do EDGE, quando declarado

**Regras**

1. **LEED v4**: WEc1 até 2 pontos pelo uso externo, WEc2 até 6 pontos pelo uso interno, pela escala oficial. Sem procura externa registada, WEc1 é zero e diz porquê.
2. **LEED v5 BD+C** (rating system de novembro de 2025): WEc2 até 8 pontos, pela Opção 1 (projeto inteiro, 30% a 65%, +1 com fonte alternativa) ou pela soma das Opções 2 (louças e metais, 30% a 40%), 4 (externo, 50% e 100%) e 6 (reutilização no lote, 2 pontos), só em construção nova. SSc3 registado como não avaliado; o ponto de reutilização dele não ultrapassa o teto de 3.
3. **EDGE**: **não pontua**. Mede percentual contra um caso-base local e compara com 20%, em três barras independentes. O nível avançado sobe a barra de *energia* para 40%, e não a de água. O programa avalia só a barra de água, pela medida WEM14, e diz que as outras duas estão fora do seu alcance.
4. Sem caso-base declarado, o EDGE usa a procura modelada e avisa que o número é **piso**.
5. **GRI 303**: captação evitada e taxa de circularidade.

**Saídas**

- `credit_details`: a matriz de créditos que alimenta a tabela do ecrã e os relatórios
- `esg_summary_text`
- cartões de LEED, EDGE e GRI

**Exceção.** Procura total nula devolve zero por cento sem dividir por zero.

### B.21. PROC-21 — Ordenar volumes por múltiplos critérios

*Multicritério*

**Gatilho.** Separador Otimizador, com o varrimento pronto.

**Entradas**

- um candidato por volume do varrimento, montado por `candidato_dos_resultados` com a simulação, a análise económica, o CO₂ de ciclo de vida e a massa a seco
- quatro pesos de eixo e oito partes no eixo, ou oito pesos de critério

**Regras**

1. Oito critérios em quatro eixos. Técnico: **maximizar** fiabilidade volumétrica e eficiência de armazenamento. Económico: **maximizar** VAL; **minimizar** LCOW e período de recuperação descontado. Ambiental: **minimizar** CO₂ de ciclo de vida. Estrutural: **minimizar** massa a seco e extravasamento anual.
2. O peso de cada eixo reparte-se pelos critérios do eixo segundo as partes no eixo. Três pesos de eixo (projetos até à 0.1.0) dão ao eixo estrutural a média dos três; sete valores são recusados.
3. Quem não recupera o investimento recebe no período de recuperação o pior observado mais 10% (ao menos mais um ano e ao menos 20 anos); o volume zero recebe no LCOW o pior observado mais 10%.
4. A normalização translada por `x − min(x)` **antes** da normalização vetorial de Hwang e Yoon, para admitir VAL negativo. É variante deliberada, e precisa ser declarada como variante.
5. O SMAA-VIKOR sorteia oito pesos e devolve as probabilidades de cada volume ocupar cada posição.
6. As condições C1 e C2 de Opricovic não estão implementadas.

**Saídas**

- Ordenação dos volumes, distância ao ideal por critério, volume de compromisso

**Exceção.** Candidato único devolve ordenação trivial. Critério constante entre candidatos não contribui para a distância.

### B.22. PROC-22 — Gravar e reabrir o projeto

*Ficheiro do projeto*

**Gatilho.** Menu de guardar e de abrir.

**Entradas**

- `TritonConfig` inteiro, com os campos do apêndice A
- estado da interface
- análise corrente

**Regras**

1. Formato JSON, em secções nomeadas.
2. A leitura usa valor por defeito campo a campo, de modo que ficheiro antigo continua abrindo.
3. `created_at` e `precip_file` descrevem o ato de guardar, e não o projeto: por isso não voltam.
4. É a quinta travessia do programa — a que atravessa o **tempo** em vez dos módulos. Trinta dos 87 campos de então não sobreviviam ao ciclo, inclusive a escolha inteira da ETAP, a altura manométrica, os materiais dos reservatórios, a rega e a água de rega.

**Saídas**

- Ficheiro `.triton`
- `TritonConfig` reconstruída

**Exceção.** Secção ausente no ficheiro cai para os valores por defeito da classe. JSON inválido interrompe a abertura com mensagem.

### B.23. PROC-23 — Emitir relatórios e exportações

*Relatórios*

**Gatilho.** Separador Relatórios; separador Exportação.

**Entradas**

- resultados de PROC-12, PROC-18, PROC-19, PROC-20 e PROC-21
- dados do projeto

**Regras**

1. Três relatórios: executivo, ambiental com ESG, e científico.
2. Exportação para CAD e BIM a partir do dimensionamento.
3. Folhas de cálculo com a série diária e a varrimento.

**Saídas**

- HTML, PDF, DXF, JSON para BIM e XLSX

**Exceção.** A conversão para PDF tenta o motor do Qt e cai para o gerador alternativo quando ele não está disponível.

### B.24. PROC-24 — Automação para estudos de larga escala

*Automação*

**Gatilho.** Linha de comandos `triton`, descrita na secção 3.6 (volume Guias de uso); acompanha a instalação como pacote Python, e não o instalador de Windows.

**Entradas**

- ficheiro de projeto
- ficheiro de chuva

**Regras**

1. Chama o **mesmo** núcleo de cálculo da janela, sem ecrã.
2. Só parte dos parâmetros é alcançável por ela; os demais só existem na interface, e o caminho é montar o projeto na janela e variar por automação só o que muda entre os casos.
3. Serve a matrizes fatoriais de milhares de casos e à propagação de incerteza por sorteio, que são o instrumental dos trabalhos publicados pelo grupo.

**Saídas**

- JSON e CSV com os resultados

**Exceção.** Parâmetro fora do intervalo admitido é recusado antes de simular, com a mesma barreira de validação da interface.

---

## Apêndice C — Fatores de emissão

Todos os fatores que a avaliação de ciclo de vida usa, com a procedência, a fronteira e o grau
de confiança. A avaliação é de **triagem**, e não um inventário conforme a ISO 14040 (apêndice G).

A Edição Ibérica separa os fatores em dois tipos.

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

### C.1. Fatores a indicar pelo utilizador

<!-- tabela: **Tabela 18** — Fatores de emissão que o utilizador indica, e o que declarar em cada um -->
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

### C.2. Materiais dos reservatórios

<!-- tabela: **Tabela 19** — Fatores de emissão dos materiais dos reservatórios, com massa e fronteira -->
| Material | Massa por m³ útil | Fator | Fronteira |
| :--- | ---: | ---: | :--- |
| polietileno de alta densidade | 22 kg/m³ | 1,612 kg CO₂e/kg | berço ao portão |
| betão armado | 1 200 kg/m³ | 0,140 kg CO₂e/kg | berço ao portão |
| fibra de vidro | 15 kg/m³ | 3,250 kg CO₂e/kg | berço ao portão |
| aço inoxidável AISI 304 | 38 kg/m³ | 3,700 kg CO₂e/kg | berço ao portão |

A massa por metro cúbico útil é o que converte o volume do reservatório em massa de material. É ela, e
não o fator, que faz o betão dominar o inventário: 1 200 kg por metro cúbico contra 22 do polietileno.
As massas são cenários geométricos do programa, e não o peso de um produto.

<!-- tabela: **Tabela 20** — Referência registada no programa para cada fator de material, e a sua situação -->
| Material | Referência registada no programa | Situação |
| :--- | :--- | :--- |
| polietileno | Franklin Associates para o American Chemistry Council (outubro de 2020), *Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin*, Tabela 6: 1 612 kg CO₂e por 1 000 kg de resina (TRACI 2.1, IPCC 2013 GWP-100, âmbito dos Estados Unidos) | registada; reverificação pendente |
| betão | valor de triagem de 0,14 kg CO₂e/kg; Hammond e Jones (2008, doi:10.1680/ener.2008.161.2.87) publicam um valor para o betão, mas o valor exato adotado não está rastreado até ele | triagem, sem fonte rastreada |
| fibra de vidro | Composites UK, *Embodied carbon data for composites*: intervalo típico de 2,5 a 4,0 kg CO₂e/kg; adota-se o ponto médio | registada; reverificação pendente |
| aço inoxidável | worldstainless (World Steel Association), relatório de emissões de CO₂ de 24/09/2024, berço ao portão: 1,95 kg CO₂/kg com 85% de sucata, 2,45 com 75%, 3,70 com 50%, 6,80 com 30%; adota-se o caso de 50% de sucata | registada; reverificação pendente |

> **Consequência prática, demonstrada na secção 4.8 (volume Tutorial):** o material pode decidir o **sinal** do
> resultado ambiental. Com a chuva de Lisboa e os fatores ilustrativos do tutorial, nenhum dos quatro
> materiais paga a dívida de carbono em vinte anos; a secção conta o resultado tal como saiu.

---

### C.3. Tubagens e eletrobomba

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

### C.4. Consumíveis de tratamento

<!-- tabela: **Tabela 21** — Fatores de emissão dos consumíveis de tratamento -->
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

### C.5. Fatores com rótulo de triagem

Nem todo o parâmetro tem fonte primária, e os que não a têm são assinalados no relatório: as massas por
metro cúbico útil do polietileno, do betão e do aço inoxidável, que são cenários geométricos, o fator do
betão, o fator do hipoclorito e qualquer fator introduzido sem fonte. Os fatores que o utilizador introduz
sem fonte recebem também o rótulo de triagem. Um inventário que apresenta todos os fatores com o mesmo grau
de confiança esconde onde está a fragilidade.

---

### C.6. O que consultar antes de publicar

1. a EPD ou a ficha técnica de cada produto que especificar;
2. o separador Documentação, capítulo de avaliação de ciclo de vida, para as justificações mostradas ao utilizador;
3. o inventário do relatório ambiental, que lista cada item com o fator aplicado.

---

## Apêndice D — Regimes tarifários

A Edição Ibérica traz o tarifário doméstico de **3 concelhos**, transcrito
dos documentos das entidades gestoras: Funchal, Lisboa, Porto. Para qualquer
outro concelho, o utilizador introduz o tarifário do projeto, na janela de tarifário (etapa 5),
e o programa calcula a fatura com e sem o sistema. Este apêndice descreve a estrutura que o
programa aceita, os seis regimes que reconhece e os tarifários transcritos.

### D.1. Os códigos de escalão

Cada linha da tabela de água é uma quádrupla `(mínimo, máximo, valor, código)`, em m³ por mês
e euros por m³ (ou euros por mês nos códigos fixos).

<!-- tabela: **Tabela 22** — Os códigos da tabela tarifária de água -->
| Código | Significado |
| ---: | :--- |
| 1 ou 0 | escalão progressivo: cobrado só sobre o volume dentro dele |
| −1 | tarifa de disponibilidade: valor fixo por mês que se soma ao consumo medido |
| −2 | franquia retroativa: até à franquia paga-se o valor fixo; depois, todo o volume desde zero é cobrado pelos escalões |
| −3 | piso de pagamento: a fatura não pode ficar abaixo do valor |

O efeito de cada código na fatura está desenhado na secção 2.7 (volume O método), e não se repete aqui.

### D.2. A fatura portuguesa

Uma fatura doméstica soma, por mês, a água (tarifa fixa e escalões por m³), o saneamento de
águas residuais, os resíduos urbanos, a taxa de recursos hídricos (TRH, por m³) e o IVA de
cada parcela, **à taxa que o próprio tarifário declara**. Nenhuma taxa de IVA fica no código.
O programa trata cada parcela assim:

<!-- tabela: **Tabela 23** — Como o programa guarda cada parcela da fatura portuguesa -->
| Parcela | Como entra no projeto |
| :--- | :--- |
| água | escalões em `water_tariffs`; o IVA da água em `water_tax_var` |
| saneamento por escalões | modo 3 do saneamento, sobre o volume recolhido (coeficiente de recolha × volume de água); a TRH e o IVA entram no preço de cada escalão |
| saneamento ou resíduos por m³ | modo 2 do saneamento, com um preço único por m³ de água, IVA incluído |
| tarifas fixas das outras parcelas | taxa fixa mensal (`water_tax_fixed`), com IVA |

Os resíduos por escalões (como no Funchal) ainda não têm campo próprio: a parte variável soma-se
à do saneamento, e só a parte fixa fica numa parcela à parte. A atualização tarifária é
introduzida em separado para a água, o saneamento e a energia (apêndice A).

### D.3. As quatro formas do saneamento

<!-- tabela: **Tabela 24** — As quatro formas de introduzir o saneamento -->
| Modo | O saneamento é |
| ---: | :--- |
| 0 | um valor fixo |
| 1 | uma percentagem da parcela de água (e não da fatura toda) |
| 2 | um valor por m³ consumido |
| 3 | escalões, aplicados a uma fração do volume de água que o utilizador declara |

### D.4. Os seis regimes

O programa classifica uma tabela de água num de seis regimes. O regime diz quanto vale poupar
água, que é o que um estudo de aproveitamento de água de chuva precisa de ver.

<!-- tabela: **Tabela 25** — Os seis regimes tarifários e o que acontece ao poupar -->
| Regime | Estrutura | O que acontece ao poupar |
| :--- | :--- | :--- |
| **Sem mínimo** | Só escalões progressivos. | Cada m³ poupado reduz a fatura. |
| **Tarifa de disponibilidade** | Um valor fixo que **soma** ao consumo medido. | Cada m³ poupado reduz a fatura; a parte fixa mantém-se. É a estrutura dos três tarifários transcritos. |
| **Franquia no mínimo** | O valor fixo já inclui um volume. | Poupar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | Até à franquia paga-se o valor fixo; passando-a, **tudo desde zero** é cobrado pelos escalões. | Ao passar a franquia, todo o volume é faturado desde zero. |
| **Piso de pagamento** | A fatura **não fica** abaixo do piso. | Não soma: limita. A poupança que leve a fatura abaixo do piso não rende nada. |
| **Fórmula exponencial** | Serviço básico mais `PB × Cⁿ`, com o expoente `n` dado pelo consumo do mês. | Cada m³ poupado reduz a fatura, mas não a um preço fixo por m³. |

**Teste rápido.** Simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os
com uma fatura real. Se só um coincidir, o regime está errado. A secção 3.3 (volume Guias de uso) ensina o
teste que identifica uma estrutura errada.

### D.5. Os tarifários transcritos

Os valores abaixo são os impressos nos documentos das entidades gestoras, transcritos em
`triton/data/portugal_tarifarios.json` e recolhidos em 07/10/2026. São exemplos fiéis de
como se introduz um tarifário, e não um catálogo: os tarifários mudam todos os anos, e é
preciso verificar o documento em vigor da sua entidade gestora antes de qualquer conclusão
económica. Os três têm a estrutura da tarifa de disponibilidade com escalões progressivos.

<!-- tabela: **Tabela 26** — Preço por escalão de consumo mensal (€/m³, sem IVA), por concelho e serviço -->
| Concelho | Serviço | 0–5 | 5–15 | 15–25 | 25–50 | mais de 50 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Funchal | água | 0,39 | 0,69 | 1,28 | 2,87 | 5,02 |
| Funchal | saneamento | 0,00 | 0,55 | 1,01 | 1,01 | 1,01 |
| Lisboa | água | 0,4634 | 0,8666 | 2,0398 | 2,5961 | 2,5961 |
| Lisboa | saneamento | 0,2198 | 0,5787 | 1,3621 | 1,7165 | 1,7165 |
| Porto | água | 0,4945 | 0,9649 | 1,7657 | 3,0016 | 3,0016 |
| Porto | saneamento | 0,3875 | 0,7606 | 1,4608 | 2,4423 | 2,4423 |

#### D.5.1. Funchal: Câmara Municipal do Funchal

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 15 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Câmara Municipal do Funchal, Tabela de Taxas e Outras Receitas Municipais 2026
  Endereço: https://cmfdoc.funchal.pt/media/k2/attachments/Tabela_de_Taxas_Municipais_2026_.pdf (entregue pelo autor); SHA-256 `97084c0265bfcb75c75e7b9e2d95aebab3417973f3cd0964b34696d3eea76f87`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 27** — Estrutura do tarifário do Funchal -->
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

<!-- tabela: **Tabela 28** — Contas mensais de conferência do tarifário do Funchal -->
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

#### D.5.2. Lisboa: EPAL (água); Câmara Municipal de Lisboa (saneamento e resíduos urbanos)

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- EPAL, Preços de venda de água, 1.ª edição 2026
  Endereço: https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0; SHA-256 `d0ebc13e306944db42fc96b57544ade72625478e99b5b0dc26d81fc6f0b5f42d`; recolhido em 07/10/2026.
- CML, Tarifário do saneamento 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf (entregue pelo autor); SHA-256 `6c6295d9e5da3d09a7cd5476abe242757edd761b137359d5a4b561d1f080c37a`; recolhido em 07/10/2026.
- CML, Tarifário dos resíduos urbanos 2026, Regulamento CML n.º 569-A/2014
  Endereço: https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf (entregue pelo autor); SHA-256 `7fa873127affb4e33306166292c9da937f0d68b39987a97ead767a866e32e54f`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 29** — Estrutura do tarifário de Lisboa -->
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

<!-- tabela: **Tabela 30** — Contas mensais de conferência do tarifário de Lisboa -->
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

#### D.5.3. Porto: Águas e Energia do Porto, EM

Vigência a partir de 01/01/2026. Utilizador doméstico, tarifário geral, contador até 25 mm, meses de 30 dias.

Documentos usados (o endereço de origem e a impressão digital SHA-256 de cada um estão registados em `tarifas_portugal/fontes/FONTES.tsv`):

- Águas e Energia do Porto, Tarifário Geral 2026
  Endereço: https://www.aguasdoporto.pt/files/uploads/cms/Tarif%C3%A1rio%20Geral%202026.pdf; SHA-256 `7d6b5d0ceeef749d558018b4b1b24e661f3a415a1d55cab09f0de7aae340e0de`; recolhido em 07/10/2026.

<!-- tabela: **Tabela 31** — Estrutura do tarifário do Porto -->
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

<!-- tabela: **Tabela 32** — Contas mensais de conferência do tarifário do Porto -->
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

#### D.5.4. Eletricidade

O Funchal leva ainda a tarifa de eletricidade, para o custo de bombagem: tarifa Base da
Empresa de Eletricidade da Madeira, 6,90 kVA, 0,1673 €/kWh sem IVA. A fonte é um comparador
(luzegas.pt, atualizado em 20/02/2025), **secundária**: confirme na EEM ou na ERSE. Lisboa e
Porto não têm tarifa de eletricidade registada, e o custo de bombagem fica a zero até o
utilizador introduzir a sua.

### D.6. Documentos recolhidos e ainda não transcritos

Os documentos abaixo estão arquivados com o endereço de origem e a impressão digital, mas
ainda não foram transcritos para o programa, que por isso não os oferece. Neles, introduza o
tarifário à mão. O tarifário de Bragança, em vigor, continua por obter.

<!-- tabela: **Tabela 33** — Concelhos com documento tarifário recolhido e ainda por transcrever -->
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

### D.7. Confiança dos valores tarifários por concelho

Nem todos os tarifários valem o mesmo. O Triton IBE traz transcritos 3 dos 280 concelhos que cobre (278 de Portugal continental, mais Funchal e Ponta Delgada), e para os restantes o utilizador introduz o tarifário do projeto. Para cada concelho, e para cada um dos três serviços (água, saneamento e resíduos urbanos), o programa de manutenção atribui um de três estados, com o motivo escrito.

Em Portugal a água, o saneamento de águas residuais e os resíduos urbanos são muitas vezes de entidades diferentes (em Lisboa, a EPAL fornece a água e a Câmara trata do saneamento e dos resíduos; no Porto, a Águas e Energia do Porto trata da água e do saneamento, e a EMAP dos resíduos). Por isso o estado é dado por serviço, cada um com a sua entidade e o seu documento. O saneamento cobra-se por escalões sobre uma fração do volume de água, o IVA vem de cada documento, a taxa de recursos hídricos (TRH) é uma parcela própria e a tarifa fixa depende do calibre do contador. Só se avalia o utilizador doméstico.

#### D.7.1. A escala e os critérios

<!-- tabela: **Tabela 34** — Estados de confiança dos valores tarifários e respetivos critérios -->
| Estado | Critério |
| :--- | :--- |
| 🟢 verde, verificado | Documento oficial arquivado com URL e SHA-256; `confirmado_em` há menos de 12 meses; transcrição conferida com as contas impressas; verificação independente registada em `verificado_por` (fatura real com tolerância de ±0,05 €, ou segunda leitura por uma pessoa diferente do transcritor; um modelo de IA nunca conta); e nenhuma pendência com efeito acima de 1 % na conta de 10 m³. |
| 🟡 amarelo, a validar | Há documento oficial arquivado ou transcrito, mas falta algum dos requisitos do verde: transcrição, conferência, reconfirmação nos últimos 12 meses, verificação independente, ou há pendência com efeito acima de 1 %. |
| ⚪ cinza, sem dado | Sem documento oficial arquivado, entidade gestora por identificar, ou dado ruim. O programa não traz tarifário e a ficha da ERSAR indica onde o procurar. |

O estado do concelho é verde quando os três serviços são verdes, cinza quando são todos cinza, e amarelo nos restantes casos. **Não há verde sem verificação independente**: a transcrição feita por quem leu o documento prova a aritmética, não a leitura. Uma **pendência** é uma hipótese que o documento não resolve (o IVA aplicado, um valor que não vem impresso, a leitura de uma tabela); cada uma traz o efeito estimado na conta de 10 m³ e, acima de 1 %, impede o verde.

#### D.7.2. Situação em 23/10/2026

<!-- tabela: **Tabela 35** — Concelhos e serviços por estado de confiança dos valores tarifários -->
| Estado | Concelhos | Água | Saneamento | Resíduos |
| :--- | ---: | ---: | ---: | ---: |
| 🟢 verde, verificado | 0 | 0 | 0 | 0 |
| 🟡 amarelo, a validar | 42 | 42 | 42 | 11 |
| ⚪ cinza, sem dado | 238 | 238 | 238 | 269 |
| **total** | **280** | **280** | **280** | **280** |

Por distrito (e região autónoma), com o estado do concelho:

<!-- tabela: **Tabela 36** — Concelhos por distrito e estado de confiança dos valores tarifários -->
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

<!-- tabela: **Tabela 37** — Concelhos com tarifário transcrito e o estado de cada serviço -->
| Concelho | Água | Saneamento | Resíduos | O que falta |
| :--- | :--- | :--- | :--- | :--- |
| Funchal | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); pendência (efeito não quantificável): a tabela não diz se o preço do escalão atingido vale por faixa ou para todo o volume; água: pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; saneamento: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero; pendência (efeito de 2,30 % na conta): Taxa de Recursos Hídricos não impressa no documento (tratada como zero); ordem de grandeza: a TRH da água do Porto, 0,0392 €/m³, pesaria cerca de 2,3 % na conta de 10 m³; resíduos: pendência (efeito não quantificável): o 1.º escalão (0 a 5 m³) do saneamento e dos resíduos não tem valor impresso e foi tratado como zero |
| Lisboa | 🟡 | 🟡 | 🟡 | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); saneamento: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 %; resíduos: pendência (efeito de 2,59 % na conta): IVA do saneamento e dos resíduos tratado como 0 % (os documentos não cobram IVA; posição contestada pela Provedora de Justiça); com 6 % a conta de 10 m³ sobe 2,59 % |
| Porto | 🟡 | 🟡 | ⚪ | em todos os serviços com documento: sem verificação independente (fatura real ±0,05 € ou segunda leitura por outra pessoa); água: pendência (efeito de 1,96 % na conta): tarifa de disponibilidade da água lida por inferência do layout (0,1242 €/dia; a outra leitura, 0,1367 €/dia, subiria a conta de 10 m³ 1,96 %); resíduos: entidade EMAP: sem documento arquivado |

#### D.7.3. Como ler o estado

1. Procure o concelho do projeto. A entidade gestora de cada serviço vem da ficha tarifária da ERSAR (e, no Funchal e em Ponta Delgada, do próprio documento); quando nenhuma fonte a indica, a tabela diz «a identificar».
2. Leia o estado de cada serviço, não só o do concelho: um concelho amarelo pode ter a água documentada e os resíduos sem dado.
3. Leia «o que falta». É a lista do que o utilizador deve verificar antes de apoiar uma conclusão económica.
4. Confira a vigência. Os tarifários portugueses mudam em regra todos os anos, em janeiro ou nos primeiros meses, e um tarifário com mais de 12 meses pode já ter sido substituído.

#### D.7.4. O que fazer em concelhos amarelos e cinzentos

- **Cinza.** Obtenha o tarifário em vigor da entidade gestora de cada serviço (a ficha da ERSAR indica a entidade e o ano), introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5) e confira a fatura que o programa calcula com uma fatura real do edifício.
- **Amarelo.** O valor tem documento oficial por trás, mas não foi verificado de modo independente. Confira a conta com uma fatura real e, se o programa lhe der um valor diferente por mais de 0,05 €, use o da fatura.
- **Em qualquer estado diferente de verde.** Declare no estudo a entidade gestora, a data de vigência e o estado de confiança, e acompanhe o resultado económico de uma análise de sensibilidade à tarifa.

### D.8. Introduzir o seu tarifário

1. Obtenha o documento tarifário em vigor da sua entidade gestora e anote a data.
2. Introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário (etapa 5).
3. Confira a fatura que o programa calcula com uma fatura real do edifício.
4. Declare no estudo a entidade gestora, a data de vigência, o regime e a moeda.

---

## Apêndice E — Base climática

> **Desde 30/10/2026 a fonte primária da Edição Ibérica é o Iberia01** (Península e Baleares, 8 319 municípios, 1971–2015, ODbL; Canárias, Madeira e Açores pela ERA5, nível C), em ficheiros separados do programa; ver `docs/DADOS.md` (§2A). O que se segue descreve a base E-OBS, que continua como fonte opcional e não comercial.
>
> **A Edição Ibérica traz duas bases de chuva.** O Iberia01 (fonte por defeito) vem em `data/chuva_iberia01_p1.db` a `p4.db`, com `data/ibe_unidades.db`, e a E-OBS opcional em `data/portugal_eobs.db`. Canárias, Madeira e Açores usam a ERA5 de 0,25° (`data/chuva_ilhas_era5.db`, nível C); Ceuta e Melilla ficam sem série, e a série é um ficheiro do utilizador (secção 4.1 (volume Tutorial)). O exemplo do Funchal usa a ERA5 de ilha.

---

### E.1. O que a base contém

<!-- tabela: **Tabela 38** — Conteúdo da base de precipitação por concelho da Edição Ibérica -->
| O que a base traz | Valor |
| :--- | :--- |
| fonte | E-OBS v33.0e, precipitação diária (RR), média do conjunto, grelha regular de 0,1° |
| período | 01/01/1950 a 31/12/2025 (27 759 dias) |
| concelhos com série | 278, todos no Continente, em 18 distritos |
| concelhos sem série | 30: os 19 dos Açores e os 11 da Madeira |
| limites dos concelhos | CAOP2025, Direção-Geral do Território (Aviso n.º 3502/2026/2, DR, 2.ª série, n.º 34, 18/02/2026) |
| formato | base SQLite (`portugal_eobs.db`), uma série comprimida por concelho |

**Como se obtém a série de um concelho.** É a média diária das células da grelha cujo centro cai dentro do
limite do concelho. Num concelho pequeno, sem nenhum centro de célula dentro do limite, usa-se a célula mais
próxima do centroide. Um dia sem dado em todas as células do concelho fica como falha (NaN), e a simulação
recusa a série, em vez de a tratar como dia seco. A grelha tem cerca de 10 km: a série de um concelho é uma
média de área, e suaviza as chuvadas intensas.

**Que concelhos ficam de fora, e porquê.** Os Açores situam-se a oeste de 25° W, fora do domínio da E-OBS.
Na Madeira, a E-OBS só tem a célula das estações que funcionavam em cada ano, e todos os concelhos faltam em
mais de 1% dos dias de 1991 a 2020 (o Funchal, em 22%). O critério da base é rejeitar o concelho com mais de
1% de dias sem dado nessa normal. Nenhum concelho recebe a série de um vizinho.

**Citação exigida pela fonte.** Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D.
(2018). An Ensemble Version of the E-OBS Temperature and Precipitation Data Sets. *Journal of Geophysical
Research: Atmospheres*, 123(17), 9391-9409. doi:10.1029/2017JD028200. Reconhecimento: *We acknowledge the E-OBS
dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the Copernicus Climate Change Service, and the
data providers in the ECA&D project (https://www.ecad.eu).*

**Recortes.** A normal climatológica de 1991 a 2020 é o recorte inicial. O programa oferece ainda as normais
de 1981-2010, 1971-2000 e 1961-1990 e o período dos últimos trinta anos (1996-2025); as janelas de estudo
são recortes livres da série.

---

### E.2. Quanto confiar na série da E-OBS

Comparámos a E-OBS (versão 33.0e) com o Iberia01, uma grelha de 0,1° feita com uma rede de 3 486 estações
da Península (AEMET, IPMA e APA), entre 1971 e 2000, célula a célula e dia a dia. Resultado:

- Em Portugal, a E-OBS dá em média 8% menos chuva que o Iberia01 (nos 10% de células mais afastadas, até 18%
  menos). Na Espanha, entre 10% e 16% menos.
- Os extremos saem alisados: o percentil 95 dos dias de chuva fica cerca de 9% abaixo em Portugal, e o máximo
  diário anual, 14% abaixo. Isto tende a subestimar o extravasamento de um reservatório.
- O calendário dos dias é bom (correlação diária mediana de 0,86 em Portugal).

Em três estações do GHCN-Daily que a E-OBS não usa (Faro, Évora e Castelo Branco), a E-OBS deu 19% a 22%
menos chuva. São poucas estações, por isso este resultado é preliminar. O Iberia01 termina em 2015 e os seus
autores avisam que não serve para análise de tendência histórica; por isso este manual não afirma nenhuma
tendência de longo prazo da chuva.

**Nível de qualidade por concelho.** O programa mostra um nível, A, B ou C, e o motivo. O nível é o pior de
duas medidas. *Concordância com o Iberia01*: A se a diferença do total anual é de 10% ou menos e a do máximo
diário anual de 15% ou menos; B se são de 20% e 25% ou menos; C no resto. Falamos de «diferença para o
Iberia01», e não de «viés»: o Iberia01 é também uma grelha interpolada, não uma medição. *Geometria*: só
rebaixa até B, quando o concelho tem menos de três células, quando nenhuma célula tem o centro lá dentro ou
quando a série é igual à de outro concelho.

<!-- tabela: **Tabela 39** — Concelhos de Portugal continental por nível de qualidade da chuva -->
| Nível | Concelhos | O que significa |
| :--- | ---: | :--- |
| A | 45 | três células ou mais e boa concordância com o Iberia01 |
| B | 159 | concordância razoável, ou poucas células |
| C | 74 | diferença grande para o Iberia01 |

Para 148 concelhos a geometria é o motivo de ficarem fora de A (menos de três células). O Algarve tem 15
dos 16 concelhos em C, e Braga, Vila Real e Santarém mais de metade. O nível não é uma nota de exatidão: diz
onde a base é mais frágil. Em C, valide com uma série local.

**E em Espanha?** A base ibérica traz 8 131 municípios de Espanha (8 041 pelo Iberia01, incluindo as 67 das Baleares; 88 das Canárias pela ERA5; Ceuta e Melilla sem série), com o limite municipal do Eurostat/GISCO (LAU 2023) e o código INE de cinco dígitos. O nível é geométrico (sem a E-OBS como referência): na Península e nas Baleares, A 321, B 7 719 e C 1; as ilhas são C. É a representação do município pela grelha, e não uma validação com pluviómetros. O ensaio que as 52 capitais de província tiveram antes desta base (feito fora do programa, com a E-OBS) já não vale como nível de nenhum município.

**Correção de escala: não incluída.** Estudou-se uma correção mensal do total, calibrada com o Iberia01 em
1971–2000 (o período de referência que os autores recomendam), mas **ela não faz parte desta versão**: o
pacote não traz nem o código nem o ficheiro dos fatores. Se vier a ser distribuída, os fatores irão num ficheiro
separado, sob a Open Database License do Iberia01, e ficará desligada por defeito. Até lá, nos concelhos de
nível C, valide a série com uma série local ou carregue a sua.

**Uso comercial.** O Iberia01 (ODbL) e a ERA5 (CC BY 4.0) permitem o uso comercial, com atribuição, que o rodapé do laudo leva (Herrera et al., 2019, doi:10.5194/essd-11-1947-2019). A E-OBS, opcional, é de uso estritamente não comercial em pesquisa e educação: só o projeto cuja fonte é a E-OBS mostra o aviso vermelho, e o laudo repete a licença e a citação.

**Reprodutibilidade.** Cada projeto grava o município (`Nome [código]`), a fonte e o SHA-256 da série; com a E-OBS, grava também o identificador do pacote (`PT-EOBS-v33.0e-37fcba20`), a
versão da E-OBS e o SHA-256 do pacote, e por defeito leva a série dentro do ficheiro. Se reabrir um projeto
com um pacote diferente, o programa avisa e o laudo regista a mudança.

**Cobertura.** O ecrã inicial, o título da janela e o rodapé dos laudos mostram uma linha lida da base: «Cobertura: Portugal 308 locais, Espanha 8131 locais; chuva Iberia01 8319, ERA5 (nível C) 118, sem série 2». Com a E-OBS escolhida, a linha é a da E-OBS (278 concelhos do Continente: A 45, B 159, C 74).

---

### E.3. A série que vem como ficheiro

Uma série diária acompanha o programa na pasta `data/rainfall`. É uma **reanálise**, e não um registo de
udómetro.

<!-- tabela: **Tabela 40** — Série de precipitação distribuída com a Edição Ibérica -->
| Ficheiro | Local | Período | Dias | Chuva média anual | Fonte |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `Funchal.csv` | Funchal (32,65° N, 16,90° O, célula de grelha a 323 m de altitude) | 01/01/1991 a 31/12/2020 | 10 958 | cerca de 538 mm | reanálise ERA5, via Open-Meteo (série de exemplo da edição; o projeto de exemplo do Funchal usa a mesma ERA5 pela base das ilhas, 1986–2015, 531 mm) |

O formato é um valor por linha: a precipitação diária em milímetros, sem data. A data do primeiro dia vem
do projeto (1 de janeiro de 1991 neste ficheiro).

**O que é.** A ERA5 é a reanálise global de quinta geração do Centro Europeu de Previsões Meteorológicas de
Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas (Hersbach et al., 2020,
*Quarterly Journal of the Royal Meteorological Society*, 146, 1999-2049). A série foi extraída para uma
célula de grelha de cerca de 9 km, pela interface de arquivo da Open-Meteo.com (licença CC BY 4.0), em
14/10/2026. Uma célula é uma média de área: suaviza as chuvadas intensas e exagera o número de dias de
chuva fraca, e por isso é um ponto de partida, e não um substituto de um registo medido.

**Porque o Funchal usa a ERA5.** O Funchal está fora do domínio do Iberia01, e a E-OBS não serve (22% de dias sem dado em 1991-2020, acima do
limite de 1%). A média anual da reanálise pode diferir da média medida na estação. Num projeto real,
use a série medida.

**Os projetos de exemplo.** Lisboa, Porto, Madrid e Palma usam o Iberia01 (normal 1986–2015), e o Funchal a ERA5 de ilha (nível C); em todos, o ficheiro do projeto guarda o município pelo código (`Lisboa [PT-1106]`), a referência da série e a impressão digital dos valores, e o programa recompõe a série da base ao abrir. Nenhum exemplo usa a E-OBS, e por isso nenhum leva o aviso vermelho de uso não comercial. Medido no mesmo período de 1991 a 2015, o Iberia01 dá 0,4% mais chuva do que a E-OBS em Lisboa e 2,4% mais no Porto; a normal 1991–2020 da E-OBS, que os exemplos usavam antes, dava 719 mm em Lisboa e 1 199 mm no Porto, contra 746 mm e 1 197 mm do Iberia01 em 1986–2015.

---

### E.4. Usar a sua própria série

1. Obtenha um registo diário, em milímetros, do serviço meteorológico ou do udómetro mais próximo do local.
   Anote a estação, a distância ao local, o período e a fonte.
2. Guarde-o num CSV com um valor por dia. Aceita-se o ponto ou a vírgula como separador decimal, e uma linha
   de cabeçalho é ignorada.
3. Abra-o na etapa 1 (Projeto e chuva) e indique a data do primeiro dia.

Um ano incompleto é descartado na leitura, para não enviesar os totais anuais. Exigem-se dados diários: as
médias mensais escondem os períodos secos que decidem o volume (secção 5.1.2 (volume Enganos, limitações e confiabilidade)).

**Que extensão de série.** A extensão necessária para estabilizar o volume ideal não é uma constante
geográfica: cresce com a fração atendível e com a procura do edifício (glossário, apêndice G). A série
de cada concelho da base tem trinta anos na normal 1991-2020.

---

### E.5. Cenários futuros

A Edição Ibérica não traz projeções de modelos climáticos. Para estudar um clima futuro, prepare a série
diária projetada, a partir da fonte que escolher, e carregue-a como qualquer outro ficheiro. O fator de chuva
da modulação probabilística (secção 7.1 (volume Modulação probabilística)) permite testar uma série mais seca ou mais húmida por uma
percentagem declarada. A secção 3.2 (volume Guias de uso) trata da condução do estudo.

---

### E.6. O que declarar num estudo

- a **fonte** da série (E-OBS v33.0e, estação ou produto de reanálise) e a sua versão;
- o **local**: o concelho da base, ou, para um udómetro, a distância ao local;
- o **período**, com o primeiro e o último ano;
- se a série foi **corrigida, preenchida ou regionalizada**, e como;
- para uma projeção, o modelo, o cenário e a janela, e o método de correção do enviesamento;
- o número de **anos** de dados;
- a citação e o reconhecimento exigidos pela E-OBS, e, para a ERA5, a atribuição à Open-Meteo.


---

### E.7. Particularidades de região e país

A Edição Ibérica chama-se assim porque foi desenhada para a Península Ibérica: a chuva cobre **Portugal e Espanha**, e os tarifários de Portugal (três concelhos transcritos) e de Espanha (média regional do INE para todos os municípios; sete com tarifa transcrita ainda não conferida). Esta secção diz o que existe, o que falta e o que é próprio de cada país. Os números vêm de `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e tamanho.

<!-- tabela: **Tabela 41** — Cobertura geográfica da Edição Ibérica nesta versão -->
| Território | Chuva no programa | Tarifário no programa |
| :--- | :--- | :--- |
| Portugal continental | 278 concelhos, Iberia01 de 1971 a 2015 (padrão 1986–2015), com nível de qualidade A, B ou C; a E-OBS é opcional | Lisboa e Porto transcritos; os restantes concelhos digitados pelo utilizador |
| Madeira (11 concelhos) | ERA5 de 0,25°, nível C, com aviso | Funchal transcrito |
| Açores (19 concelhos) | ERA5 de 0,25°, nível C, com aviso | nenhum transcrito (Ponta Delgada consta do registo de entidades) |
| Espanha | 8 131 municípios: 8 041 pelo Iberia01 (incluindo as Baleares), 88 das Canárias pela ERA5 (nível C); Ceuta e Melilla sem série | média regional do INE (indicativa); sete municípios com tarifa transcrita ainda não conferida |

**Portugal continental.** Os 278 concelhos têm uma série diária de chuva, calculada a partir da grelha do Iberia01 de 0,1° (cerca de 10 km) ou, em alternativa, da E-OBS; a série de um concelho é uma média de área e suaviza as chuvadas intensas. Cada concelho traz um nível de qualidade (A, B ou C), explicado na secção anterior e resumido abaixo.

**Ilhas.** A Madeira, os Açores e as Canárias não entram pela grelha do Iberia01 (nem a Madeira pela E-OBS: todos os concelhos faltam em mais de 1% dos dias de 1991 a 2020). Usam a reanálise ERA5 de 0,25°, sempre em nível C e com aviso no ecrã e nos laudos; para um projeto real, use a série da estação. O exemplo do Funchal mostra o caso.

**Espanha.** A chuva vem do Iberia01 por município (limites LAU 2023 do Eurostat/GISCO, código INE). Os custos de Espanha não existem, e as tarifas são a média regional do INE (camada 3, só indicativa) ou, em sete municípios (entre eles Madrid), uma tarifa transcrita de documento oficial, ainda não conferida: o laudo diz «Tarifa transcrita, ainda não conferida (segunda leitura pendente)». Os exemplos `examples/espanha/madrid.triton` e `palma.triton` mostram os dois casos.

**Licença da chuva.** O Iberia01 é ODbL (uso comercial permitido, com atribuição). A E-OBS e o ECA&D são de uso estritamente não comercial, em investigação e educação. A licença não trata da redistribuição nem de produtos derivados (nenhum pedido foi feito ao KNMI). No primeiro arranque o programa mostra o aviso e pede o uso pretendido; a declaração fica registada nos laudos. Por defeito, o programa não bloqueia a E-OBS em uso comercial. Num uso comercial, carregue a sua série. O texto do aviso ainda precisa de revisão pela UFSC.

**Níveis de qualidade da chuva.** O nível é o pior de duas medidas: a diferença entre a E-OBS e o Iberia01 (total anual e máximo diário anual, em 1971–2000) e a geometria da série (poucas células, método do centroide ou série repetida de outro concelho). Nos 278 concelhos, 45 são A, 159 são B e 74 são C. A diferença média do total anual, sobre os 278 concelhos, é de −10,1% (a E-OBS dá menos chuva; o −8% da secção anterior é a média célula a célula em Portugal): −3,1% em A, −7,1% em B e −20,7% em C. Os C concentram-se no distrito de Faro (15 dos 16 concelhos), em Santarém (11), Braga (10), Vila Real (8) e Porto (7). O nível não é uma nota de exatidão: diz onde a base é mais frágil, e em C convém validar com uma série local.

**Tarifários e entidades gestoras.** Em Portugal, a fatura soma três serviços, cada um com a sua entidade gestora e o seu tarifário: água, saneamento e resíduos urbanos. A ERSAR, a entidade reguladora, publica a ficha tarifária por concelho; o programa usa-a para indicar a entidade de cada serviço em 280 concelhos (os 278 do Continente, mais o Funchal e Ponta Delgada), com 316 entidades. Só Lisboa, Porto e Funchal têm o tarifário transcrito (vigência de 01/01/2026); nos restantes, o utilizador digita-o, e a ficha da ERSAR indica onde o procurar (apêndice D).

**Confiança tarifária.** Cada concelho e cada serviço tem um estado: verde (documento arquivado com endereço e SHA-256, reconfirmado há menos de 12 meses, transcrição conferida e verificação independente), amarelo (há documento, mas falta algum requisito do verde) ou cinzento (sem documento, entidade por identificar ou dado ruim). Em 23/10/2026: **0 verdes**, 42 amarelos e 238 cinzentos na água e no saneamento (nos resíduos, 11 amarelos e 269 cinzentos). Nenhum concelho é verde porque nenhuma verificação independente está registada, o que não quer dizer que os valores de Lisboa, Porto e Funchal estejam errados: foram conferidos à mão com as faturas impressas nos documentos.

**Normas e entidades de referência.** A norma europeia de referência é a EN 16941-1 (sistemas de água não potável no local), e em Portugal a especificação técnica ETA 0701 da ANQIP trata o aproveitamento de águas pluviais em edifícios; a secção 1.1 (volume Comece aqui) e a secção 4.6 (volume Tutorial) dizem o que o manual verificou de cada uma. As referências a rever antes de citar estão marcadas nessas secções: a edição da EN 16941-1 em vigor e a sua transposição para a norma portuguesa, e a revisão em vigor da ETA 0701. O programa não avalia a conformidade com nenhuma delas.

**Moeda e IVA.** Os valores são em euros. A taxa de IVA depende do serviço e da entidade, e o programa trata-a em cada tarifário transcrito: no Funchal, o IVA de 4% não está confirmado, e em Lisboa o adicional da Câmara e o saneamento e os resíduos foram tratados sem IVA, como declara o tarifário.

**Fator de emissão da rede.** A edição não traz série oficial: o fator é zero até o utilizador indicar o da rede do projeto. As fontes portuguesas e espanholas avaliadas (APA, MITECO, REE) não estão incorporadas.

---

### E.8. Descrição dos dados e sua qualidade

Esta secção resume os dados que a edição traz. O inventário completo, com tamanhos, endereços das fontes, licenças e o modo de reproduzir cada item, está em `docs/DADOS.md` do repositório, e os números abaixo são os de lá. Nenhum ficheiro rastreado do repositório passa de 50 MiB; o maior ficheiro de dados é `data/chuva_iberia01_p1.db`, com 15,19 MiB.

<!-- tabela: **Tabela 42** — Os conjuntos de dados da Edição Ibérica, a fonte e a licença -->
| Conjunto | O que é | Fonte e licença |
| :--- | :--- | :--- |
| Chuva por município (fonte por defeito) | quatro partes `chuva_iberia01_p1.db` a `p4.db` (13 a 15 MiB cada), `ibe_unidades.db` (3,3 MiB) e `chuva_ilhas_era5.db` (0,33 MiB): 6 523 células do Iberia01, de 01/01/1971 a 31/12/2015, e 41 nós ERA5 das ilhas | Iberia01 v1.0 (Herrera et al., 2019): ODbL 1.0, com atribuição; limites da CAOP 2025 (Portugal) e do Eurostat/GISCO LAU 2023 (Espanha); ERA5 (Copernicus, via Open-Meteo): CC BY 4.0 |
| Chuva por concelho (opcional) | base SQLite `portugal_eobs.db` (5,74 MiB): 278 séries diárias, de 01/01/1950 a 31/12/2025 (27 759 dias) | E-OBS v33.0e (ECA&D / Copernicus): só uso não comercial em investigação e educação; limites dos concelhos da CAOP 2025 (Direção-Geral do Território, cc-by) |
| Série de exemplo do Funchal | `data/rainfall/Funchal.csv` (0,04 MiB), 10 958 dias, de 01/01/1991 a 31/12/2020 | reanálise ERA5 via Open-Meteo; CC BY 4.0 |
| Tarifários transcritos | Lisboa, Porto e Funchal (`portugal_tarifarios.json`) | documentos oficiais das entidades, com endereço e SHA-256 registados |
| Entidade gestora, confiança e proveniência | 280 concelhos (`tarifas_portugal/`, 0,75 MiB) | índice da ERSAR (avisos legais: citar a fonte, sem licença aberta) |
| Fatores de emissão, custos e rotas de produção de água | ficheiros do núcleo (0,02 MiB) | do projeto; sem valor local |

**Chuva: o que a base é.** O pacote é identificado por `PT-EOBS-v33.0e-37fcba20`, com o SHA-256 da E-OBS, da CAOP e do próprio pacote nos metadados da base, e cada projeto grava esse identificador. Nos 278 concelhos da base não há nenhum dia em falta; o critério de entrada é rejeitar o concelho com mais de 1% de dias sem dado em 1991–2020. A média anual vai de 485 mm (num concelho do distrito de Faro) a 1994 mm (no distrito de Viana do Castelo), e a média dos concelhos é de 908 mm. Setenta e um concelhos têm uma só célula, 20 usam a célula mais próxima do centroide e 14 repetem a série de outro concelho.

**Chuva: o que a base não é.** A E-OBS é um produto interpolado, e não um registo de pluviómetro. Comparada com o Iberia01 (uma grelha feita com uma rede mais densa de estações) em 1971–2000, dá menos chuva e alisa os extremos; por isso o manual não afirma nenhuma tendência de longo prazo da chuva. O Iberia01 só serve aqui de referência para o nível de qualidade (licença ODbL; a tabela `qualidade` guarda diferenças percentuais agregadas derivadas dele, e ainda não está decidido se isso exige a ODbL). No Funchal, a reanálise ERA5 tem uma média anual de cerca de 538 mm, que pode diferir da medida na estação.

**Chuva do Iberia01.** A E-OBS dá em média 13,3% menos chuva do que o Iberia01 na Península (8% em Portugal) em 1971–2015, e o autor do Iberia01 recomenda 1971–2000 como referência e desaconselha a análise de tendências. O nível de qualidade do Iberia01 descreve a representação espacial do município pela grelha (A: três ou mais células; B: uma ou duas; C: célula emprestada ou ERA5), e não uma validação com pluviómetros.

**Tarifas: o que há.** O programa lê só o tarifário transcrito de Lisboa, Porto e Funchal. Os documentos oficiais em que ele se baseia (cada um com endereço de origem e SHA-256 em `tarifas_portugal/fontes/FONTES.tsv`, recolhidos em 07/10/2026) não se redistribuem: o Git leva só o registo e os valores transcritos. As pendências de cada tarifário estão em `examples/LEIA.md`; entre elas, o IVA do Funchal, a leitura por inferência da disponibilidade de água no Porto e a vigência de mais de 12 meses de Beja, Évora, Ponta Delgada e Bragança.

**Eletricidade.** Só o exemplo do Funchal traz tarifa: 0,1673 €/kWh (Empresa de Eletricidade da Madeira, sem IVA), de uma fonte secundária (um comparador de preços, atualizado em 20/02/2025), a confirmar na EEM ou na ERSE.

**Exemplos.** Os resultados económicos dos exemplos **não são resultados**: os custos de obra, bomba, tratamento e manutenção ficam a zero, porque nenhuma fonte oficial aberta foi usada para eles (secção 4.7 (volume Tutorial)).

**O que declarar.** Ao usar a base, cite Cornes et al. (2018) e repita o reconhecimento exigido pela E-OBS; para a série do Funchal, a atribuição à Open-Meteo (CC BY 4.0) e a Hersbach et al. (2020); para os tarifários, a ERSAR («Fonte: ERSAR, www.ersar.pt. © ERSAR 2026. Todos os direitos reservados.») e a entidade do documento.

**Pendências conhecidas.** A licença da E-OBS para redistribuir a base derivada é omissa; por decisão do titular (25/10/2026), o uso comercial é bloqueado e avisado, e a tabela de qualidade, derivada do Iberia01 (ODbL), vai para um ficheiro separado sob a ODbL, com atribuição; os termos de reutilização dos sítios das entidades gestoras não foram encontrados (Águas e Energia do Porto) ou não foram verificados (as restantes); o texto do aviso da E-OBS e partes deste manual precisam de revisão antes da primeira distribuição. Estas pendências estão registadas em `docs/DADOS.md`.

---

## Apêndice F — Ficheiros, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

### F.1. O que o programa lê

<!-- tabela: **Tabela 43** — Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto guardado como tabela por uma versão inicial do programa | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia (a edição traz um exemplo em `data/rainfall`) | etapa 1. Projeto e Chuva |
| procura diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de procura, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um ficheiro desses, o programa avisa e adota os valores
> padrão para o que falta. A secção 3.8 (volume Guias de uso) mostra o que conferir depois de importar.

---

### F.2. O que o programa escreve

<!-- tabela: **Tabela 44** — Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Guardar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| folha de cálculo | `.xlsx` | série diária, varrimento e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV escolhe-se o separador: **ponto e vírgula** para abrir numa folha de cálculo
configurada em português, **vírgula** para o padrão internacional. Escolher mal faz a folha de
cálculo abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um ficheiro JSON com as
propriedades dos componentes, para compatibilização BIM. A secção 3.9 (volume Guias de uso) trata de todos.

---

### F.3. O ficheiro de projeto, por dentro

O `.triton` é um ficheiro de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete secções:

<!-- tabela: **Tabela 45** — As sete secções do ficheiro de projeto e o que cada uma guarda -->
| Secção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a eletrobomba |
| `water_quality_and_etap` | classe-alvo, desinfeção e tratamento |
| `financial_and_economic` | tarifas, impostos, atualizações e prazo |

O apêndice A lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do ficheiro.** É o que torna o projeto reproduzível:
> quem receber o ficheiro obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um ficheiro e muito para um anexo de e-mail com
> vinte deles.

---

### F.4. Onde ficam as coisas

<!-- tabela: **Tabela 46** — Localização dos ficheiros do programa e dos ficheiros do utilizador -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| os tarifários transcritos (Lisboa, Porto e Funchal) | dentro do programa, em `triton\data\portugal_tarifarios.json` |
| os casos do manual | na pasta do programa, em `casos` |
| os três projetos de exemplo (Lisboa, Porto e Funchal) | na pasta do programa, em `examples\portugal` |
| a base de precipitação por município (Iberia01) e a E-OBS opcional | na pasta do programa, em `data\chuva_iberia01_p1.db` a `p4.db`, `data\ibe_unidades.db`, `data\chuva_ilhas_era5.db` e `data\portugal_eobs.db` |
| **os seus projetos e relatórios** | **onde escolher ao guardar** |

O programa não cria pasta de trabalho nem guarda ficheiros escondidos. Cada gravação
pergunta o destino, e nada do que se produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada do que é seu.

---

### F.5. O ficheiro de estudo em lote (`estudo.json`)

Usado por `triton estudo` (capítulo «Comparar muitos casos de uma vez»). Esquema `triton-estudo`, versão 1.

<!-- tabela: **Tabela 47** — Secções do ficheiro estudo.json (esquema triton-estudo, versão 1) -->
| Secção | Conteúdo |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; outra versão é recusada |
| `estudo` | `id` (letras, números, ponto, hífen e sublinhado), `titulo`, `tipologia` (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario` ou `outra`), `tipologia_rotulo`, `autores`, `nota` |
| `projeto_base` | `arquivo`: um `.triton`, com caminho relativo ao `estudo.json`; ou `modelo`: `"edicao"`, o modelo de projeto da edição (então cada caso informa área, demanda, fração e chuva: nada é presumido) |
| `padroes` | `substituicoes` e `clima` aplicados a todos os casos; o que o caso declara vence o padrão |
| `casos` | lista; cada caso tem `id`, `nome`, `grupo` (por padrão, a tipologia), `projeto` (outro `.triton` para este caso), `clima` e `substituicoes` |
| `clima` | `arquivo` (série diária de chuva, CSV), `data_inicio` (dd/mm/aaaa), `nome` e `fonte` (rótulos que vão para a procedência) |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` ou `all`), `volume` (`otimo_tecnico`, `topsis`, `smaa_vikor` ou um volume em litros), `pesos` (quatro de eixo — técnico, económico, ambiental, estrutural — ou oito de critério; três, de estudos anteriores à 0.2.0, ainda aceites), `partes_no_eixo` (oito valores) e `semente` |
| `saidas` | `formatos` (`csv`, `json`, `md`, `tex`, `xlsx`), `metricas`, `casas_decimais` (um inteiro ou uma por métrica), `idioma` (`auto`, `pt-BR`, `pt-PT`, `en`, `es`, `zh`), `milhar`, `legenda` e `orientacao` (`casos_nas_linhas` ou `metricas_nas_linhas`) |

Chaves que começam por `_` são comentários e o programa as ignora. Campo vazio, `null` ou «XX» é «a preencher»: a validação o recusa e diz onde está. Uma chave desconhecida é erro, com a sugestão da mais parecida. `triton estudo esquema` imprime o JSON Schema do ficheiro, para completar e conferir no editor.

#### F.5.1. Apelidos das substituições

<!-- tabela: **Tabela 48** — Apelidos das substituições e o campo do projeto que cada um altera -->
| Apelido | Campo do projeto | Unidade |
| :--- | :--- | :--- |
| `area_captacao_m2` | `area` | m² |
| `coeficiente_escoamento` | `runoff_coeff` | 0 a 1 |
| `descarte_mm` | `discard` | mm |
| `usuarios` (também `populacao`, `pessoas`, `ocupantes`) | `residents_count` | pessoas |
| `demanda_per_capita_l_dia` | `demand_value` | L/pessoa·dia |
| `demanda_total_l_dia` | `demand_value` (a demanda total dividida pelos utilizadores) | L/dia |
| `fracao_pluvial_pct` ou `fracao_pluvial` | `rainwater_share` | % ou 0 a 1 |
| `volume_reservatorio_l` | `lower_tank_fixed` (e `lower_tank_mode` = volume fixo) | L |
| `volume_maximo_l`, `passo_volume_l` | `lower_tank_max` (varredura), `lower_tank_step` | L |
| `reservatorio_superior_l` | `upper_tank_vol` (e `upper_tank_used`) | L |
| `limiar_bombeamento_l`, `economias`, `irrigacao_l_dia` | `pumping_threshold`, `num_economias`, `irrigation_liters_per_day` | L, unidades, L/dia |
| `data_inicio`, `regra_phi`, `delta_ideal_pct` | `start_date`, `phi_operation_rule`, `delta_ideal` | dd/mm/aaaa, 0 a 1, %/m³ |
| `periodo_analise_anos`, `tma_pct_mes`, `tarifa_energia` | `analysis_period_years`, `tma`, `elec_tariff` | anos, % ao mês, moeda/kWh |

Além dos apelidos, a chave de uma substituição pode ser **qualquer campo que `--set` aceita** (por exemplo `cost_labor`) ou um **caminho pontilhado do próprio `.triton`**, como `inputs.building_and_demand.catchment_area_m2`. O caminho precisa existir no projeto e o valor precisa ter o mesmo tipo do que já está lá; senão o caso termina com erro claro, que lista as chaves disponíveis. Um apelido desconhecido também é recusado, com a sugestão do mais parecido. Dois nomes para o mesmo parâmetro no mesmo caso (`area_captacao_m2` e `area_m2`, ou `fracao_pluvial` e `fracao_pluvial_pct`) são conflito. A fração em 0 a 1 recusa 40 (provável percentual); o percentual recusa fora de 0 a 100.

As substituições passam pela mesma conciliação de frações do `--set`, e o preenchimento preliminar de custos (CAPEX) roda **depois** delas, de modo que o preço da cisterna acompanha o volume do caso. `triton estudo apelidos` lista todos os apelidos e métricas, na língua da edição.

#### F.5.2. Saídas do estudo

<!-- tabela: **Tabela 49** — Ficheiros que triton estudo run grava na pasta de saída -->
| Ficheiro | Conteúdo |
| :--- | :--- |
| `resultados.csv` | formato **tidy**: uma linha por caso e métrica (`estudo_id`, `caso_id`, `caso`, `grupo`, `metrica`, `rotulo`, `valor`, `unidade`, `status`); ponto decimal, sem separador de milhar, UTF-8 |
| `resultados.json` | os mesmos valores, mais a **proveniência**: versão do Triton, edição, SHA-256 do `estudo.json` e de cada projeto e série de chuva, fonte, crédito e licença da chuva, avisos e a data de execução |
| `tabela.md` | tabela em Markdown, com os números no formato do idioma (vírgula decimal em português e espanhol, ponto em inglês e chinês) |
| `tabela.tex` | tabela LaTeX com `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), pronta para colar; precisa de `\usepackage{booktabs}` |
| `tabela.xlsx` | opcional (`xlsx` em `formatos`): números de verdade, formatados, mais as abas `tidy` e `proveniencia` |
| `resumo.md` | resumo curto: casos, faixa de cada resultado, avisos, fontes e licenças |
| `casos/<id>/resultado.json` e `analise.json` | todas as métricas do caso e a análise completa do motor (é o que o `resumo` e o `texto` leem) |
| `estudo.json` | cópia do estudo que gerou a pasta |
| `consolidado.csv` e `consolidado.md` | gravados por `triton estudo consolidar` (não pelo `run`): uma linha por tipologia (`grupo`), caso, métrica e unidade, com `n`, mínimo, média, mediana e máximo dos `resultados.csv` encontrados |

As saídas não levam caminho absoluto: os projetos aparecem com caminho relativo ao `estudo.json` (ou só o nome). Duas execuções do mesmo estudo dão ficheiros idênticos; a data de execução é a única diferença, e a variável de ambiente `SOURCE_DATE_EPOCH` a fixa. O `xlsx` guarda a data de criação nas propriedades do ficheiro e não é idêntico byte a byte, só no conteúdo.

**Retomada e códigos de saída.** Numa pasta de saída que já tem resultados, `run` exige `--retomar` (pula os casos prontos e inalterados: a impressão digital do caso inclui o estudo, os ficheiros, a versão e a edição) ou `--sobrescrever` (refaz tudo). O código de saída é 0 se todos os casos foram calculados, 1 se algum caso terminou com erro (as saídas dos demais são gravadas e o caso com erro aparece com `status` `erro`) e 2 se o estudo ou os argumentos são inválidos.

**Métricas.** O volume de cada caso é, por padrão, o ótimo técnico da varredura (`volume: "otimo_tecnico"`); com `"topsis"`, o primeiro do ranking; com um número, o volume fixo. As métricas disponíveis incluem `volume_l`, `economia_agua_potavel_pct`, `agua_pluvial_m3_ano`, `agua_potavel_m3_ano`, `extravasamento_m3_ano`, os dias com atendimento total, parcial e nulo, `capex`, `vpl`, `economia_anual_agua`, `opex_anual`, `tir_anual_pct`, `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` e `aceitabilidade_smaa_pct`, além das entradas do caso (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). As métricas económicas pedem `analise.tipo` `economic` ou `all`; as ambientais, `environmental` ou `all`. Os nomes crus do relatório (`potable_savings_pct`) também valem. Valores monetários saem na moeda de cada projeto; se os casos têm moedas diferentes, o resumo avisa que não são comparáveis e o comparativo não os agrega. Com CAPEX igual a zero (custos não informados), o resumo avisa que VAL, TIR e payback não são resultados.

**Texto com os números.** `triton estudo texto` substitui no seu modelo `.md` os marcadores cercados por chaves duplas (duas de cada lado; os exemplos abaixo vêm sem elas): `economia_agua_potavel_pct:caso-01` (o valor de um caso), `economia_agua_potavel_pct:@min`, `@max`, `@media`, `@mediana` (sobre os casos calculados; `@media(escolar)` restringe a um grupo), `n_casos` e, depois de uma barra vertical, as casas decimais (`vpl:caso-01|0`). Onde falta resultado o marcador vira «XX» e o comando lista as pendências (com `--estrito`, termina com código 1). Métrica desconhecida é erro.

### F.6. Compatibilidade entre versões

<!-- tabela: **Tabela 50** — Compatibilidade entre versões do ficheiro de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o valor por defeito |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto legado em CSV | abre com aviso; confira o que a secção 3.8 (volume Guias de uso) lista |
| ficheiro JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um ficheiro JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores por defeito — e o utilizador
simularia 100 m² acreditando simular os 180 m² que o ficheiro descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.

---

## Apêndice G — Glossário

Termos técnicos e siglas, em português europeu, com o equivalente em inglês quando ele é usado na
literatura, acompanhados das diretrizes de padronização terminológica do Triton.

---

**AAC** (*aproveitamento de água de chuva*). Emprego da água precipitada sobre coberturas
para usos não potáveis em edifícios; a EN 16941-1 trata os sistemas de utilização de água
da chuva no local. Prefira-se o termo «aproveitamento» a «reutilização», porque a água de chuva captada
na cobertura é um recurso primário, e não um efluente gerado por um uso anterior.

**ACV** (*life cycle assessment*). Avaliação de ciclo de vida. Método que contabiliza os
impactos ambientais de um produto ao longo de toda a sua existência, da extração das
matérias-primas ao descarte. A do programa é de **triagem**, e não um inventário completo
conforme a ISO 14040.

**Água de chuva** (*rainwater*). Precipitação atmosférica recolhida diretamente em
superfícies impermeáveis de cobertura (telhados e lajes impermeabilizadas), antes de atingir
o solo ou as redes públicas. Designa o recurso natural e a fonte hídrica captada; evite-se a
forma coloquial «água da chuva».

**Água não potável** (*non-potable water*). Água que não se destina ao consumo humano direto,
mas cumpre os requisitos de qualidade exigidos para os usos admitidos: descargas de autoclismos e
mictórios, lavagem de veículos, pavimentos e roupa, rega de jardins e torres de arrefecimento.

**Água pluvial** (*stormwater*, *pluvial water*). Água de chuva que escoa superficialmente
por superfícies urbanas ou é conduzida por canalizações e sistemas prediais de drenagem. No Triton,
o termo aplica-se de preferência à infraestrutura predial e aos componentes de engenharia: *sistema
de aproveitamento de água pluvial (SAAP)*, *rede pluvial*, *procura pluvial*, *consumo de água pluvial*
e *extravasamento pluvial*.

**Água potável** (*potable water*, *drinking water*). Água que cumpre integralmente os
requisitos de qualidade da água para consumo humano em vigor no local do projeto, destinada à
ingestão direta, à preparação de alimentos e à higiene pessoal.

**Área de captação** (*catchment area*). Área projetada na **horizontal** da superfície
impermeável da cobertura onde a água é captada. Não é a área inclinada do telhado, nem a área
de contribuição usada para dimensionar caleiras e tubos de queda.

**BD+C** (*Building Design and Construction*). Família de referenciais do LEED
para projeto e construção de edificações novas ou em grande reforma. É a família
tratada neste manual, nas versões 4, 4.1 e 5.

**BIM** (*building information modeling*). Modelagem da informação da construção.
Representação digital da edificação em que cada componente carrega propriedades além da
geometria, o que permite compatibilizar projetos de disciplinas diferentes.

**CAD** (*computer-aided design*). Desenho assistido por computador. O programa exporta o
esquema hidráulico em DXF, formato de intercâmbio aceito pelos programas de CAD.

**CAOP** (*Carta Administrativa Oficial de Portugal*). Carta com os limites administrativos oficiais, publicada pela Direção-Geral do Território. A versão CAOP2025 define os limites dos 308 concelhos usados para calcular a série de chuva de cada concelho.

**CAPEX** (*capital expenditure*). Investimento inicial.

**CDD** (*consecutive dry days*). Maior sequência de dias consecutivos com chuva
abaixo de 1 mm.

**Coeficiente de escoamento** (*runoff coefficient*). Fração da chuva que
efetivamente chega ao reservatório, descontadas perdas por absorção, evaporação e
molhamento inicial da cobertura.

**Comprimento representativo de série de precipitação** (*representative rainfall time series length*, $N_{rep}$).
Menor período contínuo em anos de dados diários de chuva necessário para estabilizar
estatisticamente o dimensionamento e o desempenho do sistema (reproduzindo o volume ideal
e o potencial de economia da série completa sob confiança $\ge 90\%$), segundo a
metodologia de Geraldi e Ghisi (2017, 2018, 2019). O comprimento necessário não é uma
constante geográfica fixa: cresce com a fração atendível e com o nível de procura da edificação.

**E-OBS**. Conjunto europeu de dados meteorológicos diários em grelha, construído a partir de observações de estações (projeto ECA&D, serviço Copernicus de alterações climáticas). A Edição Ibérica usa a versão v33.0e da precipitação diária, em grelha de 0,1°, de 1950 a 2025, e obtém a série de cada concelho pela média das células dentro do seu limite (apêndice E).

**ERA5**. Reanálise global do Centro Europeu de Previsões Meteorológicas de Médio Prazo (ECMWF), produzida pelo serviço Copernicus de alterações climáticas. Combina um modelo atmosférico com observações e dá uma série contínua em grelha. Usa-se no exemplo do Funchal; é uma média de área, e não um registo de udómetro.

**Fiabilidade temporal** ($C_t$). Percentual de dias em que o sistema atendeu
plenamente ($V_{con,t} = D_{pl,t}$), parcialmente ou não atendeu a procura pluvial.

**Fiabilidade volumétrica** ($C_v$). Fração da procura **pluvial** que o sistema atendeu
($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Não confundir com o potencial de economia,
que tem no denominador a procura total da edificação.

**CSV** (*comma-separated values*). Formato de ficheiro de texto em que cada linha é um
registo e as colunas são separadas por um caractere, tipicamente vírgula ou ponto e
vírgula. É o formato das séries de precipitação.

**cv**. Cavalo-vapor, unidade de potência equivalente a 0,7355 kW, usada na indicação de
eletrobombas. Uma eletrobomba de meio cv tem 0,37 kW de potência de eixo.

**CWD** (*consecutive wet days*). Maior sequência de dias consecutivos com chuva
igual ou superior a 1 mm.

**IVA**. Imposto sobre o valor acrescentado. Na fatura de água, cada parcela leva a taxa que o respetivo tarifário declara (6% na água de Lisboa e do Porto, 4% no Funchal, este último por confirmar); o programa não fixa nenhuma taxa no código (apêndice D).

**Procura estocástica** (*stochastic water demand*). Modelagem do consumo diário de água como
variável probabilística que varia dia a dia e entre realizações (Silva e Ghisi, 2016),
permitindo avaliar o escalão de incerteza do dimensionamento e dos indicadores de desempenho
sob variabilidade real de uso.

**Procura pluvial** (*pluvial demand*, $D_{pl}$). Parcela da procura diária de água da
edificação que pode ser suprida pelo sistema de aproveitamento ($D_{pl,t} = D_{tot,t} \times f$).
Corresponde aos pontos de consumo não potável interligados à rede pluvial.

**Descarte de primeiras águas** (*first flush*). Lâmina inicial de chuva desviada do
sistema, que arrasta a sujidade depositada na cobertura (o programa parte de 2 mm, que o utilizador
deve ajustar à sua cobertura). No Triton é **subtraída** da chuva do dia.

**Disponibilidade**. Regime tarifário em que um valor fixo **soma** por cima do
consumo medido. Cada metro cúbico economizado desconta.

**DN** (*diâmetro nominal*). Designação comercial do diâmetro de um tubo ou conexão, em
milímetros. Não corresponde exatamente ao diâmetro interno nem ao externo: é um número de
referência do qual decorrem as dimensões reais, tabeladas por norma.

**DXF** (*drawing exchange format*). Formato de intercâmbio de desenhos técnicos, lido
por praticamente todos os programas de CAD.

**EDGE** (*excellence in design for greater efficiencies*). Referencial de certificação
da International Finance Corporation, do Banco Mundial. Mede economia percentagem contra
um caso-base local em três dimensões independentes e exige que cada uma cruze o limiar.

**EN** (*Europäische Norm*, norma europeia). Norma publicada pelo Comitê Europeu de
Normalização. Neste manual, a EN 15978, que define os módulos do ciclo de vida da
edificação, e a EN 15804, que rege as declarações ambientais de produtos de construção.

**EPD** (*Environmental Product Declaration*). Declaração ambiental de produto: documento
verificado por terceiros, conforme a ISO 14025 e, na construção, a EN 15804, que publica
os impactos do ciclo de vida de um produto por unidade declarada. É a fonte preferida para
fatores de emissão de materiais e equipamentos.

**ESG** (*environmental, social and governance*). Conjunto de critérios ambientais,
sociais e de governança usado na avaliação de empresas e de empreendimentos. O programa
alimenta indicadores ambientais desse conjunto.

**ETAP**. Estação de tratamento de água pluvial. No programa, o conjunto de filtro
de entrada, desinfeção e filtro de polimento.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). Grupo de trabalho
internacional que padronizou os índices de extremos climáticos, dos quais o programa
calcula oito.

**Eficiência de armazenamento** (*storage efficiency*). Água de chuva entregue por dia
dividida pelo volume da cisterna inferior, em %: a renovação diária do volume construído. Cai
com o volume e trava o sobredimensionamento. Não é a ocupação média da cisterna.

**Extravasamento** (*spillage*, *overflow*). Volume que excede a capacidade do reservatório
e é conduzido pelo extravasor quando ele já está cheio.

**Fração atendível por água pluvial** (*non-potable demand share*, $f$). Percentual da procura
total de água da edificação ($D_{tot}$) passível de suprimento por água de chuva ($f = D_{pl} / D_{tot}$).
Representa o **teto assintótico intransponível** do potencial de economia de água potável
($E_{pot} \le f$): mesmo sob capacidade infinita de armazenamento e precipitação ilimitada,
a economia de potável nunca ultrapassa a fração atendível, pois o restante ($1 - f$) é
reservado aos usos nobres e potáveis. Distingue-se da fiabilidade volumétrica ($C_v = E_{pot} / f$),
que avalia o atendimento da parcela pluvial.

**Franquia no mínimo**. Regime tarifário em que o valor fixo já inclui um volume de
consumo. Economizar **abaixo** da franquia não reduz a fatura.

**Ganho marginal**. Variação do potencial de economia por metro cúbico acrescentado
ao reservatório, em %/m³ ($\Delta E_{pot} / \Delta V$). Critério de escolha do volume ideal.

**GRI** (*Global Reporting Initiative*). Padrão internacional de divulgação corporativa
de desempenho socioambiental. Sua série 303 trata de água e efluentes.

**IBE**. Sigla da Edição Ibérica do programa («Triton IBE», para a Península Ibérica): abre em português europeu, em euros, com a chuva do Iberia01 por município e os tarifários transcritos de Lisboa, Porto e Funchal. A linha de cobertura do programa diz quantos locais há em cada país. Os custos e os fatores de emissão são indicados pelo utilizador.

**IFC**. A sigla designa duas coisas distintas. Em certificação, é a *International
Finance Corporation*, do Banco Mundial, que desenvolve o EDGE. No contexto BIM, é o
*Industry Foundation Classes*, formato aberto de intercâmbio que o programa **não**
exporta: a exportação BIM do programa é um ficheiro JSON de propriedades.

**IPCC** (*Intergovernmental Panel on Climate Change*). Painel intergovernamental que
sintetiza o conhecimento científico sobre mudança do clima e organiza os relatórios de
avaliação a que as projeções climáticas se referem.

**ISO 14040**. Norma internacional que estabelece os princípios e a estrutura da
avaliação de ciclo de vida. Um inventário conforme a ISO 14040 exige rastreabilidade de
cada fluxo e revisão crítica externa, requisitos que uma avaliação de triagem não cumpre.

**JSON** (*JavaScript object notation*). Formato de ficheiro de texto estruturado, legível
por pessoas e por programas. É o formato interno do ficheiro `.triton`.

**LCOW** (*levelized cost of water*). Custo nivelado da água: razão entre o valor presente
dos custos do sistema (o investimento e os custos de exploração: energia, manutenção,
cloro e linha de tratamento) e o volume atualizado de água pluvial entregue ao longo do
horizonte de análise, à mesma taxa, em €/m³. É um dos oito critérios do multicritério. Permite confrontar a viabilidade económica do sistema diretamente
com a tarifa da entidade gestora.

**LEED** (*leadership in energy and environmental design*). Referencial de certificação
ambiental de edificações do *U.S. Green Building Council*, o mais difundido
internacionalmente. Trata eficiência hídrica na categoria *Water Efficiency*: na versão 4,
pelos créditos WEc1 e WEc2; na versão 5, pelo crédito WEc2, *Enhanced Water Efficiency*.

**m.c.a.** Metro de coluna d'água, unidade de pressão equivalente à exercida por uma
coluna de água de um metro de altura, cerca de 9,81 kPa. É a unidade usual em instalações
prediais.

**Micromedição**. Medição individualizada por unidade habitacional em edifício
multifamiliar. Informada ao programa como número de economias.

**Manuais do Triton** (*Triton manual suite*). A documentação do programa, montada
das mesmas fontes em três formatos: o manual completo, oito volumes avulsos, cada um com
uma parte dele, e o sítio Web de documentação. Os volumes servem a quem precisa de uma parte
só, para consultar ou enviar:

1. **Manual completo**: todos os capítulos e apêndices.
   ![Capa do Manual Completo](../figuras/capas/capa_completo.png)
2. **Volume 1 — Comece aqui**: o que o programa faz, como instalá-lo e por onde entrar
   conforme o seu objetivo.
   ![Capa do Volume 1 — Comece Aqui](../figuras/capas/capa_1-comece-aqui.png)
3. **Volume 2 — O método**: as equações, os critérios e as fontes por trás de cada número
   que o programa publica.
   ![Capa do Volume 2 — O Método](../figuras/capas/capa_2-metodo.png)
4. **Volume 3 — Guias de uso**: outras cidades, clima futuro, tarifas, procura variável,
   lote, sensibilidade e exportação.
   ![Capa do Volume 3 — Guias Práticos](../figuras/capas/capa_3-guias.png)
5. **Volume 4 — Tutorial**: um projeto de moradia em Lisboa, do primeiro dado ao
   volume recomendado.
   ![Capa do Volume 4 — Tutorial](../figuras/capas/capa_4-tutorial.png)
6. **Volume 5 — Erros, limitações e fiabilidade**: os erros mais comuns, os limites
   do modelo e como o programa é verificado.
   ![Capa do Volume 5 — Fiabilidade](../figuras/capas/capa_5-fiabilidade.png)
7. **Volume 6 — Correções, erros e versões**: o que mudou entre versões, as
   mensagens de erro e como relatar um problema.
   ![Capa do Volume 6 — Versões](../figuras/capas/capa_6-versoes.png)
8. **Volume 7 — Modulação probabilística**: o estudo refeito com premissas sorteadas —
   variáveis, distribuições, leitura dos resultados e limites do método.
   ![Capa do Volume 7 — Modulação probabilística](../figuras/capas/capa_7-modulacao.png)
9. **Volume 8 — Apêndices**: parâmetros, processos, fatores de emissão, tarifas, base
   climática, formatos, glossário e referências.
   ![Capa do Volume 8 — Apêndices](../figuras/capas/capa_8-apendices.png)

Os PDFs acompanham o programa e abrem pela etapa 9. Documentação.

**Payback de carbono**. Tempo para a economia anual líquida de emissões pagar o
carbono incorporado na fabricação do sistema.

**Payback descontado**. Tempo para o fluxo de caixa descontado acumulado cruzar zero.

**Partes no eixo**. A repartição do peso de um eixo do multicritério pelos seus critérios.
Só a proporção dentro do eixo importa; por omissão, as partes são iguais.

**Peso do sistema**. Massa a seco, carga de água e carga em operação do sistema, em kg e kN,
no subsolo, na cobertura e nas prumadas e rede. Os alertas usam limiares de atenção do
programa, e não de norma.

**PB**. Preço-base, em €/m³, da fórmula exponencial `PB × Cⁿ`, em que `C` é o consumo do mês e
`n` o expoente da tabela exponencial para esse consumo. É um dos seis regimes que o programa reconhece; os
tarifários transcritos para Portugal não o usam.

**PEAD**. Polietileno de alta densidade, material dos reservatórios de plástico mais comuns.
É o código do material no ficheiro de projeto.

**Piso de pagamento**. Regime tarifário em que a fatura **não fica** abaixo de um
valor. Diferente de disponibilidade: o piso limita por baixo, a disponibilidade soma
por cima.

**Potencial de economia de água potável** (*potable water saving potential*, $E_{pot}$).
Fração da procura **total** da edificação suprida por água pluvial ($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$).
É o indicador central do programa, limitado superiormente pela fração atendível ($E_{pot} \le f$).

**pp**. Pontos percentuais. Usado para exprimir a diferença entre dois percentuais: de
35% para 37% vão dois pontos percentuais, e não dois por cento.

**PRCPTOT**. Precipitação total anual em dias úmidos.

**PRFV**. Plástico reforçado com fibra de vidro, material de reservatórios de médio e
grande porte. Aparece no programa sob a designação «fibra».

**PRT**. Nome antigo da Edição Ibérica (IBE), de quando ela se chamava Edição Portugal. Projetos e scripts que ainda usam «PRT» (ou «POR») abrem como IBE.

**PVC**. Policloreto de vinilo, material das tubagens prediais de água fria e das colunas de
desvio do descarte inicial.

**R95p**. Soma da precipitação dos dias acima do percentil 95 dos dias úmidos.

**Rendimento da bomba**. Razão entre a potência hidráulica entregue à água e a
potência mecânica no eixo. Não inclui o motor.

**Rendimento do motor**. Razão entre a potência mecânica no eixo e a potência
elétrica consumida da rede.

**RX1day**, **RX5day**. Maior precipitação em um e em cinco dias consecutivos, no
ano.

**SAAP**. Sistema de aproveitamento de água pluvial. Conjunto integrado de componentes
prediais — área de captação, condutores, descarte inicial (*first flush*), estação de
tratamento (ETAP), cisterna inferior, reservatório superior, eletrobomba ou sobrepressor
e rede de distribuição independente — concebido para recolher, tratar, armazenar e fornecer
água não potável.

**SB**. Serviço básico: a parcela fixa mensal da fatura de água da fórmula exponencial, somada ao
resultado dessa fórmula.

**SDII** (*simple daily intensity index*). Precipitação média dos dias úmidos.

**SI** (*seasonality index*). Índice de sazonalidade de Walsh e Lawler. Zero quando a
chuva é uniforme ao longo do ano.

**SMAA** (*stochastic multicriteria acceptability analysis*). Método que sorteia
pesos — no programa, oito, um por critério — e devolve a probabilidade de cada alternativa
vencer.

**SSP** (*shared socioeconomic pathways*). Trajetórias socioeconómicas partilhadas,
que descrevem hipóteses coerentes de desenvolvimento global e as emissões correspondentes.
Combinam-se com os modelos climáticos para produzir projeções.

**TIR**. Taxa interna de retorno. A taxa de desconto que zera o valor presente
líquido.

**taxa de atualização**. Taxa de atualização. A taxa de desconto adotada.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*).
Método de ordenação multicritério de Hwang e Yoon. No programa, ordena os volumes por oito
critérios em quatro eixos: técnico, económico, ambiental e estrutural.

**TRH** (*taxa de recursos hídricos*). Taxa por m³ que acresce à fatura de água e de águas residuais. No tarifário do Porto, a TRH da água é devida à Agência Portuguesa do Ambiente (APA) e leva IVA; no de Lisboa, a TRH do saneamento acresce por m³ recolhido.

**UV**. Radiação ultravioleta, empregada na desinfeção de água por inativação de
microrganismos. Atua apenas no instante da passagem pelo reator e não deixa residual, ao
contrário da cloragem.

**VIKOR**. Método de decisão multicritério proposto por Opricovic, que busca uma solução
de compromisso entre critérios conflitantes. Ver também *SMAA*.

**Volume ideal** (*optimal tank volume*). Menor volume de reservatório da grade de simulação
a partir do qual o ganho marginal de economia de água potável ($\Delta E_{pot} / \Delta V$)
cai abaixo de um limiar declarado (tipicamente $1,0\%/\text{m}^3$ ou $0,5\%/\text{m}^3$).
Evita o superdimensionamento de reservatórios, assegurando a melhor relação custo-benefício.

**VAL**. Valor atual líquido.

**WEM**. Codificação das medidas de eficiência hídrica do EDGE. A WEM14 é o sistema
de aproveitamento de água pluvial.

**XLSX**. Formato de pasta de trabalho do Microsoft Excel, baseado em XML compactado. É um
dos formatos de exportação de folhas de cálculo e de resultados da linha de comando.

**YAS** (*yield after spillage*). Regra de operação em que o extravasamento é
calculado **antes** da retirada da procura e, na forma estrita, a retirada do dia sai
só do volume guardado na véspera. O programa calcula o extravasamento antes, como a
YAS, mas deixa a chuva do dia atender a procura do dia; fica entre a YAS e a YBS
(secção 2.1 (volume O método)).

**YBS** (*yield before spillage*). Regra de operação em que a procura é retirada **antes**
do cálculo do extravasamento. Supõe consumo anterior à chuva do dia e sobrestima o
aproveitamento; o programa não a adota, e o resultado dele fica entre a YAS e a YBS.

---

### G.1. Diretrizes de Padronização e Nomenclatura no Triton

A padronização terminológica é indispensável para assegurar a consistência e o rigor técnico
em artigos científicos, relatórios técnicos, na interface gráfica e na documentação do Triton.
As convenções a seguir detalham a distinção de termos correlatos frequentemente confundidos:

#### G.1.1. 1. Água de Chuva versus Água Pluvial versus «Água da Chuva»

<!-- tabela: **Tabela 51** — Padronização terminológica de água de chuva e água pluvial -->
| Termo | Definição e Contexto de Aplicação | Situação no Triton | Referência |
| :--- | :--- | :--- | :--- |
| **Água de chuva** (*rainwater*) | Precipitação atmosférica recolhida diretamente na cobertura (telhado/laje impermeabilizada), antes de atingir o solo ou as redes públicas. Refere-se à **fonte hídrica** e ao recurso ambiental. | **Canónico e preferencial** para o recurso captado («aproveitamento de água de chuva», «precipitação de água de chuva»). | Prática de redação técnica e científica. |
| **Água pluvial** (*stormwater* / *pluvial water*) | Água de chuva após escoamento superficial urbano ou quando conduzida por canalizações e sistemas prediais de drenagem e armazenamento. Aplica-se à **infraestrutura física** e aos componentes de engenharia. | **Canónico e preferencial** para sistemas, redes e balanço («sistema predial de água pluvial - SAAP», «rede pluvial», «procura pluvial», «extravasamento pluvial»). | Prática de redação técnica e científica. |
| **«Água da chuva»** | Expressão coloquial e informal. | **Desaconselhada**. Não deve ser empregada em publicações, textos normativos, relatórios do Triton ou código. | Prática de redação técnica e científica. |

#### G.1.2. 2. Fração Atendível, Procura Pluvial, Potencial e Fiabilidade

Para evitar ambiguidades matemáticas e conceituais frequentemente encontradas na literatura:

<!-- tabela: **Tabela 52** — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial -->
| Grandeza | Símbolo / Código | Definição | Fórmula | Relação / Teto |
| :--- | :--- | :--- | :--- | :--- |
| **Fração atendível por água pluvial** | $f$ / `rainwater_share` | Proporção da procura total da edificação correspondente a pontos de consumo não potável conectáveis ao SAAP. | $f = D_{pl} / D_{tot}$ | Parâmetro de projeto ($0 \le f \le 1$). Constitui o **teto assintótico** de $E_{pot}$. |
| **Procura pluvial** | $D_{pl}$ / `rainwater_demand` | Volume de água requerido pelos pontos não potáveis da edificação em um intervalo de tempo. | $D_{pl,t} = D_{tot,t} \times f$ | Em L/dia ou m³/ano. |
| **Volume de água pluvial consumido** | $V_{con}$ / `pluvial_consumed` | Volume de água não potável efetivamente suprido pelo reservatório pluvial aos pontos de consumo. | Determinado pelo balanço diário (secção 2.1 (volume O método)) | $V_{con,t} \le D_{pl,t}$ e $V_{con,t} \le S_{t-1} + C_t$. |
| **Potencial de economia de água potável** | $E_{pot}$ / `potential_potable_savings_pct` | Percentual da procura **total** da edificação economizado pelo aproveitamento pluvial. | $E_{pot} = \frac{\sum V_{con}}{\sum D_{tot}} \times 100\%$ | **Indicador central**. Sempre $E_{pot} \le f$. |
| **Fiabilidade volumétrica** | $C_v$ / `volumetric_reliability_pct` | Percentual da procura **pluvial** suprido pela água de chuva armazenada. | $C_v = \frac{\sum V_{con}}{\sum D_{pl}} \times 100\%$ | $C_v = \frac{E_{pot}}{f}$. Pode atingir 100% mesmo quando $E_{pot} < 100\%$. |
| **Fiabilidade temporal** | $C_t$ / `temporal_reliability_pct` | Percentual de dias da série em que a procura pluvial foi 100% atendida ($V_{con,t} = D_{pl,t}$). | $C_t = \frac{N_{dias\_plenos}}{N_{total}} \times 100\%$ | Mede a segurança de abastecimento diário sem suplementação potável. |

#### G.1.3. 3. Síntese de Nomenclatura Recomendada para Artigos e Relatórios

- Utilize **«aproveitamento de água de chuva»** (e não «reutilização de água da chuva» — a água de chuva não é um efluente; o seu uso é *aproveitamento*, não *reutilização*).
- Utilize **«área de captação»** para o plano horizontal da cobertura e reserve **«área de contribuição»** para o dimensionamento hidráulico de caleiras e tubos de queda.
- Utilize **«descarte de primeiras águas»** ou *first flush* para a lâmina inicial desviada, e não «limiar de descarte».
- Utilize **«fração atendível»** (e não «procura relativa» ou «fração de economia») para expressar a partição de usos não potáveis no consumo total.
- Utilize **«comprimento representativo de série»** para a extensão mínima em anos necessária para estabilização estatística da simulação (metodologia de Geraldi e Ghisi).
- Utilize **«LCOW»** ou **«custo nivelado da água»** para a métrica de custo unitário ao longo do ciclo de vida descontado à taxa de atualização.

---

## Apêndice H — Referências

Normas, publicações e bases que sustentam as decisões do programa. A lista da Edição Ibérica só traz normas
internacionais e europeias e publicações de alcance geral, mais os documentos portugueses de que o programa
depende. A lista completa, com a proveniência de cada citação, está no módulo de bibliografia do programa e no
separador Documentação.

---

### H.1. Normas de aproveitamento de água de chuva

**EN 16941-1:2024** — On-site non-potable water systems — Part 1: Systems for the use of rainwater.
Bruxelas: CEN, 2024.

---

### H.2. Referenciais de certificação

**LEED v4 / v4.1 BD+C** — USGBC. Categoria *Water Efficiency*, créditos WEc1 e WEc2. Registo de projetos
comerciais até 30 jun. 2027.

**LEED v5 BD+C** — U.S. GREEN BUILDING COUNCIL. *LEED v5 Building Design and Construction: rating system*.
Washington, DC: USGBC, nov. 2025. Pré-requisitos WEp1 (*Water Metering and Reporting*) e WEp2 (*Minimum Water
Efficiency*), créditos WEc2 (*Enhanced Water Efficiency*) e SSc3 (*Rainwater Management*).

**EDGE** — IFC, Grupo Banco Mundial. *EDGE Certification Process*, e a codificação WEM das medidas de eficiência
hídrica. Administrado pelo GBCI em mais de 120 países.

**GRI 303** — Global Reporting Initiative. Água e efluentes, indicadores 303-3 e 303-5.

---

### H.3. Métodos

**Hwang, C.-L.; Yoon, K.** (1981). *Multiple Attribute Decision Making: Methods and Applications*. A formulação
original do TOPSIS.

**Opricovic, S.; Tzeng, G.-H.** O método VIKOR e as condições C1 e C2 de vantagem aceitável e estabilidade.

**Lahdelma, R.; Hokkanen, J.; Salminen, P.** (1998), e **Tervonen, T.; Figueira, J.** (2008). SMAA e SMAA-2.

**Walsh, R. P. D.; Lawler, D. M.** (1981). O índice de sazonalidade.

**ETCCDI** — *Expert Team on Climate Change Detection and Indices*, da OMM. Os índices de extremos climáticos.

---

### H.4. Usos finais da água

**Mayer, P. W.; DeOreo, W. B. et al.** (1999). *Residential End Uses of Water*. Denver: AWWA Research
Foundation. Frequência de uso dos aparelhos: 5,05 descargas e 0,37 ciclos de máquina de lavar roupa por pessoa
por dia; as descargas são a base dos acionamentos da pressurização direta.

---

### H.5. Normas de avaliação de ciclo de vida

**ISO 14040:2006** — Environmental management: life cycle assessment, principles and framework. As quatro fases
da avaliação.

**ISO 14044:2006** — Environmental management: life cycle assessment, requirements and guidelines.

**EN 15978:2011** — Sustainability of construction works: assessment of environmental performance of buildings,
calculation method. Os módulos A a D do ciclo de vida do edifício.

**EN 15804:2012+A2:2019** — Sustainability of construction works: environmental product declarations, core rules
for the product category of construction products.

---

### H.6. Dimensionamento e desempenho de sistemas de aproveitamento pluvial

**SOUZA, E. L.; GHISI, E.** (2012). Potable water savings by using rainwater for non-potable uses in houses.
*Water*, v. 4, n. 3, p. 607-628. doi:10.3390/w4030607.

**CAMPISANO, A. et al.** (2017). Urban rainwater harvesting systems: research, implementation and future
perspectives. *Water Research*, v. 115. doi:10.1016/j.watres.2017.02.056.

**CAMPISANO, A.; MODICA, C.** (2015). Appropriate resolution timescale to evaluate water saving and retention
potential of rainwater harvesting for toilet flushing in single houses. *Journal of Hydroinformatics*, v. 17,
n. 3. doi:10.2166/hydro.2015.022.

**FEWKES, A.; BUTLER, D.** (2000). Simulating the performance of rainwater collection and reuse systems using
behavioural models. *Building Services Engineering Research and Technology*, v. 21, n. 2, p. 99-106.
doi:10.1177/014362440002100204.

**GHISI, E.** (2010). Parameters influencing the sizing of rainwater tanks for use in houses. *Water Resources
Management*, v. 24, n. 10, p. 2381-2403. doi:10.1007/s11269-009-9557-4.

**HASHIMOTO, T.; STEDINGER, J. R.; LOUCKS, D. P.** (1982). Reliability, resiliency, and vulnerability criteria
for water resource system performance evaluation. *Water Resources Research*, v. 18, n. 1, p. 14-20.
doi:10.1029/WR018i001p00014.

**MATOS, C.; SANTOS, C.; PEREIRA, S. et al.** (2013). Rainwater storage tank sizing: case study of a commercial
building. *International Journal of Sustainable Built Environment*, v. 2, n. 2, p. 109-118.
doi:10.1016/j.ijsbe.2014.04.004.

**SEMAAN, M. et al.** (2020). Optimal sizing of rainwater harvesting systems for domestic water usages: a
systematic literature review. *Resources, Conservation & Recycling: X*, v. 6, 100033.
doi:10.1016/j.rcrx.2020.100033.

---

### H.7. Clima futuro

**HAWKINS, E.; SUTTON, R.** (2011). The potential to narrow uncertainty in projections of regional precipitation
change. *Climate Dynamics*, v. 37, p. 407-418. doi:10.1007/s00382-010-0810-6.

**KISAKYE, V.; VAN DER BRUGGEN, B.** (2018). Effects of climate change on water savings and water security from
rainwater harvesting systems. *Resources, Conservation and Recycling*. doi:10.1016/j.resconrec.2018.07.009.

**LASH, D. et al.** (2014). Robust rainwater harvesting: probabilistic tank sizing for climate change
adaptation. *Journal of Water and Climate Change*. doi:10.2166/wcc.2014.080.

**MARAUN, D.** (2016). Bias correcting climate change simulations: a critical review. *Current Climate Change
Reports*, v. 2, n. 4, p. 211-220. doi:10.1007/s40641-016-0050-x.

---

### H.8. Ciclo de vida e energia de sistemas pluviais

**GHIMIRE, S. R. et al.** (2014). Life cycle assessment of domestic and agricultural rainwater harvesting
systems. *Environmental Science & Technology*, v. 48. doi:10.1021/es500189f.

**GHIMIRE, S. R. et al.** (2017). Life cycle assessment of a commercial rainwater harvesting system compared
with a municipal water supply system. *Journal of Cleaner Production*. doi:10.1016/j.jclepro.2017.02.025.

**VAZ, I. C. M. et al.** (2023). Sustainable rainwater management and life cycle assessment: challenges and
perspectives. *Sustainability*, v. 15, n. 16, 12133. doi:10.3390/su151612133.

**VIEIRA, A. S. et al.** (2014). Energy intensity of rainwater harvesting systems: a review. *Renewable and
Sustainable Energy Reviews*, v. 34, p. 225-242. doi:10.1016/j.rser.2014.03.012.

**WARD, S.; BUTLER, D.; MEMON, F. A.** (2012). Benchmarking energy consumption and CO2 emissions from
rainwater-harvesting systems: an improved method by proxy. *Water and Environment Journal*, v. 26, n. 2,
p. 184-190. doi:10.1111/j.1747-6593.2011.00279.x.

---

### H.9. Incerteza e simulação de Monte Carlo

**SILVA, A. S.; GHISI, E.** (2016). Uncertainty analysis of daily potable water demand on the performance
evaluation of rainwater harvesting systems in residential buildings. *Journal of Environmental Management*,
v. 180, p. 82-93. doi:10.1016/j.jenvman.2016.05.028.

**WILSON, E. B.** (1927). Probable inference, the law of succession, and statistical inference. *Journal of the
American Statistical Association*, v. 22, n. 158, p. 209-212. doi:10.1080/01621459.1927.10502953.

**SPEARMAN, C.** (1904). The proof and measurement of association between two things. *The American Journal of
Psychology*, v. 15, n. 1, p. 72-101. doi:10.2307/1412159.

**SALTELLI, A.; RATTO, M.; ANDRES, T.; CAMPOLONGO, F.; CARIBONI, J.; GATELLI, D.; SAISANA, M.; TARANTOLA, S.**
(2008). *Global Sensitivity Analysis: The Primer*. Chichester: Wiley. doi:10.1002/9780470725184.

---

### H.10. Dados de precipitação

**CORNES, R. C.; VAN DER SCHRIER, G.; VAN DEN BESSELAAR, E. J. M.; JONES, P. D.** (2018). An ensemble version
of the E-OBS temperature and precipitation data sets. *Journal of Geophysical Research: Atmospheres*, v. 123,
n. 17, p. 9391-9409. doi:10.1029/2017JD028200. A base de precipitação por concelho (apêndice E).

**DIREÇÃO-GERAL DO TERRITÓRIO.** *Carta Administrativa Oficial de Portugal (CAOP2025)*. Aviso n.º 3502/2026/2,
Diário da República, 2.ª série, n.º 34, de 18/02/2026. Os limites dos concelhos.

**HERSBACH, H. et al.** (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological
Society*, v. 146, p. 1999-2049. A reanálise da série de exemplo do Funchal.

**Open-Meteo.com.** Weather data by Open-Meteo.com, licença CC BY 4.0, com base na reanálise ERA5 do ECMWF
(Copernicus Climate Change Service). Interface de arquivo consultada em 14/10/2026.

---

### H.11. Fatores de emissão

As fontes que o programa regista para os fatores de triagem do apêndice C. A sua reverificação para esta
edição está pendente.

**FRANKLIN ASSOCIATES** para o American Chemistry Council (2020). *Cradle-to-Gate Life Cycle Analysis of
High-Density Polyethylene (HDPE) Resin*. Tabela 6.

**HAMMOND, G. P.; JONES, C. I.** (2008). Embodied energy and carbon in construction materials. *Proceedings of
the Institution of Civil Engineers: Energy*, v. 161, n. 2, p. 87-98. doi:10.1680/ener.2008.161.2.87.

**EPD Australasia.** *Environmental product declaration: PVC pipes*, S-P-05503, 25/11/2022, EN 15804+A2.

**Grundfos.** *Environmental Product Declaration*, EPD-GRU-20250340-CBA1-EN, 2025, módulos A1 a A3.

**worldstainless** (World Steel Association). Relatório de emissões de CO₂, 24/09/2024.

**Composites UK.** *Embodied carbon data for composites*.

---

### H.12. Tarifários

Os documentos das entidades gestoras de onde se transcreveram os tarifários do apêndice D, com o endereço
de origem e a impressão digital SHA-256 registados em `tarifas_portugal/fontes/FONTES.tsv`:

**EPAL.** *Preços de venda de água*, 1.ª edição 2026 (Lisboa, água).

**Câmara Municipal de Lisboa.** *Tarifário do saneamento 2026* e *Tarifário dos resíduos urbanos 2026*,
Regulamento CML n.º 569-A/2014.

**Águas e Energia do Porto, EM.** *Tarifário Geral 2026*.

**Câmara Municipal do Funchal.** *Tabela de Taxas e Outras Receitas Municipais 2026*.

---

### H.13. Como citar o programa

Ao publicar um estudo feito com o Triton, cite o programa **com a versão** e a edição, e declare os itens da
secção 4.10 (volume Tutorial). Um estudo que cita o programa sem versão não é reproduzível: as correções entre versões mudam
resultados, e a secção 2.6 (volume O método) traz o exemplo do consumo da eletrobomba, que mudou 65% entre duas versões
consecutivas.

O programa está depositado no Zenodo. O DOI de todas as versões, 10.5281/zenodo.23402915, aponta sempre para a
mais recente; a versão 0.1.0 tem o DOI próprio 10.5281/zenodo.23402916, e a 0.2.0 ainda não tem DOI próprio.
Num estudo, cite o DOI de todas as versões e escreva a versão usada: para reproduzir um estudo feito com a
0.1.0, use a 0.1.0, porque o multicritério da 0.2.0 ordena os volumes de outra maneira (secção 6.3 (volume Correções, bugs e versionamento)).

---

## Apêndice I — Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

### I.1. Ficha 1 — O fluxo de um estudo completo

<!-- tabela: **Tabela 53** — Ficha de consulta: os dez passos de um estudo completo e a secção que trata de cada um -->
| # | Passo | O que se decide nele | Secção |
| ---: | :--- | :--- | ---: |
| 1 | Projeto e chuva | série, área, coeficiente, descarte | 4.1 (volume Tutorial) |
| 2 | Edificação | tipologia, procura, fração atendível | 4.2 (volume Tutorial) |
| 3 | Primeira simulação | um volume de palpite, para ver | 4.3 (volume Tutorial) |
| 4 | Varrimento | curva de retorno, volume ideal | 4.4 (volume Tutorial) |
| 5 | Arranjo | precisa de reservatório superior? | 4.5 (volume Tutorial) |
| 6 | Qualidade | classe, desinfeção, filtros | 4.6 (volume Tutorial) |
| 7 | Economia | tarifa real, CAPEX, fluxo de caixa | 4.7 (volume Tutorial) |
| 8 | Carbono | inventário, material, período de recuperação | 4.8 (volume Tutorial) |
| 9 | Decisão | oito critérios em quatro eixos, pesos declarados | 4.9 (volume Tutorial) |
| 10 | Relatório | saídas e lista de declaração | 4.10 (volume Tutorial) |

**Antes de publicar:** secção 4.10 (volume Tutorial), a lista de declaração. Secção 5.1 (volume Enganos, limitações e confiabilidade), os dez erros. Secção 5.2 (volume Enganos, limitações e confiabilidade), as limitações que afetam o seu caso.

---

### I.2. Ficha 2 — As armadilhas, em uma linha cada

<!-- tabela: **Tabela 54** — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada -->
| Armadilha | Onde |
| :--- | :--- |
| área **inclinada** em vez da projeção horizontal | 5.1.1 (volume Enganos, limitações e confiabilidade) |
| chuva **média mensal** em vez da série diária | 5.1.2 (volume Enganos, limitações e confiabilidade) |
| descarte em **litros** quando o campo quer milímetros | 5.1.3 (volume Enganos, limitações e confiabilidade) |
| **regime de mínimo** tarifário ignorado | 5.1.4 (volume Enganos, limitações e confiabilidade) |
| escola ou hospital com **tarifa residencial** | 5.1.5 (volume Enganos, limitações e confiabilidade) |
| esperar mais **água** do reservatório superior | 5.1.6 (volume Enganos, limitações e confiabilidade) |
| **série curta** demais | 5.1.7 (volume Enganos, limitações e confiabilidade) |
| classe de qualidade escolhida pelo **custo** | 5.1.8 (volume Enganos, limitações e confiabilidade) |
| comparar com **outro programa** sem declarar as diferenças de método | 5.1.9 (volume Enganos, limitações e confiabilidade) |
| publicar o volume de **maior economia** como recomendado | 5.1.10 (volume Enganos, limitações e confiabilidade) |

---

### I.3. Ficha 3 — Os seis regimes tarifários

<!-- tabela: **Tabela 55** — Ficha de consulta: os seis regimes tarifários e o efeito de poupar -->
| Regime | Ao poupar |
| :--- | :--- |
| sem mínimo | cada m³ desconta |
| tarifa de disponibilidade | cada m³ desconta; a parte fixa mantém-se |
| fórmula exponencial | cada m³ desconta; a conta é PB × Cⁿ + serviço básico |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** |
| franquia retroativa | passando-a, cobra tudo desde zero |
| piso de pagamento | a fatura não fica abaixo do piso |

**Teste rápido:** simule dois consumos, um dentro e outro fora do escalão mínimo, e compare-os com uma fatura
real. Se só um coincidir, o regime está errado.

Os tarifários de Lisboa, do Porto e do Funchal têm a estrutura da tarifa de disponibilidade com escalões
progressivos (apêndice D).

---

### I.4. Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: **Tabela 56** — Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | procura **total** | quanto do consumo de água potável cai |
| fiabilidade volumétrica | procura **pluvial** | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | dias da série | com que frequência se pode contar |
| extravasamento | — | o reservatório é pequeno? |
| ganho marginal | — | vale ampliar? |

`Epot = fiabilidade volumétrica × fração atendível`

---

### I.5. Ficha 5 — A cadeia de energia da eletrobomba

```
elevação:  e = ρ · g · H ÷ (η_bomba · η_motor)      kWh/m³
partidas:  E = placa × tempo ÷ η_motor              kWh
```

A placa é a potência **no eixo**. O rendimento do motor separa o eixo da tomada. Se o deixar
em branco, vale o valor típico para a potência nominal; introduza o rendimento do seu motor quando
tiver a ficha técnica.

---

### I.6. Ficha 6 — A lista de declaração, resumida

**Programa:** versão, com revisão.

**Chuva:** origem, recorte, anos; se projeção, modelo, cenário e janela.

**Edificação:** área e como foi obtida, coeficiente, per capita e origem, **fração
atendível** e os usos que a compõem.

**Descarte:** lâmina e modo; e a diferença de método, se comparar programas.

**Volume:** critério de escolha — limiar de ganho marginal, ou os quatro pesos
de eixo, as partes no eixo e os candidatos do multicritério.

**Economia:** concelho, entidade gestora, vigência da tabela, **regime de mínimo**,
regra do saneamento, taxas de IVA de cada parcela, taxa de atualização, inflação, atualizações e período, e a moeda.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores **aproximados** ou com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no LEED, a versão; no EDGE, que só a
barra de água foi avaliada.

---

## Apêndice J — Ficheiros de exemplo

O manual imprime resultados; estes ficheiros são o que se abre para
reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva
incorporada: abrem sem o CSV de origem, em qualquer computador. A chuva provém do
Iberia01 por município (1986–2015) para Lisboa e Porto, e da reanálise ERA5 de ilha para o Funchal,
que acompanham o programa (apêndice E); cada ficheiro traz o tarifário oficial da
sua localidade (apêndice D).

**Os custos são ilustrativos, não são preços de mercado.** Apenas os ficheiros do
tutorial de Lisboa (01, 04, 06, 09 e 10) trazem custos, em euros, com valores
arredondados que permitem acompanhar o método. Os restantes comparam chuva, procura e
tarifário, mantendo o investimento a zero. Antes de extrair qualquer conclusão económica,
introduza os seus próprios custos na etapa 5.

---

### J.1. Os casos do manual

<!-- tabela: **Tabela 57** — Os casos de exemplo e o que cada um demonstra -->
| Ficheiro | Secção | O que demonstra |
| :--- | :--- | :--- |
| `01_tutorial_lisboa.triton` | 4.1 a 4.10 | o projeto fechado do tutorial em Lisboa: cisterna de 5.000 L em polietileno e elevação para um reservatório superior de 1.000 L (custos ilustrativos, não são preços de mercado) |
| `02_porto.triton` | 3.1 | a moradia do tutorial levada ao Porto, com a chuva do Iberia01 no Porto e o tarifário da Águas e Energia do Porto (sem custos definidos) |
| `03_funchal.triton` | 3.1 | a moradia do tutorial levada ao Funchal, com a chuva ERA5 de ilha do Funchal (nível C), o tarifário da Câmara Municipal do Funchal e a eletricidade da EEM (sem custos definidos) |
| `04_tutorial_varredura.triton` | 4.4 e 2.2 | o projeto antes do reservatório superior, em modo varredura, de 0 a 20.000 L em passos de 1.000 L (Lisboa) |
| `05_dez_dias.triton` | 2.1 | o caso didático de dez dias, 15 a 24 de dezembro de 2013 da série de Lisboa, que cabe numa folha de cálculo |
| `06_reservatorio_superior.triton` | 4.5 | 5.000 L em baixo mais 1.000 em cima, a comparação da secção 4.5 contra os 6.000 L de um reservatório só (Lisboa) |
| `07_escola_semanal.triton` | 3.4 e 3.5 | uma escola do Porto, com 300 alunos e procura modulada por dia da semana |
| `08_hotel_mensal.triton` | 3.4 | um hotel de Lisboa com ocupação mensal ilustrativa, concentrada no verão seco |
| `09_modulacao_tutorial.triton` | 7.3 e 7.4 | a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, o tarifário e o investimento, mil realizações, semente 42 |
| `10_modulacao_captacao.triton` | 7.4 | a mesma varredura com a incerteza na captação (área, coeficiente de escoamento, descarte), o fator de chuva sobre a série de Lisboa, o tarifário e o investimento; mil realizações, semente 42 |

### J.2. O que cada um produz

Os valores abaixo são obtidos **relendo o ficheiro gravado** e simulando o
que foi relido, e não a configuração que o gerou. É a diferença que
importa: um parâmetro que não sobreviva à gravação aparece aqui como
número errado, em vez de passar despercebido.

<!-- tabela: **Tabela 58** — Resultado que cada caso de exemplo produz ao ser relido e simulado -->
| Ficheiro | Modo | Volume | Potencial | Pluvial consumida |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_lisboa.triton` | volume fixo | 5.000 L | 18,28% | 109,7 L/dia |
| `02_porto.triton` | volume fixo | 5.000 L | 21,58% | 129,5 L/dia |
| `03_funchal.triton` | volume fixo | 5.000 L | 12,86% | 77,1 L/dia |
| `04_tutorial_varredura.triton` | varredura | ideal: 5.000 L | 17,87% | 21 volumes |
| `05_dez_dias.triton` | volume fixo | 2.000 L | 30,55% | 61,1 L/dia |
| `06_reservatorio_superior.triton` | volume fixo | 5.000 L | 18,28% | 109,7 L/dia |
| `07_escola_semanal.triton` | volume fixo | 30.000 L | 21,83% | 1.968,0 L/dia |
| `08_hotel_mensal.triton` | volume fixo | 25.000 L | 10,34% | 865,3 L/dia |
| `09_modulacao_tutorial.triton` | varredura | ideal: 5.000 L | 17,87% | 21 volumes |
| `10_modulacao_captacao.triton` | varredura | ideal: 5.000 L | 17,87% | 21 volumes |

O caso 01 inclui o reservatório superior de 1.000 L, e o caso 06 compara-o com um único reservatório de 6.000 L, que obtém 18,59% (secção 4.5 (volume Tutorial)).

---

### J.3. Como abrir e simular

**Ficheiro, Abrir projeto**, escolha o ficheiro pretendido, e o programa carrega tudo:
a precipitação, a edificação, o tarifário, os custos e a configuração dos módulos de análise.
Percorra as etapas de resultado na barra lateral para analisar cada dimensão.

Os casos 09 e 10 abrem com a **Modulação Probabilística** configurada — as
variáveis, distribuições, número de realizações (1.000) e semente determinística (42) da
secção 7.4 (volume Modulação probabilística): vá à etapa 13 e clique em **Simular**. Ambos estão em modo varredura,
que permite traçar as curvas por volume; num caso de volume fixo, o módulo apresenta
apenas o volume de dimensionamento.

Os ficheiros situam-se na pasta `casos`, no diretório de instalação do programa.
Para modificá-los, **grave com outro nome**: dessa forma o ficheiro original continua a
reproduzir exatamente os números apresentados no manual.

---

### J.4. Os estudos de `exemplos`

Além dos casos didáticos do manual, o programa disponibiliza em `examples/portugal/` os
projetos de referência para Lisboa, Porto e Funchal, e em `examples/espanha/` os de Madrid e Palma (Baleares). Todos usam a
chuva do Iberia01 (1986–2015), por município e pelo código, exceto o Funchal, que usa a ERA5 de ilha (nível C, com aviso).
Permitem explorar a aplicação direta dos tarifários locais em moradias unifamiliares completas. Os limites dos de Espanha: a
tarifa de Madrid é a do Canal de Isabel II, transcrita e ainda não conferida; a de Palma é a média regional do INE (indicativa,
um preço total por metro cúbico), e não a da entidade gestora.

---

### J.5. O que estes ficheiros não são

Não são modelos fechados de projeto de execução. São **casos de demonstração metodológica**:
os custos do tutorial são estritamente ilustrativos, o tarifário de base é o de Lisboa e as
categorias refletem as condições domésticas convencionais. Num projeto real de engenharia,
introduza a série pluviométrica local, os orçamentos reais de fornecedores e a tabela tarifária
em vigor do município.
