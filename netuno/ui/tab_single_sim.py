"""
Tela Principal de Entrada de Dados e Simulação do Netuno 4.
Reprodução 1:1 idêntica ao leiaute, caixas de diálogo, painéis dinâmicos, janelas de dados variáveis e tabela de resultado mensal.
"""

import os
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QFileDialog, 
    QTableWidget, QTableWidgetItem, QTextEdit, QRadioButton, QButtonGroup, 
    QMessageBox, QCheckBox, QDialog, QHeaderView, QFormLayout, QTabWidget, QStackedLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from netuno.core.parser import NetunoConfig, load_precipitation, export_netuno_csv, parse_netuno_csv, format_netuno_float
from netuno.core.simulation import run_single_simulation, run_sweep_simulation, SingleTankSimulationResult, SweepSimulationResult
from netuno.core.economic import run_economic_analysis
from netuno.ui.charts import DailyWaterBalanceChart, VolumeSweepChart
from netuno.ui.date_picker import DatePickerLineEdit


from netuno.ui.dialogs import (
    DialogUpperTank,
    DialogVariableInput,
    DialogMonthlyValues,
    DialogEconomicAnalysis
)


class TabSingleSimulation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.precip_data = None
        self.current_precip_file = ""
        self.last_sweep_result = None
        self.last_single_result = None

        # Parâmetros de Dados Variáveis
        self.variable_demand_values = None
        self.variable_residents_values = None

        # Parâmetros do Reservatório Superior (Padrão Netuno 4: Mode 0 = Igual à demanda)
        self.upper_tank_mode = 0  # 0: Demanda, 1: Desejado, 2: Não utilizar
        self.upper_tank_vol = 2100.0
        self.upper_thresh_mode = 1  # 0: Litros, 1: Percentual
        self.upper_thresh_val = 10.0

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # === LINHA SUPERIOR COM 2 COLUNAS DE CONTEÚDO ===
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(15)

        # =========================================================================
        # COLUNA DA ESQUERDA (DADOS DE ENTRADA DO SISTEMA)
        # =========================================================================
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)

        # 1. Botão Topo Esquerda: Carregar simulação previamente salva
        self.btn_load_sim = QPushButton("Carregar simulação previamente salva")
        self.btn_load_sim.clicked.connect(self.on_load_project)
        left_layout.addWidget(self.btn_load_sim)

        # 2. Tabela de Chuva / Precipitação (4 linhas, 2 colunas)
        self.table_precip = QTableWidget(4, 2)
        self.table_precip.horizontalHeader().setVisible(False)
        self.table_precip.verticalHeader().setVisible(False)
        self.table_precip.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_precip.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_precip.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_precip.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_precip.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_precip.setRowCount(4)
        self.table_precip.setColumnCount(2)
        self.table_precip.setFixedHeight(102)

        item_prec_label = QTableWidgetItem("Carregar dados de precipitação")
        item_prec_label.setFlags(Qt.ItemIsEnabled)
        self.table_precip.setItem(0, 0, item_prec_label)

        self.item_prec_val = QTableWidgetItem("Clique para carregar CSV...")
        from netuno.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"
        self.item_prec_val.setBackground(QColor("#1e3a8a" if is_dark else "#99ccff"))
        self.item_prec_val.setForeground(QColor("#ffffff" if is_dark else "#000000"))
        self.item_prec_val.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table_precip.setItem(0, 1, self.item_prec_val)

        item_reg_label = QTableWidgetItem("Número de registros")
        item_reg_label.setFlags(Qt.ItemIsEnabled)
        self.table_precip.setItem(1, 0, item_reg_label)
        self.item_reg_val = QTableWidgetItem("0")
        self.item_reg_val.setFlags(Qt.ItemIsEnabled)
        self.table_precip.setItem(1, 1, self.item_reg_val)

        item_date_label = QTableWidgetItem("Data inicial (dd/MM/yyyy)")
        item_date_label.setFlags(Qt.ItemIsEnabled)
        self.table_precip.setItem(2, 0, item_date_label)
        self.txt_start_date = DatePickerLineEdit("01/01/2000", default_preset_date="01/01/2000")
        self.table_precip.setCellWidget(2, 1, self.txt_start_date)

        item_disc_label = QTableWidgetItem("Descarte escoamento inicial (mm)")
        item_disc_label.setFlags(Qt.ItemIsEnabled)
        self.table_precip.setItem(3, 0, item_disc_label)
        self.txt_discard = QLineEdit("2")
        self.table_precip.setCellWidget(3, 1, self.txt_discard)

        self.table_precip.cellClicked.connect(self.on_precip_table_clicked)
        left_layout.addWidget(self.table_precip)

        # 3. Área de captação (m²)
        lbl_area = QLabel("Área de captação (m²)")
        left_layout.addWidget(lbl_area)
        self.txt_area = QLineEdit("100")
        left_layout.addWidget(self.txt_area)

        # 4. Demanda total de água (litros per capita/dia)
        lbl_demand = QLabel("Demanda total de água (litros per capita/dia)")
        left_layout.addWidget(lbl_demand)
        row_demand = QHBoxLayout()
        self.txt_demand = QLineEdit("200")
        self.btn_var_demand = QPushButton("Variável...")
        self.btn_var_demand.clicked.connect(self.on_variable_demand)
        row_demand.addWidget(self.txt_demand)
        row_demand.addWidget(self.btn_var_demand)
        left_layout.addLayout(row_demand)

        # 5. Número de moradores
        lbl_residents = QLabel("Número de moradores")
        left_layout.addWidget(lbl_residents)
        row_residents = QHBoxLayout()
        self.txt_residents = QLineEdit("4")
        self.btn_var_residents = QPushButton("Variável...")
        self.btn_var_residents.clicked.connect(self.on_variable_residents)
        row_residents.addWidget(self.txt_residents)
        row_residents.addWidget(self.btn_var_residents)
        left_layout.addLayout(row_residents)

        # 6. Percentual da demanda total a ser substituída por água pluvial
        lbl_share = QLabel("Percentual da demanda total a ser substituída por água pluvial")
        left_layout.addWidget(lbl_share)
        self.combo_share = QComboBox()
        for p in range(10, 110, 10):
            self.combo_share.addItem(f"{p}%", p)
        self.combo_share.setCurrentIndex(3)  # 40%
        left_layout.addWidget(self.combo_share)

        # 7. Coeficiente de escoamento superficial (Material da cobertura)
        lbl_runoff = QLabel("Material da cobertura / Coeficiente de escoamento (C)")
        left_layout.addWidget(lbl_runoff)
        
        row_runoff = QHBoxLayout()
        self.combo_runoff = QComboBox()
        self.combo_runoff.addItem("Telha Cerâmica (0,75)", 0.75)
        self.combo_runoff.addItem("Telha Metálica (0,88)", 0.88)
        self.combo_runoff.addItem("Telha de Cimento / Fibrocimento (0,73)", 0.73)
        self.combo_runoff.addItem("Telhados verdes (0,24)", 0.24)
        self.combo_runoff.addItem("Alumínio (0,70)", 0.70)
        self.combo_runoff.addItem("Plástico / Policarbonato (0,94)", 0.94)
        self.combo_runoff.addItem("Concreto Asfáltico (0,90)", 0.90)
        self.combo_runoff.addItem("Aço Galvanizado (0,92)", 0.92)
        self.combo_runoff.addItem("Outro / Personalizado...", -1.0)
        self.combo_runoff.setCurrentIndex(0)  # 0.75 Telha Cerâmica

        self.txt_custom_runoff = QLineEdit("0,75")
        self.txt_custom_runoff.setFixedWidth(80)
        self.txt_custom_runoff.setPlaceholderText("ex: 0,75")
        self.txt_custom_runoff.hide()

        self.combo_runoff.currentIndexChanged.connect(self.on_single_sim_runoff_changed)

        row_runoff.addWidget(self.combo_runoff, stretch=2)
        row_runoff.addWidget(self.txt_custom_runoff, stretch=1)
        left_layout.addLayout(row_runoff)

        # 8. Observações
        lbl_obs = QLabel("Observações")
        left_layout.addWidget(lbl_obs)
        self.txt_obs = QTextEdit()
        self.txt_obs.setPlainText("Preencha este campo para consultas futuras,\ncaso queira salvar a simulação.\nEste campo não afeta os cálculos.")
        self.txt_obs.setFixedHeight(65)
        left_layout.addWidget(self.txt_obs)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(380)
        columns_layout.addWidget(left_widget)

        # =========================================================================
        # COLUNA DA DIREITA (RESERVATÓRIOS E OPÇÕES DE SIMULAÇÃO)
        # =========================================================================
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

        # 1. Botão Topo Direita: Reservatório superior
        self.btn_upper_tank = QPushButton("Reservatório superior")
        self.btn_upper_tank.clicked.connect(self.on_upper_tank_dialog)
        right_layout.addWidget(self.btn_upper_tank)

        # 2. GroupBox "Reservatório inferior"
        group_lower = QGroupBox("Reservatório inferior")
        group_lower_layout = QVBoxLayout()

        self.radio_fixed = QRadioButton("Simulação para reservatório com volume conhecido")
        self.radio_sweep = QRadioButton("Simulação para reservatórios com diversos volumes")
        self.radio_fixed.setCursor(Qt.PointingHandCursor)
        self.radio_sweep.setCursor(Qt.PointingHandCursor)
        self.radio_fixed.setChecked(True)

        group_lower_layout.addWidget(self.radio_fixed)
        group_lower_layout.addWidget(self.radio_sweep)
        group_lower.setLayout(group_lower_layout)
        right_layout.addWidget(group_lower)

        # 3. GroupBox "Simulação" (Painel Dinâmico de Resultados sob Demanda)
        self.group_sim = QGroupBox("Simulação")
        self.stack_sim_panel = QStackedLayout()
        self.group_sim.setLayout(self.stack_sim_panel)
        right_layout.addWidget(self.group_sim)

        # =========================================================================
        # PAINEL MODO FIXO (Volume Conhecido) — Idêntico à Captura de Tela do Netuno 4
        # =========================================================================
        self.widget_fixed_panel = QWidget()
        wf_layout = QVBoxLayout()
        wf_layout.setContentsMargins(0, 0, 0, 0)
        wf_layout.setSpacing(6)

        row_fixed = QHBoxLayout()
        lbl_fixed_vol = QLabel("Volume do Reservatório inferior (litros):")
        self.txt_fixed_vol = QLineEdit("2000")
        self.txt_fixed_vol.setMinimumWidth(110)
        row_fixed.addWidget(lbl_fixed_vol)
        row_fixed.addWidget(self.txt_fixed_vol)
        wf_layout.addLayout(row_fixed)

        # Resultados do Modo Fixo (Ocultos até o clique em Simular)
        self.lbl_fixed_pot = QLabel("")
        font_bold = QFont("Segoe UI", 10)
        font_bold.setBold(True)
        self.lbl_fixed_pot.setFont(font_bold)
        self.lbl_fixed_pot.setStyleSheet("color: #000000; margin-top: 4px;")
        wf_layout.addWidget(self.lbl_fixed_pot)

        self.lbl_fixed_days_title = QLabel("Percentual de dias no período de análise em que a\ndemanda de água pluvial é atendida:")
        self.lbl_fixed_days_title.setStyleSheet("color: #333333; margin-top: 4px;")
        wf_layout.addWidget(self.lbl_fixed_days_title)

        self.lbl_fixed_full = QLabel("")
        self.lbl_fixed_partial = QLabel("")
        self.lbl_fixed_null = QLabel("")
        wf_layout.addWidget(self.lbl_fixed_full)
        wf_layout.addWidget(self.lbl_fixed_partial)
        wf_layout.addWidget(self.lbl_fixed_null)

        self.btn_monthly_values = QPushButton("Valores mensais")
        self.btn_monthly_values.setCursor(Qt.PointingHandCursor)
        self.btn_monthly_values.clicked.connect(self.on_show_monthly_values)
        wf_layout.addWidget(self.btn_monthly_values)

        self.btn_sim_fixed = QPushButton("Simular")
        self.btn_sim_fixed.setFixedHeight(34)
        self.btn_sim_fixed.setCursor(Qt.PointingHandCursor)
        self.btn_sim_fixed.setStyleSheet("background-color: #0284c7; color: #ffffff; font-weight: bold; border: 1px solid #0369a1; border-radius: 4px; padding: 7px 16px; font-size: 10pt;")
        self.btn_sim_fixed.clicked.connect(self.run_simulation)
        wf_layout.addWidget(self.btn_sim_fixed)

        row_fixed_actions = QHBoxLayout()
        self.btn_save_sim = QPushButton("Salvar simulação atual")
        self.btn_save_sim.setCursor(Qt.PointingHandCursor)
        self.btn_save_sim.clicked.connect(self.on_save_project)
        self.btn_clear_fields = QPushButton("Limpar campos")
        self.btn_clear_fields.setCursor(Qt.PointingHandCursor)
        self.btn_clear_fields.clicked.connect(self.on_clear_fields)
        row_fixed_actions.addWidget(self.btn_save_sim)
        row_fixed_actions.addWidget(self.btn_clear_fields)
        wf_layout.addLayout(row_fixed_actions)

        self.btn_econ_fixed = QPushButton("Análise Econômica")
        self.btn_econ_fixed.setCursor(Qt.PointingHandCursor)
        self.btn_econ_fixed.clicked.connect(self.on_run_economic)
        wf_layout.addWidget(self.btn_econ_fixed)
        self.widget_fixed_panel.setLayout(wf_layout)

        # =========================================================================
        # PAINEL MODO VARREDURA (Diversos Volumes)
        # =========================================================================
        self.widget_sweep_panel = QWidget()
        ws_layout = QVBoxLayout()
        ws_layout.setContentsMargins(0, 0, 0, 0)
        ws_layout.setSpacing(6)

        grid_sweep = QGridLayout()
        grid_sweep.setColumnStretch(0, 2)
        grid_sweep.setColumnStretch(1, 1)

        lbl_max = QLabel("Volume máximo do reservatório inferior (litros):")
        self.txt_sweep_max = QLineEdit("10000")
        self.txt_sweep_max.setMinimumWidth(110)
        grid_sweep.addWidget(lbl_max, 0, 0)
        grid_sweep.addWidget(self.txt_sweep_max, 0, 1)

        lbl_step = QLabel("Intervalo entre volumes do reservatório inferior (litros):")
        self.txt_sweep_step = QLineEdit("250")
        self.txt_sweep_step.setMinimumWidth(110)
        grid_sweep.addWidget(lbl_step, 1, 0)
        grid_sweep.addWidget(self.txt_sweep_step, 1, 1)

        self.chk_ideal = QCheckBox("Indicar volume ideal para o reservatório inferior")
        self.chk_ideal.setChecked(True)
        grid_sweep.addWidget(self.chk_ideal, 2, 0, 1, 2)

        lbl_delta = QLabel("Diferença entre potenciais de atendimento pluvial (%/m³):")
        self.txt_delta_ideal = QLineEdit("5,0")
        self.txt_delta_ideal.setMinimumWidth(110)
        grid_sweep.addWidget(lbl_delta, 3, 0)
        grid_sweep.addWidget(self.txt_delta_ideal, 3, 1)

        ws_layout.addLayout(grid_sweep)

        # Resultados do Modo Varredura (Ocultos até o clique em Simular)
        self.lbl_sweep_ideal_vol = QLabel("")
        self.lbl_sweep_ideal_vol.setFont(font_bold)
        self.lbl_sweep_ideal_vol.setStyleSheet("color: #000000; margin-top: 4px;")
        ws_layout.addWidget(self.lbl_sweep_ideal_vol)

        self.lbl_sweep_pot = QLabel("")
        self.lbl_sweep_pot.setFont(font_bold)
        self.lbl_sweep_pot.setStyleSheet("color: #000000;")
        ws_layout.addWidget(self.lbl_sweep_pot)

        row_sweep_actions = QHBoxLayout()
        self.btn_view_data = QPushButton("Planilha de dados")
        self.btn_view_data.setCursor(Qt.PointingHandCursor)
        self.btn_view_data.clicked.connect(self.on_show_data_sheet)
        self.btn_view_graph = QPushButton("Gráfico")
        self.btn_view_graph.setCursor(Qt.PointingHandCursor)
        self.btn_view_graph.clicked.connect(self.on_show_graph)
        row_sweep_actions.addWidget(self.btn_view_data)
        row_sweep_actions.addWidget(self.btn_view_graph)
        ws_layout.addLayout(row_sweep_actions)

        self.btn_sim_sweep = QPushButton("Simular")
        self.btn_sim_sweep.setFixedHeight(34)
        self.btn_sim_sweep.setCursor(Qt.PointingHandCursor)
        self.btn_sim_sweep.setStyleSheet("background-color: #0284c7; color: #ffffff; font-weight: bold; border: 1px solid #0369a1; border-radius: 4px; padding: 7px 16px; font-size: 10pt;")
        self.btn_sim_sweep.clicked.connect(self.run_simulation)
        ws_layout.addWidget(self.btn_sim_sweep)

        row_sweep_actions2 = QHBoxLayout()
        self.btn_save_sim_sw = QPushButton("Salvar simulação atual")
        self.btn_save_sim_sw.setCursor(Qt.PointingHandCursor)
        self.btn_save_sim_sw.clicked.connect(self.on_save_project)
        self.btn_clear_fields_sw = QPushButton("Limpar campos")
        self.btn_clear_fields_sw.setCursor(Qt.PointingHandCursor)
        self.btn_clear_fields_sw.clicked.connect(self.on_clear_fields)
        row_sweep_actions2.addWidget(self.btn_save_sim_sw)
        row_sweep_actions2.addWidget(self.btn_clear_fields_sw)
        ws_layout.addLayout(row_sweep_actions2)

        self.btn_econ_sweep = QPushButton("Análise Econômica")
        self.btn_econ_sweep.setCursor(Qt.PointingHandCursor)
        self.btn_econ_sweep.clicked.connect(self.on_run_economic)
        ws_layout.addWidget(self.btn_econ_sweep)

        self.widget_sweep_panel.setLayout(ws_layout)

        self.stack_sim_panel.addWidget(self.widget_fixed_panel)
        self.stack_sim_panel.addWidget(self.widget_sweep_panel)

        self.radio_fixed.toggled.connect(self.update_tank_mode_visibility)
        self.radio_sweep.toggled.connect(self.update_tank_mode_visibility)
        self.update_tank_mode_visibility()

        right_layout.addStretch()
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        columns_layout.addWidget(right_widget)

        main_layout.addLayout(columns_layout)
        self.setLayout(main_layout)

        # Oculta todos os resultados para inicialização limpa
        self.hide_results()

        # Auto-carrega amostra de chuva padrão (Manaus2.csv se existir)
        self.auto_load_default_rainfall()

    def hide_results(self):
        """Oculta completamente os painéis de resultado até que o usuário clique em Simular."""
        self.lbl_fixed_pot.hide()
        self.lbl_fixed_days_title.hide()
        self.lbl_fixed_full.hide()
        self.lbl_fixed_partial.hide()
        self.lbl_fixed_null.hide()
        self.btn_monthly_values.hide()

        self.lbl_sweep_ideal_vol.hide()
        self.lbl_sweep_pot.hide()
        self.btn_view_data.hide()
        self.btn_view_graph.hide()

    def auto_load_default_rainfall(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        default_p = os.path.join(base_dir, "data", "rainfall", "Manaus2.csv")
        if not os.path.exists(default_p):
            default_p = os.path.join(base_dir, "Additional_Material", "Precipitation_Samples", "Manaus2.csv")
        if not os.path.exists(default_p):
            default_p = os.path.join(base_dir, "data", "rainfall", "precFpolis_2002_2011.csv")

        if os.path.exists(default_p):
            self.load_precip_file(default_p)

    def on_precip_table_clicked(self, row, col):
        if row == 0:
            file_path, _ = QFileDialog.getOpenFileName(self, "Carregar Dados de Precipitação", "", "Arquivos CSV (*.csv);;Todos os Arquivos (*.*)")
            if file_path:
                self.load_precip_file(file_path)

    def load_precip_file(self, file_path: str):
        try:
            self.precip_data = load_precipitation(file_path)
            self.current_precip_file = file_path
            fn = os.path.basename(file_path)
            self.item_prec_val.setText(fn)
            self.item_reg_val.setText(str(len(self.precip_data)))
            self.hide_results()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar arquivo de chuva:\n{str(e)}")

    def update_tank_mode_visibility(self):
        txt_fixed = self.radio_fixed.text().replace("✓ ", "")
        txt_sweep = self.radio_sweep.text().replace("✓ ", "")
        self.radio_fixed.setText(txt_fixed)
        self.radio_sweep.setText(txt_sweep)

        if self.radio_fixed.isChecked():
            self.radio_fixed.setText(f"✓ {txt_fixed}")
            self.stack_sim_panel.setCurrentWidget(self.widget_fixed_panel)
        else:
            self.radio_sweep.setText(f"✓ {txt_sweep}")
            self.stack_sim_panel.setCurrentWidget(self.widget_sweep_panel)


    def get_calculated_daily_pluvial_demand(self) -> float:
        try:
            demand = float(self.txt_demand.text().replace(',', '.'))
            residents = float(self.txt_residents.text().replace(',', '.'))
            share = self.combo_share.currentData() / 100.0
            return demand * residents * share
        except Exception:
            return 120.0

    def update_upper_tank_button_label(self):
        if self.upper_tank_mode == 0:
            t_str = f"{self.upper_thresh_val:.0f}L" if self.upper_thresh_mode == 0 else f"{self.upper_thresh_val:.0f}%"
            self.btn_upper_tank.setText(f"✓ Reservatório superior (Demanda, {t_str})")
        elif self.upper_tank_mode == 1:
            t_str = f"{self.upper_thresh_val:.0f}L" if self.upper_thresh_mode == 0 else f"{self.upper_thresh_val:.0f}%"
            self.btn_upper_tank.setText(f"✓ Reservatório superior ({self.upper_tank_vol:.0f}L, {t_str})")
        else:
            self.btn_upper_tank.setText("Reservatório superior (Não utilizado)")

    def on_upper_tank_dialog(self):
        daily_p_demand = self.get_calculated_daily_pluvial_demand()
        current_vol = self.upper_tank_vol if self.upper_tank_mode != 0 else daily_p_demand
        dlg = DialogUpperTank(
            parent=self,
            daily_pluvial_demand=daily_p_demand,
            vol=current_vol,
            mode=self.upper_tank_mode,
            thresh_mode=self.upper_thresh_mode,
            thresh_val=self.upper_thresh_val
        )
        if dlg.exec():
            self.upper_tank_mode = dlg.upper_tank_mode
            self.upper_tank_vol = dlg.upper_tank_vol
            self.upper_thresh_mode = dlg.thresh_mode
            self.upper_thresh_val = dlg.thresh_val
            self.update_upper_tank_button_label()


    def on_variable_demand(self):
        try:
            cur_val = float(self.txt_demand.text().replace(',', '.'))
        except ValueError:
            cur_val = 200.0

        dlg = DialogVariableInput(
            parent=self,
            title="Demanda variável",
            col_title="Demanda total de água (litros per capita/dia)",
            default_val=cur_val
        )
        if dlg.exec():
            self.variable_demand_values = dlg.values
            QMessageBox.information(self, "Demanda Variável", "Valores de demanda variável atualizados com sucesso.")

    def on_variable_residents(self):
        try:
            cur_val = float(self.txt_residents.text().replace(',', '.'))
        except ValueError:
            cur_val = 4.0

        dlg = DialogVariableInput(
            parent=self,
            title="Número de moradores variável",
            col_title="Número de moradores",
            default_val=cur_val
        )
        if dlg.exec():
            self.variable_residents_values = dlg.values
            QMessageBox.information(self, "Número de Moradores Variável", "Valores de moradores variáveis atualizados com sucesso.")

    def on_single_sim_runoff_changed(self):
        is_custom = (self.combo_runoff.currentData() == -1.0)
        if is_custom:
            self.txt_custom_runoff.show()
        else:
            self.txt_custom_runoff.hide()
            val = self.combo_runoff.currentData()
            if val is not None and val > 0:
                self.txt_custom_runoff.setText(f"{val:.2f}".replace('.', ','))

    def get_selected_runoff(self) -> float:
        if self.combo_runoff.currentData() == -1.0:
            try:
                return float(self.txt_custom_runoff.text().replace(',', '.'))
            except ValueError:
                return 0.75
        return self.combo_runoff.currentData() or 0.75

    def on_clear_fields(self):
        self.txt_area.setText("100")
        self.txt_demand.setText("200")
        self.txt_residents.setText("4")
        self.combo_share.setCurrentIndex(3)
        self.txt_fixed_vol.setText("2000")
        self.txt_discard.setText("2")
        self.txt_obs.setPlainText("Preencha este campo para consultas futuras,\ncaso queira salvar a simulação.\nEste campo não afeta os cálculos.")
        self.upper_tank_mode = 0
        self.upper_tank_vol = 2100.0
        self.upper_thresh_mode = 1
        self.upper_thresh_val = 10.0
        self.variable_demand_values = None
        self.variable_residents_values = None
        self.combo_runoff.setCurrentIndex(0)
        self.hide_results()

    def run_simulation(self):
        """
        Executa o balanço hídrico diário e exibe os resultados na tela ao clicar em Simular.
        """
        if self.precip_data is None or len(self.precip_data) == 0:
            QMessageBox.warning(self, "Aviso", "Por favor, carregue um arquivo de precipitação primeiro.")
            return

        try:
            area = float(self.txt_area.text().replace(',', '.'))
            demand_per_capita = float(self.txt_demand.text().replace(',', '.'))
            residents = int(self.txt_residents.text().replace(',', '.'))
            tot_demand = demand_per_capita * residents
            
            r_share = self.combo_share.currentData() / 100.0
            runoff = self.get_selected_runoff()
            discard = float(self.txt_discard.text().replace(',', '.'))

            upper_used = (self.upper_tank_mode != 2)
            if self.upper_tank_mode == 0:
                upper_vol = tot_demand * r_share
            elif self.upper_tank_mode == 1:
                upper_vol = self.upper_tank_vol
            else:
                upper_vol = 0.0

            if self.upper_thresh_mode == 0:
                pumping_threshold = self.upper_thresh_val
            else:
                pumping_threshold = upper_vol * (self.upper_thresh_val / 100.0)

            discard_mode = 1
            discard_days = 7
            main_win = self.window()
            if main_win and hasattr(main_win, 'tab_project'):
                discard_mode = main_win.tab_project.get_discard_mode()
                discard_days = main_win.tab_project.get_discard_days()

            if self.radio_sweep.isChecked():
                max_vol = float(self.txt_sweep_max.text().replace(',', '.'))
                step_vol = float(self.txt_sweep_step.text().replace(',', '.'))
                delta_ideal = float(self.txt_delta_ideal.text().replace(',', '.')) if self.chk_ideal.isChecked() else 0.0

                self.last_sweep_result = run_sweep_simulation(
                    precip_data=self.precip_data,
                    lower_tank_max=max_vol,
                    lower_tank_step=step_vol,
                    area=area,
                    runoff_coeff=runoff,
                    discard_mm=discard,
                    discard_mode=discard_mode,
                    discard_days_interval=discard_days,
                    total_demand_per_day=tot_demand,
                    rainwater_share=r_share,
                    upper_tank_vol=upper_vol,
                    upper_tank_used=upper_used,
                    pumping_threshold=pumping_threshold,
                    delta_ideal_threshold=delta_ideal,
                    store_daily_details=True
                )

                opt_v = self.last_sweep_result.optimal_lower_tank_vol
                opt_p = self.last_sweep_result.optimal_potential_pct

                if opt_v is not None and opt_p is not None:
                    self.lbl_sweep_ideal_vol.setText(f"Volume ideal indicado para o reservatório inferior: {opt_v:.0f} litros")
                    self.lbl_sweep_pot.setText(f"Potencial de utilização de água pluvial: {opt_p:.2f}%".replace('.', ','))
                else:
                    self.lbl_sweep_ideal_vol.setText("Volume ideal indicado para o reservatório inferior: Não encontrado")
                    self.lbl_sweep_pot.setText("Potencial de utilização de água pluvial: --%")

                self.lbl_sweep_ideal_vol.show()
                self.lbl_sweep_pot.show()
                self.btn_view_data.show()
                self.btn_view_graph.show()

            else:
                fixed_vol = float(self.txt_fixed_vol.text().replace(',', '.'))
                self.last_single_result = run_single_simulation(
                    precip_data=self.precip_data,
                    lower_tank_vol=fixed_vol,
                    area=area,
                    runoff_coeff=runoff,
                    discard_mm=discard,
                    discard_mode=discard_mode,
                    discard_days_interval=discard_days,
                    total_demand_per_day=tot_demand,
                    rainwater_share=r_share,
                    upper_tank_vol=upper_vol,
                    upper_tank_used=upper_used,
                    pumping_threshold=pumping_threshold,
                    store_daily_details=True
                )

                pot = self.last_single_result.potential_potable_savings_pct
                full = self.last_single_result.pct_days_full_satisfaction
                part = self.last_single_result.pct_days_partial_satisfaction
                null = self.last_single_result.pct_days_null_satisfaction

                self.lbl_fixed_pot.setText(f"Potencial de utilização de água pluvial: {pot:.2f}%".replace('.', ','))
                self.lbl_fixed_full.setText(f"- Completamente: {full:.2f}%".replace('.', ','))
                self.lbl_fixed_partial.setText(f"- Parcialmente: {part:.2f}%".replace('.', ','))
                self.lbl_fixed_null.setText(f"- Não atende: {null:.2f}%".replace('.', ','))

                self.lbl_fixed_pot.show()
                self.lbl_fixed_days_title.show()
                self.lbl_fixed_full.show()
                self.lbl_fixed_partial.show()
                self.lbl_fixed_null.show()
                self.btn_monthly_values.show()

        except Exception as e:
            QMessageBox.critical(self, "Erro na Simulação", f"Falha ao executar simulação:\n{str(e)}")

    def on_show_monthly_values(self):
        if not self.last_single_result:
            self.run_simulation()

        stats = {}
        if self.last_single_result and self.last_single_result.daily_results and self.precip_data is not None:
            demand_per_capita = float(self.txt_demand.text().replace(',', '.'))
            residents = int(self.txt_residents.text().replace(',', '.'))
            tot_demand = demand_per_capita * residents

            dates = pd.date_range(start=self.txt_start_date.text(), periods=len(self.precip_data), freq='D')
            df = pd.DataFrame({
                'month': dates.month,
                'pluvial': [d.pluvial_consumed_liters for d in self.last_single_result.daily_results],
                'potable': [d.potable_consumed_liters for d in self.last_single_result.daily_results],
                'spilled': [d.spilled_liters for d in self.last_single_result.daily_results],
                'sat': [d.satisfaction_type for d in self.last_single_result.daily_results],
                'cycles': [d.pump_cycles for d in self.last_single_result.daily_results]
            })

            n_years = len(df['month']) / 365.25 if len(df['month']) > 0 else 1.0

            for m_idx in range(1, 13):
                m_df = df[df['month'] == m_idx]
                if len(m_df) > 0:
                    pluv_m = m_df['pluvial'].sum() / len(m_df)
                    pot_m = m_df['potable'].sum() / len(m_df)
                    spill_m = m_df['spilled'].sum() / len(m_df)
                    
                    pot_pct = (m_df['pluvial'].sum() / (tot_demand * len(m_df))) * 100.0 if tot_demand > 0 else 0.0
                    comp_pct = (m_df['sat'] == 2).mean() * 100.0
                    parc_pct = (m_df['sat'] == 1).mean() * 100.0
                    nulo_pct = (m_df['sat'] == 0).mean() * 100.0
                    rec_avg = m_df['cycles'].mean()

                    stats[m_idx] = {
                        'pot_pct': pot_pct,
                        'pluvial': pluv_m,
                        'potable': pot_m,
                        'spilled': spill_m,
                        'comp': comp_pct,
                        'parc': parc_pct,
                        'null': nulo_pct,
                        'rec': rec_avg
                    }

            tot_pluv_year = df['pluvial'].sum() / n_years
            tot_pot_year = df['potable'].sum() / n_years
            tot_spill_year = df['spilled'].sum() / n_years

            stats['year_totals'] = {
                'pluvial': tot_pluv_year,
                'potable': tot_pot_year,
                'spilled': tot_spill_year
            }

        dlg = DialogMonthlyValues(self, monthly_stats=stats)
        dlg.exec()

    def on_show_data_sheet(self):
        if not self.last_sweep_result or not self.last_sweep_result.results_by_volume:
            self.run_simulation()

        if self.last_sweep_result and self.last_sweep_result.results_by_volume:
            dlg = QDialog(self)
            dlg.setWindowTitle("Planilha de Dados - Simulação Netuno 4")
            dlg.resize(850, 400)
            layout = QVBoxLayout()

            table = QTableWidget()
            cols = [
                "Reservatório inferior (L)", "Potencial de economia (%)", 
                "Consumo médio pluvial (L/dia)", "Consumo médio potável (L/dia)", 
                "Volume extravasado (L/dia)", "Atendimento total (%)", 
                "Atendimento parcial (%)", "Sem atendimento (%)", "Delta (%/m³)"
            ]
            table.setColumnCount(len(cols))
            table.setHorizontalHeaderLabels(cols)
            table.setRowCount(len(self.last_sweep_result.results_by_volume))

            for row, res in enumerate(self.last_sweep_result.results_by_volume):
                table.setItem(row, 0, QTableWidgetItem(f"{res.lower_tank_vol:.0f}"))
                table.setItem(row, 1, QTableWidgetItem(f"{res.potential_potable_savings_pct:.2f}"))
                table.setItem(row, 2, QTableWidgetItem(f"{res.avg_pluvial_consumed_l_day:.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"{res.avg_potable_consumed_l_day:.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{res.avg_spilled_l_day:.3f}"))
                table.setItem(row, 5, QTableWidgetItem(f"{res.pct_days_full_satisfaction:.2f}"))
                table.setItem(row, 6, QTableWidgetItem(f"{res.pct_days_partial_satisfaction:.2f}"))
                table.setItem(row, 7, QTableWidgetItem(f"{res.pct_days_null_satisfaction:.2f}"))
                table.setItem(row, 8, QTableWidgetItem(f"{res.delta_potential_per_m3:.2f}"))

            layout.addWidget(table)
            dlg.setLayout(layout)
            dlg.exec()

    def on_show_graph(self):
        if not self.last_sweep_result:
            self.run_simulation()

        if self.last_sweep_result:
            dlg = QDialog(self)
            dlg.setWindowTitle("Gráfico - Potencial de Economia vs Volume do Reservatório")
            dlg.resize(750, 480)
            layout = QVBoxLayout()

            chart = VolumeSweepChart()
            chart.update_chart(self.last_sweep_result.results_by_volume, self.last_sweep_result.optimal_lower_tank_vol)
            layout.addWidget(chart)

            dlg.setLayout(layout)
            dlg.exec()

    def on_run_economic(self):
        if not self.last_single_result and not self.last_sweep_result:
            self.run_simulation()

        sim_res = self.last_single_result
        optimal_vol = None
        if not sim_res and self.last_sweep_result and self.last_sweep_result.results_by_volume:
            sim_res = self.last_sweep_result.results_by_volume[0]
            optimal_vol = self.last_sweep_result.optimal_lower_tank_vol

        try:
            cfg = NetunoConfig(
                precip_file=self.current_precip_file,
                area=float(self.txt_area.text().replace(',', '.')),
                demand_value=float(self.txt_demand.text().replace(',', '.')),
                residents_count=int(self.txt_residents.text().replace(',', '.')),
                rainwater_share=self.combo_share.currentData() / 100.0,
                runoff_coeff=self.get_selected_runoff(),
                discard=float(self.txt_discard.text().replace(',', '.')),
                upper_tank_vol=self.upper_tank_vol,
                upper_tank_used=1 if self.upper_tank_mode != 2 else 0,
                pumping_threshold=self.upper_thresh_val if self.upper_thresh_mode == 0 else self.upper_tank_vol * (self.upper_thresh_val / 100.0),
                lower_tank_fixed=float(self.txt_fixed_vol.text().replace(',', '.')) if self.radio_fixed.isChecked() else 2000.0
            )

            dlg = DialogEconomicAnalysis(self, config=cfg, sim_result=sim_res, optimal_vol=optimal_vol)
            dlg.exec()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir Análise Econômica:\n{str(e)}")


    def on_save_project(self):
        from netuno import get_kebab_filename
        def_name = get_kebab_filename("netuno-simulacao", "csv")
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Simulação", def_name, "Arquivos CSV (*.csv)")
        if not file_path:
            return

        try:
            cfg = NetunoConfig(
                precip_file=self.current_precip_file,
                area=float(self.txt_area.text().replace(',', '.')),
                demand_value=float(self.txt_demand.text().replace(',', '.')),
                residents_count=int(self.txt_residents.text().replace(',', '.')),
                rainwater_share=self.combo_share.currentData() / 100.0,
                runoff_coeff=self.get_selected_runoff(),
                discard=float(self.txt_discard.text().replace(',', '.')),
                upper_tank_vol=self.upper_tank_vol,
                upper_tank_used=1 if self.upper_tank_mode != 2 else 0,
                pumping_threshold=self.upper_thresh_val if self.upper_thresh_mode == 0 else self.upper_tank_vol * (self.upper_thresh_val / 100.0),
                lower_tank_max=float(self.txt_sweep_max.text().replace(',', '.')) if self.radio_sweep.isChecked() else 0.0,
                lower_tank_step=float(self.txt_sweep_step.text().replace(',', '.')) if self.radio_sweep.isChecked() else 0.0,
                lower_tank_mode=1 if self.radio_sweep.isChecked() else 0,
                lower_tank_fixed=float(self.txt_fixed_vol.text().replace(',', '.')) if self.radio_fixed.isChecked() else 2000.0
            )

            res_list = self.last_sweep_result.results_by_volume if self.last_sweep_result else []
            export_netuno_csv(cfg, res_list, file_path, self.precip_data)
            QMessageBox.information(self, "Sucesso", f"Simulação salva com sucesso em:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Erro ao Salvar", f"Falha ao salvar arquivo de simulação:\n{str(e)}")

    def on_load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Carregar Simulação Previamente Salva", "", "Arquivos CSV (*.csv)")
        if not file_path:
            return

        try:
            cfg = parse_netuno_csv(file_path)
            self.txt_area.setText(str(cfg.area))
            self.txt_demand.setText(str(cfg.demand_value))
            self.txt_residents.setText(str(cfg.residents_count))
            self.txt_discard.setText(str(cfg.discard))
            self.txt_start_date.setText(cfg.start_date)

            if cfg.precip_file and os.path.exists(cfg.precip_file):
                self.load_precip_file(cfg.precip_file)
            else:
                self.hide_results()

            QMessageBox.information(self, "Sucesso", f"Simulação carregada com sucesso a partir de:\n{os.path.basename(file_path)}")

        except Exception as e:
            QMessageBox.critical(self, "Erro ao Carregar", f"Falha ao carregar arquivo de simulação:\n{str(e)}")
