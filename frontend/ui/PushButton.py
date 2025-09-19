from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont

class PushButton(QPushButton):

    def __init__(self, text: str, font: QFont, minw: int = 175, minh: int = 50):
        super().__init__()
        self.setText(text)
        self.setFont(font)
        self.setMinimumSize(minw, minh)
