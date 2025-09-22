from os import getcwd
from PySide6.QtWidgets import QWidget
from backend.repository import get_tablenames
from frontend.shared.ui import HLayout, Spinner, PushButton, Icon

class TableControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.table_name_spinner_box = Spinner(get_tablenames())
        self.sort_button = PushButton(
            icon=Icon(getcwd() + "/frontend/images/icons/icons8-sort-50.png")
        )

        layout = HLayout()
        self.setLayout(layout)
        layout.add_children([self.table_name_spinner_box, self.sort_button])
