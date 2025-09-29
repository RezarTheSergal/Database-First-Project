from PySide6.QtWidgets import QLabel
from ..Alignment import Alignment
from .Font import Font


class Text(QLabel):

    def __init__(
        self,
        text: str,
        hasWordWrap=True,
        alignment=Alignment.Center.value,
        font: Font | None = None,
    ):
        super().__init__()

        self.setText(text)
        self.setWordWrap(hasWordWrap)
        self.setAlignment(alignment)

        if font is not None:
            self.setFont(font)
