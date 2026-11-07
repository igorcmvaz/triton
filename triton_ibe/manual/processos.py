# -*- coding: utf-8 -*-
"""A matriz de processos do Triton, escrita a partir da leitura do fonte.

Cada processo declara gatilho, entradas, regras, funções envolvidas, saídas e
tratamento de exceção. As funções citadas existem: um verificador ao fim do
ficheiro confere cada nome contra o fonte antes de a página ser montada.
"""

# (id, nome, família, gatilho, [entradas], [regras], [(modulo, funcao)], [saídas], exceção)
PROCESSOS = [
(
 "PROC-01", "Carregar a série de precipitação", "chuva",
 "Separador Projeto: escolher o município na base ibérica (Iberia01), o concelho na E-OBS opcional, ou abrir um ficheiro CSV.",
 ["Município do Iberia01 v1.0 (8 319 municípios da Península e das Baleares, 1971 a 2015; ERA5 nas ilhas), concelho da E-OBS v33.0e opcional (278 concelhos, 1950 a 2025), ou ficheiro CSV diário em milímetros por dia",
  "<code>climate_start_date</code> e <code>climate_end_date</code>, que recortam a série (a normal 1986-2015 do Iberia01 é o recorte inicial)",
  "<code>start_date</code>, data do primeiro dia da série"],
 ["A série vira um vetor <code>numpy</code> de milímetros por dia; o índice do vetor "
  "é o dia, e a data serve só para saber o dia da semana e o mês.",
  "A série de um município é a média diária das células da grelha do Iberia01 (0,1°) com centro dentro do município (CAOP2025 em Portugal, LAU 2023 em Espanha); na E-OBS, a média das células da sua grelha. "
  "As ilhas ficam fora do domínio do Iberia01: Canárias, Madeira e Açores usam a reanálise ERA5 de 0,25° (nível C, com aviso); Ceuta e Melilla ficam sem série, "
  "e nenhum local recebe a série de um vizinho. Para esses, a série é um ficheiro do utilizador.",
  "Dia sem dado em todas as células é uma falha (NaN), e a simulação recusa a série em vez de o tratar como dia seco.",
  "Ano incompleto é descartado na leitura, para não enviesar totais anuais.",
  "As bases vêm no programa, em <code>data/chuva_iberia01_p1.db</code> a <code>p4.db</code>, <code>data/chuva_ilhas_era5.db</code> e <code>data/portugal_eobs.db</code> (opcional); o exemplo do Funchal usa a ERA5 de ilha, e <code>data/rainfall/Funchal.csv</code> é a série de exemplo da edição."],
 [("base_climatica_iberica.py", "carregar_serie"),
  ("base_climatica_portugal.py", "carregar_serie"),
  ("parser.py", "load_precipitation")],
 ["<code>precip_data</code>: vetor de mm/dia, que é a entrada de <b>dois</b> processos "
  "distintos — PROC-04 (descarte e captação) e PROC-03 (suspensão da rega)"],
 "Ficheiro ilegível ou sem coluna de chuva interrompe o carregamento com mensagem; "
 "a simulação não corre com série vazia ou com falhas.",
),
(
 "PROC-02", "Compor a procura diária", "procura",
 "Início da simulação, uma vez por execução.",
 ["<code>demand_mode</code>: constante, semanal, mensal ou diária",
  "<code>demand_value</code> (L/dia por pessoa), <code>residents_count</code>",
  "<code>rainwater_share</code> ou <code>non_potable_indoor_share</code>",
  "vetores <code>weekly_*</code>, <code>monthly_*</code>, <code>daily_*</code> quando o modo os usa"],
 ["Procura-base do dia = <code>demand_value × residents_count</code>, com o multiplicador "
  "do dia da semana, do mês ou do dia, conforme o modo.",
  "A fração não potável separa a procura em duas: interna potável e interna não potável.",
  "Quando o modo é semanal, mensal ou diário, a fração vem do próprio vetor do período; "
  "fora disso, vale <code>non_potable_indoor_share</code>, e só então <code>rainwater_share</code>.",
  "Valor nulo ou zero em qualquer posição do vetor cai para o valor constante."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>tot_arr</code>: procura total do dia",
  "<code>pot_in_arr</code>: potável interna, que a chuva nunca atende",
  "<code>non_pot_in_arr</code>: não potável interna, prioridade 1 da chuva",
  "<code>pluv_arr</code> = não potável interna + rega ativa"],
 "Data inicial ilegível cai para 01/01/1980 em vez de interromper, porque só afeta "
 "o dia da semana.",
),
(
 "PROC-03", "Suprimir a rega nos dias de chuva", "procura",
 "Composição da procura, um teste por dia da série.",
 ["<code>irrigation_liters_per_day</code>",
  "<code>irrigation_rain_threshold_mm</code> (padrão 2 mm/dia)",
  "<code>precip_data</code>, o <b>mesmo</b> vetor que alimenta a captação"],
 ["Se a chuva do dia ≥ limiar, a rega do dia é <b>zero</b> e o dia entra na contagem "
  "de dias suprimidos.",
  "Caso contrário, a rega do dia é o volume nominal.",
  "É a segunda leitura do ficheiro de chuva, e independente da primeira: um dia pode "
  "suprimir a rega e ainda assim render captação."],
 [("simulation.py", "build_detailed_daily_demand_vectors")],
 ["<code>irr_arr</code>: rega do dia",
  "<code>irr_suppressed_mask</code>: dias suprimidos, que viram "
  "<code>total_irrigation_days_suppressed</code> no resultado"],
 "Sem volume de rega registado, o vetor é zero e a máscara é falsa em todos os dias.",
),
(
 "PROC-04", "Descartar as primeiras águas", "balanco",
 "Todo dia com chuva, dentro do ciclo diário.",
 ["<code>precip_mm</code> do dia", "<code>discard_mm</code>",
  "<code>discard_mode</code> (1, 2 ou 3)", "<code>discard_days_interval</code>"],
 ["<b>Modo 1</b>: descarta em todo evento de chuva.",
  "<b>Modo 2</b>: descarta apenas no primeiro evento após período seco, definida como "
  "véspera com menos de 1 mm.",
  "<b>Modo 3</b>: descarta quando passaram <code>discard_days_interval</code> dias "
  "desde o último descarte.",
  "Quando o descarte se aplica: <code>p_eff = p − discard_mm</code> se <code>p > discard_mm</code>, "
  "senão <b>zero</b>: toda a chuva do dia vai para o descarte.",
  "Quando não se aplica: <code>p_eff = p</code>, a chuva inteira é aproveitável."],
 [("simulation.py", "run_single_simulation")],
 ["<code>p_eff</code>: lâmina efetiva do dia, em mm, que segue <b>só</b> para PROC-05",
  "<code>eff_precip_mm</code> na série diária detalhada, quando ela é guardada"],
 "Lâmina de descarte negativa é rejeitada na barreira de validação, antes do ciclo.",
),
(
 "PROC-05", "Converter lâmina em volume captado", "balanco",
 "Todo dia, depois do descarte.",
 ["<code>p_eff</code> de PROC-04", "<code>area</code> (m²)", "<code>runoff_coeff</code>"],
 ["<code>v_ac = p_eff × area × runoff_coeff</code>, em litros.",
  "É aqui que o ficheiro de chuva vira volume, e é o único ponto onde isso acontece.",
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
 ["<b>Extravasamento antes do consumo</b>, como na regra YAS; a chuva do dia, até a "
  "capacidade, já atende a procura do dia, o que põe o modelo entre a YAS e a YBS estritas.",
  "<code>disponível = v_lower + v_ac</code>. Se passar da capacidade, o excedente extravasa "
  "e o reservatório fica cheio.",
  "A ordem importa: retirar a procura antes faria o reservatório aceitar água que "
  "fisicamente já teria extravasado, sobrestimando o aproveitamento."],
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
 ["<code>v_c = min(procura pluvial, volume no reservatório)</code>.",
  "O volume remanescente permanece para o dia seguinte: <code>v_lower = v_in_tank − v_c</code>."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>: volume pluvial consumido no dia"],
 "Nenhuma: o mínimo já trata reservatório vazio e procura nula.",
),
(
 "PROC-08", "Atender com elevação para reservatório superior", "balanco",
 "Todo dia, quando <code>upper_tank_used</code> e o volume superior é positivo.",
 ["<code>v_lower</code>, <code>v_upper</code>", "<code>upper_tank_vol</code>",
  "<code>pumping_threshold</code>, o volume de reserva que não se consome"],
 ["Laço até a procura ser atendida ou a água acabar.",
  "Primeiro consome do reservatório superior o que estiver <b>acima</b> do limiar de acionamento.",
  "Se ainda falta e há água em baixo, aciona a bomba: transfere "
  "<code>min(v_lower, espaço livre em cima)</code>, conta <b>um ciclo</b> e regista a lote.",
  "Depois do elevação, consome de novo.",
  "O limiar é limitado ao volume do reservatório superior na entrada do processo."],
 [("simulation.py", "run_single_simulation")],
 ["<code>v_c</code>", "<code>v_rec_today</code>, somado em <code>total_pumped_liters</code>",
  "<code>cycles_today</code>, somado em <code>total_pump_cycles</code>",
  "<code>max_pump_batch_liters</code>"],
 "Volume superior negativo é rejeitado na validação. O ciclo tem saída garantida: "
 "se não há água em baixo nem em cima, interrompe.",
),
(
 "PROC-09", "Repartir o atendimento e completar com potável", "balanco",
 "Todo dia, depois do atendimento.",
 ["<code>v_c</code>", "<code>non_pot_in_day</code>", "<code>irr_day</code>",
  "<code>pot_in_day</code>", "<code>irrigation_potable_backup</code>"],
 ["<b>Prioridade 1</b>, uso interno não potável: <code>c_pluv_in = min(v_c, não potável interna)</code>.",
  "<b>Prioridade 2</b>, rega: <code>c_pluv_irr = min(v_c − c_pluv_in, rega do dia)</code>.",
  "O potável consumido é a soma de três parcelas: o potável interno, o déficit do não "
  "potável interno e — só se o suprimento de reserva estiver ligado — o déficit da rega.",
  "Com o suprimento de reserva desligado, o jardim simplesmente não é regado no dia seco, "
  "e a rede não é acionada."],
 [("simulation.py", "run_single_simulation")],
 ["<code>potable_consumed_liters</code> do dia",
  "<code>avg_pluvial_indoor_consumed_l_day</code> e "
  "<code>avg_pluvial_irrigation_consumed_l_day</code>, que separam o uso interno do externo "
  "para os créditos WEc1 e WEc2 do LEED v4 e as Opções 2 e 4 do WEc2 do LEED v5"],
 "Nenhuma: todas as parcelas são mínimos e máximos com zero.",
),
(
 "PROC-10", "Classificar o atendimento do dia", "balanco",
 "Todo dia, ao fim do atendimento.",
 ["<code>v_c</code>", "<code>pluvial_demand_per_day</code>"],
 ["<b>Pleno</b> quando o consumido iguala a procura pluvial, com tolerância de 10⁻⁵ L.",
  "<b>Parcial</b> quando consumiu algo, mas menos que a procura.",
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
  "lâmina de descarte", "procura diária", "fração pluvial"],
 ["Volume negativo, área negativa, descarte negativo e procura negativa são recusados.",
  "Coeficiente de escoamento e fração pluvial têm de ficar em [0, 1].",
  "<b>Volume zero continua válido</b>: é a referência «sem sistema» da varrimento.",
  "A mensagem nomeia o campo e o valor recebido, em vez de corrigir por baixo dos panos."],
 [("simulation.py", "validar_parametros_fisicos")],
 ["Nenhuma saída: ou passa, ou levanta <code>ValueError</code>"],
 "É o próprio tratamento. Antes desta porta, volume de −1.000 L devolvia −166,67% de "
 "economia, e o número seguia para o económico, para a ACV e para o relatório.",
),
(
 "PROC-12", "Agregar o período e calcular os indicadores", "balanco",
 "Fim do ciclo diário.",
 ["acumuladores do ciclo", "<code>n_days</code>"],
 ["<b>Potencial de economia</b> = pluvial consumido no período ÷ procura total do período × 100.",
  "As médias diárias dividem os acumulados pelo número de dias simulados.",
  "As conversões para o ano usam <b>365,25</b> dias, e não 365, para absorver os bissextos "
  "da série.",
  "O potencial fica sempre em [0, 100] — invariante que a barreira de validação existe para garantir."],
 [("simulation.py", "run_single_simulation")],
 ["<code>SingleTankSimulationResult</code>, com 21 campos, que é o objeto que <b>todos</b> "
  "os módulos a jusante consomem"],
 "Procura total nula devolve potencial zero em vez de dividir por zero.",
),
(
 "PROC-13", "Varrer volumes e achar o volume ideal", "balanco",
 "Separador Varrimento: botão de simular.",
 ["<code>lower_tank_max</code>", "<code>lower_tank_step</code>",
  "<code>delta_ideal</code> (%/m³)"],
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
  "registo de que o passo foi ajustado",
  "A lista de volumes é a lista de <b>candidatos</b> do multicritério"],
 "Passo maior que o máximo devolve grade com um ponto. O ajuste do passo é registado "
 "em <code>step_adjusted</code>, e não silenciado.",
),
(
 "PROC-14", "Calcular os índices pluviométricos", "chuva",
 "Separador Gráficos e relatório científico.",
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
 "Mudança na separador Qualidade da Água, ou início do económico e da ACV.",
 ["<code>water_quality_target_class</code> (4 classes de uso)",
  "<code>water_quality_disinfection</code>: cloro, ultravioleta ou ozono",
  "<code>water_quality_polishing</code>, filtro de polimento",
  "<code>annual_pluvial_m3</code> de PROC-12", "<code>area</code>",
  "dose, pureza, preço e fator de CO₂ do cloro",
  "<code>discard</code> e <code>first_flush_system_enabled</code>, para o descarte inicial"],
 ["A classe alvo define as etapas obrigatórias; a desinfeção escolhida define o "
  "equipamento e o exploração.",
  "O filtro de polimento é aplicado <b>se e somente se</b> marcado; quando a classe o "
  "recomendaria e o utilizador recusa, isso fica registado em "
  "<code>polishing_recommended_but_declined</code> em vez de ser imposto.",
  "O que se compra é o <b>produto</b> — pastilha a 65% de cloro ativo — e não o cloro puro. "
  "Faturar a massa de cloro ativo, e não a do produto, subestima o custo em cerca de 35%.",
  "<b>Regra incremental</b>: o CAPEX da linha desconta a verba genérica de tratamento já "
  "embutida em «Acessórios», e os custos de exploração descontam a cloragem, que o fluxo de caixa já paga. "
  "A regra vive num lugar só, consumida pelos <b>dois</b> motores económicos.",
  "Com <code>first_flush_system_enabled</code>, o dispositivo de descarte inicial, de volume "
  "<code>discard × area</code>, entra no CAPEX e no exploração da linha.",
  "Na ACV, a linha de tratamento <b>substitui</b> o termo de cloragem; nunca soma a ele.",
  "Com <code>etap_enabled = False</code>, a linha de tratamento não entra em conta alguma: "
  "nem no CAPEX, nem no exploração, nem na avaliação ambiental."],
 [("water_quality.py", "size_etap"), ("etap_integration.py", "dimensionar_etap_do_projeto"),
  ("etap_integration.py", "capex_incremental_da_etap"),
  ("etap_integration.py", "opex_anual_incremental_da_etap"),
  ("chlorination.py", "Cloracao")],
 ["<code>total_etap_capex</code>, que entra no CAPEX",
  "<code>total_etap_annual_opex</code>, que entra no exploração",
  "<code>total_etap_co2e_kg_yr</code>, que substitui a cloragem na ACV",
  "<code>disinfection_stages</code>, exibido no relatório"],
 "Pureza fora de (0, 1] é recusada pelo validador da cadeia de cloragem.",
),
(
 "PROC-16", "Calcular a energia de bombeamento", "bomba",
 "Económico e ACV, a partir do mesmo resultado de simulação.",
 ["<code>supply_arrangement</code>: elevação, pressurização direta ou gravidade",
  "<code>total_pumped_liters</code> e <code>total_pump_cycles</code> de PROC-08",
  "<code>pressurizer_pressure_m</code>, <code>pressurizer_starts_per_person_day</code>, "
  "<code>residents_count</code>",
  "<code>pump_power_kw</code>, <code>pump_efficiency</code>, <code>pump_flow_rate</code>",
  "<code>pump_manometric_head_m</code>", "<code>pump_startup_time_h</code>"],
 ["O arranjo decide o que se bombeia. <b>Elevação</b>: o volume enviado ao reservatório superior. "
  "<b>Pressurização direta</b>: todo o volume pluvial consumido, com a pressão de trabalho no "
  "lugar da altura e sem energia de partida. <b>Gravidade</b>: nada. É a única fonte de kWh "
  "do económico e da ACV.",
  "Energia específica <code>e = ρgH/(η_bomba·η_motor)</code> por m³ elevado, ou "
  "<code>P/(Q·η_motor)</code> quando a caudal é declarada.",
  "A potência de placa é potência de eixo e <b>já embute</b> o rendimento da bomba; por isso "
  "<code>P × horas / η_bomba</code> conta esse rendimento duas vezes, e o que falta é dividir "
  "pelo rendimento do motor. Quatro cópias dessa fórmula antiga sobreviviam no "
  "programa e sobrestimavam o consumo em 1,68 vez — a pior delas ordenava volumes no "
  "multicritério.",
  "A energia de partida entra à parte, pelo número de ciclos.",
  "Caudal e rendimento não informados caem para valores típicos <b>da potência escolhida</b>, "
  "e não para constantes fixas."],
 [("pump_energy.py", "compute_annual_pump_energy"),
  ("pump_hydraulics.py", "energia_especifica_kwh_por_m3"),
  ("pump_hydraulics.py", "vazao_l_por_h"), ("pump_hydraulics.py", "rendimento_tipico")],
 ["<code>annual_kwh</code>, que vira custo no económico e emissão na ACV",
  "<code>pump_hours_year</code>, <code>annual_cycles</code>"],
 "Arranjo por gravidade, arranjo não informado num projeto antigo, ou potência zero: a "
 "energia é zero.",
),
(
 "PROC-17", "Calcular a fatura de água, saneamento e resíduos", "economico",
 "Duas vezes por mês de projeção: com e sem aproveitamento.",
 ["volume mensal em litros", "<code>water_tariffs</code>: quádruplas "
  "(mínimo, máximo, valor, código)", "<code>sewage_mode</code> e <code>sewage_rate</code>",
  "taxas fixa e variável (nelas entram o IVA e as parcelas fixas)", "<code>num_economias</code>, o número de frações autónomas com contador individual"],
 ["O consumo é avaliado <b>no patamar de uma fração</b> e multiplicado pelo número de "
  "frações, para não distorcer os escalões progressivos em prédio com contadores individuais.",
  "Código <b>1</b> ou <b>0</b>: escalão progressivo, cobrado só sobre o volume dentro dele.",
  "Código <b>−1</b>, tarifa de disponibilidade: valor fixo que <b>soma</b> ao consumo medido.",
  "Código <b>−2</b>, franquia retroativa: até ao volume da franquia paga-se o valor fixo; "
  "passando-o, <b>todo</b> o volume desde zero é tarifado pelos escalões.",
  "Código <b>−3</b>, piso de pagamento: não soma, <b>limita por baixo</b>. Com piso de 40 € "
  "e consumo tarifado de 55 €, poupar até 15 € não reduz nada — e é exatamente isso "
  "que um estudo de aproveitamento pluvial precisa de ver.",
  "A fatura portuguesa soma a água (tarifa fixa mensal e escalões por m³), o saneamento, os resíduos urbanos, a taxa de recursos hídricos (TRH) "
  "e o IVA de cada parcela, à taxa que o tarifário declara. Nenhuma taxa de IVA fica no código.",
  "O saneamento pode ser cobrado por escalões próprios sobre o volume recolhido (coeficiente de recolha × volume de água; em Lisboa, 90%), "
  "com a TRH por m³ recolhido, ou como percentagem da <b>parcela de água</b>, e não da fatura total.",
  "As tarifas fixas das parcelas que não são a água entram como taxa fixa mensal. Não variam com o consumo e anulam-se na poupança; "
  "entram para a conta mensal sair igual à impressa.",
  "Os seis regimes tarifários são descritos no apêndice {{n:D}}; os tarifários transcritos (Lisboa, Porto e Funchal) estão nesse mesmo apêndice."],
 [("economic.py", "calculate_water_bill"), ("fatura_portuguesa.py", "conta_mensal"),
  ("fatura_portuguesa.py", "aplicar_ao_projeto"), ("tariff_regimes.py", "resumo_do_regime"),
  ("tariff_regimes.py", "validar_estrutura"), ("tariffs_structure.py", "CODIGOS_VALIDOS")],
 ["Valor da fatura de água, saneamento e resíduos em €/mês, para a projeção de PROC-18"],
 "Tabela vazia dá fatura zero: o programa não presume tarifário. Estrutura incompleta é sinalizada pela "
 "barreira de validação, que separa erro de aviso. Os resíduos por escalões (Funchal) ainda não têm campo próprio: "
 "a parte variável soma-se à do saneamento.",
),
(
 "PROC-18", "Projetar o fluxo de caixa", "economico",
 "Separador Económico, após a simulação técnica.",
 ["CAPEX das cinco rubricas mais bomba e ETAP",
  "poupança mensal de água e saneamento de PROC-17",
  "custos de exploração: bombagem, cloragem, ETAP e custos operacionais declarados",
  "<code>tma</code> (taxa de atualização), <code>inflation</code>, <code>analysis_period_years</code>",
  "atualizações separadas de água, saneamento e energia, e o intervalo entre atualizações"],
 ["Água e saneamento são atualizados por índices <b>separados</b>, e não pela fatura agregada.",
  "A inflação incide só sobre os custos de exploração; as atualizações tarifárias incidem só sobre a fatura.",
  "A atualização é aplicada a cada <code>tariff_escalation</code> meses, em degraus.",
  "O período de recuperação é o primeiro mês em que o acumulado descontado cruza zero."],
 [("economic.py", "run_economic_analysis"), ("economic.py", "calculate_effective_tariff")],
 ["<code>vpl</code> (VAL), <code>tir_monthly_pct</code>, <code>tir_annual_pct</code>, "
  "<code>payback_months</code>",
  "<code>monthly_cash_flows</code>, série mês a mês",
  "<code>annual_pump_kwh</code>, <code>annual_chlorine_kg</code>"],
 "Poupança mensal negativa é truncada em zero antes de entrar no fluxo. TIR sem raiz real "
 "devolve nulo em vez de um número inventado.",
),
(
 "PROC-19", "Avaliar o ciclo de vida", "acv",
 "Separador Ambiental, após a simulação técnica.",
 ["<code>tank_vol_liters</code>", "<code>annual_pluvial_m3</code> de PROC-12",
  "materiais e massas dos dois reservatórios", "comprimentos por diâmetro de tubo",
  "<code>pump_count</code>", "fator da rede elétrica", "fator de emissão da água potável entregue",
  "resultado da ETAP de PROC-15"],
 ["Sete etapas: cisterna inferior, reservatório superior, tubagem, eletrobomba, operação de "
  "bombeamento, operação de tratamento e potável evitada.",
  "Volume zero <b>sem</b> volume pluvial é o cenário sem sistema, e não recebe impacto "
  "fixo de caixa, tubo ou bomba.",
  "A linha de tratamento <b>substitui</b> o termo de cloragem; não soma a ele. A cloragem "
  "acompanha o tratamento, e não o reservatório superior.",
  "Reservatório superior só no arranjo de elevação; eletrobombas em todo arranjo com bomba; energia "
  "de PROC-16.",
  "A água evitada é a <b>entregue</b>, não a produzida: as perdas de distribuição fazem com "
  "que produzir 1 m³ entregue menos de 1 m³, e um fator dado à saída da estação tem de ser "
  "convertido para o volume entregue. O utilizador indica o fator de emissão da água entregue "
  "ao edifício e o da rede elétrica local; a edição não traz valor predefinido para nenhum dos dois.",
  "O período de retorno do carbono é o carbono incorporado dividido pela economia anual líquida; "
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
 "Separador Ambiental e relatórios.",
 ["<code>potential_potable_savings_pct</code>", "volume pluvial e potável anuais",
  "repartição interno/externo de PROC-09", "CO₂ evitado no ciclo de vida",
  "<code>area</code>, para a área de captação da WEM14",
  "caso-base do EDGE, quando declarado"],
 ["<b>LEED v4</b>: WEc1 até 2 pontos pelo uso externo, WEc2 até 6 pontos pelo uso interno, "
  "pela escala oficial. Sem procura externa registada, WEc1 é zero e diz porquê.",
  "<b>LEED v5 BD+C</b> (rating system de novembro de 2025): WEc2 até 8 pontos, pela Opção 1 "
  "(projeto inteiro, 30% a 65%, +1 com fonte alternativa) ou pela soma das Opções 2 (louças e "
  "metais, 30% a 40%), 4 (externo, 50% e 100%) e 6 (reutilização no lote, 2 pontos), só em construção "
  "nova. SSc3 registado como não avaliado; o ponto de reutilização dele não ultrapassa o teto de 3.",
  "<b>EDGE</b>: <b>não pontua</b>. Mede percentual contra um caso-base local e compara com "
  "20%, em três barras independentes. O nível avançado sobe a barra de <i>energia</i> para "
  "40%, e não a de água. O programa avalia só a barra de água, pela medida WEM14, e diz "
  "que as outras duas estão fora do seu alcance.",
  "Sem caso-base declarado, o EDGE usa a procura modelada e avisa que o número é <b>piso</b>.",
  "<b>GRI 303</b>: captação evitada e taxa de circularidade."],
 [("esg_certifications.py", "calculate_esg_certifications"),
  ("edge_certification.py", "avaliar_agua_edge"),
  ("edge_certification.py", "consumo_base_anual_m3")],
 ["<code>credit_details</code>: a matriz de créditos que alimenta a tabela do ecrã e os "
  "relatórios", "<code>esg_summary_text</code>", "cartões de LEED, EDGE e GRI"],
 "Procura total nula devolve zero por cento sem dividir por zero.",
),
(
 "PROC-21", "Ordenar volumes por múltiplos critérios", "mcdm",
 "Separador Otimizador, com a varrimento pronta.",
 ["um candidato por volume da varrimento, cada um com potencial, extravasamento, VAL, "
  "período de recuperação descontado, TIR, CO₂ de ciclo de vida e consumo de potável",
  "pesos dos sete critérios"],
 ["Sete critérios: <b>maximizar</b> potencial, VAL e TIR; <b>minimizar</b> extravasamento, "
  "período de recuperação, CO₂ e consumo de potável.",
  "A normalização translada por <code>x − min(x)</code> <b>antes</b> da normalização "
  "vetorial de Hwang e Yoon, para admitir VAL negativo. É variante deliberada, e precisa "
  "ser declarada como variante.",
  "O SMAA-VIKOR sorteia pesos e devolve as probabilidades de cada volume ocupar cada posição.",
  "As condições C1 e C2 de Opricovic não estão implementadas."],
 [("topsis.py", "calculate_topsis_scores"), ("mcdm_methods.py", "run_vikor")],
 ["Ordenação dos volumes, distância ao ideal por critério, volume de compromisso"],
 "Candidato único devolve ordenação trivial. Critério constante entre candidatos não "
 "contribui para a distância.",
),
(
 "PROC-22", "Gravar e reabrir o projeto", "ficheiro",
 "Menu de guardar e de abrir.",
 ["<code>TritonConfig</code> inteiro, com os campos do apêndice {{n:A}}", "estado da interface", "análise corrente"],
 ["Formato JSON, em secções nomeadas.",
  "A leitura usa valor por defeito campo a campo, de modo que ficheiro antigo continua abrindo.",
  "<code>created_at</code> e <code>precip_file</code> descrevem o ato de guardar, e não o "
  "projeto: por isso não voltam.",
  "É a quinta travessia do programa — a que atravessa o <b>tempo</b> em vez dos módulos. "
  "Trinta dos 87 campos de então não sobreviviam ao ciclo, inclusive a escolha inteira "
  "da ETAP, a altura manométrica, os materiais dos reservatórios, a rega e a água de rega."],
 [("parser.py", "export_triton_json"), ("parser.py", "load_triton_project")],
 ["Ficheiro <code>.triton</code>", "<code>TritonConfig</code> reconstruída"],
 "Secção ausente no ficheiro cai para os valores por defeito da classe. JSON inválido interrompe a "
 "abertura com mensagem.",
),
(
 "PROC-23", "Emitir relatórios e exportações", "relatorio",
 "Separador Relatórios; separador Exportação.",
 ["resultados de PROC-12, PROC-18, PROC-19, PROC-20 e PROC-21", "dados do projeto"],
 ["Três relatórios: executivo, ambiental com ESG, e científico.",
  "Exportação para CAD e BIM a partir do dimensionamento.",
  "Folhas de cálculo com a série diária e a varrimento."],
 [("report_generator.py", "generate_executive_html_report"),
  ("report_generator.py", "generate_environmental_html_report"),
  ("report_generator.py", "generate_research_html_report"),
  ("report_generator.py", "save_pdf_report")],
 ["HTML, PDF, DXF, JSON para BIM e XLSX"],
 "A conversão para PDF tenta o motor do Qt e cai para o gerador alternativo quando ele "
 "não está disponível.",
),
(
 "PROC-24", "Automação para estudos de larga escala", "cli",
 "Linha de comandos <code>triton</code>, descrita na secção {{n:19}}; acompanha a instalação "
 "como pacote Python, e não o instalador de Windows.",
 ["ficheiro de projeto", "ficheiro de chuva"],
 ["Chama o <b>mesmo</b> núcleo de cálculo da janela, sem ecrã.",
  "Só parte dos parâmetros é alcançável por ela; os demais só existem na interface, "
  "e o caminho é montar o projeto na janela e variar por automação só o que muda "
  "entre os casos.",
  "Serve a matrizes fatoriais de milhares de casos e à propagação de incerteza por "
  "sorteio, que são o instrumental dos trabalhos publicados pelo grupo."],
 [],
 ["JSON e CSV com os resultados"],
 "Parâmetro fora do intervalo admitido é recusado antes de simular, com a mesma barreira de validação "
 "da interface.",
),
]

FAMILIAS = {
    "chuva": ("Chuva", "dad"), "procura": ("Procura", "ent"),
    "balanco": ("Balanço hídrico", "nuc"), "etap": ("Qualidade e ETAP", "nuc"),
    "bomba": ("Eletrobomba", "nuc"), "economico": ("Económico", "sai"),
    "acv": ("ACV", "sai"), "esg": ("ESG e certificações", "sai"),
    "mcdm": ("Multicritério", "sai"), "ficheiro": ("Ficheiro do projeto", "ent"),
    "relatorio": ("Relatórios", "sai"), "cli": ("Automação", "sai"),
}
