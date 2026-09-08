"""
Componente Seletor de Datas (DatePickerLineEdit) para Netuno 5.
Permite tanto a digitação manual livre quanto a seleção interativa através de um calendário popup elegante.
"""

from datetime import datetime, date
from typing import Optional, Union

from PySide6.QtWidgets import (
    QLineEdit, QCalendarWidget, QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QApplication, QWidget
)
from PySide6.QtCore import Qt, QDate, Signal, QPoint, QRect, QRectF, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QAction, QKeyEvent

from netuno.ui.translation import tr, get_current_theme


def _create_calendar_icon(is_dark: bool = False, size: int = 20) -> QIcon:
    """Gera um ícone de calendário vetorial nítido e responsivo ao tema."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)

    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)

    main_color = QColor("#38bdf8" if is_dark else "#0284c7")
    accent_color = QColor("#7dd3fc" if is_dark else "#0369a1")
    body_fill = QColor("#27272a" if is_dark else "#ffffff")

    # Contorno externo do calendário
    pen = QPen(main_color, 1.6)
    pen.setJoinStyle(Qt.RoundJoin)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.setBrush(QBrush(body_fill))

    rect = QRectF(2.5, 4.5, size - 5.0, size - 7.0)
    painter.drawRoundedRect(rect, 2.5, 2.5)

    # Faixa superior (cabeçalho do calendário)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(main_color))
    header_rect = QRectF(2.5, 4.5, size - 5.0, 4.5)
    painter.drawRoundedRect(header_rect, 2.0, 2.0)

    # Pinos superiores
    painter.setPen(QPen(accent_color, 1.8, Qt.SolidLine, Qt.RoundCap))
    painter.drawLine(QPoint(int(size * 0.32), 2), QPoint(int(size * 0.32), 5))
    painter.drawLine(QPoint(int(size * 0.68), 2), QPoint(int(size * 0.68), 5))

    # Grade de dias (pontos estilizados)
    dot_color = QColor("#94a3b8" if is_dark else "#64748b")
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(dot_color))

    spacing_x = (size - 8) / 3
    spacing_y = (size - 13) / 2
    for r in range(2):
        for c in range(3):
            cx = 4.5 + c * spacing_x + spacing_x / 2
            cy = 11.0 + r * spacing_y
            painter.drawEllipse(QRectF(cx - 1.0, cy - 1.0, 2.0, 2.0))

    painter.end()
    return QIcon(pix)


class CalendarPopup(QDialog):
    """Diálogo Popup elegante com QCalendarWidget e atalhos rápidos."""

    def __init__(
        self, 
        parent: Optional[QWidget] = None, 
        current_date: Optional[QDate] = None,
        min_date: Optional[QDate] = None,
        max_date: Optional[QDate] = None,
        default_preset_date: Optional[QDate] = None,
    ):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.selected_date: Optional[QDate] = None
        self._default_preset = default_preset_date or QDate(1980, 1, 1)

        is_dark = get_current_theme() == "dark"
        bg_color = "#18181b" if is_dark else "#ffffff"
        border_color = "#3f3f46" if is_dark else "#cbd5e1"
        header_bg = "#27272a" if is_dark else "#f8fafc"
        text_color = "#f4f4f5" if is_dark else "#1e293b"
        btn_bg = "#27272a" if is_dark else "#f1f5f9"
        btn_hover = "#3f3f46" if is_dark else "#e2e8f0"

        # Frame Container Principal com Borda e Sombra
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container = QFrame(self)
        container.setObjectName("calendarContainer")
        container.setStyleSheet(f"""
            QFrame#calendarContainer {{
                background-color: {bg_color};
                border: 1.5px solid {border_color};
                border-radius: 8px;
            }}
        """)
        lay_cont = QVBoxLayout(container)
        lay_cont.setContentsMargins(8, 8, 8, 8)
        lay_cont.setSpacing(6)

        # Widget de Calendário
        self.calendar = QCalendarWidget(self)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.setGridVisible(False)
        self.calendar.setNavigationBarVisible(True)

        if min_date and min_date.isValid():
            self.calendar.setMinimumDate(min_date)
        else:
            self.calendar.setMinimumDate(QDate(1900, 1, 1))

        if max_date and max_date.isValid():
            self.calendar.setMaximumDate(max_date)
        else:
            self.calendar.setMaximumDate(QDate(2100, 12, 31))

        if current_date and current_date.isValid():
            self.calendar.setSelectedDate(current_date)
            self.calendar.showSelectedDate()
        elif self._default_preset.isValid():
            self.calendar.setSelectedDate(self._default_preset)
            self.calendar.showSelectedDate()

        # Estilo refinado para o QCalendarWidget
        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {bg_color};
                border: none;
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: {header_bg};
                border: 1px solid {border_color};
                border-radius: 6px;
                min-height: 34px;
            }}
            QCalendarWidget QToolButton {{
                background-color: transparent;
                color: {text_color};
                font-size: 11px;
                font-weight: bold;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 4px 6px;
                margin: 2px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {btn_hover};
                color: #0284c7;
                border-color: #38bdf8;
            }}
            QCalendarWidget QToolButton:pressed {{
                background-color: {btn_bg};
            }}
            QCalendarWidget QSpinBox {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 2px 4px;
                font-weight: bold;
                selection-background-color: #0284c7;
            }}
            QCalendarWidget QMenu {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 4px;
            }}
            QCalendarWidget QTableView {{
                background-color: {bg_color};
                color: {text_color};
                selection-background-color: #0284c7;
                selection-color: #ffffff;
                outline: none;
                border: none;
                font-size: 9.5pt;
            }}
            QCalendarWidget QTableView:item:hover {{
                background-color: {'#3f3f46' if is_dark else '#e0f2fe'};
                color: {'#38bdf8' if is_dark else '#0284c7'};
                border-radius: 4px;
            }}
            QCalendarWidget QTableView:item:selected {{
                background-color: #0284c7;
                color: #ffffff;
                font-weight: bold;
                border-radius: 4px;
            }}
            QCalendarWidget QHeaderView::section {{
                background-color: {header_bg};
                color: {'#a1a1aa' if is_dark else '#64748b'};
                font-weight: 600;
                font-size: 8.5pt;
                padding: 3px 0px;
                border: none;
                border-bottom: 1px solid {border_color};
            }}
        """)

        self.calendar.clicked.connect(self._on_date_clicked)
        self.calendar.activated.connect(self._on_date_clicked)
        lay_cont.addWidget(self.calendar)

        # Barra de Ações Rápidas (Footer)
        lay_footer = QHBoxLayout()
        lay_footer.setSpacing(6)

        self.btn_today = QPushButton(tr("⚡ Hoje"))
        self.btn_today.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 10.5px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #0284c7;
                color: #ffffff;
                border-color: #0369a1;
            }}
        """)
        self.btn_today.clicked.connect(self._on_today_clicked)
        lay_footer.addWidget(self.btn_today)

        if self._default_preset and self._default_preset != QDate.currentDate():
            preset_year = self._default_preset.year()
            self.btn_preset = QPushButton(f"🎯 {preset_year}")
            self.btn_preset.setToolTip(tr(f"Ir para data padrão ({self._default_preset.toString('dd/MM/yyyy')})"))
            self.btn_preset.setStyleSheet(f"""
                QPushButton {{
                    background-color: {btn_bg};
                    color: {text_color};
                    border: 1px solid {border_color};
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 10.5px;
                }}
                QPushButton:hover {{
                    background-color: {btn_hover};
                    color: #0284c7;
                }}
            """)
            self.btn_preset.clicked.connect(self._on_preset_clicked)
            lay_footer.addWidget(self.btn_preset)

        lay_footer.addStretch()

        self.btn_close = QPushButton(tr("✕ Fechar"))
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {'#a1a1aa' if is_dark else '#64748b'};
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10.5px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                color: {text_color};
                border-color: {border_color};
            }}
        """)
        self.btn_close.clicked.connect(self.reject)
        lay_footer.addWidget(self.btn_close)

        lay_cont.addLayout(lay_footer)
        main_layout.addWidget(container)

    def _on_date_clicked(self, qdate: QDate):
        self.selected_date = qdate
        self.accept()

    def _on_today_clicked(self):
        today = QDate.currentDate()
        self.selected_date = today
        self.calendar.setSelectedDate(today)
        self.accept()

    def _on_preset_clicked(self):
        self.selected_date = self._default_preset
        self.calendar.setSelectedDate(self._default_preset)
        self.accept()

    def show_anchored(self, anchor_widget: QWidget):
        """Posiciona e exibe o popup alinhado abaixo (ou acima) do widget âncora."""
        self.adjustSize()
        popup_size = self.sizeHint()

        anchor_pos = anchor_widget.mapToGlobal(QPoint(0, 0))
        anchor_rect = QRect(anchor_pos, anchor_widget.size())

        screen = anchor_widget.screen() or QApplication.primaryScreen()
        screen_geo = screen.availableGeometry() if screen else QRect(0, 0, 1920, 1080)

        # Tenta posicionar abaixo do widget
        x = anchor_rect.left()
        y = anchor_rect.bottom() + 2

        # Se ultrapassar a margem direita da tela, alinha pela direita do widget
        if x + popup_size.width() > screen_geo.right():
            x = anchor_rect.right() - popup_size.width()
        if x < screen_geo.left():
            x = screen_geo.left() + 10

        # Se ultrapassar a parte inferior da tela, posiciona acima do widget
        if y + popup_size.height() > screen_geo.bottom():
            y = anchor_rect.top() - popup_size.height() - 2
        if y < screen_geo.top():
            y = screen_geo.top() + 10

        self.move(x, y)
        self.exec()


class DatePickerLineEdit(QLineEdit):
    """
    Campo de entrada de texto com suporte completo a digitação manual livre e
    botão de calendário integrado para seleção visual de datas.
    """

    dateChanged = Signal(object)  # Emite datetime.date quando a data muda

    def __init__(
        self, 
        default_text: str = "", 
        parent: Optional[QWidget] = None,
        min_date: Optional[Union[datetime, date, QDate, str]] = None,
        max_date: Optional[Union[datetime, date, QDate, str]] = None,
        default_preset_date: Optional[Union[datetime, date, QDate, str]] = None,
    ):
        super().__init__(default_text, parent)
        self.setPlaceholderText("dd/mm/aaaa")
        self._min_date = self._to_qdate(min_date)
        self._max_date = self._to_qdate(max_date)
        self._default_preset = self._to_qdate(default_preset_date) or QDate(1980, 1, 1)

        is_dark = get_current_theme() == "dark"
        self._action_icon = _create_calendar_icon(is_dark=is_dark)

        # Adiciona ação do botão de calendário na extremidade direita do campo
        self.action_calendar = self.addAction(self._action_icon, QLineEdit.TrailingPosition)
        self.action_calendar.setToolTip(tr("📅 Selecionar data no calendário (F4)"))
        self.action_calendar.triggered.connect(self.show_calendar_popup)

        self.editingFinished.connect(self._on_editing_finished)
        self.textChanged.connect(self._on_text_changed)

    def _to_qdate(self, val: Optional[Union[datetime, date, QDate, str]]) -> Optional[QDate]:
        """Converte diferentes formatos de data para QDate."""
        if val is None:
            return None
        if isinstance(val, QDate):
            return val if val.isValid() else None
        if isinstance(val, (datetime, date)):
            return QDate(val.year, val.month, val.day)
        if isinstance(val, str):
            dt = self._parse_date_string(val)
            if dt:
                return QDate(dt.year, dt.month, dt.day)
        return None

    def _parse_date_string(self, text: str) -> Optional[datetime]:
        """Faz a interpretação inteligente e flexível da string de data."""
        s = str(text).strip()
        if not s or s == "-":
            return None
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%y", "%d.%m.%Y"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        # Ano isolado (ex: "1980")
        if s.isdigit() and len(s) == 4:
            try:
                return datetime(int(s), 1, 1)
            except ValueError:
                pass
        return None

    def get_date(self) -> Optional[date]:
        """Retorna a data atual como objeto datetime.date ou None se inválida."""
        dt = self._parse_date_string(self.text())
        return dt.date() if dt else None

    def get_datetime(self) -> Optional[datetime]:
        """Retorna a data atual como objeto datetime ou None se inválida."""
        return self._parse_date_string(self.text())

    def set_date(self, val: Union[datetime, date, QDate, str]):
        """Define a data no campo formatada como dd/MM/yyyy."""
        if isinstance(val, (datetime, date)):
            self.setText(f"{val.day:02d}/{val.month:02d}/{val.year:04d}")
        elif isinstance(val, QDate) and val.isValid():
            self.setText(val.toString("dd/MM/yyyy"))
        elif isinstance(val, str):
            self.setText(val)

    def set_date_range(
        self, 
        min_date: Optional[Union[datetime, date, QDate, str]], 
        max_date: Optional[Union[datetime, date, QDate, str]]
    ):
        """Define limites mínimo e máximo para o calendário."""
        self._min_date = self._to_qdate(min_date)
        self._max_date = self._to_qdate(max_date)

    def set_default_preset_date(self, preset_date: Union[datetime, date, QDate, str]):
        """Define uma data padrão de contexto para o calendário."""
        self._default_preset = self._to_qdate(preset_date) or QDate(1980, 1, 1)

    def show_calendar_popup(self):
        """Abre o diálogo popup de calendário ancorado abaixo do campo de texto."""
        current_dt = self._parse_date_string(self.text())
        cur_qdate = QDate(current_dt.year, current_dt.month, current_dt.day) if current_dt else self._default_preset

        popup = CalendarPopup(
            parent=self.window(),
            current_date=cur_qdate,
            min_date=self._min_date,
            max_date=self._max_date,
            default_preset_date=self._default_preset,
        )

        popup.show_anchored(self)

        if popup.selected_date and popup.selected_date.isValid():
            date_str = popup.selected_date.toString("dd/MM/yyyy")
            self.setText(date_str)
            self.dateChanged.emit(self.get_date())

    def keyPressEvent(self, event: QKeyEvent):
        """Atalho de teclado F4 ou Alt+Down para abrir o calendário popup."""
        if event.key() == Qt.Key_F4:
            self.show_calendar_popup()
            event.accept()
            return
        if event.key() == Qt.Key_Down and (event.modifiers() & Qt.AltModifier):
            self.show_calendar_popup()
            event.accept()
            return
        super().keyPressEvent(event)

    def _on_editing_finished(self):
        d = self.get_date()
        if d:
            self.dateChanged.emit(d)

    def _on_text_changed(self, text: str):
        d = self.get_date()
        if d:
            self.dateChanged.emit(d)
