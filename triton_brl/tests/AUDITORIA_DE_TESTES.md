# Auditoria dos testes do Triton — aplicada em 06/10/2026

Base auditada: 1222 funções de teste (`tests/unit`, `invariants`, `ui`, `integration`, `benchmarking`).
Casos parametrizados contam como uma função. Ponto de volta: commit `4ae06fd`, ramo
`modulacao-probabilistica-e-auditoria-de-testes`.

| Decisão | Funções | O que aconteceu |
| :--- | ---: | :--- |
| **Núcleo** | 670 | levados, com o corpo intacto, para `tests/test_essencial.py` (525, sem interface) e `tests/test_essencial_interface.py` (145, com Qt) |
| Guarda de dado com procedência | 167 | ficaram onde estavam (o `CLAUDE.md` os cita pelo nome) |
| Guarda de manual e documentação | 207 | ficaram onde estavam; testam texto, não o programa |
| Guarda de distribuição | 44 | ficaram onde estavam; testam o pacote e o instalador |
| Validação contra o Netuno 4 | 7 | ficaram onde estavam; afirmação central do estudo de replicação |
| **Descarte** | 127 | apagados |

**Por que dois arquivos, e não um.** A integração contínua (`.github/workflows/verificacao.yml`)
roda sem PySide6 e exige 80% de cobertura de `triton.core`. Um arquivo único que importasse a
interface seria inteiro ignorado ali, e a cobertura cairia abaixo do piso. O núcleo numérico fica em
`test_essencial.py`, que roda sem Qt; o que exige a interface, em `test_essencial_interface.py`,
ignorado sem Qt como era a pasta `tests/ui`.

**Como se conferiu que nada se perdeu.** Os testes foram levados pela árvore sintática, e não
reescritos à mão: o corpo de cada um é o original; mudam só o caminho de `__file__` (passa a ser o do
arquivo de origem) e o prefixo de nomes de módulo que colidiam entre arquivos. Um verificador
confere que cada um dos 670 está na suíte nova antes de apagar a origem. Resultados na seção
«Comparação das duas versões», no fim.

**Reclassificados depois da proposta.** `integration/test_report_generator.py`:
`test_generate_executive_html_report` e `test_generate_research_html_report` ficaram como guarda
de documentação, porque a guarda `test_relatorio_nao_traz_valor_indefinido`
(`unit/test_o_que_se_comunica.py`) os executa para capturar os dados do relatório.

**Restaurados depois da medição de cobertura.** Vinte testes que a proposta descartava voltaram
ao núcleo, porque eram a única cobertura de código real: a medição sem Qt mostrou `mcdm_methods`
caindo de 96% para 74% (VIKOR e a análise SMAA só tinham os testes «felizes»), `plant_3d` de 99%
para 34%, o gerador do painel de tarifas de 81% para 10%, e quedas menores em `schematic_3d`,
`environmental_sync`, `water_quality` e `simulation`; o balanço de três dias feito à mão era o único
que exercitava `triton/core/test_framework.py`. Estão marcados abaixo como «restaurado».

## Descartados, com o motivo

| Arquivo | Teste | Motivo |
| :--- | :--- | :--- |
| `integration/test_financial_robustness.py` | `test_csv_presets_execution` | caminho feliz fraco: presets dentro de faixas amplas |
| `integration/test_financial_robustness.py` | `test_invariant_payback_discounted_gte_simple` | duplicado: = economic_properties E6 |
| `integration/test_financial_robustness.py` | `test_massive_parametric_financial_calculations` | caminho feliz fraco: 1.000 combinações só conferindo finitude; as propriedades E1–E16 cobrem com asserção forte |
| `integration/test_financial_robustness.py` | `test_massive_sensitivity_analysis_stability` | caminho feliz fraco: estabilidade genérica, sem invariante |
| `integration/test_fluidez_de_informacoes.py` | `test_a_altura_do_assistente_atravessa_ate_a_emissao` | duplicado: = propagacao::test_a_altura_manometrica_do_assistente_rege_a_emissao_de_bombeamento |
| `integration/test_fluidez_de_informacoes.py` | `test_a_dose_digitada_atravessa_ate_a_massa_anual` | duplicado: = propagacao::test_a_dose_de_cloro_digitada_rege_a_massa_anual |
| `integration/test_fluidez_de_informacoes.py` | `test_a_precipitacao_carregada_chega_ao_calculo_de_wash_off` | duplicado: = propagacao_de_entradas::test_a_serie_de_chuva_chega_a_aba_de_qualidade |
| `integration/test_fluidez_de_informacoes.py` | `test_escolher_ultravioleta_atravessa_ate_o_economico_e_a_acv` | duplicado: = propagacao::test_a_desinfeccao_escolhida_encarece_e_emite |
| `integration/test_fluidez_de_informacoes.py` | `test_o_filtro_de_polimento_atravessa_a_partir_da_caixa_de_selecao` | duplicado: = propagacao::test_o_filtro_de_polimento_move_investimento_e_manutencao |
| `integration/test_fluidez_de_informacoes.py` | `test_o_volume_simulado_chega_ao_dimensionamento_da_etap` | duplicado: = propagacao_de_entradas e etap_integration |
| `integration/test_new_tools.py` | `test_pump_catalog_structure` | duplicado: = pump_wizard::test_commercial_pump_catalog_consistency |
| `integration/test_new_tools.py` | `test_pump_wizard_calculations` | duplicado: = pump_wizard::test_forchheimer_calculation |
| `integration/test_report_generator.py` | `test_save_pdf_report` | caminho feliz fraco: gera PDF sem conferir conteúdo |
| `invariants/test_declared_dependencies.py` | `test_dependencias_essenciais_estao_presentes` | trivial: confere o próprio ambiente de teste |
| `invariants/test_economic_properties.py` | `test_reprodutibilidade_exata` | trivial: aritmética pura é determinística; o determinismo que importa é o do motor (P4) |
| `invariants/test_environmental_properties.py` | `test_reprodutibilidade_exata` | trivial: idem |
| `invariants/test_financial_invariants.py` | `test_default_materials_pead` | trivial: confere um valor padrão |
| `invariants/test_financial_invariants.py` | `test_financial_invariants_payback_never_negative` | duplicado: = economic_properties E7 |
| `invariants/test_mass_conservation.py` | `test_zero_rainfall_zero_pluvial_consumption_invariant` | duplicado: = scientific_properties P9 |
| `invariants/test_numba_python_parity.py` | `test_estado_do_kernel_esta_documentado` | sem asserção de comportamento: só registra qual kernel está ativo |
| `ui/test_documentation_tab.py` | `test_documentation_tab_creation_and_content` | caminho feliz fraco: procura strings na aba |
| `ui/test_documentation_tab.py` | `test_main_window_has_documentation_tab` | cosmético de tela: conta abas; quebra a cada aba nova (quebrou hoje) |
| `ui/test_mcdm_method_selector.py` | `test_vikor_chart_ylim_multiple_of_20_superior_to_max` | cosmético de tela: limite de eixo |
| `ui/test_modulacao_estocastica_ui.py` | `test_e_a_ultima_ferramenta_da_barra_lateral` | cosmético de tela: posição na barra |
| `ui/test_modulacao_estocastica_ui.py` | `test_exporta_csv_e_json` | caminho feliz fraco: arquivos gravados |
| `ui/test_modulacao_estocastica_ui.py` | `test_sem_rolagem_lateral_em_janela_estreita` | cosmético de tela: layout |
| `ui/test_pipe_runs_dialog.py` | `test_organizacao_com_pendencias_abre_no_editor` | cosmético de tela: qual painel abre |
| `ui/test_pipe_runs_dialog.py` | `test_organizacao_valida_abre_na_volumetria_com_o_editor_recolhido` | cosmético de tela: qual painel abre |
| `ui/test_pipe_runs_dialog.py` | `test_origin_text_distinguishes_continuation_coordinates_and_references` | cosmético de tela: texto de rótulo |
| `ui/test_tab_building_templates.py` | `test_tab_building_templates_population` | cosmético de tela: lista preenchida |
| `ui/test_tarifa_exponencial_ui.py` | `test_a_formula_nao_espreme_os_graficos` | cosmético de tela: layout |
| `ui/test_tarifa_exponencial_ui.py` | `test_o_botao_exportar_tudo_grava_a_planilha` | caminho feliz fraco: arquivo gravado |
| `ui/test_volumetry_view.py` | `test_empty_scene_shows_placeholder` | cosmético de tela: texto de cena vazia |
| `ui/test_volumetry_view.py` | `test_keyboard_switches_views_and_clears_selection` | cosmético de tela: atalhos de teclado |
| `ui/test_volumetry_view.py` | `test_view_renders_every_preset_and_fits_the_scene` | cosmético de tela: câmera e enquadramento |
| `unit/test_auditoria_do_motor.py` | `test_serie_totalmente_seca` | duplicado: = P9 |
| `unit/test_auditoria_do_motor.py` | `test_serie_valida_passa` | trivial: sem asserção; a validação positiva é exercida por todos os outros |
| `unit/test_calculator.py` | `test_compute_seasonality_index` | caminho feliz fraco: valor pontual |
| `unit/test_calculator.py` | `test_indices_calculator_real_file` | caminho feliz fraco: arquivo real, faixas amplas |
| `unit/test_calculator.py` | `test_indices_calculator_synthetic` | caminho feliz fraco: série sintética, valores pontuais |
| `unit/test_certificacao_edge.py` | `test_a_matriz_diz_que_o_edge_nao_pontua` | caminho feliz fraco: presença na matriz |
| `unit/test_certificacao_edge.py` | `test_a_sintese_executiva_menciona_o_edge` | caminho feliz fraco: presença no texto |
| `unit/test_certificacao_edge.py` | `test_o_edge_chega_ao_relatorio_consolidado` | caminho feliz fraco: presença no relatório |
| `unit/test_change_detector.py` | `test_compute_sha256` | duplicado: = change_detector_offline::test_hash_e_estavel_e_sensivel |
| `unit/test_climate_database.py` | `test_models_and_scenarios_definitions` | trivial: contagem de constantes |
| `unit/test_comprimento_de_serie_ui.py` | `test_a_aba_abre_a_janela_com_o_resultado` | cosmético de tela: janela abre |
| `unit/test_comprimento_de_serie_ui.py` | `test_a_janela_mostra_o_veredito_e_uma_linha_por_comprimento` | cosmético de tela: linhas da tabela |
| `unit/test_date_picker.py` | `test_calendar_popup_instantiation` | cosmético de tela: só instancia |
| `unit/test_date_picker.py` | `test_date_picker_default` | cosmético de tela: widget genérico |
| `unit/test_date_picker.py` | `test_date_picker_manual_typing` | cosmético de tela: widget genérico |
| `unit/test_date_picker.py` | `test_date_picker_set_date_variants` | cosmético de tela: widget genérico |
| `unit/test_date_picker.py` | `test_date_picker_signals` | cosmético de tela: widget genérico |
| `unit/test_demand_modulation.py` | `test_build_daily_demand_vectors_constant` | duplicado: modulação semanal/mensal em casos_analiticos; diária na paridade CLI |
| `unit/test_demand_modulation.py` | `test_build_daily_demand_vectors_daily` | duplicado: modulação semanal/mensal em casos_analiticos; diária na paridade CLI |
| `unit/test_demand_modulation.py` | `test_build_daily_demand_vectors_monthly` | duplicado: modulação semanal/mensal em casos_analiticos; diária na paridade CLI |
| `unit/test_demand_modulation.py` | `test_build_daily_demand_vectors_weekly` | duplicado: modulação semanal/mensal em casos_analiticos; diária na paridade CLI |
| `unit/test_demand_modulation.py` | `test_simulation_with_modulated_demand` | duplicado: modulação semanal/mensal em casos_analiticos; diária na paridade CLI |
| `unit/test_discard_modes.py` | `test_discard_mode_1_all_events` | duplicado: os três modos de descarte estão em casos_analiticos com solução fechada |
| `unit/test_discard_modes.py` | `test_discard_mode_2_after_dry_spell` | duplicado: os três modos de descarte estão em casos_analiticos com solução fechada |
| `unit/test_discard_modes.py` | `test_discard_mode_3_every_x_days` | duplicado: os três modos de descarte estão em casos_analiticos com solução fechada |
| `unit/test_economic.py` | `test_economic_unfavorable_scenario_negative_vpl` | duplicado: = E8 |
| `unit/test_economic.py` | `test_economic_vpl_and_payback_favorable` | caminho feliz fraco: propriedades E1–E16 cobrem o sentido; o valor absoluto não é invariante |
| `unit/test_economic.py` | `test_material_cost_multipliers_and_tank_pricing` | duplicado: = precos_de_reservatorio |
| `unit/test_economic.py` | `test_preliminary_capex_and_maintenance_follow_system_configuration` | caminho feliz fraco: orçamento preliminar sem invariante |
| `unit/test_economic.py` | `test_pump_operational_electricity_costs` | duplicado: = pump_hydraulics / energia_de_partida |
| `unit/test_environmental.py` | `test_calculate_lca_basic` | caminho feliz fraco: propriedades A1–A13 cobrem |
| `unit/test_environmental.py` | `test_environmental_sweep` | duplicado: = A13 |
| `unit/test_environmental.py` | `test_fator_do_cloro_deixou_de_ser_o_custo` | duplicado: = chlorination::test_o_fator_do_cloro_nunca_volta_a_ser_o_preco |
| `unit/test_environmental.py` | `test_materials_comparison` | duplicado: = A2 |
| `unit/test_environmental.py` | `test_tab_environmental_charts_dynamic_sizing` | cosmético de tela: tamanho de gráfico |
| `unit/test_environmental_params_ui.py` | `test_a_base_padrao_existe_e_e_nomeada` | trivial: existência de chave |
| `unit/test_environmental_params_ui.py` | `test_o_dialogo_abre_em_tela_cheia` | cosmético de tela: geometria da janela |
| `unit/test_environmental_report.py` | `test_generate_environmental_html_report_en` | caminho feliz fraco: procura strings no HTML |
| `unit/test_environmental_report.py` | `test_generate_environmental_html_report_pt` | caminho feliz fraco: procura strings no HTML |
| `unit/test_environmental_report.py` | `test_tab_reports_pdf_integration` | caminho feliz fraco: aba gera sem estourar |
| `unit/test_esg_certifications.py` | `test_calculate_esg_certifications` | caminho feliz fraco: caminho feliz; limiares têm testes próprios |
| `unit/test_esg_certifications.py` | `test_environmental_tab_opens_with_environmental_optimum` | cosmético de tela: aba abre |
| `unit/test_esg_certifications.py` | `test_esg_simplified_mode` | caminho feliz fraco: caminho feliz |
| `unit/test_esg_certifications.py` | `test_leed_v5_aparece_na_matriz_de_criterios` | caminho feliz fraco: presença na matriz |
| `unit/test_export_tab_and_exporters.py` | `test_csv_simulation_export` | caminho feliz fraco: exportação feliz |
| `unit/test_export_tab_and_exporters.py` | `test_excel_simulation_export_full_and_custom` | caminho feliz fraco: exportação feliz |
| `unit/test_export_tab_and_exporters.py` | `test_tab_export_ui_interactions` | cosmético de tela: caixas de marcar da aba |
| `unit/test_exportar_tudo.py` | `test_as_seis_abas_de_dados_vem_junto` | caminho feliz fraco: contagem de abas |
| `unit/test_exportar_tudo.py` | `test_o_arranjo_3d_sai_com_o_quantitativo` | caminho feliz fraco: presença de aba |
| `unit/test_fechamento_do_balanco.py` | `test_o_reservatorio_nao_cria_nem_perde_agua` | duplicado: = P8 e auditoria::test_massa_fecha_dia_a_dia |
| `unit/test_filtro_de_polimento.py` | `test_o_padrao_da_configuracao_e_nao_usar_polimento` | trivial: valor padrão; test_a_caixa_comeca_desmarcada cobre o que o usuário vê |
| `unit/test_grid_emission_factors.py` | `test_ano_padrao_existe_na_serie` | trivial: existência de chave |
| `unit/test_icones.py` | `test_existe_ao_menos_um_icone_da_lista` | trivial: os outros testes de ícone já falham sem ícone |
| `unit/test_impostos_e_bomba_reserva.py` | `test_a_tela_de_energia_tem_campo_para_os_dois_impostos_da_energia` | cosmético de tela: existência de campo |
| `unit/test_impostos_e_bomba_reserva.py` | `test_a_tela_de_tarifas_tem_campo_para_os_dois_impostos_da_agua` | cosmético de tela: existência de campo |
| `unit/test_modulacao_estocastica.py` | `test_nome_antigo_do_subcomando_continua_aceito` | trivial: alias de nome |
| `unit/test_triton_updates.py` | `test_a_cloracao_acompanha_o_tratamento_e_nao_a_caixa_superior` | duplicado: mesma regra do invariante A8 |
| `unit/test_triton_updates.py` | `test_upper_tank_chlorination_uniform_in_environmental_sweep` | duplicado: = A8 e A13 |
| `unit/test_triton_updates.py` | `test_version_is_1_0_0` | trivial: constante; test_versao_declarada_e_coerente já cobre |
| `unit/test_pump_energy_details.py` | `test_pump_energy_exact_physics_formula` | duplicado: = pump_hydraulics::test_energia_especifica_e_rho_g_h_sobre_eta |
| `unit/test_pump_energy_details.py` | `test_pump_power_conversions` | trivial: constante cv↔kW |
| `unit/test_pump_energy_details.py` | `test_pump_tab_tanks_simulation_dashboard_widgets` | cosmético de tela: rótulos de KPI |
| `unit/test_pump_wizard_chain.py` | `test_a_configuracao_nasce_sem_altura_informada` | trivial: valor padrão |
| `unit/test_report_service.py` | `test_report_aliases_are_shared` | trivial: aliases de nome |
| `unit/test_simulation.py` | `test_suggested_sweep_residential_sizing` | caminho feliz fraco: sugestão de grade, sem invariante |
| `unit/test_simulation.py` | `test_zero_rain_simulation` | duplicado: = P9 |
| `unit/test_study_layout.py` | `test_a_prancha_do_arranjo_completo_nao_embola` | cosmético de tela: diagramação da prancha |
| `unit/test_study_layout.py` | `test_as_valvulas_seguem_a_direcao_do_trecho` | cosmético de tela: rotação de bloco |
| `unit/test_study_layout.py` | `test_generate_study_layout_with_defaults` | caminho feliz fraco: caminho feliz com padrões |
| `unit/test_study_layout.py` | `test_o_comando_aparece_como_cabos_do_quadro_e_logica_na_ficha` | cosmético de tela: representação do comando |
| `unit/test_tab_building_ui.py` | `test_tab_building_cell_changes_no_exceptions` | caminho feliz fraco: 'não estoura' sem asserção de efeito |
| `unit/test_tab_building_ui.py` | `test_tab_building_instantiation` | cosmético de tela: só instancia |
| `unit/test_tab_building_ui.py` | `test_tab_building_mode_switching` | cosmético de tela: visibilidade de campos |
| `unit/test_tab_project_ui.py` | `test_descarte_vazio_fica_amarelo_pedindo_a_lamina` | cosmético de tela: cor do campo |
| `unit/test_tab_project_ui.py` | `test_tab_project_defaults` | trivial: valores padrão de widgets |
| `unit/test_tab_project_ui.py` | `test_tab_project_discard_fill` | cosmético de tela: preenchimento de campo |
| `unit/test_tariffs_database.py` | `test_dialog_electricity_ui` | cosmético de tela: inicialização do diálogo |
| `unit/test_tariffs_database.py` | `test_dialog_tariffs_ui` | cosmético de tela: inicialização do diálogo |
| `unit/test_tariffs_manager_tab.py` | `test_all_categories_present` | trivial: contagem de chaves |
| `unit/test_tariffs_manager_tab.py` | `test_americana_tab_tariffs_manager_billing` | duplicado: = transcricoes::test_cobranca_direta_reproduz_cada_m3_inteiro |
| `unit/test_tariffs_manager_tab.py` | `test_slider_movement_preserves_chart_dimensions` | cosmético de tela: dimensão de gráfico |
| `unit/test_tariffs_manager_tab.py` | `test_tab_tariffs_manager_widget` | cosmético de tela: só instancia a aba |
| `unit/test_topsis.py` | `test_topsis_proximity_chart_renders_seven_criterion_series` | cosmético de tela: desenho do gráfico |
| `unit/test_traducao_completa.py` | `test_a_varredura_acha_as_chamadas` | trivial: testa a ferramenta do teste |
| `unit/test_verificacoes_da_revisao.py` | `test_calculate_lca_without_upper_tank_keeps_chlorination` | duplicado: mesma regra do invariante A8 (environmental_properties) |
| `unit/test_verificacoes_da_revisao.py` | `test_monthly_precision_payback_discounted` | duplicado: idêntico em unit/test_triton_updates.py |
| `unit/test_verificacoes_da_revisao.py` | `test_monthly_precision_payback_simple` | duplicado: idêntico em unit/test_triton_updates.py |
| `unit/test_verificacoes_da_revisao.py` | `test_upper_tank_chlorination_uniform_in_environmental_sweep` | duplicado: idêntico em unit/test_triton_updates.py |
| `unit/test_volumetry.py` | `test_feature_edges_skip_cylinder_generatrices` | cosmético de tela: arestas de desenho |
| `unit/test_volumetry.py` | `test_package_writes_both_files_next_to_the_drawing` | trivial: arquivos gravados |
| `unit/test_volumetry.py` | `test_visual_thickness_never_makes_close_pipes_look_merged` | cosmético de tela: espessura visual |
| `unit/test_water_supply_routes.py` | `test_rota_padrao_existe` | trivial: existência de chave |

## Núcleo: o que ficou, e o risco que cada arquivo de origem cobria

### `unit/test_modulacao_estocastica.py` — 32

Risco: invariantes do Monte Carlo, paridade CLI, recusa de entradas.

`test_cada_distribuicao_devolve_a_media_e_o_desvio_pedidos`, `test_truncagem_respeita_os_limites`, `test_distribuicao_invalida_e_recusada`, `test_pessoas_sempre_inteiro_e_ao_menos_um`, `test_mesma_semente_mesmas_amostras`, `test_amostra_aplicada_recalcula_a_fracao_total`, `test_series_recebem_o_fator_e_mantem_o_perfil`, `test_sem_variar_nada_o_p50_e_o_estudo`, `test_painel_tem_faixas_ordenadas_e_frequencias_que_somam_100`, `test_otimo_economico_e_o_menor_payback_e_nao_o_maior_vpl`, `test_cancelar_devolve_o_que_ja_foi_feito`, `test_spearman`, `test_linha_de_comando_da_o_mesmo_resultado_que_o_nucleo`, `test_linha_de_comando_aceita_distribuicao_por_opcao`, `test_catalogo_padrao_liga_so_as_tres_de_consumo`, `test_formato_da_primeira_versao_ainda_abre`, `test_cada_variavel_move_o_resultado_no_sentido_esperado`, `test_fator_da_chuva_multiplica_a_serie`, `test_wilson`, `test_variavel_desconhecida_e_recusada`, `test_variaveis_de_custo_movem_o_vpl_no_sentido_esperado`, `test_fator_da_cisterna_pesa_menos_que_o_do_investimento_inteiro`, `test_periodo_de_analise_e_inteiro_e_ao_menos_um`, `test_fator_do_esgoto_vale_em_todos_os_modos`, `test_fatores_de_emissao_movem_o_saldo_de_carbono`, `test_sorteio_de_modelos_nao_muda_os_demais_sorteios`, `test_modelo_desconhecido_ou_repetido_e_recusado`, `test_modelos_pedem_a_base_climbra`, `test_cada_realizacao_usa_a_serie_do_modelo_sorteado`, `test_razao_de_correlacao`, `test_linha_de_comando_sorteia_os_modelos_como_o_nucleo`, `test_linha_de_comando_recusa_modelos_com_arquivo_proprio`

### `unit/test_etap_integration.py` — 20

Risco: invariante: cloro contado uma vez; ETAP desligada reproduz o antigo.

`test_o_volume_pluvial_vem_da_simulacao_e_nao_de_um_valor_fixo`, `test_sem_simulacao_o_volume_cai_no_valor_de_recurso`, `test_a_etap_acompanha_o_volume_do_projeto`, `test_escolher_ultravioleta_muda_a_emissao_da_acv`, `test_o_polimento_tambem_chega_a_acv`, `test_o_cloro_e_contado_uma_vez_na_acv`, `test_a_parcela_extra_isola_o_que_nao_e_cloro`, `test_desligar_a_etap_devolve_o_resultado_anterior`, `test_o_campo_legado_de_intensidade_continua_mandando`, `test_o_inventario_nomeia_os_estagios_de_desinfeccao`, `test_a_etap_entra_no_investimento`, `test_escolher_ultravioleta_encarece_o_investimento_e_o_custeio`, `test_o_cloro_e_pago_uma_vez_no_economico`, `test_o_capex_da_etap_desloca_a_verba_generica_de_acessorios`, `test_desligar_a_etap_zera_as_duas_parcelas_no_economico`, `test_a_dose_e_a_pureza_do_projeto_chegam_ao_dimensionamento`, `test_o_preco_do_cloro_e_o_mesmo_nos_dois_modulos`, `test_a_dose_relatada_vale_para_qualquer_metodo`, `test_descarte_primeiras_aguas_soma_no_capex_da_etap_e_economico`, `test_descarte_primeiras_aguas_soma_no_inventario_da_acv`

### `unit/test_quantitativo_do_arranjo.py` — 20

Risco: invariante: nada do arranjo sem custo ou carbono.

`test_todo_tipo_de_peca_tem_onde_ser_contado`, `test_nada_do_arranjo_fica_sem_custo_ou_sem_carbono`, `test_a_conferencia_aponta_a_peca_esquecida`, `test_o_capex_le_a_tubulacao_e_os_acessorios_do_arranjo`, `test_a_acv_le_a_tubulacao_e_soma_as_pecas_do_arranjo`, `test_o_valor_digitado_pelo_projetista_prevalece`, `test_a_etap_nao_desconta_verba_que_o_arranjo_nao_tem`, `test_o_arranjo_organizado_viaja_com_o_projeto`, `test_o_arquivo_antigo_mantem_os_custos_que_declara`, `test_o_arranjo_usual_acompanha_o_volume_do_projeto`, `test_o_capex_e_o_desenho_levantam_o_mesmo_arranjo`, `test_a_reserva_e_desenhada_em_paralelo_com_as_suas_pecas`, `test_sem_caixa_o_backup_potavel_desce_na_propria_cisterna`, `test_pressurizacao_leva_o_recalque_direto_ao_ponto`, `test_gravidade_nao_tem_bomba_e_a_cisterna_fica_acima_do_ponto`, `test_o_arranjo_usual_segue_o_abastecimento_e_as_bombas_do_projeto`, `test_a_mao_de_obra_automatica_acompanha_os_materiais`, `test_a_mao_de_obra_digitada_prevalece`, `test_o_capex_do_motor_usa_a_mao_de_obra_automatica`, `test_a_escolha_da_mao_de_obra_viaja_com_o_projeto`

### `integration/test_propagacao_de_entradas.py` — 19

Risco: falha real: entrada da tela que não chega ao cálculo; NaN não atravessa.

`test_a_serie_de_chuva_chega_a_aba_de_qualidade`, `test_a_area_de_captacao_dimensiona_o_filtro_de_entrada`, `test_a_tipologia_chega_a_configuracao_e_ao_aviso`, `test_o_volume_pluvial_simulado_rege_o_dimensionamento_da_etap`, `test_a_desinfeccao_escolhida_encarece_e_emite`, `test_o_filtro_de_polimento_move_investimento_e_manutencao`, `test_a_dose_de_cloro_digitada_rege_a_massa_anual`, `test_a_altura_manometrica_do_assistente_rege_a_emissao_de_bombeamento`, `test_o_investimento_informado_muda_o_retorno`, `test_a_estrutura_tarifaria_rege_a_economia_de_agua`, `test_o_percentual_de_esgoto_rege_a_economia_total`, `test_a_rota_de_agua_rege_a_emissao_evitada`, `test_o_fator_da_rede_rege_a_emissao_de_bombeamento`, `test_o_material_do_reservatorio_rege_o_carbono_incorporado`, `test_dobrar_o_aproveitamento_move_todos_os_modulos`, `test_nenhum_modulo_devolve_valor_nao_finito`, `test_a_linha_de_comando_honra_a_escolha_de_desinfeccao`, `test_a_linha_de_comando_usa_o_consumo_especifico_corrigido`, `test_a_sobreposicao_legada_vale_so_para_quem_a_declara`

### `unit/test_certificacao_edge.py` — 19

Risco: limite: fronteira inclusiva de 20%; divisão por zero.

`test_o_limiar_das_tres_barras_e_vinte_por_cento`, `test_o_nivel_avancado_pede_quarenta_por_cento_de_energia`, `test_a_fronteira_dos_vinte_por_cento_e_inclusiva`, `test_a_margem_diz_quanto_sobra_ou_falta`, `test_sem_caso_base_declarado_usa_a_demanda_do_projeto_e_avisa`, `test_caso_base_declarado_maior_reduz_o_percentual`, `test_o_caso_base_converte_de_litros_por_pessoa_dia`, `test_caso_base_zero_ou_negativo_nao_e_aceito_como_declarado`, `test_demanda_nula_nao_divide_por_zero`, `test_o_percentual_nunca_passa_de_cem`, `test_a_wem14_e_a_medida_que_este_programa_dimensiona`, `test_as_medidas_fora_do_escopo_estao_declaradas_como_tal`, `test_a_area_de_captacao_atravessa_ate_a_matriz`, `test_mais_chuva_aproveitada_move_a_barra_de_agua`, `test_o_edge_e_independente_da_pontuacao_leed`, `test_o_caso_base_e_um_campo_do_projeto_e_volta_ao_reabrir`, `test_o_campo_da_tela_chega_ao_calculo`, `test_valor_ilegivel_no_campo_nao_derruba_a_tela`, `test_o_caso_base_percorre_os_dois_sentidos`

### `unit/test_regimes_tarifarios.py` — 18

Risco: invariante: economizar nunca aumenta a conta; regimes de mínimo.

`test_franquia_no_minimo_nao_da_economia_abaixo_do_minimo`, `test_disponibilidade_converte_toda_economia_em_desconto`, `test_a_diferenca_entre_franquia_e_disponibilidade_e_a_economia_do_primeiro_bloco`, `test_piso_de_pagamento_limita_por_baixo_sem_somar_por_cima`, `test_o_piso_zera_a_economia_ate_alcanca_lo`, `test_sem_minimo_toda_economia_vira_desconto`, `test_o_regime_e_lido_da_forma_da_tabela`, `test_a_franquia_lida_e_o_volume_de_tarifa_nula`, `test_o_resumo_diz_ao_projetista_o_que_ele_precisa_saber`, `test_a_tabela_truncada_e_erro`, `test_o_minimo_diluido_em_tarifa_e_erro`, `test_o_minimo_declarado_e_nao_cobrado_e_erro`, `test_a_lacuna_entre_faixas_e_erro`, `test_a_tarifa_nao_progressiva_e_aviso_e_nao_erro`, `test_uma_estrutura_correta_nao_gera_erro`, `test_toda_conta_cresce_com_o_consumo`, `test_economizar_nunca_aumenta_a_conta`, `test_o_minimo_usual_brasileiro_e_referencia_e_nao_regra`

### `unit/test_pipe_network.py` — 17

Risco: invariante geométrico: colisões e encadeamento.

`test_parse_route_accepts_axes_aliases_and_free_deltas`, `test_runs_are_resolved_in_sequence_from_the_previous_end`, `test_reordering_changes_the_plant_and_is_reported`, `test_declared_destination_is_checked_not_completed`, `test_dependent_run_is_not_resolved_when_its_origin_failed`, `test_gravity_systems_warn_about_rising_or_flat_segments`, `test_plant_3d_refuses_invalid_or_empty_organisation`, `test_bim_layout_round_trips_through_triton_file`, `test_overlapping_pipes_under_the_tank_are_a_clash`, `test_crossing_and_parallel_close_pipes_are_clashes_but_touching_is_not`, `test_joints_tees_and_continuations_are_not_clashes`, `test_connection_ports_follow_the_component_envelope`, `test_plant_3d_dxf_has_axes_tubes_components_and_manifest` (restaurado: única cobertura do código), `test_schematic_3d_lists_sequence_and_writes_real_measures` (restaurado: única cobertura do código), `test_schematic_axis_keeps_order_and_connections_but_compresses_long_runs` (restaurado: única cobertura do código), `test_schematic_marks_gravity_slope_and_numbers_warnings` (restaurado: única cobertura do código), `test_schematic_keeps_close_parallel_pipes_apart_and_breaks_the_back_one` (restaurado: única cobertura do código)

### `invariants/test_economic_properties.py` — 15

Risco: invariante: sentido de VPL/TIR/payback com tarifa, investimento, desconto.

`test_vpl_cresce_com_a_tarifa_de_agua`, `test_vpl_decresce_com_o_investimento_inicial`, `test_vpl_decresce_com_a_taxa_de_desconto`, `test_vpl_cresce_com_o_volume_de_agua_economizada`, `test_vpl_decresce_com_o_custo_de_operacao`, `test_payback_descontado_nunca_precede_o_simples`, `test_paybacks_nunca_sao_negativos`, `test_sem_economia_de_agua_o_projeto_nao_se_paga`, `test_vpl_e_linear_no_escalonamento_do_projeto`, `test_horizonte_maior_nao_reduz_o_vpl_de_projeto_rentavel`, `test_tir_e_coerente_com_o_sinal_do_vpl`, `test_entradas_negativas_sao_rejeitadas`, `test_horizonte_invalido_e_rejeitado`, `test_indicadores_simples_acompanham_o_investimento`, `test_indicadores_simples_e_robusto_concordam_no_sinal_do_vpl`

### `unit/test_auditoria_do_motor.py` — 15

Risco: modo de falha: série com falha/NaN/vazia/sentinela recusada com mensagem.

`test_massa_fecha_dia_a_dia_e_no_periodo`, `test_evento_extremo_unico_extravasa_so_o_excedente`, `test_descarte_consome_o_dia_inteiro_quando_a_chuva_nao_passa_da_lamina`, `test_leitor_pula_cabecalho_em_vez_de_devolver_serie_vazia`, `test_leitor_preserva_falha_como_nan_e_nao_como_dia_seco`, `test_leitor_para_no_bloco_de_configuracao_do_netuno4`, `test_motor_recusa_falha_de_registro`, `test_motor_recusa_sentinela_negativo`, `test_motor_recusa_serie_vazia_com_mensagem_e_nao_divisao_por_zero`, `test_varredura_tambem_valida_a_serie`, `test_parametro_nao_finito_e_recusado`, `test_volume_nao_finito_e_recusado`, `test_modo_de_descarte_desconhecido_e_recusado`, `test_modo_3_exige_intervalo_positivo`, `test_varredura_preserva_irrigacao_e_suprimento_de_reserva`

### `unit/test_filtro_de_polimento.py` — 15

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_a_classe_padrao_nem_sequer_recomenda_polimento`, `test_sem_polimento_o_dimensionamento_nao_cobra_filtro`, `test_desmarcar_surte_efeito_em_todas_as_classes`, `test_a_recusa_da_recomendacao_fica_registrada`, `test_a_classe_1_nunca_marca_recusa`, `test_a_classe_4_leva_carvao_ativado_e_as_demais_areia`, `test_o_polimento_move_o_investimento_incremental`, `test_o_polimento_move_o_custeio_incremental`, `test_a_regra_incremental_tem_uma_definicao_so`, `test_desligar_a_etap_zera_o_incremental`, `test_a_verba_ja_prevista_em_acessorios_e_descontada_uma_vez_so`, `test_a_caixa_comeca_desmarcada`, `test_trocar_de_classe_recomenda_mas_nao_marca_a_caixa`, `test_o_investimento_e_a_manutencao_exibidos_acompanham_a_caixa`, `test_o_payback_exibido_piora_com_o_filtro`

### `unit/test_precos_de_reservatorio.py` — 15

Risco: invariante: preço nunca cai com o volume; extrapolação.

`test_o_preco_nunca_cai_quando_o_volume_sobe`, `test_a_curva_interpolada_e_monotonica_em_toda_a_faixa_de_uso`, `test_volume_nulo_nao_custa_nada`, `test_nos_pontos_tabelados_a_estimativa_devolve_o_preco_tabelado`, `test_entre_dois_pontos_a_estimativa_fica_entre_os_dois_precos`, `test_o_material_multiplica_o_preco_de_referencia`, `test_a_regressao_descreve_bem_a_tabela`, `test_a_extrapolacao_segue_a_regressao_e_nao_os_dois_ultimos_pontos`, `test_a_extrapolacao_nunca_fica_abaixo_do_ultimo_preco_tabelado`, `test_ajuste_ruim_cai_no_metodo_local`, `test_a_regressao_de_tabela_curta_nao_estoura`, `test_a_regressao_acompanha_o_material`, `test_a_regressao_da_caixa_superior_usa_a_tabela_da_caixa_superior`, `test_a_tabela_de_recurso_espelha_o_banco`, `test_a_tabela_de_recurso_tambem_e_monotonica`

### `unit/test_capex_calibrado.py` — 14

Risco: invariante: parcelas somam o total; limites de UF e volume.

`test_o_orcamento_traz_todas_as_parcelas_declaradas`, `test_as_parcelas_somam_o_capex_base`, `test_os_acessorios_somam_os_quatro_subsistemas`, `test_o_fator_regional_multiplica_a_base`, `test_o_capex_cresce_com_o_porte_da_tipologia`, `test_o_opex_fixo_cresce_com_o_porte`, `test_toda_tipologia_do_banco_e_orcavel`, `test_o_capex_cresce_com_o_volume`, `test_os_fatores_regionais_cobrem_as_27_unidades_da_federacao`, `test_roraima_custa_mais_que_sao_paulo`, `test_uf_desconhecida_cai_no_fator_neutro`, `test_a_api_legada_continua_respondendo`, `test_a_api_legada_aceita_tipologia_e_uf`, `test_volume_nulo_nao_produz_capex_negativo`

### `unit/test_tarifa_exponencial.py` — 14

Risco: invariante de cobrança exponencial (CORSAN) e limites de faixa.

`test_o_expoente_e_lido_pelo_consumo_do_mes_inteiro`, `test_a_conta_e_pb_vezes_c_elevado_a_n_mais_o_servico_basico`, `test_o_expoente_vale_para_o_volume_todo_e_nao_so_para_o_ultimo_m3`, `test_acima_do_teto_o_excedente_e_cobrado_pelo_preco_do_m3`, `test_o_esgoto_e_percentual_da_agua_inteira`, `test_a_economia_e_a_diferenca_entre_as_duas_potencias`, `test_micromedicao_aplica_a_formula_por_economia`, `test_a_estrutura_e_lida_e_validada_como_exponencial`, `test_a_validacao_aponta_a_tabela_exponencial_defeituosa`, `test_cada_consumo_le_o_expoente_da_sua_linha`, `test_o_esgoto_e_cobrado_por_m3_consumido`, `test_categoria_sem_tabela_da_corsan_nao_e_derivada_da_residencial`, `test_parcela_exponencial_sem_preco_base_e_zero`, `test_entre_dois_inteiros_a_conta_e_a_reta_que_os_une`

### `invariants/test_environmental_properties.py` — 13

Risco: invariante: emissões não negativas, saldo fecha com as parcelas.

`test_emissoes_nunca_sao_negativas`, `test_co2_incorporado_cresce_com_o_volume_da_cisterna`, `test_co2_evitado_cresce_com_a_agua_aproveitada`, `test_emissao_de_bombeamento_cresce_com_o_consumo_eletrico`, `test_comprimento_de_tubulacao_nao_reduz_o_carbono_incorporado`, `test_saldo_liquido_e_a_diferenca_entre_evitado_e_operacional`, `test_inventario_detalhado_soma_o_carbono_incorporado`, `test_inventario_detalhado_reconstitui_o_saldo_operacional`, `test_a_cloracao_nao_depende_do_reservatorio_superior`, `test_payback_ambiental_nao_e_negativo`, `test_viabilidade_ambiental_concorda_com_o_saldo_acumulado`, `test_varredura_preserva_a_monotonicidade_do_carbono_incorporado`, `test_varredura_concorda_com_o_calculo_individual`

### `invariants/test_scientific_properties.py` — 13

Risco: invariante: monotonias físicas, limites [0,100], conservação de massa, saturação.

`test_economia_monotona_nao_decrescente_no_volume`, `test_economia_dentro_dos_limites_fisicos`, `test_volume_zero_nao_aproveita_agua`, `test_saturacao_em_teto_finito`, `test_reprodutibilidade_exata`, `test_economia_nao_decrescente_na_area_de_captacao`, `test_descarte_de_primeira_chuva_nao_aumenta_economia`, `test_extravasamento_nao_crescente_no_volume`, `test_balanco_de_massa_fecha_em_grade_de_parametros`, `test_serie_sem_chuva_nao_produz_aproveitamento`, `test_descarte_subtrai_a_lamina_e_nao_atua_como_limiar`, `test_chuva_abaixo_do_descarte_nao_e_captada`, `test_modos_de_descarte_diferem_apenas_na_frequencia`

### `unit/test_arranjo_de_abastecimento.py` — 13

Risco: invariante: sem bomba não há energia; econômico e ACV na mesma energia.

`test_sem_bomba_nao_ha_energia_em_modulo_algum`, `test_economico_e_acv_usam_a_mesma_energia`, `test_pressurizacao_bombeia_todo_o_volume_pluvial`, `test_a_pressao_so_pesa_quando_a_curva_limita_a_vazao`, `test_o_modelo_maior_gasta_mais_quando_o_ponto_limita_a_vazao`, `test_o_retardo_eletronico_soma_tempo_a_cada_partida`, `test_personalizado_usa_os_dados_digitados`, `test_o_menor_modelo_que_atende`, `test_gravidade_nao_compra_nem_fabrica_motobomba`, `test_cloracao_entra_na_acv_em_qualquer_arranjo`, `test_so_o_recalque_tem_caixa_superior_no_carbono`, `test_arquivo_antigo_sem_caixa_abre_como_nao_informado`, `test_arranjo_sobrevive_a_gravar_e_reabrir`

### `unit/test_esg_certifications.py` — 12

Risco: limite: limiares LEED/AQUA/Casa Azul; demanda externa zero.

`test_esg_explicit_indoor_outdoor`, `test_esg_zero_outdoor_demand`, `test_esg_zero_outdoor_demand_simplified_mode`, `test_certificacoes_usam_so_a_economia_total`, `test_aqua_segue_os_itens_do_referencial_de_2024`, `test_casa_azul_pontua_pela_abrangencia_e_nao_pelo_percentual`, `test_wec1_segue_os_limiares_do_leed`, `test_irrigacao_atendida_sai_do_resultado_do_balanco`, `test_leed_v5_soma_as_opcoes_2_a_6`, `test_leed_v5_opcao_2_faixas`, `test_leed_v5_opcao_1_com_fonte_alternativa`, `test_leed_v5_sem_sistema_nao_pontua_a_opcao_6`

### `unit/test_excel_scenarios.py` — 12

Risco: limite: série ausente, grade vazia, exportação vazia.

`test_modelo_gerado_pelo_programa_e_legivel_pelo_programa`, `test_modelo_gerado_pelo_programa_roda_com_as_series_distribuidas`, `test_serie_ausente_e_erro_claro_e_nunca_troca_silenciosa`, `test_leitura_aceita_planilha_em_memoria`, `test_leitura_de_csv_com_separador_detectado`, `test_leitura_usa_nome_padrao_quando_a_coluna_falta`, `test_grade_fatorial_tem_o_produto_cartesiano_completo`, `test_grade_fatorial_gera_nomes_unicos`, `test_grade_fatorial_preserva_os_valores_de_entrada`, `test_grade_fatorial_vazia_quando_uma_dimensao_e_vazia`, `test_exportacao_produz_planilha_legivel`, `test_exportacao_de_lista_vazia_nao_quebra`

### `invariants/test_user_input_robustness.py` — 11

Risco: limite: zero, enorme, passo > máximo, texto caótico.

`test_parser_chaotic_strings`, `test_sweep_step_larger_than_max`, `test_sweep_with_zero_maximum`, `test_sweep_with_fractional_non_multiple_max`, `test_simulation_with_zero_demand_and_residents`, `test_simulation_with_zero_area_or_runoff`, `test_inverted_potable_and_non_potable_shares`, `test_huge_demand_and_huge_area_resilience`, `test_economic_hyper_discount_rate_and_zero_inflation`, `test_economic_zero_investment_and_zero_savings`, `test_environmental_zero_volume_and_zero_chlorine`

### `unit/test_change_detector_offline.py` — 11

Risco: modo de falha: registro corrompido, HTTP com erro, arquivo gigante.

`test_hash_e_estavel_e_sensivel`, `test_registro_ausente_produz_estrutura_inicial`, `test_registro_sobrevive_a_ida_e_volta`, `test_registro_corrompido_nao_derruba_o_detector`, `test_url_invalida_e_sinalizada_sem_requisicao`, `test_primeira_verificacao_registra_a_assinatura_inicial`, `test_conteudo_identico_nao_dispara_alarme`, `test_conteudo_alterado_exige_acao_manual`, `test_erro_http_e_sinalizado_para_acao_manual`, `test_cabecalhos_de_validacao_sao_preservados`, `test_documento_gigante_e_truncado_no_limite`

### `unit/test_chlorination.py` — 11

Risco: limite: pureza/dose fora da faixa; cadeia única do cloro.

`test_a_pureza_converte_cloro_ativo_em_produto`, `test_emissao_e_massa_de_produto_vezes_fator`, `test_valores_anuais_escalam_com_o_volume`, `test_pureza_fora_da_faixa_falha_com_mensagem_util`, `test_dose_negativa_falha`, `test_dose_padrao_dentro_da_faixa_normativa`, `test_fator_plausivel_para_hipoclorito`, `test_o_fator_do_cloro_nunca_volta_a_ser_o_preco`, `test_os_tres_modulos_partem_da_mesma_cadeia`, `test_cloracao_e_sempre_aplicada_na_linha_de_tratamento`, `test_barreiras_adicionais_somam_custo_e_emissao`

### `unit/test_pump_hydraulics.py` — 11

Risco: invariante físico ρgH/η; rendimento fora da faixa recusado.

`test_energia_especifica_e_rho_g_h_sobre_eta`, `test_energia_especifica_nao_depende_da_potencia`, `test_a_vazao_acompanha_a_potencia`, `test_a_vazao_cai_quando_a_altura_sobe`, `test_rendimento_cresce_com_o_porte`, `test_rendimento_fora_da_faixa_falha_com_mensagem_util`, `test_energia_pela_vazao_nao_divide_por_eta_de_novo`, `test_as_duas_formas_coincidem_no_ponto_de_operacao`, `test_altura_padrao_e_de_casa_e_nao_de_predio`, `test_consumo_de_recurso_e_plausivel_para_recalque_residencial`, `test_o_exportador_cad_usa_a_mesma_vazao`

### `unit/test_topsis.py` — 11

Risco: invariante: direção custo/benefício; 0 L nunca é ótimo; payback decide.

`test_topsis_uses_all_seven_requested_criteria`, `test_topsis_cost_and_benefit_directions_are_correct`, `test_three_axis_weights_are_distributed_without_changing_axis_totals`, `test_seven_explicit_weights_are_supported`, `test_no_discounted_payback_is_worse_than_any_observed_return`, `test_topsis_single_candidate_and_identical_candidates_are_stable`, `test_topsis_empty_and_invalid_inputs`, `test_topsis_translation_is_invariant_to_column_origin`, `test_optima_indices_follow_potential_vpl_and_minimum_lifecycle_co2`, `test_financial_best_prefers_shorter_payback_over_higher_vpl`, `test_zero_liter_is_never_financial_or_technical_optimum`

### `unit/test_demanda_estocastica.py` — 10

Risco: limite e reprodutibilidade do sorteio diário.

`test_o_sorteio_devolve_a_media_e_o_cv_pedidos`, `test_a_probabilidade_de_ausencia_zera_a_fracao_pedida_dos_dias`, `test_o_piso_e_o_teto_limitam_o_sorteio`, `test_perfil_implausivel_e_recusado`, `test_sem_variacao_o_sorteio_devolve_o_deterministico`, `test_a_mesma_semente_devolve_o_mesmo_resultado`, `test_o_ruido_diario_se_cancela_e_a_incerteza_do_nivel_nao`, `test_com_chuva_sobrando_o_nivel_da_demanda_quase_nao_muda_o_potencial`, `test_a_media_sorteada_respeita_a_incerteza_declarada`, `test_o_volume_ideal_sai_da_grade_e_varia_com_a_incerteza`

### `unit/test_economic.py` — 10

Risco: cobrança por faixas e paridade das duas cadeias econômicas.

`test_water_bill_multi_tier_calculation`, `test_sewage_fixed_and_water_taxes`, `test_additional_operational_costs`, `test_separate_tariff_escalations_and_pump_metrics`, `test_robust_sensitivity_rate_normalization`, `test_step5_and_step7_exact_parity`, `test_operational_cost_annualization_preserves_netuno4_throughput_basis`, `test_effective_tariff_uses_actual_total_demand_when_available`, `test_capex_dialog_opens_recalculated_for_every_sweep_volume`, `test_iptu_green_year_over_year_cashflow_and_savings`

### `unit/test_simulation.py` — 10

Risco: limite: limiar e lote de recalque; grade da varredura.

`test_higher_pump_threshold_increases_starts_and_reduces_batch_size`, `test_pump_threshold_is_bounded_and_internal_transfer_is_mass_conservative`, `test_pump_batch_is_limited_by_each_configured_upper_tank_volume`, `test_sweep_optimal_volume_determination`, `test_sweep_grid_allows_40_positive_volumes_plus_zero_reference`, `test_sweep_grid_doubles_step_above_40_and_keeps_exact_maximum`, `test_sweep_grid_rounds_step_up_to_250_l_multiple_before_doubling`, `test_monthly_potable_use_tracks_each_days_variable_demand`, `test_extreme_rain_simulation` (restaurado: única cobertura do código), `test_dual_tank_pumping` (restaurado: única cobertura do código)

### `unit/test_tres_fracoes.py` — 10

Risco: invariante: frações coerentes; não contar a externa duas vezes.

`test_total_derivada_da_interna_e_da_externa`, `test_total_impossivel_e_recusada`, `test_arquivo_antigo_com_padroes_vazados_vale_a_total`, `test_arquivo_coerente_com_demanda_externa_e_preservado`, `test_alterar_a_total_recalcula_a_interna`, `test_alterar_a_interna_recalcula_a_total`, `test_alterar_as_duas_em_desacordo_e_erro`, `test_config_montada_no_codigo_vale_a_total`, `test_motor_aplica_a_interna_a_demanda_interna_em_todos_os_modos`, `test_projetos_distribuidos_sao_coerentes`

### `invariants/test_casos_analiticos.py` — 9

Risco: invariante: o motor reproduz soluções fechadas (oferta limitada, enchimento, descarte, modulação).

`test_regime_limitado_pela_oferta_tem_solucao_fechada`, `test_enchimento_e_extravasamento_tem_solucao_fechada`, `test_descarte_subtrai_lamina_em_proporcao_exata`, `test_descarte_periodico_atinge_apenas_os_dias_previstos`, `test_descarte_apos_estiagem_atinge_apenas_o_primeiro_evento`, `test_modulacao_semanal_reproduz_o_total_do_padrao`, `test_modulacao_mensal_respeita_a_duracao_de_cada_mes`, `test_irrigacao_e_suprimida_exatamente_nos_dias_de_chuva`, `test_reservatorio_superior_amplo_nao_altera_o_consumo`

### `ui/test_edicoes.py` — 9

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_o_rotulo_identifica_a_edicao`, `test_projeto_novo_da_internacional_nao_traz_precos_brasileiros`, `test_janela_da_internacional`, `test_janela_da_brasil_continua_como_era`, `test_relatorios_e_prancha_trazem_a_edicao`, `test_instalador_por_edicao`, `test_moeda_gravada_pelo_codigo_e_lida_tambem_pelo_indice_antigo`, `test_brasil_mostra_so_o_real`, `test_modulacao_da_internacional_fala_em_euro`

### `ui/test_modulacao_estocastica_ui.py` — 9

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_valores_de_triagem_centrados_no_projeto`, `test_roda_e_da_o_mesmo_que_o_nucleo_com_o_estudo_da_tela`, `test_projeto_gravado_e_reaberto_mantem_as_distribuicoes`, `test_marcar_variavel_mostra_o_cartao_e_entra_no_sorteio`, `test_modelos_climaticos_ficam_inativos_com_arquivo_proprio`, `test_modelos_marcados_entram_no_sorteio_e_na_tabela_4`, `test_trocar_para_a_climbra_na_etapa_1_libera_os_modelos`, `test_abrir_projeto_sem_modulacao_gravada_recentra_os_cartoes`, `test_cartao_nao_editado_acompanha_a_etapa_2_e_o_editado_fica`

### `unit/test_persistencia_do_projeto.py` — 9

Risco: falha real: parâmetro perdido ao salvar/reabrir muda o estudo.

`test_o_ciclo_cobre_praticamente_toda_a_configuracao`, `test_todo_parametro_sobrevive_a_salvar_e_reabrir`, `test_a_linha_de_tratamento_sobrevive`, `test_a_tipologia_e_os_materiais_sobrevivem`, `test_a_altura_manometrica_do_assistente_sobrevive`, `test_a_irrigacao_sobrevive`, `test_os_tributos_e_as_fracoes_sobrevivem`, `test_um_arquivo_sem_as_secoes_novas_continua_legivel`, `test_o_estudo_reaberto_produz_o_mesmo_resultado`

### `unit/test_scenarios_matrix.py` — 9

Risco: invariante do lote: um cenário por combinação, nada vazio.

`test_matriz_executa_o_produto_cartesiano`, `test_cada_cenario_produz_resultado`, `test_parametros_do_cenario_sao_preservados`, `test_area_maior_nao_reduz_a_economia`, `test_callback_de_progresso_e_chamado_uma_vez_por_cenario`, `test_exportacao_gera_arquivo_com_uma_linha_por_cenario`, `test_cabecalho_exportado_coincide_com_a_planilha_real_do_netuno4`, `test_exportacao_usa_virgula_decimal`, `test_planilha_exportada_e_relida_pelo_comparador_de_replicacao`

### `unit/test_validacao_fisica.py` — 9

Risco: limite: parâmetro impossível recusado, extremos válidos aceitos.

`test_parametro_impossivel_e_rejeitado`, `test_volume_negativo_e_rejeitado`, `test_a_mensagem_diz_o_campo_e_o_valor`, `test_volume_zero_continua_valido`, `test_a_faixa_valida_do_coeficiente_passa_inteira`, `test_sem_reservatorio_superior_continua_valido`, `test_demanda_zero_continua_valida`, `test_o_potencial_fica_sempre_entre_zero_e_cem`, `test_o_validador_e_chamavel_isoladamente`

### `unit/test_comprimento_de_serie.py` — 8

Risco: limite: série curta recusada; não estabiliza → avisa.

`test_serie_constante_basta_com_um_ano`, `test_a_analise_recusa_serie_curta_demais`, `test_o_volume_ideal_e_o_primeiro_abaixo_do_limiar`, `test_a_amostragem_e_reproduzivel_com_a_mesma_semente`, `test_a_amostragem_nao_inventa_janela_alem_das_que_existem`, `test_o_comprimento_tem_de_se_manter_nos_maiores`, `test_serie_que_nao_estabiliza_avisa_em_vez_de_afirmar`, `test_a_serie_do_tutorial_estabiliza_dentro_dos_trinta_anos`

### `unit/test_environmental_params_ui.py` — 8

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_escolher_a_base_muda_o_resultado_da_acv`, `test_a_pureza_muda_a_massa_de_produto_na_acv`, `test_a_aba_entrega_a_pureza_e_a_base_escolhidas`, `test_a_aba_entrega_a_escolha_de_desinfeccao_do_projeto`, `test_a_pureza_fora_da_faixa_e_contida`, `test_o_dialogo_constroi_com_os_controles_novos`, `test_escolher_a_base_reescreve_o_fator_e_mostra_a_procedencia`, `test_salvar_devolve_a_pureza_e_a_base_para_a_aba`

### `unit/test_environmental_sync.py` — 8

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_material_preset_values_match_catalog`, `test_sync_never_changes_explicit_material_because_of_cost`, `test_lca_uses_annual_pump_kwh_when_provided`, `test_config_pipe_lengths_and_sync`, `test_infer_tank_material_from_cost` (restaurado: única cobertura do código), `test_compute_annual_pump_energy_from_simulation` (restaurado: única cobertura do código), `test_build_sync_snapshot_uses_simulation_pump_data` (restaurado: única cobertura do código), `test_nearest_pump_cv_lookup` (restaurado: única cobertura do código)

### `unit/test_impostos_e_bomba_reserva.py` — 8

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_o_imposto_da_agua_nao_e_zerado_ao_fechar`, `test_o_imposto_da_energia_nao_e_zerado_ao_fechar`, `test_o_que_o_usuario_digita_e_o_que_chega_ao_config`, `test_campo_vazio_ou_ilegivel_nao_derruba_a_tela`, `test_o_imposto_da_agua_move_a_conta`, `test_o_imposto_fixo_e_o_variavel_agem_por_caminhos_diferentes`, `test_a_contagem_de_bombas_volta_como_foi_escolhida`, `test_desmarcar_a_reserva_deixa_uma_bomba`

### `unit/test_parser.py` — 8

Risco: limite: números pt-BR/en-US; ida e volta do arquivo.

`test_project_filename_contains_name_date_and_stable_hash`, `test_parse_float_and_int`, `test_load_precipitation_file`, `test_parse_triton_project_csv`, `test_parametros_do_nome_devolvem_so_o_que_encontram`, `test_coeficiente_do_nome_nunca_passa_de_um`, `test_export_netuno4_csv_roundtrip`, `test_export_and_load_triton_json_project`

### `unit/test_water_quality.py` — 8

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_first_flush_zero_discard`, `test_water_quality_classes_nbr15527`, `test_size_first_flush_system_zero`, `test_first_flush_washoff_defaults` (restaurado: única cobertura do código), `test_size_etap` (restaurado: única cobertura do código), `test_size_first_flush_system_small_diverter` (restaurado: única cobertura do código), `test_size_first_flush_system_large_diverter` (restaurado: única cobertura do código), `test_size_etap_with_first_flush_integration` (restaurado: única cobertura do código)

### `unit/test_cad_exporter.py` — 7

Risco: limite: modo inválido e fração/percentual recusados.

`test_generate_technical_a3_dxf`, `test_generate_simple_dxf_and_svg`, `test_share_is_a_fraction_and_percent_is_refused`, `test_block_library_is_reusable_and_auditable`, `test_bim_manifest_preserves_explicit_placements`, `test_invalid_cad_mode_is_rejected`, `test_forchheimer_calculation_and_materials_list`

### `unit/test_energia_de_partida.py` — 7

Risco: invariante físico da energia de partida.

`test_a_energia_e_recalque_mais_partidas_pelo_rendimento_do_motor`, `test_o_rendimento_do_motor_sai_da_tabela_da_norma`, `test_o_rendimento_do_motor_informado_prevalece`, `test_as_partidas_nao_dividem_pelo_rendimento_da_bomba`, `test_sem_partidas_a_energia_e_so_o_recalque`, `test_o_consumo_especifico_de_recurso_segue_a_mesma_convencao`, `test_o_economico_e_a_acv_calculam_a_mesma_energia`

### `unit/test_fechamento_do_balanco.py` — 7

Risco: invariante: demanda = pluvial + potável + não atendida.

`test_desligar_a_reserva_reduz_o_potavel`, `test_o_resumo_concorda_com_a_serie_diaria`, `test_com_a_reserva_ligada_nada_muda`, `test_a_demanda_e_a_soma_de_tres_parcelas`, `test_a_nao_atendida_so_aparece_sem_reserva`, `test_sem_irrigacao_nao_ha_demanda_nao_atendida`, `test_o_nucleo_compilado_concorda_com_o_python`

### `unit/test_projeto_sobrevive_ao_arquivo.py` — 7

Risco: falha real: modulação e casos do manual sobrevivem ao arquivo.

`test_a_modulacao_semanal_sobrevive_ao_arquivo`, `test_a_modulacao_mensal_e_a_diaria_sobrevivem`, `test_a_modulacao_muda_o_resultado_depois_de_reabrir`, `test_json_sem_as_secoes_do_projeto_e_recusado`, `test_projeto_do_esquema_corrente_continua_abrindo`, `test_o_caso_da_escola_guarda_mesmo_a_modulacao`, `test_os_estudos_de_exemplo_estao_no_esquema_corrente`

### `unit/test_pump_wizard.py` — 7

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_forchheimer_calculation`, `test_suction_pipe_one_size_above`, `test_commercial_pump_catalog_consistency`, `test_motobomba_model_governs_pipes_over_forchheimer`, `test_wizard_no_forchheimer_text_and_commercial_pipes`, `test_dialog_other_op_costs_height_and_items`, `test_dialog_initial_costs_all_commercial_pipes`

### `unit/test_pump_wizard_chain.py` — 7

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_o_catalogo_tem_bombas_reais_e_coerentes`, `test_a_altura_manometrica_sai_do_assistente`, `test_desnivel_maior_leva_a_bomba_maior`, `test_a_bomba_escolhida_vence_a_altura_pedida`, `test_a_energia_por_m3_acompanha_o_desnivel`, `test_o_rendimento_do_assistente_chega_ao_retorno`, `test_dialog_electricity_open_pump_wizard`

### `unit/test_tariff_updater.py` — 7

Risco: modo de falha: download lento/interrompido preserva o cache.

`test_download_lento_para_no_prazo_e_preserva_o_cache`, `test_download_interrompido_sem_cache_e_erro_claro`, `test_download_completo_substitui_o_cache`, `test_aneel_fora_do_ar_pula_e_erro_http_falha`, `test_aneel_distributor_matching`, `test_sanitation_registry_matching`, `test_dry_run_execution`

### `unit/test_energia_de_bombeamento_unica.py` — 6

Risco: regressão: rendimento dividido duas vezes.

`test_a_energia_nao_divide_pelo_rendimento_uma_segunda_vez`, `test_o_excesso_da_formula_antiga_e_exatamente_um_sobre_eta`, `test_sem_reservatorio_superior_nao_ha_recalque`, `test_a_energia_acompanha_o_volume_recalcado`, `test_nenhuma_tela_divide_horas_de_bomba_pelo_rendimento`, `test_so_o_nucleo_converte_rendimento_percentual_em_fracao`

### `unit/test_environmental.py` — 6

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_prfv_alias_uses_fiberglass_preset_and_zero_is_no_system_baseline`, `test_chlorine_mass_and_emissions_are_calculated_from_dose`, `test_os_modulos_ambiental_e_de_qualidade_concordam_no_cloro`, `test_environmental_sweep_uses_pump_energy_of_each_volume`, `test_a_contagem_de_bombas_e_a_mesma_no_projeto_e_na_acv`, `test_o_carbono_da_bomba_dobra_com_a_bomba_reserva`

### `unit/test_projeto_climbra.py` — 6

Risco: falha de dependência: base ausente/alterada avisa; série incorporada quando não reproduzível.

`test_arquivo_guarda_a_referencia_e_nao_a_serie`, `test_leitura_recompoe_a_serie_igual`, `test_serie_alterada_continua_incorporada`, `test_arquivo_proprio_continua_incorporado`, `test_impressao_diferente_avisa`, `test_linha_de_comando_le_o_projeto_pela_referencia`

### `unit/test_study_layout.py` — 6

Risco: invariante: arranjo normativo fecha sem erro.

`test_generate_study_layout_creates_valid_bim_manifest`, `test_o_arranjo_normativo_fecha_sem_erros_nem_avisos`, `test_o_arranjo_tem_o_que_a_instalacao_pede`, `test_o_rotulo_da_bomba_vira_a_potencia_certa`, `test_o_kw_informado_prevalece_sobre_o_rotulo`, `test_a_captacao_nasce_no_telhado_e_desce_no_filtro`

### `unit/test_vigencia_tarifaria.py` — 6

Risco: limite: datas ausentes/futuras; contagem de reajustes.

`test_le_a_vigencia_do_catalogo`, `test_conta_os_reajustes_completos_entre_as_datas`, `test_sem_as_duas_datas_ou_vigencia_futura_nada_muda`, `test_conta_mensal_aplica_o_reajuste_passado_e_os_aniversarios_da_vigencia`, `test_conta_anual_usa_a_tarifa_atualizada`, `test_o_projeto_guarda_as_datas_e_o_antigo_fica_como_era`

### `unit/test_volumetry.py` — 6

Risco: invariante geométrico e glTF válido.

`test_primitives_are_closed_with_outward_normals`, `test_tank_dimensions_reproduce_the_capacity_or_keep_given_measures`, `test_scene_uses_the_expected_volumes_and_declares_estimates`, `test_scene_without_building_or_with_invalid_layout`, `test_glb_is_structurally_valid_gltf`, `test_html_viewer_is_self_contained_and_carries_the_scene`

### `invariants/test_numba_python_parity.py` — 5

Risco: falha real: resultado não pode depender de haver numba.

`test_kernels_concordam_na_economia_de_agua`, `test_kernels_concordam_nos_fluxos_agregados`, `test_kernels_concordam_na_estatistica_de_atendimento`, `test_kernel_jit_preserva_a_conservacao_de_massa`, `test_kernels_concordam_na_divisao_interno_irrigacao`

### `unit/test_discretized_demand_irrigation.py` — 5

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_discretized_indoor_and_irrigation_vectors`, `test_hydraulic_priority_and_potable_backup`, `test_irrigation_without_potable_backup`, `test_parser_discretized_roundtrip`, `test_discretized_weekly_modulation_with_irrigation`

### `unit/test_grid_emission_factors.py` — 5

Risco: modo de falha: ano/mês/base inexistente falha alto.

`test_ano_fora_da_serie_falha_alto`, `test_mes_invalido_falha`, `test_config_ambiental_usa_uma_base_declarada_de_co2eq`, `test_o_fator_da_acv_nao_e_o_do_mcti`, `test_base_desconhecida_falha_alto`

### `unit/test_porta_de_validacao_tarifaria.py` — 5

Risco: falha de dependência: raspagem quebrada não entra na base.

`test_a_porta_reconhece_cada_defeito_da_auditoria`, `test_a_porta_deixa_passar_estrutura_correta`, `test_o_motor_de_atualizacao_chama_a_porta`, `test_a_rejeicao_conserva_o_registro_anterior_e_pede_revisao`, `test_um_aviso_nao_barra_a_atualizacao`

### `integration/test_financial_robustness.py` — 4

Risco: TIR conhecida; entradas inválidas recusadas; fluxo fecha.

`test_robust_irr_matches_known_conventional_cash_flow`, `test_robust_economic_rejects_invalid_inputs`, `test_invariant_monotonicity_volume_and_tariff`, `test_invariant_cash_flow_equation_balance`

### `integration/test_report_omitted_values.py` — 4

Risco: regressão: valor omitido no laudo.

`test_o_laudo_executivo_traz_a_confiabilidade`, `test_o_laudo_ambiental_traz_a_dose_de_cloro`, `test_o_laudo_ambiental_nomeia_os_estagios_de_desinfeccao`, `test_a_emissao_por_litro_continua_no_cartao`

### `ui/test_tarifa_exponencial_ui.py` — 4

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_o_gestor_mostra_a_formula_e_simula_com_o_motor`, `test_a_etapa_economica_preserva_a_tabela_exponencial`, `test_a_etapa_economica_traz_o_esgoto_por_m3_da_corsan`, `test_municipio_com_tarifa_por_bairro_oferece_as_alternativas`

### `unit/test_capex_por_volume_na_cli.py` — 4

Risco: paridade interface × CLI.

`test_o_preco_da_cisterna_e_o_mesmo_da_interface`, `test_o_capex_cresce_com_o_volume_na_varredura`, `test_o_vpl_tem_maximo_interior`, `test_volume_unico_mantem_o_preco_declarado`

### `unit/test_cli.py` — 4

Risco: limite: sazonalidade incompleta recusada.

`test_cli_full_analysis_supports_seasonality_and_json_output`, `test_cli_validation_rejects_incomplete_monthly_seasonality`, `test_cli_reports_requested_and_effective_sweep_grid`, `test_cli_project_matrix_expands_factorial_block_and_rainfall_folder`

### `unit/test_mcdm_methods.py` — 4

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_run_smaa_vikor`, `test_smaa_rejects_invalid_number_of_simulations`, `test_run_vikor` (restaurado: única cobertura do código), `test_run_smaa_analysis` (restaurado: única cobertura do código)

### `integration/test_paridade_interface_cli.py` — 3

Risco: paridade interface × CLI.

`test_projeto_distribuido`, `test_alteracao_feita_na_tela_e_gravada`, `test_modo_diario`

### `invariants/test_financial_invariants.py` — 3

Risco: limite: CAPEX zero, volume zero, OPEX proporcional.

`test_financial_invariants_zero_investment`, `test_reference_zero_volume_has_zero_capex_and_zero_opex`, `test_opex_scales_coherently_with_water_harvested_and_pumping`

### `ui/test_fracoes_na_interface.py` — 3

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_tela_mostra_as_fracoes_do_arquivo`, `test_interface_e_linha_de_comando_dao_o_mesmo_potencial`, `test_gravar_e_reabrir_preserva_as_fracoes`

### `ui/test_pipe_runs_dialog.py` — 3

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_dialog_keeps_parameters_and_revalidates_after_reordering`, `test_dialog_builds_volumetry_with_building_and_exports`, `test_dialog_prefills_from_study_when_layout_is_empty`

### `unit/test_calculator.py` — 3

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_find_max_consecutive_run_length`, `test_indices_use_wet_day_percentile_and_keep_windows_inside_year`, `test_exclude_incomplete_years`

### `unit/test_export_tab_and_exporters.py` — 3

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_safe_float_robustness`, `test_cad_robustness_with_unsimulated_project`, `test_cad_dxf_generation`

### `unit/test_exportar_tudo.py` — 3

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_todo_campo_da_configuracao_esta_nas_premissas`, `test_a_tarifa_sai_com_o_significado_de_cada_codigo_e_o_esgoto`, `test_a_etapa_de_qualidade_entra_no_carbono_e_na_planilha`

### `integration/test_exemplo_quatro_criterios.py` — 2

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_fracoes_do_exemplo`, `test_quatro_otimos_distintos`

### `ui/test_tab_building_templates.py` — 2

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_tab_building_fixture_tweak_marks_custom`, `test_tab_building_contextual_typology_adaptations`

### `unit/test_triton_updates.py` — 2

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_monthly_precision_payback_simple`, `test_monthly_precision_payback_discounted`

### `unit/test_tariffs_manager_tab.py` — 2

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_categoria_sem_tabela_coletada_nao_e_estimada`, `test_categoria_coletada_usa_a_tabela_dela`

### `unit/test_technical_only_simulation.py` — 2

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_technical_only_simulation_clears_and_hides_economic_environmental_topsis`, `test_sweep_buttons_trigger_confirmation_dialogs`

### `integration/test_fluidez_de_informacoes.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_recalcular_a_qualidade_nao_apaga_a_escolha_do_usuario`

### `integration/test_national_climate_flow.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_national_climate_and_tariff_integration_flow`

### `integration/test_report_generator.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_generate_research_html_report_without_optimizer_data`

### `invariants/test_mass_conservation.py` — 1

Risco: invariante: balanço hídrico fecha.

`test_water_mass_balance_conservation_invariant`

### `ui/test_mcdm_method_selector.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_selector_exposes_smaa_vikor_as_one_method_with_simulation_profiles`

### `ui/test_projeto_climbra_ui.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_gravar_e_reabrir_com_a_climbra`

### `ui/test_quantitativo_na_interface.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_a_janela_nova_parte_do_arranjo`

### `ui/test_ui_flow.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_full_ui_flow`

### `ui/test_volumetry_view.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_click_selects_component_and_whole_run`

### `unit/test_comprimento_de_serie_ui.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_a_aba_avisa_quando_a_serie_e_curta_demais`

### `unit/test_pump_energy_details.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_pump_backup_count_capex_cost`

### `unit/test_report_service.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_invalid_report_type_is_rejected`

### `unit/test_tab_building_ui.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_tab_building_precalc_and_presets`

### `unit/test_tab_project_ui.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_com_o_campo_vazio_a_previa_usa_a_lamina_da_norma`

### `unit/test_verificacoes_da_revisao.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_versao_declarada_e_coerente`

### `unit/test_change_detector.py` — 1

Risco: regressão de defeito corrigido (regra: todo defeito ganha teste nas duas pontas).

`test_dashboard_generation` (restaurado: única cobertura do código)

### `unit/test_daily_water_balance.py` — 1

Risco: caso de 3 dias resolvido à mão.

`test_simple_3day_water_balance` (restaurado: única cobertura do código)

## Guardas de dado (ficaram onde estavam)

- `unit/test_catalogo_de_componentes.py` — 5
- `unit/test_categoria_tarifaria.py` — 13
- `unit/test_categorias_casan.py` — 3
- `unit/test_categorias_corsan.py` — 5
- `unit/test_climate_database.py` — 6
- `unit/test_economic.py` — 2
- `unit/test_environmental_params_ui.py` — 7
- `unit/test_funcoes_orfas.py` — 12
- `unit/test_grid_emission_factors.py` — 6
- `unit/test_modulacao_estocastica.py` — 1
- `unit/test_percentual_de_esgoto.py` — 10
- `unit/test_pipe_masses.py` — 8
- `unit/test_precos_de_reservatorio.py` — 1
- `unit/test_processar_entrada.py` — 9
- `unit/test_processo_tarifario.py` — 7
- `unit/test_projeto_sobrevive_ao_arquivo.py` — 2
- `unit/test_regimes_tarifarios.py` — 7
- `unit/test_registro_de_fontes.py` — 3
- `unit/test_rotas_por_tecnologia.py` — 17
- `unit/test_tabela_de_faixas.py` — 2
- `unit/test_tarifa_exponencial.py` — 6
- `unit/test_tariffs_database.py` — 4
- `unit/test_tariffs_structure.py` — 8
- `unit/test_transcricoes.py` — 11
- `unit/test_water_supply_routes.py` — 12

## Guardas de manual e documentação (ficaram onde estavam)

- `integration/test_report_generator.py` — 2
- `invariants/test_coerencia_da_documentacao.py` — 5
- `unit/test_acervo_de_manuais.py` — 6
- `unit/test_changelog.py` — 10
- `unit/test_documentation_citations.py` — 19
- `unit/test_escrita_segura_do_manual.py` — 6
- `unit/test_figuras_do_manual_cabem.py` — 3
- `unit/test_figuras_interativas.py` — 4
- `unit/test_figuras_interativas_validacao.py` — 19
- `unit/test_figuras_sem_corte.py` — 1
- `unit/test_graficos_de_indices_usam_o_ano.py` — 2
- `unit/test_manual_confere_com_o_programa.py` — 71
- `unit/test_manual_en.py` — 9
- `unit/test_mini_manuais.py` — 5
- `unit/test_o_que_se_comunica.py` — 28
- `unit/test_padroes_hidrologicos.py` — 5
- `unit/test_reference_documents.py` — 6
- `unit/test_relatorio_de_verificacao.py` — 1
- `unit/test_traducao_completa.py` — 2
- `unit/test_traducao_sem_mistura.py` — 3

## Guardas de distribuição (ficaram onde estavam)

- `invariants/test_declared_dependencies.py` — 2
- `invariants/test_saida_de_console.py` — 1
- `unit/test_build_git.py` — 3
- `unit/test_ci_sem_rede.py` — 3
- `unit/test_diagnostico.py` — 3
- `unit/test_edicoes_documentadas.py` — 1
- `unit/test_empacotamento.py` — 6
- `unit/test_folhas_de_estilo.py` — 2
- `unit/test_icones.py` — 3
- `unit/test_instalador.py` — 5
- `unit/test_qt_diagnostics.py` — 7
- `unit/test_volumetria_web.py` — 8

## Validação contra o Netuno 4 (ficaram onde estavam)

- `benchmarking/test_replicacao_netuno4.py` — 6
- `integration/test_batch_validation.py` — 1

