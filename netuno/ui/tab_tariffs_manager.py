"""
Aba de Gestão, Visualização e Auditoria de Tarifas Nacionais (Netuno 5).
Layout Consolidado com Gráficos Matplotlib Dinâmicos Integrados,
Simulador de Custos em Tempo Real e Discriminação de Disponibilidade.
"""

from __future__ import annotations

import os
from typing import Dict, Any, List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QDoubleSpinBox, QAbstractSpinBox, QFrame, QMessageBox, QSlider, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QUrl, QLocale
from PySide6.QtGui import QFont, QDesktopServices, QColor

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from netuno.ui.translation import tr, get_current_theme
from netuno.core.tariffs_database import (
    get_available_ufs,
    get_cities_by_uf,
    get_city_data,
    get_city_tariffs_by_category,
    CATEGORIAS_TARIFARIAS,
)


class TabTariffsManager(QWidget):
    """Aba consolidada de Gestão de Tarifas, Auditoria e Gráficos Dinâmicos."""
    
    tariffs_changed = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.current_city_data: Optional[Dict[str, Any]] = None
        self.active_tariffs_data: Optional[Dict[str, Any]] = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 28, 40, 40)
        main_layout.setSpacing(8)

        # -------------------------------------------------------------------------------------------------
        # 1. HEADER COMPACTO & AVISO DE CONTATO
        # -------------------------------------------------------------------------------------------------
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 14px;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(12)

        title_lbl = QLabel(tr("Tarifas e auditoria oficial — 652 cidades"))
        title_lbl.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 22px; font-weight: 700; color: #133c32;")
        top_layout.addWidget(title_lbl)

        top_layout.addStretch()

        contact_lbl = QLabel(
            tr("📌 Caso este valor esteja defasado, contatar: ") +
            "<a href='mailto:igorcmvaz@gmail.com?subject=Netuno%205%20-%20Ajuste%20de%20Tarifa' style='color:#0284c7; font-weight:bold; text-decoration:underline;'>igorcmvaz@gmail.com</a>"
        )
        contact_lbl.setStyleSheet("font-size: 11.5px; color: #0369a1; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px; padding: 4px 10px;")
        contact_lbl.setOpenExternalLinks(False)
        contact_lbl.linkActivated.connect(self.on_contact_link_clicked)
        top_layout.addWidget(contact_lbl)

        main_layout.addWidget(top_bar)

        # -------------------------------------------------------------------------------------------------
        # 2. LAYOUT PRINCIPAL EM 2 COLUNAS CONSOLIDADAS
        # -------------------------------------------------------------------------------------------------
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(10)

        # =================================================================================================
        # COLUNA ESQUERDA: PARÂMETROS, TABELA & AÇÕES (48% largura)
        # =================================================================================================
        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # SELETOR UF, CIDADE & CATEGORIA
        sel_card = QFrame()
        sel_card.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px;")
        sel_layout = QGridLayout(sel_card)
        sel_layout.setContentsMargins(0, 0, 0, 0)
        sel_layout.setSpacing(6)

        sel_layout.addWidget(QLabel(f"<b>{tr('UF:')}</b>"), 0, 0)
        self.combo_uf = QComboBox()
        self.combo_uf.setMinimumWidth(80)
        self.combo_uf.setStyleSheet("padding: 4px 6px; font-size: 12px;")
        sel_layout.addWidget(self.combo_uf, 0, 1)

        sel_layout.addWidget(QLabel(f"<b>{tr('Município:')}</b>"), 0, 2)
        self.combo_city = QComboBox()
        self.combo_city.setMinimumWidth(180)
        self.combo_city.setStyleSheet("padding: 4px 6px; font-size: 12px;")
        sel_layout.addWidget(self.combo_city, 0, 3)

        sel_layout.addWidget(QLabel(f"<b>{tr('Categoria:')}</b>"), 1, 0)
        self.combo_category = QComboBox()
        self.combo_category.setStyleSheet("padding: 4px 6px; font-size: 12px; font-weight: bold; color: #0284c7;")
        for cat_id, cat_info in CATEGORIAS_TARIFARIAS.items():
            self.combo_category.addItem(f"{cat_info['icone']} {tr(cat_info['nome'])}", cat_id)
        sel_layout.addWidget(self.combo_category, 1, 1, 1, 3)

        left_layout.addWidget(sel_card)

        # CARTÃO INSTITUCIONAL & EVIDÊNCIA
        inst_card = QFrame()
        inst_card.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px;")
        inst_layout = QVBoxLayout(inst_card)
        inst_layout.setContentsMargins(0, 0, 0, 0)
        inst_layout.setSpacing(4)

        row_inst1 = QHBoxLayout()
        self.lbl_prestador = QLabel("🏢 Prestador: -")
        self.lbl_prestador.setStyleSheet("font-size: 11.5px; color: #1e293b;")
        row_inst1.addWidget(self.lbl_prestador, stretch=1)

        self.lbl_status_badge = QLabel("🟢 Homologado")
        self.lbl_status_badge.setStyleSheet("background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold;")
        row_inst1.addWidget(self.lbl_status_badge)
        inst_layout.addLayout(row_inst1)

        row_inst2 = QHBoxLayout()
        self.lbl_agencia = QLabel("📋 Regulação: -")
        self.lbl_agencia.setStyleSheet("font-size: 11.5px; color: #475569;")
        row_inst2.addWidget(self.lbl_agencia, stretch=1)

        self.btn_open_url = QPushButton(tr("🌐 Fonte Oficial ↗"))
        self.btn_open_url.setStyleSheet("background: transparent; color: #0284c7; border: none; font-size: 11.5px; font-weight: bold; text-decoration: underline;")
        self.btn_open_url.clicked.connect(self.on_open_official_url)
        row_inst2.addWidget(self.btn_open_url)
        inst_layout.addLayout(row_inst2)

        self.lbl_disp_callout = QLabel("🏷️ Custo de Disponibilidade: -")
        self.lbl_disp_callout.setStyleSheet("font-size: 11px; color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 4px; padding: 3px 6px;")
        inst_layout.addWidget(self.lbl_disp_callout)

        left_layout.addWidget(inst_card)

        # PARÂMETROS NUMÉRICOS COMPACTOS
        params_card = QFrame()
        params_card.setStyleSheet("background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px;")
        p_layout = QGridLayout(params_card)
        p_layout.setContentsMargins(0, 0, 0, 0)
        p_layout.setSpacing(6)

        pt_locale = QLocale(QLocale.Portuguese, QLocale.Brazil)
        p_layout.addWidget(QLabel(tr("Tarifa Fixa / Disp. (R$/mês):")), 0, 0)
        self.spin_fixed_water = QDoubleSpinBox()
        self.spin_fixed_water.setLocale(pt_locale)
        self.spin_fixed_water.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_fixed_water.setRange(0.0, 5000.0)
        self.spin_fixed_water.setDecimals(2)
        self.spin_fixed_water.setAlignment(Qt.AlignCenter)
        self.spin_fixed_water.setStyleSheet("""
            QDoubleSpinBox { padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-weight: bold; background: #ffffff; color: #0f172a; }
            QDoubleSpinBox:focus { border: 1.5px solid #0284c7; background: #f0f9ff; }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; height: 0px; border: none; }
        """)
        p_layout.addWidget(self.spin_fixed_water, 0, 1)

        p_layout.addWidget(QLabel(tr("Alíquota de Esgoto (%):")), 0, 2)
        self.spin_sewage_pct = QDoubleSpinBox()
        self.spin_sewage_pct.setLocale(pt_locale)
        self.spin_sewage_pct.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_sewage_pct.setRange(0.0, 200.0)
        self.spin_sewage_pct.setDecimals(1)
        self.spin_sewage_pct.setAlignment(Qt.AlignCenter)
        self.spin_sewage_pct.setStyleSheet("""
            QDoubleSpinBox { padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-weight: bold; background: #ffffff; color: #0f172a; }
            QDoubleSpinBox:focus { border: 1.5px solid #0284c7; background: #f0f9ff; }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; height: 0px; border: none; }
        """)
        p_layout.addWidget(self.spin_sewage_pct, 0, 3)

        p_layout.addWidget(QLabel(tr("Energia Elétrica (R$/kWh):")), 1, 0)
        self.spin_energy_kwh = QDoubleSpinBox()
        self.spin_energy_kwh.setLocale(pt_locale)
        self.spin_energy_kwh.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_energy_kwh.setRange(0.01, 10.0)
        self.spin_energy_kwh.setDecimals(4)
        self.spin_energy_kwh.setAlignment(Qt.AlignCenter)
        self.spin_energy_kwh.setStyleSheet("""
            QDoubleSpinBox { padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-weight: bold; background: #ffffff; color: #0f172a; }
            QDoubleSpinBox:focus { border: 1.5px solid #0284c7; background: #f0f9ff; }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; height: 0px; border: none; }
        """)
        p_layout.addWidget(self.spin_energy_kwh, 1, 1)

        self.lbl_distribuidora = QLabel("Distribuidora: -")
        self.lbl_distribuidora.setStyleSheet("font-size: 11px; color: #64748b;")
        p_layout.addWidget(self.lbl_distribuidora, 1, 2, 1, 2)

        left_layout.addWidget(params_card)

        # TABELA DE FAIXAS PROGRESSIVAS
        left_layout.addWidget(QLabel(tr("<b>Matriz de Faixas Volumétricas:</b>")))
        self.table_tiers = QTableWidget(0, 4)
        self.table_tiers.setHorizontalHeaderLabels([
            tr("Inf (m³)"), tr("Sup (m³)"), tr("R$/m³"), tr("Tipo")
        ])
        self.table_tiers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_tiers.setMinimumHeight(140)
        self.table_tiers.setStyleSheet("""
            QTableWidget { border: 1px solid #cbd5e1; border-radius: 6px; font-size: 11.5px; }
            QHeaderView::section { background: #f8fafc; font-weight: bold; color: #475569; padding: 4px; }
        """)
        self.table_tiers.itemChanged.connect(self.on_table_modified)
        left_layout.addWidget(self.table_tiers)

        # BOTÕES DE AÇÃO NA TABELA
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        
        self.btn_add_tier = QPushButton(tr("➕ Faixa"))
        self.btn_add_tier.setStyleSheet("padding: 4px 8px; font-size: 11.5px;")
        self.btn_add_tier.clicked.connect(self.on_add_tier)
        btn_row.addWidget(self.btn_add_tier)

        self.btn_remove_tier = QPushButton(tr("🗑️ Excluir"))
        self.btn_remove_tier.setStyleSheet("padding: 4px 8px; font-size: 11.5px;")
        self.btn_remove_tier.clicked.connect(self.on_remove_tier)
        btn_row.addWidget(self.btn_remove_tier)

        btn_row.addStretch()

        self.btn_reset_defaults = QPushButton(tr("🔄 Restaurar"))
        self.btn_reset_defaults.setStyleSheet("padding: 4px 10px; font-size: 11.5px;")
        self.btn_reset_defaults.clicked.connect(self.on_reset_to_defaults)
        btn_row.addWidget(self.btn_reset_defaults)

        self.btn_apply_project = QPushButton(tr("💾 Salvar no Projeto"))
        self.btn_apply_project.setStyleSheet("background-color: #0284c7; color: white; border: none; padding: 5px 12px; border-radius: 5px; font-size: 12px; font-weight: bold;")
        self.btn_apply_project.clicked.connect(self.on_apply_to_project)
        btn_row.addWidget(self.btn_apply_project)

        left_layout.addLayout(btn_row)
        columns_layout.addWidget(left_col, stretch=48)

        # =================================================================================================
        # COLUNA DIREITA: GRÁFICOS INTEGRADOS & SIMULADOR EM TEMPO REAL (52% largura)
        # =================================================================================================
        right_col = QWidget()
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        # BOX DO SIMULADOR DE FATURA
        sim_box = QFrame()
        sim_box.setStyleSheet("background: #f8fafc; border: 1px solid #bae6fd; border-radius: 8px; padding: 10px 12px;")
        sim_layout = QVBoxLayout(sim_box)
        sim_layout.setContentsMargins(0, 0, 0, 0)
        sim_layout.setSpacing(6)

        sim_head = QHBoxLayout()
        sim_head.addWidget(QLabel(tr("🧮 <b>Simulador em Tempo Real:</b>")))
        
        self.slider_sim = QSlider(Qt.Horizontal)
        self.slider_sim.setRange(0, 50)
        self.slider_sim.setValue(15)
        self.slider_sim.valueChanged.connect(self.on_slider_changed)
        sim_head.addWidget(self.slider_sim, stretch=1)

        self.spin_sim_vol = QDoubleSpinBox()
        self.spin_sim_vol.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        self.spin_sim_vol.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_sim_vol.setRange(0.0, 500.0)
        self.spin_sim_vol.setValue(15.0)
        self.spin_sim_vol.setDecimals(1)
        self.spin_sim_vol.setMinimumWidth(85)
        self.spin_sim_vol.setMaximumWidth(95)
        self.spin_sim_vol.setAlignment(Qt.AlignCenter)
        self.spin_sim_vol.setStyleSheet("""
            QDoubleSpinBox { padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 6px; font-weight: bold; color: #0284c7; font-size: 13px; background: #ffffff; }
            QDoubleSpinBox:focus { border: 1.5px solid #0284c7; background: #f0f9ff; }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { width: 0px; height: 0px; border: none; }
        """)
        self.spin_sim_vol.valueChanged.connect(self.on_spin_vol_changed)
        sim_head.addWidget(self.spin_sim_vol)
        sim_head.addWidget(QLabel("m³/mês"))
        sim_layout.addLayout(sim_head)

        # Demonstrativo de Fatura
        self.lbl_sim_result = QLabel("🏷️ Fixa: R$ 0,00 | 💧 Água: R$ 0,00 | 🚽 Esgoto: R$ 0,00 | <b>Total: R$ 0,00 / mês</b>")
        self.lbl_sim_result.setStyleSheet("font-size: 12px; color: #0369a1; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 5px 8px;")
        sim_layout.addWidget(self.lbl_sim_result)

        right_layout.addWidget(sim_box)

        # CANVAS MATPLOTLIB EMBARCADO (2 SUBPLOTS: STEP CURVE + BILL CURVE)
        self.figure = Figure(figsize=(5.5, 3.8), dpi=95)
        self.figure.patch.set_facecolor("#ffffff")
        self.ax1 = self.figure.add_subplot(2, 1, 1)
        self.ax2 = self.figure.add_subplot(2, 1, 2)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(240)
        right_layout.addWidget(self.canvas, stretch=1)

        columns_layout.addWidget(right_col, stretch=52)
        main_layout.addLayout(columns_layout)

        # Popula UFs e inicializa
        self.populate_ufs()
        self.combo_uf.currentIndexChanged.connect(self.on_uf_changed)
        self.combo_city.currentIndexChanged.connect(self.on_city_changed)
        self.combo_category.currentIndexChanged.connect(self.on_category_changed)
        self.spin_fixed_water.valueChanged.connect(self.update_bill_simulation)
        self.spin_sewage_pct.valueChanged.connect(self.update_bill_simulation)

    def populate_ufs(self):
        """Popula a lista de 27 UFs."""
        self.combo_uf.blockSignals(True)
        self.combo_uf.clear()
        ufs = get_available_ufs()
        for code, name in ufs:
            self.combo_uf.addItem(f"{code} - {name}", code)
        self.combo_uf.blockSignals(False)

        idx_sc = self.combo_uf.findData("SC")
        if idx_sc >= 0:
            self.combo_uf.setCurrentIndex(idx_sc)
        self.on_uf_changed(self.combo_uf.currentIndex())

    def on_uf_changed(self, index: int):
        """Atualiza municípios ao trocar a UF."""
        uf = self.combo_uf.currentData()
        if not uf:
            return

        self.combo_city.blockSignals(True)
        self.combo_city.clear()
        cities = get_cities_by_uf(uf)
        for c in cities:
            self.combo_city.addItem(c, c)
        self.combo_city.blockSignals(False)

        if cities:
            self.combo_city.setCurrentIndex(0)
            self.on_city_changed(0)

    def on_city_changed(self, index: int):
        """Carrega os dados da cidade e categoria selecionada."""
        uf = self.combo_uf.currentData()
        city = self.combo_city.currentData()
        if not uf or not city:
            return

        cat = self.combo_category.currentData() or "residencial"
        self.current_city_data = get_city_data(uf, city)
        self.load_city_tariffs(uf, city, cat)

    def on_category_changed(self, index: int):
        """Recarrega a categoria selecionada."""
        uf = self.combo_uf.currentData()
        city = self.combo_city.currentData()
        cat = self.combo_category.currentData() or "residencial"
        if uf and city:
            self.load_city_tariffs(uf, city, cat)

    def load_city_tariffs(self, uf: str, city: str, category: str):
        """Preenche a interface e atualiza os gráficos."""
        data = get_city_tariffs_by_category(uf, city, category=category)
        if not data:
            return

        self.active_tariffs_data = data

        self.lbl_prestador.setText(f"🏢 <b>Prestador:</b> {data.get('prestador_saneamento', '-')}")
        self.lbl_agencia.setText(f"📋 <b>Regulação:</b> {data.get('agencia_reguladora', 'Municipal')}")
        
        status_glob = data.get("status_global", "AUTO_OR_VERIFIED")
        if status_glob == "MANUAL_REVIEW_NEEDED":
            self.lbl_status_badge.setText("🟡 Revisão Decreto")
            self.lbl_status_badge.setStyleSheet("background: #fffbeb; color: #b45309; border: 1px solid #fde68a; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold;")
        else:
            self.lbl_status_badge.setText("🟢 Homologado")
            self.lbl_status_badge.setStyleSheet("background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold;")

        # Parcela Fixa e Esgoto
        t_fixa = float(data.get("tarifa_fixa_mensal", 0.0) or 0.0)
        self.spin_fixed_water.blockSignals(True)
        self.spin_sewage_pct.blockSignals(True)
        self.spin_fixed_water.setValue(t_fixa)
        self.spin_sewage_pct.setValue(float(data.get("esgoto_pct", 80.0) or 80.0))
        self.spin_fixed_water.blockSignals(False)
        self.spin_sewage_pct.blockSignals(False)

        # Callout de Disponibilidade
        faixas = data.get("faixas", [])
        tem_franquia = any(t[3] == -2 or (t[3] == -1 and t[1] > 0) for t in faixas)
        tem_minima = any(t[3] in (-1, -2) for t in faixas)
        if tem_franquia:
            f_vol = next((t[1] for t in faixas if t[3] == -2 or (t[3] == -1 and t[1] > 0)), 6.0)
            self.lbl_disp_callout.setText(f"🏷️ <b>Consumo Mínimo (Franquia):</b> R$ {t_fixa:.2f}/mês cobrindo até {f_vol:.0f} m³.")
        elif t_fixa > 0 and tem_minima:
            self.lbl_disp_callout.setText(f"🏷️ <b>Custo Fixo de Disponibilidade:</b> R$ {t_fixa:.2f}/mês somado a cada m³ medido.")
        elif t_fixa > 0:
            self.lbl_disp_callout.setText(f"🏷️ <b>Custo Fixo de Disponibilidade:</b> R$ {t_fixa:.2f}/mês somado a cada m³ medido.")
        else:
            self.lbl_disp_callout.setText("🏷️ <b>Cobrança Linear:</b> Sem parcela fixa, cobrança proporcional ao consumo.")

        # Energia
        self.lbl_distribuidora.setText(f"Distr: {data.get('distribuidora_energia', '-')}")
        self.spin_energy_kwh.setValue(float(data.get("energia_r_kwh", 0.75) or 0.75))

        # Tabela de Faixas
        self.render_tiers_table(faixas)
        self.update_bill_simulation()

    def render_tiers_table(self, faixas: List[List[Any]]):
        """Renderiza a matriz de faixas na QTableWidget."""
        self.table_tiers.blockSignals(True)
        self.table_tiers.setRowCount(len(faixas))
        for r, (inf, sup, rate, t_tipo) in enumerate(faixas):
            item_inf = QTableWidgetItem(f"{inf:.1f}")
            item_sup = QTableWidgetItem(f"{sup:.1f}" if sup < 99999 else "> 99999")
            item_rate = QTableWidgetItem(f"{rate:.4f}")
            if t_tipo == -2 or (t_tipo == -1 and sup > 0):
                tipo_desc = tr("Consumo Mínimo")
            elif t_tipo == -1:
                tipo_desc = tr("Disponibilidade")
            else:
                tipo_desc = tr("Progressiva")
            item_tipo = QTableWidgetItem(tipo_desc)

            for it in (item_inf, item_sup, item_rate, item_tipo):
                it.setTextAlignment(Qt.AlignCenter)

            self.table_tiers.setItem(r, 0, item_inf)
            self.table_tiers.setItem(r, 1, item_sup)
            self.table_tiers.setItem(r, 2, item_rate)
            self.table_tiers.setItem(r, 3, item_tipo)
        self.table_tiers.blockSignals(False)

    def on_table_modified(self, item):
        self.update_bill_simulation()

    def on_slider_changed(self, val: int):
        self.spin_sim_vol.blockSignals(True)
        self.spin_sim_vol.setValue(float(val))
        self.spin_sim_vol.blockSignals(False)
        self.update_bill_simulation()

    def on_spin_vol_changed(self, val: float):
        self.slider_sim.blockSignals(True)
        self.slider_sim.setValue(int(min(50, val)))
        self.slider_sim.blockSignals(False)
        self.update_bill_simulation()

    def on_add_tier(self):
        r = self.table_tiers.rowCount()
        self.table_tiers.blockSignals(True)
        self.table_tiers.insertRow(r)
        self.table_tiers.setItem(r, 0, QTableWidgetItem(f"{r*10:.1f}"))
        self.table_tiers.setItem(r, 1, QTableWidgetItem(f"{(r+1)*10:.1f}"))
        self.table_tiers.setItem(r, 2, QTableWidgetItem("5.0000"))
        self.table_tiers.setItem(r, 3, QTableWidgetItem(tr("Progressiva")))
        self.table_tiers.blockSignals(False)
        self.update_bill_simulation()

    def on_remove_tier(self):
        cur = self.table_tiers.currentRow()
        if cur >= 0:
            self.table_tiers.removeRow(cur)
            self.update_bill_simulation()

    def on_reset_to_defaults(self):
        uf = self.combo_uf.currentData()
        city = self.combo_city.currentData()
        cat = self.combo_category.currentData() or "residencial"
        if uf and city:
            self.load_city_tariffs(uf, city, cat)

    def on_apply_to_project(self):
        uf = self.combo_uf.currentData()
        city = self.combo_city.currentData()
        cat = self.combo_category.currentData()

        faixas_custom = []
        for r in range(self.table_tiers.rowCount()):
            try:
                inf = float(self.table_tiers.item(r, 0).text().replace(',', '.'))
                sup_str = self.table_tiers.item(r, 1).text().replace(',', '.')
                sup = 999999.0 if ">" in sup_str else float(sup_str)
                rate = float(self.table_tiers.item(r, 2).text().replace(',', '.'))
                tipo_str = self.table_tiers.item(r, 3).text()
                if "Mínim" in tipo_str or "Minim" in tipo_str or "Franquia" in tipo_str:
                    t_tipo = -2 if sup > 0 else -1
                elif "Disponibilidade" in tipo_str or "Fixa" in tipo_str:
                    t_tipo = -1
                else:
                    t_tipo = 1
                faixas_custom.append([inf, sup, rate, t_tipo])
            except Exception:
                continue

        updated_dict = {
            "uf": uf,
            "municipio": city,
            "categoria": cat,
            "tarifa_fixa_mensal": self.spin_fixed_water.value(),
            "esgoto_pct": self.spin_sewage_pct.value(),
            "energia_r_kwh": self.spin_energy_kwh.value(),
            "faixas": faixas_custom,
        }

        if self.main_window and hasattr(self.main_window, "config"):
            cfg = self.main_window.config
            cfg.water_tariffs = [(float(f[0]), float(f[1]), float(f[2]), int(f[3])) for f in faixas_custom]
            cfg.sewage_mode = 1
            cfg.sewage_rate = float(self.spin_sewage_pct.value())
            cfg.cost_energy = float(self.spin_energy_kwh.value())
            cfg.tariff_city_uf = uf
            cfg.tariff_city_name = city

        if self.main_window and hasattr(self.main_window, "tab_project"):
            if hasattr(self.main_window.tab_project, "apply_custom_tariffs"):
                self.main_window.tab_project.apply_custom_tariffs(updated_dict)

        self.tariffs_changed.emit(updated_dict)
        QMessageBox.information(
            self,
            tr("Tarifas Aplicadas"),
            tr(f"As tarifas para <b>{city} ({uf})</b> na categoria <b>{self.combo_category.currentText()}</b> foram salvas no projeto!")
        )

    def on_open_official_url(self):
        if self.active_tariffs_data:
            url = self.active_tariffs_data.get("fonte_url")
            if url and url.startswith("http"):
                QDesktopServices.openUrl(QUrl(url))

    def on_contact_link_clicked(self, link_str: str):
        """Copia o e-mail de contato para a área de transferência e abre o cliente se houver."""
        from PySide6.QtGui import QGuiApplication
        cb = QGuiApplication.clipboard()
        if cb:
            cb.setText("igorcmvaz@gmail.com")
        try:
            QDesktopServices.openUrl(QUrl(link_str))
        except Exception:
            pass
        QMessageBox.information(
            self,
            tr("Canal de Contato & Auditoria"),
            tr("O e-mail <b>igorcmvaz@gmail.com</b> foi copiado para sua área de transferência!<br><br>"
               "Você pode colar diretamente no seu provedor de e-mail (Gmail, Outlook, Webmail) para enviar notas ou atualizações.")
        )

    def _calculate_bill_for_vol(self, vol: float, faixas: List[List[Any]], fixed: float, esgoto_pct: float) -> tuple[float, float, float, float]:
        """Calcula (valor_fixo, medido_agua, esgoto, total) em perfeita harmonia com o motor econômico do Netuno."""
        # 1. Identifica se existe franquia de consumo mínimo não-cumulativa (t_tipo == -2 ou linha com sup > 0 e tipo mínimo)
        min_franchise = None
        for inf, sup, rate, t_tipo in faixas:
            if t_tipo == -2 or (t_tipo == -1 and sup > 0):
                min_franchise = (sup, rate)
                break

        fixed_water = 0.0
        metered_water = 0.0

        if min_franchise is not None:
            franchise_vol, franchise_cost = min_franchise
            if vol <= franchise_vol:
                fixed_water = franchise_cost
                metered_water = 0.0
            else:
                # Excedeu o consumo mínimo: todo o volume desde 0 m³ é faturado pelas faixas variáveis
                fixed_water = 0.0
                for inf, sup, rate, t_tipo in faixas:
                    if t_tipo == 1:
                        eff_inf = 0.0 if inf <= franchise_vol else inf
                        if vol > eff_inf:
                            vol_faixa = min(vol, sup) - eff_inf
                            if vol_faixa > 0:
                                metered_water += vol_faixa * rate
        else:
            for inf, sup, rate, t_tipo in faixas:
                if t_tipo == -1:
                    fixed_water += rate
                elif t_tipo == 1:
                    if vol > inf:
                        vol_faixa = min(vol, sup) - inf
                        if vol_faixa > 0:
                            metered_water += vol_faixa * rate

            # Se houver valor fixo inserido manualmente no campo e ausente nas faixas
            if fixed > 0 and fixed_water == 0.0:
                fixed_water = fixed

        c_agua_total = fixed_water + metered_water
        esgoto_val = c_agua_total * (esgoto_pct / 100.0)
        total_val = c_agua_total + esgoto_val
        return fixed_water, metered_water, esgoto_val, total_val

    def update_bill_simulation(self):
        """Calcula os custos e redesenha os gráficos Matplotlib."""
        vol = self.spin_sim_vol.value()
        fixed = self.spin_fixed_water.value()
        esgoto_pct = self.spin_sewage_pct.value()

        # Extrai faixas da tabela
        faixas = []
        for r in range(self.table_tiers.rowCount()):
            try:
                inf = float(self.table_tiers.item(r, 0).text().replace(',', '.'))
                sup_str = self.table_tiers.item(r, 1).text().replace(',', '.')
                sup = 999999.0 if ">" in sup_str else float(sup_str)
                rate = float(self.table_tiers.item(r, 2).text().replace(',', '.'))
                tipo_str = self.table_tiers.item(r, 3).text()
                if "Mínim" in tipo_str or "Minim" in tipo_str or "Franquia" in tipo_str:
                    t_tipo = -2 if sup > 0 else -1
                elif "Disponibilidade" in tipo_str or "Fixa" in tipo_str:
                    t_tipo = -1
                else:
                    t_tipo = 1
                faixas.append([inf, sup, rate, t_tipo])
            except Exception:
                continue

        valor_fixo, medido_val, esgoto_val, total_val = self._calculate_bill_for_vol(vol, faixas, fixed, esgoto_pct)
        eff_rate = (total_val / vol) if vol > 0 else 0.0

        self.lbl_sim_result.setText(
            f"🏷️ Fixa/Disp: <b>R$ {valor_fixo:.2f}</b> | 💧 Água Medida: <b>R$ {medido_val:.2f}</b> | "
            f"🚽 Esgoto ({esgoto_pct:.0f}%): <b>R$ {esgoto_val:.2f}</b> | "
            f"💰 <b>Total: R$ {total_val:.2f}/mês</b> (Média: R$ {eff_rate:.2f}/m³)"
        )

        # Atualiza Gráficos Matplotlib
        self.redraw_charts(faixas, fixed, esgoto_pct, vol, total_val)

    def redraw_charts(self, faixas: List[List[Any]], fixed: float, esgoto_pct: float, current_vol: float, current_bill: float):
        """Redesenha os dois subplots integrados (Step-curve + Curva de Fatura)."""
        if not hasattr(self, "ax1") or not hasattr(self, "ax2"):
            return

        self.ax1.cla()
        self.ax2.cla()

        # Subplot 1: Curva de Degraus (Tarifa Marginal R$/m³)
        max_plot_vol = 40.0
        v_steps = []
        r_steps = []

        for inf, sup, rate, t_tipo in faixas:
            if t_tipo == 1:
                x_start = min(max_plot_vol, inf)
                x_end = min(max_plot_vol, sup)
                v_steps.extend([x_start, x_end])
                r_steps.extend([rate, rate])

        if v_steps:
            self.ax1.step(v_steps, r_steps, where="post", color="#0284c7", lw=2.2, label="Tarifa Marginal (R$/m³)")
            self.ax1.fill_between(v_steps, r_steps, step="post", alpha=0.15, color="#38bdf8")

        if current_vol <= max_plot_vol:
            self.ax1.axvline(current_vol, color="#ef4444", linestyle="--", lw=1.5, label=f"Consumo: {current_vol:.1f} m³")

        self.ax1.set_xlim(0, max_plot_vol)
        self.ax1.set_ylabel("R$/m³", fontsize=9, fontweight="bold", color="#334155")
        self.ax1.set_title("Estrutura de Faixas (Tarifa Marginal R$/m³)", fontsize=10, fontweight="bold", color="#0f172a", pad=4)
        self.ax1.grid(True, linestyle=":", alpha=0.5)
        self.ax1.tick_params(labelsize=8)
        self.ax1.legend(loc="upper left", fontsize=7.5, framealpha=0.8)

        # Subplot 2: Curva de Custo Total da Fatura (R$)
        vol_range = [float(v) for v in range(0, int(max_plot_vol) + 1)]
        bills = [self._calculate_bill_for_vol(v, faixas, fixed, esgoto_pct)[3] for v in vol_range]

        self.ax2.plot(vol_range, bills, color="#059669", lw=2.4, label="Fatura Total (R$/mês)")
        self.ax2.fill_between(vol_range, bills, alpha=0.12, color="#10b981")

        if current_vol <= max_plot_vol:
            self.ax2.plot(current_vol, current_bill, marker="o", markersize=6, color="#ef4444", label=f"Total: R$ {current_bill:.2f}")
            self.ax2.axvline(current_vol, color="#ef4444", linestyle="--", lw=1.2)

        self.ax2.set_xlim(0, max_plot_vol)
        self.ax2.set_xlabel("Volume Consumido Mensal (m³)", fontsize=9, fontweight="bold", color="#334155")
        self.ax2.set_ylabel("Fatura (R$)", fontsize=9, fontweight="bold", color="#334155")
        self.ax2.set_title("Evolução da Conta Mensal de Água & Esgoto", fontsize=10, fontweight="bold", color="#0f172a", pad=4)
        self.ax2.grid(True, linestyle=":", alpha=0.5)
        self.ax2.tick_params(labelsize=8)
        self.ax2.legend(loc="upper left", fontsize=7.5, framealpha=0.8)

        self.figure.tight_layout(pad=1.2)
        try:
            self.canvas.draw()
        except Exception:
            pass
