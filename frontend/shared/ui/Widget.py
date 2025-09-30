from backend.utils.logger import logging
from PySide6.QtWidgets import QWidget
from frontend.shared.ui import HLayout, VLayout

logger = logging.getLogger()


def announce_missing_layout():
    logger.warning(
        "[Warning] You tried to interact with a QWidget that doesn't have a layout."
    )


class Widget(QWidget):
    layout: VLayout | HLayout

    def __init__(self, layout: HLayout | VLayout):
        super().__init__()
        self.layout = layout
        self.setLayout(self.layout)
