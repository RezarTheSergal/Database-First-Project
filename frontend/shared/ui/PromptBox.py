"""
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
"""

from PySide6.QtWidgets import QMessageBox, QMainWindow
from frontend.shared.ui import Widget, Modal
from .const import YesButton, NoButton
from backend.settings import ICON_PATH
from .Icon import Icon

class PromptBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def prompt(
        self, parent: Widget | QMainWindow | Modal, title: str, description: str = ""
    ):
        # создание сообщения
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(description)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        msg.setWindowIcon(Icon(ICON_PATH))

        # замена текста кнопок на русский
        msg.button(QMessageBox.StandardButton.Yes).setText("Да")
        msg.button(QMessageBox.StandardButton.No).setText("Нет")

        result = msg.exec()
        return result
