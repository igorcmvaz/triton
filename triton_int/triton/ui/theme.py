"""
Estilo Profissional Refinado Triton (Grupo de Pesquisa em Ambientes Sustentáveis).
Proporciona um visual moderno, limpo e extremamente elegante para a interface desktop.
"""

NETUNO4_CLASSIC_QSS = """
QMainWindow, QDialog {
    background-color: #f2f6f3;
    color: #17332c;
}

QWidget {
    background-color: #f2f6f3;
    color: #17332c;
    font-family: 'Segoe UI', 'SF Pro Text', -apple-system, sans-serif;
    font-size: 10pt;
}

QLabel {
    background-color: transparent;
}

/* Menu Bar Clássica Triton */
QMenuBar {
    background-color: #ffffff;
    color: #17332c;
    border-bottom: 1px solid #d7e3df;
    padding: 3px 6px;
}

QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
    border-radius: 5px;
}

QMenuBar::item:selected {
    background-color: #dff4eb;
    color: #087f6b;
}

QMenu {
    background-color: #ffffff;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 8px;
    padding: 5px;
}

QMenu::item {
    padding: 6px 22px;
    border-radius: 5px;
}

QMenu::item:selected {
    background-color: #087f6b;
    color: #ffffff;
}

/* Barra de contexto: ações frequentes ficam visíveis sem competir com os menus. */
QToolBar#workspaceToolbar {
    background-color: #ffffff;
    border: 0;
    border-bottom: 1px solid #d7e3df;
    padding: 5px 12px;
    spacing: 8px;
}
QToolBar#workspaceToolbar QLabel#topBrand {
    color: #087f6b;
    font-size: 11pt;
    font-weight: 700;
    padding-right: 10px;
}
QToolBar#workspaceToolbar QLabel#workspaceContext {
    color: #526c64;
    font-weight: 600;
    min-width: 175px;
}
QToolBar#workspaceToolbar QToolButton {
    background: transparent;
    color: #17332c;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 10px;
}
QToolBar#workspaceToolbar QToolButton:hover {
    background-color: #dff4eb;
    color: #087f6b;
    border-color: #b7e3d3;
}

/* Botões Padrão Profissional */
QPushButton {
    background-color: #ffffff;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 9px;
    padding: 8px 16px;
    font-size: 9.5pt;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #f0f7f4;
    border-color: #087f6b;
    color: #087f6b;
}

QPushButton:pressed {
    background-color: #dff4eb;
    border-color: #066d5c;
}

QPushButton:disabled {
    background-color: #f2f6f3;
    color: #9eb5ac;
    border-color: #d7e3df;
}

/* Botão de Destaque / Ação Principal (Ex: Simular) */
QPushButton#btn_primary, QPushButton[primary="true"], QPushButton#btn_run {
    background-color: #087f6b;
    color: #ffffff;
    border: 1px solid #066d5c;
    border-radius: 6px;
    font-weight: 600;
}

QPushButton#btn_primary:hover, QPushButton[primary="true"]:hover, QPushButton#btn_run:hover {
    background-color: #066d5c;
    border-color: #044b3f;
}

QPushButton#btn_primary:pressed, QPushButton[primary="true"]:pressed, QPushButton#btn_run:pressed {
    background-color: #044b3f;
}

/* GroupBox com Cartão Branco e Sombra Suave */
QGroupBox {
    font-weight: 600;
    color: #133c32;
    border: 1px solid #d7e3df;
    border-radius: 16px;
    margin-top: 16px;
    padding-top: 20px;
    padding-bottom: 18px;
    padding-left: 20px;
    padding-right: 20px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    background-color: #ffffff;
    color: #087f6b;
    font-weight: bold;
}

/* Inputs de Texto, Combo e SpinBox */
QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #fcfefd;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 9px;
    padding: 7px 12px;
    min-height: 20px;
    selection-background-color: #087f6b;
}

QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #087f6b;
    background-color: #ffffff;
}

/* Oculta as setas de incremento/decremento dos SpinBoxes em todo o sistema */
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 0px;
    height: 0px;
    border: none;
    background: transparent;
}
QSpinBox::up-arrow, QSpinBox::down-arrow,
QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
    image: none;
    width: 0px;
    height: 0px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 0px;
}

/* RadioButtons Interativos Clicáveis */
QRadioButton {
    background-color: transparent;
    color: #17332c;
    padding: 6px 8px;
    border-radius: 5px;
    spacing: 8px;
}

QRadioButton:hover {
    background-color: #dff4eb;
    color: #087f6b;
}

QRadioButton::indicator {
    width: 15px;
    height: 15px;
}

/* CheckBox Interativo */
QCheckBox {
    color: #17332c;
    padding: 4px;
    spacing: 8px;
}

QCheckBox:hover {
    color: #087f6b;
}

/* Tabela de Precipitação e Tabelas Gerais */
QTableWidget {
    background-color: #ffffff;
    color: #17332c;
    gridline-color: #e2ede8;
    border: 1px solid #d7e3df;
    border-radius: 12px;
    selection-background-color: #ffffff;
    selection-color: #17332c;
}

QTableWidget::item:selected {
    background-color: #ffffff;
    color: #17332c;
}

QHeaderView::section {
    background-color: #edf5f1;
    color: #133c32;
    font-weight: 600;
    padding: 9px;
    border: 1px solid #d7e3df;
}

/* TextEdit Observações */
QTextEdit {
    background-color: #fcfefd;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 9px;
    padding: 9px;
    font-size: 10pt;
}

/* Sub-abas QTabWidget */
QTabBar::tab {
    background-color: #e5efe9;
    color: #17332c;
    font-weight: bold;
    padding: 7px 15px;
    border: 1px solid #cbdad5;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 3px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #063c36;
    border-bottom: 3px solid #087f6b;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #f0f7f4;
    color: #087f6b;
}

/* Controles auxiliares */
QScrollArea, QAbstractScrollArea, QTabWidget::pane, QSplitter::handle {
    background-color: #f2f6f3;
    border-color: #d7e3df;
}

QListView, QTreeView, QTableView, QAbstractItemView {
    background-color: #ffffff;
    color: #17332c;
    alternate-background-color: #f8fbf9;
    selection-background-color: #087f6b;
    selection-color: #ffffff;
}

QToolTip {
    background-color: #063c36;
    color: #ffffff;
    border: 1px solid #087f6b;
    padding: 6px;
    border-radius: 5px;
}

QScrollBar:vertical { background: #f2f6f3; width: 14px; margin: 2px; }
QScrollBar::handle:vertical { background: #9ec3b7; min-height: 28px; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background: #087f6b; }
QScrollBar:horizontal { background: #f2f6f3; height: 14px; margin: 2px; }
QScrollBar::handle:horizontal { background: #9ec3b7; min-width: 28px; border-radius: 5px; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; }

QProgressBar { border: 1px solid #cbdad5; border-radius: 6px; text-align: center; background: #ffffff; }
QProgressBar::chunk { background-color: #087f6b; border-radius: 5px; }
QStatusBar { background: #ffffff; color: #526c64; border-top: 1px solid #d7e3df; }

/* Estrutura equivalente ao cabeçalho contextual da edição web. */
QFrame#workspaceHeader {
    background-color: #ffffff;
    border: 0;
    border-bottom: 1px solid #d7e3df;
}
QLabel#workspaceEyebrow {
    color: #789087;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 1px;
}
QLabel#workspaceProject {
    color: #17332c;
    font-size: 11pt;
    font-weight: 700;
}
QLineEdit#workspaceProjectInput {
    background-color: transparent;
    color: #17332c;
    border: 1px solid transparent;
    border-radius: 7px;
    padding: 2px 6px;
    min-width: 250px;
    min-height: 22px;
    font-size: 11pt;
    font-weight: 700;
}
QLineEdit#workspaceProjectInput:hover { background-color: #f2f6f3; border-color: #d7e3df; }
QLineEdit#workspaceProjectInput:focus { background-color: #fcfefd; border: 1px solid #087f6b; }
QLabel#workspaceHint { color: #647b73; font-size: 9pt; }
QPushButton#workspaceSimulate {
    background-color: #087f6b;
    color: #ffffff;
    border: 1px solid #087f6b;
    border-radius: 9px;
    padding: 9px 20px;
    font-weight: 700;
}
QPushButton#workspaceSimulate:hover { background-color: #066d5c; }

/* Seletor de Datas e Calendário Popup */
DatePickerLineEdit {
    padding-right: 28px;
    background-color: #ffffff;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 6px;
}
DatePickerLineEdit:focus {
    border: 1.5px solid #087f6b;
}
QCalendarWidget {
    background-color: #ffffff;
    border: 1px solid #cbdad5;
    border-radius: 8px;
}
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #edf5f1;
    border-bottom: 1px solid #d7e3df;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-height: 36px;
}
QCalendarWidget QToolButton {
    background-color: transparent;
    color: #17332c;
    font-size: 11px;
    font-weight: bold;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 4px 6px;
    margin: 2px;
}
QCalendarWidget QToolButton:hover {
    background-color: #dff4eb;
    color: #087f6b;
    border-color: #b7e3d3;
}
QCalendarWidget QToolButton:pressed {
    background-color: #b7e3d3;
}
QCalendarWidget QSpinBox {
    background-color: #ffffff;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 5px;
    padding: 2px 4px;
    font-weight: bold;
}
QCalendarWidget QMenu {
    background-color: #ffffff;
    color: #17332c;
    border: 1px solid #cbdad5;
    border-radius: 6px;
    padding: 4px;
}
QCalendarWidget QTableView {
    background-color: #ffffff;
    color: #17332c;
    selection-background-color: #087f6b;
    selection-color: #ffffff;
    outline: none;
    border: none;
    font-size: 10pt;
}
QCalendarWidget QTableView:item:hover {
    background-color: #dff4eb;
    color: #087f6b;
    border-radius: 4px;
}
QCalendarWidget QTableView:item:selected {
    background-color: #087f6b;
    color: #ffffff;
    font-weight: bold;
    border-radius: 4px;
}
QCalendarWidget QHeaderView::section {
    background-color: #edf5f1;
    color: #526c64;
    font-weight: 600;
    font-size: 9pt;
    padding: 3px 0px;
    border: none;
    border-bottom: 1px solid #d7e3df;
}
"""

