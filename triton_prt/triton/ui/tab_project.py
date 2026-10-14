"""
Etapa 1: Configuração do Projeto, Série Climatológica de Chuva & Tarifas (Triton).
Permite selecionar:
1. 🇧🇷 Base de dados CLIMBra (652 Cidades - CMIP6 com 19 Modelos GCMs e Cenários Histórico/SSP2-4.5/SSP5-8.5).
2. 📁 Importar Arquivo CSV em formato Triton (arquivo diário simples).
Suporta recorte temporal por intervalo de datas e sincronização automática/inteligente com as tarifas municipais auditadas.
"""

import os
from datetime import datetime, timedelta
import numpy as np

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, 
    QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, 
    QTabWidget, QFrame, QComboBox, QScrollArea, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QFont

from triton.core.parser import load_precipitation, parse_float, format_ptbr
from triton.core.calculator import IndicesCalculator
from triton.core.tariffs_database import (
    esgoto_do_municipio, get_available_ufs, get_cities_by_uf, get_city_data, procedencia_tarifaria, rotulo_do_esgoto,
)
from triton.core.climate_database import (
    CLIMATE_MODELS, CLIMATE_SCENARIOS, load_national_climate_series, get_climate_file_path,
    RECORTES_SUGERIDOS, ANOS_MINIMOS_RECOMENDADOS,
    get_available_climate_cities
)
from triton.ui.translation import tr, get_current_theme
from triton.ui.date_picker import DatePickerLineEdit
from triton.ui.charts import PrcptotAnnualChart, SdiiVsR95pChart, CddCwdAnnualChart, SeasonalPrecipChart
from triton.core.hydrology_defaults import LAMINA_DE_DESCARTE_PADRAO_MM


class ClimateKpiCard(QFrame):
    """Card visual moderno para destacar um indicador climatológico médio."""
    def __init__(self, title, subtitle="", border_color="#0284c7", parent=None):
        super().__init__(parent)
        self.border_color = border_color
        is_dark = get_current_theme() == "dark"
        surface = "#27272a" if is_dark else "#ffffff"
        border = "#3f3f46" if is_dark else "#e2e8f0"
        text = "#e4e4e7" if is_dark else "#475569"
        muted = "#a1a1aa" if is_dark else "#64748b"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {surface};
                border: 1px solid {border};
                border-left: 5px solid {border_color};
                border-radius: 6px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(2)

        self.lbl_title = QLabel(tr(title))
        self.lbl_title.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {text};")
        
        self.lbl_val = QLabel("--")
        self.lbl_val.setStyleSheet(f"font-size: 17px; font-weight: bold; color: {border_color}; margin-top: 2px; margin-bottom: 2px;")
        
        self.lbl_sub = QLabel(tr(subtitle))
        self.lbl_sub.setWordWrap(True)
        self.lbl_sub.setStyleSheet(f"font-size: 10px; color: {muted};")

        lay.addWidget(self.lbl_title)
        lay.addWidget(self.lbl_val)
        lay.addWidget(self.lbl_sub)

    def set_value(self, val_str):
        self.lbl_val.setText(val_str)


class TabProject(QWidget):
    project_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.precip_data = None
        self.precip_file_path = ""
        self._is_populating = False
        self._tariff_is_customized = False
        self.climate_indices_df = None
        self.init_ui()
        self.clear_climate_cards_and_tables()
        self._abrir_sem_base_climatica()

    #: Série distribuída com o programa, usada quando a base CLIMBra não está
    #: instalada (o instalador não a inclui: ela é copiada à parte).
    SERIE_DE_EXEMPLO = "Florianopolis1.csv"

    def _abrir_sem_base_climatica(self):
        """Sem a base CLIMBra, abre a série de exemplo em vez de uma Etapa 1 vazia.

        A base das 652 cidades é distribuída separadamente. Sem ela, a janela
        abria sem chuva nenhuma, e todas as etapas seguintes ficavam sem dados.
        """
        from triton.core.edition import usa_dados_do_brasil
        # A base nacional da edição: a CLIMBra na Brasil, a E-OBS na Portugal. Na
        # International não há nenhuma, ainda que a CLIMBra esteja na pasta (rodando do
        # código-fonte): o botão da base fica oculto, e a etapa abria com o painel e a
        # série de Florianópolis da CLIMBra carregados.
        tem_base = (usa_dados_do_brasil() and bool(get_available_climate_cities())) or self._base_portugal
        if tem_base:
            return
        if usa_dados_do_brasil():
            if self.precip_data is not None:
                return
        elif self.rb_source_national.isChecked():
            # A série que a montagem da etapa leu da CLIMBra não vale fora da Brasil.
            self.precip_data = None
            self.precip_file_path = ""
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        exemplo = os.path.join(base, "data", "rainfall", self.SERIE_DE_EXEMPLO)
        if os.path.isfile(exemplo) or not usa_dados_do_brasil():
            self.rb_source_custom.setChecked(True)
        if not os.path.isfile(exemplo):
            return
        self.load_rain_file(exemplo)
        # O aviso vai no painel de arquivo, o que fica visível neste modo.
        aviso = tr(
            "Base climática CLIMBra indisponível nesta edição: aberta a série de exemplo de Florianópolis. "
            "Carregue a série do seu projeto; as 652 cidades vêm embutidas na Edição Brasil."
        ) if usa_dados_do_brasil() else tr(
            "Aberta a série de exemplo do tutorial do manual (Florianópolis, Brasil). "
            "Carregue a série diária de chuva do local do seu projeto."
        )
        self.lbl_stats.setText(self.lbl_stats.text() + "<br/>ℹ️ " + aviso)

    def clear_climate_cards_and_tables(self):
        self.card_prcptot.set_value("-")
        self.card_r95p.set_value("-")
        self.card_rx1day.set_value("-")
        self.card_rx5day.set_value("-")
        self.card_sdii.set_value("-")
        self.card_r20mm.set_value("-")
        self.card_cdd.set_value("-")
        self.card_cwd.set_value("-")
        self.card_saz.set_value("-")
        self.lbl_stats.setText(f"{tr('Registros')}: 0 {tr('dias')} | {tr('Precipitação Média Anual')}: - mm | {tr('Máximo Diário')}: - mm")
        self.table_indices.setRowCount(0)
        self.table_preview.setRowCount(0)

    def init_ui(self):
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(40, 34, 40, 40)
        layout.setSpacing(16)

        is_dark = get_current_theme() == "dark"
        heading_color = "#48d5b7" if is_dark else "#087f6b"
        text_color = "#f4f4f5" if is_dark else "#1e293b"
        muted_color = "#a1a1aa" if is_dark else "#64748b"
        card_bg = "#27272a" if is_dark else "#f8fafc"
        card_border = "#3f3f46" if is_dark else "#cbd5e1"

        # Cabeçalho da Etapa
        lbl_eyebrow = QLabel(tr("ETAPA 1"))
        lbl_eyebrow.setStyleSheet("font-size: 10px; font-weight: 800; color: #087f6b; letter-spacing: 1px;")
        layout.addWidget(lbl_eyebrow)
        lbl_title = QLabel(tr("Projeto e série de precipitação"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        layout.addWidget(lbl_title)

        from triton.core.edition import usa_dados_do_brasil
        lbl_desc = QLabel(tr(
            "Selecione uma das 652 cidades brasileiras da Base de dados CLIMBra (CMIP6 com modelos GCMs e projeções climáticas) "
            "ou importe um arquivo CSV próprio. Defina o intervalo de análise, first flush e consulte os 9 indicadores pluviométricos."
        ) if usa_dados_do_brasil() else tr(
            "Importe a série diária de chuva do local do projeto em arquivo CSV. Defina o intervalo de análise, "
            "first flush e consulte os 9 indicadores pluviométricos."
        ))
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet(f"color: {muted_color}; font-size: 12px; margin-bottom: 2px;")
        layout.addWidget(lbl_desc)

        # ── GroupBox 1: FONTE DOS DADOS DE PRECIPITAÇÃO ──
        gb_rain = QGroupBox(tr("Série Climatológica de Precipitação Diária"))
        gb_rain.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_rain = QVBoxLayout()
        lay_rain.setSpacing(10)

        # Alternador de Modo: Base Nacional vs Arquivo Triton
        row_modes = QHBoxLayout()
        self.btn_group_source = QButtonGroup(self)
        
        self.rb_source_national = QRadioButton(tr("🇧🇷 Base de dados CLIMBra (652 Cidades - CMIP6)"))
        self.rb_source_national.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.rb_source_national.setChecked(True)
        self.btn_group_source.addButton(self.rb_source_national, 0)
        row_modes.addWidget(self.rb_source_national)
        # A base CLIMBra cobre só cidades brasileiras e não vai na Internacional; na Portugal, o
        # mesmo painel serve a base E-OBS por concelho (triton/core/base_climatica_portugal.py).
        from triton.core import base_climatica_portugal as _pt
        from triton.core.edition import usa_dados_de_portugal
        self._base_portugal = usa_dados_de_portugal() and _pt.disponivel()
        if self._base_portugal:
            self.rb_source_national.setText(tr("🇵🇹 Base E-OBS por concelho (precipitação observada, 1950–2025)"))
        self.rb_source_national.setVisible(usa_dados_do_brasil() or self._base_portugal)

        self.rb_source_custom = QRadioButton(tr("📁 Importar Arquivo CSV em Formato Triton"))
        self.rb_source_custom.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.rb_source_custom.setToolTip(
            tr("O formato Triton é um arquivo CSV simples em que há somente os dados de precipitação em milímetros, e cada linha representa um dia diferente consecutivo.")
        )
        self.btn_group_source.addButton(self.rb_source_custom, 1)
        row_modes.addWidget(self.rb_source_custom)
        row_modes.addStretch()
        lay_rain.addLayout(row_modes)

        # ── PAINEL A: BASE DE DADOS CLIMBRA ──
        self.panel_national = QFrame()
        self.panel_national.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 6px; padding: 6px; }}")
        lay_pnat = QVBoxLayout(self.panel_national)
        lay_pnat.setSpacing(8)

        grid_nat = QGridLayout()
        grid_nat.setSpacing(8)

        # Linha 0: Localização
        self.lbl_climate_uf = QLabel(f"<b>{tr('Estado (UF):')}</b>")
        grid_nat.addWidget(self.lbl_climate_uf, 0, 0)
        self.combo_climate_uf = QComboBox()
        self.combo_climate_uf.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.combo_tariff_uf = self.combo_climate_uf  # Alias para compatibilidade
        grid_nat.addWidget(self.combo_climate_uf, 0, 1)

        self.lbl_climate_city = QLabel(f"<b>{tr('Município (652 Cidades):')}</b>")
        grid_nat.addWidget(self.lbl_climate_city, 0, 2)
        self.combo_climate_city = QComboBox()
        self.combo_climate_city.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.combo_tariff_city = self.combo_climate_city  # Alias para compatibilidade
        grid_nat.addWidget(self.combo_climate_city, 0, 3)

        # Linha 1: Modelo GCM e Cenário
        grid_nat.addWidget(QLabel(f"<b>{tr('Modelo Climático (GCM):')}</b>"), 1, 0)
        self.combo_climate_model = QComboBox()
        for m in CLIMATE_MODELS:
            self.combo_climate_model.addItem(m, m)
        self.combo_climate_model.setCurrentText("INM-CM4")
        grid_nat.addWidget(self.combo_climate_model, 1, 1)

        grid_nat.addWidget(QLabel(f"<b>{tr('Simulação / Cenário:')}</b>"), 1, 2)
        self.combo_climate_scenario = QComboBox()
        for k, sc_data in CLIMATE_SCENARIOS.items():
            self.combo_climate_scenario.addItem(tr(sc_data["label"]), k)
        grid_nat.addWidget(self.combo_climate_scenario, 1, 3)

        # Linha 2: Recorte Temporal
        grid_nat.addWidget(QLabel(f"<b>{tr('Data / Ano Inicial:')}</b>"), 2, 0)
        self.txt_start_date = DatePickerLineEdit("01/01/1980", default_preset_date="01/01/1980")
        self.txt_start_date.textChanged.connect(self.on_start_date_changed)
        grid_nat.addWidget(self.txt_start_date, 2, 1)

        grid_nat.addWidget(QLabel(f"<b>{tr('Data / Ano Final:')}</b>"), 2, 2)
        row_end = QHBoxLayout()
        self.txt_end_date = DatePickerLineEdit("31/12/2013", default_preset_date="31/12/2013")
        row_end.addWidget(self.txt_end_date, stretch=1)

        self.btn_apply_date_filter = QPushButton(tr("⚡ Aplicar Recorte"))
        self.btn_apply_date_filter.setProperty("primary", True)
        self.btn_apply_date_filter.clicked.connect(self.on_apply_date_filter)
        row_end.addWidget(self.btn_apply_date_filter)
        grid_nat.addLayout(row_end, 2, 3)

        # Linha 3: atalhos de recorte. O recorte continua livre nas datas acima.
        grid_nat.addWidget(QLabel(f"<b>{tr('Atalho de recorte:')}</b>"), 3, 0)
        self.combo_recorte = QComboBox()
        self.combo_recorte.setToolTip(tr(
            "Preenche as datas com um período de trinta anos, a duração das normais "
            "climatológicas. As datas continuam editáveis."))
        self.combo_recorte.activated.connect(self.on_recorte_sugerido)
        grid_nat.addWidget(self.combo_recorte, 3, 1, 1, 3)

        lay_pnat.addLayout(grid_nat)

        # Banner informativo do recorte
        self.lbl_date_range_info = QLabel()
        self.lbl_date_range_info.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {'#93c5fd' if is_dark else '#0369a1'}; padding: 4px;")
        lay_pnat.addWidget(self.lbl_date_range_info)

        lay_rain.addWidget(self.panel_national)

        # ── PAINEL B: IMPORTAÇÃO DE ARQUIVO MANUAL ──
        self.panel_custom = QFrame()
        self.panel_custom.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 6px; padding: 6px; }}")
        lay_pcust = QVBoxLayout(self.panel_custom)
        lay_pcust.setSpacing(6)

        row_file = QHBoxLayout()
        self.txt_file_path = QLineEdit(tr("Nenhum arquivo de chuva selecionado — Clique ao lado para carregar"))
        self.txt_file_path.setReadOnly(True)
        self.btn_browse = QPushButton(tr("📁 Selecionar Arquivo CSV..."))
        self.btn_browse.setProperty("primary", True)
        self.btn_browse.clicked.connect(self.on_browse_file)
        row_file.addWidget(self.txt_file_path)
        row_file.addWidget(self.btn_browse)
        lay_pcust.addLayout(row_file)

        row_custom_date = QHBoxLayout()
        row_custom_date.addWidget(QLabel(f"<b>{tr('Data Inicial da Série (CSV):')}</b>"))
        self.txt_custom_start_date = DatePickerLineEdit("01/01/1980", default_preset_date="01/01/1980")
        self.txt_custom_start_date.textChanged.connect(self.on_custom_start_date_changed)
        row_custom_date.addWidget(self.txt_custom_start_date, stretch=1)
        row_custom_date.addStretch(2)
        lay_pcust.addLayout(row_custom_date)

        self.panel_custom.hide()
        lay_rain.addWidget(self.panel_custom)

        gb_rain.setLayout(lay_rain)
        layout.addWidget(gb_rain)

        # ── GroupBox 2: MUNICÍPIO DE REFERÊNCIA & ESTRUTURA TARIFÁRIA ──
        gb_tariffs = QGroupBox(tr("📍 Município de Referência & Estrutura Tarifária (Saneamento & Energia)"))
        self.gb_tariffs = gb_tariffs
        gb_tariffs.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_tariffs = QVBoxLayout()
        lay_tariffs.setSpacing(8)

        # Card de informações tarifárias com status
        self.card_tariff_info = QFrame()
        self.card_tariff_info.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        lay_card = QVBoxLayout(self.card_tariff_info)
        lay_card.setContentsMargins(10, 8, 10, 8)
        lay_card.setSpacing(5)

        row_tinfo1 = QHBoxLayout()
        self.lbl_t_prestador = QLabel(f"🏢 <b>{tr('Saneamento:')}</b> --")
        self.lbl_t_prestador.setStyleSheet(f"font-size: 11.5px; color: {text_color}; background-color: transparent;")
        self.lbl_t_elec = QLabel(f"⚡ <b>{tr('Eletricidade (ANEEL B1):')}</b> --")
        self.lbl_t_elec.setStyleSheet(f"font-size: 11.5px; color: {text_color}; background-color: transparent;")
        row_tinfo1.addWidget(self.lbl_t_prestador, stretch=1)
        row_tinfo1.addWidget(self.lbl_t_elec, stretch=1)
        lay_card.addLayout(row_tinfo1)

        row_tinfo2 = QHBoxLayout()
        self.lbl_t_reg = QLabel(f"📋 <b>{tr('Regulação / Vigência:')}</b> --")
        self.lbl_t_reg.setStyleSheet(f"font-size: 11px; color: {muted_color}; background-color: transparent;")
        self.lbl_tariff_status = QLabel(tr("🟢 Tarifas Oficiais do Catálogo Auditado"))
        self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #10b981; background-color: transparent;")
        row_tinfo2.addWidget(self.lbl_t_reg, stretch=1)
        row_tinfo2.addWidget(self.lbl_tariff_status)
        lay_card.addLayout(row_tinfo2)

        self.lbl_t_audit = QLabel(tr("📅 <b>Auditoria Tarifária:</b> Valores auditados e validados em <b>27/08/2026</b> (atualizações periódicas podem ser necessárias conforme novos reajustes vigentes)."))
        self.lbl_t_audit.setWordWrap(True)
        self.lbl_t_audit.setStyleSheet(f"font-size: 10.5px; color: {'#93c5fd' if is_dark else '#0369a1'}; background-color: transparent; padding-top: 2px;")
        lay_card.addWidget(self.lbl_t_audit)

        # Botões de edição e restauração de tarifas
        row_tbtns = QHBoxLayout()
        self.btn_open_tariffs = QPushButton(tr("⚙️ Editar / Detalhar Tarifas da Cidade..."))
        self.btn_open_tariffs.setStyleSheet(
            f"font-size: 11px; font-weight: bold; background-color: {'#3f3f46' if is_dark else '#e2e8f0'}; color: {text_color}; padding: 4px 10px; border-radius: 4px;"
        )
        self.btn_open_tariffs.clicked.connect(self.on_open_tariffs_dialog)
        row_tbtns.addWidget(self.btn_open_tariffs)

        self.btn_restore_tariffs = QPushButton(tr("🔄 Restaurar Tarifas Oficiais da Cidade"))
        self.btn_restore_tariffs.setStyleSheet("font-size: 11px; font-weight: bold; color: #0284c7; padding: 4px 10px;")
        self.btn_restore_tariffs.clicked.connect(self.on_restore_official_tariffs)
        row_tbtns.addWidget(self.btn_restore_tariffs)
        row_tbtns.addStretch()
        lay_card.addLayout(row_tbtns)

        lay_tariffs.addWidget(self.card_tariff_info)
        gb_tariffs.setLayout(lay_tariffs)
        layout.addWidget(gb_tariffs)
        # Município de referência e tarifas auditadas: no Brasil, o catálogo; na Portugal, os
        # tarifários transcritos (triton/core/tarifarios_portugal.py), sem energia nem auditoria
        # brasileiras. Na Internacional, tarifa e energia são digitadas nos diálogos econômicos.
        from triton.core.edition import usa_dados_de_portugal
        self._tarifas_portugal = usa_dados_de_portugal()
        gb_tariffs.setVisible(usa_dados_do_brasil() or self._tarifas_portugal)
        if self._tarifas_portugal:
            gb_tariffs.setTitle(tr("📍 Concelho de referência & tarifário (água, saneamento e resíduos)"))
            self.lbl_t_elec.setVisible(False)
            self.lbl_t_audit.setVisible(False)
            self.btn_open_tariffs.setText(tr("⚙️ Editar / Detalhar Tarifas da Cidade..."))
            self.btn_restore_tariffs.setText(tr("🔄 Repor o tarifário transcrito do concelho"))

        # ── GroupBox 3: PARÂMETROS DE DESCARTE INICIAL (FIRST FLUSH) ──
        gb_params = QGroupBox(tr("Parâmetros do Projeto & Regra de Descarte Inicial (First Flush)"))
        gb_params.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        grid_p = QGridLayout()
        grid_p.setSpacing(10)

        grid_p.addWidget(QLabel(tr("Descarte do Escoamento Inicial (mm):")), 0, 0)
        # O campo abre vazio e em amarelo, para pedir a lâmina medida na própria
        # cobertura. Quem não declarar nada recebe a da ABNT NBR 15527:2019 — o
        # mesmo número do exemplo, e o mesmo que o motor assume.
        self.txt_discard = QLineEdit("")
        # Texto inteiro, e não concatenado: a tradução é por frase. Um teste
        # confere que o exemplo é a lâmina da norma.
        self.txt_discard.setPlaceholderText(tr("Ex: 2,0"))
        self.txt_discard.textChanged.connect(self.on_discard_changed)
        grid_p.addWidget(self.txt_discard, 0, 1)

        grid_p.addWidget(QLabel(tr("Abordagem de Descarte Inicial:")), 0, 2)
        
        row_mode = QHBoxLayout()
        self.combo_discard_mode = QComboBox()
        self.combo_discard_mode.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.combo_discard_mode.setStyleSheet(f"font-weight: bold; color: {'#ffffff' if is_dark else '#0284c7'}; padding: 3px 6px;")
        self.combo_discard_mode.addItem(tr("🌧️ Descartado de TODOS os eventos de chuva"), 1)
        self.combo_discard_mode.addItem(tr("☀️ Descartado do 1º evento após estiagem (1 dia sem chuva)"), 2)
        self.combo_discard_mode.addItem(tr("📅 Descartado a cada X dias de intervalo..."), 3)
        self.combo_discard_mode.currentIndexChanged.connect(self.on_discard_mode_changed)

        self.txt_discard_days = QLineEdit("")
        self.txt_discard_days.setFixedWidth(50)
        self.txt_discard_days.setPlaceholderText("7")
        self.txt_discard_days.hide()
        self.lbl_discard_days = QLabel(tr("dias"))
        self.lbl_discard_days.hide()
        self.txt_discard_days.textChanged.connect(self.on_discard_days_changed)

        row_mode.addWidget(self.combo_discard_mode, stretch=2)
        row_mode.addWidget(self.txt_discard_days)
        row_mode.addWidget(self.lbl_discard_days)
        grid_p.addLayout(row_mode, 0, 3)

        gb_params.setLayout(grid_p)
        layout.addWidget(gb_params)

        # ── GroupBox 4: INDICADORES CLIMATOLÓGICOS MÉDIOS DA SÉRIE TEMPORAL ──
        gb_preview = QGroupBox(tr("📊 Indicadores Climatológicos Médios da Série Temporal (Triton)"))
        gb_preview.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_prev = QVBoxLayout()
        lay_prev.setSpacing(10)

        # 9 Cards de Indicadores Médios (Grid 3x3)
        grid_cards = QGridLayout()
        grid_cards.setSpacing(8)

        self.card_prcptot = ClimateKpiCard("PRCPTOT Médio Anual", "Precipitação total média anual (mm/ano)", "#0284c7")
        self.card_r95p    = ClimateKpiCard("R95p Médio Anual", "Chuva acumulada em dias muito úmidos (>P95) (mm)", "#059669")
        self.card_rx1day  = ClimateKpiCard("RX1day Médio", "Precipitação máxima diária média anual (mm)", "#0ea5e9")
        self.card_rx5day  = ClimateKpiCard("RX5day Médio", "Máxima precipitação acumulada em 5 dias (mm)", "#2563eb")
        self.card_sdii    = ClimateKpiCard("SDII Médio Anual", "Intensidade diária de chuva (mm/dia úmido)", "#d97706")
        self.card_r20mm   = ClimateKpiCard("R20mm Médio", "Dias no ano com chuva diária ≥ 20 mm (dias/ano)", "#7c3aed")
        self.card_cdd     = ClimateKpiCard("CDD Médio (Estiagem)", "Máximo de dias secos consecutivos (<1mm) (dias)", "#dc2626")
        self.card_cwd     = ClimateKpiCard("CWD Médio (Chuvosos)", "Máximo de dias chuvosos consecutivos (≥1mm) (dias)", "#059669")
        self.card_saz     = ClimateKpiCard("Sazonalidade da Chuva", "Índice de Concentração de Walsh e Lawler", "#ea580c")

        cards_list = [
            (self.card_prcptot, 0, 0), (self.card_r95p, 0, 1), (self.card_rx1day, 0, 2),
            (self.card_rx5day, 1, 0),  (self.card_sdii, 1, 1), (self.card_r20mm, 1, 2),
            (self.card_cdd, 2, 0),     (self.card_cwd, 2, 1),  (self.card_saz, 2, 2)
        ]
        for card, r, c in cards_list:
            grid_cards.addWidget(card, r, c)
        lay_prev.addLayout(grid_cards)

        # Linha de Resumo Geral
        self.lbl_stats = QLabel(f"{tr('Registros')}: 0 {tr('dias')} | {tr('Precipitação Média Anual')}: - mm | {tr('Máximo Diário')}: - mm")
        self.lbl_stats.setStyleSheet(f"font-weight: bold; color: {heading_color}; padding-left: 2px;")
        self.lbl_stats.setWordWrap(True)
        lay_prev.addWidget(self.lbl_stats)

        # Abas Inferiores: Gráficos, Tabela Anual e Amostra Diária
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {'#3f3f46' if is_dark else '#e2e8f0'};
                background-color: {'#18181b' if is_dark else '#ffffff'};
                border-radius: 6px;
            }}
        """)

        # Sub-aba 1: Gráficos Climatológicos
        w_charts = QWidget()
        lay_ch = QVBoxLayout(w_charts)
        lay_ch.setContentsMargins(5, 5, 5, 5)

        self.tab_charts_sub = QTabWidget()
        self.chart_prcptot = PrcptotAnnualChart()
        self.chart_sdii_r95p = SdiiVsR95pChart()
        self.chart_cdd_cwd = CddCwdAnnualChart()
        self.chart_seasonal = SeasonalPrecipChart()

        self.tab_charts_sub.addTab(self.chart_prcptot, tr("🌧️ Precipitação Total Anual (PRCPTOT)"))
        self.tab_charts_sub.addTab(self.chart_sdii_r95p, tr("⚡ Intensidade (SDII) & Extremos (R95p)"))
        self.tab_charts_sub.addTab(self.chart_cdd_cwd, tr("☀️ Estiagens (CDD) vs Dias Chuvosos (CWD)"))
        self.tab_charts_sub.addTab(self.chart_seasonal, tr("📅 Ciclo Sazonal Médio Mensal"))
        lay_ch.addWidget(self.tab_charts_sub)
        self.tab_widget.addTab(w_charts, tr("📊 Gráficos Climatológicos"))

        # Sub-aba 2: Tabela Anual
        w_table_years = QWidget()
        lay_ty = QVBoxLayout(w_table_years)
        lay_ty.setContentsMargins(5, 5, 5, 5)
        lay_ty.setSpacing(2)

        self.table_indices = QTableWidget()
        self.table_indices.setColumnCount(10)
        self.table_indices.setHorizontalHeaderLabels([
            tr("Ano"), tr("PRCPTOT (mm)"), tr("R95p (mm)"), tr("RX1day (mm)"), tr("RX5day (mm)"), 
            tr("SDII (mm/d)"), tr("R20mm (dias)"), tr("CDD (dias)"), tr("CWD (dias)"), tr("Sazonalidade")
        ])
        self.table_indices.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_indices.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_indices.setFixedHeight(230)
        lay_ty.addWidget(self.table_indices)

        self.table_indices_summary = QTableWidget()
        self.table_indices_summary.setColumnCount(10)
        self.table_indices_summary.setRowCount(4)
        self.table_indices_summary.horizontalHeader().setVisible(False)
        self.table_indices_summary.verticalHeader().setVisible(False)
        self.table_indices_summary.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_indices_summary.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_indices_summary.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_indices_summary.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_indices_summary.setFixedHeight(112)
        for r in range(4):
            self.table_indices_summary.setRowHeight(r, 26)
        self.table_indices_summary.setStyleSheet(f"""
            QTableWidget {{
                border-top: 2px solid {'#38bdf8' if is_dark else '#0284c7'};
                background-color: transparent;
                gridline-color: {'#3f3f46' if is_dark else '#e2e8f0'};
            }}
        """)
        lay_ty.addWidget(self.table_indices_summary)

        self.table_indices.horizontalScrollBar().valueChanged.connect(
            self.table_indices_summary.horizontalScrollBar().setValue
        )
        self.table_indices.horizontalHeader().sectionResized.connect(self._sync_summary_column_widths)
        self.tab_widget.addTab(w_table_years, tr("📋 Tabela Detalhada Ano a Ano"))

        # Sub-aba 3: Pré-visualização Diária (First Flush)
        w_daily = QWidget()
        lay_daily = QVBoxLayout(w_daily)
        lay_daily.setContentsMargins(5, 5, 5, 5)

        self.table_preview = QTableWidget()
        self.table_preview.setColumnCount(6)
        self.table_preview.setHorizontalHeaderLabels([
            tr("Dia / Registro #"), 
            tr("Data Estimada"), 
            tr("Precipitação Bruta (mm)"), 
            tr("Descarte / Redução (mm)"),
            tr("Precipitação Efetiva (mm)"), 
            tr("Status do Aproveitamento (First Flush)")
        ])
        self.table_preview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_preview.setMinimumHeight(260)
        self.table_preview.setFixedHeight(300)
        lay_daily.addWidget(self.table_preview)
        self.tab_widget.addTab(w_daily, tr("📅 Amostra Diária (First Flush)"))

        lay_prev.addWidget(self.tab_widget)
        gb_preview.setLayout(lay_prev)
        layout.addWidget(gb_preview)

        layout.addStretch()
        content_widget.setLayout(layout)
        scroll.setWidget(content_widget)
        main_vbox.addWidget(scroll)

        self.check_field_highlight(self.txt_start_date, is_date=True)
        self.check_field_highlight(self.txt_discard, is_date=False)

        # Conectar eventos de alternância de modo e localização
        self.btn_group_source.buttonToggled.connect(self.on_source_mode_toggled)
        self.init_climate_and_tariff_ui()

    def _preparar_painel_portugal(self):
        """Na Edição Portugal: distritos e concelhos, e a E-OBS como única série (observada)."""
        from triton.core import base_climatica_portugal as _pt
        self.lbl_climate_uf.setText(f"<b>{tr('Distrito / ilha:')}</b>")
        self.lbl_climate_city.setText(f"<b>{tr('Concelho:')}</b>")
        for combo, rotulo, dado in ((self.combo_climate_model, _pt.MODELO_EOBS, _pt.MODELO_EOBS),
                                    (self.combo_climate_scenario, tr("Observado — E-OBS, 1950–2025"),
                                     _pt.CENARIO_EOBS)):
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(rotulo, dado)
            combo.setEnabled(False)
            combo.blockSignals(False)
        for caixa, valor in ((self.txt_start_date, _pt.INICIO_PADRAO), (self.txt_end_date, _pt.FIM_PADRAO)):
            caixa.blockSignals(True)
            caixa.setText(valor)
            caixa.blockSignals(False)
        self.combo_climate_uf.clear()
        for d in _pt.distritos():
            self.combo_climate_uf.addItem(d, d)
        self.combo_climate_uf.setToolTip(tr(
            "Os 18 distritos do Continente. Açores (fora do domínio da E-OBS) e Madeira (a E-OBS só tem "
            "ali as estações em funcionamento, com falhas em mais de 20% dos dias) não têm série na base: "
            "importe uma série própria."))

    def init_climate_and_tariff_ui(self):
        self._is_populating = True
        try:
            self.combo_climate_uf.clear()
            if getattr(self, "_base_portugal", False):
                self._preparar_painel_portugal()
            else:
                for uf_code, state_name in get_available_ufs():
                    self.combo_climate_uf.addItem(f"{uf_code} - {state_name}", uf_code)

            cfg = self._get_config()
            saved_uf = getattr(cfg, 'climate_city_uf', getattr(cfg, 'tariff_city_uf', 'SC'))
            saved_city = getattr(cfg, 'climate_city_name', getattr(cfg, 'tariff_city_name', 'Florianópolis'))
            if getattr(self, "_base_portugal", False) and self.combo_climate_uf.findData(saved_uf) < 0:
                from triton.core import base_climatica_portugal as _pt
                saved_uf, saved_city = _pt.DISTRITO_PADRAO, _pt.CONCELHO_PADRAO

            uf_idx = -1
            for i in range(self.combo_climate_uf.count()):
                if self.combo_climate_uf.itemData(i) == saved_uf:
                    uf_idx = i
                    break
            if uf_idx >= 0:
                self.combo_climate_uf.setCurrentIndex(uf_idx)
            else:
                self.combo_climate_uf.setCurrentIndex(0)

            self.populate_climate_cities(select_city=saved_city)
        finally:
            self._is_populating = False

        self.combo_climate_uf.currentIndexChanged.connect(self.on_climate_uf_changed)
        self.combo_climate_city.currentIndexChanged.connect(self.on_climate_city_changed)
        self.combo_climate_model.currentIndexChanged.connect(self.on_climate_model_changed)
        self.combo_climate_scenario.currentIndexChanged.connect(self.on_climate_scenario_changed)
        self.populate_recortes()

        # Carrega a série inicial
        self.load_active_national_series()

    def populate_climate_cities(self, select_city=None):
        uf_code = self.combo_climate_uf.currentData() or "SC"
        prev_blocked = self.combo_climate_city.blockSignals(True)
        self.combo_climate_city.clear()
        if getattr(self, "_base_portugal", False):
            from triton.core import base_climatica_portugal as _pt
            for c in _pt.concelhos(uf_code):
                self.combo_climate_city.addItem(c, c)
            idx = self.combo_climate_city.findData(select_city) if select_city else -1
            self.combo_climate_city.setCurrentIndex(idx if idx >= 0 else 0)
            self.combo_climate_city.blockSignals(prev_blocked)
            return

        # A lista vem da base tarifaria, e quem tem de ter arquivo e a base
        # CLIMATICA. Ofertar uma cidade sem serie de precipitacao levaria o
        # usuario a descobrir a falta so ao tentar simular.
        cities = get_cities_by_uf(uf_code)
        try:
            com_serie = set(get_available_climate_cities())
        except Exception:
            com_serie = set()
        if com_serie:
            filtradas = [c for c in cities if c in com_serie]
            # Se o filtro esvaziar a lista, o problema esta na base climatica e
            # nao na escolha do usuario: melhor ofertar tudo que nada.
            cities = filtradas or cities
        for c in cities:
            self.combo_climate_city.addItem(c, c)

        if select_city:
            idx = self.combo_climate_city.findData(select_city)
            if idx >= 0:
                self.combo_climate_city.setCurrentIndex(idx)
            elif self.combo_climate_city.count() > 0:
                self.combo_climate_city.setCurrentIndex(0)
        elif self.combo_climate_city.count() > 0:
            self.combo_climate_city.setCurrentIndex(0)

        self.combo_climate_city.blockSignals(prev_blocked)

    def on_source_mode_toggled(self, button, checked):
        if not checked:
            return
        if self.rb_source_national.isChecked():
            self.panel_national.show()
            self.panel_custom.hide()
            self.load_active_national_series()
        else:
            self.panel_national.hide()
            self.panel_custom.show()
            if not self.precip_file_path:
                self.txt_file_path.setText(tr("Selecione um arquivo CSV de chuva no botão ao lado"))

    def on_climate_uf_changed(self):
        if self._is_populating:
            return
        self.populate_climate_cities()
        self.load_active_national_series()

    def on_climate_city_changed(self):
        if self._is_populating:
            return
        self.load_active_national_series()

    def on_climate_model_changed(self):
        if self._is_populating:
            return
        self.load_active_national_series()

    def on_climate_scenario_changed(self):
        if self._is_populating:
            return
        sc_key = self.combo_climate_scenario.currentData() or "HIST"
        sc_info = CLIMATE_SCENARIOS.get(sc_key, CLIMATE_SCENARIOS["HIST"])
        # Reseta datas padrão do cenário selecionado
        self.txt_start_date.blockSignals(True)
        self.txt_start_date.setText(sc_info["start_date"])
        self.txt_start_date.blockSignals(False)
        self.txt_end_date.setText(sc_info.get("end_date", ""))
        self.populate_recortes()
        self.load_active_national_series()

    def on_apply_date_filter(self):
        self.load_active_national_series()

    def populate_recortes(self):
        """Atalhos de recorte da simulação escolhida; o primeiro item não altera nada."""
        sc_key = self.combo_climate_scenario.currentData() or "HIST"
        self.combo_recorte.blockSignals(True)
        self.combo_recorte.clear()
        self.combo_recorte.addItem(tr("Personalizado — datas acima"), None)
        from triton.core import base_climatica_portugal as _pt
        recortes = _pt.RECORTES if sc_key == _pt.CENARIO_EOBS else RECORTES_SUGERIDOS.get(sc_key, [])
        for rotulo, ini, fim in recortes:
            self.combo_recorte.addItem(tr(rotulo), (ini, fim))
        self.combo_recorte.setCurrentIndex(0)
        self.combo_recorte.blockSignals(False)

    def on_recorte_sugerido(self, *_args):
        periodo = self.combo_recorte.currentData()
        if not periodo:
            return
        ini, fim = periodo
        self.txt_start_date.blockSignals(True)
        self.txt_start_date.setText(ini)
        self.txt_start_date.blockSignals(False)
        self.txt_end_date.setText(fim)
        self.load_active_national_series()

    def load_active_national_series(self):
        if not self.rb_source_national.isChecked():
            return
        city_name = self.combo_climate_city.currentText().strip()
        uf_code = self.combo_climate_uf.currentData() or "SC"
        model_name = self.combo_climate_model.currentText().strip() or "ACCESS-CM2"
        scenario_key = self.combo_climate_scenario.currentData() or "HIST"

        start_date_in = self.txt_start_date.text().strip()
        end_date_in = self.txt_end_date.text().strip()

        try:
            from triton.core import base_climatica_portugal as _pt
            if scenario_key == _pt.CENARIO_EOBS:
                p_data, eff_start, eff_end, tot_days, sel_days, fpath = _pt.carregar_serie(
                    city_name, start_date_in if start_date_in != "-" else None,
                    end_date_in if end_date_in != "-" else None)
            else:
                p_data, eff_start, eff_end, tot_days, sel_days, fpath = load_national_climate_series(
                    city_name=city_name,
                    model_name=model_name,
                    scenario_key=scenario_key,
                    start_date_str=start_date_in if start_date_in != "-" else None,
                    end_date_str=end_date_in if end_date_in != "-" else None,
                )
            self.precip_data = p_data
            self.precip_file_path = fpath

            self.txt_start_date.blockSignals(True)
            self.txt_start_date.setText(eff_start)
            self.txt_start_date.blockSignals(False)
            self.txt_end_date.setText(eff_end)

            years_sel = sel_days / 365.25 if sel_days > 0 else 1.0
            years_tot = tot_days / 365.25 if tot_days > 0 else 1.0

            aviso = ""
            if years_sel < ANOS_MINIMOS_RECOMENDADOS:
                aviso = (f"<br/>⚠️ {tr('Recorte com menos de dez anos: o resultado passa a depender do trecho escolhido. Declare a limitação ou amplie o período.')}")
            self.lbl_date_range_info.setText(
                f"ℹ️ {tr('Série Completa')}: {years_tot:.0f} {tr('anos')} ({tot_days:,} {tr('dias')}) | "
                f"{tr('Período Selecionado para Simulação')}: <b>{years_sel:.1f} {tr('anos')} ({sel_days:,} {tr('dias de')} {eff_start} {tr('a')} {eff_end})</b>".replace(',', '.')
                + aviso
            )

            # Sincroniza tarifas automaticamente com a cidade selecionada
            self.sync_tariffs_for_city(uf_code, city_name)

            self.update_tables()
            self.project_updated.emit()

        except Exception as e:
            self.lbl_date_range_info.setText(f"⚠️ {str(e)}")

    def sync_tariffs_for_city(self, uf_code: str, city_name: str):
        cfg = self._get_config()
        cfg.tariff_city_uf = uf_code
        cfg.tariff_city_name = city_name
        cfg.elec_city_uf = uf_code
        cfg.elec_city_name = city_name
        cfg.climate_city_uf = uf_code
        cfg.climate_city_name = city_name
        cfg.climate_model = self.combo_climate_model.currentText().strip()
        cfg.climate_scenario = self.combo_climate_scenario.currentData() or "HIST"

        if getattr(self, "_tarifas_portugal", False):
            from triton.core import tarifarios_portugal as _tp
            if not self._tariff_is_customized:
                _tp.aplicar(city_name, cfg)
            self.update_tariff_location_preview()
            return

        # O catálogo de tarifas é brasileiro: na Internacional a tarifa é sempre digitada.
        from triton.core.edition import usa_dados_do_brasil
        data = get_city_data(uf_code, city_name) if usa_dados_do_brasil() else None
        if data and not self._tariff_is_customized:
            cfg.water_tariffs = data.get('faixas', cfg.water_tariffs)
            cfg.sewage_mode, cfg.sewage_rate = esgoto_do_municipio(data)
            # Os reajustes contam da vigência da tabela (triton/core/vigencia_tarifaria.py).
            from triton.core.vigencia_tarifaria import data_da_vigencia
            vig = data_da_vigencia(data.get('vigencia_saneamento', ''))
            cfg.tariff_vigencia = vig.strftime("%d/%m/%Y") if vig else ""
            e_kwh = data.get('energia_r_kwh', 0.0)
            if e_kwh > 0:
                cfg.elec_tariff = e_kwh

        self.update_tariff_location_preview()

    def _preview_portugal(self, city_name: str):
        """O quadro do tarifário na Edição Portugal: entidades, vigência e fontes."""
        from triton.core import tarifarios_portugal as _tp
        d = _tp.carregar().get(city_name)
        if d is None:
            self.lbl_t_prestador.setText(f"🏢 <b>{tr('Entidades gestoras:')}</b> --")
            self.lbl_t_reg.setText(f"📋 <b>{tr('Vigência:')}</b> --")
            self.lbl_t_reg.setToolTip("")
            self.lbl_tariff_status.setText(tr("⚪ Concelho ainda sem tarifário transcrito: informe a tarifa em «Editar»"))
            self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #64748b; background-color: transparent;")
            return
        self.lbl_t_prestador.setText(f"🏢 <b>{tr('Entidades gestoras:')}</b> {d['entidades']}")
        self.lbl_t_reg.setText(f"📋 <b>{tr('Vigência:')}</b> {d.get('vigencia', '--')}")
        self.lbl_t_reg.setToolTip("\n".join([tr("Fontes:")] + d.get("fontes", []) + [""] + d.get("notas", [])))
        if self._tariff_is_customized:
            self.lbl_tariff_status.setText(tr("✏️ Tarifas Customizadas pelo Usuário"))
            self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #eab308; background-color: transparent;")
        else:
            self.lbl_tariff_status.setText(tr("🟢 Tarifário transcrito dos documentos oficiais"))
            self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #10b981; background-color: transparent;")

    def update_tariff_location_preview(self):
        uf_code = self.combo_climate_uf.currentData() or "SC"
        city_name = self.combo_climate_city.currentText().strip()
        if getattr(self, "_tarifas_portugal", False):
            self._preview_portugal(city_name)
            return
        data = get_city_data(uf_code, city_name)

        is_dark = get_current_theme() == "dark"
        text_color = '#f4f4f5' if is_dark else '#1e293b'
        muted_color = '#a1a1aa' if is_dark else '#64748b'

        if not data:
            self.lbl_t_prestador.setText(f"🏢 <b>{tr('Saneamento:')}</b> --")
            self.lbl_t_elec.setText(f"⚡ <b>{tr('Eletricidade:')}</b> --")
            self.lbl_t_reg.setText(f"📋 <b>{tr('Regulação:')}</b> --")
            return

        prestador = data.get('prestador_saneamento', '--')
        esgoto = rotulo_do_esgoto(data)
        dist_e = data.get('distribuidora_energia', '--')
        e_kwh = data.get('energia_r_kwh', 0.0)
        agencia = data.get('agencia_reguladora', '')
        vigencia = data.get('vigencia_saneamento', '')
        reg_str = f"{agencia} ({vigencia})" if agencia and vigencia else (agencia or vigencia or "--")

        self.lbl_t_prestador.setText(f"🏢 <b>{tr('Saneamento:')}</b> {prestador} &nbsp;•&nbsp; <b>{tr('Esgoto:')}</b> {esgoto}")
        self.lbl_t_elec.setText(f"⚡ <b>{tr('Eletricidade (ANEEL B1):')}</b> {dist_e} (R$ {e_kwh:.4f}/kWh)")
        self.lbl_t_reg.setText(f"📋 <b>{tr('Regulação & Vigência:')}</b> {reg_str}")
        self.lbl_t_reg.setToolTip(f"{tr('Fonte da tarifa:')} {procedencia_tarifaria(data)}")

        if self._tariff_is_customized:
            self.lbl_tariff_status.setText(tr("✏️ Tarifas Customizadas pelo Usuário"))
            self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #eab308; background-color: transparent;")
        else:
            self.lbl_tariff_status.setText(tr("🟢 Tarifas Oficiais do Catálogo Auditado"))
            self.lbl_tariff_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #10b981; background-color: transparent;")

    def on_open_tariffs_dialog(self):
        from triton.ui.dialogs import DialogTariffs
        cfg = self._get_config()
        dlg = DialogTariffs(self, config=cfg)
        if dlg.exec():
            self._tariff_is_customized = True
            self.update_tariff_location_preview()
            self.project_updated.emit()

    def on_restore_official_tariffs(self, show_dialog=True):
        self._tariff_is_customized = False
        uf_code = self.combo_climate_uf.currentData() or "SC"
        city_name = self.combo_climate_city.currentText().strip()
        if getattr(self, "_tarifas_portugal", False):
            from triton.core import tarifarios_portugal as _tp
            _tp.aplicar(city_name, self._get_config())
            self.update_tariff_location_preview()
            self.project_updated.emit()
            return
        data = get_city_data(uf_code, city_name)
        if data:
            cfg = self._get_config()
            cfg.water_tariffs = data.get('faixas', cfg.water_tariffs)
            cfg.sewage_mode, cfg.sewage_rate = esgoto_do_municipio(data)
            # Os reajustes contam da vigência da tabela (triton/core/vigencia_tarifaria.py).
            from triton.core.vigencia_tarifaria import data_da_vigencia
            vig = data_da_vigencia(data.get('vigencia_saneamento', ''))
            cfg.tariff_vigencia = vig.strftime("%d/%m/%Y") if vig else ""
            e_kwh = data.get('energia_r_kwh', 0.0)
            if e_kwh > 0:
                cfg.elec_tariff = e_kwh
        self.update_tariff_location_preview()
        self.project_updated.emit()
    def get_tariff_location(self) -> tuple:
        from triton.core.edition import usa_dados_do_brasil
        if not (usa_dados_do_brasil() or getattr(self, "_base_portugal", False)):
            # Na International, a lista é a das cidades brasileiras da CLIMBra, oculta: o
            # projeto gravava Florianópolis (SC) como local da tarifa e do fator regional.
            return ("CUSTOM", "CUSTOM")
        return (self.combo_climate_uf.currentData() or "SC", self.combo_climate_city.currentText().strip())

    def set_tariff_location(self, uf_code: str, city_name: str):
        self._is_populating = True
        try:
            uf_idx = self.combo_climate_uf.findData(uf_code)
            if uf_idx >= 0:
                self.combo_climate_uf.setCurrentIndex(uf_idx)
            self.populate_climate_cities(select_city=city_name)
        finally:
            self._is_populating = False
        if getattr(self, "rb_source_national", None) and self.rb_source_national.isChecked():
            if self.precip_data is None:
                self.load_active_national_series()
            else:
                self.update_tariff_location_preview()
        else:
            self.update_tariff_location_preview()

    def _get_config(self):
        main_win = self.window()
        if main_win and hasattr(main_win, "config"):
            return main_win.config
        if not hasattr(self, "_internal_config"):
            from triton.core.parser import TritonConfig
            self._internal_config = TritonConfig()
        return self._internal_config

    def check_field_highlight(self, widget, is_date=False):
        val = widget.text().strip()
        is_dark = get_current_theme() == "dark"
        bg_valid = "#27272a" if is_dark else "#ffffff"
        border_valid = "#3f3f46" if is_dark else "#cbd5e1"
        text_valid = "#ffffff" if is_dark else "#1e293b"

        if not val or val == "-":
            widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {'#713f12' if is_dark else '#fef08a'}; border: 1.5px solid #eab308; color: {'#fef08a' if is_dark else '#1e293b'}; }}")
            return False
        if is_date:
            try:
                datetime.strptime(val, "%d/%m/%Y")
                widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {bg_valid}; border: 1px solid {border_valid}; color: {text_valid}; }}")
                return True
            except ValueError:
                # Permite ano isolado válido (ex: 1980 a 2100)
                if val.isdigit() and len(val) == 4 and 1900 <= int(val) <= 2100:
                    widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {bg_valid}; border: 1px solid {border_valid}; color: {text_valid}; }}")
                    return True
                widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {'#713f12' if is_dark else '#fef08a'}; border: 1.5px solid #eab308; color: {'#fef08a' if is_dark else '#1e293b'}; }}")
                return False
        else:
            try:
                v = float(val.replace(',', '.'))
                if v >= 0:
                    widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {bg_valid}; border: 1px solid {border_valid}; color: {text_valid}; }}")
                    return True
            except ValueError:
                pass
            widget.setStyleSheet(f"QLineEdit, DatePickerLineEdit {{ background-color: {'#713f12' if is_dark else '#fef08a'}; border: 1.5px solid #eab308; color: {'#fef08a' if is_dark else '#1e293b'}; }}")
            return False

    def on_start_date_changed(self):
        self.check_field_highlight(self.txt_start_date, is_date=True)
        if hasattr(self, 'txt_custom_start_date') and self.txt_custom_start_date.text() != self.txt_start_date.text():
            self.txt_custom_start_date.blockSignals(True)
            self.txt_custom_start_date.setText(self.txt_start_date.text())
            self.txt_custom_start_date.blockSignals(False)
        self.update_tables()
        self.project_updated.emit()

    def on_custom_start_date_changed(self):
        self.check_field_highlight(self.txt_custom_start_date, is_date=True)
        if self.txt_start_date.text() != self.txt_custom_start_date.text():
            self.txt_start_date.blockSignals(True)
            self.txt_start_date.setText(self.txt_custom_start_date.text())
            self.txt_start_date.blockSignals(False)
        self.update_tables()
        self.project_updated.emit()

    def on_discard_changed(self):
        self.check_field_highlight(self.txt_discard, is_date=False)
        self.update_preview_table()
        self.project_updated.emit()

    def on_discard_mode_changed(self, idx=None):
        mode = self.get_discard_mode()
        if mode == 3:
            self.txt_discard_days.show()
            self.lbl_discard_days.show()
        else:
            self.txt_discard_days.hide()
            self.lbl_discard_days.hide()
        self.update_preview_table()
        self.project_updated.emit()

    def on_discard_days_changed(self):
        self.update_preview_table()
        self.project_updated.emit()

    def get_discard_mode(self) -> int:
        if hasattr(self, 'combo_discard_mode') and self.combo_discard_mode.currentData():
            return int(self.combo_discard_mode.currentData())
        return 1

    def get_discard_days(self) -> int:
        if hasattr(self, 'txt_discard_days'):
            try:
                return max(1, int(float(self.txt_discard_days.text().replace(',', '.'))))
            except Exception:
                return 7
        return 7

    def on_browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            tr("Selecionar Arquivo CSV de Chuva"), 
            "", 
            f"{tr('Arquivos CSV')} (*.csv);;{tr('Todos os Arquivos')} (*.*)"
        )
        if file_path:
            self.load_rain_file(file_path)

    def load_rain_file(self, file_path: str):
        try:
            self.precip_data = load_precipitation(file_path)
            self.precip_file_path = file_path
            self.txt_file_path.setText(os.path.basename(file_path))

            total_days = len(self.precip_data)
            max_p = float(max(self.precip_data)) if total_days > 0 else 0.0
            sum_p = float(sum(self.precip_data)) if total_days > 0 else 0.0
            years = total_days / 365.25 if total_days > 0 else 1.0
            avg_annual = sum_p / years

            self.lbl_stats.setText(
                f"{tr('Registros')}: {total_days} {tr('dias')} ({years:.1f} {tr('anos')}) | "
                f"{tr('Precipitação Média Anual')}: {avg_annual:.1f} mm | "
                f"{tr('Máximo Diário')}: {max_p:.1f} mm"
            )
            self.update_tables()
            self.project_updated.emit()
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao carregar arquivo de chuva')}:\n{str(e)}")

    def update_tables(self):
        if self.precip_data is None:
            return

        try:
            start_dt = datetime.strptime(self.txt_start_date.text().strip(), "%d/%m/%Y")
            if start_dt.year < 1900 or start_dt.year > 2100:
                start_dt = datetime(1980, 1, 1)
        except Exception:
            start_dt = datetime(1980, 1, 1)

        try:
            dates = [start_dt + timedelta(days=i) for i in range(len(self.precip_data))]
            data_series = list(zip(dates, self.precip_data))
            calc = IndicesCalculator(data_series)
            df_raw = calc.compute_climate_indices()
            df_indices = df_raw.set_index('year')
            self.climate_indices_df = df_indices

            cols_keys = ['PRCPTOT', 'R95p', 'RX1day', 'RX5day', 'SDII', 'R20mm', 'CDD', 'CWD', 'Seasonality_Index']
            summary = {}
            for col in cols_keys:
                s = df_indices[col].dropna()
                summary[col] = {
                    'mean': float(s.mean()) if not s.empty else 0.0,
                    'min': float(s.min()) if not s.empty else 0.0,
                    'max': float(s.max()) if not s.empty else 0.0,
                    'std': float(s.std()) if len(s) > 1 else 0.0,
                }

            self.card_prcptot.set_value(f"{summary['PRCPTOT']['mean']:.1f} mm")
            self.card_r95p.set_value(f"{summary['R95p']['mean']:.1f} mm")
            self.card_rx1day.set_value(f"{summary['RX1day']['mean']:.1f} mm")
            self.card_rx5day.set_value(f"{summary['RX5day']['mean']:.1f} mm")
            self.card_sdii.set_value(f"{summary['SDII']['mean']:.2f} mm/d")
            self.card_r20mm.set_value(f"{summary['R20mm']['mean']:.1f} dias")
            self.card_cdd.set_value(f"{summary['CDD']['mean']:.1f} dias")
            self.card_cwd.set_value(f"{summary['CWD']['mean']:.1f} dias")
            self.card_saz.set_value(f"{summary['Seasonality_Index']['mean']:.2f}")

            self.chart_prcptot.plot_data(df_indices)
            self.chart_sdii_r95p.plot_data(df_indices)
            self.chart_cdd_cwd.plot_data(df_indices)
            self.chart_seasonal.plot_data(self.precip_data, start_dt)

            self.populate_indices_table(df_indices, summary)
            self.update_preview_table(start_dt)

        except Exception as e:
            print(f"Erro no cálculo de indicadores climatológicos: {e}")

    def populate_indices_table(self, df, summary):
        from triton.ui.translation import get_current_theme
        is_dark = get_current_theme() == "dark"

        years = df.index.tolist()
        self.table_indices.setRowCount(len(years))

        for r, yr in enumerate(years):
            row_data = df.loc[yr]
            self.table_indices.setItem(r, 0, QTableWidgetItem(str(int(yr))))
            self.table_indices.item(r, 0).setTextAlignment(Qt.AlignCenter)

            cols_keys = ['PRCPTOT', 'R95p', 'RX1day', 'RX5day', 'SDII', 'R20mm', 'CDD', 'CWD', 'Seasonality_Index']
            for c, k in enumerate(cols_keys):
                val = row_data[k]
                item = QTableWidgetItem(f"{val:.2f}" if k in ['SDII', 'Seasonality_Index'] else f"{val:.1f}")
                item.setTextAlignment(Qt.AlignCenter)
                self.table_indices.setItem(r, c+1, item)

        if summary:
            bold_font = QFont("Segoe UI", 9, QFont.Bold)
            summary_specs = [
                (0, tr("Média"), [f"{summary[k]['mean']:.2f}" if k in ['SDII', 'Seasonality_Index'] else f"{summary[k]['mean']:.1f}" for k in cols_keys],
                 QColor("#1e3a8a" if is_dark else "#e0f2fe"), QColor("#38bdf8" if is_dark else "#0369a1")),
                (1, tr("Mínimo"), [f"{summary[k]['min']:.2f}" if k in ['SDII', 'Seasonality_Index'] else f"{summary[k]['min']:.1f}" for k in cols_keys],
                 QColor("#27272a" if is_dark else "#f8fafc"), QColor("#f4f4f5" if is_dark else "#1e293b")),
                (2, tr("Máximo"), [f"{summary[k]['max']:.2f}" if k in ['SDII', 'Seasonality_Index'] else f"{summary[k]['max']:.1f}" for k in cols_keys],
                 QColor("#27272a" if is_dark else "#f8fafc"), QColor("#f4f4f5" if is_dark else "#1e293b")),
                (3, tr("Desvio Padrão"), [f"{summary[k]['std']:.2f}" if k in ['SDII', 'Seasonality_Index'] else f"{summary[k]['std']:.1f}" for k in cols_keys],
                 QColor("#27272a" if is_dark else "#f8fafc"), QColor("#f4f4f5" if is_dark else "#1e293b"))
            ]
            self.table_indices_summary.setRowCount(4)
            for r_idx, label_str, stat_vals, bg_color, fg_color in summary_specs:
                self.table_indices_summary.setRowHeight(r_idx, 26)
                row_items = [label_str] + stat_vals
                for c_idx, val_str in enumerate(row_items):
                    item = QTableWidgetItem(val_str)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFont(bold_font)
                    item.setBackground(bg_color)
                    item.setForeground(fg_color)
                    self.table_indices_summary.setItem(r_idx, c_idx, item)
            self._sync_summary_column_widths()

    def _sync_summary_column_widths(self, *args):
        if not hasattr(self, 'table_indices') or not hasattr(self, 'table_indices_summary'):
            return
        for c in range(self.table_indices.columnCount()):
            w = self.table_indices.columnWidth(c)
            if w > 0:
                self.table_indices_summary.setColumnWidth(c, w)

    def update_preview_table(self, start_dt=None):
        if self.precip_data is None:
            return

        if start_dt is None:
            try:
                start_dt = datetime.strptime(self.txt_start_date.text().strip(), "%d/%m/%Y")
            except Exception:
                start_dt = datetime(1980, 1, 1)

        # Campo vazio não é lâmina zero: é lâmina não declarada, e aí vale a da
        # ABNT NBR 15527:2019 — a mesma que o motor assume. Antes esta prévia
        # mostrava a chuva sem descarte nenhum enquanto a simulação descontava
        # 2 mm, duas contas diferentes na mesma janela. O campo segue em amarelo
        # até o usuário declarar a lâmina que mediu.
        discard_valid = True
        discard_mm = LAMINA_DE_DESCARTE_PADRAO_MM
        val_txt = self.txt_discard.text().strip().replace(',', '.')
        if val_txt and val_txt != "-":
            try:
                lida = float(val_txt)
                if lida >= 0:
                    discard_mm = lida
                else:
                    discard_valid = False
            except ValueError:
                discard_valid = False        # texto que não é número

        total_days = len(self.precip_data)
        show_count = min(total_days, 100)
        self.table_preview.setRowCount(show_count)

        discard_mode = self.get_discard_mode()
        discard_days = self.get_discard_days()
        last_discard_day = -999999

        is_dark = get_current_theme() == "dark"

        sum_p = float(sum(self.precip_data)) if total_days > 0 else 0.0
        max_p = float(max(self.precip_data)) if total_days > 0 else 0.0
        years = total_days / 365.25 if total_days > 0 else 1.0
        avg_annual = sum_p / years

        if discard_valid:
            total_discard = 0.0
            last_d_stat = -999999
            for i, p_val in enumerate(self.precip_data):
                p_v = float(p_val)
                if p_v > 0.0:
                    app = False
                    if discard_mode == 1:
                        app = True
                    elif discard_mode == 2:
                        prev_p = float(self.precip_data[i-1]) if i > 0 else 0.0
                        if prev_p < 1.0:
                            app = True
                    elif discard_mode == 3:
                        if (i - last_d_stat) >= discard_days:
                            app = True
                    if app:
                        last_d_stat = i
                        total_discard += min(p_v, discard_mm)
            avg_discard_annual = total_discard / years
            avg_eff_annual = (sum_p - total_discard) / years
            disc_pct = (total_discard / sum_p * 100.0) if sum_p > 0 else 0.0
            self.lbl_stats.setText(
                tr('{0}: {1:,} {2} ({3:.1f} {4}) | {5}: {6:.1f} mm/ano | {7}: {8:.1f} mm/ano ({9:.1f}%) | {10}: {11:.1f} mm/ano').format(tr('Registros'), total_days, tr('dias'), years, tr('anos'), tr('Chuva Bruta'), avg_annual, tr('Descarte'), avg_discard_annual, disc_pct, tr('Chuva Efetiva'), avg_eff_annual).replace(',', '.')
            )
        else:
            self.lbl_stats.setText(
                f"{tr('Registros')}: {total_days:,} {tr('dias')} ({years:.1f} {tr('anos')}) | "
                f"{tr('Precipitação Média Anual')}: {avg_annual:.1f} mm | "
                f"{tr('Máximo Diário')}: {max_p:.1f} mm".replace(',', '.')
            )

        for r in range(show_count):
            cur_dt = start_dt + timedelta(days=r)
            dt_str = cur_dt.strftime("%d/%m/%Y")
            rain_p = float(self.precip_data[r])

            item_day = QTableWidgetItem(f"{tr('Dia')} {r+1}")
            item_day.setTextAlignment(Qt.AlignCenter)

            item_date = QTableWidgetItem(dt_str)
            item_date.setTextAlignment(Qt.AlignCenter)

            item_rain = QTableWidgetItem(f"{format_ptbr(rain_p, 1)} mm")
            item_rain.setTextAlignment(Qt.AlignCenter)

            item_disc = QTableWidgetItem()
            item_disc.setTextAlignment(Qt.AlignCenter)

            item_eff = QTableWidgetItem()
            item_eff.setTextAlignment(Qt.AlignCenter)

            item_status = QTableWidgetItem()

            apply_discard = False
            if rain_p > 0.0:
                if discard_mode == 1:
                    apply_discard = True
                elif discard_mode == 2:
                    prev_p = float(self.precip_data[r-1]) if r > 0 else 0.0
                    if prev_p < 1.0:
                        apply_discard = True
                elif discard_mode == 3:
                    if (r - last_discard_day) >= discard_days:
                        apply_discard = True

            if not discard_valid:
                if rain_p == 0.0:
                    item_disc.setText("0,0 mm")
                    item_disc.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
                    item_eff.setText("0,0 mm")
                    item_eff.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
                    item_status.setText(tr("Sem chuva (0,0 mm)"))
                    item_status.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
                else:
                    item_disc.setText("-")
                    item_eff.setText("-")
                    item_status.setText(tr("⚠️ Informe o descarte inicial (mm) acima para calcular"))
                    item_status.setBackground(QColor("#713f12" if is_dark else "#fef08a"))
                    item_status.setForeground(QColor("#fef9c3" if is_dark else "#854d0e"))
            elif rain_p == 0.0:
                item_disc.setText("0,0 mm")
                item_disc.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
                item_eff.setText("0,0 mm")
                item_eff.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
                item_status.setText(tr("Sem chuva (0,0 mm)"))
                item_status.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))
            elif apply_discard:
                last_discard_day = r
                disc_val = min(rain_p, discard_mm)
                eff_rain = max(0.0, rain_p - discard_mm)

                item_disc.setText(f"-{format_ptbr(disc_val, 1)} mm")
                item_eff.setText(f"{format_ptbr(eff_rain, 1)} mm")

                if eff_rain <= 0.0:
                    item_disc.setBackground(QColor("#7f1d1d" if is_dark else "#fee2e2"))
                    item_disc.setForeground(QColor("#fecaca" if is_dark else "#991b1b"))
                    item_disc.setFont(QFont("Segoe UI", 9, QFont.Bold))
                    item_eff.setText("0,0 mm")
                    item_eff.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))

                    item_status.setText(f"❌ {tr('Chuva 100% descartada')} ({format_ptbr(rain_p, 1)} mm ≤ {tr('Descarte')} {format_ptbr(discard_mm, 1)} mm)")
                    item_status.setBackground(QColor("#7f1d1d" if is_dark else "#fee2e2"))
                    item_status.setForeground(QColor("#fecaca" if is_dark else "#991b1b"))
                    item_status.setFont(QFont("Segoe UI", 9, QFont.Bold))
                else:
                    item_disc.setBackground(QColor("#78350f" if is_dark else "#fef3c7"))
                    item_disc.setForeground(QColor("#fde68a" if is_dark else "#b45309"))
                    item_disc.setFont(QFont("Segoe UI", 9, QFont.Bold))

                    item_eff.setBackground(QColor("#064e3b" if is_dark else "#dcfce7"))
                    item_eff.setForeground(QColor("#d1fae5" if is_dark else "#166534"))
                    item_eff.setFont(QFont("Segoe UI", 9, QFont.Bold))

                    item_status.setText(f"✅ {tr('Descarte Aplicado')} (-{format_ptbr(disc_val, 1)} mm {tr('First Flush')})")
                    item_status.setBackground(QColor("#064e3b" if is_dark else "#dcfce7"))
                    item_status.setForeground(QColor("#d1fae5" if is_dark else "#166534"))
                    item_status.setFont(QFont("Segoe UI", 9, QFont.Bold))
            else:
                disc_val = 0.0
                eff_rain = rain_p
                item_disc.setText("0,0 mm")
                item_disc.setForeground(QColor("#a1a1aa" if is_dark else "#64748b"))

                item_eff.setText(f"{format_ptbr(eff_rain, 1)} mm")
                item_eff.setBackground(QColor("#1e3a8a" if is_dark else "#e0f2fe"))
                item_eff.setForeground(QColor("#dbeafe" if is_dark else "#0369a1"))
                item_eff.setFont(QFont("Segoe UI", 9, QFont.Bold))

                item_status.setText(f"✅ {tr('Aproveitável sem descarte')} ({tr('Telhado Limpo')})")
                item_status.setBackground(QColor("#1e3a8a" if is_dark else "#e0f2fe"))
                item_status.setForeground(QColor("#dbeafe" if is_dark else "#0369a1"))
                item_status.setFont(QFont("Segoe UI", 9, QFont.Bold))

            self.table_preview.setItem(r, 0, item_day)
            self.table_preview.setItem(r, 1, item_date)
            self.table_preview.setItem(r, 2, item_rain)
            self.table_preview.setItem(r, 3, item_disc)
            self.table_preview.setItem(r, 4, item_eff)
            self.table_preview.setItem(r, 5, item_status)

    def get_project_state(self) -> dict:
        return {
            "source_mode": "national_db" if self.rb_source_national.isChecked() else "custom_file",
            "climate_uf": self.combo_climate_uf.currentData() or "SC",
            "climate_city": self.combo_climate_city.currentText().strip(),
            "climate_model": self.combo_climate_model.currentText().strip(),
            "climate_scenario": self.combo_climate_scenario.currentData() or "HIST",
            "start_date": self.txt_start_date.text().strip(),
            "end_date": self.txt_end_date.text().strip(),
            "file_path": self.txt_file_path.text().strip(),
            "discard": self.txt_discard.text().strip(),
            "discard_mode": self.get_discard_mode(),
            "discard_days": self.get_discard_days(),
            "tariff_customized": self._tariff_is_customized,
        }

    def apply_project_state(self, state: dict, config=None):
        state = state or {}
        # Sem o estado da tela gravado, vale a fonte do projeto: a série recomposta da base
        # CLIMBra (referência no arquivo) continua sendo da CLIMBra, e não «arquivo próprio».
        if (config is not None and getattr(config, "climate_source_mode", "") == "national_db"
                and self.rb_source_national.isChecked()):
            padrao = "national_db"
        else:
            padrao = "custom_file" if self.precip_data is not None else "national_db"
        mode = state.get("source_mode", padrao)
        if mode == "national_db":
            self.rb_source_national.setChecked(True)
        else:
            self.rb_source_custom.setChecked(True)

        uf = state.get("climate_uf", getattr(config, 'climate_city_uf', 'SC'))
        city = state.get("climate_city", getattr(config, 'climate_city_name', 'Florianópolis'))
        model = state.get("climate_model", getattr(config, 'climate_model', 'ACCESS-CM2'))
        scenario = state.get("climate_scenario", getattr(config, 'climate_scenario', 'HIST'))

        self._is_populating = True
        try:
            uf_idx = self.combo_climate_uf.findData(uf)
            if uf_idx >= 0:
                self.combo_climate_uf.setCurrentIndex(uf_idx)
            self.populate_climate_cities(select_city=city)

            m_idx = self.combo_climate_model.findText(model)
            if m_idx >= 0:
                self.combo_climate_model.setCurrentIndex(m_idx)

            sc_idx = self.combo_climate_scenario.findData(scenario)
            if sc_idx >= 0:
                self.combo_climate_scenario.setCurrentIndex(sc_idx)

            s_date = state.get("start_date", getattr(config, 'climate_start_date' if mode == "national_db"
                                                     else 'start_date', '01/01/1980'))
            e_date = state.get("end_date", getattr(config, 'climate_end_date', '31/12/2013'))
            self.txt_start_date.setText(s_date)
            self.txt_end_date.setText(e_date)

            disc = state.get("discard", getattr(config, 'discard', '-'))
            self.txt_discard.setText(str(disc))

            d_mode = int(state.get("discard_mode", getattr(config, 'discard_mode', 1)))
            idx_dm = self.combo_discard_mode.findData(d_mode)
            if idx_dm >= 0:
                self.combo_discard_mode.setCurrentIndex(idx_dm)

            self.txt_discard_days.setText(str(state.get("discard_days", getattr(config, 'discard_days_interval', 7))))
            self._tariff_is_customized = bool(state.get("tariff_customized", getattr(config, 'tariff_customized', False)))
        finally:
            self._is_populating = False

        if mode == "national_db":
            if self.precip_data is None or state.get("source_mode") == "national_db":
                self.load_active_national_series()
        else:
            f_path = state.get("file_path", getattr(config, 'precip_file', ''))
            if f_path and os.path.isfile(f_path):
                self.load_rain_file(f_path)

    def apply_custom_tariffs(self, tariffs_dict: dict):
        """Aplica tarifas personalizadas vindas do Gestor de Tarifas ou Diálogo de Tarifas."""
        if not tariffs_dict:
            return
        self._tariff_is_customized = True
        self.project_updated.emit()
