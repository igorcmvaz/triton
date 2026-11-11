"""
Aba de Documentação do Triton (Layout Vertical em Duas Colunas).
Explicitação detalhada de todas as variáveis de entrada/saída, equações,
os 9 índices pluviométricos (ETCCDI / Walsh & Lawler), coeficientes de escoamento/absorção
de telhados (com citação do artigo do MIX Sustentável 2020), discussão sobre valores médios
vs. simulação diária e referências bibliográficas.
"""

import base64
import os
from pathlib import Path
import re
import subprocess
import webbrowser

from triton.core.edition import get_current_edition

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QStackedWidget, QTextBrowser, QFrame, QPushButton, QScrollArea, QSizePolicy,
    QFileDialog, QMessageBox, QMenu
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices

from triton.ui.translation import get_current_lang, tr, get_current_theme, get_resource_path


def paginas_do_pdf(caminho_relativo: str, padrao: int) -> int:
    """Páginas do PDF do manual, do ``paginas.json`` que o gerador grava ao lado dele.

    ``padrao`` (o número escrito no código) só vale se o índice faltar.
    """
    import json
    try:
        indice = get_resource_path(os.path.join(os.path.dirname(caminho_relativo), "paginas.json"))
        with open(indice, encoding="utf-8") as f:
            return int(json.load(f)[os.path.basename(caminho_relativo)])
    except (OSError, ValueError, KeyError, TypeError):
        return padrao
from triton.core.bibliography import render_bloco_da_secao, render_bibliografia_completa
from triton.core.environmental_justifications import (
    generate_html_justifications_materials,
    generate_html_justifications_pipes,
    generate_html_justifications_pumps,
    generate_html_justifications_operational
)

# ── CONFIGURAÇÃO DE LINKS DO ACERVO TÉCNICO E MANUAL INTERATIVO ──
# URLs de contingência caso os arquivos locais não estejam presentes.
URL_MANUAL_INTERATIVO = "https://www.google.com"


def open_url_in_browser(url: str):
    """Abre uma URL preferencialmente em uma nova janela/aba do Google Chrome ou no navegador padrão."""
    chrome_candidates = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for chrome_path in chrome_candidates:
        if os.path.isfile(chrome_path):
            try:
                subprocess.Popen([chrome_path, url])
                return
            except Exception:
                pass

    # Fallback para o navegador padrão do sistema
    try:
        webbrowser.open_new_tab(url)
    except Exception:
        QDesktopServices.openUrl(QUrl(url))


#: Páginas de cada manual completo, que a aba anuncia; `test_acervo_de_manuais` confere
#: contra os PDFs.
#: As páginas dependem da edição (cada edição publica um manual): o literal fica igual nas três.
PAGINAS_POR_EDICAO = {
    "BRL": {"manual/Manual-Triton.pdf": 482},
    "INT": {"manual/en/Triton-User-Manual.pdf": 297},
    "IBE": {"manual/Manual-Triton.pdf": 310},
}
PAGINAS_DO_MANUAL_COMPLETO = PAGINAS_POR_EDICAO.get(get_current_edition(), {})


def caminho_do_manual_completo() -> str:
    """O manual completo desta edição: o inglês na Internacional, o português na Brasil e na Portugal.

    Não há manual de reserva de outra edição: abri-lo em silêncio seria entregar a quem pediu o manual
    da sua edição o de outro país. Se o arquivo faltar, o aviso diz.
    """
    from triton.core.edition import manual_do_usuario
    return manual_do_usuario(get_current_lang())


def abrir_ou_baixar_manual(rel_path: str, parent: QWidget = None, salvar_como: bool = False):
    """
    Abre o manual técnico em PDF no leitor padrão do sistema operacional ou permite salvar uma cópia local no disco.
    """
    import shutil
    ingles = get_current_lang() != "pt"
    caminho = get_resource_path(rel_path)
    if not os.path.isfile(caminho):
        # Tenta caminhos alternativos conhecidos no repositório / pacote
        basename = os.path.basename(rel_path)
        alternativas = [
            os.path.join("manual", basename),
            os.path.join("manual", "mini", basename),
            os.path.join("manual", "site", "pdf", basename),
        ]
        for alt in alternativas:
            alt_c = get_resource_path(alt)
            if os.path.isfile(alt_c):
                caminho = alt_c
                break

    if not os.path.isfile(caminho):
        if parent:
            title = "Manual" if not ingles else "Manual"
            from triton.core.edition import usa_dados_do_brasil
            if usa_dados_do_brasil():
                msg = ("Arquivo do manual não encontrado:" if not ingles else "Manual file not found:") + f"\n{rel_path}"
            else:
                # o caminho seria o do manual do Brasil; a mensagem não o cita
                from triton.ui.translation import em_portugues_da_edicao
                msg = (em_portugues_da_edicao("O manual desta edição não está instalado.") if not ingles
                       else "The manual for this edition is not installed.")
            QMessageBox.warning(parent, title, msg)
        return False

    caminho_abs = os.path.abspath(caminho)

    if salvar_como:
        nome_sugerido = os.path.basename(caminho_abs)
        title_save = "Salvar Manual em PDF" if not ingles else "Save Manual PDF"
        filter_save = "Documento PDF (*.pdf)" if not ingles else "PDF Document (*.pdf)"
        dest_path, _ = QFileDialog.getSaveFileName(
            parent,
            title_save,
            nome_sugerido,
            filter_save
        )
        if dest_path:
            try:
                shutil.copy2(caminho_abs, dest_path)
                title_ok = "Sucesso" if not ingles else "Success"
                msg_ok = ("Manual salvo com sucesso em:" if not ingles else "Manual saved successfully to:") + f"\n{dest_path}"
                QMessageBox.information(parent, title_ok, msg_ok)
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(dest_path)))
                return True
            except Exception as e:
                if parent:
                    title_err = "Erro ao Salvar" if not ingles else "Save Error"
                    QMessageBox.critical(parent, title_err, str(e))
                return False
        return False

    # Abertura direta no leitor de PDF padrão do sistema
    url = QUrl.fromLocalFile(caminho_abs)
    sucesso = QDesktopServices.openUrl(url)
    if not sucesso and hasattr(os, "startfile"):
        try:
            os.startfile(caminho_abs)
            sucesso = True
        except Exception:
            pass

    if not sucesso and parent:
        title = "Manual" if not ingles else "Manual"
        msg = (
            "Não foi possível abrir o leitor padrão de PDF. Tente salvar uma cópia do arquivo."
            if not ingles else
            "Could not open default PDF viewer. Try saving a copy."
        )
        QMessageBox.warning(parent, title, msg)
    return sucesso


def abrir_manual_interativo(parent: QWidget = None):
    """
    Abre o portal interativo do manual (HTML local ou fallback web).
    """
    site_path = get_resource_path(os.path.join("manual", "site", "index.html"))
    if os.path.isfile(site_path):
        url = QUrl.fromLocalFile(os.path.abspath(site_path)).toString()
        open_url_in_browser(url)
        return True
    elif URL_MANUAL_INTERATIVO and URL_MANUAL_INTERATIVO != "https://www.google.com":
        open_url_in_browser(URL_MANUAL_INTERATIVO)
        return True
    else:
        return abrir_ou_baixar_manual(caminho_do_manual_completo(), parent=parent)


def _configurar_botao_manual(btn: QPushButton, rel_path: str, parent: QWidget = None):
    """Conecta o clique do botão para abrir o PDF e adiciona menu de contexto para salvar cópia."""
    btn.clicked.connect(lambda: abrir_ou_baixar_manual(rel_path, parent=parent, salvar_como=False))
    btn.setToolTip(
        "Clique para abrir o PDF no leitor padrão ou clique com o botão direito para salvar uma cópia."
        if get_current_lang() == "pt" else
        "Click to open PDF in default viewer or right-click to save a copy."
    )
    btn.setContextMenuPolicy(Qt.CustomContextMenu)

    def on_context(point):
        menu = QMenu(btn)
        ingles = get_current_lang() != "pt"
        act_open = menu.addAction("Abrir no leitor de PDF" if not ingles else "Open in PDF Reader")
        act_save = menu.addAction("Salvar cópia do arquivo como..." if not ingles else "Save copy as...")
        chosen = menu.exec(btn.mapToGlobal(point))
        if chosen == act_open:
            abrir_ou_baixar_manual(rel_path, parent=parent, salvar_como=False)
        elif chosen == act_save:
            abrir_ou_baixar_manual(rel_path, parent=parent, salvar_como=True)

    btn.customContextMenuRequested.connect(on_context)


def _get_asset_data_uri(rel_path: str) -> str:
    """Retorna data URI em base64 para imagens garantindo renderização independente de path."""
    for base in [Path(__file__).resolve().parent.parent.parent, Path.cwd()]:
        candidate = base / rel_path
        if candidate.is_file():
            try:
                mime = "image/png" if rel_path.endswith(".png") else "image/jpeg"
                with open(candidate, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("ascii")
                return f"data:{mime};base64,{b64}"
            except Exception:
                pass
    return ""


def _get_asset_pixmap(rel_path: str, w: int, h: int) -> QPixmap:
    """Carrega imagem de caminho relativo e redimensiona suavemente mantendo proporção."""
    for base in [Path(__file__).resolve().parent.parent.parent, Path.cwd()]:
        candidate = base / rel_path
        if candidate.is_file():
            pm = QPixmap(str(candidate))
            if not pm.isNull():
                return pm.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return QPixmap()


class _ResponsiveScrollArea(QScrollArea):
    """QScrollArea que restringe a largura máxima do widget interno à largura visível do viewport,
    impedindo que cartões ou rótulos empurrem a área útil para fora da tela legível.
    """
    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.widget()
        if w:
            vw = self.viewport().width()
            w.setMaximumWidth(vw)


class _DocTabsProxy:
    """Proxy para manter compatibilidade retroativa com códigos/testes que acessem self.doc_tabs."""
    def __init__(self, list_widget: QListWidget, stack_widget: QStackedWidget):
        self.list_widget = list_widget
        self.stack_widget = stack_widget

    def count(self) -> int:
        return self.stack_widget.count()

    def widget(self, index: int):
        # Mapeamento retrocompatível para testes que acessavam índices da versão pré-reordenação
        legacy_signatures = {
            2: "10.29183/2447-3073",
            3: "PRCPTOT",
            7: "Maykot",
        }
        if index in legacy_signatures:
            target_kw = legacy_signatures[index]
            for i in range(self.stack_widget.count()):
                w = self.stack_widget.widget(i)
                if hasattr(w, "toHtml") and target_kw in w.toHtml():
                    return w
        return self.stack_widget.widget(index)

    def setCurrentIndex(self, index: int):
        self.list_widget.setCurrentRow(index)
        self.stack_widget.setCurrentIndex(index)

    def currentIndex(self) -> int:
        return self.stack_widget.currentIndex()


class TabDocumentation(QWidget):
    #: Fora da Edição Brasil, a página que perde quase todo o texto ao tirar o que cita o Brasil
    #: (menos de tantos caracteres) não é oferecida: melhor sem a página do que uma página oca.
    MINIMO_DE_TEXTO_DA_PAGINA = 600

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.init_ui()
        self._no_portugues_da_edicao()

    def _no_portugues_da_edicao(self):
        """Na Portugal, os rótulos e botões escritos direto em português (as capas dos
        volumes do manual, «Baixar PDF») passam pelo glossário, como os do catálogo.

        Os textos longos da documentação (QTextBrowser) ficam como estão: citam títulos
        de trabalhos brasileiros, que o glossário não pode reescrever."""
        from triton.ui.translation import em_portugues_da_edicao
        for w in self.findChildren(QLabel) + self.findChildren(QPushButton):
            texto = w.text()
            novo = em_portugues_da_edicao(texto)
            if novo != texto:
                w.setText(novo)
            dica = w.toolTip()
            if dica and em_portugues_da_edicao(dica) != dica:
                w.setToolTip(em_portugues_da_edicao(dica))

    def init_ui(self):
        self.setObjectName("tabDocumentationRoot")
        is_dark = get_current_theme() == "dark"
        canvas_bg = "#0c1815" if is_dark else "#eef2f6"
        card_border = "#234d43" if is_dark else "#cbd5e1"
        self.setStyleSheet(f"""
            QWidget#tabDocumentationRoot {{
                background-color: {canvas_bg};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)

        # Header Principal da Aba - Tipografia Moderna e Semântica
        title_color = "#f8fafc" if is_dark else "#0f172a"
        sub_color = "#94a3b8" if is_dark else "#64748b"

        lbl_title = QLabel(tr("📚 Base Técnica, Metodologia e Premissas do Projeto"))
        lbl_title.setStyleSheet(f"font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, sans-serif; font-size: 22px; font-weight: 800; color: {title_color}; letter-spacing: -0.4px; margin: 0px;")
        main_layout.addWidget(lbl_title)

        lbl_subtitle = QLabel(
            tr("Guia técnico para leitura dos resultados, definição das premissas e consulta das fontes. Valores automáticos são referências "
            "preliminares: o responsável técnico deve validar dados locais, normas aplicáveis, equipamentos e orçamentos antes de emitir o projeto.")
        )
        lbl_subtitle.setStyleSheet(f"font-size: 12.5px; color: {sub_color}; line-height: 1.5;")
        lbl_subtitle.setWordWrap(True)
        lbl_subtitle.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        lbl_subtitle.setMinimumWidth(100)
        main_layout.addWidget(lbl_subtitle)

        # LAYOUT EM DUAS COLUNAS (Navegação Vertical na Esquerda + Conteúdo na Direita)
        body_layout = QHBoxLayout()
        body_layout.setSpacing(14)

        # Coluna Esquerda: Menu Vertical de Tópicos (QListWidget Moderno)
        self.list_topics = QListWidget()
        self.list_topics.setFixedWidth(290)
        self.list_topics.setWordWrap(True)
        self.list_topics.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        list_bg = "#122b25" if is_dark else "#ffffff"
        list_text = "#f4fbf8" if is_dark else "#334155"
        list_hover = "#1a4d40" if is_dark else "#f1f5f9"
        self.list_topics.setStyleSheet(f"""
            QListWidget {{
                background-color: {list_bg};
                border: 1px solid {card_border};
                border-radius: 14px;
                padding: 8px;
                outline: 0;
            }}
            QListWidget::item {{
                padding: 10px 14px;
                font-size: 12.5px;
                font-weight: 500;
                color: {list_text};
                border-radius: 8px;
                margin-bottom: 3px;
            }}
            QListWidget::item:hover {{
                background-color: {list_hover};
                color: {'#48d5b7' if is_dark else '#0f172a'};
                font-weight: 600;
            }}
            QListWidget::item:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #087f6b, stop:1 #0284c7);
                color: #ffffff;
                font-weight: 700;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 6px;
                margin: 4px 2px 4px 0;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {'#234d43' if is_dark else '#cbd5e1'};
                min-height: 24px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {'#48d5b7' if is_dark else '#94a3b8'};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                width: 0px;
                border: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)
        self.list_topics.setCursor(Qt.PointingHandCursor)

        from triton.core.edition import usa_dados_do_brasil as _brasil
        titulo_esg = (tr("Certificações Sustentáveis & Critérios ESG (LEED, AQUA, Casa Azul, EDGE, GRI)") if _brasil()
                      else tr("Certificações Sustentáveis & Critérios ESG (LEED, EDGE, GRI)"))
        paginas = [
            ("📚 " + tr("Manuais Oficiais & Acervo Técnico"), self.create_tab_manuals_overview),
            ("🧭 " + tr("Metodologia de Cálculo por Etapa"), self.create_tab_calculation_method),
            ("🏆 " + tr("TOPSIS: Decisão Multicritério"), self.create_tab_topsis_method),
            ("🏠 " + tr("Coeficientes de Telhados (MIX)"), self.create_tab_roof_materials),
            ("📊 " + tr("9 Índices Pluviométricos (ETCCDI + Sazonalidade)"), self.create_tab_rain_indices),
            ("🌧️ " + tr("Precipitação & Hidrologia"), self.create_tab_rainfall_hydrology),
            ("🏢 " + tr("Edificação & Demanda"), self.create_tab_building_demand),
            ("🚰 " + tr("Reservatórios & Bombeamento"), self.create_tab_tanks_pumping),
            ("🧪 " + tr("Qualidade da Água & Linha de Tratamento (ETAP)"), self.create_tab_water_quality_etap),
            ("📈 " + tr("Indicadores de Eficiência"), self.create_tab_indicators_performance),
            ("💰 " + tr("Análise Econômico-Financeira"), self.create_tab_economics),
            ("💡 " + tr("Discussão: Valores Médios vs Simulação"), self.create_tab_discussion_average_values),
            ("⚙️ " + tr("Tarifas, Impostos & OPEX"), self.create_tab_tariffs_and_opex),
            ("🍃 " + tr("Análise do Ciclo de Vida (ACV): Premissas e Justificativas"), self.create_tab_acv_justifications),
            ("🌿 " + titulo_esg, self.create_tab_esg_certifications),
            ("📖 " + tr("Referências Bibliográficas"), self.create_tab_references),
            ("⌨️ " + tr("Uso pela Linha de Comando"), self.create_tab_cli_usage),
        ]

        # Coluna Direita: QStackedWidget com os Painéis de Conteúdo
        self.stack_content = QStackedWidget()
        self.stack_content.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)

        # O Manual Oficial e Acervo Técnico é a primeira página. Fora da Edição Brasil as páginas
        # saem sem o que cita o Brasil; a que não sobra com conteúdo seguro não é oferecida.
        for titulo, criar in paginas:
            pagina = criar()
            if not _brasil() and isinstance(pagina, QTextBrowser) and int(pagina.property("texto_do_corpo") or 0) < self.MINIMO_DE_TEXTO_DA_PAGINA:
                pagina.deleteLater()
                continue
            self.list_topics.addItem(QListWidgetItem(titulo))
            self.stack_content.addWidget(pagina)

        body_layout.addWidget(self.list_topics)

        body_layout.addWidget(self.stack_content, stretch=1)
        main_layout.addLayout(body_layout, stretch=1)

        # Conecta seleção da lista com a troca de página no stacked widget
        self.list_topics.currentRowChanged.connect(self.stack_content.setCurrentIndex)
        self.list_topics.setCurrentRow(0)

        # Proxy para manter retrocompatibilidade com self.doc_tabs
        self.doc_tabs = _DocTabsProxy(self.list_topics, self.stack_content)

    def _equation_where(self, equation: str) -> str:
        """Glossário local das variáveis, repetido após cada equação para leitura independente."""
        clean = re.sub(r"<[^>]+>", "", equation).replace(" ", "").lower()
        # Espanhol e chinês exibem a documentação técnica em inglês enquanto
        # seus catálogos editoriais específicos são expandidos.
        en = get_current_lang() != "pt"
        if clean.startswith("vcap"):
            return ("Where: <i>Vcap,t</i> is the captured volume on day <i>t</i>; <i>A</i> is catchment area; <i>P<sub>t</sub></i> is daily rainfall; <i>d<sub>f</sub></i> is first-flush depth; and <i>C</i> is the runoff coefficient."
                    if en else "Onde: <i>Vcap,t</i> é o volume captado no dia <i>t</i>; <i>A</i> é a área de captação; <i>P<sub>t</sub></i> é a precipitação diária; <i>d<sub>f</sub></i> é a lâmina de descarte inicial; e <i>C</i> é o coeficiente de escoamento.")
        if clean.startswith("dpl"):
            return ("Where: <i>Dpl,t</i> is daily rainwater demand; <i>N</i> is the number of occupants; <i>q</i> is per-capita demand; and <i>s</i> is the non-potable rainwater share."
                    if en else "Onde: <i>Dpl,t</i> é a demanda pluvial diária; <i>N</i> é o número de ocupantes; <i>q</i> é a demanda per capita; e <i>s</i> é a fração não potável atendida por água pluvial.")
        if clean.startswith(("st=", "vinf")):
            return ("Where: <i>S<sub>t</sub></i> / <i>Vinf,t</i> is end-of-day stored volume; <i>V</i> is tank capacity; <i>Vcap,t</i> is captured water; and <i>Dpl,t</i> is the requested demand."
                    if en else "Onde: <i>S<sub>t</sub></i> / <i>Vinf,t</i> é o volume armazenado no fim do dia; <i>V</i> é a capacidade do reservatório; <i>Vcap,t</i> é a água captada; e <i>Dpl,t</i> é a demanda solicitada.")
        if clean.startswith("epot"):
            return ("Where: <i>Epot</i> is potable-water saving potential; the numerator is rainwater actually supplied; and the denominator is total potable-water demand."
                    if en else "Onde: <i>Epot</i> é o potencial de economia de água potável; o numerador é a água pluvial efetivamente atendida; e o denominador é a demanda total de água potável.")
        if clean.startswith(("vpl", "npv")):
            return ("Where: NPV is net present value; CAPEX is initial investment; <i>FCt</i> is net cash flow in year <i>t</i>; and <i>i</i> / MARR is the discount rate."
                    if en else "Onde: VPL é o valor presente líquido; CAPEX é o investimento inicial; <i>FCt</i> é o fluxo de caixa líquido no ano <i>t</i>; e <i>i</i> / TMA é a taxa de desconto.")
        if clean.startswith(("co2emb", "co2incorporado")):
            return ("Where: CO2emb is embodied carbon; <i>m<sub>i</sub></i> / quantity is the amount of component <i>i</i>; and <i>f<sub>i</sub></i> / emission factor is its carbon factor."
                    if en else "Onde: CO2incorporado é o carbono incorporado; <i>m<sub>i</sub></i> / quantidade é a quantidade do componente <i>i</i>; e <i>f<sub>i</sub></i> / fator de emissão é seu fator de carbono.")
        if clean.startswith(("co2op", "co2operacional")):
            return ("Where: CO2op is operational carbon; pump energy is electricity used for pumping; grid factor is kg CO2e per kWh; treated volume is water treated; and treatment factor is kg CO2e per m³."
                    if en else "Onde: CO2operacional é o carbono operacional; energia da bomba é a eletricidade de recalque; fator da rede é kg CO2e por kWh; volume tratado é a água tratada; e fator de tratamento é kg CO2e por m³.")
        if clean.startswith(("co2avoid", "co2evitado")):
            return ("Where: CO2avoid is avoided carbon; saved potable water is the volume not supplied by the grid; and potable-water factor is the associated emission factor."
                    if en else "Onde: CO2evitado é o carbono evitado; água potável economizada é o volume não suprido pela rede; e fator de água potável é o fator de emissão associado.")
        if clean.startswith(("co2net", "co2líquido")):
            return ("Where: CO2net is the life-cycle balance; CO2avoid is avoided emissions; CO2emb is embodied emissions; CO2op is operational emissions; and life is the analysis period."
                    if en else "Onde: CO2líquido é o balanço de ciclo de vida; CO2evitado são as emissões evitadas; CO2incorporado são as emissões incorporadas; CO2operacional são as emissões operacionais; e vida é o período de análise.")
        if clean.startswith("x="):
            return ("Where: <i>X</i> is the decision matrix and <i>xij</i> is the value of criterion <i>j</i> for alternative <i>i</i>."
                    if en else "Onde: <i>X</i> é a matriz de decisão e <i>xij</i> é o valor do critério <i>j</i> para a alternativa <i>i</i>.")
        if clean.startswith("rij"):
            return ("Where: <i>rij</i> is the normalized value of criterion <i>j</i> for alternative <i>i</i>; and the denominator is the Euclidean norm of that criterion."
                    if en else "Onde: <i>rij</i> é o valor normalizado do critério <i>j</i> para a alternativa <i>i</i>; e o denominador é a norma euclidiana desse critério.")
        if clean.startswith("vij"):
            return ("Where: <i>vij</i> is the weighted normalized value; <i>wj</i> is the normalized weight of criterion <i>j</i>; and <i>rij</i> is its normalized performance."
                    if en else "Onde: <i>vij</i> é o valor normalizado ponderado; <i>wj</i> é o peso normalizado do critério <i>j</i>; e <i>rij</i> é seu desempenho normalizado.")
        if clean.startswith(("aj+", "aj−", "aj-", "a+", "a−")):
            return ("Where: <i>A+</i> is the ideal positive solution, <i>A−</i> is the ideal negative solution, and <i>vij</i> is the weighted normalized value."
                    if en else "Onde: <i>A+</i> é a solução ideal positiva, <i>A−</i> é a solução ideal negativa, e <i>vij</i> é o valor normalizado ponderado.")
        if clean.startswith(("di+", "di−", "di-")):
            return ("Where: <i>Di+</i> / <i>Di−</i> is the Euclidean distance of alternative <i>i</i> to the positive/negative ideal; <i>vij</i> is its weighted value; and <i>A+j</i> / <i>A−j</i> is the ideal criterion value."
                    if en else "Onde: <i>Di+</i> / <i>Di−</i> é a distância euclidiana da alternativa <i>i</i> ao ideal positivo/negativo; <i>vij</i> é seu valor ponderado; e <i>A+j</i> / <i>A−j</i> é o valor ideal do critério.")
        if clean.startswith("ci"):
            return ("Where: <i>Ci</i> is the TOPSIS closeness coefficient; <i>Di−</i> is the distance to the negative ideal; and <i>Di+</i> is the distance to the positive ideal."
                    if en else "Onde: <i>Ci</i> é o coeficiente de proximidade TOPSIS; <i>Di−</i> é a distância ao ideal negativo; e <i>Di+</i> é a distância ao ideal positivo.")
        if clean.startswith(("energy", "energia")):
            return ("Where: energy is annual electricity use; power is pump power; pumping hours are transfer hours; startups are pump activations; startup duration is time per activation; and η is pump efficiency."
                    if en else "Onde: energia é o consumo anual de eletricidade; potência é a potência da bomba; horas de recalque são as horas de transferência; partidas são os acionamentos; tempo de partida é a duração de cada acionamento; e η é o rendimento da bomba.")
        return "Where: all symbols are defined by the immediately associated calculation step." if en else "Onde: todos os símbolos são definidos pela etapa de cálculo imediatamente associada."

    @staticmethod
    def _html_da_edicao(html: str) -> str:
        """Fora da Edição Brasil, a página sem o que cita o Brasil (``textos_da_edicao.html_da_edicao``).

        A série de exemplo dos comandos de linha de comando é a da edição, e não a de Florianópolis.
        """
        from triton.core.edition import usa_dados_do_brasil, serie_de_exemplo_da_edicao
        if usa_dados_do_brasil():
            return html
        from triton.ui.textos_da_edicao import html_da_edicao
        return html_da_edicao(html.replace("Florianopolis1.csv", serie_de_exemplo_da_edicao()))

    def _create_browser(self, html_content: str, secao: str | None = None) -> QTextBrowser:
        """Aplica tipografia editorial e transforma equações em blocos científicos numerados.

        As fórmulas são extraídas somente de parágrafos completos.  Substituir uma
        tag ``code`` no meio de um ``p`` gerava HTML inválido no QTextBrowser, o
        que fazia texto normal herdar a fonte matemática e deixava pontuação e
        espaçamentos soltos.

        Quando ``secao`` é informada, o bloco «Referências desta seção» é
        anexado ao final, a partir de :mod:`triton.core.bibliography`. Ele entra
        **depois** do processamento de equações justamente para ficar fora do
        alcance do regex acima, que reescreve parágrafos contendo ``<code>``
        com ``=`` — uma citação apanhada por ele sairia reempacotada.
        """
        equation_number = 0
        html_content = self._html_da_edicao(html_content)
        from triton.ui.textos_da_edicao import texto_do_html
        corpo_da_pagina = len(texto_do_html(html_content))   # sem o bloco de referências, anexado depois

        def equation_block(raw_equation: str) -> str:
            nonlocal equation_number
            equation_number += 1
            equation = re.sub(r"\s+", " ", raw_equation).strip()
            where = self._equation_where(equation)
            where_title = where.split(':', 1)[0]
            where_desc = where.split(':', 1)[1] if ':' in where else ''

            is_dark = get_current_theme() == "dark"
            card_bg = "#122b25" if is_dark else "#f8fafc"
            card_border = "#234d43" if is_dark else "#e2e8f0"
            border_accent = "#48d5b7" if is_dark else "#0284c7"
            formula_color = "#38bdf8" if is_dark else "#0369a1"
            badge_bg = "#1a4d40" if is_dark else "#e0f2fe"
            badge_fg = "#48d5b7" if is_dark else "#0284c7"
            note_color = "#a3cdc3" if is_dark else "#64748b"
            title_color = "#f4fbf8" if is_dark else "#334155"

            return (
                f"<table width='100%' cellpadding='0' cellspacing='0' style='background-color: {card_bg}; border: 1px solid {card_border}; border-left: 4px solid {border_accent}; border-radius: 8px; margin: 14px 0;'>"
                "<tr>"
                f"<td style='padding: 10px 14px; font-family: \"Cascadia Code\", \"Fira Code\", \"Segoe UI\", monospace; font-size: 13px; font-weight: 700; color: {formula_color};'>{equation}</td>"
                f"<td align='right' style='padding: 10px 14px; white-space: nowrap;'><span style='background-color: {badge_bg}; color: {badge_fg}; font-weight: 800; font-size: 10.5px; padding: 3px 8px; border-radius: 4px;'>EQ. {equation_number}</span></td>"
                "</tr>"
                "<tr>"
                f"<td colspan='2' style='padding: 6px 14px 10px 14px; border-top: 1px dashed {card_border}; font-size: 11.5px; color: {note_color}; line-height: 1.45;'>"
                f"<b style='color: {title_color};'>{where_title}:</b>{where_desc}"
                "</td>"
                "</tr>"
                "</table>"
            )

        code_pattern = re.compile(r"<code(?:\s+[^>]*)?>(.*?)</code>", re.DOTALL | re.IGNORECASE)

        def replace_paragraph(match: re.Match) -> str:
            body = match.group(1)
            pieces = code_pattern.split(body)
            if len(pieces) == 1:
                return match.group(0)

            # Comandos, caminhos e opções também usam <code>, mas não são
            # equações. Mantê-los no parágrafo original evita numerá-los e
            # anexar a explicação de símbolos destinada apenas às fórmulas.
            code_items = code_pattern.findall(body)
            if not any("=" in re.sub(r"<[^>]+>", "", item) for item in code_items):
                return match.group(0)

            blocks = []
            for index, piece in enumerate(pieces):
                piece = piece.strip()
                if not piece:
                    continue
                if index % 2:
                    blocks.append(equation_block(piece))
                else:
                    # Texto antes/depois de uma fórmula permanece em fonte normal.
                    blocks.append(f"<p>{piece}</p>")
            return "".join(blocks)

        content = re.sub(
            r"<p(?:\s+[^>]*)?>(.*?)</p>",
            replace_paragraph,
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        is_dark = get_current_theme() == "dark"
        text_color = "#f4fbf8" if is_dark else "#334155"
        surface_color = "#122b25" if is_dark else "#ffffff"
        border_color = "#234d43" if is_dark else "#cbd5e1"
        header_title = "#f8fafc" if is_dark else "#0f172a"
        header_sub = "#48d5b7" if is_dark else "#0284c7"
        tbl_th_bg = "#1a4d40" if is_dark else "#f1f5f9"
        tbl_th_fg = "#f8fafc" if is_dark else "#0f172a"
        tbl_th_border = "#2bb99c" if is_dark else "#cbd5e1"
        tbl_td_border = "#1f4239" if is_dark else "#f1f5f9"
        tbl_even_bg = "#15332c" if is_dark else "#f8fafc"
        pre_bg = "#0b1a17" if is_dark else "#0f172a"
        pre_fg = "#48d5b7" if is_dark else "#38bdf8"
        code_bg = "#1a4d40" if is_dark else "#f1f5f9"
        code_fg = "#48d5b7" if is_dark else "#0369a1"

        style = f"""
        <style>
            body {{ color:{text_color}; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, sans-serif; font-size:13px; line-height:1.6; margin:16px 36px 24px 20px; padding:0; }}
            h2 {{ color:{header_title}; font-size:21px; margin:0 0 16px 0; font-weight:800; letter-spacing:-0.3px; border-bottom:2px solid {border_color}; padding-bottom:10px; }}
            h3 {{ color:{header_sub}; font-size:15.5px; margin:24px 0 8px 0; font-weight:700; }}
            h4 {{ font-size:13.5px; margin:14px 0 6px 0; font-weight:600; color:{header_title}; }}
            p {{ margin:8px 0; line-height:1.6; color:{text_color}; }}
            b, strong {{ color:{header_title}; }}
            pre {{ background:{pre_bg}; border:1px solid {border_color}; border-radius:8px; padding:12px 16px; color:{pre_fg}; font-family:'Cascadia Code','Consolas',monospace; font-size:11.5px; white-space:pre-wrap; line-height:1.5; }}
            code {{ background:{code_bg}; color:{code_fg}; border:1px solid {border_color}; border-radius:4px; padding:2px 6px; font-family:'Cascadia Code','Consolas',monospace; font-size:11.5px; }}
            li {{ margin:4px 0; line-height:1.5; }}
            table {{ border-collapse:collapse; width:100%; margin:16px 0; font-size:12px; border:1px solid {border_color}; border-radius:8px; }}
            th {{ background:{tbl_th_bg}; color:{tbl_th_fg}; font-weight:700; padding:9px 12px; border-bottom:2px solid {tbl_th_border}; text-align:left; }}
            td {{ padding:9px 12px; border-bottom:1px solid {tbl_td_border}; color:{text_color}; vertical-align:top; }}
            tr:nth-child(even) td {{ background-color:{tbl_even_bg}; }}
        </style>
        """
        if secao:
            content += self._html_da_edicao(
                render_bloco_da_secao(secao, get_current_lang() if get_current_lang() == "pt" else "en"))

        browser = QTextBrowser()
        browser.setOpenLinks(False)
        browser.setOpenExternalLinks(False)
        browser.anchorClicked.connect(self._on_anchor_clicked)
        browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        browser.setFrameShape(QFrame.NoFrame)
        browser.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {surface_color};
                border: 1px solid {border_color};
                border-radius: 14px;
                padding: 0px;
                color: {text_color};
                selection-background-color: #0284c7;
                selection-color: #ffffff;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 6px 4px 6px 0;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {'#234d43' if is_dark else '#cbd5e1'};
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {'#48d5b7' if is_dark else '#94a3b8'};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                width: 0px;
                border: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)
        browser.setHtml(f"<html><head>{style}</head><body>{content}</body></html>")
        browser.setProperty("texto_do_corpo", corpo_da_pagina)
        return browser

    def _on_anchor_clicked(self, qurl: QUrl):
        target = qurl.toString().strip()
        if not target:
            return
        if target.startswith("http://") or target.startswith("https://"):
            open_url_in_browser(target)
            return

        manual_map = {
            "URL_DO_MANUAL_COMPLETO": caminho_do_manual_completo(),
            "URL_DO_MANUAL_VOL_1": "manual/mini/Manual-Triton-1-comece-aqui.pdf",
            "URL_DO_MANUAL_VOL_2": "manual/mini/Manual-Triton-2-metodo.pdf",
            "URL_DO_MANUAL_VOL_3": "manual/mini/Manual-Triton-3-guias.pdf",
            "URL_DO_MANUAL_VOL_4": "manual/mini/Manual-Triton-4-tutorial.pdf",
            "URL_DO_MANUAL_VOL_5": "manual/mini/Manual-Triton-5-confiabilidade.pdf",
            "URL_DO_MANUAL_VOL_6": "manual/mini/Manual-Triton-6-versoes.pdf",
            "URL_DO_MANUAL_VOL_7": "manual/mini/Manual-Triton-7-modulacao.pdf",
            "URL_DO_MANUAL_VOL_8": "manual/mini/Manual-Triton-8-apendices.pdf",
        }

        if target in manual_map:
            abrir_ou_baixar_manual(manual_map[target], parent=self)
            return

        if target in ("URL_DA_PAGINA_WEB_MANUAL_INTERATIVO", "URL_MANUAL_INTERATIVO"):
            abrir_manual_interativo(parent=self)
            return

        if "://" not in target:
            open_url_in_browser(f"https://{target}")
        else:
            open_url_in_browser(target)

    def create_tab_calculation_method(self) -> QWidget:
        """Roteiro auditável das etapas e das equações empregadas pelo programa."""
        if get_current_lang() != "pt":
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🧭 Calculation Method: End-to-End Workflow</h2>
            <p>This page describes the calculation chain used by Triton. Values are calculated from the historical daily series; therefore, results are not based on monthly averages.</p>
            <h3 style='color:#0369a1;'>Steps 1–2 — Rainfall, catchment and demand</h3>
            <p>For each day <i>t</i>, the programme calculates the usable captured volume.</p>
            <p><code>Peff,t = max(0, Pt − df)</code> on days when the first-flush rule applies, and <code>Peff,t = Pt</code> otherwise; <code>Vcap,t = A × C × Peff,t</code>.</p>
            <p>The first-flush depth <code>df</code> is subtracted from the day's rainfall, so a day with rainfall at or below <code>df</code> yields no capture. This differs deliberately from Netuno 4, which treated <code>df</code> as an event threshold. Since 1 mm over 1 m² equals 1 L, no additional conversion is required. Daily non-potable demand is calculated as follows.</p>
            <p><code>Dpl,t = N × q × s</code></p>
            <h3 style='color:#0369a1;'>Step 3 — Tank sweep and daily balance</h3>
            <p>Each candidate lower-tank volume is simulated over every day in the input series using yield after spillage (YAS):</p>
            <p><code>It = min(V, St−1 + Vcap,t)</code>; <code>Ot = max(0, St−1 + Vcap,t − V)</code>; <code>Yt = min(Dpl,t, It)</code>; <code>St = It − Yt</code>.</p>
            <p>This order matters: storage is capped and spillage occurs before demand is withdrawn. When an upper tank is enabled, transfer cycles are simulated explicitly; pump energy is then calculated from transferred volume, starts, nominal flow, power and global efficiency. The sweep repeats the same state transition for each candidate volume.</p>
            <h3 style='color:#0369a1;'>Step 4 — Technical indicators</h3>
            <p>Water-saving potential is calculated by:</p>
            <p><code>Epot = 100 × Σ(supplied rainwater) / Σ(total potable demand)</code></p>
            <p>The program also reports full, partial and zero-supply days, annual rainwater use, mean overflow and the marginal gain between adjacent tank volumes. The technical optimum is identified after the configured marginal-gain threshold is reached.</p>
            <h3 style='color:#0369a1;'>Step 5 — Economic assessment</h3>
            <p>CAPEX combines tanks, pump (when applicable), pipes, filters, labour and user-adjusted costs. Automatic tank costs are screening estimates obtained by piecewise linear interpolation of the explicit internal table; definitive studies must replace them with dated local quotations. Other operational costs preserve the Netuno 4 semantics: a fixed term plus an optional coefficient per m³ of rainwater consumed in the month when the expense occurs. The default maintenance items are fixed because there is no universal, scientifically transferable cost per m³ of tank capacity.</p>
            <p>Annual gross saving is potable-water and, where applicable, sewage savings less pumping electricity and O&amp;M. Net present value is calculated by:</p>
            <p><code>NPV = −CAPEX + Σ[FCt/(1+i)^t]</code></p>
            <p>IRR is the rate that makes NPV equal zero; simple and discounted payback are the first years with non-negative accumulated nominal and discounted cash flow, respectively.</p>
            <h3 style='color:#0369a1;'>Step 6 — Simplified LCA</h3>
            <p>Embodied emissions are the sum of each component mass times its emission factor.</p>
            <p><code>CO2emb = Σ(mi × fi)</code></p>
            <p>Operational emissions are calculated by:</p>
            <p><code>CO2op = E_pump × f_grid + V_treatment × f_treatment</code></p>
            <p>For chlorine, the detailed calculation is <code>m_Cl2,eq = V_rainwater × dose_applied / 1000</code>, where rainwater is in m³/year and dose is in mg/L; its contribution is <code>CO2chlorine = m_Cl2,eq × f_Cl2</code>. This is theoretical chlorine-equivalent consumption. It is not the water's measured chlorine demand, which requires quality tests and a target residual. These are editable LCA/cost assumptions, not a treatment specification.</p>
            <p>Avoided emissions are calculated by:</p>
            <p><code>CO2avoid = Vwater_saved × f_potable</code></p>
            <p>The lifetime balance is:</p>
            <p><code>CO2net = CO2avoid − CO2emb − life × CO2op</code></p>
            <p>Before the technical sweep, the interface intentionally shows zero environmental results.</p>
            <h3 style='color:#0369a1;'>Steps 7–9 — Decision and communication</h3>
            <p>Step 7 ranks sweep alternatives with TOPSIS using technical, economic and environmental criteria. Step 8 generates stakeholder and research reports from the selected inputs, assumptions and calculated results; Step 9 provides the methodological documentation. Reports are decision-support documents: local designs, standards, bills, quotations and material quantities require professional validation.</p>
            """
        else:
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🧭 Metodologia de Cálculo: Fluxo Completo</h2>
            <p>Esta página descreve a cadeia de cálculo do Triton. Os valores são obtidos a partir da série histórica diária; portanto, os resultados não dependem de médias mensais.</p>
            <h3 style='color:#0369a1;'>Etapas 1–2 — Chuva, captação e demanda</h3>
            <p>Para cada dia <i>t</i>, o programa calcula a precipitação efetiva disponível e o volume captável:</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                P<sub>ef,t</sub> = max(0, P<sub>t</sub> − d<sub>f</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; V<sub>cap,t</sub> = A × C × P<sub>ef,t</sub>
                </code>
            </p>
            <p>Quando a regra de descarte inicial (<i>First Flush</i> — NBR 15527) está ativa no evento, o volume de descarte <code>d<sub>f</sub></code> (em mm) é subtraído da chuva bruta do dia, aproveitando integralmente o excedente efetivo. Como 1 mm sobre 1 m² equivale a 1 L, não há fator de conversão adicional. A demanda diária não potável é calculada por:</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                D<sub>pl,t</sub> = N × q × s
                </code>
            </p>
            <h3 style='color:#0369a1;'>Etapa 3 — Varredura de volumes e balanço diário</h3>
            <p>Cada volume candidato do reservatório inferior é simulado em todos os dias da série pelo modelo <i>yield after spillage</i> (YAS):</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                I<sub>t</sub> = min(V, S<sub>t−1</sub> + V<sub>cap,t</sub>) &nbsp;|&nbsp; O<sub>t</sub> = max(0, S<sub>t−1</sub> + V<sub>cap,t</sub> − V) &nbsp;|&nbsp; Y<sub>t</sub> = min(D<sub>pl,t</sub>, I<sub>t</sub>) &nbsp;|&nbsp; S<sub>t</sub> = I<sub>t</sub> − Y<sub>t</sub>
                </code>
            </p>
            <p>A ordem é relevante: o estoque é limitado e o extravasamento ocorre antes da retirada da demanda. Quando há reservatório superior, os ciclos de transferência são simulados explicitamente; a energia decorre do volume recalcado, partidas, vazão, potência e rendimento global. A varredura repete a mesma transição de estados para cada volume candidato.</p>
            <h3 style='color:#0369a1;'>Etapa 4 — Indicadores técnicos</h3>
            <p>O potencial de economia é calculado por:</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                E<sub>pot</sub> = 100 × [ Σ(consumo pluvial atendido) / Σ(demanda total de água) ]
                </code>
            </p>
            <p>O programa também informa dias com atendimento total, parcial e nulo, consumo pluvial anual, extravasamento médio e ganho marginal entre volumes consecutivos. O ótimo técnico é identificado após o limiar configurado de ganho marginal.</p>
            <h3 style='color:#0369a1;'>Etapa 5 — Avaliação econômica</h3>
            <p>CAPEX reúne reservatórios, motobomba quando aplicável, tubulações, filtros, mão de obra e custos ajustados pelo usuário. Os custos automáticos dos reservatórios são estimativas de triagem obtidas por interpolação linear por trechos da tabela interna explícita; estudos definitivos devem substituí-los por cotações locais datadas. Os outros custos operacionais preservam a semântica do Netuno 4: parcela fixa mais coeficiente opcional por m³ de água pluvial consumida no mês de incidência. A manutenção padrão é fixa, pois não existe um custo universal e cientificamente transferível por m³ de capacidade da cisterna.</p>
            <p>A economia anual bruta considera água potável e, quando aplicável, esgoto; dela são abatidos energia de recalque e O&amp;M. O valor presente líquido é calculado por:</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                VPL = −CAPEX + Σ [ FC<sub>t</sub> / (1 + i)<sup>t</sup> ]
                </code>
            </p>
            <p>A TIR é a taxa que zera o VPL; paybacks simples e descontado são os primeiros anos de fluxo acumulado nominal e descontado não negativo.</p>
            <h3 style='color:#0369a1;'>Etapa 6 — ACV simplificada</h3>
            <p>As emissões incorporadas são a soma da massa de cada componente pelo seu fator.</p>
            <p><code>CO2emb = Σ(mi × fi)</code></p>
            <p>As emissões operacionais são calculadas por:</p>
            <p><code>CO2op = E_bomba × f_rede + V_tratamento × f_tratamento</code></p>
            <p>Para a cloração, o cálculo detalhado é <code>m_Cl2,eq = V_pluvial × dose_aplicada / 1000</code>, em que o volume está em m³/ano e a dose em mg/L; sua contribuição é <code>CO2cloro = m_Cl2,eq × f_Cl2</code>. Trata-se de consumo teórico em cloro equivalente, não da demanda de cloro medida na água, que exige ensaio de qualidade e residual-alvo. São premissas editáveis de custo/ACV, não uma especificação de tratamento.</p>
            <p>As emissões evitadas são calculadas por:</p>
            <p><code>CO2evitado = V_água economizada × f_água potável</code></p>
            <p>O saldo de vida útil é:</p>
            <p><code>CO2líquido = CO2evitado − CO2emb − vida × CO2op</code></p>
            <p>Antes da varredura técnica, a interface deliberadamente apresenta resultados ambientais zerados.</p>
            <h3 style='color:#0369a1;'>Etapas 7–9 — Decisão e comunicação</h3>
            <p>A etapa 7 classifica as alternativas da varredura por TOPSIS, com critérios técnicos, econômicos e ambientais. A etapa 8 gera relatórios para stakeholders e pesquisa com as entradas, premissas e resultados calculados; a etapa 9 apresenta a documentação metodológica. Os documentos são apoio à decisão: projeto local, normas, faturas, orçamentos e quantitativos devem ser validados por responsável técnico.</p>
            """
        return self._create_browser(html, secao='metodologia')

    def create_tab_topsis_method(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🏆 Multi-Criteria Decision Analysis: TOPSIS & SMAA-VIKOR</h2>
            <p>Triton provides two complementary MCDA workflows: <b>TOPSIS</b> with declared/custom weight profiles, and <b>SMAA-VIKOR</b> with stochastic simulations across technical, economic, and environmental trade-offs.</p>

            <h3 style='color:#0369a1;'>1. TOPSIS (Deterministic Distance-to-Ideal)</h3>
            <p><b>TOPSIS</b> (<i>Technique for Order Preference by Similarity to Ideal Solution</i> — Hwang & Yoon, 1981) ranks candidate cisterns based on their geometric Euclidean proximity to the ideal positive solution (A⁺) and distance from the ideal negative solution (A⁻):</p>
            <p><code>C<sub>i</sub> = D<sub>i</sub><sup>−</sup> / (D<sub>i</sub><sup>+</sup> + D<sub>i</sub><sup>−</sup>)</code></p>
            <p>The relative closeness score <i>C<sub>i</sub></i> varies between 0.00 and 1.00. The alternative with highest <i>C<sub>i</sub></i> is ranked #1.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>1.1 Equal Weights vs. Custom Weight Profiles</h4>
            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 10px 14px; margin: 8px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.5;'>
                <p style='margin: 0 0 6px 0;'><b>• Equal Weights (Default Benchmark):</b> By default, TOPSIS assigns balanced 33.3% Technical, 33.3% Economic, and 33.4% Environmental weighting. This impartial baseline guarantees that no single dimension dominates without explicit stakeholder preference.</p>
                <p style='margin: 0 0 6px 0;'><b>• Dedicated Presets:</b> Presets allow prioritizing Economic (80% Financial / 10% Tech / 10% Env), Environmental (80% Environmental / 10% Tech / 10% Fin), or Technical (80% Technical / 10% Fin / 10% Env).</p>
                <p style='margin: 0;'><b>• Dynamic Real-Time Reactivity:</b> Adjusting weight spinboxes or presets triggers an immediate re-normalization of the decision matrix, recalculating scores, rankings, and the executive trade-off conclusion banner instantly.</p>
            </div>

            <h3 style='color:#0369a1;'>2. VIKOR (Compromise Engine Run by SMAA)</h3>
            <p><b>VIKOR</b> (Opricovic & Tzeng, 2004) determines the <i>compromise solution</i> by balancing group utility (majority benefit S) and individual regret (worst single criterion R):</p>
            <p><code>S<sub>i</sub> = Σ [ w<sub>j</sub> × (f<sub>j</sub><sup>*</sup> − x<sub>ij</sub>) / (f<sub>j</sub><sup>*</sup> − f<sub>j</sub><sup>−</sup>) ]</code></p>
            <p><code>R<sub>i</sub> = max<sub>j</sub> [ w<sub>j</sub> × (f<sub>j</sub><sup>*</sup> − x<sub>ij</sub>) / (f<sub>j</sub><sup>*</sup> − f<sub>j</sub><sup>−</sup>) ]</code></p>
            <p><code>Q<sub>i</sub> = v × (S<sub>i</sub> − S<sup>*</sup>) / (S<sup>−</sup> − S<sup>*</sup>) + (1 − v) × (R<sub>i</sub> − R<sup>*</sup>) / (R<sup>−</sup> − R<sup>*</sup>)</code></p>
            <p>Where <code>v ∈ [0, 1]</code> is the decision strategy weight (v = 0.50 balanced consensus; v > 0.50 majority rule; v < 0.50 veto/risk aversion).</p>

            <h3 style='color:#0369a1;'>3. SMAA-VIKOR (Stochastic Acceptability Analysis)</h3>
            <p>Combining <b>SMAA-2</b> (Lahdelma & Salminen, 2001) with <b>VIKOR</b> (as featured in the Python MCDA research library <code>crispyn</code>) removes the need for a single fixed profile: each simulation samples a weight vector and runs a new VIKOR ranking.</p>
            <ul>
                <li><b>Weight-Free Stochastic Sampling:</b> Generates thousands of Monte Carlo weight vectors <code>w ~ Dirichlet(1)</code> across the entire preference simplex <code>Σ w<sub>j</sub> = 1</code>.</li>
                <li><b>First-Rank Acceptability Index (b<sub>i</sub><sup>1</sup>):</b> Probability (%) that candidate tank <i>i</i> achieves the #1 compromise rank under any random decision-maker preference.</li>
                <li><b>Central Weight Vector (w<sub>i</sub><sup>c</sup>):</b> The typical centroid preference profile that justifies selecting alternative <i>i</i>.</li>
                <li><b>Confidence Factor (p<sub>i</sub><sup>c</sup>):</b> Reliability probability that alternative <i>i</i> remains optimal when preferences are close to its central weight vector.</li>
            </ul>

            <h3 style='color:#0369a1;'>4. Fidelity to the published formulations</h3>
            <p>Three notes on how this implementation relates to the published formulations, so that results can be compared with other software on equal terms.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.1 Normalisation adopted</h4>
            <p>Hwang &amp; Yoon normalise each column by its Euclidean norm. Net present value, however, is routinely negative, and vector normalisation over signed values does not preserve the ordering the method assumes. This engine therefore <b>translates each criterion by its own minimum before normalising</b>:</p>
            <p><i>r<sub>ij</sub> = (x<sub>ij</sub> − min<sub>i</sub> x<sub>ij</sub>) / √( Σ<sub>i</sub> (x<sub>ij</sub> − min<sub>i</sub> x<sub>ij</sub>)² )</i></p>
            <p>Where every value of a criterion is positive and its minimum is zero, this reduces to the canonical form. Where negative values occur, the two differ, so closeness scores should be compared only against runs using the same normalisation.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.2 Scope of the VIKOR ranking</h4>
            <p>Opricovic &amp; Tzeng propose the compromise solution subject to two conditions: <b>C1</b>, acceptable advantage, and <b>C2</b>, acceptable stability in decision making; when either fails, the method returns a set of compromise solutions rather than a single one. This engine ranks by <i>Q</i> without evaluating those conditions, so the VIKOR output is an ordering of alternatives. The stochastic analysis in section 3 addresses the same concern by other means, reporting how often each alternative holds first place across the preference space.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.3 Reference implementations and criteria</h4>
            <p>The SMAA-VIKOR here follows the design of the <code>crispyn</code> library (Aleksandra Bączkiewicz, MIT licence), which implements <code>VIKOR</code> and <code>VIKOR_SMAA</code>. Triton's version is an <b>independent implementation</b> written directly on NumPy; the repository serves as a comparison baseline, not as the origin of this code. Note that <code>crispyn</code> does <b>not</b> implement TOPSIS, so it is not the reference for section 1.</p>
            <p>The seven criteria evaluated are: potable water savings, overflow, net present value, discounted payback, internal rate of return, life-cycle CO₂ and potable water consumed. Weights may be supplied as three pillar weights, apportioned within each pillar, or as seven individual weights.</p>
            """
        else:
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🏆 Decisão Multicritério: TOPSIS & SMAA-VIKOR</h2>
            <p>O Triton oferece dois fluxos complementares de decisão multicritério (MCDA): <b>TOPSIS</b> com perfil de pesos declarado (ou customizado) e <b>SMAA-VIKOR</b> com milhares de simulações estocásticas no simplex de preferências.</p>

            <h3 style='color:#0369a1;'>1. TOPSIS (Distância Geométrica aos Ideais)</h3>
            <p>O <b>TOPSIS</b> (<i>Technique for Order Preference by Similarity to Ideal Solution</i> — Hwang & Yoon, 1981) classifica as alternativas com base na proximidade euclidiana à solução ideal positiva (A⁺) e no afastamento da solução ideal negativa (A⁻):</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                C<sub>i</sub> = D<sub>i</sub><sup>−</sup> / (D<sub>i</sub><sup>+</sup> + D<sub>i</sub><sup>−</sup>)
                </code>
            </p>
            <p>O escore relativo de proximidade <i>C<sub>i</sub></i> varia de 0,00 a 1,00. A alternativa de maior score é classificada em 1º lugar (Rank #1).</p>

            <h4 style='color:#0369a1; margin-top:12px;'>1.1 Pesos Iguais (Equilibrado) vs. Pesos Ponderados Personalizados</h4>
            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 8px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0;'><b>• Pesos Iguais (Perfil Padrão — 33,3% Técnico, 33,3% Econômico, 33,4% Ambiental):</b> Por padrão, o TOPSIS inicia com ponderação equitativa entre os três pilares da sustentabilidade, garantindo neutralidade técnica e impedindo que a dimensão econômica ou hídrica mascare os impactos ambientais.</p>
                <p style='margin: 0 0 6px 0;'><b>• Presets Temáticos:</b> O projetista pode optar rapidamente por perfis pré-definidos: <i>Econômico</i> (80% Financeiro / 10% Técnico / 10% Ambiental), <i>Ambiental</i> (80% Ambiental / 10% Técnico / 10% Financeiro) ou <i>Técnico</i> (80% Técnico / 10% Financeiro / 10% Ambiental).</p>
                <p style='margin: 0 0 6px 0;'><b>• Reatividade e Atualização Imediata:</b> Conforme o usuário digita ou altera qualquer peso nos campos numéricos, o Triton recalcula instantaneamente as distâncias euclidianas, atualiza o ranking da tabela, ajusta os gráficos de proximidade e reflete dinamicamente na conclusão textual se a recomendação decorre de <b>pesos iguais</b> ou dos <b>pesos ponderados específicos</b> adotados.</p>
            </div>

            <h3 style='color:#0369a1;'>2. VIKOR (Motor de Compromisso Executado pelo SMAA)</h3>
            <p>O <b>VIKOR</b> (Opricovic & Tzeng, 2004) identifica a <i>solução de compromisso</i> ponderando a utilidade coletiva da maioria (S) contra o arrependimento máximo individual (R):</p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                S<sub>i</sub> = Σ [ w<sub>j</sub> × (f<sub>j</sub><sup>*</sup> − x<sub>ij</sub>) / (f<sub>j</sub><sup>*</sup> − f<sub>j</sub><sup>−</sup>) ] &nbsp;|&nbsp; R<sub>i</sub> = max<sub>j</sub> [ w<sub>j</sub> × (f<sub>j</sub><sup>*</sup> − x<sub>ij</sub>) / (f<sub>j</sub><sup>*</sup> − f<sub>j</sub><sup>−</sup>) ]
                </code>
            </p>
            <p>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                Q<sub>i</sub> = v × (S<sub>i</sub> − S<sup>*</sup>) / (S<sup>−</sup> − S<sup>*</sup>) + (1 − v) × (R<sub>i</sub> − R<sup>*</sup>) / (R<sup>−</sup> − R<sup>*</sup>)
                </code>
            </p>
            <p>Onde <code>v ∈ [0, 1]</code> é o parâmetro de estratégia de consenso (v = 0,50 consenso equilibrado; v &gt; 0,50 regra da maioria; v &lt; 0,50 aversão ao risco/veto individual).</p>

            <h3 style='color:#0369a1;'>3. SMAA-VIKOR (Análise Estocástica de Aceitabilidade de Compromisso)</h3>
            <p>O modelo híbrido <b>SMAA-VIKOR</b> (baseado no algoritmo da biblioteca científica <code>crispyn</code> e em Lahdelma & Salminen, 2001) elimina a subjetividade de um perfil único: cada simulação de Monte Carlo sorteia um vetor de pesos uniforme no simplex e calcula um ranking VIKOR completo.</p>
            <ul style='font-size: 12.5px; line-height: 1.6; color: #334155;'>
                <li><b>Exploração Estocástica do Espaço de Pesos:</b> Amostra milhares de combinações de pesos no <i>simplex</i> <code>Σ w<sub>j</sub> = 1</code> via distribuição de Dirichlet simétrica.</li>
                <li><b>Índice de Aceitabilidade de 1º Lugar (b<sub>i</sub><sup>1</sup>):</b> Probabilidade estatística (%) da cisterna <i>i</i> ser a solução de compromisso número 1 diante de qualquer preferência de decisor.</li>
                <li><b>Vetor Central de Pesos (w<sub>i</sub><sup>c</sup>):</b> Vetor baricêntrico de preferências que justificaria a escolha daquela cisterna específica.</li>
                <li><b>Fator de Confiança (p<sub>i</sub><sup>c</sup>):</b> Grau de estabilidade da alternativa quando as preferências reais do decisor gravitam em torno do seu vetor central.</li>
            </ul>

            <h3 style='color:#0369a1;'>4. Fidelidade às formulações publicadas</h3>
            <p>Três notas sobre a relação entre esta implementação e as formulações publicadas, para que os resultados possam ser comparados com os de outros programas em igualdade de condições.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.1 Normalização adotada</h4>
            <p>Hwang &amp; Yoon normalizam cada coluna pela norma euclidiana. O valor presente líquido, porém, é rotineiramente negativo, e a normalização vetorial sobre valores com sinal não preserva a ordenação que o método pressupõe. Este motor, portanto, <b>translada cada critério pelo seu próprio mínimo antes de normalizar</b>:</p>
            <p><i>r<sub>ij</sub> = (x<sub>ij</sub> − mín<sub>i</sub> x<sub>ij</sub>) / √( Σ<sub>i</sub> (x<sub>ij</sub> − mín<sub>i</sub> x<sub>ij</sub>)² )</i></p>
            <p>Onde todos os valores de um critério são positivos e o mínimo é zero, isso se reduz à forma canônica. Havendo valores negativos, as duas diferem, de modo que os escores de proximidade devem ser comparados apenas com execuções que usem a mesma normalização.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.2 Alcance do ranking VIKOR</h4>
            <p>Opricovic &amp; Tzeng propõem a solução de compromisso sujeita a duas condições: <b>C1</b>, vantagem aceitável, e <b>C2</b>, estabilidade aceitável na decisão; falhando qualquer uma, o método devolve um conjunto de soluções de compromisso em vez de uma só. Este motor ordena por <i>Q</i> sem avaliar essas condições, de modo que a saída do VIKOR é uma ordenação de alternativas. A análise estocástica da seção 3 trata da mesma preocupação por outro caminho, ao informar com que frequência cada alternativa ocupa o primeiro lugar ao longo do espaço de preferências.</p>

            <h4 style='color:#0369a1; margin-top:12px;'>4.3 Implementações de referência e critérios</h4>
            <p>O SMAA-VIKOR daqui segue o desenho da biblioteca <code>crispyn</code> (Aleksandra Bączkiewicz, licença MIT), que implementa <code>VIKOR</code> e <code>VIKOR_SMAA</code>. A versão do Triton é uma <b>implementação independente</b>, escrita diretamente sobre NumPy; o repositório serve de base de comparação, não de origem deste código. Note que <code>crispyn</code> <b>não</b> implementa TOPSIS, de modo que não é a referência da seção 1.</p>
            <p>Os sete critérios avaliados são: potencial de economia de água potável, extravasamento, valor presente líquido, payback descontado, taxa interna de retorno, CO₂ de ciclo de vida e água potável consumida. Os pesos podem ser informados como três pesos por pilar, rateados dentro de cada um, ou como sete pesos individuais.</p>
            """
        return self._create_browser(html, secao='topsis')

    def create_tab_acv_justifications(self) -> QWidget:
        """Capítulo único de ACV: reúne inventário, equações, premissas e referências."""
        if get_current_lang() != "pt":
            introduction = """
            <h2 style='color:#0284c7; margin-top:0;'>🍃 Life-Cycle Assessment (LCA): Assumptions and Rationale</h2>
            <p>This chapter documents the simplified LCA inventory used by Triton. It separates <b>embodied impacts</b> (tanks, pipes and pump), <b>operational impacts</b> (electricity and treatment), and the <b>avoided potable-water impact</b>. Default factors are transparent, editable starting assumptions—not a substitute for an EPD, supplier declaration, or local inventory.</p>
            <h3 style='color:#0369a1;'>Calculation chain and interpretation</h3>
            <p>For each component, the embodied impact is calculated by:</p>
            <p><code>CO2emb = quantity × emission factor</code></p>
            <p>Over the selected lifetime, operational impact is calculated by:</p>
            <p><code>CO2op = lifetime × (pump energy × grid factor + treated volume × treatment factor)</code></p>
            <p>For chlorination, Triton reports <code>m_Cl2 = V_rainwater × dose_Cl2 / 1000</code> and calculates <code>CO2chlorine = m_Cl2 × f_Cl2</code>. Dose (mg/L) and the chlorine emission factor (kg CO2e/kg Cl2) are editable LCA assumptions; they are not a prescription for water-quality treatment.</p>
            <p>Avoided impact is calculated by:</p>
            <p><code>CO2avoid = saved potable water × potable-water factor</code></p>
            <p><b>Carbon Accounting Convention & Color Coding:</b></p>
            <ul>
                <li><b>Atmospheric Emissions are POSITIVE (+) in RED:</b> Initial embodied emissions from tanks, pipes, and pumps, plus operational emissions from electricity (pumping) and chlorination inputs.</li>
                <li><b>Avoided / Removed Carbon is NEGATIVE (−) in GREEN:</b> Displaced municipal water treatment and pumping avoids GHG emissions, functioning as an ecological carbon offset.</li>
                <li><b>20-Year Net Climate Balance:</b> <code>Net Balance = (CO2emb + CO2op) − CO2avoid</code>. A <b>negative (−)</b> final balance represents net carbon abatement/removal from the atmosphere (highlighted in <b>green</b>). A <b>positive (+)</b> balance indicates net carbon addition (highlighted in <b>red</b>).</li>
                <li><b>Eco-Payback:</b> <code>Payback (years) = CO2emb / (CO2avoid,annual − CO2op,annual)</code>.</li>
            </ul>
            <p><b>How to use this section:</b> first check quantities (material, tank volume, pipe lengths and pump power), then validate factors and sources, and finally test sensitivity using local suppliers, grid mix and service life. Piping adopts a baseline estimate of 5m suction and 20m discharge, sized automatically by pump hydraulics.</p>
            """
        else:
            introduction = """
            <h2 style='color:#0284c7; margin-top:0;'>🍃 Análise do Ciclo de Vida (ACV): Premissas e Justificativas</h2>
            <p>Este capítulo documenta o inventário da ACV simplificada adotada pelo Triton. Ele separa <b>impactos incorporados</b> (reservatórios, tubulações e motobomba), <b>impactos operacionais</b> (eletricidade e tratamento) e o <b>impacto evitado da água potável</b>. Os fatores padrão são premissas iniciais transparentes e editáveis, não substituem EPD, declaração do fornecedor ou inventário local.</p>
            <h3 style='color:#0369a1;'>Cadeia de cálculo e convenção de sinais</h3>
            <p>Para cada componente físico, a pegada de carbono incorporada de fabricação é calculada por:</p>
            <p><code>CO2incorporado = quantidade × fator de emissão (+ kg CO2e)</code></p>
            <p>Na vida útil definida (20 anos padrão), o impacto operacional de bombeamento e cloração é calculado por:</p>
            <p><code>CO2operacional = vida × (energia da bomba × fator da rede + volume tratado × fator de tratamento) (+ kg CO2e)</code></p>
            <p>Para a cloração, o Triton computa <code>m_Cl2 = V_pluvial × dose_Cl2 / 1000</code> e calcula <code>CO2cloro = m_Cl2 × f_Cl2</code>. A dose (mg/L) e o fator de emissão do cloro (kg CO2e/kg Cl2) são premissas editáveis de ACV; não são uma prescrição sanitária de tratamento da água.</p>
            <p>O impacto evitado da rede pública de distribuição de água potável é calculado por:</p>
            <p><code>CO2evitado = água potável economizada × fator da concessionária (− kg CO2e)</code></p>
            
            <div style='background-color: #f8fafc; border-left: 4px solid #059669; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0; font-weight: bold; color: #047857;'>Convenção Rigorosa de Balanço de Carbono e Código de Cores:</p>
                <p style='margin: 0 0 4px 0;'>• <b>Carbono Emitido para a Atmosfera:</b> Valor <b>POSITIVO (+)</b> associado à cor <b>VERMELHA</b> (impacto ambiental/ruim). Engloba a fabricação da cisterna, caixa d'água, tubos, motobomba, eletricidade de rede e desinfecção química.</p>
                <p style='margin: 0 0 4px 0;'>• <b>Carbono Retirado / Evitado da Atmosfera:</b> Valor <b>NEGATIVO (−)</b> associado à cor <b>VERDE</b> (benefício ecológico/bom). Engloba a substituição da água potável que deixa de ser captada, tratada e recalcada pela concessionária.</p>
                <p style='margin: 0 0 4px 0;'>• <b>Saldo Líquido Acumulado em 20 Anos:</b> <code>Saldo Líquido = (CO2incorporado + CO2operacional) − CO2evitado</code>. Um resultado <b>negativo (−)</b> expressa que o sistema retirou líquido mais carbono da atmosfera do que emitiu para existir (mitigação líquida positiva, em verde). Um resultado positivo (+) aponta pegada líquida de carbono (em vermelho).</p>
                <p style='margin: 0;'>• <b>Payback Ecológico:</b> <code>T_pb = CO2incorporado / (CO2evitado_anual − CO2operacional_anual)</code>. Determina o número de anos de operação necessários para neutralizar as emissões incorporadas nos materiais.</p>
            </div>

            <p><b>Como usar esta seção:</b> primeiro verifique quantitativos (materiais, volumes, tubulações de 5m sucção / 20m recalque e potência da motobomba), depois valide fatores e fontes e, por fim, faça uma análise de sensibilidade com fornecedores, matriz elétrica e vida útil locais.</p>
            """

        sections = [
            generate_html_justifications_materials(),
            generate_html_justifications_pipes(),
            generate_html_justifications_pumps(),
            generate_html_justifications_operational(),
        ]
        separator = "<hr style='border:0; border-top:2px solid #cbd5e1; margin:24px 0;'/>"
        return self._create_browser(introduction + separator.join(sections), secao='acv')

    def create_tab_esg_certifications(self) -> QWidget:
        """Capítulo de Certificações Ambientais e Critérios ESG (LEED, AQUA, Casa Azul, GRI 303)."""
        if get_current_lang() != "pt":
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🌿 Sustainable Certifications & ESG Criteria (LEED, AQUA-HQE, Casa Azul, GRI)</h2>
            <p style='font-size: 13px; line-height: 1.6;'>
                Rainwater harvesting in buildings is a high-impact strategy for global green building certification and ESG corporate sustainability reporting. 
                Triton integrates the daily Yield-After-Spill (YAS) water balance results with the technical criteria of four major sustainability frameworks:
                <b>LEED v4/v4.1</b>, <b>Processo AQUA-HQE</b>, <b>Selo Casa Azul CAIXA</b>, <b>EDGE</b>, and <b>GRI Standard 303</b>.
            </p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px;'>1. LEED v4 and v4.1 (USGBC / GBC Brasil) — Water Efficiency (WE) Category</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The USGBC LEED v4 BD+C standard allocates points based on water demand reduction compared to an ASHRAE/EPAct compliant baseline building:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>WEp1 (Water Efficiency Prerequisite 1 — Mandatory):</b> Buildings must achieve a mandatory minimum reduction of <b>20%</b> in indoor potable water consumption. <i>Prerequisites award 0 points</i>.</li>
                <li><b>WEc1 (Outdoor Water Use Reduction — 0 to 2 points):</b> Evaluates eliminating or reducing potable water consumption for landscape irrigation:
                    <br/>• <b>No outdoor demand (0 m³/year or no landscaping):</b> <b>0 points</b> (projects without outdoor water demand cannot score outdoor efficiency points).
                    <br/>• <b>≥ 50% irrigation reduction</b> via rainwater: <b>1 point</b>.
                    <br/>• <b>100% irrigation reduction (no potable water for irrigation):</b> <b>2 points</b> (Maximum).
                </li>
                <li><b>WEc2 (Indoor Water Use Reduction — 1 to 6 points):</b> Awards points according to the official LEED v4 BD+C scale for potable water replaced by alternative non-potable sources (toilets, urinals, cooling, laundry):
                    <br/>• <b>25% savings:</b> 1 point &nbsp;|&nbsp; <b>30%:</b> 2 points &nbsp;|&nbsp; <b>35%:</b> 3 points
                    <br/>• <b>40% savings:</b> 4 points &nbsp;|&nbsp; <b>45%:</b> 5 points &nbsp;|&nbsp; <b>≥ 50% savings:</b> 6 points (Maximum credit score).
                </li>
            </ul>
            <div style='background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px 14px; border-radius: 4px; margin: 10px 0;'>
                <b>Total LEED WE Potential:</b> Rainwater harvesting can unlock up to <b>8 direct points</b> in the Water Efficiency category (2 pts outdoor + 6 pts indoor), decisive for Silver (50 pts), Gold (60 pts), or Platinum (80+ pts) certifications.
            </div>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>2. LEED v5 BD+C — WEc2 Enhanced Water Efficiency</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                LEED v5 reorganised water efficiency: the two separate v4 credits — outdoor and indoor use — became a single credit,
                <b>WEc2 Enhanced Water Efficiency</b>, worth <b>1 to 8 points</b> in New Construction and 1 to 7 in Core and Shell. Projects may still register
                under v4 and v4.1 until <b>30 June 2027</b>, which is why both versions appear on this page.
            </p>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The rule that most changes the calculation is this: a project either follows Option 1, which measures the whole project, <b>or</b> combines Options 2 to 6 — never both.
                Triton evaluates both paths and reports the better result, because the choice depends on data the programme does not hold, such as process water use.
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>Option 1 — Whole-project water use (1 to 8 points):</b> reduction measured against the project baseline.
                    <br/>• 30%: 1 pt &nbsp;|&nbsp; 35%: 2 &nbsp;|&nbsp; 40%: 3 &nbsp;|&nbsp; 45%: 4 &nbsp;|&nbsp; 50%: 5 &nbsp;|&nbsp; 55%: 6 &nbsp;|&nbsp; 60%: 7 &nbsp;|&nbsp; 65%: 8.
                    <br/>• <b>With an alternative water source — which is what rainwater harvesting is — each band is worth one extra point</b>, capped at 8. The 65% band with an alternative
                    source is treated by the rating system as exemplary performance rather than a point under this credit, and the programme does not count it.
                </li>
                <li><b>Option 2 — Fixtures and fittings, calculated reduction (1 to 3 points):</b> 30%: 1 pt &nbsp;|&nbsp; 35%: 2 &nbsp;|&nbsp; 40%: 3, measured above the WEp2 prerequisite.</li>
                <li><b>Option 4 — Outdoor water use (1 to 2 points):</b> Path 1 awards 2 points to a project with no permanent irrigation. Path 2 reduces the theoretical irrigation requirement (TIR):
                    50%: 1 pt &nbsp;|&nbsp; 100%: 2 pts. This is where rainwater sent to irrigation in the daily balance enters.
                </li>
                <li><b>Option 6 — Water reuse (1 to 2 points):</b> Path 1 awards 1 point for a reuse-ready system; <b>Path 2 awards 2 points for an alternative-water system that actually serves
                    one or more end uses</b> — irrigation, flushing, make-up or process. The programme treats the rainwater harvesting system as this path.
                </li>
            </ul>
            <div style='background-color: #fffbeb; border-left: 4px solid #d97706; padding: 10px 14px; border-radius: 4px; margin: 10px 0;'>
                <b>What the programme does not assess.</b> Options 3 and 5 cover appliances, cooling towers and process water, which sit outside Triton's water balance.
                Core and Shell has its own bands, not the ones used here. The score is a <b>screening estimate</b> derived from the daily simulation: credit documentation
                requires the project baseline model, produced by the certification team.
            </div>
            <p style='font-size: 11.5px; line-height: 1.5; color: #64748b;'>
                Source: <i>LEED v5 Reference Guide for Building Design and Construction</i>, November 2025 Edition (USGBC), credit WEc2, Tables 1, 2 and 7.
            </p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>3. AQUA-HQE Residential (Fundação Vanzolini / CERQUAL) — Water Consumption theme</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                In the residential reference framework, version 00 of 22 November 2024, water is assessed item by item, each classified as prerequisite (PR), HQE, HQE 2 or HQE 3. Three items concern rainwater harvesting:
            </p>
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; font-size: 12px; margin-top: 8px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='center' width='16%'>Item</th>
                    <th align='center' width='14%'>Level</th>
                    <th align='left'>Requirement</th>
                </tr>
                <tr><td align='center'><b>EAU.1.2</b></td><td align='center'>HQE</td><td>At least 20% reduction in potable water consumption against the reference consumption.</td></tr>
                <tr style='background-color: #f8fafc;'><td align='center'><b>EAU.1.3</b></td><td align='center'>HQE 3</td><td>40% potable water saving in the development.</td></tr>
                <tr><td align='center'><b>EAU.1.5</b></td><td align='center'>HQE 3</td><td>Rainwater recovery system complying with ABNT NBR 15527 and NBR 16783.</td></tr>
            </table>
            <p style='font-size: 12px; color: #64748b;'>The framework measures savings against the reference scenario of the Fundação Vanzolini auxiliary spreadsheet, which also counts water-saving fixtures: Triton's percentage is indicative. Earlier versions of Triton used "Base / Boas Práticas / Excelente" profiles at 10, 25 and 40%, which the 2024 framework does not contain.</p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>4. Selo Casa Azul + CAIXA — Criterion 3.6: Rainwater Harvesting</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                In the guide version V023 of 29 April 2026, the indicator is the <b>existence</b> of a rainwater harvesting system (catchment, treatment, storage and points of use), not a savings percentage. Points depend on the scope of use:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>Common areas:</b> 2 points (houses in subdivisions with the required provisions: 2 points).</li>
                <li><b>Housing units:</b> 4 points.</li>
                <li><b>Housing units and common areas:</b> 5 points. Mandatory for the Diamante level.</li>
            </ul>
            <p style='font-size: 12px; color: #64748b;'>For single houses, the Selo Casa Azul Uni guide (V001, December 2025) awards 1 point under criterion 7, mandatory for the Ouro seal. Earlier versions of Triton graded "Prata / Ouro / Diamante" at 10, 20 and 30% savings, which the guide does not contain.</p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>5. GRI Standard 303 (Global Reporting Initiative) & Water Circularity</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Provides standardized corporate disclosure metrics for ESG and sustainability reports:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>GRI 303-3 (Water Withdrawal Saved):</b> Volume of treated municipal water avoided (m³/year and 20-year cumulative).</li>
                <li><b>GRI 303-5 (Water Positive Ratio):</b> Percentage of circular on-site water utilization:
                    <br/><code>Water Positive Ratio = (Annual Rainwater Harvested / Total Annual Water Demand) × 100%</code>.
                </li>
            </ul>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>6. EDGE (IFC / World Bank Group) &mdash; the Water Bar</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                EDGE is the only standard on this list that <b>awards no points</b>. It measures the
                percentage of savings against a <i>local base case</i> along three independent bars
                &mdash; energy, water, and embodied energy in materials &mdash; and requires each one to
                cross its threshold:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>EDGE Certified:</b> at least <b>20%</b> savings in energy, water and embodied energy in materials.</li>
                <li><b>EDGE Advanced (Zero Carbon Ready):</b> EDGE Certified plus <b>40%</b> or more on-site energy savings.</li>
                <li><b>Zero Carbon:</b> EDGE Advanced plus 100% renewables, on-site or off-site, or purchased offsets.</li>
            </ul>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Rainwater harvesting is measure <b>WEM14</b>, whose input in the EDGE App is the
                <b>catchment area in m&sup2;</b>. Triton reports the contribution of that single measure
                to the water bar, together with the catchment area to declare.
            </p>
            <div style='background-color: #fffbeb; border-left: 4px solid #b45309; padding: 10px 14px; border-radius: 4px; margin: 10px 0; font-size: 12.5px;'>
                <b>What Triton cannot know.</b> The base case is local: it varies by country and
                building type and is set by the EDGE App itself. Without a declared base case, Triton
                uses the project's own modelled demand, which is a floor rather than the certification
                figure &mdash; a project that also installs efficient fixtures has a higher base case.
                <b>Certification comes from the EDGE App, not from here.</b>
            </div>
            <p style='font-size: 11.5px; color: #64748b;'>
                Source: IFC, <i>EDGE Certification Process</i>, edgebuildings.com/certify/certification/,
                accessed 10 September 2026. Measure codes checked against a certified EDGE v3.0.0
                assessment report.
            </p>
            """
        else:
            html = """
            <h2 style='color:#0284c7; margin-top:0;'>🌿 Certificações Sustentáveis & Critérios ESG (LEED, AQUA-HQE, Casa Azul, GRI)</h2>
            <p style='font-size: 13px; line-height: 1.6;'>
                O aproveitamento de água de chuva em edificações constitui uma das estratégias de maior peso para obtenção de selos sustentáveis e elaboração de relatórios corporativos ESG. 
                O <b>Triton</b> traduz os resultados da simulação hidrológica diária contínua (modelo YAS) em pontuações e enquadramentos auditáveis em quatro referenciais líderes:
                <b>LEED v4/v4.1</b>, <b>Processo AQUA-HQE</b>, <b>Selo Casa Azul CAIXA</b>, <b>EDGE</b> e <b>GRI Standard 303</b>.
            </p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px;'>1. LEED v4 e v4.1 (USGBC / GBC Brasil) — Categoria Water Efficiency (WE)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                A certificação LEED v4 BD+C pontua a redução no consumo de água potável em comparação ao edifício basal padrão (fixtures regulamentados pela EPAct/ASHRAE):
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>Pré-requisito Obrigatório WEp1 (Indoor Water Use Reduction):</b> Exige redução basal mínima de <b>20%</b> no consumo interno de água potável. <i>Pré-requisitos são mandatórios e não atribuem pontos</i>.</li>
                <li><b>Crédito WEc1 — Redução do Uso Externo de Água (0 a 2 pontos):</b> Avalia a substituição de água potável na irrigação paisagística:
                    <br/>• <b>Sem demanda externa (0 m³/ano ou ausência de áreas irrigadas):</b> <b>0 pontos</b> (o projeto não pontua neste crédito caso não possua demanda externa para reduzir).
                    <br/>• <b>≥ 50% de redução na irrigação</b> com água pluvial: <b>1 ponto</b>.
                    <br/>• <b>100% de redução na irrigação (zero água potável externa):</b> <b>2 pontos</b> (Pontuação Máxima).
                </li>
                <li><b>Crédito WEc2 — Redução do Uso Interno de Água (1 a 6 pontos):</b> Concede pontos conforme a escala oficial do LEED v4 BD+C para a economia interna com fontes alternativas (bacias sanitárias, mictórios, lavanderia e torres de resfriamento):
                    <br/>• <b>25% de economia:</b> 1 ponto &nbsp;|&nbsp; <b>30%:</b> 2 pontos &nbsp;|&nbsp; <b>35%:</b> 3 pontos
                    <br/>• <b>40% de economia:</b> 4 pontos &nbsp;|&nbsp; <b>45%:</b> 5 pontos &nbsp;|&nbsp; <b>≥ 50% de economia:</b> 6 pontos (Pontuação Máxima do crédito).
                </li>
            </ul>
            <div style='background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px 14px; border-radius: 4px; margin: 10px 0;'>
                <b>Potencial Total LEED WE:</b> O sistema pluvial habilita até <b>8 pontos diretos</b> na categoria de Eficiência Hídrica (2 pts externos + 6 pts internos), determinantes para a obtenção dos níveis Prata (50 pts), Ouro (60 pts) ou Platina (80+ pts).
            </div>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>2. LEED v5 BD+C — WEc2 Enhanced Water Efficiency</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O LEED v5 reorganizou a eficiência hídrica: os dois créditos separados do v4 — uso externo e uso interno — deram lugar a um crédito único,
                <b>WEc2 Enhanced Water Efficiency</b>, de <b>1 a 8 pontos</b> em New Construction e de 1 a 7 em Core and Shell. O v4 e o v4.1 continuam aceitando
                registro de projetos até <b>30/06/2027</b>, e por isso as duas versões convivem nesta aba.
            </p>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                A regra que mais muda o cálculo é esta: o projeto <b>ou</b> segue a Opção 1, que mede o projeto inteiro, <b>ou</b> combina as Opções 2 a 6 — nunca as duas.
                O Triton avalia os dois caminhos e informa o melhor resultado, porque a escolha depende de dados que o programa não conhece, como o consumo de processo.
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>Opção 1 — Uso de água do projeto inteiro (1 a 8 pontos):</b> a redução é medida contra a linha de base do projeto.
                    <br/>• 30%: 1 pt &nbsp;|&nbsp; 35%: 2 &nbsp;|&nbsp; 40%: 3 &nbsp;|&nbsp; 45%: 4 &nbsp;|&nbsp; 50%: 5 &nbsp;|&nbsp; 55%: 6 &nbsp;|&nbsp; 60%: 7 &nbsp;|&nbsp; 65%: 8.
                    <br/>• <b>Com fonte alternativa de água — que é o caso do aproveitamento pluvial — cada faixa vale um ponto a mais</b>, até o teto de 8. A faixa de 65% com fonte alternativa
                    é tratada pelo referencial como desempenho exemplar, e não como ponto deste crédito; o programa não a contabiliza.
                </li>
                <li><b>Opção 2 — Louças e metais, redução calculada (1 a 3 pontos):</b> 30%: 1 pt &nbsp;|&nbsp; 35%: 2 &nbsp;|&nbsp; 40%: 3, medidos acima do pré-requisito WEp2.</li>
                <li><b>Opção 4 — Uso externo (1 a 2 pontos):</b> o Caminho 1 dá 2 pontos ao projeto sem irrigação permanente. O Caminho 2 reduz o requisito teórico de irrigação (TIR):
                    50%: 1 pt &nbsp;|&nbsp; 100%: 2 pts. É por aqui que entra a água de chuva destinada à irrigação no balanço diário.
                </li>
                <li><b>Opção 6 — Reúso de água (1 a 2 pontos):</b> o Caminho 1 dá 1 ponto ao sistema preparado para reúso; o <b>Caminho 2 dá 2 pontos ao sistema de fontes alternativas
                    que de fato atenda um ou mais usos finais</b> — irrigação, descargas, reposição ou processo. O programa trata o sistema de aproveitamento pluvial como esse caminho.
                </li>
            </ul>
            <div style='background-color: #fffbeb; border-left: 4px solid #d97706; padding: 10px 14px; border-radius: 4px; margin: 10px 0;'>
                <b>O que o programa não avalia.</b> As Opções 3 e 5 tratam de equipamentos, torres de resfriamento e água de processo, que estão fora do balanço hídrico do Triton.
                As faixas do Core and Shell são próprias e não são as usadas aqui. A pontuação é uma <b>estimativa de triagem</b> a partir da simulação diária: a documentação
                do crédito exige a modelagem de linha de base do projeto, feita pela equipe de certificação.
            </div>
            <p style='font-size: 11.5px; line-height: 1.5; color: #64748b;'>
                Referencial: <i>LEED v5 Reference Guide for Building Design and Construction</i>, edição de novembro de 2025 (USGBC), crédito WEc2, Tabelas 1, 2 e 7.
            </p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>3. AQUA-HQE Residencial (Fundação Vanzolini / CERQUAL) — Tema Consumo de Água</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                No referencial de edifícios residenciais, versão 00 de 22 de novembro de 2024, a água é avaliada por itens, cada um classificado como pré-requisito (PR), HQE, HQE 2 ou HQE 3. Três itens tratam do aproveitamento pluvial:
            </p>
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; font-size: 12px; margin-top: 8px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='center' width='16%'>Item</th>
                    <th align='center' width='14%'>Nível</th>
                    <th align='left'>Exigência</th>
                </tr>
                <tr><td align='center'><b>EAU.1.2</b></td><td align='center'>HQE</td><td>Redução de pelo menos 20% do consumo de água potável em relação ao consumo de referência.</td></tr>
                <tr style='background-color: #f8fafc;'><td align='center'><b>EAU.1.3</b></td><td align='center'>HQE 3</td><td>Economia de 40% de água potável no empreendimento.</td></tr>
                <tr><td align='center'><b>EAU.1.5</b></td><td align='center'>HQE 3</td><td>Sistema de recuperação de águas pluviais conforme as ABNT NBR 15527 e NBR 16783.</td></tr>
            </table>
            <p style='font-size: 12px; color: #64748b;'>O referencial mede a economia contra o cenário de referência da planilha auxiliar da Fundação Vanzolini, que soma também os dispositivos economizadores: o percentual do Triton é indicativo. Versões anteriores do programa usavam perfis «Base / Boas Práticas / Excelente» a 10, 25 e 40%, que o referencial de 2024 não contém.</p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>4. Selo Casa Azul + CAIXA — Critério 3.6: Aproveitamento de Águas Pluviais</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                No guia versão V023, de 29 de abril de 2026, o indicador é a <b>existência</b> de sistema de aproveitamento de águas pluviais (captação, tratamento, reservação e pontos de uso), e não um percentual de economia. A pontuação depende da abrangência do uso:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>Áreas comuns:</b> 2 pontos (casas em loteamento com a preparação exigida: 2 pontos).</li>
                <li><b>Unidades habitacionais:</b> 4 pontos.</li>
                <li><b>Unidades habitacionais e áreas comuns:</b> 5 pontos. Obrigatório para o nível Diamante.</li>
            </ul>
            <p style='font-size: 12px; color: #64748b;'>Para a unidade isolada, o guia Selo Casa Azul Uni (V001, dezembro de 2025) atribui 1 ponto no critério 7, obrigatório para o Selo Ouro. Versões anteriores do programa graduavam «Prata / Ouro / Diamante» a 10, 20 e 30% de economia, que o guia não contém.</p>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>5. GRI Standard 303 (Global Reporting Initiative) & Pegada Hídrica Positiva</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Padrão internacional de divulgação para relatórios corporativos ESG, demonstrações de sustentabilidade e emissão de green bonds (títulos verdes):
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>GRI 303-3 (Captação Evitada / Water Withdrawal Saved):</b> Volume total de água potável que o empreendimento deixa de retirar das represas e bacias hidrográficas públicas (m³/ano e m³ acumulados em 20 anos).</li>
                <li><b>GRI 303-5 (Consumo e Circularidade Hídrica / Water Positive Ratio):</b> Índice de circularidade hídrica no empreendimento:
                    <br/><code>Water Positive Ratio = (Volume Pluvial Anual Consumido / Demanda Anual Total) × 100%</code>.
                </li>
            </ul>

            <h3 style='color:#0369a1; border-bottom: 2px solid #0284c7; padding-bottom: 4px; margin-top: 20px;'>6. EDGE (IFC / Grupo Banco Mundial) &mdash; a Barra de &Aacute;gua</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O EDGE &eacute; o &uacute;nico desta lista que <b>n&atilde;o pontua</b>. Ele mede
                percentual de economia contra um <i>caso-base local</i> em tr&ecirc;s barras
                independentes &mdash; energia, &aacute;gua e energia incorporada nos materiais &mdash;
                e exige que cada uma cruze o seu limiar:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6;'>
                <li><b>EDGE Certified:</b> no m&iacute;nimo <b>20%</b> de economia em energia, em &aacute;gua e na energia incorporada aos materiais.</li>
                <li><b>EDGE Advanced (Zero Carbon Ready):</b> o n&iacute;vel anterior, mais <b>40%</b> ou mais de economia de energia no local.</li>
                <li><b>Zero Carbon:</b> o EDGE Advanced, mais 100% de energia renov&aacute;vel, no local ou fora dele, ou compensa&ccedil;&atilde;o adquirida.</li>
            </ul>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O aproveitamento pluvial &eacute; a medida <b>WEM14</b>, cuja entrada no aplicativo
                EDGE &eacute; a <b>&aacute;rea de capta&ccedil;&atilde;o em m&sup2;</b>. O Triton informa
                a contribui&ccedil;&atilde;o dessa medida para a barra de &aacute;gua e a &aacute;rea
                de capta&ccedil;&atilde;o a declarar.
            </p>
            <div style='background-color: #fffbeb; border-left: 4px solid #b45309; padding: 10px 14px; border-radius: 4px; margin: 10px 0; font-size: 12.5px;'>
                <b>O que o Triton n&atilde;o tem como saber.</b> O caso-base &eacute; local: varia por
                pa&iacute;s e por tipologia, e &eacute; fixado pelo pr&oacute;prio aplicativo EDGE. Sem
                caso-base declarado, o Triton usa a demanda modelada do projeto, que &eacute; um piso e
                n&atilde;o o n&uacute;mero da certifica&ccedil;&atilde;o &mdash; um projeto que tamb&eacute;m
                instale lou&ccedil;as e metais eficientes tem caso-base maior.
                <b>A certifica&ccedil;&atilde;o sai do aplicativo EDGE, n&atilde;o daqui.</b>
            </div>
            <p style='font-size: 11.5px; color: #64748b;'>
                Fonte: IFC, <i>EDGE Certification Process</i>, edgebuildings.com/certify/certification/,
                consultado em 10 de setembro de 2026. C&oacute;digos das medidas conferidos contra um
                relat&oacute;rio de avalia&ccedil;&atilde;o EDGE v3.0.0 de projeto certificado.
            </p>
            """
        return self._create_browser(html, secao='esg')

    def create_tab_roof_materials(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🏠 Runoff and Absorption Coefficients of Roofs (Runoff - C)</h2>
            <p style='font-size: 13px; line-height: 1.5;'>
                The <b>Runoff Coefficient (<i>C</i>)</b> represents the ratio of rainwater that actually flows off the catchment surface to the total incident rainfall. The complement (<i>1 - C</i>) corresponds to the fraction absorbed or retained by wetting of the material, porosity, roughness, and evaporation.
            </p>
            
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 10px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left'>Roofing / Catchment Material</th>
                    <th align='center'>Runoff Coefficient (<i>C</i>)</th>
                    <th align='center'>Estimated Absorption / Loss (1 - C)</th>
                    <th align='left'>Technical Remarks and Material Characteristics</th>
                </tr>
                <tr>
                    <td><b>Clay Tile (Ceramic) / Telha Cerâmica</b></td>
                    <td align='center'><b>0,75</b></td>
                    <td align='center'>25%</td>
                    <td>Standard in Brazilian residences; retention due to porosity in ceramic and surface wetting.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Metallic Tile (Aluzinc / Zinc)</b></td>
                    <td align='center'><b>0,88</b></td>
                    <td align='center'>12%</td>
                    <td>Smooth and impermeable surface with extremely high efficiency and very low absorption.</td>
                </tr>
                <tr>
                    <td><b>Concrete / Fiber Cement Tile</b></td>
                    <td align='center'><b>0,73</b></td>
                    <td align='center'>27%</td>
                    <td>Moderate porosity of the cementitious matrix and surface roughness.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Green Roofs (Vegetal Cover)</b></td>
                    <td align='center'><b>0,24</b></td>
                    <td align='center'>76%</td>
                    <td>High water retention in the vegetal substrate, foliar interception, and evapotranspiration.</td>
                </tr>
                <tr>
                    <td><b>Aluminum</b></td>
                    <td align='center'><b>0,70</b></td>
                    <td align='center'>30%</td>
                    <td>Profile with roughness, grooves, or sheet joints under a gentle slope.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Plastic / Polycarbonate</b></td>
                    <td align='center'><b>0,94</b></td>
                    <td align='center'>6%</td>
                    <td>Smooth impermeable synthetic surface; minimal retention by initial wetting.</td>
                </tr>
                <tr>
                    <td><b>Asphalt Concrete</b></td>
                    <td align='center'><b>0,90</b></td>
                    <td align='center'>10%</td>
                    <td>Asphalt waterproofing membranes applied on flat roofs or slabs.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Galvanized Steel</b></td>
                    <td align='center'><b>0,92</b></td>
                    <td align='center'>8%</td>
                    <td>Excellent surface pluvial utilization and high durability.</td>
                </tr>
            </table>

            <div style='background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 14px; margin-top: 20px; border-radius: 4px;'>
                <h4 style='color: #0369a1; margin: 0px 0px 8px 0px; font-size: 13px;'>📚 Required Bibliographic Source for Roofing Materials:</h4>
                <p style='font-size: 12px; margin: 0px; line-height: 1.6; color: #0f172a;'>
                    <b>ESTUDO SOBRE MATERIAIS PARA COBERTURAS UTILIZADAS EM SISTEMAS DE APROVEITAMENTO DE ÁGUA PLUVIAL RESIDENCIAIS.</b><br/>
                    <i>MIX Sustentável</i>, [S. l.], v. 6, n. 2, p. 53–66, 2020. DOI: <a href='https://doi.org/10.29183/2447-3073.MIX2020.v6.n2.53-66' style='color: #0284c7;'>10.29183/2447-3073.MIX2020.v6.n2.53-66</a>.<br/>
                    Available at: <a href='https://ojs.sites.ufsc.br/index.php/mixsustentavel/article/view/4080' style='color: #0284c7;'>https://ojs.sites.ufsc.br/index.php/mixsustentavel/article/view/4080</a>. Accessed on: Jul 31, 2026.
                </p>
            </div>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🏠 Coeficientes de Escoamento e Absorção de Telhados (Runoff - C)</h2>
            <p style='font-size: 13px; line-height: 1.5;'>
                O <b>Coeficiente de Escoamento Superficial (Runoff Coefficient, <i>C</i>)</b> representa a razão entre a lâmina de água pluvial que efetivamente escoa pela superfície de cobertura e a precipitação total incidente. O complemento (<i>1 - C</i>) corresponde à fração absorvida ou retida por molhamento do material, porosidade, rugosidade e evaporação.
            </p>
            
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 10px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left'>Material da Cobertura / Telhado</th>
                    <th align='center'>Coeficiente de Escoamento (<i>C</i>)</th>
                    <th align='center'>Absorção / Perda Estimada (1 - C)</th>
                    <th align='left'>Observações Técnicas e Características do Material</th>
                </tr>
                <tr>
                    <td><b>Telha Cerâmica (Argila)</b></td>
                    <td align='center'><b>0,75</b></td>
                    <td align='center'>25%</td>
                    <td>Padrão em residências brasileiras; retenção por porosidade na cerâmica e molhamento superficial.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Telha Metálica (Aluzinco / Zinco)</b></td>
                    <td align='center'><b>0,88</b></td>
                    <td align='center'>12%</td>
                    <td>Superfície impermeável e lisa com altíssimo rendimento e baixíssima absorção.</td>
                </tr>
                <tr>
                    <td><b>Telha de Cimento / Fibrocimento</b></td>
                    <td align='center'><b>0,73</b></td>
                    <td align='center'>27%</td>
                    <td>Porosidade moderada da matriz cimentícia e rugosidade de superfície.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Telhados Verdes (Cobertura Vegetal)</b></td>
                    <td align='center'><b>0,24</b></td>
                    <td align='center'>76%</td>
                    <td>Elevada retenção hídrica no substrato vegetal, intercepção foliar e evapotranspiração.</td>
                </tr>
                <tr>
                    <td><b>Alumínio</b></td>
                    <td align='center'><b>0,70</b></td>
                    <td align='center'>30%</td>
                    <td>Perfil com rugosidades, sulcos ou junções de chapas sob aclive suave.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Plástico / Policarbonato</b></td>
                    <td align='center'><b>0,94</b></td>
                    <td align='center'>6%</td>
                    <td>Superfície sintética impermeável lisa; retenção mínima por molhamento inicial.</td>
                </tr>
                <tr>
                    <td><b>Concreto Asfáltico</b></td>
                    <td align='center'><b>0,90</b></td>
                    <td align='center'>10%</td>
                    <td>Mantas impermeabilizantes asfálticas aplicadas em lajes planas ou de cobertura.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Aço Galvanizado</b></td>
                    <td align='center'><b>0,92</b></td>
                    <td align='center'>8%</td>
                    <td>Excelente aproveitamento pluvial superficial e alta durabilidade.</td>
                </tr>
            </table>

            <div style='background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 14px; margin-top: 20px; border-radius: 4px;'>
                <h4 style='color: #0369a1; margin: 0px 0px 8px 0px; font-size: 13px;'>📚 Fonte Bibliográfica Exigida e Adotada para os Materiais de Cobertura:</h4>
                <p style='font-size: 12px; margin: 0px; line-height: 1.6; color: #0f172a;'>
                    <b>ESTUDO SOBRE MATERIAIS PARA COBERTURAS UTILIZADAS EM SISTEMAS DE APROVEITAMENTO DE ÁGUA PLUVIAL RESIDENCIAIS.</b><br/>
                    <i>MIX Sustentável</i>, [S. l.], v. 6, n. 2, p. 53–66, 2020. DOI: <a href='https://doi.org/10.29183/2447-3073.MIX2020.v6.n2.53-66' style='color: #0284c7;'>10.29183/2447-3073.MIX2020.v6.n2.53-66</a>.<br/>
                    Disponível em: <a href='https://ojs.sites.ufsc.br/index.php/mixsustentavel/article/view/4080' style='color: #0284c7;'>https://ojs.sites.ufsc.br/index.php/mixsustentavel/article/view/4080</a>. Acesso em: 31 jul. 2026.
                </p>
            </div>
            """
        return self._create_browser(html, secao='telhados')

    def create_tab_rain_indices(self) -> QWidget:
        """Os nove índices, com a equação de cada um e as divergências declaradas.

        A tabela anterior tinha uma coluna intitulada «Descrição e Equação de
        Cálculo» que não trazia equação nenhuma. Aqui cada índice aparece com a
        fórmula efetivamente implementada em ``triton/core/calculator.py``, e as
        três escolhas metodológicas que se afastam do ETCCDI padrão estão ditas
        em voz alta, em vez de ficarem só no código.
        """
        ingles = get_current_lang() != "pt"

        if ingles:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>📊 Nine Rainfall Indices (ETCCDI + Seasonality)</h2>
            <p style='font-size: 13px; line-height: 1.5;'>
                Triton characterises the rainfall series through eight indices from the
                <b>ETCCDI</b> set (<i>Expert Team on Climate Change Detection and Indices</i>, WMO/CLIVAR)
                plus the <b>Seasonality Index</b> of Walsh &amp; Lawler. Together they describe annual
                depth, extremes, dry spells and how concentrated the rain is across the year — the four
                things that decide whether a tank of a given size will keep working.
            </p>

            <h3>Common definitions</h3>
            <p>Every index below is computed <b>per calendar year</b>, over years with a complete record
            (365 or 366 days). Two thresholds govern the whole set:</p>
            <ul>
                <li><b>Wet day:</b> <i>P<sub>i</sub> ≥ 1.0 mm</i></li>
                <li><b>Dry day:</b> <i>P<sub>i</sub> &lt; 1.0 mm</i></li>
            </ul>
            <p>where <i>P<sub>i</sub></i> is the rainfall depth on day <i>i</i>, in millimetres.</p>

            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 10px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left' style='width: 13%;'>Index</th>
                    <th align='center' style='width: 13%;'>Unit</th>
                    <th align='left' style='width: 36%;'>Equation</th>
                    <th align='left'>What it tells you</th>
                </tr>
                <tr>
                    <td><b>PRCPTOT</b></td><td align='center'>mm/year</td>
                    <td><i>PRCPTOT = Σ P<sub>i</sub></i> &nbsp; for all <i>P<sub>i</sub> ≥ 1.0</i></td>
                    <td>Annual wet-day total. The gross water available to the catchment.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>R95p</b></td><td align='center'>mm/year</td>
                    <td><i>R95p = Σ P<sub>i</sub></i> &nbsp; for all <i>P<sub>i</sub> &gt; q<sub>95</sub></i>,<br/>
                        where <i>q<sub>95</sub></i> is the 95th percentile of wet-day rainfall</td>
                    <td>Depth falling on the very wettest days — water that arrives faster than a tank can hold.</td>
                </tr>
                <tr>
                    <td><b>RX1day</b></td><td align='center'>mm/day</td>
                    <td><i>RX1day = max(P<sub>i</sub>)</i></td>
                    <td>The single largest daily depth. Sizes gutters and downpipes.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>RX5day</b></td><td align='center'>mm</td>
                    <td><i>RX5day = max<sub>i</sub> ( Σ<sub>j=i−4</sub><sup>i</sup> P<sub>j</sub> )</i></td>
                    <td>Largest five-day accumulation. The event most likely to overflow a full tank.</td>
                </tr>
                <tr>
                    <td><b>SDII</b></td><td align='center'>mm/wet day</td>
                    <td><i>SDII = ( Σ P<sub>i</sub> ) / n<sub>wet</sub></i> &nbsp; over wet days only</td>
                    <td>Mean intensity of a rainy day. High SDII with few wet days means bursty supply.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>R20mm</b></td><td align='center'>days/year</td>
                    <td><i>R20mm = #{ i : P<sub>i</sub> ≥ 20.0 }</i></td>
                    <td>Count of heavy-rain days.</td>
                </tr>
                <tr>
                    <td><b>CDD</b></td><td align='center'>days</td>
                    <td>Longest run of consecutive <i>i</i> with <i>P<sub>i</sub> &lt; 1.0</i></td>
                    <td>The longest drought the tank must bridge. The single most demanding constraint on volume.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>CWD</b></td><td align='center'>days</td>
                    <td>Longest run of consecutive <i>i</i> with <i>P<sub>i</sub> ≥ 1.0</i></td>
                    <td>The longest wet spell; indicates prolonged spill.</td>
                </tr>
                <tr>
                    <td><b>SI</b></td><td align='center'>dimensionless</td>
                    <td><i>SI = (1/R) · Σ<sub>m=1</sub><sup>12</sup> | X<sub>m</sub> − R/12 |</i><br/>
                        <i>R</i> = annual total; <i>X<sub>m</sub></i> = total of month <i>m</i></td>
                    <td>How unevenly rain is spread across the months. 0 = perfectly uniform; 1.83 = all rain in one month.</td>
                </tr>
            </table>

            <h3>Methodological notes</h3>
            <p><b>1. Composition of the set.</b> Eight indices follow the ETCCDI definitions; the Seasonality
            Index follows Walsh &amp; Lawler (1981). The two references are combined because the ETCCDI set
            characterises totals, extremes and spells, but not how rainfall is distributed across the months
            &mdash; which is what governs the storage a tank needs. R10mm, part of the ETCCDI set, is not
            computed here: R20mm already covers heavy-rain days at the threshold relevant to roof catchment.</p>
            <p><b>2. Percentile base period.</b> <i>q<sub>95</sub></i> is computed over the series loaded for
            the study, rather than over the 1961&ndash;1990 reference period used in climate-monitoring
            applications of ETCCDI. This keeps R95p consistent with the record actually driving the
            simulation. For comparison with published ETCCDI figures, load a series covering the same base
            period.</p>
            <p><b>3. Rolling window at the turn of the year.</b> RX5day is computed within each calendar
            year, so the first four days form windows of one to four days. The effect is confined to peaks
            occurring in the first days of January.</p>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>📊 Nove Índices Pluviométricos (ETCCDI + Sazonalidade)</h2>
            <p style='font-size: 13px; line-height: 1.5;'>
                O Triton caracteriza a série de chuva por oito índices do conjunto <b>ETCCDI</b>
                (<i>Expert Team on Climate Change Detection and Indices</i>, OMM/CLIVAR) mais o
                <b>Índice de Sazonalidade</b> de Walsh &amp; Lawler. Juntos descrevem lâmina anual,
                extremos, estiagens e a concentração da chuva ao longo do ano — as quatro coisas que
                decidem se um reservatório de dado volume continuará funcionando.
            </p>

            <h3>Definições comuns a todos</h3>
            <p>Todos os índices são calculados <b>por ano civil</b>, sobre anos com registro completo
            (365 ou 366 dias). Dois limiares regem o conjunto inteiro:</p>
            <ul>
                <li><b>Dia úmido:</b> <i>P<sub>i</sub> ≥ 1,0 mm</i></li>
                <li><b>Dia seco:</b> <i>P<sub>i</sub> &lt; 1,0 mm</i></li>
            </ul>
            <p>em que <i>P<sub>i</sub></i> é a lâmina precipitada no dia <i>i</i>, em milímetros.</p>

            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 10px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left' style='width: 13%;'>Índice</th>
                    <th align='center' style='width: 13%;'>Unidade</th>
                    <th align='left' style='width: 36%;'>Equação</th>
                    <th align='left'>O que informa</th>
                </tr>
                <tr>
                    <td><b>PRCPTOT</b></td><td align='center'>mm/ano</td>
                    <td><i>PRCPTOT = Σ P<sub>i</sub></i> &nbsp; para todo <i>P<sub>i</sub> ≥ 1,0</i></td>
                    <td>Total anual em dias úmidos. A água bruta disponível à área de captação.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>R95p</b></td><td align='center'>mm/ano</td>
                    <td><i>R95p = Σ P<sub>i</sub></i> &nbsp; para todo <i>P<sub>i</sub> &gt; q<sub>95</sub></i>,<br/>
                        em que <i>q<sub>95</sub></i> é o percentil 95 da chuva dos dias úmidos</td>
                    <td>Lâmina que cai nos dias mais chuvosos — água que chega mais depressa do que o reservatório consegue guardar.</td>
                </tr>
                <tr>
                    <td><b>RX1day</b></td><td align='center'>mm/dia</td>
                    <td><i>RX1day = máx(P<sub>i</sub>)</i></td>
                    <td>Maior lâmina diária do ano. Dimensiona calhas e condutores.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>RX5day</b></td><td align='center'>mm</td>
                    <td><i>RX5day = máx<sub>i</sub> ( Σ<sub>j=i−4</sub><sup>i</sup> P<sub>j</sub> )</i></td>
                    <td>Maior acumulado em cinco dias. O evento que mais provavelmente extravasa um reservatório cheio.</td>
                </tr>
                <tr>
                    <td><b>SDII</b></td><td align='center'>mm/dia úmido</td>
                    <td><i>SDII = ( Σ P<sub>i</sub> ) / n<sub>úmidos</sub></i> &nbsp; só nos dias úmidos</td>
                    <td>Intensidade média de um dia de chuva. SDII alto com poucos dias úmidos indica oferta concentrada.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>R20mm</b></td><td align='center'>dias/ano</td>
                    <td><i>R20mm = #{ i : P<sub>i</sub> ≥ 20,0 }</i></td>
                    <td>Contagem de dias de chuva forte.</td>
                </tr>
                <tr>
                    <td><b>CDD</b></td><td align='center'>dias</td>
                    <td>Maior sequência de <i>i</i> consecutivos com <i>P<sub>i</sub> &lt; 1,0</i></td>
                    <td>A maior estiagem que o reservatório precisa atravessar. É a restrição mais exigente sobre o volume.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>CWD</b></td><td align='center'>dias</td>
                    <td>Maior sequência de <i>i</i> consecutivos com <i>P<sub>i</sub> ≥ 1,0</i></td>
                    <td>O maior período chuvoso contínuo; indica extravasamento prolongado.</td>
                </tr>
                <tr>
                    <td><b>SI</b></td><td align='center'>adimensional</td>
                    <td><i>SI = (1/R) · Σ<sub>m=1</sub><sup>12</sup> | X<sub>m</sub> − R/12 |</i><br/>
                        <i>R</i> = total anual; <i>X<sub>m</sub></i> = total do mês <i>m</i></td>
                    <td>Quão desigual é a distribuição da chuva entre os meses. 0 = perfeitamente uniforme; 1,83 = toda a chuva num único mês.</td>
                </tr>
            </table>

            <h3>Notas metodológicas</h3>
            <p><b>1. Composição do conjunto.</b> Oito índices seguem as definições do ETCCDI; o Índice de
            Sazonalidade segue Walsh &amp; Lawler (1981). As duas referências são combinadas porque o conjunto
            ETCCDI caracteriza totais, extremos e sequências, mas não a distribuição da chuva ao longo dos
            meses &mdash; que é justamente o que governa o volume de reservação necessário. O R10mm, do
            conjunto ETCCDI, não é calculado: o R20mm já cobre dias de chuva forte no limiar relevante para
            captação em cobertura.</p>
            <p><b>2. Período-base do percentil.</b> O <i>q<sub>95</sub></i> é calculado sobre a série carregada
            para o estudo, e não sobre o período de referência de 1961&ndash;1990 usado nas aplicações do
            ETCCDI voltadas ao monitoramento climático. Isso mantém o R95p coerente com o registro que de
            fato alimenta a simulação. Para comparar com valores ETCCDI publicados, carregue série que
            cubra o mesmo período-base.</p>
            <p><b>3. Janela móvel na virada do ano.</b> O RX5day é calculado dentro de cada ano civil, de
            modo que os quatro primeiros dias formam janelas de um a quatro dias. O efeito restringe-se a
            picos ocorridos nos primeiros dias de janeiro.</p>
            """
        return self._create_browser(html, secao='indices')


    def create_tab_rainfall_hydrology(self) -> QWidget:
        climbra_uri = _get_asset_data_uri("icons/CLIMBra.png") or _get_asset_data_uri("manual/figuras/CLIMBra.jpg")
        from triton.core.edition import usa_dados_do_brasil as _brasil
        img_climbra_tag = (f"<div style='margin: 12px 0;'><img src='{climbra_uri}' width='260' alt='CLIMbra Dataset'/></div>"
                           if climbra_uri and _brasil() else "")

        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🌧️ Rainfall and Pluvial Hydrology</h2>
            
            <h3 style='color: #0369a1;'>Daily Historical Rainfall Series ($P_t$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Continuous daily historical records of rainfall depth (in millimeters, mm) registered in a weather station. Triton simulates the water balance day by day over the entire historical series.
                <br/><b>Data Source:</b> INMET (National Institute of Meteorology), ANA (National Water Agency), CEMADEN or local stations.
            </p>

            <h3 style='color: #0369a1;'>CLIMBra Climate Database (CMIP6 / Projections)</h3>
            __CLIMBRA_IMG__
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Beyond single-station ground rain gauges, Triton integrates the high-resolution meteorological projections of <b>CLIMBra</b> (<i>Climate Change Dataset for Brazil</i>), encompassing <b>652 Brazilian municipalities</b>, <b>19 global climate models (GCMs/ESMs)</b> from CMIP6, and two emission trajectories: <b>SSP2-4.5</b> (middle-of-the-road) and <b>SSP5-8.5</b> (fossil-fueled development).
            </p>
            <ul style='font-size: 12px; line-height: 1.6;'>
                <li><b>Bias Correction:</b> 0.25° gridded daily time-series adjusted by <i>Quantile Delta Mapping</i> (QDM) against Xavier et al. (2016) ground observation grid.</li>
                <li><b>Time Horizons:</b> Continuous historical baseline (1980–2013, 12,419 days) and 21st-century projections (2015–2100, 31,411 days).</li>
                <li><b>Scientific Reference:</b> BALLARIN, A. S. et al. <i>CLIMBra - Climate Change Dataset for Brazil</i>. Sci Data 10, 48 (2023). <a href='https://doi.org/10.1038/s41597-023-01956-z' style='color:#0284c7;'>doi:10.1038/s41597-023-01956-z</a></li>
                <li><b>Open Data Repository:</b> Science Data Bank (CC0 License). <a href='https://doi.org/10.57760/sciencedb.02316' style='color:#0284c7;'>doi:10.57760/sciencedb.02316</a></li>
            </ul>

            <h3 style='color: #0369a1;'>First Flush / Initial Discard ($d_f$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                When the discard rule applies on a given day, <i>d<sub>f</sub></i> is <b>subtracted</b> from the gross daily rainfall: the effective rainfall is <i>P<sub>t</sub> − d<sub>f</sub></i> when <i>P<sub>t</sub> &gt; d<sub>f</sub></i>, and <b>zero</b> otherwise — a day that does not exceed the depth is lost in full, not in part. On days when the rule does not apply, the whole daily rainfall is capturable. Note that <i>d<sub>f</sub></i> is a <b>depth</b> (mm), not the hydraulic volume of the physical first-flush device, <i>A × d<sub>f</sub></i>, which requires a separate design.
            </p>

            <h3 style='color: #0369a1;'>Daily Capturable Volume ($V_{cap, t}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The rainwater volume actually directed to the lower cistern on a day <i>t</i>:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                V<sub>cap,t</sub> = A × C × P<sub>eff,t</sub>, where P<sub>eff,t</sub> = 0 if the applicable event is below d<sub>f</sub>; otherwise P<sub>eff,t</sub> = P<sub>t</sub>
                </code>
            </p>
            """.replace("__CLIMBRA_IMG__", img_climbra_tag)
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🌧️ Precipitação e Hidrologia Pluvial</h2>
            
            <h3 style='color: #0369a1;'>Série Histórica Pluviométrica Diária ($P_t$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                É a sequência temporal diária contínua da lâmina de chuva (em milímetros, mm) registrada em uma estação meteorológica. O Triton simula o balanço hídrico dia a dia ao longo de toda a série histórica fornecida pelo usuário.
                <br/><b>Fonte dos Dados:</b> INMET (Instituto Nacional de Meteorologia), ANA (Agência Nacional de Águas), CEMADEN ou estações locais (ex: EPAGRI/CIRAM).
            </p>

            <h3 style='color: #0369a1;'>Base de dados CLIMBra (CMIP6 / Projeções)</h3>
            __CLIMBRA_IMG__
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Além das séries pontuais de estações meteorológicas, o Triton integra as projeções climáticas em grade de alta resolução do <b>CLIMBra</b> (<i>Climate Change Dataset for Brazil</i>), cobrindo <b>652 municípios brasileiros</b>, <b>19 modelos climáticos globais</b> (GCMs/ESMs) do CMIP6 e dois cenários de emissões: <b>SSP2-4.5</b> (trajetória intermediária) e <b>SSP5-8.5</b> (trajetória extrema de emissões elevadas).
            </p>
            <ul style='font-size: 12px; line-height: 1.6;'>
                <li><b>Metodologia de Correção:</b> Séries em grade de 0,25° (~28 km) corrigidas estatisticamente pelo método <i>Quantile Delta Mapping</i> (QDM), calibradas contra o conjunto observacional diário de Xavier, King e Scanlon (2016).</li>
                <li><b>Horizontes Temporais:</b> Série histórica simulada contínua de 1980 a 2013 (12.419 dias) e projeções futuras ininterruptas de 2015 a 2100 (31.411 dias), com atalhos de recortes de 30 anos (2021–2050, 2041–2070 e 2071–2100).</li>
                <li><b>Artigo na Nature Scientific Data:</b> BALLARIN, A. S. et al. <i>CLIMBra - Climate Change Dataset for Brazil</i>. Scientific Data 10, art. 47 (2023). <a href='https://doi.org/10.1038/s41597-023-01956-z' style='color:#0284c7;'>doi:10.1038/s41597-023-01956-z</a></li>
                <li><b>Repositório de Dados Abertos:</b> Science Data Bank (licença pública CC0). <a href='https://doi.org/10.57760/sciencedb.02316' style='color:#0284c7;'>doi:10.57760/sciencedb.02316</a></li>
            </ul>

            <h3 style='color: #0369a1;'>First Flush / Descarte Inicial ($d_f$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Quando a regra de descarte se aplica no dia, <i>d<sub>f</sub></i> é <b>subtraída</b> da chuva bruta: a chuva efetiva é <i>P<sub>t</sub> − d<sub>f</sub></i> quando <i>P<sub>t</sub> &gt; d<sub>f</sub></i>, e <b>zero</b> caso contrário — o dia que não supera a lâmina se perde inteiro, e não em parte. Nos dias em que a regra não se aplica, a chuva do dia é captável integralmente. Repare que <i>d<sub>f</sub></i> é uma <b>lâmina</b> (mm), e não o volume hidráulico do dispositivo físico de first flush, <i>A × d<sub>f</sub></i>, que exige dimensionamento separado.
            </p>

            <h3 style='color: #0369a1;'>Volume Diário Captável ($V_{cap, t}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Volume de água efetivamente direcionado ao reservatório inferior em um dia <i>t</i>:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                V<sub>cap,t</sub> = A × C × P<sub>ef,t</sub>, em que P<sub>ef,t</sub> = 0 se o evento aplicável estiver abaixo de d<sub>f</sub>; caso contrário, P<sub>ef,t</sub> = P<sub>t</sub>
                </code>
            </p>
            """.replace("__CLIMBRA_IMG__", img_climbra_tag)
        return self._create_browser(html, secao='hidrologia')

    def create_tab_building_demand(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🏢 Building Parameters and Water Demand</h2>
            
            <h3 style='color: #0369a1;'>Catchment / Roof Area ($A$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The area of the impervious roof surface where water is collected, projected on the horizontal plane, in square metres (m²), as defined in item 3.6 of ABNT NBR 15527:2019. It is neither the sloped roof area nor the contributing area of ABNT NBR 10844, which adds the roof slope and walls to size gutters.
            </p>

            <h3 style='color: #0369a1;'>Total Per Capita Demand ($D_{hab}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Total average volume of water consumed daily by each building occupant (Liters/occupant/day).
                <br/><b>Evidence hierarchy:</b> use metered bills with occupancy records or a building end-use audit. Population-level utility indicators are contextual and must not be transferred to a building without justification.
            </p>

            <h3 style='color: #0369a1;'>Percentage to be Replaced by Rainwater ($S_{pct}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The portion of total water demand intended exclusively for non-potable uses (flushing toilets, washing clothes, garden irrigation, floor cleaning).
                <br/><b>Daily Rainwater Demand Formula:</b> <i>D<sub>rainwater</sub> (L/day) = N<sub>occupants</sub> × D<sub>hab</sub> × (S<sub>pct</sub> / 100)</i>.
                <br/><b>Evidence requirement:</b> derive the fraction from the intended fixtures/uses and measured or cited end-use data for the same building type; test uncertainty instead of assuming a universal percentage.
            </p>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>🏢 Parâmetros da Edificação e Demanda de Água</h2>
            
            <h3 style='color: #0369a1;'>Área de Captação / Cobertura ($A$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Área projetada na horizontal da superfície impermeável da cobertura onde a água é captada, em metros quadrados (m²), conforme o item 3.6 da ABNT NBR 15527:2019. Não é a área inclinada do telhado, nem a área de contribuição da ABNT NBR 10844, que soma a inclinação e as paredes para dimensionar calhas.
            </p>

            <h3 style='color: #0369a1;'>Demanda Total Per Capita ($D_{hab}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Volume total de água consumido diariamente por habitante/ocupante (Litros/habitante/dia).
                <br/><b>Hierarquia de evidência:</b> use faturas medidas com registro de ocupação ou auditoria de usos finais da edificação. Indicadores populacionais de concessionárias servem como contexto e não devem ser transferidos à edificação sem justificativa.
            </p>

            <h3 style='color: #0369a1;'>Percentual a Substituir por Água Pluvial ($S_{pct}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Percentual do consumo total de água destinado exclusivamente aos usos não potáveis (bacias sanitárias, lavagem de roupas, rega de jardim, limpeza de pisos).
                <br/><b>Fórmula da Demanda Pluvial Diária:</b> <i>D<sub>pluvial</sub> (L/dia) = N<sub>moradores</sub> × D<sub>hab</sub> × (S<sub>pct</sub> / 100)</i>.
                <br/><b>Requisito de evidência:</b> derive a fração dos aparelhos/usos previstos e de dados medidos ou citados para a mesma tipologia; teste a incerteza em vez de assumir um percentual universal.
            </p>
            """
        return self._create_browser(html, secao='demanda')

    def create_tab_tanks_pumping(self) -> QWidget:
        if get_current_lang() != "pt":
            html = r"""
            <h2 style='color: #0284c7; margin-top: 0px;'>🚰 Tanks and Pumping System</h2>
            
            <h3 style='color: #0369a1;'>Daily Water Balance in the Lower Tank (Cistern)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The lower cistern follows the <b>Yield After Spillage (YAS)</b> operational rule: storage capacity and spillage are evaluated prior to demand abstraction:<br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                I<sub>t</sub> = min(V, S<sub>t-1</sub> + V<sub>cap,t</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; O<sub>t</sub> = max(0, S<sub>t-1</sub> + V<sub>cap,t</sub> − V) &nbsp;&nbsp;|&nbsp;&nbsp; Y<sub>t</sub> = min(D<sub>pl,t</sub>, I<sub>t</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; S<sub>t</sub> = I<sub>t</sub> − Y<sub>t</sub>
                </code>
            </p>

            <h3 style='color: #0369a1;'>First Flush Discard Subtraction (NBR 15527)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                When an active discard event triggers according to the selected mode (every event, after drought, or periodic interval), the first flush depth <i>d<sub>f</sub></i> (in mm) is subtracted from the gross daily rainfall:
                <br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                P<sub>eff,t</sub> = max(0, P<sub>t</sub> − d<sub>f</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; V<sub>cap,t</sub> = A × C × P<sub>eff,t</sub>
                </code>
            </p>

            <h3 style='color: #0369a1;'>Maximum Sweep Volume ($V_{max}$) Formulation</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The maximum simulation volume ($V_{max}$) represents the boundary where the rainwater savings curve enters saturation (the plateau of marginal technical gain $\Delta E_{pot} \to 0$). It is dynamically established through the coupling of <b>Daily Pluvial Demand ($D_{pl}$)</b>, the <b>Simple Daily Intensity Index (SDII)</b>, <b>Roof Catchment Capacity ($V_{catch}$)</b>, and the <b>Upper Tank Volume ($V_{sup}$)</b>:
            </p>
            
            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 10px 14px; margin: 10px 0; border-radius: 0 6px 6px 0;'>
                <p style='font-weight: bold; margin: 0 0 6px 0; color: #0369a1;'>1. Rainwater Autonomy Modulated by Climate Index (SDII):</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                Autonomy (days) = 15 + min(20, 1.0 × SDII)
                </code>
                <p style='font-size: 12px; margin: 4px 0 0 0; color: #475569;'>
                • Low SDII (&le;8 mm/d, frequent gentle drizzle): ~18 to 22 days of storage are sufficient due to continuous replenishment.<br/>
                • High SDII (&gt;18 mm/d, torrential storms with longer dry spells): ~30 to 35 days of storage capture torrent peaks and bridge droughts.
                </p>
                
                <p style='font-weight: bold; margin: 10px 0 6px 0; color: #0369a1;'>2. Storage Volumes derived from Demand & Catchment:</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                V<sub>demand</sub> = D<sub>pl,day</sub> × Autonomy(days) &nbsp;&nbsp;|&nbsp;&nbsp; V<sub>catch</sub> = min(8.0, 3.0 + 0.3 × SDII) × SDII × A × C
                </code>

                <p style='font-weight: bold; margin: 10px 0 6px 0; color: #0369a1;'>3. Final Harmonized Sweep Upper Bound:</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                V<sub>max,sugg</sub> = max( V<sub>demand</sub>, min(V<sub>catch</sub>, 1.8 × V<sub>demand</sub>), 10 × V<sub>sup</sub> )
                </code>
                <p style='font-size: 12px; margin: 4px 0 0 0; color: #475569;'>
                The suggested maximum is rounded to multiples of 250 L with an automatic step ensuring up to 40 simulated capacities.
                </p>
            </div>

            <h3 style='color: #0369a1;'>Pumping Activation Threshold ($T_{pump}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The percentage level of the upper tank below which the pump triggers to transfer water from the lower cistern to the upper tank (e.g., 30–50%).
            </p>

            <h3 style='color: #0369a1;'>Electric Consumption of the Pumping System</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The annual electricity consumption of the pump (kWh/year) takes into account continuous pumping hours, pump startups, and global efficiency:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                Energy (kWh/year) = [ Power (kW) × (Pumping_hours + Startups × startup_duration) ] / Efficiency (η)
                </code>
            </p>

            <h3 style='color: #0369a1;'>Hydraulic Piping Sizing (NBR 5626 / Forchheimer Formula)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Piping estimates in Triton adopt standard baseline lengths of <b>5 meters for suction</b> (from cistern to pump) and <b>20 meters for discharge/recalque</b> (from pump to elevated upper tank).
                Diameters are automatically synchronized with the selected pump using Forchheimer's economic diameter formula:
                <br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                D<sub>rec</sub> = 1.3 × (T / 24)<sup>0.25</sup> × √Q &nbsp;&nbsp;|&nbsp;&nbsp; DN<sub>suc</sub> ≥ DN<sub>rec</sub>
                </code>
                <br/>
                Where <i>Q</i> is pump flow rate (m³/s) and <i>T</i> is daily pumping hours. Suction velocity is capped below 1.0 m/s to prevent pump cavitation.
            </p>
            """
        else:
            html = r"""
            <h2 style='color: #0284c7; margin-top: 0px;'>🚰 Reservatórios e Sistema de Bombeamento</h2>
            
            <h3 style='color: #0369a1;'>Balanço Hídrico Diário no Reservatório Inferior (Cisterna)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                A cisterna inferior segue o modelo de operação <b>Yield After Spillage (YAS)</b>: o extravasamento e a capacidade de armazenagem são calculados antes da retirada do consumo diário:<br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                I<sub>t</sub> = min(V, S<sub>t-1</sub> + V<sub>cap,t</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; O<sub>t</sub> = max(0, S<sub>t-1</sub> + V<sub>cap,t</sub> − V) &nbsp;&nbsp;|&nbsp;&nbsp; Y<sub>t</sub> = min(D<sub>pl,t</sub>, I<sub>t</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; S<sub>t</sub> = I<sub>t</sub> − Y<sub>t</sub>
                </code>
            </p>

            <h3 style='color: #0369a1;'>Redução por Descarte de Primeiras Águas (First Flush — NBR 15527)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Quando um evento de chuva ativa a regra de descarte selecionada (todos os eventos, pós estiagem ou intervalo de X dias), a lâmina de descarte <i>d<sub>f</sub></i> (em mm) é subtraída diretamente da chuva bruta:
                <br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                P<sub>ef,t</sub> = max(0, P<sub>t</sub> − d<sub>f</sub>) &nbsp;&nbsp;|&nbsp;&nbsp; V<sub>cap,t</sub> = A × C × P<sub>ef,t</sub>
                </code>
            </p>

            <h3 style='color: #0369a1;'>Formulação do Volume Máximo de Varredura ($V_{máx}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O volume máximo da varredura ($V_{máx}$) deve delimitar com segurança o <b>platô de saturação técnica</b> (onde o ganho marginal de economia $\Delta E_{pot} \to 0$), evitando simulações desnecessárias ou reservatórios superdimensionados. O Triton estabelece essa referência acoplando a <b>Demanda Pluvial Diária ($D_{pl}$)</b>, o <b>Índice Pluviométrico SDII</b>, a <b>Capacidade de Captação do Telhado ($V_{oferta}$)</b> e o <b>Reservatório Superior ($V_{sup}$)</b>:
            </p>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0;'>
                <p style='font-weight: bold; margin: 0 0 6px 0; color: #0369a1;'>1. Autonomia em Dias Modulada pelo SDII:</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                Autonomia (dias) = 15 + min(20, 1{,}0 × SDII)
                </code>
                <p style='font-size: 12px; margin: 4px 0 0 0; color: #475569;'>
                • <b>SDII Baixo (&le;8 mm/dia — chuvas brandas/frequentes):</b> Reposição quase contínua; requer ~18 a 22 dias de autonomia.<br/>
                • <b>SDII Médio (10 a 18 mm/dia — regime típico Centro-Sul):</b> Autonomia balanceada de ~25 a 30 dias.<br/>
                • <b>SDII Alto (&gt;18 mm/dia — tempestades tropicais concentradas e estiagens):</b> Requer ~30 a 35 dias para amortecer torrentes e cobrir períodos secos.
                </p>

                <p style='font-weight: bold; margin: 10px 0 6px 0; color: #0369a1;'>2. Volumes Derivados da Demanda e da Captação:</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                V<sub>demanda</sub> = D<sub>pl,dia</sub> × Autonomia(dias) &nbsp;&nbsp;|&nbsp;&nbsp; V<sub>oferta</sub> = min(8{,}0, 3{,}0 + 0{,}3 × SDII) × SDII × A × C
                </code>

                <p style='font-weight: bold; margin: 10px 0 6px 0; color: #0369a1;'>3. Teto Harmonizado de Varredura:</p>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12.5px; color: #0284c7;'>
                V<sub>máx,sugerido</sub> = max( V<sub>demanda</sub>, min(V<sub>oferta</sub>, 1{,}8 × V<sub>demanda</sub>), 10 × V<sub>sup</sub> )
                </code>
                <p style='font-size: 12px; margin: 4px 0 0 0; color: #475569;'>
                O resultado é ajustado ao quantum de 250 L com passo automático dimensionado para até 40 volumes positivos simulados.
                </p>
            </div>

            <h3 style='color: #0369a1;'>Limiar de Acionamento da Motobomba ($T_{pump}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Nível percentual do reservatório superior abaixo do qual a bomba aciona para transferir água da cisterna inferior para a caixa d'água superior (perfis usuais de 10%, 30% e 50%).
            </p>

            <h3 style='color: #0369a1;'>Consumo Elétrico da Motobomba</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O consumo anual de energia elétrica da bomba (kWh/ano) leva em consideração as horas de recalque contínuo, as partidas da bomba e o rendimento global:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                Energia (kWh/ano) = [ Potência (kW) × (Horas_recalque + Partidas × t_partida) ] / Rendimento (η)
                </code>
            </p>

            <h3 style='color: #0369a1;'>Dimensionamento Hidráulico de Tubulações (Fórmula de Forchheimer / NBR 5626)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O Triton adota como estimativa orçamentária e de inventário ACV o traçado padrão de <b>5 metros para a linha de sucção</b> (cisterna à bomba) e <b>20 metros para a linha de recalque</b> (bomba ao reservatório superior).
                Os diâmetros comerciais vêm vinculados diretamente à motobomba selecionada no <i>Assistente de Dimensionamento</i> via Fórmula de Forchheimer (NBR 5626 / NBR 12214):
                <br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 4px 0;'>
                D<sub>rec</sub> = 1{,}3 · (T / 24)<sup>0{,}25</sup> · √Q &nbsp;&nbsp;|&nbsp;&nbsp; DN<sub>suc</sub> ≥ DN<sub>rec</sub>
                </code>
                <br/>
                Onde <i>Q</i> é a vazão em m³/s e <i>T</i> as horas diárias de funcionamento. A linha de sucção adota diâmetro comercial superior (ex.: recalque DN 32 mm e sucção DN 40 mm) para manter a velocidade abaixo de 1,0 m/s e evitar perda de carga excessiva ou risco de cavitação.
            </p>
            """
        return self._create_browser(html, secao='reservatorios')

    def create_tab_water_quality_etap(self) -> QWidget:
        """Apresenta a fundamentação hidrológica do descarte inicial (wash-off), artigos de base e dimensionamento da ETAP."""
        if get_current_lang() != "pt":
            html = r"""
            <h2 style='color: #0284c7; margin-top: 0px;'>🧪 Water Quality, First Flush Wash-Off & Rainwater Treatment Plant (ETAP)</h2>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0;'><b>What this tab does, and does not do.</b> It answers four questions, in this order:</p>
                <p style='margin: 0 0 4px 0;'>1. <b>Which limits the design must meet</b> &mdash; the NBR 15527:2019 parameters, in section 3.</p>
                <p style='margin: 0 0 4px 0;'>2. <b>Which first-flush discard is being adopted</b> &mdash; and what the standard recommends where data are lacking.</p>
                <p style='margin: 0 0 4px 0;'>3. <b>How discard correlates with the expected improvement</b> &mdash; the curve in section 1.</p>
                <p style='margin: 0;'>4. <b>Which treatment barriers make up the line</b> &mdash; chlorination always, with ultraviolet, ozone and a polishing filter as optional stages.</p>
                <p style='margin: 6px 0 0 0;'>The curve in section 1 is a <b>design correlation</b>, used to size the discard and compare alternatives. It does not replace laboratory testing: the standard requires monitoring at least every six months (clause 4.6.7).</p>
            </div>

            <h3 style='color: #0369a1;'>1. Scientific Foundation for First Flush Pollutant Removal (Wash-Off Model)</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                During antecedent dry periods (ADP), airborne particulates, vehicular soot, bird droppings, and organic debris accumulate on catchment surfaces.
                The fundamental experimental mechanisms are anchored in foundational literature (<b>Yaziz et al., 1989</b>; <b>Martinson & Thomas, 2005</b>)
                and rigorously corroborated by recent experimental investigations by the research group:
            </p>

            <div style='background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0;'>
                <b style='color: #15803d;'>Recent Core Research Benchmark (UFSC):</b><br/>
                <b>MAYKOT, J. K.; VAZ, I. C. M.; GHISI, E. (2025).</b><br/>
                <i>"Characterisation of First Flush for Rainwater Harvesting Purposes in Buildings"</i>. <b>Water</b>, v. 17, n. 12, art. 1772. DOI: <a href='https://doi.org/10.3390/w17121772' style='color: #087f6b;'>10.3390/w17121772</a>.<br/>
                <span style='font-size: 12px; color: #374151; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                This experimental study characterized real roof runoff (fibre-cement, southern Brazil) across multiple events and antecedent dry periods (ADP).
                It quantified pH, total suspended solids (TSS), turbidity, apparent colour, conductivity, total coliforms, and <i>Escherichia coli</i>,
                demonstrating strong statistical correlations among turbidity, colour, and microbial loads, and reinforcing the indispensability of automated first-flush diversion (1.0 to 2.0 mm) for building non-potable safety.
                </span>
            </div>

            <h4 style='color: #0369a1;'>Exponential Wash-Off Mathematical Formulation</h4>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Triton applies the exponential decay model formalized by <b>Martinson & Thomas (2005)</b> and validated by <b>Maykot, Vaz & Ghisi (2025)</b>:<br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 6px 0;'>
                E(d) = 100% × ( 1 − e<sup>−k · d</sup> )
                </code><br/>
                Where:
                <ul style='font-size: 12px; line-height: 1.5; color: #334155;'>
                    <li><b>E(d):</b> Cumulative pollutant mass removal efficiency (%);</li>
                    <li><b>d:</b> Applied first-flush discard depth (mm), where 1.0 mm = 1.0 L discarded per m² of roof;</li>
                    <li><b>k:</b> Wash-off coefficient (mm<sup>−1</sup>), adopted per impurity fraction. The values sit within the range reported in the first-flush literature and are design parameters rather than measured constants, so they remain editable:
                        <ul>
                            <li><b>Coarse / Settleable Solids (k = 1.6 mm<sup>−1</sup>):</b> Heavy particles washed quickly by initial droplet impact (<i>E ≈ 79.8% at 1.0 mm; E ≈ 95.9% at 2.0 mm</i>).</li>
                            <li><b>Fine Turbidity / Soot (k = 1.3 mm<sup>−1</sup>):</b> Colloidal and atmospheric dust particles (<i>E ≈ 72.7% at 1.0 mm; E ≈ 92.6% at 2.0 mm</i>).</li>
                            <li><b>Bacterial Load / Attached Biofilm (k = 1.1 mm<sup>−1</sup>):</b> Coliforms and microbes requiring higher shear stress (<i>E ≈ 66.7% at 1.0 mm; E ≈ 88.9% at 2.0 mm</i>).</li>
                        </ul>
                    </li>
                </ul>
            </p>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 12px 0; border-radius: 0 6px 6px 0;'>
                <b>Post-Discard Turbidity Formulation:</b><br/>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12px; color: #0284c7; display: inline-block; margin-top: 4px;'>
                Turbidity<sub>post-discard</sub> = max( 1.5 NTU, Turbidity<sub>raw</sub> × [ 1 − E<sub>turb</sub> / 100 ] )
                </code><br/>
                <span style='font-size: 11.5px; color: #64748b;'>Adopted benchmark raw roof runoff turbidity = 45.0 NTU.</span>
            </div>

            <h3 style='color: #0369a1;'>2. Rainwater Treatment Plant (ETAP) Equipment & Data Sources</h3>
            
            <table style='width: 100%; border-collapse: collapse; font-size: 12px; margin: 10px 0;'>
                <thead>
                    <tr style='background-color: #f1f5f9; text-align: left;'>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Treatment Stage</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Equipment Specification</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Mesh / Design Criteria</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>CAPEX & OPEX Reference</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>1. Mechanical Pre-filtration</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Vortex self-cleaning filter (DN 100 up to 150 m², DN 150 up to 400 m², Cyclonic DN 200 >400 m²)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>AISI 304 stainless steel mesh (350 µm to 500 µm), &gt;90% hydraulic recovery</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>SINAPI / Specialized commercial suppliers (BRL 650 to BRL 2,800)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>2. Chemical Disinfection (Chlorination)</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>In-line erosion tablet feeder using Calcium Hypochlorite (65% active chlorine)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Dosage: 0.5 to 2.0 mg/L active Cl<sub>2</sub> (NBR 15527:2019, clause 4.6.5; permitted maximum 5 mg/L). Always present: it is the only barrier leaving a free residual, which ultraviolet and ozone do not.</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>BRL 280 feeder; chemical cost: BRL 38.00/kg; LCA: 1.72 kg CO<sub>2</sub>e/kg of tablet (Ecoinvent 3.8, sodium hypochlorite as proxy, active-chlorine basis)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>3. Physical Disinfection (Ultraviolet UV)</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Low-pressure mercury vapor germicidal UV reactor (254 nm wavelength)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>UV dosage &ge; 30 mJ/cm² (NSF/ANSI 55), 25W (&le;200 m³/yr) to 55W</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>BRL 1,200 to BRL 2,200; 9,000h lamp life (annual replacement BRL 180 to BRL 320)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>4. Polishing Filtration</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Extruded Carbon Block (5–10 µm) for noble uses or multi-layer sand (20 µm)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Removes residual color, odor and VOCs for laundry (Class 4) and cooling</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>BRL 380 to BRL 550; annual cartridge renewal: BRL 90 to BRL 150/yr</td>
                    </tr>
                </tbody>
            </table>

            <h3 style='color: #0369a1;'>3. Water Quality Classes by Use</h3>
            <ul style='font-size: 12.5px; line-height: 1.6; color: #334155;'>
                <li><b>Class 1 (Toilet & Urinal Flushing):</b> Turbidity &le; 5.0 NTU; Color &le; 15 uH; pH 6.0–9.0; Free Residual Cl<sub>2</sub> 0.5–2.0 mg/L; Coliforms &le; 200 CFU/100 mL.</li>
                <li><b>Class 2 (Garden Irrigation, Floor & Vehicle Washing):</b> Turbidity &le; 5.0 NTU; Color &le; 15 uH; pH 6.0–9.0; Free Residual Cl<sub>2</sub> 1.0–3.0 mg/L; Coliforms = 0 (Absence).</li>
                <li><b>Class 3 (Cooling Towers & Industrial Boilers):</b> Turbidity &le; 2.0 NTU; Color &le; 10 uH; pH 6.5–8.5; Free Residual Cl<sub>2</sub> 1.0–2.5 mg/L; Coliforms = 0 (Absence).</li>
                <li><b>Class 4 (Laundry & Noble Non-Potable Uses):</b> Turbidity &le; 2.0 NTU; Color &le; 5 uH; pH 6.5–8.5; Free Residual Cl<sub>2</sub> 0.5–1.5 mg/L; Coliforms = 0 (Absence).</li>
            </ul>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 14px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0;'><b>Requirements of NBR 15527:2019.</b> The standard sets a single set of minimum parameters, with no matrix of use classes: clause 4.6.3, Table 1, sets a <b>single</b> set of minimum parameters, valid for every non-potable use listed in 4.1.7.</p>
                <table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse; border-color: #cbd5e1; width: 60%; margin: 8px 0; font-size: 12px; background: #ffffff;'>
                    <tr style='background-color: #0284c7; color: #ffffff;'><th align='left'>Parameter</th><th align='left'>Value</th></tr>
                    <tr><td><i>Escherichia coli</i></td><td>&lt; 200 / 100 mL</td></tr>
                    <tr><td>Turbidity</td><td>&lt; 5.0 NTU</td></tr>
                    <tr><td>pH</td><td>6.0 to 9.0</td></tr>
                </table>
                <p style='margin: 0 0 6px 0;'>Clause 4.6.5 adds free residual chlorine between <b>0.5 and 2.0 mg/L</b>, with 5 mg/L as the permitted maximum. The standard has no colour parameter.</p>
                <p style='margin: 0;'><b>How the table above is built.</b> Class 1 corresponds to the normative set, with two design additions: a colour limit, absent from the standard, and thermotolerant coliforms in place of <i>E. coli</i>, which is the more restrictive of the two. Classes 2 to 4 are a graded scheme adopted by this programme for uses whose exposure differs &mdash; drawing on the parameters-by-use approach of the 2007 edition and on current practice &mdash; and are offered as design guidance, the normative requirement being Class 1 in every case.</p>
            </div>

            <h3 style='color: #0369a1;'>4. Why these parameters, and not others</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Five quantities are enough to decide whether a water is fit for a non-potable use. Each answers a different question, and none substitutes for the others.
            </p>
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 8px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left' style='width: 22%;'>Parameter</th>
                    <th align='left'>Why it is measured</th>
                </tr>
                <tr>
                    <td><b>Turbidity</b></td>
                    <td>The operational proxy for disinfection efficiency. Suspended particles shelter microorganisms and consume chlorine, so cloudy water can receive an adequate dose and still not be disinfected. Turbidity is measured in minutes, in the field; a microbiological count takes 24 hours in a laboratory. That is why it is the continuous control parameter and the bacteriological test the periodic verification.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Apparent colour</b></td>
                    <td>Signals dissolved organic matter and material leached from the roof. It matters for two reasons: it consumes chlorine without turbidity registering it, and it is why users reject water in visible uses &mdash; laundry above all. That is exactly why it is the most restrictive parameter in Class 4.</td>
                </tr>
                <tr>
                    <td><b>pH</b></td>
                    <td>Governs chlorine effectiveness and the water's aggressiveness towards pipework. Above pH 8 the hypochlorous acid fraction &mdash; the species that actually disinfects &mdash; falls sharply, and the same measured residual disinfects less. Below pH 6 the water attacks metals and mortars. The range is a precondition for the residual to mean anything at all.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Free residual chlorine</b></td>
                    <td>The only parameter attesting <i>continued</i> protection: it measures the remaining capacity to inactivate contamination introduced after treatment, inside the tank and the pipes. It has a minimum and a maximum &mdash; below the minimum there is no barrier; above it, odour, taste and disinfection by-products appear. Hence a band, not a ceiling.</td>
                </tr>
                <tr>
                    <td><b>Faecal coliforms</b></td>
                    <td>Indicator of faecal contamination, which on a roof comes mostly from birds and small animals. The pathogen is not measured directly: what is measured is an abundant, easily cultured organism that travels with the contamination. Class 1 admits up to 200 CFU/100 mL because toilet flushing carries minimal human exposure; the other classes require absence because they involve aerosol, contact, or contact with clothing.</td>
                </tr>
            </table>
            <p style='font-size: 12.5px; line-height: 1.6; margin-top: 10px;'>
                <b>Two deliberate omissions.</b> Potability is not assessed: the rainwater here is intended for non-potable uses, and comparing its limits with Brazil's drinking-water regulation (<b>Portaria GM/MS 888/2021</b>) would wrongly suggest the system fails a requirement it never set out to meet. Metals and organic compounds are not assessed either: they would matter on old metal roofs or in heavily polluted airsheds, cases that demand their own sampling campaign and lie outside the reach of a preliminary sizing.
            </p>
            """
        else:
            html = r"""
            <h2 style='color: #0284c7; margin-top: 0px;'>🧪 Qualidade da Água, Descarte Inicial (Wash-Off) e Linha de Tratamento (ETAP)</h2>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0;'><b>O que esta aba faz, e o que não faz.</b> Ela responde a quatro perguntas, nesta ordem:</p>
                <p style='margin: 0 0 4px 0;'>1. <b>Quais limites o projeto precisa atender</b> &mdash; os parâmetros da NBR 15527:2019, na seção 3.</p>
                <p style='margin: 0 0 4px 0;'>2. <b>Qual descarte de primeira chuva está sendo adotado</b> &mdash; e o que a norma recomenda na falta de dados.</p>
                <p style='margin: 0 0 4px 0;'>3. <b>Como o descarte se correlaciona com a melhoria de qualidade</b> &mdash; a curva da seção 1.</p>
                <p style='margin: 0;'>4. <b>Quais barreiras de tratamento compõem a linha</b> &mdash; cloração sempre, com ultravioleta, ozônio e filtro de polimento como estágios opcionais.</p>
                <p style='margin: 6px 0 0 0;'>A curva da seção 1 é uma <b>correlação de projeto</b>, para dimensionar o descarte e comparar alternativas. Não substitui análise laboratorial: a norma exige monitoramento com frequência mínima semestral (item 4.6.7).</p>
            </div>

            <h3 style='color: #0369a1;'>1. Fundamentação Científica da Remoção de Poluentes por Descarte Inicial (Modelo Wash-Off)</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Durante os períodos de estiagem antecedentes (<i>Antecedent Dry Periods — ADP</i>), poeiras atmosféricas, fezes de pássaros, fuligem veicular de combustão e matéria orgânica se acumulam sobre a cobertura.
                O mecanismo de carreamento e lavagem das impurezas fundamenta-se nos trabalhos seminais (<b>Yaziz et al., 1989</b>; <b>Martinson & Thomas, 2005</b>) e na pesquisa experimental recente do grupo:
            </p>

            <div style='background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; margin: 10px 0; border-radius: 0 6px 6px 0;'>
                <b style='color: #15803d;'>Referência Científica Central Recente (UFSC):</b><br/>
                <b>MAYKOT, J. K.; VAZ, I. C. M.; GHISI, E. (2025).</b><br/>
                <i>"Characterisation of First Flush for Rainwater Harvesting Purposes in Buildings"</i>. <b>Water</b>, v. 17, n. 12, art. 1772. DOI: <a href='https://doi.org/10.3390/w17121772' style='color: #087f6b;'>10.3390/w17121772</a>.<br/>
                <span style='font-size: 12px; color: #374151; line-height: 1.5; display: inline-block; margin-top: 4px;'>
                Este trabalho experimental caracterizou o escoamento inicial em cobertura real de fibrocimento no sul do Brasil ao longo de diversos eventos e períodos secos antecedentes.
                Foram monitorados e modelados parâmetros físico-químicos e microbiológicos (pH, sólidos suspensos totais — SST, turbidez, cor aparente, condutividade, coliformes totais e <i>Escherichia coli</i>),
                demonstrando fortes correlações estatísticas entre turbidez, cor e cargas bacterianas, comprovando a eficácia e a indispensabilidade do descarte inicial calibrado (1,0 a 2,0 mm) para garantir a segurança sanitária em usos não potáveis.
                </span>
            </div>

            <h4 style='color: #0369a1;'>Formulação Matemática de Decaimento Exponencial de Lavagem</h4>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                O Triton emprega a formulação analítica exponencial proposta por <b>Martinson & Thomas (2005)</b> e validada experimentalmente por <b>Maykot, Vaz & Ghisi (2025)</b>:<br/>
                <code style='background-color: #f1f5f9; padding: 6px 10px; border-radius: 4px; font-size: 13px; color: #0284c7; display: inline-block; margin: 6px 0;'>
                E(d) = 100\% × ( 1 − e<sup>−k · d</sup> )
                </code><br/>
                Onde:
                <ul style='font-size: 12px; line-height: 1.5; color: #334155;'>
                    <li><b>E(d):</b> Eficiência percentual acumulada de remoção do contaminante (%);</li>
                    <li><b>d:</b> Lâmina de descarte inicial aplicada (mm), onde 1,0 mm = 1,0 litro descartado por m² de telhado;</li>
                    <li><b>k:</b> Coeficiente de lavagem (mm<sup>−1</sup>), adotado por fração de impureza. Os valores situam-se na faixa relatada pela literatura de <i>first flush</i> e são parâmetros de projeto, não constantes medidas, razão pela qual permanecem editáveis:
                        <ul>
                            <li><b>Sólidos Grosseiros e Sedimentáveis (k = 1,6 mm<sup>−1</sup>):</b> Partículas pesadas desprendidas rapidamente pelo impacto inicial das gotas (<i>E ≈ 79,8% para 1,0 mm; E ≈ 95,9% para 2,0 mm</i>).</li>
                            <li><b>Turbidez Fina e Fuligem (k = 1,3 mm<sup>−1</sup>):</b> Partículas coloidais e poeiras finas atmosféricas (<i>E ≈ 72,7% para 1,0 mm; E ≈ 92,6% para 2,0 mm</i>).</li>
                            <li><b>Carga Bacteriológica e Biofilme (k = 1,1 mm<sup>−1</sup>):</b> Coliformes e biofilmes aderidos às telhas (<i>E ≈ 66,7% para 1,0 mm; E ≈ 88,9% para 2,0 mm</i>).</li>
                        </ul>
                    </li>
                </ul>
            </p>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 12px 0; border-radius: 0 6px 6px 0;'>
                <b>Cálculo da Turbidez Efetiva Pós-Descarte:</b><br/>
                <code style='background-color: #ffffff; padding: 4px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12px; color: #0284c7; display: inline-block; margin-top: 4px;'>
                Turbidez<sub>pós-descarte</sub> = max( 1{,}5 NTU, Turbidez<sub>bruta</sub> × [ 1 − E<sub>turb</sub> / 100 ] )
                </code><br/>
                <span style='font-size: 11.5px; color: #64748b;'>Turbidez bruta média de referência sem descarte = 45,0 NTU.</span>
            </div>

            <h3 style='color: #0369a1;'>2. Dimensionamento Paramétrico da ETAP e Origem dos Dados</h3>
            
            <table style='width: 100%; border-collapse: collapse; font-size: 12px; margin: 10px 0;'>
                <thead>
                    <tr style='background-color: #f1f5f9; text-align: left;'>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Etapa de Tratamento</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Especificação Técnica</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Malha / Critério de Projeto</th>
                        <th style='padding: 8px; border: 1px solid #cbd5e1;'>Origem dos Dados & Custos</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>1. Pré-filtração Mecânica</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Filtro autolimpante tipo Vórtex (DN 100 até 150 m², DN 150 até 400 m², Ciclônico DN 200 >400 m²)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Malha em aço inox AISI 304 (350 µm a 500 µm), rendimento hidráulico &gt;90%</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Catálogos técnicos (3P Technik / Wisy) e SINAPI (R$ 650 a R$ 2.800)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>2. Desinfecção Química (Cloração)</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Dosador de passagem por erosão com pastilhas de Hipoclorito de Cálcio (65% cloro ativo)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Dosagem: 0,5 a 2,0 mg/L de Cl<sub>2</sub> ativo (NBR 15527:2019, item 4.6.5; máximo permitido de 5 mg/L). Sempre presente: é a única barreira que deixa residual livre, o que ultravioleta e ozônio não fazem.</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Dosador R$ 280; Químico: R$ 38,00/kg; Fator ACV: 1,72 kg CO<sub>2</sub>e/kg de pastilha (Ecoinvent 3.8, hipoclorito de sódio como aproximação, na base de cloro ativo)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>3. Desinfecção Física (Radiação UV)</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Reator ultravioleta germicida com lâmpada de vapor de mercúrio a 254 nm</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Dose UV &ge; 30 mJ/cm² (NSF/ANSI 55), potência de 25W (&le;200 m³/ano) a 55W</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>R$ 1.200 a R$ 2.200; Vida útil de 9.000 h (troca anual de lâmpada: R$ 180 a R$ 320)</td>
                    </tr>
                    <tr>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'><b>4. Filtração de Polimento</b></td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Carvão Ativado em Bloco (5–10 µm) para usos nobres ou leito de areia/plissado (20 µm)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>Adsorção de cor residual, odores e compostos voláteis para lavagem de roupas (Classe 4)</td>
                        <td style='padding: 8px; border: 1px solid #e2e8f0;'>R$ 380 a R$ 550; Troca anual de refil de carvão: R$ 90 a R$ 150/ano</td>
                    </tr>
                </tbody>
            </table>

            <h3 style='color: #0369a1;'>3. Matriz de Classes de Qualidade por Uso</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                A água pluvial tratada é enquadrada em quatro classes de uso, com os parâmetros abaixo:
            </p>
            <ul style='font-size: 12.5px; line-height: 1.6; color: #334155;'>
                <li><b>Classe 1 (Bacias Sanitárias e Mictórios):</b> Turbidez &le; 5,0 NTU; Cor Aparente &le; 15 uH; pH 6,0 a 9,0; Cloro Residual Livre 0,5 a 2,0 mg/L; Coliformes Termotolerantes &le; 200 UFC/100 mL.</li>
                <li><b>Classe 2 (Irrigação Paisagística, Lavagem de Pisos e Veículos):</b> Turbidez &le; 5,0 NTU; Cor &le; 15 uH; pH 6,0 a 9,0; Cloro Residual 1,0 a 3,0 mg/L; Coliformes = 0 (Ausência).</li>
                <li><b>Classe 3 (Torres de Resfriamento e Caldeiras Industriais):</b> Turbidez &le; 2,0 NTU; Cor &le; 10 uH; pH 6,5 a 8,5; Cloro Residual 1,0 a 2,5 mg/L; Coliformes = 0 (Ausência).</li>
                <li><b>Classe 4 (Lavagem de Roupas e Usos Nobres Não Potáveis):</b> Turbidez &le; 2,0 NTU; Cor &le; 5 uH; pH 6,5 a 8,5; Cloro Residual 0,5 a 1,5 mg/L; Coliformes = 0 (Ausência). Exige filtração por carvão ativado.</li>
            </ul>

            <div style='background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 14px 0; border-radius: 0 6px 6px 0; font-size: 12.5px; line-height: 1.6;'>
                <p style='margin: 0 0 6px 0;'><b>Requisitos da NBR 15527:2019.</b> A norma estabelece um conjunto único de parâmetros mínimos, sem matriz de classes de uso: o item 4.6.3, Tabela 1, estabelece um <b>único</b> conjunto de parâmetros mínimos, válido para todos os usos não potáveis listados em 4.1.7.</p>
                <table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse; border-color: #cbd5e1; width: 60%; margin: 8px 0; font-size: 12px; background: #ffffff;'>
                    <tr style='background-color: #0284c7; color: #ffffff;'><th align='left'>Parâmetro</th><th align='left'>Valor</th></tr>
                    <tr><td><i>Escherichia coli</i></td><td>&lt; 200 / 100 mL</td></tr>
                    <tr><td>Turbidez</td><td>&lt; 5,0 uT</td></tr>
                    <tr><td>pH</td><td>6,0 a 9,0</td></tr>
                </table>
                <p style='margin: 0 0 6px 0;'>O item 4.6.5 acrescenta cloro residual livre entre <b>0,5 e 2,0 mg/L</b>, com máximo permitido de 5 mg/L. Não há parâmetro de cor na norma.</p>
                <p style='margin: 0;'><b>Como a tabela acima é montada.</b> A Classe 1 corresponde ao conjunto normativo, com dois acréscimos de projeto: um limite de cor, ausente da norma, e coliformes termotolerantes no lugar de <i>E. coli</i>, sendo aquele o parâmetro mais restritivo. As Classes 2 a 4 formam um escalonamento adotado por este programa para usos de exposição distinta — apoiado na abordagem por uso da edição de 2007 e na prática corrente — e valem como orientação de projeto, permanecendo a Classe 1 o requisito normativo em todos os casos.</p>
            </div>

            <h3 style='color: #0369a1;'>4. Por que estes parâmetros, e não outros</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Cinco grandezas bastam para decidir se uma água serve a um uso não potável. Cada uma responde a uma pergunta distinta, e nenhuma substitui as demais.
            </p>
            <table border='1' cellspacing='0' cellpadding='8' style='border-collapse: collapse; border-color: #cbd5e1; width: 100%; margin-top: 8px; font-size: 12px;'>
                <tr style='background-color: #0284c7; color: #ffffff;'>
                    <th align='left' style='width: 22%;'>Parâmetro</th>
                    <th align='left'>Por que é medido</th>
                </tr>
                <tr>
                    <td><b>Turbidez</b></td>
                    <td>É o indicador operacional da eficiência da desinfecção. Partículas em suspensão abrigam microrganismos e consomem cloro, de modo que uma água turva pode receber dose adequada e ainda assim não ficar desinfetada. Turbidez é medida em minutos e em campo; a contagem microbiológica leva 24 horas em laboratório. Por isso ela é o parâmetro de controle contínuo, e o exame bacteriológico, o de verificação periódica.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Cor aparente</b></td>
                    <td>Sinaliza matéria orgânica dissolvida e material lixiviado da cobertura. Importa por dois motivos: consome cloro sem que a turbidez acuse, e é a razão pela qual usuários rejeitam a água em usos visíveis — lavagem de roupa acima de tudo. É o parâmetro mais restritivo da Classe 4 justamente por isso.</td>
                </tr>
                <tr>
                    <td><b>pH</b></td>
                    <td>Governa a eficácia do cloro e a agressividade da água às tubulações. Acima de pH 8 a fração de ácido hipocloroso — a espécie efetivamente desinfetante — cai acentuadamente, e o mesmo residual medido desinfeta menos. Abaixo de pH 6 a água ataca metais e argamassas. A faixa é uma condição para que o cloro residual signifique alguma coisa.</td>
                </tr>
                <tr style='background-color: #f8fafc;'>
                    <td><b>Cloro residual livre</b></td>
                    <td>Único parâmetro que atesta proteção <i>continuada</i>: mede a capacidade que resta de inativar contaminação introduzida depois do tratamento, dentro do reservatório e da rede. Tem mínimo e máximo — abaixo do mínimo não há barreira; acima do máximo aparecem odor, sabor e subprodutos de desinfecção. É por isso uma faixa, e não um limite superior.</td>
                </tr>
                <tr>
                    <td><b>Coliformes termotolerantes</b></td>
                    <td>Indicador de contaminação fecal, que em cobertura vem sobretudo de aves e pequenos animais. Não se mede o patógeno diretamente: mede-se um organismo abundante, fácil de cultivar e que acompanha a contaminação. A Classe 1 admite até 200 UFC/100 mL porque a bacia sanitária tem exposição humana mínima; as demais classes exigem ausência porque envolvem aerossol, contato ou contato com roupa.</td>
                </tr>
            </table>
            <p style='font-size: 12.5px; line-height: 1.6; margin-top: 10px;'>
                <b>Duas ausências deliberadas.</b> Não se avalia potabilidade: a água pluvial deste programa destina-se a usos não potáveis, e comparar seus limites com os da <b>Portaria GM/MS n.º 888/2021</b> — que rege a potabilidade no Brasil — levaria à conclusão errada de que o sistema falha num requisito que não se propõe a atender. E não se avaliam metais nem compostos orgânicos: seriam pertinentes em coberturas metálicas antigas ou em áreas de intensa poluição atmosférica, casos que exigem campanha de amostragem própria e estão fora do alcance de um pré-dimensionamento.
            </p>
            """
        return self._create_browser(html, secao='qualidade')

    def create_tab_indicators_performance(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>📊 Water Performance Indicators</h2>
            
            <h3 style='color: #0369a1;'>Potable Water Savings Potential ($E_{pot}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Percentage of total water demand that was saved by utilizing the pluvial system throughout the simulation:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                E<sub>pot</sub> (%) = ( Rainwater Volume Actually Consumed / Total Water Demand ) × 100%
                </code>
            </p>

            <h3 style='color: #0369a1;'>Daily Satisfaction Reliability</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Classification of days of the year based on the rainwater demand satisfaction level:
                <ul>
                    <li><b>Full Satisfaction (100%):</b> The pluvial tank fully met the daily rainwater demand.</li>
                    <li><b>Partial Satisfaction:</b> The tank only met a fraction of the demand.</li>
                    <li><b>No Satisfaction (0%):</b> The tank was completely empty.</li>
                </ul>
            </p>

            <h3 style='color: #0369a1;'>Overflow Volume (Spillover)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The excess rainwater wasted by spilling over when the cistern reaches its maximum capacity.
            </p>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>📊 Indicadores de Desempenho Hídrico</h2>
            
            <h3 style='color: #0369a1;'>Potencial de Economia de Água Potável ($E_{pot}$)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Percentual da demanda total de água potável que foi economizado pelo uso do sistema pluvial ao longo de toda a simulação:<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                E<sub>pot</sub> (%) = ( Volume Pluvial Efetivamente Consumido / Demanda Total de Água Potável ) × 100%
                </code>
            </p>

            <h3 style='color: #0369a1;'>Garantia / Confiabilidade de Atendimento dos Dias</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Classificação dos dias do ano segundo o nível de atendimento da demanda pluvial:
                <ul>
                    <td><b>Atendimento Total (100%):</b> O reservatório supriu integralmente a demanda pluvial do dia.</td>
                    <td><b>Atendimento Parcial:</b> O reservatório atendeu apenas uma fração da demanda.</td>
                    <td><b>Sem Atendimento (0%):</b> O reservatório estava vazio no dia.</td>
                </ul>
            </p>

            <h3 style='color: #0369a1;'>Volume Extravasado / Transbordado (Spillover)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Volume de água pluvial excedente desperdiçado por extravasamento quando o reservatório atinge sua capacidade máxima.
            </p>
            """
        return self._create_browser(html, secao='indicadores')

    def create_tab_economics(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>💰 Financial Indicators and Economic Methodology</h2>

            <h3 style='color: #0369a1;'>Inflation, tariff escalation and indices</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                In Triton, <b>inflation indexes additional O&amp;M costs only</b>. Water, sewage and electricity tariff adjustments are separate and change savings and pumping-cost tariffs at the chosen adjustment interval. If the same rate is entered in both fields, the model intentionally applies both effects to their respective flows; use separate assumptions to avoid an unintended double count. The optional IPCA, INPC, IGP-DI and IGP-M profiles only fill editable O&amp;M references; they are not live quotations and are never applied unless selected. INCC may still be useful when reviewing the initial CAPEX, but it is not offered as an O&amp;M inflation profile.
            </p>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The tariff-adjustment profile appears before the water/sewage and electricity percentage fields it can populate. The 2025 planning profile is only a starting point: there is no single Brazilian national average for water and sewage, because adjustments follow each provider, contract and local regulator. Confirm water/sewage values locally and confirm electricity values with the relevant distributor and ANEEL information before issuing a report.
            </p>
            
            <h3 style='color: #0369a1;'>Net Present Value (NPV)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                NPV measures the net financial return of the system in current values, discounting future cash flows by the Minimum Acceptable Rate of Return (MARR / TMA):<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                NPV = ∑ [ Net_Cash_Flow<sub>t</sub> / (1 + MARR)<sup>t</sup> ] - CAPEX
                </code>
            </p>

            <h3 style='color: #0369a1;'>Internal Rate of Return (IRR)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The annual discount rate at which the NPV of the investment becomes exactly zero. If IRR > MARR, the project is economically viable.
            </p>

            <h3 style='color: #0369a1;'>Simple and Discounted Payback</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                The time (in years) required for the cumulative cash flows of water savings to recoup the initial investment (CAPEX). The discounted payback considers the time value of money via MARR.
            </p>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>💰 Indicadores Financeiros e Metodologia Econômica</h2>

            <h3 style='color: #0369a1;'>Inflação, reajuste tarifário e índices</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                No Triton, a <b>inflação indexa somente os custos adicionais de O&amp;M</b>. Os reajustes de água, esgoto e energia são independentes e alteram as tarifas das economias e do bombeamento no intervalo configurado. Se a mesma taxa for inserida nos dois campos, o modelo aplica intencionalmente os dois efeitos aos seus fluxos correspondentes; use premissas distintas para evitar dupla contagem não desejada. Os perfis opcionais de IPCA, INPC, IGP-DI e IGP-M apenas preenchem referências editáveis de O&amp;M: não são cotações atualizadas e nunca são aplicados sem seleção explícita. O INCC pode continuar útil na revisão do CAPEX inicial, mas não é oferecido como perfil de inflação para O&amp;M.
            </p>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O perfil de reajuste tarifário aparece antes dos percentuais de água/esgoto e energia que ele pode preencher. A referência de planejamento de 2025 é apenas um ponto de partida: não existe média nacional única de água e esgoto, pois o reajuste depende do prestador, contrato e regulador local. O catálogo de 652 municípios do Triton foi auditado e validado em <b>27/08/2026</b>; confirme sempre a vigência de novos reajustes locais de água/esgoto e energia na distribuidora/ANEEL antes de emitir um relatório executivo.
            </p>
            
            <h3 style='color: #0369a1;'>Valor Presente Líquido (VPL)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O VPL mede o retorno financeiro líquido do sistema em moeda corrente atual, desconsiderando o efeito do tempo pela Taxa Mínima de Atratividade (TMA):<br/>
                <code style='background-color: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 13px; color: #0284c7;'>
                VPL = ∑ [ Fluxo_Líquido<sub>t</sub> / (1 + TMA)<sup>t</sup> ] - CAPEX
                </code>
            </p>

            <h3 style='color: #0369a1;'>Taxa Interna de Retorno (TIR)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Taxa de desconto anual para a qual o VPL do investimento se torna exatamente igual a zero. Se TIR > TMA, o projeto é economicamente viável.
            </p>

            <h3 style='color: #0369a1;'>Payback Simples e Descontado</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Tempo (em anos) necessário para que o fluxo de caixa acumulado das economias de água compense o investimento inicial (CAPEX). O payback descontado considera a perda do valor do dinheiro no tempo pela TMA.
            </p>
            """
        return self._create_browser(html, secao='economico')

    def create_tab_discussion_average_values(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>💡 Technical Discussion: Average Values vs. Continuous Daily Simulation</h2>
            
            <h3 style='color: #0369a1;'>1. The Illusion of Monthly or Annual Averages</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                In water engineering design, relying on <b>monthly or annual averages of rainfall and consumption</b> (such as the simplified Rippl method or basic table estimates) leads to inaccurate or severely overestimated predictions about rainwater availability.
            </p>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                For example, in a month with 150 mm of rain, if all that rain occurs concentrated in just 2 days of extreme storms, the cistern will overflow and dump most of the water in those initial days (<i>spillover</i>). During the subsequent 28 dry days, the cistern will remain empty and the building will depend entirely on the public potable water grid.
            </p>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Simplified calculations based on averages would erroneously suggest that 150 mm satisfies the whole month's demand (5 mm/day), completely hiding the overflows and the supply failures.
            </p>

            <h3 style='color: #0369a1;'>2. Why use continuous daily simulation?</h3>
            <ul style='font-size: 12.5px; line-height: 1.6; color: #334155;'>
                <li><b>Captures Real Dry Spells (CDD):</b> Accounts for the exact sequence of consecutive dry days.</li>
                <li><b>First-flush depth:</b> Subtracts <i>df</i> from the rainfall of each day on which the rule applies; a day with rainfall at or below <i>df</i> yields no capture.</li>
                <li><b>Sequence-dependent overflow:</b> Computes overflow under the stated daily YAS assumptions when the cistern reaches capacity.</li>
                <li><b>Dynamic Consumption & Pumping:</b> Simulates the daily interaction between lower cistern, upper tank, and pump cycles.</li>
            </ul>

            <div style='background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 12px; margin-top: 15px; border-radius: 4px;'>
                <h4 style='color: #0369a1; margin: 0px 0px 6px 0px;'>📌 Methodological Conclusion of Triton:</h4>
                <p style='font-size: 12px; margin: 0px; line-height: 1.5; color: #0f172a;'>
                    Continuous daily simulation preserves the observed order of wet and dry days and is therefore more informative than monthly averages for storage analysis. Its results remain conditional on data quality, timestep, model structure and demand assumptions; they require sensitivity analysis and professional validation.
                </p>
            </div>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>💡 Discussão Técnica: Valores Médios vs. Simulação Diária Contínua</h2>
            
            <h3 style='color: #0369a1;'>1. A Ilusão das Médias Mensais ou Anuais</h3>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Em projetos de engenharia hídrica, a utilização de <b>valores médios mensais ou anuais de chuva e consumo</b> (como no Método de Rippl simplificado ou métodos empíricos de prateleira) gera estimativas imprecisas ou severamente superestimadas sobre o aproveitamento real de água pluvial.
            </p>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                Em um mês em que chove 150 mm, por exemplo, se toda essa chuva ocorrer concentrada em apenas 2 dias de tempestade extrema, a cisterna irá transbordar e descartar a maior parte da água nos dias iniciais (<i>spillover</i>). Nos 28 dias subsequentes de estiagem, a cisterna estará vazia e o sistema dependerá integralmente da rede pública de água potável. 
            </p>
            <p style='font-size: 12.5px; line-height: 1.6;'>
                No cálculo simplificado por médias, a conta sugeriria erroneamente que os 150 mm supririam a demanda do mês inteiro (5 mm/dia), ocultando o transbordamento e a falha de atendimento.
            </p>

            <h3 style='color: #0369a1;'>2. Por que usar a simulação diária contínua?</h3>
            <ul style='font-size: 12.5px; line-height: 1.6; color: #334155;'>
                <li><b>Captura da Estiagem Real (CDD):</b> Considera a sequência exata de dias secos consecutivos.</li>
                <li><b>Lâmina de descarte:</b> Subtrai <i>df</i> da chuva de cada dia em que a regra se aplica; um dia com chuva igual ou menor que <i>df</i> não produz captação.</li>
                <li><b>Extravasamento dependente da sequência:</b> Calcula a perda sob as premissas diárias do YAS quando a cisterna atinge a capacidade.</li>
                <li><b>Dinâmica de Consumo e Recalque:</b> Avalia a interação diária entre o reservatório inferior, o reservatório superior e o acionamento da motobomba.</li>
            </ul>

            <div style='background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 12px; margin-top: 15px; border-radius: 4px;'>
                <h4 style='color: #0369a1; margin: 0px 0px 6px 0px;'>📌 Conclusão Metodológica do Triton:</h4>
                <p style='font-size: 12px; margin: 0px; line-height: 1.5; color: #0f172a;'>
                    A simulação diária contínua preserva a ordem observada de dias secos e chuvosos e, por isso, é mais informativa que médias mensais para analisar armazenamento. Os resultados continuam condicionados à qualidade dos dados, ao passo temporal, à estrutura do modelo e às premissas de demanda; exigem sensibilidade e validação profissional.
                </p>
            </div>
            """
        return self._create_browser(html, secao='discussao')

    def create_tab_tariffs_and_opex(self) -> QWidget:
        if get_current_lang() != "pt":
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>⚙️ Tariffs, CAPEX and Operation (Economic Premises)</h2>
            
            <h3 style='color: #0369a1;'>1. Water and Sewage Tariffs by Consumption Tiers (Escalated)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Utilities apply their own rules for availability, consumption tiers, and sewage. The internal editable snapshot is labelled CASAN residential, date 01/04/2026: TFDI flat rate of BRL 46,34/month; BRL 3,08/m³ (0–10), BRL 14,31/m³ (11–25), BRL 19,14/m³ (26–50) and BRL 24,08/m³ (above 50). Sewage rate is configured as 100% of water. The label is metadata, not proof that the table remains current.
                <br/><b>Important:</b> TFDI is a flat availability cost and is not a marginal saving per m³. Always replace rates with local bills and local utility rules.
            </p>

            <h3 style='color: #0369a1;'>2. Sewage Charging Mode</h3>
            <ul style='font-size: 12.5px; line-height: 1.5; color: #334155;'>
                <li><b>Proportional to Water Consumption (Default 100%):</b> Rainwater savings generate equivalent savings in the sewage bill.</li>
                <li><b>Exempt or Fixed Fee:</b> Sewage fees are not affected by the volume of water saved.</li>
            </ul>

            <h3 style='color: #0369a1;'>3. Electricity Bill Taxes & Operating Costs (OPEX)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Pre-sizing assumes three annual reference routines: gutters and pre-filter inspection/cleaning (BRL 240), cistern cleaning and inspection (BRL 320), and pump preventive maintenance (BRL 180, when applicable). These are baseline premises for preliminary studies, not contracted prices.
            </p>
            <h3 style='color: #0369a1;'>4. CAPEX and Pumping System</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                Automatic CAPEX interpolates tank costs based on volume, estimates piping/filters, accessories, and labor according to system scale, and only includes a pump when there is an upper tank. The reference residential pump is 1/2 HP, 0,37 kW, and about 2.280 L/h, with an initial unit cost of BRL 300.
                <br/><b>Mandatory Review:</b> freight, excavation, base, electrical, plumbing, manometric head, filtration, brands, warranty, and labor vary locally and can substantially change the required investment.
            </p>
            <div style='background-color: #fff7ed; border-left: 4px solid #ea580c; padding: 12px; margin-top: 15px; border-radius: 4px;'>
                <b>Professional Use:</b> confirm all items in "Initial Investment", "Motobomba", and "Other Operating Costs" before interpreting NPV, IRR, or payback.
            </div>
            """
        else:
            html = """
            <h2 style='color: #0284c7; margin-top: 0px;'>⚙️ Tarifas, CAPEX e Operação (Premissas Econômicas)</h2>
            
            <h3 style='color: #0369a1;'>1. Tarifas de Água e Esgoto por Faixas de Consumo (Escaladas)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                As concessionárias aplicam regras próprias de disponibilidade, faixas de consumo e esgoto. A fotografia interna editável está identificada como CASAN residencial, data 01/04/2026: TFDI de R$ 46,34/mês; R$ 3,08/m³ (0–10), R$ 14,31/m³ (11–25), R$ 19,14/m³ (26–50) e R$ 24,08/m³ (acima de 50). A tarifa de esgoto está configurada como 100% da água. A identificação é metadado, não prova de que a tabela continue vigente.
                <br/><b>Importante:</b> a TFDI é custo de disponibilidade e não constitui economia marginal por m³. Substitua sempre as tarifas pela fatura e pela regra da concessionária da localidade.
            </p>

            <h3 style='color: #0369a1;'>2. Modo de Cobrança de Esgoto</h3>
            <ul style='font-size: 12.5px; line-height: 1.5; color: #334155;'>
                <li><b>Proporcional ao Consumo de Água (Padrão 100%):</b> A economia de água pluvial gera economia equivalente na tarifa de esgoto.</li>
                <li><b>Isento ou Tarifa Fixa:</b> A tarifa de esgoto não é impactada pelo volume economizado de água potável.</li>
            </ul>

            <h3 style='color: #0369a1;'>3. Impostos na Fatura Elétrica & Custos de Operação (OPEX)</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O pré-dimensionamento adota três rotinas anuais de referência: inspeção/limpeza de calhas e pré-filtro (R$ 240), limpeza e inspeção do reservatório (R$ 320) e manutenção preventiva da motobomba (R$ 180, quando aplicável). Esses valores são premissas para estudos preliminares, não preços contratados.
            </p>
            <h3 style='color: #0369a1;'>4. CAPEX e motobomba</h3>
            <p style='font-size: 12.5px; line-height: 1.5;'>
                O CAPEX automático interpola o custo dos reservatórios pelo volume, estima tubulações/filtros, acessórios e mão de obra a partir do porte do sistema e só inclui motobomba quando houver reservatório superior. A referência de motobomba residencial é 1/2 CV, 0,37 kW e cerca de 2.280 L/h, com custo unitário inicial de R$ 300.
                <br/><b>Revisão obrigatória:</b> frete, escavação, base, abrigo, elétrica, recalque, altura manométrica, filtragem, marcas, garantia e mão de obra variam por local e podem alterar substancialmente o investimento.
            </p>
            <div style='background-color: #fff7ed; border-left: 4px solid #ea580c; padding: 12px; margin-top: 15px; border-radius: 4px;'>
                <b>Uso profissional:</b> confirme todos os itens nas etapas “Investimento Inicial”, “Motobomba” e “Outros Custos Operacionais” antes de interpretar VPL, TIR ou payback.
            </div>
            """
        return self._create_browser(html, secao='tarifas')

    def create_tab_manuals_overview(self) -> QWidget:
        """Painel técnico dos Manuais Oficiais do Triton e do Manual Interativo Web."""
        from triton.core.edition import usa_dados_do_brasil as _brasil_
        ingles = get_current_lang() != "pt"
        is_dark = get_current_theme() == "dark"

        # Paleta de cores responsiva ao tema (superfícies elevadas e contraste refinado)
        canvas_bg = "#0c1815" if is_dark else "#eef2f6"
        card_bg = "#122b25" if is_dark else "#ffffff"
        card_border = "#234d43" if is_dark else "#cbd5e1"
        text_title = "#f8fafc" if is_dark else "#0f172a"
        text_desc = "#a3cdc3" if is_dark else "#475569"
        chip_bg = "#1a4d40" if is_dark else "#f1f5f9"
        chip_fg = "#48d5b7" if is_dark else "#334155"
        feat_border = "#48d5b7" if is_dark else "#0284c7"
        feat_bg = "#122b25" if is_dark else "#ffffff"

        scroll = _ResponsiveScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 4px 2px 4px 0;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {'#234d43' if is_dark else '#cbd5e1'};
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {'#48d5b7' if is_dark else '#94a3b8'};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                width: 0px;
                border: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)

        container = QWidget()
        container.setObjectName("manualsContainer")
        container.setStyleSheet("QWidget#manualsContainer { background-color: transparent; }")

        lay = QVBoxLayout(container)
        lay.setContentsMargins(8, 12, 12, 20)
        lay.setSpacing(14)

        # 1. HERO BANNER DA PLATAFORMA WEB
        hero = QFrame()
        hero.setObjectName("heroBanner")
        hero.setStyleSheet("""
            QFrame#heroBanner {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0.85,
                    stop:0 #0f172a, stop:0.45 #1e293b, stop:1 #0369a1);
                border: 1px solid #334155;
                border-radius: 14px;
            }
        """)
        h_lay = QVBoxLayout(hero)
        h_lay.setContentsMargins(20, 18, 20, 18)
        h_lay.setSpacing(10)

        h_badge = QLabel("PLATAFORMA ONLINE • MANUAL INTERATIVO" if not ingles else "ONLINE PLATFORM • INTERACTIVE MANUAL")
        h_badge.setStyleSheet("background-color: rgba(2, 132, 199, 0.45); border: 1px solid #38bdf8; color: #e0f2fe; font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 10px; letter-spacing: 0.5px;")
        h_badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        h_lay.addWidget(h_badge)

        h_title = QLabel("Manual Interativo e Metodologia Web" if not ingles else "Interactive Web Manual & Methodology")
        h_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.3px;")
        h_lay.addWidget(h_title)

        h_desc = QLabel(
            "Simulações interativas do balanço hídrico diário, formulação matemática detalhada e visualizações conceituais diretamente no navegador."
            if not ingles else
            "Interactive daily water balance simulations, detailed mathematical formulation, and conceptual visualizations directly in the browser."
        )
        h_desc.setStyleSheet("font-size: 12.5px; color: #cbd5e1; line-height: 1.45;")
        h_desc.setWordWrap(True)
        h_desc.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        h_desc.setMinimumWidth(100)
        h_lay.addWidget(h_desc)

        h_btn_row = QHBoxLayout()
        h_btn_row.setSpacing(12)
        h_btn = QPushButton("Abrir Manual Interativo (Web) →" if not ingles else "Open Interactive Manual (Web) →")
        h_btn.setStyleSheet("""
            QPushButton {
                background-color: #38bdf8;
                color: #082f49;
                font-weight: 800;
                font-size: 12px;
                padding: 10px 22px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7dd3fc;
            }
            QPushButton:pressed {
                background-color: #0284c7;
                color: #ffffff;
            }
        """)
        h_btn.setCursor(Qt.PointingHandCursor)
        h_btn.clicked.connect(lambda: abrir_manual_interativo(parent=self))
        h_btn_row.addWidget(h_btn)
        h_btn_row.addStretch(1)
        h_lay.addLayout(h_btn_row)

        lay.addWidget(hero)

        # 2. CABEÇALHO DO ACERVO DE MANUAIS
        sec_box = QVBoxLayout()
        sec_box.setSpacing(3)
        lbl_sec = QLabel("Manuais Técnicos do Triton (PDF)" if not ingles else "Triton Technical Manuals (PDF)")
        lbl_sec.setStyleSheet(f"font-size: 18px; font-weight: 800; color: {'#48d5b7' if is_dark else '#0f172a'}; margin-top: 6px;")
        sec_box.addWidget(lbl_sec)

        lbl_sec_desc = QLabel(
            "Documentos de referência para engenharia, formulação dos métodos, diretrizes por tipologia predial e tabelas de parâmetros."
            if not ingles else
            "Engineering reference documents, method formulation, building typology guidelines, and design tables."
        )
        lbl_sec_desc.setStyleSheet(f"font-size: 12.5px; color: {text_desc};")
        lbl_sec_desc.setWordWrap(True)
        lbl_sec_desc.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        lbl_sec_desc.setMinimumWidth(100)
        sec_box.addWidget(lbl_sec_desc)
        lay.addLayout(sec_box)

        # 3. CARD DE DESTAQUE (Volume Geral)
        feat = QFrame()
        feat.setObjectName("featCard")
        feat.setStyleSheet(f"""
            QFrame#featCard {{
                background-color: {feat_bg};
                border: 1px solid {card_border};
                border-top: 5px solid {feat_border};
                border-radius: 14px;
            }}
        """)
        f_lay = QHBoxLayout(feat)
        f_lay.setContentsMargins(16, 14, 16, 14)
        f_lay.setSpacing(14)

        # Capa Esquerda
        f_left = QVBoxLayout()
        f_left.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        f_left.setSpacing(6)

        lbl_f_img = QLabel()
        lbl_f_img.setFixedSize(120, 85)
        lbl_f_img.setStyleSheet(f"border-radius: 8px; border: 1px solid {card_border}; background-color: {'#15332c' if is_dark else '#f8fafc'};")
        lbl_f_img.setAlignment(Qt.AlignCenter)
        pm_comp = _get_asset_pixmap("icons/capas/thumb_capa_completo.png", 120, 85) or _get_asset_pixmap("manual/figuras/capas/thumb_capa_completo.png", 120, 85)
        if not pm_comp.isNull():
            lbl_f_img.setPixmap(pm_comp)
        f_left.addWidget(lbl_f_img)

        _paginas = PAGINAS_DO_MANUAL_COMPLETO.get(caminho_do_manual_completo(), 0)
        lbl_f_sub = QLabel(f"PDF • {_paginas} PÁGINAS" if not ingles else f"PDF • {_paginas} PAGES")
        lbl_f_sub.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {feat_border};")
        lbl_f_sub.setAlignment(Qt.AlignCenter)
        f_left.addWidget(lbl_f_sub)
        f_lay.addLayout(f_left)

        # Conteúdo Direita
        f_right = QVBoxLayout()
        f_right.setSpacing(6)

        f_badge = QLabel(f"VOLUME GERAL • {_paginas} PÁGINAS" if not ingles else f"GENERAL VOLUME • {_paginas} PAGES")
        f_badge.setStyleSheet(f"background-color: {'#087f6b' if is_dark else '#0284c7'}; color: #ffffff; font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 5px;")
        f_badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        f_right.addWidget(f_badge)

        f_title = QLabel("Manual Triton — Volume Geral" if not ingles else "Triton Manual — General Volume")
        f_title.setStyleSheet(f"font-size: 17px; font-weight: 800; color: {text_title}; margin: 2px 0;")
        f_right.addWidget(f_title)

        f_desc = QLabel(
            "Manual abrangente de engenharia para aproveitamento de água de chuva. Apresenta o método de simulação diária Yield-After-Spill (YAS), coeficientes de escoamento para coberturas, matriz multicritério TOPSIS, análise de ciclo de vida (ACV) e viabilidade econômico-financeira."
            if not ingles else
            "Comprehensive engineering manual for rainwater harvesting. Presents the daily Yield-After-Spill (YAS) simulation method, roof runoff coefficients, TOPSIS multi-criteria matrix, life-cycle assessment (LCA), and economic feasibility."
        )
        f_desc.setStyleSheet(f"font-size: 12px; color: {text_desc}; line-height: 1.5;")
        f_desc.setWordWrap(True)
        f_desc.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        f_desc.setMinimumWidth(100)
        f_right.addWidget(f_desc)

        chips_master = (
            ["Balanço Diário YAS", "Análise Econômica"]
            if not ingles else
            ["Daily YAS Balance", "Economic Analysis"]
        )
        f_chips_lay = QHBoxLayout()
        f_chips_lay.setSpacing(6)
        for ch in chips_master:
            c = QLabel(ch)
            c_bg = "#1a4d40" if is_dark else "#f0f9ff"
            c_fg = "#48d5b7" if is_dark else "#0369a1"
            c.setStyleSheet(f"background-color: {c_bg}; color: {c_fg}; border: 1px solid {'#234d43' if is_dark else '#bae6fd'}; font-size: 10.5px; font-weight: 600; padding: 3px 8px; border-radius: 4px;")
            f_chips_lay.addWidget(c)
        f_chips_lay.addStretch(1)
        f_right.addLayout(f_chips_lay)

        f_btn = QPushButton("Baixar Volume Geral (PDF)" if not ingles else "Download General Volume (PDF)")
        f_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {'#087f6b' if is_dark else '#0284c7'};
                color: #ffffff;
                font-weight: 700;
                font-size: 12px;
                padding: 8px 20px;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {'#066d5c' if is_dark else '#0369a1'};
            }}
            QPushButton:pressed {{
                background-color: {'#044b3f' if is_dark else '#0c4a6e'};
            }}
        """)
        f_btn.setCursor(Qt.PointingHandCursor)
        f_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        _configurar_botao_manual(f_btn, caminho_do_manual_completo(), parent=self)
        f_right.addWidget(f_btn)

        f_lay.addLayout(f_right, stretch=1)
        lay.addWidget(feat)

        # 4. OS 8 MINI-MANUAIS TEMÁTICOS
        vols_data = [
            (1, 32,
             "VOLUME 1 • INTRODUÇÃO" if not ingles else "VOLUME 1 • INTRODUCTION",
             "Volume 1 — Primeiros Passos" if not ingles else "Volume 1 — Getting Started",
             "Instalação, navegação na interface, fluxo de trabalho e conceitos básicos para estruturar o primeiro estudo de aproveitamento pluvial."
             if not ingles else
             "Installation, interface navigation, workflow, and basic concepts for setting up a rainwater harvesting study.",
             ["Instalação e Interface" if not ingles else "Installation & UI", "Fluxo de Trabalho" if not ingles else "Workflow"],
             "icons/capas/thumb_capa_1-comece-aqui.png", "#059669", "#064e3b" if is_dark else "#d1fae5", "#6ee7b7" if is_dark else "#065f46",
             "manual/mini/Manual-Triton-1-comece-aqui.pdf"),
            (2, 122,
             "VOLUME 2 • MÉTODO DE SIMULAÇÃO" if not ingles else "VOLUME 2 • SIMULATION METHOD",
             "Volume 2 — Formulação Matemática" if not ingles else "Volume 2 — Mathematical Formulation",
             "Balanço hídrico diário Yield-After-Spill (YAS), coeficientes de escoamento superficial em coberturas e a lâmina de descarte da primeira chuva (first flush)."
             if not ingles else
             "Daily Yield-After-Spill (YAS) water balance, catchment runoff coefficients, and first-flush diversion rules.",
             ["Balanço Diário YAS" if not ingles else "Daily YAS Balance", "Descarte Inicial" if not ingles else "First-Flush Rule"],
             "icons/capas/thumb_capa_2-metodo.png", "#0284c7", "#0c4a6e" if is_dark else "#e0f2fe", "#7dd3fc" if is_dark else "#0369a1",
             "manual/mini/Manual-Triton-2-metodo.pdf"),
            (3, 220,
             "VOLUME 3 • DIRETRIZES POR TIPOLOGIA" if not ingles else "VOLUME 3 • TYPOLOGY GUIDELINES",
             "Volume 3 — Aplicações Práticas" if not ingles else "Volume 3 — Practical Applications",
             "Diretrizes de projeto e parâmetros específicos para escolas, hospitais, residências e edifícios comerciais."
             if not ingles else
             "Design guidelines and specific parameters for schools, hospitals, residential buildings, and commercial facilities.",
             ["Tipologias Prediais" if not ingles else "Building Typologies", "Casos Práticos" if not ingles else "Case Studies"],
             "icons/capas/thumb_capa_3-guias.png", "#4f46e5", "#312e81" if is_dark else "#e0e7ff", "#a5b4fc" if is_dark else "#3730a3",
             "manual/mini/Manual-Triton-3-guias.pdf"),
            (4, 73,
             "VOLUME 4 • TUTORIAL PASSO A PASSO" if not ingles else "VOLUME 4 • STEP-BY-STEP TUTORIAL",
             "Volume 4 — Dimensionamento e Viabilidade" if not ingles else "Volume 4 — Sizing & Feasibility",
             "Exemplo completo de dimensionamento: dados pluviométricos, capacidade do reservatório, viabilidade financeira e emissões evitadas."
             if not ingles else
             "End-to-end sizing walkthrough: rainfall data, tank storage, financial feasibility, and avoided emissions.",
             ["Dimensionamento" if not ingles else "Tank Sizing", "Viabilidade Econômica" if not ingles else "Economic Feasibility"],
             "icons/capas/thumb_capa_4-tutorial.png", "#7c3aed", "#4c1d95" if is_dark else "#ede9fe", "#c4b5fd" if is_dark else "#5b21b6",
             "manual/mini/Manual-Triton-4-tutorial.pdf"),
            (5, 31,
             "VOLUME 5 • CONFIABILIDADE E INCERTEZA" if not ingles else "VOLUME 5 • RELIABILITY & UNCERTAINTY",
             "Volume 5 — Análise Estatística" if not ingles else "Volume 5 — Statistical Analysis",
             "Confiabilidade temporal e volumétrica, curvas de permanência e avaliação da sensibilidade do tamanho da série histórica."
             if not ingles else
             "Temporal and volumetric reliability, duration curves, and historical series length sensitivity analysis.",
             ["Confiabilidade Hídrica" if not ingles else "Water Reliability", "Curvas de Permanência" if not ingles else "Duration Curves"],
             "icons/capas/thumb_capa_5-confiabilidade.png", "#d97706", "#78350f" if is_dark else "#fef3c7", "#fcd34d" if is_dark else "#92400e",
             "manual/mini/Manual-Triton-5-confiabilidade.pdf"),
            (6, 24,
             "VOLUME 6 • HISTÓRICO E VERIFICAÇÃO" if not ingles else "VOLUME 6 • HISTORY & VERIFICATION",
             "Volume 6 — Histórico e Verificação" if not ingles else "Volume 6 — History & Verification",
             ("Evolução do software, protocolo de verificação frente ao Netuno 4, invariantes de conservação de massa e testes analíticos."
              if _brasil_() else
              "Evolução do software, protocolo de verificação, invariantes de conservação de massa e testes analíticos.")
             if not ingles else
             ("Software evolution, verification against Netuno 4, mass conservation invariants, and analytical benchmarks."
              if _brasil_() else
              "Software evolution, verification protocol, mass conservation invariants, and analytical benchmarks."),
             ["Histórico de Versões" if not ingles else "Version History", "Verificação Numérica" if not ingles else "Numerical Verification"],
             "icons/capas/thumb_capa_6-versoes.png", "#0d9488", "#134e4a" if is_dark else "#ccfbf1", "#5eead4" if is_dark else "#115e59",
             "manual/mini/Manual-Triton-6-versoes.pdf"),
            (7, 40,
             "VOLUME 7 • MODULAÇÃO PROBABILÍSTICA" if not ingles else "VOLUME 7 • PROBABILISTIC MODULATION",
             "Volume 7 — Robustez do Estudo" if not ingles else "Volume 7 — Robustness of the Study",
             "O estudo refeito com premissas sorteadas: catálogo de variáveis, distribuições, Monte Carlo pareado, faixas, probabilidade de retorno e sensibilidade."
             if not ingles else
             "The study rerun with drawn assumptions: variable catalogue, distributions, paired Monte Carlo, bands, payback probability and sensitivity.",
             ["Monte Carlo" if not ingles else "Monte Carlo", "Incerteza" if not ingles else "Uncertainty"],
             "icons/capas/thumb_capa_7-modulacao.png", "#ca8a04", "#713f12" if is_dark else "#fef9c3", "#fde047" if is_dark else "#854d0e",
             "manual/mini/Manual-Triton-7-modulacao.pdf"),
            (8, 217,
             "VOLUME 8 • APÊNDICES E DADOS" if not ingles else "VOLUME 8 • APPENDICES & DATA",
             "Volume 8 — Tabelas de Referência" if not ingles else "Volume 8 — Reference Tables",
             "Tabelas de coeficientes de escoamento, fatores de emissão para ACV, parâmetros tarifários, glossário de termos e referências."
             if not ingles else
             "Runoff coefficient tables, LCA emission factors, tariff parameters, glossary, and references.",
             ["Tabelas de Parâmetros" if not ingles else "Design Tables", "Fatores de Emissão" if not ingles else "Emission Factors"],
             "icons/capas/thumb_capa_8-apendices.png", "#e11d48", "#881337" if is_dark else "#ffe4e6", "#fda4af" if is_dark else "#9f1239",
             "manual/mini/Manual-Triton-8-apendices.pdf"),
        ]

        for vol_num, pags, badge, title, desc, chips, thumb, accent, b_bg, b_fg, rel_pdf in vols_data:
            # O número vem do PDF que acompanha o programa; o escrito acima só vale se
            # o PDF faltar. Antes era só o escrito, e ficava para trás a cada regeração.
            pags = paginas_do_pdf(rel_pdf, pags)
            card = QFrame()
            card.setObjectName(f"miniCard_{vol_num}")
            card.setStyleSheet(f"""
                QFrame#miniCard_{vol_num} {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-left: 6px solid {accent};
                    border-radius: 12px;
                }}
            """)
            c_lay = QHBoxLayout(card)
            c_lay.setContentsMargins(14, 12, 14, 12)
            c_lay.setSpacing(14)

            # Coluna Capa
            col_l = QVBoxLayout()
            col_l.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            col_l.setSpacing(6)

            lbl_i = QLabel()
            lbl_i.setFixedSize(100, 72)
            lbl_i.setStyleSheet(f"border-radius: 8px; border: 1px solid {card_border}; background-color: {'#15332c' if is_dark else '#f8fafc'};")
            lbl_i.setAlignment(Qt.AlignCenter)
            pm = _get_asset_pixmap(thumb, 100, 72) or _get_asset_pixmap(thumb.replace("icons/capas/", "manual/figuras/capas/"), 100, 72)
            if not pm.isNull():
                lbl_i.setPixmap(pm)
            col_l.addWidget(lbl_i)

            lbl_v = QLabel(f"VOL. 0{vol_num} • {pags} PÁG. • PDF" if not ingles else f"VOL. 0{vol_num} • {pags} PGS. • PDF")
            lbl_v.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {accent};")
            lbl_v.setAlignment(Qt.AlignCenter)
            col_l.addWidget(lbl_v)
            c_lay.addLayout(col_l)

            # Coluna Conteúdo
            col_r = QVBoxLayout()
            col_r.setSpacing(6)

            lbl_b = QLabel(badge)
            lbl_b.setStyleSheet(f"background-color: {b_bg}; color: {b_fg}; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.3px; border: 1px solid {accent};")
            lbl_b.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            col_r.addWidget(lbl_b)

            lbl_t = QLabel(title)
            lbl_t.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {text_title}; margin: 2px 0;")
            col_r.addWidget(lbl_t)

            lbl_d = QLabel(desc)
            lbl_d.setStyleSheet(f"font-size: 12px; color: {text_desc}; line-height: 1.5;")
            lbl_d.setWordWrap(True)
            lbl_d.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            lbl_d.setMinimumWidth(100)
            col_r.addWidget(lbl_d)

            # Chips
            chips_l = QHBoxLayout()
            chips_l.setSpacing(6)
            for ch in chips:
                c = QLabel(ch)
                c.setStyleSheet(f"background-color: {chip_bg}; color: {chip_fg}; border: 1px solid {card_border}; font-size: 10.5px; font-weight: 600; padding: 3px 8px; border-radius: 4px;")
                chips_l.addWidget(c)
            chips_l.addStretch(1)
            col_r.addLayout(chips_l)

            # Botão
            btn = QPushButton("Baixar PDF" if not ingles else "Download PDF")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {accent};
                    color: #ffffff;
                    font-weight: 700;
                    font-size: 11.5px;
                    padding: 7px 18px;
                    border-radius: 6px;
                    border: none;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            _configurar_botao_manual(btn, rel_pdf, parent=self)
            col_r.addWidget(btn)

            c_lay.addLayout(col_r, stretch=1)
            lay.addWidget(card)

        scroll.setWidget(container)
        scroll.toHtml = lambda: "Manuais Oficiais & Acervo Técnico Triton"
        return scroll

    def create_tab_references(self) -> QWidget:
        """Lista geral, gerada a partir de `triton.core.bibliography`.

        Era escrita à mão, em dois idiomas, com dezesseis entradas. A conferência
        no Crossref encontrou quatro defeitos nela: Walsh & Lawler com título,
        periódico e páginas errados; Lahdelma grafado com a inicial errada; o
        artigo da MIX Sustentável sem autoria nenhuma, com o título ocupando o
        lugar dos autores; e duas datas de acesso situadas no futuro. Gerar a
        lista de um registro único elimina a classe do problema.
        """
        ingles = get_current_lang() != "pt"
        lang = "en" if ingles else "pt"

        if ingles:
            titulo = "📖 Bibliographic and Normative References"
            intro = (
                "Every record below was retrieved from Crossref, OpenAlex or the publisher — "
                "and each entry states what it supports in this programme. "
                "Section-specific lists appear at the foot of each documentation page."
            )
        else:
            titulo = "📖 Referências Bibliográficas e Normativas"
            intro = (
                "Todos os registros abaixo foram recuperados do Crossref, do OpenAlex ou da página "
                "do periódico, e cada entrada diz o que sustenta neste programa. "
                "As listas por assunto aparecem ao pé de cada página da documentação."
            )

        html = (
            f"<h2 style='color: #0284c7; margin-top: 0px;'>{titulo}</h2>"
            f"<p style='color: #475569;'>{intro}</p>"
            + render_bibliografia_completa(lang)
        )
        return self._create_browser(html)


    def create_tab_cli_usage(self) -> QWidget:
        """Guia conciso do fluxo reproduzível da CLI e de suas análises integradas."""
        if get_current_lang() == "pt":
            html = """
            <h2>⌨️ Linha de comando</h2>
            <p>Use a CLI para automatizar simulações e registrar resultados reproduzíveis. O fluxo recomendado é: <b>criar ou editar → validar → analisar → exportar</b>.</p>
            <h3>1. Criar e validar o projeto</h3>
            <pre>python -m triton.cli init projeto.triton --rainfall Florianopolis1.csv --embed-rainfall
python -m triton.cli validate projeto.triton</pre>
            <p>O arquivo <b>.triton</b> guarda as premissas do edifício, chuva, custos, ACV e pesos TOPSIS. Use <b>--embed-rainfall</b> para torná-lo portátil.</p>
            <h3>2. Rodar a análise completa</h3>
            <pre>python -m triton.cli analyze projeto.triton --analysis all --format json --output resultado.json</pre>
            <p><b>all</b> calcula, para cada volume: balanço hídrico técnico, economia, ACV e TOPSIS. Use <b>run</b> quando quiser somente a simulação técnica.</p>
            <h3>3. Casos comuns</h3>
            <pre># Volume fixo
python -m triton.cli run projeto.triton --volume 5000 --analysis all

# Alterar premissas sem editar o arquivo
python -m triton.cli analyze projeto.triton --set area=150 --set rainwater_share=0.5

# Pesos TOPSIS: técnico,econômico,ambiental
python -m triton.cli analyze projeto.triton --analysis topsis --weights 0.40,0.35,0.25</pre>
            <h3>4. Vários edifícios e climas</h3>
            <pre>python -m triton.cli matrix premissas.json climas.json --analysis all --output-dir resultados</pre>
            <p>O terminal mostra progresso e ETA. A pasta final contém resumo decisório, todas as alternativas, JSON auditável e painel HTML.</p>
            <h3>5. Projetos reais, pasta de chuva e fatores</h3>
            <pre># Cada .triton com sua própria chuva: não há produto cartesiano
python -m triton.cli matrix-projects --projects modelos/ --analysis all --output-dir resultados-modelos

# Um ou mais projetos × todos os CSV/TXT/DAT de uma pasta
python -m triton.cli matrix-projects --projects edificio.triton --rainfall-dir climas/ --analysis all --output-dir resultados-climas</pre>
            <p>Dentro de um <b>.triton</b>, o bloco opcional <code>cli_factorial</code> cria produto cartesiano entre listas de valores. Exemplo: <code>{"cli_factorial":{"factors":{"area":[80,120],"demand_value":[100,150]},"rainfall_files":["climas/a.csv","climas/b.csv"]}}</code>. Sem <code>--rainfall-dir</code>, os arquivos declarados no projeto são usados; com a pasta, ela prevalece. Use <code>--ignore-project-factors</code> para rodar somente os arquivos base.</p>
            <p><b>Saídas:</b> use <b>--format json</b>, <b>csv</b>, <b>html</b> ou <b>xlsx</b> com <b>--output caminho</b>.</p>
            """
        else:
            html = """
            <h2>⌨️ Command line</h2>
            <p>Use the CLI for automation and reproducible simulations. Recommended flow: <b>create or edit → validate → analyse → export</b>.</p>
            <h3>1. Create and validate a project</h3>
            <pre>python -m triton.cli init project.triton --rainfall Florianopolis1.csv --embed-rainfall
python -m triton.cli validate project.triton</pre>
            <p>The <b>.triton</b> file stores building, rainfall, cost, LCA and TOPSIS assumptions. Use <b>--embed-rainfall</b> for a portable project.</p>
            <h3>2. Run the full analysis</h3>
            <pre>python -m triton.cli analyze project.triton --analysis all --format json --output result.json</pre>
            <p><b>all</b> calculates technical balance, economics, LCA and TOPSIS for every volume. Use <b>run</b> for technical simulation only.</p>
            <h3>3. Building × climate matrix</h3>
            <pre>python -m triton.cli matrix premises.json climates.json --analysis all --output-dir results</pre>
            <p>The terminal shows progress and ETA. Output contains a decision summary, all alternatives, auditable JSON and an HTML panel.</p>
            <h3>4. Real projects, rainfall folders and factors</h3>
            <pre># Each .triton with its own rainfall: no Cartesian product
python -m triton.cli matrix-projects --projects models/ --analysis all --output-dir model-results

# One or more projects × every CSV/TXT/DAT series in a folder
python -m triton.cli matrix-projects --projects building.triton --rainfall-dir climates/ --analysis all --output-dir climate-results</pre>
            <p>The optional <code>cli_factorial</code> block inside a <b>.triton</b> expands every combination of its value lists. Add <code>rainfall_files</code> to the same block to use project-declared climate files; <code>--rainfall-dir</code> takes precedence. Use <code>--ignore-project-factors</code> to run only the base files.</p>
            """
        return self._create_browser(html)

