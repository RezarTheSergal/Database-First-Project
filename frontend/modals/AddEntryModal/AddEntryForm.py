from PySide6.QtWidgets import QFormLayout, QWidget


class AddEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QFormLayout())
