import math
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, 
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, 
    QRadioButton, QMessageBox, QCheckBox, QHeaderView, QFrame, QScrollArea,
    QApplication
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QFont, QDesktopServices

from netuno.ui.translation import tr, get_current_theme
from netuno.core.parser import NetunoConfig, format_ptbr
from netuno.core.economic import run_economic_analysis, calculate_water_bill
from netuno.core.tariff_regimes import resumo_do_regime, validar_estrutura
from netuno.core.tariff_category import incompatibilidade_de_categoria
from netuno.core.tariffs_database import (
    get_available_ufs, get_cities_by_uf, get_city_data, get_total_cities_count,
    search_cities
)
from netuno.core.cost_estimates import (
    LOWER_TANK_PRICE_TABLE, UPPER_TANK_PRICE_TABLE, estimate_preliminary_capex,
    COSTS_FILE_PATH, _refresh_runtime_constants, REGIONAL_FACTORS_BY_UF,
    COMMERCIAL_PIPES_CAPEX, PIPE_COST_PER_METER, compute_pipe_item_cost
)


def adapt_dialog_size(dlg, target_w=980, target_h=840, min_w=680, min_h=580):
    """Redimensiona o diálogo para acomodar todo o conteúdo sem barras de rolagem desnecessárias."""
    screen = dlg.screen() or QApplication.primaryScreen()
    if screen:
        avail = screen.availableGeometry()
        w = min(target_w, max(min_w, int(avail.width() * 0.92)))
        h = min(target_h, max(min_h, int(avail.height() * 0.92)))
        dlg.resize(w, h)
    else:
        dlg.resize(target_w, target_h)


class DialogLowerTankVol(QDialog):
    """
    Diálogo para Especificação do Volume do Reservatório Inferior na Análise Econômica.
    Permite escolher qualquer volume da varredura técnica ou personalizar um volume específico.
    """
    def __init__(self, parent=None, current_vol=2000.0, optimal_vol=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Volume do reservatório inferior para a análise econômica"))
        self.resize(400, 230)
        self.vol = current_vol
        self.optimal_vol = optimal_vol
        self.init_ui()

    def init_ui(self):
        lay = QVBoxLayout()
        lay.setSpacing(10)

        gb = QGroupBox(tr("Seleção do Volume para Análise Econômica (litros)"))
        gb_lay = QVBoxLayout()

        self.radio_opt = QRadioButton()
        self.radio_custom = QRadioButton()

        if self.optimal_vol:
            self.radio_opt.setChecked(True)
        else:
            self.radio_opt.setEnabled(False)
            self.radio_custom.setChecked(True)

        gb_lay.addWidget(self.radio_opt)
        gb_lay.addWidget(self.radio_custom)
        gb.setLayout(gb_lay)
        lay.addWidget(gb)

        self.txt_vol = QLineEdit(f"{self.vol:.0f}")
        lay.addWidget(self.txt_vol)

        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"

        self.setStyleSheet(f"""
            QRadioButton {{ padding: 3px; }}
            QRadioButton:checked {{ font-weight: bold; color: {text_color}; }}
        """)

        self.radio_opt.toggled.connect(self.update_checks)
        self.radio_custom.toggled.connect(self.update_checks)
        self.radio_custom.toggled.connect(lambda chk: self.txt_vol.setEnabled(chk))
        self.txt_vol.setEnabled(self.radio_custom.isChecked())
        self.update_checks()

        btn_ok = QPushButton(tr("Concluir"))
        btn_ok.setFixedHeight(30)
        btn_ok.clicked.connect(self.on_accept)
        lay.addWidget(btn_ok)

        self.setLayout(lay)

    def update_checks(self):
        opt_base = f"{tr('Volume de referência da varredura')} ({self.optimal_vol:.0f} {tr('litros')})" if self.optimal_vol else tr("Volume de referência da simulação")
        custom_base = tr("Especificar volume personalizado (litros)")
        
        if self.radio_opt.isChecked():
            self.radio_opt.setText(f"✓ {opt_base}")
            self.radio_custom.setText(custom_base)
        else:
            self.radio_opt.setText(opt_base)
            self.radio_custom.setText(f"✓ {custom_base}")

    def on_accept(self):
        try:
            if self.radio_opt.isChecked() and self.optimal_vol:
                self.vol = float(self.optimal_vol)
            else:
                self.vol = float(self.txt_vol.text().replace(',', '.'))
            self.accept()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Insira um volume válido."))


class DialogTariffs(QDialog):
    """
    Diálogo completo para Tarifas Municipais de Água, Esgoto e Eletricidade.
    Contém a base oficial auditada de 652 cidades brasileiras (27 UFs),
    com seletor Estado-Cidade, auto-preenchimento das faixas e alíquotas de esgoto,
    card com prestador, agência reguladora, vigência, grau de confiança,
    link direto clicável da resolução oficial da concessionária e aviso/disclaimer de vigência.
    """
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        
        # Get parent currency symbol
        self._sym = "R$"
        if parent and hasattr(parent, 'get_currency_symbol'):
            self._sym = parent.get_currency_symbol()
            
        self.setWindowTitle(f"{tr('Tarifas de água e esgoto')} ({self._sym})")
        adapt_dialog_size(self, target_w=980, target_h=820, min_w=680, min_h=620)
        self.setMinimumWidth(640)
        self.config = config or NetunoConfig()
        self._current_city_data = None
        self._is_populating_ui = False
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"
        card_bg = "#1e293b" if is_dark else "#f8fafc"
        card_border = "#334155" if is_dark else "#cbd5e1"
        sub_text_color = "#94a3b8" if is_dark else "#64748b"
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setSpacing(10)
        lay.setContentsMargins(6, 6, 6, 6)

        # ── BLOCO 1: SELEÇÃO MUNICIPAL & BASE DE TARIFAS AUDITADAS (652 CIDADES) ──
        gb_city = QGroupBox(tr("🏛️ Base de Tarifas Municipais Oficiais (652 Cidades - Brasil)"))
        gb_city.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_city = QVBoxLayout(gb_city)
        lay_city.setSpacing(8)
        
        lbl_sel_info = QLabel(tr(
            "Selecione o Estado (UF) e o Município para carregar automaticamente a estrutura tarifária oficial auditada (Residencial), ou escolha 'Personalizado':"
        ))
        lbl_sel_info.setWordWrap(True)
        lbl_sel_info.setStyleSheet(f"font-size: 11px; font-weight: normal; color: {sub_text_color};")
        lay_city.addWidget(lbl_sel_info)

        # Busca de municipio: a selecao exigia saber a UF de antemao, e a base
        # tem 652 municipios de 27 estados. A busca varre nome, estado e
        # prestadora de saneamento, e posiciona os dois combos no resultado.
        row_busca = QHBoxLayout()
        row_busca.setSpacing(6)
        row_busca.addWidget(QLabel(f"<b>{tr('Buscar município:')}</b>"))
        self.txt_busca_municipio = QLineEdit()
        self.txt_busca_municipio.setPlaceholderText(
            tr("Nome do município, estado ou prestadora (ex.: Joinville, CASAN)"))
        self.txt_busca_municipio.textEdited.connect(self._buscar_municipio)
        row_busca.addWidget(self.txt_busca_municipio, stretch=1)
        self.lbl_busca_resultado = QLabel("")
        self.lbl_busca_resultado.setStyleSheet("color: #475569; font-size: 11px;")
        row_busca.addWidget(self.lbl_busca_resultado)
        lay_city.addLayout(row_busca)

        row_sel = QHBoxLayout()
        row_sel.setSpacing(6)
        row_sel.addWidget(QLabel(f"<b>{tr('Estado (UF):')}</b>"))
        self.combo_uf = QComboBox()
        self.combo_uf.setMinimumWidth(110)
        row_sel.addWidget(self.combo_uf)

        row_sel.addWidget(QLabel(f"<b>{tr('Município:')}</b>"))
        self.combo_city = QComboBox()
        self.combo_city.setMinimumWidth(160)
        row_sel.addWidget(self.combo_city, stretch=1)

        row_sel.addWidget(QLabel(f"<b>{tr('Categoria:')}</b>"))
        self.combo_category = QComboBox()
        self.combo_category.setMinimumWidth(150)
        from netuno.core.tariffs_database import CATEGORIAS_TARIFARIAS
        for cat_id, cat_info in CATEGORIAS_TARIFARIAS.items():
            self.combo_category.addItem(f"{cat_info['icone']} {tr(cat_info['nome'])}", cat_id)
        row_sel.addWidget(self.combo_category)

        self.btn_load_city = QPushButton(tr("📥 Carregar"))
        self.btn_load_city.setMinimumWidth(90)
        self.btn_load_city.setToolTip(tr("Aplica os dados tarifários oficiais da cidade e categoria selecionada"))
        self.btn_load_city.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: white;
                font-weight: bold;
                padding: 5px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)
        self.btn_load_city.clicked.connect(self.apply_city_tariffs)
        row_sel.addWidget(self.btn_load_city)
        lay_city.addLayout(row_sel)

        # Card de Auditoria & Evidência
        self.card_info = QFrame()
        self.card_info.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
            }}
            QLabel {{
                color: {'#e2e8f0' if is_dark else '#1e293b'};
            }}
        """)
        card_lay = QVBoxLayout(self.card_info)
        card_lay.setContentsMargins(10, 8, 10, 8)
        card_lay.setSpacing(6)

        # Linha 0: Tipologia / Categoria
        row_tipo = QHBoxLayout()
        self.lbl_tipologia = QLabel(f"🏠 <b>{tr('Tipologia / Categoria:')}</b> {tr('Residencial (Padrão Normal)')}")
        self.lbl_tipologia.setStyleSheet(f"font-size: 11.5px; font-weight: bold; color: {text_color};")
        row_tipo.addWidget(self.lbl_tipologia)
        row_tipo.addStretch()
        card_lay.addLayout(row_tipo)

        # Linha 1: Prestador & Vigência
        row_info1 = QHBoxLayout()
        self.lbl_prestador = QLabel(f"🏢 <b>{tr('Prestador:')}</b> --")
        self.lbl_prestador.setStyleSheet("font-size: 11.5px;")
        self.lbl_vigencia = QLabel(f"📋 <b>{tr('Regulação & Vigência:')}</b> --")
        self.lbl_vigencia.setStyleSheet("font-size: 11.5px;")
        row_info1.addWidget(self.lbl_prestador, stretch=1)
        row_info1.addWidget(self.lbl_vigencia, stretch=1)
        card_lay.addLayout(row_info1)

        # Linha 2: Confiança da Base & Link Clicável
        row_info2 = QHBoxLayout()
        self.lbl_confianca = QLabel(f"⭐ <b>{tr('Confiança da Base:')}</b> --")
        self.lbl_confianca.setStyleSheet("font-size: 11.5px;")
        self.btn_open_url = QPushButton(tr("🔗 Abrir Resolução / Fonte Oficial"))
        self.btn_open_url.setCursor(Qt.PointingHandCursor)
        self.btn_open_url.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #0284c7;
                font-weight: bold;
                text-decoration: underline;
                border: none;
                text-align: left;
                padding: 0px 4px;
            }
            QPushButton:hover { color: #0369a1; }
        """)
        self.btn_open_url.clicked.connect(self.on_open_source_url)
        row_info2.addWidget(self.lbl_confianca)
        row_info2.addWidget(self.btn_open_url)
        row_info2.addStretch()
        card_lay.addLayout(row_info2)

        # Linha 2.1: regime de tarifa minima e ressalva de estrutura.
        self.lbl_regime = QLabel("")
        self.lbl_regime.setWordWrap(True)
        self.lbl_regime.setStyleSheet("font-size: 11px; color: #1e3a8a;")
        card_lay.addWidget(self.lbl_regime)

        self.lbl_estrutura_aviso = QLabel("")
        self.lbl_estrutura_aviso.setWordWrap(True)
        self.lbl_estrutura_aviso.setStyleSheet(
            "font-size: 11px; color: #7c2d12; background-color: #fef3c7; "
            "border: 1px solid #fbbf24; border-radius: 4px; padding: 5px;"
        )
        self.lbl_estrutura_aviso.setVisible(False)
        card_lay.addWidget(self.lbl_estrutura_aviso)

        # Linha 3: Eletricidade B1 (ANEEL)
        row_elec = QHBoxLayout()
        self.chk_update_elec = QCheckBox(tr("Sincronizar tarifa de eletricidade B1 (ANEEL)"))
        self.chk_update_elec.setChecked(True)
        self.lbl_elec_info = QLabel("")
        self.lbl_elec_info.setStyleSheet(f"font-size: 11px; color: {sub_text_color};")
        row_elec.addWidget(self.chk_update_elec)
        row_elec.addWidget(self.lbl_elec_info)
        row_elec.addStretch()
        card_lay.addLayout(row_elec)

        # Linha 4: Caixa de Aviso / Disclaimer de Vigência & Contato
        disc_bg = "rgba(245, 158, 11, 0.14)" if is_dark else "#fffbeb"
        disc_border = "#f59e0b" if is_dark else "#fcd34d"
        disc_text = "#fbbf24" if is_dark else "#92400e"
        self.box_disclaimer = QFrame()
        self.box_disclaimer.setStyleSheet(f"""
            QFrame {{
                background-color: {disc_bg};
                border: 1px solid {disc_border};
                border-radius: 4px;
            }}
        """)
        lay_disc = QVBoxLayout(self.box_disclaimer)
        lay_disc.setContentsMargins(8, 6, 8, 6)
        self.lbl_disclaimer = QLabel(tr(
            "📅 <b>Auditoria Tarifária:</b> Tarifas auditadas e validadas oficialmente com suporte a todas as categorias (Residencial, Comercial, Industrial, Pública, Social). "
            "<br>📌 <i>Caso este valor esteja errado ou defasado, favor contatar pelo e-mail: <a href='mailto:igorcmvaz@gmail.com?subject=Netuno%205%20-%20Ajuste%20de%20Tarifa' style='color:#0284c7;font-weight:bold;'>igorcmvaz@gmail.com</a></i>"
        ))
        self.lbl_disclaimer.setOpenExternalLinks(False)
        self.lbl_disclaimer.linkActivated.connect(self.on_contact_link_clicked)
        self.lbl_disclaimer.setWordWrap(True)
        self.lbl_disclaimer.setStyleSheet(f"font-size: 10.5px; color: {disc_text}; background: transparent; border: none;")
        lay_disc.addWidget(self.lbl_disclaimer)
        card_lay.addWidget(self.box_disclaimer)

        lay_city.addWidget(self.card_info)
        lay.addWidget(gb_city)

        # ── BLOCO 2: FAIXAS DE TARIFA DE ÁGUA ──
        lay.addWidget(QLabel(tr("<b>Faixas de tarifa de água potável (por unidade habitacional):</b>")))
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([tr("Intervalo"), tr("Volume (m³)"), tr("Custo"), tr("Valor")])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setMinimumHeight(140)
        self.table.itemChanged.connect(self.on_table_item_changed)
        lay.addWidget(self.table)

        row_btns = QHBoxLayout()
        btn_add = QPushButton(tr("➕ Adicionar faixa"))
        btn_add.clicked.connect(self.on_add_row)
        btn_rem = QPushButton(tr("➖ Excluir faixa"))
        btn_rem.clicked.connect(self.on_rem_row)
        row_btns.addWidget(btn_add)
        row_btns.addWidget(btn_rem)
        row_btns.addStretch()
        lay.addLayout(row_btns)

        # ── BLOCO 3: TARIFA DE ESGOTO ──
        gb_esgoto = QGroupBox(tr("Tarifa de esgoto"))
        lay_esg = QHBoxLayout()
        self.radio_esg_fix = QRadioButton()
        self.radio_esg_var = QRadioButton()
        
        is_brl = (self._sym == "R$")
        esg_mode = getattr(self.config, 'sewage_mode', 1)
        if esg_mode == 0:
            self.radio_esg_fix.setChecked(True)
        else:
            self.radio_esg_var.setChecked(True)

        esg_val = getattr(self.config, 'sewage_rate', 100.0 if is_brl else 0.0)
        esg_val_str = f"{esg_val:.1f}".replace('.', ',') if (esg_val > 0 or is_brl) else ""
        self.txt_esg_val = QLineEdit(esg_val_str)
        self.txt_esg_val.setFixedWidth(100)

        lay_esg.addWidget(self.radio_esg_fix)
        lay_esg.addWidget(self.radio_esg_var)
        lay_esg.addWidget(self.txt_esg_val)
        lay_esg.addStretch()
        gb_esgoto.setLayout(lay_esg)
        lay.addWidget(gb_esgoto)

        # ── BLOCO 4: IMPOSTOS SOBRE A CONTA DE AGUA ──
        # O motor economico soma os dois desde sempre; ate esta versao a tela
        # nao os oferecia e ainda os zerava ao fechar.
        gb_imp = QGroupBox(tr("Impostos e encargos sobre a conta de água (opcional)"))
        lay_imp = QHBoxLayout()
        _tax_fix = float(getattr(self.config, "water_tax_fixed", 0.0) or 0.0)
        _tax_var = float(getattr(self.config, "water_tax_var", 0.0) or 0.0)
        lay_imp.addWidget(QLabel(tr("Imposto fixo (R$/mês):")))
        self.txt_tax_fix = QLineEdit(f"{_tax_fix:.2f}".replace(".", ","))
        self.txt_tax_fix.setFixedWidth(90)
        lay_imp.addWidget(self.txt_tax_fix)
        lay_imp.addSpacing(18)
        lay_imp.addWidget(QLabel(tr("Imposto variável (%):")))
        self.txt_tax_var = QLineEdit(f"{_tax_var:.2f}".replace(".", ","))
        self.txt_tax_var.setFixedWidth(90)
        lay_imp.addWidget(self.txt_tax_var)
        lay_imp.addStretch()
        gb_imp.setLayout(lay_imp)
        lay.addWidget(gb_imp)

        # Estilo de RadioButtons
        self.setStyleSheet(f"""
            QRadioButton {{ padding: 3px; }}
            QRadioButton:checked {{ font-weight: bold; color: {text_color}; }}
        """)

        self.radio_esg_fix.toggled.connect(self.update_esg_checks)
        self.radio_esg_var.toggled.connect(self.update_esg_checks)
        self.update_esg_checks()

        # Botões de Ação
        row_actions = QHBoxLayout()
        btn_cancel = QPushButton(tr("Cancelar"))
        btn_cancel.setFixedHeight(32)
        btn_cancel.clicked.connect(self.reject)
        
        btn_ok = QPushButton(tr("Concluir e Aplicar"))
        btn_ok.setFixedHeight(32)
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                font-weight: bold;
                padding: 6px 18px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #047857; }
        """)
        btn_ok.clicked.connect(self.on_accept)
        
        row_actions.addStretch()
        row_actions.addWidget(btn_cancel)
        row_actions.addWidget(btn_ok)
        lay.addLayout(row_actions)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Inicializa a lista de cidades e restaura seleção
        self.init_city_database_ui()

    def init_city_database_ui(self):
        self._is_populating_ui = True
        try:
            self.combo_uf.clear()
            self.combo_uf.addItem(tr("⚙️ Personalizado"), "CUSTOM")
            ufs = get_available_ufs()
            for uf_code, state_name in ufs:
                self.combo_uf.addItem(f"{uf_code} - {state_name}", uf_code)

            saved_uf = getattr(self.config, 'tariff_city_uf', 'SC')
            saved_city = getattr(self.config, 'tariff_city_name', 'Florianópolis')

            # Localiza UF
            uf_idx = -1
            for i in range(self.combo_uf.count()):
                if self.combo_uf.itemData(i) == saved_uf:
                    uf_idx = i
                    break
            if uf_idx >= 0:
                self.combo_uf.setCurrentIndex(uf_idx)
            else:
                self.combo_uf.setCurrentIndex(1 if self.combo_uf.count() > 1 else 0)

            self.populate_cities_for_current_uf(select_city=saved_city)
            
            if saved_uf != "CUSTOM" and saved_city not in ("CUSTOM", "Personalizado"):
                self.apply_city_tariffs()
            elif self.config.water_tariffs:
                self.populate_table_from_tariffs(self.config.water_tariffs)
            else:
                self.apply_city_tariffs()

        finally:
            self._is_populating_ui = False

        self.combo_uf.currentIndexChanged.connect(self.on_uf_changed)
        self.combo_city.currentIndexChanged.connect(self.on_city_changed)
        self.combo_category.currentIndexChanged.connect(self.apply_city_tariffs)
        self.update_city_preview()

    def _buscar_municipio(self, texto: str):
        """Posiciona os combos no primeiro municipio que casa com a busca.

        Devolve o numero de resultados para que o usuario saiba que ha mais de
        um, e nao se surpreenda com a escolha feita por ele.
        """
        consulta = (texto or "").strip()
        if len(consulta) < 3:
            self.lbl_busca_resultado.setText("")
            return

        achados = search_cities(consulta, limit=20)
        if not achados:
            self.lbl_busca_resultado.setText(tr("nenhum município encontrado"))
            return

        primeiro = achados[0]
        uf = primeiro.get("uf", "")
        municipio = primeiro.get("municipio", "")
        if not uf or not municipio:
            return

        idx_uf = self.combo_uf.findData(uf)
        if idx_uf < 0:
            return

        anterior = self._is_populating_ui
        self._is_populating_ui = True
        try:
            self.combo_uf.setCurrentIndex(idx_uf)
            self.populate_cities_for_current_uf(select_city=municipio)
        finally:
            self._is_populating_ui = anterior

        prestadora = primeiro.get("prestador_saneamento", "")
        sufixo = f" — {prestadora}" if prestadora else ""
        extra = f" (+{len(achados) - 1})" if len(achados) > 1 else ""
        self.lbl_busca_resultado.setText(f"{uf} · {municipio}{sufixo}{extra}")

        self.apply_city_tariffs()
        self.update_city_preview()

    def populate_cities_for_current_uf(self, select_city=None):
        uf_code = self.combo_uf.currentData() or "CUSTOM"
        
        prev_blocked = self.combo_city.blockSignals(True)
        self.combo_city.clear()
        
        if uf_code == "CUSTOM":
            self.combo_city.addItem(tr("⚙️ Personalizado (Definir faixas manualmente)"), "CUSTOM")
            self.combo_city.setEnabled(False)
        else:
            self.combo_city.setEnabled(True)
            self.combo_city.addItem(tr("⚙️ Personalizado (Definir faixas manualmente)"), "CUSTOM")
            cities = get_cities_by_uf(uf_code)
            for c in cities:
                self.combo_city.addItem(c, c)
            
            if select_city and select_city not in ("CUSTOM", "Personalizado"):
                idx = self.combo_city.findData(select_city)
                if idx >= 0:
                    self.combo_city.setCurrentIndex(idx)
                else:
                    self.combo_city.setCurrentIndex(1 if self.combo_city.count() > 1 else 0)
            elif select_city in ("CUSTOM", "Personalizado"):
                self.combo_city.setCurrentIndex(0)
            elif self.combo_city.count() > 1:
                self.combo_city.setCurrentIndex(1)
            else:
                self.combo_city.setCurrentIndex(0)
            
        self.combo_city.blockSignals(prev_blocked)

    def on_uf_changed(self):
        if self._is_populating_ui:
            return
        self.populate_cities_for_current_uf()
        self.update_city_preview()
        city_val = self.combo_city.currentData()
        if city_val and city_val != "CUSTOM":
            self.apply_city_tariffs()

    def on_city_changed(self):
        if self._is_populating_ui:
            return
        self.update_city_preview()
        city_val = self.combo_city.currentData()
        if city_val and city_val != "CUSTOM":
            self.apply_city_tariffs()

    def update_city_preview(self):
        uf_code = self.combo_uf.currentData() or ""
        city_data_val = self.combo_city.currentData()
        is_custom = (uf_code == "CUSTOM" or city_data_val == "CUSTOM")
        
        if is_custom:
            self._current_city_data = None
            self.lbl_tipologia.setText(f"🏠 <b>{tr('Tipologia / Categoria:')}</b> {tr('Residencial (Personalizado)')}")
            self.lbl_prestador.setText(f"🏢 <b>{tr('Prestador:')}</b> {tr('Definido pelo usuário')}")
            self.lbl_vigencia.setText(f"📋 <b>{tr('Regulação & Vigência:')}</b> {tr('Conforme projeto')}")
            self.lbl_confianca.setText(f"⭐ <b>{tr('Modo:')}</b> {tr('Personalizado')}")
            self.btn_open_url.setVisible(False)
            self.lbl_elec_info.setText("")
            self.lbl_regime.setText(tr(
                "💧 <b>Regime de cobrança:</b> defina você mesmo. Se a sua concessionária cobra um "
                "mínimo que já dá direito a alguns m³, lance-o como faixa de R$ 0,00/m³ até esse "
                "volume: abaixo dele economizar água não reduz a conta."
            ))
            self.lbl_estrutura_aviso.setText("")
            self.lbl_estrutura_aviso.setVisible(False)
            self.lbl_disclaimer.setText(tr(
                "💡 <b>Modo Personalizado:</b> As faixas e alíquotas abaixo são editáveis livremente. "
                "Insira os valores com impostos inclusos conforme a fatura do seu projeto."
            ))
            return

        city_name = self.combo_city.currentText().strip()
        data = get_city_data(uf_code, city_name)
        self._current_city_data = data
        if not data:
            self.lbl_tipologia.setText(f"🏠 <b>{tr('Tipologia / Categoria:')}</b> {tr('Residencial (Auditada)')}")
            self.lbl_prestador.setText(f"🏢 <b>{tr('Prestador:')}</b> --")
            self.lbl_vigencia.setText(f"📋 <b>{tr('Regulação & Vigência:')}</b> --")
            self.lbl_confianca.setText(f"⭐ <b>{tr('Confiança:')}</b> --")
            self.btn_open_url.setVisible(False)
            self.lbl_elec_info.setText("")
            return

        prestador = data.get('prestador_saneamento', '--')
        esg_pct = data.get('esgoto_pct', 80.0)
        agencia = data.get('agencia_reguladora', '')
        vigencia = data.get('vigencia_saneamento', '')
        reg_str = f"{agencia} ({vigencia})" if agencia and vigencia else (agencia or vigencia or "--")
        
        conf_grau = data.get('confianca_grau', 'A — alta')
        conf_score = data.get('confianca_score', 95.0)
        
        self.lbl_tipologia.setText(f"🏠 <b>{tr('Tipologia / Categoria:')}</b> {tr('Residencial (Auditada)')}")
        self.lbl_prestador.setText(f"🏢 <b>{tr('Prestador:')}</b> {prestador} &nbsp;•&nbsp; <b>{tr('Esgoto:')}</b> {esg_pct:.0f}%")
        self.lbl_vigencia.setText(f"📋 <b>{tr('Regulação / Vigência:')}</b> {reg_str}")
        self.lbl_confianca.setText(f"⭐ <b>{tr('Confiança:')}</b> {conf_grau} ({conf_score:.0f}/100)")

        # Regime de tarifa minima. O projetista nao precisa do nome do regime:
        # precisa saber se economizar agua reduz a conta, e a partir de que
        # consumo. Num municipio com franquia de 15 m3, uma residencia que
        # consome 12 m3 nao economiza um centavo por instalar cisterna.
        self.lbl_regime.setText(f"💧 <b>{tr('Regime de cobrança:')}</b> {resumo_do_regime(data)}")

        # Estrutura incompleta ou suspeita: escolhivel sim, mas nunca em silencio.
        # A categoria vem primeiro, porque erra a conta inteira e nao um trecho.
        incompativel = incompatibilidade_de_categoria(self.config)
        erros = [a for a in validar_estrutura(data) if a.gravidade == "erro"]
        ressalva = data.get("_ressalva_estrutura", "") or data.get("_ressalva_esgoto", "")
        if incompativel:
            self.lbl_estrutura_aviso.setText(
                f"⚠️ <b>{tr('Categoria tarifária incompatível:')}</b> "
                + incompativel.replace("\n\n", "<br><br>")
            )
            self.lbl_estrutura_aviso.setVisible(True)
        elif erros or ressalva:
            texto = ressalva or "; ".join(a.mensagem for a in erros)
            self.lbl_estrutura_aviso.setText(
                f"⚠️ <b>{tr('Estrutura tarifária a conferir:')}</b> {texto}"
            )
            self.lbl_estrutura_aviso.setVisible(True)
        else:
            self.lbl_estrutura_aviso.setText("")
            self.lbl_estrutura_aviso.setVisible(False)
        
        # Link da Fonte
        url = data.get('fonte_url', '')
        if url and url.startswith("http"):
            self.btn_open_url.setEnabled(True)
            self.btn_open_url.setVisible(True)
            self.btn_open_url.setText(f"🔗 {tr('Abrir Resolução / Fonte Oficial')} ({prestador})")
        else:
            self.btn_open_url.setEnabled(False)
            self.btn_open_url.setVisible(True)
            self.btn_open_url.setText(tr("Fonte oficial não disponível online"))

        # Energia
        dist_e = data.get('distribuidora_energia', '')
        e_kwh = data.get('energia_r_kwh', 0.0)
        if dist_e and e_kwh > 0:
            self.lbl_elec_info.setText(f"({dist_e}: R$ {e_kwh:.4f}/kWh)")
        else:
            self.lbl_elec_info.setText("")

        self.lbl_disclaimer.setText(tr(
            f"⚠️ <b>Aviso de Vigência & Tipologia:</b> Tarifas auditadas para a categoria <b>Residencial</b> com esgoto oficial a <b>{esg_pct:.0f}%</b> (com tributos inclusos). "
            "Para outras tipologias (comercial, industrial, etc.) ou faturas recentes, use 'Personalizado' ou ajuste os valores na tabela."
        ))

    def on_contact_link_clicked(self, link_str: str):
        """Copia o e-mail para a área de transferência e abre o cliente se disponível."""
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtCore import QUrl
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
            tr("O e-mail <b>igorcmvaz@gmail.com</b> foi copiado para a sua área de transferência!<br><br>"
               "Você pode colar diretamente no seu cliente de e-mail para enviar correções ou anexar decretos municipais.")
        )

    def apply_city_tariffs(self):
        uf_code = self.combo_uf.currentData() or ""
        city_data_val = self.combo_city.currentData()
        
        if uf_code == "CUSTOM" or city_data_val == "CUSTOM":
            self.update_city_preview()
            return

        city_name = self.combo_city.currentText().strip()
        cat_val = self.combo_category.currentData() or "residencial"
        from netuno.core.tariffs_database import get_city_tariffs_by_category
        data = get_city_tariffs_by_category(uf_code, city_name, category=cat_val)
        if not data:
            QMessageBox.warning(self, tr("Aviso"), tr("Dados tarifários não encontrados para a cidade selecionada."))
            return

        self._current_city_data = data
        self.update_city_preview()

        # 1. Preenche faixas de água
        faixas = data.get('faixas', [])
        if faixas:
            self.populate_table_from_tariffs(faixas)

        # 2. Preenche esgoto
        esg_pct = data.get('esgoto_pct', 80.0)
        self.radio_esg_var.setChecked(True)
        self.txt_esg_val.setText(f"{esg_pct:.1f}".replace('.', ','))
        self.update_esg_checks()

        # 3. Atualiza energia se selecionado
        if self.chk_update_elec.isChecked() and data.get('energia_r_kwh', 0.0) > 0:
            self.config.elec_tariff = data['energia_r_kwh']

    def on_open_source_url(self):
        if self._current_city_data:
            url_str = self._current_city_data.get('fonte_url', '')
            if url_str and url_str.startswith("http"):
                QDesktopServices.openUrl(QUrl(url_str))

    def populate_table_from_tariffs(self, tariffs):
        prev_blocked = self.table.blockSignals(True)
        self.table.setRowCount(len(tariffs))
        for r, (min_v, max_v, val, is_fix) in enumerate(tariffs):
            if is_fix in (-1, -2):
                vol_str = f"{max_v:.0f}" if max_v > 0 else "0"
                cost_str = tr("Consumo mínimo (fixo)") if is_fix == -2 or (max_v > 0) else tr("Custo fixo")
            else:
                vol_str = f"{max_v:.0f}" if max_v < 900 else f"{min_v:.0f}"
                cost_str = f"{tr('Custo variável')} ({self._sym}/m³)"
            val_str = f"{val:.2f}".replace('.', ',')

            self.table.setItem(r, 1, QTableWidgetItem(vol_str))
            self.table.setItem(r, 2, QTableWidgetItem(cost_str))
            self.table.setItem(r, 3, QTableWidgetItem(val_str))

        self.table.blockSignals(prev_blocked)
        self.update_table_intervals()

    def update_esg_checks(self):
        fix_base = f"{tr('Fixa')} ({self._sym})"
        var_base = tr("Variável (% da conta de água)")
        if self.radio_esg_fix.isChecked():
            self.radio_esg_fix.setText(f"✓ {fix_base}")
            self.radio_esg_var.setText(var_base)
        else:
            self.radio_esg_fix.setText(fix_base)
            self.radio_esg_var.setText(f"✓ {var_base}")

    def on_table_item_changed(self, item):
        if item.column() == 1 or item.column() == 2:
            self.update_table_intervals()

    def update_table_intervals(self):
        if getattr(self, '_updating_intervals', False):
            return
        self._updating_intervals = True
        try:
            n = self.table.rowCount()
            vols = []
            for r in range(n):
                item = self.table.item(r, 1)
                txt = item.text().replace(',', '.').strip() if item else ""
                try:
                    val = float(txt)
                except ValueError:
                    val = 0.0
                vols.append(val)

            prev = 0.0
            for r in range(n):
                item_c = self.table.item(r, 2)
                c_text = item_c.text().lower() if item_c else ""
                is_fix_row = ("fixo" in c_text or tr("fixo").lower() in c_text)

                if n == 1:
                    inter_str = tr("TFDI mensal") if is_fix_row else tr("Qualquer consumo")
                elif is_fix_row:
                    v_fix = vols[r]
                    if v_fix > 0:
                        inter_str = f"{tr('Até')} {v_fix:.0f} m³ ({tr('Mínimo')})" if v_fix == int(v_fix) else f"{tr('Até')} {v_fix:.1f} m³ ({tr('Mínimo')})"
                    else:
                        inter_str = tr("TFDI mensal")
                elif r == 0 or (r == 1 and self.table.item(0, 2) and ("fixo" in self.table.item(0, 2).text().lower() or tr("fixo").lower() in self.table.item(0, 2).text().lower())):
                    v_curr = vols[r]
                    inter_str = f"{tr('Até')} {v_curr:.0f} m³" if v_curr == int(v_curr) else f"{tr('Até')} {v_curr:.1f} m³"
                    prev = v_curr
                elif r == n - 1:
                    inter_str = f"{tr('Acima de')} {prev:.0f} m³" if prev == int(prev) else f"{tr('Acima de')} {prev:.1f} m³"
                else:
                    v_curr = vols[r]
                    p_str = f"{prev:.0f}" if prev == int(prev) else f"{prev:.1f}"
                    c_str = f"{v_curr:.0f}" if v_curr == int(v_curr) else f"{v_curr:.1f}"
                    inter_str = f"{tr('De')} {p_str} {tr('a')} {c_str} m³"
                    prev = v_curr

                item_inter = QTableWidgetItem(inter_str)
                item_inter.setFlags(item_inter.flags() & ~Qt.ItemIsEditable)
                item_inter.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, 0, item_inter)
        finally:
            self._updating_intervals = False

    def on_add_row(self):
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 1, QTableWidgetItem("20"))
        self.table.setItem(r, 2, QTableWidgetItem(f"{tr('Custo variável')} ({self._sym}/m³)"))
        self.table.setItem(r, 3, QTableWidgetItem("5,00"))
        self.update_table_intervals()

    def on_rem_row(self):
        r = self.table.rowCount()
        if r > 1:
            self.table.removeRow(r - 1)
            self.update_table_intervals()

    def on_accept(self):
        try:
            tariffs = []
            prev_max = 0.0
            for r in range(self.table.rowCount()):
                v_str = self.table.item(r, 1).text().replace(',', '.').strip() if self.table.item(r, 1) else "0"
                val_str = self.table.item(r, 3).text().replace(',', '.').strip() if self.table.item(r, 3) else "0"
                c_type_str = self.table.item(r, 2).text().lower() if self.table.item(r, 2) else ""

                v_val = float(v_str) if v_str else 0.0
                rate_val = float(val_str) if val_str else 0.0
                is_fix = -1 if tr("fixo").lower() in c_type_str or "fixo" in c_type_str else 1

                if is_fix == -1:
                    is_fix_type = -2 if v_val > 0 else -1
                    tariffs.append((0.0, v_val, rate_val, is_fix_type))
                    if v_val > 0:
                        prev_max = v_val
                else:
                    min_v = prev_max
                    max_v = v_val if (r < self.table.rowCount() - 1 or v_val > min_v) else 999999.0
                    prev_max = max_v
                    tariffs.append((min_v, max_v, rate_val, 1))

            self.config.water_tariffs = tariffs
            self.config.sewage_mode = 0 if self.radio_esg_fix.isChecked() else 1
            self.config.sewage_rate = float(self.txt_esg_val.text().replace(',', '.'))
            # Ate 5.0.8 estes dois eram zerados aqui, apagando o que o arquivo
            # do projeto ou a linha de comando tivessem declarado.
            def _num(campo, padrao=0.0):
                t = campo.text().strip().replace(".", "").replace(",", ".")
                try:
                    return max(0.0, float(t)) if t else padrao
                except ValueError:
                    return padrao
            self.config.water_tax_fixed = _num(self.txt_tax_fix)
            self.config.water_tax_var = _num(self.txt_tax_var)
            
            # Persist selected city metadata
            if self.combo_uf.currentIndex() >= 0:
                self.config.tariff_city_uf = self.combo_uf.currentData() or self.combo_uf.currentText().split(' - ')[0]
            if self.combo_city.currentIndex() >= 0:
                self.config.tariff_city_name = self.combo_city.currentText().strip()
                
            if self.chk_update_elec.isChecked() and self._current_city_data:
                e_kwh = self._current_city_data.get('energia_r_kwh', 0.0)
                if e_kwh > 0:
                    self.config.elec_tariff = e_kwh

            self.accept()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Verifique os valores preenchidos na tabela de tarifas."))


class DialogWaterEstimates(QDialog):
    """
    Diálogo 1:1 idêntico ao Netuno 4 para Estimativas Iniciais de Consumos e Economias Mensais de Água (Figura 10).
    Calcula consumos mensais individualizados da simulação e contas de água com/sem água de chuva.
    """
    def __init__(self, parent=None, config=None, sim_result=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Estimativas iniciais de consumos e economias mensais de água"))
        adapt_dialog_size(self, target_w=940, target_h=560, min_w=740, min_h=440)
        self.config = config or NetunoConfig()
        self.sim_result = sim_result
        self.init_ui()

    def init_ui(self):
        lay = QVBoxLayout()
        table = QTableWidget()
        cols = [
            tr("Mês"), tr("Consumo pluvial\n(L/dia)"), tr("Consumo potável\n(L/dia)"), 
            tr("Economia pluvial\n(L/mês)"), tr("Conta s/ pluvial\n(R$)"), 
            tr("Conta c/ pluvial\n(R$)"), tr("Economia mensal\n(R$)")
        ]
        table.setColumnCount(len(cols))
        table.setHorizontalHeaderLabels(cols)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setRowCount(14)

        months_pt = [
            tr("Janeiro"), tr("Fevereiro"), tr("Março"), tr("Abril"),
            tr("Maio"), tr("Junho"), tr("Julho"), tr("Agosto"),
            tr("Setembro"), tr("Outubro"), tr("Novembro"), tr("Dezembro")
        ]
        days_in_m_list = [31.0, 28.25, 31.0, 30.0, 31.0, 30.0, 31.0, 31.0, 30.0, 31.0, 30.0, 31.0]

        font_bold = QFont("Segoe UI", 9)
        font_bold.setBold(True)
        
        is_dark = get_current_theme() == "dark"
        green_bg = QColor("#0f5132" if is_dark else "#d1e7dd")
        fg_color = QColor("#ffffff" if is_dark else "#000000")

        import pandas as pd
        df = None
        if self.sim_result and self.sim_result.daily_results:
            dates = pd.date_range(start=getattr(self.config, 'start_date', '01/01/2002'), periods=len(self.sim_result.daily_results), freq='D')
            df = pd.DataFrame({
                'month': dates.month,
                'pluvial': [d.pluvial_consumed_liters for d in self.sim_result.daily_results],
                'potable': [d.potable_consumed_liters for d in self.sim_result.daily_results],
            })

        m_pluv_day = []
        m_pot_day = []
        m_pluv_month = []
        m_bw_list = []
        m_bwth_list = []
        m_sav_list = []

        for r in range(12):
            m_idx = r + 1
            if df is not None:
                m_df = df[df['month'] == m_idx]
                if len(m_df) > 0:
                    p_day = float(m_df['pluvial'].mean())
                    pot_day = float(m_df['potable'].mean())
                else:
                    p_day = self.sim_result.avg_pluvial_consumed_l_day if self.sim_result else 0.0
                    pot_day = self.sim_result.avg_potable_consumed_l_day if self.sim_result else 0.0
            else:
                p_day = self.sim_result.avg_pluvial_consumed_l_day if self.sim_result else 0.0
                pot_day = self.sim_result.avg_potable_consumed_l_day if self.sim_result else 0.0

            tot_day = p_day + pot_day
            days_m = days_in_m_list[r]
            p_month = p_day * days_m

            bw = calculate_water_bill(tot_day * days_m, self.config.water_tariffs, self.config.sewage_mode, self.config.sewage_rate, self.config.water_tax_fixed, self.config.water_tax_var)
            bwth = calculate_water_bill(pot_day * days_m, self.config.water_tariffs, self.config.sewage_mode, self.config.sewage_rate, self.config.water_tax_fixed, self.config.water_tax_var)
            msav = max(0.0, bw - bwth)

            m_pluv_day.append(p_day)
            m_pot_day.append(pot_day)
            m_pluv_month.append(p_month)
            m_bw_list.append(bw)
            m_bwth_list.append(bwth)
            m_sav_list.append(msav)

            table.setItem(r, 0, QTableWidgetItem(months_pt[r]))
            table.setItem(r, 1, QTableWidgetItem(f"{p_day:.1f}".replace('.', ',')))
            table.setItem(r, 2, QTableWidgetItem(f"{pot_day:.1f}".replace('.', ',')))
            table.setItem(r, 3, QTableWidgetItem(f"{p_month:.0f}"))
            table.setItem(r, 4, QTableWidgetItem(f"{bw:.2f}".replace('.', ',')))
            table.setItem(r, 5, QTableWidgetItem(f"{bwth:.2f}".replace('.', ',')))
            table.setItem(r, 6, QTableWidgetItem(f"{msav:.2f}".replace('.', ',')))

        # Linha Média (Linha 12)
        it_m = QTableWidgetItem(tr("Média"))
        it_m.setFont(font_bold)
        it_m.setBackground(green_bg)
        it_m.setForeground(fg_color)
        table.setItem(12, 0, it_m)

        avg_p_day = sum(m_pluv_day) / 12.0
        avg_pot_day = sum(m_pot_day) / 12.0
        avg_p_m = sum(m_pluv_month) / 12.0
        avg_bw = sum(m_bw_list) / 12.0
        avg_bwth = sum(m_bwth_list) / 12.0
        avg_sav = sum(m_sav_list) / 12.0

        vals_med = [
            f"{avg_p_day:.1f}".replace('.', ','),
            f"{avg_pot_day:.1f}".replace('.', ','),
            f"{avg_p_m:.0f}",
            f"{avg_bw:.2f}".replace('.', ','),
            f"{avg_bwth:.2f}".replace('.', ','),
            f"{avg_sav:.2f}".replace('.', ',')
        ]
        for c_idx, val_str in enumerate(vals_med):
            it = QTableWidgetItem(val_str)
            it.setFont(font_bold)
            it.setBackground(green_bg)
            it.setForeground(fg_color)
            table.setItem(12, c_idx + 1, it)

        # Linha Total Ano (Linha 13)
        it_t = QTableWidgetItem(tr("Total ano"))
        it_t.setFont(font_bold)
        it_t.setBackground(green_bg)
        it_t.setForeground(fg_color)
        table.setItem(13, 0, it_t)

        tot_p_m = sum(m_pluv_month)
        tot_bw = sum(m_bw_list)
        tot_bwth = sum(m_bwth_list)
        tot_sav = sum(m_sav_list)

        table.setItem(13, 1, QTableWidgetItem(""))
        table.setItem(13, 2, QTableWidgetItem(""))

        it_p_tot = QTableWidgetItem(f"{tot_p_m:.0f}")
        it_p_tot.setFont(font_bold)
        it_p_tot.setBackground(green_bg)
        it_p_tot.setForeground(fg_color)
        table.setItem(13, 3, it_p_tot)

        it_bw_tot = QTableWidgetItem(f"{tot_bw:.2f}".replace('.', ','))
        it_bw_tot.setFont(font_bold)
        it_bw_tot.setBackground(green_bg)
        it_bw_tot.setForeground(fg_color)
        table.setItem(13, 4, it_bw_tot)

        it_bwth_tot = QTableWidgetItem(f"{tot_bwth:.2f}".replace('.', ','))
        it_bwth_tot.setFont(font_bold)
        it_bwth_tot.setBackground(green_bg)
        it_bwth_tot.setForeground(fg_color)
        table.setItem(13, 5, it_bwth_tot)

        it_sav_tot = QTableWidgetItem(f"{tot_sav:.2f}".replace('.', ','))
        it_sav_tot.setFont(font_bold)
        it_sav_tot.setBackground(green_bg)
        it_sav_tot.setForeground(fg_color)
        table.setItem(13, 6, it_sav_tot)

        lay.addWidget(table)
        btn_close = QPushButton(tr("Fechar"))
        btn_close.clicked.connect(self.accept)
        lay.addWidget(btn_close)
        self.setLayout(lay)


class DialogInitialCosts(QDialog):
    """
    Diálogo de Custos Iniciais de Construção / CAPEX com estimativas inteligentes baseadas
    no volume e material dos reservatórios, tubulações e equipamentos.
    """

    LOWER_TANK_PRICE_TABLE = LOWER_TANK_PRICE_TABLE
    UPPER_TANK_PRICE_TABLE = UPPER_TANK_PRICE_TABLE

    def __init__(self, parent=None, config=None, evaluated_volumes=None):
        super().__init__(parent)
        self.config = config or NetunoConfig()
        _refresh_runtime_constants()
        
        # Get parent currency symbol
        self._sym = "R$"
        if parent and hasattr(parent, 'get_currency_symbol'):
            self._sym = parent.get_currency_symbol()
            
        self.setWindowTitle(f"{tr('🏗️ Investimento Inicial (CAPEX)')} ({self._sym})")
        self.resize(520, 520)
        self._lower_vol = getattr(config, 'econ_lower_tank_vol', config.lower_tank_fixed if config else 2000.0)
        volumes = evaluated_volumes or [self._lower_vol]
        self._lower_volumes = sorted({max(0.0, float(v)) for v in volumes})
        if not self._lower_volumes:
            self._lower_volumes = [max(0.0, float(self._lower_vol))]
        self._upper_vol = getattr(config, 'upper_tank_vol', 500.0)
        self._upper_used = bool(getattr(config, 'upper_tank_used', 1))
        self.init_ui()

    def _get_current_pipes(self):
        def _parse_len(txt, default=0.0):
            if isinstance(txt, str):
                widget = getattr(self, txt, None)
            else:
                widget = txt
            if widget is None:
                return default
            val = widget.text().strip().replace('.', '').replace(',', '.')
            try:
                return max(0.0, float(val))
            except ValueError:
                return default
        if hasattr(self, "txt_pipes") and self.txt_pipes:
            return [
                (p["dn"], _parse_len(self.txt_pipes.get(p["dn"]), self.config.get_pipe_length(p["dn"])))
                for p in COMMERCIAL_PIPES_CAPEX
            ]
        if hasattr(self, "txt_pipe_50"):
            return [
                (50, _parse_len("txt_pipe_50", self.config.get_pipe_length(50))),
                (75, _parse_len("txt_pipe_75", self.config.get_pipe_length(75))),
                (100, _parse_len("txt_pipe_100", self.config.get_pipe_length(100))),
                (150, _parse_len("txt_pipe_150", self.config.get_pipe_length(150))),
            ]
        return getattr(self.config, "pipes_list", None)

    def _estimate_costs(self, lower_volume=None):
        low_mat = self.combo_lower_mat.currentData() if hasattr(self, "combo_lower_mat") else getattr(self.config, "lower_tank_material", "PEAD")
        up_mat = self.combo_upper_mat.currentData() if hasattr(self, "combo_upper_mat") else getattr(self.config, "upper_tank_material", "PEAD")
        pipes = self._get_current_pipes()
        uf = getattr(self.config, "tariff_city_uf", "SC")
        estimates = estimate_preliminary_capex(
            self._lower_vol if lower_volume is None else lower_volume,
            self._upper_vol, self._upper_used,
            self.config.pump_power_kw, self.config.pump_count,
            lower_material=low_mat, upper_material=up_mat,
            pipes=pipes,
            uf=uf
        )
        return estimates['lower'], estimates['upper'], estimates['labor'], estimates['piping'], estimates['accessories']

    def init_ui(self):
        adapt_dialog_size(self, target_w=980, target_h=860, min_w=680, min_h=640)
        self.setMinimumWidth(640)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content_w = QWidget()
        lay = QVBoxLayout(content_w)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)

        is_dark = get_current_theme() == "dark"
        in_use_str = tr("em uso no sistema") if self._upper_used else tr("não utilizado")
        
        positive_volumes = [v for v in self._lower_volumes if v > 0]
        if len(self._lower_volumes) > 1 and positive_volumes:
            range_text = (
                f"<b>{min(positive_volumes):,.0f}–{max(positive_volumes):,.0f} L</b> "
                f"({len(positive_volumes)} {tr('volumes positivos')}"
                + (f" + {tr('referência de 0 L')}" if 0.0 in self._lower_volumes else "")
                + ")"
            )
        else:
            range_text = f"<b>{self._lower_volumes[0]:,.0f} L</b>"

        uf_code = getattr(self.config, 'tariff_city_uf', 'SC')
        city_name = getattr(self.config, 'tariff_city_name', 'Florianópolis')
        f_reg = REGIONAL_FACTORS_BY_UF.get(str(uf_code).upper(), 1.00)
        reg_info = f"<br>▸ {tr('Localidade:')} <b>{city_name} ({uf_code})</b> — {tr('Fator Regional SINAPI/CUB:')} <b>{f_reg:.2f}x</b> ({'+' if f_reg >= 1.0 else ''}{(f_reg - 1.0)*100:.0f}%)" if uf_code != "CUSTOM" else f"<br>▸ {tr('Localidade:')} <b>{tr('Personalizado')}</b> (Fator 1.00x)"

        lbl_info = QLabel(
            f"<b>{tr('Faixa de capacidades avaliadas:')}</b><br>"
            f"▸ {tr('Reservatório inferior:')} {range_text}<br>"
            f"▸ {tr('Reservatório superior:')} <b>{self._upper_vol:,.0f} L</b> (<i>{in_use_str}</i>)"
            f"{reg_info}"
        )
        
        if is_dark:
            lbl_info.setStyleSheet(
                "background-color: #1e3a8a; border: 1px solid #1d4ed8; "
                "border-radius: 6px; padding: 8px; color: #dbeafe;"
            )
        else:
            lbl_info.setStyleSheet(
                "background-color: #f0f9ff; border: 1px solid #7dd3fc; "
                "border-radius: 6px; padding: 8px; color: #0369a1;"
            )
        lbl_info.setWordWrap(True)
        lay.addWidget(lbl_info)

        # Seletores de Material
        gb_mat = QGroupBox(tr("Seleção de Materiais dos Reservatórios"))
        grid_mat = QGridLayout()
        grid_mat.setSpacing(8)

        grid_mat.addWidget(QLabel(tr("Material Cisterna Inferior:")), 0, 0)
        self.combo_lower_mat = QComboBox()
        self.combo_lower_mat.addItem(tr("Polietileno de Alta Densidade (PEAD)"), "PEAD")
        self.combo_lower_mat.addItem(tr("Concreto Armado Moldado in loco"), "CONCRETO")
        self.combo_lower_mat.addItem(tr("Fibra de Vidro (PRFV)"), "PRFV")
        self.combo_lower_mat.addItem(tr("Aço Inoxidável (AISI 304/316)"), "ACO_INOX")
        cur_low = getattr(self.config, "lower_tank_material", "PEAD")
        idx_low = self.combo_lower_mat.findData(cur_low)
        if idx_low >= 0:
            self.combo_lower_mat.setCurrentIndex(idx_low)
        self.combo_lower_mat.currentIndexChanged.connect(self._on_material_changed)
        grid_mat.addWidget(self.combo_lower_mat, 0, 1)

        grid_mat.addWidget(QLabel(tr("Material Reservatório Superior:")), 1, 0)
        self.combo_upper_mat = QComboBox()
        self.combo_upper_mat.addItem(tr("Polietileno de Alta Densidade (PEAD)"), "PEAD")
        self.combo_upper_mat.addItem(tr("Concreto Armado Moldado in loco"), "CONCRETO")
        self.combo_upper_mat.addItem(tr("Fibra de Vidro (PRFV)"), "PRFV")
        self.combo_upper_mat.addItem(tr("Aço Inoxidável (AISI 304/316)"), "ACO_INOX")
        cur_up = getattr(self.config, "upper_tank_material", "PEAD")
        idx_up = self.combo_upper_mat.findData(cur_up)
        if idx_up >= 0:
            self.combo_upper_mat.setCurrentIndex(idx_up)
        self.combo_upper_mat.currentIndexChanged.connect(self._on_material_changed)
        grid_mat.addWidget(self.combo_upper_mat, 1, 1)

        gb_mat.setLayout(grid_mat)
        lay.addWidget(gb_mat)

        # ── REDE DE TUBULAÇÕES (Comprimentos em metros por DN) ──
        gb_pipes = QGroupBox(tr("Comprimentos de Tubulações em PVC (Rede Hidráulica - Todos os Diâmetros Comerciais)"))
        lay_pipes_v = QVBoxLayout(gb_pipes)
        grid_pipes = QGridLayout()
        grid_pipes.setHorizontalSpacing(10)
        grid_pipes.setVerticalSpacing(6)

        self.txt_pipes = {}
        self.lbl_pipe_costs = {}

        half = (len(COMMERCIAL_PIPES_CAPEX) + 1) // 2
        for idx, p in enumerate(COMMERCIAL_PIPES_CAPEX):
            dn = p["dn"]
            col_base = 0 if idx < half else 4
            row_idx = idx if idx < half else (idx - half)

            lbl_name = QLabel(f"{p['label']}:")
            lbl_name.setStyleSheet("font-weight: 500;")
            txt_pipe = QLineEdit(f"{self.config.get_pipe_length(dn):.1f}".replace('.', ','))
            txt_pipe.setMinimumWidth(60)
            txt_pipe.setMaximumWidth(90)
            txt_pipe.textChanged.connect(self._on_pipes_changed)

            lbl_cost = QLabel()
            lbl_cost.setStyleSheet("color: #0284c7; font-size: 10.5px; font-weight: 500;" if not is_dark else "color: #38bdf8; font-size: 10.5px; font-weight: 500;")

            grid_pipes.addWidget(lbl_name, row_idx, col_base + 0)
            grid_pipes.addWidget(txt_pipe, row_idx, col_base + 1)
            grid_pipes.addWidget(lbl_cost, row_idx, col_base + 2)

            self.txt_pipes[dn] = txt_pipe
            self.lbl_pipe_costs[dn] = lbl_cost
            setattr(self, f"txt_pipe_{dn}", txt_pipe)
            setattr(self, f"lbl_cost_{dn}", lbl_cost)

        grid_pipes.setColumnMinimumWidth(3, 16)
        lay_pipes_v.addLayout(grid_pipes)

        self.lbl_pipe_network_total = QLabel()
        self.lbl_pipe_network_total.setStyleSheet(
            "background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 4px; padding: 4px 8px; color: #166534; font-weight: bold; font-size: 11.5px;"
            if not is_dark else
            "background-color: #052e16; border: 1px solid #166534; border-radius: 4px; padding: 4px 8px; color: #86efac; font-weight: bold; font-size: 11.5px;"
        )
        lay_pipes_v.addWidget(self.lbl_pipe_network_total)

        lbl_pipe_guidance = QLabel(
            tr("💡 <b>Custos de Referência SINAPI:</b> Tubulações comerciais de PVC Soldável Água Fria (DN 20 a 110 mm) e Pluvial (DN 100 e 150 mm) com acréscimo normativo de 25% para conexões e registros.<br>Os comprimentos informados aqui são automaticamente sincronizados com o Módulo Ambiental (ACV).")
        )
        lbl_pipe_guidance.setWordWrap(True)
        lbl_pipe_guidance.setStyleSheet("color: #475569; font-size: 10.5px; padding: 2px 0;" if not is_dark else "color: #94a3b8; font-size: 10.5px; padding: 2px 0;")
        lay_pipes_v.addWidget(lbl_pipe_guidance)
        lay.addWidget(gb_pipes)

        gb_variable = QGroupBox(tr("Custo da Cisterna Inferior por Volume Avaliado"))
        lay_variable = QVBoxLayout(gb_variable)
        self.table_lower_costs = QTableWidget()
        self.table_lower_costs.setColumnCount(2)
        self.table_lower_costs.setHorizontalHeaderLabels([
            tr("Volume avaliado (L)"), tr("Custo estimado da cisterna"),
        ])
        self.table_lower_costs.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_lower_costs.verticalHeader().setVisible(False)
        self.table_lower_costs.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_lower_costs.setMaximumHeight(160)
        lay_variable.addWidget(self.table_lower_costs)
        lay.addWidget(gb_variable)

        est_lower, est_upper, est_labor, est_piping, est_acc = self._estimate_costs()
        is_brl = (self._sym == "R$")

        upper_val = f"{self.config.cost_upper_tank:.2f}".replace('.', ',') if self.config.cost_upper_tank > 0 else (f"{est_upper:.2f}".replace('.', ',') if is_brl else "")
        labor_val = f"{self.config.cost_labor:.2f}".replace('.', ',') if self.config.cost_labor > 0 else (f"{est_labor:.2f}".replace('.', ',') if is_brl else "")
        piping_val = f"{self.config.cost_piping:.2f}".replace('.', ',') if self.config.cost_piping > 0 else (f"{est_piping:.2f}".replace('.', ',') if is_brl else "")
        acc_val = f"{self.config.cost_accessories:.2f}".replace('.', ',') if self.config.cost_accessories > 0 else (f"{est_acc:.2f}".replace('.', ',') if is_brl else "")

        grid = QGridLayout()
        grid.setVerticalSpacing(6)
        grid.setHorizontalSpacing(10)

        def add_row(row, label, txt_field, est_val):
            grid.addWidget(QLabel(label), row, 0)
            grid.addWidget(txt_field, row, 1)
            lbl_est = QLabel(f"(est. R$ {est_val:,.0f})".replace(',', 'X').replace('.', ',').replace('X', '.') if is_brl else "")
            lbl_est.setStyleSheet("color: #a1a1aa; font-size: 11px;" if is_dark else "color: #64748b; font-size: 11px;")
            grid.addWidget(lbl_est, row, 2)
            return lbl_est

        self.txt_upper = QLineEdit(upper_val)
        self.lbl_est_upper = add_row(0, f"{tr('Reservatório superior')} ({self._upper_vol:,.0f} L) {self._sym}:", self.txt_upper, est_upper)

        self.txt_labor = QLineEdit(labor_val)
        self.lbl_est_labor = add_row(1, f"{tr('Mão de obra e instalação')} {self._sym}:", self.txt_labor, est_labor)

        self.txt_piping = QLineEdit(piping_val)
        self.lbl_est_piping = add_row(2, f"{tr('Tubulações e filtros')} {self._sym}:", self.txt_piping, est_piping)

        self.txt_accessories = QLineEdit(acc_val)
        self.lbl_est_acc = add_row(3, f"{tr('Acessórios')} {self._sym}:", self.txt_accessories, est_acc)

        lay.addLayout(grid)

        # Label de total dinâmico
        self.lbl_total = QLabel()
        self.lbl_total.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {'#ffffff' if is_dark else '#0f172a'}; "
            f"background-color: {'#27272a' if is_dark else '#f1f5f9'}; border-radius: 6px; padding: 6px;"
        )
        lay.addWidget(self.lbl_total)

        # Botões
        row_btns = QHBoxLayout()
        btn_reset = QPushButton(tr("🔄 Recalcular por Material"))
        btn_reset.setStyleSheet("color: #38bdf8; font-weight: bold;" if is_dark else "color: #0284c7; font-weight: bold;")
        btn_reset.clicked.connect(self._reset_estimates)
        row_btns.addWidget(btn_reset)

        btn_open_db = QPushButton(tr("📁 Base de Custos (JSON)..."))
        btn_open_db.setToolTip(tr("Abre o arquivo JSON com a tabela base de custos e cotações para edição."))
        btn_open_db.clicked.connect(self._open_costs_file)
        row_btns.addWidget(btn_open_db)

        row_btns.addStretch()
        btn_ok = QPushButton(tr("Confirmar"))
        btn_ok.setStyleSheet("font-weight: bold; background-color: #059669; color: white; padding: 6px 18px;")
        btn_ok.setFixedHeight(34)
        btn_ok.clicked.connect(self.on_accept)
        row_btns.addWidget(btn_ok)
        lay.addLayout(row_btns)

        scroll.setWidget(content_w)
        outer_layout.addWidget(scroll)

        # Conecta atualização do total
        for txt in [self.txt_upper, self.txt_labor, self.txt_piping, self.txt_accessories]:
            txt.textChanged.connect(lambda _, w=txt: self._check_highlight(w))
            txt.textChanged.connect(self._update_total)
            self._check_highlight(txt)
        pipe_txts = list(self.txt_pipes.values()) if hasattr(self, "txt_pipes") else [self.txt_pipe_50, self.txt_pipe_75, self.txt_pipe_100, self.txt_pipe_150]
        for txt in pipe_txts:
            txt.textChanged.connect(lambda _, w=txt: self._check_highlight(w))
            self._check_highlight(txt)
        self._on_pipes_changed()
        self._reset_estimates()

    def _on_pipes_changed(self):
        pipes = self._get_current_pipes() or []
        p_dict = {int(d): float(l) for d, l in pipes}
        for p in COMMERCIAL_PIPES_CAPEX:
            dn = p["dn"]
            if hasattr(self, "lbl_pipe_costs") and dn in self.lbl_pipe_costs:
                cost_item = compute_pipe_item_cost(dn, p_dict.get(dn, 0.0), include_fittings=True)
                unit_cost = PIPE_COST_PER_METER.get(dn, 35.0)
                self.lbl_pipe_costs[dn].setText(f"➔ {self._sym} {format_ptbr(cost_item, 2)} ({self._sym} {format_ptbr(unit_cost, 2)}/m + 25%)")

        est_lower, est_upper, est_labor, est_piping, est_acc = self._estimate_costs()
        is_brl = (self._sym == "R$")
        def _fmt_est(v): return f"(est. R$ {v:,.0f})".replace(',', 'X').replace('.', ',').replace('X', '.') if is_brl else ""
        if hasattr(self, "lbl_pipe_network_total"):
            self.lbl_pipe_network_total.setText(f"⚡ {tr('Subtotal Calculado de Tubulações (SINAPI + conexões):')} {self._sym} {format_ptbr(est_piping, 2)}")
        if hasattr(self, "lbl_est_piping"):
            self.lbl_est_piping.setText(_fmt_est(est_piping))
        if hasattr(self, "lbl_est_labor"):
            self.lbl_est_labor.setText(_fmt_est(est_labor))
        if is_brl and hasattr(self, "txt_piping"):
            self.txt_piping.setText(f"{est_piping:.2f}".replace('.', ','))
        self._update_total()

    def _on_material_changed(self):
        est_lower, est_upper, est_labor, est_piping, est_acc = self._estimate_costs()
        is_brl = (self._sym == "R$")
        def _fmt_est(v): return f"(est. R$ {v:,.0f})".replace(',', 'X').replace('.', ',').replace('X', '.') if is_brl else ""
        if hasattr(self, "lbl_est_upper"):
            self.lbl_est_upper.setText(_fmt_est(est_upper))
        if hasattr(self, "lbl_est_labor"):
            self.lbl_est_labor.setText(_fmt_est(est_labor))
        if hasattr(self, "lbl_est_piping"):
            self.lbl_est_piping.setText(_fmt_est(est_piping))
        if hasattr(self, "lbl_est_acc"):
            self.lbl_est_acc.setText(_fmt_est(est_acc))
        self._reset_estimates()

    def _refresh_lower_cost_table(self):
        self.table_lower_costs.setRowCount(len(self._lower_volumes))
        for row, volume in enumerate(self._lower_volumes):
            lower_cost = self._estimate_costs(lower_volume=volume)[0]
            volume_item = QTableWidgetItem(f"{volume:,.0f}".replace(',', '.'))
            cost_item = QTableWidgetItem(f"{self._sym} {format_ptbr(lower_cost, 2)}")
            volume_item.setTextAlignment(Qt.AlignCenter)
            cost_item.setTextAlignment(Qt.AlignCenter)
            self.table_lower_costs.setItem(row, 0, volume_item)
            self.table_lower_costs.setItem(row, 1, cost_item)

    def _check_highlight(self, line_edit):
        val = line_edit.text().strip()
        is_dark = get_current_theme() == "dark"
        try:
            v = float(val.replace('.', '').replace(',', '.'))
            if v >= 0:
                if is_dark:
                    line_edit.setStyleSheet("QLineEdit { background-color: #1c1c1f; border: 1px solid #3f3f46; color: #ffffff; }")
                else:
                    line_edit.setStyleSheet("QLineEdit { background-color: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; }")
                return
        except ValueError:
            pass
        if is_dark:
            line_edit.setStyleSheet("QLineEdit { background-color: #713f12; border: 1.5px solid #eab308; color: #fef9c3; }")
        else:
            line_edit.setStyleSheet("QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }")

    def _update_total(self):
        try:
            fixed_total = 0.0
            for t in [self.txt_upper, self.txt_labor, self.txt_piping, self.txt_accessories]:
                val_str = t.text().strip().replace('.', '').replace(',', '.')
                if val_str:
                    fixed_total += float(val_str)
            totals = [
                0.0 if volume <= 0 else fixed_total + self._estimate_costs(lower_volume=volume)[0]
                for volume in self._lower_volumes
            ]
            if len(totals) > 1:
                positive_totals = [value for value in totals if value > 0] or [0.0]
                min_fmt = format_ptbr(min(positive_totals), 2)
                max_fmt = format_ptbr(max(positive_totals), 2)
                self.lbl_total.setText(
                    f"   💰 {tr('CAPEX estimado na faixa:')} {self._sym} {min_fmt} – {self._sym} {max_fmt}"
                )
            else:
                self.lbl_total.setText(
                    f"   💰 {tr('CAPEX Total Estimado:')} {self._sym} {format_ptbr(totals[0], 2)}"
                )
        except ValueError:
            self.lbl_total.setText(tr("   ⚠️ Verifique os valores inseridos"))

    def _reset_estimates(self):
        est_lower, est_upper, est_labor, est_piping, est_acc = self._estimate_costs()
        is_brl = (self._sym == "R$")
        def _fmt(v): return f"{v:.2f}".replace('.', ',') if is_brl else ""
        self.txt_upper.setText(_fmt(est_upper))
        self.txt_labor.setText(_fmt(est_labor))
        self.txt_piping.setText(_fmt(est_piping))
        self.txt_accessories.setText(_fmt(est_acc))
        self._refresh_lower_cost_table()
        self._update_total()

    def _open_costs_file(self):
        """Abre o arquivo JSON de custos para edição externa ou consulta."""
        if COSTS_FILE_PATH.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(COSTS_FILE_PATH)))
        _refresh_runtime_constants()
        self._reset_estimates()

    def on_accept(self):
        try:
            def _parse_val(txt):
                v_str = txt.text().strip().replace('.', '').replace(',', '.')
                return float(v_str) if v_str else 0.0
            self.config.lower_tank_material = self.combo_lower_mat.currentData()
            self.config.upper_tank_material = self.combo_upper_mat.currentData()
            for p in COMMERCIAL_PIPES_CAPEX:
                dn = p["dn"]
                if hasattr(self, "txt_pipes") and dn in self.txt_pipes:
                    self.config.set_pipe_length(dn, _parse_val(self.txt_pipes[dn]))
            self.config.cost_lower_tank  = self._estimate_costs(lower_volume=self._lower_vol)[0]
            self.config.cost_upper_tank  = _parse_val(self.txt_upper)
            self.config.cost_labor       = _parse_val(self.txt_labor)
            self.config.cost_piping      = _parse_val(self.txt_piping)
            self.config.cost_accessories = _parse_val(self.txt_accessories)
            self.accept()
        except ValueError:
            QMessageBox.critical(
                self, tr("Erro de Validação"),
                tr("Um ou mais valores inseridos não são números válidos.\nUse vírgula como separador decimal (ex: 1.250,00).")
            )


class DialogElectricity(QDialog):
    """
    Diálogo de Parâmetros da Motobomba e Tarifa de Eletricidade.
    Permite seleção de concessionária e tarifa B1 Residencial homologada pela ANEEL
    entre as 652 cidades auditadas ou definição personalizada.
    """
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        
        # Get parent currency symbol
        self._sym = "R$"
        if parent and hasattr(parent, 'get_currency_symbol'):
            self._sym = parent.get_currency_symbol()
            
        self.setWindowTitle(f"{tr('Motobomba e Energia')} ({self._sym})")
        adapt_dialog_size(self, target_w=960, target_h=820, min_w=660, min_h=600)
        self.setMinimumSize(660, 600)
        self.config = config or NetunoConfig()
        self._current_elec_data = None
        self._is_populating_elec_ui = False
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"
        card_bg = "#1e293b" if is_dark else "#f8fafc"
        card_border = "#334155" if is_dark else "#cbd5e1"
        sub_text_color = "#94a3b8" if is_dark else "#64748b"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setSpacing(10)
        lay.setContentsMargins(2, 2, 2, 2)

        # ── BLOCO 1: SELEÇÃO DA TARIFA DE ENERGIA (ANEEL / 652 CIDADES) ──
        gb_elec = QGroupBox(tr("⚡ Tarifa de Eletricidade Residencial B1 (ANEEL / 652 Cidades)"))
        gb_elec.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_elec = QVBoxLayout(gb_elec)
        lay_elec.setSpacing(8)

        lbl_elec_note = QLabel(tr(
            "Selecione o Estado (UF) e o Município para carregar a tarifa homologada ANEEL da distribuidora local (com impostos), ou escolha 'Personalizado':"
        ))
        lbl_elec_note.setWordWrap(True)
        lbl_elec_note.setStyleSheet(f"font-size: 11px; font-weight: normal; color: {sub_text_color};")
        lay_elec.addWidget(lbl_elec_note)

        row_elec_sel = QHBoxLayout()
        row_elec_sel.setSpacing(6)
        row_elec_sel.addWidget(QLabel(f"<b>{tr('UF:')}</b>"))
        self.combo_elec_uf = QComboBox()
        self.combo_elec_uf.setMinimumWidth(110)
        row_elec_sel.addWidget(self.combo_elec_uf)

        row_elec_sel.addWidget(QLabel(f"<b>{tr('Município:')}</b>"))
        self.combo_elec_city = QComboBox()
        self.combo_elec_city.setMinimumWidth(180)
        row_elec_sel.addWidget(self.combo_elec_city, stretch=1)

        self.btn_load_elec_city = QPushButton(tr("📥 Carregar"))
        self.btn_load_elec_city.setMinimumWidth(90)
        self.btn_load_elec_city.setToolTip(tr("Aplica a tarifa de energia oficial da cidade selecionada"))
        self.btn_load_elec_city.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: white;
                font-weight: bold;
                padding: 5px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)
        self.btn_load_elec_city.clicked.connect(self.apply_elec_city)
        row_elec_sel.addWidget(self.btn_load_elec_city)
        lay_elec.addLayout(row_elec_sel)

        # Card de Auditoria Elétrica
        self.card_elec_info = QFrame()
        self.card_elec_info.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
            }}
            QLabel {{
                color: {'#e2e8f0' if is_dark else '#1e293b'};
            }}
        """)
        card_elec_lay = QVBoxLayout(self.card_elec_info)
        card_elec_lay.setContentsMargins(8, 6, 8, 6)
        card_elec_lay.setSpacing(4)

        self.lbl_elec_tipo = QLabel(f"⚡ <b>{tr('Tipologia / Classe:')}</b> {tr('Residencial B1 (Homologada ANEEL)')}")
        self.lbl_elec_tipo.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {text_color};")
        self.lbl_elec_dist = QLabel(f"🏢 <b>{tr('Distribuidora ANEEL:')}</b> --")
        self.lbl_elec_dist.setStyleSheet("font-size: 11px;")
        card_elec_lay.addWidget(self.lbl_elec_tipo)
        card_elec_lay.addWidget(self.lbl_elec_dist)

        # Disclaimer elétrico
        disc_bg = "rgba(245, 158, 11, 0.14)" if is_dark else "#fffbeb"
        disc_border = "#f59e0b" if is_dark else "#fcd34d"
        disc_text = "#fbbf24" if is_dark else "#92400e"
        box_elec_disc = QFrame()
        box_elec_disc.setStyleSheet(f"""
            QFrame {{
                background-color: {disc_bg};
                border: 1px solid {disc_border};
                border-radius: 4px;
            }}
        """)
        lay_ed = QVBoxLayout(box_elec_disc)
        lay_ed.setContentsMargins(6, 4, 6, 4)
        self.lbl_elec_disc = QLabel(tr(
            "📅 <b>Auditoria ANEEL B1:</b> Tarifas homologadas pela ANEEL validadas em <b>27/08/2026</b> para a classe <b>Residencial B1</b> (com tributos). "
            "Atualizações periódicas podem ser necessárias conforme novos processos tarifários da distribuidora. "
            "Para outras classes (comercial, industrial, etc.), selecione 'Personalizado' e insira a tarifa contratada."
        ))
        self.lbl_elec_disc.setWordWrap(True)
        self.lbl_elec_disc.setStyleSheet(f"font-size: 10px; color: {disc_text}; background: transparent; border: none;")
        lay_ed.addWidget(self.lbl_elec_disc)
        card_elec_lay.addWidget(box_elec_disc)

        lay_elec.addWidget(self.card_elec_info)
        lay.addWidget(gb_elec)

        # ── BLOCO 2: PARÂMETROS DA MOTOBOMBA ──
        gb_pump = QGroupBox(tr("⚙️ Parâmetros da Motobomba"))
        gb_pump.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {text_color}; }}")
        lay_p = QVBoxLayout(gb_pump)
        lay_p.setSpacing(6)

        btn_wizard = QPushButton(tr("🧙‍♂️ Assistente de Dimensionamento de Motobomba & Tubulações..."))
        btn_wizard.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 6px 12px;
                border-radius: 4px;
                margin-bottom: 4px;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)
        btn_wizard.clicked.connect(self._open_pump_wizard)
        lay_p.addWidget(btn_wizard)

        lay_p.addWidget(QLabel(tr("Potência unitária:")))
        row_p = QHBoxLayout()
        self.txt_power = QLineEdit(f"{(self.config.pump_power_kw / 0.735499):.2f}".replace('.', ','))
        self.combo_power_unit = QComboBox()
        self.combo_power_unit.addItems(["CV", "W", "kW", "HP"])
        row_p.addWidget(self.txt_power)
        row_p.addWidget(self.combo_power_unit)
        lay_p.addLayout(row_p)

        lay_p.addWidget(QLabel(tr("Rendimento (%):")))
        self.txt_eff = QLineEdit(f"{self.config.pump_efficiency:.1f}".replace('.', ','))
        self.txt_eff.setToolTip(tr(
            "Rendimento da BOMBA, isto é, da parte hidráulica. Não inclui o motor: a potência de placa é a mecânica no eixo, e o rendimento do motor é campo à parte."))
        lay_p.addWidget(self.txt_eff)

        # O rendimento do motor separa a energia de eixo da energia faturada.
        lay_p.addWidget(QLabel(tr("Rendimento do motor (%, em branco usa a NBR 17094-2):")))
        _mot = float(getattr(self.config, 'pump_motor_efficiency', 0.0) or 0.0)
        self.txt_motor_eff = QLineEdit(
            f"{_mot:.1f}".replace('.', ',') if _mot > 0 else "")
        self.txt_motor_eff.setPlaceholderText(tr("Ex: 60,5 para meio CV"))
        self.txt_motor_eff.setToolTip(tr(
            "A potência de placa é a potência mecânica no eixo, e a ABNT NBR 17094-2 manda marcar o rendimento na placa como grandeza separada. Em branco, o programa adota a Tabela 13 da norma para a potência escolhida: 60,5% em meio CV, 69,3% em um CV."))
        lay_p.addWidget(self.txt_motor_eff)

        lay_p.addWidget(QLabel(tr("Vazão nominal (litros/hora):")))
        self.txt_flow = QLineEdit(f"{self.config.pump_flow_rate:.0f}".replace('.', ','))
        lay_p.addWidget(self.txt_flow)

        lay_p.addWidget(QLabel(tr("Tempo de partida (segundos):")))
        self.txt_startup = QLineEdit(f"{(self.config.pump_startup_time_h * 3600.0):.0f}")
        lay_p.addWidget(self.txt_startup)

        is_brl = (self._sym == "R$")
        unit_cost_str = f"{self.config.pump_unit_cost:.2f}".replace('.', ',') if (self.config.pump_unit_cost > 0 or is_brl) else ""
        elec_tariff_str = f"{self.config.elec_tariff:.4f}".replace('.', ',') if (self.config.elec_tariff > 0 or is_brl) else ""

        lay_p.addWidget(QLabel(f"{tr('Custo Unitário da Motobomba')} ({self._sym}):"))
        self.txt_unit_cost = QLineEdit(unit_cost_str)
        lay_p.addWidget(self.txt_unit_cost)

        lay_p.addWidget(QLabel(f"<b>{tr('Tarifa de energia elétrica')} ({self._sym}/kWh):</b>"))
        self.txt_elec_tariff = QLineEdit(elec_tariff_str)
        lay_p.addWidget(self.txt_elec_tariff)

        # Impostos da conta de energia. No Brasil a fatura carrega ICMS mais
        # PIS/COFINS, entre 25% e 30% em boa parte dos estados, e o bombeamento
        # e o unico custo operacional recorrente do sistema.
        _e_var = float(getattr(self.config, "elec_tax_var", 0.0) or 0.0)
        _e_fix = float(getattr(self.config, "elec_tax_fixed", 0.0) or 0.0)
        lay_p.addWidget(QLabel(tr("Imposto variável sobre a conta de energia (%):")))
        self.txt_elec_tax_var = QLineEdit(f"{_e_var:.2f}".replace(".", ","))
        lay_p.addWidget(self.txt_elec_tax_var)
        lay_p.addWidget(QLabel(tr("Imposto fixo sobre a conta de energia (R$/mês):")))
        self.txt_elec_tax_fix = QLineEdit(f"{_e_fix:.2f}".replace(".", ","))
        lay_p.addWidget(self.txt_elec_tax_fix)

        self.chk_backup_pump = QCheckBox(tr("Considerar motobomba de reserva"))
        # O ternario anterior devolvia True nos dois ramos, de modo que a caixa abria
        # sempre marcada e o OK devolvia pump_count = 2, apagando a escolha de bomba
        # unica. A contagem de bombas entra na ACV e no CAPEX.
        self.chk_backup_pump.setChecked(int(getattr(self.config, 'pump_count', 2)) >= 2)
        lay_p.addWidget(self.chk_backup_pump)

        lay.addWidget(gb_pump)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Botões de Ação Fixos no Rodapé
        row_actions = QHBoxLayout()
        btn_cancel = QPushButton(tr("Cancelar"))
        btn_cancel.setFixedHeight(32)
        btn_cancel.clicked.connect(self.reject)

        self.btn_ok = QPushButton(tr("Concluir e Aplicar"))
        self.btn_ok.setFixedHeight(32)
        self.btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                font-weight: bold;
                padding: 6px 18px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #047857; }
        """)
        self.btn_ok.clicked.connect(self.on_accept)

        row_actions.addStretch()
        row_actions.addWidget(btn_cancel)
        row_actions.addWidget(self.btn_ok)
        main_layout.addLayout(row_actions)

        # Inicializa seletor elétrico
        self.init_elec_city_ui()

    def init_elec_city_ui(self):
        self._is_populating_elec_ui = True
        try:
            self.combo_elec_uf.clear()
            self.combo_elec_uf.addItem(tr("⚙️ Personalizado"), "CUSTOM")
            ufs = get_available_ufs()
            for uf_code, state_name in ufs:
                self.combo_elec_uf.addItem(f"{uf_code} - {state_name}", uf_code)

            saved_uf = getattr(self.config, 'elec_city_uf', getattr(self.config, 'tariff_city_uf', 'SC'))
            saved_city = getattr(self.config, 'elec_city_name', getattr(self.config, 'tariff_city_name', 'Florianópolis'))

            uf_idx = -1
            for i in range(self.combo_elec_uf.count()):
                if self.combo_elec_uf.itemData(i) == saved_uf:
                    uf_idx = i
                    break
            if uf_idx >= 0:
                self.combo_elec_uf.setCurrentIndex(uf_idx)
            else:
                self.combo_elec_uf.setCurrentIndex(1 if self.combo_elec_uf.count() > 1 else 0)

            self.populate_elec_cities_for_current_uf(select_city=saved_city)
        finally:
            self._is_populating_elec_ui = False

        self.combo_elec_uf.currentIndexChanged.connect(self.on_elec_uf_changed)
        self.combo_elec_city.currentIndexChanged.connect(self.on_elec_city_changed)
        self.update_elec_city_preview()
        
        city_val = self.combo_elec_city.currentData()
        if city_val and city_val != "CUSTOM":
            self.apply_elec_city()
        elif self.config.elec_tariff > 0:
            self.txt_elec_tariff.setText(f"{self.config.elec_tariff:.4f}".replace('.', ','))

    def populate_elec_cities_for_current_uf(self, select_city=None):
        uf_code = self.combo_elec_uf.currentData() or "CUSTOM"
        
        prev_blocked = self.combo_elec_city.blockSignals(True)
        self.combo_elec_city.clear()
        
        if uf_code == "CUSTOM":
            self.combo_elec_city.addItem(tr("⚙️ Personalizado (Definir tarifa manualmente)"), "CUSTOM")
            self.combo_elec_city.setEnabled(False)
        else:
            self.combo_elec_city.setEnabled(True)
            self.combo_elec_city.addItem(tr("⚙️ Personalizado (Definir tarifa manualmente)"), "CUSTOM")
            cities = get_cities_by_uf(uf_code)
            for c in cities:
                self.combo_elec_city.addItem(c, c)
            
            if select_city and select_city not in ("CUSTOM", "Personalizado"):
                idx = self.combo_elec_city.findData(select_city)
                if idx >= 0:
                    self.combo_elec_city.setCurrentIndex(idx)
                else:
                    self.combo_elec_city.setCurrentIndex(1 if self.combo_elec_city.count() > 1 else 0)
            elif select_city in ("CUSTOM", "Personalizado"):
                self.combo_elec_city.setCurrentIndex(0)
            elif self.combo_elec_city.count() > 1:
                self.combo_elec_city.setCurrentIndex(1)
            else:
                self.combo_elec_city.setCurrentIndex(0)
            
        self.combo_elec_city.blockSignals(prev_blocked)

    def on_elec_uf_changed(self):
        if self._is_populating_elec_ui:
            return
        self.populate_elec_cities_for_current_uf()
        self.update_elec_city_preview()
        city_val = self.combo_elec_city.currentData()
        if city_val and city_val != "CUSTOM":
            self.apply_elec_city()

    def on_elec_city_changed(self):
        if self._is_populating_elec_ui:
            return
        self.update_elec_city_preview()
        city_val = self.combo_elec_city.currentData()
        if city_val and city_val != "CUSTOM":
            self.apply_elec_city()

    def update_elec_city_preview(self):
        uf_code = self.combo_elec_uf.currentData() or ""
        city_data_val = self.combo_elec_city.currentData()
        is_custom = (uf_code == "CUSTOM" or city_data_val == "CUSTOM")

        if is_custom:
            self._current_elec_data = None
            self.lbl_elec_tipo.setText(f"⚡ <b>{tr('Tipologia / Classe:')}</b> {tr('Residencial (Personalizada)')}")
            self.lbl_elec_dist.setText(f"🏢 <b>{tr('Distribuidora:')}</b> {tr('Definido pelo usuário')}")
            self.lbl_elec_disc.setText(tr("💡 <b>Modo Personalizado:</b> Insira o valor da tarifa de energia elétrica (R$/kWh) desejado diretamente no campo abaixo."))
            return

        city_name = self.combo_elec_city.currentText().strip()
        data = get_city_data(uf_code, city_name)
        self._current_elec_data = data
        if not data:
            self.lbl_elec_tipo.setText(f"⚡ <b>{tr('Tipologia / Classe:')}</b> {tr('Residencial B1 (Homologada ANEEL)')}")
            self.lbl_elec_dist.setText(f"🏢 <b>{tr('Distribuidora ANEEL:')}</b> --")
            return

        dist_e = data.get('distribuidora_energia', '--')
        e_kwh = data.get('energia_r_kwh', 0.0)
        self.lbl_elec_tipo.setText(f"⚡ <b>{tr('Tipologia / Classe:')}</b> {tr('Residencial B1 (Homologada ANEEL)')}")
        self.lbl_elec_dist.setText(f"🏢 <b>{tr('Distribuidora ANEEL:')}</b> {dist_e} (R$ {e_kwh:.4f}/kWh)")
        self.lbl_elec_disc.setText(tr(
            "⚠️ <b>Aviso de Tipologia:</b> Tarifas auditadas para a classe <b>Residencial B1</b> (com tributos). "
            "Para outras classes (comercial, industrial, etc.), selecione 'Personalizado' e insira a tarifa contratada."
        ))

    def apply_elec_city(self):
        uf_code = self.combo_elec_uf.currentData() or ""
        city_data_val = self.combo_elec_city.currentData()

        if uf_code == "CUSTOM" or city_data_val == "CUSTOM":
            self.update_elec_city_preview()
            return

        city_name = self.combo_elec_city.currentText().strip()
        data = get_city_data(uf_code, city_name)
        if not data:
            QMessageBox.warning(self, tr("Aviso"), tr("Dados tarifários de eletricidade não encontrados para a cidade selecionada."))
            return

        self._current_elec_data = data
        self.update_elec_city_preview()

        e_kwh = data.get('energia_r_kwh', 0.0)
        if e_kwh > 0:
            self.txt_elec_tariff.setText(f"{e_kwh:.4f}".replace('.', ','))

    def on_accept(self):
        try:
            def _parse_val(txt):
                v_str = txt.text().strip().replace('.', '').replace(',', '.')
                return float(v_str) if v_str else 0.0
            p_val = float(self.txt_power.text().replace(',', '.'))
            unit = self.combo_power_unit.currentText()
            if unit == "CV":
                p_kw = p_val * 0.735499
            elif unit == "HP":
                p_kw = p_val * 0.7457
            elif unit == "W":
                p_kw = p_val / 1000.0
            else:
                p_kw = p_val

            self.config.pump_power_kw = p_kw
            self.config.pump_efficiency = float(self.txt_eff.text().replace(',', '.'))
            _mot_txt = self.txt_motor_eff.text().strip().replace(',', '.')
            try:
                self.config.pump_motor_efficiency = max(0.0, min(100.0, float(_mot_txt))) \
                    if _mot_txt else 0.0
            except ValueError:
                self.config.pump_motor_efficiency = 0.0
            self.config.pump_flow_rate = float(self.txt_flow.text().replace(',', '.'))
            self.config.pump_startup_time_h = float(self.txt_startup.text().replace(',', '.')) / 3600.0
            self.config.pump_unit_cost = _parse_val(self.txt_unit_cost)
            self.config.elec_tariff = _parse_val(self.txt_elec_tariff)
            self.config.elec_tax_fixed = max(0.0, _parse_val(self.txt_elec_tax_fix))
            self.config.elec_tax_var = max(0.0, _parse_val(self.txt_elec_tax_var))
            self.config.pump_count = 2 if self.chk_backup_pump.isChecked() else 1
            
            # Persiste seleção de cidade da eletricidade
            uf_code = self.combo_elec_uf.currentData() or ""
            city_code = self.combo_elec_city.currentData() or ""
            if uf_code == "CUSTOM" or city_code == "CUSTOM":
                self.config.elec_city_uf = "CUSTOM"
                self.config.elec_city_name = "Personalizado"
            else:
                self.config.elec_city_uf = uf_code
                self.config.elec_city_name = self.combo_elec_city.currentText().strip()

            self.accept()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Insira valores numéricos válidos para os parâmetros da motobomba."))

    def _open_pump_wizard(self):
        from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog
        up_vol = getattr(self.config, 'upper_tank_vol', 500.0) or 500.0
        dlg = PumpSelectionWizardDialog(upper_tank_vol=up_vol, parent=self)
        if dlg.exec():
            p = dlg.selected_pump_data
            if p:
                self.txt_power.setText(f"{p['cv']:.2f}".replace('.', ','))
                self.combo_power_unit.setCurrentText("CV")
                self.txt_flow.setText(f"{p['flow_lh']:.0f}".replace('.', ','))
                self.txt_eff.setText(f"{p['efficiency']:.1f}".replace('.', ','))
                self.txt_unit_cost.setText(f"{p['cost']:.2f}".replace('.', ','))
                if hasattr(self.config, "update_pump_pipes") and "suction_dn" in p and "recalque_dn" in p:
                    self.config.update_pump_pipes(
                        p["suction_dn"], p["recalque_dn"],
                        p.get("suction_len", 5.0), p.get("recalque_len", 20.0)
                    )
                    if hasattr(self, "txt_pipes"):
                        for dn_pipe, txt_p in self.txt_pipes.items():
                            txt_p.setText(f"{self.config.get_pipe_length(dn_pipe):.1f}".replace('.', ','))
                    self._on_pipes_changed()



# Alias para retrocompatibilidade
DialogMotobomba = DialogElectricity


class DialogOtherOpCosts(QDialog):
    """
    Diálogo 1:1 idêntico ao Netuno 4 para Outros Custos Operacionais (Figura 13/15).
    """
    def __init__(self, parent=None, op_costs=None):
        super().__init__(parent)
        
        # Get parent currency symbol
        self._sym = "R$"
        if parent and hasattr(parent, 'get_currency_symbol'):
            self._sym = parent.get_currency_symbol()
            
        self.setWindowTitle(f"{tr('Outros custos operacionais')} ({self._sym})")
        adapt_dialog_size(self, target_w=720, target_h=720, min_w=560, min_h=620)
        self.setMinimumHeight(620)
        self.op_costs = list(op_costs) if op_costs else []
        if not self.op_costs:
            from netuno.core.cost_estimates import default_maintenance_items
            self.op_costs = default_maintenance_items(upper_used=True)
        self.init_ui()

    def init_ui(self):
        lay = QVBoxLayout()
        lay.setSpacing(6)

        lay.addWidget(QLabel(tr("Nome do custo operacional")))
        self.txt_name = QLineEdit(tr("Manutenção periódica"))
        lay.addWidget(self.txt_name)

        lay.addWidget(QLabel(tr("Periodicidade (meses)")))
        self.txt_period = QLineEdit("12")
        lay.addWidget(self.txt_period)

        gb_type = QGroupBox(tr("Tipo de custo"))
        gb_lay = QVBoxLayout()
        self.radio_fix = QRadioButton()
        self.radio_var = QRadioButton()
        self.radio_fix.setChecked(True)
        gb_lay.addWidget(self.radio_fix)
        gb_lay.addWidget(self.radio_var)
        gb_type.setLayout(gb_lay)
        lay.addWidget(gb_type)

        is_brl = (self._sym == "R$")
        linear_val = "200,00" if is_brl else ""

        lay.addWidget(QLabel(f"{tr('Coeficiente linear')} ({self._sym})"))
        self.txt_linear = QLineEdit(linear_val)
        lay.addWidget(self.txt_linear)

        lay.addWidget(QLabel(f"{tr('Coeficiente angular')} ({self._sym}/m³)"))
        self.txt_angular = QLineEdit("0,00")
        lay.addWidget(self.txt_angular)

        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"

        self.setStyleSheet(f"""
            QRadioButton {{ padding: 3px; }}
            QRadioButton:checked {{ font-weight: bold; color: {text_color}; }}
        """)

        self.radio_fix.toggled.connect(self.update_type_checks)
        self.radio_var.toggled.connect(self.update_type_checks)
        self.update_type_checks()

        lay_btns = QHBoxLayout()
        self.btn_add = QPushButton(tr("Adicionar custo"))
        self.btn_add.clicked.connect(self.on_add)
        self.btn_rem = QPushButton(tr("Excluir item selecionado"))
        self.btn_rem.clicked.connect(self.on_remove)
        self.btn_restore = QPushButton(tr("🔄 Restaurar 3 Manutenções de Referência"))
        self.btn_restore.clicked.connect(self.on_restore_defaults)
        lay_btns.addWidget(self.btn_add)
        lay_btns.addWidget(self.btn_rem)
        lay_btns.addWidget(self.btn_restore)
        lay.addLayout(lay_btns)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([tr("Nome"), tr("Período"), f"{tr('Fixo')} ({self._sym})", f"{tr('Var')} ({self._sym}/m³)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setMinimumHeight(155)
        self.refresh_table()
        lay.addWidget(self.table, stretch=1)

        self.btn_close = QPushButton(tr("Concluir"))
        self.btn_close.clicked.connect(self.accept)
        lay.addWidget(self.btn_close)

        self.setLayout(lay)

    def on_restore_defaults(self):
        from netuno.core.cost_estimates import default_maintenance_items
        self.op_costs = default_maintenance_items(upper_used=True)
        self.refresh_table()

    def on_remove(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0 and curr_row < len(self.op_costs):
            self.op_costs.pop(curr_row)
            self.refresh_table()
        elif self.op_costs:
            self.op_costs.pop()
            self.refresh_table()

    def update_type_checks(self):
        fix_base = tr("Fixo")
        var_base = tr("Variável (consumo de água pluvial)")
        if self.radio_fix.isChecked():
            self.radio_fix.setText(f"✓ {fix_base}")
            self.radio_var.setText(var_base)
        else:
            self.radio_fix.setText(fix_base)
            self.radio_var.setText(f"✓ {var_base}")

    def refresh_table(self):
        self.table.setRowCount(len(self.op_costs))
        for r, item in enumerate(self.op_costs):
            name, period, fix_c, var_c = item
            self.table.setItem(r, 0, QTableWidgetItem(str(name)))
            self.table.setItem(r, 1, QTableWidgetItem(f"{period}m"))
            self.table.setItem(r, 2, QTableWidgetItem(f"{fix_c:.2f}".replace('.', ',')))
            self.table.setItem(r, 3, QTableWidgetItem(f"{var_c:.2f}".replace('.', ',')))

    def on_add(self):
        try:
            name = self.txt_name.text().strip() or tr("Custo Operacional")
            period = int(self.txt_period.text())
            fix_c = float(self.txt_linear.text().replace(',', '.'))
            var_c = float(self.txt_angular.text().replace(',', '.')) if self.radio_var.isChecked() else 0.0
            self.op_costs.append((name, period, fix_c, var_c))
            self.refresh_table()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Verifique os valores preenchidos."))


class DialogCashFlow(QDialog):
    """
    Diálogo 1:1 idêntico ao Netuno 4 para Economias e Custos Mensais / Fluxo de Caixa (Figura 16).
    """
    def __init__(self, parent=None, econ_res=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Economias e custos mensais (Fluxo de Caixa)"))
        adapt_dialog_size(self, target_w=1040, target_h=640, min_w=800, min_h=480)
        self.econ_res = econ_res
        self.init_ui()

    def init_ui(self):
        lay = QVBoxLayout()
        lay.setSpacing(8)

        gb_view = QGroupBox(tr("Formato dos dados"))
        gb_lay = QHBoxLayout()
        self.radio_simple = QRadioButton()
        self.radio_detailed = QRadioButton()
        self.radio_simple.setChecked(True)
        gb_lay.addWidget(self.radio_simple)
        gb_lay.addWidget(self.radio_detailed)
        gb_view.setLayout(gb_lay)
        lay.addWidget(gb_view)
        self.table = QTableWidget()
        lay.addWidget(self.table)

        is_dark = get_current_theme() == "dark"
        text_color = "#38bdf8" if is_dark else "#0369a1"

        self.setStyleSheet(f"""
            QRadioButton {{ padding: 3px; }}
            QRadioButton:checked {{ font-weight: bold; color: {text_color}; }}
        """)

        self.radio_simple.toggled.connect(self.on_view_toggled)
        self.radio_detailed.toggled.connect(self.on_view_toggled)

        btn_close = QPushButton(tr("Fechar"))
        btn_close.clicked.connect(self.accept)
        lay.addWidget(btn_close)

        self.setLayout(lay)
        self.on_view_toggled()

    def on_view_toggled(self):
        simple_base = tr("Dados simplificados")
        detailed_base = tr("Dados detalhados")
        if self.radio_simple.isChecked():
            self.radio_simple.setText(f"✓ {simple_base}")
            self.radio_detailed.setText(detailed_base)
        else:
            self.radio_simple.setText(simple_base)
            self.radio_detailed.setText(f"✓ {detailed_base}")
        self.refresh_table()

    def refresh_table(self):
        if not self.econ_res or not self.econ_res.monthly_cash_flows:
            return

        is_detailed = self.radio_detailed.isChecked()

        if is_detailed:
            cols = [
                tr("Mês"), tr("Ano"), tr("Conta s/ Pluvial (R$)"), tr("Conta c/ Pluvial (R$)"), 
                tr("Economia Água (R$)"), tr("Custo Bomba (R$)"), tr("Outros Custos (R$)"), tr("Economia Líquida (R$)"), tr("Acumulado Descontado (R$)")
            ]
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setRowCount(len(self.econ_res.monthly_cash_flows))

            for r, item in enumerate(self.econ_res.monthly_cash_flows):
                self.table.setItem(r, 0, QTableWidgetItem(str(item.month)))
                self.table.setItem(r, 1, QTableWidgetItem(str(item.year)))
                self.table.setItem(r, 2, QTableWidgetItem(f"{item.water_bill_without_pluvial:.2f}".replace('.', ',')))
                self.table.setItem(r, 3, QTableWidgetItem(f"{item.water_bill_with_pluvial:.2f}".replace('.', ',')))
                self.table.setItem(r, 4, QTableWidgetItem(f"{item.water_savings:.2f}".replace('.', ',')))
                self.table.setItem(r, 5, QTableWidgetItem(f"{item.pump_cost:.2f}".replace('.', ',')))
                self.table.setItem(r, 6, QTableWidgetItem(f"{item.om_cost:.2f}".replace('.', ',')))
                self.table.setItem(r, 7, QTableWidgetItem(f"{item.net_savings:.2f}".replace('.', ',')))
                self.table.setItem(r, 8, QTableWidgetItem(f"{item.cumulative_discounted:.2f}".replace('.', ',')))
        else:
            cols = [tr("Mês"), tr("Ano"), tr("Investimento / Custos (R$)"), tr("Economia Líquida (R$)"), tr("Acumulado Descontado (R$)")]
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setRowCount(len(self.econ_res.monthly_cash_flows) + 1)

            # Mês 0: Investimento Inicial
            self.table.setItem(0, 0, QTableWidgetItem("0"))
            self.table.setItem(0, 1, QTableWidgetItem("0"))
            self.table.setItem(0, 2, QTableWidgetItem(f"{self.econ_res.capex_total:.2f}".replace('.', ',')))
            self.table.setItem(0, 3, QTableWidgetItem(f"{-self.econ_res.capex_total:.2f}".replace('.', ',')))
            self.table.setItem(0, 4, QTableWidgetItem(f"{-self.econ_res.capex_total:.2f}".replace('.', ',')))

            for r, item in enumerate(self.econ_res.monthly_cash_flows):
                self.table.setItem(r + 1, 0, QTableWidgetItem(str(item.month)))
                self.table.setItem(r + 1, 1, QTableWidgetItem(str(item.year)))
                self.table.setItem(r + 1, 2, QTableWidgetItem(f"{(item.pump_cost + item.om_cost):.2f}".replace('.', ',')))
                self.table.setItem(r + 1, 3, QTableWidgetItem(f"{item.net_savings:.2f}".replace('.', ',')))
                self.table.setItem(r + 1, 4, QTableWidgetItem(f"{item.cumulative_discounted:.2f}".replace('.', ',')))


class DialogEconomicAnalysis(QDialog):
    """
    Janela Principal da Análise Econômica 1:1 idêntica ao Netuno 4 (Figura 6).
    """
    def __init__(self, parent=None, config=None, sim_result=None, optimal_vol=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Análise econômica"))
        adapt_dialog_size(self, target_w=820, target_h=680, min_w=600, min_h=520)

        self.config = config or NetunoConfig()
        self.sim_result = sim_result
        self.optimal_vol = optimal_vol
        self.last_econ_res = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # 1. GroupBox "Volume do reservatório inferior"
        gb_vol = QGroupBox(tr("Volume do reservatório inferior"))
        lay_vol = QHBoxLayout()
        vol_current = self.config.lower_tank_fixed if self.config.lower_tank_fixed > 0 else 2000.0
        self.lbl_vol = QLabel(f"{tr('Volume do reservatório inferior:')} <b>{vol_current:.0f} {tr('litros')}</b>")
        btn_mod_vol = QPushButton(tr("Modificar volume..."))
        btn_mod_vol.clicked.connect(self.on_modify_volume)
        lay_vol.addWidget(self.lbl_vol)
        lay_vol.addStretch()
        lay_vol.addWidget(btn_mod_vol)
        gb_vol.setLayout(lay_vol)
        main_layout.addWidget(gb_vol)

        # 2. Botão "Tarifas de água e esgoto..."
        self.btn_tariffs = QPushButton(tr("Tarifas de água e esgoto..."))
        self.btn_tariffs.setFixedHeight(30)
        self.btn_tariffs.clicked.connect(self.on_open_tariffs)
        main_layout.addWidget(self.btn_tariffs)

        # 3. Botão "Estimativas de consumo de água..."
        self.btn_water_est = QPushButton(tr("Estimativas de consumo de água..."))
        self.btn_water_est.setFixedHeight(30)
        self.btn_water_est.clicked.connect(self.on_open_water_estimates)
        main_layout.addWidget(self.btn_water_est)

        # 4. Botão "Custos iniciais..."
        self.btn_init_costs = QPushButton(tr("Custos iniciais..."))
        self.btn_init_costs.setFixedHeight(30)
        self.btn_init_costs.clicked.connect(self.on_open_initial_costs)
        main_layout.addWidget(self.btn_init_costs)

        # 5. GroupBox "Custos operacionais"
        gb_opex = QGroupBox(tr("Custos operacionais"))
        lay_opex = QHBoxLayout()
        self.btn_motobomba = QPushButton(tr("Motobomba..."))
        self.btn_motobomba.clicked.connect(self.on_open_motobomba)
        self.btn_other_op = QPushButton(tr("Manutenção / Tratamento da água / Outros..."))
        self.btn_other_op.clicked.connect(self.on_open_other_op)
        lay_opex.addWidget(self.btn_motobomba)
        lay_opex.addWidget(self.btn_other_op)
        gb_opex.setLayout(lay_opex)
        main_layout.addWidget(gb_opex)

        # 6. GroupBox "Parâmetros econômicos"
        gb_params = QGroupBox(tr("Parâmetros econômicos"))
        grid_p = QGridLayout()
        grid_p.setSpacing(6)

        grid_p.addWidget(QLabel(tr("Período de análise (anos):")), 0, 0)
        self.txt_years = QLineEdit(str(self.config.analysis_period_years))
        grid_p.addWidget(self.txt_years, 0, 1)

        grid_p.addWidget(QLabel(tr("Inflação (% ao mês):")), 1, 0)
        self.txt_inflation = QLineEdit(f"{self.config.inflation:.2f}".replace('.', ','))
        grid_p.addWidget(self.txt_inflation, 1, 1)

        grid_p.addWidget(QLabel(tr("Período de reajuste (meses):")), 2, 0)
        self.txt_escalation = QLineEdit("12")
        grid_p.addWidget(self.txt_escalation, 2, 1)

        grid_p.addWidget(QLabel(tr("Taxa mínima de atratividade (% ao mês):")), 3, 0)
        self.txt_tma = QLineEdit(f"{self.config.tma:.2f}".replace('.', ','))
        grid_p.addWidget(self.txt_tma, 3, 1)

        grid_p.addWidget(QLabel(tr("Mês de instalação:")), 4, 0)
        self.txt_start_m = QLineEdit("1")
        grid_p.addWidget(self.txt_start_m, 4, 1)

        gb_params.setLayout(grid_p)
        main_layout.addWidget(gb_params)

        # 7. Botão "Calcular"
        self.btn_calc = QPushButton(tr("Calcular"))
        self.btn_calc.setFixedHeight(34)
        self.btn_calc.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; font-size: 10pt; border-radius: 4px;")
        self.btn_calc.clicked.connect(self.run_economic_calc)
        main_layout.addWidget(self.btn_calc)

        # 8. Quadro de Resultados (Figura 6)
        res_layout = QVBoxLayout()
        res_layout.setSpacing(4)

        font_res = QFont("Segoe UI", 9)
        font_res.setBold(True)

        self.lbl_vpl = QLabel(tr("Valor presente líquido: --"))
        self.lbl_vpl.setFont(font_res)

        self.lbl_payback = QLabel(tr("Tempo de retorno do investimento: --"))
        self.lbl_payback.setFont(font_res)

        self.lbl_tir = QLabel(tr("Taxa interna de retorno: --"))
        self.lbl_tir.setFont(font_res)

        res_layout.addWidget(self.lbl_vpl)
        res_layout.addWidget(self.lbl_payback)
        res_layout.addWidget(self.lbl_tir)
        main_layout.addLayout(res_layout)

        # 9. Botão "Economias e custos mensais"
        self.btn_cashflow = QPushButton(tr("Economias e custos mensais..."))
        self.btn_cashflow.setEnabled(False)
        self.btn_cashflow.clicked.connect(self.on_show_cashflow)
        main_layout.addWidget(self.btn_cashflow)

        self.setLayout(main_layout)

        # Executa um cálculo inicial
        self.run_economic_calc()

    def on_modify_volume(self):
        vol_curr = self.config.lower_tank_fixed if self.config.lower_tank_fixed > 0 else 2000.0
        dlg = DialogLowerTankVol(self, current_vol=vol_curr, optimal_vol=self.optimal_vol)
        if dlg.exec():
            self.config.lower_tank_fixed = dlg.vol
            self.lbl_vol.setText(f"{tr('Volume do reservatório inferior:')} <b>{dlg.vol:.0f} {tr('litros')}</b>")
            self.run_economic_calc()

    def on_open_tariffs(self):
        dlg = DialogTariffs(self, config=self.config)
        if dlg.exec():
            self.run_economic_calc()

    def on_open_water_estimates(self):
        dlg = DialogWaterEstimates(self, config=self.config, sim_result=self.sim_result)
        dlg.exec()

    def on_open_initial_costs(self):
        dlg = DialogInitialCosts(self, config=self.config)
        if dlg.exec():
            self.run_economic_calc()

    def on_open_motobomba(self):
        dlg = DialogMotobomba(self, config=self.config)
        if dlg.exec():
            self.run_economic_calc()

    def on_open_other_op(self):
        dlg = DialogOtherOpCosts(self, op_costs=self.config.op_costs)
        if dlg.exec():
            self.config.op_costs = dlg.op_costs
            self.run_economic_calc()

    def run_economic_calc(self):
        if not self.sim_result:
            return

        try:
            self.config.analysis_period_years = int(self.txt_years.text())
            self.config.inflation = float(self.txt_inflation.text().replace(',', '.'))
            self.config.tma = float(self.txt_tma.text().replace(',', '.'))
            self.config.tariff_escalation = float(self.txt_escalation.text().replace(',', '.'))

            self.last_econ_res = run_economic_analysis(self.config, self.sim_result)

            vpl = self.last_econ_res.vpl
            vpl_color = "#16a34a" if vpl >= 0 else "#dc2626"
            self.lbl_vpl.setText(f"{tr('Valor presente líquido:')} R$ {format_ptbr(vpl, 2)}")
            self.lbl_vpl.setStyleSheet(f"color: {vpl_color};")

            pb_yrs = self.last_econ_res.payback_years
            if pb_yrs:
                self.lbl_payback.setText(f"{tr('Tempo de retorno do investimento:')} {math.floor(pb_yrs)} {tr('anos e')} {self.last_econ_res.payback_months % 12} {tr('meses')}")
            else:
                self.lbl_payback.setText(f"{tr('Tempo de retorno do investimento:')} {tr('Não retorna no período de análise')}")

            tir_a = self.last_econ_res.tir_annual_pct
            self.lbl_tir.setText(f"{tr('Taxa interna de retorno:')} {format_ptbr(tir_a, 2)}% {tr('ao ano')} ({format_ptbr(self.last_econ_res.tir_monthly_pct, 2)}% {tr('ao mês')})")

            self.btn_cashflow.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, tr("Erro no Cálculo"), f"{tr('Verifique os parâmetros econômicos')}:\n{str(e)}")

    def on_show_cashflow(self):
        if not self.last_econ_res:
            return
        dlg = DialogCashFlow(self, econ_res=self.last_econ_res)
        dlg.exec()
