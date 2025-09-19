import sys
from PySide6.QtWidgets import QApplication, QPushButton


class PushButton(QPushButton):

    def __init__(self, *args):
        super().__init__(self, *args)
