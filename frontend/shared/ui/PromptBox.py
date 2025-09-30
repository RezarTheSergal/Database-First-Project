from PySide6.QtWidgets import QMessageBox, QMainWindow
from frontend.shared.ui import Widget, Modal
from .const import YesButton, NoButton


class PromptBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def prompt(
        self, parent: Widget | QMainWindow | Modal, title: str, description: str = ""
    ) -> QMessageBox.StandardButton:
        return self.question(parent, title, description, YesButton | NoButton, NoButton)
