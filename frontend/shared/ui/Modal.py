from .core.Size import Size
from .Icon import Icon
from .Layouts import VLayout
from .Widget import Widget
from backend.settings import ICON_PATH
from frontend.shared.lib.utils import setClass

FULL_HD:Size = Size(1920,1080)

class Modal(Widget):
    def __init__(
        self,
        parent,
        max_size: Size = FULL_HD,
        title="NO_TITLE",
        accessible_name="",
    ):
        super().__init__(VLayout())
        setClass(self, "modal")
        self.setWindowTitle(title)
        self.setMaximumSize(max_size.w, max_size.h)
        self.setAccessibleName(accessible_name)
        self.setWindowIcon(Icon(ICON_PATH))

        self.activateWindow()  # Puts window on top
        self.setFocus()

        self.main_window = parent

    def closeEvent(self, event):
        # Re-enable the main window when this widget is closed
        if self.main_window:
            self.main_window.setEnabled(True)
        event.accept()
