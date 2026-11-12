"""
Aba do Otimizador Econômico Global de Reservatórios do Triton (PySide6).
Consolida os resultados das 3 dimensões (Técnica, Econômica e Ambiental) para todos os volumes da varredura,
aplicando a Otimização Multi-Critério TOPSIS com Seletor de Relevância / Pesos de Decisão.
"""

import numpy as np
from triton.core.numero import decimal, milhar
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDoubleSpinBox, QSpinBox,
    QApplication, QScrollArea, QFrame, QSizePolicy, QTabWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from triton.core.taxas import mensal_pct_para_anual_fracao
from triton.core.parser import TritonConfig, format_ptbr, parse_float
from triton.core.economic import run_robust_economic_analysis, calculate_effective_tariff
from triton.core.environmental import EnvironmentalConfig, run_environmental_sweep
from triton.core.topsis import (PESOS_PADRAO, PARTES_NO_EIXO_PADRAO, PARTES_IGUAIS_NO_EIXO, CRITERION_LABELS, validar_partes_no_eixo,
                                payback_do_criterio, TopsisCandidate, calculate_topsis_scores)
from triton.core.mcdm_methods import run_smaa_vikor, run_vikor, run_promethee, VikorResult, PrometheeResult
from triton.core.system_weight import calculate_system_weight_from_config
from triton.core.cost_estimates import (
    precos_de_catalogo,
    annualize_operational_costs,
    estimate_annual_chlorination_cost,
)
from triton.ui.charts import TOPSISComparisonChart, TOPSISProximityChart
from triton.ui.translation import tr, get_current_lang, get_current_theme


class TabEconomicGlobalOptimizer(QWidget):
    optimization_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scenarios = []
        self._updating_table = False
        self._updating_weights = False
        self.last_topsis_result = None
        self.last_mcdm_result = None
        self.last_smaa_vikor_result = None
        # Resultados completos por alternativa para relatórios e rastreabilidade.
        self.last_scenario_results = []
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        surface = "#27272a" if is_dark else "#ffffff"
        border = "#3f3f46" if is_dark else "#cbd5e1"
        heading = "#f4f4f5" if is_dark else "#1e293b"
        body = "#d4d4d8" if is_dark else "#334155"
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        main_vbox = QVBoxLayout(content)
        main_vbox.setContentsMargins(40, 34, 40, 40)
        main_vbox.setSpacing(16)

        lbl_title = QLabel(tr("Otimização multicritério e cenários"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        main_vbox.addWidget(lbl_title)

        # ── CONTROLE DE RELEVÂNCIA E PESOS DOS CRITÉRIOS (SELETOR TOPSIS / SMAA-VIKOR) ──
        gb_weights = QGroupBox(tr("⚖️ Método e configuração da decisão multicritério"))
        gb_weights.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        gb_weights.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        gb_weights.setMaximumHeight(200)
        lay_w = QVBoxLayout(gb_weights)
        lay_w.setContentsMargins(8, 6, 8, 6)
        lay_w.setSpacing(3)

        profile_row = QHBoxLayout()
        profile_row.setSpacing(8)
        profile_row.addWidget(QLabel(f"<b>{tr('Método:')}</b>"))
        self.combo_mcdm_method = QComboBox()
        self.combo_mcdm_method.addItem(tr("🏆 TOPSIS (Pesos Fixos por Perfil de Decisão)"), "topsis")
        self.combo_mcdm_method.addItem(tr("🤝 VIKOR (Solução de Compromisso Direta)"), "vikor")
        self.combo_mcdm_method.addItem(
            tr("🎲 SMAA-VIKOR (Simulações Estocásticas no Simplex / Cryspin)"), "smaa_vikor"
        )
        self.combo_mcdm_method.addItem(tr("⚖️ PROMETHEE II (Superação Completa por Fluxos Líquidos)"), "promethee")
        self.combo_mcdm_method.currentIndexChanged.connect(self.on_method_changed)
        self.combo_mcdm_method.setFixedHeight(28)
        profile_row.addWidget(self.combo_mcdm_method)

        profile_row.addSpacing(10)
        self.lbl_profile = QLabel(tr("Perfil de decisão:"))
        profile_row.addWidget(self.lbl_profile)

        # Perfil de pesos determinísticos para TOPSIS
        self.combo_preset = QComboBox()
        self.combo_preset.addItem(tr("⚖️ Relevâncias Similares (Equilibrado: 25% em cada eixo)"), "equilibrado")
        self.combo_preset.addItem(tr("💰 Priorizar Retorno Econômico (70% Econômico / 10% em cada outro eixo)"), "economico")
        self.combo_preset.addItem(tr("🍃 Priorizar Sustentabilidade Ambiental (70% Ambiental / 10% em cada outro eixo)"), "ambiental")
        self.combo_preset.addItem(tr("💧 Priorizar Desempenho Técnico (70% Técnico / 10% em cada outro eixo)"), "tecnico")
        self.combo_preset.addItem(tr("🏗️ Priorizar Leveza e Drenagem (70% Estrutural / 10% em cada outro eixo)"), "estrutural")
        self.combo_preset.addItem(tr("⚙️ Personalizado (Ajuste Manual dos Pesos)"), "custom")
        self.combo_preset.currentIndexChanged.connect(self.on_preset_changed)
        self.combo_preset.setMaximumWidth(520)
        self.combo_preset.setFixedHeight(28)
        profile_row.addWidget(self.combo_preset)

        # Perfil de contagem de simulações para SMAA-VIKOR (Padrão Cryspin)
        self.combo_smaa_profile = QComboBox()
        self.combo_smaa_profile.addItem(tr("⚡ Rápido — 1.000 simulações Monte Carlo"), 1000)
        self.combo_smaa_profile.addItem(tr("✅ Recomendado — 5.000 simulações Monte Carlo"), 5000)
        self.combo_smaa_profile.addItem(tr("📊 Robusto — 10.000 simulações Monte Carlo"), 10000)
        self.combo_smaa_profile.addItem(tr("🔬 Alta precisão — 20.000 simulações Monte Carlo"), 20000)
        self.combo_smaa_profile.addItem(tr("💎 Ultra rigor — 50.000 simulações Monte Carlo"), 50000)
        self.combo_smaa_profile.addItem(tr("⚙️ Personalizado (Definir Simulações)"), "custom")
        self.combo_smaa_profile.setCurrentIndex(3)
        self.combo_smaa_profile.setMaximumWidth(520)
        self.combo_smaa_profile.setFixedHeight(28)
        self.combo_smaa_profile.setVisible(False)
        self.combo_smaa_profile.currentIndexChanged.connect(self.on_smaa_profile_changed)
        profile_row.addWidget(self.combo_smaa_profile)

        # Spinbox para simulações customizadas no SMAA-VIKOR
        self.spin_smaa_custom_samples = QSpinBox()
        self.spin_smaa_custom_samples.setRange(100, 100000)
        self.spin_smaa_custom_samples.setValue(20000)
        self.spin_smaa_custom_samples.setSingleStep(500)
        self.spin_smaa_custom_samples.setSuffix(tr(" simulações"))
        self.spin_smaa_custom_samples.setFixedHeight(28)
        self.spin_smaa_custom_samples.setFixedWidth(130)
        self.spin_smaa_custom_samples.setVisible(False)
        self.spin_smaa_custom_samples.valueChanged.connect(self.on_smaa_custom_samples_changed)
        profile_row.addWidget(self.spin_smaa_custom_samples)

        profile_row.addStretch()
        lay_w.addLayout(profile_row)

        # Linha de parâmetros: pesos fixos (TOPSIS) ou parâmetros estocásticos (SMAA-VIKOR)
        weights_row = QHBoxLayout()
        weights_row.setSpacing(8)

        # Labels e Spinners de Pesos TOPSIS: um por eixo (técnico, econômico, ambiental, estrutural)
        def _spin_de_peso(rotulo):
            lbl = QLabel(rotulo)
            weights_row.addWidget(lbl)
            spin = QDoubleSpinBox()
            spin.setRange(0.0, 100.0)
            spin.setValue(25.0)
            spin.setSuffix("%")
            spin.setDecimals(1)
            spin.setSingleStep(1.0)
            spin.setFixedWidth(100)
            spin.setFixedHeight(28)
            spin.valueChanged.connect(self.on_spin_weight_changed)
            weights_row.addWidget(spin)
            return lbl, spin

        self.lbl_w_tech, self.spin_w_tech = _spin_de_peso(tr("💧 Técnico:"))
        self.lbl_w_fin, self.spin_w_fin = _spin_de_peso(tr("💰 Econômico:"))
        self.lbl_w_env, self.spin_w_env = _spin_de_peso(tr("🍃 Ambiental:"))
        self.lbl_w_struct, self.spin_w_struct = _spin_de_peso(tr("🏗️ Estrutural:"))
        self.lbl_w_struct.setToolTip(tr("Eixo estrutural: massa a seco dos materiais e volume extravasado por ano."))

        # Parâmetro v do VIKOR (Consenso vs Arrependimento) para SMAA-VIKOR
        self.lbl_v_param = QLabel(tr("⚖️ Consenso VIKOR (v):"))
        self.lbl_v_param.setToolTip(tr("Peso da estratégia de consenso VIKOR: 0,50 = Equilibrado; >0,50 = Prioriza utilidade de grupo; <0,50 = Prioriza arrependimento individual."))
        weights_row.addWidget(self.lbl_v_param)
        self.spin_v_param = QDoubleSpinBox()
        self.spin_v_param.setRange(0.0, 1.0)
        self.spin_v_param.setValue(0.50)
        self.spin_v_param.setSingleStep(0.05)
        self.spin_v_param.setDecimals(2)
        self.spin_v_param.setFixedWidth(90)
        self.spin_v_param.setFixedHeight(28)
        self.spin_v_param.setToolTip(tr("Peso da estratégia de consenso VIKOR (v): 0,50 = Equilibrado."))
        self.spin_v_param.valueChanged.connect(self.on_v_param_changed)
        weights_row.addWidget(self.spin_v_param)
        self.lbl_v_param.setVisible(False)
        self.spin_v_param.setVisible(False)

        self.btn_recalc = QPushButton(tr("⚡ Recalcular"))
        self.btn_recalc.setStyleSheet("background-color: #059669; color: white; font-weight: bold; padding: 6px 12px;")
        self.btn_recalc.setFixedHeight(28)
        self.btn_recalc.clicked.connect(self.recalculate_all)
        weights_row.addWidget(self.btn_recalc)

        self.lbl_weight_validation = QLabel()
        self.lbl_weight_validation.setStyleSheet("font-size: 10px; color: #047857; font-weight: bold;")
        weights_row.addWidget(self.lbl_weight_validation)
        weights_row.addStretch()
        lay_w.addLayout(weights_row)

        # Partes no eixo: quanto do peso de cada eixo vai para cada critério do eixo (TOPSIS com oito critérios).
        shares_row = QHBoxLayout()
        shares_row.setSpacing(6)
        self._shares_widgets = []
        lbl_shares = QLabel(tr("Partes no eixo:"))
        lbl_shares.setToolTip(tr("Quanto do peso de cada eixo vai para cada critério do eixo (só a proporção dentro do eixo importa). "
                                 "Padrão: partes iguais dentro de cada eixo. Parte zero tira o critério da conta."))
        shares_row.addWidget(lbl_shares)
        self._shares_widgets.append(lbl_shares)
        self.spin_shares = []
        nomes_curtos = (tr("Confiabilidade"), tr("Eficiência"), tr("Economia"), tr("LCOW"), tr("Payback"),
                        tr("CO₂"), tr("Massa"), tr("Extravasamento"))
        for nome, completo, parte in zip(nomes_curtos, CRITERION_LABELS, PARTES_NO_EIXO_PADRAO):
            lbl = QLabel(nome)
            lbl.setToolTip(tr(completo))
            spin = QDoubleSpinBox()
            spin.setRange(0.0, 100.0)
            spin.setDecimals(0)
            spin.setSingleStep(10.0)
            spin.setValue(100.0 * parte)
            spin.setFixedWidth(58)
            spin.setFixedHeight(26)
            spin.setToolTip(tr(completo))
            spin.valueChanged.connect(self.on_shares_changed)
            shares_row.addWidget(lbl)
            shares_row.addWidget(spin)
            self.spin_shares.append(spin)
            self._shares_widgets += [lbl, spin]
        self.btn_shares_default = QPushButton(tr("Partes iguais"))
        self.btn_shares_default.setFixedHeight(26)
        self.btn_shares_default.setToolTip(tr("Os oito critérios com a mesma parte dentro do seu eixo (o padrão)."))
        self.btn_shares_default.clicked.connect(lambda: self.reset_shares(PARTES_NO_EIXO_PADRAO))
        # O padrão é a partilha igual: um só botão, com os dois nomes que o código usa.
        self.btn_shares_equal = self.btn_shares_default
        shares_row.addWidget(self.btn_shares_default)
        self._shares_widgets.append(self.btn_shares_default)
        shares_row.addStretch()
        lay_w.addLayout(shares_row)
        self._update_weight_validation()

        main_vbox.addWidget(gb_weights)

        # ── TABELA COMPARATIVA AJUSTADA (TODAS AS COLUNAS UNIFORMES E VISÍVEIS) ──
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels([
            tr("Opção"),
            tr("Cisterna\n(L)"),
            tr("Caixa\n(L)"),
            tr("Economia\n(%)"),
            tr("Extravas.\n(m³/ano)"),
            tr("Vol. Pluvial\n(m³/ano)"),
            tr("Água Potável\n(m³/ano)"),
            tr("Atend.\n(dias)"),
            tr("VPL\n(R$)"),
            tr("PB Desc.\n(anos)"),
            tr("TIR\n(% a.a.)"),
            tr("CO₂ Líquido\nFim de Vida (kg)"),
            tr("PB Amb.\n(anos)"),
            tr("TOPSIS\nScore"),
            tr("Rank")
        ])
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setMinimumHeight(38)
        
        for col in range(15):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        
        self.table.setFixedHeight(240)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setTextElideMode(Qt.ElideRight)
        self.table.setStyleSheet(
            "QTableWidget { font-size: 13px; } "
            "QHeaderView::section { font-size: 12px; font-weight: bold; padding: 4px 2px; }"
        )
        main_vbox.addWidget(self.table, stretch=2)

        # Painel de Conclusão Executiva da Decisão Multi-Critério (MCDM)
        self.gb_best = QGroupBox(tr("🏆 Conclusão da Decisão Multi-Critério"))
        self.gb_best.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; background-color: {surface}; border: 1px solid {border}; border-radius: 6px; }}")
        lay_best = QVBoxLayout(self.gb_best)
        lay_best.setContentsMargins(10, 8, 10, 8)
        lay_best.setSpacing(6)

        grid_cards = QGridLayout()
        grid_cards.setSpacing(6)

        self.lbl_best_tech = QLabel(tr("💧 Ótimo Técnico (pós-limiar): --"))
        self.lbl_best_tech.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.lbl_best_tech.setStyleSheet("color: #0284c7; background: #e0f2fe; padding: 5px 8px; border-radius: 4px;")
        self.lbl_best_tech.setWordWrap(True)

        self.lbl_best_vpl = QLabel(tr("💵 Ótimo Econômico (Menor Payback): --"))
        self.lbl_best_vpl.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.lbl_best_vpl.setStyleSheet("color: #047857; background: #dcfce7; padding: 5px 8px; border-radius: 4px;")
        self.lbl_best_vpl.setWordWrap(True)

        self.lbl_best_env = QLabel(tr("🍃 Ótimo Ambiental (Maior CO2 Evitado): --"))
        self.lbl_best_env.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.lbl_best_env.setStyleSheet("color: #059669; background: #d1fae5; padding: 5px 8px; border-radius: 4px;")
        self.lbl_best_env.setWordWrap(True)

        self.lbl_best_topsis = QLabel(tr("🏆 Ótimo TOPSIS: --"))
        self.lbl_best_topsis.setFont(QFont("Segoe UI", 9.5, QFont.Bold))
        self.lbl_best_topsis.setStyleSheet("color: #4338ca; background: #e0e7ff; padding: 6px 10px; border-radius: 4px;")
        self.lbl_best_topsis.setWordWrap(True)

        self.lbl_best_vikor = QLabel(tr("🎲 Ótimo VIKOR / SMAA: --"))
        self.lbl_best_vikor.setFont(QFont("Segoe UI", 9.5, QFont.Bold))
        self.lbl_best_vikor.setStyleSheet("color: #b45309; background: #fef3c7; padding: 6px 10px; border-radius: 4px;")
        self.lbl_best_vikor.setWordWrap(True)

        self.lbl_best_promethee = QLabel(tr("⚖️ Ótimo PROMETHEE II: --"))
        self.lbl_best_promethee.setFont(QFont("Segoe UI", 9.5, QFont.Bold))
        self.lbl_best_promethee.setStyleSheet("color: #7c2d12; background: #ffedd5; padding: 6px 10px; border-radius: 4px;")
        self.lbl_best_promethee.setWordWrap(True)

        grid_cards.addWidget(self.lbl_best_tech, 0, 0)
        grid_cards.addWidget(self.lbl_best_vpl, 0, 1)
        grid_cards.addWidget(self.lbl_best_env, 1, 0, 1, 2)
        grid_cards.addWidget(self.lbl_best_topsis, 2, 0)
        grid_cards.addWidget(self.lbl_best_vikor, 2, 1)
        grid_cards.addWidget(self.lbl_best_promethee, 3, 0, 1, 2)
        lay_best.addLayout(grid_cards)

        self.lbl_tradeoff_desc = QLabel(tr("Comparação de Trade-off: --"))
        self.lbl_tradeoff_desc.setFont(QFont("Segoe UI", 9))
        self.lbl_tradeoff_desc.setStyleSheet(f"color: {body};")
        self.lbl_tradeoff_desc.setWordWrap(True)
        lay_best.addWidget(self.lbl_tradeoff_desc)

        main_vbox.addWidget(self.gb_best)

        # ── SUB-ABAS DE GRÁFICOS MULTI-CRITÉRIO ──
        self.tab_charts_topsis = QTabWidget()

        tab_score = QWidget()
        lay_score = QVBoxLayout(tab_score)
        lay_score.setContentsMargins(8, 8, 8, 8)
        self.gb_chart = QGroupBox(tr("📊 Gráfico de Decisão Multi-Critério por Volume"))
        self.gb_chart.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        lay_gc = QVBoxLayout(self.gb_chart)
        lay_gc.setContentsMargins(8, 8, 8, 8)

        self.topsis_chart = TOPSISComparisonChart(self)
        # Altura confortável e generosa para visualização nítida dos escores TOPSIS e SMAA-VIKOR
        self.topsis_chart.set_canvas_height_range(minimum=440, maximum=550)
        lay_gc.addWidget(self.topsis_chart)

        lay_score.addWidget(self.gb_chart)
        self.tab_charts_topsis.addTab(tab_score, tr("📊 Gráfico Decisão Multi-Critério"))

        tab_proximity = QWidget()
        lay_proximity_tab = QVBoxLayout(tab_proximity)
        lay_proximity_tab.setContentsMargins(8, 8, 8, 8)
        gb_proximity = QGroupBox(tr("📐 Proximidade de cada Volume aos Oito Critérios"))
        gb_proximity.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        lay_proximity = QVBoxLayout(gb_proximity)
        lay_proximity.setContentsMargins(8, 8, 8, 8)
        proximity_note = QLabel(tr(
            "100% significa o melhor valor observado naquele critério; 0%, o pior. "
            "As proximidades são normalizadas por critério e não substituem o escore ponderado."
        ))
        proximity_note.setWordWrap(True)
        proximity_note.setStyleSheet(f"font-size: 10px; color: {body};")
        lay_proximity.addWidget(proximity_note)
        self.topsis_proximity_chart = TOPSISProximityChart(self)
        self.topsis_proximity_chart.set_canvas_height_range(minimum=440, maximum=550)
        lay_proximity.addWidget(self.topsis_proximity_chart)
        lay_proximity_tab.addWidget(gb_proximity)
        self.tab_charts_topsis.addTab(tab_proximity, tr("🎯 Proximidade aos Ótimos"))

        main_vbox.addWidget(self.tab_charts_topsis)

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

        self._update_method_controls()

    def generate_neighborhood_scenarios(self):
        self.recalculate_all()

    def showEvent(self, event):
        """Ao abrir a aba, calcula o TOPSIS sincronizado com as etapas anteriores."""
        super().showEvent(event)
        self.recalculate_all()

    def on_method_changed(self, _index: int):
        """Alterna entre decisão por pesos fixos (TOPSIS) e robustez SMAA-VIKOR."""
        self._update_method_controls()
        self.recalculate_all()

    def on_smaa_profile_changed(self, _index: int):
        """Recalcula a aceitabilidade com o perfil de simulações selecionado."""
        is_custom = self.combo_smaa_profile.currentData() == "custom"
        if hasattr(self, "spin_smaa_custom_samples"):
            self.spin_smaa_custom_samples.setVisible(is_custom)
        self._update_weight_validation()
        if self.combo_mcdm_method.currentData() == "smaa_vikor":
            self.recalculate_all()

    def on_smaa_custom_samples_changed(self, _value: int):
        """Dispara recálculo quando a quantidade personalizada de simulações é ajustada."""
        self._update_weight_validation()
        if self.combo_mcdm_method.currentData() == "smaa_vikor":
            self.recalculate_all()

    def on_v_param_changed(self, _value: float):
        """Dispara recálculo quando o peso de consenso v do VIKOR é ajustado."""
        self._update_weight_validation()
        if self.combo_mcdm_method.currentData() == "smaa_vikor":
            self.recalculate_all()

    def get_smaa_num_simulations(self) -> int:
        """Retorna o número de simulações Monte Carlo configurado para o SMAA-VIKOR."""
        if hasattr(self, "combo_smaa_profile"):
            if self.combo_smaa_profile.currentData() == "custom" and hasattr(self, "spin_smaa_custom_samples"):
                return max(10, int(self.spin_smaa_custom_samples.value()))
            return max(10, int(self.combo_smaa_profile.currentData() or 20000))
        return 20000

    def get_vikor_v_param(self) -> float:
        """Retorna o peso da estratégia de consenso v do VIKOR (padrão 0.50)."""
        if hasattr(self, "spin_v_param"):
            return float(self.spin_v_param.value())
        return 0.50

    def _update_method_controls(self):
        method = self.combo_mcdm_method.currentData() if hasattr(self, "combo_mcdm_method") else "topsis"
        is_smaa_vikor = method == "smaa_vikor"
        is_vikor = method == "vikor"
        is_promethee = method == "promethee"

        self.lbl_profile.setText(tr("Perfil de simulações:") if is_smaa_vikor else tr("Perfil de decisão:"))
        self.combo_preset.setVisible(not is_smaa_vikor)
        self.combo_smaa_profile.setVisible(is_smaa_vikor)
        
        is_custom_smaa = is_smaa_vikor and (self.combo_smaa_profile.currentData() == "custom")
        if hasattr(self, "spin_smaa_custom_samples"):
            self.spin_smaa_custom_samples.setVisible(is_custom_smaa)

        # Oculta/Exibe controles de pesos manuais vs parâmetros estocásticos
        for lbl in (self.lbl_w_tech, self.lbl_w_fin, self.lbl_w_env, self.lbl_w_struct):
            if hasattr(self, lbl.objectName() or "lbl"):
                lbl.setVisible(not is_smaa_vikor)
        for spin in (self.spin_w_tech, self.spin_w_fin, self.spin_w_env, self.spin_w_struct):
            spin.setVisible(not is_smaa_vikor)
            spin.setEnabled(not is_smaa_vikor)
        for widget in getattr(self, "_shares_widgets", []):
            widget.setVisible(not (is_smaa_vikor or is_vikor or is_promethee))

        show_v = is_smaa_vikor or is_vikor
        if hasattr(self, "lbl_v_param"):
            self.lbl_v_param.setVisible(show_v)
        if hasattr(self, "spin_v_param"):
            self.spin_v_param.setVisible(show_v)

        if hasattr(self, "table"):
            if is_smaa_vikor:
                label_score = tr("Aceit. 1º (%)") + "\n" + tr("SMAA-VIKOR")
                label_rank = tr("Rank") + "\n" + tr("SMAA-VIKOR")
            elif is_vikor:
                label_score = tr("Índice Q") + "\n" + tr("VIKOR")
                label_rank = tr("Rank") + "\n" + tr("VIKOR")
            elif is_promethee:
                label_score = tr("Fluxo Líq. (Φ)") + "\n" + tr("PROMETHEE II")
                label_rank = tr("Rank") + "\n" + tr("PROMETHEE II")
            else:
                label_score = tr("TOPSIS") + "\n" + tr("Score")
                label_rank = tr("Rank") + "\n" + tr("TOPSIS")
            self.table.setHorizontalHeaderItem(13, QTableWidgetItem(label_score))
            self.table.setHorizontalHeaderItem(14, QTableWidgetItem(label_rank))
        if hasattr(self, "gb_best"):
            self.gb_best.setTitle(tr("🏆 Conclusão da Decisão Multi-Critério"))
        if hasattr(self, "gb_chart"):
            method_name = "SMAA-VIKOR" if is_smaa_vikor else ("VIKOR" if is_vikor else ("PROMETHEE II" if is_promethee else "TOPSIS"))
            self.gb_chart.setTitle(tr("📊 Gráfico de Decisão Multi-Critério por Volume") + f" ({method_name})")
        if hasattr(self, "tab_charts_topsis"):
            method_name = "SMAA-VIKOR" if is_smaa_vikor else ("VIKOR" if is_vikor else ("PROMETHEE II" if is_promethee else "TOPSIS"))
            self.tab_charts_topsis.setTabText(0, tr("📊 Gráfico Decisão Multi-Critério") + f" ({method_name})")
        self._update_weight_validation()

    def on_preset_changed(self, index: int):
        if self._updating_weights:
            return
        self._updating_weights = True
        key = self.combo_preset.currentData()
        perfis = {
            "equilibrado": (25.0, 25.0, 25.0, 25.0),
            "economico": (10.0, 70.0, 10.0, 10.0),
            "ambiental": (10.0, 10.0, 70.0, 10.0),
            "tecnico": (70.0, 10.0, 10.0, 10.0),
            "estrutural": (10.0, 10.0, 10.0, 70.0),
        }
        if key in perfis:
            for spin, valor in zip((self.spin_w_tech, self.spin_w_fin, self.spin_w_env, self.spin_w_struct), perfis[key]):
                spin.setValue(valor)
        self._updating_weights = False
        self._update_weight_validation()
        self.recalculate_all()

    def get_current_shares(self):
        """Partes no eixo escolhidas na interface; inválidas (eixo sem nenhum critério), volta ao padrão."""
        valores = tuple(spin.value() for spin in self.spin_shares)
        try:
            validar_partes_no_eixo(valores)
            return valores
        except ValueError:
            return PARTES_NO_EIXO_PADRAO

    def set_shares(self, valores):
        self._updating_weights = True
        for spin, valor in zip(self.spin_shares, valores):
            spin.setValue(float(valor))
        self._updating_weights = False
        self._update_weight_validation()

    def reset_shares(self, partes):
        self.set_shares([100.0 * float(p) for p in partes])
        self.recalculate_all()

    def on_shares_changed(self):
        if self._updating_weights:
            return
        self._update_weight_validation()
        self.recalculate_all()

    def on_spin_weight_changed(self):
        if self._updating_weights:
            return
        self._updating_weights = True
        self.combo_preset.setCurrentIndex(self.combo_preset.findData("custom"))
        self._updating_weights = False
        self._update_weight_validation()
        self.recalculate_all()

    def _update_weight_validation(self):
        if not hasattr(self, "lbl_weight_validation"):
            return
        if (
            hasattr(self, "combo_mcdm_method")
            and self.combo_mcdm_method.currentData() == "smaa_vikor"
        ):
            samples = self.get_smaa_num_simulations()
            v_val = self.get_vikor_v_param()
            self.lbl_weight_validation.setText(
                milhar(tr('✓ {0:,} simulações Monte Carlo no simplex uniforme (sem perfil único de pesos) · VIKOR v={1:.2f}').format(samples, v_val))
            )
            self.lbl_weight_validation.setStyleSheet(
                "font-size: 10px; font-weight: bold; color: #047857;"
            )
            return
        total = self.spin_w_tech.value() + self.spin_w_fin.value() + self.spin_w_env.value() + self.spin_w_struct.value()
        valid = total > 0
        if hasattr(self, "spin_shares"):
            try:
                validar_partes_no_eixo(tuple(spin.value() for spin in self.spin_shares))
            except ValueError:
                valid = False
        if not valid:
            message = f"⚠ {tr('Pesos inválidos')}: {format_ptbr(0, 1)}%"
        elif abs(total - 100.0) < 0.05:
            message = f"✓ {tr('Soma dos pesos')}: {total:.1f}%"
        else:
            message = f"ℹ {tr('Soma dos pesos')}: {total:.1f}% — {tr('normalizada automaticamente')}"
        self.lbl_weight_validation.setText(decimal(message))
        self.lbl_weight_validation.setStyleSheet(
            f"font-size: 10px; font-weight: bold; color: {'#047857' if valid else '#b91c1c'};"
        )

    def get_current_weights(self):
        pesos = (self.spin_w_tech.value(), self.spin_w_fin.value(),
                 self.spin_w_env.value(), self.spin_w_struct.value())
        total = sum(pesos)
        if total <= 0:
            return PESOS_PADRAO
        return tuple(w / total for w in pesos)

    def recalculate_all(self):
        if hasattr(self, 'btn_recalc'):
            self.btn_recalc.setEnabled(False)
            self.btn_recalc.setText(tr("Calculando..."))
        QApplication.processEvents()

        try:
            self._do_recalculate_all()
        finally:
            if hasattr(self, 'btn_recalc'):
                self.btn_recalc.setEnabled(True)
                self.btn_recalc.setText(tr("⚡ Recalcular"))

    def clear_results(self):
        self.last_topsis_result = None
        self.last_mcdm_result = None
        self.last_smaa_vikor_result = None
        self.last_scenario_results = []
        self.scenarios = []
        if hasattr(self, "table"):
            self.table.setRowCount(0)
        if hasattr(self, "lbl_best_tech"):
            self.lbl_best_tech.setText(tr("💧 Ótimo Técnico (pós-limiar): --"))
        if hasattr(self, "lbl_best_vpl"):
            self.lbl_best_vpl.setText(tr("💵 Ótimo Econômico (Menor Payback): --"))
        if hasattr(self, "lbl_best_env"):
            self.lbl_best_env.setText(tr("🍃 Ótimo Ambiental (Maior CO2 Evitado): --"))
        if hasattr(self, "lbl_best_topsis"):
            self.lbl_best_topsis.setText(tr("🏆 Ótimo TOPSIS: --"))
        if hasattr(self, "lbl_best_vikor"):
            self.lbl_best_vikor.setText(tr("🎲 Ótimo VIKOR / SMAA: --"))
        if hasattr(self, "lbl_best_promethee"):
            self.lbl_best_promethee.setText(tr("⚖️ Ótimo PROMETHEE II: --"))
        if hasattr(self, "lbl_tradeoff_desc"):
            self.lbl_tradeoff_desc.setText(tr("Comparação de Trade-off: --"))
        if hasattr(self, "topsis_chart"):
            self.topsis_chart.plot_empty(tr("Execute a varredura completa na Etapa 3 para gerar a decisão multi-critério"))
        if hasattr(self, "topsis_proximity_chart"):
            self.topsis_proximity_chart.plot_empty(tr("Execute a varredura completa na Etapa 3 para gerar as proximidades"))

    def _do_recalculate_all(self):
        self._updating_table = True
        main_win = self.window()
        if main_win and hasattr(main_win, 'tab_tanks_simulation'):
            if getattr(main_win.tab_tanks_simulation, '_is_technical_only', False):
                self.clear_results()
                self._updating_table = False
                return

        cfg = None

        if main_win and hasattr(main_win, 'tab_economic'):
            cfg = main_win.tab_economic.get_triton_config()
        elif main_win and hasattr(main_win, 'config'):
            cfg = main_win.config
        else:
            cfg = TritonConfig()

        # Resgata resultados da Varredura Técnica (Etapa 4)
        sweep_results = []
        opt_tech_vol = None
        if main_win and hasattr(main_win, 'tab_tanks_simulation'):
            sweep = main_win.tab_tanks_simulation.last_sweep_result
            sweep_results = list(getattr(sweep, 'results_by_volume', []) or [])
            if sweep and getattr(sweep, 'optimal_lower_tank_vol', None):
                opt_tech_vol = float(sweep.optimal_lower_tank_vol)

        if not sweep_results:
            if main_win and hasattr(main_win, 'tab_tanks_simulation') and main_win.tab_tanks_simulation.last_single_result:
                sweep_results = [main_win.tab_tanks_simulation.last_single_result]

        if not sweep_results:
            self.clear_results()
            self._updating_table = False
            return

        # Resgata os exatos resultados econômicos da Etapa 5 (para garantir 100% de paridade)
        econ_dict = {}
        if main_win and hasattr(main_win, 'tab_economic'):
            econ_dict = getattr(main_win.tab_economic, 'last_sweep_econ_results', {}) or {}

        # Resgata ou calcula ACV da Etapa 6
        env_cfg = None
        if main_win and hasattr(main_win, 'tab_environmental'):
            env_cfg = main_win.tab_environmental.get_config()
        else:
            env_cfg = EnvironmentalConfig()

        v_map = []
        for r in sweep_results:
            # A energia de recalque sai da funcao unica do nucleo. Aqui havia uma
            # copia da formula antiga, que dividia pelo rendimento uma segunda vez:
            # o criterio ambiental do multicriterio ranqueava volumes com uma
            # energia 1,68 vezes maior que a da aba ambiental, no mesmo projeto.
            annual_pump_kwh = _energia_anual_de_bombeamento(cfg, r)
            v_map.append((r.lower_tank_vol, r.annual_pluvial_consumed_m3, annual_pump_kwh))
        env_sweep = run_environmental_sweep(v_map, env_cfg)
        env_dict = {d["volume_l"]: d for d in env_sweep.sweep_details}

        technical_threshold = getattr(cfg, 'delta_ideal', 5.0)
        if main_win and hasattr(main_win, 'tab_tanks_simulation'):
            technical_threshold = parse_float(
                main_win.tab_tanks_simulation.txt_delta_ideal.text(), technical_threshold
            )

        lang_is_en = get_current_lang() == "en"
        # O símbolo é o da moeda escolhida, não o do idioma: em inglês, valores em
        # reais apareciam como dólares.
        curr_sym = (main_win.tab_tanks_simulation.get_currency_symbol()
                    if main_win and hasattr(main_win, "tab_tanks_simulation") else "R$")
        unit_m3_yr = "m³/year" if lang_is_en else "m³/ano"
        unit_yrs = "years" if lang_is_en else "anos"
        no_payback_str = "No payback" if lang_is_en else "Sem Retorno"

        self.table.setRowCount(len(sweep_results))
        topsis_candidates = []
        results_summary = []
        best_vpl = -1e9
        best_vpl_row = -1
        best_pb_row = -1
        min_pb = float("inf")
        best_vpl_for_pb = -float("inf")

        tma_annual = mensal_pct_para_anual_fracao(cfg.tma)
        inf_annual = mensal_pct_para_anual_fracao(cfg.inflation)
        n_readj_per_year = 12.0 / max(1.0, cfg.tariff_escalation)
        w_esc_annual = (1.0 + getattr(cfg, 'water_tariff_escalation', 5.0) / 100.0) ** n_readj_per_year - 1.0
        s_esc_annual = (1.0 + getattr(cfg, 'sewage_tariff_escalation', 5.0) / 100.0) ** n_readj_per_year - 1.0
        e_esc_annual = (1.0 + getattr(cfg, 'elec_tariff_escalation', 5.0) / 100.0) ** n_readj_per_year - 1.0
        period_yrs = cfg.analysis_period_years
        upper_used = bool(getattr(cfg, 'upper_tank_used', 1))

        for row, r_item in enumerate(sweep_results):
            v_vol = r_item.lower_tank_vol
            vol_key = round(v_vol, 1)

            # 1. Indicadores Técnicos
            pot_pct = r_item.potential_potable_savings_pct
            annual_m3_val = r_item.annual_pluvial_consumed_m3
            sim_days = getattr(r_item, 'total_days', 365)
            num_full_days = int(round((r_item.pct_days_full_satisfaction / 100.0) * sim_days))

            # 2. Indicadores Econômicos
            if vol_key in econ_dict:
                sc_econ = econ_dict[vol_key]
                capex_tot = sc_econ["capex"]
                gross_savings_month = sc_econ["gross_monthly"]
                vpl = sc_econ["vpl"]
                tir = sc_econ["tir"]
                pb_num = sc_econ["payback"]
                pb_discounted = sc_econ.get("payback_discounted")
                lcow_v = sc_econ.get("lcow_per_m3")
            else:
                low_mat = getattr(cfg, "lower_tank_material", "PEAD")
                up_mat = getattr(cfg, "upper_tank_material", "PEAD")
                from triton.core.cost_estimates import preco_da_cisterna_do_volume
                c_low = preco_da_cisterna_do_volume(cfg, v_vol)
                etap_c_inc = 0.0
                if getattr(cfg, 'etap_enabled', True):
                    from triton.core.etap_integration import capex_incremental_da_etap
                    etap_c_inc = capex_incremental_da_etap(cfg, annual_m3_val)
                capex_tot = 0.0 if v_vol <= 0 else (
                    c_low + cfg.upper_tank_unit_cost +
                    (cfg.pump_unit_cost * getattr(cfg, "pump_count", 1) if upper_used else 0.0) +
                    cfg.filters_pipes_cost + cfg.labor_installation_cost + etap_c_inc
                )
                tw_v, ts_v = calculate_effective_tariff(
                    cfg, annual_m3_val if v_vol > 0 else 0.0,
                    annual_total_demand_m3=(r_item.annual_pluvial_consumed_m3 + r_item.annual_potable_consumed_m3) if v_vol > 0 else 0.0,
                )
                p_hrs_v = 0.0
                if upper_used and cfg.pump_flow_rate > 0 and v_vol > 0:
                    if hasattr(r_item, 'total_pumped_liters') and r_item.total_pumped_liters > 0:
                        t_rec_v = (r_item.total_pumped_liters / max(1.0, sim_days / 365.25)) / cfg.pump_flow_rate
                        ann_cyc_v = r_item.total_pump_cycles / max(1.0, sim_days / 365.25)
                        t_part_v = ann_cyc_v * cfg.pump_startup_time_h
                        # Horas de operacao, sem dividir pelo rendimento.
                        p_hrs_v = t_rec_v + t_part_v
                    else:
                        ann_pumped_l = (annual_m3_val if v_vol > 0 else 0.0) * 1000.0
                        t_rec_v = ann_pumped_l / cfg.pump_flow_rate
                        p_hrs_v = t_rec_v

                cl2_enabled = getattr(cfg, "chlorine_treatment_enabled", True)
                cl2_dose = getattr(cfg, "chlorine_dose_mg_l", 2.0)
                cl2_cost_kg = getattr(cfg, "chlorine_cost_per_kg", 25.0)
                if upper_used and v_vol > 0:
                    _, ann_cl_cost_v = estimate_annual_chlorination_cost(
                        annual_m3_val, cl2_dose if cl2_enabled else 0.0, cl2_cost_kg
                    )
                else:
                    ann_cl_cost_v = 0.0

                annual_om_v = annualize_operational_costs(cfg.op_costs, annual_m3_val) if v_vol > 0 else 0.0

                iptu_enabled = getattr(cfg, "iptu_green_enabled", False)
                ann_iptu_savings = 0.0
                if iptu_enabled and v_vol > 0:
                    ann_iptu_savings = float(getattr(cfg, "iptu_annual_value", 0.0)) * (float(getattr(cfg, "iptu_discount_pct", 0.0)) / 100.0)

                econ_v = run_robust_economic_analysis(
                    initial_investment=capex_tot,
                    annual_water_saved_m3=annual_m3_val if v_vol > 0 else 0.0,
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
                    elec_tariff_kwh=cfg.elec_tariff,
                    analysis_period_years=period_yrs,
                    annual_chlorine_cost=ann_cl_cost_v,
                    annual_iptu_savings=ann_iptu_savings,
                )
                gross_savings_month = (econ_v.annual_cash_flows[1].total_gross_savings_brl / 12.0) if len(econ_v.annual_cash_flows) > 1 else 0.0
                vpl = econ_v.vpl
                tir = econ_v.tir_pct
                pb_discounted = econ_v.payback_discounted_years
                pb_num = pb_discounted if pb_discounted is not None else econ_v.payback_simple_years
                lcow_v = econ_v.lcow_per_m3 if v_vol > 0 else None

            # 3. Indicadores Ambientais
            env_data = env_dict.get(v_vol, {})
            co2_saved_lifetime = env_data.get("lifetime_net_co2_saved_kg", 0.0)
            lifecycle_co2 = -co2_saved_lifetime
            env_pb = env_data.get("environmental_payback_years", 999.0)

            # Preenchimento da Tabela
            opt_label = f"{tr('Opção')} {row+1} ({v_vol:.0f} L)"
            item_name = QTableWidgetItem(opt_label)
            item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_name)

            def _mk_item(txt):
                it = QTableWidgetItem(txt)
                it.setTextAlignment(Qt.AlignCenter)
                return it

            self.table.setItem(row, 1, _mk_item(f"{v_vol:.0f}"))
            self.table.setItem(row, 2, _mk_item(f"{cfg.upper_tank_vol if upper_used else 0:.0f}"))
            self.table.setItem(row, 3, _mk_item(f"{format_ptbr(pot_pct, 1)}%"))
            self.table.setItem(row, 4, _mk_item(f"{format_ptbr(r_item.annual_spill_m3, 1)}"))
            self.table.setItem(row, 5, _mk_item(f"{format_ptbr(annual_m3_val, 1)}"))
            self.table.setItem(row, 6, _mk_item(f"{format_ptbr(r_item.annual_potable_consumed_m3, 1)}"))
            self.table.setItem(row, 7, _mk_item(f"{num_full_days}"))
            self.table.setItem(row, 8, _mk_item(f"{curr_sym} {format_ptbr(vpl, 2)}"))
            self.table.setItem(row, 9, _mk_item(f"{format_ptbr(pb_discounted, 1)}" if pb_discounted is not None else no_payback_str))
            self.table.setItem(row, 10, _mk_item(f"{format_ptbr(tir, 1)}%"))
            self.table.setItem(row, 11, _mk_item(f"{format_ptbr(lifecycle_co2, 0)} kg"))
            self.table.setItem(row, 12, _mk_item(f"{format_ptbr(env_pb, 1)}" if env_pb < 90 else "> 50"))

            is_tech_opt = (opt_tech_vol is not None and abs(v_vol - opt_tech_vol) < 1.0)
            cand = TopsisCandidate(
                lower_tank_vol=v_vol,
                water_saved_m3_yr=annual_m3_val,
                vpl_brl=vpl,
                co2_saved_kg_lifetime=co2_saved_lifetime,
                capex_brl=capex_tot,
                upper_tank_vol=cfg.upper_tank_vol if upper_used else 0.0,
                technical_threshold_met=(v_vol > 0 and r_item.delta_potential_per_m3 <= technical_threshold),
                is_technical_optimum=is_tech_opt,
                potential_savings_pct=pot_pct,
                overflow_m3_yr=r_item.annual_spill_m3,
                discounted_payback_years=payback_do_criterio(pb_discounted, vpl) if v_vol > 0 else None,
                irr_pct=tir,
                potable_consumed_m3_yr=r_item.annual_potable_consumed_m3,
                volumetric_reliability_pct=r_item.volumetric_reliability_pct,
                storage_efficiency_pct=r_item.storage_efficiency_pct,
                net_financial_savings_brl=vpl,
                lcow_brl_m3=lcow_v,
                # O material da cisterna vem da etapa ambiental, como na linha de comando: é o que
                # faz a massa variar com o volume (tubos, bomba e caixa superior são constantes).
                material_mass_kg=(calculate_system_weight_from_config(
                    cfg, lower_tank_vol_l=v_vol, environmental_raw={
                        "lower_material_key": getattr(env_cfg, "lower_material_key", None),
                        "upper_material_key": getattr(env_cfg, "upper_material_key", None),
                        "custom_lower_density_kg_m3": getattr(env_cfg, "custom_lower_density_kg_m3", None),
                        "custom_upper_density_kg_m3": getattr(env_cfg, "custom_upper_density_kg_m3", None),
                    }).total_dry_mass_kg if v_vol > 0 else 0.0),
            )
            topsis_candidates.append(cand)

            results_summary.append({
                "name": opt_label,
                "vol": v_vol,
                "capex": capex_tot,
                "gross_m": gross_savings_month,
                "vpl": vpl,
                "tir": tir,
                "payback": pb_num,
                "payback_discounted": pb_discounted,
                "co2": co2_saved_lifetime,
                "lifecycle_co2": lifecycle_co2,
                "overflow_m3": r_item.annual_spill_m3,
                "potable_m3": r_item.annual_potable_consumed_m3,
            })

            # Rastreamento de ótimo econômico padrão: menor tempo de retorno (payback) viável entre volumes > 0
            if v_vol > 0:
                pb_cand = pb_discounted if (pb_discounted is not None and pb_discounted > 0) else (pb_num if (pb_num is not None and pb_num > 0) else None)
                if pb_cand is not None and pb_cand > 0:
                    if pb_cand < min_pb - 1e-4:
                        min_pb = pb_cand
                        best_vpl_for_pb = vpl
                        best_pb_row = row
                    elif abs(pb_cand - min_pb) <= 1e-4 and vpl > best_vpl_for_pb:
                        best_vpl_for_pb = vpl
                        best_pb_row = row

                if vpl > best_vpl:
                    best_vpl = vpl
                    best_vpl_row = row

        best_econ_row = best_pb_row if best_pb_row >= 0 else best_vpl_row

        # Calcula SEMPRE todos os métodos para apresentar ambos na conclusão executiva
        self.last_scenario_results = results_summary
        weights = self.get_current_weights()
        selected_method = self.combo_mcdm_method.currentData() if hasattr(self, 'combo_mcdm_method') else "topsis"

        topsis_res = calculate_topsis_scores(topsis_candidates, weights=weights, parts=self.get_current_shares())
        self.last_topsis_result = topsis_res

        smaa_samples = self.get_smaa_num_simulations()
        v_param_val = self.get_vikor_v_param()
        smaa_res = run_smaa_vikor(topsis_candidates, v_param=v_param_val, num_samples=smaa_samples)
        self.last_smaa_vikor_result = smaa_res

        vikor_res = run_vikor(topsis_candidates, weights=weights, v_param=v_param_val)
        self.last_vikor_result = vikor_res

        promethee_res = run_promethee(topsis_candidates, weights=weights)
        self.last_promethee_result = promethee_res

        if selected_method == "smaa_vikor":
            self.last_mcdm_result = smaa_res
            best_mcdm_row = smaa_res.best_index
            mcdm_label_title = milhar(f"🎲 Ótimo SMAA-VIKOR ({smaa_samples:,} simulações)")
            for r, (acc, rk) in enumerate(zip(smaa_res.first_rank_acceptabilities, smaa_res.ranks)):
                item_score = QTableWidgetItem(f"{acc*100:.1f}%")
                item_score.setTextAlignment(Qt.AlignCenter)
                item_rk = QTableWidgetItem(f"#{rk}")
                item_rk.setTextAlignment(Qt.AlignCenter)
                if r == smaa_res.best_index:
                    font = item_score.font(); font.setBold(True); item_score.setFont(font); item_rk.setFont(font)
                self.table.setItem(r, 13, item_score)
                self.table.setItem(r, 14, item_rk)
        elif selected_method == "vikor":
            self.last_mcdm_result = vikor_res
            best_mcdm_row = vikor_res.best_index
            mcdm_label_title = tr("🤝 Ótimo VIKOR (Compromisso v={0:.2f})").format(v_param_val)
            for r, (q, rk) in enumerate(zip(vikor_res.q_scores, vikor_res.ranks)):
                item_score = QTableWidgetItem(f"{q:.3f}")
                item_score.setTextAlignment(Qt.AlignCenter)
                item_rk = QTableWidgetItem(f"#{rk}")
                item_rk.setTextAlignment(Qt.AlignCenter)
                if r == vikor_res.best_index:
                    font = item_score.font(); font.setBold(True); item_score.setFont(font); item_rk.setFont(font)
                self.table.setItem(r, 13, item_score)
                self.table.setItem(r, 14, item_rk)
        elif selected_method == "promethee":
            self.last_mcdm_result = promethee_res
            best_mcdm_row = promethee_res.best_index
            mcdm_label_title = tr("⚖️ Ótimo PROMETHEE II (Superação)")
            for r, (phi, rk) in enumerate(zip(promethee_res.net_flows, promethee_res.ranks)):
                item_score = QTableWidgetItem(f"{phi:+.3f}")
                item_score.setTextAlignment(Qt.AlignCenter)
                item_rk = QTableWidgetItem(f"#{rk}")
                item_rk.setTextAlignment(Qt.AlignCenter)
                if r == promethee_res.best_index:
                    font = item_score.font(); font.setBold(True); item_score.setFont(font); item_rk.setFont(font)
                self.table.setItem(r, 13, item_score)
                self.table.setItem(r, 14, item_rk)
        else:
            self.last_mcdm_result = topsis_res
            best_mcdm_row = topsis_res.best_index if topsis_res else best_econ_row
            mcdm_label_title = "🏆 Ótimo TOPSIS"
            if topsis_res:
                rankings = np.argsort(np.argsort(-np.array(topsis_res.scores))) + 1
                for r, (score, rk) in enumerate(zip(topsis_res.scores, rankings)):
                    item_score = QTableWidgetItem(f"{score:.2f}")
                    item_score.setTextAlignment(Qt.AlignCenter)
                    item_rk = QTableWidgetItem(f"#{rk}")
                    item_rk.setTextAlignment(Qt.AlignCenter)
                    if r == topsis_res.best_index:
                        font = item_score.font(); font.setBold(True); item_score.setFont(font); item_rk.setFont(font)
                    self.table.setItem(r, 13, item_score)
                    self.table.setItem(r, 14, item_rk)

        # Atualiza todos os cards de decisão multicritério (TOPSIS, VIKOR e PROMETHEE)
        is_equal_weights = all(abs(w - 0.25) < 0.015 for w in weights)
        if is_equal_weights:
            weights_desc = tr("pesos iguais: 25% em cada eixo (técnico, econômico, ambiental e estrutural)")
            weights_short = tr("pesos iguais")
        else:
            weights_desc = tr("pesos ponderados: {0}% Técnico, {1}% Econômico, {2}% Ambiental, {3}% Estrutural").format(
                *(f"{w*100:.1f}" for w in weights))
            weights_short = "/".join(f"{w*100:.0f}" for w in weights) + "%"

        if topsis_res:
            best_top = topsis_res.best_candidate
            self.lbl_best_topsis.setText(
                f"🏆 {tr('Ótimo TOPSIS')} ({weights_short}): {best_top.lower_tank_vol:.0f} L (Score: {topsis_res.scores[topsis_res.best_index]:.2f})"
            )
        if selected_method == "vikor" and vikor_res:
            best_vik = vikor_res.best_candidate
            self.lbl_best_vikor.setText(
                f"🤝 {tr('Ótimo VIKOR')} ({weights_short}, v={v_param_val:.2f}): {best_vik.lower_tank_vol:.0f} L (Q: {vikor_res.q_scores[vikor_res.best_index]:.3f})"
            )
        elif smaa_res:
            best_sma = smaa_res.best_candidate
            self.lbl_best_vikor.setText(
                milhar(tr('🎲 {0}: {1:.0f} L ({2:.1f}% em {3:,} simulações)').format(tr('Ótimo VIKOR / SMAA'), best_sma.lower_tank_vol, smaa_res.first_rank_acceptabilities[smaa_res.best_index]*100, smaa_samples))
            )
        if promethee_res:
            best_prom = promethee_res.best_candidate
            self.lbl_best_promethee.setText(
                f"⚖️ {tr('Ótimo PROMETHEE II')} ({weights_short}): {best_prom.lower_tank_vol:.0f} L (Φ: {promethee_res.net_flows[promethee_res.best_index]:+.3f})"
            )

        if topsis_res:
            self.topsis_chart.update_chart(
                topsis_result=topsis_res,
                smaa_result=self.last_smaa_vikor_result,
                vikor_result=self.last_vikor_result,
                promethee_result=self.last_promethee_result,
                method=selected_method
            )
            self.topsis_proximity_chart.update_chart(
                topsis_res,
                selected_best_index=best_mcdm_row,
                method_label=("SMAA-VIKOR" if selected_method == "smaa_vikor" else ("VIKOR" if selected_method == "vikor" else ("PROMETHEE II" if selected_method == "promethee" else "TOPSIS")))
            )

            best_t = topsis_candidates[topsis_res.technical_best_index]
            best_f = topsis_candidates[topsis_res.financial_best_index]
            best_e = topsis_candidates[topsis_res.environmental_best_index]

            self.lbl_best_tech.setText(tr('💧 {0}: {1:.0f} L ({2:.1f} m³/ano)').format(tr('Ótimo Técnico'), best_t.lower_tank_vol, best_t.water_saved_m3_yr))
            pb_f = best_f.discounted_payback_years
            pb_f_str = f" | Payback: {format_ptbr(pb_f, 1)}a" if (pb_f is not None and pb_f > 0) else ""
            self.lbl_best_vpl.setText(f"💵 {tr('Ótimo Econômico (Menor Payback)')}: {best_f.lower_tank_vol:.0f} L ({curr_sym} {format_ptbr(best_f.vpl_brl, 2)}{pb_f_str})")
            self.lbl_best_env.setText(tr('🍃 {0}: {1:.0f} L ({2:.0f} kg CO2e líquidos)').format(tr('Ótimo Ambiental'), best_e.lower_tank_vol, best_e.lifecycle_co2_kg))

        target_econ_row = topsis_res.financial_best_index if topsis_res else best_econ_row
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    if row == best_mcdm_row:
                        item.setBackground(QColor("#dcfce7"))
                    elif row == target_econ_row:
                        item.setBackground(QColor("#fef9c3"))
                    else:
                        item.setBackground(QColor("#ffffff"))

        if best_mcdm_row >= 0 and best_mcdm_row < len(results_summary):
            best = results_summary[best_mcdm_row]
            if len(results_summary) > 1:
                sorted_by_vol = sorted(results_summary, key=lambda x: x["vol"])
                smallest = sorted_by_vol[0]
                extra_vpl = best["vpl"] - smallest["vpl"]
                top_vol = topsis_res.best_candidate.lower_tank_vol if topsis_res else best["vol"]
                top_score = topsis_res.scores[topsis_res.best_index] if topsis_res else 0.0
                vik_vol = smaa_res.best_candidate.lower_tank_vol if smaa_res else best["vol"]
                vik_acc = (smaa_res.first_rank_acceptabilities[smaa_res.best_index] * 100.0) if smaa_res else 0.0

                # Frase montada com o catálogo (en/es/zh) e só números já formatados: o ``.replace(",", ".")``
                # global que existia trocava também as vírgulas do texto e as decimais do VPL («2.428.94»).
                _milhar = lambda n: milhar(f"{n:,}")
                tradeoff_msg = tr(
                    "O método TOPSIS ({0}) recomenda a cisterna de {1} L (Score: {2}), enquanto o método VIKOR "
                    "(SMAA-VIKOR estocástico, {3} simulações) recomenda a cisterna de {4} L (aceitabilidade de 1º lugar: {5}%). "
                    "A alternativa selecionada na tabela ({6} L) proporciona {7} {8} a mais de VPL e {9} kg de CO2e evitado "
                    "em relação à menor cisterna ({10} L)."
                ).format(
                    weights_desc, f"{top_vol:.0f}", f"{top_score:.2f}", _milhar(smaa_samples), f"{vik_vol:.0f}", f"{vik_acc:.1f}",
                    f"{best['vol']:.0f}", curr_sym, format_ptbr(extra_vpl, 2), f"{best['co2']:.0f}", f"{smallest['vol']:.0f}")
                # Em português a frase não passa pelo catálogo da Portugal: na IBE, VPL vira VAL.
                from triton.ui.translation import em_portugues_da_edicao
                self.lbl_tradeoff_desc.setText(em_portugues_da_edicao(tradeoff_msg))

        self._updating_table = False
        self.optimization_updated.emit()


def _energia_anual_de_bombeamento(cfg, resultado) -> float:
    """kWh/ano de recalque, pela função única do núcleo.

    Existiam quatro cópias da fórmula antiga espalhadas pela interface, todas
    dividindo pelo rendimento uma segunda vez — a potência de placa já o embute.
    Superestimavam em 1/η, 1,68 vezes com rendimento de 55%.
    """
    from triton.core.pump_energy import compute_annual_pump_energy

    if not bool(getattr(cfg, "upper_tank_used", 1)):
        return 0.0
    return compute_annual_pump_energy(cfg, resultado, upper_tank_used=True).annual_kwh
