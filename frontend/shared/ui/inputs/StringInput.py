from PySide6.QtWidgets import QLineEdit
from .lib.is_null import is_null


class StringInput(QLineEdit):
    is_nullable: bool

    def __init__(self,is_nullable:bool=False,max_input_length:int=256,**kwargs):
        super().__init__()
        self.is_nullable = is_nullable
        self.setMaxLength(max_input_length)

    def is_value_valid(self):
        if not self.is_nullable and is_null(self.text()):
            return False
        return True

    def get_value(self) -> str:
        return self.text()
