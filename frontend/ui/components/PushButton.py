from PySide6.QtWidgets import QPushButton
from .Font import Font

button_font = Font(12, family="Roboto")

class PushButton(QPushButton):

    def __init__(
        self,
        text: str,
        callback=None,
    ):
        super().__init__()
        self.setText(text)
        self.setFont(button_font)

        if callback != None:
            self.clicked.connect(callback)
