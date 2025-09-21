from PySide6.QtWidgets import QWidget
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
    ):
        super().__init__()

        self.setWindowTitle(title)
        self.setMaximumSize(max_size.w, max_size.h)
        self.setAccessibleName(accessible_name)
        self.setWindowIcon(Icon(ICON_PATH))
        setClass(self, "modal")
        self.setFocus()

        gridLayout = GridLayout()
        self.setLayout(gridLayout)
        self.gridLayout = gridLayout
