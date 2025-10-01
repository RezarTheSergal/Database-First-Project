from frontend.shared.ui.inputs.ComboBox import ComboBox
from .BaseFilterWidget import BaseFilterWidget


class EnumFilterWidget(BaseFilterWidget):
    """Виджет фильтра для ENUM полей"""

    input_widget: ComboBox

    def _create_input_widget(self) -> ComboBox:
        self.input_widget = ComboBox()

        # Добавляем пустой элемент для сброса фильтра
        enum_values = (self.column_info.get("enum_values", []))
        self.input_widget.set_items(enum_values)

        return self.input_widget

    def get_filter_value(self) -> str:
        return self.input_widget.currentText()

    def clear_value(self):
        self.input_widget.setCurrentIndex(0)  # Выбираем пустой элемент
