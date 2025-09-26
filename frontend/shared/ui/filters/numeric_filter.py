from PySide6.QtWidgets import QSpinBox, QDoubleSpinBox
from frontend.shared.ui.inputs import IntInput, FloatInput
from .base import BaseFilterWidget

class IntegerFilterWidget(BaseFilterWidget):
    """Виджет фильтра для целочисленных полей"""
    
    def _create_input_widget(self) -> QSpinBox:
        spin = IntInput()
        spin.setMinimum(-2147483648)
        spin.setMaximum(2147483647)
        spin.setValue(0)
        return spin
    
    def get_filter_value(self) -> int:
        return self.input_widget.value()
    
    def clear_value(self):
        self.input_widget.setValue(0)

class FloatFilterWidget(BaseFilterWidget):
    """Виджет фильтра для числовых полей с плавающей точкой"""
    
    def _create_input_widget(self) -> QDoubleSpinBox:
        spin = FloatInput()
        spin.setDecimals(2)
        spin.setMinimum(-999999999.99)
        spin.setMaximum(999999999.99)
        spin.setValue(0.0)
        return spin
    
    def get_filter_value(self) -> float:
        return self.input_widget.value()
    
    def clear_value(self):
        self.input_widget.setValue(0.0)
