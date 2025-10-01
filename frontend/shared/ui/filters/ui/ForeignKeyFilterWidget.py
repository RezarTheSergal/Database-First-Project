from frontend.shared.ui.inputs import ForeignKeySearchBox
from .BaseFilterWidget import BaseFilterWidget


class ForeignKeyFilterWidget(BaseFilterWidget):
    """Filter widget for foreign key fields using your UI component"""

    def _setup_ui(self):
        """Setup UI components"""
        # Extract foreign key info from column metadata
        foreign_keys = self.column_info.get("foreign_keys", [])
        if not foreign_keys:
            raise ValueError(f"No foreign key info for column {self.column_name}")

        fk_info = foreign_keys[0]
        target_table = fk_info.get("target_table", "")
        display_column = fk_info.get("display_column", "name")  # Default display column
        id_column = fk_info.get("id_column", "id")  # Default id column

        self.input_widget = ForeignKeySearchBox(
            target_table=target_table,
            display_column=display_column,
            id_column=id_column,
        )

        # Add the input widget to this widget's layout
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        self.input_widget.currentIndexChanged.connect(self._on_index_changed)

    def _on_index_changed(self, index):
        """Handle index change"""
        self._value = self.input_widget.get_filter_value()
        self.value_changed.emit(self._value)

    def get_filter_value(self):
        """Get current filter value"""
        return self.input_widget.get_filter_value()

    def clear_value(self):
        """Clear the filter value"""
        self.input_widget.clear()
        self.input_widget.selected_id = None

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None

    def _update_ui_value(self, value):
        """Update UI with value"""
        # For a foreign key search box, we might need to update based on ID
        if value is not None:
            # This would require additional logic to set the display text based on the ID
            # For now, we'll just clear and set the selected ID
            self.input_widget.selected_id = value
            # You might need to fetch the display text from the database and set it
        else:
            self.input_widget.clear()
            self.input_widget.selected_id = None
