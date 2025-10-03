from typing import Sequence
from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    items: Sequence[str] | None = None

    def __init__(self, items: Sequence[str] = [""], callback=None):
        super().__init__()
        self.clear()
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        if items:
            self.set_items(items)
        if callback is not None:
            self.currentTextChanged.connect(callback)

    def set_items(self, items: Sequence[str]) -> None:
        self.clear()
        self.addItem("--не выбрано--", None)
        self.addItems([item for item in items if item != ""])

    def get_value(self) -> str:
        return self.currentText()
