from PySide6.QtWidgets import QComboBox
from frontend.shared.ui.inputs.ComboBox import ComboBox
from .base import BaseFilterWidget
from typing import List

class EnumFilterWidget(BaseFilterWidget):
    """Виджет фильтра для ENUM полей"""
    
    def _create_input_widget(self) -> ComboBox:
        combo = ComboBox()
        
        # Добавляем пустой элемент для сброса фильтра
        enum_values = [""] + (self.column_info.get("enum_values", []))
        combo.set_items(enum_values)
        
        return combo
    
    def get_filter_value(self) -> str:
        return self.input_widget.currentText()
    
    def clear_value(self):
        self.input_widget.setCurrentIndex(0)  # Выбираем пустой элемент

