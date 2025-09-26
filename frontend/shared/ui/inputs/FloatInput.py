from PySide6.QtWidgets import QDoubleSpinBox
from .GenericInput import GenericInput


class FloatInput(GenericInput, QDoubleSpinBox):
    def __init__(self, min: float = -(10.0**10), max: float = 10.0**10, **kwargs):
        super().__init__()
        if range:
            self.setRange(min, max)

    def get_value(self) -> float:
        return float(self.text())
