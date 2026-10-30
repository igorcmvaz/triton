"""
Etapa 8: Gerador de Relatórios Executivos e de Pesquisa (Exportação PDF/HTML em Triton).
Suporta exportação em dois formatos estruturais:
1. Relatório Econômico (Clientes) — Visão gerencial de 1 página A4 para apresentação comercial.
2. Relatório de Pesquisa — Estudo técnico-científico aprofundado com hidrologia, ACV e equações.
"""

from triton.core.edition import rotulo_da_edicao
from triton.core.numero import milhar, normalizar, normalizar_milhar, para_float, usa_ponto_decimal
import os
import base64
from io import BytesIO
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QFileDialog, QMessageBox, QComboBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from triton.ui.translation import tr, get_current_theme, get_current_lang, set_current_lang
from triton.ui.textos_da_edicao import artefato_de_laudo
from triton.core.report_generator import save_pdf_report
from triton.core.report_service import generate_report_html

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import QWebEngineSettings
    HAS_WEBENGINE = True
except Exception:
    HAS_WEBENGINE = False


class TabReportsPdf(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._project_data = {}
        self._reference_code = None
        self.web_preview = None
        self._zoom_factor = 1.0
        self._user_selected_vol = None
        self._populating_volumes = False
        self.init_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self._populate_volume_selector()
        self.update_report_preview()

    def init_ui(self):
        self._zoom_factor = 1.0
        is_dark = get_current_theme() == "dark"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # ── 1. CARD SUPERIOR DE CONTROLE E EXPORTAÇÃO ──
        card_header = QFrame(self)
        card_header.setObjectName("reportControlCard")
        bg_card = "#1e1e24" if is_dark else "#ffffff"
        border_card = "#3f3f46" if is_dark else "#cbdad5"
        text_primary = "#f4f4f5" if is_dark else "#17332c"
        text_muted = "#a1a1aa" if is_dark else "#64748b"

        card_header.setStyleSheet(f"""
            QFrame#reportControlCard {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-radius: 8px;
            }}
        """)
        lay_card = QVBoxLayout(card_header)
        lay_card.setContentsMargins(14, 10, 14, 10)
        lay_card.setSpacing(8)

        # Linha 1: Título na esquerda + Badges de Status na direita
        row_title = QHBoxLayout()
        row_title.setSpacing(10)

        icon_title = QLabel("📑")
        icon_title.setStyleSheet("font-size: 18px;")
        row_title.addWidget(icon_title)

        lay_titles = QVBoxLayout()
        lay_titles.setSpacing(1)
        lbl_title = QLabel(tr("Central de Relatórios & Exportações Oficiais"))
        lbl_title.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {'#34d399' if is_dark else '#087f6b'}; background-color: transparent;")
        lbl_subtitle = QLabel(tr("Geração de laudos executivos A4, auditoria ambiental ESG/ACV e dossiês de engenharia."))
        lbl_subtitle.setStyleSheet(f"font-size: 10.5px; color: {text_muted}; background-color: transparent;")
        lay_titles.addWidget(lbl_title)
        lay_titles.addWidget(lbl_subtitle)
        row_title.addLayout(lay_titles)

        row_title.addStretch()

        self.lbl_ref_badge = QLabel(f"🏷️ {self._generate_ref_code()}")
        self.lbl_ref_badge.setStyleSheet(f"""
            background-color: {'#27272a' if is_dark else '#ffffff'};
            color: {'#e4e4e7' if is_dark else '#334155'};
            border: 1px solid {'#3f3f46' if is_dark else '#cbd5e1'};
            font-size: 11px; font-weight: 600;
            padding: 4px 10px; border-radius: 5px;
        """)
        row_title.addWidget(self.lbl_ref_badge)

        self.lbl_report_status = QLabel(tr("● Pronto para exportação"))
        self.lbl_report_status.setObjectName("reportPreviewStatus")
        self.lbl_report_status.setStyleSheet(f"""
            background-color: {'#064e3b' if is_dark else '#ecfdf5'};
            color: {'#6ee7b7' if is_dark else '#065f46'};
            border: 1px solid {'#047857' if is_dark else '#a7f3d0'};
            font-size: 11px; font-weight: 600;
            padding: 4px 10px; border-radius: 5px;
        """)
        row_title.addWidget(self.lbl_report_status)

        lay_card.addLayout(row_title)

        card_header.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Linha 2: Seletores de Relatório/Idioma na esquerda + Botões de Ação na direita
        row_controls = QHBoxLayout()
        row_controls.setSpacing(10)

        lbl_type = QLabel(tr("Modelo:"))
        lbl_type.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {text_primary}; background-color: transparent;")
        lbl_type.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        row_controls.addWidget(lbl_type)

        self.combo_report_type = QComboBox()
        self.combo_report_type.addItem(tr("📊 Relatório Econômico Executivo (Clientes)"), "economic")
        self.combo_report_type.addItem(tr("🌱 Relatório Ambiental ESG & ACV"), "environmental")
        self.combo_report_type.addItem(tr("🔬 Relatório de Pesquisa & Dossiê Técnico"), "research")
        # Piso baixo de propósito: com a janela estreita, uma largura mínima
        # grande não encolhe, estoura a linha e o rótulo «Idioma:» acaba por
        # cima da caixa. Assim o nome do modelo é reticenciado, e os dois campos
        # continuam separados em qualquer largura.
        self.combo_report_type.setMinimumWidth(170)
        self.combo_report_type.setMaximumWidth(420)
        self.combo_report_type.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.combo_report_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_report_type.setStyleSheet(f"""
            QComboBox {{
                font-size: 11px; font-weight: 500;
                padding: 5px 10px;
                border: 1px solid {'#52525b' if is_dark else '#cbd5e1'};
                border-radius: 5px;
                background-color: {'#27272a' if is_dark else '#ffffff'};
                color: {text_primary};
            }}
            QComboBox:hover {{
                border-color: #087f6b;
            }}
        """)
        self.combo_report_type.currentIndexChanged.connect(self._on_report_type_changed)
        # Em janela estreita o nome do modelo é cortado; a dica mostra o inteiro.
        self.combo_report_type.currentIndexChanged.connect(
            lambda: self.combo_report_type.setToolTip(self.combo_report_type.currentText()))
        self.combo_report_type.setToolTip(self.combo_report_type.currentText())
        row_controls.addWidget(self.combo_report_type)

        row_controls.addSpacing(10)

        lbl_lang = QLabel(tr("Idioma:"))
        lbl_lang.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {text_primary}; background-color: transparent;")
        lbl_lang.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        row_controls.addWidget(lbl_lang)

        self.combo_report_lang = QComboBox()
        from triton.core.edition import is_ibe_edition as _ibe, usa_dados_do_brasil as _brl
        # O laudo em português é o da edição: do Brasil na BRL, de Portugal na IBE; a Internacional
        # não cita país. O inglês é «US» só na Brasil (o texto de lá segue o formato brasileiro).
        if _ibe():
            self.combo_report_lang.addItem(tr("🇵🇹 Português (Portugal)"), "pt")
        elif _brl():
            self.combo_report_lang.addItem(tr("🇧🇷 Português (Brasil)"), "pt")
        else:
            self.combo_report_lang.addItem("Português", "pt")
        self.combo_report_lang.addItem("🇺🇸 English (US)" if _brl() else "English", "en")
        self.combo_report_lang.addItem("🇪🇸 Español", "es")
        self.combo_report_lang.addItem("🇨🇳 中文（简体）", "zh")
        self.combo_report_lang.setMinimumWidth(130)
        self.combo_report_lang.setMaximumWidth(180)
        self.combo_report_lang.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.combo_report_lang.setStyleSheet(f"""
            QComboBox {{
                font-size: 11px; font-weight: 500;
                padding: 5px 10px;
                border: 1px solid {'#52525b' if is_dark else '#cbd5e1'};
                border-radius: 5px;
                background-color: {'#27272a' if is_dark else '#ffffff'};
                color: {text_primary};
            }}
            QComboBox:hover {{
                border-color: #087f6b;
            }}
        """)
        cur_l = get_current_lang()
        self.combo_report_lang.setCurrentIndex(max(0, self.combo_report_lang.findData(cur_l)))
        self.combo_report_lang.currentIndexChanged.connect(self.update_report_preview)
        row_controls.addWidget(self.combo_report_lang)

        row_controls.addSpacing(10)

        self.lbl_volume = QLabel(tr("Volume:"))
        self.lbl_volume.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {text_primary}; background-color: transparent;")
        self.lbl_volume.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        row_controls.addWidget(self.lbl_volume)

        self.combo_volume = QComboBox()
        self.combo_volume.setEditable(False)
        self.combo_volume.setMinimumWidth(140)
        self.combo_volume.setMaximumWidth(310)
        self.combo_volume.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.combo_volume.setStyleSheet(f"""
            QComboBox {{
                font-size: 11px; font-weight: 500;
                padding: 5px 10px;
                border: 1px solid {'#52525b' if is_dark else '#cbd5e1'};
                border-radius: 5px;
                background-color: {'#27272a' if is_dark else '#ffffff'};
                color: {text_primary};
            }}
            QComboBox:hover {{
                border-color: #087f6b;
            }}
        """)
        self.combo_volume.currentIndexChanged.connect(self._on_volume_changed)
        if self.combo_volume.lineEdit():
            self.combo_volume.lineEdit().editingFinished.connect(self._on_volume_text_edited)
        row_controls.addWidget(self.combo_volume)

        row_controls.addStretch()

        self.btn_refresh = QPushButton(tr("🔄 Atualizar"))
        self.btn_refresh.setObjectName("btnReportRefresh")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setStyleSheet(f"""
            QPushButton#btnReportRefresh {{
                font-size: 11px; font-weight: 600;
                background-color: {'#27272a' if is_dark else '#f8fafc'};
                color: {text_primary};
                border: 1px solid {'#52525b' if is_dark else '#cbd5e1'};
                padding: 6px 14px; border-radius: 5px;
            }}
            QPushButton#btnReportRefresh:hover {{
                background-color: {'#3f3f46' if is_dark else '#f1f5f9'};
                border-color: #087f6b;
                color: #087f6b;
            }}
        """)
        self.btn_refresh.clicked.connect(self.update_report_preview)
        row_controls.addWidget(self.btn_refresh)

        self.btn_export_html = QPushButton(tr("🌐 Exportar HTML"))
        self.btn_export_html.setObjectName("btnExportHtml")
        self.btn_export_html.setCursor(Qt.PointingHandCursor)
        self.btn_export_html.setStyleSheet("""
            QPushButton#btnExportHtml {{
                font-size: 11px; font-weight: 600;
                background-color: #0284c7; color: #ffffff;
                border: 1px solid #0369a1;
                padding: 6px 15px; border-radius: 5px;
            }}
            QPushButton#btnExportHtml:hover {{ background-color: #0369a1; }}
            QPushButton#btnExportHtml:pressed {{ background-color: #075985; }}
        """)
        self.btn_export_html.clicked.connect(self.export_html)
        row_controls.addWidget(self.btn_export_html)

        self.btn_export_pdf = QPushButton(tr("📄 Exportar PDF"))
        self.btn_export_pdf.setObjectName("btnExportPdf")
        self.btn_export_pdf.setCursor(Qt.PointingHandCursor)
        self.btn_export_pdf.setStyleSheet("""
            QPushButton#btnExportPdf {{
                font-size: 11px; font-weight: 700;
                background-color: #e11d48; color: #ffffff;
                border: 1px solid #be123c;
                padding: 6px 18px; border-radius: 5px;
            }}
            QPushButton#btnExportPdf:hover {{ background-color: #be123c; }}
            QPushButton#btnExportPdf:pressed {{ background-color: #9f1239; }}
        """)
        self.btn_export_pdf.clicked.connect(self.export_pdf)
        row_controls.addWidget(self.btn_export_pdf)

        lay_card.addLayout(row_controls)
        layout.addWidget(card_header)

        # ── 2. CONTAINER DE PRÉ-VISUALIZAÇÃO DO DOCUMENTO (EXPANSÍVEL) ──
        preview_frame = QFrame(self)
        preview_frame.setObjectName("reportPreviewContainer")
        preview_frame.setStyleSheet(f"""
            QFrame#reportPreviewContainer {{
                background-color: {'#18181b' if is_dark else '#ffffff'};
                border: 1px solid {border_card};
                border-radius: 8px;
            }}
        """)
        lay_preview_frame = QVBoxLayout(preview_frame)
        lay_preview_frame.setContentsMargins(0, 0, 0, 0)
        lay_preview_frame.setSpacing(0)

        # Barra de ferramentas da visualização do documento
        toolbar_view = QFrame(preview_frame)
        toolbar_view.setFixedHeight(34)
        toolbar_view.setStyleSheet(f"""
            QFrame {{
                background-color: {'#27272a' if is_dark else '#f8fafc'};
                border-bottom: 1px solid {border_card};
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                padding: 3px 12px;
            }}
        """)
        lay_toolbar = QHBoxLayout(toolbar_view)
        lay_toolbar.setContentsMargins(6, 2, 6, 2)
        lay_toolbar.setSpacing(6)

        lbl_view_title = QLabel(tr("📄 Visualização Oficial do Documento (Padrão A4)"))
        lbl_view_title.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {text_primary};")
        lay_toolbar.addWidget(lbl_view_title)

        lay_toolbar.addStretch()

        zoom_btn_style = f"""
            QPushButton {{
                font-size: 14px; font-weight: bold;
                padding: 0px; margin: 0px;
                border-radius: 4px;
                border: 1px solid {border_card};
                background-color: {'#18181b' if is_dark else '#ffffff'};
                color: {text_primary};
            }}
            QPushButton:hover {{
                background-color: {'#3f3f46' if is_dark else '#f1f5f9'};
                border-color: #087f6b;
                color: #087f6b;
            }}
        """

        self.btn_zoom_out = QPushButton("-")
        self.btn_zoom_out.setObjectName("btnZoomOut")
        self.btn_zoom_out.setToolTip(tr("Reduzir Zoom"))
        self.btn_zoom_out.setFixedSize(28, 24)
        self.btn_zoom_out.setCursor(Qt.PointingHandCursor)
        self.btn_zoom_out.setStyleSheet(zoom_btn_style)
        self.btn_zoom_out.clicked.connect(self._zoom_out)
        lay_toolbar.addWidget(self.btn_zoom_out)

        self.lbl_zoom = QLabel("100%")
        self.lbl_zoom.setAlignment(Qt.AlignCenter)
        self.lbl_zoom.setFixedWidth(46)
        self.lbl_zoom.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {text_muted};")
        lay_toolbar.addWidget(self.lbl_zoom)

        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_in.setObjectName("btnZoomIn")
        self.btn_zoom_in.setToolTip(tr("Aumentar Zoom"))
        self.btn_zoom_in.setFixedSize(28, 24)
        self.btn_zoom_in.setCursor(Qt.PointingHandCursor)
        self.btn_zoom_in.setStyleSheet(zoom_btn_style)
        self.btn_zoom_in.clicked.connect(self._zoom_in)
        lay_toolbar.addWidget(self.btn_zoom_in)

        self.btn_zoom_reset = QPushButton("↺ 100%")
        self.btn_zoom_reset.setObjectName("btnZoomReset")
        self.btn_zoom_reset.setToolTip(tr("Redefinir Zoom"))
        self.btn_zoom_reset.setFixedHeight(24)
        self.btn_zoom_reset.setCursor(Qt.PointingHandCursor)
        self.btn_zoom_reset.setStyleSheet(f"""
            QPushButton#btnZoomReset {{
                font-size: 10px; font-weight: 600;
                padding: 2px 8px; margin: 0px;
                border-radius: 4px;
                border: 1px solid {border_card};
                background-color: {'#18181b' if is_dark else '#ffffff'};
                color: {text_primary};
            }}
            QPushButton#btnZoomReset:hover {{
                background-color: {'#3f3f46' if is_dark else '#f1f5f9'};
                border-color: #087f6b;
                color: #087f6b;
            }}
        """)
        self.btn_zoom_reset.clicked.connect(self._zoom_reset)
        lay_toolbar.addWidget(self.btn_zoom_reset)

        lay_preview_frame.addWidget(toolbar_view, 0)

        lay_p = QVBoxLayout()
        lay_p.setContentsMargins(0, 0, 0, 0)
        lay_p.setSpacing(0)

        self.txt_preview = QTextBrowser()
        self.txt_preview.setReadOnly(True)
        self.txt_preview.setOpenExternalLinks(True)
        self.txt_preview.setStyleSheet(f"""
            background-color: {'#18181b' if is_dark else '#f8fafc'};
            color: {'#e2e8f0' if is_dark else '#1e293b'};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11px; padding: 18px;
            border: none;
        """)

        platform = os.environ.get("QT_QPA_PLATFORM", "").lower()
        allow_webengine = platform not in {"offscreen", "minimal"} and os.environ.get("TRITON_LIGHTWEIGHT_REPORT_PREVIEW") != "1"

        if HAS_WEBENGINE and allow_webengine:
            try:
                self.web_preview = QWebEngineView(self)
                settings = self.web_preview.settings()
                settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)
                settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
                settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
                self.web_preview.setStyleSheet("border: none;")
                self.web_preview.setZoomFactor(1.0)
                lay_p.addWidget(self.web_preview)
            except Exception:
                self.web_preview = None
                lay_p.addWidget(self.txt_preview)
        else:
            lay_p.addWidget(self.txt_preview)

        self._preview_layout = lay_p
        self.preview_view = self.web_preview if self.web_preview is not None else self.txt_preview
        lay_preview_frame.addLayout(lay_p, 1)

        # STRETCH = 1 para ocupar todo o espaço restante
        layout.addWidget(preview_frame, 1)

        self.setLayout(layout)
        self.update_report_preview()

    def _zoom_in(self):
        if self.web_preview is not None:
            self._zoom_factor = min(2.5, self._zoom_factor + 0.1)
            self.web_preview.setZoomFactor(self._zoom_factor)
            self.lbl_zoom.setText(f"{int(round(self._zoom_factor * 100))}%")

    def _zoom_out(self):
        if self.web_preview is not None:
            self._zoom_factor = max(0.4, self._zoom_factor - 0.1)
            self.web_preview.setZoomFactor(self._zoom_factor)
            self.lbl_zoom.setText(f"{int(round(self._zoom_factor * 100))}%")

    def _zoom_reset(self):
        if self.web_preview is not None:
            self._zoom_factor = 1.0
            self.web_preview.setZoomFactor(self._zoom_factor)
            self.lbl_zoom.setText("100%")

    @staticmethod
    def _marcar_custos_em_branco(data: dict, cfg, mw) -> None:
        """Fora da Brasil, os exemplos não trazem custos locais: o laudo avisa em vez de calcular com zeros."""
        from triton.core.edition import usa_dados_do_brasil
        if usa_dados_do_brasil():
            return
        if not data.get("capex") or not float(getattr(cfg, "elec_tariff", 0.0) or 0.0):
            data["custos_nao_informados"] = True
        try:
            tab_env = getattr(mw, "tab_environmental", None)
            amb = tab_env.get_config() if tab_env is not None and callable(getattr(tab_env, "get_config", None)) else None
            fator = float(getattr(amb, "grid_co2_factor_kg_kwh", 0.0) or 0.0) if amb is not None else 0.0
        except Exception:
            fator = 0.0
        if fator <= 0.0:
            data["fator_rede_nao_informado"] = True

    @staticmethod
    def _etiqueta_da_edicao() -> str:
        """«-INT» ou «-IBE» no nome sugerido do laudo; nada na Brasil (o nome de sempre)."""
        from triton.core.edition import rotulo_da_edicao, usa_dados_do_brasil
        return "" if usa_dados_do_brasil() else "-" + rotulo_da_edicao(curto=True)

    @staticmethod
    def _base_climatica(cfg) -> str:
        """A base da série de chuva. O modelo e o cenário (CLIMBra) só valem na Brasil; na Portugal a base é a
        E-OBS; na Internacional a série é a do arquivo do usuário e o laudo não inventa modelo."""
        from triton.core.edition import is_ibe_edition, usa_dados_do_brasil
        if usa_dados_do_brasil():
            return " · ".join(filter(None, [
                str(getattr(cfg, "climate_model", "") or ""),
                str(getattr(cfg, "climate_scenario", "") or ""),
            ])) or "Série observada"
        return "E-OBS" if is_ibe_edition() else "Série observada"

    @staticmethod
    def _acrescentar_procedencia_da_chuva(audit: dict, cfg) -> None:
        """Edição IBE: o concelho, a procedência do pacote E-OBS e se a série é do utilizador.

        O rodapé do laudo (licença, citação, nível de qualidade e cobertura) lê estas chaves em
        ``triton.core.licenca_eobs.rodape_do_laudo``. Nas outras edições nada é acrescentado.
        """
        from triton.core.edition import usa_dados_de_portugal, usa_dados_do_brasil
        if not usa_dados_do_brasil():
            audit["climate_model"] = str(getattr(cfg, "climate_model", "") or "")   # crédito das séries ERA5
        if not usa_dados_de_portugal():
            return
        audit["climate_city_name"] = str(getattr(cfg, "climate_city_name", "") or "")
        audit["climate_scenario"] = str(getattr(cfg, "climate_scenario", "") or "")
        audit["chuva_serie_propria"] = (getattr(cfg, "climate_source_mode", "") or "") == "custom_file"
        audit["chuva_procedencia"] = dict(getattr(cfg, "chuva_procedencia", None) or {})
        audit["tariff_city_code"] = str(getattr(cfg, "tariff_city_name", "") or "")

    @staticmethod
    def _periodo_climatico(cfg) -> str:
        """«início a fim» na Brasil (como sempre); fora dela, com travessão, que vale em qualquer idioma."""
        from triton.core.edition import usa_dados_do_brasil
        separador = " a " if usa_dados_do_brasil() else " – "
        return separador.join(filter(None, [
            str(getattr(cfg, "climate_start_date", "") or ""),
            str(getattr(cfg, "climate_end_date", "") or ""),
        ])) or "-"

    @staticmethod
    def _juntar_locais(*partes) -> str:
        """«Cidade / UF» sem repetir: na Portugal concelho e distrito podem ser iguais («Lisboa / Lisboa»).

        «CUSTOM» é o marcador interno de «tarifa digitada pelo usuário», e não um lugar."""
        vistas = []
        for parte in partes:
            texto = str(parte or "").strip()
            if texto.upper() == "CUSTOM":
                continue
            if texto and texto not in vistas:
                vistas.append(texto)
        return " / ".join(vistas)

    @staticmethod
    def _nome_da_serie_sem_arquivo(mw) -> str:
        """O nome do local no lugar do identificador da série.

        Na Portugal a série vem da base E-OBS por concelho e o «arquivo» é o código do concelho
        («1106»): o laudo diz o nome do local («Lisboa (E-OBS)»), e não o código.
        """
        from triton.core.edition import is_ibe_edition
        if not is_ibe_edition():
            return ""
        cfg = getattr(mw, "config", None)
        nome = str(getattr(cfg, "climate_city_name", "") or "").strip()
        if not nome:
            return ""
        return f"{nome} (E-OBS)"

    def _generate_ref_code(self) -> str:
        mw = self.window()
        config = getattr(mw, "config", None) if mw else None
        project_id = getattr(config, "project_id", None)
        if project_id:
            return project_id
        if self._reference_code is None:
            from triton.core.parser import generate_project_id
            self._reference_code = generate_project_id()
        return self._reference_code

    def _parse_volume_string(self, text: str) -> Optional[float]:
        if not text:
            return None
        t = text.split('(')[0].replace('L', '').replace('l', '').strip()
        if '.' in t and ',' in t:
            t = normalizar_milhar(t)
        elif '.' in t:
            parts = t.split('.')
            if len(parts[-1]) == 3 and len(parts) > 1 and not usa_ponto_decimal():
                t = t.replace('.', '')
        elif ',' in t:
            parts = t.split(',')
            if len(parts[-1]) == 3 and len(parts) > 1:
                t = t.replace(',', '')
            else:
                t = normalizar(t)
        try:
            val = float(t)
            return val if val >= 0 else None
        except ValueError:
            return None

    def get_selected_volume(self) -> Optional[float]:
        if getattr(self, "_user_selected_vol", None) is not None:
            return self._user_selected_vol
        if hasattr(self, "combo_volume"):
            data = self.combo_volume.currentData()
            if data is not None:
                try:
                    return float(data)
                except (ValueError, TypeError):
                    pass
            text = self.combo_volume.currentText()
            parsed = self._parse_volume_string(text)
            if parsed is not None:
                return parsed
        return None

    def _on_volume_changed(self, index: int):
        if getattr(self, "_populating_volumes", False):
            return
        data = self.combo_volume.itemData(index)
        if data is not None:
            try:
                self._user_selected_vol = float(data)
            except (ValueError, TypeError):
                self._user_selected_vol = None
        else:
            self._user_selected_vol = self._parse_volume_string(self.combo_volume.currentText())
        self.update_report_preview()

    def _on_volume_text_edited(self):
        if getattr(self, "_populating_volumes", False):
            return
        parsed = self._parse_volume_string(self.combo_volume.currentText())
        if parsed is not None:
            self._user_selected_vol = parsed
            self.update_report_preview()

    def _on_report_type_changed(self):
        # Se o usuário não travou manualmente um volume digitado, sugere o ótimo do modelo escolhido
        rep_type = self.combo_report_type.currentData() or "economic"
        mw = self.window()
        opt_econ = None
        opt_env = None
        if mw and hasattr(mw, 'tab_global_optimizer'):
            opt = mw.tab_global_optimizer
            topsis = getattr(opt, 'last_topsis_result', None)
            if topsis and getattr(topsis, 'candidates', None):
                fi = getattr(topsis, 'financial_best_index', None)
                if fi is not None and 0 <= fi < len(topsis.candidates):
                    opt_econ = float(topsis.candidates[fi].lower_tank_vol)
                ei = getattr(topsis, 'environmental_best_index', None)
                if ei is not None and 0 <= ei < len(topsis.candidates):
                    opt_env = float(topsis.candidates[ei].lower_tank_vol)

        suggested_vol = None
        if rep_type == "environmental" and opt_env is not None:
            suggested_vol = opt_env
        elif rep_type == "economic" and opt_econ is not None:
            suggested_vol = opt_econ

        if suggested_vol is not None and self._user_selected_vol is None:
            # Seleciona o sugerido no combo
            for i in range(self.combo_volume.count()):
                v = self.combo_volume.itemData(i)
                if v is not None and abs(float(v) - suggested_vol) < 1.0:
                    self._populating_volumes = True
                    try:
                        self.combo_volume.setCurrentIndex(i)
                    finally:
                        self._populating_volumes = False
                    break

        self.update_report_preview()

    def _populate_volume_selector(self):
        if not hasattr(self, "combo_volume"):
            return
        self._populating_volumes = True
        try:
            mw = self.window()
            all_vols = set()
            opt_econ = None
            opt_env = None
            opt_topsis = None
            opt_tech = None

            # 1. Da simulação de reservatórios (Fonte Primária do Ótimo Técnico pelo Threshold)
            if mw and hasattr(mw, 'tab_tanks_simulation'):
                ts = mw.tab_tanks_simulation
                sw = getattr(ts, 'last_sweep_result', None)
                if sw and getattr(sw, 'results_by_volume', None):
                    for r in sw.results_by_volume:
                        all_vols.add(float(r.lower_tank_vol))
                if getattr(ts, 'last_single_result', None):
                    all_vols.add(float(ts.last_single_result.lower_tank_vol))
                if sw and getattr(sw, 'optimal_lower_tank_vol', None):
                    v_tech = float(sw.optimal_lower_tank_vol)
                    if v_tech > 0:
                        opt_tech = v_tech

            # 2. Da aba econômica integrada (Fonte Primária do Ótimo Econômico por Menor Payback)
            tei = getattr(mw, 'tab_economic', getattr(mw, 'tab_economic_integrated', None))
            if tei is not None:
                if getattr(tei, 'combo_active_volume', None):
                    for i in range(tei.combo_active_volume.count()):
                        v = tei.combo_active_volume.itemData(i)
                        if v is not None:
                            all_vols.add(float(v))
                if getattr(tei, 'economic_optimum_volume', None):
                    v_econ = float(tei.economic_optimum_volume)
                    if v_econ > 0:
                        opt_econ = v_econ

            # 3. Da aba ambiental / ACV (Fonte Primária do Ótimo Ambiental por CO2)
            if mw and hasattr(mw, 'tab_environmental'):
                tenv = mw.tab_environmental
                if getattr(tenv, 'combo_env_active_volume', None):
                    for i in range(tenv.combo_env_active_volume.count()):
                        v = tenv.combo_env_active_volume.itemData(i)
                        if v is not None:
                            all_vols.add(float(v))
                if getattr(tenv, 'environmental_optimum_volume', None):
                    v_env = float(tenv.environmental_optimum_volume)
                    if v_env > 0:
                        opt_env = v_env

            # 4. Do otimizador global / MCDM (Fonte do Ótimo TOPSIS / Decisão Multi-Critério)
            if mw and hasattr(mw, 'tab_global_optimizer'):
                opt = mw.tab_global_optimizer
                topsis = getattr(opt, 'last_topsis_result', None)
                if topsis and getattr(topsis, 'candidates', None):
                    for c in topsis.candidates:
                        all_vols.add(float(c.lower_tank_vol))
                    bi = getattr(topsis, 'best_index', None)
                    if bi is not None and 0 <= bi < len(topsis.candidates):
                        v_top = float(topsis.candidates[bi].lower_tank_vol)
                        if v_top > 0:
                            opt_topsis = v_top
                    if opt_econ is None:
                        fi = getattr(topsis, 'financial_best_index', None)
                        if fi is not None and 0 <= fi < len(topsis.candidates):
                            v_fi = float(topsis.candidates[fi].lower_tank_vol)
                            if v_fi > 0:
                                opt_econ = v_fi
                    if opt_env is None:
                        ei = getattr(topsis, 'environmental_best_index', None)
                        if ei is not None and 0 <= ei < len(topsis.candidates):
                            v_ei = float(topsis.candidates[ei].lower_tank_vol)
                            if v_ei > 0:
                                opt_env = v_ei
                    if opt_tech is None:
                        ti = getattr(topsis, 'technical_best_index', None)
                        if ti is not None and 0 <= ti < len(topsis.candidates):
                            v_ti = float(topsis.candidates[ti].lower_tank_vol)
                            if v_ti > 0:
                                opt_tech = v_ti

            prev_selected = self._user_selected_vol
            if prev_selected is None and self.combo_volume.currentData() is not None:
                prev_selected = float(self.combo_volume.currentData())

            self.combo_volume.clear()

            sorted_vols = sorted(list(all_vols))
            # Sem simulação, a lista fica vazia: oferecer 1.000 a 10.000 L era sugerir
            # volumes que nenhum cálculo avaliou.

            for v in sorted_vols:
                tags = []
                # Apenas volumes maiores que zero (> 0 L) podem receber tags de ótimos
                if v > 0:
                    if opt_econ is not None and abs(v - opt_econ) < 1.0:
                        tags.append(tr("Ótimo Econômico"))
                    if opt_env is not None and abs(v - opt_env) < 1.0:
                        tags.append(tr("Ótimo Ambiental"))
                    if opt_tech is not None and abs(v - opt_tech) < 1.0 and "Ótimo Econômico" not in tags and "Ótimo Ambiental" not in tags:
                        tags.append(tr("Ótimo Técnico"))
                    elif opt_topsis is not None and abs(v - opt_topsis) < 1.0 and not tags:
                        tags.append(tr("Recomendado TOPSIS"))

                tag_str = f" ({' & '.join(tags)})" if tags else ""
                label = milhar(f"{v:,.0f} L{tag_str}")
                self.combo_volume.addItem(label, v)

            # Define qual volume selecionar inicialmente
            rep_type = self.combo_report_type.currentData() or "economic"
            target_to_select = None
            if prev_selected is not None:
                target_to_select = prev_selected
            elif rep_type == "environmental" and opt_env is not None:
                target_to_select = opt_env
            elif rep_type == "economic" and opt_econ is not None:
                target_to_select = opt_econ
            elif opt_topsis is not None:
                target_to_select = opt_topsis
            elif opt_econ is not None:
                target_to_select = opt_econ
            elif opt_env is not None:
                target_to_select = opt_env
            elif sorted_vols:
                target_to_select = sorted_vols[0]

            if target_to_select is not None:
                idx = -1
                for i in range(self.combo_volume.count()):
                    v = self.combo_volume.itemData(i)
                    if v is not None and abs(float(v) - target_to_select) < 1.0:
                        idx = i
                        break
                if idx >= 0:
                    self.combo_volume.setCurrentIndex(idx)
                else:
                    label = milhar(f"{target_to_select:,.0f} L")
                    self.combo_volume.setEditText(label)
        finally:
            self._populating_volumes = False

    def _collect_project_data(self) -> dict:
        data = {
            "ref_code":        self._generate_ref_code(),
            "rain_file":      tr("Não carregado"),
            "area":           "-", "runoff": 0.75, "discard": "-",
            "residents":      "-", "demand": "-",  "share":   "-",
            # Resultado não calculado fica None: o documento diz «Não calculado».
            "lower_vol":      None, "potential_pct": None,
            "pluv_day":       None, "potable_day":   None, "spill_day": None,
            "sat_full":       None, "sat_null":      None,
            "capex":          None, "annual_gross":  None,
            "vpl":            None, "tir":           None,
            "payback_s":      None, "payback_d":     None,
        }

        mw = self.window()

        if mw and hasattr(mw, 'tab_project'):
            tp = mw.tab_project
            if getattr(tp, 'precip_file_path', None):
                data["rain_file"] = os.path.basename(tp.precip_file_path)
            nome_da_serie = self._nome_da_serie_sem_arquivo(mw)
            if nome_da_serie:
                data["rain_file"] = nome_da_serie
            try:
                disc = tp.txt_discard.text().strip()
                if disc and disc != "-":
                    data["discard"] = para_float(disc)
            except Exception:
                pass

        if mw and hasattr(mw, 'tab_building'):
            tb = mw.tab_building
            for key, attr in [("area", "txt_area"), ("residents", "txt_residents"),
                               ("demand", "txt_demand"), ("share", "txt_share")]:
                w = getattr(tb, attr, None)
                if w:
                    val = w.text().strip()
                    if val and val != "-":
                        try:
                            data[key] = int(para_float(val)) if key == "residents" \
                                        else para_float(val)
                        except Exception:
                            pass
            # O campo da tela é percentual; o que segue para relatório e desenho é fração.
            if isinstance(data["share"], float):
                from triton.core.fracao_atendivel import percentual_para_fracao
                data["share"] = percentual_para_fracao(tr("Substituição por Água de Chuva (%):"), data["share"])
            if hasattr(tb, 'get_building_config'):
                data["runoff"] = tb.get_building_config().get("runoff", 0.75)

        rep_type = (self.combo_report_type.currentData() or "economic") if hasattr(self, "combo_report_type") else "economic"
        from triton.core.dados_do_relatorio import (
            volume_do_relatorio, indicadores_hidricos, indicadores_economicos, demanda_total_diaria,
        )
        ts = getattr(mw, 'tab_tanks_simulation', None) if mw else None
        te = getattr(mw, 'tab_economic', None) if mw else None
        tenv = getattr(mw, 'tab_environmental', None) if mw else None
        optimizer = getattr(mw, 'tab_global_optimizer', None) if mw else None
        sweep = getattr(ts, 'last_sweep_result', None)
        single = getattr(ts, 'last_single_result', None)
        topsis = getattr(optimizer, 'last_topsis_result', None)
        if not (topsis and getattr(topsis, 'candidates', None)):
            topsis = None
        cfg_mw = getattr(mw, 'config', None) if mw else None

        # O volume é decidido antes de qualquer indicador: antes, os hídricos eram
        # lidos para um volume e o otimizador trocava o volume depois.
        chosen_vol = volume_do_relatorio(
            selecionado=self.get_selected_volume(), tipo=rep_type, topsis=topsis,
            otimo_economico=getattr(te, 'economic_optimum_volume', None),
            otimo_ambiental=getattr(tenv, 'environmental_optimum_volume', None),
            single=single, sweep=sweep,
        )
        data["lower_vol"] = chosen_vol
        data["selection_method"] = (
            "custom_selection" if self.get_selected_volume() is not None
            else ("environmental_optimum" if rep_type == "environmental" else "economic_optimum")
        )
        # Moeda e demanda total do projeto (o desenho supunha 1.000 L/dia).
        if ts is not None and hasattr(ts, 'get_currency_symbol'):
            # «¤» é o sinal da tela para «moeda ainda não escolhida» (Internacional): o laudo
            # então diz que a moeda não foi definida, em vez de imprimir o sinal.
            data["moeda"] = (ts.get_currency_symbol() or "").replace("¤", "")
        tot = demanda_total_diaria(cfg_mw)
        if tot is not None:
            data["tot_demand"] = tot

        sweep_points = list(getattr(sweep, 'results_by_volume', []) or [])
        data["sweep_points"] = [
            {"volume": r.lower_tank_vol, "saving": r.potential_potable_savings_pct,
             "pluvial_m3": r.annual_pluvial_consumed_m3,
             "potable_m3": r.avg_potable_consumed_l_day * 365.25 / 1000.0,
             "spill_m3": r.annual_spill_m3,
             "sat_full": r.pct_days_full_satisfaction,
             "sat_null": r.pct_days_null_satisfaction,
             "marginal_gain_pct_m3": r.delta_potential_per_m3}
            for r in sweep_points
        ]
        # Indicadores hídricos do volume: da varredura ou da simulação única; volume
        # não simulado fica «Não calculado» (antes era interpolado entre vizinhos).
        data.update(indicadores_hidricos(chosen_vol, sweep=sweep, single=single))

        # Economia do volume. A aba econômica guarda o resultado em ``last_result``
        # (o relatório procurava ``last_econ_res``, que ela não define, e saía zerado).
        volume_do_ultimo = None
        if te is not None and getattr(te, 'last_result', None) is not None:
            combo = getattr(te, 'combo_active_volume', None)
            volume_do_ultimo = combo.currentData() if combo is not None else None
            if volume_do_ultimo is None and single is not None:
                volume_do_ultimo = single.lower_tank_vol
        data.update(indicadores_economicos(
            chosen_vol,
            varredura_economica=getattr(te, 'last_sweep_econ_results', None),
            ultimo=getattr(te, 'last_result', None),
            volume_do_ultimo=volume_do_ultimo,
            topsis=topsis,
            cenarios=getattr(optimizer, 'last_scenario_results', None),
        ))

        if optimizer is not None:
            if topsis is not None:
                decision = getattr(optimizer, 'last_mcdm_result', None) or topsis
                method = optimizer.combo_mcdm_method.currentData() if hasattr(optimizer, "combo_mcdm_method") else "topsis"
                smaa_result = getattr(optimizer, "last_smaa_vikor_result", None)
                data["mcdm_method"] = method
                data["mcdm_num_simulations"] = int(getattr(smaa_result, "num_simulations", 0) or 0)
                financial_index = getattr(topsis, 'financial_best_index', 0)
                def optimum_data(index):
                    candidate = topsis.candidates[index]
                    return {
                        "volume": candidate.lower_tank_vol,
                        "water_saved": candidate.water_saved_m3_yr,
                        "vpl": candidate.vpl_brl,
                        "co2": candidate.co2_saved_kg_lifetime,
                        "capex": candidate.capex_brl,
                    }
                balanced_candidate = getattr(decision, "best_candidate", topsis.best_candidate)
                data["optima"] = {
                    "technical": optimum_data(getattr(topsis, 'technical_best_index', 0)),
                    "economic": optimum_data(financial_index),
                    "environmental": optimum_data(getattr(topsis, 'environmental_best_index', 0)),
                    "balanced": {
                        "volume": balanced_candidate.lower_tank_vol,
                        "water_saved": balanced_candidate.water_saved_m3_yr,
                        "vpl": balanced_candidate.vpl_brl,
                        "co2": balanced_candidate.co2_saved_kg_lifetime,
                        "capex": balanced_candidate.capex_brl,
                    },
                }
                data["topsis_criterion_labels"] = list(getattr(topsis, 'criterion_labels', ()))
                data["topsis_criterion_weights"] = [
                    float(value) for value in getattr(topsis, 'criterion_weights', ())
                ]
                if method == "smaa_vikor" and smaa_result is not None:
                    rankings = getattr(smaa_result, "ranks", [])
                    scores = [float(value) * 100.0 for value in smaa_result.first_rank_acceptabilities]
                    selected_best_index = smaa_result.best_index
                else:
                    rankings = getattr(topsis, 'rankings', [])
                    scores = getattr(topsis, 'scores', [])
                    selected_best_index = topsis.best_index
                t_candidates = []
                for i, cand in enumerate(topsis.candidates):
                    rk = int(rankings[i]) if i < len(rankings) else i + 1
                    sc = float(scores[i]) if i < len(scores) else 0.0
                    sav_val = next((r["saving"] for r in data.get("sweep_points", []) if abs(r["volume"] - cand.lower_tank_vol) < 0.1),
                                   getattr(cand, 'potential_savings_pct', None))
                    t_candidates.append({
                        "volume": cand.lower_tank_vol,
                        "saving": sav_val,
                        "water_m3": cand.water_saved_m3_yr,
                        "capex": cand.capex_brl,
                        "vpl": cand.vpl_brl,
                        "co2": cand.co2_saved_kg_lifetime,
                        "score": sc,
                        "rank": rk,
                        "overflow_m3": cand.overflow_m3_yr,
                        "potable_m3": cand.potable_consumed_m3_yr,
                        "discounted_payback": cand.discounted_payback_years,
                        "irr": cand.irr_pct,
                        "upper_volume": cand.upper_tank_vol,
                        "technical_threshold_met": cand.technical_threshold_met,
                        "distance_to_ideal": float(topsis.dist_best[i]) if i < len(topsis.dist_best) else 0.0,
                        "distance_from_anti_ideal": float(topsis.dist_worst[i]) if i < len(topsis.dist_worst) else 0.0,
                        "criterion_gap_pct": [float(value) * 100.0 for value in topsis.criterion_gap_to_best[i]],
                        "criterion_proximity_pct": [float(value) * 100.0 for value in topsis.criterion_proximity_to_best[i]],
                        "is_best": (i == selected_best_index)
                    })
                data["topsis_candidates"] = t_candidates
            data["optimization_rows"] = [
                {"volume": sc.get("lower_vol", 0.0), "capex": sc.get("capex_lower", 0.0) + sc.get("capex_upper_pump", 0.0) + sc.get("capex_other", 0.0)}
                for sc in getattr(optimizer, 'scenarios', [])
            ]

        # Imagens em base64 são reservadas ao dossiê científico. Isso mantém
        # os laudos executivo e ambiental rápidos e atende ao perfil pedido:
        # texto detalhado em todos, figuras analíticas apenas na pesquisa.
        include_figures = (self.combo_report_type.currentData() or "economic") == "research"
        data["report_charts"] = self._collect_report_charts() if include_figures else []
        cfg = getattr(mw, 'config', None) if mw else None
        if cfg:
            data["project_name"] = getattr(cfg, "project_name", "Novo projeto Triton")
            data["audit_context"] = {
                "climate_location": self._juntar_locais(
                    getattr(cfg, "climate_city_name", ""), getattr(cfg, "climate_city_uf", "")) or "-",
                "climate_basis": self._base_climatica(cfg),
                "climate_period": self._periodo_climatico(cfg),
                "analysis_period_years": getattr(cfg, "analysis_period_years", 20),
                "tariff_location": self._juntar_locais(
                    getattr(cfg, "tariff_city_name", ""), getattr(cfg, "tariff_city_uf", "")) or "-",
            }
            self._acrescentar_procedencia_da_chuva(data["audit_context"], cfg)
            self._marcar_custos_em_branco(data, cfg, mw)
            up_vol = float(getattr(cfg, "upper_tank_vol", 0.0) or 0.0)
            if up_vol <= 0:
                if mw and hasattr(mw, "tab_tanks_simulation") and hasattr(mw.tab_tanks_simulation, "txt_upper_vol"):
                    try:
                        up_vol = para_float(mw.tab_tanks_simulation.txt_upper_vol.text())
                    except Exception:
                        pass
                elif mw and hasattr(mw, "tab_environmental") and hasattr(mw.tab_environmental, "txt_upper_vol"):
                    try:
                        up_vol = para_float(mw.tab_environmental.txt_upper_vol.text())
                    except Exception:
                        pass
            data["upper_vol"] = up_vol
            data["upper_volume"] = up_vol
            data["upper_volume_l"] = up_vol

            data["system_design"] = {
                "lower_volume_l": data.get("lower_vol", 0.0),
                "upper_used": bool(getattr(cfg, "upper_tank_used", 0)),
                "upper_volume_l": up_vol if up_vol > 0 else getattr(cfg, "upper_tank_vol", 0.0),
                "pump_power_cv": getattr(cfg, "pump_power_str", "-"),
                "pump_power_kw": getattr(cfg, "pump_power_kw", 0.0),
                "pump_flow_l_h": getattr(cfg, "pump_flow_rate", 0.0),
                "pump_count": getattr(cfg, "pump_count", 0),
                "pump_threshold_pct": getattr(getattr(mw, "tab_tanks_simulation", None), "txt_pump_thresh_pct", None).text()
                    if getattr(getattr(mw, "tab_tanks_simulation", None), "txt_pump_thresh_pct", None) else "-",
            }

        return data

    def _collect_report_charts(self):
        """Captura as figuras já calculadas para o dossiê de pesquisa.

        A geração é feita diretamente das figuras Matplotlib em memória, sem
        arquivos temporários e sem depender do tamanho visível da interface.
        """
        mw = self.window()
        if not mw:
            return []
        chart_sources = [
            ("hydraulic", "Desempenho hídrico: potencial de economia", getattr(getattr(mw, 'tab_charts', None), 'chart_pot', None)),
            ("hydraulic", "Desempenho hídrico: ganho marginal", getattr(getattr(mw, 'tab_charts', None), 'chart_delta', None)),
            ("hydraulic", "Desempenho hídrico: consumo pluvial e extravasamento", getattr(getattr(mw, 'tab_charts', None), 'chart_spill_cons', None)),
            ("hydraulic", "Desempenho hídrico: atendimento anual", getattr(getattr(mw, 'tab_charts', None), 'chart_days', None)),
            ("economic", "Avaliação econômica: sensibilidade do VPL", getattr(getattr(mw, 'tab_economic', None), 'chart_sensitivity', None)),
            ("economic", "Avaliação econômica: VPL por volume", getattr(getattr(mw, 'tab_economic', None), 'chart_vpl_volume', None)),
            ("decision", "Decisão multicritério: desempenho TOPSIS", getattr(getattr(mw, 'tab_global_optimizer', None), 'topsis_chart', None)),
            ("decision", "Decisão multicritério: proximidade por eixo", getattr(getattr(mw, 'tab_global_optimizer', None), 'topsis_proximity_chart', None)),
            ("environmental", "ACV: comparação ambiental", getattr(getattr(mw, 'tab_environmental', None), 'chart_opt', None)),
            ("environmental", "ACV: emissões com e sem aproveitamento", getattr(getattr(mw, 'tab_environmental', None), 'chart_payback', None)),
            ("environmental", "ACV: balanço acumulado de CO2 por volume", getattr(getattr(mw, 'tab_environmental', None), 'chart_component_breakdown', None)),
        ]
        charts = []
        for chapter, title, chart in chart_sources:
            figure = getattr(chart, 'figure', None)
            if figure is None or not figure.axes:
                continue
            has_data = any(
                any(len(line.get_xdata()) > 0 for line in axis.lines)
                or bool(axis.collections)
                or bool(axis.patches)
                or bool(axis.images)
                for axis in figure.axes
            )
            if not has_data:
                continue
            try:
                buffer = BytesIO()
                figure.savefig(buffer, format='png', dpi=160, bbox_inches='tight', facecolor='#ffffff')
                encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
                charts.append({
                    'chapter': chapter,
                    'title': title,
                    'source': 'Resultados calculados pelo Triton para as premissas e alternativas deste estudo.',
                    'data': f'data:image/png;base64,{encoded}',
                })
            except Exception:
                continue
        return charts

    def _safe_float(self, val, default=0.0):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    def get_lca_result(self):
        from triton.core.environmental import empty_environmental_result
        vol = self._project_data.get("lower_vol")
        pluv_d = self._project_data.get("pluv_day")
        # Sem volume ou sem consumo pluvial simulado para ele, não há ACV a mostrar:
        # antes valiam 5.000 L e 100 m³/ano, números de ninguém.
        if vol is None or pluv_d is None:
            return empty_environmental_result()
        vol = self._safe_float(vol, 0.0)
        m3_year = (self._safe_float(pluv_d, 0.0) * 365.25) / 1000.0

        mw = self.window()
        if mw and hasattr(mw, 'tab_environmental'):
            tab_env = mw.tab_environmental
            has_sweep = bool(
                hasattr(mw, 'tab_tanks_simulation')
                and getattr(mw.tab_tanks_simulation, 'last_sweep_result', None)
            )
            if not has_sweep:
                return empty_environmental_result()
            cached = getattr(tab_env, '_last_lca_result', None)
            if cached and abs(getattr(cached, 'tank_vol_liters', -1.0) - vol) < 1.0:
                return cached
            from triton.core.environmental import calculate_lca, EnvironmentalConfig
            cfg_func = getattr(tab_env, 'get_config', None)
            env_cfg = cfg_func() if callable(cfg_func) else EnvironmentalConfig()
            return calculate_lca(vol, m3_year, env_cfg)

        from triton.core.environmental import calculate_lca, EnvironmentalConfig
        return calculate_lca(vol, m3_year, EnvironmentalConfig())

    def get_esg_result(self):
        from triton.core.esg_certifications import calculate_esg_certifications
        lca = self.get_lca_result()
        potential_pct = self._safe_float(self._project_data.get("potential_pct"), 0.0)
        pluv_d = self._safe_float(self._project_data.get("pluv_day"), 0.0)
        potable_d = self._safe_float(self._project_data.get("potable_day"), 0.0)
        annual_pluvial_m3 = (pluv_d * 365.0) / 1000.0
        annual_potable_m3 = (potable_d * 365.0) / 1000.0

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
                tot_dem = annual_pluvial_m3 + annual_potable_m3

                if is_simplified:
                    ext_l_d = float(b_cfg.get("irrigation_liters_per_day", 0.0) or 0.0)
                    outdoor_dem_m3 = (ext_l_d * 365.25) / 1000.0
                else:
                    irr_l_d = float(b_cfg.get("irrigation_liters_per_day", 0.0) or 0.0)
                    wash_ext = float(b_cfg.get("wash_external", 0.0) or 0.0)
                    outdoor_l_d = irr_l_d + (wash_ext / 7.0)
                    outdoor_dem_m3 = (outdoor_l_d * 365.25) / 1000.0

                has_irr = (outdoor_dem_m3 > 0.001)
                if has_irr and outdoor_dem_m3 > 0:
                    indoor_dem_m3 = max(0.0, tot_dem - outdoor_dem_m3)
                    # Parcela externa só se o balanço a calculou; sem ela, o
                    # crédito externo fica como não avaliado, e não estimado.
                    irr_d = self._project_data.get("pluv_irrigation_day")
                    pluv_to_outdoor = (self._safe_float(irr_d, 0.0) * 365.25 / 1000.0) if irr_d is not None else None
                    pluv_to_indoor = max(0.0, annual_pluvial_m3 - (pluv_to_outdoor or 0.0))
                    outdoor_savings_pct = (pluv_to_outdoor / outdoor_dem_m3 * 100.0) if pluv_to_outdoor is not None else None
                    indoor_savings_pct = (pluv_to_indoor / indoor_dem_m3 * 100.0) if indoor_dem_m3 > 0 else potential_pct
                else:
                    outdoor_dem_m3 = 0.0
                    indoor_dem_m3 = tot_dem
                    has_irr = False
                    pluv_to_outdoor = 0.0
                    pluv_to_indoor = annual_pluvial_m3
                    outdoor_savings_pct = 0.0
                    indoor_savings_pct = (annual_pluvial_m3 / tot_dem * 100.0) if tot_dem > 0 else potential_pct
            except Exception:
                pass

        return calculate_esg_certifications(
            potable_savings_pct=potential_pct,
            annual_pluvial_consumed_m3=annual_pluvial_m3,
            annual_potable_consumed_m3=annual_potable_m3,
            net_co2e_saved_kg_lifetime=getattr(lca, 'lifetime_net_co2_saved_kg', 0.0),
            project_lifetime_years=20,
            has_irrigation_demand=has_irr,
            indoor_savings_pct=indoor_savings_pct,
            outdoor_savings_pct=outdoor_savings_pct,
            is_simplified_mode=is_simplified,
            indoor_demand_m3=indoor_dem_m3,
            outdoor_demand_m3=outdoor_dem_m3,
            catchment_area_m2=self._safe_float(
                self._project_data.get("area"), 0.0),
        )

    def update_report_preview(self):
        """Atualiza a pré-visualização oficial do relatório."""
        self._project_data = self._collect_project_data()
        if hasattr(self, "lbl_ref_badge"):
            ref = self._project_data.get("ref_code") or self._generate_ref_code()
            self.lbl_ref_badge.setText(f"🏷️ {ref}")

        report_lang = self.combo_report_lang.currentData() or "pt"
        try:
            html = self.generate_html_content(lang=report_lang)
            # Atualiza txt_preview (para compatibilidade e testes) e web_preview (para visualização rica)
            self.txt_preview.setHtml(html)
            if self.web_preview is not None:
                self.web_preview.setHtml(html)

            report_type = self.combo_report_type.currentData() or "economic"
            figure_count = len(self._project_data.get("report_charts", []))
            if report_type == "research":
                self.lbl_report_status.setText(
                    tr(f"● {figure_count} figuras incluídas") if figure_count
                    else tr("● Dossiê sem figuras (execute simulação)")
                )
            else:
                self.lbl_report_status.setText(tr("● Pronto para exportação"))
        except Exception as exc:
            self.txt_preview.setPlainText(f"{tr('Não foi possível gerar a pré-visualização')}: {exc}")
            if self.web_preview is not None:
                self.web_preview.setHtml(f"<div style='padding:20px;color:red;'>{tr('Falha na pré-visualização')}: {exc}</div>")
            self.lbl_report_status.setText(tr("Falha na pré-visualização"))

    def generate_html_content(self, lang: str | None = None) -> str:
        rep_type = self.combo_report_type.currentData() or "economic"
        lca_res = self.get_lca_result() if rep_type in {"environmental", "research"} else None
        esg_res = self.get_esg_result() if rep_type == "environmental" else None
        return generate_report_html(
            rep_type,
            self._project_data,
            lang=lang,
            lca_result=lca_res,
            esg_result=esg_res,
        )

    def export_pdf(self):
        from triton import get_auditable_filename
        prev_lang = get_current_lang()
        selected_lang = self.combo_report_lang.currentData() or "pt"
        set_current_lang(selected_lang)

        try:
            self.update_report_preview()
            rep_type = self.combo_report_type.currentData() or "economic"
            suffix = artefato_de_laudo(rep_type) + self._etiqueta_da_edicao()
            project_name = self._project_data.get("project_name", "Projeto Triton")
            def_name = get_auditable_filename(
                project_name, self._project_data["ref_code"], f"{suffix}-{selected_lang}", "pdf"
            )

            file_path, _ = QFileDialog.getSaveFileName(
                self, tr("Salvar Relatório em PDF"), def_name, f"{tr('Documento PDF')} (*.pdf)"
            )
            if file_path:
                html = self.generate_html_content(lang=selected_lang)
                save_pdf_report(file_path, html)
                QMessageBox.information(self, tr("Sucesso"), f"{tr('Relatório PDF salvo com sucesso em:')}\n{file_path}")
        except Exception as e:
            import traceback
            QMessageBox.critical(
                self, tr("Erro ao gerar PDF"),
                f"{tr('Falha ao gerar PDF')}:\n{str(e)}\n\n{traceback.format_exc()}"
            )
        finally:
            set_current_lang(prev_lang)
            self.update_report_preview()

    def export_html(self):
        from triton import get_auditable_filename
        prev_lang = get_current_lang()
        selected_lang = self.combo_report_lang.currentData() or "pt"
        set_current_lang(selected_lang)

        try:
            self.update_report_preview()
            rep_type = self.combo_report_type.currentData() or "economic"
            suffix = artefato_de_laudo(rep_type) + self._etiqueta_da_edicao()
            project_name = self._project_data.get("project_name", "Projeto Triton")
            def_name = get_auditable_filename(
                project_name, self._project_data["ref_code"], f"{suffix}-{selected_lang}", "html"
            )

            file_path, _ = QFileDialog.getSaveFileName(
                self, tr("Salvar Relatório em HTML"), def_name, f"{tr('Página Web')} (*.html)"
            )
            if file_path:
                html = self.generate_html_content(lang=selected_lang)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)
                QMessageBox.information(self, tr("Sucesso"), f"{tr('Relatório HTML salvo com sucesso em:')}\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao salvar HTML')}:\n{str(e)}")
        finally:
            set_current_lang(prev_lang)
            self.update_report_preview()
