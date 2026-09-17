"""
Janela Principal da Aplicação Netuno 5.
Interface moderna com navegação por Sidebar em 6 Etapas, Live Preview e Sem Pop-ups.
"""

import os
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMenuBar, QMenu, QMessageBox, QFileDialog,
    QToolBar, QLabel, QVBoxLayout, QFrame, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon

from netuno.ui.theme import NETUNO4_CLASSIC_QSS
from netuno import APP_TITLE, APP_VERSION_LABEL, __version__
from netuno.ui.sidebar import Sidebar
from netuno.core.parser import NetunoConfig
from netuno.ui.translation import tr, get_current_lang, get_available_languages, get_resource_path, restart_app

from netuno.ui.tab_project import TabProject
from netuno.ui.tab_building import TabBuilding
from netuno.ui.tab_water_quality import TabWaterQuality
from netuno.ui.tab_tanks_simulation import TabTanksSimulation
from netuno.ui.tab_charts_netuno import TabChartsNetuno
from netuno.ui.tab_economic_integrated import TabEconomicIntegrated
from netuno.ui.tab_environmental import TabEnvironmental
from netuno.ui.tab_reports_pdf import TabReportsPdf
from netuno.ui.tab_export import TabExport
from netuno.ui.tab_documentation import TabDocumentation
from netuno.ui.tab_tariffs_manager import TabTariffsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        from netuno import get_kebab_filename
        self.get_kebab_filename = get_kebab_filename
        self.setWindowTitle(tr(APP_TITLE))
        self.resize(1280, 760)
        self.setMinimumSize(900, 600)
        self.config = NetunoConfig()
        
        logo_path = get_resource_path("Netuno2.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        self.setStyleSheet(NETUNO4_CLASSIC_QSS)

        self.init_menu_bar()
        self.init_ui()

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        # Menu Arquivo
        menu_file = menu_bar.addMenu(tr("Arquivo"))
        
        action_new = QAction(tr("Novo Projeto"), self)
        menu_file.addAction(action_new)

        action_open = QAction(tr("Carregar Projeto CSV..."), self)
        action_open.triggered.connect(self.on_load_simulation)
        menu_file.addAction(action_open)

        action_save = QAction(tr("Salvar Projeto..."), self)
        action_save.triggered.connect(self.on_save_simulation)
        menu_file.addAction(action_save)

        menu_file.addSeparator()

        action_exit = QAction(tr("Sair"), self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        # Área de execução e cenários: uma seção própria torna as ações de
        # projeto e as ações de análise claramente distintas.
        menu_sim = menu_bar.addMenu(tr("Cenários && Ferramentas"))

        action_excel_sample = QAction(tr("Baixar Planilha Modelo Excel (.xlsx)..."), self)
        action_excel_sample.triggered.connect(self.on_download_excel_sample)
        menu_sim.addAction(action_excel_sample)

        action_excel_import = QAction(tr("Importar e Simular Cenários em Lote (Excel)..."), self)
        action_excel_import.triggered.connect(self.on_import_excel_scenarios)
        menu_sim.addAction(action_excel_import)

        action_export_tab = QAction(tr("Central de Exportação (Planilhas, CAD e Projeto)..."), self)
        action_export_tab.triggered.connect(lambda: self.on_step_changed(9))
        menu_sim.addAction(action_export_tab)

        menu_sim.addSeparator()
        action_tariffs_mgr = QAction(tr("Gestor Nacional de Tarifas & Auditoria (652 Cidades)..."), self)
        action_tariffs_mgr.triggered.connect(lambda: self.on_step_changed(11))
        menu_sim.addAction(action_tariffs_mgr)

        # Menu Opções
        menu_options = menu_bar.addMenu(tr("Opções"))

        # Submenu Idioma
        menu_lang = menu_options.addMenu(tr("Idioma"))
        self.action_pt = QAction(tr("Português"), self)
        self.action_pt.setCheckable(True)
        self.action_pt.setChecked(get_current_lang() == "pt")
        self.action_pt.triggered.connect(lambda: self.set_language("pt"))

        self.action_en = QAction(tr("Inglês"), self)
        self.action_en.setCheckable(True)
        self.action_en.setChecked(get_current_lang() == "en")
        self.action_en.triggered.connect(lambda: self.set_language("en"))

        menu_lang.addAction(self.action_pt)
        menu_lang.addAction(self.action_en)
        language_actions = [self.action_pt, self.action_en]
        if "es" in get_available_languages():
            self.action_es = QAction("Español", self)
            self.action_es.setCheckable(True)
            self.action_es.setChecked(get_current_lang() == "es")
            self.action_es.triggered.connect(lambda: self.set_language("es"))
            menu_lang.addAction(self.action_es)
            language_actions.append(self.action_es)
        if "zh" in get_available_languages():
            self.action_zh = QAction("中文 (简体)", self)
            self.action_zh.setCheckable(True)
            self.action_zh.setChecked(get_current_lang() == "zh")
            self.action_zh.triggered.connect(lambda: self.set_language("zh"))
            menu_lang.addAction(self.action_zh)
            language_actions.append(self.action_zh)
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)
        for action in language_actions:
            lang_group.addAction(action)

        # Menu Ajuda
        menu_ajuda = menu_bar.addMenu(tr("Ajuda"))
        action_manual = QAction(tr(f"Manual do Usuário — Netuno {__version__}"), self)
        action_manual.triggered.connect(self.on_show_manual)
        menu_ajuda.addAction(action_manual)

        action_citacao = QAction(tr("Como Citar o Netuno"), self)
        action_citacao.triggered.connect(self.on_show_citation)
        menu_ajuda.addAction(action_citacao)

        action_val_report = QAction(tr("Relatório de Verificação Técnica e Computacional..."), self)
        action_val_report.triggered.connect(self.on_show_validation_report)
        menu_ajuda.addAction(action_val_report)

        action_doc = QAction(tr("Documentação das Variáveis e Fontes (MIX Sustentável)..."), self)
        action_doc.triggered.connect(lambda: self.on_step_changed(10))

        menu_ajuda.addAction(action_doc)

        action_sobre = QAction(tr(f"Sobre o Netuno {__version__}"), self)
        action_sobre.triggered.connect(self.on_show_about)
        menu_ajuda.addAction(action_sobre)

    def set_theme(self, theme):
        """Compatibilidade interna: a edição atual é exclusivamente clara."""
        self.setStyleSheet(NETUNO4_CLASSIC_QSS)

        if hasattr(self, 'sidebar'):
            self.sidebar.init_ui()
            self.sync_project_state()
        if hasattr(self, 'stack'):
            cur_idx = self.stack.currentIndex()
            # A documentação possui conteúdo HTML com cores editoriais próprias;
            # recriá-la aplica o tema novo também aos navegadores internos.
            if hasattr(self, "tab_documentation"):
                old_doc = self.tab_documentation
                doc_index = self.stack.indexOf(old_doc)
                if doc_index >= 0:
                    self.stack.removeWidget(old_doc)
                    self.tab_documentation = TabDocumentation(self)
                    self.stack.insertWidget(doc_index, self.tab_documentation)
                    old_doc.deleteLater()
            self.on_step_changed(cur_idx)

    def set_language(self, lang):
        from netuno.ui.translation import set_current_lang
        set_current_lang(lang)
        self.action_pt.setChecked(lang == "pt")
        self.action_en.setChecked(lang == "en")
        if hasattr(self, "action_es"):
            self.action_es.setChecked(lang == "es")
        if hasattr(self, "action_zh"):
            self.action_zh.setChecked(lang == "zh")

        restart_copy = {
            "pt": ("Reiniciar Aplicativo", "Deseja reiniciar o aplicativo para aplicar as alterações de idioma?"),
            "en": ("Restart Application", "Do you want to restart the application to apply the language changes?"),
            "es": ("Reiniciar aplicación", "¿Desea reiniciar la aplicación para aplicar el cambio de idioma?"),
            "zh": ("重启应用", "是否重启应用以应用语言更改？"),
        }
        title, msg = restart_copy.get(lang, restart_copy["pt"])
        
        reply = QMessageBox.question(
            self, 
            title,
            msg,
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.Yes
        )
        if reply == QMessageBox.Yes:
            restart_app()


    def init_ui(self):
        central_widget = QWidget(self)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Componente Sidebar Lateral
        self.sidebar = Sidebar(self)
        self.sidebar.step_changed.connect(self.on_step_changed)
        main_layout.addWidget(self.sidebar)

        # 2. Área direita com contexto do projeto, como na edição web.
        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        workspace_header = QFrame()
        workspace_header.setObjectName("workspaceHeader")
        header_layout = QHBoxLayout(workspace_header)
        header_layout.setContentsMargins(30, 12, 30, 12)
        project_block = QVBoxLayout()
        project_block.setSpacing(1)
        eyebrow = QLabel(tr("PROJETO ATUAL"))
        eyebrow.setObjectName("workspaceEyebrow")
        from PySide6.QtWidgets import QLineEdit
        self.txt_workspace_project = QLineEdit(getattr(self.config, "project_name", tr("Novo projeto Netuno")))
        self.txt_workspace_project.setObjectName("workspaceProjectInput")
        self.txt_workspace_project.setPlaceholderText(tr("Nome do projeto"))
        self.txt_workspace_project.setToolTip(tr("Edite o nome do projeto. Ele será salvo no projeto e no nome do arquivo."))
        self.txt_workspace_project.textChanged.connect(self._on_project_name_changed)
        project_block.addWidget(eyebrow)
        project_block.addWidget(self.txt_workspace_project)
        header_layout.addLayout(project_block)
        header_layout.addStretch()
        hint = QLabel(tr("Configure o projeto e carregue uma série de chuva."))
        hint.setObjectName("workspaceHint")
        header_layout.addWidget(hint)
        btn_simulate = QPushButton(tr("▷  Simular"))
        btn_simulate.setObjectName("workspaceSimulate")
        btn_simulate.clicked.connect(lambda: self.on_step_changed(3))
        header_layout.addWidget(btn_simulate)
        workspace_layout.addWidget(workspace_header)

        # 3. QStackedWidget com as 11 Etapas
        self.stack = QStackedWidget(self)

        self.tab_project = TabProject(self)
        self.tab_building = TabBuilding(self)
        self.tab_water_quality = TabWaterQuality(self)
        self.tab_tanks_simulation = TabTanksSimulation(self)
        self.tab_charts = TabChartsNetuno(self)
        self.tab_economic = TabEconomicIntegrated(self)
        self.tab_environmental = TabEnvironmental(self)
        from netuno.ui.tab_economic_global_optimizer import TabEconomicGlobalOptimizer
        self.tab_global_optimizer = TabEconomicGlobalOptimizer(self)
        self.tab_reports = TabReportsPdf(self)
        self.tab_export = TabExport(self)
        self.tab_documentation = TabDocumentation(self)
        self.tab_tariffs_manager = TabTariffsManager(self)

        # 12 Etapas em 3 Blocos (Dados de Entrada -> Resultados -> Ferramentas)
        self.stack.addWidget(self.tab_project)           # 0. Projeto e Chuva (Input)
        self.stack.addWidget(self.tab_building)          # 2. Edificação e Consumo (Input)
        self.stack.addWidget(self.tab_water_quality)     # 2. Qualidade & ETAP (Input)
        self.stack.addWidget(self.tab_tanks_simulation)  # 3. Reservatório & Custos (Input)
        self.stack.addWidget(self.tab_charts)            # 4. Resultados Técnicos (Output)
        self.stack.addWidget(self.tab_economic)          # 5. Resultados Econômicos (Output)
        self.stack.addWidget(self.tab_environmental)     # 6. Resultados Ambientais & ESG (Output)
        self.stack.addWidget(self.tab_global_optimizer)  # 7. Multi-Critério (MCDM) (Output)
        self.stack.addWidget(self.tab_reports)           # 8. Relatórios PDF (Output)
        self.stack.addWidget(self.tab_export)            # 9. Central de Exportação (Ferramentas - NOVA)
        self.stack.addWidget(self.tab_documentation)     # 10. Documentação (Ferramentas)
        self.stack.addWidget(self.tab_tariffs_manager)   # 11. Gestor de Tarifas (Ferramentas)

        workspace_layout.addWidget(self.stack, stretch=1)
        main_layout.addWidget(workspace, stretch=1)
        self.setCentralWidget(central_widget)

        # Conecta eventos para sincronizar o status da Sidebar
        self.tab_project.project_updated.connect(self.sync_project_state)
        self.tab_building.building_updated.connect(self.sync_project_state)
        self.tab_water_quality.water_quality_updated.connect(self.sync_project_state)
        self.tab_tanks_simulation.simulation_completed.connect(self.on_sim_completed)
        self.tab_economic.economic_calculated.connect(self._refresh_sidebar_summary)
        self.tab_environmental.environmental_updated.connect(self._refresh_sidebar_summary)
        self.tab_global_optimizer.optimization_updated.connect(self._refresh_sidebar_summary)
        self.tab_tariffs_manager.tariffs_changed.connect(self.sync_project_state)

        self.sync_project_state()

    def on_step_changed(self, index: int):
        self.stack.setCurrentIndex(index)
        self.sidebar.set_active_step(index)
        if index == 2 and hasattr(self, 'tab_water_quality'):
            # Etapa 3: Qualidade & ETAP — atualiza diagnósticos
            self.tab_water_quality.recalculate_all()
        elif index == 4 and hasattr(self, 'tab_charts'):
            # Etapa 5: Resultados Tecnicos — atualiza KPIs e graficos ao entrar
            ts = self.tab_tanks_simulation
            try:
                threshold = float(ts.txt_delta_ideal.text().replace(',', '.'))
            except Exception:
                threshold = 1.0
            self.tab_charts.update_charts_data(
                sweep_result=getattr(ts, 'last_sweep_result', None),
                single_result=getattr(ts, 'last_single_result', None),
                delta_threshold=threshold,
            )
        elif index == 5 and hasattr(self, 'tab_economic'):
            # Etapa 6: Resultados Economicos
            is_tech_only = getattr(self.tab_tanks_simulation, "_is_technical_only", False)
            if not is_tech_only:
                self.tab_economic._sync_volume_selector()
                self.tab_economic._select_optimum_when_calculated = True
                self.tab_economic.calculate_economics()
            else:
                self.tab_economic.clear_economic_outputs()
        elif index == 6 and hasattr(self, 'tab_environmental'):
            is_tech_only = getattr(self.tab_tanks_simulation, "_is_technical_only", False)
            if not is_tech_only:
                self.tab_environmental.recalculate_and_update()
            else:
                self.tab_environmental.clear_results()
        elif index == 7 and hasattr(self, 'tab_global_optimizer'):
            is_tech_only = getattr(self.tab_tanks_simulation, "_is_technical_only", False)
            if not is_tech_only:
                self.tab_global_optimizer.recalculate_all()
            else:
                self.tab_global_optimizer.clear_results()
        elif index == 8 and hasattr(self, 'tab_reports'):
            self.tab_reports.update_report_preview()
        elif index == 9 and hasattr(self, 'tab_reports'):
            self.tab_reports.update_report_preview()

    def _on_project_name_changed(self, value: str):
        """Mantém o nome visível sincronizado com o contrato persistido."""
        clean = " ".join(value.split())
        self.config.project_name = clean or "Novo projeto Netuno"


    def sync_project_state(self):
        if self.tab_project.precip_data is not None:
            self.tab_tanks_simulation.set_precip_data(self.tab_project.precip_data)

        if hasattr(self, 'tab_water_quality'):
            self.tab_water_quality.recalculate_all()

        self._refresh_sidebar_summary()
        self.tab_tanks_simulation.on_param_changed()

    def _optimal_volumes(self):
        technical = economic = environmental = topsis = None
        is_tech_only = getattr(self.tab_tanks_simulation, "_is_technical_only", False)

        sweep = getattr(self.tab_tanks_simulation, "last_sweep_result", None)
        if sweep is not None:
            technical = getattr(sweep, "optimal_lower_tank_vol", None)

        if not is_tech_only:
            economic = getattr(self.tab_economic, "economic_optimum_volume", None)
            if economic is None:
                econ_results = getattr(self.tab_economic, "last_sweep_econ_results", {}) or {}
                if econ_results:
                    economic = max(econ_results.values(), key=lambda item: item.get("vpl", float("-inf"))).get("volume_l")

            env_sweep = getattr(self.tab_environmental, "_last_sweep_lca", None)
            if env_sweep is not None:
                environmental = getattr(env_sweep, "best_lifetime_co2_vol_liters", None)

            decision_result = (
                getattr(self.tab_global_optimizer, "last_mcdm_result", None)
                or getattr(self.tab_global_optimizer, "last_topsis_result", None)
            )
            if decision_result is not None and getattr(decision_result, "best_candidate", None) is not None:
                topsis = decision_result.best_candidate.lower_tank_vol

        return technical, economic, environmental, topsis

    def _refresh_sidebar_summary(self):

        rain_fn = self.tab_project.txt_file_path.text()
        b_cfg = self.tab_building.get_building_config()
        
        last_single = getattr(self.tab_tanks_simulation, 'last_single_result', None)
        last_sweep = getattr(self.tab_tanks_simulation, 'last_sweep_result', None)
        sel_mode = getattr(self.tab_tanks_simulation, 'selected_volume_mode', 'sweep')

        if sel_mode == "sweep" and last_sweep:
            mode_str = "Varredura completa (decisão no TOPSIS)"
        elif last_single:
            mode_str = "Volume Fixo Personalizado"
        else:
            mode_str = "Não simulado"

        technical, economic, environmental, topsis = self._optimal_volumes()

        self.sidebar.update_summary(
            rain_name=rain_fn,
            area=b_cfg["area"],
            residents=b_cfg["residents"],
            demand_per_capita=b_cfg["demand"],
            share=b_cfg["share"],
            mode_str=mode_str,
            technical_opt_vol=technical,
            economic_opt_vol=economic,
            environmental_opt_vol=environmental,
            topsis_opt_vol=topsis,
        )

    def on_sim_completed(self, single_res, sweep_res=None):
        is_tech_only = getattr(self.tab_tanks_simulation, "_is_technical_only", False)
        if single_res:
            self._refresh_sidebar_summary()
        # Atualiza Etapa 4 (Resultados Tecnicos: diagrama + KPIs + graficos)
        if sweep_res or single_res:
            threshold = 1.0
            try:
                threshold = float(self.tab_tanks_simulation.txt_delta_ideal.text().replace(',', '.'))
            except Exception:
                pass
            self.tab_charts.update_charts_data(
                sweep_result=sweep_res, single_result=single_res,
                delta_threshold=threshold,
            )
        if not is_tech_only:
            # Etapa 5: recalcula economico com novos dados hidricos e seleciona ótimo (menor payback)
            if hasattr(self, 'tab_economic') and hasattr(self.tab_economic, 'calculate_economics'):
                self.tab_economic._sync_volume_selector()
                self.tab_economic._select_optimum_when_calculated = True
                self.tab_economic.calculate_economics()
            if hasattr(self, 'tab_environmental') and hasattr(self.tab_environmental, 'recalculate_and_update'):
                self.tab_environmental.recalculate_and_update()
            # A Etapa 7 sempre deve refletir os pontos da última varredura
            if hasattr(self, 'tab_global_optimizer'):
                self.tab_global_optimizer.generate_neighborhood_scenarios()
        else:
            if hasattr(self, 'tab_economic'):
                self.tab_economic.clear_economic_outputs()
            if hasattr(self, 'tab_environmental'):
                self.tab_environmental.clear_results()
            if hasattr(self, 'tab_global_optimizer'):
                self.tab_global_optimizer.clear_results()

        if hasattr(self, 'tab_reports'):
            self.tab_reports.update_report_preview()

    def _collect_project_ui_state(self) -> dict:
        """Captura controles de interface que complementam o NetunoConfig.

        O arquivo .netuno permanece autocontido: o modelo numérico fica em
        ``inputs`` e os controles necessários para reabrir cada etapa ficam
        aqui. Isso evita depender do estado visual ou de arquivos externos.
        """
        state = {
            "project": self.tab_project.get_project_state(),
            "stage3": self.tab_tanks_simulation.get_project_state(),
        }
        optimizer = getattr(self, "tab_global_optimizer", None)
        if optimizer:
            state["topsis"] = {
                "preset": optimizer.combo_preset.currentIndex(),
                "technical_weight": optimizer.spin_w_tech.value(),
                "economic_weight": optimizer.spin_w_fin.value(),
                "environmental_weight": optimizer.spin_w_env.value(),
            }

        environmental = getattr(self, "tab_environmental", None)
        if environmental:
            env_state = {"text": {}, "combos": {}, "checks": {}}
            for name, widget in vars(environmental).items():
                if name.startswith("txt_") and hasattr(widget, "text"):
                    env_state["text"][name] = widget.text()
                elif name.startswith("combo_") and hasattr(widget, "currentIndex"):
                    env_state["combos"][name] = widget.currentIndex()
                elif name.startswith("chk_") and hasattr(widget, "isChecked"):
                    env_state["checks"][name] = widget.isChecked()
            env_state["params_customized"] = bool(getattr(environmental, "_params_customized", False))
            state["environmental"] = env_state
        return state

    def _apply_project_ui_state(self, state: dict, cfg) -> None:
        """Restaura de forma defensiva o estado salvo por _collect_project_ui_state."""
        state = state or {}
        project = state.get("project", {})
        self.tab_project.apply_project_state(project, cfg)

        self.tab_tanks_simulation.apply_project_state(state.get("stage3", {}), cfg)

        topsis_state = state.get("topsis", {})
        optimizer = getattr(self, "tab_global_optimizer", None)
        if optimizer and topsis_state:
            optimizer.combo_preset.setCurrentIndex(max(0, min(int(topsis_state.get("preset", 0)), optimizer.combo_preset.count() - 1)))
            optimizer.spin_w_tech.setValue(float(topsis_state.get("technical_weight", 33.3)))
            optimizer.spin_w_fin.setValue(float(topsis_state.get("economic_weight", 33.3)))
            optimizer.spin_w_env.setValue(float(topsis_state.get("environmental_weight", 33.4)))
            optimizer._update_weight_validation()

        environmental = getattr(self, "tab_environmental", None)
        env_state = state.get("environmental", {})
        if environmental and env_state:
            for name, index in env_state.get("combos", {}).items():
                widget = getattr(environmental, name, None)
                if widget and hasattr(widget, "setCurrentIndex"):
                    widget.setCurrentIndex(max(0, min(int(index), widget.count() - 1)))
            for name, value in env_state.get("text", {}).items():
                widget = getattr(environmental, name, None)
                if widget and hasattr(widget, "setText"):
                    widget.setText(str(value))
            for name, checked in env_state.get("checks", {}).items():
                widget = getattr(environmental, name, None)
                if widget and hasattr(widget, "setChecked"):
                    widget.setChecked(bool(checked))
            environmental._params_customized = bool(env_state.get("params_customized", True))

    def on_load_simulation(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("Carregar Projeto Netuno"),
            "",
            f"{tr('Todos os Projetos Aceitos')} (*.netuno *.json *.csv);;{tr('Projeto Netuno')} (*.netuno);;{tr('Projeto JSON')} (*.json);;{tr('Arquivos CSV')} (*.csv)"
        )
        if not file_path:
            return

        try:
            from netuno.core.parser import load_netuno_project
            proj = load_netuno_project(file_path)

            cfg = proj["config"]
            self.config = cfg
            self.txt_workspace_project.setText(getattr(cfg, "project_name", "Novo projeto Netuno"))

            if hasattr(self, 'tab_economic'):
                self.tab_economic._internal_config = cfg

            # 1. Carrega chuva
            if proj["precip_data"] is not None:
                self.tab_project.precip_data = proj["precip_data"]
                self.tab_project.precip_file_path = proj["precip_filename"]
                self.tab_project.txt_file_path.setText(proj["precip_filename"])
                self.tab_project.update_tables()

            # 1.1 Carrega localização tarifária
            if hasattr(self.tab_project, 'set_tariff_location'):
                uf = getattr(cfg, 'tariff_city_uf', 'SC')
                city = getattr(cfg, 'tariff_city_name', 'Florianópolis')
                self.tab_project.set_tariff_location(uf, city)

            # 2. Carrega Edificação
            b_data = proj.get("building_data", {})
            if b_data and hasattr(self.tab_building, 'set_building_config'):
                self.tab_building.set_building_config(b_data)

            # 3–6. Restaura os controles das etapas, inclusive a Etapa 3
            # (varredura, reservatórios, limiar, economia, ACV e TOPSIS).
            self._apply_project_ui_state(proj.get("ui_state", {}), cfg)

            # 5. Carrega Cenários no Otimizador Econômico Global
            if hasattr(self, 'tab_global_optimizer') and proj.get("global_scenarios"):
                self.tab_global_optimizer.scenarios = proj["global_scenarios"]
                self.tab_global_optimizer.refresh_table_rows()

            # 6. Sincroniza e simula se houver chuva
            self.sync_project_state()
            if proj["precip_data"] is not None and hasattr(self.tab_tanks_simulation, 'run_simulation'):
                self.tab_tanks_simulation.run_simulation(force=False)
            if hasattr(self, 'tab_global_optimizer') and getattr(self.tab_global_optimizer, 'scenarios', None):
                self.tab_global_optimizer.recalculate_all()

            QMessageBox.information(
                self,
                tr("Sucesso"),
                f"{tr('Projeto carregado com sucesso!')}\n"
                f"{tr('Arquivo')}: {os.path.basename(file_path)}"
            )
        except Exception as e:
            import traceback
            QMessageBox.critical(self, tr("Erro ao Carregar"), f"{tr('Falha ao carregar arquivo de projeto')}:\n{str(e)}\n\n{traceback.format_exc()}")

    def on_save_simulation(self):
        from netuno import get_project_filename
        project_name = " ".join(self.txt_workspace_project.text().split()) or tr("Novo projeto Netuno")
        self.config.project_name = project_name
        def_name = get_project_filename(project_name, self.config.project_id, "netuno")
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            tr("Salvar Projeto Completo"),
            def_name,
            f"{tr('Projeto Netuno')} (*.netuno);;{tr('Projeto JSON')} (*.json);;CSV legado — não preserva todas as etapas (*.csv)"
        )
        if not file_path:
            return

        try:
            from netuno.core.parser import NetunoConfig, export_netuno_json, export_netuno_csv, parse_float
            import os

            # Base config do componente econômico
            if hasattr(self, 'tab_economic'):
                cfg = self.tab_economic.get_netuno_config()
            else:
                cfg = NetunoConfig()
            cfg.project_id = getattr(self.config, 'project_id', 'N5-PROJ')
            cfg.created_at = getattr(self.config, 'created_at', '')
            cfg.project_name = project_name

            b_cfg = self.tab_building.get_building_config()
            cfg.area = b_cfg.get('area', 100.0)
            cfg.demand_value = b_cfg.get('demand', 200.0)
            cfg.residents_count = b_cfg.get('residents', 3)
            cfg.rainwater_share = b_cfg.get('share', 0.4)
            cfg.runoff_coeff = b_cfg.get('runoff', COEFICIENTE_DE_ESCOAMENTO_PADRAO)
            cfg.demand_monthly = b_cfg.get('monthly_demands') or []
            cfg.residents_monthly = b_cfg.get('monthly_residents') or []
            # O modo de demanda e as listas de calendario vinham da tela e
            # paravam aqui: sem estas sete linhas o arquivo gravava sempre
            # "constant", e as duas listas mensais acima eram ignoradas na
            # releitura por causa do modo.
            cfg.demand_mode = b_cfg.get('demand_mode') or 'constant'
            cfg.weekly_demands = b_cfg.get('weekly_demands') or []
            cfg.weekly_residents = b_cfg.get('weekly_residents') or []
            cfg.weekly_shares = b_cfg.get('weekly_shares') or []
            cfg.monthly_shares = b_cfg.get('monthly_shares') or []
            cfg.daily_demands = b_cfg.get('daily_demands') or []
            cfg.daily_residents = b_cfg.get('daily_residents') or []
            cfg.daily_shares = b_cfg.get('daily_shares') or []

            if hasattr(self, 'tab_project'):
                cfg.discard_mode = self.tab_project.get_discard_mode()
                cfg.discard_days_interval = self.tab_project.get_discard_days()
                cfg.discard = parse_float(self.tab_project.txt_discard.text(), cfg.discard)
                cfg.start_date = self.tab_project.txt_start_date.text().strip() or cfg.start_date
                if self.tab_project.precip_file_path:
                    cfg.precip_file = os.path.basename(self.tab_project.precip_file_path)
                if hasattr(self.tab_project, 'get_tariff_location'):
                    t_uf, t_city = self.tab_project.get_tariff_location()
                    cfg.tariff_city_uf = t_uf
                    cfg.tariff_city_name = t_city
                    cfg.elec_city_uf = t_uf
                    cfg.elec_city_name = t_city

            if hasattr(self, 'tab_tanks_simulation'):
                ts = self.tab_tanks_simulation
                cfg.lower_tank_max = parse_float(ts.txt_sweep_max.text(), cfg.lower_tank_max)
                cfg.lower_tank_step = parse_float(ts.txt_sweep_step.text(), cfg.lower_tank_step)
                cfg.lower_tank_mode = 1
                cfg.delta_ideal = parse_float(ts.txt_delta_ideal.text(), cfg.delta_ideal)
                cfg.upper_tank_used = 1 if ts.combo_upper_mode.currentIndex() != 2 else 0
                ts.write_supply_to_config(cfg)
                cfg.upper_tank_vol = parse_float(ts.txt_upper_vol.text(), cfg.upper_tank_vol)
                pump_pct = parse_float(ts.txt_pump_thresh_pct.text(), 10.0)
                cfg.pumping_threshold = cfg.upper_tank_vol * pump_pct / 100.0 if cfg.upper_tank_used else 0.0

            self.config = cfg

            global_scenarios = getattr(self.tab_global_optimizer, 'scenarios', [])
            is_en = get_current_lang() == "en"

            if file_path.lower().endswith('.csv'):
                QMessageBox.warning(
                    self,
                    "Legacy format" if is_en else "Formato legado",
                    "CSV is retained only for compatibility and does not preserve every control, LCA input or TOPSIS weight. Use .netuno to save a complete self-contained project."
                    if is_en else
                    "CSV é mantido somente para compatibilidade e não preserva todos os controles, a ACV ou os pesos TOPSIS. Para salvar um projeto completo e autocontido, use o formato .netuno.",
                )
                sweep_res = getattr(self.tab_tanks_simulation, 'last_sweep_result', None)
                results = sweep_res.results_by_volume if (sweep_res and sweep_res.results_by_volume) else []
                export_netuno_csv(cfg, results, file_path, precip_data=self.tab_project.precip_data)
            else:
                export_netuno_json(
                    config=cfg,
                    file_path=file_path,
                    precip_data=self.tab_project.precip_data,
                    building_data=b_cfg,
                    global_scenarios=global_scenarios,
                    ui_state=self._collect_project_ui_state(),
                )

            QMessageBox.information(
                self,
                tr("Sucesso"),
                f"{tr('Projeto salvo com sucesso (incluindo chuva, edificação, custos e otimizador) em:')}\n{file_path}\n\n"
                + (".netuno/.json files include the daily rainfall series in the project itself and can be reopened without the original CSV."
                   if is_en else
                   "Arquivos .netuno/.json incluem a série diária de chuva no próprio projeto e podem ser reabertos sem o CSV original.")
            )
        except Exception as e:
            import traceback
            QMessageBox.critical(self, tr("Erro ao Salvar"), f"{tr('Falha ao salvar projeto')}:\n{str(e)}\n\n{traceback.format_exc()}")

    def on_show_manual(self):
        # O menu mostrava só autores e versão; agora abre o PDF do manual, que
        # acompanha o programa, e só cai na mensagem quando ele não existe.
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        for relativo in (os.path.join("manual", "Manual-Netuno-5.pdf"),):
            caminho = get_resource_path(relativo)
            if os.path.isfile(caminho):
                QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))
                return
        QMessageBox.information(
            self,
            tr(f"Manual do Usuário — Netuno {__version__}"),
            f"{APP_VERSION_LABEL} — {tr('Manual do Usuário')}\n"
            f"{tr('Autores')}: Eng. Igor Catão Martins Vaz & Prof. Enedir Ghisi, PhD\n"
            f"{tr('Grupo de Pesquisa Gestão do Espaço Sustentável')} (UFSC)"
        )

    def on_show_citation(self):
        citation = (
            f"VAZ, I. C. M.; GHISI, E. <b>Netuno {__version__}</b>: "
            f"{tr('Programa computacional para simulação de aproveitamento de água de chuva em edificações')}. "
            f"Florianópolis: Universidade Federal de Santa Catarina, {tr('Grupo de Pesquisa Gestão do Espaço Sustentável')}, 2026. "
            f"Software de computador, versão {__version__}."
        )
        bibtex = (
            f"@software{{netuno_{__version__.replace('.', '_')},<br>"
            f"&nbsp;&nbsp;author = {{Vaz, Igor Catão Martins and Ghisi, Enedir}},<br>"
            f"&nbsp;&nbsp;title = {{Netuno {__version__}: Programa computacional para simulação de aproveitamento de água de chuva em edificações}},<br>"
            f"&nbsp;&nbsp;year = {{2026}},<br>"
            f"&nbsp;&nbsp;publisher = {{Universidade Federal de Santa Catarina (UFSC)}},<br>"
            f"&nbsp;&nbsp;address = {{Florianópolis, Brasil}},<br>"
            f"&nbsp;&nbsp;version = {{{__version__}}}<br>}}"
        )
        QMessageBox.information(
            self,
            tr("Como Citar o Netuno"),
            f"<p><b>{tr('Referência recomendada (ABNT NBR 6023)')}</b></p><p>{citation}</p>"
            f"<p><b>BibTeX</b></p><p><tt>{bibtex}</tt></p>"
        )

    def on_show_validation_report(self):
        from netuno.ui.dialogs import DialogValidationReport
        dlg = DialogValidationReport(self)
        dlg.exec()

    def on_show_about(self):
        QMessageBox.information(
            self,
            tr(f"Sobre o Netuno {__version__}"),
            f"<b>{APP_VERSION_LABEL}</b><br><br>"
            f"{tr('Plataforma para Aproveitamento de Água de Chuva em Edificações.')}<br>"
            f"<b>{tr('Autores')}:</b> Eng. Igor Catão Martins Vaz &amp; Prof. Enedir Ghisi, PhD<br>"
            f"{tr('Desenvolvido no Grupo de Pesquisa Gestão do Espaço Sustentável (UFSC).')}<br><br>"
            f"<i>{tr('Versão científica e operacional com modelagem diária YAS, análise de ciclo de vida (ACV), tomada de decisão multicritério (TOPSIS/SMAA-VIKOR) e catálogo tarifário nacional.')}</i>"
        )

    def on_download_excel_sample(self):
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("Simulação de Cenários em Lote"))
        msg.setIcon(QMessageBox.Information)
        msg.setText(tr("<b>O que é a Simulação de Cenários em Lote?</b>"))
        msg.setInformativeText(
            tr(
                "<p>Esta funcionalidade permite simular dezenas ou centenas de combinações de projetos "
                "de água de chuva (variando área de captação, demanda, volume de cisterna, custos e coeficientes de escoamento) "
                "de forma automatizada a partir de uma planilha Excel (<code>.xlsx</code>).</p>"
                "<p>💡 <b>Para matrizes muito grandes:</b><br>"
                "Estudos com milhares de cenários e séries longas são executados pela interface de "
                "automação que acompanha a distribuição de código-fonte, usada nos trabalhos do "
                "Grupo de Pesquisa Gestão do Espaço Sustentável. Para um estudo de projeto, a planilha "
                "de cenários desta tela responde a mesma pergunta.</p>"
                "<p>Deseja salvar a planilha modelo de cenários (<code>.xlsx</code>) para preenchimento agora?</p>"
            )
        )
        btn_download = msg.addButton(tr("📥 Baixar Planilha Modelo (.xlsx)"), QMessageBox.AcceptRole)
        btn_cancel = msg.addButton(tr("Cancelar"), QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() != btn_download:
            return

        def_name = self.get_kebab_filename("netuno-modelo-cenarios", "xlsx")
        file_path, _ = QFileDialog.getSaveFileName(self, tr("Salvar Modelo Excel de Cenários"), def_name, "Planilha Excel (*.xlsx)")
        if file_path:
            from netuno.core.excel_scenarios import generate_sample_scenario_excel
            generate_sample_scenario_excel(file_path)
            QMessageBox.information(
                self,
                tr("Modelo Criado"),
                tr(
                    f"Planilha modelo de cenários salva com sucesso em:\n{file_path}\n\n"
                    "Preencha as linhas com os parâmetros desejados e depois utilize a opção:\n"
                    "'Cenários & Ferramentas > Importar e Simular Cenários em Lote'."
                )
            )

    def generate_batch_template(self):
        return self.on_download_excel_sample()

    def on_import_excel_scenarios(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo de Cenários Excel", "", "Planilhas (*.xlsx *.xls *.csv)")
        if file_path:
            from netuno.core.excel_scenarios import parse_excel_scenarios, run_parsed_scenarios, export_scenarios_to_excel_bytes
            try:
                scenarios = parse_excel_scenarios(file_path)
                if not scenarios:
                    QMessageBox.warning(self, "Aviso", "Nenhum cenário válido encontrado na planilha.")
                    return
                avisos = [a for sc in scenarios for a in sc.get("avisos", [])]
                if avisos and QMessageBox.question(
                        self, "Confira a substituição pluvial",
                        "A coluna de substituição está em percentual (40 = 40%).\n\n"
                        + "\n".join(avisos) + "\n\nSimular mesmo assim?") != QMessageBox.Yes:
                    return
                results = run_parsed_scenarios(scenarios)
                def_out = self.get_kebab_filename("netuno-resultados-cenarios", "xlsx")
                out_path, _ = QFileDialog.getSaveFileName(self, "Salvar Resultados dos Cenários", def_out, "Planilha Excel (*.xlsx)")
                if out_path:
                    excel_bytes = export_scenarios_to_excel_bytes(results)
                    with open(out_path, "wb") as f:
                        f.write(excel_bytes)
                    QMessageBox.information(self, "Simulação Concluída", f"Simulação de {len(scenarios)} cenários realizada com sucesso!\nResultados salvos em:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erro na Simulação", f"Erro ao processar arquivo:\n{str(e)}")
