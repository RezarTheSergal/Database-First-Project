import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtCore import Slot


class PushButton(QPushButton):
    def __init__(self, *args):
        super().__init__(self, *args)


app = QApplication(sys.argv)

btn = PushButton("Hello World!")

app.exec()
