from frontend.shared.ui.inputs import IntInput
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
        return self.input_widget.value()

    def clear_value(self):
        self.input_widget.setValue(0)
