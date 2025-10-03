from PySide6.QtWidgets import QSpinBox
from .lib.is_null import is_null

class IntInput(QSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min_val: int
    max_val: int
    step: int

    def __init__(
        self,
        min_val: int = -10**9,
        max_val: int = 10**9,
        step: int = 1,
        can_be_negative: bool = False,
        **kwargs
    ):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.can_be_negative = can_be_negative

        self.setMaximum(max_val)
        self.setSingleStep(step)

        if not can_be_negative:
            self.setMinimum(min_val if min_val >= 0 else 0)
        else:
            self.setMinimum(min_val)

    def get_value(self) -> int:
        return int(self.text())

    def is_value_valid(self):
        if not self.is_nullable and is_null(self.text()):
            return False
        elif not self.can_be_negative and int(self.text()) < 0:
            return False
        return True
