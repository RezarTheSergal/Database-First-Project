from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint
from .Size import Size
from .Icon import Icon
from .Layouts import GridLayout
from .const import DEFAULT_MAX_SIZE
from ..lib.utils import setClass
from os import getcwd

ICON_PATH = getcwd() + "/frontend/images/favicon.ico"


class Modal(QWidget):

    def __init__(
        self,
        max_size: Size = DEFAULT_MAX_SIZE,
        title="NO_TITLE",
        accessible_name="",
        x: int = 0,
        y: int = 360,
    ):
        super().__init__(pos=QPoint(x, y))

        self.setWindowTitle(title)
        self.setMaximumSize(max_size.w, max_size.h)
        self.setAccessibleName(accessible_name)
        self.setWindowIcon(Icon(ICON_PATH))
        setClass(self, "modal")
        self.setFocus()

        gridLayout = GridLayout()
        self.setLayout(gridLayout)
        self.gridLayout = gridLayout

    def add(self, child: QWidget):
        self.gridLayout.addWidget(child)
