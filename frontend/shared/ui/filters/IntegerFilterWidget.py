from frontend.shared.ui.inputs import IntInput, FloatInput
from .BaseFilterWidget import BaseFilterWidget


class IntegerFilterWidget(BaseFilterWidget):
    """Виджет фильтра для целочисленных полей"""

    input_widget: IntInput

    def _create_input_widget(self) -> IntInput:
        spin = IntInput()
        spin.setMinimum(-2147483648)
        spin.setMaximum(2147483647)
        spin.setValue(0)
        return spin

    def get_filter_value(self) -> int:
        return self.input_widget.get_value()

    def clear_value(self):
        self.input_widget.setValue(0)


class FloatFilterWidget(BaseFilterWidget):
    """Виджет фильтра для числовых полей с плавающей точкой"""

    input_widget: FloatInput

    def _create_input_widget(self) -> FloatInput:
        spin = FloatInput()
        spin.setDecimals(2)
        spin.setMinimum(-999999999.99)
        spin.setMaximum(999999999.99)
        spin.setValue(0.0)
        return spin

    def get_filter_value(self) -> float:
        return self.input_widget.get_value()

    def clear_value(self):
        self.input_widget.setValue(0.0)
