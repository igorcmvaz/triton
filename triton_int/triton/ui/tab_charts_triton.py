"""
Etapa 4: Resultados Tecnicos — Balanco Hidrico, Diagrama 2D e Curvas Grid 2x2 (Triton).
Exibe o Diagrama Hidraulico 2D, KPIs numericos e os 4 graficos fundamentais.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QScrollArea, QFrame, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from triton.ui.translation import tr, get_current_theme
from triton.ui.hydraulic_diagram import HydraulicDiagramWidget
from triton.ui.charts import (
    PotentialVsVolumeChart, DeltaVsVolumeChart,
    SpillAndConsumptionVsVolumeChart, DaysSatisfactionVsVolumeChart
)
from triton.core.parser import format_ptbr


class TabChartsTriton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
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
        lbl_title = QLabel(tr("Resultados técnicos e balanço hídrico"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        main_layout.addWidget(lbl_title)

        # ===== LAYOUT SUPERIOR: Diagrama 2D (esq) + KPIs (dir) =====
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)

        # Esquerda: Diagrama Hidraulico 2D Interativo
        gb_diagram = QGroupBox(tr("\U0001f4a7 Diagrama Hidraulico 2D Interativo"))
        lay_diag = QVBoxLayout(gb_diagram)
        self.hydraulic_diagram = HydraulicDiagramWidget(self)
        lay_diag.addWidget(self.hydraulic_diagram)
        top_layout.addWidget(gb_diagram, stretch=3)

        # Direita: KPIs numericos em sub-tabs
        kpi_tabs = QTabWidget()
        kpi_tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #cbd5e1; }")

        # ── Sub-tab 1: Balanco Hidrico Geral ──
        tab_hid = QWidget()
        grid_res = QGridLayout(tab_hid)
        grid_res.setSpacing(10)

        font_val = QFont("Segoe UI", 12, QFont.Bold)
        font_lbl = QFont("Segoe UI", 9)

        def mk_card(label_text, color, row, col, grid):
            v = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFont(font_lbl)
            val = QLabel("--")
            val.setFont(font_val)
            val.setStyleSheet(f"color: {color};")
            v.addWidget(lbl)
            v.addWidget(val)
            grid.addLayout(v, row, col)
            return val

        self.val_pot        = mk_card(tr("Potencial de Economia"),              "#059669", 0, 0, grid_res)
        self.val_vol_annual = mk_card(tr("Vol. Pluvial Aproveitado"),            "#0284c7", 0, 1, grid_res)
        self.val_fin_annual = mk_card(tr("Economia Financeira Estimada"),        "#16a34a", 0, 2, grid_res)
        self.val_days_full  = mk_card(tr("Atendimento Total (Dias)"),            "#16a34a", 1, 0, grid_res)
        self.val_days_part  = mk_card(tr("Atendimento Parcial (Dias)"),          "#d97706", 1, 1, grid_res)
        self.val_days_null  = mk_card(tr("Sem Atendimento (Dias Secos)"),        "#dc2626", 1, 2, grid_res)
        self.val_spill      = mk_card(tr("Volume Extravasado (m3/ano)"),         "#475569", 2, 0, grid_res)
        self.val_daily_demand = mk_card(tr("Demanda Pluvial Diaria (L/dia)"),    "#0369a1", 2, 1, grid_res)
        self.val_opt_vol    = mk_card(tr("Volume Otimo Indicado (Varredura)"),   "#7c3aed", 2, 2, grid_res)
        self.val_phi_rule   = mk_card(tr("Regra Operacional (φ)"),               "#0284c7", 3, 0, grid_res)

        kpi_tabs.addTab(tab_hid, tr("\U0001f4ca Balanco Hidrico"))

        # ── Sub-tab 2: Motobomba e Energia ──
        tab_pump = QWidget()
        grid_pump = QGridLayout(tab_pump)
        grid_pump.setSpacing(10)

        self.val_pump_thresh  = mk_card(tr("Limiar Acionamento (Recalque)"),    "#0284c7", 0, 0, grid_pump)
        self.val_pump_power   = mk_card(tr("Potencia da Motobomba"),            "#0369a1", 0, 1, grid_pump)
        self.val_pump_cycles  = mk_card(tr("Acionamentos (Partidas/ano)"),      "#d97706", 0, 2, grid_pump)
        self.val_pump_energy  = mk_card(tr("Consumo de Energia (kWh/ano)"),     "#ca8a04", 1, 0, grid_pump)
        self.val_pump_cost    = mk_card(tr("Custo de Energia (R$/ano)"),        "#dc2626", 1, 1, grid_pump)
        self.val_pumped_vol   = mk_card(tr("Volume Total Recalcado (m3/ano)"),  "#059669", 1, 2, grid_pump)
        self.val_pump_batch   = mk_card(tr("Volume Medio por Partida (L)"),      "#7c3aed", 2, 0, grid_pump)

        kpi_tabs.addTab(tab_pump, tr("\u26a1 Motobomba & Energia"))

        # ── Sub-tab 3: Usos Discretizados & Irrigação ──
        tab_disc = QWidget()
        grid_disc = QGridLayout(tab_disc)
        grid_disc.setSpacing(10)

        self.val_pot_indoor = mk_card(tr("Potável Interno Rede (m³/ano)"), "#0284c7", 0, 0, grid_disc)
        self.val_pluv_indoor = mk_card(tr("Não-Potável Interno Cisterna (m³/ano)"), "#059669", 0, 1, grid_disc)
        self.val_pluv_irr = mk_card(tr("Irrigação Cisterna (m³/ano)"), "#16a34a", 0, 2, grid_disc)
        self.val_irr_supp_vol = mk_card(tr("Água Poupada por Chuva (m³/ano)"), "#7c3aed", 1, 0, grid_disc)
        self.val_irr_supp_days = mk_card(tr("Dias c/ Irrigação Dispensada"), "#d97706", 1, 1, grid_disc)
        self.val_irr_active_days = mk_card(tr("Dias c/ Irrigação Ativa"), "#0369a1", 1, 2, grid_disc)

        kpi_tabs.addTab(tab_disc, tr("🌿 Usos & Irrigação"))

        top_layout.addWidget(kpi_tabs, stretch=2)
        main_layout.addLayout(top_layout)

        # ===== GRID 2x2 DE GRAFICOS =====
        gb_charts = QGroupBox(tr("\U0001f4c8 Curvas de Desempenho e Dimensionamento (Grid 2x2)"))
        grid_layout = QGridLayout(gb_charts)
        grid_layout.setSpacing(12)

        gb1 = QGroupBox(tr("Potencial de Economia de Agua Potavel (%)"))
        lay1 = QVBoxLayout(gb1)
        self.chart_pot = PotentialVsVolumeChart()
        lay1.addWidget(self.chart_pot)
        grid_layout.addWidget(gb1, 0, 0)

        gb2 = QGroupBox(tr("Variacao do Potencial / Delta Marginal (%/m3)"))
        lay2 = QVBoxLayout(gb2)
        self.chart_delta = DeltaVsVolumeChart()
        lay2.addWidget(self.chart_delta)
        grid_layout.addWidget(gb2, 0, 1)

        gb3 = QGroupBox(tr("Volume Anual Extravasado & Consumo Pluvial (Eixo Duplo)"))
        lay3 = QVBoxLayout(gb3)
        self.chart_spill_cons = SpillAndConsumptionVsVolumeChart()
        lay3.addWidget(self.chart_spill_cons)
        grid_layout.addWidget(gb3, 1, 0)

        gb4 = QGroupBox(tr("Percentual de Dias de Atendimento no Ano (%)"))
        lay4 = QVBoxLayout(gb4)
        self.chart_days = DaysSatisfactionVsVolumeChart()
        lay4.addWidget(self.chart_days)
        grid_layout.addWidget(gb4, 1, 1)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        main_layout.addWidget(gb_charts, stretch=1)

        scroll.setWidget(content_widget)
        main_vbox.addWidget(scroll)

    def update_charts_data(self, sweep_result=None, single_result=None, optimal_vol=None, delta_threshold=1.0):
        """Atualiza graficos e KPIs com os resultados da simulacao."""
        results = sweep_result.results_by_volume if (sweep_result and hasattr(sweep_result, "results_by_volume")) else None
        opt_v = optimal_vol if optimal_vol is not None else (sweep_result.optimal_lower_tank_vol if (sweep_result and hasattr(sweep_result, "optimal_lower_tank_vol")) else None)

        self.chart_pot.update_chart(sweep_results=results, single_result=single_result, optimal_vol=opt_v)
        self.chart_delta.update_chart(sweep_results=results, single_result=single_result, delta_threshold=delta_threshold)
        self.chart_spill_cons.update_chart(sweep_results=results, single_result=single_result)
        self.chart_days.update_chart(sweep_results=results, single_result=single_result)

        # Atualiza KPIs
        if single_result:
            res = single_result
            main_win = self.window()
            b_cfg = {}
            if main_win and hasattr(main_win, "tab_building"):
                b_cfg = main_win.tab_building.get_building_config()
            tot_demand = b_cfg.get("demand", 200.0) * b_cfg.get("residents", 4)
            share = b_cfg.get("share", 0.4)
            total_days = getattr(res, "total_days", 365) if hasattr(res, "total_days") else len(getattr(main_win.tab_tanks_simulation, "precip_data", []) or []) or 365
            num_full = int(round((res.pct_days_full_satisfaction / 100.0) * total_days))
            num_part = int(round((res.pct_days_partial_satisfaction / 100.0) * total_days))
            num_null = total_days - num_full - num_part

            sym = "R$"
            if main_win and hasattr(main_win, "tab_tanks_simulation"):
                sym = main_win.tab_tanks_simulation.get_currency_symbol()

            # Tarifa estimada
            # Tarifa de recurso, se a conta falhar: a média brasileira só vale em reais.
            tariff_ws = 11.70 if sym == "R$" else 0.0
            if main_win and hasattr(main_win, "config"):
                try:
                    from triton.core.economic import calculate_effective_tariff
                    tw, ts = calculate_effective_tariff(
                        main_win.config,
                        res.annual_pluvial_consumed_m3,
                        annual_total_demand_m3=(res.annual_pluvial_consumed_m3 + res.annual_potable_consumed_m3),
                    )
                    tariff_ws = tw + ts
                except Exception:
                    pass

            est_fin = res.annual_pluvial_consumed_m3 * tariff_ws
            is_tech_only = False
            if main_win and hasattr(main_win, "tab_tanks_simulation"):
                is_tech_only = getattr(main_win.tab_tanks_simulation, "_is_technical_only", False)

            self.val_pot.setText(f"{format_ptbr(res.potential_potable_savings_pct, 2)} %")
            self.val_vol_annual.setText(tr('{0} m³/ano').format(format_ptbr(res.annual_pluvial_consumed_m3, 1)))
            self.val_fin_annual.setText("--" if is_tech_only else tr("{0} {1}/ano").format(sym, format_ptbr(est_fin, 2)))
            self.val_days_full.setText(tr('{0} dias ({1}%)').format(num_full, format_ptbr(res.pct_days_full_satisfaction, 1)))
            self.val_days_part.setText(tr('{0} dias ({1}%)').format(num_part, format_ptbr(res.pct_days_partial_satisfaction, 1)))
            self.val_days_null.setText(tr('{0} dias ({1}%)').format(num_null, format_ptbr(res.pct_days_null_satisfaction, 1)))
            self.val_spill.setText(tr('{0} m³/ano').format(format_ptbr(res.total_overflow_liters / 1000.0, 1)))
            self.val_daily_demand.setText(tr('{0} L/dia').format(format_ptbr(tot_demand * share, 0)))
            self.val_opt_vol.setText(f"{format_ptbr(opt_v, 0)} L" if opt_v else "--")
            phi_label = getattr(res, "operation_rule_name", "") or "Triton"
            self.val_phi_rule.setText(phi_label)

            # KPIs da motobomba
            cfg_kw = 0.36775; cfg_elec = 1.0; cfg_eff = 55.0
            cfg_flow = 2280.0; cfg_startup = 0.03
            if main_win and hasattr(main_win, "config"):
                c = main_win.config
                cfg_kw = c.pump_power_kw
                cfg_elec = c.elec_tariff
                cfg_eff = c.pump_efficiency
                cfg_flow = c.pump_flow_rate
                cfg_startup = c.pump_startup_time_h

            upper_used = main_win.tab_tanks_simulation.combo_upper_mode.currentIndex() != 2 if (main_win and hasattr(main_win, "tab_tanks_simulation")) else True
            try:
                pump_thresh_pct = float(main_win.tab_tanks_simulation.txt_pump_thresh_pct.text().replace(",", ".")) if main_win and hasattr(main_win, "tab_tanks_simulation") else 10.0
                upper_vol = float(main_win.tab_tanks_simulation.txt_upper_vol.text().replace(",", ".")) if main_win and hasattr(main_win, "tab_tanks_simulation") else 500.0
            except Exception:
                pump_thresh_pct = 10.0; upper_vol = 500.0
            pump_thresh_vol = (upper_vol * (pump_thresh_pct / 100.0)) if upper_used else 0.0

            num_years = max(1.0, total_days / 365.25)
            annual_cycles = int(round(res.total_pump_cycles / num_years))
            annual_pumped_m3 = (res.total_pumped_liters / num_years) / 1000.0
            cfg_power_cv = cfg_kw / 0.735499

            if upper_used and cfg_flow > 0:
                t_rec = (res.total_pumped_liters / num_years) / cfg_flow
                t_part = annual_cycles * cfg_startup
                eta = max(0.01, cfg_eff / 100.0)
                energy_kwh = (cfg_kw * (t_rec + t_part)) / eta
                energy_cost = energy_kwh * cfg_elec
            else:
                energy_kwh = 0.0; energy_cost = 0.0

            self.val_pump_thresh.setText(f"{format_ptbr(pump_thresh_pct, 1)}% ({format_ptbr(pump_thresh_vol, 0)} L)" if upper_used else tr("Sem Res. Sup."))
            self.val_pump_power.setText(f"{format_ptbr(cfg_power_cv, 2)} CV ({format_ptbr(cfg_kw, 3)} kW)")
            self.val_pump_cycles.setText(tr('{0} partidas/ano').format(format_ptbr(annual_cycles, 0)))
            self.val_pump_energy.setText(tr('{0} kWh/ano').format(format_ptbr(energy_kwh, 1)))
            self.val_pump_cost.setText(tr('{0} {1}/ano').format(sym, format_ptbr(energy_cost, 2)))
            self.val_pumped_vol.setText(tr('{0} m³/ano').format(format_ptbr(annual_pumped_m3, 1)))
            self.val_pump_batch.setText(f"{format_ptbr(res.average_pumped_liters_per_cycle, 1)} L/partida")

            # KPIs discretizados e irrigação
            self.val_pot_indoor.setText(tr('{0} m³/ano').format(format_ptbr(res.annual_potable_consumed_m3, 1)))
            self.val_pluv_indoor.setText(tr('{0} m³/ano').format(format_ptbr(res.annual_pluvial_indoor_consumed_m3, 1)))
            self.val_pluv_irr.setText(tr('{0} m³/ano').format(format_ptbr(res.annual_pluvial_irrigation_consumed_m3, 1)))
            self.val_irr_supp_vol.setText(tr('{0} m³/ano').format(format_ptbr(res.annual_irrigation_volume_suppressed_m3, 1)))
            self.val_irr_supp_days.setText(tr('{0} dias/ano').format(res.total_irrigation_days_suppressed))
            self.val_irr_active_days.setText(tr('{0} dias/ano').format(res.total_irrigation_days_active))

        # Atualiza diagrama hidraulico
        main_win = self.window()
        if main_win and hasattr(main_win, "tab_tanks_simulation"):
            ts = main_win.tab_tanks_simulation
            try:
                from triton.core.parser import parse_float as pf
                b_cfg = main_win.tab_building.get_building_config() if hasattr(main_win, "tab_building") else {}
                area_val = b_cfg.get("area", 100.0)
                demand_val = b_cfg.get("demand", 200.0) * b_cfg.get("residents", 4) * b_cfg.get("share", 0.4)
                discard_val = pf(main_win.tab_project.txt_discard.text(), 2.0) if hasattr(main_win, "tab_project") else 2.0
                upper_mode = ts.combo_upper_mode.currentIndex()
                upper_used2 = (upper_mode != 2)
                upper_v = pf(ts.txt_upper_vol.text(), 320.0)
                lower_v = single_result.lower_tank_vol if single_result else 5000.0
                pot_pct = single_result.potential_potable_savings_pct if single_result else 0.0
                self.hydraulic_diagram.update_params(
                    area=area_val, discard=discard_val, lower_vol=lower_v,
                    upper_vol=upper_v, upper_used=upper_used2,
                    potential_pct=pot_pct, pluvial_demand=demand_val
                )
            except Exception:
                pass
