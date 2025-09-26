from PySide6.QtWidgets import QSpinBox
from backend.utils.logger import logging
from .GenericInput import GenericInput

logger = logging.getLogger()


class IntInput(GenericInput, QSpinBox):

    def __init__(self, min: int = -(10**9), max: int = 10**9, **kwargs):
        super().__init__()
        if range:
            self.setRange(min, max)

    def get_value(self) -> int:
        return int(self.text())

    def is_value_valid(self):
        return self.text().isdigit()  # isdigit() means 'is integer'
