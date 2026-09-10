# Apêndice A — Os parâmetros do projeto

São **103 parâmetros**. Este apêndice é **gerado do fonte** por
`manual/gerar_apendices.py`, lendo a classe `NetunoConfig` e varrendo os
79 arquivos do pacote atrás de cada nome de campo. Não foi
transcrito à mão, e por isso não diverge do programa.

A coluna **onde se informa** lista as telas em que o campo aparece; a coluna
**quem consome** lista os módulos de cálculo que o leem. Campo sem nenhuma das
duas é campo gravado no arquivo e nunca lido, e está listado no capítulo 34.

## A.1. Identificação

3 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `project_name` | Novo projeto Netuno | — | Exportação, Janela principal, Relatórios | CAD e BIM, Linha de comando, Planilhas, Relatórios |
| `project_id` | — | — | Janela principal, Relatórios | Linha de comando |
| `created_at` | — | — | Janela principal | — |

## A.2. Chuva

9 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `precip_file` | — | — | Cenários, Janela principal, Projeto, Simulação | Cenários, Linha de comando, Planilhas |
| `climate_source_mode` | national_db | — | — | — |
| `climate_city_uf` | SC | — | Projeto, Relatórios | — |
| `climate_city_name` | Florianópolis | — | Projeto, Relatórios | — |
| `climate_model` | INM-CM4 | — | Projeto, Relatórios | — |
| `climate_scenario` | HIST | — | Projeto, Relatórios | — |
| `climate_start_date` | 01/01/1980 | — | Relatórios | — |
| `climate_end_date` | 31/12/2013 | — | Projeto, Relatórios | — |
| `start_date` | 01/01/1980 | — | Cenários, Janela principal, Projeto, Simulação, Tarifas e custos | Clima, Linha de comando |

Observações do fonte:

- `climate_source_mode`: "national_db" ou "custom_file"

## A.3. Captação

6 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `discard` | 1 | mm | Cenários, Documentação, Gráficos, Janela principal, Matriz, Projeto, Qualidade, Relatórios, Simulação | CAD e BIM, Cenários, Linha de comando, Planilhas, Relatórios |
| `discard_mode` | 1 | código | Janela principal, Projeto, Simulação, Varredura | Balanço diário, Cenários, Linha de comando |
| `discard_days_interval` | 7 | dias | Janela principal, Projeto, Simulação, Varredura | Balanço diário, Cenários, Linha de comando |
| `area` | 100 | m² | Ambiental, Cenários, Documentação, Edificação, Gráficos, Janela principal, Matriz, Qualidade, Relatórios, Simulação, Varredura | ACV, Balanço diário, CAD e BIM, Cenários, ETAP, Linha de comando, Planilhas, Relatórios |
| `irrigation_garden_area_m2` | 0 | m² | — | — |
| `runoff_coeff` | — | — | Cenários, Janela principal, Matriz, Qualidade, Relatórios, Simulação, Varredura | Balanço diário, Cenários, Linha de comando, Planilhas |

Observações do fonte:

- `discard`: mm
- `discard_mode`: 1 = todos os eventos, 2 = 1º evento após estiagem, 3 = a cada X dias
- `discard_days_interval`: intervalo para modo 3
- `area`: m2
- `irrigation_garden_area_m2`: Área de jardim em m² para o assistente de dimensionamento
- `runoff_coeff`: ver hydrology_defaults

## A.4. Edificação

2 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `num_economias` | 1 | un | Ambiental, Edificação | Econômico |
| `building_template_id` | res_medio | — | Edificação | Tarifas |

Observações do fonte:

- `num_economias`: Número de economias / apartamentos com micromedição individual

## A.5. Demanda

17 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `demand_type` | 0 | código | — | — |
| `demand_mode` | constant | — | Ambiental, Edificação, Relatórios, Varredura | Balanço diário |
| `demand_value` | 200 | L/dia | Documentação, Econ. integrado, Janela principal, Relatórios, Simulação | Balanço diário, Linha de comando |
| `demand_monthly` | — | — | Janela principal | Linha de comando |
| `residents_type` | 0 | código | — | — |
| `residents_count` | 4 | hab | Ambiental, Econ. integrado, Janela principal, Relatórios, Simulação | Balanço diário, Linha de comando |
| `residents_monthly` | — | — | Janela principal | Linha de comando |
| `potable_indoor_share` | 0,65 | fração | Edificação | — |
| `non_potable_indoor_share` | 0,35 | fração | Edificação | Balanço diário |
| `rainwater_share` | 0,4 | fração | Cenários, Documentação, Janela principal, Matriz, Relatórios, Simulação, Varredura | Balanço diário, Cenários, Linha de comando, Planilhas |
| `weekly_demands` | — | — | Edificação, Varredura | Balanço diário |
| `weekly_residents` | — | — | Edificação, Varredura | Balanço diário |
| `weekly_shares` | — | — | Edificação, Varredura | Balanço diário |
| `monthly_shares` | — | — | Edificação, Varredura | Balanço diário |
| `daily_demands` | — | — | Edificação, Varredura | Balanço diário |
| `daily_residents` | — | — | Edificação, Varredura | Balanço diário |
| `daily_shares` | — | — | Edificação, Varredura | Balanço diário |

Observações do fonte:

- `demand_mode`: "constant", "weekly", "monthly", "daily"
- `demand_value`: liters/day per capita or total
- `potable_indoor_share`: Fração potável do consumo interno (ex: 65% para banho/cozinha/beber)
- `non_potable_indoor_share`: Fração não-potável do consumo interno (ex: 35% para bacias/máquina)
- `rainwater_share`: fraction 0..1 (e.g. 0.4 = 40%)

## A.6. Irrigação

4 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `irrigation_liters_per_day` | 50 | L/dia | Ambiental, Edificação, Relatórios | Balanço diário |
| `irrigation_rain_threshold_mm` | 2 | mm/dia | Edificação | Balanço diário |
| `irrigation_potable_backup` | sim | — | Edificação | Balanço diário |
| `irrigation_rate_l_m2_day` | 3 | L/m²·dia | — | — |

Observações do fonte:

- `irrigation_liters_per_day`: Volume diário fixo de irrigação/usos externos (L/dia)
- `irrigation_rain_threshold_mm`: Limiar diário de precipitação para supressão da irrigação (mm/dia)
- `irrigation_potable_backup`: Se True, a rede pública atende a irrigação em dias secos se a cisterna secar
- `irrigation_rate_l_m2_day`: Taxa diária de rega (L/m²/dia)

## A.7. Qualidade da água

9 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `water_quality_target_class` | classe_1 | — | Ambiental, Qualidade | ACV, ETAP, Linha de comando |
| `water_quality_disinfection` | cloro | — | Ambiental, Qualidade | ACV, ETAP, Linha de comando |
| `water_quality_polishing` | não | — | Ambiental, Qualidade | ACV, ETAP, Linha de comando |
| `etap_enabled` | sim | — | Ambiental | ACV, ETAP, Linha de comando |
| `chlorine_treatment_enabled` | sim | — | Econ. integrado, Otimizador, Qualidade | Econômico |
| `chlorine_dose_mg_l` | — | mg Cl₂/L | Ambiental, Econ. integrado, Otimizador, Qualidade | ACV, ETAP, Econômico, Linha de comando, Relatórios |
| `chlorine_product_purity` | — | kg/kg | Ambiental, Qualidade | ACV, ETAP, Econômico, Linha de comando |
| `chlorine_cost_per_kg` | 25 | R$/kg | Econ. integrado, Otimizador, Qualidade | ETAP, Econômico, Preços |
| `chlorine_co2_kg_per_kg` | — | kg CO₂e/kg | Ambiental, Qualidade | ACV, ETAP, Linha de comando |

Observações do fonte:

- `water_quality_disinfection`: "cloro", "uv", "ozonio", "nenhum"
- `chlorine_dose_mg_l`: mg de Cl2 ativo por litro
- `chlorine_product_purity`: kg Cl2 ativo por kg de produto
- `chlorine_cost_per_kg`: R$ por kg de PRODUTO comercial

## A.8. Reservatórios

12 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `upper_tank_vol` | 500 | L | Ambiental, Assistente da bomba, Caixa superior, Cenários, Econ. integrado, Exportação, Janela principal, Matriz, Otimizador, Relatórios, Simulação, Tarifas e custos, Varredura | Balanço diário, CAD e BIM, Cenários, Linha de comando, Multicritério, Planilhas |
| `upper_tank_used` | 1 | código | Ambiental, Cenários, Econ. integrado, Janela principal, Matriz, Otimizador, Relatórios, Simulação, Tarifas e custos, Varredura | ACV, Balanço diário, Cenários, Econômico, Linha de comando, Motobomba, Planilhas |
| `lower_tank_max` | 10000 | L | Cenários, Janela principal, Relatórios, Simulação, Varredura | Balanço diário, Cenários, Linha de comando, Planilhas |
| `lower_tank_step` | 250 | L | Cenários, Janela principal, Relatórios, Simulação, Varredura | Balanço diário, Cenários, Linha de comando, Planilhas |
| `lower_tank_mode` | 1 | código | Janela principal, Relatórios, Simulação | Linha de comando |
| `lower_tank_fixed` | 2000 | L | Simulação, Tarifas e custos | Linha de comando |
| `delta_ideal` | 5 | %/m³ | Janela principal, Matriz, Otimizador, Simulação, Varredura | Cenários, Linha de comando |
| `econ_lower_tank_vol` | 2000 | L | Ambiental, Econ. integrado, Tarifas e custos, Varredura | Linha de comando |
| `lower_tank_material` | PEAD | — | Econ. integrado, Otimizador, Tarifas e custos | ACV |
| `upper_tank_material` | PEAD | — | Econ. integrado, Otimizador, Tarifas e custos | ACV |
| `cost_lower_tank` | 0 | R$ | Econ. integrado, Tarifas e custos, Varredura | Econômico, Linha de comando |
| `cost_upper_tank` | 0 | R$ | Econ. integrado, Tarifas e custos, Varredura | Econômico, Linha de comando |

Observações do fonte:

- `upper_tank_vol`: liters
- `upper_tank_used`: 0 = not used, 1 = used (default used in system)
- `lower_tank_max`: liters
- `lower_tank_step`: liters
- `lower_tank_mode`: 0 = fixed volume, 1 = sweep range
- `lower_tank_fixed`: if fixed mode
- `delta_ideal`: %/m3 threshold for optimal tank size
- `lower_tank_material`: "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"
- `upper_tank_material`: "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"

## A.9. Motobomba

10 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pumping_threshold` | 50 | L | Cenários, Janela principal, Matriz, Simulação, Varredura | Balanço diário, Cenários, Linha de comando, Planilhas |
| `pump_count` | 2 | un | Ambiental, Econ. integrado, Otimizador, Relatórios, Tarifas e custos | ACV, Econômico, Linha de comando, Preços, Relatórios |
| `pump_power_str` | 1/2 | — | Relatórios | — |
| `pump_power_kw` | 0,36775 | kW | Econ. integrado, Gráficos, Otimizador, Relatórios, Tarifas e custos, Varredura | CAD e BIM, Econômico, Linha de comando, Motobomba, Preços, Relatórios |
| `pump_manometric_head_m` | 0 | m.c.a. | Varredura | Econômico, Motobomba |
| `pump_efficiency` | 0 | % | Gráficos, Tarifas e custos, Varredura | Econômico, Linha de comando, Motobomba |
| `pump_flow_rate` | 0 | L/h | Econ. integrado, Gráficos, Otimizador, Relatórios, Tarifas e custos, Varredura | Econômico, Linha de comando, Motobomba |
| `pump_startup_time_h` | 0,03 | h | Econ. integrado, Gráficos, Otimizador, Tarifas e custos | Econômico, Linha de comando, Motobomba |
| `pump_motor_efficiency` | 0 | % | Tarifas e custos | Econômico, Motobomba |
| `pump_unit_cost` | 300 | R$ | Econ. integrado, Otimizador, Tarifas e custos, Varredura | Econômico, Linha de comando, Preços |

Observações do fonte:

- `pumping_threshold`: liters (recalque trigger level)
- `pump_count`: principal + reserva como configuração inicial recomendada
- `pump_power_kw`: kW (1 CV ~ 0.7355 kW -> 1/2 CV ~ 0.36775 kW)
- `pump_efficiency`: %, 0 = deduzir do porte
- `pump_startup_time_h`: hours
- `pump_motor_efficiency`: %
- `pump_unit_cost`: R$, referência de mercado para motobomba periférica 1/2 CV

## A.10. Tubulação

1 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `pipes_list` | — | — | Econ. integrado, Tarifas e custos | ACV |

## A.11. Investimento

3 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `cost_labor` | 0 | R$ | Econ. integrado, Tarifas e custos, Varredura | Econômico, Linha de comando |
| `cost_piping` | 0 | R$ | Econ. integrado, Tarifas e custos, Varredura | Econômico, Linha de comando |
| `cost_accessories` | 0 | R$ | Econ. integrado, Tarifas e custos, Varredura | ETAP, Econômico, Linha de comando |

## A.12. Operação

1 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `op_costs` | — | — | Econ. integrado, Otimizador, Tarifas e custos, Varredura | Econômico |

## A.13. Tarifas

14 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `tariff_customized` | não | — | Projeto | — |
| `water_tariffs` | — | — | Projeto, Tarifas, Tarifas e custos, Varredura | Econômico |
| `tariff_city_uf` | SC | — | Janela principal, Projeto, Relatórios, Tarifas, Tarifas e custos | — |
| `tariff_city_name` | Florianópolis | — | Janela principal, Projeto, Relatórios, Tarifas, Tarifas e custos | — |
| `sewage_rate` | 100 | % da água | Projeto, Tarifas, Tarifas e custos | Econômico, Linha de comando |
| `sewage_mode` | 1 | código | Econ. integrado, Otimizador, Projeto, Tarifas, Tarifas e custos | Econômico, Linha de comando |
| `water_tax_fixed` | 0 | R$/mês | Tarifas e custos | Econômico, Linha de comando |
| `water_tax_var` | 0 | % | Tarifas e custos | Econômico, Linha de comando |
| `tariff_escalation` | 12 | meses | Econ. integrado, Otimizador, Tarifas e custos, Varredura | Econômico, Linha de comando |
| `water_tariff_escalation` | 5 | %/ano | Econ. integrado, Otimizador, Varredura | Econômico, Linha de comando |
| `sewage_tariff_escalation` | 5 | %/ano | Econ. integrado, Otimizador | Econômico, Linha de comando |
| `elec_tariff_escalation` | 5 | %/ano | Econ. integrado, Otimizador, Varredura | Econômico, Linha de comando |
| `tariff_flag` | verde | — | Econ. integrado | Econômico |
| `elec_tariff` | 0,6957 | R$/kWh | Econ. integrado, Gráficos, Otimizador, Projeto, Tarifas e custos, Varredura | Econômico, Linha de comando |

Observações do fonte:

- `sewage_mode`: 0 = fixed R$, 1 = % of water bill
- `water_tax_fixed`: R$
- `water_tax_var`: %
- `tariff_escalation`: months period
- `water_tariff_escalation`: % escalation per period (annual)
- `sewage_tariff_escalation`: % escalation per period (annual)
- `elec_tariff_escalation`: % escalation per period (annual)
- `tariff_flag`: "verde", "amarela", "vermelha_1", "vermelha_2", "branca"
- `elec_tariff`: R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)

## A.14. Energia

4 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `elec_city_uf` | SC | — | Janela principal, Projeto, Tarifas e custos | — |
| `elec_city_name` | Florianópolis | — | Janela principal, Projeto, Tarifas e custos | — |
| `elec_tax_fixed` | 0 | R$/mês | Tarifas e custos | Econômico, Linha de comando |
| `elec_tax_var` | 0 | % | Tarifas e custos | Econômico, Linha de comando |

Observações do fonte:

- `elec_tax_fixed`: R$
- `elec_tax_var`: %

## A.15. Incentivos

3 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `iptu_green_enabled` | não | — | Econ. integrado, Otimizador | Econômico |
| `iptu_annual_value` | 4000 | R$/ano | Econ. integrado, Otimizador | Econômico |
| `iptu_discount_pct` | 5 | % | Econ. integrado, Otimizador | Econômico |

Observações do fonte:

- `iptu_annual_value`: Valor venal do IPTU anual da edificação (R$/ano)
- `iptu_discount_pct`: Desconto municipal do IPTU Verde (%)

## A.16. Financeiro

4 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `inflation` | 0,2 | %/mês | Documentação, Econ. integrado, Otimizador, Tarifas e custos, Varredura | Econômico, Linha de comando |
| `analysis_period_years` | 20 | anos | Econ. integrado, Econômico, Otimizador, Relatórios, Tarifas e custos, Varredura | ACV, Econômico, Linha de comando, Relatórios |
| `tma` | 2 | %/mês | Econ. integrado, Otimizador, Tarifas e custos, Varredura | Econômico, Linha de comando, Planilhas |
| `install_month` | 0 | mês | — | — |

Observações do fonte:

- `inflation`: % monthly
- `analysis_period_years`: years
- `tma`: % monthly discount rate

## A.17. Certificações

1 parâmetros.

| Parâmetro | Padrão | Unidade | Onde se informa | Quem consome |
| :--- | ---: | :--- | :--- | :--- |
| `edge_base_case_l_person_day` | 0 | L/pessoa·dia | Ambiental | — |

