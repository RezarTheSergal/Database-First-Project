from .Size import Size
from .Icon import Icon
from .Layouts import GridLayout
from .Widget import Widget
from .const import DEFAULT_MAX_SIZE
from ..lib.utils import setClass
from os import getcwd

ICON_PATH = getcwd() + "/frontend/images/favicon.ico"


class Modal(Widget):

    def __init__(
        self,
        max_size: Size = DEFAULT_MAX_SIZE,
        title="NO_TITLE",
        accessible_name="",
        x: int = 0,
        y: int = 360,
    ):
        super().__init__(GridLayout())
        setClass(self, "modal")

        self.setWindowTitle(title)
        self.setMaximumSize(max_size.w, max_size.h)
        self.setAccessibleName(accessible_name)
        self.setWindowIcon(Icon(ICON_PATH))

        self.activateWindow()  # Puts window on top
        self.setFocus()
