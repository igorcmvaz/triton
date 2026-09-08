"""
Aba de Simulação de Cenários em Matriz Fatorial Multi-Core do Netuno 5 (PySide6).
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QProgressBar, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, QThread, Signal

from netuno.core.scenarios import run_multi_scenario_matrix


class MatrixWorkerThread(QThread):
    finished_signal = Signal(object)
    progress_signal = Signal(int, int, object)
    error_signal = Signal(str)

    def __init__(self, precip_files, areas, residents, demands, shares, runoffs, lower_tanks, discard, delta_ideal, sweep_step):
        super().__init__()
        self.precip_files = precip_files
        self.areas = areas
        self.residents = residents
        self.demands = demands
        self.shares = shares
        self.runoffs = runoffs
        self.lower_tanks = lower_tanks
        self.discard = discard
        self.delta_ideal = delta_ideal
        self.sweep_step = sweep_step

    def run(self):
        try:
            def on_progress(completed, total, scen_out, m_row):
                self.progress_signal.emit(completed, total, scen_out)

            res = run_multi_scenario_matrix(
                precip_files=self.precip_files,
                areas=self.areas,
                residents_list=self.residents,
                demands_per_capita=self.demands,
                rainwater_shares=self.shares,
                lower_tanks=self.lower_tanks,
                runoff_coeffs=self.runoffs,
                upper_tank_vol=0.0,
                upper_tank_used=False,
                pumping_threshold=0.0,
                discard_mm=self.discard,
                delta_ideal=self.delta_ideal,
                run_as_sweeps=True,
                sweep_step=self.sweep_step,
                parallel=True,
                progress_callback=on_progress
            )
            self.finished_signal.emit(res)
        except Exception as e:
            self.error_signal.emit(str(e))


class TabMatrixSimulation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # === PAINEL ESQUERDO: CONFIGURAÇÃO DA MATRIZ FATORIAL ===
        left_panel = QVBoxLayout()
        
        group_matrix = QGroupBox("Parâmetros Fatoriais da Matriz")
        grid = QGridLayout()

        grid.addWidget(QLabel("Áreas (m²) [sep por vírgula]:"), 0, 0)
        self.input_areas = QLineEdit("50, 100, 200")
        grid.addWidget(self.input_areas, 0, 1)

        grid.addWidget(QLabel("Demandas (L/hab/dia) [sep vírgula]:"), 1, 0)
        self.input_demands = QLineEdit("100, 150, 200")
        grid.addWidget(self.input_demands, 1, 1)

        grid.addWidget(QLabel("Moradores [sep vírgula]:"), 2, 0)
        self.input_residents = QLineEdit("1, 2, 4")
        grid.addWidget(self.input_residents, 2, 1)

        grid.addWidget(QLabel("% Pluvial [sep vírgula]:"), 3, 0)
        self.input_shares = QLineEdit("50, 60, 70")
        grid.addWidget(self.input_shares, 3, 1)

        grid.addWidget(QLabel("Coeficientes C [sep vírgula]:"), 4, 0)
        self.input_runoffs = QLineEdit("0.7, 0.8, 0.9")
        grid.addWidget(self.input_runoffs, 4, 1)

        grid.addWidget(QLabel("Descarte Inicial (mm):"), 5, 0)
        self.spin_discard = QDoubleSpinBox()
        self.spin_discard.setRange(0.0, 50.0)
        self.spin_discard.setValue(2.0)
        grid.addWidget(self.spin_discard, 5, 1)

        grid.addWidget(QLabel("Volume Máximo Reservatório (L):"), 6, 0)
        self.spin_max_vol = QDoubleSpinBox()
        self.spin_max_vol.setRange(500.0, 100000.0)
        self.spin_max_vol.setSingleStep(500.0)
        self.spin_max_vol.setValue(5000.0)
        grid.addWidget(self.spin_max_vol, 6, 1)

        grid.addWidget(QLabel("Passo de Varredura (L):"), 7, 0)
        self.spin_step = QDoubleSpinBox()
        self.spin_step.setRange(50.0, 5000.0)
        self.spin_step.setSingleStep(50.0)
        self.spin_step.setValue(500.0)
        grid.addWidget(self.spin_step, 7, 1)

        group_matrix.setLayout(grid)
        left_panel.addWidget(group_matrix)

        # Botão Executar Matriz Fatorial
        self.btn_run_matrix = QPushButton("🚀 EXECUTAR MATRIZ FATORIAL MULTI-CORE")
        self.btn_run_matrix.setProperty("class", "btn-primary")
        self.btn_run_matrix.setStyleSheet("font-size: 14px; padding: 12px; background-color: #059669; font-weight: bold;")
        self.btn_run_matrix.clicked.connect(self.run_matrix)
        left_panel.addWidget(self.btn_run_matrix)

        self.btn_dialog_scenarios = QPushButton("📋 Abrir Janela 'Simulação de Cenários'...")
        self.btn_dialog_scenarios.setStyleSheet("font-size: 12px; padding: 8px;")
        self.btn_dialog_scenarios.clicked.connect(self.on_open_scenarios_dialog)
        left_panel.addWidget(self.btn_dialog_scenarios)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        left_panel.addWidget(self.progress_bar)

        left_panel.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(340)
        main_layout.addWidget(left_widget)

        # === PAINEL DIREITO: TABELA DE RESULTADOS FATORIAIS ===
        right_panel = QVBoxLayout()
        
        lbl_table_title = QLabel("Resultados Fatoriais por Cenário")
        lbl_table_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #10b981;")
        right_panel.addWidget(lbl_table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID Cenário", "Chuva / Cidade", "Área (m²)", "Moradores", 
            "Demanda (L/hab)", "% Pluvial", "Coef. C", "Vol. Ótimo (L)", "Potencial (%)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_panel.addWidget(self.table)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        main_layout.addWidget(right_widget)

        self.setLayout(main_layout)

    def parse_list_float(self, text, default=[100.0]):
        try:
            return [float(x.strip()) for x in text.split(",") if x.strip()]
        except ValueError:
            return default

    def parse_list_int(self, text, default=[1]):
        try:
            return [int(x.strip()) for x in text.split(",") if x.strip()]
        except ValueError:
            return default

    def run_matrix(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        rainfall_dir = os.path.join(base_dir, "data", "rainfall")

        precip_tuples = []
        if os.path.exists(rainfall_dir):
            for fn in os.listdir(rainfall_dir):
                if fn.endswith(".csv"):
                    precip_tuples.append((fn, os.path.join(rainfall_dir, fn)))

        if not precip_tuples:
            samples_dir = os.path.join(base_dir, "Additional_Material", "Precipitation_Samples")
            if os.path.exists(samples_dir):
                for fn in os.listdir(samples_dir):
                    if fn.endswith(".csv"):
                        precip_tuples.append((fn, os.path.join(samples_dir, fn)))

        if not precip_tuples:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo de chuva foi encontrado na pasta data/rainfall.")
            return

        areas = self.parse_list_float(self.input_areas.text(), [100.0])
        demands = self.parse_list_float(self.input_demands.text(), [100.0])
        residents = self.parse_list_int(self.input_residents.text(), [1])
        shares = self.parse_list_float(self.input_shares.text(), [50.0])
        runoffs = self.parse_list_float(self.input_runoffs.text(), [0.9])
        discard = self.spin_discard.value()
        max_vol = self.spin_max_vol.value()
        step = self.spin_step.value()

        self.table.setRowCount(0)
        self.btn_run_matrix.setEnabled(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        self.worker = MatrixWorkerThread(
            precip_files=precip_tuples,
            areas=areas,
            residents=residents,
            demands=demands,
            shares=shares,
            runoffs=runoffs,
            lower_tanks=[max_vol],
            discard=discard,
            delta_ideal=2.0,
            sweep_step=step
        )
        self.worker.progress_signal.connect(self.on_matrix_progress)
        self.worker.finished_signal.connect(self.on_matrix_finished)
        self.worker.error_signal.connect(self.on_matrix_error)
        self.worker.start()

    def on_matrix_progress(self, completed: int, total: int, scen_out: object):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(completed)

        if scen_out and hasattr(scen_out, "scenario"):
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            scen = scen_out.scenario
            pot_val = scen_out.sweep_result.optimal_potential_pct if scen_out.sweep_result and scen_out.sweep_result.optimal_potential_pct is not None else 0.0

            self.table.setItem(row_idx, 0, QTableWidgetItem(scen.scenario_id))
            self.table.setItem(row_idx, 1, QTableWidgetItem(scen.city_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{scen.area:.0f}"))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{scen.residents}"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"{scen.demand_per_capita:.0f}"))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{scen.rainwater_share * 100.0:.0f}%"))
            self.table.setItem(row_idx, 6, QTableWidgetItem(f"{scen.runoff_coeff:.2f}"))
            self.table.setItem(row_idx, 7, QTableWidgetItem(f"{scen.lower_tank_vol:.0f} L"))
            self.table.setItem(row_idx, 8, QTableWidgetItem(f"{pot_val:.2f}%"))

    def on_matrix_finished(self, matrix_res):
        self.btn_run_matrix.setEnabled(True)
        self.progress_bar.hide()
        QMessageBox.information(self, "Matriz Concluída", f"Simulação concluída com sucesso! {matrix_res.total_scenarios_run} cenários fatoriais executados.")

    def on_matrix_error(self, err_msg):
        self.btn_run_matrix.setEnabled(True)
        self.progress_bar.hide()
        QMessageBox.critical(self, "Erro na Matriz Fatorial", f"Erro na execução paralela:\n{err_msg}")

    def on_open_scenarios_dialog(self):
        from netuno.ui.dialogs import DialogScenarioSimulation
        dlg = DialogScenarioSimulation(self)
        dlg.exec()
