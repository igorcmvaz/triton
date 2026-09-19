"""
Aba Integrada de Análise Econômico-Financeira do Netuno 5 (PySide6).
Consolida os indicadores de viabilidade: CAPEX, OPEX, VPL, TIR, Payback Simples/Descontado,
Tabela do Fluxo de Caixa Anual com exportação CSV, e Análise de Sensibilidade em Janela Separada.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QFileDialog, QMessageBox, QFrame, QSizePolicy, QDialog, QComboBox,
    QDoubleSpinBox, QAbstractSpinBox, QCheckBox, QApplication
)
from PySide6.QtCore import Qt, Signal, QLocale
from PySide6.QtGui import QFont, QColor

from netuno.core.taxas import mensal_pct_para_anual_fracao, mensal_pct_para_anual_pct
from netuno.core.parser import NetunoConfig, parse_float, format_ptbr
from netuno.core.economic import (
    run_robust_economic_analysis, EconomicAnalysisResult, calculate_effective_tariff,
    run_sensitivity_analysis
)
from netuno.core.tariff_category import incompatibilidade_de_categoria
from netuno.core.etap_integration import (
    capex_incremental_da_etap,
    opex_anual_incremental_da_etap,
    dimensionar_etap_do_projeto,
)
from netuno.core.cost_estimates import (
    estimate_preliminary_capex, default_maintenance_items,
    MATERIAL_COST_MULTIPLIERS, PIPE_COST_PER_METER, estimate_annual_chlorination_cost,
    annualize_operational_costs,
)
from netuno.ui.charts import SensitivityChart, VplVsVolumeChart
from netuno.ui.translation import tr, get_current_lang, get_current_theme
import csv


class SensitivityMatrixDialog(QDialog):
    """Janela Modal para Exibição Completa da Matriz de Sensibilidade do VPL."""
    def __init__(self, parent=None, table_widget=None):
        super().__init__(parent)
        self.setWindowTitle(tr("📊 Matriz de Sensibilidade Multivariável do VPL"))
        screen = self.screen() or QApplication.primaryScreen()
        target_w, target_h = 1040, 640
        if screen:
            avail = screen.availableGeometry()
            target_w = min(target_w, max(850, int(avail.width() * 0.88)))
            target_h = min(target_h, max(500, int(avail.height() * 0.88)))
        self.resize(target_w, target_h)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        lbl_desc = QLabel(tr("Variação do Valor Presente Líquido (VPL em R$) em função das flutuações de ±15% e ±30% nos parâmetros críticos do projeto:"))
        lbl_desc.setFont(QFont("Segoe UI", 10))
        lbl_desc.setStyleSheet("color: #334155; font-weight: bold;")
        lay.addWidget(lbl_desc)

        if table_widget:
            table_copy = self._clone_table(table_widget)
            lay.addWidget(table_copy, stretch=1)

        btns = QHBoxLayout()
        btns.addStretch()
        btn_close = QPushButton(tr("Fechar Janela"))
        btn_close.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 6px 18px;")
        btn_close.clicked.connect(self.accept)
        btns.addWidget(btn_close)
        lay.addLayout(btns)

    @staticmethod
    def _clone_table(source: QTableWidget) -> QTableWidget:
        clone = QTableWidget(source.rowCount(), source.columnCount())
        clone.setEditTriggers(QTableWidget.NoEditTriggers)
        clone.setAlternatingRowColors(source.alternatingRowColors())

        for col in range(source.columnCount()):
            header_item = source.horizontalHeaderItem(col)
            clone.setHorizontalHeaderItem(
                col,
                QTableWidgetItem(header_item.text() if header_item else ""),
            )
            clone.setColumnWidth(col, source.columnWidth(col))

        for row in range(source.rowCount()):
            clone.setRowHeight(row, source.rowHeight(row))
            for col in range(source.columnCount()):
                source_item = source.item(row, col)
                if source_item is None:
                    continue
                item = QTableWidgetItem(source_item.text())
                item.setTextAlignment(source_item.textAlignment())
                item.setFont(source_item.font())
                item.setForeground(source_item.foreground())
                item.setBackground(source_item.background())
                item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
                clone.setItem(row, col, item)

        clone.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        clone.verticalHeader().setVisible(source.verticalHeader().isVisible())
        return clone


class TabEconomicIntegrated(QWidget):
    """
    Aba Principal da Etapa 5: Otimização Econômico-Financeira e Análise de Viabilidade.
    Evidencia o impacto econômico das escolhas de materiais, tubulações, bomba e cloração.
    """
    economic_calculated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_result = None
        self.last_sweep_econ_results = {}
        self.economic_optimum_volume = None
        self._select_optimum_when_calculated = False
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        heading = "#f4f4f5" if is_dark else "#0f172a"
        muted = "#a1a1aa" if is_dark else "#64748b"
        card_bg = "#27272a" if is_dark else "#ffffff"
        card_border = "#3f3f46" if is_dark else "#cbd5e1"
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 34, 40, 40)
        layout.setSpacing(16)

        # ── CABEÇALHO DA ETAPA 5 ──
        top_bar = QHBoxLayout()
        lbl_title = QLabel(tr("Economia e viabilidade financeira"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 24px; font-weight: 700; color: #133c32;")
        top_bar.addWidget(lbl_title)
        top_bar.addStretch()

        # Seletor de Volume para Análise
        top_bar.addWidget(QLabel(tr("Referência (ótimo econômico):")))
        self.combo_active_volume = QComboBox()
        self.combo_active_volume.setMinimumWidth(160)
        self.combo_active_volume.currentIndexChanged.connect(self._on_active_volume_changed)
        top_bar.addWidget(self.combo_active_volume)

        self.lbl_economic_optimum = QLabel(tr("Ótimo econômico: -- L"))
        self.lbl_economic_optimum.setStyleSheet(f"font-weight: bold; color: {heading};")
        top_bar.addWidget(self.lbl_economic_optimum)

        self.btn_recalc = QPushButton(tr("⚡ Recalcular Indicadores"))
        self.btn_recalc.setProperty("primary", True)
        self.btn_recalc.clicked.connect(self.calculate_economics)
        top_bar.addWidget(self.btn_recalc)

        layout.addLayout(top_bar)

        # ── PAINEL SUPERIOR DE CARDS DE RESUMO FINANCEIRO ──
        self.gb_res = QGroupBox(tr("📊 Indicadores de Viabilidade Econômica"))
        gb_res = self.gb_res
        gb_res.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        lay_r = QHBoxLayout(gb_res)
        lay_r.setSpacing(10)

        def mk_card(title, color):
            frame = QFrame()
            frame.setStyleSheet(f"QFrame {{ background: {card_bg}; border: 1px solid {card_border}; border-top: 3px solid {color}; border-radius: 6px; padding: 6px; }}")
            l = QVBoxLayout(frame)
            l.setContentsMargins(4, 4, 4, 4)
            l.setSpacing(2)
            t = QLabel(title); t.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {muted};"); t.setAlignment(Qt.AlignCenter)
            v = QLabel("--"); v.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {heading};"); v.setAlignment(Qt.AlignCenter)
            l.addWidget(t); l.addWidget(v)
            lay_r.addWidget(frame)
            return v

        self.lbl_val_invest  = mk_card(tr("Investimento Inicial (CAPEX)"),    "#475569")
        self.lbl_val_annual  = mk_card(tr("Economia Bruta (1º Ano)"),          "#059669")
        self.lbl_val_payback = mk_card(tr("Payback Simples / Descontado"),     "#0284c7")
        self.lbl_val_vpl     = mk_card(tr("VPL (Valor Presente Líquido)"),     "#16a34a")
        self.lbl_val_tir     = mk_card(tr("TIR (Taxa Interna Retorno)"),       "#d97706")

        # Aviso de categoria tarifaria incompativel, acima dos indicadores:
        # se a tarifa esta errada, os cinco numeros abaixo estao errados.
        self.lbl_aviso_categoria = QLabel("")
        self.lbl_aviso_categoria.setWordWrap(True)
        self.lbl_aviso_categoria.setStyleSheet(
            "font-size: 11px; color: #7c2d12; background-color: #fef3c7; "
            "border: 1px solid #fbbf24; border-radius: 4px; padding: 6px;"
        )
        self.lbl_aviso_categoria.setVisible(False)
        layout.addWidget(self.lbl_aviso_categoria)

        layout.addWidget(gb_res)

        # ── SUB-ABAS FINANCEIRAS ──
        self.sub_tabs = QTabWidget()

        # ── SUB-ABA 0: IMPACTO DA SELEÇÃO DE MATERIAIS & EQUIPAMENTOS ──
        sub_tab_materials = QWidget()
        lay_mat = QVBoxLayout(sub_tab_materials)
        lay_mat.setSpacing(8)

        # Barra de Configuração Rápida de Materiais
        gb_quick_mat = QGroupBox(tr("⚙️ Configuração de Materiais e Insumos do Sistema"))
        lay_qm = QHBoxLayout(gb_quick_mat)
        lay_qm.setSpacing(12)

        lay_qm.addWidget(QLabel(tr("Cisterna:")))
        self.combo_lower_mat = QComboBox()
        self.combo_lower_mat.addItem(tr("PEAD (Polietileno)"), "PEAD")
        self.combo_lower_mat.addItem(tr("Concreto Armado"), "CONCRETO")
        self.combo_lower_mat.addItem(tr("PRFV (Fibra de Vidro)"), "PRFV")
        self.combo_lower_mat.addItem(tr("Aço Inoxidável"), "ACO_INOX")
        self.combo_lower_mat.currentIndexChanged.connect(self._on_material_selection_changed)
        lay_qm.addWidget(self.combo_lower_mat)

        lay_qm.addWidget(QLabel(tr("Caixa Superior:")))
        self.combo_upper_mat = QComboBox()
        self.combo_upper_mat.addItem(tr("PEAD (Polietileno)"), "PEAD")
        self.combo_upper_mat.addItem(tr("Concreto Armado"), "CONCRETO")
        self.combo_upper_mat.addItem(tr("PRFV (Fibra de Vidro)"), "PRFV")
        self.combo_upper_mat.addItem(tr("Aço Inoxidável"), "ACO_INOX")
        self.combo_upper_mat.currentIndexChanged.connect(self._on_material_selection_changed)
        lay_qm.addWidget(self.combo_upper_mat)

        self.chk_chlorine = QCheckBox(tr("Cloração / Desinfecção"))
        self.chk_chlorine.setChecked(True)
        self.chk_chlorine.toggled.connect(self._on_material_selection_changed)
        lay_qm.addWidget(self.chk_chlorine)

        pt_locale = QLocale(QLocale.Portuguese, QLocale.Brazil)
        lay_qm.addWidget(QLabel(tr("Dose:")))
        self.spin_cl_dose = QDoubleSpinBox()
        self.spin_cl_dose.setLocale(pt_locale)
        self.spin_cl_dose.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_cl_dose.setRange(0.1, 20.0)
        self.spin_cl_dose.setValue(2.0)
        self.spin_cl_dose.setSuffix(" mg/L")
        self.spin_cl_dose.valueChanged.connect(self._on_material_selection_changed)
        lay_qm.addWidget(self.spin_cl_dose)

        self.btn_edit_opex = QPushButton(tr("🛠️ Rotinas de Manutenção (OPEX)..."))
        self.btn_edit_opex.setStyleSheet("font-weight: bold; padding: 4px 10px;")
        self.btn_edit_opex.clicked.connect(self._on_open_opex_dialog)
        lay_qm.addWidget(self.btn_edit_opex)

        lay_qm.addStretch()
        lay_mat.addWidget(gb_quick_mat)

        # Barra de Incentivos Fiscais (IPTU Verde) & Bandeiras Tarifárias ANEEL
        gb_fiscal = QGroupBox(tr("🌿 Incentivos Fiscais (IPTU Verde) & Bandeiras Tarifárias ANEEL"))
        lay_fisc = QHBoxLayout(gb_fiscal)
        lay_fisc.setSpacing(12)

        self.chk_iptu = QCheckBox(tr("Ativar IPTU Verde"))
        self.chk_iptu.toggled.connect(self._on_fiscal_param_changed)
        lay_fisc.addWidget(self.chk_iptu)

        lay_fisc.addWidget(QLabel(tr("IPTU Anual:")))
        self.spin_iptu_val = QDoubleSpinBox()
        self.spin_iptu_val.setLocale(pt_locale)
        self.spin_iptu_val.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_iptu_val.setRange(0.0, 500000.0)
        self.spin_iptu_val.setValue(4000.0)
        self.spin_iptu_val.setPrefix("R$ ")
        self.spin_iptu_val.setEnabled(False)
        self.spin_iptu_val.valueChanged.connect(self._on_fiscal_param_changed)
        lay_fisc.addWidget(self.spin_iptu_val)

        lay_fisc.addWidget(QLabel(tr("Desconto:")))
        self.spin_iptu_disc = QDoubleSpinBox()
        self.spin_iptu_disc.setLocale(pt_locale)
        self.spin_iptu_disc.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_iptu_disc.setRange(0.0, 50.0)
        self.spin_iptu_disc.setValue(5.0)
        self.spin_iptu_disc.setSuffix(" %")
        self.spin_iptu_disc.setEnabled(False)
        self.spin_iptu_disc.valueChanged.connect(self._on_fiscal_param_changed)
        lay_fisc.addWidget(self.spin_iptu_disc)

        self.lbl_iptu_badge = QLabel(tr("(Desativado)"))
        self.lbl_iptu_badge.setStyleSheet("color: #94a3b8; font-style: italic; padding: 2px 6px;")
        lay_fisc.addWidget(self.lbl_iptu_badge)

        lay_fisc.addWidget(QLabel(tr("Regime Elétrico:")))
        self.combo_tariff_flag = QComboBox()
        self.combo_tariff_flag.addItem(tr("🟢 Bandeira Verde (R$ 0,00)"), "verde")
        self.combo_tariff_flag.addItem(tr("🟡 Bandeira Amarela (+R$ 0,019/kWh)"), "amarela")
        self.combo_tariff_flag.addItem(tr("🔴 Vermelha 1 (+R$ 0,045/kWh)"), "vermelha_1")
        self.combo_tariff_flag.addItem(tr("🔴 Vermelha 2 (+R$ 0,079/kWh)"), "vermelha_2")
        self.combo_tariff_flag.addItem(tr("⚪ Tarifa Branca (Otimizada -15%)"), "branca")
        self.combo_tariff_flag.currentIndexChanged.connect(self._on_fiscal_param_changed)
        lay_fisc.addWidget(self.combo_tariff_flag)

        lay_fisc.addStretch()
        lay_mat.addWidget(gb_fiscal)

        # Tabela Detalhada de Impacto
        self.table_mat_impact = QTableWidget()
        self.table_mat_impact.setColumnCount(5)
        self.table_mat_impact.setHorizontalHeaderLabels([
            tr("Componente"), tr("Material / Especificação"), tr("Quantidade / Porte"),
            tr("CAPEX Inicial (R$)"), tr("OPEX Anual (R$/ano)")
        ])
        self.table_mat_impact.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_mat_impact.setMinimumHeight(280)
        lay_mat.addWidget(self.table_mat_impact)
        self.sub_tabs.addTab(sub_tab_materials, tr("🧱 Detalhamento de Materiais & Componentes"))

        # Sub-aba 1: Tabela do Fluxo de Caixa Anual
        sub_tab_cashflow = QWidget()
        lay_cf = QVBoxLayout(sub_tab_cashflow)

        lay_btn_exp = QHBoxLayout()
        lbl_tbl = QLabel(tr("📄 Projeção Detalhada do Fluxo de Caixa Ano a Ano"))
        lbl_tbl.setStyleSheet(f"font-weight: bold; color: {heading};")
        lay_btn_exp.addWidget(lbl_tbl)
        lay_btn_exp.addStretch()

        self.btn_export_csv = QPushButton(tr("📥 Exportar Fluxo de Caixa (CSV / Excel)"))
        self.btn_export_csv.setStyleSheet("font-weight: bold; background-color: #0284c7; color: white; padding: 6px 12px;")
        self.btn_export_csv.clicked.connect(self.export_cash_flow_csv)
        lay_btn_exp.addWidget(self.btn_export_csv)
        lay_cf.addLayout(lay_btn_exp)

        self.table_cashflow = QTableWidget()
        self.table_cashflow.setColumnCount(14)
        self.table_cashflow.setHorizontalHeaderLabels([
            tr("Ano"), tr("Investimento (R$)"), tr("Água Econ. (m³)"), tr("Tarifa Água (R$/m³)"),
            tr("Economia Água (R$)"), tr("Economia Esgoto (R$)"), tr("IPTU Verde (R$)"),
            tr("Econ. Bruta Total (R$)"), tr("Energia Bomba (R$)"), tr("Outros Custos O&M (R$)"),
            tr("Fluxo Líquido (R$)"), tr("Fator Desconto"), tr("Fluxo Descontado (R$)"),
            tr("Fluxo Acumulado (R$)")
        ])
        self.table_cashflow.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        lay_cf.addWidget(self.table_cashflow)
        self.sub_tabs.addTab(sub_tab_cashflow, tr("📊 Tabela de Fluxo de Caixa Anual"))

        # Sub-aba 2: Sensibilidade Multivariável (Gráfico em 100% da largura + Botão para Modal)
        sub_tab_sens = QWidget()
        lay_sens = QVBoxLayout(sub_tab_sens)
        lay_sens.setSpacing(8)

        top_sens_bar = QHBoxLayout()
        lbl_sens_title = QLabel(tr("📉 Análise do Comportamento do VPL frente a Flutuações nos Parâmetros"))
        lbl_sens_title.setStyleSheet(f"font-weight: bold; color: {heading};")
        top_sens_bar.addWidget(lbl_sens_title)
        top_sens_bar.addStretch()

        self.btn_open_matrix = QPushButton(tr("📊 Ver Matriz de Sensibilidade do VPL (Tabela)..."))
        self.btn_open_matrix.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 5px 12px; border-radius: 4px;")
        self.btn_open_matrix.clicked.connect(self.open_sensitivity_matrix_modal)
        top_sens_bar.addWidget(self.btn_open_matrix)
        lay_sens.addLayout(top_sens_bar)

        self.chart_sensitivity = SensitivityChart()
        self.chart_sensitivity.set_canvas_height_range(maximum=400)
        lay_sens.addWidget(self.chart_sensitivity, stretch=1)

        # Tabela interna oculta para ser exibida no Modal ao clicar
        self.table_sens = QTableWidget()
        self.table_sens.setColumnCount(6)
        self.table_sens.setHorizontalHeaderLabels([
            tr("Parâmetro Variado"), "-30%", "-15%", tr("Base (0%)"), "+15%", "+30%"
        ])
        self.table_sens.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for c in range(1, 6):
            self.table_sens.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch)

        self.sub_tabs.addTab(sub_tab_sens, tr("📈 Análise de Sensibilidade Multivariável"))

        # Sub-aba 3: Comparativo de Volumes & Indicadores Financeiros
        sub_tab_vpl_volumes = QWidget()
        lay_vv_main = QVBoxLayout(sub_tab_vpl_volumes)
        lay_vv_main.setContentsMargins(4, 8, 4, 4)
        lay_vv_main.setSpacing(8)

        bar_metric = QHBoxLayout()
        lbl_metric = QLabel(tr("Métrica exibida no gráfico:"))
        lbl_metric.setStyleSheet(f"font-weight: bold; color: {heading};")
        bar_metric.addWidget(lbl_metric)

        self.combo_chart_metric = QComboBox()
        self.combo_chart_metric.addItem(tr("Payback Descontado (anos)"), "payback_discounted")
        self.combo_chart_metric.addItem(tr("Payback Simples (anos)"), "payback_simple")
        self.combo_chart_metric.addItem(tr("VPL Líquido (R$)"), "vpl")
        self.combo_chart_metric.addItem(tr("TIR — Taxa Interna de Retorno (% a.a.)"), "tir")
        self.combo_chart_metric.addItem(tr("Custos Totais (CAPEX, OPEX Acumulado e Total)"), "costs")
        self.combo_chart_metric.addItem(tr("Custos Operacionais Anuais (OPEX R$/ano)"), "opex_annual")
        self.combo_chart_metric.currentIndexChanged.connect(self._on_chart_metric_changed)
        self.combo_chart_metric.setMinimumWidth(260)
        bar_metric.addWidget(self.combo_chart_metric)
        bar_metric.addStretch()
        lay_vv_main.addLayout(bar_metric)

        lay_vv = QHBoxLayout()
        lay_vv.setSpacing(12)

        self.chart_vpl_volume = VplVsVolumeChart()
        self.chart_vpl_volume.set_canvas_height_range(minimum=420)
        lay_vv.addWidget(self.chart_vpl_volume, stretch=3)

        gb_vpl_tbl = QGroupBox(tr("Tabela Comparativa de Indicadores por Volume da Varredura"))
        lay_vt = QVBoxLayout(gb_vpl_tbl)
        lay_vt.setContentsMargins(8, 12, 8, 8)
        self.table_vpl_volumes = QTableWidget()
        self.table_vpl_volumes.setColumnCount(7)
        self.table_vpl_volumes.setHorizontalHeaderLabels([
            tr("Volume (L)"), tr("CAPEX (R$)"), tr("OPEX Anual (R$/ano)"), tr("Economia (m³/ano)"),
            tr("VPL Líquido (R$)"), tr("TIR (% a.a.)"), tr("Payback (anos)")
        ])
        self.table_vpl_volumes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lay_vt.addWidget(self.table_vpl_volumes)
        lay_vv.addWidget(gb_vpl_tbl, stretch=3)
        lay_vv_main.addLayout(lay_vv, stretch=1)
        self.sub_tabs.addTab(sub_tab_vpl_volumes, tr("📈 Comparativo de Volumes && Indicadores"))

        layout.addWidget(self.sub_tabs, stretch=1)
        self.setLayout(layout)
        self.clear_economic_outputs()

    def _on_chart_metric_changed(self):
        if hasattr(self, "last_sweep_econ_results") and self.last_sweep_econ_results:
            metric = self.combo_chart_metric.currentData() or "payback_discounted"
            curr_sym = self.get_currency_symbol()
            main_win = self.window()
            opt_tech_vol = None
            if main_win and hasattr(main_win, "tab_tanks_simulation"):
                sw_tech = main_win.tab_tanks_simulation.last_sweep_result
                if sw_tech:
                    opt_tech_vol = getattr(sw_tech, "optimal_lower_tank_vol", None)
            cfg = getattr(main_win, "config", None) if main_win else None
            tma_r = mensal_pct_para_anual_pct(cfg.tma) if cfg else 8.0
            self.chart_vpl_volume.update_chart(
                self.last_sweep_econ_results,
                metric=metric,
                currency_symbol=curr_sym,
                optimal_tech_vol=opt_tech_vol,
                tma_rate=tma_r
            )

    def open_sensitivity_matrix_modal(self):
        """Abre o diálogo modal contendo a matriz de sensibilidade detalhada."""
        dlg = SensitivityMatrixDialog(parent=self, table_widget=self.table_sens)
        dlg.exec()

    def get_currency_symbol(self):
        main_win = self.window()
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            return main_win.tab_tanks_simulation.get_currency_symbol()
        return "R$"

    def get_netuno_config(self):
        main_win = self.window()
        cfg = getattr(main_win, "config", None) or NetunoConfig()

        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            ts = main_win.tab_tanks_simulation
            try:
                # O projeto grava a TMA e a inflação em % ao mês. Gravar aqui a
                # taxa anual fazia o arquivo salvo guardar um valor anual sob a
                # chave «tma_monthly_pct».
                cfg.tma       = ts.get_tma_monthly_pct()
                cfg.inflation = ts.get_inflation_monthly_pct()
                cfg.analysis_period_years = int(parse_float(ts.txt_period.text(), 20.0))
                cfg.tariff_escalation         = parse_float(ts.txt_readj_period.text(), 12.0)
                cfg.water_tariff_escalation   = parse_float(ts.txt_readj_water.text(), 5.0)
                cfg.sewage_tariff_escalation  = cfg.water_tariff_escalation
                cfg.elec_tariff_escalation    = parse_float(ts.txt_readj_elec.text(), 6.0)
            except Exception:
                pass

        vol_used   = cfg.econ_lower_tank_vol if cfg.econ_lower_tank_vol > 0 else 4000.0
        upper_used = bool(getattr(cfg, "upper_tank_used", 1))
        low_mat = self.combo_lower_mat.currentData() if hasattr(self, "combo_lower_mat") else getattr(cfg, "lower_tank_material", "PEAD")
        up_mat = self.combo_upper_mat.currentData() if hasattr(self, "combo_upper_mat") else getattr(cfg, "upper_tank_material", "PEAD")
        
        estimates  = estimate_preliminary_capex(
            vol_used, getattr(cfg, "upper_tank_vol", 500.0), upper_used,
            cfg.pump_power_kw, cfg.pump_count,
            lower_material=low_mat, upper_material=up_mat
        )
        if cfg.cost_lower_tank  <= 0: cfg.cost_lower_tank  = estimates["lower"]
        if cfg.cost_upper_tank  <= 0: cfg.cost_upper_tank  = estimates["upper"]
        if cfg.cost_piping      <= 0: cfg.cost_piping      = estimates["piping"]
        if cfg.cost_accessories <= 0: cfg.cost_accessories = estimates["accessories"]
        if cfg.cost_labor       <= 0: cfg.cost_labor       = estimates["labor"]
        if cfg.pump_unit_cost   <= 0: cfg.pump_unit_cost   = estimates["pump_unit"]
        if not cfg.op_costs:
            cfg.op_costs = default_maintenance_items(upper_used)

        if hasattr(self, "chk_iptu"):
            cfg.iptu_green_enabled = self.chk_iptu.isChecked()
            cfg.iptu_annual_value = self.spin_iptu_val.value()
            cfg.iptu_discount_pct = self.spin_iptu_disc.value()
        if hasattr(self, "combo_tariff_flag"):
            cfg.tariff_flag = self.combo_tariff_flag.currentData() or "verde"

        return cfg

    def clear_economic_outputs(self):
        for attr in ["lbl_val_invest", "lbl_val_annual", "lbl_val_payback", "lbl_val_vpl", "lbl_val_tir"]:
            if hasattr(self, attr):
                getattr(self, attr).setText("--")
        if hasattr(self, "lbl_economic_optimum"):
            self.lbl_economic_optimum.setText(tr("Ótimo econômico: -- (Pendente)"))
        self.last_result = None
        self.last_sweep_econ_results = {}
        self.economic_optimum_volume = None
        if hasattr(self, "table_mat_impact"):
            self.table_mat_impact.setRowCount(0)
        if hasattr(self, "table_cashflow"):
            self.table_cashflow.setRowCount(0)
        if hasattr(self, "table_vpl_comparison"):
            self.table_vpl_comparison.setRowCount(0)
        if hasattr(self, "chart_sensitivity"):
            self.chart_sensitivity.plot_empty(tr("Execute a varredura completa na Etapa 3 para gerar o gráfico de sensibilidade"))
        if hasattr(self, "chart_vpl_volume"):
            self.chart_vpl_volume.plot_empty(tr("Execute a varredura completa na Etapa 3 para gerar o gráfico comparativo"))

    def showEvent(self, event):
        super().showEvent(event)
        main_win = self.window()
        is_tech = False
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            is_tech = getattr(main_win.tab_tanks_simulation, "_is_technical_only", False)
        if is_tech:
            self.clear_economic_outputs()
        else:
            self._sync_volume_selector()
            self._select_optimum_when_calculated = True
            self.calculate_economics()

    def _sync_volume_selector(self):
        main_win = self.window()
        if not main_win or not hasattr(main_win, "tab_tanks_simulation"):
            return
        ts = main_win.tab_tanks_simulation
        sw_tech = getattr(ts, "last_sweep_result", None)
        
        self.combo_active_volume.blockSignals(True)
        self.combo_active_volume.clear()
        
        best_vpl_vol = None
        if sw_tech and getattr(sw_tech, "results_by_volume", None):
            # Pré-identifica o volume com maior potencial / maior VPL estimado
            for item in sw_tech.results_by_volume:
                v = item.lower_tank_vol
                self.combo_active_volume.addItem(f"{v:,.0f} L".replace(',', '.'), v)
        else:
            single = getattr(ts, "last_single_result", None)
            v = single.lower_tank_vol if single else 4000.0
            self.combo_active_volume.addItem(f"{v:,.0f} L".replace(',', '.'), v)
            
        # Sincroniza índice atual com a configuração ou melhor VPL
        cfg = getattr(main_win, "config", None)
        if cfg and cfg.econ_lower_tank_vol:
            idx = self.combo_active_volume.findData(cfg.econ_lower_tank_vol)
            if idx >= 0:
                self.combo_active_volume.setCurrentIndex(idx)
        elif self.combo_active_volume.count() > 0:
            self.combo_active_volume.setCurrentIndex(0)
            
        self.combo_active_volume.blockSignals(False)

    def _on_active_volume_changed(self):
        v = self.combo_active_volume.currentData()
        if v is not None:
            main_win = self.window()
            if main_win and hasattr(main_win, "config"):
                main_win.config.econ_lower_tank_vol = float(v)
            self.calculate_economics()

    def _on_material_selection_changed(self):
        main_win = self.window()
        if main_win and hasattr(main_win, "config"):
            cfg = main_win.config
            cfg.lower_tank_material = self.combo_lower_mat.currentData()
            cfg.upper_tank_material = self.combo_upper_mat.currentData()
            cfg.chlorine_treatment_enabled = self.chk_chlorine.isChecked()
            cfg.chlorine_dose_mg_l = self.spin_cl_dose.value()
            
            # Recalcula custos preliminares baseados nos novos materiais
            upper_used = bool(getattr(cfg, "upper_tank_used", 1))
            est = estimate_preliminary_capex(
                cfg.econ_lower_tank_vol, getattr(cfg, "upper_tank_vol", 500.0), upper_used,
                cfg.pump_power_kw, cfg.pump_count,
                lower_material=cfg.lower_tank_material, upper_material=cfg.upper_tank_material
            )
            cfg.cost_lower_tank = est["lower"]
            cfg.cost_upper_tank = est["upper"]
            cfg.cost_piping = est["piping"]
            
        self.calculate_economics()

    def _on_open_opex_dialog(self):
        from netuno.ui.dialogs import DialogOtherOpCosts
        cfg = self.get_netuno_config()
        dlg = DialogOtherOpCosts(self, op_costs=cfg.op_costs)
        if dlg.exec():
            cfg.op_costs = dlg.op_costs
            if hasattr(self, "_internal_config") and self._internal_config:
                self._internal_config.op_costs = dlg.op_costs
            main_win = self.window()
            if main_win and hasattr(main_win, "config"):
                main_win.config.op_costs = dlg.op_costs
            self.calculate_economics(force=True)

    def _on_fiscal_param_changed(self):
        main_win = self.window()
        if not hasattr(main_win, "config") and hasattr(self, "parent") and self.parent():
            p = self.parent()
            while p:
                if hasattr(p, "config"):
                    main_win = p
                    break
                p = p.parent() if hasattr(p, "parent") else None

        is_active = self.chk_iptu.isChecked()
        self.spin_iptu_val.setEnabled(is_active)
        self.spin_iptu_disc.setEnabled(is_active)

        val = self.spin_iptu_val.value()
        disc = self.spin_iptu_disc.value()
        ann_savings = val * (disc / 100.0) if is_active else 0.0
        curr_sym = self.get_currency_symbol()

        cfg = getattr(main_win, "config", None) or getattr(self, "_internal_config", None)
        if cfg:
            cfg.iptu_green_enabled = is_active
            cfg.iptu_annual_value = val
            cfg.iptu_discount_pct = disc
            cfg.tariff_flag = self.combo_tariff_flag.currentData() or "verde"
        if hasattr(self, "_internal_config") and self._internal_config:
            self._internal_config.iptu_green_enabled = is_active
            self._internal_config.iptu_annual_value = val
            self._internal_config.iptu_discount_pct = disc
            self._internal_config.tariff_flag = self.combo_tariff_flag.currentData() or "verde"

        n_years = getattr(cfg, "analysis_period_years", 20) if cfg else 20
        tot_nominal = ann_savings * n_years

        if is_active:
            self.lbl_iptu_badge.setText(
                f"✓ {tr('IPTU Verde Ativo:')} {curr_sym} {format_ptbr(ann_savings, 2)}/{tr('ano')} "
                f"({curr_sym} {format_ptbr(tot_nominal, 2)} / {n_years} {tr('anos')})"
            )
            self.lbl_iptu_badge.setStyleSheet(
                "color: #15803d; font-weight: bold; background: #dcfce7; "
                "border: 1px solid #86efac; border-radius: 6px; padding: 3px 10px;"
            )
        else:
            self.lbl_iptu_badge.setText(tr("(Desativado)"))
            self.lbl_iptu_badge.setStyleSheet(
                "color: #94a3b8; font-style: italic; background: transparent; padding: 2px 6px;"
            )

        self.calculate_economics(force=True)

        if main_win and hasattr(main_win, "tab_global_optimizer"):
            opt = main_win.tab_global_optimizer
            if hasattr(opt, "generate_neighborhood_scenarios"):
                opt.generate_neighborhood_scenarios()

        if main_win and hasattr(main_win, "_refresh_sidebar_summary"):
            main_win._refresh_sidebar_summary()

    def calculate_economics(self, force=False):
        main_win = self.window()
        if not hasattr(main_win, "config") and hasattr(self, "parent") and self.parent():
            p = self.parent()
            while p:
                if hasattr(p, "config"):
                    main_win = p
                    break
                p = p.parent() if hasattr(p, "parent") else None

        cfg = self.get_netuno_config()
        curr_sym = self.get_currency_symbol()

        annual_saved_m3 = 0.0
        lower_vol = cfg.econ_lower_tank_vol if cfg.econ_lower_tank_vol > 0 else 4000.0

        upper_used = bool(getattr(cfg, "upper_tank_used", 1))
        low_mat = getattr(cfg, "lower_tank_material", "PEAD")
        up_mat = getattr(cfg, "upper_tank_material", "PEAD")

        # IPTU Verde
        iptu_enabled = getattr(cfg, "iptu_green_enabled", False)
        iptu_val = getattr(cfg, "iptu_annual_value", 4000.0)
        iptu_disc = getattr(cfg, "iptu_discount_pct", 5.0)
        ann_iptu_savings = (iptu_val * (iptu_disc / 100.0)) if iptu_enabled else 0.0

        cl2_enabled = getattr(cfg, "chlorine_treatment_enabled", False)
        cl2_dose = getattr(cfg, "chlorine_dose_mg_l", 2.0)
        cl2_cost_kg = getattr(cfg, "chlorine_cost_per_kg", 25.0)

        est = estimate_preliminary_capex(
            lower_vol, getattr(cfg, "upper_tank_vol", 500.0), upper_used,
            cfg.pump_power_kw, cfg.pump_count,
            lower_material=low_mat, upper_material=up_mat
        )
        # A linha de tratamento entra no investimento. Ate a 5.0.8 esta soma a
        # ignorava, e marcar a filtracao fina nao mexia no valor exibido.
        # A regra incremental - descontar a verba generica ja embutida em
        # «Acessorios» - vive em netuno/core/etap_integration.py, e e a mesma
        # que o motor do nucleo usa.
        # Tipologia nao residencial com tarifa residencial: a conta inteira sai
        # errada, e o sentido do erro e conhecido. Avisar aqui tambem, e nao so
        # no dialogo, porque e aqui que o resultado contaminado e lido.
        if hasattr(self, "lbl_aviso_categoria"):
            _incompat = incompatibilidade_de_categoria(cfg)
            self.lbl_aviso_categoria.setText(
                (tr("⚠️ Categoria tarifária incompatível: ") + _incompat.split("\n")[0])
                if _incompat else ""
            )
            self.lbl_aviso_categoria.setVisible(bool(_incompat))

        etap_capex_inc = capex_incremental_da_etap(cfg)
        total_capex = 0.0 if lower_vol <= 0 else (
            est["lower"] + cfg.cost_upper_tank +
            (cfg.pump_unit_cost * cfg.pump_count if upper_used else 0.0) +
            cfg.cost_piping + cfg.cost_accessories + cfg.cost_labor +
            etap_capex_inc
        )

        has_sim = False
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            ts = main_win.tab_tanks_simulation
            if (ts.last_single_result is not None or ts.last_sweep_result is not None) and (not getattr(ts, "_is_technical_only", False) or force):
                has_sim = True

        if not has_sim:
            # Ainda não houve simulação hídrica: atualiza CAPEX preliminar e tabela de materiais com IPTU Verde
            self.lbl_val_invest.setText(f"{curr_sym} {format_ptbr(total_capex, 2)}")
            if ann_iptu_savings > 0:
                self.lbl_val_annual.setText(f"{curr_sym} {format_ptbr(ann_iptu_savings, 2)}*")
                self.lbl_val_annual.setToolTip(f"{tr('Benefício anual do IPTU Verde')} ({curr_sym} {format_ptbr(ann_iptu_savings, 2)}/{tr('ano')}). " + tr("Execute a simulação hídrica na Etapa 3 para incluir economia de água."))
            else:
                self.lbl_val_annual.setText("--")
                self.lbl_val_annual.setToolTip("")
            self.lbl_val_payback.setText("--")
            self.lbl_val_vpl.setText("--")
            self.lbl_val_tir.setText("--")
            self._populate_materials_breakdown_table(
                cfg, lower_vol, upper_used, low_mat, up_mat,
                0.0, 0.0, 0.0, curr_sym,
                ann_iptu_savings, iptu_disc, iptu_val, iptu_enabled
            )
            return

        # Obtém o resultado hídrico específico para o volume selecionado
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            ts = main_win.tab_tanks_simulation
            sw = getattr(ts, "last_sweep_result", None)
            if sw and getattr(sw, "results_by_volume", None):
                matching = [r for r in sw.results_by_volume if abs(r.lower_tank_vol - lower_vol) < 1.0]
                if matching:
                    annual_saved_m3 = matching[0].annual_pluvial_consumed_m3
                elif sw.results_by_volume:
                    annual_saved_m3 = sw.results_by_volume[0].annual_pluvial_consumed_m3
            elif ts.last_single_result:
                annual_saved_m3 = ts.last_single_result.annual_pluvial_consumed_m3
                lower_vol = ts.last_single_result.lower_tank_vol

        # Atualiza título do painel de indicadores com o volume efetivo
        self.gb_res.setTitle(tr("📊 Indicadores de Viabilidade Econômica") + f" — Cisterna de {lower_vol:,.0f} L".replace(',', '.'))


        annual_total_demand_m3 = (
            max(0.0, float(getattr(cfg, "demand_value", 0.0)))
            * max(0, int(getattr(cfg, "residents_count", 0)))
            * 365.25 / 1000.0
        )
        water_t, sewage_t = calculate_effective_tariff(
            cfg, annual_saved_m3, annual_total_demand_m3=annual_total_demand_m3
        )
        tma_annual = mensal_pct_para_anual_fracao(cfg.tma)
        inf_annual = mensal_pct_para_anual_fracao(cfg.inflation)

        n_readj_per_year = 12.0 / max(1.0, cfg.tariff_escalation)
        w_esc_annual = (1.0 + cfg.water_tariff_escalation / 100.0) ** n_readj_per_year - 1.0
        s_esc_annual = (1.0 + cfg.sewage_tariff_escalation / 100.0) ** n_readj_per_year - 1.0
        e_esc_annual = (1.0 + cfg.elec_tariff_escalation / 100.0) ** n_readj_per_year - 1.0

        pump_hours_year = 0.0
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            single_res = main_win.tab_tanks_simulation.last_single_result
            if single_res and upper_used and cfg.pump_flow_rate > 0:
                sim_days = getattr(single_res, 'total_days', 365)
                t_rec = (single_res.total_pumped_liters / max(1.0, sim_days / 365.25)) / cfg.pump_flow_rate
                ann_cyc = single_res.total_pump_cycles / max(1.0, sim_days / 365.25)
                t_part = ann_cyc * cfg.pump_startup_time_h
                # Horas de operacao, sem dividir pelo rendimento: a potencia de
                # placa ja o embute, e dividir de novo conta a perda duas vezes.
                pump_hours_year = t_rec + t_part

        annual_om_base = annualize_operational_costs(cfg.op_costs, annual_saved_m3)
        # Custeio da linha de tratamento sem a cloracao, que a linha de cloro
        # abaixo ja cobra. Sem isto, escolher ultravioleta ou filtro de polimento
        # nao mexia na manutencao exibida.
        annual_om_base += opex_anual_incremental_da_etap(cfg, annual_saved_m3)

        # Cloração
        cl2_enabled = getattr(cfg, "chlorine_treatment_enabled", True)
        cl2_dose = getattr(cfg, "chlorine_dose_mg_l", 2.0)
        cl2_cost_kg = getattr(cfg, "chlorine_cost_per_kg", 25.0)
        ann_cl2_kg, ann_cl2_cost = estimate_annual_chlorination_cost(
            annual_saved_m3, cl2_dose if cl2_enabled else 0.0, cl2_cost_kg
        )

        # IPTU Verde
        iptu_enabled = getattr(cfg, "iptu_green_enabled", False)
        iptu_val = getattr(cfg, "iptu_annual_value", 4000.0)
        iptu_disc = getattr(cfg, "iptu_discount_pct", 5.0)
        ann_iptu_savings = (iptu_val * (iptu_disc / 100.0)) if iptu_enabled else 0.0

        # Eletricidade ajustada por bandeira
        flag_sel = getattr(cfg, "tariff_flag", "verde")
        flag_add = 0.0
        if flag_sel == "amarela":
            flag_add = 0.01885
        elif flag_sel == "vermelha_1":
            flag_add = 0.04463
        elif flag_sel == "vermelha_2":
            flag_add = 0.07877
        elif flag_sel == "branca":
            flag_add = -0.15 * cfg.elec_tariff
        eff_elec_tariff = max(0.0, cfg.elec_tariff + flag_add)

        econ_res = run_robust_economic_analysis(
            initial_investment=total_capex,
            annual_water_saved_m3=annual_saved_m3,
            water_tariff_per_m3=water_t,
            sewage_tariff_per_m3=sewage_t,
            sewage_mode=cfg.sewage_mode,
            water_tariff_escalation_rate=w_esc_annual,
            sewage_tariff_escalation_rate=s_esc_annual,
            elec_tariff_escalation_rate=e_esc_annual,
            inflation_rate=inf_annual,
            discount_rate=tma_annual,
            annual_om_cost_base=annual_om_base,
            pump_power_kw=cfg.pump_power_kw,
            pump_hours_year=pump_hours_year,
            elec_tariff_kwh=eff_elec_tariff,
            analysis_period_years=cfg.analysis_period_years,
            annual_chlorine_cost=ann_cl2_cost,
            annual_iptu_savings=ann_iptu_savings,
        )
        self.last_result = econ_res

        gross_1st_year = (
            econ_res.annual_cash_flows[1].total_gross_savings_brl
            if len(econ_res.annual_cash_flows) > 1 else 0.0
        )
        self.lbl_val_invest.setText(f"{curr_sym} {format_ptbr(total_capex, 2)}")
        self.lbl_val_annual.setText(f"{curr_sym} {format_ptbr(gross_1st_year, 2)}")
        if ann_iptu_savings > 0:
            self.lbl_val_annual.setToolTip(f"{tr('Inclui')} {curr_sym} {format_ptbr(ann_iptu_savings, 2)}/{tr('ano de benefício IPTU Verde')}")
        else:
            self.lbl_val_annual.setToolTip("")

        pb_sim = f"{format_ptbr(econ_res.payback_simple_years, 1)}a" if econ_res.payback_simple_years else "--"
        pb_disc = f"{format_ptbr(econ_res.payback_discounted_years, 1)}a" if econ_res.payback_discounted_years else "--"
        self.lbl_val_payback.setText(f"{pb_sim} / {pb_disc}")

        self.lbl_val_vpl.setText(f"{curr_sym} {format_ptbr(econ_res.vpl, 2)}")
        self.lbl_val_tir.setText(f"{format_ptbr(econ_res.tir_pct, 1)}%")

        # Preenche Tabela de Detalhamento de Materiais e Equipamentos
        self._populate_materials_breakdown_table(
            cfg, lower_vol, upper_used, low_mat, up_mat,
            ann_cl2_kg, ann_cl2_cost, pump_hours_year, curr_sym,
            ann_iptu_savings, iptu_disc, iptu_val, iptu_enabled
        )

        # Preenche Fluxo de Caixa Anual (com coluna explícita de economia IPTU Verde ano a ano)
        self.table_cashflow.setRowCount(len(econ_res.annual_cash_flows))
        for r_idx, cf in enumerate(econ_res.annual_cash_flows):
            self.table_cashflow.setItem(r_idx, 0,  QTableWidgetItem(str(cf.year)))
            self.table_cashflow.setItem(r_idx, 1,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.initial_investment, 2)}"))
            self.table_cashflow.setItem(r_idx, 2,  QTableWidgetItem(f"{format_ptbr(cf.water_saved_m3, 1)}"))
            self.table_cashflow.setItem(r_idx, 3,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.water_tariff_readjusted, 2)}"))
            self.table_cashflow.setItem(r_idx, 4,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.gross_water_savings_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 5,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.gross_sewage_savings_brl, 2)}"))
            
            it_iptu = QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.iptu_green_savings_brl, 2)}")
            if cf.iptu_green_savings_brl > 0:
                it_iptu.setBackground(QColor("#f0fdf4"))
                it_iptu.setForeground(QColor("#15803d"))
                it_iptu.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table_cashflow.setItem(r_idx, 6,  it_iptu)

            self.table_cashflow.setItem(r_idx, 7,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.total_gross_savings_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 8,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.pump_energy_cost_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 9,  QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.om_cost_brl + cf.chlorine_cost_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 10, QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.net_cash_flow_nominal_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 11, QTableWidgetItem(f"{cf.discount_factor:.4f}"))
            self.table_cashflow.setItem(r_idx, 12, QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.discounted_cash_flow_brl, 2)}"))
            self.table_cashflow.setItem(r_idx, 13, QTableWidgetItem(f"{curr_sym} {format_ptbr(cf.cumulative_discounted_cash_flow_brl, 2)}"))

        # Atualiza Análise de Sensibilidade
        base_params = dict(
            initial_investment=total_capex,
            annual_water_saved_m3=annual_saved_m3,
            water_tariff_per_m3=water_t,
            sewage_tariff_per_m3=sewage_t,
            sewage_mode=cfg.sewage_mode,
            water_tariff_escalation_rate=w_esc_annual,
            sewage_tariff_escalation_rate=s_esc_annual,
            elec_tariff_escalation_rate=e_esc_annual,
            inflation_rate=inf_annual,
            discount_rate=tma_annual,
            annual_om_cost_base=annual_om_base,
            pump_power_kw=cfg.pump_power_kw,
            pump_hours_year=pump_hours_year,
            elec_tariff_kwh=eff_elec_tariff,
            analysis_period_years=cfg.analysis_period_years,
            annual_chlorine_cost=ann_cl2_cost,
            annual_iptu_savings=ann_iptu_savings,
        )
        sens_data = run_sensitivity_analysis(base_params, variations_pct=[-30, -15, 0, 15, 30])
        self.chart_sensitivity.update_chart(sens_data)

        # Preenche a tabela de sensibilidade para o modal
        self.table_sens.setRowCount(len(sens_data))
        for row, (param_name, points) in enumerate(sens_data.items()):
            self.table_sens.setItem(row, 0, QTableWidgetItem(tr(param_name)))
            for c_idx, (v_pct, vpl_val) in enumerate(points):
                item = QTableWidgetItem(f"{curr_sym} {format_ptbr(vpl_val, 2)}")
                if vpl_val < 0: item.setForeground(QColor("#dc2626"))
                self.table_sens.setItem(row, c_idx + 1, item)

        # Atualiza Varredura por Volume e Destaca o Ótimo Econômico (VPL Máximo)
        sweep_econ_results = {}
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            sw_tech = main_win.tab_tanks_simulation.last_sweep_result
            if sw_tech and getattr(sw_tech, 'results_by_volume', None):
                vol_items = sw_tech.results_by_volume
                self.table_vpl_volumes.setRowCount(len(vol_items))
                
                best_pb_idx = -1
                min_pb_val = float('inf')
                best_vpl_idx = -1
                max_vpl_val = -float('inf')

                for row, r_item in enumerate(vol_items):
                    v_vol = r_item.lower_tank_vol
                    vol_m3_val = r_item.annual_pluvial_consumed_m3 if v_vol > 0 else 0.0
                    sim_days = getattr(r_item, 'total_days', getattr(r_item, 'n_days_simulated', 365))

                    est_v = estimate_preliminary_capex(v_vol, getattr(cfg, "upper_tank_vol", 500.0), upper_used, cfg.pump_power_kw, cfg.pump_count, lower_material=low_mat, upper_material=up_mat)
                    c_low = est_v["lower"]
                    capex_v = 0.0 if v_vol <= 0 else (
                        c_low + cfg.cost_upper_tank +
                        (cfg.pump_unit_cost * cfg.pump_count if upper_used else 0.0) +
                        cfg.cost_piping + cfg.cost_accessories + cfg.cost_labor +
                        capex_incremental_da_etap(cfg, vol_m3_val)
                    )
                    tw_v, ts_v = calculate_effective_tariff(
                        cfg, vol_m3_val,
                        annual_total_demand_m3=(r_item.annual_pluvial_consumed_m3 + r_item.annual_potable_consumed_m3) if v_vol > 0 else 0.0,
                    )
                    p_hrs_v = 0.0
                    if upper_used and cfg.pump_flow_rate > 0 and v_vol > 0:
                        if hasattr(r_item, 'total_pumped_liters') and r_item.total_pumped_liters > 0:
                            t_rec_v = (r_item.total_pumped_liters / max(1.0, sim_days / 365.25)) / cfg.pump_flow_rate
                            ann_cyc_v = r_item.total_pump_cycles / max(1.0, sim_days / 365.25)
                            t_part_v = ann_cyc_v * cfg.pump_startup_time_h
                            p_hrs_v = t_rec_v + t_part_v
                        else:
                            ann_pumped_l = vol_m3_val * 1000.0
                            t_rec_v = ann_pumped_l / cfg.pump_flow_rate
                            p_hrs_v = t_rec_v

                    # Cloração proporcional ao volume tratado para cada reservatório
                    if upper_used and v_vol > 0:
                        _, ann_cl_cost_v = estimate_annual_chlorination_cost(
                            vol_m3_val, cl2_dose if cl2_enabled else 0.0, cl2_cost_kg
                        )
                    else:
                        ann_cl_cost_v = 0.0

                    annual_om_v = annualize_operational_costs(cfg.op_costs, vol_m3_val) if v_vol > 0 else 0.0
                    if v_vol > 0:
                        annual_om_v += opex_anual_incremental_da_etap(cfg, vol_m3_val)

                    econ_v = run_robust_economic_analysis(
                        initial_investment=capex_v,
                        annual_water_saved_m3=vol_m3_val,
                        water_tariff_per_m3=tw_v,
                        sewage_tariff_per_m3=ts_v,
                        sewage_mode=cfg.sewage_mode,
                        water_tariff_escalation_rate=w_esc_annual,
                        sewage_tariff_escalation_rate=s_esc_annual,
                        elec_tariff_escalation_rate=e_esc_annual,
                        inflation_rate=inf_annual,
                        discount_rate=tma_annual,
                        annual_om_cost_base=annual_om_v,
                        pump_power_kw=cfg.pump_power_kw,
                        pump_hours_year=p_hrs_v,
                        elec_tariff_kwh=eff_elec_tariff,
                        analysis_period_years=cfg.analysis_period_years,
                        annual_chlorine_cost=ann_cl_cost_v,
                        annual_iptu_savings=(ann_iptu_savings if v_vol > 0 else 0.0),
                    )
                    gross_m = (econ_v.annual_cash_flows[1].total_gross_savings_brl / 12.0) if len(econ_v.annual_cash_flows) > 1 else 0.0
                    pb_v = econ_v.payback_discounted_years or econ_v.payback_simple_years

                    # Custo operacional anual (1º ano)
                    if v_vol > 0 and len(econ_v.annual_cash_flows) > 1:
                        cf1 = econ_v.annual_cash_flows[1]
                        annual_opex_v = cf1.pump_energy_cost_brl + cf1.om_cost_brl + getattr(cf1, "chlorine_cost_brl", 0.0)
                    else:
                        annual_opex_v = 0.0

                    if v_vol > 0:
                        if econ_v.vpl > max_vpl_val:
                            max_vpl_val = econ_v.vpl
                            best_vpl_idx = row

                        # Critério padrão de ótimo econômico: menor payback viável (> 0)
                        pb_cand = econ_v.payback_discounted_years if (econ_v.payback_discounted_years and econ_v.payback_discounted_years > 0) else econ_v.payback_simple_years
                        if pb_cand is not None and pb_cand > 0:
                            if pb_cand < min_pb_val - 1e-4:
                                min_pb_val = pb_cand
                                best_pb_idx = row
                            elif abs(pb_cand - min_pb_val) <= 1e-4:
                                prev_vpl = sweep_econ_results.get(round(vol_items[best_pb_idx].lower_tank_vol, 1), {}).get("vpl", -1e18) if best_pb_idx >= 0 else -1e18
                                if econ_v.vpl > prev_vpl:
                                    min_pb_val = pb_cand
                                    best_pb_idx = row

                    sweep_econ_results[round(v_vol, 1)] = {
                        "volume_l": v_vol,
                        "capex": capex_v,
                        "annual_m3": vol_m3_val,
                        "gross_monthly": gross_m,
                        "vpl": econ_v.vpl,
                        "tir": econ_v.tir_pct,
                        "payback_simple": econ_v.payback_simple_years,
                        "payback_discounted": econ_v.payback_discounted_years,
                        "payback": pb_v,
                        "annual_opex": annual_opex_v,
                        "total_opex": econ_v.total_opex_brl if v_vol > 0 else 0.0,
                        "total_costs": (capex_v + econ_v.total_opex_brl) if v_vol > 0 else 0.0,
                    }

                    self.table_vpl_volumes.setItem(row, 0, QTableWidgetItem(f"{v_vol:.0f}"))
                    self.table_vpl_volumes.setItem(row, 1, QTableWidgetItem(f"{curr_sym} {format_ptbr(capex_v, 2)}"))
                    self.table_vpl_volumes.setItem(row, 2, QTableWidgetItem(f"{curr_sym} {format_ptbr(annual_opex_v, 2)}/a" if annual_opex_v > 0 else f"{curr_sym} 0,00/a"))
                    self.table_vpl_volumes.setItem(row, 3, QTableWidgetItem(f"{format_ptbr(vol_m3_val, 1)}"))
                    self.table_vpl_volumes.setItem(row, 4, QTableWidgetItem(f"{curr_sym} {format_ptbr(econ_v.vpl, 2)}"))
                    self.table_vpl_volumes.setItem(row, 5, QTableWidgetItem(f"{format_ptbr(econ_v.tir_pct, 1)}%"))
                    self.table_vpl_volumes.setItem(row, 6, QTableWidgetItem(f"{format_ptbr(pb_v, 1)}" if pb_v else tr("Sem Retorno")))

                # O default de referência ótima econômica é o payback mais curto
                best_opt_idx = best_pb_idx if best_pb_idx >= 0 else best_vpl_idx

                # Destaque do volume de Ótimo Econômico (Menor Payback)
                if best_opt_idx >= 0:
                    for col in range(7):
                        it = self.table_vpl_volumes.item(best_opt_idx, col)
                        if it:
                            it.setBackground(QColor("#dcfce7"))
                            it.setFont(QFont("Segoe UI", 9, QFont.Bold))
                    it_vol = self.table_vpl_volumes.item(best_opt_idx, 0)
                    if it_vol:
                        tag = tr("Menor Payback") if best_pb_idx >= 0 else tr("VPL Máximo")
                        it_vol.setText(f"★ {it_vol.text()} ({tag})")

                # Se o VPL Máximo for em outro volume, anota-o de forma informativa
                if best_vpl_idx >= 0 and best_vpl_idx != best_opt_idx:
                    it_vpl = self.table_vpl_volumes.item(best_vpl_idx, 0)
                    if it_vpl and "★" not in it_vpl.text():
                        it_vpl.setText(f"{it_vpl.text()} ({tr('Maior VPL')})")

                self.last_sweep_econ_results = sweep_econ_results
                
                opt_tech_v = None
                if sw_tech:
                    opt_tech_v = getattr(sw_tech, "optimal_lower_tank_vol", None)
                cur_metric = self.combo_chart_metric.currentData() if hasattr(self, "combo_chart_metric") else "payback_discounted"
                self.chart_vpl_volume.update_chart(
                    sweep_econ_results,
                    metric=cur_metric or "payback_discounted",
                    currency_symbol=curr_sym,
                    optimal_tech_vol=opt_tech_v,
                    tma_rate=mensal_pct_para_anual_pct(cfg.tma)
                )

                if best_opt_idx >= 0:
                    self.economic_optimum_volume = float(vol_items[best_opt_idx].lower_tank_vol)
                    opt_pb = sweep_econ_results.get(round(self.economic_optimum_volume, 1), {}).get("payback")
                    pb_str = f" ({format_ptbr(opt_pb, 1)} anos)" if opt_pb else ""
                    self.lbl_economic_optimum.setText(
                        f"{tr('Ótimo econômico (menor payback):')} {format_ptbr(self.economic_optimum_volume, 0)} L{pb_str}"
                    )
                    # Atualiza rótulos do seletor de volume ativo com o marcador do ótimo econômico
                    self.combo_active_volume.blockSignals(True)
                    for c_i in range(self.combo_active_volume.count()):
                        c_vol = self.combo_active_volume.itemData(c_i)
                        if c_vol is not None:
                            v_float = float(c_vol)
                            if abs(v_float - self.economic_optimum_volume) < 1.0:
                                self.combo_active_volume.setItemText(c_i, f"★ {format_ptbr(v_float, 0)} L ({tr('Ótimo Econômico - Menor Payback')})")
                            else:
                                self.combo_active_volume.setItemText(c_i, f"{format_ptbr(v_float, 0)} L")
                    self.combo_active_volume.blockSignals(False)

                    if self._select_optimum_when_calculated:
                        self._select_optimum_when_calculated = False
                        idx = self.combo_active_volume.findData(self.economic_optimum_volume)
                        current = self.combo_active_volume.currentData()
                        if idx >= 0 and (current is None or abs(float(current) - self.economic_optimum_volume) >= 1.0):
                            self.combo_active_volume.blockSignals(True)
                            self.combo_active_volume.setCurrentIndex(idx)
                            self.combo_active_volume.blockSignals(False)
                            cfg.econ_lower_tank_vol = self.economic_optimum_volume
                            self.calculate_economics(force=force)
                            return
            elif self.combo_active_volume.currentData() is not None:
                self.economic_optimum_volume = float(self.combo_active_volume.currentData())
                self.lbl_economic_optimum.setText(
                    f"{tr('Ótimo econômico:')} {format_ptbr(self.economic_optimum_volume, 0)} L"
                )
                self._select_optimum_when_calculated = False

        self.economic_calculated.emit()

    def _populate_materials_breakdown_table(
        self, cfg, lower_vol, upper_used, low_mat, up_mat,
        ann_cl2_kg, ann_cl2_cost, pump_hours_year, curr_sym,
        ann_iptu_savings=0.0, iptu_disc=0.0, iptu_val=0.0, iptu_enabled=False
    ):
        font_bold = QFont("Segoe UI", 9, QFont.Bold)
        bg_tot = QColor("#f1f5f9")
        bg_iptu = QColor("#f0fdf4")
        fg_iptu = QColor("#15803d")

        from netuno.core.cost_estimates import default_maintenance_items
        raw_maint = list(cfg.op_costs) if getattr(cfg, "op_costs", None) else default_maintenance_items(upper_used)
        if not raw_maint:
            raw_maint = default_maintenance_items(upper_used)

        if lower_vol <= 0:
            fixed_rows = [
                (tr("Cisterna Inferior"), tr(low_mat), "0 L", 0.0, 0.0),
                (tr("Reservatório Superior"), tr("Desabilitado"), "-", 0.0, 0.0),
                (tr("Tubulações e Conexões"), "-", "-", 0.0, 0.0),
                (tr("Motobomba de Recalque"), "-", "-", 0.0, 0.0),
                (tr("Cloração / Desinfecção"), tr("Inativo"), "-", 0.0, 0.0),
            ]
            maint_rows = [
                (f"🛠️ {tr(it[0])}", f"{tr('Rotina')} {it[1]}m", "-", 0.0, 0.0)
                for it in raw_maint
            ]
            iptu_row = (tr("🌿 Incentivo Fiscal (IPTU Verde)"), tr("Desativado"), "-", 0.0, 0.0)
            rows_data = fixed_rows + maint_rows + [iptu_row]
            tot_capex = 0.0
            tot_opex_net = 0.0
        else:
            # Bomba
            pump_cv = round(cfg.pump_power_kw / 0.735499, 2)
            ann_pump_kwh = (cfg.pump_power_kw * pump_hours_year) if upper_used else 0.0
            ann_pump_cost = ann_pump_kwh * cfg.elec_tariff

            pipe_desc_list = [f"{float(l):.0f}m DN{d}" for d, l in (cfg.pipes_list or []) if float(l) > 0]
            tot_pipe_m = cfg.total_pipe_length() if hasattr(cfg, "total_pipe_length") else sum(float(l) for _, l in (cfg.pipes_list or []))
            pipe_qty_str = f"{tot_pipe_m:,.0f} m lineares".replace(',', '.')
            pipe_spec_str = f"PVC ({', '.join(pipe_desc_list)})" if pipe_desc_list else "PVC Rígido"

            iptu_desc = f"Desconto de {iptu_disc:.1f}% sobre IPTU" if iptu_enabled else tr("(Desativado)")
            iptu_dim = f"{curr_sym} {format_ptbr(iptu_val, 2)}/ano" if iptu_enabled else "-"
            iptu_opex_reduction = -ann_iptu_savings if iptu_enabled else 0.0

            fixed_rows = [
                (tr("Cisterna Inferior"), tr(low_mat), f"{lower_vol:,.0f} L", estimate_preliminary_capex(
                    lower_vol, getattr(cfg, "upper_tank_vol", 500.0), upper_used,
                    cfg.pump_power_kw, cfg.pump_count,
                    lower_material=low_mat, upper_material=up_mat,
                    pipes=cfg.pipes_list
                )["lower"], 0.0),
                (tr("Reservatório Superior"), tr(up_mat) if upper_used else tr("Desabilitado"), f"{cfg.upper_tank_vol:,.0f} L" if upper_used else "-", cfg.cost_upper_tank if upper_used else 0.0, 0.0),
                (tr("Tubulações e Conexões"), pipe_spec_str, pipe_qty_str, cfg.cost_piping + cfg.cost_accessories, 0.0),
                (tr("Motobomba de Recalque"), f"{pump_cv:.2f} CV ({cfg.pump_count}x)", f"{cfg.pump_flow_rate:,.0f} L/h" if upper_used else "-", cfg.pump_unit_cost * cfg.pump_count if upper_used else 0.0, ann_pump_cost),
                (tr("Cloração / Desinfecção"), f"Cloro Ativo ({cfg.chlorine_dose_mg_l:.1f} mg/L)" if cfg.chlorine_treatment_enabled else tr("Inativo"), f"{ann_cl2_kg:.2f} kg/ano", 0.0, ann_cl2_cost),
            ]

            if getattr(cfg, 'etap_enabled', True):
                etap_p = dimensionar_etap_do_projeto(cfg)
                etap_c_inc = capex_incremental_da_etap(cfg)
                etap_o_inc = opex_anual_incremental_da_etap(cfg)
                ff_info = ""
                if etap_p.resultado.first_flush and etap_p.resultado.first_flush.diverter_volume_liters > 0:
                    ff_info = f" + Descarte {etap_p.resultado.first_flush.diverter_volume_liters:.0f} L"
                fixed_rows.append((
                    tr("Linha de Tratamento (ETAP) & Descarte"),
                    f"{tr(etap_p.resultado.target_quality_class)}{ff_info}",
                    f"{etap_p.resultado.disinfection_method.upper()}",
                    etap_c_inc,
                    etap_o_inc,
                ))

            # As 3 manutenções de referência (ou todas as configuradas pelo usuário)
            maint_rows = []
            for it in raw_maint:
                name, period_m, fix_c, var_c = it
                is_pump_maint = "motobomba" in name.lower() or "bomba" in name.lower()
                if is_pump_maint and not upper_used:
                    cost_a = 0.0
                    spec_txt = tr("Inativo (Sem Motobomba)")
                else:
                    cost_a = (fix_c * 12.0 / max(1, period_m))
                    spec_txt = f"{tr('Rotina')} {period_m}m"
                dim_txt = f"{curr_sym} {format_ptbr(fix_c, 2)}" + (f" + {curr_sym} {format_ptbr(var_c, 2)}/m³" if var_c > 0 else "")
                maint_rows.append((f"🛠️ {tr(name)}", spec_txt, dim_txt, 0.0, cost_a))

            iptu_row = (tr("🌿 Incentivo Fiscal (IPTU Verde)"), iptu_desc, iptu_dim, 0.0, iptu_opex_reduction)
            rows_data = fixed_rows + maint_rows + [iptu_row]

            n_capex_opex_items = len(fixed_rows) + len(maint_rows)
            tot_capex = sum(r[3] for r in rows_data[:n_capex_opex_items]) + cfg.cost_labor
            tot_opex_gross = sum(r[4] for r in rows_data[:n_capex_opex_items])
            tot_opex_net = tot_opex_gross - (ann_iptu_savings if iptu_enabled else 0.0)

        total_row_count = len(rows_data) + 1
        self.table_mat_impact.setRowCount(total_row_count)

        iptu_row_idx = len(rows_data) - 1
        tot_row_idx = len(rows_data)

        for i, r in enumerate(rows_data):
            self.table_mat_impact.setItem(i, 0, QTableWidgetItem(r[0]))
            self.table_mat_impact.setItem(i, 1, QTableWidgetItem(r[1]))
            self.table_mat_impact.setItem(i, 2, QTableWidgetItem(r[2]))
            self.table_mat_impact.setItem(i, 3, QTableWidgetItem(f"{curr_sym} {format_ptbr(r[3], 2)}"))
            if i == iptu_row_idx and iptu_enabled:
                it_opex = QTableWidgetItem(f"- {curr_sym} {format_ptbr(ann_iptu_savings, 2)}/a ({tr('Economia')})")
                it_opex.setForeground(fg_iptu)
                it_opex.setBackground(bg_iptu)
                it_opex.setFont(font_bold)
                self.table_mat_impact.setItem(i, 4, it_opex)
                if self.table_mat_impact.item(i, 0):
                    self.table_mat_impact.item(i, 0).setForeground(fg_iptu)
                    self.table_mat_impact.item(i, 0).setFont(font_bold)
            else:
                self.table_mat_impact.setItem(i, 4, QTableWidgetItem(f"{curr_sym} {format_ptbr(r[4], 2)}/a" if r[4] > 0 else "-"))

        # Linha Total
        tot_label = f"★ {tr('TOTAL DO SISTEMA')} (+Mão de Obra e IPTU Verde)" if iptu_enabled else f"★ {tr('TOTAL DO SISTEMA')} (+Mão de Obra)"
        self.table_mat_impact.setItem(tot_row_idx, 0, QTableWidgetItem(tot_label))
        self.table_mat_impact.setItem(tot_row_idx, 1, QTableWidgetItem(f"{low_mat} / {up_mat}"))
        self.table_mat_impact.setItem(tot_row_idx, 2, QTableWidgetItem(f"{lower_vol:,.0f} L"))
        self.table_mat_impact.setItem(tot_row_idx, 3, QTableWidgetItem(f"{curr_sym} {format_ptbr(tot_capex, 2)}"))
        self.table_mat_impact.setItem(tot_row_idx, 4, QTableWidgetItem(f"{curr_sym} {format_ptbr(tot_opex_net, 2)}/a" if lower_vol > 0 else "-"))
        for col in range(5):
            it = self.table_mat_impact.item(tot_row_idx, col)
            if it:
                it.setFont(font_bold)
                it.setBackground(bg_tot)

    def export_cash_flow_csv(self):
        if not self.last_result or not self.last_result.annual_cash_flows:
            QMessageBox.warning(self, tr("Aviso"), tr("Nenhum fluxo de caixa calculado para exportação."))
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("Salvar Fluxo de Caixa"), "fluxo_de_caixa_netuno.csv", "Arquivos CSV (*.csv)"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    "Ano", "Investimento Inicial (R$)", "Água Economizada (m³)", "Tarifa Água (R$/m³)",
                    "Economia Água (R$)", "Economia Esgoto (R$)", "Benefício IPTU Verde (R$)", "Economia Bruta (R$)",
                    "Energia Bomba (R$)", "Custos O&M (R$)", "Cloração (R$)", "Fluxo Líquido (R$)",
                    "Fator Desconto", "Fluxo Descontado (R$)", "Fluxo Acumulado Descontado (R$)"
                ])
                for cf in self.last_result.annual_cash_flows:
                    writer.writerow([
                        cf.year,
                        f"{cf.initial_investment:.2f}".replace('.', ','),
                        f"{cf.water_saved_m3:.2f}".replace('.', ','),
                        f"{cf.water_tariff_readjusted:.2f}".replace('.', ','),
                        f"{cf.gross_water_savings_brl:.2f}".replace('.', ','),
                        f"{cf.gross_sewage_savings_brl:.2f}".replace('.', ','),
                        f"{getattr(cf, 'iptu_green_savings_brl', 0.0):.2f}".replace('.', ','),
                        f"{cf.total_gross_savings_brl:.2f}".replace('.', ','),
                        f"{cf.pump_energy_cost_brl:.2f}".replace('.', ','),
                        f"{cf.om_cost_brl:.2f}".replace('.', ','),
                        f"{getattr(cf, 'chlorine_cost_brl', 0.0):.2f}".replace('.', ','),
                        f"{cf.net_cash_flow_nominal_brl:.2f}".replace('.', ','),
                        f"{cf.discount_factor:.4f}".replace('.', ','),
                        f"{cf.discounted_cash_flow_brl:.2f}".replace('.', ','),
                        f"{cf.cumulative_discounted_cash_flow_brl:.2f}".replace('.', ',')
                    ])
            QMessageBox.information(self, tr("Sucesso"), tr("Fluxo de caixa exportado com sucesso!"))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao salvar CSV:')} {str(e)}")
