from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QIcon


class TableItem(QTableWidgetItem):
    def __init__(self, value, icon: QIcon | None = None):
        super().__init__()
        self.setText(value)
        if icon != None:
            self.setIcon(icon)
