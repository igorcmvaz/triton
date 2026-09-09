"""
Etapa 3: Reservatorio, Varredura & Custos (Netuno 5).
Todos os inputs: varredura, reservatorios, parametros financeiros, CAPEX, OPEX e Tarifas.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame, QScrollArea, QInputDialog
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont
from netuno.ui.translation import tr, get_current_theme

from netuno.core.simulation import (
    SWEEP_STEP_QUANTUM_L,
    build_sweep_volume_grid,
    run_single_simulation,
    run_sweep_simulation,
)
from netuno.core.parser import parse_float, parse_int, format_ptbr


class TabTanksSimulation(QWidget):
    simulation_completed = Signal(object, object)  # (single_result, sweep_result)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.last_single_result = None
        self.last_sweep_result = None
        self.precip_data = None
        # A varredura é a fonte única de alternativas do projeto.  Nenhuma
        # etapa anterior ao TOPSIS deve transformar o ponto do threshold em
        # uma decisão de projeto.
        self.selected_volume_mode = "sweep"
        self.custom_selected_vol = 5000.0
        self.verified_dialogs = set()
        self._is_technical_only = True
        self._inf_mode = "month"
        self._tma_mode = "month"
        self._applying_preset = False
        self._setting_auto_sweep = False
        self._auto_sweep_max_value = None
        self._auto_sweep_step_value = None
        # Alterações hidráulicas são agrupadas para não recalcular a cada
        # caractere digitado, mas nunca deixam cartões com dados defasados.
        self._hydraulic_refresh_timer = QTimer(self)
        self._hydraulic_refresh_timer.setSingleShot(True)
        self._hydraulic_refresh_timer.setInterval(350)
        self._hydraulic_refresh_timer.timeout.connect(self._refresh_hydraulic_results)
        self.init_ui()

    def init_ui(self):
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(40, 34, 40, 40)
        main_layout.setSpacing(16)

        is_dark = get_current_theme() == "dark"
        lbl_title = QLabel(tr("Reservatórios, bombeamento e custos"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        main_layout.addWidget(lbl_title)

        # ===== SECAO A: VARREDURA + RESERVATORIOS =====
        gb_tanks = QGroupBox(tr("🔍 A. Parametros da Varredura de Volumes e Reservatorios"))
        lay_t = QVBoxLayout()
        grid_sw = QGridLayout()
        grid_sw.setSpacing(8)

        grid_sw.addWidget(QLabel(tr("Volume Maximo da Varredura (L):")), 0, 0)
        self.txt_sweep_max = QLineEdit("")
        self.txt_sweep_max.setPlaceholderText(tr("Ex: 50000"))
        self.txt_sweep_max.textChanged.connect(lambda: self.check_input_highlight(self.txt_sweep_max))
        self.txt_sweep_max.textChanged.connect(self._on_sweep_max_changed)
        self.txt_sweep_max.editingFinished.connect(self._apply_sweep_grid_policy)
        grid_sw.addWidget(self.txt_sweep_max, 0, 1)

        grid_sw.addWidget(QLabel(tr("Passo de Varredura (L):")), 1, 0)
        self.txt_sweep_step = QLineEdit("")
        self.txt_sweep_step.setPlaceholderText(tr("Ex: 1000"))
        self.txt_sweep_step.textChanged.connect(lambda: self.check_input_highlight(self.txt_sweep_step))
        self.txt_sweep_step.textChanged.connect(self._on_sweep_step_changed)
        self.txt_sweep_step.editingFinished.connect(self._apply_sweep_grid_policy)
        grid_sw.addWidget(self.txt_sweep_step, 1, 1)

        grid_sw.addWidget(QLabel(tr("Limiar Minimo / Threshold (Delta %/m3):")), 2, 0)
        self.txt_delta_ideal = QLineEdit("")
        self.txt_delta_ideal.setPlaceholderText(tr("Ex: 2,5"))
        self.txt_delta_ideal.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")
        self.txt_delta_ideal.textChanged.connect(lambda: self.check_input_highlight(self.txt_delta_ideal))
        self.txt_delta_ideal.textChanged.connect(lambda: self._mark_preset_custom("combo_threshold_profile"))
        grid_sw.addWidget(self.txt_delta_ideal, 2, 1)

        grid_sw.addWidget(QLabel(tr("Perfil do limiar tecnico:")), 3, 0)
        self.combo_threshold_profile = QComboBox()
        self.combo_threshold_profile.addItem(tr("Personalizado — manter valor informado"), None)
        self.combo_threshold_profile.addItem(tr("Conservador — 5,0 %/m3"), 5.0)
        self.combo_threshold_profile.addItem(tr("Equilibrado — 2,5 %/m3"), 2.5)
        self.combo_threshold_profile.addItem(tr("Maximo aproveitamento — 1,0 %/m3"), 1.0)
        self.combo_threshold_profile.setCurrentIndex(0)
        self.combo_threshold_profile.currentIndexChanged.connect(self._apply_threshold_profile)
        grid_sw.addWidget(self.combo_threshold_profile, 3, 1)
        lay_t.addLayout(grid_sw)

        self.lbl_sweep_guidance = QLabel(tr("Sugestao: limite = 8 × SDII × area × coeficiente de escoamento; passo-base de 250 L, dobrado automaticamente para manter no maximo 40 volumes positivos."))
        self.lbl_sweep_guidance.setWordWrap(True)
        self.lbl_sweep_guidance.setStyleSheet("color: #475569; font-size: 11px; padding: 2px 0;")
        lay_t.addWidget(self.lbl_sweep_guidance)

        lbl_sup = QLabel(tr("Reservatorio Superior (Elevado / Motobomba):"))
        lbl_sup.setStyleSheet("font-weight: bold; margin-top: 6px;")
        lay_t.addWidget(lbl_sup)

        self.combo_upper_mode = QComboBox()
        self.combo_upper_mode.addItem(tr("Igual a Demanda Diaria Pluvial"), 0)
        self.combo_upper_mode.addItem(tr("Volume Especifico Customizado (L)"), 1)
        self.combo_upper_mode.addItem(tr("Nao Utilizar Reservatorio Superior"), 2)
        self.combo_upper_mode.currentIndexChanged.connect(self.on_param_changed)
        self.combo_upper_mode.currentIndexChanged.connect(self._queue_hydraulic_refresh)
        lay_t.addWidget(self.combo_upper_mode)

        row_up_vol = QHBoxLayout()
        row_up_vol.addWidget(QLabel(tr("Vol. Superior (L):")))
        self.txt_upper_vol = QLineEdit("")
        self.txt_upper_vol.setPlaceholderText("Ex: 500")
        self.txt_upper_vol.textChanged.connect(self.on_param_changed)
        self.txt_upper_vol.textChanged.connect(self._queue_hydraulic_refresh)
        row_up_vol.addWidget(self.txt_upper_vol)
        lay_t.addLayout(row_up_vol)

        row_pump_thresh = QHBoxLayout()
        row_pump_thresh.addWidget(QLabel(tr("Limiar Recalque (% Res. Sup.):")))
        self.txt_pump_thresh_pct = QLineEdit("")
        self.txt_pump_thresh_pct.setPlaceholderText(tr("Ex: 30"))
        self.txt_pump_thresh_pct.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")
        self.txt_pump_thresh_pct.textChanged.connect(self.check_pump_threshold_highlight)
        self.txt_pump_thresh_pct.textChanged.connect(self.on_param_changed)
        self.txt_pump_thresh_pct.textChanged.connect(self._queue_hydraulic_refresh)
        self.txt_pump_thresh_pct.textChanged.connect(lambda: self._mark_preset_custom("combo_pump_profile"))
        row_pump_thresh.addWidget(self.txt_pump_thresh_pct)
        self.combo_pump_profile = QComboBox()
        self.combo_pump_profile.addItem(tr("Recalque personalizado"), None)
        self.combo_pump_profile.addItem(tr("Recalque responsivo — 10%"), 10.0)
        self.combo_pump_profile.addItem(tr("Recalque equilibrado — 30%"), 30.0)
        self.combo_pump_profile.addItem(tr("Recalque conservador — 50%"), 50.0)
        self.combo_pump_profile.setCurrentIndex(0)
        self.combo_pump_profile.currentIndexChanged.connect(self._apply_pump_profile)
        self.combo_pump_profile.setMinimumWidth(220)
        row_pump_thresh.addWidget(self.combo_pump_profile)
        lay_t.addLayout(row_pump_thresh)
        lbl_pump_guidance = QLabel(tr("Para a motobomba, 30–50% e uma faixa inicial usual. Este campo so controla o recalque entre os reservatorios do sistema pluvial."))
        lbl_pump_guidance.setWordWrap(True)
        lbl_pump_guidance.setStyleSheet("color: #475569; font-size: 11px; padding: 0 0 2px 0;")
        lay_t.addWidget(lbl_pump_guidance)

        self.btn_pump_wizard = QPushButton(tr("🧙 Assistente de Dimensionamento de Motobomba..."))
        self.btn_pump_wizard.setStyleSheet("font-weight: bold; background-color: #0d9488; color: white; padding: 6px 12px; margin-top: 4px;")
        self.btn_pump_wizard.clicked.connect(self.open_pump_wizard)
        lay_t.addWidget(self.btn_pump_wizard)

        # ── BOTÃO DE VARREDURA TÉCNICA (SOMENTE HIDRÁULICA) ──
        card_tech_sim = QFrame()
        if is_dark:
            card_tech_sim.setStyleSheet("QFrame { background-color: #064e3b; border: 1.5px solid #059669; border-radius: 6px; padding: 6px; margin-top: 6px; }")
        else:
            card_tech_sim.setStyleSheet("QFrame { background-color: #f0fdf4; border: 1.5px solid #86efac; border-radius: 6px; padding: 6px; margin-top: 6px; }")
        lay_tech_btn = QVBoxLayout(card_tech_sim)
        lay_tech_btn.setContentsMargins(6, 6, 6, 6)
        lay_tech_btn.setSpacing(4)

        self.btn_run_tech_sim = QPushButton(tr("⚡ EXECUTAR VARREDURA TÉCNICA (SOMENTE HIDRÁULICA)"))
        self.btn_run_tech_sim.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 12.5px;
                background-color: #059669;
                color: white;
                padding: 10px 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        self.btn_run_tech_sim.clicked.connect(self.run_technical_simulation)
        lay_tech_btn.addWidget(self.btn_run_tech_sim)

        lbl_tech_desc = QLabel(
            tr("💡 <b>Análise Técnica Rápida:</b> Simula o potencial de economia de água (%), dias de atendimento e balanço hídrico diário para toda a grade de volumes (Etapa 4), sem exigir o preenchimento prévio das seções financeiras (B) e de custos (C).")
        )
        lbl_tech_desc.setWordWrap(True)
        lbl_tech_desc.setStyleSheet("color: #166534; font-size: 11px;" if not is_dark else "color: #a7f3d0; font-size: 11px;")
        lay_tech_btn.addWidget(lbl_tech_desc)
        lay_t.addWidget(card_tech_sim)

        gb_tanks.setLayout(lay_t)
        main_layout.addWidget(gb_tanks)

        # ===== SECAO B: PARAMETROS FINANCEIROS GLOBAIS =====
        gb_params = QGroupBox(tr("💰 B. Parametros Financeiros Globais"))
        lay_p = QVBoxLayout()
        lay_p.setSpacing(10)
        grid_fin = QGridLayout()
        grid_fin.setHorizontalSpacing(14)
        grid_fin.setVerticalSpacing(8)

        # Linha 0: Inflacao | Periodo de analise
        grid_fin.addWidget(QLabel(tr("Inflacao:")), 0, 0)
        row_inf = QHBoxLayout()
        self.txt_inflation = QLineEdit("-")
        self.txt_inflation.setFixedWidth(80)
        self.txt_inflation.setToolTip(tr("Taxa aplicada somente aos custos adicionais de O&M; nao reajusta agua, esgoto ou energia."))
        self.txt_inflation.textChanged.connect(lambda: self.check_econ_highlight(self.txt_inflation))
        self.txt_inflation.textChanged.connect(lambda: self._mark_preset_custom("combo_inflation_profile"))
        row_inf.addWidget(self.txt_inflation)
        self.btn_inf_toggle = QPushButton(tr("% a.m."))
        self.btn_inf_toggle.setFixedWidth(62)
        self.btn_inf_toggle.setCheckable(True)
        self.btn_inf_toggle.setStyleSheet("QPushButton{background:#e0f2fe;color:#0369a1;border:1px solid #7dd3fc;border-radius:3px;padding:2px 4px;font-size:10px;}QPushButton:checked{background:#0369a1;color:white;}")
        self.btn_inf_toggle.clicked.connect(self._on_inf_toggle)
        row_inf.addWidget(self.btn_inf_toggle)
        self.combo_inflation_profile = QComboBox()
        self.combo_inflation_profile.addItem(tr("Inflação personalizada"), {"description": tr("Informe a taxa compatível com o contrato e o período analisado.")})
        self.combo_inflation_profile.addItem(tr("Referência IPCA — 4,5% a.a. (O&M)"), {"annual_rate": 4.5, "description": tr("Referência de longo prazo para O&M; revise antes de usar em um orçamento real.")})
        self.combo_inflation_profile.addItem(tr("Referência INPC — 4,5% a.a. (O&M)"), {"annual_rate": 4.5, "description": tr("Referência para despesas familiares e serviços; revise antes de usar em um orçamento real.")})
        self.combo_inflation_profile.addItem(tr("Referência IGP-DI — 5,0% a.a. (O&M)"), {"annual_rate": 5.0, "description": tr("Referência contratual ampla; mais sensível a atacado, insumos e câmbio.")})
        self.combo_inflation_profile.addItem(tr("Referência IGP-M — 5,0% a.a. (O&M)"), {"annual_rate": 5.0, "description": tr("Referência contratual para O&M; mais sensível a insumos e câmbio.")})
        self.combo_inflation_profile.currentIndexChanged.connect(self._apply_inflation_profile)
        self.combo_inflation_profile.setMinimumWidth(300)
        row_inf.addWidget(self.combo_inflation_profile)
        row_inf.addStretch()
        grid_fin.addLayout(row_inf, 0, 1)

        grid_fin.addWidget(QLabel(tr("Periodo de analise (anos):")), 0, 2)
        self.txt_period = QLineEdit("-")
        self.txt_period.textChanged.connect(lambda: self.check_econ_highlight(self.txt_period))
        grid_fin.addWidget(self.txt_period, 0, 3)

        # Linha 1: TMA | Periodo de reajuste
        grid_fin.addWidget(QLabel(tr("TMA:")), 1, 0)
        row_tma = QHBoxLayout()
        self.txt_tma = QLineEdit("-")
        self.txt_tma.setFixedWidth(80)
        self.txt_tma.setToolTip(tr("Taxa Minima de Atratividade."))
        self.txt_tma.textChanged.connect(lambda: self.check_econ_highlight(self.txt_tma))
        self.txt_tma.textChanged.connect(lambda: self._mark_preset_custom("combo_tma_profile"))
        row_tma.addWidget(self.txt_tma)
        self.btn_tma_toggle = QPushButton(tr("% a.m."))
        self.btn_tma_toggle.setFixedWidth(62)
        self.btn_tma_toggle.setCheckable(True)
        self.btn_tma_toggle.setStyleSheet("QPushButton{background:#e0f2fe;color:#0369a1;border:1px solid #7dd3fc;border-radius:3px;padding:2px 4px;font-size:10px;}QPushButton:checked{background:#0369a1;color:white;}")
        self.btn_tma_toggle.clicked.connect(self._on_tma_toggle)
        row_tma.addWidget(self.btn_tma_toggle)
        self.combo_tma_profile = QComboBox()
        self.combo_tma_profile.addItem(tr("TMA personalizada"), None)
        self.combo_tma_profile.addItem(tr("Referência real (IPCA + spread) — 6,0% a.a."), 6.0)
        self.combo_tma_profile.addItem(tr("Referência neutra de mercado — 10,0% a.a."), 10.0)
        self.combo_tma_profile.addItem(tr("Custo de capital conservador — 12,0% a.a."), 12.0)
        self.combo_tma_profile.addItem(tr("Taxa Selic / Custo de oportunidade atual — 14,0% a.a."), 14.0)
        self.combo_tma_profile.addItem(tr("Capital próprio com risco / Comercial — 16,0% a.a."), 16.0)
        self.combo_tma_profile.currentIndexChanged.connect(self._apply_tma_profile)
        self.combo_tma_profile.setMinimumWidth(260)
        row_tma.addWidget(self.combo_tma_profile)
        row_tma.addStretch()
        grid_fin.addLayout(row_tma, 1, 1)

        grid_fin.addWidget(QLabel(tr("Periodo de reajuste de tarifas (meses):")), 2, 2)
        self.txt_readj_period = QLineEdit("-")
        self.txt_readj_period.setToolTip(tr("Periodo em meses entre cada reajuste tarifario."))
        self.txt_readj_period.textChanged.connect(lambda: self.check_econ_highlight(self.txt_readj_period))
        self.txt_readj_period.textChanged.connect(lambda: self._mark_preset_custom("combo_tariff_profile"))
        grid_fin.addWidget(self.txt_readj_period, 2, 3)

        # Linha 2: perfil antes dos valores que ele pode preencher
        grid_fin.addWidget(QLabel(tr("Perfil de reajuste tarifario:")), 2, 0)
        self.combo_tariff_profile = QComboBox()
        self.combo_tariff_profile.addItem(tr("Tarifas personalizadas"), None)
        self.combo_tariff_profile.addItem(tr("Sem projecao — 0,0% a.a."), (12, 0.0, 0.0))
        self.combo_tariff_profile.addItem(tr("Referência de planejamento 2025 — energia 3,5%; água contratual 4,5% a.a."), (12, 4.5, 3.5))
        self.combo_tariff_profile.addItem(tr("Referência regulatória — água/esgoto 5,0%; energia 6,0% a.a."), (12, 5.0, 6.0))
        self.combo_tariff_profile.addItem(tr("Cenário inflacionário moderado — água 6,5% a.a.; energia 7,5% a.a."), (12, 6.5, 7.5))
        self.combo_tariff_profile.addItem(tr("Escalada de escassez hídrica — água 8,5% a.a.; energia 9,0% a.a."), (12, 8.5, 9.0))
        self.combo_tariff_profile.currentIndexChanged.connect(self._apply_tariff_profile)
        grid_fin.addWidget(self.combo_tariff_profile, 2, 1)
        grid_fin.addWidget(QLabel(tr("Moeda / Currency:")), 1, 2)
        self.combo_currency = QComboBox()
        self.combo_currency.addItems(["R$ (BRL)", "$ (USD)", "\u20ac (EUR)", "\u00a3 (GBP)", "\u00a5 (CNY)"])
        self.combo_currency.currentIndexChanged.connect(self.on_currency_changed)
        grid_fin.addWidget(self.combo_currency, 1, 3)

        # Linha 3: Reajuste agua | Reajuste energia
        grid_fin.addWidget(QLabel(tr("Reajuste agua/esgoto (% por periodo):")), 3, 0)
        self.txt_readj_water = QLineEdit("-")
        self.txt_readj_water.setToolTip(tr("Reajuste independente das tarifas de agua e esgoto; altera as economias calculadas no periodo configurado."))
        self.txt_readj_water.textChanged.connect(lambda: self.check_econ_highlight(self.txt_readj_water))
        self.txt_readj_water.textChanged.connect(lambda: self._mark_preset_custom("combo_tariff_profile"))
        grid_fin.addWidget(self.txt_readj_water, 3, 1)

        grid_fin.addWidget(QLabel(tr("Reajuste energia eletrica (% por periodo):")), 3, 2)
        self.txt_readj_elec = QLineEdit("-")
        self.txt_readj_elec.setToolTip(tr("Reajuste independente da tarifa de energia; altera o custo de bombeamento no periodo configurado."))
        self.txt_readj_elec.textChanged.connect(lambda: self.check_econ_highlight(self.txt_readj_elec))
        self.txt_readj_elec.textChanged.connect(lambda: self._mark_preset_custom("combo_tariff_profile"))
        grid_fin.addWidget(self.txt_readj_elec, 3, 3)

        lay_p.addLayout(grid_fin)
        self.lbl_preset_guidance = QLabel(tr("Perfis são opcionais: selecione um para preencher valores de referência ou mantenha cada campo personalizado."))
        self.lbl_preset_guidance.setWordWrap(True)
        self.lbl_preset_guidance.setStyleSheet("color: #475569; font-size: 11px; padding: 2px 0;")
        lay_p.addWidget(self.lbl_preset_guidance)
        gb_params.setLayout(lay_p)
        main_layout.addWidget(gb_params)

        # ===== SECAO C: CAPEX / OPEX / TARIFAS =====
        gb_costs = QGroupBox(tr("\U0001f4b3 C. Custos de Implantacao, Operacao e Tarifas de Agua/Energia"))
        lay_c = QVBoxLayout()
        lay_c.setSpacing(10)
        lay_modals = QHBoxLayout()
        lay_modals.setSpacing(10)

        self.btn_mod_capex     = QPushButton(tr("⚪ 1. Investimento Inicial (CAPEX)..."))
        self.btn_mod_motobomba = QPushButton(tr("⚪ 2. Motobomba e Custo de Energia..."))
        self.btn_mod_opex      = QPushButton(tr("⚪ 3. Outros Custos Operacionais..."))
        self.btn_mod_tariffs   = QPushButton(tr("⚪ 4. Tarifas de Água e Esgoto..."))

        self.btn_mod_capex.clicked.connect(self.on_open_capex_dialog)
        self.btn_mod_motobomba.clicked.connect(self.on_open_motobomba_dialog)
        self.btn_mod_opex.clicked.connect(self.on_open_opex_dialog)
        self.btn_mod_tariffs.clicked.connect(self.on_open_tariffs_dialog)

        lay_modals.addWidget(self.btn_mod_capex)
        lay_modals.addWidget(self.btn_mod_motobomba)
        lay_modals.addWidget(self.btn_mod_opex)
        lay_modals.addWidget(self.btn_mod_tariffs)
        lay_c.addLayout(lay_modals)

        self.lbl_verification_status = QLabel()
        self.lbl_verification_status.setAlignment(Qt.AlignCenter)
        lay_c.addWidget(self.lbl_verification_status)
        gb_costs.setLayout(lay_c)
        main_layout.addWidget(gb_costs)

        # ===== SECAO D: EXECUCAO DA VARREDURA & ALTERNATIVAS =====
        gb_exec = QGroupBox(tr("⚡ D. Execução da Varredura & Alternativas de Projeto"))
        lay_exec = QVBoxLayout()
        lay_exec.setSpacing(8)

        self.btn_run_sim = QPushButton(tr("⚡ EXECUTAR VARREDURA COMPLETA (HIDRÁULICA, ECONÔMICA & AMBIENTAL)"))
        self.btn_run_sim.setStyleSheet(f"""
            QPushButton {{
                font-weight: bold;
                font-size: 13px;
                background-color: #0284c7;
                color: white;
                padding: 12px 18px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #0369a1;
            }}
        """)
        self.btn_run_sim.clicked.connect(self.run_complete_simulation)
        lay_exec.addWidget(self.btn_run_sim)

        lbl_full_desc = QLabel(
            tr("Executa a simulação hidráulica completa para toda a grade de volumes e processa automaticamente as análises financeira e ambiental, consolidando os resultados para as Etapas 5 (Econômico), 6 (Ambiental — ACV) e 7 (Decisão Multicritério TOPSIS).")
        )
        lbl_full_desc.setWordWrap(True)
        lbl_full_desc.setStyleSheet("color: #475569; font-size: 11px;")
        lay_exec.addWidget(lbl_full_desc)

        # Card de status das alternativas
        self.card_volume_select = QFrame()
        if is_dark:
            self.card_volume_select.setStyleSheet("QFrame { background-color: #1e293b; border: 1.5px solid #3b82f6; border-radius: 6px; padding: 6px; }")
        else:
            self.card_volume_select.setStyleSheet("QFrame { background-color: #f0f9ff; border: 1.5px solid #0284c7; border-radius: 6px; padding: 6px; }")
        lay_vsel = QVBoxLayout(self.card_volume_select)
        lay_vsel.setContentsMargins(10, 8, 10, 8)
        lay_vsel.setSpacing(8)

        self.lbl_selected_vol_status = QLabel(tr("Varredura ainda não executada. Preencha os dados das seções A, B e C e clique acima para executar."))
        self.lbl_selected_vol_status.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {'#93c5fd' if is_dark else '#0369a1'};"
        )
        lay_vsel.addWidget(self.lbl_selected_vol_status)

        lay_exec.addWidget(self.card_volume_select)
        gb_exec.setLayout(lay_exec)
        main_layout.addWidget(gb_exec)
        main_layout.addStretch(1)

        # Highlights iniciais
        for w in [self.txt_sweep_max, self.txt_sweep_step, self.txt_delta_ideal]:
            self.check_input_highlight(w)
        self.check_pump_threshold_highlight()
        for w in [self.txt_inflation, self.txt_tma, self.txt_period, self.txt_readj_period, self.txt_readj_water, self.txt_readj_elec]:
            self.check_econ_highlight(w)
        self.update_dialog_button_styles()

        scroll.setWidget(content_widget)
        main_vbox.addWidget(scroll)

    # ── Highlights ─────────────────────────────────────────────────────────────
    def check_input_highlight(self, le):
        v = le.text().strip()
        if not v or v == "-" or not self.is_valid_number(v):
            le.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")
        else:
            le.setStyleSheet("QLineEdit { background-color: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; }")

    def check_econ_highlight(self, le):
        v = le.text().strip()
        if not v or v == "-" or not self.is_valid_econ_number(v):
            le.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")
        else:
            le.setStyleSheet("QLineEdit { background-color: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; }")

    def is_valid_number(self, v):
        try:
            return float(v.replace(",", ".")) > 0
        except ValueError:
            return False

    def is_valid_pump_threshold(self, v):
        try:
            return 0.0 <= float(v.replace(",", ".")) <= 100.0
        except ValueError:
            return False

    def check_pump_threshold_highlight(self, *_args):
        valid = self.is_valid_pump_threshold(self.txt_pump_thresh_pct.text().strip())
        self.txt_pump_thresh_pct.setStyleSheet(
            "QLineEdit { background-color: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; }"
            if valid else
            "QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }"
        )

    def is_valid_econ_number(self, v):
        try:
            float(v.replace(",", "."))
            return True
        except ValueError:
            return False

    # ── Toggles Taxa ──────────────────────────────────────────────────────────
    def _on_inf_toggle(self, checked):
        val = parse_float(self.txt_inflation.text(), None)
        if checked:
            self._inf_mode = "year"
            self.btn_inf_toggle.setText("% a.a.")
            if val is not None:
                self.txt_inflation.setText(format_ptbr(((1 + val / 100.0) ** 12 - 1) * 100.0, 3, thousands=False))
        else:
            self._inf_mode = "month"
            self.btn_inf_toggle.setText("% a.m.")
            if val is not None:
                self.txt_inflation.setText(format_ptbr(((1 + val / 100.0) ** (1/12) - 1) * 100.0, 3, thousands=False))

    def _on_tma_toggle(self, checked):
        val = parse_float(self.txt_tma.text(), None)
        if checked:
            self._tma_mode = "year"
            self.btn_tma_toggle.setText("% a.a.")
            if val is not None:
                self.txt_tma.setText(format_ptbr(((1 + val / 100.0) ** 12 - 1) * 100.0, 3, thousands=False))
        else:
            self._tma_mode = "month"
            self.btn_tma_toggle.setText("% a.m.")
            if val is not None:
                self.txt_tma.setText(format_ptbr(((1 + val / 100.0) ** (1/12) - 1) * 100.0, 3, thousands=False))

    def _set_preset_guidance(self, message):
        if hasattr(self, "lbl_preset_guidance"):
            self.lbl_preset_guidance.setText(message)

    def _mark_preset_custom(self, combo_name):
        """Reflect a manual edit without overwriting the user's input."""
        if self._applying_preset:
            return
        combo = getattr(self, combo_name, None)
        if combo is not None and combo.currentIndex() != 0:
            combo.blockSignals(True)
            combo.setCurrentIndex(0)
            combo.blockSignals(False)
            self._set_preset_guidance(tr("Valor personalizado mantido; nenhum perfil será aplicado automaticamente."))

    def _set_field_from_preset(self, field, value):
        self._applying_preset = True
        try:
            field.setText(format_ptbr(value, 2, thousands=False))
        finally:
            self._applying_preset = False

    def _set_annual_rate_from_preset(self, field, button, mode_attr, value):
        self._applying_preset = True
        try:
            setattr(self, mode_attr, "year")
            button.blockSignals(True)
            button.setChecked(True)
            button.setText("% a.a.")
            button.blockSignals(False)
            field.setText(format_ptbr(value, 2, thousands=False))
        finally:
            self._applying_preset = False

    def _apply_threshold_profile(self, _index):
        value = self.combo_threshold_profile.currentData()
        if value is None or self._applying_preset:
            return
        self._set_field_from_preset(self.txt_delta_ideal, value)
        self._set_preset_guidance(tr("Perfil técnico aplicado como referência; o limiar continua livre para edição."))

    def _apply_pump_profile(self, _index):
        value = self.combo_pump_profile.currentData()
        if value is None or self._applying_preset:
            return
        self._set_field_from_preset(self.txt_pump_thresh_pct, value)
        self._set_preset_guidance(tr("Perfil de recalque aplicado como referência; este controle não representa a rede pública."))

    def _apply_inflation_profile(self, _index):
        profile = self.combo_inflation_profile.currentData() or {}
        if self._applying_preset:
            return
        annual_rate = profile.get("annual_rate")
        if annual_rate is not None:
            self._set_annual_rate_from_preset(self.txt_inflation, self.btn_inf_toggle, "_inf_mode", annual_rate)
        self._set_preset_guidance(profile.get("description", tr("Valor personalizado mantido; nenhum perfil será aplicado automaticamente.")))

    def _apply_tma_profile(self, _index):
        value = self.combo_tma_profile.currentData()
        if value is None or self._applying_preset:
            return
        self._set_annual_rate_from_preset(self.txt_tma, self.btn_tma_toggle, "_tma_mode", value)
        self._set_preset_guidance(tr("Perfil de TMA aplicado como referência; valide-o com o custo de capital do projeto."))

    def _apply_tariff_profile(self, _index):
        values = self.combo_tariff_profile.currentData()
        if values is None or self._applying_preset:
            return
        period, water, electricity = values
        self._applying_preset = True
        try:
            self.txt_readj_period.setText(format_ptbr(period, 0, thousands=False))
            self.txt_readj_water.setText(format_ptbr(water, 2, thousands=False))
            self.txt_readj_elec.setText(format_ptbr(electricity, 2, thousands=False))
        finally:
            self._applying_preset = False
        self._set_preset_guidance(tr("Perfil tarifário aplicado como referência; inflação e tarifas continuam sendo premissas independentes."))

    def get_tma_annual_pct(self):
        val = parse_float(self.txt_tma.text(), 12.0)
        if getattr(self, "_tma_mode", "year") == "month":
            return ((1 + val / 100.0) ** 12 - 1) * 100.0
        return val

    def get_inflation_annual_pct(self):
        val = parse_float(self.txt_inflation.text(), 4.5)
        if getattr(self, "_inf_mode", "year") == "month":
            return ((1 + val / 100.0) ** 12 - 1) * 100.0
        return val

    def get_currency_symbol(self):
        if not hasattr(self, "combo_currency"):
            return "R$"
        cur = self.combo_currency.currentText()
        if "R$" in cur:
            return "R$"
        elif "$" in cur:
            return "$"
        elif "\u20ac" in cur:
            return "\u20ac"
        elif "\u00a3" in cur:
            return "\u00a3"
        elif "\u00a5" in cur:
            return "\u00a5"
        return "$"

    def on_currency_changed(self):
        main_win = self.window()
        if main_win and hasattr(main_win, "config"):
            cfg = main_win.config
            self.verified_dialogs.clear()
            if self.get_currency_symbol() != "R$":
                cfg.cost_lower_tank = 0.0; cfg.cost_upper_tank = 0.0
                cfg.cost_labor = 0.0; cfg.cost_piping = 0.0
                cfg.cost_accessories = 0.0; cfg.op_costs = []
                cfg.elec_tariff = 0.0; cfg.water_tariffs = []
                cfg.pump_unit_cost = 0.0
        self.update_dialog_button_styles()

    def update_dialog_button_styles(self):
        is_dark = get_current_theme() == "dark"
        s0 = (
            "background-color: #27272a; color: #e4e4e7; border: 1px solid #52525b; font-weight: bold; padding: 8px; border-radius: 6px;"
            if is_dark else
            "background-color: #f8fafc; color: #475569; border: 1px solid #cbd5e1; font-weight: bold; padding: 8px; border-radius: 6px;"
        )
        s1 = (
            "background-color: #143624; color: #86efac; border: 2px solid #16a34a; font-weight: bold; padding: 8px; border-radius: 6px;"
            if is_dark else
            "background-color: #f0fdf4; color: #15803d; border: 2px solid #16a34a; font-weight: bold; padding: 8px; border-radius: 6px;"
        )
        chk = self.verified_dialogs
        self.btn_mod_capex.setText(tr("\u2705 1. Investimento Inicial (CAPEX)") if "capex" in chk else tr("\u26aa 1. Investimento Inicial (CAPEX)..."))
        self.btn_mod_capex.setStyleSheet(s1 if "capex" in chk else s0)
        self.btn_mod_motobomba.setText(tr("\u2705 2. Motobomba e Custo de Energia") if "motobomba" in chk else tr("\u26aa 2. Motobomba e Custo de Energia..."))
        self.btn_mod_motobomba.setStyleSheet(s1 if "motobomba" in chk else s0)
        self.btn_mod_opex.setText(tr("\u2705 3. Outros Custos Operacionais") if "opex" in chk else tr("\u26aa 3. Outros Custos Operacionais..."))
        self.btn_mod_opex.setStyleSheet(s1 if "opex" in chk else s0)
        self.btn_mod_tariffs.setText(tr("✅ 4. Tarifas de Água e Esgoto") if "tariffs" in chk else tr("⚪ 4. Tarifas de Água e Esgoto..."))
        self.btn_mod_tariffs.setStyleSheet(s1 if "tariffs" in chk else s0)
        count = len(chk)
        if count < 4:
            self.lbl_verification_status.setText(f"{tr('Status: Verifique as 4 etapas de custos para liberar o calculo')} ({count}/4 {tr('verificadas')})")
            self.lbl_verification_status.setStyleSheet(
                "color: #fecaca; font-weight: bold; background-color: #3f1d1d; border: 1px solid #991b1b; padding: 6px 12px; border-radius: 6px; font-size: 11px;"
                if is_dark else
                "color: #b91c1c; font-weight: bold; background-color: #fef2f2; border: 1px solid #fca5a5; padding: 6px 12px; border-radius: 6px; font-size: 11px;"
            )
        else:
            self.lbl_verification_status.setText(tr("Status: Todas as 4 etapas de custos foram verificadas! Analise Economica liberada."))
            self.lbl_verification_status.setStyleSheet(
                "color: #86efac; font-weight: bold; background-color: #143624; border: 1px solid #166534; padding: 6px 12px; border-radius: 6px; font-size: 11px;"
                if is_dark else
                "color: #15803d; font-weight: bold; background-color: #f0fdf4; border: 1px solid #86efac; padding: 6px 12px; border-radius: 6px; font-size: 11px;"
            )

    def _get_config(self):
        from netuno.core.parser import NetunoConfig
        main_win = self.window()
        if main_win and hasattr(main_win, "config"):
            return main_win.config
        if not hasattr(self, "_internal_config"):
            self._internal_config = NetunoConfig()
        return self._internal_config

    def on_open_capex_dialog(self):
        from netuno.ui.dialogs import DialogInitialCosts
        from netuno.core.simulation import build_sweep_volume_grid
        cfg = self._get_config()
        evaluated_volumes = []
        if self.last_sweep_result and getattr(self.last_sweep_result, "results_by_volume", None):
            evaluated_volumes = [r.lower_tank_vol for r in self.last_sweep_result.results_by_volume]
        else:
            try:
                s_max = parse_float(self.txt_sweep_max.text(), 10000.0)
                s_step = parse_float(self.txt_sweep_step.text(), 250.0)
                if s_max > 0 and s_step > 0:
                    evaluated_volumes = build_sweep_volume_grid(s_max, s_step).volumes_l
            except Exception:
                pass
            if not evaluated_volumes and self.last_single_result:
                cfg.econ_lower_tank_vol = self.last_single_result.lower_tank_vol
                evaluated_volumes = [self.last_single_result.lower_tank_vol]
        up_mode = self.combo_upper_mode.currentIndex()
        cfg.upper_tank_used = 1 if up_mode != 2 else 0
        try:
            cfg.upper_tank_vol = float(self.txt_upper_vol.text().replace(",", "."))
        except ValueError:
            cfg.upper_tank_vol = 500.0
        dlg = DialogInitialCosts(self, config=cfg, evaluated_volumes=evaluated_volumes)
        if dlg.exec():
            self.verified_dialogs.add("capex")
            self.update_dialog_button_styles()
            self._auto_calc()

    def on_open_motobomba_dialog(self):
        from netuno.ui.dialogs import DialogMotobomba
        dlg = DialogMotobomba(self, config=self._get_config())
        if dlg.exec():
            self.verified_dialogs.add("motobomba")
            self.update_dialog_button_styles()
            self._auto_calc()

    def on_open_opex_dialog(self):
        from netuno.ui.dialogs import DialogOtherOpCosts
        cfg = self._get_config()
        dlg = DialogOtherOpCosts(self, op_costs=cfg.op_costs)
        if dlg.exec():
            cfg.op_costs = dlg.op_costs
            self.verified_dialogs.add("opex")
            self.update_dialog_button_styles()
            self._auto_calc()

    def on_open_tariffs_dialog(self):
        from netuno.ui.dialogs import DialogTariffs
        dlg = DialogTariffs(self, config=self._get_config())
        if dlg.exec():
            self.verified_dialogs.add("tariffs")
            self.update_dialog_button_styles()
            self._auto_calc()

    def _auto_calc(self):
        if len(self.verified_dialogs) == 4:
            main_win = self.window()
            if main_win and hasattr(main_win, "tab_economic"):
                main_win.tab_economic.calculate_economics(force=True)

    # ── Simulacao ─────────────────────────────────────────────────────────────
    def get_project_state(self) -> dict:
        """Estado da Etapa 3 que não cabe apenas no modelo numérico global."""
        return {
            "sweep_max": self.txt_sweep_max.text(),
            "sweep_step": self.txt_sweep_step.text(),
            "delta_ideal": self.txt_delta_ideal.text(),
            "threshold_profile": self.combo_threshold_profile.currentIndex(),
            "upper_mode": self.combo_upper_mode.currentIndex(),
            "upper_volume": self.txt_upper_vol.text(),
            "pump_threshold_pct": self.txt_pump_thresh_pct.text(),
            "pump_profile": self.combo_pump_profile.currentIndex(),
            "inflation": self.txt_inflation.text(),
            "inflation_mode": self._inf_mode,
            "inflation_profile": self.combo_inflation_profile.currentIndex(),
            "tma": self.txt_tma.text(),
            "tma_mode": self._tma_mode,
            "tma_profile": self.combo_tma_profile.currentIndex(),
            "analysis_period": self.txt_period.text(),
            "tariff_period": self.txt_readj_period.text(),
            "water_adjustment": self.txt_readj_water.text(),
            "electricity_adjustment": self.txt_readj_elec.text(),
            "tariff_profile": self.combo_tariff_profile.currentIndex(),
            "currency": self.combo_currency.currentIndex(),
            "verified_cost_sections": sorted(self.verified_dialogs),
            "selected_volume_mode": self.selected_volume_mode,
            "custom_selected_volume": self.custom_selected_vol,
        }

    def apply_project_state(self, state: dict, config=None):
        """Restaura os controles da Etapa 3 sem disparar cálculo prematuro."""
        state = state or {}

        def text(name, widget, fallback=""):
            if name in state:
                value = state[name]
            elif config is not None and hasattr(config, name) and state:
                value = getattr(config, name)
            else:
                value = fallback
            widget.blockSignals(True)
            widget.setText(str(value))
            widget.blockSignals(False)

        text("sweep_max", self.txt_sweep_max, "")
        text("sweep_step", self.txt_sweep_step, "")
        text("delta_ideal", self.txt_delta_ideal, "")
        mode = state.get("upper_mode", 2 if not getattr(config, "upper_tank_used", True) else 1)
        self.combo_upper_mode.blockSignals(True)
        self.combo_upper_mode.setCurrentIndex(max(0, min(int(mode), self.combo_upper_mode.count() - 1)))
        self.combo_upper_mode.blockSignals(False)
        text("upper_volume", self.txt_upper_vol, "")
        text("pump_threshold_pct", self.txt_pump_thresh_pct, "")
        text("inflation", self.txt_inflation, getattr(config, "inflation", 0.0))
        text("tma", self.txt_tma, getattr(config, "tma", 0.0))
        text("analysis_period", self.txt_period, getattr(config, "analysis_period_years", 20))
        text("tariff_period", self.txt_readj_period, getattr(config, "tariff_escalation", 12))
        text("water_adjustment", self.txt_readj_water, getattr(config, "water_tariff_escalation", 5.0))
        text("electricity_adjustment", self.txt_readj_elec, getattr(config, "elec_tariff_escalation", 5.0))
        self._inf_mode = state.get("inflation_mode", "year")
        self._tma_mode = state.get("tma_mode", "year")
        self.btn_inf_toggle.setChecked(self._inf_mode == "year")
        self.btn_tma_toggle.setChecked(self._tma_mode == "year")
        self.btn_inf_toggle.setText("% a.a." if self._inf_mode == "year" else "% a.m.")
        self.btn_tma_toggle.setText("% a.a." if self._tma_mode == "year" else "% a.m.")
        for key, combo in [
            ("threshold_profile", self.combo_threshold_profile),
            ("pump_profile", self.combo_pump_profile),
            ("inflation_profile", self.combo_inflation_profile),
            ("tma_profile", self.combo_tma_profile),
            ("tariff_profile", self.combo_tariff_profile),
        ]:
            combo.blockSignals(True)
            combo.setCurrentIndex(max(0, min(int(state.get(key, 0)), combo.count() - 1)))
            combo.blockSignals(False)
        self.combo_currency.blockSignals(True)
        self.combo_currency.setCurrentIndex(max(0, min(int(state.get("currency", 0)), self.combo_currency.count() - 1)))
        self.combo_currency.blockSignals(False)
        self.verified_dialogs = set(state.get("verified_cost_sections", []))
        self.selected_volume_mode = state.get("selected_volume_mode", "sweep")
        self.custom_selected_vol = parse_float(state.get("custom_selected_volume"), 5000.0)
        self.on_param_changed()
        for widget in [self.txt_sweep_max, self.txt_sweep_step, self.txt_delta_ideal]:
            self.check_input_highlight(widget)
        self.check_pump_threshold_highlight()
        for widget in [self.txt_inflation, self.txt_tma, self.txt_period, self.txt_readj_period, self.txt_readj_water, self.txt_readj_elec]:
            self.check_econ_highlight(widget)
        self.update_dialog_button_styles()

    def set_precip_data(self, precip_data):
        self.precip_data = precip_data
        self.auto_fill_sweep_range()

    def on_param_changed(self):
        """Atualiza a parametrização do reservatório superior e sincroniza varredura."""
        if not hasattr(self, "combo_upper_mode") or not hasattr(self, "txt_upper_vol"):
            return

        demand_val = 1200.0
        main_win = self.window()
        if main_win and hasattr(main_win, "tab_building"):
            b_cfg = main_win.tab_building.get_building_config()
            demand_val = b_cfg.get("demand", 200.0) * b_cfg.get("residents", 4.0) * b_cfg.get("share", 0.4)

        upper_mode = self.combo_upper_mode.currentIndex()
        self.txt_upper_vol.blockSignals(True)
        if upper_mode == 0:  # Igual à demanda diária
            self.txt_upper_vol.setReadOnly(True)
            self.txt_upper_vol.setText(f"{demand_val:.0f}")
        elif upper_mode == 2:  # Não utilizar reservatório superior
            self.txt_upper_vol.setReadOnly(True)
            self.txt_upper_vol.setText("0")
        else:  # Customizado
            self.txt_upper_vol.setReadOnly(False)
        self.txt_upper_vol.blockSignals(False)

        self.auto_fill_sweep_range()

    def _queue_hydraulic_refresh(self, *_args):
        """Agenda atualização do balanço hidráulico com debounce para evitar recálculos desnecessários."""
        if self.last_sweep_result is None or self.precip_data is None or len(self.precip_data) == 0:
            return
        self._hydraulic_refresh_timer.start()

    def _refresh_hydraulic_results(self):
        """Reexecuta silenciosamente a simulação hidráulica quando os parâmetros forem válidos."""
        required = (self.txt_sweep_max, self.txt_sweep_step, self.txt_delta_ideal)
        if any(not widget.text().strip() or widget.text().strip() == "-" or
               not self.is_valid_number(widget.text()) for widget in required):
            return
        if not self.is_valid_pump_threshold(self.txt_pump_thresh_pct.text().strip()):
            return

        sweep_max = parse_float(self.txt_sweep_max.text(), 0.0)
        sweep_step = parse_float(self.txt_sweep_step.text(), 0.0)
        if sweep_step <= 0 or sweep_max <= 0:
            return

        # Executa mantendo a modalidade ativa (técnica ou completa) sem diálogos intrusivos
        self.run_simulation(force=False, is_technical_only=self._is_technical_only)

    def _calculate_suggested_sweep(self, building: dict, sdii_mm_day: float):
        """Calcula de forma consistente o volume máximo de varredura e passo."""
        tot_demand = building.get("demand", 200.0) * building.get("residents", 4.0)
        share = building.get("share", 0.40)
        share_dec = (share / 100.0) if share > 1.0 else share
        pluvial_demand_day = tot_demand * max(0.0, min(1.0, share_dec))

        if building.get("demand_mode") == "weekly" and building.get("weekly_demands"):
            w_d = building["weekly_demands"]
            w_r = building.get("weekly_residents", [4.0]*7)
            w_s = [((s/100.0) if s > 1.0 else s) for s in building.get("weekly_shares", [0.4]*7)]
            pluvial_demand_day = sum(w_d[i] * w_r[i] * w_s[i] for i in range(len(w_d))) / len(w_d)
        elif building.get("demand_mode") == "monthly" and building.get("monthly_demands"):
            m_d = building["monthly_demands"]
            m_r = building.get("monthly_residents", [4.0]*12)
            m_s = [((s/100.0) if s > 1.0 else s) for s in building.get("monthly_shares", [0.4]*12)]
            pluvial_demand_day = sum(m_d[i] * m_r[i] * m_s[i] for i in range(len(m_d))) / len(m_d)

        # Autonomia em dias modulada pelo SDII:
        autonomy_days = 15.0 + min(20.0, 1.0 * sdii_mm_day)
        sweep_from_demand = pluvial_demand_day * autonomy_days

        # Oferta pluvial captável por ciclo de eventos de chuva
        sweep_from_catchment = min(8.0, 3.0 + 0.3 * sdii_mm_day) * sdii_mm_day * building.get("area", 100.0) * building.get("runoff", 0.8)

        # Se houver reservatório superior configurado
        try:
            upper_vol = float(self.txt_upper_vol.text().replace(',', '.'))
        except Exception:
            upper_vol = 0.0
        sweep_from_upper = upper_vol * 10.0 if self.combo_upper_mode.currentIndex() != 2 else 0.0

        if pluvial_demand_day > 0:
            raw_sweep_max_l = max(sweep_from_demand, min(sweep_from_catchment, sweep_from_demand * 1.8), sweep_from_upper)
        else:
            raw_sweep_max_l = max(sweep_from_catchment, 5000.0)

        sweep_max_l = max(SWEEP_STEP_QUANTUM_L, int(round(raw_sweep_max_l / SWEEP_STEP_QUANTUM_L)) * SWEEP_STEP_QUANTUM_L)
        grid_plan = build_sweep_volume_grid(sweep_max_l, SWEEP_STEP_QUANTUM_L)
        sweep_step_l = grid_plan.effective_step_l

        return {
            "pluvial_demand_day": pluvial_demand_day,
            "autonomy_days": autonomy_days,
            "raw_sweep_max_l": raw_sweep_max_l,
            "sweep_max_l": sweep_max_l,
            "sweep_step_l": sweep_step_l,
            "grid_plan": grid_plan,
            "positive_volume_count": grid_plan.positive_volume_count,
        }

    def suggest_sweep_parameters(self):
        """Preenche referências opcionais e editáveis de varredura."""
        if self.precip_data is None or len(self.precip_data) == 0:
            main_win = self.window()
            if main_win and hasattr(main_win, "tab_project"):
                self.precip_data = getattr(main_win.tab_project, "precip_data", None)
        if self.precip_data is None or len(self.precip_data) == 0:
            QMessageBox.warning(self, tr("Aviso"), tr("Carregue um arquivo de precipitacao na Etapa 1 antes de solicitar a sugestao."))
            return

        main_win = self.window()
        building = None
        if main_win and hasattr(main_win, "tab_building"):
            building = main_win.tab_building.get_building_config()
        if not building:
            QMessageBox.warning(self, tr("Aviso"), tr("Preencha os dados da edificacao na Etapa 2 antes de solicitar a sugestao."))
            return

        sdii_mm_day = 0.0
        project_tab = getattr(main_win, "tab_project", None) if main_win else None
        indices = getattr(project_tab, "climate_indices_df", None)
        try:
            values = [float(value) for value in indices["SDII"].dropna().tolist()]
            sdii_mm_day = sum(values) / len(values) if values else 0.0
        except Exception:
            wet_days = [float(value) for value in self.precip_data if float(value) >= 1.0]
            sdii_mm_day = sum(wet_days) / len(wet_days) if wet_days else 0.0
        if sdii_mm_day <= 0:
            QMessageBox.warning(self, tr("Aviso"), tr("A serie de chuva nao possui dias umidos suficientes para calcular o SDII."))
            return

        res = self._calculate_suggested_sweep(building, sdii_mm_day)
        sweep_max_l = res["sweep_max_l"]
        sweep_step_l = res["sweep_step_l"]

        self._setting_auto_sweep = True
        try:
            self.txt_sweep_max.setText(format_ptbr(sweep_max_l, 0, thousands=False))
            self.txt_sweep_step.setText(format_ptbr(sweep_step_l, 0, thousands=False))
            self._auto_sweep_max_value = sweep_max_l
            self._auto_sweep_step_value = sweep_step_l
        finally:
            self._setting_auto_sweep = False
        # Mantém txt_delta_ideal e txt_pump_thresh_pct em Personalizado com destaque amarelo para o usuário definir
        if not self.txt_delta_ideal.text().strip():
            self.check_input_highlight(self.txt_delta_ideal)
        if not self.txt_pump_thresh_pct.text().strip():
            self.check_pump_threshold_highlight()

        self.lbl_sweep_guidance.setText(
            tr("💡 Sugestão automática: Demanda pluvial de {dem} L/dia ({days:.0f} dias de autonomia com SDII = {sdii} mm/d) | Volume máx: {maximum} L (passo de {step} L, {points} volumes).").format(
                dem=format_ptbr(res["pluvial_demand_day"], 0), days=res["autonomy_days"],
                sdii=format_ptbr(sdii_mm_day, 1), maximum=format_ptbr(sweep_max_l, 0),
                step=format_ptbr(sweep_step_l, 0), points=res["positive_volume_count"],
            )
        )

    def _on_sweep_max_changed(self):
        if not self._setting_auto_sweep:
            self._auto_sweep_max_value = None

    def _on_sweep_step_changed(self):
        if not self._setting_auto_sweep:
            self._auto_sweep_step_value = None

    def _apply_sweep_grid_policy(self, announce=True):
        """Normalize the editable grid without turning a valid edit into an error."""
        if self._setting_auto_sweep:
            return None
        if not self.is_valid_number(self.txt_sweep_max.text()) or not self.is_valid_number(self.txt_sweep_step.text()):
            return None

        maximum_l = parse_float(self.txt_sweep_max.text(), 0.0)
        requested_step_l = parse_float(self.txt_sweep_step.text(), 0.0)
        grid_plan = build_sweep_volume_grid(maximum_l, requested_step_l)
        if grid_plan.step_adjusted:
            self._setting_auto_sweep = True
            try:
                self.txt_sweep_step.setText(format_ptbr(grid_plan.effective_step_l, 0, thousands=False))
                self._auto_sweep_step_value = grid_plan.effective_step_l
            finally:
                self._setting_auto_sweep = False
            self.check_input_highlight(self.txt_sweep_step)
            if announce:
                self.lbl_sweep_guidance.setText(
                    tr("Passo ajustado de {requested} L para {effective} L ({points} volumes positivos, além de 0 L). Volume máximo de {maximum} L preservado.").format(
                        requested=format_ptbr(requested_step_l, 0),
                        effective=format_ptbr(grid_plan.effective_step_l, 0),
                        points=grid_plan.positive_volume_count,
                        maximum=format_ptbr(maximum_l, 0),
                    )
                )
        elif announce:
            self.lbl_sweep_guidance.setText(
                tr("Grade válida: passo efetivo de {effective} L ({points} volumes positivos, além de 0 L). Volume máximo de {maximum} L.").format(
                    effective=format_ptbr(grid_plan.effective_step_l, 0),
                    points=grid_plan.positive_volume_count,
                    maximum=format_ptbr(maximum_l, 0),
                )
            )
        return grid_plan

    def auto_fill_sweep_range(self):
        """Fill only blank or previously auto-generated sweep fields."""
        main_win = self.window()
        if self.precip_data is None or len(self.precip_data) == 0:
            if main_win and hasattr(main_win, "tab_project"):
                self.precip_data = getattr(main_win.tab_project, "precip_data", None)
        if self.precip_data is None or len(self.precip_data) == 0:
            return False
        if not main_win or not hasattr(main_win, "tab_building"):
            return False
        building_tab = main_win.tab_building
        if not self.is_valid_number(building_tab.txt_area.text()):
            return False
        building = building_tab.get_building_config()
        project_tab = getattr(main_win, "tab_project", None)
        indices = getattr(project_tab, "climate_indices_df", None)
        try:
            values = [float(value) for value in indices["SDII"].dropna().tolist()]
            sdii_mm_day = sum(values) / len(values) if values else 0.0
        except Exception:
            wet_days = [float(value) for value in self.precip_data if float(value) >= 1.0]
            sdii_mm_day = sum(wet_days) / len(wet_days) if wet_days else 0.0
        if sdii_mm_day <= 0:
            return False

        res = self._calculate_suggested_sweep(building, sdii_mm_day)
        max_l = res["sweep_max_l"]
        step_l = res["sweep_step_l"]

        max_blank = not self.is_valid_number(self.txt_sweep_max.text())
        step_blank = not self.is_valid_number(self.txt_sweep_step.text())
        if not (max_blank or step_blank or self._auto_sweep_max_value is not None or self._auto_sweep_step_value is not None):
            return False

        active_max_l = max_l if max_blank or self._auto_sweep_max_value is not None else parse_float(self.txt_sweep_max.text(), max_l)
        requested_step_l = SWEEP_STEP_QUANTUM_L if step_blank or self._auto_sweep_step_value is not None else parse_float(self.txt_sweep_step.text(), SWEEP_STEP_QUANTUM_L)
        grid_plan = build_sweep_volume_grid(active_max_l, requested_step_l)
        step_l = grid_plan.effective_step_l

        self._setting_auto_sweep = True
        updated_max = False
        updated_step = False
        try:
            if max_blank or self._auto_sweep_max_value is not None:
                self.txt_sweep_max.setText(format_ptbr(max_l, 0, thousands=False))
                self._auto_sweep_max_value = max_l
                updated_max = True
            if step_blank or self._auto_sweep_step_value is not None:
                self.txt_sweep_step.setText(format_ptbr(step_l, 0, thousands=False))
                self._auto_sweep_step_value = step_l
                updated_step = True
        finally:
            self._setting_auto_sweep = False

        if updated_max:
            self.lbl_sweep_guidance.setText(
                tr("💡 Sugestão automática: Demanda pluvial de {dem} L/dia ({days:.0f} dias de autonomia com SDII = {sdii} mm/d) | Volume máx: {maximum} L (passo de {step} L, {points} volumes).").format(
                    dem=format_ptbr(res["pluvial_demand_day"], 0), days=res["autonomy_days"],
                    sdii=format_ptbr(sdii_mm_day, 1), maximum=format_ptbr(max_l, 0),
                    step=format_ptbr(step_l, 0), points=res["positive_volume_count"],
                )
            )
        elif updated_step:
            self.lbl_sweep_guidance.setText(tr("Passo de varredura preenchido automaticamente; o limite manual foi preservado."))
        return True

    def run_technical_simulation(self):
        """Executa exclusivamente a varredura técnica hidráulica (Etapas 1 a 4)."""
        self.run_simulation(force=True, is_technical_only=True)

    def run_complete_simulation(self):
        """Executa a varredura completa (hidráulica, econômica e ambiental)."""
        self.run_simulation(force=True, is_technical_only=False)

    def run_simulation(self, force=True, is_technical_only=False):
        if getattr(self, "_is_simulating", False):
            return
        self._is_simulating = True
        self._hydraulic_refresh_timer.stop()
        self._is_technical_only = is_technical_only
        try:
            if self.precip_data is None or len(self.precip_data) == 0:
                main_win = self.window()
                if main_win and hasattr(main_win, "tab_project") and main_win.tab_project.precip_data is not None:
                    self.precip_data = main_win.tab_project.precip_data
            if self.precip_data is None or len(self.precip_data) == 0:
                if force:
                    QMessageBox.warning(self, tr("Aviso"), tr("Carregue um arquivo de precipitacao na Etapa 1."))
                return

            unfilled = []
            for name, widget, validator in [
                (tr("Volume Maximo"), self.txt_sweep_max, self.is_valid_number),
                (tr("Passo de Varredura"), self.txt_sweep_step, self.is_valid_number),
                (tr("Limiar Threshold"), self.txt_delta_ideal, self.is_valid_number),
                (tr("Limiar Recalque"), self.txt_pump_thresh_pct, self.is_valid_pump_threshold)
            ]:
                val = widget.text().strip()
                if not val or val == "-" or not validator(val):
                    unfilled.append(name)
                    widget.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")
            if unfilled:
                if force:
                    QMessageBox.warning(self, tr("Campos Nao Preenchidos"), tr("Preencha todos os campos destacados em amarelo na Etapa 3."))
                return

            # Valid numerical edits are normalized, not rejected: the step is a
            # 250-L multiple, doubles above 40 positive capacities, and Vmax stays.
            self._apply_sweep_grid_policy(announce=True)

            upper_vol = parse_float(self.txt_upper_vol.text(), 500.0)
            upper_used = (self.combo_upper_mode.currentIndex() != 2)
            pump_thresh_pct = parse_float(self.txt_pump_thresh_pct.text(), 10.0)
            pump_thresh_vol = (upper_vol * (pump_thresh_pct / 100.0)) if upper_used else 0.0
            b_cfg = {"area": 100.0, "demand": 200.0, "residents": 4, "runoff": 0.75, "share": 0.4,
                     "monthly_demands": None, "monthly_residents": None}
            discard_mm = 2.0; start_date_str = "01/01/1980"; discard_mode = 1; discard_days = 7
            main_win = self.window()
            if main_win and hasattr(main_win, "tab_building"):
                b_cfg = main_win.tab_building.get_building_config()
            if main_win and hasattr(main_win, "tab_project"):
                discard_mm = parse_float(main_win.tab_project.txt_discard.text(), 2.0)
                discard_mode = main_win.tab_project.get_discard_mode()
                discard_days = main_win.tab_project.get_discard_days()
                start_date_str = main_win.tab_project.txt_start_date.text()
            area = b_cfg["area"]
            tot_demand = b_cfg["demand"] * b_cfg["residents"]
            sweep_max   = parse_float(self.txt_sweep_max.text(), 10000.0)
            sweep_step  = parse_float(self.txt_sweep_step.text(), 250.0)
            delta_ideal = parse_float(self.txt_delta_ideal.text(), 5.0)
            self.last_sweep_result = run_sweep_simulation(
                precip_data=self.precip_data, lower_tank_max=sweep_max, lower_tank_step=sweep_step,
                area=area, runoff_coeff=b_cfg["runoff"], discard_mm=discard_mm,
                discard_mode=discard_mode, discard_days_interval=discard_days,
                total_demand_per_day=tot_demand, rainwater_share=b_cfg["share"],
                upper_tank_vol=upper_vol if upper_used else 0.0, upper_tank_used=upper_used,
                pumping_threshold=pump_thresh_vol, delta_ideal_threshold=delta_ideal,
                store_daily_details=False,
                start_date_str=start_date_str,
                building_config=b_cfg
            )
            sweep_points = self.last_sweep_result.results_by_volume
            # A seleção exibida na Etapa 4 é o primeiro ponto cuja variação
            # marginal atende ao threshold técnico informado pelo usuário.
            # Todos os pontos continuam disponíveis para o TOPSIS.
            technical_point = next(
                (r for r in sweep_points
                 if r.lower_tank_vol > 0 and r.delta_potential_per_m3 <= delta_ideal),
                sweep_points[-1],
            )
            opt_vol = technical_point.lower_tank_vol
            if self.selected_volume_mode == "custom":
                target_vol = self.custom_selected_vol
            else:
                target_vol = opt_vol
                self.selected_volume_mode = "sweep"
            self._run_single_sim_for_target_volume(
                target_vol, area, b_cfg, discard_mm,
                upper_vol, upper_used, pump_thresh_vol, pump_thresh_pct,
                start_date_str, discard_mode, discard_days
            )

            if force and is_technical_only:
                msg = tr("✅ <b>Varredura Técnica Concluída com Sucesso!</b><br><br>"
                         "O dimensionamento hidráulico e o balanço hídrico diário foram simulados para todos os volumes da grade.<br><br>"
                         "Você já pode visualizar as curvas de potencial de economia, atendimento de demanda e balanço hídrico na <b>Etapa 4 (Resultados Técnicos)</b>.")
                QMessageBox.information(self, tr("Varredura Técnica Concluída"), msg)
            elif force and not is_technical_only:
                msg = tr("✅ <b>Varredura Completa Concluída com Sucesso!</b><br><br>"
                         "A simulação técnica, a modelagem econômico-financeira e a <b>Análise de Ciclo de Vida (ACV Ambiental)</b> foram processadas para todos os volumes da grade.<br><br>"
                         "Os resultados integrados estão disponíveis nas <b>Etapas 4 (Técnico), 5 (Econômico), 6 (Ambiental) e 7 (Decisão TOPSIS)</b>.")
                QMessageBox.information(self, tr("Varredura Completa Concluída"), msg)
        except Exception as e:
            if force:
                QMessageBox.critical(self, tr("Erro na Simulacao"), f"{tr('Falha ao executar simulacao')}:\n{str(e)}")
        finally:
            self._is_simulating = False

    def on_select_threshold_volume(self):
        if not self.last_sweep_result or not self.last_sweep_result.optimal_lower_tank_vol:
            QMessageBox.information(self, tr("Aviso"), tr("Execute a Varredura de Volumes primeiro."))
            return
        self.selected_volume_mode = "threshold"
        self._recalculate_selected_volume(self.last_sweep_result.optimal_lower_tank_vol)

    def on_select_custom_volume(self):
        curr = self.last_single_result.lower_tank_vol if self.last_single_result else 5000.0
        val, ok = QInputDialog.getDouble(
            self, tr("Volume Fixo Customizado"),
            tr("Volume do reservatorio inferior (Litros):"), curr, 100.0, 500000.0, 0
        )
        if ok:
            self.selected_volume_mode = "custom"
            self.custom_selected_vol = val
            self._recalculate_selected_volume(val)

    def _recalculate_selected_volume(self, target_vol=None):
        if target_vol is None:
            target_vol = self.last_single_result.lower_tank_vol if self.last_single_result else 5000.0
        if self.precip_data is None or len(self.precip_data) == 0:
            return
        upper_vol = float(self.txt_upper_vol.text().replace(",", "."))
        upper_used = (self.combo_upper_mode.currentIndex() != 2)
        try:
            pump_thresh_pct = float(self.txt_pump_thresh_pct.text().replace(",", "."))
        except Exception:
            pump_thresh_pct = 10.0
        pump_thresh_vol = (upper_vol * (pump_thresh_pct / 100.0)) if upper_used else 0.0
        b_cfg = {"area": 100.0, "demand": 200.0, "residents": 4, "runoff": 0.75, "share": 0.4,
                 "monthly_demands": None, "monthly_residents": None}
        discard_mm = 2.0; start_date_str = "01/01/1980"; discard_mode = 1; discard_days = 7
        main_win = self.window()
        if main_win and hasattr(main_win, "tab_building"):
            b_cfg = main_win.tab_building.get_building_config()
        if main_win and hasattr(main_win, "tab_project"):
            try:
                discard_mm = float(main_win.tab_project.txt_discard.text().replace(",", "."))
            except Exception:
                discard_mm = 2.0
            discard_mode = main_win.tab_project.get_discard_mode()
            discard_days = main_win.tab_project.get_discard_days()
            start_date_str = main_win.tab_project.txt_start_date.text()
        self._run_single_sim_for_target_volume(
            target_vol, b_cfg["area"], b_cfg, discard_mm,
            upper_vol, upper_used, pump_thresh_vol, pump_thresh_pct,
            start_date_str, discard_mode, discard_days
        )

    def _run_single_sim_for_target_volume(self, target_vol, area, b_cfg, discard_mm,
                                           upper_vol, upper_used, pump_thresh_vol, pump_thresh_pct,
                                           start_date_str, discard_mode=1, discard_days=7):
        is_dark = get_current_theme() == "dark"
        tot_demand = b_cfg["demand"] * b_cfg["residents"]
        self.last_single_result = run_single_simulation(
            precip_data=self.precip_data, lower_tank_vol=target_vol, area=area,
            runoff_coeff=b_cfg["runoff"], discard_mm=discard_mm, discard_mode=discard_mode,
            discard_days_interval=discard_days, total_demand_per_day=tot_demand,
            rainwater_share=b_cfg["share"],
            upper_tank_vol=upper_vol if upper_used else 0.0, upper_tank_used=upper_used,
            pumping_threshold=pump_thresh_vol, store_daily_details=True,
            monthly_demands=b_cfg.get("monthly_demands"),
            monthly_residents=b_cfg.get("monthly_residents"),
            monthly_shares=b_cfg.get("monthly_shares"),
            weekly_demands=b_cfg.get("weekly_demands"),
            weekly_residents=b_cfg.get("weekly_residents"),
            weekly_shares=b_cfg.get("weekly_shares"),
            daily_demands=b_cfg.get("daily_demands"),
            daily_residents=b_cfg.get("daily_residents"),
            daily_shares=b_cfg.get("daily_shares"),
            demand_mode=b_cfg.get("demand_mode", "constant"),
            start_date_str=start_date_str,
            building_config=b_cfg
        )
        if self.selected_volume_mode == "sweep":
            self.lbl_selected_vol_status.setText(
                f"\u2713 {len(self.last_sweep_result.results_by_volume) if self.last_sweep_result else 0} volumes disponíveis para avaliação; decisão final no TOPSIS."
            )
            self.lbl_selected_vol_status.setStyleSheet("font-size: 12px; font-weight: bold; color: #059669;")
        else:
            self.lbl_selected_vol_status.setText(
                f"\u2713 Volume: {format_ptbr(target_vol, 0)} L ({tr('Volume Fixo Personalizado')})"
            )
            self.lbl_selected_vol_status.setStyleSheet(
                f"font-size: 12px; font-weight: bold; color: {'#ffffff' if is_dark else '#0284c7'};"
            )
        self.simulation_completed.emit(self.last_single_result, self.last_sweep_result)

    def open_pump_wizard(self):
        from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
        upper_v = parse_float(self.txt_upper_vol.text(), 500.0)
        sw_vols = [1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000]
        try:
            v_start = parse_float(self.txt_vol_start.text(), 1000.0)
            v_end   = parse_float(self.txt_vol_end.text(), 10000.0)
            v_step  = parse_float(self.txt_vol_step.text(), 1000.0)
            sw_vols = [v_start + i * v_step for i in range(int((v_end - v_start) / max(1.0, v_step)) + 1)]
        except Exception:
            pass
        dialog = PumpSelectionWizardDialog(upper_tank_vol=upper_v, sweep_volumes=sw_vols, parent=self)
        if dialog.exec_():
            data = dialog.selected_pump_data
            if data:
                main_win = self.window()
                if main_win and hasattr(main_win, "config"):
                    main_win.config.pump_power_kw  = data["kw"]
                    main_win.config.pump_flow_rate = data["flow_lh"]
                    main_win.config.pump_unit_cost = data["cost"]
                    main_win.config.upper_tank_vol = data["upper_vol"]
                    # O rendimento e a altura manométrica eram calculados pelo
                    # assistente e descartados aqui. Sem eles, a emissão e o custo
                    # de bombeamento ignoravam o desnível informado pelo usuário.
                    if data.get("efficiency"):
                        main_win.config.pump_efficiency = float(data["efficiency"])
                    if data.get("manometric_head_m"):
                        main_win.config.pump_manometric_head_m = float(data["manometric_head_m"])
                    if hasattr(main_win.config, "update_pump_pipes") and "suction_dn" in data and "recalque_dn" in data:
                        main_win.config.update_pump_pipes(
                            data["suction_dn"], data["recalque_dn"],
                            data.get("suction_len", 5.0), data.get("recalque_len", 20.0)
                        )
                self.txt_upper_vol.setText(str(data["upper_vol"]))
                QMessageBox.information(self, tr("Motobomba Selecionada"),
                    tr(f"Motobomba selecionada com sucesso!\n"
                       f"Potencia: {data['kw']:.3f} kW | Vazao: {data['flow_lh']:.0f} L/h\n"
                       f"Altura manometrica: {data.get('manometric_head_m', 0):.1f} mca | "
                       f"Rendimento: {data.get('efficiency', 0):.0f}%\n"
                       f"Custo: R$ {data['cost']:.2f} | Vol. Sup.: {data['upper_vol']:.0f} L"))
                self.on_param_changed()
