"""
Etapa 6: Otimizador Ambiental & Análise do Ciclo de Vida (ACV Simplificada e Granular) - Netuno 5.
Interface limpa, intuitiva e organizada com diálogo estruturado de parâmetros da ACV:
- Cisternas e Caixas d'Água Superiores por material, densidade e fator CO2.
- Tubulações PVC por Diâmetro Nominal (DN 50, 75, 100, 150 mm).
- Motobombas por potência (CV), peso incorporado e eficiência elétrica.
- Insumos de tratamento químico e substituição de água da rede pública.
- Tabela dinâmica de Inventário de Ciclo de Vida (ICV) e Gráfico de Balanço de Carbono por empilhamento.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QComboBox, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QCheckBox, QTabWidget, QDialog, QFormLayout,
    QMessageBox, QTextBrowser
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QColor

from netuno.ui.translation import tr, get_current_theme, get_current_lang
from netuno.core.parser import format_ptbr
from netuno.core.environmental import (
    EnvironmentalConfig, EnvironmentalResult, EnvironmentalSweepResult,
    PipeInput, PumpInput, MATERIAL_PRESETS, PIPE_EMISSION_FACTORS_PER_METER, PUMP_EMBEDDED_CO2,
    calculate_lca, run_environmental_sweep, grid_factor_default
)
from netuno.core.environmental_sync import build_sync_snapshot, material_preset_values, pipe_co2_factor
from netuno.core import water_supply_routes as rotas_de_agua
from netuno.core.grid_emission_factors import (
    BASE_PADRAO as BASE_PADRAO_DA_REDE,
    bases_disponiveis as bases_de_rede_disponiveis,
    fator_co2eq as fator_co2eq_da_base,
    procedencia_da_base,
)
from netuno.core.chlorination import PUREZA_PADRAO as PUREZA_PADRAO_DO_CLORO
from netuno.core.etap_integration import AREA_DE_RECURSO_M2
from netuno.core.environmental import pump_embodied_co2_is_extrapolated
from dataclasses import replace
from netuno.core.chlorination import DOSE_PADRAO_MG_POR_LITRO, FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
from netuno.core.pump_energy import compute_annual_pump_energy, consumo_especifico_padrao_kwh_por_m3, CV_TO_KW
from netuno.core.esg_certifications import calculate_esg_certifications, EsgConsolidatedReport
from netuno.core.edge_certification import consumo_base_anual_m3
from netuno.ui.charts import (
    NetunoBaseChart, CO2ComparisonChart, EnvironmentalBalanceSummaryChart,
    LCAComponentBreakdownChart, WaterAndCarbonComparisonChart
)
from netuno.ui.justified_widgets import (
    JustifiedLineEdit, JustifiedComboBox, JustifiedCheckBox
)
from netuno.core.environmental_justifications import (
    get_material_justification, get_operational_justification,
    get_pipe_justification, get_pump_justification
)
import numpy as np


def adapt_dialog_size(dlg, target_w=1080, target_h=860, min_w=840, min_h=720):
    """Redimensiona o diálogo adaptativamente conforme a resolução da tela para evitar barras de rolagem."""
    from PySide6.QtWidgets import QApplication
    screen = dlg.screen() or QApplication.primaryScreen()
    if screen:
        avail = screen.availableGeometry()
        w = min(target_w, max(min_w, int(avail.width() * 0.94)))
        h = min(target_h, max(min_h, int(avail.height() * 0.94)))
        dlg.resize(w, h)
    else:
        dlg.resize(target_w, target_h)


class LCAParametersDialog(QDialog):
    """
    Diálogo intuitivo e estruturado para configurar todos os parâmetros da ACV.
    Organizado em 2 Colunas Limpas:
    - Coluna Esquerda: Quantidades, Dimensões e Equipamentos (com volumes sincronizados do projeto).
    - Coluna Direita: Fatores de Emissão de CO2e por Insumo (com destaque para valores pré-estimados).
    """
    def __init__(self, tab_env, parent=None):
        super().__init__(parent)
        self.tab_env = tab_env
        self._has_sweep = tab_env.has_technical_sweep()
        self._sync = tab_env.sync_from_project(force=False) if self._has_sweep else {}
        self.setWindowTitle(tr("⚙️ Parâmetros do Ciclo de Vida (ACV — Materiais, Tubulações e Operação)"))
        adapt_dialog_size(self, target_w=1080, target_h=860, min_w=840, min_h=720)
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        heading = "#f4f4f5" if is_dark else "#0f172a"
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        sync = self._sync or {}
        cur_vol = sync.get("lower_vol_l")
        if cur_vol is None: cur_vol = 5000.0
        up_vol = sync.get("upper_vol_l")
        if up_vol is None: up_vol = 500.0
        pump_cv = sync.get("pump_cv")
        if pump_cv is None: pump_cv = 0.5
        ann_kwh = sync.get("annual_pump_kwh")
        if ann_kwh is None: ann_kwh = 0.0
        spec_kwh = sync.get("specific_kwh_per_m3")
        if spec_kwh is None: spec_kwh = consumo_especifico_padrao_kwh_por_m3()

        banner = QFrame()
        banner.setStyleSheet("QFrame { background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 6px 12px; }")
        lay_b = QVBoxLayout(banner)
        lay_b.setContentsMargins(8, 4, 8, 4)
        lay_b.setSpacing(2)

        if self._has_sweep:
            info_text = (
                f"💧 <b>Cisterna:</b> {format_ptbr(cur_vol, 0)} L &nbsp;|&nbsp; "
                f"📦 <b>Caixa Superior:</b> {format_ptbr(up_vol, 0)} L &nbsp;|&nbsp; "
                f"⚡ <b>Motobomba:</b> {format_ptbr(pump_cv, 2)} CV &nbsp;|&nbsp; "
                f"🔌 <b>Consumo simulado:</b> {format_ptbr(ann_kwh, 1)} kWh/ano ({format_ptbr(spec_kwh, 3)} kWh/m³)"
            )
        else:
            info_text = tr("Execute a varredura da Etapa 3 para carregar os valores de cisterna e motobomba.")
        lbl_vol_info = QLabel(info_text)
        lbl_vol_info.setStyleSheet("color: #0369a1; font-size: 11.5px;")
        lay_b.addWidget(lbl_vol_info)

        lbl_hint = QLabel(
            tr("Valores em amarelo foram pré-preenchidos a partir da simulação (Etapa 3/5), "
               "catálogo de materiais ou CAPEX. Ajuste manualmente se necessário.")
        )
        lbl_hint.setStyleSheet("color: #475569; font-size: 10.5px;")
        lbl_hint.setWordWrap(True)
        lay_b.addWidget(lbl_hint)

        main_layout.addWidget(banner)

        # ── LEGENDA DE CORES DE CAMPO ──
        leg_box = QHBoxLayout()
        leg_box.setSpacing(15)

        lbl_leg_pre = QLabel("🟡 Campo Pré-estimado (Catálogo/Engenharia)")
        lbl_leg_pre.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; color: #854d0e; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: bold;")
        leg_box.addWidget(lbl_leg_pre)

        lbl_leg_cred = QLabel("🟢 Crédito / Abatimento de CO2")
        lbl_leg_cred.setStyleSheet("background-color: #dcfce7; border: 1px solid #86efac; color: #166534; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: bold;")
        leg_box.addWidget(lbl_leg_cred)

        lbl_leg_usr = QLabel("⚪ Quantidade / Entrada do Projetista")
        lbl_leg_usr.setStyleSheet("background-color: #ffffff; border: 1px solid #cbd5e1; color: #334155; padding: 3px 8px; border-radius: 4px; font-size: 10.5px;")
        leg_box.addWidget(lbl_leg_usr)

        leg_box.addStretch()
        main_layout.addLayout(leg_box)

        # ── ÁREA PRINCIPAL COM 2 COLUNAS (Sem scroll em monitores normais) ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        container = QWidget()
        lay_cols = QHBoxLayout(container)
        lay_cols.setContentsMargins(0, 0, 0, 0)
        lay_cols.setSpacing(16)

        # ── COLUNA DA ESQUERDA: QUANTIDADES E DIMENSÕES ──
        gb_left = QGroupBox(tr("📐 1. Quantidades, Dimensões e Equipamentos"))
        gb_left.setStyleSheet("QGroupBox { font-weight: bold; color: #1e293b; }")
        lay_l = QVBoxLayout(gb_left)
        lay_l.setContentsMargins(10, 10, 10, 10)
        lay_l.setSpacing(6)

        form_l = QFormLayout()
        form_l.setLabelAlignment(Qt.AlignLeft)
        form_l.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form_l.setSpacing(6)

        # ── MATERIAL CISTERNA INFERIOR COM JUSTIFICATIVAS ──
        self.combo_lower_mat = JustifiedComboBox()
        self.combo_lower_mat.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        material_justifications = {}
        for k, p in MATERIAL_PRESETS.items():
            self.combo_lower_mat.addItem(tr(p.name), k)
            # Mapa de justificativas: data_value -> justification
            density_just = get_material_justification(k, "density")
            if density_just:
                material_justifications[k] = density_just
        self.combo_lower_mat.set_justifications(material_justifications)
        idx_low = self.combo_lower_mat.findData(self.tab_env.combo_lower_mat.currentData())
        if idx_low >= 0:
            self.combo_lower_mat.setCurrentIndex(idx_low)
        self.combo_lower_mat.currentIndexChanged.connect(self._on_lower_material_changed)
        form_l.addRow(QLabel(tr("Material Cisterna Inferior:")), self.combo_lower_mat)

        # Densidade Cisterna (Pré-estimada) com justificativa
        self.txt_lower_density = JustifiedLineEdit(self.tab_env.txt_lower_density.text())
        self.txt_lower_density.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self._update_lower_density_justification()
        form_l.addRow(QLabel(tr("Densidade Cisterna (kg/m³):")), self.txt_lower_density)

        # Caixa d'Água Superior
        self.chk_upper_used = JustifiedCheckBox(tr("Habilitada"))
        self.chk_upper_used.setChecked(self.tab_env.chk_upper_used.isChecked())
        form_l.addRow(QLabel(tr("Usar Caixa d'Água Superior:")), self.chk_upper_used)

        self.combo_upper_mat = JustifiedComboBox()
        self.combo_upper_mat.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        for k, p in MATERIAL_PRESETS.items():
            self.combo_upper_mat.addItem(tr(p.name), k)
        self.combo_upper_mat.set_justifications(material_justifications)
        idx_up = self.combo_upper_mat.findData(self.tab_env.combo_upper_mat.currentData())
        if idx_up >= 0:
            self.combo_upper_mat.setCurrentIndex(idx_up)
        self.combo_upper_mat.currentIndexChanged.connect(self._on_upper_material_changed)
        form_l.addRow(QLabel(tr("Material Caixa Superior:")), self.combo_upper_mat)

        self.txt_upper_vol = JustifiedLineEdit(self.tab_env.txt_upper_vol.text())
        form_l.addRow(QLabel(tr("Volume Caixa Superior (L):")), self.txt_upper_vol)

        self.txt_upper_density = JustifiedLineEdit(self.tab_env.txt_upper_density.text())
        self.txt_upper_density.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self._update_upper_density_justification()
        form_l.addRow(QLabel(tr("Densidade Caixa Sup. (kg/m³):")), self.txt_upper_density)

        # ── TUBULAÇÕES (Sincronizadas com o CAPEX / Projeto) ──
        self.txt_pipes_m = {}
        for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
            val_str = self.tab_env.txt_pipes_m[dn].text() if (hasattr(self.tab_env, 'txt_pipes_m') and dn in self.tab_env.txt_pipes_m) else "0.0"
            txt_p = JustifiedLineEdit(val_str)
            self.txt_pipes_m[dn] = txt_p
            lbl_name = f"Tubulação PVC DN {dn} mm (m):"
            if dn in (20, 25, 32, 40):
                lbl_name = f"Tubo PVC DN {dn} (Sucção/Recalque) (m):"
            elif dn == 100:
                lbl_name = f"Tubo PVC DN 100 (Captação/Extrav.) (m):"
            form_l.addRow(QLabel(tr(lbl_name)), txt_p)

        # Aliases retrocompatíveis
        self.txt_pipe_50_m = self.txt_pipes_m[50]
        self.txt_pipe_75_m = self.txt_pipes_m[75]
        self.txt_pipe_100_m = self.txt_pipes_m[100]
        self.txt_pipe_150_m = self.txt_pipes_m[150]

        # ── MOTOBOMBA E OPERAÇÃO ──
        self.txt_pump_cv = JustifiedLineEdit(self.tab_env.txt_pump_cv.text())
        self.txt_pump_cv.textChanged.connect(self._update_pump_co2_justification)
        form_l.addRow(QLabel(tr("Potência Motobomba (CV):")), self.txt_pump_cv)

        self.txt_pump_kwh = JustifiedLineEdit(self.tab_env.txt_pump_kwh.text())
        self.txt_pump_kwh.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        form_l.addRow(QLabel(tr("Consumo Específico (kWh/m³):")), self.txt_pump_kwh)

        self.txt_chlorine_dose = JustifiedLineEdit(self.tab_env.txt_chlorine_dose.text())
        self.txt_chlorine_dose.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self.txt_chlorine_dose.set_justification(get_operational_justification("chlorine_dose"))
        form_l.addRow(QLabel(tr("Dosagem de Cloro (mg Cl2 ativo/L):")), self.txt_chlorine_dose)

        # A dose e de cloro ATIVO; o que se compra e o PRODUTO. A pureza faz a
        # ponte, e nao era editavel: valia sempre 65%, do hipoclorito de calcio
        # em pastilha. Quem usa agua sanitaria (cerca de 10%) precisa de seis
        # vezes mais produto para a mesma dose.
        self.txt_chlorine_purity = JustifiedLineEdit(
            f"{getattr(self.tab_env, '_pureza_do_cloro', PUREZA_PADRAO_DO_CLORO):.2f}"
        )
        self.txt_chlorine_purity.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self.txt_chlorine_purity.set_justification(get_operational_justification("chlorine_purity"))
        form_l.addRow(QLabel(tr("Pureza do Produto (kg Cl2 ativo/kg):")), self.txt_chlorine_purity)

        self.txt_lifespan = JustifiedLineEdit(self.tab_env.txt_lifespan.text())
        form_l.addRow(QLabel(tr("Vida Útil do Projeto (anos):")), self.txt_lifespan)

        lay_l.addLayout(form_l)
        lay_cols.addWidget(gb_left, stretch=1)

        # ── COLUNA DA DIREITA: FATORES DE EMISSÃO DE CO2 ──
        gb_right = QGroupBox(tr("🌱 2. Fatores de Emissão de CO2e por Insumo"))
        gb_right.setStyleSheet("QGroupBox { font-weight: bold; color: #1e293b; }")
        lay_r = QVBoxLayout(gb_right)
        lay_r.setContentsMargins(10, 10, 10, 10)
        lay_r.setSpacing(6)

        form_r = QFormLayout()
        form_r.setLabelAlignment(Qt.AlignLeft)
        form_r.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form_r.setSpacing(6)

        # ── FATORES DE EMISSÃO ──
        self.txt_lower_co2_kg = JustifiedLineEdit(self.tab_env.txt_lower_co2_kg.text())
        self.txt_lower_co2_kg.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self._update_lower_co2_justification()
        form_r.addRow(QLabel(tr("CO2 Material Cisterna (kg/kg):")), self.txt_lower_co2_kg)

        self.txt_upper_co2_kg = JustifiedLineEdit(self.tab_env.txt_upper_co2_kg.text())
        self.txt_upper_co2_kg.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self._update_upper_co2_justification()
        form_r.addRow(QLabel(tr("CO2 Material Caixa (kg/kg):")), self.txt_upper_co2_kg)

        # ── FATORES TUBULAÇÕES (kg CO2e / m) ──
        self.txt_pipes_co2 = {}
        for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
            val_str = self.tab_env.txt_pipes_co2[dn].text() if (hasattr(self.tab_env, 'txt_pipes_co2') and dn in self.tab_env.txt_pipes_co2) else f"{pipe_co2_factor(dn):.2f}"
            txt_co2 = JustifiedLineEdit(val_str)
            txt_co2.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
            # A justificativa existia e nao era exibida. Os quatro diametros
            # documentados a recebem; os demais seguem sem nota propria, porque
            # a massa linear vem da mesma tabela e nao ha texto especifico.
            txt_co2.set_justification(get_pipe_justification(dn))
            self.txt_pipes_co2[dn] = txt_co2
            form_r.addRow(QLabel(tr(f"CO2 Tubo DN {dn} (kg CO2/m):")), txt_co2)

        # Aliases retrocompatíveis
        self.txt_pipe_50_co2 = self.txt_pipes_co2[50]
        self.txt_pipe_75_co2 = self.txt_pipes_co2[75]
        self.txt_pipe_100_co2 = self.txt_pipes_co2[100]
        self.txt_pipe_150_co2 = self.txt_pipes_co2[150]

        # ── FATOR BOMBA ──
        self.txt_pump_co2 = JustifiedLineEdit(self.tab_env.txt_pump_co2.text())
        self.txt_pump_co2.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self._update_pump_co2_justification()
        form_r.addRow(QLabel(tr("CO2 Motobomba (kg CO2/un):")), self.txt_pump_co2)

        # ── FATORES OPERACIONAIS ──
        # ── BASE DO FATOR DA REDE ──
        # As bases documentadas diferem em gas contabilizado e em fronteira:
        # a serie do MCTI e CO2 apenas, e apenas da geracao; as demais sao
        # CO2-equivalente com fronteira mais larga. Escolher a base reescreve o
        # campo abaixo, e a procedencia fica a vista.
        self.cmb_base_rede = QComboBox()
        for _chave in sorted(bases_de_rede_disponiveis()):
            self.cmb_base_rede.addItem(_chave, _chave)
        _idx = self.cmb_base_rede.findData(BASE_PADRAO_DA_REDE)
        if _idx >= 0:
            self.cmb_base_rede.setCurrentIndex(_idx)
        self.cmb_base_rede.currentIndexChanged.connect(self._aplicar_base_da_rede)
        form_r.addRow(QLabel(tr("Base do fator da rede:")), self.cmb_base_rede)

        self.txt_grid_co2 = JustifiedLineEdit(self.tab_env.txt_grid_co2.text())
        self.txt_grid_co2.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        form_r.addRow(QLabel(tr("Matriz Elétrica (kg CO2/kWh):")), self.txt_grid_co2)

        self.lbl_base_rede_fonte = QLabel("")
        self.lbl_base_rede_fonte.setWordWrap(True)
        self.lbl_base_rede_fonte.setStyleSheet("color: #475569; font-size: 11px;")
        form_r.addRow("", self.lbl_base_rede_fonte)

        self.txt_chlorine_co2 = JustifiedLineEdit(self.tab_env.txt_chlorine_co2.text())
        self.txt_chlorine_co2.setStyleSheet("background-color: #fef9c3; border: 1px solid #fde047; font-weight: bold;")
        self.txt_chlorine_co2.set_justification(get_operational_justification("chlorine_co2"))
        form_r.addRow(QLabel(tr("Fator do Cloro (kg CO2e/kg Cl2):")), self.txt_chlorine_co2)

        # ── ABATIMENTO (Verde Destaque) ──
        self.txt_potable_co2 = JustifiedLineEdit(self.tab_env.txt_potable_co2.text())
        self.txt_potable_co2.setStyleSheet("background-color: #dcfce7; border: 1px solid #86efac; font-weight: bold; color: #166534;")
        form_r.addRow(QLabel(tr("Abatimento Água Potável (kg CO2/m³):")), self.txt_potable_co2)

        # ── ROTA DA AGUA SUBSTITUIDA ──
        # A emissao evitada nao e propriedade do sistema pluvial: e propriedade
        # da agua que ele desloca. Escolher a rota reescreve o campo abaixo.
        #
        # O combo ja existia e reescrevia o numero em silencio. Quem nao
        # conhecesse a literatura nao tinha como saber por que escolher uma rota
        # e nao outra, nem qual e a base do programa.
        _lbl_rota_ajuda = QLabel(tr(
            "<b>Qual água o sistema substitui?</b> O CO₂ evitado por m³ não é uma constante "
            "do sistema pluvial: é propriedade da água que ele deixa de consumir. Substituir "
            "água dessalinizada vale dezenas de vezes mais do que substituir água de manancial "
            "tratada por gravidade.<br><br>"
            "A <b>base do programa é {base:.2f} kg CO₂e/m³</b>, de tratamento convencional. Foi "
            "escolhida por ficar logo abaixo das faixas publicadas tanto com matriz europeia "
            "(0,41 a 0,47, Garfí et al., 2016) quanto com matriz brasileira (0,336 a 0,461 por "
            "macrorregião, Vaz et al., 2025): subestimar o benefício é o erro conservador.<br><br>"
            "Escolha abaixo a rota que corresponde ao <b>tratamento do seu local</b>. Cada uma "
            "declara fonte, tecnologia, matriz elétrica e fronteira do sistema."
        ).format(base=rotas_de_agua.BASE_DO_PROGRAMA_KG_M3))
        _lbl_rota_ajuda.setWordWrap(True)
        _lbl_rota_ajuda.setStyleSheet(
            "color: #334155; font-size: 11px; font-weight: normal; "
            "background-color: #f1f5f9; border: 1px solid #cbd5e1; "
            "border-radius: 4px; padding: 7px;"
        )
        form_r.addRow(_lbl_rota_ajuda)
        self.cmb_rota_agua = QComboBox()
        for _chave in rotas_de_agua.chaves_das_rotas():
            self.cmb_rota_agua.addItem(rotas_de_agua.nome_da_rota(_chave, get_current_lang()), _chave)
        _padrao = self.cmb_rota_agua.findData(rotas_de_agua.ROTA_PADRAO)
        if _padrao >= 0:
            self.cmb_rota_agua.setCurrentIndex(_padrao)
        self.cmb_rota_agua.currentIndexChanged.connect(self._aplicar_rota_de_agua)
        form_r.addRow(QLabel(tr("Água substituída pelo sistema:")), self.cmb_rota_agua)

        self.lbl_rota_aviso = QLabel("")
        self.lbl_rota_aviso.setWordWrap(True)
        self.lbl_rota_aviso.setStyleSheet(
            "color: #7c2d12; font-size: 11px; font-weight: bold; "
            "background-color: #fef3c7; border: 1px solid #fbbf24; "
            "border-radius: 4px; padding: 5px;"
        )
        self.lbl_rota_aviso.setVisible(False)
        form_r.addRow("", self.lbl_rota_aviso)

        self.lbl_rota_fonte = QLabel("")
        self.lbl_rota_fonte.setWordWrap(True)
        self.lbl_rota_fonte.setStyleSheet("color: #475569; font-size: 11px;")
        form_r.addRow("", self.lbl_rota_fonte)


        lay_r.addLayout(form_r)
        lay_cols.addWidget(gb_right, stretch=1)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # ── INICIALIZA JUSTIFICATIVAS INICIAIS ──
        self._update_lower_density_justification()
        self._update_lower_co2_justification()
        self._update_upper_density_justification()
        self._update_upper_co2_justification()
        self._update_pump_co2_justification()
        self._mostrar_procedencia_da_base()
        self._mostrar_procedencia_da_rota()

        # ── BOTÕES DE SALVAR E CANCELAR ──
        btns = QHBoxLayout()

        btn_resync = QPushButton(tr("🔄 Restaurar do Projeto (Etapa 3)"))
        btn_resync.setStyleSheet("padding: 6px 14px; color: #0369a1; border: 1px solid #bae6fd; border-radius: 4px;")
        btn_resync.clicked.connect(self._resync_from_project)
        btns.addWidget(btn_resync)
        btns.addStretch()

        btn_cancel = QPushButton(tr("Cancelar"))
        btn_cancel.setStyleSheet("padding: 6px 16px;")
        btn_cancel.clicked.connect(self.reject)
        btns.addWidget(btn_cancel)

        btn_save = QPushButton(tr("💾 Salvar Parâmetros e Recalcular"))
        btn_save.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 6px 18px;")
        btn_save.clicked.connect(self.save_and_accept)
        btns.addWidget(btn_save)

        main_layout.addLayout(btns)

    def _aplicar_rota_de_agua(self):
        """Reescreve o abatimento por m3 com o valor da rota escolhida.

        As rotas dominadas por eletricidade - a dessalinizacao a frente - sao
        recalculadas com o fator de rede que estiver no formulario, e nao com o
        da matriz do pais onde a fonte foi publicada. Com a matriz brasileira a
        dessalinizacao sai perto do tratamento convencional; com uma matriz
        carvoeira, varias vezes acima. Fixar um numero unico esconderia isso.
        """
        chave = self.cmb_rota_agua.currentData()
        if not chave or not hasattr(self, "txt_potable_co2"):
            # O combo e montado antes do campo; durante a construcao nao ha o
            # que reescrever ainda.
            return

        try:
            fator_da_rede = float(str(self.txt_grid_co2.text()).replace(",", "."))
        except ValueError:
            fator_da_rede = grid_factor_default()

        valor = rotas_de_agua.co2_evitado_por_m3(chave, fator_da_rede)
        self.txt_potable_co2.setText(f"{valor:.3f}")
        self._mostrar_procedencia_da_rota()

    def _mostrar_procedencia_da_rota(self):
        """Escreve fonte, tecnologia, matriz e fronteira da rota selecionada.

        Separado de `_aplicar_rota_de_agua` porque a abertura do diálogo precisa
        do rótulo e NÃO pode reescrever o fator: apagaria um valor editado à mão.
        """
        chave = self.cmb_rota_agua.currentData()
        if not chave or not hasattr(self, "lbl_rota_fonte"):
            return

        procedencia = rotas_de_agua.procedencia_da_rota(chave)
        partes = []
        if procedencia.get("tecnologia"):
            partes.append(tr("Tecnologia") + ": " + str(procedencia["tecnologia"]) + ".")
        if procedencia.get("faixa"):
            _min, _max = procedencia["faixa"][0], procedencia["faixa"][-1]
            partes.append(tr("Faixa publicada") + f": {_min:.3f} a {_max:.3f} kg CO2e/m3.")
        partes.append(procedencia.get("fonte", ""))
        if procedencia.get("matriz_da_fonte"):
            partes.append(tr("Matriz assumida pela fonte") + ": " + procedencia["matriz_da_fonte"] + ".")
        if procedencia.get("fronteira"):
            partes.append(tr("Fronteira") + ": " + str(procedencia["fronteira"]))
        if procedencia.get("observacao"):
            partes.append(procedencia["observacao"])
        self.lbl_rota_fonte.setText(" ".join(x for x in partes if x))

        # Rotas de fronteira parcial subestimam por construcao. Deixa-las
        # escolhiveis sem aviso seria repetir, com outro nome, o defeito de
        # publicar numero sem procedencia.
        if hasattr(self, "lbl_rota_aviso"):
            incompleta = rotas_de_agua.fronteira_e_incompleta(chave)
            self.lbl_rota_aviso.setVisible(incompleta)
            # Limpar o texto, e nao so esconder: um rotulo escondido que guarda
            # o aviso da rota anterior mente sobre a rota atual.
            self.lbl_rota_aviso.setText("")
            if incompleta:
                self.lbl_rota_aviso.setText(tr(
                    "⚠ Fronteira incompleta. Esta rota subestima por construção e serve como "
                    "LIMITE INFERIOR, não como estimativa central da emissão evitada. Para o "
                    "valor central, use a base do programa ou uma das rotas de Vaz et al. (2025)."
                ))

    def _aplicar_base_da_rede(self):
        """Reescreve o fator da rede com o valor da base escolhida.

        As bases nao sao intercambiaveis: a serie do MCTI contabiliza CO2 apenas,
        e apenas da geracao, ao passo que as demais sao CO2-equivalente com
        fronteira mais larga. Trocar uma pela outra sem dizer qual e qual foi o
        que produziu a divergencia de quase duas vezes entre modulos.
        """
        chave = self.cmb_base_rede.currentData()
        if not chave or not hasattr(self, "txt_grid_co2"):
            return

        self.txt_grid_co2.setText(f"{fator_co2eq_da_base(chave):.4f}")
        self._mostrar_procedencia_da_base()

        # A rota da agua depende do fator da rede quando e dominada por energia.
        if hasattr(self, "cmb_rota_agua"):
            self._aplicar_rota_de_agua()

    def _mostrar_procedencia_da_base(self):
        """Escreve a fonte, o gas e a fronteira da base selecionada.

        Separado de `_aplicar_base_da_rede` porque a abertura do dialogo precisa
        do rotulo e NAO pode reescrever o fator: apagaria um valor que o usuario
        tenha editado a mao.
        """
        chave = self.cmb_base_rede.currentData()
        if not chave or not hasattr(self, "lbl_base_rede_fonte"):
            return
        proc = procedencia_da_base(chave)
        partes = [proc.get("fonte", "")]
        if proc.get("gas"):
            partes.append(tr("Gás contabilizado") + ": " + str(proc["gas"]) + ".")
        if proc.get("fronteira"):
            partes.append(tr("Fronteira") + ": " + str(proc["fronteira"]) + ".")
        if proc.get("observacao"):
            partes.append(str(proc["observacao"]))
        self.lbl_base_rede_fonte.setText(" ".join(x for x in partes if x))

    def _apply_material_preset(self, combo, density_field, co2_field):
        key = combo.currentData() or "PEAD"
        density, co2 = material_preset_values(key)
        density_field.setText(f"{density:.1f}")
        co2_field.setText(f"{co2:.2f}")
        # Atualiza justificativas dos campos
        if combo == self.combo_lower_mat:
            self._update_lower_density_justification()
            self._update_lower_co2_justification()
        elif combo == self.combo_upper_mat:
            self._update_upper_density_justification()
            self._update_upper_co2_justification()

    def _update_lower_density_justification(self):
        """Atualiza a justificativa do campo de densidade da cisterna inferior."""
        key = self.combo_lower_mat.currentData() or "PEAD"
        just = get_material_justification(key, "density")
        if isinstance(self.txt_lower_density, JustifiedLineEdit):
            self.txt_lower_density.set_justification(just)

    def _update_lower_co2_justification(self):
        """Atualiza a justificativa do campo de CO2 da cisterna inferior."""
        key = self.combo_lower_mat.currentData() or "PEAD"
        just = get_material_justification(key, "co2_factor")
        if isinstance(self.txt_lower_co2_kg, JustifiedLineEdit):
            self.txt_lower_co2_kg.set_justification(just)

    def _update_upper_density_justification(self):
        """Atualiza a justificativa do campo de densidade da caixa superior."""
        key = self.combo_upper_mat.currentData() or "PEAD"
        just = get_material_justification(key, "density")
        if isinstance(self.txt_upper_density, JustifiedLineEdit):
            self.txt_upper_density.set_justification(just)

    def _update_upper_co2_justification(self):
        """Atualiza a justificativa do campo de CO2 da caixa superior."""
        key = self.combo_upper_mat.currentData() or "PEAD"
        just = get_material_justification(key, "co2_factor")
        if isinstance(self.txt_upper_co2_kg, JustifiedLineEdit):
            self.txt_upper_co2_kg.set_justification(just)

    def _update_pump_co2_justification(self):
        """Exibe a justificativa da emissão de fabricação da motobomba.

        Era um `pass`: o método existia apenas para não quebrar os signals, e a
        motobomba ficava sem justificativa visível — o único fator do módulo
        ambiental cuja procedência continua sendo extrapolação aritmética a
        partir do valor de meio cavalo. É o que a nota abaixo declara.
        """
        if not isinstance(getattr(self, "txt_pump_co2", None), JustifiedLineEdit):
            return
        try:
            cv = float(str(self.txt_pump_cv.text()).replace(",", "."))
        except (ValueError, AttributeError):
            cv = 0.5

        # O dicionário é indexado pelas seis potências comerciais; a mais
        # próxima é a que descreve o valor exibido.
        potencias = (0.25, 0.5, 0.75, 1.0, 1.5, 2.0)
        proxima = min(potencias, key=lambda x: abs(x - cv))
        just = get_pump_justification(proxima)

        if just is not None and pump_embodied_co2_is_extrapolated(proxima):
            just = replace(
                just,
                detailed_explanation=(
                    "VALOR EXTRAPOLADO — a emissão de fabricação desta potência não foi "
                    "medida nem publicada: resulta de escalonamento aritmético a partir "
                    "do valor de 0,5 CV. Trate-a como ordem de grandeza.\n\n"
                    + just.detailed_explanation
                ),
            )
        self.txt_pump_co2.set_justification(just)

    def _on_lower_material_changed(self):
        self._apply_material_preset(self.combo_lower_mat, self.txt_lower_density, self.txt_lower_co2_kg)

    def _on_upper_material_changed(self):
        self._apply_material_preset(self.combo_upper_mat, self.txt_upper_density, self.txt_upper_co2_kg)

    def _resync_from_project(self):
        snap = self.tab_env.sync_from_project(force=True)
        self._sync = snap
        self._populate_from_tab_env()

    def _populate_from_tab_env(self):
        te = self.tab_env
        self.combo_lower_mat.setCurrentIndex(self.combo_lower_mat.findData(te.combo_lower_mat.currentData()))
        self.txt_lower_density.setText(te.txt_lower_density.text())
        self.txt_lower_co2_kg.setText(te.txt_lower_co2_kg.text())
        self.chk_upper_used.setChecked(te.chk_upper_used.isChecked())
        self.combo_upper_mat.setCurrentIndex(self.combo_upper_mat.findData(te.combo_upper_mat.currentData()))
        self.txt_upper_vol.setText(te.txt_upper_vol.text())
        self.txt_upper_density.setText(te.txt_upper_density.text())
        self.txt_upper_co2_kg.setText(te.txt_upper_co2_kg.text())
        self.txt_pipe_50_m.setText(te.txt_pipe_50_m.text())
        self.txt_pipe_75_m.setText(te.txt_pipe_75_m.text())
        self.txt_pipe_100_m.setText(te.txt_pipe_100_m.text())
        self.txt_pipe_150_m.setText(te.txt_pipe_150_m.text())
        self.txt_pipe_50_co2.setText(te.txt_pipe_50_co2.text())
        self.txt_pipe_75_co2.setText(te.txt_pipe_75_co2.text())
        self.txt_pipe_100_co2.setText(te.txt_pipe_100_co2.text())
        self.txt_pipe_150_co2.setText(te.txt_pipe_150_co2.text())
        self.txt_pump_cv.setText(te.txt_pump_cv.text())
        self.txt_pump_co2.setText(te.txt_pump_co2.text())
        self.txt_pump_kwh.setText(te.txt_pump_kwh.text())
        self.txt_grid_co2.setText(te.txt_grid_co2.text())
        self.txt_potable_co2.setText(te.txt_potable_co2.text())
        self.txt_chlorine_dose.setText(te.txt_chlorine_dose.text())
        self.txt_chlorine_co2.setText(te.txt_chlorine_co2.text())
        self.txt_lifespan.setText(te.txt_lifespan.text())
        self.txt_chlorine_purity.setText(
            f"{getattr(te, '_pureza_do_cloro', PUREZA_PADRAO_DO_CLORO):.2f}")
        _ib = self.cmb_base_rede.findData(getattr(te, '_base_do_fator_da_rede', BASE_PADRAO_DA_REDE))
        if _ib >= 0:
            self.cmb_base_rede.setCurrentIndex(_ib)

        # Atualiza justificativas após carregar os valores
        self._update_lower_density_justification()
        self._update_lower_co2_justification()
        self._update_upper_density_justification()
        self._update_upper_co2_justification()
        self._update_pump_co2_justification()
        self.txt_pump_kwh.setText(te.txt_pump_kwh.text())
        self.txt_grid_co2.setText(te.txt_grid_co2.text())
        self.txt_potable_co2.setText(te.txt_potable_co2.text())
        self.txt_chlorine_dose.setText(te.txt_chlorine_dose.text())
        self.txt_chlorine_co2.setText(te.txt_chlorine_co2.text())
        self.txt_lifespan.setText(te.txt_lifespan.text())

    def save_and_accept(self):
        """Salva as alterações de volta na aba TabEnvironmental e executa o recálculo."""
        te = self.tab_env
        pipe_fields = list(self.txt_pipes_m.values())
        if any(not field.text().strip() for field in pipe_fields):
            QMessageBox.warning(
                self,
                tr("Configuração incompleta"),
                tr("Informe os metros de tubulação para todos os diâmetros. "
                   "Use 0 quando um diâmetro não fizer parte do projeto."),
            )
            return
        try:
            if any(float(field.text().replace(',', '.')) < 0 for field in pipe_fields):
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self,
                tr("Valor inválido"),
                tr("Os comprimentos de tubulação devem ser números maiores ou iguais a zero."),
            )
            return

        te.combo_lower_mat.setCurrentIndex(self.combo_lower_mat.currentIndex())
        te.txt_lower_density.setText(self.txt_lower_density.text())
        te.txt_lower_co2_kg.setText(self.txt_lower_co2_kg.text())

        te.chk_upper_used.setChecked(self.chk_upper_used.isChecked())
        te.combo_upper_mat.setCurrentIndex(self.combo_upper_mat.currentIndex())
        te.txt_upper_vol.setText(self.txt_upper_vol.text())
        te.txt_upper_density.setText(self.txt_upper_density.text())
        te.txt_upper_co2_kg.setText(self.txt_upper_co2_kg.text())

        # Salva comprimentos e fatores de todas as bitolas comerciais
        for dn, txt_f in self.txt_pipes_m.items():
            if hasattr(te, 'txt_pipes_m') and dn in te.txt_pipes_m:
                te.txt_pipes_m[dn].setText(txt_f.text())
        for dn, txt_f in self.txt_pipes_co2.items():
            if hasattr(te, 'txt_pipes_co2') and dn in te.txt_pipes_co2:
                te.txt_pipes_co2[dn].setText(txt_f.text())

        # Atualiza campos legados
        te.txt_pipe_50_m.setText(self.txt_pipe_50_m.text())
        te.txt_pipe_50_co2.setText(self.txt_pipe_50_co2.text())
        te.txt_pipe_75_m.setText(self.txt_pipe_75_m.text())
        te.txt_pipe_75_co2.setText(self.txt_pipe_75_co2.text())
        te.txt_pipe_100_m.setText(self.txt_pipe_100_m.text())
        te.txt_pipe_100_co2.setText(self.txt_pipe_100_co2.text())
        te.txt_pipe_150_m.setText(self.txt_pipe_150_m.text())
        te.txt_pipe_150_co2.setText(self.txt_pipe_150_co2.text())

        te.txt_pump_cv.setText(self.txt_pump_cv.text())
        te.txt_pump_co2.setText(self.txt_pump_co2.text())
        te.txt_pump_kwh.setText(self.txt_pump_kwh.text())

        te.txt_grid_co2.setText(self.txt_grid_co2.text())
        te.txt_potable_co2.setText(self.txt_potable_co2.text())
        te.txt_chlorine_dose.setText(self.txt_chlorine_dose.text())
        te.txt_chlorine_co2.setText(self.txt_chlorine_co2.text())
        te.txt_lifespan.setText(self.txt_lifespan.text())

        # A pureza e a base nomeada nao tem campo proprio na aba; ficam no
        # estado dela, de onde `get_config` as le.
        try:
            te._pureza_do_cloro = max(0.01, min(1.0,
                float(str(self.txt_chlorine_purity.text()).replace(',', '.'))))
        except ValueError:
            te._pureza_do_cloro = PUREZA_PADRAO_DO_CLORO
        te._base_do_fator_da_rede = self.cmb_base_rede.currentData() or BASE_PADRAO_DA_REDE

        # Sincroniza todos os comprimentos de tubulação com a configuração global do projeto (CAPEX)
        cfg = getattr(te.window(), "config", None) if te.window() else None
        if cfg and hasattr(cfg, "set_pipe_length"):
            def _parse_len(txt):
                try:
                    return max(0.0, float(txt.replace('.', '').replace(',', '.')))
                except ValueError:
                    return 0.0
            for dn, txt_f in self.txt_pipes_m.items():
                cfg.set_pipe_length(dn, _parse_len(txt_f.text()))

        te._params_customized = True
        te.recalculate_and_update()
        self.accept()


class TabEnvironmental(QWidget):
    """
    Aba Principal da Etapa 6: Otimizador Ambiental & Análise do Ciclo de Vida.
    """
    environmental_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_lca_result = None
        self._last_sweep_lca = None
        self._last_sync_snapshot = {}
        self._params_customized = False
        self.environmental_optimum_volume = None
        self._user_selected_env_vol = None
        self.init_ui()

    def init_ui(self):
        is_dark = get_current_theme() == "dark"
        heading = "#f4f4f5" if is_dark else "#0f172a"
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 34, 40, 40)
        main_layout.setSpacing(16)

        # ── ELEMENTOS DE ARMAZENAMENTO OCULTOS PARA COMPATIBILIDADE ──
        self._init_hidden_storage_elements()

        # ── CABEÇALHO COM SELETOR DE VOLUME E BOTÃO DE PARÂMETROS ──
        top_bar = QHBoxLayout()
        lbl_step_title = QLabel(tr("Desempenho ambiental e ESG"))
        lbl_step_title.setStyleSheet("font-family: Georgia, 'Times New Roman', serif; font-size: 24px; font-weight: 700; color: #133c32;")
        top_bar.addWidget(lbl_step_title)
        top_bar.addSpacing(15)

        lbl_vol_sel = QLabel(tr("Referência (ótimo ambiental):"))
        lbl_vol_sel.setStyleSheet(f"font-weight: bold; color: {heading};")
        top_bar.addWidget(lbl_vol_sel)

        self.combo_env_active_volume = QComboBox()
        self.combo_env_active_volume.setMinimumWidth(160)
        self.combo_env_active_volume.setStyleSheet("font-weight: bold; padding: 3px 8px; border-radius: 4px; border: 1px solid #cbd5e1; background-color: #ffffff; color: #0f172a;")
        self.combo_env_active_volume.currentIndexChanged.connect(self._on_env_volume_changed)
        top_bar.addWidget(self.combo_env_active_volume)

        top_bar.addStretch()

        self.btn_open_params = QPushButton(tr("⚙️ Configurar Parâmetros da ACV (Materiais, Tubos e Emissões)..."))
        self.btn_open_params.setProperty("primary", True)
        self.btn_open_params.clicked.connect(self.open_parameters_dialog)
        top_bar.addWidget(self.btn_open_params)

        main_layout.addLayout(top_bar)

        # ── ÁREA ROLÁVEL PRINCIPAL DA ETAPA 6 ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll_widget = QWidget()
        lay_scroll = QVBoxLayout(scroll_widget)
        lay_scroll.setContentsMargins(0, 0, 0, 0)
        lay_scroll.setSpacing(12)

        # ── CARDS DE KPI AMBIENTAIS SINTÉTICOS ──
        grid_kpi = QGridLayout()
        grid_kpi.setSpacing(8)

        self.card_emb_co2 = self._create_kpi_card(tr("Emissão Incorporada Total"), "-- kg", tr("Fabricação de Materiais (+kg)"), "#0284c7", is_dark)
        self.card_ann_avoided = self._create_kpi_card(tr("CO2 Evitado Anualmente"), "-- kg/ano", tr("Retirada da Rede (-kg/ano)"), "#059669", is_dark)
        self.card_env_pb = self._create_kpi_card(tr("Payback Ambiental"), "-- anos", tr("Recuperação do CO2"), "#d97706", is_dark)
        self.card_net_20yr = self._create_kpi_card(tr("Saldo Líquido em 20 Anos"), "-- kg", tr("Balanço Final (- Retirada / + Emissão)"), "#16a34a", is_dark)
        self.card_opt_vol = self._create_kpi_card(tr("Volume Ótimo Ambiental"), "-- L", tr("Maior Retirada de CO2"), "#6366f1", is_dark)

        grid_kpi.addWidget(self.card_emb_co2, 0, 0)
        grid_kpi.addWidget(self.card_ann_avoided, 0, 1)
        grid_kpi.addWidget(self.card_env_pb, 0, 2)
        grid_kpi.addWidget(self.card_net_20yr, 0, 3)
        grid_kpi.addWidget(self.card_opt_vol, 0, 4)

        lay_scroll.addLayout(grid_kpi)

        self.lbl_chlorination_summary = QLabel(tr("Cloração calculada: --"))
        self.lbl_chlorination_summary.setWordWrap(True)
        self.lbl_chlorination_summary.setStyleSheet(
            "background: #f0fdf4; border: 1px solid #86efac; color: #166534; "
            "border-radius: 5px; padding: 6px 10px; font-weight: 600;"
        )
        lay_scroll.addWidget(self.lbl_chlorination_summary)

        # ── TABELA DO INVENTÁRIO DE CICLO DE VIDA (ICV) ──
        gb_icv = QGroupBox(tr("📋 Inventário de Ciclo de Vida Simplificado (ICV — ISO 14040/14044)"))
        gb_icv.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        lay_icv = QVBoxLayout(gb_icv)
        lay_icv.setContentsMargins(8, 12, 8, 8)

        self.table_icv = QTableWidget()
        self.table_icv.setColumnCount(5)
        self.table_icv.setHorizontalHeaderLabels([
            tr("Fase / Componente do Sistema"),
            tr("Quantidade / Dimensão"),
            tr("CO2 Incorporado (+ kg)"),
            tr("CO2 Operacional (kg/ano) [- Retirada / + Emissão]"),
            tr("Fonte de Dados / Referência")
        ])
        header = self.table_icv.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_icv.setMinimumHeight(170)

        lay_icv.addWidget(self.table_icv)
        lay_scroll.addWidget(gb_icv)

        # ── SUB-ABAS DE GRÁFICOS AMBIENTAIS ──
        self.tab_charts_env = QTabWidget()

        # Sub-aba 1: indicadores complementares — evita gráficos duplicados.
        tab_env_1 = QWidget()
        lay_te1 = QHBoxLayout(tab_env_1)
        lay_te1.setSpacing(10)

        gb_c1 = QGroupBox(tr("Composição do Balanço de Carbono (20 Anos)"))
        lay_c1 = QVBoxLayout(gb_c1)
        self.chart_opt = EnvironmentalBalanceSummaryChart()
        self.chart_opt.set_canvas_height_range(minimum=340, maximum=480)
        lay_c1.addWidget(self.chart_opt)
        lay_te1.addWidget(gb_c1, stretch=1)

        gb_c2 = QGroupBox(tr("Comparativo de Emissão de CO2 (Com vs Sem Aproveitamento)"))
        lay_c2 = QVBoxLayout(gb_c2)
        self.chart_payback = CO2ComparisonChart()
        self.chart_payback.set_canvas_height_range(minimum=340, maximum=480)
        lay_c2.addWidget(self.chart_payback)
        lay_te1.addWidget(gb_c2, stretch=1)

        self.tab_charts_env.addTab(tab_env_1, tr("📊 Otimização de Volume & Consumo de Água"))

        # Sub-tab 2: Balanço Acumulado de CO2 por Volume (SEM COMPARATIVO REDUNDANTE — FIGURA MAIS LARGA)
        tab_env_2 = QWidget()
        lay_te2 = QVBoxLayout(tab_env_2)
        lay_te2.setContentsMargins(12, 8, 12, 8)

        gb_c4 = QGroupBox(tr("Balanço Acumulado de CO2 por Volume (Impactos Positivos vs Offset Negativo)"))
        gb_c4.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {heading}; }}")
        lay_c4 = QVBoxLayout(gb_c4)
        self.chart_component_breakdown = LCAComponentBreakdownChart()
        self.chart_component_breakdown.set_canvas_height_range(minimum=300, maximum=420)
        lay_c4.addWidget(self.chart_component_breakdown)
        lay_te2.addWidget(gb_c4)

        self.tab_charts_env.addTab(tab_env_2, tr("🍃 Balanço Acumulado de CO2 por Volume"))

        # Sub-tab 3: Relatório ESG & Pontuação de Certificações Ambientais
        tab_env_esg = QWidget()
        lay_esg = QVBoxLayout(tab_env_esg)
        lay_esg.setContentsMargins(12, 10, 12, 10)
        lay_esg.setSpacing(10)

        grid_esg = QGridLayout()
        grid_esg.setSpacing(10)

        self.card_leed = self._create_kpi_card(tr("Selo LEED v4 WE (Máx: 8 pts)"), "--", tr("Máximo de 8 pontos possíveis"), "#16a34a", is_dark)
        self.card_aqua = self._create_kpi_card(tr("Processo AQUA-HQE (Gestão da Água)"), "--", tr("Categoria 4 — Desempenho"), "#0284c7", is_dark)
        self.card_casa_azul = self._create_kpi_card(tr("Selo Casa Azul CAIXA"), "--", tr("Critério de Conservação"), "#0ea5e9", is_dark)
        self.card_gri = self._create_kpi_card(tr("GRI 303: Água Evitada da Rede"), "-- m³/ano", tr("Pegada Hídrica Preservada"), "#059669", is_dark)
        self.card_edge = self._create_kpi_card(
            tr("EDGE (IFC): Barra de Água"), "--%",
            tr("Limiar de 20% — o EDGE não pontua"), "#b45309", is_dark)

        grid_esg.addWidget(self.card_leed, 0, 0)
        grid_esg.addWidget(self.card_aqua, 0, 1)
        grid_esg.addWidget(self.card_casa_azul, 1, 0)
        grid_esg.addWidget(self.card_gri, 1, 1)
        grid_esg.addWidget(self.card_edge, 2, 0, 1, 2)
        lay_esg.addLayout(grid_esg)

        # Caso-base do EDGE. O aplicativo do IFC fixa um consumo de referencia
        # local, que o Netuno nao tem como saber; quem informa e o usuario.
        row_edge = QHBoxLayout()
        row_edge.addWidget(QLabel(
            tr("Caso-base de consumo do EDGE (L/pessoa·dia, opcional):")))
        self.txt_edge_base = QLineEdit()
        self.txt_edge_base.setPlaceholderText(tr("em branco: usa a demanda do projeto"))
        self.txt_edge_base.setFixedWidth(150)
        self.txt_edge_base.setToolTip(tr(
            "O EDGE mede a economia contra um caso-base local, que varia por país e "
            "tipologia e é fixado pelo aplicativo. Em branco, o Netuno usa a demanda "
            "modelada do projeto — que é um piso, não o número da certificação."))
        row_edge.addWidget(self.txt_edge_base)
        row_edge.addStretch()
        lay_esg.addLayout(row_edge)

        self.lbl_esg_summary_box = QLabel(tr("Síntese Executiva ESG: Execute a simulação para gerar o relatório de créditos ambientais."))
        self.lbl_esg_summary_box.setWordWrap(True)
        self.lbl_esg_summary_box.setStyleSheet(f"""
            background: {'#14532d' if is_dark else '#f0fdf4'};
            border: 1.5px solid {'#16a34a' if is_dark else '#86efac'};
            color: {'#bbf7d0' if is_dark else '#166534'};
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 11.5px;
            font-weight: 500;
        """)
        lay_esg.addWidget(self.lbl_esg_summary_box)

        # ── Tabela Detalhada de Pontuação e Conformidade Normativa ──
        lbl_tbl_title = QLabel(tr("📋 Matriz de Pontuação e Conformidade de Certificações Ambientais"))
        lbl_tbl_title.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#38bdf8' if is_dark else '#0369a1'}; margin-top: 6px;")
        lay_esg.addWidget(lbl_tbl_title)

        self.table_esg_breakdown = QTableWidget()
        self.table_esg_breakdown.setColumnCount(5)
        self.table_esg_breakdown.setHorizontalHeaderLabels([
            tr("Certificação"),
            tr("Crédito / Código"),
            tr("Foco / Aplicação"),
            tr("Desempenho no Projeto"),
            tr("Pontuação / Status")
        ])
        h_esg = self.table_esg_breakdown.horizontalHeader()
        h_esg.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h_esg.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h_esg.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h_esg.setSectionResizeMode(3, QHeaderView.Stretch)
        h_esg.setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_esg_breakdown.setMinimumHeight(180)
        lay_esg.addWidget(self.table_esg_breakdown)

        # ── Painel Didático e Explicativo: Como Cada Certificação Avalia o Sistema ──
        lbl_info_title = QLabel(tr("📖 Metodologia de Avaliação: Como Cada Certificação Considera o Aproveitamento Pluvial"))
        lbl_info_title.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#38bdf8' if is_dark else '#0369a1'}; margin-top: 6px;")
        lay_esg.addWidget(lbl_info_title)

        self.browser_esg_info = QTextBrowser()
        self.browser_esg_info.setOpenExternalLinks(True)
        self.browser_esg_info.setMinimumHeight(240)
        info_bg = "#18181b" if is_dark else "#f8fafc"
        info_border = "#3f3f46" if is_dark else "#cbd5e1"
        self.browser_esg_info.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {info_bg};
                border: 1px solid {info_border};
                border-radius: 6px;
                padding: 10px;
            }}
        """)
        self.browser_esg_info.setHtml(self._get_esg_methodology_html(is_dark))
        lay_esg.addWidget(self.browser_esg_info)

        self.tab_charts_env.addTab(tab_env_esg, tr("🌿 Certificações ESG (LEED / AQUA / Casa Azul)"))

        self.tab_charts_env.currentChanged.connect(self._on_charts_tab_changed)
        self._on_charts_tab_changed(0)

        lay_scroll.addWidget(self.tab_charts_env)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

    def _on_charts_tab_changed(self, index: int):
        if index in (0, 1):
            # Abas 0 e 1: gráficos otimização e balanço de carbono com altura confortável e legível
            self.tab_charts_env.setMinimumHeight(0)
            self.tab_charts_env.setMaximumHeight(520)
        else:
            # Aba 2: Relatório ESG & Certificações Sustentáveis com tabela e síntese
            self.tab_charts_env.setMaximumHeight(16777215)
            self.tab_charts_env.setMinimumHeight(720)
        self.tab_charts_env.updateGeometry()

    def _init_hidden_storage_elements(self):
        """Campos ocultos para armazenar os valores usados na sincronização com LCAParametersDialog."""
        pead = MATERIAL_PRESETS["PEAD"]

        self.combo_lower_mat = QComboBox()
        self.combo_upper_mat = QComboBox()
        for key, preset in MATERIAL_PRESETS.items():
            self.combo_lower_mat.addItem(tr(preset.name), key)
            self.combo_upper_mat.addItem(tr(preset.name), key)
        self.combo_lower_mat.setCurrentIndex(self.combo_lower_mat.findData("PEAD"))
        self.combo_upper_mat.setCurrentIndex(self.combo_upper_mat.findData("PEAD"))

        self.txt_lower_density = QLineEdit(f"{pead.material_density_kg_per_m3_tank:.1f}")
        self.txt_lower_co2_kg = QLineEdit(f"{pead.co2_factor_kg_per_kg:.2f}")

        self.chk_upper_used = QCheckBox()
        self.chk_upper_used.setChecked(True)
        self.txt_upper_vol = QLineEdit("500")
        self.txt_upper_density = QLineEdit(f"{pead.material_density_kg_per_m3_tank:.1f}")
        self.txt_upper_co2_kg = QLineEdit(f"{pead.co2_factor_kg_per_kg:.2f}")

        # Comprimentos e fatores de tubulação PVC (todas as bitolas comerciais NBR 5648 / SINAPI)
        self.txt_pipes_m = {}
        self.txt_pipes_co2 = {}
        for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
            def_m = "20.0" if dn == 100 else ("5.0" if dn == 32 else ("20.0" if dn == 25 else "0.0"))
            self.txt_pipes_m[dn] = QLineEdit(def_m)
            self.txt_pipes_co2[dn] = QLineEdit(f"{pipe_co2_factor(dn):.2f}")

        # Aliases retrocompatíveis
        self.txt_pipe_50_m = self.txt_pipes_m[50]
        self.txt_pipe_50_co2 = self.txt_pipes_co2[50]
        self.txt_pipe_75_m = self.txt_pipes_m[75]
        self.txt_pipe_75_co2 = self.txt_pipes_co2[75]
        self.txt_pipe_100_m = self.txt_pipes_m[100]
        self.txt_pipe_100_co2 = self.txt_pipes_co2[100]
        self.txt_pipe_150_m = self.txt_pipes_m[150]
        self.txt_pipe_150_co2 = self.txt_pipes_co2[150]

        default_cv = 0.5
        self.txt_pump_cv = QLineEdit(f"{default_cv:.2f}")
        self.txt_pump_co2 = QLineEdit(f"{PUMP_EMBEDDED_CO2.get(default_cv, 18.0):.1f}")
        # Até a versão 5.0.7 este campo nascia com 0,085 — o fator da rede
        # elétrica, copiado da linha seguinte. São grandezas diferentes, e o
        # padrão do modelo vem da física do bombeamento: a interface partia de um
        # valor várias vezes menor que o do motor.
        self.txt_pump_kwh = QLineEdit(f"{consumo_especifico_padrao_kwh_por_m3():.2f}")

        self.txt_grid_co2 = QLineEdit(f"{grid_factor_default():.4f}")
        self.txt_potable_co2 = QLineEdit("0.350")
        # Dose e fator ficam separados para tornar a massa anual de cloro
        # auditável; os padrões equivalem a 0,050 kg CO2e/m³.
        self.txt_chlorine_dose = QLineEdit(f"{DOSE_PADRAO_MG_POR_LITRO:.2f}")
        self.txt_chlorine_co2 = QLineEdit(f"{FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO:.2f}")
        self.txt_lifespan = QLineEdit("20")

    def _get_project_context(self):
        """Coleta config, simulação e edificação para sincronização da ACV."""
        mw = self.window()
        if not mw:
            return None, None, True, 500.0, 5000.0, 100.0

        cfg = getattr(mw, "config", None)
        ts = getattr(mw, "tab_tanks_simulation", None)
        sim = ts.last_single_result if ts else None

        upper_used = True
        upper_vol = getattr(cfg, "upper_tank_vol", 500.0) if cfg else 500.0
        
        # Prioriza o volume ótimo ambiental para referências de cálculo da ACV
        lower_vol = 5000.0
        if getattr(self, "environmental_optimum_volume", None) and self.environmental_optimum_volume > 0:
            lower_vol = float(self.environmental_optimum_volume)
        elif cfg and getattr(cfg, "econ_lower_tank_vol", 0) > 0:
            lower_vol = float(cfg.econ_lower_tank_vol)
        elif mw and hasattr(mw, "tab_economic_integrated") and mw.tab_economic_integrated.combo_active_volume.count() > 0:
            te_data = mw.tab_economic_integrated.combo_active_volume.currentData()
            if te_data is not None:
                lower_vol = float(te_data)
        elif sim and getattr(sim, "lower_tank_vol", 0) > 0:
            lower_vol = sim.lower_tank_vol

        capture_area = 100.0

        if ts:
            upper_used = ts.combo_upper_mode.currentIndex() != 2
            try:
                upper_vol = float(ts.txt_upper_vol.text().replace(",", "."))
            except ValueError:
                pass

        if hasattr(mw, "tab_building"):
            try:
                b_cfg = mw.tab_building.get_building_config()
                capture_area = float(b_cfg.get("area", 100.0))
            except Exception:
                pass

        return cfg, sim, upper_used, upper_vol, lower_vol, capture_area

    def has_technical_sweep(self) -> bool:
        """Indica se a varredura que define cisterna e bomba já foi executada."""
        mw = self.window()
        return bool(
            mw and hasattr(mw, "tab_tanks_simulation")
            and getattr(mw.tab_tanks_simulation, "last_sweep_result", None)
        )

    def sync_from_project(self, force: bool = False) -> dict:
        """
        Sincroniza parâmetros da ACV com Etapa 3 (simulação, motobomba, CAPEX).
        Respeita personalizações do usuário, a menos que force=True.
        """
        cfg, sim, upper_used, upper_vol, lower_vol, capture_area = self._get_project_context()
        if cfg is None:
            return self._last_sync_snapshot

        # Caso-base do EDGE: vem do projeto, e volta para ele ao calcular. Sem os
        # dois sentidos, o valor gravado no arquivo nunca chegaria à tela.
        if hasattr(self, 'txt_edge_base'):
            base_edge = float(getattr(cfg, 'edge_base_case_l_person_day', 0.0) or 0.0)
            if base_edge > 0.0 and not self.txt_edge_base.text().strip():
                self.txt_edge_base.setText(f"{base_edge:g}".replace(".", ","))

        # Sincroniza sempre os comprimentos de tubulação do CAPEX / projeto
        if hasattr(cfg, "get_pipe_length"):
            for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
                if hasattr(self, 'txt_pipes_m') and dn in self.txt_pipes_m:
                    self.txt_pipes_m[dn].setText(f"{cfg.get_pipe_length(dn):.1f}")
            self.txt_pipe_50_m.setText(f"{cfg.get_pipe_length(50):.1f}")
            self.txt_pipe_75_m.setText(f"{cfg.get_pipe_length(75):.1f}")
            self.txt_pipe_100_m.setText(f"{cfg.get_pipe_length(100):.1f}")
            self.txt_pipe_150_m.setText(f"{cfg.get_pipe_length(150):.1f}")

        if not self.has_technical_sweep() and not force:
            return self._last_sync_snapshot
        if self._params_customized and not force:
            return self._last_sync_snapshot

        snap = build_sync_snapshot(
            cfg, sim,
            upper_used=upper_used,
            upper_vol_l=upper_vol,
            lower_vol_l=lower_vol,
            capture_area_m2=capture_area,
        )
        snap["lower_vol_l"] = lower_vol
        snap["upper_vol_l"] = upper_vol
        self._last_sync_snapshot = snap

        def _set(field, value, fmt="{}"):
            field.setText(fmt.format(value))

        idx_low = self.combo_lower_mat.findData(snap["lower_material_key"])
        if idx_low >= 0:
            self.combo_lower_mat.setCurrentIndex(idx_low)
        _set(self.txt_lower_density, snap["lower_density"], "{:.1f}")
        _set(self.txt_lower_co2_kg, snap["lower_co2_kg"], "{:.2f}")

        self.chk_upper_used.setChecked(bool(snap["upper_used"]))
        idx_up = self.combo_upper_mat.findData(snap["upper_material_key"])
        if idx_up >= 0:
            self.combo_upper_mat.setCurrentIndex(idx_up)
        _set(self.txt_upper_vol, snap["upper_vol_l"], "{:.0f}")
        _set(self.txt_upper_density, snap["upper_density"], "{:.1f}")
        _set(self.txt_upper_co2_kg, snap["upper_co2_kg"], "{:.2f}")

        pipes = snap["pipes_m"]
        pipe_co2 = snap["pipe_co2"]
        # Comprimentos de tubulação sincronizados com os dados de projeto / CAPEX
        if cfg and hasattr(cfg, "get_pipe_length"):
            for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
                if hasattr(self, 'txt_pipes_m') and dn in self.txt_pipes_m:
                    _set(self.txt_pipes_m[dn], cfg.get_pipe_length(dn), "{:.1f}")
            _set(self.txt_pipe_50_m, cfg.get_pipe_length(50), "{:.1f}")
            _set(self.txt_pipe_75_m, cfg.get_pipe_length(75), "{:.1f}")
            _set(self.txt_pipe_100_m, cfg.get_pipe_length(100), "{:.1f}")
            _set(self.txt_pipe_150_m, cfg.get_pipe_length(150), "{:.1f}")
        else:
            for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
                if hasattr(self, 'txt_pipes_m') and dn in self.txt_pipes_m:
                    _set(self.txt_pipes_m[dn], pipes.get(dn, 0.0), "{:.1f}")
            _set(self.txt_pipe_50_m, pipes.get(50, 0.0), "{:.1f}")
            _set(self.txt_pipe_75_m, pipes.get(75, 0.0), "{:.1f}")
            _set(self.txt_pipe_100_m, pipes.get(100, 0.0), "{:.1f}")
            _set(self.txt_pipe_150_m, pipes.get(150, 0.0), "{:.1f}")

        for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
            if hasattr(self, 'txt_pipes_co2') and dn in self.txt_pipes_co2:
                _set(self.txt_pipes_co2[dn], pipe_co2.get(dn, pipe_co2_factor(dn)), "{:.2f}")

        _set(self.txt_pipe_50_co2, pipe_co2.get(50, pipe_co2_factor(50)), "{:.2f}")
        _set(self.txt_pipe_75_co2, pipe_co2.get(75, pipe_co2_factor(75)), "{:.2f}")
        _set(self.txt_pipe_100_co2, pipe_co2.get(100, pipe_co2_factor(100)), "{:.2f}")
        _set(self.txt_pipe_150_co2, pipe_co2.get(150, pipe_co2_factor(150)), "{:.2f}")

        _set(self.txt_pump_cv, snap["pump_cv"], "{:.2f}")
        _set(self.txt_pump_co2, snap["pump_co2"], "{:.1f}")
        if snap["specific_kwh_per_m3"] > 0:
            _set(self.txt_pump_kwh, snap["specific_kwh_per_m3"], "{:.3f}")
        _set(self.txt_lifespan, snap["lifespan_years"], "{:.0f}")

        if force:
            self._params_customized = False

        return snap

    def open_parameters_dialog(self):
        dlg = LCAParametersDialog(self, parent=self)
        if dlg.exec():
            self._params_customized = True

    def _create_kpi_card(self, title, val_str, sub_str, border_color, is_dark):
        card = QFrame()
        card.setObjectName("kpi_card")
        bg_col = "#27272a" if is_dark else "#f8fafc"
        card.setStyleSheet(f"""
            QFrame#kpi_card {{
                background-color: {bg_col};
                border: 1px solid #cbd5e1;
                border-top: 3px solid {border_color};
                border-radius: 6px;
                padding: 6px;
            }}
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(2)

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {'#a1a1aa' if is_dark else '#64748b'};")
        lbl_t.setAlignment(Qt.AlignCenter)

        lbl_v = QLabel(val_str)
        lbl_v.setObjectName("lbl_val")
        lbl_v.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {'#ffffff' if is_dark else '#0f172a'};")
        lbl_v.setAlignment(Qt.AlignCenter)

        lbl_s = QLabel(sub_str)
        lbl_s.setObjectName("lbl_sub")
        lbl_s.setStyleSheet(f"font-size: 9.5px; color: {'#71717a' if is_dark else '#94a3b8'};")
        lbl_s.setAlignment(Qt.AlignCenter)

        lay.addWidget(lbl_t); lay.addWidget(lbl_v); lay.addWidget(lbl_s)
        return card

    def _update_kpi(self, card, text_val, sub_val=None):
        lbl = card.findChild(QLabel, "lbl_val")
        if lbl: lbl.setText(text_val)
        if sub_val is not None:
            lbl_s = card.findChild(QLabel, "lbl_sub")
            if lbl_s: lbl_s.setText(sub_val)

    def has_technical_sweep(self) -> bool:
        mw = self.window()
        if not mw or not hasattr(mw, 'tab_tanks_simulation'):
            return False
        ts = mw.tab_tanks_simulation
        if getattr(ts, "_is_technical_only", False):
            return False
        return ts.last_sweep_result is not None or ts.last_single_result is not None

    def clear_results(self):
        self._user_selected_env_vol = None
        self._show_empty_state()

    def _show_empty_state(self):
        """Exibe ACV zerada até o usuário executar a varredura completa."""
        self._last_lca_result = None
        self._last_sweep_lca = None
        self._update_kpi(self.card_emb_co2, "-- kg")
        self._update_kpi(self.card_ann_avoided, "-- kg/ano")
        self._update_kpi(self.card_env_pb, "--")
        self._update_kpi(self.card_net_20yr, "-- kg")
        self._update_kpi(self.card_opt_vol, "-- L")
        if hasattr(self, "lbl_chlorination_summary"):
            self.lbl_chlorination_summary.setText(tr("Cloração calculada: --"))
        if hasattr(self, "table_icv"):
            self.table_icv.setRowCount(0)

    def showEvent(self, event):
        super().showEvent(event)
        if self.has_technical_sweep():
            self.recalculate_and_update()
        else:
            self._show_empty_state()

    def get_config(self) -> EnvironmentalConfig:
        def parse_f(txt, def_v):
            try:
                return float(txt.replace(',', '.'))
            except Exception:
                return def_v

        def preset_or_none(material_key, value, preset_attr):
            preset = MATERIAL_PRESETS.get(material_key, MATERIAL_PRESETS["PEAD"])
            ref = getattr(preset, preset_attr)
            if abs(value - ref) < max(0.01, ref * 0.001):
                return None
            return value

        def pipe_co2_or_none(dn, value):
            ref = PIPE_EMISSION_FACTORS_PER_METER.get(dn, 3.92)
            if abs(value - ref) < 0.01:
                return None
            return value

        lower_key = self.combo_lower_mat.currentData() or "PEAD"
        upper_key = self.combo_upper_mat.currentData() or "PEAD"
        if upper_key == "FIBERGLASS":
            upper_key = "FIBRA"

        lower_density = parse_f(self.txt_lower_density.text(), MATERIAL_PRESETS[lower_key].material_density_kg_per_m3_tank)
        lower_co2 = parse_f(self.txt_lower_co2_kg.text(), MATERIAL_PRESETS[lower_key].co2_factor_kg_per_kg)
        upper_density = parse_f(self.txt_upper_density.text(), MATERIAL_PRESETS[upper_key].material_density_kg_per_m3_tank)
        upper_co2 = parse_f(self.txt_upper_co2_kg.text(), MATERIAL_PRESETS[upper_key].co2_factor_kg_per_kg)

        cfg, sim, upper_used, _, _, _ = self._get_project_context()

        # Constrói tubulações exatamente conforme definidas no projeto / CAPEX
        pipes = []
        capex_pipe_dict = {}
        if cfg and hasattr(cfg, "get_pipe_lengths_dict"):
            capex_pipe_dict = cfg.get_pipe_lengths_dict()

        for dn in (20, 25, 32, 40, 50, 60, 75, 85, 100, 110, 150):
            # A tubulação definida no CAPEX rege o quantitativo da ACV
            if self._params_customized and hasattr(self, 'txt_pipes_m') and dn in self.txt_pipes_m:
                len_val = parse_f(self.txt_pipes_m[dn].text(), 0.0)
            elif dn in capex_pipe_dict:
                len_val = float(capex_pipe_dict[dn])
            elif hasattr(self, 'txt_pipes_m') and dn in self.txt_pipes_m:
                len_val = parse_f(self.txt_pipes_m[dn].text(), 0.0)
            else:
                len_val = 0.0

            custom_co2_txt = self.txt_pipes_co2[dn].text() if (hasattr(self, 'txt_pipes_co2') and dn in self.txt_pipes_co2) else None
            custom_co2_val = parse_f(custom_co2_txt, pipe_co2_factor(dn)) if custom_co2_txt else pipe_co2_factor(dn)
            custom_co2 = pipe_co2_or_none(dn, custom_co2_val)

            if len_val > 0 or self._params_customized:
                pipes.append(PipeInput(diameter_mm=dn, length_m=len_val, custom_co2_per_m=custom_co2))

        pump_cv = parse_f(self.txt_pump_cv.text(), 0.5)
        pump_co2_val = parse_f(self.txt_pump_co2.text(), PUMP_EMBEDDED_CO2.get(pump_cv, 18.0))
        pump_co2 = None if abs(pump_co2_val - PUMP_EMBEDDED_CO2.get(pump_cv, pump_co2_val)) < 0.1 else pump_co2_val

        annual_pump_kwh = 0.0
        specific_kwh = parse_f(self.txt_pump_kwh.text(), consumo_especifico_padrao_kwh_por_m3())
        pump_count = 1

        if cfg is not None:
            pump_count = max(1, cfg.pump_count)
            if not self._params_customized or sim is not None:
                energy = compute_annual_pump_energy(cfg, sim, upper_tank_used=upper_used)
                if energy.annual_kwh > 0:
                    annual_pump_kwh = energy.annual_kwh
                if energy.specific_kwh_per_m3 > 0:
                    specific_kwh = energy.specific_kwh_per_m3
                if energy.pump_power_cv > 0 and not self._params_customized:
                    pump_cv = energy.pump_power_cv

        pump = PumpInput(
            power_cv=pump_cv,
            custom_embodied_co2=pump_co2,
            specific_kwh_per_m3=specific_kwh,
        )

        proj_cfg = getattr(self.window(), 'config', None) if self.window() else None

        return EnvironmentalConfig(
            lower_material_key=lower_key,
            custom_lower_density_kg_m3=preset_or_none(lower_key, lower_density, "material_density_kg_per_m3_tank"),
            custom_lower_co2_per_kg=preset_or_none(lower_key, lower_co2, "co2_factor_kg_per_kg"),
            upper_material_key=upper_key,
            custom_upper_density_kg_m3=preset_or_none(upper_key, upper_density, "material_density_kg_per_m3_tank"),
            custom_upper_co2_per_kg=preset_or_none(upper_key, upper_co2, "co2_factor_kg_per_kg"),
            upper_tank_vol_liters=parse_f(self.txt_upper_vol.text(), 500.0),
            upper_tank_used=self.chk_upper_used.isChecked(),
            pipes=pipes,
            pump=pump,
            pump_count=pump_count,
            annual_pump_kwh=annual_pump_kwh,
            grid_co2_factor_kg_kwh=parse_f(self.txt_grid_co2.text(), grid_factor_default()),
            potable_water_co2_kg_m3=parse_f(self.txt_potable_co2.text(), 0.350),
            chlorine_dose_mg_l=parse_f(self.txt_chlorine_dose.text(), 2.0),
            chlorine_co2_kg_per_kg=parse_f(self.txt_chlorine_co2.text(), FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO),
            # A pureza e a base nomeada nao tem campo nesta aba: sao editadas no
            # dialogo de parametros, que as deixa aqui. Sem esta linha o valor
            # escolhido seria ignorado, que e o defeito que ele corrige.
            chlorine_product_purity=max(0.01, min(1.0, float(
                getattr(self, '_pureza_do_cloro', PUREZA_PADRAO_DO_CLORO)))),
            grid_co2_factor_basis=str(
                getattr(self, '_base_do_fator_da_rede', BASE_PADRAO_DA_REDE)),
            system_lifespan_years=parse_f(self.txt_lifespan.text(), 20.0),
            # A escolha de desinfeccao vem da Etapa 2 e atravessa ate aqui: e o
            # que faz optar por ultravioleta mudar a emissao anual.
            water_quality_target_class=str(getattr(proj_cfg, 'water_quality_target_class', 'classe_1')),
            water_quality_disinfection=str(getattr(proj_cfg, 'water_quality_disinfection', 'cloro')),
            water_quality_polishing=bool(getattr(proj_cfg, 'water_quality_polishing', False)),
            roof_area_m2=float(getattr(proj_cfg, 'area', AREA_DE_RECURSO_M2) or AREA_DE_RECURSO_M2),
            etap_enabled=bool(getattr(proj_cfg, 'etap_enabled', True)),
        )

    def _edge_base_case_annual_m3(self):
        """Caso-base do EDGE em m3/ano, ou None quando nao foi declarado."""
        campo = getattr(self, 'txt_edge_base', None)
        if campo is None:
            return None
        texto = campo.text().strip().replace(',', '.')
        if not texto:
            return None
        try:
            litros = float(texto)
        except ValueError:
            return None
        if litros <= 0.0:
            return None
        cfg = getattr(self.window(), 'config', None)
        if cfg is not None:
            # Devolve ao projeto para que o valor sobreviva a salvar e reabrir.
            cfg.edge_base_case_l_person_day = litros
        pessoas = float(getattr(cfg, 'residents_count', 0) or 0)
        economias = float(getattr(cfg, 'num_economias', 1) or 1)
        if pessoas <= 0.0:
            return None
        return consumo_base_anual_m3(litros, pessoas * max(1.0, economias))

    def _on_env_volume_changed(self):
        cur_v = self.combo_env_active_volume.currentData()
        if cur_v is not None:
            self._user_selected_env_vol = float(cur_v)
        self.recalculate_and_update(from_combo=True)

    def recalculate_and_update(self, from_combo=False):
        mw = self.window()
        if not self.has_technical_sweep():
            self._show_empty_state()
            return

        if not self._params_customized and not from_combo:
            self.sync_from_project(force=False)

        cfg = self.get_config()

        sw_res_tech = None
        if mw and hasattr(mw, 'tab_tanks_simulation'):
            sw_res_tech = getattr(mw.tab_tanks_simulation, 'last_sweep_result', None)

        sweep_details = []
        opt_vol = 5000.0
        active_vol = None

        if sw_res_tech and getattr(sw_res_tech, 'results_by_volume', None):
            v_map = [(r.lower_tank_vol, r.annual_pluvial_consumed_m3) for r in sw_res_tech.results_by_volume]
            sw_res = run_environmental_sweep(v_map, cfg)
            self._last_sweep_lca = sw_res
            sweep_details = sw_res.sweep_details
            opt_vol = sw_res.best_lifetime_co2_vol_liters
            self.environmental_optimum_volume = float(opt_vol) if opt_vol is not None else None

            # Na aba de Desempenho Ambiental e ESG, o volume padrão de abertura deve ser
            # rigorosamente o Reservatório Ótimo Ambiental (maior CO2 líquido evitado).
            # Apenas se o usuário já tiver selecionado explicitamente outro volume no combo desta aba, preserva-se.
            user_chosen = getattr(self, "_user_selected_env_vol", None)
            preferred_vol = user_chosen if (from_combo and user_chosen is not None) else opt_vol

            # Atualiza o combo de seleção de volume se não veio de alteração manual do combo
            if not from_combo or self.combo_env_active_volume.count() == 0:
                self.combo_env_active_volume.blockSignals(True)
                self.combo_env_active_volume.clear()
                selected_idx = 0
                for idx, r in enumerate(sw_res_tech.results_by_volume):
                    v = r.lower_tank_vol
                    label = f"★ {format_ptbr(v, 0)} L ({tr('Ótimo Ambiental')})" if abs(v - opt_vol) < 1.0 else f"{format_ptbr(v, 0)} L"
                    self.combo_env_active_volume.addItem(label, v)
                    if abs(v - preferred_vol) < 1.0:
                        selected_idx = idx
                self.combo_env_active_volume.setCurrentIndex(selected_idx)
                self.combo_env_active_volume.blockSignals(False)

            cur_data = self.combo_env_active_volume.currentData()
            active_vol = float(cur_data) if cur_data is not None else preferred_vol
            # Encontra annual_m3 correspondente
            matching = [r for r in sw_res_tech.results_by_volume if abs(r.lower_tank_vol - active_vol) < 1.0]
            ann_m3 = matching[0].annual_pluvial_consumed_m3 if matching else sw_res_tech.results_by_volume[0].annual_pluvial_consumed_m3
        else:
            single_res = getattr(mw.tab_tanks_simulation, 'last_single_result', None) if (mw and hasattr(mw, 'tab_tanks_simulation')) else None
            active_vol = single_res.lower_tank_vol if single_res else 5000.0
            ann_m3 = single_res.annual_pluvial_consumed_m3 if single_res else 200.0
            opt_vol = active_vol

        lca_res = calculate_lca(active_vol, ann_m3, cfg)
        self._last_lca_result = lca_res

        self._update_kpi(self.card_emb_co2, f"+{format_ptbr(lca_res.total_embodied_co2_kg, 0)} kg")
        ann_av = lca_res.net_annual_avoided_co2_kg
        ann_av_str = f"-{format_ptbr(ann_av, 0)} kg/ano" if ann_av >= 0 else f"+{format_ptbr(abs(ann_av), 0)} kg/ano"
        self._update_kpi(self.card_ann_avoided, ann_av_str)
        
        pb_val = lca_res.environmental_payback_years
        pb_str = (
            f"{format_ptbr(pb_val, 1)} anos"
            if (pb_val is not None and not np.isnan(pb_val) and pb_val < 90)
            else ("> 50 anos" if pb_val is not None else "--")
        )
        self._update_kpi(self.card_env_pb, pb_str)
        
        # Saldo líquido em 20 anos: Negativo (-) = Retirada líquida, Positivo (+) = Emissão líquida
        net_saved = lca_res.lifetime_net_co2_saved_kg
        net_str = f"-{format_ptbr(net_saved, 0)} kg" if net_saved >= 0 else f"+{format_ptbr(abs(net_saved), 0)} kg"
        self._update_kpi(self.card_net_20yr, net_str)
        self._update_kpi(self.card_opt_vol, f"{format_ptbr(opt_vol, 0)} L")

        self.lbl_chlorination_summary.setText(
            tr("Cloração calculada: {mass} kg Cl2/ano ({dose} mg/L) · +{co2} kg CO2e/ano").format(
                mass=format_ptbr(lca_res.annual_chlorine_kg, 3),
                dose=format_ptbr(lca_res.chlorine_dose_mg_l, 2),
                co2=format_ptbr(lca_res.annual_treatment_co2_kg, 2),
            )
        )

        self.table_icv.setRowCount(len(lca_res.inventory_items))
        for row, item in enumerate(lca_res.inventory_items):
            self.table_icv.setItem(row, 0, QTableWidgetItem(tr(item.category)))
            self.table_icv.setItem(row, 1, QTableWidgetItem(item.quantity_str))
            
            emb_item = QTableWidgetItem(f"+{format_ptbr(item.embodied_co2_kg, 2)}" if item.embodied_co2_kg > 0 else "--")
            if item.embodied_co2_kg > 0:
                emb_item.setForeground(QColor("#dc2626"))  # Emissão incorporada (+) = Vermelho
            self.table_icv.setItem(row, 2, emb_item)

            if item.annual_op_co2_kg > 0:
                op_item = QTableWidgetItem(f"+{format_ptbr(item.annual_op_co2_kg, 2)}")
                op_item.setForeground(QColor("#dc2626"))  # Emissão operacional (+) = Vermelho
            elif item.annual_op_co2_kg < 0:
                op_item = QTableWidgetItem(f"{format_ptbr(item.annual_op_co2_kg, 2)}")  # Contém '-'
                op_item.setForeground(QColor("#16a34a"))  # Retirada/Evitada (-) = Verde
            else:
                op_item = QTableWidgetItem("--")
            self.table_icv.setItem(row, 3, op_item)
            self.table_icv.setItem(row, 4, QTableWidgetItem(item.source_reference))

        tot_demand_m3 = 100.0
        if mw and hasattr(mw, 'tab_building'):
            b_cfg = mw.tab_building.get_building_config()
            calc_dem = (b_cfg.get("demand", 0.0) * b_cfg.get("residents", 0) * 365.25) / 1000.0
            if calc_dem > 0:
                tot_demand_m3 = calc_dem

        self.chart_opt.update_chart(lca_result=lca_res)
        self.chart_payback.update_chart(lca_result=lca_res, total_demand_m3=tot_demand_m3)
        self.chart_component_breakdown.update_chart(lca_result=lca_res, sweep_details=sweep_details)

        # ── CÁLCULO E ATUALIZAÇÃO ESG & CERTIFICAÇÕES AMBIENTAIS ──
        potable_savings_pct = 0.0
        if sw_res_tech and matching:
            potable_savings_pct = getattr(matching[0], 'potential_potable_savings_pct', 0.0)
        elif single_res:
            potable_savings_pct = getattr(single_res, 'potential_potable_savings_pct', 0.0)
        
        if potable_savings_pct <= 0.0 and tot_demand_m3 > 0:
            potable_savings_pct = (ann_m3 / tot_demand_m3 * 100.0)

        potable_ann_m3 = max(0.0, tot_demand_m3 - ann_m3)

        # Contexto do edifício: modo simplificado vs avançado, e demandas interna / externa
        mw = self.window()
        is_simplified = True
        has_irr = True
        indoor_savings_pct = None
        outdoor_savings_pct = None
        indoor_dem_m3 = None
        outdoor_dem_m3 = None

        if mw and hasattr(mw, 'tab_building'):
            tb = mw.tab_building
            try:
                b_cfg = tb.get_building_config() if hasattr(tb, 'get_building_config') else {}
                mode_idx = getattr(getattr(tb, 'tab_demand_mode', None), 'currentIndex', lambda: 0)()
                is_simplified = (mode_idx == 0 or b_cfg.get("demand_mode") == "constant")
                
                if is_simplified:
                    ext_l_d = float(b_cfg.get("irrigation_liters_per_day", 0.0) or 0.0)
                    outdoor_dem_m3 = (ext_l_d * 365.25) / 1000.0
                    has_irr = (outdoor_dem_m3 > 0.001)

                    if has_irr and outdoor_dem_m3 > 0:
                        indoor_dem_m3 = max(0.0, tot_demand_m3 - outdoor_dem_m3)
                        pluv_to_outdoor = min(ann_m3, outdoor_dem_m3)
                        pluv_to_indoor = max(0.0, ann_m3 - pluv_to_outdoor)
                        outdoor_savings_pct = (pluv_to_outdoor / outdoor_dem_m3 * 100.0)
                        indoor_savings_pct = (pluv_to_indoor / indoor_dem_m3 * 100.0) if indoor_dem_m3 > 0 else potable_savings_pct
                    else:
                        outdoor_dem_m3 = 0.0
                        indoor_dem_m3 = tot_demand_m3
                        has_irr = False
                        pluv_to_outdoor = 0.0
                        pluv_to_indoor = ann_m3
                        outdoor_savings_pct = 0.0
                        indoor_savings_pct = (ann_m3 / tot_demand_m3 * 100.0) if tot_demand_m3 > 0 else potable_savings_pct
                else:
                    irr_l_d = float(b_cfg.get("irrigation_liters_per_day", 0.0) or 0.0)
                    wash_ext = float(b_cfg.get("wash_external", 0.0) or 0.0)
                    outdoor_l_d = irr_l_d + (wash_ext / 7.0)
                    outdoor_dem_m3 = (outdoor_l_d * 365.25) / 1000.0
                    has_irr = (outdoor_dem_m3 > 0.001)

                    if has_irr and outdoor_dem_m3 > 0:
                        indoor_dem_m3 = max(0.0, tot_demand_m3 - outdoor_dem_m3)
                        pluv_to_outdoor = min(ann_m3, outdoor_dem_m3)
                        pluv_to_indoor = max(0.0, ann_m3 - pluv_to_outdoor)
                        outdoor_savings_pct = (pluv_to_outdoor / outdoor_dem_m3 * 100.0)
                        indoor_savings_pct = (pluv_to_indoor / indoor_dem_m3 * 100.0) if indoor_dem_m3 > 0 else potable_savings_pct
                    else:
                        outdoor_dem_m3 = 0.0
                        indoor_dem_m3 = tot_demand_m3
                        has_irr = False
                        pluv_to_outdoor = 0.0
                        pluv_to_indoor = ann_m3
                        outdoor_savings_pct = 0.0
                        indoor_savings_pct = (ann_m3 / tot_demand_m3 * 100.0) if tot_demand_m3 > 0 else potable_savings_pct
            except Exception:
                pass

        esg_res = calculate_esg_certifications(
            potable_savings_pct=potable_savings_pct,
            annual_pluvial_consumed_m3=ann_m3,
            annual_potable_consumed_m3=potable_ann_m3,
            net_co2e_saved_kg_lifetime=lca_res.lifetime_net_co2_saved_kg,
            project_lifetime_years=20,
            has_irrigation_demand=has_irr,
            indoor_savings_pct=indoor_savings_pct,
            outdoor_savings_pct=outdoor_savings_pct,
            is_simplified_mode=is_simplified,
            indoor_demand_m3=indoor_dem_m3,
            outdoor_demand_m3=outdoor_dem_m3,
            # Entrada do campo WEM14 do EDGE, vinda da aba de projeto.
            catchment_area_m2=float(
                getattr(getattr(self.window(), 'config', None), 'area', 0.0) or 0.0
            ),
            edge_base_case_annual_m3=self._edge_base_case_annual_m3(),
        )

        if hasattr(self, 'card_leed'):
            leed_tot = esg_res.leed.total_leed_we_points
            self._update_kpi(
                self.card_leed,
                f"{leed_tot} de 8 pts",
                f"Tirou {leed_tot} de 8 pontos (Máx: 8 pts)"
            )
            self.card_leed.setToolTip(
                f"Selo LEED v4 WE (Water Efficiency):\n"
                f"Teto máximo normativo: 8 pontos possíveis.\n"
                f"Pontuação obtida pelo projeto: tirou {leed_tot} de 8 pontos.\n\n"
                f"• WEc1 (Uso Externo): tirou {esg_res.leed.outdoor_water_points} de 2 pontos (máx: 2 pts)\n"
                f"• WEc2 (Uso Interno): tirou {esg_res.leed.indoor_water_points} de 6 pontos (máx: 6 pts)\n"
                f"Classificação: {esg_res.leed.badge_label}"
            )
        if hasattr(self, 'card_aqua'):
            stars_str = "⭐" * esg_res.aqua.stars if esg_res.aqua.stars > 0 else ""
            self._update_kpi(self.card_aqua, f"{esg_res.aqua.performance_level} {stars_str}".strip())
        if hasattr(self, 'card_casa_azul'):
            self._update_kpi(self.card_casa_azul, f"Nível {esg_res.casa_azul.category} (+{esg_res.casa_azul.points_awarded} pts)")
        if hasattr(self, 'card_gri'):
            self._update_kpi(self.card_gri, f"{format_ptbr(esg_res.annual_potable_saved_m3, 0)} m³/ano")
        if hasattr(self, 'card_edge'):
            e = esg_res.edge
            self._update_kpi(
                self.card_edge,
                f"{format_ptbr(e.economia_de_agua_pct, 1)}%",
                ("Atende ao padrão de água (≥ 20%)" if e.atende_o_padrao_de_agua
                 else f"Faltam {format_ptbr(abs(e.margem_pct), 1)} pontos percentuais"),
            )
            self.card_edge.setToolTip(
                f"{e.descricao}\n\n{e.ressalva}\n\n"
                f"Área de captação a declarar no campo da medida WEM14: "
                f"{format_ptbr(e.area_de_captacao_m2, 0)} m²."
            )
        if hasattr(self, 'lbl_esg_summary_box'):
            self.lbl_esg_summary_box.setText(f"🌿 <b>{tr('Síntese Executiva ESG & Certificações:')}</b> {esg_res.esg_summary_text}")

        if hasattr(self, 'table_esg_breakdown') and esg_res.credit_details:
            self.table_esg_breakdown.setRowCount(len(esg_res.credit_details))
            for row, d in enumerate(esg_res.credit_details):
                # 0: Certificação
                it_cert = QTableWidgetItem(d.certification)
                self.table_esg_breakdown.setItem(row, 0, it_cert)

                # 1: Crédito / Código
                it_code = QTableWidgetItem(d.credit_code)
                it_code.setTextAlignment(Qt.AlignCenter)
                self.table_esg_breakdown.setItem(row, 1, it_code)

                # 2: Foco / Aplicação
                it_foc = QTableWidgetItem(d.focus or d.credit_name)
                self.table_esg_breakdown.setItem(row, 2, it_foc)

                # 3: Desempenho
                it_perf = QTableWidgetItem(d.achieved_performance)
                self.table_esg_breakdown.setItem(row, 3, it_perf)

                # 4: Pontos / Status
                pts_text = f"{d.points_or_level} — {d.status}" if d.status else d.points_or_level
                it_p = QTableWidgetItem(pts_text)
                it_p.setToolTip(f"{d.requirement_rule}\n\nNota técnica: {d.notes}")
                self.table_esg_breakdown.setItem(row, 4, it_p)

        self.environmental_updated.emit()

    def _get_esg_methodology_html(self, is_dark: bool) -> str:
        text_col = '#f4f4f5' if is_dark else '#1e293b'
        sub_col = '#a1a1aa' if is_dark else '#475569'
        h_col = '#38bdf8' if is_dark else '#0284c7'
        card_bg = '#27272a' if is_dark else '#f1f5f9'
        card_border = '#3f3f46' if is_dark else '#cbd5e1'
        tag_bg = '#14532d' if is_dark else '#dcfce7'
        tag_col = '#86efac' if is_dark else '#15803d'

        return f"""
        <div style="color: {text_col}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 1.55;">
            <p style="margin-top: 0; font-size: 12.5px;">
                O aproveitamento de água de chuva é um dos vetores de maior pontuação em certificações ambientais de edifícios. 
                O <b>Netuno 5</b> processa a simulação contínua do balanço hídrico diário (modelo YAS) e converte automaticamente 
                a taxa de economia e a conservação de recursos em pontuações auditáveis nos quatro principais referenciais:
            </p>

            <div style="background-color: {card_bg}; border: 1px solid {card_border}; border-left: 4px solid #16a34a; padding: 10px 14px; border-radius: 6px; margin-bottom: 12px;">
                <h4 style="margin: 0 0 6px 0; color: {h_col}; font-size: 13px;">1. LEED v4 / v4.1 BD+C & O+M (USGBC / GBC Brasil) — Categoria WE (Water Efficiency)</h4>
                <p style="margin: 0 0 6px 0;">
                    <b>Pontuação Máxima Possível: 8 pontos</b> no crédito de aproveitamento pluvial (de 110 pontos totais da certificação LEED). O Netuno calcula exatamente quantos pontos (X de 8 pontos) a edificação tirou:
                </p>
                <ul style="margin: 0 0 6px 0; padding-left: 18px;">
                    <li><b>Crédito WEc1 — Redução do Uso Externo (Outdoor Water Use - Máx. 2 pontos):</b> Avalia a substituição de água potável na irrigação e torneiras de jardim. Requer demanda externa ativa; sem demanda externa no projeto, atribui-se 0 pontos (não aplicável). Havendo irrigação: ≥ 50% de redução = <b>1 ponto</b>; ≥ 95% = <b>2 pontos (máximo)</b>.</li>
                    <li><b>Crédito WEc2 — Redução do Uso Interno (Indoor Water Use - Máx. 6 pontos):</b> Avalia a substituição de água potável em bacias sanitárias, mictórios e lavanderia por fontes alternativas não potáveis. Pontuação progressiva oficial do USGBC LEED v4 BD+C / O+M:
                        <br/>&nbsp;&nbsp;• <b>25%</b>: <b>1 ponto</b> &nbsp;|&nbsp; <b>30%</b>: <b>2 pontos</b> &nbsp;|&nbsp; <b>35%</b>: <b>3 pontos</b>
                        <br/>&nbsp;&nbsp;• <b>40%</b>: <b>4 pontos</b> &nbsp;|&nbsp; <b>45%</b>: <b>5 pontos</b> &nbsp;|&nbsp; <b>≥ 50%</b>: <b>6 pontos (máximo)</b>.
                    </li>
                </ul>
                <span style="display: inline-block; background: {tag_bg}; color: {tag_col}; font-weight: bold; font-size: 11px; padding: 2px 8px; border-radius: 4px;">
                    Teto Máximo em Eficiência Hídrica: Até 8 pontos diretos (Tirou X de 8 pontos possíveis)
                </span>
            </div>

            <div style="background-color: {card_bg}; border: 1px solid {card_border}; border-left: 4px solid #0284c7; padding: 10px 14px; border-radius: 6px; margin-bottom: 12px;">
                <h4 style="margin: 0 0 6px 0; color: {h_col}; font-size: 13px;">2. Processo AQUA-HQE (Fundação Vanzolini / CertiVéa) — Categoria 4 (Gestão da Água)</h4>
                <p style="margin: 0 0 6px 0;">
                    Baseado no referencial internacional HQE e na <b>ABNT NBR 15527</b>, a Categoria 4 avalia a gestão sustentável das águas pluviais, retenção no lote e conservação de água potável:
                </p>
                <ul style="margin: 0; padding-left: 18px;">
                    <li><b>Nível Base (⭐):</b> Substituição de água potável ≥ 10%. Atendimento às exigências construtivas mínimas (gradeamento, pré-filtro autolimpante, extravasor protegido e sifão anti-roedores).</li>
                    <li><b>Nível Boas Práticas (⭐⭐):</b> Substituição de água potável ≥ 25%. Sistema integrado de descarte inicial calibrado (first flush), cloração com residual livre e abastecimento estável aos pontos de uso não potável.</li>
                    <li><b>Nível Excelente (⭐⭐⭐):</b> Substituição de água potável ≥ 40%. Alta autossuficiência hídrica, retenção e amortecimento de vazões pluviais no terreno, medição setorizada de vazão e qualidade classe 1 ou 2.</li>
                </ul>
            </div>

            <div style="background-color: {card_bg}; border: 1px solid {card_border}; border-left: 4px solid #0ea5e9; padding: 10px 14px; border-radius: 6px; margin-bottom: 12px;">
                <h4 style="margin: 0 0 6px 0; color: {h_col}; font-size: 13px;">3. Selo Casa Azul CAIXA — Critério 2.1 (Conservação de Água e Fontes Alternativas)</h4>
                <p style="margin: 0 0 6px 0;">
                    Criado pela Caixa Econômica Federal para classificar empreendimentos habitacionais sustentáveis financiados. Concede bonificação direta de pontos que habilitam a taxas de juros reduzidas no crédito imobiliário:
                </p>
                <ul style="margin: 0; padding-left: 18px;">
                    <li><b>Graduação Prata (+2 pontos CAIXA):</b> Redução de pelo menos 10% no consumo de água potável da edificação via água de chuva.</li>
                    <li><b>Graduação Ouro (+3 pontos CAIXA):</b> Redução ≥ 20%, com simulação hidrológica demonstrando regularidade e sistema de recalque automatizado.</li>
                    <li><b>Graduação Diamante (+5 pontos CAIXA):</b> Redução ≥ 30%, com desinfecção ativa, dosagem de cloro, monitoramento contínuo e reserva técnica de emergência.</li>
                </ul>
            </div>

            <div style="background-color: {card_bg}; border: 1px solid {card_border}; border-left: 4px solid #059669; padding: 10px 14px; border-radius: 6px;">
                <h4 style="margin: 0 0 6px 0; color: {h_col}; font-size: 13px;">4. GRI Standard 303 (Global Reporting Initiative) & Pegada Hídrica Positiva</h4>
                <p style="margin: 0 0 6px 0;">
                    Padrão internacional para relatórios corporativos ESG, relatórios anuais de sustentabilidade e enquadramento em títulos verdes (green bonds):
                </p>
                <ul style="margin: 0; padding-left: 18px;">
                    <li><b>GRI 303-3 (Captação de Água Evitada / Water Withdrawal Saved):</b> Volume total em m³/ano que o empreendimento deixa de extrair dos mananciais públicos e da concessionária.</li>
                    <li><b>GRI 303-5 (Consumo e Circularidade Hídrica / Water Positive Ratio):</b> Razão entre o volume pluvial circular aproveitado e a demanda total de água:
                        <br/><code>Water Positive Ratio = (Volume Pluvial Anual / Demanda Anual Total) × 100%</code>.
                    </li>
                </ul>
            </div>
        </div>
        """
