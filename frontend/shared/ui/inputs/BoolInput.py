from PySide6.QtWidgets import QLineEdit, QCheckBox
from .lib.is_null import is_null
from .BaseInput import BaseInput

class BoolInput(BaseInput,QLineEdit):
    is_nullable: bool
    ALLOWED_VALUES: list[str] = ["true", "false"]

    def __init__(self,**kwargs):
        super().__init__()

    def get_value(self) -> bool:
        return bool(self.text())

    def is_value_valid(self) -> bool:
        if not self.is_nullable and is_null(self.text()):
            return False
        return True


class BoolEditCheckBox(BaseInput,QCheckBox):
    def __init__(self,**kwargs):
        super().__init__()

    def get_value(self) -> bool:
        return bool(self.isChecked())

    def is_value_valid(self) -> bool:
        return True