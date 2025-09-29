from PySide6.QtWidgets import QDoubleSpinBox
from .isNull import isNull


class FloatInput(QDoubleSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min: float
    max: float

    def get_value(self) -> float:
        return float(self.text())

    def is_value_valid(self) -> bool:
        if not self.is_nullable and isNull(self.text()):
            return False
        elif not self.can_be_negative and float(self.text()) < 0:
            return False
        return True
