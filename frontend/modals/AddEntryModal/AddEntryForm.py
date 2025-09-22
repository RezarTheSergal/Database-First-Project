from PySide6.QtWidgets import QFormLayout, QWidget
from frontend.shared.ui import Spinner
from backend.repository import get_tablenames


class AddEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        self.setLayout(layout)

        self.table_name_spinner_box = Spinner(get_tablenames())
        layout.addWidget(self.table_name_spinner_box)
