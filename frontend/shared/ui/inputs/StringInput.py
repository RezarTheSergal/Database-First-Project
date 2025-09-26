from PySide6.QtWidgets import QLineEdit
from .isNull import isNull


class StringInput(QLineEdit):
    is_nullable: bool

    def is_value_valid(self):
        if not self.is_nullable and isNull(self.text()):
            return False
        return True

    def get_value(self) -> str:
        return self.text()

    def clear_value(self):
        self.setText("")
