from PySide6.QtWidgets import QWidget
from .Icon import Icon
from .Size import Size


class Modal(QWidget):
    def __init__(
        self,
        max_size: Size = Size(400, 400),
        icon_path: str = "",
        title="NO_TITLE",
        accessible_name="",
    ):
        super().__init__()

        self.setWindowTitle(title)
        self.setMaximumSize(max_size.w, max_size.h)
        self.setAccessibleName(accessible_name)
        if len(icon_path) > 0:
            self.setWindowIcon(Icon(icon_path))
