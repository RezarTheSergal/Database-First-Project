from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate
from frontend.shared.ui.inputs import DateInput
from .base import BaseFilterWidget

class DateFilterWidget(BaseFilterWidget):
    """Виджет фильтра для полей даты"""
    
    def _create_input_widget(self) -> QDateEdit:
        date_edit = DateInput()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        return date_edit
    
    def get_filter_value(self) -> str:
        return self.input_widget.date().toString("yyyy-MM-dd")
    
    def clear_value(self):
        self.input_widget.setDate(QDate.currentDate())