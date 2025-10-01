from PySide6.QtWidgets import QPushButton
from .Icon import Icon

class PushButton(QPushButton):

    def __init__(
        self,
        text: str = "",
        icon: Icon | None = None,
        callback=None,
    ):
        super().__init__()
        self.setText(text)

        if icon is not None:
            self.setIcon(icon)
        if callback is not None:
            self.clicked.connect(callback)
