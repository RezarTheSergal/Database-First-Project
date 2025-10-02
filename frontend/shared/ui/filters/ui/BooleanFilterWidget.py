from frontend.shared.ui.inputs import BoolEditCheckBox
from .BaseFilterWidget import BaseFilterWidget


class BooleanFilterWidget(BaseFilterWidget):
    """Filter widget for boolean fields using your UI component"""

    def _setup_ui(self):
        """Setup UI components"""
        self.input_widget = BoolEditCheckBox()

        # Add the input widget to this widget's layout
        self.layout.addWidget(self.input_widget)

    def _setup_connections(self):
        """Setup signal connections"""
        self.input_widget.stateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state):
        """Handle state change"""
        self._value = bool(state)
        self.value_changed.emit(self._value)

    def get_filter_value(self) -> bool:
        """Get current filter value"""
        return self.input_widget.get_value()

    def clear_value(self):
        """Clear the filter value"""
        self.input_widget.setChecked(False)

    def is_empty(self):
        """Check if the filter is empty"""
        return self.get_filter_value() is None

    def _update_ui_value(self, value: bool):
        """Update UI with value"""
        if value is not None:
            self.input_widget.setChecked(bool(value))
        else:
            self.input_widget.setChecked(False)
