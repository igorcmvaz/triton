# -*- coding: utf-8 -*-
"""A matriz de processos do Netuno 5, escrita a partir da leitura do fonte.

Cada processo declara gatilho, entradas, regras, funcoes envolvidas, saidas e
tratamento de excecao. As funcoes citadas existem: um verificador ao fim do
arquivo confere cada nome contra o fonte antes de a pagina ser montada.
"""

# (id, nome, familia, gatilho, [entradas], [regras], [(modulo, funcao)], [saidas], excecao)
PROCESSOS = [
(
 "PROC-01", "Carregar a série de precipitação", "chuva",
 "Aba Projeto: escolher cidade na base nacional ou abrir arquivo CSV.",
 ["Arquivo CSV diário, ou cidade da base CMIP6 (652 cidades, 19 modelos, 3 cenários)",
  "<code>climate_start_date</code> e <code>climate_end_date</code>, que recortam a série",
  "<code>start_date</code>, data do primeiro dia da série"],
 ["A série vira um vetor <code>numpy</code> de milímetros por dia; o índice do vetor "
  "é o dia, e a data serve só para saber o dia da semana e o mês.",
  "Ano incompleto é descartado na leitura, para não enviesar totais anuais.",
  "A base climática de 6,5 GB é distribuída à parte; sem ela, a aba cai para arquivo do usuário."],
 [("climate_database.py", "load_national_climate_series"),
  ("climate_database.py", "get_climate_file_path"),
  ("parser.py", "load_precipitation")],
 ["<code>precip_data</code>: vetor de mm/dia, que é a entrada de <b>dois</b> processos "
  "distintos — PROC-04 (descarte e captação) e PROC-03 (supressão de irrigação)"],
 "Arquivo ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; "
 "a simulação não roda com série vazia.",
),
(
 "PROC-02", "Compor a demanda diária", "demanda",
 "Início da simulação, uma vez por execução.",
 ["<code>demand_mode</code>: constante, semanal, mensal ou diária",
  "<code>demand_value</code> (L/dia por pessoa), <code>residents_count</code>",
  "<code>rainwater_share</code> ou <code>non_potable_indoor_share</code>",
  "vetores <code>weekly_*</code>, <code>monthly_*</code>, <code>daily_*</code> quando o modo os usa"],
 ["Demanda-base do dia = <code>demand_value × residents_count</code>, com o multiplicador "
  "do dia da semana, do mês ou do dia, conforme o modo.",
  "A fração não potável separa a demanda em duas: interna potável e interna não potável.",
  "Quando o modo é semanal, mensal ou diário, a fração vem do próprio vetor do período; "
  "fora disso, vale <code>non_potable_indoor_share</code>, e só então <code>rainwater_share</code>.",
  "Valor nulo ou zero em qualquer posição do vetor cai para o valor constante."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>tot_arr</code>: demanda total do dia",
  "<code>pot_in_arr</code>: potável interna, que a chuva nunca atende",
  "<code>non_pot_in_arr</code>: não potável interna, prioridade 1 da chuva",
  "<code>pluv_arr</code> = não potável interna + irrigação ativa"],
 "Data inicial ilegível cai para 01/01/1980 em vez de interromper, porque só afeta "
 "o dia da semana.",
),
(
 "PROC-03", "Suprimir a irrigação nos dias de chuva", "demanda",
 "Composição da demanda, um teste por dia da série.",
 ["<code>irrigation_liters_per_day</code>",
  "<code>irrigation_rain_threshold_mm</code> (padrão 2 mm/dia)",
  "<code>precip_data</code>, o <b>mesmo</b> vetor que alimenta a captação"],
 ["Se a chuva do dia ≥ limiar, a irrigação do dia é <b>zero</b> e o dia entra na contagem "
  "de dias suprimidos.",
  "Caso contrário, a irrigação do dia é o volume nominal.",
  "É a segunda leitura do arquivo de chuva, e independente da primeira: um dia pode "
  "suprimir a irrigação e ainda assim render captação."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>irr_arr</code>: irrigação do dia",
  "<code>irr_suppressed_mask</code>: dias suprimidos, que viram "
  "<code>total_irrigation_days_suppressed</code> no resultado"],
 "Sem volume de irrigação cadastrado, o vetor é zero e a máscara é falsa em todos os dias.",
),
(
 "PROC-04", "Descartar as primeiras águas", "balanco",
 "Todo dia com chuva, dentro do laço diário.",
 ["<code>precip_mm</code> do dia", "<code>discard_mm</code>",
  "<code>discard_mode</code> (1, 2 ou 3)", "<code>discard_days_interval</code>"],
 ["<b>Modo 1</b>: descarta em todo evento de chuva.",
  "<b>Modo 2</b>: descarta apenas no primeiro evento após estiagem, definida como "
  "véspera com menos de 1 mm.",
  "<b>Modo 3</b>: descarta quando passaram <code>discard_days_interval</code> dias "
  "desde o último descarte.",
  "Quando o descarte se aplica: <code>p_eff = p − discard_mm</code> se <code>p > discard_mm</code>, "
  "senão <b>zero</b> — o dia inteiro é descartado, não a diferença.",
  "Quando não se aplica: <code>p_eff = p</code>, a chuva inteira é aproveitável."],
 [("simulation.py", "run_single_simulation")],
 ["<code>p_eff</code>: lâmina efetiva do dia, em mm, que segue <b>só</b> para PROC-05",
  "<code>eff_precip_mm</code> na série diária detalhada, quando ela é guardada"],
 "Lâmina de descarte negativa é rejeitada na porta de validação, antes do laço.",
),
(
 "PROC-05", "Converter lâmina em volume captado", "balanco",
 "Todo dia, depois do descarte.",
 ["<code>p_eff</code> de PROC-04", "<code>area</code> (m²)", "<code>runoff_coeff</code>"],
 ["<code>v_ac = p_eff × area × runoff_coeff</code>, em litros.",
  "É aqui que o arquivo de chuva vira volume, e é o único ponto onde isso acontece.",
  "O coeficiente é adimensional e fica em [0, 1]; fora disso a simulação nem começa."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_ac</code>: volume captado do dia, que segue para PROC-06",
  "<code>harvested_liters</code> na série diária"],
 "Área negativa ou coeficiente fora de [0, 1] levantam <code>ValueError</code> nomeando "
 "o campo, em PROC-11.",
),
(
 "PROC-06", "Armazenar e extravasar", "balanco",
 "Todo dia, depois da captação.",
 ["<code>v_ac</code>", "volume remanescente do dia anterior", "<code>lower_tank_vol</code>"],
 ["<b>Modelo YAS</b>: o extravasamento é calculado <b>antes</b> de retirar a demanda.",
  "<code>disponível = v_lower + v_ac</code>. Se passar da capacidade, o excedente extravasa "
  "e o reservatório fica cheio.",
  "A ordem importa: retirar a demanda antes faria o reservatório aceitar água que "
  "fisicamente já teria extravasado, superestimando o aproveitamento."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_spill_today</code>, somado em <code>avg_spilled_l_day</code>, que vira "
  "critério de extravasamento no multicritério",
  "<code>v_in_tank</code>, o volume disponível para atendimento"],
 "Volume zero é válido e representa o cenário sem sistema; negativo é rejeitado.",
),
(
 "PROC-07", "Atender com reservatório único", "balanco",
 "Todo dia, quando não há reservatório superior.",
 ["<code>v_in_tank</code>", "<code>pluvial_demand_per_day</code> de PROC-02"],
 ["<code>v_c = min(demanda pluvial, volume no reservatório)</code>.",
  "O volume remanescente permanece para o dia seguinte: <code>v_lower = v_in_tank − v_c</code>."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>: volume pluvial consumido no dia"],
 "Nenhuma: o mínimo já trata reservatório vazio e demanda nula.",
),
(
 "PROC-08", "Atender com recalque para caixa superior", "balanco",
 "Todo dia, quando <code>upper_tank_used</code> e o volume superior é positivo.",
 ["<code>v_lower</code>, <code>v_upper</code>", "<code>upper_tank_vol</code>",
  "<code>pumping_threshold</code>, o volume de reserva que não se consome"],
 ["Laço até a demanda ser atendida ou a água acabar.",
  "Primeiro consome da caixa superior o que estiver <b>acima</b> do limiar de acionamento.",
  "Se ainda falta e há água embaixo, aciona a bomba: transfere "
  "<code>min(v_lower, espaço livre em cima)</code>, conta <b>um ciclo</b> e registra a batelada.",
  "Depois do recalque, consome de novo.",
  "O limiar é limitado ao volume da caixa superior na entrada do processo."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>", "<code>v_rec_today</code>, somado em <code>total_pumped_liters</code>",
  "<code>cycles_today</code>, somado em <code>total_pump_cycles</code>",
  "<code>max_pump_batch_liters</code>"],
 "Volume superior negativo é rejeitado na validação. O laço tem saída garantida: "
 "se não há água embaixo nem em cima, interrompe.",
),
(
 "PROC-09", "Repartir o atendimento e completar com potável", "balanco",
 "Todo dia, depois do atendimento.",
 ["<code>v_c</code>", "<code>non_pot_in_day</code>", "<code>irr_day</code>",
  "<code>pot_in_day</code>", "<code>irrigation_potable_backup</code>"],
 ["<b>Prioridade 1</b>, uso interno não potável: <code>c_pluv_in = min(v_c, não potável interna)</code>.",
  "<b>Prioridade 2</b>, irrigação: <code>c_pluv_irr = min(v_c − c_pluv_in, irrigação do dia)</code>.",
  "O potável consumido é a soma de três parcelas: o potável interno, o déficit do não "
  "potável interno e — só se o suprimento de reserva estiver ligado — o déficit da irrigação.",
  "Com o suprimento de reserva desligado, o jardim simplesmente não é regado no dia seco, "
  "e a rede não é acionada."],
 [("simulation.py", "run_single_simulation")],
 ["<code>potable_consumed_liters</code> do dia",
  "<code>avg_pluvial_indoor_consumed_l_day</code> e "
  "<code>avg_pluvial_irrigation_consumed_l_day</code>, que separam o uso interno do externo "
  "para os créditos WEc1 e WEc2 do LEED"],
 "Nenhuma: todas as parcelas são mínimos e máximos com zero.",
),
(
 "PROC-10", "Classificar o atendimento do dia", "balanco",
 "Todo dia, ao fim do atendimento.",
 ["<code>v_c</code>", "<code>pluvial_demand_per_day</code>"],
 ["<b>Pleno</b> quando o consumido iguala a demanda pluvial, com tolerância de 10⁻⁵ L.",
  "<b>Parcial</b> quando consumiu algo, mas menos que a demanda.",
  "<b>Nulo</b> quando não consumiu nada."],
 [("simulation.py", "run_single_simulation")],
 ["<code>pct_days_full_satisfaction</code>, <code>pct_days_partial_satisfaction</code> "
  "e <code>pct_days_null_satisfaction</code>, que são a confiabilidade temporal do sistema"],
 "Nenhuma.",
),
(
 "PROC-11", "Validar a entrada física", "balanco",
 "Primeira linha de <code>run_single_simulation</code>, antes de qualquer conta.",
 ["volume inferior e superior", "área", "coeficiente de escoamento",
  "lâmina de descarte", "demanda diária", "fração pluvial"],
 ["Volume negativo, área negativa, descarte negativo e demanda negativa são recusados.",
  "Coeficiente de escoamento e fração pluvial têm de ficar em [0, 1].",
  "<b>Volume zero continua válido</b>: é a referência «sem sistema» da varredura.",
  "A mensagem nomeia o campo e o valor recebido, em vez de corrigir por baixo dos panos."],
 [("simulation.py", "validar_parametros_fisicos")],
 ["Nenhuma saída: ou passa, ou levanta <code>ValueError</code>"],
 "É o próprio tratamento. Antes desta porta, volume de −1.000 L devolvia −166,67% de "
 "economia, e o número seguia para o econômico, para a ACV e para o relatório.",
),
(
 "PROC-12", "Agregar o período e calcular os indicadores", "balanco",
 "Fim do laço diário.",
 ["acumuladores do laço", "<code>n_days</code>"],
 ["<b>Potencial de economia</b> = pluvial consumido no período ÷ demanda total do período × 100.",
  "As médias diárias dividem os acumulados pelo número de dias simulados.",
  "As conversões para o ano usam <b>365,25</b> dias, e não 365, para absorver os bissextos "
  "da série.",
  "O potencial fica sempre em [0, 100] — invariante que a porta de validação existe para garantir."],
 [("simulation.py", "run_single_simulation")],
 ["<code>SingleTankSimulationResult</code>, com 21 campos, que é o objeto que <b>todos</b> "
  "os módulos a jusante consomem"],
 "Demanda total nula devolve potencial zero em vez de dividir por zero.",
),
(
 "PROC-13", "Varrer volumes e achar o volume ideal", "balanco",
 "Aba Varredura: botão de simular.",
 ["<code>lower_tank_max</code>", "<code>lower_tank_step</code>",
  "<code>delta_ideal_threshold</code> (%/m³)"],
 ["A grade discreta arredonda o passo <b>para cima</b> até o múltiplo de 250 L, que é o "
  "quantum comercial de reservatório, e limita a 40 volumes positivos.",
  "O volume máximo informado é sempre preservado como último ponto, de modo que só o "
  "último intervalo pode ser menor que o passo.",
  "Zero entra na grade como alternativa de referência.",
  "Roda PROC-04 a PROC-12 uma vez por volume.",
  "O <b>volume ideal</b> é o primeiro cujo ganho marginal <code>Δpotencial/Δm³</code> cai "
  "abaixo do limiar: a partir dali, mais reservatório não compensa."],
 [("simulation.py", "build_sweep_volume_grid"), ("simulation.py", "run_sweep_simulation")],
 ["<code>SweepSimulationResult</code>: um resultado por volume, o volume ideal, e o "
  "registro de que o passo foi ajustado",
  "A lista de volumes é a lista de <b>candidatos</b> do multicritério"],
 "Passo maior que o máximo devolve grade com um ponto. O ajuste do passo é registrado "
 "em <code>step_adjusted</code>, e não silenciado.",
),
(
 "PROC-14", "Calcular os índices pluviométricos", "chuva",
 "Aba Gráficos e relatório científico.",
 ["<code>precip_data</code>", "datas da série"],
 ["Nove índices: PRCPTOT, R95p, RX1day, RX5day, SDII, R20mm, CDD, CWD e o índice de "
  "sazonalidade de Walsh e Lawler.",
  "O conjunto <b>não</b> é ETCCDI puro: a sazonalidade não é do conjunto, e o R10mm, que é, "
  "está ausente.",
  "O percentil 95 é calculado sobre a <b>série inteira carregada</b>, e não sobre a base "
  "fixa 1961–1990 do ETCCDI.",
  "O RX5day usa <code>min_periods=1</code>, de modo que as primeiras janelas do ano têm "
  "de 1 a 4 dias."],
 [("calculator.py", "IndicesCalculator"), ("calculator.py", "compute_seasonality_index"),
  ("calculator.py", "find_max_consecutive_run_length")],
 ["Nove séries anuais, para gráfico e relatório"],
 "Série menor que um ano devolve os índices possíveis, sem interromper.",
),
(
 "PROC-15", "Dimensionar a estação de tratamento", "etap",
 "Mudança na aba Qualidade da Água, ou início do econômico e da ACV.",
 ["<code>water_quality_target_class</code> (4 classes de uso)",
  "<code>water_quality_disinfection</code>: cloro, ultravioleta ou ozônio",
  "<code>water_quality_polishing</code>, filtro de polimento",
  "<code>annual_pluvial_m3</code> de PROC-12", "<code>area</code>",
  "dose, pureza, preço e fator de CO₂ do cloro"],
 ["A classe alvo define as etapas obrigatórias; a desinfecção escolhida define o "
  "equipamento e o custeio.",
  "O filtro de polimento é aplicado <b>se e somente se</b> marcado; quando a classe o "
  "recomendaria e o usuário recusa, isso fica registrado em "
  "<code>polishing_recommended_but_declined</code> em vez de ser imposto.",
  "O que se compra é o <b>produto</b> — pastilha a 65% de cloro ativo — e não o cloro puro. "
  "Faturar a massa de cloro ativo, e não a do produto, subestima o custo em cerca de 35%.",
  "<b>Regra incremental</b>: o CAPEX da linha desconta a verba genérica de tratamento já "
  "embutida em «Acessórios», e o custeio desconta a cloração, que o fluxo de caixa já paga. "
  "A regra vive num lugar só, consumida pelos <b>dois</b> motores econômicos.",
  "Na ACV, a linha de tratamento <b>substitui</b> o termo de cloração; nunca soma a ele.",
  "Com <code>etap_enabled = False</code>, a linha de tratamento não entra em conta alguma: "
  "nem no CAPEX, nem no custeio, nem na avaliação ambiental."],
 [("water_quality.py", "size_etap"), ("etap_integration.py", "dimensionar_etap_do_projeto"),
  ("etap_integration.py", "capex_incremental_da_etap"),
  ("etap_integration.py", "opex_anual_incremental_da_etap"),
  ("chlorination.py", "Cloracao")],
 ["<code>total_etap_capex</code>, que entra no CAPEX",
  "<code>total_etap_annual_opex</code>, que entra no custeio",
  "<code>total_etap_co2e_kg_yr</code>, que substitui a cloração na ACV",
  "<code>disinfection_stages</code>, exibido no relatório"],
 "Pureza fora de (0, 1] é recusada pelo validador da cadeia de cloração.",
),
(
 "PROC-16", "Calcular a energia de bombeamento", "bomba",
 "Econômico e ACV, a partir do mesmo resultado de simulação.",
 ["<code>total_pumped_liters</code> e <code>total_pump_cycles</code> de PROC-08",
  "<code>pump_power_kw</code>, <code>pump_efficiency</code>, <code>pump_flow_rate</code>",
  "<code>pump_manometric_head_m</code>", "<code>pump_startup_time_h</code>"],
 ["Energia específica <code>e = ρgH/η</code> por m³ recalcado, ou <code>P/Q</code> quando "
  "a vazão é declarada.",
  "A potência de placa <b>já embute</b> o rendimento; por isso <code>P × horas / η</code> "
  "conta o rendimento duas vezes. Quatro cópias dessa fórmula antiga sobreviviam no "
  "programa e superestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no "
  "multicritério.",
  "A energia de partida entra à parte, pelo número de ciclos.",
  "Vazão e rendimento não informados caem para valores típicos <b>da potência escolhida</b>, "
  "e não para constantes fixas."],
 [("pump_energy.py", "compute_annual_pump_energy"),
  ("pump_hydraulics.py", "energia_especifica_kwh_por_m3"),
  ("pump_hydraulics.py", "vazao_l_por_h"), ("pump_hydraulics.py", "rendimento_tipico")],
 ["<code>annual_kwh</code>, que vira custo no econômico e emissão na ACV",
  "<code>pump_hours_year</code>, <code>annual_cycles</code>"],
 "Sem caixa superior, ou com potência zero, a energia é zero e o processo não roda.",
),
(
 "PROC-17", "Calcular a fatura de água e esgoto", "economico",
 "Duas vezes por mês de projeção: com e sem aproveitamento.",
 ["volume mensal em litros", "<code>water_tariffs</code>: quádruplas "
  "(mínimo, máximo, valor, código)", "<code>sewage_mode</code> e <code>sewage_rate</code>",
  "impostos fixo e variável", "<code>num_economias</code>"],
 ["O consumo é avaliado <b>no patamar de uma economia</b> e multiplicado pelo número de "
  "economias, para não distorcer as faixas progressivas em prédio com micromedição.",
  "Código <b>1</b> ou <b>0</b>: faixa progressiva, cobrada só sobre o volume dentro dela.",
  "Código <b>−1</b>, disponibilidade: valor fixo que <b>soma</b> por cima do consumo medido.",
  "Código <b>−2</b>, franquia retroativa: até o volume da franquia paga-se o valor fixo; "
  "passando dele, <b>todo</b> o volume desde zero é tarifado pelas faixas.",
  "Código <b>−3</b>, piso de pagamento: não soma, <b>limita por baixo</b>. Com piso de R$ 40 "
  "e consumo tarifado de R$ 55, economizar até R$ 15 não reduz nada — e é exatamente isso "
  "que um estudo de aproveitamento pluvial precisa enxergar.",
  "O esgoto é percentual da <b>tarifa de água</b>, não da fatura. Em Florianópolis são 100% "
  "da água, que é metade da fatura.",
  "Os cinco regimes de mínimo estão nomeados e auditados na base dos 652 municípios."],
 [("economic.py", "calculate_water_bill"), ("tariff_regimes.py", "resumo_do_regime"),
  ("tariff_regimes.py", "validar_estrutura"), ("tariffs_structure.py", "CODIGOS_VALIDOS")],
 ["Valor da fatura de água e esgoto em R$/mês, para a projeção de PROC-18"],
 "Tabela vazia cai para a estrutura da CASAN. Estrutura incompleta é sinalizada pela "
 "porta de validação, que separa erro de aviso.",
),
(
 "PROC-18", "Projetar o fluxo de caixa", "economico",
 "Aba Econômico, após a simulação técnica.",
 ["CAPEX das cinco rubricas mais bomba e ETAP",
  "economia mensal de água e esgoto de PROC-17",
  "custeio: bombeamento, cloração, ETAP e custos operacionais declarados",
  "<code>tma</code>, <code>inflation</code>, <code>analysis_period_years</code>",
  "reajustes separados de água, esgoto e energia, e o intervalo entre reajustes",
  "IPTU verde, quando habilitado"],
 ["Água e esgoto são reajustados por índices <b>separados</b>, e não pela fatura agregada.",
  "A inflação incide só sobre o custeio; os reajustes tarifários incidem só sobre a fatura.",
  "O reajuste é aplicado a cada <code>tariff_escalation</code> meses, em degraus.",
  "A bandeira tarifária ajusta a tarifa de energia: amarela, vermelha 1, vermelha 2, ou "
  "desconto fora de ponta na branca.",
  "O IPTU verde entra como economia anual dividida por doze.",
  "O payback é o primeiro mês em que o acumulado descontado cruza zero."],
 [("economic.py", "run_economic_analysis"), ("economic.py", "calculate_effective_tariff")],
 ["<code>vpl</code>, <code>tir_monthly_pct</code>, <code>tir_annual_pct</code>, "
  "<code>payback_months</code>",
  "<code>monthly_cash_flows</code>, série mês a mês",
  "<code>annual_pump_kwh</code>, <code>annual_chlorine_kg</code>, <code>etap_capex_brl</code>"],
 "Economia mensal negativa é truncada em zero antes de entrar no fluxo. TIR sem raiz real "
 "devolve nulo em vez de um número inventado.",
),
(
 "PROC-19", "Avaliar o ciclo de vida", "acv",
 "Aba Ambiental, após a simulação técnica.",
 ["<code>tank_vol_liters</code>", "<code>annual_pluvial_m3</code> de PROC-12",
  "materiais e massas dos dois reservatórios", "comprimentos por diâmetro de tubo",
  "<code>pump_count</code>", "fator da rede elétrica", "rota de produção da água potável",
  "resultado da ETAP de PROC-15"],
 ["Sete etapas: cisterna inferior, caixa superior, tubulação, motobomba, operação de "
  "bombeamento, operação de tratamento e potável evitada.",
  "Volume zero <b>sem</b> volume pluvial é o cenário sem sistema, e não recebe impacto "
  "fixo de caixa, tubo ou bomba.",
  "A linha de tratamento <b>substitui</b> o termo de cloração; não soma a ele.",
  "A água evitada é a <b>entregue</b>, não a produzida: as perdas de distribuição no Brasil "
  "vão de 33,9% no Sudeste a 46,9% no Norte, de modo que produzir 1 m³ entrega de 0,53 a "
  "0,66 m³. O fator publicado de 0,236 kg CO₂e/m³ é de saída de estação; por m³ entregue "
  "vira de 0,336 a 0,461 conforme a macrorregião.",
  "O payback de carbono é o carbono incorporado dividido pela economia anual líquida; "
  "sem economia líquida positiva, devolve 999 anos em vez de infinito."],
 [("environmental.py", "calculate_lca"), ("water_supply_routes.py", "co2_evitado_por_m3"),
  ("grid_emission_factors.py", "fator_co2eq")],
 ["<code>total_embodied_co2_kg</code>, <code>net_annual_avoided_co2_kg</code>",
  "<code>lifetime_net_co2_saved_kg</code>, que é critério do multicritério",
  "<code>environmental_payback_years</code>", "<code>inventory_items</code>, o inventário item a item"],
 "Fator sem procedência primária recebe rótulo de triagem, e o rótulo é exibido — a "
 "lacuna é declarada, não escondida.",
),
(
 "PROC-20", "Enquadrar nas certificações", "esg",
 "Aba Ambiental e relatórios.",
 ["<code>potential_potable_savings_pct</code>", "volume pluvial e potável anuais",
  "repartição interno/externo de PROC-09", "CO₂ evitado no ciclo de vida",
  "<code>area</code>, para a área de captação da WEM14",
  "caso-base do EDGE, quando declarado"],
 ["<b>LEED v4</b>: WEc1 até 2 pontos pelo uso externo, WEc2 até 6 pontos pelo uso interno, "
  "pela escala oficial. Sem demanda externa cadastrada, WEc1 é zero e diz por quê.",
  "<b>AQUA-HQE Residencial</b> (referencial de 22/11/2024): itens EAU.1.2 (HQE, 20% de "
  "economia), EAU.1.3 (HQE 3, 40%) e EAU.1.5 (HQE 3, existência de sistema pluvial).",
  "<b>Casa Azul + CAIXA</b> (guia V023, 29/04/2026): critério 3.6 atendido pela existência "
  "do sistema; 2, 4 ou 5 pontos conforme a abrangência do uso, só quando informada.",
  "<b>EDGE</b>: <b>não pontua</b>. Mede percentual contra um caso-base local e compara com "
  "20%, em três barras independentes. O nível avançado sobe a barra de <i>energia</i> para "
  "40%, e não a de água. O programa avalia só a barra de água, pela medida WEM14, e diz "
  "que as outras duas estão fora do seu alcance.",
  "Sem caso-base declarado, o EDGE usa a demanda modelada e avisa que o número é <b>piso</b>.",
  "<b>GRI 303</b>: captação evitada e taxa de circularidade."],
 [("esg_certifications.py", "calculate_esg_certifications"),
  ("edge_certification.py", "avaliar_agua_edge"),
  ("edge_certification.py", "consumo_base_anual_m3")],
 ["<code>credit_details</code>: a matriz de créditos que alimenta a tabela da tela e os "
  "relatórios", "<code>esg_summary_text</code>", "cartões de LEED, AQUA, Casa Azul, EDGE e GRI"],
 "Demanda total nula devolve zero por cento sem dividir por zero.",
),
(
 "PROC-21", "Ordenar volumes por múltiplos critérios", "mcdm",
 "Aba Otimizador, com a varredura pronta.",
 ["um candidato por volume da varredura, cada um com potencial, extravasamento, VPL, "
  "payback descontado, TIR, CO₂ de ciclo de vida e consumo de potável",
  "pesos dos sete critérios"],
 ["Sete critérios: <b>maximizar</b> potencial, VPL e TIR; <b>minimizar</b> extravasamento, "
  "payback, CO₂ e consumo de potável.",
  "A normalização translada por <code>x − min(x)</code> <b>antes</b> da normalização "
  "vetorial de Hwang e Yoon, para admitir VPL negativo. É variante deliberada, e precisa "
  "ser declarada como variante.",
  "O SMAA-VIKOR sorteia pesos e devolve as probabilidades de cada volume ocupar cada posição.",
  "As condições C1 e C2 de Opricovic não estão implementadas."],
 [("topsis.py", "calculate_topsis_scores"), ("mcdm_methods.py", "run_vikor")],
 ["Ordenação dos volumes, distância ao ideal por critério, volume de compromisso"],
 "Candidato único devolve ordenação trivial. Critério constante entre candidatos não "
 "contribui para a distância.",
),
(
 "PROC-22", "Gravar e reabrir o projeto", "arquivo",
 "Menu de salvar e de abrir.",
 ["<code>NetunoConfig</code> inteiro, 102 campos", "estado da interface", "análise corrente"],
 ["Formato JSON, em seções nomeadas.",
  "A leitura usa valor-padrão campo a campo, de modo que arquivo antigo continua abrindo.",
  "<code>created_at</code> e <code>precip_file</code> descrevem o ato de salvar, e não o "
  "projeto: por isso não voltam.",
  "É a quinta travessia do programa — a que atravessa o <b>tempo</b> em vez dos módulos. "
  "Trinta dos 87 campos de então não sobreviviam ao ciclo, inclusive a escolha inteira "
  "da ETAP, a altura manométrica, os materiais dos reservatórios, a irrigação e o IPTU."],
 [("parser.py", "export_netuno_json"), ("parser.py", "load_netuno_project")],
 ["Arquivo <code>.netuno</code>", "<code>NetunoConfig</code> reconstruída"],
 "Seção ausente no arquivo cai para os padrões da classe. JSON inválido interrompe a "
 "abertura com mensagem.",
),
(
 "PROC-23", "Emitir relatórios e exportações", "relatorio",
 "Aba Relatórios; aba Exportação.",
 ["resultados de PROC-12, PROC-18, PROC-19, PROC-20 e PROC-21", "dados do projeto"],
 ["Três relatórios: executivo, ambiental com ESG, e científico.",
  "Exportação para CAD e BIM a partir do dimensionamento.",
  "Planilhas com a série diária e a varredura."],
 [("report_generator.py", "generate_executive_html_report"),
  ("report_generator.py", "generate_environmental_html_report"),
  ("report_generator.py", "generate_research_html_report"),
  ("report_generator.py", "save_pdf_report")],
 ["HTML, PDF, DXF, IFC e XLSX"],
 "A conversão para PDF tenta o motor do Qt e cai para o gerador alternativo quando ele "
 "não está disponível.",
),
(
 "PROC-24", "Automação para estudos de larga escala", "cli",
 "Interface de automação, que acompanha a distribuição de código-fonte e não o "
 "programa instalado.",
 ["arquivo de projeto", "arquivo de chuva"],
 ["Chama o <b>mesmo</b> núcleo de cálculo da janela, sem tela.",
  "55 dos 103 parâmetros são alcançáveis por ela; os demais só existem na interface, "
  "e o caminho é montar o projeto na janela e variar por automação só o que muda "
  "entre os casos.",
  "Serve a matrizes fatoriais de milhares de casos e à propagação de incerteza por "
  "sorteio, que são o instrumental dos trabalhos publicados pelo grupo."],
 [],
 ["JSON e CSV com os resultados"],
 "Parâmetro fora de faixa é recusado antes de simular, com a mesma porta de validação "
 "da interface.",
),
]

FAMILIAS = {
    "chuva": ("Chuva", "dad"), "demanda": ("Demanda", "ent"),
    "balanco": ("Balanço hídrico", "nuc"), "etap": ("Qualidade e ETAP", "nuc"),
    "bomba": ("Motobomba", "nuc"), "economico": ("Econômico", "sai"),
    "acv": ("ACV", "sai"), "esg": ("ESG e certificações", "sai"),
    "mcdm": ("Multicritério", "sai"), "arquivo": ("Arquivo do projeto", "ent"),
    "relatorio": ("Relatórios", "sai"), "cli": ("Automação", "sai"),
}
