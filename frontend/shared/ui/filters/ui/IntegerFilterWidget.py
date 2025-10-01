from frontend.shared.ui.inputs import IntInput
from .BaseFilterWidget import BaseFilterWidget


class IntegerFilterWidget(BaseFilterWidget):
    """Filter widget for integer fields using your UI component"""

    def _setup_ui(self):
        """Setup UI components"""
        # Extract min/max from column info
        min_val = self.column_info.get("min", None)
        max_val = self.column_info.get("max", None)
        # You might need to determine if negative values are allowed
        can_be_negative = self.column_info.get("can_be_negative", False)

        self.input_widget = IntInput(
            min_val=min_val, max_val=max_val, can_be_negative=can_be_negative
        )

        # Add the input widget to this widget's layout (inherited from BaseFilterWidget)
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        self.input_widget.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value):
        """Handle value change"""
        self._value = value
        self.value_changed.emit(value)

    def get_filter_value(self) -> int:
        """Get current filter value"""
        return self.input_widget.get_value()

    def clear_value(self):
        """Clear the filter value"""
        self.input_widget.setValue(0)  # Default to 0 or min value

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None or self.get_filter_value() == 0

    def _update_ui_value(self, value: int):
        """Update UI with value"""
        if value is not None:
            self.input_widget.setValue(value)
        else:
            self.input_widget.setValue(0)
