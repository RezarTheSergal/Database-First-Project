from frontend.shared.ui.inputs import ForeignKeySearchBox
from .BaseFilterWidget import BaseFilterWidget

class ForeignKeyFilterWidget(BaseFilterWidget):
    """Filter widget for foreign key fields - coordinates UI and filter logic"""

    def _setup_ui(self):
        """Setup UI components"""
        # Create ForeignKeySearchBox with the same parameters
        self.input_widget = ForeignKeySearchBox(
            column_name=self.column_name,
            column_info=self.column_info,
            parent=self
        )

        # Add the input widget to this widget's layout
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        # Connect to the ForeignKeySearchBox's selection_changed signal
        self.input_widget.selection_changed.connect(self._on_selection_changed)

    def _on_selection_changed(self, selected_id):
        """Handle selection change from ForeignKeySearchBox"""
        self._value = selected_id
        self.value_changed.emit(self._value)

    def get_filter_value(self):
        """Get current filter value"""
        return self.input_widget.get_filter_value()

    def clear_value(self):
        """Clear the filter value"""
        self.input_widget.clear()
        self.input_widget.selected_id = None
        self._value = None

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None

    def _update_ui_value(self, value):
        """Update UI with value"""
        self.input_widget.set_selected_value(value)
        self._value = value