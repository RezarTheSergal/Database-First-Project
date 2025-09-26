from PySide6.QtCore import QDate
from frontend.shared.ui.inputs import DateInput
from .BaseFilterWidget import BaseFilterWidget


class DateFilterWidget(BaseFilterWidget):
    """Виджет фильтра для полей даты"""

    input_widget: DateInput

    def _create_input_widget(self) -> DateInput:
        date_edit = DateInput()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        return date_edit

    def get_filter_value(self) -> str:
        return self.input_widget.date().toString("yyyy-MM-dd")

    def clear_value(self):
        self.input_widget.setDate(QDate.currentDate())
