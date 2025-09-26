from frontend.shared.ui.inputs import StringInput
from .BaseFilterWidget import BaseFilterWidget


class StringFilterWidget(BaseFilterWidget):
    """Виджет фильтра для строковых полей"""

    input_widget: StringInput

    def _create_input_widget(self) -> StringInput:
        edit = StringInput()
        edit.setPlaceholderText("Введите текст для поиска...")
        return edit

    def get_filter_value(self) -> str:
        return self.input_widget.text().strip()

    def clear_value(self):
        self.input_widget.clear()
