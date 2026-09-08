"""
Janela de Resultado Mensal da Simulação (1:1 com a captura de tela do Netuno 4).
Exibe as médias diárias de cada mês e os totais anuais no formato exato do Netuno 4.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QColor, QFont
from netuno.ui.translation import tr, get_current_theme


class DialogMonthlyValues(QDialog):
    """
    Janela de Resultado Mensal da Simulação (1:1 com a captura de tela do Netuno 4).
    Exibe as médias diárias de cada mês e os totais anuais no formato exato do Netuno 4.
    """
    def __init__(self, parent=None, monthly_stats=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Resultado mensal da simulação"))
        self.resize(880, 440)

        layout = QVBoxLayout()
        table = QTableWidget()
        cols = [
            tr("Mês"),
            tr("Potencial de utilização\nde água pluvial (%)"), 
            tr("Volume consumido de\nágua pluvial (litros)"),
            tr("Volume consumido de\nágua potável (litros)"), 
            tr("Volume extravasado\n(litros)"),
            tr("Atendimento\ncompleto (%)"), 
            tr("Atendimento\nparcial (%)"),
            tr("Sem\natendimento (%)"),
            tr("Média diária\nde recalques")
        ]
        table.setColumnCount(len(cols))
        table.setHorizontalHeaderLabels(cols)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for c in range(1, 9):
            table.horizontalHeader().setSectionResizeMode(c, QHeaderView.Stretch)

        months_pt = [
            tr("Janeiro"), tr("Fevereiro"), tr("Março"), tr("Abril"),
            tr("Maio"), tr("Junho"), tr("Julho"), tr("Agosto"),
            tr("Setembro"), tr("Outubro"), tr("Novembro"), tr("Dezembro")
        ]
        table.setRowCount(14)  # 12 meses + Média + Total ano

        is_dark = get_current_theme() == "dark"
        green_bg = QColor("#0f5132" if is_dark else "#d1e7dd")
        fg_color = QColor("#ffffff" if is_dark else "#000000")
        font_bold = QFont("Segoe UI", 9)
        font_bold.setBold(True)

        if monthly_stats:
            sum_pluv = 0.0
            sum_pot = 0.0
            sum_spill = 0.0
            sum_pot_pct = 0.0
            sum_comp = 0.0
            sum_parc = 0.0
            sum_null = 0.0
            sum_rec = 0.0

            for r, m_name in enumerate(months_pt):
                st = monthly_stats.get(r + 1, {'pot_pct': 0.0, 'pluvial': 0.0, 'potable': 0.0, 'spilled': 0.0, 'comp': 0.0, 'parc': 0.0, 'null': 0.0, 'rec': 0.0})
                
                table.setItem(r, 0, QTableWidgetItem(m_name))
                table.setItem(r, 1, QTableWidgetItem(f"{st['pot_pct']:.2f}".replace('.', ',')))
                table.setItem(r, 2, QTableWidgetItem(f"{st['pluvial']:.2f}".replace('.', ',')))
                table.setItem(r, 3, QTableWidgetItem(f"{st['potable']:.2f}".replace('.', ',')))
                table.setItem(r, 4, QTableWidgetItem(f"{st['spilled']:.2f}".replace('.', ',')))
                table.setItem(r, 5, QTableWidgetItem(f"{st['comp']:.2f}".replace('.', ',')))
                table.setItem(r, 6, QTableWidgetItem(f"{st['parc']:.2f}".replace('.', ',')))
                table.setItem(r, 7, QTableWidgetItem(f"{st['null']:.2f}".replace('.', ',')))
                table.setItem(r, 8, QTableWidgetItem(f"{st['rec']:.2f}".replace('.', ',')))

                sum_pot_pct += st['pot_pct']
                sum_pluv += st['pluvial']
                sum_pot += st['potable']
                sum_spill += st['spilled']
                sum_comp += st['comp']
                sum_parc += st['parc']
                sum_null += st['null']
                sum_rec += st['rec']

            # Linha 13: Média
            item_med = QTableWidgetItem(tr("Média"))
            item_med.setFont(font_bold)
            item_med.setBackground(green_bg)
            item_med.setForeground(fg_color)
            table.setItem(12, 0, item_med)

            avg_pot_pct = sum_pot_pct / 12.0
            avg_pluv = sum_pluv / 12.0
            avg_pot = sum_pot / 12.0
            avg_spill = sum_spill / 12.0
            avg_comp = sum_comp / 12.0
            avg_parc = sum_parc / 12.0
            avg_null = sum_null / 12.0
            avg_rec = sum_rec / 12.0

            vals_med = [
                f"{avg_pot_pct:.2f}".replace('.', ','),
                f"{avg_pluv:.2f}".replace('.', ','),
                f"{avg_pot:.2f}".replace('.', ','),
                f"{avg_spill:.2f}".replace('.', ','),
                f"{avg_comp:.2f}".replace('.', ','),
                f"{avg_parc:.2f}".replace('.', ','),
                f"{avg_null:.2f}".replace('.', ','),
                f"{avg_rec:.2f}".replace('.', ',')
            ]
            for c_idx, val_str in enumerate(vals_med):
                item = QTableWidgetItem(val_str)
                item.setFont(font_bold)
                item.setBackground(green_bg)
                item.setForeground(fg_color)
                table.setItem(12, c_idx + 1, item)

            # Linha 14: Total ano
            item_tot = QTableWidgetItem(tr("Total ano"))
            item_tot.setFont(font_bold)
            item_tot.setBackground(green_bg)
            item_tot.setForeground(fg_color)
            table.setItem(13, 0, item_tot)

            year_tots = monthly_stats.get('year_totals', {})
            tot_pluv_year = year_tots.get('pluvial', sum_pluv * 365.25 / 12.0)
            tot_pot_year = year_tots.get('potable', sum_pot * 365.25 / 12.0)
            tot_spill_year = year_tots.get('spilled', sum_spill * 365.25 / 12.0)

            table.setItem(13, 1, QTableWidgetItem(""))
            
            it_p = QTableWidgetItem(f"{tot_pluv_year:.0f}")
            it_p.setFont(font_bold)
            it_p.setBackground(green_bg)
            it_p.setForeground(fg_color)
            table.setItem(13, 2, it_p)

            it_po = QTableWidgetItem(f"{tot_pot_year:.0f}")
            it_po.setFont(font_bold)
            it_po.setBackground(green_bg)
            it_po.setForeground(fg_color)
            table.setItem(13, 3, it_po)

            it_sp = QTableWidgetItem(f"{tot_spill_year:.5E}".replace('E+', 'E')) if tot_spill_year > 1e6 else QTableWidgetItem(f"{tot_spill_year:.0f}")
            it_sp.setFont(font_bold)
            it_sp.setBackground(green_bg)
            it_sp.setForeground(fg_color)
            table.setItem(13, 4, it_sp)

            for c in range(5, 9):
                table.setItem(13, c, QTableWidgetItem(""))

        layout.addWidget(table)
        btn_close = QPushButton(tr("Fechar"))
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        self.setLayout(layout)
