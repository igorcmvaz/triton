"""
Testes unitários para o componente DatePickerLineEdit e CalendarPopup do Netuno 5.
Verifica digitação manual livre, formatação, integração com calendário e emissão de sinais.
"""

import sys
from datetime import datetime, date
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QDate

from netuno.ui.date_picker import DatePickerLineEdit, CalendarPopup


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


def test_date_picker_default(qapp):
    picker = DatePickerLineEdit("01/01/1980")
    assert picker.text() == "01/01/1980"
    assert picker.get_date() == date(1980, 1, 1)
    assert picker.get_datetime() == datetime(1980, 1, 1)


def test_date_picker_manual_typing(qapp):
    picker = DatePickerLineEdit()
    
    # Digitação direta no formato padrão dd/mm/aaaa
    picker.setText("15/03/2012")
    assert picker.text() == "15/03/2012"
    assert picker.get_date() == date(2012, 3, 15)

    # Digitação de ano isolado (comum em modelagem de cenários climáticos)
    picker.setText("1995")
    assert picker.get_date() == date(1995, 1, 1)

    # Digitação com hífen
    picker.setText("20-08-2026")
    assert picker.get_date() == date(2026, 8, 20)

    # Texto inválido / vazio
    picker.setText("-")
    assert picker.get_date() is None

    picker.setText("")
    assert picker.get_date() is None


def test_date_picker_set_date_variants(qapp):
    picker = DatePickerLineEdit()

    # Via datetime.date
    picker.set_date(date(2005, 6, 10))
    assert picker.text() == "10/06/2005"
    assert picker.get_date() == date(2005, 6, 10)

    # Via datetime.datetime
    picker.set_date(datetime(2020, 12, 31, 14, 30))
    assert picker.text() == "31/12/2020"

    # Via QDate
    picker.set_date(QDate(2018, 5, 25))
    assert picker.text() == "25/05/2018"

    # Via string
    picker.set_date("05/08/2022")
    assert picker.text() == "05/08/2022"


def test_date_picker_signals(qapp):
    picker = DatePickerLineEdit("01/01/2000")
    received_dates = []

    picker.dateChanged.connect(lambda d: received_dates.append(d))

    picker.setText("02/02/2002")
    assert len(received_dates) >= 1
    assert received_dates[-1] == date(2002, 2, 2)


def test_calendar_popup_instantiation(qapp):
    popup = CalendarPopup(
        current_date=QDate(2024, 7, 15),
        default_preset_date=QDate(1980, 1, 1)
    )
    assert popup.calendar.selectedDate() == QDate(2024, 7, 15)
    
    # Teste de clique no botão 'Hoje'
    popup._on_today_clicked()
    assert popup.selected_date == QDate.currentDate()

    # Teste de clique no preset
    popup._on_preset_clicked()
    assert popup.selected_date == QDate(1980, 1, 1)
