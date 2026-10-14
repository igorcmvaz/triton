"""
Diálogo para configuração do Reservatório Superior (1:1 com o Netuno 4).
Sincronização em tempo real bidirecional entre Litros e Percentual de recalque.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QLineEdit, QPushButton, QRadioButton, QButtonGroup, QMessageBox
)
from triton.ui.translation import tr


class DialogUpperTank(QDialog):
    """
    Diálogo para configuração do Reservatório Superior (1:1 com o Netuno 4).
    Sincronização em tempo real bidirecional entre Litros e Percentual de recalque.
    """
    def __init__(self, parent=None, daily_pluvial_demand=120.0, vol=500.0, mode=0, thresh_mode=1, thresh_val=10.0):
        super().__init__(parent)
        self.setWindowTitle(tr("Reservatório superior"))
        self.resize(380, 360)

        self.daily_pluvial_demand = daily_pluvial_demand
        self.upper_tank_vol = vol if mode != 0 else daily_pluvial_demand
        self.upper_tank_mode = mode  # 0: Igual à demanda, 1: Desejado, 2: Não utilizar
        self.thresh_mode = thresh_mode  # 0: Litros, 1: Percentual
        self.thresh_val = thresh_val

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        gb_mode = QGroupBox(tr("Reservatório superior"))
        gb_layout = QVBoxLayout()

        self.radio_demand = QRadioButton(tr("Volume igual à demanda diária média de água pluvial"))
        self.radio_custom = QRadioButton(tr("Entrar com volume desejado"))
        self.radio_none = QRadioButton(tr("Não utilizar reservatório superior"))

        self.bg_mode = QButtonGroup(self)
        self.bg_mode.addButton(self.radio_demand, 0)
        self.bg_mode.addButton(self.radio_custom, 1)
        self.bg_mode.addButton(self.radio_none, 2)

        if self.upper_tank_mode == 0:
            self.radio_demand.setChecked(True)
        elif self.upper_tank_mode == 1:
            self.radio_custom.setChecked(True)
        else:
            self.radio_none.setChecked(True)

        gb_layout.addWidget(self.radio_demand)
        gb_layout.addWidget(self.radio_custom)
        gb_layout.addWidget(self.radio_none)
        gb_mode.setLayout(gb_layout)
        layout.addWidget(gb_mode)

        layout.addWidget(QLabel(tr("Volume do reservatório superior (litros)")))
        init_vol_str = f"{self.upper_tank_vol:.1f}".replace('.', ',') if self.upper_tank_mode != 2 else "0"
        self.txt_vol = QLineEdit(init_vol_str)
        layout.addWidget(self.txt_vol)

        self.radio_thresh_liters = QRadioButton(tr("Volume no reservatório superior abaixo do qual há recalque (litros)"))
        thresh_lit_str = f"{self.thresh_val:.1f}".replace('.', ',') if self.thresh_mode == 0 else f"{(self.upper_tank_vol * (self.thresh_val / 100.0)):.1f}".replace('.', ',')
        self.txt_thresh_liters = QLineEdit(thresh_lit_str)

        self.radio_thresh_pct = QRadioButton(tr("Percentual do volume do reservatório superior abaixo do qual há recalque"))
        thresh_pct_str = f"{self.thresh_val:.1f}".replace('.', ',') if self.thresh_mode == 1 else "10"
        self.txt_thresh_pct = QLineEdit(thresh_pct_str)

        self.bg_thresh = QButtonGroup(self)
        self.bg_thresh.addButton(self.radio_thresh_liters, 0)
        self.bg_thresh.addButton(self.radio_thresh_pct, 1)

        if self.thresh_mode == 0:
            self.radio_thresh_liters.setChecked(True)
        else:
            self.radio_thresh_pct.setChecked(True)

        layout.addWidget(self.radio_thresh_liters)
        layout.addWidget(self.txt_thresh_liters)
        layout.addWidget(self.radio_thresh_pct)
        layout.addWidget(self.txt_thresh_pct)

        # Estilo para destacar a opção selecionada com marca de seleção clara
        self.setStyleSheet("""
            QRadioButton {
                padding: 3px;
            }
            QRadioButton:checked {
                font-weight: bold;
                color: #0369a1;
            }
        """)

        # Conexões de eventos
        self.radio_demand.toggled.connect(self.update_states)
        self.radio_custom.toggled.connect(self.update_states)
        self.radio_none.toggled.connect(self.update_states)
        
        self.radio_thresh_liters.toggled.connect(self.update_states)
        self.radio_thresh_pct.toggled.connect(self.update_states)

        self.txt_vol.textChanged.connect(self.on_vol_changed)
        self.txt_thresh_liters.textChanged.connect(self.on_thresh_liters_changed)
        self.txt_thresh_pct.textChanged.connect(self.on_thresh_pct_changed)

        row_btns = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.on_ok)
        self.btn_cancel = QPushButton(tr("Cancelar"))
        self.btn_cancel.clicked.connect(self.reject)

        row_btns.addStretch()
        row_btns.addWidget(self.btn_ok)
        row_btns.addWidget(self.btn_cancel)
        layout.addLayout(row_btns)

        self.setLayout(layout)
        self.update_states()

    def update_states(self):
        mode = self.bg_mode.checkedId()
        self.txt_vol.setEnabled(mode == 1)

        has_tank = (mode != 2)
        self.radio_thresh_liters.setEnabled(has_tank)
        self.radio_thresh_pct.setEnabled(has_tank)

        thresh_mode = self.bg_thresh.checkedId()
        self.txt_thresh_liters.setEnabled(has_tank and (thresh_mode == 0))
        self.txt_thresh_pct.setEnabled(has_tank and (thresh_mode == 1))

        if mode == 0:
            self.txt_vol.setText(f"{self.daily_pluvial_demand:.1f}".replace('.', ','))
        elif mode == 2:
            self.txt_vol.setText("0")
            self.txt_thresh_liters.setText("0")
            self.txt_thresh_pct.setText("0")

    def on_vol_changed(self):
        if self.bg_mode.checkedId() == 2:
            return
        try:
            vol = float(self.txt_vol.text().replace(',', '.'))
            if vol > 0:
                self.upper_tank_vol = vol
                self.recalc_thresholds()
        except ValueError:
            pass

    def on_thresh_liters_changed(self):
        if not self.txt_thresh_liters.hasFocus() or self.bg_mode.checkedId() == 2 or self.bg_thresh.checkedId() != 0:
            return
        try:
            lit = float(self.txt_thresh_liters.text().replace(',', '.'))
            if self.upper_tank_vol > 0:
                pct = (lit / self.upper_tank_vol) * 100.0
                self.txt_thresh_pct.blockSignals(True)
                self.txt_thresh_pct.setText(f"{pct:.1f}".replace('.', ','))
                self.txt_thresh_pct.blockSignals(False)
        except ValueError:
            pass

    def on_thresh_pct_changed(self):
        if not self.txt_thresh_pct.hasFocus() or self.bg_mode.checkedId() == 2 or self.bg_thresh.checkedId() != 1:
            return
        try:
            pct = float(self.txt_thresh_pct.text().replace(',', '.'))
            if self.upper_tank_vol > 0:
                lit = self.upper_tank_vol * (pct / 100.0)
                self.txt_thresh_liters.blockSignals(True)
                self.txt_thresh_liters.setText(f"{lit:.1f}".replace('.', ','))
                self.txt_thresh_liters.blockSignals(False)
        except ValueError:
            pass

    def recalc_thresholds(self):
        if self.upper_tank_vol <= 0:
            return
        try:
            if self.bg_thresh.checkedId() == 0:
                lit = float(self.txt_thresh_liters.text().replace(',', '.'))
                pct = (lit / self.upper_tank_vol) * 100.0
                self.txt_thresh_pct.blockSignals(True)
                self.txt_thresh_pct.setText(f"{pct:.1f}".replace('.', ','))
                self.txt_thresh_pct.blockSignals(False)
            else:
                pct = float(self.txt_thresh_pct.text().replace(',', '.'))
                lit = self.upper_tank_vol * (pct / 100.0)
                self.txt_thresh_liters.blockSignals(True)
                self.txt_thresh_liters.setText(f"{lit:.1f}".replace('.', ','))
                self.txt_thresh_liters.blockSignals(False)
        except ValueError:
            pass

    def on_ok(self):
        mode = self.bg_mode.checkedId()
        if mode == 2:
            self.upper_tank_vol = 0.0
            self.upper_tank_mode = 2
            self.thresh_mode = 1
            self.thresh_val = 0.0
            self.accept()
            return

        try:
            vol = float(self.txt_vol.text().replace(',', '.'))
            if vol <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.critical(self, tr("Erro"), tr("Volume do reservatório superior inválido."))
            return

        thresh_mode = self.bg_thresh.checkedId()
        if thresh_mode == 0:
            try:
                lit = float(self.txt_thresh_liters.text().replace(',', '.'))
                if lit < 0 or lit > vol:
                    raise ValueError()
                val = lit
            except ValueError:
                QMessageBox.critical(self, tr("Erro"), tr("Volume de gatilho de recalque inválido."))
                return
        else:
            try:
                pct = float(self.txt_thresh_pct.text().replace(',', '.'))
                if pct < 0 or pct > 100:
                    raise ValueError()
                val = pct
            except ValueError:
                QMessageBox.critical(self, tr("Erro"), tr("Percentual de gatilho de recalque inválido."))
                return

        self.upper_tank_vol = vol
        self.upper_tank_mode = mode
        self.thresh_mode = thresh_mode
        self.thresh_val = val
        self.accept()
