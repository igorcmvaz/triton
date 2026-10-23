"""
Widget Helper para Tooltips Ricos com Justificativas.
Fornece wrappers para campos de entrada que exibem tooltips detalhados
quando o mouse passa sobre eles, integrado com o sistema de justificativas ambiental.
"""

from typing import Optional
from PySide6.QtWidgets import QLineEdit, QComboBox, QWidget, QCheckBox
from PySide6.QtWidgets import QToolTip

from triton.core.environmental_justifications import ParameterJustification, format_justification_as_tooltip
from triton.ui.translation import tr


class JustifiedLineEdit(QLineEdit):
    """
    QLineEdit com suporte a tooltips ricos baseados em justificativas.
    
    Uso:
        field = JustifiedLineEdit(justification=my_justification)
        # ou
        field = JustifiedLineEdit()
        field.set_justification(my_justification)
    """
    
    def __init__(self, parent=None, justification: Optional[ParameterJustification] = None):
        super().__init__(parent)
        self.justification = justification
        self.setMouseTracking(True)
    
    def set_justification(self, justification: Optional[ParameterJustification]) -> None:
        """Define a justificativa para este campo."""
        self.justification = justification
    
    def mouseDoubleClickEvent(self, event):
        """Permite o comportamento padrão de clique duplo sem exibir detalhes extras."""
        super().mouseDoubleClickEvent(event)
    
    def enterEvent(self, event):
        """Ao entrar com mouse, mostra a justificativa completa em tooltip."""
        if self.justification:
            tooltip_html = format_justification_as_tooltip(self.justification, tr=tr)
            QToolTip.showText(
                self.mapToGlobal(self.rect().center()),
                tooltip_html,
                self,
                self.rect()
            )
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Ao sair com mouse, esconde o tooltip."""
        QToolTip.hideText()
        super().leaveEvent(event)


class JustifiedComboBox(QComboBox):
    """
    QComboBox com suporte a tooltips ricos.
    
    Uso:
        combo = JustifiedComboBox(justifications_dict)
        # justifications_dict: {data_value: ParameterJustification}
    """
    
    def __init__(self, parent=None, justifications: dict = None):
        super().__init__(parent)
        self.justifications = justifications or {}
        self.setMouseTracking(True)
        self.currentIndexChanged.connect(self._on_selection_changed)
    
    def set_justifications(self, justifications: dict) -> None:
        """Define o mapa de justificativas {data_value: ParameterJustification}."""
        self.justifications = justifications
    
    def _show_current_tooltip(self):
        data = self.currentData()
        if data and data in self.justifications:
            justification = self.justifications[data]
            tooltip_html = format_justification_as_tooltip(justification, tr=tr)
            QToolTip.showText(
                self.mapToGlobal(self.rect().center()),
                tooltip_html,
                self,
                self.rect()
            )

    def _on_selection_changed(self):
        """Atualiza o tooltip quando a seleção muda."""
        self._show_current_tooltip()
    
    def mouseDoubleClickEvent(self, event):
        """Permite o comportamento padrão de clique duplo sem exibir detalhes extras."""
        super().mouseDoubleClickEvent(event)
    
    def enterEvent(self, event):
        """Mostra justificativa completa ao passar o mouse."""
        self._show_current_tooltip()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Esconde o tooltip ao sair."""
        QToolTip.hideText()
        super().leaveEvent(event)


class JustifiedCheckBox(QCheckBox):
    """
    QCheckBox com suporte a tooltip rico.
    """
    
    def __init__(self, parent=None, justification: Optional[ParameterJustification] = None):
        super().__init__(parent)
        self.justification = justification
        self.setMouseTracking(True)
    
    def set_justification(self, justification: Optional[ParameterJustification]) -> None:
        """Define a justificativa para este campo."""
        self.justification = justification
    
    def mouseDoubleClickEvent(self, event):
        """Permite o comportamento padrão de clique duplo sem exibir detalhes extras."""
        super().mouseDoubleClickEvent(event)
    
    def enterEvent(self, event):
        """Mostra justificativa completa ao passar o mouse."""
        if self.justification:
            tooltip_html = format_justification_as_tooltip(self.justification, tr=tr)
            QToolTip.showText(
                self.mapToGlobal(self.rect().center()),
                tooltip_html,
                self,
                self.rect()
            )
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Esconde ao sair."""
        QToolTip.hideText()
        super().leaveEvent(event)


