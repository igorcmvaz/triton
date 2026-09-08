"""
Diálogo 1:1 idêntico ao Netuno 4 para "Simulação de Cenários".
Permite selecionar múltiplos arquivos de precipitação e inserir parâmetros em grade com todos os detalhes:
- Data de início da chuva
- Descarte inicial (mm)
- Modo de reservatório inferior (Varredura vs Fixo) e passo de varredura
- Opção Fatorial vs Lista Direta (Posicional)
"""

import os
import itertools
from typing import List, Dict, Any, Tuple
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QRadioButton, QButtonGroup, QGroupBox, QLabel, QProgressBar, QMessageBox, QFileDialog, QHeaderView
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor
from netuno.ui.translation import tr, get_current_theme

from netuno.core.parser import load_precipitation, parse_float, parse_int
from netuno.core.simulation import run_single_simulation, run_sweep_simulation
from netuno.core.excel_scenarios import export_scenarios_to_excel_bytes


class ScenarioWorkerThread(QThread):
    finished_signal = Signal(list)
    progress_signal = Signal(int, int, dict)
    error_signal = Signal(str)

    def __init__(self, scenarios: List[Dict[str, Any]]):
        super().__init__()
        self.scenarios = scenarios

    def run(self):
        try:
            precip_cache: Dict[str, Any] = {}
            results = []
            total = len(self.scenarios)

            for idx, sc in enumerate(self.scenarios):
                fpath = sc["precip_file"]
                if fpath not in precip_cache:
                    try:
                        precip_cache[fpath] = load_precipitation(fpath)
                    except Exception:
                        base_name = os.path.basename(fpath)
                        precip_cache[fpath] = load_precipitation(base_name)

                prec = precip_cache[fpath]
                tot_demand = sc["demand_per_capita"] * sc["residents"]

                if sc.get("is_sweep", True):
                    sw = run_sweep_simulation(
                        precip_data=prec,
                        lower_tank_max=sc["lower_tank_vol"],
                        lower_tank_step=sc.get("lower_tank_step", 250.0),
                        area=sc["area"],
                        runoff_coeff=sc["runoff_coeff"],
                        discard_mm=sc["discard"],
                        total_demand_per_day=tot_demand,
                        rainwater_share=sc["rainwater_share"],
                        upper_tank_vol=sc["upper_tank_vol"],
                        upper_tank_used=bool(sc["upper_tank_vol"] > 0),
                        pumping_threshold=sc["pumping_threshold"]
                    )
                    opt_v = sw.optimal_lower_tank_vol
                    opt_pot = sw.optimal_potential_pct
                    avg_pluv = 0.0
                    avg_spill = 0.0
                    if sw.results_by_volume:
                        for r in sw.results_by_volume:
                            if r.lower_tank_vol == opt_v:
                                avg_pluv = r.avg_pluvial_consumed_l_day
                                avg_spill = r.avg_spilled_l_day
                                break
                        if avg_pluv == 0.0 and len(sw.results_by_volume) > 0:
                            avg_pluv = sw.results_by_volume[-1].avg_pluvial_consumed_l_day
                            avg_spill = sw.results_by_volume[-1].avg_spilled_l_day

                    res_item = {
                        tr("ID"): f"CEN_{idx+1:03d}",
                        tr("Nome Cenário"): sc["scenario_name"],
                        tr("Arquivo de Chuva"): os.path.basename(sc["precip_file"]),
                        tr("Data de Início"): sc.get("start_date", "01/01/2002"),
                        tr("Área (m²)"): sc["area"],
                        tr("Moradores"): sc["residents"],
                        tr("Demanda per capita (L/hab/dia)"): sc["demand_per_capita"],
                        tr("Demanda Total (L/dia)"): tot_demand,
                        tr("Substituição Pluvial (%)"): round(sc["rainwater_share"] * 100.0, 1),
                        tr("Descarte (mm)"): sc["discard"],
                        tr("Coeficiente de Escoamento (C)"): sc["runoff_coeff"],
                        tr("Modo do Reservatório"): tr("Varredura"),
                        tr("Volume Recomendado (L)"): opt_v if opt_v is not None else tr("Indeterminado"),
                        tr("Economia Potencial (%)"): round(opt_pot, 2) if opt_pot else 0.0,
                        tr("Consumo Pluvial Médio (L/dia)"): round(avg_pluv, 2),
                        tr("Volume Extravasado Médio (L/dia)"): round(avg_spill, 2)
                    }
                else:
                    s_res = run_single_simulation(
                        precip_data=prec,
                        lower_tank_vol=sc["lower_tank_vol"],
                        area=sc["area"],
                        runoff_coeff=sc["runoff_coeff"],
                        discard_mm=sc["discard"],
                        total_demand_per_day=tot_demand,
                        rainwater_share=sc["rainwater_share"],
                        upper_tank_vol=sc["upper_tank_vol"],
                        upper_tank_used=bool(sc["upper_tank_vol"] > 0),
                        pumping_threshold=sc["pumping_threshold"]
                    )
                    res_item = {
                        tr("ID"): f"CEN_{idx+1:03d}",
                        tr("Nome Cenário"): sc["scenario_name"],
                        tr("Arquivo de Chuva"): os.path.basename(sc["precip_file"]),
                        tr("Data de Início"): sc.get("start_date", "01/01/2002"),
                        tr("Área (m²)"): sc["area"],
                        tr("Moradores"): sc["residents"],
                        tr("Demanda per capita (L/hab/dia)"): sc["demand_per_capita"],
                        tr("Demanda Total (L/dia)"): tot_demand,
                        tr("Substituição Pluvial (%)"): round(sc["rainwater_share"] * 100.0, 1),
                        tr("Descarte (mm)"): sc["discard"],
                        tr("Coeficiente de Escoamento (C)"): sc["runoff_coeff"],
                        tr("Modo do Reservatório"): tr("Fixo"),
                        tr("Volume Recomendado (L)"): sc["lower_tank_vol"],
                        tr("Economia Potencial (%)"): round(s_res.potential_potable_savings_pct, 2),
                        tr("Consumo Pluvial Médio (L/dia)"): round(s_res.avg_pluvial_consumed_l_day, 2),
                        tr("Volume Extravasado Médio (L/dia)"): round(s_res.avg_spilled_l_day, 2)
                    }

                results.append(res_item)
                self.progress_signal.emit(idx + 1, total, res_item)

            self.finished_signal.emit(results)
        except Exception as e:
            self.error_signal.emit(str(e))


class DialogScenarioSimulation(QDialog):
    """
    Janela 1:1 com a tela "Simulação de Cenários" do Netuno 4 com todos os detalhes e modos.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Simulação de Cenários"))
        self.resize(780, 520)
        self.selected_rain_files: List[str] = []
        self.last_results: List[Dict[str, Any]] = []

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # 1. Tabela Principal (Parâmetro | Valores)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([tr("Parâmetro"), tr("Valores")])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setRowCount(12)

        params = [
            tr("Arquivos de precipitação"),
            tr("Data de início da chuva (dd/mm/aaaa)"),
            tr("Área de captação (m²)"),
            tr("Demandas totais de água (L/hab/dia)"),
            tr("Números de moradores"),
            tr("Percentuais de substituição (%)"),
            tr("Descarte inicial de chuva (mm)"),
            tr("Coeficientes de escoamento superficial (C)"),
            tr("Reservatórios superiores (L)"),
            tr("Modo do reservatório inferior"),
            tr("Reservatórios inferiores (L)"),
            tr("Passo de varredura (L)")
        ]

        default_vals = [
            "",  # Múltiplos arquivos
            "01/01/2002",
            "100",
            "100",
            "3",
            "40",
            "1,0",
            "0,9",
            "500",
            tr("Varredura"),
            "10000",
            "250"
        ]

        font_bold = QFont("Segoe UI", 9)
        font_bold.setBold(True)

        for r, (p_name, d_val) in enumerate(zip(params, default_vals)):
            item_p = QTableWidgetItem(p_name)
            item_p.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item_p.setFont(font_bold)
            self.table.setItem(r, 0, item_p)

            item_v = QTableWidgetItem(d_val)
            self.table.setItem(r, 1, item_v)

        # Evento de clique para linha 0 (Arquivos de precipitação)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.cellClicked.connect(self.on_cell_clicked)

        main_layout.addWidget(self.table)

        # 2. Seleção de Modo de Simulação (Fatorial vs Lista Direta)
        gb_mode = QGroupBox(tr("Modo de Combinação dos Cenários"))
        lay_mode = QHBoxLayout()
        self.radio_factorial = QRadioButton(tr("Mode Fatorial (matriz de combinações entre todas as opções)"))
        self.radio_list = QRadioButton(tr("Modo Lista Direta (execução pareada cenário a cenário)"))
        self.radio_factorial.setChecked(True)

        self.radio_factorial.toggled.connect(self.update_mode_checks)
        self.radio_list.toggled.connect(self.update_mode_checks)

        lay_mode.addWidget(self.radio_factorial)
        lay_mode.addWidget(self.radio_list)
        gb_mode.setLayout(lay_mode)
        main_layout.addWidget(gb_mode)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        # 3. Painel de Botões Inferior
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_run = QPushButton(tr("Simular cenários"))
        self.btn_run.setFixedHeight(34)
        self.btn_run.setStyleSheet("font-weight: bold; background-color: #0284c7; color: white;")
        self.btn_run.clicked.connect(self.on_run_simulation)

        self.btn_clear = QPushButton(tr("Limpar"))
        self.btn_clear.setFixedHeight(34)
        self.btn_clear.clicked.connect(self.on_clear)

        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_clear)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        self.update_mode_checks()

    def update_mode_checks(self):
        f_base = tr("Modo Fatorial (matriz de combinações entre todas as opções)")
        l_base = tr("Modo Lista Direta (execução pareada cenário a cenário)")
        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"
        norm_color = "#e4e4e7" if is_dark else "#333333"

        if self.radio_factorial.isChecked():
            self.radio_factorial.setText(f"✓ {f_base}")
            self.radio_list.setText(l_base)
            self.radio_factorial.setStyleSheet(f"font-weight: bold; color: {text_color};")
            self.radio_list.setStyleSheet(f"font-weight: normal; color: {norm_color};")
        else:
            self.radio_factorial.setText(f_base)
            self.radio_list.setText(f"✓ {l_base}")
            self.radio_list.setStyleSheet(f"font-weight: bold; color: {text_color};")
            self.radio_factorial.setStyleSheet(f"font-weight: normal; color: {norm_color};")

    def on_cell_clicked(self, row, col):
        if row == 0 and col == 1:
            self.select_rain_files()

    def on_cell_double_clicked(self, row, col):
        if row == 0:
            self.select_rain_files()

    def select_rain_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            tr("Selecionar Arquivos de Precipitação"), 
            "", 
            f"{tr('Arquivos CSV')} (*.csv)"
        )
        if files:
            self.selected_rain_files = files
            names_str = ", ".join([os.path.basename(f) for f in files])
            self.table.setItem(0, 1, QTableWidgetItem(names_str))

    def parse_list_float(self, val_str: str, default: List[float]) -> List[float]:
        if not val_str or not val_str.strip():
            return default
        try:
            return [parse_float(x) for x in val_str.replace(';', ',').split(',') if x.strip()]
        except Exception:
            return default

    def parse_list_int(self, val_str: str, default: List[int]) -> List[int]:
        if not val_str or not val_str.strip():
            return default
        try:
            return [parse_int(x) for x in val_str.replace(';', ',').split(',') if x.strip()]
        except Exception:
            return default

    def on_clear(self):
        self.selected_rain_files = []
        for r in range(12):
            self.table.setItem(r, 1, QTableWidgetItem(""))

    def on_run_simulation(self):
        # 1. Obter arquivos de chuva
        rain_files = self.selected_rain_files
        if not rain_files:
            cell_str = self.table.item(0, 1).text().strip() if self.table.item(0, 1) else ""
            if cell_str:
                rain_files = [x.strip() for x in cell_str.split(',') if x.strip()]

        if not rain_files:
            rain_files = ["precFpolis_2002_2011.csv"]

        start_dates = [x.strip() for x in (self.table.item(1, 1).text() if self.table.item(1, 1) else "01/01/2002").split(',') if x.strip()]
        areas = self.parse_list_float(self.table.item(2, 1).text() if self.table.item(2, 1) else "", [100.0])
        demands = self.parse_list_float(self.table.item(3, 1).text() if self.table.item(3, 1) else "", [100.0])
        residents = self.parse_list_int(self.table.item(4, 1).text() if self.table.item(4, 1) else "", [3])
        
        raw_shares = self.parse_list_float(self.table.item(5, 1).text() if self.table.item(5, 1) else "", [40.0])
        shares = [s / 100.0 if s > 1.0 else s for s in raw_shares]
        
        discards = self.parse_list_float(self.table.item(6, 1).text() if self.table.item(6, 1) else "", [1.0])
        runoffs = self.parse_list_float(self.table.item(7, 1).text() if self.table.item(7, 1) else "", [0.9])
        upper_tanks = self.parse_list_float(self.table.item(8, 1).text() if self.table.item(8, 1) else "", [500.0])
        
        mode_str = (self.table.item(9, 1).text() if self.table.item(9, 1) else "Varredura").strip().lower()
        is_sweep_mode = "varredura" in mode_str or "sweep" in mode_str
        
        lower_tanks = self.parse_list_float(self.table.item(10, 1).text() if self.table.item(10, 1) else "", [10000.0 if is_sweep_mode else 2000.0])
        sweep_steps = self.parse_list_float(self.table.item(11, 1).text() if self.table.item(11, 1) else "", [250.0])

        scenarios = []
        is_factorial = self.radio_factorial.isChecked()

        if is_factorial:
            idx = 0
            for rf, s_date, area, dem, res, sh, disc, c_eff, u_vol, l_vol, step_v in itertools.product(
                rain_files, start_dates, areas, demands, residents, shares, discards, runoffs, upper_tanks, lower_tanks, sweep_steps
            ):
                idx += 1
                c_name = os.path.splitext(os.path.basename(rf))[0]
                scenarios.append({
                    "scenario_name": f"Cenario_{idx:03d}_{c_name}",
                    "precip_file": rf,
                    "start_date": s_date,
                    "area": area,
                    "residents": res,
                    "demand_per_capita": dem,
                    "rainwater_share": sh,
                    "discard": disc,
                    "runoff_coeff": c_eff,
                    "is_sweep": is_sweep_mode,
                    "lower_tank_vol": l_vol,
                    "lower_tank_step": step_v,
                    "upper_tank_vol": u_vol,
                    "pumping_threshold": u_vol * 0.75 if u_vol > 0 else 0.0
                })
        else:
            max_len = max(
                len(rain_files), len(start_dates), len(areas), len(demands), len(residents), 
                len(shares), len(discards), len(runoffs), len(upper_tanks), len(lower_tanks), len(sweep_steps)
            )
            for i in range(max_len):
                rf = rain_files[i % len(rain_files)]
                s_date = start_dates[i % len(start_dates)]
                area = areas[i % len(areas)]
                dem = demands[i % len(demands)]
                res = residents[i % len(residents)]
                sh = shares[i % len(shares)]
                disc = discards[i % len(discards)]
                c_eff = runoffs[i % len(runoffs)]
                u_vol = upper_tanks[i % len(upper_tanks)]
                l_vol = lower_tanks[i % len(lower_tanks)]
                step_v = sweep_steps[i % len(sweep_steps)]

                c_name = os.path.splitext(os.path.basename(rf))[0]
                scenarios.append({
                    "scenario_name": f"Cenario_{i+1:03d}_{c_name}",
                    "precip_file": rf,
                    "start_date": s_date,
                    "area": area,
                    "residents": res,
                    "demand_per_capita": dem,
                    "rainwater_share": sh,
                    "discard": disc,
                    "runoff_coeff": c_eff,
                    "is_sweep": is_sweep_mode,
                    "lower_tank_vol": l_vol,
                    "lower_tank_step": step_v,
                    "upper_tank_vol": u_vol,
                    "pumping_threshold": u_vol * 0.75 if u_vol > 0 else 0.0
                })

        if not scenarios:
            QMessageBox.warning(self, tr("Aviso"), tr("Nenhum cenário configurado."))
            return

        self.btn_run.setEnabled(False)
        self.progress_bar.setRange(0, len(scenarios))
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        self.worker = ScenarioWorkerThread(scenarios)
        self.worker.progress_signal.connect(self.on_simulation_progress)
        self.worker.finished_signal.connect(self.on_simulation_finished)
        self.worker.error_signal.connect(self.on_simulation_error)
        self.worker.start()

    def on_simulation_progress(self, completed: int, total: int, res_item: dict):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(completed)

    def on_simulation_finished(self, results):
        self.btn_run.setEnabled(True)
        self.progress_bar.hide()
        self.last_results = results

        res_dlg = QDialog(self)
        res_dlg.setWindowTitle(tr("Resultados da Simulação de Cenários"))
        res_dlg.resize(900, 480)
        res_lay = QVBoxLayout()

        table_res = QTableWidget()
        if results:
            cols = list(results[0].keys())
            table_res.setColumnCount(len(cols))
            table_res.setHorizontalHeaderLabels(cols)
            table_res.setRowCount(len(results))

            for r, row_dict in enumerate(results):
                for c, (k, val) in enumerate(row_dict.items()):
                    table_res.setItem(r, c, QTableWidgetItem(str(val)))

        res_lay.addWidget(table_res)

        btn_excel = QPushButton(tr("📥 Exportar Resultados para Excel (.xlsx)..."))
        btn_excel.setStyleSheet("font-weight: bold; padding: 8px; background-color: #10b981; color: white;")
        btn_excel.clicked.connect(lambda: self.export_to_excel(results))
        res_lay.addWidget(btn_excel)

        res_dlg.setLayout(res_lay)
        res_dlg.exec()

    def export_to_excel(self, results):
        out_path, _ = QFileDialog.getSaveFileName(
            self, tr("Salvar Resultados dos Cenários"), "resultado_cenarios_netuno.xlsx", f"{tr('Planilha Excel')} (*.xlsx)"
        )
        if out_path:
            excel_bytes = export_scenarios_to_excel_bytes(results)
            with open(out_path, "wb") as f:
                f.write(excel_bytes)
            QMessageBox.information(self, tr("Excel Salvo"), f"{tr('Resultados salvos com sucesso em:')}\n{out_path}")

    def on_simulation_error(self, err_msg):
        self.btn_run.setEnabled(True)
        self.progress_bar.hide()
        QMessageBox.critical(self, tr("Erro na Simulação"), f"{tr('Ocorreu um erro durante a simulação')}:\n{err_msg}")
