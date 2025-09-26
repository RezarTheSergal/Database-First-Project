from PySide6.QtWidgets import QDateEdit


class DateInput(QDateEdit):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def get_value(self) -> str:
        return str(self.text())
