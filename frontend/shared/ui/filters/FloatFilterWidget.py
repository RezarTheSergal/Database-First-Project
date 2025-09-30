from frontend.shared.ui.inputs import FloatInput
from .BaseFilterWidget import BaseFilterWidget


class FloatFilterWidget(BaseFilterWidget):
    """Виджет фильтра для числовых полей с плавающей точкой"""

    input_widget: FloatInput

    def _create_input_widget(self) -> FloatInput:
        self.input_widget = FloatInput()
        self.input_widget.setDecimals(2)
        self.input_widget.setMinimum(-999999999.99)
        self.input_widget.setMaximum(999999999.99)
        self.input_widget.setValue(0.0)
        return self.input_widget

    def get_filter_value(self) -> float:
        return self.input_widget.value()

    def clear_value(self):
        self.input_widget.setValue(0.0)
