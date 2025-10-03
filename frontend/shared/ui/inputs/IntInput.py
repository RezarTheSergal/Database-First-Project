from PySide6.QtWidgets import QSpinBox
from .BaseInput import BaseInput
from .lib.is_null import is_null

class IntInput(BaseInput,QSpinBox):
    is_nullable: bool
    can_be_negative: bool
    min_val: int
    max_val: int
    step: int

    def __init__(
        self,
        is_nullable: bool = False,
        min_val: int = -10**9,
        max_val: int = 10**9,
        step: int = 1,
        can_be_negative: bool = False,
        **kwargs
    ):
        super().__init__()
        self.is_nullable = is_nullable
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

    def is_zero(self) -> bool:
        return self.get_value() == 0

    def is_negative(self) -> bool:
        return self.get_value() < 0

    def is_positive(self) -> bool:
        return self.get_value() > 0

    def is_in_range(self) -> bool:
        return self.min_val <= self.get_value() <= self.max_val

    def is_zero_or_less(self) -> bool:
        return self.get_value() <= 0

    def get_value(self) -> int:
        return int(self.text())

    def is_empty(self) -> bool:
        return is_null(self.text())

    def is_value_valid(self) -> bool:
        if not self.is_nullable and self.is_empty():
            return False
        elif not self.can_be_negative and self.is_negative():
            return False
        return True