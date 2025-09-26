from PySide6.QtWidgets import QLineEdit
from .isNull import isNull


class BoolInput(QLineEdit):
    is_nullable: bool
    ALLOWED_VALUES: list[str] = ["true", "false"]

    def get_value(self) -> bool:
        return bool(self.text())

    def is_value_valid(self) -> bool:
        if not self.is_nullable and isNull(self.text()):
            return False
        return True
