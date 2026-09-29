# Estudo de Caso e Verificação Manual — Três Modelos de Referência (Netuno 5.0.7)

> Documento gerado por `python scripts/generate_reference_case_studies.py`. Não edite os números manualmente: altere premissas/código, execute o script e revise os resíduos.

## Escopo e cautelas

Este relatório confronta, por substituição numérica, os resultados do motor com contas independentes das mesmas equações. Isso é verificação interna e reprodutibilidade computacional; não é validação externa, certificação normativa, orçamento executivo nem ensaio de qualidade da água.

Decisões metodológicas essenciais:

- O descarte é o **limiar diário legado do Netuno 4**: abaixo de `df`, a chuva aplicável é zerada; ao atingir o limiar, `P` entra integralmente. Não se usa `P-df`.
- O balanço é YAS: limita estoque/extravasamento antes de retirar a demanda.
- A alternativa de 0 L é a referência sem sistema: CAPEX e impactos ambientais iguais a zero.
- CAPEX automático é triagem por interpolação da tabela interna; deve ser substituído por cotações locais.
- O O&M variável do formato Netuno 4 depende do **volume pluvial consumido no mês**, não da capacidade da cisterna. Os três casos usam itens fixos; não se adotou o coeficiente não comprovado de R$ 15/m³ de cisterna.
- A massa de cloro é consumo teórico em Cl2 equivalente. Demanda real de cloro exige ensaio e residual-alvo.
- A ACV é de triagem: fatores de material, rede, água e cloro são editáveis e exigem calibração local/EPD.

## Síntese dos ótimos recalculados

| Caso | Ótimo técnico (L) | Maior VPL (L) | Maior CO2 líquido (L) | TOPSIS (L) | Score |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 — Residência Unifamiliar Sustentável | 2.000 | 4.500 | 1.500 | 2.500 | 0,926528 |
| 2 — Edifício Corporativo EcoOffice | 5.000 | 25.000 | 2.500 | 10.000 | 0,848610 |
| 3 — Escola Pública de Tempo Integral Amazonas | 3.000 | 60.000 | 18.000 | 30.000 | 0,908461 |

## Caso 1 — Residência Unifamiliar Sustentável (Florianopolis1)

Projeto: [`estudo_caso_1_florianopolis1.netuno`](estudo_caso_1_florianopolis1.netuno). Série: `Florianopolis1.csv`, `31411` dias (`85,9986` anos de 365,25 dias), precipitação média anual `1.800,53 mm/ano`; SHA-256 `c2efedd93b596b29f1b72c4fd1e6c9a251248d89cf68698a625a8296b1f36842`.

### 1. Entradas e demanda

- Demanda total: `4 × 180,0 = 720,0 L/dia`.
- Demanda pluvial-alvo: `720,0 × 0,400 = 288,0 L/dia`.
- Demanda total anual equivalente: `720,0 × 365,25 / 1000 = 262,980 m³/ano`.
- Área `180,0 m²`, coeficiente `0,850`, limiar `2,00 mm`, modo `1`.

### 2. Um dia auditado e conservação de massa

No dia de índice `2`, `P=25,5204 mm` e `Pef=25,5204 mm`. Logo, `Vcap = 25,5204 × 180,0 × 0,850 = 3.904,6136 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 3.904,6136 = 2.212,0000 + 288,0000 + 1.404,6136`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `2.500 L`. Consumo anual: `243,378391 × 365,25 / 1000 = 88,893957 m³/ano`.
Potencial: `100 × 243,378391 / 720,0 = 33,802554%`.
Ganho marginal do ponto: `2,912386 %/m³`; limiar técnico: `5,000 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `2.400,00` + caixa `380,00` + bombas `300,14` + tubos `1.525,00` + acessórios `500,00` + mão de obra `1.531,54` = **R$ 6.636,69**.
Recalque anual: `7.645.114,645 / 85,9986 = 88.898,097 L/ano`; partidas: `17.439 / 85,9986 = 202,782 /ano`.
Energia: `0,3680 × [(88.898,097 / 2.280,0) + (202,782 × 0,0300)] / 0,5500 = 30,158512 kWh/ano`.
Cloro equivalente: `88,893957 × 2,000 / 1000 = 0,177788 kg Cl2-eq/ano`; custo `= 0,177788 × 25,00 = R$ 4,44/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 14,310000/m³` + esgoto `R$ 14,310000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `88,893957 × (14,310000 + 14,310000) = R$ 2.544,15`; fluxo líquido `= 2.544,15 − 740,00 − 28,65 − 4,44 = R$ 1.771,05`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 15.464,83**.
TIR: com `r=31,781416% a.a.`, `Σ FC_t/(1+r)^t = R$ 0,000000000`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `4` ano(s) e descontado `5` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6.636,69 | 0,00 | 0,00 | 0,00 | 0,00 | -6.636,69 | -6.636,69 | 0,000000000 |
| 1 | 0,00 | 2.544,15 | 28,65 | 740,00 | 4,44 | 1.771,05 | 1.771,05 | 0,000000000 |
| 2 | 0,00 | 2.671,35 | 30,08 | 769,60 | 4,62 | 1.867,05 | 1.867,05 | 0,000000000 |
| 3 | 0,00 | 2.804,92 | 31,59 | 800,38 | 4,81 | 1.968,14 | 1.968,14 | 0,000000000 |
| 4 | 0,00 | 2.945,17 | 33,17 | 832,40 | 5,00 | 2.074,60 | 2.074,60 | 0,000000000 |
| 5 | 0,00 | 3.092,42 | 34,82 | 865,70 | 5,20 | 2.186,70 | 2.186,70 | 0,000000000 |
| 6 | 0,00 | 3.247,05 | 36,57 | 900,32 | 5,41 | 2.304,75 | 2.304,75 | 0,000000000 |
| 7 | 0,00 | 3.409,40 | 38,39 | 936,34 | 5,62 | 2.429,04 | 2.429,04 | 0,000000000 |
| 8 | 0,00 | 3.579,87 | 40,31 | 973,79 | 5,85 | 2.559,91 | 2.559,91 | 0,000000000 |
| 9 | 0,00 | 3.758,86 | 42,33 | 1.012,74 | 6,08 | 2.697,71 | 2.697,71 | 0,000000000 |
| 10 | 0,00 | 3.946,80 | 44,45 | 1.053,25 | 6,33 | 2.842,78 | 2.842,78 | 0,000000000 |
| 11 | 0,00 | 4.144,14 | 46,67 | 1.095,38 | 6,58 | 2.995,52 | 2.995,52 | 0,000000000 |
| 12 | 0,00 | 4.351,35 | 49,00 | 1.139,20 | 6,84 | 3.156,31 | 3.156,31 | 0,000000000 |
| 13 | 0,00 | 4.568,92 | 51,45 | 1.184,76 | 7,12 | 3.325,59 | 3.325,59 | 0,000000000 |
| 14 | 0,00 | 4.797,36 | 54,02 | 1.232,15 | 7,40 | 3.503,78 | 3.503,78 | 0,000000000 |
| 15 | 0,00 | 5.037,23 | 56,73 | 1.281,44 | 7,70 | 3.691,37 | 3.691,37 | 0,000000000 |
| 16 | 0,00 | 5.289,09 | 59,56 | 1.332,70 | 8,00 | 3.888,83 | 3.888,83 | 0,000000000 |
| 17 | 0,00 | 5.553,55 | 62,54 | 1.386,01 | 8,32 | 4.096,68 | 4.096,68 | 0,000000000 |
| 18 | 0,00 | 5.831,23 | 65,67 | 1.441,45 | 8,66 | 4.315,46 | 4.315,46 | 0,000000000 |
| 19 | 0,00 | 6.122,79 | 68,95 | 1.499,10 | 9,00 | 4.545,73 | 4.545,73 | 0,000000000 |
| 20 | 0,00 | 6.428,93 | 72,40 | 1.559,07 | 9,36 | 4.788,10 | 4.788,10 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -6.636,69 | 0,000000000 | -6.636,69 | 0,000000000 |
| 1 | 0,909091 | 1.610,05 | 0,000000000 | -5.026,64 | 0,000000000 |
| 2 | 0,826446 | 1.543,01 | 0,000000000 | -3.483,63 | 0,000000000 |
| 3 | 0,751315 | 1.478,69 | 0,000000000 | -2.004,93 | 0,000000000 |
| 4 | 0,683013 | 1.416,98 | 0,000000000 | -587,95 | 0,000000000 |
| 5 | 0,620921 | 1.357,77 | 0,000000000 | 769,82 | 0,000000000 |
| 6 | 0,564474 | 1.300,97 | 0,000000000 | 2.070,79 | 0,000000000 |
| 7 | 0,513158 | 1.246,48 | 0,000000000 | 3.317,27 | 0,000000000 |
| 8 | 0,466507 | 1.194,22 | 0,000000000 | 4.511,49 | 0,000000000 |
| 9 | 0,424098 | 1.144,09 | 0,000000000 | 5.655,58 | 0,000000000 |
| 10 | 0,385543 | 1.096,01 | 0,000000000 | 6.751,60 | 0,000000000 |
| 11 | 0,350494 | 1.049,91 | 0,000000000 | 7.801,51 | 0,000000000 |
| 12 | 0,318631 | 1.005,70 | 0,000000000 | 8.807,21 | 0,000000000 |
| 13 | 0,289664 | 963,30 | 0,000000000 | 9.770,51 | 0,000000000 |
| 14 | 0,263331 | 922,66 | 0,000000000 | 10.693,17 | 0,000000000 |
| 15 | 0,239392 | 883,68 | 0,000000000 | 11.576,85 | 0,000000000 |
| 16 | 0,217629 | 846,32 | 0,000000000 | 12.423,17 | 0,000000000 |
| 17 | 0,197845 | 810,51 | 0,000000000 | 13.233,68 | 0,000000000 |
| 18 | 0,179859 | 776,17 | 0,000000000 | 14.009,85 | 0,000000000 |
| 19 | 0,163508 | 743,26 | 0,000000000 | 14.753,11 | 0,000000000 |
| 20 | 0,148644 | 711,72 | 0,000000000 | 15.464,83 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `337,100000 kg CO2e`; operação anual: bomba `2,563473` + cloro `4,444698`; crédito anual de água potável: `31,112885 kg CO2e`.
Saldo de vida: `(31,112885 − 2,563473 − 4,444698) × 20 − 337,100000 = **144,994275 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 720,000000000 | 720,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 288,000000000 | 288,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 3.904,613550000 | 3.904,613550000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 3.904,613550000 | 3.904,613550000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 88,893957374 | 88,893957374 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 174,086042626 | 174,086042626 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 180,627259521 | 180,627259521 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 33,802554329 | 33,802554329 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 2,912385913 | 2,912385913 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 2.400,000000000 | 2.400,000000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 380,000000000 | 380,000000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 300,142745474 | 300,142745474 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 1.525,000000000 | 1.525,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 500,000000000 | 500,000000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 1.531,542823642 | 1.531,542823642 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 6.636,685569116 | 6.636,685569116 | 0,000000000000 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 81,952476978 | 81,952476978 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 30,158511528 | 30,158511528 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 0,177787915 | 0,177787915 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 4,444697869 | 4,444697869 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 14,310000000 | 14,310000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 14,310000000 | 14,310000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 2.544,145060031 | 2.544,145060031 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 1.771,049776210 | 1.771,049776210 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 15.464,833776957 | 15.464,833776957 | 0,000000000000 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | 0,000000000 | 0,000000000 | 0,000000000011 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 4 | 4 | 0,000000000000 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 5 | 5 | 0,000000000000 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 55,000000000 | 55,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 11,000000000 | 11,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 121,100000000 | 121,100000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 18,000000000 | 18,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 337,100000000 | 337,100000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 2,563473480 | 2,563473480 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 4,444697869 | 4,444697869 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 31,112885081 | 31,112885081 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 24,104713732 | 24,104713732 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 13,984816569 | 13,984816569 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | 144,994274644 | 144,994274644 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,011659798446 | 0,011659798446 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,147036332161 | 0,147036332161 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,926527518969 | 0,926527518969 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,131054213907 | 0,131054213907 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,038734316431 | 0,038734316431 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,033510707024 | 0,033510707024 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,333333`, econômico `0,333333`, ambiental `0,333333`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | -8.316,41 | 0,00 | 0,000000 | 0,000000 | 0,202603 |
| 500 | 56,882 | 6.237,92 | 102,71 | 0,135543 | 0,142831 | 0,277698 |
| 1.000 | 70,947 | 10.652,14 | 146,19 | 0,169059 | 0,186150 | 0,309484 |
| 1.500 | 79,469 | 13.169,58 | 159,63 | 0,189365 | 0,210855 | 0,319313 |
| 2.000 | 85,064 | 14.673,80 | 157,13 | 0,202698 | 0,225617 | 0,317485 |
| 2.500 | 88,894 | 15.464,83 | 144,99 | 0,211824 | 0,233380 | 0,308612 |
| 3.000 | 91,677 | 15.897,56 | 127,15 | 0,218455 | 0,237627 | 0,295562 |
| 3.500 | 93,786 | 16.229,31 | 105,62 | 0,223480 | 0,240883 | 0,279823 |
| 4.000 | 95,383 | 16.386,05 | 81,31 | 0,227286 | 0,242421 | 0,262048 |
| 4.500 | 96,631 | 16.423,10 | 55,09 | 0,230259 | 0,242784 | 0,242878 |
| 5.000 | 97,605 | 16.365,98 | 27,37 | 0,232581 | 0,242224 | 0,222611 |
| 5.500 | 98,394 | 16.102,42 | -1,34 | 0,234461 | 0,239637 | 0,201620 |
| 6.000 | 99,031 | 15.787,00 | -30,88 | 0,235979 | 0,236542 | 0,180027 |
| 6.500 | 99,601 | 15.448,43 | -60,78 | 0,237336 | 0,233219 | 0,158163 |
| 7.000 | 100,099 | 15.085,65 | -91,07 | 0,238525 | 0,229659 | 0,136019 |
| 7.500 | 100,564 | 14.711,23 | -121,55 | 0,239632 | 0,225985 | 0,113738 |
| 8.000 | 100,968 | 14.372,22 | -152,35 | 0,240596 | 0,222658 | 0,091217 |
| 8.500 | 101,359 | 14.028,66 | -183,22 | 0,241527 | 0,219286 | 0,068642 |
| 9.000 | 101,712 | 13.672,02 | -214,31 | 0,242368 | 0,215786 | 0,045918 |
| 9.500 | 102,023 | 13.301,10 | -245,62 | 0,243109 | 0,212146 | 0,023024 |
| 10.000 | 102,301 | 12.918,80 | -277,11 | 0,243771 | 0,208394 | 0,000000 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,121101 | 0,067534 | 0,358015 | 21 |
| 500 | 0,051029 | 0,113475 | 0,689800 | 13 |
| 1.000 | 0,031422 | 0,132922 | 0,808805 | 8 |
| 1.500 | 0,021028 | 0,142314 | 0,871266 | 6 |
| 2.000 | 0,014851 | 0,146358 | 0,907877 | 3 |
| 2.500 | 0,011660 | 0,147036 | 0,926528 | 1 |
| 3.000 | 0,011698 | 0,145887 | 0,925768 | 2 |
| 3.500 | 0,014813 | 0,143863 | 0,906648 | 4 |
| 4.000 | 0,019864 | 0,141066 | 0,876568 | 5 |
| 4.500 | 0,025873 | 0,137822 | 0,841943 | 7 |
| 5.000 | 0,032450 | 0,134297 | 0,805396 | 9 |
| 5.500 | 0,039368 | 0,130405 | 0,768116 | 10 |
| 6.000 | 0,046548 | 0,126512 | 0,731031 | 11 |
| 6.500 | 0,053854 | 0,122807 | 0,695157 | 12 |
| 7.000 | 0,061279 | 0,119321 | 0,660691 | 14 |
| 7.500 | 0,068767 | 0,116156 | 0,628130 | 15 |
| 8.000 | 0,076335 | 0,113423 | 0,597726 | 16 |
| 8.500 | 0,083926 | 0,111122 | 0,569716 | 17 |
| 9.000 | 0,091576 | 0,109247 | 0,543996 | 18 |
| 9.500 | 0,099290 | 0,107826 | 0,520607 | 19 |
| 10.000 | 0,107053 | 0,106902 | 0,499647 | 20 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 100,0% | 36,6% |
| 500 | 44,4% | 41,2% | 13,0% |
| 1.000 | 30,6% | 23,3% | 3,1% |
| 1.500 | 22,3% | 13,2% | 0,0% |
| 2.000 | 16,8% | 7,1% | 0,6% |
| 2.500 | 13,1% | 3,9% | 3,4% |
| 3.000 | 10,4% | 2,1% | 7,4% |
| 3.500 | 8,3% | 0,8% | 12,4% |
| 4.000 | 6,8% | 0,1% | 17,9% |
| 4.500 | 5,5% | 0,0% | 23,9% |
| 5.000 | 4,6% | 0,2% | 30,3% |
| 5.500 | 3,8% | 1,3% | 36,9% |
| 6.000 | 3,2% | 2,6% | 43,6% |
| 6.500 | 2,6% | 3,9% | 50,5% |
| 7.000 | 2,2% | 5,4% | 57,4% |
| 7.500 | 1,7% | 6,9% | 64,4% |
| 8.000 | 1,3% | 8,3% | 71,4% |
| 8.500 | 0,9% | 9,7% | 78,5% |
| 9.000 | 0,6% | 11,1% | 85,6% |
| 9.500 | 0,3% | 12,6% | 92,8% |
| 10.000 | 0,0% | 14,2% | 100,0% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Caso 2 — Edifício Corporativo EcoOffice (Brasilia2)

Projeto: [`estudo_caso_2_brasilia2.netuno`](estudo_caso_2_brasilia2.netuno). Série: `Brasilia2.csv`, `12419` dias (`34,0014` anos de 365,25 dias), precipitação média anual `1.501,03 mm/ano`; SHA-256 `fb121ac5e308c6a009111ba20408d0a7e27363bddeca5404b29cae3cf864d54d`.

### 1. Entradas e demanda

- Demanda total: `80 × 50,0 = 4.000,0 L/dia`.
- Demanda pluvial-alvo: `4.000,0 × 0,650 = 2.600,0 L/dia`.
- Demanda total anual equivalente: `4.000,0 × 365,25 / 1000 = 1.461,000 m³/ano`.
- Área `650,0 m²`, coeficiente `0,900`, limiar `2,00 mm`, modo `2`.

### 2. Um dia auditado e conservação de massa

No dia de índice `1`, `P=16,3909 mm` e `Pef=16,3909 mm`. Logo, `Vcap = 16,3909 × 650,0 × 0,900 = 9.588,6496 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 9.588,6496 = 6.988,6496 + 2.600,0000 + 0,0000`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `10.000 L`. Consumo anual: `1.068,463880 × 365,25 / 1000 = 390,256432 m³/ano`.
Potencial: `100 × 1.068,463880 / 4.000,0 = 26,711597%`.
Ganho marginal do ponto: `0,620307 %/m³`; limiar técnico: `3,000 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `15.960,00` + caixa `2.835,00` + bombas `1.291,93` + tubos `4.975,00` + acessórios `1.653,60` + mão de obra `8.014,66` = **R$ 34.730,19**.
Recalque anual: `13.269.252,930 / 34,0014 = 390.256,432 L/ano`; partidas: `5.479 / 34,0014 = 161,141 /ano`.
Energia: `1,1000 × [(390.256,432 / 7.200,0) + (161,141 × 0,0400)] / 0,6500 = 102,634916 kWh/ano`.
Cloro equivalente: `390,256432 × 3,000 / 1000 = 1,170769 kg Cl2-eq/ano`; custo `= 1,170769 × 20,00 = R$ 23,42/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 28,900000/m³` + esgoto `R$ 28,900000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `390,256432 × (28,900000 + 28,900000) = R$ 22.556,82`; fluxo líquido `= 22.556,82 − 740,00 − 107,77 − 23,42 = R$ 21.685,64`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 190.125,02**.
TIR: com `r=67,452240% a.a.`, `Σ FC_t/(1+r)^t = R$ -0,000000000`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `2` ano(s) e descontado `2` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 34.730,19 | 0,00 | 0,00 | 0,00 | 0,00 | -34.730,19 | -34.730,19 | 0,000000000 |
| 1 | 0,00 | 22.556,82 | 107,77 | 740,00 | 23,42 | 21.685,64 | 21.685,64 | 0,000000000 |
| 2 | 0,00 | 23.684,66 | 113,15 | 773,30 | 24,47 | 22.773,74 | 22.773,74 | 0,000000000 |
| 3 | 0,00 | 24.868,90 | 118,81 | 808,10 | 25,57 | 23.916,41 | 23.916,41 | 0,000000000 |
| 4 | 0,00 | 26.112,34 | 124,75 | 844,46 | 26,72 | 25.116,40 | 25.116,40 | 0,000000000 |
| 5 | 0,00 | 27.417,96 | 130,99 | 882,46 | 27,92 | 26.376,58 | 26.376,58 | 0,000000000 |
| 6 | 0,00 | 28.788,86 | 137,54 | 922,17 | 29,18 | 27.699,96 | 27.699,96 | 0,000000000 |
| 7 | 0,00 | 30.228,30 | 144,42 | 963,67 | 30,49 | 29.089,72 | 29.089,72 | 0,000000000 |
| 8 | 0,00 | 31.739,71 | 151,64 | 1.007,04 | 31,87 | 30.549,17 | 30.549,17 | 0,000000000 |
| 9 | 0,00 | 33.326,70 | 159,22 | 1.052,35 | 33,30 | 32.081,83 | 32.081,83 | 0,000000000 |
| 10 | 0,00 | 34.993,03 | 167,18 | 1.099,71 | 34,80 | 33.691,34 | 33.691,34 | 0,000000000 |
| 11 | 0,00 | 36.742,69 | 175,54 | 1.149,20 | 36,36 | 35.381,58 | 35.381,58 | 0,000000000 |
| 12 | 0,00 | 38.579,82 | 184,32 | 1.200,91 | 38,00 | 37.156,59 | 37.156,59 | 0,000000000 |
| 13 | 0,00 | 40.508,81 | 193,53 | 1.254,95 | 39,71 | 39.020,62 | 39.020,62 | 0,000000000 |
| 14 | 0,00 | 42.534,25 | 203,21 | 1.311,43 | 41,50 | 40.978,12 | 40.978,12 | 0,000000000 |
| 15 | 0,00 | 44.660,96 | 213,37 | 1.370,44 | 43,36 | 43.033,79 | 43.033,79 | 0,000000000 |
| 16 | 0,00 | 46.894,01 | 224,04 | 1.432,11 | 45,32 | 45.192,55 | 45.192,55 | 0,000000000 |
| 17 | 0,00 | 49.238,71 | 235,24 | 1.496,55 | 47,35 | 47.459,56 | 47.459,56 | 0,000000000 |
| 18 | 0,00 | 51.700,65 | 247,00 | 1.563,90 | 49,49 | 49.840,26 | 49.840,26 | 0,000000000 |
| 19 | 0,00 | 54.285,68 | 259,35 | 1.634,27 | 51,71 | 52.340,34 | 52.340,34 | 0,000000000 |
| 20 | 0,00 | 56.999,97 | 272,32 | 1.707,82 | 54,04 | 54.965,79 | 54.965,79 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -34.730,19 | 0,000000000 | -34.730,19 | 0,000000000 |
| 1 | 0,892857 | 19.362,18 | 0,000000000 | -15.368,01 | 0,000000000 |
| 2 | 0,797194 | 18.155,09 | 0,000000000 | 2.787,07 | 0,000000000 |
| 3 | 0,711780 | 17.023,23 | 0,000000000 | 19.810,30 | 0,000000000 |
| 4 | 0,635518 | 15.961,93 | 0,000000000 | 35.772,23 | 0,000000000 |
| 5 | 0,567427 | 14.966,78 | 0,000000000 | 50.739,01 | 0,000000000 |
| 6 | 0,506631 | 14.033,66 | 0,000000000 | 64.772,68 | 0,000000000 |
| 7 | 0,452349 | 13.158,71 | 0,000000000 | 77.931,39 | 0,000000000 |
| 8 | 0,403883 | 12.338,30 | 0,000000000 | 90.269,68 | 0,000000000 |
| 9 | 0,360610 | 11.569,03 | 0,000000000 | 101.838,71 | 0,000000000 |
| 10 | 0,321973 | 10.847,71 | 0,000000000 | 112.686,42 | 0,000000000 |
| 11 | 0,287476 | 10.171,36 | 0,000000000 | 122.857,78 | 0,000000000 |
| 12 | 0,256675 | 9.537,17 | 0,000000000 | 132.394,95 | 0,000000000 |
| 13 | 0,229174 | 8.942,52 | 0,000000000 | 141.337,47 | 0,000000000 |
| 14 | 0,204620 | 8.384,94 | 0,000000000 | 149.722,41 | 0,000000000 |
| 15 | 0,182696 | 7.862,11 | 0,000000000 | 157.584,52 | 0,000000000 |
| 16 | 0,163122 | 7.371,88 | 0,000000000 | 164.956,40 | 0,000000000 |
| 17 | 0,145644 | 6.912,22 | 0,000000000 | 171.868,62 | 0,000000000 |
| 18 | 0,130040 | 6.481,21 | 0,000000000 | 178.349,83 | 0,000000000 |
| 19 | 0,116107 | 6.077,07 | 0,000000000 | 184.426,90 | 0,000000000 |
| 20 | 0,103667 | 5.698,13 | 0,000000000 | 190.125,02 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `2.425,700000 kg CO2e`; operação anual: bomba `8,723968` + cloro `29,269232`; crédito anual de água potável: `136,589751 kg CO2e`.
Saldo de vida: `(136,589751 − 8,723968 − 29,269232) × 20 − 2.425,700000 = **-453,768980 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 4.000,000000000 | 4.000,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 2.600,000000000 | 2.600,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 9.588,649590000 | 9.588,649590000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 9.588,649590000 | 9.588,649590000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 390,256432300 | 390,256432300 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 1.070,743567700 | 1.070,743567700 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 479,700065576 | 479,700065576 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 26,711597009 | 26,711597009 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 0,620307007 | 0,620307007 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 15.960,000000000 | 15.960,000000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 2.835,000000000 | 2.835,000000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 1.291,930802833 | 1.291,930802833 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 4.975,000000000 | 4.975,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 1.653,600000000 | 1.653,600000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 8.014,659240850 | 8.014,659240850 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 34.730,190043683 | 34.730,190043683 | 0,000000000000 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 93,304469384 | 93,304469384 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 102,634916323 | 102,634916323 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 1,170769297 | 1,170769297 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 23,415385938 | 23,415385938 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 28,900000000 | 28,900000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 28,900000000 | 28,900000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 22.556,821786935 | 22.556,821786935 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 21.685,639738858 | 21.685,639738858 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 190.125,021591344 | 190.125,021591344 | 0,000000000000 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | -0,000000000 | 0,000000000 | 0,000000000055 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 2 | 2 | 0,000000000000 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 2 | 2 | 0,000000000000 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 12.000,000000000 | 12.000,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 60,000000000 | 60,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 406,700000000 | 406,700000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 84,000000000 | 84,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 2.425,700000000 | 2.425,700000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 8,723967887 | 8,723967887 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 29,269232422 | 29,269232422 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 136,589751305 | 136,589751305 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 98,596550995 | 98,596550995 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 24,602280460 | 24,602280460 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | -453,768980099 | -453,768980099 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,024933436787 | 0,024933436787 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,139763184081 | 0,139763184081 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,848609906774 | 0,848609906774 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,245342684973 | 0,245342684973 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,082641477861 | 0,082641477861 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,106869778885 | 0,106869778885 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,333333`, econômico `0,333333`, ambiental `0,333333`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | -7.399,86 | 0,00 | 0,000000 | 0,000000 | 0,326466 |
| 2.500 | 285,103 | 142.867,04 | 273,49 | 0,140244 | 0,164340 | 0,340135 |
| 5.000 | 339,102 | 170.293,39 | 127,43 | 0,166806 | 0,194334 | 0,332835 |
| 7.500 | 367,600 | 181.652,51 | -148,41 | 0,180824 | 0,206757 | 0,319048 |
| 10.000 | 390,256 | 190.125,02 | -453,77 | 0,191969 | 0,216023 | 0,303785 |
| 12.500 | 408,690 | 196.378,87 | -780,50 | 0,201037 | 0,222863 | 0,287454 |
| 15.000 | 424,204 | 200.895,00 | -1.121,98 | 0,208668 | 0,227802 | 0,270386 |
| 17.500 | 437,739 | 204.233,64 | -1.473,44 | 0,215326 | 0,231453 | 0,252819 |
| 20.000 | 448,806 | 206.103,18 | -1.837,41 | 0,220770 | 0,233498 | 0,234627 |
| 22.500 | 458,155 | 207.245,41 | -2.210,10 | 0,225369 | 0,234747 | 0,215999 |
| 25.000 | 466,718 | 207.919,32 | -2.586,74 | 0,229581 | 0,235484 | 0,197174 |
| 27.500 | 474,113 | 207.898,08 | -2.969,33 | 0,233219 | 0,235461 | 0,178051 |
| 30.000 | 480,687 | 207.388,09 | -3.356,05 | 0,236453 | 0,234903 | 0,158722 |
| 32.500 | 486,614 | 206.493,26 | -3.746,05 | 0,239368 | 0,233924 | 0,139229 |
| 35.000 | 492,242 | 205.420,61 | -4.137,56 | 0,242137 | 0,232751 | 0,119660 |
| 37.500 | 497,215 | 203.957,56 | -4.532,39 | 0,244583 | 0,231151 | 0,099925 |
| 40.000 | 501,728 | 202.221,45 | -4.929,55 | 0,246803 | 0,229253 | 0,080075 |
| 42.500 | 505,970 | 200.323,68 | -5.328,07 | 0,248890 | 0,227177 | 0,060155 |
| 45.000 | 509,983 | 198.289,22 | -5.727,76 | 0,250864 | 0,224952 | 0,040178 |
| 47.500 | 513,675 | 196.064,11 | -6.129,08 | 0,252680 | 0,222519 | 0,020119 |
| 50.000 | 517,131 | 193.698,24 | -6.531,60 | 0,254380 | 0,219931 | 0,000000 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,115638 | 0,108822 | 0,484817 | 21 |
| 2.500 | 0,044831 | 0,134316 | 0,749752 | 9 |
| 5.000 | 0,032345 | 0,139988 | 0,812312 | 5 |
| 7.500 | 0,027244 | 0,140332 | 0,837422 | 3 |
| 10.000 | 0,024933 | 0,139763 | 0,848610 | 1 |
| 12.500 | 0,025342 | 0,138529 | 0,845354 | 2 |
| 15.000 | 0,027916 | 0,136847 | 0,830572 | 4 |
| 17.500 | 0,031912 | 0,134929 | 0,808728 | 6 |
| 20.000 | 0,036917 | 0,132628 | 0,782260 | 7 |
| 22.500 | 0,042494 | 0,130194 | 0,753924 | 8 |
| 25.000 | 0,048365 | 0,127818 | 0,725483 | 10 |
| 27.500 | 0,054487 | 0,125404 | 0,697113 | 11 |
| 30.000 | 0,060766 | 0,123055 | 0,669428 | 12 |
| 32.500 | 0,067158 | 0,120832 | 0,642758 | 13 |
| 35.000 | 0,073611 | 0,118847 | 0,617524 | 14 |
| 37.500 | 0,080150 | 0,117017 | 0,593493 | 15 |
| 40.000 | 0,086749 | 0,115413 | 0,570894 | 16 |
| 42.500 | 0,093386 | 0,114102 | 0,549923 | 17 |
| 45.000 | 0,100054 | 0,113113 | 0,530629 | 18 |
| 47.500 | 0,106761 | 0,112431 | 0,512933 | 19 |
| 50.000 | 0,113497 | 0,112091 | 0,496883 | 20 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 100,0% | 4,0% |
| 2.500 | 44,9% | 30,2% | 0,0% |
| 5.000 | 34,4% | 17,5% | 2,1% |
| 7.500 | 28,9% | 12,2% | 6,2% |
| 10.000 | 24,5% | 8,3% | 10,7% |
| 12.500 | 21,0% | 5,4% | 15,5% |
| 15.000 | 18,0% | 3,3% | 20,5% |
| 17.500 | 15,4% | 1,7% | 25,7% |
| 20.000 | 13,2% | 0,8% | 31,0% |
| 22.500 | 11,4% | 0,3% | 36,5% |
| 25.000 | 9,7% | 0,0% | 42,0% |
| 27.500 | 8,3% | 0,0% | 47,7% |
| 30.000 | 7,0% | 0,2% | 53,3% |
| 32.500 | 5,9% | 0,7% | 59,1% |
| 35.000 | 4,8% | 1,2% | 64,8% |
| 37.500 | 3,9% | 1,8% | 70,6% |
| 40.000 | 3,0% | 2,6% | 76,5% |
| 42.500 | 2,2% | 3,5% | 82,3% |
| 45.000 | 1,4% | 4,5% | 88,2% |
| 47.500 | 0,7% | 5,5% | 94,1% |
| 50.000 | 0,0% | 6,6% | 100,0% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Caso 3 — Escola Pública de Tempo Integral Amazonas (Manaus3)

Projeto: [`estudo_caso_3_manaus3.netuno`](estudo_caso_3_manaus3.netuno). Série: `Manaus3.csv`, `31410` dias (`85,9959` anos de 365,25 dias), precipitação média anual `1.802,57 mm/ano`; SHA-256 `6f91aa11c06482fc8708bccd953900d091f636abe23874d51bffc510d1a0d153`.

### 1. Entradas e demanda

- Demanda total: `350 × 40,0 = 14.000,0 L/dia`.
- Demanda pluvial-alvo: `14.000,0 × 0,500 = 7.000,0 L/dia`.
- Demanda total anual equivalente: `14.000,0 × 365,25 / 1000 = 5.113,500 m³/ano`.
- Área `1.400,0 m²`, coeficiente `0,800`, limiar `1,50 mm`, modo `3`.

### 2. Um dia auditado e conservação de massa

No dia de índice `1`, `P=9,8940 mm` e `Pef=9,8940 mm`. Logo, `Vcap = 9,8940 × 1.400,0 × 0,800 = 11.081,2733 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 11.081,2733 = 4.081,2733 + 7.000,0000 + 0,0000`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `30.000 L`. Consumo anual: `3.466,337512 × 365,25 / 1000 = 1.266,079776 m³/ano`.
Potencial: `100 × 3.466,337512 / 14.000,0 = 24,759554%`.
Ganho marginal do ponto: `0,175253 %/m³`; limiar técnico: `3,500 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `27.000,00` + caixa `5.400,00` + bombas `974,24` + tubos `6.500,00` + acessórios `2.742,00` + mão de obra `12.784,87` = **R$ 55.401,11**.
Recalque anual: `108.877.661,250 / 85,9959 = 1.266.079,776 L/ano`; partidas: `25.568 / 85,9959 = 297,317 /ano`.
Energia: `0,7350 × [(1.266.079,776 / 5.400,0) + (297,317 × 0,0300)] / 0,6000 = 298,138924 kWh/ano`.
Cloro equivalente: `1.266,079776 × 2,500 / 1000 = 3,165199 kg Cl2-eq/ano`; custo `= 3,165199 × 22,00 = R$ 69,63/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 25,300000/m³` + esgoto `R$ 20,240000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `1.266,079776 × (25,300000 + 20,240000) = R$ 57.657,27`; fluxo líquido `= 57.657,27 − 740,00 − 342,86 − 69,63 = R$ 56.504,78`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 629.352,39**.
TIR: com `r=106,999140% a.a.`, `Σ FC_t/(1+r)^t = R$ -0,000000000`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `1` ano(s) e descontado `2` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 55.401,11 | 0,00 | 0,00 | 0,00 | 0,00 | -55.401,11 | -55.401,11 | 0,000000000 |
| 1 | 0,00 | 57.657,27 | 342,86 | 740,00 | 69,63 | 56.504,78 | 56.504,78 | 0,000000000 |
| 2 | 0,00 | 60.540,14 | 360,00 | 773,30 | 72,77 | 59.334,07 | 59.334,07 | 0,000000000 |
| 3 | 0,00 | 63.567,14 | 378,00 | 808,10 | 76,04 | 62.305,00 | 62.305,00 | 0,000000000 |
| 4 | 0,00 | 66.745,50 | 396,90 | 844,46 | 79,46 | 65.424,67 | 65.424,67 | 0,000000000 |
| 5 | 0,00 | 70.082,78 | 416,75 | 882,46 | 83,04 | 68.700,52 | 68.700,52 | 0,000000000 |
| 6 | 0,00 | 73.586,91 | 437,59 | 922,17 | 86,78 | 72.140,38 | 72.140,38 | 0,000000000 |
| 7 | 0,00 | 77.266,26 | 459,46 | 963,67 | 90,68 | 75.752,44 | 75.752,44 | 0,000000000 |
| 8 | 0,00 | 81.129,57 | 482,44 | 1.007,04 | 94,76 | 79.545,33 | 79.545,33 | 0,000000000 |
| 9 | 0,00 | 85.186,05 | 506,56 | 1.052,35 | 99,03 | 83.528,11 | 83.528,11 | 0,000000000 |
| 10 | 0,00 | 89.445,35 | 531,89 | 1.099,71 | 103,48 | 87.710,27 | 87.710,27 | 0,000000000 |
| 11 | 0,00 | 93.917,62 | 558,48 | 1.149,20 | 108,14 | 92.101,80 | 92.101,80 | 0,000000000 |
| 12 | 0,00 | 98.613,50 | 586,41 | 1.200,91 | 113,01 | 96.713,18 | 96.713,18 | 0,000000000 |
| 13 | 0,00 | 103.544,18 | 615,73 | 1.254,95 | 118,09 | 101.555,41 | 101.555,41 | 0,000000000 |
| 14 | 0,00 | 108.721,39 | 646,51 | 1.311,43 | 123,41 | 106.640,04 | 106.640,04 | 0,000000000 |
| 15 | 0,00 | 114.157,46 | 678,84 | 1.370,44 | 128,96 | 111.979,22 | 111.979,22 | 0,000000000 |
| 16 | 0,00 | 119.865,33 | 712,78 | 1.432,11 | 134,76 | 117.585,68 | 117.585,68 | 0,000000000 |
| 17 | 0,00 | 125.858,60 | 748,42 | 1.496,55 | 140,83 | 123.472,80 | 123.472,80 | 0,000000000 |
| 18 | 0,00 | 132.151,53 | 785,84 | 1.563,90 | 147,16 | 129.654,62 | 129.654,62 | 0,000000000 |
| 19 | 0,00 | 138.759,10 | 825,13 | 1.634,27 | 153,79 | 136.145,91 | 136.145,91 | 0,000000000 |
| 20 | 0,00 | 145.697,06 | 866,39 | 1.707,82 | 160,71 | 142.962,14 | 142.962,14 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -55.401,11 | 0,000000000 | -55.401,11 | 0,000000000 |
| 1 | 0,909091 | 51.367,98 | 0,000000000 | -4.033,13 | 0,000000000 |
| 2 | 0,826446 | 49.036,42 | 0,000000000 | 45.003,29 | 0,000000000 |
| 3 | 0,751315 | 46.810,67 | 0,000000000 | 91.813,96 | 0,000000000 |
| 4 | 0,683013 | 44.685,93 | 0,000000000 | 136.499,89 | 0,000000000 |
| 5 | 0,620921 | 42.657,62 | 0,000000000 | 179.157,51 | 0,000000000 |
| 6 | 0,564474 | 40.721,36 | 0,000000000 | 219.878,87 | 0,000000000 |
| 7 | 0,513158 | 38.872,98 | 0,000000000 | 258.751,85 | 0,000000000 |
| 8 | 0,466507 | 37.108,49 | 0,000000000 | 295.860,33 | 0,000000000 |
| 9 | 0,424098 | 35.424,07 | 0,000000000 | 331.284,41 | 0,000000000 |
| 10 | 0,385543 | 33.816,11 | 0,000000000 | 365.100,51 | 0,000000000 |
| 11 | 0,350494 | 32.281,12 | 0,000000000 | 397.381,63 | 0,000000000 |
| 12 | 0,318631 | 30.815,80 | 0,000000000 | 428.197,43 | 0,000000000 |
| 13 | 0,289664 | 29.416,98 | 0,000000000 | 457.614,42 | 0,000000000 |
| 14 | 0,263331 | 28.081,66 | 0,000000000 | 485.696,07 | 0,000000000 |
| 15 | 0,239392 | 26.806,93 | 0,000000000 | 512.503,01 | 0,000000000 |
| 16 | 0,217629 | 25.590,07 | 0,000000000 | 538.093,08 | 0,000000000 |
| 17 | 0,197845 | 24.428,43 | 0,000000000 | 562.521,51 | 0,000000000 |
| 18 | 0,179859 | 23.319,52 | 0,000000000 | 585.841,04 | 0,000000000 |
| 19 | 0,163508 | 22.260,94 | 0,000000000 | 608.101,98 | 0,000000000 |
| 20 | 0,148644 | 21.250,41 | 0,000000000 | 629.352,39 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `3.571,900000 kg CO2e`; operação anual: bomba `25,341809` + cloro `79,129986`; crédito anual de água potável: `443,127922 kg CO2e`.
Saldo de vida: `(443,127922 − 25,341809 − 79,129986) × 20 − 3.571,900000 = **3.201,222542 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 14.000,000000000 | 14.000,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 7.000,000000000 | 7.000,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 11.081,273280000 | 11.081,273280000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 11.081,273280000 | 11.081,273280000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 1.266,079776241 | 1.266,079776241 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 3.847,420223759 | 3.847,420223759 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 740,398595132 | 740,398595132 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 24,759553657 | 24,759553657 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 0,175253317 | 0,175253317 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 27.000,000000000 | 27.000,000000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 5.400,000000000 | 5.400,000000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 974,238999619 | 974,238999619 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 6.500,000000000 | 6.500,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 2.742,000000000 | 2.742,000000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 12.784,871699886 | 12.784,871699886 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 55.401,110699505 | 55.401,110699505 | 0,000000000000 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 405,631189207 | 405,631189207 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 298,138924067 | 298,138924067 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 3,165199441 | 3,165199441 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 69,634387693 | 69,634387693 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 25,300000000 | 25,300000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 20,240000000 | 20,240000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 57.657,273010018 | 57.657,273010018 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 56.504,778859647 | 56.504,778859647 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 629.352,391946892 | 629.352,391946892 | 0,000000000000 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | -0,000000000 | 0,000000000 | 0,000000000017 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 1 | 1 | 0,000000000000 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 2 | 2 | 0,000000000000 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 600,000000000 | 600,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 100,000000000 | 100,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 536,900000000 | 536,900000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 60,000000000 | 60,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 3.571,900000000 | 3.571,900000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 25,341808546 | 25,341808546 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 79,129986015 | 79,129986015 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 443,127921684 | 443,127921684 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 338,656127124 | 338,656127124 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 10,547277058 | 10,547277058 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | 3.201,222542472 | 3.201,222542472 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,014068598236 | 0,014068598236 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,139620547385 | 0,139620547385 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,908460690706 | 0,908460690706 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,112858856667 | 0,112858856667 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,078166241950 | 0,078166241950 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,080708690995 | 0,080708690995 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,333333`, econômico `0,333333`, ambiental `0,333333`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | -8.631,28 | 0,00 | 0,000000 | 0,000000 | 0,000000 |
| 3.000 | 432,560 | 205.438,61 | 1.033,88 | 0,079375 | 0,078702 | 0,083256 |
| 6.000 | 738,217 | 369.108,80 | 2.412,59 | 0,135464 | 0,138874 | 0,194281 |
| 9.000 | 930,880 | 470.553,73 | 3.191,32 | 0,170818 | 0,176170 | 0,256990 |
| 12.000 | 1.011,035 | 510.741,84 | 3.365,75 | 0,185526 | 0,190945 | 0,271036 |
| 15.000 | 1.076,539 | 542.979,00 | 3.461,40 | 0,197546 | 0,202797 | 0,278739 |
| 18.000 | 1.128,043 | 567.549,05 | 3.482,27 | 0,206997 | 0,211830 | 0,280420 |
| 21.000 | 1.171,759 | 587.928,56 | 3.461,25 | 0,215019 | 0,219322 | 0,278728 |
| 24.000 | 1.207,919 | 604.321,80 | 3.399,91 | 0,221655 | 0,225349 | 0,273788 |
| 27.000 | 1.239,195 | 618.039,63 | 3.312,31 | 0,227394 | 0,230393 | 0,266733 |
| 30.000 | 1.266,080 | 629.352,39 | 3.201,22 | 0,232327 | 0,234552 | 0,257788 |
| 33.000 | 1.289,972 | 639.026,30 | 3.074,15 | 0,236712 | 0,238108 | 0,247555 |
| 36.000 | 1.311,209 | 647.245,85 | 2.932,83 | 0,240609 | 0,241130 | 0,236175 |
| 39.000 | 1.330,155 | 654.210,79 | 2.779,24 | 0,244085 | 0,243691 | 0,223806 |
| 42.000 | 1.347,433 | 660.262,33 | 2.616,77 | 0,247256 | 0,245916 | 0,210723 |
| 45.000 | 1.363,315 | 665.549,04 | 2.446,77 | 0,250170 | 0,247859 | 0,197033 |
| 48.000 | 1.377,867 | 670.106,96 | 2.269,65 | 0,252840 | 0,249535 | 0,182770 |
| 51.000 | 1.391,455 | 674.137,42 | 2.087,40 | 0,255334 | 0,251017 | 0,168094 |
| 54.000 | 1.404,171 | 677.690,42 | 1.900,47 | 0,257667 | 0,252323 | 0,153041 |
| 57.000 | 1.415,912 | 680.708,73 | 1.708,31 | 0,259822 | 0,253433 | 0,137567 |
| 60.000 | 1.427,146 | 683.449,77 | 1.513,45 | 0,261883 | 0,254440 | 0,121875 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,153463 | 0,000000 | 0,000000 | 21 |
| 3.000 | 0,107013 | 0,046459 | 0,302719 | 20 |
| 6.000 | 0,063907 | 0,091519 | 0,588826 | 19 |
| 9.000 | 0,040781 | 0,118443 | 0,743874 | 16 |
| 12.000 | 0,033250 | 0,126641 | 0,792045 | 13 |
| 15.000 | 0,027506 | 0,132433 | 0,828023 | 10 |
| 18.000 | 0,023162 | 0,135956 | 0,854437 | 8 |
| 21.000 | 0,019529 | 0,138253 | 0,876229 | 6 |
| 24.000 | 0,016695 | 0,139393 | 0,893039 | 4 |
| 27.000 | 0,014739 | 0,139816 | 0,904636 | 2 |
| 30.000 | 0,014069 | 0,139621 | 0,908461 | 1 |
| 33.000 | 0,014834 | 0,139049 | 0,903601 | 3 |
| 36.000 | 0,016956 | 0,138169 | 0,890697 | 5 |
| 39.000 | 0,020104 | 0,137053 | 0,872079 | 7 |
| 42.000 | 0,023908 | 0,135816 | 0,850317 | 9 |
| 45.000 | 0,028154 | 0,134512 | 0,826921 | 11 |
| 48.000 | 0,032730 | 0,133167 | 0,802708 | 12 |
| 51.000 | 0,037523 | 0,131850 | 0,778460 | 14 |
| 54.000 | 0,042489 | 0,130589 | 0,754510 | 15 |
| 57.000 | 0,047624 | 0,129383 | 0,730949 | 17 |
| 60.000 | 0,052848 | 0,128312 | 0,708279 | 18 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 100,0% | 100,0% |
| 3.000 | 69,7% | 69,1% | 70,3% |
| 6.000 | 48,3% | 45,4% | 30,7% |
| 9.000 | 34,8% | 30,8% | 8,4% |
| 12.000 | 29,2% | 25,0% | 3,3% |
| 15.000 | 24,6% | 20,3% | 0,6% |
| 18.000 | 21,0% | 16,7% | 0,0% |
| 21.000 | 17,9% | 13,8% | 0,6% |
| 24.000 | 15,4% | 11,4% | 2,4% |
| 27.000 | 13,2% | 9,5% | 4,9% |
| 30.000 | 11,3% | 7,8% | 8,1% |
| 33.000 | 9,6% | 6,4% | 11,7% |
| 36.000 | 8,1% | 5,2% | 15,8% |
| 39.000 | 6,8% | 4,2% | 20,2% |
| 42.000 | 5,6% | 3,4% | 24,9% |
| 45.000 | 4,5% | 2,6% | 29,7% |
| 48.000 | 3,5% | 1,9% | 34,8% |
| 51.000 | 2,5% | 1,3% | 40,1% |
| 54.000 | 1,6% | 0,8% | 45,4% |
| 57.000 | 0,8% | 0,4% | 50,9% |
| 60.000 | 0,0% | 0,0% | 56,5% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Referências e rastreabilidade

- [Atlas de fluxogramas metodológicos](../netuno/docs/fluxogramas_metodologicos.md): cadeia visual das equações e decisões implementadas.
- GHISI, E.; CORDOVA, M. M. *Netuno 4 — Manual do Usuário*. UFSC, 2014. Cópia local em [`additional_material/documentation/Manual-Netuno-4_Junho2014.pdf`](../additional_material/documentation/Manual-Netuno-4_Junho2014.pdf).
- ROCHA, V. L. *Validação do algoritmo do programa Netuno para avaliação do potencial de economia de água potável e dimensionamento de reservatórios de sistemas de aproveitamento de água pluvial em edificações*. Dissertação (Mestrado em Engenharia Civil) — UFSC, 2009. [Registro institucional](https://repositorio.ufsc.br/handle/123456789/92966).
- HWANG, C.-L.; YOON, K. *Multiple Attribute Decision Making*. Springer, 1981. [DOI](https://doi.org/10.1007/978-3-642-48318-9).
- [MCTI/SIRENE — fatores de emissão](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao). O fator deve ser escolhido para o período do estudo; o valor padrão do software é apenas uma hipótese editável de triagem.
