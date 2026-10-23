"""
Etapa 2: Edificação, Ocupantes & Modulação de Demanda de Água (Triton).
Oferece:
1. 💧 Demanda Diária Simplificada (Modo clássico, direto e intuitivo por consumo per capita e % de substituição pluvial).
2. 🧮 Detalhamento Avançado de Usos & Aparelhos (Estimativa NBR 5626/ANA, partição potável/não-potável e irrigação de jardim).
3. 📅 Variação Semanal (Segunda a Domingo).
4. 🗓️ Variação Mensal (Sazonalidade Jan–Dez).
5. 📊 Variação Total Diária (Planilha CSV/Excel).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, 
    QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, 
    QTabWidget, QFrame, QComboBox, QCheckBox, QScrollArea, QDoubleSpinBox, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor

from triton.core.parser import parse_float, parse_int
from triton.core.fracao_atendivel import aviso_percentual_pequeno, fracao_para_percentual, fracao_total
from triton.ui.translation import tr, get_current_theme, get_current_lang
from triton.ui.textos_da_edicao import titulo_tipologia


# Catálogo oficial unificado de tipologias de edificação (NBR 5626 / ANA / NBR 15527 / ANVISA)
BUILDING_TEMPLATES = [
    {
        "id": "res_medio",
        "name": "🏠 Residencial Unifamiliar — Padrão Médio (150 L/hab/dia | 65% Potável | Jardim 15 m²)",
        "occupant_label": "Número de Moradores:",
        "demand_label": "Consumo Per Capita (L/hab/dia):",
        "unit": "hab",
        "potable_title": "<b>🚿 Usos Potáveis Internos (por Morador)</b>",
        "sink_label": "Pias, Cozinha & Filtro (L/hab/dia):",
        "non_potable_title": "<b>🚽 Usos Não-Potáveis Internos (por Morador)</b>",
        "wash_cycles_label": "Máquina de Lavar Roupas (ciclos/sem):",
        "wash_vol_label": "Consumo da máquina (L/ciclo):",
        "outdoor_title": "<b>🌿 Jardim & Usos Externos</b>",
        "garden_label": "Área de Jardim Privativo (m²):",
        "wash_ext_label": "Lavagem calçadas / veículos (L/sem):",
        "default_residents": 4,
        "shower_count": 1.0, "shower_time": 8.0, "shower_flow": 9.0,
        "sink_liters": 26.0,
        "toilet_flushes": 4.0, "toilet_type_idx": 0,  # Caixa Acoplada (6 L)
        "wash_cycles": 3.0, "wash_vol": 100.0,
        "garden_area": 15.0, "garden_rate_idx": 0,     # Gramado / Geral (3.0 L/m²/dia)
        "wash_external": 35.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "res_popular",
        "name": "🏡 Residencial Unifamiliar — Econômico / Popular (120 L/hab/dia | 68% Potável | Jardim 10 m²)",
        "occupant_label": "Número de Moradores:",
        "demand_label": "Consumo Per Capita (L/hab/dia):",
        "unit": "hab",
        "potable_title": "<b>🚿 Usos Potáveis Internos (por Morador)</b>",
        "sink_label": "Pias, Tanque & Cozinha (L/hab/dia):",
        "non_potable_title": "<b>🚽 Usos Não-Potáveis Internos (por Morador)</b>",
        "wash_cycles_label": "Máquina / Tanque (ciclos/sem):",
        "wash_vol_label": "Consumo por ciclo (L):",
        "outdoor_title": "<b>🌿 Jardim & Usos Externos</b>",
        "garden_label": "Área de Jardim (m²):",
        "wash_ext_label": "Lavagem calçadas / pisos (L/sem):",
        "default_residents": 4,
        "shower_count": 1.0, "shower_time": 6.0, "shower_flow": 7.0,
        "sink_liters": 40.0,
        "toilet_flushes": 4.0, "toilet_type_idx": 0,  # 6 L
        "wash_cycles": 2.0, "wash_vol": 80.0,
        "garden_area": 10.0, "garden_rate_idx": 2,     # Plantas Baixo Consumo (1.5 L/m²/dia)
        "wash_external": 35.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "res_alto",
        "name": "🏰 Residencial Unifamiliar — Alto Padrão (220 L/hab/dia | 60% Potável | Jardim 30 m²)",
        "occupant_label": "Número de Moradores:",
        "demand_label": "Consumo Per Capita (L/hab/dia):",
        "unit": "hab",
        "potable_title": "<b>🚿 Usos Potáveis Internos (por Morador)</b>",
        "sink_label": "Pias, Cozinha Gourmet & Filtros (L/hab/dia):",
        "non_potable_title": "<b>🚽 Usos Não-Potáveis Internos (por Morador)</b>",
        "wash_cycles_label": "Máquina / Lavanderia (ciclos/sem):",
        "wash_vol_label": "Consumo por ciclo (L):",
        "outdoor_title": "<b>🌿 Jardim, Paisagismo & Usos Externos</b>",
        "garden_label": "Área de Jardim / Paisagismo (m²):",
        "wash_ext_label": "Lavagem calçadas / veículos (L/sem):",
        "default_residents": 4,
        "shower_count": 1.0, "shower_time": 10.0, "shower_flow": 11.0,
        "sink_liters": 22.0,
        "toilet_flushes": 5.0, "toilet_type_idx": 0,  # 6 L
        "wash_cycles": 4.0, "wash_vol": 120.0,
        "garden_area": 30.0, "garden_rate_idx": 0,     # 3.0 L/m²/dia
        "wash_external": 70.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "res_multi",
        "name": "🏢 Edifício Residencial Multifamiliar / Apartamentos (140 L/hab/dia | 65% Potável | Sem rega privativa)",
        "occupant_label": "Número de Moradores:",
        "demand_label": "Consumo Per Capita (L/hab/dia):",
        "unit": "hab",
        "potable_title": "<b>🚿 Usos Potáveis Internos (por Morador)</b>",
        "sink_label": "Pias & Cozinha (L/hab/dia):",
        "non_potable_title": "<b>🚽 Usos Não-Potáveis Internos (por Morador)</b>",
        "wash_cycles_label": "Máquina de Lavar (ciclos/sem):",
        "wash_vol_label": "Consumo por ciclo (L):",
        "outdoor_title": "<b>🌿 Áreas Comuns & Jardim Condominial</b>",
        "garden_label": "Área Verde Condominial (m²):",
        "wash_ext_label": "Lavagem de garagens / pátios (L/sem):",
        "default_residents": 20,
        "shower_count": 1.0, "shower_time": 8.0, "shower_flow": 8.5,
        "sink_liters": 23.0,
        "toilet_flushes": 4.0, "toilet_type_idx": 0,  # 6 L
        "wash_cycles": 3.0, "wash_vol": 90.0,
        "garden_area": 10.0, "garden_rate_idx": 0,     # 3.0 L/m²/dia
        "wash_external": 0.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "comercial",
        "name": "💼 Comercial / Escritórios (50 L/pessoa/dia — Foco em Copas, Bebedouros & Bacias)",
        "occupant_label": "Número de Funcionários / Ocupantes:",
        "demand_label": "Consumo por Funcionário (L/pessoa/dia):",
        "unit": "pessoa",
        "potable_title": "<b>☕ Usos Potáveis: Copas, Bebedouros & Cafeteria (por Funcionário)</b>",
        "sink_label": "Copas, Bebedouros & Café (L/pessoa/dia):",
        "non_potable_title": "<b>🚽 Usos Não-Potáveis: Bacias & Limpeza (por Funcionário)</b>",
        "wash_cycles_label": "Limpeza de Pisos / Sanitização (vezes/sem):",
        "wash_vol_label": "Consumo por limpeza (L):",
        "outdoor_title": "<b>🌿 Paisagismo Comercial & Pátios</b>",
        "garden_label": "Área Verde / Paisagismo Comercial (m²):",
        "wash_ext_label": "Lavagem de calçadas / pátios (L/sem):",
        "default_residents": 20,
        "shower_count": 0.0, "shower_time": 0.0, "shower_flow": 6.0,
        "sink_liters": 25.0,
        "toilet_flushes": 4.0, "toilet_type_idx": 0,  # Caixa Acoplada 6 L (4x6 = 24 L) -> Total ~50 L
        "wash_cycles": 0.0, "wash_vol": 0.0,
        "garden_area": 10.0, "garden_rate_idx": 2,     # 1.5 L/m²/dia
        "wash_external": 35.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "escola",
        "name": "🏫 Escola / Creche / Educação (40 L/aluno/dia — Foco em Bebedouros, Merenda & Bacias)",
        "occupant_label": "Número de Alunos (por turno):",
        "demand_label": "Consumo por Aluno (L/aluno/dia):",
        "unit": "aluno",
        "potable_title": "<b>🚰 Usos Potáveis: Bebedouros, Pias & Merenda (por Aluno)</b>",
        "sink_label": "Bebedouros, Lavatórios & Merenda (L/aluno/dia):",
        "non_potable_title": "<b>🎒 Usos Não-Potáveis: Bacias & Sanitários (por Aluno)</b>",
        "wash_cycles_label": "Limpeza de Salas / Pátios (vezes/sem):",
        "wash_vol_label": "Volume por lavagem (L):",
        "outdoor_title": "<b>🌿 Áreas Verdes, Quadras & Pátios</b>",
        "garden_label": "Área Verde / Pátios Escolares (m²):",
        "wash_ext_label": "Lavagem de quadras / pátios (L/sem):",
        "default_residents": 100,
        "shower_count": 0.0, "shower_time": 0.0, "shower_flow": 6.0,
        "sink_liters": 16.0,
        "toilet_flushes": 4.0, "toilet_type_idx": 0,  # Caixa 6 L (4x6 = 24 L) -> Total 40 L (16/24 = 40%/60%)
        "wash_cycles": 0.0, "wash_vol": 0.0,
        "garden_area": 10.0, "garden_rate_idx": 0,     # 3.0 L/m²/dia
        "wash_external": 0.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "hotel",
        "name": "🏨 Hotel / Pousada / Hospedagem (250 L/hóspede/dia — Duchas, Restaurante & Enxoval)",
        "occupant_label": "Número de Hóspedes / Vagas:",
        "demand_label": "Consumo por Hóspede (L/hóspede/dia):",
        "unit": "hóspede",
        "potable_title": "<b>🚿 Usos Potáveis: Duchas, Pias & Restaurante (por Hóspede)</b>",
        "sink_label": "Lavatórios, Bar & Restaurante (L/hóspede/dia):",
        "non_potable_title": "<b>🛏️ Usos Não-Potáveis: Bacias & Enxoval (por Hóspede)</b>",
        "wash_cycles_label": "Lavanderia de Enxoval / Rouparia (ciclos/sem):",
        "wash_vol_label": "Consumo da lavanderia (L/ciclo):",
        "outdoor_title": "<b>🌿 Jardins, Decks & Piscinas</b>",
        "garden_label": "Jardins & Decks Paisagísticos (m²):",
        "wash_ext_label": "Lavagem de pisos / áreas externas (L/sem):",
        "default_residents": 30,
        "shower_count": 1.5, "shower_time": 10.0, "shower_flow": 10.0,
        "sink_liters": 12.5,
        "toilet_flushes": 5.0, "toilet_type_idx": 0,  # 6 L
        "wash_cycles": 40.0, "wash_vol": 300.0,
        "garden_area": 25.0, "garden_rate_idx": 0,     # 3.0 L/m²/dia
        "wash_external": 35.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
    {
        "id": "hospital",
        "name": "🏥 Hospital / Clínica de Saúde (250 L/leito/dia — Esterilização, Higiene & Lavanderia)",
        "occupant_label": "Número de Leitos / Pacientes:",
        "demand_label": "Consumo por Leito (L/leito/dia):",
        "unit": "leito",
        "potable_title": "<b>🩺 Usos Potáveis: Higiene, Esterilização & Copa (por Leito)</b>",
        "sink_label": "Esterilização, Higiene & Copa (L/leito/dia):",
        "non_potable_title": "<b>🏥 Usos Não-Potáveis: Bacias & Lavanderia Hospitalar (por Leito)</b>",
        "wash_cycles_label": "Lavanderia Hospitalar / Rouparia (ciclos/sem):",
        "wash_vol_label": "Volume por ciclo de lavagem (L):",
        "outdoor_title": "<b>🌿 Áreas Verdes Hospitalares & Acessos</b>",
        "garden_label": "Área Verde Hospitalar (m²):",
        "wash_ext_label": "Lavagem ambulâncias / acessos (L/sem):",
        "default_residents": 40,
        "shower_count": 1.0, "shower_time": 8.0, "shower_flow": 9.0,
        "sink_liters": 65.5,
        "toilet_flushes": 5.0, "toilet_type_idx": 0,  # 6 L
        "wash_cycles": 46.0, "wash_vol": 500.0,
        "garden_area": 20.0, "garden_rate_idx": 0,     # 3.0 L/m²/dia
        "wash_external": 50.0,
        "irr_rain_thresh": 2.0, "irr_potable_backup": True,
    },
]


class TabBuilding(QWidget):
    building_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.daily_custom_series = None
        self._updating_tables = False
        self._updating_shares = False
        self.init_ui()

    def init_ui(self):
        self._updating_tables = True
        self._updating_shares = True

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
        card_bg = "#27272a" if is_dark else "#ffffff"
        card_border = "#3f3f46" if is_dark else "#cbd5e1"

        # Título
        lbl_title = QLabel(tr("Edificação, ocupação e demanda de água"))
        lbl_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 28px; font-weight: 700; color: #133c32;")
        layout.addWidget(lbl_title)

        # ── GroupBox 1: Área de Captação & Coeficiente de Escoamento ──
        gb_roof = QGroupBox(tr("Área de Captação & Coeficiente de Escoamento (Runoff)"))
        gb_roof.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        grid_r = QGridLayout()
        grid_r.setSpacing(10)

        grid_r.addWidget(QLabel(tr("Área de Captação (m²):")), 0, 0)
        self.txt_area = QLineEdit("")
        self.txt_area.setPlaceholderText(tr("Ex: 100"))
        self.txt_area.textChanged.connect(self.on_area_changed)
        grid_r.addWidget(self.txt_area, 0, 1)

        grid_r.addWidget(QLabel(tr("Material da Cobertura / Coeficiente de Escoamento (C):")), 0, 2)
        row_runoff = QHBoxLayout()
        self.combo_runoff = QComboBox()
        self.combo_runoff.addItem(tr("Telha Cerâmica (0,75)"), 0.75)
        self.combo_runoff.addItem(tr("Telha Metálica (0,88)"), 0.88)
        self.combo_runoff.addItem(tr("Telha de Cimento / Fibrocimento (0,73)"), 0.73)
        self.combo_runoff.addItem(tr("Telhados verdes (0,24)"), 0.24)
        self.combo_runoff.addItem(tr("Alumínio (0,70)"), 0.70)
        self.combo_runoff.addItem(tr("Plástico / Policarbonato (0,94)"), 0.94)
        self.combo_runoff.addItem(tr("Concreto Asfáltico (0,90)"), 0.90)
        self.combo_runoff.addItem(tr("Aço Galvanizado (0,92)"), 0.92)
        self.combo_runoff.addItem(tr("Outro / Personalizado..."), -1.0)
        self.combo_runoff.setCurrentIndex(0)

        self.txt_custom_runoff = QLineEdit("")
        self.txt_custom_runoff.setFixedWidth(80)
        self.txt_custom_runoff.setPlaceholderText("ex: 0,75")
        self.txt_custom_runoff.hide()
        self.txt_custom_runoff.textChanged.connect(lambda: self.building_updated.emit())

        self.combo_runoff.currentIndexChanged.connect(self.on_runoff_changed)
        row_runoff.addWidget(self.combo_runoff, stretch=2)
        row_runoff.addWidget(self.txt_custom_runoff, stretch=1)
        grid_r.addLayout(row_runoff, 0, 3)

        grid_r.addWidget(QLabel(tr("Economias (Micromedição):")), 1, 0)
        self.txt_economias = QLineEdit("")
        self.txt_economias.setPlaceholderText(tr("Ex: 1"))
        self.txt_economias.textChanged.connect(lambda: self.building_updated.emit())
        grid_r.addWidget(self.txt_economias, 1, 1)

        lbl_micromed_note = QLabel(tr("💡 Para edifícios ou condomínios com hidrômetros individualizados, informe o nº de apartamentos/economias para cálculo correto das faixas tarifárias."))
        lbl_micromed_note.setStyleSheet(f"font-size: 10.5px; color: {muted_color};")
        grid_r.addWidget(lbl_micromed_note, 1, 2, 1, 2)

        gb_roof.setLayout(grid_r)
        layout.addWidget(gb_roof)

        # ── GroupBox 2: Modulação do Consumo de Água (Sub-Abas) ──
        gb_demand = QGroupBox(tr("💧 Parâmetros de Consumo & Modulação da Demanda"))
        gb_demand.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_demand = QVBoxLayout(gb_demand)
        lay_demand.setSpacing(8)

        self.tab_demand_mode = QTabWidget()
        self.tab_demand_mode.setStyleSheet("""
            QTabBar::tab {
                font-weight: bold;
                font-size: 11.5px;
                padding: 6px 12px;
                min-width: 90px;
            }
        """)

        # ══════════════════════════════════════════════════════════════════════════
        # ── ABA 0: DEMANDA DIÁRIA SIMPLIFICADA (VALOR CONSTANTE) ──
        # ══════════════════════════════════════════════════════════════════════════
        tab_simple = QWidget()
        lay_s = QVBoxLayout(tab_simple)
        lay_s.setContentsMargins(10, 10, 10, 10)
        lay_s.setSpacing(12)

        # Bloco de Entradas Simplificadas
        gb_s_inputs = QGroupBox(tr("Consumo Básico da Edificação (Modo Simplificado)"))
        lay_sin = QGridLayout(gb_s_inputs)
        lay_sin.setSpacing(10)

        # Linha 0: Consumo Interno (por habitante) e Número de Moradores
        self.lbl_demand_title = QLabel(f"<b>{tr('Consumo Interno Per Capita (L/hab/dia):')}</b>")
        lay_sin.addWidget(self.lbl_demand_title, 0, 0)
        self.txt_demand = QLineEdit("")
        self.txt_demand.setPlaceholderText(tr("Ex: 150"))
        self.txt_demand.textChanged.connect(self.on_base_demand_changed)
        lay_sin.addWidget(self.txt_demand, 0, 1)

        self.lbl_residents_title = QLabel(f"<b>{tr('Número de Moradores / Ocupantes:')}</b>")
        lay_sin.addWidget(self.lbl_residents_title, 0, 2)
        self.txt_residents = QLineEdit("")
        self.txt_residents.setPlaceholderText(tr("Ex: 4"))
        self.txt_residents.textChanged.connect(self.on_base_residents_changed)
        lay_sin.addWidget(self.txt_residents, 0, 3)

        # Linha 1: Partição Interna (Potável vs Não-Potável)
        lay_sin.addWidget(QLabel(f"<b>{tr('Consumo Interno Potável (%):')}</b>"), 1, 0)
        self.txt_potable_indoor_share_simple = QLineEdit("65")
        self.txt_potable_indoor_share_simple.setPlaceholderText(tr("Ex: 65"))
        self.txt_potable_indoor_share_simple.setToolTip(tr("Percentual do consumo interno que exige água potável (chuveiro, pias, cozinha)."))
        self.txt_potable_indoor_share_simple.textChanged.connect(self._on_potable_share_simple_changed)
        lay_sin.addWidget(self.txt_potable_indoor_share_simple, 1, 1)

        lay_sin.addWidget(QLabel(f"<b>{tr('Consumo Interno Não-Potável (%):')}</b>"), 1, 2)
        self.txt_non_potable_indoor_share_simple = QLineEdit("35")
        self.txt_non_potable_indoor_share_simple.setPlaceholderText(tr("Ex: 35"))
        self.txt_non_potable_indoor_share_simple.setToolTip(tr("Percentual do consumo interno passível de substituição (descarga de vasos sanitários, máquina de lavar)."))
        self.txt_non_potable_indoor_share_simple.textChanged.connect(self._on_non_potable_share_simple_changed)
        lay_sin.addWidget(self.txt_non_potable_indoor_share_simple, 1, 3)

        # Linha 2: Consumo Externo Fixo (L/dia) e Substituição Global por Chuva
        lbl_ext = QLabel(f"<b>{tr('Consumo Externo Fixo (L/dia):')}</b>")
        lbl_ext.setToolTip(tr("Demanda externa diária total fixa (ex: irrigação de jardim, lavagem de calçadas). Não depende do número de habitantes."))
        lay_sin.addWidget(lbl_ext, 2, 0)
        self.txt_external_demand_l_day = QLineEdit("0")
        self.txt_external_demand_l_day.setPlaceholderText(tr("Ex: 100"))
        self.txt_external_demand_l_day.setToolTip(tr("Consumo externo total em litros por dia (não é calculado por habitante)."))
        self.txt_external_demand_l_day.textChanged.connect(self._on_external_demand_simple_changed)
        lay_sin.addWidget(self.txt_external_demand_l_day, 2, 1)

        lay_sin.addWidget(QLabel(f"<b>{tr('Substituição por Água de Chuva (%):')}</b>"), 2, 2)
        self.txt_share = QLineEdit("")
        self.txt_share.setPlaceholderText(tr("Ex: 40"))
        self.txt_share.setToolTip(tr("Fração total da demanda que a chuva pode atender. É calculada a partir da fração não potável interna e da demanda externa, e não se edita diretamente."))
        # A total é derivada: editá-la aqui mudava só os rótulos, e a simulação
        # seguia com a fração interna. Ver triton/core/fracao_atendivel.py.
        self.txt_share.setReadOnly(True)
        self.txt_share.textChanged.connect(self.on_base_share_changed)
        lay_sin.addWidget(self.txt_share, 2, 3)

        # Card de Resumo Imediato
        self.card_simple_summary = QFrame()
        self.card_simple_summary.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        lay_css = QHBoxLayout(self.card_simple_summary)
        lay_css.setContentsMargins(6, 4, 6, 4)

        self.lbl_simple_tot_demand = QLabel()
        self.lbl_simple_tot_demand.setStyleSheet(f"font-size: 11.5px; font-weight: bold; color: {text_color}; background-color: transparent;")
        self.lbl_simple_month_vol = QLabel()
        self.lbl_simple_month_vol.setStyleSheet(f"font-size: 11.5px; font-weight: bold; color: {text_color}; background-color: transparent;")
        self.lbl_simple_pluvial_demand = QLabel()
        self.lbl_simple_pluvial_demand.setStyleSheet("font-size: 11.5px; font-weight: bold; color: #10b981; background-color: transparent;")

        lay_css.addWidget(self.lbl_simple_tot_demand, stretch=1)
        lay_css.addWidget(self.lbl_simple_month_vol, stretch=1)
        lay_css.addWidget(self.lbl_simple_pluvial_demand, stretch=1)
        lay_sin.addWidget(self.card_simple_summary, 3, 0, 1, 4)

        lay_s.addWidget(gb_s_inputs)

        # Banner Convidativo de Atalho para o Modo Avançado
        banner_advanced_invite = QFrame()
        banner_advanced_invite.setStyleSheet(f"""
            QFrame {{
                background-color: {'#1e293b' if is_dark else '#eff6ff'};
                border: 1px solid {'#3b82f6' if is_dark else '#bfdbfe'};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)
        lay_bai = QHBoxLayout(banner_advanced_invite)
        lay_bai.setContentsMargins(6, 4, 6, 4)

        lbl_bai_text = QLabel(tr(
            "💡 <b>Deseja estimar por aparelhos hidráulicos (bacias, chuveiros, máquinas) ou irrigação de jardim?</b><br>"
            "Acesse a aba <b>'🧮 Detalhamento Avançado de Usos'</b> ao lado para escolher um template base (residencial, comercial, etc.) e ajustar livremente."
        ))
        lbl_bai_text.setWordWrap(True)
        lbl_bai_text.setStyleSheet(f"font-size: 11px; color: {'#93c5fd' if is_dark else '#1e40af'};")
        lay_bai.addWidget(lbl_bai_text, stretch=1)

        btn_go_advanced = QPushButton(tr("🧮 Abrir Detalhamento Avançado →"))
        btn_go_advanced.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; font-size: 11px; padding: 6px 12px; border-radius: 4px;")
        btn_go_advanced.clicked.connect(lambda: self.tab_demand_mode.setCurrentIndex(1))
        lay_bai.addWidget(btn_go_advanced)

        lay_s.addWidget(banner_advanced_invite)
        lay_s.addStretch()
        self.tab_demand_mode.addTab(tab_simple, tr("💧 Demanda Diária Simplificada"))

        # ══════════════════════════════════════════════════════════════════════════
        # ── ABA 1: DETALHAMENTO AVANÇADO DE USOS (MODELO UNIFICADO DE TEMPLATES) ──
        # ══════════════════════════════════════════════════════════════════════════
        tab_advanced = QWidget()
        lay_adv = QVBoxLayout(tab_advanced)
        lay_adv.setContentsMargins(10, 10, 10, 10)
        lay_adv.setSpacing(10)

        # Campos de controle de partição mantidos para sincronização e compatibilidade
        self.txt_potable_indoor_share = QLineEdit("")
        self.txt_potable_indoor_share.setPlaceholderText(tr("Ex: 65"))
        self.txt_potable_indoor_share.textChanged.connect(self._on_potable_indoor_changed)
        self.txt_non_potable_indoor_share = QLineEdit("")
        self.txt_non_potable_indoor_share.setPlaceholderText(tr("Ex: 35"))
        self.txt_non_potable_indoor_share.textChanged.connect(self._on_non_potable_indoor_changed)
        self.txt_irrigation_l_day = QLineEdit("")
        self.txt_irrigation_l_day.setPlaceholderText(tr("Ex: 50"))
        self.txt_irrigation_l_day.textChanged.connect(self._on_irrigation_changed)

        # ── 1. Seletor Unificado de Tipologia / Template ──
        gb_tpl = QGroupBox(tr(titulo_tipologia()))
        gb_tpl.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_tpl = QVBoxLayout(gb_tpl)
        lay_tpl.setSpacing(8)

        row_tpl_select = QHBoxLayout()
        row_tpl_select.addWidget(QLabel(f"<b>{tr('Selecione o Modelo Base:')}</b>"))
        self.combo_building_template = QComboBox()
        for tpl in BUILDING_TEMPLATES:
            self.combo_building_template.addItem(tr(tpl["name"]), tpl["id"])
        self.combo_building_template.addItem(tr("⚙️ Personalizado (Configuração sob medida do usuário)"), "custom")
        self.combo_building_template.setCurrentIndex(0)
        self.combo_building_template.currentIndexChanged.connect(self._on_template_combo_changed)
        row_tpl_select.addWidget(self.combo_building_template, stretch=1)
        lay_tpl.addLayout(row_tpl_select)
        lay_adv.addWidget(gb_tpl)

        # ── 2. Painel de Aparelhos Hidráulicos e Usos (3 Colunas) ──
        gb_fixtures = QGroupBox(tr("🧮 Aparelhos Hidráulicos & Parâmetros de Uso (Ajuste Conforme o Projeto)"))
        gb_fixtures.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_fix_main = QVBoxLayout(gb_fixtures)
        lay_fix_main.setSpacing(8)

        row_cards = QHBoxLayout()
        row_cards.setSpacing(10)

        # Coluna 1: Usos Potáveis Internos
        card_in_pot = QFrame()
        card_in_pot.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 6px; padding: 8px; }}")
        lay_card_in_pot = QVBoxLayout(card_in_pot)
        lay_card_in_pot.setSpacing(6)

        self.lbl_cin_pot_title = QLabel(tr("<b>🚿 Usos Potáveis Internos (por Morador)</b>"))
        self.lbl_cin_pot_title.setStyleSheet(f"color: {heading_color}; font-size: 11.5px;")
        lay_card_in_pot.addWidget(self.lbl_cin_pot_title)

        grid_cin_pot = QGridLayout()
        grid_cin_pot.setSpacing(6)

        grid_cin_pot.addWidget(QLabel(tr("Banhos / dia:")), 0, 0)
        self.sp_shower_count = QDoubleSpinBox()
        self.sp_shower_count.setRange(0.0, 10.0); self.sp_shower_count.setValue(1.0); self.sp_shower_count.setSingleStep(0.5)
        self.sp_shower_count.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_pot.addWidget(self.sp_shower_count, 0, 1)

        grid_cin_pot.addWidget(QLabel(tr("Duração banho (min):")), 1, 0)
        self.sp_shower_time = QDoubleSpinBox()
        self.sp_shower_time.setRange(0.0, 60.0); self.sp_shower_time.setValue(8.0); self.sp_shower_time.setSingleStep(1.0)
        self.sp_shower_time.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_pot.addWidget(self.sp_shower_time, 1, 1)

        grid_cin_pot.addWidget(QLabel(tr("Vazão ducha (L/min):")), 2, 0)
        self.sp_shower_flow = QDoubleSpinBox()
        self.sp_shower_flow.setRange(0.0, 35.0); self.sp_shower_flow.setValue(9.0); self.sp_shower_flow.setSingleStep(0.5)
        self.sp_shower_flow.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_pot.addWidget(self.sp_shower_flow, 2, 1)

        self.lbl_sp_sink_title = QLabel(tr("Pias & Cozinha (L/hab/dia):"))
        grid_cin_pot.addWidget(self.lbl_sp_sink_title, 3, 0)
        self.sp_sink_liters = QDoubleSpinBox()
        self.sp_sink_liters.setRange(0.0, 250.0); self.sp_sink_liters.setValue(26.0); self.sp_sink_liters.setSingleStep(2.0)
        self.sp_sink_liters.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_pot.addWidget(self.sp_sink_liters, 3, 1)

        lay_card_in_pot.addLayout(grid_cin_pot)
        lay_card_in_pot.addStretch()

        self.lbl_subtot_potable = QLabel()
        self.lbl_subtot_potable.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {'#38bdf8' if is_dark else '#0284c7'}; padding: 4px 0;")
        lay_card_in_pot.addWidget(self.lbl_subtot_potable)

        row_cards.addWidget(card_in_pot, stretch=1)

        # Coluna 2: Usos Não-Potáveis Internos
        card_in_nonpot = QFrame()
        card_in_nonpot.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 6px; padding: 8px; }}")
        lay_card_in_nonpot = QVBoxLayout(card_in_nonpot)
        lay_card_in_nonpot.setSpacing(6)

        self.lbl_cin_nonpot_title = QLabel(tr("<b>🚽 Usos Não-Potáveis Internos (por Morador)</b>"))
        self.lbl_cin_nonpot_title.setStyleSheet(f"color: {heading_color}; font-size: 11.5px;")
        lay_card_in_nonpot.addWidget(self.lbl_cin_nonpot_title)

        grid_cin_nonpot = QGridLayout()
        grid_cin_nonpot.setSpacing(6)

        grid_cin_nonpot.addWidget(QLabel(tr("Descargas bacia / dia:")), 0, 0)
        self.sp_toilet_flushes = QDoubleSpinBox()
        self.sp_toilet_flushes.setRange(0.0, 20.0); self.sp_toilet_flushes.setValue(4.0); self.sp_toilet_flushes.setSingleStep(1.0)
        self.sp_toilet_flushes.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_nonpot.addWidget(self.sp_toilet_flushes, 0, 1)

        grid_cin_nonpot.addWidget(QLabel(tr("Tipo de Bacia Sanitária:")), 1, 0)
        self.combo_toilet_vol = QComboBox()
        self.combo_toilet_vol.addItem(tr("Caixa Acoplada (6 L)"), 6.0)
        self.combo_toilet_vol.addItem(tr("Duplo Fluxo 3/6L (4,5 L)"), 4.5)
        self.combo_toilet_vol.addItem(tr("Válvula Tradicional (12 L)"), 12.0)
        self.combo_toilet_vol.currentIndexChanged.connect(self._on_fixture_param_changed)
        grid_cin_nonpot.addWidget(self.combo_toilet_vol, 1, 1)

        self.lbl_sp_wash_cycles_title = QLabel(tr("Máquina de Lavar (ciclos/sem):"))
        grid_cin_nonpot.addWidget(self.lbl_sp_wash_cycles_title, 2, 0)
        self.sp_wash_cycles = QDoubleSpinBox()
        self.sp_wash_cycles.setRange(0.0, 50.0); self.sp_wash_cycles.setValue(3.0); self.sp_wash_cycles.setSingleStep(1.0)
        self.sp_wash_cycles.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_nonpot.addWidget(self.sp_wash_cycles, 2, 1)

        self.lbl_sp_wash_vol_title = QLabel(tr("Consumo máquina (L/ciclo):"))
        grid_cin_nonpot.addWidget(self.lbl_sp_wash_vol_title, 3, 0)
        self.sp_wash_vol = QDoubleSpinBox()
        self.sp_wash_vol.setRange(0.0, 500.0); self.sp_wash_vol.setValue(100.0); self.sp_wash_vol.setSingleStep(10.0)
        self.sp_wash_vol.valueChanged.connect(self._on_fixture_param_changed)
        grid_cin_nonpot.addWidget(self.sp_wash_vol, 3, 1)

        lay_card_in_nonpot.addLayout(grid_cin_nonpot)
        lay_card_in_nonpot.addStretch()

        self.lbl_subtot_non_potable = QLabel()
        self.lbl_subtot_non_potable.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {'#34d399' if is_dark else '#059669'}; padding: 4px 0;")
        lay_card_in_nonpot.addWidget(self.lbl_subtot_non_potable)

        row_cards.addWidget(card_in_nonpot, stretch=1)

        # Coluna 3: Usos Externos & Jardim
        card_out = QFrame()
        card_out.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 6px; padding: 8px; }}")
        lay_card_out = QVBoxLayout(card_out)
        lay_card_out.setSpacing(6)

        self.lbl_cout_title = QLabel(tr("<b>🌿 Jardim & Usos Externos</b>"))
        self.lbl_cout_title.setStyleSheet(f"color: {heading_color}; font-size: 11.5px;")
        lay_card_out.addWidget(self.lbl_cout_title)

        grid_cout = QGridLayout()
        grid_cout.setSpacing(6)

        self.lbl_sp_garden_title = QLabel(tr("Área de Jardim (m²):"))
        grid_cout.addWidget(self.lbl_sp_garden_title, 0, 0)
        self.sp_garden_area = QDoubleSpinBox()
        self.sp_garden_area.setRange(0.0, 5000.0); self.sp_garden_area.setValue(15.0); self.sp_garden_area.setSingleStep(5.0)
        self.sp_garden_area.valueChanged.connect(self._on_fixture_param_changed)
        grid_cout.addWidget(self.sp_garden_area, 0, 1)

        grid_cout.addWidget(QLabel(tr("Taxa de Rega Diária:")), 1, 0)
        self.combo_garden_rate = QComboBox()
        self.combo_garden_rate.addItem(tr("Gramado / Geral (3,0 L/m²/dia)"), 3.0)
        self.combo_garden_rate.addItem(tr("Jardim Denso (4,0 L/m²/dia)"), 4.0)
        self.combo_garden_rate.addItem(tr("Plantas Baixo Consumo (1,5 L/m²/dia)"), 1.5)
        self.combo_garden_rate.addItem(tr("Sem Rega (0,0 L/m²/dia)"), 0.0)
        self.combo_garden_rate.currentIndexChanged.connect(self._on_fixture_param_changed)
        grid_cout.addWidget(self.combo_garden_rate, 1, 1)

        self.lbl_sp_wash_ext_title = QLabel(tr("Lavagem piso/carro (L/sem):"))
        grid_cout.addWidget(self.lbl_sp_wash_ext_title, 2, 0)
        self.sp_wash_external = QDoubleSpinBox()
        self.sp_wash_external.setRange(0.0, 2000.0); self.sp_wash_external.setValue(35.0); self.sp_wash_external.setSingleStep(10.0)
        self.sp_wash_external.valueChanged.connect(self._on_fixture_param_changed)
        grid_cout.addWidget(self.sp_wash_external, 2, 1)

        grid_cout.addWidget(QLabel(tr("Limiar Chuva Rega (mm/dia):")), 3, 0)
        self.txt_irr_rain_threshold = QLineEdit("")
        self.txt_irr_rain_threshold.setPlaceholderText(tr("Ex: 2,0"))
        self.txt_irr_rain_threshold.setToolTip(tr("Precipitação diária a partir da qual a irrigação é 100% dispensada."))
        self.txt_irr_rain_threshold.textChanged.connect(self._on_fixture_param_changed)
        grid_cout.addWidget(self.txt_irr_rain_threshold, 3, 1)

        lay_card_out.addLayout(grid_cout)

        self.chk_irr_potable_backup = QCheckBox(tr("Permitir backup potável se pluvial secar"))
        self.chk_irr_potable_backup.setChecked(True)
        self.chk_irr_potable_backup.setStyleSheet(f"font-size: 10.5px; color: {text_color};")
        self.chk_irr_potable_backup.toggled.connect(lambda: self.building_updated.emit())
        lay_card_out.addWidget(self.chk_irr_potable_backup)

        self.lbl_subtot_outdoor = QLabel()
        self.lbl_subtot_outdoor.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {'#fbbf24' if is_dark else '#d97706'}; padding: 4px 0;")
        lay_card_out.addWidget(self.lbl_subtot_outdoor)

        row_cards.addWidget(card_out, stretch=1)
        lay_fix_main.addLayout(row_cards)
        lay_adv.addWidget(gb_fixtures)

        # ── 3. Balanço Hídrico & Sincronização em Tempo Real ──
        gb_summary = QGroupBox(tr("📊 Balanço Hídrico Consolidado & Sincronização"))
        gb_summary.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading_color}; }}")
        lay_sum = QVBoxLayout(gb_summary)
        lay_sum.setSpacing(6)

        self.lbl_discretized_balance = QLabel()
        self.lbl_discretized_balance.setWordWrap(True)
        self.lbl_discretized_balance.setStyleSheet(f"font-size: 11px; color: {text_color}; background-color: {card_bg}; border: 1px solid {card_border}; border-radius: 4px; padding: 8px 12px;")
        lay_sum.addWidget(self.lbl_discretized_balance)

        row_sync = QHBoxLayout()
        self.lbl_sync_indicator = QLabel(tr("✅ Demanda e partição sincronizadas em tempo real com o edifício"))
        self.lbl_sync_indicator.setStyleSheet("font-size: 11px; font-weight: bold; color: #16a34a;")
        row_sync.addWidget(self.lbl_sync_indicator)
        row_sync.addStretch()

        btn_sync_now = QPushButton(tr("🔄 Forçar Re-sincronização"))
        btn_sync_now.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; font-size: 10.5px; padding: 4px 10px; border-radius: 4px;")
        btn_sync_now.clicked.connect(self._force_sync_to_project)
        row_sync.addWidget(btn_sync_now)
        lay_sum.addLayout(row_sync)

        lay_adv.addWidget(gb_summary)
        lay_adv.addStretch()
        self.tab_demand_mode.addTab(tab_advanced, tr("🧮 Detalhamento Avançado de Usos"))

        # ══════════════════════════════════════════════════════════════════════════
        # ── ABA 2: VARIAÇÃO SEMANAL (POR DIA DA SEMANA) ──
        # ══════════════════════════════════════════════════════════════════════════
        tab_week = QWidget()
        lay_w = QVBoxLayout(tab_week)
        lay_w.setContentsMargins(8, 8, 8, 8)
        lay_w.setSpacing(6)

        row_w_actions = QHBoxLayout()
        lbl_w_info = QLabel(tr("Defina o consumo interno e percentual não-potável para cada dia da semana:"))
        lbl_w_info.setStyleSheet(f"color: {muted_color}; font-size: 11px;")
        row_w_actions.addWidget(lbl_w_info)
        row_w_actions.addStretch()

        btn_fill_week = QPushButton(tr("⚡ Preencher com valores do modo constante"))
        btn_fill_week.setStyleSheet("padding: 3px 8px; font-size: 11px; font-weight: bold;")
        btn_fill_week.clicked.connect(self._fill_weekly_from_constant)
        row_w_actions.addWidget(btn_fill_week)
        lay_w.addLayout(row_w_actions)

        self.table_weekly = QTableWidget(7, 5)
        self.table_weekly.setHorizontalHeaderLabels([
            tr("Dia da Semana"), tr("Consumo Interno (L/hab/dia)"), tr("Habitantes"),
            tr("Não-Potável Interno (%)"), tr("Demanda Não-Potável (L/dia)")
        ])
        self.table_weekly.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_weekly.verticalHeader().setVisible(False)
        self.table_weekly.verticalHeader().setDefaultSectionSize(26)
        self.table_weekly.setFixedHeight(215)
        self.table_weekly.setStyleSheet("QTableWidget { font-size: 11.5px; } QHeaderView::section { font-weight: bold; font-size: 11px; padding: 2px; }")
        self.table_weekly.cellChanged.connect(self._on_weekly_cell_changed)

        days_pt = [
            tr("Segunda-feira"), tr("Terça-feira"), tr("Quarta-feira"),
            tr("Quinta-feira"), tr("Sexta-feira"), tr("Sábado"), tr("Domingo")
        ]
        for r_idx, day_name in enumerate(days_pt):
            it_name = QTableWidgetItem(day_name)
            it_name.setFlags(it_name.flags() & ~Qt.ItemIsEditable)
            it_name.setTextAlignment(Qt.AlignCenter)
            self.table_weekly.setItem(r_idx, 0, it_name)
            self.table_weekly.setItem(r_idx, 1, QTableWidgetItem("-"))
            self.table_weekly.setItem(r_idx, 2, QTableWidgetItem("-"))
            self.table_weekly.setItem(r_idx, 3, QTableWidgetItem("-"))
            it_calc = QTableWidgetItem("-")
            it_calc.setFlags(it_calc.flags() & ~Qt.ItemIsEditable)
            it_calc.setTextAlignment(Qt.AlignCenter)
            self.table_weekly.setItem(r_idx, 4, it_calc)

        lay_w.addWidget(self.table_weekly)
        self.tab_demand_mode.addTab(tab_week, tr("📅 Variação Semanal"))

        # ══════════════════════════════════════════════════════════════════════════
        # ── ABA 3: VARIAÇÃO MENSAL (SAZONALIDADE) ──
        # ══════════════════════════════════════════════════════════════════════════
        tab_month = QWidget()
        lay_m = QVBoxLayout(tab_month)
        lay_m.setContentsMargins(8, 8, 8, 8)
        lay_m.setSpacing(6)

        row_m_actions = QHBoxLayout()
        lbl_m_info = QLabel(tr("Defina a variação mensal de consumo interno, ocupantes e percentual não-potável:"))
        lbl_m_info.setStyleSheet(f"color: {muted_color}; font-size: 11px;")
        row_m_actions.addWidget(lbl_m_info)
        row_m_actions.addStretch()

        btn_fill_month = QPushButton(tr("⚡ Preencher com valores do modo constante"))
        btn_fill_month.setStyleSheet("padding: 3px 8px; font-size: 11px; font-weight: bold;")
        btn_fill_month.clicked.connect(self._fill_monthly_from_constant)
        row_m_actions.addWidget(btn_fill_month)
        lay_m.addLayout(row_m_actions)

        self.table_monthly = QTableWidget(12, 5)
        self.table_monthly.setHorizontalHeaderLabels([
            tr("Mês"), tr("Consumo Interno (L/hab/dia)"), tr("Habitantes"),
            tr("Não-Potável Interno (%)"), tr("Demanda Não-Potável (L/dia)")
        ])
        self.table_monthly.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_monthly.verticalHeader().setVisible(False)
        self.table_monthly.verticalHeader().setDefaultSectionSize(24)
        self.table_monthly.setFixedHeight(330)
        self.table_monthly.setStyleSheet("QTableWidget { font-size: 11.5px; } QHeaderView::section { font-weight: bold; font-size: 11px; padding: 2px; }")
        self.table_monthly.cellChanged.connect(self._on_monthly_cell_changed)

        months_pt = [
            tr("Janeiro"), tr("Fevereiro"), tr("Março"), tr("Abril"), tr("Maio"), tr("Junho"),
            tr("Julho"), tr("Agosto"), tr("Setembro"), tr("Outubro"), tr("Novembro"), tr("Dezembro")
        ]
        for m_idx, m_name in enumerate(months_pt):
            it_name = QTableWidgetItem(m_name)
            it_name.setFlags(it_name.flags() & ~Qt.ItemIsEditable)
            it_name.setTextAlignment(Qt.AlignCenter)
            self.table_monthly.setItem(m_idx, 0, it_name)
            self.table_monthly.setItem(m_idx, 1, QTableWidgetItem("-"))
            self.table_monthly.setItem(m_idx, 2, QTableWidgetItem("-"))
            self.table_monthly.setItem(m_idx, 3, QTableWidgetItem("-"))
            it_calc = QTableWidgetItem("-")
            it_calc.setFlags(it_calc.flags() & ~Qt.ItemIsEditable)
            it_calc.setTextAlignment(Qt.AlignCenter)
            self.table_monthly.setItem(m_idx, 4, it_calc)

        lay_m.addWidget(self.table_monthly)
        self.tab_demand_mode.addTab(tab_month, tr("🗓️ Variação Mensal"))

        # ══════════════════════════════════════════════════════════════════════════
        # ── ABA 4: VARIAÇÃO TOTAL (SÉRIE TEMPORAL DIÁRIA) ──
        # ══════════════════════════════════════════════════════════════════════════
        tab_daily = QWidget()
        lay_d = QVBoxLayout(tab_daily)
        lay_d.setContentsMargins(10, 10, 10, 10)
        lay_d.setSpacing(10)

        lbl_daily_desc = QLabel(tr(
            "Permite importar uma série temporal diária completa personalizada. "
            "Baixe a planilha modelo contendo o número exato de dias simulados, "
            "preencha os valores de cada dia e importe o arquivo de volta no Triton."
        ))
        lbl_daily_desc.setWordWrap(True)
        lbl_daily_desc.setStyleSheet(f"color: {muted_color}; font-size: 11px;")
        lay_d.addWidget(lbl_daily_desc)

        row_daily_btns = QHBoxLayout()
        self.btn_download_template = QPushButton(tr("📥 Baixar Planilha Modelo (Template CSV / Excel)..."))
        self.btn_download_template.setStyleSheet("font-weight: bold; background-color: #0284c7; color: white; padding: 7px 14px; border-radius: 4px;")
        self.btn_download_template.clicked.connect(self.on_download_daily_template)
        row_daily_btns.addWidget(self.btn_download_template)

        self.btn_import_daily = QPushButton(tr("📂 Importar Planilha de Consumo Diário..."))
        self.btn_import_daily.setStyleSheet("font-weight: bold; background-color: #059669; color: white; padding: 7px 14px; border-radius: 4px;")
        self.btn_import_daily.clicked.connect(self.on_import_daily_series)
        row_daily_btns.addWidget(self.btn_import_daily)
        row_daily_btns.addStretch()
        lay_d.addLayout(row_daily_btns)

        self.lbl_daily_status = QLabel(tr("Nenhuma série diária importada. Clique acima para baixar o template ou importar."))
        self.lbl_daily_status.setStyleSheet("font-weight: bold; color: #d97706; padding: 4px 0;")
        lay_d.addWidget(self.lbl_daily_status)

        self.table_daily_preview = QTableWidget(0, 5)
        self.table_daily_preview.setHorizontalHeaderLabels([
            tr("Dia / Data"), tr("Consumo Interno (L/hab/dia)"), tr("Habitantes"),
            tr("Não-Potável Interno (%)"), tr("Demanda Não-Potável (L/dia)")
        ])
        self.table_daily_preview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_daily_preview.verticalHeader().setDefaultSectionSize(30)
        self.table_daily_preview.setFixedHeight(300)
        self.table_daily_preview.setStyleSheet("QTableWidget { font-size: 12px; } QHeaderView::section { font-weight: bold; font-size: 11px; padding: 4px; }")
        self.table_daily_preview.setEditTriggers(QTableWidget.NoEditTriggers)
        lay_d.addWidget(self.table_daily_preview)

        self.tab_demand_mode.addTab(tab_daily, tr("📊 Variação Total Diária"))

        self.tab_pages = [tab_simple, tab_advanced, tab_week, tab_month, tab_daily]
        for i, page in enumerate(self.tab_pages):
            if i == 0:
                page.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            else:
                page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.tab_demand_mode.currentChanged.connect(self._on_demand_mode_changed)
        lay_demand.addWidget(self.tab_demand_mode)

        # ── BANNER INFORMATIVO RESUMO DA DEMANDA ──
        banner_dem = QFrame()
        banner_dem.setStyleSheet(f"""
            QFrame {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 6px;
                padding: 6px 10px;
            }}
        """)
        lay_bd = QHBoxLayout(banner_dem)
        lay_bd.setContentsMargins(4, 4, 4, 4)

        self.lbl_tot_pluvial = QLabel(tr("Demanda Pluvial Calculada: -- L/dia"))
        self.lbl_tot_pluvial.setStyleSheet(f"font-weight: bold; color: {'#38bdf8' if is_dark else '#0284c7'}; font-size: 11.5px;")
        lay_bd.addWidget(self.lbl_tot_pluvial)
        lay_bd.addStretch()

        self.lbl_mode_summary = QLabel(tr("Modo ativo: Demanda Diária Simplificada"))
        self.lbl_mode_summary.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {heading_color};")
        lay_bd.addWidget(self.lbl_mode_summary)

        lay_demand.addWidget(banner_dem)
        layout.addWidget(gb_demand)
        layout.addStretch()

        scroll.setWidget(content_widget)
        main_vbox.addWidget(scroll)

        # Validações e inicializações finais
        self._updating_tables = False
        self._updating_shares = False
        self.check_input_highlight(self.txt_area)
        self.check_input_highlight(self.txt_demand)
        self.check_input_highlight(self.txt_residents)
        self.check_input_highlight(self.txt_potable_indoor_share)
        self.check_input_highlight(self.txt_non_potable_indoor_share)
        self.check_input_highlight(self.txt_irrigation_l_day)
        self.check_input_highlight(self.txt_share)
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()

    #: Campos que a tela pede em percentual. Cada um ganha a nota da unidade na
    #: dica, e fica laranja quando recebe um valor entre 0 e 1, que costuma ser
    #: a fração digitada no lugar do percentual.
    _CAMPOS_PERCENTUAIS = ("txt_share", "txt_potable_indoor_share_simple",
                           "txt_non_potable_indoor_share_simple",
                           "txt_potable_indoor_share", "txt_non_potable_indoor_share")

    def _assinalar_percentual(self, line_edit, val):
        """Nota da unidade na dica; devolve o aviso, se o valor parecer fração."""
        if not any(getattr(self, nome, None) is line_edit for nome in self._CAMPOS_PERCENTUAIS):
            return None
        dica = line_edit.property("dica_percentual")
        if dica is None:
            base = line_edit.toolTip()
            nota = tr("Em percentual, de 0 a 100: 40 significa 40%.")
            dica = f"{base}\n{nota}" if base else nota
            line_edit.setProperty("dica_percentual", dica)
        aviso = aviso_percentual_pequeno(parse_float(val, None), get_current_lang()) if val else None
        line_edit.setToolTip(dica + (f"\n⚠ {aviso}" if aviso else ""))
        return aviso

    def _assinalar_celula_percentual(self, tabela, row):
        """A mesma marcação na coluna de percentual das tabelas de calendário."""
        item = tabela.item(row, 3)
        if item is None:
            return
        aviso = aviso_percentual_pequeno(parse_float(item.text(), None), get_current_lang())
        tabela.blockSignals(True)
        try:
            item.setToolTip(tr("Em percentual, de 0 a 100: 40 significa 40%.") + (f"\n⚠ {aviso}" if aviso else ""))
            item.setBackground(QColor("#fed7aa") if aviso else QColor(0, 0, 0, 0))
        finally:
            tabela.blockSignals(False)

    def check_input_highlight(self, line_edit):
        val = line_edit.text().strip()
        is_dark = get_current_theme() == "dark"
        aviso = self._assinalar_percentual(line_edit, val)
        if not val or val == "-" or not self.is_valid_number(val):
            line_edit.setStyleSheet(
                "QLineEdit { background-color: #713f12; border: 1.5px solid #eab308; color: #fef9c3; }"
                if is_dark else
                "QLineEdit { background-color: #fef08a; border: 1.5px solid #eab308; color: #1e293b; }"
            )
        elif aviso:
            line_edit.setStyleSheet(
                "QLineEdit { background-color: #7c2d12; border: 1.5px solid #fb923c; color: #ffedd5; }"
                if is_dark else
                "QLineEdit { background-color: #ffedd5; border: 1.5px solid #f97316; color: #1e293b; }"
            )
        else:
            line_edit.setStyleSheet(
                "QLineEdit { background-color: #18181b; border: 1px solid #3f3f46; color: #ffffff; }"
                if is_dark else
                "QLineEdit { background-color: #ffffff; border: 1px solid #cbd5e1; color: #1e293b; }"
            )

    def is_valid_number(self, val_str):
        try:
            return float(val_str.replace(',', '.')) >= 0
        except ValueError:
            return False

    def on_area_changed(self):
        self.check_input_highlight(self.txt_area)
        self.building_updated.emit()

    def on_base_share_changed(self):
        self.check_input_highlight(self.txt_share)
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def on_base_demand_changed(self):
        self.check_input_highlight(self.txt_demand)
        if hasattr(self, "tab_demand_mode") and self.tab_demand_mode.currentIndex() != 0:
            self._sync_consolidated_share()
        else:
            self._sync_simple_pluvial_share()
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def on_base_residents_changed(self):
        self.check_input_highlight(self.txt_residents)
        if hasattr(self, "tab_demand_mode") and self.tab_demand_mode.currentIndex() != 0:
            self._recalc_unified_balance(sync_to_base=False)
            self._sync_consolidated_share()
        else:
            self._sync_simple_pluvial_share()
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _update_contextual_labels(self, tpl: dict):
        if not tpl:
            return

        # Aba 0: Rótulo de Ocupantes e Demanda
        if hasattr(self, "lbl_residents_title"):
            self.lbl_residents_title.setText(f"<b>{tr(tpl.get('occupant_label', 'Número de Moradores / Ocupantes:'))}</b>")
        if hasattr(self, "lbl_demand_title"):
            self.lbl_demand_title.setText(f"<b>{tr(tpl.get('demand_label', 'Consumo Per Capita (L/hab/dia):'))}</b>")

        # Aba 1 - Card 1 (Potável)
        if hasattr(self, "lbl_cin_pot_title"):
            self.lbl_cin_pot_title.setText(tr(tpl.get('potable_title', "<b>🚿 Usos Potáveis Internos</b>")))
        if hasattr(self, "lbl_sp_sink_title"):
            self.lbl_sp_sink_title.setText(tr(tpl.get('sink_label', "Pias & Cozinha (L/hab/dia):")))

        # Aba 1 - Card 2 (Não-Potável)
        if hasattr(self, "lbl_cin_nonpot_title"):
            self.lbl_cin_nonpot_title.setText(tr(tpl.get('non_potable_title', "<b>🚽 Usos Não-Potáveis Internos</b>")))
        if hasattr(self, "lbl_sp_wash_cycles_title"):
            self.lbl_sp_wash_cycles_title.setText(tr(tpl.get('wash_cycles_label', "Máquina de Lavar (ciclos/sem):")))
        if hasattr(self, "lbl_sp_wash_vol_title"):
            self.lbl_sp_wash_vol_title.setText(tr(tpl.get('wash_vol_label', "Consumo máquina (L/ciclo):")))

        # Aba 1 - Card 3 (Externo)
        if hasattr(self, "lbl_cout_title"):
            self.lbl_cout_title.setText(tr(tpl.get('outdoor_title', "<b>🌿 Jardim & Usos Externos</b>")))
        if hasattr(self, "lbl_sp_garden_title"):
            self.lbl_sp_garden_title.setText(tr(tpl.get('garden_label', "Área de Jardim (m²):")))
        if hasattr(self, "lbl_sp_wash_ext_title"):
            self.lbl_sp_wash_ext_title.setText(tr(tpl.get('wash_ext_label', "Lavagem piso/carro (L/sem):")))

    def _on_template_combo_changed(self, idx: int):
        if self._updating_tables:
            return
        tpl_id = self.combo_building_template.itemData(idx)
        if not tpl_id or tpl_id == "custom":
            return
        # Localiza o template no catálogo
        tpl = next((t for t in BUILDING_TEMPLATES if t["id"] == tpl_id), None)
        if not tpl:
            return
        self._updating_tables = True
        try:
            self.sp_shower_count.setValue(tpl["shower_count"])
            self.sp_shower_time.setValue(tpl["shower_time"])
            self.sp_shower_flow.setValue(tpl["shower_flow"])
            self.sp_sink_liters.setValue(tpl["sink_liters"])
            self.sp_toilet_flushes.setValue(tpl["toilet_flushes"])
            self.combo_toilet_vol.setCurrentIndex(tpl["toilet_type_idx"])
            self.sp_wash_cycles.setValue(tpl["wash_cycles"])
            self.sp_wash_vol.setValue(tpl["wash_vol"])
            self.sp_garden_area.setValue(tpl["garden_area"])
            self.combo_garden_rate.setCurrentIndex(tpl["garden_rate_idx"])
            self.sp_wash_external.setValue(tpl["wash_external"])
            self.txt_irr_rain_threshold.setText(f"{tpl['irr_rain_thresh']:.1f}".replace('.', ','))
            self.chk_irr_potable_backup.setChecked(tpl["irr_potable_backup"])
            if "default_residents" in tpl:
                self.txt_residents.setText(str(tpl["default_residents"]))
        finally:
            self._updating_tables = False

        self._update_contextual_labels(tpl)
        self._recalc_unified_balance(sync_to_base=True)

    def _on_fixture_param_changed(self):
        if self._updating_tables:
            return
        # Ao alterar manualmente qualquer aparelho, sinaliza como Personalizado no combo
        if hasattr(self, "combo_building_template"):
            custom_idx = self.combo_building_template.findData("custom")
            if custom_idx >= 0 and self.combo_building_template.currentIndex() != custom_idx:
                self.combo_building_template.blockSignals(True)
                self.combo_building_template.setCurrentIndex(custom_idx)
                self.combo_building_template.blockSignals(False)
        self._recalc_unified_balance(sync_to_base=True)

    def _calculate_fixture_values(self):
        res = parse_int(self.txt_residents.text(), 4)
        if res <= 0:
            res = 4

        v_shower = self.sp_shower_count.value() * self.sp_shower_time.value() * self.sp_shower_flow.value()
        v_sink = self.sp_sink_liters.value()
        v_pot_in = v_shower + v_sink

        v_toilet = self.sp_toilet_flushes.value() * float(self.combo_toilet_vol.currentData() or 6.0)
        v_wash = (self.sp_wash_cycles.value() * self.sp_wash_vol.value()) / (7.0 * res)
        v_non_pot_in = v_toilet + v_wash

        d_in = max(10.0, v_pot_in + v_non_pot_in)
        pot_sh = max(5.0, min(95.0, (v_pot_in / d_in) * 100.0))
        non_pot_sh = 100.0 - pot_sh

        area = self.sp_garden_area.value()
        rate = float(self.combo_garden_rate.currentData() or 3.0)
        wash_ext = self.sp_wash_external.value() / 7.0
        irr_l = max(0.0, (area * rate) + wash_ext)

        return v_pot_in, v_non_pot_in, d_in, pot_sh, non_pot_sh, irr_l

    def _recalc_unified_balance(self, sync_to_base: bool = True):
        if not hasattr(self, "sp_shower_count") or self._updating_tables:
            return

        v_pot_in, v_non_pot_in, d_in, pot_sh, non_pot_sh, irr_l = self._calculate_fixture_values()
        res = parse_int(self.txt_residents.text(), 4)
        if res <= 0:
            res = 4

        unit = "hab"
        if hasattr(self, "combo_building_template"):
            tpl_id = self.combo_building_template.currentData()
            tpl = next((t for t in BUILDING_TEMPLATES if t["id"] == tpl_id), None)
            if tpl:
                unit = tpl.get("unit", "hab")

        # Atualiza subtotais nos cards
        if hasattr(self, "lbl_subtot_potable"):
            self.lbl_subtot_potable.setText(tr('🚿 {0} {1:.1f} L/{2}/dia').format(tr('Subtotal Potável:'), v_pot_in, unit))
        if hasattr(self, "lbl_subtot_non_potable"):
            self.lbl_subtot_non_potable.setText(tr('🚽 {0} {1:.1f} L/{2}/dia').format(tr('Subtotal Não-Potável:'), v_non_pot_in, unit))
        if hasattr(self, "lbl_subtot_outdoor"):
            self.lbl_subtot_outdoor.setText(tr('🌿 {0} {1:.1f} L/dia').format(tr('Subtotal Externo:'), irr_l))

        # Sincroniza com as variáveis base da edificação
        if sync_to_base and not self._updating_shares:
            self._updating_shares = True
            try:
                self.txt_demand.setText(f"{d_in:.0f}")
                self.txt_potable_indoor_share.setText(f"{pot_sh:.1f}".replace('.0', ''))
                self.txt_non_potable_indoor_share.setText(f"{non_pot_sh:.1f}".replace('.0', ''))
                if hasattr(self, "txt_potable_indoor_share_simple"):
                    self.txt_potable_indoor_share_simple.setText(f"{pot_sh:.1f}".replace('.0', ''))
                    self.txt_non_potable_indoor_share_simple.setText(f"{non_pot_sh:.1f}".replace('.0', ''))
                if hasattr(self, "txt_external_demand_l_day"):
                    self.txt_external_demand_l_day.setText(f"{irr_l:.0f}")
                self.txt_irrigation_l_day.setText(f"{irr_l:.0f}")
                self._sync_consolidated_share()
            finally:
                self._updating_shares = False

        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _force_sync_to_project(self):
        self._recalc_unified_balance(sync_to_base=True)
        QMessageBox.information(
            self,
            tr("Sincronização Concluída"),
            tr("Os parâmetros de consumo e partição foram recalculados e sincronizados com sucesso!")
        )

    def _on_potable_share_simple_changed(self):
        if self._updating_shares: return
        self._updating_shares = True
        try:
            val = parse_float(self.txt_potable_indoor_share_simple.text(), 65.0)
            val = max(0.0, min(100.0, val))
            non_pot = 100.0 - val
            self.txt_non_potable_indoor_share_simple.setText(f"{non_pot:.1f}".replace('.0', ''))
            self.check_input_highlight(self.txt_potable_indoor_share_simple)
            self.check_input_highlight(self.txt_non_potable_indoor_share_simple)
            self._sync_simple_pluvial_share()
        finally:
            self._updating_shares = False
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_non_potable_share_simple_changed(self):
        if self._updating_shares: return
        self._updating_shares = True
        try:
            val = parse_float(self.txt_non_potable_indoor_share_simple.text(), 35.0)
            val = max(0.0, min(100.0, val))
            pot = 100.0 - val
            self.txt_potable_indoor_share_simple.setText(f"{pot:.1f}".replace('.0', ''))
            self.check_input_highlight(self.txt_potable_indoor_share_simple)
            self.check_input_highlight(self.txt_non_potable_indoor_share_simple)
            self._sync_simple_pluvial_share()
        finally:
            self._updating_shares = False
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_external_demand_simple_changed(self):
        self.check_input_highlight(self.txt_external_demand_l_day)
        self._sync_simple_pluvial_share()
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _sync_simple_pluvial_share(self):
        d_val = parse_float(self.txt_demand.text(), 0.0)
        res_val = parse_float(self.txt_residents.text(), 0.0)
        non_pot_pct = parse_float(self.txt_non_potable_indoor_share_simple.text(), 35.0) if hasattr(self, "txt_non_potable_indoor_share_simple") else 35.0
        ext_l = parse_float(self.txt_external_demand_l_day.text(), 0.0) if hasattr(self, "txt_external_demand_l_day") else 0.0

        tot_in = max(0.0, d_val * res_val)
        tot_non_pot_in = tot_in * (non_pot_pct / 100.0)
        tot_pluvial_l = tot_non_pot_in + ext_l
        tot_all_l = tot_in + ext_l

        if tot_all_l > 0:
            equiv_share = (tot_pluvial_l / tot_all_l * 100.0)
            self.txt_share.blockSignals(True)
            self.txt_share.setText(f"{equiv_share:.1f}".replace('.0', ''))
            self.txt_share.blockSignals(False)
            self.check_input_highlight(self.txt_share)

    def _on_potable_indoor_changed(self):
        if self._updating_shares: return
        self._updating_shares = True
        try:
            val = parse_float(self.txt_potable_indoor_share.text(), 65.0)
            val = max(0.0, min(100.0, val))
            non_pot = 100.0 - val
            self.txt_non_potable_indoor_share.setText(f"{non_pot:.1f}".replace('.0', ''))
            self.check_input_highlight(self.txt_potable_indoor_share)
            self.check_input_highlight(self.txt_non_potable_indoor_share)
            self._sync_consolidated_share()
        finally:
            self._updating_shares = False
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_non_potable_indoor_changed(self):
        if self._updating_shares: return
        self._updating_shares = True
        try:
            val = parse_float(self.txt_non_potable_indoor_share.text(), 35.0)
            val = max(0.0, min(100.0, val))
            pot = 100.0 - val
            self.txt_potable_indoor_share.setText(f"{pot:.1f}".replace('.0', ''))
            self.check_input_highlight(self.txt_potable_indoor_share)
            self.check_input_highlight(self.txt_non_potable_indoor_share)
            self._sync_consolidated_share()
        finally:
            self._updating_shares = False
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_irrigation_changed(self):
        self.check_input_highlight(self.txt_irrigation_l_day)
        self._sync_consolidated_share()
        self._update_discretized_balance_label()
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _sync_consolidated_share(self):
        # No modo simplificado (Aba 0), o usuário define o percentual livremente; o avançado não deve sobrescrever!
        if hasattr(self, "tab_demand_mode") and self.tab_demand_mode.currentIndex() == 0:
            return

        d_val = parse_float(self.txt_demand.text(), 0.0)
        res_val = parse_float(self.txt_residents.text(), 0.0)
        non_pot_pct = parse_float(self.txt_non_potable_indoor_share.text(), 0.0)
        irr_l = parse_float(self.txt_irrigation_l_day.text(), 0.0)

        tot_indoor_l = max(0.0, d_val * res_val)
        tot_non_pot_indoor_l = tot_indoor_l * (non_pot_pct / 100.0)
        tot_pluvial_l = tot_non_pot_indoor_l + irr_l
        tot_all_l = tot_indoor_l + irr_l

        if tot_all_l > 0:
            equiv_share_pct = (tot_pluvial_l / tot_all_l * 100.0)
            self.txt_share.blockSignals(True)
            self.txt_share.setText(f"{equiv_share_pct:.1f}".replace('.0', ''))
            self.txt_share.blockSignals(False)
            self.check_input_highlight(self.txt_share)

    def _update_discretized_balance_label(self):
        d_val = parse_float(self.txt_demand.text(), 0.0)
        res_val = parse_float(self.txt_residents.text(), 0.0)
        share_pct = parse_float(self.txt_share.text(), 0.0)

        # ── 1. Modo Simplificado: CÁLCULO DIRETO E ISOLADO ──
        if hasattr(self, "lbl_simple_tot_demand"):
            ext_l = parse_float(self.txt_external_demand_l_day.text(), 0.0) if hasattr(self, "txt_external_demand_l_day") else 0.0
            pot_pct = parse_float(self.txt_potable_indoor_share_simple.text(), 65.0) if hasattr(self, "txt_potable_indoor_share_simple") else (100.0 - share_pct)
            non_pot_pct = parse_float(self.txt_non_potable_indoor_share_simple.text(), 35.0) if hasattr(self, "txt_non_potable_indoor_share_simple") else share_pct

            tot_indoor = max(0.0, d_val * res_val)
            pot_indoor = tot_indoor * (pot_pct / 100.0)
            non_pot_indoor = tot_indoor * (non_pot_pct / 100.0)
            tot_combined = tot_indoor + ext_l
            pluvial_target = non_pot_indoor + ext_l
            month_tot_m3 = (tot_combined * 30.417) / 1000.0
            global_share_pct = (pluvial_target / tot_combined * 100.0) if tot_combined > 0 else share_pct

            if d_val > 0 and res_val > 0:
                self.lbl_simple_tot_demand.setText(
                    f"💧 {tr('Demanda:')} {tot_combined:,.0f} L/d ({tot_indoor:,.0f} int + {ext_l:,.0f} ext)".replace(',', '.')
                )
                self.lbl_simple_month_vol.setText(
                    tr('📦 {0} {1:.1f} m³/mês (🔵 {2:.0f}% pot / 🟢 {3:.0f}% não-pot)').format(tr('Consumo Mensal:'), month_tot_m3, pot_pct, non_pot_pct)
                )
                self.lbl_simple_pluvial_demand.setText(
                    f"🌧️ {tr('Alvo Pluvial:')} {pluvial_target:,.0f} L/d ({global_share_pct:.0f}%)".replace(',', '.')
                )
            else:
                self.lbl_simple_tot_demand.setText(tr('💧 {0} -- L/dia').format(tr('Demanda Total:')))
                self.lbl_simple_month_vol.setText(tr('📦 {0} -- m³/mês').format(tr('Consumo Mensal:')))
                self.lbl_simple_pluvial_demand.setText(tr('🌧️ {0} -- L/dia').format(tr('Alvo Pluvial:')))

        # ── 2. Modo Avançado (Detalhamento de Usos) ──
        pot_pct = parse_float(self.txt_potable_indoor_share.text(), 0.0)
        non_pot_pct = parse_float(self.txt_non_potable_indoor_share.text(), 0.0)
        irr_l = parse_float(self.txt_irrigation_l_day.text(), 0.0)

        tot_indoor_l = max(0.0, d_val * res_val)
        pot_l = tot_indoor_l * (pot_pct / 100.0)
        non_pot_l = tot_indoor_l * (non_pot_pct / 100.0)
        tot_combined_dry_l = tot_indoor_l + irr_l
        month_m3_adv = (tot_combined_dry_l * 30.417) / 1000.0

        if hasattr(self, "lbl_discretized_balance"):
            if d_val > 0 and res_val > 0:
                txt = (
                    f"<b>{tr('Balanço Geral de Usos (Dia Seco):')}</b> &nbsp;"
                    f"🔵 {tr('Potável Interno:')} <b>{pot_l:,.0f} L/dia ({pot_pct:.0f}%)</b> &nbsp;•&nbsp; "
                    f"🟢 {tr('Não-Potável Interno:')} <b>{non_pot_l:,.0f} L/dia ({non_pot_pct:.0f}%)</b> &nbsp;•&nbsp; "
                    f"🌿 {tr('Irrigação Seca:')} <b>{irr_l:,.0f} L/dia</b> &nbsp;•&nbsp; "
                    f"🌊 <b>{tr('Demanda Total:')} {tot_combined_dry_l:,.0f} L/dia ({month_m3_adv:.1f} m³/mês)</b> &nbsp;•&nbsp; "
                    f"🌧️ {tr('Fração Pluvial Total:')} <b>{share_pct:.1f}%</b>"
                ).replace(',', '.')
            else:
                txt = f"<b>{tr('Balanço Geral de Usos (Dia Seco):')}</b> &nbsp;{tr('Preencha os dados de consumo e ocupantes para visualizar o balanço.')}"
            self.lbl_discretized_balance.setText(txt)

    def on_runoff_changed(self, idx):
        val = self.combo_runoff.currentData()
        if val == -1.0:
            self.txt_custom_runoff.show()
            self.txt_custom_runoff.setFocus()
        else:
            self.txt_custom_runoff.hide()
        self.building_updated.emit()

    def get_runoff_value(self) -> float:
        val = self.combo_runoff.currentData()
        if val == -1.0:
            try:
                return float(self.txt_custom_runoff.text().replace(',', '.'))
            except ValueError:
                return 0.75
        return float(val) if val is not None else 0.75

    def _on_demand_mode_changed(self, index: int):
        if hasattr(self, "tab_pages"):
            for i, page in enumerate(self.tab_pages):
                if i == index:
                    page.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                else:
                    page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.tab_demand_mode.adjustSize()

        names = [
            tr("Demanda Diária Simplificada"),
            tr("Detalhamento Avançado de Usos & Aparelhos"),
            tr("Variação Semanal"),
            tr("Variação Mensal"),
            tr("Variação Total Diária")
        ]
        if index < len(names):
            self.lbl_mode_summary.setText(f"{tr('Modo ativo:')} {names[index]}")
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _fill_weekly_from_constant(self):
        d_val = self.txt_demand.text().strip()
        res_val = self.txt_residents.text().strip()
        share_val = self.txt_non_potable_indoor_share.text().strip()
        self.table_weekly.blockSignals(True)
        for r in range(7):
            self.table_weekly.setItem(r, 1, QTableWidgetItem(d_val))
            self.table_weekly.setItem(r, 2, QTableWidgetItem(res_val))
            self.table_weekly.setItem(r, 3, QTableWidgetItem(share_val))
            try:
                tot = float(d_val.replace(',', '.')) * float(res_val.replace(',', '.')) * (float(share_val.replace(',', '.'))/100.0)
                self.table_weekly.setItem(r, 4, QTableWidgetItem(f"{tot:.1f}"))
            except Exception:
                self.table_weekly.setItem(r, 4, QTableWidgetItem("-"))
        self.table_weekly.blockSignals(False)
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_weekly_cell_changed(self, row, col):
        if self._updating_tables:
            return
        if col in (1, 2, 3):
            try:
                d = float(self.table_weekly.item(row, 1).text().replace(',', '.'))
                r = float(self.table_weekly.item(row, 2).text().replace(',', '.'))
                s = float(self.table_weekly.item(row, 3).text().replace(',', '.')) / 100.0
                tot = d * r * s
                self._assinalar_celula_percentual(self.table_weekly, row)
                self.table_weekly.blockSignals(True)
                self.table_weekly.setItem(row, 4, QTableWidgetItem(f"{tot:.1f}"))
                self.table_weekly.blockSignals(False)
            except Exception:
                pass
            self.update_tot_pluvial_label()
            self.building_updated.emit()

    def _fill_monthly_from_constant(self):
        d_val = self.txt_demand.text().strip()
        res_val = self.txt_residents.text().strip()
        share_val = self.txt_non_potable_indoor_share.text().strip()
        self.table_monthly.blockSignals(True)
        for r in range(12):
            self.table_monthly.setItem(r, 1, QTableWidgetItem(d_val))
            self.table_monthly.setItem(r, 2, QTableWidgetItem(res_val))
            self.table_monthly.setItem(r, 3, QTableWidgetItem(share_val))
            try:
                tot = float(d_val.replace(',', '.')) * float(res_val.replace(',', '.')) * (float(share_val.replace(',', '.'))/100.0)
                self.table_monthly.setItem(r, 4, QTableWidgetItem(f"{tot:.1f}"))
            except Exception:
                self.table_monthly.setItem(r, 4, QTableWidgetItem("-"))
        self.table_monthly.blockSignals(False)
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def _on_monthly_cell_changed(self, row, col):
        if self._updating_tables:
            return
        if col in (1, 2, 3):
            try:
                d = float(self.table_monthly.item(row, 1).text().replace(',', '.'))
                r = float(self.table_monthly.item(row, 2).text().replace(',', '.'))
                s = float(self.table_monthly.item(row, 3).text().replace(',', '.')) / 100.0
                tot = d * r * s
                self._assinalar_celula_percentual(self.table_monthly, row)
                self.table_monthly.blockSignals(True)
                self.table_monthly.setItem(row, 4, QTableWidgetItem(f"{tot:.1f}"))
                self.table_monthly.blockSignals(False)
            except Exception:
                pass
            self.update_tot_pluvial_label()
            self.building_updated.emit()

    def on_download_daily_template(self):
        main_win = self.window()
        total_days = 365
        start_date_str = "01/01/1980"
        if main_win and hasattr(main_win, "tab_project"):
            pj = main_win.tab_project
            if pj.precip_data is not None and len(pj.precip_data) > 0:
                total_days = len(pj.precip_data)
            start_date_str = pj.txt_start_date.text().strip() or "01/01/1980"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("Salvar Planilha Modelo de Consumo Diário"),
            "modelo_consumo_diario_triton.csv",
            f"{tr('Planilha CSV')} (*.csv);;{tr('Todos os Arquivos')} (*.*)"
        )
        if not file_path:
            return

        from datetime import datetime, timedelta
        try:
            start_dt = datetime.strptime(start_date_str, "%d/%m/%Y")
        except Exception:
            start_dt = datetime(1980, 1, 1)

        d_def = parse_float(self.txt_demand.text(), 200.0)
        res_def = parse_int(self.txt_residents.text(), 3)
        sh_def = parse_float(self.txt_non_potable_indoor_share.text(), 35.0)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("dia;data;consumo_per_capita_l_dia;habitantes;nao_potavel_pct;irrigacao_l_dia\n")
            for i in range(total_days):
                cur_dt = start_dt + timedelta(days=i)
                dt_str = cur_dt.strftime("%d/%m/%Y")
                f.write(f"{i+1};{dt_str};{d_def:.1f};{res_def};{sh_def:.1f};0.0\n")

        QMessageBox.information(
            self,
            tr("Modelo Gerado"),
            f"{tr('Planilha modelo gerada com sucesso para')} {total_days} {tr('dias')}.\n{file_path}"
        )

    def on_import_daily_series(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("Selecionar Planilha de Consumo Diário Preenchida"),
            "",
            f"{tr('Planilhas CSV')} (*.csv);;{tr('Todos os Arquivos')} (*.*)"
        )
        if not file_path:
            return

        rows = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line_s = line.strip()
                    if not line_s or line_s.startswith("dia") or line_s.startswith("Dia"):
                        continue
                    parts = line_s.split(";") if ";" in line_s else line_s.split(",")
                    if len(parts) >= 5:
                        day_lbl = parts[0].strip()
                        dt_lbl = parts[1].strip()
                        d_val = float(parts[2].replace(",", "."))
                        res_val = int(float(parts[3].replace(",", ".")))
                        sh_val = float(parts[4].replace(",", "."))
                        tot_l = d_val * res_val * (sh_val / 100.0)
                        rows.append((f"{day_lbl} ({dt_lbl})", d_val, res_val, sh_val, tot_l))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao ler arquivo CSV')}:\n{str(e)}")
            return

        if not rows:
            QMessageBox.warning(self, tr("Aviso"), tr("Nenhum registro válido encontrado no arquivo."))
            return

        self.daily_custom_series = rows
        self.table_daily_preview.setRowCount(len(rows))
        for r_idx, (dt_str, d_val, res_val, sh_val, tot_l) in enumerate(rows):
            self.table_daily_preview.setItem(r_idx, 0, QTableWidgetItem(dt_str))
            self.table_daily_preview.setItem(r_idx, 1, QTableWidgetItem(f"{d_val:.1f}"))
            self.table_daily_preview.setItem(r_idx, 2, QTableWidgetItem(str(res_val)))
            self.table_daily_preview.setItem(r_idx, 3, QTableWidgetItem(f"{sh_val:.1f}"))
            self.table_daily_preview.setItem(r_idx, 4, QTableWidgetItem(f"{tot_l:.1f}"))

        self.lbl_daily_status.setText(f"✅ {len(rows)} {tr('dias importados com sucesso a partir de')} {file_path}")
        self.lbl_daily_status.setStyleSheet("font-weight: bold; color: #16a34a; padding: 4px 0;")
        self.update_tot_pluvial_label()
        self.building_updated.emit()

    def update_tot_pluvial_label(self):
        if not hasattr(self, "lbl_tot_pluvial") or self.lbl_tot_pluvial is None:
            return
        idx = self.tab_demand_mode.currentIndex()
        if idx == 0:  # Simplificado
            d = parse_float(self.txt_demand.text(), 0.0)
            r = parse_float(self.txt_residents.text(), 0.0)
            ext_l = parse_float(self.txt_external_demand_l_day.text(), 0.0) if hasattr(self, "txt_external_demand_l_day") else 0.0
            non_pot_pct = parse_float(self.txt_non_potable_indoor_share_simple.text(), 35.0) if hasattr(self, "txt_non_potable_indoor_share_simple") else parse_float(self.txt_share.text(), 40.0)
            if d > 0 and r > 0:
                tot = (d * r * (non_pot_pct / 100.0)) + ext_l
                self.lbl_tot_pluvial.setText(tr('{0} {1:,.1f} L/dia').format(tr('Demanda Pluvial Alvo:'), tot).replace(',', '.'))
            else:
                self.lbl_tot_pluvial.setText(tr('{0} -- L/dia').format(tr('Demanda Pluvial Alvo:')))
        elif idx == 1:  # Avançado
            d = parse_float(self.txt_demand.text(), 0.0)
            r = parse_float(self.txt_residents.text(), 0.0)
            s = parse_float(self.txt_share.text(), 0.0) / 100.0
            if d > 0 and r > 0:
                tot = d * r * s
                self.lbl_tot_pluvial.setText(tr('{0} {1:,.1f} L/dia').format(tr('Demanda Pluvial Alvo:'), tot).replace(',', '.'))
            else:
                self.lbl_tot_pluvial.setText(tr('{0} -- L/dia').format(tr('Demanda Pluvial Alvo:')))
        elif idx == 2:  # Semanal
            tots = []
            for row in range(7):
                try:
                    d = float(self.table_weekly.item(row, 1).text().replace(',', '.'))
                    res = float(self.table_weekly.item(row, 2).text().replace(',', '.'))
                    sh = float(self.table_weekly.item(row, 3).text().replace(',', '.')) / 100.0
                    tots.append(d * res * sh)
                except Exception:
                    pass
            avg = sum(tots)/len(tots) if tots else 0.0
            self.lbl_tot_pluvial.setText(tr('{0} {1:,.1f} L/dia').format(tr('Demanda Pluvial Média Semanal:'), avg).replace(',', '.'))
        elif idx == 3:  # Mensal
            tots = []
            for row in range(12):
                try:
                    d = float(self.table_monthly.item(row, 1).text().replace(',', '.'))
                    res = float(self.table_monthly.item(row, 2).text().replace(',', '.'))
                    sh = float(self.table_monthly.item(row, 3).text().replace(',', '.')) / 100.0
                    tots.append(d * res * sh)
                except Exception:
                    pass
            avg = sum(tots)/len(tots) if tots else 0.0
            self.lbl_tot_pluvial.setText(tr('{0} {1:,.1f} L/dia').format(tr('Demanda Pluvial Média Mensal:'), avg).replace(',', '.'))
        elif idx == 4:  # Diária
            if self.daily_custom_series:
                avg = sum(r[4] for r in self.daily_custom_series) / len(self.daily_custom_series)
                self.lbl_tot_pluvial.setText(tr('{0} {1:,.1f} L/dia').format(tr('Demanda Pluvial Média Diária:'), avg).replace(',', '.'))
            else:
                self.lbl_tot_pluvial.setText(tr("Demanda Pluvial: -- L/dia"))

    def _preencher_tabela_calendario(self, tabela, linhas, demandas,
                                     moradores, fracoes):
        """Escreve na tabela os valores lidos do projeto.

        A fracao e gravada de 0 a 1 e exibida em porcentagem, que e a mesma
        convencao da leitura em `get_building_config`.
        """
        if not demandas and not moradores and not fracoes:
            return
        tabela.blockSignals(True)
        try:
            for r in range(linhas):
                d = float(demandas[r]) if demandas and r < len(demandas) else None
                m = float(moradores[r]) if moradores and r < len(moradores) else None
                f = float(fracoes[r]) if fracoes and r < len(fracoes) else None
                if d is not None:
                    tabela.setItem(r, 1, QTableWidgetItem(f"{d:.1f}"))
                if m is not None:
                    tabela.setItem(r, 2, QTableWidgetItem(str(int(m))))
                if f is not None:
                    tabela.setItem(r, 3, QTableWidgetItem(f"{f * 100.0:.1f}"))
                if d is not None and m is not None and f is not None:
                    tabela.setItem(r, 4, QTableWidgetItem(f"{d * m * f:.1f}"))
        except (TypeError, ValueError):
            pass
        finally:
            tabela.blockSignals(False)

    def _restaurar_serie_diaria(self, demandas, moradores, fracoes):
        """Reconstroi a serie diaria lida do projeto, com a mesma forma do CSV."""
        if not demandas:
            return
        linhas = []
        for i, d in enumerate(demandas):
            m = moradores[i] if moradores and i < len(moradores) else 1
            f = fracoes[i] if fracoes and i < len(fracoes) else 0.0
            linhas.append((f"dia {i + 1}", float(d), int(m), float(f) * 100.0,
                           float(d) * int(m) * float(f)))
        self.daily_custom_series = linhas
        if hasattr(self, "table_daily_preview"):
            self.table_daily_preview.setRowCount(len(linhas))
            for r, (rotulo, d, m, sh, tot) in enumerate(linhas):
                self.table_daily_preview.setItem(r, 0, QTableWidgetItem(rotulo))
                self.table_daily_preview.setItem(r, 1, QTableWidgetItem(f"{d:.1f}"))
                self.table_daily_preview.setItem(r, 2, QTableWidgetItem(str(m)))
                self.table_daily_preview.setItem(r, 3, QTableWidgetItem(f"{sh:.1f}"))
                self.table_daily_preview.setItem(r, 4, QTableWidgetItem(f"{tot:.1f}"))

    def get_building_config(self) -> dict:
        area_val = parse_float(self.txt_area.text(), 0.0)
        runoff_val = self.get_runoff_value()
        residents_val = parse_float(self.txt_residents.text(), 0.0)
        demand_val = parse_float(self.txt_demand.text(), 0.0)
        share_val = parse_float(self.txt_share.text(), 0.0) / 100.0

        idx = self.tab_demand_mode.currentIndex()

        if idx == 0:
            # Modo Simplificado: CÁLCULO DIRETO E ISOLADO
            # O externo é inserido em volume diário fixo (NÃO por habitante)
            irr_vol = parse_float(self.txt_external_demand_l_day.text(), 0.0) if hasattr(self, "txt_external_demand_l_day") else 0.0
            irr_thresh = 2.0
            irr_backup = True
            if hasattr(self, "txt_potable_indoor_share_simple"):
                pot_in_share = parse_float(self.txt_potable_indoor_share_simple.text(), 65.0) / 100.0
                non_pot_in_share = parse_float(self.txt_non_potable_indoor_share_simple.text(), 35.0) / 100.0
            elif share_val > 0.0:
                pot_in_share = max(0.0, 1.0 - share_val)
                non_pot_in_share = share_val
            else:
                pot_in_share = 0.65
                non_pot_in_share = 0.35
        else:
            pot_in_share = parse_float(self.txt_potable_indoor_share.text(), 65.0) / 100.0
            non_pot_in_share = parse_float(self.txt_non_potable_indoor_share.text(), 35.0) / 100.0
            irr_vol = parse_float(self.txt_irrigation_l_day.text(), 0.0)
            irr_thresh = parse_float(self.txt_irr_rain_threshold.text(), 2.0)
            irr_backup = self.chk_irr_potable_backup.isChecked()

        # A fração total é sempre a derivada das outras duas, e não o texto do
        # campo, para que o arquivo gravado nunca discorde do que se simulou.
        share_val = fracao_total(demand_val * max(residents_val, 0.0),
                                 min(1.0, max(0.0, non_pot_in_share)), irr_vol)

        cfg = {
            "area": area_val,
            "runoff": runoff_val,
            "residents": int(residents_val) if residents_val >= 1 else 0,
            "demand": demand_val,
            "share": share_val,
            "potable_indoor_share": pot_in_share,
            "non_potable_indoor_share": non_pot_in_share,
            "irrigation_liters_per_day": irr_vol,
            "irrigation_rain_threshold_mm": irr_thresh,
            "irrigation_potable_backup": irr_backup,
            "num_economias": parse_int(self.txt_economias.text(), 1),
            "demand_mode": "constant",
            "monthly_demands": None,
            "monthly_residents": None,
            "monthly_shares": None,
            "weekly_demands": None,
            "weekly_residents": None,
            "weekly_shares": None,
            "daily_demands": None,
            "daily_residents": None,
            "daily_shares": None
        }

        # Salva o estado dos aparelhos hidráulicos e template
        if hasattr(self, "combo_building_template"):
            cfg["template_id"] = self.combo_building_template.currentData() or "res_medio"
            # A tipologia também vai para a configuração do projeto. Sem isto
            # ela ficava presa neste dicionário, e o módulo econômico não
            # tinha como saber que cobra tarifa residencial de uma escola.
            _janela = self.window()
            _proj = getattr(_janela, "config", None) if _janela else None
            if _proj is not None:
                _proj.building_template_id = cfg["template_id"]
        if hasattr(self, "sp_shower_count"):
            cfg["shower_count"] = self.sp_shower_count.value()
            cfg["shower_time"] = self.sp_shower_time.value()
            cfg["shower_flow"] = self.sp_shower_flow.value()
            cfg["sink_liters"] = self.sp_sink_liters.value()
            cfg["toilet_flushes"] = self.sp_toilet_flushes.value()
            cfg["toilet_type_idx"] = self.combo_toilet_vol.currentIndex()
            cfg["wash_cycles"] = self.sp_wash_cycles.value()
            cfg["wash_vol"] = self.sp_wash_vol.value()
            cfg["garden_area"] = self.sp_garden_area.value()
            cfg["garden_rate_idx"] = self.combo_garden_rate.currentIndex()
            cfg["wash_external"] = self.sp_wash_external.value()

        if idx == 2:  # Semanal
            cfg["demand_mode"] = "weekly"
            w_d, w_r, w_s = [], [], []
            for row in range(7):
                try:
                    w_d.append(float(self.table_weekly.item(row, 1).text().replace(',', '.')))
                    w_r.append(int(float(self.table_weekly.item(row, 2).text().replace(',', '.'))))
                    w_s.append(float(self.table_weekly.item(row, 3).text().replace(',', '.')) / 100.0)
                except Exception:
                    w_d.append(demand_val); w_r.append(int(residents_val)); w_s.append(non_pot_in_share)
            cfg["weekly_demands"] = w_d
            cfg["weekly_residents"] = w_r
            cfg["weekly_shares"] = w_s
        elif idx == 3:  # Mensal
            cfg["demand_mode"] = "monthly"
            m_d, m_r, m_s = [], [], []
            for row in range(12):
                try:
                    m_d.append(float(self.table_monthly.item(row, 1).text().replace(',', '.')))
                    m_r.append(int(float(self.table_monthly.item(row, 2).text().replace(',', '.'))))
                    m_s.append(float(self.table_monthly.item(row, 3).text().replace(',', '.')) / 100.0)
                except Exception:
                    m_d.append(demand_val); m_r.append(int(residents_val)); m_s.append(non_pot_in_share)
            cfg["monthly_demands"] = m_d
            cfg["monthly_residents"] = m_r
            cfg["monthly_shares"] = m_s
        elif idx == 4:  # Diária
            cfg["demand_mode"] = "daily"
            if self.daily_custom_series:
                cfg["daily_demands"] = [r[1] for r in self.daily_custom_series]
                cfg["daily_residents"] = [r[2] for r in self.daily_custom_series]
                cfg["daily_shares"] = [r[3]/100.0 for r in self.daily_custom_series]

        return cfg

    def set_building_config(self, cfg: dict) -> None:
        if not cfg or not isinstance(cfg, dict):
            return
        self._updating_tables = True
        self._updating_shares = True
        try:
            if "area" in cfg:
                self.txt_area.setText(str(cfg["area"]))
            if "residents" in cfg:
                self.txt_residents.setText(str(cfg["residents"]))
            if "demand" in cfg:
                self.txt_demand.setText(str(cfg["demand"]))
            if "share" in cfg:
                sh_pct = fracao_para_percentual("A fração atendível", cfg["share"])
                self.txt_share.setText(f"{sh_pct:.1f}".replace('.0', ''))
            if "num_economias" in cfg:
                self.txt_economias.setText(str(cfg["num_economias"]))
            # Fração interna e demanda externa: sem restaurá-las, a tela voltava
            # aos padrões (35% e 0 L/dia) a cada projeto aberto e simulava com eles.
            if cfg.get("non_potable_indoor_share") is not None:
                fi_pct = fracao_para_percentual("A fração não potável interna", cfg["non_potable_indoor_share"])
                txt_fi = f"{fi_pct:.1f}".replace('.0', '')
                txt_fp = f"{100.0 - fi_pct:.1f}".replace('.0', '')
                for campo, texto in (("txt_non_potable_indoor_share_simple", txt_fi),
                                     ("txt_potable_indoor_share_simple", txt_fp),
                                     ("txt_non_potable_indoor_share", txt_fi),
                                     ("txt_potable_indoor_share", txt_fp)):
                    if hasattr(self, campo):
                        getattr(self, campo).setText(texto)
            if cfg.get("irrigation_liters_per_day") is not None:
                txt_e = f"{float(cfg['irrigation_liters_per_day']):.0f}"
                for campo in ("txt_external_demand_l_day", "txt_irrigation_l_day"):
                    if hasattr(self, campo):
                        getattr(self, campo).setText(txt_e)
            runoff_val = cfg.get("runoff") if "runoff" in cfg else cfg.get("runoff_coeff")
            if runoff_val is not None:
                r_val = float(runoff_val)
                matched = False
                for i in range(self.combo_runoff.count()):
                    c_data = self.combo_runoff.itemData(i)
                    if c_data is not None and c_data > 0 and abs(float(c_data) - r_val) < 0.01:
                        self.combo_runoff.setCurrentIndex(i)
                        matched = True
                        break
                if not matched:
                    self.combo_runoff.setCurrentIndex(self.combo_runoff.count() - 1)
                    self.txt_custom_runoff.setText(f"{r_val:.2f}".replace('.', ','))
                    self.txt_custom_runoff.show()

            # Restaura aparelhos se presentes
            if "shower_count" in cfg and hasattr(self, "sp_shower_count"):
                self.sp_shower_count.setValue(float(cfg.get("shower_count", 1.0)))
                self.sp_shower_time.setValue(float(cfg.get("shower_time", 8.0)))
                self.sp_shower_flow.setValue(float(cfg.get("shower_flow", 9.0)))
                self.sp_sink_liters.setValue(float(cfg.get("sink_liters", 26.0)))
                self.sp_toilet_flushes.setValue(float(cfg.get("toilet_flushes", 4.0)))
                if "toilet_type_idx" in cfg:
                    self.combo_toilet_vol.setCurrentIndex(int(cfg["toilet_type_idx"]))
                self.sp_wash_cycles.setValue(float(cfg.get("wash_cycles", 3.0)))
                self.sp_wash_vol.setValue(float(cfg.get("wash_vol", 100.0)))
                self.sp_garden_area.setValue(float(cfg.get("garden_area", 15.0)))
                if "garden_rate_idx" in cfg:
                    self.combo_garden_rate.setCurrentIndex(int(cfg["garden_rate_idx"]))
                self.sp_wash_external.setValue(float(cfg.get("wash_external", 35.0)))
                if "irrigation_rain_threshold_mm" in cfg:
                    self.txt_irr_rain_threshold.setText(f"{float(cfg['irrigation_rain_threshold_mm']):.1f}".replace('.', ','))
                if "irrigation_potable_backup" in cfg:
                    self.chk_irr_potable_backup.setChecked(bool(cfg["irrigation_potable_backup"]))

            # Restaura template selecionado
            if "template_id" in cfg and hasattr(self, "combo_building_template"):
                tpl_id = cfg["template_id"]
                idx = self.combo_building_template.findData(tpl_id)
                if idx >= 0:
                    self.combo_building_template.blockSignals(True)
                    self.combo_building_template.setCurrentIndex(idx)
                    self.combo_building_template.blockSignals(False)
                    tpl = next((t for t in BUILDING_TEMPLATES if t["id"] == tpl_id), None)
                    if tpl:
                        self._update_contextual_labels(tpl)

            # Repovoa as tabelas de calendario. Sem isto a configuracao
            # carrega a modulacao e a tela mostra tabelas vazias: o primeiro
            # salvamento seguinte leria a tela e apagaria o que foi lido.
            self._preencher_tabela_calendario(
                self.table_weekly, 7, cfg.get("weekly_demands"),
                cfg.get("weekly_residents"), cfg.get("weekly_shares"))
            self._preencher_tabela_calendario(
                self.table_monthly, 12, cfg.get("monthly_demands"),
                cfg.get("monthly_residents"), cfg.get("monthly_shares"))
            self._restaurar_serie_diaria(
                cfg.get("daily_demands"), cfg.get("daily_residents"),
                cfg.get("daily_shares"))

            # Restaura modo de demanda
            d_mode = cfg.get("demand_mode", "constant")
            mode_map = {"constant": 0, "advanced": 1, "weekly": 2, "monthly": 3, "daily": 4}
            target_tab = mode_map.get(d_mode, 0)
            self.tab_demand_mode.setCurrentIndex(target_tab)

        finally:
            self._updating_tables = False
            self._updating_shares = False

        self._recalc_unified_balance(sync_to_base=False)
        if self.tab_demand_mode.currentIndex() == 0:
            self._sync_simple_pluvial_share()
        else:
            self._sync_consolidated_share()
        self.update_tot_pluvial_label()
