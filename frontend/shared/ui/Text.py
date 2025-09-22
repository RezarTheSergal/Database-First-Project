from PySide6.QtWidgets import QLabel
from .Alignment import Alignment


class Text(QLabel):
    def __init__(
        self,
        text: str,
        hasWordWrap=True,
        alignment=Alignment.Center.value,
    ):
        super().__init__()
        self.setText(text)
        self.setWordWrap(hasWordWrap)
        self.setAlignment(alignment)
