from backend.utils.logger import logging
from PySide6.QtWidgets import QWidget
from frontend.shared.ui import HLayout, VLayout, GridLayout

logger = logging.getLogger()


def announce_missing_layout():
    logger.warning(
        "[Warning] You tried to interact with a QWidget that doesn't have a layout."
    )


class Widget(QWidget):
    _layout = None

    def __init__(self, layout: HLayout | VLayout | GridLayout):
        super().__init__()
        if layout != None:
            self._layout = layout
            self.setLayout(self._layout)

    def add_children(self, children: list[QWidget]):
        if self._layout != None:
            self._layout.add_children(children)
        else:
            announce_missing_layout()

    def set_children(self, children: list[QWidget]):
        if self._layout != None:
            self._layout.set_children(children)
        else:
            announce_missing_layout()

    def clean(self):
        if self._layout != None:
            self._layout.clean()
        else:
            announce_missing_layout()
