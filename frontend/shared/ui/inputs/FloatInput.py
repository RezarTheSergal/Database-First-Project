from PySide6.QtWidgets import QDoubleSpinBox
from .lib.is_null import is_null


class FloatInput(QDoubleSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min_val: float | None
    max_val: float | None
    step: float

    def __init__(
        self,
        min_val: float | None = None,
        max_val: float | None = None,
        step: float = 0.1,
        can_be_negative: bool = False,
    ):
        super().__init__()
        self.setMaximum(max_val or 1000000)
        if can_be_negative:
            self.setMinimum(min_val or -1000000)
        else:
            self.setMinimum(min_val or 0)
        self.setSingleStep(step)

        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.can_be_negative = can_be_negative

    def get_value(self) -> float:
        return float(self.text())

    def is_value_valid(self) -> bool:
        if not self.is_nullable and is_null(self.text()):
            return False
        elif not self.can_be_negative and float(self.text()) < 0:
            return False
        return True
