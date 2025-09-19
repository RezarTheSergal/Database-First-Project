from PySide6.QtWidgets import QLabel
from .Font import Font
from .Alignment import Alignment


class Text(QLabel):
    def __init__(
        self, text: str, font: Font, hasWordWrap=True, alignment=Alignment.Center.value
    ):
        super().__init__()
        self.setText(text)
        self.setFont(font)
        self.setWordWrap(hasWordWrap)
        self.setAlignment(alignment)
