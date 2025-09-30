from PySide6.QtWidgets import QCheckBox
from .BaseFilterWidget import BaseFilterWidget


class BooleanFilterWidget(BaseFilterWidget):
    """Виджет фильтра для булевых полей"""

    input_widget: QCheckBox

    def _create_input_widget(self) -> QCheckBox:
        self.input_widget = QCheckBox("Включено")
        return self.input_widget

    def get_filter_value(self) -> bool:
        return self.input_widget.isChecked()

    def clear_value(self):
        self.input_widget.setChecked(False)
