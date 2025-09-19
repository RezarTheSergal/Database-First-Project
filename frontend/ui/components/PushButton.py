from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot

class PushButton(QPushButton):

    def __init__(
        self, text: str, font: QFont, minw: int = 175, minh: int = 50, callback=None
    ):
        super().__init__()
        self.callback = callback
        self.setText(text)
        self.setFont(font)
        self.setMinimumSize(minw, minh)

    @Slot(bool)
    def _handle_click(self, isChecked):
        if self.callback:
            self.callback(isChecked)
