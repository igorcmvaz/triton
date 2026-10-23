<!-- tabela: Constantes que o código usa para orçar e que a base de custos não acompanha com fonte e data -->
| Constante | Valor | Onde está | Fonte registrada |
| :--- | ---: | :--- | :---: |
| consumo específico de recalque do orçamento calibrado | 0,45 kWh/m³ | `estimate_calibrated_capex_opex` | não |
| custo de cloração do orçamento calibrado | R$ 0,05/m³ | `estimate_calibrated_capex_opex` | não |
| mão de obra | 30% dos materiais | `labor_percentage` | não |
| acessórios sem arranjo | 8% dos reservatórios | `accessories_percentage` | não |
| tubulação sem arranjo | 18% da cisterna | `piping_percentage_fallback` | não |
| conexões sobre o tubo, no orçamento por comprimento | 25% | `compute_pipe_item_cost` | não |
| volume da caixa no orçamento calibrado | 10% da cisterna | `estimate_calibrated_capex_opex` | não |
| pisos da tubulação, dos acessórios e da mão de obra | R$ 950, R$ 500 e R$ 1 400 | `estimate_preliminary_capex` | não |
| preço da energia do reator ultravioleta | R$ 0,95/kWh | `water_quality.py` | não |
| preços da linha de tratamento e do descarte | tabela anterior | `water_quality.py` | não |
| multiplicadores de material | 1,35, 2,10, 3,60 | `material_multipliers` | não |
