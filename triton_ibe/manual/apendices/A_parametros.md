# Os parâmetros do projeto

São **119 parâmetros**. É a lista completa do que um projeto guarda nesta
edição, com o nome exato de cada campo dentro do ficheiro `.triton`.

A lista não foi transcrita à mão: é extraída do próprio programa a cada versão, e por
isso não pode divergir dele.

A coluna **onde se introduz** diz em que ecrã o campo aparece; a coluna **quem consome**
diz que cálculo o usa. Um campo sem nenhuma das duas é um campo gravado no ficheiro e
nunca lido, e está listado na secção {{n:36}}.

Os padrões são os do projeto com que a Edição Ibérica abre: a chuva é a normal 1986-2015
do município de Lisboa [PT-1106] no Iberia01, e os custos, os preços e a tarifa de eletricidade
partem de zero ou vazios, para o utilizador os introduzir em euros. Um traço significa
que o campo não tem valor inicial.

O ficheiro de projeto guarda ainda 4 campos de esquemas nacionais de outras
edições. Não têm efeito nesta e não são listados.

## Identificação

3 parâmetros.

<!-- tabela: Parâmetros do projeto: identificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | Novo projeto Triton | — | Exportação, Janela principal, Relatórios | Automação, CAD e BIM, Folhas de cálculo, Relatórios |
| `project_id` | — | — | Janela principal, Relatórios | Automação |
| `created_at` | — | — | Janela principal | — |

## Chuva

9 parâmetros.

<!-- tabela: Parâmetros do projeto: chuva -->
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

## Captação

7 parâmetros.

<!-- tabela: Parâmetros do projeto: captação -->
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

## Edificação

2 parâmetros.

<!-- tabela: Parâmetros do projeto: edificação -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | — | Ambiental, Edificação | Automação, Económico |
| `building_template_id` | res_medio | — | Edificação | Automação, Tarifário |

Observações do código:

- `num_economias`: Número de frações autónomas com contador individual

## Procura

17 parâmetros.

<!-- tabela: Parâmetros do projeto: procura -->
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

## Rega

4 parâmetros.

<!-- tabela: Parâmetros do projeto: rega -->
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

## Qualidade da água

9 parâmetros.

<!-- tabela: Parâmetros do projeto: qualidade da água -->
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

## Reservatórios

13 parâmetros.

<!-- tabela: Parâmetros do projeto: reservatórios -->
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

## Eletrobomba

18 parâmetros.

<!-- tabela: Parâmetros do projeto: eletrobomba -->
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

## Tubagem

1 parâmetro.

<!-- tabela: Parâmetros do projeto: tubagem -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Económico, Tarifário e custos | ACV, Automação |

## Investimento

3 parâmetros.

<!-- tabela: Parâmetros do projeto: investimento -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_piping` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, Económico |
| `cost_accessories` | 0 | — | Económico, Tarifário e custos, Varrimento | Automação, ETAP, Económico |

## Exploração

1 parâmetro.

<!-- tabela: Parâmetros do projeto: exploração -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Económico, Otimizador, Tarifário e custos, Varrimento | Automação, Económico |

## Tarifário

17 parâmetros.

<!-- tabela: Parâmetros do projeto: tarifário -->
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

## Energia

4 parâmetros.

<!-- tabela: Parâmetros do projeto: energia -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_city_name` | personalizado | — | Janela principal, Projeto, Tarifário e custos | — |
| `elec_tax_fixed` | 0 | — | Tarifário e custos | Automação, Económico |
| `elec_tax_var` | 0 | — | Tarifário e custos | Automação, Económico |

Observações do código:

- `elec_tax_fixed`: € por mês
- `elec_tax_var`: %

## Financeiro

4 parâmetros.

<!-- tabela: Parâmetros do projeto: financeiro -->
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

## Certificações

1 parâmetro.

<!-- tabela: Parâmetros do projeto: certificações -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | — | Ambiental | — |

## Outros

6 parâmetros.

<!-- tabela: Parâmetros do projeto: outros -->
| Parâmetro | Padrão | Unidade | Onde se introduz | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `phi_operation_rule` | — | — | Janela principal, Varrimento | Automação, Balanço diário, Folhas de cálculo |
| `data_base_estudo` | — | — | Tarifário e custos | — |
| `precos_de_catalogo` | não | — | Assistente da bomba, Económico, Otimizador, Qualidade, Tarifário e custos, Varrimento | Automação, ETAP, Preços |
| `bim_layout` | — | — | Exportação, Janela principal | — |
| `capex_do_arranjo` | não | — | Janela principal, Tarifário e custos, Varrimento | ETAP |
| `mao_de_obra_automatica` | não | — | Janela principal, Tarifário e custos, Varrimento | — |

