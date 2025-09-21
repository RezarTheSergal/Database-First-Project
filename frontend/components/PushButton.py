from PySide6.QtWidgets import QPushButton


class PushButton(QPushButton):
    def __init__(
        self,
        text: str,
        callback=None,
    ):
        super().__init__()
        self.setText(text)

        if callback != None:
            self.clicked.connect(callback)
