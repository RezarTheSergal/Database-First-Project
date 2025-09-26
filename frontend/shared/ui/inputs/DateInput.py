from PySide6.QtWidgets import QDateEdit
from .GenericInput import GenericInput

allowed_characters = "1234567890."


class DateInput(GenericInput, QDateEdit):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get_value(self) -> str:
        return str(self.text())

    def is_value_valid(self):
        value = self.get_value()
        return all(c in allowed_characters for c in value)
