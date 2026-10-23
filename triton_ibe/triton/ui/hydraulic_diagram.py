"""
Diagrama Hidráulico 2D Interativo do Sistema de Aproveitamento de Água de Chuva.
Utiliza PySide6 QPainter para desenhar o esquema funcional do sistema em tempo real:
Captação -> Descarte Inicial (First Flush) -> Reservatório Inferior -> Motobomba -> (Reservatório Superior) -> Uso.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath


class HydraulicDiagramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(240)

        # Parâmetros de Entrada para Renderização
        self.area_m2 = 1000.0
        self.discard_mm = 2.0
        self.lower_vol_l = 5000.0
        self.upper_vol_l = 500.0
        self.upper_used = True
        self.potential_pct = 0.0
        self.pluvial_demand_l_day = 1200.0

    def update_params(self, area: float, discard: float, lower_vol: float, upper_vol: float, 
                      upper_used: bool = True, potential_pct: float = 0.0, pluvial_demand: float = 0.0):
        self.area_m2 = area
        self.discard_mm = discard
        self.lower_vol_l = lower_vol
        self.upper_vol_l = upper_vol
        self.upper_used = upper_used
        self.potential_pct = potential_pct
        self.pluvial_demand_l_day = pluvial_demand
        self.update()  # Força repintura

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Fundo do cartão
        painter.fillRect(0, 0, w, h, QColor("#f8fafc"))
        painter.setPen(QPen(QColor("#cbd5e1"), 1))
        painter.drawRoundedRect(1, 1, w - 2, h - 2, 8, 8)

        font_bold = QFont("Segoe UI", 9, QFont.Bold)
        font_small = QFont("Segoe UI", 8)
        font_title = QFont("Segoe UI", 9, QFont.Bold)

        from triton.ui.translation import tr
        # ---------------------------------------------------------------------
        # TOP BAR: TÍTULO E BADGE DE ECONOMIA (SEM SOBREPOSIÇÃO)
        # ---------------------------------------------------------------------
        painter.setPen(QColor("#0369a1"))
        painter.setFont(font_title)
        painter.drawText(12, 22, tr("Esquema Hidráulico 2D"))

        # Badge de Economia no Topo Direito
        badge_w = 120
        badge_x = w - badge_w - 12
        painter.setBrush(QBrush(QColor("#0284c7")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(badge_x, 8, badge_w, 22, 11, 11)

        painter.setPen(QColor("#ffffff"))
        painter.setFont(font_bold)
        painter.drawText(badge_x + 10, 23, f"{tr('Economia')}: {self.potential_pct:.1f}%")

        # ---------------------------------------------------------------------
        # GEOMETRIA PROPORCIONAL DAS ZONAS (ESQUERDA, CENTRO, DIREITA)
        # ---------------------------------------------------------------------
        # 1. TELHADO (Canto Superior Esquerdo)
        # ---------------------------------------------------------------------
        roof_x, roof_y = 20, 38
        roof_w, roof_h = 95, 28

        roof_path = QPainterPath()
        roof_path.moveTo(roof_x, roof_y + roof_h)
        roof_path.lineTo(roof_x + roof_w / 2, roof_y)
        roof_path.lineTo(roof_x + roof_w, roof_y + roof_h)
        roof_path.closeSubpath()

        painter.setBrush(QBrush(QColor("#e0f2fe")))
        painter.setPen(QPen(QColor("#0284c7"), 1.5))
        painter.drawPath(roof_path)

        painter.setPen(QColor("#0f172a"))
        painter.setFont(font_small)
        painter.drawText(int(roof_x + 6), int(roof_y + 20), f"{tr('Telhado')}: {self.area_m2:.0f}m²")

        # Gotas de chuva
        painter.setPen(QPen(QColor("#38bdf8"), 1, Qt.DashLine))
        painter.drawLine(roof_x + 18, roof_y - 8, roof_x + 18, roof_y + 4)
        painter.drawLine(roof_x + 48, roof_y - 12, roof_x + 48, roof_y + 2)
        painter.drawLine(roof_x + 78, roof_y - 8, roof_x + 78, roof_y + 4)

        # ---------------------------------------------------------------------
        # 2. CALHA & FILTRO DE DESCARTE (FIRST FLUSH - TUBO DIRETO VERTICAL)
        # ---------------------------------------------------------------------
        gutter_x = roof_x + roof_w  # x = 115
        gutter_y = roof_y + roof_h  # y = 66
        
        # Filtro / Descarte (First Flush) alinhado no centro do tubo vertical
        flush_w, flush_h = 32, 18
        flush_x = gutter_x - (flush_w / 2)
        flush_y = gutter_y + 15

        # Tubo vertical reto que desce do telhado até o reservatório inferior
        tank_x = 20
        tank_y = h - 75
        tank_w = 105
        tank_h = 58

        painter.setPen(QPen(QColor("#0284c7"), 2.5))
        painter.drawLine(int(gutter_x), int(gutter_y), int(gutter_x), int(tank_y))

        # Desenho do Filtro / Descarte
        painter.setBrush(QBrush(QColor("#ffedd5")))
        painter.setPen(QPen(QColor("#f97316"), 1.2))
        painter.drawRoundedRect(int(flush_x), int(flush_y), flush_w, flush_h, 4, 4)
        painter.setFont(font_small)
        painter.setPen(QColor("#c2410c"))
        painter.drawText(int(flush_x + flush_w + 5), int(flush_y + 13), f"{tr('Descarte')}: {self.discard_mm:.1f}mm")

        # Corpo do Reservatório Inferior (Destacado com borda em azul/verde)
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#0284c7"), 1.8))
        painter.drawRoundedRect(tank_x, tank_y, tank_w, tank_h, 5, 5)

        # Nível de água (simulado ~65%)
        water_h = int(tank_h * 0.65)
        painter.setBrush(QBrush(QColor("#38bdf8")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(tank_x + 2, tank_y + (tank_h - water_h), tank_w - 4, water_h - 2, 3, 3)

        # Texto Reservatório Inferior
        painter.setPen(QColor("#0f172a"))
        painter.setFont(font_bold)
        painter.drawText(tank_x + 8, tank_y + 18, tr("Res. Inferior"))
        painter.setFont(font_bold)
        painter.setPen(QColor("#059669"))
        painter.drawText(tank_x + 8, tank_y + 35, f"{self.lower_vol_l:,.0f} {tr('Litros')}".replace(',', '.'))

        use_w = 90
        use_h = 55
        use_x = w - use_w - 15
        use_y = h - 75

        if self.upper_used:
            # ---------------------------------------------------------------------
            # 4. MOTOBOMBA DE RECALQUE (Para Reservatório Superior)
            # ---------------------------------------------------------------------
            pump_x = tank_x + tank_w + 25
            pump_y = tank_y + 15
            pump_r = 24

            # Tubo de sucção (Res. Inferior -> Motobomba)
            painter.setPen(QPen(QColor("#16a34a"), 2))
            painter.drawLine(tank_x + tank_w, pump_y + (pump_r / 2), pump_x, pump_y + (pump_r / 2))

            # Círculo da Motobomba
            painter.setBrush(QBrush(QColor("#dcfce7")))
            painter.setPen(QPen(QColor("#16a34a"), 1.8))
            painter.drawEllipse(pump_x, pump_y, pump_r, pump_r)

            painter.setPen(QColor("#15803d"))
            painter.setFont(font_bold)
            painter.drawText(int(pump_x + 7), int(pump_y + 16), "M")

            # Rótulo Motobomba
            painter.setFont(font_small)
            painter.drawText(pump_x - 12, pump_y + 36, tr("Motobomba Recalque"))

            up_w = 85
            up_h = 45
            up_x = max(pump_x + 50, w - up_w - 120)
            up_y = 38

            # Tubo de Recalque (Motobomba -> Reservatório Superior)
            recalque_x_up = up_x - 15
            painter.setPen(QPen(QColor("#16a34a"), 2, Qt.DashLine))
            painter.drawLine(int(pump_x + pump_r), int(pump_y + pump_r/2), int(recalque_x_up), int(pump_y + pump_r/2))
            painter.drawLine(int(recalque_x_up), int(pump_y + pump_r/2), int(recalque_x_up), int(up_y + up_h/2))
            painter.drawLine(int(recalque_x_up), int(up_y + up_h/2), int(up_x), int(up_y + up_h/2))

            # Desenho Reservatório Superior
            painter.setBrush(QBrush(QColor("#ffffff")))
            painter.setPen(QPen(QColor("#0284c7"), 1.5))
            painter.drawRoundedRect(up_x, up_y, up_w, up_h, 5, 5)

            # Nível água Res Superior
            up_water_h = int(up_h * 0.65)
            painter.setBrush(QBrush(QColor("#7dd3fc")))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(up_x + 2, up_y + (up_h - up_water_h), up_w - 4, up_water_h - 2, 3, 3)

            painter.setPen(QColor("#0369a1"))
            painter.setFont(font_bold)
            painter.drawText(up_x + 6, up_y + 18, tr("Res. Superior"))
            painter.setFont(font_small)
            painter.drawText(up_x + 6, up_y + 33, f"{self.upper_vol_l:.0f} {tr('Litros')}")

            # Tubo por Gravidade (Reservatório Superior -> Pontos de Uso)
            painter.setPen(QPen(QColor("#0284c7"), 2))
            grav_x = up_x + up_w
            painter.drawLine(grav_x, up_y + int(up_h/2), use_x + int(use_w/2), up_y + int(up_h/2))
            painter.drawLine(use_x + int(use_w/2), up_y + int(up_h/2), use_x + int(use_w/2), use_y)

        else:
            # SEM RESERVATÓRIO SUPERIOR: Sem Motobomba, Uso Direto por Gravidade do Inferior
            line_y = tank_y + int(tank_h / 2)
            painter.setPen(QPen(QColor("#0284c7"), 2.5))
            painter.drawLine(tank_x + tank_w, line_y, use_x, line_y)

            # Rótulo da tubulação de gravidade
            painter.setPen(QColor("#0284c7"))
            painter.setFont(font_small)
            painter.drawText(tank_x + tank_w + 15, line_y - 8, tr("Uso Direto por Gravidade"))

        # ---------------------------------------------------------------------
        # 6. PONTOS DE USO / CONSUMO (Canto Inferior Direito)
        # ---------------------------------------------------------------------
        painter.setBrush(QBrush(QColor("#f0fdf4")))
        painter.setPen(QPen(QColor("#16a34a"), 1.2))
        painter.drawRoundedRect(use_x, use_y, use_w, use_h, 5, 5)

        painter.setPen(QColor("#15803d"))
        painter.setFont(font_bold)
        painter.drawText(use_x + 6, use_y + 20, tr("Pontos de Uso"))
        painter.setFont(font_small)
        painter.drawText(use_x + 6, use_y + 36, f"{self.pluvial_demand_l_day:.0f} L/dia")
