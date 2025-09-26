from typing import Sequence
from PySide6.QtWidgets import QComboBox


class ComboBoxClass(QComboBox):

    def __init__(self, items: Sequence[str] = [""], callback=None):
        super().__init__()
        self.set_items(items)
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        if callback is not None:
            self.currentTextChanged.connect(callback)

    def set_items(self, items: Sequence[str]) -> None:
        self.clear()
        self.addItems(items)

    def get_current_item_text(self) -> str:
        return self.currentText()
