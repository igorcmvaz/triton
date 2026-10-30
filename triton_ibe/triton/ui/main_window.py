"""
Janela Principal da Aplicação Triton.
Interface moderna com navegação por Sidebar em 6 Etapas, Live Preview e Sem Pop-ups.
"""

import os
from triton.core.numero import para_float
from triton.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QApplication,
)
from PySide6.QtCore import QObject, QEvent, Signal
from PySide6.QtGui import QAction, QActionGroup, QIcon

from triton.ui.theme import NETUNO4_CLASSIC_QSS
from triton import APP_TITLE, APP_VERSION_LABEL, __version__
from triton.ui.sidebar import Sidebar
from triton.core.parser import TritonConfig
from triton.ui.translation import tr, get_current_lang, get_available_languages, get_resource_path, restart_app
from triton.ui.textos_da_edicao import nome_sugerido

from triton.ui.tab_project import TabProject
from triton.ui.tab_building import TabBuilding
from triton.ui.tab_water_quality import TabWaterQuality
from triton.ui.tab_tanks_simulation import TabTanksSimulation
from triton.ui.tab_charts_triton import TabChartsTriton
from triton.ui.tab_economic_integrated import TabEconomicIntegrated
from triton.ui.tab_environmental import TabEnvironmental
from triton.ui.tab_reports_pdf import TabReportsPdf
from triton.ui.tab_export import TabExport
from triton.ui.tab_documentation import TabDocumentation
from triton.ui.tab_tariffs_manager import TabTariffsManager

class _PaginaSemGestor(QWidget):
    """Lugar do Gestor de Tarifas fora da Edição Brasil.

    O Gestor é o catálogo das 652 cidades brasileiras: nas outras edições nem é construído
    (não há banco para ler) e a barra lateral e o menu não têm acesso a ele. A página existe
    para que os índices das etapas continuem os mesmos nas três edições.
    """

    tariffs_changed = Signal()


class _MoedaNosDialogos(QObject):
    """Fora da Edição Brasil, os diálogos abertos pela janela mostram a moeda do projeto.

    Os rótulos fixos dos diálogos («Imposto fixo (R$/mês):», cabeçalhos do fluxo de caixa)
    estão em reais no catálogo; ao aparecer, cada diálogo da janela passa por
    `aplicar_moeda`, como as etapas.
    """

    def __init__(self, janela):
        super().__init__(janela)
        self._janela = janela

    def eventFilter(self, obj, event):
        try:
            if (event.type() == QEvent.Show and isinstance(obj, QDialog)
                    and obj.parentWidget() is not None and obj.parentWidget().window() is self._janela):
                self._janela._aplicar_moeda(obj)
        except RuntimeError:
            pass  # janela já destruída
        return False


class MainWindow(QMainWindow):
    @property
    def bim_layout(self) -> dict:
        """Componentes posicionados, trechos na ordem do projetista e volumetria.

        Vive na configuração do projeto, e não na janela: é assim que o CAPEX, a
        ACV e a linha de comando leem o mesmo arranjo que a Planta 3D mostra.
        """
        if not self.config.bim_layout:
            self.config.bim_layout = {"bim_components": [], "pipe_runs": [], "building_volume": {}}
        return self.config.bim_layout

    @bim_layout.setter
    def bim_layout(self, valor: dict) -> None:
        self.config.bim_layout = dict(valor or {})

    def __init__(self):
        # Antes de criar a janela: ela e as abas (spin boxes, validadores) herdam o QLocale padrão ao nascer.
        from triton.core.numero import aplicar_locale
        aplicar_locale()
        super().__init__()
        from triton import get_kebab_filename
        self.get_kebab_filename = get_kebab_filename
        self.setWindowTitle(tr(APP_TITLE))
        from triton.core.edition import usa_dados_de_portugal as _pt_ed, get_edition_title as _titulo
        if _pt_ed():
            # Edição IBE: o título leva a linha de cobertura lida do banco de chuva.
            self.setWindowTitle(_titulo())
        self.resize(1280, 760)
        self.setMinimumSize(900, 600)
        # Projeto novo da edição: na Brasil, os padrões históricos (tubulação e acessórios do arranjo
        # 3D, mão de obra automática, tarifas de Florianópolis); na Internacional, nada de preço,
        # tarifa nem localidade; na Portugal, o tarifário de Lisboa. A fábrica é do núcleo
        # (``projeto_novo_da_edicao``), a mesma da linha de comando.
        from triton.core.edition import usa_dados_do_brasil, projeto_novo_da_edicao
        self.config = projeto_novo_da_edicao()
        if not usa_dados_do_brasil() and self.config.project_name == "Novo projeto Triton":
            self.config.project_name = tr("Novo projeto Triton")
        
        # Ícone da janela principal
        for icone_rel in (
            os.path.join("icons", "triton.ico"),
            os.path.join("icons", "icon.ico"),
            os.path.join("icons", "triton_brl.png"),
            os.path.join("icons", "triton_int.png"),
            os.path.join("icons", "triton_ibe.png"),
            os.path.join("icons", "triton.png"),
            os.path.join("icons", "icon.png"),
            os.path.join("icons", "Triton2.png"),
        ):
            logo_path = get_resource_path(icone_rel)
            if os.path.isfile(logo_path):
                self.setWindowIcon(QIcon(logo_path))
                break

        self.setStyleSheet(NETUNO4_CLASSIC_QSS)

        self.init_menu_bar()
        self.init_ui()

        # Fora da Edição Brasil, os textos fixos em reais passam à moeda do projeto.
        if not usa_dados_do_brasil():
            ts = self.tab_tanks_simulation
            ts.combo_currency.setProperty("moeda_fixa", True)
            # A documentação cita valores brasileiros como exemplo, e o Gestor de Tarifas é
            # só da Brasil; relatórios e exportações formatam a moeda por conta própria.
            for aba in (self.tab_documentation, self.tab_tariffs_manager, self.tab_reports, self.tab_export):
                aba.setProperty("moeda_fixa", True)
            ts.combo_currency.currentIndexChanged.connect(lambda *_: self._aplicar_moeda())
            if QApplication.instance() is not None:
                QApplication.instance().installEventFilter(_MoedaNosDialogos(self))
            self._aplicar_moeda()
            # a Modulação Probabilística escreve as dicas na moeda do projeto ao ser exibida;
            # antes disso o catálogo falaria em reais
            self.tab_modulacao_estocastica.atualizar_moeda()

    def _aplicar_moeda(self, raiz=None):
        """Troca «R$» pelo símbolo da moeda do projeto nos textos fixos (moeda_na_interface)."""
        from triton.core.edition import usa_dados_do_brasil
        if usa_dados_do_brasil() or not hasattr(self, "tab_tanks_simulation"):
            return
        from triton.ui.moeda_na_interface import aplicar_moeda
        ts = self.tab_tanks_simulation
        aplicar_moeda(raiz if raiz is not None else self, ts.get_currency_symbol(), ts.get_currency_code())

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        # Menu Arquivo
        menu_file = menu_bar.addMenu(tr("Arquivo"))
        
        action_new = QAction(tr("Novo Projeto"), self)
        action_new.triggered.connect(lambda *_: self.on_new_project())
        menu_file.addAction(action_new)

        action_open = QAction(tr("Carregar Projeto CSV"), self)
        action_open.triggered.connect(self.on_load_simulation)
        menu_file.addAction(action_open)

        action_save = QAction(tr("Salvar Projeto"), self)
        action_save.triggered.connect(self.on_save_simulation)
        menu_file.addAction(action_save)

        menu_file.addSeparator()

        action_exit = QAction(tr("Sair"), self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        # Área de execução e cenários: uma seção própria torna as ações de
        # projeto e as ações de análise claramente distintas.
        menu_sim = menu_bar.addMenu(tr("Cenários && Ferramentas"))

        action_excel_sample = QAction(tr("Baixar Planilha Modelo Excel (.xlsx)"), self)
        action_excel_sample.triggered.connect(self.on_download_excel_sample)
        menu_sim.addAction(action_excel_sample)

        action_excel_import = QAction(tr("Importar e Simular Cenários em Lote (Excel)"), self)
        action_excel_import.triggered.connect(self.on_import_excel_scenarios)
        menu_sim.addAction(action_excel_import)

        action_export_tab = QAction(tr("Central de Exportação (Planilhas, CAD e Projeto)"), self)
        action_export_tab.triggered.connect(lambda: self.on_step_changed(9))
        menu_sim.addAction(action_export_tab)

        menu_sim.addSeparator()
        action_tariffs_mgr = QAction(tr("Gestor Nacional de Tarifas & Auditoria (652 Cidades)"), self)
        action_tariffs_mgr.triggered.connect(lambda: self.on_step_changed(11))
        # O Gestor de Tarifas é o catálogo brasileiro: fora da Brasil, nem na barra lateral
        # nem no menu.
        from triton.core.edition import usa_dados_do_brasil
        if usa_dados_do_brasil():
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
        action_manual = QAction(tr(f"Manual do Usuário — Triton {__version__}"), self)
        action_manual.triggered.connect(self.on_show_manual)
        menu_ajuda.addAction(action_manual)

        action_citacao = QAction(tr("Como Citar o Triton"), self)
        action_citacao.triggered.connect(self.on_show_citation)
        menu_ajuda.addAction(action_citacao)

        action_val_report = QAction(tr("Relatório de Verificação"), self)
        action_val_report.triggered.connect(self.on_show_validation_report)
        menu_ajuda.addAction(action_val_report)

        action_doc = QAction(tr("Documentação"), self)
        action_doc.triggered.connect(lambda: self.on_step_changed(10))
        menu_ajuda.addAction(action_doc)

        action_about = QAction(tr("Sobre o Triton"), self)
        action_about.triggered.connect(self.on_show_about)
        menu_ajuda.addAction(action_about)

    def set_language(self, lang):
        from triton.ui.translation import set_current_lang
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


    def _criar_linha_de_cobertura(self):
        """A linha «Cobertura: ...» da tela inicial da edição IBE, lida do banco; None nas outras edições."""
        from triton.core.edition import usa_dados_de_portugal
        if not usa_dados_de_portugal():
            return None
        from triton.core import qualidade_chuva as _q
        if not _q.tem_qualidade():
            return None
        _l = get_current_lang()
        lingua = _l if _l in ("pt", "es", "zh") else "en"
        rotulo = QLabel(_q.linha_de_cobertura(lingua))
        rotulo.setObjectName("linhaDeCobertura")
        rotulo.setWordWrap(True)
        rotulo.setToolTip(chr(10).join(_q.descricao_dos_niveis(lingua)))
        rotulo.setStyleSheet("font-size: 11px; font-weight: 600; color: #475569; padding: 4px 30px; "
                             "background-color: #f1f5f9; border-bottom: 1px solid #e2e8f0;")
        return rotulo

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
        self.txt_workspace_project = QLineEdit(getattr(self.config, "project_name", tr("Novo projeto Triton")))
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
        self.lbl_cobertura = self._criar_linha_de_cobertura()
        if self.lbl_cobertura is not None:
            workspace_layout.addWidget(self.lbl_cobertura)

        # 3. QStackedWidget com as 11 Etapas
        self.stack = QStackedWidget(self)

        self.tab_project = TabProject(self)
        self.tab_building = TabBuilding(self)
        self.tab_water_quality = TabWaterQuality(self)
        self.tab_tanks_simulation = TabTanksSimulation(self)
        self.tab_charts = TabChartsTriton(self)
        self.tab_economic = TabEconomicIntegrated(self)
        self.tab_environmental = TabEnvironmental(self)
        from triton.ui.tab_economic_global_optimizer import TabEconomicGlobalOptimizer
        self.tab_global_optimizer = TabEconomicGlobalOptimizer(self)
        self.tab_reports = TabReportsPdf(self)
        self.tab_export = TabExport(self)
        self.tab_documentation = TabDocumentation(self)
        from triton.core.edition import usa_dados_do_brasil as _brasil
        self.tab_tariffs_manager = TabTariffsManager(self) if _brasil() else _PaginaSemGestor(self)
        from triton.ui.tab_modulacao_estocastica import TabModulacaoEstocastica
        self.tab_modulacao_estocastica = TabModulacaoEstocastica(self)

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
        self.stack.addWidget(self.tab_modulacao_estocastica)  # 12. Modulação Probabilística (Ferramentas)

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
                threshold = para_float(ts.txt_delta_ideal.text())
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
        self._aplicar_moeda(self.stack.widget(index))

    def _on_project_name_changed(self, value: str):
        """Mantém o nome visível sincronizado com o contrato persistido."""
        clean = " ".join(value.split())
        self.config.project_name = clean or tr("Novo projeto Triton")


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
                threshold = para_float(self.tab_tanks_simulation.txt_delta_ideal.text())
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
        """Captura controles de interface que complementam o TritonConfig.

        O arquivo .triton permanece autocontido: o modelo numérico fica em
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
        modulacao = getattr(self, "tab_modulacao_estocastica", None)
        if modulacao:
            state["modulacao_estocastica"] = modulacao.get_project_state()
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

        modulacao = getattr(self, "tab_modulacao_estocastica", None)
        if modulacao and state.get("modulacao_estocastica"):
            modulacao.apply_project_state(state["modulacao_estocastica"])

    def on_new_project(self, confirmar: bool = True):
        """Arquivo > Novo Projeto: troca esta janela por uma nova, com os padrões da edição.

        Reiniciar etapa por etapa deixava resquícios (séries, tarifas, escolhas de diálogo) e
        divergia do que o programa mostra ao abrir. Uma janela nova passa pelo mesmo caminho da
        abertura: na Brasil, o projeto de Florianópolis; na Internacional, sem preços, tarifas
        nem localidade; na Portugal, o tarifário de Lisboa. O idioma e o tamanho da janela ficam.

        Devolve a janela nova, ou ``None`` se o usuário desistiu.
        """
        if confirmar:
            resposta = QMessageBox.question(
                self, tr("Novo Projeto"),
                tr("Descartar o projeto atual e começar um novo? As alterações não salvas serão perdidas."),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta != QMessageBox.Yes:
                return None
        nova = MainWindow()
        nova.resize(self.size())
        if self.isMaximized():
            nova.showMaximized()
        else:
            nova.move(self.pos())
            nova.show()
        app = QApplication.instance()
        if app is not None:
            # a referência impede que a janela nova seja coletada enquanto o programa roda
            app._triton_janela_atual = nova
        self.close()
        return nova

    def on_load_simulation(self, file_path=None):
        # Recebe o caminho quando o programa é aberto por um arquivo .triton
        # (associação criada pelo instalador); o menu passa um bool, e então
        # o diálogo de abertura é mostrado.
        if not isinstance(file_path, str) or not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                tr("Carregar Projeto Triton"),
                "",
                f"{tr('Todos os Projetos Aceitos')} (*.triton *.json *.csv);;{tr('Projeto Triton')} (*.triton);;{tr('Projeto JSON')} (*.json);;{tr('Arquivos CSV')} (*.csv)"
            )
        if not file_path:
            return

        try:
            from triton.core.parser import load_triton_project
            proj = load_triton_project(file_path)
            cfg = proj["config"]
            cfg.bim_layout = proj.get("bim_layout") or {"bim_components": [], "pipe_runs": [], "building_volume": {}}
            self.config = cfg
            self.txt_workspace_project.setText(getattr(cfg, "project_name", "Novo projeto Triton"))
            # O cursor volta ao início: com o texto longo, o campo mostrava só o fim do nome.
            self.txt_workspace_project.setCursorPosition(0)

            if hasattr(self, 'tab_economic'):
                self.tab_economic._internal_config = cfg

            # 1. Carrega chuva
            if proj.get("chuva_da_climbra"):
                # Série recomposta da base CLIMBra pela referência gravada no arquivo.
                self.tab_project.btn_group_source.blockSignals(True)
                self.tab_project.rb_source_national.setChecked(True)
                self.tab_project.btn_group_source.blockSignals(False)
                self.tab_project.precip_data = proj["precip_data"]
                self.tab_project.panel_custom.hide()
                self.tab_project.panel_national.show()
                self.tab_project.update_tables()
            elif proj["precip_data"] is not None:
                self.tab_project.btn_group_source.blockSignals(True)
                self.tab_project.rb_source_custom.setChecked(True)
                self.tab_project.btn_group_source.blockSignals(False)
                self.tab_project.precip_data = proj["precip_data"]
                self.tab_project.precip_file_path = proj["precip_filename"]
                self.tab_project.txt_file_path.setText(proj["precip_filename"])
                self.tab_project.panel_national.hide()
                self.tab_project.panel_custom.show()
                self.tab_project.update_tables()
            if proj.get("aviso_chuva"):
                QMessageBox.warning(self, tr("Série de chuva"), proj["aviso_chuva"])

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
            # A Modulação Probabilística sem estado gravado parte da triagem deste projeto,
            # e não da do projeto aberto antes (ou da tela vazia do início).
            modulacao = getattr(self, "tab_modulacao_estocastica", None)
            if modulacao and not (proj.get("ui_state") or {}).get("modulacao_estocastica"):
                modulacao.restaurar_padroes()
            if proj["precip_data"] is not None and hasattr(self.tab_tanks_simulation, 'run_simulation'):
                self.tab_tanks_simulation.run_simulation(force=False)
            if hasattr(self, 'tab_global_optimizer') and getattr(self.tab_global_optimizer, 'scenarios', None):
                self.tab_global_optimizer.recalculate_all()
            self._aplicar_moeda()

            QMessageBox.information(
                self,
                tr("Sucesso"),
                f"{tr('Projeto carregado com sucesso!')}\n"
                f"{tr('Arquivo')}: {os.path.basename(file_path)}"
            )
        except Exception as e:
            import traceback
            QMessageBox.critical(self, tr("Erro ao Carregar"), f"{tr('Falha ao carregar arquivo de projeto')}:\n{str(e)}\n\n{traceback.format_exc()}")

    def config_do_estudo(self, project_name=None):
        """O projeto como a tela o mostra: a mesma configuração que o arquivo grava.

        Usado ao salvar e pela Modulação Probabilística, que refaz este estudo com as
        premissas de consumo sorteadas.
        """
        from triton.core.parser import TritonConfig, parse_float
        import os
        if project_name is None:
            project_name = " ".join(self.txt_workspace_project.text().split()) or tr("Novo projeto Triton")
        # Base config do componente econômico
        if hasattr(self, 'tab_economic'):
            cfg = self.tab_economic.get_triton_config()
        else:
            cfg = TritonConfig()
        cfg.project_id = getattr(self.config, 'project_id', 'N5-PROJ')
        cfg.created_at = getattr(self.config, 'created_at', '')
        cfg.project_name = project_name
        # A procedência da chuva E-OBS (pacote, SHA-256 e histórico de mudanças) segue com o estudo.
        procedencia = getattr(self.config, 'chuva_procedencia', None)
        if procedencia:
            cfg.chuva_procedencia = procedencia

        b_cfg = self.tab_building.get_building_config()
        cfg.area = b_cfg.get('area', 100.0)
        cfg.demand_value = b_cfg.get('demand', 200.0)
        cfg.residents_count = b_cfg.get('residents', 3)
        cfg.rainwater_share = b_cfg.get('share', 0.4)
        # A fração interna e a demanda externa são as que a tela simula; sem
        # copiá-las, o arquivo gravava os valores padrão (0,35 e 50 L/dia) e
        # discordava da fração total. Ver triton/core/fracao_atendivel.py.
        cfg.non_potable_indoor_share = b_cfg.get('non_potable_indoor_share', cfg.rainwater_share)
        cfg.potable_indoor_share = 1.0 - cfg.non_potable_indoor_share
        cfg.irrigation_liters_per_day = b_cfg.get('irrigation_liters_per_day', 0.0)
        cfg.irrigation_rain_threshold_mm = b_cfg.get('irrigation_rain_threshold_mm', 2.0)
        cfg.irrigation_potable_backup = b_cfg.get('irrigation_potable_backup', True)
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
            # A fonte da chuva escolhida na Etapa 1 (base CLIMBra ou arquivo próprio), com a
            # cidade, o modelo, o cenário e o recorte. Sem estas linhas, o projeto guardava a
            # fonte da última gravação: a Modulação Probabilística não liberava os modelos
            # climáticos, e a linha de comando lia do arquivo a fonte errada.
            if hasattr(self.tab_project, 'get_project_state'):
                chuva = self.tab_project.get_project_state()
                cfg.climate_source_mode = chuva.get("source_mode") or cfg.climate_source_mode
                from triton.core.edition import usa_dados_do_brasil as _brasil
                if _brasil() or chuva.get("source_mode") == "national_db":
                    cfg.climate_city_uf = chuva.get("climate_uf") or cfg.climate_city_uf
                    cfg.climate_city_name = chuva.get("climate_city") or cfg.climate_city_name
                    cfg.climate_model = chuva.get("climate_model") or cfg.climate_model
                    cfg.climate_scenario = chuva.get("climate_scenario") or cfg.climate_scenario
                else:
                    # série de arquivo fora da Brasil: sem cidade, modelo nem cenário da CLIMBra
                    # (voltavam ao padrão do TritonConfig, INM-CM4/HIST)
                    # (os combos da Etapa 1 são os da CLIMBra, escondidos: valem os descritores do projeto aberto,
                    # como «ERA5 (Open-Meteo)», que os laudos e o crédito da série leem)
                    previo = getattr(self, "config", None)
                    cfg.climate_city_uf = getattr(previo, "climate_city_uf", "") or ""
                    cfg.climate_city_name = getattr(previo, "climate_city_name", "") or ""
                    cfg.climate_model = getattr(previo, "climate_model", "") or ""
                    cfg.climate_scenario = getattr(previo, "climate_scenario", "") or ""
                cfg.climate_start_date = chuva.get("start_date") or cfg.climate_start_date
                cfg.climate_end_date = chuva.get("end_date") or cfg.climate_end_date
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
            # Volume escolhido à mão na tela = volume fixo do projeto; a linha
            # de comando o avalia sozinho, e a releitura o seleciona de novo.
            if getattr(ts, 'selected_volume_mode', 'sweep') == 'custom':
                cfg.lower_tank_mode = 0
                cfg.lower_tank_fixed = float(ts.custom_selected_vol)
            else:
                cfg.lower_tank_mode = 1
            cfg.delta_ideal = parse_float(ts.txt_delta_ideal.text(), cfg.delta_ideal)
            cfg.phi_operation_rule = ts._phi_escolhido()
            cfg.upper_tank_used = 1 if ts.combo_upper_mode.currentIndex() != 2 else 0
            ts.write_supply_to_config(cfg)
            cfg.upper_tank_vol = parse_float(ts.txt_upper_vol.text(), cfg.upper_tank_vol)
            pump_pct = parse_float(ts.txt_pump_thresh_pct.text(), 10.0)
            cfg.pumping_threshold = cfg.upper_tank_vol * pump_pct / 100.0 if cfg.upper_tank_used else 0.0

        if cfg is not self.config:
            cfg.bim_layout = self.config.bim_layout
            cfg.capex_do_arranjo = self.config.capex_do_arranjo
            cfg.mao_de_obra_automatica = self.config.mao_de_obra_automatica
        self.config = cfg
        return cfg

    def on_save_simulation(self):
        from triton import get_auditable_filename
        from triton.ui.textos_da_edicao import artefato_de_projeto
        project_name = " ".join(self.txt_workspace_project.text().split()) or tr("Novo projeto Triton")
        self.config.project_name = project_name
        def_name = get_auditable_filename(project_name, self.config.project_id, artefato_de_projeto(), "triton")
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            tr("Salvar Projeto Completo"),
            def_name,
            tr('{0} (*.triton);;{1} (*.json);;CSV legado — não preserva todas as etapas (*.csv)').format(tr('Projeto Triton'), tr('Projeto JSON'))
        )
        if not file_path:
            return

        try:
            from triton.core.parser import TritonConfig, export_triton_json, export_netuno_csv, parse_float
            import os

            cfg = self.config_do_estudo(project_name)
            b_cfg = self.tab_building.get_building_config()

            global_scenarios = getattr(self.tab_global_optimizer, 'scenarios', [])
            is_en = get_current_lang() == "en"

            if file_path.lower().endswith('.csv'):
                QMessageBox.warning(
                    self,
                    tr("Formato legado"),
                    tr("CSV é mantido somente para compatibilidade e não preserva todos os controles, a ACV ou os pesos TOPSIS. Para salvar um projeto completo e autocontido, use o formato .triton."),
                )
                from triton.core.dados_do_relatorio import resultados_para_csv_legado
                results = resultados_para_csv_legado(
                    getattr(self.tab_tanks_simulation, 'last_sweep_result', None),
                    getattr(self.tab_tanks_simulation, 'last_single_result', None))
                export_netuno_csv(cfg, results, file_path, precip_data=self.tab_project.precip_data)
            else:
                export_triton_json(
                    config=cfg,
                    file_path=file_path,
                    precip_data=self.tab_project.precip_data,
                    building_data=b_cfg,
                    global_scenarios=global_scenarios,
                    ui_state=self._collect_project_ui_state(),
                    bim_layout=self.bim_layout,
                )

            QMessageBox.information(
                self,
                tr("Sucesso"),
                f"{tr('Projeto salvo com sucesso (incluindo chuva, edificação, custos e otimizador) em:')}\n{file_path}\n\n"
                + tr("Arquivos .triton/.json incluem a série diária de chuva no próprio projeto e podem ser reabertos sem o CSV original.")
            )
        except Exception as e:
            import traceback
            QMessageBox.critical(self, tr("Erro ao Salvar"), f"{tr('Falha ao salvar projeto')}:\n{str(e)}\n\n{traceback.format_exc()}")

    def on_show_manual(self):
        # O menu mostrava só autores e versão; agora abre o PDF do manual, que
        # acompanha o programa, e só cai na mensagem quando ele não existe.
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        from triton.ui.tab_documentation import caminho_do_manual_completo
        for relativo in (caminho_do_manual_completo(),):
            caminho = get_resource_path(relativo)
            if os.path.isfile(caminho):
                QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))
                return
        QMessageBox.information(
            self,
            tr(f"Manual do Usuário — Triton {__version__}"),
            tr('{0} — {1}\n{2}: Eng. Igor Catão Martins Vaz & Prof. Enedir Ghisi, PhD\n{3} (UFSC)').format(APP_VERSION_LABEL, tr('Manual do Usuário'), tr('Autores'), tr('Grupo de Pesquisa em Ambientes Sustentáveis'))
        )

    def on_show_citation(self):
        from triton.core.edition import usa_dados_do_brasil
        brasil = usa_dados_do_brasil()
        # O local de publicação (Florianópolis/Brasil) é da Edição Brasil; as outras citam só a
        # instituição, sem país, e não nomeiam norma de citação.
        local = "Florianópolis: " if brasil else ""
        citation = (
            f"VAZ, I. C. M.; GHISI, E. <b>Triton {__version__}</b>: "
            f"{tr('Programa computacional para simulação de aproveitamento de água de chuva em edificações')}. "
            f"{local}Universidade Federal de Santa Catarina, {tr('Grupo de Pesquisa em Ambientes Sustentáveis')}, 2026. "
            f"{tr('Software de computador, versão')} {__version__}."
        )
        endereco = "&nbsp;&nbsp;address = {Florianópolis, Brasil},<br>" if brasil else ""
        bibtex = (
            f"@software{{triton_{__version__.replace('.', '_')},<br>"
            f"&nbsp;&nbsp;author = {{Vaz, Igor Catão Martins and Ghisi, Enedir}},<br>"
            f"&nbsp;&nbsp;title = {{Triton {__version__}: Programa computacional para simulação de aproveitamento de água de chuva em edificações}},<br>"
            f"&nbsp;&nbsp;year = {{2026}},<br>"
            f"&nbsp;&nbsp;publisher = {{Universidade Federal de Santa Catarina (UFSC)}},<br>"
            f"{endereco}"
            f"&nbsp;&nbsp;version = {{{__version__}}}<br>}}"
        )
        titulo_da_referencia = "Referência recomendada (ABNT NBR 6023)" if brasil else "Referência recomendada"
        QMessageBox.information(
            self,
            tr("Como Citar o Triton"),
            f"<p><b>{tr(titulo_da_referencia)}</b></p><p>{citation}</p>"
            f"<p><b>BibTeX</b></p><p><tt>{bibtex}</tt></p>"
        )

    def on_show_validation_report(self):
        from triton.ui.dialogs import DialogValidationReport
        dlg = DialogValidationReport(self)
        dlg.exec()

    def on_show_about(self):
        from triton.core.edition import usa_dados_do_brasil
        QMessageBox.information(
            self,
            tr(f"Sobre o Triton {__version__}"),
            tr('<b>{0}</b><br><br>{1}<br><b>{2}:</b> Eng. Igor Catão Martins Vaz &amp; Prof. Enedir Ghisi, PhD<br>{3}<br><br><i>{4}</i>').format(APP_VERSION_LABEL, tr('Plataforma para Aproveitamento de Água de Chuva em Edificações.'), tr('Autores'), tr('Desenvolvido no Grupo de Pesquisa em Ambientes Sustentáveis (UFSC).'), tr('Versão científica e operacional com modelagem diária YAS, análise de ciclo de vida (ACV), tomada de decisão multicritério (TOPSIS/SMAA-VIKOR) e catálogo tarifário nacional.' if usa_dados_do_brasil() else 'Versão científica e operacional com modelagem diária YAS, análise de ciclo de vida (ACV) e tomada de decisão multicritério (TOPSIS/SMAA-VIKOR).'))
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
                "Grupo de Pesquisa em Ambientes Sustentáveis. Para um estudo de projeto, a planilha "
                "de cenários desta tela responde a mesma pergunta.</p>"
                "<p>Deseja salvar a planilha modelo de cenários (<code>.xlsx</code>) para preenchimento agora?</p>"
            )
        )
        btn_download = msg.addButton(tr("📥 Baixar Planilha Modelo (.xlsx)"), QMessageBox.AcceptRole)
        btn_cancel = msg.addButton(tr("Cancelar"), QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() != btn_download:
            return

        def_name = self.get_kebab_filename(nome_sugerido("triton-modelo-cenarios"), "xlsx")
        file_path, _ = QFileDialog.getSaveFileName(self, tr("Salvar Modelo Excel de Cenários"), def_name, "Planilha Excel (*.xlsx)")
        if file_path:
            from triton.core.excel_scenarios import generate_sample_scenario_excel
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
        file_path, _ = QFileDialog.getOpenFileName(self, tr("Selecionar Arquivo de Cenários Excel"), "", "Planilhas (*.xlsx *.xls *.csv)")
        if file_path:
            from triton.core.excel_scenarios import parse_excel_scenarios, run_parsed_scenarios, export_scenarios_to_excel_bytes
            try:
                scenarios = parse_excel_scenarios(file_path)
                if not scenarios:
                    QMessageBox.warning(self, tr("Aviso"), tr("Nenhum cenário válido encontrado na planilha."))
                    return
                avisos = [a for sc in scenarios for a in sc.get("avisos", [])]
                if avisos and QMessageBox.question(
                        self, tr("Confira a substituição pluvial"),
                        tr("A coluna de substituição está em percentual (40 = 40%).") + "\n\n"
                        + "\n".join(avisos) + "\n\n" + tr("Simular mesmo assim?")) != QMessageBox.Yes:
                    return
                results = run_parsed_scenarios(scenarios)
                def_out = self.get_kebab_filename(nome_sugerido("triton-resultados-cenarios"), "xlsx")
                out_path, _ = QFileDialog.getSaveFileName(self, tr("Salvar Resultados dos Cenários"), def_out, "Planilha Excel (*.xlsx)")
                if out_path:
                    excel_bytes = export_scenarios_to_excel_bytes(results)
                    with open(out_path, "wb") as f:
                        f.write(excel_bytes)
                    QMessageBox.information(self, tr("Simulação Concluída"), tr('Simulação de {0} cenários realizada com sucesso!\nResultados salvos em:\n{1}').format(len(scenarios), out_path))
            except Exception as e:
                QMessageBox.critical(self, tr("Erro na Simulação"), tr('Erro ao processar arquivo:\n{0}').format(str(e)))
