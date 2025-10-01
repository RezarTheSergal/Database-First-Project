from frontend.shared.ui.inputs import DateInput
from .BaseFilterWidget import BaseFilterWidget


class DateFilterWidget(BaseFilterWidget):
    """Filter widget for date fields using your UI component"""

    def _setup_ui(self):
        """Setup UI components"""
        self.input_widget = DateInput()

        # Add the input widget to this widget's layout
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        self.input_widget.dateChanged.connect(self._on_date_changed)

    def _on_date_changed(self, date):
        """Handle date change"""
        self._value = date.toString("yyyy-MM-dd")
        self.value_changed.emit(self._value)

    def get_filter_value(self) -> str:
        """Get current filter value"""
        return self.input_widget.get_value()

    def clear_value(self):
        """Clear the filter value"""
        # Reset to current date or a default date
        from PySide6.QtCore import QDate

        self.input_widget.setDate(QDate.currentDate())

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None or self.get_filter_value() == ""

    def _update_ui_value(self, value: str):
        """Update UI with value"""
        if value:
            from PySide6.QtCore import QDate

            date = QDate.fromString(value, "yyyy-MM-dd")
            self.input_widget.setDate(date)
        else:
            from PySide6.QtCore import QDate

            self.input_widget.setDate(QDate.currentDate())
