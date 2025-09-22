from PySide6.QtCore import QSize


class Size(QSize):
    def __init__(self, w: int, h: int) -> None:
        super().__init__()
        self.w = w
        self.h = h
        self.setWidth(w)
        self.setHeight(h)
