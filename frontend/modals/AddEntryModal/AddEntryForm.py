from PySide6.QtWidgets import QFormLayout, QWidget
from frontend.shared.ui import Spinner


class AddEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        self.setLayout(layout)

        self.table_name_spinner_box = Spinner(["1", "2", "3"])
        layout.addWidget(self.table_name_spinner_box)
