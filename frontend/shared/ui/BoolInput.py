from PySide6.QtWidgets import QLineEdit


class BoolEdit(QLineEdit):
    def __init__(self, placeholder: str = ""):
        super().__init__()

    def get_value(self) -> bool:
        return bool(self.text())
