# Os processos do programa

São **24 processos**, do arquivo de chuva ao relatório. Cada
um declara o que o dispara, o que recebe, as regras com suas ramificações, o
que produz e o que acontece quando falha.

É o apêndice mais técnico do manual, e serve a duas pessoas: quem revisa um
estudo feito com o programa e precisa saber exatamente que conta foi feita, e
quem encontrou um resultado estranho e quer saber por onde o número passou.

Os nomes em `código` são os campos do arquivo de projeto, listados na seção {{n:A}}.

## PROC-01 — Carregar a série de precipitação

*Chuva*

**Gatilho.** Aba Projeto: escolher cidade na base nacional ou abrir arquivo CSV.

**Entradas**

- Arquivo CSV diário, ou cidade da base CMIP6 (652 cidades, 19 modelos, 3 cenários)
- `climate_start_date` e `climate_end_date`, que recortam a série
- `start_date`, data do primeiro dia da série

**Regras**

1. A série vira um vetor `numpy` de milímetros por dia; o índice do vetor é o dia, e a data serve só para saber o dia da semana e o mês.
2. Ano incompleto é descartado na leitura, para não enviesar totais anuais.
3. A base climática de 6,5 GB é distribuída à parte; sem ela, a aba cai para arquivo do usuário.

**Saídas**

- `precip_data`: vetor de mm/dia, que é a entrada de **dois** processos distintos — PROC-04 (descarte e captação) e PROC-03 (supressão de irrigação)

**Exceção.** Arquivo ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; a simulação não roda com série vazia.

## PROC-02 — Compor a demanda diária

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

## PROC-03 — Suprimir a irrigação nos dias de chuva

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

## PROC-04 — Descartar as primeiras águas

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

## PROC-05 — Converter lâmina em volume captado

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

## PROC-06 — Armazenar e extravasar

*Balanço hídrico*

**Gatilho.** Todo dia, depois da captação.

**Entradas**

- `v_ac`
- volume remanescente do dia anterior
- `lower_tank_vol`

**Regras**

1. **Modelo YAS**: o extravasamento é calculado **antes** de retirar a demanda.
2. `disponível = v_lower + v_ac`. Se passar da capacidade, o excedente extravasa e o reservatório fica cheio.
3. A ordem importa: retirar a demanda antes faria o reservatório aceitar água que fisicamente já teria extravasado, superestimando o aproveitamento.

**Saídas**

- `v_spill_today`, somado em `avg_spilled_l_day`, que vira critério de extravasamento no multicritério
- `v_in_tank`, o volume disponível para atendimento

**Exceção.** Volume zero é válido e representa o cenário sem sistema; negativo é rejeitado.

## PROC-07 — Atender com reservatório único

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

## PROC-08 — Atender com recalque para caixa superior

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

## PROC-09 — Repartir o atendimento e completar com potável

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
- `avg_pluvial_indoor_consumed_l_day` e `avg_pluvial_irrigation_consumed_l_day`, que separam o uso interno do externo para os créditos WEc1 e WEc2 do LEED

**Exceção.** Nenhuma: todas as parcelas são mínimos e máximos com zero.

## PROC-10 — Classificar o atendimento do dia

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

## PROC-11 — Validar a entrada física

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

## PROC-12 — Agregar o período e calcular os indicadores

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

## PROC-13 — Varrer volumes e achar o volume ideal

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

## PROC-14 — Calcular os índices pluviométricos

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

## PROC-15 — Dimensionar a estação de tratamento

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

## PROC-16 — Calcular a energia de bombeamento

*Motobomba*

**Gatilho.** Econômico e ACV, a partir do mesmo resultado de simulação.

**Entradas**

- `total_pumped_liters` e `total_pump_cycles` de PROC-08
- `pump_power_kw`, `pump_efficiency`, `pump_flow_rate`
- `pump_manometric_head_m`
- `pump_startup_time_h`

**Regras**

1. Energia específica `e = ρgH/(η_bomba·η_motor)` por m³ recalcado, ou `P/(Q·η_motor)` quando a vazão é declarada.
2. A potência de placa é potência de eixo e **já embute** o rendimento da bomba; por isso `P × horas / η_bomba` conta esse rendimento duas vezes, e o que falta é dividir pelo rendimento do motor, da ABNT NBR 17094-2. Quatro cópias dessa fórmula antiga sobreviviam no programa e superestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no multicritério.
3. A energia de partida entra à parte, pelo número de ciclos.
4. Vazão e rendimento não informados caem para valores típicos **da potência escolhida**, e não para constantes fixas.

**Saídas**

- `annual_kwh`, que vira custo no econômico e emissão na ACV
- `pump_hours_year`, `annual_cycles`

**Exceção.** Sem caixa superior, ou com potência zero, a energia é zero e o processo não roda.

## PROC-17 — Calcular a fatura de água e esgoto

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
7. Os cinco regimes de mínimo estão nomeados e auditados na base dos 652 municípios.

**Saídas**

- Valor da fatura de água e esgoto em R$/mês, para a projeção de PROC-18

**Exceção.** Tabela vazia cai para a estrutura da CASAN. Estrutura incompleta é sinalizada pela porta de validação, que separa erro de aviso.

## PROC-18 — Projetar o fluxo de caixa

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

## PROC-19 — Avaliar o ciclo de vida

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
3. A linha de tratamento **substitui** o termo de cloração; não soma a ele.
4. A água evitada é a **entregue**, não a produzida: as perdas de distribuição no Brasil vão de 33,9% no Sudeste a 46,9% no Norte, de modo que produzir 1 m³ entrega de 0,53 a 0,66 m³. O fator publicado de 0,236 kg CO₂e/m³ é de saída de estação; por m³ entregue vira de 0,336 a 0,461 conforme a macrorregião.
5. O payback de carbono é o carbono incorporado dividido pela economia anual líquida; sem economia líquida positiva, devolve 999 anos em vez de infinito.

**Saídas**

- `total_embodied_co2_kg`, `net_annual_avoided_co2_kg`
- `lifetime_net_co2_saved_kg`, que é critério do multicritério
- `environmental_payback_years`
- `inventory_items`, o inventário item a item

**Exceção.** Fator sem procedência primária recebe rótulo de triagem, e o rótulo é exibido — a lacuna é declarada, não escondida.

## PROC-20 — Enquadrar nas certificações

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
2. **LEED v5 BD+C** (rating system de novembro de 2025): WEc2 até 8 pontos, pela Opção 1 (projeto inteiro, 30% a 65%, +1 com fonte alternativa) ou pela soma das Opções 2 (louças e metais, 30% a 40%), 4 (externo, 50% e 100%) e 6 (fonte alternativa, 2 pontos). SSc3 registrado como não avaliado.
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

## PROC-21 — Ordenar volumes por múltiplos critérios

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

## PROC-22 — Gravar e reabrir o projeto

*Arquivo do projeto*

**Gatilho.** Menu de salvar e de abrir.

**Entradas**

- `NetunoConfig` inteiro, com os campos da seção {{n:A}}
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

## PROC-23 — Emitir relatórios e exportações

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

## PROC-24 — Automação para estudos de larga escala

*Automação*

**Gatilho.** Linha de comando `netuno`, descrita na seção {{n:19}}; acompanha a instalação como pacote Python, e não o instalador de Windows.

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

