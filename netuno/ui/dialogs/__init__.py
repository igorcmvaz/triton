"""
Módulo de Diálogos e Modais da Interface Gráfica do Netuno.
"""

from netuno.ui.dialogs.dialog_upper_tank import DialogUpperTank
from netuno.ui.dialogs.dialog_variable_input import DialogVariableInput
from netuno.ui.dialogs.dialog_monthly_values import DialogMonthlyValues
from netuno.ui.dialogs.dialog_validation_report import DialogValidationReport
from netuno.ui.dialogs.dialog_economic import (
    DialogLowerTankVol,
    DialogTariffs,
    DialogWaterEstimates,
    DialogInitialCosts,
    DialogElectricity,
    DialogMotobomba,
    DialogOtherOpCosts,
    DialogCashFlow,
    DialogEconomicAnalysis
)

from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog

__all__ = [
    "DialogUpperTank",
    "DialogVariableInput",
    "DialogMonthlyValues",
    "DialogValidationReport",
    "DialogLowerTankVol",
    "DialogTariffs",
    "DialogWaterEstimates",
    "DialogInitialCosts",
    "DialogElectricity",
    "DialogMotobomba",
    "DialogOtherOpCosts",
    "DialogCashFlow",
    "DialogEconomicAnalysis",
    "PumpSelectionWizardDialog",
]
