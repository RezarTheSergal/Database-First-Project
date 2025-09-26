from PySide6.QtWidgets import QSpinBox
from .isNull import isNull

class IntInput(QSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min: float
    max: float

    def get_value(self) -> int:
        return int(self.text())

    def is_value_valid(self):
        if not self.is_nullable and isNull(self.text()):
            return False
        elif not self.can_be_negative and int(self.text()) < 0:
            return False
        return True
