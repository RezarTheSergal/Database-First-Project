from PySide6.QtWidgets import QMessageBox
from backend.settings import ICON_PATH
from .Icon import Icon

class PromptBox(QMessageBox):
    def __init__(self):
        super().__init__()

    def prompt(
        self, title: str, description: str = ""
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
