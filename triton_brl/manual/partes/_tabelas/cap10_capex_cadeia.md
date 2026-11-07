<!-- tabela: Rubricas do investimento que o programa calcula sozinho, a regra de cada uma, o parâmetro que a governa e o valor padrão -->
| Rubrica | Como o programa a calcula | Parâmetro | Valor padrão |
| :--- | :--- | :--- | :--- |
| cisterna | interpola linearmente a tabela de preços do polietileno pelo volume e multiplica pelo fator do material | `lower_tank_pead_prices`, `material_multipliers` | 9 preços, de 310 L a 15.000 L |
| caixa superior | a mesma interpolação, na tabela própria da caixa, com o volume da caixa | `upper_tank_pead_prices`, `upper_tank_vol` | 5 preços, de 310 L a 2.000 L; caixa de 500 L |
| motobombas | custo unitário vezes o número de motobombas; zero no abastecimento por gravidade | `pump_unit_cost`, `pump_count` do projeto | R$ 300,00 por unidade, 2 unidades |
| tubulação | soma, no arranjo 3D, dos metros de tubo de cada diâmetro vezes o preço por metro, mais curvas, conexões de extremidade e tês | `pipes_cost_per_meter` e as peças de linha do arranjo | 11 diâmetros, de DN 20 a DN 150 |
| acessórios | soma, no arranjo 3D, do preço de cada peça (registros, válvulas, quadro, sensores, air gap, hidrômetro) e dos cabos de comando | `CATALOGO_DE_PECAS`, que `pecas_do_arranjo` pode sobrescrever | 16 tipos de peça |
| mão de obra | percentual da soma de cisterna, caixa, motobombas, tubulação e acessórios, com um piso | `labor_percentage`, `MAO_DE_OBRA_MINIMA` | 30% dos materiais, no mínimo R$ 1 400,00 |
| linha de tratamento e descarte | dimensiona a linha pela classe de qualidade, pelo método de desinfecção e pela área do telhado; soma ao CAPEX só o que excede a verba genérica de filtragem dos acessórios digitados | `size_etap`, `capex_incremental_da_etap` | verba genérica de R$ 350,00 |
| tubulação e acessórios sem arranjo | estimativa por percentual do preço dos reservatórios, com piso, quando o arranjo não é a fonte | `piping_percentage_fallback`, `accessories_percentage` | tubulação: 18%, piso de R$ 950,00; acessórios: 8%, piso de R$ 500,00 |
| fator regional | multiplica o total do estimador preliminar; **não entra** no investimento do projeto, porque a interface e a linha de comando usam as parcelas, e não o total | `regional_factors_by_uf` | 27 UFs, de 0,93 a 1,21 |
