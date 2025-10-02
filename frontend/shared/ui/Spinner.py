from typing import Sequence
from PySide6.QtWidgets import QListWidget
from ..ui.core.SizeAdjustPolicy import SizeAdjustPolicy


class Spinner(QListWidget):

    def __init__(self, items: Sequence[str] = [""], callback=None):
        super().__init__()
        self.set_items(items)
        self.setSizeAdjustPolicy(SizeAdjustPolicy.AdjustToContents)
        if callback is not None:
            self.currentItemChanged.connect(callback)

    def set_items(self, items: Sequence[str]) -> None:
        self.clear()
        self.addItems(items)

    def get_current_item_text(self) -> str:
        return self.currentItem().text()
