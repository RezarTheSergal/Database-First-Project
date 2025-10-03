from PySide6.QtWidgets import QTableWidgetItem
from frontend.shared.ui import Icon

class TableItem(QTableWidgetItem):
    def __init__(self, value, icon: Icon | None = None) -> None:
        super().__init__()
        self.setText(value)
        if icon is not None:
            self.setIcon(icon)
