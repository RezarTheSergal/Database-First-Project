from PySide6.QtWidgets import QLineEdit
from .lib.isNull import isNull


class StringInput(QLineEdit):
    is_nullable: bool

    def __init__(self,is_nullable:bool,max_input_length:int=256):
        self.is_nullable = is_nullable
        self.setMaxLength(max_input_length)

    def is_value_valid(self):
        if not self.is_nullable and isNull(self.text()):
            return False
        return True

    def get_value(self) -> str:
        return self.text()
