"""
Aba 10: Central de Exportação de Dados, Planilhas e Projetos CAD (Netuno 5).
Permite exportar planilhas Excel/CSV completas e personalizadas da simulação,
arquivos de projeto, templates de cenários e desenhos técnicos em formato CAD DXF / Vetorial SVG.
"""

import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QFileDialog, QMessageBox, QScrollArea, QGridLayout, QGroupBox,
    QCheckBox, QComboBox, QRadioButton, QButtonGroup, QDialog
)
from PySide6.QtCore import Qt, QUrl, QByteArray
from PySide6.QtGui import QFont, QDesktopServices, QPixmap, QPainter, QColor, QImage
from PySide6.QtSvg import QSvgRenderer

from netuno.ui.translation import tr, get_current_theme
from netuno.core.cad_exporter import generate_project_dxf, generate_project_svg_diagram
from netuno.core.simulation_excel_exporter import export_simulation_to_excel, export_simulation_to_csv


class TabExport(QWidget):
    """Aba central de exportação do Netuno 5 com personalização e design responsivo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._last_exported_path = None
        self.init_ui()

    def init_ui(self):
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(32, 28, 32, 36)
        layout.setSpacing(16)

        is_dark = get_current_theme() == "dark"

        # ── HEADER DA ABA ──
        header_lay = QVBoxLayout()
        lbl_title = QLabel(tr("Central de Exportação de Dados e Projetos"))
        lbl_title.setStyleSheet("""
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 25px;
            font-weight: 700;
            color: #133c32;
        """)
        lbl_sub = QLabel(tr(
            "Exporte planilhas personalizadas de simulação, dados brutos, arquivos de projeto "
            "e esquemas unifilares em CAD DXF / Vetorial para integração com softwares de engenharia."
        ))
        lbl_sub.setWordWrap(True)
        lbl_sub.setStyleSheet("font-size: 13px; color: #475569; margin-top: 2px;")
        header_lay.addWidget(lbl_title)
        header_lay.addWidget(lbl_sub)
        layout.addLayout(header_lay)

        # ── STATUS / FEEDBACK BANNER ──
        self.lbl_status = QLabel(tr("Pronto para exportar. Escolha os formatos e dados desejados abaixo."))
        self.lbl_status.setStyleSheet("""
            background-color: #f1f5f9;
            color: #334155;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 9px 14px;
            font-size: 12.5px;
            font-weight: 500;
        """)
        layout.addWidget(self.lbl_status)

        # =========================================================================
        # SEÇÃO 1: PERSONALIZAÇÃO DA EXPORTAÇÃO DE PLANILHAS (EXCEL / CSV)
        # =========================================================================
        card_custom_sheets = QFrame()
        card_custom_sheets.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 12px;
            }
        """)
        lay_custom = QVBoxLayout(card_custom_sheets)
        lay_custom.setContentsMargins(20, 18, 20, 18)
        lay_custom.setSpacing(14)

        # Título da Seção
        header_custom = QHBoxLayout()
        lbl_cs_title = QLabel(tr("📊 Personalização da Exportação de Planilhas e Dados"))
        lbl_cs_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #064e3b; border: none; background: transparent;")
        header_custom.addWidget(lbl_cs_title)
        header_custom.addStretch()

        btn_all = QPushButton(tr("Marcar Todas"))
        btn_all.setStyleSheet("font-size: 11px; padding: 4px 10px; background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 4px;")
        btn_all.clicked.connect(lambda: self._set_all_checkboxes(True))
        btn_none = QPushButton(tr("Desmarcar Todas"))
        btn_none.setStyleSheet("font-size: 11px; padding: 4px 10px; background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 4px;")
        btn_none.clicked.connect(lambda: self._set_all_checkboxes(False))
        header_custom.addWidget(btn_all)
        header_custom.addWidget(btn_none)
        lay_custom.addLayout(header_custom)

        lbl_cs_desc = QLabel(tr("Escolha quais conjuntos de dados analíticos deseja incluir no arquivo e configure as preferências de formatação:"))
        lbl_cs_desc.setWordWrap(True)
        lbl_cs_desc.setStyleSheet("color: #64748b; font-size: 12px; border: none; background: transparent;")
        lay_custom.addWidget(lbl_cs_desc)

        # Grade de Seleção de Abas/Dados (2 colunas equilibradas)
        grid_checks = QGridLayout()
        grid_checks.setSpacing(10)

        self.chk_resumo = QCheckBox(tr("📄 1. Resumo Executivo e Metadados do Projeto"))
        self.chk_resumo.setChecked(True)
        self.chk_resumo.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_resumo, 0, 0)

        self.chk_balanco = QCheckBox(tr("💧 2. Balanço Hídrico Diário (Chuva, Demanda e Consumo)"))
        self.chk_balanco.setChecked(True)
        self.chk_balanco.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_balanco, 0, 1)

        self.chk_varredura = QCheckBox(tr("📈 3. Curva de Varredura de Volumes e Confiabilidade"))
        self.chk_varredura.setChecked(True)
        self.chk_varredura.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_varredura, 1, 0)

        self.chk_fluxo = QCheckBox(tr("💰 4. Fluxo de Caixa Econômico (CAPEX, OPEX e Retorno)"))
        self.chk_fluxo.setChecked(True)
        self.chk_fluxo.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_fluxo, 1, 1)

        self.chk_acv = QCheckBox(tr("🍃 5. Inventário de Ciclo de Vida (ACV e Carbono ESG)"))
        self.chk_acv.setChecked(True)
        self.chk_acv.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_acv, 2, 0)

        self.chk_mcdm = QCheckBox(tr("🏆 6. Matriz de Decisão Multicritério (TOPSIS / VIKOR)"))
        self.chk_mcdm.setChecked(True)
        self.chk_mcdm.setStyleSheet("font-weight: 600; color: #1e293b; border: none; background: transparent;")
        grid_checks.addWidget(self.chk_mcdm, 2, 1)

        lay_custom.addLayout(grid_checks)

        # Linha de Opções de Formatação
        opts_box = QFrame()
        opts_box.setObjectName("optsBox")
        opts_box.setStyleSheet("#optsBox { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px; }")
        lay_opts = QHBoxLayout(opts_box)
        lay_opts.setSpacing(14)

        # Formato de Arquivo
        lay_opts.addWidget(QLabel(tr("<b>Formato:</b>")))
        self.combo_format = QComboBox()
        self.combo_format.addItem(tr("Pasta de Trabalho Excel (.xlsx)"), "xlsx")
        self.combo_format.addItem(tr("Texto Delimitado CSV (.csv)"), "csv")
        self.combo_format.currentIndexChanged.connect(self._on_format_changed)
        lay_opts.addWidget(self.combo_format)

        # Delimitador CSV (visível apenas se CSV for selecionado)
        self.lbl_delim = QLabel(tr("<b>Separador:</b>"))
        self.combo_delim = QComboBox()
        self.combo_delim.addItem(tr("Ponto e vírgula (;) [Padrão Brasil/Excel]"), ";")
        self.combo_delim.addItem(tr("Vírgula (,) [Padrão Internacional/R]"), ",")
        lay_opts.addWidget(self.lbl_delim)
        lay_opts.addWidget(self.combo_delim)
        self.lbl_delim.hide()
        self.combo_delim.hide()

        # Horizonte Econômico
        lay_opts.addWidget(QLabel(tr("<b>Horizonte Econômico:</b>")))
        self.combo_horizon = QComboBox()
        self.combo_horizon.addItem(tr("20 Anos (Padrão)"), 20)
        self.combo_horizon.addItem(tr("10 Anos"), 10)
        self.combo_horizon.addItem(tr("25 Anos"), 25)
        self.combo_horizon.addItem(tr("30 Anos"), 30)
        lay_opts.addWidget(self.combo_horizon)

        # Granularidade Diária
        lay_opts.addWidget(QLabel(tr("<b>Filtro Temporal:</b>")))
        self.combo_daily_mode = QComboBox()
        self.combo_daily_mode.addItem(tr("Série Histórica Completa"), "all")
        self.combo_daily_mode.addItem(tr("Primeiro Ano Típico (365 dias)"), "year1")
        lay_opts.addWidget(self.combo_daily_mode)
        lay_opts.addStretch()

        lay_custom.addWidget(opts_box)

        # Botão Principal de Exportação Personalizada
        btn_action_row = QHBoxLayout()
        self.btn_export_custom = QPushButton(tr("🚀 Exportar Planilha Personalizada..."))
        self.btn_export_custom.setStyleSheet("""
            QPushButton {
                font-size: 13px;
                font-weight: bold;
                background-color: #059669;
                color: white;
                padding: 10px 22px;
                border-radius: 7px;
                border: none;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        self.btn_export_custom.clicked.connect(self._export_custom_planilha)
        btn_action_row.addWidget(self.btn_export_custom)

        btn_batch_tpl = QPushButton(tr("📋 Baixar Modelo de Cenários em Lote (.xlsx)"))
        btn_batch_tpl.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: 600;
                background-color: #f1f5f9;
                color: #334155;
                padding: 10px 16px;
                border-radius: 7px;
                border: 1.5px solid #cbd5e1;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        btn_batch_tpl.clicked.connect(self._export_batch_template)
        btn_action_row.addWidget(btn_batch_tpl)
        btn_action_row.addStretch()

        lay_custom.addLayout(btn_action_row)
        layout.addWidget(card_custom_sheets)

        # =========================================================================
        # SEÇÃO 2: ARQUIVOS DE PROJETO & ESQUEMAS TÉCNICOS CAD (2 CARDS EMPILHADOS)
        # =========================================================================
        sec_bottom_grid = QGridLayout()
        sec_bottom_grid.setSpacing(16)

        # Card: Arquivos de Projeto Netuno
        card_proj = self._create_card(
            title=tr("📁 Arquivos de Projeto Netuno"),
            desc=tr("Salve o estado do projeto para reutilização, auditoria ou compartilhamento:"),
            buttons=[
                (tr("💾 Salvar Projeto (.netuno)"), self._export_project_netuno, "#0d9488"),
                (tr("🌐 Exportar JSON (.json)"), self._export_project_json, "#087f6b"),
                (tr("📜 Exportar CSV Legado (.csv)"), self._export_project_legacy_csv, "#475569"),
            ]
        )
        sec_bottom_grid.addWidget(card_proj, 0, 0)

        # Card: Desenho Técnico CAD & Diagrama Unifilar
        card_cad = QFrame()
        card_cad.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 12px;
            }
        """)
        lay_cad = QVBoxLayout(card_cad)
        lay_cad.setContentsMargins(18, 16, 18, 16)
        lay_cad.setSpacing(10)

        lbl_cad_t = QLabel(tr("📐 Desenho Técnico CAD & Diagrama Unifilar"))
        lbl_cad_t.setStyleSheet("font-family: 'Segoe UI', system-ui, sans-serif; font-size: 14.5px; font-weight: 700; color: #064e3b; border: none; background: transparent;")
        lay_cad.addWidget(lbl_cad_t)

        lbl_cad_d = QLabel(tr("Gere pranchas A3, diagramas ou uma biblioteca de blocos 1:1 mm com manifesto BIM para AutoCAD e Revit:"))
        lbl_cad_d.setWordWrap(True)
        lbl_cad_d.setStyleSheet("color: #64748b; font-size: 11.5px; border: none; background: transparent;")
        lay_cad.addWidget(lbl_cad_d)

        # Seletor de Modo CAD
        lay_cad_mode = QHBoxLayout()
        lay_cad_mode.setSpacing(8)
        lbl_cad_mode = QLabel(tr("Padrão do Desenho:"))
        lbl_cad_mode.setStyleSheet("font-size: 12px; font-weight: 600; color: #334155; border: none; background: transparent;")
        self.combo_cad_mode = QComboBox()
        self.combo_cad_mode.addItem(tr("📐 Prancha Técnica Completa em A3 (Engenharia NBR 15527)"), "technical_a3")
        self.combo_cad_mode.addItem(tr("✏️ Esquemático Unifilar Simples (Apresentação Rápida)"), "simple")
        self.combo_cad_mode.addItem(tr("🧩 Biblioteca de Blocos para Plantas + BIM JSON"), "block_library")
        self.combo_cad_mode.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 1.5px solid #cbd5e1;
                border-radius: 6px;
                background-color: #f8fafc;
                font-size: 12px;
                font-weight: 600;
                color: #0f172a;
            }
            QComboBox:focus {
                border-color: #0284c7;
            }
        """)
        lay_cad_mode.addWidget(lbl_cad_mode)
        lay_cad_mode.addWidget(self.combo_cad_mode, 1)
        lay_cad.addLayout(lay_cad_mode)

        # Botões organizados em grade
        btn_grid_cad = QGridLayout()
        btn_grid_cad.setSpacing(8)
        btn_preview = QPushButton(tr("👁️ Pré-visualizar Desenho"))
        btn_preview.setStyleSheet("font-size: 12px; font-weight: bold; background-color: #0d9488; color: white; padding: 9px 16px; border-radius: 6px; border: none;")
        btn_preview.clicked.connect(self._preview_cad_drawing)

        btn_dxf = QPushButton(tr("📐 Exportar CAD (.dxf)"))
        btn_dxf.setStyleSheet("font-size: 12px; font-weight: bold; background-color: #b45309; color: white; padding: 9px 16px; border-radius: 6px; border: none;")
        btn_dxf.clicked.connect(self._export_cad_dxf)

        btn_svg = QPushButton(tr("🎨 Exportar Vetorial (.svg)"))
        btn_svg.setStyleSheet("font-size: 12px; font-weight: bold; background-color: #d97706; color: white; padding: 9px 16px; border-radius: 6px; border: none;")
        btn_svg.clicked.connect(self._export_diagram_svg)

        btn_open = QPushButton(tr("📂 Abrir Pasta"))
        btn_open.setStyleSheet("font-size: 12px; font-weight: bold; background-color: #334155; color: white; padding: 9px 16px; border-radius: 6px; border: none;")
        btn_open.clicked.connect(self._open_last_folder)

        btn_grid_cad.addWidget(btn_preview, 0, 0)
        btn_grid_cad.addWidget(btn_dxf, 0, 1)
        btn_grid_cad.addWidget(btn_svg, 0, 2)
        btn_grid_cad.addWidget(btn_open, 0, 3)
        lay_cad.addLayout(btn_grid_cad)

        sec_bottom_grid.addWidget(card_cad, 0, 1)

        layout.addLayout(sec_bottom_grid)
        layout.addStretch()

        scroll.setWidget(content_widget)
        main_vbox.addWidget(scroll)

    def _on_format_changed(self):
        """Alterna a exibição das opções de separador conforme o formato."""
        is_csv = (self.combo_format.currentData() == "csv")
        self.lbl_delim.setVisible(is_csv)
        self.combo_delim.setVisible(is_csv)

    def _set_all_checkboxes(self, state: bool):
        """Marca ou desmarca todas as caixas de seleção."""
        for chk in [self.chk_resumo, self.chk_balanco, self.chk_varredura, self.chk_fluxo, self.chk_acv, self.chk_mcdm]:
            chk.setChecked(state)

    def _create_card(self, title: str, desc: str, buttons: list) -> QFrame:
        """Cria um cartão com layout interno flexível e sem estourar a largura."""
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1.5px solid #cbd5e1;
                border-radius: 12px;
            }
        """)
        lay = QVBoxLayout(box)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("""
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-size: 14.5px;
            font-weight: 700;
            color: #064e3b;
            border: none;
            background: transparent;
        """)
        lay.addWidget(lbl_t)

        lbl_d = QLabel(desc)
        lbl_d.setWordWrap(True)
        lbl_d.setStyleSheet("color: #64748b; font-size: 11.5px; border: none; background: transparent;")
        lay.addWidget(lbl_d)

        # Botões organizados em grade responsiva (wrap) em vez de linha única infinita
        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)
        for idx, (btn_text, handler, bg_color) in enumerate(buttons):
            btn = QPushButton(btn_text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 11.5px;
                    font-weight: bold;
                    background-color: {bg_color};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {bg_color};
                    border: 1px solid rgba(255,255,255,0.4);
                }}
            """)
            btn.clicked.connect(handler)
            row = idx // 2
            col = idx % 2
            if len(buttons) == 3 and idx == 2:
                btn_grid.addWidget(btn, 1, 0, 1, 2)
            else:
                btn_grid.addWidget(btn, row, col)

        lay.addLayout(btn_grid)
        return box

    def _get_main_window(self):
        return self.window()

    def _collect_project_data(self) -> dict:
        mw = self._get_main_window()
        data = {}
        if mw and hasattr(mw, "tab_reports"):
            try:
                mw.tab_reports.update_report_preview()
            except Exception:
                pass
            data = getattr(mw.tab_reports, "_project_data", {}) or {}

        # Garante a passagem do volume superior configurado para o gerador de CAD
        if not data.get("upper_vol") or data.get("upper_vol") <= 0:
            if mw and hasattr(mw, "config") and getattr(mw.config, "upper_tank_vol", 0) > 0:
                data["upper_vol"] = float(mw.config.upper_tank_vol)
            elif mw and hasattr(mw, "tab_tanks_simulation") and hasattr(mw.tab_tanks_simulation, "txt_upper_vol"):
                try:
                    data["upper_vol"] = float(mw.tab_tanks_simulation.txt_upper_vol.text().replace(',', '.'))
                except Exception:
                    pass
        return data

    def _set_status(self, text: str, is_success: bool = True):
        bg = "#ecfdf5" if is_success else "#fef2f2"
        fg = "#065f46" if is_success else "#991b1b"
        border = "#a7f3d0" if is_success else "#fecaca"
        self.lbl_status.setText(text)
        self.lbl_status.setStyleSheet(f"""
            background-color: {bg};
            color: {fg};
            border: 1.5px solid {border};
            border-radius: 6px;
            padding: 9px 14px;
            font-size: 12.5px;
            font-weight: 600;
        """)

    # ── EXPORTAÇÃO PERSONALIZADA ──

    def _export_custom_planilha(self):
        """Exporta a planilha com a seleção de abas, horizonte e formato definidos pelo usuário."""
        fmt = self.combo_format.currentData()
        data = self._collect_project_data()
        mw = self._get_main_window()

        single_res = getattr(mw.tab_tanks_simulation, "last_single_result", None) if mw else None
        sweep_res = getattr(mw.tab_tanks_simulation, "last_sweep_result", None) if mw else None
        eco_res = getattr(mw.tab_economic, "last_economic_result", None) if mw else None
        env_res = getattr(mw.tab_environmental, "last_env_result", None) if mw else None
        mcdm_res = getattr(mw.tab_global_optimizer, "last_mcdm_result", None) if mw else None

        selected_sheets = {
            "resumo": self.chk_resumo.isChecked(),
            "balanco": self.chk_balanco.isChecked(),
            "varredura": self.chk_varredura.isChecked(),
            "fluxo": self.chk_fluxo.isChecked(),
            "acv": self.chk_acv.isChecked(),
            "mcdm": self.chk_mcdm.isChecked()
        }

        if not any(selected_sheets.values()):
            QMessageBox.warning(self, tr("Aviso"), tr("Selecione pelo menos um conjunto de dados para exportação."))
            return

        horizon = int(self.combo_horizon.currentData() or 20)
        daily_mode = str(self.combo_daily_mode.currentData() or "all")
        proj_slug = str(data.get("project_name", "Simulacao_Netuno")).replace(" ", "_")

        if fmt == "xlsx":
            file_path, _ = QFileDialog.getSaveFileName(
                self, tr("Exportar Planilha Excel Personalizada"),
                f"{proj_slug}_Dados_Simulados.xlsx",
                "Planilhas Excel (*.xlsx)"
            )
            if not file_path:
                return

            try:
                export_simulation_to_excel(
                    project_data=data,
                    file_path=file_path,
                    single_result=single_res,
                    sweep_result=sweep_res,
                    economic_result=eco_res,
                    environmental_result=env_res,
                    mcdm_result=mcdm_res,
                    selected_sheets=selected_sheets,
                    horizon_years=horizon,
                    daily_mode=daily_mode
                )
                self._last_exported_path = file_path
                n_sheets = sum(1 for v in selected_sheets.values() if v)
                self._set_status(tr(f"✓ Planilha Excel exportada com sucesso: {Path(file_path).name} ({n_sheets} abas)"))
            except Exception as e:
                QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao gerar planilha Excel: {e}"))
        else:
            # Formato CSV
            delimiter = str(self.combo_delim.currentData() or ";")
            file_path, _ = QFileDialog.getSaveFileName(
                self, tr("Exportar Dados em CSV"),
                f"{proj_slug}_Balanco_Hidrico.csv",
                "Arquivos CSV (*.csv)"
            )
            if not file_path:
                return

            try:
                export_simulation_to_csv(
                    project_data=data,
                    file_path=file_path,
                    single_result=single_res,
                    delimiter=delimiter,
                    mode=daily_mode
                )
                self._last_exported_path = file_path
                self._set_status(tr(f"✓ Arquivo CSV exportado com sucesso: {Path(file_path).name} (delimitador '{delimiter}')"))
            except Exception as e:
                QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao gerar arquivo CSV: {e}"))

    # ── OUTROS HANDLERS ──

    def _export_project_netuno(self):
        mw = self._get_main_window()
        if mw and hasattr(mw, "save_project"):
            mw.save_project()
            self._set_status(tr("✓ Projeto Netuno salvo com sucesso!"))

    def _export_project_json(self):
        data = self._collect_project_data()
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("Exportar Dados em JSON"), "projeto_netuno.json", "Arquivos JSON (*.json)"
        )
        if not file_path:
            return

        try:
            def _default(o):
                if hasattr(o, "isoformat"):
                    return o.isoformat()
                return str(o)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=_default)
            self._last_exported_path = file_path
            self._set_status(tr(f"✓ Dados JSON exportados com sucesso em: {Path(file_path).name}"))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao exportar JSON: {e}"))

    def _export_project_legacy_csv(self):
        mw = self._get_main_window()
        if mw and hasattr(mw, "export_legacy_csv"):
            mw.export_legacy_csv()
            self._set_status(tr("✓ Projeto exportado em formato CSV legado."))

    def _export_batch_template(self):
        mw = self._get_main_window()
        if mw and hasattr(mw, "on_download_excel_sample"):
            mw.on_download_excel_sample()
            self._set_status(tr("✓ Modelo de cenários em lote gerado com sucesso."))
        elif mw and hasattr(mw, "generate_batch_template"):
            mw.generate_batch_template()
            self._set_status(tr("✓ Modelo de cenários em lote gerado com sucesso."))
        else:
            from netuno.core.excel_scenarios import generate_sample_scenario_excel
            file_path, _ = QFileDialog.getSaveFileName(self, tr("Salvar Modelo Excel de Cenários"), "netuno-modelo-cenarios.xlsx", "Planilha Excel (*.xlsx)")
            if file_path:
                generate_sample_scenario_excel(file_path)
                self._set_status(tr(f"✓ Modelo de cenários salvo em: {Path(file_path).name}"))

    def _export_cad_dxf(self):
        data = self._collect_project_data()
        proj_slug = str(data.get("project_name", "Esquema_Hidraulico")).replace(" ", "_")
        mode = self.combo_cad_mode.currentData() if hasattr(self, "combo_cad_mode") else "technical_a3"
        mode_slug = {"technical_a3": "Prancha_A3", "simple": "Esquematico", "block_library": "Biblioteca_Blocos"}.get(mode, "CAD")
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("Exportar Esquema em CAD DXF"),
            f"{proj_slug}_{mode_slug}_Netuno.dxf",
            "Desenho CAD DXF (*.dxf)"
        )
        if not file_path:
            return

        try:
            generate_project_dxf(data, file_path, mode=mode)
            self._last_exported_path = file_path
            lbl_mode = {"technical_a3": tr("Prancha Técnica A3"), "simple": tr("Esquemático Simples"), "block_library": tr("Biblioteca de Blocos + BIM JSON")}.get(mode, tr("CAD"))
            suffix = tr("; manifesto BIM salvo ao lado do DXF") if mode == "block_library" else ""
            self._set_status(tr(f"✓ Desenho CAD DXF exportado ({lbl_mode}): {Path(file_path).name}{suffix}"))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao gerar desenho CAD DXF: {e}"))

    def _export_diagram_svg(self):
        data = self._collect_project_data()
        proj_slug = str(data.get("project_name", "Diagrama_Unifilar")).replace(" ", "_")
        mode = self.combo_cad_mode.currentData() if hasattr(self, "combo_cad_mode") else "technical_a3"
        if mode == "block_library":
            QMessageBox.information(self, tr("Biblioteca CAD"), tr("A biblioteca é entregue em DXF 1:1 mm e JSON BIM. Selecione ‘Exportar CAD (.dxf)’ para gerar o pacote."))
            return
        mode_slug = "Prancha_A3" if mode == "technical_a3" else "Esquematico"
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("Exportar Diagrama Técnico em SVG"),
            f"{proj_slug}_{mode_slug}_Netuno.svg",
            "Imagem Vetorial SVG (*.svg)"
        )
        if not file_path:
            return

        try:
            generate_project_svg_diagram(data, file_path, mode=mode)
            self._last_exported_path = file_path
            lbl_mode = tr("Prancha Técnica A3") if mode == "technical_a3" else tr("Esquemático Simples")
            self._set_status(tr(f"✓ Diagrama vetorial SVG exportado ({lbl_mode}): {Path(file_path).name}"))
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao exportar diagrama SVG: {e}"))

    def _preview_cad_drawing(self):
        data = self._collect_project_data()
        mode = self.combo_cad_mode.currentData() if hasattr(self, "combo_cad_mode") else "technical_a3"
        if mode == "block_library":
            QMessageBox.information(
                self, tr("Biblioteca CAD"),
                tr("A biblioteca de blocos é exportada em formato CAD DXF 1:1 e manifesto BIM JSON.")
            )
            return

        try:
            svg_content = generate_project_svg_diagram(data, mode=mode)
            renderer = QSvgRenderer(QByteArray(svg_content.encode("utf-8")))
            if not renderer.isValid():
                QMessageBox.warning(self, tr("Aviso"), tr("Não foi possível renderizar a imagem vetorial."))
                return

            w = 1200 if mode == "technical_a3" else 950
            h = 850 if mode == "technical_a3" else 650
            image = QImage(w, h, QImage.Format_ARGB32)
            image.fill(QColor("white"))
            painter = QPainter(image)
            renderer.render(painter)
            painter.end()

            pixmap = QPixmap.fromImage(image)

            dlg = QDialog(self)
            dlg.setWindowTitle(tr("👁️ Pré-visualização do Desenho CAD / Prancha Técnica"))
            dlg.resize(1150, 800)
            dlg_lay = QVBoxLayout(dlg)
            dlg_lay.setContentsMargins(16, 14, 16, 14)
            dlg_lay.setSpacing(10)

            top_bar = QHBoxLayout()
            mode_name = tr("Prancha Técnica A3 (ABNT NBR 15527)") if mode == "technical_a3" else tr("Esquema Unifilar Simples")
            organization = str(data.get("organization") or tr("Organização a definir"))
            responsible = str(data.get("technical_responsible") or tr("Responsável técnico a definir"))
            lbl_info = QLabel(f"<b>{tr('Padrão:')}</b> {mode_name} | <b>{tr('Organização:')}</b> {organization} | <b>{tr('Responsável:')}</b> {responsible}")
            lbl_info.setStyleSheet("font-size: 12px; color: #1e293b;")
            top_bar.addWidget(lbl_info)
            top_bar.addStretch()

            btn_dxf_now = QPushButton(tr("📐 Exportar DXF"))
            btn_dxf_now.setStyleSheet("font-size: 11px; font-weight: bold; background-color: #b45309; color: white; padding: 5px 12px; border-radius: 4px;")
            btn_dxf_now.clicked.connect(lambda: (dlg.accept(), self._export_cad_dxf()))
            top_bar.addWidget(btn_dxf_now)

            btn_close = QPushButton(tr("Fechar"))
            btn_close.setStyleSheet("font-size: 11px; padding: 5px 12px;")
            btn_close.clicked.connect(dlg.accept)
            top_bar.addWidget(btn_close)
            dlg_lay.addLayout(top_bar)

            scroll_prev = QScrollArea()
            scroll_prev.setWidgetResizable(True)
            scroll_prev.setObjectName("scrollPrev")
            scroll_prev.setStyleSheet("#scrollPrev { background-color: #334155; border: 1px solid #cbd5e1; border-radius: 6px; }")
            lbl_img = QLabel()
            lbl_img.setPixmap(pixmap)
            lbl_img.setAlignment(Qt.AlignCenter)
            scroll_prev.setWidget(lbl_img)
            dlg_lay.addWidget(scroll_prev, stretch=1)

            dlg.exec()
        except Exception as e:
            QMessageBox.critical(self, tr("Erro"), tr(f"Falha ao pré-visualizar desenho: {e}"))

    def _open_last_folder(self):
        folder = Path(self._last_exported_path).parent if self._last_exported_path else Path.cwd()
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
