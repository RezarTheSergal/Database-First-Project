from PySide6.QtWidgets import QDateEdit
from .isNull import isNull

allowed_characters = "1234567890."


class DateInput(QDateEdit):
    is_nullable: bool

    def get_value(self) -> str:
        return str(self.text())

    def is_value_valid(self):
        value = self.get_value()
        if not self.is_nullable and isNull(self.text()):
            return False
        return all(c in allowed_characters for c in value)
