from PySide6.QtWidgets import QSpinBox
from .lib.is_null import is_null

class IntInput(QSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min_val: int | None
    max_val: int | None
    step: int

    def __init__(
        self,
        min_val: int | None = None,
        max_val: int | None = None,
        step: int = 1,
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

    def get_value(self) -> int:
        return int(self.text())

    def is_value_valid(self):
        if not self.is_nullable and is_null(self.text()):
            return False
        elif not self.can_be_negative and int(self.text()) < 0:
            return False
        return True
