"""
Diálogo para entrada de dados variáveis de demanda ou moradores (1:1 com o Netuno 4).
"""

import numpy as np
from triton.core.numero import decimal, para_float
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QLineEdit, QPushButton, QRadioButton, QFileDialog, 
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from triton.ui.translation import tr


class DialogVariableInput(QDialog):
    """
    Diálogo 1:1 idêntico ao Netuno 4 para Demanda Variável ou Número de Moradores Variável.
    """
    def __init__(self, parent=None, title="Demanda variável", col_title="Demanda total de água (litros per capita/dia)", default_val=200.0):
        super().__init__(parent)
        self.setWindowTitle(tr(title))
        self.resize(360, 480)
        self.col_title = tr(col_title)
        self.default_val = default_val
        self.values = [default_val] * 12

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        gb_period = QGroupBox(tr("Periodicidade dos dados"))
        gb_lay = QHBoxLayout()
        self.radio_daily = QRadioButton(tr("Diária"))
        self.radio_monthly = QRadioButton(tr("Mensal"))
        self.radio_daily.setChecked(True)
        gb_lay.addWidget(self.radio_daily)
        gb_lay.addWidget(self.radio_monthly)
        gb_period.setLayout(gb_lay)
        layout.addWidget(gb_period)

        row_rep = QHBoxLayout()
        row_rep.addWidget(QLabel(tr("Período de repetição")))
        self.txt_repeat = QLineEdit("1")
        self.txt_repeat.setFixedWidth(60)
        row_rep.addWidget(self.txt_repeat)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setFixedWidth(60)
        self.btn_ok.clicked.connect(self.on_update_table)
        row_rep.addWidget(self.btn_ok)

        self.btn_load_file = QPushButton(tr("Carregar arquivo"))
        self.btn_load_file.clicked.connect(self.on_load_file)
        row_rep.addWidget(self.btn_load_file)
        layout.addLayout(row_rep)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels([tr("Dia"), self.col_title])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.btn_conclude = QPushButton(tr("Concluir"))
        self.btn_conclude.setFixedHeight(32)
        self.btn_conclude.clicked.connect(self.on_conclude)
        layout.addWidget(self.btn_conclude)

        self.setStyleSheet("""
            QRadioButton {
                padding: 3px;
            }
            QRadioButton:checked {
                font-weight: bold;
                color: #0369a1;
            }
        """)

        self.radio_daily.toggled.connect(self.on_update_table)
        self.radio_monthly.toggled.connect(self.on_update_table)

        self.setLayout(layout)
        self.on_update_table()

    def on_update_table(self):
        is_monthly = self.radio_monthly.isChecked()
        if is_monthly:
            self.radio_monthly.setText(f"✓ {tr('Mensal')}")
            self.radio_daily.setText(tr("Diária"))
        else:
            self.radio_daily.setText(f"✓ {tr('Diária')}")
            self.radio_monthly.setText(tr("Mensal"))

        months_pt = [
            tr("Janeiro"), tr("Fevereiro"), tr("Março"), tr("Abril"),
            tr("Maio"), tr("Junho"), tr("Julho"), tr("Agosto"),
            tr("Setembro"), tr("Outubro"), tr("Novembro"), tr("Dezembro")
        ]
        
        if is_monthly:
            self.table.setHorizontalHeaderLabels([tr("Mês"), self.col_title])
            self.table.setRowCount(12)
            for r in range(12):
                self.table.setItem(r, 0, QTableWidgetItem(months_pt[r]))
                val = self.values[r] if r < len(self.values) else self.default_val
                self.table.setItem(r, 1, QTableWidgetItem(decimal(f"{val:.1f}")))
        else:
            self.table.setHorizontalHeaderLabels([tr("Dia"), self.col_title])
            try:
                n_days = int(self.txt_repeat.text())
            except ValueError:
                n_days = 1
            n_days = max(1, min(n_days, 365))
            self.table.setRowCount(n_days)
            for r in range(n_days):
                self.table.setItem(r, 0, QTableWidgetItem(str(r + 1)))
                self.table.setItem(r, 1, QTableWidgetItem(decimal(f"{self.default_val:.1f}")))

    def on_load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, tr("Carregar Arquivo de Dados Variáveis"), "", f"{tr('Arquivos Texto/CSV')} (*.txt *.csv);;{tr('Todos')} (*.*)"
        )
        if file_path:
            try:
                arr = np.loadtxt(file_path, delimiter=';', dtype=float)
                if len(arr) > 0:
                    self.table.setRowCount(len(arr))
                    for r, val in enumerate(arr):
                        self.table.setItem(r, 0, QTableWidgetItem(str(r + 1)))
                        self.table.setItem(r, 1, QTableWidgetItem(decimal(f"{val:.1f}")))
            except Exception as e:
                QMessageBox.critical(self, tr("Erro"), f"{tr('Falha ao ler arquivo')}:\n{str(e)}")

    def on_conclude(self):
        try:
            res = []
            for r in range(self.table.rowCount()):
                item = self.table.item(r, 1)
                val = para_float(item.text()) if item else self.default_val
                res.append(val)
            self.values = res
            self.accept()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Verifique os valores numéricos inseridos."))
