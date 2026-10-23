"""
Módulo de Interface Gráfica do Usuário (UI) do Triton.
"""

__all__ = [
    "MainWindow",
    "DatePickerLineEdit",
]

def __getattr__(name):
    if name == "MainWindow":
        from triton.ui.main_window import MainWindow
        return MainWindow
    if name == "DatePickerLineEdit":
        from triton.ui.date_picker import DatePickerLineEdit
        return DatePickerLineEdit
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

