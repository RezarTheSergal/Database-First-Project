from PySide6.QtGui import QIcon


class Icon(QIcon):
    def __init__(self, path: str):
        super().__init__(path)


__all__ = ["Icon"]
