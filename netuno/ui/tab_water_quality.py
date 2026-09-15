"""
Etapa 3: Qualidade da Água & Linha de Tratamento da ETAP (Netuno 5).
Integra o modelo físico de lavagem de primeira chuva (wash-off), diretrizes da NBR 15527 / NBR 16783,
dimensionamento paramétrico de filtros autolimpantes, dosagem de cloro, reatores UV e filtros de polimento.
"""

from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame, QScrollArea,
    QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor

from netuno.ui.translation import tr, get_current_theme
from netuno.core.parser import NetunoConfig, parse_float, format_ptbr
from netuno.core.water_quality import (
    calculate_first_flush_washoff, size_etap, size_first_flush_system,
    WATER_QUALITY_CLASSES, FirstFlushAnalysis, FirstFlushSizingResult
)
from netuno.core.etap_integration import volume_pluvial_anual_m3


class TabWaterQuality(QWidget):
    water_quality_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.config: NetunoConfig = getattr(parent, 'config', NetunoConfig())
        self.init_ui()

    def init_ui(self):
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setContentsMargins(40, 34, 40, 40)
        lay.setSpacing(16)

        is_dark = get_current_theme() == "dark"
        text_color = "#48d5b7" if is_dark else "#087f6b"
        card_bg = "#1e293b" if is_dark else "#f8fafc"
        card_border = "#334155" if is_dark else "#cbd5e1"
        sub_text_color = "#94a3b8" if is_dark else "#64748b"

        # ── HEADER DA ABA ──
        lbl_title = QLabel(tr("Qualidade da água e linha de tratamento"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        lay.addWidget(lbl_title)

        lbl_desc = QLabel(tr(
            "Análise do impacto físico do descarte de primeira chuva (wash-off), metas normativas da ABNT NBR 15527:2019 / NBR 16783 "
            "e dimensionamento paramétrico de filtros mecânicos, desinfecção e polimento."
        ))
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"font-size: 11.5px; color: {sub_text_color}; margin-bottom: 4px;")
        lay.addWidget(lbl_desc)

        # ── SEÇÃO A: DESCARTE INICIAL & MODELO DE LAVAGEM (FIRST FLUSH WASH-OFF) ──
        gb_ff = QGroupBox(tr("🌧️ A. Descarte de Primeira Chuva (First Flush) e Eficiência de Limpeza"))
        gb_ff.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_ff = QVBoxLayout(gb_ff)
        lay_ff.setSpacing(10)

        row_ff_input = QHBoxLayout()
        self.lbl_discard_info = QLabel()
        self.lbl_discard_info.setStyleSheet(
            f"font-size: 12.5px; font-weight: bold; color: {'#38bdf8' if is_dark else '#0284c7'}; "
            f"background-color: {'#1e293b' if is_dark else '#e0f2fe'}; padding: 5px 12px; border-radius: 6px;"
        )
        row_ff_input.addWidget(self.lbl_discard_info)

        lbl_unit_info = QLabel(tr("(Parâmetro unificado na Etapa 1: Projeto e Chuva · 1,0 mm = 1,0 L descartado por m² de telhado)"))
        lbl_unit_info.setStyleSheet(f"font-size: 11px; color: {sub_text_color};")
        row_ff_input.addWidget(lbl_unit_info)
        row_ff_input.addStretch()
        lay_ff.addLayout(row_ff_input)

        # Cards com Indicadores da Limpeza
        grid_cards = QGridLayout()
        grid_cards.setSpacing(10)

        self.card_vol_disc = self._create_metric_card(tr("Volume Descartado Estimado"), "-- m³/ano", "#0284c7")
        self.card_rem_solids = self._create_metric_card(tr("Remoção Sólidos Grosseiros"), "-- %", "#059669")
        self.card_rem_turb = self._create_metric_card(tr("Remoção Turbidez / Fuligem"), "-- %", "#059669")
        self.card_rem_bact = self._create_metric_card(tr("Remoção Carga Bacteriológica"), "-- %", "#059669")

        grid_cards.addWidget(self.card_vol_disc, 0, 0)
        grid_cards.addWidget(self.card_rem_solids, 0, 1)
        grid_cards.addWidget(self.card_rem_turb, 0, 2)
        grid_cards.addWidget(self.card_rem_bact, 0, 3)
        lay_ff.addLayout(grid_cards)

        # Card de Diagnóstico Físico
        self.frame_ff_diag = QFrame()
        self.frame_ff_diag.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        lay_diag = QVBoxLayout(self.frame_ff_diag)
        lay_diag.setSpacing(4)
        self.lbl_diag_class = QLabel("<b>Classificação:</b> --")
        self.lbl_diag_text = QLabel("--")
        self.lbl_diag_text.setWordWrap(True)
        self.lbl_diag_text.setStyleSheet(f"font-size: 11px; color: {sub_text_color};")
        lay_diag.addWidget(self.lbl_diag_class)
        lay_diag.addWidget(self.lbl_diag_text)
        lay_ff.addWidget(self.frame_ff_diag)

        lay.addWidget(gb_ff)

        # ── SEÇÃO A.1: DIMENSIONAMENTO E ORÇAMENTO DO SISTEMA DE DESCARTE E GRADEAMENTO ──
        gb_ff_sys = QGroupBox(tr("🌧️ A.1. Dimensionamento e Orçamento do Sistema Físico de Descarte (First Flush)"))
        gb_ff_sys.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_ff_sys = QVBoxLayout(gb_ff_sys)
        lay_ff_sys.setSpacing(10)

        row_chk = QHBoxLayout()
        self.chk_ff_enabled = QCheckBox(tr("Dimensionar e orçar sistema físico de descarte (Filtro de Folhas/Gradeamento + Reservatório de Descarte)"))
        # Por padrão na interface da ETAP, o dimensionamento físico do descarte vem habilitado
        self.chk_ff_enabled.setChecked(True)
        self.config.first_flush_system_enabled = True
        self.chk_ff_enabled.toggled.connect(self.on_first_flush_toggled)
        self.chk_ff_enabled.setStyleSheet("font-size: 12px; font-weight: bold; color: #0284c7;")
        row_chk.addWidget(self.chk_ff_enabled)
        row_chk.addStretch()
        lay_ff_sys.addLayout(row_chk)

        self.frame_ff_details = QFrame()
        self.frame_ff_details.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        grid_ff = QGridLayout(self.frame_ff_details)
        grid_ff.setSpacing(8)

        # 1. Filtro de Folhas e Gradeamento
        grid_ff.addWidget(QLabel(f"<b>{tr('1. Filtro de Folhas e Gradeamento:')}</b>"), 0, 0)
        self.lbl_ff_filter_desc = QLabel("--")
        self.lbl_ff_filter_desc.setWordWrap(True)
        self.lbl_ff_filter_cost = QLabel("--")
        self.lbl_ff_filter_cost.setStyleSheet("font-weight: bold; color: #0284c7; font-size: 13px;")
        grid_ff.addWidget(self.lbl_ff_filter_desc, 0, 1)
        grid_ff.addWidget(self.lbl_ff_filter_cost, 0, 2)

        # 2. Reservatório de Descarte
        grid_ff.addWidget(QLabel(f"<b>{tr('2. Reservatório de Descarte (V = d × A):')}</b>"), 1, 0)
        self.lbl_ff_tank_desc = QLabel("--")
        self.lbl_ff_tank_desc.setWordWrap(True)
        self.lbl_ff_tank_cost = QLabel("--")
        self.lbl_ff_tank_cost.setStyleSheet("font-weight: bold; color: #0284c7; font-size: 13px;")
        grid_ff.addWidget(self.lbl_ff_tank_desc, 1, 1)
        grid_ff.addWidget(self.lbl_ff_tank_cost, 1, 2)

        # 3. Purga Automática
        grid_ff.addWidget(QLabel(f"<b>{tr('3. Purga Automática Lenta:')}</b>"), 2, 0)
        self.lbl_ff_purge_desc = QLabel("--")
        self.lbl_ff_purge_desc.setWordWrap(True)
        self.lbl_ff_purge_desc.setStyleSheet(f"font-size: 11px; color: {sub_text_color};")
        grid_ff.addWidget(self.lbl_ff_purge_desc, 2, 1, 1, 2)

        # 4. Materiais e Pegada ACV
        grid_ff.addWidget(QLabel(f"<b>{tr('4. Materiais e Fabricação (ACV):')}</b>"), 3, 0)
        self.lbl_ff_materials = QLabel("--")
        self.lbl_ff_materials.setStyleSheet(f"font-size: 11px; color: {sub_text_color};")
        grid_ff.addWidget(self.lbl_ff_materials, 3, 1, 1, 2)

        # 5. Custo Total Descarte
        grid_ff.addWidget(QLabel(f"<b>{tr('Investimento Total do Descarte (CAPEX):')}</b>"), 4, 0)
        self.lbl_ff_total_capex = QLabel("--")
        self.lbl_ff_total_capex.setStyleSheet(f"""
            font-size: 14px; font-weight: bold; color: {'#38bdf8' if is_dark else '#0369a1'};
            background-color: {'#1e293b' if is_dark else '#e0f2fe'};
            padding: 4px 12px; border-radius: 6px;
        """)
        grid_ff.addWidget(self.lbl_ff_total_capex, 4, 1)

        # 6. Banner de Integração
        lbl_ff_integ = QLabel(tr(
            "💡 <b>Integração Multidimensional Automática:</b> O investimento (CAPEX) e a pegada de carbono incorporada deste reservatório "
            "de descarte são somados em todas as etapas do Netuno: Análise Econômica (VPL, Payback, TIR, LCOW), Análise de Ciclo de Vida (ACV) "
            "e Decisão Multicritério (TOPSIS / VIKOR)."
        ))
        lbl_ff_integ.setWordWrap(True)
        lbl_ff_integ.setStyleSheet(f"""
            font-size: 11px;
            color: {'#86efac' if is_dark else '#166534'};
            background-color: {'#14532d' if is_dark else '#f0fdf4'};
            border: 1px solid {'#166534' if is_dark else '#bbf7d0'};
            border-radius: 6px;
            padding: 8px;
            margin-top: 4px;
        """)
        grid_ff.addWidget(lbl_ff_integ, 5, 0, 1, 3)

        lay_ff_sys.addWidget(self.frame_ff_details)
        lay.addWidget(gb_ff_sys)

        # ── SEÇÃO B: USOS FINAIS & LIMITES NORMATIVOS NBR 15527 ──
        gb_uses = QGroupBox(tr("📋 B. Classe de Uso Final e Parâmetros da Qualidade (ABNT NBR 15527)"))
        gb_uses.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_uses = QVBoxLayout(gb_uses)
        lay_uses.setSpacing(10)

        row_class_sel = QHBoxLayout()
        row_class_sel.addWidget(QLabel(f"<b>{tr('Classe de Uso Alvo:')}</b>"))
        self.combo_class = QComboBox()
        self.combo_class.setMinimumWidth(320)
        for class_id, class_info in WATER_QUALITY_CLASSES.items():
            self.combo_class.addItem(tr(class_info.nome), class_id)
        self.combo_class.currentIndexChanged.connect(self.on_class_changed)
        row_class_sel.addWidget(self.combo_class)
        row_class_sel.addStretch()
        lay_uses.addLayout(row_class_sel)

        # Tabela com Parâmetros Normativos
        self.table_limits = QTableWidget()
        self.table_limits.setFixedHeight(75)
        self.table_limits.setColumnCount(5)
        self.table_limits.setHorizontalHeaderLabels([
            tr("Turbidez Máxima"), tr("Cor Aparente"), tr("Faixa de pH"),
            tr("Cloro Residual Livre"), tr("Coliformes Termotolerantes")
        ])
        self.table_limits.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_limits.verticalHeader().setVisible(False)
        self.table_limits.verticalHeader().setDefaultSectionSize(32)
        self.table_limits.setRowCount(1)
        lay_uses.addWidget(self.table_limits)

        lay.addWidget(gb_uses)

        # ── SEÇÃO C: LINHA DE TRATAMENTO PARAMETRIZADA (ETAP) ──
        gb_etap = QGroupBox(tr("⚙️ C. Dimensionamento Paramétrico da Linha de Tratamento (ETAP)"))
        gb_etap.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_etap = QGridLayout(gb_etap)
        lay_etap.setSpacing(10)

        # 1. Filtro Mecânico de Entrada
        lay_etap.addWidget(QLabel(f"<b>{tr('1. Pré-Filtração Mecânica:')}</b>"), 0, 0)
        self.lbl_filter_type = QLabel("--")
        self.lbl_filter_type.setStyleSheet("font-weight: bold; color: #0284c7;")
        lay_etap.addWidget(self.lbl_filter_type, 0, 1)

        # 2. Desinfecção
        lay_etap.addWidget(QLabel(f"<b>{tr('2. Sistema de Desinfecção:')}</b>"), 1, 0)
        self.combo_disinf = QComboBox()
        self.combo_disinf.addItem(tr("Dosador de Pastilhas de Cloro (Hipoclorito)"), "cloro")
        self.combo_disinf.addItem(tr("Reator de Radiação Ultravioleta (UV) Germicida"), "uv")
        self.combo_disinf.addItem(tr("Gerador de Ozônio (O3)"), "ozonio")
        self.combo_disinf.addItem(tr("Nenhum (Sem desinfecção química/física)"), "nenhum")
        self.combo_disinf.currentIndexChanged.connect(self.on_disinfection_changed)
        lay_etap.addWidget(self.combo_disinf, 1, 1)

        # Dose de Cloro (se selecionado)
        self.lbl_cl_dose = QLabel(f"<b>{tr('Dose de Cloro (mg/L):')}</b>")
        self.txt_cl_dose = QLineEdit("")
        self.txt_cl_dose.setPlaceholderText(tr("Ex: 1,5"))
        self.txt_cl_dose.setFixedWidth(70)
        self.txt_cl_dose.textChanged.connect(self.recalculate_all)
        row_cl = QHBoxLayout()
        row_cl.addWidget(self.lbl_cl_dose)
        row_cl.addWidget(self.txt_cl_dose)
        row_cl.addStretch()
        lay_etap.addLayout(row_cl, 2, 1)

        # 3. Filtro de Polimento
        lay_etap.addWidget(QLabel(f"<b>{tr('3. Polimento Físico:')}</b>"), 3, 0)
        self.chk_polishing = QCheckBox(tr("Incluir Filtro de Polimento Fino (Carvão Ativado / Areia Multicamada)"))
        self.chk_polishing.setChecked(False)   # padrão: não utilizar
        self.chk_polishing.toggled.connect(self.on_polishing_changed)
        lay_etap.addWidget(self.chk_polishing, 3, 1)

        # A classe alvo pode recomendar o polimento. Recomendar é escrever aqui,
        # e não marcar a caixa por conta própria.
        self.lbl_polishing_reco = QLabel("")
        self.lbl_polishing_reco.setWordWrap(True)
        self.lbl_polishing_reco.setStyleSheet("color: #92400e; font-size: 11px;")
        self.lbl_polishing_reco.setVisible(False)
        lay_etap.addWidget(self.lbl_polishing_reco, 4, 1)

        lay.addWidget(gb_etap)

        # ── SEÇÃO C.1: MEMÓRIA DE CÁLCULO DA CLORAÇÃO ──
        self.gb_cl_calc = QGroupBox(tr("🧪 Memória de Cálculo da Desinfecção por Cloração (Hipoclorito de Cálcio)"))
        self.gb_cl_calc.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                color: {text_color};
                background-color: {'#18181b' if is_dark else '#f0fdf4'};
                border: 1.5px solid {'#166534' if is_dark else '#86efac'};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        lay_cl_calc = QGridLayout(self.gb_cl_calc)
        lay_cl_calc.setSpacing(8)

        self.lbl_cl_calc_demand = QLabel("--")
        self.lbl_cl_calc_dose = QLabel("--")
        self.lbl_cl_calc_active = QLabel("--")
        self.lbl_cl_calc_commercial = QLabel("--")
        self.lbl_cl_calc_daily = QLabel("--")
        self.lbl_cl_calc_cost = QLabel("--")
        self.lbl_cl_calc_norm = QLabel("--")

        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Volume Anual Tratado:')}</b>"), 0, 0)
        lay_cl_calc.addWidget(self.lbl_cl_calc_demand, 0, 1)
        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Dosagem de Projeto:')}</b>"), 0, 2)
        lay_cl_calc.addWidget(self.lbl_cl_calc_dose, 0, 3)

        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Massa Cloro Ativo Puro:')}</b>"), 1, 0)
        lay_cl_calc.addWidget(self.lbl_cl_calc_active, 1, 1)
        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Consumo de Pastilhas (65%):')}</b>"), 1, 2)
        lay_cl_calc.addWidget(self.lbl_cl_calc_commercial, 1, 3)

        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Consumo Diário Estimado:')}</b>"), 2, 0)
        lay_cl_calc.addWidget(self.lbl_cl_calc_daily, 2, 1)
        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Custo Químico Anual:')}</b>"), 2, 2)
        lay_cl_calc.addWidget(self.lbl_cl_calc_cost, 2, 3)

        lay_cl_calc.addWidget(QLabel(f"<b>{tr('Enquadramento Normativo:')}</b>"), 3, 0)
        lay_cl_calc.addWidget(self.lbl_cl_calc_norm, 3, 1, 1, 3)

        lay.addWidget(self.gb_cl_calc)

        # ── SEÇÃO D: RESUMO DE CUSTOS E IMPACTO AMBIENTAL DA ETAP ──
        gb_summary = QGroupBox(tr("💰 D. Síntese de Custos (CAPEX/OPEX) e Pegada de Carbono da ETAP"))
        gb_summary.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_sum = QHBoxLayout(gb_summary)
        lay_sum.setSpacing(12)

        self.card_ff_capex = self._create_metric_card(tr("Descarte 1ª Água (CAPEX)"), "R$ --", "#0284c7")
        self.card_etap_capex = self._create_metric_card(tr("Investimento Total ETAP"), "R$ --", "#0d9488")
        self.card_etap_opex = self._create_metric_card(tr("Insumos Anuais (OPEX)"), "R$ --/ano", "#e11d48")
        self.card_etap_co2 = self._create_metric_card(tr("Emissões Anuais Insumos"), "-- kg CO2e/ano", "#059669")

        lay_sum.addWidget(self.card_ff_capex)
        lay_sum.addWidget(self.card_etap_capex)
        lay_sum.addWidget(self.card_etap_opex)
        lay_sum.addWidget(self.card_etap_co2)
        lay.addWidget(gb_summary)

        scroll.setWidget(content)
        main_vbox.addWidget(scroll)

        self.on_class_changed()
        self.on_disinfection_changed()
        self.recalculate_all()

    def on_first_flush_toggled(self):
        enabled = self.chk_ff_enabled.isChecked() if hasattr(self, 'chk_ff_enabled') else True
        self.config.first_flush_system_enabled = enabled
        if hasattr(self, 'frame_ff_details'):
            self.frame_ff_details.setVisible(enabled)
        self.recalculate_all()
        self.water_quality_updated.emit()

    def _create_metric_card(self, title: str, initial_value: str, color_hex: str) -> QFrame:
        is_dark = get_current_theme() == "dark"
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {'#18181b' if is_dark else '#ffffff'};
                border: 1.5px solid {'#3f3f46' if is_dark else '#e2e8f0'};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        v = QVBoxLayout(card)
        v.setContentsMargins(4, 4, 4, 4)
        v.setSpacing(3)
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet(f"font-size: 10.5px; color: {'#a1a1aa' if is_dark else '#64748b'}; font-weight: 500;")
        lbl_v = QLabel(initial_value)
        lbl_v.setObjectName("val_label")
        lbl_v.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color_hex};")
        v.addWidget(lbl_t)
        v.addWidget(lbl_v)
        return card

    def _set_card_value(self, card: QFrame, val_str: str):
        lbl = card.findChild(QLabel, "val_label")
        if lbl:
            lbl.setText(val_str)

    def on_discard_changed(self):
        try:
            val = parse_float(self.txt_discard.text().replace(',', '.'))
            self.config.discard = max(0.0, val)
            self.recalculate_all()
            self.water_quality_updated.emit()
        except Exception:
            pass

    def on_class_changed(self):
        class_id = self.combo_class.currentData() or "classe_1"
        self.config.water_quality_target_class = class_id
        class_obj = WATER_QUALITY_CLASSES.get(class_id, WATER_QUALITY_CLASSES["classe_1"])

        # Atualiza tabela de limites com itens alinhados e protegidos contra edição
        colif_str = "Ausência (0 UFC/100 mL)" if class_obj.coliformes_termo_max_ufc_100ml == 0 else f"≤ {class_obj.coliformes_termo_max_ufc_100ml:.0f} UFC"
        vals = [
            f"≤ {class_obj.turbidez_max_ntu:.1f} NTU",
            f"≤ {class_obj.cor_aparente_max_uh:.0f} uH",
            f"{class_obj.ph_min:.1f} a {class_obj.ph_max:.1f}",
            f"{class_obj.cloro_residual_min_mg_l:.1f} a {class_obj.cloro_residual_max_mg_l:.1f} mg/L",
            colif_str
        ]
        for c_idx, val_txt in enumerate(vals):
            it = QTableWidgetItem(val_txt)
            it.setTextAlignment(Qt.AlignCenter)
            it.setFlags(it.flags() & ~Qt.ItemIsEditable)
            self.table_limits.setItem(0, c_idx, it)

        # A classe NAO marca mais a caixa. Marcar sozinho fazia o polimento
        # parecer obrigatorio, e as classes 2 a 4 sao "adaptada, nao normativa"
        # pelo proprio programa: a recomendacao e dele, e a escolha e do
        # projetista. Recomendacao se apresenta, nao se impoe.
        self._atualizar_recomendacao_de_polimento(class_obj)
        self.config.water_quality_polishing = self.chk_polishing.isChecked()

        self.recalculate_all()
        self.water_quality_updated.emit()

    def _atualizar_recomendacao_de_polimento(self, class_obj):
        """Mostra a recomendação da classe sem tocar na caixa de seleção.

        As classes 2 a 4 são adaptadas e não normativas: a exigência de
        filtração fina é recomendação do programa, e cabe ao projetista aceitá-la
        ou não. Marcar a caixa sozinho fazia a recomendação parecer obrigação.
        """
        if not hasattr(self, "lbl_polishing_reco"):
            return
        recomenda = bool(getattr(class_obj, "exige_filtracao_fina", False))
        self.lbl_polishing_reco.setVisible(recomenda)
        # Limpar o texto, e nao so esconder: um rotulo escondido que guarda a
        # recomendacao da classe anterior mente sobre a classe atual.
        self.lbl_polishing_reco.setText("")
        if recomenda and not self.chk_polishing.isChecked():
            self.lbl_polishing_reco.setText(tr(
                "A classe selecionada recomenda filtração fina. A recomendação é do "
                "programa, e não da NBR 15527:2019 — as classes 2 a 4 são adaptadas. "
                "Sem o filtro, o investimento e o custeio da linha de tratamento não o incluem."
            ))
        elif recomenda:
            self.lbl_polishing_reco.setText(tr(
                "A classe selecionada recomenda filtração fina, e ela está incluída."
            ))

    def on_polishing_changed(self):
        # O campo existia e nunca era escrito: marcar o filtro nao alterava o
        # investimento nem a emissao vistos pelos demais modulos.
        self.config.water_quality_polishing = self.chk_polishing.isChecked()
        classe = WATER_QUALITY_CLASSES.get(
            self.combo_class.currentData() or "classe_1", WATER_QUALITY_CLASSES["classe_1"]
        )
        self._atualizar_recomendacao_de_polimento(classe)
        self.recalculate_all()
        self.water_quality_updated.emit()

    def on_disinfection_changed(self):
        method = self.combo_disinf.currentData() or "cloro"
        self.config.water_quality_disinfection = method
        is_cloro = (method == "cloro")
        self.lbl_cl_dose.setVisible(is_cloro)
        self.txt_cl_dose.setVisible(is_cloro)
        if hasattr(self, 'gb_cl_calc'):
            self.gb_cl_calc.setVisible(is_cloro)
        self.recalculate_all()
        self.water_quality_updated.emit()

    def _simulacao_corrente(self):
        """O resultado da simulação de volume único, quando já houve uma."""
        mw = self.main_window
        if mw is None or not hasattr(mw, 'tab_tanks_simulation'):
            return None
        return getattr(mw.tab_tanks_simulation, 'last_single_result', None)

    def _precipitacao_anual_mm(self, padrao: float = 1500.0) -> float:
        """Precipitação média anual da série carregada.

        Estava fixa em 1.500 mm no cálculo de wash-off, o que fazia o volume
        anual de descarte ser o mesmo em Manaus e em Caxias do Sul.
        """
        mw = self.main_window
        if mw is None or not hasattr(mw, 'tab_tanks_simulation'):
            return padrao
        dados = getattr(mw.tab_tanks_simulation, 'precip_data', None)
        if dados is None or len(dados) == 0:
            return padrao
        try:
            total = float(sum(float(v) for v in dados))
            anos = max(1.0, len(dados) / 365.25)
            media = total / anos
        except (TypeError, ValueError):
            return padrao
        return media if media > 0 else padrao

    def recalculate_all(self):
        # Sincroniza com a Etapa 1 (Projeto e Chuva)
        discard_val = getattr(self.config, 'discard', 1.0)
        if self.main_window and hasattr(self.main_window, 'tab_project') and hasattr(self.main_window.tab_project, 'txt_discard'):
            try:
                discard_val = parse_float(self.main_window.tab_project.txt_discard.text().replace(',', '.'), discard_val)
            except Exception:
                pass
        self.config.discard = max(0.0, discard_val)

        roof_area = getattr(self.config, 'area', 100.0)
        if self.main_window and hasattr(self.main_window, 'tab_building') and hasattr(self.main_window.tab_building, 'txt_area'):
            try:
                roof_area = parse_float(self.main_window.tab_building.txt_area.text().replace(',', '.'), roof_area)
            except Exception:
                pass

        if hasattr(self, 'lbl_discard_info'):
            self.lbl_discard_info.setText(f"💧 {tr('Lâmina de Descarte Configurada:')} {format_ptbr(discard_val, 1)} mm")

        # A precipitacao anual e o volume pluvial saem da simulacao carregada.
        # Estavam fixos em 1.500 mm e 120 m3/ano, de modo que a linha de
        # tratamento era dimensionada para um projeto imaginario.
        sim_result = self._simulacao_corrente()
        precip_anual = self._precipitacao_anual_mm()

        # 1. Análise Wash-off
        ff_res: FirstFlushAnalysis = calculate_first_flush_washoff(
            discard_mm=discard_val,
            roof_area_m2=roof_area,
            annual_precipitation_mm=precip_anual,
            roof_runoff_coeff=getattr(self.config, 'runoff_coeff', COEFICIENTE_DE_ESCOAMENTO_PADRAO),
        )

        self._set_card_value(self.card_vol_disc, f"{ff_res.annual_discard_volume_m3:.1f} m³/ano")
        self._set_card_value(self.card_rem_solids, f"{ff_res.removal_coarse_solids_pct:.1f} %")
        self._set_card_value(self.card_rem_turb, f"{ff_res.removal_turbidity_pct:.1f} %")
        self._set_card_value(self.card_rem_bact, f"{ff_res.removal_bacteria_pct:.1f} %")

        self.lbl_diag_class.setText(f"<b>{tr('Classificação:')}</b> {ff_res.cleanliness_classification} "
                                   f"(Turbidez Bruta Pós-Descarte Estimada: ~{ff_res.estimated_post_discard_turbidity_ntu:.1f} NTU)")
        self.lbl_diag_text.setText(ff_res.recommendation_text)

        # 2. Dimensionamento ETAP
        class_id = self.combo_class.currentData() or "classe_1"
        disinf_method = self.combo_disinf.currentData() or "cloro"
        dose_cl = parse_float(self.txt_cl_dose.text().replace(',', '.'),
                              getattr(self.config, 'chlorine_dose_mg_l', 1.5))
        include_pol = self.chk_polishing.isChecked()

        # A dose digitada aqui e a do projeto: sem esta linha, o economico e a
        # ACV seguiam com a dose padrao enquanto a tela mostrava outra.
        self.config.chlorine_dose_mg_l = max(0.0, dose_cl)
        self.config.water_quality_polishing = include_pol

        # Consumo anual de água pluvial, medido pela simulação quando existe.
        sim_pluv_m3 = volume_pluvial_anual_m3(self.config, sim_result)

        include_ff = self.chk_ff_enabled.isChecked() if hasattr(self, 'chk_ff_enabled') else True
        self.config.first_flush_system_enabled = include_ff

        etap_res = size_etap(
            target_class_id=class_id,
            annual_pluvial_consumed_m3=sim_pluv_m3,
            roof_area_m2=roof_area,
            disinfection_choice=disinf_method,
            include_polishing_filter=include_pol,
            chlorine_dose_mg_l=dose_cl,
            # O preco estava fixo em R$ 38,00/kg enquanto o modulo economico
            # usava `chlorine_cost_per_kg`, de 25,00: a mesma cloracao custava
            # dois valores diferentes no mesmo projeto.
            chlorine_kg_price_brl=getattr(self.config, 'chlorine_cost_per_kg', 25.0),
            chlorine_product_purity=getattr(self.config, 'chlorine_product_purity', 0.65),
            chlorine_co2_kg_per_kg=getattr(self.config, 'chlorine_co2_kg_per_kg', 1.85),
            regional_factor=1.0,
            discard_mm=discard_val,
            include_first_flush=include_ff,
        )

        self.lbl_filter_type.setText(f"{etap_res.pre_filter_type} (Malha {etap_res.pre_filter_mesh_microns} µm)")

        # Atualiza subsistema de descarte físico
        if hasattr(self, 'lbl_ff_filter_desc') and etap_res.first_flush:
            ff = etap_res.first_flush
            self.lbl_ff_filter_desc.setText(ff.leaf_filter_type)
            self.lbl_ff_filter_cost.setText(f"R$ {ff.leaf_filter_capex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            self.lbl_ff_tank_desc.setText(f"{ff.diverter_tank_type} (Volume = {ff.diverter_volume_liters:.0f} L)")
            self.lbl_ff_tank_cost.setText(f"R$ {ff.diverter_tank_capex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            self.lbl_ff_purge_desc.setText(ff.purge_drain_description)
            self.lbl_ff_materials.setText(
                f"{ff.material_description} — Massa total: {ff.diverter_mass_kg + ff.leaf_filter_mass_kg:.1f} kg "
                f"| Carbono de Fabricação: ~{ff.first_flush_embodied_co2_kg:.1f} kg CO2e"
            )
            self.lbl_ff_total_capex.setText(f"R$ {ff.first_flush_total_capex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            if hasattr(self, 'card_ff_capex'):
                self._set_card_value(self.card_ff_capex, f"R$ {ff.first_flush_total_capex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        elif hasattr(self, 'card_ff_capex'):
            self._set_card_value(self.card_ff_capex, "R$ 0,00")

        self._set_card_value(self.card_etap_capex, f"R$ {etap_res.total_etap_capex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        self._set_card_value(self.card_etap_opex, f"R$ {etap_res.total_etap_annual_opex:,.2f}/ano".replace(',', 'X').replace('.', ',').replace('X', '.'))
        self._set_card_value(self.card_etap_co2, f"{etap_res.total_etap_co2e_kg_yr:.1f} kg CO2e/ano")

        # Atualiza a memória de cálculo do cloro
        if hasattr(self, 'gb_cl_calc'):
            is_cloro = (disinf_method == "cloro")
            self.gb_cl_calc.setVisible(is_cloro)
            if is_cloro:
                vol_pluv_m3 = sim_pluv_m3
                vol_pluv_l_dia = (vol_pluv_m3 * 1000.0) / 365.25
                active_kg_yr = (vol_pluv_m3 * dose_cl) / 1000.0
                comm_kg_yr = active_kg_yr / 0.65 if dose_cl > 0 else 0.0
                daily_g_day = (vol_pluv_l_dia * dose_cl) / 1000.0
                cost_yr = comm_kg_yr * 38.0

                self.lbl_cl_calc_demand.setText(f"{vol_pluv_m3:,.1f} m³/ano ({vol_pluv_l_dia:,.0f} L/dia)".replace(',', 'X').replace('.', ',').replace('X', '.'))
                self.lbl_cl_calc_dose.setText(f"{dose_cl:.2f} mg/L (ou g/m³ de Cl₂ ativo)")
                self.lbl_cl_calc_active.setText(f"{active_kg_yr:.3f} kg Cl₂ ativo/ano")
                self.lbl_cl_calc_commercial.setText(f"{comm_kg_yr:.2f} kg pastilhas/ano ({comm_kg_yr*1000/12:.0f} g/mês)")
                self.lbl_cl_calc_daily.setText(f"{daily_g_day:.2f} g Cl₂ ativo/dia")
                self.lbl_cl_calc_cost.setText(f"R$ {cost_yr:,.2f}/ano (base R$ 38,00/kg)".replace(',', 'X').replace('.', ',').replace('X', '.'))
                
                if dose_cl < 0.5:
                    self.lbl_cl_calc_norm.setText(f"<span style='color: #ea580c;'>⚠️ Dosagem baixa (< 0,5 mg/L). Risco de residual livre insuficiente conforme NBR 15527.</span>")
                elif dose_cl <= 2.0:
                    self.lbl_cl_calc_norm.setText(f"<span style='color: #16a34a;'>✅ Atende plenamente à NBR 15527 / NBR 16783 (Residual livre esperado: 0,5 a 2,0 mg/L).</span>")
                else:
                    self.lbl_cl_calc_norm.setText(f"<span style='color: #0284c7;'>ℹ️ Hipercloração (> 2,0 mg/L). Recomendado para desinfecção de choque ou águas com alta matéria orgânica.</span>")

        # Atualiza parâmetros na config
        self.config.chlorine_dose_mg_l = dose_cl
        self.config.chlorine_treatment_enabled = (disinf_method == "cloro")
