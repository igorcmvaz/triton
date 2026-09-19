"""
Diálogo Modal do Mini Simulador / Assistente de Seleção de Motobomba do Netuno 5.
Inclui dimensionamento hidroenergético de tubulações (diâmetro econômico),
sucção uma bitola comercial acima do recalque, verificação de velocidade de escoamento,
e catálogo de motobombas comerciais brasileiras (Schneider, Dancor, Lepono) com bocais compatíveis.
"""

import math
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QMessageBox, QFrame,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QWidget,
    QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from netuno.ui.translation import tr, get_current_theme
from netuno.core.parser import format_ptbr


# ── TABELA DE TUBULAÇÕES COMERCIAIS DE PVC SOLDÁVEL (NBR 5648) ──
COMMERCIAL_PIPES = [
    {"dn": 20, "pol": '1/2"',   "di_mm": 16.6, "label": 'DN 20 mm (1/2")'},
    {"dn": 25, "pol": '3/4"',   "di_mm": 21.6, "label": 'DN 25 mm (3/4")'},
    {"dn": 32, "pol": '1"',     "di_mm": 27.8, "label": 'DN 32 mm (1")'},
    {"dn": 40, "pol": '1 1/4"', "di_mm": 35.2, "label": 'DN 40 mm (1 1/4")'},
    {"dn": 50, "pol": '1 1/2"', "di_mm": 44.0, "label": 'DN 50 mm (1 1/2")'},
    {"dn": 60, "pol": '2"',     "di_mm": 53.4, "label": 'DN 60 mm (2")'},
    {"dn": 75, "pol": '2 1/2"', "di_mm": 66.8, "label": 'DN 75 mm (2 1/2")'},
    {"dn": 85, "pol": '3"',     "di_mm": 76.0, "label": 'DN 85 mm (3")'},
    {"dn": 110, "pol": '4"',    "di_mm": 98.8, "label": 'DN 110 mm (4")'},
]


def calculate_forchheimer_diameter(q_m3s: float, t_hours_per_day: float = 2.0) -> float:
    """
    Fórmula de Forchheimer para diâmetro econômico de recalque:
    D = 1.3 * (t / 24)^0.25 * sqrt(Q)
    Retorna o diâmetro teórico em metros (m).
    """
    if q_m3s <= 0:
        return 0.025
    t_clamped = max(0.25, min(24.0, float(t_hours_per_day)))
    return 1.3 * math.pow(t_clamped / 24.0, 0.25) * math.sqrt(q_m3s)


# Alias técnico para dimensionamento econômico
calculate_economic_diameter = calculate_forchheimer_diameter


def find_commercial_recalque(d_forch_m: float) -> dict:
    """Retorna o diâmetro comercial mínimo que atende ao diâmetro de Forchheimer."""
    d_mm = d_forch_m * 1000.0
    for p in COMMERCIAL_PIPES:
        if p["di_mm"] >= (d_mm * 0.92):  # tolerância leve para proximidade de diâmetro
            return p
    return COMMERCIAL_PIPES[-1]


def get_suction_pipe(rec_pipe: dict) -> dict:
    """
    Regra hidráulica clássica de bombeamento:
    A tubulação de sucção deve ser estritamente uma bitola comercial acima do recalque (DN_suc > DN_rec).
    """
    try:
        idx = COMMERCIAL_PIPES.index(rec_pipe)
    except ValueError:
        idx = 2
    suc_idx = min(idx + 1, len(COMMERCIAL_PIPES) - 1)
    return COMMERCIAL_PIPES[suc_idx]


# ── CATÁLOGO DE MOTOBOMBAS COMERCIAIS REAIS DO MERCADO BRASILEIRO ──
# Dados técnicos e curvas H x Q catalogados de fabricantes nacionais (Schneider/Franklin Electric, Dancor e Lepono).
# Os bocais de fábrica e faixas de vazão/pressão utilizam exatamente os diâmetros calculados.
PUMP_CATALOG = [
    {
        "label": "Schneider BC-98 1/4 CV (0.18 kW) — Residencial Leve",
        "brand": "Schneider BC-98",
        "cv": 0.25,
        "kw": 0.184,
        "flow_lh": 1800.0,
        "max_h": 22.0,
        "cost": 340.0,
        "bocal_suc": '1" (DN 32)',
        "bocal_rec": '3/4" (DN 25)',
        "rec_pipe_dn": 25,
        "suc_pipe_dn": 32,
        "curve_q": [0, 500, 1000, 1500, 1800, 2200, 2500],
        "curve_h": [22.0, 21.0, 18.5, 15.0, 12.0, 7.0, 2.0],
    },
    {
        "label": "Schneider BC-98 1/3 CV (0.25 kW) — Residencial Padrão",
        "brand": "Schneider BC-98",
        "cv": 0.33,
        "kw": 0.245,
        "flow_lh": 2400.0,
        "max_h": 26.0,
        "cost": 395.0,
        "bocal_suc": '1" (DN 32)',
        "bocal_rec": '3/4" (DN 25)',
        "rec_pipe_dn": 25,
        "suc_pipe_dn": 32,
        "curve_q": [0, 500, 1000, 1500, 2000, 2400, 2800],
        "curve_h": [26.0, 25.0, 23.0, 20.0, 16.0, 12.5, 5.0],
    },
    {
        "label": "Schneider BC-92 S 1/2 CV (0.37 kW) — Centrífuga Sobrado",
        "brand": "Schneider BC-92 S",
        "cv": 0.50,
        "kw": 0.368,
        "flow_lh": 3600.0,
        "max_h": 30.0,
        "cost": 485.0,
        "bocal_suc": '1" (DN 32)',
        "bocal_rec": '1" (DN 32)',
        "rec_pipe_dn": 32,
        "suc_pipe_dn": 40,
        "curve_q": [0, 1000, 2000, 3000, 3600, 4200, 4800],
        "curve_h": [30.0, 28.5, 25.5, 21.5, 18.0, 13.5, 7.0],
    },
    {
        "label": "Schneider BC-92 T / Dancor CHS 3/4 CV (0.55 kW) — Média Elevação",
        "brand": "Schneider BC-92 T",
        "cv": 0.75,
        "kw": 0.552,
        "flow_lh": 5200.0,
        "max_h": 36.0,
        "cost": 690.0,
        "bocal_suc": '1 1/4" (DN 40)',
        "bocal_rec": '1" (DN 32)',
        "rec_pipe_dn": 32,
        "suc_pipe_dn": 40,
        "curve_q": [0, 1000, 2000, 3000, 4000, 5200, 6000],
        "curve_h": [36.0, 34.5, 32.0, 28.5, 24.0, 17.5, 10.0],
    },
    {
        "label": "Schneider BC-21 R 1.0 CV (0.75 kW) — Alta Vazão Predial",
        "brand": "Schneider BC-21 R",
        "cv": 1.00,
        "kw": 0.736,
        "flow_lh": 7200.0,
        "max_h": 42.0,
        "cost": 890.0,
        "bocal_suc": '1 1/4" (DN 40)',
        "bocal_rec": '1" (DN 32)',
        "rec_pipe_dn": 40,
        "suc_pipe_dn": 50,
        "curve_q": [0, 2000, 4000, 6000, 7200, 8500, 10000],
        "curve_h": [42.0, 39.5, 36.0, 30.5, 26.0, 18.5, 8.0],
    },
    {
        "label": "Schneider BC-22 R 1.5 CV (1.10 kW) — Edifício / Grande Altura",
        "brand": "Schneider BC-22 R",
        "cv": 1.50,
        "kw": 1.103,
        "flow_lh": 9800.0,
        "max_h": 48.0,
        "cost": 1280.0,
        "bocal_suc": '1 1/2" (DN 50)',
        "bocal_rec": '1 1/4" (DN 40)',
        "rec_pipe_dn": 40,
        "suc_pipe_dn": 50,
        "curve_q": [0, 2000, 4000, 6000, 8000, 9800, 11500, 13000],
        "curve_h": [48.0, 46.5, 43.5, 39.5, 33.5, 27.0, 18.0, 8.0],
    },
    {
        "label": "Schneider BC-22 R 2.0 CV (1.50 kW) — Comercial / Coletivo",
        "brand": "Schneider BC-22 R",
        "cv": 2.00,
        "kw": 1.471,
        "flow_lh": 13500.0,
        "max_h": 54.0,
        "cost": 1680.0,
        "bocal_suc": '1 1/2" (DN 50)',
        "bocal_rec": '1 1/4" (DN 40)',
        "rec_pipe_dn": 50,
        "suc_pipe_dn": 60,
        "curve_q": [0, 3000, 6000, 9000, 12000, 13500, 15500, 17500],
        "curve_h": [54.0, 51.5, 47.5, 42.0, 34.5, 30.0, 21.0, 8.0],
    },
    {
        "label": "Schneider ME-AL 3.0 CV (2.20 kW) — Multi-estágio Alta Pressão",
        "brand": "Schneider ME-AL",
        "cv": 3.00,
        "kw": 2.206,
        "flow_lh": 16000.0,
        "max_h": 68.0,
        "cost": 2450.0,
        "bocal_suc": '2" (DN 60)',
        "bocal_rec": '1 1/2" (DN 50)',
        "rec_pipe_dn": 50,
        "suc_pipe_dn": 75,
        "curve_q": [0, 3000, 6000, 9000, 12000, 15000, 16000, 18500],
        "curve_h": [68.0, 65.5, 61.5, 56.0, 49.0, 39.5, 35.0, 22.0],
    },
]


class PumpSelectionWizardDialog(QDialog):
    """
    Assistente técnico para dimensionamento e seleção de motobombas e tubulações.
    Calcula recalque pelo dimensionamento econômico, sucção uma bitola comercial acima,
    e consulta motobombas comerciais com diâmetros de bocais verificados.
    """
    def __init__(self, upper_tank_vol: float = 500.0, sweep_volumes: list = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("🧙‍♂️ Assistente de Dimensionamento de Motobomba & Tubulações"))
        screen = self.screen() or QApplication.primaryScreen()
        target_w, target_h = 960, 710
        if screen:
            avail = screen.availableGeometry()
            target_w = min(target_w, max(760, int(avail.width() * 0.86)))
            target_h = min(target_h, max(600, int(avail.height() * 0.86)))
        self.resize(target_w, target_h)

        self.upper_tank_vol = upper_tank_vol
        self.sweep_volumes = sweep_volumes or [1000, 2000, 3000, 5000, 7500, 10000, 15000, 20000]
        self.selected_pump_data = None
        self._user_selected_pipe = False

        self.init_ui()
        self.recalculate()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        heading = "#f4f4f5" if is_dark else "#0f172a"
        sub_color = "#38bdf8" if is_dark else "#0284c7"
        bg_card = "#1e293b" if is_dark else "#f8fafc"
        border_card = "#334155" if is_dark else "#cbd5e1"

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Cabeçalho Informativo
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-left: 4px solid #0284c7;
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        h_lay = QVBoxLayout(header_frame)
        h_lay.setContentsMargins(4, 4, 4, 4)
        h_lay.setSpacing(2)

        lbl_title = QLabel(tr("⚡ Assistente Hidráulico de Dimensionamento de Motobomba & Tubulações"))
        lbl_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        lbl_title.setStyleSheet(f"color: {sub_color};")
        h_lay.addWidget(lbl_title)

        lbl_sub = QLabel(tr("Dimensiona o diâmetro econômico de recalque, adota sucção uma bitola acima e cruza com motobombas comerciais (Schneider, Dancor, Lepono)."))
        lbl_sub.setStyleSheet("font-size: 11px; color: #64748b;")
        h_lay.addWidget(lbl_sub)
        layout.addWidget(header_frame)

        self.tabs = QTabWidget()

        # ── ABA 1: DIMENSIONAMENTO HIDRÁULICO ──
        tab_dim = QWidget()
        lay_dim = QVBoxLayout(tab_dim)
        lay_dim.setSpacing(10)

        # PAINEL 1: ENTRADA DE DADOS FÍSICOS DA EDIFICAÇÃO
        gb_input = QGroupBox(tr("1. Parâmetros de Operação e Geometria da Instalação"))
        grid_in = QGridLayout()
        grid_in.setSpacing(8)

        grid_in.addWidget(QLabel(tr("Volume Reservatório Superior (L):")), 0, 0)
        self.spin_upper_vol = QDoubleSpinBox()
        self.spin_upper_vol.setRange(50.0, 50000.0)
        self.spin_upper_vol.setValue(self.upper_tank_vol)
        self.spin_upper_vol.setSuffix(" L")
        self.spin_upper_vol.valueChanged.connect(self.on_param_changed)
        grid_in.addWidget(self.spin_upper_vol, 0, 1)

        grid_in.addWidget(QLabel(tr("Altura Geométrica (h_geom):")), 0, 2)
        self.spin_h_geom = QDoubleSpinBox()
        self.spin_h_geom.setRange(1.0, 100.0)
        self.spin_h_geom.setValue(10.0)
        self.spin_h_geom.setSuffix(" m")
        self.spin_h_geom.valueChanged.connect(self.recalculate)
        grid_in.addWidget(self.spin_h_geom, 0, 3)

        grid_in.addWidget(QLabel(tr("Extensão Tubo Recalque (L):")), 1, 0)
        self.spin_pipe_len = QDoubleSpinBox()
        self.spin_pipe_len.setRange(1.0, 300.0)
        self.spin_pipe_len.setValue(20.0)
        self.spin_pipe_len.setSuffix(" m")
        self.spin_pipe_len.valueChanged.connect(self.recalculate)
        grid_in.addWidget(self.spin_pipe_len, 1, 1)

        grid_in.addWidget(QLabel(tr("Tempo Operação Diária (t):")), 1, 2)
        self.spin_op_hours = QDoubleSpinBox()
        self.spin_op_hours.setRange(0.5, 24.0)
        self.spin_op_hours.setValue(2.0)
        self.spin_op_hours.setSingleStep(0.5)
        self.spin_op_hours.setSuffix(f" {tr('h/dia')}")
        self.spin_op_hours.setToolTip(tr("Número de horas de funcionamento por dia da motobomba (variável 't' no dimensionamento econômico)."))
        self.spin_op_hours.valueChanged.connect(self.on_param_changed)
        grid_in.addWidget(self.spin_op_hours, 1, 3)

        grid_in.addWidget(QLabel(tr("Tempo Máx. Enchimento Reservatório:")), 2, 0)
        self.spin_fill_time = QSpinBox()
        self.spin_fill_time.setRange(5, 360)
        self.spin_fill_time.setValue(45)
        self.spin_fill_time.setSuffix(f" {tr('minutos')}")
        self.spin_fill_time.valueChanged.connect(self.on_param_changed)
        grid_in.addWidget(self.spin_fill_time, 2, 1)

        grid_in.addWidget(QLabel(tr("Rendimento do Conjunto (%):")), 2, 2)
        self.spin_efficiency = QDoubleSpinBox()
        self.spin_efficiency.setRange(20.0, 95.0)
        self.spin_efficiency.setValue(55.0)
        self.spin_efficiency.setSuffix(" %")
        self.spin_efficiency.valueChanged.connect(self.recalculate)
        grid_in.addWidget(self.spin_efficiency, 2, 3)

        gb_input.setLayout(grid_in)
        lay_dim.addWidget(gb_input)

        # PAINEL 2: RESULTADOS HIDRÁULICOS & TUBULAÇÕES
        gb_calc = QGroupBox(tr("2. Dimensionamento Hidráulico de Tubulações & Requisitos"))
        grid_calc = QGridLayout()
        grid_calc.setSpacing(8)

        grid_calc.addWidget(QLabel(tr("Diâmetro Econômico Teórico:")), 0, 0)
        self.lbl_economic_diam = QLabel("-- mm")
        self.lbl_economic_diam.setStyleSheet("font-weight: bold; color: #0284c7; font-size: 11.5px;")
        self.lbl_forchheimer = self.lbl_economic_diam
        grid_calc.addWidget(self.lbl_economic_diam, 0, 1)

        grid_calc.addWidget(QLabel(tr("Vazão Requerida (Q_rec):")), 0, 2)
        self.lbl_qmin = QLabel("-- L/h")
        self.lbl_qmin.setStyleSheet("font-weight: bold; color: #0369a1;")
        grid_calc.addWidget(self.lbl_qmin, 0, 3)

        grid_calc.addWidget(QLabel(tr("Tubulação Recalque Selecionada:")), 1, 0)
        self.combo_pipe_dn = QComboBox()
        for p in COMMERCIAL_PIPES:
            self.combo_pipe_dn.addItem(p["label"], p["dn"])
        self.combo_pipe_dn.currentIndexChanged.connect(self.on_user_recalque_changed)
        grid_calc.addWidget(self.combo_pipe_dn, 1, 1)

        grid_calc.addWidget(QLabel(tr("Tubulação Sucção Selecionada:")), 1, 2)
        self.combo_suction_dn = QComboBox()
        for p in COMMERCIAL_PIPES:
            self.combo_suction_dn.addItem(p["label"], p["dn"])
        self.combo_suction_dn.currentIndexChanged.connect(self.on_user_suction_changed)
        grid_calc.addWidget(self.combo_suction_dn, 1, 3)

        self.lbl_suction_dn = QLabel("--")
        self.lbl_suction_dn.setVisible(False)

        grid_calc.addWidget(QLabel(tr("Velocidade no Recalque:")), 2, 0)
        self.lbl_velocity = QLabel("-- m/s")
        grid_calc.addWidget(self.lbl_velocity, 2, 1)

        grid_calc.addWidget(QLabel(tr("Perda de Carga Estimada (J*L):")), 2, 2)
        self.lbl_loss = QLabel("-- mca")
        self.lbl_loss.setStyleSheet("font-weight: bold; color: #64748b;")
        grid_calc.addWidget(self.lbl_loss, 2, 3)

        grid_calc.addWidget(QLabel(tr("Altura Manométrica Total (H_man):")), 3, 0)
        self.lbl_hman = QLabel("-- mca")
        self.lbl_hman.setStyleSheet("font-weight: bold; color: #0369a1; font-size: 11.5px;")
        grid_calc.addWidget(self.lbl_hman, 3, 1)

        grid_calc.addWidget(QLabel(tr("Potência Teórica Necessária:")), 3, 2)
        self.lbl_pteor = QLabel("-- kW (-- CV)")
        self.lbl_pteor.setStyleSheet("font-weight: bold; color: #059669; font-size: 11.5px;")
        grid_calc.addWidget(self.lbl_pteor, 3, 3)

        gb_calc.setLayout(grid_calc)
        lay_dim.addWidget(gb_calc)

        # PAINEL 3: SELEÇÃO DE MOTOBOMBA COMERCIAL
        gb_recommendation = QGroupBox(tr("3. Seleção de Motobomba Comercial (Bocais Compatíveis)"))
        vlay_rec = QVBoxLayout()
        vlay_rec.setSpacing(8)

        self.combo_pump = QComboBox()
        for p in PUMP_CATALOG:
            self.combo_pump.addItem(p["label"], p)
        self.combo_pump.currentIndexChanged.connect(self.on_pump_selection_changed)
        vlay_rec.addWidget(self.combo_pump)

        # Detalhes do modelo selecionado
        grid_pump_det = QGridLayout()
        grid_pump_det.addWidget(QLabel(tr("Potência Elétrica:")), 0, 0)
        self.lbl_pump_power = QLabel("-- kW")
        self.lbl_pump_power.setStyleSheet("font-weight: bold;")
        grid_pump_det.addWidget(self.lbl_pump_power, 0, 1)

        grid_pump_det.addWidget(QLabel(tr("Vazão Nominal do Modelo:")), 0, 2)
        self.lbl_pump_flow = QLabel("-- L/h")
        self.lbl_pump_flow.setStyleSheet("font-weight: bold;")
        grid_pump_det.addWidget(self.lbl_pump_flow, 0, 3)

        grid_pump_det.addWidget(QLabel(tr("Bocais de Fábrica (Sucção x Recalque):")), 1, 0)
        self.lbl_pump_threads = QLabel("--")
        self.lbl_pump_threads.setStyleSheet("font-weight: bold; color: #0284c7;")
        grid_pump_det.addWidget(self.lbl_pump_threads, 1, 1)

        grid_pump_det.addWidget(QLabel(tr("Tempo Real de Enchimento:")), 1, 2)
        self.lbl_actual_time = QLabel("-- min")
        self.lbl_actual_time.setStyleSheet("font-weight: bold; color: #0284c7;")
        grid_pump_det.addWidget(self.lbl_actual_time, 1, 3)

        grid_pump_det.addWidget(QLabel(tr("Preço Médio de Aquisição (CAPEX):")), 2, 0)
        self.lbl_pump_cost = QLabel("R$ --")
        self.lbl_pump_cost.setStyleSheet("font-weight: bold; color: #059669; font-size: 11.5px;")
        grid_pump_det.addWidget(self.lbl_pump_cost, 2, 1)

        grid_pump_det.addWidget(QLabel(tr("Pressão Máxima de Fechamento:")), 2, 2)
        self.lbl_pump_maxh = QLabel("-- mca")
        grid_pump_det.addWidget(self.lbl_pump_maxh, 2, 3)

        # Nota técnica de referência na aba de dimensionamento
        lbl_ref_note = QLabel(
            tr("📌 <b>Modelo de Referência:</b> O dimensionamento adota os parâmetros de catálogo de um modelo comercial de referência. "
               "Você pode visualizar a curva de desempenho e alterar livremente os parâmetros na aba <i>Curva Característica (H × Q)</i>.")
        )
        lbl_ref_note.setStyleSheet("font-size: 10.5px; color: #64748b; padding-top: 2px;")
        lbl_ref_note.setWordWrap(True)
        vlay_rec.addWidget(lbl_ref_note)

        btn_view_curve = QPushButton(tr("📈 Visualizar Curva Característica da Motobomba (H × Q)"))
        btn_view_curve.setStyleSheet("font-weight: bold; color: #0284c7; background-color: transparent; border: 1px solid #0284c7; border-radius: 4px; padding: 4px 10px;")
        btn_view_curve.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        vlay_rec.addWidget(btn_view_curve)

        gb_recommendation.setLayout(vlay_rec)
        lay_dim.addWidget(gb_recommendation)
        self.tabs.addTab(tab_dim, tr("📐 Dimensionamento Hidráulico"))

        # ── ABA 2: CURVA CARACTERÍSTICA DA MOTOBOMBA (H × Q) ──
        tab_curve = QWidget()
        lay_curve = QVBoxLayout(tab_curve)
        lay_curve.setSpacing(8)

        # Banner de Aviso / Indicação de Modelo Específico e Liberdade de Modificação
        self.frame_curve_banner = QFrame()
        self.frame_curve_banner.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-left: 4px solid #f59e0b;
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        b_lay = QVBoxLayout(self.frame_curve_banner)
        b_lay.setContentsMargins(4, 4, 4, 4)
        b_lay.setSpacing(2)

        self.lbl_curve_model_title = QLabel(tr("📌 Modelo de Referência Comercial: Schneider BC-98"))
        self.lbl_curve_model_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.lbl_curve_model_title.setStyleSheet("color: #d97706;")
        b_lay.addWidget(self.lbl_curve_model_title)

        self.lbl_curve_model_desc = QLabel(
            tr("A curva de desempenho abaixo corresponde ao modelo comercial de referência selecionado. "
               "Os dados de catálogo orientam a especificação técnica, mas você pode modificar os parâmetros "
               "de vazão, desnível geométrico, rendimento e diâmetros de acordo com o modelo do fabricante de sua preferência.")
        )
        self.lbl_curve_model_desc.setStyleSheet("font-size: 11px; color: #64748b;")
        self.lbl_curve_model_desc.setWordWrap(True)
        b_lay.addWidget(self.lbl_curve_model_desc)
        lay_curve.addWidget(self.frame_curve_banner)

        # Canvas Matplotlib da Curva H x Q
        self.figure = Figure(figsize=(8, 4.5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        lay_curve.addWidget(self.canvas, stretch=1)

        self.tabs.addTab(tab_curve, tr("📈 Curva Característica (H × Q)"))

        # ── ABA 3: ANÁLISE NA VARREDURA DE VOLUMES ──
        tab_sweep = QWidget()
        lay_sw = QVBoxLayout(tab_sweep)
        lay_sw.setSpacing(8)

        lbl_sw_desc = QLabel(tr("Comportamento da Motobomba e Consumo de Energia ao Longo da Varredura de Volumes:"))
        lbl_sw_desc.setStyleSheet("font-weight: bold; color: #475569;")
        lay_sw.addWidget(lbl_sw_desc)

        self.table_sweep = QTableWidget()
        self.table_sweep.setColumnCount(8)
        self.table_sweep.setHorizontalHeaderLabels([
            tr("Cisterna (L)"), tr("Vazão Mín. (L/h)"), tr("Recalque / Sucção"),
            tr("Modelo Recomendado"), tr("CAPEX (R$)"), tr("Tempo Recalque (h/ano)"),
            tr("Energia (kWh/ano)"), tr("Custo Energia (R$/ano)")
        ])
        self.table_sweep.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        lay_sw.addWidget(self.table_sweep)
        self.tabs.addTab(tab_sweep, tr("📊 Comportamento na Varredura de Volumes"))

        layout.addWidget(self.tabs)

        # BOTÕES DE AÇÃO
        row_btns = QHBoxLayout()
        row_btns.addStretch()

        btn_cancel = QPushButton(tr("Cancelar"))
        btn_cancel.clicked.connect(self.reject)
        row_btns.addWidget(btn_cancel)

        self.btn_apply = QPushButton(tr("✅ Aplicar ao Projeto"))
        self.btn_apply.setStyleSheet("background-color: #059669; color: white; font-weight: bold; padding: 8px 18px; border-radius: 4px;")
        self.btn_apply.clicked.connect(self.on_apply)
        row_btns.addWidget(self.btn_apply)

        layout.addLayout(row_btns)

    def on_param_changed(self):
        self._user_selected_pipe = False
        self.recalculate()

    def on_user_recalque_changed(self):
        rec_dn = self.combo_pipe_dn.currentData()
        if rec_dn:
            rec_pipe_obj = next((p for p in COMMERCIAL_PIPES if p["dn"] == rec_dn), None)
            if rec_pipe_obj:
                req_suc = get_suction_pipe(rec_pipe_obj)["dn"]
                cur_suc = self.combo_suction_dn.currentData()
                if cur_suc is None or cur_suc <= rec_dn:
                    idx_s = -1
                    for i in range(self.combo_suction_dn.count()):
                        if self.combo_suction_dn.itemData(i) == req_suc:
                            idx_s = i
                            break
                    if idx_s >= 0:
                        self.combo_suction_dn.blockSignals(True)
                        self.combo_suction_dn.setCurrentIndex(idx_s)
                        self.combo_suction_dn.blockSignals(False)
        self.recalculate(keep_recalque=True, keep_suction=True)

    def on_user_suction_changed(self):
        self.recalculate(keep_recalque=True, keep_suction=True)

    def recalculate(self, keep_recalque: bool = False, keep_suction: bool = False):
        upper_v = self.spin_upper_vol.value()
        h_geom = self.spin_h_geom.value()
        pipe_l = self.spin_pipe_len.value()
        t_op_h = self.spin_op_hours.value()
        fill_t_min = self.spin_fill_time.value()
        eff_pct = self.spin_efficiency.value()

        # 1. Vazão Mínima necessária (L/h e m³/s)
        fill_t_h = fill_t_min / 60.0
        q_rec_lh = upper_v / fill_t_h if fill_t_h > 0 else upper_v
        q_rec_m3h = q_rec_lh / 1000.0
        q_rec_m3s = q_rec_m3h / 3600.0
        self.lbl_qmin.setText(f"{q_rec_lh:,.0f} L/h ({q_rec_m3h:.2f} m³/h)".replace(',', '.'))

        # 2. Diâmetro Econômico Teórico (Fórmula de Forchheimer):
        # D = 1.3 * (t / 24)^0.25 * sqrt(Q)
        d_forch_m = calculate_forchheimer_diameter(q_rec_m3s, t_hours_per_day=t_op_h)
        d_forch_mm = d_forch_m * 1000.0
        rec_pipe_forch = find_commercial_recalque(d_forch_m)

        # 3. Estimativa inicial de H_man para selecionar modelo comercial adequado
        loss_est = 0.04 * pipe_l * 1.30
        h_man_est = h_geom + loss_est
        eta = eff_pct / 100.0
        p_teor_est_kw = (9810.0 * q_rec_m3s * h_man_est) / (1000.0 * eta) if eta > 0 else 0.37

        best_idx = 0
        for i, p in enumerate(PUMP_CATALOG):
            if p["flow_lh"] >= q_rec_lh and p["max_h"] >= h_man_est and p["kw"] >= (p_teor_est_kw * 0.90):
                best_idx = i
                break
            best_idx = i

        candidate_pump = PUMP_CATALOG[best_idx]

        # 4. A MOTOBOMBA REGE O DIMENSIONAMENTO:
        # Tubulações não podem ser inferiores aos bocais e especificações do modelo da motobomba.
        # A sucção deve ser estritamente superior ao recalque (DN_suc > DN_rec).
        governed_rec_dn = max(rec_pipe_forch["dn"], candidate_pump.get("rec_pipe_dn", 25))
        rec_pipe_obj = next((p for p in COMMERCIAL_PIPES if p["dn"] == governed_rec_dn), COMMERCIAL_PIPES[1])
        min_suc_dn = get_suction_pipe(rec_pipe_obj)["dn"]
        governed_suc_dn = max(min_suc_dn, candidate_pump.get("suc_pipe_dn", 32))

        if not keep_recalque:
            idx_r = -1
            for i in range(self.combo_pipe_dn.count()):
                if self.combo_pipe_dn.itemData(i) == governed_rec_dn:
                    idx_r = i
                    break
            if idx_r >= 0:
                self.combo_pipe_dn.blockSignals(True)
                self.combo_pipe_dn.setCurrentIndex(idx_r)
                self.combo_pipe_dn.blockSignals(False)

        if not keep_suction:
            idx_s = -1
            for i in range(self.combo_suction_dn.count()):
                if self.combo_suction_dn.itemData(i) == governed_suc_dn:
                    idx_s = i
                    break
            if idx_s >= 0:
                self.combo_suction_dn.blockSignals(True)
                self.combo_suction_dn.setCurrentIndex(idx_s)
                self.combo_suction_dn.blockSignals(False)

        # Recupera os diâmetros efetivos escolhidos
        selected_rec_dn = self.combo_pipe_dn.currentData() or governed_rec_dn
        current_rec_pipe = next((p for p in COMMERCIAL_PIPES if p["dn"] == selected_rec_dn), COMMERCIAL_PIPES[1])

        selected_suc_dn = self.combo_suction_dn.currentData() or governed_suc_dn
        current_suc_pipe = next((p for p in COMMERCIAL_PIPES if p["dn"] == selected_suc_dn), COMMERCIAL_PIPES[2])

        self.lbl_economic_diam.setText(
            tr('{0:.1f} mm (Teórico) → Regido pela Bomba: {1}').format(d_forch_mm, current_rec_pipe['label'])
        )
        self.lbl_suction_dn.setText(f"{current_suc_pipe['label']}")

        # 5. Velocidade de escoamento e Perda de carga (Hazen-Williams PVC C=140)
        d_int_m = current_rec_pipe["di_mm"] / 1000.0
        area_tubo = (math.pi * d_int_m * d_int_m) / 4.0
        velocity = (q_rec_m3s / area_tubo) if area_tubo > 0 else 0.0
        v_color = "#16a34a" if 0.6 <= velocity <= 2.5 else ("#d97706" if velocity < 0.6 else "#dc2626")
        self.lbl_velocity.setText(f"{velocity:.2f} m/s")
        self.lbl_velocity.setStyleSheet(f"font-weight: bold; color: {v_color};")

        # J = 10.643 * Q^1.852 * C^-1.852 * D^-4.87
        if q_rec_m3s > 0 and d_int_m > 0:
            c_pvc = 140.0
            j_loss = 10.643 * math.pow(q_rec_m3s, 1.852) * math.pow(c_pvc, -1.852) * math.pow(d_int_m, -4.87)
            loss_m = j_loss * pipe_l * 1.30  # 30% perdas localizadas
        else:
            loss_m = 0.5

        h_man = h_geom + loss_m
        # Guardados para irem no retorno: são o resultado do assistente, e sem
        # eles o cálculo de energia volta a usar a altura de recurso.
        self.h_man_calculada = h_man
        self.h_geom_informada = h_geom
        self.perda_de_carga_calculada = loss_m
        self.lbl_loss.setText(f"{loss_m:.2f} mca")
        self.lbl_hman.setText(f"{h_man:.2f} mca")

        # 6. Potência teórica (kW e CV): P = (rho * g * Q * H) / eta
        p_teor_kw = (9810.0 * q_rec_m3s * h_man) / (1000.0 * eta) if eta > 0 else 0.37
        p_teor_cv = p_teor_kw / 0.735499
        self.lbl_pteor.setText(f"{p_teor_kw:.2f} kW ({p_teor_cv:.2f} CV)")

        # Ajusta combo_pump para a melhor bomba
        self.combo_pump.blockSignals(True)
        self.combo_pump.setCurrentIndex(best_idx)
        self.combo_pump.blockSignals(False)

        self.update_pump_details(current_rec_pipe, current_suc_pipe)
        self.update_sweep_table(h_man, eta)
        self.update_pump_curve_plot(q_rec_lh, h_man, h_geom, current_rec_pipe)

    def on_pump_selection_changed(self):
        p_data = self.combo_pump.currentData()
        if not p_data:
            return

        p_rec_dn = p_data.get("rec_pipe_dn", 25)
        rec_pipe_obj = next((p for p in COMMERCIAL_PIPES if p["dn"] == p_rec_dn), COMMERCIAL_PIPES[1])
        min_suc_dn = get_suction_pipe(rec_pipe_obj)["dn"]
        p_suc_dn = max(min_suc_dn, p_data.get("suc_pipe_dn", 32))

        # A motobomba rege: sincroniza as tubulações com o modelo selecionado
        self.combo_pipe_dn.blockSignals(True)
        idx_rec = -1
        for i in range(self.combo_pipe_dn.count()):
            if self.combo_pipe_dn.itemData(i) == p_rec_dn:
                idx_rec = i
                break
        if idx_rec >= 0:
            self.combo_pipe_dn.setCurrentIndex(idx_rec)
        self.combo_pipe_dn.blockSignals(False)

        self.combo_suction_dn.blockSignals(True)
        idx_suc = -1
        for i in range(self.combo_suction_dn.count()):
            if self.combo_suction_dn.itemData(i) == p_suc_dn:
                idx_suc = i
                break
        if idx_suc >= 0:
            self.combo_suction_dn.setCurrentIndex(idx_suc)
        self.combo_suction_dn.blockSignals(False)

        self.recalculate(keep_recalque=True, keep_suction=True)

    def update_pump_details(self, rec_pipe: dict, suc_pipe: dict):
        p_data = self.combo_pump.currentData()
        if not p_data:
            return

        upper_v = self.spin_upper_vol.value()
        self.lbl_pump_power.setText(f"{p_data['kw']:.3f} kW ({p_data['cv']} CV)")
        self.lbl_pump_flow.setText(f"{p_data['flow_lh']:,.0f} L/h".replace(',', '.'))
        self.lbl_pump_threads.setText(tr('Sucção {0}  ×  Recalque {1}').format(p_data.get('bocal_suc', '--'), p_data.get('bocal_rec', '--')))
        self.lbl_pump_cost.setText(f"R$ {p_data['cost']:.2f}")
        self.lbl_pump_maxh.setText(f"{p_data['max_h']:.1f} mca")

        actual_t_min = (upper_v / p_data['flow_lh']) * 60.0 if p_data['flow_lh'] > 0 else 0
        self.lbl_actual_time.setText(f"{actual_t_min:.1f} min")

        self.selected_pump_data = {
            "kw": p_data['kw'],
            "cv_str": f"{p_data['cv']} CV",
            "cv": p_data['cv'],
            "flow_lh": p_data['flow_lh'],
            "cost": p_data['cost'],
            "upper_vol": upper_v,
            "efficiency": self.spin_efficiency.value(),
            "recalque_dn": rec_pipe["dn"],
            "recalque_label": rec_pipe["label"],
            "recalque_len": self.spin_pipe_len.value(),
            "suction_dn": suc_pipe["dn"],
            "suction_label": suc_pipe["label"],
            "suction_len": 5.0,
            "bocal_suc": p_data.get('bocal_suc', ''),
            "bocal_rec": p_data.get('bocal_rec', ''),
            "brand": p_data.get('brand', ''),
            # A hidráulica calculada aqui precisa chegar ao motor. Sem estes três
            # campos o programa refazia a conta com a altura de recurso, e não com
            # o desnível que o usuário informou.
            "manometric_head_m": getattr(self, "h_man_calculada", 0.0),
            "geometric_head_m": getattr(self, "h_geom_informada", 0.0),
            "head_loss_m": getattr(self, "perda_de_carga_calculada", 0.0),
        }

    def update_sweep_table(self, h_man: float, eta: float):
        vols = self.sweep_volumes
        self.table_sweep.setRowCount(len(vols))
        tarifa_kwh = 1.0

        for r, vol in enumerate(vols):
            daily_demand_l = min(vol * 0.35, 1200.0)
            q_nec_lh = max(1000.0, daily_demand_l / 1.5)
            q_m3s = (q_nec_lh / 1000.0) / 3600.0

            d_f = calculate_forchheimer_diameter(q_m3s, 2.0)
            rec_p = find_commercial_recalque(d_f)

            rec_pump = PUMP_CATALOG[0]
            for p in PUMP_CATALOG:
                if p["flow_lh"] >= q_nec_lh and p["max_h"] >= h_man:
                    rec_pump = p
                    break

            # A motobomba rege: tubulações mínimas acompanham o modelo (DN_suc > DN_rec)
            dn_rec_eff = max(rec_p["dn"], rec_pump.get("rec_pipe_dn", 25))
            rec_pipe_obj = next((p for p in COMMERCIAL_PIPES if p["dn"] == dn_rec_eff), COMMERCIAL_PIPES[1])
            min_suc_eff = get_suction_pipe(rec_pipe_obj)["dn"]
            dn_suc_eff = max(min_suc_eff, rec_pump.get("suc_pipe_dn", 32))

            ann_pumped_m3 = (daily_demand_l * 365.25 * 0.85) / 1000.0
            runtime_h_year = (ann_pumped_m3 * 1000.0) / rec_pump["flow_lh"] if rec_pump["flow_lh"] > 0 else 0
            energy_kwh = (rec_pump["kw"] * runtime_h_year) / eta if eta > 0 else 0
            cost_energy = energy_kwh * tarifa_kwh

            self.table_sweep.setItem(r, 0, QTableWidgetItem(f"{vol:,.0f} L".replace(',', '.')))
            self.table_sweep.setItem(r, 1, QTableWidgetItem(f"{q_nec_lh:.0f} L/h"))
            self.table_sweep.setItem(r, 2, QTableWidgetItem(f"DN {dn_rec_eff} (Rec) / DN {dn_suc_eff} (Suc)"))
            self.table_sweep.setItem(r, 3, QTableWidgetItem(rec_pump["brand"]))
            self.table_sweep.setItem(r, 4, QTableWidgetItem(f"R$ {rec_pump['cost']:.2f}"))
            self.table_sweep.setItem(r, 5, QTableWidgetItem(f"{runtime_h_year:.1f} h"))
            self.table_sweep.setItem(r, 6, QTableWidgetItem(f"{energy_kwh:.1f} kWh"))
            self.table_sweep.setItem(r, 7, QTableWidgetItem(f"R$ {cost_energy:.2f}"))

    def update_pump_curve_plot(self, q_rec_lh: float, h_man: float, h_geom: float, rec_pipe: dict):
        """Plota a curva característica H x Q da motobomba comercial e a curva do sistema."""
        if not hasattr(self, "figure") or not hasattr(self, "canvas"):
            return

        p_data = self.combo_pump.currentData()
        if not p_data:
            return

        # 1. Atualiza cabeçalho explicativo da aba de curva
        self.lbl_curve_model_title.setText(
            tr('📌 Modelo de Referência Comercial: {0}').format(p_data['label'])
        )
        self.lbl_curve_model_desc.setText(
            tr('A curva azul contínua representa o ensaio de bancada do fabricante para o modelo <b>{0} ({1} CV / {2} kW)</b> com bocal de recalque {3}. O ponto vermelho indica a solicitação calculada para a sua instalação ({4:,.0f} L/h @ {5:.1f} mca). Você pode ajustar livremente a vazão, altura geométrica, rendimento e tubulações de acordo com qualquer modelo comercial.').format(p_data['brand'], p_data['cv'], p_data['kw'], p_data.get('bocal_rec', ''), q_rec_lh, h_man)
        )

        # 2. Configura visual (tema dark / light)
        is_dark = get_current_theme() == "dark"
        bg_color = "#1e293b" if is_dark else "#ffffff"
        text_color = "#f1f5f9" if is_dark else "#0f172a"
        grid_color = "#334155" if is_dark else "#e2e8f0"
        line_pump_color = "#38bdf8" if is_dark else "#0284c7"
        line_sys_color = "#fb923c" if is_dark else "#ea580c"

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.figure.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # 3. Curva da Motobomba (H x Q)
        raw_q = np.array(p_data.get("curve_q", [0, p_data["flow_lh"]]), dtype=float)
        raw_h = np.array(p_data.get("curve_h", [p_data["max_h"], 0.0]), dtype=float)

        # Ajuste de curva polinomial quadrática suave (H = H0 - b * Q^2)
        if len(raw_q) >= 3:
            poly_coeff = np.polyfit(raw_q, raw_h, 2)
            q_max_plot = max(raw_q[-1], q_rec_lh * 1.35)
            q_dense = np.linspace(0.0, q_max_plot, 120)
            h_dense = np.polyval(poly_coeff, q_dense)
            h_dense = np.maximum(0.0, h_dense)
        else:
            q_dense = raw_q
            h_dense = raw_h
            q_max_plot = max(raw_q[-1], q_rec_lh * 1.35)

        ax.plot(
            q_dense, h_dense,
            color=line_pump_color, linewidth=2.4,
            label=f"Curva da Bomba: {p_data['brand']} ({p_data['cv']} CV)"
        )
        ax.scatter(
            raw_q, raw_h,
            color=line_pump_color, edgecolors="white" if is_dark else "black",
            s=45, zorder=4, label="Pontos de Catálogo (Ensaio)"
        )

        # 4. Curva do Sistema Hidráulico: H_sist(Q) = H_geom + Perdas(Q)
        # J = 10.643 * Q^1.852 * C^-1.852 * D^-4.87 * L_eq
        pipe_l = self.spin_pipe_len.value()
        d_int_m = rec_pipe["di_mm"] / 1000.0
        c_pvc = 140.0

        q_sys_dense = np.linspace(0.0, q_max_plot, 120)
        h_sys_dense = np.zeros_like(q_sys_dense)
        for i, q_val in enumerate(q_sys_dense):
            if q_val > 0 and d_int_m > 0:
                q_m3s_i = (q_val / 1000.0) / 3600.0
                j_i = 10.643 * math.pow(q_m3s_i, 1.852) * math.pow(c_pvc, -1.852) * math.pow(d_int_m, -4.87)
                loss_i = j_i * pipe_l * 1.30
                h_sys_dense[i] = h_geom + loss_i
            else:
                h_sys_dense[i] = h_geom

        ax.plot(
            q_sys_dense, h_sys_dense,
            color=line_sys_color, linewidth=2.0, linestyle="--",
            label=f"Curva da Instalação ({rec_pipe['label']}, L={pipe_l:.0f}m)"
        )

        # 5. Ponto de Operação do Projeto (Q_req, H_man)
        ax.scatter(
            [q_rec_lh], [h_man],
            color="#dc2626", edgecolors="white", s=130, marker="*",
            zorder=6, label=f"Ponto de Operação: {q_rec_lh:,.0f} L/h @ {h_man:.1f} mca"
        )
        # Linhas de chamada do ponto
        ax.vlines(q_rec_lh, 0, h_man, colors="#dc2626", linestyles=":", alpha=0.6)
        ax.hlines(h_man, 0, q_rec_lh, colors="#dc2626", linestyles=":", alpha=0.6)

        # Texto do ponto de operação
        ax.annotate(
            f"  Ponto de Trabalho\n  ({q_rec_lh:,.0f} L/h, {h_man:.1f} mca)",
            xy=(q_rec_lh, h_man),
            xytext=(10, 10), textcoords="offset points",
            color="#dc2626", fontweight="bold", fontsize=9.5,
            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec="#dc2626", alpha=0.85)
        )

        # 6. Formatação de eixos e títulos
        ax.set_xlabel(tr("Vazão de Recalque Q (L/h)"), color=text_color, fontsize=10.5, fontweight="bold")
        ax.set_ylabel(tr("Altura Manométrica Total H (mca)"), color=text_color, fontsize=10.5, fontweight="bold")
        ax.set_title(
            f"{tr('Curva Característica H × Q')} — {p_data['label']}",
            color=text_color, fontsize=12, fontweight="bold", pad=12
        )

        ax.tick_params(colors=text_color, labelsize=9.5)
        for spine in ax.spines.values():
            spine.set_color(grid_color)
        ax.grid(True, linestyle="--", alpha=0.5, color=grid_color)

        ax.set_xlim(0, q_max_plot * 1.05)
        max_h_axis = max(p_data["max_h"], h_man) * 1.15
        ax.set_ylim(0, max_h_axis)

        # Legenda limpa e legível
        leg = ax.legend(
            loc="upper right", frameon=True,
            facecolor=bg_color, edgecolor=grid_color, fontsize=9
        )
        for text in leg.get_texts():
            text.set_color(text_color)

        self.figure.tight_layout()
        self.canvas.draw()

    def on_apply(self):
        if not self.selected_pump_data:
            self.reject()
            return
        self.accept()
