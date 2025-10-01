from frontend.shared.ui.inputs import StringInput
from .BaseFilterWidget import BaseFilterWidget


class StringFilterWidget(BaseFilterWidget):
    """Filter widget for string fields using your UI component"""

    def _setup_ui(self):
        """Setup UI components"""
        self.input_widget = StringInput(False)

        # Add the input widget to this widget's layout
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        self.input_widget.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text):
        """Handle text change"""
        self._value = text
        self.value_changed.emit(text)

    def get_filter_value(self) -> str:
        """Get current filter value"""
        return self.input_widget.get_value()

    def clear_value(self):
        """Clear the filter value"""
        self.input_widget.clear()

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None or self.get_filter_value() == ""

    def _update_ui_value(self, value: str):
        """Update UI with value"""
        if value is not None:
            self.input_widget.setText(str(value))
        else:
            self.input_widget.clear()
