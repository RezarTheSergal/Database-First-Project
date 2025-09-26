from PySide6.QtWidgets import QDoubleSpinBox
from backend.utils.logger import logging
from .GenericInput import GenericInput

logger = logging.getLogger()


class IntInput(GenericInput, QDoubleSpinBox):

    def __init__(self, min: float = -(10.0**10), max: float = 10.0**10, **kwargs):
        super().__init__()
        if range:
            self.setRange(min, max)

    def get_value(self) -> int:
        return int(self.text())

    def is_value_valid(self):
        return self.text().isdigit()  # isdigit() means 'is integer'
