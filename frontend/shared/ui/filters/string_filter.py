from PySide6.QtWidgets import QLineEdit
from frontend.shared.ui.inputs import StringInput
from .base import BaseFilterWidget

class StringFilterWidget(BaseFilterWidget):
    """Виджет фильтра для строковых полей"""
    
    def _create_input_widget(self) -> QLineEdit:
        edit = StringInput()
        edit.setPlaceholderText("Введите текст для поиска...")
        return edit
    
    def get_filter_value(self) -> str:
        return self.input_widget.text().strip()
    
    def clear_value(self):
        self.input_widget.clear()