from PySide6.QtWidgets import QLineEdit


class StringInput(QLineEdit):
    def __init__(self, placeholder: str = "") -> None:
        super().__init__()
        self.setMaximumHeight(30)

    def get_value(self) -> str:
        return self.text()
