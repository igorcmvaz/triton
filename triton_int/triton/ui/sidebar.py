"""
Componente Sidebar para Navegação por Etapas no Triton.
Permite trocar de aba com facilidade e exibe o Resumo Expandido do Projeto em tempo real.
"""

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QButtonGroup
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap

from triton import APP_VERSION_LABEL
from triton.ui.translation import tr, get_resource_path, get_current_theme


class Sidebar(QWidget):
    step_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(296)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.buttons = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 18, 10, 12)
        layout.setSpacing(4)
        self.setStyleSheet("QWidget { background-color: #063c36; color: #ffffff; }")

        is_dark = get_current_theme() == "dark"

        # Header Compacto do App com Logo Oficial Triton
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        logo_path = get_resource_path("Triton2.png")
        if os.path.exists(logo_path):
            lbl_logo = QLabel()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                lbl_logo.setPixmap(pixmap.scaledToHeight(40, Qt.SmoothTransformation))
                lbl_logo.setAlignment(Qt.AlignCenter)
                header_layout.addWidget(lbl_logo)

        v_title = QVBoxLayout()
        v_title.setSpacing(1)

        lbl_title = QLabel(APP_VERSION_LABEL)
        lbl_title.setText("TRITON")
        lbl_title.setStyleSheet("""
            font-family: 'Segoe UI', 'Montserrat', 'Inter', 'Arial', sans-serif;
            font-size: 18px;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 2.2px;
        """)
        lbl_sub = QLabel(tr("UFSC · ENGENHARIA HÍDRICA"))
        lbl_sub.setStyleSheet("""
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 9.5px;
            font-weight: 700;
            color: #9ec3b7;
            letter-spacing: 1.2px;
        """)

        v_title.addWidget(lbl_title)
        v_title.addWidget(lbl_sub)
        # Selo da edição: a Brasil traz os dados brasileiros; a Internacional, não; a
        # Portugal, os portugueses à medida que são conferidos.
        from triton.core.edition import is_int_edition, is_prt_edition, rotulo_da_edicao
        self.lbl_edicao = QLabel(rotulo_da_edicao())
        self.lbl_edicao.setObjectName("selo_edicao")
        if is_int_edition():
            dica = tr("Edição Internacional: tarifas, custos, moeda e fator de emissão informados pelo usuário.")
            cor = "background-color: #1d4ed8; color: #ffffff;"
        elif is_prt_edition():
            dica = tr("Edição Portugal: precipitação por concelho (E-OBS), tarifários das entidades gestoras "
                      "e valores em euros.")
            cor = "background-color: #b91c1c; color: #ffffff;"
        else:
            dica = tr("Edição Brasil: base climática CLIMBra, tarifas de 652 municípios e custos em reais.")
            cor = "background-color: #15803d; color: #ffffff;"
        self.lbl_edicao.setToolTip(dica)
        self.lbl_edicao.setStyleSheet(
            "font-size: 9.5px; font-weight: 800; letter-spacing: 0.6px; padding: 1px 6px; border-radius: 4px; " + cor)
        v_title.addWidget(self.lbl_edicao)
        header_layout.addLayout(v_title)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Divisor
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #1f6559; margin-top: 8px; margin-bottom: 6px;")
        layout.addWidget(line)

        # Grupo de Botões das Etapas com Categorização Visual
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        steps_sections = [
            (tr("DADOS DE ENTRADA"), "inputs", [
                (f"🌧️ {tr('1. Projeto e Chuva')}", 0),
                (f"🏠 {tr('2. Edificação e Consumo')}", 1),
                (f"🧪 {tr('3. Qualidade & ETAP')}", 2),
                (f"🚰 {tr('4. Reservatório & Custos')}", 3),
            ]),
            (tr("RESULTADOS"), "outputs", [
                (f"📊 {tr('5. Resultados Técnicos')}", 4),
                (f"💰 {tr('6. Resultados Econômicos')}", 5),
                (f"🍃 {tr('7. Resultados Ambientais & ESG')}", 6),
                (f"🏆 {tr('8. Decisão Multicritério')}", 7),
                (f"📑 {tr('9. Relatórios PDF')}", 8),
            ]),
            (tr("FERRAMENTAS"), "utils", [
                (f"📦 {tr('10. Exportação')}", 9),
                (f"📚 {tr('11. Documentação')}", 10),
                (f"🏛️ {tr('12. Gestor de Tarifas')}", 11),
                (f"🎲 {tr('13. Modulação Probabilística')}", 12),
            ])
        ]
        # O Gestor de Tarifas é o catálogo dos 652 municípios brasileiros.
        from triton.core.edition import usa_dados_do_brasil
        if not usa_dados_do_brasil():
            # Sai só o Gestor de Tarifas; a Modulação Probabilística fica nas duas edições.
            steps_sections[-1][2].pop(-2)

        # Estilo unificado, robusto e destacado para as etapas
        btn_style = """
            QPushButton {
                text-align: left;
                padding: 7px 12px;
                font-family: 'Segoe UI', 'Inter', 'Roboto', 'Arial', sans-serif;
                font-size: 12.5px;
                font-weight: 600;
                color: #e2f2ed;
                background-color: transparent;
                border: 1px solid transparent;
                border-left: 4px solid transparent;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0b5148;
                color: #ffffff;
                font-weight: 700;
            }
            QPushButton:checked {
                background-color: #0b594f;
                color: #ffffff;
                font-weight: 800;
                border-left: 4px solid #31c4a5;
            }
        """

        for sec_idx, (sec_title, sec_type, items) in enumerate(steps_sections):
            if sec_idx > 0:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setFrameShadow(QFrame.Plain)
                sep.setStyleSheet("color: #0e483e; margin-top: 4px; margin-bottom: 2px;")
                layout.addWidget(sep)

            lbl_sec = QLabel(sec_title)
            sec_color = "#34d399" if sec_type == "inputs" else ("#38bdf8" if sec_type == "outputs" else "#fbbf24")
            lbl_sec.setStyleSheet(f"""
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 9.5px;
                font-weight: 800;
                color: {sec_color};
                padding: 3px 6px 1px 6px;
                letter-spacing: 1.1px;
            """)
            layout.addWidget(lbl_sec)

            for text, idx in items:
                btn = QPushButton(text.replace("&", "&&"))  # «&» das traduções não vira atalho sublinhado
                btn.setCheckable(True)
                btn.setStyleSheet(btn_style)
                btn.setCursor(Qt.PointingHandCursor)
                self.btn_group.addButton(btn, idx)
                layout.addWidget(btn)
                self.buttons.append(btn)

        # Seleciona o primeiro por padrão
        if self.buttons:
            self.buttons[0].setChecked(True)
        self.btn_group.idClicked.connect(self.on_btn_clicked)

        layout.addStretch()

        # Painel de Resumo Expandido do Projeto no Rodapé da Sidebar
        self.card_summary = QFrame()
        self.card_summary.setObjectName("card_summary")
        
        if is_dark:
            self.card_summary.setStyleSheet("""
                QFrame#card_summary {
                    background-color: #122b25;
                    border: 1.5px solid #1f4239;
                    border-radius: 8px;
                }
                QFrame#card_summary QLabel {
                    border: none;
                    background-color: transparent;
                    padding: 1px 0px;
                    margin: 0px;
                }
            """)
        else:
            self.card_summary.setStyleSheet("""
                QFrame#card_summary {
                    background-color: #f0f7f4;
                    border: 1.5px solid #087f6b;
                    border-radius: 8px;
                }
                QFrame#card_summary QLabel {
                    border: none;
                    background-color: transparent;
                    padding: 1px 0px;
                    margin: 0px;
                }
            """)
            
        lay_sum = QVBoxLayout(self.card_summary)
        lay_sum.setContentsMargins(10, 10, 10, 10)
        lay_sum.setSpacing(3)

        lbl_sum_header = QLabel(f"📌 {tr('Resumo do Projeto')}")
        lbl_sum_header.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#48d5b7' if is_dark else '#087f6b'}; margin-bottom: 4px;")
        
        self.lbl_sum_rain = QLabel(tr("Chuva: Não carregada"))
        self.lbl_sum_rain.setWordWrap(True)
        self.lbl_sum_rain.setStyleSheet(f"font-size: 10px; color: {'#a3cdc3' if is_dark else '#334155'};")
        
        self.lbl_sum_building = QLabel(tr("Edificação: 100m² | 3hab"))
        self.lbl_sum_building.setStyleSheet(f"font-size: 10px; color: {'#a3cdc3' if is_dark else '#334155'};")

        self.lbl_sum_mode = QLabel(tr("Modo: Não simulado"))
        self.lbl_sum_mode.setWordWrap(True)
        self.lbl_sum_mode.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {'#48d5b7' if is_dark else '#087f6b'};")

        optimum_style = f"font-size: 10px; font-weight: bold; color: {'#ffffff' if is_dark else '#063c36'};"
        self.lbl_sum_opt_tech = QLabel(tr("Ótimo técnico: -- L"))
        self.lbl_sum_opt_econ = QLabel(tr("Ótimo econômico: -- L"))
        self.lbl_sum_opt_env = QLabel(tr("Ótimo ambiental: -- L"))
        self.lbl_sum_opt_topsis = QLabel(tr("Ótimo TOPSIS: -- L"))
        for label in (
            self.lbl_sum_opt_tech, self.lbl_sum_opt_econ,
            self.lbl_sum_opt_env, self.lbl_sum_opt_topsis,
        ):
            label.setStyleSheet(optimum_style)

        lay_sum.addWidget(lbl_sum_header)
        lay_sum.addWidget(self.lbl_sum_rain)
        lay_sum.addWidget(self.lbl_sum_building)
        lay_sum.addWidget(self.lbl_sum_mode)
        lay_sum.addWidget(self.lbl_sum_opt_tech)
        lay_sum.addWidget(self.lbl_sum_opt_econ)
        lay_sum.addWidget(self.lbl_sum_opt_env)
        lay_sum.addWidget(self.lbl_sum_opt_topsis)

        self.card_summary.hide()

        # Identificação discreta da versão publicada.
        self.lbl_beta_disclaimer = QLabel(f"UFSC • {tr('Versão')} {APP_VERSION_LABEL.split()[-1]}")
        self.lbl_beta_disclaimer.setAlignment(Qt.AlignCenter)
        self.lbl_beta_disclaimer.setWordWrap(True)
        self.lbl_beta_disclaimer.setText(tr('Motor científico compartilhado · {0}').format(APP_VERSION_LABEL.split()[-1]))
        self.lbl_beta_disclaimer.setStyleSheet("font-size: 8.5px; color: #789f95; margin-top: 4px; font-weight: 500;")
        layout.addWidget(self.lbl_beta_disclaimer)

        self.setLayout(layout)

    def on_btn_clicked(self, step_idx: int):
        self.step_changed.emit(step_idx)

    def set_active_step(self, index: int):
        """Marca programaticamente o botão correspondente ao índice de etapa."""
        btn = self.btn_group.button(index)
        if btn:
            btn.setChecked(True)

    def update_summary(
        self, 
        rain_name: str = "", 
        area: float = 100.0, 
        residents: int = 3, 
        demand_per_capita: float = 100.0, 
        share: float = 0.4, 
        mode_str: str = "Não simulado",
        technical_opt_vol: float = None,
        economic_opt_vol: float = None,
        environmental_opt_vol: float = None,
        topsis_opt_vol: float = None,
    ):
        if rain_name and rain_name != "Nenhum arquivo de chuva selecionado — Clique ao lado para carregar":
            clean_name = rain_name.replace('\\', '/').split('/')[-1]
            self.lbl_sum_rain.setText(f"{tr('Chuva: ')}{clean_name}")
        else:
            self.lbl_sum_rain.setText(tr("Chuva: Não carregada"))

        self.lbl_sum_building.setText(f"{tr('Edificação: ')}{area:.0f}m² | {residents} {tr('hab')}")
        self.lbl_sum_mode.setText(f"{tr('Modo: ')}{tr(mode_str)}")

        def optimum_text(label, value):
            if value is None:
                return f"{label} -- L"
            return f"{label} {float(value):,.0f} L".replace(',', '.')

        self.lbl_sum_opt_tech.setText(optimum_text(f"💧 {tr('Ótimo técnico:')}", technical_opt_vol))
        self.lbl_sum_opt_econ.setText(optimum_text(f"💵 {tr('Ótimo econômico:')}", economic_opt_vol))
        self.lbl_sum_opt_env.setText(optimum_text(f"🍃 {tr('Ótimo ambiental:')}", environmental_opt_vol))
        self.lbl_sum_opt_topsis.setText(optimum_text(f"🏆 {tr('Ótimo TOPSIS:')}", topsis_opt_vol))
