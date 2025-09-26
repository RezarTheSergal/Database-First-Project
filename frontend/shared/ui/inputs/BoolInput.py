from PySide6.QtWidgets import QLineEdit, QCheckBox
from .GenericInput import GenericInput


class BoolEdit(GenericInput, QLineEdit):
    ALLOWED_VALUES: list[str] = ["true", "false"]

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.set_allowed_values(self.ALLOWED_VALUES)

    def get_value(self) -> bool:
        return bool(self.text())

    def is_value_valid(self) -> bool:
        return super().is_value_valid(True)

class BoolEditCheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get_value(self) -> bool:
        return bool(self.isChecked())