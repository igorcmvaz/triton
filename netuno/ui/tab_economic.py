"""
Aba de Análise Econômica & Viabilidade Financeira do Netuno 5 (PySide6).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

from netuno.core.economic import calculate_economic_indicators


class TabEconomicAnalysis(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # === PAINEL ESQUERDO: INPUTS FINANCEIROS ===
        left_panel = QVBoxLayout()

        group_econ = QGroupBox("Parâmetros Econômicos && Tarifários")
        grid = QGridLayout()

        grid.addWidget(QLabel("Custo do Sistema (R$):"), 0, 0)
        self.spin_capex = QDoubleSpinBox()
        self.spin_capex.setRange(100.0, 1000000.0)
        self.spin_capex.setSingleStep(500.0)
        self.spin_capex.setValue(8500.0)
        grid.addWidget(self.spin_capex, 0, 1)

        grid.addWidget(QLabel("Manutenção Anual (R$/ano):"), 1, 0)
        self.spin_opex = QDoubleSpinBox()
        self.spin_opex.setRange(0.0, 50000.0)
        self.spin_opex.setValue(150.0)
        grid.addWidget(self.spin_opex, 1, 1)

        grid.addWidget(QLabel("Tarifa de Água (R$/m³):"), 2, 0)
        self.spin_tariff = QDoubleSpinBox()
        self.spin_tariff.setRange(0.5, 200.0)
        self.spin_tariff.setValue(8.50)
        grid.addWidget(self.spin_tariff, 2, 1)

        grid.addWidget(QLabel("Reajuste Anual Tarifa (%/ano):"), 3, 0)
        self.spin_esc = QDoubleSpinBox()
        self.spin_esc.setRange(0.0, 50.0)
        self.spin_esc.setValue(6.0)
        grid.addWidget(self.spin_esc, 3, 1)

        grid.addWidget(QLabel("Taxa de Desconto / SELIC (%/ano):"), 4, 0)
        self.spin_discount = QDoubleSpinBox()
        self.spin_discount.setRange(0.0, 50.0)
        self.spin_discount.setValue(8.0)
        grid.addWidget(self.spin_discount, 4, 1)

        grid.addWidget(QLabel("Horizonte de Análise (Anos):"), 5, 0)
        self.spin_horizon = QSpinBox()
        self.spin_horizon.setRange(1, 50)
        self.spin_horizon.setValue(20)
        grid.addWidget(self.spin_horizon, 5, 1)

        grid.addWidget(QLabel("Economia Pluvial Estimada (m³/ano):"), 6, 0)
        self.spin_water_saved = QDoubleSpinBox()
        self.spin_water_saved.setRange(1.0, 100000.0)
        self.spin_water_saved.setValue(85.0)  # Ex: 85 m3/ano
        grid.addWidget(self.spin_water_saved, 6, 1)

        group_econ.setLayout(grid)
        left_panel.addWidget(group_econ)

        self.btn_calc = QPushButton("💰 CALCULAR PAYBACK && VPL")
        self.btn_calc.setProperty("class", "btn-gold")
        self.btn_calc.setStyleSheet("font-size: 14px; padding: 12px;")
        self.btn_calc.clicked.connect(self.calculate_economics)
        left_panel.addWidget(self.btn_calc)

        left_panel.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(340)
        main_layout.addWidget(left_widget)

        # === PAINEL DIREITO: RESULTADOS FINANCEIROS ===
        right_panel = QVBoxLayout()

        kpi_layout = QGridLayout()

        self.card_vpl = self.create_kpi("Valor Presente Líquido (VPL)", "R$ --", "#10b981")
        self.card_payback = self.create_kpi("Payback Simples", "-- Anos", "#f59e0b")
        self.card_payback_disc = self.create_kpi("Payback Descontado", "-- Anos", "#00b4d8")
        self.card_savings_tot = self.create_kpi("Economia Acumulada no Período", "R$ --", "#2a9d8f")

        kpi_layout.addWidget(self.card_vpl, 0, 0)
        kpi_layout.addWidget(self.card_payback, 0, 1)
        kpi_layout.addWidget(self.card_payback_disc, 1, 0)
        kpi_layout.addWidget(self.card_savings_tot, 1, 1)

        right_panel.addLayout(kpi_layout)
        right_panel.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        main_layout.addWidget(right_widget)

        self.setLayout(main_layout)

    def create_kpi(self, title, val_str, color):
        group = QGroupBox(title)
        layout = QVBoxLayout()
        lbl = QLabel(val_str)
        lbl.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        group.setLayout(layout)
        group.lbl_val = lbl
        return group

    def calculate_economics(self):
        try:
            capex = self.spin_capex.value()
            opex = self.spin_opex.value()
            tariff = self.spin_tariff.value()
            esc = self.spin_esc.value() / 100.0
            discount = self.spin_discount.value() / 100.0
            horizon = self.spin_horizon.value()
            water_saved_m3 = self.spin_water_saved.value()

            econ = calculate_economic_indicators(
                initial_investment=capex,
                annual_water_saved_m3=water_saved_m3,
                water_tariff_per_m3=tariff,
                tariff_escalation_rate=esc,
                discount_rate=discount,
                annual_om_cost=opex,
                analysis_period_years=horizon
            )

            self.card_vpl.lbl_val.setText(f"R$ {econ.npv:,.2f}")
            self.card_payback.lbl_val.setText(f"{econ.payback_simple_years:.1f} Anos" if econ.payback_simple_years else "N/A")
            self.card_payback_disc.lbl_val.setText(f"{econ.payback_discounted_years:.1f} Anos" if econ.payback_discounted_years else "N/A")
            self.card_savings_tot.lbl_val.setText(f"R$ {econ.total_net_savings:,.2f}")

        except Exception as e:
            QMessageBox.critical(self, "Erro no Cálculo Financeiro", f"Erro: {str(e)}")
