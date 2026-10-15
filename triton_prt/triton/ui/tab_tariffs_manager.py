"""
Aba de Gestão, Visualização e Auditoria de Tarifas Nacionais (Triton).
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

from triton.ui.translation import tr, get_current_theme
from triton.ui.categorias_tarifarias import preencher_categorias
from triton.core.economic import calculate_water_bill
from triton.core.tariff_regimes import EXPONENCIAL, ler_estrutura
from triton.core.tariffs_structure import (
    ESGOTO_PERCENTUAL,
    ESGOTO_POR_M3,
    EXPOENTE_DE_CONSUMO,
    PRECO_BASE_EXPONENCIAL,
    expoente_do_consumo,
)
from triton.core.tariffs_database import (
    esgoto_do_municipio,
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
            "<a href='mailto:igorcmvaz@gmail.com?subject=Triton%20-%20Ajuste%20de%20Tarifa' style='color:#0284c7; font-weight:bold; text-decoration:underline;'>igorcmvaz@gmail.com</a>"
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
        sel_card.setObjectName("selCard")
        sel_card.setStyleSheet("#selCard { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; }")
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
        preencher_categorias(self.combo_category, None)
        sel_layout.addWidget(self.combo_category, 1, 1, 1, 3)

        left_layout.addWidget(sel_card)

        # CARTÃO INSTITUCIONAL & EVIDÊNCIA
        inst_card = QFrame()
        inst_card.setObjectName("instCard")
        inst_card.setStyleSheet("#instCard { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; }")
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
        self.lbl_agencia = QLabel(tr("📋 Regulação: -"))
        self.lbl_agencia.setStyleSheet("font-size: 11.5px; color: #475569;")
        row_inst2.addWidget(self.lbl_agencia, stretch=1)

        self.btn_open_url = QPushButton(tr("🌐 Fonte Oficial ↗"))
        self.btn_open_url.setStyleSheet("background: transparent; color: #0284c7; border: none; font-size: 11.5px; font-weight: bold; text-decoration: underline;")
        self.btn_open_url.clicked.connect(self.on_open_official_url)
        row_inst2.addWidget(self.btn_open_url)
        inst_layout.addLayout(row_inst2)

        self.lbl_disp_callout = QLabel(tr("🏷️ Custo de Disponibilidade: -"))
        self.lbl_disp_callout.setStyleSheet("font-size: 11px; color: #92400e; background: #fffbeb; border: 1px solid #fde68a; border-radius: 4px; padding: 3px 6px;")
        # Quebra de linha: sem ela, o texto da fórmula exponencial alargava a
        # coluna e espremia os gráficos.
        self.lbl_disp_callout.setWordWrap(True)
        inst_layout.addWidget(self.lbl_disp_callout)

        left_layout.addWidget(inst_card)

        # PARÂMETROS NUMÉRICOS COMPACTOS
        params_card = QFrame()
        params_card.setObjectName("paramsCard")
        params_card.setStyleSheet("#paramsCard { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; }")
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

        self._esgoto_modo = ESGOTO_PERCENTUAL
        self.lbl_sewage = QLabel(tr("Alíquota de Esgoto (%):"))
        p_layout.addWidget(self.lbl_sewage, 0, 2)
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
        # As proporções valem sobre a largura inteira, e não só sobre a sobra:
        # conteúdo largo numa coluna não rouba espaço da outra.
        left_col.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
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
        # A folha de estilo é presa ao quadro pelo nome. Sem seletor, o Qt a
        # propaga aos filhos: o `padding` caía também sobre a barra deslizante,
        # que passava a ser desenhada acima do centro da linha, desalinhada do
        # texto ao lado.
        sim_box.setObjectName("simBox")
        sim_box.setStyleSheet(
            "#simBox { background: #f8fafc; border: 1px solid #bae6fd; "
            "border-radius: 8px; padding: 10px 12px; }")
        sim_layout = QVBoxLayout(sim_box)
        sim_layout.setContentsMargins(0, 0, 0, 0)
        sim_layout.setSpacing(6)

        sim_head = QHBoxLayout()
        sim_head.addWidget(QLabel(tr("🧮 <b>Simulador em Tempo Real:</b>")))
        
        self.slider_sim = QSlider(Qt.Horizontal)
        # Estilo próprio, e não o que vazava do quadro: trilho fino centrado na
        # linha, percorrido em vermelho até o volume escolhido.
        self.slider_sim.setStyleSheet("""
            QSlider::groove:horizontal { height: 6px; border-radius: 3px; background: #e2e8f0; }
            QSlider::sub-page:horizontal { height: 6px; border-radius: 3px; background: #ef4444; }
            QSlider::handle:horizontal { width: 16px; height: 16px; margin: -5px 0;
                border-radius: 8px; background: #1f2937; border: 2px solid #ffffff; }
            QSlider::handle:horizontal:hover { background: #087f6b; }
        """)
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
        sim_head.addWidget(QLabel(tr("m³/mês")))
        sim_layout.addLayout(sim_head)

        # Demonstrativo de Fatura
        self.lbl_sim_result = QLabel(tr("🏷️ Fixa: R$ 0,00 | 💧 Água: R$ 0,00 | 🚽 Esgoto: R$ 0,00 | <b>Total: R$ 0,00 / mês</b>"))
        self.lbl_sim_result.setStyleSheet("font-size: 12px; color: #0369a1; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 5px 8px;")
        self.lbl_sim_result.setWordWrap(True)
        sim_layout.addWidget(self.lbl_sim_result)

        right_layout.addWidget(sim_box)

        # CANVAS MATPLOTLIB EMBARCADO (2 SUBPLOTS: STEP CURVE + BILL CURVE)
        self.figure = Figure(figsize=(5.5, 3.8), dpi=95)
        self.figure.patch.set_facecolor("#ffffff")
        self.figure.subplots_adjust(left=0.11, right=0.96, top=0.93, bottom=0.12, hspace=0.38)
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

        self.current_city_data = get_city_data(uf, city)
        cat = preencher_categorias(self.combo_category, self.current_city_data,
                                   self.combo_category.currentData() or "residencial")
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
        self.lbl_agencia.setText(tr('📋 <b>Regulação:</b> {0}').format(data.get('agencia_reguladora', 'Municipal')))
        
        status_glob = data.get("status_global", "AUTO_OR_VERIFIED")
        if status_glob == "MANUAL_REVIEW_NEEDED":
            self.lbl_status_badge.setText(tr("🟡 Revisão Decreto"))
            self.lbl_status_badge.setStyleSheet("background: #fffbeb; color: #b45309; border: 1px solid #fde68a; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold;")
        else:
            self.lbl_status_badge.setText("🟢 Homologado")
            self.lbl_status_badge.setStyleSheet("background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 4px; padding: 2px 6px; font-size: 11px; font-weight: bold;")

        # Parcela Fixa e Esgoto
        t_fixa = float(data.get("tarifa_fixa_mensal", 0.0) or 0.0)
        self.spin_fixed_water.blockSignals(True)
        self.spin_sewage_pct.blockSignals(True)
        self.spin_fixed_water.setValue(t_fixa)
        self._definir_modo_do_esgoto(*esgoto_do_municipio(data))
        self.spin_fixed_water.blockSignals(False)
        self.spin_sewage_pct.blockSignals(False)

        # Callout do regime
        faixas = data.get("faixas", [])
        estrutura = ler_estrutura(faixas)
        tem_franquia = any(t[3] == -2 or (t[3] == -1 and t[1] > 0) for t in faixas)
        tem_minima = any(t[3] in (-1, -2) for t in faixas)
        if estrutura.regime == EXPONENCIAL:
            texto = tr('📈 <b>Fórmula exponencial:</b> Água = PB × Cⁿ + serviço básico — PB R$ {0:.2f}/m³, serviço básico R$ {1:.2f}/mês; o expoente n cresce com o consumo do mês, pela Tabela de Exponenciais.').format(
                estrutura.preco_base, estrutura.custo_fixo_mensal)
            if data.get("expoentes_verificados") is False:
                texto += tr(' ⚠️ Tabela exponencial não conferida com a homologada: edite as linhas «Expoente n» com a tabela vigente.')
            self.lbl_disp_callout.setText(texto)
        elif tem_franquia:
            f_vol = next((t[1] for t in faixas if t[3] == -2 or (t[3] == -1 and t[1] > 0)), 6.0)
            self.lbl_disp_callout.setText(tr('🏷️ <b>Consumo Mínimo (Franquia):</b> R$ {0:.2f}/mês cobrindo até {1:.0f} m³.').format(t_fixa, f_vol))
        elif t_fixa > 0 and tem_minima:
            self.lbl_disp_callout.setText(tr('🏷️ <b>Custo Fixo de Disponibilidade:</b> R$ {0:.2f}/mês somado a cada m³ medido.').format(t_fixa))
        elif t_fixa > 0:
            self.lbl_disp_callout.setText(tr('🏷️ <b>Custo Fixo de Disponibilidade:</b> R$ {0:.2f}/mês somado a cada m³ medido.').format(t_fixa))
        else:
            self.lbl_disp_callout.setText(tr("🏷️ <b>Cobrança Linear:</b> Sem parcela fixa, cobrança proporcional ao consumo."))

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
            item_tipo = QTableWidgetItem(self._rotulo_do_tipo(int(t_tipo), sup))

            for it in (item_inf, item_sup, item_rate, item_tipo):
                it.setTextAlignment(Qt.AlignCenter)

            self.table_tiers.setItem(r, 0, item_inf)
            self.table_tiers.setItem(r, 1, item_sup)
            self.table_tiers.setItem(r, 2, item_rate)
            self.table_tiers.setItem(r, 3, item_tipo)
        self.table_tiers.blockSignals(False)

    def _definir_modo_do_esgoto(self, modo: int, valor: float) -> None:
        """Percentual da água ou preço por m³ consumido, no mesmo campo."""
        self._esgoto_modo = modo
        if modo == ESGOTO_POR_M3:
            self.lbl_sewage.setText(tr("Esgoto (R$/m³ consumido):"))
            self.spin_sewage_pct.setDecimals(2)
            self.spin_sewage_pct.setRange(0.0, 100.0)
        else:
            self.lbl_sewage.setText(tr("Alíquota de Esgoto (%):"))
            self.spin_sewage_pct.setDecimals(1)
            self.spin_sewage_pct.setRange(0.0, 200.0)
        self.spin_sewage_pct.setValue(valor)

    def _rotulo_do_esgoto(self, valor: float) -> str:
        if self._esgoto_modo == ESGOTO_POR_M3:
            return f"R$ {valor:.2f}/m³"
        return f"{valor:.0f}%"

    @staticmethod
    def _rotulo_do_tipo(t_tipo: int, sup: float) -> str:
        if t_tipo == PRECO_BASE_EXPONENCIAL:
            return tr("Preço-base (PB × Cⁿ)")
        if t_tipo == EXPOENTE_DE_CONSUMO:
            return tr("Expoente n")
        if t_tipo == -3:
            return tr("Piso de pagamento")
        if t_tipo == -2 or (t_tipo == -1 and sup > 0):
            return tr("Consumo Mínimo")
        if t_tipo == -1:
            return tr("Disponibilidade")
        return tr("Progressiva")

    @staticmethod
    def _tipo_do_rotulo(tipo_str: str, sup: float) -> int:
        if "PB" in tipo_str or tipo_str == tr("Preço-base (PB × Cⁿ)"):
            return PRECO_BASE_EXPONENCIAL
        if "Expoente" in tipo_str or tipo_str == tr("Expoente n"):
            return EXPOENTE_DE_CONSUMO
        if "Piso" in tipo_str or tipo_str == tr("Piso de pagamento"):
            return -3
        if "Mínim" in tipo_str or "Minim" in tipo_str or "Franquia" in tipo_str or tipo_str == tr("Consumo Mínimo"):
            return -2 if sup > 0 else -1
        if "Disponibilidade" in tipo_str or "Fixa" in tipo_str or tipo_str == tr("Disponibilidade"):
            return -1
        return 1

    def _faixas_da_tabela(self) -> List[List[Any]]:
        """Lê a tabela editável de volta para quádruplas."""
        faixas = []
        for r in range(self.table_tiers.rowCount()):
            try:
                inf = float(self.table_tiers.item(r, 0).text().replace(',', '.'))
                sup_str = self.table_tiers.item(r, 1).text().replace(',', '.')
                sup = 999999.0 if ">" in sup_str else float(sup_str)
                rate = float(self.table_tiers.item(r, 2).text().replace(',', '.'))
                t_tipo = self._tipo_do_rotulo(self.table_tiers.item(r, 3).text(), sup)
                faixas.append([inf, sup, rate, t_tipo])
            except Exception:
                continue
        return faixas

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

        faixas_custom = self._faixas_da_tabela()

        updated_dict = {
            "uf": uf,
            "municipio": city,
            "categoria": cat,
            "tarifa_fixa_mensal": self.spin_fixed_water.value(),
            "esgoto_modo": self._esgoto_modo,
            "esgoto_pct": self.spin_sewage_pct.value() if self._esgoto_modo != ESGOTO_POR_M3 else None,
            "esgoto_r_m3": self.spin_sewage_pct.value() if self._esgoto_modo == ESGOTO_POR_M3 else None,
            "energia_r_kwh": self.spin_energy_kwh.value(),
            "faixas": faixas_custom,
        }

        if self.main_window and hasattr(self.main_window, "config"):
            cfg = self.main_window.config
            cfg.water_tariffs = [(float(f[0]), float(f[1]), float(f[2]), int(f[3])) for f in faixas_custom]
            cfg.sewage_mode = self._esgoto_modo
            cfg.sewage_rate = float(self.spin_sewage_pct.value())
            cfg.cost_energy = float(self.spin_energy_kwh.value())
            cfg.tariff_city_uf = uf
            cfg.tariff_city_name = city
            cfg.tariff_category = cat or "residencial"

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
        """Calcula (valor_fixo, medido_agua, esgoto, total) com o próprio motor econômico.

        Não há uma segunda implementação da conta aqui: a fatura simulada é a de
        `calculate_water_bill`, inclusive na fórmula exponencial e no piso.
        """
        quadruplas = [(float(a), float(b), float(c), int(d)) for a, b, c, d in faixas]
        agua = calculate_water_bill(vol * 1000.0, quadruplas, sewage_mode=1, sewage_rate=0.0) if quadruplas else 0.0

        franquia = next(((sup, rate) for inf, sup, rate, t in quadruplas if t == -2), None)
        if franquia is not None:
            fixed_water = franquia[1] if vol <= franquia[0] else 0.0
        else:
            fixed_water = sum(rate for inf, sup, rate, t in quadruplas if t == -1)
            # Valor fixo inserido no campo e ausente das faixas
            if fixed > 0 and fixed_water == 0.0:
                fixed_water = fixed
                agua += fixed
        metered_water = max(0.0, agua - fixed_water)

        c_agua_total = fixed_water + metered_water
        if self._esgoto_modo == ESGOTO_POR_M3:
            esgoto_val = esgoto_pct * vol  # R$/m³ sobre o consumo, sem serviço básico
        else:
            esgoto_val = c_agua_total * (esgoto_pct / 100.0)
        total_val = c_agua_total + esgoto_val
        return fixed_water, metered_water, esgoto_val, total_val

    def update_bill_simulation(self):
        """Calcula os custos e redesenha os gráficos Matplotlib."""
        vol = self.spin_sim_vol.value()
        fixed = self.spin_fixed_water.value()
        esgoto_pct = self.spin_sewage_pct.value()

        faixas = self._faixas_da_tabela()

        valor_fixo, medido_val, esgoto_val, total_val = self._calculate_bill_for_vol(vol, faixas, fixed, esgoto_pct)
        eff_rate = (total_val / vol) if vol > 0 else 0.0

        texto = tr('🏷️ Fixa/Disp: <b>R$ {0:.2f}</b> | 💧 Água Medida: <b>R$ {1:.2f}</b> | 🚽 Esgoto ({2}): <b>R$ {3:.2f}</b> | 💰 <b>Total: R$ {4:.2f}/mês</b> (Média: R$ {5:.2f}/m³)').format(valor_fixo, medido_val, self._rotulo_do_esgoto(esgoto_pct), esgoto_val, total_val, eff_rate)
        estrutura = ler_estrutura(faixas)
        if estrutura.regime == EXPONENCIAL and vol > 0:
            c = min(vol, estrutura.teto_exponencial_m3)
            n = expoente_do_consumo(faixas, c)
            texto += "<br>" + '📈 PB × Cⁿ = {0:.2f} × {1:g}^{2:.4f} = <b>R$ {3:.2f}</b>'.format(
                estrutura.preco_base, c, n, estrutura.preco_base * c ** n)
        self.lbl_sim_result.setText(texto)

        # Atualiza Gráficos Matplotlib
        self.redraw_charts(faixas, fixed, esgoto_pct, vol, total_val)

    def safe_draw(self):
        """Atualização segura do canvas sem falhas de destruição de widgets ou timers pendentes."""
        try:
            if not hasattr(self, "canvas") or not self.canvas:
                return
            self.canvas.draw()
        except Exception:
            pass

    def showEvent(self, event):
        super().showEvent(event)
        self.figure.subplots_adjust(left=0.11, right=0.96, top=0.93, bottom=0.12, hspace=0.38)
        self.safe_draw()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.figure.subplots_adjust(left=0.11, right=0.96, top=0.93, bottom=0.12, hspace=0.38)

    def redraw_charts(self, faixas: List[List[Any]], fixed: float, esgoto_pct: float, current_vol: float, current_bill: float):
        """Redesenha os dois subplots integrados (Step-curve + Curva de Fatura)."""
        if not hasattr(self, "ax1") or not hasattr(self, "ax2"):
            return

        self.ax1.cla()
        self.ax2.cla()

        # Subplot 1: Curva de Degraus (Tarifa Marginal R$/m³)
        max_plot_vol = 50.0
        v_steps = []
        r_steps = []

        for inf, sup, rate, t_tipo in faixas:
            if t_tipo == 1:
                x_start = min(max_plot_vol, inf)
                x_end = min(max_plot_vol, sup)
                v_steps.extend([x_start, x_end])
                r_steps.extend([rate, rate])

        estrutura = ler_estrutura(faixas)
        if estrutura.regime == EXPONENCIAL:
            # Na fórmula exponencial não há degrau: o m³ custa, em média, PB × Cⁿ⁻¹.
            cs = [max(0.5, v * 0.5) for v in range(1, int(max_plot_vol * 2) + 1)]
            medio = [estrutura.preco_base * c ** (expoente_do_consumo(faixas, c) - 1.0) for c in cs]
            self.ax1.plot(cs, medio, color="#0284c7", lw=2.2, label="Preço médio PB·Cⁿ⁻¹ (R$/m³)")
            self.ax1.fill_between(cs, medio, alpha=0.15, color="#38bdf8")
        elif v_steps:
            self.ax1.step(v_steps, r_steps, where="post", color="#0284c7", lw=2.2, label="Tarifa Marginal (R$/m³)")
            self.ax1.fill_between(v_steps, r_steps, step="post", alpha=0.15, color="#38bdf8")

        if current_vol <= max_plot_vol:
            self.ax1.axvline(current_vol, color="#ef4444", linestyle="--", lw=1.5, label=f"Consumo: {current_vol:.1f} m³")

        self.ax1.set_xlim(0, max_plot_vol)
        self.ax1.set_ylabel("R$/m³", fontsize=9, fontweight="bold", color="#334155")
        titulo = (tr("Preço Médio do m³ (PB × Cⁿ⁻¹, R$/m³)") if estrutura.regime == EXPONENCIAL
                  else tr("Estrutura de Faixas (Tarifa Marginal R$/m³)"))
        self.ax1.set_title(titulo, fontsize=10, fontweight="bold", color="#0f172a", pad=4)
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
        self.ax2.set_title(tr("Evolução da Conta Mensal de Água & Esgoto"), fontsize=10, fontweight="bold", color="#0f172a", pad=4)
        self.ax2.grid(True, linestyle=":", alpha=0.5)
        self.ax2.tick_params(labelsize=8)
        self.ax2.legend(loc="upper left", fontsize=7.5, framealpha=0.8)

        self.figure.subplots_adjust(left=0.11, right=0.96, top=0.93, bottom=0.12, hspace=0.38)
        self.safe_draw()
