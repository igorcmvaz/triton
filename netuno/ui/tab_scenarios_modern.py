"""
Etapa 6: Estudo de Cenários, Análise de Sensibilidade & Avaliação de Risco (Worst to Best Case).
Permite modelar 7 perfis de cenários normativos/legais com variações de ±10%, ±20% e ±30% em conjunto para
Área de Captação, Percentual de Uso Não Potável e Consumo de Água, mantendo transparência com uma coluna descritiva.
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QBrush, QColor

from netuno.ui.translation import tr, get_current_theme
from netuno.core.simulation import run_sweep_simulation
from netuno.ui.charts import MultiScenarioSweepChart


class TabScenariosModern(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.last_scenarios_data = []
        
        # Propriedades para retrocompatibilidade
        self.txt_min_val = QLineEdit("100")
        self.txt_max_val = QLineEdit("300")
        self.txt_step_val = QLineEdit("100")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        is_dark = get_current_theme() == "dark"

        # Título da Etapa 6
        lbl_title = QLabel(tr("🎯 Etapa 6: Estudo de Cenários, Análise de Sensibilidade & Avaliação de Risco Legal"))
        lbl_title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {'#ffffff' if is_dark else '#0284c7'};")
        layout.addWidget(lbl_title)

        lbl_desc = QLabel(tr(
            "Avalie o comportamento hídrico da edificação em 7 cenários de sensibilidade e risco legal (de Worst Case a Best Case). "
            "Os cenários variam a Área de Captação, o Percentual de Uso Não Potável e a Demanda per capita em etapas de ±10% em conjunto, "
            "com explicação detalhada na tabela."
        ))
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #475569; font-size: 11.5px;")
        layout.addWidget(lbl_desc)

        # GroupBox 1: Tabela Editável de Cenários
        gb_editor = QGroupBox(tr("📋 Tabela de Cenários e Variação dos Parâmetros"))
        lay_ed = QVBoxLayout()

        # Toolbar de Botões
        tb_layout = QHBoxLayout()

        btn_risk = QPushButton(tr("⚖️ GERAR 7 CENÁRIOS DE RISCO (Worst to Best Case)"))
        btn_risk.setStyleSheet("font-weight: bold; font-size: 11.5px; background-color: #7c3aed; color: white; padding: 7px 14px; border-radius: 4px;")
        btn_risk.clicked.connect(self.load_risk_scenarios)
        tb_layout.addWidget(btn_risk)
        
        btn_add = QPushButton(tr("➕ Adicionar Cenário"))
        btn_add.setStyleSheet("font-weight: bold; background-color: #0284c7; color: white; padding: 7px 12px; border-radius: 4px;")
        btn_add.clicked.connect(lambda: self.add_scenario_row(name=f"{tr('Novo Cenário')} {self.table_input.rowCount()+1}"))
        tb_layout.addWidget(btn_add)

        btn_remove = QPushButton(tr("🗑️ Remover Selecionado"))
        btn_remove.setStyleSheet("font-weight: bold; background-color: #dc2626; color: white; padding: 7px 12px; border-radius: 4px;")
        btn_remove.clicked.connect(self.remove_selected_row)
        tb_layout.addWidget(btn_remove)

        tb_layout.addStretch()

        self.btn_run_sim = QPushButton(tr("🚀 SIMULAR CENÁRIOS E COMPARAR CURVAS"))
        self.btn_run_sim.setStyleSheet("font-weight: bold; font-size: 12px; background-color: #005a36; color: white; padding: 8px 16px; border-radius: 4px;")
        self.btn_run_sim.clicked.connect(self.run_scenarios_simulation)
        tb_layout.addWidget(self.btn_run_sim)

        lay_ed.addLayout(tb_layout)

        # Tabela de Entrada (8 Colunas incluindo a explicação de variação)
        self.table_input = QTableWidget()
        self.table_input.setColumnCount(8)
        self.table_input.setHorizontalHeaderLabels([
            tr("Cenário / Perfil"),
            tr("Variação dos Parâmetros (O que mudou)"),
            tr("Área Telhado (m²)"),
            tr("Subst. Pluvial (%)"), 
            tr("Demanda (L/hab/dia)"),
            tr("Moradores"),
            tr("Coef. C"),
            tr("Descarte (mm)")
        ])
        self.table_input.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_input.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table_input.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.table_input.setFixedHeight(210)
        self.table_input.itemChanged.connect(self.on_item_changed)
        lay_ed.addWidget(self.table_input)

        gb_editor.setLayout(lay_ed)
        layout.addWidget(gb_editor)

        # GroupBox 2: Gráfico Multi-Curvas de Potencial por Volume do Reservatório Inferior
        gb_chart = QGroupBox(tr("Gráfico de Potencial de Economia (%) vs Volume do Reservatório Inferior"))
        lay_ch = QVBoxLayout()
        
        self.chart_sweep_curves = MultiScenarioSweepChart(self)
        lay_ch.addWidget(self.chart_sweep_curves)

        gb_chart.setLayout(lay_ch)
        layout.addWidget(gb_chart)

        # GroupBox 3: Tabela de Resultados dos Cenários
        gb_table = QGroupBox(tr("Resumo de Desempenho e Enquadramento de Risco Legal"))
        lay_t = QVBoxLayout()

        self.table_results = QTableWidget()
        self.table_results.setColumnCount(9)
        self.table_results.setHorizontalHeaderLabels([
            tr("ID"),
            tr("Cenário / Perfil"),
            tr("Variação dos Parâmetros"),
            tr("Área (m²)"),
            tr("Moradores"),
            tr("Demanda (L/hab)"), 
            tr("% Pluvial"),
            tr("Vol. Ótimo (L)"),
            tr("Economia Potencial (%)")
        ])
        self.table_results.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_results.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.table_results.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

        self.table_results.setFixedHeight(180)
        lay_t.addWidget(self.table_results)

        gb_table.setLayout(lay_t)
        layout.addWidget(gb_table)

        layout.addStretch()
        self.setLayout(layout)

        # Carrega automaticamente os 7 cenários baseados na modelagem anterior
        self.load_risk_scenarios()

    def on_item_changed(self, item):
        if item is None:
            return
        col = item.column()
        # Não valida texto descritivo nas colunas 0 e 1
        if col in (0, 1):
            return

        val = item.text().strip()
        is_dark = get_current_theme() == "dark"
        if not val or val == "-" or not self.is_valid_number(val):
            item.setBackground(QBrush(QColor("#fef08a" if not is_dark else "#78350f")))
            item.setForeground(QBrush(QColor("#1e293b" if not is_dark else "#fef08a")))
        else:
            if is_dark:
                item.setBackground(QBrush(QColor("#1c1c1f")))
                item.setForeground(QBrush(QColor("#ffffff")))
            else:
                item.setBackground(QBrush(QColor("#ffffff")))
                item.setForeground(QBrush(QColor("#000000")))

    def is_valid_number(self, val_str):
        if not val_str or val_str == "-":
            return False
        try:
            v = float(val_str.replace(',', '.'))
            return v > 0
        except ValueError:
            return False

    def add_scenario_row(self, name="", variation_desc="", area=None, share=None, demand=None, residents=None, runoff=None, discard=None):
        r = self.table_input.rowCount()
        self.table_input.blockSignals(True)
        self.table_input.insertRow(r)
        
        if not name and area is not None:
            name = f"{tr('Cenário')} {r+1} ({area:.0f}m²)"

        items = [
            (0, str(name) if name else ""),
            (1, str(variation_desc) if variation_desc else "-"),
            (2, f"{area:.1f}" if area is not None else "-"),
            (3, f"{share:.1f}" if share is not None else "-"),
            (4, f"{demand:.1f}" if demand is not None else "-"),
            (5, f"{residents}" if residents is not None else "-"),
            (6, f"{runoff:.2f}" if runoff is not None else "-"),
            (7, f"{discard:.1f}" if discard is not None else "-"),
        ]

        is_dark = get_current_theme() == "dark"
        bg_yellow = QBrush(QColor("#fef08a" if not is_dark else "#78350f"))
        fg_yellow = QBrush(QColor("#1e293b" if not is_dark else "#fef08a"))
        bg_normal = QBrush(QColor("#ffffff" if not is_dark else "#1c1c1f"))
        fg_normal = QBrush(QColor("#000000" if not is_dark else "#ffffff"))

        for col, val in items:
            it = QTableWidgetItem(val)
            if col > 1 and (not val.strip() or val.strip() == "-" or not self.is_valid_number(val)):
                it.setBackground(bg_yellow)
                it.setForeground(fg_yellow)
            else:
                it.setBackground(bg_normal)
                it.setForeground(fg_normal)
            self.table_input.setItem(r, col, it)

        self.table_input.blockSignals(False)

    def remove_selected_row(self):
        curr_r = self.table_input.currentRow()
        if curr_r >= 0:
            self.table_input.removeRow(curr_r)

    def get_base_project_config(self):
        """Resgata as configurações ativas da edificação modeladas na Etapa 1 e Etapa 2."""
        mw = self.window()
        base = {
            "area": 100.0,
            "share": 40.0,
            "demand": 150.0,
            "residents": 4,
            "runoff": 0.75,
            "discard": 2.0
        }
        if mw and hasattr(mw, 'tab_building'):
            b_cfg = mw.tab_building.get_building_config()
            base["area"] = b_cfg.get("area", 100.0)
            base["residents"] = b_cfg.get("residents", 4)
            base["demand"] = b_cfg.get("demand", 150.0)
            base["share"] = b_cfg.get("share", 40.0)
            base["runoff"] = b_cfg.get("runoff_coeff", 0.75)

        if mw and hasattr(mw, 'tab_project'):
            try:
                disc = mw.tab_project.txt_discard.text().strip()
                if disc and disc != "-":
                    base["discard"] = float(disc.replace(',', '.'))
            except Exception:
                pass
        return base

    def load_risk_scenarios(self):
        """
        Gera 7 cenários normativos de risco e sensibilidade (Worst case a Best Case)
        variando em conjunto a Área, o Percentual de Uso Não Potável e o Consumo em etapas de ±10%.
        """
        base = self.get_base_project_config()
        b_area = base["area"]
        b_share = base["share"]
        b_demand = base["demand"]
        b_res = base["residents"]
        b_runoff = base["runoff"]
        b_discard = base["discard"]

        self.table_input.setRowCount(0)

        # Definição estrita das 7 variações (-30%, -20%, -10%, 0%, +10%, +20%, +30%)
        risk_cases = [
            ("Worst case",           -0.30, tr("Diminuídos em 30% (Área -30%, Uso Não Potável -30%, Consumo -30%)")),
            ("Bad case",             -0.20, tr("Diminuídos em 20% (Área -20%, Uso Não Potável -20%, Consumo -20%)")),
            ("Medium bad case",      -0.10, tr("Diminuídos em 10% (Área -10%, Uso Não Potável -10%, Consumo -10%)")),
            ("A simulada",            0.00, tr("Parâmetros Atuais do Projeto (Sem variação - 0%)")),
            ("Medium good case",     +0.10, tr("Aumentados em 10% (Área +10%, Uso Não Potável +10%, Consumo +10%)")),
            ("Good case",            +0.20, tr("Aumentados em 20% (Área +20%, Uso Não Potável +20%, Consumo +20%)")),
            ("Best case",            +0.30, tr("Aumentados em 30% (Área +30%, Uso Não Potável +30%, Consumo +30%)")),
        ]

        for name, pct, desc in risk_cases:
            area_v = max(10.0, b_area * (1.0 + pct))
            share_v = max(5.0, min(100.0, b_share * (1.0 + pct)))
            demand_v = max(20.0, b_demand * (1.0 + pct))

            self.add_scenario_row(
                name=name,
                variation_desc=desc,
                area=area_v,
                share=share_v,
                demand=demand_v,
                residents=b_res,
                runoff=b_runoff,
                discard=b_discard
            )

        self.run_scenarios_simulation()

    def run_range_scenarios(self):
        """Retrocompatibilidade para testes automatizados."""
        try:
            min_v = float(self.txt_min_val.text().replace(',', '.'))
            max_v = float(self.txt_max_val.text().replace(',', '.'))
            step_v = float(self.txt_step_val.text().replace(',', '.'))

            self.table_input.setRowCount(0)
            cur = min_v
            idx = 1
            while cur <= max_v + 1e-6:
                self.add_scenario_row(
                    name=f"{tr('Cenário')} {idx} ({cur:.0f}m²)",
                    variation_desc=f"Variação de Área para {cur:.0f}m²",
                    area=cur, share=40.0, demand=100.0, residents=3, runoff=0.9, discard=1.0
                )
                cur += step_v
                idx += 1

            self.run_scenarios_simulation()
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao gerar faixa')}:\n{str(e)}")

    def run_scenarios_simulation(self):
        try:
            r_count = self.table_input.rowCount()
            if r_count == 0:
                QMessageBox.warning(self, tr("Tabela Vazia"), tr("Por favor, adicione ao menos um cenário ou clique em 'Gerar 7 Cenários de Risco'."))
                return

            from netuno.ui.translation import get_current_theme
            is_dark = get_current_theme() == "dark"
            yellow_bg = QBrush(QColor("#fef08a" if not is_dark else "#78350f"))
            yellow_fg = QBrush(QColor("#1e293b" if not is_dark else "#fef08a"))
            invalid_rows = []

            for r in range(r_count):
                scen_name_item = self.table_input.item(r, 0)
                scen_name = scen_name_item.text().strip() if scen_name_item and scen_name_item.text().strip() else f"{tr('Cenário')} {r+1}"
                
                row_has_error = False
                for col_idx in range(2, 8):
                    item = self.table_input.item(r, col_idx)
                    val_str = item.text().strip() if item else ""
                    if not val_str or val_str == "-" or not self.is_valid_number(val_str):
                         row_has_error = True
                         if item:
                             item.setBackground(yellow_bg)
                             item.setForeground(yellow_fg)
                
                if row_has_error:
                    invalid_rows.append(scen_name)

            if invalid_rows:
                names_str = ", ".join(f"'{n}'" for n in invalid_rows)
                QMessageBox.warning(
                    self, 
                    tr("Preenchimento Incompleto"), 
                    f"{tr('Atenção: Os seguintes cenários possuem campos inválidos')}: {names_str}\n\n"
                    f"{tr('Por favor, preencha todos os números em amarelo antes de simular.')}"
                )
                return

            main_win = self.window()
            precip_data = None
            if main_win and hasattr(main_win, 'tab_project'):
                precip_data = main_win.tab_project.precip_data

            if precip_data is None or len(precip_data) == 0:
                QMessageBox.warning(self, tr("Aviso"), tr("Por favor, carregue uma série de chuva na Etapa 1 antes de executar os cenários."))
                return

            from netuno.core.parser import parse_float, parse_int, format_ptbr
            scenarios_data = []
            self.table_results.setRowCount(r_count)

            for r in range(r_count):
                scen_name = self.table_input.item(r, 0).text().strip() if self.table_input.item(r, 0) and self.table_input.item(r, 0).text().strip() else f"{tr('Cenário')} {r+1}"
                var_desc = self.table_input.item(r, 1).text().strip() if self.table_input.item(r, 1) and self.table_input.item(r, 1).text().strip() else "-"
                
                area_v = parse_float(self.table_input.item(r, 2).text() if self.table_input.item(r, 2) else "", 100.0)
                share_v = parse_float(self.table_input.item(r, 3).text() if self.table_input.item(r, 3) else "", 40.0)
                demand_v = parse_float(self.table_input.item(r, 4).text() if self.table_input.item(r, 4) else "", 100.0)
                res_v = parse_int(self.table_input.item(r, 5).text() if self.table_input.item(r, 5) else "", 3)
                runoff_v = parse_float(self.table_input.item(r, 6).text() if self.table_input.item(r, 6) else "", 0.75)
                discard_v = parse_float(self.table_input.item(r, 7).text() if self.table_input.item(r, 7) else "", 2.0)

                tot_demand = demand_v * res_v
                r_share = share_v / 100.0 if share_v > 1.0 else share_v

                sweep_res = run_sweep_simulation(
                    precip_data=precip_data,
                    lower_tank_max=10000.0,
                    lower_tank_step=500.0,
                    area=area_v,
                    runoff_coeff=runoff_v,
                    discard_mm=discard_v,
                    total_demand_per_day=tot_demand,
                    rainwater_share=r_share,
                    upper_tank_vol=500.0,
                    upper_tank_used=False,
                    pumping_threshold=375.0,
                    delta_ideal_threshold=5.0
                )

                vols = [sw.lower_tank_vol for sw in sweep_res.results_by_volume]
                pots = [sw.potential_potable_savings_pct for sw in sweep_res.results_by_volume]

                scenarios_data.append({
                    "name": scen_name,
                    "vols": vols,
                    "pots": pots,
                    "optimal_vol": sweep_res.optimal_lower_tank_vol,
                    "optimal_pot": sweep_res.optimal_potential_pct
                })

                scen_id = f"CEN_{r+1:02d}"
                self.table_results.setItem(r, 0, QTableWidgetItem(scen_id))
                self.table_results.setItem(r, 1, QTableWidgetItem(scen_name))
                self.table_results.setItem(r, 2, QTableWidgetItem(var_desc))
                self.table_results.setItem(r, 3, QTableWidgetItem(format_ptbr(area_v, 1)))
                self.table_results.setItem(r, 4, QTableWidgetItem(f"{res_v}"))
                self.table_results.setItem(r, 5, QTableWidgetItem(format_ptbr(demand_v, 0)))
                self.table_results.setItem(r, 6, QTableWidgetItem(f"{format_ptbr(share_v, 0)}%"))
                self.table_results.setItem(r, 7, QTableWidgetItem(f"{format_ptbr(sweep_res.optimal_lower_tank_vol, 0)} L" if sweep_res.optimal_lower_tank_vol else "N/A"))
                self.table_results.setItem(r, 8, QTableWidgetItem(f"{format_ptbr(sweep_res.optimal_potential_pct, 2)}%" if sweep_res.optimal_potential_pct else "0%"))

            self.chart_sweep_curves.update_chart(scenarios_data)

        except Exception as e:
            QMessageBox.critical(self, tr("Erro na Simulação"), f"{tr('Falha ao simular cenários')}:\n{str(e)}")
