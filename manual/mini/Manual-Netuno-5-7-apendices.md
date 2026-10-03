# Netuno 5

## Manual do Usuário — Apêndices

Igor Catão Martins Vaz e Enedir Ghisi

Grupo de Pesquisa em Ambientes Sustentáveis
Universidade Federal de Santa Catarina

Florianópolis, 2026

---

### Sobre este volume

Este é um dos sete volumes em que o manual do Netuno 5 pode ser distribuído, e
reúne os apêndices do manual completo. Serve para mandar
só a parte que interessa: o método a um revisor, o tutorial a uma turma, os guias
a quem já usa o programa.

A numeração das seções e das equações é a mesma do manual completo, de modo que
uma remissão vale nos dois. Quando o texto remete a uma seção que está em outro
volume, o nome do volume vem entre parênteses.

| Volume | Conteúdo |
| :--- | :--- |
| Comece aqui | o capítulo 1 (Comece aqui) e o apêndice G |
| O método | o capítulo 2 (O método) e os apêndices A, B, C, E, G e H |
| Guias de uso | o capítulo 3 (Guias disponíveis no programa) e os apêndices D, F e G |
| Tutorial | o capítulo 4 (Tutorial: um exemplo do começo ao fim) e os apêndices G, I e J |
| Enganos, limitações e confiabilidade | o capítulo 5 (Enganos, limitações e confiabilidade) e os apêndices G e H |
| Correções, bugs e versionamento | o capítulo 6 (Correções, bugs e versionamento) |
| **Apêndices** | os apêndices |

### Como citar

> VAZ, Igor Catão Martins; GHISI, Enedir. **Netuno 5: manual do usuário**.
> Apêndices. Versão 5.0.0. Florianópolis: Universidade Federal de Santa
> Catarina, 2026.

---

## Sumário

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



## Lista de figuras

Figura 1 — Quanto de cada metro cúbico produzido chega efetivamente à edificação, por macrorregião

Figura 2 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião

---

## Lista de tabelas

Tabela 1 — Parâmetros do projeto: identificação

Tabela 2 — Parâmetros do projeto: chuva

Tabela 3 — Parâmetros do projeto: captação

Tabela 4 — Parâmetros do projeto: edificação

Tabela 5 — Parâmetros do projeto: demanda

Tabela 6 — Parâmetros do projeto: irrigação

Tabela 7 — Parâmetros do projeto: qualidade da água

Tabela 8 — Parâmetros do projeto: reservatórios

Tabela 9 — Parâmetros do projeto: motobomba

Tabela 10 — Parâmetros do projeto: tubulação

Tabela 11 — Parâmetros do projeto: investimento

Tabela 12 — Parâmetros do projeto: operação

Tabela 13 — Parâmetros do projeto: tarifas

Tabela 14 — Parâmetros do projeto: energia

Tabela 15 — Parâmetros do projeto: incentivos

Tabela 16 — Parâmetros do projeto: financeiro

Tabela 17 — Parâmetros do projeto: certificações

Tabela 18 — Parâmetros do projeto: outros

Tabela 19 — Fatores de emissão dos materiais de reservatório, com massa e fronteira

Tabela 20 — Fatores de emissão dos insumos de tratamento

Tabela 21 — Emissão de fabricação da motobomba por potência, com a massa de catálogo

Tabela 22 — Procedência do fator de emissão do hipoclorito

Tabela 23 — Distribuição dos municípios do catálogo pelos seis regimes tarifários

Tabela 24 — Grau de confiança dos registros tarifários do catálogo

Tabela 25 — Cobertura do catálogo tarifário: municípios por categoria e situação do dado

Tabela 26 — As estruturas tarifárias do catálogo, numeradas para as tabelas de preço por faixa que vêm a seguir

Tabela 27 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 1 de 3: 0–5 a 20–25 m³)

Tabela 28 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 2 de 3: 25–30 a 70–75 m³)

Tabela 29 — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 3 de 3: 75–80 a 5.000 m³)

Tabela 30 — Categorias tarifárias ainda não coletadas, por prestador

Tabela 31 — Vigência e última verificação da fonte de cada estrutura tarifária, com a situação do dado

Tabela 32 — A fórmula exponencial da CORSAN em cada tabela tarifária e categoria coletada

Tabela 33 — Conteúdo da base climática nacional

Tabela 34 — Séries históricas de precipitação distribuídas com o programa

Tabela 35 — Formatos que o programa lê e onde cada um é carregado

Tabela 36 — Formatos que o programa escreve e onde cada um é gerado

Tabela 37 — As sete seções do arquivo de projeto e o que cada uma guarda

Tabela 38 — Localização dos arquivos do programa e dos arquivos do usuário

Tabela 39 — Compatibilidade entre versões do arquivo de projeto

Tabela 40 — Padronização terminológica de água de chuva e água pluvial

Tabela 41 — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial

Tabela 42 — Ficha de consulta: os dez passos de um estudo completo e a seção que trata de cada um

Tabela 43 — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada

Tabela 44 — Ficha de consulta: os seis regimes tarifários e o efeito da economia

Tabela 45 — Ficha de consulta: os indicadores e a pergunta que cada um responde

Tabela 46 — Os nove casos de exemplo e o que cada um demonstra

Tabela 47 — Resultado que cada caso de exemplo produz ao ser relido e simulado

---


---
# Apêndices

---

## Apêndice A — Os parâmetros do projeto

São **116 parâmetros**. É a lista completa do que um projeto
guarda, com o nome exato de cada campo dentro do arquivo `.netuno`.

A lista não foi transcrita à mão: é extraída do próprio programa a cada
versão, e por isso não pode divergir dele.

A coluna **onde se informa** diz em que tela o campo aparece; a coluna
**quem consome** diz que cálculo o usa. Campo sem nenhuma das duas é campo
gravado no arquivo e nunca lido, e está listado na seção 5.2 (volume Enganos, limitações e confiabilidade).

### A.1. Identificação

3 parâmetros.

<!-- tabela: **Tabela 1** — Parâmetros do projeto: identificação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | Novo projeto Netuno | — | Exportação, Janela principal, Relatórios | Automação, CAD e BIM, Planilhas, Relatórios |
| `project_id` | — | — | Janela principal, Relatórios | Automação |
| `created_at` | — | — | Janela principal | — |

### A.2. Chuva

9 parâmetros.

<!-- tabela: **Tabela 2** — Parâmetros do projeto: chuva -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Janela principal, Projeto | Automação, Cenários, Planilhas |
| `climate_source_mode` | national_db | — | — | — |
| `climate_city_uf` | SC | — | Projeto, Relatórios | — |
| `climate_city_name` | Florianópolis | — | Projeto, Relatórios | — |
| `climate_model` | INM-CM4 | — | Projeto, Relatórios | — |
| `climate_scenario` | HIST | — | Projeto, Relatórios | — |
| `climate_start_date` | 01/01/1980 | — | Relatórios | — |
| `climate_end_date` | 31/12/2013 | — | Projeto, Relatórios | — |
| `start_date` | 01/01/1980 | — | Janela principal, Projeto, Tarifas e custos | Automação, Clima |

Observações do código:

- `climate_source_mode`: "national_db" (base nacional) ou "custom_file" (arquivo próprio)

### A.3. Captação

7 parâmetros.

<!-- tabela: **Tabela 3** — Parâmetros do projeto: captação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | — | mm | Ambiental, Documentação, Gráficos, Janela principal, Projeto, Qualidade, Relatórios | ACV, Automação, CAD e BIM, Cenários, ETAP, Planilhas, Relatórios |
| `discard_mode` | 1 | código | Janela principal, Projeto, Varredura | Automação, Balanço diário, Cenários |
| `discard_days_interval` | 7 | dias | Janela principal, Projeto, Varredura | Automação, Balanço diário, Cenários |
| `area` | 100 | m² | Ambiental, Documentação, Edificação, Gráficos, Janela principal, Qualidade, Relatórios, Varredura | ACV, Automação, Balanço diário, CAD e BIM, Cenários, ETAP, Planilhas, Relatórios |
| `irrigation_garden_area_m2` | 0 | m² | — | — |
| `runoff_coeff` | — | — | Edificação, Janela principal, Qualidade, Varredura | Automação, Balanço diário, Cenários, Planilhas |
| `first_flush_system_enabled` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `discard`: mm
- `discard_mode`: 1 = todos os eventos, 2 = 1º evento após estiagem, 3 = a cada X dias
- `discard_days_interval`: intervalo para modo 3
- `area`: m²
- `irrigation_garden_area_m2`: Área de jardim em m² para o assistente de dimensionamento
- `runoff_coeff`: ver hydrology_defaults

### A.4. Edificação

2 parâmetros.

<!-- tabela: **Tabela 4** — Parâmetros do projeto: edificação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | un | Ambiental, Edificação | Automação, Econômico |
| `building_template_id` | res_medio | — | Edificação | Automação, Tarifas |

Observações do código:

- `num_economias`: Número de economias / apartamentos com micromedição individual

### A.5. Demanda

17 parâmetros.

<!-- tabela: **Tabela 5** — Parâmetros do projeto: demanda -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `demand_type` | 0 | código | — | — |
| `demand_mode` | constant | — | Ambiental, Edificação, Janela principal, Relatórios, Varredura | Automação, Balanço diário |
| `demand_value` | 200 | L/dia | Documentação, Econômico, Janela principal | Automação, Balanço diário |
| `demand_monthly` | — | — | Janela principal | Automação |
| `residents_type` | 0 | código | — | — |
| `residents_count` | 4 | hab | Ambiental, Econômico, Janela principal | Automação, Balanço diário, Motobomba |
| `residents_monthly` | — | — | Janela principal | Automação |
| `potable_indoor_share` | 0,6 | fração | Edificação, Janela principal | Automação |
| `non_potable_indoor_share` | 0,4 | fração | Edificação, Janela principal | Automação, Balanço diário |
| `rainwater_share` | 0,4 | fração | Documentação, Janela principal, Varredura | Automação, Balanço diário, Cenários, Planilhas |
| `weekly_demands` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `weekly_residents` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `weekly_shares` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `monthly_shares` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `daily_demands` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `daily_residents` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |
| `daily_shares` | — | — | Edificação, Janela principal, Varredura | Automação, Balanço diário |

Observações do código:

- `demand_mode`: "constant", "weekly", "monthly", "daily"
- `demand_value`: L/dia, por habitante ou total
- `potable_indoor_share`: Fração potável do consumo interno; 1 − non_potable_indoor_share
- `non_potable_indoor_share`: Fração não potável do consumo interno (bacias, máquina); ver fracao_atendivel
- `rainwater_share`: fração de 0 a 1 (0,4 = 40%)

### A.6. Irrigação

4 parâmetros.

<!-- tabela: **Tabela 6** — Parâmetros do projeto: irrigação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `irrigation_liters_per_day` | 0 | L/dia | Ambiental, Edificação, Janela principal, Relatórios | Automação, Balanço diário |
| `irrigation_rain_threshold_mm` | 2 | mm/dia | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_potable_backup` | sim | — | Edificação, Janela principal | Automação, Balanço diário |
| `irrigation_rate_l_m2_day` | 3 | L/m²·dia | — | — |

Observações do código:

- `irrigation_liters_per_day`: Demanda externa (rega, lavagem de áreas externas), L/dia
- `irrigation_rain_threshold_mm`: Limiar diário de precipitação para supressão da irrigação (mm/dia)
- `irrigation_potable_backup`: Se True, a rede pública atende a irrigação em dias secos se a cisterna secar
- `irrigation_rate_l_m2_day`: Taxa diária de rega (L/m²/dia)

### A.7. Qualidade da água

9 parâmetros.

<!-- tabela: **Tabela 7** — Parâmetros do projeto: qualidade da água -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `water_quality_target_class` | classe_1 | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_disinfection` | cloro | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `water_quality_polishing` | não | — | Ambiental, Qualidade | ACV, Automação, ETAP |
| `etap_enabled` | sim | — | Ambiental, Econômico, Otimizador | ACV, Automação, ETAP |
| `chlorine_treatment_enabled` | sim | — | Ambiental, Econômico, Otimizador, Qualidade | ACV, Automação, Econômico |
| `chlorine_dose_mg_l` | — | mg Cl₂/L | Ambiental, Econômico, Otimizador, Qualidade | ACV, Automação, ETAP, Econômico, Relatórios |
| `chlorine_product_purity` | — | kg/kg | Ambiental, Qualidade | ACV, Automação, ETAP, Econômico |
| `chlorine_cost_per_kg` | 25 | R$/kg | Econômico, Otimizador, Qualidade | Automação, ETAP, Econômico, Preços |
| `chlorine_co2_kg_per_kg` | — | kg CO₂e/kg | Ambiental, Qualidade | ACV, Automação, ETAP |

Observações do código:

- `water_quality_disinfection`: "cloro", "uv", "ozonio", "nenhum"
- `chlorine_dose_mg_l`: mg de Cl2 ativo por litro
- `chlorine_product_purity`: kg Cl2 ativo por kg de produto
- `chlorine_cost_per_kg`: R$ por kg de PRODUTO comercial

### A.8. Reservatórios

12 parâmetros.

<!-- tabela: **Tabela 8** — Parâmetros do projeto: reservatórios -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | L | Ambiental, Assistente da bomba, Caixa superior, Econômico, Exportação, Janela principal, Otimizador, Relatórios, Tarifas e custos, Varredura | Automação, Balanço diário, CAD e BIM, Cenários, Multicritério, Planilhas |
| `upper_tank_used` | 1 | código | Ambiental, Econômico, Janela principal, Otimizador, Relatórios, Tarifas e custos, Varredura | ACV, Automação, Balanço diário, Cenários, Motobomba, Planilhas |
| `lower_tank_max` | 10000 | L | Janela principal, Varredura | Automação, Balanço diário, Cenários, Planilhas |
| `lower_tank_step` | 250 | L | Janela principal, Varredura | Automação, Balanço diário, Cenários, Planilhas |
| `lower_tank_mode` | 1 | código | Janela principal, Varredura | Automação |
| `lower_tank_fixed` | 2000 | L | Janela principal, Tarifas e custos, Varredura | Automação |
| `delta_ideal` | 5 | %/m³ | Janela principal, Otimizador, Varredura | Automação, Cenários |
| `econ_lower_tank_vol` | 2000 | L | Ambiental, Econômico, Tarifas e custos, Varredura | Automação |
| `lower_tank_material` | PEAD | — | Econômico, Otimizador, Tarifas e custos | ACV, Automação |
| `upper_tank_material` | PEAD | — | Econômico, Otimizador, Tarifas e custos | ACV, Automação |
| `cost_lower_tank` | 0 | R$ | Econômico, Tarifas e custos, Varredura | Automação, Econômico |
| `cost_upper_tank` | 0 | R$ | Econômico, Tarifas e custos, Varredura | Automação, Econômico |

Observações do código:

- `upper_tank_vol`: L
- `upper_tank_used`: 0 = sem caixa superior, 1 = com caixa superior
- `lower_tank_max`: L
- `lower_tank_step`: L
- `lower_tank_mode`: 0 = volume fixo, 1 = varredura
- `lower_tank_fixed`: usado no modo de volume fixo
- `delta_ideal`: limiar de ganho marginal para o volume ideal, em %/m³
- `lower_tank_material`: "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"
- `upper_tank_material`: "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"

### A.9. Motobomba

18 parâmetros.

<!-- tabela: **Tabela 9** — Parâmetros do projeto: motobomba -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pumping_threshold` | 50 | L | Janela principal, Varredura | Automação, Balanço diário, Cenários, Planilhas |
| `supply_arrangement` | — | código | Ambiental, Econômico, Varredura | ACV, Automação, Econômico, Motobomba |
| `pressurizer_pressure_m` | 18 | m.c.a. | Varredura | Motobomba |
| `pressurizer_starts_per_person_day` | 5,05 | 1/pessoa·dia | Varredura | Motobomba |
| `pressurizer_model` | komeco_tp820t | código | Varredura | Motobomba |
| `pressurizer_point_flow_l_min` | 9 | L/min | Varredura | Motobomba |
| `pressurizer_power_kw` | 0,18 | kW | Varredura | Motobomba |
| `pressurizer_flow_l_min` | 13,3 | L/min | Varredura | Motobomba |
| `pressurizer_post_run_s` | 0 | s | Varredura | Motobomba |
| `pump_count` | 2 | un | Ambiental, Econômico, Otimizador, Relatórios, Tarifas e custos | ACV, Automação, Econômico, Preços, Relatórios |
| `pump_power_str` | 1/2 | — | Relatórios | — |
| `pump_power_kw` | 0,36775 | kW | Econômico, Gráficos, Otimizador, Relatórios, Tarifas e custos, Varredura | Automação, CAD e BIM, Econômico, Motobomba, Preços, Relatórios |
| `pump_manometric_head_m` | 0 | m.c.a. | Varredura | Automação, Motobomba |
| `pump_efficiency` | 0 | % | Gráficos, Tarifas e custos, Varredura | Automação, Motobomba |
| `pump_flow_rate` | 0 | L/h | Econômico, Gráficos, Otimizador, Relatórios, Tarifas e custos, Varredura | Automação, Motobomba |
| `pump_startup_time_h` | 0,03 | h | Econômico, Gráficos, Otimizador, Tarifas e custos | Automação, Motobomba |
| `pump_motor_efficiency` | 0 | % | Tarifas e custos | Automação, Motobomba |
| `pump_unit_cost` | 300 | R$ | Econômico, Otimizador, Tarifas e custos, Varredura | Automação, Econômico, Preços |

Observações do código:

- `pumping_threshold`: L, nível de acionamento do recalque
- `pump_count`: principal + reserva como configuração inicial recomendada
- `pump_power_kw`: kW (1 CV = 0,7355 kW; 1/2 CV = 0,36775 kW)
- `pump_efficiency`: %, 0 = deduzir do porte
- `pump_startup_time_h`: h
- `pump_motor_efficiency`: %
- `pump_unit_cost`: R$, referência de mercado para motobomba periférica 1/2 CV

### A.10. Tubulação

1 parâmetro.

<!-- tabela: **Tabela 10** — Parâmetros do projeto: tubulação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Econômico, Tarifas e custos | ACV, Automação |

### A.11. Investimento

3 parâmetros.

<!-- tabela: **Tabela 11** — Parâmetros do projeto: investimento -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | R$ | Econômico, Tarifas e custos, Varredura | Automação, Econômico |
| `cost_piping` | 0 | R$ | Econômico, Tarifas e custos, Varredura | Automação, Econômico |
| `cost_accessories` | 0 | R$ | Econômico, Tarifas e custos, Varredura | Automação, ETAP, Econômico |

### A.12. Operação

1 parâmetro.

<!-- tabela: **Tabela 12** — Parâmetros do projeto: operação -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Econômico, Otimizador, Tarifas e custos, Varredura | Automação, Econômico |

### A.13. Tarifas

15 parâmetros.

<!-- tabela: **Tabela 13** — Parâmetros do projeto: tarifas -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | não | — | Projeto | — |
| `water_tariffs` | — | — | Projeto, Tarifas, Tarifas e custos, Varredura | Econômico |
| `tariff_city_uf` | SC | — | Janela principal, Projeto, Relatórios, Tarifas, Tarifas e custos | — |
| `tariff_city_name` | Florianópolis | — | Janela principal, Projeto, Relatórios, Tarifas, Tarifas e custos | — |
| `tariff_category` | residencial | — | Econômico, Tarifas, Tarifas e custos | Tarifas |
| `sewage_rate` | 100 | % da água | Projeto, Tarifas, Tarifas e custos | Automação, Econômico, Tarifas |
| `sewage_mode` | 1 | código | Econômico, Otimizador, Projeto, Tarifas, Tarifas e custos | Automação, Econômico, Tarifas |
| `water_tax_fixed` | 0 | R$/mês | Tarifas e custos | Automação, Econômico |
| `water_tax_var` | 0 | % | Tarifas e custos | Automação, Econômico |
| `tariff_escalation` | 12 | meses | Econômico, Otimizador, Tarifas e custos, Varredura | Automação, Econômico |
| `water_tariff_escalation` | 5 | % por período | Econômico, Otimizador, Varredura | Automação, Econômico |
| `sewage_tariff_escalation` | 5 | % por período | Econômico, Otimizador | Automação, Econômico |
| `elec_tariff_escalation` | 5 | % por período | Econômico, Otimizador, Varredura | Automação, Econômico |
| `tariff_flag` | verde | — | Econômico | Automação, Econômico |
| `elec_tariff` | 0,6957 | R$/kWh | Econômico, Gráficos, Otimizador, Projeto, Tarifas e custos, Varredura | Automação, Econômico |

Observações do código:

- `tariff_category`: categoria da tabela tarifária aplicada; "personalizada" quando digitada
- `sewage_mode`: 0 = valor fixo em R$, 1 = percentual da parcela de água, 2 = R$/m³ consumido
- `water_tax_fixed`: R$
- `water_tax_var`: %
- `tariff_escalation`: meses; comprimento do período de reajuste
- `water_tariff_escalation`: % por período de reajuste; com 12 meses, % ao ano
- `sewage_tariff_escalation`: % por período de reajuste; com 12 meses, % ao ano
- `elec_tariff_escalation`: % por período de reajuste; com 12 meses, % ao ano
- `tariff_flag`: "verde", "amarela", "vermelha_1", "vermelha_2", "branca"
- `elec_tariff`: R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)

### A.14. Energia

4 parâmetros.

<!-- tabela: **Tabela 14** — Parâmetros do projeto: energia -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | SC | — | Janela principal, Projeto, Tarifas e custos | — |
| `elec_city_name` | Florianópolis | — | Janela principal, Projeto, Tarifas e custos | — |
| `elec_tax_fixed` | 0 | R$/mês | Tarifas e custos | Automação, Econômico |
| `elec_tax_var` | 0 | % | Tarifas e custos | Automação, Econômico |

Observações do código:

- `elec_tax_fixed`: R$
- `elec_tax_var`: %

### A.15. Incentivos

3 parâmetros.

<!-- tabela: **Tabela 15** — Parâmetros do projeto: incentivos -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `iptu_green_enabled` | não | — | Econômico, Otimizador | Automação, Econômico |
| `iptu_annual_value` | 4000 | R$/ano | Econômico, Otimizador | Automação, Econômico |
| `iptu_discount_pct` | 5 | % | Econômico, Otimizador | Automação, Econômico |

Observações do código:

- `iptu_annual_value`: Valor venal do IPTU anual da edificação (R$/ano)
- `iptu_discount_pct`: Desconto municipal do IPTU Verde (%)

### A.16. Financeiro

4 parâmetros.

<!-- tabela: **Tabela 16** — Parâmetros do projeto: financeiro -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0,2 | % ao mês | Documentação, Econômico, Otimizador, Tarifas e custos, Varredura | Automação, Econômico |
| `analysis_period_years` | 20 | anos | Econômico, Otimizador, Relatórios, Tarifas e custos, Varredura | ACV, Automação, Econômico, Relatórios |
| `tma` | 2 | % ao mês | Econômico, Otimizador, Tarifas e custos, Varredura | Automação, Econômico, Planilhas |
| `install_month` | 0 | mês | — | — |

Observações do código:

- `inflation`: % ao mês; inflação dos custos de O&M
- `analysis_period_years`: anos
- `tma`: % ao mês; taxa mínima de atratividade

### A.17. Certificações

1 parâmetro.

<!-- tabela: **Tabela 17** — Parâmetros do projeto: certificações -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | L/pessoa·dia | Ambiental | — |

### A.18. Outros

3 parâmetros.

<!-- tabela: **Tabela 18** — Parâmetros do projeto: outros -->
| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `bim_layout` | — | — | Exportação, Janela principal | — |
| `capex_do_arranjo` | não | — | Janela principal, Tarifas e custos, Varredura | ETAP |
| `mao_de_obra_automatica` | não | — | Janela principal, Tarifas e custos, Varredura | — |

---

## Apêndice B — Os processos do programa

São **24 processos**, do arquivo de chuva ao relatório. Cada
um declara o que o dispara, o que recebe, as regras com suas ramificações, o
que produz e o que acontece quando falha.

É o apêndice mais técnico do manual, e serve a duas pessoas: quem revisa um
estudo feito com o programa e precisa saber exatamente que conta foi feita, e
quem encontrou um resultado estranho e quer saber por onde o número passou.

Os nomes em `código` são os campos do arquivo de projeto, listados no apêndice A.

### B.1. PROC-01 — Carregar a série de precipitação

*Chuva*

**Gatilho.** Aba Projeto: escolher cidade na base nacional ou abrir arquivo CSV.

**Entradas**

- Arquivo CSV diário, ou cidade da base CMIP6 (652 cidades, 19 modelos, histórico mais SSP2-4.5 e SSP5-8.5)
- `climate_start_date` e `climate_end_date`, que recortam a série
- `start_date`, data do primeiro dia da série

**Regras**

1. A série vira um vetor `numpy` de milímetros por dia; o índice do vetor é o dia, e a data serve só para saber o dia da semana e o mês.
2. Ano incompleto é descartado na leitura, para não enviesar totais anuais.
3. A base climática vai embutida na Edição Brasil, em `climbra.db`; na International Edition, que não a traz, a série é sempre um arquivo do usuário.

**Saídas**

- `precip_data`: vetor de mm/dia, que é a entrada de **dois** processos distintos — PROC-04 (descarte e captação) e PROC-03 (supressão de irrigação)

**Exceção.** Arquivo ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; a simulação não roda com série vazia.

### B.2. PROC-02 — Compor a demanda diária

*Demanda*

**Gatilho.** Início da simulação, uma vez por execução.

**Entradas**

- `demand_mode`: constante, semanal, mensal ou diária
- `demand_value` (L/dia por pessoa), `residents_count`
- `rainwater_share` ou `non_potable_indoor_share`
- vetores `weekly_*`, `monthly_*`, `daily_*` quando o modo os usa

**Regras**

1. Demanda-base do dia = `demand_value × residents_count`, com o multiplicador do dia da semana, do mês ou do dia, conforme o modo.
2. A fração não potável separa a demanda em duas: interna potável e interna não potável.
3. Quando o modo é semanal, mensal ou diário, a fração vem do próprio vetor do período; fora disso, vale `non_potable_indoor_share`, e só então `rainwater_share`.
4. Valor nulo ou zero em qualquer posição do vetor cai para o valor constante.

**Saídas**

- `tot_arr`: demanda total do dia
- `pot_in_arr`: potável interna, que a chuva nunca atende
- `non_pot_in_arr`: não potável interna, prioridade 1 da chuva
- `pluv_arr` = não potável interna + irrigação ativa

**Exceção.** Data inicial ilegível cai para 01/01/1980 em vez de interromper, porque só afeta o dia da semana.

### B.3. PROC-03 — Suprimir a irrigação nos dias de chuva

*Demanda*

**Gatilho.** Composição da demanda, um teste por dia da série.

**Entradas**

- `irrigation_liters_per_day`
- `irrigation_rain_threshold_mm` (padrão 2 mm/dia)
- `precip_data`, o **mesmo** vetor que alimenta a captação

**Regras**

1. Se a chuva do dia ≥ limiar, a irrigação do dia é **zero** e o dia entra na contagem de dias suprimidos.
2. Caso contrário, a irrigação do dia é o volume nominal.
3. É a segunda leitura do arquivo de chuva, e independente da primeira: um dia pode suprimir a irrigação e ainda assim render captação.

**Saídas**

- `irr_arr`: irrigação do dia
- `irr_suppressed_mask`: dias suprimidos, que viram `total_irrigation_days_suppressed` no resultado

**Exceção.** Sem volume de irrigação cadastrado, o vetor é zero e a máscara é falsa em todos os dias.

### B.4. PROC-04 — Descartar as primeiras águas

*Balanço hídrico*

**Gatilho.** Todo dia com chuva, dentro do laço diário.

**Entradas**

- `precip_mm` do dia
- `discard_mm`
- `discard_mode` (1, 2 ou 3)
- `discard_days_interval`

**Regras**

1. **Modo 1**: descarta em todo evento de chuva.
2. **Modo 2**: descarta apenas no primeiro evento após estiagem, definida como véspera com menos de 1 mm.
3. **Modo 3**: descarta quando passaram `discard_days_interval` dias desde o último descarte.
4. Quando o descarte se aplica: `p_eff = p − discard_mm` se `p > discard_mm`, senão **zero**: toda a chuva do dia vai para o descarte.
5. Quando não se aplica: `p_eff = p`, a chuva inteira é aproveitável.

**Saídas**

- `p_eff`: lâmina efetiva do dia, em mm, que segue **só** para PROC-05
- `eff_precip_mm` na série diária detalhada, quando ela é guardada

**Exceção.** Lâmina de descarte negativa é rejeitada na porta de validação, antes do laço.

### B.5. PROC-05 — Converter lâmina em volume captado

*Balanço hídrico*

**Gatilho.** Todo dia, depois do descarte.

**Entradas**

- `p_eff` de PROC-04
- `area` (m²)
- `runoff_coeff`

**Regras**

1. `v_ac = p_eff × area × runoff_coeff`, em litros.
2. É aqui que o arquivo de chuva vira volume, e é o único ponto onde isso acontece.
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

1. **Extravasamento antes do consumo**, como na regra YAS; a chuva do dia, até a capacidade, já atende a demanda do dia, o que põe o modelo entre a YAS e a YBS estritas.
2. `disponível = v_lower + v_ac`. Se passar da capacidade, o excedente extravasa e o reservatório fica cheio.
3. A ordem importa: retirar a demanda antes faria o reservatório aceitar água que fisicamente já teria extravasado, superestimando o aproveitamento.

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

1. `v_c = min(demanda pluvial, volume no reservatório)`.
2. O volume remanescente permanece para o dia seguinte: `v_lower = v_in_tank − v_c`.

**Saídas**

- `v_c`: volume pluvial consumido no dia

**Exceção.** Nenhuma: o mínimo já trata reservatório vazio e demanda nula.

### B.8. PROC-08 — Atender com recalque para caixa superior

*Balanço hídrico*

**Gatilho.** Todo dia, quando `upper_tank_used` e o volume superior é positivo.

**Entradas**

- `v_lower`, `v_upper`
- `upper_tank_vol`
- `pumping_threshold`, o volume de reserva que não se consome

**Regras**

1. Laço até a demanda ser atendida ou a água acabar.
2. Primeiro consome da caixa superior o que estiver **acima** do limiar de acionamento.
3. Se ainda falta e há água embaixo, aciona a bomba: transfere `min(v_lower, espaço livre em cima)`, conta **um ciclo** e registra a batelada.
4. Depois do recalque, consome de novo.
5. O limiar é limitado ao volume da caixa superior na entrada do processo.

**Saídas**

- `v_c`
- `v_rec_today`, somado em `total_pumped_liters`
- `cycles_today`, somado em `total_pump_cycles`
- `max_pump_batch_liters`

**Exceção.** Volume superior negativo é rejeitado na validação. O laço tem saída garantida: se não há água embaixo nem em cima, interrompe.

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
2. **Prioridade 2**, irrigação: `c_pluv_irr = min(v_c − c_pluv_in, irrigação do dia)`.
3. O potável consumido é a soma de três parcelas: o potável interno, o déficit do não potável interno e — só se o suprimento de reserva estiver ligado — o déficit da irrigação.
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

1. **Pleno** quando o consumido iguala a demanda pluvial, com tolerância de 10⁻⁵ L.
2. **Parcial** quando consumiu algo, mas menos que a demanda.
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
- demanda diária
- fração pluvial

**Regras**

1. Volume negativo, área negativa, descarte negativo e demanda negativa são recusados.
2. Coeficiente de escoamento e fração pluvial têm de ficar em [0, 1].
3. **Volume zero continua válido**: é a referência «sem sistema» da varredura.
4. A mensagem nomeia o campo e o valor recebido, em vez de corrigir por baixo dos panos.

**Saídas**

- Nenhuma saída: ou passa, ou levanta `ValueError`

**Exceção.** É o próprio tratamento. Antes desta porta, volume de −1.000 L devolvia −166,67% de economia, e o número seguia para o econômico, para a ACV e para o relatório.

### B.12. PROC-12 — Agregar o período e calcular os indicadores

*Balanço hídrico*

**Gatilho.** Fim do laço diário.

**Entradas**

- acumuladores do laço
- `n_days`

**Regras**

1. **Potencial de economia** = pluvial consumido no período ÷ demanda total do período × 100.
2. As médias diárias dividem os acumulados pelo número de dias simulados.
3. As conversões para o ano usam **365,25** dias, e não 365, para absorver os bissextos da série.
4. O potencial fica sempre em [0, 100] — invariante que a porta de validação existe para garantir.

**Saídas**

- `SingleTankSimulationResult`, com 21 campos, que é o objeto que **todos** os módulos a jusante consomem

**Exceção.** Demanda total nula devolve potencial zero em vez de dividir por zero.

### B.13. PROC-13 — Varrer volumes e achar o volume ideal

*Balanço hídrico*

**Gatilho.** Aba Varredura: botão de simular.

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

- `SweepSimulationResult`: um resultado por volume, o volume ideal, e o registro de que o passo foi ajustado
- A lista de volumes é a lista de **candidatos** do multicritério

**Exceção.** Passo maior que o máximo devolve grade com um ponto. O ajuste do passo é registrado em `step_adjusted`, e não silenciado.

### B.14. PROC-14 — Calcular os índices pluviométricos

*Chuva*

**Gatilho.** Aba Gráficos e relatório científico.

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

**Gatilho.** Mudança na aba Qualidade da Água, ou início do econômico e da ACV.

**Entradas**

- `water_quality_target_class` (4 classes de uso)
- `water_quality_disinfection`: cloro, ultravioleta ou ozônio
- `water_quality_polishing`, filtro de polimento
- `annual_pluvial_m3` de PROC-12
- `area`
- dose, pureza, preço e fator de CO₂ do cloro
- `discard` e `first_flush_system_enabled`, para o descarte inicial

**Regras**

1. A classe alvo define as etapas obrigatórias; a desinfecção escolhida define o equipamento e o custeio.
2. O filtro de polimento é aplicado **se e somente se** marcado; quando a classe o recomendaria e o usuário recusa, isso fica registrado em `polishing_recommended_but_declined` em vez de ser imposto.
3. O que se compra é o **produto** — pastilha a 65% de cloro ativo — e não o cloro puro. Faturar a massa de cloro ativo, e não a do produto, subestima o custo em cerca de 35%.
4. **Regra incremental**: o CAPEX da linha desconta a verba genérica de tratamento já embutida em «Acessórios», e o custeio desconta a cloração, que o fluxo de caixa já paga. A regra vive num lugar só, consumida pelos **dois** motores econômicos.
5. Com `first_flush_system_enabled`, o dispositivo de descarte inicial, de volume `discard × area`, entra no CAPEX e no custeio da linha.
6. Na ACV, a linha de tratamento **substitui** o termo de cloração; nunca soma a ele.
7. Com `etap_enabled = False`, a linha de tratamento não entra em conta alguma: nem no CAPEX, nem no custeio, nem na avaliação ambiental.

**Saídas**

- `total_etap_capex`, que entra no CAPEX
- `total_etap_annual_opex`, que entra no custeio
- `total_etap_co2e_kg_yr`, que substitui a cloração na ACV
- `disinfection_stages`, exibido no relatório

**Exceção.** Pureza fora de (0, 1] é recusada pelo validador da cadeia de cloração.

### B.16. PROC-16 — Calcular a energia de bombeamento

*Motobomba*

**Gatilho.** Econômico e ACV, a partir do mesmo resultado de simulação.

**Entradas**

- `supply_arrangement`: recalque, pressurização direta ou gravidade
- `total_pumped_liters` e `total_pump_cycles` de PROC-08
- `pressurizer_pressure_m`, `pressurizer_starts_per_person_day`, `residents_count`
- `pump_power_kw`, `pump_efficiency`, `pump_flow_rate`
- `pump_manometric_head_m`
- `pump_startup_time_h`

**Regras**

1. O arranjo decide o que se bombeia. **Recalque**: o volume enviado à caixa superior. **Pressurização direta**: todo o volume pluvial consumido, com a pressão de trabalho no lugar da altura e sem energia de partida. **Gravidade**: nada. É a única fonte de kWh do econômico e da ACV.
2. Energia específica `e = ρgH/(η_bomba·η_motor)` por m³ recalcado, ou `P/(Q·η_motor)` quando a vazão é declarada.
3. A potência de placa é potência de eixo e **já embute** o rendimento da bomba; por isso `P × horas / η_bomba` conta esse rendimento duas vezes, e o que falta é dividir pelo rendimento do motor, da ABNT NBR 17094-2. Quatro cópias dessa fórmula antiga sobreviviam no programa e superestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no multicritério.
4. A energia de partida entra à parte, pelo número de ciclos.
5. Vazão e rendimento não informados caem para valores típicos **da potência escolhida**, e não para constantes fixas.

**Saídas**

- `annual_kwh`, que vira custo no econômico e emissão na ACV
- `pump_hours_year`, `annual_cycles`

**Exceção.** Arranjo por gravidade, arranjo não informado num projeto antigo, ou potência zero: a energia é zero.

### B.17. PROC-17 — Calcular a fatura de água e esgoto

*Econômico*

**Gatilho.** Duas vezes por mês de projeção: com e sem aproveitamento.

**Entradas**

- volume mensal em litros
- `water_tariffs`: quádruplas (mínimo, máximo, valor, código)
- `sewage_mode` e `sewage_rate`
- impostos fixo e variável
- `num_economias`

**Regras**

1. O consumo é avaliado **no patamar de uma economia** e multiplicado pelo número de economias, para não distorcer as faixas progressivas em prédio com micromedição.
2. Código **1** ou **0**: faixa progressiva, cobrada só sobre o volume dentro dela.
3. Código **−1**, disponibilidade: valor fixo que **soma** por cima do consumo medido.
4. Código **−2**, franquia retroativa: até o volume da franquia paga-se o valor fixo; passando dele, **todo** o volume desde zero é tarifado pelas faixas.
5. Código **−3**, piso de pagamento: não soma, **limita por baixo**. Com piso de R$ 40 e consumo tarifado de R$ 55, economizar até R$ 15 não reduz nada — e é exatamente isso que um estudo de aproveitamento pluvial precisa enxergar.
6. O esgoto é percentual da **parcela de água**, não da fatura total. Em Florianópolis são 100% da água, que é metade da fatura.
7. Os seis regimes tarifários estão nomeados e auditados na base dos 652 municípios.

**Saídas**

- Valor da fatura de água e esgoto em R$/mês, para a projeção de PROC-18

**Exceção.** Tabela vazia cai para a estrutura da CASAN. Estrutura incompleta é sinalizada pela porta de validação, que separa erro de aviso.

### B.18. PROC-18 — Projetar o fluxo de caixa

*Econômico*

**Gatilho.** Aba Econômico, após a simulação técnica.

**Entradas**

- CAPEX das cinco rubricas mais bomba e ETAP
- economia mensal de água e esgoto de PROC-17
- custeio: bombeamento, cloração, ETAP e custos operacionais declarados
- `tma`, `inflation`, `analysis_period_years`
- reajustes separados de água, esgoto e energia, e o intervalo entre reajustes
- IPTU verde, quando habilitado

**Regras**

1. Água e esgoto são reajustados por índices **separados**, e não pela fatura agregada.
2. A inflação incide só sobre o custeio; os reajustes tarifários incidem só sobre a fatura.
3. O reajuste é aplicado a cada `tariff_escalation` meses, em degraus.
4. A bandeira tarifária ajusta a tarifa de energia: amarela, vermelha 1, vermelha 2, ou desconto fora de ponta na branca.
5. O IPTU verde entra como economia anual dividida por doze.
6. O payback é o primeiro mês em que o acumulado descontado cruza zero.

**Saídas**

- `vpl`, `tir_monthly_pct`, `tir_annual_pct`, `payback_months`
- `monthly_cash_flows`, série mês a mês
- `annual_pump_kwh`, `annual_chlorine_kg`, `etap_capex_brl`

**Exceção.** Economia mensal negativa é truncada em zero antes de entrar no fluxo. TIR sem raiz real devolve nulo em vez de um número inventado.

### B.19. PROC-19 — Avaliar o ciclo de vida

*ACV*

**Gatilho.** Aba Ambiental, após a simulação técnica.

**Entradas**

- `tank_vol_liters`
- `annual_pluvial_m3` de PROC-12
- materiais e massas dos dois reservatórios
- comprimentos por diâmetro de tubo
- `pump_count`
- fator da rede elétrica
- rota de produção da água potável
- resultado da ETAP de PROC-15

**Regras**

1. Sete etapas: cisterna inferior, caixa superior, tubulação, motobomba, operação de bombeamento, operação de tratamento e potável evitada.
2. Volume zero **sem** volume pluvial é o cenário sem sistema, e não recebe impacto fixo de caixa, tubo ou bomba.
3. A linha de tratamento **substitui** o termo de cloração; não soma a ele. A cloração acompanha o tratamento, e não a caixa superior.
4. Caixa superior só no arranjo de recalque; motobombas em todo arranjo com bomba; energia de PROC-16.
5. A água evitada é a **entregue**, não a produzida: as perdas de distribuição no Brasil vão de 33,9% no Sudeste a 46,9% no Norte, de modo que produzir 1 m³ entrega de 0,53 a 0,66 m³. O fator publicado de 0,236 kg CO₂e/m³ é de saída de estação; por m³ entregue vira de 0,336 a 0,461 conforme a macrorregião.
6. O payback de carbono é o carbono incorporado dividido pela economia anual líquida; sem economia líquida positiva, devolve 999 anos em vez de infinito.

**Saídas**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, que é critério do multicritério
- `environmental_payback_years`
- `inventory_items`, o inventário item a item

**Exceção.** Fator sem procedência primária recebe rótulo de triagem, e o rótulo é exibido — a lacuna é declarada, não escondida.

### B.20. PROC-20 — Enquadrar nas certificações

*ESG e certificações*

**Gatilho.** Aba Ambiental e relatórios.

**Entradas**

- `potential_potable_savings_pct`
- volume pluvial e potável anuais
- repartição interno/externo de PROC-09
- CO₂ evitado no ciclo de vida
- `area`, para a área de captação da WEM14
- caso-base do EDGE, quando declarado

**Regras**

1. **LEED v4**: WEc1 até 2 pontos pelo uso externo, WEc2 até 6 pontos pelo uso interno, pela escala oficial. Sem demanda externa cadastrada, WEc1 é zero e diz por quê.
2. **LEED v5 BD+C** (rating system de novembro de 2025): WEc2 até 8 pontos, pela Opção 1 (projeto inteiro, 30% a 65%, +1 com fonte alternativa) ou pela soma das Opções 2 (louças e metais, 30% a 40%), 4 (externo, 50% e 100%) e 6 (reúso no lote, 2 pontos), só em construção nova. SSc3 registrado como não avaliado; o ponto de reúso dele não ultrapassa o teto de 3.
3. **AQUA-HQE Residencial** (referencial de 22/11/2024): itens EAU.1.2 (HQE, 20% de economia), EAU.1.3 (HQE 3, 40%) e EAU.1.5 (HQE 3, existência de sistema pluvial).
4. **Casa Azul + CAIXA** (guia V023, 29/04/2026): critério 3.6 atendido pela existência do sistema; 2, 4 ou 5 pontos conforme a abrangência do uso, só quando informada.
5. **EDGE**: **não pontua**. Mede percentual contra um caso-base local e compara com 20%, em três barras independentes. O nível avançado sobe a barra de *energia* para 40%, e não a de água. O programa avalia só a barra de água, pela medida WEM14, e diz que as outras duas estão fora do seu alcance.
6. Sem caso-base declarado, o EDGE usa a demanda modelada e avisa que o número é **piso**.
7. **GRI 303**: captação evitada e taxa de circularidade.

**Saídas**

- `credit_details`: a matriz de créditos que alimenta a tabela da tela e os relatórios
- `esg_summary_text`
- cartões de LEED, AQUA, Casa Azul, EDGE e GRI

**Exceção.** Demanda total nula devolve zero por cento sem dividir por zero.

### B.21. PROC-21 — Ordenar volumes por múltiplos critérios

*Multicritério*

**Gatilho.** Aba Otimizador, com a varredura pronta.

**Entradas**

- um candidato por volume da varredura, cada um com potencial, extravasamento, VPL, payback descontado, TIR, CO₂ de ciclo de vida e consumo de potável
- pesos dos sete critérios

**Regras**

1. Sete critérios: **maximizar** potencial, VPL e TIR; **minimizar** extravasamento, payback, CO₂ e consumo de potável.
2. A normalização translada por `x − min(x)` **antes** da normalização vetorial de Hwang e Yoon, para admitir VPL negativo. É variante deliberada, e precisa ser declarada como variante.
3. O SMAA-VIKOR sorteia pesos e devolve as probabilidades de cada volume ocupar cada posição.
4. As condições C1 e C2 de Opricovic não estão implementadas.

**Saídas**

- Ordenação dos volumes, distância ao ideal por critério, volume de compromisso

**Exceção.** Candidato único devolve ordenação trivial. Critério constante entre candidatos não contribui para a distância.

### B.22. PROC-22 — Gravar e reabrir o projeto

*Arquivo do projeto*

**Gatilho.** Menu de salvar e de abrir.

**Entradas**

- `NetunoConfig` inteiro, com os campos do apêndice A
- estado da interface
- análise corrente

**Regras**

1. Formato JSON, em seções nomeadas.
2. A leitura usa valor-padrão campo a campo, de modo que arquivo antigo continua abrindo.
3. `created_at` e `precip_file` descrevem o ato de salvar, e não o projeto: por isso não voltam.
4. É a quinta travessia do programa — a que atravessa o **tempo** em vez dos módulos. Trinta dos 87 campos de então não sobreviviam ao ciclo, inclusive a escolha inteira da ETAP, a altura manométrica, os materiais dos reservatórios, a irrigação e o IPTU.

**Saídas**

- Arquivo `.netuno`
- `NetunoConfig` reconstruída

**Exceção.** Seção ausente no arquivo cai para os padrões da classe. JSON inválido interrompe a abertura com mensagem.

### B.23. PROC-23 — Emitir relatórios e exportações

*Relatórios*

**Gatilho.** Aba Relatórios; aba Exportação.

**Entradas**

- resultados de PROC-12, PROC-18, PROC-19, PROC-20 e PROC-21
- dados do projeto

**Regras**

1. Três relatórios: executivo, ambiental com ESG, e científico.
2. Exportação para CAD e BIM a partir do dimensionamento.
3. Planilhas com a série diária e a varredura.

**Saídas**

- HTML, PDF, DXF, JSON para BIM e XLSX

**Exceção.** A conversão para PDF tenta o motor do Qt e cai para o gerador alternativo quando ele não está disponível.

### B.24. PROC-24 — Automação para estudos de larga escala

*Automação*

**Gatilho.** Linha de comando `netuno`, descrita na seção 3.6 (volume Guias de uso); acompanha a instalação como pacote Python, e não o instalador de Windows.

**Entradas**

- arquivo de projeto
- arquivo de chuva

**Regras**

1. Chama o **mesmo** núcleo de cálculo da janela, sem tela.
2. Só parte dos parâmetros é alcançável por ela; os demais só existem na interface, e o caminho é montar o projeto na janela e variar por automação só o que muda entre os casos.
3. Serve a matrizes fatoriais de milhares de casos e à propagação de incerteza por sorteio, que são o instrumental dos trabalhos publicados pelo grupo.

**Saídas**

- JSON e CSV com os resultados

**Exceção.** Parâmetro fora de faixa é recusado antes de simular, com a mesma porta de validação da interface.

---

## Apêndice C — Fatores de emissão

Todo fator usado pela avaliação de ciclo de vida, com procedência, fronteira e grau
de confiança. O detalhamento completo, com as fontes item a item, está em
`docs/procedencia_fatores_co2.md`.

---

### C.1. Materiais de reservatório

<!-- tabela: **Tabela 19** — Fatores de emissão dos materiais de reservatório, com massa e fronteira -->
| Material | Massa por m³ útil | Fator | Fronteira |
| :--- | ---: | ---: | :--- |
| polietileno de alta densidade | 22 kg/m³ | 1,612 kg CO₂e/kg | berço ao portão |
| concreto armado | 1.200 kg/m³ | 0,140 kg CO₂e/kg | berço ao portão |
| fibra de vidro | 15 kg/m³ | 3,250 kg CO₂e/kg | berço ao portão |
| aço inoxidável AISI 304 | 38 kg/m³ | 3,700 kg CO₂e/kg | berço ao portão |

A massa por metro cúbico útil é a que converte volume de reservatório em massa de
material. É ela, e não o fator, que faz o concreto dominar o inventário: 1.200 kg
por metro cúbico contra 22 do polietileno.

> **Consequência prática, demonstrada na seção 4.8 (volume Tutorial):** o material decide o **sinal**
> do resultado ambiental. Com concreto e vida útil de vinte anos, o sistema do
> tutorial não paga a dívida de carbono.

---

### C.2. Água potável de rede

Dezenove rotas de produção disponíveis, por macrorregião e tipo de manancial.

**A fronteira é por metro cúbico entregue na edificação**, e não por metro cúbico
produzido na estação. A conversão usa as perdas de distribuição de cada macrorregião (Figura 1):

![As perdas de distribuição por macrorregião](../figuras/fig43_perdas.png)

*Figura 1 — Quanto de cada metro cúbico produzido chega efetivamente à edificação, por macrorregião. É essa fração que converte um fator de emissão de saída de estação em fator por metro cúbico entregue, e ignorá-la subestima a emissão evitada em até um terço.*


---

### C.3. Rede elétrica

O fator da matriz elétrica brasileira muda **todo ano**, e um estudo sem o ano
declarado é irreprodutível. O programa traz cinco bases de referência e registra qual
foi usada.

---

### C.4. Insumos de tratamento

<!-- tabela: **Tabela 20** — Fatores de emissão dos insumos de tratamento -->
| Insumo | Fator |
| :--- | ---: |
| hipoclorito de cálcio em pastilha a 65% | 1,72 kg CO₂e/kg de produto |
| lâmpada ultravioleta | energia da rede |
| gerador de ozônio | energia da rede |

A massa é de **produto**, e não de cloro ativo. Pastilhas têm cerca de 65% de cloro
ativo.

---

### C.5. Motobomba

Não existe Declaração Ambiental de Produto de motobomba residencial brasileira. O
programa compõe o valor com duas fontes lidas: a massa de cada potência, do catálogo da
Dancor, e a intensidade de 4,77 kg CO₂e por quilo de bomba, da EPD da Grundfos
EPD-GRU-20250340-CBA1-EN (2025, módulos A1 a A3).

<!-- tabela: **Tabela 21** — Emissão de fabricação da motobomba por potência, com a massa de catálogo -->
| Potência | Massa | Emissão de fabricação |
| ---: | ---: | ---: |
| 1/4 CV | 6,1 kg | 29,1 kg CO₂e |
| 1/2 CV | 6,4 kg | 30,5 kg CO₂e |
| 3/4 CV | 13,5 kg | 64,4 kg CO₂e |
| 1 CV | 15,3 kg | 73,0 kg CO₂e |
| 1 1/2 CV | 17,5 kg | 83,5 kg CO₂e |
| 2 CV | 20,7 kg | 98,8 kg CO₂e |

> **Declare no estudo.** A EPD é de um circulador europeu com eletrônica embarcada, e a
> massa de referência inclui a embalagem. A intensidade por quilo é aproximação de ordem
> de grandeza, e não inventário da bomba instalada; havendo EPD do fabricante empregado,
> ela prevalece. Os valores anteriores, de 12 a 55 kg CO₂e, ficavam de 1,7 a 2,7 vezes
> abaixo destes, e quatro deles eram extrapolação aritmética.

---

### C.6. Fatores com rótulo de triagem

Nem todo parâmetro tem fonte primária, e os que não têm são marcados no relatório: hoje,
as massas por metro cúbico útil do polietileno, do concreto e do aço inoxidável, que são
cenários geométricos, e qualquer fator digitado sem fonte. Na revisão de setembro de 2026,
o último fator de emissão padrão sem procedência, o do hipoclorito, passou a tê-la:

<!-- tabela: **Tabela 22** — Procedência do fator de emissão do hipoclorito -->
| Etapa | Valor |
| :--- | :--- |
| base e modelo | Ecoinvent 3.8, *cutoff* |
| processo | *sodium hypochlorite production, product in 15% solution state*, geografia RoW (resto do mundo) |
| método | EF 3.1, categoria *Climate change* |
| resultado | 2,522 kg CO₂e por kg de NaOCl puro |
| conversão | 0,9525 kg de cloro ativo por kg de NaOCl, logo 2,65 kg CO₂e por kg de cloro ativo |
| fator adotado | 2,65 × 0,65 = **1,72 kg CO₂e por kg de pastilha** |

> **Declare a aproximação.** O Ecoinvent 3.8 não tem hipoclorito de cálcio, e o fator é
> o do hipoclorito de sódio levado à base de cloro ativo. Fatores informados pelo usuário
> sem fonte continuam recebendo o rótulo de triagem, e um inventário que apresenta todos
> os fatores com o mesmo grau de confiança esconde onde está a fragilidade.

---

### C.7. O que consultar antes de publicar

1. `docs/procedencia_fatores_co2.md`, para a fonte item a item;
2. a aba de Documentação, capítulo de avaliação de ciclo de vida, para as
   justificativas exibidas ao usuário;
3. o inventário do relatório ambiental, que lista cada item com o fator aplicado.

---

## Apêndice D — Regimes tarifários

A base traz **652 municípios** com estrutura tarifária, percentual
de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída
da própria base do programa, e não transcrita.

### D.1. Os códigos de faixa

Cada linha da tabela tarifária é uma quádrupla `(mínimo, máximo, valor, código)`.

Os seis códigos e o efeito de cada um sobre a fatura estão desenhados na seção 2.7 (volume O método), e não se repetem aqui.


### D.2. Os seis regimes

<!-- tabela: **Tabela 23** — Distribuição dos municípios do catálogo pelos seis regimes tarifários -->
| Regime | Municípios | O que acontece ao economizar |
| :--- | ---: | :--- |
| **Sem mínimo** | 165 | Cada m³ economizado reduz a fatura. |
| **Disponibilidade** | 122 | Valor fixo que **soma** por cima do consumo medido. Cada m³ economizado desconta. |
| **Franquia no mínimo** | 329 | O valor fixo já inclui um volume. Economizar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | 2 | Até a franquia paga-se o fixo; passando dela, tarifa-se **tudo desde zero**. |
| **Piso de pagamento** | 0 | A fatura **não fica** abaixo do piso. Não soma: limita. |
| **Fórmula exponencial** | 34 | Serviço básico mais `PB × Cⁿ`, com `n` pelo consumo do mês (CORSAN). Cada m³ economizado desconta. |

> O piso de pagamento está implementado e nenhum município da base foi
> classificado nele até esta versão.

### D.3. Distribuição por unidade da federação

A cobertura do catálogo acompanha a população, e não o território: as capitais e as regiões metropolitanas estão quase todas cadastradas, e o interior das regiões Norte e Centro-Oeste concentra os municípios ainda ausentes (Figura 2).

![Os municípios do catálogo, por unidade da federação](../figuras/fig42_uf.png)

*Figura 2 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião. São Paulo e Minas Gerais respondem sozinhos por quase um terço do catálogo.*


### D.4. Atualização e auditoria da base

A base tarifária é mantida pelo grupo com uma rotina de atualização executada fora da interface, antes de cada versão. A rotina tem três componentes.

**Energia elétrica.** As tarifas residenciais do subgrupo B1 são lidas da base aberta de tarifas homologadas das distribuidoras, publicada pela Agência Nacional de Energia Elétrica (ANEEL), e associadas à distribuidora de cada município do catálogo.

**Água e esgoto.** Um registro de evidências primárias associa cada prestador à agência reguladora, à página oficial de tarifas e ao tipo de ato que as publica. Os prestadores com portal padronizado têm leitura automática; os demais são marcados para conferência manual do decreto ou da resolução, e a estrutura resultante é submetida à mesma validação de regime descrita neste apêndice.

**Detecção de alterações.** Cada página oficial monitorada é registrada com a assinatura SHA-256 do conteúdo e os cabeçalhos `ETag` e `Last-Modified`. Uma nova verificação compara as assinaturas e aponta as páginas alteradas desde a última coleta, que são as candidatas a revisão tarifária.

A rotina pode simular a atualização sem gravar a base, executar apenas a detecção de alterações, restringir-se a uma unidade da federação ou a um município e separar energia de saneamento. Cada execução grava um relatório de auditoria em Markdown e um painel HTML com a situação de cada município.

### D.5. Grau de confiança

Cada registro traz o grau de confiança da coleta:

<!-- tabela: **Tabela 24** — Grau de confiança dos registros tarifários do catálogo -->
| Grau | Registros |
| :--- | ---: |
| A — alta | 580 |
| B — boa | 63 |
| C — estrutura a conferir | 5 |
| D — estrutura incompleta | 4 |

> **Confira sempre a data de vigência** do registro do seu município contra a
> resolução da concessionária. Tarifas são reajustadas anualmente, e a seção 3.3 (volume Guias de uso)
> ensina o teste que identifica estrutura errada.


### D.6. As faixas por município e categoria

A tabela abaixo traz o preço da água, em R$/m³, em cada intervalo de consumo mensal,
para cada estrutura do catálogo. As colunas são a maior discretização que o catálogo
pede: a união dos limites de faixa de todos os prestadores, de modo que dentro de cada
coluna nenhum prestador muda o preço. Municípios com a mesma tabela formam uma linha,
identificada pelo número da primeira coluna, que se repete nas partes seguintes.

A categoria residencial está nos 652 municípios; as demais aparecem onde a tabela oficial
do prestador foi coletada. A tabela é gerada da base a cada versão e cresce com ela.
A parcela fixa soma por cima do consumo; um preço zero nas primeiras faixas é o volume
já incluído no valor fixo (franquia no mínimo).

A cor da linha diz quanto o dado merece confiança: **verde** (🟢), auditado contra a
fonte primária, a resolução ou a tabela oficial do prestador; **amarelo** (🟡), coletado
automaticamente ou marcado para revisão, e por isso a confirmar contra a resolução
vigente; **vermelho** (🔴), estrutura incompleta, que não deve ser usada sem correção.

São 652 municípios e cinco categorias, 3260 combinações. A primeira tabela diz, para cada categoria, em quantos municípios a tabela tarifária está auditada, a confirmar, incompleta ou ainda não coletada; cada município aparece por extenso nas tabelas seguintes, e as categorias não coletadas estão listadas por prestador ao fim da seção.

<!-- tabela: **Tabela 25** — Cobertura do catálogo tarifário: municípios por categoria e situação do dado -->
| Categoria | 🟢 auditada | 🟡 a confirmar | 🔴 incompleta | 🔴 não coletada | Municípios |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Residencial | 363 | 285 | 4 | 0 | 652 |
| Comercial | 34 | 0 | 0 | 618 | 652 |
| Pública | 34 | 0 | 0 | 618 | 652 |
| Industrial | 30 | 0 | 0 | 622 | 652 |
| Social | 0 | 0 | 0 | 652 | 652 |

<!-- tabela: **Tabela 26** — As estruturas tarifárias do catálogo, numeradas para as tabelas de preço por faixa que vêm a seguir -->
| Nº | Prestador: municípios | Categoria | Fixo (R$/mês) | Esgoto |
| ---: | :--- | :--- | :--- | :--- |
| 🟢 1 | BRK Alagoas: Maceió (AL) | Residencial | — | 100% |
| 🟢 2 | BRK Alagoas: Marechal Deodoro (AL) | Residencial | — | 80% |
| 🟢 3 | BRK Alagoas: Rio Largo (AL) | Residencial | — | 80% |
| 🟡 4 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Residencial | 45,00 | 80% |
| 🟢 5 | BRK Ambiental Limeira: Limeira (SP) | Residencial | 37,10 | 100% |
| 🟡 6 | BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Residencial | 42,00 | 90% |
| 🟢 7 | BRK Ambiental Sumaré: Sumaré (SP) | Residencial | 36,35 | 80% |
| 🟢 8 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Residencial | — | 70% |
| 🟡 9 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Residencial | — | 80% |
| 🟢 10 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Residencial | 33,58 | 100% |
| 🟡 11 | CAER: Boa Vista (RR) | Residencial | 39,92 | 80% |
| 🟢 12 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Residencial | 57,51 | 70% |
| 🟢 13 | CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN), Extremoz (RN), Macaíba (RN), Mossoró (RN), Parnamirim (RN) | Residencial | 56,96 | 70% |
| 🟢 14 | CAERN: Natal (RN) | Residencial | 51,40 | 70% |
| 🟢 15 | CAESB: Brasília (DF) | Residencial | 11,62 | 100% |
| 🟡 16 | CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Residencial | 32,50 | 80% |
| 🟡 17 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Residencial | — | 80% |
| 🟢 18 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Residencial | 54,82 | 80% |
| 🟢 19 | CASAL: Arapiraca (AL) | Residencial | — | 80% |
| 🟡 20 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Residencial | 46,34 | 100% |
| 🟡 21 | CEDAE/serviço local – validar área: Guapimirim (RJ), Itaperuna (RJ), Macaé (RJ), Valença (RJ) | Residencial | — | 100% |
| 🟢 22 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Residencial | 15,01 | 80% |
| 🟢 23 | CESAN: Cariacica (ES), Guarapari (ES), Serra (ES), Vila Velha (ES), Vitória (ES) | Residencial | 57,39 | 80% |
| 🟢 24 | CODAU Uberaba: Uberaba (MG) | Residencial | — | 95% |
| 🟡 25 | COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Residencial | 32,50 | 80% |
| 🟢 26 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Residencial | 36,96 | 100% |
| 🟢 27 | Companhia Águas de Joinville: Joinville (SC) | Residencial | 34,93 | 80% |
| 🟢 28 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Residencial | 61,77 | 100% |
| 🟢 29 | COMUSA Novo Hamburgo: Novo Hamburgo (RS) | Residencial | 43,21 | 70% |
| 🟡 30 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Montes Claros (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Residencial | 25,77 | 74% |
| 🟡 31 | COSAMA: Tabatinga (AM) | Residencial | 32,50 | 80% |
| 🟢 32 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Altamira (PA), Ananindeua (PA), Baião (PA), Barcarena (PA), Belém (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Marituba (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Parauapebas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Residencial | — | 80% |
| 🟢 33 | CSA Equatorial: Macapá (AP), Santana (AP) | Residencial | 42,91 | 100% |
| 🟢 34 | DAAE Araraquara: Araraquara (SP) | Residencial | 22,70 | 100% |
| 🟢 35 | DAAE Rio Claro: Rio Claro (SP) | Residencial | 35,36 | 100% |
| 🟢 36 | DAE Americana: Americana (SP) | Residencial | até 6 m³: 14,30 (retroativa) | 100% |
| 🟢 37 | DAE Bauru: Bauru (SP) | Residencial | até 6 m³: 19,37 (retroativa) | 65% |
| 🟢 38 | DAE Jundiaí: Jundiaí (SP) | Residencial | 40,84 | 69% |
| 🟡 39 | DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Residencial | — | 80% |
| 🟢 40 | DAE Valinhos: Valinhos (SP) | Residencial | 23,73 | 100% |
| 🟡 41 | DAE/VG: Várzea Grande (MT) | Residencial | 31,20 | 80% |
| 🟢 42 | DAEB Bagé: Bagé (RS) | Residencial | 53,37 | 50% |
| 🟢 43 | DAEP Penápolis: Penápolis (SP) | Residencial | 7,31 | 70% |
| 🟡 44 | DAEPA: Patrocínio (MG) | Residencial | — | 80% |
| 🟡 45 | DAESC Coruripe: Coruripe (AL) | Residencial | — | 80% |
| 🟡 46 | DAMAE São João del-Rei: São João del-Rei (MG) | Residencial | — | 80% |
| 🟡 47 | DEMSUR: Muriaé (MG) | Residencial | — | 80% |
| 🟢 48 | DMAE Porto Alegre: Porto Alegre (RS) | Residencial | — | 100% |
| 🟢 49 | DMAE Poços de Caldas: Poços de Caldas (MG) | Residencial | — | 85% |
| 🟡 50 | DMAE Uberlândia: Uberlândia (MG) | Residencial | — | 80% |
| 🟡 51 | DMAES Ponte Nova: Ponte Nova (MG) | Residencial | — | 80% |
| 🟢 52 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Residencial | 44,95 | 100% |
| 🟡 53 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Residencial | 44,77 | 80% |
| 🟢 54 | GS Inima SAMAR: Araçatuba (SP) | Residencial | 28,48 | 80% |
| 🟢 55 | Iguá Sergipe: Aracaju (SE), Estância (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Residencial | 49,26 | 80% |
| 🟢 56 | Ourinhos Saneamento: Ourinhos (SP) | Residencial | — | 50% |
| 🟡 57 | Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Residencial | 23,90 | 100% |
| 🟡 58 | Prestador municipal/local – Iranduba: Iranduba (AM) | Residencial | 32,50 | 80% |
| 🟡 59 | Prestador municipal/local – Manicoré: Manicoré (AM) | Residencial | 32,50 | 80% |
| 🟡 60 | Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Residencial | 32,50 | 80% |
| 🟡 61 | Prestador municipal/local – Tefé: Tefé (AM) | Residencial | 32,50 | 80% |
| 🟢 62 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Residencial | — | 100% |
| 🟢 63 | RIC Ambiental: Marília (SP) | Residencial | 19,71 | 75% |
| 🟡 64 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Residencial | — | 100% |
| 🟡 65 | SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Residencial | 32,50 | 80% |
| 🟡 66 | SAAE Angra dos Reis: Angra dos Reis (RJ) | Residencial | — | 100% |
| 🟡 67 | SAAE Aracruz / CESAN conforme área: Aracruz (ES) | Residencial | 57,39 | 80% |
| 🟡 68 | SAAE Atibaia: Atibaia (SP) | Residencial | 52,97 | 100% |
| 🟡 69 | SAAE Barra Mansa: Barra Mansa (RJ) | Residencial | — | 100% |
| 🟡 70 | SAAE Cacoal: Cacoal (RO) | Residencial | 17,58 | 60% |
| 🟡 71 | SAAE Capivari: Capivari (SP) | Residencial | 33,11 | 90% |
| 🟡 72 | SAAE Cruzeiro: Cruzeiro (SP) | Residencial | 42,00 | 90% |
| 🟡 73 | SAAE Formiga: Formiga (MG) | Residencial | 21,40 | 50% |
| 🟡 74 | SAAE Ibitinga: Ibitinga (SP) | Residencial | — | 100% |
| 🟡 75 | SAAE Indaiatuba: Indaiatuba (SP) | Residencial | 35,10 | 90% |
| 🟡 76 | SAAE Itabira: Itabira (MG) | Residencial | — | 80% |
| 🟡 77 | SAAE Itabirito: Itabirito (MG) | Residencial | 22,73 | 60% |
| 🟡 78 | SAAE Itacoatiara: Itacoatiara (AM) | Residencial | 32,50 | 80% |
| 🟡 79 | SAAE Itapira: Itapira (SP) | Residencial | 22,71 | 100% |
| 🟡 80 | SAAE Jaboticabal: Jaboticabal (SP) | Residencial | 28,91 | 100% |
| 🟡 81 | SAAE Jacareí: Jacareí (SP) | Residencial | 42,00 | 90% |
| 🟡 82 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Residencial | 41,70 | 65% |
| 🟡 83 | SAAE Lençóis Paulista: Lençóis Paulista (SP) | Residencial | 42,00 | 90% |
| 🟡 84 | SAAE Linhares: Linhares (ES) | Residencial | 45,00 | 80% |
| 🟡 85 | SAAE Lucas do Rio Verde: Lucas do Rio Verde (MT) | Residencial | — | 80% |
| 🟡 86 | SAAE Manhuaçu: Manhuaçu (MG) | Residencial | — | 80% |
| 🟡 87 | SAAE Mariana: Mariana (MG) | Residencial | 29,82 | 100% |
| 🟡 88 | SAAE Maués: Maués (AM) | Residencial | 32,50 | 80% |
| 🟡 89 | SAAE Mogi Mirim: Mogi Mirim (SP) | Residencial | 20,25 | 140% |
| 🟡 90 | SAAE Nova Mutum: Nova Mutum (MT) | Residencial | 24,82 | 80% |
| 🟡 91 | SAAE Parintins: Parintins (AM) | Residencial | 32,50 | 80% |
| 🟡 92 | SAAE Passos: Passos (MG) | Residencial | — | 80% |
| 🟡 93 | SAAE Pirapora: Pirapora (MG) | Residencial | 43,06 | 50% |
| 🟡 94 | SAAE Salto: Salto (SP) | Residencial | 32,22 | 100% |
| 🔴 95 | SAAE Sete Lagoas: Sete Lagoas (MG) | Residencial | 30,96 | 80% |
| 🟡 96 | SAAE Sorocaba: Sorocaba (SP) | Residencial | 22,00 | 92% |
| 🟡 97 | SAAE São Carlos: São Carlos (SP) | Residencial | — | 100% |
| 🟡 98 | SAAE São Mateus: São Mateus (ES) | Residencial | — | 80% |
| 🟡 99 | SAAE Três Pontas: Três Pontas (MG) | Residencial | — | 80% |
| 🟡 100 | SAAE Três Rios: Três Rios (RJ) | Residencial | — | 100% |
| 🟡 101 | SAAE Vilhena: Vilhena (RO) | Residencial | 57,51 | 70% |
| 🟡 102 | SAAE Viçosa: Viçosa (MG) | Residencial | — | 50% |
| 🟡 103 | SAAE Volta Redonda: Volta Redonda (RJ) | Residencial | — | 100% |
| 🔴 104 | SAAEB Ambiental: Bebedouro (SP) | Residencial | 34,62 | 80% |
| 🟡 105 | SAAEB Barretos: Barretos (SP) | Residencial | 28,90 | 50% |
| 🟡 106 | SAAEJA: Jaguariúna (SP) | Residencial | 22,81 | 100% |
| 🟡 107 | SAAET: Taquaritinga (SP) | Residencial | 42,00 | 90% |
| 🟢 108 | SABESP: Amparo (SP) | Residencial | 29,47 | 90% |
| 🟢 109 | SABESP: Artur Nogueira (SP), Assis (SP), Avaré (SP), Batatais (SP), Boituva (SP), Botucatu (SP), Campo Limpo Paulista (SP), Caçapava (SP), Cosmópolis (SP), Fernandópolis (SP), Franca (SP), Hortolândia (SP), Ibiúna (SP), Itapetininga (SP), Itapeva (SP), Itatiba (SP), Itupeva (SP), Lins (SP), Lorena (SP), Mococa (SP), Mogi das Cruzes (SP), Monte Mor (SP), Nova Odessa (SP), Paulínia (SP), Piedade (SP), Pindamonhangaba (SP), Porto Feliz (SP), Registro (SP), Santa Bárbara d'Oeste (SP), Suzano (SP), São José dos Campos (SP), São João da Boa Vista (SP), São Roque (SP), Tatuí (SP), Taubaté (SP), Tremembé (SP), Tupã (SP), Votorantim (SP), Várzea Paulista (SP) | Residencial | 40,42 | 80% |
| 🟢 110 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP), Cajamar (SP), Carapicuíba (SP), Cotia (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Ferraz de Vasconcelos (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarulhos (SP), Itapecerica da Serra (SP), Itapevi (SP), Itaquaquecetuba (SP), Jandira (SP), Mairiporã (SP), Mauá (SP), Osasco (SP), Poá (SP), Ribeirão Pires (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), São Bernardo do Campo (SP), São Paulo (SP), Taboão da Serra (SP), Vargem Grande Paulista (SP) | Residencial | 40,42 | 100% |
| 🟢 111 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP), Guarujá (SP), Itanhaém (SP), Mongaguá (SP), Peruíbe (SP), Praia Grande (SP), Santos (SP), São Sebastião (SP), São Vicente (SP), Ubatuba (SP) | Residencial | 40,42 | 100% |
| 🟢 112 | SABESP: Bragança Paulista (SP) | Residencial | 40,42 | 100% |
| 🟢 113 | SABESP: Olímpia (SP) | Residencial | 25,34 | 80% |
| 🟢 114 | SABESP: Presidente Prudente (SP) | Residencial | 32,27 | 80% |
| 🟢 115 | SAE Araguari: Araguari (MG) | Residencial | 33,89 | 80% |
| 🟢 116 | SAE Ituiutaba: Ituiutaba (MG) | Residencial | 18,12 | 70% |
| 🟢 117 | SAE Louveira: Louveira (SP) | Residencial | 27,93 | 85% |
| 🟢 118 | SAEC Catanduva: Catanduva (SP) | Residencial | 24,79 | 100% |
| 🟢 119 | SAECIL Leme: Leme (SP) | Residencial | 35,33 | 85% |
| 🟢 120 | SAEG: Guaratinguetá (SP) | Residencial | 30,06 | 80% |
| 🟢 121 | SAEMA Araras: Araras (SP) | Residencial | 25,71 | 80% |
| 🟢 122 | SAEMAS Sertãozinho: Sertãozinho (SP) | Residencial | 25,31 | 80% |
| 🔴 123 | SAEP Pirassununga: Pirassununga (SP) | Residencial | 29,91 | 100% |
| 🟢 124 | SAERP Ribeirão Preto: Ribeirão Preto (SP) | Residencial | 14,06 | 128% |
| 🔴 125 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Residencial | 29,99 | 80% |
| 🟡 126 | SAESA: São Caetano do Sul (SP) | Residencial | 42,00 | 90% |
| 🟢 127 | SAEV Ambiental: Votuporanga (SP) | Residencial | 28,22 | 100% |
| 🟢 128 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Residencial | 47,43 | 112% |
| 🟢 129 | SAMAE Brusque: Brusque (SC) | Residencial | 42,38 | 80% |
| 🟢 130 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Residencial | 38,30 | 80% |
| 🟢 131 | SAMAE Gaspar: Gaspar (SC) | Residencial | 50,58 | 80% |
| 🟢 132 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Residencial | 30,16 | 80% |
| 🟢 133 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Residencial | 18,91 | 100% |
| 🟢 134 | SAMAE São Bento do Sul: São Bento do Sul (SC) | Residencial | 31,40 | 80% |
| 🟡 135 | SAMAE Tangará da Serra: Tangará da Serra (MT) | Residencial | — | 80% |
| 🟢 136 | SANASA Campinas: Campinas (SP) | Residencial | 53,65 | 123% |
| 🟢 137 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Residencial | 38,37 | 80% |
| 🟢 138 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Residencial | 17,46 | 100% |
| 🟢 139 | Saneaqua: Mairinque (SP) | Residencial | — | 100% |
| 🟢 140 | SANEAR Colatina: Colatina (ES) | Residencial | — | 80% |
| 🟡 141 | SANEAR Rondonópolis: Rondonópolis (MT) | Residencial | 36,50 | 80% |
| 🟢 142 | SANEBAVI Vinhedo: Vinhedo (SP) | Residencial | 40,20 | 100% |
| 🟢 143 | Saneouro: Ouro Preto (MG) | Residencial | 25,72 | 95% |
| 🟢 144 | SANEP Pelotas: Pelotas (RS) | Residencial | 28,96 | 80% |
| 🟡 145 | SANEPAR – Curitiba: Curitiba (PR) | Residencial | 55,09 | 85% |
| 🟡 146 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Residencial | 55,09 | 80% |
| 🟡 147 | Sanessol: Mirassol (SP) | Residencial | 42,00 | 90% |
| 🟢 148 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS), Três Lagoas (MS) | Residencial | 16,50 | 70% |
| 🟢 149 | SEMAE Piracicaba: Piracicaba (SP) | Residencial | 31,99 | 100% |
| 🟢 150 | SeMAE Rio Preto: São José do Rio Preto (SP) | Residencial | 26,63 | 100% |
| 🟢 151 | SEMAE São Leopoldo: São Leopoldo (RS) | Residencial | 61,29 | 80% |
| 🟢 152 | SEMASA Itajaí: Itajaí (SC) | Residencial | 41,70 | 80% |
| 🟢 153 | SEMASA Lages: Lages (SC) | Residencial | 44,00 | 80% |
| 🟡 154 | Serviço local – Barra do Piraí: Barra do Piraí (RJ) | Residencial | — | 100% |
| 🟡 155 | São Gabriel Saneamento S.A.: São Gabriel (RS) | Residencial | 33,89 | 80% |
| 🟢 156 | Tubarão Saneamento: Tubarão (SC) | Residencial | — | 100% |
| 🟢 157 | Verde Alagoas: União dos Palmares (AL) | Residencial | — | 80% |
| 🟡 158 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Residencial | — | 80% |
| 🟢 159 | Águas Cuiabá (Iguá): Cuiabá (MT) | Residencial | — | 90% |
| 🟢 160 | Águas da Imperatriz: Teresópolis (RJ) | Residencial | — | 90% |
| 🟡 161 | Águas das Agulhas Negras: Resende (RJ) | Residencial | — | 100% |
| 🟡 162 | Águas de Andradina: Andradina (SP) | Residencial | 42,00 | 90% |
| 🟢 163 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Residencial | — | 80% |
| 🟡 164 | Águas de Jahu: Jaú (SP) | Residencial | 42,00 | 90% |
| 🟢 165 | Águas de Juturnaíba: Araruama (RJ) | Residencial | — | 100% |
| 🟡 166 | Águas de Manaus: Manaus (AM) | Residencial | — | 80% |
| 🟢 167 | Águas de Matão: Matão (SP) | Residencial | 45,32 | 100% |
| 🟡 168 | Águas de Niterói: Niterói (RJ) | Residencial | — | 100% |
| 🟡 169 | Águas de Nova Friburgo: Nova Friburgo (RJ) | Residencial | — | 100% |
| 🟡 170 | Águas de Pará de Minas: Pará de Minas (MG) | Residencial | — | 80% |
| 🟢 171 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Residencial | — | 90% |
| 🟢 172 | Águas de Sinop (Aegea): Sinop (MT) | Residencial | — | 100% |
| 🟢 173 | Águas de Sorriso: Sorriso (MT) | Residencial | — | 80% |
| 🟢 174 | Águas de Teresina: Teresina (PI) | Residencial | 46,83 | 80% |
| 🟢 175 | Águas de Valadares (Aegea): Governador Valadares (MG) | Residencial | 14,67 | 70% |
| 🟡 176 | Águas do Imperador: Petrópolis (RJ) | Residencial | — | 100% |
| 🟢 177 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Residencial | — | 50% |
| 🟡 178 | Águas do Paraíba: Campos dos Goytacazes (RJ) | Residencial | — | 100% |
| 🟢 179 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Residencial | 52,89 | 80% |
| 🟡 180 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), São João de Meriti (RJ) | Residencial | — | 100% |
| 🟡 181 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ), Maricá (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ) | Residencial | — | 100% |
| 🟡 182 | Águas do Rio / Iguá / Rio+ Saneamento: Rio de Janeiro (RJ) | Residencial | — | 100% |
| 🟢 183 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL) | Residencial | — | 80% |
| 🟢 184 | Águas do Sertão: Penedo (AL) | Residencial | — | 80% |
| 🟢 185 | Águas do Sertão: São Miguel dos Campos (AL) | Residencial | — | 80% |
| 🟢 186 | Águas Guariroba: Campo Grande (MS) | Residencial | 19,87 | 70% |
| 🟢 187 | Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Residencial | — | 90% |

<!-- tabela: **Tabela 27** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 1 de 3: 0–5 a 20–25 m³) -->
| Nº | 0–5 | 5–6 | 6–7 | 7–10 | 10–12 | 12–13 | 13–15 | 15–17 | 17–20 | 20–25 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 7,64 | 7,64 | 7,64 | 7,64 | 14,61 | 14,61 | 14,61 | 16,89 | 16,89 | 18,04 |
| 🟢 2 | 6,82 | 6,82 | 6,82 | 6,82 | 12,70 | 12,70 | 12,70 | 14,27 | 14,27 | 15,46 |
| 🟢 3 | 7,64 | 7,64 | 7,64 | 7,64 | 14,61 | 14,61 | 14,61 | 16,89 | 16,89 | 18,04 |
| 🟡 4 | 0,00 | 0,00 | 0,00 | 0,00 | 6,10 | 6,10 | 6,10 | 6,10 | 6,10 | 9,80 |
| 🟢 5 | 0,00 | 0,00 | 0,00 | 0,00 | 5,11 | 5,11 | 5,11 | 10,14 | 10,14 | 10,14 |
| 🟡 6 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 7 | 0,00 | 0,00 | 0,00 | 0,00 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 4,01 |
| 🟢 8 | 10,20 | 10,20 | 10,20 | 10,20 | 10,70 | 10,70 | 10,70 | 10,70 | 10,70 | 15,34 |
| 🟡 9 | 8,76 | 3,05 | 3,05 | 3,05 | 8,66 | 8,66 | 8,66 | 11,07 | 11,07 | 13,53 |
| 🟢 10 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 10,77 |
| 🟡 11 | 0,00 | 0,00 | 0,00 | 0,00 | 5,40 | 5,40 | 5,40 | 5,40 | 5,40 | 8,90 |
| 🟢 12 | 0,00 | 0,00 | 0,00 | 0,00 | 6,52 | 6,52 | 6,52 | 7,17 | 7,17 | 8,61 |
| 🟢 13 | 0,00 | 0,00 | 0,00 | 0,00 | 6,34 | 6,34 | 6,34 | 7,51 | 7,51 | 8,45 |
| 🟢 14 | 0,00 | 0,00 | 0,00 | 0,00 | 5,73 | 5,73 | 5,73 | 6,77 | 6,77 | 7,64 |
| 🟢 15 | 4,30 | 4,30 | 4,30 | 5,15 | 5,15 | 5,15 | 10,21 | 10,21 | 10,21 | 14,81 |
| 🟡 16 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 17 | 6,77 | 6,77 | 6,77 | 6,77 | 8,78 | 8,78 | 8,78 | 9,49 | 9,49 | 16,29 |
| 🟢 18 | 0,00 | 0,00 | 0,00 | 0,00 | 7,08 | 7,08 | 7,08 | 7,08 | 7,08 | 9,32 |
| 🟢 19 | 7,28 | 7,28 | 7,28 | 7,28 | 13,90 | 13,90 | 13,90 | 16,07 | 16,07 | 17,17 |
| 🟡 20 | 3,08 | 3,08 | 3,08 | 3,08 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟡 21 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟢 22 | 1,65 | 4,46 | 4,46 | 4,46 | 5,58 | 5,58 | 5,58 | 6,32 | 6,32 | 8,55 |
| 🟢 23 | 2,26 | 2,26 | 2,26 | 2,26 | 4,52 | 4,52 | 4,52 | 8,14 | 8,14 | 9,77 |
| 🟢 24 | 3,91 | 3,91 | 3,91 | 3,91 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,74 |
| 🟡 25 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 26 | 0,00 | 0,00 | 0,00 | 0,00 | 4,34 | 4,34 | 4,34 | 4,34 | 4,34 | 6,63 |
| 🟢 27 | 1,49 | 1,49 | 1,49 | 1,49 | 9,89 | 9,89 | 9,89 | 9,95 | 9,95 | 9,95 |
| 🟢 28 | 0,00 | 0,00 | 0,00 | 0,00 | 7,09 | 7,09 | 7,09 | 7,09 | 7,09 | 8,42 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 2,69 | 5,33 | 5,33 | 5,33 | 8,06 | 8,06 | 8,06 | 10,83 | 10,83 | 13,66 |
| 🟡 31 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 32 | 4,91 | 4,91 | 4,91 | 4,91 | 7,00 | 7,00 | 7,00 | 7,00 | 7,00 | 9,38 |
| 🟢 33 | 0,00 | 0,00 | 0,00 | 0,00 | 4,49 | 4,49 | 4,49 | 4,49 | 4,49 | 5,06 |
| 🟢 34 | 0,00 | 0,00 | 0,00 | 0,00 | 4,09 | 4,09 | 4,09 | 4,09 | 4,09 | 5,83 |
| 🟢 35 | 0,00 | 0,00 | 0,00 | 0,00 | 7,19 | 7,19 | 7,19 | 7,19 | 7,19 | 10,77 |
| 🟢 36 | — | — | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | — | — | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 0,00 | 0,00 | 0,00 | 0,00 | 5,18 | 5,18 | 5,18 | 7,65 | 7,65 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 0,00 | 0,00 | 0,00 | 0,00 | 4,40 | 4,40 | 4,40 | 4,40 | 5,69 | 5,69 |
| 🟡 41 | 0,00 | 0,00 | 0,00 | 0,00 | 4,20 | 4,20 | 4,20 | 4,20 | 4,20 | 6,80 |
| 🟢 42 | 4,26 | 4,26 | 4,26 | 4,26 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 6,84 |
| 🟢 43 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 4,89 |
| 🟡 44 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 45 | 7,28 | 7,28 | 7,28 | 7,28 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 |
| 🟡 46 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 47 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 3,70 | 3,70 | 3,70 | 3,70 | 4,44 | 4,44 | 4,44 | 5,22 | 5,22 | 6,74 |
| 🟡 50 | 3,85 | 3,85 | 3,85 | 3,85 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 8,20 |
| 🟡 51 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 52 | 0,66 | 0,66 | 0,66 | 0,66 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟡 53 | 0,00 | 0,00 | 1,77 | 1,77 | 12,53 | 12,53 | 12,53 | 13,41 | 13,41 | 15,08 |
| 🟢 54 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,50 | 3,50 | 3,50 | 3,50 | 6,46 |
| 🟢 55 | 0,00 | 0,00 | 0,00 | 0,00 | 11,02 | 11,02 | 11,02 | 11,02 | 11,02 | 16,75 |
| 🟢 56 | 3,11 | 3,11 | 3,11 | 3,11 | 6,17 | 6,17 | 6,17 | 6,17 | 6,17 | 7,77 |
| 🟡 57 | 0,00 | 0,00 | 0,00 | 0,00 | 2,90 | 2,90 | 2,90 | 2,90 | 2,90 | 3,34 |
| 🟡 58 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 59 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 60 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 61 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 62 | 17,04 | 17,04 | 17,04 | 17,04 | 22,32 | 22,32 | 22,32 | 35,74 | 35,74 | 35,74 |
| 🟢 63 | 0,00 | 2,31 | 2,31 | 2,31 | 2,31 | 2,31 | 2,31 | 6,24 | 6,24 | 6,24 |
| 🟡 64 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 15,37 | 15,37 | 15,37 |
| 🟡 65 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 66 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 67 | 0,00 | 0,00 | 0,00 | 0,00 | 4,52 | 4,52 | 4,52 | 8,14 | 8,14 | 9,77 |
| 🟡 68 | 0,00 | 0,00 | 0,00 | 0,00 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 13,13 |
| 🟡 69 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 70 | 0,00 | 0,00 | 0,00 | 0,00 | 2,11 | 2,11 | 2,11 | 2,43 | 2,43 | 2,79 |
| 🟡 71 | 0,00 | 0,00 | 0,00 | 0,00 | 5,33 | 5,33 | 5,33 | 5,33 | 5,33 | 6,65 |
| 🟡 72 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 73 | 0,60 | 0,85 | 0,85 | 0,85 | 2,82 | 2,82 | 2,82 | 4,29 | 4,29 | 6,26 |
| 🟡 74 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,99 | 2,99 | 3,59 |
| 🟡 75 | 0,00 | 0,52 | 0,52 | 0,52 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 | 6,16 |
| 🟡 76 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 77 | 1,66 | 1,95 | 1,95 | 1,95 | 3,84 | 3,84 | 3,84 | 5,64 | 5,64 | 6,19 |
| 🟡 78 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 79 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,29 | 7,29 | 8,27 |
| 🟡 80 | 0,00 | 0,00 | 0,00 | 0,00 | 3,48 | 3,48 | 3,48 | 3,48 | 3,48 | 4,38 |
| 🟡 81 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 82 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,58 | 3,58 | 3,76 |
| 🟡 83 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 84 | 0,00 | 0,00 | 0,00 | 0,00 | 6,10 | 6,10 | 6,10 | 6,10 | 6,10 | 9,80 |
| 🟡 85 | 2,43 | 2,43 | 2,43 | 2,43 | 3,12 | 3,12 | 3,12 | 3,12 | 3,12 | 4,15 |
| 🟡 86 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 89 | 0,00 | 0,00 | 0,00 | 0,00 | 2,22 | 2,22 | 2,22 | 9,09 | 9,09 | 9,17 |
| 🟡 90 | 0,00 | 0,00 | 0,00 | 0,00 | 5,22 | 5,22 | 5,22 | 5,22 | 5,22 | 7,54 |
| 🟡 91 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 92 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 93 | 1,01 | 1,30 | 1,30 | 1,30 | 2,44 | 2,44 | 2,44 | 4,16 | 4,16 | 6,45 |
| 🟡 94 | 0,00 | 0,00 | 0,00 | 0,00 | 3,60 | 3,60 | 3,60 | 3,92 | 3,92 | 4,31 |
| 🔴 95 | 0,00 | 0,00 | — | — | — | — | — | — | — | — |
| 🟡 96 | 0,00 | 0,00 | 0,00 | 0,00 | 3,30 | 3,30 | 3,30 | 4,81 | 4,81 | 6,98 |
| 🟡 97 | 2,41 | 2,41 | 2,41 | 2,41 | 6,05 | 6,05 | 6,05 | 6,05 | 6,05 | 7,77 |
| 🟡 98 | 3,87 | 3,87 | 3,87 | 3,87 | 6,11 | 6,11 | 6,11 | 7,44 | 7,44 | 8,21 |
| 🟡 99 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 100 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 101 | 0,00 | 0,00 | 0,00 | 0,00 | 7,85 | 7,85 | 7,85 | 7,85 | 7,85 | 11,90 |
| 🟡 102 | 2,82 | 2,93 | 2,93 | 2,93 | 3,14 | 3,14 | 3,14 | 7,03 | 7,03 | 7,03 |
| 🟡 103 | 4,05 | 4,05 | 4,05 | 4,05 | 4,85 | 4,85 | 4,85 | 4,85 | 4,85 | 8,20 |
| 🔴 104 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟡 105 | 0,00 | 0,00 | 0,00 | 0,00 | 5,99 | 5,99 | 5,99 | 6,71 | 6,71 | 7,58 |
| 🟡 106 | 0,00 | 0,00 | 0,00 | 0,00 | 2,76 | 2,76 | 2,76 | 3,22 | 3,22 | 3,96 |
| 🟡 107 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 108 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,17 | 4,17 | 4,17 | 4,17 | 13,78 |
| 🟢 109 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 8,74 |
| 🟢 110 | 0,00 | 0,00 | 0,00 | 0,00 | 6,40 | 6,40 | 6,40 | 6,40 | 6,40 | 15,95 |
| 🟢 111 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 8,74 |
| 🟢 112 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 7,53 |
| 🟢 113 | 0,00 | 0,00 | 0,00 | 0,00 | 5,09 | 5,09 | 5,09 | 5,09 | 5,09 | 5,16 |
| 🟢 114 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 | 6,95 |
| 🟢 115 | 0,00 | 0,00 | 0,00 | 0,00 | 2,34 | 2,34 | 2,34 | 2,34 | 2,34 | 2,57 |
| 🟢 116 | 1,67 | 2,88 | 2,88 | 2,88 | 4,08 | 4,08 | 4,08 | 5,04 | 5,04 | 5,77 |
| 🟢 117 | 0,00 | 0,00 | 0,00 | 0,00 | 3,78 | 3,78 | 3,78 | 3,78 | 3,78 | 4,68 |
| 🟢 118 | 0,00 | 0,00 | 0,00 | 0,00 | 3,25 | 3,25 | 3,25 | 3,25 | 3,25 | 7,75 |
| 🟢 119 | 0,00 | 0,00 | 0,00 | 0,00 | 4,03 | 4,03 | 4,03 | 4,03 | 4,03 | 5,15 |
| 🟢 120 | 0,00 | 0,00 | 0,00 | 0,00 | 4,12 | 4,12 | 4,12 | 4,12 | 4,12 | 6,91 |
| 🟢 121 | 0,00 | 0,00 | 0,00 | 0,00 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 4,13 |
| 🟢 122 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,05 | 2,05 | 4,81 |
| 🔴 123 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟢 124 | 0,00 | 0,00 | 0,00 | 0,00 | 2,48 | 2,48 | 2,48 | 3,93 | 3,93 | 5,39 |
| 🔴 125 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟡 126 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 127 | 0,00 | 0,00 | 0,00 | 0,00 | 4,87 | 4,87 | 4,87 | 4,87 | 4,87 | 8,31 |
| 🟢 128 | 0,00 | 0,00 | 0,00 | 0,00 | 8,63 | 8,63 | 8,63 | 8,63 | 8,63 | 8,63 |
| 🟢 129 | 0,00 | 0,00 | 0,00 | 0,00 | 7,80 | 7,80 | 7,80 | 10,01 | 10,01 | 11,37 |
| 🟢 130 | 0,00 | 8,77 | 8,77 | 8,77 | 10,54 | 10,54 | 10,54 | 16,56 | 16,56 | 21,75 |
| 🟢 131 | 0,00 | 0,00 | 0,00 | 0,00 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 |
| 🟢 132 | 1,59 | 1,80 | 1,80 | 1,80 | 8,05 | 8,05 | 8,05 | 10,23 | 10,23 | 11,37 |
| 🟢 133 | 0,00 | 0,00 | 0,00 | 0,00 | 2,29 | 2,29 | 2,29 | 2,82 | 2,82 | 7,52 |
| 🟢 134 | 2,36 | 2,55 | 2,55 | 2,55 | 8,83 | 8,83 | 8,83 | 9,40 | 9,40 | 10,02 |
| 🟡 135 | 5,85 | 5,85 | 5,85 | 5,85 | 7,90 | 7,90 | 7,90 | 7,90 | 7,90 | 10,80 |
| 🟢 136 | 0,00 | 0,00 | 0,00 | 0,00 | 9,96 | 9,96 | 9,96 | 10,18 | 10,18 | 10,43 |
| 🟢 137 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,68 | 3,68 | 4,57 |
| 🟢 138 | 5,77 | 5,77 | 5,77 | 5,77 | 6,51 | 6,51 | 6,51 | 7,45 | 7,45 | 8,45 |
| 🟢 139 | 4,71 | 4,71 | 4,71 | 4,71 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,04 |
| 🟢 140 | 2,85 | 2,85 | 2,85 | 2,85 | 5,92 | 5,92 | 5,92 | 8,50 | 8,50 | 9,36 |
| 🟡 141 | 0,00 | 0,00 | 0,00 | 0,00 | 5,10 | 5,10 | 5,10 | 5,10 | 5,10 | 8,20 |
| 🟢 142 | 0,00 | 0,00 | 0,00 | 0,00 | 4,56 | 4,56 | 4,56 | 5,73 | 5,73 | 8,00 |
| 🟢 143 | 3,67 | 3,67 | 3,67 | 3,67 | 10,06 | 10,06 | 10,06 | 12,46 | 12,46 | 14,30 |
| 🟢 144 | 6,13 | 6,13 | 6,13 | 6,13 | 7,05 | 7,05 | 7,05 | 7,05 | 7,05 | 9,32 |
| 🟡 145 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,54 | 9,54 | 9,62 |
| 🟡 146 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,54 | 9,54 | 9,62 |
| 🟡 147 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 148 | 5,92 | 5,92 | 5,92 | 5,92 | 7,45 | 7,45 | 7,45 | 9,15 | 9,15 | 11,80 |
| 🟢 149 | 0,00 | 0,00 | 0,00 | 0,00 | 5,49 | 5,49 | 5,49 | 7,88 | 7,88 | 11,28 |
| 🟢 150 | 0,00 | 0,00 | 0,00 | 0,00 | 3,84 | 3,84 | 3,84 | 3,84 | 3,84 | 5,25 |
| 🟢 151 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 11,45 | 11,45 | 11,45 |
| 🟢 152 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟢 153 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟡 154 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 5,25 | 5,25 | 5,25 | 5,25 | 9,68 | 9,68 | 9,68 | 9,68 | 9,68 | 11,11 |
| 🟢 157 | 5,58 | 5,58 | 5,58 | 5,58 | 10,25 | 10,25 | 10,25 | 11,14 | 11,14 | 12,22 |
| 🟡 158 | 5,85 | 5,85 | 5,85 | 5,85 | 7,90 | 7,90 | 7,90 | 7,90 | 7,90 | 10,80 |
| 🟢 159 | 4,92 | 4,92 | 4,92 | 4,92 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 | 10,06 |
| 🟢 160 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 11,62 | 11,62 | 11,62 |
| 🟡 161 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 162 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 163 | 4,33 | 4,33 | 4,33 | 4,33 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,83 |
| 🟡 164 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 165 | 13,79 | 13,79 | 13,79 | 13,79 | 17,71 | 17,71 | 17,71 | 26,45 | 26,45 | 26,45 |
| 🟡 166 | 6,42 | 6,42 | 6,42 | 6,42 | 12,43 | 12,43 | 12,43 | 12,43 | 12,43 | 18,98 |
| 🟢 167 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 | 6,04 |
| 🟡 168 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 14,13 | 14,13 | 14,13 |
| 🟡 169 | 4,25 | 4,25 | 4,25 | 4,25 | 7,10 | 7,10 | 7,10 | 7,10 | 7,10 | 7,10 |
| 🟡 170 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 171 | 5,76 | 5,76 | 5,76 | 5,76 | 8,64 | 8,64 | 8,64 | 8,64 | 8,64 | 14,40 |
| 🟢 172 | 6,01 | 6,01 | 6,01 | 6,01 | 8,54 | 8,54 | 8,54 | 8,54 | 8,54 | 14,32 |
| 🟢 173 | 3,06 | 3,06 | 3,06 | 3,06 | 4,59 | 4,59 | 4,59 | 4,59 | 4,59 | 7,66 |
| 🟢 174 | 0,00 | 0,00 | 0,00 | 0,00 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 |
| 🟢 175 | 1,79 | 1,83 | 1,83 | 1,83 | 5,24 | 5,24 | 5,24 | 5,57 | 5,57 | 5,62 |
| 🟡 176 | 4,80 | 4,80 | 4,80 | 4,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 11,50 |
| 🟢 177 | 3,27 | 3,27 | 3,27 | 3,27 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 8,87 |
| 🟡 178 | 4,85 | 4,85 | 4,85 | 4,85 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 11,50 |
| 🟢 179 | 0,00 | 0,00 | 0,00 | 0,00 | 9,81 | 9,81 | 9,81 | 10,92 | 10,92 | 12,80 |
| 🟡 180 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 16,54 | 16,54 | 16,54 |
| 🟡 181 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 16,36 | 16,36 | 16,36 |
| 🟡 182 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 15,37 | 15,37 | 15,37 |
| 🟢 183 | 7,39 | 7,39 | 7,39 | 7,39 | 14,10 | 14,10 | 14,10 | 16,30 | 16,30 | 17,41 |
| 🟢 184 | 6,14 | 6,14 | 6,14 | 6,14 | 10,68 | 10,68 | 10,68 | 12,17 | 12,17 | 13,72 |
| 🟢 185 | 5,49 | 5,49 | 5,49 | 5,49 | 10,48 | 10,48 | 10,48 | 12,11 | 12,11 | 12,94 |
| 🟢 186 | 8,03 | 8,03 | 8,03 | 8,03 | 10,28 | 10,28 | 10,28 | 10,46 | 10,46 | 11,57 |
| 🟢 187 | 3,03 | 3,03 | 3,03 | 3,03 | 4,55 | 4,55 | 4,55 | 4,55 | 4,55 | 7,57 |

<!-- tabela: **Tabela 28** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 2 de 3: 25–30 a 70–75 m³) -->
| Nº | 25–30 | 30–35 | 35–40 | 40–45 | 45–50 | 50–55 | 55–60 | 60–65 | 65–70 | 70–75 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 |
| 🟢 2 | 15,46 | 15,97 | 15,97 | 15,92 | 15,92 | 15,14 | 15,14 | 15,14 | 15,14 | 15,14 |
| 🟢 3 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 |
| 🟡 4 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 5 | 10,14 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 16,48 | 16,48 | 16,48 |
| 🟡 6 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 7 | 4,01 | 5,64 | 5,64 | 5,64 | 5,64 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 8 | 15,34 | 15,85 | 15,85 | 15,85 | 15,85 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟡 9 | 15,67 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 10 | 10,77 | 13,68 | 13,68 | 13,68 | 13,68 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟡 11 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 12 | 9,87 | 11,82 | 11,82 | 11,82 | 11,82 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟢 13 | 8,45 | 9,74 | 9,74 | 9,74 | 9,74 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 14 | 7,64 | 8,79 | 8,79 | 8,79 | 8,79 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 15 | 14,81 | 22,22 | 22,22 | 22,22 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 16 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 17 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 18 | 9,32 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 19 | 17,17 | 17,72 | 17,72 | 17,96 | 17,96 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 |
| 🟡 20 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟡 21 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 22 | 8,55 | 8,55 | 8,55 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 |
| 🟢 23 | 9,77 | 11,24 | 11,24 | 11,24 | 11,24 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟢 24 | 5,74 | 6,13 | 6,13 | 6,13 | 6,13 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 |
| 🟡 25 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 26 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 27 | 13,18 | 13,18 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 28 | 8,42 | 11,59 | 11,59 | 11,59 | 11,59 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 13,66 | 13,66 | 13,66 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟡 31 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 32 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 33 | 5,06 | 6,58 | 6,58 | 6,58 | 6,58 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 |
| 🟢 34 | 5,83 | 7,64 | 7,64 | 9,07 | 9,07 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 |
| 🟢 35 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 |
| 🟢 36 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 7,77 | 7,77 | 10,69 | 10,69 | 10,69 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 |
| 🟡 41 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 42 | 6,84 | 8,10 | 8,10 | 8,94 | 8,94 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 43 | 4,89 | 5,26 | 5,26 | 5,64 | 5,64 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 |
| 🟡 44 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 45 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 46 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 47 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 6,74 | 8,37 | 8,37 | 9,93 | 9,93 | 11,47 | 11,47 | 13,08 | 13,08 | 14,61 |
| 🟡 50 | 8,20 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 51 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 52 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟡 53 | 16,82 | 18,49 | 18,49 | 20,28 | 20,28 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 54 | 6,46 | 8,82 | 8,82 | 8,82 | 8,82 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 55 | 16,75 | 23,49 | 23,49 | 23,49 | 23,49 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 |
| 🟢 56 | 7,77 | 10,04 | 10,04 | 10,04 | 10,04 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 57 | 3,34 | 3,70 | 3,70 | 5,06 | 5,06 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 |
| 🟡 58 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 59 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 61 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 62 | 42,88 | 42,88 | 51,46 | 51,46 | 63,18 | 63,18 | 80,25 | 80,25 | 91,26 | 91,26 |
| 🟢 63 | 6,24 | 8,41 | 8,41 | 8,41 | 8,41 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 64 | 15,37 | 20,94 | 20,94 | 20,94 | 41,88 | 41,88 | 41,88 | 55,84 | 55,84 | 55,84 |
| 🟡 65 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 66 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 67 | 9,77 | 11,24 | 11,24 | 11,24 | 11,24 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟡 68 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟡 69 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 70 | 3,21 | 3,69 | 3,69 | 3,69 | 3,69 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟡 71 | 6,65 | 9,53 | 9,53 | 14,27 | 14,27 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 72 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 73 | 8,23 | 9,71 | 9,71 | 9,96 | 9,96 | 10,01 | 10,01 | 10,01 | 10,01 | 10,01 |
| 🟡 74 | 4,11 | 4,66 | 5,33 | 6,07 | 6,92 | 7,88 | 7,88 | 7,88 | 7,88 | 8,99 |
| 🟡 75 | 6,16 | 6,83 | 6,83 | 9,65 | 9,65 | 9,65 | 9,65 | 11,45 | 11,45 | 11,45 |
| 🟡 76 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 77 | 6,83 | 7,49 | 7,49 | 8,29 | 8,29 | 9,09 | 9,09 | 9,09 | 9,09 | 9,09 |
| 🟡 78 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 79 | 8,27 | 8,37 | 8,50 | 8,67 | 8,67 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟡 80 | 4,38 | 7,21 | 7,21 | 8,37 | 8,37 | 11,88 | 11,88 | 13,03 | 13,03 | 14,36 |
| 🟡 81 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 82 | 3,93 | 4,31 | 4,31 | 4,51 | 4,51 | 4,72 | 4,72 | 4,72 | 4,72 | 4,72 |
| 🟡 83 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 84 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟡 85 | 5,96 | 5,96 | 7,03 | 7,03 | 7,03 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟡 86 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 89 | 9,17 | 9,56 | 9,56 | 10,05 | 10,05 | 10,66 | 10,66 | 10,66 | 10,66 | 10,66 |
| 🟡 90 | 7,54 | 9,28 | 9,28 | 11,59 | 11,59 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 91 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 92 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 93 | 8,17 | 9,88 | 9,88 | 10,17 | 10,17 | 10,23 | 10,23 | 10,23 | 10,23 | 10,23 |
| 🟡 94 | 4,77 | 5,27 | 6,34 | 8,07 | 8,07 | 8,07 | 8,07 | 10,21 | 10,21 | 10,21 |
| 🔴 95 | — | — | — | — | — | — | — | — | — | — |
| 🟡 96 | 7,69 | 8,05 | 8,05 | 8,47 | 8,47 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟡 97 | 7,77 | 9,81 | 9,81 | 11,65 | 11,65 | 12,78 | 12,78 | 14,16 | 14,16 | 14,16 |
| 🟡 98 | 8,21 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 99 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 100 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 101 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 102 | 7,03 | 7,03 | 7,03 | 9,74 | 9,74 | 9,74 | 9,74 | 10,33 | 10,33 | 10,33 |
| 🟡 103 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🔴 104 | — | — | — | — | — | — | — | — | — | — |
| 🟡 105 | 8,64 | 9,94 | 11,54 | 13,50 | 13,50 | 15,91 | 15,91 | 15,91 | 15,91 | 15,91 |
| 🟡 106 | 4,73 | 5,65 | 6,85 | 6,85 | 8,21 | 8,21 | 8,21 | 9,78 | 9,78 | 9,78 |
| 🟡 107 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 108 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 |
| 🟢 109 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 110 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 111 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 112 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 113 | 5,16 | 7,09 | 7,09 | 7,09 | 7,09 | 11,82 | 11,82 | 11,93 | 11,93 | 12,03 |
| 🟢 114 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 115 | 2,57 | 2,81 | 2,81 | 3,10 | 3,10 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 116 | 6,49 | 6,97 | 6,97 | 7,45 | 7,45 | 7,69 | 7,69 | 7,69 | 7,69 | 7,69 |
| 🟢 117 | 4,68 | 6,43 | 6,43 | 7,25 | 7,25 | 10,21 | 10,21 | 10,21 | 10,21 | 15,08 |
| 🟢 118 | 7,79 | 8,34 | 8,34 | 9,77 | 9,77 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 |
| 🟢 119 | 5,15 | 6,62 | 6,62 | 6,90 | 6,90 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟢 120 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 121 | 4,13 | 5,58 | 5,58 | 5,58 | 5,58 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 |
| 🟢 122 | 5,39 | 5,83 | 5,93 | 6,46 | 6,46 | 7,02 | 7,02 | 7,67 | 7,67 | 9,92 |
| 🔴 123 | — | — | — | — | — | — | — | — | — | — |
| 🟢 124 | 7,18 | 9,33 | 9,33 | 12,57 | 12,57 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🔴 125 | — | — | — | — | — | — | — | — | — | — |
| 🟡 126 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 127 | 8,31 | 8,25 | 8,25 | 8,25 | 8,25 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 |
| 🟢 128 | 8,63 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 129 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 130 | 21,75 | 22,66 | 22,66 | 22,66 | 22,66 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 |
| 🟢 131 | 10,30 | 10,30 | 10,30 | 12,49 | 12,49 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 132 | 12,49 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 133 | 7,52 | 7,58 | 7,58 | 9,34 | 9,34 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 134 | 10,34 | 10,34 | 10,34 | 10,34 | 10,34 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 |
| 🟡 135 | 10,80 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 136 | 12,82 | 13,65 | 13,65 | 13,65 | 13,65 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 137 | 5,46 | 6,35 | 7,24 | 8,12 | 9,01 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 138 | 9,54 | 10,89 | 10,89 | 12,33 | 12,33 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 139 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 140 | 9,36 | 9,98 | 9,98 | 9,98 | 9,98 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟡 141 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 142 | 8,00 | 8,00 | 11,63 | 11,63 | 11,63 | 16,92 | 16,92 | 16,92 | 16,92 | 16,92 |
| 🟢 143 | 14,30 | 14,30 | 14,30 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 |
| 🟢 144 | 9,32 | 10,74 | 10,74 | 10,74 | 10,74 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟡 145 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 146 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 147 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 148 | 11,80 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 |
| 🟢 149 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 |
| 🟢 150 | 5,25 | 6,99 | 6,99 | 8,64 | 8,64 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 |
| 🟢 151 | 11,45 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 152 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 153 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 154 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 11,11 | 13,59 | 13,59 | 13,59 | 13,59 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 157 | 12,22 | 12,64 | 12,64 | 13,29 | 13,29 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 158 | 10,80 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 159 | 10,06 | 12,31 | 12,31 | 12,31 | 12,31 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 160 | 11,62 | 15,85 | 15,85 | 15,85 | 31,70 | 31,70 | 31,70 | 42,27 | 42,27 | 42,27 |
| 🟡 161 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 162 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 163 | 10,83 | 14,29 | 14,29 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟡 164 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 165 | 33,10 | 33,10 | 42,43 | 42,43 | 51,93 | 51,93 | 66,02 | 66,02 | 80,27 | 80,27 |
| 🟡 166 | 18,98 | 25,86 | 25,86 | 29,84 | 29,84 | 29,84 | 29,84 | 34,02 | 34,02 | 34,02 |
| 🟢 167 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 168 | 14,13 | 17,53 | 17,53 | 17,53 | 33,92 | 33,92 | 33,92 | 45,23 | 45,23 | 45,23 |
| 🟡 169 | 7,10 | 11,80 | 11,80 | 11,80 | 11,80 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 170 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 171 | 14,40 | 19,01 | 19,01 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 172 | 14,32 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 173 | 7,66 | 11,48 | 11,48 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 174 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 175 | 5,62 | 5,62 | 5,62 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟡 176 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 177 | 8,87 | 11,37 | 11,37 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 |
| 🟡 178 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 179 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 180 | 16,54 | 22,56 | 22,56 | 22,56 | 45,12 | 45,12 | 45,12 | 60,16 | 60,16 | 60,16 |
| 🟡 181 | 16,36 | 22,31 | 22,31 | 22,31 | 44,62 | 44,62 | 44,62 | 59,49 | 59,49 | 59,49 |
| 🟡 182 | 15,37 | 20,94 | 20,94 | 20,94 | 41,88 | 41,88 | 41,88 | 55,84 | 55,84 | 55,84 |
| 🟢 183 | 17,41 | 17,98 | 17,98 | 18,21 | 18,21 | 18,33 | 18,33 | 18,33 | 18,33 | 18,33 |
| 🟢 184 | 13,72 | 14,83 | 14,83 | 15,57 | 15,57 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 |
| 🟢 185 | 12,94 | 13,36 | 13,36 | 13,54 | 13,54 | 13,62 | 13,62 | 13,62 | 13,62 | 13,62 |
| 🟢 186 | 14,23 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 187 | 7,57 | 9,99 | 9,99 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: **Tabela 29** — Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 3 de 3: 75–80 a 5.000 m³) -->
| Nº | 75–80 | 80–90 | 90–99 | 99–100 | 100–150 | 150–200 | 200–300 | 300–500 | 500–5.000 | > 5.000 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 2 | 15,14 | 15,14 | 16,96 | 16,96 | 16,96 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 |
| 🟢 3 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟡 4 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 5 | 16,48 | 16,48 | 16,48 | 16,48 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟡 6 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 7 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 8 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟡 9 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 10 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟡 11 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 12 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟢 13 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 14 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 15 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 16 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 17 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 18 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 19 | 18,07 | 18,07 | 18,18 | 18,18 | 18,18 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟡 20 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟡 21 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 22 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 |
| 🟢 23 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟢 24 | 6,88 | 6,88 | 6,88 | 6,88 | 7,03 | 7,03 | 7,28 | 7,28 | 7,28 | 7,28 |
| 🟡 25 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 26 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 27 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 28 | 13,74 | 13,74 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟡 31 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 32 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 33 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 |
| 🟢 34 | 10,82 | 10,82 | 10,82 | 10,82 | 12,76 | 12,76 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 35 | 15,55 | 15,55 | 15,55 | 15,55 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 |
| 🟢 36 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 |
| 🟡 41 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 42 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 43 | 6,39 | 6,39 | 6,39 | 6,39 | 6,76 | 6,76 | 6,76 | 6,76 | 6,76 | 6,76 |
| 🟡 44 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 45 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 46 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 47 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟡 50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 51 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 52 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟡 53 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 54 | 12,69 | 12,69 | 12,69 | 12,69 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 |
| 🟢 55 | 32,67 | 32,67 | 32,67 | 32,67 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 |
| 🟢 56 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 57 | 6,46 | 6,46 | 6,46 | 6,46 | 8,12 | 8,12 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟡 58 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 59 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 61 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 62 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 63 | 10,20 | 10,20 | 10,20 | 10,20 | 11,63 | 11,63 | 11,63 | 11,63 | 11,63 | 11,63 |
| 🟡 64 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 |
| 🟡 65 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 66 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 67 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟡 68 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟡 69 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 70 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟡 71 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 72 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 73 | 10,06 | 10,06 | 10,06 | 10,06 | 10,11 | 10,11 | 10,16 | 10,16 | 10,16 | 10,16 |
| 🟡 74 | 8,99 | 8,99 | 8,99 | 8,99 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 |
| 🟡 75 | 11,45 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟡 76 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 77 | 9,99 | 9,99 | 9,99 | 9,99 | 10,99 | 10,99 | 12,09 | 12,09 | 12,09 | 12,09 |
| 🟡 78 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 79 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟡 80 | 14,36 | 15,93 | 17,47 | 17,47 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟡 81 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 82 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟡 83 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 84 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟡 85 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟡 86 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 89 | 11,67 | 11,67 | 11,67 | 11,67 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 |
| 🟡 90 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 91 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 92 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 93 | 10,29 | 10,29 | 10,29 | 10,29 | 10,34 | 10,34 | 10,40 | 10,40 | 10,40 | 10,40 |
| 🟡 94 | 10,21 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🔴 95 | — | — | — | — | — | — | — | — | — | — |
| 🟡 96 | 9,12 | 9,12 | 9,12 | 9,12 | 10,95 | 10,95 | 13,13 | 15,75 | 15,75 | 15,75 |
| 🟡 97 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 |
| 🟡 98 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 99 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 100 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 101 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 102 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,95 | 10,95 | 10,95 |
| 🟡 103 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🔴 104 | — | — | — | — | — | — | — | — | — | — |
| 🟡 105 | 15,91 | 15,91 | 15,91 | 15,91 | 17,18 | 17,18 | 17,18 | 17,18 | 17,18 | 17,18 |
| 🟡 106 | 9,78 | 9,78 | 9,78 | 9,78 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟡 107 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 108 | 20,37 | 20,37 | 20,37 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟢 109 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 110 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 111 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 112 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 113 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 114 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 115 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 116 | 7,93 | 7,93 | 7,93 | 7,93 | 8,17 | 8,17 | 8,41 | 8,41 | 8,41 | 8,41 |
| 🟢 117 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 118 | 11,47 | 11,47 | 11,47 | 11,47 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 119 | 9,23 | 9,23 | 9,23 | 9,23 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 120 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 121 | 7,82 | 7,82 | 7,82 | 7,82 | 11,34 | 11,34 | 11,34 | 11,34 | 17,02 | 26,39 |
| 🟢 122 | 9,92 | 12,03 | 12,81 | 12,81 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🔴 123 | — | — | — | — | — | — | — | — | — | — |
| 🟢 124 | 15,77 | 19,02 | 19,02 | 19,02 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 |
| 🔴 125 | — | — | — | — | — | — | — | — | — | — |
| 🟡 126 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 127 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 |
| 🟢 128 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 129 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 130 | 24,36 | 24,36 | 24,36 | 24,36 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 131 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 132 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 133 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 134 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 |
| 🟡 135 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 136 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 137 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 138 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 139 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 140 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟡 141 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 142 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 143 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 |
| 🟢 144 | 12,33 | 12,33 | 12,33 | 12,33 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟡 145 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 147 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 148 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 |
| 🟢 149 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 |
| 🟢 150 | 13,14 | 13,14 | 13,14 | 13,14 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 |
| 🟢 151 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 152 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 153 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 154 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 157 | 13,92 | 13,92 | 13,96 | 13,96 | 13,96 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟡 158 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 159 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 160 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟡 161 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 162 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 163 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟡 164 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 165 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟡 166 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 167 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 168 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 169 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 170 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 171 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 172 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 173 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 174 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 175 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟡 176 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 177 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 |
| 🟡 178 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 179 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 180 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟡 181 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 |
| 🟡 182 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 |
| 🟢 183 | 18,33 | 18,33 | 18,44 | 18,44 | 18,44 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 |
| 🟢 184 | 15,95 | 15,95 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 |
| 🟢 185 | 13,62 | 13,62 | 13,70 | 13,70 | 13,70 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 |
| 🟢 186 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 187 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

As categorias abaixo ainda não têm a tabela oficial do prestador no catálogo. Nesses municípios o programa não as oferece, e o caminho é lançar a tabela no modo Personalizado.

<!-- tabela: **Tabela 30** — Categorias tarifárias ainda não coletadas, por prestador -->
| Prestador: municípios | Categorias não coletadas |
| :--- | :--- |
| 🔴 BRK Alagoas: Maceió (AL), Marechal Deodoro (AL), Rio Largo (AL) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Limeira: Limeira (SP) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Sumaré: Sumaré (SP) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Ambiental Uruguaiana: Uruguaiana (RS) | Comercial, Pública, Industrial, Social |
| 🔴 BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO), Paraíso do Tocantins (TO), Porto Nacional (TO) | Comercial, Pública, Industrial, Social |
| 🔴 CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA), Barra do Corda (MA), Barreirinhas (MA), Buriticupu (MA), Caxias (MA), Chapadinha (MA), Codó (MA), Coroatá (MA), Grajaú (MA), Imperatriz (MA), Itapecuru-Mirim (MA), Paço do Lumiar (MA), Pinheiro (MA), Santa Inês (MA), Santa Luzia (MA), São José de Ribamar (MA), São Luís (MA), Timon (MA), Tutóia (MA), Viana (MA) | Comercial, Pública, Industrial, Social |
| 🔴 CAER: Boa Vista (RR) | Comercial, Pública, Industrial, Social |
| 🔴 CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO), Porto Velho (RO), Rolim de Moura (RO) | Comercial, Pública, Industrial, Social |
| 🔴 CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN), Extremoz (RN), Macaíba (RN), Mossoró (RN), Natal (RN), Parnamirim (RN) | Comercial, Pública, Industrial, Social |
| 🔴 CAESB: Brasília (DF) | Comercial, Pública, Industrial, Social |
| 🔴 CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Comercial, Pública, Industrial, Social |
| 🔴 CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE), Barbalha (CE), Beberibe (CE), Boa Viagem (CE), Brejo Santo (CE), Camocim (CE), Canindé (CE), Cascavel (CE), Caucaia (CE), Crateús (CE), Crato (CE), Eusébio (CE), Fortaleza (CE), Granja (CE), Horizonte (CE), Icó (CE), Iguatu (CE), Itaitinga (CE), Itapipoca (CE), Juazeiro do Norte (CE), Limoeiro do Norte (CE), Maracanaú (CE), Maranguape (CE), Morada Nova (CE), Pacajus (CE), Pacatuba (CE), Quixadá (CE), Quixeramobim (CE), Russas (CE), Sobral (CE), São Gonçalo do Amarante (CE), Tauá (CE), Tianguá (CE), Trairi (CE), Viçosa do Ceará (CE) | Comercial, Pública, Industrial, Social |
| 🔴 CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB), Campina Grande (PB), Guarabira (PB), João Pessoa (PB), Patos (PB), Santa Rita (PB), Sapé (PB), Sousa (PB) | Comercial, Pública, Industrial, Social |
| 🔴 CASAL: Arapiraca (AL) | Comercial, Pública, Industrial, Social |
| 🔴 CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC), Canoinhas (SC), Caçador (SC), Chapecó (SC), Concórdia (SC), Criciúma (SC), Florianópolis (SC), Imbituba (SC), Indaial (SC), Itapema (SC), Içara (SC), Mafra (SC), Navegantes (SC), Palhoça (SC), Rio do Sul (SC), São Francisco do Sul (SC), São José (SC), Tijucas (SC), Videira (SC), Xanxerê (SC) | Comercial, Pública, Industrial, Social |
| 🔴 CEDAE/serviço local – validar área: Guapimirim (RJ), Itaperuna (RJ), Macaé (RJ), Valença (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 CESAMA Juiz de Fora: Juiz de Fora (MG) | Comercial, Pública, Industrial, Social |
| 🔴 CESAN: Cariacica (ES), Guarapari (ES), Serra (ES), Vila Velha (ES), Vitória (ES) | Comercial, Pública, Industrial, Social |
| 🔴 CODAU Uberaba: Uberaba (MG) | Comercial, Pública, Industrial, Social |
| 🔴 COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Companhia Ituana de Saneamento (CIS): Itu (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Companhia Águas de Joinville: Joinville (SC) | Comercial, Pública, Industrial, Social |
| 🔴 COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE), Belo Jardim (PE), Bezerros (PE), Buíque (PE), Cabo de Santo Agostinho (PE), Camaragibe (PE), Carpina (PE), Caruaru (PE), Escada (PE), Garanhuns (PE), Goiana (PE), Gravatá (PE), Igarassu (PE), Ipojuca (PE), Jaboatão dos Guararapes (PE), Limoeiro (PE), Moreno (PE), Olinda (PE), Ouricuri (PE), Palmares (PE), Paudalho (PE), Paulista (PE), Pesqueira (PE), Petrolina (PE), Recife (PE), Salgueiro (PE), Santa Cruz do Capibaribe (PE), Serra Talhada (PE), Surubim (PE), São Lourenço da Mata (PE), Vitória de Santo Antão (PE) | Comercial, Pública, Industrial, Social |
| 🔴 COMUSA Novo Hamburgo: Novo Hamburgo (RS) | Comercial, Pública, Industrial, Social |
| 🔴 COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG), Belo Horizonte (MG), Betim (MG), Bom Despacho (MG), Campo Belo (MG), Caratinga (MG), Cataguases (MG), Congonhas (MG), Conselheiro Lafaiete (MG), Contagem (MG), Coronel Fabriciano (MG), Curvelo (MG), Divinópolis (MG), Esmeraldas (MG), Extrema (MG), Frutal (MG), Guaxupé (MG), Ibirité (MG), Ipatinga (MG), Itajubá (MG), Itaúna (MG), Janaúba (MG), Januária (MG), João Monlevade (MG), Lagoa Santa (MG), Lavras (MG), Leopoldina (MG), Montes Claros (MG), Nova Lima (MG), Nova Serrana (MG), Paracatu (MG), Patos de Minas (MG), Pedro Leopoldo (MG), Pouso Alegre (MG), Ribeirão das Neves (MG), Sabará (MG), São Francisco (MG), São Sebastião do Paraíso (MG), Teófilo Otoni (MG), Timóteo (MG), Três Corações (MG), Ubá (MG), Unaí (MG), Varginha (MG), Vespasiano (MG) | Comercial, Pública, Industrial, Social |
| 🔴 CORSAN: Canoas (RS), Erechim (RS), Esteio (RS), Santa Cruz do Sul (RS) | Industrial |
| 🔴 CORSAN: Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Canoas (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Erechim (RS), Esteio (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Cruz do Sul (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Social |
| 🔴 COSAMA: Tabatinga (AM) | Comercial, Pública, Industrial, Social |
| 🔴 COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA), Altamira (PA), Ananindeua (PA), Baião (PA), Barcarena (PA), Belém (PA), Benevides (PA), Bragança (PA), Breves (PA), Cametá (PA), Canaã dos Carajás (PA), Capanema (PA), Capitão Poço (PA), Castanhal (PA), Dom Eliseu (PA), Igarapé-Miri (PA), Itaituba (PA), Juruti (PA), Marabá (PA), Marituba (PA), Moju (PA), Monte Alegre (PA), Novo Repartimento (PA), Oriximiná (PA), Paragominas (PA), Parauapebas (PA), Portel (PA), Redenção (PA), Rondon do Pará (PA), Santa Izabel do Pará (PA), Santarém (PA), São Félix do Xingu (PA), São Miguel do Guamá (PA), Tailândia (PA), Tomé-Açu (PA), Tucuruí (PA), Vigia (PA), Viseu (PA), Xinguara (PA), Óbidos (PA) | Comercial, Pública, Industrial, Social |
| 🔴 CSA Equatorial: Macapá (AP), Santana (AP) | Comercial, Pública, Industrial, Social |
| 🔴 DAAE Araraquara: Araraquara (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAAE Rio Claro: Rio Claro (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Americana: Americana (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Bauru: Bauru (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Jundiaí: Jundiaí (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Comercial, Pública, Industrial, Social |
| 🔴 DAE Valinhos: Valinhos (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAE/VG: Várzea Grande (MT) | Comercial, Pública, Industrial, Social |
| 🔴 DAEB Bagé: Bagé (RS) | Comercial, Pública, Industrial, Social |
| 🔴 DAEP Penápolis: Penápolis (SP) | Comercial, Pública, Industrial, Social |
| 🔴 DAEPA: Patrocínio (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DAESC Coruripe: Coruripe (AL) | Comercial, Pública, Industrial, Social |
| 🔴 DAMAE São João del-Rei: São João del-Rei (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DEMSUR: Muriaé (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DMAE Porto Alegre: Porto Alegre (RS) | Comercial, Pública, Industrial, Social |
| 🔴 DMAE Poços de Caldas: Poços de Caldas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DMAE Uberlândia: Uberlândia (MG) | Comercial, Pública, Industrial, Social |
| 🔴 DMAES Ponte Nova: Ponte Nova (MG) | Comercial, Pública, Industrial, Social |
| 🔴 EMASA Balneário Camboriú: Balneário Camboriú (SC) | Comercial, Pública, Industrial, Social |
| 🔴 EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA), Bom Jesus da Lapa (BA), Brumado (BA), Caetité (BA), Camaçari (BA), Campo Formoso (BA), Candeias (BA), Casa Nova (BA), Conceição do Coité (BA), Cruz das Almas (BA), Dias d'Ávila (BA), Euclides da Cunha (BA), Eunápolis (BA), Feira de Santana (BA), Guanambi (BA), Ilhéus (BA), Ipirá (BA), Irecê (BA), Itaberaba (BA), Itabuna (BA), Itamaraju (BA), Itapetinga (BA), Jacobina (BA), Jequié (BA), Juazeiro (BA), Lauro de Freitas (BA), Luís Eduardo Magalhães (BA), Paulo Afonso (BA), Porto Seguro (BA), Ribeira do Pombal (BA), Salvador (BA), Santo Amaro (BA), Santo Antônio de Jesus (BA), Santo Estêvão (BA), Senhor do Bonfim (BA), Serrinha (BA), Simões Filho (BA), Teixeira de Freitas (BA), Vitória da Conquista (BA) | Comercial, Pública, Industrial, Social |
| 🔴 GS Inima SAMAR: Araçatuba (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Iguá Sergipe: Aracaju (SE), Estância (SE), Itabaiana (SE), Lagarto (SE), Nossa Senhora do Socorro (SE), São Cristóvão (SE), Tobias Barreto (SE) | Comercial, Pública, Industrial, Social |
| 🔴 Ourinhos Saneamento: Ourinhos (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – Iranduba: Iranduba (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – Manicoré: Manicoré (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prestador municipal/local – Tefé: Tefé (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 RIC Ambiental: Marília (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Angra dos Reis: Angra dos Reis (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Aracruz / CESAN conforme área: Aracruz (ES) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Atibaia: Atibaia (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Barra Mansa: Barra Mansa (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Cacoal: Cacoal (RO) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Capivari: Capivari (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Cruzeiro: Cruzeiro (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Formiga: Formiga (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Ibitinga: Ibitinga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Indaiatuba: Indaiatuba (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Itabira: Itabira (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Itabirito: Itabirito (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Itacoatiara: Itacoatiara (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Itapira: Itapira (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Jaboticabal: Jaboticabal (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Jacareí: Jacareí (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Lagoa da Prata: Lagoa da Prata (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Lençóis Paulista: Lençóis Paulista (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Linhares: Linhares (ES) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Lucas do Rio Verde: Lucas do Rio Verde (MT) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Manhuaçu: Manhuaçu (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Mariana: Mariana (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Maués: Maués (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Mogi Mirim: Mogi Mirim (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Nova Mutum: Nova Mutum (MT) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Parintins: Parintins (AM) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Passos: Passos (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Pirapora: Pirapora (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Salto: Salto (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Sete Lagoas: Sete Lagoas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Sorocaba: Sorocaba (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE São Carlos: São Carlos (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE São Mateus: São Mateus (ES) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Três Pontas: Três Pontas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Três Rios: Três Rios (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Vilhena: Vilhena (RO) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Viçosa: Viçosa (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAAE Volta Redonda: Volta Redonda (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 SAAEB Ambiental: Bebedouro (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAEB Barretos: Barretos (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAEJA: Jaguariúna (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAAET: Taquaritinga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SABESP: Amparo (SP), Artur Nogueira (SP), Arujá (SP), Assis (SP), Avaré (SP), Barueri (SP), Batatais (SP), Bertioga (SP), Boituva (SP), Botucatu (SP), Bragança Paulista (SP), Caieiras (SP), Cajamar (SP), Campo Limpo Paulista (SP), Caraguatatuba (SP), Carapicuíba (SP), Caçapava (SP), Cosmópolis (SP), Cotia (SP), Cubatão (SP), Diadema (SP), Embu das Artes (SP), Embu-Guaçu (SP), Fernandópolis (SP), Ferraz de Vasconcelos (SP), Franca (SP), Francisco Morato (SP), Franco da Rocha (SP), Guarujá (SP), Guarulhos (SP), Hortolândia (SP), Ibiúna (SP), Itanhaém (SP), Itapecerica da Serra (SP), Itapetininga (SP), Itapeva (SP), Itapevi (SP), Itaquaquecetuba (SP), Itatiba (SP), Itupeva (SP), Jandira (SP), Lins (SP), Lorena (SP), Mairiporã (SP), Mauá (SP), Mococa (SP), Mogi das Cruzes (SP), Mongaguá (SP), Monte Mor (SP), Nova Odessa (SP), Olímpia (SP), Osasco (SP), Paulínia (SP), Peruíbe (SP), Piedade (SP), Pindamonhangaba (SP), Porto Feliz (SP), Poá (SP), Praia Grande (SP), Presidente Prudente (SP), Registro (SP), Ribeirão Pires (SP), Santa Bárbara d'Oeste (SP), Santa Isabel (SP), Santana de Parnaíba (SP), Santo André (SP), Santos (SP), Suzano (SP), São Bernardo do Campo (SP), São José dos Campos (SP), São João da Boa Vista (SP), São Paulo (SP), São Roque (SP), São Sebastião (SP), São Vicente (SP), Taboão da Serra (SP), Tatuí (SP), Taubaté (SP), Tremembé (SP), Tupã (SP), Ubatuba (SP), Vargem Grande Paulista (SP), Votorantim (SP), Várzea Paulista (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAE Araguari: Araguari (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAE Ituiutaba: Ituiutaba (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SAE Louveira: Louveira (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEC Catanduva: Catanduva (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAECIL Leme: Leme (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEG: Guaratinguetá (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEMA Araras: Araras (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEMAS Sertãozinho: Sertãozinho (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEP Pirassununga: Pirassununga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAERP Ribeirão Preto: Ribeirão Preto (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAESA: São Caetano do Sul (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAEV Ambiental: Votuporanga (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Brusque: Brusque (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Caxias do Sul: Caxias do Sul (RS) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Gaspar: Gaspar (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE São Bento do Sul: São Bento do Sul (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SAMAE Tangará da Serra: Tangará da Serra (MT) | Comercial, Pública, Industrial, Social |
| 🔴 SANASA Campinas: Campinas (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Comercial, Pública, Industrial, Social |
| 🔴 SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO), Catalão (GO), Cidade Ocidental (GO), Cristalina (GO), Formosa (GO), Goianira (GO), Goianésia (GO), Goiânia (GO), Inhumas (GO), Itumbiara (GO), Jataí (GO), Luziânia (GO), Mineiros (GO), Morrinhos (GO), Novo Gama (GO), Planaltina (GO), Rio Verde (GO), Santo Antônio do Descoberto (GO), Senador Canedo (GO), Trindade (GO), Valparaíso de Goiás (GO), Águas Lindas de Goiás (GO) | Comercial, Pública, Industrial, Social |
| 🔴 Saneaqua: Mairinque (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SANEAR Colatina: Colatina (ES) | Comercial, Pública, Industrial, Social |
| 🔴 SANEAR Rondonópolis: Rondonópolis (MT) | Comercial, Pública, Industrial, Social |
| 🔴 SANEBAVI Vinhedo: Vinhedo (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Saneouro: Ouro Preto (MG) | Comercial, Pública, Industrial, Social |
| 🔴 SANEP Pelotas: Pelotas (RS) | Comercial, Pública, Industrial, Social |
| 🔴 SANEPAR – Curitiba: Curitiba (PR) | Comercial, Pública, Industrial, Social |
| 🔴 SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR), Araucária (PR), Cambé (PR), Campo Largo (PR), Campo Mourão (PR), Castro (PR), Cianorte (PR), Colombo (PR), Fazenda Rio Grande (PR), Foz do Iguaçu (PR), Francisco Beltrão (PR), Guarapuava (PR), Ibiporã (PR), Irati (PR), Londrina (PR), Marechal Cândido Rondon (PR), Maringá (PR), Medianeira (PR), Paranaguá (PR), Paranavaí (PR), Pato Branco (PR), Pinhais (PR), Piraquara (PR), Ponta Grossa (PR), Rolândia (PR), Sarandi (PR), São José dos Pinhais (PR), Telêmaco Borba (PR), Toledo (PR), Umuarama (PR), União da Vitória (PR) | Comercial, Pública, Industrial, Social |
| 🔴 Sanessol: Mirassol (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS), Ponta Porã (MS), Três Lagoas (MS) | Comercial, Pública, Industrial, Social |
| 🔴 SEMAE Piracicaba: Piracicaba (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SeMAE Rio Preto: São José do Rio Preto (SP) | Comercial, Pública, Industrial, Social |
| 🔴 SEMAE São Leopoldo: São Leopoldo (RS) | Comercial, Pública, Industrial, Social |
| 🔴 SEMASA Itajaí: Itajaí (SC) | Comercial, Pública, Industrial, Social |
| 🔴 SEMASA Lages: Lages (SC) | Comercial, Pública, Industrial, Social |
| 🔴 Serviço local – Barra do Piraí: Barra do Piraí (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 São Gabriel Saneamento S.A.: São Gabriel (RS) | Comercial, Pública, Industrial, Social |
| 🔴 Tubarão Saneamento: Tubarão (SC) | Comercial, Pública, Industrial, Social |
| 🔴 Verde Alagoas: União dos Palmares (AL) | Comercial, Pública, Industrial, Social |
| 🔴 Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas Cuiabá (Iguá): Cuiabá (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas da Imperatriz: Teresópolis (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas das Agulhas Negras: Resende (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Andradina: Andradina (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Jahu: Jaú (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Juturnaíba: Araruama (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Manaus: Manaus (AM) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Matão: Matão (SP) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Niterói: Niterói (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Nova Friburgo: Nova Friburgo (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Pará de Minas: Pará de Minas (MG) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Primavera (Aegea): Primavera do Leste (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Sinop (Aegea): Sinop (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Sorriso: Sorriso (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Teresina: Teresina (PI) | Comercial, Pública, Industrial, Social |
| 🔴 Águas de Valadares (Aegea): Governador Valadares (MG) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Imperador: Petrópolis (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Pantanal (autarquia municipal): Cáceres (MT) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Paraíba: Campos dos Goytacazes (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI), Piripiri (PI) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Rio: Belford Roxo (RJ), Cachoeiras de Macacu (RJ), Duque de Caxias (RJ), Itaboraí (RJ), Japeri (RJ), Magé (RJ), Maricá (RJ), Mesquita (RJ), Nilópolis (RJ), Nova Iguaçu (RJ), Queimados (RJ), Rio Bonito (RJ), Saquarema (RJ), São Gonçalo (RJ), São João de Meriti (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Rio / Iguá / Rio+ Saneamento: Rio de Janeiro (RJ) | Comercial, Pública, Industrial, Social |
| 🔴 Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL), Penedo (AL), São Miguel dos Campos (AL) | Comercial, Pública, Industrial, Social |
| 🔴 Águas Guariroba: Campo Grande (MS) | Comercial, Pública, Industrial, Social |
| 🔴 Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Comercial, Pública, Industrial, Social |

A segunda tabela traz, para as mesmas linhas, a vigência declarada pela fonte e a data em que a página oficial foi verificada pela última vez pela rotina de monitoramento da base. Linha sem data é fonte que a rotina ainda não monitora.

<!-- tabela: **Tabela 31** — Vigência e última verificação da fonte de cada estrutura tarifária, com a situação do dado -->
| Nº | Vigência declarada | Fonte verificada em | Situação |
| ---: | :--- | :--- | :--- |
| 🟢 1 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 2 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 3 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟡 4 | Resoluções ARSP / Concessões ES | 31/08/2026 | a confirmar |
| 🟢 5 | Contas emitidas desde julho de 2026 | 31/08/2026 | auditada |
| 🟡 6 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 7 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 8 | Tabela vigente desde 30/08/2025; ainda vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 9 | Vigente desde 05/12/2025 | 31/08/2026 | a confirmar |
| 🟢 10 | Água vigente desde 05/01/2024; relação esgoto/água confirmada em 19/01/2026 | 31/08/2026 | auditada |
| 🟡 11 | Estrutura Tarifária CAER Oficial | 31/08/2026 | a confirmar |
| 🟢 12 | Vigente em 2025/2026 | 31/08/2026 | auditada |
| 🟢 13 | Vigente desde 01/04/2025 | 31/08/2026 | auditada |
| 🟢 14 | Vigente desde 01/07/2025 | 31/08/2026 | auditada |
| 🟢 15 | Resolução ADASA nº 70 | 31/08/2026 | auditada |
| 🟡 16 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 17 | Vigente desde 05/11/2025 | 31/08/2026 | a confirmar |
| 🟢 18 | Vigente desde 30/06/2025 | 31/08/2026 | auditada |
| 🟢 19 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟡 20 | Vigente desde 01/04/2026 | 31/08/2026 | a confirmar |
| 🟡 21 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟢 22 | Res. ARISB-MG 332/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 23 | Tabela aplicável desde 01/08/2025 e vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 24 | Vigente desde março de 2026 | 31/08/2026 | auditada |
| 🟡 25 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 26 | Vigente desde maio de 2026 | 31/08/2026 | auditada |
| 🟢 27 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 28 | Resolução ARPE nº 289 | 31/08/2026 | auditada |
| 🟢 29 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 30 | 22/01/2026–21/01/2027 | 31/08/2026 | a confirmar |
| 🟡 31 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 32 | Resoluções ARCON-PA 2024-2026 | 31/08/2026 | auditada |
| 🟢 33 | Vigente de 30/08/2025 a 29/08/2026 | 31/08/2026 | auditada |
| 🟢 34 | Vigente desde novembro de 2025 | 31/08/2026 | auditada |
| 🟢 35 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 36 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 37 | Resolução nº 02, de 11/02/2026 | 31/08/2026 | auditada |
| 🟢 38 | Res. 664/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 39 | Referência vigente pesquisada em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 40 | Vigente desde abril de 2023; último ato listado pela ARES-PCJ | 31/08/2026 | auditada |
| 🟡 41 | Estrutura Tarifária DAE/VG | 31/08/2026 | a confirmar |
| 🟢 42 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 43 | Vigente desde 01/03/2026 | 31/08/2026 | auditada |
| 🟡 44 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 45 | Resolução ARSAL Nº 233 | 31/08/2026 | a confirmar |
| 🟡 46 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 47 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 48 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 49 | Vigente desde 01/06/2026 | 31/08/2026 | auditada |
| 🟡 50 | Estrutura Tarifária DMAE / ARESAN | 31/08/2026 | a confirmar |
| 🟡 51 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 52 | Vigente desde 04/05/2026 | 31/08/2026 | auditada |
| 🟡 53 | Vigente desde 20/07/2026 | 31/08/2026 | a confirmar |
| 🟢 54 | Desde 01/03/2026 | 31/08/2026 | auditada |
| 🟢 55 | Vigente desde 01/08/2025 | 31/08/2026 | auditada |
| 🟢 56 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 57 | Desde 03/2026 | 31/08/2026 | a confirmar |
| 🟡 58 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 59 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 60 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 61 | Estrutura Municipal Vigente | — | a confirmar |
| 🟢 62 | Vigente desde 01/12/2025 | 31/08/2026 | auditada |
| 🟢 63 | Vigente desde abril de 2026 | 31/08/2026 | auditada |
| 🟡 64 | Deliberação AGENERSA | — | a confirmar |
| 🟡 65 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 66 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 67 | SAAE: efeitos desde 09/06/2026; Res. ARSP 103/2026 | 31/08/2026 | a confirmar |
| 🟡 68 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 69 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 70 | Vigente desde 28/12/2025 | 31/08/2026 | a confirmar |
| 🟡 71 | Res. 704/2026; desde 07/2026 | 31/08/2026 | a confirmar |
| 🟡 72 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 73 | Res. ARISB-MG 361/2025; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 74 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 75 | Res. ARES-PCJ 699/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 76 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 77 | Vigente desde agosto de 2026 | 31/08/2026 | a confirmar |
| 🟡 78 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 79 | Vigente desde junho de 2026 | 31/08/2026 | a confirmar |
| 🟡 80 | Res. 713/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 81 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 82 | Res. ARISB-MG 373/2025; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 83 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 84 | Resoluções ARSP / Concessões ES | 31/08/2026 | a confirmar |
| 🟡 85 | Tabela oficial de 2026 | 31/08/2026 | a confirmar |
| 🟡 86 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 87 | Desde 01/2026 | 31/08/2026 | a confirmar |
| 🟡 88 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 89 | Vigente desde julho de 2026 | 31/08/2026 | a confirmar |
| 🟡 90 | Vigente desde abril de 2025; mantida como vigente pelo SAAE em 24/08/2026 | 31/08/2026 | a confirmar |
| 🟡 91 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 92 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 93 | Res. ARISB-MG 367/2025 c/ correção 377/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 94 | Vigente desde novembro de 2025 | — | a confirmar |
| 🔴 95 | Vigente desde 03/03/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 96 | Res. 703/2026; desde 07/2026 | 31/08/2026 | a confirmar |
| 🟡 97 | Vigente desde setembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 98 | 26/02/2026–25/02/2027; Res. ARSP 098/2026 | 31/08/2026 | a confirmar |
| 🟡 99 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 100 | Regulação Oficial | — | a confirmar |
| 🟡 101 | Resoluções AGERO / CAERD | 31/08/2026 | a confirmar |
| 🟡 102 | Resolução ARIS-MG nº 227/2026 | 31/08/2026 | a confirmar |
| 🟡 103 | Decreto Municipal | — | a confirmar |
| 🔴 104 | Desde 03/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 105 | Vigente desde setembro de 2025; tabela sucessora ainda não aplicável na data de corte | 31/08/2026 | a confirmar |
| 🟡 106 | Res. 696/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 107 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 108 | Res. 697/2026; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 109 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 110 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 111 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 112 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 113 | Res. 659/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 114 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 115 | Res. ARISB-MG 368/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 116 | Res. ARISB-MG 371/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 117 | Resolução ARES-PCJ nº 687/2026 | 31/08/2026 | auditada |
| 🟢 118 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟢 119 | Tabela da Resolução ARES-PCJ nº 680/2025 vigente em 2026 | 31/08/2026 | auditada |
| 🟢 120 | Vigente desde 15/03/2026 | 31/08/2026 | auditada |
| 🟢 121 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 122 | Tabela da Resolução ARES-PCJ nº 678/2025 vigente em 2026 | 31/08/2026 | auditada |
| 🔴 123 | Res. 695/2026; vigente em 19/08/2026 | 31/08/2026 | estrutura incompleta |
| 🟢 124 | Vigente desde maio de 2026 | 31/08/2026 | auditada |
| 🔴 125 | Res. 694/2026; vigente em 19/08/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 126 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 127 | Vigente no exercício de 2026 | 31/08/2026 | auditada |
| 🟢 128 | Água desde 01/01/2026; esgoto desde 01/04/2026 | 31/08/2026 | auditada |
| 🟢 129 | Tarifa de água vigente desde 17/05/2026; esgoto ainda não faturado no cenário atual | 31/08/2026 | auditada |
| 🟢 130 | Vigente desde 01/07/2026 | 31/08/2026 | auditada |
| 🟢 131 | Tarifa de água vigente desde 01/07/2026; adicional de esgoto condicionado à unidade atendida | 31/08/2026 | auditada |
| 🟢 132 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟢 133 | Resolução ARES-PCJ nº 686/2026 | 31/08/2026 | auditada |
| 🟢 134 | 01/08/2026 | 31/08/2026 | auditada |
| 🟡 135 | Resoluções AGER-MT / Concessões | 31/08/2026 | a confirmar |
| 🟢 136 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 137 | Vigente desde julho de 2025 | 31/08/2026 | auditada |
| 🟢 138 | Desde 01/04/2026 | 31/08/2026 | auditada |
| 🟢 139 | Res. ARSESP 1787/2026; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 140 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 141 | Estrutura Tarifária SANEAR | 31/08/2026 | a confirmar |
| 🟢 142 | Vigente desde agosto de 2026 | 31/08/2026 | auditada |
| 🟢 143 | Tabela jan/2026 - Res. ARISB-MG 369/2025 | 31/08/2026 | auditada |
| 🟢 144 | Vigente de 07/2026 a 06/2027 | — | auditada |
| 🟡 145 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 146 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 147 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 148 | Portaria AGEMS 315 / SANESUL | 31/08/2026 | auditada |
| 🟢 149 | Res. 638/2025 adotada no corte 19/08/2026 | 31/08/2026 | auditada |
| 🟢 150 | Vigente em agosto de 2026, após o prazo legal mínimo | 31/08/2026 | auditada |
| 🟢 151 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟢 152 | Vigente para faturas com vencimento desde 05/10/2025 | 31/08/2026 | auditada |
| 🟢 153 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟡 154 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 155 | 2026 vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 156 | Vigente de 01/05/2026 a 30/04/2027 | 31/08/2026 | auditada |
| 🟢 157 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟡 158 | Resoluções AGER-MT / Concessões | 31/08/2026 | a confirmar |
| 🟢 159 | Vigente desde 20/03/2025 | 31/08/2026 | auditada |
| 🟢 160 | Vigente desde 06/01/2026 | 31/08/2026 | auditada |
| 🟡 161 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 162 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 163 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟡 164 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 165 | Vigente desde 01/12/2025 | 31/08/2026 | auditada |
| 🟡 166 | Vigente desde fevereiro de 2026 | 31/08/2026 | a confirmar |
| 🟢 167 | Res. 665/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 168 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 169 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 170 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 171 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟢 172 | Estrutura vigente após as parcelas/reajustes de junho de 2026 | 31/08/2026 | auditada |
| 🟢 173 | Vigente desde novembro de 2025 | 31/08/2026 | auditada |
| 🟢 174 | Vigente desde 28/06/2026 | 31/08/2026 | auditada |
| 🟢 175 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 176 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 177 | Tabela oficial consultada em 24/08/2026 | 31/08/2026 | auditada |
| 🟡 178 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 179 | Vigente desde 01/03/2026 | — | auditada |
| 🟡 180 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 181 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 182 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟢 183 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 184 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 185 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 186 | Vigente desde 03/01/2026 | 31/08/2026 | auditada |
| 🟢 187 | Estrutura tarifária 2026; aplicação publicada para março de 2026 | 31/08/2026 | auditada |

Os municípios da CORSAN cobram pela fórmula exponencial `PB × Cⁿ + SB` (seção 3.3 (volume Guias de uso)), sem preço por faixa; o expoente `n` é o da coluna da categoria na Tabela de Exponenciais.

<!-- tabela: **Tabela 32** — A fórmula exponencial da CORSAN em cada tabela tarifária e categoria coletada -->
| Municípios | Categoria | PB (R$/m³) | SB (R$/mês) | Esgoto (R$/m³) |
| :--- | :--- | ---: | ---: | ---: |
| Erechim (RS) | Residencial | 6,95 | 32,95 | 4,86 |
| Erechim (RS) | Comercial | 7,90 | 58,79 | 5,53 |
| Erechim (RS) | Pública | 7,90 | 117,40 | 5,53 |
| Santa Cruz do Sul (RS) | Residencial | 7,91 | 37,50 | 5,53 |
| Canoas (RS), Esteio (RS) | Residencial | 8,68 | 41,20 | 6,07 |
| Santa Cruz do Sul (RS) | Comercial | 8,98 | 66,92 | 6,28 |
| Santa Cruz do Sul (RS) | Pública | 8,98 | 133,64 | 6,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Residencial | 9,15 | 43,39 | 6,40 |
| Canoas (RS), Esteio (RS) | Comercial | 9,88 | 73,48 | 6,91 |
| Canoas (RS), Esteio (RS) | Pública | 9,88 | 146,79 | 6,91 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Comercial | 10,41 | 77,41 | 7,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Pública | 10,41 | 154,64 | 7,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS), Cachoeira do Sul (RS), Cachoeirinha (RS), Camaquã (RS), Campo Bom (RS), Capão da Canoa (RS), Carazinho (RS), Cruz Alta (RS), Farroupilha (RS), Gravataí (RS), Guaíba (RS), Ijuí (RS), Lajeado (RS), Montenegro (RS), Parobé (RS), Passo Fundo (RS), Rio Grande (RS), Santa Maria (RS), Santa Rosa (RS), Santo Ângelo (RS), Sapiranga (RS), Sapucaia do Sul (RS), São Borja (RS), Taquara (RS), Tramandaí (RS), Vacaria (RS), Venâncio Aires (RS), Viamão (RS) | Industrial | 11,83 | 154,64 | 8,28 |

---

## Apêndice E — Base climática

![Logotipo do conjunto de dados CLIMBra](../figuras/CLIMBra.jpg)

---

### E.1. O que a base contém

<!-- tabela: **Tabela 33** — Conteúdo da base climática nacional -->
| O que a base traz | Quantidade |
| :--- | ---: |
| cidades brasileiras | 652 |
| modelos climáticos do CMIP6 | 19 |
| cenários de emissão | 2, SSP2-4.5 e SSP5-8.5 |
| simulações por cidade e modelo | 3: histórica, SSP2-4.5 e SSP5-8.5 |
| total de séries temporais | 37.164 séries |
| formato original descompactado | ~6,5 GB (CSVs) |
| formato compilado do Netuno 5 | Banco SQLite comprimido (`climbra.db`) |

Cada série é um registro diário contínuo de precipitação, em milímetros, para uma combinação de
cidade, modelo e simulação: 652 cidades × 19 modelos × 3 simulações dão as 37.164
séries. As séries vêm do **CLIMBra** (Ballarin et al., 2023, [*Scientific Data / Nature*](https://www.nature.com/articles/s41597-023-01956-z), [doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z); repositório [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316), [doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)), corrigidas de viés por
*Quantile Delta Mapping* contra a grade diária de Xavier, King e Scanlon (2016), com
resolução de 0,25°. A histórica cobre de 1980 a 2013 (12.419 dias) e as futuras, de 2015 a 2100 (31.411 dias); as
janelas de estudo são recortes livres dessas séries. Todas estão em calendário
gregoriano. Os modelos HadGEM3-GC31-LL, KACE e UKESM1-0-LL, que usam originalmente anos
de 360 dias, têm um dia a menos no fim de cada série, o que não afeta o recorte.

---

### E.2. Embarque no executável e formato otimizado

Para evitar a manipulação morosa de dezenas de milhares de arquivos de texto e viabilizar
a distribuição direta no instalador e executável do Netuno 5, as 37.164 séries foram
compiladas e indexadas em um banco de dados **SQLite de alta eficiência** (`climbra.db`), com
compressão binária por série via `zlib`.

- **Velocidade de acesso:** O acesso indexado no banco leva **menos de 1 milissegundo** por série, contra dezenas de milissegundos na abertura e parse de arquivos CSV em disco.
- **Transparência:** O motor de dados climáticos do Netuno 5 prioriza o banco compilado e recorre automaticamente à pasta de arquivos `.csv` soltos se o banco não for encontrado.
- **Portabilidade:** Permite ao instalador do Netuno 5 fornecer a base nacional pronta para uso sem exigir download manual e descompactação de 6,5 GB pelo usuário.

---

### E.3. Os cenários

As duas trajetórias socioeconômicas compartilhadas do CMIP6 disponíveis na base, as *Shared Socioeconomic Pathways*, estão desenhadas na seção 3.2 (volume Guias de uso): o SSP2-4.5 é a trajetória intermediária e o SSP5-8.5 supõe emissões altas sem mitigação. O CLIMBra não inclui cenários de mitigação forte, como o SSP1-2.6.


---

### E.4. As séries históricas que acompanham o programa

Independentes da base CMIP6, quatro séries históricas longas acompanham a
instalação, na pasta `data/rainfall` do programa:

<!-- tabela: **Tabela 34** — Séries históricas de precipitação distribuídas com o programa -->
| Cidade | Arquivos |
| :--- | ---: |
| Florianópolis | 3 |
| Brasília | 3 |
| Manaus | 3 |
| São Paulo | 3 |

A série de Florianópolis usada no tutorial tem 86 anos; os trinta primeiros anos
somam 1.795 mm anuais médios, com chuva em 46% dos dias.

---

### E.5. O que declarar num estudo

- **modelo ou modelos**, pelo nome, e o critério de seleção;
- **cenário** SSP;
- **janela temporal**, com os anos;
- a **série histórica** usada como referência;
- se houve *downscaling* ou correção de viés, e qual;
- a **procedência e a versão** da base.

A seção 3.2 (volume Guias de uso) trata da condução do estudo com cenários futuros, e alerta para o erro de
escolher o modelo pelo resultado.

---

## Apêndice F — Arquivos, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

### F.1. O que o programa lê

<!-- tabela: **Tabela 35** — Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.netuno` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto do Netuno 4 ou da série 5.0 inicial | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia | etapa 1. Projeto e Chuva |
| demanda diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de demanda, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um arquivo desses, o programa avisa e adota os valores
> padrão para o que falta. A seção 3.8 (volume Guias de uso) mostra o que conferir depois de importar.

---

### F.2. O que o programa escreve

<!-- tabela: **Tabela 36** — Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.netuno` | todos os parâmetros e a série de chuva | Salvar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| planilha | `.xlsx` | série diária, varredura e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV você escolhe o separador: **ponto e vírgula** para abrir no Excel
em português, **vírgula** para o padrão internacional. Escolher errado faz a planilha
abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um arquivo JSON com as
propriedades dos componentes, para compatibilização BIM. A seção 3.9 (volume Guias de uso) trata de todos.

---

### F.3. O arquivo de projeto, por dentro

O `.netuno` é um arquivo de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete seções:

<!-- tabela: **Tabela 37** — As sete seções do arquivo de projeto e o que cada uma guarda -->
| Seção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a motobomba |
| `water_quality_and_etap` | classe-alvo, desinfecção e tratamento |
| `financial_and_economic` | tarifas, impostos, reajustes e prazo |

O apêndice A lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do arquivo.** É o que torna o projeto reproduzível:
> quem receber o arquivo obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um arquivo e muito para um anexo de e-mail com
> vinte deles.

---

### F.4. Onde ficam as coisas

<!-- tabela: **Tabela 38** — Localização dos arquivos do programa e dos arquivos do usuário -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Netuno 5` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| a base de tarifas dos 652 municípios | dentro do programa |
| os casos do manual | na pasta do programa, em `casos` |
| os três estudos de referência | na pasta do programa, em `exemplos` |
| a base climática nacional, se instalada | onde o instalador dela indicar |
| **os seus projetos e relatórios** | **onde você escolher ao salvar** |

O programa não cria pasta de trabalho nem guarda arquivos escondidos. Cada gravação
pergunta o destino, e nada do que você produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada seu.

---

### F.5. Compatibilidade entre versões

<!-- tabela: **Tabela 39** — Compatibilidade entre versões do arquivo de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o padrão |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto do Netuno 4 em CSV | abre com aviso; confira o que a seção 3.8 (volume Guias de uso) lista |
| arquivo JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um arquivo JSON que não seja um projeto do Netuno
poderia, em princípio, ser aceito e preenchido com valores padrão — e o usuário
simularia 100 m² acreditando simular os 180 m² que o arquivo descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.

---

## Apêndice G — Glossário

Termos técnicos e siglas, com o equivalente em inglês quando ele é usado na
literatura, acompanhados das diretrizes de padronização terminológica do Netuno 5.

---

**AAC** (*aproveitamento de água de chuva*). Emprego de água precipitada sobre coberturas
para usos não potáveis em edificações, regulamentado no Brasil pela ABNT NBR 15527:2019.
Deve-se preferir o termo «aproveitamento» a «reúso», uma vez que a água de chuva captada
na cobertura é um recurso primário e não um efluente gerado por uso antrópico anterior.

**ABNT**. Associação Brasileira de Normas Técnicas, o organismo que publica as normas
brasileiras. Uma norma é identificada pela sigla NBR seguida do número e do ano da
edição, como em ABNT NBR 15527:2019.

**ACV** (*life cycle assessment*). Avaliação de ciclo de vida. Método que contabiliza os
impactos ambientais de um produto ao longo de toda a sua existência, da extração das
matérias-primas ao descarte. A do programa é de **triagem**, e não um inventário completo
conforme a ISO 14040.

**Água de chuva** (*rainwater*). Precipitação atmosférica coletada diretamente em
superfícies impermeáveis de cobertura (telhados e lajes impermeabilizadas), antes de atingir
o solo ou galerias públicas. É o termo técnico-normativo oficial consagrado pela ABNT NBR
15527:2019. Deve-se utilizar rigorosamente «água de chuva» para designar o recurso natural
e a fonte hídrica captada, evitando a forma coloquial «água da chuva».

**Água não potável** (*non-potable water*). Água que não se destina ao consumo humano direto,
mas atende aos padrões de qualidade física, química e microbiológica estabelecidos por
normas específicas (como a Tabela 1 da ABNT NBR 15527:2019 e a ABNT NBR 16783:2019) para
usos admitidos: descargas em bacias sanitárias e mictórios, lavagem de veículos, calçadas e
pisos, irrigação paisagística, lavagem de roupas e torres de resfriamento.

**Água pluvial** (*stormwater*, *pluvial water*). Água de chuva que escoa superficialmente
por superfícies urbanas ou é conduzida por canalizações e sistemas prediais de drenagem
(ABNT NBR 10844). No Netuno, o termo aplica-se preferencialmente à infraestrutura predial
e aos componentes de engenharia: *sistema de aproveitamento de água pluvial (SAAP)*, *rede
pluvial*, *demanda pluvial*, *consumo de água pluvial* e *extravasamento pluvial*.

**Água potável** (*potable water*, *drinking water*). Água que atende integralmente aos
padrões de potabilidade definidos pela Portaria GM/MS nº 888/2021 do Ministério da Saúde,
destinada à ingestão direta, preparação de alimentos e higiene pessoal.

**ANEEL**. Agência Nacional de Energia Elétrica, que homologa as tarifas das
distribuidoras de energia. O Netuno lê delas o preço da energia do bombeamento, e a
atualização das tarifas é feita a partir dos dados abertos da agência.

**AQUA-HQE**. Referencial de certificação ambiental de edificações, adaptação brasileira
do francês HQE conduzida pela Fundação Vanzolini. No referencial residencial de 2024, a
água é tratada no tema «Consumo de água», em itens classificados nos níveis PR, HQE,
HQE 2 e HQE 3.

**Área de captação** (*catchment area*). Área projetada na **horizontal** da superfície
impermeável da cobertura onde a água é captada, conforme o item 3.6 da NBR 15527:2019.
Não é a área inclinada do telhado, nem a área de contribuição da NBR 10844, que serve
ao dimensionamento de calhas.

**Bandeira tarifária**. Acréscimo ou desconto sobre a tarifa de energia elétrica,
conforme as condições de geração. Verde, amarela, vermelha 1, vermelha 2, e a
modalidade branca.

**BD+C** (*Building Design and Construction*). Família de referenciais do LEED
para projeto e construção de edificações novas ou em grande reforma. É a família
tratada neste manual, nas versões 4, 4.1 e 5.

**BIM** (*building information modeling*). Modelagem da informação da construção.
Representação digital da edificação em que cada componente carrega propriedades além da
geometria, o que permite compatibilizar projetos de disciplinas diferentes.

**BRL**. Sigla da Edição Brasil do programa, a que traz os dados brasileiros: base
climática CLIMBra, tarifas de 652 municípios, energia da ANEEL, custos em reais e
certificações nacionais. A seção 1.2 (volume Comece aqui) compara as duas edições.

**CAD** (*computer-aided design*). Desenho assistido por computador. O programa exporta o
esquema hidráulico em DXF, formato de intercâmbio aceito pelos programas de CAD.

**CAPEX** (*capital expenditure*). Investimento inicial.

**CASAN**. Companhia Catarinense de Águas e Saneamento, a concessionária de água e esgoto
de Florianópolis e de boa parte de Santa Catarina. A estrutura tarifária dela é a adotada
no tutorial deste manual.

**CDD** (*consecutive dry days*). Maior sequência de dias consecutivos com chuva
abaixo de 1 mm.

**CMIP6**. Sexta fase do *Coupled Model Intercomparison Project*, o exercício
internacional coordenado que produz as projeções climáticas usadas pelos relatórios do
IPCC. A base climática do programa deriva dele.

**CLIMBra** (*Climate Change Dataset for Brazil*). Conjunto de dados meteorológicos diários em grade de alta resolução (0,25° × 0,25°, ~28 km) para todo o Brasil, cobrindo 19 modelos climáticos globais do CMIP6 e cenários de emissões SSP2-4.5 e SSP5-8.5. Desenvolvido por Ballarin et al. (2023) na revista [*Scientific Data* (Nature)](https://www.nature.com/articles/s41597-023-01956-z) ([doi:10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)) e disponibilizado publicamente no [*Science Data Bank*](https://doi.org/10.57760/sciencedb.02316) ([doi:10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)). As projeções brutas foram corrigidas de viés pelo método *Quantile Delta Mapping* (QDM) utilizando como referência observacional a base de Xavier, King e Scanlon (2016). No Netuno 5, o CLIMBra constitui a Base de dados CLIMBra para 652 cidades brasileiras (série histórica de 1980 a 2013 e projeções futuras contínuas de 2015 a 2100).

**Coeficiente de escoamento** (*runoff coefficient*). Fração da chuva que
efetivamente chega ao reservatório, descontadas perdas por absorção, evaporação e
molhamento inicial da cobertura.

**Comprimento representativo de série de precipitação** (*representative rainfall time series length*, $N_{rep}$).
Menor período contínuo em anos de dados diários de chuva necessário para estabilizar
estatisticamente o dimensionamento e o desempenho do sistema (reproduzindo o volume ideal
e o potencial de economia da série completa sob confiança $\ge 90\%$), segundo a
metodologia de Geraldi e Ghisi (2017, 2018, 2019). O comprimento necessário não é uma
constante geográfica fixa: cresce com a fração atendível e com o nível de demanda da edificação.

**Confiabilidade temporal** ($C_t$). Percentual de dias em que o sistema atendeu
plenamente ($V_{con,t} = D_{pl,t}$), parcialmente ou não atendeu a demanda pluvial.

**Confiabilidade volumétrica** ($C_v$). Fração da demanda **pluvial** que o sistema atendeu
($C_v = \sum V_{con} / \sum D_{pl} = E_{pot} / f$). Não confundir com o potencial de economia,
que tem no denominador a demanda total da edificação.

**CORSAN**. Companhia Riograndense de Saneamento, a concessionária de água e esgoto de boa
parte do Rio Grande do Sul. Fatura a água pela fórmula exponencial `PB × Cⁿ` somada ao
serviço básico, e não por faixas de consumo.

**CSV** (*comma-separated values*). Formato de arquivo de texto em que cada linha é um
registro e as colunas são separadas por um caractere, tipicamente vírgula ou ponto e
vírgula. É o formato das séries de precipitação.

**CV**. Cavalo-vapor, unidade de potência equivalente a 0,7355 kW, corrente no comércio
de motobombas no Brasil. Uma motobomba de meio CV tem 0,37 kW de potência de eixo.

**CWD** (*consecutive wet days*). Maior sequência de dias consecutivos com chuva
igual ou superior a 1 mm.

**Demanda estocástica** (*stochastic water demand*). Modelagem do consumo diário de água como
variável probabilística que varia dia a dia e entre realizações (Silva e Ghisi, 2016),
permitindo avaliar a faixa de incerteza do dimensionamento e dos indicadores de desempenho
sob variabilidade real de uso.

**Demanda pluvial** (*pluvial demand*, $D_{pl}$). Parcela da demanda diária de água da
edificação que pode ser suprida pelo sistema de aproveitamento ($D_{pl,t} = D_{tot,t} \times f$).
Corresponde aos pontos de consumo não potável interligados à rede pluvial.

**Descarte de primeiras águas** (*first flush*). Lâmina inicial de chuva desviada do
sistema, que carrega a sujeira depositada na cobertura (mínimo de 2 mm conforme a NBR
15527:2019). No Netuno 5 é **subtraída** da chuva do dia; no Netuno 4 era tratada como
limiar do evento.

**Disponibilidade**. Regime tarifário em que um valor fixo **soma** por cima do
consumo medido. Cada metro cúbico economizado desconta.

**DN** (*diâmetro nominal*). Designação comercial do diâmetro de um tubo ou conexão, em
milímetros. Não corresponde exatamente ao diâmetro interno nem ao externo: é um número de
referência do qual decorrem as dimensões reais, tabeladas por norma.

**DXF** (*drawing exchange format*). Formato de intercâmbio de desenhos técnicos, lido
por praticamente todos os programas de CAD.

**EAU**. Prefixo dos itens do tema «Consumo de água» no referencial AQUA-HQE, do francês
*eau*, água. Os itens ligados ao aproveitamento pluvial são o EAU.1.2, o EAU.1.3 e o
EAU.1.5.

**EDGE** (*excellence in design for greater efficiencies*). Referencial de certificação
da International Finance Corporation, do Banco Mundial. Mede economia percentual contra
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
de entrada, desinfecção e filtro de polimento.

**ETCCDI** (*Expert Team on Climate Change Detection and Indices*). Grupo de trabalho
internacional que padronizou os índices de extremos climáticos, dos quais o programa
calcula oito.

**Extravasamento** (*spillage*, *overflow*). Volume que excede a capacidade do reservatório
e é conduzido pelo extravasor quando ele já está cheio.

**Fração atendível por água pluvial** (*non-potable demand share*, $f$). Percentual da demanda
total de água da edificação ($D_{tot}$) passível de suprimento por água de chuva ($f = D_{pl} / D_{tot}$).
Representa o **teto assintótico intransponível** do potencial de economia de água potável
($E_{pot} \le f$): mesmo sob capacidade infinita de armazenamento e precipitação ilimitada,
a economia de potável nunca ultrapassa a fração atendível, pois o restante ($1 - f$) é
reservado aos usos nobres e potáveis. Distingue-se da confiabilidade volumétrica ($C_v = E_{pot} / f$),
que avalia o atendimento da parcela pluvial.

**Franquia no mínimo**. Regime tarifário em que o valor fixo já inclui um volume de
consumo. Economizar **abaixo** da franquia não reduz a fatura.

**Ganho marginal**. Variação do potencial de economia por metro cúbico acrescentado
ao reservatório, em %/m³ ($\Delta E_{pot} / \Delta V$). Critério de escolha do volume ideal.

**GRI** (*Global Reporting Initiative*). Padrão internacional de divulgação corporativa
de desempenho socioambiental. Sua série 303 trata de água e efluentes.

**HQE** (*Haute Qualité Environnementale*). Referencial francês de alta qualidade
ambiental, base do AQUA-HQE. Designa também os níveis dos itens do referencial: HQE,
HQE 2 e HQE 3, em ordem crescente de exigência, acima do pré-requisito (PR).

**IFC**. A sigla designa duas coisas distintas. Em certificação, é a *International
Finance Corporation*, do Banco Mundial, que desenvolve o EDGE. No contexto BIM, é o
*Industry Foundation Classes*, formato aberto de intercâmbio que o programa **não**
exporta: a exportação BIM do programa é um arquivo JSON de propriedades.

**INT**. Sigla da *International Edition* do programa: abre em inglês e não traz dados
brasileiros. Tarifas, custos, moeda e fatores de emissão são informados pelo usuário.

**IPCC** (*Intergovernmental Panel on Climate Change*). Painel intergovernamental que
sintetiza o conhecimento científico sobre mudança do clima e organiza os relatórios de
avaliação a que as projeções climáticas se referem.

**IPTU verde**. Desconto no imposto predial concedido por alguns municípios a edificações
que adotam medidas de sustentabilidade, entre elas o aproveitamento de água pluvial. O
percentual e as condições variam por legislação municipal.

**ISO 14040**. Norma internacional que estabelece os princípios e a estrutura da
avaliação de ciclo de vida. Um inventário conforme a ISO 14040 exige rastreabilidade de
cada fluxo e revisão crítica externa, requisitos que uma avaliação de triagem não cumpre.

**JSON** (*JavaScript object notation*). Formato de arquivo de texto estruturado, legível
por pessoas e por programas. É o formato interno do arquivo `.netuno`.

**LCOW** (*levelized cost of water*). Custo nivelado da água: razão entre o valor presente
de todos os custos do ciclo de vida do sistema (CAPEX, substituições, O&M, energia e
produtos químicos) e o volume descontado de água pluvial consumida ao longo do horizonte
de análise, em R$/m³. Permite confrontar a viabilidade econômica do sistema diretamente
com a tarifa da concessionária.

**LEED** (*leadership in energy and environmental design*). Referencial de certificação
ambiental de edificações do *U.S. Green Building Council*, o mais difundido
internacionalmente. Trata eficiência hídrica na categoria *Water Efficiency*: na versão 4,
pelos créditos WEc1 e WEc2; na versão 5, pelo crédito WEc2, *Enhanced Water Efficiency*.

**m.c.a.** Metro de coluna d'água, unidade de pressão equivalente à exercida por uma
coluna de água de um metro de altura, cerca de 9,81 kPa. É a unidade usual em instalações
prediais.

**Micromedição**. Medição individualizada por unidade habitacional em edifício
multifamiliar. Informada ao programa como número de economias.

**Manuais do Netuno 5** (*Netuno 5 manual suite*). A documentação do programa, montada
das mesmas fontes em três formatos: o manual completo, sete volumes avulsos, cada um com
uma parte dele, e o site de documentação. Os volumes servem a quem precisa de uma parte
só, para consultar ou enviar:

1. **Manual completo**: todos os capítulos e apêndices.
   ![Capa do Manual Completo](../figuras/capas/capa_completo.png)
2. **Volume 1 — Comece aqui**: o que o programa faz, como instalá-lo e por onde entrar
   conforme o seu objetivo.
   ![Capa do Volume 1 — Comece Aqui](../figuras/capas/capa_1-comece-aqui.png)
3. **Volume 2 — O método**: as equações, os critérios e as fontes por trás de cada número
   que o programa publica.
   ![Capa do Volume 2 — O Método](../figuras/capas/capa_2-metodo.png)
4. **Volume 3 — Guias de uso**: outras cidades, clima futuro, tarifas, demanda variável,
   lote, sensibilidade e exportação.
   ![Capa do Volume 3 — Guias Práticos](../figuras/capas/capa_3-guias.png)
5. **Volume 4 — Tutorial**: um projeto de residência em Florianópolis, do primeiro dado ao
   volume recomendado.
   ![Capa do Volume 4 — Tutorial](../figuras/capas/capa_4-tutorial.png)
6. **Volume 5 — Enganos, limitações e confiabilidade**: os enganos mais comuns, os limites
   do modelo e como o programa é verificado.
   ![Capa do Volume 5 — Confiabilidade](../figuras/capas/capa_5-confiabilidade.png)
7. **Volume 6 — Correções, bugs e versionamento**: o que mudou desde o Netuno 4, as
   mensagens de erro e como relatar um problema.
   ![Capa do Volume 6 — Versões](../figuras/capas/capa_6-versoes.png)
8. **Volume 7 — Apêndices**: parâmetros, processos, fatores de emissão, tarifas, base
   climática, formatos, glossário e referências.
   ![Capa do Volume 7 — Apêndices](../figuras/capas/capa_7-apendices.png)

Os PDFs acompanham o programa e abrem pela etapa 9. Documentação; o manual existe também
em inglês, na íntegra.

**NBR**. Norma Brasileira, publicada pela ABNT. As mais citadas neste manual são a NBR
15527, de aproveitamento de água de chuva, a NBR 10844, de instalações prediais de águas
pluviais, a NBR 5626, de sistemas prediais de água fria e quente, e a NBR 17094-2, de
motores de indução.

**Payback de carbono**. Tempo para a economia anual líquida de emissões pagar o
carbono incorporado na fabricação do sistema.

**Payback descontado**. Tempo para o fluxo de caixa descontado acumulado cruzar zero.

**PB**. Preço-base, em R$/m³, da fórmula exponencial da CORSAN, `PB × Cⁿ`, em que `C` é o
consumo do mês e `n` o expoente da tabela exponencial para aquele consumo.

**PEAD**. Polietileno de alta densidade, material dos reservatórios plásticos mais
comuns no mercado brasileiro.

**Piso de pagamento**. Regime tarifário em que a fatura **não fica** abaixo de um
valor. Diferente de disponibilidade: o piso limita por baixo, a disponibilidade soma
por cima.

**Potencial de economia de água potável** (*potable water saving potential*, $E_{pot}$).
Fração da demanda **total** da edificação suprida por água pluvial ($E_{pot} = \sum V_{con} / \sum D_{tot} \times 100\%$).
É o indicador central do programa, limitado superiormente pela fração atendível ($E_{pot} \le f$).

**pp**. Pontos percentuais. Usado para exprimir a diferença entre dois percentuais: de
35% para 37% vão dois pontos percentuais, e não dois por cento.

**PR**. Pré-requisito: no AQUA-HQE, o nível de item de atendimento obrigatório, abaixo
dos níveis HQE, HQE 2 e HQE 3.

**PRCPTOT**. Precipitação total anual em dias úmidos.

**PRFV**. Plástico reforçado com fibra de vidro, material de reservatórios de médio e
grande porte. Aparece no programa sob a designação «fibra».

**PVC**. Policloreto de vinila, material das tubulações prediais de água fria e das
colunas de desvio do descarte inicial. As dimensões dos tubos soldáveis seguem a ABNT NBR 5648.

**R95p**. Soma da precipitação dos dias acima do percentil 95 dos dias úmidos.

**Rendimento da bomba**. Razão entre a potência hidráulica entregue à água e a
potência mecânica no eixo. Não inclui o motor.

**Rendimento do motor**. Razão entre a potência mecânica no eixo e a potência
elétrica consumida da rede. A ABNT NBR 17094-2 manda marcá-lo na placa.

**RX1day**, **RX5day**. Maior precipitação em um e em cinco dias consecutivos, no
ano.

**SAAP**. Sistema de aproveitamento de água pluvial. Conjunto integrado de componentes
prediais — área de captação, condutores, descarte inicial (first flush), estação de
tratamento (ETAP), cisterna inferior, reservatório superior, grupo motobomba ou pressurizador
e rede de distribuição independente — concebido para coletar, tratar, armazenar e fornecer
água não potável em conformidade com a ABNT NBR 15527 e a ABNT NBR 5626.

**SB**. Serviço básico: a parcela fixa mensal da fatura de água da CORSAN, somada ao
resultado da fórmula exponencial.

**SDII** (*simple daily intensity index*). Precipitação média dos dias úmidos.

**SI** (*seasonality index*). Índice de sazonalidade de Walsh e Lawler. Zero quando a
chuva é uniforme ao longo do ano.

**SMAA** (*stochastic multicriteria acceptability analysis*). Método que sorteia
pesos e devolve a probabilidade de cada alternativa vencer.

**SNIS**. Sistema Nacional de Informações sobre Saneamento, base oficial brasileira de
indicadores do setor, mantida pelo governo federal. É a origem dos indicadores de
consumo energético do saneamento usados na avaliação ambiental.

**SSP** (*shared socioeconomic pathways*). Trajetórias socioeconômicas compartilhadas,
que descrevem hipóteses coerentes de desenvolvimento global e as emissões correspondentes.
Combinam-se com os modelos climáticos para produzir projeções.

**TFDI**. Tarifa fixa de disponibilidade da infraestrutura, nome que algumas
concessionárias dão à parcela da fatura cobrada independentemente do consumo. Ver
*Disponibilidade*.

**TIR**. Taxa interna de retorno. A taxa de desconto que zera o valor presente
líquido.

**TMA**. Taxa mínima de atratividade. A taxa de desconto adotada.

**TOPSIS** (*technique for order of preference by similarity to ideal solution*).
Método de ordenação multicritério de Hwang e Yoon.

**UV**. Radiação ultravioleta, empregada na desinfecção de água por inativação de
microrganismos. Atua apenas no instante da passagem pelo reator e não deixa residual, ao
contrário da cloração.

**VIKOR**. Método de decisão multicritério proposto por Opricovic, que busca uma solução
de compromisso entre critérios conflitantes. Ver também *SMAA*.

**Volume ideal** (*optimal tank volume*). Menor volume de reservatório da grade de simulação
a partir do qual o ganho marginal de economia de água potável ($\Delta E_{pot} / \Delta V$)
cai abaixo de um limiar declarado (tipicamente $1,0\%/\text{m}^3$ ou $0,5\%/\text{m}^3$).
Evita o superdimensionamento de reservatórios, assegurando a melhor relação custo-benefício.

**VPL**. Valor presente líquido.

**WEM**. Codificação das medidas de eficiência hídrica do EDGE. A WEM14 é o sistema
de aproveitamento de água pluvial.

**XLSX**. Formato de pasta de trabalho do Microsoft Excel, baseado em XML compactado. É um
dos formatos de exportação de planilhas e de resultados da linha de comando.

**YAS** (*yield after spillage*). Regra de operação em que o extravasamento é
calculado **antes** da retirada da demanda e, na forma estrita, a retirada do dia sai
só do volume guardado na véspera. O programa calcula o extravasamento antes, como a
YAS, mas deixa a chuva do dia atender a demanda do dia; fica entre a YAS e a YBS
(seção 2.1 (volume O método)).

**YBS** (*yield before spillage*). Regra de operação em que a demanda é retirada **antes**
do cálculo do extravasamento. Supõe consumo anterior à chuva do dia e superestima o
aproveitamento; o programa não a adota, e o resultado dele fica entre a YAS e a YBS.

---

### G.1. Diretrizes de Padronização e Nomenclatura no Netuno

A padronização terminológica é indispensável para assegurar a consistência e o rigor técnico
em artigos científicos, relatórios técnicos, na interface gráfica e na documentação do Netuno.
As convenções a seguir detalham a distinção de termos correlatos frequentemente confundidos:

#### G.1.1. 1. Água de Chuva versus Água Pluvial versus «Água da Chuva»

<!-- tabela: **Tabela 40** — Padronização terminológica de água de chuva e água pluvial -->
| Termo | Definição e Contexto de Aplicação | Situação no Netuno | Referência |
| :--- | :--- | :--- | :--- |
| **Água de chuva** (*rainwater*) | Precipitação atmosférica coletada diretamente na cobertura (telhado/laje impermeabilizada), antes de atingir o solo ou galerias. Refere-se à **fonte hídrica** e ao recurso ambiental. | **Canônico e preferencial** para o recurso captado («aproveitamento de água de chuva», «precipitação de água de chuva»). | ABNT NBR 15527:2019, título e item 3.1. |
| **Água pluvial** (*stormwater* / *pluvial water*) | Água de chuva após escoamento superficial urbano ou quando conduzida por canalizações e sistemas prediais de drenagem e armazenamento. Aplica-se à **infraestrutura física** e aos componentes de engenharia. | **Canônico e preferencial** para sistemas, redes e balanço («sistema predial de água pluvial - SAAP», «rede pluvial», «demanda pluvial», «extravasamento pluvial»). | ABNT NBR 10844:1989; ABNT NBR 5626:2020. |
| **«Água da chuva»** | Expressão coloquial e informal. | **Desaconselhada**. Não deve ser empregada em publicações, textos normativos, relatórios do Netuno ou código. | Prática de redação técnica e científica. |

#### G.1.2. 2. Fração Atendível, Demanda Pluvial, Potencial e Confiabilidade

Para evitar ambiguidades matemáticas e conceituais frequentemente encontradas na literatura:

<!-- tabela: **Tabela 41** — Grandezas fundamentais do balanço hídrico e relações entre fração e potencial -->
| Grandeza | Símbolo / Código | Definição | Fórmula | Relação / Teto |
| :--- | :--- | :--- | :--- | :--- |
| **Fração atendível por água pluvial** | $f$ / `rainwater_share` | Proporção da demanda total da edificação correspondente a pontos de consumo não potável conectáveis ao SAAP. | $f = D_{pl} / D_{tot}$ | Parâmetro de projeto ($0 \le f \le 1$). Constitui o **teto assintótico** de $E_{pot}$. |
| **Demanda pluvial** | $D_{pl}$ / `rainwater_demand` | Volume de água requerido pelos pontos não potáveis da edificação em um intervalo de tempo. | $D_{pl,t} = D_{tot,t} \times f$ | Em L/dia ou m³/ano. |
| **Volume de água pluvial consumido** | $V_{con}$ / `pluvial_consumed` | Volume de água não potável efetivamente suprido pelo reservatório pluvial aos pontos de consumo. | Determinado pelo balanço diário (seção 2.1 (volume O método)) | $V_{con,t} \le D_{pl,t}$ e $V_{con,t} \le S_{t-1} + C_t$. |
| **Potencial de economia de água potável** | $E_{pot}$ / `potential_potable_savings_pct` | Percentual da demanda **total** da edificação economizado pelo aproveitamento pluvial. | $E_{pot} = \frac{\sum V_{con}}{\sum D_{tot}} \times 100\%$ | **Indicador central**. Sempre $E_{pot} \le f$. |
| **Confiabilidade volumétrica** | $C_v$ / `volumetric_reliability_pct` | Percentual da demanda **pluvial** suprido pela água de chuva armazenada. | $C_v = \frac{\sum V_{con}}{\sum D_{pl}} \times 100\%$ | $C_v = \frac{E_{pot}}{f}$. Pode atingir 100% mesmo quando $E_{pot} < 100\%$. |
| **Confiabilidade temporal** | $C_t$ / `temporal_reliability_pct` | Percentual de dias da série em que a demanda pluvial foi 100% atendida ($V_{con,t} = D_{pl,t}$). | $C_t = \frac{N_{dias\_plenos}}{N_{total}} \times 100\%$ | Mede a segurança de abastecimento diário sem suplementação potável. |

#### G.1.3. 3. Síntese de Nomenclatura Recomendada para Artigos e Relatórios

- Utilize **«aproveitamento de água de chuva»** (e não «reúso de água da chuva» — água de chuva não é efluente; seu uso é *aproveitamento*, não *reúso*).
- Utilize **«área de captação»** para o plano horizontal da cobertura (NBR 15527) e reserve **«área de contribuição»** exclusivamente para o dimensionamento hidráulico de calhas sob vento (NBR 10844).
- Utilize **«descarte de primeiras águas»** ou *first flush* para a lâmina inicial desviada (mínimo de 2 mm conforme NBR 15527), e não «limiar de descarte».
- Utilize **«fração atendível»** (e não «demanda relativa» ou «fração de economia») para expressar a partição de usos não potáveis no consumo total.
- Utilize **«comprimento representativo de série»** para a extensão mínima em anos necessária para estabilização estatística da simulação (método Geraldi & Ghisi).
- Utilize **«LCOW»** ou **«custo nivelado da água»** para a métrica de custo unitário ao longo do ciclo de vida descontado à TMA.

---

## Apêndice H — Referências

Normas, publicações e bases que sustentam as decisões do programa. A lista completa,
com a proveniência de cada citação, está no módulo de bibliografia do programa e na
aba de Documentação.

---

### H.1. Normas técnicas brasileiras

**ABNT NBR 15527** — Água de chuva: aproveitamento de coberturas em áreas urbanas
para fins não potáveis. Requisitos. Estabelece os parâmetros de qualidade, o
descarte de primeiras águas e a manutenção.

**ABNT NBR 10844:1989** — Instalações prediais de águas pluviais. Procedimento.
Define a área de contribuição (item 3.2 e Figura 2), com os incrementos da inclinação e
das paredes, para a vazão de projeto de calhas e condutores; não é a área de captação do
balanço hídrico, que segue a NBR 15527:2019, item 3.6.

**ABNT NBR 16783** — Uso de fontes alternativas de água não potável em edificações.

**ABNT NBR 5626:2020** — Sistemas prediais de água fria e água quente. Projeto,
execução, operação e manutenção. Segunda edição, versão corrigida de 30/09/2020.

**ABNT NBR 15575-1:2025** — Edificações habitacionais. Desempenho. Parte 1: Requisitos
gerais. Sétima edição, 05/12/2025.

**ABNT NBR 15575-6:2021** — Edificações habitacionais. Desempenho. Parte 6: Requisitos
para os sistemas hidrossanitários. Quinta edição, 29/09/2021.

**ABNT NBR 17094-2:2016** — Máquinas elétricas girantes. Parte 2: motores de indução
monofásicos. Requisitos. A Tabela 13 traz o rendimento nominal mínimo a plena carga
da linha IR1, e a Tabela 14 o da linha IR2. A norma manda marcar o rendimento na
placa de identificação, o que estabelece que a potência de placa é a mecânica no
eixo.

**Portaria GM/MS 888/2021** — Procedimentos de controle e vigilância da qualidade da
água para consumo humano. Rege cloro residual e coliformes.

---

### H.2. Referenciais de certificação

**LEED v4 / v4.1 BD+C** — USGBC. Categoria *Water Efficiency*, créditos WEc1 e WEc2. Registro de projetos comerciais até 30 jun. 2027.

**LEED v5 BD+C** — U.S. GREEN BUILDING COUNCIL. *LEED v5 Building Design and Construction: rating system*. Washington, DC: USGBC, nov. 2025. Pré-requisitos WEp1 (*Water Metering and Reporting*) e WEp2 (*Minimum Water Efficiency*), créditos WEc2 (*Enhanced Water Efficiency*) e SSc3 (*Rainwater Management*).

**AQUA-HQE Residencial** — FUNDAÇÃO VANZOLINI; CERQUAL QUALITEL. *Referencial de avaliação
do desempenho de edifícios residenciais em construção e renovação*. Versão 00. São Paulo:
Fundação Vanzolini, 22 nov. 2024. Tema «Consumo de água», itens EAU.1.2, EAU.1.3 e EAU.1.5.

**Selo Casa Azul + CAIXA** — CAIXA ECONÔMICA FEDERAL. *Guia Selo Casa Azul + CAIXA*. V023.
Brasília: CAIXA, 29 abr. 2026. Critério 3.6, aproveitamento de águas pluviais.

**Selo Casa Azul Uni** — CAIXA ECONÔMICA FEDERAL. *Guia Selo Casa Azul Uni*. V001. Brasília:
CAIXA, dez. 2025. Critério 7, aproveitamento de águas pluviais.

**EDGE** — IFC, Grupo Banco Mundial. *EDGE Certification Process*, e a codificação
WEM das medidas de eficiência hídrica. Administrado pelo GBCI em mais de 120 países.

**GRI 303** — Global Reporting Initiative. Água e efluentes, indicadores 303-3 e
303-5.

---

### H.3. Métodos

**Hwang, C.-L.; Yoon, K.** (1981). *Multiple Attribute Decision Making: Methods and
Applications*. A formulação original do TOPSIS.

**Opricovic, S.; Tzeng, G.-H.** O método VIKOR e as condições C1 e C2 de vantagem
aceitável e estabilidade.

**Lahdelma, R.; Hokkanen, J.; Salminen, P.** (1998), e **Tervonen, T.; Figueira, J.**
(2008). SMAA e SMAA-2.

**Walsh, R. P. D.; Lawler, D. M.** (1981). O índice de sazonalidade.

**ETCCDI** — *Expert Team on Climate Change Detection and Indices*, da OMM. Os
índices de extremos climáticos.

---

**Mayer, P. W.; DeOreo, W. B. et al.** (1999). *Residential End Uses of Water*.
Denver: AWWA Research Foundation. Frequência de uso dos aparelhos: 5,05 descargas e
0,37 ciclos de máquina de lavar por pessoa por dia; as descargas são a base dos
acionamentos da pressurização direta.

**Komeco.** *Pressurizador de água TP 820T e TP 825T G2: manual do usuário*. Versão de
15/05/2007. Ficha técnica e gráfico vazão × pressão; a faixa do pressostato do TP 820T, 12
a 24 m.c.a., é a base da pressão de trabalho padrão.

**Cardal.** *Pressurizador Potenza: manual de instruções*. IM 311. Especificações
técnicas e curva vazão × pressão (figura 8).

**Jacuzzi.** *Pressurizador residencial AcquaHouse: manual de instruções*. Março de 2017.
Curvas vazão × pressão ensaiadas no Laboratório de Etiquetagem de Bombas da
Universidade Federal de Itajubá.

**Syllent (Eberle).** *Pressurizador para água quente, linha Impulse Press: manual de
instalação e operação*. Des. 3I4743. Tabela vazão × altura manométrica e retardo de
desligamento de 10 s do controle eletrônico.

**Rowa.** *Pressurizadores Max Press E: manual de instalação*, e ficha técnica do Max
Press 20E: pressão máxima de 20 m.c.a. e 5.000 L/h a 7 m.c.a.

### H.4. Normas de avaliação de ciclo de vida

**ABNT NBR ISO 14040** — Gestão ambiental: avaliação do ciclo de vida, princípios e
estrutura. Correspondente à ISO 14040:2006. As quatro fases da avaliação.

**ABNT NBR ISO 14044** — Gestão ambiental: avaliação do ciclo de vida, requisitos e
orientações. Correspondente à ISO 14044:2006.

**EN 15978:2011** — Sustainability of construction works: assessment of environmental
performance of buildings, calculation method. Os módulos A a D do ciclo de vida da
edificação.

**EN 15804:2012+A2:2019** — Sustainability of construction works: environmental product
declarations, core rules for the product category of construction products.

**EN 16941-1:2024** — On-site non-potable water systems — Part 1: Systems for the use
of rainwater. Bruxelas: CEN, 2024.

**ABNT NBR 15527:2007** — Água de chuva: aproveitamento de coberturas em áreas urbanas
para fins não potáveis. Anexo A, informativo: métodos de Rippl, da simulação, de Azevedo
Neto e práticos alemão, inglês e australiano.

---

### H.5. Dimensionamento e desempenho de sistemas de aproveitamento pluvial

**GHISI, E.; SOUZA, E. L.** (2012). Potable water savings by using rainwater for
non-potable uses in houses. *Water*, v. 4, n. 3, p. 607-628. doi:10.3390/w4030607.

**GHISI, E.; LOPES, A. C.; RUPP, R. F.** (2016). Assessment of the potential for potable
water savings by using rainwater in houses in southern Brazil. *Water Science and
Technology: Water Supply*, v. 16, n. 2, p. 533-541. doi:10.2166/ws.2015.166.

**GHISI, E.; CUSTÓDIO, D. A.** (2019). Assessing the potential for potable water savings
in the residential sector of a city: a case study of Joinville city. *Water*, v. 11,
n. 10, 2074. doi:10.3390/w11102074.

**CAMPISANO, A. et al.** (2017). Urban rainwater harvesting systems: research,
implementation and future perspectives. *Water Research*, v. 115.
doi:10.1016/j.watres.2017.02.056.

**CAMPISANO, A.; MODICA, C.** (2015). Appropriate resolution timescale to evaluate water
saving and retention potential of rainwater harvesting for toilet flushing in single
houses. *Journal of Hydroinformatics*, v. 17, n. 3. doi:10.2166/hydro.2015.022.

**FEWKES, A.; BUTLER, D.** (2000). Simulating the performance of rainwater collection and
reuse systems using behavioural models. *Building Services Engineering Research and
Technology*, v. 21, n. 2, p. 99-106. doi:10.1177/014362440002100204.

**GHISI, E.** (2010). Parameters influencing the sizing of rainwater tanks for use in
houses. *Water Resources Management*, v. 24, n. 10, p. 2381-2403.
doi:10.1007/s11269-009-9557-4.

**HASHIMOTO, T.; STEDINGER, J. R.; LOUCKS, D. P.** (1982). Reliability, resiliency, and
vulnerability criteria for water resource system performance evaluation. *Water
Resources Research*, v. 18, n. 1, p. 14-20. doi:10.1029/WR018i001p00014.

**MAYKOT, J. K.; GHISI, E.** (2020). Assessment of a rainwater harvesting system in a
multi-storey residential building in Brazil. *Water*, v. 12, n. 2, 546.
doi:10.3390/w12020546.

**PROENÇA, L. C.; GHISI, E.** (2010). Water end-uses in Brazilian office buildings.
*Resources, Conservation and Recycling*, v. 54, n. 8, p. 489-500.
doi:10.1016/j.resconrec.2009.10.005.

**SEMAAN, M. et al.** (2020). Optimal sizing of rainwater harvesting systems for domestic
water usages: a systematic literature review. *Resources, Conservation & Recycling: X*,
v. 6, 100033. doi:10.1016/j.rcrx.2020.100033.

---

### H.6. Clima futuro

**BALLARIN, A. S. et al.** (2023). CLIMBra: Climate Change Dataset for Brazil.
*Scientific Data*, v. 10. doi:10.1038/s41597-023-01956-z. A origem da base climática do
programa.

**HAWKINS, E.; SUTTON, R.** (2011). The potential to narrow uncertainty in projections of
regional precipitation change. *Climate Dynamics*, v. 37, p. 407-418.
doi:10.1007/s00382-010-0810-6.

**KISAKYE, V.; VAN DER BRUGGEN, B.** (2018). Effects of climate change on
water savings and water security from rainwater harvesting systems. *Resources,
Conservation and Recycling*. doi:10.1016/j.resconrec.2018.07.009.

**LASH, D. et al.** (2014). Robust rainwater harvesting: probabilistic tank sizing for
climate change adaptation. *Journal of Water and Climate Change*.
doi:10.2166/wcc.2014.080.

**MARAUN, D.** (2016). Bias correcting climate change simulations: a critical review.
*Current Climate Change Reports*, v. 2, n. 4, p. 211-220.
doi:10.1007/s40641-016-0050-x.

**XAVIER, A. C.; KING, C. W.; SCANLON, B. R.** (2016). Daily gridded meteorological
variables in Brazil (1980-2013). *International Journal of Climatology*, v. 36,
p. 2644-2659. doi:10.1002/joc.4518.

---

### H.7. Ciclo de vida e energia de sistemas pluviais

**GHIMIRE, S. R. et al.** (2014). Life cycle assessment of domestic and agricultural
rainwater harvesting systems. *Environmental Science & Technology*, v. 48.
doi:10.1021/es500189f.

**GHIMIRE, S. R. et al.** (2017). Life cycle assessment of a commercial rainwater
harvesting system compared with a municipal water supply system. *Journal of Cleaner
Production*. doi:10.1016/j.jclepro.2017.02.025.

**MARINOSKI, A. K.; GHISI, E.** (2018). Avaliação de viabilidade ambiental e econômica
de sistemas de aproveitamento de água pluvial em habitação de baixo padrão: estudo de
caso em Florianópolis, SC. *Ambiente Construído*, v. 18, n. 1, p. 423-443.
doi:10.1590/s1678-86212018000100230.

**VAZ, I. C. M. et al.** (2023). Sustainable rainwater management and life cycle
assessment: challenges and perspectives. *Sustainability*, v. 15, n. 16, 12133.
doi:10.3390/su151612133.

**VIEIRA, A. S. et al.** (2014). Energy intensity of rainwater harvesting systems: a
review. *Renewable and Sustainable Energy Reviews*, v. 34, p. 225-242.
doi:10.1016/j.rser.2014.03.012.

**WARD, S.; BUTLER, D.; MEMON, F. A.** (2012). Benchmarking energy consumption and CO2
emissions from rainwater-harvesting systems: an improved method by proxy. *Water and
Environment Journal*, v. 26, n. 2, p. 184-190. doi:10.1111/j.1747-6593.2011.00279.x.

---

### H.8. O programa antecessor

**Ghisi, E.; Cordova, M. M.** (2014). *Netuno 4 — Manual do Usuário*. Universidade
Federal de Santa Catarina, Departamento de Engenharia Civil, Laboratório de
Eficiência Energética em Edificações. Florianópolis, junho de 2014.

A seção 6.1 (volume Correções, bugs e versionamento) traz a comparação quantitativa entre as duas versões e a decomposição
das diferenças.

---

### H.9. Bases de dados

**CMIP6** — *Coupled Model Intercomparison Project*, fase 6. Projeções climáticas
que alimentam os relatórios do IPCC.

**ANEEL** — Dados abertos de tarifas homologadas de distribuidoras de energia
elétrica.

**Agências reguladoras estaduais e municipais de saneamento** — resoluções
tarifárias, uma por município da base.

**SNIS** — Sistema Nacional de Informações sobre Saneamento. Índices de perdas na
distribuição por macrorregião.

---

### H.10. Como citar o programa

Ao publicar um estudo feito com o Netuno 5, cite o programa **com a versão**, e
declare os itens da seção 4.10 (volume Tutorial). Um estudo que cita «Netuno» sem versão não é
reproduzível: correções entre versões mudam resultados, e a seção 2.6 (volume O método) traz o
exemplo do consumo da motobomba, que mudou 65% entre duas versões consecutivas.

---

## Apêndice I — Fichas de uma página

Resumos destacáveis. Cada ficha cabe numa página e serve de consulta rápida ao lado
do computador.

---

### I.1. Ficha 1 — O fluxo de um estudo completo

<!-- tabela: **Tabela 42** — Ficha de consulta: os dez passos de um estudo completo e a seção que trata de cada um -->
| # | Passo | O que se decide nele | Seção |
| ---: | :--- | :--- | ---: |
| 1 | Projeto e chuva | série, área, coeficiente, descarte | 4.1 (volume Tutorial) |
| 2 | Edificação | tipologia, demanda, fração atendível | 4.2 (volume Tutorial) |
| 3 | Primeira simulação | um volume de palpite, para ver | 4.3 (volume Tutorial) |
| 4 | Varredura | curva de retorno, volume ideal | 4.4 (volume Tutorial) |
| 5 | Arranjo | precisa de caixa superior? | 4.5 (volume Tutorial) |
| 6 | Qualidade | classe, desinfecção, filtros | 4.6 (volume Tutorial) |
| 7 | Economia | tarifa real, CAPEX, fluxo de caixa | 4.7 (volume Tutorial) |
| 8 | Carbono | inventário, material, payback | 4.8 (volume Tutorial) |
| 9 | Decisão | sete critérios, pesos declarados | 4.9 (volume Tutorial) |
| 10 | Relatório | saídas e lista de declaração | 4.10 (volume Tutorial) |

**Antes de publicar:** seção 4.10 (volume Tutorial), a lista de declaração. Seção 5.1 (volume Enganos, limitações e confiabilidade), os dez
enganos. Seção 5.2 (volume Enganos, limitações e confiabilidade), as limitações que afetam o seu caso.

---

### I.2. Ficha 2 — As armadilhas, em uma linha cada

<!-- tabela: **Tabela 43** — Ficha de consulta: as dez armadilhas de projeto e onde cada uma é tratada -->
| Armadilha | Onde |
| :--- | :--- |
| área **inclinada** em vez da projeção horizontal | 5.1.1 (volume Enganos, limitações e confiabilidade) |
| chuva **média mensal** em vez da série diária | 5.1.2 (volume Enganos, limitações e confiabilidade) |
| descarte em **litros** quando o campo quer milímetros | 5.1.3 (volume Enganos, limitações e confiabilidade) |
| **regime de mínimo** tarifário ignorado | 5.1.4 (volume Enganos, limitações e confiabilidade) |
| escola ou hospital com **tarifa residencial** | 5.1.5 (volume Enganos, limitações e confiabilidade) |
| esperar mais **água** da caixa superior | 5.1.6 (volume Enganos, limitações e confiabilidade) |
| **série curta** demais | 5.1.7 (volume Enganos, limitações e confiabilidade) |
| classe de qualidade escolhida pelo **custo** | 5.1.8 (volume Enganos, limitações e confiabilidade) |
| comparar com o **Netuno 4** sem declarar a divergência | 5.1.9 (volume Enganos, limitações e confiabilidade) |
| publicar o volume de **maior economia** como recomendado | 5.1.10 (volume Enganos, limitações e confiabilidade) |

---

### I.3. Ficha 3 — Os seis regimes tarifários

<!-- tabela: **Tabela 44** — Ficha de consulta: os seis regimes tarifários e o efeito da economia -->
| Regime | Ao economizar | Municípios |
| :--- | :--- | ---: |
| sem mínimo | cada m³ desconta | 165 |
| disponibilidade | cada m³ desconta; o fixo continua | 122 |
| fórmula exponencial (CORSAN) | cada m³ desconta; a conta é PB × Cⁿ + serviço básico | 34 |
| **franquia no mínimo** | **abaixo da franquia não desconta nada** | **329** |
| franquia retroativa | passando dela, tarifa tudo desde zero | 2 |
| piso de pagamento | a fatura não fica abaixo do piso | 0 |

**Teste rápido:** simule dois consumos, um dentro e um fora da faixa mínima, e
compare com uma fatura real. Se só um bater, o regime está errado.

---

### I.4. Ficha 4 — Os indicadores, e o que cada um responde

<!-- tabela: **Tabela 45** — Ficha de consulta: os indicadores e a pergunta que cada um responde -->
| Indicador | Denominador | Responde |
| :--- | :--- | :--- |
| potencial de economia | demanda **total** | quanto do consumo de água potável cai |
| confiabilidade volumétrica | demanda **pluvial** | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | dias da série | com que frequência se pode contar |
| extravasamento | — | o reservatório é pequeno? |
| ganho marginal | — | vale ampliar? |

`Epot = confiabilidade volumétrica × fração atendível`

---

### I.5. Ficha 5 — A cadeia de energia da motobomba

```
recalque:  e = ρ · g · H ÷ (η_bomba · η_motor)      kWh/m³
partidas:  E = placa × tempo ÷ η_motor              kWh
```

A placa é a potência **no eixo**. O rendimento do motor separa o eixo da tomada. Em
branco, vale a Tabela 13 da NBR 17094-2: 60,5% em meio CV, 69,3% em um CV.

---

### I.6. Ficha 6 — A lista de declaração, resumida

**Programa:** versão, com revisão.

**Chuva:** origem, recorte, anos; se projeção, modelo, cenário e janela.

**Edificação:** área e como foi obtida, coeficiente, per capita e origem, **fração
atendível** e os usos que a compõem.

**Descarte:** lâmina e modo; a divergência contra o Netuno 4, se comparar versões.

**Volume:** critério de escolha — limiar de ganho marginal, ou pesos do
multicritério.

**Economia:** município, concessionária, vigência da tabela, **regime de mínimo**,
percentual de esgoto, TMA, inflação, reajustes e período.

**Carbono:** fronteira (água entregue), vida útil, material do reservatório, base da
rede com o ano, fatores **aproximados** ou com **rótulo de triagem**.

**Certificação:** que as classes 2 a 4 são adaptações do programa; no LEED, a versão; no EDGE, que só a
barra de água foi avaliada.

---

## Apêndice J — Arquivos de exemplo

O manual imprime resultados; estes arquivos são o que se abre para
reproduzi-los. Ficam na pasta `casos` do programa, e cada um traz a série de chuva
incorporada: abrem sem o CSV de origem, em qualquer máquina.

---

### J.1. Os nove casos do manual

<!-- tabela: **Tabela 46** — Os nove casos de exemplo e o que cada um demonstra -->
| Arquivo | Seção | O que demonstra |
| :--- | :--- | :--- |
| `01_tutorial_florianopolis.netuno` | 4.1 a 4.10 | o projeto fechado do tutorial: cisterna de 4.000 L em polietileno e recalque para caixa superior de 1.000 L |
| `02_tutorial_varredura.netuno` | 4.4 e 2.2 | o projeto antes da caixa superior, em modo varredura, de 0 a 20.000 L, passo de 1.000 L |
| `03_dez_dias.netuno` | 2.1 | o caso didático de dez dias, que cabe numa planilha |
| `04_reservatorio_superior.netuno` | 4.5 | 4.000 L embaixo mais 1.000 em cima, a comparação da seção 4.5 contra os 5.000 L de um tanque só |
| `05_manaus.netuno` | 3.1 | o projeto do tutorial levado a Manaus, que chove mais e rende menos |
| `06_brasilia.netuno` | 3.1 | o projeto do tutorial levado a Brasília, de estação seca marcada |
| `07_saopaulo.netuno` | 3.1 | o projeto do tutorial levado a São Paulo |
| `08_escola_semanal.netuno` | 3.4 e 3.5 | escola de 300 alunos com demanda modulada por dia da semana |
| `09_hotel_mensal.netuno` | 3.4 | hotel de litoral com ocupação mensal em fase com a chuva |

### J.2. O que cada um produz

Os valores abaixo são obtidos **relendo o arquivo gravado** e simulando o
que foi relido, e não a configuração que o gerou. É a diferença que
importa: um parâmetro que não sobreviva à gravação aparece aqui como
número errado, em vez de passar despercebido.

<!-- tabela: **Tabela 47** — Resultado que cada caso de exemplo produz ao ser relido e simulado -->
| Arquivo | Modo | Volume | Potencial | Pluvial consumida |
| :--- | :--- | ---: | ---: | ---: |
| `01_tutorial_florianopolis.netuno` | volume fixo | 4.000 L | 27,30% | 163,8 L/dia |
| `02_tutorial_varredura.netuno` | varredura | ideal: 4.000 L | 27,12% | 21 volumes |
| `03_dez_dias.netuno` | volume fixo | 2.000 L | 36,00% | 72,0 L/dia |
| `04_reservatorio_superior.netuno` | volume fixo | 4.000 L | 27,30% | 163,8 L/dia |
| `05_manaus.netuno` | volume fixo | 4.000 L | 20,96% | 125,8 L/dia |
| `06_brasilia.netuno` | volume fixo | 4.000 L | 15,45% | 92,7 L/dia |
| `07_saopaulo.netuno` | volume fixo | 4.000 L | 25,74% | 154,4 L/dia |
| `08_escola_semanal.netuno` | volume fixo | 30.000 L | 34,34% | 3.095,8 L/dia |
| `09_hotel_mensal.netuno` | volume fixo | 25.000 L | 32,11% | 1.854,9 L/dia |

---

### J.3. Como rodar

**Arquivo, Abrir projeto**, escolha o arquivo, e o programa carrega tudo: a
chuva, a edificação, os custos e a configuração das análises. Percorra as
etapas de resultado na barra lateral para ver cada dimensão.

Os arquivos ficam na pasta `casos`, dentro da pasta de instalação do
programa. Se quiser modificá-los, **salve com outro nome**: assim o caso
original continua reproduzindo o número impresso no manual.

---

### J.4. Os três estudos de `exemplos`

Além dos casos do manual, o programa traz três estudos de referência em
`exemplos`: residência unifamiliar em Florianópolis, edifício
corporativo em Brasília e escola pública em Manaus. São maiores e menos
didáticos que os do manual, e servem de ponto de partida para projetos
reais.

> **Eles foram regravados nesta versão.** Estavam num esquema plano
> anterior, que o programa lia sem reconhecer: abriam como projeto
> padrão, com 100 m² e três moradores, e nada avisava. A abertura agora
> recusa formato desconhecido com mensagem própria, e os três foram
> convertidos para o esquema corrente, com a chuva incorporada.

---

### J.5. O que estes arquivos não são

Não são gabarito de projeto. São **casos de demonstração**: os custos são
os do tutorial, a tarifa é a da CASAN e a categoria é residencial em
todos, inclusive na escola e no hotel, pela limitação que a seção 5.2 (volume Enganos, limitações e confiabilidade)
descreve. Para um estudo real, troque tarifa, custos e série de chuva
pelos do seu caso.
