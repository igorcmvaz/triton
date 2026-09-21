"""
Estilo Profissional Refinado Netuno (Grupo de Pesquisa Gestão do Espaço Sustentável).
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

/* Menu Bar Clássica Netuno */
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

/* Tabela de Precipitação */
QTableWidget {
    background-color: #ffffff;
    color: #17332c;
    gridline-color: #e2ede8;
    border: 1px solid #d7e3df;
    border-radius: 12px;
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

UFSC_SUSTAINABILITY_QSS = NETUNO4_CLASSIC_QSS

# Premium de Alto Contraste Dark Gray / Forest Emerald para interface profissional elegante
NETUNO4_DARK_QSS = """
QMainWindow, QDialog {
    background-color: #0b1a17;
    color: #f4fbf8;
}

QWidget {
    background-color: #0b1a17;
    color: #f4fbf8;
    font-family: 'Segoe UI', 'SF Pro Text', -apple-system, sans-serif;
    font-size: 9pt;
}

QLabel {
    background-color: transparent;
}

/* Menu Bar Clássica Netuno */
QMenuBar {
    background-color: #122b25;
    color: #f4fbf8;
    border-bottom: 1px solid #1f4239;
    padding: 3px 6px;
}

QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
    border-radius: 5px;
}

QMenuBar::item:selected {
    background-color: #1a4d40;
    color: #48d5b7;
}

QMenu {
    background-color: #122b25;
    color: #f4fbf8;
    border: 1px solid #1f4239;
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

/* Barra de contexto — superfícies e estados coerentes com o tema escuro. */
QToolBar#workspaceToolbar {
    background-color: #122b25;
    border: 0;
    border-bottom: 1px solid #1f4239;
    padding: 5px 12px;
    spacing: 8px;
}
QToolBar#workspaceToolbar QLabel#topBrand {
    color: #48d5b7;
    font-size: 11pt;
    font-weight: 700;
    padding-right: 10px;
}
QToolBar#workspaceToolbar QLabel#workspaceContext {
    color: #a3cdc3;
    font-weight: 600;
    min-width: 175px;
}
QToolBar#workspaceToolbar QToolButton {
    background: transparent;
    color: #f4fbf8;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 10px;
}
QToolBar#workspaceToolbar QToolButton:hover {
    background-color: #1a4d40;
    color: #48d5b7;
    border-color: #2bb99c;
}

/* Botões Padrão Profissional */
QPushButton {
    background-color: #15332c;
    color: #f4fbf8;
    border: 1px solid #234d43;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 9pt;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #1e473e;
    border-color: #2bb99c;
    color: #48d5b7;
}

QPushButton:pressed {
    background-color: #0d2922;
    border-color: #087f6b;
}

QPushButton:disabled {
    background-color: #0b1a17;
    color: #52736b;
    border-color: #15332c;
}

/* Botão de Destaque / Ação Principal (Ex: Simular) */
QPushButton#btn_primary, QPushButton[primary="true"], QPushButton#btn_run {
    background-color: #087f6b;
    color: #ffffff;
    border: 1px solid #2bb99c;
    border-radius: 6px;
    font-weight: 600;
}

QPushButton#btn_primary:hover, QPushButton[primary="true"]:hover, QPushButton#btn_run:hover {
    background-color: #0d9a80;
    border-color: #48d5b7;
}

QPushButton#btn_primary:pressed, QPushButton[primary="true"]:pressed, QPushButton#btn_run:pressed {
    background-color: #066d5c;
}

/* GroupBox com Cartão Escuro e Sombra Suave */
QGroupBox {
    font-weight: 600;
    color: #ffffff;
    border: 1px solid #1f4239;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 14px;
    padding-bottom: 10px;
    padding-left: 12px;
    padding-right: 12px;
    background-color: #122b25;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    background-color: #122b25;
    color: #48d5b7;
    font-weight: bold;
}

/* Inputs de Texto, Combo e SpinBox */
QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
    background-color: #122b25;
    color: #ffffff;
    border: 1px solid #1f4239;
    border-radius: 6px;
    padding: 5px 8px;
    selection-background-color: #087f6b;
}

QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #2bb99c;
    background-color: #122b25;
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
    color: #f4fbf8;
    padding: 6px 8px;
    border-radius: 5px;
    spacing: 8px;
}

QRadioButton:hover {
    background-color: #1a4d40;
    color: #48d5b7;
}

QRadioButton::indicator {
    width: 15px;
    height: 15px;
}

/* CheckBox Interativo */
QCheckBox {
    color: #f4fbf8;
    padding: 4px;
    spacing: 8px;
}

QCheckBox:hover {
    color: #48d5b7;
}

/* Tabela de Precipitação */
QTableWidget {
    background-color: #122b25;
    color: #ffffff;
    gridline-color: #1f4239;
    border: 1px solid #1f4239;
    border-radius: 6px;
}

QHeaderView::section {
    background-color: #0b1a17;
    color: #ffffff;
    font-weight: 600;
    padding: 6px;
    border: 1px solid #1f4239;
}

/* TextEdit Observações */
QTextEdit {
    background-color: #122b25;
    color: #f4fbf8;
    border: 1px solid #1f4239;
    border-radius: 6px;
    padding: 6px;
    font-size: 9pt;
}

/* Sub-abas QTabWidget com texto em branco e negrito */
QTabBar::tab {
    background-color: #15332c;
    color: #a3cdc3;
    font-weight: bold;
    padding: 7px 15px;
    border: 1px solid #1f4239;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 3px;
}

QTabBar::tab:selected {
    background-color: #0b1a17;
    color: #48d5b7;
    border-bottom: 3px solid #2bb99c;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #1a4d40;
    color: #ffffff;
}

/* Superfícies secundárias e seleção */
QScrollArea, QAbstractScrollArea, QTabWidget::pane, QSplitter::handle {
    background-color: #0b1a17;
    border-color: #1f4239;
}

QListView, QTreeView, QTableView, QAbstractItemView {
    background-color: #122b25;
    color: #f4fbf8;
    alternate-background-color: #0e241f;
    selection-background-color: #087f6b;
    selection-color: #ffffff;
}

QTableWidget::item:selected, QListView::item:selected, QTreeView::item:selected {
    background-color: #087f6b;
    color: #ffffff;
}

QToolTip {
    background-color: #063c36;
    color: #ffffff;
    border: 1px solid #2bb99c;
    padding: 6px;
    border-radius: 5px;
}

QScrollBar:vertical { background: #0b1a17; width: 14px; margin: 2px; }
QScrollBar::handle:vertical { background: #284d43; min-height: 28px; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background: #2bb99c; }
QScrollBar:horizontal { background: #0b1a17; height: 14px; margin: 2px; }
QScrollBar::handle:horizontal { background: #284d43; min-width: 28px; border-radius: 5px; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; }

QProgressBar { border: 1px solid #1f4239; border-radius: 6px; text-align: center; background: #122b25; color: #f4fbf8; }
QProgressBar::chunk { background-color: #087f6b; border-radius: 5px; }
QStatusBar { background: #122b25; color: #a3cdc3; border-top: 1px solid #1f4239; }

/* Seletor de Datas e Calendário Popup (Tema Escuro) */
DatePickerLineEdit {
    padding-right: 28px;
    background-color: #122b25;
    color: #ffffff;
    border: 1px solid #1f4239;
    border-radius: 6px;
}
DatePickerLineEdit:focus {
    border: 1.5px solid #2bb99c;
}
QCalendarWidget {
    background-color: #0b1a17;
    border: 1px solid #1f4239;
    border-radius: 8px;
}
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #122b25;
    border-bottom: 1px solid #1f4239;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-height: 36px;
}
QCalendarWidget QToolButton {
    background-color: transparent;
    color: #f4fbf8;
    font-size: 11px;
    font-weight: bold;
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 4px 6px;
    margin: 2px;
}
QCalendarWidget QToolButton:hover {
    background-color: #1a4d40;
    color: #48d5b7;
    border-color: #2bb99c;
}
QCalendarWidget QToolButton:pressed {
    background-color: #087f6b;
}
QCalendarWidget QSpinBox {
    background-color: #122b25;
    color: #f4fbf8;
    border: 1px solid #1f4239;
    border-radius: 5px;
    padding: 2px 4px;
    font-weight: bold;
    selection-background-color: #087f6b;
}
QCalendarWidget QMenu {
    background-color: #122b25;
    color: #f4fbf8;
    border: 1px solid #1f4239;
    border-radius: 6px;
    padding: 4px;
}
QCalendarWidget QTableView {
    background-color: #0b1a17;
    color: #f4fbf8;
    selection-background-color: #087f6b;
    selection-color: #ffffff;
    outline: none;
    border: none;
    font-size: 10pt;
}
QCalendarWidget QTableView:item:hover {
    background-color: #1a4d40;
    color: #48d5b7;
    border-radius: 4px;
}
QCalendarWidget QTableView:item:selected {
    background-color: #087f6b;
    color: #ffffff;
    font-weight: bold;
    border-radius: 4px;
}
QCalendarWidget QHeaderView::section {
    background-color: #122b25;
    color: #a3cdc3;
    font-weight: 600;
    font-size: 9pt;
    padding: 3px 0px;
    border: none;
    border-bottom: 1px solid #1f4239;
}
"""
