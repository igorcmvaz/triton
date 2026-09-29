"""
Módulo de Interface Gráfica do Usuário (UI) do Netuno 5.
"""

__all__ = [
    "MainWindow",
    "DatePickerLineEdit",
]

def __getattr__(name):
    if name == "MainWindow":
        from netuno.ui.main_window import MainWindow
        return MainWindow
    if name == "DatePickerLineEdit":
        from netuno.ui.date_picker import DatePickerLineEdit
        return DatePickerLineEdit
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

