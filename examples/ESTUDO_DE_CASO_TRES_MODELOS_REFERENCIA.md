# Estudo de Caso e Verificação Manual — Três Modelos de Referência (Netuno 5.0.0)

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
| 1 — Residência Unifamiliar Sustentável | 2.000 | 5.500 | 1.500 | 4.000 | 0,892458 |
| 2 — Edifício Corporativo EcoOffice | 5.000 | 27.500 | 2.500 | 20.000 | 0,819936 |
| 3 — Escola Pública de Tempo Integral Amazonas | 3.000 | 60.000 | 18.000 | 30.000 | 0,892497 |

## Caso 1 — Residência Unifamiliar Sustentável (Florianopolis1)

Projeto: [`estudo_caso_1_florianopolis1.netuno`](estudo_caso_1_florianopolis1.netuno). Série: `Florianopolis1.csv`, `31411` dias (`85,9986` anos de 365,25 dias), precipitação média anual `1.800,53 mm/ano`; SHA-256 `c2efedd93b596b29f1b72c4fd1e6c9a251248d89cf68698a625a8296b1f36842`.

### 1. Entradas e demanda

- Demanda total: `4 × 180,0 = 720,0 L/dia`.
- Demanda pluvial-alvo: `720,0 × 0,400 = 288,0 L/dia`.
- Demanda total anual equivalente: `720,0 × 365,25 / 1000 = 262,980 m³/ano`.
- Área `180,0 m²`, coeficiente `0,850`, limiar `2,00 mm`, modo `1`.

### 2. Um dia auditado e conservação de massa

No dia de índice `2`, `P=25,5204 mm` e `Pef=23,5204 mm`. Logo, `Vcap = 23,5204 × 180,0 × 0,850 = 3.598,6136 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 3.598,6136 = 3.310,6136 + 288,0000 + 0,0000`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `4.000 L`. Consumo anual: `248,038415 × 365,25 / 1000 = 90,596031 m³/ano`.
Potencial: `100 × 248,038415 / 720,0 = 34,449780%`.
Ganho marginal do ponto: `1,475859 %/m³`; limiar técnico: `5,000 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `2.424,50` + caixa `289,90` + bombas `300,14` + tubos `1.525,00` + acessórios `500,00` + mão de obra `1.511,86` = **R$ 6.551,41**.
Recalque anual: `7.791.580,663 / 85,9986 = 90.601,217 L/ano`; partidas: `17.790 / 85,9986 = 206,864 /ano`.
Energia: `0,3680 × [(90.601,217 / 2.280,0) + (206,864 × 0,0300)] / 0,5500 = 30,740237 kWh/ano`.
Cloro equivalente: `90,596031 × 2,000 / 1000 = 0,181192 kg Cl2-eq/ano`; custo `= 0,181192 × 25,00 = R$ 4,53/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 14,310000/m³` + esgoto `R$ 14,310000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `90,596031 × (14,310000 + 14,310000) = R$ 2.592,86`; fluxo líquido `= 2.592,86 − 740,00 − 29,20 − 4,53 = R$ 1.819,13`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 16.132,48**.
TIR: com `r=32,889860% a.a.`, `Σ FC_t/(1+r)^t = R$ 0,000000003`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `4` ano(s) e descontado `5` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6.551,41 | 0,00 | 0,00 | 0,00 | 0,00 | -6.551,41 | -6.551,41 | 0,000000000 |
| 1 | 0,00 | 2.592,86 | 29,20 | 740,00 | 4,53 | 1.819,13 | 1.819,13 | 0,000000000 |
| 2 | 0,00 | 2.722,50 | 30,66 | 769,60 | 4,71 | 1.917,53 | 1.917,53 | 0,000000000 |
| 3 | 0,00 | 2.858,63 | 32,20 | 800,38 | 4,90 | 2.021,15 | 2.021,15 | 0,000000000 |
| 4 | 0,00 | 3.001,56 | 33,81 | 832,40 | 5,10 | 2.130,26 | 2.130,26 | 0,000000000 |
| 5 | 0,00 | 3.151,64 | 35,50 | 865,70 | 5,30 | 2.245,14 | 2.245,14 | 0,000000000 |
| 6 | 0,00 | 3.309,22 | 37,27 | 900,32 | 5,51 | 2.366,11 | 2.366,11 | 0,000000000 |
| 7 | 0,00 | 3.474,68 | 39,14 | 936,34 | 5,73 | 2.493,48 | 2.493,48 | 0,000000000 |
| 8 | 0,00 | 3.648,41 | 41,09 | 973,79 | 5,96 | 2.627,57 | 2.627,57 | 0,000000000 |
| 9 | 0,00 | 3.830,83 | 43,15 | 1.012,74 | 6,20 | 2.768,75 | 2.768,75 | 0,000000000 |
| 10 | 0,00 | 4.022,37 | 45,30 | 1.053,25 | 6,45 | 2.917,37 | 2.917,37 | 0,000000000 |
| 11 | 0,00 | 4.223,49 | 47,57 | 1.095,38 | 6,71 | 3.073,84 | 3.073,84 | 0,000000000 |
| 12 | 0,00 | 4.434,67 | 49,95 | 1.139,20 | 6,97 | 3.238,55 | 3.238,55 | 0,000000000 |
| 13 | 0,00 | 4.656,40 | 52,44 | 1.184,76 | 7,25 | 3.411,94 | 3.411,94 | 0,000000000 |
| 14 | 0,00 | 4.889,22 | 55,07 | 1.232,15 | 7,54 | 3.594,46 | 3.594,46 | 0,000000000 |
| 15 | 0,00 | 5.133,68 | 57,82 | 1.281,44 | 7,84 | 3.786,58 | 3.786,58 | 0,000000000 |
| 16 | 0,00 | 5.390,37 | 60,71 | 1.332,70 | 8,16 | 3.988,80 | 3.988,80 | 0,000000000 |
| 17 | 0,00 | 5.659,88 | 63,75 | 1.386,01 | 8,48 | 4.201,65 | 4.201,65 | 0,000000000 |
| 18 | 0,00 | 5.942,88 | 66,93 | 1.441,45 | 8,82 | 4.425,67 | 4.425,67 | 0,000000000 |
| 19 | 0,00 | 6.240,02 | 70,28 | 1.499,10 | 9,18 | 4.661,46 | 4.661,46 | 0,000000000 |
| 20 | 0,00 | 6.552,02 | 73,80 | 1.559,07 | 9,54 | 4.909,62 | 4.909,62 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -6.551,41 | 0,000000000 | -6.551,41 | 0,000000000 |
| 1 | 0,909091 | 1.653,75 | 0,000000000 | -4.897,66 | 0,000000000 |
| 2 | 0,826446 | 1.584,73 | 0,000000000 | -3.312,92 | 0,000000000 |
| 3 | 0,751315 | 1.518,52 | 0,000000000 | -1.794,40 | 0,000000000 |
| 4 | 0,683013 | 1.454,99 | 0,000000000 | -339,41 | 0,000000000 |
| 5 | 0,620921 | 1.394,06 | 0,000000000 | 1.054,65 | 0,000000000 |
| 6 | 0,564474 | 1.335,61 | 0,000000000 | 2.390,26 | 0,000000000 |
| 7 | 0,513158 | 1.279,55 | 0,000000000 | 3.669,80 | 0,000000000 |
| 8 | 0,466507 | 1.225,78 | 0,000000000 | 4.895,58 | 0,000000000 |
| 9 | 0,424098 | 1.174,22 | 0,000000000 | 6.069,80 | 0,000000000 |
| 10 | 0,385543 | 1.124,77 | 0,000000000 | 7.194,58 | 0,000000000 |
| 11 | 0,350494 | 1.077,36 | 0,000000000 | 8.271,94 | 0,000000000 |
| 12 | 0,318631 | 1.031,90 | 0,000000000 | 9.303,84 | 0,000000000 |
| 13 | 0,289664 | 988,32 | 0,000000000 | 10.292,16 | 0,000000000 |
| 14 | 0,263331 | 946,53 | 0,000000000 | 11.238,69 | 0,000000000 |
| 15 | 0,239392 | 906,48 | 0,000000000 | 12.145,17 | 0,000000000 |
| 16 | 0,217629 | 868,08 | 0,000000000 | 13.013,24 | 0,000000000 |
| 17 | 0,197845 | 831,27 | 0,000000000 | 13.844,52 | 0,000000000 |
| 18 | 0,179859 | 796,00 | 0,000000000 | 14.640,51 | 0,000000000 |
| 19 | 0,163508 | 762,19 | 0,000000000 | 15.402,70 | 0,000000000 |
| 20 | 0,148644 | 729,78 | 0,000000000 | 16.132,48 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `436,100000 kg CO2e`; operação anual: bomba `2,612920` + cloro `4,529802`; crédito anual de água potável: `31,708611 kg CO2e`.
Saldo de vida: `(31,708611 − 2,612920 − 4,529802) × 20 − 436,100000 = **55,217785 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 720,000000000 | 720,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 288,000000000 | 288,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 3.598,613550000 | 3.598,613550000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 3.598,613550000 | 3.598,613550000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 90,596031194 | 90,596031194 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 172,383968806 | 172,383968806 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 136,754651651 | 136,754651651 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 34,449779905 | 34,449779905 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 1,475858711 | 1,475858711 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 2.424,500000000 | 2.424,500000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 289,900000000 | 289,900000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 300,142745474 | 300,142745474 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 1.525,000000000 | 1.525,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 500,000000000 | 500,000000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 1.511,862823642 | 1.511,862823642 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 6.551,405569116 | 6.551,405569116 | 0,000000000001 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 83,533252284 | 83,533252284 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 30,740236841 | 30,740236841 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 0,181192062 | 0,181192062 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 4,529801560 | 4,529801560 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 14,310000000 | 14,310000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 14,310000000 | 14,310000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 2.592,858412768 | 2.592,858412768 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 1.819,125386210 | 1.819,125386210 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 16.132,483960826 | 16.132,483960826 | 0,000000000002 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | 0,000000003 | 0,000000000 | 0,000000002590 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 4 | 3.37254048684715 | 0,627459513153 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 5 | 4.039171943218903 | 0,960828056781 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 88,000000000 | 88,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 11,000000000 | 11,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 121,100000000 | 121,100000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 18,000000000 | 18,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 436,100000000 | 436,100000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 2,612920131 | 2,612920131 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 4,529801560 | 4,529801560 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 31,708610918 | 31,708610918 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 24,565889227 | 24,565889227 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 17,752257855 | 17,752257855 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | 55,217784534 | 55,217784534 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,017192357655 | 0,017192357655 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,142674377050 | 0,142674377050 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,892458192212 | 0,892458192212 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,090907898652 | 0,090907898652 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,000000000000 | 0,000000000000 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,022523791689 | 0,022523791689 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,166667`, econômico `0,000000`, ambiental `0,111111`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | 0,00 | 0,00 | 0,000000 | 0,000000 | 0,000000 |
| 500 | 49,435 | 4.287,14 | 61,91 | 0,123429 | 0,000000 | 0,064284 |
| 1.000 | 63,458 | 8.927,41 | 105,26 | 0,158440 | 0,000000 | 0,133863 |
| 1.500 | 72,422 | 11.363,99 | 121,16 | 0,180822 | 0,000000 | 0,170398 |
| 2.000 | 78,455 | 13.213,24 | 121,07 | 0,195885 | 0,000000 | 0,198127 |
| 2.500 | 82,851 | 14.392,76 | 112,03 | 0,206860 | 0,000000 | 0,215814 |
| 3.000 | 86,111 | 15.183,31 | 96,79 | 0,215000 | 0,000000 | 0,227668 |
| 3.500 | 88,655 | 15.776,56 | 77,65 | 0,221354 | 0,000000 | 0,236563 |
| 4.000 | 90,596 | 16.132,48 | 55,22 | 0,226199 | 0,000000 | 0,241900 |
| 4.500 | 92,150 | 16.355,80 | 30,66 | 0,230078 | 0,000000 | 0,245249 |
| 5.000 | 93,403 | 16.476,37 | 4,48 | 0,233207 | 0,000000 | 0,247056 |
| 5.500 | 94,472 | 16.504,22 | -22,70 | 0,235877 | 0,000000 | 0,247474 |
| 6.000 | 95,397 | 16.482,61 | -50,66 | 0,238187 | 0,000000 | 0,247150 |
| 6.500 | 96,179 | 16.411,86 | -79,40 | 0,240138 | 0,000000 | 0,246089 |
| 7.000 | 96,826 | 16.295,15 | -108,88 | 0,241754 | 0,000000 | 0,244339 |
| 7.500 | 97,416 | 16.146,89 | -138,68 | 0,243227 | 0,000000 | 0,242116 |
| 8.000 | 97,945 | 15.991,11 | -168,80 | 0,244547 | 0,000000 | 0,239780 |
| 8.500 | 98,416 | 15.815,93 | -199,24 | 0,245725 | 0,000000 | 0,237153 |
| 9.000 | 98,859 | 15.630,85 | -229,83 | 0,246831 | 0,000000 | 0,234378 |
| 9.500 | 99,269 | 15.434,23 | -260,60 | 0,247852 | 0,000000 | 0,231430 |
| 10.000 | 99,656 | 15.229,99 | -291,50 | 0,248819 | 0,000000 | 0,228367 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,142840 | 0,051673 | 0,265654 | 21 |
| 500 | 0,073464 | 0,093258 | 0,559362 | 20 |
| 1.000 | 0,051948 | 0,113786 | 0,686558 | 17 |
| 1.500 | 0,038809 | 0,125865 | 0,764327 | 12 |
| 2.000 | 0,029973 | 0,133132 | 0,816234 | 9 |
| 2.500 | 0,023676 | 0,137669 | 0,853257 | 6 |
| 3.000 | 0,019441 | 0,140365 | 0,878349 | 4 |
| 3.500 | 0,017167 | 0,141975 | 0,892126 | 2 |
| 4.000 | 0,017192 | 0,142674 | 0,892458 | 1 |
| 4.500 | 0,019137 | 0,142858 | 0,881865 | 3 |
| 5.000 | 0,022435 | 0,142689 | 0,864133 | 5 |
| 5.500 | 0,026499 | 0,142368 | 0,843080 | 7 |
| 6.000 | 0,031028 | 0,141979 | 0,820656 | 8 |
| 6.500 | 0,035880 | 0,141533 | 0,797759 | 10 |
| 7.000 | 0,040969 | 0,141056 | 0,774925 | 11 |
| 7.500 | 0,046169 | 0,140680 | 0,752909 | 13 |
| 8.000 | 0,051462 | 0,140412 | 0,731792 | 14 |
| 8.500 | 0,056833 | 0,140262 | 0,711648 | 15 |
| 9.000 | 0,062245 | 0,140279 | 0,692655 | 16 |
| 9.500 | 0,067699 | 0,140458 | 0,674769 | 18 |
| 10.000 | 0,073181 | 0,140818 | 0,658030 | 19 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 0,0% | 100,0% |
| 500 | 50,4% | 0,0% | 74,0% |
| 1.000 | 36,3% | 0,0% | 45,9% |
| 1.500 | 27,3% | 0,0% | 31,1% |
| 2.000 | 21,3% | 0,0% | 19,9% |
| 2.500 | 16,9% | 0,0% | 12,8% |
| 3.000 | 13,6% | 0,0% | 8,0% |
| 3.500 | 11,0% | 0,0% | 4,4% |
| 4.000 | 9,1% | 0,0% | 2,3% |
| 4.500 | 7,5% | 0,0% | 0,9% |
| 5.000 | 6,3% | 0,0% | 0,2% |
| 5.500 | 5,2% | 0,0% | 0,0% |
| 6.000 | 4,3% | 0,0% | 0,1% |
| 6.500 | 3,5% | 0,0% | 0,6% |
| 7.000 | 2,8% | 0,0% | 1,3% |
| 7.500 | 2,2% | 0,0% | 2,2% |
| 8.000 | 1,7% | 0,0% | 3,1% |
| 8.500 | 1,2% | 0,0% | 4,2% |
| 9.000 | 0,8% | 0,0% | 5,3% |
| 9.500 | 0,4% | 0,0% | 6,5% |
| 10.000 | 0,0% | 0,0% | 7,7% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Caso 2 — Edifício Corporativo EcoOffice (Brasilia2)

Projeto: [`estudo_caso_2_brasilia2.netuno`](estudo_caso_2_brasilia2.netuno). Série: `Brasilia2.csv`, `12419` dias (`34,0014` anos de 365,25 dias), precipitação média anual `1.501,03 mm/ano`; SHA-256 `fb121ac5e308c6a009111ba20408d0a7e27363bddeca5404b29cae3cf864d54d`.

### 1. Entradas e demanda

- Demanda total: `80 × 50,0 = 4.000,0 L/dia`.
- Demanda pluvial-alvo: `4.000,0 × 0,650 = 2.600,0 L/dia`.
- Demanda total anual equivalente: `4.000,0 × 365,25 / 1000 = 1.461,000 m³/ano`.
- Área `650,0 m²`, coeficiente `0,900`, limiar `2,00 mm`, modo `2`.

### 2. Um dia auditado e conservação de massa

No dia de índice `1`, `P=16,3909 mm` e `Pef=14,3909 mm`. Logo, `Vcap = 14,3909 × 650,0 × 0,900 = 8.418,6496 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 8.418,6496 = 5.818,6496 + 2.600,0000 + 0,0000`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `20.000 L`. Consumo anual: `1.191,438643 × 365,25 / 1000 = 435,172964 m³/ano`.
Potencial: `100 × 1.191,438643 / 4.000,0 = 29,785966%`.
Ganho marginal do ponto: `0,313630 %/m³`; limiar técnico: `3,000 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `24.150,00` + caixa `2.632,50` + bombas `1.291,93` + tubos `4.975,00` + acessórios `2.292,60` + mão de obra `10.602,61` = **R$ 45.944,64**.
Recalque anual: `14.796.876,506 / 34,0014 = 435.184,729 L/ano`; partidas: `6.091 / 34,0014 = 179,140 /ano`.
Energia: `1,1000 × [(435.184,729 / 7.200,0) + (179,140 × 0,0400)] / 0,6500 = 114,413398 kWh/ano`.
Cloro equivalente: `435,172964 × 3,000 / 1000 = 1,305519 kg Cl2-eq/ano`; custo `= 1,305519 × 20,00 = R$ 26,11/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 28,900000/m³` + esgoto `R$ 28,900000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `435,172964 × (28,900000 + 28,900000) = R$ 25.153,00`; fluxo líquido `= 25.153,00 − 740,00 − 120,13 − 26,11 = R$ 24.266,75`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 205.642,32**.
TIR: com `r=57,817708% a.a.`, `Σ FC_t/(1+r)^t = R$ 0,000000020`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `2` ano(s) e descontado `3` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 45.944,64 | 0,00 | 0,00 | 0,00 | 0,00 | -45.944,64 | -45.944,64 | 0,000000000 |
| 1 | 0,00 | 25.153,00 | 120,13 | 740,00 | 26,11 | 24.266,75 | 24.266,75 | 0,000000000 |
| 2 | 0,00 | 26.410,65 | 126,14 | 773,30 | 27,29 | 25.483,92 | 25.483,92 | 0,000000000 |
| 3 | 0,00 | 27.731,18 | 132,45 | 808,10 | 28,51 | 26.762,12 | 26.762,12 | 0,000000000 |
| 4 | 0,00 | 29.117,74 | 139,07 | 844,46 | 29,80 | 28.104,41 | 28.104,41 | 0,000000000 |
| 5 | 0,00 | 30.573,63 | 146,02 | 882,46 | 31,14 | 29.514,00 | 29.514,00 | 0,000000000 |
| 6 | 0,00 | 32.102,31 | 153,32 | 922,17 | 32,54 | 30.994,27 | 30.994,27 | 0,000000000 |
| 7 | 0,00 | 33.707,42 | 160,99 | 963,67 | 34,00 | 32.548,76 | 32.548,76 | 0,000000000 |
| 8 | 0,00 | 35.392,79 | 169,04 | 1.007,04 | 35,53 | 34.181,18 | 34.181,18 | 0,000000000 |
| 9 | 0,00 | 37.162,43 | 177,49 | 1.052,35 | 37,13 | 35.895,45 | 35.895,45 | 0,000000000 |
| 10 | 0,00 | 39.020,55 | 186,37 | 1.099,71 | 38,80 | 37.695,67 | 37.695,67 | 0,000000000 |
| 11 | 0,00 | 40.971,58 | 195,69 | 1.149,20 | 40,55 | 39.586,15 | 39.586,15 | 0,000000000 |
| 12 | 0,00 | 43.020,16 | 205,47 | 1.200,91 | 42,37 | 41.571,41 | 41.571,41 | 0,000000000 |
| 13 | 0,00 | 45.171,17 | 215,74 | 1.254,95 | 44,28 | 43.656,19 | 43.656,19 | 0,000000000 |
| 14 | 0,00 | 47.429,73 | 226,53 | 1.311,43 | 46,27 | 45.845,50 | 45.845,50 | 0,000000000 |
| 15 | 0,00 | 49.801,21 | 237,86 | 1.370,44 | 48,35 | 48.144,56 | 48.144,56 | 0,000000000 |
| 16 | 0,00 | 52.291,27 | 249,75 | 1.432,11 | 50,53 | 50.558,88 | 50.558,88 | 0,000000000 |
| 17 | 0,00 | 54.905,84 | 262,24 | 1.496,55 | 52,80 | 53.094,24 | 53.094,24 | 0,000000000 |
| 18 | 0,00 | 57.651,13 | 275,35 | 1.563,90 | 55,18 | 55.756,70 | 55.756,70 | 0,000000000 |
| 19 | 0,00 | 60.533,69 | 289,12 | 1.634,27 | 57,66 | 58.552,63 | 58.552,63 | 0,000000000 |
| 20 | 0,00 | 63.560,37 | 303,57 | 1.707,82 | 60,26 | 61.488,72 | 61.488,72 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -45.944,64 | 0,000000000 | -45.944,64 | 0,000000000 |
| 1 | 0,892857 | 21.666,74 | 0,000000000 | -24.277,90 | 0,000000000 |
| 2 | 0,797194 | 20.315,63 | 0,000000000 | -3.962,27 | 0,000000000 |
| 3 | 0,711780 | 19.048,75 | 0,000000000 | 15.086,48 | 0,000000000 |
| 4 | 0,635518 | 17.860,86 | 0,000000000 | 32.947,34 | 0,000000000 |
| 5 | 0,567427 | 16.747,04 | 0,000000000 | 49.694,37 | 0,000000000 |
| 6 | 0,506631 | 15.702,66 | 0,000000000 | 65.397,04 | 0,000000000 |
| 7 | 0,452349 | 14.723,40 | 0,000000000 | 80.120,44 | 0,000000000 |
| 8 | 0,403883 | 13.805,21 | 0,000000000 | 93.925,65 | 0,000000000 |
| 9 | 0,360610 | 12.944,26 | 0,000000000 | 106.869,91 | 0,000000000 |
| 10 | 0,321973 | 12.137,00 | 0,000000000 | 119.006,91 | 0,000000000 |
| 11 | 0,287476 | 11.380,07 | 0,000000000 | 130.386,98 | 0,000000000 |
| 12 | 0,256675 | 10.670,34 | 0,000000000 | 141.057,32 | 0,000000000 |
| 13 | 0,229174 | 10.004,87 | 0,000000000 | 151.062,19 | 0,000000000 |
| 14 | 0,204620 | 9.380,90 | 0,000000000 | 160.443,09 | 0,000000000 |
| 15 | 0,182696 | 8.795,83 | 0,000000000 | 169.238,92 | 0,000000000 |
| 16 | 0,163122 | 8.247,25 | 0,000000000 | 177.486,17 | 0,000000000 |
| 17 | 0,145644 | 7.732,88 | 0,000000000 | 185.219,05 | 0,000000000 |
| 18 | 0,130040 | 7.250,58 | 0,000000000 | 192.469,63 | 0,000000000 |
| 19 | 0,116107 | 6.798,36 | 0,000000000 | 199.267,99 | 0,000000000 |
| 20 | 0,103667 | 6.374,34 | 0,000000000 | 205.642,32 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `4.105,700000 kg CO2e`; operação anual: bomba `9,725139` + cloro `32,637972`; crédito anual de água potável: `152,310538 kg CO2e`.
Saldo de vida: `(152,310538 − 9,725139 − 32,637972) × 20 − 4.105,700000 = **-1.906,751474 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 4.000,000000000 | 4.000,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 2.600,000000000 | 2.600,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 8.418,649590000 | 8.418,649590000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 8.418,649590000 | 8.418,649590000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 435,172964319 | 435,172964319 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 1.025,827035681 | 1.025,827035681 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 415,996819052 | 415,996819052 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 29,785966072 | 29,785966072 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 0,313630070 | 0,313630070 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 24.150,000000000 | 24.150,000000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 2.632,500000000 | 2.632,500000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 1.291,930802833 | 1.291,930802833 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 4.975,000000000 | 4.975,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 2.292,600000000 | 2.292,600000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 10.602,609240850 | 10.602,609240850 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 45.944,640043683 | 45.944,640043683 | 0,000000000000 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 104,012180397 | 104,012180397 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 114,413398437 | 114,413398437 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 1,305518893 | 1,305518893 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 26,110377859 | 26,110377859 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 28,900000000 | 28,900000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 28,900000000 | 28,900000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 25.152,997337644 | 25.152,997337644 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 24.266,752891427 | 24.266,752891427 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 205.642,322238772 | 205.642,322238773 | 0,000000000029 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | 0,000000020 | 0,000000000 | 0,000000020441 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 2 | 1.8506495949934585 | 0,149350405007 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 3 | 2.0804614711797083 | 0,919538528820 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 24.000,000000000 | 24.000,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 60,000000000 | 60,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 406,700000000 | 406,700000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 84,000000000 | 84,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 4.105,700000000 | 4.105,700000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 9,725138867 | 9,725138867 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 32,637972324 | 32,637972324 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 152,310537512 | 152,310537512 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 109,947426321 | 109,947426321 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 37,342392973 | 37,342392973 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | -1.906,751473587 | -1.906,751473587 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,028090466903 | 0,028090466903 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,127912522366 | 0,127912522366 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,819936354843 | 0,819936354843 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,139937100598 | 0,139937100598 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,000000000000 | 0,000000000000 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,011305658019 | 0,011305658019 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,166667`, econômico `0,000000`, ambiental `0,111111`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | 0,00 | 0,00 | 0,000000 | 0,000000 | 0,000000 |
| 2.500 | 272,301 | 137.815,10 | 208,19 | 0,137777 | 0,000000 | 0,156295 |
| 5.000 | 324,501 | 165.130,42 | 53,00 | 0,164189 | 0,000000 | 0,187273 |
| 7.500 | 352,803 | 178.139,44 | -223,77 | 0,178509 | 0,000000 | 0,202027 |
| 10.000 | 375,697 | 188.230,18 | -527,91 | 0,190093 | 0,000000 | 0,213471 |
| 12.500 | 394,528 | 194.867,06 | -852,59 | 0,199621 | 0,000000 | 0,220998 |
| 15.000 | 410,318 | 199.693,88 | -1.192,63 | 0,207610 | 0,000000 | 0,226472 |
| 17.500 | 423,718 | 203.246,59 | -1.544,77 | 0,214390 | 0,000000 | 0,230501 |
| 20.000 | 435,173 | 205.642,32 | -1.906,75 | 0,220186 | 0,000000 | 0,233218 |
| 22.500 | 444,949 | 207.038,28 | -2.277,26 | 0,225132 | 0,000000 | 0,234801 |
| 25.000 | 453,624 | 207.779,42 | -2.653,33 | 0,229522 | 0,000000 | 0,235641 |
| 27.500 | 461,415 | 207.993,83 | -3.033,88 | 0,233464 | 0,000000 | 0,235885 |
| 30.000 | 468,298 | 207.668,02 | -3.419,02 | 0,236946 | 0,000000 | 0,235515 |
| 32.500 | 474,381 | 207.234,46 | -3.808,23 | 0,240024 | 0,000000 | 0,235023 |
| 35.000 | 480,049 | 206.554,15 | -4.199,56 | 0,242892 | 0,000000 | 0,234252 |
| 37.500 | 485,214 | 205.573,97 | -4.593,39 | 0,245505 | 0,000000 | 0,233140 |
| 40.000 | 489,954 | 204.341,33 | -4.989,39 | 0,247904 | 0,000000 | 0,231742 |
| 42.500 | 494,336 | 202.895,65 | -5.387,18 | 0,250121 | 0,000000 | 0,230103 |
| 45.000 | 498,425 | 201.275,30 | -5.786,48 | 0,252190 | 0,000000 | 0,228265 |
| 47.500 | 502,370 | 199.569,62 | -6.186,51 | 0,254186 | 0,000000 | 0,226331 |
| 50.000 | 505,978 | 197.662,85 | -6.588,23 | 0,256011 | 0,000000 | 0,224168 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,138053 | 0,064544 | 0,318581 | 21 |
| 2.500 | 0,063213 | 0,100273 | 0,613344 | 20 |
| 5.000 | 0,048932 | 0,110548 | 0,693180 | 17 |
| 7.500 | 0,041417 | 0,115419 | 0,735922 | 13 |
| 10.000 | 0,035720 | 0,119223 | 0,769462 | 9 |
| 12.500 | 0,031652 | 0,122179 | 0,794239 | 7 |
| 15.000 | 0,029085 | 0,124524 | 0,810655 | 4 |
| 17.500 | 0,027942 | 0,126404 | 0,818965 | 2 |
| 20.000 | 0,028090 | 0,127913 | 0,819936 | 1 |
| 22.500 | 0,029328 | 0,129106 | 0,814888 | 3 |
| 25.000 | 0,031345 | 0,130134 | 0,805886 | 5 |
| 27.500 | 0,033931 | 0,131050 | 0,794336 | 6 |
| 30.000 | 0,036941 | 0,131843 | 0,781137 | 8 |
| 32.500 | 0,040248 | 0,132548 | 0,767077 | 10 |
| 35.000 | 0,043737 | 0,133261 | 0,752895 | 11 |
| 37.500 | 0,047369 | 0,133955 | 0,738761 | 12 |
| 40.000 | 0,051102 | 0,134651 | 0,724892 | 14 |
| 42.500 | 0,054909 | 0,135367 | 0,711424 | 15 |
| 45.000 | 0,058770 | 0,136119 | 0,698445 | 16 |
| 47.500 | 0,062664 | 0,136947 | 0,686070 | 18 |
| 50.000 | 0,066596 | 0,137797 | 0,674177 | 19 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 0,0% | 100,0% |
| 2.500 | 46,2% | 0,0% | 33,7% |
| 5.000 | 35,9% | 0,0% | 20,6% |
| 7.500 | 30,3% | 0,0% | 14,4% |
| 10.000 | 25,7% | 0,0% | 9,5% |
| 12.500 | 22,0% | 0,0% | 6,3% |
| 15.000 | 18,9% | 0,0% | 4,0% |
| 17.500 | 16,3% | 0,0% | 2,3% |
| 20.000 | 14,0% | 0,0% | 1,1% |
| 22.500 | 12,1% | 0,0% | 0,5% |
| 25.000 | 10,3% | 0,0% | 0,1% |
| 27.500 | 8,8% | 0,0% | 0,0% |
| 30.000 | 7,4% | 0,0% | 0,2% |
| 32.500 | 6,2% | 0,0% | 0,4% |
| 35.000 | 5,1% | 0,0% | 0,7% |
| 37.500 | 4,1% | 0,0% | 1,2% |
| 40.000 | 3,2% | 0,0% | 1,8% |
| 42.500 | 2,3% | 0,0% | 2,5% |
| 45.000 | 1,5% | 0,0% | 3,2% |
| 47.500 | 0,7% | 0,0% | 4,1% |
| 50.000 | 0,0% | 0,0% | 5,0% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Caso 3 — Escola Pública de Tempo Integral Amazonas (Manaus3)

Projeto: [`estudo_caso_3_manaus3.netuno`](estudo_caso_3_manaus3.netuno). Série: `Manaus3.csv`, `31410` dias (`85,9959` anos de 365,25 dias), precipitação média anual `1.802,57 mm/ano`; SHA-256 `6f91aa11c06482fc8708bccd953900d091f636abe23874d51bffc510d1a0d153`.

### 1. Entradas e demanda

- Demanda total: `350 × 40,0 = 14.000,0 L/dia`.
- Demanda pluvial-alvo: `14.000,0 × 0,500 = 7.000,0 L/dia`.
- Demanda total anual equivalente: `14.000,0 × 365,25 / 1000 = 5.113,500 m³/ano`.
- Área `1.400,0 m²`, coeficiente `0,800`, limiar `1,50 mm`, modo `3`.

### 2. Um dia auditado e conservação de massa

No dia de índice `1`, `P=9,8940 mm` e `Pef=8,3940 mm`. Logo, `Vcap = 8,3940 × 1.400,0 × 0,800 = 9.401,2733 L`.

Balanço dos dois reservatórios (o recalque é transferência interna): estoque inicial + captação = estoque final + consumo pluvial + extravasamento. `0,0000 + 9.401,2733 = 2.401,2733 + 7.000,0000 + 0,0000`. Resíduo: `0,000000000 L`.

### 3. Indicadores técnicos do volume TOPSIS

Volume selecionado: `30.000 L`. Consumo anual: `3.295,943200 × 365,25 / 1000 = 1.203,843254 m³/ano`.
Potencial: `100 × 3.295,943200 / 14.000,0 = 23,542451%`.
Ganho marginal do ponto: `0,177472 %/m³`; limiar técnico: `3,500 %/m³`.

### 4. CAPEX, bombeamento, cloro e O&M

CAPEX = cisterna `23.625,00` + caixa `3.913,65` + bombas `974,24` + tubos `6.500,00` + acessórios `2.353,09` + mão de obra `11.209,79` = **R$ 48.575,78**.
Recalque anual: `103.525.575,901 / 85,9959 = 1.203.843,254 L/ano`; partidas: `24.951 / 85,9959 = 290,142 /ano`.
Energia: `0,7350 × [(1.203.843,254 / 5.400,0) + (290,142 × 0,0300)] / 0,6000 = 283,756781 kWh/ano`.
Cloro equivalente: `1.203,843254 × 2,500 / 1000 = 3,009608 kg Cl2-eq/ano`; custo `= 3,009608 × 22,00 = R$ 66,21/ano`.
O&M anualizado: **R$ 740,00/ano**. Todos os itens deste caso têm coeficiente variável igual a zero; portanto, o valor não depende da capacidade nem do volume tratado.

### 5. Economia e VPL

Tarifa marginal evitada: água `R$ 25,300000/m³` + esgoto `R$ 20,240000/m³`, obtida comparando a conta para a demanda total simulada com a conta após a economia pluvial.
Ano 1: economia bruta `1.203,843254 × (25,300000 + 20,240000) = R$ 54.823,02`; fluxo líquido `= 54.823,02 − 740,00 − 326,32 − 66,21 = R$ 53.690,49`.
VPL manual: soma dos 21 fluxos descontados (ano 0 a 20) = **R$ 602.089,29**.
TIR: com `r=115,536764% a.a.`, `Σ FC_t/(1+r)^t = R$ -0,000000002`. Paybacks obtidos pela primeira mudança do acumulado para valor não negativo: simples `1` ano(s) e descontado `1` ano(s).

#### Fluxo de caixa: verificação termo a termo

Em cada ano, a coluna manual recompõe `FC = −CAPEX + economia bruta − energia − O&M − cloro`; o fator é `(1 + TMA)^−t`. Os resíduos comparam essa substituição com o objeto retornado pelo motor.

##### Fluxos nominais

| Ano | CAPEX (R$) | Economia bruta (R$) | Energia (R$) | O&M (R$) | Cloro (R$) | FC sistema (R$) | FC manual (R$) | Resíduo FC (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 48.575,78 | 0,00 | 0,00 | 0,00 | 0,00 | -48.575,78 | -48.575,78 | 0,000000000 |
| 1 | 0,00 | 54.823,02 | 326,32 | 740,00 | 66,21 | 53.690,49 | 53.690,49 | 0,000000000 |
| 2 | 0,00 | 57.564,17 | 342,64 | 773,30 | 69,19 | 56.379,05 | 56.379,05 | 0,000000000 |
| 3 | 0,00 | 60.442,38 | 359,77 | 808,10 | 72,30 | 59.202,21 | 59.202,21 | 0,000000000 |
| 4 | 0,00 | 63.464,50 | 377,76 | 844,46 | 75,56 | 62.166,72 | 62.166,72 | 0,000000000 |
| 5 | 0,00 | 66.637,73 | 396,64 | 882,46 | 78,96 | 65.279,66 | 65.279,66 | 0,000000000 |
| 6 | 0,00 | 69.969,61 | 416,48 | 922,17 | 82,51 | 68.548,45 | 68.548,45 | 0,000000000 |
| 7 | 0,00 | 73.468,09 | 437,30 | 963,67 | 86,22 | 71.980,90 | 71.980,90 | 0,000000000 |
| 8 | 0,00 | 77.141,50 | 459,17 | 1.007,04 | 90,10 | 75.585,19 | 75.585,19 | 0,000000000 |
| 9 | 0,00 | 80.998,57 | 482,12 | 1.052,35 | 94,16 | 79.369,93 | 79.369,93 | 0,000000000 |
| 10 | 0,00 | 85.048,50 | 506,23 | 1.099,71 | 98,40 | 83.344,16 | 83.344,16 | 0,000000000 |
| 11 | 0,00 | 89.300,93 | 531,54 | 1.149,20 | 102,82 | 87.517,36 | 87.517,36 | 0,000000000 |
| 12 | 0,00 | 93.765,97 | 558,12 | 1.200,91 | 107,45 | 91.899,49 | 91.899,49 | 0,000000000 |
| 13 | 0,00 | 98.454,27 | 586,02 | 1.254,95 | 112,29 | 96.501,01 | 96.501,01 | 0,000000000 |
| 14 | 0,00 | 103.376,98 | 615,33 | 1.311,43 | 117,34 | 101.332,89 | 101.332,89 | 0,000000000 |
| 15 | 0,00 | 108.545,83 | 646,09 | 1.370,44 | 122,62 | 106.406,68 | 106.406,68 | 0,000000000 |
| 16 | 0,00 | 113.973,12 | 678,40 | 1.432,11 | 128,14 | 111.734,48 | 111.734,48 | 0,000000000 |
| 17 | 0,00 | 119.671,78 | 712,32 | 1.496,55 | 133,90 | 117.329,01 | 117.329,01 | 0,000000000 |
| 18 | 0,00 | 125.655,37 | 747,93 | 1.563,90 | 139,93 | 123.203,61 | 123.203,61 | 0,000000000 |
| 19 | 0,00 | 131.938,14 | 785,33 | 1.634,27 | 146,23 | 129.372,31 | 129.372,31 | 0,000000000 |
| 20 | 0,00 | 138.535,05 | 824,60 | 1.707,82 | 152,81 | 135.849,83 | 135.849,83 | 0,000000000 |

##### Desconto e acumulado

| Ano | Fator manual | FC descontado do sistema (R$) | Resíduo do desconto (R$) | Acumulado do sistema (R$) | Resíduo acumulado (R$) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1,000000 | -48.575,78 | 0,000000000 | -48.575,78 | 0,000000000 |
| 1 | 0,909091 | 48.809,54 | 0,000000000 | 233,76 | 0,000000000 |
| 2 | 0,826446 | 46.594,25 | 0,000000000 | 46.828,01 | 0,000000000 |
| 3 | 0,751315 | 44.479,50 | 0,000000000 | 91.307,51 | 0,000000000 |
| 4 | 0,683013 | 42.460,71 | 0,000000000 | 133.768,22 | 0,000000000 |
| 5 | 0,620921 | 40.533,53 | 0,000000000 | 174.301,75 | 0,000000000 |
| 6 | 0,564474 | 38.693,81 | 0,000000000 | 212.995,56 | 0,000000000 |
| 7 | 0,513158 | 36.937,58 | 0,000000000 | 249.933,14 | 0,000000000 |
| 8 | 0,466507 | 35.261,05 | 0,000000000 | 285.194,19 | 0,000000000 |
| 9 | 0,424098 | 33.660,60 | 0,000000000 | 318.854,79 | 0,000000000 |
| 10 | 0,385543 | 32.132,78 | 0,000000000 | 350.987,58 | 0,000000000 |
| 11 | 0,350494 | 30.674,30 | 0,000000000 | 381.661,88 | 0,000000000 |
| 12 | 0,318631 | 29.282,01 | 0,000000000 | 410.943,89 | 0,000000000 |
| 13 | 0,289664 | 27.952,90 | 0,000000000 | 438.896,79 | 0,000000000 |
| 14 | 0,263331 | 26.684,12 | 0,000000000 | 465.580,91 | 0,000000000 |
| 15 | 0,239392 | 25.472,91 | 0,000000000 | 491.053,82 | 0,000000000 |
| 16 | 0,217629 | 24.316,68 | 0,000000000 | 515.370,50 | 0,000000000 |
| 17 | 0,197845 | 23.212,92 | 0,000000000 | 538.583,42 | 0,000000000 |
| 18 | 0,179859 | 22.159,25 | 0,000000000 | 560.742,67 | 0,000000000 |
| 19 | 0,163508 | 21.153,41 | 0,000000000 | 581.896,08 | 0,000000000 |
| 20 | 0,148644 | 20.193,21 | 0,000000000 | 602.089,29 | 0,000000000 |

### 6. ACV de triagem

Impacto incorporado total: `3.571,900000 kg CO2e`; operação anual: bomba `24,119326` + cloro `75,240203`; crédito anual de água potável: `421,345139 kg CO2e`.
Saldo de vida: `(421,345139 − 24,119326 − 75,240203) × 20 − 3.571,900000 = **2.867,812181 kg CO2e**`.

### 7. Comparação item a item: conta manual × sistema

Cada linha abaixo possui substituição numérica própria. `Manual` é recomposto das entradas elementares; `Sistema` é o campo retornado pelo motor. O resíduo é `|Manual − Sistema|`, exceto nas identidades de fechamento.

| Item | Equação/identidade manual | Manual | Sistema | Resíduo absoluto |
| --- | --- | ---: | ---: | ---: |
| Demanda total (L/d) | `N × d` | 14.000,000000000 | 14.000,000000000 | 0,000000000000 |
| Demanda pluvial-alvo (L/d) | `D × f` | 7.000,000000000 | 7.000,000000000 | 0,000000000000 |
| Captação do dia (L) | `Pef × A × C` | 9.401,273280000 | 9.401,273280000 | 0,000000000000 |
| Conservação de massa do dia (L) | `estoque inicial + captação = estoque final + consumo + extravasamento` | 9.401,273280000 | 9.401,273280000 | 0,000000000000 |
| Água pluvial anual (m³/a) | `média diária × 365,25 / 1000` | 1.203,843253671 | 1.203,843253671 | 0,000000000000 |
| Água potável anual (m³/a) | `média diária × 365,25 / 1000` | 3.909,656746329 | 3.909,656746329 | 0,000000000000 |
| Extravasamento anual (m³/a) | `média diária × 365,25 / 1000` | 697,551960109 | 697,551960109 | 0,000000000000 |
| Potencial de economia (%) | `100 × Qpluvial / Dtotal` | 23,542451426 | 23,542451426 | 0,000000000000 |
| Fechamento dos estados de atendimento (%) | `pleno + parcial + nulo = 100` | 100,000000000 | 100,000000000 | 0,000000000000 |
| Ganho marginal (%/m³) | `Δpotencial / ΔV` | 0,177471591 | 0,177471591 | 0,000000000000 |
| CAPEX — cisterna inferior (R$) | `interpolação × μmaterial` | 23.625,000000000 | 23.625,000000000 | 0,000000000000 |
| CAPEX — reservatório superior (R$) | `interpolação × μmaterial` | 3.913,650000000 | 3.913,650000000 | 0,000000000000 |
| CAPEX — bombas (R$) | `preço unitário × quantidade` | 974,238999619 | 974,238999619 | 0,000000000000 |
| CAPEX — tubos e conexões (R$) | `max(350; 1,25 Σ L·preçoDN)` | 6.500,000000000 | 6.500,000000000 | 0,000000000000 |
| CAPEX — acessórios (R$) | `max(500; 150 + 0,08·tanques)` | 2.353,092000000 | 2.353,092000000 | 0,000000000000 |
| CAPEX — mão de obra (R$) | `max(1400; 0,30·subtotal)` | 11.209,794299886 | 11.209,794299886 | 0,000000000000 |
| CAPEX total (R$) | `Σ componentes` | 48.575,775299505 | 48.575,775299505 | 0,000000000000 |
| Horas equivalentes de bombeamento (h/a) | `(V/Q + n·tpartida)/η` | 386,063647884 | 386,063647884 | 0,000000000000 |
| Energia da bomba (kWh/a) | `potência × horas equivalentes` | 283,756781195 | 283,756781195 | 0,000000000000 |
| Cloro equivalente (kg/a) | `m³ × mg/L / 1000` | 3,009608134 | 3,009608134 | 0,000000000000 |
| Custo de cloro (R$/a) | `massa × preço/kg` | 66,211378952 | 66,211378952 | 0,000000000000 |
| O&M anual (R$/a) | `Σ 12/p · (fixo + variável·m³mês)` | 740,000000000 | 740,000000000 | 0,000000000000 |
| Tarifa efetiva de água (R$/m³) | `Δconta de água / m³ poupado` | 25,300000000 | 25,300000000 | 0,000000000000 |
| Tarifa efetiva de esgoto (R$/m³) | `(Δconta total − Δágua) / m³ poupado` | 20,240000000 | 20,240000000 | 0,000000000000 |
| Economia bruta ano 1 (R$) | `m³ × (Tágua + Tesgoto)` | 54.823,021772189 | 54.823,021772189 | 0,000000000000 |
| Fluxo líquido ano 1 (R$) | `bruta − energia − O&M − cloro` | 53.690,490094863 | 53.690,490094863 | 0,000000000000 |
| VPL (R$) | `Σ FCt/(1+i)^t` | 602.089,291101272 | 602.089,291101271 | 0,000000000116 |
| Resíduo da TIR (R$) | `Σ FCt/(1+TIR)^t` | -0,000000002 | 0,000000000 | 0,000000002486 |
| Payback simples (anos) | `primeiro acumulado nominal ≥ 0` | 1 | 0.9047370440031254 | 0,095262955997 |
| Payback descontado (anos) | `primeiro acumulado descontado ≥ 0` | 1 | 0.9501660307147913 | 0,049833969285 |
| Massa da cisterna inferior (kg) | `V × kg material/m³` | 600,000000000 | 600,000000000 | 0,000000000000 |
| Massa do reservatório superior (kg) | `Vsup × kg material/m³` | 100,000000000 | 100,000000000 | 0,000000000000 |
| CO2e incorporado dos tubos (kg) | `Σ L × fatorDN` | 536,900000000 | 536,900000000 | 0,000000000000 |
| CO2e incorporado das bombas (kg) | `fator unitário × quantidade` | 60,000000000 | 60,000000000 | 0,000000000000 |
| CO2e incorporado total (kg) | `Σ materiais e equipamentos` | 3.571,900000000 | 3.571,900000000 | 0,000000000000 |
| CO2e do bombeamento (kg/a) | `kWh × fator da rede` | 24,119326402 | 24,119326402 | 0,000000000000 |
| CO2e do tratamento (kg/a) | `kg Cl2 × fator do insumo` | 75,240203354 | 75,240203354 | 0,000000000000 |
| CO2e evitado da rede (kg/a) | `m³ poupado × fator da água` | 421,345138785 | 421,345138785 | 0,000000000000 |
| CO2e líquido anual (kg/a) | `evitado − bomba − tratamento` | 321,985609029 | 321,985609029 | 0,000000000000 |
| Payback ambiental (anos) | `incorporado / líquido anual` | 11,093352932 | 11,093352932 | 0,000000000000 |
| CO2e líquido de vida (kg) | `líquido anual × vida − incorporado` | 2.867,812180579 | 2.867,812180579 | 0,000000000000 |
| TOPSIS D+ | `distância euclidiana ao ideal` | 0,016636815492 | 0,016636815492 | 0,000000000000000 |
| TOPSIS D− | `distância euclidiana ao anti-ideal` | 0,138120568302 | 0,138120568302 | 0,000000000000000 |
| Score TOPSIS | `D−/(D+ + D−)` | 0,892497436411 | 0,892497436411 | 0,000000000000000 |
| Gap técnico | `(máx − x)/(máx − mín)` | 0,118610407936 | 0,118610407936 | 0,000000000000000 |
| Gap econômico | `(máx − x)/(máx − mín)` | 0,000000000000 | 0,000000000000 | 0,000000000000000 |
| Gap ambiental | `(máx − x)/(máx − mín)` | 0,087112569662 | 0,087112569662 | 0,000000000000000 |

#### TOPSIS: conta completa por alternativa

A matriz é transladada pelo pior observado em cada coluna, normalizada vetorialmente e ponderada. Pesos efetivos: técnico `0,166667`, econômico `0,000000`, ambiental `0,111111`.

##### Critérios e normalização

| V (L) | Água (m³/a) | VPL (R$) | CO2 líquido (kg) | r técnico | r econômico | r ambiental |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0,000 | 0,00 | 0,00 | 0,000000 | 0,000000 | 0,000000 |
| 3.000 | 400,955 | 191.824,12 | 864,34 | 0,077388 | 0,000000 | 0,074703 |
| 6.000 | 683,822 | 343.943,22 | 2.121,19 | 0,131983 | 0,000000 | 0,133943 |
| 9.000 | 868,602 | 442.320,90 | 2.857,61 | 0,167647 | 0,000000 | 0,172255 |
| 12.000 | 948,208 | 482.663,23 | 3.029,13 | 0,183012 | 0,000000 | 0,187966 |
| 15.000 | 1.012,660 | 514.436,69 | 3.119,16 | 0,195452 | 0,000000 | 0,200339 |
| 18.000 | 1.065,152 | 539.775,82 | 3.145,34 | 0,205583 | 0,000000 | 0,210207 |
| 21.000 | 1.108,797 | 560.267,85 | 3.123,95 | 0,214007 | 0,000000 | 0,218188 |
| 24.000 | 1.145,039 | 576.706,67 | 3.063,06 | 0,221002 | 0,000000 | 0,224590 |
| 27.000 | 1.176,618 | 590.590,31 | 2.977,10 | 0,227097 | 0,000000 | 0,229996 |
| 30.000 | 1.203,843 | 602.089,29 | 2.867,81 | 0,232352 | 0,000000 | 0,234474 |
| 33.000 | 1.227,805 | 612.085,59 | 2.741,12 | 0,236976 | 0,000000 | 0,238367 |
| 36.000 | 1.249,004 | 620.569,05 | 2.599,62 | 0,241068 | 0,000000 | 0,241671 |
| 39.000 | 1.268,340 | 628.031,66 | 2.448,12 | 0,244800 | 0,000000 | 0,244577 |
| 42.000 | 1.285,867 | 634.504,26 | 2.286,99 | 0,248183 | 0,000000 | 0,247098 |
| 45.000 | 1.301,708 | 640.052,42 | 2.116,77 | 0,251240 | 0,000000 | 0,249259 |
| 48.000 | 1.316,169 | 644.845,05 | 1.939,18 | 0,254031 | 0,000000 | 0,251125 |
| 51.000 | 1.329,966 | 649.274,63 | 1.758,05 | 0,256695 | 0,000000 | 0,252850 |
| 54.000 | 1.342,564 | 653.046,93 | 1.570,49 | 0,259126 | 0,000000 | 0,254319 |
| 57.000 | 1.354,485 | 656.448,59 | 1.379,30 | 0,261427 | 0,000000 | 0,255644 |
| 60.000 | 1.365,847 | 659.543,85 | 1.185,12 | 0,263620 | 0,000000 | 0,256849 |

##### Distâncias e ranking

| V (L) | D+ | D− | C | Rank |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0,154578 | 0,000000 | 0,000000 | 21 |
| 3.000 | 0,110268 | 0,044340 | 0,286790 | 20 |
| 6.000 | 0,068610 | 0,088116 | 0,562229 | 19 |
| 9.000 | 0,045587 | 0,115434 | 0,716888 | 16 |
| 12.000 | 0,037726 | 0,124079 | 0,766843 | 13 |
| 15.000 | 0,031742 | 0,130065 | 0,803827 | 11 |
| 18.000 | 0,026985 | 0,133998 | 0,832375 | 9 |
| 21.000 | 0,023051 | 0,136444 | 0,855474 | 7 |
| 24.000 | 0,019923 | 0,137687 | 0,873595 | 5 |
| 27.000 | 0,017643 | 0,138220 | 0,886804 | 3 |
| 30.000 | 0,016637 | 0,138121 | 0,892497 | 1 |
| 33.000 | 0,017153 | 0,137599 | 0,889158 | 2 |
| 36.000 | 0,019181 | 0,136758 | 0,876995 | 4 |
| 39.000 | 0,022331 | 0,135765 | 0,858751 | 6 |
| 42.000 | 0,026306 | 0,134650 | 0,836564 | 8 |
| 45.000 | 0,030876 | 0,133452 | 0,812105 | 10 |
| 48.000 | 0,035856 | 0,132241 | 0,786694 | 12 |
| 51.000 | 0,041050 | 0,131144 | 0,761605 | 14 |
| 54.000 | 0,046506 | 0,130099 | 0,736669 | 15 |
| 57.000 | 0,052109 | 0,129200 | 0,712595 | 17 |
| 60.000 | 0,057828 | 0,128479 | 0,689608 | 18 |

##### Distância relativa ao melhor de cada critério

| V (L) | Gap técnico | Gap econômico | Gap ambiental |
| ---: | ---: | ---: | ---: |
| 0 | 100,0% | 0,0% | 100,0% |
| 3.000 | 70,6% | 0,0% | 70,9% |
| 6.000 | 49,9% | 0,0% | 47,9% |
| 9.000 | 36,4% | 0,0% | 32,9% |
| 12.000 | 30,6% | 0,0% | 26,8% |
| 15.000 | 25,9% | 0,0% | 22,0% |
| 18.000 | 22,0% | 0,0% | 18,2% |
| 21.000 | 18,8% | 0,0% | 15,1% |
| 24.000 | 16,2% | 0,0% | 12,6% |
| 27.000 | 13,9% | 0,0% | 10,5% |
| 30.000 | 11,9% | 0,0% | 8,7% |
| 33.000 | 10,1% | 0,0% | 7,2% |
| 36.000 | 8,6% | 0,0% | 5,9% |
| 39.000 | 7,1% | 0,0% | 4,8% |
| 42.000 | 5,9% | 0,0% | 3,8% |
| 45.000 | 4,7% | 0,0% | 3,0% |
| 48.000 | 3,6% | 0,0% | 2,2% |
| 51.000 | 2,6% | 0,0% | 1,6% |
| 54.000 | 1,7% | 0,0% | 1,0% |
| 57.000 | 0,8% | 0,0% | 0,5% |
| 60.000 | 0,0% | 0,0% | 0,0% |

Para cada linha, `C = D- / (D+ + D-)`. Os três gaps são independentes dos pesos: 0% é o ótimo observado no eixo e 100% é o pior valor observado.

## Referências e rastreabilidade

- [Atlas de fluxogramas metodológicos](../netuno/docs/fluxogramas_metodologicos.md): cadeia visual das equações e decisões implementadas.
- GHISI, E.; CORDOVA, M. M. *Netuno 4 — Manual do Usuário*. UFSC, 2014. Cópia local em [`additional_material/documentation/Manual-Netuno-4_Junho2014.pdf`](../additional_material/documentation/Manual-Netuno-4_Junho2014.pdf).
- ROCHA, V. L. *Validação do algoritmo do programa Netuno para avaliação do potencial de economia de água potável e dimensionamento de reservatórios de sistemas de aproveitamento de água pluvial em edificações*. Dissertação (Mestrado em Engenharia Civil) — UFSC, 2009. [Registro institucional](https://repositorio.ufsc.br/handle/123456789/92966).
- HWANG, C.-L.; YOON, K. *Multiple Attribute Decision Making*. Springer, 1981. [DOI](https://doi.org/10.1007/978-3-642-48318-9).
- [MCTI/SIRENE — fatores de emissão](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao). O fator deve ser escolhido para o período do estudo; o valor padrão do software é apenas uma hipótese editável de triagem.
