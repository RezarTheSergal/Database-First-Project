from typing import Sequence
from PySide6.QtWidgets import QListWidget
from .SizeAdjustPolicy import SizeAdjustPolicy


class Spinner(QListWidget):
    def __init__(self, items: Sequence[str] = [""]):
        super().__init__()
        self.set_items(items)
        self.setSizeAdjustPolicy(SizeAdjustPolicy.AdjustToContents)

    def set_items(self, items: Sequence[str]):
        self.clear()
        self.addItems(items)
